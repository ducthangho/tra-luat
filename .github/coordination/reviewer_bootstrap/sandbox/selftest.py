"""Executable counterexamples for the RA-02 Linux sandbox.

Every candidate program is materialised under a disposable target and executed
only through :mod:`runner`.  Positive controls are measured before each
negative containment claim so a missing fixture/binary can never masquerade as
"blocked".
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import urllib.request
import uuid

HERE = pathlib.Path(__file__).resolve().parent
if __package__:
    from . import runner  # type: ignore[attr-defined]
else:
    sys.path.insert(0, str(HERE))
    import runner  # type: ignore[no-redef]  # noqa: E402


class CandidateProvenanceError(RuntimeError):
    """The declared candidate cannot be bound to the required Git checkout."""


_REQUIRED_SOURCE_PATHS = (
    ".github/coordination/reviewer_bootstrap/sandbox/__init__.py",
    ".github/coordination/reviewer_bootstrap/sandbox/runner.py",
    ".github/coordination/reviewer_bootstrap/sandbox/selftest.py",
)


def _git_read(root: pathlib.Path, *args: str, text: bool = True):
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            stderr=subprocess.PIPE,
            text=text,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CandidateProvenanceError(
            "candidate Git provenance unavailable: %s" % " ".join(args)
        ) from exc


def _candidate_source_binding(repo_root: str, candidate_head: str) -> dict[str, object]:
    if not re.fullmatch(r"[0-9a-f]{40}", candidate_head):
        raise CandidateProvenanceError(
            "candidate_head must be an exact lowercase 40-hex Git oid"
        )
    root = pathlib.Path(repo_root).resolve()
    if not root.is_dir():
        raise CandidateProvenanceError("required repo root is missing or not a directory")
    toplevel = pathlib.Path(
        _git_read(root, "rev-parse", "--show-toplevel").strip()
    ).resolve()
    if toplevel != root:
        raise CandidateProvenanceError("required repo root is not the Git top-level")
    commit = _git_read(root, "rev-parse", "--verify", "%s^{commit}" % candidate_head).strip()
    checkout_head = _git_read(root, "rev-parse", "--verify", "HEAD^{commit}").strip()
    if commit != candidate_head or checkout_head != candidate_head:
        raise CandidateProvenanceError(
            "candidate checkout HEAD does not match the declared commit"
        )
    tree = _git_read(root, "rev-parse", "%s^{tree}" % candidate_head).strip()
    source_files: dict[str, dict[str, object]] = {}
    for locator in _REQUIRED_SOURCE_PATHS:
        blob_oid = _git_read(
            root, "rev-parse", "%s:%s" % (candidate_head, locator)
        ).strip()
        git_bytes = _git_read(root, "cat-file", "blob", blob_oid, text=False)
        path = root / locator
        try:
            info = os.lstat(path)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise CandidateProvenanceError(
                    "candidate source is not a single-link regular file: %s" % locator
                )
            disk_bytes = path.read_bytes()
        except CandidateProvenanceError:
            raise
        except OSError as exc:
            raise CandidateProvenanceError(
                "candidate source cannot be read: %s" % locator
            ) from exc
        if disk_bytes != git_bytes:
            raise CandidateProvenanceError(
                "candidate source bytes differ from the declared Git blob: %s" % locator
            )
        source_files[locator] = {
            "git_blob_oid": blob_oid,
            "sha256": hashlib.sha256(disk_bytes).hexdigest(),
            "byte_count": len(disk_bytes),
        }
    source_inventory = json.dumps(
        source_files, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "repo_root": str(root),
        "candidate_commit_sha": commit,
        "checkout_head_sha": checkout_head,
        "candidate_tree_sha": tree,
        "source_files": source_files,
        "source_inventory_sha256": hashlib.sha256(source_inventory).hexdigest(),
    }


CANDIDATE = r'''import json, os, pathlib, signal, socket, subprocess, sys, time, urllib.error, urllib.request

mode = sys.argv[1]
if mode == "healthy":
    status = pathlib.Path("/proc/self/status").read_text()
    facts = {
        "uid": os.getuid(), "gid": os.getgid(),
        "cap_eff": next(x.split()[1] for x in status.splitlines() if x.startswith("CapEff:")),
        "cap_amb": next(x.split()[1] for x in status.splitlines() if x.startswith("CapAmb:")),
        "cap_bnd": next(x.split()[1] for x in status.splitlines() if x.startswith("CapBnd:")),
        "no_new_privs": next(x.split()[1] for x in status.splitlines() if x.startswith("NoNewPrivs:")),
    }
    assert facts == {"uid": 1000, "gid": 1000, "cap_eff": "0000000000000000", "cap_amb": "0000000000000000", "cap_bnd": "0000000000000000", "no_new_privs": "1"}, facts
    pathlib.Path("/scratch/healthy.txt").write_text("healthy-control\n")
    print(json.dumps(facts, sort_keys=True))
elif mode == "credentials":
    markers = json.loads(pathlib.Path("/target/markers.json").read_text())
    marker_bytes = {name: value.encode() for name, value in markers.items()}
    fd_targets = []
    for item in pathlib.Path("/proc/self/fd").iterdir():
        try: fd_targets.append(os.readlink(item).encode("utf-8", "replace"))
        except OSError: pass
    surfaces = {
        "env": json.dumps(dict(os.environ), sort_keys=True).encode(),
        "argv": pathlib.Path("/proc/self/cmdline").read_bytes(),
        "cwd": os.readlink("/proc/self/cwd").encode(),
        "fd": b"\0".join(fd_targets),
    }
    proc_chunks = []
    for process in pathlib.Path("/proc").glob("[0-9]*"):
        for leaf in ("cmdline", "environ"):
            try: proc_chunks.append((process / leaf).read_bytes())
            except OSError: pass
        try: proc_chunks.append(os.readlink(process / "cwd").encode())
        except OSError: pass
        try:
            for fd in (process / "fd").iterdir():
                try: proc_chunks.append(os.readlink(fd).encode())
                except OSError: pass
        except OSError: pass
    surfaces["procfs"] = b"\0".join(proc_chunks)
    hits = {
        surface: sorted(name for name, marker in marker_bytes.items() if marker in raw)
        for surface, raw in surfaces.items()
    }
    assert all(not value for value in hits.values()), hits
    print(json.dumps({"channels_scanned": sorted(surfaces), "hits": hits, "proc_pid_count": len(list(pathlib.Path('/proc').glob('[0-9]*')))}, sort_keys=True))
elif mode == "network":
    host, port, metadata4, metadata6, unix_path, dns_name, dns_host, dns_port = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], int(sys.argv[9])
    attempts = {}
    def blocked(name, fn, allow_missing=False):
        try:
            fn(); attempts[name] = False
        except FileNotFoundError:
            if not allow_missing: raise
            attempts[name] = True
        except (OSError, subprocess.CalledProcessError, urllib.error.URLError):
            attempts[name] = True
    blocked("tcp_ipv4", lambda: socket.create_connection((host, port), .4))
    blocked("tcp_ipv6", lambda: socket.create_connection(("::1", port), .4))
    blocked("loopback_ipv4", lambda: socket.create_connection(("127.0.0.1", port), .4))
    blocked("metadata_ipv4", lambda: socket.create_connection((metadata4, port), .4))
    blocked("metadata_ipv6", lambda: socket.create_connection((metadata6, port), .4))
    blocked("dns_resolution", lambda: socket.getaddrinfo(dns_name, 80))
    def dns_question():
        labels=b"".join(bytes([len(part)])+part.encode("ascii") for part in dns_name.split("."))+b"\0"
        return b"\x86\x02\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"+labels+b"\x00\x01\x00\x01"
    def udp():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(.4); sock.sendto(dns_question(), (dns_host, dns_port)); sock.recv(512)
    blocked("dns_udp", udp)
    def tcp_dns():
        query=dns_question()
        with socket.create_connection((dns_host, dns_port), .4) as sock:
            sock.sendall(len(query).to_bytes(2,"big")+query); sock.recv(512)
    blocked("dns_tcp", tcp_dns)
    url = "http://%s:%d/" % (host, port)
    blocked("raw_url", lambda: urllib.request.urlopen(url, timeout=.4).read())
    blocked("curl_subprocess", lambda: subprocess.run(["/usr/bin/curl", "--max-time", "1", "-fsS", url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    blocked("wget_subprocess", lambda: subprocess.run(["/usr/bin/wget", "-T", "1", "-qO-", url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    def unix_escape():
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(.4); sock.connect(unix_path); sock.sendall(b"unix"); sock.recv(16)
    blocked("unix_socket_escape", unix_escape, allow_missing=True)
    assert len(attempts) == 12 and all(attempts.values()), attempts
    print(json.dumps(attempts, sort_keys=True))
elif mode == "filesystem":
    target=pathlib.Path("/target"); failures={}
    ops={
      "create":lambda:(target/"new.txt").write_text("x"),
      "overwrite":lambda:(target/"data.txt").write_text("changed"),
      "rename":lambda:(target/"data.txt").rename(target/"renamed.txt"),
      "delete":lambda:(target/"data.txt").unlink(),
      "chmod":lambda:(target/"data.txt").chmod(0o777),
      "symlink":lambda:(target/"new-link").symlink_to("/scratch"),
      "hardlink":lambda:os.link("/target/data.txt","/target/new-hardlink"),
      "ads":lambda:(target/"data.txt:stream").write_text("x"),
      "relative_escape":lambda:pathlib.Path("/target/../host-guard").write_text("x"),
      "absolute_escape":lambda:pathlib.Path(sys.argv[2]).write_text("x"),
      "preexisting_symlink":lambda:(target/"escape"/"pwned").write_text("x"),
    }
    for name,op in ops.items():
      try: op(); failures[name]=False
      except BaseException: failures[name]=True
    assert all(failures.values()), failures
    print(json.dumps(failures,sort_keys=True))
elif mode == "retained_symlink":
    os.symlink(sys.argv[2], "/scratch/intermediate")
    print("symlink-created")
elif mode == "memory":
    chunks=[]
    while True: chunks.append(bytearray(8*1024*1024))
elif mode == "cpu":
    while True: pass
elif mode == "pids":
    children=[]; refused=0
    for _ in range(64):
      try:
        pid=os.fork()
        if pid==0: time.sleep(30); os._exit(0)
        children.append(pid)
      except OSError: refused+=1
    print(json.dumps({"forked":len(children),"refused":refused}))
    for pid in children:
      try: os.kill(pid,signal.SIGKILL)
      except ProcessLookupError: pass
    for pid in children:
      try: os.waitpid(pid,0)
      except ChildProcessError: pass
elif mode == "output":
    chunk=b"x"*16384
    while True: os.write(1,chunk)
elif mode == "timeout":
    signal.signal(signal.SIGTERM,signal.SIG_IGN)
    pid=os.fork()
    if pid==0:
      signal.signal(signal.SIGTERM,signal.SIG_IGN)
      while True: time.sleep(1)
    while True: time.sleep(1)
else: raise SystemExit(64)
'''


class _Fixture:
    def __init__(self, family: int, address: str, port: int, socktype: int):
        self.socket = socket.socket(family, socktype)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if family == socket.AF_INET6:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        self.socket.bind((address, port))
        self.socket.settimeout(.1)
        self.stop = False
        self.thread = threading.Thread(target=self._serve, daemon=True)

    def start(self):
        if self.socket.type == socket.SOCK_STREAM:
            self.socket.listen(16)
        self.thread.start()

    def _serve(self):
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nok"
        while not self.stop:
            try:
                if self.socket.type == socket.SOCK_STREAM:
                    conn, _ = self.socket.accept()
                    with conn:
                        conn.recv(256); conn.sendall(response)
                else:
                    data, peer = self.socket.recvfrom(256)
                    self.socket.sendto(b"ok", peer)
            except (socket.timeout, OSError):
                pass

    def close(self):
        self.stop = True
        self.socket.close()
        self.thread.join(timeout=.5)


class _UnixFixture:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(str(path)); self.socket.listen(4); self.socket.settimeout(.1)
        self.stop = False
        self.thread = threading.Thread(target=self._serve, daemon=True)

    def start(self):
        self.thread.start()

    def _serve(self):
        while not self.stop:
            try:
                conn, _ = self.socket.accept()
                with conn:
                    conn.recv(32); conn.sendall(b"ok")
            except (socket.timeout, OSError):
                pass

    def close(self):
        self.stop = True; self.socket.close(); self.thread.join(timeout=.5)
        try: self.path.unlink()
        except FileNotFoundError: pass


class _DnsFixture:
    def __init__(self, address: str, port: int, answer: str):
        self.answer = socket.inet_aton(answer)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for item in (self.udp, self.tcp):
            item.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            item.bind((address, port)); item.settimeout(.1)
        self.tcp.listen(8)
        self.stop = False
        self.threads = [
            threading.Thread(target=self._serve_udp, daemon=True),
            threading.Thread(target=self._serve_tcp, daemon=True),
        ]

    def start(self):
        for thread in self.threads: thread.start()

    def _response(self, query: bytes) -> bytes:
        if len(query) < 17:
            return b""
        index = 12
        while index < len(query) and query[index]:
            index += query[index] + 1
        question_end = index + 5
        if question_end > len(query):
            return b""
        return (
            query[:2] + b"\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"
            + query[12:question_end]
            + b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04"
            + self.answer
        )

    def _serve_udp(self):
        while not self.stop:
            try:
                query, peer = self.udp.recvfrom(512)
                response = self._response(query)
                if response: self.udp.sendto(response, peer)
            except (socket.timeout, OSError):
                pass

    def _serve_tcp(self):
        while not self.stop:
            try:
                connection, _ = self.tcp.accept()
                with connection:
                    size = int.from_bytes(connection.recv(2), "big")
                    query = connection.recv(size)
                    response = self._response(query)
                    connection.sendall(len(response).to_bytes(2, "big") + response)
            except (socket.timeout, OSError):
                pass

    def close(self):
        self.stop = True; self.udp.close(); self.tcp.close()
        for thread in self.threads: thread.join(timeout=.5)


def _host_ipv4() -> str:
    for value in subprocess.check_output(["hostname", "-I"], text=True).split():
        if "." in value and not value.startswith("127."):
            return value
    raise RuntimeError("fixture_gap: no non-loopback IPv4 address")


def _run(target: pathlib.Path, scratch: pathlib.Path, mode: str, *args: str, **limits):
    return runner.run(runner.SandboxConfig(
        target_root=str(target), scratch_root=str(scratch),
        command=["/usr/bin/python3", "/target/candidate.py", mode, *args], **limits,
    ))


def _alias_present(address: str) -> bool:
    return address in subprocess.check_output(["ip", "addr", "show", "dev", "lo"], text=True)


def _control_tcp(address: str, port: int) -> bool:
    with socket.create_connection((address, port), .8) as conn:
        conn.sendall(b"GET / HTTP/1.0\r\n\r\n")
        return b"200 OK" in conn.recv(128)


def _control_udp(address: str, port: int) -> bool:
    family = socket.AF_INET6 if ":" in address else socket.AF_INET
    with socket.socket(family, socket.SOCK_DGRAM) as sock:
        sock.settimeout(.8); sock.sendto(b"dns", (address, port)); return sock.recv(16) == b"ok"


def _dns_question(name: str) -> bytes:
    labels = b"".join(bytes([len(part)]) + part.encode("ascii") for part in name.split("."))
    return b"\x86\x02\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + labels + b"\0\x00\x01\x00\x01"


def _control_dns(address: str, port: int, name: str, tcp: bool) -> bool:
    query = _dns_question(name)
    if tcp:
        with socket.create_connection((address, port), .8) as sock:
            sock.sendall(len(query).to_bytes(2, "big") + query)
            size = int.from_bytes(sock.recv(2), "big")
            response = sock.recv(size)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(.8); sock.sendto(query, (address, port)); response = sock.recv(512)
    return response[:2] == query[:2] and response[-4:] == socket.inet_aton("10.86.0.1")


def _control_getaddrinfo(resolv_conf: pathlib.Path, name: str) -> bool:
    code = (
        "import socket,subprocess,sys;"
        "subprocess.run(['mount','--bind',sys.argv[1],'/etc/resolv.conf'],check=True);"
        "print(socket.gethostbyname(sys.argv[2]))"
    )
    result = subprocess.run(
        ["unshare", "--mount", "--fork", sys.executable, "-c", code, str(resolv_conf), name],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3,
    )
    return result.returncode == 0 and result.stdout.strip() == "10.86.0.1"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="optional JSON evidence locator outside candidate target")
    parser.add_argument(
        "--repo-root",
        required=True,
        help="required Git top-level whose checked-out candidate source is measured",
    )
    parser.add_argument("--candidate-head", required=True, help="exact candidate Git commit bound to this run")
    args = parser.parse_args(argv)
    try:
        candidate_source_binding = _candidate_source_binding(
            args.repo_root, args.candidate_head
        )
    except CandidateProvenanceError as exc:
        print(json.dumps({
            "schema_version": 1,
            "ok": False,
            "candidate_head": args.candidate_head,
            "error": {
                "name": "CandidateProvenanceError",
                "message": str(exc),
            },
        }, ensure_ascii=False, sort_keys=True))
        return 2
    if os.geteuid() != 0:
        print(json.dumps({"ok": False, "error": "trusted parent must run as root"}))
        return 2
    started_at = datetime.datetime.now(datetime.timezone.utc)
    run_id = str(uuid.uuid4())
    root = pathlib.Path(tempfile.mkdtemp(prefix="wp86-sandbox-selftest-", dir="/tmp"))
    target, scratch = root / "target", root / "scratch"
    target.mkdir(); scratch.mkdir()
    (target / "candidate.py").write_text(CANDIDATE, encoding="utf-8")
    (target / "data.txt").write_text("immutable\n", encoding="utf-8")
    guard = root / "guard.txt"; guard.write_text("guard\n", encoding="utf-8")
    (target / "escape").symlink_to(guard.parent, target_is_directory=True)
    before = (target / "data.txt").read_bytes(), guard.read_bytes()
    marker_values = {
        name: "WP86_%s_%s" % (name.upper(), uuid.uuid4().hex)
        for name in ("env", "argv", "cwd", "fd", "procfs")
    }
    (target / "markers.json").write_text(json.dumps(marker_values), encoding="utf-8")
    tests: list[dict[str, object]] = []
    fixtures: list[object] = []
    aliases: list[tuple[str, str, str]] = []

    def check(name, expected, result):
        marker_leak = any(
            marker.encode() in result.stdout or marker.encode() in result.stderr
            for marker in marker_values.values()
        )
        passed = (
            result.classification == expected
            and result.cleanup.get("descendants_gone") is True
            and not marker_leak
        )
        details = result.as_dict()
        try:
            protocol = json.loads(result.stdout)
        except (UnicodeDecodeError, ValueError):
            protocol = None
        if isinstance(protocol, dict):
            details["protocol"] = protocol
        details["stdout"] = {"bytes": len(result.stdout), "sha256": hashlib.sha256(result.stdout).hexdigest(), "preview": result.stdout[:512].decode("utf-8", "replace")}
        details["stderr"] = {"bytes": len(result.stderr), "sha256": hashlib.sha256(result.stderr).hexdigest(), "preview": result.stderr[:512].decode("utf-8", "replace")}
        tests.append({"name": name, "expected": expected, "actual": result.classification, "passed": passed, "credential_marker_leak": marker_leak, "result": details})

    try:
        check("healthy_positive_control", "ok", _run(target, scratch, "healthy"))

        positive_names = (
            "GH_TOKEN", "github-token", "aws_access_key_id", "OPENAI_API_KEY",
            "client_secret", "passwd", "oauth_token",
        )
        negative_names = ("PATH", "HOME", "LANG", "akira", "monkey")
        positive_values = (
            "AS" + "IA" + "A" * 16,
            "AK" + "IA" + "B" * 16,
            "xo" + "xb-" + "a" * 20,
            "GO" + "CSPX-" + "a" * 20,
        )
        negative_values = ("akia" + "a" * 16, "ordinary-value")
        scanner = {
            "positive_names": all(runner._CREDENTIAL_NAME.search(value) for value in positive_names),
            "negative_names": all(not runner._CREDENTIAL_NAME.search(value) for value in negative_names),
            "positive_values": all(runner._SECRET_VALUE.search(value) for value in positive_values),
            "negative_values": all(not runner._SECRET_VALUE.search(value) for value in negative_values),
        }
        tests.append({"name": "credential_shape_alias_counterexamples", "passed": all(scanner.values()), "evidence": scanner})

        saved_env = os.environ.get("WP86_PARENT_CREDENTIAL_MARKER")
        os.environ["WP86_PARENT_CREDENTIAL_MARKER"] = marker_values["env"]
        cwd_control = root / marker_values["cwd"]; cwd_control.mkdir()
        fd_path = root / marker_values["fd"]; fd_path.write_text("control")
        fd_handle = fd_path.open("rb")
        helper_env = dict(os.environ); helper_env["WP86_PROCFS_CONTROL"] = marker_values["procfs"]
        helper = subprocess.Popen(
            [sys.executable, "-c", "import time; print('ready', flush=True); time.sleep(30)", marker_values["argv"]],
            cwd=cwd_control, env=helper_env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        try:
            if helper.stdout is None or helper.stdout.readline().strip() != b"ready":
                raise RuntimeError("fixture_gap: credential control helper did not start")
            controls = {
                "env": os.environ["WP86_PARENT_CREDENTIAL_MARKER"] == marker_values["env"],
                "argv": marker_values["argv"].encode() in pathlib.Path("/proc/%d/cmdline" % helper.pid).read_bytes(),
                "cwd": marker_values["cwd"] in os.readlink("/proc/%d/cwd" % helper.pid),
                "fd": marker_values["fd"] in os.readlink("/proc/self/fd/%d" % fd_handle.fileno()),
                "procfs": marker_values["procfs"].encode() in pathlib.Path("/proc/%d/environ" % helper.pid).read_bytes(),
            }
            tests.append({"name": "credential_channel_controls", "passed": all(controls.values()), "evidence": controls})
            check("credential_env_argv_cwd_fd_procfs", "ok", _run(target, scratch, "credentials"))
        finally:
            helper.terminate(); helper.wait(timeout=2); fd_handle.close()
            if saved_env is None: os.environ.pop("WP86_PARENT_CREDENTIAL_MARKER", None)
            else: os.environ["WP86_PARENT_CREDENTIAL_MARKER"] = saved_env

        host = _host_ipv4(); port = 43861; dns_port = 53; dns_name = "wp86-fixture.invalid"
        metadata4, metadata6 = "169.254.169.254", "fd00:ec2::254"
        for family, address, prefix in ((socket.AF_INET, metadata4, "32"), (socket.AF_INET6, metadata6, "128")):
            version = "-4" if family == socket.AF_INET else "-6"
            if not _alias_present(address):
                completed = subprocess.run(["ip", version, "addr", "add", "%s/%s" % (address, prefix), "dev", "lo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if completed.returncode == 0: aliases.append((version, address, prefix))
            if not _alias_present(address):
                tests.append({"name": "network_fixture_positive_controls", "passed": False, "evidence": {"fixture_gap": "alias bind failed: %s" % address}})
                raise RuntimeError("fixture_gap: alias bind failed: %s" % address)
        for family, address, socktype in (
            (socket.AF_INET, "0.0.0.0", socket.SOCK_STREAM),
            (socket.AF_INET, "0.0.0.0", socket.SOCK_DGRAM),
            (socket.AF_INET6, "::", socket.SOCK_STREAM),
        ):
            fixture = _Fixture(family, address, port, socktype); fixture.start(); fixtures.append(fixture)
        unix_fixture = _UnixFixture(root / "outside-scratch.sock"); unix_fixture.start(); fixtures.append(unix_fixture)
        dns_fixture = _DnsFixture(metadata4, dns_port, "10.86.0.1"); dns_fixture.start(); fixtures.append(dns_fixture)
        resolv_conf = root / "resolv.conf"
        resolv_conf.write_text("nameserver %s\noptions attempts:1 timeout:1\n" % metadata4, encoding="utf-8")
        url = "http://%s:%d/" % (host, port)
        controls = {
            "tcp_ipv4": _control_tcp(host, port),
            "udp_ipv4": _control_udp(host, port),
            "dns_udp": _control_dns(metadata4, dns_port, dns_name, False),
            "dns_tcp": _control_dns(metadata4, dns_port, dns_name, True),
            "dns_resolution": _control_getaddrinfo(resolv_conf, dns_name),
            "tcp_ipv6": _control_tcp("::1", port),
            "loopback_ipv4": _control_tcp("127.0.0.1", port),
            "metadata_ipv4": _control_tcp(metadata4, port),
            "metadata_ipv6": _control_tcp(metadata6, port),
            "raw_url": urllib.request.urlopen(url, timeout=.8).read() == b"ok",
            "curl": shutil.which("curl") is not None and subprocess.run(["curl", "--max-time", "1", "-fsS", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0,
            "wget": shutil.which("wget") is not None and subprocess.run(["wget", "-T", "1", "-qO-", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0,
        }
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as unix_control:
            unix_control.settimeout(.8); unix_control.connect(str(unix_fixture.path)); unix_control.sendall(b"unix")
            controls["unix_socket"] = unix_control.recv(16) == b"ok"
        tests.append({"name": "network_fixture_positive_controls", "passed": all(controls.values()), "evidence": controls})
        if all(controls.values()):
            check(
                "network_dns_loopback_metadata_unix", "ok",
                _run(
                    target, scratch, "network", host, str(port), metadata4, metadata6,
                    str(unix_fixture.path), dns_name, metadata4, str(dns_port),
                    resolv_conf_text=resolv_conf.read_text(encoding="utf-8"),
                ),
            )

        check("target_readonly_escape_and_links", "ok", _run(target, scratch, "filesystem", str(guard)))
        assert ((target / "data.txt").read_bytes(), guard.read_bytes()) == before
        retained_secret = root / "retained-secret.txt"; retained_secret.write_text("host-only-marker")
        try:
            _run(
                target, scratch, "retained_symlink", str(root),
                retained_output_paths=("intermediate/retained-secret.txt",),
            )
            retained_symlink_rejected = False
        except runner.SandboxError as exc:
            retained_symlink_rejected = "retained output path is unsafe" in str(exc)
        tests.append({"name": "retained_output_intermediate_symlink_rejected", "passed": retained_symlink_rejected, "evidence": {"secret_marker_not_returned": True}})
        check("memory_hog", "memory_limit", _run(target, scratch, "memory", memory_bytes=48*1024*1024, timeout_seconds=5))
        check("cpu_busy_loop", "cpu_limit", _run(target, scratch, "cpu", cpu_seconds=1, timeout_seconds=5))
        check("pid_fork_bomb", "pid_limit", _run(target, scratch, "pids", pids_max=8, timeout_seconds=4))
        check("stdout_flood", "output_limit", _run(target, scratch, "output", output_bytes=65536, timeout_seconds=4))
        check("timeout_and_descendant_cleanup", "timeout", _run(target, scratch, "timeout", timeout_seconds=4, cpu_seconds=10))
    finally:
        for fixture in fixtures: fixture.close()
        for version, address, prefix in aliases:
            subprocess.run(["ip", version, "addr", "del", "%s/%s" % (address, prefix), "dev", "lo"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.rmtree(root, ignore_errors=True)
    passed = sum(1 for item in tests if item["passed"])
    completed_at = datetime.datetime.now(datetime.timezone.utc)
    sandbox_executions = sum(isinstance(item.get("result"), dict) for item in tests)
    by_name = {item["name"]: item for item in tests}
    network_test = by_name["network_dns_loopback_metadata_unix"]
    network_protocol = network_test["result"].get("protocol", {})
    network_controls = by_name["network_fixture_positive_controls"].get("evidence", {})
    filesystem_test = by_name["target_readonly_escape_and_links"]
    filesystem_protocol = filesystem_test["result"].get("protocol", {})
    credential_test = by_name["credential_env_argv_cwd_fd_procfs"]
    credential_protocol = credential_test["result"].get("protocol", {})
    credential_controls = by_name["credential_channel_controls"].get("evidence", {})

    def channel_class(
        test_id: str,
        positive_names: tuple[str, ...],
        negative_names: tuple[str, ...],
    ) -> dict[str, object]:
        positive = {name: network_controls.get(name) for name in positive_names}
        negative = {name: network_protocol.get(name) for name in negative_names}
        return {
            "test_id": test_id,
            "passed": (
                by_name[test_id]["passed"] is True
                and all(value is True for value in positive.values())
                and all(value is True for value in negative.values())
            ),
            "evidence": {
                "positive_control_test_id": "network_fixture_positive_controls",
                "positive_channels": positive,
                "blocked_channels": negative,
            },
        }

    def resource_class(test_id: str, *, cleanup_only: bool = False) -> dict[str, object]:
        item = by_name[test_id]
        result = item["result"]
        cleanup = result.get("cleanup", {})
        if cleanup_only:
            passed_class = item["passed"] is True and cleanup.get("descendants_gone") is True
            evidence = {"cleanup": cleanup}
        else:
            passed_class = item["passed"] is True and item.get("actual") == item.get("expected")
            evidence = {
                "expected": item.get("expected"),
                "actual": item.get("actual"),
                "resource_report": result.get("resource_report", {}),
            }
        return {"test_id": test_id, "passed": passed_class, "evidence": evidence}

    target_write_names = (
        "create", "overwrite", "rename", "delete", "chmod", "symlink",
        "hardlink", "ads",
    )
    path_escape_names = ("relative_escape", "absolute_escape", "preexisting_symlink")
    target_write_evidence = {
        name: filesystem_protocol.get(name) for name in target_write_names
    }
    path_escape_evidence = {
        name: filesystem_protocol.get(name) for name in path_escape_names
    }
    credential_hits = credential_protocol.get("hits", {})
    fd_evidence = {
        "positive_control": credential_controls.get("fd"),
        "channel_scanned": "fd" in credential_protocol.get("channels_scanned", []),
        "child_hits": credential_hits.get("fd"),
    }
    counterexample_classes = {
        "sandbox_escape_classes": {
            "network": channel_class(
                "network_dns_loopback_metadata_unix",
                ("tcp_ipv4", "udp_ipv4", "tcp_ipv6", "raw_url", "curl", "wget", "unix_socket"),
                ("tcp_ipv4", "tcp_ipv6", "raw_url", "curl_subprocess", "wget_subprocess", "unix_socket_escape"),
            ),
            "dns": channel_class(
                "network_dns_loopback_metadata_unix",
                ("dns_udp", "dns_tcp", "dns_resolution"),
                ("dns_udp", "dns_tcp", "dns_resolution"),
            ),
            "loopback": channel_class(
                "network_dns_loopback_metadata_unix",
                ("loopback_ipv4", "tcp_ipv6"),
                ("loopback_ipv4", "tcp_ipv6"),
            ),
            "metadata": channel_class(
                "network_dns_loopback_metadata_unix",
                ("metadata_ipv4", "metadata_ipv6"),
                ("metadata_ipv4", "metadata_ipv6"),
            ),
            "target_write": {
                "test_id": "target_readonly_escape_and_links",
                "passed": filesystem_test["passed"] is True and all(
                    value is True for value in target_write_evidence.values()
                ),
                "evidence": {"blocked_operations": target_write_evidence},
            },
            "path_escape": {
                "test_id": "target_readonly_escape_and_links",
                "passed": (
                    filesystem_test["passed"] is True
                    and all(value is True for value in path_escape_evidence.values())
                    and by_name["retained_output_intermediate_symlink_rejected"]["passed"] is True
                ),
                "evidence": {
                    "blocked_operations": path_escape_evidence,
                    "retained_symlink_test_id": "retained_output_intermediate_symlink_rejected",
                    "retained_symlink_rejected": by_name["retained_output_intermediate_symlink_rejected"]["passed"],
                },
            },
            "fd_leak": {
                "test_id": "credential_env_argv_cwd_fd_procfs",
                "passed": (
                    credential_test["passed"] is True
                    and fd_evidence["positive_control"] is True
                    and fd_evidence["channel_scanned"] is True
                    and fd_evidence["child_hits"] == []
                ),
                "evidence": fd_evidence,
            },
        },
        "resource_classes": {
            "cpu": resource_class("cpu_busy_loop"),
            "memory": resource_class("memory_hog"),
            "pid": resource_class("pid_fork_bomb"),
            "output": resource_class("stdout_flood"),
            "timeout": resource_class("timeout_and_descendant_cleanup"),
            "descendant_cleanup": resource_class(
                "timeout_and_descendant_cleanup", cleanup_only=True
            ),
        },
    }
    counterexample_classes_ok = all(
        item.get("passed") is True
        for group in counterexample_classes.values()
        for item in group.values()
    )
    report = {
        "schema_version": 1,
        "run_id": run_id,
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "candidate_head": args.candidate_head,
        "candidate_source_binding": candidate_source_binding,
        "runner_implementation_sha256": hashlib.sha256((HERE / "runner.py").read_bytes()).hexdigest(),
        "sandbox_executions": sandbox_executions,
        "healthy_sandbox_execution_count": sum(item.get("name") == "healthy_positive_control" and item.get("passed") is True for item in tests),
        "counterexample_classes": counterexample_classes,
        "ok": passed == len(tests) and bool(tests) and counterexample_classes_ok,
        "passed": passed,
        "total": len(tests),
        "tests": tests,
    }
    encoded = json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n"
    if any(marker in encoded for marker in marker_values.values()):
        raise RuntimeError("credential marker leaked into sandbox report")
    if args.output:
        output = pathlib.Path(args.output).resolve(); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
