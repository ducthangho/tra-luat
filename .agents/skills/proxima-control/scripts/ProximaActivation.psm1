Set-StrictMode -Version 3.0

function New-ActivationResult([string]$Code, [bool]$Ok = $false, [hashtable]$Details = @{}) {
    $Details['ok'] = $Ok
    $Details['code'] = $Code
    return [pscustomobject]$Details
}

# JSON tokenizer and object parser follow ProximaConfig's RFC 8259 parser.
# Preserve case-distinct keys, value types, and string timestamps across hosts.
$script:ReWs = [regex]'\G[ \t\r\n]*'
$script:ReString = [regex]'\G"((?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4}))*)"'
$script:ReNumber = [regex]'\G-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?'

function Stop-ActivationJson([string]$Reason) { throw "Invalid JSON: $Reason" }

function Skip-ActivationJsonWs($s) { $s.P += $script:ReWs.Match($s.T, $s.P).Length }
function Test-ActivationJsonNext($s, [string]$Ch) { Skip-ActivationJsonWs $s; return ($s.P -lt $s.T.Length -and $s.T[$s.P] -ceq $Ch) }
function Read-ActivationJsonLiteral($s, [string]$Lit) {
    if ($s.P + $Lit.Length -gt $s.T.Length -or [string]::CompareOrdinal($s.T, $s.P, $Lit, 0, $Lit.Length) -ne 0) { Stop-ActivationJson MalformedJson }
    $s.P += $Lit.Length
}
function Read-ActivationJsonString($s) {
    $m = $script:ReString.Match($s.T, $s.P)
    if (-not $m.Success) { Stop-ActivationJson MalformedJson }
    $s.P += $m.Length
    return [regex]::Replace($m.Groups[1].Value, '\\(u[0-9A-Fa-f]{4}|.)', [Text.RegularExpressions.MatchEvaluator]{
            param($e) $c = $e.Groups[1].Value
            if ($c.Length -eq 5) { return [string][char][Convert]::ToInt32($c.Substring(1), 16) }
            switch -CaseSensitive ($c) { 'b' { "`b" } 'f' { "`f" } 'n' { "`n" } 'r' { "`r" } 't' { "`t" } default { $c } } })
}
function Read-ActivationJsonValue($s, [int]$Depth) {
    Skip-ActivationJsonWs $s
    if ($Depth -gt 32 -or $s.P -ge $s.T.Length) { Stop-ActivationJson MalformedJson }
    switch -CaseSensitive ([string]$s.T[$s.P]) {
        '{' { return @{ K = 'object'; V = (Read-ActivationJsonContainer $s $Depth '}') } }
        '[' { $null = Read-ActivationJsonContainer $s $Depth ']'; return @{ K = 'array'; V = $null } }
        '"' { return @{ K = 'string'; V = (Read-ActivationJsonString $s) } }
        't' { Read-ActivationJsonLiteral $s 'true'; return @{ K = 'bool'; V = $true } }
        'f' { Read-ActivationJsonLiteral $s 'false'; return @{ K = 'bool'; V = $false } }
        'n' { Read-ActivationJsonLiteral $s 'null'; return @{ K = 'null'; V = $null } }
    }
    $m = $script:ReNumber.Match($s.T, $s.P)
    if (-not $m.Success -or $m.Length -eq 0) { Stop-ActivationJson MalformedJson }
    $s.P += $m.Length
    return @{ K = 'number'; V = $m.Value }
}
function Read-ActivationJsonContainer($s, [int]$Depth, [string]$Close) {
    $o = [Collections.Generic.Dictionary[string, object]]::new([StringComparer]::Ordinal)
    $s.P += 1
    if (Test-ActivationJsonNext $s $Close) { $s.P += 1; return , $o }
    while ($true) {
        if ($Close -ceq '}') {
            if (-not (Test-ActivationJsonNext $s '"')) { Stop-ActivationJson MalformedJson }
            $k = Read-ActivationJsonString $s; Skip-ActivationJsonWs $s; Read-ActivationJsonLiteral $s ':'
            if ($o.ContainsKey($k)) { Stop-ActivationJson DuplicateField }
            $o[$k] = Read-ActivationJsonValue $s ($Depth + 1)
        } else { $null = Read-ActivationJsonValue $s ($Depth + 1) }
        if (Test-ActivationJsonNext $s ',') { $s.P += 1; continue }
        Read-ActivationJsonLiteral $s $Close
        return , $o
    }
}
function Read-ActivationJson([string]$Path) {
    $text = [IO.File]::ReadAllText($Path, [Text.UTF8Encoding]::new($false, $true))
    $state = @{ T = $text; P = 0 }
    $root = Read-ActivationJsonValue $state 0
    Skip-ActivationJsonWs $state
    if ($state.P -ne $text.Length -or $root.K -cne 'object') { throw 'Expected one JSON object.' }
    return , $root.V
}

function Get-ActivationField($Object, [string]$Name) {
    if ($Object -is [hashtable]) { return , $Object[$Name] }
    if ($Object -isnot [Collections.Generic.Dictionary[string, object]]) { throw "Expected an object with field $Name." }
    if (-not $Object.ContainsKey($Name)) { return }
    $field = $Object[$Name]
    switch -CaseSensitive ($field.K) {
        'object' { return , $field.V }
        'string' { return $field.V }
        'bool' { return $field.V }
        'number' {
            $integer = [long]0
            if ($field.V -cmatch '^-?[0-9]+\z' -and
                [long]::TryParse($field.V, [Globalization.NumberStyles]::AllowLeadingSign,
                    [Globalization.CultureInfo]::InvariantCulture, [ref]$integer)) { return $integer }
        }
    }
}

function Test-ActivationInteger($Value) {
    return ($Value -is [int] -or $Value -is [long])
}

function Assert-ArtifactRelative([string]$Relative) {
    if ($Relative -cmatch '(^|/)\.{1,2}(/|$)|^/|/$|//|[\\:\x00]' -or $Relative.Length -eq 0) {
        throw "Invalid manifest path: $Relative"
    }
}

function Read-ArtifactEntry([string]$Relative, $Entry) {
    Assert-ArtifactRelative $Relative
    $size = Get-ActivationField $Entry 'bytes'
    $sha = Get-ActivationField $Entry 'sha256'
    if (-not (Test-ActivationInteger $size) -or $size -lt 0 -or
        $sha -isnot [string] -or $sha -cnotmatch '^[a-fA-F0-9]{64}\z') {
        throw "Invalid manifest entry: $Relative"
    }
    return @{ bytes = $size; sha256 = $sha }
}

function Test-ArtifactEntry($File, $Expected) {
    $stream = [IO.File]::OpenRead($File.FullName)
    try {
        if ($stream.Length -ne $Expected.bytes) { return $false }
        $sha = [Security.Cryptography.SHA256]::Create()
        try { $hex = [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-', '') }
        finally { $sha.Dispose() }
        return [string]::Equals($hex, $Expected.sha256, [StringComparison]::OrdinalIgnoreCase)
    } finally { $stream.Dispose() }
}

function Test-ActivationRootedPath($Path) {
    # Fully qualified only: C:\x or \\server\share on Windows, /x elsewhere.
    # Drive-relative (C:foo) and current-drive-relative (\foo) spellings depend on process state.
    if ($Path -isnot [string] -or [string]::IsNullOrWhiteSpace($Path)) { return $false }
    try { if (-not [IO.Path]::IsPathRooted($Path)) { return $false } } catch { return $false }
    if ([IO.Path]::DirectorySeparatorChar -eq [char]'\') {
        return ($Path -cmatch '^(?:[A-Za-z]:[\\/]|[\\/]{2}[^\\/])')
    }
    return $Path.StartsWith('/', [StringComparison]::Ordinal)
}

function ConvertTo-ActivationFullPath([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    if ($full.Length -gt [IO.Path]::GetPathRoot($full).Length) {
        $full = $full.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    }
    return $full
}

function Resolve-ActivationPath($Value, [string]$Name) {
    if (-not (Test-ActivationRootedPath $Value)) { throw "$Name must be a fully qualified path." }
    return (ConvertTo-ActivationFullPath $Value)
}

function Test-ActivationReparsePoint([string]$Path) {
    try { $attributes = [IO.File]::GetAttributes($Path) }
    catch [IO.FileNotFoundException], [IO.DirectoryNotFoundException] { return $false }
    return (($attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)
}

function Test-ProximaArtifactTree {
    [CmdletBinding()]
    param(
        [Parameter()][AllowNull()]$Root,
        [Parameter()][AllowNull()]$ManifestPath,
        [Parameter()][AllowNull()]$MutableRelative,
        [Parameter()][AllowNull()]$Override
    )
    $ErrorActionPreference = 'Stop'
    $extra = [Collections.Generic.List[string]]::new()
    $missing = [Collections.Generic.List[string]]::new()
    $changed = [Collections.Generic.List[string]]::new()
    $extraDirs = [Collections.Generic.List[string]]::new()
    $verified = 0
    $errorText = $null
    $rootText = $null
    if ($Root -is [string]) { $rootText = $Root }
    try {
        $rootText = Resolve-ActivationPath $Root 'Root'
        $manifestFile = Resolve-ActivationPath $ManifestPath 'ManifestPath'
        if ($null -eq $Override) { $Override = @{} }
        if ($Override -isnot [hashtable]) { throw 'Override must be a hashtable.' }
        $mutableNames = [Collections.Generic.List[string]]::new()
        if ($null -ne $MutableRelative) {
            foreach ($name in @($MutableRelative)) {
                if ($name -isnot [string]) { throw 'MutableRelative entries must be strings.' }
                $name = $name.Replace('\', '/')
                Assert-ArtifactRelative $name
                $mutableNames.Add($name)
            }
        }
        $rootDir = [IO.DirectoryInfo]::new($rootText)
        $comparer = [StringComparer]::OrdinalIgnoreCase
        $files = [Collections.Generic.Dictionary[string, IO.FileInfo]]::new($comparer)
        $seen = [Collections.Generic.HashSet[string]]::new($comparer)
        $todo = [Collections.Generic.Stack[object]]::new()
        $todo.Push(@{ dir = $rootDir; relative = '' })
        $reparse = $false
        $duplicate = $false
        while ($todo.Count -gt 0) {
            $item = $todo.Pop()
            $dir = $item.dir
            $attributes = $dir.Attributes
            if ([int]$attributes -eq -1) { throw "Directory unavailable: $($dir.FullName)" }
            if (($attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                $reparse = $true
                continue
            }
            $children = $dir.GetFileSystemInfos()
            if ($children.Length -eq 0 -and $item.relative) { $extraDirs.Add($item.relative) }
            foreach ($child in $children) {
                $relative = $child.Name
                if ($item.relative) { $relative = $item.relative + '/' + $relative }
                if (-not $seen.Add($relative)) { $duplicate = $true }
                if (($child.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                    $reparse = $true
                } elseif ($child -is [IO.DirectoryInfo]) {
                    $todo.Push(@{ dir = $child; relative = $relative })
                } elseif (-not $files.ContainsKey($relative)) {
                    $files.Add($relative, $child)
                }
            }
        }

        $expected = [Collections.Generic.Dictionary[string, object]]::new($comparer)
        $manifest = Read-ActivationJson $manifestFile
        # A bare manifest can also contain a file literally named "files".
        if ($manifest.PSBase.Count -eq 1 -and $manifest.ContainsKey('files') -and $manifest['files'].K -ceq 'object') {
            $wrapped = $manifest['files'].V
            if (-not $wrapped.ContainsKey('bytes') -or $wrapped['bytes'].K -ceq 'object') { $manifest = $wrapped }
        }
        foreach ($relative in $manifest.PSBase.Keys) {
            $entry = Read-ArtifactEntry $relative (Get-ActivationField $manifest $relative)
            if ($expected.ContainsKey($relative)) { $duplicate = $true }
            $expected[$relative] = $entry
        }
        foreach ($relative in $Override.PSBase.Keys) {
            if ($relative -isnot [string]) { throw 'Override keys must be strings.' }
            $expected[$relative] = Read-ArtifactEntry $relative $Override[$relative]
        }
        $mutable = [Collections.Generic.HashSet[string]]::new($comparer)
        foreach ($name in $mutableNames) {
            # A mutable name that matches nothing is a configuration error, not an extra file.
            if (-not $expected.ContainsKey($name)) { throw "MutableRelative entry is not in the manifest or override: $name" }
            $null = $mutable.Add($name)
        }
        $unlistedDirs = [Collections.Generic.List[string]]::new()
        foreach ($relative in $extraDirs) {
            if (-not $expected.ContainsKey($relative)) { $unlistedDirs.Add($relative) }
        }
        $unlistedDirs.Sort($comparer)
        $extraDirs = $unlistedDirs

        $actualPaths = [Collections.Generic.List[string]]::new($files.PSBase.Keys)
        $actualPaths.Sort($comparer)
        foreach ($relative in $actualPaths) {
            if (-not $expected.ContainsKey($relative)) {
                if ($extra.Count -lt 100) { $extra.Add($relative) }
            }
        }

        $expectedPaths = [Collections.Generic.List[string]]::new($expected.PSBase.Keys)
        $expectedPaths.Sort($comparer)
        foreach ($relative in $expectedPaths) {
            if ($mutable.Contains($relative)) { continue }
            if (-not $files.ContainsKey($relative)) {
                if ($missing.Count -lt 100) { $missing.Add($relative) }
            } elseif (-not (Test-ArtifactEntry $files[$relative] $expected[$relative])) {
                if ($changed.Count -lt 100) { $changed.Add($relative) }
            } else {
                $verified++
            }
        }
        $code = if ($reparse) { 'REPARSE_POINT' }
            elseif ($duplicate) { 'DUPLICATE_CASE' }
            elseif ($extra.Count) { 'ARTIFACT_EXTRA' }
            elseif ($missing.Count) { 'ARTIFACT_MISSING' }
            elseif ($changed.Count) { 'ARTIFACT_CHANGED' }
            else { 'OK' }
    } catch {
        $code = 'NOT_MEASURED'
        $errorText = $_.Exception.Message
    }
    $details = @{ root = $rootText; verified_files = $verified; extra = $extra.ToArray()
        missing = $missing.ToArray(); changed = $changed.ToArray(); extra_dirs = $extraDirs.ToArray() }
    if ($null -ne $errorText) { $details.error = $errorText }
    return (New-ActivationResult $code ($code -ceq 'OK') $details)
}

$script:ReArgument = [regex]'(?:[^\s"]|"[^"]*"?)+'
$script:ReUserDataDir = [regex]::new('^(?:--|-|/)user-data-dir(?:=(.*))?\z',
    [Text.RegularExpressions.RegexOptions]'IgnoreCase, CultureInvariant, Singleline')
$script:ReLockLine = [regex]'\A[0-9]+\t[^\t\r\n]+\t[^\t\r\n]+\r?\n?\z'
$script:LockName = '.proxima-activation.lock'
$script:LockMaxBytes = 512

function Test-ProximaProcessName($Name, [bool]$RequireExe) {
    if ($Name -isnot [string]) { return $false }
    if (-not $Name.StartsWith('Proxima', [StringComparison]::OrdinalIgnoreCase)) { return $false }
    return (-not $RequireExe -or $Name.EndsWith('.exe', [StringComparison]::OrdinalIgnoreCase))
}

function Get-ProfileCommandLineState([string]$CommandLine, [string]$ProfilePath) {
    # 'match': a user-data-dir switch names this profile. 'unknown': a switch value cannot be
    # resolved without the other process's working directory. 'other': neither.
    # Quotes are removed per token, so "--user-data-dir=C:\a b" and --user-data-dir="C:\a b" agree.
    $tokens = [Collections.Generic.List[string]]::new()
    foreach ($match in $script:ReArgument.Matches($CommandLine)) { $tokens.Add($match.Value.Replace('"', '')) }
    $state = 'other'
    for ($index = 0; $index -lt $tokens.Count; $index++) {
        $flag = $script:ReUserDataDir.Match($tokens[$index])
        if (-not $flag.Success) { continue }
        $value = ''
        if ($flag.Groups[1].Success) {
            $value = $flag.Groups[1].Value
        } elseif ($index + 1 -lt $tokens.Count) {
            $index++
            $value = $tokens[$index]
        }
        $candidate = $null
        if (Test-ActivationRootedPath $value) {
            try { $candidate = ConvertTo-ActivationFullPath $value } catch { $candidate = $null }
        }
        if ($null -eq $candidate) {
            $state = 'unknown'
            continue
        }
        # Whole-path equality only; a prefix test would confuse prof with prof2 or prof\sub.
        if ([string]::Equals($candidate, $ProfilePath, [StringComparison]::OrdinalIgnoreCase)) { return 'match' }
    }
    return $state
}

function Get-ProfileBusyState([scriptblock]$ProcessProvider, [string]$ProfilePath) {
    # One snapshot: 'busy' (pid, rule), 'unknown' (pid, error) or 'clear'. A definite busy
    # finding wins over an unreadable process; an unreadable process is never read as clear.
    $processes = @(& $ProcessProvider)
    $self = $false
    foreach ($process in $processes) {
        if ($null -eq $process) { throw 'Process snapshot contains an empty entry.' }
        if ($process.ProcessId -eq $PID) { $self = $true }
    }
    # An empty or filtered snapshot is not evidence that the profile is unused.
    if (-not $self) { throw "Process snapshot does not contain the current process (pid $PID)." }
    $unknown = $null
    foreach ($process in $processes) {
        if (-not (Test-ProximaProcessName $process.Name $true)) { continue }
        $commandLine = $process.CommandLine
        $state = 'unknown'
        $reason = 'has no readable command line (elevated or owned by another user)'
        if ($commandLine -is [string] -and -not [string]::IsNullOrWhiteSpace($commandLine)) {
            $state = Get-ProfileCommandLineState $commandLine $ProfilePath
            $reason = 'has a user-data-dir value that is not a fully qualified path'
        }
        if ($state -ceq 'match') {
            return @{ state = 'busy'; pid = $process.ProcessId; rule = 'command_line' }
        }
        if ($state -ceq 'unknown' -and $null -eq $unknown) {
            $unknown = @{ state = 'unknown'; pid = $process.ProcessId
                error = "Proxima process pid $($process.ProcessId) $reason; profile use was not measured." }
        }
    }
    foreach ($name in 'rest-port.json', 'ipc-port.json') {
        $path = [IO.Path]::Combine($ProfilePath, $name)
        try { $data = Read-ActivationJson $path }
        catch [IO.FileNotFoundException] { continue }
        $discoveryPid = Get-ActivationField $data 'pid'
        if (-not (Test-ActivationInteger $discoveryPid) -or $discoveryPid -le 0) {
            throw "Invalid pid in $name."
        }
        foreach ($process in $processes) {
            if ($process.ProcessId -eq $discoveryPid -and (Test-ProximaProcessName $process.Name $false)) {
                return @{ state = 'busy'; pid = $process.ProcessId; rule = "discovery:$name" }
            }
        }
    }
    if ($null -ne $unknown) { return $unknown }
    return @{ state = 'clear' }
}

function Assert-ProfileLockTarget([string]$ProfilePath, [string]$LockPath) {
    # Opening through a link would lock, and later truncate, a file outside the profile.
    if (Test-ActivationReparsePoint $ProfilePath) { throw 'ProfileDir is a reparse point.' }
    if (Test-ActivationReparsePoint $LockPath) { throw 'The profile lock file is a reparse point.' }
}

function Enter-ProximaProfileGuard {
    [CmdletBinding()]
    param(
        [Parameter()][AllowNull()]$ProfileDir,
        [Parameter()][AllowNull()]$ProcessProvider = { Get-CimInstance -ClassName Win32_Process -ErrorAction Stop }
    )
    $ErrorActionPreference = 'Stop'
    $stream = $null
    $keep = $false
    try {
        if ($ProcessProvider -isnot [scriptblock]) { throw 'ProcessProvider must be a script block.' }
        $profilePath = Resolve-ActivationPath $ProfileDir 'ProfileDir'
        if (-not [IO.Directory]::Exists($profilePath)) { throw 'ProfileDir must be an existing directory.' }
        $lockPath = [IO.Path]::Combine($profilePath, $script:LockName)
        Assert-ProfileLockTarget $profilePath $lockPath

        $before = Get-ProfileBusyState $ProcessProvider $profilePath
        if ($before.state -ceq 'busy') {
            return (New-ActivationResult 'PROFILE_BUSY' $false @{ pid = $before.pid; rule = $before.rule })
        }
        if ($before.state -cne 'clear') {
            return (New-ActivationResult 'NOT_MEASURED' $false @{ pid = $before.pid; error = $before.error })
        }

        try {
            $stream = [IO.File]::Open($lockPath, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
        } catch [IO.IOException] {
            $exception = $_.Exception
            while ($exception -isnot [IO.IOException] -and $null -ne $exception.InnerException) {
                $exception = $exception.InnerException
            }
            $nativeError = $exception.HResult -band 0xffff
            if ($nativeError -in 32, 33 -or
                ($nativeError -eq 11 -and [Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT)) {
                return (New-ActivationResult 'PROFILE_LOCKED')
            }
            throw
        }
        # Re-check now that the handle is held, then refuse to overwrite anything that is not our own record.
        Assert-ProfileLockTarget $profilePath $lockPath
        $length = $stream.Length
        if ($length -gt $script:LockMaxBytes) { throw "The profile lock file is larger than $($script:LockMaxBytes) bytes; not truncating it." }
        $existing = [byte[]]::new([int]$length)
        $read = 0
        while ($read -lt $existing.Length) {
            $count = $stream.Read($existing, $read, $existing.Length - $read)
            if ($count -le 0) { throw 'The profile lock file changed while it was read.' }
            $read += $count
        }
        if ($existing.Length -gt 0) {
            $shaped = $false
            try { $shaped = $script:ReLockLine.IsMatch([Text.UTF8Encoding]::new($false, $true).GetString($existing)) }
            catch { $shaped = $false }
            if (-not $shaped) { throw 'The profile lock file does not hold a pid/utc/host record; not truncating it.' }
        }

        # The first snapshot predates the lock; a second one closes that window for other guard callers.
        $after = Get-ProfileBusyState $ProcessProvider $profilePath
        if ($after.state -ceq 'busy') {
            return (New-ActivationResult 'PROFILE_BUSY' $false @{ pid = $after.pid; rule = 'recheck_after_lock'; recheck_rule = $after.rule })
        }
        if ($after.state -cne 'clear') {
            return (New-ActivationResult 'NOT_MEASURED' $false @{ pid = $after.pid; error = $after.error })
        }

        $utc = [DateTime]::UtcNow.ToString('o', [Globalization.CultureInfo]::InvariantCulture)
        $line = "$PID`t$utc`t$([Environment]::MachineName)`n"
        $bytes = [Text.UTF8Encoding]::new($false).GetBytes($line)
        $stream.Position = 0
        $stream.SetLength(0)
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush()
        $keep = $true
        return (New-ActivationResult 'ACQUIRED' $true @{ guard = [pscustomobject]@{ stream = $stream } })
    } catch {
        return (New-ActivationResult 'NOT_MEASURED' $false @{ error = $_.Exception.Message })
    } finally {
        if (-not $keep -and $null -ne $stream) {
            try { $stream.Dispose() } catch { $null = $_ }
        }
    }
}

function Exit-ProximaProfileGuard {
    [CmdletBinding()]
    param([Parameter()][AllowNull()]$Guard)
    try {
        if ($null -eq $Guard) { throw 'Guard is required.' }
        $stream = $Guard.stream
        if ($stream -isnot [IO.Stream]) { throw 'Guard does not hold a lock stream.' }
        $stream.Dispose()
        return (New-ActivationResult 'RELEASED' $true)
    } catch {
        return (New-ActivationResult 'NOT_MEASURED' $false @{ error = $_.Exception.Message })
    }
}

function Test-ProximaPromotionFence {
    [CmdletBinding()]
    param(
        [Parameter()][AllowNull()]$Plan,
        [Parameter()][AllowNull()]$TargetHost,
        [Parameter()][AllowNull()]$ArtifactSha256,
        [Parameter()][AllowNull()]$ReceiptDir
    )
    $ErrorActionPreference = 'Stop'
    $details = @{ blocking_host = $null }
    try {
        if ($TargetHost -isnot [string] -or $TargetHost.Length -eq 0) { throw 'TargetHost must be a non-empty string.' }
        if ($ArtifactSha256 -isnot [string] -or $ArtifactSha256 -cnotmatch '^[0-9a-fA-F]{64}\z') {
            throw 'ArtifactSha256 must be 64 hexadecimal characters.'
        }
        $receiptRoot = Resolve-ActivationPath $ReceiptDir 'ReceiptDir'
        $planIds = [Collections.Generic.List[string]]::new()
        $planSeen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
        if ($null -ne $Plan) {
            foreach ($id in @($Plan)) {
                if ($id -isnot [string]) { throw 'Plan entries must be strings.' }
                # Receipt files are named after hosts, and file names on Windows ignore case.
                if (-not $planSeen.Add($id)) { throw "Plan lists a host more than once: $id" }
                $planIds.Add($id)
            }
        }
        $targetIndex = $planIds.IndexOf($TargetHost)
        if ($targetIndex -lt 0) { return (New-ActivationResult 'FENCE_TARGET_UNKNOWN' $false $details) }
        for ($index = 0; $index -lt $targetIndex; $index++) {
            $prior = $planIds[$index]
            $details.blocking_host = $prior
            if ([string]::IsNullOrWhiteSpace($prior) -or $prior.IndexOfAny([IO.Path]::GetInvalidFileNameChars()) -ge 0 -or
                $prior -cmatch '[\\/:]') { throw 'Invalid receipt host identifier.' }
            $path = [IO.Path]::Combine($receiptRoot, "$prior.json")
            try {
                $receipt = Read-ActivationJson $path
                $schema = Get-ActivationField $receipt 'schema'
                $receiptHost = Get-ActivationField $receipt 'host'
                $sha = Get-ActivationField $receipt 'artifact_sha256'
                $passed = Get-ActivationField $receipt 'passed'
                $completed = Get-ActivationField $receipt 'completed_at'
                if ($schema -isnot [string] -or $schema -cne 'proxima_activation_receipt.v1' -or
                    $receiptHost -isnot [string] -or -not [string]::Equals($receiptHost, $prior, [StringComparison]::Ordinal) -or
                    $sha -isnot [string] -or $sha -cnotmatch '^[a-fA-F0-9]{64}\z' -or $passed -isnot [bool]) {
                    return (New-ActivationResult 'FENCE_RECEIPT_INVALID' $false $details)
                }
                $timestamp = [DateTimeOffset]::MinValue
                if ($completed -isnot [string] -or $completed -cnotmatch '^\d{4}-\d{2}-\d{2}T' -or
                    -not [DateTimeOffset]::TryParse($completed, [Globalization.CultureInfo]::InvariantCulture,
                        [Globalization.DateTimeStyles]::AssumeUniversal, [ref]$timestamp)) {
                    return (New-ActivationResult 'FENCE_RECEIPT_INVALID' $false $details)
                }
            } catch [IO.FileNotFoundException], [IO.DirectoryNotFoundException] {
                return (New-ActivationResult 'FENCE_PRIOR_MISSING' $false $details)
            } catch [IO.IOException], [UnauthorizedAccessException] {
                throw
            } catch {
                return (New-ActivationResult 'FENCE_RECEIPT_INVALID' $false $details)
            }
            if (-not $passed) { return (New-ActivationResult 'FENCE_PRIOR_FAILED' $false $details) }
            if (-not [string]::Equals($sha, $ArtifactSha256, [StringComparison]::OrdinalIgnoreCase)) {
                return (New-ActivationResult 'FENCE_ARTIFACT_MISMATCH' $false $details)
            }
        }
        $details.blocking_host = $null
        return (New-ActivationResult 'ALLOWED' $true $details)
    } catch {
        $details.error = $_.Exception.Message
        return (New-ActivationResult 'NOT_MEASURED' $false $details)
    }
}

Export-ModuleMember -Function Test-ProximaArtifactTree, Enter-ProximaProfileGuard, Exit-ProximaProfileGuard, Test-ProximaPromotionFence
