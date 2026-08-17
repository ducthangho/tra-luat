# -*- coding: utf-8 -*-
"""Run one gate with exact-identity evidence and a per-host heavy-gate lock.

This is the pre-selector seam from ADR-0035.  It deliberately does not decide
which tests are affected.  Callers choose targeted commands; promotion callers
may reuse a successful full-gate record only after ``validate`` accepts every
identity field they require.
"""

from __future__ import annotations

import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterator


SCHEMA_VERSION = 2
EXIT_PREFLIGHT = 2
EXIT_NOT_REUSABLE = 3
EXIT_BUSY = 75
EXIT_TIMEOUT = 124
# 128 + SIGINT(2), quy ước shell cho "bị ngắt". Tách khỏi `EXIT_TIMEOUT` vì hai
# chuyện khác nhau: quá hạn là gate tự quyết, ngắt là người gõ Ctrl-C.
EXIT_INTERRUPTED = 130
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_CATALOG_POLICY_PATHS = (
    ".claude/dev/gate_lifecycle.py",
    ".github/workflows/ci.yml",
    "docs/PROTOCOL_DA_PHIEN.md",
    "docs/adr/0035-dieu-phoi-ben-vung-va-selftest-phan-tang.md",
    "scripts/tl_selftest.py",
    "scripts/test_fragments",
    "scripts/tl_test_fragments_bundled.py",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, raw_temp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    temp = Path(raw_temp)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(_json_bytes(payload))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            temp.unlink()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _positive_match(path: Path, pattern: str) -> str | None:
    compiled = re.compile(pattern)
    text = path.read_text(encoding="utf-8", errors="replace")
    match = compiled.search(text)
    return match.group(0)[-500:] if match else None


def _first_failure(path: Path, returncode: int) -> str | None:
    if returncode == 0:
        return None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    failure = re.compile(r'(?i)(?:\bFAIL(?:ED|URE)?\b|\bERROR\b|\bHONG\b|Traceback|"ok"\s*:\s*false)')
    for line in lines:
        if failure.search(line):
            return line[-1000:]
    for line in reversed(lines):
        if line.strip():
            return line[-1000:]
    return "process exited without output"


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "git failed"
        raise ValueError(detail)
    return proc.stdout.strip()


def _repo_identity(repo_arg: str | Path) -> tuple[Path, dict[str, Any]]:
    requested = Path(repo_arg).resolve()
    root = Path(_git(requested, "rev-parse", "--show-toplevel")).resolve()
    head = _git(root, "rev-parse", "HEAD")
    tree = _git(root, "rev-parse", "HEAD^{tree}")
    tracked_dirty = _git(root, "status", "--porcelain=v1", "--untracked-files=no")
    worktree_dirty = _git(root, "status", "--porcelain=v1", "--untracked-files=normal")
    catalog_policy = _git(root, "ls-files", "-s", "--", *_CATALOG_POLICY_PATHS)
    return root, {
        "head_sha": head,
        "tree_sha": tree,
        "tracked_clean": not bool(tracked_dirty),
        "worktree_clean": not bool(worktree_dirty),
        "runner_sha256": _sha256_bytes(Path(__file__).read_bytes()),
        "system": platform.system(),
        "system_release": platform.release(),
        "machine": platform.machine(),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "catalog_policy_sha256": _sha256_bytes(catalog_policy.encode("utf-8")),
    }


def _lock_path() -> Path:
    folder = Path(tempfile.gettempdir()) / "tra-luat-heavy-gates"
    return folder / "heavy-gate-v1.lock"


class _HeavyGateLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.stream: Any = None

    def _try_lock(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.stream is None:
            self.stream = self.path.open("a+b")
            self.stream.seek(0, os.SEEK_END)
            if self.stream.tell() == 0:
                self.stream.write(b"\0")
                self.stream.flush()
        self.stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False

    def acquire(self, wait_seconds: float) -> bool:
        deadline = time.monotonic() + max(0.0, wait_seconds)
        while True:
            if self._try_lock():
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(min(0.1, max(0.0, deadline - time.monotonic())))

    def release(self) -> None:
        if self.stream is None:
            return
        try:
            self.stream.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self.stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.stream.fileno(), fcntl.LOCK_UN)
        finally:
            self.stream.close()
            self.stream = None


class _WindowsJob:
    """Own a Windows Job Object whose close terminates the entire child tree."""

    def __init__(self, handle: Any, kernel32: Any) -> None:
        self.handle = handle
        self.kernel32 = kernel32

    @classmethod
    def attach(cls, proc: subprocess.Popen[Any]) -> _WindowsJob | None:
        if os.name != "nt":
            return None
        import ctypes
        from ctypes import wintypes

        class BasicLimit(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD),
            ]

        class IoCounters(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_ulonglong),
                ("WriteOperationCount", ctypes.c_ulonglong),
                ("OtherOperationCount", ctypes.c_ulonglong),
                ("ReadTransferCount", ctypes.c_ulonglong),
                ("WriteTransferCount", ctypes.c_ulonglong),
                ("OtherTransferCount", ctypes.c_ulonglong),
            ]

        class ExtendedLimit(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", BasicLimit),
                ("IoInfo", IoCounters),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        kernel32.CreateJobObjectW.restype = wintypes.HANDLE
        kernel32.SetInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        kernel32.SetInformationJobObject.restype = wintypes.BOOL
        kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL

        handle = kernel32.CreateJobObjectW(None, None)
        if not handle:
            return None
        info = ExtendedLimit()
        info.BasicLimitInformation.LimitFlags = 0x00002000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        configured = kernel32.SetInformationJobObject(handle, 9, ctypes.byref(info), ctypes.sizeof(info))
        assigned = configured and kernel32.AssignProcessToJobObject(handle, int(proc._handle))
        if not assigned:
            kernel32.CloseHandle(handle)
            return None
        return cls(handle, kernel32)

    def close(self) -> None:
        if self.handle is None:
            return
        self.kernel32.CloseHandle(self.handle)
        self.handle = None


def _resume_windows_process(proc: subprocess.Popen[Any]) -> None:
    """Resume the sole main thread of a process created with CREATE_SUSPENDED."""
    if os.name != "nt":
        return
    import ctypes
    from ctypes import wintypes

    class ThreadEntry(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ThreadID", wintypes.DWORD),
            ("th32OwnerProcessID", wintypes.DWORD),
            ("tpBasePri", wintypes.LONG),
            ("tpDeltaPri", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(ThreadEntry)]
    kernel32.Thread32First.restype = wintypes.BOOL
    kernel32.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(ThreadEntry)]
    kernel32.Thread32Next.restype = wintypes.BOOL
    kernel32.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenThread.restype = wintypes.HANDLE
    kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
    kernel32.ResumeThread.restype = wintypes.DWORD
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL

    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000004, 0)  # TH32CS_SNAPTHREAD
    invalid = ctypes.c_void_p(-1).value
    if not snapshot or snapshot == invalid:
        raise OSError(ctypes.get_last_error(), "cannot snapshot suspended process threads")
    entry = ThreadEntry()
    entry.dwSize = ctypes.sizeof(entry)
    try:
        more = bool(kernel32.Thread32First(snapshot, ctypes.byref(entry)))
        while more:
            if entry.th32OwnerProcessID == proc.pid:
                thread = kernel32.OpenThread(0x0002, False, entry.th32ThreadID)  # THREAD_SUSPEND_RESUME
                if not thread:
                    raise OSError(ctypes.get_last_error(), "cannot open suspended process thread")
                try:
                    previous = kernel32.ResumeThread(thread)
                    if previous == 0xFFFFFFFF:
                        raise OSError(ctypes.get_last_error(), "cannot resume gate process")
                    return
                finally:
                    kernel32.CloseHandle(thread)
            more = bool(kernel32.Thread32Next(snapshot, ctypes.byref(entry)))
    finally:
        kernel32.CloseHandle(snapshot)
    raise OSError("suspended gate process has no resumable thread")


@contextlib.contextmanager
def _maybe_heavy_lock(kind: str, root: Path, wait_seconds: float) -> Iterator[tuple[bool, str | None]]:
    if kind != "heavy":
        yield True, None
        return
    path = _lock_path()
    lock = _HeavyGateLock(path)
    acquired = lock.acquire(wait_seconds)
    try:
        yield acquired, str(path)
    finally:
        if acquired:
            lock.release()


def _terminate_process_tree(proc: subprocess.Popen[Any], windows_job: _WindowsJob | None = None) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        if windows_job is not None:
            windows_job.close()
        else:
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
    else:
        # HẬU DUỆ RỜI NHÓM VẪN PHẢI CHẾT (P1 cross-review PR "#141").
        #
        # `killpg` chỉ với tới nhóm của đứa con gốc. Một cháu gọi `setsid()` hoặc
        # `start_new_session=True` sang NHÓM MỚI và sống sót nguyên vẹn — rồi
        # `_maybe_heavy_lock` nhả khoá trong khi nó vẫn ghi vào kho. Khoá mà nhả
        # lúc thứ nó bảo vệ còn sống thì không phải khoá.
        #
        # Chụp cây TRƯỚC khi giết: nhóm chết xong, hậu duệ mồ côi được `init` nhận
        # nuôi và quan hệ cha-con biến mất — chụp sau là chụp một cái cây đã bị cắt.
        hau_due = _hau_due_posix(proc.pid)
        with contextlib.suppress(ProcessLookupError):
            os.killpg(proc.pid, signal.SIGTERM)
        for q in hau_due:                       # kể cả đứa đã sang nhóm khác
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.kill(q, signal.SIGTERM)
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(proc.pid, signal.SIGKILL)
        # "Đã gọi lệnh giết" ≠ "đã chết" — kiểm lại rồi mới nâng lên SIGKILL.
        for q in hau_due:
            if _con_song(q):
                with contextlib.suppress(ProcessLookupError, PermissionError):
                    os.kill(q, signal.SIGKILL)


def _con_song(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True                             # có thật, chỉ là ta không với tới
    return True


def _hau_due_posix(pid: int) -> list[int]:
    """Mọi hậu duệ của `pid`, KỂ CẢ đứa đã sang nhóm/session khác.

    Dựng quan hệ cha-con từ `ps` (có trên mọi POSIX, không chỉ Linux như `/proc`).
    Không đo được thì trả rỗng — phía gọi vẫn `killpg`, nên ta không tệ hơn bản cũ.
    """
    try:
        p = subprocess.run(["ps", "-A", "-o", "pid=,ppid="],
                           capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return []
    if p.returncode != 0:
        return []
    con: dict[int, list[int]] = {}
    for dong in (p.stdout or "").splitlines():
        phan = dong.split()
        if len(phan) < 2:
            continue
        try:
            con.setdefault(int(phan[1]), []).append(int(phan[0]))
        except ValueError:
            continue
    ra, hang, ta = [], list(con.get(pid, [])), os.getpid()
    while hang:
        q = hang.pop()
        if q in ra or q == ta:                  # tuyệt đối không tự giết mình
            continue
        ra.append(q)
        hang.extend(con.get(q, []))
    return ra


def _base_payload(args: argparse.Namespace, root: Path | None, identity: dict[str, Any]) -> dict[str, Any]:
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    return {
        "schema_version": SCHEMA_VERSION,
        "name": args.name,
        "kind": args.kind,
        "repo": str(root) if root is not None else str(Path(args.repo).resolve()),
        "identity": identity,
        "base_sha": args.base_sha,
        "command": command,
        "command_sha256": _sha256_bytes(_json_bytes(command)),
        "selected_tests": list(args.selected_test),
        "output_sha256": None,
        "positive_regex": args.positive_regex,
        "positive_match": None,
        "positive_verified": False,
        "first_failure": None,
        "artifact_identity": None,
        "started_at": _utc_now(),
        "completed_at": None,
        "duration_seconds": None,
        "status": "starting",
        "returncode": None,
        "timeout_seconds": args.timeout_seconds,
        "lock_path": None,
        "error": None,
    }


def _finish(payload: dict[str, Any], started: float, *, status: str, returncode: int, error: str | None = None) -> None:
    payload["completed_at"] = _utc_now()
    payload["duration_seconds"] = round(max(0.0, time.monotonic() - started), 6)
    payload["status"] = status
    payload["returncode"] = returncode
    payload["error"] = error


def cmd_run(args: argparse.Namespace) -> int:
    started = time.monotonic()
    evidence = Path(args.evidence).resolve()
    output = Path(args.output).resolve() if args.output else evidence.with_name(evidence.name + ".out")
    root: Path | None = None
    identity: dict[str, Any] = {}
    payload = _base_payload(args, root, identity)
    try:
        command = payload["command"]
        if not command:
            raise ValueError("command is required after --")
        if args.positive_regex is not None:
            re.compile(args.positive_regex)
        root, identity = _repo_identity(args.repo)
        payload["repo"] = str(root)
        payload["identity"] = identity
        if args.expected_head is not None:
            if not _SHA40.fullmatch(args.expected_head):
                raise ValueError("expected head must be a lowercase 40-character SHA")
            if identity["head_sha"] != args.expected_head:
                raise ValueError(
                    "HEAD mismatch: %s != %s" % (identity["head_sha"], args.expected_head)
                )
        if args.base_sha is not None and not _SHA40.fullmatch(args.base_sha):
            raise ValueError("base SHA must be a lowercase 40-character SHA")
        if args.require_clean and not identity["worktree_clean"]:
            raise ValueError("worktree is not clean, including untracked files")
    except (OSError, UnicodeError, ValueError) as exc:
        _finish(payload, started, status="preflight_error", returncode=EXIT_PREFLIGHT, error=str(exc))
        _atomic_json(evidence, payload)
        if not args.quiet:
            print(json.dumps({"ok": False, "status": payload["status"], "error": str(exc)}, ensure_ascii=False))
        return EXIT_PREFLIGHT

    with _maybe_heavy_lock(args.kind, root, args.wait_seconds) as (acquired, lock_path):
        payload["lock_path"] = lock_path
        if not acquired:
            _finish(
                payload,
                started,
                status="busy",
                returncode=EXIT_BUSY,
                error="another heavy gate holds the repository host lock",
            )
            _atomic_json(evidence, payload)
            if not args.quiet:
                print(json.dumps({"ok": False, "status": "busy", "lock_path": lock_path}, ensure_ascii=False))
            return EXIT_BUSY

        creationflags = (
            subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000004  # CREATE_SUSPENDED: attach job before code runs
            if os.name == "nt"
            else 0
        )
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            output_stream = output.open("wb")
        except OSError as exc:
            returncode = EXIT_PREFLIGHT
            _finish(
                payload,
                started,
                status="infra_error",
                returncode=returncode,
                error="cannot open gate output: %s" % exc,
            )
            _atomic_json(evidence, payload)
            if not args.quiet:
                print(json.dumps({"ok": False, "status": "infra_error", "error": str(exc)}))
            return returncode
        try:
            proc = subprocess.Popen(
                payload["command"],
                cwd=root,
                creationflags=creationflags,
                start_new_session=os.name != "nt",
                stdout=output_stream,
                stderr=subprocess.STDOUT,
            )
            windows_job = _WindowsJob.attach(proc)
            if os.name == "nt":
                if windows_job is None:
                    proc.kill()
                    proc.wait(timeout=5)
                    raise OSError("cannot attach suspended gate process to Windows Job Object")
                try:
                    _resume_windows_process(proc)
                except OSError:
                    windows_job.close()
                    proc.wait(timeout=5)
                    raise
        except OSError as exc:
            output_stream.close()
            returncode = EXIT_PREFLIGHT
            _finish(
                payload,
                started,
                status="infra_error",
                returncode=returncode,
                error="cannot start gate command: %s" % exc,
            )
            _atomic_json(evidence, payload)
            if not args.quiet:
                print(
                    json.dumps(
                        {
                            "ok": False,
                            "status": payload["status"],
                            "returncode": returncode,
                            "error": payload["error"],
                            "evidence": str(evidence),
                        },
                        ensure_ascii=False,
                    )
                )
            return returncode
        try:
            returncode = proc.wait(timeout=args.timeout_seconds)
            status = "pass" if returncode == 0 else "fail"
            _finish(payload, started, status=status, returncode=returncode)
        except subprocess.TimeoutExpired:
            _terminate_process_tree(proc, windows_job)
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.wait(timeout=5)
            returncode = EXIT_TIMEOUT
            _finish(
                payload,
                started,
                status="timeout",
                returncode=returncode,
                error="gate exceeded timeout",
            )
        except BaseException as exc:
            # NGẮT (Ctrl-C) VÀ MỌI ĐƯỜNG THOÁT BẤT THƯỜNG PHẢI GIẾT CÂY TRƯỚC KHI NHẢ KHOÁ.
            #
            # Cross-review P1 trên PR "#141" (`gate_lifecycle.py:540`). Con được đặt ở
            # SESSION MỚI nên nó KHÔNG nhận ngắt từ terminal; chỉ tiến trình cha nhận.
            # Khối trên chỉ bắt `TimeoutExpired`, nên `proc.wait()` ném `KeyboardInterrupt`
            # là stack unwind chạy thẳng qua đây, `_maybe_heavy_lock` NHẢ KHOÁ ở `finally`
            # của nó, trong khi con và cả cây hậu duệ VẪN CHẠY. Lượt heavy gate kế tiếp
            # lấy được khoá và chồng lên lượt "đã huỷ" — hai gate cùng ghi vào một kho.
            # Khoá mà nhả trong lúc thứ nó bảo vệ còn sống thì không phải khoá.
            #
            # `BaseException` chứ KHÔNG phải `Exception`: `KeyboardInterrupt` và
            # `SystemExit` đều KHÔNG kế thừa `Exception`, nên `except Exception` trượt
            # đúng ca cần bắt. Đây là lý do duy nhất dùng `BaseException` ở đây.
            #
            # Giết XONG rồi `wait` rồi mới `raise` lại: "đã gọi lệnh giết" ≠ "đã chết"
            # (bài học `taskkill`). Không nuốt ngoại lệ — Ctrl-C vẫn phải là Ctrl-C với
            # người gõ nó; ta chỉ chèn việc dọn vào TRƯỚC lúc nhả khoá.
            _terminate_process_tree(proc, windows_job)
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.wait(timeout=5)
            returncode = EXIT_INTERRUPTED
            _finish(
                payload,
                started,
                status="interrupted",
                returncode=returncode,
                error="gate interrupted: %s" % type(exc).__name__,
            )
            with contextlib.suppress(OSError):
                _atomic_json(evidence, payload)   # ghi bằng chứng TRƯỚC khi ném tiếp
            raise
        finally:
            if windows_job is not None:
                windows_job.close()
            output_stream.close()

        payload["output_sha256"] = _file_sha256(output)
        payload["artifact_identity"] = {
            "kind": "gate-output",
            "sha256": payload["output_sha256"],
        }
        if args.positive_regex is not None:
            payload["positive_match"] = _positive_match(output, args.positive_regex)
            payload["positive_verified"] = payload["positive_match"] is not None
            if returncode == 0 and not payload["positive_verified"]:
                returncode = 1
                _finish(
                    payload,
                    started,
                    status="fail",
                    returncode=returncode,
                    error="positive success evidence was not found in gate output",
                )

        try:
            after_root, after_identity = _repo_identity(root)
            payload["identity_after"] = after_identity
            stable_fields = ("head_sha", "tree_sha", "tracked_clean", "worktree_clean")
            changed = [field for field in stable_fields if identity.get(field) != after_identity.get(field)]
            if after_root != root:
                changed.append("repo")
            if changed:
                returncode = EXIT_PREFLIGHT
                _finish(
                    payload,
                    started,
                    status="infra_error",
                    returncode=returncode,
                    error="repository identity changed during gate: %s" % ", ".join(sorted(changed)),
                )
        except (OSError, UnicodeError, ValueError) as exc:
            returncode = EXIT_PREFLIGHT
            _finish(
                payload,
                started,
                status="infra_error",
                returncode=returncode,
                error="cannot read back repository identity: %s" % exc,
            )

        payload["first_failure"] = _first_failure(output, returncode)

    _atomic_json(evidence, payload)
    if not args.quiet:
        with output.open("rb") as stream:
            target = getattr(sys.stdout, "buffer", sys.stdout)
            shutil.copyfileobj(stream, target)
            target.flush()
        print(
            json.dumps(
                {
                    "ok": payload["status"] == "pass",
                    "status": payload["status"],
                    "name": payload["name"],
                    "returncode": payload["returncode"],
                    "duration_seconds": payload["duration_seconds"],
                    "evidence": str(evidence),
                },
                ensure_ascii=False,
            )
        )
    return returncode


def _read_evidence(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("evidence root must be an object")
    return value


def cmd_validate(args: argparse.Namespace) -> int:
    mismatches: list[str] = []
    try:
        for label, value in (
            ("expected head", args.expected_head),
            ("expected tree", args.expected_tree),
            ("expected base SHA", args.expected_base_sha),
        ):
            if not _SHA40.fullmatch(value):
                raise ValueError("%s must be a lowercase 40-character SHA" % label)
        re.compile(args.expected_positive_regex)
        payload = _read_evidence(Path(args.evidence))
        identity = payload.get("identity")
        if not isinstance(identity, dict):
            raise ValueError("identity is missing")
        if payload.get("schema_version") != SCHEMA_VERSION:
            mismatches.append("schema_version")
        if payload.get("status") != "pass":
            mismatches.append("status")
        if payload.get("returncode") != 0:
            mismatches.append("returncode")
        if payload.get("first_failure") is not None:
            mismatches.append("first_failure")
        if payload.get("positive_verified") is not True:
            mismatches.append("positive_verified")
        if payload.get("positive_regex") != args.expected_positive_regex:
            mismatches.append("positive_regex")
        output = Path(args.output)
        if not output.is_file():
            mismatches.append("output_missing")
        else:
            if payload.get("output_sha256") != _file_sha256(output):
                mismatches.append("output_sha256")
            if _positive_match(output, args.expected_positive_regex) is None:
                mismatches.append("positive_match")
        artifact_identity = payload.get("artifact_identity")
        if not isinstance(artifact_identity, dict):
            mismatches.append("artifact_identity")
        elif (
            artifact_identity.get("kind") != "gate-output"
            or artifact_identity.get("sha256") != payload.get("output_sha256")
        ):
            mismatches.append("artifact_identity")
        if identity.get("tracked_clean") is not True:
            mismatches.append("tracked_clean")
        if identity.get("worktree_clean") is not True:
            mismatches.append("worktree_clean")
        identity_after = payload.get("identity_after")
        if not isinstance(identity_after, dict):
            mismatches.append("identity_after")
        else:
            for field in ("head_sha", "tree_sha", "tracked_clean", "worktree_clean"):
                if identity_after.get(field) != identity.get(field):
                    mismatches.append("identity_after.%s" % field)
        if identity.get("head_sha") != args.expected_head:
            mismatches.append("head_sha")
        if identity.get("tree_sha") != args.expected_tree:
            mismatches.append("tree_sha")
        if payload.get("base_sha") != args.expected_base_sha:
            mismatches.append("base_sha")
        if payload.get("name") != args.expected_name:
            mismatches.append("name")
        if identity.get("system") != args.expected_system:
            mismatches.append("system")
        if identity.get("system_release") != args.expected_system_release:
            mismatches.append("system_release")
        if identity.get("machine") != args.expected_machine:
            mismatches.append("machine")
        if identity.get("python_implementation") != args.expected_python_implementation:
            mismatches.append("python_implementation")
        if identity.get("python_version") != args.expected_python:
            mismatches.append("python_version")
        if payload.get("selected_tests") != args.expected_selected_test:
            mismatches.append("selected_tests")
        expected_command = json.loads(args.expected_command_json)
        if not isinstance(expected_command, list) or not all(isinstance(x, str) for x in expected_command):
            raise ValueError("expected command JSON must be an array of strings")
        if payload.get("command") != expected_command:
            mismatches.append("command")
        if payload.get("command_sha256") != _sha256_bytes(_json_bytes(payload.get("command"))):
            mismatches.append("command_sha256")
        current = _sha256_bytes(Path(__file__).read_bytes())
        if identity.get("runner_sha256") != current:
            mismatches.append("runner_sha256")
        _, current_identity = _repo_identity(args.repo)
        if current_identity.get("head_sha") != args.expected_head:
            mismatches.append("current.head_sha")
        if current_identity.get("tree_sha") != args.expected_tree:
            mismatches.append("current.tree_sha")
        if current_identity.get("worktree_clean") is not True:
            mismatches.append("current.worktree_clean")
        if identity.get("catalog_policy_sha256") != current_identity.get("catalog_policy_sha256"):
            mismatches.append("catalog_policy_sha256")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        result = {"reusable": False, "mismatches": ["evidence_invalid"], "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return EXIT_PREFLIGHT

    result = {"reusable": not mismatches, "mismatches": sorted(set(mismatches))}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if not mismatches else EXIT_NOT_REUSABLE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    run = subparsers.add_parser("run", help="run one targeted or heavy gate and write JSON evidence")
    run.add_argument("--kind", choices=("targeted", "heavy"), required=True)
    run.add_argument("--name", required=True)
    run.add_argument("--repo", default=".")
    run.add_argument("--evidence", required=True)
    run.add_argument("--output")
    run.add_argument("--expected-head")
    run.add_argument("--base-sha")
    run.add_argument("--selected-test", action="append", required=True)
    run.add_argument("--require-clean", action="store_true")
    run.add_argument("--wait-seconds", type=float, default=0.0)
    run.add_argument("--timeout-seconds", type=float, required=True)
    run.add_argument("--quiet", action="store_true", help="do not replay captured child output to stdout")
    run.add_argument("--positive-regex", help="positive marker required before success evidence is reusable")
    run.add_argument("command", nargs=argparse.REMAINDER)
    run.set_defaults(handler=cmd_run)

    validate = subparsers.add_parser("validate", help="fail closed unless full-gate evidence is reusable")
    validate.add_argument("--evidence", required=True)
    validate.add_argument("--output", required=True)
    validate.add_argument("--repo", default=".")
    validate.add_argument("--expected-head", required=True)
    validate.add_argument("--expected-tree", required=True)
    validate.add_argument("--expected-base-sha", required=True)
    validate.add_argument("--expected-name", required=True)
    validate.add_argument("--expected-system", required=True)
    validate.add_argument("--expected-system-release", required=True)
    validate.add_argument("--expected-machine", required=True)
    validate.add_argument("--expected-python-implementation", required=True)
    validate.add_argument("--expected-python", required=True)
    validate.add_argument("--expected-selected-test", action="append", required=True)
    validate.add_argument("--expected-command-json", required=True)
    validate.add_argument("--expected-positive-regex", required=True)
    validate.add_argument(
        "--require-current-runner",
        action="store_true",
        help="compatibility flag; current-runner validation is always fail-closed",
    )
    validate.set_defaults(handler=cmd_validate)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if getattr(args, "timeout_seconds", None) is not None and args.timeout_seconds <= 0:
        print("timeout-seconds must be positive", file=sys.stderr)
        return EXIT_PREFLIGHT
    if getattr(args, "wait_seconds", 0.0) < 0:
        print("wait-seconds cannot be negative", file=sys.stderr)
        return EXIT_PREFLIGHT
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
