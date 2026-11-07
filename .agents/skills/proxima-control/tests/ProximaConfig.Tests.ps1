# ProximaConfig.Tests.ps1 - wp1271 r2 focused harness for Read-ProximaConfig; self-contained, no Pester.
# The SAME harness and ID set run on any tree via explicit -ModulePath (baseline or candidate), e.g.
#   powershell.exe|pwsh.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File <copy>\ProximaConfig.Tests.ps1 `
#     -ModulePath <tree>\.agents\skills\proxima-control\scripts\ProximaConfig.psm1 `
#     -ScratchRoot <existing long-name dir outside the tree> -ReportPath <json outside the tree> [-Counterexamples]
# rc 0: every mandatory ID ran once and passed. rc 1: a case failed; an absent module/API fails each case with
# API_ABSENT and every case still executes. rc 2: setup error, never a test outcome. -Counterexamples mutates
# COPIES of module/sample under ScratchRoot and requires each mutant to fail the named case for the named reason.
[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$ModulePath, [Parameter(Mandatory = $true)][string]$ScratchRoot,
    [string]$ReportPath = '', [string]$RepositoryRoot = '', [string]$SamplePath = '', [switch]$Counterexamples)
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$Ids = 'A1-01', 'A2-01', 'A2-02', 'A2-03', 'A2-04', 'A2-05', 'A2-06', 'A2-07', 'A3-01', 'A3-02', 'A3-03', 'A3-04', 'A4-01', 'A5-01', 'A5-02', 'A6-01', 'A6-02', 'A5-03'
$Results = [Collections.Generic.List[object]]::new()
$Report = [ordered]@{ schema = 'proxima_config_tests.v1'; ps_version = "$($PSVersionTable.PSVersion)"; ps_edition = "$($PSVersionTable.PSEdition)"
    module_path = $ModulePath; module_sha256 = $null; sample_sha256 = $null; harness_sha256 = $null; api_state = 'unknown'
    setup_error = $null; total = 0; passed = 0; failed = 0; failed_ids = @(); cases = $Results }
$Utf8 = [Text.UTF8Encoding]::new($false); $Sha = [Security.Cryptography.SHA256]::Create()
function Hash([string]$P) { if ($P -and [IO.File]::Exists($P)) { ([BitConverter]::ToString($Sha.ComputeHash([IO.File]::ReadAllBytes($P))) -replace '-').ToLowerInvariant() } }
function Finish([int]$Rc) {
    $Report.failed_ids = @($Results | Where-Object outcome -eq 'failed' | ForEach-Object id)
    $Report.total = $Results.Count; $Report.failed = $Report.failed_ids.Count; $Report.passed = $Report.total - $Report.failed
    $Report.harness_sha256 = Hash $PSCommandPath; $Report.module_sha256 = Hash $ModulePath; $Report.sample_sha256 = Hash $SamplePath
    if ($ReportPath) { [IO.File]::WriteAllText($ReportPath, ($Report | ConvertTo-Json -Depth 4), $Utf8) }
    Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; api_state={3}; setup_error={4}; rc={5}' -f $Report.passed, $Report.total, ($Report.failed_ids -join ','), $Report.api_state, $Report.setup_error, $Rc)
    exit $Rc
}
trap { $Report.setup_error = "$($_.Exception.Message)"; Write-Host "SETUP_ERROR $($Report.setup_error)"; Finish 2 }
# ---- setup: any failure here is rc 2 ----
if ([Environment]::OSVersion.Platform -ne 'Win32NT') { throw 'Windows host required' }
$ModulePath = [IO.Path]::GetFullPath($ModulePath); $Report.module_path = $ModulePath; $ModuleDir = Split-Path -Parent $ModulePath
if (-not $RepositoryRoot) { $RepositoryRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ModuleDir))) }
if (-not $SamplePath) { $SamplePath = Join-Path (Split-Path -Parent $ModuleDir) 'config.example.json' }
$RepositoryRoot = [IO.Path]::GetFullPath($RepositoryRoot).TrimEnd('\'); $SamplePath = [IO.Path]::GetFullPath($SamplePath)
foreach ($p in $ScratchRoot, $ReportPath) {
    if ($p -and [IO.Path]::GetFullPath($p).StartsWith($RepositoryRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'ScratchRoot/ReportPath must be outside the measured tree' }
}
if (-not [IO.Directory]::Exists($ScratchRoot)) { throw 'ScratchRoot must be an existing directory' }
$S = [IO.Path]::GetFullPath($ScratchRoot).TrimEnd('\') + '\pxcfg-' + [guid]::NewGuid().ToString('N').Substring(0, 12)
foreach ($d in 'repo\cfg', 'repo-sibling', 'ext1', 'ext2', 'cx') { $null = [IO.Directory]::CreateDirectory("$S\$d") }
foreach ($j in @('jn', 'ext1'), @('jin', 'repo\cfg'), @('repojn', 'repo')) { $null = New-Item -ItemType Junction -Path "$S\$($j[0])" -Value "$S\$($j[1])" }
function Snap([string]$Root, [switch]$Meta) {
    if (-not [IO.Directory]::Exists($Root)) { return 'absent' }
    $rows = foreach ($p in [IO.Directory]::GetFileSystemEntries($Root, '*', [IO.SearchOption]::AllDirectories)) {
        if (-not [IO.File]::Exists($p)) { "$p|dir" } elseif ($Meta) { $f = [IO.FileInfo]::new($p); "$p|$($f.Length)|$($f.LastWriteTimeUtc.Ticks)" } else { "$p|$(Hash $p)" } }
    return (@($rows) | Sort-Object) -join "`n"
}
function EnvSnap { (@([Environment]::GetEnvironmentVariables().GetEnumerator() | Sort-Object Name | ForEach-Object { if (-not "$($_.Name)".StartsWith('=')) { "$($_.Name)=$($_.Value)" } })) -join "`n" }
$EnvBefore = EnvSnap; $RepoBefore = Snap $RepositoryRoot -Meta
# Scoped side-effect sentinels: global functions shadow these cmdlets for the module from here on; each call is
# recorded and throws. The harness itself uses only .NET calls below this line.
$global:PxHits = [Collections.Generic.List[string]]::new()
$Sentinels = 'Invoke-WebRequest', 'Invoke-RestMethod', 'New-PSSession', 'Enter-PSSession', 'Invoke-Command', 'Start-Process', 'Start-Job', 'New-Item',
'Set-Content', 'Add-Content', 'Out-File', 'Set-Item', 'Set-ItemProperty', 'New-ItemProperty', 'Remove-Item', 'Copy-Item', 'Move-Item', 'Rename-Item',
'New-Service', 'Set-Service', 'Start-Service', 'Register-ScheduledTask', 'Set-Acl', 'Add-Type', 'Test-Connection', 'Test-NetConnection', 'Resolve-DnsName', 'Export-Clixml'
. ([scriptblock]::Create((($Sentinels | ForEach-Object { "function global:$_ { `$global:PxHits.Add('$_'); throw 'PX_SENTINEL $_' }" }) -join "`n")))
$Forbidden = $Sentinels + @('WebClient', 'HttpClient', 'WebRequest', 'Sockets', 'Diagnostics.Process', 'WriteAll', 'AppendAll',
    'File]::Create', 'File]::Open', 'FileStream', 'StreamWriter', 'Import-Module', 'using module', '$env:', 'Environment]::')
$ApiPresent = $false; $ImportHits = 0; $Exported = @(); $Report.api_state = 'module_absent'
if ([IO.File]::Exists($ModulePath)) {
    $h0 = $global:PxHits.Count
    try { $mod = Import-Module -Name $ModulePath -Force -PassThru -DisableNameChecking }
    catch { throw "existing module failed to import (sentinel hits: $($global:PxHits.Count - $h0))" }
    $ImportHits = $global:PxHits.Count - $h0; $Exported = @($mod.ExportedCommands.Keys)
    $ApiPresent = $Exported -contains 'Read-ProximaConfig'
    $Report.api_state = $(if ($ApiPresent) { 'present' } else { 'module_without_api' })
}
function Cwd([string]$P) { Set-Location -LiteralPath $P; [Environment]::CurrentDirectory = $P }
function Put([string]$Rel, $Content) { $p = "$S\$Rel"; if ($Content -is [byte[]]) { [IO.File]::WriteAllBytes($p, $Content) } else { [IO.File]::WriteAllText($p, $Content, $Utf8) }; $p }
# JSON fixture from raw value tokens: a valid Local (or -Remote) config with fields replaced/added/dropped.
function Obj([hashtable]$Set = @{}, [string[]]$Drop = @(), [switch]$Remote) {
    $m = [ordered]@{ schemaVersion = '1'; targetId = '"tgt-one"'; mode = '"Local"'; basePath = '"C:\\px1"' }
    if ($Remote) { $m.targetId = '"tgt-two"'; $m.mode = '"Remote"'; $m.connectionUri = '"https://gw.example.invalid:5986/wsman"'; $m.configurationName = '"px.endpoint"' }
    foreach ($k in $Set.Keys) { $m[$k] = $Set[$k] }
    foreach ($k in $Drop) { $m.Remove($k) }
    return '{' + (@($m.Keys | ForEach-Object { '"' + $_ + '":' + $m[$_] }) -join ',') + '}'
}
# One guarded read: scratch tree bytes and sentinel count must not change; every error text is collected.
function R([string]$Cfg, [string]$Repo = "$S\repo") {
    $before = Snap $S; $hits = $global:PxHits.Count; $global:Error.Clear(); $o = $null; $e = $null
    try { $o = Read-ProximaConfig -ConfigPath $Cfg -RepositoryRoot $Repo } catch { $e = $_ }
    if ((Snap $S) -cne $before) { throw 'filesystem tree/bytes changed during read' }
    if ($global:PxHits.Count -ne $hits) { throw 'side-effect sentinel hit during read' }
    $text = @(@($global:Error) + @($e) | Where-Object { $_ } | ForEach-Object { ($_ | Format-List * -Force | Out-String) + "$_" +
            $(if ($_ -is [Management.Automation.ErrorRecord]) { $_.Exception | Format-List * -Force | Out-String }) }) -join "`n"
    return [pscustomobject]@{ Out = $o; Err = $e; Text = $text }
}
function Rej($X, [string]$Code, [string]$Label) {
    $id = $(if ($X.Err) { $X.Err.FullyQualifiedErrorId } else { '<none>' })
    if ($null -ne $X.Out) { throw "accepted invalid input [$Label]" }
    if (-not $X.Err -or ($Code -and $id -notmatch "^ProximaConfig\.$Code(,|\z)")) { throw "expected ProximaConfig.$Code, got $id [$Label]" }
}
function Case([string]$Id, [string[]]$Needs, [scriptblock]$Body) {
    $why = $null
    try {
        if ($Needs -contains 'api' -and -not $ApiPresent) { throw "API_ABSENT: Read-ProximaConfig not available from ModulePath ($($Report.api_state))" }
        if ($Needs -contains 'module' -and -not [IO.File]::Exists($ModulePath)) { throw 'API_ABSENT: module file absent' }
        if ($Needs -contains 'sample' -and -not [IO.File]::Exists($SamplePath)) { throw 'API_ABSENT: sample file absent' }
        Cwd $S; & $Body
    } catch { $why = "$($_.Exception.Message)" } finally { Cwd $S }
    $Results.Add([pscustomobject]@{ id = $Id; outcome = $(if ($null -eq $why) { 'passed' } else { 'failed' }); reason = $why })
    Write-Host $(if ($null -eq $why) { "PASS $Id" } else { "FAIL $Id :: $why" })
}
$SampleExpect = [ordered]@{ schemaVersion = 1; targetId = 'example-target'; mode = 'Remote'; basePath = 'C:\ProximaExample'
    connectionUri = 'https://gateway.example.invalid:5986/wsman'; configurationName = 'Example.Endpoint' }
# ---- cases (mandatory IDs; A5-03 runs last so it sees every read) ----
Case 'A1-01' api {
    $a = Put 'ext1\a.json' (Obj); $b = Put 'ext2\b.json' (Obj -Remote)
    Cwd "$S\ext2"; $r1 = R $a; Cwd "$S\ext1"; $r2 = R $b; Cwd "$S\repo"; $r3 = R $a
    foreach ($r in $r1, $r2, $r3) { if ($null -eq $r.Out) { throw "valid external config rejected: $(if ($r.Err) { $r.Err.FullyQualifiedErrorId })" } }
    if ((@($r1.Out.PSObject.Properties.Name) -join ',') -cne 'schemaVersion,targetId,mode,basePath' -or $r1.Out.schemaVersion -ne 1 -or
        $r1.Out.targetId -cne 'tgt-one' -or $r1.Out.mode -cne 'Local' -or $r1.Out.basePath -cne 'C:\px1') { throw 'Local target values/properties wrong' }
    if ((@($r2.Out.PSObject.Properties.Name) -join ',') -cne 'schemaVersion,targetId,mode,basePath,connectionUri,configurationName' -or
        $r2.Out.targetId -cne 'tgt-two' -or $r2.Out.mode -cne 'Remote' -or $r2.Out.connectionUri -cne 'https://gw.example.invalid:5986/wsman' -or
        $r2.Out.configurationName -cne 'px.endpoint') { throw 'Remote target values/properties wrong' }
    if ($r3.Out.targetId -cne 'tgt-one') { throw 'result depends on the current directory' }
}
Case 'A2-01' api {
    $m = "$S\ext1\missing.json"; Rej (R $m) 'NotFound' 'missing config'
    if ([IO.File]::Exists($m)) { throw 'missing config was synthesized on disk' }
    Rej (R (Put 'ext1\a.json' (Obj)) "$S\nope") 'RepositoryRootNotFound' 'missing repository root'
}
Case 'A2-02' api {
    $bad = '', '{', '{"schemaVersion":1,}', ((Obj) + ' x'), "{'schemaVersion':1}", '{"schemaVersion":01}', '{"targetId":"a\q"}',
    "// c`n{}", '{"schemaVersion":NaN}', '{"a":1 "b":2}', '{"a":"x', [byte[]](0xEF, 0xBB, 0xBF)
    $i = 0; foreach ($j in $bad) { $i++; Rej (R (Put 'ext1\m.json' $j)) 'MalformedJson' "malformed#$i" }
    Rej (R (Put 'ext1\m.json' ([byte[]](0x7B, 0x22, 0x61, 0x22, 0x3A, 0x22, 0xC3, 0x28, 0x22, 0x7D)))) 'Encoding' 'invalid utf-8'
}
Case 'A2-03' api { $i = 0; foreach ($j in '1', '"x"', '[]', '[{}]', 'null', 'true') { $i++; Rej (R (Put 'ext1\m.json' $j)) 'NotObject' "nonobject#$i" } }
Case 'A2-04' api {
    $bad = [ordered]@{ schemaVersion = '"1"', '1.0', '2', 'true', 'null', '1e0', '[1]'; targetId = '5', '""', '"   "', '["t"]', '{}', '"bad id"', '"a/b"'
        mode = '"local"', '"Hybrid"', '1', '""'; basePath = '"px\\rel"', '"C:px"', '"\\\\srv\\share"', '"\\px"', '"C:\\a\\..\\b"', '"C:/a"', '""', '"C:\\a\\"' }
    foreach ($f in $bad.Keys) {
        foreach ($v in $bad[$f]) {
            $r = R (Put 'ext1\t.json' (Obj @{ $f = $v })); Rej $r 'InvalidField' "$f=$v"
            if ($r.Err.Exception.Message -notlike "*Field: $f.*") { throw "error does not name field $f" }
        }
        Rej (R (Put 'ext1\t.json' (Obj -Drop $f))) 'InvalidField' "missing $f"
    }
}
Case 'A2-05' api {
    Rej (R (Put 'ext1\u.json' (Obj @{ extra = '1' }))) 'UnknownField' 'unknown field'
    Rej (R (Put 'ext1\u.json' ('{"schemaVersion":1,' + (Obj).Substring(1)))) 'DuplicateField' 'duplicate field'
    Rej (R (Put 'ext1\u.json' ((Obj) -creplace '"mode"', '"Mode"'))) 'UnknownField' 'case-variant key'
}
Case 'A2-06' api {
    Rej (R (Put 'ext1\x.json' (Obj @{ connectionUri = '"https://gw.example.invalid/"' }))) 'ModeMismatch' 'Local+connectionUri'
    Rej (R (Put 'ext1\x.json' (Obj @{ configurationName = '"px.endpoint"' }))) 'ModeMismatch' 'Local+configurationName'
    foreach ($f in 'connectionUri', 'configurationName') { Rej (R (Put 'ext1\x.json' (Obj -Remote -Drop $f))) 'InvalidField' "Remote without $f" }
    foreach ($u in 'http://gw.example.invalid/wsman', 'https:/gw', '/wsman', 'gw.example.invalid:5986', 'https://u:p@gw.example.invalid/',
        'https://gw.example.invalid/?a=1', 'https://gw.example.invalid/#f', 'https://gw x.invalid/', 'HTTPS://gw.example.invalid/', 'https://') {
        Rej (R (Put 'ext1\x.json' (Obj -Remote @{ connectionUri = '"' + $u + '"' }))) 'InvalidField' "uri $u"
    }
}
Case 'A2-07' api {
    $a = Put 'ext1\a.json' (Obj)
    $cfg = 'ext1\a.json', ($a.Substring(0, 2) + $a.Substring(3)), $a.Substring(2), ('\\localhost\' + $a[0] + '$' + $a.Substring(2)), ('\\?\' + $a),
    "$S\ext1\..\ext1\a.json", "$S\ext1\.\a.json", $a.Replace('\', '/'), "$($a):s", "$a.", "$a ", "$S\ext1\"
    foreach ($p in $cfg) { Rej (R $p) 'ConfigPathInvalid' "ConfigPath $p" }
    Rej (R "$S\ext1") 'NotAFile' 'directory as ConfigPath'
    foreach ($q in 'repo', ($S.Substring(0, 2) + $S.Substring(3) + '\repo'), "$S\repo\", '\\localhost\x\repo') { Rej (R $a $q) 'RepositoryRootInvalid' "RepositoryRoot $q" }
    Rej (R '') '' 'empty ConfigPath'
}
Case 'A3-01' api { Rej (R (Put 'repo\cfg\in.json' (Obj))) 'InsideRepository' 'config inside repository' }
Case 'A3-02' api {
    $in = Put 'repo\cfg\in.json' (Obj)
    Rej (R ($S + '\REPO\CFG\IN.JSON')) 'InsideRepository' 'case-variant config path'
    Rej (R $in ($S + '\Repo')) 'InsideRepository' 'case-variant repository root'
}
Case 'A3-03' api {
    $r = R (Put 'repo-sibling\ok.json' (Obj))
    if ($null -eq $r.Out -or $r.Out.targetId -cne 'tgt-one') { throw "same-prefix sibling outside repository rejected: $(if ($r.Err) { $r.Err.FullyQualifiedErrorId })" }
}
Case 'A3-04' api {
    $null = Put 'ext1\a.json' (Obj); $null = Put 'repo\cfg\in.json' (Obj)
    Rej (R "$S\jn\a.json") 'ReparsePoint' 'junction ancestor'
    Rej (R "$S\jin\in.json") 'ReparsePoint' 'junction into repository'
    Rej (R "$S\ext1\a.json" "$S\repojn") 'ReparsePoint' 'junction repository root'
}
Case 'A4-01' api {
    $z = 'PXSENTINEL' + [guid]::NewGuid().ToString('N'); $q = '"' + $z + '"'
    $all = @(@('SecretField', (Obj @{ password = $q })), @('SecretField', (Obj @{ apiToken = $q })), @('SecretField', (Obj @{ Client_Secret = $q })),
        @('SecretField', (Obj @{ cookie = $q })), @('SecretField', (Obj @{ credential = '{"u":' + $q + '}' })), @('UnknownField', (Obj @{ notes = $q })),
        @('InvalidField', (Obj @{ targetId = '"' + $z + ' x"' })), @('InvalidField', (Obj @{ mode = $q })),
        @('InvalidField', (Obj -Remote @{ connectionUri = '"https://u:' + $z + '@gw.example.invalid/"' })),
        @('MalformedJson', ('{"targetId":' + $q + ',')), @('NotObject', $q))
    foreach ($c in $all) {
        $r = R (Put 'ext1\s.json' $c[1]); Rej $r $c[0] $c[0]
        if ($r.Text -notlike '*ProximaConfig*') { throw 'error text was not captured' }
        if ($r.Text.Contains($z)) { throw "error text contains sentinel value [$($c[0])]" }
    }
}
Case 'A5-01' module {
    $src = [IO.File]::ReadAllText($ModulePath)
    $hit = @($Forbidden | Where-Object { $src.IndexOf($_, [StringComparison]::OrdinalIgnoreCase) -ge 0 })
    if ($hit.Count) { throw "forbidden side-effect token(s) in module: $($hit -join ', ')" }
}
Case 'A5-02' api {
    if ($ImportHits -ne 0) { throw "import hit $ImportHits side-effect sentinel(s)" }
    if (($Exported -join ',') -cne 'Read-ProximaConfig') { throw "unexpected exports: $($Exported -join ',')" }
    $p = (Get-Command Read-ProximaConfig).Parameters
    foreach ($n in 'ConfigPath', 'RepositoryRoot') { if (-not @($p[$n].Attributes | Where-Object { $_ -is [Parameter] -and $_.Mandatory }).Count) { throw "$n is not mandatory" } }
}
Case 'A6-01' sample {
    $raw = [IO.File]::ReadAllText($SamplePath); $v = $raw | ConvertFrom-Json; $names = @($v.PSObject.Properties.Name)
    if (($names -join ',') -cne (@($SampleExpect.Keys) -join ',')) { throw "sample fields differ from schema: $($names -join ',')" }
    foreach ($k in $SampleExpect.Keys) { if ("$($v.$k)" -cne "$($SampleExpect[$k])") { throw "sample value of $k is not the expected placeholder" } }
    if ($v.schemaVersion -is [string] -or $raw -cnotmatch '"schemaVersion"\s*:\s*1\s*,') { throw 'sample schemaVersion is not integer 1' }
}
Case 'A6-02' api, sample {
    $r = R (Put 'ext2\sample-copy.json' ([IO.File]::ReadAllBytes($SamplePath)))
    if ($null -eq $r.Out) { throw "explicit external copy of the sample rejected: $(if ($r.Err) { $r.Err.FullyQualifiedErrorId })" }
    foreach ($k in $SampleExpect.Keys) { if ("$($r.Out.$k)" -cne "$($SampleExpect[$k])") { throw "reader returned an unexpected $k for the sample copy" } }
    Rej (R $SamplePath $RepositoryRoot) 'InsideRepository' 'sample read in place'
    if ([IO.File]::ReadAllText($ModulePath) -match 'example') { throw 'module references the sample (implicit fallback)' }
}
Case 'A5-03' api {
    if ($global:PxHits.Count) { throw "side-effect sentinel hits: $($global:PxHits -join ',')" }
    if ((EnvSnap) -cne $EnvBefore) { throw 'environment variables changed' }
    if ((Snap $RepositoryRoot -Meta) -cne $RepoBefore) { throw 'repository tree changed' }
}
# ---- counterexamples: mutate scratch COPIES only, rerun this harness in a child, require the named kill ----
$Default = 'return [pscustomobject]@{ schemaVersion = 1; targetId = ''tgt-default''; mode = ''Local''; basePath = ''C:\px0'' }'
$Cx = @(@{ n = 'default-config'; f = 'm'; e = @('$repo = Resolve-PxEntry', "$Default; `$repo = Resolve-PxEntry"); red = @('A1-01:Local target') },
    @{ n = 'synthesize-missing'; f = 'm'; e = @('$file = Resolve-PxEntry', "if (-not [IO.File]::Exists(`$ConfigPath)) { $Default }; `$file = Resolve-PxEntry"); red = @('A2-01:accepted invalid') },
    @{ n = 'accept-wrong-type'; f = 'm'; e = @(' -or $o[$Name].K -cne $Kind', ''); red = @('A2-04:accepted invalid') },
    @{ n = 'textual-prefix'; f = 'm'; e = @('$file.FullName.StartsWith($repoPrefix, [StringComparison]::OrdinalIgnoreCase)',
            '$ConfigPath.StartsWith($RepositoryRoot, [StringComparison]::Ordinal)'); red = @('A3-02:accepted invalid', 'A3-03:sibling') },
    @{ n = 'accept-reparse'; f = 'm'; e = @('if (($e.Attributes -band $script:BadAttr) -ne 0) { Stop-Px ReparsePoint }', ''); red = @('A3-04:accepted invalid') },
    @{ n = 'allow-unknown'; f = 'm'; e = @('Stop-Px SecretField', '', 'Stop-Px UnknownField', ''); red = @('A2-05:accepted invalid', 'A4-01:accepted invalid') },
    @{ n = 'echo-raw'; f = 'm'; e = @('$msg = "Config rejected: $Code."', '$msg = "Config rejected: $Code." + $Field',
            '(New-PxError $code $field)', '(New-PxError $code ([string]$text))'); red = @('A4-01:sentinel') },
    @{ n = 'side-effect'; f = 'm'; e = @('$repo = Resolve-PxEntry', 'Invoke-WebRequest -Uri https://side-effect.invalid/ -UseBasicParsing | Out-Null; $repo = Resolve-PxEntry'); red = @('A5-03:sentinel') },
    @{ n = 'sample-secret'; f = 's'; e = @('"configurationName"', '"password": "x", "configurationName"'); red = @('A6-01:sample fields') },
    @{ n = 'sample-version'; f = 's'; e = @('"schemaVersion": 1', '"schemaVersion": 2'); red = @('A6-01:schemaVersion') })
if ($Counterexamples) {
    $exe = [Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
    foreach ($m in $Cx) {
        Case "CX-$($m.n)" none {
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
$rc = $(if (@($Results | Where-Object outcome -eq 'failed').Count) { 1 } else { 0 })
Cwd ([IO.Path]::GetFullPath($ScratchRoot))
if ($rc -eq 0) { foreach ($j in 'jn', 'jin', 'repojn') { [IO.Directory]::Delete("$S\$j") }; [IO.Directory]::Delete($S, $true) } else { Write-Host "scratch kept for evidence: $S" }
Finish $rc
