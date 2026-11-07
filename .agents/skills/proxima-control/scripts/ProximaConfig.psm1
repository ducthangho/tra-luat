# ProximaConfig.psm1 - wp1271 r2 (PROXIMA-P1-S1). Standalone, read-only reader for ONE explicit Proxima
# target config file. No discovery, defaults, fallback or writes; reading never contacts the target.
# Fail closed: any path or value that is not provably safe is rejected. Errors have FullyQualifiedErrorId
# 'ProximaConfig.<Code>' and a fixed message that never echoes config keys, values, raw JSON or inner errors.
# Windows path semantics only: drive-qualified, local fixed drive, case-insensitive containment.
Set-StrictMode -Version 3.0
$script:Fields = @('schemaVersion', 'targetId', 'mode', 'basePath', 'connectionUri', 'configurationName')
$script:RemoteOnly = @('connectionUri', 'configurationName')
$script:SecretKey = '(?i)pass|pwd|secret|token|credential|cookie|api.?key|auth|bearer|private|cert'
$script:IdPattern = '^[A-Za-z0-9][A-Za-z0-9._-]{0,127}\z'
$script:BadAttr = [IO.FileAttributes]::ReparsePoint -bor [IO.FileAttributes]::Offline
$script:MaxBytes = 65536
$script:ReWs = [regex]'\G[ \t\r\n]*'
$script:ReString = [regex]'\G"((?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4}))*)"'
$script:ReNumber = [regex]'\G-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?'
# Codes are constant identifiers set only by Stop-Px (see the Stop-Px calls below); anything else is Internal.
function Stop-Px([string]$Code, [string]$Field = '') { $ex = [Exception]::new("ProximaConfig.$Code"); $ex.Data['PxCode'] = $Code; $ex.Data['PxField'] = $Field; throw $ex }
function New-PxError([string]$Code, [string]$Field) {
    if ($Code -cnotmatch '^[A-Za-z]{1,40}\z') { $Code = 'Internal' }
    $msg = "Config rejected: $Code."
    if ($script:Fields -ccontains $Field) { $msg += " Field: $Field." }
    $cat = $(if ($Code -like '*NotFound') { 'ObjectNotFound' } else { 'InvalidData' })
    return [Management.Automation.ErrorRecord]::new([InvalidOperationException]::new("ProximaConfig: $msg"), "ProximaConfig.$Code", $cat, $null)
}
# Syntax only, no filesystem access: X:\seg\seg with no empty, dot, trailing-dot/space, device or stream
# segment. Rejects relative, drive-relative (C:x), rooted (\x), UNC/device (\\x) and forward-slash forms.
function Test-PxPathSyntax([string]$Path) {
    if ($Path.Length -gt 1024 -or $Path -notmatch '^[A-Za-z]:\\') { return $false }
    if ($Path.Length -eq 3) { return $true }
    foreach ($seg in $Path.Substring(3).Split([char]'\')) {
        if ($seg.Length -eq 0 -or $seg -match '[\x00-\x1f<>:"/|?*]|[. ]\z' -or
            $seg -match '^(?i:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[0-9]|LPT[0-9])(\..*)?\z') { return $false }
    }
    return $true
}

# Walks from the drive root one on-disk entry per component: exactly one entry with the same long name (8.3 aliases
# and case-sensitive duplicates rejected), never a reparse point, so no junction is followed. Returns that entry.
function Resolve-PxEntry([string]$Path, [bool]$File, [string]$Missing) {
    if ([IO.DriveInfo]::new($Path.Substring(0, 1)).DriveType -ne [IO.DriveType]::Fixed) { Stop-Px DriveUnsupported }
    $cur = [IO.DirectoryInfo]::new($Path.Substring(0, 3).ToUpperInvariant())
    $segs = @(); if ($Path.Length -gt 3) { $segs = $Path.Substring(3).Split([char]'\') }
    for ($i = 0; $i -lt $segs.Count; $i++) {
        try { $hits = @($cur.GetFileSystemInfos($segs[$i])) } catch { Stop-Px Ambiguous }
        if ($hits.Count -eq 0) { Stop-Px $Missing }
        $e = $hits[0]
        if ($hits.Count -ne 1 -or -not [string]::Equals($e.Name, $segs[$i], [StringComparison]::OrdinalIgnoreCase)) { Stop-Px Ambiguous }
        if (($e.Attributes -band $script:BadAttr) -ne 0) { Stop-Px ReparsePoint }
        if ($i -lt $segs.Count - 1 -or -not $File) {
            if ($e -isnot [IO.DirectoryInfo]) { Stop-Px $Missing }
            $cur = $e
        } elseif ($e -isnot [IO.FileInfo]) { Stop-Px NotAFile }
        else { return $e }
    }
    if ($File) { Stop-Px NotAFile }
    return $cur
}
# Strict UTF-8: decoding without replacement must round-trip to the exact bytes. A leading BOM is allowed.
function ConvertFrom-PxUtf8([byte[]]$Bytes) {
    $skip = 0
    if ($Bytes.Length -ge 3 -and $Bytes[0] -eq 0xEF -and $Bytes[1] -eq 0xBB -and $Bytes[2] -eq 0xBF) { $skip = 3 }
    $utf8 = [Text.UTF8Encoding]::new($false, $false)
    $text = $utf8.GetString($Bytes, $skip, $Bytes.Length - $skip)
    if ([Convert]::ToBase64String($utf8.GetBytes($text)) -cne [Convert]::ToBase64String($Bytes, $skip, $Bytes.Length - $skip)) { Stop-Px Encoding }
    return $text
}
# Strict RFC 8259 parser, identical on PS5.1/PS7 (ConvertFrom-Json differs there on duplicate keys, key case, number
# and date types, and its errors quote input). Values are tagged @{ K = kind; V = value }; numbers keep source text.
function Skip-PxWs($s) { $s.P += $script:ReWs.Match($s.T, $s.P).Length }
function Test-PxNext($s, [string]$Ch) { Skip-PxWs $s; return ($s.P -lt $s.T.Length -and $s.T[$s.P] -ceq $Ch) }
function Read-PxLiteral($s, [string]$Lit) {
    if ($s.P + $Lit.Length -gt $s.T.Length -or [string]::CompareOrdinal($s.T, $s.P, $Lit, 0, $Lit.Length) -ne 0) { Stop-Px MalformedJson }
    $s.P += $Lit.Length
}
function Read-PxString($s) {
    $m = $script:ReString.Match($s.T, $s.P)
    if (-not $m.Success) { Stop-Px MalformedJson }
    $s.P += $m.Length
    return [regex]::Replace($m.Groups[1].Value, '\\(u[0-9A-Fa-f]{4}|.)', [Text.RegularExpressions.MatchEvaluator]{
            param($e) $c = $e.Groups[1].Value
            if ($c.Length -eq 5) { return [string][char][Convert]::ToInt32($c.Substring(1), 16) }
            switch -CaseSensitive ($c) { 'b' { "`b" } 'f' { "`f" } 'n' { "`n" } 'r' { "`r" } 't' { "`t" } default { $c } } })
}
function Read-PxValue($s, [int]$Depth) {
    Skip-PxWs $s
    if ($Depth -gt 32 -or $s.P -ge $s.T.Length) { Stop-Px MalformedJson }
    switch -CaseSensitive ([string]$s.T[$s.P]) {
        '{' { return @{ K = 'object'; V = (Read-PxContainer $s $Depth '}') } }
        '[' { $null = Read-PxContainer $s $Depth ']'; return @{ K = 'array'; V = $null } }
        '"' { return @{ K = 'string'; V = (Read-PxString $s) } }
        't' { Read-PxLiteral $s 'true'; return @{ K = 'bool'; V = $true } }
        'f' { Read-PxLiteral $s 'false'; return @{ K = 'bool'; V = $false } }
        'n' { Read-PxLiteral $s 'null'; return @{ K = 'null'; V = $null } }
    }
    $m = $script:ReNumber.Match($s.T, $s.P)
    if (-not $m.Success -or $m.Length -eq 0) { Stop-Px MalformedJson }
    $s.P += $m.Length
    return @{ K = 'number'; V = $m.Value }
}
function Read-PxContainer($s, [int]$Depth, [string]$Close) {
    $o = [Collections.Generic.Dictionary[string, object]]::new([StringComparer]::Ordinal)
    $s.P += 1
    if (Test-PxNext $s $Close) { $s.P += 1; return , $o }
    while ($true) {
        if ($Close -ceq '}') {
            if (-not (Test-PxNext $s '"')) { Stop-Px MalformedJson }
            $k = Read-PxString $s; Skip-PxWs $s; Read-PxLiteral $s ':'
            if ($o.ContainsKey($k)) { Stop-Px DuplicateField }
            $o[$k] = Read-PxValue $s ($Depth + 1)
        } else { $null = Read-PxValue $s ($Depth + 1) }
        if (Test-PxNext $s ',') { $s.P += 1; continue }
        Read-PxLiteral $s $Close
        return , $o
    }
}
function Get-PxField($o, [string]$Name, [string]$Kind, [string]$Pattern = '') {
    if (-not $o.ContainsKey($Name) -or $o[$Name].K -cne $Kind) { Stop-Px InvalidField $Name }
    $v = $o[$Name].V
    if ($Kind -ceq 'string' -and ($v.Trim().Length -eq 0 -or ($Pattern -and $v -cnotmatch $Pattern))) { Stop-Px InvalidField $Name }
    return $v
}
function ConvertTo-PxConfig($o) {
    foreach ($k in $o.Keys) { if ($script:Fields -cnotcontains $k -and $k -match $script:SecretKey) { Stop-Px SecretField } }
    foreach ($k in $o.Keys) { if ($script:Fields -cnotcontains $k) { Stop-Px UnknownField } }
    if ((Get-PxField $o 'schemaVersion' 'number') -cne '1') { Stop-Px InvalidField 'schemaVersion' }
    $out = [ordered]@{ schemaVersion = 1 }
    $out.targetId = Get-PxField $o 'targetId' 'string' $script:IdPattern
    $out.mode = Get-PxField $o 'mode' 'string' '^(Local|Remote)\z'
    $out.basePath = Get-PxField $o 'basePath' 'string'
    if (-not (Test-PxPathSyntax $out.basePath)) { Stop-Px InvalidField 'basePath' }
    if ($out.mode -ceq 'Local') {
        foreach ($f in $script:RemoteOnly) { if ($o.ContainsKey($f)) { Stop-Px ModeMismatch $f } }
        return [pscustomobject]$out
    }
    $uri = Get-PxField $o 'connectionUri' 'string' '^https://[^\s/?#@\\]+(/[^\s?#@\\]*)?\z'
    [Uri]$u = $null
    if (-not [Uri]::TryCreate($uri, [UriKind]::Absolute, [ref]$u) -or $u.Scheme -cne 'https' -or
        $u.UserInfo -or $u.Query -or $u.Fragment -or -not $u.Host) { Stop-Px InvalidField 'connectionUri' }
    $out.connectionUri = $uri
    $out.configurationName = Get-PxField $o 'configurationName' 'string' $script:IdPattern
    return [pscustomobject]$out
}
# Public API. ConfigPath: existing ordinary file outside RepositoryRoot; both absolute, canonical, drive-qualified,
# free of reparse points. Returns only validated properties (Local: 4, Remote: 6).
function Read-ProximaConfig {
    [CmdletBinding()]
    [OutputType([pscustomobject])]
    param([Parameter(Mandatory = $true)][string]$ConfigPath, [Parameter(Mandatory = $true)][string]$RepositoryRoot)
    $text = $null
    try {
        if (-not (Test-PxPathSyntax $ConfigPath)) { Stop-Px ConfigPathInvalid }
        if (-not (Test-PxPathSyntax $RepositoryRoot)) { Stop-Px RepositoryRootInvalid }
        $repo = Resolve-PxEntry $RepositoryRoot $false 'RepositoryRootNotFound'
        $file = Resolve-PxEntry $ConfigPath $true 'NotFound'
        $repoPrefix = $repo.FullName.TrimEnd('\') + '\'
        if ($file.FullName.StartsWith($repoPrefix, [StringComparison]::OrdinalIgnoreCase)) { Stop-Px InsideRepository }
        if ($file.Length -gt $script:MaxBytes) { Stop-Px TooLarge }
        $bytes = [IO.File]::ReadAllBytes($file.FullName)
        # Re-walk after reading: narrows (does not close) the window for a swap between check and read.
        $again = Resolve-PxEntry $ConfigPath $true 'Changed'
        if ($again.FullName -cne $file.FullName -or $again.Length -ne $bytes.Length -or
            $again.LastWriteTimeUtc -ne $file.LastWriteTimeUtc) { Stop-Px Changed }
        $text = ConvertFrom-PxUtf8 $bytes
        $state = @{ T = $text; P = 0 }
        $root = Read-PxValue $state 0
        Skip-PxWs $state
        if ($state.P -ne $text.Length) { Stop-Px MalformedJson }
        if ($root.K -cne 'object') { Stop-Px NotObject }
        return (ConvertTo-PxConfig $root.V)
    } catch {
        $code = 'Internal'; $field = ''
        if ($_.Exception.Data.Contains('PxCode')) { $code = [string]$_.Exception.Data['PxCode']; $field = [string]$_.Exception.Data['PxField'] }
        $PSCmdlet.ThrowTerminatingError((New-PxError $code $field))
    }
}
Export-ModuleMember -Function Read-ProximaConfig
