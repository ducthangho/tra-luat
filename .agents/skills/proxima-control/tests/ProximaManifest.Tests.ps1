# ProximaManifest.Tests.ps1 - wp1285 r1 (PROXIMA-P1-S3): self-contained harness (no Pester) for scripts/ProximaControl.psd1 (M1) + SKILL.md (M2).
#   powershell.exe|pwsh.exe -NoProfile -NonInteractive -File <copy>\ProximaManifest.Tests.ps1 -AddonRoot <tree>\.agents\skills\proxima-control `
#     -ScratchRoot <existing dir outside the repository> -ReportPath <json outside the add-on> [-Counterexamples]
# rc 0: PM01..PM07 (+CX00..CX04) passed, evidence re-verified. rc 1: a property failed (no manifest/SKILL => all seven run and fail
# MANIFEST_ABSENT/SKILL_ABSENT). rc 2: setup error or unavailable runtime only. PM01/PM02 judge the manifest STATICALLY (AST + SafeGetValue);
# only then do FRESH children import it (this process never loads Proxima): 'runtime' = PM03+PM06, 'tamper' = PM04 (see $ChildScript).
# Help calls only: no config, network, gateway, service, session or credential. <ScratchRoot>\pm-<run> keeps every child script, argv, raw
# stdout/stderr, output, private copy and mutation; nothing is deleted, all is re-hashed at the end. Children inherit the caller's policy.
using namespace System.Management.Automation.Language
[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$AddonRoot, [Parameter(Mandatory = $true)][string]$ScratchRoot,
    [Parameter(Mandatory = $true)][string]$ReportPath, [switch]$Counterexamples)
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$Ids = 'PM01', 'PM02', 'PM03', 'PM04', 'PM05', 'PM06', 'PM07'
$Want = @{ RootModule = 'ProximaControl.psm1'; ModuleVersion = '2.0.0'; GUID = '7f7055d6-51e3-4fb8-bbeb-7851a739bfb6'; PowerShellVersion = '5.1' }
$WantArrays = [ordered]@{ CompatiblePSEditions = @('Desktop', 'Core'); FunctionsToExport = @('px', 'Invoke-ProximaOperation'); CmdletsToExport = @()
    VariablesToExport = @(); AliasesToExport = @() }
$KeySet = [Collections.Generic.HashSet[string]]::new([string[]](@($Want.Keys) + @($WantArrays.Keys)), [StringComparer]::Ordinal)
$PxActions = [Collections.Generic.HashSet[string]]::new([string[]]('help config status models use ask start stop restart connect disconnect' -split ' '), [StringComparer]::Ordinal)
$Legacy = 'scripts/ProximaConfig.psm1', 'scripts/ProximaControl.psm1', 'scripts/Run-Px.ps1', 'config.example.json', 'tests/ProximaConfig.Tests.ps1', 'tests/ProximaControl.Tests.ps1'
$Tags = 'Scope', 'Entry points', 'Target', 'WhatIf', 'Versions', 'Limits'
$Utf8 = [Text.UTF8Encoding]::new($false, $true); $Sha = [Security.Cryptography.SHA256]::Create(); $Inv = [Globalization.CultureInfo]::InvariantCulture
$Results = [Collections.Generic.List[object]]::new(); $Artifacts = [Collections.Generic.List[object]]::new(); $Children = [Collections.Generic.List[object]]::new()
$Report = [ordered]@{ schema = 'proxima_manifest_tests.v1'; ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"
    culture = [Globalization.CultureInfo]::CurrentCulture.Name; ui_culture = [Globalization.CultureInfo]::CurrentUICulture.Name; launch = $null; addon_root = $AddonRoot
    harness_sha256 = $null; git_head = 'not_measured (no git in harness; the operator records H/tree)'; source_hashes = $null; manifest_state = 'unknown'
    skill_state = 'unknown'; setup_error = $null; required_ids = @(); total = 0; passed = 0; failed_ids = @(); setup_error_ids = @(); runtime_children = 0; tamper = $null
    cases = $Results; children = $Children; counterexamples = [Collections.Generic.List[object]]::new(); evidence = [ordered]@{ dir = $null; artifacts = $Artifacts; check = $null }; cleanup = $null }
$Run = $null; $Completing = $false
function Get-FileSha([string]$P) { if ([IO.File]::Exists($P)) { ([BitConverter]::ToString($Sha.ComputeHash([IO.File]::ReadAllBytes($P))) -replace '-', '').ToLowerInvariant() } }
function Join-Addon([string]$Base, [string]$Rel) { [IO.Path]::Combine($Base, $Rel.Replace([char]'/', [IO.Path]::DirectorySeparatorChar)) }
function Test-Inside([string]$Path, [string]$Dir) { $s = [IO.Path]::DirectorySeparatorChar; ($Path.TrimEnd($s) + $s).StartsWith($Dir.TrimEnd($s) + $s, [StringComparison]::OrdinalIgnoreCase) }
function Add-Artifact([string]$Role, [string]$Path) { $Artifacts.Add([ordered]@{ role = $Role; path = $Path; sha256 = (Get-FileSha $Path) }) }
function Save-Text([string]$Role, [string]$Path, [string]$Text) { [IO.File]::WriteAllText($Path, $Text, $Utf8); Add-Artifact $Role $Path }
# Property failures carry a marker; any other exception inside a case is a setup/runtime error (rc 2), never a test outcome.
function Stop-Case([string]$Reason) { $e = [Exception]::new($Reason); $e.Data['pm'] = 1; throw $e }
function Invoke-Case([string]$Id, [scriptblock]$Body) {
    $caseRec = [ordered]@{ id = $Id; outcome = 'passed'; reason = $null; detail = $null }
    try { $caseRec.detail = & $Body } catch { $caseRec.reason = "$($_.Exception.Message)"; $caseRec.outcome = $(if ($_.Exception.Data.Contains('pm')) { 'failed' } else { 'setup_error' }) }
    $Results.Add([pscustomobject]$caseRec)
}
# Every file under the add-on root -> sha256 (reparse points recorded, never followed).
function Get-Snapshot([string]$Base) {
    $map = [Collections.Generic.SortedDictionary[string, string]]::new([StringComparer]::Ordinal); $todo = [Collections.Generic.Stack[string]]::new(); $todo.Push($Base)
    while ($todo.Count) {
        foreach ($p in [IO.Directory]::GetFileSystemEntries($todo.Pop())) {
            $a = [int][IO.File]::GetAttributes($p); $rel = $p.Substring($Base.Length + 1).Replace([char]'\', [char]'/')
            if ($a -band 0x400) { $map[$rel] = 'reparse' } elseif ($a -band 0x10) { $todo.Push($p) } else { $map[$rel] = Get-FileSha $p }
        }
    }
    return , $map
}
function ConvertTo-ArgText([string]$T) { if ($T -cmatch '^[A-Za-z0-9_.:/\\-]+$') { return $T }; '"' + (($T -replace '(\\*)"', '$1$1\"') -replace '(\\+)$', '$1$1') + '"' }
# Fresh child of this same executable; argv, command line, raw stdout/stderr bytes and rc are kept. A timeout is a setup error.
function Start-Child([string]$Role, [string[]]$ArgList, [int]$TimeoutSec) {
    $base = [IO.Path]::Combine($Run, ('child{0:d2}-{1}' -f $Children.Count, $Role))
    $psi = [Diagnostics.ProcessStartInfo]::new($SelfExe); $psi.Arguments = @($ArgList | ForEach-Object { ConvertTo-ArgText $_ }) -join ' '
    $psi.UseShellExecute = $false; $psi.CreateNoWindow = $true; $psi.WorkingDirectory = $Run; foreach ($n in 'Input', 'Output', 'Error') { $psi."RedirectStandard$n" = $true }
    $ch = [ordered]@{ role = $Role; exe = $SelfExe; argv = $ArgList; arguments = $psi.Arguments; cwd = $Run; started_utc = [DateTime]::UtcNow.ToString('o', $Inv)
        ended_utc = $null; rc = $null; timed_out = $false; stdout = "$base.stdout.bin"; stderr = "$base.stderr.bin" }
    $Children.Add($ch); $so = [IO.MemoryStream]::new(); $se = [IO.MemoryStream]::new(); $proc = [Diagnostics.Process]::Start($psi)
    try {
        $proc.StandardInput.Close(); $t1 = $proc.StandardOutput.BaseStream.CopyToAsync($so); $t2 = $proc.StandardError.BaseStream.CopyToAsync($se)
        if (-not $proc.WaitForExit($TimeoutSec * 1000)) { $ch.timed_out = $true; try { $proc.Kill() } catch { $null = $_ }; $null = $proc.WaitForExit(30000) }
        $null = $t1.Wait(30000); $null = $t2.Wait(30000); if ($proc.HasExited) { $ch.rc = $proc.ExitCode }
    } finally { $proc.Dispose(); [IO.File]::WriteAllBytes($ch.stdout, $so.ToArray()); [IO.File]::WriteAllBytes($ch.stderr, $se.ToArray()) }
    $ch.ended_utc = [DateTime]::UtcNow.ToString('o', $Inv); Add-Artifact "$Role-stdout" $ch.stdout; Add-Artifact "$Role-stderr" $ch.stderr
    Save-Text "$Role-command" "$base.command.json" ($ch | ConvertTo-Json -Depth 4)
    if ($ch.timed_out) { throw "child $Role timed out after $TimeoutSec s (killed; partial output kept)" }; return $ch
}
function Read-Skill([string]$Path) {
    $doc = [ordered]@{ text = ''; decode = 'ok'; fm = $null; sections = [Collections.Generic.List[object]]::new(); code = [Collections.Generic.List[string]]::new() }
    try { $doc.text = [IO.File]::ReadAllText($Path, $Utf8) } catch { $doc.decode = 'invalid_utf8' }
    $lines = @($doc.text -split "`r?`n"); $i = 0; $cur = $null; $lang = $null
    if ($lines[0] -ceq '---') {
        $fm = [ordered]@{}
        for ($i = 1; $i -lt $lines.Count -and $lines[$i] -cne '---'; $i++) { if ($lines[$i] -cmatch '^([a-z]+):\s*(.*)$') { $fm[$Matches[1]] = $Matches[2].Trim() } }
        if ($i -lt $lines.Count) { $doc.fm = $fm; $i++ } else { $i = 0 }
    }
    for (; $i -lt $lines.Count; $i++) {
        $l = $lines[$i]
        if ($l -cmatch '^```(\S*)') { $lang = $(if ($null -eq $lang) { $Matches[1] }); continue }
        # '## Heading (Tag)' -> tag 'Tag'; a heading without a trailing '(...)' gets an empty tag.
        if ($null -eq $lang -and $l -cmatch '^## (?:.*\(([^()]+)\)\s*|.*)$') { $cur = [pscustomobject]@{ tag = "$($Matches[1])"; body = [Collections.Generic.List[string]]::new() }; $doc.sections.Add($cur); continue }
        if ($lang -ceq 'powershell') { $doc.code.Add($l) }
        if ($null -ne $cur) { $cur.body.Add($l) }
    }
    return [pscustomobject]$doc
}
function Get-Section([string]$Tag) { (@($Doc.sections | Where-Object { $_.tag -ceq $Tag } | ForEach-Object { $_.body }) -join "`n") }
# First command of each non-comment powershell code line: name, positional action, -Parameter -> following value (or $null).
function Get-DocCommands {
    foreach ($line in $Doc.code) {
        if (-not $line.Trim() -or $line.TrimStart().StartsWith('#')) { continue }
        $tk = $null; $er = $null; $cmd = [Parser]::ParseInput($line, [ref]$tk, [ref]$er).Find({ param($n) $n -is [CommandAst] }, $true)
        $item = [pscustomobject]@{ line = $line; errors = @($er).Count; name = ''; action = ''; params = @{} }
        if ($null -eq $cmd) { $item; continue }
        $el = @($cmd.CommandElements); $item.name = "$($cmd.GetCommandName())"
        if ($el.Count -gt 1 -and $el[1] -is [StringConstantExpressionAst]) { $item.action = $el[1].Value }
        for ($j = 1; $j -lt $el.Count; $j++) {
            if ($el[$j] -isnot [CommandParameterAst]) { continue }
            $nx = $(if ($j + 1 -lt $el.Count -and $el[$j + 1] -isnot [CommandParameterAst]) { $el[$j + 1] })
            $item.params[$el[$j].ParameterName] = $(if ($nx -is [StringConstantExpressionAst]) { $nx.Value } elseif ($null -ne $nx) { $nx.Extent.Text })
        }
        $item
    }
}
function Complete-Run([int]$Rc) {
    if ($script:Completing) { exit 2 }
    $script:Completing = $true; $errs = [Collections.Generic.List[string]]::new(); $n = 0
    try {
        $nested = @(foreach ($cx in $Report.counterexamples) { if ([IO.File]::Exists($cx.report_path)) { ([IO.File]::ReadAllText($cx.report_path, $Utf8) | ConvertFrom-Json).evidence.artifacts } })
        foreach ($a in @($Artifacts) + $nested) { $n++; if (-not $a.sha256 -or (Get-FileSha ([string]$a.path)) -cne [string]$a.sha256) { $errs.Add("EVIDENCE_MISSING_OR_CHANGED[$($a.role) $($a.path)]") } }
    } catch { $errs.Add("EVIDENCE_CHECK_ERROR $($_.Exception.Message)") }
    $Report.evidence.check = [ordered]@{ status = $(if ($errs.Count) { 'failed' } else { 'ok' }); verified = $n; errors = @($errs); scope = 'own + nested CX artifacts, after all cases' }
    $Report.cleanup = [ordered]@{ status = 'ok'; policy = 'retain_all: this run deletes nothing; evidence is re-hashed instead'; deleted = 0; retained_dir = $Run }; if ($errs.Count) { $Rc = 2 }
    foreach ($oc in 'failed', 'setup_error') { $Report["$($oc)_ids"] = @($Results | Where-Object { $_.outcome -ceq $oc } | ForEach-Object { $_.id }) }
    $Report.passed = @($Results | Where-Object { $_.outcome -ceq 'passed' }).Count; $Report.total = $Results.Count; $Report.harness_sha256 = Get-FileSha $PSCommandPath
    $Report.runtime_children = @($Children | Where-Object { $_.role -ceq 'runtime' -or $_.role -ceq 'tamper' }).Count
    try { [IO.File]::WriteAllText($ReportPath, ($Report | ConvertTo-Json -Depth 8), $Utf8) } catch { Write-Host "REPORT_WRITE_ERROR $($_.Exception.Message)"; $Rc = 2 }
    Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; setup_error_ids=[{3}]; manifest={4}; skill={5}; setup_error={6}; evidence={7}; rc={8}' -f $Report.passed, $Report.total,
        ($Report.failed_ids -join ','), ($Report.setup_error_ids -join ','), $Report.manifest_state, $Report.skill_state, $Report.setup_error, $Report.evidence.check.status, $Rc)
    exit $Rc
}
trap { $Report.setup_error = "$($_.Exception.Message)"; Write-Host "SETUP_ERROR $($Report.setup_error)"; Complete-Run 2 }
# ---- child script (written into the evidence dir per phase, executed there, kept) ----
$ChildScript = @'
# runtime (PM03+PM06): Test-ModuleManifest, manifest import, px help, then the UNCHANGED Run-Px.ps1 help in this same process with a test-owned
# in-memory sentinel in the module. tamper (PM04): import a private copy whose ProximaConfig.psm1 has a harmless sentinel line; S2 must reject it.
param([string]$Mode, [string]$ManifestPath, [string]$SentinelPath, [string]$OutPath)
Set-StrictMode -Version 3.0; $ErrorActionPreference = 'Stop'
$r = [ordered]@{ mode = $Mode; ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"; culture = [Globalization.CultureInfo]::CurrentCulture.Name
    preloaded = @(Get-Module -Name ProximaControl, ProximaConfig | ForEach-Object { $_.Path }); test_manifest = $null; module = $null; help = $null; wrapper = $null
    imported = $false; error = $null; messages = @(); sentinel_exists = $false; loaded_after = @() }
$scripts = [IO.Path]::GetDirectoryName($ManifestPath)
try {
    if ($Mode -ceq 'tamper') { $null = Import-Module -Name $ManifestPath -DisableNameChecking -ErrorAction Stop; $r.imported = $true; return }
    $tm = Test-ModuleManifest -Path $ManifestPath -ErrorAction Stop; $r.test_manifest = [ordered]@{ version = "$($tm.Version)"; guid = "$($tm.Guid)"; root_module = "$($tm.RootModule)" }
    $m = Import-Module -Name $ManifestPath -PassThru -Global -DisableNameChecking -ErrorAction Stop; $r.imported = $true
    $r.module = [ordered]@{ path = $m.Path; version = "$($m.Version)"; guid = "$($m.Guid)"; commands = @($m.ExportedCommands.Keys); functions = @($m.ExportedFunctions.Keys).Count
        others = @($m.ExportedCmdlets.Keys).Count + @($m.ExportedAliases.Keys).Count + @($m.ExportedVariables.Keys).Count; loaded = @(Get-Module -Name ProximaControl).Count
        path_is_root_module = [string]::Equals([IO.Path]::GetFullPath($m.Path), [IO.Path]::Combine($scripts, 'ProximaControl.psm1'), [StringComparison]::OrdinalIgnoreCase) }
    $h = & $m.ExportedCommands['px'] help; $r.help = [ordered]@{ schema = "$($h.schema)"; action = "$($h.action)"; outcome = "$($h.outcome)"; first = "$(@($h.data)[0])" }
    $tok = [guid]::NewGuid().ToString('N'); & $m { param($t) $script:PmSentinel = $t } $tok
    $w = [ordered]@{ action = $null; outcome = $null; error = $null; conflict = $false; loaded_after = 0; same_instance = $false; sentinel_intact = $false }
    try { $wo = @(& ([IO.Path]::Combine($scripts, 'Run-Px.ps1')) help); if ($wo.Count) { $w.action = "$($wo[0].action)"; $w.outcome = "$($wo[0].outcome)" } }
    catch { $w.error = "$($_.FullyQualifiedErrorId) | $($_.Exception.Message)"; $w.conflict = "$($_.FullyQualifiedErrorId)".StartsWith('ProximaControl.ModuleConflict', [StringComparison]::Ordinal) }
    $after = @(Get-Module -Name ProximaControl); $w.loaded_after = $after.Count
    $w.same_instance = $after.Count -eq 1 -and [object]::ReferenceEquals($after[0].PSObject.BaseObject, $m.PSObject.BaseObject)
    $w.sentinel_intact = $after.Count -eq 1 -and ((& $after[0] { Get-Variable -Name PmSentinel -Scope Script -ValueOnly -ErrorAction SilentlyContinue }) -ceq $tok)
    $r.wrapper = $w
} catch {
    $r.error = "$($_.FullyQualifiedErrorId) | $($_.Exception.Message)"; $x = $_.Exception
    while ($null -ne $x) { $r.messages += $x.Message; if ($x -is [Management.Automation.IContainsErrorRecord]) { $r.messages += "$($x.ErrorRecord.FullyQualifiedErrorId)" }; $x = $x.InnerException }
} finally {
    $r.sentinel_exists = [bool]$SentinelPath -and [IO.File]::Exists($SentinelPath); $r.loaded_after = @(Get-Module -Name ProximaControl, ProximaConfig | ForEach-Object { $_.Path })
    [IO.File]::WriteAllText($OutPath, ($r | ConvertTo-Json -Depth 5), [Text.UTF8Encoding]::new($false))
}
'@
function Invoke-Phase([string]$Role, [string[]]$More) {
    $s = [IO.Path]::Combine($Run, "$Role-child.ps1"); $o = [IO.Path]::Combine($Run, "$Role-child.out.json"); Save-Text "$Role-script" $s $ChildScript
    $c = Start-Child $Role (@('-NoProfile', '-NonInteractive', '-File', $s, '-Mode', $Role, '-OutPath', $o) + $More) 300
    if (-not [IO.File]::Exists($o)) { throw "$Role child wrote no output (rc=$($c.rc))" }; Add-Artifact "$Role-output" $o; return ([IO.File]::ReadAllText($o, $Utf8) | ConvertFrom-Json)
}
# ---- setup (any failure here is rc 2) ----
$Root = [IO.Path]::GetFullPath($AddonRoot).TrimEnd([char]'\', [char]'/'); $Scratch = [IO.Path]::GetFullPath($ScratchRoot); $ReportPath = [IO.Path]::GetFullPath($ReportPath)
if (-not [IO.Directory]::Exists($Root) -or -not [IO.Directory]::Exists($Scratch)) { throw 'AddonRoot and ScratchRoot must be existing directories' }
foreach ($rel in $Legacy) { if (-not [IO.File]::Exists((Join-Addon $Root $rel))) { throw "S1/S2 file missing: $rel (not a proxima-control add-on tree)" } }
$RepoTop = $null; $probe = [IO.Directory]::GetParent($Root)
while ($null -ne $probe -and $null -eq $RepoTop) { if ([IO.Directory]::Exists("$($probe.FullName)/.git") -or [IO.File]::Exists("$($probe.FullName)/.git")) { $RepoTop = $probe.FullName }; $probe = $probe.Parent }
foreach ($p in $Scratch, $ReportPath) { if ((Test-Inside $p $Root) -or ($RepoTop -and (Test-Inside $p $RepoTop))) { throw "evidence path inside the add-on or its repository: $p" } }
if (@(Get-Module -Name ProximaControl, ProximaConfig).Count) { throw 'a Proxima module is already loaded in this process; run the harness in a fresh process' }
$SelfExe = [Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$Run = [IO.Path]::Combine($Scratch, ('pm-{0}-{1}' -f [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ', $Inv), [guid]::NewGuid().ToString('N').Substring(0, 8)))
$null = [IO.Directory]::CreateDirectory($Run); $Report.evidence.dir = $Run
$Report.launch = [ordered]@{ exe = $SelfExe; command_line = [Environment]::CommandLine; execution_policy_preference = $env:PSExecutionPolicyPreference; repository = $RepoTop }
$Before = Get-Snapshot $Root; $Report.source_hashes = $Before
$ManifestPath = Join-Addon $Root 'scripts/ProximaControl.psd1'; $SkillPath = Join-Addon $Root 'SKILL.md'; $ManifestPresent = [IO.File]::Exists($ManifestPath)
$SkillPresent = [IO.File]::Exists($SkillPath); $Doc = $null; $DocCommands = @(); $ManifestAst = $null; $ManifestData = $null; $SchemaOk = $false
$Report.manifest_state = $(if ($ManifestPresent) { 'present' } else { 'MANIFEST_ABSENT' }); $Report.skill_state = $(if ($SkillPresent) { 'present' } else { 'SKILL_ABSENT' })
if ($SkillPresent) { $Doc = Read-Skill $SkillPath; $DocCommands = @(Get-DocCommands) }
# ---- PM01/PM02: static manifest judgement, BEFORE any import ----
Invoke-Case 'PM01' {
    if (-not $ManifestPresent) { Stop-Case 'MANIFEST_ABSENT: scripts/ProximaControl.psd1' }
    $tk = $null; $er = $null; $ast = [Parser]::ParseFile($ManifestPath, [ref]$tk, [ref]$er); if (@($er).Count) { Stop-Case "PARSE_ERROR: $(@($er)[0].Message)" }
    if (@($tk | Where-Object { $_.Kind -eq [TokenKind]::Comment -and $_.Text -imatch '^#\s*requires' }).Count -or $ast.ParamBlock -or $ast.BeginBlock -or
        $ast.ProcessBlock -or $ast.DynamicParamBlock -or $ast.UsingStatements -or ($ast.EndBlock -and $ast.EndBlock.Traps)) { Stop-Case 'EXECUTABLE_STATEMENT: requires/param/block/using/trap' }
    $st = @(if ($ast.EndBlock) { $ast.EndBlock.Statements })
    $ce = $(if ($st.Count -eq 1 -and $st[0] -is [PipelineAst] -and @($st[0].PipelineElements).Count -eq 1) { $st[0].PipelineElements[0] })
    if ($ce -isnot [CommandExpressionAst] -or @($ce.Redirections).Count -or $ce.Expression -isnot [HashtableAst]) { Stop-Case "NOT_SINGLE_HASHTABLE: $($st.Count) top-level statement(s)" }
    try { $data = $ce.Expression.SafeGetValue() } catch { Stop-Case "UNSAFE_VALUE: $($_.Exception.Message)" }
    $script:ManifestAst = $ce.Expression; $script:ManifestData = $data
    'exactly one hashtable data expression, no executable statement, SafeGetValue accepted'
}
Invoke-Case 'PM02' {
    if (-not $ManifestPresent) { Stop-Case 'MANIFEST_ABSENT: scripts/ProximaControl.psd1' } elseif ($null -eq $ManifestAst) { Stop-Case 'NOT_EVALUATED: PM01 rejected the manifest' }
    $bad = [Collections.Generic.List[string]]::new(); $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($kv in $ManifestAst.KeyValuePairs) {
        $name = $(if ($kv.Item1 -is [StringConstantExpressionAst]) { $kv.Item1.Value } else { $kv.Item1.Extent.Text })
        if (-not $KeySet.Contains($name)) { $bad.Add("UNEXPECTED_KEY[$name]") } elseif (-not $seen.Add($name)) { $bad.Add("DUPLICATE_KEY[$name]") }
    }
    foreach ($k in $KeySet) { if (-not $seen.Contains($k)) { $bad.Add("MISSING_KEY[$k]") } }
    foreach ($k in $Want.Keys) { if ($ManifestData[$k] -isnot [string] -or -not [string]::Equals($ManifestData[$k], $Want[$k], [StringComparison]::Ordinal)) { $bad.Add("VALUE[$k]") } }
    foreach ($k in $WantArrays.Keys) {
        $v = $ManifestData[$k]; $w = @($WantArrays[$k])
        if ($v -isnot [object[]]) { $bad.Add("TYPE[$k]"); continue }
        # Wildcards are invalid even though the unchanged S2 Export-ModuleMember would hide them at runtime (actual exports cannot see this).
        if (@($v | Where-Object { "$_".IndexOfAny([char[]]'*?[') -ge 0 }).Count) { $bad.Add("WILDCARD_EXPORT[$k]") }
        $same = $v.Count -eq $w.Count; for ($i = 0; $same -and $i -lt $w.Count; $i++) { $same = $v[$i] -is [string] -and [string]::Equals($v[$i], $w[$i], [StringComparison]::Ordinal) }
        if (-not $same) { $bad.Add("VALUE[$k]") }
    }
    if ($bad.Count) { Stop-Case ($bad -join '; ') }
    $script:SchemaOk = $true; 'nine allowed keys exactly; RootModule/ModuleVersion/GUID/PS metadata and Ordinal export arrays as specified; no wildcard'
}
# ---- fresh children, only after the static gate ----
$RtOut = $null; $TaOut = $null; $RtSetup = $null; $TaSetup = $null; $Tamper = $null
if ($SchemaOk) {
    try { $RtOut = Invoke-Phase 'runtime' @('-ManifestPath', $ManifestPath) } catch { $RtSetup = "$($_.Exception.Message)" }
    try {
        $td = [IO.Path]::Combine($Run, 'pm04-private-copy'); $ts = [IO.Path]::Combine($td, 'scripts'); $null = [IO.Directory]::CreateDirectory($ts)
        foreach ($f in 'ProximaControl.psd1', 'ProximaControl.psm1', 'ProximaConfig.psm1') { [IO.File]::Copy((Join-Addon $Root "scripts/$f"), [IO.Path]::Combine($ts, $f)) }
        $cfg = [IO.Path]::Combine($ts, 'ProximaConfig.psm1')
        $edit = "[IO.File]::WriteAllText([IO.Path]::Combine(`$PSScriptRoot, '..', 'sentinel-executed.txt'), 'PM04 sentinel: tampered ProximaConfig.psm1 ran')`r`n"
        [IO.File]::WriteAllBytes($cfg, [byte[]]($Utf8.GetBytes($edit) + [IO.File]::ReadAllBytes($cfg)))
        foreach ($f in 'ProximaControl.psd1', 'ProximaControl.psm1', 'ProximaConfig.psm1') { Add-Artifact "pm04-copy-$f" ([IO.Path]::Combine($ts, $f)) }
        $Tamper = [ordered]@{ edit = "prepended: $($edit.Trim())"; path = $cfg; sha256 = (Get-FileSha $cfg); sentinel = [IO.Path]::Combine($td, 'sentinel-executed.txt') }
        $Report.tamper = $Tamper; $TaOut = Invoke-Phase 'tamper' @('-ManifestPath', [IO.Path]::Combine($ts, 'ProximaControl.psd1'), '-SentinelPath', $Tamper.sentinel)
    } catch { $TaSetup = "$($_.Exception.Message)" }
}
function Assert-Gate([string]$Setup, $Out) {
    if (-not $ManifestPresent) { Stop-Case 'MANIFEST_ABSENT: scripts/ProximaControl.psd1' } elseif (-not $SchemaOk) { Stop-Case 'NOT_EXECUTED: manifest rejected by PM01/PM02 before any import' }
    if ($Setup) { throw "runtime child unavailable: $Setup" }
    if ("$($Out.error)" -cmatch 'UnauthorizedAccess|PSSecurityException') { throw "runtime denied by execution policy (not a property result): $($Out.error)" }
}
Invoke-Case 'PM03' {
    Assert-Gate $RtSetup $RtOut; $o = $RtOut; $bad = [Collections.Generic.List[string]]::new()
    if ($null -eq $o.test_manifest -or $null -eq $o.module) { Stop-Case "TEST_MODULE_MANIFEST_OR_IMPORT_FAILED: $($o.error)" }
    if (@($o.preloaded).Count) { $bad.Add('NOT_FRESH_PROCESS') }
    foreach ($x in $o.test_manifest, $o.module) { if ($x.version -cne $Want.ModuleVersion -or $x.guid -cne $Want.GUID) { $bad.Add("IDENTITY[$($x.version) $($x.guid)]") } }
    $cmds = @($o.module.commands)
    if ($cmds.Count -ne 2 -or $cmds -cnotcontains 'px' -or $cmds -cnotcontains 'Invoke-ProximaOperation' -or $o.module.functions -ne 2 -or $o.module.others) { $bad.Add("EXPORTS[$($cmds -join ',')]") }
    if ($o.module.loaded -ne 1) { $bad.Add("LOADED_INSTANCES[$($o.module.loaded)]") }
    if ($null -eq $o.help -or "$($o.help.schema)|$($o.help.action)|$($o.help.outcome)|$($o.help.first)" -cne 'px.result.v1|help|ok|px help') { $bad.Add('HELP_NEGATIVE') }
    if ($bad.Count) { Stop-Case ($bad -join '; ') }
    "fresh $($o.ps_edition) $($o.ps_version) [$($o.culture)]: Test-ModuleManifest + import ok, path=$($o.module.path) (root psm1: $($o.module.path_is_root_module)), 2 exports, px help ok"
}
Invoke-Case 'PM04' {
    Assert-Gate $TaSetup $TaOut; $o = $TaOut; $bad = [Collections.Generic.List[string]]::new(); $text = (@($o.error) + @($o.messages)) -join ' | '
    if (@($o.preloaded).Count) { $bad.Add('NOT_FRESH_PROCESS') }; if ($o.imported) { $bad.Add('TAMPERED_DEPENDENCY_IMPORTED') }
    if ($text.IndexOf('DependencyMismatch', [StringComparison]::Ordinal) -lt 0) { $bad.Add("NOT_NAMED_DependencyMismatch[$text]") }
    if ($o.sentinel_exists -or [IO.File]::Exists($Tamper.sentinel)) { $bad.Add('SENTINEL_EXECUTED') }
    if (@($o.loaded_after).Count) { $bad.Add("MODULE_LEFT_LOADED[$(@($o.loaded_after) -join ',')]") }
    if ((Get-FileSha $Tamper.path) -cne $Tamper.sha256 -or (Get-FileSha (Join-Addon $Root 'scripts/ProximaConfig.psm1')) -cne $Before['scripts/ProximaConfig.psm1']) { $bad.Add('FIXTURE_OR_ORIGINAL_S1_CHANGED') }
    if ($bad.Count) { Stop-Case ($bad -join '; ') }
    "DependencyMismatch before the sentinel line ran ($($o.ps_edition) $($o.ps_version)); private copy and original S1 intact"
}
Invoke-Case 'PM05' {
    if (-not $SkillPresent) { Stop-Case 'SKILL_ABSENT: SKILL.md' }; $bad = [Collections.Generic.List[string]]::new(); $fm = $(if ($null -ne $Doc.fm) { $Doc.fm } else { @{} })
    $mv = $(if ($null -ne $ManifestData -and $ManifestData['ModuleVersion'] -is [string]) { $ManifestData['ModuleVersion'] } else { 'MANIFEST_VERSION_UNAVAILABLE' })
    if ($Doc.decode -cne 'ok' -or $null -eq $Doc.fm) { $bad.Add("FRONTMATTER_MISSING[$($Doc.decode)]") }
    if ("$($fm['name'])" -cne 'proxima-control' -or "$($fm['description'])".Length -lt 20) { $bad.Add('NAME_OR_DESCRIPTION') }
    if ("$($fm['version'])" -cne $mv) { $bad.Add("DOC_VERSION_MISMATCH[frontmatter=$($fm['version']) manifest=$mv]") }
    foreach ($t in $Tags) {
        $s = @($Doc.sections | Where-Object { $_.tag -ceq $t })
        if ($s.Count -ne 1) { $bad.Add("HEADING[$t x$($s.Count)]") } elseif (-not ($s[0].body -join '').Trim()) { $bad.Add("SECTION_EMPTY[$t]") }
    }
    $ver = Get-Section 'Versions'
    foreach ($tok in $mv, 'moduleSha256', 'configModuleSha256', 'FileVersion', 'NOT_MEASURED') { if ($ver.IndexOf($tok, [StringComparison]::Ordinal) -lt 0) { $bad.Add("VERSION_DOMAIN_MISSING[$tok]") } }
    foreach ($m in [regex]::Matches($Doc.text, '(?<![\d.])\d+\.\d+\.\d+(?![\d.])')) { if ($m.Value -cne $mv -and $m.Value -cne '1.0.1') { $bad.Add("DOC_VERSION_MISMATCH[stray $($m.Value)]") } }
    $ph = @{ ConfigPath = '<ConfigPath>'; RepositoryRoot = '<RepoRoot>'; TargetId = '<TargetId>' }; $targeted = 0
    foreach ($c in $DocCommands) {
        foreach ($k in $ph.Keys) { if ($c.params.Contains($k) -and "$($c.params[$k])" -cne $ph[$k]) { $bad.Add("PLACEHOLDER[$k=$($c.params[$k])]") } }
        if ($c.params.Contains('TargetId')) { $targeted++ }
    }
    if ($targeted -lt 3) { $bad.Add("TARGET_EXAMPLES[$targeted]") }; if ($bad.Count) { Stop-Case ($bad -join '; ') }
    "name/description; version $mv in frontmatter and Versions (both directions); six headings; three version domains; $targeted placeholder targets"
}
Invoke-Case 'PM06' {
    Assert-Gate $RtSetup $RtOut; $w = $RtOut.wrapper
    if ($null -eq $w) { Stop-Case "NOT_EXECUTED: manifest import failed before the wrapper ran: $($RtOut.error)" }
    $state = "loaded_after=$($w.loaded_after) same_instance=$($w.same_instance) sentinel_intact=$($w.sentinel_intact)"; $kept = $w.loaded_after -eq 1 -and $w.same_instance -and $w.sentinel_intact
    if ($w.conflict) { if (-not $kept) { Stop-Case "CONFLICT_WITH_RESET[$state]" }; return "ModuleConflict fail-closed; prior instance and sentinel untouched ($state)" }
    if ($w.error) { Stop-Case "WRAPPER_ERROR[$($w.error)]" } elseif ("$($w.action)/$($w.outcome)" -cne 'help/ok') { Stop-Case "WRAPPER_HELP_NEGATIVE[$($w.action)/$($w.outcome)]" }
    if (-not $kept) { Stop-Case "SILENT_RESET_OR_REIMPORT[$state]" }
    "Run-Px help reused the manifest-imported instance; test-owned sentinel intact ($state)"
}
# ---- counterexamples: single-anchor semantic mutants of COPIES, each rerunning this harness in a fresh child ----
$CxCases = @(@{ id = 'CX00'; file = ''; anchor = ''; replacement = ''; want = ''; before_import = $false },
    @{ id = 'CX01'; file = 'scripts/ProximaControl.psd1'; anchor = '    AliasesToExport'; want = 'PM02:UNEXPECTED_KEY[ScriptsToProcess]'; before_import = $true
        replacement = "    ScriptsToProcess     = @('cx01-never-run.ps1')`r`n    AliasesToExport" },
    @{ id = 'CX02'; file = 'scripts/ProximaControl.psd1'; anchor = "@('px', 'Invoke-ProximaOperation')"; replacement = "@('*')"; want = 'PM02:WILDCARD_EXPORT[FunctionsToExport]'; before_import = $true },
    @{ id = 'CX03'; file = 'scripts/ProximaControl.psd1'; anchor = '    AliasesToExport'; want = 'PM02:UNEXPECTED_KEY[NestedModules]'; before_import = $true
        replacement = "    NestedModules        = @('ProximaConfig.psm1')`r`n    AliasesToExport" },
    @{ id = 'CX04'; file = 'SKILL.md'; anchor = 'version: 2.0.0'; replacement = 'version: 2.0.1'; want = 'PM05:DOC_VERSION_MISMATCH[frontmatter'; before_import = $false })
# Credit only for child rc 1 with the named reason in the named case; CX01..CX03 also need ZERO runtime children (rejected before import).
function Test-CxKill($Cx, $Rc, $Rep, $Rec) {
    $state = "rc=$Rc passed=$($Rep.passed)/$($Rep.total) setup_error=$($Rep.setup_error) evidence=$($Rep.evidence.check.status) runtime_children=$($Rep.runtime_children)"
    if ($Rep.setup_error -or @($Rep.setup_error_ids).Count -or "$($Rep.evidence.check.status)" -cne 'ok') { throw "child did not measure cleanly, no credit ($state)" }
    if ($Cx.id -ceq 'CX00') { if ($Rc -ne 0 -or $Rep.passed -ne $Ids.Count -or $Rep.total -ne $Ids.Count) { Stop-Case "CONTROL_FAILED ($state)" }; return "CONTROL_PASSED: 7/7 rc 0 ($state)" }
    if ($Rc -eq 0) { Stop-Case "SURVIVED: mutant passed every case, no credit ($state)" } elseif ($Rc -ne 1) { throw "wrong child rc, no credit ($state)" }
    $cid, $tok = $Cx.want -split ':', 2; $hit = @($Rep.cases | Where-Object { $_.id -ceq $cid -and $_.outcome -ceq 'failed' -and "$($_.reason)".Contains($tok) })
    if (-not $hit.Count) { Stop-Case "NAMED_REASON_MISSING[$($Cx.want)] ($state)" }
    $Rec.matched = "$($cid): $($hit[0].reason)"; $pm04 = "$(@($Rep.cases | Where-Object { $_.id -ceq 'PM04' } | ForEach-Object { $_.reason }))"
    if ($Cx.before_import -and ($Rep.runtime_children -ne 0 -or -not $pm04.StartsWith('NOT_EXECUTED', [StringComparison]::Ordinal))) { Stop-Case "IMPORTED_BEFORE_REJECTION ($state)" }
    $Rec.credited = $true; "KILLED: named reason in the named case$(if ($Cx.before_import) { ' with zero imports (PM04 not executed)' }) ($state)"
}
if ($Counterexamples) {
    foreach ($cx in $CxCases) {
        Invoke-Case $cx.id {
            if (-not ($ManifestPresent -and $SkillPresent)) { Stop-Case 'CANDIDATE_ABSENT: counterexamples need the manifest and SKILL.md' }
            $dir = [IO.Path]::Combine($Run, $cx.id); $src = [IO.Path]::Combine($dir, 'addon'); $rep = [IO.Path]::Combine($dir, 'report.json')
            $rec = [ordered]@{ id = $cx.id; mutated_file = $cx.file; anchor = $cx.anchor; replacement = $cx.replacement; source_dir = $src; sha256_before = $null
                sha256_after = $null; command = $null; rc = $null; report_path = $rep; want = $cx.want; matched = $null; credited = $false; verdict = $null }
            $Report.counterexamples.Add($rec)
            try {
                foreach ($rel in $Before.Keys) {
                    if ($Before[$rel] -ceq 'reparse') { throw "reparse point in add-on tree: $rel" }
                    $to = Join-Addon $src $rel; $null = [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($to)); [IO.File]::Copy((Join-Addon $Root $rel), $to)
                }
                if ($cx.file) {
                    $p = Join-Addon $src $cx.file; $t = [IO.File]::ReadAllText($p, $Utf8); $rec.sha256_before = Get-FileSha $p; $at = $t.IndexOf($cx.anchor, [StringComparison]::Ordinal)
                    if ($at -lt 0 -or $t.IndexOf($cx.anchor, $at + 1, [StringComparison]::Ordinal) -ge 0) { throw "mutation anchor absent or not unique: $($cx.anchor)" }
                    [IO.File]::WriteAllText($p, $t.Substring(0, $at) + $cx.replacement + $t.Substring($at + $cx.anchor.Length), $Utf8)
                    $rec.sha256_after = Get-FileSha $p; Add-Artifact "$($cx.id)-mutated-source" $p
                }
                $ch = Start-Child $cx.id @('-NoProfile', '-NonInteractive', '-File', $PSCommandPath, '-AddonRoot', $src, '-ScratchRoot', $dir, '-ReportPath', $rep) 1200
                $rec.command = "$SelfExe $($ch.arguments)"; $rec.rc = $ch.rc; if (-not [IO.File]::Exists($rep)) { throw "child report absent (rc=$($ch.rc))" }
                Add-Artifact "$($cx.id)-report" $rep; $rec.verdict = Test-CxKill $cx $ch.rc ([IO.File]::ReadAllText($rep, $Utf8) | ConvertFrom-Json) $rec; $rec.verdict
            } catch { $rec.verdict = "NOT_CREDITED: $($_.Exception.Message)"; throw }
            finally { Save-Text "$($cx.id)-record" ([IO.Path]::Combine($dir, 'record.json')) ($rec | ConvertTo-Json -Depth 5) }
        }
    }
}
# ---- PM07 (last): optional publication, examples, file references, and add-on bytes unchanged by this whole run ----
Invoke-Case 'PM07' {
    $bad = [Collections.Generic.List[string]]::new()
    if (-not $SkillPresent) { $bad.Add('SKILL_ABSENT: SKILL.md') }
    else {
        foreach ($tok in '_RELEASE_EXCLUDE_DIRS', 'Package') { if ((Get-Section 'Scope').IndexOf($tok, [StringComparison]::Ordinal) -lt 0) { $bad.Add("ISOLATION_STATEMENT_MISSING[$tok]") } }
        $deny = [ordered]@{ 'guid-or-device-id' = '[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}'; 'user-profile-path' = '[a-z]:\\users\\'; 'secret' = 'convertto-securestring'
            'real-host-url' = 'https?://(?![^/\s]*\.invalid(?:[/:\s]|$))'; 'policy-override' = 'executionpolicy\s+(bypass|unrestricted)|set-executionpolicy' }
        foreach ($k in $deny.Keys) { if ([regex]::IsMatch($Doc.text, $deny[$k], 'IgnoreCase, CultureInvariant')) { $bad.Add("FORBIDDEN_CLAIM[$k]") } }
        $imports = 0; $wrappers = 0
        foreach ($c in $DocCommands) {
            if ($c.errors) { $bad.Add("EXAMPLE_PARSE[$($c.line)]"); continue }
            if ($c.name -ceq 'Import-Module') {
                $imports++; if (-not "$($c.params['Name'])".EndsWith('\scripts\ProximaControl.psd1', [StringComparison]::Ordinal) -or $c.params.Contains('Force')) { $bad.Add("IMPORT_EXAMPLE[$($c.line)]") }
                continue
            }
            if ($c.name.EndsWith('\scripts\Run-Px.ps1', [StringComparison]::Ordinal)) { $wrappers++ } elseif ($c.name -cne 'px') { continue }
            if (-not $PxActions.Contains($c.action)) { $bad.Add("EXAMPLE_ACTION[$($c.line)]"); continue }
            if ($c.action -cne 'help') { foreach ($k in 'ConfigPath', 'RepositoryRoot', 'TargetId') { if (-not $c.params.Contains($k)) { $bad.Add("EXAMPLE_TARGET_MISSING[$k $($c.line)]") } } }
            if ($c.params.Contains('Credential') -and $c.action -cne 'connect') { $bad.Add("CREDENTIAL_OUTSIDE_CONNECT[$($c.line)]") }
        }
        if (-not $imports -or -not $wrappers) { $bad.Add("ENTRY_EXAMPLE_MISSING[import=$imports wrapper=$wrappers]") }
        $refs = @([regex]::Matches($Doc.text, '`((?:scripts|tests)/[A-Za-z0-9._-]+|config\.example\.json)`') | ForEach-Object { $_.Groups[1].Value })
        foreach ($r in $refs) { if (-not [IO.File]::Exists((Join-Addon $Root $r))) { $bad.Add("BROKEN_REF[$r]") } }
        foreach ($r in 'scripts/ProximaControl.psd1', 'scripts/Run-Px.ps1', 'tests/ProximaManifest.Tests.ps1') { if ($refs -cnotcontains $r) { $bad.Add("REF_MISSING[$r]") } }
    }
    $after = Get-Snapshot $Root; $v = $null
    foreach ($k in $Before.Keys) { if (-not $after.TryGetValue($k, [ref]$v) -or $v -cne $Before[$k]) { $bad.Add($(if ($Legacy -ccontains $k) { "S1S2_CHANGED[$k]" } else { "SOURCE_CHANGED_BY_RUN[$k]" })) } }
    foreach ($k in $after.Keys) { if (-not $Before.ContainsKey($k)) { $bad.Add("SOURCE_ADDED_BY_RUN[$k]") } }
    if ($bad.Count) { Stop-Case ($bad -join '; ') }
    "optional/excluded publication stated; $(@($DocCommands).Count) example lines valid; file refs resolve; $($Before.Count) add-on files byte-identical before/after"
}
$required = @($Ids) + @($(if ($Counterexamples) { $CxCases | ForEach-Object { $_.id } })); $Report.required_ids = $required
$missing = @($required | Where-Object { $want1 = $_; @($Results | Where-Object { $_.id -ceq $want1 }).Count -ne 1 })
if ($missing.Count) { throw "IDs not executed exactly once: $($missing -join ',')" }
Complete-Run $(if (@($Results | Where-Object { $_.outcome -ceq 'setup_error' }).Count) { 2 } elseif (@($Results | Where-Object { $_.outcome -cne 'passed' }).Count) { 1 } else { 0 })
