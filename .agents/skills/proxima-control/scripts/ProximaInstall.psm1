Set-StrictMode -Version 3.0

# Controlled removal of what the vendor uninstaller of Proxima (per-user) leaves behind:
#   <LocalAppData>\Programs\Proxima          an empty directory
#   <LocalAppData>\proxima-updater           one file, installer.exe, a copy of the installer
# This module never runs an installer or uninstaller, never starts Proxima and only reads the registry.
# Nothing is deleted by path: every removal is a delete disposition set on a handle that was opened
# without delete sharing and whose object (attributes, final path, content) was verified through that
# same handle. A directory disposition is refused by the file system when the directory is not empty.

$script:DefaultInstallerSha256 = '959c14c1ba489deb53bdaa34e83939fb18f9d7ade58a48a03d361ad1dd12ebf8'
$script:DefaultInstallerBytes = 161754969
$script:InstallerName = 'installer.exe'
$script:QuarantinePrefix = 'proxima-updater.pxu-'
$script:ErrorDirNotEmpty = 145

# C# 5 only: Windows PowerShell 5.1 compiles this with the .NET Framework compiler.
$script:NativeSource = @'
using System;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Win32.SafeHandles;

namespace TraLuatPxu
{
    public sealed class FsNode : IDisposable
    {
        public int Error;
        public SafeFileHandle Handle;
        public uint Attributes;
        public uint Links;
        public long Size;
        public string FinalPath;

        public void Dispose()
        {
            if (Handle != null) { Handle.Dispose(); }
        }
    }

    public static class NativeFs
    {
        private const uint GENERIC_READ = 0x80000000;
        private const uint DELETE = 0x00010000;
        private const uint SYNCHRONIZE = 0x00100000;
        private const uint FILE_READ_ATTRIBUTES = 0x00000080;
        private const uint FILE_SHARE_READ = 0x00000001;
        private const uint FILE_SHARE_WRITE = 0x00000002;
        private const uint OPEN_EXISTING = 3;
        private const uint FILE_FLAG_BACKUP_SEMANTICS = 0x02000000;
        private const uint FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000;
        private const int FileDispositionInfo = 4;

        [StructLayout(LayoutKind.Sequential)]
        private struct HandleInfo
        {
            public uint FileAttributes;
            public uint CreationLow;
            public uint CreationHigh;
            public uint AccessLow;
            public uint AccessHigh;
            public uint WriteLow;
            public uint WriteHigh;
            public uint VolumeSerialNumber;
            public uint FileSizeHigh;
            public uint FileSizeLow;
            public uint NumberOfLinks;
            public uint FileIndexHigh;
            public uint FileIndexLow;
        }

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode, ExactSpelling = true)]
        private static extern SafeFileHandle CreateFileW(string name, uint access, uint share, IntPtr security,
            uint creation, uint flags, IntPtr template);

        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool GetFileInformationByHandle(SafeFileHandle handle, out HandleInfo info);

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode, ExactSpelling = true)]
        private static extern uint GetFinalPathNameByHandleW(SafeFileHandle handle, StringBuilder buffer, uint length, uint flags);

        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool SetFileInformationByHandle(SafeFileHandle handle, int infoClass, ref int info, uint size);

        private static int LastError()
        {
            int error = Marshal.GetLastWin32Error();
            return error == 0 ? -1 : error;
        }

        // Opens the object named by path itself (never the target of a link at the last component),
        // WITHOUT delete sharing: while the handle is open nobody can rename, replace or delete it.
        // Error is 0 on success; then Attributes, Links, Size and FinalPath describe the opened object.
        public static FsNode Open(string path, bool directory, bool wantRead, bool wantDelete)
        {
            FsNode node = new FsNode();
            uint access = FILE_READ_ATTRIBUTES | SYNCHRONIZE;
            if (wantRead) { access |= GENERIC_READ; }
            if (wantDelete) { access |= DELETE; }
            uint share = directory ? (FILE_SHARE_READ | FILE_SHARE_WRITE) : FILE_SHARE_READ;
            uint flags = FILE_FLAG_OPEN_REPARSE_POINT | (directory ? FILE_FLAG_BACKUP_SEMANTICS : 0u);
            SafeFileHandle handle = CreateFileW(path, access, share, IntPtr.Zero, OPEN_EXISTING, flags, IntPtr.Zero);
            if (handle.IsInvalid)
            {
                node.Error = LastError();
                handle.Dispose();
                return node;
            }
            HandleInfo info;
            if (!GetFileInformationByHandle(handle, out info))
            {
                node.Error = LastError();
                handle.Dispose();
                return node;
            }
            StringBuilder buffer = new StringBuilder(520);
            uint written = GetFinalPathNameByHandleW(handle, buffer, (uint)buffer.Capacity, 0u);
            if (written >= (uint)buffer.Capacity)
            {
                buffer = new StringBuilder((int)written + 2);
                written = GetFinalPathNameByHandleW(handle, buffer, (uint)buffer.Capacity, 0u);
            }
            if (written == 0 || written >= (uint)buffer.Capacity)
            {
                node.Error = LastError();
                handle.Dispose();
                return node;
            }
            string final = buffer.ToString();
            if (final.StartsWith("\\\\?\\UNC\\", StringComparison.Ordinal)) { final = "\\\\" + final.Substring(8); }
            else if (final.StartsWith("\\\\?\\", StringComparison.Ordinal)) { final = final.Substring(4); }
            node.Handle = handle;
            node.Attributes = info.FileAttributes;
            node.Links = info.NumberOfLinks;
            node.Size = ((long)info.FileSizeHigh << 32) | (long)info.FileSizeLow;
            node.FinalPath = final;
            return node;
        }

        // Marks exactly the opened object for deletion; it disappears when its last handle closes.
        // Returns 0, or the Win32 error (145 = directory not empty).
        public static int MarkDelete(SafeFileHandle handle)
        {
            int flag = 1;
            if (SetFileInformationByHandle(handle, FileDispositionInfo, ref flag, 4u)) { return 0; }
            return LastError();
        }
    }
}
'@

function Initialize-InstallNative {
    # A re-imported module finds the type already defined in this process.
    if ($null -eq ('TraLuatPxu.NativeFs' -as [type])) {
        Add-Type -TypeDefinition $script:NativeSource -Language CSharp -IgnoreWarnings -ErrorAction Stop
    }
}

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

function Test-InstallNodeReparse($Node) {
    # FILE_ATTRIBUTE_REPARSE_POINT of the opened object itself.
    return ((([long]$Node.Attributes) -band 0x400) -ne 0)
}

function Test-InstallNodeDirectory($Node) {
    return ((([long]$Node.Attributes) -band 0x10) -ne 0)
}

function Test-InstallSamePath([string]$Left, [string]$Right) {
    $separator = [char]'\'
    return [string]::Equals($Left.TrimEnd($separator), $Right.TrimEnd($separator), [StringComparison]::OrdinalIgnoreCase)
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

function Get-InstallPathForm([string]$Value) {
    # 'drive' (C:\x) and 'unc' (\\server\share\x) are absolute; 'device' (\\?\, \\.\) and 'relative' are refused.
    if ($Value -cmatch '\A[\\/]{2}[?.](?:[\\/]|\z)') { return 'device' }
    if ($Value -cmatch '\A[A-Za-z]:[\\/]') { return 'drive' }
    if ($Value -cmatch '\A[\\/]{2}[^\\/]+[\\/][^\\/]+') { return 'unc' }
    return 'relative'
}

function Resolve-InstallLocalAppData($Value) {
    if ($Value -isnot [string] -or [string]::IsNullOrWhiteSpace($Value)) {
        return @{ path = $null; error = 'LocalAppData must be a non-empty string.' }
    }
    $form = Get-InstallPathForm $Value
    if ($form -ceq 'device') { return @{ path = $null; error = 'LocalAppData must not be a device or namespace path.' } }
    if ($form -ceq 'relative') { return @{ path = $null; error = 'LocalAppData must be an absolute path.' } }
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
    # Returns the name of the first blocking process, or $null. An empty list holds no blocker.
    foreach ($process in @(& $ProcessProvider)) {
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
        if ($display -is [string] -and $display.StartsWith('Proxima', [StringComparison]::OrdinalIgnoreCase)) {
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

function Get-InstallUpdaterEntry([string]$Path) {
    # The directory must hold exactly one entry, a regular file named installer.exe; item is its path.
    $found = @{ refusal = $null; item = $null }
    $updaterEntries = [IO.Directory]::GetFileSystemEntries($Path)
    $item = $null
    foreach ($entry in $updaterEntries) {
        if ([string]::Equals([IO.Path]::GetFileName($entry), $script:InstallerName, [StringComparison]::OrdinalIgnoreCase)) {
            $item = $entry
        }
    }
    if ($updaterEntries.Length -ne 1) {
        $found.refusal = "UpdaterDir holds $($updaterEntries.Length) entries; expected exactly one."
        return $found
    }
    if ($null -eq $item) { $found.refusal = 'The only entry of UpdaterDir is not installer.exe.'; return $found }
    $itemAttributes = Get-InstallAttributes $item
    if ($null -eq $itemAttributes) { $found.refusal = 'installer.exe is no longer there.'; return $found }
    if (Test-InstallReparseFlag $itemAttributes) { $found.refusal = 'installer.exe is a reparse point.'; return $found }
    if (Test-InstallDirectoryFlag $itemAttributes) { $found.refusal = 'installer.exe is a directory.'; return $found }
    $found.item = $item
    return $found
}

function Get-InstallContentRefusal([IO.Stream]$Stream, [long]$Bytes, [string]$ExpectedSha) {
    # Size and hash are read through the stream that is passed in, never through a second open.
    if ($Stream.Length -ne $Bytes) { return "installer.exe is $($Stream.Length) bytes; expected $Bytes." }
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { $actualSha = [BitConverter]::ToString($hasher.ComputeHash($Stream)).Replace('-', '') }
    finally { $hasher.Dispose() }
    if (-not [string]::Equals($actualSha, $ExpectedSha, [StringComparison]::OrdinalIgnoreCase)) {
        return 'installer.exe does not have the expected sha256.'
    }
    return $null
}

function Get-InstallUpdaterRefusal([string]$Path, [long]$Bytes, [string]$ExpectedSha) {
    # Preliminary, read-only look at the updater directory. $null when it holds exactly the known installer copy.
    $attributes = Get-InstallAttributes $Path
    if ($null -eq $attributes) { return 'UpdaterDir is no longer there.' }
    if (Test-InstallReparseFlag $attributes) { return 'UpdaterDir is a reparse point.' }
    if (-not (Test-InstallDirectoryFlag $attributes)) { return 'UpdaterDir is not a directory.' }
    $found = Get-InstallUpdaterEntry $Path
    if ($null -ne $found.refusal) { return $found.refusal }
    $stream = [IO.File]::Open($found.item, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try { return (Get-InstallContentRefusal $stream $Bytes $ExpectedSha) }
    finally { $stream.Dispose() }
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

function Wait-InstallGone([string]$Path) {
    # A deletion completes when the last handle closes; give a scanner that still holds one a moment.
    for ($attempt = 0; $attempt -lt 20; $attempt++) {
        try { if ($null -eq (Get-InstallAttributes $Path)) { return } } catch { $null = $_ }
        [Threading.Thread]::Sleep(100)
    }
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

function New-InstallChange([string]$Detail) {
    return @{ code = 'changed'; detail = $Detail; removed = 0 }
}

function Enter-InstallUpdaterQuarantine($Plan, $State) {
    # Isolate first, verify afterwards. One atomic rename inside the same parent; then a handle on the
    # renamed directory and a handle on its installer.exe are opened without delete sharing and every
    # check runs on those handles. Returns $null when the held objects are exactly the known residue;
    # otherwise the reason. Nothing is deleted here; the caller disposes the handles kept in $State.
    $target = [IO.Path]::Combine($Plan.root, $script:QuarantinePrefix + [guid]::NewGuid().ToString('N'))
    try { [IO.Directory]::Move($Plan.updaterDir, $target) }
    catch [IO.DirectoryNotFoundException], [IO.FileNotFoundException] {
        return 'UpdaterDir disappeared before it could be quarantined.'
    }
    $State.quarantine = $target
    $hold = [TraLuatPxu.NativeFs]::Open($target, $true, $false, $true)
    $State.holdNode = $hold
    if ($hold.Error -ne 0) { throw "Opening the quarantined updater directory failed with Win32 error $($hold.Error)." }
    if (Test-InstallNodeReparse $hold) { return 'After quarantine: UpdaterDir is a reparse point.' }
    if (-not (Test-InstallNodeDirectory $hold)) { return 'After quarantine: UpdaterDir is not a directory.' }
    $canonicalTarget = [IO.Path]::Combine($Plan.rootCanonical, [IO.Path]::GetFileName($target))
    if (-not (Test-InstallSamePath $hold.FinalPath $canonicalTarget)) {
        return "After quarantine: the directory resolves to '$($hold.FinalPath)', not to '$canonicalTarget'."
    }
    # The directory handle is held from here on, so this listing is of the verified directory.
    $found = Get-InstallUpdaterEntry $target
    if ($null -ne $found.refusal) { return "After quarantine: $($found.refusal)" }
    $file = [TraLuatPxu.NativeFs]::Open($found.item, $false, $true, $true)
    $State.fileNode = $file
    if ($file.Error -eq 2 -or $file.Error -eq 3) { return 'After quarantine: installer.exe is no longer there.' }
    if ($file.Error -ne 0) { throw "Opening the quarantined installer.exe failed with Win32 error $($file.Error)." }
    if (Test-InstallNodeReparse $file) { return 'After quarantine: installer.exe is a reparse point.' }
    if (Test-InstallNodeDirectory $file) { return 'After quarantine: installer.exe is a directory.' }
    $canonicalItem = [IO.Path]::Combine($canonicalTarget, [IO.Path]::GetFileName($found.item))
    if (-not (Test-InstallSamePath $file.FinalPath $canonicalItem)) {
        return "After quarantine: installer.exe resolves to '$($file.FinalPath)', not to '$canonicalItem'."
    }
    # Size and hash are read through the very handle that is later marked for deletion.
    $State.stream = [IO.FileStream]::new($file.Handle, [IO.FileAccess]::Read)
    $contentRefusal = Get-InstallContentRefusal $State.stream $Plan.bytes $Plan.expectedSha
    if ($null -ne $contentRefusal) { return "After quarantine: $contentRefusal" }
    $State.item = $found.item
    return $null
}

function Invoke-InstallRemovalCore($Plan, $State, $Actions) {
    $native = [TraLuatPxu.NativeFs]
    if ($Plan.installPlanned) {
        # The object at InstallDir itself is opened (a link is not followed) and held until it is deleted.
        $State.installNode = $native::Open($Plan.installDir, $true, $false, $true)
        if ($State.installNode.Error -eq 2 -or $State.installNode.Error -eq 3) {
            return (New-InstallChange 'InstallDir is no longer there.')
        }
        if ($State.installNode.Error -ne 0) { throw "Opening InstallDir failed with Win32 error $($State.installNode.Error)." }
        if (Test-InstallNodeReparse $State.installNode) {
            # A link appeared after the preliminary check: remove the link object, never what it points to.
            $unlinkError = $native::MarkDelete($State.installNode.Handle)
            if ($unlinkError -ne 0) { throw "Unlinking the reparse point at InstallDir failed with Win32 error $unlinkError." }
            $State.installNode.Dispose()
            Wait-InstallGone $Plan.installDir
            $Actions.Add("unlinked junction at InstallDir $($Plan.installDir) (target untouched)")
            return (New-InstallChange 'InstallDir became a reparse point after the preliminary check.')
        }
        if (-not (Test-InstallNodeDirectory $State.installNode)) { return (New-InstallChange 'InstallDir is not a directory.') }
        # An ancestor swapped for a link shows up here: the opened object is then somewhere else.
        if (-not (Test-InstallSamePath $State.installNode.FinalPath $Plan.installCanonical)) {
            return (New-InstallChange "InstallDir resolves to '$($State.installNode.FinalPath)', not to '$($Plan.installCanonical)'.")
        }
        $installChange = Get-InstallDirRefusal $Plan.installDir
        if ($null -ne $installChange) { return (New-InstallChange $installChange) }
    }
    if ($Plan.updaterPlanned) {
        $isolationRefusal = Enter-InstallUpdaterQuarantine $Plan $State
        if ($null -ne $isolationRefusal) { return (New-InstallChange $isolationRefusal) }
    }
    # Both targets are verified and held. Only now is anything removed.
    if ($Plan.installPlanned) {
        $installError = $native::MarkDelete($State.installNode.Handle)
        if ($installError -eq $script:ErrorDirNotEmpty) { return (New-InstallChange 'InstallDir gained entries after the preliminary check.') }
        if ($installError -ne 0) { throw "Removing InstallDir failed with Win32 error $installError." }
        $State.installNode.Dispose()
        Wait-InstallGone $Plan.installDir
        $Actions.Add("removed empty directory $($Plan.installDir)")
        $State.removed++
    }
    if ($Plan.updaterPlanned -and $null -ne $State.stream) {
        $target = $State.quarantine
        if ($Plan.hookStage -ceq 'BeforeInstallerDelete' -and $null -ne $Plan.hook) { $null = & $Plan.hook $target }
        $fileError = $native::MarkDelete($State.fileNode.Handle)
        if ($fileError -ne 0) { throw "Removing the verified installer.exe failed with Win32 error $fileError." }
        $State.installerRemoved = $true
        $State.stream.Dispose()
        $State.fileNode.Dispose()
        Wait-InstallGone $State.item
        $linkNote = ''
        if ($State.fileNode.Links -gt 1) { $linkNote = "; it had $($State.fileNode.Links) hard links, the other names remain" }
        $Actions.Add("removed file $([IO.Path]::Combine($Plan.updaterDir, $script:InstallerName)) (verified and deleted by handle under $target$linkNote)")
        $State.removed++
        $holdError = 0
        for ($attempt = 0; $attempt -lt 10; $attempt++) {
            $holdError = $native::MarkDelete($State.holdNode.Handle)
            if ($holdError -ne $script:ErrorDirNotEmpty) { break }
            [Threading.Thread]::Sleep(200)
        }
        if ($holdError -eq $script:ErrorDirNotEmpty) {
            # Measured, not assumed: list what is in the way.
            $names = @([IO.Directory]::GetFileSystemEntries($target) | ForEach-Object { [IO.Path]::GetFileName($_) })
            if ($names.Count -eq 0) {
                $Actions.Add("retained quarantine $target (it reports not empty but lists no entries)")
                throw 'Removing the quarantined updater directory failed: it reports not empty but lists no entries.'
            }
            $Actions.Add("retained quarantine $target; installer.exe was removed, these entries appeared after verification: $($names -join ', ')")
            return (New-InstallChange 'The quarantined updater directory gained entries after verification.')
        }
        if ($holdError -ne 0) {
            $Actions.Add("retained quarantine $target (installer.exe was removed; removing the directory failed with Win32 error $holdError)")
            throw "Removing the quarantined updater directory failed with Win32 error $holdError."
        }
        $State.holdNode.Dispose()
        Wait-InstallGone $target
        $State.quarantine = $null
        $Actions.Add("removed directory $($Plan.updaterDir)")
        $State.removed++
    }
    return @{ code = 'done'; detail = $null; removed = 0 }
}

function Invoke-InstallRemoval($Plan, $Actions) {
    # Runs the removal, always closes every handle, and puts a quarantined updater back when its
    # installer was not removed. Returns code 'done' or 'changed' with the number of removals.
    $state = @{
        installNode = $null; holdNode = $null; fileNode = $null; stream = $null
        quarantine = $null; item = $null; installerRemoved = $false; removed = 0
    }
    $outcome = $null
    $failure = $null
    try { $outcome = Invoke-InstallRemovalCore $Plan $state $Actions }
    catch { $failure = $_ }
    finally {
        foreach ($name in 'stream', 'fileNode', 'holdNode', 'installNode') {
            if ($null -ne $state[$name]) { try { $state[$name].Dispose() } catch { $null = $_ } }
        }
    }
    if ($null -ne $state.quarantine -and -not $state.installerRemoved) {
        $Actions.Add("renamed $($Plan.updaterDir) to $($state.quarantine)")
        $null = Restore-InstallUpdater $state.quarantine $Plan.updaterDir $Actions
    }
    if ($null -ne $failure) { throw $failure }
    $outcome.removed = $state.removed
    return $outcome
}

function Remove-ProximaUninstallResidue {
    [CmdletBinding()]
    param(
        [Parameter()][AllowNull()]$LocalAppData = $env:LOCALAPPDATA,
        [Parameter()][AllowNull()]$InstallerSha256 = $script:DefaultInstallerSha256,
        [Parameter()][long]$InstallerBytes = $script:DefaultInstallerBytes,
        [Parameter()][AllowNull()]$ProcessProvider = { Get-Process -ErrorAction Stop },
        [Parameter()][AllowNull()]$UninstallKeyProvider = $script:DefaultUninstallKeyProvider,
        [Parameter(DontShow = $true)][AllowNull()]$TestHook = $null,
        [Parameter(DontShow = $true)][AllowNull()]$TestHookStage = 'BeforeRemoval',
        [Parameter()][switch]$WhatIf
    )
    $ErrorActionPreference = 'Stop'
    $actions = [Collections.Generic.List[string]]::new()
    $before = $null
    $removed = 0
    $root = $null
    $rootNode = $null
    $programsDir = $null
    $installDir = $null
    $updaterDir = $null
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
        if ($TestHookStage -isnot [string] -or ($TestHookStage -cne 'BeforeRemoval' -and $TestHookStage -cne 'BeforeInstallerDelete')) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'TestHookStage is not a known stage.' $null)
        }
        if ($InstallerSha256 -isnot [string] -or $InstallerSha256 -cnotmatch '\A[0-9A-Fa-f]{64}\z') {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'InstallerSha256 must be 64 hexadecimal characters.' $null)
        }
        $expectedSha = [string]$InstallerSha256
        $bytes = [long]$InstallerBytes
        if ($bytes -le 0) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'InstallerBytes must be a positive integer.' $null)
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

        # LocalAppData is held open (no delete sharing) for the whole call; its final path is the
        # canonical base every other opened object must sit under.
        Initialize-InstallNative
        $rootNode = [TraLuatPxu.NativeFs]::Open($root, $true, $false, $false)
        if ($rootNode.Error -ne 0) { throw "Opening LocalAppData failed with Win32 error $($rootNode.Error)." }
        if ((Test-InstallNodeReparse $rootNode) -or -not (Test-InstallNodeDirectory $rootNode)) {
            return (New-InstallResult 'BAD_ARGUMENT' $false $actions $null $null 'LocalAppData must be a directory that is not a reparse point.' $null)
        }
        $rootCanonical = [string]$rootNode.FinalPath
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
        if ($updaterPresent) { $updaterRefusal = Get-InstallUpdaterRefusal $updaterDir $bytes $expectedSha }
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
            if ($null -ne $TestHook -and $TestHookStage -ceq 'BeforeRemoval') { $null = & $TestHook }

            # Everything from here on distrusts the preliminary check and works on held handles.
            $plan = @{
                root = $root; rootCanonical = $rootCanonical
                installDir = $installDir; installCanonical = [IO.Path]::Combine($rootCanonical, 'Programs', 'Proxima')
                updaterDir = $updaterDir; bytes = $bytes; expectedSha = $expectedSha
                installPlanned = $installPlanned; updaterPlanned = $updaterPlanned
                hook = $TestHook; hookStage = $TestHookStage
            }
            $outcome = Invoke-InstallRemoval $plan $actions
            $removed += $outcome.removed
            if ($outcome.code -ceq 'changed') {
                $after = Get-InstallInventorySafe $root $programsDir $installDir $updaterDir
                return (New-InstallResult 'RESIDUE_CHANGED' $false $actions $before $after $outcome.detail $null)
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
        # Whatever was already done is in actions; a quarantined updater was put back or its path recorded.
        $message = $_.Exception.Message
        $after = $null
        if ($null -ne $root) { $after = Get-InstallInventorySafe $root $programsDir $installDir $updaterDir }
        return (New-InstallResult 'NOT_MEASURED' $false $actions $before $after $null $message)
    } finally {
        if ($null -ne $rootNode) { try { $rootNode.Dispose() } catch { $null = $_ } }
    }
}

Export-ModuleMember -Function Remove-ProximaUninstallResidue
