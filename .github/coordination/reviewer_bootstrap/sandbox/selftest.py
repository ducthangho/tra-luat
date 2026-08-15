"""Standalone scheduled counterexamples for the RA-02 sandbox."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import shutil
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import uuid
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from oracle import source_pin  # noqa: E402
from oracle.trusted_inventory import (  # noqa: E402
    REQUIRED_ESCAPE_KEYS,
    REQUIRED_RESOURCE_KEYS,
    SANDBOX_PORTABLE_CONTROL_IDS,
    SANDBOX_TEST_IDS,
)
from sandbox import runner  # noqa: E402

NET_NS_SELF = "/proc/self/ns/net"
NET_NS_INIT = "/proc/1/ns/net"
PARENT_NET_NS_ENV = "RA02_PARENT_NET_NS"
REENTRY_MARKER_ENV = "RA02_DISPOSABLE_FIXTURE_NS"
PRISTINE_LOOPBACK = ("127.0.0.1/8", "::1/128")
CLONE_NEWNET = 0x40000000


class DisposableNamespaceError(RuntimeError):
    """The fixture cannot prove it is inside a network namespace it created."""


def measure_network_namespace(read_link=os.readlink) -> dict[str, object]:
    try:
        current = read_link(NET_NS_SELF)
    except OSError as exc:
        raise DisposableNamespaceError("cannot read %s: %s" % (NET_NS_SELF, exc)) from exc
    try:
        initial = read_link(NET_NS_INIT)
    except OSError:
        initial = None
    return {"current": current, "initial": initial}


def _libc_unshare(flags: int) -> tuple[int, int]:
    import ctypes

    libc = ctypes.CDLL(None, use_errno=True)
    return libc.unshare(flags), ctypes.get_errno()


def create_disposable_network_namespace(read_link=os.readlink, unshare=_libc_unshare) -> dict[str, object]:
    """TỰ tạo namespace mạng và ĐO chuyển dịch của chính tiến trình này.

    Đây là chốt của WP99-R3G3-SPEC-003.  Mọi tín hiệu do TIẾN TRÌNH CHA truyền
    xuống — biến môi trường, đối số, thậm chí `/proc/<ppid>/cmdline` — đều giả
    mạo được, vì cha kiểm soát toàn bộ những gì con quan sát.  Reviewer attempt 3
    đã chứng minh bằng hành vi: đứng trong một `unshare --net --mount` bên ngoài,
    đặt `RA02_DISPOSABLE_FIXTURE_NS=1` và bịa `RA02_PARENT_NET_NS=net:[111]`, bộ
    thử bỏ qua bước tạo namespace của chính nó mà vẫn trả rc 0 với 11/11.

    Không có cách nào chặn việc đó bằng cách kiểm lời khai kỹ hơn.  Cách duy
    nhất là ĐỪNG NHẬN lời khai: gọi `unshare(CLONE_NEWNET)` NGAY TRONG tiến
    trình này rồi đọc lại `/proc/self/ns/net`.  Bản ghi trả về sinh ra tại chỗ,
    không thể thừa kế, và `before != after` là bằng chứng tự quan sát rằng
    namespace đang đứng do chính bộ thử tạo ra.

    `unshare` là tham số để control khả chuyển chạy được trên nền không Linux;
    đường THẬT luôn dùng `_libc_unshare`.
    """
    before = read_link(NET_NS_SELF)
    rc, errno_value = unshare(CLONE_NEWNET)
    if rc != 0:
        raise DisposableNamespaceError(
            "cannot create a disposable network namespace: rc=%d errno=%d" % (rc, errno_value)
        )
    after = read_link(NET_NS_SELF)
    if after == before:
        # rc=0 mà không rời namespace cũ là đúng kiểu "cổng xanh nhờ rc": phải
        # đo hiệu quả THẬT, không tin mã trả về.
        raise DisposableNamespaceError(
            "unshare(CLONE_NEWNET) reported success without moving this process out of %s" % before
        )
    return {
        "before": before,
        "after": after,
        "created_in_process": True,
        "clone_flags": CLONE_NEWNET,
    }


def disposable_namespace_evidence(
    environment: Mapping[str, str],
    read_link=os.readlink,
    creation: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Đo, không tin lời khai.

    Bản trước quyết định bằng biến môi trường `RA02_DISPOSABLE_FIXTURE_NS`: đặt
    sẵn `=1` ở tiến trình cha là bỏ qua `unshare`, rồi fixture nhét địa chỉ
    metadata vào loopback CỦA MÁY và bộ thử vẫn xanh (R2).  Danh tính namespace
    là thứ ĐO được; biến môi trường thì không.

    Bốn phép kiểm đầu vẫn giữ nguyên nhưng chúng chỉ chứng minh "khác namespace
    khởi tạo", KHÔNG chứng minh "do ta tạo": một namespace THỪA KẾ cũng khác
    `/proc/1/ns/net` (SPEC-003).  Ba phép kiểm sau nói về BẢN GHI TẠO sinh tại
    chỗ bởi `create_disposable_network_namespace`, thứ không tiến trình cha nào
    truyền xuống được.
    """
    measured = measure_network_namespace(read_link)
    recorded = environment.get(PARENT_NET_NS_ENV)
    created = creation if isinstance(creation, Mapping) else None
    checks = {
        "parent_namespace_recorded": bool(recorded),
        "initial_namespace_readable": measured["initial"] is not None,
        "differs_from_initial": measured["initial"] is not None
        and measured["current"] != measured["initial"],
        "differs_from_recorded_parent": bool(recorded) and measured["current"] != recorded,
        "namespace_created_in_process": created is not None
        and created.get("created_in_process") is True,
        "creation_left_the_previous_namespace": created is not None
        and created.get("before") != created.get("after"),
        "current_is_the_created_namespace": created is not None
        and measured["current"] == created.get("after"),
    }
    return {
        "measured": measured,
        "recorded_parent": recorded,
        "creation": dict(created) if created is not None else None,
        "checks": checks,
        "disposable": all(checks.values()),
    }


def require_disposable_network_namespace(
    environment: Mapping[str, str] | None = None,
    read_link=os.readlink,
    creation: Mapping[str, object] | None = None,
) -> dict[str, object]:
    evidence = disposable_namespace_evidence(
        os.environ if environment is None else environment, read_link, creation
    )
    if not evidence["disposable"]:
        failed = sorted(name for name, value in evidence["checks"].items() if not value)
        raise DisposableNamespaceError(
            "refusing host-visible network fixtures; failed namespace checks: %s" % failed
        )
    return evidence


def loopback_addresses(run=subprocess.run) -> list[str]:
    proc = run(
        ["ip", "-o", "addr", "show", "dev", "lo"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        raise DisposableNamespaceError(
            "cannot enumerate loopback addresses rc=%d: %s" % (proc.returncode, proc.stderr.strip())
        )
    found = []
    for line in proc.stdout.splitlines():
        parts = line.split()
        for index, token in enumerate(parts):
            if token in ("inet", "inet6") and index + 1 < len(parts):
                found.append(parts[index + 1])
    return sorted(found)


def establish_fixture_baseline(
    environment: Mapping[str, str] | None = None,
    read_link=os.readlink,
    run=subprocess.run,
    create=create_disposable_network_namespace,
) -> dict[str, object]:
    """TẠO namespace, rồi chứng minh MỘT LẦN rằng loopback còn nguyên sơ.

    Thứ tự có tải trọng.  Bước một là `create`: bộ thử KHÔNG hỏi ai xem mình
    đang ở đâu, nó tự tạo namespace và giữ bản ghi chuyển dịch (SPEC-003).  Bước
    hai kiểm lại danh tính đã đo.  Bước ba mới chạm loopback.

    Phép kiểm "nguyên sơ" phụ thuộc THỨ TỰ: lượt chạy thứ nhất hợp lệ tự thêm
    10.99.0.1/32, 169.254.169.254/32 và fd00:ec2::254/128 vào loopback CỦA CHÍNH
    namespace đó, nên nếu gọi lại ở lượt thứ hai nó sẽ tố cáo chính ta và chuỗi
    >=8 lượt chết ở lượt 2.  Đó là lỗi đã ĐO được, không phải giả định.

    Vì vậy: chốt độ nguyên sơ đúng một lần, TRƯỚC vòng lặp, khi chưa ai ghi gì;
    còn danh tính namespace thì vẫn kiểm LẠI mỗi lượt cùng bản ghi tạo, vì nó
    bất biến theo thời gian và chính nó mới là thứ chặn được lời khai môi trường
    giả (R2) lẫn namespace thừa kế (SPEC-003).
    """
    creation = create(read_link)
    namespace = require_disposable_network_namespace(environment, read_link, creation)
    loopback = require_pristine_loopback(run)
    return {
        "namespace": namespace,
        "creation": creation,
        "loopback_before_first_run": loopback,
        "pristine_checked_once_before_any_fixture": True,
    }


def require_pristine_loopback(run=subprocess.run) -> list[str]:
    """Loopback của một namespace mới CHỈ có 127.0.0.1/8 và ::1/128.

    Thấy nhiều hơn nghĩa là ta đang đứng trên loopback dùng chung của ai đó —
    dừng TRƯỚC khi ghi, chứ không dựa vào `finally` để dọn.
    """
    found = loopback_addresses(run)
    extra = [address for address in found if address not in PRISTINE_LOOPBACK]
    if extra:
        raise DisposableNamespaceError(
            "loopback is not a fresh namespace; unexpected addresses present: %s" % extra
        )
    return found


CANDIDATE = textwrap.dedent(
    r'''
    import json, os, pathlib, signal, socket, subprocess, sys, time, urllib.request

    mode = sys.argv[1]

    def emit(value):
        print(json.dumps(value, sort_keys=True), flush=True)

    def blocked(operation):
        try:
            operation()
        except BaseException:
            return True
        return False

    if mode == "healthy":
        emit({"healthy": True})
    elif mode == "credentials":
        hits = {"env": [], "argv": [], "cwd": [], "fd": [], "procfs": []}
        needle = "RA02_SECRET_MARKER_"
        for key, value in os.environ.items():
            if needle in key or needle in value:
                hits["env"].append(key)
        hits["argv"] = [value for value in sys.argv if needle in value]
        if needle in os.getcwd():
            hits["cwd"].append(os.getcwd())
        for fd in pathlib.Path("/proc/self/fd").iterdir():
            try:
                target = os.readlink(fd)
            except OSError:
                continue
            if needle in target:
                hits["fd"].append(fd.name)
        for proc in pathlib.Path("/proc").iterdir():
            if not proc.name.isdigit():
                continue
            for name in ("cmdline", "environ"):
                try:
                    raw = (proc / name).read_bytes().decode("utf-8", "replace")
                except OSError:
                    continue
                if needle in raw:
                    hits["procfs"].append(proc.name + ":" + name)
        emit({"hits": hits, "channels_scanned": sorted(hits)})
    elif mode == "network":
        host, port, metadata4, metadata6, unix_path, dns_name, dns_ip, dns_port = sys.argv[2:10]
        port = int(port); dns_port = int(dns_port)
        def tcp(address, family=socket.AF_INET, target_port=port):
            sock = socket.socket(family, socket.SOCK_STREAM); sock.settimeout(.5)
            try:
                sock.connect((address, target_port)); sock.sendall(b"GET / HTTP/1.0\r\n\r\n"); sock.recv(16)
            finally:
                sock.close()
        def udp(address, target_port=port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); sock.settimeout(.5)
            try:
                sock.sendto(b"probe", (address, target_port)); sock.recvfrom(16)
            finally:
                sock.close()
        def unix_socket():
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); sock.settimeout(.5)
            try:
                sock.connect(unix_path); sock.sendall(b"probe"); sock.recv(16)
            finally:
                sock.close()
        report = {
            "tcp_ipv4": blocked(lambda: tcp(host)),
            "udp_ipv4": blocked(lambda: udp(host)),
            "tcp_ipv6": blocked(lambda: tcp("::1", socket.AF_INET6)),
            "loopback_ipv4": blocked(lambda: tcp("127.0.0.1")),
            "metadata_ipv4": blocked(lambda: tcp(metadata4)),
            "metadata_ipv6": blocked(lambda: tcp(metadata6, socket.AF_INET6)),
            "dns_udp": blocked(lambda: udp(dns_ip, dns_port)),
            "dns_tcp": blocked(lambda: tcp(dns_ip, socket.AF_INET, dns_port)),
            "dns_resolution": blocked(lambda: socket.getaddrinfo(dns_name, 80)),
            "unix_socket_escape": blocked(unix_socket),
            "urllib": blocked(lambda: urllib.request.urlopen("http://%s:%d/" % (host, port), timeout=.5).read()),
            "curl": blocked(lambda: subprocess.run(["curl", "--max-time", "1", "-fsS", "http://%s:%d/" % (host, port)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)),
            "wget": blocked(lambda: subprocess.run(["wget", "-T", "1", "-qO-", "http://%s:%d/" % (host, port)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)),
        }
        emit(report)
    elif mode == "filesystem":
        target = pathlib.Path("/target")
        operations = {
            "create": lambda: (target / "created.txt").write_text("x"),
            "overwrite": lambda: (target / "data.txt").write_text("changed"),
            "rename": lambda: (target / "data.txt").rename(target / "renamed.txt"),
            "delete": lambda: (target / "data.txt").unlink(),
            "chmod": lambda: (target / "data.txt").chmod(0o777),
            "symlink": lambda: (target / "link.txt").symlink_to("/scratch/outside"),
            "hardlink": lambda: os.link(target / "data.txt", target / "hard.txt"),
            "ads": lambda: (target / "data.txt:stream").write_text("x"),
            "relative_escape": lambda: pathlib.Path("../../outside.txt").write_text("x"),
            "absolute_escape": lambda: pathlib.Path("/outside.txt").write_text("x"),
            "unc_escape": lambda: pathlib.Path("//server/share/outside.txt").write_text("x"),
            "device_escape": lambda: pathlib.Path("/dev/null").write_text("x"),
            "preexisting_symlink": lambda: (target / "escape" / "guard.txt").write_text("x"),
        }
        emit({name: blocked(operation) for name, operation in operations.items()})
    elif mode == "retained":
        path = pathlib.Path("/scratch/retained/output.txt")
        path.parent.mkdir(parents=True)
        path.write_bytes(b"measured-retained-bytes\n")
        emit({"locator": "retained/output.txt", "bytes": path.stat().st_size})
    elif mode == "memory":
        values = []
        while True:
            values.append(bytearray(4 * 1024 * 1024))
    elif mode == "cpu":
        while True:
            pass
    elif mode == "pids":
        children = []
        while True:
            try:
                pid = os.fork()
            except OSError:
                break
            if pid == 0:
                os.closerange(0, 3)
                time.sleep(60)
                os._exit(0)
            children.append(pid)
        emit({"forked": len(children)})
    elif mode == "output":
        block = "x" * 8192
        while True:
            print(block, flush=True)
    elif mode == "timeout":
        pid = os.fork()
        if pid == 0:
            os.closerange(0, 3)
            os.setsid()
            time.sleep(60)
            os._exit(0)
        time.sleep(60)
    elif mode == "signal_timeout":
        signal.signal(signal.SIGXCPU, signal.SIG_IGN)
        while True:
            pass
    else:
        raise SystemExit(64)
    '''
).lstrip()


def watchdog_timeout_precedes_cpu_heuristics() -> None:
    record = runner.classify_termination(
        returncode=-9,
        forced="timeout",
        resource_report={"cpu_stat": {"usage_usec": 99_000_000}},
    )
    if record["classification"] != "timeout" or record["termination_source"] != "parent_watchdog":
        raise AssertionError(record)


def cpu_limit_requires_explicit_signal_evidence() -> None:
    killed = runner.classify_termination(
        returncode=-9,
        forced=None,
        resource_report={"cpu_stat": {"usage_usec": 99_000_000}},
    )
    if killed["classification"] == "cpu_limit":
        raise AssertionError(killed)
    signalled = runner.classify_termination(
        returncode=-24,
        forced=None,
        resource_report={"cpu_stat": {"usage_usec": 1}},
    )
    if signalled["classification"] != "cpu_limit" or signalled["limit_evidence"] != "returncode_SIGXCPU":
        raise AssertionError(signalled)


def descendant_checks_treat_zombies_as_gone_with_one_snapshot() -> None:
    observed = {41: "100", 42: "200", 43: "300", 44: "400"}
    snapshots = {
        41: ("Z", "100"),
        42: ("R", "200"),
        43: None,
        44: ("R", "401"),
    }
    calls: list[int] = []
    original = runner._pid_observation

    def fake_observation(pid: int) -> tuple[str, str] | None:
        calls.append(pid)
        return snapshots[pid]

    runner._pid_observation = fake_observation
    try:
        checks = runner._descendant_identity_checks(observed)
    finally:
        runner._pid_observation = original
    expected = {"41": True, "42": False, "43": True, "44": True}
    if checks != expected or calls != [41, 42, 43, 44]:
        raise AssertionError({"checks": checks, "calls": calls})


HOST_INITIAL_NS = "net:[4026531840]"


class _FakeNamespace:
    """Bản đồ `/proc/.../ns/net` giả cùng `unshare` giả.

    Có `unshare` tiêm được thì các control này chạy được trên MỌI nền — kể cả
    nền không có namespace — nên phản chứng SPEC-003 nằm trong bộ khả chuyển
    chứ không chỉ sống trên runner Linux.
    """

    def __init__(self, current: str, initial: str = HOST_INITIAL_NS):
        self._links = {NET_NS_SELF: current, NET_NS_INIT: initial}

    def read_link(self, path: str) -> str:
        return self._links[path]

    def moving_unshare(self, destination: str):
        def _unshare(flags: int) -> tuple[int, int]:
            if flags != CLONE_NEWNET:
                return -1, 22
            self._links[NET_NS_SELF] = destination
            return 0, 0

        return _unshare

    @staticmethod
    def lying_unshare():
        """rc=0 nhưng không đi đâu cả — đúng kiểu cổng xanh nhờ mã trả về."""

        def _unshare(flags: int) -> tuple[int, int]:
            return 0, 0

        return _unshare

    @staticmethod
    def failing_unshare(errno_value: int = 1):
        def _unshare(flags: int) -> tuple[int, int]:
            return -1, errno_value

        return _unshare


def _fresh_creation(before: str = HOST_INITIAL_NS, after: str = "net:[4026532999]") -> dict[str, object]:
    """Bản ghi tạo dựng bằng CHÍNH bộ tạo thật, không phải một dict viết tay."""
    fake = _FakeNamespace(before)
    return create_disposable_network_namespace(fake.read_link, fake.moving_unshare(after))


def disposable_namespace_guard_rejects_inherited_environment_claim() -> None:
    """Phản chứng CHÍNH XÁC của R2: cha đặt sẵn cờ, không hề có namespace mới."""
    host_links = {NET_NS_SELF: "net:[4026531840]", NET_NS_INIT: "net:[4026531840]"}
    hostile_environment = {REENTRY_MARKER_ENV: "1", PARENT_NET_NS_ENV: "net:[4026531840]"}
    evidence = disposable_namespace_evidence(hostile_environment, host_links.__getitem__)
    if evidence["disposable"] is not False:
        raise AssertionError(evidence)
    if evidence["checks"]["differs_from_initial"] is not False:
        raise AssertionError(evidence)
    try:
        require_disposable_network_namespace(hostile_environment, host_links.__getitem__)
    except DisposableNamespaceError as exc:
        if "differs_from_initial" not in str(exc):
            raise AssertionError(str(exc)) from exc
    else:
        raise AssertionError("inherited environment claim was accepted as a disposable namespace")

    # Cánh dương: một namespace THẬT sự mới, do chính ta tạo, phải đi qua.
    fresh_links = {NET_NS_SELF: "net:[4026532999]", NET_NS_INIT: "net:[4026531840]"}
    fresh_environment = {REENTRY_MARKER_ENV: "1", PARENT_NET_NS_ENV: "net:[4026531840]"}
    fresh = require_disposable_network_namespace(
        fresh_environment, fresh_links.__getitem__, _fresh_creation()
    )
    if fresh["disposable"] is not True or fresh["checks"]["differs_from_recorded_parent"] is not True:
        raise AssertionError(fresh)


def host_loopback_fixture_refuses_outside_disposable_namespace() -> None:
    """Không có ghi chép namespace cha, và loopback bẩn: cả hai đều phải chặn TRƯỚC khi ghi."""
    fresh_links = {NET_NS_SELF: "net:[4026532999]", NET_NS_INIT: "net:[4026531840]"}
    try:
        # Bản ghi tạo hợp lệ để phép kiểm CÒN LẠI duy nhất là bản ghi namespace
        # cha: một ca kiểm chỉ có giá trị khi nó đỏ vì đúng lý do của nó.
        require_disposable_network_namespace({}, fresh_links.__getitem__, _fresh_creation())
    except DisposableNamespaceError as exc:
        if "parent_namespace_recorded" not in str(exc):
            raise AssertionError(str(exc)) from exc
    else:
        raise AssertionError("missing parent namespace record was accepted")

    class _Completed:
        def __init__(self, stdout: str):
            self.returncode = 0
            self.stdout = stdout
            self.stderr = ""

    dirty = (
        "1: lo    inet 127.0.0.1/8 scope host lo\\       valid_lft forever\n"
        "1: lo    inet 169.254.169.254/32 scope global lo\\       valid_lft forever\n"
        "1: lo    inet6 ::1/128 scope host \\       valid_lft forever\n"
    )
    try:
        require_pristine_loopback(lambda *a, **k: _Completed(dirty))
    except DisposableNamespaceError as exc:
        if "169.254.169.254/32" not in str(exc):
            raise AssertionError(str(exc)) from exc
    else:
        raise AssertionError("a loopback carrying metadata addresses was treated as pristine")

    clean = (
        "1: lo    inet 127.0.0.1/8 scope host lo\\       valid_lft forever\n"
        "1: lo    inet6 ::1/128 scope host \\       valid_lft forever\n"
    )
    observed = require_pristine_loopback(lambda *a, **k: _Completed(clean))
    if observed != ["127.0.0.1/8", "::1/128"]:
        raise AssertionError(observed)


def fixture_baseline_is_established_once_and_survives_our_own_addresses() -> None:
    """Hồi quy cho lỗi ĐO được: lượt 2 tự tố cáo lượt 1.

    Loopback sau lượt 1 mang chính ba địa chỉ fixture của ta.  Nếu phép kiểm
    nguyên sơ chạy lại mỗi lượt, chuỗi >=8 lượt chết ở lượt 2 với
    `stable_classifications: false` — đúng như đã quan sát tại
    `d8b08e7398b3b660c9c6b7f509e7214bf4b238c5`.
    """

    class _Completed:
        def __init__(self, stdout: str):
            self.returncode = 0
            self.stdout = stdout
            self.stderr = ""

    environment = {REENTRY_MARKER_ENV: "1", PARENT_NET_NS_ENV: "net:[4026531840]"}
    empty_lo = ""
    fake = _FakeNamespace(HOST_INITIAL_NS)

    def _create(read_link):
        return create_disposable_network_namespace(read_link, fake.moving_unshare("net:[4026532999]"))

    baseline = establish_fixture_baseline(
        environment, fake.read_link, lambda *a, **k: _Completed(empty_lo), _create
    )
    if baseline["pristine_checked_once_before_any_fixture"] is not True:
        raise AssertionError(baseline)
    if baseline["loopback_before_first_run"] != []:
        raise AssertionError(baseline)
    # Baseline phải mang bản ghi TẠO, không chỉ mang danh tính đo được.
    if baseline["creation"]["before"] == baseline["creation"]["after"]:
        raise AssertionError(baseline["creation"])

    # Sau lượt 1 loopback mang địa chỉ CỦA TA; baseline vẫn phải dùng lại được.
    after_run_one = (
        "1: lo    inet 127.0.0.1/8 scope host lo\\       valid_lft forever\n"
        "1: lo    inet 10.99.0.1/32 scope global lo\\       valid_lft forever\n"
        "1: lo    inet 169.254.169.254/32 scope global lo\\       valid_lft forever\n"
        "1: lo    inet6 ::1/128 scope host \\       valid_lft forever\n"
        "1: lo    inet6 fd00:ec2::254/128 scope global \\       valid_lft forever\n"
    )
    try:
        require_pristine_loopback(lambda *a, **k: _Completed(after_run_one))
    except DisposableNamespaceError:
        pass
    else:
        raise AssertionError("the pristine check no longer refuses a populated loopback")

    # Danh tính namespace KHÔNG đổi giữa các lượt, nên nó vẫn kiểm lại được —
    # cùng bản ghi tạo của baseline, vì đó mới là thứ chứng minh quyền sở hữu.
    repeat_evidence = require_disposable_network_namespace(
        environment, fake.read_link, baseline["creation"]
    )
    if repeat_evidence["measured"]["current"] != baseline["namespace"]["measured"]["current"]:
        raise AssertionError({"baseline": baseline["namespace"], "repeat": repeat_evidence})

    # Và loopback bẩn TRƯỚC lượt đầu vẫn phải chặn baseline ngay từ đầu.
    dirty_before_start = (
        "1: lo    inet 127.0.0.1/8 scope host lo\\       valid_lft forever\n"
        "1: lo    inet 10.255.255.254/32 scope global lo\\       valid_lft forever\n"
        "1: lo    inet6 ::1/128 scope host \\       valid_lft forever\n"
    )
    dirty_namespace = _FakeNamespace(HOST_INITIAL_NS)
    try:
        establish_fixture_baseline(
            environment,
            dirty_namespace.read_link,
            lambda *a, **k: _Completed(dirty_before_start),
            lambda read_link: create_disposable_network_namespace(
                read_link, dirty_namespace.moving_unshare("net:[4026532998]")
            ),
        )
    except DisposableNamespaceError as exc:
        if "10.255.255.254/32" not in str(exc):
            raise AssertionError(str(exc)) from exc
    else:
        raise AssertionError("a shared, already-populated loopback was accepted as a baseline")


def namespace_guard_requires_a_self_created_namespace() -> None:
    """Phản chứng CHÍNH XÁC của SPEC-003: namespace THỪA KẾ chứ không phải của ta.

    Reviewer attempt 3 đứng trong một `unshare --net --mount` BÊN NGOÀI rồi đặt
    `RA02_DISPOSABLE_FIXTURE_NS=1` cùng `RA02_PARENT_NET_NS=net:[111]` bịa đặt.
    Bộ thử bỏ qua bước tạo namespace của chính nó và vẫn trả rc 0 với 11/11 pass.
    Điểm đau: bốn phép kiểm cũ ĐỀU qua trong tình huống đó — một namespace thừa
    kế thật sự khác `/proc/1/ns/net` và thật sự khác chuỗi cha bịa ra — nên
    không có phép kiểm nào trong số đó bắt được.  Chỉ bản ghi TẠO sinh tại chỗ
    mới phân biệt được "namespace mới" với "namespace của ta".
    """
    inherited = "net:[4026532777]"
    fake = _FakeNamespace(inherited)
    hostile_environment = {REENTRY_MARKER_ENV: "1", PARENT_NET_NS_ENV: "net:[111]"}

    evidence = disposable_namespace_evidence(hostile_environment, fake.read_link)
    legacy = (
        "parent_namespace_recorded",
        "initial_namespace_readable",
        "differs_from_initial",
        "differs_from_recorded_parent",
    )
    if not all(evidence["checks"][name] for name in legacy):
        raise AssertionError("the inherited-namespace exploit no longer reproduces: %r" % evidence)
    if evidence["disposable"] is not False:
        raise AssertionError(evidence)
    try:
        require_disposable_network_namespace(hostile_environment, fake.read_link)
    except DisposableNamespaceError as exc:
        for needle in (
            "namespace_created_in_process",
            "creation_left_the_previous_namespace",
            "current_is_the_created_namespace",
        ):
            if needle not in str(exc):
                raise AssertionError("%r absent from %s" % (needle, exc)) from exc
    else:
        raise AssertionError("an inherited network namespace was accepted as self-created")

    # Cánh dương: tự tạo thì đi qua.
    creator = _FakeNamespace(HOST_INITIAL_NS)
    creation = create_disposable_network_namespace(
        creator.read_link, creator.moving_unshare("net:[4026532999]")
    )
    if creation["created_in_process"] is not True or creation["before"] == creation["after"]:
        raise AssertionError(creation)
    accepted = require_disposable_network_namespace(
        {PARENT_NET_NS_ENV: HOST_INITIAL_NS}, creator.read_link, creation
    )
    if accepted["disposable"] is not True:
        raise AssertionError(accepted)

    # `rc=0` mà không rời namespace cũ là cổng xanh bị lừa — phải chết.
    liar = _FakeNamespace(HOST_INITIAL_NS)
    try:
        create_disposable_network_namespace(liar.read_link, liar.lying_unshare())
    except DisposableNamespaceError as exc:
        if "without moving this process" not in str(exc):
            raise AssertionError(str(exc)) from exc
    else:
        raise AssertionError("unshare rc=0 without a namespace change was accepted")

    # Syscall hỏng phải nổi lên bằng lỗi CÓ TÊN, không phải một baseline im lặng.
    broken = _FakeNamespace(HOST_INITIAL_NS)
    try:
        create_disposable_network_namespace(broken.read_link, broken.failing_unshare(1))
    except DisposableNamespaceError as exc:
        if "cannot create a disposable network namespace" not in str(exc):
            raise AssertionError(str(exc)) from exc
    else:
        raise AssertionError("a failed unshare was treated as a disposable namespace")

    # Bản ghi tạo THẬT nhưng của một namespace khác cũng không cứu được: quyền sở
    # hữu phải nói về namespace ĐANG ĐỨNG, không phải về một lần tạo nào đó.
    elsewhere = _FakeNamespace("net:[4026532888]")
    mismatched = disposable_namespace_evidence(
        {PARENT_NET_NS_ENV: HOST_INITIAL_NS}, elsewhere.read_link, creation
    )
    if mismatched["checks"]["current_is_the_created_namespace"] is not False:
        raise AssertionError(mismatched)
    if mismatched["disposable"] is not False:
        raise AssertionError(mismatched)


class SocketFixture:
    def __init__(self, family: int, address: str, port: int, socktype: int):
        self.family = family
        self.socktype = socktype
        self.socket = socket.socket(family, socktype)
        if family == socket.AF_INET6:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((address, port))
        self.address = self.socket.getsockname()
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self._serve, daemon=True)

    def start(self) -> None:
        if self.socktype == socket.SOCK_STREAM:
            self.socket.listen(16)
        self.socket.settimeout(.1)
        self.thread.start()

    def _serve(self) -> None:
        while not self.stop.is_set():
            try:
                if self.socktype == socket.SOCK_STREAM:
                    connection, _peer = self.socket.accept()
                    with connection:
                        connection.settimeout(.2)
                        try:
                            connection.recv(1024)
                        except OSError:
                            pass
                        connection.sendall(b"HTTP/1.0 200 OK\r\nContent-Length: 2\r\n\r\nok")
                else:
                    data, peer = self.socket.recvfrom(1024)
                    self.socket.sendto(b"ok" if data else b"empty", peer)
            except (socket.timeout, OSError):
                continue

    def close(self) -> None:
        self.stop.set()
        self.socket.close()
        self.thread.join(timeout=1)


class UnixFixture:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(str(path))
        self.socket.listen(8)
        self.socket.settimeout(.1)
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self._serve, daemon=True)

    def start(self) -> None:
        self.thread.start()

    def _serve(self) -> None:
        while not self.stop.is_set():
            try:
                connection, _peer = self.socket.accept()
                with connection:
                    connection.recv(32)
                    connection.sendall(b"ok")
            except (socket.timeout, OSError):
                continue

    def close(self) -> None:
        self.stop.set()
        self.socket.close()
        self.thread.join(timeout=1)


class DnsFixture:
    def __init__(self, address: str, port: int):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for item in (self.udp, self.tcp):
            item.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            item.bind((address, port))
            item.settimeout(.1)
        self.tcp.listen(8)
        self.stop = threading.Event()
        self.threads = [
            threading.Thread(target=self._serve_udp, daemon=True),
            threading.Thread(target=self._serve_tcp, daemon=True),
        ]

    @staticmethod
    def response(query: bytes) -> bytes:
        if len(query) < 12:
            return b""
        offset = 12
        while offset < len(query) and query[offset] != 0:
            offset += 1 + query[offset]
        question = query[12 : min(len(query), offset + 5)]
        header = query[:2] + b"\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"
        answer = b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x01\x00\x04\x0a\x63\x00\x02"
        return header + question + answer

    def start(self) -> None:
        for thread in self.threads:
            thread.start()

    def _serve_udp(self) -> None:
        while not self.stop.is_set():
            try:
                query, peer = self.udp.recvfrom(2048)
                self.udp.sendto(self.response(query), peer)
            except (socket.timeout, OSError):
                continue

    def _serve_tcp(self) -> None:
        while not self.stop.is_set():
            try:
                connection, _peer = self.tcp.accept()
                with connection:
                    connection.settimeout(.5)
                    size = connection.recv(2)
                    if len(size) != 2:
                        continue
                    query = connection.recv(struct.unpack("!H", size)[0])
                    response = self.response(query)
                    connection.sendall(struct.pack("!H", len(response)) + response)
            except (socket.timeout, OSError):
                continue

    def close(self) -> None:
        self.stop.set()
        self.udp.close()
        self.tcp.close()
        for thread in self.threads:
            thread.join(timeout=1)


def _outside_controls(host: str, port: int, metadata4: str, metadata6: str, unix_path: pathlib.Path, dns_port: int) -> dict[str, bool]:
    def tcp(address: str, family: int = socket.AF_INET, target_port: int = port) -> bool:
        try:
            with socket.socket(family, socket.SOCK_STREAM) as item:
                item.settimeout(.8)
                item.connect((address, target_port))
                item.sendall(b"GET / HTTP/1.0\r\n\r\n")
                return bool(item.recv(64))
        except OSError:
            return False

    def udp(address: str, target_port: int = port) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as item:
                item.settimeout(.8)
                item.sendto(b"probe", (address, target_port))
                item.recvfrom(16)
                return True
        except OSError:
            return False

    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as item:
            item.settimeout(.8)
            item.connect(str(unix_path))
            item.sendall(b"probe")
            unix_ok = item.recv(16) == b"ok"
    except OSError:
        unix_ok = False
    url = "http://%s:%d/" % (host, port)
    return {
        "tcp_ipv4": tcp(host),
        "udp_ipv4": udp(host),
        "tcp_ipv6": tcp("::1", socket.AF_INET6),
        "loopback": tcp("127.0.0.1"),
        "metadata_ipv4": tcp(metadata4),
        "metadata_ipv6": tcp(metadata6, socket.AF_INET6),
        "dns_udp": udp(metadata4, dns_port),
        "dns_tcp": tcp(metadata4, socket.AF_INET, dns_port),
        "unix_socket": unix_ok,
        "curl": shutil.which("curl") is not None and subprocess.run(["curl", "--max-time", "1", "-fsS", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0,
        "wget": shutil.which("wget") is not None and subprocess.run(["wget", "-T", "1", "-qO-", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0,
    }


def _parse_protocol(result: runner.SandboxResult) -> object:
    try:
        return json.loads(result.stdout.decode("utf-8"))
    except (UnicodeError, ValueError):
        return None


def _result_record(test_id: str, expected: str, result: runner.SandboxResult, markers: Sequence[str]) -> dict[str, object]:
    serialized = json.dumps(result.as_dict(), sort_keys=True)
    leaks = [marker for marker in markers if marker in serialized]
    invariant_checks = {
        "classification_matches": result.classification == expected,
        "cgroup_empty": result.cleanup.get("cgroup_empty") is True,
        "descendants_gone": result.cleanup.get("descendants_gone") is True,
        "cgroup_removed": result.cleanup.get("cgroup_removed") is True,
        "scratch_removed": result.cleanup.get("scratch_removed") is True,
        "credential_markers_absent": not leaks,
    }
    failed_invariants = sorted(name for name, value in invariant_checks.items() if value is not True)
    passed = not failed_invariants
    return {
        "test_id": test_id,
        "status": "passed" if passed else "failed",
        "passed": passed,
        "expected_classification": expected,
        "actual_classification": result.classification,
        "rc": result.returncode,
        "credential_marker_leaks": leaks,
        "invariant_checks": invariant_checks,
        "failed_invariants": failed_invariants,
        "protocol": _parse_protocol(result),
        "result": result.as_dict(),
    }


def _run_case(target: pathlib.Path, scratch: pathlib.Path, mode: str, *args: str, **limits: object) -> runner.SandboxResult:
    config = runner.SandboxConfig(
        target_root=str(target),
        scratch_root=str(scratch),
        command=["/usr/bin/python3", "/target/candidate.py", mode, *args],
        **limits,
    )
    return runner.run(config)


def _full_once(
    repo_root: str,
    candidate_head: str,
    dispatcher_pin: str,
    run_index: int,
    fixture_baseline: Mapping[str, object],
) -> dict[str, object]:
    binding = source_pin.verify(repo_root, candidate_head, dispatcher_pin)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records: dict[str, dict[str, object]] = {}
    fixtures: list[object] = []
    marker_names = (
        "ENV",
        "ARGV",
        "CWD",
        "FD",
        "PROCFS",
        "ALIAS_GITHUB",
        "ALIAS_CLOUD",
        "ALIAS_MODEL",
        "ALIAS_REGISTRY",
        "ALIAS_CREDENTIAL",
    )
    markers = ["RA02_SECRET_MARKER_%s_%s" % (name, uuid.uuid4().hex) for name in marker_names]
    alias_markers = {
        "RA02_GITHUB_TOKEN_ALIAS": markers[5],
        "RA02_CLOUD_SECRET_ALIAS": markers[6],
        "RA02_MODEL_API_KEY_ALIAS": markers[7],
        "RA02_REGISTRY_TOKEN_ALIAS": markers[8],
        "RA02_CREDENTIAL_ALIAS": markers[9],
    }
    with tempfile.TemporaryDirectory(prefix="ra02-suite-", dir="/tmp") as tmp:
        root = pathlib.Path(tmp)
        target = root / "target"
        scratch = root / "scratch"
        target.mkdir()
        scratch.mkdir()
        (target / "candidate.py").write_text(CANDIDATE, encoding="utf-8")
        (target / "data.txt").write_bytes(b"immutable-target\n")
        guard = root / "guard.txt"
        guard.write_bytes(b"guard\n")
        (target / "escape").symlink_to(root)
        before = (target / "data.txt").read_bytes(), guard.read_bytes()

        def record(test_id: str, expected: str, result: runner.SandboxResult) -> runner.SandboxResult:
            records[test_id] = _result_record(test_id, expected, result, markers)
            return result

        record("healthy_positive_control", "ok", _run_case(target, scratch, "healthy"))

        controlled_environment = {"RA02_SECRET_MARKER_ENV": markers[0], **alias_markers}
        saved = {key: os.environ.get(key) for key in controlled_environment}
        os.environ.update(controlled_environment)
        cwd = root / markers[2]
        cwd.mkdir()
        descriptor_path = root / markers[3]
        descriptor_path.write_text("control", encoding="utf-8")
        descriptor = descriptor_path.open("rb")
        helper_env = dict(os.environ)
        helper_env["RA02_SECRET_MARKER_PROCFS"] = markers[4]
        helper = subprocess.Popen(
            [sys.executable, "-c", "import time; print('ready',flush=True); time.sleep(30)", markers[1]],
            cwd=cwd,
            env=helper_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        try:
            ready = helper.stdout is not None and helper.stdout.readline().strip() == b"ready"
            controls = {
                "env": os.environ.get("RA02_SECRET_MARKER_ENV") == markers[0],
                "argv": markers[1].encode() in pathlib.Path("/proc/%d/cmdline" % helper.pid).read_bytes(),
                "cwd": markers[2] in os.readlink("/proc/%d/cwd" % helper.pid),
                "fd": markers[3] in os.readlink("/proc/self/fd/%d" % descriptor.fileno()),
                "procfs": markers[4].encode() in pathlib.Path("/proc/%d/environ" % helper.pid).read_bytes(),
                "alias_github": os.environ.get("RA02_GITHUB_TOKEN_ALIAS") == markers[5],
                "alias_cloud": os.environ.get("RA02_CLOUD_SECRET_ALIAS") == markers[6],
                "alias_model": os.environ.get("RA02_MODEL_API_KEY_ALIAS") == markers[7],
                "alias_registry": os.environ.get("RA02_REGISTRY_TOKEN_ALIAS") == markers[8],
                "alias_credential": os.environ.get("RA02_CREDENTIAL_ALIAS") == markers[9],
                "helper_ready": ready,
            }
            credential = record("credential_channels", "ok", _run_case(target, scratch, "credentials"))
            records["credential_channels"]["outside_positive_controls"] = controls
            protocol = _parse_protocol(credential)
            hits = protocol.get("hits") if isinstance(protocol, Mapping) else None
            if not all(controls.values()) or not isinstance(hits, Mapping) or any(hits.get(name) for name in ("env", "argv", "cwd", "fd", "procfs")):
                records["credential_channels"]["passed"] = False
                records["credential_channels"]["status"] = "failed"
        finally:
            helper.terminate()
            helper.wait(timeout=2)
            descriptor.close()
            for key, previous in saved.items():
                if previous is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = previous

        # Chốt R2: chỉ được chạm vào loopback SAU khi chứng minh được namespace
        # này do chính ta tạo.  Không có `finally` nào cứu được máy chủ nếu ta đã
        # ghi nhầm chỗ.  Danh tính namespace kiểm LẠI mỗi lượt; còn độ nguyên sơ
        # của loopback là bằng chứng chốt MỘT LẦN trước vòng lặp (xem
        # `establish_fixture_baseline`) vì từ lượt 2 trở đi loopback mang đúng
        # các địa chỉ mà chính ta đã đặt ở lượt 1.
        namespace_evidence = require_disposable_network_namespace(
            creation=fixture_baseline.get("creation")
        )
        if fixture_baseline.get("pristine_checked_once_before_any_fixture") is not True:
            raise DisposableNamespaceError(
                "fixture baseline was not established before the repeat loop"
            )
        if fixture_baseline.get("namespace", {}).get("measured", {}).get("current") != namespace_evidence[
            "measured"
        ]["current"]:
            raise DisposableNamespaceError(
                "network namespace changed between the baseline and this run"
            )
        loopback_before = fixture_baseline["loopback_before_first_run"]
        host, metadata4, metadata6, port, dns_port = "10.99.0.1", "169.254.169.254", "fd00:ec2::254", 43861, 53
        for command in (
            ["ip", "link", "set", "lo", "up"],
            ["ip", "addr", "replace", host + "/32", "dev", "lo"],
            ["ip", "addr", "replace", metadata4 + "/32", "dev", "lo"],
            ["ip", "-6", "addr", "replace", metadata6 + "/128", "dev", "lo"],
        ):
            completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed.returncode != 0:
                raise RuntimeError("disposable network fixture setup failed rc=%d: %s" % (completed.returncode, completed.stderr.decode("utf-8", "replace")))
        for fixture in (
            SocketFixture(socket.AF_INET, "0.0.0.0", port, socket.SOCK_STREAM),
            SocketFixture(socket.AF_INET, "0.0.0.0", port, socket.SOCK_DGRAM),
            SocketFixture(socket.AF_INET6, "::", port, socket.SOCK_STREAM),
        ):
            fixture.start()
            fixtures.append(fixture)
        unix_fixture = UnixFixture(root / "outside-scratch.sock")
        unix_fixture.start()
        fixtures.append(unix_fixture)
        dns_fixture = DnsFixture(metadata4, dns_port)
        dns_fixture.start()
        fixtures.append(dns_fixture)
        controls = _outside_controls(host, port, metadata4, metadata6, unix_fixture.path, dns_port)
        network = record(
            "network_dns_loopback_metadata_unix",
            "ok",
            _run_case(
                target,
                scratch,
                "network",
                host,
                str(port),
                metadata4,
                metadata6,
                str(unix_fixture.path),
                "fixture.ra02.invalid",
                metadata4,
                str(dns_port),
                resolv_conf_text="nameserver %s\noptions attempts:1 timeout:1\n" % metadata4,
            ),
        )
        records["network_dns_loopback_metadata_unix"]["outside_positive_controls"] = controls
        records["network_dns_loopback_metadata_unix"]["disposable_namespace_evidence"] = namespace_evidence
        records["network_dns_loopback_metadata_unix"]["loopback_before_fixture"] = loopback_before
        records["network_dns_loopback_metadata_unix"]["fixture_baseline"] = dict(fixture_baseline)
        protocol = _parse_protocol(network)
        if not all(controls.values()) or not isinstance(protocol, Mapping) or not protocol or not all(value is True for value in protocol.values()):
            records["network_dns_loopback_metadata_unix"]["passed"] = False
            records["network_dns_loopback_metadata_unix"]["status"] = "failed"

        filesystem = record("target_readonly_and_path_escapes", "ok", _run_case(target, scratch, "filesystem"))
        protocol = _parse_protocol(filesystem)
        if not isinstance(protocol, Mapping) or not protocol or not all(value is True for value in protocol.values()) or ((target / "data.txt").read_bytes(), guard.read_bytes()) != before:
            records["target_readonly_and_path_escapes"]["passed"] = False
            records["target_readonly_and_path_escapes"]["status"] = "failed"

        retained = record(
            "retained_output_integrity",
            "ok",
            _run_case(target, scratch, "retained", retained_output_paths=("retained/output.txt",)),
        )
        retained_bytes = retained.retained_outputs.get("retained/output.txt")
        records["retained_output_integrity"]["observed_retained_sha256"] = hashlib.sha256(retained_bytes or b"").hexdigest()
        records["retained_output_integrity"]["observed_retained_bytes"] = len(retained_bytes or b"")
        if retained_bytes != b"measured-retained-bytes\n":
            records["retained_output_integrity"]["passed"] = False
            records["retained_output_integrity"]["status"] = "failed"

        record("memory_hog", "memory_limit", _run_case(target, scratch, "memory", memory_bytes=48 * 1024 * 1024, timeout_seconds=5))
        record("cpu_busy_loop", "cpu_limit", _run_case(target, scratch, "cpu", cpu_seconds=1, timeout_seconds=12))
        record("pid_fork_bomb", "pid_limit", _run_case(target, scratch, "pids", pids_max=8, timeout_seconds=12, cpu_seconds=20))
        record("stdout_flood", "output_limit", _run_case(target, scratch, "output", output_bytes=65_536, timeout_seconds=4))
        record("timeout_and_descendant_cleanup", "timeout", _run_case(target, scratch, "timeout", timeout_seconds=2, cpu_seconds=10))
        record("signal_handler_timeout", "timeout", _run_case(target, scratch, "signal_timeout", timeout_seconds=2, cpu_seconds=10))

        for fixture in fixtures:
            fixture.close()

    ordered = []
    for test_id in SANDBOX_TEST_IDS:
        item = records.get(test_id)
        if item is None:
            item = {
                "test_id": test_id,
                "status": "not_run",
                "passed": False,
                "reason": "scheduled test produced no record",
                "rc": None,
            }
        ordered.append(item)
    executed = sum(item["status"] in ("passed", "failed") for item in ordered)
    passed = sum(item["status"] == "passed" for item in ordered)
    failed = sum(item["status"] == "failed" for item in ordered)
    skipped = sum(item["status"] == "skipped" for item in ordered)
    not_run = sum(item["status"] == "not_run" for item in ordered)

    by_id = {item["test_id"]: item for item in ordered}
    network_protocol = by_id["network_dns_loopback_metadata_unix"].get("protocol", {})
    network_controls = by_id["network_dns_loopback_metadata_unix"].get("outside_positive_controls", {})
    filesystem_protocol = by_id["target_readonly_and_path_escapes"].get("protocol", {})
    credential_protocol = by_id["credential_channels"].get("protocol", {})
    escape = {
        "network": {"test_id": "network_dns_loopback_metadata_unix", "rc": by_id["network_dns_loopback_metadata_unix"].get("rc"), "passed": by_id["network_dns_loopback_metadata_unix"]["passed"], "evidence": {"outside": network_controls, "blocked": {key: network_protocol.get(key) for key in ("tcp_ipv4", "udp_ipv4", "tcp_ipv6", "urllib", "curl", "wget", "unix_socket_escape")}}},
        "dns": {"test_id": "network_dns_loopback_metadata_unix", "rc": by_id["network_dns_loopback_metadata_unix"].get("rc"), "passed": by_id["network_dns_loopback_metadata_unix"]["passed"], "evidence": {key: network_protocol.get(key) for key in ("dns_udp", "dns_tcp", "dns_resolution")}},
        "loopback": {"test_id": "network_dns_loopback_metadata_unix", "rc": by_id["network_dns_loopback_metadata_unix"].get("rc"), "passed": by_id["network_dns_loopback_metadata_unix"]["passed"], "evidence": {key: network_protocol.get(key) for key in ("loopback_ipv4", "tcp_ipv6")}},
        "metadata": {"test_id": "network_dns_loopback_metadata_unix", "rc": by_id["network_dns_loopback_metadata_unix"].get("rc"), "passed": by_id["network_dns_loopback_metadata_unix"]["passed"], "evidence": {key: network_protocol.get(key) for key in ("metadata_ipv4", "metadata_ipv6")}},
        "target_write": {"test_id": "target_readonly_and_path_escapes", "rc": by_id["target_readonly_and_path_escapes"].get("rc"), "passed": by_id["target_readonly_and_path_escapes"]["passed"], "evidence": {key: filesystem_protocol.get(key) for key in ("create", "overwrite", "rename", "delete", "chmod", "symlink", "hardlink", "ads")}},
        "path_escape": {"test_id": "target_readonly_and_path_escapes", "rc": by_id["target_readonly_and_path_escapes"].get("rc"), "passed": by_id["target_readonly_and_path_escapes"]["passed"], "evidence": {key: filesystem_protocol.get(key) for key in ("relative_escape", "absolute_escape", "unc_escape", "device_escape", "preexisting_symlink")}},
        "fd_leak": {"test_id": "credential_channels", "rc": by_id["credential_channels"].get("rc"), "passed": by_id["credential_channels"]["passed"], "evidence": {"hits": credential_protocol.get("hits") if isinstance(credential_protocol, Mapping) else None, "boundary_descriptors": by_id["credential_channels"].get("result", {}).get("boundary", {}).get("descriptor_inventory")}},
    }
    resource_map = {
        "cpu": "cpu_busy_loop",
        "memory": "memory_hog",
        "pid": "pid_fork_bomb",
        "output": "stdout_flood",
        "timeout": "timeout_and_descendant_cleanup",
        "descendant_cleanup": "timeout_and_descendant_cleanup",
    }
    resources = {}
    for key, test_id in resource_map.items():
        item = by_id[test_id]
        result = item.get("result", {})
        evidence = result.get("cleanup") if key == "descendant_cleanup" else {"termination": result.get("termination"), "resource_report": result.get("resource_report")}
        resources[key] = {"test_id": test_id, "rc": item.get("rc"), "passed": item["passed"], "evidence": evidence}
    class_keys_exact = tuple(escape) == REQUIRED_ESCAPE_KEYS and tuple(resources) == REQUIRED_RESOURCE_KEYS
    all_classes = list(escape.values()) + list(resources.values())
    report = {
        "schema_version": 1,
        "run_id": "ra02-sandbox-%02d-%s" % (run_index, uuid.uuid4().hex),
        "started_at": started,
        "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "candidate_head": candidate_head,
        "candidate_source_binding": binding,
        "scheduled_test_ids": list(SANDBOX_TEST_IDS),
        "scheduled_total": len(SANDBOX_TEST_IDS),
        "executed": executed,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "not_run": not_run,
        "tests": ordered,
        "required_counterexamples": {
            "sandbox_escape_classes": escape,
            "resource_classes": resources,
        },
        "required_class_keys_exact": class_keys_exact,
        "ok": (
            len(SANDBOX_TEST_IDS) > 0
            and executed == len(SANDBOX_TEST_IDS)
            and passed == len(SANDBOX_TEST_IDS)
            and failed == skipped == not_run == 0
            and class_keys_exact
            and all(item["passed"] is True and item["rc"] is not None and item["evidence"] for item in all_classes)
        ),
    }
    encoded = json.dumps(report, ensure_ascii=False, sort_keys=True)
    if any(marker in encoded for marker in markers):
        report["ok"] = False
        report["report_credential_marker_leak"] = True
    return report


PORTABLE_CONTROLS = (
    watchdog_timeout_precedes_cpu_heuristics,
    cpu_limit_requires_explicit_signal_evidence,
    descendant_checks_treat_zombies_as_gone_with_one_snapshot,
    disposable_namespace_guard_rejects_inherited_environment_claim,
    host_loopback_fixture_refuses_outside_disposable_namespace,
    fixture_baseline_is_established_once_and_survives_our_own_addresses,
    namespace_guard_requires_a_self_created_namespace,
)


def _run_portable_controls() -> list[dict[str, object]]:
    declared = tuple(control.__name__ for control in PORTABLE_CONTROLS)
    if declared != SANDBOX_PORTABLE_CONTROL_IDS:
        raise RuntimeError(
            "portable control registry drift: declared=%s callable=%s"
            % (list(SANDBOX_PORTABLE_CONTROL_IDS), list(declared))
        )
    records = []
    for control in PORTABLE_CONTROLS:
        try:
            control()
        except Exception as exc:
            records.append(
                {
                    "test_id": control.__name__,
                    "status": "failed",
                    "error": {"name": type(exc).__name__, "message": str(exc)},
                }
            )
        else:
            records.append({"test_id": control.__name__, "status": "passed"})
    return records


def _platform_report(exc: Exception) -> dict[str, object]:
    portable_controls = _run_portable_controls()
    return {
        "schema_version": 1,
        "ok": False,
        "error": {"name": "PlatformUnsupported", "message": str(exc)},
        "scheduled_test_ids": list(SANDBOX_TEST_IDS),
        "scheduled_total": len(SANDBOX_TEST_IDS),
        "executed": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "not_run": len(SANDBOX_TEST_IDS),
        "portable_controls": portable_controls,
        "portable_controls_passed": sum(
            item["status"] == "passed" for item in portable_controls
        ),
        "portable_controls_total": len(portable_controls),
    }


def _enter_disposable_fixture_namespace(
    repo_root: str,
    candidate_head: str,
    dispatcher_pin: str,
    repeat: int,
    output: str | None,
) -> None:
    bootstrap = os.environ.get("RA02_BOOTSTRAP_PATH")
    if not bootstrap:
        raise source_pin.SourcePinError("external bootstrap path is absent")
    env = dict(os.environ)
    # Cờ này CHỈ đánh dấu "đã re-exec một lần" để khỏi lặp vô hạn; nó KHÔNG phải
    # bằng chứng cách ly.  Danh tính namespace cha được ghi lại làm quan sát bổ
    # sung; quyền sở hữu namespace do `create_disposable_network_namespace` tự
    # đo trong tiến trình, không do hai biến này khai (SPEC-003).
    env[REENTRY_MARKER_ENV] = "1"
    env[PARENT_NET_NS_ENV] = str(measure_network_namespace()["current"])
    command = [
        "unshare",
        "--fork",
        "--kill-child=KILL",
        "--net",
        "--mount",
        sys.executable,
        bootstrap,
        "run-sandbox",
        "--repo-root",
        repo_root,
        "--candidate-head",
        candidate_head,
        "--pin",
        dispatcher_pin,
        "--repeat",
        str(repeat),
    ]
    if output:
        command.extend(("--output", output))
    os.execvpe(command[0], command, env)


def _unit() -> int:
    """Chạy các control khả chuyển và NÓI RÕ chúng không đo ID nào của bộ đầy đủ.

    `3/3` cộng rc=0 từng là toàn bộ kết quả của lần gọi mặc định, trong khi không
    một ID nào trong `SANDBOX_TEST_IDS` được chạm tới — cổng xanh nhờ rc=0 đúng
    kiểu bị lừa.  Mẫu số của bộ đầy đủ nay được in ra cùng chỗ.
    """
    tests = PORTABLE_CONTROLS
    passed = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            print("[FAIL] %s -- %s: %s" % (test.__name__, type(exc).__name__, exc))
        else:
            passed += 1
            print("[OK] %s" % test.__name__)
    accounting = {
        "schema_version": 1,
        "mode": "portable_controls_only",
        "portable_controls_passed": passed,
        "portable_controls_total": len(tests),
        "sandbox_scheduled_test_ids": list(SANDBOX_TEST_IDS),
        "sandbox_scheduled_total": len(SANDBOX_TEST_IDS),
        "sandbox_executed": 0,
        "sandbox_passed": 0,
        "sandbox_failed": 0,
        "sandbox_skipped": 0,
        "sandbox_not_run": len(SANDBOX_TEST_IDS),
        "sandbox_suite_ok": False,
        "full_suite_command": "source_pin.py run-sandbox --repo-root ... --candidate-head ... --pin ...",
    }
    print(json.dumps(accounting, ensure_ascii=False, sort_keys=True))
    print(
        "== ra02 sandbox portable controls %d/%d · sandbox scheduled %d executed 0 not_run %d — NOT the full suite =="
        % (passed, len(tests), len(SANDBOX_TEST_IDS), len(SANDBOX_TEST_IDS))
    )
    return 0 if passed == len(tests) and len(tests) > 0 else 1


def _refuse_default_invocation() -> int:
    report = {
        "schema_version": 1,
        "ok": False,
        "error": {
            "name": "NoMeasurementRequested",
            "message": (
                "a bare invocation measures none of the scheduled sandbox test IDs; "
                "pass --unit for the portable controls or --full for the measured suite"
            ),
        },
        "scheduled_test_ids": list(SANDBOX_TEST_IDS),
        "scheduled_total": len(SANDBOX_TEST_IDS),
        "executed": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "not_run": len(SANDBOX_TEST_IDS),
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 2


def _exception_run(candidate_head: str, run_index: int, exc: Exception) -> dict[str, object]:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tests = [
        {
            "test_id": test_id,
            "status": "not_run",
            "passed": False,
            "reason": "%s: %s" % (type(exc).__name__, exc),
            "rc": None,
        }
        for test_id in SANDBOX_TEST_IDS
    ]
    return {
        "schema_version": 1,
        "run_id": "ra02-sandbox-%02d-error" % run_index,
        "started_at": now,
        "completed_at": now,
        "candidate_head": candidate_head,
        "scheduled_test_ids": list(SANDBOX_TEST_IDS),
        "scheduled_total": len(SANDBOX_TEST_IDS),
        "executed": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "not_run": len(SANDBOX_TEST_IDS),
        "tests": tests,
        "error": {"name": type(exc).__name__, "message": str(exc)},
        "ok": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--unit", action="store_true")
    parser.add_argument("--repo-root")
    parser.add_argument("--candidate-head")
    parser.add_argument("--dispatcher-pin")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    if not args.full:
        return _unit() if args.unit else _refuse_default_invocation()
    if not args.repo_root or not args.candidate_head or not args.dispatcher_pin or args.repeat < 1:
        parser.error("--full requires --repo-root, --candidate-head, --dispatcher-pin, and positive --repeat")
    bootstrap = os.environ.get("RA02_BOOTSTRAP_PATH")
    candidate_bootstrap = pathlib.Path(args.repo_root).resolve() / pathlib.PurePosixPath(
        source_pin.SOURCE_PIN_RELATIVE
    )
    externally_verified = (
        os.environ.get("RA02_SOURCE_PIN_VERIFIED") == "1"
        and bootstrap is not None
        and pathlib.Path(bootstrap).resolve() != candidate_bootstrap.resolve()
    )
    if not externally_verified:
        aggregate = {
            "schema_version": 1,
            "ok": False,
            "error": {
                "name": "SourcePinError",
                "message": "full sandbox execution requires the external source-pin bootstrap",
            },
            "artifact_written": False,
        }
        print(json.dumps(aggregate, ensure_ascii=False, sort_keys=True))
        return 1
    # Re-exec ĐÚNG MỘT LẦN, và chỉ để lấy mount namespace riêng cùng
    # `--kill-child=KILL`.  Cờ môi trường ở đây CHỈ chống lặp vô hạn: nó KHÔNG
    # còn là thẩm quyền cách ly nào cả.  Ai đặt sẵn cờ để bỏ qua bước này vẫn
    # không thoát được, vì `establish_fixture_baseline` TỰ tạo namespace mạng
    # trong tiến trình và đo chuyển dịch của chính nó trước khi chạm loopback
    # (SPEC-003).
    if sys.platform.startswith("linux") and os.environ.get(REENTRY_MARKER_ENV) != "1":
        _enter_disposable_fixture_namespace(
            args.repo_root,
            args.candidate_head,
            args.dispatcher_pin,
            args.repeat,
            args.output,
        )
    try:
        runner.fingerprint()
        # Chốt độ nguyên sơ của loopback đúng một lần, khi chưa lượt nào ghi gì.
        fixture_baseline = establish_fixture_baseline()
        runs = []
        for index in range(args.repeat):
            try:
                runs.append(
                    _full_once(
                        args.repo_root,
                        args.candidate_head,
                        args.dispatcher_pin,
                        index + 1,
                        fixture_baseline,
                    )
                )
            except Exception as exc:
                runs.append(_exception_run(args.candidate_head, index + 1, exc))
                break
        scheduled_sets = [run["scheduled_test_ids"] for run in runs]
        classifications = [
            [item.get("actual_classification") for item in run["tests"]]
            for run in runs
        ]
        aggregate = {
            "schema_version": 1,
            "ok": all(run["ok"] is True for run in runs)
            and len(runs) == args.repeat
            and all(value == scheduled_sets[0] for value in scheduled_sets)
            and all(value == classifications[0] for value in classifications),
            "repeat_requested": args.repeat,
            "repeat_executed": len(runs),
            "repeat_completed": sum("error" not in run for run in runs),
            "same_scheduled_test_ids": all(value == scheduled_sets[0] for value in scheduled_sets),
            "stable_classifications": all(value == classifications[0] for value in classifications),
            "runs": runs,
        }
    except runner.PlatformUnsupported as exc:
        aggregate = _platform_report(exc)
    except Exception as exc:
        aggregate = {
            "schema_version": 1,
            "ok": False,
            "error": {"name": type(exc).__name__, "message": str(exc)},
            "scheduled_test_ids": list(SANDBOX_TEST_IDS),
            "scheduled_total": len(SANDBOX_TEST_IDS),
            "executed": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "not_run": len(SANDBOX_TEST_IDS),
        }
    encoded = json.dumps(aggregate, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output and aggregate.get("error", {}).get("name") != "SourcePinError":
        output = pathlib.Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8", newline="\n")
    print(encoded, end="")
    return 0 if aggregate.get("ok") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
