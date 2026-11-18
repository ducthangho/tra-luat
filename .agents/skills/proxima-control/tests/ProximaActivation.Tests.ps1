# Self-contained harness for Windows PowerShell 5.1 and PowerShell 7.
# rc 0: all applicable cases passed; rc 1: property failure; rc 2: setup/runtime error.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$AddonRoot,
    [Parameter(Mandatory = $true)][string]$ScratchRoot,
    [Parameter(Mandatory = $true)][string]$ReportPath,
    [switch]$Counterexamples
)
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$utf8 = [Text.UTF8Encoding]::new($false, $true)
$windows = [Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT
$cases = [Collections.Generic.List[object]]::new()
$mutations = [Collections.Generic.List[object]]::new()
$report = [ordered]@{
    schema = 'proxima_activation_tests.v1'; ps_version = "$($PSVersionTable.PSVersion)"
    ps_edition = $PSVersionTable.PSEdition; culture = [Globalization.CultureInfo]::CurrentCulture.Name
    addon_root = $AddonRoot; scratch_run = $null; setup_error = $null
    total = 0; passed = 0; failed_ids = @(); skipped_ids = @(); setup_error_ids = @()
    required_ids = @(); id_errors = @(); child_timeout_sec = 300
    harness_sha256 = $null; source_hashes = [ordered]@{}
    cases = $null; counterexamples = $null
}
$reportWritable = $false
$requiredIds = @(1..28 | ForEach-Object { 'PA{0:d2}' -f $_ })
if ($Counterexamples) { $requiredIds += @(1..5 | ForEach-Object { 'CX{0:d2}' -f $_ }) }
$report.required_ids = $requiredIds

function Get-FileSha([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    try {
        $sha = [Security.Cryptography.SHA256]::Create()
        try { return [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-', '').ToLowerInvariant() }
        finally { $sha.Dispose() }
    } finally { $stream.Dispose() }
}

function Assert-NoReparsePath([string]$Path) {
    $node = $Path
    while ($null -ne $node) {
        try {
            $attributes = [IO.File]::GetAttributes($node)
            if ($attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse path: $node" }
        } catch [IO.FileNotFoundException], [IO.DirectoryNotFoundException] {
            # These components can be created later.
        }
        $node = [IO.Path]::GetDirectoryName($node)
    }
}

function Assert-SafeOutputPath([string]$Path, [string]$SourceDir) {
    $separator = [IO.Path]::DirectorySeparatorChar
    $prefix = $SourceDir.TrimEnd($separator) + $separator
    if (($Path.TrimEnd($separator) + $separator).StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Output path is inside the add-on or its repository: $Path"
    }
    Assert-NoReparsePath $Path
}

function Find-RepositoryTop([string]$Start) {
    # Same rule as ProximaManifest.Tests.ps1: the nearest ancestor holding a .git directory or file.
    $probe = [IO.DirectoryInfo]::new($Start)
    while ($null -ne $probe) {
        $marker = [IO.Path]::Combine($probe.FullName, '.git')
        if ([IO.Directory]::Exists($marker) -or [IO.File]::Exists($marker)) { return $probe.FullName }
        $probe = $probe.Parent
    }
}

function ConvertTo-ArgText([string]$Value) {
    if ($Value.Length -gt 0 -and $Value -cnotmatch '[\s"]') { return $Value }
    $escaped = [regex]::Replace($Value, '(\\*)"', '$1$1\"')
    $escaped = [regex]::Replace($escaped, '(\\+)\z', '$1$1')
    return '"' + $escaped + '"'
}

function Get-ResultField($Result, [string]$Name) {
    if ($null -eq $Result) { return }
    $property = $Result.PSObject.Properties[$Name]
    if ($null -ne $property) { return $property.Value }
}

function New-ProcessEntry([int]$Id, [string]$Name, $CommandLine) {
    return [pscustomobject]@{ ProcessId = $Id; Name = $Name; ExecutablePath = $Name; CommandLine = $CommandLine }
}

function New-Snapshot([object[]]$Extra = @()) {
    # The guard only trusts a snapshot that shows the calling process.
    $entries = @(New-ProcessEntry $PID 'activation-harness-host' 'activation-harness-host') + @($Extra)
    return { $entries }.GetNewClosure()
}

function Enter-Guard([string]$ProfileDir, $Provider) {
    # Never leave a lock behind when a case expects a refusal.
    $actual = Enter-ProximaProfileGuard -ProfileDir $ProfileDir -ProcessProvider $Provider
    if ($actual.ok) { $null = Exit-ProximaProfileGuard -Guard $actual.guard }
    return $actual
}

function Stop-Case([string]$Reason, [string]$Outcome = 'failed') {
    $exception = [InvalidOperationException]::new($Reason)
    $exception.Data['activation_case_outcome'] = $Outcome
    throw $exception
}

function Invoke-Case([string]$Id, [scriptblock]$Body) {
    $case = [ordered]@{ id = $Id; outcome = 'passed'; reason = $null }
    try {
        $case.reason = (@(& $Body) -join '; ')
    } catch {
        $case.reason = $_.Exception.Message
        $case.outcome = 'setup_error'
        if ($_.Exception.Data.Contains('activation_case_outcome')) {
            $case.outcome = $_.Exception.Data['activation_case_outcome']
        }
    }
    $cases.Add($case)
    Write-Host "$Id $($case.outcome) $($case.reason)"
}

function Assert-Result($Result, [string]$Code, [bool]$Ok = $false) {
    if ($null -eq $Result -or $Result.ok -isnot [bool] -or $Result.code -isnot [string]) {
        Stop-Case "Expected one activation result for $Code"
    }
    if ($Result.code -cne $Code -or $Result.ok -ne $Ok) {
        Stop-Case "Expected $Code (ok=$Ok), got $($Result.code) (ok=$($Result.ok))"
    }
}

function New-ArtifactFixture([string]$Id, [switch]$Wrapped) {
    $dir = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, $Id)).FullName
    $root = [IO.Directory]::CreateDirectory([IO.Path]::Combine($dir, 'tree')).FullName
    $exe = [IO.Path]::Combine($root, 'Proxima.exe')
    $mutable = [IO.Path]::Combine($root, 'providers.json')
    [IO.File]::WriteAllText($exe, 'app', $utf8)
    [IO.File]::WriteAllText($mutable, '{}', $utf8)
    $expected = @{
        'Proxima.exe' = @{ bytes = 3; sha256 = (Get-FileSha $exe) }
        'providers.json' = @{ bytes = 2; sha256 = (Get-FileSha $mutable) }
    }
    $manifest = [IO.Path]::Combine($dir, 'manifest.json')
    $document = $expected
    if ($Wrapped) { $document = @{ files = $expected } }
    [IO.File]::WriteAllText($manifest, ($document | ConvertTo-Json -Depth 5), $utf8)
    return @{ dir = $dir; root = $root; manifest = $manifest; exe = $exe; mutable = $mutable }
}

function Measure-Artifact($Fixture, [string[]]$Mutable = @(), [hashtable]$Override = @{}) {
    Test-ProximaArtifactTree -Root $Fixture.root -ManifestPath $Fixture.manifest -MutableRelative $Mutable -Override $Override
}

function New-Profile([string]$Id) {
    return [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, "$Id profile")).FullName
}

function Assert-Unlocked([string]$Profile) {
    if ([IO.File]::Exists([IO.Path]::Combine($Profile, '.proxima-activation.lock'))) {
        Stop-Case 'Profile precheck created a lock file'
    }
}

function Write-Receipt([string]$Dir, [bool]$Passed, [string]$Sha, [string]$Schema = 'proxima_activation_receipt.v1',
    [string]$ReceiptHost = 'first') {
    $receipt = @{ schema = $Schema; host = $ReceiptHost; artifact_sha256 = $Sha; passed = $Passed; completed_at = '2026-11-18T12:00:00Z' }
    [IO.File]::WriteAllText([IO.Path]::Combine($Dir, 'first.json'), ($receipt | ConvertTo-Json), $utf8)
}

function Assert-Fence([string]$Dir, [string]$Target, [string]$Code, [string]$Blocking = '') {
    $result = Test-ProximaPromotionFence -Plan @('first', 'second') -TargetHost $Target -ArtifactSha256 $artifactSha -ReceiptDir $Dir
    Assert-Result $result $Code ($Code -ceq 'ALLOWED')
    if ([string]$result.blocking_host -cne $Blocking) { Stop-Case "Expected blocking host '$Blocking'" }
}

function Invoke-Counterexample($Mutation) {
    $record = [ordered]@{
        id = $Mutation.id; target_case = $Mutation.target; anchor = $Mutation.anchor
        replacement = $Mutation.replacement; source_sha256 = $report.source_hashes['scripts/ProximaActivation.psm1']
        mutated_sha256 = $null; rc = $null; report_path = $null; stdout_path = $null; stderr_path = $null
        timed_out = $false
        verdict = $null; reason = $null
    }
    $mutations.Add($record)
    try {
        $source = [IO.File]::ReadAllText($modulePath, $utf8)
        $offset = $source.IndexOf($Mutation.anchor, [StringComparison]::Ordinal)
        if ($offset -lt 0 -or $source.IndexOf($Mutation.anchor, $offset + 1, [StringComparison]::Ordinal) -ge 0) {
            Stop-Case 'Mutation anchor is absent or ambiguous'
        }
        $dir = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, $Mutation.id)).FullName
        $addon = [IO.Path]::Combine($dir, 'addon')
        $scripts = [IO.Directory]::CreateDirectory([IO.Path]::Combine($addon, 'scripts')).FullName
        $copy = [IO.Path]::Combine($scripts, 'ProximaActivation.psm1')
        $mutated = $source.Substring(0, $offset) + $Mutation.replacement + $source.Substring($offset + $Mutation.anchor.Length)
        [IO.File]::WriteAllText($copy, $mutated, $utf8)
        $record.mutated_sha256 = Get-FileSha $copy
        $record.report_path = [IO.Path]::Combine($dir, 'report.json')
        $record.stdout_path = [IO.Path]::Combine($dir, 'stdout.txt')
        $exeName = if ($PSVersionTable.PSEdition -ceq 'Desktop') { 'powershell.exe' }
            elseif ($windows) { 'pwsh.exe' } else { 'pwsh' }
        $exe = [IO.Path]::Combine($PSHOME, $exeName)
        $record.stderr_path = [IO.Path]::Combine($dir, 'stderr.txt')
        $arguments = @('-NoProfile', '-NonInteractive', '-File', $PSCommandPath, '-AddonRoot', $addon,
            '-ScratchRoot', $dir, '-ReportPath', $record.report_path)
        $start = [Diagnostics.ProcessStartInfo]::new($exe)
        $start.Arguments = @($arguments | ForEach-Object { ConvertTo-ArgText $_ }) -join ' '
        $start.UseShellExecute = $false
        $start.CreateNoWindow = $true
        $start.WorkingDirectory = $dir
        $start.RedirectStandardInput = $true
        $start.RedirectStandardOutput = $true
        $start.RedirectStandardError = $true
        $stdout = [IO.MemoryStream]::new()
        $stderr = [IO.MemoryStream]::new()
        $child = [Diagnostics.Process]::Start($start)
        try {
            $child.StandardInput.Close()
            $copyOut = $child.StandardOutput.BaseStream.CopyToAsync($stdout)
            $copyErr = $child.StandardError.BaseStream.CopyToAsync($stderr)
            # Bounded wait; only the child started here is ever killed.
            if (-not $child.WaitForExit($report.child_timeout_sec * 1000)) {
                $record.timed_out = $true
                try { $child.Kill() } catch { $null = $_ }
                $null = $child.WaitForExit(30000)
            }
            foreach ($task in $copyOut, $copyErr) { try { $null = $task.Wait(30000) } catch { $null = $_ } }
            if ($child.HasExited) { $record.rc = $child.ExitCode }
        } finally {
            $child.Dispose()
            [IO.File]::WriteAllBytes($record.stdout_path, $stdout.ToArray())
            [IO.File]::WriteAllBytes($record.stderr_path, $stderr.ToArray())
        }
        if ($record.timed_out) {
            Stop-Case "Counterexample child timed out after $($report.child_timeout_sec) s and was killed"
        }
        if ($record.rc -notin 0, 1 -or -not [IO.File]::Exists($record.report_path)) {
            throw "Counterexample child did not complete (rc=$($record.rc))"
        }
        $childReport = ConvertFrom-Json -InputObject ([IO.File]::ReadAllText($record.report_path, $utf8))
        $hit = @($childReport.cases | Where-Object { $_.id -ceq $Mutation.target -and $_.outcome -ceq 'failed' })
        $moduleSha = $childReport.source_hashes.PSObject.Properties['scripts/ProximaActivation.psm1'].Value
        if ($moduleSha -cne $record.mutated_sha256 -or $childReport.harness_sha256 -cne $report.harness_sha256 -or
            $childReport.ps_edition -cne $report.ps_edition) { throw 'Counterexample child provenance mismatch' }
        if ($record.rc -ne 1 -or @($childReport.failed_ids).Count -ne 1 -or $hit.Count -ne 1 -or
            -not $hit[0].reason.StartsWith($Mutation.reason, [StringComparison]::Ordinal)) {
            Stop-Case "Expected only $($Mutation.target) to fail with '$($Mutation.reason)'"
        }
        $record.verdict = 'killed'
        return $hit[0].reason
    } catch {
        $record.verdict = 'not_credited'
        $record.reason = $_.Exception.Message
        throw
    }
}

try {
    $root = [IO.Path]::GetFullPath($AddonRoot)
    if ($root.Length -gt [IO.Path]::GetPathRoot($root).Length) {
        $root = $root.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    }
    $scratch = [IO.Path]::GetFullPath($ScratchRoot)
    $ReportPath = [IO.Path]::GetFullPath($ReportPath)
    # Check both the spelled add-on root and its ancestors before permitting output.
    Assert-NoReparsePath $root
    # Evidence must stay outside the add-on under test, this harness's directory and their repositories.
    $harnessDir = [IO.Path]::GetDirectoryName($PSCommandPath)
    $protected = [Collections.Generic.List[string]]::new()
    foreach ($source in $root, $harnessDir) {
        $protected.Add($source)
        $top = Find-RepositoryTop $source
        if ($top) { $protected.Add($top) }
    }
    foreach ($source in $protected) { Assert-SafeOutputPath $ReportPath $source }
    $reportWritable = $true
    foreach ($source in $protected) { Assert-SafeOutputPath $scratch $source }
    if (-not [IO.Directory]::Exists($scratch)) { throw 'ScratchRoot must be an existing directory' }
    $run = [IO.Directory]::CreateDirectory([IO.Path]::Combine($scratch, 'activation-' + [guid]::NewGuid().ToString('N'))).FullName
    $report.scratch_run = $run
    $modulePath = [IO.Path]::Combine($root, 'scripts', 'ProximaActivation.psm1')
    $report.harness_sha256 = Get-FileSha $PSCommandPath
    $report.source_hashes['scripts/ProximaActivation.psm1'] = Get-FileSha $modulePath
    $null = Import-Module -Name $modulePath -Force -DisableNameChecking -ErrorAction Stop
    $noProcesses = New-Snapshot
    $lockName = '.proxima-activation.lock'
    $artifactSha = 'ab' * 32
    $receipts = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, 'receipts')).FullName

    Invoke-Case 'PA01' {
        $f = New-ArtifactFixture 'PA01' -Wrapped
        $null = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.root, 'empty'))
        $actual = Measure-Artifact $f
        Assert-Result $actual 'OK' $true
        if ($actual.verified_files -ne 2 -or ($actual.extra_dirs -join ',') -cne 'empty') {
            Stop-Case 'Expected two checked files and one reported empty directory'
        }
        [IO.File]::WriteAllText($f.exe, 'override', $utf8)
        $override = @{ 'proxima.exe' = @{ bytes = 8; sha256 = (Get-FileSha $f.exe) } }
        Assert-Result (Measure-Artifact $f -Override $override) 'OK' $true
    }
    Invoke-Case 'PA02' {
        $f = New-ArtifactFixture 'PA02'
        [IO.File]::WriteAllText($f.exe, 'App', $utf8)
        Assert-Result (Measure-Artifact $f) 'ARTIFACT_CHANGED'
    }
    Invoke-Case 'PA03' {
        $f = New-ArtifactFixture 'PA03'
        [IO.File]::WriteAllText($f.exe, 'apps', $utf8)
        Assert-Result (Measure-Artifact $f) 'ARTIFACT_CHANGED'
    }
    Invoke-Case 'PA04' {
        $f = New-ArtifactFixture 'PA04'
        [IO.File]::WriteAllText([IO.Path]::Combine($f.root, 'version.dll'), 'extra', $utf8)
        $actual = Measure-Artifact $f
        Assert-Result $actual 'ARTIFACT_EXTRA'
        if (($actual.extra -join ',') -cne 'version.dll') { Stop-Case 'Expected version.dll in extra' }
    }
    Invoke-Case 'PA05' {
        $f = New-ArtifactFixture 'PA05'
        [IO.File]::Delete($f.exe)
        Assert-Result (Measure-Artifact $f) 'ARTIFACT_MISSING'
    }
    Invoke-Case 'PA06' {
        if (-not $windows) { Stop-Case 'NTFS junction fixture requires Windows' 'skipped' }
        $f = New-ArtifactFixture 'PA06'
        $target = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.dir, 'target')).FullName
        $link = [IO.Path]::Combine($f.root, 'junction')
        $null = New-Item -Path $link -ItemType Junction -Target $target -ErrorAction Stop
        [IO.File]::WriteAllText([IO.Path]::Combine($target, 'outside.txt'), 'outside', $utf8)
        [IO.File]::WriteAllText([IO.Path]::Combine($f.root, 'extra.txt'), 'extra', $utf8)
        $actual = Measure-Artifact $f
        Assert-Result $actual 'REPARSE_POINT'
        if ($actual.extra -contains 'junction/outside.txt') { Stop-Case 'Junction contents entered the artifact inventory' }
        Assert-Result (Test-ProximaArtifactTree -Root $link -ManifestPath $f.manifest) 'REPARSE_POINT'
    }
    Invoke-Case 'PA07' {
        $f = New-ArtifactFixture 'PA07'
        [IO.File]::WriteAllText($f.mutable, 'different', $utf8)
        Assert-Result (Measure-Artifact $f -Mutable @('PROVIDERS.json')) 'OK' $true
        [IO.File]::Delete($f.mutable)
        Assert-Result (Measure-Artifact $f -Mutable @('providers.json')) 'OK' $true
    }
    Invoke-Case 'PA08' {
        $f = New-ArtifactFixture 'PA08'
        [IO.File]::WriteAllText($f.manifest, '{broken', $utf8)
        Assert-Result (Measure-Artifact $f) 'NOT_MEASURED'
    }
    Invoke-Case 'PA09' {
        $profile = New-Profile 'PA09'
        $guards = [Collections.Generic.List[object]]::new()
        try {
            $first = Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider $noProcesses
            if ($first.ok) { $guards.Add($first.guard) }
            Assert-Result $first 'ACQUIRED' $true
            $second = Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider $noProcesses
            if ($second.ok) { $guards.Add($second.guard) }
            Assert-Result $second 'PROFILE_LOCKED'
            Assert-Result (Exit-ProximaProfileGuard -Guard $first.guard) 'RELEASED' $true
            Assert-Result (Exit-ProximaProfileGuard -Guard $first.guard) 'RELEASED' $true
            $lockPath = [IO.Path]::Combine($profile, '.proxima-activation.lock')
            $metadata = [IO.File]::ReadAllText($lockPath, $utf8).TrimEnd([char]"`n") -split "`t"
            if ($metadata.Count -ne 3 -or $metadata[0] -cne "$PID" -or $metadata[2] -cne [Environment]::MachineName) {
                Stop-Case 'Expected lock metadata with pid, UTC and host'
            }
            $third = Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider $noProcesses
            if ($third.ok) { $guards.Add($third.guard) }
            Assert-Result $third 'ACQUIRED' $true
        } finally {
            foreach ($guard in $guards) { $null = Exit-ProximaProfileGuard -Guard $guard }
        }
    }
    Invoke-Case 'PA10' {
        $profile = New-Profile 'PA10'
        $plain = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, 'PA10-plain')).FullName
        $suffix = if ($windows) { '\' } else { '' }
        $forms = @(
            @{ path = $profile; arg = ('--user-data-dir="{0}{1}"' -f $profile.ToUpperInvariant(), $suffix) }
            @{ path = $profile; arg = ('--user-data-dir "{0}"' -f $profile) }
            @{ path = $plain; arg = ('--user-data-dir={0}' -f $plain) }
            # Whole-argument quoting: what list2cmdline, .NET and PowerShell 7 emit for a path with a space.
            @{ path = $profile; arg = ('"--user-data-dir={0}"' -f $profile) }
            @{ path = $profile; arg = ('"--user-data-dir" "{0}"' -f $profile) }
            @{ path = $profile; arg = ('-user-data-dir="{0}"' -f $profile) }
            @{ path = $profile; arg = ('/USER-DATA-DIR="{0}"' -f $profile) }
        )
        if ($profile -notmatch '\s') { Stop-Case 'PA10 needs a profile path that contains a space' 'setup_error' }
        foreach ($form in $forms) {
            # An unquoted path containing whitespace is not a single argument.
            if ($form.path -ceq $plain -and $plain -match '\s') { continue }
            $process = New-ProcessEntry 23456 'Proxima.exe' "Proxima.exe $($form.arg) --other"
            $actual = Enter-Guard $form.path (New-Snapshot @($process))
            Assert-Result $actual 'PROFILE_BUSY'
            if ((Get-ResultField $actual 'rule') -cne 'command_line' -or (Get-ResultField $actual 'pid') -ne 23456) {
                Stop-Case "Expected rule command_line and pid 23456 for $($form.arg)"
            }
            Assert-Unlocked $form.path
        }
    }
    Invoke-Case 'PA11' {
        $profile = New-Profile 'PA11'
        [IO.File]::WriteAllText([IO.Path]::Combine($profile, 'rest-port.json'), '{"pid":23456}', $utf8)
        # The discovery file is a definite finding, so it wins over the unreadable command line.
        $actual = Enter-Guard $profile (New-Snapshot @(New-ProcessEntry 23456 'Proxima.exe' ''))
        Assert-Result $actual 'PROFILE_BUSY'
        if ((Get-ResultField $actual 'rule') -cne 'discovery:rest-port.json' -or (Get-ResultField $actual 'pid') -ne 23456) {
            Stop-Case 'Expected rule discovery:rest-port.json and pid 23456'
        }
        Assert-Unlocked $profile
    }
    Invoke-Case 'PA12' {
        $profile = New-Profile 'PA12'
        $actual = Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider { throw 'Process snapshot unavailable' }
        if ($actual.ok) { $null = Exit-ProximaProfileGuard -Guard $actual.guard }
        Assert-Result $actual 'NOT_MEASURED'
        Assert-Unlocked $profile
        [IO.File]::WriteAllText([IO.Path]::Combine($profile, 'ipc-port.json'), '{broken', $utf8)
        $actual = Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider $noProcesses
        if ($actual.ok) { $null = Exit-ProximaProfileGuard -Guard $actual.guard }
        Assert-Result $actual 'NOT_MEASURED'
        Assert-Unlocked $profile
    }

    Invoke-Case 'PA13' { Assert-Fence $receipts 'first' 'ALLOWED' }
    Invoke-Case 'PA14' {
        Write-Receipt $receipts $true ($artifactSha.ToUpperInvariant())
        Assert-Fence $receipts 'second' 'ALLOWED'
    }
    Invoke-Case 'PA15' {
        $empty = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, 'empty-receipts')).FullName
        Assert-Fence $empty 'second' 'FENCE_PRIOR_MISSING' 'first'
    }
    Invoke-Case 'PA16' {
        Write-Receipt $receipts $false $artifactSha
        Assert-Fence $receipts 'second' 'FENCE_PRIOR_FAILED' 'first'
    }
    Invoke-Case 'PA17' {
        Write-Receipt $receipts $true ('cd' * 32)
        Assert-Fence $receipts 'second' 'FENCE_ARTIFACT_MISMATCH' 'first'
    }
    Invoke-Case 'PA18' {
        Write-Receipt $receipts $true $artifactSha 'wrong_schema'
        Assert-Fence $receipts 'second' 'FENCE_RECEIPT_INVALID' 'first'
        Assert-Fence $receipts 'unknown' 'FENCE_TARGET_UNKNOWN'
    }

    Invoke-Case 'PA19' {
        # Neighbours that merely share a prefix with the profile are different profiles.
        $profile = New-Profile 'PA19'
        $others = @(($profile + '2'), ($profile + [IO.Path]::DirectorySeparatorChar + 'sub'))
        foreach ($other in $others) {
            foreach ($arg in ('--user-data-dir="{0}"' -f $other), ('"--user-data-dir={0}"' -f $other)) {
                $process = New-ProcessEntry 23456 'Proxima.exe' "Proxima.exe $arg --other"
                Assert-Result (Enter-Guard $profile (New-Snapshot @($process))) 'ACQUIRED' $true
            }
        }
    }
    Invoke-Case 'PA20' {
        # Elevated or other-user processes expose no command line; that is not evidence of a free profile.
        $profile = New-Profile 'PA20'
        foreach ($commandLine in $null, '', '   ', 'Proxima.exe --user-data-dir=relative-profile', 'Proxima.exe --user-data-dir') {
            $process = New-ProcessEntry 34567 'Proxima Helper.exe' $commandLine
            $actual = Enter-Guard $profile (New-Snapshot @($process))
            Assert-Result $actual 'NOT_MEASURED'
            if ([string](Get-ResultField $actual 'error') -notmatch '\b34567\b' -or (Get-ResultField $actual 'pid') -ne 34567) {
                Stop-Case "Expected pid 34567 in the result for command line '$commandLine'"
            }
            Assert-Unlocked $profile
        }
    }
    Invoke-Case 'PA21' {
        # A snapshot that cannot even show the caller is filtered or empty.
        $profile = New-Profile 'PA21'
        $foreign = New-ProcessEntry 0 'Idle' $null
        foreach ($provider in { }, { $foreign }.GetNewClosure()) {
            $actual = Enter-Guard $profile $provider
            Assert-Result $actual 'NOT_MEASURED'
            if ([string](Get-ResultField $actual 'error') -notmatch 'current process') { Stop-Case 'Expected the missing-self reason' }
            Assert-Unlocked $profile
        }
    }
    Invoke-Case 'PA22' {
        # Relative spellings resolve from this directory, so only the rooted-path rule can refuse them.
        $f = New-ArtifactFixture 'PA22'
        $null = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.dir, 'prof'))
        $null = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.dir, 'receipts'))
        $prefixes = [Collections.Generic.List[string]]::new()
        $prefixes.Add('')
        $prefixes.Add('.' + [IO.Path]::DirectorySeparatorChar)
        if ($windows -and $f.dir -cmatch '^[A-Za-z]:') { $prefixes.Add($f.dir.Substring(0, 2)) }
        $previous = [Environment]::CurrentDirectory
        try {
            [Environment]::CurrentDirectory = $f.dir
            foreach ($prefix in $prefixes) {
                Assert-Result (Test-ProximaArtifactTree -Root ($prefix + 'tree') -ManifestPath $f.manifest) 'NOT_MEASURED'
                Assert-Result (Test-ProximaArtifactTree -Root $f.root -ManifestPath ($prefix + 'manifest.json')) 'NOT_MEASURED'
                Assert-Result (Enter-Guard ($prefix + 'prof') $noProcesses) 'NOT_MEASURED'
                Assert-Result (Test-ProximaPromotionFence -Plan @('first', 'second') -TargetHost 'first' -ArtifactSha256 $artifactSha -ReceiptDir ($prefix + 'receipts')) 'NOT_MEASURED'
            }
            Assert-Unlocked ([IO.Path]::Combine($f.dir, 'prof'))
            Assert-Result (Measure-Artifact $f) 'OK' $true
        } finally { [Environment]::CurrentDirectory = $previous }
    }
    Invoke-Case 'PA23' {
        $profile = New-Profile 'PA23'
        $lockPath = [IO.Path]::Combine($profile, $lockName)
        foreach ($content in ('x' * 600), 'not a lock record', "1`t2", ("12`tutc`thost`n" + 'trailing')) {
            [IO.File]::WriteAllText($lockPath, $content, $utf8)
            Assert-Result (Enter-Guard $profile $noProcesses) 'NOT_MEASURED'
            if ([IO.File]::ReadAllText($lockPath, $utf8) -cne $content) { Stop-Case 'A file that is not a lock record was modified' }
        }
        [IO.File]::WriteAllText($lockPath, '', $utf8)
        Assert-Result (Enter-Guard $profile $noProcesses) 'ACQUIRED' $true
        $target = New-Profile 'PA23 target'
        $link = [IO.Path]::Combine($run, 'PA23 link')
        $linkType = if ($windows) { 'Junction' } else { 'SymbolicLink' }
        $null = New-Item -Path $link -ItemType $linkType -Target $target -ErrorAction Stop
        Assert-Result (Enter-Guard $link $noProcesses) 'NOT_MEASURED'
        Assert-Unlocked $target
        if (-not $windows) {
            # File links need a privilege on Windows; the directory junction above covers that platform.
            $linked = New-Profile 'PA23 linked'
            $victim = [IO.Path]::Combine($run, 'PA23-victim.txt')
            [IO.File]::WriteAllText($victim, '', $utf8)
            $null = New-Item -Path ([IO.Path]::Combine($linked, $lockName)) -ItemType SymbolicLink -Target $victim -ErrorAction Stop
            Assert-Result (Enter-Guard $linked $noProcesses) 'NOT_MEASURED'
            if ([IO.FileInfo]::new($victim).Length -ne 0) { Stop-Case 'The link target was written' }
        }
    }
    Invoke-Case 'PA24' {
        # Proxima appears between the first snapshot and the lock: the second snapshot must see it.
        $profile = New-Profile 'PA24'
        $discovery = [IO.Path]::Combine($profile, 'rest-port.json')
        [IO.File]::WriteAllText($discovery, '{"pid":23456}', $utf8)
        $state = @{ calls = 0 }
        $own = New-ProcessEntry $PID 'activation-harness-host' 'activation-harness-host'
        $late = New-ProcessEntry 23456 'Proxima.exe' 'Proxima.exe --type=renderer'
        $provider = {
            $state.calls++
            $own
            if ($state.calls -ge 2) { $late }
        }.GetNewClosure()
        $actual = Enter-Guard $profile $provider
        Assert-Result $actual 'PROFILE_BUSY'
        if ((Get-ResultField $actual 'rule') -cne 'recheck_after_lock' -or (Get-ResultField $actual 'pid') -ne 23456 -or
            $state.calls -ne 2) { Stop-Case 'Expected rule recheck_after_lock with pid 23456 after two snapshots' }
        [IO.File]::Delete($discovery)
        Assert-Result (Enter-Guard $profile $noProcesses) 'ACQUIRED' $true
    }
    Invoke-Case 'PA25' {
        # Bad arguments are results, not exceptions.
        $f = New-ArtifactFixture 'PA25'
        $profile = New-Profile 'PA25'
        $calls = [ordered]@{
            'Exit null guard' = { Exit-ProximaProfileGuard -Guard $null }
            'Exit foreign guard' = { Exit-ProximaProfileGuard -Guard 'not a guard' }
            'Exit without arguments' = { Exit-ProximaProfileGuard }
            'Enter null profile' = { Enter-ProximaProfileGuard -ProfileDir $null -ProcessProvider $noProcesses }
            'Enter empty profile' = { Enter-ProximaProfileGuard -ProfileDir '' -ProcessProvider $noProcesses }
            'Enter array profile' = { Enter-ProximaProfileGuard -ProfileDir @($profile, $profile) -ProcessProvider $noProcesses }
            'Enter null provider' = { Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider $null }
            'Enter text provider' = { Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider 'Get-Process' }
            'Tree null root' = { Test-ProximaArtifactTree -Root $null -ManifestPath '' }
            'Tree without arguments' = { Test-ProximaArtifactTree }
            'Tree text override' = { Test-ProximaArtifactTree -Root $f.root -ManifestPath $f.manifest -Override 'providers.json' }
            'Tree numeric mutable' = { Test-ProximaArtifactTree -Root $f.root -ManifestPath $f.manifest -MutableRelative @(1) }
            'Fence null arguments' = { Test-ProximaPromotionFence -Plan $null -TargetHost $null -ArtifactSha256 $null -ReceiptDir $null }
            'Fence without arguments' = { Test-ProximaPromotionFence }
        }
        foreach ($name in $calls.PSBase.Keys) {
            $actual = $null
            $thrown = $null
            try { $actual = & $calls[$name] } catch { $thrown = $_.Exception.Message }
            if ($null -ne $thrown) { Stop-Case "$name threw: $thrown" }
            if ($null -ne $actual -and $actual.ok -is [bool] -and $actual.ok -and $name.StartsWith('Enter', [StringComparison]::Ordinal)) {
                $null = Exit-ProximaProfileGuard -Guard $actual.guard
            }
            if ($null -eq $actual -or $actual.code -cne 'NOT_MEASURED' -or $actual.ok -ne $false) { Stop-Case "$name did not return NOT_MEASURED" }
        }
        Assert-Unlocked $profile
    }
    Invoke-Case 'PA26' {
        # Target 'first' would be ALLOWED, so only input validation can refuse these.
        foreach ($sha in $artifactSha.Substring(1), ($artifactSha + '0'), ('zz' * 32), ($artifactSha + "`n")) {
            $actual = Test-ProximaPromotionFence -Plan @('first', 'second') -TargetHost 'first' -ArtifactSha256 $sha -ReceiptDir $receipts
            Assert-Result $actual 'NOT_MEASURED'
        }
        foreach ($plan in @('first', 'second', 'FIRST'), @('first', 'second', 'second')) {
            $actual = Test-ProximaPromotionFence -Plan $plan -TargetHost 'first' -ArtifactSha256 $artifactSha -ReceiptDir $receipts
            Assert-Result $actual 'NOT_MEASURED'
        }
    }
    Invoke-Case 'PA27' {
        $dir = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, 'PA27-receipts')).FullName
        # first.json that names another host is a misfiled receipt.
        Write-Receipt $dir $true $artifactSha -ReceiptHost 'other'
        Assert-Fence $dir 'second' 'FENCE_RECEIPT_INVALID' 'first'
        Write-Receipt $dir $true $artifactSha -ReceiptHost 'FIRST'
        Assert-Fence $dir 'second' 'FENCE_RECEIPT_INVALID' 'first'
        $text = '{"schema":"proxima_activation_receipt.v1","host":"first","artifact_sha256":"' + $artifactSha +
            '","passed":"true","completed_at":"2026-11-18T12:00:00Z"}'
        [IO.File]::WriteAllText([IO.Path]::Combine($dir, 'first.json'), $text, $utf8)
        Assert-Fence $dir 'second' 'FENCE_RECEIPT_INVALID' 'first'
        Write-Receipt $dir $true $artifactSha
        Assert-Fence $dir 'second' 'ALLOWED'
    }
    Invoke-Case 'PA28' {
        $f = New-ArtifactFixture 'PA28'
        $sub = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.root, 'sub')).FullName
        $data = [IO.Path]::Combine($sub, 'data.json')
        [IO.File]::WriteAllText($data, '{}', $utf8)
        $override = @{ 'sub/data.json' = @{ bytes = 2; sha256 = (Get-FileSha $data) } }
        [IO.File]::WriteAllText($data, 'changed', $utf8)
        Assert-Result (Measure-Artifact $f -Override $override) 'ARTIFACT_CHANGED'
        Assert-Result (Measure-Artifact $f -Mutable @('sub\data.json') -Override $override) 'OK' $true
        # A mutable name that matches nothing is a configuration error, with or without such a file on disk.
        Assert-Result (Measure-Artifact $f -Mutable @('notes.txt') -Override $override) 'NOT_MEASURED'
        [IO.File]::WriteAllText([IO.Path]::Combine($f.root, 'notes.txt'), 'note', $utf8)
        $actual = Measure-Artifact $f -Mutable @('notes.txt', 'sub/data.json') -Override $override
        Assert-Result $actual 'NOT_MEASURED'
        if ([string](Get-ResultField $actual 'error') -notmatch 'notes\.txt') { Stop-Case 'Expected the unknown mutable name in the error' }
        Assert-Result (Measure-Artifact $f -Mutable @('../providers.json') -Override $override) 'NOT_MEASURED'
    }

    if ($Counterexamples) {
        $counterexampleCases = @(
            @{ id = 'CX01'; target = 'PA04'; anchor = 'foreach ($relative in $actualPaths) {'
                replacement = 'foreach ($relative in @()) {'
                reason = 'Expected ARTIFACT_EXTRA (ok=False), got OK (ok=True)' }
            @{ id = 'CX02'; target = 'PA10'; anchor = 'if ($state -ceq ''match'') {'
                replacement = 'if ($false) {'
                reason = 'Expected PROFILE_BUSY (ok=False), got ACQUIRED (ok=True)' }
            @{ id = 'CX03'; target = 'PA16'; anchor = 'if (-not $passed) {'
                replacement = 'if ($false) {'
                reason = 'Expected FENCE_PRIOR_FAILED (ok=False), got ALLOWED (ok=True)' }
            @{ id = 'CX04'; target = 'PA19'
                anchor = '[string]::Equals($candidate, $ProfilePath, [StringComparison]::OrdinalIgnoreCase)'
                replacement = '$candidate.StartsWith($ProfilePath, [StringComparison]::OrdinalIgnoreCase)'
                reason = 'Expected ACQUIRED (ok=True), got PROFILE_BUSY (ok=False)' }
            @{ id = 'CX05'; target = 'PA27'
                anchor = '-not [string]::Equals($receiptHost, $prior, [StringComparison]::Ordinal) -or'
                replacement = '$false -or'
                reason = 'Expected FENCE_RECEIPT_INVALID (ok=False), got ALLOWED (ok=True)' }
        )
        foreach ($mutation in $counterexampleCases) {
            Invoke-Case $mutation.id { Invoke-Counterexample $mutation }
        }
    }
    if ((Get-FileSha $modulePath) -cne $report.source_hashes['scripts/ProximaActivation.psm1'] -or
        (Get-FileSha $PSCommandPath) -cne $report.harness_sha256) { throw 'Source changed during the harness run' }
} catch {
    $report.setup_error = $_.Exception.Message
}

$report.cases = $cases.ToArray()
$report.counterexamples = $mutations.ToArray()
$report.total = $cases.Count
$report.passed = @($report.cases | Where-Object { $_.outcome -ceq 'passed' }).Count
foreach ($outcome in 'failed', 'skipped', 'setup_error') {
    $report["${outcome}_ids"] = @($report.cases | Where-Object { $_.outcome -ceq $outcome } | ForEach-Object { $_.id })
}
# Every required ID must have run exactly once; a silently missing case is a failure, not a pass.
$idErrors = [Collections.Generic.List[string]]::new()
foreach ($id in $requiredIds) {
    $count = @($report.cases | Where-Object { $_.id -ceq $id }).Count
    if ($count -eq 0) { $idErrors.Add("missing:$id") } elseif ($count -gt 1) { $idErrors.Add("duplicate:$id x$count") }
}
foreach ($case in $report.cases) {
    if ($requiredIds -cnotcontains $case.id) { $idErrors.Add("unexpected:$($case.id)") }
}
$report.id_errors = $idErrors.ToArray()
$rc = if ($report.setup_error -or $report.setup_error_ids.Count) { 2 }
    elseif ($report.failed_ids.Count -or $idErrors.Count) { 1 } else { 0 }
if ($reportWritable) {
    try { [IO.File]::WriteAllText($ReportPath, ($report | ConvertTo-Json -Depth 8), $utf8) }
    catch { $report.setup_error = $_.Exception.Message; $rc = 2 }
}
Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; skipped_ids=[{3}]; setup_error_ids=[{4}]; id_errors=[{5}]; setup_error={6}; rc={7}' -f
    $report.passed, $report.total, ($report.failed_ids -join ','), ($report.skipped_ids -join ','),
    ($report.setup_error_ids -join ','), ($report.id_errors -join ','), $report.setup_error, $rc)
exit $rc
