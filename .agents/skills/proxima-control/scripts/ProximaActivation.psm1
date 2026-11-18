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

function Read-ArtifactEntry([string]$Relative, $Entry) {
    if ($Relative -cmatch '(^|/)\.{1,2}(/|$)|^/|/$|//|[\\:\x00]' -or $Relative.Length -eq 0) {
        throw "Invalid manifest path: $Relative"
    }
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

function Test-ProximaArtifactTree {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$ManifestPath,
        [string[]]$MutableRelative = @(),
        [hashtable]$Override = @{}
    )
    $ErrorActionPreference = 'Stop'
    $extra = [Collections.Generic.List[string]]::new()
    $missing = [Collections.Generic.List[string]]::new()
    $changed = [Collections.Generic.List[string]]::new()
    $extraDirs = [Collections.Generic.List[string]]::new()
    $verified = 0
    $errorText = $null
    try {
        $Root = [IO.Path]::GetFullPath($Root)
        if ($Root.Length -gt [IO.Path]::GetPathRoot($Root).Length) {
            $Root = $Root.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
        }
        $rootDir = [IO.DirectoryInfo]::new($Root)
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
        $manifest = Read-ActivationJson $ManifestPath
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
            $expected[$relative] = Read-ArtifactEntry $relative $Override[$relative]
        }
        $mutable = [Collections.Generic.HashSet[string]]::new($MutableRelative, $comparer)
        $unlistedDirs = [Collections.Generic.List[string]]::new()
        foreach ($relative in $extraDirs) {
            if (-not $expected.ContainsKey($relative)) { $unlistedDirs.Add($relative) }
        }
        $unlistedDirs.Sort($comparer)
        $extraDirs = $unlistedDirs

        $actualPaths = [Collections.Generic.List[string]]::new($files.Keys)
        $actualPaths.Sort($comparer)
        foreach ($relative in $actualPaths) {
            if (-not $expected.ContainsKey($relative)) {
                if ($extra.Count -lt 100) { $extra.Add($relative) }
            }
        }

        $expectedPaths = [Collections.Generic.List[string]]::new($expected.Keys)
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
    $details = @{ root = $Root; verified_files = $verified; extra = $extra.ToArray()
        missing = $missing.ToArray(); changed = $changed.ToArray(); extra_dirs = $extraDirs.ToArray() }
    if ($null -ne $errorText) { $details.error = $errorText }
    return (New-ActivationResult $code ($code -ceq 'OK') $details)
}

function ConvertTo-ProfilePath([string]$Path) {
    return [IO.Path]::GetFullPath($Path).TrimEnd([char]'\')
}

function Test-ProfileCommandLine([string]$CommandLine, [string]$ProfilePath) {
    # Consume complete quoted arguments so a switch inside an unrelated value is ignored.
    $argument = [regex]::new('(?:^|\s)(?:--user-data-dir(?:=|\s+)(?:"([^"]*)"|([^\s"]+))(?=\s|$)|(?:[^\s"]|"[^"]*")+)',
        [Text.RegularExpressions.RegexOptions]'IgnoreCase, CultureInvariant')
    foreach ($match in $argument.Matches($CommandLine)) {
        $value = $match.Groups[1].Value + $match.Groups[2].Value
        if ($value -and [string]::Equals((ConvertTo-ProfilePath $value), $ProfilePath, [StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    return $false
}

function Enter-ProximaProfileGuard {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ProfileDir,
        [scriptblock]$ProcessProvider = { Get-CimInstance -ClassName Win32_Process -ErrorAction Stop }
    )
    $ErrorActionPreference = 'Stop'
    $stream = $null
    try {
        $processes = @(& $ProcessProvider)
        $profilePath = ConvertTo-ProfilePath $ProfileDir
        $dir = [IO.Path]::GetFullPath($ProfileDir)
        foreach ($process in $processes) {
            if ($process.Name -ilike 'Proxima*.exe' -and
                (Test-ProfileCommandLine $process.CommandLine $profilePath)) {
                return (New-ActivationResult 'PROFILE_BUSY')
            }
        }
        foreach ($name in 'rest-port.json', 'ipc-port.json') {
            $path = [IO.Path]::Combine($dir, $name)
            try { $data = Read-ActivationJson $path }
            catch [IO.FileNotFoundException] { continue }
            $discoveryPid = Get-ActivationField $data 'pid'
            if (-not (Test-ActivationInteger $discoveryPid) -or $discoveryPid -le 0) {
                throw "Invalid pid in $name."
            }
            foreach ($process in $processes) {
                if ($process.ProcessId -eq $discoveryPid -and $process.Name -ilike 'Proxima*') {
                    return (New-ActivationResult 'PROFILE_BUSY')
                }
            }
        }
        $lockPath = [IO.Path]::Combine($dir, '.proxima-activation.lock')
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
        $utc = [DateTime]::UtcNow.ToString('o', [Globalization.CultureInfo]::InvariantCulture)
        $line = "$PID`t$utc`t$([Environment]::MachineName)`n"
        $bytes = [Text.UTF8Encoding]::new($false).GetBytes($line)
        $stream.SetLength(0)
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush()
        return (New-ActivationResult 'ACQUIRED' $true @{ guard = [pscustomobject]@{ stream = $stream } })
    } catch {
        $message = $_.Exception.Message
        if ($null -ne $stream) {
            try { $stream.Dispose() } catch { $message += ' ' + $_.Exception.Message }
        }
        return (New-ActivationResult 'NOT_MEASURED' $false @{ error = $message })
    }
}

function Exit-ProximaProfileGuard {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)]$Guard)
    try {
        $Guard.stream.Dispose()
        return (New-ActivationResult 'RELEASED' $true)
    } catch {
        return (New-ActivationResult 'NOT_MEASURED' $false @{ error = $_.Exception.Message })
    }
}

function Test-ProximaPromotionFence {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]]$Plan,
        [Parameter(Mandatory = $true)][string]$TargetHost,
        [Parameter(Mandatory = $true)][string]$ArtifactSha256,
        [Parameter(Mandatory = $true)][string]$ReceiptDir
    )
    $ErrorActionPreference = 'Stop'
    $details = @{ blocking_host = $null }
    try {
        $targetIndex = [Array]::IndexOf($Plan, $TargetHost)
        if ($targetIndex -lt 0) { return (New-ActivationResult 'FENCE_TARGET_UNKNOWN' $false $details) }
        for ($index = 0; $index -lt $targetIndex; $index++) {
            $prior = $Plan[$index]
            $details.blocking_host = $prior
            if ([string]::IsNullOrWhiteSpace($prior) -or $prior.IndexOfAny([IO.Path]::GetInvalidFileNameChars()) -ge 0 -or
                $prior -cmatch '[\\/:]') { throw 'Invalid receipt host identifier.' }
            $path = [IO.Path]::Combine($ReceiptDir, "$prior.json")
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
