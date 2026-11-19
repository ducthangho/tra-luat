Set-StrictMode -Version 3.0

# Controlled removal of what the vendor uninstaller of Proxima 5.5.0 (per-user) leaves behind:
#   <LocalAppData>\Programs\Proxima          an empty directory
#   <LocalAppData>\proxima-updater           one file, installer.exe, a copy of the installer
# This module never runs an installer or uninstaller, never starts Proxima and only reads the registry.
# No delete here is recursive: a directory is only ever removed by a call that refuses a non-empty directory.

$script:DefaultInstallerSha256 = '959c14c1ba489deb53bdaa34e83939fb18f9d7ade58a48a03d361ad1dd12ebf8'
$script:DefaultInstallerBytes = 161754969
$script:InstallerName = 'installer.exe'
$script:QuarantinePrefix = 'proxima-updater.pxu-'

# Reads the Uninstall keys of HKCU and HKLM in both registry views (the 32-bit view of HKLM is WOW6432Node).
$script:DefaultUninstallKeyProvider = {
    $subPath = 'Software\Microsoft\Windows\CurrentVersion\Uninstall'
    foreach ($hive in [Microsoft.Win32.RegistryHive]::CurrentUser, [Microsoft.Win32.RegistryHive]::LocalMachine) {
        foreach ($view in [Microsoft.Win32.RegistryView]::Registry64, [Microsoft.Win32.RegistryView]::Registry32) {
            $hiveKey = [Microsoft.Win32.RegistryKey]::OpenBaseKey($hive, $view)
            try {
                $uninstallKey = $hiveKey.OpenSubKey($subPath, $false)
                if ($null -eq $uninstallKey) { continue }
                try {
                    foreach ($keyName in $uninstallKey.GetSubKeyNames()) {
                        $entryKey = $uninstallKey.OpenSubKey($keyName, $false)
                        # A key removed between the listing and the open is simply no longer there.
                        if ($null -eq $entryKey) { continue }
                        try {
                            [pscustomobject]@{
                                Hive = "$hive"; View = "$view"; Key = $keyName
                                DisplayName = $entryKey.GetValue('DisplayName')
                            }
                        } finally { $entryKey.Dispose() }
                    }
                } finally { $uninstallKey.Dispose() }
            } finally { $hiveKey.Dispose() }
        }
    }
}

function New-InstallResult([string]$Code, [bool]$Ok, $Actions, $Before, $After, $Detail, $ErrorText) {
    $list = @()
    if ($null -ne $Actions) { $list = $Actions.ToArray() }
    return [pscustomobject]@{
        ok = $Ok; code = $Code; actions = $list; before = $Before; after = $After
        detail = $Detail; error = $ErrorText
    }
}

function Get-InstallAttributes([string]$Path) {
    # $null means the path does not exist. Never follows the final component.
    try { return [IO.File]::GetAttributes($Path) }
    catch [IO.FileNotFoundException], [IO.DirectoryNotFoundException] { return $null }
}

function Test-InstallReparseFlag($Attributes) {
    return (($Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)
}

function Test-InstallDirectoryFlag($Attributes) {
    return (($Attributes -band [IO.FileAttributes]::Directory) -ne 0)
}

function Test-InstallReparsePoint([string]$Path) {
    $attributes = Get-InstallAttributes $Path
    if ($null -eq $attributes) { return $false }
    return (Test-InstallReparseFlag $attributes)
}

function Get-InstallMember($Entry, [string]$Name) {
    if ($Entry -is [Collections.IDictionary]) {
        if ($Entry.Contains($Name)) { return $Entry[$Name] }
        return $null
    }
    $property = $Entry.PSObject.Properties[$Name]
    if ($null -ne $property) { return $property.Value }
    return $null
}

function Resolve-InstallLocalAppData($Value) {
    if ($Value -isnot [string] -or [string]::IsNullOrWhiteSpace($Value)) {
        return @{ path = $null; error = 'LocalAppData must be a non-empty string.' }
    }
    # Only a drive-letter path is accepted: no relative, drive-relative, UNC or device path.
    if ($Value -cnotmatch '\A[A-Za-z]:[\\/]') {
        return @{ path = $null; error = 'LocalAppData must be a fully qualified drive path.' }
    }
    try { $full = [IO.Path]::GetFullPath($Value) }
    catch { return @{ path = $null; error = "LocalAppData is not a usable path: $($_.Exception.Message)" } }
    if ($full.Length -gt [IO.Path]::GetPathRoot($full).Length) {
        $full = $full.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    }
    $attributes = Get-InstallAttributes $full
    if ($null -eq $attributes -or -not (Test-InstallDirectoryFlag $attributes)) {
        return @{ path = $null; error = 'LocalAppData must be an existing directory.' }
    }
    if (Test-InstallReparseFlag $attributes) {
        return @{ path = $null; error = 'LocalAppData must not be a reparse point.' }
    }
    return @{ path = $full; error = $null }
}

function Find-InstallBlockingProcess([scriptblock]$ProcessProvider) {
    # Returns the name of the first blocking process, or $null.
    $processes = @(& $ProcessProvider)
    # An empty snapshot is not evidence that nothing is running.
    if ($processes.Count -eq 0) { throw 'Process snapshot is empty; running processes were not measured.' }
    foreach ($process in $processes) {
        if ($null -eq $process) { throw 'Process snapshot contains an empty entry.' }
        $processName = Get-InstallMember $process 'ProcessName'
        if ($processName -isnot [string]) { $processName = Get-InstallMember $process 'Name' }
        if ($processName -isnot [string] -or $processName.Length -eq 0) {
            throw 'Process snapshot contains an entry without a name.'
        }
        if ($processName.EndsWith('.exe', [StringComparison]::OrdinalIgnoreCase)) {
            $processName = $processName.Substring(0, $processName.Length - 4)
        }
        if ([string]::Equals($processName, 'Proxima', [StringComparison]::OrdinalIgnoreCase) -or
            $processName.StartsWith('Un_', [StringComparison]::OrdinalIgnoreCase) -or
            $processName.StartsWith('Au_', [StringComparison]::OrdinalIgnoreCase)) {
            return $processName
        }
    }
    return $null
}

function Find-InstallUninstallKey([scriptblock]$UninstallKeyProvider) {
    # Returns the DisplayName of the first uninstall entry of Proxima, or $null.
    foreach ($entry in @(& $UninstallKeyProvider)) {
        if ($null -eq $entry) { throw 'Uninstall key snapshot contains an empty entry.' }
        $display = Get-InstallMember $entry 'DisplayName'
        if ($display -is [string] -and $display.TrimStart().StartsWith('Proxima', [StringComparison]::OrdinalIgnoreCase)) {
            return $display
        }
    }
    return $null
}

function Get-InstallDirRefusal([string]$Path) {
    # $null when the install directory may be removed: a real, completely empty directory.
    $attributes = Get-InstallAttributes $Path
    if ($null -eq $attributes) { return 'InstallDir is no longer there.' }
    if (Test-InstallReparseFlag $attributes) { return 'InstallDir is a reparse point.' }
    if (-not (Test-InstallDirectoryFlag $attributes)) { return 'InstallDir is not a directory.' }
    # GetFileSystemEntries also lists hidden and system entries.
    $installEntries = [IO.Directory]::GetFileSystemEntries($Path)
    if ($installEntries.Length -ne 0) { return "InstallDir holds $($installEntries.Length) entries; expected none." }
    return $null
}

function Get-InstallUpdaterState([string]$Path, [long]$Bytes, [string]$ExpectedSha) {
    # refusal is $null when the directory holds exactly the known installer copy; item is that file.
    $state = @{ refusal = $null; item = $null }
    $attributes = Get-InstallAttributes $Path
    if ($null -eq $attributes) { $state.refusal = 'UpdaterDir is no longer there.'; return $state }
    if (Test-InstallReparseFlag $attributes) { $state.refusal = 'UpdaterDir is a reparse point.'; return $state }
    if (-not (Test-InstallDirectoryFlag $attributes)) { $state.refusal = 'UpdaterDir is not a directory.'; return $state }
    $updaterEntries = [IO.Directory]::GetFileSystemEntries($Path)
    $item = $null
    foreach ($entry in $updaterEntries) {
        if ([string]::Equals([IO.Path]::GetFileName($entry), $script:InstallerName, [StringComparison]::OrdinalIgnoreCase)) {
            $item = $entry
        }
    }
    if ($updaterEntries.Length -ne 1) {
        $state.refusal = "UpdaterDir holds $($updaterEntries.Length) entries; expected exactly one."
        return $state
    }
    if ($null -eq $item) { $state.refusal = 'The only entry of UpdaterDir is not installer.exe.'; return $state }
    $itemAttributes = Get-InstallAttributes $item
    if ($null -eq $itemAttributes) { $state.refusal = 'installer.exe is no longer there.'; return $state }
    if (Test-InstallReparseFlag $itemAttributes) { $state.refusal = 'installer.exe is a reparse point.'; return $state }
    if (Test-InstallDirectoryFlag $itemAttributes) { $state.refusal = 'installer.exe is a directory.'; return $state }
    $actualSha = $null
    # Size and hash come from one handle that allows no writer, renamer or deleter while it is open.
    $stream = [IO.File]::Open($item, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try {
        if ($stream.Length -ne $Bytes) {
            $state.refusal = "installer.exe is $($stream.Length) bytes; expected $Bytes."
            return $state
        }
        $hasher = [Security.Cryptography.SHA256]::Create()
        try { $actualSha = [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-', '') }
        finally { $hasher.Dispose() }
    } finally { $stream.Dispose() }
    if (-not [string]::Equals($actualSha, $ExpectedSha, [StringComparison]::OrdinalIgnoreCase)) {
        $state.refusal = 'installer.exe does not have the expected sha256.'
        return $state
    }
    $state.item = $item
    return $state
}

function Get-InstallNode([string]$Path) {
    # Read-only description of one target. A reparse point is reported, never listed.
    $attributes = Get-InstallAttributes $Path
    if ($null -eq $attributes) {
        return [pscustomobject]@{ path = $Path; kind = 'absent'; reparse_point = $false; entry_count = 0; entries = @() }
    }
    $reparse = Test-InstallReparseFlag $attributes
    $kind = 'file'
    if (Test-InstallDirectoryFlag $attributes) { $kind = 'directory' }
    $listed = [Collections.Generic.List[object]]::new()
    $count = 0
    if ($kind -ceq 'directory' -and -not $reparse) {
        $all = [IO.Directory]::GetFileSystemEntries($Path)
        $count = $all.Length
        foreach ($entry in $all) {
            if ($listed.Count -ge 20) { break }
            $entryAttributes = Get-InstallAttributes $entry
            $entryKind = 'absent'
            $entryReparse = $false
            $entryBytes = $null
            if ($null -ne $entryAttributes) {
                $entryReparse = Test-InstallReparseFlag $entryAttributes
                $entryKind = 'file'
                if (Test-InstallDirectoryFlag $entryAttributes) { $entryKind = 'directory' }
                elseif (-not $entryReparse) {
                    try { $entryBytes = [IO.FileInfo]::new($entry).Length } catch { $entryBytes = $null }
                }
            }
            $listed.Add([pscustomobject]@{
                    name = [IO.Path]::GetFileName($entry); kind = $entryKind
                    reparse_point = $entryReparse; bytes = $entryBytes
                })
        }
    }
    return [pscustomobject]@{
        path = $Path; kind = $kind; reparse_point = $reparse; entry_count = $count; entries = $listed.ToArray()
    }
}

function Get-InstallInventory([string]$Root, [string]$ProgramsDir, [string]$InstallDir, [string]$UpdaterDir) {
    $programsReparse = Test-InstallReparsePoint $ProgramsDir
    $installNode = $null
    # Nothing below a linked Programs directory is looked at.
    if (-not $programsReparse) { $installNode = Get-InstallNode $InstallDir }
    $held = [Collections.Generic.List[string]]::new()
    foreach ($entry in [IO.Directory]::GetFileSystemEntries($Root, $script:QuarantinePrefix + '*')) { $held.Add($entry) }
    return [pscustomobject]@{
        programs_dir_reparse_point = $programsReparse
        install_dir = $installNode
        updater_dir = (Get-InstallNode $UpdaterDir)
        quarantined = $held.ToArray()
    }
}

function Get-InstallInventorySafe([string]$Root, [string]$ProgramsDir, [string]$InstallDir, [string]$UpdaterDir) {
    try { return (Get-InstallInventory $Root $ProgramsDir $InstallDir $UpdaterDir) } catch { return $null }
}

function Restore-InstallUpdater([string]$Quarantine, [string]$UpdaterDir, $Actions) {
    # Puts a quarantined updater back under its original name. Never throws, never overwrites.
    try {
        if ($null -eq (Get-InstallAttributes $Quarantine)) {
            $Actions.Add("quarantine $Quarantine is no longer there; nothing was restored")
            return $false
        }
        if ($null -ne (Get-InstallAttributes $UpdaterDir)) {
            $Actions.Add("left the quarantined updater at $Quarantine because $UpdaterDir exists again")
            return $false
        }
        [IO.Directory]::Move($Quarantine, $UpdaterDir)
        $Actions.Add("renamed $Quarantine back to $UpdaterDir")
        return $true
    } catch {
        $Actions.Add("left the quarantined updater at $Quarantine (rename back failed: $($_.Exception.Message))")
        return $false
    }
}

function Move-InstallUpdaterToQuarantine([string]$UpdaterDir, [string]$Root, [long]$Bytes, [string]$ExpectedSha, $Actions) {
    # Isolate first, verify afterwards: one atomic rename inside the same parent, then every check
    # runs on the renamed copy. On success quarantine and item are set and nothing has been deleted.
    $outcome = @{ refusal = $null; quarantine = $null; item = $null }
    $target = [IO.Path]::Combine($Root, $script:QuarantinePrefix + [guid]::NewGuid().ToString('N'))
    try { [IO.Directory]::Move($UpdaterDir, $target) }
    catch [IO.DirectoryNotFoundException], [IO.FileNotFoundException] {
        $outcome.refusal = 'UpdaterDir disappeared before it could be quarantined.'
        return $outcome
    }
    try { $state = Get-InstallUpdaterState $target $Bytes $ExpectedSha }
    catch {
        $Actions.Add("renamed $UpdaterDir to $target")
        $null = Restore-InstallUpdater $target $UpdaterDir $Actions
        throw
    }
    if ($null -ne $state.refusal) {
        $Actions.Add("renamed $UpdaterDir to $target")
        $null = Restore-InstallUpdater $target $UpdaterDir $Actions
        $outcome.refusal = "After quarantine: $($state.refusal)"
        return $outcome
    }
    $outcome.quarantine = $target
    $outcome.item = $state.item
    return $outcome
}

function Remove-ProximaUninstallResidue {
    [CmdletBinding()]
    param(
        [Parameter()][AllowNull()]$LocalAppData = $env:LOCALAPPDATA,
        [Parameter()][AllowNull()]$InstallerSha256 = $script:DefaultInstallerSha256,
        [Parameter()][AllowNull()]$InstallerBytes = $script:DefaultInstallerBytes,
        [Parameter()][AllowNull()]$ProcessProvider = { Get-Process -ErrorAction Stop },
        [Parameter()][AllowNull()]$UninstallKeyProvider = $script:DefaultUninstallKeyProvider,
        [Parameter(DontShow = $true)][AllowNull()]$TestHook = $null,
        [Parameter()][switch]$WhatIf
    )
    $ErrorActionPreference = 'Stop'
    $actions = [Collections.Generic.List[string]]::new()
    $before = $null
    $removed = 0
    $root = $null
    $programsDir = $null
    $installDir = $null
    $updaterDir = $null
    $quarantine = $null
    $quarantineItem = $null
    $installerDeleted = $false
    try {
        # Arguments.
        if ($ProcessProvider -isnot [scriptblock]) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'ProcessProvider must be a script block.' $null)
        }
        if ($UninstallKeyProvider -isnot [scriptblock]) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'UninstallKeyProvider must be a script block.' $null)
        }
        if ($null -ne $TestHook -and $TestHook -isnot [scriptblock]) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'TestHook must be a script block.' $null)
        }
        if ($InstallerSha256 -isnot [string] -or $InstallerSha256 -cnotmatch '\A[0-9A-Fa-f]{64}\z') {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'InstallerSha256 must be 64 hexadecimal characters.' $null)
        }
        $expectedSha = [string]$InstallerSha256
        $bytes = [long]-1
        if ($InstallerBytes -is [int] -or $InstallerBytes -is [long] -or $InstallerBytes -is [uint32] -or
            $InstallerBytes -is [int16] -or $InstallerBytes -is [uint16] -or $InstallerBytes -is [byte]) {
            $bytes = [long]$InstallerBytes
        }
        if ($bytes -lt 0) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'InstallerBytes must be a non-negative integer.' $null)
        }
        $resolved = Resolve-InstallLocalAppData $LocalAppData
        if ($null -ne $resolved.error) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null $resolved.error $null)
        }
        # The targets are fixed; no caller-supplied path is ever deleted.
        $root = [string]$resolved.path
        $programsDir = [IO.Path]::Combine($root, 'Programs')
        $installDir = [IO.Path]::Combine($programsDir, 'Proxima')
        $updaterDir = [IO.Path]::Combine($root, 'proxima-updater')
        $before = Get-InstallInventory $root $programsDir $installDir $updaterDir

        # Preconditions: nothing is deleted while Proxima or its uninstaller may still be at work.
        $running = Find-InstallBlockingProcess $ProcessProvider
        if ($null -ne $running) {
            return (New-InstallResult 'UNINSTALL_RUNNING' $false $actions $before $before "Process '$running' is running." $null)
        }
        $registered = Find-InstallUninstallKey $UninstallKeyProvider
        if ($null -ne $registered) {
            return (New-InstallResult 'STILL_INSTALLED' $false $actions $before $before "Uninstall entry '$registered' is present." $null)
        }
        if (Test-InstallReparsePoint $programsDir) {
            return (New-InstallResult 'RESIDUE_UNEXPECTED' $false $actions $before $before 'LocalAppData\Programs is a reparse point.' $null)
        }
        if ([IO.File]::Exists([IO.Path]::Combine($installDir, 'Proxima.exe'))) {
            return (New-InstallResult 'STILL_INSTALLED' $false $actions $before $before 'InstallDir still holds Proxima.exe.' $null)
        }

        # Preliminary check of BOTH targets before anything is touched.
        $installPresent = ($null -ne (Get-InstallAttributes $installDir))
        $updaterPresent = ($null -ne (Get-InstallAttributes $updaterDir))
        $installRefusal = $null
        $updaterRefusal = $null
        if ($installPresent) { $installRefusal = Get-InstallDirRefusal $installDir }
        if ($updaterPresent) { $updaterRefusal = (Get-InstallUpdaterState $updaterDir $bytes $expectedSha).refusal }
        if ($null -ne $installRefusal -or $null -ne $updaterRefusal) {
            $detail = (@($installRefusal, $updaterRefusal) | Where-Object { $null -ne $_ }) -join ' '
            return (New-InstallResult 'RESIDUE_UNEXPECTED' $false $actions $before $before $detail $null)
        }
        $installPlanned = $installPresent
        $updaterPlanned = $updaterPresent

        if ($WhatIf) {
            $planned = [Collections.Generic.List[string]]::new()
            if ($installPlanned) { $planned.Add("would remove empty directory $installDir") }
            if ($updaterPlanned) {
                $planned.Add("would remove file $([IO.Path]::Combine($updaterDir, $script:InstallerName))")
                $planned.Add("would remove directory $updaterDir")
            }
            if ($planned.Count -eq 0) {
                return (New-InstallResult 'NOTHING_TO_DO' $true $planned $before $before $null $null)
            }
            return (New-InstallResult 'WOULD_REMOVE' $false $planned $before $before 'Preview only; nothing was removed.' $null)
        }

        if ($installPlanned -or $updaterPlanned) {
            if ($null -ne $TestHook) { $null = & $TestHook }

            # Everything from here on distrusts the preliminary check.
            if ((Test-InstallReparsePoint $root) -or (Test-InstallReparsePoint $programsDir)) {
                return (New-InstallResult 'RESIDUE_CHANGED' $false $actions $before $before 'An ancestor of the targets became a reparse point.' $null)
            }
            if ($installPlanned) {
                $installChange = Get-InstallDirRefusal $installDir
                if ($null -ne $installChange) {
                    $after = Get-InstallInventorySafe $root $programsDir $installDir $updaterDir
                    return (New-InstallResult 'RESIDUE_CHANGED' $false $actions $before $after $installChange $null)
                }
            }
            if ($updaterPlanned) {
                $isolation = Move-InstallUpdaterToQuarantine $updaterDir $root $bytes $expectedSha $actions
                if ($null -ne $isolation.refusal) {
                    $after = Get-InstallInventorySafe $root $programsDir $installDir $updaterDir
                    return (New-InstallResult 'RESIDUE_CHANGED' $false $actions $before $after $isolation.refusal $null)
                }
                $quarantine = $isolation.quarantine
                $quarantineItem = $isolation.item
            }
            if ($installPlanned) {
                # Non-recursive: the call itself refuses a directory that is no longer empty. If the directory
                # was swapped for a junction in the instant since the check above, only the link is removed.
                try { [IO.Directory]::Delete($installDir, $false) }
                catch [IO.IOException] {
                    $installChange = Get-InstallDirRefusal $installDir
                    if ($null -eq $installChange) { throw }
                    if ($null -ne $quarantine) {
                        $actions.Add("renamed $updaterDir to $quarantine")
                        $null = Restore-InstallUpdater $quarantine $updaterDir $actions
                        $quarantine = $null
                    }
                    $after = Get-InstallInventorySafe $root $programsDir $installDir $updaterDir
                    return (New-InstallResult 'RESIDUE_CHANGED' $false $actions $before $after $installChange $null)
                }
                $actions.Add("removed empty directory $installDir")
                $removed++
            }
            if ($null -ne $quarantine) {
                [IO.File]::Delete($quarantineItem)
                $installerDeleted = $true
                $actions.Add("removed file $([IO.Path]::Combine($updaterDir, $script:InstallerName)) (verified under $quarantine)")
                $removed++
                $leftBehind = $false
                try { [IO.Directory]::Delete($quarantine, $false) }
                catch [IO.IOException] {
                    if ($null -ne (Get-InstallAttributes $quarantine)) { $leftBehind = $true }
                }
                if ($leftBehind) {
                    $actions.Add("left $quarantine in place: it is not empty after installer.exe was removed")
                    $after = Get-InstallInventorySafe $root $programsDir $installDir $updaterDir
                    return (New-InstallResult 'RESIDUE_CHANGED' $false $actions $before $after 'The quarantined updater directory gained entries.' $null)
                }
                $actions.Add("removed directory $updaterDir")
                $removed++
                $quarantine = $null
            }
        }

        $after = Get-InstallInventory $root $programsDir $installDir $updaterDir
        if ($removed -eq 0) {
            return (New-InstallResult 'NOTHING_TO_DO' $true $actions $before $after $null $null)
        }
        if ($null -ne $after.install_dir -and $after.install_dir.kind -ceq 'absent' -and $after.updater_dir.kind -ceq 'absent') {
            return (New-InstallResult 'CLEANED' $true $actions $before $after $null $null)
        }
        return (New-InstallResult 'CLEAN_INCOMPLETE' $false $actions $before $after 'A target is still present after removal.' $null)
    } catch {
        $message = $_.Exception.Message
        if ($null -ne $quarantine) {
            if ($installerDeleted) { $actions.Add("left $quarantine in place after an unexpected error") }
            else {
                $actions.Add("renamed $updaterDir to $quarantine")
                $null = Restore-InstallUpdater $quarantine $updaterDir $actions
            }
        }
        $after = $null
        if ($null -ne $root) { $after = Get-InstallInventorySafe $root $programsDir $installDir $updaterDir }
        return (New-InstallResult 'NOT_MEASURED' $false $actions $before $after $null $message)
    }
}

Export-ModuleMember -Function Remove-ProximaUninstallResidue
