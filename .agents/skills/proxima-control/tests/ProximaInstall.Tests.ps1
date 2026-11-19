# Self-contained harness for Windows PowerShell 5.1 and PowerShell 7 (Windows only: junctions, links, NTFS names).
# rc 0: all cases passed; rc 1: property failure; rc 2: setup/runtime error.
# Everything runs against a fake LocalAppData below ScratchRoot with a small fake installer.exe; no real
# installer, uninstaller, registry key or process is touched.
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
$moduleKey = 'scripts/ProximaInstall.psm1'
$cases = [Collections.Generic.List[object]]::new()
$mutations = [Collections.Generic.List[object]]::new()
$report = [ordered]@{
    schema = 'proxima_install_tests.v1'; ps_version = "$($PSVersionTable.PSVersion)"
    ps_edition = $PSVersionTable.PSEdition; edition = $PSVersionTable.PSEdition
    culture = [Globalization.CultureInfo]::CurrentCulture.Name
    addon_root = $AddonRoot; scratch_run = $null; setup_error = $null
    total = 0; passed = 0; failed_ids = @(); skipped_ids = @(); setup_error_ids = @()
    required_ids = @(); id_errors = @(); child_timeout_sec = 300
    harness_sha256 = $null; source_hashes = [ordered]@{}
    cases = $null; counterexamples = $null
}
$reportWritable = $false
$requiredIds = @(1..21 | ForEach-Object { 'PU{0:d2}' -f $_ }) + @('PU21b', 'PU21c', 'PU22')
if ($Counterexamples) { $requiredIds += @(1..7 | ForEach-Object { 'CU{0:d2}' -f $_ }) }
$report.required_ids = $requiredIds

function Get-FileSha([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    try {
        $hasher = [Security.Cryptography.SHA256]::Create()
        try { return [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-', '').ToLowerInvariant() }
        finally { $hasher.Dispose() }
    } finally { $stream.Dispose() }
}

function Assert-NoReparsePath([string]$Path) {
    $node = $Path
    while ($null -ne $node -and $node.Length -gt 0) {
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
    # The nearest ancestor holding a .git directory or file.
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

function Stop-Case([string]$Reason, [string]$Outcome = 'failed') {
    $exception = [InvalidOperationException]::new($Reason)
    $exception.Data['install_case_outcome'] = $Outcome
    throw $exception
}

function Invoke-Case([string]$Id, [scriptblock]$Body) {
    # An exception that is not a Stop-Case verdict means the case could not measure: setup_error, never passed.
    $case = [ordered]@{ id = $Id; outcome = 'passed'; reason = $null }
    try {
        $case.reason = (@(& $Body) -join '; ')
    } catch {
        $case.reason = $_.Exception.Message
        $case.outcome = 'setup_error'
        if ($_.Exception.Data.Contains('install_case_outcome')) {
            $case.outcome = $_.Exception.Data['install_case_outcome']
        }
    }
    $cases.Add($case)
    Write-Host "$Id $($case.outcome) $($case.reason)"
}

function Assert-Result($Result, [string]$Code, [bool]$Ok = $false) {
    if ($null -eq $Result -or @($Result).Count -ne 1 -or $Result.ok -isnot [bool] -or $Result.code -isnot [string]) {
        Stop-Case "Expected one result object for $Code"
    }
    if ($Result.code -cne $Code -or $Result.ok -ne $Ok) {
        Stop-Case "Expected $Code (ok=$Ok), got $($Result.code) (ok=$($Result.ok))"
    }
    foreach ($name in 'actions', 'before', 'after', 'error') {
        if ($null -eq $Result.PSObject.Properties[$name]) { Stop-Case "Result has no '$name' field" }
    }
    if ($Result.actions -isnot [array]) { Stop-Case "Result field 'actions' is not an array" }
    foreach ($action in $Result.actions) {
        if ($action -isnot [string]) { Stop-Case "Result field 'actions' holds a non-string entry" }
    }
}

function Assert-ActionCount($Result, [int]$Least, [int]$Most) {
    $count = @($Result.actions).Count
    if ($count -lt $Least -or $count -gt $Most) { Stop-Case "Expected $Least..$Most actions, got $count" }
}

function Test-PathPresent([string]$Path) {
    try { $null = [IO.File]::GetAttributes($Path); return $true }
    catch [IO.FileNotFoundException], [IO.DirectoryNotFoundException] { return $false }
}

function Test-Reparse([string]$Path) {
    return (([IO.File]::GetAttributes($Path) -band [IO.FileAttributes]::ReparsePoint) -ne 0)
}

function New-Fixture([string]$Id, [switch]$Install, [switch]$Updater, [string]$ProgramsName = 'Programs',
    [string]$InstallName = 'Proxima', [string]$UpdaterName = 'proxima-updater', [string]$InstallerName = 'installer.exe') {
    $dir = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, $Id)).FullName
    $localDir = [IO.Directory]::CreateDirectory([IO.Path]::Combine($dir, 'Local')).FullName
    $programs = [IO.Path]::Combine($localDir, $ProgramsName)
    $installPath = [IO.Path]::Combine($programs, $InstallName)
    $updaterPath = [IO.Path]::Combine($localDir, $UpdaterName)
    $installerPath = [IO.Path]::Combine($updaterPath, $InstallerName)
    if ($Install) { $null = [IO.Directory]::CreateDirectory($installPath) }
    if ($Updater) {
        $null = [IO.Directory]::CreateDirectory($updaterPath)
        [IO.File]::WriteAllBytes($installerPath, $installerContent)
    }
    # Neighbours that no outcome may ever touch.
    $keepDir = [IO.Directory]::CreateDirectory([IO.Path]::Combine($localDir, 'proxima-updater-other')).FullName
    $keep = [IO.Path]::Combine($keepDir, 'keep.txt')
    [IO.File]::WriteAllText($keep, 'keep', $utf8)
    return @{ dir = $dir; local = $localDir; programs = $programs; install = $installPath; updater = $updaterPath
        installer = $installerPath; keep = $keep }
}

function Invoke-Clean($Fixture, [hashtable]$Extra = @{}) {
    $arguments = @{
        LocalAppData = $Fixture.local; InstallerSha256 = $installerSha; InstallerBytes = $installerLength
        ProcessProvider = $noProcesses; UninstallKeyProvider = $noKeys
    }
    foreach ($key in $Extra.Keys) { $arguments[$key] = $Extra[$key] }
    return Remove-ProximaUninstallResidue @arguments
}

function New-ProcessProvider([string[]]$Names) {
    return { foreach ($name in $Names) { [pscustomobject]@{ Name = $name } } }.GetNewClosure()
}

function New-KeyProvider([object[]]$Entries) {
    return { $Entries }.GetNewClosure()
}

function Assert-Neighbours($Fixture) {
    if (-not [IO.File]::Exists($Fixture.keep)) { Stop-Case 'A neighbouring directory lost its file' }
    if (-not [IO.Directory]::Exists($Fixture.local)) { Stop-Case 'LocalAppData itself was removed' }
}

function Assert-NoQuarantine($Fixture) {
    $held = [IO.Directory]::GetFileSystemEntries($Fixture.local, 'proxima-updater.pxu-*')
    if ($held.Length -ne 0) { Stop-Case "Expected no quarantine directory to be left behind, found $($held.Length)" }
}

function Assert-UpdaterIntact($Fixture) {
    $intact = $false
    if ([IO.Directory]::Exists($Fixture.updater) -and -not (Test-Reparse $Fixture.updater)) {
        $entries = [IO.Directory]::GetFileSystemEntries($Fixture.updater)
        if ($entries.Length -eq 1 -and [IO.File]::Exists($Fixture.installer) -and
            (Get-FileSha $Fixture.installer) -ceq $installerSha) { $intact = $true }
    }
    if (-not $intact) { Stop-Case 'Expected the updater residue to be left untouched' }
    Assert-NoQuarantine $Fixture
}

function Assert-InstallDirKept($Fixture) {
    if (-not [IO.Directory]::Exists($Fixture.install)) { Stop-Case 'Expected the install directory to be left in place' }
}

function Assert-BothGone($Fixture) {
    if (Test-PathPresent $Fixture.install) { Stop-Case 'Expected the install directory to be gone' }
    if (Test-PathPresent $Fixture.updater) { Stop-Case 'Expected the updater directory to be gone' }
    Assert-NoQuarantine $Fixture
    Assert-Neighbours $Fixture
}

function New-Junction([string]$Link, [string]$Target) {
    # No elevation needed. A failure here surfaces as setup_error for the case.
    $null = New-Item -Path $Link -ItemType Junction -Target $Target -ErrorAction Stop
    if (-not (Test-Reparse $Link)) { throw "Junction fixture is not a reparse point: $Link" }
}

function New-FileSymlink([string]$Link, [string]$Target) {
    # Needs Developer Mode or elevation. When it cannot be created the case is a setup_error, not a pass.
    $failure = $null
    try { $null = New-Item -Path $Link -ItemType SymbolicLink -Target $Target -ErrorAction Stop }
    catch { $failure = $_.Exception.Message }
    if ($null -ne $failure) {
        if (-not ('PxuTest.Native' -as [type])) {
            Add-Type -Namespace PxuTest -Name Native -MemberDefinition (
                '[DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)] ' +
                'public static extern byte CreateSymbolicLinkW(string link, string target, int flags);')
        }
        # 2 = SYMBOLIC_LINK_FLAG_ALLOW_UNPRIVILEGED_CREATE (Developer Mode).
        $made = [PxuTest.Native]::CreateSymbolicLinkW($Link, $Target, 2)
        $lastError = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
        if ($made -eq 0 -or -not (Test-PathPresent $Link)) {
            throw "File symbolic link could not be created (enable Developer Mode or run elevated): New-Item: $failure; CreateSymbolicLinkW error $lastError"
        }
    }
    if (-not (Test-Reparse $Link)) { throw "Symbolic link fixture is not a reparse point: $Link" }
}

function Invoke-Counterexample($Mutation) {
    $targetIds = @($Mutation.targets.Keys)
    $record = [ordered]@{
        id = $Mutation.id; target_case = ($targetIds -join ','); edits = $Mutation.edits
        source_sha256 = $report.source_hashes[$moduleKey]
        mutated_sha256 = $null; rc = $null; report_path = $null; stdout_path = $null; stderr_path = $null
        timed_out = $false; child_failed_ids = $null
        verdict = $null; reason = $null
    }
    $mutations.Add($record)
    try {
        $mutated = [IO.File]::ReadAllText($modulePath, $utf8)
        foreach ($edit in $Mutation.edits) {
            $offset = $mutated.IndexOf($edit.anchor, [StringComparison]::Ordinal)
            if ($offset -lt 0 -or $mutated.IndexOf($edit.anchor, $offset + 1, [StringComparison]::Ordinal) -ge 0) {
                Stop-Case "Mutation anchor is absent or ambiguous: $($edit.anchor)"
            }
            $mutated = $mutated.Substring(0, $offset) + $edit.replacement + $mutated.Substring($offset + $edit.anchor.Length)
        }
        $dir = [IO.Directory]::CreateDirectory([IO.Path]::Combine($run, $Mutation.id)).FullName
        $addon = [IO.Path]::Combine($dir, 'addon')
        $scripts = [IO.Directory]::CreateDirectory([IO.Path]::Combine($addon, 'scripts')).FullName
        $copy = [IO.Path]::Combine($scripts, 'ProximaInstall.psm1')
        [IO.File]::WriteAllText($copy, $mutated, $utf8)
        $record.mutated_sha256 = Get-FileSha $copy
        if ($record.mutated_sha256 -ceq $record.source_sha256) { Stop-Case 'Mutation did not change the module' }
        $record.report_path = [IO.Path]::Combine($dir, 'report.json')
        $record.stdout_path = [IO.Path]::Combine($dir, 'stdout.txt')
        $record.stderr_path = [IO.Path]::Combine($dir, 'stderr.txt')
        $exeName = if ($PSVersionTable.PSEdition -ceq 'Desktop') { 'powershell.exe' } else { 'pwsh.exe' }
        $exe = [IO.Path]::Combine($PSHOME, $exeName)
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
        $moduleSha = $childReport.source_hashes.PSObject.Properties[$moduleKey].Value
        if ($moduleSha -cne $record.mutated_sha256 -or $childReport.harness_sha256 -cne $report.harness_sha256 -or
            $childReport.ps_edition -cne $report.ps_edition) { throw 'Counterexample child provenance mismatch' }
        $childFailed = @($childReport.failed_ids | Where-Object { $null -ne $_ })
        $record.child_failed_ids = $childFailed
        # Killed only when exactly the declared cases turn red, each for its declared reason.
        $problems = [Collections.Generic.List[string]]::new()
        if ($record.rc -ne 1) { $problems.Add("child rc=$($record.rc)") }
        foreach ($id in $childFailed) {
            if ($targetIds -cnotcontains $id) { $problems.Add("undeclared failure $id") }
        }
        $reasons = [Collections.Generic.List[string]]::new()
        foreach ($id in $targetIds) {
            $hit = @($childReport.cases | Where-Object { $_.id -ceq $id -and $_.outcome -ceq 'failed' })
            if ($hit.Count -ne 1) { $problems.Add("$id did not fail"); continue }
            $expected = [string]$Mutation.targets[$id]
            if (-not ([string]$hit[0].reason).StartsWith($expected, [StringComparison]::Ordinal)) {
                $problems.Add("$id failed with '$($hit[0].reason)' instead of '$expected'")
                continue
            }
            $reasons.Add("${id}: $($hit[0].reason)")
        }
        if ($problems.Count -ne 0) { Stop-Case ("Mutant not credited: " + ($problems -join '; ')) }
        $record.verdict = 'killed'
        $record.reason = ($reasons -join ' | ')
        return $record.reason
    } catch {
        $record.verdict = 'not_credited'
        $record.reason = $_.Exception.Message
        throw
    }
}

try {
    if (-not $windows) { throw 'This harness requires Windows (NTFS junctions, links and case-insensitive names).' }
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
    $run = [IO.Directory]::CreateDirectory([IO.Path]::Combine($scratch, 'install-' + [guid]::NewGuid().ToString('N'))).FullName
    $report.scratch_run = $run
    $modulePath = [IO.Path]::Combine($root, 'scripts', 'ProximaInstall.psm1')
    $report.harness_sha256 = Get-FileSha $PSCommandPath
    $report.source_hashes[$moduleKey] = Get-FileSha $modulePath
    $null = Import-Module -Name $modulePath -Force -DisableNameChecking -ErrorAction Stop

    # A small stand-in for the installer copy; the function is told its size and hash.
    $installerContent = [Text.Encoding]::ASCII.GetBytes('proxima installer fixture 0001')
    $wrongContent = [Text.Encoding]::ASCII.GetBytes('proxima installer fixture 0002')
    $seed = [IO.Path]::Combine($run, 'installer-seed.bin')
    [IO.File]::WriteAllBytes($seed, $installerContent)
    $installerSha = Get-FileSha $seed
    $installerLength = [long]$installerContent.Length
    $noProcesses = New-ProcessProvider @('pxu-harness-host')
    $noKeys = New-KeyProvider @()

    Invoke-Case 'PU01' {
        $f = New-Fixture 'PU01'
        $calls = @{ n = 0 }
        $actual = Invoke-Clean $f @{ TestHook = { $calls.n++ }.GetNewClosure() }
        Assert-Result $actual 'NOTHING_TO_DO' $true
        Assert-ActionCount $actual 0 0
        if ($calls.n -ne 0) { Stop-Case 'The hook ran although there was no removal phase' }
        # An existing Programs directory without Proxima is left alone.
        $null = [IO.Directory]::CreateDirectory($f.programs)
        Assert-Result (Invoke-Clean $f) 'NOTHING_TO_DO' $true
        if (-not [IO.Directory]::Exists($f.programs)) { Stop-Case 'The Programs directory was removed' }
        Assert-Neighbours $f
    }
    Invoke-Case 'PU02' {
        $f = New-Fixture 'PU02' -Install -Updater
        $sibling = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.programs, 'Other')).FullName
        $actual = Invoke-Clean $f
        Assert-Result $actual 'CLEANED' $true
        Assert-BothGone $f
        Assert-ActionCount $actual 2 3
        if (-not [IO.Directory]::Exists($sibling)) { Stop-Case 'A sibling of the install directory was removed' }
        if ($actual.before.install_dir.kind -cne 'directory' -or $actual.before.updater_dir.kind -cne 'directory' -or
            $actual.before.updater_dir.entry_count -ne 1) { Stop-Case 'Expected both targets in the inventory taken before' }
        if ($actual.after.install_dir.kind -cne 'absent' -or $actual.after.updater_dir.kind -cne 'absent') {
            Stop-Case 'Expected both targets absent in the inventory taken after'
        }
        # A second run finds nothing.
        Assert-Result (Invoke-Clean $f) 'NOTHING_TO_DO' $true
    }
    Invoke-Case 'PU03' {
        $f = New-Fixture 'PU03' -Install
        $calls = @{ n = 0 }
        $actual = Invoke-Clean $f @{ TestHook = { $calls.n++ }.GetNewClosure() }
        Assert-Result $actual 'CLEANED' $true
        Assert-BothGone $f
        Assert-ActionCount $actual 1 1
        if ($calls.n -ne 1) { Stop-Case "Expected the hook to run exactly once, ran $($calls.n) times" }
        if (-not [IO.Directory]::Exists($f.programs)) { Stop-Case 'The Programs directory was removed' }
    }
    Invoke-Case 'PU04' {
        $f = New-Fixture 'PU04' -Updater
        $actual = Invoke-Clean $f
        Assert-Result $actual 'CLEANED' $true
        Assert-BothGone $f
        Assert-ActionCount $actual 2 2
    }
    Invoke-Case 'PU05' {
        $f = New-Fixture 'PU05' -Install -Updater
        $leftover = [IO.Path]::Combine($f.install, 'leftover.txt')
        [IO.File]::WriteAllText($leftover, 'leftover', $utf8)
        $actual = Invoke-Clean $f
        Assert-Result $actual 'RESIDUE_UNEXPECTED'
        if (-not [IO.File]::Exists($leftover)) { Stop-Case 'The unexpected file in the install directory was removed' }
        Assert-UpdaterIntact $f
        Assert-ActionCount $actual 0 0
        Assert-Neighbours $f
    }
    Invoke-Case 'PU06' {
        $f = New-Fixture 'PU06' -Install
        $sub = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.install, 'sub')).FullName
        Assert-Result (Invoke-Clean $f) 'RESIDUE_UNEXPECTED'
        if (-not [IO.Directory]::Exists($sub)) { Stop-Case 'The empty subdirectory was removed' }
        # A hidden system file also counts as content.
        $g = New-Fixture 'PU06-hidden' -Install
        $hidden = [IO.Path]::Combine($g.install, 'desktop.ini')
        [IO.File]::WriteAllText($hidden, 'x', $utf8)
        [IO.File]::SetAttributes($hidden, ([IO.FileAttributes]::Hidden -bor [IO.FileAttributes]::System))
        Assert-Result (Invoke-Clean $g) 'RESIDUE_UNEXPECTED'
        if (-not [IO.File]::Exists($hidden)) { Stop-Case 'The hidden file was removed' }
    }
    Invoke-Case 'PU07' {
        $f = New-Fixture 'PU07' -Install -Updater
        $extra = [IO.Path]::Combine($f.updater, 'zz-extra.txt')
        [IO.File]::WriteAllText($extra, 'extra', $utf8)
        Assert-Result (Invoke-Clean $f) 'RESIDUE_UNEXPECTED'
        if (-not [IO.File]::Exists($extra) -or -not [IO.File]::Exists($f.installer) -or
            (Get-FileSha $f.installer) -cne $installerSha) { Stop-Case 'A file of the updater directory was lost' }
        Assert-InstallDirKept $f
        Assert-NoQuarantine $f
    }
    Invoke-Case 'PU08' {
        $f = New-Fixture 'PU08' -Updater
        if ($wrongContent.Length -ne $installerContent.Length) { throw 'Fixture contents must have equal length' }
        [IO.File]::WriteAllBytes($f.installer, $wrongContent)
        $wrongSha = Get-FileSha $f.installer
        Assert-Result (Invoke-Clean $f) 'RESIDUE_UNEXPECTED'
        if (-not [IO.File]::Exists($f.installer) -or (Get-FileSha $f.installer) -cne $wrongSha) {
            Stop-Case 'The installer with the wrong hash was removed or changed'
        }
        Assert-NoQuarantine $f
    }
    Invoke-Case 'PU09' {
        $f = New-Fixture 'PU09' -Updater
        [IO.File]::WriteAllBytes($f.installer, [byte[]]($installerContent + [byte]0))
        Assert-Result (Invoke-Clean $f) 'RESIDUE_UNEXPECTED'
        if ([IO.FileInfo]::new($f.installer).Length -ne ($installerLength + 1)) { Stop-Case 'The installer with the wrong size was removed or changed' }
        # The expected size is what the caller states, not what the file has.
        Assert-Result (Invoke-Clean (New-Fixture 'PU09-arg' -Updater) @{ InstallerBytes = ($installerLength + 1) }) 'RESIDUE_UNEXPECTED'
        Assert-NoQuarantine $f
    }
    Invoke-Case 'PU10' {
        $f = New-Fixture 'PU10' -Updater
        $sub = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.updater, 'sub')).FullName
        Assert-Result (Invoke-Clean $f) 'RESIDUE_UNEXPECTED'
        if (-not [IO.Directory]::Exists($sub) -or -not [IO.File]::Exists($f.installer)) { Stop-Case 'An entry of the updater directory was lost' }
        Assert-NoQuarantine $f
        # An empty updater directory is not the known residue.
        $g = New-Fixture 'PU10-empty'
        $null = [IO.Directory]::CreateDirectory($g.updater)
        Assert-Result (Invoke-Clean $g) 'RESIDUE_UNEXPECTED'
        if (-not [IO.Directory]::Exists($g.updater)) { Stop-Case 'The empty updater directory was removed' }
        # Neither is a directory that merely carries the installer's name.
        $h = New-Fixture 'PU10-dir'
        $null = [IO.Directory]::CreateDirectory($h.installer)
        Assert-Result (Invoke-Clean $h) 'RESIDUE_UNEXPECTED'
        if (-not [IO.Directory]::Exists($h.installer)) { Stop-Case 'The directory named installer.exe was removed' }
    }
    Invoke-Case 'PU11' {
        $f = New-Fixture 'PU11'
        $outside = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.dir, 'outside')).FullName
        $outsideFile = [IO.Path]::Combine($outside, 'outside.txt')
        [IO.File]::WriteAllText($outsideFile, 'outside', $utf8)
        $null = [IO.Directory]::CreateDirectory($f.programs)
        New-Junction $f.install $outside
        Assert-Result (Invoke-Clean $f) 'RESIDUE_UNEXPECTED'
        if (-not [IO.File]::Exists($outsideFile)) { Stop-Case 'The junction target lost its file' }
        if (-not (Test-PathPresent $f.install) -or -not (Test-Reparse $f.install)) { Stop-Case 'The junction itself was removed' }
        # Same with an EMPTY target: only the reparse check stands between the junction and its removal.
        $g = New-Fixture 'PU11-empty'
        $emptyTarget = [IO.Directory]::CreateDirectory([IO.Path]::Combine($g.dir, 'outside')).FullName
        $null = [IO.Directory]::CreateDirectory($g.programs)
        New-Junction $g.install $emptyTarget
        Assert-Result (Invoke-Clean $g) 'RESIDUE_UNEXPECTED'
        if (-not (Test-PathPresent $g.install) -or -not (Test-Reparse $g.install)) { Stop-Case 'The junction to an empty directory was removed' }
        if (-not [IO.Directory]::Exists($emptyTarget)) { Stop-Case 'The empty junction target was removed' }
    }
    Invoke-Case 'PU12' {
        $f = New-Fixture 'PU12'
        # The target holds a perfectly valid installer, so only the reparse check can refuse.
        $outside = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.dir, 'outside')).FullName
        $outsideFile = [IO.Path]::Combine($outside, 'installer.exe')
        [IO.File]::WriteAllBytes($outsideFile, $installerContent)
        New-Junction $f.updater $outside
        Assert-Result (Invoke-Clean $f) 'RESIDUE_UNEXPECTED'
        if (-not [IO.File]::Exists($outsideFile)) { Stop-Case 'The junction target lost its installer' }
        if (-not (Test-PathPresent $f.updater) -or -not (Test-Reparse $f.updater)) { Stop-Case 'The updater junction was removed or renamed' }
        Assert-NoQuarantine $f
    }
    Invoke-Case 'PU13' {
        # Hard link. A hard link is a second name of the same file and cannot be told apart from a regular
        # file by attributes, so a link with the right size and hash is accepted. Removing it removes one
        # name only: the content stays reachable under the other name, which is what this part records.
        $h = New-Fixture 'PU13-hard'
        $original = [IO.Path]::Combine($h.dir, 'original.bin')
        [IO.File]::WriteAllBytes($original, $installerContent)
        $null = [IO.Directory]::CreateDirectory($h.updater)
        $null = New-Item -Path $h.installer -ItemType HardLink -Target $original -ErrorAction Stop
        $actual = Invoke-Clean $h
        Assert-Result $actual 'CLEANED' $true
        Assert-BothGone $h
        if (-not [IO.File]::Exists($original) -or (Get-FileSha $original) -cne $installerSha) {
            Stop-Case 'Removing the hard link damaged the original file'
        }
        # Symbolic link to a file with the right size and hash: refused because it is a reparse point.
        $s = New-Fixture 'PU13-sym'
        $target = [IO.Path]::Combine($s.dir, 'target.bin')
        [IO.File]::WriteAllBytes($target, $installerContent)
        $null = [IO.Directory]::CreateDirectory($s.updater)
        New-FileSymlink $s.installer $target
        Assert-Result (Invoke-Clean $s) 'RESIDUE_UNEXPECTED'
        if (-not [IO.File]::Exists($target) -or (Get-FileSha $target) -cne $installerSha) { Stop-Case 'The symbolic link target was removed or changed' }
        if (-not (Test-PathPresent $s.installer) -or -not (Test-Reparse $s.installer)) { Stop-Case 'The symbolic link was removed' }
        Assert-NoQuarantine $s
        'hardlink=accepted_one_name_removed'
    }
    Invoke-Case 'PU14' {
        $f = New-Fixture 'PU14' -Install -Updater
        foreach ($name in 'Un_A', 'proxima.EXE', 'PROXIMA', 'au_helper', 'UN_b.exe', 'Au_') {
            $actual = Invoke-Clean $f @{ ProcessProvider = (New-ProcessProvider @('pxu-harness-host', $name)) }
            Assert-Result $actual 'UNINSTALL_RUNNING'
            Assert-InstallDirKept $f
            Assert-UpdaterIntact $f
            Assert-ActionCount $actual 0 0
        }
        # Names that only resemble the blocked ones do not block.
        $actual = Invoke-Clean $f @{ ProcessProvider = (New-ProcessProvider @('Unrelated', 'Aurora', 'ProximaHelper', 'xUn_a', 'Proxima2.exe')) }
        Assert-Result $actual 'CLEANED' $true
        Assert-BothGone $f
    }
    Invoke-Case 'PU15' {
        $f = New-Fixture 'PU15' -Install -Updater
        foreach ($display in 'Proxima 5.5.0', 'Proxima', 'PROXIMA 5.5.0') {
            $keys = @([pscustomobject]@{ Key = 'other' }, [pscustomobject]@{ Key = 'x'; DisplayName = $display })
            $actual = Invoke-Clean $f @{ UninstallKeyProvider = (New-KeyProvider $keys) }
            Assert-Result $actual 'STILL_INSTALLED'
            Assert-InstallDirKept $f
            Assert-UpdaterIntact $f
        }
        # Keys without a DisplayName, with an empty one or with another product do not block.
        $keys = @([pscustomobject]@{ Key = 'a' }, [pscustomobject]@{ Key = 'b'; DisplayName = $null },
            [pscustomobject]@{ Key = 'c'; DisplayName = 'Other App' }, [pscustomobject]@{ Key = 'd'; DisplayName = 'My Proxima' })
        $actual = Invoke-Clean $f @{ UninstallKeyProvider = (New-KeyProvider $keys) }
        Assert-Result $actual 'CLEANED' $true
        Assert-BothGone $f
    }
    Invoke-Case 'PU16' {
        $f = New-Fixture 'PU16' -Install -Updater
        $exe = [IO.Path]::Combine($f.install, 'Proxima.exe')
        [IO.File]::WriteAllText($exe, 'app', $utf8)
        Assert-Result (Invoke-Clean $f) 'STILL_INSTALLED'
        if (-not [IO.File]::Exists($exe)) { Stop-Case 'Proxima.exe was removed' }
        Assert-UpdaterIntact $f
    }
    Invoke-Case 'PU17' {
        $f = New-Fixture 'PU17' -Install -Updater
        $calls = @{ n = 0 }
        $actual = Invoke-Clean $f @{ WhatIf = $true; TestHook = { $calls.n++ }.GetNewClosure() }
        # WOULD_REMOVE is not one of the two codes the specification gives ok=true.
        Assert-Result $actual 'WOULD_REMOVE'
        Assert-ActionCount $actual 2 3
        Assert-InstallDirKept $f
        Assert-UpdaterIntact $f
        if ($calls.n -ne 0) { Stop-Case 'The hook ran during a preview' }
        $actual = Invoke-Clean (New-Fixture 'PU17-none') @{ WhatIf = $true }
        Assert-Result $actual 'NOTHING_TO_DO' $true
        Assert-ActionCount $actual 0 0
        # A preview still refuses what a real run would refuse.
        $g = New-Fixture 'PU17-bad' -Install -Updater
        [IO.File]::WriteAllText([IO.Path]::Combine($g.install, 'leftover.txt'), 'leftover', $utf8)
        Assert-Result (Invoke-Clean $g @{ WhatIf = $true }) 'RESIDUE_UNEXPECTED'
    }
    Invoke-Case 'PU18' {
        $f = New-Fixture 'PU18' -Install -Updater
        $missing = [IO.Path]::Combine($f.dir, 'no-such-directory')
        $linked = [IO.Path]::Combine($f.dir, 'LinkedLocal')
        New-Junction $linked $f.local
        $badValues = @('Local\relative', 'relative', 'C:relative', '', '   ', $null, 42, $missing, $f.keep, $linked,
            ('\\?\' + $f.local))
        foreach ($value in $badValues) {
            $actual = Invoke-Clean $f @{ LocalAppData = $value }
            Assert-Result $actual 'BAD_ARGUMENT'
            Assert-InstallDirKept $f
            Assert-UpdaterIntact $f
        }
        $badArguments = @(
            @{ InstallerSha256 = 'abc' }, @{ InstallerSha256 = $null }, @{ InstallerSha256 = ('g' * 64) },
            @{ InstallerBytes = -1 }, @{ InstallerBytes = '30' }, @{ InstallerBytes = $null },
            @{ ProcessProvider = $null }, @{ ProcessProvider = 'Get-Process' }, @{ UninstallKeyProvider = $null },
            @{ TestHook = 'hook' })
        foreach ($extra in $badArguments) {
            Assert-Result (Invoke-Clean $f $extra) 'BAD_ARGUMENT'
            Assert-InstallDirKept $f
            Assert-UpdaterIntact $f
        }
        "refused=$($badValues.Count + $badArguments.Count)"
    }
    Invoke-Case 'PU19' {
        # Windows names are case-insensitive: other spellings are the same residue. The expected hash is
        # passed in upper case and the cases run under whatever culture the host has (tr-TR in acceptance).
        $f = New-Fixture 'PU19' -Install -Updater -ProgramsName 'PROGRAMS' -InstallName 'PROXIMA' -UpdaterName 'Proxima-Updater' -InstallerName 'INSTALLER.EXE'
        $actual = Invoke-Clean $f @{ InstallerSha256 = $installerSha.ToUpperInvariant() }
        Assert-Result $actual 'CLEANED' $true
        Assert-BothGone $f
        Assert-ActionCount $actual 2 3
        if (-not [IO.Directory]::Exists($f.programs)) { Stop-Case 'The Programs directory was removed' }
    }
    Invoke-Case 'PU20' {
        $f = New-Fixture 'PU20' -Install -Updater
        $providers = @(
            @{ ProcessProvider = { throw 'process provider failed' } },
            @{ UninstallKeyProvider = { throw 'key provider failed' } },
            # An empty process list is not evidence that nothing runs.
            @{ ProcessProvider = { } },
            @{ ProcessProvider = { [pscustomobject]@{ Id = 1 } } })
        foreach ($extra in $providers) {
            $actual = Invoke-Clean $f $extra
            Assert-Result $actual 'NOT_MEASURED'
            if ([string]::IsNullOrEmpty([string](Get-ResultField $actual 'error'))) { Stop-Case 'Expected an error text with NOT_MEASURED' }
            Assert-InstallDirKept $f
            Assert-UpdaterIntact $f
            Assert-ActionCount $actual 0 0
        }
        # A failing hook is also reported, with nothing removed.
        $g = New-Fixture 'PU20-hook' -Install
        $actual = Invoke-Clean $g @{ TestHook = { throw 'hook failed' } }
        Assert-Result $actual 'NOT_MEASURED'
        Assert-InstallDirKept $g
    }
    Invoke-Case 'PU21' {
        $f = New-Fixture 'PU21' -Install -Updater
        $added = [IO.Path]::Combine($f.updater, 'added.txt')
        $calls = @{ n = 0 }
        # The closure only sees variables of this block, so it uses nothing else.
        $hook = { $calls.n++; [IO.File]::WriteAllText($added, 'added after the preliminary check') }.GetNewClosure()
        $actual = Invoke-Clean $f @{ TestHook = $hook }
        Assert-Result $actual 'RESIDUE_CHANGED'
        if (-not [IO.Directory]::Exists($f.updater)) { Stop-Case 'Expected the updater back under its original name' }
        if (-not [IO.File]::Exists($added)) { Stop-Case 'The file added after the preliminary check was removed' }
        if (-not [IO.File]::Exists($f.installer) -or (Get-FileSha $f.installer) -cne $installerSha) {
            Stop-Case 'The installer was removed although the updater directory had changed'
        }
        Assert-NoQuarantine $f
        Assert-InstallDirKept $f
        if ($calls.n -ne 1) { Stop-Case "Expected the hook to run exactly once, ran $($calls.n) times" }
        Assert-Neighbours $f
    }
    Invoke-Case 'PU21b' {
        $f = New-Fixture 'PU21b' -Install -Updater
        $added = [IO.Path]::Combine($f.install, 'added.txt')
        $hook = { [IO.File]::WriteAllText($added, 'added after the preliminary check') }.GetNewClosure()
        $actual = Invoke-Clean $f @{ TestHook = $hook }
        Assert-Result $actual 'RESIDUE_CHANGED'
        if (-not [IO.File]::Exists($added)) { Stop-Case 'The file added after the preliminary check was removed' }
        Assert-UpdaterIntact $f
        Assert-Neighbours $f
    }
    Invoke-Case 'PU21c' {
        $f = New-Fixture 'PU21c' -Updater
        $outside = [IO.Directory]::CreateDirectory([IO.Path]::Combine($f.dir, 'outside')).FullName
        $outsideInstall = [IO.Directory]::CreateDirectory([IO.Path]::Combine($outside, 'Proxima')).FullName
        New-Junction $f.programs $outside
        $actual = Invoke-Clean $f
        Assert-Result $actual 'RESIDUE_UNEXPECTED'
        if (-not [IO.Directory]::Exists($outsideInstall)) { Stop-Case 'A directory behind the Programs junction was removed' }
        if (-not (Test-Reparse $f.programs)) { Stop-Case 'The Programs junction was removed' }
        Assert-UpdaterIntact $f
        Assert-ActionCount $actual 0 0
    }
    Invoke-Case 'PU22' {
        $module = @(Get-Module -Name ProximaInstall)
        if ($module.Count -ne 1) { Stop-Case "Expected exactly one loaded ProximaInstall module, found $($module.Count)" }
        $commands = @($module[0].ExportedCommands.Keys)
        if ($commands.Count -ne 1 -or $commands[0] -cne 'Remove-ProximaUninstallResidue') {
            Stop-Case "Expected exactly Remove-ProximaUninstallResidue to be exported, got '$($commands -join ',')'"
        }
        if ($module[0].ExportedVariables.Count -ne 0 -or $module[0].ExportedAliases.Count -ne 0) {
            Stop-Case 'The module exports a variable or an alias'
        }
        "exports=$($commands -join ',')"
    }

    if ($Counterexamples) {
        $unexpectedToCleaned = 'Expected RESIDUE_UNEXPECTED (ok=False), got CLEANED (ok=True)'
        $unexpectedToChanged = 'Expected RESIDUE_UNEXPECTED (ok=False), got RESIDUE_CHANGED (ok=False)'
        $changedToCleaned = 'Expected RESIDUE_CHANGED (ok=False), got CLEANED (ok=True)'
        $updaterTouched = 'Expected the updater residue to be left untouched'
        $counterexampleCases = @(
            # The "empty" check is gone and the install directory is deleted recursively.
            @{ id = 'CU01'
                edits = @(
                    @{ anchor = 'if ($installEntries.Length -ne 0) {'; replacement = 'if ($false) {' },
                    @{ anchor = '[IO.Directory]::Delete($installDir, $false)'; replacement = '[IO.Directory]::Delete($installDir, $true)' })
                targets = [ordered]@{ PU05 = $unexpectedToCleaned; PU06 = $unexpectedToCleaned
                    PU17 = 'Expected RESIDUE_UNEXPECTED (ok=False), got WOULD_REMOVE (ok=False)'; PU21b = $changedToCleaned } }
            # The installer hash is not compared.
            @{ id = 'CU02'
                edits = @(@{ anchor = 'if (-not [string]::Equals($actualSha, $ExpectedSha, [StringComparison]::OrdinalIgnoreCase)) {'
                        replacement = 'if ($false) {' })
                targets = [ordered]@{ PU08 = $unexpectedToCleaned } }
            # The updater directory may hold more than the installer. The mutant then removes the installer
            # and strands the rest in quarantine, so the race case PU21 is red as well.
            @{ id = 'CU03'
                edits = @(@{ anchor = 'if ($updaterEntries.Length -ne 1) {'; replacement = 'if ($false) {' })
                targets = [ordered]@{ PU07 = $unexpectedToChanged; PU10 = $unexpectedToChanged
                    PU21 = 'Expected the updater back under its original name' } }
            # The install directory may be a reparse point.
            @{ id = 'CU04'
                edits = @(@{ anchor = 'if (Test-InstallReparseFlag $attributes) { return ''InstallDir is a reparse point.'' }'
                        replacement = 'if ($false) { return ''InstallDir is a reparse point.'' }' })
                targets = [ordered]@{ PU11 = $unexpectedToCleaned } }
            # A running uninstaller no longer blocks.
            @{ id = 'CU05'
                edits = @(@{ anchor = 'if ($null -ne $running) {'; replacement = 'if ($false) {' })
                targets = [ordered]@{ PU14 = 'Expected UNINSTALL_RUNNING (ok=False), got CLEANED (ok=True)' } }
            # Each target is removed as soon as its own check passes, before the other one is looked at.
            @{ id = 'CU06'
                edits = @(@{ anchor = 'if ($updaterPresent) { $updaterRefusal = (Get-InstallUpdaterState $updaterDir $bytes $expectedSha).refusal }'
                        replacement = 'if ($updaterPresent) { $updaterRefusal = (Get-InstallUpdaterState $updaterDir $bytes $expectedSha).refusal }; ' +
                            'if ($updaterPresent -and $null -eq $updaterRefusal -and -not $WhatIf) { ' +
                            '[IO.File]::Delete([IO.Path]::Combine($updaterDir, ''installer.exe'')); [IO.Directory]::Delete($updaterDir, $false); ' +
                            '$actions.Add(''mutant removed installer''); $actions.Add(''mutant removed updater''); $removed += 2; $updaterPresent = $false }' })
                targets = [ordered]@{ PU05 = $updaterTouched
                    PU21 = 'Expected RESIDUE_CHANGED (ok=False), got NOT_MEASURED (ok=False)'; PU21b = $updaterTouched } }
            # The defect of the N3 driver: the updater is deleted recursively on the strength of the
            # preliminary check, without quarantine and without a second look.
            @{ id = 'CU07'
                edits = @(@{ anchor = '$isolation = Move-InstallUpdaterToQuarantine $updaterDir $root $bytes $expectedSha $actions'
                        replacement = '[IO.Directory]::Delete($updaterDir, $true); $actions.Add(''mutant removed installer''); ' +
                            '$actions.Add(''mutant removed updater''); $removed += 2; $isolation = @{ refusal = $null; quarantine = $null; item = $null }' })
                targets = [ordered]@{ PU21 = $changedToCleaned } }
        )
        foreach ($mutation in $counterexampleCases) {
            Invoke-Case $mutation.id { Invoke-Counterexample $mutation }
        }
    }
    if ((Get-FileSha $modulePath) -cne $report.source_hashes[$moduleKey] -or
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
$rc = if ($report.setup_error -or $report.setup_error_ids.Count -or $report.skipped_ids.Count) { 2 }
    elseif ($report.failed_ids.Count -or $idErrors.Count) { 1 } else { 0 }
if ($reportWritable) {
    try { [IO.File]::WriteAllText($ReportPath, ($report | ConvertTo-Json -Depth 8), $utf8) }
    catch { $report.setup_error = $_.Exception.Message; $rc = 2 }
}
Write-Host ('RESULT {0}/{1} passed; failed_ids=[{2}]; skipped_ids=[{3}]; setup_error_ids=[{4}]; id_errors=[{5}]; setup_error={6}; rc={7}' -f
    $report.passed, $report.total, ($report.failed_ids -join ','), ($report.skipped_ids -join ','),
    ($report.setup_error_ids -join ','), ($report.id_errors -join ','), $report.setup_error, $rc)
exit $rc
