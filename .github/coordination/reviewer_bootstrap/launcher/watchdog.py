"""Controller-owned watchdog and process fence (Issue 125 §6).

Timeout and fencing authority live in the parent.  The Reviewer child cannot extend, disable or
acknowledge away its deadline, and nothing it writes counts as liveness: a child that prints
``heartbeat`` and then hangs forever is *more* dangerous than one that prints nothing, because the
first one talks a cooperative watchdog out of firing.  So this module never reads the child's
output to decide whether the child is alive.

Three mechanisms carry the section.

**Containment before the first descendant.**  On Windows the child is created suspended, assigned to
a Job Object, and only then resumed.  Assigning after an ordinary create leaves a window in which
the child can spawn a descendant that the job never owns — small, but "small" is not a property a
fence gets to have.  ``JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`` means the tree also dies if the
controller itself dies, which is the detached-descendant case the contract names.

**Identity, not just a number.**  A PID is reused.  Every process this module may terminate is
recorded as (pid, creation time), and the pair is re-checked immediately before the kill.  A
mismatch is a refusal, not a best-effort kill: fencing the wrong process is worse than failing to
fence, because it is a fence that reports success.

**Verification by a second, independent path.**  After terminating, the module asks the Job Object
how many processes are still active *and* enumerates the live process table to confirm no recorded
descendant survives.  Only when both agree does it mint a cleanup receipt.  When it cannot prove
cleanup it returns a red receipt and raises; §6 forbids a green completion receipt in that case, and
an unproven cleanup is exactly the state that looks green to everyone downstream.

The POSIX path is the session/process-group equivalent and is kept for the delegated Linux runner;
Windows remains the primary platform.
"""

from __future__ import annotations

import ctypes
import dataclasses
import datetime
import os
import signal
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence

from .errors import reject

IS_WINDOWS = os.name == "nt"

# --------------------------------------------------------------------------- Windows declarations

if IS_WINDOWS:  # pragma: no cover - exercised on the primary platform only
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    PROCESS_TERMINATE = 0x0001
    # AssignProcessToJobObject needs PROCESS_SET_QUOTA in addition to PROCESS_TERMINATE; omitting it
    # fails with ACCESS_DENIED at assignment time rather than at open time.
    PROCESS_SET_QUOTA = 0x0100
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    THREAD_SUSPEND_RESUME = 0x0002
    TH32CS_SNAPPROCESS = 0x00000002
    TH32CS_SNAPTHREAD = 0x00000004
    CREATE_SUSPENDED = 0x00000004
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    JobObjectBasicAccountingInformation = 1
    JobObjectExtendedLimitInformation = 9
    STILL_ACTIVE = 259

    class _FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

        def value(self) -> int:
            return (self.dwHighDateTime << 32) | self.dwLowDateTime

    class _PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.WCHAR * 260),
        ]

    class _THREADENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ThreadID", wintypes.DWORD),
            ("th32OwnerProcessID", wintypes.DWORD),
            ("tpBasePri", ctypes.c_long),
            ("tpDeltaPri", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
        ]

    class _IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_ulonglong),
            ("WriteOperationCount", ctypes.c_ulonglong),
            ("OtherOperationCount", ctypes.c_ulonglong),
            ("ReadTransferCount", ctypes.c_ulonglong),
            ("WriteTransferCount", ctypes.c_ulonglong),
            ("OtherTransferCount", ctypes.c_ulonglong),
        ]

    class _JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.POINTER(ctypes.c_ulong)),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class _JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", _IO_COUNTERS),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    class _JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("TotalUserTime", ctypes.c_longlong),
            ("TotalKernelTime", ctypes.c_longlong),
            ("ThisPeriodTotalUserTime", ctypes.c_longlong),
            ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
            ("TotalPageFaultCount", wintypes.DWORD),
            ("TotalProcesses", wintypes.DWORD),
            ("ActiveProcesses", wintypes.DWORD),
            ("TotalTerminatedProcesses", wintypes.DWORD),
        ]

    # Prototypes are declared, never defaulted.  ctypes assumes ``c_int`` for an undeclared return
    # value, so on 64-bit Windows an undeclared ``HANDLE`` is silently truncated to its low 32 bits.
    # The truncated value is usually still non-zero, so the failure does not look like a failure: the
    # code proceeds to call ``AssignProcessToJobObject`` on a handle that is not the job, gets a
    # plausible error, and the fence quietly stops fencing.  A watchdog that fails this way reports
    # success, which is the one outcome §6 refuses to allow.
    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    _kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    ]
    _kernel32.SetInformationJobObject.restype = wintypes.BOOL
    _kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    _kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    _kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    _kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.TerminateJobObject.restype = wintypes.BOOL
    _kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenThread.restype = wintypes.HANDLE
    _kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
    _kernel32.ResumeThread.restype = wintypes.DWORD
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.GetProcessTimes.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_FILETIME),
        ctypes.POINTER(_FILETIME),
        ctypes.POINTER(_FILETIME),
        ctypes.POINTER(_FILETIME),
    ]
    _kernel32.GetProcessTimes.restype = wintypes.BOOL
    _kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    _kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W)]
    _kernel32.Process32FirstW.restype = wintypes.BOOL
    _kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W)]
    _kernel32.Process32NextW.restype = wintypes.BOOL
    _kernel32.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(_THREADENTRY32)]
    _kernel32.Thread32First.restype = wintypes.BOOL
    _kernel32.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(_THREADENTRY32)]
    _kernel32.Thread32Next.restype = wintypes.BOOL
    _kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _kernel32.WaitForSingleObject.restype = wintypes.DWORD
    _kernel32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.TerminateProcess.restype = wintypes.BOOL

    WAIT_OBJECT_0 = 0x00000000


# --------------------------------------------------------------------------- process identity


@dataclasses.dataclass(frozen=True)
class ProcessIdentity:
    """A process named by more than its number.

    ``created`` is the OS creation stamp: FILETIME ticks on Windows, ``starttime`` jiffies from
    ``/proc/<pid>/stat`` on Linux.  Two processes can share a pid across time; they cannot share a
    pid *and* a creation stamp.
    """

    pid: int
    created: int

    def as_dict(self) -> dict[str, int]:
        return {"pid": self.pid, "created": self.created}


def _windows_creation_stamp(pid: int) -> int | None:
    handle = _kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return None
    try:
        creation = _FILETIME()
        exit_time = _FILETIME()
        kernel = _FILETIME()
        user = _FILETIME()
        ok = _kernel32.GetProcessTimes(
            handle,
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel),
            ctypes.byref(user),
        )
        if not ok:
            return None
        return creation.value()
    finally:
        _kernel32.CloseHandle(handle)


def _posix_creation_stamp(pid: int) -> int | None:
    try:
        with open("/proc/%d/stat" % pid, "rb") as handle:
            raw = handle.read()
    except OSError:
        return None
    # The executable name is parenthesised and may itself contain spaces and parentheses, so the
    # fields after it are found from the *last* ')' rather than by splitting the whole line.
    close = raw.rfind(b")")
    if close < 0:
        return None
    fields = raw[close + 2 :].split()
    if len(fields) < 20:
        return None
    try:
        return int(fields[19])
    except ValueError:
        return None


def creation_stamp(pid: int) -> int | None:
    """The OS creation stamp for ``pid``, or ``None`` when the process is gone or opaque."""
    if IS_WINDOWS:
        return _windows_creation_stamp(pid)
    return _posix_creation_stamp(pid)


def identify(pid: int) -> ProcessIdentity | None:
    stamp = creation_stamp(pid)
    if stamp is None:
        return None
    return ProcessIdentity(pid=pid, created=stamp)


def _windows_has_exited(pid: int) -> bool:
    """True when the process object is signalled, i.e. the process has run down.

    A terminated Windows process keeps answering ``GetProcessTimes`` for as long as anybody holds a
    handle to it — and the supervisor itself holds one through ``Popen``.  So "creation stamp still
    readable" is not "still running", and a cleanup proof built on that alone reports a survivor
    that is really a corpse.  ``WaitForSingleObject(handle, 0)`` answers the question that was
    actually asked, and unlike ``GetExitCodeProcess`` it cannot be confused by a child that
    legitimately exits with 259 (``STILL_ACTIVE``).
    """
    handle = _kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | 0x00100000, False, pid)
    if not handle:
        return True
    try:
        return _kernel32.WaitForSingleObject(handle, 0) == WAIT_OBJECT_0
    finally:
        _kernel32.CloseHandle(handle)


def _posix_is_zombie(pid: int) -> bool:
    try:
        with open("/proc/%d/stat" % pid, "rb") as handle:
            raw = handle.read()
    except OSError:
        return True
    close = raw.rfind(b")")
    if close < 0:
        return True
    fields = raw[close + 2 :].split()
    return bool(fields) and fields[0] == b"Z"


def is_alive(identity_value: ProcessIdentity) -> bool:
    """Alive *and still the same process*, and not merely a reaped corpse.

    A bare ``os.kill(pid, 0)`` answers only the first half, which is how a cleanup check reports a
    survivor that is actually an unrelated process that inherited the number.
    """
    current = creation_stamp(identity_value.pid)
    if current is None:
        return False
    if current != identity_value.created:
        return False
    if IS_WINDOWS:
        return not _windows_has_exited(identity_value.pid)
    return not _posix_is_zombie(identity_value.pid)


# --------------------------------------------------------------------------- deadline


@dataclasses.dataclass(frozen=True)
class Deadline:
    """A monotonic deadline that can never outlive the durable lease.

    Monotonic because wall-clock time moves: a laptop that sleeps for four hours mid-run, or an NTP
    correction, must not silently extend a fence.  Bounded by the lease because §6 makes the lease's
    absolute ``effective_stop_utc`` the ceiling, with no renewal and no grace.
    """

    monotonic_stop: float
    lease_stop_utc: str
    requested_seconds: float
    bounded_by_lease: bool

    def remaining(self) -> float:
        return max(0.0, self.monotonic_stop - time.monotonic())

    def expired(self) -> bool:
        return self.remaining() <= 0.0

    def as_dict(self) -> dict[str, object]:
        return {
            "requested_seconds": self.requested_seconds,
            "lease_effective_stop_utc": self.lease_stop_utc,
            "bounded_by_lease": self.bounded_by_lease,
        }


def parse_utc(value: str, label: str) -> datetime.datetime:
    if not isinstance(value, str) or not value:
        raise reject("lease_expired", "%s must be an ISO-8601 UTC timestamp" % label)
    text = value.replace("Z", "+00:00")
    try:
        parsed = datetime.datetime.fromisoformat(text)
    except ValueError as exc:
        raise reject("lease_expired", "%s is not a valid timestamp" % label) from exc
    if parsed.tzinfo is None:
        raise reject("lease_expired", "%s must carry an explicit UTC offset" % label)
    return parsed.astimezone(datetime.timezone.utc)


def build_deadline(
    requested_seconds: float,
    lease_effective_stop_utc: str,
    *,
    now_utc: datetime.datetime | None = None,
) -> Deadline:
    """Clamp the requested timeout to whatever the lease still allows."""
    if not isinstance(requested_seconds, (int, float)) or requested_seconds <= 0:
        raise reject("watchdog_identity", "the requested timeout must be a positive number")
    stop = parse_utc(lease_effective_stop_utc, "lease effective_stop_utc")
    now = now_utc or datetime.datetime.now(datetime.timezone.utc)
    lease_seconds = (stop - now).total_seconds()
    if lease_seconds <= 0:
        raise reject("lease_expired", "the lease has already reached its absolute stop")
    bounded = lease_seconds < float(requested_seconds)
    effective = min(float(requested_seconds), lease_seconds)
    return Deadline(
        monotonic_stop=time.monotonic() + effective,
        lease_stop_utc=lease_effective_stop_utc,
        requested_seconds=float(requested_seconds),
        bounded_by_lease=bounded,
    )


# --------------------------------------------------------------------------- process table


def live_pids() -> dict[int, int]:
    """A snapshot of ``pid -> parent pid`` for the whole machine."""
    if IS_WINDOWS:
        return _windows_live_pids()
    return _posix_live_pids()


def _windows_live_pids() -> dict[int, int]:
    snapshot = _kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if not snapshot or snapshot == _INVALID_HANDLE_VALUE:
        raise reject("watchdog_cleanup", "the process table could not be enumerated")
    try:
        entry = _PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(_PROCESSENTRY32W)
        table: dict[int, int] = {}
        if not _kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
            return table
        while True:
            table[int(entry.th32ProcessID)] = int(entry.th32ParentProcessID)
            if not _kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                break
        return table
    finally:
        _kernel32.CloseHandle(snapshot)


def _posix_live_pids() -> dict[int, int]:
    table: dict[int, int] = {}
    try:
        names = os.listdir("/proc")
    except OSError:
        return table
    for name in names:
        if not name.isdigit():
            continue
        pid = int(name)
        try:
            with open("/proc/%d/stat" % pid, "rb") as handle:
                raw = handle.read()
        except OSError:
            continue
        close = raw.rfind(b")")
        if close < 0:
            continue
        fields = raw[close + 2 :].split()
        if len(fields) < 2:
            continue
        try:
            table[pid] = int(fields[1])
        except ValueError:
            continue
    return table


def descendants_of(root_pid: int, table: Mapping[int, int] | None = None) -> list[int]:
    """Every live descendant of ``root_pid``, transitively.

    Used for *evidence*, not for killing: on Windows the Job Object does the killing, and a parent
    table cannot see a descendant that was reparented after its parent exited.  That blind spot is
    exactly why the job exists and why this function is not the fence.
    """
    snapshot = dict(table if table is not None else live_pids())
    children: dict[int, list[int]] = {}
    for pid, parent in snapshot.items():
        children.setdefault(parent, []).append(pid)
    found: list[int] = []
    stack = list(children.get(root_pid, ()))
    seen = set()
    while stack:
        pid = stack.pop()
        if pid in seen or pid == root_pid:
            continue
        seen.add(pid)
        found.append(pid)
        stack.extend(children.get(pid, ()))
    return sorted(found)


# --------------------------------------------------------------------------- the fence


class _RealGroupProbe:
    """The live process table, behind the same interface the controls use.

    Existing as an object rather than as three inline calls is what lets the group-identity logic be
    exercised with a supplied table — so the control runs on a platform with no process groups
    instead of being skipped there, which is the difference between a covered case and a declared one.
    """

    @staticmethod
    def pids() -> list[int]:
        return sorted(live_pids())

    @staticmethod
    def pgid(pid: int):
        try:
            return os.getpgid(pid)
        except (OSError, AttributeError):
            return None

    @staticmethod
    def session(pid: int):
        try:
            return os.getsid(pid)
        except (OSError, AttributeError):
            return None

    @staticmethod
    def created(pid: int):
        """The creation stamp, behind the same interface as pgid and session.

        WP125-RV-010-R5.  Creation identity has to travel with the rest of the group observation.
        Reading it out-of-band from the module function would mean the identity controls could only
        run where the pids under test are real, i.e. not on the platform this Packet runs on — and a
        control that cannot execute is a control that is not proving anything.
        """
        return creation_stamp(pid)


_real_group_probe = _RealGroupProbe()


class ProcessFence:
    """Owns one child process tree and can prove it is gone."""

    def __init__(self, label: str):
        self.label = label
        self._job = None
        self._assigned = False
        self.recorded: list[ProcessIdentity] = []
        # Evidence for WP125-RV-010: what was killed in the window before job adoption, and whether
        # each kill was proven rather than merely attempted.
        self.pre_adoption_cleanup: list[dict[str, object]] = []
        # The direct child handle, retained from creation. `OpenProcess` can fail — that is one of
        # the failures this window has to survive — and when it does, the handle the OS already gave
        # us at spawn time is the only way left to kill a suspended child. Popen owns it and cannot
        # lose it, so this is the terminator of last resort rather than a convenience.
        self._child = None

        # WP125-RV-010-R3.  POSIX identity for the *group*, kept independently of the root pid.
        # `os.getpgid(pid)` stops working the moment the root exits, which is precisely the case the
        # group exists to survive: root gone, descendants still in the group. Recording the pgid and
        # session at adoption means the fence can still name, signal and census the group afterwards.
        self.pgid: int | None = None
        self.session: int | None = None
        self.leader_pid: int | None = None
        self.leader_created: int | None = None
        # pid -> creation stamp observed at adoption. A pid alone cannot survive its own reuse, so
        # the members are retained by identity and not by number (WP125-RV-010-R5).
        self.adopted_members: dict[int, object] = {}

    def attach_child(self, child) -> None:
        self._child = child

    # -- POSIX group identity ---------------------------------------------
    def record_group_identity(self, pid: int) -> dict[str, object]:
        """Capture pgid/session while the root is still alive to be asked."""
        if IS_WINDOWS:
            return {"applicable": False, "reason": "windows_uses_job_object"}
        try:
            self.pgid = os.getpgid(pid)
        except OSError:
            self.pgid = None
        try:
            self.session = os.getsid(pid)
        except (OSError, AttributeError):
            self.session = None
        # WP125-RV-010-R5: the leader is named by its creation stamp as well as its number, and the
        # members present at adoption are retained.  A pgid is reused, and so is a pid; the creation
        # stamp is what makes "the leader we launched" a different claim from "whatever holds that
        # number now".
        self.leader_pid = pid
        self.leader_created = creation_stamp(pid)
        self.adopted_members = {
            member: _real_group_probe.created(member) for member in self.group_members()
        }
        # WP125-RV-010-R5.  An adoption observation that could not read what it needed is not an
        # adoption observation.  Round 5 stored `None` and carried on, so a fence that never learned
        # its own session went on to compare every later observation against nothing.
        captured = (
            self.pgid is not None
            and self.session is not None
            and self.leader_created is not None
            and all(value is not None for value in self.adopted_members.values())
        )
        return {
            "applicable": True,
            "captured": captured,
            "pgid": self.pgid,
            "session": self.session,
            "leader_pid": self.leader_pid,
            "leader_created": self.leader_created,
            "adopted_members": sorted(self.adopted_members),
            "adopted_member_identities": {
                str(member): stamp for member, stamp in sorted(self.adopted_members.items())
            },
            "captured_while_root_alive": True,
        }

    def group_members(self, probe=None) -> list[int]:
        """Live pids whose process group is ours, read from the process table, not from the root.

        ``probe`` exists so the identity logic can be exercised with a supplied table; it is the same
        code path either way, which keeps the control executable on a platform that has no process
        groups instead of skipping it.
        """
        if self.pgid is None:
            return []
        if probe is None:
            if IS_WINDOWS:
                return []
            probe = _real_group_probe
        members: list[int] = []
        for pid in probe.pids():
            if probe.pgid(pid) == self.pgid:
                members.append(pid)
        return sorted(members)

    def group_identity_is_intact(self, probe=None) -> dict[str, object]:
        """Refuse an ambiguous or drifted group before signalling or counting it.

        WP125-RV-010-R4.  Round 4 captured the session and never used it, and then signalled a bare
        numeric pgid.  A pgid is a small integer the kernel reuses, so "the group with that number"
        and "our group" are different claims — and killing the first while believing the second is
        how a fence terminates something it never launched.  The recorded session is the
        discriminator: our group's members belong to our session, and a recycled pgid's members do
        not.
        """
        if self.pgid is None:
            return {"applicable": True, "intact": False, "reason": "identity_never_captured"}
        if probe is None:
            if IS_WINDOWS:
                return {"applicable": False, "intact": True, "reason": "windows_uses_job_object"}
            probe = _real_group_probe

        # WP125-RV-010-R5.  If the leader is still alive it must still be *our* leader: same pid and
        # same creation stamp. A pid that has been recycled onto a different process is the case a
        # numeric comparison cannot see.
        if self.leader_pid is not None:
            current = probe.created(self.leader_pid)
            if current is not None and self.leader_created is not None and current != self.leader_created:
                return {
                    "applicable": True,
                    "intact": False,
                    "reason": "leader_pid_was_reused_by_a_different_process",
                    "recorded_leader": {"pid": self.leader_pid, "created": self.leader_created},
                    "observed_created": current,
                }
            if self.leader_created is None:
                return {
                    "applicable": True,
                    "intact": False,
                    "reason": "leader_creation_identity_was_never_readable",
                    "recorded_leader": {"pid": self.leader_pid, "created": None},
                }

        members = self.group_members(probe)
        if not members:
            return {"applicable": True, "intact": True, "reason": "group_empty", "members": []}

        sessions = {pid: probe.session(pid) for pid in members}
        # An unreadable session is not agreement. Round 5 skipped `None` before comparing, so a
        # member whose session could not be observed counted as one of ours — the fence would then
        # signal a group it had not actually identified. Unavailable is now fail-closed.
        unreadable = sorted(pid for pid, value in sessions.items() if value is None)
        if unreadable:
            return {
                "applicable": True,
                "intact": False,
                "reason": "member_session_could_not_be_observed",
                "members": members,
                "unreadable_members": unreadable,
            }
        foreign = {value for value in sessions.values() if value != self.session}
        if foreign:
            return {
                "applicable": True,
                "intact": False,
                "reason": "process_group_number_was_reused_by_another_session",
                "members": members,
                "recorded_session": self.session,
                "observed_sessions": sorted(str(value) for value in sessions.values()),
            }
        if self.session is None:
            return {
                "applicable": True,
                "intact": False,
                "reason": "recorded_session_identity_is_missing",
                "members": members,
            }

        # WP125-RV-010-R5.  Every member we adopted and can still see must still be the process we
        # adopted.  Session equality alone cannot see a member pid the kernel recycled *within* our
        # own session, which is the likeliest reuse of all on a busy machine — and an unreadable
        # stamp for a pid that is still listed as a member is an ambiguous observation, not an
        # agreement.
        for member, adopted_stamp in sorted(self.adopted_members.items()):
            if member not in members:
                continue
            now = probe.created(member)
            if now is None:
                return {
                    "applicable": True,
                    "intact": False,
                    "reason": "member_creation_identity_could_not_be_observed",
                    "members": members,
                    "member": member,
                }
            if adopted_stamp is not None and now != adopted_stamp:
                return {
                    "applicable": True,
                    "intact": False,
                    "reason": "member_pid_was_reused_by_a_different_process",
                    "members": members,
                    "member": member,
                }
        return {
            "applicable": True,
            "intact": True,
            "reason": "leader_creation_and_member_sessions_match_recorded_identity",
            "members": members,
            "recorded_session": self.session,
            "recorded_leader": {"pid": self.leader_pid, "created": self.leader_created},
            "adopted_members_revalidated": sorted(self.adopted_members),
        }

    def group_census(self) -> dict[str, object]:
        """Independent census of the POSIX process group.

        On Windows this is *not applicable* and says so.  A non-applicable answer is not proof of
        cleanup — it is the absence of a measurement — so :meth:`prove_cleanup` treats the two
        platforms' authorities separately rather than letting one stand in for the other.
        """
        if IS_WINDOWS:
            return {
                "applicable": False,
                "ok": True,
                "members": None,
                "reason": "windows_job_object_is_the_authority",
            }
        if self.pgid is None:
            return {
                "applicable": True,
                "ok": False,
                "members": None,
                "reason": "process_group_identity_was_never_captured",
            }
        identity = self.group_identity_is_intact()
        if not identity["intact"]:
            # An ambiguous group cannot be counted as ours, so it cannot be counted as empty either.
            return {
                "applicable": True,
                "ok": False,
                "members": identity.get("members"),
                "pgid": self.pgid,
                "reason": identity["reason"],
            }
        members = self.group_members()
        return {
            "applicable": True,
            "ok": True,
            "members": members,
            "empty": not members,
            "pgid": self.pgid,
            "session": self.session,
            "reason": "measured_for_the_recorded_identity",
        }

    def terminate_group(self, probe=None) -> dict[str, object]:
        """Kill the recorded process group — after proving it is still the group we recorded.

        A supplied ``probe`` drives the identity decision on any platform, so the refusal path is
        reachable where there are no real process groups.  Only the actual signal is POSIX-only.
        """
        if self.pgid is None or (IS_WINDOWS and probe is None):
            return {"applicable": not IS_WINDOWS, "signalled": False}
        identity = self.group_identity_is_intact(probe)
        if not identity["intact"]:
            # Never signal an ambiguous group. Declining to kill is recoverable; killing an unrelated
            # process that inherited the number is not.
            return {
                "applicable": True,
                "signalled": False,
                "pgid": self.pgid,
                "refused": identity["reason"],
            }
        if IS_WINDOWS:
            return {"applicable": False, "signalled": False, "identity_checked": True}
        try:
            os.killpg(self.pgid, signal.SIGKILL)
            return {"applicable": True, "signalled": True, "pgid": self.pgid}
        except OSError as exc:
            return {
                "applicable": True,
                "signalled": False,
                "pgid": self.pgid,
                "error": type(exc).__name__,
            }


    # -- containment ------------------------------------------------------
    def open(self) -> None:
        if not IS_WINDOWS:
            return
        job = _kernel32.CreateJobObjectW(None, None)
        if not job:
            raise reject("watchdog_cleanup", "a job object could not be created")
        info = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        ok = _kernel32.SetInformationJobObject(
            job,
            JobObjectExtendedLimitInformation,
            ctypes.byref(info),
            ctypes.sizeof(info),
        )
        if not ok:
            _kernel32.CloseHandle(job)
            raise reject("watchdog_cleanup", "the job object kill-on-close limit could not be set")
        self._job = job

    def creation_flags(self) -> int:
        """Flags the child must be created with for containment to be race-free."""
        if not IS_WINDOWS:
            return 0
        return CREATE_SUSPENDED | CREATE_NEW_PROCESS_GROUP

    def _abort_pre_adoption(self, handle, pid: int, reason: str) -> "LauncherRejected":
        """Kill a child that never reached the job, prove it is gone, and return the red rejection.

        WP125-RV-010.  Every failure between ``CreateProcess`` and a successful
        ``AssignProcessToJobObject`` used to raise straight out, leaving a child that was created
        **suspended** sitting in the process table forever.  The job could not clean it up — that is
        precisely what failed — and ``run_supervised``'s fallback terminates *the job*, which by then
        owns nothing.  So the one path that reported "containment failed" was also the one path that
        leaked a process.

        The direct handle is therefore opened before anything can fail and retained across the whole
        window, terminated unconditionally here, waited on, and then checked against the process
        table by identity.  The rejection names whether the child was proven gone, because "we tried
        to kill it" and "it is gone" are different claims and only the second one is cleanup.
        """
        # WP125-RV-010-R2.  Round 2 recorded `terminated: True` unconditionally — it recorded that a
        # kill had been *attempted*.  An attempted call is not an outcome, and a receipt that says
        # "terminated" because a function was entered is the same false green this finding is about.
        # Every field below is an observation: what the API returned, what the wait returned, and
        # what an independent census of the process table says afterwards.
        record: dict[str, object] = {
            "pid": pid,
            "reason": reason,
            "identified": False,
            "terminate_calls": [],
            "waited": False,
            "wait_signalled": None,
            "census_after": None,
            "terminated": False,
            "proven_gone": False,
        }
        identity_value = identify(pid)
        record["identified"] = identity_value is not None

        if IS_WINDOWS and handle:
            ok = bool(_kernel32.TerminateProcess(handle, 1))
            record["terminate_calls"].append({"via": "direct_handle", "returned_ok": ok})
            wait = _kernel32.WaitForSingleObject(handle, 5000)
            record["waited"] = True
            record["wait_signalled"] = wait == WAIT_OBJECT_0
        # The retained creation handle. When the failure being handled *is* `OpenProcess` returning
        # null there is no ctypes handle at all, and this is the only terminator left.
        if self._child is not None:
            try:
                self._child.kill()
                self._child.wait(timeout=5)
                record["terminate_calls"].append({"via": "creation_handle", "returned_ok": True})
                record["waited"] = True
                record["wait_signalled"] = True
            except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
                record["terminate_calls"].append(
                    {"via": "creation_handle", "returned_ok": False, "error": type(exc).__name__}
                )
        if not IS_WINDOWS:
            try:
                os.kill(pid, signal.SIGKILL)
                record["terminate_calls"].append({"via": "signal", "returned_ok": True})
            except OSError as exc:
                record["terminate_calls"].append(
                    {"via": "signal", "returned_ok": False, "error": type(exc).__name__}
                )

        record["terminated"] = any(
            call.get("returned_ok") for call in record["terminate_calls"]
        )

        # Independent census: the live process table, consulted after the wait, by identity.
        end = time.monotonic() + 5.0
        survivor = True
        while True:
            table = live_pids()
            present = pid in table
            still_same = identity_value is not None and is_alive(identity_value)
            survivor = still_same or (identity_value is None and present)
            if not survivor:
                break
            if time.monotonic() >= end:
                break
            time.sleep(0.02)
        record["census_after"] = {"pid_in_table": pid in live_pids(), "identity_alive": survivor}

        # Green only from observation, and only when every leg is observed. An unidentifiable child
        # cannot be proven gone even if the table happens not to list it, because there is nothing to
        # compare the table against.
        record["proven_gone"] = bool(
            record["identified"]
            and record["terminated"]
            and record["waited"]
            and not survivor
        )

        if IS_WINDOWS and handle:
            _kernel32.CloseHandle(handle)
        self.pre_adoption_cleanup.append(record)
        return reject(
            "watchdog_cleanup",
            "%s; pre-adoption child pid=%s identified=%s terminated=%s waited=%s proven_gone=%s"
            % (
                reason,
                pid,
                record["identified"],
                record["terminated"],
                record["waited"],
                record["proven_gone"],
            ),
        )

    def adopt(self, pid: int) -> ProcessIdentity:
        """Assign the still-suspended child to the job and record its identity."""
        handle = None
        if IS_WINDOWS:
            # Opened first, and with TERMINATE, so that every later failure in this window has a way
            # to kill the suspended child rather than only a way to complain about it.
            handle = _kernel32.OpenProcess(
                PROCESS_TERMINATE | PROCESS_SET_QUOTA | PROCESS_QUERY_LIMITED_INFORMATION,
                False,
                pid,
            )
            if not handle:
                raise self._abort_pre_adoption(
                    None, pid, "the child could not be opened for containment"
                )

        identity_value = identify(pid)
        if identity_value is None:
            raise self._abort_pre_adoption(
                handle, pid, "the child could not be identified after creation"
            )

        if IS_WINDOWS:
            if not _kernel32.AssignProcessToJobObject(self._job, handle):
                raise self._abort_pre_adoption(
                    handle, pid, "the child could not be assigned to the job"
                )
            _kernel32.CloseHandle(handle)
            self._assigned = True
        self.recorded.append(identity_value)
        # Capture the POSIX group identity while the root can still be asked for it.
        self.record_group_identity(pid)
        return identity_value

    def resume(self, pid: int) -> None:
        """Release the suspended child, after containment is already in force."""
        if not IS_WINDOWS:
            return
        snapshot = _kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
        if not snapshot or snapshot == _INVALID_HANDLE_VALUE:
            raise reject("watchdog_cleanup", "the thread table could not be enumerated")
        resumed = 0
        try:
            entry = _THREADENTRY32()
            entry.dwSize = ctypes.sizeof(_THREADENTRY32)
            if not _kernel32.Thread32First(snapshot, ctypes.byref(entry)):
                raise reject("watchdog_cleanup", "the child has no enumerable thread")
            while True:
                if int(entry.th32OwnerProcessID) == pid:
                    thread = _kernel32.OpenThread(THREAD_SUSPEND_RESUME, False, entry.th32ThreadID)
                    if thread:
                        try:
                            _kernel32.ResumeThread(thread)
                            resumed += 1
                        finally:
                            _kernel32.CloseHandle(thread)
                if not _kernel32.Thread32Next(snapshot, ctypes.byref(entry)):
                    break
        finally:
            _kernel32.CloseHandle(snapshot)
        if resumed == 0:
            raise reject("watchdog_cleanup", "the suspended child could not be resumed")

    # -- termination ------------------------------------------------------
    def terminate(self) -> dict[str, object]:
        """Kill the whole tree.  Returns what was attempted, not whether it worked."""
        attempted: list[dict[str, int]] = []
        table = live_pids()
        for identity_value in self.recorded:
            attempted.extend(
                {"pid": pid, "created": -1}
                for pid in descendants_of(identity_value.pid, table)
            )
        # Measured before the kill.  This is the only number that can show an *orphan* was
        # contained: once its parent has exited, a parent-table walk cannot find it, so the job's
        # own census is the sole witness that more than one process was inside the fence.
        active_before = self.active_process_count()
        group_result: dict[str, object] = {"applicable": not IS_WINDOWS, "signalled": False}
        if IS_WINDOWS and self._job is not None:
            _kernel32.TerminateJobObject(self._job, 1)
        else:
            # WP125-RV-010-R3: signal the *recorded* group, not `getpgid(root)`. Round 3 asked the
            # root for its group id at kill time, which fails with ESRCH exactly when the root has
            # already exited — the orphaned-group case. The identity was captured at adoption for
            # this reason, so it is still available now.
            group_result = self.terminate_group()
            for identity_value in self.recorded:
                if not is_alive(identity_value):
                    continue
                try:
                    os.kill(identity_value.pid, signal.SIGKILL)
                except OSError:
                    pass
        return {
            "group": group_result,
            "observed_descendants": attempted,
            "job_active_before_terminate": active_before,
            "mechanism": "job_object" if IS_WINDOWS else "killpg",
        }

    # -- proof ------------------------------------------------------------
    def job_census(self) -> dict[str, object]:
        """Ask the job how many processes it still owns, and say *why* if it cannot answer.

        WP125-RV-005.  Generation 1 collapsed three different states into ``None`` — "this is POSIX,
        there is no job", "the job handle is missing", and "the Win32 census call failed" — and then
        treated ``None`` as clean.  On Windows the last two are the states where the fence has
        stopped being able to see anything, which is precisely when a green receipt is most
        dangerous.  Returning a reason instead of ``None`` is what lets :meth:`prove_cleanup` call
        them red on Windows while still accepting the genuinely inapplicable POSIX case.
        """
        if not IS_WINDOWS:
            return {
                "applicable": False,
                "ok": True,
                "active": None,
                "reason": "posix_process_group_has_no_job_census",
            }
        if self._job is None:
            return {
                "applicable": True,
                "ok": False,
                "active": None,
                "reason": "job_handle_absent",
            }
        info = _JOBOBJECT_BASIC_ACCOUNTING_INFORMATION()
        returned = wintypes.DWORD(0)
        ok = _kernel32.QueryInformationJobObject(
            self._job,
            JobObjectBasicAccountingInformation,
            ctypes.byref(info),
            ctypes.sizeof(info),
            ctypes.byref(returned),
        )
        if not ok:
            return {
                "applicable": True,
                "ok": False,
                "active": None,
                "reason": "query_information_job_object_failed",
            }
        return {
            "applicable": True,
            "ok": True,
            "active": int(info.ActiveProcesses),
            "reason": "measured",
        }

    def active_process_count(self) -> int | None:
        """The job's live-process count, or ``None`` when the census could not answer.

        Kept for the pre-terminate observation, where an unavailable census is information rather
        than a verdict.  Cleanup proof must use :meth:`job_census` so it can tell the reasons apart.
        """
        census = self.job_census()
        return census["active"] if census["ok"] else None

    def prove_cleanup(self, *, budget_seconds: float = 10.0) -> dict[str, object]:
        """Two independent proofs that nothing survived.

        Raises when cleanup cannot be proven.  §6 is explicit that an unproven cleanup is red and
        must not mint a green completion receipt, so this refuses to return a receipt at all.
        """
        end = time.monotonic() + budget_seconds
        survivors: list[int] = []
        census: dict[str, object] = {}
        while True:
            table = live_pids()
            survivors = []
            for identity_value in self.recorded:
                if not is_alive(identity_value):
                    # The root is gone. Its former children are no longer attributable to it: a pid
                    # is reused the moment it is free, and `th32ParentProcessID` keeps pointing at the
                    # number, not at the process that owned it. Walking the parent table from a dead
                    # root therefore harvests *unrelated live processes* — measured here as ten of
                    # them, on a busy machine, while the Job Object census said zero active. Treating
                    # that as a survivor list turns a clean fence into an unprovable one, and the same
                    # noise would drown a real survivor. The job is the authority for the tree; the
                    # parent walk is only meaningful while the root it starts from is alive.
                    continue
                survivors.append(identity_value.pid)
                survivors.extend(descendants_of(identity_value.pid, table))
            census = self.job_census()
            group = self.group_census()
            table_clean = not survivors
            # WP125-RV-005.  On Windows a census that cannot answer is RED, not clean: a missing job
            # handle or a failed Win32 query means the fence has lost sight of the tree, and "I
            # cannot see any survivors" is not the same claim as "there are none".  Off Windows the
            # census is genuinely inapplicable, and that is recorded as such rather than silently
            # counted as a second proof.
            census_clean = bool(census["ok"]) and (
                census["active"] == 0 if census["applicable"] else True
            )
            # WP125-RV-010-R3: on POSIX the group census is the second authority, and it must be a
            # real measurement showing an empty group. A Windows "not applicable" answer proves
            # nothing about a POSIX group and is never allowed to stand in for one; each platform's
            # second path is its own.
            group_clean = (
                (bool(group["ok"]) and bool(group.get("empty")))
                if group["applicable"]
                else True
            )
            if table_clean and census_clean and group_clean:
                paths = 2 if (census["applicable"] or group["applicable"]) else 1
                return {
                    "cleanup_proven": True,
                    "process_table_survivors": [],
                    "recorded_identities": [item.as_dict() for item in self.recorded],
                    "job_census": census,
                    "group_census": group,
                    "job_active_processes": census["active"],
                    "independent_paths": paths,
                }
            if time.monotonic() >= end:
                break
            time.sleep(0.05)
        raise reject(
            "watchdog_cleanup",
            "cleanup could not be proven: %d table survivors, job census %s (active=%s), "
            "group census %s (members=%s)"
            % (
                len(set(survivors)),
                census.get("reason"),
                census.get("active"),
                group.get("reason"),
                group.get("members"),
            ),
        )

    def close(self) -> None:
        if IS_WINDOWS and self._job is not None:
            _kernel32.CloseHandle(self._job)
            self._job = None

    def __enter__(self) -> "ProcessFence":
        self.open()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


# --------------------------------------------------------------------------- supervised run


@dataclasses.dataclass(frozen=True)
class RunOutcome:
    """What actually happened, in the controller's words rather than the child's."""

    status: str
    return_code: int | None
    fenced: bool
    identity: dict[str, int]
    deadline: dict[str, object]
    cleanup: dict[str, object]
    termination: dict[str, object]
    self_reported_markers: tuple[str, ...]
    # Bounded, decoded child output.  Deliberately absent from `as_dict`: the child may print
    # anything, and `as_dict` is what reaches the retained artifact set.  Callers that need the
    # text — the cases where the child's *own* report is the measurement, such as observing the
    # memory variable from inside it — read this field directly and extract only the field they
    # asked for.
    stdout_text: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "return_code": self.return_code,
            "fenced": self.fenced,
            "identity": self.identity,
            "deadline": self.deadline,
            "cleanup": self.cleanup,
            "termination": self.termination,
            "self_reported_markers": list(self.self_reported_markers),
            "self_report_used_as_liveness": False,
        }


# Markers a hostile child may print to talk a cooperative watchdog out of firing.  They are recorded
# as *evidence that the child lied*, and never consulted when deciding whether to fence.
FORGEABLE_MARKERS = ("READY", "HEARTBEAT", "DONE", "SUCCESS", "CLEANUP-COMPLETE")


def run_supervised(
    command: Sequence[str],
    *,
    environment: Mapping[str, str],
    working_directory: str,
    deadline: Deadline,
    label: str = "reviewer-child",
    poll_seconds: float = 0.02,
    output_ceiling: int = 64 * 1024,
) -> RunOutcome:
    """Spawn one contained child and supervise it to a controller-owned deadline.

    Output is drained into a bounded buffer so that a flooding child cannot fill a pipe, wedge
    itself on a blocked write and thereby make a naive supervisor wait forever — but the drained
    text is never used to decide liveness.
    """
    with ProcessFence(label) as fence:
        popen_kwargs: dict[str, object] = {
            "cwd": working_directory,
            "env": dict(environment),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
            "stdin": subprocess.DEVNULL,
        }
        if IS_WINDOWS:
            popen_kwargs["creationflags"] = fence.creation_flags()
        else:
            popen_kwargs["start_new_session"] = True

        child = subprocess.Popen(list(command), **popen_kwargs)  # noqa: S603 - vector is structured
        fence.attach_child(child)
        try:
            identity_value = fence.adopt(child.pid)
            fence.resume(child.pid)

            collected = bytearray()
            status = "completed"
            fenced = False
            reader = _start_drain(child, collected, output_ceiling)

            while True:
                code = child.poll()
                if code is not None:
                    break
                if deadline.expired():
                    status = "timeout"
                    fenced = True
                    break
                time.sleep(poll_seconds)

            # The tree is torn down on *every* path, not only on timeout.  Two reasons, both
            # learned the hard way here:
            #
            #   1. "The child exited" is not "the tree exited".  A descendant that outlives its
            #      parent is exactly the case §6 names, and proving cleanup before tearing the tree
            #      down would report success while an orphan is still running — a green receipt over
            #      a live process.
            #   2. A descendant inherits the stdout write handle, so the pipe never reaches EOF
            #      while it lives.  The drain thread then blocks in `read` holding the buffer lock,
            #      and closing the stream from here deadlocks the supervisor against its own reader.
            #      Killing the tree first is what releases both.
            termination = fence.terminate()
            termination["reason"] = "deadline_fence" if fenced else "end_of_run_sweep"
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
            if reader is not None:
                reader.join(timeout=5)
            cleanup = fence.prove_cleanup()
            text = bytes(collected).decode("utf-8", "replace")
            markers = tuple(marker for marker in FORGEABLE_MARKERS if marker in text)
            return RunOutcome(
                status=status,
                return_code=child.returncode,
                fenced=fenced,
                identity=identity_value.as_dict(),
                deadline=deadline.as_dict(),
                cleanup=cleanup,
                termination=termination,
                self_reported_markers=markers,
                stdout_text=text,
            )
        finally:
            if child.poll() is None:
                fence.terminate()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
            if child.stdout is not None:
                # Closing can still contend with a drain thread that has not yet noticed EOF.  The
                # thread is a daemon and the tree is already dead by here, so a failure to close
                # cleanly is a resource detail, not a correctness one — and it must never mask the
                # outcome the caller is waiting for.
                try:
                    child.stdout.close()
                except (OSError, ValueError, RuntimeError):
                    pass


def _start_drain(child: subprocess.Popen, sink: bytearray, ceiling: int):
    """Drain the child's output on a daemon thread, bounded.

    Bounded because §6 names output flood as a way out of cleanup: an unbounded reader turns a
    hostile child's ``while true: print`` into the supervisor's own memory exhaustion.
    """
    import threading

    if child.stdout is None:
        return None

    def pump() -> None:
        stream = child.stdout
        if stream is None:
            return
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    return
                if len(sink) < ceiling:
                    sink.extend(chunk[: ceiling - len(sink)])
        except (OSError, ValueError):
            return

    thread = threading.Thread(target=pump, name="wp125-drain", daemon=True)
    thread.start()
    return thread


def python_executable() -> str:
    """The interpreter used for offline control children.

    Taken from ``sys.executable`` — the running interpreter — rather than discovered on ``PATH``.
    Discovery is what §4.1 forbids, and a control that discovers its own helper undermines the rule
    it is meant to demonstrate.
    """
    if not sys.executable:
        raise reject("argument_vector", "the running interpreter has no resolvable path")
    return sys.executable
