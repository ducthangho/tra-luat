# ProximaControl.psm1 - wp1279 r2 (PROXIMA-P1-S2). Explicit-target control surface over ONE S1-validated Proxima config:
# px (client) and Invoke-ProximaOperation (endpoint). No discovery, defaults, CWD/environment target lookup, Get-PSSession
# adoption, autoconnect or fallback. Not exposed by SKILL/manifest until S3; imported directly from this .psm1.
# - Dependency: sibling ProximaConfig.psm1 (S1), SHA256 pinned below and verified BEFORE it is imported; it is invoked only
#   through the pinned module object. Internal coupling (declared): S1 PRIVATE helpers Test-PxPathSyntax, Open-PxChain,
#   Assert-PxOutside, Get-PxNode, Test-PxChild and the strict JSON reader run inside that pinned module scope. S1 is not modified.
# - Every business action re-reads the config and requires Ordinal targetId equality. Target fingerprint = SHA256 of a
#   fixed-order, length-prefixed UTF-8 encoding of all validated fields (missing != empty); it keys sessions and model
#   selection (Ordinal). Only its first 12 hex digits are displayed; it is routing correlation, not a credential.
# - ShouldProcess precedes EVERY effect: queries (status/models included), selection change, session, credential use,
#   journal, process, service and network. WhatIf (explicit or ambient) wins over -Confirm:$false and -Force; -Force only
#   overrides the pending-request guard of stop/restart. Approved inner calls suppress duplicate confirmation only after it.
# - State is session-only, in THIS module instance: sessions and selections are lost in a new process and when the module is
#   removed or re-imported (OnRemove releases owned sessions only). Nothing is written to config/settings/profile.
# - Remote requests are DATA (fixed key/type set) run by one constant endpoint scriptblock. Hashes bind compatibility; they
#   are not server attestation or hostile-endpoint security. Hash-then-import is a declared race.
# - Backend primitives (session, remote invoke, HTTP, CIM, service, id) live in a private table that only an isolated test
#   harness replaces through module scope. There is no public callback/executor.
# - Model ids: an advertised id belongs to provider P only if it starts with 'P/' (Ordinal) and is advertised verbatim.
# Not proven: runtime provenance/version/quota, real WinRM auth, model identity (answers are untrusted data), installed
# service wrapper layouts (NSSM and the like fail closed), admin ABA races, outward junctions elsewhere in a repository.
# Remote ProtectedRoot protects only the deployed control tree. Completed journal records are kept (no housekeeping).
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$script:Protocol = 1
$script:ConfigSha = '59abfa860e59af7c596a9e3f60829f8dc1af4a853c5d4ac197c00cc033d76e7d'
$script:IdFields = @('schemaVersion', 'targetId', 'mode', 'basePath', 'connectionUri', 'configurationName')
$script:PxActions = [Collections.Generic.HashSet[string]]::new([string[]]@('help', 'config', 'status', 'models', 'use', 'ask', 'start', 'stop', 'restart', 'connect', 'disconnect'), [StringComparer]::Ordinal)
$script:OpActions = [Collections.Generic.HashSet[string]]::new([string[]]@('status', 'models', 'ask', 'start', 'stop', 'restart', 'handshake'), [StringComparer]::Ordinal)
$script:Sessions = [Collections.Generic.Dictionary[string, object]]::new([StringComparer]::Ordinal)
$script:Selection = [Collections.Generic.Dictionary[string, object]]::new([StringComparer]::Ordinal)
$script:Orphans = [Collections.Generic.List[object]]::new()
$script:Utf8 = [Text.UTF8Encoding]::new($false, $true)
$script:BadAttr = 0x441400
$script:ReGuid = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\z'
$script:ReRecord = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.json\z'
$script:Help = @('px help', 'px config|status|start|stop|restart|connect|disconnect -ConfigPath <file> -RepositoryRoot <dir> -TargetId <id> [-Credential <PSCredential>] [-Force]',
    'px models [<provider>] -ConfigPath ... -RepositoryRoot ... -TargetId ...', 'px use <provider> <provider/model> -ConfigPath ... -RepositoryRoot ... -TargetId ...',
    'px ask <provider> <prompt> [-Model <provider/model>] -ConfigPath ... -RepositoryRoot ... -TargetId ...', 'Every action supports -WhatIf and -Confirm.')

function Get-PxcSha256([byte[]]$Bytes) {
    $h = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($h.ComputeHash($Bytes)) -replace '-', '').ToLowerInvariant() } finally { $h.Dispose() }
}
# Codes are constant identifiers; messages never carry values, paths, bodies or inner errors.
function New-PxcError([string]$Code) {
    if ($Code -cnotmatch '^[A-Za-z]{1,40}\z') { $Code = 'Internal' }
    return [Management.Automation.ErrorRecord]::new([InvalidOperationException]::new("ProximaControl: operation rejected: $Code."), "ProximaControl.$Code", 'InvalidOperation', $null)
}
function Stop-Pxc([string]$Code) { $ex = [Exception]::new("ProximaControl.$Code"); $ex.Data['PxcCode'] = $Code; throw $ex }
# Runs one step; any failure that is not already a ProximaControl code becomes $PxcStepCode (inner text discarded).
function Invoke-PxcStep([string]$PxcStepCode, [scriptblock]$PxcStepBody) {
    try { & $PxcStepBody } catch { if ($_.Exception.Data.Contains('PxcCode')) { throw }; Stop-Pxc $PxcStepCode }
}
function Resolve-PxcError($Err) {
    if ($Err.Exception.Data.Contains('PxcCode')) { return (New-PxcError ([string]$Err.Exception.Data['PxcCode'])) }
    if ([string]$Err.FullyQualifiedErrorId -clike 'ProximaConfig.*' -and $Err.Exception.Message -clike 'ProximaConfig: *') { return $Err }
    return (New-PxcError 'Internal')
}

# ---- dependency: S1 verified by hash BEFORE import, then used only through the pinned module object ----
$cfgOk = $false
try {
    $script:SelfSha = Get-PxcSha256 ([IO.File]::ReadAllBytes($PSCommandPath))
    $script:CfgPath = [IO.Path]::Combine($PSScriptRoot, 'ProximaConfig.psm1')
    $cfgOk = (Get-PxcSha256 ([IO.File]::ReadAllBytes($script:CfgPath))) -ceq $script:ConfigSha
} catch { $cfgOk = $false }
if (-not $cfgOk) { throw (New-PxcError 'DependencyMismatch') }
try { $script:CfgMod = Import-Module -Name $script:CfgPath -PassThru -DisableNameChecking -ErrorAction Stop } catch { throw (New-PxcError 'DependencyMismatch') }
$script:ReadConfig = $script:CfgMod.ExportedCommands['Read-ProximaConfig']
if ($null -eq $script:ReadConfig) { throw (New-PxcError 'DependencyMismatch') }

function Test-PxcPath([string]$P) { return [bool](& $script:CfgMod { param($x) Test-PxPathSyntax $x } $P) }
function Join-PxcPath([string]$Base, [string]$Rel) { if ($Base.Length -eq 3) { return $Base + $Rel }; return $Base + '\' + $Rel }
function Test-PxcProvider([string]$P) { return $P.Length -gt 0 -and $P.IndexOf([char]'/') -lt 0 }
function Test-PxcEncodable([string]$S) { try { $null = $script:Utf8.GetBytes($S); return $true } catch { return $false } }
function New-PxcCtx {
    return @{ Held = [Collections.Generic.List[IDisposable]]::new(); Recheck = [Collections.Generic.List[object]]::new()
        Seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase) }
}
function Close-PxcCtx($Ctx) { for ($i = $Ctx.Held.Count - 1; $i -ge 0; $i--) { try { $Ctx.Held[$i].Dispose() } catch { $null = $_ } } }
function Get-PxcS1Code($Err) { if ($Err.Exception.Data.Contains('PxCode')) { return [string]$Err.Exception.Data['PxCode'] }; return '' }

# ---- identity ----
function Write-PxcField($Ms, $Value) {
    if ($null -eq $Value) { $Ms.WriteByte(0); return }
    $b = $script:Utf8.GetBytes([string]$Value); $n = $b.Length; $Ms.WriteByte(1)
    foreach ($s in 24, 16, 8, 0) { $Ms.WriteByte([byte](($n -shr $s) -band 0xFF)) }
    $Ms.Write($b, 0, $n)
}
function Get-PxcFingerprint($Cfg) {
    $ms = [IO.MemoryStream]::new(); Write-PxcField $ms 'px.target.v1'
    foreach ($f in $script:IdFields) {
        $p = $Cfg.PSObject.Properties[$f]
        Write-PxcField $ms $(if ($null -eq $p) { $null } else { [Convert]::ToString($p.Value, [Globalization.CultureInfo]::InvariantCulture) })
    }
    return (Get-PxcSha256 $ms.ToArray())
}
# Selection key: the full target fingerprint, never the targetId alone.
function Get-PxcSelectionKey($Cfg, [string]$Fp) { return $Fp }
function New-PxcResult([string]$Action, $Fp, $Mode, [bool]$DryRun, [bool]$Dispatched, [string]$Outcome, $Data) {
    return [pscustomobject][ordered]@{ schema = 'px.result.v1'; action = $Action; targetFingerprint = $Fp; mode = $Mode; dryRun = $DryRun
        dispatched = $Dispatched; outcome = $Outcome; data = $Data }
}

# ---- strict small-file / JSON helpers (S1 reader through the pinned scope) ----
function Read-PxcSmallFile([string]$Path, [int]$Max) {
    $fs = [IO.FileStream]::new($Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
    try {
        if ($fs.Length -gt $Max) { throw [IO.IOException]::new('size') }
        $b = [byte[]]::new([int]$fs.Length); $n = 0
        while ($n -lt $b.Length) { $k = $fs.Read($b, $n, $b.Length - $n); if ($k -le 0) { throw [IO.IOException]::new('short') }; $n += $k }
        return , $b
    } finally { $fs.Dispose() }
}
function Read-PxcJsonObject([byte[]]$Bytes) {
    $o = & $script:CfgMod { param([byte[]]$b) $t = ConvertFrom-PxUtf8 $b; $s = @{ T = $t; P = 0 }; $v = Read-PxValue $s 0; Skip-PxWs $s
        if ($s.P -ne $t.Length -or $v.K -cne 'object') { Stop-Px MalformedJson }; return , $v.V } $Bytes
    return , $o
}
function ConvertTo-PxcJsonString([string]$S) {
    $sb = [Text.StringBuilder]::new($S.Length + 2); $null = $sb.Append([char]0x22)
    foreach ($c in $S.ToCharArray()) {
        $i = [int]$c
        if ($i -eq 0x22 -or $i -eq 0x5C) { $null = $sb.Append([char]0x5C).Append($c) }
        elseif ($i -lt 0x20) { $null = $sb.Append([char]0x5C).Append('u').Append($i.ToString('x4', [Globalization.CultureInfo]::InvariantCulture)) }
        else { $null = $sb.Append($c) }
    }
    $null = $sb.Append([char]0x22); return $sb.ToString()
}
function ConvertTo-PxcRecordJson($Rec) { return '{' + (@(foreach ($k in $Rec.Keys) { (ConvertTo-PxcJsonString $k) + ':' + (ConvertTo-PxcJsonString ([string]$Rec[$k])) }) -join ',') + '}' }
# Property or dictionary entry (deserialized results carry Hashtables). Arrays come back as ONE object: wrap with @($x)
# on a VARIABLE, never @(Get-PxcProp ...), which would nest the array.
function Get-PxcProp($Obj, [string]$Name) {
    if ($null -eq $Obj) { return $null }
    if ($Obj -is [Collections.IDictionary]) { if ($Obj.Contains($Name)) { return , $Obj[$Name] }; return $null }
    $p = $Obj.PSObject.Properties[$Name]; if ($null -eq $p) { return $null }
    return , $p.Value
}

# ---- gateway: metadata, fail-closed runtime identity, single loopback HTTP send ----
function Get-PxcGateway([string]$Base) {
    $meta = Invoke-PxcStep 'GatewayMetadataInvalid' {
        $o = Read-PxcJsonObject (Read-PxcSmallFile (Join-PxcPath $Base 'profile\rest-port.json') 4096)
        $r = @{}
        foreach ($k in 'pid', 'port') {
            if (-not $o.ContainsKey($k) -or $o[$k].K -cne 'number' -or $o[$k].V -cnotmatch '^[1-9][0-9]{0,9}\z') { throw 'metadata' }
            $r[$k] = [long]::Parse($o[$k].V, [Globalization.CultureInfo]::InvariantCulture)
        }
        if ($r['pid'] -gt 4294967295 -or $r['port'] -gt 65535) { throw 'metadata' }
        return $r
    }
    $expected = Join-PxcPath $Base 'runtime\Proxima.exe'
    Invoke-PxcStep 'RuntimeUnverified' {
        $procs = @(& $script:Prim.GetProcess $meta['pid'])
        if ($procs.Count -ne 1 -or $null -eq $procs[0]) { throw 'process' }
        $sid = Get-PxcProp $procs[0] 'SessionId'; $exePath = [string](Get-PxcProp $procs[0] 'ExecutablePath')
        if ($null -eq $sid -or [long]$sid -ne 0) { throw 'session' }
        if ([string]::IsNullOrEmpty($exePath)) { throw 'unreadable' }
        if (-not (Test-PxcPath $exePath) -or -not [string]::Equals([IO.Path]::GetFullPath($exePath), [IO.Path]::GetFullPath($expected), [StringComparison]::OrdinalIgnoreCase)) { throw 'path' }
    }
    return 'http://127.0.0.1:' + $meta['port'].ToString([Globalization.CultureInfo]::InvariantCulture)
}
# Exactly one primitive send; the API key is read from THIS endpoint's environment and only when $Auth.
function Invoke-PxcHttp([string]$Url, [string]$Method, [string]$Path, $Body, [int]$Timeout, [bool]$Auth) {
    $h = [ordered]@{}
    if ($Auth) { $k = [Environment]::GetEnvironmentVariable('PROXIMA_API_KEY'); if ($k) { $h['Authorization'] = 'Bearer ' + $k } }
    $resp = & $script:Prim.Http ([ordered]@{ Method = $Method; Uri = $Url + $Path; Headers = $h; Body = $Body; TimeoutSec = $Timeout })
    return @{ Status = [int]$resp['Status']; Body = [string]$resp['Body'] }
}
function Get-PxcAdvertised([string]$Url) {
    $r = Invoke-PxcStep 'ModelsUnavailable' { Invoke-PxcHttp $Url 'GET' '/v1/models' $null 30 $true }
    if ($r.Status -ne 200) { Stop-Pxc 'ModelsUnavailable' }
    $ids = Invoke-PxcStep 'ModelsUnavailable' {
        $list = [Collections.Generic.List[string]]::new()
        $j = Microsoft.PowerShell.Utility\ConvertFrom-Json -InputObject $r.Body
        $data = Get-PxcProp $j 'data'; if ($null -eq $data) { throw 'shape' }
        foreach ($e in @($data)) { $id = Get-PxcProp $e 'id'; if ($id -is [string]) { $list.Add($id) } }
        , $list
    }
    return , $ids
}
function Test-PxcModel($Ids, [string]$Provider, [string]$Model) {
    if (-not $Model.StartsWith($Provider + '/', [StringComparison]::Ordinal)) { return $false }
    foreach ($i in $Ids) { if ([string]::Equals($i, $Model, [StringComparison]::Ordinal)) { return $true } }
    return $false
}

# ---- journal: physical chain outside ProtectedRoot (S1 helpers, held handles), CreateNew record ----
function Open-PxcDir([string]$Path, $Ctx) { return (& $script:CfgMod { param($p, $c) Open-PxChain $p $false 'PxcMissing' $c 0 } $Path $Ctx) }
# Containment is proven for the base and for each level BEFORE anything below it is created; every level is reopened
# (held, no reparse, exactly one segment below its parent) after creation.
function Assert-PxcOutside($Node, $Prot, $Ctx) {
    if ([string]::Equals($Node.Final.TrimEnd('\'), $Prot.Final.TrimEnd('\'), [StringComparison]::OrdinalIgnoreCase)) { throw 'inside' }
    & $script:CfgMod { param($f, $r, $c) Assert-PxOutside $f ($r.TrimEnd('\') + '\') $c 0 } $Node.Final $Prot.Final $Ctx
}
function Open-PxcJournal([string]$Base, [string]$Protected, [bool]$Create, $Ctx) {
    $prot = Open-PxcDir $Protected $Ctx
    $node = Open-PxcDir $Base $Ctx; Assert-PxcOutside $node $prot $Ctx
    foreach ($rel in 'results', 'results\px-active') {
        $p = Join-PxcPath $Base $rel
        try { $node = Open-PxcDir $p $Ctx }
        catch {
            if ((Get-PxcS1Code $_) -cne 'PxcMissing') { throw }
            if (-not $Create) { return $null }
            $null = [IO.Directory]::CreateDirectory($p)
            $node = Open-PxcDir $p $Ctx
        }
        Assert-PxcOutside $node $prot $Ctx
    }
    return $node
}
function New-PxcRecordStream([string]$Base, $Dir, $Ctx) {
    $id = [string](& $script:Prim.NewId)
    if ($id -cnotmatch $script:ReGuid) { throw 'id' }
    $fs = [IO.FileStream]::new((Join-PxcPath $Base "results\px-active\$id.json"), [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::Read)
    $Ctx.Held.Add($fs)
    $n = & $script:CfgMod { param($h) Get-PxNode $h } $fs.SafeFileHandle
    $child = & $script:CfgMod { param($a, $b) Test-PxChild $a $b } $Dir.Final $n.Final
    if (-not $child -or $n.Links -ne 1 -or ($n.Attr -band $script:BadAttr) -ne 0) { throw 'record' }
    return @{ Id = $id; Stream = $fs }
}
function Write-PxcRecord($Fs, $Rec) {
    $b = $script:Utf8.GetBytes((ConvertTo-PxcRecordJson $Rec)); $Fs.SetLength(0); $Fs.Position = 0; $Fs.Write($b, 0, $b.Length); $Fs.Flush($true)
}
# A record is settled only if it is a regular GUID-named file holding {"state":"completed",...}. Anything else blocks.
function Test-PxcRecordDone([string]$P) {
    try {
        if ([IO.Path]::GetFileName($P) -cnotmatch $script:ReRecord) { return $false }
        if (([int][IO.File]::GetAttributes($P) -band ($script:BadAttr -bor 0x10)) -ne 0) { return $false }
        $o = Read-PxcJsonObject (Read-PxcSmallFile $P 65536)
        return ($o.ContainsKey('state') -and $o['state'].K -ceq 'string' -and $o['state'].V -ceq 'completed')
    } catch { return $false } # malformed/unreadable record: never settled
}
function Get-PxcPending([string]$Base, [string]$Protected) {
    $ctx = New-PxcCtx
    try {
        return (Invoke-PxcStep 'PendingGuardUnverified' {
                $dir = Open-PxcJournal $Base $Protected $false $ctx
                if ($null -eq $dir) { return 0 }
                $n = 0
                foreach ($e in [IO.Directory]::GetFileSystemEntries((Join-PxcPath $Base 'results\px-active'))) { if (-not (Test-PxcRecordDone $e)) { $n++ } }
                return $n
            })
    } finally { Close-PxcCtx $ctx }
}

# ---- operations (endpoint side; also the in-process Local path after px's gate) ----
function Invoke-PxcAsk([string]$Base, [string]$Fp, [string]$Protected, [string]$Provider, [string]$Model, [string]$Prompt) {
    $url = Get-PxcGateway $Base
    if (-not (Test-PxcModel (Get-PxcAdvertised $url) $Provider $Model)) { Stop-Pxc 'ModelNotAdvertised' }
    $ctx = New-PxcCtx
    try {
        $dir = Invoke-PxcStep 'JournalUnsafe' { Open-PxcJournal $Base $Protected $true $ctx }
        $rs = Invoke-PxcStep 'JournalFailed' { New-PxcRecordStream $Base $dir $ctx }
        $rec = [ordered]@{ schema = 'px.active.v1'; action = 'ask'; targetFingerprint = $Fp; requestedModel = $Model; state = 'pending' }
        Invoke-PxcStep 'JournalFailed' { Write-PxcRecord $rs.Stream $rec }
        $body = '{"model":' + (ConvertTo-PxcJsonString $Model) + ',"messages":[{"role":"user","content":' + (ConvertTo-PxcJsonString $Prompt) + '}]}'
        $resp = $null
        try { $resp = Invoke-PxcHttp $url 'POST' '/v1/chat/completions' $body 300 $true } catch { $resp = $null }
        $state = 'unknown'; $status = $null; $answer = $null; $reported = $null; $parsed = $false
        if ($null -ne $resp) {
            $status = $resp.Status
            if ($status -eq 200) {
                $state = 'completed'
                try {
                    $j = Microsoft.PowerShell.Utility\ConvertFrom-Json -InputObject $resp.Body
                    $choices = Get-PxcProp $j 'choices'; $first = @($choices)[0]
                    $answer = Get-PxcProp (Get-PxcProp $first 'message') 'content'; $reported = Get-PxcProp $j 'model'
                    $parsed = $answer -is [string]
                } catch { $parsed = $false }
            }
        }
        $rec['state'] = $state; $final = $true
        try { Write-PxcRecord $rs.Stream $rec } catch { $final = $false }
        $outcome = $(if (-not $final) { 'finalize_failed' } elseif ($state -cne 'completed') { 'unknown' } elseif ($parsed) { 'ok' } else { 'response_unparsed' })
        return (New-PxcResult 'ask' $Fp 'Endpoint' $false $true $outcome ([ordered]@{ requestedModel = $Model; reportedModel = $(if ($reported -is [string]) { $reported })
                    answer = $(if ($parsed) { $answer }); answerTrust = 'untrusted_data'; httpStatus = $status; recordId = $rs.Id
                    recordState = $(if ($final) { $state } else { 'pending_finalize_failed' }) }))
    } finally { Close-PxcCtx $ctx }
}
function Assert-PxcNoLoginUi {
    $ui = Invoke-PxcStep 'LoginUiUnknown' { $n = 0; foreach ($i in @(& $script:Prim.UiSessions)) { if ($null -eq $i -or [long]$i -ne 0) { $n++ } }; $n }
    if ($ui -ne 0) { Stop-Pxc 'LoginUiPresent' }
}
# Recognized binding only: exactly "<base>\runtime\Proxima.exe" quoted with no arguments, or unquoted when it has no spaces.
function Assert-PxcService([string]$Base) {
    $exe = Join-PxcPath $Base 'runtime\Proxima.exe'
    $ok = Invoke-PxcStep 'ServiceIdentityUnverified' {
        $svc = @(& $script:Prim.GetService)
        if ($svc.Count -ne 1 -or $null -eq $svc[0]) { return $false }
        if (-not [string]::Equals([string](Get-PxcProp $svc[0] 'Name'), 'ProximaGateway', [StringComparison]::Ordinal)) { return $false }
        $pn = [string](Get-PxcProp $svc[0] 'PathName')
        if ([string]::Equals($pn, '"' + $exe + '"', [StringComparison]::OrdinalIgnoreCase)) { return $true }
        return ($exe.IndexOf([char]' ') -lt 0 -and [string]::Equals($pn, $exe, [StringComparison]::OrdinalIgnoreCase))
    }
    if ($ok -ne $true) { Stop-Pxc 'ServiceIdentityUnverified' }
}
function Invoke-PxcService([string]$Action, [string]$Base, [string]$Fp, [string]$Protected, [bool]$Force) {
    $data = [ordered]@{ pendingOverridden = 0; serviceCommand = $null; readiness = 'not_checked' }
    if ($Action -cne 'start') {
        $pending = Get-PxcPending $Base $Protected
        if ($pending -gt 0) { if (-not $Force) { Stop-Pxc 'PendingRequests' }; $data['pendingOverridden'] = $pending }
    }
    if ($Action -cne 'stop') { Assert-PxcNoLoginUi }
    Assert-PxcService $Base
    $verb = $(switch -CaseSensitive ($Action) { 'start' { 'Start' } 'stop' { 'Stop' } default { 'Restart' } })
    Invoke-PxcStep 'ServiceCommandFailed' { $null = & $script:Prim.ServiceControl $verb }
    $data['serviceCommand'] = $verb
    return (New-PxcResult $Action $Fp 'Endpoint' $false $true 'service_command_completed' $data)
}
function Invoke-PxcCore([string]$Action, [string]$Base, [string]$Fp, [string]$Protected, [string]$Provider, [string]$Model, [string]$Prompt, [bool]$Force) {
    switch -CaseSensitive ($Action) {
        'handshake' { return (New-PxcResult $Action $Fp 'Endpoint' $false $false 'ok' ([ordered]@{ protocolVersion = $script:Protocol; moduleSha256 = $script:SelfSha; configModuleSha256 = $script:ConfigSha })) }
        'status' {
            $url = Get-PxcGateway $Base
            $r = Invoke-PxcStep 'StatusUnavailable' { Invoke-PxcHttp $url 'GET' '/api/status' $null 10 $false }
            return (New-PxcResult $Action $Fp 'Endpoint' $false $true $(if ($r.Status -eq 200) { 'ok' } else { 'unhealthy' }) ([ordered]@{ httpStatus = $r.Status; authentication = 'not_verified_by_status' }))
        }
        'models' {
            $ids = Get-PxcAdvertised (Get-PxcGateway $Base)
            $sel = @(foreach ($i in $ids) { if (-not $Provider -or $i.StartsWith($Provider + '/', [StringComparison]::Ordinal)) { $i } })
            return (New-PxcResult $Action $Fp 'Endpoint' $false $true 'ok' ([ordered]@{ models = $sel; modelState = 'advertised_not_execution_tested' }))
        }
        'ask' { return (Invoke-PxcAsk $Base $Fp $Protected $Provider $Model $Prompt) }
        default { return (Invoke-PxcService $Action $Base $Fp $Protected $Force) }
    }
}

# ---- remote: constant endpoint body, request is DATA only ----
$script:EndpointBody = {
    param($Request)
    Set-StrictMode -Version 3.0
    $ErrorActionPreference = 'Stop'
    $fail = { param([string]$c) throw [Management.Automation.ErrorRecord]::new([InvalidOperationException]::new("ProximaControl: operation rejected: $c."), "ProximaControl.$c", 'InvalidOperation', $null) }
    $names = 'Action', 'BasePath', 'Provider', 'Model', 'Prompt', 'Force', 'TargetFingerprint', 'WhatIf', 'ModuleSha256', 'ConfigModuleSha256', 'ProtocolVersion'
    $allowed = [Collections.Generic.HashSet[string]]::new([string[]]$names, [StringComparer]::Ordinal)
    $acts = [Collections.Generic.HashSet[string]]::new([string[]]@('status', 'models', 'ask', 'start', 'stop', 'restart', 'handshake'), [StringComparer]::Ordinal)
    $v = [Collections.Generic.Dictionary[string, object]]::new([StringComparer]::Ordinal)
    if ($Request -isnot [Collections.IDictionary]) { & $fail 'RequestInvalid' }
    foreach ($e in $Request.GetEnumerator()) {
        if ($e.Key -isnot [string] -or -not $allowed.Contains($e.Key) -or $v.ContainsKey($e.Key)) { & $fail 'RequestInvalid' }
        $v[$e.Key] = $e.Value
    }
    if ($v.Count -ne $names.Count -or $v['Force'] -isnot [bool] -or $v['WhatIf'] -isnot [bool]) { & $fail 'RequestInvalid' }
    if ($v['ProtocolVersion'] -isnot [int] -or $v['ProtocolVersion'] -ne 1) { & $fail 'ProtocolMismatch' }
    foreach ($k in 'TargetFingerprint', 'ModuleSha256', 'ConfigModuleSha256') { if ($v[$k] -isnot [string] -or $v[$k] -cnotmatch '^[0-9a-f]{64}\z') { & $fail 'RequestInvalid' } }
    foreach ($k in 'Action', 'BasePath', 'Provider', 'Model', 'Prompt') { if ($null -ne $v[$k] -and $v[$k] -isnot [string]) { & $fail 'RequestInvalid' } }
    if ($null -eq $v['Action'] -or -not $acts.Contains($v['Action'])) { & $fail 'RequestInvalid' }
    # Effective WhatIf = ambient OR envelope; true returns before any filesystem access, import or dispatch.
    if ([bool]$WhatIfPreference -or $v['WhatIf']) {
        return [pscustomobject][ordered]@{ schema = 'px.result.v1'; action = $v['Action']; targetFingerprint = $v['TargetFingerprint']; mode = 'Remote'
            dryRun = $true; dispatched = $false; outcome = 'whatif'; data = $null }
    }
    $b = $v['BasePath']
    # Superscripts 1-3 from code points (as S1 does): the pattern must not depend on how this BOM-less file is decoded (PS5.1: ANSI).
    $dev = [regex]::new('^(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|(?:COM|LPT)[0-9' + [char]0xB9 + [char]0xB2 + [char]0xB3 + '])(?:\..*)?\z', [Text.RegularExpressions.RegexOptions]'IgnoreCase, CultureInvariant')
    $okPath = $null -ne $b -and $b.Length -le 32000 -and $b -cmatch '^[A-Za-z]:\\'
    if ($okPath -and $b.Length -gt 3) { foreach ($seg in $b.Substring(3).Split([char]'\')) { if ($seg.Length -eq 0 -or $seg -cmatch '[\x00-\x1f<>:"/|?*]|[. ]\z' -or $dev.IsMatch($seg)) { $okPath = $false } } }
    if (-not $okPath) { & $fail 'RequestInvalid' }
    $ctl = $(if ($b.Length -eq 3) { $b + 'control' } else { $b + '\control' })
    $files = @("$ctl\ProximaControl.psm1", "$ctl\ProximaConfig.psm1"); $want = @($v['ModuleSha256'], $v['ConfigModuleSha256'])
    for ($i = 0; $i -lt 2; $i++) {
        $got = $null
        try { $h = [Security.Cryptography.SHA256]::Create(); $got = ([BitConverter]::ToString($h.ComputeHash([IO.File]::ReadAllBytes($files[$i]))) -replace '-', '').ToLowerInvariant() } catch { $got = $null }
        if ($got -cne $want[$i]) { & $fail 'EndpointCodeMismatch' }
    }
    $m = Import-Module -Name $files[0] -PassThru -DisableNameChecking -ErrorAction Stop
    $op = $m.ExportedCommands['Invoke-ProximaOperation']
    if ($null -eq $op) { & $fail 'EndpointCodeMismatch' }
    $p = @{ Action = $v['Action']; BasePath = $b; TargetFingerprint = $v['TargetFingerprint']; ProtectedRoot = $ctl; Force = [bool]$v['Force']; WhatIf = $false; Confirm = $false }
    foreach ($k in 'Provider', 'Model', 'Prompt') { if ($null -ne $v[$k]) { $p[$k] = $v[$k] } }
    & $op @p
}
function Invoke-PxcRemoteCall($Session, [string]$Base, [string]$Fp, [string]$Action, [string]$Provider, [string]$Model, [string]$Prompt, [bool]$Force) {
    $envelope = @{ Action = $Action; BasePath = $Base; Provider = $Provider; Model = $Model; Prompt = $Prompt; Force = $Force; TargetFingerprint = $Fp
        WhatIf = [bool]$WhatIfPreference; ModuleSha256 = $script:SelfSha; ConfigModuleSha256 = $script:ConfigSha; ProtocolVersion = $script:Protocol }
    $out = $null
    try { $out = @(& $script:Prim.InvokeRemote $Session $script:EndpointBody $envelope) }
    catch {
        if ([string]$_.FullyQualifiedErrorId -cmatch '^ProximaControl\.([A-Za-z]{1,40})(,|\z)') { Stop-Pxc $Matches[1] }
        Stop-Pxc 'RemoteFailed'
    }
    return (Invoke-PxcStep 'RemoteFailed' {
            if ($out.Count -ne 1) { throw 'shape' }
            $r = $out[0]
            if ([string](Get-PxcProp $r 'schema') -cne 'px.result.v1' -or [string](Get-PxcProp $r 'targetFingerprint') -cne $Fp -or [string](Get-PxcProp $r 'action') -cne $Action) { throw 'shape' }
            $r
        })
}
function Invoke-PxcDispatch($Cfg, [string]$Fp, [string]$Action, [string]$Protected, [string]$Provider, [string]$Model, [string]$Prompt, [bool]$Force) {
    if ([string]$Cfg.mode -ceq 'Local') {
        $r = Invoke-PxcCore $Action ([string]$Cfg.basePath) $Fp $Protected $Provider $Model $Prompt $Force
        $r.mode = 'Local'; return $r
    }
    $s = $null
    if (-not $script:Sessions.TryGetValue($Fp, [ref]$s)) { Stop-Pxc 'NotConnected' }
    $r = Invoke-PxcRemoteCall $s ([string]$Cfg.basePath) $Fp $Action $Provider $Model $Prompt $Force
    return (New-PxcResult $Action $Fp 'Remote' $false ([bool](Get-PxcProp $r 'dispatched')) ([string](Get-PxcProp $r 'outcome')) (Get-PxcProp $r 'data'))
}
function Connect-PxcTarget($Cfg, [string]$Fp, $Credential) {
    if ($null -eq $Credential) { Stop-Pxc 'CredentialRequired' }
    $req = [ordered]@{ ConnectionUri = [string]$Cfg.connectionUri; ConfigurationName = [string]$Cfg.configurationName; Credential = $Credential
        Authentication = 'Negotiate'; SkipCACheck = $false; SkipCNCheck = $false; SkipRevocationCheck = $false }
    $new = Invoke-PxcStep 'SessionFailed' { & $script:Prim.NewSession $req }
    if ($null -eq $new) { Stop-Pxc 'SessionFailed' }
    $ok = $false
    try {
        $d = Get-PxcProp (Invoke-PxcRemoteCall $new ([string]$Cfg.basePath) $Fp 'handshake' '' '' '' $false) 'data'
        $pv = Get-PxcProp $d 'protocolVersion'
        $ok = $pv -is [int] -and $pv -eq $script:Protocol -and [string](Get-PxcProp $d 'moduleSha256') -ceq $script:SelfSha -and [string](Get-PxcProp $d 'configModuleSha256') -ceq $script:ConfigSha
    } catch { $ok = $false }
    if (-not $ok) {
        try { $null = & $script:Prim.RemoveSession $new } catch { $script:Orphans.Add(@{ fp = $Fp; session = $new }); Stop-Pxc 'ConnectCleanupFailed' }
        Stop-Pxc 'HandshakeFailed'
    }
    $old = $null; $had = $script:Sessions.TryGetValue($Fp, [ref]$old)
    $script:Sessions[$Fp] = $new; $cleanup = 'none'
    if ($had) { try { $null = & $script:Prim.RemoveSession $old; $cleanup = 'removed' } catch { $script:Orphans.Add(@{ fp = $Fp; session = $old }); $cleanup = 'failed_retained' } }
    return (New-PxcResult 'connect' $Fp 'Remote' $false $true $(if ($cleanup -ceq 'failed_retained') { 'connected_old_cleanup_failed' } else { 'connected' }) ([ordered]@{ replaced = $had; oldSessionCleanup = $cleanup }))
}
function Disconnect-PxcTarget([string]$Fp) {
    $s = $null; $had = $script:Sessions.TryGetValue($Fp, [ref]$s)
    $orph = @($script:Orphans | Where-Object { [string]::Equals($_.fp, $Fp, [StringComparison]::Ordinal) })
    if (-not $had -and $orph.Count -eq 0) { Stop-Pxc 'NotConnected' }
    $failed = 0
    if ($had) { try { $null = & $script:Prim.RemoveSession $s; $null = $script:Sessions.Remove($Fp) } catch { $failed++ } }
    foreach ($o in $orph) { try { $null = & $script:Prim.RemoveSession $o.session; $null = $script:Orphans.Remove($o) } catch { $failed++ } }
    if ($failed) { Stop-Pxc 'DisconnectFailed' }
    return (New-PxcResult 'disconnect' $Fp 'Remote' $false $true 'disconnected' ([ordered]@{ orphansReleased = $orph.Count }))
}

# ---- public API ----
function px {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium', PositionalBinding = $false)]
    param([Parameter(Position = 0)][string]$Action = 'help', [Parameter(Position = 1)][string]$Provider, [Parameter(Position = 2)][string]$Value,
        [string]$ConfigPath, [string]$RepositoryRoot, [string]$TargetId, [string]$Model, [pscredential]$Credential, [switch]$Force)
    try {
        if (-not $script:PxActions.Contains($Action)) { Stop-Pxc 'UnknownAction' }
        if ($Action -ceq 'help') { return (New-PxcResult 'help' $null $null $false $false 'ok' $script:Help) }
        foreach ($n in 'ConfigPath', 'RepositoryRoot', 'TargetId') { if (-not $PSBoundParameters.ContainsKey($n)) { Stop-Pxc 'ArgumentMissing' } }
        $cfg = & $script:ReadConfig -ConfigPath $ConfigPath -RepositoryRoot $RepositoryRoot
        if (-not [string]::Equals([string]$cfg.targetId, $TargetId, [StringComparison]::Ordinal)) { Stop-Pxc 'TargetMismatch' }
        $fp = Get-PxcFingerprint $cfg; $mode = [string]$cfg.mode; $display = 'px target ' + $fp.Substring(0, 12)
        if ($Action -ceq 'config') { return (New-PxcResult 'config' $fp $mode $false $false 'ok' $cfg) }
        $useModel = $(if ($PSBoundParameters.ContainsKey('Value')) { $Value } else { $Model })
        switch -CaseSensitive ($Action) {
            'use' { if (-not (Test-PxcProvider $Provider) -or -not $useModel) { Stop-Pxc 'ArgumentInvalid' } }
            'ask' { if (-not (Test-PxcProvider $Provider) -or -not $PSBoundParameters.ContainsKey('Value') -or -not (Test-PxcEncodable $Value)) { Stop-Pxc 'ArgumentInvalid' } }
            'models' { if ($Provider -and -not (Test-PxcProvider $Provider)) { Stop-Pxc 'ArgumentInvalid' } }
            { $_ -ceq 'connect' -or $_ -ceq 'disconnect' } { if ($mode -cne 'Remote') { Stop-Pxc 'NotRemote' } }
        }
        if (-not $PSCmdlet.ShouldProcess($display, $Action)) { return (New-PxcResult $Action $fp $mode $true $false 'whatif' $null) }
        $key = Get-PxcSelectionKey $cfg $fp
        switch -CaseSensitive ($Action) {
            'connect' { return (Connect-PxcTarget $cfg $fp $(if ($PSBoundParameters.ContainsKey('Credential')) { $Credential })) }
            'disconnect' { return (Disconnect-PxcTarget $fp) }
            'use' {
                $r = Invoke-PxcDispatch $cfg $fp 'models' $RepositoryRoot $Provider '' '' $false
                $advertised = Get-PxcProp (Get-PxcProp $r 'data') 'models'
                if (-not (Test-PxcModel @($advertised) $Provider $useModel)) { Stop-Pxc 'ModelNotAdvertised' }
                $inner = $null
                if (-not $script:Selection.TryGetValue($key, [ref]$inner)) { $inner = [Collections.Generic.Dictionary[string, string]]::new([StringComparer]::Ordinal); $script:Selection[$key] = $inner }
                $inner[$Provider] = $useModel
                return (New-PxcResult 'use' $fp $mode $false $true 'selected' ([ordered]@{ provider = $Provider; model = $useModel; modelState = 'advertised_not_execution_tested' }))
            }
            'ask' {
                $m = $null
                if ($PSBoundParameters.ContainsKey('Model')) { $m = $Model }
                else { $inner = $null; if ($script:Selection.TryGetValue($key, [ref]$inner)) { $null = $inner.TryGetValue($Provider, [ref]$m) } }
                if (-not $m) { Stop-Pxc 'NoModelSelected' }
                return (Invoke-PxcDispatch $cfg $fp 'ask' $RepositoryRoot $Provider $m $Value $false)
            }
            default { return (Invoke-PxcDispatch $cfg $fp $Action $RepositoryRoot $Provider '' '' ([bool]$Force -and ($Action -ceq 'stop' -or $Action -ceq 'restart'))) }
        }
    } catch { $PSCmdlet.ThrowTerminatingError((Resolve-PxcError $_)) }
}
function Invoke-ProximaOperation {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium', PositionalBinding = $false)]
    param([Parameter(Mandatory = $true)][string]$Action, [Parameter(Mandatory = $true)][string]$BasePath, [Parameter(Mandatory = $true)][string]$TargetFingerprint,
        [Parameter(Mandatory = $true)][string]$ProtectedRoot, [string]$Provider, [string]$Model, [string]$Prompt, [switch]$Force)
    try {
        if (-not $script:OpActions.Contains($Action) -or $TargetFingerprint -cnotmatch '^[0-9a-f]{64}\z' -or -not (Test-PxcPath $BasePath) -or -not (Test-PxcPath $ProtectedRoot)) { Stop-Pxc 'ArgumentInvalid' }
        if (($Provider -and -not (Test-PxcProvider $Provider)) -or ($Action -ceq 'ask' -and (-not (Test-PxcProvider $Provider) -or -not $Model -or -not (Test-PxcEncodable $Prompt)))) { Stop-Pxc 'ArgumentInvalid' }
        $opTarget = 'px target ' + $TargetFingerprint.Substring(0, 12)
        if (-not $PSCmdlet.ShouldProcess($opTarget, $Action)) { return (New-PxcResult $Action $TargetFingerprint 'Endpoint' $true $false 'whatif' $null) }
        return (Invoke-PxcCore $Action $BasePath $TargetFingerprint $ProtectedRoot $Provider $Model $Prompt ([bool]$Force -and ($Action -ceq 'stop' -or $Action -ceq 'restart')))
    } catch { $PSCmdlet.ThrowTerminatingError((Resolve-PxcError $_)) }
}

# ---- concrete backend (qualified commands); replaceable ONLY through module scope by the isolated test harness ----
function Invoke-PxcHttpDefault($Req) {
    if ($PSVersionTable.PSEdition -cne 'Core') { Add-Type -AssemblyName System.Net.Http }
    $handler = [Net.Http.HttpClientHandler]::new(); $handler.UseProxy = $false; $handler.AllowAutoRedirect = $false; $handler.UseCookies = $false
    $client = [Net.Http.HttpClient]::new($handler); $client.Timeout = [TimeSpan]::FromSeconds($Req['TimeoutSec']); $client.MaxResponseContentBufferSize = 8MB
    try {
        $msg = [Net.Http.HttpRequestMessage]::new([Net.Http.HttpMethod]::new($Req['Method']), [Uri]::new($Req['Uri']))
        $msg.Headers.ExpectContinue = $false
        foreach ($k in $Req['Headers'].Keys) { $null = $msg.Headers.TryAddWithoutValidation($k, [string]$Req['Headers'][$k]) }
        if ($null -ne $Req['Body']) { $msg.Content = [Net.Http.StringContent]::new([string]$Req['Body'], [Text.UTF8Encoding]::new($false), 'application/json') }
        $resp = $client.SendAsync($msg).GetAwaiter().GetResult()
        $bytes = $resp.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
        return @{ Status = [int]$resp.StatusCode; Body = [Text.UTF8Encoding]::new($false).GetString($bytes) }
    } finally { $client.Dispose() }
}
$script:Prim = @{
    NewSession     = { param($Req)
        $o = Microsoft.PowerShell.Core\New-PSSessionOption -SkipCACheck:$Req['SkipCACheck'] -SkipCNCheck:$Req['SkipCNCheck'] -SkipRevocationCheck:$Req['SkipRevocationCheck']
        Microsoft.PowerShell.Core\New-PSSession -ConnectionUri $Req['ConnectionUri'] -ConfigurationName $Req['ConfigurationName'] -Credential $Req['Credential'] -Authentication $Req['Authentication'] -SessionOption $o -ErrorAction Stop }
    RemoveSession  = { param($Session) Microsoft.PowerShell.Core\Remove-PSSession -Session $Session -WhatIf:$false -Confirm:$false -ErrorAction Stop }
    InvokeRemote   = { param($Session, $Body, $Envelope) Microsoft.PowerShell.Core\Invoke-Command -Session $Session -ScriptBlock $Body -ArgumentList (, $Envelope) -ErrorAction Stop }
    Http           = { param($Req) Invoke-PxcHttpDefault $Req }
    GetProcess     = { param($ProcessId) CimCmdlets\Get-CimInstance -ClassName Win32_Process -Filter ('ProcessId=' + ([long]$ProcessId).ToString([Globalization.CultureInfo]::InvariantCulture)) -ErrorAction Stop }
    UiSessions     = { @(CimCmdlets\Get-CimInstance -ClassName Win32_Process -Filter "Name='Proxima.exe'" -ErrorAction Stop | ForEach-Object { $_.SessionId }) }
    GetService     = { CimCmdlets\Get-CimInstance -ClassName Win32_Service -Filter "Name='ProximaGateway'" -ErrorAction Stop }
    ServiceControl = { param($Verb)
        switch -CaseSensitive ($Verb) {
            'Start' { Microsoft.PowerShell.Management\Start-Service -Name 'ProximaGateway' -WhatIf:$false -Confirm:$false -ErrorAction Stop }
            'Stop' { Microsoft.PowerShell.Management\Stop-Service -Name 'ProximaGateway' -WhatIf:$false -Confirm:$false -ErrorAction Stop }
            'Restart' { Microsoft.PowerShell.Management\Restart-Service -Name 'ProximaGateway' -WhatIf:$false -Confirm:$false -ErrorAction Stop }
            default { throw 'verb' }
        } }
    NewId          = { [guid]::NewGuid().ToString('D') }
}
$ExecutionContext.SessionState.Module.OnRemove = {
    foreach ($s in @(@($script:Sessions.Values) + @($script:Orphans | ForEach-Object { $_.session }))) { try { $null = & $script:Prim.RemoveSession $s } catch { $null = $_ } }
}
Export-ModuleMember -Function 'px', 'Invoke-ProximaOperation'
