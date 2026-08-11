"""Trusted-parent Linux sandbox for untrusted candidate commands.

The boundary is deliberately OS-backed.  Python monkeypatches are not treated as
security controls: the parent creates user, mount, PID and network namespaces,
an isolated chroot, a read-only candidate bind mount and a cgroup-v2 envelope.
The final process runs as uid/gid 1000 with no capability and no-new-privileges.

This module never imports candidate code.  Candidate paths are data and are only
executed after the namespace/chroot/cgroup boundary is established.
"""

from __future__ import annotations

import argparse
import base64
import ctypes
import dataclasses
import json
import os
import pathlib
import re
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from typing import Iterable, Mapping, Sequence

try:
    import resource
except ImportError:  # Windows: fingerprint() reports the named unsupported platform.
    resource = None  # type: ignore[assignment]


class SandboxError(RuntimeError):
    """A fail-closed sandbox setup or execution failure."""


class PlatformUnsupported(SandboxError):
    """The current platform cannot provide the required kernel boundary."""


_REQUIRED_TOOLS = ("unshare", "mount", "umount", "chroot")
_REQUIRED_CONTROLLERS = frozenset({"cpu", "memory", "pids"})
_SAFE_ENV = {
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "HOME": "/scratch/home",
    "TMPDIR": "/scratch/tmp",
    "GIT_CONFIG_NOSYSTEM": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONUNBUFFERED": "1",
}
_SECRET_VALUE = re.compile(
    r"(?i)(?:github_pat_|gh[pousr]_|bearer\s+|basic\s+|sk-[a-z0-9]|"
    r"AKIA[0-9A-Z]{8,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)


@dataclasses.dataclass(frozen=True)
class SandboxConfig:
    target_root: str
    scratch_root: str
    command: Sequence[str]
    timeout_seconds: float = 8.0
    memory_bytes: int = 64 * 1024 * 1024
    pids_max: int = 16
    cpu_quota_us: int = 50_000
    cpu_period_us: int = 100_000
    cpu_seconds: int = 2
    output_bytes: int = 65_536
    expected_distro: str | None = "Ubuntu 24.04.4 LTS"
    expected_kernel: str | None = "6.18.33.2-microsoft-standard-WSL2"


@dataclasses.dataclass(frozen=True)
class SandboxResult:
    ok: bool
    classification: str
    returncode: int
    stdout: bytes
    stderr: bytes
    elapsed_seconds: float
    output_truncated: bool
    fingerprint: Mapping[str, object]
    resource_report: Mapping[str, object]
    cleanup: Mapping[str, object]

    def as_dict(self) -> dict[str, object]:
        data = dataclasses.asdict(self)
        data["stdout"] = self.stdout.decode("utf-8", "replace")
        data["stderr"] = self.stderr.decode("utf-8", "replace")
        return data


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read().strip()


def _os_release() -> dict[str, str]:
    result: dict[str, str] = {}
    for line in _read_text("/etc/os-release").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key] = value.strip().strip('"')
    return result


def fingerprint() -> dict[str, object]:
    """Return a machine-readable runner fingerprint, failing on weak platforms."""
    if not sys.platform.startswith("linux"):
        raise PlatformUnsupported("PlatformUnsupported: Linux namespaces are required")
    if os.geteuid() != 0:
        raise PlatformUnsupported("PlatformUnsupported: trusted parent must run as root")
    try:
        fs_type = subprocess.check_output(
            ["stat", "-fc", "%T", "/sys/fs/cgroup"], text=True
        ).strip()
        controllers = set(_read_text("/sys/fs/cgroup/cgroup.controllers").split())
    except (OSError, subprocess.SubprocessError) as exc:
        raise PlatformUnsupported("PlatformUnsupported: cgroup v2 is unavailable") from exc
    if fs_type != "cgroup2fs":
        raise PlatformUnsupported("PlatformUnsupported: cgroup v2 is required, got %s" % fs_type)
    missing = sorted(_REQUIRED_CONTROLLERS - controllers)
    if missing:
        raise PlatformUnsupported(
            "PlatformUnsupported: missing cgroup controllers: %s" % ", ".join(missing)
        )
    absent = [tool for tool in _REQUIRED_TOOLS if shutil.which(tool) is None]
    if absent:
        raise PlatformUnsupported(
            "PlatformUnsupported: required tools missing: %s" % ", ".join(absent)
        )
    release = _os_release()
    return {
        "platform": "linux",
        "distro": release.get("PRETTY_NAME", "unknown"),
        "distro_id": release.get("ID", "unknown"),
        "kernel": os.uname().release,
        "architecture": os.uname().machine,
        "cgroup": "v2",
        "cgroup_controllers": sorted(controllers),
        "parent_uid": os.geteuid(),
        "tools": {tool: shutil.which(tool) for tool in _REQUIRED_TOOLS},
    }


def _validate_config(config: SandboxConfig, fp: Mapping[str, object]) -> tuple[str, str]:
    target = os.path.realpath(os.path.abspath(config.target_root))
    scratch = os.path.realpath(os.path.abspath(config.scratch_root))
    if not os.path.isdir(target):
        raise SandboxError("target_root is not a directory: %s" % target)
    if os.path.commonpath([target, scratch]) == target:
        raise SandboxError("scratch_root must be outside target_root")
    if os.path.commonpath([target, scratch]) == scratch:
        raise SandboxError("target_root must be outside scratch_root")
    if not config.command or not all(isinstance(part, str) and part for part in config.command):
        raise SandboxError("command must be a non-empty sequence of non-empty strings")
    if any(_SECRET_VALUE.search(part) for part in config.command):
        raise SandboxError("candidate argv contains credential-shaped material")
    numeric = {
        "timeout_seconds": config.timeout_seconds,
        "memory_bytes": config.memory_bytes,
        "pids_max": config.pids_max,
        "cpu_quota_us": config.cpu_quota_us,
        "cpu_period_us": config.cpu_period_us,
        "cpu_seconds": config.cpu_seconds,
        "output_bytes": config.output_bytes,
    }
    if any(isinstance(value, bool) or value <= 0 for value in numeric.values()):
        raise SandboxError("all resource limits must be positive")
    if config.expected_distro and fp["distro"] != config.expected_distro:
        raise PlatformUnsupported(
            "PlatformUnsupported: distro drift: expected %r, got %r"
            % (config.expected_distro, fp["distro"])
        )
    if config.expected_kernel and fp["kernel"] != config.expected_kernel:
        raise PlatformUnsupported(
            "PlatformUnsupported: kernel drift: expected %r, got %r"
            % (config.expected_kernel, fp["kernel"])
        )
    return target, scratch


def _write(path: str, value: object) -> None:
    with open(path, "w", encoding="ascii") as handle:
        handle.write(str(value))


def _read_kv(path: str) -> dict[str, int]:
    try:
        lines = _read_text(path).splitlines()
    except OSError:
        return {}
    result: dict[str, int] = {}
    for line in lines:
        fields = line.split()
        if len(fields) == 2:
            try:
                result[fields[0]] = int(fields[1])
            except ValueError:
                pass
    return result


class _Cgroup:
    def __init__(self, config: SandboxConfig):
        self.path = os.path.join("/sys/fs/cgroup", "wp86-%s" % uuid.uuid4().hex)
        os.mkdir(self.path, 0o700)
        _write(os.path.join(self.path, "memory.max"), config.memory_bytes)
        swap = os.path.join(self.path, "memory.swap.max")
        if os.path.exists(swap):
            _write(swap, 0)
        _write(os.path.join(self.path, "pids.max"), config.pids_max)
        _write(
            os.path.join(self.path, "cpu.max"),
            "%d %d" % (config.cpu_quota_us, config.cpu_period_us),
        )

    def attach_self_preexec(self) -> None:
        os.setsid()
        _write(os.path.join(self.path, "cgroup.procs"), os.getpid())

    def kill(self) -> None:
        kill_path = os.path.join(self.path, "cgroup.kill")
        if os.path.exists(kill_path):
            try:
                _write(kill_path, 1)
                return
            except OSError:
                pass
        for raw_pid in _read_text(os.path.join(self.path, "cgroup.procs")).split():
            try:
                os.kill(int(raw_pid), signal.SIGKILL)
            except (ValueError, ProcessLookupError, PermissionError):
                pass

    def report(self) -> dict[str, object]:
        return {
            "memory_max": _read_text(os.path.join(self.path, "memory.max")),
            "pids_max": _read_text(os.path.join(self.path, "pids.max")),
            "cpu_max": _read_text(os.path.join(self.path, "cpu.max")),
            "memory_events": _read_kv(os.path.join(self.path, "memory.events")),
            "pids_events": _read_kv(os.path.join(self.path, "pids.events")),
            "cpu_stat": _read_kv(os.path.join(self.path, "cpu.stat")),
            "remaining_pids": _read_text(os.path.join(self.path, "cgroup.procs")).split(),
        }

    def cleanup(self) -> dict[str, object]:
        self.kill()
        deadline = time.monotonic() + 2.0
        remaining: list[str] = []
        while time.monotonic() < deadline:
            remaining = _read_text(os.path.join(self.path, "cgroup.procs")).split()
            if not remaining:
                break
            time.sleep(0.02)
        removed = False
        try:
            os.rmdir(self.path)
            removed = True
        except OSError:
            removed = False
        return {"cgroup_empty": not remaining, "cgroup_removed": removed, "remaining_pids": remaining}


def _mount(*args: str) -> None:
    completed = subprocess.run(["mount", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed.returncode:
        raise SandboxError(
            "mount failed (%s): %s"
            % (" ".join(args), completed.stderr.decode("utf-8", "replace").strip())
        )


def _mkdir(path: str, mode: int = 0o755) -> None:
    os.makedirs(path, mode=mode, exist_ok=True)


def _bind_readonly(source: str, destination: str) -> None:
    _mkdir(destination)
    _mount("--bind", source, destination)
    _mount("-o", "remount,bind,ro,nosuid,nodev", destination)


def _drop_bounding_set(libc) -> None:
    PR_CAPBSET_DROP = 24
    for capability in range(0, 64):
        libc.prctl(PR_CAPBSET_DROP, capability, 0, 0, 0)


def _enter_final_user_namespace() -> None:
    """Create the final user namespace without depending on ``newuidmap``.

    Ubuntu-Clean intentionally has no setuid ``newuidmap`` helper.  The trusted
    parent already owns the other namespaces and performs all mounts first.  It
    then becomes the ordinary outer uid/gid and creates a one-id nested user
    namespace.  Its still-root namespace-init parent installs the one-id map;
    Linux intentionally does not permit the child to authorize its own map.
    """
    libc = ctypes.CDLL(None, use_errno=True)
    CLONE_NEWUSER = 0x10000000
    if libc.unshare(CLONE_NEWUSER) != 0:
        errno_value = ctypes.get_errno()
        raise SandboxError("cannot create final user namespace: errno %d" % errno_value)
def _clear_privileges_and_chroot(rootfs: str) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    PR_SET_NO_NEW_PRIVS = 38
    PR_CAP_AMBIENT = 47
    PR_CAP_AMBIENT_CLEAR_ALL = 4
    # The fresh namespace still has CAP_SYS_CHROOT in its own user namespace.
    # Use it once, then erase every capability before candidate exec.
    # The trusted init placed cwd at rootfs before changing outer uid.  Using
    # '.' avoids re-traversing root-owned /tmp ancestors as outer uid 1000.
    os.chroot(".")
    os.chdir("/scratch")
    # A freshly-created user namespace grants capabilities in that namespace.
    # Drop its bounding and effective/permitted/inheritable sets as well.
    _drop_bounding_set(libc)
    libc.prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_CLEAR_ALL, 0, 0, 0)
    class _CapHeader(ctypes.Structure):
        _fields_ = [("version", ctypes.c_uint32), ("pid", ctypes.c_int)]
    class _CapData(ctypes.Structure):
        _fields_ = [
            ("effective", ctypes.c_uint32),
            ("permitted", ctypes.c_uint32),
            ("inheritable", ctypes.c_uint32),
        ]
    header = _CapHeader(0x20080522, 0)
    data = (_CapData * 2)()
    if libc.capset(ctypes.byref(header), ctypes.byref(data)) != 0:
        raise SandboxError("cannot clear capability sets")
    if libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        raise SandboxError("cannot set no_new_privs")


def _launch_final_candidate(spec: Mapping[str, object], rootfs: str) -> int:
    """Fork the non-root userns child and install its map from the trusted init."""
    ready_r, ready_w = os.pipe()
    go_r, go_w = os.pipe()
    pid = os.fork()
    if pid == 0:
        try:
            os.close(ready_r); os.close(go_w)
            os.chdir(rootfs)
            os.setgroups([])
            os.setgid(1000)
            os.setuid(1000)
            _enter_final_user_namespace()
            os.write(ready_w, b"1")
            os.close(ready_w)
            if os.read(go_r, 1) != b"1":
                raise SandboxError("trusted parent did not install user namespace map")
            os.close(go_r)
            _clear_privileges_and_chroot(rootfs)
            resource.setrlimit(resource.RLIMIT_CPU, (spec["cpu_seconds"], spec["cpu_seconds"]))
            resource.setrlimit(resource.RLIMIT_FSIZE, (spec["output_bytes"], spec["output_bytes"]))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
            command = spec["command"]
            os.execvpe(command[0], command, _SAFE_ENV)
        except BaseException as exc:
            print("sandbox final child failed: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
            os._exit(125)
    os.close(ready_w); os.close(go_r)
    try:
        if os.read(ready_r, 1) != b"1":
            raise SandboxError("final child failed before user namespace map request")
        proc_dir = os.path.join(rootfs, "proc", str(pid))
        try:
            _write(os.path.join(proc_dir, "setgroups"), "deny")
        except OSError:
            pass
        _write(os.path.join(proc_dir, "uid_map"), "1000 1000 1\n")
        _write(os.path.join(proc_dir, "gid_map"), "1000 1000 1\n")
        os.write(go_w, b"1")
    finally:
        os.close(ready_r); os.close(go_w)
    _, status_value = os.waitpid(pid, 0)
    if os.WIFEXITED(status_value):
        return os.WEXITSTATUS(status_value)
    if os.WIFSIGNALED(status_value):
        return 128 + os.WTERMSIG(status_value)
    return 125


def _child_init(encoded: str) -> int:
    """Namespace init.  Called only by the trusted parent through ``unshare``."""
    spec = json.loads(base64.urlsafe_b64decode(encoded.encode("ascii")).decode("utf-8"))
    rootfs = spec["rootfs"]
    target = spec["target"]
    writable = spec["writable"]
    _mount("--make-rprivate", "/")
    _mkdir(rootfs, 0o700)
    _mount("-t", "tmpfs", "-o", "mode=0755,nosuid,nodev", "tmpfs", rootfs)
    for name in ("target", "scratch", "proc", "dev", "etc", "usr", "bin", "lib", "lib64"):
        _mkdir(os.path.join(rootfs, name))
    for source in ("/usr", "/bin", "/lib", "/lib64"):
        if os.path.exists(source):
            _bind_readonly(source, os.path.join(rootfs, source.lstrip("/")))
    _bind_readonly(target, os.path.join(rootfs, "target"))
    _mkdir(writable, 0o700)
    os.chown(writable, 1000, 1000)
    _mount("--bind", writable, os.path.join(rootfs, "scratch"))
    _mount("-o", "remount,bind,rw,nosuid,nodev", os.path.join(rootfs, "scratch"))
    os.chown(os.path.join(rootfs, "scratch"), 1000, 1000)
    _mkdir(os.path.join(rootfs, "scratch", "home"), 0o700)
    _mkdir(os.path.join(rootfs, "scratch", "tmp"), 0o700)
    os.chown(os.path.join(rootfs, "scratch", "home"), 1000, 1000)
    os.chown(os.path.join(rootfs, "scratch", "tmp"), 1000, 1000)
    _mount("-t", "proc", "-o", "nosuid,nodev,noexec,hidepid=2", "proc", os.path.join(rootfs, "proc"))
    _mount("-t", "tmpfs", "-o", "mode=0755,nosuid,noexec", "tmpfs", os.path.join(rootfs, "dev"))
    for name, mode, major, minor in (
        ("null", stat.S_IFCHR | 0o666, 1, 3),
        ("zero", stat.S_IFCHR | 0o666, 1, 5),
        ("random", stat.S_IFCHR | 0o444, 1, 8),
        ("urandom", stat.S_IFCHR | 0o444, 1, 9),
    ):
        os.mknod(os.path.join(rootfs, "dev", name), mode, os.makedev(major, minor))
    for name in ("hosts", "nsswitch.conf", "resolv.conf", "ld.so.cache"):
        source = os.path.join("/etc", name)
        if os.path.isfile(source):
            shutil.copyfile(source, os.path.join(rootfs, "etc", name))
            os.chmod(os.path.join(rootfs, "etc", name), 0o444)
    return _launch_final_candidate(spec, rootfs)


def _bounded_communicate(
    process: subprocess.Popen[bytes], cgroup: _Cgroup, timeout: float, output_limit: int
) -> tuple[bytes, bytes, str | None, bool]:
    selector = selectors.DefaultSelector()
    buffers: dict[str, bytearray] = {"stdout": bytearray(), "stderr": bytearray()}
    for name, stream in (("stdout", process.stdout), ("stderr", process.stderr)):
        if stream is not None:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
    start = time.monotonic()
    forced: str | None = None
    truncated = False
    while selector.get_map() or process.poll() is None:
        if forced is None and time.monotonic() - start > timeout:
            forced = "timeout"
            cgroup.kill()
        for key, _ in selector.select(0.03):
            try:
                chunk = os.read(key.fileobj.fileno(), 16_384)
            except BlockingIOError:
                continue
            if not chunk:
                selector.unregister(key.fileobj)
                key.fileobj.close()
                continue
            total_before = len(buffers["stdout"]) + len(buffers["stderr"])
            keep = max(0, output_limit - total_before)
            buffers[key.data].extend(chunk[:keep])
            if len(chunk) > keep and forced is None:
                forced = "output_limit"
                truncated = True
                cgroup.kill()
        if process.poll() is not None and not selector.get_map():
            break
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        cgroup.kill()
        process.wait(timeout=1)
    return bytes(buffers["stdout"]), bytes(buffers["stderr"]), forced, truncated


def _classification(
    returncode: int, forced: str | None, report: Mapping[str, object], cpu_seconds: int
) -> str:
    memory_events = report.get("memory_events", {})
    pids_events = report.get("pids_events", {})
    cpu_stat = report.get("cpu_stat", {})
    if forced == "output_limit":
        return forced
    if isinstance(memory_events, Mapping) and memory_events.get("oom_kill", 0):
        return "memory_limit"
    if isinstance(pids_events, Mapping) and pids_events.get("max", 0):
        return "pid_limit"
    if (
        returncode in (-signal.SIGKILL, -signal.SIGXCPU, 128 + signal.SIGKILL, 128 + signal.SIGXCPU)
        and isinstance(cpu_stat, Mapping)
        and cpu_stat.get("usage_usec", 0) >= cpu_seconds * 800_000
    ):
        return "cpu_limit"
    if forced:
        return forced
    return "ok" if returncode == 0 else "candidate_error"


def run(config: SandboxConfig) -> SandboxResult:
    """Execute a candidate command inside the required Linux boundary."""
    fp = fingerprint()
    target, scratch = _validate_config(config, fp)
    os.makedirs(scratch, exist_ok=True)
    run_root = tempfile.mkdtemp(prefix="wp86-sandbox-", dir=scratch)
    os.chmod(run_root, 0o700)
    writable = os.path.join(run_root, "writable")
    rootfs = os.path.join(run_root, "rootfs")
    cgroup = _Cgroup(config)
    spec = {
        "target": target,
        "rootfs": rootfs,
        "writable": writable,
        "command": list(config.command),
        "cpu_seconds": config.cpu_seconds,
        "output_bytes": config.output_bytes,
    }
    encoded = base64.urlsafe_b64encode(
        json.dumps(spec, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).decode("ascii")
    argv = [
        "unshare",
        "--fork",
        "--kill-child=KILL",
        "--mount",
        "--pid",
        "--net",
        "--ipc",
        "--uts",
        sys.executable,
        os.path.abspath(__file__),
        "--child-init",
        encoded,
    ]
    start = time.monotonic()
    process: subprocess.Popen[bytes] | None = None
    resource_report: dict[str, object] = {}
    cleanup: dict[str, object] = {}
    stdout = b""
    stderr = b""
    forced: str | None = None
    truncated = False
    returncode = 125
    try:
        process = subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=run_root,
            env=dict(_SAFE_ENV),
            close_fds=True,
            preexec_fn=cgroup.attach_self_preexec,
        )
        stdout, stderr, forced, truncated = _bounded_communicate(
            process, cgroup, config.timeout_seconds, config.output_bytes
        )
        returncode = process.returncode
        resource_report = cgroup.report()
    finally:
        cleanup.update(cgroup.cleanup())
        try:
            shutil.rmtree(run_root)
            cleanup["scratch_removed"] = True
        except OSError as exc:
            cleanup["scratch_removed"] = False
            cleanup["scratch_error"] = str(exc)
        cleanup["descendants_gone"] = bool(cleanup.get("cgroup_empty"))
    classification = _classification(returncode, forced, resource_report, config.cpu_seconds)
    ok = (
        classification == "ok"
        and cleanup.get("descendants_gone") is True
        and cleanup.get("scratch_removed") is True
    )
    return SandboxResult(
        ok=ok,
        classification=classification,
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        elapsed_seconds=round(time.monotonic() - start, 6),
        output_truncated=truncated,
        fingerprint=fp,
        resource_report=resource_report,
        cleanup=cleanup,
    )


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--child-init")
    args = parser.parse_args(argv)
    if args.child_init:
        try:
            return _child_init(args.child_init)
        except BaseException as exc:
            print("sandbox child setup failed: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
            return 125
    return 64


if __name__ == "__main__":
    raise SystemExit(_main())
