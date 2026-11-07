# ProximaConfig.Tests.ps1 - wp1271 r4 focused harness for Read-ProximaConfig; self-contained, no Pester.
# The SAME harness and ID set run on any tree via explicit -ModulePath (baseline or candidate), e.g.
#   powershell.exe|pwsh.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File <copy>\ProximaConfig.Tests.ps1 `
#     -ModulePath <tree>\.agents\skills\proxima-control\scripts\ProximaConfig.psm1 -RepositoryRoot <tree> `
#     -ScratchRoot <existing dir outside the tree> -ReportPath <json outside the tree> [-VhdFixture] `
#     [-Counterexamples [-EvidenceRoot <durable dir outside the tree; default ScratchRoot>]]
# rc 0: every required ID ran once and passed AND cleanup was verified. rc 1: a case failed (an absent module/API fails
# each case with API_ABSENT; every case still executes). rc 2: setup or cleanup error - never a test outcome; the report
# is written on every path. Required: 21 mandatory IDs, plus closure A3-08 with -VhdFixture (r4 acceptance runs give
# it). Optional A3-07 (8.3) and A3-08 without -VhdFixture are 'unavailable', never a pass.
# -VhdFixture (elevated admin; diskpart, mountvol): ONE fresh expandable 64 MB VHD inside this run's scratch, selected
# only by its new file path, given a free letter and mounted under the fixture repository; always detached in cleanup.
# -Counterexamples keeps every child's command, rc, original report, output and SHA256 in a run-specific evidence
# directory OUTSIDE the scratch tree. Credit needs the named BEHAVIOURAL failure; WRONG_CODE never earns it. Helpers are
# alias-free (H0's helper R lost to the default alias r, which stays).
[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$ModulePath, [Parameter(Mandatory = $true)][string]$ScratchRoot,
    [string]$ReportPath = '', [string]$RepositoryRoot = '', [string]$SamplePath = '', [string]$EvidenceRoot = '',
    [switch]$Counterexamples, [switch]$VhdFixture, [switch]$InjectCleanupFailure)
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$Ids = 'A1-01', 'A1-02', 'A2-01', 'A2-02', 'A2-03', 'A2-04', 'A2-05', 'A2-06', 'A2-07', 'A3-01', 'A3-02', 'A3-03', 'A3-04', 'A3-05', 'A3-06',
'A4-01', 'A5-01', 'A5-02', 'A6-01', 'A6-02', 'A5-03'
$Closure = @('A3-08')
$Results = [Collections.Generic.List[object]]::new()
$Cleanup = [ordered]@{ status = 'not_run'; errors = [Collections.Generic.List[string]]::new(); subst = [Collections.Generic.List[object]]::new(); vhd = $null
    tree_removed = $false; keep_sentinel_intact = $null; mappings_before = $null; mappings_after = $null }
$Report = [ordered]@{ schema = 'proxima_config_tests.v3'; ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"
    module_path = $ModulePath; module_sha256 = $null; sample_sha256 = $null; harness_sha256 = $null; api_state = 'unknown'
    alias_r = $null; subst_drive = $null; subst_junction_drive = $null; short_name_alias = $null; vhd_fixture = [bool]$VhdFixture; setup_error = $null
    mandatory_ids = $Ids; optional_ids = @('A3-07'); closure_ids = $Closure; counterexample_ids = @(); scratch = $null; evidence_dir = $null
    total = 0; passed = 0; failed = 0; failed_ids = @(); setup_error_ids = @(); unavailable_ids = @(); cases = $Results
    counterexample_evidence = [Collections.Generic.List[object]]::new(); cleanup = $Cleanup }
$Utf8 = [Text.UTF8Encoding]::new($false); $Sha = [Security.Cryptography.SHA256]::Create()
$Sys = [Environment]::SystemDirectory; $SubstExe = "$Sys\subst.exe"; $DiskpartExe = "$Sys\diskpart.exe"; $MountvolExe = "$Sys\mountvol.exe"
$S = $null; $FullScratch = $null; $Keep = $null; $KeepSha = $null; $Vhd = $null; $Evid = $null; $Locked = $null; $Completing = $false
function Get-FileSha256([string]$P) { if ($P -and [IO.File]::Exists($P)) { ([BitConverter]::ToString($Sha.ComputeHash([IO.File]::ReadAllBytes($P))) -replace '-').ToLowerInvariant() } }
# Native fixture tools (subst, diskpart, mountvol, child harness): output captured, rc returned, never thrown away.
function Invoke-Native([string]$Exe, [string[]]$ArgList) {
    $ErrorActionPreference = 'Continue'; $out = & $Exe @ArgList 2>&1 | Out-String
    return [pscustomobject]@{ rc = $LASTEXITCODE; out = $out }
}
# Deletes $Root bottom-up, never following a reparse point: junctions, symlinks and mount folders (dangling, nested or
# cyclic) are removed as links, so no target is touched. Not recursive Directory.Delete: on a junction it calls
# DeleteVolumeMountPoint, which failed 'The parameter is incorrect' in H1 (rc 2). Errors are collected, never ignored.
function Remove-OwnedTree([string]$Root, $Errors) {
    if ([int][IO.File]::GetAttributes($Root) -band 0x400) { $Errors.Add("refusing to recurse into reparse point $Root"); return }
    foreach ($p in [IO.Directory]::GetFileSystemEntries($Root)) {
        try {
            $a = [int][IO.File]::GetAttributes($p)
            if ($a -band 0x400) { if ($a -band 0x10) { [IO.Directory]::Delete($p) } else { [IO.File]::Delete($p) } }
            elseif ($a -band 0x10) { Remove-OwnedTree $p $Errors }
            else { if ($a -band 1) { [IO.File]::SetAttributes($p, [IO.FileAttributes]::Normal) }; [IO.File]::Delete($p) }
        } catch { $Errors.Add("$p :: $($_.Exception.Message)") }
    }
    try { [IO.Directory]::Delete($Root) } catch { $Errors.Add("$Root :: $($_.Exception.Message)") }
}
# Tree listing that records reparse points as such and never enters them (junction cycles, dangling links, mounts).
function Get-TreeSnapshot([string]$Root, [switch]$Meta) {
    if (-not [IO.Directory]::Exists($Root)) { return 'absent' }
    $rows = [Collections.Generic.List[string]]::new(); $todo = [Collections.Generic.Stack[string]]::new(); $todo.Push($Root)
    while ($todo.Count) {
        foreach ($p in [IO.Directory]::GetFileSystemEntries($todo.Pop())) {
            $a = [int][IO.File]::GetAttributes($p)
            if ($a -band 0x400) { $rows.Add("$p|reparse") } elseif ($a -band 0x10) { $rows.Add("$p|dir"); $todo.Push($p) }
            elseif ($Meta) { $f = [IO.FileInfo]::new($p); $rows.Add("$p|$($f.Length)|$($f.LastWriteTimeUtc.Ticks)") } else { $rows.Add("$p|$(Get-FileSha256 $p)") }
        }
    }
    $rows.Sort([StringComparer]::Ordinal); return ($rows -join "`n")
}
function Get-MappingSnapshot { "$((Invoke-Native $SubstExe @()).out.Trim())|$(@([IO.DriveInfo]::GetDrives() | ForEach-Object { $_.Name }) -join ',')" }
# SUBST letter owned by this run: first free letter, proven by a marker file visible through it.
function New-TestSubst([string]$Target) {
    $o = [ordered]@{ letter = $null; target = $Target; marker = 'pxsubst-' + [guid]::NewGuid().ToString('N') + '.txt'; create_rc = $null; delete_rc = $null; removed = $false; error = $null }
    [IO.File]::WriteAllText("$Target\$($o.marker)", 'marker', $Utf8)
    foreach ($l in [char[]]'ZYXWVUTSRQPONMLKJIHG') {
        if ([IO.Directory]::Exists("${l}:\") -or @([IO.DriveInfo]::GetDrives() | Where-Object { $_.Name -eq "${l}:\" }).Count) { continue }
        $r = Invoke-Native $SubstExe @("${l}:", $Target); $o.create_rc = $r.rc
        if ($r.rc -eq 0) { $o.letter = "${l}:"; $Cleanup.subst.Add($o); break }
    }
    if (-not $o.letter -or -not [IO.File]::Exists("$($o.letter)\$($o.marker)")) { throw "SUBST fixture for $Target could not be created/verified" }
    return $o.letter
}
# Removes only own letters still showing own marker, verifies removal; a failure keeps the record and is a cleanup error.
function Remove-TestSubst {
    foreach ($o in $Cleanup.subst) {
        if ($o.removed) { continue }
        if (-not [IO.File]::Exists("$($o.letter)\$($o.marker)")) { $o.error = 'own marker not visible; mapping left untouched' }
        else {
            $r = Invoke-Native $SubstExe @($o.letter, '/D'); $o.delete_rc = $r.rc
            if ($r.rc -ne 0 -or [IO.Directory]::Exists("$($o.letter)\")) { $o.error = "subst /D rc=$($r.rc); letter still mapped" } else { $o.removed = $true }
        }
        if ($o.error) { $Cleanup.errors.Add("SUBST $($o.letter) -> $($o.target): $($o.error)") }
    }
}
function Invoke-Diskpart([string[]]$Lines, [string]$Step) {
    $f = "$S\vhd\$Step.txt"; [IO.File]::WriteAllText($f, ($Lines -join "`r`n") + "`r`n", [Text.Encoding]::ASCII)
    $r = Invoke-Native $DiskpartExe @('/s', $f); $Cleanup.vhd.log.Add([ordered]@{ step = $Step; script = $Lines; rc = $r.rc; output = $r.out }); return $r.rc
}
function Test-Unattached([string]$F) { try { [IO.File]::Open($F, 'Open', 'Read', 'None').Dispose(); return $true } catch { return $false } }
# The record is owned (and cleaned) from before creation, so a half-built fixture is still detached.
function New-TestVhd {
    if ($S -cnotmatch '^[A-Za-z]:\\[\x21-\x7e]+\z') { throw 'VhdFixture needs a scratch path of printable ASCII without spaces' }
    $me = [Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $me.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { throw 'VhdFixture needs an elevated administrator session' }
    $l = $null; foreach ($x in [char[]]'YXWVUTSRQPONMLKJIHG') { if (-not [IO.Directory]::Exists("${x}:\") -and -not @([IO.DriveInfo]::GetDrives() | Where-Object { $_.Name -eq "${x}:\" }).Count) { $l = $x; break } }
    if (-not $l) { throw 'no free drive letter for the VHD fixture' }
    $g = [guid]::NewGuid().ToString('N')
    $v = [ordered]@{ file = "$S\vhd\px.vhd"; letter = "${l}:"; mount = "$S\repo\mnt"; label = 'PX' + $g.Substring(0, 8).ToUpperInvariant(); marker = "pxvhd-$g.txt"
        max_mb = 64; file_bytes = $null; total_bytes = $null; removed = $false; log = [Collections.Generic.List[object]]::new() }
    $Cleanup.vhd = $v
    foreach ($d in "$S\vhd", $v.mount) { $null = [IO.Directory]::CreateDirectory($d) }
    $rc = Invoke-Diskpart @("create vdisk file=""$($v.file)"" maximum=64 type=expandable", "select vdisk file=""$($v.file)""", 'attach vdisk',
        'create partition primary', "format fs=ntfs quick label=$($v.label)", "assign letter=$l", "assign mount=""$($v.mount)""") 'create'
    $d = [IO.DriveInfo]::new($v.letter)
    if ($rc -ne 0 -or -not $d.IsReady -or $d.VolumeLabel -cne $v.label -or $d.DriveFormat -cne 'NTFS') { throw "VHD fixture not created/verified (diskpart rc=$rc)" }
    $v.total_bytes = $d.TotalSize; $v.file_bytes = [IO.FileInfo]::new($v.file).Length; if ($v.total_bytes -gt 256MB -or $v.file_bytes -gt 256MB) { throw 'VHD fixture exceeds 256 MB' }
    $null = [IO.Directory]::CreateDirectory("$($v.letter)\px"); [IO.File]::WriteAllText("$($v.letter)\px\$($v.marker)", 'marker', $Utf8); [IO.File]::WriteAllText("$($v.letter)\px\cfg.json", (New-ConfigJson), $Utf8)
    if (-not [IO.File]::Exists("$($v.mount)\px\$($v.marker)")) { throw 'VHD mount under the fixture repository not verified' }
    return $v
}
# Unmount, detach (even if unmount failed), verify: no mount point, file exclusively openable, letter gone.
function Remove-TestVhd {
    $v = $Cleanup.vhd; if (-not $v -or $v.removed) { return }
    $n = $Cleanup.errors.Count
    if ([IO.Directory]::Exists($v.mount) -and ([int][IO.File]::GetAttributes($v.mount) -band 0x400)) {
        $r = Invoke-Native $MountvolExe @("$($v.mount)\", '/D'); $v.log.Add([ordered]@{ step = 'mountvol /D'; rc = $r.rc; output = $r.out })
        if ([int][IO.File]::GetAttributes($v.mount) -band 0x400) { $Cleanup.errors.Add("own VHD mount folder still mounted: $($v.mount)") }
    }
    if ([IO.File]::Exists($v.file) -and -not (Test-Unattached $v.file)) {
        $null = Invoke-Diskpart @("select vdisk file=""$($v.file)""", 'detach vdisk') 'detach'
        for ($t = 0; $t -lt 10 -and -not (Test-Unattached $v.file); $t++) { [Threading.Thread]::Sleep(500) }
        if (-not (Test-Unattached $v.file)) { $Cleanup.errors.Add("own VHD still attached: $($v.file)") }
    }
    $d = [IO.DriveInfo]::new($v.letter); if ($d.IsReady -and $d.VolumeLabel -ceq $v.label) { $Cleanup.errors.Add("own VHD letter $($v.letter) still present") }
    $v.removed = $Cleanup.errors.Count -eq $n
}
function Get-OutcomeIds([string]$Outcome) { @($Results | Where-Object { $_.outcome -eq $Outcome } | ForEach-Object { $_.id }) }
# Every terminal path: owned SUBST/VHD removal; scratch tree removal only if the run passed and nothing failed so far;
# outside sentinel intact; drive mappings unchanged. Any cleanup error is rc 2 and keeps the tree; report always written.
function Complete-Run([int]$Rc) {
    if ($script:Completing) { exit 2 }
    $script:Completing = $true; $c = $Cleanup
    foreach ($step in { if ($FullScratch) { Set-TestLocation $FullScratch } }, { Remove-TestSubst }, { Remove-TestVhd }) {
        try { & $step } catch { $c.errors.Add("$($_.Exception.Message)") }
    }
    try {
        if ($InjectCleanupFailure -and $S) { $script:Locked = [IO.FileStream]::new("$S\pxlocked.bin", [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None) }
        if ($S -and [IO.Directory]::Exists($S)) {
            if ($Rc -eq 0 -and -not $c.errors.Count) { Remove-OwnedTree $S $c.errors; $c.tree_removed = -not [IO.Directory]::Exists($S) }
            else { Write-Host "scratch kept for evidence: $S" }
        }
        if ($Keep) {
            $c.keep_sentinel_intact = (Get-FileSha256 "$Keep\keep.txt") -ceq $KeepSha
            if (-not $c.keep_sentinel_intact) { $c.errors.Add("outside sentinel $Keep\keep.txt changed or missing: cleanup followed a junction") }
            elseif ($c.tree_removed) { Remove-OwnedTree $Keep $c.errors }
        }
        if ($null -ne $c.mappings_before) { $c.mappings_after = Get-MappingSnapshot; if ($c.mappings_after -cne $c.mappings_before) { $c.errors.Add('drive mappings differ from before the run') } }
    } catch { $c.errors.Add("$($_.Exception.Message)") } finally { if ($script:Locked) { $script:Locked.Dispose() } }
    $c.status = $(if ($c.errors.Count) { 'failed' } else { 'ok' }); if ($c.errors.Count) { $Rc = 2 }
    $Report.failed_ids = @(Get-OutcomeIds 'failed'); $Report.setup_error_ids = @(Get-OutcomeIds 'setup_error'); $Report.unavailable_ids = @(Get-OutcomeIds 'unavailable')
    $Report.passed = @(Get-OutcomeIds 'passed').Count; $Report.failed = $Report.failed_ids.Count
    $Report.total = $Report.passed + $Report.failed + $Report.setup_error_ids.Count
    $Report.harness_sha256 = Get-FileSha256 $PSCommandPath; $Report.module_sha256 = Get-FileSha256 $ModulePath; $Report.sample_sha256 = Get-FileSha256 $SamplePath
    if ($ReportPath) { try { [IO.File]::WriteAllText($ReportPath, ($Report | ConvertTo-Json -Depth 8), $Utf8) } catch { Write-Host "REPORT_WRITE_ERROR $($_.Exception.Message)"; $Rc = 2 } }
    Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; setup_error_ids=[{3}]; unavailable_ids=[{4}]; api_state={5}; setup_error={6}; cleanup={7} [{8}]; rc={9}' -f $Report.passed,
        $Report.total, ($Report.failed_ids -join ','), ($Report.setup_error_ids -join ','), ($Report.unavailable_ids -join ','), $Report.api_state, $Report.setup_error,
        $c.status, ($c.errors -join ' || '), $Rc)
    exit $Rc
}
trap { $Report.setup_error = "$($_.Exception.Message)"; Write-Host "SETUP_ERROR $($Report.setup_error)"; Complete-Run 2 }
function Get-EnvSnapshot { (@([Environment]::GetEnvironmentVariables().GetEnumerator() | Sort-Object Name | ForEach-Object { if (-not "$($_.Name)".StartsWith('=')) { "$($_.Name)=$($_.Value)" } })) -join "`n" }
function Set-TestLocation([string]$P) { Set-Location -LiteralPath $P; [Environment]::CurrentDirectory = $P }
function Write-Fixture([string]$Rel, $Content) {
    $p = "$S\$Rel"
    try { if ($Content -is [byte[]]) { [IO.File]::WriteAllBytes($p, $Content) } else { [IO.File]::WriteAllText($p, $Content, $Utf8) } }
    catch { throw "SETUP: fixture $Rel could not be written" }
    return $p
}
# JSON fixture from raw value tokens: a valid Local (or -Remote) config with fields replaced/added/dropped.
function New-ConfigJson([hashtable]$Set = @{}, [string[]]$Drop = @(), [switch]$Remote) {
    $m = [ordered]@{ schemaVersion = '1'; targetId = '"tgt-one"'; mode = '"Local"'; basePath = '"C:\\px1"' }
    if ($Remote) { $m.targetId = '"tgt-two"'; $m.mode = '"Remote"'; $m.connectionUri = '"https://gw.example.invalid:5986/wsman"'; $m.configurationName = '"px.endpoint"' }
    foreach ($k in $Set.Keys) { $m[$k] = $Set[$k] }
    foreach ($k in $Drop) { $m.Remove($k) }
    return '{' + (@($m.Keys | ForEach-Object { '"' + $_ + '":' + $m[$_] }) -join ',') + '}'
}
function Get-FixtureSnapshot { (Get-TreeSnapshot $S) + "`n" + $(if ($Vhd) { Get-TreeSnapshot "$($Vhd.letter)\px" }) }
# One guarded read: fixture tree bytes (VHD included) and sentinel count must not change; every error text is collected.
function Invoke-GuardedRead([string]$Cfg, [string]$Repo = "$S\repo") {
    $before = Get-FixtureSnapshot; $hits = $global:PxHits.Count; $global:Error.Clear(); $o = $null; $e = $null
    try { $o = Read-ProximaConfig -ConfigPath $Cfg -RepositoryRoot $Repo } catch { $e = $_ }
    if ((Get-FixtureSnapshot) -cne $before) { throw 'TREE_CHANGED: filesystem tree/bytes changed during read' }
    if ($global:PxHits.Count -ne $hits) { throw 'SIDE_EFFECT: sentinel hit during read' }
    $text = @(@($global:Error) + @($e) | Where-Object { $_ } | ForEach-Object { ($_ | Format-List * -Force | Out-String) + "$_" +
            $(if ($_ -is [Management.Automation.ErrorRecord]) { $_.Exception | Format-List * -Force | Out-String }) }) -join "`n"
    return [pscustomobject]@{ Out = $o; Err = $e; Text = $text }
}
# Assertions RECORD a behavioural token and the case continues, so a failed probe never hides later ones. WRONG_CODE
# (rejected, other reason) is diagnostic only; ACCEPTED_INVALID/NO_ERROR/REJECTED_VALID/ALTERED_VALID are behaviours.
function Add-Fail([string]$Msg) { $script:CaseFail.Add($Msg) }
function Assert-Rejected($X, [string]$Code, [string]$Label) {
    $id = $(if ($X.Err) { $X.Err.FullyQualifiedErrorId } else { '<none>' })
    if ($null -ne $X.Out) { Add-Fail "ACCEPTED_INVALID[$Label]" }
    elseif (-not $X.Err) { Add-Fail "NO_ERROR[$Label]" }
    elseif ($Code -and $id -notmatch "^ProximaConfig\.$Code(,|\z)") { Add-Fail "WRONG_CODE[$Label] expected ProximaConfig.$Code, got $id" }
}
function Assert-Accepted($X, [string]$TargetId, [string]$Label) {
    if ($null -eq $X.Out) { Add-Fail "REJECTED_VALID[$Label] $(if ($X.Err) { $X.Err.FullyQualifiedErrorId })" }
    elseif ($X.Out.targetId -cne $TargetId) { Add-Fail "ALTERED_VALID[$Label]" }
}
function Invoke-Case([string]$Id, [string[]]$Needs, [scriptblock]$Body) {
    $script:CaseFail = [Collections.Generic.List[string]]::new(); $why = $null; $outcome = 'passed'
    try {
        if ($Needs -contains 'api' -and -not $ApiPresent) { throw "API_ABSENT: Read-ProximaConfig not available from ModulePath ($($Report.api_state))" }
        if ($Needs -contains 'module' -and -not [IO.File]::Exists($ModulePath)) { throw 'API_ABSENT: module file absent' }
        if ($Needs -contains 'sample' -and -not [IO.File]::Exists($SamplePath)) { throw 'API_ABSENT: sample file absent' }
        Set-TestLocation $S; & $Body
    } catch { $script:CaseFail.Add("$($_.Exception.Message)") } finally { Set-TestLocation $S }
    if ($script:CaseFail.Count) { $why = $script:CaseFail -join ' | ' }
    if ($why) { $outcome = $(if ($why.StartsWith('SETUP:')) { 'setup_error' } elseif ($why.StartsWith('UNAVAILABLE:')) { 'unavailable' } else { 'failed' }) }
    $Results.Add([pscustomobject]@{ id = $Id; outcome = $outcome; reason = $why })
    Write-Host ('{0} {1}{2}' -f $outcome.ToUpperInvariant(), $Id, $(if ($why) { " :: $why" }))
}
# Named behavioural tokens ('CASE:TOKEN') found as failures of their case in a child report.
function Get-Kill($Rep, [string[]]$Want) {
    $hit = [Collections.Generic.List[object]]::new()
    foreach ($w in $Want) {
        $cid, $tok = $w -split ':', 2; $c = @($Rep.cases | Where-Object { $_.id -eq $cid -and $_.outcome -eq 'failed' -and "$($_.reason)".Contains($tok) })
        if ($c.Count) { $hit.Add([ordered]@{ want = $w; reason = "$($c[0].reason)" }) }
    }
    return , $hit
}
# ---- setup: any failure here is rc 2 ----
if ([Environment]::OSVersion.Platform -ne 'Win32NT') { throw 'Windows host required' }
$Helpers = @(Get-Command -CommandType Function | Where-Object { $_.ScriptBlock.File -eq $PSCommandPath } | ForEach-Object { $_.Name })
$shadowed = @($Helpers | Where-Object { Get-Alias -Name $_ -ErrorAction SilentlyContinue })
if ($Helpers.Count -lt 20 -or $shadowed.Count) { throw "helper alias check failed: $($Helpers.Count) helpers, shadowed by an alias: $($shadowed -join ',')" }
$Report.alias_r = "$(@(Get-Alias -Name r -ErrorAction SilentlyContinue | ForEach-Object { $_.Definition }))"
$ModulePath = [IO.Path]::GetFullPath($ModulePath); $Report.module_path = $ModulePath; $ModuleDir = Split-Path -Parent $ModulePath
if (-not $RepositoryRoot) { $RepositoryRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ModuleDir))) }
if (-not $SamplePath) { $SamplePath = Join-Path (Split-Path -Parent $ModuleDir) 'config.example.json' }
$RepositoryRoot = [IO.Path]::GetFullPath($RepositoryRoot).TrimEnd('\'); $SamplePath = [IO.Path]::GetFullPath($SamplePath)
foreach ($p in $ScratchRoot, $ReportPath, $EvidenceRoot) {
    if ($p -and [IO.Path]::GetFullPath($p).StartsWith($RepositoryRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'ScratchRoot/ReportPath/EvidenceRoot must be outside the measured tree' }
}
if (-not [IO.Directory]::Exists($ScratchRoot)) { throw 'ScratchRoot must be an existing directory' }
$FullScratch = [IO.Path]::GetFullPath($ScratchRoot).TrimEnd('\'); $RunId = [guid]::NewGuid().ToString('N').Substring(0, 12)
$Cleanup.mappings_before = Get-MappingSnapshot
$S = "$FullScratch\pxcfg-$RunId"; $Report.scratch = $S
foreach ($d in 'repo\cfg', 'repo\pxshortnamealias', 'repo-sibling', 'rep', 'ext1\deep', 'ext2\nest', 'cx', 'gone') { $null = [IO.Directory]::CreateDirectory("$S\$d") }
# Outside sentinel: a directory NEXT TO the scratch tree, reached from inside only through junction jout.
$Keep = "$FullScratch\pxkeep-$RunId"; $null = [IO.Directory]::CreateDirectory($Keep); [IO.File]::WriteAllText("$Keep\keep.txt", $RunId, $Utf8); $KeepSha = Get-FileSha256 "$Keep\keep.txt"
# Junctions: jn/jin/repojn for the cases; jout leaves the tree, ext2\nest\jloop is a cycle, jdang dangles (cleanup).
foreach ($j in @('jn', "$S\ext1"), @('jin', "$S\repo\cfg"), @('repojn', "$S\repo"), @('jout', $Keep), @('ext2\nest\jloop', $S), @('jdang', "$S\gone")) { $null = New-Item -ItemType Junction -Path "$S\$($j[0])" -Value $j[1] }
[IO.Directory]::Delete("$S\gone"); if (-not ([int][IO.File]::GetAttributes("$S\jdang") -band 0x400) -or [IO.Directory]::Exists("$S\gone")) { throw 'dangling junction fixture not created' }
# Hardlink alias: an external name for a file inside the repository (H0 accepted it).
$null = Write-Fixture 'repo\cfg\linked.json' (New-ConfigJson); $null = New-Item -ItemType HardLink -Path "$S\ext1\hardlink.json" -Value "$S\repo\cfg\linked.json"
if ([IO.FileInfo]::new("$S\ext1\hardlink.json").Length -ne [IO.FileInfo]::new("$S\repo\cfg\linked.json").Length) { throw 'hardlink fixture not created' }
# SUBST of a repository subdirectory (H0 accepted it); r4: SUBST backed through junction jn to external ext1\deep.
$SubstDrive = New-TestSubst "$S\repo\cfg"; $Report.subst_drive = $SubstDrive
$SubstJn = New-TestSubst "$S\jn\deep"; $Report.subst_junction_drive = $SubstJn
if ($VhdFixture) { $Vhd = New-TestVhd }
$Evid = "$(if ($EvidenceRoot) { [IO.Path]::GetFullPath($EvidenceRoot).TrimEnd('\') } else { $FullScratch })\pxevid-$RunId"
if ($Counterexamples) { $null = [IO.Directory]::CreateDirectory($Evid); $Report.evidence_dir = $Evid }
# 8.3 alias: capability evidence only. A short name is used only when it really resolves to this directory.
$null = Write-Fixture 'repo\pxshortnamealias\in.json' (New-ConfigJson)
$ShortAlias = $(if ([IO.File]::Exists("$S\repo\PXSHOR~1\in.json")) { 'PXSHOR~1' }); $Report.short_name_alias = $(if ($ShortAlias) { 'observed' } else { 'unavailable' })
$EnvBefore = Get-EnvSnapshot; $RepoBefore = Get-TreeSnapshot $RepositoryRoot -Meta
# Scoped side-effect sentinels: global functions shadow these cmdlets for the module from here on; each call is
# recorded and throws. Below this line the harness uses only .NET calls and the native fixture tools (subst, diskpart,
# mountvol, child harness) through Invoke-Native - never a sentinel-named cmdlet.
$global:PxHits = [Collections.Generic.List[string]]::new()
$Sentinels = 'Invoke-WebRequest', 'Invoke-RestMethod', 'New-PSSession', 'Enter-PSSession', 'Invoke-Command', 'Start-Process', 'Start-Job', 'New-Item',
'Set-Content', 'Add-Content', 'Out-File', 'Set-Item', 'Set-ItemProperty', 'New-ItemProperty', 'Remove-Item', 'Copy-Item', 'Move-Item', 'Rename-Item',
'New-Service', 'Set-Service', 'Start-Service', 'Register-ScheduledTask', 'Set-Acl', 'Add-Type', 'Test-Connection', 'Test-NetConnection', 'Resolve-DnsName', 'Export-Clixml'
. ([scriptblock]::Create((($Sentinels | ForEach-Object { "function global:$_ { `$global:PxHits.Add('$_'); throw 'PX_SENTINEL $_' }" }) -join "`n")))
$Forbidden = $Sentinels + @('WebClient', 'HttpClient', 'WebRequest', 'Sockets', 'Diagnostics.Process', 'StreamWriter', 'WriteAll', 'AppendAll', 'File]::Create',
    'File]::Open', 'FileMode]::', 'FileAccess]::Write', 'FileAccess]::ReadWrite', 'RunAndSave', 'AssemblyBuilderAccess]::Save', 'CodeDom', 'CSharpCodeProvider',
    'Import-Module', 'using module', '$env:', 'Environment]::', 'Registry')
$ApiPresent = $false; $ImportHits = 0; $Exported = @(); $Report.api_state = 'module_absent'
if ([IO.File]::Exists($ModulePath)) {
    $h0 = $global:PxHits.Count
    try { $mod = Import-Module -Name $ModulePath -Force -PassThru -DisableNameChecking }
    catch { throw "existing module failed to import (sentinel hits: $($global:PxHits.Count - $h0))" }
    $ImportHits = $global:PxHits.Count - $h0; $Exported = @($mod.ExportedCommands.Keys)
    $ApiPresent = $Exported -contains 'Read-ProximaConfig'
    $Report.api_state = $(if ($ApiPresent) { 'present' } else { 'module_without_api' })
}
$SampleExpect = [ordered]@{ schemaVersion = 1; targetId = 'example-target'; mode = 'Remote'; basePath = 'C:\ProximaExample'
    connectionUri = 'https://gateway.example.invalid:5986/wsman'; configurationName = 'Example.Endpoint' }
# ---- cases (mandatory IDs; A5-03 runs last so it sees every read) ----
Invoke-Case 'A1-01' api {
    $a = Write-Fixture 'ext1\a.json' (New-ConfigJson); $b = Write-Fixture 'ext2\b.json' (New-ConfigJson -Remote)
    Set-TestLocation "$S\ext2"; $r1 = Invoke-GuardedRead $a; Set-TestLocation "$S\ext1"; $r2 = Invoke-GuardedRead $b; Set-TestLocation "$S\repo"; $r3 = Invoke-GuardedRead $a
    Assert-Accepted $r1 'tgt-one' 'Local from another CWD'; Assert-Accepted $r2 'tgt-two' 'Remote from another CWD'; Assert-Accepted $r3 'tgt-one' 'Local from the repository CWD'
    if ($r1.Out -and ((@($r1.Out.PSObject.Properties.Name) -join ',') -cne 'schemaVersion,targetId,mode,basePath' -or $r1.Out.schemaVersion -ne 1 -or
            $r1.Out.mode -cne 'Local' -or $r1.Out.basePath -cne 'C:\px1')) { Add-Fail 'WRONG_RESULT[Local properties/values]' }
    if ($r2.Out -and ((@($r2.Out.PSObject.Properties.Name) -join ',') -cne 'schemaVersion,targetId,mode,basePath,connectionUri,configurationName' -or
            $r2.Out.mode -cne 'Remote' -or $r2.Out.connectionUri -cne 'https://gw.example.invalid:5986/wsman' -or $r2.Out.configurationName -cne 'px.endpoint')) { Add-Fail 'WRONG_RESULT[Remote properties/values]' }
    # Every handle must be closed after the read: an exclusive open of the file and a rename of its directory succeed
    # (bounded retries only absorb a transient scanner handle; a leaked handle stays open and keeps this red).
    Set-TestLocation $S; $released = $false
    for ($t = 0; $t -lt 10 -and -not $released; $t++) {
        try { [IO.File]::Open($a, 'Open', 'ReadWrite', 'None').Dispose(); [IO.Directory]::Move("$S\ext1", "$S\ext1-moved"); $released = $true }
        catch { [Threading.Thread]::Sleep(200) }
    }
    if (-not $released) { throw 'HANDLE_LEAK: a file or directory handle stayed open after the read' }
    [IO.Directory]::Move("$S\ext1-moved", "$S\ext1")
}
Invoke-Case 'A1-02' api {
    $uni = [regex]::Unescape('M\u1ee5c-ti\u00eau_\u76ee\u6a19') + [char]::ConvertFromUtf32(0x1F680); $cn = [regex]::Unescape('C\u1ea5u.H\u00ecnh'); $uri = 'HTTPS://GW.Example.Invalid:5986/WSMan'
    $r = Invoke-GuardedRead (Write-Fixture 'ext2\u.json' (New-ConfigJson -Remote @{ targetId = '"' + $uni + '"'; configurationName = '"' + $cn + '"'; connectionUri = '"' + $uri + '"' }))
    Assert-Accepted $r $uni 'Unicode targetId'
    if ($r.Out -and ($r.Out.configurationName -cne $cn -or $r.Out.connectionUri -cne $uri)) { Add-Fail 'ALTERED_VALID[Unicode configurationName or uppercase HTTPS]' }
    $long = 'T' * 300; Assert-Accepted (Invoke-GuardedRead (Write-Fixture 'ext2\l.json' (New-ConfigJson @{ targetId = '"' + $long + '"' }))) $long 'long targetId'
    $esc = [char]::ConvertFromUtf32(0x1F680) + 'x'; Assert-Accepted (Invoke-GuardedRead (Write-Fixture 'ext2\e.json' (New-ConfigJson @{ targetId = '"\ud83d\ude80x"' }))) $esc 'escaped surrogate pair'
}
Invoke-Case 'A2-01' api {
    $m = "$S\ext1\missing.json"; Assert-Rejected (Invoke-GuardedRead $m) 'NotFound' 'missing config'
    if ([IO.File]::Exists($m)) { Add-Fail 'SYNTHESIZED[missing config written to disk]' }
    Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\a.json' (New-ConfigJson)) "$S\nope") 'RepositoryRootNotFound' 'missing repository root'
}
Invoke-Case 'A2-02' api {
    $bad = '', '{', '{"schemaVersion":1,}', ((New-ConfigJson) + ' x'), "{'schemaVersion':1}", '{"schemaVersion":01}', '{"targetId":"a\q"}',
    "// c`n{}", '{"schemaVersion":NaN}', '{"a":1 "b":2}', '{"a":"x', [byte[]](0xEF, 0xBB, 0xBF)
    $i = 0; foreach ($j in $bad) { $i++; Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\m.json' $j)) 'MalformedJson' "malformed#$i" }
    Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\m.json' ([byte[]](0x7B, 0x22, 0x61, 0x22, 0x3A, 0x22, 0xC3, 0x28, 0x22, 0x7D)))) 'Encoding' 'invalid utf-8'
}
Invoke-Case 'A2-03' api { $i = 0; foreach ($j in '1', '"x"', '[]', '[{}]', 'null', 'true') { $i++; Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\m.json' $j)) 'NotObject' "nonobject#$i" } }
Invoke-Case 'A2-04' api {
    $bad = [ordered]@{ schemaVersion = '"1"', '1.0', '2', 'true', 'null', '1e0', '[1]'
        targetId = '5', '""', '"   "', '["t"]', '{}', '"bad id"', '"a\tb"', '"\u0000x"', '"\ud800"', '"\udc00x"'
        mode = '"local"', '"Hybrid"', '1', '""'; basePath = '"px\\rel"', '"C:px"', '"\\\\srv\\share"', '"\\px"', '"C:\\a\\..\\b"', '"C:/a"', '""', '"C:\\a\\"' }
    foreach ($f in $bad.Keys) {
        foreach ($v in $bad[$f]) {
            $r = Invoke-GuardedRead (Write-Fixture 'ext1\t.json' (New-ConfigJson @{ $f = $v })); Assert-Rejected $r 'InvalidField' "$f=$v"
            if ($r.Err -and $r.Err.Exception.Message -notlike "*Field: $f.*") { Add-Fail "FIELD_NOT_NAMED[$f=$v]" }
        }
        Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\t.json' (New-ConfigJson -Drop $f))) 'InvalidField' "missing $f"
    }
}
Invoke-Case 'A2-05' api {
    Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\u.json' (New-ConfigJson @{ extra = '1' }))) 'UnknownField' 'unknown field'
    Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\u.json' ('{"schemaVersion":1,' + (New-ConfigJson).Substring(1)))) 'DuplicateField' 'duplicate field'
    Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\u.json' ((New-ConfigJson) -creplace '"mode"', '"Mode"'))) 'UnknownField' 'case-variant key'
}
Invoke-Case 'A2-06' api {
    Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\x.json' (New-ConfigJson @{ connectionUri = '"https://gw.example.invalid/"' }))) 'ModeMismatch' 'Local+connectionUri'
    Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\x.json' (New-ConfigJson @{ configurationName = '"px.endpoint"' }))) 'ModeMismatch' 'Local+configurationName'
    foreach ($f in 'connectionUri', 'configurationName') { Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\x.json' (New-ConfigJson -Remote -Drop $f))) 'InvalidField' "Remote without $f" }
    foreach ($v in '""', '"a b"', '5') { Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\x.json' (New-ConfigJson -Remote @{ configurationName = $v }))) 'InvalidField' "configurationName $v" }
    # r4: '@' in the PATH is not userinfo - accepted and returned byte-for-byte; '@' in the authority stays rejected.
    $at = 'https://gateway.example.invalid/a@b'; $r = Invoke-GuardedRead (Write-Fixture 'ext1\x.json' (New-ConfigJson -Remote @{ connectionUri = '"' + $at + '"' }))
    Assert-Accepted $r 'tgt-two' 'uri path with @'
    if ($r.Out -and $r.Out.connectionUri -cne $at) { Add-Fail 'ALTERED_VALID[uri path with @]' }
    foreach ($u in 'http://gw.example.invalid/wsman', 'https:/gw', '/wsman', 'gw.example.invalid:5986', 'https://u:p@gw.example.invalid/', 'ftp://gw.example.invalid/',
        'https://u@gateway.example.invalid/a@b', 'https://@gw.example.invalid/', 'https://gateway.example.invalid@evil.invalid/a@b', 'https:///a@b',
        'https://gw.example.invalid/?a=1', 'https://gw.example.invalid/a@b?k=1', 'https://gw.example.invalid/#f', 'https://gw.example.invalid/a@b#f',
        'https://gw x.invalid/', 'https://gw.example.invalid/a@b c', 'https://gw.example.invalid\a@b', 'https://') {
        Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\x.json' (New-ConfigJson -Remote @{ connectionUri = '"' + $u.Replace('\', '\\') + '"' }))) 'InvalidField' "uri $u"
    }
}
Invoke-Case 'A2-07' api {
    $a = Write-Fixture 'ext1\a.json' (New-ConfigJson)
    $cfg = 'ext1\a.json', ($a.Substring(0, 2) + $a.Substring(3)), $a.Substring(2), ('\\localhost\' + $a[0] + '$' + $a.Substring(2)), ('\\?\' + $a),
    "$S\ext1\..\ext1\a.json", "$S\ext1\.\a.json", $a.Replace('\', '/'), "$($a):s", "$a.", "$a ", "$S\ext1\"
    foreach ($p in $cfg) { Assert-Rejected (Invoke-GuardedRead $p) 'ConfigPathInvalid' "ConfigPath $p" }
    Assert-Rejected (Invoke-GuardedRead "$S\ext1") 'NotAFile' 'directory as ConfigPath'
    foreach ($q in 'repo', ($S.Substring(0, 2) + $S.Substring(3) + '\repo'), "$S\repo\", '\\localhost\x\repo') { Assert-Rejected (Invoke-GuardedRead $a $q) 'RepositoryRootInvalid' "RepositoryRoot $q" }
    Assert-Rejected (Invoke-GuardedRead '') '' 'empty ConfigPath'
}
Invoke-Case 'A3-01' api { Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'repo\cfg\in.json' (New-ConfigJson))) 'InsideRepository' 'config inside repository' }
Invoke-Case 'A3-02' api {
    $in = Write-Fixture 'repo\cfg\in.json' (New-ConfigJson)
    Assert-Rejected (Invoke-GuardedRead ($S + '\REPO\CFG\IN.JSON')) 'InsideRepository' 'case-variant config path'
    Assert-Rejected (Invoke-GuardedRead $in ($S + '\Repo')) 'InsideRepository' 'case-variant repository root'
}
Invoke-Case 'A3-03' api { Assert-Accepted (Invoke-GuardedRead (Write-Fixture 'repo-sibling\ok.json' (New-ConfigJson))) 'tgt-one' 'same-prefix sibling outside repository' }
Invoke-Case 'A3-04' api {
    $null = Write-Fixture 'ext1\a.json' (New-ConfigJson); $null = Write-Fixture 'repo\cfg\in.json' (New-ConfigJson)
    Assert-Rejected (Invoke-GuardedRead "$S\jn\a.json") 'ReparsePoint' 'junction ancestor'
    Assert-Rejected (Invoke-GuardedRead "$S\jin\in.json") 'ReparsePoint' 'junction into repository'
    Assert-Rejected (Invoke-GuardedRead "$S\ext1\a.json" "$S\repojn") 'ReparsePoint' 'junction repository root'
}
Invoke-Case 'A3-05' api {
    $null = Write-Fixture 'repo\cfg\in.json' (New-ConfigJson)
    Assert-Rejected (Invoke-GuardedRead "$SubstDrive\in.json") 'InsideRepository' 'SUBST alias of a repository subdirectory'
    Assert-Rejected (Invoke-GuardedRead "$S\repo\cfg\in.json" "$SubstDrive\") 'InsideRepository' 'repository root given as SUBST alias'
    Assert-Accepted (Invoke-GuardedRead "$SubstDrive\in.json" "$S\ext1") 'tgt-one' 'SUBST path physically outside the repository'
    # r4 hidden backing ancestor: the drive root handle alone looks ordinary; only the backing chain shows junction jn.
    $null = Write-Fixture 'ext1\deep\a.json' (New-ConfigJson); $null = Write-Fixture 'ext1\a.json' (New-ConfigJson)
    Assert-Rejected (Invoke-GuardedRead "$SubstJn\a.json") 'ReparsePoint' 'SUBST backing through junction'
    Assert-Rejected (Invoke-GuardedRead "$S\ext1\a.json" "$SubstJn\") 'ReparsePoint' 'repository root as SUBST through junction'
}
Invoke-Case 'A3-06' api {
    Assert-Rejected (Invoke-GuardedRead "$S\ext1\hardlink.json") 'MultiLink' 'external hardlink to a repository file'
    Assert-Rejected (Invoke-GuardedRead "$S\ext1\hardlink.json" "$S\ext2") 'MultiLink' 'multiply-linked file outside both'
}
Invoke-Case 'A3-07' api {
    if (-not $ShortAlias) { throw 'UNAVAILABLE: no 8.3 short name observed on the scratch volume' }
    Assert-Rejected (Invoke-GuardedRead "$S\repo\$ShortAlias\in.json") 'InsideRepository' '8.3 alias config path'
    Assert-Rejected (Invoke-GuardedRead "$S\repo\pxshortnamealias\in.json" "$S\repo\$ShortAlias") 'InsideRepository' '8.3 alias repository root'
    Assert-Accepted (Invoke-GuardedRead (Write-Fixture 'ext1\a.json' (New-ConfigJson)) "$S\repo\$ShortAlias") 'tgt-one' 'external config, 8.3 repository root'
}
# r4 closure: the VHD volume has its own letter AND is mounted at repo\mnt, so its letter path is inside the repository.
Invoke-Case 'A3-08' api {
    if (-not $Vhd) { throw 'UNAVAILABLE: mounted-volume fixture not requested (-VhdFixture)' }
    $q = "$($Vhd.letter)\px\cfg.json"; $ext = Write-Fixture 'ext1\a.json' (New-ConfigJson)
    Assert-Rejected (Invoke-GuardedRead $q) 'InsideRepository' 'volume mounted inside repository'
    Assert-Rejected (Invoke-GuardedRead "$($Vhd.mount)\px\cfg.json") 'ReparsePoint' 'config through mount folder'
    Assert-Accepted (Invoke-GuardedRead $q "$S\ext2") 'tgt-one' 'mounted volume, unrelated repository'
    Assert-Accepted (Invoke-GuardedRead $q "$S\rep") 'tgt-one' 'same-prefix repository beside mount'
    Assert-Accepted (Invoke-GuardedRead $ext) 'tgt-one' 'ordinary external file with mount present'
}
Invoke-Case 'A4-01' api {
    $z = 'PXSENTINEL' + [guid]::NewGuid().ToString('N'); $q = '"' + $z + '"'
    $all = @(@('password', 'SecretField', (New-ConfigJson @{ password = $q })), @('apiToken', 'SecretField', (New-ConfigJson @{ apiToken = $q })),
        @('Client_Secret', 'SecretField', (New-ConfigJson @{ Client_Secret = $q })), @('cookie', 'SecretField', (New-ConfigJson @{ cookie = $q })),
        @('credential', 'SecretField', (New-ConfigJson @{ credential = '{"u":' + $q + '}' })), @('notes', 'UnknownField', (New-ConfigJson @{ notes = $q })),
        @('targetId', 'InvalidField', (New-ConfigJson @{ targetId = '"' + $z + ' x"' })), @('mode', 'InvalidField', (New-ConfigJson @{ mode = $q })),
        @('uri userinfo', 'InvalidField', (New-ConfigJson -Remote @{ connectionUri = '"https://u:' + $z + '@gw.example.invalid/"' })),
        @('uri query', 'InvalidField', (New-ConfigJson -Remote @{ connectionUri = '"https://gw.example.invalid/?k=' + $z + '"' })),
        @('malformed', 'MalformedJson', ('{"targetId":' + $q + ',')), @('scalar', 'NotObject', $q))
    foreach ($c in $all) {
        $r = Invoke-GuardedRead (Write-Fixture 'ext1\s.json' $c[2]); Assert-Rejected $r $c[1] $c[0]
        if ($r.Text -notlike '*ProximaConfig*') { Add-Fail "TEXT_NOT_CAPTURED[$($c[0])]" }
        if ($r.Text.Contains($z)) { Add-Fail "SENTINEL_ECHOED[$($c[0])]" }
    }
}
Invoke-Case 'A5-01' module {
    $src = [IO.File]::ReadAllText($ModulePath)
    $hit = @($Forbidden | Where-Object { $src.IndexOf($_, [StringComparison]::OrdinalIgnoreCase) -ge 0 })
    if ($hit.Count) { throw "FORBIDDEN_TOKEN: side-effect token(s) in module: $($hit -join ', ')" }
}
Invoke-Case 'A5-02' api {
    if ($ImportHits -ne 0) { throw "import hit $ImportHits side-effect sentinel(s)" }
    if (($Exported -join ',') -cne 'Read-ProximaConfig') { throw "unexpected exports: $($Exported -join ',')" }
    $p = (Get-Command Read-ProximaConfig).Parameters
    foreach ($n in 'ConfigPath', 'RepositoryRoot') { if (-not @($p[$n].Attributes | Where-Object { $_ -is [Parameter] -and $_.Mandatory }).Count) { throw "$n is not mandatory" } }
}
Invoke-Case 'A6-01' sample {
    $raw = [IO.File]::ReadAllText($SamplePath); $v = $raw | ConvertFrom-Json; $names = @($v.PSObject.Properties.Name)
    if (($names -join ',') -cne (@($SampleExpect.Keys) -join ',')) { Add-Fail "SAMPLE_FIELDS[$($names -join ',')]" }
    foreach ($k in $SampleExpect.Keys) { if ($names -ccontains $k -and "$($v.$k)" -cne "$($SampleExpect[$k])") { Add-Fail "SAMPLE_VALUE[$k]" } }
    if ($names -cnotcontains 'schemaVersion' -or $v.schemaVersion -is [string] -or $raw -cnotmatch '"schemaVersion"\s*:\s*1\s*,') { Add-Fail 'SAMPLE_VERSION[not integer 1]' }
}
Invoke-Case 'A6-02' api, sample {
    $r = Invoke-GuardedRead (Write-Fixture 'ext2\sample-copy.json' ([IO.File]::ReadAllBytes($SamplePath)))
    if ($null -eq $r.Out) { throw "explicit external copy of the sample rejected: $(if ($r.Err) { $r.Err.FullyQualifiedErrorId })" }
    foreach ($k in $SampleExpect.Keys) { if ("$($r.Out.$k)" -cne "$($SampleExpect[$k])") { throw "reader returned an unexpected $k for the sample copy" } }
    Assert-Rejected (Invoke-GuardedRead $SamplePath $RepositoryRoot) 'InsideRepository' 'sample read in place'
    if ([IO.File]::ReadAllText($ModulePath) -match 'example') { throw 'module references the sample (implicit fallback)' }
}
Invoke-Case 'A5-03' api {
    if ($global:PxHits.Count) { Add-Fail "SIDE_EFFECT_HITS[$($global:PxHits -join ',')]" }
    if ((Get-EnvSnapshot) -cne $EnvBefore) { Add-Fail 'ENV_CHANGED' }
    if ((Get-TreeSnapshot $RepositoryRoot -Meta) -cne $RepoBefore) { Add-Fail 'REPOSITORY_TREE_CHANGED' }
}
# ---- counterexamples: mutate COPIES (in the evidence dir), rerun this harness in a child, classify ----
# k='m': credited only when EVERY 'CASE:BEHAVIOUR[label]' token is a failure of that case; redundant safeguards are
# removed together so the forbidden behaviour is really reached. k='c' control: rejects with another code only - no
# ACCEPTED_INVALID, and its target's tokens must NOT be met. k='i': injected owned cleanup failure must give rc 2.
$Default = 'return [pscustomobject]@{ schemaVersion = 1; targetId = ''tgt-default''; mode = ''Local''; basePath = ''C:\px0'' }'
$Physical = 'Assert-PxOutside $file.Final ($repo.Final.TrimEnd(''\'') + ''\'') $ctx 0'
$AttrCheck = 'if (($node.Attr -band $script:BadAttr) -ne 0) { Stop-Px ReparsePoint }'
$Backing = '$want = Get-PxBackingFinal $target.Substring(4) $Ctx $Depth'
# Entries mutate the module unless f = 's' (sample); kind k defaults to 'm'.
$Cx = @(@{ n = 'default-config'; e = @('$repo = Open-PxChain', "$Default; `$repo = Open-PxChain"); red = @('A1-01:ALTERED_VALID[Local from another CWD]') },
    @{ n = 'synthesize-missing'; e = @('$file = Open-PxChain', "if (-not [IO.File]::Exists(`$ConfigPath)) { $Default }; `$file = Open-PxChain"); red = @('A2-01:ACCEPTED_INVALID[missing config]') },
    @{ n = 'accept-wrong-type'; e = @(' -or $o[$Name].K -cne $Kind', ''); red = @('A2-04:ACCEPTED_INVALID[targetId=5]') },
    @{ n = 'ascii-only-text'; e = @('return $V.Length -gt 0 -and', 'return $V -cmatch ''^[A-Za-z0-9][A-Za-z0-9._-]{0,127}\z'' -and'); red = @('A1-02:REJECTED_VALID[Unicode targetId]') },
    @{ n = 'textual-prefix'; e = @($Physical, 'if ($ConfigPath.StartsWith($RepositoryRoot, [StringComparison]::Ordinal)) { Stop-Px InsideRepository }')
        red = @('A3-02:ACCEPTED_INVALID[case-variant config path]', 'A3-03:REJECTED_VALID[same-prefix sibling outside repository]') },
    @{ n = 'display-path-containment'; e = @($Physical, 'if ($ConfigPath.StartsWith($RepositoryRoot.TrimEnd(''\'') + ''\'', [StringComparison]::OrdinalIgnoreCase)) { Stop-Px InsideRepository }')
        red = @('A3-05:ACCEPTED_INVALID[SUBST alias of a repository subdirectory]') },
    @{ n = 'accept-multilink'; e = @('if ($file.Links -ne 1) { Stop-Px MultiLink }', ''); red = @('A3-06:ACCEPTED_INVALID[external hardlink to a repository file]') },
    @{ n = 'accept-reparse'; e = @($AttrCheck, '', '-not (Test-PxChild $parent.Final $node.Final)', '$false')
        red = @('A3-04:ACCEPTED_INVALID[junction ancestor]', 'A3-04:ACCEPTED_INVALID[junction repository root]', 'A3-05:ACCEPTED_INVALID[SUBST backing through junction]') },
    # Attribute check alone: ancestors still stop at parent/child, a LAST-component junction (H1 never reached it) passes.
    @{ n = 'accept-reparse-attr'; e = @($AttrCheck, ''); red = @('A3-04:ACCEPTED_INVALID[junction repository root]') },
    @{ n = 'control-reparse-code'; k = 'c'; target = 'accept-reparse'; e = @('{ Stop-Px ReparsePoint }', '{ Stop-Px Unverifiable }')
        red = @('A3-04:WRONG_CODE[junction ancestor]', 'A3-05:WRONG_CODE[SUBST backing through junction]') },
    @{ n = 'ignore-subst-backing'; e = @($Backing, '$want = (Open-PxNode "$Drive\" 3 ''Unverifiable'' $Ctx).Final')
        red = @('A3-05:ACCEPTED_INVALID[SUBST backing through junction]', 'A3-05:ACCEPTED_INVALID[repository root as SUBST through junction]') },
    @{ n = 'reject-external-subst'; e = @($Backing, 'Stop-Px Unverifiable'); red = @('A3-05:REJECTED_VALID[SUBST path physically outside the repository]') },
    @{ n = 'ignore-mount-topology'; vhd = $true; e = @('if (-not $Ctx.Seen.Add($vol)) { return }', 'return'); red = @('A3-08:ACCEPTED_INVALID[volume mounted inside repository]') },
    @{ n = 'allow-unknown'; e = @('Stop-Px SecretField', '', 'Stop-Px UnknownField', ''); red = @('A2-05:ACCEPTED_INVALID[unknown field]', 'A4-01:ACCEPTED_INVALID[password]') },
    @{ n = 'echo-raw'; e = @('$msg = "Config rejected: $Code."', '$msg = "Config rejected: $Code." + $Field', '(New-PxError $code $field)', '(New-PxError $code ([string]$text))')
        red = @('A4-01:SENTINEL_ECHOED[password]') },
    @{ n = 'side-effect'; e = @('$repo = Open-PxChain', 'Invoke-WebRequest -Uri https://side-effect.invalid/ -UseBasicParsing | Out-Null; $repo = Open-PxChain'); red = @('A5-03:SIDE_EFFECT_HITS[') },
    @{ n = 'uri-userinfo'; e = @('[^\s\p{Cc}/?#@\\]+', '[^\s\p{Cc}/?#\\]+', ' -and -not $u.UserInfo', ''); red = @('A2-06:ACCEPTED_INVALID[uri https://u:p@gw.example.invalid/]') },
    @{ n = 'uri-path-at-rejected'; e = @('(/[^\s\p{Cc}?#\\]*)?', '(/[^\s\p{Cc}?#@\\]*)?'); red = @('A2-06:REJECTED_VALID[uri path with @]') },
    @{ n = 'sample-secret'; f = 's'; e = @('"configurationName"', '"password": "x", "configurationName"'); red = @('A6-01:SAMPLE_FIELDS[') },
    @{ n = 'sample-version'; f = 's'; e = @('"schemaVersion": 1', '"schemaVersion": 2'); red = @('A6-01:SAMPLE_VERSION[') },
    @{ n = 'cleanup-failure'; k = 'i'; e = @(); red = @() })
foreach ($m in $Cx) { if (-not $m['k']) { $m['k'] = 'm' }; $m['f'] = "$($m['f'])"; $m['vhd'] = [bool]$m['vhd'] }
$Report.counterexample_ids = @($Cx | ForEach-Object { "CX-$($_.n)" })
function Test-Counterexample($M, [int]$Rc, $Rec) {
    if (-not [IO.File]::Exists($Rec.report_path)) { throw "child report absent (rc=$Rc)" }
    $rep = [IO.File]::ReadAllText($Rec.report_path) | ConvertFrom-Json
    $state = "rc=$Rc setup_error=$($rep.setup_error) cleanup=$($rep.cleanup.status) [$($rep.cleanup.errors -join '; ')]"
    if ($M.k -eq 'i') {
        $kept = @($rep.cleanup.subst | Where-Object { -not $_.removed })
        $bad = $Rc -ne 2 -or $rep.setup_error -or $rep.failed -or $rep.passed -ne $rep.total -or $rep.total -lt $Ids.Count -or $kept.Count
        if ($bad -or "$($rep.cleanup.errors)" -notlike '*pxlocked.bin*' -or $rep.cleanup.keep_sentinel_intact -ne $true -or -not [IO.Directory]::Exists("$($rep.scratch)")) { throw "injected cleanup failure not reported as required ($state)" }
        return 'CLEANUP_FAILURE_REPORTED: rc 2, every case passed, owned SUBSTs removed, outside sentinel intact, scratch and report kept'
    }
    if ($Rc -ne 1 -or $rep.setup_error -or $rep.cleanup.status -ne 'ok') { throw "want rc=1, no setup error and verified resource cleanup ($state)" }
    $hit = Get-Kill $rep $M.red; $Rec.matched = @($hit)
    if ($hit.Count -ne $M.red.Count) { throw "named failure(s) missing: $(@($M.red | Where-Object { $w = $_; -not @($hit | Where-Object { $_.want -eq $w }).Count }) -join '; ')" }
    if ($M.k -eq 'm') { $Rec.credited = $true; return 'KILLED: every named behavioural failure observed' }
    $target = @($Cx | Where-Object { $_.n -eq $M.target })[0]
    $acc = @($rep.cases | Where-Object { "$($_.reason)".Contains('ACCEPTED_INVALID') }).Count
    if ($acc -or (Get-Kill $rep $target.red).Count -eq $target.red.Count) { throw "control reached forbidden behaviour or would earn $($M.target) credit" }
    return "CONTROL_NO_CREDIT: rejects with another code only; $($M.target) tokens not satisfied"
}
if ($Counterexamples) {
    $Exe = [Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
    foreach ($m in $Cx) {
        Invoke-Case "CX-$($m.n)" @() {
            if ($m.vhd -and -not $Vhd) { throw 'UNAVAILABLE: this counterexample needs -VhdFixture' }
            $tag = "$Evid\cx-$($m.n)"; $mp = $ModulePath; $sp = $SamplePath; $mut = $null
            if ($m.k -ne 'i') {
                $src = [IO.File]::ReadAllText($(if ($m.f -eq 's') { $SamplePath } else { $ModulePath }))
                for ($i = 0; $i -lt $m.e.Count; $i += 2) {
                    $at = $src.IndexOf($m.e[$i], [StringComparison]::Ordinal)
                    if ($at -lt 0 -or $src.IndexOf($m.e[$i], $at + 1, [StringComparison]::Ordinal) -ge 0) { throw "ANCHOR: mutation anchor absent or not unique: $($m.e[$i])" }
                    $src = $src.Substring(0, $at) + $m.e[$i + 1] + $src.Substring($at + $m.e[$i].Length)
                }
                if ($m.f -eq 's') { $sp = $mut = "$tag.mutant.json" } else { $mp = $mut = "$tag.mutant.psm1" }; [IO.File]::WriteAllText($mut, $src, $Utf8)
            }
            $d = "$S\cx\$($m.n)"; $null = [IO.Directory]::CreateDirectory($d)
            $argv = [Collections.Generic.List[string]]@('-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-ModulePath', $mp,
                '-SamplePath', $sp, '-RepositoryRoot', $RepositoryRoot, '-ScratchRoot', $d, '-ReportPath', "$tag.report.json")
            if ($m.vhd) { $argv.Add('-VhdFixture') }; if ($m.k -eq 'i') { $argv.Add('-InjectCleanupFailure') }
            $run = Invoke-Native $Exe @($argv); [IO.File]::WriteAllText("$tag.output.txt", "$($run.out)", $Utf8)
            # Hashes are taken right after the child exits, before anything else reads or removes anything.
            $rec = [ordered]@{ id = "CX-$($m.n)"; kind = $m.k; command = @($Exe) + @($argv); rc = $run.rc; mutant_path = $mut; mutant_sha256 = (Get-FileSha256 $mut)
                report_path = "$tag.report.json"; report_sha256 = (Get-FileSha256 "$tag.report.json"); output_path = "$tag.output.txt"; output_sha256 = (Get-FileSha256 "$tag.output.txt")
                required = $m.red; matched = @(); credited = $false; verdict = $null }
            $Report.counterexample_evidence.Add($rec)
            try { $rec.verdict = Test-Counterexample $m $run.rc $rec } catch { $rec.verdict = "NOT_ACCEPTED: $($_.Exception.Message)"; throw }
            finally { [IO.File]::WriteAllText("$tag.record.json", ($rec | ConvertTo-Json -Depth 6), $Utf8) }
        }
    }
}
$missing = @(($Ids + $Closure + 'A3-07') | Where-Object { $i = $_; @($Results | Where-Object { $_.id -eq $i }).Count -ne 1 })
if ($missing.Count) { throw "IDs not executed exactly once: $($missing -join ',')" }
$required = @($Ids) + @($(if ($VhdFixture) { $Closure }))
$notPassed = @($Results | Where-Object { $required -contains $_.id -and $_.outcome -ne 'passed' })
$rc = $(if (@(Get-OutcomeIds 'setup_error').Count) { 2 } elseif (@(Get-OutcomeIds 'failed').Count -or $notPassed.Count) { 1 } else { 0 })
Complete-Run $rc
