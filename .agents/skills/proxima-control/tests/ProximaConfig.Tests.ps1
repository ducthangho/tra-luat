# ProximaConfig.Tests.ps1 - wp1271 r3 focused harness for Read-ProximaConfig; self-contained, no Pester.
# The SAME harness and ID set run on any tree via explicit -ModulePath (baseline or candidate), e.g.
#   powershell.exe|pwsh.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File <copy>\ProximaConfig.Tests.ps1 `
#     -ModulePath <tree>\.agents\skills\proxima-control\scripts\ProximaConfig.psm1 `
#     -ScratchRoot <existing long-name dir outside the tree> -ReportPath <json outside the tree> [-Counterexamples]
# rc 0: every mandatory ID ran once and passed. rc 1: a case failed; an absent module/API fails each case with
# API_ABSENT and every case still executes. rc 2: setup error (harness, fixture or existing-module import), never a
# test outcome. Optional A3-07 (8.3 alias) is 'unavailable' when the volume shows no short name; it is never a pass.
# -Counterexamples mutates COPIES of module/sample under ScratchRoot and requires each mutant to fail the named case
# for the named reason. Helpers have descriptive alias-free names: H0's helper R lost to the default alias r
# (Invoke-History) because aliases win over functions. Default aliases stay; setup proves no helper is shadowed.
[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$ModulePath, [Parameter(Mandatory = $true)][string]$ScratchRoot,
    [string]$ReportPath = '', [string]$RepositoryRoot = '', [string]$SamplePath = '', [switch]$Counterexamples)
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$Ids = 'A1-01', 'A1-02', 'A2-01', 'A2-02', 'A2-03', 'A2-04', 'A2-05', 'A2-06', 'A2-07', 'A3-01', 'A3-02', 'A3-03', 'A3-04', 'A3-05', 'A3-06',
'A4-01', 'A5-01', 'A5-02', 'A6-01', 'A6-02', 'A5-03'
$Results = [Collections.Generic.List[object]]::new()
$Report = [ordered]@{ schema = 'proxima_config_tests.v2'; ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"
    module_path = $ModulePath; module_sha256 = $null; sample_sha256 = $null; harness_sha256 = $null; api_state = 'unknown'
    alias_r = $null; subst_drive = $null; short_name_alias = $null; setup_error = $null; mandatory_ids = $Ids; optional_ids = @('A3-07')
    total = 0; passed = 0; failed = 0; failed_ids = @(); setup_error_ids = @(); unavailable_ids = @(); cases = $Results }
$Utf8 = [Text.UTF8Encoding]::new($false); $Sha = [Security.Cryptography.SHA256]::Create()
$SubstExe = [Environment]::SystemDirectory + '\subst.exe'; $SubstDrive = $null; $SubstMarker = $null
function Get-FileSha256([string]$P) { if ($P -and [IO.File]::Exists($P)) { ([BitConverter]::ToString($Sha.ComputeHash([IO.File]::ReadAllBytes($P))) -replace '-').ToLowerInvariant() } }
# Removes only the SUBST letter this run created, and only while it still shows this run's marker file.
function Remove-TestSubst {
    if ($script:SubstDrive -and [IO.File]::Exists("$($script:SubstDrive)\$($script:SubstMarker)")) { $null = & $SubstExe $script:SubstDrive /D }
    $script:SubstDrive = $null
}
function Get-OutcomeIds([string]$Outcome) { @($Results | Where-Object { $_.outcome -eq $Outcome } | ForEach-Object { $_.id }) }
function Complete-Run([int]$Rc) {
    Remove-TestSubst
    $Report.failed_ids = @(Get-OutcomeIds 'failed'); $Report.setup_error_ids = @(Get-OutcomeIds 'setup_error'); $Report.unavailable_ids = @(Get-OutcomeIds 'unavailable')
    $Report.passed = @(Get-OutcomeIds 'passed').Count; $Report.failed = $Report.failed_ids.Count
    $Report.total = $Report.passed + $Report.failed + $Report.setup_error_ids.Count
    $Report.harness_sha256 = Get-FileSha256 $PSCommandPath; $Report.module_sha256 = Get-FileSha256 $ModulePath; $Report.sample_sha256 = Get-FileSha256 $SamplePath
    if ($ReportPath) { [IO.File]::WriteAllText($ReportPath, ($Report | ConvertTo-Json -Depth 4), $Utf8) }
    Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; setup_error_ids=[{3}]; unavailable_ids=[{4}]; api_state={5}; setup_error={6}; rc={7}' -f $Report.passed,
        $Report.total, ($Report.failed_ids -join ','), ($Report.setup_error_ids -join ','), ($Report.unavailable_ids -join ','), $Report.api_state, $Report.setup_error, $Rc)
    exit $Rc
}
trap { $Report.setup_error = "$($_.Exception.Message)"; Write-Host "SETUP_ERROR $($Report.setup_error)"; Complete-Run 2 }
function Get-TreeSnapshot([string]$Root, [switch]$Meta) {
    if (-not [IO.Directory]::Exists($Root)) { return 'absent' }
    $rows = foreach ($p in [IO.Directory]::GetFileSystemEntries($Root, '*', [IO.SearchOption]::AllDirectories)) {
        if (-not [IO.File]::Exists($p)) { "$p|dir" } elseif ($Meta) { $f = [IO.FileInfo]::new($p); "$p|$($f.Length)|$($f.LastWriteTimeUtc.Ticks)" } else { "$p|$(Get-FileSha256 $p)" } }
    return (@($rows) | Sort-Object) -join "`n"
}
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
# One guarded read: scratch tree bytes and sentinel count must not change; every error text is collected.
function Invoke-GuardedRead([string]$Cfg, [string]$Repo = "$S\repo") {
    $before = Get-TreeSnapshot $S; $hits = $global:PxHits.Count; $global:Error.Clear(); $o = $null; $e = $null
    try { $o = Read-ProximaConfig -ConfigPath $Cfg -RepositoryRoot $Repo } catch { $e = $_ }
    if ((Get-TreeSnapshot $S) -cne $before) { throw 'filesystem tree/bytes changed during read' }
    if ($global:PxHits.Count -ne $hits) { throw 'side-effect sentinel hit during read' }
    $text = @(@($global:Error) + @($e) | Where-Object { $_ } | ForEach-Object { ($_ | Format-List * -Force | Out-String) + "$_" +
            $(if ($_ -is [Management.Automation.ErrorRecord]) { $_.Exception | Format-List * -Force | Out-String }) }) -join "`n"
    return [pscustomobject]@{ Out = $o; Err = $e; Text = $text }
}
function Assert-Rejected($X, [string]$Code, [string]$Label) {
    $id = $(if ($X.Err) { $X.Err.FullyQualifiedErrorId } else { '<none>' })
    if ($null -ne $X.Out) { throw "accepted invalid input [$Label]" }
    if (-not $X.Err -or ($Code -and $id -notmatch "^ProximaConfig\.$Code(,|\z)")) { throw "expected ProximaConfig.$Code, got $id [$Label]" }
}
function Assert-Accepted($X, [string]$TargetId, [string]$Label) {
    if ($null -eq $X.Out -or $X.Out.targetId -cne $TargetId) { throw "valid config rejected or altered [$Label]: $(if ($X.Err) { $X.Err.FullyQualifiedErrorId })" }
}
function Invoke-Case([string]$Id, [string[]]$Needs, [scriptblock]$Body) {
    $why = $null; $outcome = 'passed'
    try {
        if ($Needs -contains 'api' -and -not $ApiPresent) { throw "API_ABSENT: Read-ProximaConfig not available from ModulePath ($($Report.api_state))" }
        if ($Needs -contains 'module' -and -not [IO.File]::Exists($ModulePath)) { throw 'API_ABSENT: module file absent' }
        if ($Needs -contains 'sample' -and -not [IO.File]::Exists($SamplePath)) { throw 'API_ABSENT: sample file absent' }
        Set-TestLocation $S; & $Body
    } catch {
        $why = "$($_.Exception.Message)"
        $outcome = $(if ($why.StartsWith('SETUP:')) { 'setup_error' } elseif ($why.StartsWith('UNAVAILABLE:')) { 'unavailable' } else { 'failed' })
    } finally { Set-TestLocation $S }
    $Results.Add([pscustomobject]@{ id = $Id; outcome = $outcome; reason = $why })
    Write-Host ('{0} {1}{2}' -f $outcome.ToUpperInvariant(), $Id, $(if ($why) { " :: $why" }))
}
# ---- setup: any failure here is rc 2 ----
if ([Environment]::OSVersion.Platform -ne 'Win32NT') { throw 'Windows host required' }
$Helpers = 'Get-FileSha256', 'Remove-TestSubst', 'Get-OutcomeIds', 'Complete-Run', 'Get-TreeSnapshot', 'Get-EnvSnapshot', 'Set-TestLocation', 'Write-Fixture',
'New-ConfigJson', 'Invoke-GuardedRead', 'Assert-Rejected', 'Assert-Accepted', 'Invoke-Case'
$shadowed = @($Helpers | Where-Object { Get-Alias -Name $_ -ErrorAction SilentlyContinue })
if ($shadowed.Count) { throw "helper(s) shadowed by an alias: $($shadowed -join ',')" }
$Report.alias_r = "$(@(Get-Alias -Name r -ErrorAction SilentlyContinue | ForEach-Object { $_.Definition }))"
$ModulePath = [IO.Path]::GetFullPath($ModulePath); $Report.module_path = $ModulePath; $ModuleDir = Split-Path -Parent $ModulePath
if (-not $RepositoryRoot) { $RepositoryRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ModuleDir))) }
if (-not $SamplePath) { $SamplePath = Join-Path (Split-Path -Parent $ModuleDir) 'config.example.json' }
$RepositoryRoot = [IO.Path]::GetFullPath($RepositoryRoot).TrimEnd('\'); $SamplePath = [IO.Path]::GetFullPath($SamplePath)
foreach ($p in $ScratchRoot, $ReportPath) {
    if ($p -and [IO.Path]::GetFullPath($p).StartsWith($RepositoryRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'ScratchRoot/ReportPath must be outside the measured tree' }
}
if (-not [IO.Directory]::Exists($ScratchRoot)) { throw 'ScratchRoot must be an existing directory' }
$S = [IO.Path]::GetFullPath($ScratchRoot).TrimEnd('\') + '\pxcfg-' + [guid]::NewGuid().ToString('N').Substring(0, 12)
foreach ($d in 'repo\cfg', 'repo\pxshortnamealias', 'repo-sibling', 'ext1', 'ext2', 'cx') { $null = [IO.Directory]::CreateDirectory("$S\$d") }
foreach ($j in @('jn', 'ext1'), @('jin', 'repo\cfg'), @('repojn', 'repo')) { $null = New-Item -ItemType Junction -Path "$S\$($j[0])" -Value "$S\$($j[1])" }
# Hardlink alias: an external name for a file inside the repository (H0 accepted it).
$null = Write-Fixture 'repo\cfg\linked.json' (New-ConfigJson); $null = New-Item -ItemType HardLink -Path "$S\ext1\hardlink.json" -Value "$S\repo\cfg\linked.json"
if ([IO.FileInfo]::new("$S\ext1\hardlink.json").Length -ne [IO.FileInfo]::new("$S\repo\cfg\linked.json").Length) { throw 'hardlink fixture not created' }
# SUBST alias of a directory INSIDE the repository (H0 accepted it): first free letter, verified by a marker file.
$SubstMarker = 'pxsubst-' + [guid]::NewGuid().ToString('N') + '.txt'; $null = Write-Fixture "repo\cfg\$SubstMarker" 'marker'
foreach ($l in [char[]]'ZYXWVUTSRQPONMLKJIHG') {
    if ([IO.Directory]::Exists("${l}:\") -or @([IO.DriveInfo]::GetDrives() | Where-Object { $_.Name -eq "${l}:\" }).Count) { continue }
    $null = & $SubstExe "${l}:" "$S\repo\cfg"
    if ($LASTEXITCODE -eq 0) { $SubstDrive = "${l}:"; break }
}
if (-not $SubstDrive -or -not [IO.File]::Exists("$SubstDrive\$SubstMarker")) { throw 'SUBST alias fixture could not be created/verified' }
$Report.subst_drive = $SubstDrive
# 8.3 alias: capability evidence only. A short name is used only when it really resolves to this directory.
$null = Write-Fixture 'repo\pxshortnamealias\in.json' (New-ConfigJson)
$ShortAlias = $(if ([IO.File]::Exists("$S\repo\PXSHOR~1\in.json")) { 'PXSHOR~1' }); $Report.short_name_alias = $(if ($ShortAlias) { 'observed' } else { 'unavailable' })
$EnvBefore = Get-EnvSnapshot; $RepoBefore = Get-TreeSnapshot $RepositoryRoot -Meta
# Scoped side-effect sentinels: global functions shadow these cmdlets for the module from here on; each call is
# recorded and throws. The harness itself uses only .NET calls (and subst.exe cleanup) below this line.
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
    foreach ($r in $r1, $r2, $r3) { if ($null -eq $r.Out) { throw "valid external config rejected: $(if ($r.Err) { $r.Err.FullyQualifiedErrorId })" } }
    if ((@($r1.Out.PSObject.Properties.Name) -join ',') -cne 'schemaVersion,targetId,mode,basePath' -or $r1.Out.schemaVersion -ne 1 -or
        $r1.Out.targetId -cne 'tgt-one' -or $r1.Out.mode -cne 'Local' -or $r1.Out.basePath -cne 'C:\px1') { throw 'Local target values/properties wrong' }
    if ((@($r2.Out.PSObject.Properties.Name) -join ',') -cne 'schemaVersion,targetId,mode,basePath,connectionUri,configurationName' -or
        $r2.Out.targetId -cne 'tgt-two' -or $r2.Out.mode -cne 'Remote' -or $r2.Out.connectionUri -cne 'https://gw.example.invalid:5986/wsman' -or
        $r2.Out.configurationName -cne 'px.endpoint') { throw 'Remote target values/properties wrong' }
    if ($r3.Out.targetId -cne 'tgt-one') { throw 'result depends on the current directory' }
    # Every handle must be closed after the read: an exclusive open of the file and a rename of its directory succeed
    # (bounded retries only absorb a transient scanner handle; a leaked handle stays open and keeps this red).
    Set-TestLocation $S; $released = $false
    for ($t = 0; $t -lt 10 -and -not $released; $t++) {
        try { [IO.File]::Open($a, 'Open', 'ReadWrite', 'None').Dispose(); [IO.Directory]::Move("$S\ext1", "$S\ext1-moved"); $released = $true }
        catch { [Threading.Thread]::Sleep(200) }
    }
    if (-not $released) { throw 'a file or directory handle stayed open after the read' }
    [IO.Directory]::Move("$S\ext1-moved", "$S\ext1")
}
Invoke-Case 'A1-02' api {
    $uni = [regex]::Unescape('M\u1ee5c-ti\u00eau_\u76ee\u6a19') + [char]::ConvertFromUtf32(0x1F680); $cn = [regex]::Unescape('C\u1ea5u.H\u00ecnh'); $uri = 'HTTPS://GW.Example.Invalid:5986/WSMan'
    $r = Invoke-GuardedRead (Write-Fixture 'ext2\u.json' (New-ConfigJson -Remote @{ targetId = '"' + $uni + '"'; configurationName = '"' + $cn + '"'; connectionUri = '"' + $uri + '"' }))
    Assert-Accepted $r $uni 'Unicode targetId'
    if ($r.Out.configurationName -cne $cn -or $r.Out.connectionUri -cne $uri) { throw 'Unicode configurationName or uppercase HTTPS rejected or altered' }
    $long = 'T' * 300; Assert-Accepted (Invoke-GuardedRead (Write-Fixture 'ext2\l.json' (New-ConfigJson @{ targetId = '"' + $long + '"' }))) $long 'long targetId'
    $esc = [char]::ConvertFromUtf32(0x1F680) + 'x'; Assert-Accepted (Invoke-GuardedRead (Write-Fixture 'ext2\e.json' (New-ConfigJson @{ targetId = '"\ud83d\ude80x"' }))) $esc 'escaped surrogate pair'
}
Invoke-Case 'A2-01' api {
    $m = "$S\ext1\missing.json"; Assert-Rejected (Invoke-GuardedRead $m) 'NotFound' 'missing config'
    if ([IO.File]::Exists($m)) { throw 'missing config was synthesized on disk' }
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
            if ($r.Err.Exception.Message -notlike "*Field: $f.*") { throw "error does not name field $f" }
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
    foreach ($u in 'http://gw.example.invalid/wsman', 'https:/gw', '/wsman', 'gw.example.invalid:5986', 'https://u:p@gw.example.invalid/', 'ftp://gw.example.invalid/',
        'https://gw.example.invalid/?a=1', 'https://gw.example.invalid/#f', 'https://gw x.invalid/', 'https://gw.example.invalid/a@b', 'https://') {
        Assert-Rejected (Invoke-GuardedRead (Write-Fixture 'ext1\x.json' (New-ConfigJson -Remote @{ connectionUri = '"' + $u + '"' }))) 'InvalidField' "uri $u"
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
Invoke-Case 'A4-01' api {
    $z = 'PXSENTINEL' + [guid]::NewGuid().ToString('N'); $q = '"' + $z + '"'
    $all = @(@('SecretField', (New-ConfigJson @{ password = $q })), @('SecretField', (New-ConfigJson @{ apiToken = $q })), @('SecretField', (New-ConfigJson @{ Client_Secret = $q })),
        @('SecretField', (New-ConfigJson @{ cookie = $q })), @('SecretField', (New-ConfigJson @{ credential = '{"u":' + $q + '}' })), @('UnknownField', (New-ConfigJson @{ notes = $q })),
        @('InvalidField', (New-ConfigJson @{ targetId = '"' + $z + ' x"' })), @('InvalidField', (New-ConfigJson @{ mode = $q })),
        @('InvalidField', (New-ConfigJson -Remote @{ connectionUri = '"https://u:' + $z + '@gw.example.invalid/"' })),
        @('InvalidField', (New-ConfigJson -Remote @{ connectionUri = '"https://gw.example.invalid/?k=' + $z + '"' })),
        @('MalformedJson', ('{"targetId":' + $q + ',')), @('NotObject', $q))
    foreach ($c in $all) {
        $r = Invoke-GuardedRead (Write-Fixture 'ext1\s.json' $c[1]); Assert-Rejected $r $c[0] $c[0]
        if ($r.Text -notlike '*ProximaConfig*') { throw 'error text was not captured' }
        if ($r.Text.Contains($z)) { throw "error text contains sentinel value [$($c[0])]" }
    }
}
Invoke-Case 'A5-01' module {
    $src = [IO.File]::ReadAllText($ModulePath)
    $hit = @($Forbidden | Where-Object { $src.IndexOf($_, [StringComparison]::OrdinalIgnoreCase) -ge 0 })
    if ($hit.Count) { throw "forbidden side-effect token(s) in module: $($hit -join ', ')" }
}
Invoke-Case 'A5-02' api {
    if ($ImportHits -ne 0) { throw "import hit $ImportHits side-effect sentinel(s)" }
    if (($Exported -join ',') -cne 'Read-ProximaConfig') { throw "unexpected exports: $($Exported -join ',')" }
    $p = (Get-Command Read-ProximaConfig).Parameters
    foreach ($n in 'ConfigPath', 'RepositoryRoot') { if (-not @($p[$n].Attributes | Where-Object { $_ -is [Parameter] -and $_.Mandatory }).Count) { throw "$n is not mandatory" } }
}
Invoke-Case 'A6-01' sample {
    $raw = [IO.File]::ReadAllText($SamplePath); $v = $raw | ConvertFrom-Json; $names = @($v.PSObject.Properties.Name)
    if (($names -join ',') -cne (@($SampleExpect.Keys) -join ',')) { throw "sample fields differ from schema: $($names -join ',')" }
    foreach ($k in $SampleExpect.Keys) { if ("$($v.$k)" -cne "$($SampleExpect[$k])") { throw "sample value of $k is not the expected placeholder" } }
    if ($v.schemaVersion -is [string] -or $raw -cnotmatch '"schemaVersion"\s*:\s*1\s*,') { throw 'sample schemaVersion is not integer 1' }
}
Invoke-Case 'A6-02' api, sample {
    $r = Invoke-GuardedRead (Write-Fixture 'ext2\sample-copy.json' ([IO.File]::ReadAllBytes($SamplePath)))
    if ($null -eq $r.Out) { throw "explicit external copy of the sample rejected: $(if ($r.Err) { $r.Err.FullyQualifiedErrorId })" }
    foreach ($k in $SampleExpect.Keys) { if ("$($r.Out.$k)" -cne "$($SampleExpect[$k])") { throw "reader returned an unexpected $k for the sample copy" } }
    Assert-Rejected (Invoke-GuardedRead $SamplePath $RepositoryRoot) 'InsideRepository' 'sample read in place'
    if ([IO.File]::ReadAllText($ModulePath) -match 'example') { throw 'module references the sample (implicit fallback)' }
}
Invoke-Case 'A5-03' api {
    if ($global:PxHits.Count) { throw "side-effect sentinel hits: $($global:PxHits -join ',')" }
    if ((Get-EnvSnapshot) -cne $EnvBefore) { throw 'environment variables changed' }
    if ((Get-TreeSnapshot $RepositoryRoot -Meta) -cne $RepoBefore) { throw 'repository tree changed' }
}
# ---- counterexamples: mutate scratch COPIES only, rerun this harness in a child, require the named kill ----
$Default = 'return [pscustomobject]@{ schemaVersion = 1; targetId = ''tgt-default''; mode = ''Local''; basePath = ''C:\px0'' }'
$Physical = '$file.Final.StartsWith($repo.Final.TrimEnd(''\'') + ''\'', [StringComparison]::OrdinalIgnoreCase)'
$Cx = @(@{ n = 'default-config'; f = 'm'; e = @('$repo = Open-PxChain', "$Default; `$repo = Open-PxChain"); red = @('A1-01:Local target') },
    @{ n = 'synthesize-missing'; f = 'm'; e = @('$file = Open-PxChain', "if (-not [IO.File]::Exists(`$ConfigPath)) { $Default }; `$file = Open-PxChain"); red = @('A2-01:accepted invalid') },
    @{ n = 'accept-wrong-type'; f = 'm'; e = @(' -or $o[$Name].K -cne $Kind', ''); red = @('A2-04:accepted invalid') },
    @{ n = 'ascii-only-text'; f = 'm'; e = @('return $V.Length -gt 0 -and', 'return $V -cmatch ''^[A-Za-z0-9][A-Za-z0-9._-]{0,127}\z'' -and'); red = @('A1-02:rejected or altered') },
    @{ n = 'textual-prefix'; f = 'm'; e = @($Physical, '$ConfigPath.StartsWith($RepositoryRoot, [StringComparison]::Ordinal)'); red = @('A3-02:accepted invalid', 'A3-03:sibling') },
    @{ n = 'display-path-containment'; f = 'm'; e = @($Physical, '$ConfigPath.StartsWith($RepositoryRoot.TrimEnd(''\'') + ''\'', [StringComparison]::OrdinalIgnoreCase)')
        red = @('A3-05:accepted invalid') },
    @{ n = 'accept-multilink'; f = 'm'; e = @('if ($file.Links -ne 1) { Stop-Px MultiLink }', ''); red = @('A3-06:accepted invalid') },
    @{ n = 'accept-reparse'; f = 'm'; e = @('if (($node.Attr -band $script:BadAttr) -ne 0) { Stop-Px ReparsePoint }', ''); red = @('A3-04:junction') },
    @{ n = 'allow-unknown'; f = 'm'; e = @('Stop-Px SecretField', '', 'Stop-Px UnknownField', ''); red = @('A2-05:accepted invalid', 'A4-01:accepted invalid') },
    @{ n = 'echo-raw'; f = 'm'; e = @('$msg = "Config rejected: $Code."', '$msg = "Config rejected: $Code." + $Field',
            '(New-PxError $code $field)', '(New-PxError $code ([string]$text))'); red = @('A4-01:sentinel') },
    @{ n = 'side-effect'; f = 'm'; e = @('$repo = Open-PxChain', 'Invoke-WebRequest -Uri https://side-effect.invalid/ -UseBasicParsing | Out-Null; $repo = Open-PxChain'); red = @('A5-03:sentinel') },
    @{ n = 'sample-secret'; f = 's'; e = @('"configurationName"', '"password": "x", "configurationName"'); red = @('A6-01:sample fields') },
    @{ n = 'sample-version'; f = 's'; e = @('"schemaVersion": 1', '"schemaVersion": 2'); red = @('A6-01:schemaVersion') })
if ($Counterexamples) {
    $exe = [Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
    foreach ($m in $Cx) {
        Invoke-Case "CX-$($m.n)" none {
            $src = [IO.File]::ReadAllText($(if ($m.f -eq 'm') { $ModulePath } else { $SamplePath }))
            for ($i = 0; $i -lt $m.e.Count; $i += 2) {
                $at = $src.IndexOf($m.e[$i], [StringComparison]::Ordinal)
                if ($at -lt 0 -or $src.IndexOf($m.e[$i], $at + 1, [StringComparison]::Ordinal) -ge 0) { throw "mutation anchor absent or not unique: $($m.e[$i])" }
                $src = $src.Substring(0, $at) + $m.e[$i + 1] + $src.Substring($at + $m.e[$i].Length)
            }
            $d = "$S\cx\$($m.n)"; $null = [IO.Directory]::CreateDirectory($d); $mp = $ModulePath; $sp = $SamplePath
            if ($m.f -eq 'm') { $mp = "$d\ProximaConfig.psm1"; [IO.File]::WriteAllText($mp, $src, $Utf8) } else { $sp = "$d\config.example.json"; [IO.File]::WriteAllText($sp, $src, $Utf8) }
            $null = & $exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $PSCommandPath -ModulePath $mp -SamplePath $sp -RepositoryRoot $RepositoryRoot -ScratchRoot $d -ReportPath "$d.json"
            $rc = $LASTEXITCODE; $rep = [IO.File]::ReadAllText("$d.json") | ConvertFrom-Json
            if ($rc -ne 1 -or $rep.setup_error) { throw "mutant run rc=$rc setup_error=$($rep.setup_error); want rc=1 (killed) without setup error" }
            foreach ($want in $m.red) {
                $id, $why = $want -split ':', 2
                if (-not @($rep.cases | Where-Object { $_.id -eq $id -and $_.outcome -eq 'failed' -and "$($_.reason)" -like "*$why*" }).Count) { throw "mutant not killed by $want" }
            }
        }
    }
}
$missing = @($Ids | Where-Object { $i = $_; @($Results | Where-Object { $_.id -eq $i }).Count -ne 1 })
if ($missing.Count) { throw "mandatory IDs not executed exactly once: $($missing -join ',')" }
$rc = $(if (@(Get-OutcomeIds 'setup_error').Count) { 2 } elseif (@(Get-OutcomeIds 'failed').Count) { 1 } else { 0 })
Set-TestLocation ([IO.Path]::GetFullPath($ScratchRoot)); Remove-TestSubst
if ($rc -eq 0) { foreach ($j in 'jn', 'jin', 'repojn') { [IO.Directory]::Delete("$S\$j") }; [IO.Directory]::Delete($S, $true) } else { Write-Host "scratch kept for evidence: $S" }
Complete-Run $rc
