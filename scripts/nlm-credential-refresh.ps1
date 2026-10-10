#requires -Version 7.0
# WP710: refresh -> real notebook canary -> stage, serialized on this host. Never prints child output.
# Exit codes: 0 staged; 2 refresh/canary rc != 0 (auth_failure, network_failure or inconclusive);
# 3 timeout; 4 inconclusive (canary body or preflight); 5 inconclusive/lock_busy/tree_quarantine/tree_containment;
# 6 stage_failure.
param(
    [Parameter(Mandatory=$true)][string]$ConfigPath,
    [string]$NlmCommand = 'nlm',
    [string[]]$NlmArgumentsPrefix = @(),
    [string]$StageCommand = 'python',
    [string[]]$StageArguments = @((Join-Path $PSScriptRoot 'tl.py'), 'nlm-auth-stage'),
    [int]$TimeoutSeconds = 120,
    [int]$LockWaitSeconds = 10,
    [switch]$EnableKeepalive,
    [int]$IntervalSeconds = 3600,
    [int]$MaxCycles = 1,
    # Bounded exit for an operation record whose process tree cannot be MEASURED (see Get-RecordVerdict). It never
    # releases a tree that was measured and found alive or unknown.
    [int]$UnconfirmedQuarantineSeconds = 900,
    # WP714 round 4: the manual exit, with evidence. An operator who has checked the old tree by hand releases a
    # quarantined record (never a tree proven alive); the reason is carried in the emitted evidence.
    [string]$OperatorReleaseReason = ''
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

# A child that outlives a killed wrapper keeps running after the OS mutex is released. The wrapper
# records each operation here BEFORE spawning it (marker, then pid + start time) and a new owner waits
# until that operation is gone. Every child gets TRA_LUAT_NLM_OP=<marker> in its environment; descendants
# inherit it, so on Linux the whole tree is found again even after the direct child exited.
$OperationRecord = Join-Path ([IO.Path]::GetTempPath()) 'tra_luat_nlm_credential_refresh.operation.json'
$MarkerName = 'TRA_LUAT_NLM_OP'
$Evidence = [ordered]@{ cycle = 0; profile_fingerprint = ''; cli_version = ''; takeover = 'none'; takeover_reason = '';
    operator_reason = ''; containment_reason = ''; steps = [ordered]@{} }

# WP714 round 3: the ONE place that decides whether this platform can enumerate the operation's process
# tree. Only Linux can (/proc). Everywhere else every "no descendant found" is NOT MEASURED, never "none".
$TreeMeasurable = [bool]$IsLinux
# WP710 g4 (Windows): a step's processes are CONTAINED, not enumerated. Each step runs in its own named Job
# Object with JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE; the child is created suspended and assigned before its first
# instruction, so every descendant is born inside the job (no breakaway is granted). The job's own
# ActiveProcesses count is the measurement: 0 is the only proof that the step's tree is gone.
$JobContainment = [bool]$IsWindows
$JobPrefix = 'Global\tra_luat_nlm_op_'
$JobReady = $false
$ProcRoot = '/proc'   # where the operation tree is enumerated (the wrapper's own entry is always /proc/$PID)
$Subreaper = $false
$CanReap = $false
$OwnUid = $null
$OwnerStartJiffies = $null
# WP714 round 4: "pid:start" of this wrapper and every ancestor, recorded so a later owner knows who could have
# ADOPTED an orphan of this run (only an ancestor subreaper or init can). $null = could not be read.
$OwnerChain = $null

function Read-ProcStat([string]$dir) {
    # /proc/<pid>/stat -> @{State; Ppid; Start}; $null when the process is gone. Throws when it exists but
    # cannot be read, so the caller counts it as unknown instead of absent.
    try { $text = [IO.File]::ReadAllText("$dir/stat") }
    catch { if ([IO.Directory]::Exists($dir)) { throw } else { return $null } }
    $fields = $text.Substring($text.LastIndexOf(')') + 2).Split(' ')
    # flags & PF_KTHREAD (0x00200000): a kernel thread is never a descendant of a user process.
    return @{ State = $fields[0]; Ppid = [int]$fields[1]; Start = [uint64]$fields[19]
        Kernel = (([uint64]$fields[6] -band 0x00200000) -ne 0) }
}

function Read-ProcUid([string]$dir) {
    try { $text = [IO.File]::ReadAllText("$dir/status") }
    catch { if ([IO.Directory]::Exists($dir)) { throw } else { return $null } }
    $match = [regex]::Match($text, '(?m)^Uid:\s+(\d+)')
    if (-not $match.Success) { throw 'status without Uid' }
    return [int64]$match.Groups[1].Value
}

if ($TreeMeasurable) {
    # A child subreaper adopts every orphan of this wrapper's subtree (a daemon that double-forked, cleared its
    # environment or made itself non-dumpable), so while this wrapper lives its descendants are found by
    # parent links, not only by the inherited marker. Failure leaves the marker scan, with unknowns blocking.
    # WP714 round 4: an adopted orphan that is stopped stays a ZOMBIE child of this wrapper until it is waited
    # for, and .NET only waits for the processes it started itself. waitpid reaps the adopted ones (see
    # Invoke-ReapAdopted); the direct child of each step is left to .NET.
    try {
        Add-Type -Namespace TraLuatWp710 -Name NativeLinux -MemberDefinition ('[DllImport("libc", SetLastError = true)] public static extern int prctl(int option, ulong arg2, ulong arg3, ulong arg4, ulong arg5);' +
            ' [DllImport("libc", SetLastError = true)] public static extern int waitpid(int pid, out int status, int options);')
        $Subreaper = ([TraLuatWp710.NativeLinux]::prctl(36, 1, 0, 0, 0) -eq 0)
        $CanReap = $Subreaper
    } catch { $Subreaper = $false; $CanReap = $false }
    try {
        $OwnUid = Read-ProcUid "/proc/$PID"
        $OwnerStartJiffies = (Read-ProcStat "/proc/$PID").Start
    } catch { $OwnUid = $null; $OwnerStartJiffies = $null }
    try {
        $chain = [Collections.Generic.List[string]]::new()
        $walk = $PID
        while ($walk -gt 1 -and $chain.Count -lt 512) {
            $stat = Read-ProcStat "/proc/$walk"
            if ($null -eq $stat) { break }
            $chain.Add("$walk`:$($stat.Start)")
            $walk = $stat.Ppid
        }
        $OwnerChain = @($chain)
    } catch { $OwnerChain = $null }
}

if ($JobContainment) {
    # No job API, no step: Invoke-Bounded refuses (rc 5) instead of falling back to an uncontained child.
    try {
        Add-Type -TypeDefinition @'
using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Win32.SafeHandles;
namespace TraLuatWp710 {
    public sealed class JobChild {
        public IntPtr Process; public IntPtr Thread; public int Id; public SafeFileHandle Out; public SafeFileHandle Err;
    }
    public static class Job {
        [StructLayout(LayoutKind.Sequential)] struct BasicLimit {
            public long PerProcessUserTimeLimit, PerJobUserTimeLimit; public uint LimitFlags;
            public UIntPtr MinimumWorkingSetSize, MaximumWorkingSetSize; public uint ActiveProcessLimit;
            public UIntPtr Affinity; public uint PriorityClass, SchedulingClass;
        }
        [StructLayout(LayoutKind.Sequential)] struct IoCounters { public ulong A, B, C, D, E, F; }
        [StructLayout(LayoutKind.Sequential)] struct ExtendedLimit {
            public BasicLimit Basic; public IoCounters Io;
            public UIntPtr ProcessMemoryLimit, JobMemoryLimit, PeakProcessMemoryUsed, PeakJobMemoryUsed;
        }
        [StructLayout(LayoutKind.Sequential)] struct Accounting {
            public long TotalUserTime, TotalKernelTime, ThisPeriodTotalUserTime, ThisPeriodTotalKernelTime;
            public uint TotalPageFaultCount, TotalProcesses, ActiveProcesses, TotalTerminatedProcesses;
        }
        [StructLayout(LayoutKind.Sequential)] struct StartupInfo {
            public int cb; public IntPtr lpReserved, lpDesktop, lpTitle;
            public int dwX, dwY, dwXSize, dwYSize, dwXCountChars, dwYCountChars, dwFillAttribute, dwFlags;
            public short wShowWindow, cbReserved2; public IntPtr lpReserved2, hStdInput, hStdOutput, hStdError;
        }
        [StructLayout(LayoutKind.Sequential)] struct StartupInfoEx { public StartupInfo Info; public IntPtr AttributeList; }
        [StructLayout(LayoutKind.Sequential)] struct ProcessInformation {
            public IntPtr hProcess, hThread; public int dwProcessId, dwThreadId;
        }
        const string K = "kernel32.dll";
        [DllImport(K, SetLastError = true, CharSet = CharSet.Unicode)] static extern IntPtr CreateJobObjectW(IntPtr sa, string name);
        [DllImport(K, SetLastError = true, CharSet = CharSet.Unicode)] static extern IntPtr OpenJobObjectW(uint access, bool inherit, string name);
        [DllImport(K, SetLastError = true)] static extern bool SetInformationJobObject(IntPtr job, int cls, ref ExtendedLimit info, int length);
        [DllImport(K, SetLastError = true)] static extern bool QueryInformationJobObject(IntPtr job, int cls, out Accounting info, int length, IntPtr returned);
        [DllImport(K, SetLastError = true, EntryPoint = "QueryInformationJobObject")] static extern bool QueryJobBuffer(IntPtr job, int cls, IntPtr buffer, int length, IntPtr returned);
        [DllImport(K, SetLastError = true)] static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
        [DllImport(K, SetLastError = true)] static extern bool IsProcessInJob(IntPtr process, IntPtr job, out bool result);
        [DllImport(K, SetLastError = true)] static extern bool TerminateJobObject(IntPtr job, uint exitCode);
        [DllImport(K, SetLastError = true)] static extern bool CreatePipe(out IntPtr read, out IntPtr write, IntPtr sa, int size);
        [DllImport(K, SetLastError = true)] static extern bool SetHandleInformation(IntPtr handle, int mask, int flags);
        [DllImport(K, SetLastError = true, CharSet = CharSet.Unicode)] static extern bool CreateProcessW(string application, StringBuilder commandLine,
            IntPtr processAttributes, IntPtr threadAttributes, bool inheritHandles, uint flags, byte[] environment, string directory,
            ref StartupInfoEx startupInfo, out ProcessInformation information);
        [DllImport(K, SetLastError = true, CharSet = CharSet.Unicode)] static extern IntPtr CreateFileW(string name, uint access, uint share,
            IntPtr securityAttributes, uint disposition, uint flags, IntPtr template);
        [DllImport(K, SetLastError = true)] static extern bool InitializeProcThreadAttributeList(IntPtr list, int count, int flags, ref IntPtr size);
        [DllImport(K, SetLastError = true)] static extern bool UpdateProcThreadAttribute(IntPtr list, uint flags, IntPtr attribute, IntPtr value,
            IntPtr size, IntPtr previous, IntPtr returned);
        [DllImport(K)] static extern void DeleteProcThreadAttributeList(IntPtr list);
        [DllImport(K, SetLastError = true)] static extern uint ResumeThread(IntPtr thread);
        [DllImport(K, SetLastError = true)] static extern bool TerminateProcess(IntPtr process, uint exitCode);
        [DllImport(K, SetLastError = true)] static extern uint WaitForSingleObject(IntPtr handle, uint milliseconds);
        [DllImport(K, SetLastError = true)] static extern bool GetExitCodeProcess(IntPtr process, out uint exitCode);
        [DllImport(K, SetLastError = true)] static extern bool CloseHandle(IntPtr handle);

        // A new, named job that kills every member when its last handle closes. Zero + error on any failure,
        // including a name that already exists (that job is somebody else's).
        public static IntPtr Create(string name, out int error) {
            IntPtr job = CreateJobObjectW(IntPtr.Zero, name);
            error = Marshal.GetLastWin32Error();
            if (job == IntPtr.Zero) return job;
            if (error == 183) { CloseHandle(job); return IntPtr.Zero; }
            ExtendedLimit info = new ExtendedLimit();
            info.Basic.LimitFlags = 0x2000;   // JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if (!SetInformationJobObject(job, 9, ref info, Marshal.SizeOf(typeof(ExtendedLimit)))) {
                error = Marshal.GetLastWin32Error(); CloseHandle(job); return IntPtr.Zero;
            }
            error = 0;
            return job;
        }
        // ActiveProcesses of the job (JobObjectBasicAccountingInformation); -1 when it cannot be read.
        public static int Active(IntPtr job) {
            Accounting info;
            if (!QueryInformationJobObject(job, 1, out info, Marshal.SizeOf(typeof(Accounting)), IntPtr.Zero)) return -1;
            return (int)info.ActiveProcesses;
        }
        // Members other than the step's direct child (JobObjectBasicProcessIdList); -1 when it cannot be read.
        public static int Others(IntPtr job, int root) {
            int size = 8 + IntPtr.Size * 4096;
            IntPtr buffer = Marshal.AllocHGlobal(size);
            try {
                if (!QueryJobBuffer(job, 3, buffer, size, IntPtr.Zero)) return -1;
                int listed = Marshal.ReadInt32(buffer, 4), others = 0;
                for (int i = 0; i < listed; i++) {
                    if (Marshal.ReadIntPtr(buffer, 8 + IntPtr.Size * i).ToInt64() != root) others++;
                }
                return others;
            } finally { Marshal.FreeHGlobal(buffer); }
        }
        // A job recorded by an earlier owner: 0 opened (active = its ActiveProcesses), 1 no job has that name,
        // 2 it exists but cannot be opened or read. The handle is closed again before returning.
        public static int Probe(string name, out int active) {
            active = -1;
            IntPtr job = OpenJobObjectW(0x0004, false, name);   // JOB_OBJECT_QUERY
            if (job == IntPtr.Zero) return Marshal.GetLastWin32Error() == 2 ? 1 : 2;
            try { active = Active(job); } finally { CloseHandle(job); }
            return active < 0 ? 2 : 0;
        }
        public static bool Terminate(IntPtr job) { return TerminateJobObject(job, 1); }
        public static void Close(IntPtr handle) { if (handle != IntPtr.Zero) CloseHandle(handle); }

        // Create the child SUSPENDED with redirected stdout/stderr, put it in the job and verify the membership.
        // It has not executed anything when this returns; Resume starts it. null + stage/error on failure: a
        // child that could not be placed in the job is terminated before it ever ran. pid is set as soon as the
        // process exists, so a caller can still name a child whose termination could not be confirmed
        // (stage ends in _alive): that child is suspended, outside the job, and nothing else tracks it.
        public static JobChild Start(IntPtr job, string commandLine, byte[] environment, out string stage, out int error, out int pid) {
            stage = ""; error = 0; pid = 0;
            IntPtr outRead, outWrite, errRead, errWrite;
            if (!CreatePipe(out outRead, out outWrite, IntPtr.Zero, 0)) { error = Marshal.GetLastWin32Error(); stage = "pipe"; return null; }
            if (!CreatePipe(out errRead, out errWrite, IntPtr.Zero, 0)) {
                error = Marshal.GetLastWin32Error(); stage = "pipe"; CloseHandle(outRead); CloseHandle(outWrite); return null;
            }
            ProcessInformation pi = new ProcessInformation();
            bool created = false;
            // g5: the child inherits EXACTLY three handles (PROC_THREAD_ATTRIBUTE_HANDLE_LIST): NUL as stdin and
            // the two pipe write ends. With a plain bInheritHandles it would also inherit every inheritable
            // handle of this wrapper - its own stdout/stderr among them - and a descendant that outlives the
            // wrapper would keep the wrapper's caller waiting on a pipe that never closes (measured: a stray
            // suspended child held the caller for 13 minutes).
            IntPtr nul = CreateFileW("NUL", 0x80000000, 3, IntPtr.Zero, 3, 0, IntPtr.Zero);
            IntPtr list = IntPtr.Zero, handles = IntPtr.Zero;
            bool listReady = false;
            try {
                IntPtr size = IntPtr.Zero;
                InitializeProcThreadAttributeList(IntPtr.Zero, 1, 0, ref size);
                if (nul == new IntPtr(-1) || nul == IntPtr.Zero || size == IntPtr.Zero ||
                    !SetHandleInformation(nul, 1, 1) || !SetHandleInformation(outWrite, 1, 1) || !SetHandleInformation(errWrite, 1, 1)) {
                    error = Marshal.GetLastWin32Error(); stage = "pipe";
                } else {
                    list = Marshal.AllocHGlobal(size);
                    handles = Marshal.AllocHGlobal(IntPtr.Size * 3);
                    Marshal.WriteIntPtr(handles, 0, nul);
                    Marshal.WriteIntPtr(handles, IntPtr.Size, outWrite);
                    Marshal.WriteIntPtr(handles, IntPtr.Size * 2, errWrite);
                    listReady = InitializeProcThreadAttributeList(list, 1, 0, ref size);
                    // PROC_THREAD_ATTRIBUTE_HANDLE_LIST
                    if (!listReady || !UpdateProcThreadAttribute(list, 0, new IntPtr(0x00020002), handles, new IntPtr(IntPtr.Size * 3), IntPtr.Zero, IntPtr.Zero)) {
                        error = Marshal.GetLastWin32Error(); stage = "pipe";
                    } else {
                        StartupInfoEx si = new StartupInfoEx();
                        si.Info.cb = Marshal.SizeOf(typeof(StartupInfoEx));
                        si.Info.dwFlags = 0x100;   // STARTF_USESTDHANDLES
                        si.Info.hStdInput = nul; si.Info.hStdOutput = outWrite; si.Info.hStdError = errWrite;
                        si.AttributeList = list;
                        // CREATE_SUSPENDED | CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT
                        created = CreateProcessW(null, new StringBuilder(commandLine), IntPtr.Zero, IntPtr.Zero, true, 0x4 | 0x400 | 0x00080000,
                            environment, null, ref si, out pi);
                        if (!created) { error = Marshal.GetLastWin32Error(); stage = "create"; }
                    }
                }
            } finally {
                if (listReady) DeleteProcThreadAttributeList(list);
                if (list != IntPtr.Zero) Marshal.FreeHGlobal(list);
                if (handles != IntPtr.Zero) Marshal.FreeHGlobal(handles);
                if (nul != new IntPtr(-1) && nul != IntPtr.Zero) CloseHandle(nul);
            }
            CloseHandle(outWrite); CloseHandle(errWrite);   // the parent keeps only the read ends
            if (!created) { CloseHandle(outRead); CloseHandle(errRead); return null; }
            pid = pi.dwProcessId;
            bool member = false;
            if (!AssignProcessToJobObject(job, pi.hProcess)) { error = Marshal.GetLastWin32Error(); stage = "assign"; }
            else if (!IsProcessInJob(pi.hProcess, job, out member)) { error = Marshal.GetLastWin32Error(); stage = "verify"; }
            else if (!member) { stage = "verify"; }
            if (stage.Length > 0) {
                TerminateProcess(pi.hProcess, 1);
                if (WaitForSingleObject(pi.hProcess, 5000) != 0) stage += "_alive";
                CloseHandle(pi.hThread); CloseHandle(pi.hProcess); CloseHandle(outRead); CloseHandle(errRead);
                return null;
            }
            JobChild child = new JobChild();
            child.Process = pi.hProcess; child.Thread = pi.hThread; child.Id = pi.dwProcessId;
            child.Out = new SafeFileHandle(outRead, true); child.Err = new SafeFileHandle(errRead, true);
            return child;
        }
        public static bool Resume(JobChild child) {
            bool resumed = ResumeThread(child.Thread) != 0xFFFFFFFF;
            CloseHandle(child.Thread); child.Thread = IntPtr.Zero;
            return resumed;
        }
        public static bool Wait(JobChild child, int milliseconds) {
            return WaitForSingleObject(child.Process, (uint)Math.Max(0, milliseconds)) == 0;
        }
        public static int ExitCode(JobChild child) {
            uint code;
            if (!GetExitCodeProcess(child.Process, out code)) return -1;
            return unchecked((int)code);
        }
        // The command line Process.Start builds from ArgumentList (CommandLineToArgvW rules).
        public static string Quote(string[] arguments) {
            StringBuilder line = new StringBuilder();
            foreach (string argument in arguments) {
                if (line.Length > 0) line.Append(' ');
                bool plain = argument.Length > 0;
                foreach (char c in argument) { if (char.IsWhiteSpace(c) || c == '"') { plain = false; break; } }
                if (plain) { line.Append(argument); continue; }
                line.Append('"');
                int slashes = 0;
                foreach (char c in argument) {
                    if (c == '\\') { slashes++; continue; }
                    if (c == '"') { line.Append('\\', slashes * 2 + 1); line.Append('"'); slashes = 0; continue; }
                    line.Append('\\', slashes); slashes = 0; line.Append(c);
                }
                line.Append('\\', slashes * 2);
                line.Append('"');
            }
            return line.ToString();
        }
        public static byte[] EnvironmentBlock(IDictionary variables) {
            List<string> keys = new List<string>();
            foreach (object key in variables.Keys) keys.Add((string)key);
            keys.Sort(StringComparer.OrdinalIgnoreCase);
            StringBuilder block = new StringBuilder();
            foreach (string key in keys) { block.Append(key).Append('=').Append((string)variables[key]).Append('\0'); }
            block.Append('\0');
            return Encoding.Unicode.GetBytes(block.ToString());
        }
    }
}
'@
        $JobReady = $true
    } catch { $JobReady = $false }
}

function Emit([string]$status, [string]$step, [int]$rc, [double]$elapsed) {
    # Never emit child stdout/stderr: either stream can include cookies.
    [ordered]@{
        status = $status; step = $step; rc = $rc; elapsed_seconds = $elapsed; cycle = $Evidence.cycle
        profile_fingerprint = $Evidence.profile_fingerprint
        profile_fingerprint_basis = 'sha256 of the lower-cased full browser_profile_path declared in config (first 16 hex)'
        profile_bound_to_cli = $false
        cli_version = $Evidence.cli_version
        tree_measurement = $(if ($JobContainment) { 'windows_job_object' } elseif (-not $TreeMeasurable) { 'not_measurable' } elseif ($Subreaper) { 'linux_subreaper_and_marker' } else { 'linux_marker' })
        containment_reason = $Evidence.containment_reason
        takeover = $Evidence.takeover; takeover_reason = $Evidence.takeover_reason
        operator_reason = $Evidence.operator_reason
        steps = $Evidence.steps
    } | ConvertTo-Json -Compress -Depth 5
}

function Write-Step([string]$name, $result) {
    $Evidence.steps[$name] = [ordered]@{ rc = $result.rc; elapsed_seconds = $result.elapsed
        timeout = $result.timeout; child_confirmed_exited = $result.exited; descendants_stopped = $result.reaped
        tree_state = $result.tree }
}

function Get-StartTicks($process) {
    try { return $process.StartTime.ToUniversalTime().Ticks } catch { return $null }
}

function Get-OperationTree([string]$marker, $floor, [bool]$inRun, $escape = $null) {
    # Ids: live processes of the operation (marker in the inherited environment, plus - while this wrapper
    # runs - every descendant by parent link). Unknown: processes that COULD belong to it but whose
    # environment cannot be read (non-dumpable, or a vanished /proc entry that still exists), counted only
    # when they started after $floor and run under this user. Measured=$false: nothing was enumerated.
    # WP714 round 4, $escape (takeover of a record written by this version only): after the owner died a
    # descendant that CLEARED the marker is no longer linked to anything. Such a process started after the
    # step began (Floor). It is found when it still holds one of the step's redirected pipes (Pipes), and
    # otherwise it is UNKNOWN unless its parent line proves it unrelated: an orphan is re-parented only to an
    # ancestor subreaper of the dead owner (Chain) or to init, so a candidate whose oldest in-scope ancestor
    # hangs under init, under the recorded chain or under nothing readable cannot be told apart from an orphan.
    $tree = [pscustomobject]@{ Measured = $false; Ids = @(); Unknown = 0 }
    if (-not $TreeMeasurable) { return $tree }
    $haveMarker = $marker -match '^[0-9a-f]{32}$'
    $needle = "`0$MarkerName=$marker`0"
    $children = @{}
    $stats = @{}
    $found = [Collections.Generic.HashSet[int]]::new()
    $unreadable = [Collections.Generic.List[int]]::new()
    $candidates = [Collections.Generic.List[int]]::new()
    foreach ($dir in [IO.Directory]::GetDirectories($ProcRoot)) {
        $name = [IO.Path]::GetFileName($dir)
        if ($name -notmatch '^\d+$' -or [int]$name -eq $PID) { continue }
        $id = [int]$name
        try { $stat = Read-ProcStat $dir } catch { $unreadable.Add($id); continue }
        if ($null -eq $stat -or $stat.State -in @('Z', 'X')) { continue }   # zombies are dead
        $stats[$id] = $stat
        if (-not $children.ContainsKey($stat.Ppid)) { $children[$stat.Ppid] = [Collections.Generic.List[int]]::new() }
        $children[$stat.Ppid].Add($id)
        # Init (pid 1) is the ancestor of every process and kernel threads are not user processes: neither can
        # belong to an operation, and both have environments root cannot always read.
        if (-not $haveMarker -or $id -eq 1 -or $stat.Kernel) { continue }
        if ($null -ne $floor -and $stat.Start -lt [uint64]$floor) { continue }   # older than the owner: not ours
        if ($OwnUid -ne 0) {
            try { $uid = Read-ProcUid $dir } catch { $unreadable.Add($id); continue }
            if ($null -eq $uid) { continue }
            if ($null -ne $OwnUid -and $uid -ne $OwnUid) { continue }
        }
        try {
            $environ = "`0" + [Text.Encoding]::Latin1.GetString([IO.File]::ReadAllBytes("$dir/environ"))
            if ($environ.Contains($needle)) { [void]$found.Add($id) }
            elseif ($null -ne $escape -and $stat.Start -ge [uint64]$escape.Floor) { $candidates.Add($id) }
        } catch {
            if ([IO.Directory]::Exists($dir)) { $unreadable.Add($id) }   # exists but unreadable: UNKNOWN
        }
    }
    $escaped = 0
    if ($null -ne $escape -and -not $inRun -and $candidates.Count -gt 0) {
        # The new owner and its own ancestors are not the old operation.
        $self = [Collections.Generic.HashSet[int]]::new()
        [void]$self.Add($PID)
        try { $walk = (Read-ProcStat "/proc/$PID").Ppid } catch { $walk = 0 }
        while ($walk -gt 1 -and $self.Add($walk) -and $stats.ContainsKey($walk)) { $walk = $stats[$walk].Ppid }
        foreach ($id in $candidates) {
            if ($self.Contains($id)) { continue }
            if ($escape.Pipes.Count -gt 0) {
                $holds = $false
                try {
                    foreach ($fd in [IO.Directory]::GetFileSystemEntries("$ProcRoot/$id/fd")) {
                        if ($escape.Pipes.Contains([string]([IO.FileInfo]::new($fd)).LinkTarget)) { $holds = $true; break }
                    }
                } catch { if ([IO.Directory]::Exists("$ProcRoot/$id")) { $escaped++; continue } }
                if ($holds) { [void]$found.Add($id); continue }
            }
            $parent = $stats[$id].Ppid
            for ($hop = 0; $hop -lt 4096 -and $stats.ContainsKey($parent) -and -not $self.Contains($parent) -and
                 $stats[$parent].Start -ge [uint64]$escape.Floor; $hop++) { $parent = $stats[$parent].Ppid }
            if ($self.Contains($parent)) { continue }   # forked under the new owner's own line: not adopted
            if ($parent -le 1 -or -not $stats.ContainsKey($parent) -or $null -eq $escape.Chain -or
                $escape.Chain.Contains("$parent`:$($stats[$parent].Start)")) { $escaped++ }
        }
    }
    if ($inRun) {
        $queue = [Collections.Generic.Queue[int]]::new()
        $queue.Enqueue($PID)
        while ($queue.Count -gt 0) {
            $parent = $queue.Dequeue()
            if (-not $children.ContainsKey($parent)) { continue }
            foreach ($child in $children[$parent]) { [void]$found.Add($child); $queue.Enqueue($child) }
        }
    }
    $tree.Measured = $true
    $tree.Ids = @($found)
    # With the subreaper active every descendant is adopted, so parent links are complete in-run.
    $tree.Unknown = if ($inRun -and $Subreaper) { 0 } else { @($unreadable | Where-Object { -not $found.Contains($_) }).Count + $escaped }
    return $tree
}

function Invoke-ReapAdopted([int]$direct) {
    # WP714 round 4: wait for every ZOMBIE child of this wrapper except the step's direct child, which .NET
    # started and waits for itself (reaping it here would race Process.WaitForExit). With the subreaper set,
    # those zombies are the adopted descendants stopped above; without waitpid they pile up for the whole
    # keepalive run. WNOHANG (1): never blocks; a pid already reaped elsewhere returns -1 and is ignored.
    if (-not $CanReap) { return 0 }
    $reaped = 0
    for ($pass = 0; $pass -lt 20; $pass++) {
        $zombies = [Collections.Generic.List[int]]::new()
        foreach ($dir in [IO.Directory]::GetDirectories('/proc')) {
            $name = [IO.Path]::GetFileName($dir)
            if ($name -notmatch '^\d+$' -or [int]$name -eq $direct) { continue }
            try { $stat = Read-ProcStat $dir } catch { continue }
            if ($null -ne $stat -and $stat.Ppid -eq $PID -and $stat.State -eq 'Z') { $zombies.Add([int]$name) }
        }
        if ($zombies.Count -eq 0) { break }
        foreach ($zombie in $zombies) {
            $status = 0
            if ([TraLuatWp710.NativeLinux]::waitpid($zombie, [ref]$status, 1) -eq $zombie) { $reaped++ }
        }
    }
    return $reaped
}

function Stop-OperationTree([string]$marker, [bool]$inRun, [int]$direct = 0) {
    # Kill the operation's processes and confirm. State: gone | alive | unknown | not_measurable.
    # Only 'gone' is a proof; the other three keep the operation record. In-run, the stopped adopted
    # descendants are then reaped (Invoke-ReapAdopted), whatever the state.
    $tree = Get-OperationTree $marker $OwnerStartJiffies $inRun
    if (-not $tree.Measured) { return @{ State = 'not_measurable'; Stopped = 0 } }
    $stopped = [Collections.Generic.HashSet[int]]::new()
    $watch = [Diagnostics.Stopwatch]::StartNew()
    try {
        while ($tree.Ids.Count -gt 0) {
            foreach ($id in $tree.Ids) { [void]$stopped.Add($id); Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
            if ($watch.ElapsedMilliseconds -gt 5000) { return @{ State = 'alive'; Stopped = $stopped.Count } }
            Start-Sleep -Milliseconds 50
            $tree = Get-OperationTree $marker $OwnerStartJiffies $inRun
        }
        if ($tree.Unknown -gt 0) { return @{ State = 'unknown'; Stopped = $stopped.Count } }
        return @{ State = 'gone'; Stopped = $stopped.Count }
    } finally {
        if ($inRun) { [void](Invoke-ReapAdopted $direct) }
    }
}

function Write-OperationRecord($marker, $process, [bool]$unconfirmed, [string[]]$pipes = @(), [string]$job = '', [int]$strayPid = 0) {
    # format 2 (WP714 round 4) adds what a later owner needs to look for descendants that cleared the marker:
    # the step's start (before the spawn: the owner's own start, a lower bound), the step's redirected pipes
    # and the owner's ancestor chain. A record without format 2 is checked by marker only.
    $data = [ordered]@{ format = 2; marker = $marker; pid = $null; start_ticks = $null; tree_unconfirmed = $unconfirmed
        owner_start_jiffies = $OwnerStartJiffies; step_start_jiffies = $OwnerStartJiffies; owner_chain = $OwnerChain
        pipes = @($pipes) }
    if ($job) { $data.job = $job }   # Windows: the step's Job Object, so a later owner can ask it for its count
    if ($process) {
        $data.pid = $process.Id; $data.start_ticks = (Get-StartTicks $process)
        if ($TreeMeasurable) {
            try { $childStat = Read-ProcStat "/proc/$($process.Id)" } catch { $childStat = $null }
            if ($null -ne $childStat) { $data.step_start_jiffies = $childStat.Start }   # else keep the owner's (lower)
        }
    }
    if ($strayPid -gt 0) {
        # g5: a child that exists OUTSIDE its job (it could not be assigned and its termination was not confirmed).
        # The pid comes from CreateProcess itself, so it is recorded even when the process can no longer be
        # looked up or its start time cannot be read; the job named above says nothing about this process.
        $data.outside_job = $true
        if ($null -eq $data.pid) { $data.pid = $strayPid }
    }
    Set-Content -LiteralPath $OperationRecord -Value ($data | ConvertTo-Json -Compress -Depth 4) -Encoding utf8
}

function Get-StepPipes($process) {
    # "pipe:[inode]" of the step's redirected stdout/stderr, as this wrapper holds them. Linux only.
    if (-not $TreeMeasurable) { return @() }
    $pipes = foreach ($stream in @($process.StandardOutput.BaseStream, $process.StandardError.BaseStream)) {
        try { [string]([IO.FileInfo]::new("/proc/$PID/fd/" + $stream.SafePipeHandle.DangerousGetHandle().ToInt32())).LinkTarget } catch { }
    }
    return @($pipes | Where-Object { $_ -match '^pipe:\[\d+\]$' })
}

function Test-RecordedRootAlive($record) {
    # $true alive (or not decidable), $false gone or pid reused, $null no pid was ever recorded.
    if ($null -eq $record.pid -or $null -eq $record.start_ticks) { return $null }
    $process = Get-Process -Id ([int]$record.pid) -ErrorAction SilentlyContinue
    if (-not $process) { return $false }
    $ticks = Get-StartTicks $process
    if ($null -eq $ticks) { return $true }
    # A different start time is pid reuse, not the recorded child.
    if ([math]::Abs([int64]$ticks - [int64]$record.start_ticks) -gt 10000000) { return $false }
    if ($IsLinux) {
        try { if ([IO.File]::ReadAllText("/proc/$([int]$record.pid)/stat") -match '\)\s+Z\s') { return $false } } catch { }
    }
    return $true
}

function ConvertTo-Jiffies($value) {
    if (($value -is [long] -or $value -is [int]) -and $value -ge 0) { return [uint64]$value }
    return $null
}

function Get-RecordVerdict {
    # clear: no record, or Linux proved the old tree gone. alive: the old root or a member of the old operation
    # lives (marker, or a recorded pipe still held), or the record cannot be read (fail closed; an operator
    # deletes it). quarantine: the root is not alive but the tree is not proven gone.
    # WP714 round 4 - the timer is NOT evidence. A tree that was MEASURED and found unknown (Linux: unreadable
    # environments, or a candidate orphan that cleared the marker) stays quarantined: each run waits at most
    # -LockWaitSeconds and returns rc 5; it ends when the tree is proven gone, or by -OperatorReleaseReason.
    # Only a tree that cannot be measured at all (not Linux, or a record without a marker) still has the
    # bounded exit: the first owner that sees it stamps the record, and once -UnconfirmedQuarantineSeconds have
    # passed a takeover is released with takeover=quarantine_elapsed in the evidence (owner decision pending).
    if (-not (Test-Path -LiteralPath $OperationRecord -PathType Leaf)) { return @{ State = 'clear'; Reason = '' } }
    try { $record = [string](Get-Content -LiteralPath $OperationRecord -Raw) | ConvertFrom-Json } catch { $record = $null }
    if ($null -eq $record -or $record -isnot [pscustomobject]) { return @{ State = 'alive'; Reason = 'record_unreadable' } }
    if ((Test-RecordedRootAlive $record) -eq $true) { return @{ State = 'alive'; Reason = 'root_alive' } }
    # g5: the recorded child was never inside its job, so neither the job's count nor the job being closed can
    # prove anything about it. Not known alive (gone, pid reused, or no start time to tell) is still not proven
    # gone: quarantine, no timer, operator only.
    if ($record.outside_job -eq $true) { return @{ State = 'quarantine'; Reason = 'stray_child_unconfirmed' } }
    if ($JobContainment -and $JobReady -and [string]$record.job -cmatch ('^' + [regex]::Escape($JobPrefix) + '[0-9a-f]{32}$')) {
        # WP710 g4: the old step's job answers for its whole tree. Opened: its ActiveProcesses decides. No job
        # of that name: its last handle is closed, and KILL_ON_JOB_CLOSE ended every member at that close - but a
        # record whose owner already FAILED to empty that job (tree_unconfirmed) is not cleared by that alone.
        $active = -1
        switch ([TraLuatWp710.Job]::Probe([string]$record.job, [ref]$active)) {
            0 { if ($active -gt 0) { return @{ State = 'alive'; Reason = 'job_alive' } } else { return @{ State = 'clear'; Reason = '' } } }
            1 { if ($record.tree_unconfirmed -eq $false) { return @{ State = 'clear'; Reason = '' } } else { return @{ State = 'quarantine'; Reason = 'job_closed_unconfirmed' } } }
            default { return @{ State = 'quarantine'; Reason = 'job_unknown' } }
        }
    }
    $reason = 'tree_not_measurable'
    $marker = [string]$record.marker
    if ($marker -match '^[0-9a-f]{32}$') {
        $floor = ConvertTo-Jiffies $record.owner_start_jiffies
        $escape = $null
        if ($record.format -eq 2) {
            $chain = $null
            if ($null -ne $record.owner_chain) {
                $chain = [Collections.Generic.HashSet[string]]::new([string[]]@($record.owner_chain | Where-Object { $_ -is [string] }))
            }
            $pipes = [Collections.Generic.HashSet[string]]::new([string[]]@($record.pipes | Where-Object { $_ -is [string] -and $_ -match '^pipe:\[\d+\]$' }))
            $escapeFloor = ConvertTo-Jiffies $record.step_start_jiffies
            if ($null -eq $escapeFloor) { $escapeFloor = $floor }
            if ($null -eq $escapeFloor) { $escapeFloor = [uint64]0 }   # no bound: every process is in scope
            $escape = @{ Floor = $escapeFloor; Chain = $chain; Pipes = $pipes }
        }
        $tree = Get-OperationTree $marker $floor $false $escape
        if ($tree.Measured) {
            if ($tree.Ids.Count -gt 0) { return @{ State = 'alive'; Reason = 'marked_alive' } }
            if ($tree.Unknown -eq 0) { return @{ State = 'clear'; Reason = '' } }
            return @{ State = 'quarantine'; Reason = 'tree_unknown' }   # measured, not proven gone: no timer exit
        }
    }
    # WP710 g4: the timer exit exists only where the platform enumerates trees (a Linux record without a marker).
    # Everywhere else nothing was measured, so waiting proves nothing: quarantine until -OperatorReleaseReason.
    if (-not $TreeMeasurable) { return @{ State = 'quarantine'; Reason = $reason } }
    $now = [DateTime]::UtcNow.Ticks
    $seen = $record.root_dead_seen_utc_ticks
    if ($null -eq $seen) {
        $record | Add-Member -NotePropertyName root_dead_seen_utc_ticks -NotePropertyValue $now -Force
        Set-Content -LiteralPath $OperationRecord -Value ($record | ConvertTo-Json -Compress -Depth 4) -Encoding utf8
        $seen = $now
    }
    if (-not ($seen -is [long] -or $seen -is [int])) { return @{ State = 'alive'; Reason = 'record_unreadable' } }
    $age = $now - [int64]$seen
    if ($age -lt 0) { return @{ State = 'alive'; Reason = 'record_clock' } }
    if ($age -ge [int64]$UnconfirmedQuarantineSeconds * 10000000) { return @{ State = 'released'; Reason = $reason } }
    return @{ State = 'quarantine'; Reason = $reason }
}

function Stop-OperationJob([IntPtr]$job, [int]$root) {
    # Windows: end every process of the step's job and confirm by the job's own count.
    # State: gone (ActiveProcesses read as 0) | alive (still above 0 after 5 s) | unknown (the count cannot be read).
    # Stopped: members other than the step's direct child that were in the job when it was terminated.
    $others = [Math]::Max(0, [TraLuatWp710.Job]::Others($job, $root))
    $active = [TraLuatWp710.Job]::Active($job)
    if ($active -lt 0) { return @{ State = 'unknown'; Stopped = 0 } }
    if ($active -eq 0) { return @{ State = 'gone'; Stopped = 0 } }
    [void][TraLuatWp710.Job]::Terminate($job)
    $watch = [Diagnostics.Stopwatch]::StartNew()
    while ($watch.ElapsedMilliseconds -le 5000) {
        $active = [TraLuatWp710.Job]::Active($job)
        if ($active -eq 0) { return @{ State = 'gone'; Stopped = $others } }
        if ($active -lt 0) { return @{ State = 'unknown'; Stopped = $others } }
        Start-Sleep -Milliseconds 50
    }
    return @{ State = 'alive'; Stopped = $others }
}

function Invoke-BoundedJob([string]$file, [string[]]$arguments, [int]$seconds, [hashtable]$environment, [string]$marker) {
    # Windows path of Invoke-Bounded. A result with `blocked` set means the step's tree is not contained or not
    # proven gone: the caller stops with rc 5 (tree_containment) and never starts the next step.
    $budget = [int64]$seconds * 1000
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    $jobName = $JobPrefix + $marker
    $code = 0
    $job = [TraLuatWp710.Job]::Create($jobName, [ref]$code)
    if ($job -eq [IntPtr]::Zero) {   # nothing was started and no record was written
        return @{timeout=$false; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$false; reaped=0;
            tree='not_contained'; blocked="job_create_failed:$code"}
    }
    $child = $null
    $streams = @()
    $started = $false
    $confirmed = $false
    Write-OperationRecord $marker $null $false @() $jobName
    try {
        $variables = @{}
        foreach ($entry in [Environment]::GetEnvironmentVariables().GetEnumerator()) { $variables[[string]$entry.Key] = [string]$entry.Value }
        foreach ($key in $environment.Keys) { $variables[[string]$key] = [string]$environment[$key] }
        $variables[$MarkerName] = $marker
        $stage = ''
        $childId = 0
        $child = [TraLuatWp710.Job]::Start($job, [TraLuatWp710.Job]::Quote([string[]](@($file) + $arguments)),
            [TraLuatWp710.Job]::EnvironmentBlock($variables), [ref]$stage, [ref]$code, [ref]$childId)
        if ($null -eq $child) {
            if ($stage -in @('pipe', 'create')) { throw "process start failed ($stage $code)" }   # as Process.Start() would
            # Created but not in the job: it was terminated while still suspended, so no step code ran.
            $confirmed = $stage -notlike '*_alive'
            if (-not $confirmed) {
                # Its termination was NOT confirmed: a process exists, suspended and outside the job. The record
                # must survive this run and name it, so the next owner does not find "no record": it waits
                # (root_alive) while that child is recognised as alive by pid and start time, and is quarantined
                # (stray_child_unconfirmed) in every other case - gone, or no start time to recognise it by.
                $started = $true
                Write-OperationRecord $marker (Get-Process -Id $childId -ErrorAction SilentlyContinue) $true @() $jobName $childId
            }
            return @{timeout=$false; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$confirmed; reaped=0;
                tree='not_contained'; blocked="job_${stage}_failed:$code"}
        }
        $started = $true
        $process = Get-Process -Id $child.Id -ErrorAction SilentlyContinue
        Write-OperationRecord $marker $process $false @() $jobName
        $streams = @([IO.FileStream]::new($child.Out, [IO.FileAccess]::Read, 4096, $false),
            [IO.FileStream]::new($child.Err, [IO.FileAccess]::Read, 4096, $false))
        $outBytes = [IO.MemoryStream]::new()
        $stdout = $streams[0].CopyToAsync($outBytes)
        $stderr = [IO.StreamReader]::new($streams[1], $Utf8Lenient).ReadToEndAsync()
        $done = [TraLuatWp710.Job]::Resume($child)
        if ($done) { $done = [TraLuatWp710.Job]::Wait($child, [int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds)) }
        if ($done) {
            $done = [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($stdout, $stderr),
                [int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds))
        }
        if (-not $done) {
            # Budget spent (or the child could not be resumed): end the whole job, then prove it empty.
            $tree = Stop-OperationJob $job $child.Id
            $rootGone = [TraLuatWp710.Job]::Wait($child, 5000)
            $pipesClosed = $false
            try { $pipesClosed = [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($stdout, $stderr), 5000) } catch { $pipesClosed = $false }
            $confirmed = $rootGone -and $pipesClosed -and $tree.State -eq 'gone'
            if (-not $confirmed) { Write-OperationRecord $marker $process $true @() $jobName }
            return @{timeout=$true; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$confirmed;
                reaped=$tree.Stopped; tree=$tree.State}
        }
        # Success path: the direct child returned and the pipes are closed. Anything still in the job is a
        # descendant that dropped the pipes; it is ended and the job must count 0 before the next step may start.
        $tree = Stop-OperationJob $job $child.Id
        if ($tree.State -ne 'gone') {
            Write-OperationRecord $marker $process $true @() $jobName
            return @{timeout=$false; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$false;
                reaped=$tree.Stopped; tree=$tree.State; blocked="job_$($tree.State)"; ran=$true}
        }
        $confirmed = $true
        return @{timeout=$false; rc=[TraLuatWp710.Job]::ExitCode($child); out=$Utf8Lenient.GetString($outBytes.ToArray()); err=$stderr.Result;
            elapsed=$watch.Elapsed.TotalSeconds; exited=$true; reaped=$tree.Stopped; tree=$tree.State}
    } finally {
        if (-not $started -or $confirmed) { Remove-Item -LiteralPath $OperationRecord -ErrorAction SilentlyContinue }
        foreach ($stream in $streams) { try { $stream.Dispose() } catch { } }
        if ($null -ne $child) {
            [TraLuatWp710.Job]::Close($child.Thread); [TraLuatWp710.Job]::Close($child.Process)
            if ($streams.Count -eq 0) { $child.Out.Dispose(); $child.Err.Dispose() }
        }
        [TraLuatWp710.Job]::Close($job)   # last: closing the job ends whatever is still in it
    }
}

function Invoke-Bounded([string]$file, [string[]]$arguments, [int]$seconds, [hashtable]$environment = @{}) {
    $marker = [guid]::NewGuid().ToString('N')
    if ($JobContainment) {
        if (-not $JobReady) {
            return @{timeout=$false; rc=-1; out=''; err=''; elapsed=0.0; exited=$false; reaped=0; tree='not_contained';
                blocked='job_api_unavailable'}
        }
        return Invoke-BoundedJob $file $arguments $seconds $environment $marker
    }
    $info = [System.Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $file
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($arg in $arguments) { [void]$info.ArgumentList.Add($arg) }
    foreach ($key in $environment.Keys) { $info.Environment[$key] = [string]$environment[$key] }
    $info.Environment[$MarkerName] = $marker
    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $info
    $budget = [int64]$seconds * 1000
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    $started = $false
    $confirmed = $false
    # Record BEFORE spawning: a wrapper killed between Start() and the pid write leaves the marker behind
    # (Linux finds the tree by marker; elsewhere a record without pid goes to the bounded quarantine).
    Write-OperationRecord $marker $null $false
    try {
        [void]$process.Start()
        $started = $true
        $pipes = Get-StepPipes $process
        Write-OperationRecord $marker $process $false $pipes
        # WP714 round 4: stdout is read as BYTES and decoded once, the way the Python stage command does
        # (strict UTF-8 with U+FFFD for bad bytes, nothing stripped). StandardOutput would drop a UTF-8 BOM
        # (StreamReader detects it) and, on Windows, decode with the console code page.
        $outBytes = [IO.MemoryStream]::new()
        $stdout = $process.StandardOutput.BaseStream.CopyToAsync($outBytes)
        $stderr = $process.StandardError.ReadToEndAsync()
        $done = $process.WaitForExit([int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds))
        # A descendant can keep the redirected pipes open after the CLI exits; the budget covers both.
        if ($done) {
            $done = [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($stdout, $stderr),
                [int][Math]::Max(0, $budget - $watch.ElapsedMilliseconds))
        }
        if (-not $done) {
            # The direct child may have exited while a descendant still holds the pipes: Kill($true) cannot
            # reach an orphan, so the tree sweep does. Asking to kill is not proof of death: confirm the
            # child, the tree and that every pipe writer is gone, or keep the record. A tree that cannot be
            # enumerated (not Linux) or has unreadable members is NOT confirmed.
            try { if (-not $process.HasExited) { $process.Kill($true) } } catch { }
            $rootGone = $false
            try { $rootGone = $process.WaitForExit(5000) } catch { $rootGone = $false }
            $tree = Stop-OperationTree $marker $true $process.Id
            $pipesClosed = $false
            try { $pipesClosed = [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($stdout, $stderr), 5000) } catch { $pipesClosed = $false }
            $confirmed = $rootGone -and $pipesClosed -and $tree.State -eq 'gone'
            if (-not $confirmed) { Write-OperationRecord $marker $process $true $pipes }
            return @{timeout=$true; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$confirmed;
                reaped=$tree.Stopped; tree=$tree.State}
        }
        # Success path: a descendant that dropped the pipes may still run; it is part of this operation and
        # must not overlap the next step, so it is stopped and confirmed first (Linux). WP710 g4: a tree that
        # cannot be enumerated is NOT a tree that ended - the record stays and the run stops (rc 5).
        $tree = Stop-OperationTree $marker $true $process.Id
        if ($tree.State -in @('alive', 'unknown')) {
            Write-OperationRecord $marker $process $true $pipes
            return @{timeout=$true; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$false;
                reaped=$tree.Stopped; tree=$tree.State}
        }
        if ($tree.State -ne 'gone') {
            Write-OperationRecord $marker $process $true $pipes
            return @{timeout=$false; rc=-1; out=''; err=''; elapsed=$watch.Elapsed.TotalSeconds; exited=$false;
                reaped=$tree.Stopped; tree=$tree.State; blocked='tree_not_measurable'; ran=$true}
        }
        $confirmed = $true
        return @{timeout=$false; rc=$process.ExitCode; out=$Utf8Lenient.GetString($outBytes.ToArray()); err=$stderr.Result;
            elapsed=$watch.Elapsed.TotalSeconds; exited=$true; reaped=$tree.Stopped; tree=$tree.State}
    } finally {
        if (-not $started -or $confirmed) { Remove-Item -LiteralPath $OperationRecord -ErrorAction SilentlyContinue }
        $process.Dispose()
    }
}

$Utf8Lenient = [Text.UTF8Encoding]::new($false, $false)   # no BOM handling, bad bytes -> U+FFFD (Python errors='replace')

$CanaryKnownKeys = @('id', 'notebook_id', 'title', 'name', 'data', 'ok', 'error')

# WP714 round 4: ONE table of "blank" characters for title/name, the same numbers as
# tl_gws._NLM_CANARY_BLANK_CODEPOINTS (selftest wp714_canary_bang_trang_khop_ps compares them). Neither
# String.IsNullOrWhiteSpace nor Python str.strip(): their sets differ (U+001C-U+001F), measured.
$CanaryBlankCodePoints = @(
    0x0009, 0x000A, 0x000B, 0x000C, 0x000D, 0x001C, 0x001D, 0x001E, 0x001F, 0x0020, 0x0085, 0x00A0, 0x1680,
    0x180E, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x200B,
    0x200C, 0x200D, 0x2028, 0x2029, 0x202F, 0x205F, 0x2060, 0x3000, 0xFEFF
)
$CanaryBlank = [Collections.Generic.HashSet[int]]::new([int[]]$CanaryBlankCodePoints)

function Test-CanaryBlank([string]$text) {
    foreach ($ch in $text.ToCharArray()) { if (-not $CanaryBlank.Contains([int]$ch)) { return $false } }
    return $true
}

# WP714 round 4: the stdout the Python stage command judges is not the raw stdout. nlm_cli._run reads it with
# text=True (\r\n and \r become \n) and _strip_keyring then splits it with str.splitlines (which also breaks
# at \v \f \x1c \x1d \x1e \x85 \u2028 \u2029), drops keyring-noise lines that carry no {}[] and joins
# with \n. The wrapper applies the SAME transformation so both judge the same text. The pattern below is
# nlm_cli._KEYRING_NOISE_RE with Python's re semantics spelled out: \s is Python's str.isspace set and
# (?i) matches the case variants Python 3.11 matches (K: U+212A, S: U+017F, I: U+0130 U+0131), measured.
$KeyringNoise = '(?:[Uu][Ss\u017F][Ii\u0130\u0131][Nn][Gg]{0}+[Kk\u212A][Ee][Yy][Rr][Ii\u0130\u0131][Nn][Gg]{0}+[Bb][Aa][Cc][Kk\u212A][Ee][Nn][Dd]|[Kk\u212A][Ee][Yy][Rr][Ii\u0130\u0131][Nn][Gg]\.[Bb][Aa][Cc][Kk\u212A][Ee][Nn][Dd][Ss\u017F]?|[Nn][Oo]{0}+[Rr][Ee][Cc][Oo][Mm][Mm][Ee][Nn][Dd][Ee][Dd]{0}+[Bb][Aa][Cc][Kk\u212A][Ee][Nn][Dd])' -f '[\t\n\x0B\f\r\x1C-\x20\x85\xA0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]'

function ConvertTo-StageText([string]$text) {
    $text = $text.Replace("`r`n", "`n").Replace("`r", "`n")
    if ($text.Length -eq 0) { return $text }
    $lines = [Collections.Generic.List[string]]::new([string[]][regex]::Split($text, '[\n\x0B\f\x1C\x1D\x1E\x85\u2028\u2029]'))
    if ($lines[$lines.Count - 1] -eq '') { $lines.RemoveAt($lines.Count - 1) }   # splitlines: no empty last line
    $kept = @($lines | Where-Object { -not ([regex]::IsMatch($_, $KeyringNoise) -and $_.IndexOfAny([char[]]'{}[]') -lt 0) })
    return ($kept -join "`n")
}

function Get-CanaryLevel($element) {
    # One object level as an ordinal (case-sensitive) map, or $null: duplicate key, a known key in another
    # case, `ok` present but not true, or `error` present and not null/false/"" make the answer ambiguous.
    if ($element.ValueKind -ne [Text.Json.JsonValueKind]::Object) { return $null }
    $props = [Collections.Generic.Dictionary[string, Text.Json.JsonElement]]::new([StringComparer]::Ordinal)
    foreach ($property in $element.EnumerateObject()) {
        if ($props.ContainsKey($property.Name)) { return $null }
        if ($CanaryKnownKeys -contains $property.Name -and $CanaryKnownKeys -cnotcontains $property.Name) { return $null }
        $props[$property.Name] = $property.Value
    }
    if ($props.ContainsKey('ok') -and $props['ok'].ValueKind -ne [Text.Json.JsonValueKind]::True) { return $null }
    if ($props.ContainsKey('error')) {
        $e = $props['error']
        $empty = $e.ValueKind -in @([Text.Json.JsonValueKind]::Null, [Text.Json.JsonValueKind]::False) -or
            ($e.ValueKind -eq [Text.Json.JsonValueKind]::String -and $e.GetString() -eq '')
        if (-not $empty) { return $null }
    }
    return ,$props
}

function Test-JsonStrictTree($root) {
    # WP714 round 3: the same document contract as tl_gws._nlm_canary_json_strict, over the WHOLE tree, not
    # only the levels the notebook rule reads. Parse already rejects NaN/Infinity, comments, trailing commas,
    # raw control characters, a leading BOM in the string and nesting deeper than 64 (measured, pwsh 7.4.6).
    # It does NOT reject: a duplicate key in nested metadata, a lone escaped surrogate (only reading the
    # string throws) or a number that overflows double (TryGetDouble returns true with +/-Infinity).
    $stack = [Collections.Generic.Stack[Text.Json.JsonElement]]::new()
    $stack.Push($root)
    while ($stack.Count -gt 0) {
        $element = $stack.Pop()
        switch ($element.ValueKind) {
            ([Text.Json.JsonValueKind]::Object) {
                $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
                foreach ($property in $element.EnumerateObject()) {
                    if (-not $seen.Add($property.Name)) { return $false }
                    $stack.Push($property.Value)
                }
            }
            ([Text.Json.JsonValueKind]::Array) { foreach ($item in $element.EnumerateArray()) { $stack.Push($item) } }
            ([Text.Json.JsonValueKind]::String) { [void]$element.GetString() }
            ([Text.Json.JsonValueKind]::Number) {
                $number = 0.0
                if (-not $element.TryGetDouble([ref]$number) -or -not [double]::IsFinite($number)) { return $false }
            }
        }
    }
    return $true
}

function Test-CanaryBody([string]$text, [string]$notebook) {
    # Allow-list, same rules as tl_gws._nlm_canary_body_ok: exactly ONE notebook object; every id key
    # present is a string equal to the trusted id; every title/name present is a non-blank string.
    # System.Text.Json keeps JSON types and sees duplicate keys (ConvertFrom-Json keeps the last one silently
    # and turns date-like strings into DateTime). Any exception while reading (a lone surrogate in a property
    # name or string throws) is a negative answer, never a positive one.
    try { $doc = [Text.Json.JsonDocument]::Parse($text) } catch { return $false }
    try {
        if (-not (Test-JsonStrictTree $doc.RootElement)) { return $false }
        $node = $doc.RootElement
        if ($node.ValueKind -eq [Text.Json.JsonValueKind]::Array) {
            if ($node.GetArrayLength() -ne 1) { return $false }
            $node = $node[0]
        }
        $props = Get-CanaryLevel $node
        if ($null -eq $props) { return $false }
        if (-not $props.ContainsKey('id') -and -not $props.ContainsKey('notebook_id') -and $props.ContainsKey('data')) {
            $props = Get-CanaryLevel $props['data']
            if ($null -eq $props) { return $false }
        }
        $ids = @(@('id', 'notebook_id') | Where-Object { $props.ContainsKey($_) })
        if ($ids.Count -eq 0) { return $false }
        foreach ($key in $ids) {
            $value = $props[$key]
            if ($value.ValueKind -ne [Text.Json.JsonValueKind]::String -or $value.GetString() -cne $notebook) { return $false }
        }
        $titles = @(@('title', 'name') | Where-Object { $props.ContainsKey($_) })
        if ($titles.Count -eq 0) { return $false }
        foreach ($key in $titles) {
            $value = $props[$key]
            if ($value.ValueKind -ne [Text.Json.JsonValueKind]::String -or (Test-CanaryBlank $value.GetString())) { return $false }
        }
        return $true
    } catch { return $false } finally { $doc.Dispose() }
}

function Exit-IfBlocked($result, [string]$step = '') {
    # WP710 g4: a step whose tree is not contained, or not proven gone, ends the run before any later step.
    # g5: `inconclusive` promises zero stage calls. When the STAGE command itself ran (`ran`) and only its tree
    # is unproven, the upload may have happened: that is a stage_failure (rc 6), with the reason kept.
    if (-not $result.blocked) { return }
    $Evidence.containment_reason = [string]$result.blocked
    if ($step -eq 'stage' -and $result.ran) {
        Emit 'stage_failure' 'stage' -1 $result.elapsed
        exit 6
    }
    Emit 'inconclusive' 'tree_containment' -1 $result.elapsed
    exit 5
}

function Classify([string]$message) {
    # Bare words are not evidence: `nlm auth refresh`, `nlm login` and .../nlm/auth/refresh.py all
    # contain auth words. Only anchored failure phrases count (allow-list); a mixed or unknown signal
    # stays inconclusive. Any non-zero rc still makes zero stage calls whatever the label.
    $auth = $message -match '(?i)\bauth(?:entication)?\s+(?:has\s+)?(?:expired|failed|required|invalid)\b|\bunauthori[sz]ed\b|\bHTTP\s*40[13]\b|\b40[13]\s+(?:Unauthorized|Forbidden)\b|\bClientAuthenticationError\b|\b(?:session|cookies?)\s+(?:has\s+|have\s+)?(?:expired|invalid)\b'
    $network = $message -match '(?i)\bnetwork\s+(?:failure|error|(?:is\s+)?unreachable)\b|\bconnection\s+(?:reset|refused|aborted|timed\s+out)\b|\bname\s+resolution\b|\bgetaddrinfo\b|\bno\s+route\s+to\s+host\b|\bHTTP\s*50[234]\b|\b50[234]\s+(?:Bad\s+Gateway|Service\s+Unavailable|Gateway\s+Time-?out)\b|\bConnectionError\b'
    if ($auth -and -not $network) { return 'auth_failure' }
    if ($network -and -not $auth) { return 'network_failure' }
    return 'inconclusive'
}

$mutex = $null
$held = $false
try {
    if ($TimeoutSeconds -lt 1 -or $LockWaitSeconds -lt 0 -or $IntervalSeconds -lt 1 -or $MaxCycles -lt 1 -or
        $UnconfirmedQuarantineSeconds -lt 1) {
        throw 'invalid bounded timing parameters'
    }
    if ($OperatorReleaseReason -and $OperatorReleaseReason -cnotmatch '^[^\p{C}]{8,200}$') { throw 'invalid operator release reason' }
    $configFull = [IO.Path]::GetFullPath($ConfigPath)
    $config = [string](Get-Content -LiteralPath $configFull -Raw) | ConvertFrom-Json
    $notebook = [string]$config.notebook_id
    $browserProfile = [string]$config.browser_profile_path
    if ($notebook -cnotmatch '^[A-Za-z0-9_-]{8,128}$') { throw 'trusted config lacks valid notebook_id' }
    if (-not $browserProfile -or -not (Test-Path -LiteralPath $browserProfile -PathType Container)) { throw 'original browser profile missing' }
    $profileFull = [IO.Path]::GetFullPath($browserProfile)
    $digest = [Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($profileFull.ToLowerInvariant()))
    $Evidence.profile_fingerprint = [Convert]::ToHexString($digest).Substring(0, 16)
    # Resolve to a real application path: a bare name does not find a .cmd shim through Process.Start.
    $nlmPath = (Get-Command -Name $NlmCommand -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    $stagePath = (Get-Command -Name $StageCommand -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    $deadline = [DateTime]::UtcNow.AddSeconds($LockWaitSeconds)
    # One lock for every config on this interactive host, including distinct config paths.
    $mutex = [Threading.Mutex]::new($false, 'Global\tra_luat_nlm_credential_refresh')
    try { $held = $mutex.WaitOne([TimeSpan]::FromSeconds($LockWaitSeconds)) }
    catch [Threading.AbandonedMutexException] { $held = $true } # The OS reports the prior owner process ended.
    if (-not $held) { Emit 'inconclusive' 'lock_busy' -1 0; exit 5 }
    # The owner process ending does not end its child: wait for a recorded operation first.
    while ($true) {
        $verdict = Get-RecordVerdict
        if ($verdict.State -eq 'clear') { break }
        if ($verdict.State -eq 'released') {
            $Evidence.takeover = 'quarantine_elapsed'; $Evidence.takeover_reason = $verdict.Reason
            break
        }
        if ($verdict.State -eq 'quarantine' -and $OperatorReleaseReason) {
            # Manual exit: never for a tree proven alive (State alive), and always on the record.
            $Evidence.takeover = 'operator_release'; $Evidence.takeover_reason = $verdict.Reason
            $Evidence.operator_reason = $OperatorReleaseReason
            break
        }
        if ([DateTime]::UtcNow -ge $deadline) {
            $Evidence.takeover_reason = $verdict.Reason
            Emit 'inconclusive' $(if ($verdict.State -eq 'quarantine') { 'tree_quarantine' } else { 'lock_busy' }) -1 0
            exit 5
        }
        Start-Sleep -Milliseconds 200
    }
    Remove-Item -LiteralPath $OperationRecord -ErrorAction SilentlyContinue
    $versionResult = Invoke-Bounded $nlmPath ($NlmArgumentsPrefix + @('--version')) $TimeoutSeconds
    Write-Step 'version' $versionResult
    Exit-IfBlocked $versionResult
    # WP714 round 3: the version probe is an operation like any other. A tree it left unconfirmed keeps the
    # record; starting the refresh would overwrite that record and overlap the old tree.
    if ($versionResult.timeout -and -not $versionResult.exited) { Emit 'timeout' 'version' -1 $versionResult.elapsed; exit 3 }
    $versionMatch = [regex]::Match($versionResult.out, '\b\d+\.\d+(?:\.\d+)?\b')
    $Evidence.cli_version = if ($versionResult.rc -eq 0 -and -not $versionResult.timeout -and $versionMatch.Success) {
        $versionMatch.Value
    } else { 'unavailable' }
    for ($cycle=0; $cycle -lt $MaxCycles; $cycle++) {
        # The lock is held through the keepalive interval as well: a manual run then sees lock_busy.
        if ($cycle -gt 0) { Start-Sleep -Seconds $IntervalSeconds }
        $Evidence.cycle = $cycle + 1
        foreach ($name in @('refresh', 'canary', 'stage')) { [void]$Evidence.steps.Remove($name) }
        $refresh = Invoke-Bounded $nlmPath ($NlmArgumentsPrefix + @('auth','refresh')) $TimeoutSeconds
        Write-Step 'refresh' $refresh
        Exit-IfBlocked $refresh
        if ($refresh.timeout) { Emit 'timeout' 'refresh' -1 $refresh.elapsed; exit 3 }
        if ($refresh.rc -ne 0) {
            Emit (Classify ($refresh.err + ' ' + $refresh.out)) 'refresh' $refresh.rc $refresh.elapsed
            exit 2
        }
        $canary = Invoke-Bounded $nlmPath ($NlmArgumentsPrefix + @('notebook','get',$notebook,'-j')) $TimeoutSeconds
        Write-Step 'canary' $canary
        Exit-IfBlocked $canary
        if ($canary.timeout) { Emit 'timeout' 'canary' -1 $canary.elapsed; exit 3 }
        if ($canary.rc -ne 0) {
            Emit (Classify ($canary.err + ' ' + $canary.out)) 'canary' $canary.rc $canary.elapsed
            exit 2
        }
        if (-not (Test-CanaryBody (ConvertTo-StageText $canary.out) $notebook)) {
            Emit 'inconclusive' 'canary' $canary.rc $canary.elapsed
            exit 4
        }
        # The stage command repeats its own canary; give it the same trusted notebook. TL_CANARY_NOTEBOOK_ID
        # is the pin: a profile config loaded by the stage command rewrites TL_NOTEBOOK_ID, never this one.
        $pin = @{ TL_NOTEBOOK_ID = $notebook; TL_CANARY_NOTEBOOK_ID = $notebook }
        try { $stage = Invoke-Bounded $stagePath $StageArguments $TimeoutSeconds $pin }
        catch { Emit 'stage_failure' 'stage' -1 0; exit 6 }
        Write-Step 'stage' $stage
        Exit-IfBlocked $stage 'stage'
        if ($stage.timeout -or $stage.rc -ne 0) {
            Emit 'stage_failure' 'stage' $stage.rc $stage.elapsed
            exit 6
        }
        Emit 'staged' 'stage' $stage.rc $stage.elapsed
        if (-not $EnableKeepalive) { break }
    }
} catch {
    Emit 'inconclusive' 'preflight' -1 0
    exit 4
} finally {
    if ($held) { $mutex.ReleaseMutex() }
    if ($mutex) { $mutex.Dispose() }
}
