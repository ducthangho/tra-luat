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
    SANDBOX_TEST_IDS,
)
from sandbox import runner  # noqa: E402


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


def _full_once(repo_root: str, candidate_head: str, dispatcher_pin: str, run_index: int) -> dict[str, object]:
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


def _run_portable_controls() -> list[dict[str, object]]:
    records = []
    for control in (
        watchdog_timeout_precedes_cpu_heuristics,
        cpu_limit_requires_explicit_signal_evidence,
    ):
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
    env["RA02_DISPOSABLE_FIXTURE_NS"] = "1"
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
    tests = (watchdog_timeout_precedes_cpu_heuristics, cpu_limit_requires_explicit_signal_evidence)
    passed = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            print("[FAIL] %s -- %s: %s" % (test.__name__, type(exc).__name__, exc))
        else:
            passed += 1
            print("[OK] %s" % test.__name__)
    print("== ra02 sandbox unit selftest %d/%d ==" % (passed, len(tests)))
    return 0 if passed == len(tests) and len(tests) > 0 else 1


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
    parser.add_argument("--repo-root")
    parser.add_argument("--candidate-head")
    parser.add_argument("--dispatcher-pin")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    if not args.full:
        return _unit()
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
    if sys.platform.startswith("linux") and os.environ.get("RA02_DISPOSABLE_FIXTURE_NS") != "1":
        _enter_disposable_fixture_namespace(
            args.repo_root,
            args.candidate_head,
            args.dispatcher_pin,
            args.repeat,
            args.output,
        )
    try:
        runner.fingerprint()
        runs = []
        for index in range(args.repeat):
            try:
                runs.append(
                    _full_once(
                        args.repo_root,
                        args.candidate_head,
                        args.dispatcher_pin,
                        index + 1,
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
