# ProximaConfig.psm1 - wp1271 r3 (PROXIMA-P1-S1). Standalone, read-only reader for ONE explicit Proxima
# target config file. No discovery, defaults, fallback or writes; reading never contacts the target.
# Fail closed: any path or value that is not provably safe is rejected. Errors have FullyQualifiedErrorId
# 'ProximaConfig.<Code>' and a fixed message that never echoes config keys, values, raw JSON or inner errors.
# Windows path semantics only: drive-qualified, local fixed drive, case-insensitive containment.
# r3 (H0 accepted repository files through SUBST and hardlink aliases on PS5.1 and PS7) - containment is decided
# on PHYSICAL paths read back from handles that stay open while verifying and reading, and multiply-linked files
# are rejected. Native calls are emitted in memory only (Reflection.Emit, Run access): no C# compiler, temp files,
# disk assembly cache or child processes.
Set-StrictMode -Version 3.0
$script:Fields = @('schemaVersion', 'targetId', 'mode', 'basePath', 'connectionUri', 'configurationName')
$script:RemoteOnly = @('connectionUri', 'configurationName')
$script:SecretKey = '(?i)pass|pwd|secret|token|credential|cookie|api.?key|auth|bearer|private|cert'
# ReparsePoint 0x400 | Offline 0x1000 | RecallOnOpen 0x40000 | RecallOnDataAccess 0x400000 (cloud placeholders).
$script:BadAttr = 0x441400
$script:MaxBytes = 65536
$script:ReWs = [regex]'\G[ \t\r\n]*'
$script:ReString = [regex]'\G"((?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4}))*)"'
$script:ReNumber = [regex]'\G-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?'
$script:Native = & {
    $ab = [Reflection.Emit.AssemblyBuilder]::DefineDynamicAssembly([Reflection.AssemblyName]::new('ProximaConfigNative'), [Reflection.Emit.AssemblyBuilderAccess]::Run)
    $tb = $ab.DefineDynamicModule('ProximaConfigNative').DefineType('ProximaConfigNative', [Reflection.TypeAttributes]'Public, Sealed, Abstract')
    $h = [Microsoft.Win32.SafeHandles.SafeFileHandle]
    $sigs = @(@('CreateFileW', $h, @([string], [uint32], [uint32], [IntPtr], [uint32], [uint32], [IntPtr])),
        @('GetFileInformationByHandle', [bool], @($h, [byte[]])), @('GetFinalPathNameByHandleW', [uint32], @($h, [char[]], [uint32], [uint32])))
    foreach ($s in $sigs) {
        $mb = $tb.DefinePInvokeMethod($s[0], 'kernel32.dll', [Reflection.MethodAttributes]'Public, Static, PinvokeImpl, HideBySig',
            [Reflection.CallingConventions]::Standard, $s[1], [type[]]$s[2], [Runtime.InteropServices.CallingConvention]::Winapi, [Runtime.InteropServices.CharSet]::Unicode)
        $mb.SetImplementationFlags($mb.GetMethodImplementationFlags() -bor [Reflection.MethodImplAttributes]::PreserveSig)
        for ($i = 0; $i -lt $s[2].Count; $i++) { if ($s[2][$i].IsArray) { $null = $mb.DefineParameter($i + 1, [Reflection.ParameterAttributes]'In, Out', $null) } }
    }
    $tb.CreateType()
}
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
    if ($Path.Length -gt 32000 -or $Path -notmatch '^[A-Za-z]:\\') { return $false }
    if ($Path.Length -eq 3) { return $true }
    foreach ($seg in $Path.Substring(3).Split([char]'\')) {
        if ($seg.Length -eq 0 -or $seg -match '[\x00-\x1f<>:"/|?*]|[. ]\z' -or
            $seg -match '^(?i:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[0-9]|LPT[0-9])(\..*)?\z') { return $false }
    }
    return $true
}
# Identity of an open handle: attributes, size, link count and the final path in the volume-GUID namespace
# (VOLUME_NAME_GUID = 1, normalized long names), so SUBST, 8.3, case and drive-letter spellings all collapse to one
# physical path. No volume GUID (network, unusual volumes) or any API failure is unverifiable.
function Get-PxNode($Handle) {
    $info = [byte[]]::new(52); $name = [char[]]::new(32768)
    if (-not $script:Native::GetFileInformationByHandle($Handle, $info)) { Stop-Px Unverifiable }
    $len = $script:Native::GetFinalPathNameByHandleW($Handle, $name, [uint32]$name.Length, [uint32]1)
    if ($len -eq 0 -or $len -ge $name.Length) { Stop-Px Unverifiable }
    return @{ Handle = $Handle; Attr = [BitConverter]::ToUInt32($info, 0); Links = [BitConverter]::ToUInt32($info, 40)
        Size = [long][BitConverter]::ToUInt32($info, 32) * 4294967296 + [BitConverter]::ToUInt32($info, 36); Final = [string]::new($name, 0, [int]$len) }
}
# Opens every component from the drive root and adds each handle to $Held (closed by the caller). Each component
# is opened without following a reparse point and must not be one, and its physical path must be exactly one
# segment below its parent's, so the held chain is the path that was given. 0x100081 = READ_DATA|READ_ATTRIBUTES|
# SYNCHRONIZE; share READ (+WRITE for directories) but never DELETE, so no held component can be renamed or
# replaced while held; 0x02200000 = BACKUP_SEMANTICS|OPEN_REPARSE_POINT. Returns the node of the last component.
function Open-PxChain([string]$Path, [bool]$File, [string]$Missing, $Held) {
    if ([IO.DriveInfo]::new($Path.Substring(0, 1)).DriveType -ne [IO.DriveType]::Fixed) { Stop-Px DriveUnsupported }
    $segs = @($Path.Substring(0, 3)); if ($Path.Length -gt 3) { $segs += $Path.Substring(3).Split([char]'\') }
    $sofar = ''; $node = $null
    for ($i = 0; $i -lt $segs.Count; $i++) {
        $sofar = $(if ($i) { $sofar.TrimEnd('\') + '\' + $segs[$i] } else { $segs[0] })
        $leaf = $File -and $i -eq $segs.Count - 1
        $h = $script:Native::CreateFileW('\\?\' + $sofar, [uint32]0x100081, [uint32]$(if ($leaf) { 1 } else { 3 }), [IntPtr]::Zero, [uint32]3, [uint32]0x02200000, [IntPtr]::Zero)
        $Held.Add($h)
        if ($h.IsInvalid) { if ([IO.Directory]::Exists($sofar) -or [IO.File]::Exists($sofar)) { Stop-Px Unverifiable }; Stop-Px $Missing }
        $parent = $node; $node = Get-PxNode $h
        if (($node.Attr -band $script:BadAttr) -ne 0) { Stop-Px ReparsePoint }
        $isDir = ($node.Attr -band 0x10) -ne 0
        if ($leaf -and $isDir) { Stop-Px NotAFile }
        if (-not $leaf -and -not $isDir) { Stop-Px $Missing }
        if ($null -ne $parent) {
            $pre = $parent.Final.TrimEnd('\') + '\'
            if ($node.Final.Length -le $pre.Length -or -not $node.Final.StartsWith($pre, [StringComparison]::OrdinalIgnoreCase) -or
                $node.Final.IndexOf([char]'\', $pre.Length) -ge 0) { Stop-Px Unverifiable }
        }
    }
    return $node
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
# targetId/configurationName: any Unicode text without whitespace, control characters or unpaired surrogates;
# no ASCII-only or length rule (the file itself is bounded). Values are returned exactly as given.
function Test-PxText([string]$V) {
    return $V.Length -gt 0 -and $V -notmatch '[\s\p{Cc}]|[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]'
}
# Absolute HTTPS URI (scheme case-insensitive) with a host. Userinfo, query and fragment are forbidden so no auth
# material can live in the JSON.
function Test-PxUri([string]$V) {
    [Uri]$u = $null
    return $V -match '^(?i:https)://[^\s\p{Cc}/?#@\\]+(/[^\s\p{Cc}?#@\\]*)?\z' -and [Uri]::TryCreate($V, [UriKind]::Absolute, [ref]$u) -and
        $u.Scheme -ceq 'https' -and [bool]$u.Host -and -not $u.UserInfo -and -not $u.Query -and -not $u.Fragment
}
function Get-PxField($o, [string]$Name, [string]$Kind, [scriptblock]$Valid) {
    if (-not $o.ContainsKey($Name) -or $o[$Name].K -cne $Kind -or -not (& $Valid $o[$Name].V)) { Stop-Px InvalidField $Name }
    return $o[$Name].V
}
function ConvertTo-PxConfig($o) {
    foreach ($k in $o.Keys) { if ($script:Fields -cnotcontains $k -and $k -match $script:SecretKey) { Stop-Px SecretField } }
    foreach ($k in $o.Keys) { if ($script:Fields -cnotcontains $k) { Stop-Px UnknownField } }
    $null = Get-PxField $o 'schemaVersion' 'number' { $args[0] -ceq '1' }
    $out = [ordered]@{ schemaVersion = 1 }
    $out.targetId = Get-PxField $o 'targetId' 'string' { Test-PxText $args[0] }
    $out.mode = Get-PxField $o 'mode' 'string' { $args[0] -cmatch '^(Local|Remote)\z' }
    $out.basePath = Get-PxField $o 'basePath' 'string' { Test-PxPathSyntax $args[0] }
    if ($out.mode -ceq 'Local') {
        foreach ($f in $script:RemoteOnly) { if ($o.ContainsKey($f)) { Stop-Px ModeMismatch $f } }
        return [pscustomobject]$out
    }
    $out.connectionUri = Get-PxField $o 'connectionUri' 'string' { Test-PxUri $args[0] }
    $out.configurationName = Get-PxField $o 'configurationName' 'string' { Test-PxText $args[0] }
    return [pscustomobject]$out
}
# Public API. ConfigPath: existing single-link ordinary file physically outside RepositoryRoot; both absolute,
# canonical, drive-qualified, free of reparse points. Returns only validated properties (Local: 4, Remote: 6).
function Read-ProximaConfig {
    [CmdletBinding()]
    [OutputType([pscustomobject])]
    param([Parameter(Mandatory = $true)][string]$ConfigPath, [Parameter(Mandatory = $true)][string]$RepositoryRoot)
    $text = $null
    $held = [Collections.Generic.List[IDisposable]]::new()
    try {
        if (-not (Test-PxPathSyntax $ConfigPath)) { Stop-Px ConfigPathInvalid }
        if (-not (Test-PxPathSyntax $RepositoryRoot)) { Stop-Px RepositoryRootInvalid }
        $repo = Open-PxChain $RepositoryRoot $false 'RepositoryRootNotFound' $held
        $file = Open-PxChain $ConfigPath $true 'NotFound' $held
        # Both physical paths come from handles still held; directories cannot be hard-linked, files can.
        if ($file.Final.StartsWith($repo.Final.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) { Stop-Px InsideRepository }
        if ($file.Links -ne 1) { Stop-Px MultiLink }
        if ($file.Size -gt $script:MaxBytes) { Stop-Px TooLarge }
        # The file handle shares READ only, so nobody can write it between the checks above and this read.
        $fs = [IO.FileStream]::new($file.Handle, [IO.FileAccess]::Read); $held.Add($fs)
        $bytes = [byte[]]::new($file.Size); $n = 0
        while ($n -lt $bytes.Length) { $k = $fs.Read($bytes, $n, $bytes.Length - $n); if ($k -le 0) { Stop-Px Changed }; $n += $k }
        if ($fs.ReadByte() -ne -1) { Stop-Px Changed }
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
    } finally {
        for ($i = $held.Count - 1; $i -ge 0; $i--) { $held[$i].Dispose() }
    }
}
Export-ModuleMember -Function Read-ProximaConfig
