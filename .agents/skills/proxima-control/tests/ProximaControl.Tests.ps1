# ProximaControl.Tests.ps1 - wp1279 r2 (PROXIMA-P1-S2) focused harness for ProximaControl.psm1 + Run-Px.ps1; self-contained, no Pester.
# The SAME harness and ID set run against any tree (baseline B without S2, candidate H) through an explicit -ModulePath:
#   powershell.exe|pwsh.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File <copy>\ProximaControl.Tests.ps1 `
#     -ModulePath <tree>\.agents\skills\proxima-control\scripts\ProximaControl.psm1 -ScratchRoot <existing dir outside the tree> `
#     -ReportPath <json outside the tree> [-Counterexamples [-EvidenceRoot <durable dir outside the tree>]] [-TestCulture en-US|tr-TR]
# rc 0: all 25 mandatory IDs (with -Counterexamples also CX00-CX10) passed and cleanup was verified. rc 1: a case failed - an absent
# module fails EVERY case with API_ABSENT while every case still executes. rc 2: setup or cleanup error, never a test outcome.
# Safety: every hazardous backend binding (session, remote invoke, HTTP, CIM process/service, service control, id) is replaced in
# the module's private table BEFORE any product call, and the replacement is asserted. HTTP is re-bound to the real default only
# in wire cases and only towards an owned 127.0.0.1 TcpListener; dummy credentials only; no real gateway, service or WinRM.
# Children (all receive -TestCulture; parent and child cultures are recorded): the constant endpoint body + CLIXML request run out
# of process (this exe, plus the other PowerShell edition when installed) with ambient WhatIf false; Run-Px.ps1 runs in a fresh
# process. -Counterexamples: CX00 unmodified control + CX01-CX10 single-anchor mutants of COPIES in <EvidenceRoot>\pxctl-evid-<run>,
# each rerunning this harness; credit only for rc 1 with the named behavioural token in the named case (setup/import/wrong-rc
# earn nothing; a surviving mutant is reported, never credited). Evidence is never deleted. Helpers are alias-free and no
# automatic variable (args, PID, HOME, PROFILE) is assigned; setup refuses any inner binding that reuses a top-level name
# (Find-ScopeShadowing: PowerShell resolves helper names through the caller's scopes, case-insensitively). 'All streams' = output/error/warning/verbose/debug/information plus
# the terminating error record; $global:Error history (which keeps the fakes' own raw backend exceptions) is not a product stream.
[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$ModulePath, [Parameter(Mandatory = $true)][string]$ScratchRoot, [string]$ReportPath = '',
    [string]$EvidenceRoot = '', [switch]$Counterexamples, [ValidateSet('en-US', 'tr-TR', IgnoreCase = $false)][string]$TestCulture = 'en-US')
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$Ids = 'X1-01', 'X1-02', 'X1-03', 'X2-01', 'X2-02', 'X2-03', 'X2-04', 'X2-05', 'X2-06', 'X2-07', 'X3-01', 'X3-02', 'X4-01', 'X4-02', 'X4-03',
'X5-01', 'X5-02', 'X5-03', 'X5-04', 'X5-05', 'X5-06', 'X5-07', 'X5-08', 'X6-01', 'X6-02'
$PrimKeys = 'GetProcess', 'GetService', 'Http', 'InvokeRemote', 'NewId', 'NewSession', 'RemoveSession', 'ServiceControl', 'UiSessions'
$Results = [Collections.Generic.List[object]]::new()
$Cleanup = [ordered]@{ status = 'not_run'; errors = [Collections.Generic.List[string]]::new(); tree_removed = $false; keep_sentinel_intact = $null; wire_servers_stopped = $null }
$Report = [ordered]@{ schema = 'proxima_control_tests.v1'; ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"
    test_culture_requested = $TestCulture; test_culture = $null; test_ui_culture = $null; test_culture_probe = $null; module_path = $ModulePath
    module_sha256 = $null; wrapper_sha256 = $null; config_module_sha256 = $null; harness_sha256 = $null; git_head = 'not_measured'; git_tree = 'not_measured'
    api_state = 'unknown'; alias_r = $null; setup_error = $null; mandatory_ids = $Ids; required_ids = @(); counterexample_ids = @(); primitive_keys = $PrimKeys
    primitives_replaced = $null; child_exes = @(); scratch = $null; evidence_dir = $null; total = 0; passed = 0; failed = 0; failed_ids = @(); setup_error_ids = @()
    cases = $Results; children = [Collections.Generic.List[object]]::new(); counterexample_evidence = [Collections.Generic.List[object]]::new(); cleanup = $Cleanup }
$Utf8 = [Text.UTF8Encoding]::new($false); $Sha = [Security.Cryptography.SHA256]::Create(); $Inv = [Globalization.CultureInfo]::InvariantCulture
$S = $null; $FullScratch = $null; $Keep = $null; $KeepSha = $null; $Evid = $null; $Completing = $false; $ApiPresent = $false
$Mod = $null; $PxCmd = $null; $OpCmd = $null; $OrigPrim = $null; $EpRun = $null; $Wires = [Collections.Generic.List[object]]::new()
function Get-FileSha256([string]$P) { if ($P -and [IO.File]::Exists($P)) { ([BitConverter]::ToString($Sha.ComputeHash([IO.File]::ReadAllBytes($P))) -replace '-', '').ToLowerInvariant() } }
function Get-TextSha256([string]$T) { ([BitConverter]::ToString($Sha.ComputeHash($Utf8.GetBytes($T))) -replace '-', '').ToLowerInvariant() }
function Invoke-Native([string]$Exe, [string[]]$ArgList) {
    $ErrorActionPreference = 'Continue'; $out = & $Exe @ArgList 2>&1 | Out-String
    return [pscustomobject]@{ rc = $LASTEXITCODE; out = $out }
}
# Bottom-up delete that never follows a reparse point (junctions are removed as links); errors are collected, never ignored.
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
# Listing that records reparse points as such and never enters them; -Hash = file bytes, else length + write time.
function Get-TreeSnapshot([string]$Root, [switch]$Hash) {
    if (-not [IO.Directory]::Exists($Root)) { return 'absent' }
    $rows = [Collections.Generic.List[string]]::new(); $todo = [Collections.Generic.Stack[string]]::new(); $todo.Push($Root)
    while ($todo.Count) {
        foreach ($p in [IO.Directory]::GetFileSystemEntries($todo.Pop())) {
            $a = [int][IO.File]::GetAttributes($p)
            if ($a -band 0x400) { $rows.Add("$p|reparse") } elseif ($a -band 0x10) { $rows.Add("$p|dir"); $todo.Push($p) }
            elseif ($Hash) { $rows.Add("$p|$(Get-FileSha256 $p)") } else { $f = [IO.FileInfo]::new($p); $rows.Add("$p|$($f.Length)|$($f.LastWriteTimeUtc.Ticks)") }
        }
    }
    $rows.Sort([StringComparer]::Ordinal); return ($rows -join "`n")
}
function Get-EnvSnapshot { (@([Environment]::GetEnvironmentVariables().GetEnumerator() | ForEach-Object { "$($_.Name)=$($_.Value)" } | Sort-Object)) -join "`n" }
function Get-UserStateSnapshot {
    $rows = foreach ($n in 'AllUsersAllHosts', 'AllUsersCurrentHost', 'CurrentUserAllHosts', 'CurrentUserCurrentHost') { $f = [string]$PROFILE.$n; "$n=$(Get-FileSha256 $f)" }
    return ((@($rows) + @("cwd=$([Environment]::CurrentDirectory)", (Get-EnvSnapshot))) -join "`n")
}
function Get-OutcomeIds([string]$Outcome) { @($Results | Where-Object { $_.outcome -eq $Outcome } | ForEach-Object { $_.id }) }
function Stop-WireServer($W) {
    if ($W['Stopped']) { return }
    try { $W.Listener.Stop() } catch { $null = $_ }
    try { $null = $W.Ps.EndInvoke($W.Async) } catch { $null = $_ }
    $W.Ps.Dispose(); $W['Stopped'] = $true
}
function Complete-Run([int]$Rc) {
    if ($script:Completing) { exit 2 }
    $script:Completing = $true; $c = $Cleanup
    try { foreach ($w in $Wires) { Stop-WireServer $w }; $c.wire_servers_stopped = $true } catch { $c.errors.Add("wire server stop: $($_.Exception.Message)") }
    try {
        if ($FullScratch) { Set-Location -LiteralPath $FullScratch; [Environment]::CurrentDirectory = $FullScratch }
        if ($S -and [IO.Directory]::Exists($S)) {
            if ($Rc -eq 0 -and -not $c.errors.Count) { Remove-OwnedTree $S $c.errors; $c.tree_removed = -not [IO.Directory]::Exists($S) }
            else { Write-Host "scratch kept for evidence: $S" }
        }
        if ($Keep) {
            $c.keep_sentinel_intact = (Get-FileSha256 "$Keep\keep.txt") -ceq $KeepSha
            if (-not $c.keep_sentinel_intact) { $c.errors.Add("outside sentinel $Keep\keep.txt changed or missing") }
            elseif ($c.tree_removed) { Remove-OwnedTree $Keep $c.errors }
        }
    } catch { $c.errors.Add("$($_.Exception.Message)") }
    $c.status = $(if ($c.errors.Count) { 'failed' } else { 'ok' }); if ($c.errors.Count) { $Rc = 2 }
    $Report.failed_ids = @(Get-OutcomeIds 'failed'); $Report.setup_error_ids = @(Get-OutcomeIds 'setup_error')
    $Report.passed = @(Get-OutcomeIds 'passed').Count; $Report.failed = $Report.failed_ids.Count; $Report.total = $Results.Count
    $Report.harness_sha256 = Get-FileSha256 $PSCommandPath; $Report.module_sha256 = Get-FileSha256 $ModulePath
    if ($ReportPath) { try { [IO.File]::WriteAllText($ReportPath, ($Report | ConvertTo-Json -Depth 10), $Utf8) } catch { Write-Host "REPORT_WRITE_ERROR $($_.Exception.Message)"; $Rc = 2 } }
    Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; setup_error_ids=[{3}]; api_state={4}; setup_error={5}; cleanup={6} [{7}]; rc={8}' -f $Report.passed,
        $Report.total, ($Report.failed_ids -join ','), ($Report.setup_error_ids -join ','), $Report.api_state, $Report.setup_error, $c.status, ($c.errors -join ' || '), $Rc)
    exit $Rc
}
trap { $Report.setup_error = "$($_.Exception.Message)"; Write-Host "SETUP_ERROR $($Report.setup_error)"; Complete-Run 2 }
function Set-TestLocation([string]$P) { Set-Location -LiteralPath $P; [Environment]::CurrentDirectory = $P }
function Write-Fixture([string]$Path, $Content) {
    $null = [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Path))
    if ($Content -is [byte[]]) { [IO.File]::WriteAllBytes($Path, $Content) } else { [IO.File]::WriteAllText($Path, [string]$Content, $Utf8) }
    return $Path
}
# JSON string from [char]92 escapes, so no tool or transport layer can decode them while this file is edited.
function ConvertTo-JsonText([string]$Text) {
    $bs = [string][char]92; $sb = [Text.StringBuilder]::new(); $null = $sb.Append('"')
    foreach ($ch in $Text.ToCharArray()) {
        $i = [int]$ch
        if ($i -eq 34 -or $i -eq 92) { $null = $sb.Append($bs).Append($ch) } elseif ($i -lt 32) { $null = $sb.Append($bs + 'u' + $i.ToString('x4', $Inv)) } else { $null = $sb.Append($ch) }
    }
    $null = $sb.Append('"'); return $sb.ToString()
}
# Fixture target: an S1 config file OUTSIDE the fake repository, plus its gateway base (profile\rest-port.json, owned pid).
function New-Target([string]$Name, [string]$Tid, [string]$Base, [int]$ProcId = 0, [string]$Uri = '', [string]$Endpoint = '') {
    $j = '{"schemaVersion":1,"targetId":' + (ConvertTo-JsonText $Tid) + ',"mode":' + $(if ($Uri) { '"Remote"' } else { '"Local"' }) + ',"basePath":' + (ConvertTo-JsonText $Base)
    if ($Uri) { $j += ',"connectionUri":' + (ConvertTo-JsonText $Uri) + ',"configurationName":' + (ConvertTo-JsonText $Endpoint) }
    $cfg = Write-Fixture "$S\cfg\$Name.json" ($j + '}')
    if ($ProcId) { $null = [IO.Directory]::CreateDirectory("$Base\runtime"); Set-RestPort $Base $ProcId 1; $global:PxcT.Pids["$ProcId"] = "$Base\runtime\Proxima.exe" }
    return @{ Name = $Name; Cfg = $cfg; Tid = $Tid; Base = $Base; ProcId = $ProcId; Fp = $null }
}
function Set-RestPort([string]$Base, [int]$ProcId, [int]$Port) { $null = Write-Fixture "$Base\profile\rest-port.json" ('{"pid":' + $ProcId + ',"port":' + $Port + '}') }
function New-Cred([string]$Password) { $sec = [Security.SecureString]::new(); foreach ($ch in $Password.ToCharArray()) { $sec.AppendChar($ch) }; return [pscredential]::new('pxdummy', $sec) }
function New-PxArgs([string]$Action, $Tgt, [hashtable]$More = @{}) {
    $h = @{ Action = $Action; ConfigPath = $Tgt.Cfg; RepositoryRoot = $Repo; TargetId = $Tgt.Tid }
    foreach ($k in $More.Keys) { $h[$k] = $More[$k] }
    return $h
}
# ---- fakes: recorded in $global:PxcT (harness-owned), installed into the module table before any product call ----
$DefaultHttp = { param($Req) $p = ([Uri]$Req['Uri']).AbsolutePath; $m = $Req['Method']
    if ($m -ceq 'GET' -and $p -ceq '/api/status') { return @{ Status = 200; Body = '{"ok":true}' } }
    if ($m -ceq 'GET' -and $p -ceq '/v1/models') { return @{ Status = 200; Body = $global:PxcT.Models } }
    if ($m -ceq 'POST' -and $p -ceq '/v1/chat/completions') { return @{ Status = 200; Body = '{"model":"prov/served","choices":[{"message":{"content":"answer-text"}}]}' } }
    return @{ Status = 404; Body = '' } }
$DefaultProc = { param($ProcId) [pscustomobject]@{ SessionId = [uint32]0; ExecutablePath = $global:PxcT.Pids["$ProcId"] } }
$DefaultSvc = { [pscustomobject]@{ Name = 'ProximaGateway'; PathName = '"' + $global:PxcT.ServiceExe + '"' } }
$DefaultRemote = { param($Session, $Envelope) $T = $global:PxcT; $a = $Envelope['Action']; $d = $null
    if ($a -ceq 'handshake') { $d = @{ protocolVersion = 1; moduleSha256 = $T.SelfSha; configModuleSha256 = $T.CfgSha } }
    elseif ($a -ceq 'models') { $d = @{ models = @('prov/m1', 'prov/m2'); modelState = 'advertised_not_execution_tested' } }
    [pscustomobject]@{ schema = 'px.result.v1'; action = $a; targetFingerprint = $Envelope['TargetFingerprint']; mode = 'Remote'; dryRun = $false; dispatched = $a -cne 'handshake'; outcome = 'ok'; data = $d } }
$Fakes = @{
    NewSession     = { param($Req) $T = $global:PxcT; $T.Calls.Add('NewSession'); $T.SessReqs.Add($Req); if ($T.NewSessionFail) { throw "backend session failure $($T.Sentinel)" }
        $T.SessSeq++; [pscustomobject]@{ PxFakeSession = $T.SessSeq } }
    RemoveSession  = { param($Session) $T = $global:PxcT; $T.Calls.Add("RemoveSession:$($Session.PxFakeSession)"); if ($T.RemoveFail.Contains([int]$Session.PxFakeSession)) { throw "remove failure $($T.Sentinel)" } }
    InvokeRemote   = { param($Session, $Body, $Envelope) $T = $global:PxcT; $T.Calls.Add("InvokeRemote:$($Envelope['Action']):$($Session.PxFakeSession)"); $T.Envelopes.Add($Envelope); $T.Bodies.Add($Body); & $T.RemoteHandler $Session $Envelope }
    Http           = { param($Req) $T = $global:PxcT; $T.Calls.Add("Http:$($Req['Method']) $(([Uri]$Req['Uri']).AbsolutePath)"); $T.HttpReqs.Add($Req); & $T.HttpHandler $Req }
    GetProcess     = { param($ProcId) $T = $global:PxcT; $T.Calls.Add('GetProcess'); & $T.ProcHandler $ProcId }
    UiSessions     = { $T = $global:PxcT; $T.Calls.Add('UiSessions'); & $T.UiHandler }
    GetService     = { $T = $global:PxcT; $T.Calls.Add('GetService'); & $T.SvcHandler }
    ServiceControl = { param($Verb) $T = $global:PxcT; $T.Calls.Add("ServiceControl:$Verb") }
    NewId          = { $T = $global:PxcT; $T.Calls.Add('NewId'); & $T.IdHandler }
}
function Install-Fakes {
    $script:OrigPrim = & $script:Mod { $script:Prim.Clone() }
    $keys = @($script:OrigPrim.Keys | ForEach-Object { [string]$_ }); [Array]::Sort($keys, [StringComparer]::Ordinal)
    if (($keys -join ',') -cne ($PrimKeys -join ',')) { throw "primitive table keys differ from the replaced set: $($keys -join ',')" }
    & $script:Mod { param($f) foreach ($k in @($f.Keys)) { $script:Prim[$k] = $f[$k] } } $Fakes
    $now = & $script:Mod { $script:Prim }
    foreach ($k in $PrimKeys) { if (-not [object]::ReferenceEquals($now[$k], $Fakes[$k])) { throw "primitive $k not replaced" } }
    $Report.primitives_replaced = "$($PrimKeys.Count)/$($PrimKeys.Count) asserted before any product call"
    $script:PxCmd = $script:Mod.ExportedCommands['px']; $script:OpCmd = $script:Mod.ExportedCommands['Invoke-ProximaOperation']
}
function Set-RealHttp([bool]$Real) { $sb = $(if ($Real) { $script:OrigPrim['Http'] } else { $Fakes['Http'] }); & $script:Mod { param($b) $script:Prim['Http'] = $b } $sb }
function Reset-T {
    $T = $global:PxcT
    foreach ($l in $T.Calls, $T.HttpReqs, $T.Envelopes, $T.Bodies, $T.SessReqs) { $l.Clear() }
    $T.RemoveFail.Clear(); $T.NewSessionFail = $false; $T.SessSeq = 0; $T.HttpHandler = $DefaultHttp; $T.RemoteHandler = $DefaultRemote; $T.ProcHandler = $DefaultProc
    $T.UiHandler = { }; $T.SvcHandler = $DefaultSvc; $T.IdHandler = { [guid]::NewGuid().ToString('D') }; $T.ServiceExe = "$($Tg.Svc.Base)\runtime\Proxima.exe"
    $T.Models = '{"data":[{"id":"prov/m1"},{"id":"prov/m2"},{"id":"prov/Model-X"},{"id":"prov/TITLE"},{"id":"other/m9"}]}'
    if ($script:Mod) { & $script:Mod { $script:Sessions.Clear(); $script:Selection.Clear(); $script:Orphans.Clear() } }
}
function Get-ModState {
    & $script:Mod {
        $rows = [Collections.Generic.List[string]]::new()
        foreach ($k in $script:Sessions.Keys) { $rows.Add("S|$k|$($script:Sessions[$k].PxFakeSession)") }
        foreach ($k in $script:Selection.Keys) { foreach ($p in $script:Selection[$k].Keys) { $rows.Add("M|$k|$p|$($script:Selection[$k][$p])") } }
        foreach ($o in $script:Orphans) { $rows.Add("O|$($o.fp)|$($o.session.PxFakeSession)") }
        $rows.Sort([StringComparer]::Ordinal); $rows -join "`n"
    }
}
function Get-Bound([string]$Fp) { & $script:Mod { param($f) $sess = $null; if ($script:Sessions.TryGetValue($f, [ref]$sess)) { $sess.PxFakeSession } } $Fp }
function Get-OrphanIds { @(& $script:Mod { foreach ($o in $script:Orphans) { $o.session.PxFakeSession } }) -join ',' }
# One product call: new primitive calls, module state and fixture tree change, all streams and the terminating error as text.
function Invoke-Guarded([scriptblock]$Call) {
    $T = $global:PxcT; $n = $T.Calls.Count; $st = Get-ModState; $tree = Get-TreeSnapshot $S; $out = @(); $err = $null
    try { $out = @(& $Call *>&1) } catch { $err = $_ }
    $res = @($out | Where-Object { $null -ne $_ -and $_ -isnot [Management.Automation.ErrorRecord] -and $null -ne $_.PSObject.Properties['schema'] })
    $text = ($out | Format-List * -Force | Out-String) + ($res | ConvertTo-Json -Depth 6 | Out-String)
    if ($err) { $text += ($err | Format-List * -Force | Out-String) + "$err" + ($err.Exception | Format-List * -Force | Out-String); if ($err.Exception.InnerException) { $text += "$($err.Exception.InnerException)" } }
    return [pscustomobject]@{ R = $(if ($res.Count) { $res[0] }); Err = $err; Id = $(if ($err) { [string]$err.FullyQualifiedErrorId } else { '' }); Text = $text
        Calls = @($T.Calls.GetRange($n, $T.Calls.Count - $n)); StateChanged = (Get-ModState) -cne $st; TreeChanged = (Get-TreeSnapshot $S) -cne $tree }
}
function Invoke-Px([hashtable]$PxArgs) { $cmd = $script:PxCmd; return (Invoke-Guarded { & $cmd @PxArgs }) }
function Invoke-Op([hashtable]$OpArgs) { $cmd = $script:OpCmd; return (Invoke-Guarded { & $cmd @OpArgs }) }
function Invoke-Wrapper([hashtable]$WArgs) { $w = $WrapperPath; return (Invoke-Guarded { & $w @WArgs }) }
function Get-Fp($Tgt) {
    if ($Tgt.Fp) { return $Tgt.Fp }
    $x = Invoke-Px (New-PxArgs 'config' $Tgt); if (-not $x.R -or "$($x.R.targetFingerprint)" -cnotmatch '^[0-9a-f]{64}\z') { throw "config read failed for fixture target $($Tgt.Name): $($x.Id)" }
    $Tgt.Fp = [string]$x.R.targetFingerprint; return $Tgt.Fp
}
# Assertions record a behavioural token and the case continues; WRONG_CODE is diagnostic only.
function Add-Fail([string]$Msg) { $script:CaseFail.Add($Msg) }
function Assert-Code($X, [string]$Code, [string]$Label) {
    if ($X.R) { Add-Fail "ACCEPTED_INVALID[$Label]" } elseif (-not $X.Err) { Add-Fail "NO_ERROR[$Label]" }
    elseif ($X.Id -cnotmatch "^ProximaControl\.$Code(,|\z)") { Add-Fail "WRONG_CODE[$Label] expected $Code got $($X.Id)" }
}
function Assert-Ok($X, [string]$Label) { if (-not $X.R) { Add-Fail "REJECTED_VALID[$Label] $($X.Id)" } }
function Assert-DryRun($X, [string]$Label) { if (-not $X.R -or $X.R.dryRun -ne $true -or $X.R.dispatched -ne $false -or "$($X.R.outcome)" -cne 'whatif') { Add-Fail "NOT_DRYRUN[$Label] $($X.Id)" } }
function Assert-NoEffect($X, [string]$Token, [string]$Label) {
    if ($X.Calls.Count -or $X.StateChanged -or $X.TreeChanged) { Add-Fail "$Token[$Label] calls=$($X.Calls -join ';') state=$($X.StateChanged) tree=$($X.TreeChanged)" }
}
function Assert-Calls($X, [string[]]$Want, [string]$Label) { if (($X.Calls -join '|') -cne ($Want -join '|')) { Add-Fail "PRIMITIVE_COUNTS[$Label] want=$($Want -join ';') got=$($X.Calls -join ';')" } }
function Get-CallCount($X, [string]$Prefix) { @($X.Calls | Where-Object { $_.StartsWith($Prefix, [StringComparison]::Ordinal) }).Count }
function Invoke-Case([string]$Id, [scriptblock]$Body, [switch]$NoApi) {
    $script:CaseFail = [Collections.Generic.List[string]]::new(); $why = $null; $outcome = 'passed'
    try {
        if ([Globalization.CultureInfo]::CurrentCulture.Name -cne $TestCulture) { throw "CULTURE_CHANGED[$([Globalization.CultureInfo]::CurrentCulture.Name)] before this case" }
        if (-not $NoApi) {
            if (-not $ApiPresent) { throw "API_ABSENT: px/Invoke-ProximaOperation not available from ModulePath ($($Report.api_state))" }
            Reset-T
        }
        Set-TestLocation $S; & $Body
    } catch { $script:CaseFail.Add("$($_.Exception.Message)") } finally { Set-TestLocation $S; if ($ApiPresent) { Set-RealHttp $false } }
    if ($script:CaseFail.Count) { $why = $script:CaseFail -join ' | ' }
    if ($why) { $outcome = $(if ($why.StartsWith('SETUP:')) { 'setup_error' } else { 'failed' }) }
    $Results.Add([pscustomobject]@{ id = $Id; outcome = $outcome; reason = $why })
    Write-Host ('{0} {1}{2}' -f $outcome.ToUpperInvariant(), $Id, $(if ($why) { " :: $why" }))
}
# ---- out-of-process children ----
function Invoke-ChildPs([string]$Exe, [string[]]$ArgList, [string]$Kind) {
    $run = Invoke-Native $Exe $ArgList
    $rec = [ordered]@{ kind = $Kind; exe = $Exe; command = @($Exe) + $ArgList; rc = $run.rc; output_sha256 = (Get-TextSha256 "$($run.out)"); ps_version = $null; ps_edition = $null; culture = $null; ui_culture = $null }
    $Report.children.Add($rec); return @{ Run = $run; Rec = $rec }
}
function Read-ChildJson([string]$Path, $Rec) {
    if (-not [IO.File]::Exists($Path)) { return $null }
    $rep = [IO.File]::ReadAllText($Path) | ConvertFrom-Json
    $Rec.ps_version = "$($rep.ps_version)"; $Rec.ps_edition = "$($rep.ps_edition)"; $Rec.culture = "$($rep.culture)"; $Rec.ui_culture = "$($rep.ui_culture)"
    if ($Rec.culture -cne $TestCulture) { throw "child measured culture '$($Rec.culture)', parent runs $TestCulture" }
    return $rep
}
function Invoke-WrapperChild([hashtable]$WArgs, [string]$PreImport = '') {
    $n = [guid]::NewGuid().ToString('N').Substring(0, 8); $af = "$S\child\wa-$n.xml"; $of = "$S\child\wo-$n.json"
    $null = Write-Fixture $af ([Management.Automation.PSSerializer]::Serialize($WArgs))
    $al = @('-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', "$S\child\child-wrapper.ps1", '-Wrapper', $WrapperPath, '-ArgsFile', $af, '-Out', $of, '-Culture', $TestCulture)
    if ($PreImport) { $al += @('-PreImport', $PreImport) }
    $c = Invoke-ChildPs $SelfExe $al 'fresh-process wrapper'
    return @{ Rc = $c.Run.rc; Out = "$($c.Run.out)"; Rep = (Read-ChildJson $of $c.Rec) }
}
function Copy-Envelope($E, [hashtable]$Set = @{}, [string[]]$Drop = @()) {
    $h = [Collections.Hashtable]::new([StringComparer]::Ordinal)
    foreach ($k in $E.Keys) { if ($Drop -cnotcontains $k) { $h[[string]$k] = $E[$k] } }
    foreach ($k in $Set.Keys) { $h[$k] = $Set[$k] }
    return $h
}
# Once per run: the product's OWN captured handshake envelope and endpoint body, replayed out of process.
function Get-EndpointRun {
    if ($null -ne $script:EpRun) { return $script:EpRun }
    Reset-T
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.Rd @{ Credential = $Cred })
    if (-not $x.R -or $global:PxcT.Envelopes.Count -ne 1) { throw "remote payload capture failed: connect $($x.Id)" }
    $hs = $global:PxcT.Envelopes[0]; $body = $global:PxcT.Bodies[0]; $null = Invoke-Px (New-PxArgs 'disconnect' $Tg.Rd)
    $z64 = '0' * 64
    $items = @(@{ Name = 'whatif-handshake'; Envelope = (Copy-Envelope $hs @{ WhatIf = $true }) }, @{ Name = 'whatif-status'; Envelope = (Copy-Envelope $hs @{ WhatIf = $true; Action = 'status' }) },
        @{ Name = 'bad-protocol'; Envelope = (Copy-Envelope $hs @{ ProtocolVersion = 2 }) }, @{ Name = 'string-protocol'; Envelope = (Copy-Envelope $hs @{ ProtocolVersion = '1' }) },
        @{ Name = 'alias-key'; Envelope = (Copy-Envelope $hs @{ whatIf = $false } @('WhatIf')) }, @{ Name = 'extra-key'; Envelope = (Copy-Envelope $hs @{ Extra = 'x' }) },
        @{ Name = 'string-force'; Envelope = (Copy-Envelope $hs @{ Force = 'False' }) }, @{ Name = 'bad-fingerprint'; Envelope = (Copy-Envelope $hs @{ TargetFingerprint = 'ABC' }) },
        @{ Name = 'relative-base'; Envelope = (Copy-Envelope $hs @{ BasePath = 'rbase' }) }, @{ Name = 'wrong-config-hash'; Envelope = (Copy-Envelope $hs @{ ConfigModuleSha256 = $z64 }) },
        @{ Name = 'wrong-module-hash'; Envelope = (Copy-Envelope $hs @{ ModuleSha256 = $z64 }) }, @{ Name = 'benign-wrong-code'; Envelope = (Copy-Envelope $hs @{ BasePath = "$S\rbad" }) },
        @{ Name = 'dependency-mismatch'; Envelope = (Copy-Envelope $hs @{ BasePath = "$S\rdep"; ConfigModuleSha256 = (Get-FileSha256 "$S\rdep\control\ProximaConfig.psm1") }) },
        @{ Name = 'positive-handshake'; Envelope = (Copy-Envelope $hs) })
    $in = Write-Fixture "$S\child\endpoint-in.xml" ([Management.Automation.PSSerializer]::Serialize([pscustomobject]@{ Body = $body.ToString(); Items = $items }, 6))
    $runs = [Collections.Generic.List[object]]::new()
    foreach ($exe in $ChildExes) {
        $of = "$S\child\endpoint-out-$($runs.Count).json"
        $c = Invoke-ChildPs $exe @('-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', "$S\child\child-endpoint.ps1", '-In', $in, '-Out', $of, '-Culture', $TestCulture) 'endpoint'
        $runs.Add(@{ Exe = $exe; Rc = $c.Run.rc; Out = "$($c.Run.out)"; Rep = (Read-ChildJson $of $c.Rec); Sentinel = [IO.File]::Exists("$S\rbad\control\imported.txt") })
        if ([IO.File]::Exists("$S\rbad\control\imported.txt")) { [IO.File]::Delete("$S\rbad\control\imported.txt") }
    }
    $script:EpRun = @{ Runs = $runs; Body = $body; Envelope = $hs }
    return $script:EpRun
}
function Get-EpRow($Run, [string]$Name) { $r = @($Run.Rep.rows | Where-Object { $_.name -ceq $Name }); if ($r.Count -ne 1) { return $null }; return $r[0] }
# ---- owned loopback HTTP server (TcpListener avoids HttpListener URL ACLs); records method/path/headers/body ----
$WireScript = @'
param($Listener, $Log, $Routes)
while ($true) {
    $c = $null
    try { $c = $Listener.AcceptTcpClient() } catch { break }
    try {
        $c.ReceiveTimeout = 10000; $s = $c.GetStream(); $hdr = [Collections.Generic.List[byte]]::new()
        while ($true) { $b = $s.ReadByte(); if ($b -lt 0) { break }; $hdr.Add([byte]$b); $n = $hdr.Count; if ($n -ge 4 -and $hdr[$n - 4] -eq 13 -and $hdr[$n - 3] -eq 10 -and $hdr[$n - 2] -eq 13 -and $hdr[$n - 1] -eq 10) { break } }
        $lines = [Text.Encoding]::ASCII.GetString($hdr.ToArray()) -split "`r`n"; $first = $lines[0] -split ' '; $len = 0; $headers = [Collections.Generic.List[string]]::new()
        foreach ($l in ($lines | Select-Object -Skip 1)) { if ($l) { $headers.Add($l); if ($l -match '^(?i)content-length:\s*(\d+)') { $len = [int]$Matches[1] } } }
        $body = [byte[]]::new($len); $got = 0; while ($got -lt $len) { $k = $s.Read($body, $got, $len - $got); if ($k -le 0) { break }; $got += $k }
        $Log.Add([pscustomobject]@{ Method = $first[0]; Path = $first[1]; Headers = @($headers); Body = [Text.UTF8Encoding]::new($false).GetString($body, 0, $got) })
        $r = $Routes["$($first[0]) $($first[1])"]; if ($null -eq $r) { $r = @(404, '') }
        $rb = [Text.UTF8Encoding]::new($false).GetBytes([string]$r[1])
        $head = [Text.Encoding]::ASCII.GetBytes("HTTP/1.1 $($r[0]) X`r`nContent-Type: application/json`r`nContent-Length: $($rb.Length)`r`nConnection: close`r`n`r`n")
        $s.Write($head, 0, $head.Length); $s.Write($rb, 0, $rb.Length); $s.Flush()
    } catch { $Log.Add([pscustomobject]@{ Method = 'ERROR'; Path = "$($_.Exception.Message)"; Headers = @(); Body = '' }) } finally { $c.Close() }
}
'@
function Start-WireServer([hashtable]$Routes) {
    $l = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 0); $l.Start()
    $log = [Collections.ArrayList]::Synchronized([Collections.ArrayList]::new()); $ps = [powershell]::Create()
    $null = $ps.AddScript($WireScript).AddArgument($l).AddArgument($log).AddArgument($Routes)
    $w = @{ Listener = $l; Port = $l.LocalEndpoint.Port; Log = $log; Ps = $ps; Async = $ps.BeginInvoke(); Routes = $Routes; Stopped = $false }
    $Wires.Add($w); return $w
}
function Get-WireCount($W, [string]$Method, [string]$Path) { @($W.Log | Where-Object { $_.Method -ceq $Method -and $_.Path -ceq $Path }).Count }
function Get-RecordState([string]$Base, [string]$Id) {
    $p = "$Base\results\px-active\$Id.json"; if (-not [IO.File]::Exists($p)) { return '<absent>' }
    return "$(([IO.File]::ReadAllText($p) | ConvertFrom-Json).state)"
}
function Clear-Journal([string]$Base) { if ([IO.Directory]::Exists("$Base\results")) { $e = [Collections.Generic.List[string]]::new(); Remove-OwnedTree "$Base\results" $e; if ($e.Count) { throw "SETUP: journal reset failed: $($e -join '; ')" } } }
# Dynamic scope: an unqualified name a helper does not bind itself ($S, $Sha, $Keep, $Repo, $Tg ...) resolves through its CALLER's
# scopes, case-insensitively, so a case/handler/helper binding such as $s, $sha, $keep or $repo silently replaces the script value
# for every helper it calls (g2 native run: X5-03 relative junction target, X5-05 [string].ComputeHash, X6-02 WhatIf calls with
# a snapshot string as RepositoryRoot). Returns each non-top-level binding (assignment target, foreach variable, parameter) that
# reuses the name of a top-level binding; the setup refuses to run a harness that has one.
function Find-ScopeShadowing($Root) {
    $top = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase); $inner = [Collections.Generic.List[object]]::new()
    foreach ($v in $Root.FindAll({ param($node) $node -is [Management.Automation.Language.VariableExpressionAst] }, $true)) {
        $name = $v.VariablePath.UserPath
        if (-not $v.VariablePath.IsUnqualified -or [string]::Equals($name, 'null', [StringComparison]::OrdinalIgnoreCase) -or $name.EndsWith('Preference', [StringComparison]::OrdinalIgnoreCase)) { continue }
        $up = $v; $pa = $v.Parent
        while ($pa -is [Management.Automation.Language.ConvertExpressionAst] -or $pa -is [Management.Automation.Language.ArrayLiteralAst]) { $up = $pa; $pa = $pa.Parent }
        if (-not (($pa -is [Management.Automation.Language.AssignmentStatementAst] -and [object]::ReferenceEquals($pa.Left, $up)) -or
                ($pa -is [Management.Automation.Language.ForEachStatementAst] -and [object]::ReferenceEquals($pa.Variable, $v)) -or
                ($pa -is [Management.Automation.Language.ParameterAst] -and [object]::ReferenceEquals($pa.Name, $v)))) { continue }
        $isInner = $false
        for ($an = $v.Parent; $null -ne $an; $an = $an.Parent) {
            if ($an -is [Management.Automation.Language.FunctionDefinitionAst] -or ($an -is [Management.Automation.Language.ScriptBlockAst] -and $null -ne $an.Parent)) { $isInner = $true; break }
        }
        if ($isInner) { $inner.Add($v) } else { $null = $top.Add($name) }
    }
    return @(foreach ($v in $inner) { if ($top.Contains($v.VariablePath.UserPath)) { '{0}@{1}' -f $v.VariablePath.UserPath, $v.Extent.StartLineNumber } })
}

# ---- setup: any failure here is rc 2 ----
$Tc = [Globalization.CultureInfo]::GetCultureInfo($TestCulture); [Threading.Thread]::CurrentThread.CurrentCulture = $Tc; [Threading.Thread]::CurrentThread.CurrentUICulture = $Tc
[Globalization.CultureInfo]::DefaultThreadCurrentCulture = $Tc; [Globalization.CultureInfo]::DefaultThreadCurrentUICulture = $Tc
$Report.test_culture = [Globalization.CultureInfo]::CurrentCulture.Name; $Report.test_ui_culture = [Globalization.CultureInfo]::CurrentUICulture.Name
$LowI = [int]('I'.ToLower()[0]); $Report.test_culture_probe = 'lower(I)=U+{0:X4}' -f $LowI
if ($Report.test_culture -cne $TestCulture -or ($LowI -eq 0x131) -ne ($TestCulture -ceq 'tr-TR')) { throw "test culture $TestCulture not in effect: $($Report.test_culture_probe)" }
if ([Environment]::OSVersion.Platform -ne 'Win32NT') { throw 'Windows host required' }
$Helpers = @(Get-Command -CommandType Function | Where-Object { $_.ScriptBlock.File -eq $PSCommandPath } | ForEach-Object { $_.Name })
$shadowed = @($Helpers | Where-Object { Get-Alias -Name $_ -ErrorAction SilentlyContinue })
if ($Helpers.Count -lt 30 -or $shadowed.Count) { throw "helper alias check failed: $($Helpers.Count) helpers, shadowed: $($shadowed -join ',')" }
if ([IO.File]::ReadAllText($PSCommandPath) -match '(?i)\$(args|pid|home|profile)\s*=[^=]') { throw 'harness assigns an automatic variable' }
# Positive control first (the g2 bug shapes must be found), then this harness itself must have none.
$probeHits = @(Find-ScopeShadowing ([Management.Automation.Language.Parser]::ParseInput('$S = 1; function f { foreach ($s in 1) { } }; & { $sha = 2 }; $Sha = 3', [ref]$null, [ref]$null)))
$selfHits = @(Find-ScopeShadowing ([Management.Automation.Language.Parser]::ParseFile($PSCommandPath, [ref]$null, [ref]$null)))
if (($probeHits -join ',') -cne 's@1,sha@1' -or $selfHits.Count) { throw "scope shadowing check failed: probe=[$($probeHits -join ',')] harness=[$($selfHits -join ',')]" }
$Report.alias_r = "$(@(Get-Alias -Name r -ErrorAction SilentlyContinue | ForEach-Object { $_.Definition }))"
$ModulePath = [IO.Path]::GetFullPath($ModulePath); $Report.module_path = $ModulePath; $ModDir = [IO.Path]::GetDirectoryName($ModulePath)
$WrapperPath = "$ModDir\Run-Px.ps1"; $CfgModPath = "$ModDir\ProximaConfig.psm1"
$Suffix = '\.agents\skills\proxima-control\scripts'
$TreeRoot = $(if ($ModDir.EndsWith($Suffix, [StringComparison]::OrdinalIgnoreCase)) { $ModDir.Substring(0, $ModDir.Length - $Suffix.Length) } else { $ModDir })
# Byte-compared product area: the skill directory of a repository tree, or the isolated source copy of a counterexample.
$MeasuredRoot = $(if ($TreeRoot -cne $ModDir) { [IO.Path]::GetDirectoryName($ModDir) } else { $ModDir })
foreach ($outPath in $ScratchRoot, $ReportPath, $EvidenceRoot) {
    if ($outPath -and ([IO.Path]::GetFullPath($outPath).TrimEnd('\') + '\').StartsWith($TreeRoot.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'ScratchRoot/ReportPath/EvidenceRoot must be outside the measured tree' }
}
if (-not [IO.Directory]::Exists($ScratchRoot)) { throw 'ScratchRoot must be an existing directory' }
$Report.wrapper_sha256 = Get-FileSha256 $WrapperPath; $Report.config_module_sha256 = Get-FileSha256 $CfgModPath
if (Get-Command -Name git -CommandType Application -ErrorAction SilentlyContinue) {
    $gitRun = Invoke-Native 'git' @('-C', $TreeRoot, 'rev-parse', 'HEAD', 'HEAD^{tree}')
    if ($gitRun.rc -eq 0) { $gitOut = @($gitRun.out.Trim() -split '\s+'); if ($gitOut.Count -eq 2) { $Report.git_head = $gitOut[0]; $Report.git_tree = $gitOut[1] } }
}
$SelfExe = [Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$OtherExe = $(if ($PSVersionTable.PSEdition -ceq 'Core') { "$([Environment]::GetEnvironmentVariable('SystemRoot'))\System32\WindowsPowerShell\v1.0\powershell.exe" } else { "$(@(Get-Command -Name pwsh.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object { $_.Source }))" })
$ChildExes = @($SelfExe) + @($(if ($OtherExe -and [IO.File]::Exists($OtherExe)) { $OtherExe }))
$Report.child_exes = $ChildExes
$FullScratch = [IO.Path]::GetFullPath($ScratchRoot).TrimEnd('\'); $RunId = [guid]::NewGuid().ToString('N').Substring(0, 12)
$S = "$FullScratch\pxctl-$RunId"; $Report.scratch = $S; $Repo = "$S\repo"
foreach ($fixDir in 'repo', 'cfg', 'child', 'cx', 'conflict', 'journal-target') { $null = [IO.Directory]::CreateDirectory("$S\$fixDir") }
$Keep = "$FullScratch\pxctl-keep-$RunId"; $null = [IO.Directory]::CreateDirectory($Keep); [IO.File]::WriteAllText("$Keep\keep.txt", $RunId, $Utf8); $KeepSha = Get-FileSha256 "$Keep\keep.txt"
$Evid = "$(if ($EvidenceRoot) { [IO.Path]::GetFullPath($EvidenceRoot).TrimEnd('\') } else { $FullScratch })\pxctl-evid-$RunId"
if ($Counterexamples) { $null = [IO.Directory]::CreateDirectory($Evid); $Report.evidence_dir = $Evid }
$global:PxcT = @{ Calls = [Collections.Generic.List[string]]::new(); HttpReqs = [Collections.Generic.List[object]]::new(); Envelopes = [Collections.Generic.List[object]]::new()
    Bodies = [Collections.Generic.List[object]]::new(); SessReqs = [Collections.Generic.List[object]]::new(); RemoveFail = [Collections.Generic.HashSet[int]]::new(); Pids = @{}
    SessSeq = 0; NewSessionFail = $false; Sentinel = ''; SelfSha = (Get-FileSha256 $ModulePath); CfgSha = (Get-FileSha256 $CfgModPath); Models = ''; ServiceExe = '' }
$Cred = New-Cred 'dummy-not-a-secret'
$Tg = @{}
$Tg.L1 = New-Target 'l1' 'tgt-local' "$S\base1" 4101
$Tg.L1b = New-Target 'l1b' 'tgt-local' "$S\base2" 4102
$Tg.Svc = New-Target 'svc' 'tgt-svc' "$S\base3" 4103
$Tg.J4 = New-Target 'j4' 'tgt-j4' "$S\base4" 4104
$Tg.J5 = New-Target 'j5' 'tgt-j5' "$S\base5" 4105
$Tg.J6 = New-Target 'j6' 'tgt-j6' "$S\base6" 4106
$Tg.In = New-Target 'in' 'tgt-in' "$Repo\inner" 4107
$Tg.Pos = New-Target 'pos' 'tgt-pos' "$S\base7" 4108
$Tg.Sp = New-Target 'sp' 'tgt-sp' "$S\base sp" 4109
$Tg.A = New-Target 'ta' 'Tgt-A' "$S\base1" 4101
$Tg.Nfc = New-Target 'nfc' ('Caf' + [char]0xE9) "$S\base1" 4101
$Tg.Nfd = New-Target 'nfd' ('Cafe' + [char]0x301) "$S\base1" 4101
$Tg.Blank = New-Target 'blank' ' ' "$S\base1" 4101
$Tg.Blank2 = New-Target 'blank2' '  ' "$S\base1" 4101
$Tg.Ctl = New-Target 'ctl' ('PXTID' + [char]9 + [char]0 + 'x') "$S\base1" 4101
$Tg.R1 = New-Target 'r1' 'tgt-remote' "$S\rbase" 0 'https://127.0.0.1:59861/wsman' 'px.test'
$Tg.R2 = New-Target 'r2' 'tgt-remote' "$S\rbase" 0 'https://127.0.0.1:59862/wsman' 'px.test'
$Tg.Rc = New-Target 'rc' 'tgt-rc' "$S\rbase" 0 'https://127.0.0.1:59863/ws@man' (' px' + [char]9 + 'E ')
$Tg.Rd = New-Target 'rd' 'tgt-rd' "$S\rbase" 0 'https://127.0.0.1:59864/wsman' 'px.test'
# Deployed endpoint trees: rbase = the module under test + S1; rbad = benign wrong code (own sentinel); rdep = S1 altered.
foreach ($epTree in 'rbase', 'rbad', 'rdep') { $null = [IO.Directory]::CreateDirectory("$S\$epTree\control") }
if ([IO.File]::Exists($ModulePath)) { [IO.File]::Copy($ModulePath, "$S\rbase\control\ProximaControl.psm1"); [IO.File]::Copy($ModulePath, "$S\rdep\control\ProximaControl.psm1") }
if ([IO.File]::Exists($CfgModPath)) {
    foreach ($epTree in 'rbase', 'rbad') { [IO.File]::Copy($CfgModPath, "$S\$epTree\control\ProximaConfig.psm1") }
    [IO.File]::WriteAllBytes("$S\rdep\control\ProximaConfig.psm1", [byte[]](@([IO.File]::ReadAllBytes($CfgModPath)) + @(13, 10, 35, 10)))
}
$null = Write-Fixture "$S\rbad\control\ProximaControl.psm1" "[IO.File]::WriteAllText((Join-Path `$PSScriptRoot 'imported.txt'), 'imported')`nfunction Invoke-ProximaOperation { 'benign' }`n"
$null = Write-Fixture "$S\conflict\ProximaControl.psm1" "function px { 'conflict' }`n"
$null = Write-Fixture "$S\child\child-endpoint.ps1" @'
param([string]$In, [string]$Out, [string]$Culture)
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$tc = [Globalization.CultureInfo]::GetCultureInfo($Culture); [Threading.Thread]::CurrentThread.CurrentCulture = $tc; [Threading.Thread]::CurrentThread.CurrentUICulture = $tc
$WhatIfPreference = $false
$x = [Management.Automation.PSSerializer]::Deserialize([IO.File]::ReadAllText($In))
$sb = [scriptblock]::Create([string]$x.Body)
$rows = [Collections.Generic.List[object]]::new()
foreach ($it in $x.Items) {
    $e = $it.Envelope
    $row = [ordered]@{ name = [string]$it.Name; ambient_whatif = [bool]$WhatIfPreference; received_whatif = $null; received_whatif_type = $null; fqid = $null; message = $null
        result = $null; imported_before = @(Get-Module -Name ProximaControl).Count; imported_after = $null }
    foreach ($k in @($e.Keys)) { if ([string]$k -ceq 'WhatIf') { $row.received_whatif = "$($e[$k])"; if ($null -ne $e[$k]) { $row.received_whatif_type = $e[$k].GetType().FullName } } }
    try { $o = @(& $sb $e); $row.result = $(if ($o.Count -eq 1) { $o[0] } else { "count=$($o.Count)" }) } catch { $row.fqid = [string]$_.FullyQualifiedErrorId; $row.message = [string]$_.Exception.Message }
    $row.imported_after = @(Get-Module -Name ProximaControl).Count
    $rows.Add([pscustomobject]$row)
}
$rep = [ordered]@{ ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"; culture = [Globalization.CultureInfo]::CurrentCulture.Name
    ui_culture = [Globalization.CultureInfo]::CurrentUICulture.Name; rows = $rows }
[IO.File]::WriteAllText($Out, ($rep | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
'@
$null = Write-Fixture "$S\child\child-wrapper.ps1" @'
param([string]$Wrapper, [string]$ArgsFile, [string]$Out, [string]$Culture, [string]$PreImport = '')
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$tc = [Globalization.CultureInfo]::GetCultureInfo($Culture); [Threading.Thread]::CurrentThread.CurrentCulture = $tc; [Threading.Thread]::CurrentThread.CurrentUICulture = $tc
$WhatIfPreference = $false
$a = [Management.Automation.PSSerializer]::Deserialize([IO.File]::ReadAllText($ArgsFile)); $h = @{}; foreach ($k in $a.Keys) { $h[[string]$k] = $a[$k] }
if ($PreImport) { $null = Import-Module -Name $PreImport -DisableNameChecking -Global }
$row = [ordered]@{ ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"; culture = [Globalization.CultureInfo]::CurrentCulture.Name
    ui_culture = [Globalization.CultureInfo]::CurrentUICulture.Name; fqid = $null; result = $null }
try { $row.result = @(& $Wrapper @h) } catch { $row.fqid = [string]$_.FullyQualifiedErrorId }
[IO.File]::WriteAllText($Out, ($row | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
if ($row.fqid) { exit 1 }
exit 0
'@
$ModSource = $(if ([IO.File]::Exists($ModulePath)) { [IO.File]::ReadAllText($ModulePath) } else { '' })
$UserBefore = Get-UserStateSnapshot; $TreeBeforeImport = Get-TreeSnapshot $S -Hash; $RepoTreeBefore = Get-TreeSnapshot $MeasuredRoot -Hash
$Report.api_state = 'module_absent'
if ([IO.File]::Exists($ModulePath)) {
    try { $Mod = Import-Module -Name $ModulePath -PassThru -DisableNameChecking -Global -ErrorAction Stop } catch { throw "existing module failed to import: $($_.FullyQualifiedErrorId)" }
    $ApiPresent = $null -ne $Mod.ExportedCommands['px'] -and $null -ne $Mod.ExportedCommands['Invoke-ProximaOperation'] -and [IO.File]::Exists($WrapperPath)
    $Report.api_state = $(if ($ApiPresent) { 'present' } else { 'module_without_api' })
}
$UserAfterImport = Get-UserStateSnapshot; $TreeAfterImport = Get-TreeSnapshot $S -Hash
if ($ApiPresent) { Install-Fakes; Reset-T }

# ---- cases ----
Invoke-Case 'X1-01' {
    $names = @($Mod.ExportedCommands.Keys | ForEach-Object { [string]$_ }); [Array]::Sort($names, [StringComparer]::Ordinal)
    if (($names -join ',') -cne 'Invoke-ProximaOperation,px') { Add-Fail "EXPORTS[$($names -join ',')]" }
    if ($Mod.ExportedAliases.Count -or $Mod.ExportedVariables.Count) { Add-Fail 'EXPORTS_EXTRA[alias or variable]' }
    foreach ($c in @($PxCmd, $OpCmd, (Get-Command -Name $WrapperPath))) {
        $cb = @($c.ScriptBlock.Attributes | Where-Object { $_ -is [Management.Automation.CmdletBindingAttribute] })
        if ($cb.Count -ne 1 -or -not $cb[0].SupportsShouldProcess -or "$($cb[0].ConfirmImpact)" -cne 'Medium') { Add-Fail "NO_SHOULDPROCESS[$($c.Name)]" }
        if (-not $c.Parameters.ContainsKey('WhatIf') -or -not $c.Parameters.ContainsKey('Confirm')) { Add-Fail "NO_WHATIF_PARAM[$($c.Name)]" }
    }
    $wc = Get-Command -Name $WrapperPath
    foreach ($n in 'Action', 'Provider', 'Value', 'ConfigPath', 'RepositoryRoot', 'TargetId', 'Model', 'Credential', 'Force') {
        foreach ($c in $PxCmd, $wc) { if (-not $c.Parameters.ContainsKey($n)) { Add-Fail "PARAM_MISSING[$($c.Name) $n]" } }
    }
    foreach ($n in 'ConnectionUri', 'ConfigurationName', 'Session') { foreach ($c in $PxCmd, $wc) { if ($c.Parameters.ContainsKey($n)) { Add-Fail "OVERRIDE_PARAM[$($c.Name) $n]" } } }
    foreach ($pp in @(@('Action', 0), @('Provider', 1), @('Value', 2))) {
        foreach ($c in $PxCmd, $wc) {
            $pa = @($c.Parameters[$pp[0]].Attributes | Where-Object { $_ -is [Management.Automation.ParameterAttribute] })
            if ($pa.Count -lt 1 -or $pa[0].Position -ne $pp[1]) { Add-Fail "POSITION[$($c.Name) $($pp[0])]" }
        }
    }
    foreach ($n in 'Action', 'BasePath', 'TargetFingerprint', 'ProtectedRoot') { if (-not @($OpCmd.Parameters[$n].Attributes | Where-Object { $_ -is [Management.Automation.ParameterAttribute] -and $_.Mandatory }).Count) { Add-Fail "OP_NOT_MANDATORY[$n]" } }
    if (@([IO.File]::ReadAllLines($WrapperPath))[0] -cne '#requires -Version 5.1') { Add-Fail 'WRAPPER_REQUIRES_5_1' }
    $x = Invoke-Px @{ Action = 'help' }; if (-not $x.R -or "$($x.R.schema)" -cne 'px.result.v1' -or "$($x.R.outcome)" -cne 'ok') { Add-Fail 'HELP_RESULT' }
    Assert-NoEffect $x 'HELP_SIDE_EFFECT' 'help'
    Assert-Code (Invoke-Px @{ Action = 'Status'; ConfigPath = $Tg.L1.Cfg; RepositoryRoot = $Repo; TargetId = $Tg.L1.Tid }) 'UnknownAction' 'action case variant'
    Assert-Code (Invoke-Px @{ Action = 'status'; ConfigPath = $Tg.L1.Cfg; RepositoryRoot = $Repo }) 'ArgumentMissing' 'TargetId missing'
}
Invoke-Case 'X1-02' {
    $cases = @(@('case', $Tg.A, 'tgt-A'), @('NUL', $Tg.A, ('Tgt-A' + [char]0)), @('trailing blank', $Tg.A, 'Tgt-A '), @('leading blank', $Tg.A, ' Tgt-A'),
        @('NFD id for NFC config', $Tg.Nfc, ('Cafe' + [char]0x301)), @('NFC id for NFD config', $Tg.Nfd, ('Caf' + [char]0xE9)))
    foreach ($c in $cases) {
        foreach ($v in @(@('status', @{}), @('ask', @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' }), @('status WhatIf', @{ WhatIf = $true }), @('config', @{}))) {
            $a = New-PxArgs (($v[0] -split ' ')[0]) $c[1] $v[1]; $a.TargetId = $c[2]; $x = Invoke-Px $a
            Assert-Code $x 'TargetMismatch' "$($c[0]) $($v[0])"; Assert-NoEffect $x 'MISMATCH_SIDE_EFFECT' "$($c[0]) $($v[0])"
            if ($x.Text.Contains('Tgt-A') -or $x.Text.Contains('Caf')) { Add-Fail "TARGET_ECHOED[$($c[0]) $($v[0])]" }
        }
    }
    Assert-DryRun (Invoke-Px (New-PxArgs 'status' $Tg.A @{ WhatIf = $true })) 'exact Tgt-A'
    Assert-DryRun (Invoke-Px (New-PxArgs 'status' $Tg.Nfc @{ WhatIf = $true })) 'exact NFC'
}
Invoke-Case 'X1-03' {
    $fps = @{}
    foreach ($t in $Tg.Blank, $Tg.Blank2, $Tg.Ctl, $Tg.L1) {
        $x = Invoke-Px (New-PxArgs 'config' $t)
        if (-not $x.R -or -not [string]::Equals([string]$x.R.data.targetId, $t.Tid, [StringComparison]::Ordinal)) { Add-Fail "ALTERED_VALID[$($t.Name)] $($x.Id)"; continue }
        $fps[$t.Name] = [string]$x.R.targetFingerprint
        $d = Invoke-Px (New-PxArgs 'status' $t @{ WhatIf = $true }); Assert-DryRun $d "blank/control $($t.Name)"; Assert-NoEffect $d 'WHATIF_SIDE_EFFECT' "$($t.Name) status"
    }
    if (@($fps.Values | Select-Object -Unique).Count -ne 4) { Add-Fail 'FINGERPRINT_COLLISION[blank/control/ordinary targets]' }
    foreach ($t in $Tg.Ctl, $Tg.Blank) {
        if (-not $fps.ContainsKey($t.Name)) { continue }
        $w = Invoke-WrapperChild @{ Action = 'status'; ConfigPath = $t.Cfg; RepositoryRoot = $Repo; TargetId = $t.Tid; WhatIf = $true }
        if ($w.Rc -ne 0 -or -not $w.Rep -or $w.Rep.fqid) { Add-Fail "CHILD_WHATIF_FAILED[$($t.Name)] rc=$($w.Rc)" }
        if (-not $w.Out.Contains('px target ' + $fps[$t.Name].Substring(0, 12))) { Add-Fail "DIGEST_NOT_DISPLAYED[$($t.Name)]" }
        if ($w.Out.Contains('PXTID')) { Add-Fail "RAW_TARGET_DISPLAYED[$($t.Name)]" }
    }
}
Invoke-Case 'X2-01' {
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'fixture connect R1'
    Assert-Ok (Invoke-Px (New-PxArgs 'use' $Tg.L1 @{ Provider = 'prov'; Value = 'prov/m1' })) 'fixture use L1'
    $variants = [ordered]@{ 'WhatIf' = @{ WhatIf = $true }; 'WhatIf+Force' = @{ WhatIf = $true; Force = $true }; 'WhatIf+Confirm:false' = @{ WhatIf = $true; Confirm = $false } }
    $acts = @(@('status', $Tg.L1, @{}), @('models', $Tg.L1, @{ Provider = 'prov' }), @('use', $Tg.L1, @{ Provider = 'prov'; Value = 'prov/m2' }), @('ask', $Tg.L1, @{ Provider = 'prov'; Value = 'p' }),
        @('start', $Tg.Svc, @{}), @('stop', $Tg.Svc, @{}), @('restart', $Tg.Svc, @{}), @('connect', $Tg.R1, @{ Credential = $Cred }), @('disconnect', $Tg.R1, @{}),
        @('remote status', $Tg.R1, @{}), @('remote models', $Tg.R1, @{}), @('remote use', $Tg.R1, @{ Provider = 'prov'; Value = 'prov/m2' }),
        @('remote ask', $Tg.R1, @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' }), @('remote stop', $Tg.R1, @{}), @('remote restart', $Tg.R1, @{}))
    foreach ($a in $acts) {
        foreach ($vn in $variants.Keys) {
            $more = @{}; foreach ($k in $a[2].Keys) { $more[$k] = $a[2][$k] }; foreach ($k in $variants[$vn].Keys) { $more[$k] = $variants[$vn][$k] }
            $x = Invoke-Px (New-PxArgs (($a[0] -split ' ')[-1]) $a[1] $more)
            Assert-DryRun $x "$($a[0]) $vn"; Assert-NoEffect $x 'WHATIF_SIDE_EFFECT' "$($a[0]) $vn"
        }
    }
    foreach ($act in 'config', 'help') { Assert-NoEffect (Invoke-Px (New-PxArgs $act $Tg.L1 @{ WhatIf = $true; Force = $true })) 'WHATIF_SIDE_EFFECT' "$act WhatIf+Force" }
    # Ambient WhatIf at global scope (what a module function sees) also wins.
    $saved = $global:WhatIfPreference
    try { $global:WhatIfPreference = $true; $x = Invoke-Px (New-PxArgs 'use' $Tg.L1 @{ Provider = 'prov'; Value = 'prov/m2'; Confirm = $false }) } finally { $global:WhatIfPreference = $saved }
    Assert-DryRun $x 'global ambient use'; Assert-NoEffect $x 'WHATIF_SIDE_EFFECT' 'global ambient use'
}
Invoke-Case 'X2-02' {
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'fixture connect R1'
    foreach ($v in @(@('WhatIf', @{ WhatIf = $true }), @('WhatIf+Confirm:false', @{ WhatIf = $true; Confirm = $false }), @('WhatIf+Force', @{ WhatIf = $true; Force = $true }))) {
        $x = Invoke-Px (New-PxArgs 'connect' $Tg.R1 $v[1]); Assert-DryRun $x "connect no credential $($v[0])"; Assert-NoEffect $x 'WHATIF_SIDE_EFFECT' "connect no credential $($v[0])"
    }
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.R1); Assert-Code $x 'CredentialRequired' 'connect without credential'
    if (Get-CallCount $x 'NewSession') { Add-Fail 'SESSION_WITHOUT_CREDENTIAL' }
    foreach ($tok in 'Get-Credential', 'Read-Host', 'PromptForCredential') { if ($ModSource.IndexOf($tok, [StringComparison]::OrdinalIgnoreCase) -ge 0) { Add-Fail "CREDENTIAL_PROMPT_TOKEN[$tok]" } }
}
Invoke-Case 'X2-03' {
    $marker = [guid]::NewGuid().ToString('N'); & $Mod { param($m) $script:PxcHarnessMarker = $m } $marker
    if ((& $Mod { [bool]$WhatIfPreference }) -ne $false) { throw 'SETUP: module ambient WhatIf is not false' }
    foreach ($a in @(@('status', $Tg.L1, @{}), @('use', $Tg.L1, @{ Provider = 'prov'; Value = 'prov/m1' }), @('ask', $Tg.L1, @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' }),
            @('stop', $Tg.Svc, @{ Force = $true }), @('connect', $Tg.R1, @{ Credential = $Cred }))) {
        $more = @{ WhatIf = $true }; foreach ($k in $a[2].Keys) { $more[$k] = $a[2][$k] }
        $x = Invoke-Wrapper (New-PxArgs $a[0] $a[1] $more); Assert-DryRun $x "wrapper $($a[0])"; Assert-NoEffect $x 'WRAPPER_WHATIF_LOST' "wrapper $($a[0])"
    }
    $x = Invoke-Wrapper (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred }); Assert-Ok $x 'wrapper connect'
    $sid = Get-Bound (Get-Fp $Tg.R1)
    $x = Invoke-Wrapper (New-PxArgs 'status' $Tg.R1); Assert-Ok $x 'wrapper status after connect'; Assert-Calls $x @("InvokeRemote:status:$sid") 'same-process session reuse'
    if ((& $Mod { $script:PxcHarnessMarker }) -cne $marker -or @(Get-Module -Name ProximaControl).Count -ne 1) { Add-Fail 'MODULE_REIMPORTED[wrapper reset module state]' }
    Assert-Ok (Invoke-Wrapper (New-PxArgs 'disconnect' $Tg.R1)) 'wrapper disconnect'
}
Invoke-Case 'X2-04' {
    $fp = Get-Fp $Tg.L1
    foreach ($act in 'status', 'models', 'ask', 'start', 'stop', 'restart', 'handshake') {
        foreach ($v in @(@('WhatIf', @{ WhatIf = $true }), @('WhatIf+Force+Confirm:false', @{ WhatIf = $true; Force = $true; Confirm = $false }))) {
            $a = @{ Action = $act; BasePath = $Tg.L1.Base; TargetFingerprint = $fp; ProtectedRoot = $Repo; Provider = 'prov'; Model = 'prov/m1'; Prompt = 'p' }
            foreach ($k in $v[1].Keys) { $a[$k] = $v[1][$k] }
            $x = Invoke-Op $a; Assert-DryRun $x "export $act $($v[0])"; Assert-NoEffect $x 'EXPORT_WHATIF_LOST' "export $act $($v[0])"
        }
    }
    $ep = Get-EndpointRun
    foreach ($run in $ep.Runs) {
        if (-not $run.Rep) { Add-Fail "CHILD_NO_REPORT[$($run.Exe)] rc=$($run.Rc)"; continue }
        foreach ($n in 'whatif-handshake', 'whatif-status') {
            $row = Get-EpRow $run $n
            if (-not $row -or -not $row.result -or $row.result.dryRun -ne $true -or $row.imported_after -ne 0 -or $row.ambient_whatif -ne $false) { Add-Fail "ENDPOINT_WHATIF_LOST[$($run.Rep.ps_edition) $n]" }
            elseif ($row.received_whatif -cne 'True' -or $row.received_whatif_type -cne 'System.Boolean') { Add-Fail "ENVELOPE_WHATIF_NOT_BOOL[$($run.Rep.ps_edition) $n]" }
        }
    }
}
Invoke-Case 'X2-05' {
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'fixture connect R1'
    foreach ($a in @(@('status', @{}), @('models', @{}), @('use', @{ Provider = 'prov'; Value = 'prov/m1' }), @('ask', @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' }),
            @('start', @{}), @('stop', @{ Force = $true }), @('restart', @{}), @('connect', @{ Credential = $Cred }), @('disconnect', @{}))) {
        $more = @{ WhatIf = $true }; foreach ($k in $a[1].Keys) { $more[$k] = $a[1][$k] }
        $x = Invoke-Px (New-PxArgs $a[0] $Tg.R1 $more)
        if ((Get-CallCount $x 'InvokeRemote') + (Get-CallCount $x 'NewSession') + (Get-CallCount $x 'RemoveSession')) { Add-Fail "REMOTE_TRANSPORT_UNDER_WHATIF[$($a[0])]" }
        Assert-DryRun $x "remote $($a[0])"
    }
}
Invoke-Case 'X2-06' {
    Assert-Ok (Invoke-Px (New-PxArgs 'use' $Tg.L1 @{ Provider = 'prov'; Value = 'prov/m1' })) 'fixture use m1'
    foreach ($v in @(@('WhatIf', @{ WhatIf = $true }), @('WhatIf+Confirm:false', @{ WhatIf = $true; Confirm = $false }))) {
        $more = @{ Provider = 'prov'; Value = 'prov/m2' }; foreach ($k in $v[1].Keys) { $more[$k] = $v[1][$k] }
        $x = Invoke-Px (New-PxArgs 'use' $Tg.L1 $more)
        if ((Get-CallCount $x 'Http:GET') -or $x.StateChanged) { Add-Fail "USE_WHATIF_EFFECT[$($v[0])]" }
    }
    $x = Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = 'p' }); Assert-Ok $x 'ask uses unchanged selection'
    if ($x.R -and "$($x.R.data.requestedModel)" -cne 'prov/m1') { Add-Fail 'SELECTION_CHANGED_UNDER_WHATIF' }
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'fixture connect R1'
    $x = Invoke-Px (New-PxArgs 'use' $Tg.R1 @{ Provider = 'prov'; Value = 'prov/m1'; WhatIf = $true }); if ((Get-CallCount $x 'InvokeRemote') -or $x.StateChanged) { Add-Fail 'USE_WHATIF_EFFECT[remote]' }
}
Invoke-Case 'X2-07' {
    $z = 'PXSENTINEL' + [guid]::NewGuid().ToString('N'); $global:PxcT.Sentinel = $z; $savedKey = [Environment]::GetEnvironmentVariable('PROXIMA_API_KEY')
    try {
        [Environment]::SetEnvironmentVariable('PROXIMA_API_KEY', "$z-key")
        $global:PxcT.HttpHandler = { param($Req) throw "backend models failure $($global:PxcT.Sentinel)-body" }
        $xs = @(@('models error', (Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = "$z-prompt"; Model = 'prov/m1' }))), @('status error', (Invoke-Px (New-PxArgs 'status' $Tg.L1))))
        $global:PxcT.HttpHandler = { param($Req) if ($Req['Method'] -ceq 'POST') { return @{ Status = 500; Body = "$($global:PxcT.Sentinel)-body" } }; & $DefaultHttp $Req }
        $xs += , @('post 500', (Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = "$z-prompt"; Model = 'prov/m1' })))
        $global:PxcT.HttpHandler = $DefaultHttp
        $ok = Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = "$z-prompt"; Model = 'prov/m1' }); $xs += , @('ask ok', $ok)
        if (@($global:PxcT.HttpReqs | Where-Object { "$($_['Headers']['Authorization'])" -ceq "Bearer $z-key" }).Count -lt 1) { Add-Fail 'KEY_NOT_USED[positive control]' }
        $global:PxcT.NewSessionFail = $true
        $xs += , @('connect error', (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = (New-Cred "$z-pw") })))
        $global:PxcT.NewSessionFail = $false
        Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = (New-Cred "$z-pw") })) 'fixture connect R1'
        $global:PxcT.RemoteHandler = { param($Session, $Envelope) throw [Management.Automation.ErrorRecord]::new([Exception]::new("$($global:PxcT.Sentinel)-body"), 'Backend.Failure', 'NotSpecified', $null) }
        $xs += , @('remote error', (Invoke-Px (New-PxArgs 'ask' $Tg.R1 @{ Provider = 'prov'; Value = "$z-prompt"; Model = 'prov/m1' })))
        $xs += , @('whatif ask', (Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = "$z-prompt"; Model = 'prov/m1'; WhatIf = $true })))
        foreach ($c in $xs) {
            if ($c[1].Text.Contains($z)) { Add-Fail "SENTINEL_ECHOED[$($c[0])]" }
            if ($c[1].Err -and "$($c[1].Err.Exception.Message)" -cnotmatch '^ProximaControl: operation rejected: [A-Za-z]+\.\z') { Add-Fail "ERROR_NOT_FIXED[$($c[0])]" }
        }
        if ($xs[0][1].Id -cnotmatch '^ProximaControl\.ModelsUnavailable' -or $xs[1][1].Id -cnotmatch '^ProximaControl\.StatusUnavailable' -or $xs[4][1].Id -cnotmatch '^ProximaControl\.SessionFailed' -or $xs[5][1].Id -cnotmatch '^ProximaControl\.RemoteFailed') { Add-Fail 'WRONG_CODE[sentinel paths]' }
        foreach ($f in @([IO.Directory]::GetFiles("$($Tg.L1.Base)\results\px-active"))) { if ([IO.File]::ReadAllText($f).Contains($z)) { Add-Fail 'SENTINEL_IN_RECORD' } }
        $w = Invoke-WrapperChild @{ Action = 'ask'; Provider = 'prov'; Value = "$z-prompt"; Model = 'prov/m1'; ConfigPath = $Tg.L1.Cfg; RepositoryRoot = $Repo; TargetId = $Tg.L1.Tid; WhatIf = $true }
        if ($w.Rc -ne 0 -or -not $w.Out.Contains('px target ' + (Get-Fp $Tg.L1).Substring(0, 12))) { Add-Fail "CHILD_WHATIF_NOT_SHOWN rc=$($w.Rc)" }
        if ($w.Out.Contains($z)) { Add-Fail 'SENTINEL_ECHOED[child WhatIf text]' }
    } finally { [Environment]::SetEnvironmentVariable('PROXIMA_API_KEY', $savedKey) }
}
Invoke-Case 'X3-01' {
    $fps = @(foreach ($t in $Tg.L1, $Tg.L1b, $Tg.R1, $Tg.R2) { Get-Fp $t })
    if (@($fps | Select-Object -Unique).Count -ne 4) { Add-Fail 'FINGERPRINT_COLLISION[same targetId, different base/URI]' }
    Assert-Ok (Invoke-Px (New-PxArgs 'use' $Tg.L1 @{ Provider = 'prov'; Value = 'prov/m1' })) 'use on L1'
    $x = Invoke-Px (New-PxArgs 'ask' $Tg.L1b @{ Provider = 'prov'; Value = 'p' })
    if ($x.R -or (Get-CallCount $x 'Http:POST')) { Add-Fail 'SELECTION_LEAK[same targetId, different base]' } else { Assert-Code $x 'NoModelSelected' 'second target has no selection' }
    $x = Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = 'p' }); Assert-Ok $x 'L1 uses its own selection'
    $post = @($global:PxcT.HttpReqs | Where-Object { $_['Method'] -ceq 'POST' })
    if ($post.Count -ne 1 -or ([string]$post[-1]['Body'] | ConvertFrom-Json).model -cne 'prov/m1') { Add-Fail 'WRONG_SELECTED_MODEL' }
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'connect R1'
    $x = Invoke-Px (New-PxArgs 'status' $Tg.R2); if ($x.R -or (Get-CallCount $x 'InvokeRemote')) { Add-Fail 'SESSION_LEAK[same targetId, different URI]' } else { Assert-Code $x 'NotConnected' 'R2 not connected' }
    $sid = Get-Bound $fps[2]; $n = $global:PxcT.Calls.Count
    $script:Mod = Import-Module -Name $ModulePath -Force -PassThru -DisableNameChecking -Global -ErrorAction Stop
    if (@($global:PxcT.Calls.GetRange($n, $global:PxcT.Calls.Count - $n)) -cnotcontains "RemoveSession:$sid") { Add-Fail 'ONREMOVE_DID_NOT_RELEASE_OWNED_SESSION' }
    Install-Fakes
    $x = Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = 'p' }); if ($x.R) { Add-Fail 'STATE_SURVIVED_REIMPORT[selection]' } else { Assert-Code $x 'NoModelSelected' 'selection after reimport' }
    $x = Invoke-Px (New-PxArgs 'status' $Tg.R1); if ($x.R) { Add-Fail 'STATE_SURVIVED_REIMPORT[session]' } else { Assert-Code $x 'NotConnected' 'session after reimport' }
}
Invoke-Case 'X3-02' {
    $adopt = 'Get-PSSession', 'Connect-PSSession', 'Enter-PSSession'
    # Static: no NON-comment token (call, module-qualified name, or string usable with & / Get-Command) names an adoption command.
    # Comments are prose, not calls (the module header documents "no Get-PSSession adoption"); New-PSSession proves code is scanned.
    $toks = $null; $null = [Management.Automation.Language.Parser]::ParseInput($ModSource, [ref]$toks, [ref]$null)
    $code = @($toks | Where-Object { $_.Kind -ne [Management.Automation.Language.TokenKind]::Comment } | ForEach-Object { $_.Text }) -join "`n"
    if ($code.IndexOf('New-PSSession', [StringComparison]::Ordinal) -lt 0) { Add-Fail 'TOKEN_SCAN_VACUOUS[New-PSSession not seen]' }
    foreach ($tok in $adopt) { if ($code.IndexOf($tok, [StringComparison]::OrdinalIgnoreCase) -ge 0) { Add-Fail "IMPLICIT_SESSION_LOOKUP[$tok]" } }
    # Behavioural: unqualified adoption commands resolve to recording global shims while px and the in-process wrapper run.
    try {
        foreach ($tok in $adopt) { Set-Item -Path "function:global:$tok" -Value ([scriptblock]::Create("`$global:PxcT.Calls.Add('Adopt:$tok')")) }
        $x = Invoke-Px (New-PxArgs 'status' $Tg.R1); Assert-Code $x 'NotConnected' 'status without connect'
        if ($x.Calls.Count) { Add-Fail "AUTOCONNECT[$($x.Calls -join ';')]" }
        $x = Invoke-Wrapper (New-PxArgs 'status' $Tg.R1); Assert-Code $x 'NotConnected' 'wrapper status without connect'
        if ($x.Calls.Count) { Add-Fail "AUTOCONNECT[wrapper $($x.Calls -join ';')]" }
    } finally { foreach ($tok in $adopt) { if (Test-Path -Path "function:global:$tok") { Remove-Item -Path "function:global:$tok" } } }
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'parent connect R1'
    $w = Invoke-WrapperChild @{ Action = 'status'; ConfigPath = $Tg.R1.Cfg; RepositoryRoot = $Repo; TargetId = $Tg.R1.Tid }
    if ($w.Rc -eq 0 -or -not $w.Rep -or "$($w.Rep.fqid)" -cnotmatch '^ProximaControl\.NotConnected') { Add-Fail "FRESH_PROCESS_REUSED[rc=$($w.Rc) fqid=$(if ($w.Rep) { $w.Rep.fqid })]" }
    $w = Invoke-WrapperChild @{ Action = 'help' } "$S\conflict\ProximaControl.psm1"
    if ($w.Rc -eq 0 -or -not $w.Rep -or "$($w.Rep.fqid)" -cnotmatch '^ProximaControl\.ModuleConflict') { Add-Fail "MODULE_CONFLICT_ACCEPTED[rc=$($w.Rc)]" }
}
Invoke-Case 'X4-01' {
    $f1 = Get-Fp $Tg.R1; $f2 = Get-Fp $Tg.R2
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R2 @{ Credential = $Cred })) 'connect R2 (unrelated, session 1)'
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'connect R1 (session 2)'
    $global:PxcT.RemoteHandler = { param($Session, $Envelope) $r = & $DefaultRemote $Session $Envelope; if ($Envelope['Action'] -ceq 'handshake') { $r.data['moduleSha256'] = '0' * 64 }; $r }
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred }); Assert-Code $x 'HandshakeFailed' 'handshake mismatch'
    if ($x.Calls -cnotcontains 'RemoveSession:3' -or (Get-Bound $f1) -ne 2) { Add-Fail "REPLACEMENT_LOST_BINDING[handshake failure] bound=$(Get-Bound $f1)" }
    $global:PxcT.RemoveFail.Add(4) | Out-Null
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred }); Assert-Code $x 'ConnectCleanupFailed' 'handshake mismatch + cleanup failure'
    if ((Get-Bound $f1) -ne 2 -or (Get-OrphanIds) -cne '4') { Add-Fail "ORPHAN_NOT_RETAINED[new session] orphans=$(Get-OrphanIds)" }
    $global:PxcT.RemoteHandler = $DefaultRemote; $global:PxcT.RemoveFail.Clear(); $global:PxcT.RemoveFail.Add(2) | Out-Null
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })
    if (-not $x.R -or "$($x.R.outcome)" -cne 'connected_old_cleanup_failed' -or (Get-Bound $f1) -ne 5 -or (Get-OrphanIds) -cne '4,2') { Add-Fail "OLD_CLEANUP_NOT_REPORTED bound=$(Get-Bound $f1) orphans=$(Get-OrphanIds) $($x.Id)" }
    $global:PxcT.NewSessionFail = $true
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred }); Assert-Code $x 'SessionFailed' 'new session failure'
    if ((Get-Bound $f1) -ne 5) { Add-Fail 'REPLACEMENT_LOST_BINDING[session factory failure]' }
    $global:PxcT.NewSessionFail = $false; $global:PxcT.RemoveFail.Clear(); foreach ($i in 5, 4, 2) { $null = $global:PxcT.RemoveFail.Add($i) }
    $x = Invoke-Px (New-PxArgs 'disconnect' $Tg.R1); Assert-Code $x 'DisconnectFailed' 'disconnect failure'
    if ((Get-Bound $f1) -ne 5 -or (Get-OrphanIds) -cne '4,2') { Add-Fail 'DISCONNECT_DROPPED_OWNED_ENTRY' }
    $global:PxcT.RemoveFail.Clear()
    $x = Invoke-Px (New-PxArgs 'disconnect' $Tg.R1); Assert-Ok $x 'disconnect retry'
    Assert-Calls $x @('RemoveSession:5', 'RemoveSession:4', 'RemoveSession:2') 'disconnect releases binding and own orphans'
    if ($null -ne (Get-Bound $f1) -or (Get-OrphanIds) -cne '' -or (Get-Bound $f2) -ne 1 -or $global:PxcT.Calls -ccontains 'RemoveSession:1') { Add-Fail 'UNRELATED_SESSION_TOUCHED' }
}
Invoke-Case 'X4-02' {
    $global:PxcT.RemoteHandler = { param($Session, $Envelope) $r = & $DefaultRemote $Session $Envelope; if ($Envelope['Action'] -ceq 'handshake') { $r.data['protocolVersion'] = '1' }; $r }
    Assert-Code (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'HandshakeFailed' 'protocol as string'
    $body = (& $Mod { $script:EndpointBody }).ToString()
    if ($body.IndexOf('EndpointCodeMismatch', [StringComparison]::Ordinal) -lt 0 -or $body.IndexOf('EndpointCodeMismatch', [StringComparison]::Ordinal) -gt $body.IndexOf('Import-Module', [StringComparison]::Ordinal)) { Add-Fail 'HASH_CHECK_ORDER' }
    $want = [ordered]@{ 'bad-protocol' = 'ProtocolMismatch'; 'string-protocol' = 'ProtocolMismatch'; 'alias-key' = 'RequestInvalid'; 'extra-key' = 'RequestInvalid'; 'string-force' = 'RequestInvalid'
        'bad-fingerprint' = 'RequestInvalid'; 'relative-base' = 'RequestInvalid'; 'wrong-config-hash' = 'EndpointCodeMismatch'; 'wrong-module-hash' = 'EndpointCodeMismatch'; 'benign-wrong-code' = 'EndpointCodeMismatch' }
    foreach ($run in (Get-EndpointRun).Runs) {
        $ed = "$(if ($run.Rep) { $run.Rep.ps_edition } else { $run.Exe })"
        if ($run.Sentinel) { Add-Fail "HASH_BEFORE_IMPORT[$ed benign wrong code executed]" }
        if (-not $run.Rep) { Add-Fail "CHILD_NO_REPORT[$ed] rc=$($run.Rc)"; continue }
        foreach ($n in $want.Keys) {
            $row = Get-EpRow $run $n
            if (-not $row -or $row.result -or "$($row.fqid)" -cnotmatch "^ProximaControl\.$($want[$n])(,|\z)" -or $row.imported_after -ne 0) { Add-Fail "ENDPOINT_ACCEPTED_INVALID[$ed $n] fqid=$(if ($row) { $row.fqid })" }
        }
        $row = Get-EpRow $run 'dependency-mismatch'
        if (-not $row -or $row.result -or "$($row.fqid) $($row.message)" -notmatch 'DependencyMismatch') { Add-Fail "S1_HASH_NOT_CHECKED_ON_ENDPOINT[$ed]" }
    }
}
Invoke-Case 'X4-03' {
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.Rc @{ Credential = $Cred }); Assert-Ok $x 'connect Rc'
    if ($global:PxcT.SessReqs.Count -ne 1) { throw 'session factory not called exactly once' }
    $r = $global:PxcT.SessReqs[0]; $keys = @($r.Keys | ForEach-Object { [string]$_ }); [Array]::Sort($keys, [StringComparer]::Ordinal)
    if (($keys -join ',') -cne 'Authentication,ConfigurationName,ConnectionUri,Credential,SkipCACheck,SkipCNCheck,SkipRevocationCheck') { Add-Fail "SESSION_REQUEST_SHAPE[$($keys -join ',')]" }
    if ([string]$r['ConnectionUri'] -cne 'https://127.0.0.1:59863/ws@man' -or -not [string]::Equals([string]$r['ConfigurationName'], (' px' + [char]9 + 'E '), [StringComparison]::Ordinal)) { Add-Fail 'ENDPOINT_NOT_EXACT' }
    if (-not [object]::ReferenceEquals($r['Credential'], $Cred) -or [string]$r['Authentication'] -cne 'Negotiate') { Add-Fail 'CREDENTIAL_OR_AUTH_NOT_FORWARDED' }
    foreach ($k in 'SkipCACheck', 'SkipCNCheck', 'SkipRevocationCheck') { if ($r[$k] -isnot [bool] -or $r[$k]) { Add-Fail "CERT_SKIP[$k]" } }
    $src = $OrigPrim['NewSession'].ToString()
    foreach ($tok in "-SkipCACheck:`$Req['SkipCACheck']", "-SkipCNCheck:`$Req['SkipCNCheck']", "-SkipRevocationCheck:`$Req['SkipRevocationCheck']", "-Authentication `$Req['Authentication']", "-Credential `$Req['Credential']", "-ConnectionUri `$Req['ConnectionUri']", "-ConfigurationName `$Req['ConfigurationName']") {
        if ($src.IndexOf($tok, [StringComparison]::Ordinal) -lt 0) { Add-Fail "DEFAULT_SESSION_PRIMITIVE_DROPS[$tok]" }
    }
}
Invoke-Case 'X5-01' {
    $z = 'PXSENTINEL' + [guid]::NewGuid().ToString('N'); $savedKey = [Environment]::GetEnvironmentVariable('PROXIMA_API_KEY')
    $prompt = 'line1' + [char]10 + '"q" ' + [char]92 + ' tab' + [char]9 + ' ' + [char]0xE9 + ' ' + [char]::ConvertFromUtf32(0x1F680) + [char]0 + ' end'
    $w = Start-WireServer @{ 'GET /v1/models' = @(200, '{"data":[{"id":"prov/m1"},{"id":"prov/m2"}]}'); 'POST /v1/chat/completions' = @(500, "$z-errbody") }
    try {
        [Environment]::SetEnvironmentVariable('PROXIMA_API_KEY', 'dummy-test-key'); Set-RestPort $Tg.Pos.Base $Tg.Pos.ProcId $w.Port; Set-RealHttp $true
        $x = Invoke-Px (New-PxArgs 'ask' $Tg.Pos @{ Provider = 'prov'; Value = $prompt; Model = 'prov/m1' })
        $g = Get-WireCount $w 'GET' '/v1/models'; $p = Get-WireCount $w 'POST' '/v1/chat/completions'
        if ($p -gt 1) { Add-Fail "INFERENCE_RETRIED[wire 500] posts=$p" }
        if ($g -ne 1 -or $p -ne 1 -or $w.Log.Count -ne 2) { Add-Fail "WIRE_COUNTS[500] get=$g post=$p total=$($w.Log.Count)" }
        if (-not $x.R -or "$($x.R.outcome)" -cne 'unknown' -or $x.R.dispatched -ne $true) { Add-Fail "NOT_UNKNOWN[wire 500] $($x.Id)" }
        elseif ((Get-RecordState $Tg.Pos.Base $x.R.data.recordId) -cne 'unknown') { Add-Fail 'RECORD_NOT_UNKNOWN[wire 500]' }
        if ($x.Text.Contains($z)) { Add-Fail 'ERROR_BODY_ECHOED' }
        $pr = @($w.Log | Where-Object { $_.Method -ceq 'POST' })
        if ($pr.Count) {
            $b = $pr[0].Body | ConvertFrom-Json
            if ($b.model -cne 'prov/m1' -or -not [string]::Equals([string]@($b.messages)[0].content, $prompt, [StringComparison]::Ordinal)) { Add-Fail 'BODY_NOT_VERBATIM' }
            if (@($pr[0].Headers | Where-Object { $_ -ceq 'Authorization: Bearer dummy-test-key' }).Count -ne 1) { Add-Fail 'KEY_NOT_SENT_ON_ASK' }
        }
        $w.Routes['POST /v1/chat/completions'] = @(200, '{"model":"prov/served","choices":[{"message":{"content":"wire-answer"}}]}'); $before = $w.Log.Count
        $x = Invoke-Px (New-PxArgs 'ask' $Tg.Pos @{ Provider = 'prov'; Value = 'second'; Model = 'prov/m1' })
        if (-not $x.R -or "$($x.R.outcome)" -cne 'ok' -or "$($x.R.data.requestedModel)" -cne 'prov/m1' -or "$($x.R.data.reportedModel)" -cne 'prov/served' -or "$($x.R.data.answer)" -cne 'wire-answer') { Add-Fail "WIRE_POSITIVE[$($x.Id)]" }
        if ($w.Log.Count - $before -ne 2) { Add-Fail "WIRE_COUNTS[200] $($w.Log.Count - $before)" }
    } finally { Set-RealHttp $false; Stop-WireServer $w; Set-RestPort $Tg.Pos.Base $Tg.Pos.ProcId 1; [Environment]::SetEnvironmentVariable('PROXIMA_API_KEY', $savedKey) }
    foreach ($c in @(@('timeout', { param($Req) if ($Req['Method'] -ceq 'POST') { throw [TimeoutException]::new('timeout') }; & $DefaultHttp $Req }),
            @('503', { param($Req) if ($Req['Method'] -ceq 'POST') { return @{ Status = 503; Body = 'x' } }; & $DefaultHttp $Req }))) {
        $global:PxcT.HttpHandler = $c[1]
        $x = Invoke-Px (New-PxArgs 'ask' $Tg.Pos @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' })
        $p = Get-CallCount $x 'Http:POST'; if ($p -gt 1) { Add-Fail "INFERENCE_RETRIED[mock $($c[0])] posts=$p" }
        if (-not $x.R -or "$($x.R.outcome)" -cne 'unknown' -or $p -ne 1) { Add-Fail "NOT_UNKNOWN[mock $($c[0])] $($x.Id)" }
    }
}
Invoke-Case 'X5-02' {
    $cases = @(@('case alias', 'prov', 'prov/model-x'), @('nul alias', 'prov', ('prov/m1' + [char]0)), @('turkish case alias', 'prov', 'prov/title'), @('provider prefix mismatch', 'prov', 'other/m9'),
        @('provider case alias', 'Prov', 'Prov/m1'))
    foreach ($c in $cases) {
        $x = Invoke-Px (New-PxArgs 'use' $Tg.L1 @{ Provider = $c[1]; Value = $c[2] })
        if ($x.R -or $x.StateChanged) { Add-Fail "MODEL_MATCH_NOT_ORDINAL[$($c[0])]" } else { Assert-Code $x 'ModelNotAdvertised' $c[0] }
        $x = Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = $c[1]; Value = 'p'; Model = $c[2] })
        if ($x.R -or (Get-CallCount $x 'Http:POST')) { Add-Fail "MODEL_MATCH_NOT_ORDINAL[ask $($c[0])]" }
    }
    foreach ($c in @(@('prov', 'prov/Model-X'), @('other', 'other/m9'), @('prov', 'prov/TITLE'))) { Assert-Ok (Invoke-Px (New-PxArgs 'use' $Tg.L1 @{ Provider = $c[0]; Value = $c[1] })) "exact $($c[1])" }
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'fixture connect R1'
    $x = Invoke-Px (New-PxArgs 'use' $Tg.R1 @{ Provider = 'prov'; Value = 'prov/M1' }); if ($x.R) { Add-Fail 'MODEL_MATCH_NOT_ORDINAL[remote case alias]' }
    Assert-Ok (Invoke-Px (New-PxArgs 'use' $Tg.R1 @{ Provider = 'prov'; Value = 'prov/m1' })) 'remote exact'
}
Invoke-Case 'X5-03' {
    $base = $Tg.Svc.Base; $dir = "$base\results\px-active"; $global:PxcT.UiHandler = { 0 }
    $g = @(1..3 | ForEach-Object { [guid]::NewGuid().ToString('D') })
    $subs = @(@('pending', 'stop', @{ "$($g[0]).json" = '{"state":"pending"}' }), @('unknown', 'restart', @{ "$($g[0]).json" = '{"state":"unknown"}' }),
        @('malformed', 'stop', @{ "$($g[0]).json" = '{"state":' }), @('malformed restart', 'restart', @{ "$($g[0]).json" = '[1,2' }),
        @('non-record entry', 'stop', @{ 'junk.txt' = 'x'; "$($g[1]).json" = '{"state":"completed"}' }), @('state case alias', 'stop', @{ "$($g[0]).json" = '{"state":"Completed"}' }),
        @('unreadable', 'stop', @{ "$($g[2]).json" = '{"state":"completed"}' }))
    foreach ($sub in $subs) {
        Clear-Journal $base; foreach ($k in $sub[2].Keys) { $null = Write-Fixture "$dir\$k" $sub[2][$k] }
        $lock = $(if ($sub[0] -ceq 'unreadable') { [IO.File]::Open("$dir\$($g[2]).json", 'Open', 'ReadWrite', 'None') })
        try { $x = Invoke-Px (New-PxArgs $sub[1] $Tg.Svc) } finally { if ($lock) { $lock.Dispose() } }
        if (Get-CallCount $x 'ServiceControl') { Add-Fail "PENDING_GUARD_BYPASS[$($sub[0])]" } else { Assert-Code $x 'PendingRequests' $sub[0] }
    }
    Clear-Journal $base; $null = [IO.Directory]::CreateDirectory("$base\results"); $null = New-Item -ItemType Junction -Path $dir -Value "$S\journal-target"
    $x = Invoke-Px (New-PxArgs 'stop' $Tg.Svc @{ Force = $false })
    if (Get-CallCount $x 'ServiceControl') { Add-Fail 'GUARD_ENUM_TREATED_EMPTY' } else { Assert-Code $x 'PendingGuardUnverified' 'journal junction' }
    [IO.Directory]::Delete($dir)
    Clear-Journal $base; $null = Write-Fixture "$dir\$($g[0]).json" '{"state":"pending"}'
    $x = Invoke-Px (New-PxArgs 'stop' $Tg.Svc @{ Force = $true }); Assert-Calls $x @('GetService', 'ServiceControl:Stop') 'Force overrides pending guard'
    if ($x.R -and $x.R.data.pendingOverridden -ne 1) { Add-Fail 'PENDING_OVERRIDE_NOT_REPORTED' }
    Clear-Journal $base; $null = Write-Fixture "$dir\$($g[0]).json" '{"state":"completed"}'
    Assert-Calls (Invoke-Px (New-PxArgs 'stop' $Tg.Svc)) @('GetService', 'ServiceControl:Stop') 'settled journal'
    Clear-Journal $base
}
Invoke-Case 'X5-04' {
    Clear-Journal $Tg.Svc.Base
    foreach ($u in @(@('UI present', { 0; 3 }, 'LoginUiPresent'), @('UI unknown session', { $null }, 'LoginUiPresent'), @('UI query error', { throw 'cim failure' }, 'LoginUiUnknown'))) {
        $global:PxcT.UiHandler = $u[1]
        foreach ($act in 'start', 'restart') {
            $x = Invoke-Px (New-PxArgs $act $Tg.Svc @{ Force = $true })
            if ((Get-CallCount $x 'ServiceControl') -or (Get-CallCount $x 'GetService')) { Add-Fail "UI_GUARD_BYPASS[$($u[0]) $act]" } else { Assert-Code $x $u[2] "$($u[0]) $act" }
        }
    }
    $global:PxcT.UiHandler = { 0 }; Assert-Calls (Invoke-Px (New-PxArgs 'start' $Tg.Svc)) @('UiSessions', 'GetService', 'ServiceControl:Start') 'no UI'
}
Invoke-Case 'X5-05' {
    $keepBefore = Get-TreeSnapshot $Keep -Hash; $links = [Collections.Generic.List[string]]::new()
    try {
        $null = New-Item -ItemType Junction -Path "$($Tg.J4.Base)\results" -Value $Keep; $links.Add("$($Tg.J4.Base)\results")
        $null = [IO.Directory]::CreateDirectory("$($Tg.J5.Base)\results"); $null = New-Item -ItemType Junction -Path "$($Tg.J5.Base)\results\px-active" -Value $Keep; $links.Add("$($Tg.J5.Base)\results\px-active")
        $null = [IO.Directory]::CreateDirectory("$S\gone"); $null = New-Item -ItemType Junction -Path "$($Tg.J6.Base)\results" -Value "$S\gone"; $links.Add("$($Tg.J6.Base)\results"); [IO.Directory]::Delete("$S\gone")
        foreach ($c in @(@('base inside ProtectedRoot', $Tg.In), @('results junction', $Tg.J4), @('px-active junction', $Tg.J5), @('dangling results junction', $Tg.J6))) {
            $x = Invoke-Px (New-PxArgs 'ask' $c[1] @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' })
            if (Get-CallCount $x 'Http:POST') { Add-Fail "JOURNAL_POST[$($c[0])]" } else { Assert-Code $x 'JournalUnsafe' $c[0] }
        }
        if ((Get-TreeSnapshot $Keep -Hash) -cne $keepBefore -or [IO.Directory]::Exists("$S\gone")) { Add-Fail 'OUTSIDE_CHANGED[journal followed a junction]' }
        if ([IO.Directory]::Exists("$($Tg.In.Base)\results")) { Add-Fail 'JOURNAL_CREATED_INSIDE_PROTECTED_ROOT' }
        $id = [guid]::NewGuid().ToString('D'); $occ = Write-Fixture "$($Tg.L1.Base)\results\px-active\$id.json" 'occupied'; $occSha = Get-FileSha256 $occ
        $global:PxcT.IdHandler = [scriptblock]::Create("'$id'")
        $x = Invoke-Px (New-PxArgs 'ask' $Tg.L1 @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' })
        if (Get-CallCount $x 'Http:POST') { Add-Fail 'JOURNAL_POST[GUID collision]' } else { Assert-Code $x 'JournalFailed' 'GUID collision' }
        if ((Get-FileSha256 $occ) -cne $occSha) { Add-Fail 'RECORD_OVERWRITTEN[GUID collision]' }
        [IO.File]::Delete($occ)
    } finally { foreach ($j in $links) { [IO.Directory]::Delete($j) } }
}
Invoke-Case 'X5-06' {
    $w = Start-WireServer @{ 'GET /api/status' = @(200, '{"ok":true}') }; $savedKey = [Environment]::GetEnvironmentVariable('PROXIMA_API_KEY')
    try {
        [Environment]::SetEnvironmentVariable('PROXIMA_API_KEY', 'dummy-test-key'); Set-RestPort $Tg.Pos.Base $Tg.Pos.ProcId $w.Port; Set-RealHttp $true
        $x = Invoke-Px (New-PxArgs 'status' $Tg.Pos)
        if (-not $x.R -or "$($x.R.outcome)" -cne 'ok' -or "$($x.R.data.authentication)" -cne 'not_verified_by_status') { Add-Fail "STATUS_RESULT[$($x.Id)]" }
        if ($w.Log.Count -ne 1 -or (Get-WireCount $w 'GET' '/api/status') -ne 1) { Add-Fail "WIRE_COUNTS[status] $($w.Log.Count)" }
        if (@($w.Log | ForEach-Object { $_.Headers } | Where-Object { $_ -match '^(?i)authorization:' }).Count) { Add-Fail 'STATUS_AUTH_SENT[wire]' }
        if (@($w.Log | Where-Object { $_.Method -cne 'GET' }).Count) { Add-Fail 'STATUS_POST[wire]' }
        if ((Get-CallCount $x 'GetService') + (Get-CallCount $x 'ServiceControl') + (Get-CallCount $x 'UiSessions')) { Add-Fail 'STATUS_SCM_QUERY' }
    } finally { Set-RealHttp $false; Stop-WireServer $w; Set-RestPort $Tg.Pos.Base $Tg.Pos.ProcId 1; [Environment]::SetEnvironmentVariable('PROXIMA_API_KEY', $savedKey) }
    $x = Invoke-Px (New-PxArgs 'status' $Tg.L1); Assert-Calls $x @('GetProcess', 'Http:GET /api/status') 'mock status'
    if (@($global:PxcT.HttpReqs | Where-Object { $_['Headers'].Contains('Authorization') }).Count) { Add-Fail 'STATUS_AUTH_SENT[mock]' }
}
Invoke-Case 'X5-07' {
    Clear-Journal $Tg.Svc.Base; $exe = "$($Tg.Svc.Base)\runtime\Proxima.exe"
    $bad = @(@('nssm wrapper', { [pscustomobject]@{ Name = 'ProximaGateway'; PathName = 'C:\nssm\nssm.exe' } }), @('quoted with args', { [pscustomobject]@{ Name = 'ProximaGateway'; PathName = '"' + $global:PxcT.ServiceExe + '" --service' } }),
        @('other exe', { [pscustomobject]@{ Name = 'ProximaGateway'; PathName = '"C:\other\Proxima.exe"' } }), @('name case', { [pscustomobject]@{ Name = 'proximagateway'; PathName = '"' + $global:PxcT.ServiceExe + '"' } }),
        @('other name', { [pscustomobject]@{ Name = 'ProximaGatewayX'; PathName = '"' + $global:PxcT.ServiceExe + '"' } }), @('CIM denied', { throw [UnauthorizedAccessException]::new('denied') }),
        @('two services', { $svcRow = [pscustomobject]@{ Name = 'ProximaGateway'; PathName = '"' + $global:PxcT.ServiceExe + '"' }; $svcRow; $svcRow }), @('no service', { }))
    $global:PxcT.UiHandler = { 0 }
    foreach ($b in $bad) {
        $global:PxcT.SvcHandler = $b[1]
        foreach ($act in 'start', 'stop') {
            $x = Invoke-Px (New-PxArgs $act $Tg.Svc)
            if (Get-CallCount $x 'ServiceControl') { Add-Fail "SERVICE_BINDING_BYPASS[$($b[0]) $act]" } else { Assert-Code $x 'ServiceIdentityUnverified' "$($b[0]) $act" }
        }
    }
    $global:PxcT.SvcHandler = { [pscustomobject]@{ Name = 'ProximaGateway'; PathName = $global:PxcT.ServiceExe } }
    $x = Invoke-Px (New-PxArgs 'start' $Tg.Svc)
    if ($exe.IndexOf([char]' ') -lt 0) { Assert-Calls $x @('UiSessions', 'GetService', 'ServiceControl:Start') 'unquoted without spaces' } elseif (Get-CallCount $x 'ServiceControl') { Add-Fail 'SERVICE_BINDING_BYPASS[unquoted with spaces]' }
    $global:PxcT.ServiceExe = "$($Tg.Sp.Base)\runtime\Proxima.exe"
    $x = Invoke-Px (New-PxArgs 'start' $Tg.Sp); if (Get-CallCount $x 'ServiceControl') { Add-Fail 'SERVICE_BINDING_BYPASS[unquoted with spaces]' } else { Assert-Code $x 'ServiceIdentityUnverified' 'unquoted with spaces' }
}
Invoke-Case 'X5-08' {
    $runtime = @(@('unreadable', { param($ProcId) [pscustomobject]@{ SessionId = [uint32]0; ExecutablePath = $null } }),
        @('wrong path', { param($ProcId) [pscustomobject]@{ SessionId = [uint32]0; ExecutablePath = 'C:\Windows\notepad.exe' } }),
        @('interactive session', { param($ProcId) [pscustomobject]@{ SessionId = [uint32]1; ExecutablePath = $global:PxcT.Pids["$ProcId"] } }),
        @('query error', { param($ProcId) throw 'cim failure' }), @('no process', { param($ProcId) }))
    foreach ($r in $runtime) {
        $global:PxcT.ProcHandler = $r[1]
        foreach ($a in @(@('status', @{}), @('models', @{}), @('ask', @{ Provider = 'prov'; Value = 'p'; Model = 'prov/m1' }))) {
            $x = Invoke-Px (New-PxArgs $a[0] $Tg.L1 $a[1])
            if (Get-CallCount $x 'Http:') { Add-Fail "UNVERIFIED_RUNTIME_USED[$($r[0]) $($a[0])]" } else { Assert-Code $x 'RuntimeUnverified' "$($r[0]) $($a[0])" }
        }
    }
    $global:PxcT.ProcHandler = $DefaultProc; $rp = "$($Tg.L1.Base)\profile\rest-port.json"
    $meta = @(@('port 0', '{"pid":4101,"port":0}'), @('port 65536', '{"pid":4101,"port":65536}'), @('fractional port', '{"pid":4101,"port":80.5}'), @('string port', '{"pid":4101,"port":"80"}'),
        @('negative pid', '{"pid":-1,"port":80}'), @('missing port', '{"pid":4101}'), @('exponent port', '{"pid":4101,"port":8e1}'), @('trailing garbage', '{"pid":4101,"port":80} x'), @('oversized', ('{"pid":4101,"port":80}' + (' ' * 5000))))
    try {
        foreach ($m in $meta) {
            $null = Write-Fixture $rp $m[1]; $x = Invoke-Px (New-PxArgs 'status' $Tg.L1)
            if ($x.Calls.Count) { Add-Fail "METADATA_COERCED[$($m[0])] $($x.Calls -join ';')" } else { Assert-Code $x 'GatewayMetadataInvalid' $m[0] }
        }
    } finally { Set-RestPort $Tg.L1.Base $Tg.L1.ProcId 1 }
}
Invoke-Case 'X6-01' {
    $h = Invoke-Px @{ Action = 'help' }; if (-not $h.R -or @($h.R.data).Count -lt 3) { Add-Fail 'HELP_EMPTY' }
    $x = Invoke-Px (New-PxArgs 'config' $Tg.L1); if (-not $x.R -or "$($x.R.data.basePath)" -cne $Tg.L1.Base -or $x.Calls.Count) { Add-Fail 'CONFIG_POSITIVE' }
    $x = Invoke-Px (New-PxArgs 'status' $Tg.Pos); Assert-Calls $x @('GetProcess', 'Http:GET /api/status') 'status'
    if (-not $x.R -or "$($x.R.outcome)" -cne 'ok' -or "$($x.R.mode)" -cne 'Local') { Add-Fail 'STATUS_POSITIVE' }
    $x = Invoke-Px (New-PxArgs 'models' $Tg.Pos @{ Provider = 'prov' }); Assert-Calls $x @('GetProcess', 'Http:GET /v1/models') 'models'
    if (-not $x.R -or (@($x.R.data.models) -join ',') -cne 'prov/m1,prov/m2,prov/Model-X,prov/TITLE' -or "$($x.R.data.modelState)" -cne 'advertised_not_execution_tested') { Add-Fail 'MODELS_POSITIVE' }
    $x = Invoke-Px (New-PxArgs 'use' $Tg.Pos @{ Provider = 'prov'; Value = 'prov/m2' }); Assert-Calls $x @('GetProcess', 'Http:GET /v1/models') 'use'
    if (-not $x.R -or "$($x.R.outcome)" -cne 'selected') { Add-Fail 'USE_POSITIVE' }
    $x = Invoke-Px (New-PxArgs 'ask' $Tg.Pos @{ Provider = 'prov'; Value = 'hello' }); Assert-Calls $x @('GetProcess', 'Http:GET /v1/models', 'NewId', 'Http:POST /v1/chat/completions') 'ask'
    if (-not $x.R -or "$($x.R.outcome)" -cne 'ok' -or "$($x.R.data.requestedModel)" -cne 'prov/m2' -or "$($x.R.data.reportedModel)" -cne 'prov/served' -or "$($x.R.data.answer)" -cne 'answer-text' -or "$($x.R.data.answerTrust)" -cne 'untrusted_data') { Add-Fail 'ASK_POSITIVE' }
    elseif ((Get-RecordState $Tg.Pos.Base $x.R.data.recordId) -cne 'completed') { Add-Fail 'ASK_RECORD_NOT_COMPLETED' }
    Clear-Journal $Tg.Svc.Base; $global:PxcT.UiHandler = { 0 }
    Assert-Calls (Invoke-Px (New-PxArgs 'start' $Tg.Svc)) @('UiSessions', 'GetService', 'ServiceControl:Start') 'start'
    Assert-Calls (Invoke-Px (New-PxArgs 'stop' $Tg.Svc)) @('GetService', 'ServiceControl:Stop') 'stop'
    Assert-Calls (Invoke-Px (New-PxArgs 'restart' $Tg.Svc)) @('UiSessions', 'GetService', 'ServiceControl:Restart') 'restart'
    $fp = Get-Fp $Tg.Pos
    $x = Invoke-Op @{ Action = 'status'; BasePath = $Tg.Pos.Base; TargetFingerprint = $fp; ProtectedRoot = $Repo; Confirm = $false }; Assert-Calls $x @('GetProcess', 'Http:GET /api/status') 'direct export status'
    $x = Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred }); Assert-Calls $x @('NewSession', 'InvokeRemote:handshake:1') 'connect'
    if (-not $x.R -or "$($x.R.outcome)" -cne 'connected') { Add-Fail 'CONNECT_POSITIVE' }
    $x = Invoke-Px (New-PxArgs 'status' $Tg.R1); Assert-Calls $x @('InvokeRemote:status:1') 'remote status'
    $e = $global:PxcT.Envelopes[$global:PxcT.Envelopes.Count - 1]; $keys = @($e.Keys | ForEach-Object { [string]$_ }); [Array]::Sort($keys, [StringComparer]::Ordinal)
    if (($keys -join ',') -cne 'Action,BasePath,ConfigModuleSha256,Force,Model,ModuleSha256,Prompt,ProtocolVersion,Provider,TargetFingerprint,WhatIf' -or $e['WhatIf'] -isnot [bool] -or $e['WhatIf'] -or
        $e['Force'] -isnot [bool] -or $e['ProtocolVersion'] -isnot [int] -or $e['ProtocolVersion'] -ne 1 -or "$($e['ModuleSha256'])" -cne $global:PxcT.SelfSha) { Add-Fail 'ENVELOPE_SHAPE' }
    if (-not [object]::ReferenceEquals($global:PxcT.Bodies[$global:PxcT.Bodies.Count - 1], (& $Mod { $script:EndpointBody }))) { Add-Fail 'ENDPOINT_BODY_NOT_CONSTANT' }
    Assert-Calls (Invoke-Px (New-PxArgs 'disconnect' $Tg.R1)) @('RemoveSession:1') 'disconnect'
    foreach ($run in (Get-EndpointRun).Runs) {
        $row = $(if ($run.Rep) { Get-EpRow $run 'positive-handshake' })
        if (-not $row -or -not $row.result -or "$($row.result.outcome)" -cne 'ok' -or $row.result.dryRun -ne $false -or $row.result.data.protocolVersion -ne 1 -or
            "$($row.result.data.moduleSha256)" -cne $global:PxcT.SelfSha -or "$($row.result.data.configModuleSha256)" -cne $global:PxcT.CfgSha -or $row.ambient_whatif -ne $false -or $row.received_whatif -cne 'False') {
            Add-Fail "REMOTE_PAYLOAD_POSITIVE[$($run.Exe)] rc=$($run.Rc) fqid=$(if ($row) { $row.fqid })"
        }
    }
}
Invoke-Case 'X6-02' {
    if ($TreeAfterImport -cne $TreeBeforeImport -or $UserAfterImport -cne $UserBefore) { Add-Fail 'IMPORT_SIDE_EFFECT[fixture tree or user state]' }
    Assert-Ok (Invoke-Px (New-PxArgs 'connect' $Tg.R1 @{ Credential = $Cred })) 'fixture connect R1'
    Assert-Ok (Invoke-Px (New-PxArgs 'use' $Tg.L1 @{ Provider = 'prov'; Value = 'prov/m1' })) 'fixture use L1'
    $treeSnap = Get-TreeSnapshot $S -Hash; $userSnap = Get-UserStateSnapshot; $measuredSnap = Get-TreeSnapshot $MeasuredRoot -Hash; $keepSnap = Get-TreeSnapshot $Keep -Hash
    $st = Get-ModState; $n = $global:PxcT.Calls.Count; $dry = 0
    foreach ($t in $Tg.L1, $Tg.R1, $Tg.Svc) {
        foreach ($a in 'config', 'status', 'models', 'use', 'ask', 'start', 'stop', 'restart', 'connect', 'disconnect') {
            $x = Invoke-Px (New-PxArgs $a $t @{ Provider = 'prov'; Value = 'prov/m2'; Model = 'prov/m1'; Credential = $Cred; Force = $true; WhatIf = $true })
            if ($x.R -and $x.R.dryRun -eq $true) { $dry++ }
        }
    }
    # Non-vacuous: the WhatIf matrix must reach real dry runs (a bad RepositoryRoot once made every call fail validation).
    if ($dry -lt 10) { Add-Fail "WHATIF_MATRIX_VACUOUS[dry runs=$dry]" }
    if ($global:PxcT.Calls.Count -ne $n -or (Get-ModState) -cne $st) { Add-Fail 'WHATIF_STATE_CHANGED[primitive calls or session/selection]' }
    if ((Get-TreeSnapshot $S -Hash) -cne $treeSnap -or (Get-UserStateSnapshot) -cne $userSnap -or (Get-TreeSnapshot $MeasuredRoot -Hash) -cne $measuredSnap -or (Get-TreeSnapshot $Keep -Hash) -cne $keepSnap) { Add-Fail 'WHATIF_STATE_CHANGED[fixture, user state, measured tree or outside sentinel]' }
    if ((Get-TreeSnapshot $MeasuredRoot -Hash) -cne $RepoTreeBefore) { Add-Fail 'MEASURED_TREE_CHANGED' }
    $probe = "$S\cleanup-probe"; $null = Write-Fixture "$probe\a.txt" 'a'; $null = New-Item -ItemType Junction -Path "$probe\jout" -Value $Keep
    $errs = [Collections.Generic.List[string]]::new(); Remove-OwnedTree $probe $errs
    if ($errs.Count -or [IO.Directory]::Exists($probe) -or (Get-FileSha256 "$Keep\keep.txt") -cne $KeepSha) { Add-Fail "CLEANUP_FOLLOWED_REPARSE[$($errs -join '; ')]" }
}

# ---- counterexamples: single-anchor mutants of COPIES outside the fixture tree, each rerunning this harness in a child ----
$Cx = @(@{ id = 'CX00'; file = ''; e = @(); red = @() },
    @{ id = 'CX01'; file = 'ProximaControl.psm1'; e = @('if (-not $PSCmdlet.ShouldProcess($display, $Action)) {', 'if (-not ($Force -or $PSCmdlet.ShouldProcess($display, $Action))) {'); red = @('X2-01:WHATIF_SIDE_EFFECT[use WhatIf+Force]', 'X2-01:WHATIF_SIDE_EFFECT[connect WhatIf+Force]') },
    @{ id = 'CX02'; file = 'Run-Px.ps1'; e = @('$pxArgs[''WhatIf''] = [bool]$WhatIfPreference', '$null = $WhatIfPreference'); red = @('X2-03:WRAPPER_WHATIF_LOST[wrapper status]') },
    @{ id = 'CX03'; file = 'ProximaControl.psm1'; e = @('if ([bool]$WhatIfPreference -or $v[''WhatIf'']) {', 'if ($false) {'); red = @('X2-04:ENDPOINT_WHATIF_LOST[') },
    @{ id = 'CX04'; file = 'ProximaControl.psm1'; e = @('function Get-PxcSelectionKey($Cfg, [string]$Fp) { return $Fp }', 'function Get-PxcSelectionKey($Cfg, [string]$Fp) { return [string]$Cfg.targetId }'); red = @('X3-01:SELECTION_LEAK[') },
    @{ id = 'CX05'; file = 'ProximaControl.psm1'; e = @('if ($got -cne $want[$i]) { & $fail ''EndpointCodeMismatch'' }', '$null = $got'); red = @('X4-02:HASH_BEFORE_IMPORT[') },
    @{ id = 'CX06'; file = 'ProximaControl.psm1'; e = @('try { $resp = Invoke-PxcHttp $url ''POST'' ''/v1/chat/completions'' $body 300 $true } catch { $resp = $null }',
            'try { $resp = Invoke-PxcHttp $url ''POST'' ''/v1/chat/completions'' $body 300 $true; if ($resp.Status -ge 500) { $resp = Invoke-PxcHttp $url ''POST'' ''/v1/chat/completions'' $body 300 $true } } catch { $resp = $null }'); red = @('X5-01:INFERENCE_RETRIED[wire 500]') },
    @{ id = 'CX07'; file = 'ProximaControl.psm1'; e = @('foreach ($i in $Ids) { if ([string]::Equals($i, $Model, [StringComparison]::Ordinal)) { return $true } }', 'foreach ($i in $Ids) { if ($i -eq $Model) { return $true } }'); red = @('X5-02:MODEL_MATCH_NOT_ORDINAL[case alias]') },
    @{ id = 'CX08'; file = 'ProximaControl.psm1'; e = @('} catch { return $false } # malformed/unreadable record: never settled', '} catch { return $true } # malformed/unreadable record: never settled'); red = @('X5-03:PENDING_GUARD_BYPASS[malformed]') },
    @{ id = 'CX09'; file = 'ProximaControl.psm1'; e = @('if ($ok -ne $true) { Stop-Pxc ''ServiceIdentityUnverified'' }', '$null = $ok'); red = @('X5-07:SERVICE_BINDING_BYPASS[nssm wrapper start]') },
    @{ id = 'CX10'; file = 'ProximaControl.psm1'; e = @('if ([string]::IsNullOrEmpty($exePath)) { throw ''unreadable'' }', 'if ([string]::IsNullOrEmpty($exePath)) { $exePath = $expected }'); red = @('X5-08:UNVERIFIED_RUNTIME_USED[unreadable status]') })
$Report.counterexample_ids = @($Cx | ForEach-Object { $_.id })
function Get-Kill($Rep, [string[]]$Want) {
    $hit = [Collections.Generic.List[object]]::new()
    foreach ($w in $Want) {
        $cid, $tok = $w -split ':', 2; $c = @($Rep.cases | Where-Object { $_.id -ceq $cid -and $_.outcome -ceq 'failed' -and "$($_.reason)".Contains($tok) })
        if ($c.Count) { $hit.Add([ordered]@{ want = $w; reason = "$($c[0].reason)" }) }
    }
    return , $hit
}
function Test-Counterexample($M, [int]$Rc, $Rec) {
    if (-not [IO.File]::Exists($Rec.report_path)) { throw "child report absent (rc=$Rc)" }
    $rep = [IO.File]::ReadAllText($Rec.report_path) | ConvertFrom-Json
    $state = "rc=$Rc api=$($rep.api_state) setup_error=$($rep.setup_error) cleanup=$($rep.cleanup.status) passed=$($rep.passed)/$($rep.total)"
    if ("$($rep.test_culture)" -cne $TestCulture) { throw "child measured culture '$($rep.test_culture)', parent runs $TestCulture ($state)" }
    if ("$($rep.module_sha256)" -cne $Rec.module_sha256 -or "$($rep.api_state)" -cne 'present' -or $rep.setup_error -or $rep.cleanup.status -ne 'ok') { throw "child did not measure this source cleanly ($state)" }
    if ($M.id -ceq 'CX00') {
        if ($Rc -ne 0 -or $rep.failed -or $rep.passed -ne $Ids.Count -or $rep.total -ne $Ids.Count) { throw "unmodified positive control did not pass ($state)" }
        return 'CONTROL_PASSED: unmodified copy, every mandatory ID passed, rc 0'
    }
    if ($Rc -eq 0) { throw "SURVIVED: mutant passed every case - equivalent or masked by another guard; no credit ($state)" }
    if ($Rc -ne 1) { throw "wrong exit code, no credit ($state)" }
    $hit = Get-Kill $rep $M.red; $Rec.matched = @($hit)
    if ($hit.Count -ne $M.red.Count) { throw "named behaviour missing: $(@($M.red | Where-Object { $w = $_; -not @($hit | Where-Object { $_.want -ceq $w }).Count }) -join '; ') ($state)" }
    $Rec.credited = $true; return 'KILLED: every named behavioural failure observed in the named case'
}
if ($Counterexamples) {
    foreach ($cxCase in $Cx) {
        Invoke-Case $cxCase.id -NoApi {
            if (-not $ApiPresent) { throw "API_ABSENT: counterexamples need the candidate module ($($Report.api_state))" }
            $dir = "$Evid\$($cxCase.id)"; $null = [IO.Directory]::CreateDirectory($dir)
            foreach ($f in 'ProximaControl.psm1', 'Run-Px.ps1', 'ProximaConfig.psm1') { [IO.File]::Copy("$ModDir\$f", "$dir\$f") }
            if ($cxCase.file) {
                $src = [IO.File]::ReadAllText("$dir\$($cxCase.file)")
                for ($i = 0; $i -lt $cxCase.e.Count; $i += 2) {
                    $at = $src.IndexOf($cxCase.e[$i], [StringComparison]::Ordinal)
                    if ($at -lt 0 -or $src.IndexOf($cxCase.e[$i], $at + 1, [StringComparison]::Ordinal) -ge 0) { throw "ANCHOR: mutation anchor absent or not unique: $($cxCase.e[$i])" }
                    $src = $src.Substring(0, $at) + $cxCase.e[$i + 1] + $src.Substring($at + $cxCase.e[$i].Length)
                }
                [IO.File]::WriteAllText("$dir\$($cxCase.file)", $src, $Utf8)
            }
            $cs = "$S\cx\$($cxCase.id)"; $null = [IO.Directory]::CreateDirectory($cs)
            # Report/output/record sit NEXT TO the source copy: the child measures $dir byte-for-byte and rejects outputs inside it.
            $ev = "$Evid\$($cxCase.id)"
            $argv = @('-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-ModulePath', "$dir\ProximaControl.psm1", '-ScratchRoot', $cs, '-ReportPath', "$ev.report.json", '-TestCulture', $TestCulture)
            $c = Invoke-ChildPs $SelfExe $argv "counterexample $($cxCase.id)"; [IO.File]::WriteAllText("$ev.output.txt", "$($c.Run.out)", $Utf8)
            $rec = [ordered]@{ id = $cxCase.id; mutated_file = $cxCase.file; anchor = $(if ($cxCase.e.Count) { $cxCase.e[0] }); replacement = $(if ($cxCase.e.Count) { $cxCase.e[1] }); command = @($SelfExe) + $argv; rc = $c.Run.rc
                module_sha256 = (Get-FileSha256 "$dir\ProximaControl.psm1"); wrapper_sha256 = (Get-FileSha256 "$dir\Run-Px.ps1"); config_module_sha256 = (Get-FileSha256 "$dir\ProximaConfig.psm1")
                report_path = "$ev.report.json"; report_sha256 = (Get-FileSha256 "$ev.report.json"); output_path = "$ev.output.txt"; output_sha256 = (Get-FileSha256 "$ev.output.txt")
                required = $cxCase.red; matched = @(); credited = $false; verdict = $null }
            $Report.counterexample_evidence.Add($rec)
            try { $rec.verdict = Test-Counterexample $cxCase $c.Run.rc $rec } catch { $rec.verdict = "NOT_ACCEPTED: $($_.Exception.Message)"; throw }
            finally { [IO.File]::WriteAllText("$ev.record.json", ($rec | ConvertTo-Json -Depth 6), $Utf8) }
        }
    }
}
$required = @($Ids) + @($(if ($Counterexamples) { $Report.counterexample_ids }))
$Report.required_ids = $required
$missing = @($required | Where-Object { $i = $_; @($Results | Where-Object { $_.id -ceq $i }).Count -ne 1 })
if ($missing.Count) { throw "IDs not executed exactly once: $($missing -join ',')" }
$notPassed = @($Results | Where-Object { $required -ccontains $_.id -and $_.outcome -ne 'passed' })
$finalRc = $(if (@(Get-OutcomeIds 'setup_error').Count) { 2 } elseif ($notPassed.Count) { 1 } else { 0 })
Complete-Run $finalRc
