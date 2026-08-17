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
import uuid
import atexit
from typing import Any, Iterator


SCHEMA_VERSION = 2
EXIT_PREFLIGHT = 2
EXIT_NOT_REUSABLE = 3
EXIT_BUSY = 75
EXIT_TIMEOUT = 124
# 128 + SIGINT(2), quy ước shell cho "bị ngắt". Tách khỏi `EXIT_TIMEOUT` vì hai
# chuyện khác nhau: quá hạn là gate tự quyết, ngắt là người gõ Ctrl-C.
EXIT_INTERRUPTED = 130
# FAIL-CLOSE: lượt dọn KHÔNG trọn vẹn thì lượt gate ấy hỏng, kể cả khi lệnh gate
# đã chạy xong và trả 0. "Khoá mà nhả trong lúc thứ nó bảo vệ còn sống thì không
# phải khoá" — trước đây sự thật ấy chỉ ĐI VÀO BẢN GHI mà không đổi mã thoát, nên
# một lượt rò tiến trình vẫn đi qua như đạt.
EXIT_GIET_KHONG_TRON_VEN = 4
# 128 + SIGTERM(15), quy ước shell. Tách khỏi `EXIT_INTERRUPTED` vì hai chuyện
# khác nhau: Ctrl-C là người gõ, SIGTERM là hệ thống (CI huỷ, job hết giờ, máy
# tắt dịch vụ) — và chỉ đường thứ hai mới đi qua handler dưới đây.
EXIT_BI_KET_THUC = 143


class BiKetThuc(BaseException):
    """Nhận `SIGTERM`/`SIGHUP`. Kế thừa `BaseException`, KHÔNG phải `Exception`.

    Vì sao cần cả một lớp riêng: mặc định `SIGTERM` GIẾT NGAY tiến trình Python —
    không `finally`, không `atexit`, không ngoại lệ nào được ném. Đo được trên
    `e0a4cb9`: bắn `SIGTERM` vào runner đang `proc.wait()` thì nó thoát `-15`,
    KHÔNG ghi tệp bằng chứng, con gate SỐNG SÓT qua mốc tuyệt đối, và hệ điều
    hành đã nhả `flock` — tức lượt heavy gate kế tiếp vào được trong lúc con của
    lượt "đã huỷ" vẫn ghi vào kho.

    Đó ĐÚNG hình dạng P1 mở đầu PR này ("ngắt phải giết cây trước khi nhả khoá"),
    chỉ khác lối vào: bản vá cũ chỉ che `KeyboardInterrupt` (SIGINT). Biến tín
    hiệu thành ngoại lệ thì khối `except BaseException` sẵn có xử lý được cả hai.
    """
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


# ---------------------------------------------------------------------------
# CÁCH LY BẰNG CGROUP v2 — ĐỔI KIẾN TRÚC, KHÔNG PHẢI VÁ TIẾP
#
# Vòng quét cây đã qua BỐN vòng vá cùng một hình dạng (`killpg` → chụp một lần →
# subreaper + khoá danh tính → điều kiện lặng), và vòng nào cross-review cũng lộ
# một lỗ mới. Đo được trên `38f1253`: một kẻ ĐẺ LẠI LIÊN TỤC vẫn thoát — 33 kẻ
# sinh ra, 5 sống sót, kẻ sớm nhất sinh lúc t=11,4s tức SAU khi hạn 10s vỡ, trong
# cửa sổ `killpg` → `proc.wait(2)`. Hạn đồng hồ 10s CÙNG HÌNH DẠNG với bộ đếm 6
# lượt mà nó thay thế: kẻ đẻ lại chỉ cần sống lâu hơn cái hạn là thoát.
#
# Không có bản vá thứ năm nào đóng được lớp ấy, vì lỗ nằm ở CHỖ KHÁC: mọi cơ chế
# quét đều phải hỏi "ai là hậu duệ của ta", mà câu hỏi ấy trả lời được hay không
# lại do chính đối tượng bị quét quyết định (`setsid`, mồ côi, đẻ trong lúc dọn).
# cgroup lật ngược quan hệ: thành viên là THEO CẤU TRÚC, gán lúc sinh và kế thừa
# không thể từ chối, nên không còn gì để quét và không còn cửa sổ để lách.
# Đo được: `cgroup.kill` giết sạch đúng kẻ đẻ lại ấy trong 0,0002s, 0 sống sót.
#
# PHẠM VI CỦA CHÍNH LỚP CGROUP — KHAI THẲNG, ĐỪNG ĐỂ AI ĐỌC RỘNG HƠN.
#
# ĐÓNG ĐƯỢC (đo được): thoát VÔ TÌNH — `setsid`, mồ côi rồi được `init` nhận
# nuôi, đẻ trong lúc dọn, sinh sau khi hạn vỡ. Đó đúng là thứ đã gãy BỐN vòng vá,
# và cgroup đóng nó bằng MỘT thao tác nguyên tử của nhân, không quét, không đua.
#
# KHÔNG ĐÓNG ĐƯỢC: tiến trình CỐ TÌNH tự ghi PID của mình vào `cgroup.procs` của
# cgroup cha để trèo ra. Uỷ quyền cgroup KHÔNG ĐẶC QUYỀN về nguyên tắc không chặn
# nổi: quyền cần để chuyển VÀO chính là quyền cho phép trèo RA một tầng. Muốn
# chặn thật thì phải có helper đặc quyền làm việc chuyển, hoặc cgroup namespace —
# cả hai đều bắt gate phải có quyền root ở mọi nơi nó chạy, kể cả máy người dùng.
# HIỆN TẠI KHE NÀY KHÔNG CHẶN VÀ CŨNG CHƯA PHÁT HIỆN ĐƯỢC — nói thẳng, vì một
# lời khai nửa vời ở đây còn tệ hơn không khai. Đã thử một bản phát hiện (nhớ ai
# từng ở trong cgroup rồi kiểm lại từng đứa) và ĐO THẤY NÓ SAI CẢ HAI CHIỀU:
#   · kẻ trèo ra TRƯỚC lượt dọn thì chưa từng được ghi nhớ ⇒ lọt;
#   · tiến trình đã chết nhưng chưa được cha gặt (zombie) vẫn còn
#     `/proc/<pid>/stat` với đúng `starttime` ⇒ khoá danh tính khớp ⇒ HÔ OAN.
# Một bộ phát hiện hô oan sẽ làm cổng mất tin cậy nhanh hơn là cái lỗ nó vá. Nên
# nó bị TÁCH RA làm việc riêng, không nhét nửa vời vào đây (xem `ops/NO_KY_THUAT.md`).
#
# Nghĩa là: `giet_tron_ven: true` KHÔNG bao gồm lời hứa "không ai trèo ra". Nó chỉ
# nói "cgroup đã rỗng và đã xác nhận rỗng". Ai đọc bản ghi phải hiểu đúng chừng ấy.
#
# PHẠM VI NỀN: chỉ Linux có cgroup v2. Windows đã có Job Object — cùng
# một kiến trúc "vùng chứa, giết cả vùng". macOS và FreeBSD KHÔNG có cả hai, nên
# ở đó vẫn là vòng quét cây và lỗ "đẻ trong lúc dọn" CÒN NGUYÊN; `giet_tron_ven`
# và `co_che_cach_ly` là thứ nói thật về điều đó.
# ---------------------------------------------------------------------------

# Cơ chế THỰC SỰ đã dùng cho lượt này, đi thẳng vào bằng chứng. Không có trường
# này thì một lần tụt về quét cây sẽ đi qua y hệt một lượt cgroup thành công —
# đúng bẫy "đếm sự CÓ MẶT của một đường thay vì KHẢ NĂNG của nó" mà kho đã trả giá
# bốn lần.
_CO_CHE_CACH_LY = "quet-cay"

# Cgroup riêng của lượt gate này; None = không cấp được, chạy đường dự phòng.
_CGROUP_GATE: Path | None = None

# Bật khi đã THẬT SỰ quét cgroup và xác nhận nó rỗng. Phân biệt "đo rồi, sạch"
# với "chưa đo lần nào" — hai thứ mà đường ĐẠT không có vùng chứa hay bị gộp.
_CGROUP_GATE_DA_QUET = False


# MỐI NỐI KIỂM THỬ — liệt kê ở MỘT chỗ để còn khai được vào bằng chứng.
#
# P1 cross-review trên `e480a93`: ba biến này nằm trong MÃ SẢN XUẤT và kế thừa
# thẳng từ môi trường, nên một lượt gate có thể bị hạ cấp (hoặc bị bơm lỗi) rồi
# vẫn sinh ra bằng chứng TÁI DÙNG ĐƯỢC. Đó là đường lách cổng, và tệ hơn là nó
# có thể bị bật NGOÀI Ý MUỐN bởi môi trường shell/CI.
#
# Chốt: hai biến BƠM LỖI làm bằng chứng KHÔNG tái dùng được (đó là lượt thí
# nghiệm, không phải lượt gate thật). `TL_GATE_TAT_CGROUP` KHÔNG bơm lỗi — nó là
# công tắc vận hành thật cho host cgroup hỏng — nên nó chỉ hạ `co_che_cach_ly`
# xuống `quet-cay`, và ai cần vùng chứa thì đòi bằng `validate --doi-cach-ly`.
_MOI_NOI_BOM_LOI = ("TL_GATE_EP_BAO_RO", "TL_GATE_EP_HONG_VAO_CGROUP")
_MOI_NOI_HA_CAP = ("TL_GATE_TAT_CGROUP",)


def _moi_noi_dang_bat() -> list[str]:
    return sorted(k for k in (_MOI_NOI_BOM_LOI + _MOI_NOI_HA_CAP)
                  if os.environ.get(k) == "1")


def _don_cgroup_con_sot() -> None:
    """Dọn cgroup nếu đường chính chưa kịp dọn. Đăng ký qua `atexit`.

    P2 cross-review trên `e480a93`: cgroup được cấp TRƯỚC khi sinh con, nhưng
    khối `finally` dọn tổng quát chỉ bắt đầu SAU khi sinh con xong. Một
    `KeyboardInterrupt` rơi vào đúng quãng giữa thì cgroup ở lại vĩnh viễn — nên
    câu "dọn ở mọi đường thoát" là khai rộng hơn thứ mã làm được.
    Dùng `atexit` thay vì bọc thêm một tầng `try` quanh cả khối: nó phủ được cả
    ngắt, `SystemExit`, lẫn mọi `return` sớm mai sau ai đó thêm vào.
    """
    if _CGROUP_GATE is not None:
        with contextlib.suppress(Exception):
            _giet_cgroup(_CGROUP_GATE, han_giay=2.0)
        _don_cgroup(_CGROUP_GATE)


def _mount_cgroup2() -> Path | None:
    """Điểm gắn cgroup v2, dò từ `/proc/self/mountinfo`.

    KHÔNG hardcode `/sys/fs/cgroup`: máy lai (v1 và v2 song song) gắn v2 ở chỗ
    khác — đo được trong container của phiên này là `/sys/fs/cgroup/unified`.
    Hardcode thì cgroup hoá ra "không có" ở đúng nơi nó đang có, và ta lặng lẽ
    tụt về đường quét cây trong khi đường tốt vẫn nằm đó.

    Cắt theo dấu `" - "` chứ KHÔNG đếm cột: `mountinfo` có số trường tuỳ biến
    (optional fields) trước dấu ấy, đếm cột là lệch trên đúng máy có chúng.
    """
    try:
        noi_dung = Path("/proc/self/mountinfo").read_text()
    except OSError:
        return None
    for dong in noi_dung.splitlines():
        try:
            trai, phai = dong.split(" - ", 1)
        except ValueError:
            continue
        sau = phai.split()
        truoc = trai.split()
        if sau and sau[0] == "cgroup2" and len(truoc) >= 5:
            return Path(truoc[4])
    return None


def _cgroup_cua_ta() -> str:
    """Đường cgroup v2 của CHÍNH tiến trình này (dòng `0::` trong `/proc/self/cgroup`)."""
    with contextlib.suppress(OSError):
        for dong in Path("/proc/self/cgroup").read_text().splitlines():
            phan = dong.split(":", 2)
            if len(phan) == 3 and phan[0] == "0":
                return phan[2]
    return "/"


def _pid_trong_cgroup(cg: Path) -> list[int] | None:
    """PID trong cgroup. `[]` = RỖNG THẬT. `None` = KHÔNG ĐỌC ĐƯỢC — khác hẳn nhau.

    P1 cross-review trên `e480a93`: bản trước trả `[]` cho CẢ HAI, nên một lượt
    đọc hỏng (`EACCES`, `EIO`, cgroup bị xoá mất giữa chừng) được `_giet_cgroup`
    đọc thành "cgroup đã rỗng" rồi khai `giet_tron_ven: true` — xanh giả. Tác giả
    đã tự dựng lại: `_giet_cgroup(<cgroup khong doc duoc>)` trả `True`.

    Đây ĐÚNG hình dạng lỗi mà cả bản vá này sinh ra để đóng ("vắng mặt vì sạch"
    ≠ "vắng mặt vì chưa đo"), và tôi mắc lại nó ngay trong hàm đi đóng nó.
    """
    # PHẢI QUÉT CẢ CÂY CON, không chỉ `cgroup.procs` ở tầng trên (P1 cross-review
    # trên `19a9c0e`). Lệnh gate hoàn toàn có thể tự tạo cgroup CON bên trong
    # cgroup của ta; tiến trình nằm trong đó KHÔNG xuất hiện ở `cgroup.procs`
    # tầng trên. Đo được: tiến trình sống trong cgroup con mà `_giet_cgroup` khai
    # `True` = "đã xác nhận rỗng". Lại đúng hình dạng cũ — hỏi sai chỗ rồi đọc
    # câu trả lời rỗng thành "sạch".
    #
    # `rmdir` cũng hỏng khi còn cgroup con, nên không quét cây con thì vừa khai
    # sai vừa để lại rác.
    # TẦNG TRÊN và TẦNG CON chịu luật KHÁC NHAU — gộp lại là tự dựng lại đúng P1
    # vừa vá. `FileNotFoundError` ở cgroup CON nghĩa là nó vừa biến mất giữa lúc
    # quét (bình thường, bỏ qua được). Cũng lỗi ấy ở cgroup GỐC nghĩa là ta không
    # đọc được thứ cần đọc — và im lặng bỏ qua nó thì hàm trả `[]` = "rỗng thật"
    # cho một cgroup chưa từng đọc nổi. Bộ ca bắt đúng chỗ này.
    try:
        tong = [int(x) for x in (cg / "cgroup.procs").read_text().split()]
    except (OSError, ValueError):
        return None                      # gốc KHÔNG đọc được ⇒ không kết luận gì
    try:
        con = [q for q in cg.rglob("*") if q.is_dir()]
    except OSError:
        return None
    for muc in con:
        try:
            tong.extend(int(x) for x in (muc / "cgroup.procs").read_text().split())
        except FileNotFoundError:
            continue                     # cgroup con vừa biến mất giữa chừng
        except (OSError, ValueError):
            return None
    return tong


def _tao_cgroup_gate() -> Path | None:
    """Cấp một cgroup riêng cho lượt gate. None = không cấp được (chạy dự phòng).

    Tạo DƯỚI cgroup của chính ta, KHÔNG phải ở gốc điểm gắn: trên host systemd
    chạy non-root ta chỉ được uỷ quyền trong nhánh của mình, `mkdir` ở gốc trả
    `EACCES`. Tạo ở gốc "chạy được trong container này" là đúng kiểu kết luận từ
    một nền rồi khai cho mọi nền — lỗi kho đã ghi sổ.
    """
    # CÔNG TẮC TẮT — để đường DỰ PHÒNG có thể kiểm được.
    #
    # Không có công tắc này thì đường quét cây (thứ macOS/FreeBSD thực sự chạy)
    # KHÔNG kiểm được trên Linux, và "có nhánh dự phòng trong mã" lại bị đọc thành
    # "nhánh dự phòng chạy được" — đúng lỗi đếm SỰ CÓ MẶT thay vì KHẢ NĂNG. Nó
    # cũng có ích thật ngoài đời: host nào cgroup hành xử lạ thì tắt mà chạy tiếp.
    if os.environ.get("TL_GATE_TAT_CGROUP") == "1":
        return None
    if platform.system() != "Linux":
        return None
    mount = _mount_cgroup2()
    if mount is None:
        return None
    cha = mount / _cgroup_cua_ta().lstrip("/")
    if not cha.is_dir():
        cha = mount                      # lệch cgroup-namespace: lùi về gốc điểm gắn
    cg = cha / ("tl-gate-%d-%s" % (os.getpid(), uuid.uuid4().hex[:8]))
    try:
        cg.mkdir()
    except OSError:
        return None
    # KHẢ NĂNG, KHÔNG PHẢI SỰ CÓ MẶT: thư mục tạo được KHÔNG có nghĩa là ghi được
    # pid vào. Hỏi "thứ này đã làm được việc chưa", đừng hỏi "nó có ở đó không".
    if not os.access(cg / "cgroup.procs", os.W_OK):
        with contextlib.suppress(OSError):
            cg.rmdir()
        return None
    return cg


def _tao_cgroup_gate_thu() -> bool:
    """Thử cấp rồi trả lại ngay — chỉ để CHẨN ĐOÁN, không giữ cgroup nào."""
    cg = _tao_cgroup_gate()
    if cg is None:
        return False
    _don_cgroup(cg)
    return True


def _vao_cgroup(cg: Path) -> None:
    """Tự đưa mình vào cgroup. Gọi trong `preexec_fn`, tức SAU `fork` TRƯỚC `exec`.

    Phải là con tự ghi pid của nó, không phải cha ghi hộ sau khi `Popen` trả về:
    ghi sau là có một khoảng con đã chạy mà chưa thuộc cgroup, và đúng khoảng ấy
    nó kịp đẻ ra thứ nằm ngoài vùng chứa. Vào lúc `fork` thì không có khoảng nào.
    """
    # MỐI NỐI KIỂM THỬ: ép hỏng đúng lúc `fork` để nhánh tụt-về-quét-cây có ca
    # chạy được. Ca ấy không dựng lại được theo ý muốn trên máy thường.
    if os.environ.get("TL_GATE_EP_HONG_VAO_CGROUP") == "1":
        raise OSError(16, "ep hong khi vao cgroup (moi noi kiem thu)")
    (cg / "cgroup.procs").write_text(str(os.getpid()))


def _giet_cgroup(cg: Path, han_giay: float = 5.0) -> bool:
    """Giết TOÀN BỘ cgroup. True = đã XÁC NHẬN rỗng, không phải "đã gọi lệnh giết".

    `cgroup.kill` (nhân ≥ 5.14) bắn `SIGKILL` cho mọi thành viên trong MỘT thao
    tác của nhân — không quét, không đua, và `SIGKILL` thì không handler nào phớt
    lờ được. Nhân cũ hơn không có tệp ấy: ĐÓNG BĂNG trước rồi mới bắn, vì đóng
    băng xong thì không ai đẻ thêm được nữa nên vòng quét dưới đây HỘI TỤ — khác
    hẳn quét một cây đang chạy tự do, chỗ mà bốn vòng vá trước đã chết.
    """
    try:
        (cg / "cgroup.kill").write_text("1")
    except OSError:
        with contextlib.suppress(OSError):
            (cg / "cgroup.freeze").write_text("1")
        for _ in range(50):
            pids = _pid_trong_cgroup(cg)
            if pids == []:                       # RỖNG THẬT, không phải đọc hỏng
                break
            for q in (pids or []):
                with contextlib.suppress(ProcessLookupError, PermissionError):
                    os.kill(q, signal.SIGKILL)
            time.sleep(0.1)
        with contextlib.suppress(OSError):
            (cg / "cgroup.freeze").write_text("0")
    # "ĐÃ GỌI LỆNH GIẾT" ≠ "ĐÃ CHẾT" (bài học `taskkill`): đòi cgroup RỖNG.
    het = time.monotonic() + han_giay
    xong = False
    while True:
        # CHỈ `[]` mới là "đã xác nhận rỗng". `None` là không đọc được, và không
        # đọc được thì KHÔNG được kết luận gì — cứ đợi tới hết hạn rồi khai thua.
        if _pid_trong_cgroup(cg) == []:
            xong = True
            break
        if time.monotonic() > het:
            break
        time.sleep(0.05)
    # MỐI NỐI KIỂM THỬ: ép BÁO rò (vẫn giết thật ở trên) để nhánh fail-close có
    # ca chạy được. Nhánh ấy chỉ tự nhiên xảy ra khi `cgroup.kill` không hội tụ
    # trong hạn — không dựng lại được theo ý muốn, mà một nhánh KHÔNG THỂ đỏ thì
    # lời khai về độ phủ của nó là lời khai sai. Không bao giờ làm rò thật.
    if os.environ.get("TL_GATE_EP_BAO_RO") == "1":
        return False
    return xong


def _don_cgroup(cg: Path) -> None:
    """Xoá cgroup, kể cả cgroup CON do lệnh gate tự tạo (sâu nhất trước).

    `rmdir` một cgroup còn con sẽ hỏng, và hỏng ở đây bị `suppress` nuốt mất —
    thành ra để lại nguyên cụm cgroup rác mà không ai biết.
    """
    with contextlib.suppress(OSError):
        for muc in sorted((q for q in cg.rglob("*") if q.is_dir()),
                          key=lambda q: len(q.parts), reverse=True):
            with contextlib.suppress(OSError):
                muc.rmdir()
    with contextlib.suppress(OSError):
        cg.rmdir()


def _terminate_process_tree(proc: subprocess.Popen[Any], windows_job: _WindowsJob | None = None) -> None:
    global _GIET_KHONG_TRON_VEN
    # CGROUP TRƯỚC MỌI THỨ KHÁC — và KHÔNG thoát sớm theo `proc.poll()`.
    #
    # Con gốc chết KHÔNG có nghĩa là cây đã sạch: hậu duệ `setsid` sống lâu hơn
    # cha là đúng ca ta đang đóng. Đường quét cây buộc phải thoát sớm ở đây vì
    # mất cha là mất mỏ neo để truy cây; cgroup thì không cần mỏ neo nào, thành
    # viên là theo cấu trúc, nên vẫn dọn được sau khi cha đã chết.
    if _CGROUP_GATE is not None:
        if not _giet_cgroup(_CGROUP_GATE):
            _GIET_KHONG_TRON_VEN = True
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.wait(timeout=2)
        return
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
        # LÀM LẶNG CÂY TRƯỚC, GIẾT CHA SAU — và đó là toàn bộ mấu chốt.
        #
        # Bản trước chụp cây MỘT LẦN rồi giết. Hai lỗ, cross-review bắt cả hai với
        # bằng chứng tươi trên `47d10b0`:
        #   · một hậu duệ có thể cài handler SIGTERM và ĐẺ THÊM tiến trình `setsid()`
        #     ngay khi bị bắn — đứa mới sinh SAU ảnh chụp nên không ai với tới;
        #   · PID trong ảnh có thể chết rồi được CẤP LẠI cho tiến trình vô can, và
        #     `os.kill(SIGKILL)` sau đó giết nhầm người ngoài.
        #
        # Vì sao phải giữ cha sống trong lúc dọn: giết nhóm cha xong thì mọi cháu mồ
        # côi được `init` nhận nuôi, quan hệ cha-con ĐỨT, và không còn cách nào truy
        # chúng là hậu duệ nữa. Cha là cái MỎ NEO duy nhất để lần ra cây; bỏ neo
        # trước rồi mới đi tìm là tự làm mù mình.
        #
        # Nên: lặp {chụp → bắn đứa MỚI} khi cha CÒN SỐNG, tới khi một vòng không
        # thấy ai mới (cây đã lặng) — đứa đẻ trong lúc dọn vì thế vẫn bị bắt ở vòng
        # sau. Rồi mới giết nhóm cha. Mọi tín hiệu đều KIỂM DANH TÍNH trước khi bắn.
        # Gốc duyệt: là CHÍNH TA khi đã làm subreaper (đứa mồ côi rơi về đây), còn
        # không thì là con gốc. Chọn sai gốc thì vòng lặp dưới mù đúng ca cần bắt.
        goc = os.getpid() if _CO_SUBREAPER else proc.pid
        # LẶP TỚI KHI CÂY LẶNG, chặn bằng ĐỒNG HỒ — không phải đếm vòng.
        #
        # Bản trước cắt cứng ở 6 lượt (P1 cross-review PR "#141"): một kẻ đẻ lại
        # liên tục chỉ cần sống lâu hơn 6 lượt là thoát, và ta KHÔNG hề biết — vòng
        # lặp kết thúc êm y như khi cây đã lặng thật. Hai kết cục khác hẳn nhau mà
        # nhìn giống nhau, đúng bệnh "vắng mặt vì sạch" và "vắng mặt vì chưa chạy"
        # trông như một. Hết hạn mà còn đứa mới là DỮ KIỆN, phải ghi chứ không nuốt.
        da_gui: dict[int, str] = {}
        han_lang = time.monotonic() + 10.0
        # "KHÔNG AI MỚI" KHÔNG PHẢI "CÂY ĐÃ LẶNG" (P1 cross-review PR "#141").
        #
        # Một hậu duệ ĐÃ bị bắn vẫn có thể đang nằm trong handler SIGTERM của nó.
        # Nếu handler chờ lâu hơn 0,2s rồi mới đẻ đứa tách rời, vòng lặp của bản
        # trước đã thoát: đứa mới sinh trong lúc `proc.wait(2)`, được subreaper nhận
        # nuôi, và KHÔNG BAO GIỜ được quét lại. Tệ nhất là bản ghi khi ấy vẫn khai
        # `giet_tron_ven: true` — tức bản vá của tôi làm BẰNG CHỨNG NÓI DỐI, hỏng
        # nặng hơn hẳn việc sót một tiến trình mà khai đúng.
        #
        # Điều kiện lặng phải gồm CẢ HAI: không ai mới, VÀ mọi đứa đã bắn đã BIẾN
        # MẤT — rồi còn phải đứng yên qua một khoảng ÂN HẠN để đứa đẻ muộn kịp lộ.
        while True:
            anh = _cac_hau_due(goc)             # cha còn sống nên cây còn truy được
            moi = {q: k for q, k in anh.items() if da_gui.get(q) != k}
            con_song = [q for q, k in da_gui.items() if _khoa_pid(q) == k]
            if not moi and not con_song:
                # Ân hạn: đứng yên rồi soi lại. Đứa đẻ muộn xuất hiện ở đây.
                time.sleep(AN_HAN_LANG_GIAY)
                lai = _cac_hau_due(goc)
                if not {q: k for q, k in lai.items() if da_gui.get(q) != k}:
                    break                        # cây đã lặng THẬT
                anh = lai
                moi = {q: k for q, k in lai.items() if da_gui.get(q) != k}
            if time.monotonic() > han_lang:
                _GIET_KHONG_TRON_VEN = True      # KHÔNG im lặng bỏ qua
                break
            for q, khoa in moi.items():
                if _khoa_pid(q) == khoa:         # đúng tiến trình cũ, không phải PID tái dùng
                    with contextlib.suppress(ProcessLookupError, PermissionError):
                        os.kill(q, signal.SIGTERM)
                    da_gui[q] = khoa
            time.sleep(0.2)

        with contextlib.suppress(ProcessLookupError):
            os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(proc.pid, signal.SIGKILL)
        # "Đã gọi lệnh giết" ≠ "đã chết". Leo thang có KIỂM DANH TÍNH: so lại khoá
        # thời điểm tạo, vì giữa SIGTERM và đây PID có thể đã đổi chủ.
        for q, khoa in da_gui.items():
            if _khoa_pid(q) == khoa:
                with contextlib.suppress(ProcessLookupError, PermissionError):
                    os.kill(q, signal.SIGKILL)


# Đặt ở đường `run` TRƯỚC khi sinh con; xem `_dat_subreaper`.
_CO_SUBREAPER = False

# Bật khi `_terminate_process_tree` HẾT HẠN mà cây vẫn còn đứa mới sinh. Đi thẳng
# vào bằng chứng: "đã gọi lệnh dọn" KHÔNG phải "đã dọn xong", và người đọc bản ghi
# phải phân biệt được hai thứ đó.
_GIET_KHONG_TRON_VEN = False

# Khoảng ÂN HẠN sau khi cây có vẻ lặng: đứa đẻ muộn (handler chờ rồi mới sinh) chỉ
# lộ ra nếu ta đứng yên đủ lâu rồi soi lại. Dài hơn nhịp quét 0,2s một bậc.
AN_HAN_LANG_GIAY = 1.0


def _dat_subreaper() -> bool:
    """Nhận nuôi mọi hậu duệ mồ côi (Linux `PR_SET_CHILD_SUBREAPER`).

    VÌ SAO CẦN, và vì sao lặp-phát-hiện KHÔNG đủ: một cháu có thể đẻ thêm rồi CHẾT
    NGAY. Đứa mới lập tức mồ côi và được `init` nhận nuôi, nên quan hệ cha-con tới
    cây của ta ĐỨT — duyệt bao nhiêu vòng cũng không thấy nó nữa. Ảnh chụp không
    sai vì chụp thiếu; nó sai vì thứ cần tìm đã rời khỏi cây trước khi ta nhìn lại.
    (Đo được: ca `case_descendant_spawned_during_shutdown_is_contained` ĐỎ với bản
    chỉ lặp-phát-hiện.)

    Đặt tiến trình NÀY làm subreaper thì mọi hậu duệ mồ côi trong cả cây rơi về
    ĐÂY thay vì về `init`, nên chúng vẫn truy được — đó là lý do phải duyệt từ
    `os.getpid()` chứ không từ `proc.pid`.

    KHAI THẲNG PHẠM VI — CHỈ LINUX.
    Bản trước viết "Linux (và FreeBSD)" trong khi điều kiện là
    `platform.system() != "Linux"`, tức FreeBSD LUÔN bị tắt. Phạm vi tuyên bố rộng
    hơn phạm vi mã làm được, đúng lỗi kho đã ghi sổ — và tôi mắc nó NGAY TRONG câu
    viết ra để khai phạm vi cho trung thực (P2 cross-review PR "#141").
    FreeBSD có `procctl(PROC_REAP_ACQUIRE)`, nhưng ở đây KHÔNG có FreeBSD để chạy
    thử, mà khai một nền chưa từng đo lại đúng là cái vừa sai. Nên: macOS,
    Windows VÀ FreeBSD đều nằm ngoài — ở đó lỗ "đẻ trong lúc dọn" CÒN NGUYÊN, và
    `giet_tron_ven` là thứ duy nhất nói thật về điều đó.
    """
    if platform.system() != "Linux":
        return False
    try:
        import ctypes
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        return libc.prctl(36, 1, 0, 0, 0) == 0      # 36 = PR_SET_CHILD_SUBREAPER
    except (OSError, AttributeError, ValueError):
        return False


def _khoa_pid(pid: int) -> str | None:
    """Khoá danh tính của MỘT pid — thời điểm tạo. None = không xác định được.

    PID quay vòng. "PID này còn tồn tại" KHÔNG trả lời được câu ta cần hỏi là "có
    còn ĐÚNG tiến trình cũ không" — và giết nhầm một tiến trình vô can của cùng
    người dùng là hỏng nặng hơn nhiều so với để sót một tiến trình.

    ĐỘ PHÂN GIẢI LÀ NỘI DUNG, KHÔNG PHẢI CHI TIẾT (P1 cross-review PR "#141").
    Bản trước dùng `ps -o lstart=`, mà nó chỉ tới GIÂY — đo được:
    `Mon Aug 17 02:50:06 2026`. Hai tiến trình cùng PID sinh trong CÙNG một giây
    là không phân biệt được, tức khoá không đóng nổi đúng ca nó sinh ra để đóng,
    và trên máy có tốc độ tạo tiến trình cao thì đó không phải giả thuyết.
    Linux có `/proc/<pid>/stat` trường 22 (`starttime`) tính bằng TICK — mặc định
    100 tick/giây, tức mịn gấp 100 lần. Dùng nó khi có; nơi khác lùi về `lstart`
    và CHẤP NHẬN độ phân giải thô — nhưng khai ra ở đây thay vì im lặng.
    """
    v = _khoa_pid_proc(pid)
    if v is not None:
        return v
    try:
        p = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)],
                           capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    v = (p.stdout or "").strip()
    return ("giay:" + v) if (p.returncode == 0 and v) else None


def _khoa_pid_proc(pid: int) -> str | None:
    """`starttime` (tick) từ `/proc/<pid>/stat`; None nếu nền không có `/proc`.

    `comm` có thể chứa khoảng trắng và dấu ')' nên cắt từ ')' CUỐI CÙNG — cùng
    khuôn `launcher.py` đã dùng, và cùng lý do.
    """
    try:
        nd = Path(f"/proc/{pid}/stat").read_text()
        sau = nd[nd.rindex(")") + 2:].split()
        return "tick:" + sau[19]
    except (OSError, ValueError, IndexError):
        return None


def _cac_hau_due(pid: int) -> dict[int, str]:
    """Hậu duệ của `pid` -> khoá danh tính, KỂ CẢ đứa đã sang nhóm/session khác.

    Một lần gọi `ps` lấy cả quan hệ cha-con LẪN thời điểm tạo: hai nguồn khác nhau
    thì khoá đo ở đây và khoá đo lúc bắn có thể lệch định dạng và không bao giờ
    khớp — chốt hoá ra LUÔN từ chối bắn, hỏng âm thầm theo chiều ngược lại.
    Dùng `ps` chứ không `/proc` để chạy được cả trên macOS. Không đo được thì trả
    rỗng — phía gọi vẫn `killpg`, tức không tệ hơn bản không có hàm này.
    """
    con: dict[int, list[int]] = {}
    khoa: dict[int, str] = {}
    goc_proc = Path("/proc")
    if goc_proc.is_dir():
        # MỘT NGUỒN cho cả quan hệ cha-con lẫn khoá, và khoá mịn tới tick. Hai
        # nguồn khác nhau thì khoá đo ở đây và khoá đo lúc bắn lệch định dạng,
        # chốt hoá ra LUÔN từ chối bắn — hỏng âm thầm theo chiều ngược lại.
        for muc in goc_proc.iterdir():
            if not muc.name.isdigit():
                continue
            try:
                nd = (muc / "stat").read_text()
                sau = nd[nd.rindex(")") + 2:].split()
                q, cha = int(muc.name), int(sau[1])
            except (OSError, ValueError, IndexError):
                continue
            con.setdefault(cha, []).append(q)
            khoa[q] = "tick:" + sau[19]
    else:
        try:
            p = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,lstart="],
                               capture_output=True, text=True,
                               stdin=subprocess.DEVNULL, timeout=10)
        except (OSError, subprocess.SubprocessError):
            return {}
        if p.returncode != 0:
            return {}
        for dong in (p.stdout or "").splitlines():
            phan = dong.split(None, 2)
            if len(phan) < 3:
                continue
            try:
                q, cha = int(phan[0]), int(phan[1])
            except ValueError:
                continue
            con.setdefault(cha, []).append(q)
            khoa[q] = "giay:" + phan[2].strip()
    ra: dict[int, str] = {}
    hang, ta = list(con.get(pid, [])), os.getpid()
    while hang:
        q = hang.pop()
        if q in ra or q == ta:                  # tuyệt đối không tự giết mình
            continue
        ra[q] = khoa.get(q, "")
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
        # PHẢI đặt TRƯỚC khi sinh con: subreaper chỉ nhận nuôi những đứa mồ côi
        # SAU khi cờ có hiệu lực. Đặt sau thì đúng ca cần bắt vẫn rơi về `init`.
        # BIẾN TÍN HIỆU KẾT THÚC THÀNH NGOẠI LỆ, đặt TRƯỚC khi sinh con.
        #
        # `SIGHUP` đi cùng vì cùng hình dạng: đóng terminal/ngắt phiên ssh cũng
        # giết ngay mà không chạy dọn. Không có trên Windows nên bọc `suppress`.
        tin_hieu_cu: list[tuple[Any, Any]] = []
        _da_cam: list[Any] = []
        _dang_ket_thuc: list[bool] = []

        def _ket_thuc(so_hieu, _khung):
            # TÍN HIỆU THỨ HAI KHÔNG ĐƯỢC NÉM LẦN NỮA (P1 cross-review `8eca8d4`).
            #
            # Nếu `SIGTERM` thứ hai tới trong lúc đang dọn, handler vẫn còn cắm sẽ
            # ném `BiKetThuc` từ BÊN TRONG khối `except BaseException` — mà ngoại
            # lệ ném ra từ trong một `except` thì chính `except` ấy KHÔNG bắt lại
            # được, nên luồng nhảy thẳng tới `finally` và nhả khoá khi cây chưa
            # dọn xong. Đo được bằng probe bắn hai phát: con còn sống, không bằng
            # chứng. Nên: nhận phát đầu là LÀM NGƠ ngay các phát sau.
            _dang_ket_thuc.append(True)
            for _s2 in _da_cam:
                with contextlib.suppress(OSError, ValueError):
                    signal.signal(_s2, signal.SIG_IGN)
            raise BiKetThuc("tin hieu %d" % so_hieu)

        for _ten in ("SIGTERM", "SIGHUP"):
            _sh = getattr(signal, _ten, None)
            if _sh is not None:
                with contextlib.suppress(OSError, ValueError):
                    tin_hieu_cu.append((_sh, signal.signal(_sh, _ket_thuc)))
                    _da_cam.append(_sh)
        global _CO_SUBREAPER
        _CO_SUBREAPER = _dat_subreaper()
        # Cấp cgroup TRƯỚC khi sinh con; con vào cgroup ngay lúc `fork`.
        global _CGROUP_GATE, _CO_CHE_CACH_LY, _GIET_KHONG_TRON_VEN, _CGROUP_GATE_DA_QUET
        _CGROUP_GATE = _tao_cgroup_gate()
        if _CGROUP_GATE is not None:
            _CO_CHE_CACH_LY = "cgroup2"
        elif os.name == "nt":
            _CO_CHE_CACH_LY = "job-object"
        payload["co_che_cach_ly"] = _CO_CHE_CACH_LY
        payload["moi_noi_kiem_thu"] = _moi_noi_dang_bat()
        if _CGROUP_GATE is not None:
            atexit.register(_don_cgroup_con_sot)
        # CHẶN TÍN HIỆU QUANH QUÃNG SINH CON — không phải bắt nó cho khéo hơn.
        #
        # Đo được trên `8eca8d4`: bắn `SIGTERM` đúng lúc `Popen` đang chạy thì con
        # ĐÃ fork nhưng biến `proc` CHƯA được gán (và có thể chưa kịp vào cgroup),
        # nên nhánh dọn không với tới nó — bằng chứng ghi được mà con vẫn sống.
        # Sweep 14 mốc thời gian: đúng một mốc (0,10s) rơi vào khe ấy.
        #
        # Bắt cho khéo hơn không đóng được khe này: nó là khe GIỮA fork và sổ sách.
        # Chặn thì tín hiệu nằm chờ (pending) tới khi ta đã nhất quán rồi mới nhận
        # — không mất tín hiệu, chỉ hoãn nó vài dòng.
        #
        # Mặt nạ tín hiệu DI TRUYỀN qua `fork`+`exec`, nên con sẽ điếc `SIGTERM`
        # nếu ta không gỡ. Gỡ trong `preexec_fn` (chạy ở CON, sau `fork` trước
        # `exec`) — và vì thế `preexec_fn` phải LUÔN có, kể cả khi không có cgroup.
        mat_na = None
        _bo_chan = [x for x in (getattr(signal, "SIGTERM", None),
                                getattr(signal, "SIGHUP", None)) if x is not None]
        if hasattr(signal, "pthread_sigmask") and _bo_chan:
            with contextlib.suppress(OSError, ValueError):
                mat_na = signal.pthread_sigmask(signal.SIG_BLOCK, set(_bo_chan))

        def _truoc_exec() -> None:
            if mat_na is not None:
                with contextlib.suppress(OSError, ValueError):
                    signal.pthread_sigmask(signal.SIG_SETMASK, mat_na)
            if _CGROUP_GATE is not None:
                _vao_cgroup(_CGROUP_GATE)

        vao_cgroup = None
        if os.name != "nt" and (mat_na is not None or _CGROUP_GATE is not None):
            vao_cgroup = _truoc_exec
        # Khai TRƯỚC khối `try` để nhánh bắt tín hiệu biết con đã sinh hay chưa.
        proc: subprocess.Popen[Any] | None = None

        def _sinh_con(vao: Any) -> subprocess.Popen[Any]:
            return subprocess.Popen(
                payload["command"],
                cwd=root,
                creationflags=creationflags,
                start_new_session=os.name != "nt",
                stdout=output_stream,
                stderr=subprocess.STDOUT,
                preexec_fn=vao,
            )

        try:
            try:
                proc = _sinh_con(vao_cgroup)
            except subprocess.SubprocessError:
                # VÀO CGROUP HỎNG NGAY LÚC `fork`. `preexec_fn` ném thì Python gói
                # lại thành `SubprocessError`, KHÔNG phải `OSError` — đo được, nên
                # khối `except OSError` bên dưới KHÔNG bắt được ca này và nó sẽ
                # thoát ra ngoài, mất luôn tệp bằng chứng.
                #
                # `os.access(W_OK)` lúc tạo cgroup KHÔNG đủ để loại ca này: chạy
                # root thì `access` bỏ qua kiểm quyền, mà `write` vẫn hỏng được vì
                # lý do khác (`EBUSY` do luật "no internal processes", cgroup bị
                # xoá mất giữa chừng). Lại đúng bài "sự CÓ MẶT của một đường không
                # phải KHẢ NĂNG của nó".
                #
                # Bỏ vùng chứa, chạy tiếp bằng đường dự phòng, và KHAI ĐÚNG là
                # `quet-cay` — chạy quét cây mà khai `cgroup2` mới là hỏng thật.
                if vao_cgroup is None:
                    raise
                if _CGROUP_GATE is not None:
                    _don_cgroup(_CGROUP_GATE)
                _CGROUP_GATE = None
                _CO_CHE_CACH_LY = "quet-cay"
                payload["co_che_cach_ly"] = _CO_CHE_CACH_LY
                # Vẫn cần `preexec` để GỠ MẶT NẠ cho con, chỉ bỏ phần vào cgroup.
                def _chi_go_mat_na() -> None:
                    if mat_na is not None:
                        with contextlib.suppress(OSError, ValueError):
                            signal.pthread_sigmask(signal.SIG_SETMASK, mat_na)

                proc = _sinh_con(_chi_go_mat_na if (os.name != "nt" and mat_na is not None) else None)
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
            # SỔ SÁCH ĐÃ NHẤT QUÁN: `proc` có rồi, job/cgroup gắn rồi. Giờ mới
            # nhận tín hiệu đang chờ — nó rơi vào `except BiKetThuc` ngay dưới,
            # nơi `proc` đã dùng được.
            if mat_na is not None:
                with contextlib.suppress(OSError, ValueError):
                    signal.pthread_sigmask(signal.SIG_SETMASK, mat_na)
        except BiKetThuc:
            # TÍN HIỆU RƠI VÀO ĐÚNG QUÃNG SINH CON (P1 cross-review `8eca8d4`).
            #
            # Khối này trước chỉ bắt `OSError`, nên `BiKetThuc` ném ra giữa
            # `Popen` và khối `proc.wait()` sẽ bay thẳng qua cả `except
            # BaseException` lẫn `finally` của khối dưới — hai thứ đó CHƯA vào
            # phạm vi. Đo được: bắn tín hiệu ngay sau khi `_sinh_con` trả về thì
            # không có bằng chứng và con gate sống sót sau khi khoá đã nhả.
            #
            # Con có thể đã sinh hoặc chưa; cả hai đường đều phải dọn.
            if proc is not None:
                with contextlib.suppress(Exception):
                    _terminate_process_tree(proc, None)
            if _CGROUP_GATE is not None:
                if not _giet_cgroup(_CGROUP_GATE):
                    _GIET_KHONG_TRON_VEN = True
                _don_cgroup(_CGROUP_GATE)
                _CGROUP_GATE = None
            for _sh2, _cu2 in tin_hieu_cu:
                with contextlib.suppress(OSError, ValueError, TypeError):
                    signal.signal(_sh2, _cu2)
            output_stream.close()
            _finish(payload, started, status="interrupted",
                    returncode=EXIT_BI_KET_THUC,
                    error="gate interrupted while spawning: BiKetThuc")
            payload["giet_tron_ven"] = not _GIET_KHONG_TRON_VEN
            with contextlib.suppress(OSError):
                _atomic_json(evidence, payload)
            raise SystemExit(EXIT_BI_KET_THUC)
        except OSError as exc:
            output_stream.close()
            # DỌN CGROUP Ở ĐÂY NỮA: nhánh này `return` SỚM, không đi qua khối
            # `finally` bên dưới, nên cgroup vừa cấp sẽ ở lại vĩnh viễn. Đo được
            # bằng ca `case_spawn_error_records_infra_error`: mỗi lượt sinh con
            # hỏng để lại một thư mục cgroup rỗng, tích dần trên runner CI.
            if _CGROUP_GATE is not None:
                _don_cgroup(_CGROUP_GATE)
                _CGROUP_GATE = None
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
            payload["giet_tron_ven"] = not _GIET_KHONG_TRON_VEN
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
            # SIGTERM và Ctrl-C đi CÙNG đường dọn nhưng KHÔNG cùng mã thoát:
            # người đọc bản ghi phải phân biệt được "người gõ Ctrl-C" với "hệ
            # thống bảo dừng".
            returncode = EXIT_BI_KET_THUC if isinstance(exc, BiKetThuc) else EXIT_INTERRUPTED
            _finish(
                payload,
                started,
                status="interrupted",
                returncode=returncode,
                error="gate interrupted: %s" % type(exc).__name__,
            )
            # SỰ THẬT VỀ LƯỢT DỌN đi vào bằng chứng, kể cả khi nó khó nghe.
            payload["giet_tron_ven"] = not _GIET_KHONG_TRON_VEN
            with contextlib.suppress(OSError):
                _atomic_json(evidence, payload)   # ghi bằng chứng TRƯỚC khi ném tiếp
            # Ctrl-C VẪN PHẢI LÀ Ctrl-C với người gõ nó: ném lại nguyên vẹn.
            # Nhưng `SIGTERM` thì phía gọi là MÁY, và máy đọc MÃ THOÁT — ném lại
            # `BiKetThuc` sẽ cho traceback + mã 1, tức bản ghi khai 143 còn shell
            # thấy 1. Hai con số cho cùng một lượt là đúng thứ kho cấm.
            if isinstance(exc, BiKetThuc):
                raise SystemExit(EXIT_BI_KET_THUC)
            raise
        finally:
            # KHÔNG TRẢ HANDLER VỀ MẶC ĐỊNH KHI ĐANG TẮT (P1 tự tìm sau khi nâng ca
            # lên ba phát `SIGTERM`). Với cgroup, lượt dọn xong trong vài mili-giây,
            # nên phát thứ hai/thứ ba tới SAU khi `finally` đã trả `SIG_DFL` —
            # tiến trình chết `-15` dù bằng chứng vừa khai `143`. Hai con số cho
            # cùng một lượt, đúng thứ vế khẳng định mã thoát sinh ra để chặn.
            # Đã tắt rồi thì cứ để `SIG_IGN` tới lúc thoát hẳn.
            if not _dang_ket_thuc:
                for _sh, _cu in tin_hieu_cu:  # trả handler về như cũ
                    with contextlib.suppress(OSError, ValueError, TypeError):
                        signal.signal(_sh, _cu)
            if windows_job is not None:
                windows_job.close()
            output_stream.close()
            # DỌN CẢ TRÊN ĐƯỜNG ĐẠT, không chỉ khi huỷ/quá hạn.
            #
            # Lệnh gate trả 0 rồi bỏ lại một daemon vẫn ghi vào kho thì khoá vẫn
            # bị nhả trong lúc thứ nó bảo vệ còn sống — cùng một lỗi với ca huỷ,
            # chỉ khác lối vào. Đường quét cây không làm nổi việc này (mất cha là
            # mất mỏ neo); cgroup thì làm được, nên đóng luôn.
            if _CGROUP_GATE is not None:
                # ĐẾM THỨ CÒN SÓT rồi mới giết: "gate đạt nhưng bỏ lại 3 tiến
                # trình" là tín hiệu người đọc cần, và giết lặng lẽ thì tín hiệu
                # ấy biến mất. Trên đường huỷ/quá hạn `_terminate_process_tree`
                # đã dọn rồi nên số này là 0 — chỗ nó có nghĩa là đường ĐẠT.
                _sot = _pid_trong_cgroup(_CGROUP_GATE)
                # Không đọc được thì ghi `null`, KHÔNG ghi 0: 0 là lời khai
                # "đã đếm và không có", null là "không đếm được".
                payload["so_sot_da_don"] = None if _sot is None else len(_sot)
                if _giet_cgroup(_CGROUP_GATE):
                    _CGROUP_GATE_DA_QUET = True  # đã đo VÀ xác nhận rỗng
                else:
                    _GIET_KHONG_TRON_VEN = True
                _don_cgroup(_CGROUP_GATE)
                _CGROUP_GATE = None              # atexit ở trên thành vô hại

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

        # SỰ THẬT VỀ LƯỢT DỌN đi vào bằng chứng trên MỌI đường, không riêng
        # đường huỷ/quá hạn — nếu chỉ ghi ở hai đường kia thì đường đạt im lặng,
        # và im lặng lại bị đọc thành "đã dọn sạch".
        #
        # "KHÔNG ĐO ĐƯỢC" KHÁC "ĐÃ SẠCH" (P1 cross-review trên `052d100`).
        # Không có vùng chứa thì đường ĐẠT không hề gọi `_terminate_process_tree`
        # (nó chỉ chạy ở đường huỷ/quá hạn), nên KHÔNG có phép đo nào cả — mà bản
        # trước vẫn ghi `giet_tron_ven: true`. Đo được: `TL_GATE_TAT_CGROUP=1` +
        # một lệnh gate đẻ con tách rời rồi thoát 0 ⇒ bản ghi ĐẠT và TÁI DÙNG
        # ĐƯỢC, trong khi đứa con ghi dấu SAU khi khoá đã nhả.
        #
        # `null` = chưa đo, `false` = đo và thấy sót, `true` = đo và thấy sạch.
        # Ba thứ khác nhau, và gộp cái đầu vào cái cuối chính là lỗi kho đã trả
        # giá nhiều lần. Ai đòi vùng chứa thì dùng `validate --doi-cach-ly`.
        if _GIET_KHONG_TRON_VEN:
            payload["giet_tron_ven"] = False
        elif _CGROUP_GATE_DA_QUET:
            payload["giet_tron_ven"] = True
        else:
            payload["giet_tron_ven"] = None      # KHÔNG ĐO ĐƯỢC
        # FAIL-CLOSE. Trước đây sự thật này chỉ ĐI VÀO BẢN GHI: một lượt rò tiến
        # trình vẫn trả 0 và vẫn tái dùng được. Dọn không trọn vẹn thì lượt gate
        # ấy KHÔNG được tính là đạt.
        if _GIET_KHONG_TRON_VEN and returncode == 0:
            returncode = EXIT_GIET_KHONG_TRON_VEN
            _finish(
                payload,
                started,
                status="fail",
                returncode=returncode,
                error="gate leaked processes: cleanup was not complete",
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
        # FAIL-CLOSE Ở ĐƯỜNG TÁI DÙNG. `giet_tron_ven` VẮNG MẶT là bản ghi cũ hơn
        # trường này, không phải lời khai "đã dọn sạch" — chỉ từ chối khi nó khai
        # THẲNG là false. Vắng mặt và false không được nhập làm một; đó đúng là
        # lỗi "vắng mặt vì sạch" ≠ "vắng mặt vì chưa chạy" mà kho đã trả giá.
        if payload.get("giet_tron_ven") is False:
            mismatches.append("giet_tron_ven")
        # BẰNG CHỨNG SINH RA TỪ LƯỢT CÓ BƠM LỖI KHÔNG PHẢI BẰNG CHỨNG.
        moi_noi = payload.get("moi_noi_kiem_thu") or []
        if any(k in _MOI_NOI_BOM_LOI for k in moi_noi):
            mismatches.append("moi_noi_kiem_thu")
        # AI CẦN VÙNG CHỨA THÌ ĐÒI THẲNG. Không bật mặc định: macOS/FreeBSD không
        # có vùng chứa nào cả, ép cứng ở đây là chặn oan cả một nền hợp lệ.
        if args.doi_cach_ly and payload.get("co_che_cach_ly") not in ("cgroup2", "job-object"):
            mismatches.append("co_che_cach_ly")
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
    validate.add_argument(
        "--doi-cach-ly",
        action="store_true",
        help=("doi bang chung phai sinh ra tu mot VUNG CHUA that (cgroup2/job-object). "
              "Khong bat mac dinh: macOS/FreeBSD khong co vung chua nao, ep cung se chan oan."),
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
