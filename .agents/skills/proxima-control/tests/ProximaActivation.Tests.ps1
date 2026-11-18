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
    harness_sha256 = $null; source_hashes = [ordered]@{}
    cases = $null; counterexamples = $null
}
$reportWritable = $false

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
    if ([string]::Equals($Path, $SourceDir, [StringComparison]::OrdinalIgnoreCase) -or
        $Path.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Output paths must be outside the add-on.'
    }
    Assert-NoReparsePath $Path
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

function Write-Receipt([string]$Dir, [bool]$Passed, [string]$Sha, [string]$Schema = 'proxima_activation_receipt.v1') {
    $receipt = @{ schema = $Schema; host = 'first'; artifact_sha256 = $Sha; passed = $Passed; completed_at = '2026-11-18T12:00:00Z' }
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
        mutated_sha256 = $null; rc = $null; report_path = $null; stdout_path = $null
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
        # Expected rc 1 from a killed mutant must remain an exit code in newer hosts.
        $PSNativeCommandUseErrorActionPreference = $false
        $output = & $exe -NoProfile -NonInteractive -File $PSCommandPath -AddonRoot $addon -ScratchRoot $dir -ReportPath $record.report_path
        $record.rc = $LASTEXITCODE
        [IO.File]::WriteAllLines($record.stdout_path, [string[]]@($output), $utf8)
        if ($record.rc -notin 0, 1 -or -not [IO.File]::Exists($record.report_path)) {
            throw "Counterexample child did not complete (rc=$($record.rc))"
        }
        $child = ConvertFrom-Json -InputObject ([IO.File]::ReadAllText($record.report_path, $utf8))
        $hit = @($child.cases | Where-Object { $_.id -ceq $Mutation.target -and $_.outcome -ceq 'failed' })
        $moduleSha = $child.source_hashes.PSObject.Properties['scripts/ProximaActivation.psm1'].Value
        if ($moduleSha -cne $record.mutated_sha256 -or $child.harness_sha256 -cne $report.harness_sha256 -or
            $child.ps_edition -cne $report.ps_edition) { throw 'Counterexample child provenance mismatch' }
        if ($record.rc -ne 1 -or @($child.failed_ids).Count -ne 1 -or $hit.Count -ne 1 -or
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
    Assert-SafeOutputPath $ReportPath $root
    Assert-SafeOutputPath $ReportPath ([IO.Path]::GetDirectoryName($PSCommandPath))
    $reportWritable = $true
    Assert-SafeOutputPath $scratch $root
    Assert-SafeOutputPath $scratch ([IO.Path]::GetDirectoryName($PSCommandPath))
    if (-not [IO.Directory]::Exists($scratch)) { throw 'ScratchRoot must be an existing directory' }
    $run = [IO.Directory]::CreateDirectory([IO.Path]::Combine($scratch, 'activation-' + [guid]::NewGuid().ToString('N'))).FullName
    $report.scratch_run = $run
    $modulePath = [IO.Path]::Combine($root, 'scripts', 'ProximaActivation.psm1')
    $report.harness_sha256 = Get-FileSha $PSCommandPath
    $report.source_hashes['scripts/ProximaActivation.psm1'] = Get-FileSha $modulePath
    $null = Import-Module -Name $modulePath -Force -DisableNameChecking -ErrorAction Stop
    $noProcesses = { }
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
        )
        foreach ($form in $forms) {
            # An unquoted path containing whitespace is not a single argument.
            if ($form.path -ceq $plain -and $plain -match '\s') { continue }
            $process = [pscustomobject]@{
                ProcessId = 23456; Name = 'Proxima.exe'; ExecutablePath = 'Proxima.exe'
                CommandLine = "Proxima.exe $($form.arg) --other"
            }
            $provider = { $process }.GetNewClosure()
            $actual = Enter-ProximaProfileGuard -ProfileDir $form.path -ProcessProvider $provider
            if ($actual.ok) { $null = Exit-ProximaProfileGuard -Guard $actual.guard }
            Assert-Result $actual 'PROFILE_BUSY'
            Assert-Unlocked $form.path
        }
    }
    Invoke-Case 'PA11' {
        $profile = New-Profile 'PA11'
        [IO.File]::WriteAllText([IO.Path]::Combine($profile, 'rest-port.json'), '{"pid":23456}', $utf8)
        $provider = { [pscustomobject]@{ ProcessId = 23456; Name = 'Proxima.exe'; ExecutablePath = 'Proxima.exe'; CommandLine = '' } }
        $actual = Enter-ProximaProfileGuard -ProfileDir $profile -ProcessProvider $provider
        if ($actual.ok) { $null = Exit-ProximaProfileGuard -Guard $actual.guard }
        Assert-Result $actual 'PROFILE_BUSY'
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

    if ($Counterexamples) {
        $counterexampleCases = @(
            @{ id = 'CX01'; target = 'PA04'; anchor = 'foreach ($relative in $actualPaths) {'
                replacement = 'foreach ($relative in @()) {'
                reason = 'Expected ARTIFACT_EXTRA (ok=False), got OK (ok=True)' }
            @{ id = 'CX02'; target = 'PA10'; anchor = '(Test-ProfileCommandLine $process.CommandLine $profilePath)) {'
                replacement = '$false) {'
                reason = 'Expected PROFILE_BUSY (ok=False), got ACQUIRED (ok=True)' }
            @{ id = 'CX03'; target = 'PA16'; anchor = 'if (-not $passed) {'
                replacement = 'if ($false) {'
                reason = 'Expected FENCE_PRIOR_FAILED (ok=False), got ALLOWED (ok=True)' }
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
$rc = if ($report.setup_error -or $report.setup_error_ids.Count) { 2 }
    elseif ($report.failed_ids.Count) { 1 } else { 0 }
if ($reportWritable) {
    try { [IO.File]::WriteAllText($ReportPath, ($report | ConvertTo-Json -Depth 8), $utf8) }
    catch { $report.setup_error = $_.Exception.Message; $rc = 2 }
}
Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; skipped_ids=[{3}]; setup_error_ids=[{4}]; setup_error={5}; rc={6}' -f
    $report.passed, $report.total, ($report.failed_ids -join ','), ($report.skipped_ids -join ','),
    ($report.setup_error_ids -join ','), $report.setup_error, $rc)
exit $rc
