# ProximaConfig.psm1 - wp1271 r4 (PROXIMA-P1-S1). Standalone, read-only reader for ONE explicit Proxima
# target config file. No discovery, defaults, fallback or writes; reading never contacts the target.
# Fail closed: any path that is not provably safe, and any value outside the schema, is rejected. Errors have
# FullyQualifiedErrorId 'ProximaConfig.<Code>' and a fixed message that never echoes config keys, values, raw JSON or inner errors.
# Windows path semantics only: drive-qualified, local fixed drive, case-insensitive containment.
# r3 (H0 accepted repository files through SUBST and hardlink aliases on PS5.1 and PS7) - containment is decided
# on PHYSICAL paths read back from handles that stay open while verifying and reading, and multiply-linked files
# are rejected. Native calls are emitted in memory only (Reflection.Emit, Run access): no C# compiler, temp files,
# disk assembly cache or child processes.
# r4 (review 9e799cda: a SUBST backed through a junction, and a volume also mounted inside RepositoryRoot used by its
# own letter, both passed) - drive letters resolve via QueryDosDeviceW with SUBST targets verified as full chains, and
# the config volume's mount folders must not be reachable from the repository; both re-queried after reading. Not
# covered: junctions/symlinks stored INSIDE the repository pointing out to the config (needs a repository tree walk).
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
$script:ReVolume = [regex]'^\\\\\?\\Volume\{[0-9A-Fa-f-]{36}\}\\'
$script:Native = & {
    $ab = [Reflection.Emit.AssemblyBuilder]::DefineDynamicAssembly([Reflection.AssemblyName]::new('ProximaConfigNative'), [Reflection.Emit.AssemblyBuilderAccess]::Run)
    $tb = $ab.DefineDynamicModule('ProximaConfigNative').DefineType('ProximaConfigNative', [Reflection.TypeAttributes]'Public, Sealed, Abstract')
    $h = [Microsoft.Win32.SafeHandles.SafeFileHandle]
    $sigs = @(@('CreateFileW', $h, @([string], [uint32], [uint32], [IntPtr], [uint32], [uint32], [IntPtr])),
        @('GetFileInformationByHandle', [bool], @($h, [byte[]])), @('GetFinalPathNameByHandleW', [uint32], @($h, [char[]], [uint32], [uint32])),
        @('QueryDosDeviceW', [uint32], @([string], [char[]], [uint32])), @('GetVolumePathNamesForVolumeNameW', [bool], @([string], [char[]], [uint32], [uint32[]])))
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
# Opens one path, not following a final reparse point; the handle goes to $Ctx.Held. 0x100081 = READ_DATA|READ_ATTRIBUTES|
# SYNCHRONIZE; share READ (+WRITE for dirs) never DELETE, so nothing held is renamed; 0x02200000 = BACKUP|OPEN_REPARSE_POINT.
function Open-PxNode([string]$Path, [uint32]$Share, [string]$Missing, $Ctx) {
    $h = $script:Native::CreateFileW('\\?\' + $Path, [uint32]0x100081, $Share, [IntPtr]::Zero, [uint32]3, [uint32]0x02200000, [IntPtr]::Zero)
    $Ctx.Held.Add($h)
    if ($h.IsInvalid) { if ([IO.Directory]::Exists($Path) -or [IO.File]::Exists($Path)) { Stop-Px Unverifiable }; Stop-Px $Missing }
    return (Get-PxNode $h)
}
# Physical path $Child is exactly one segment below physical path $Parent.
function Test-PxChild([string]$Parent, [string]$Child) {
    $pre = $Parent.TrimEnd('\') + '\'
    return $Child.Length -gt $pre.Length -and $Child.StartsWith($pre, [StringComparison]::OrdinalIgnoreCase) -and $Child.IndexOf([char]'\', $pre.Length) -lt 0
}
# Current target of a drive letter ('C:') in this session: '\Device\...' for a volume, '\??\X:\...' for SUBST.
function Get-PxDosTarget([string]$Drive) {
    $buf = [char[]]::new(32768)
    if ($script:Native::QueryDosDeviceW($Drive, $buf, [uint32]$buf.Length) -eq 0) { Stop-Px Unverifiable }
    return [string]::new($buf).Split([char]0)[0]
}
# Every path a volume ('\\?\Volume{guid}\') is reachable at - drive roots and mount folders - sorted, one per line.
function Get-PxVolumePaths([string]$Volume) {
    $buf = [char[]]::new(32768); $len = [uint32[]]::new(1)
    if (-not $script:Native::GetVolumePathNamesForVolumeNameW($Volume, $buf, [uint32]$buf.Length, $len)) { Stop-Px Unverifiable }
    $names = [Collections.Generic.List[string]]::new()
    foreach ($n in [string]::new($buf).Split([char]0)) { if (-not $n) { break }; $names.Add($n) }
    $names.Sort([StringComparer]::OrdinalIgnoreCase); return ($names -join "`n")
}
# Drive-root identity (r4): a volume letter must open as exactly that volume's root; a SUBST target is verified as a full
# chain (junctions in its backing ancestors reject) and the root must be its last directory. Other targets (raw device
# sub-paths, UNC) and mapping chains deeper than 8 (cycles) are unverifiable.
function Open-PxRoot([string]$Drive, $Ctx, [int]$Depth) {
    if ($Depth -gt 8) { Stop-Px Unverifiable }
    $target = Get-PxDosTarget $Drive; $Ctx.Recheck.Add(@('dos', $Drive, $target)); $want = $null
    if ($target.StartsWith('\??\')) { $want = Get-PxBackingFinal $target.Substring(4) $Ctx $Depth }
    elseif (-not $target.StartsWith('\Device\')) { Stop-Px Unverifiable }
    $node = Open-PxNode "$Drive\" 3 'Unverifiable' $Ctx
    if ($null -eq $want) { $want = $script:ReVolume.Match($node.Final).Value }
    if (-not $node.Final.Equals($want, [StringComparison]::OrdinalIgnoreCase)) { Stop-Px Unverifiable }
    return $node
}
function Get-PxBackingFinal([string]$Back, $Ctx, [int]$Depth) {
    if ($Back.Length -gt 3) { $Back = $Back.TrimEnd('\') }; if (-not (Test-PxPathSyntax $Back)) { Stop-Px Unverifiable }
    return (Open-PxChain $Back $false 'Unverifiable' $Ctx ($Depth + 1)).Final
}
# Opens every component from the verified drive root; none may be a reparse point and each physical path must be exactly
# one segment below its parent's, so the held chain is the path that was given. Returns the last component's node.
function Open-PxChain([string]$Path, [bool]$File, [string]$Missing, $Ctx, [int]$Depth) {
    if ([IO.DriveInfo]::new($Path.Substring(0, 1)).DriveType -ne [IO.DriveType]::Fixed) { Stop-Px DriveUnsupported }
    $node = Open-PxRoot $Path.Substring(0, 2) $Ctx $Depth
    $segs = @(); if ($Path.Length -gt 3) { $segs = $Path.Substring(3).Split([char]'\') }
    if ($File -and $segs.Count -eq 0) { Stop-Px NotAFile }
    $sofar = $Path.Substring(0, 2)
    for ($i = 0; $i -lt $segs.Count; $i++) {
        $sofar += '\' + $segs[$i]; $leaf = $File -and $i -eq $segs.Count - 1
        $parent = $node; $node = Open-PxNode $sofar $(if ($leaf) { 1 } else { 3 }) $Missing $Ctx
        if (($node.Attr -band $script:BadAttr) -ne 0) { Stop-Px ReparsePoint }
        $isDir = ($node.Attr -band 0x10) -ne 0
        if ($leaf -and $isDir) { Stop-Px NotAFile }
        if (-not $leaf -and -not $isDir) { Stop-Px $Missing }
        if (-not (Test-PxChild $parent.Final $node.Final)) { Stop-Px Unverifiable }
    }
    return $node
}
# Physical containment (r4): inside if the physical path is under the repository, or a mount folder of its volume is
# inside, directly or via mount folders of THAT folder's volume (each volume once, depth 8). Mount folders are held
# like chain components (no DELETE sharing); drive letters are not folders.
function Assert-PxOutside([string]$Final, [string]$RepoPrefix, $Ctx, [int]$Depth) {
    if ($Final.StartsWith($RepoPrefix, [StringComparison]::OrdinalIgnoreCase)) { Stop-Px InsideRepository }
    $vol = $script:ReVolume.Match($Final).Value
    if (-not $vol -or $Depth -gt 8) { Stop-Px Unverifiable }
    if (-not $Ctx.Seen.Add($vol)) { return }
    $paths = Get-PxVolumePaths $vol; $Ctx.Recheck.Add(@('vol', $vol, $paths))
    foreach ($p in $paths.Split([char]"`n")) {
        if ($p.Length -le 3) { continue }
        $p = $p.TrimEnd('\'); if (-not (Test-PxPathSyntax $p)) { Stop-Px Unverifiable }
        $mount = Open-PxNode $p 3 'Unverifiable' $Ctx
        if (($mount.Attr -band 0x400) -eq 0) { Stop-Px Unverifiable }
        Assert-PxOutside $mount.Final $RepoPrefix $Ctx ($Depth + 1)
    }
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
# targetId/configurationName = the schema's 'nonempty string', literally: length >= 1 and valid Unicode (no unpaired
# surrogate). Whitespace-only text (ASCII or Unicode) and JSON-escaped controls are valid values; unescaped controls are
# already malformed JSON. No token, nonblank, control-free, ASCII-only or length rule (the file itself is bounded).
# Returned exactly: never trimmed, normalized or truncated. S1 only returns them - never used as paths or commands.
# r7/r8 (reviews 42c31cf4, 0fcd56b7: spaces, then blank and escaped-control names were rejected without schema basis).
function Test-PxText([string]$V) {
    return $V.Length -gt 0 -and $V -notmatch '[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]'
}
# Absolute HTTPS URI (scheme case-insensitive) with a host. Userinfo, query and fragment are forbidden so no auth
# material can live in the JSON. Only the AUTHORITY excludes '@'; a path may contain it (r4: https://h/a@b is valid).
function Test-PxUri([string]$V) {
    [Uri]$u = $null
    return $V -match '^(?i:https)://[^\s\p{Cc}/?#@\\]+(/[^\s\p{Cc}?#\\]*)?\z' -and [Uri]::TryCreate($V, [UriKind]::Absolute, [ref]$u) -and
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
# Public API. ConfigPath: existing single-link ordinary file physically outside RepositoryRoot and on no volume mounted
# inside it; both absolute, canonical, drive-qualified, free of reparse points (SUBST backing paths included).
# Returns only validated properties (Local: 4, Remote: 6).
function Read-ProximaConfig {
    [CmdletBinding()]
    [OutputType([pscustomobject])]
    param([Parameter(Mandatory = $true)][string]$ConfigPath, [Parameter(Mandatory = $true)][string]$RepositoryRoot)
    $text = $null
    $ctx = @{ Held = [Collections.Generic.List[IDisposable]]::new(); Recheck = [Collections.Generic.List[object]]::new()
        Seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase) }
    try {
        if (-not (Test-PxPathSyntax $ConfigPath)) { Stop-Px ConfigPathInvalid }
        if (-not (Test-PxPathSyntax $RepositoryRoot)) { Stop-Px RepositoryRootInvalid }
        $repo = Open-PxChain $RepositoryRoot $false 'RepositoryRootNotFound' $ctx 0
        $file = Open-PxChain $ConfigPath $true 'NotFound' $ctx 0
        # Both physical paths come from handles still held; directories cannot be hard-linked, files can.
        Assert-PxOutside $file.Final ($repo.Final.TrimEnd('\') + '\') $ctx 0
        if ($file.Links -ne 1) { Stop-Px MultiLink }
        if ($file.Size -gt $script:MaxBytes) { Stop-Px TooLarge }
        # The file handle shares READ only, so nobody can write it between the checks above and this read.
        $fs = [IO.FileStream]::new($file.Handle, [IO.FileAccess]::Read); $ctx.Held.Add($fs)
        $bytes = [byte[]]::new($file.Size); $n = 0
        while ($n -lt $bytes.Length) { $k = $fs.Read($bytes, $n, $bytes.Length - $n); if ($k -le 0) { Stop-Px Changed }; $n += $k }
        if ($fs.ReadByte() -ne -1) { Stop-Px Changed }
        # Mappings/mount lists changed since verifying reject (narrows, does not close, a change-and-restore window).
        foreach ($c in $ctx.Recheck) { if ($(if ($c[0] -ceq 'dos') { Get-PxDosTarget $c[1] } else { Get-PxVolumePaths $c[1] }) -cne $c[2]) { Stop-Px Changed } }
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
        for ($i = $ctx.Held.Count - 1; $i -ge 0; $i--) { $ctx.Held[$i].Dispose() }
    }
}
Export-ModuleMember -Function Read-ProximaConfig
