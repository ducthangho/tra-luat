"""Executable counterexamples for the RA-02 Linux sandbox.

Run as the trusted WSL parent:

    sudo python3 selftest.py

Every candidate program is materialised under a disposable *target* and is only
executed through :mod:`runner`; no candidate program is run bare.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import runner  # noqa: E402


CANDIDATE = r'''import json, os, pathlib, signal, socket, subprocess, sys, time, urllib.request

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
    shaped = ("TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "ANTHROPIC", "OPENAI", "AWS_")
    env_hits = sorted(k for k in os.environ if any(s in k.upper() for s in shaped))
    argv = pathlib.Path("/proc/self/cmdline").read_bytes()
    fd_hits = []
    for item in pathlib.Path("/proc/self/fd").iterdir():
        try:
            target = os.readlink(item)
            if "marker" in target.lower() or "socket" in target.lower(): fd_hits.append(target)
        except OSError: pass
    assert not env_hits, env_hits
    assert b"WP86_SECRET_MARKER" not in argv
    assert not fd_hits, fd_hits
    print(json.dumps({"env_hits": env_hits, "fd_hits": fd_hits, "proc_pid_count": len(list(pathlib.Path('/proc').glob('[0-9]*')))}))
elif mode == "network":
    host, port, metadata4, metadata6 = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
    attempts = {}
    def blocked(name, fn):
        try: fn(); attempts[name] = False
        except BaseException: attempts[name] = True
    blocked("ipv4", lambda: socket.create_connection((host, port), .25))
    blocked("ipv6", lambda: socket.create_connection(("::1", port), .25))
    blocked("loopback", lambda: socket.create_connection(("127.0.0.1", port), .25))
    blocked("metadata4", lambda: socket.create_connection((metadata4, port), .25))
    blocked("metadata6", lambda: socket.create_connection((metadata6, port), .25))
    blocked("dns_resolution", lambda: socket.getaddrinfo("wp86-nonexistent.invalid", 80))
    def udp():
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.settimeout(.25); s.sendto(b"dns",(host,port)); s.recv(4)
    blocked("dns_udp", udp)
    def tcp_dns():
        s=socket.create_connection((host,port),.25); s.sendall(b"dns"); s.recv(4)
    blocked("dns_tcp", tcp_dns)
    blocked("raw_url", lambda: urllib.request.urlopen("http://%s:%d/" % (host,port), timeout=.25).read())
    blocked("curl_subprocess", lambda: subprocess.run(["/usr/bin/curl","--max-time","1","http://%s:%d/"%(host,port)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
    blocked("wget_subprocess", lambda: subprocess.run(["/usr/bin/wget","-T","1","-qO-","http://%s:%d/"%(host,port)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
    assert all(attempts.values()), attempts
    print(json.dumps(attempts,sort_keys=True))
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
        self.socket.bind((address, port))
        self.socket.settimeout(.1)
        self.stop = False
        self.thread = threading.Thread(target=self._serve, daemon=True)

    def start(self):
        if self.socket.type == socket.SOCK_STREAM:
            self.socket.listen(8)
        self.thread.start()

    def _serve(self):
        while not self.stop:
            try:
                if self.socket.type == socket.SOCK_STREAM:
                    conn, _ = self.socket.accept()
                    with conn:
                        conn.recv(128)
                        conn.sendall(b"ok")
                else:
                    data, peer = self.socket.recvfrom(128)
                    self.socket.sendto(b"ok", peer)
            except (socket.timeout, OSError):
                pass

    def close(self):
        self.stop = True
        self.socket.close()
        self.thread.join(timeout=.5)


def _host_ipv4() -> str:
    for value in subprocess.check_output(["hostname", "-I"], text=True).split():
        if "." in value and not value.startswith("127."):
            return value
    return "127.0.0.1"


def _run(target: pathlib.Path, scratch: pathlib.Path, mode: str, *args: str, **limits):
    config = runner.SandboxConfig(
        target_root=str(target),
        scratch_root=str(scratch),
        command=["/usr/bin/python3", "/target/candidate.py", mode, *args],
        **limits,
    )
    return runner.run(config)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="optional JSON evidence locator outside candidate target")
    args = parser.parse_args(argv)
    if os.geteuid() != 0:
        print(json.dumps({"ok": False, "error": "trusted parent must run as root"}))
        return 2
    root = pathlib.Path(tempfile.mkdtemp(prefix="wp86-sandbox-selftest-", dir="/tmp"))
    target, scratch = root / "target", root / "scratch"
    target.mkdir(); scratch.mkdir()
    (target / "candidate.py").write_text(CANDIDATE, encoding="utf-8")
    (target / "data.txt").write_text("immutable\n", encoding="utf-8")
    guard = root / "guard.txt"; guard.write_text("guard\n", encoding="utf-8")
    (target / "escape").symlink_to(guard.parent, target_is_directory=True)
    before = (target / "data.txt").read_bytes(), guard.read_bytes()
    tests = []
    fixtures = []
    aliases = []
    try:
        def check(name, expected, result):
            passed = result.classification == expected and result.cleanup.get("descendants_gone") is True
            details = result.as_dict()
            details["stdout"] = {"bytes": len(result.stdout), "sha256": hashlib.sha256(result.stdout).hexdigest(), "preview": result.stdout[:256].decode("utf-8", "replace")}
            details["stderr"] = {"bytes": len(result.stderr), "sha256": hashlib.sha256(result.stderr).hexdigest(), "preview": result.stderr[:256].decode("utf-8", "replace")}
            tests.append({"name": name, "expected": expected, "actual": result.classification, "passed": passed, "result": details})

        check("healthy_positive_control", "ok", _run(target, scratch, "healthy"))

        saved = {k: os.environ.get(k) for k in ("GH_TOKEN", "GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
        try:
            for index, key in enumerate(saved): os.environ[key] = "WP86_SECRET_MARKER_%d" % index
            check("credential_env_argv_fd_procfs", "ok", _run(target, scratch, "credentials"))
        finally:
            for key, value in saved.items():
                if value is None: os.environ.pop(key, None)
                else: os.environ[key] = value

        host = _host_ipv4(); port = 43861
        metadata4, metadata6 = "169.254.169.254", "fd00:ec2::254"
        for family, address, prefix in ((socket.AF_INET, metadata4, "32"), (socket.AF_INET6, metadata6, "128")):
            version = "-4" if family == socket.AF_INET else "-6"
            added = subprocess.run(["ip", version, "addr", "add", "%s/%s" % (address, prefix), "dev", "lo"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
            if added: aliases.append((version, address, prefix))
        for family, address, socktype in ((socket.AF_INET,"0.0.0.0",socket.SOCK_STREAM),(socket.AF_INET,"0.0.0.0",socket.SOCK_DGRAM),(socket.AF_INET6,"::",socket.SOCK_STREAM)):
            try:
                fixture=_Fixture(family,address,port,socktype); fixture.start(); fixtures.append(fixture)
            except OSError:
                pass
        control = socket.create_connection((host, port), .5)
        control.sendall(b"control"); assert control.recv(2) == b"ok"; control.close()
        if any(item[1] == metadata4 for item in aliases):
            control = socket.create_connection((metadata4, port), .5); control.close()
        check("network_dns_loopback_metadata", "ok", _run(target, scratch, "network", host, str(port), metadata4, metadata6))

        check("target_readonly_escape_and_links", "ok", _run(target, scratch, "filesystem", str(guard)))
        assert ((target / "data.txt").read_bytes(), guard.read_bytes()) == before
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
    report = {"ok": passed == len(tests) and bool(tests), "passed": passed, "total": len(tests), "tests": tests}
    if args.output:
        output = pathlib.Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
