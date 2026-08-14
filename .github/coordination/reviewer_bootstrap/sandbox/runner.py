"""Trusted-parent Linux sandbox with measured OS-backed containment.

The parent creates cgroup-v2 limits plus mount, PID, network, IPC, UTS and
user namespaces.  Candidate code is imported nowhere.  It executes only after
the child has stopped with uid/gid 1000, empty capability sets, NoNewPrivs=1,
a read-only target, and an observed descriptor inventory.
"""

from __future__ import annotations

import argparse
import base64
import ctypes
import dataclasses
import hashlib
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
from typing import Mapping, Sequence

try:
    import resource
except ImportError:
    resource = None  # type: ignore[assignment]

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))
from oracle.trusted_inventory import RUNNER_REQUIREMENTS  # noqa: E402

SIGKILL_VALUE = int(getattr(signal, "SIGKILL", 9))
SIGXCPU_VALUE = int(getattr(signal, "SIGXCPU", 24))
BOUNDARY_SETUP_TIMEOUT_SECONDS = 20.0

SAFE_ENV = {
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "HOME": "/scratch/home",
    "TMPDIR": "/scratch/tmp",
    "GIT_CONFIG_NOSYSTEM": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONUNBUFFERED": "1",
}
REQUIRED_TOOLS = ("unshare", "mount", "umount", "chroot", "ip")
SECRET_VALUE = re.compile(
    r"(?:AKIA|ASIA)[0-9A-Z]{8,}|"
    r"(?i:github_pat_|gh[pousr]_|bearer\s+|basic\s+|sk-[a-z0-9]|"
    r"xox[baprs]-|gocspx-|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
CREDENTIAL_NAME = re.compile(
    r"(?i)(?:^|[_-])(?:token|secret|pass(?:word|wd)?|credential|api[_-]?key|"
    r"access[_-]?key|private[_-]?key|oauth|github|gitlab|anthropic|openai|"
    r"aws|azure|gcp|google|stripe|slack)(?:$|[_-])"
)


class SandboxError(RuntimeError):
    """A fail-closed sandbox configuration, setup, or evidence failure."""


class PlatformUnsupported(SandboxError):
    """The host cannot provide the Packet's required kernel boundary."""


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
    retained_output_paths: Sequence[str] = ()
    scratch_input_files: Mapping[str, str] = dataclasses.field(default_factory=dict)
    resolv_conf_text: str | None = None


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
    boundary: Mapping[str, object]
    termination: Mapping[str, object]
    resource_report: Mapping[str, object]
    cleanup: Mapping[str, object]
    retained_outputs: Mapping[str, bytes]

    def as_dict(self) -> dict[str, object]:
        value = dataclasses.asdict(self)
        value["stdout"] = {
            "bytes": len(self.stdout),
            "sha256": hashlib.sha256(self.stdout).hexdigest(),
            "text": self.stdout.decode("utf-8", "replace"),
        }
        value["stderr"] = {
            "bytes": len(self.stderr),
            "sha256": hashlib.sha256(self.stderr).hexdigest(),
            "text": self.stderr.decode("utf-8", "replace"),
        }
        value["retained_outputs"] = {
            name: {
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "text": data.decode("utf-8", "replace"),
            }
            for name, data in self.retained_outputs.items()
        }
        return value


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read().strip()


def _write_text(path: str, value: object) -> None:
    with open(path, "w", encoding="ascii") as handle:
        handle.write(str(value))


def _read_kv(path: str) -> dict[str, int]:
    try:
        lines = _read_text(path).splitlines()
    except OSError:
        return {}
    result = {}
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            try:
                result[parts[0]] = int(parts[1])
            except ValueError:
                continue
    return result


def _os_release() -> dict[str, str]:
    result = {}
    for line in _read_text("/etc/os-release").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value.strip().strip('"')
    return result


def fingerprint() -> dict[str, object]:
    if not sys.platform.startswith("linux"):
        raise PlatformUnsupported("PlatformUnsupported: Linux namespaces are required")
    if not hasattr(os, "geteuid") or os.geteuid() != RUNNER_REQUIREMENTS["parent_uid"]:
        raise PlatformUnsupported("PlatformUnsupported: trusted parent uid must be zero")
    if not hasattr(os, "getegid") or os.getegid() != RUNNER_REQUIREMENTS["parent_gid"]:
        raise PlatformUnsupported("PlatformUnsupported: trusted parent gid must be zero")
    try:
        fs_type = subprocess.check_output(["stat", "-fc", "%T", "/sys/fs/cgroup"], text=True).strip()
        controllers = set(_read_text("/sys/fs/cgroup/cgroup.controllers").split())
        subtree = set(item.lstrip("+") for item in _read_text("/sys/fs/cgroup/cgroup.subtree_control").split())
    except (OSError, subprocess.SubprocessError) as exc:
        raise PlatformUnsupported("PlatformUnsupported: cgroup v2 is unavailable") from exc
    required = set(RUNNER_REQUIREMENTS["cgroup_controllers"])
    if fs_type != RUNNER_REQUIREMENTS["cgroup_filesystem"]:
        raise PlatformUnsupported("PlatformUnsupported: cgroup v2 filesystem mismatch: %s" % fs_type)
    if not required.issubset(controllers):
        raise PlatformUnsupported("PlatformUnsupported: missing cgroup controllers: %s" % sorted(required - controllers))
    absent = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
    if absent:
        raise PlatformUnsupported("PlatformUnsupported: required tools missing: %s" % absent)
    release = _os_release()
    measured = {
        "platform": "linux",
        "distro": release.get("PRETTY_NAME", "unknown"),
        "kernel": os.uname().release,
        "architecture": os.uname().machine,
        "cgroup_filesystem": fs_type,
        "cgroup_controllers": sorted(controllers),
        "cgroup_subtree_control": sorted(subtree),
        "cgroup_parent_writable": os.access("/sys/fs/cgroup", os.W_OK),
        "parent_uid": os.geteuid(),
        "parent_gid": os.getegid(),
        "tools": {tool: shutil.which(tool) for tool in REQUIRED_TOOLS},
    }
    for key in ("distro", "kernel", "parent_uid", "parent_gid"):
        if measured[key] != RUNNER_REQUIREMENTS[key]:
            raise PlatformUnsupported(
                "PlatformUnsupported: %s drift: expected %r got %r"
                % (key, RUNNER_REQUIREMENTS[key], measured[key])
            )
    if not measured["cgroup_parent_writable"]:
        raise PlatformUnsupported("PlatformUnsupported: cgroup parent is not writable")
    return measured


def _safe_locator(locator: object) -> str:
    if not isinstance(locator, str) or not locator or "\\" in locator or os.path.isabs(locator):
        raise SandboxError("unsafe scratch locator: %r" % (locator,))
    if any(part in ("", ".", "..") for part in locator.split("/")):
        raise SandboxError("unsafe scratch locator: %r" % (locator,))
    if ":" in locator or any(ord(character) < 32 for character in locator):
        raise SandboxError("non-portable scratch locator: %r" % (locator,))
    return locator


def _validate_config(config: SandboxConfig, measured: Mapping[str, object]) -> tuple[str, str]:
    target = os.path.realpath(os.path.abspath(config.target_root))
    scratch = os.path.realpath(os.path.abspath(config.scratch_root))
    if not os.path.isdir(target) or not os.path.isdir(scratch):
        raise SandboxError("target_root and scratch_root must already be directories")
    try:
        if os.path.commonpath([target, scratch]) in (target, scratch):
            raise SandboxError("target_root and scratch_root must not contain each other")
    except ValueError as exc:
        raise SandboxError("target_root and scratch_root must share a filesystem namespace") from exc
    if not config.command or not all(isinstance(item, str) and item for item in config.command):
        raise SandboxError("command must be a non-empty string sequence")
    if any(SECRET_VALUE.search(item) for item in config.command):
        raise SandboxError("candidate argv contains credential-shaped material")
    for locator in tuple(config.retained_output_paths) + tuple(config.scratch_input_files):
        _safe_locator(locator)
    for locator, content in config.scratch_input_files.items():
        if not isinstance(content, str) or len(content.encode("utf-8")) > config.output_bytes:
            raise SandboxError("unsafe or oversized scratch input: %s" % locator)
    if config.resolv_conf_text is not None:
        if not isinstance(config.resolv_conf_text, str) or not config.resolv_conf_text or "\0" in config.resolv_conf_text:
            raise SandboxError("unsafe resolv.conf fixture")
        if len(config.resolv_conf_text.encode("utf-8")) > 4096 or SECRET_VALUE.search(config.resolv_conf_text):
            raise SandboxError("unsafe resolv.conf fixture")
    limits = (
        config.timeout_seconds,
        config.memory_bytes,
        config.pids_max,
        config.cpu_quota_us,
        config.cpu_period_us,
        config.cpu_seconds,
        config.output_bytes,
    )
    if any(isinstance(value, bool) or value <= 0 for value in limits):
        raise SandboxError("all resource limits must be positive")
    return target, scratch


def _pid_identity(pid: int) -> str | None:
    try:
        fields = _read_text("/proc/%d/stat" % pid).split()
        return fields[21] if len(fields) > 21 else None
    except OSError:
        return None


class _Cgroup:
    def __init__(self, config: SandboxConfig):
        root = "/sys/fs/cgroup"
        required = tuple(RUNNER_REQUIREMENTS["cgroup_controllers"])
        try:
            enabled = set(item.lstrip("+") for item in _read_text(os.path.join(root, "cgroup.subtree_control")).split())
            missing = [name for name in required if name not in enabled]
            if missing:
                _write_text(os.path.join(root, "cgroup.subtree_control"), " ".join("+" + name for name in missing))
        except OSError as exc:
            raise PlatformUnsupported("PlatformUnsupported: cannot delegate cgroup controllers: %s" % exc) from exc
        self.path = os.path.join(root, "wp99-%s" % uuid.uuid4().hex)
        self.observed: dict[int, str | None] = {}
        os.mkdir(self.path, 0o700)
        try:
            _write_text(os.path.join(self.path, "memory.max"), config.memory_bytes)
            swap = os.path.join(self.path, "memory.swap.max")
            if os.path.exists(swap):
                _write_text(swap, 0)
            _write_text(os.path.join(self.path, "pids.max"), config.pids_max)
            _write_text(
                os.path.join(self.path, "cpu.max"),
                "%d %d" % (config.cpu_quota_us, config.cpu_period_us),
            )
        except BaseException:
            try:
                os.rmdir(self.path)
            except OSError:
                pass
            raise

    def attach(self, pid: int) -> None:
        _write_text(os.path.join(self.path, "cgroup.procs"), pid)

    def observe(self, pid: int) -> None:
        if pid not in self.observed:
            self.observed[pid] = _pid_identity(pid)

    def observe_current(self) -> None:
        for pid in self.pids():
            self.observe(pid)

    def pids(self) -> list[int]:
        try:
            return [int(value) for value in _read_text(os.path.join(self.path, "cgroup.procs")).split()]
        except (OSError, ValueError):
            return []

    def kill(self) -> None:
        kill_path = os.path.join(self.path, "cgroup.kill")
        try:
            _write_text(kill_path, 1)
            return
        except OSError:
            pass
        for pid in self.pids():
            try:
                os.kill(pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                continue

    def report(self) -> dict[str, object]:
        return {
            "memory_max": _read_text(os.path.join(self.path, "memory.max")),
            "pids_max": _read_text(os.path.join(self.path, "pids.max")),
            "cpu_max": _read_text(os.path.join(self.path, "cpu.max")),
            "memory_events": _read_kv(os.path.join(self.path, "memory.events")),
            "pids_events": _read_kv(os.path.join(self.path, "pids.events")),
            "cpu_stat": _read_kv(os.path.join(self.path, "cpu.stat")),
            "pids_at_report": self.pids(),
        }

    def cleanup(self) -> dict[str, object]:
        self.observe_current()
        observed = dict(self.observed)
        self.kill()
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline and self.pids():
            time.sleep(0.02)
        remaining = self.pids()
        events = _read_kv(os.path.join(self.path, "cgroup.events"))
        cgroup_empty = events.get("populated") == 0 and not remaining
        descendants = {
            str(pid): (_pid_identity(pid) is None or _pid_identity(pid) != identity)
            for pid, identity in observed.items()
        }
        descendants_gone = bool(observed) and all(descendants.values())
        removed = False
        removal_error = None
        removal_attempts = 0
        removal_deadline = time.monotonic() + 2.0
        while True:
            removal_attempts += 1
            try:
                os.rmdir(self.path)
                removed = True
                removal_error = None
                break
            except FileNotFoundError:
                removed = True
                removal_error = None
                break
            except OSError as exc:
                removal_error = "%s: %s" % (type(exc).__name__, exc)
                if time.monotonic() >= removal_deadline:
                    break
                time.sleep(0.02)
        return {
            "cgroup_empty": cgroup_empty,
            "cgroup_empty_evidence": {"events": events, "remaining_pids": remaining},
            "descendants_gone": descendants_gone,
            "descendant_identity_checks": descendants,
            "observed_descendant_pids": sorted(observed),
            "cgroup_removed": removed,
            "cgroup_removal_attempts": removal_attempts,
            "cgroup_removal_error": removal_error,
        }


def _mount(*args: str) -> None:
    proc = subprocess.run(["mount", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SandboxError(
            "mount failed rc=%d (%s): %s"
            % (proc.returncode, " ".join(args), proc.stderr.decode("utf-8", "replace").strip())
        )


def _mkdir(path: str, mode: int = 0o755) -> None:
    os.makedirs(path, mode=mode, exist_ok=True)


def _bind_readonly(source: str, destination: str) -> None:
    _mkdir(destination)
    _mount("--bind", source, destination)
    _mount("-o", "remount,bind,ro,nosuid,nodev", destination)


def _drop_capabilities() -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    cap_last = int(_read_text("/proc/sys/kernel/cap_last_cap"))
    for capability in range(cap_last + 1):
        if libc.prctl(24, capability, 0, 0, 0) != 0:
            raise SandboxError("cannot drop capability %d from bounding set" % capability)
    if libc.prctl(47, 4, 0, 0, 0) != 0:
        raise SandboxError("cannot clear ambient capability set")

    class CapHeader(ctypes.Structure):
        _fields_ = [("version", ctypes.c_uint32), ("pid", ctypes.c_int)]

    class CapData(ctypes.Structure):
        _fields_ = [("effective", ctypes.c_uint32), ("permitted", ctypes.c_uint32), ("inheritable", ctypes.c_uint32)]

    header = CapHeader(0x20080522, 0)
    data = (CapData * 2)()
    if libc.capset(ctypes.byref(header), ctypes.byref(data)) != 0:
        raise SandboxError("cannot clear effective, permitted and inheritable capability sets")
    if libc.prctl(38, 1, 0, 0, 0) != 0:
        raise SandboxError("cannot set NoNewPrivs")


def _enter_user_namespace() -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.unshare(0x10000000) != 0:
        raise SandboxError("cannot create final user namespace: errno %d" % ctypes.get_errno())


def _status_fields(proc_root: str, pid: int) -> dict[str, object]:
    fields: dict[str, object] = {}
    for line in _read_text(os.path.join(proc_root, str(pid), "status")).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if key in ("Uid", "Gid", "Groups"):
            fields[key] = [int(item) for item in value.split()]
        elif key in ("CapPrm", "CapEff", "CapAmb", "CapBnd"):
            fields[key] = value
        elif key == "NoNewPrivs":
            fields[key] = int(value)
    return fields


def _boundary_observation(rootfs: str, pid: int) -> dict[str, object]:
    proc_root = os.path.join(rootfs, "proc")
    fd_root = os.path.join(proc_root, str(pid), "fd")
    descriptors = []
    for name in sorted(os.listdir(fd_root), key=int):
        try:
            target = os.readlink(os.path.join(fd_root, name))
        except OSError as exc:
            target = "unreadable:%s" % exc
        descriptors.append({"fd": int(name), "target": target})
    namespaces = {
        name: os.readlink(os.path.join(proc_root, str(pid), "ns", name))
        for name in ("user", "net", "pid", "mnt")
    }
    links = subprocess.run(["ip", "-brief", "link"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {
        "status": _status_fields(proc_root, pid),
        "namespaces": namespaces,
        "descriptor_inventory": descriptors,
        "network_links_rc": links.returncode,
        "network_links": links.stdout.splitlines(),
    }


def _close_candidate_descriptors() -> None:
    maximum = 1024
    if resource is not None:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        value = hard if hard not in (-1, resource.RLIM_INFINITY) else soft
        if value not in (-1, resource.RLIM_INFINITY):
            maximum = min(int(value), 1_048_576)
    os.closerange(3, maximum)


def _launch_candidate(spec: Mapping[str, object], rootfs: str, boundary_fd: int) -> int:
    ready_r, ready_w = os.pipe()
    go_r, go_w = os.pipe()
    pid = os.fork()
    if pid == 0:
        try:
            os.close(ready_r)
            os.close(go_w)
            os.chdir(rootfs)
            os.setgroups([])
            os.setgid(int(RUNNER_REQUIREMENTS["child_gid"]))
            os.setuid(int(RUNNER_REQUIREMENTS["child_uid"]))
            _enter_user_namespace()
            os.write(ready_w, b"1")
            os.close(ready_w)
            if os.read(go_r, 1) != b"1":
                raise SandboxError("trusted namespace parent did not install uid/gid maps")
            os.close(go_r)
            os.chroot(".")
            os.chdir("/scratch")
            _drop_capabilities()
            if resource is None:
                raise PlatformUnsupported("PlatformUnsupported: resource limits unavailable")
            cpu = int(spec["cpu_seconds"])
            output = int(spec["output_bytes"])
            resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 1))
            resource.setrlimit(resource.RLIMIT_FSIZE, (output, output))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
            _close_candidate_descriptors()
            os.kill(os.getpid(), signal.SIGSTOP)
            command = spec["command"]
            os.execvpe(command[0], command, SAFE_ENV)
        except BaseException as exc:
            print("sandbox final child failed: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
            os._exit(125)
    os.close(ready_w)
    os.close(go_r)
    try:
        if os.read(ready_r, 1) != b"1":
            raise SandboxError("final child failed before requesting uid/gid maps")
        proc_dir = os.path.join(rootfs, "proc", str(pid))
        try:
            _write_text(os.path.join(proc_dir, "setgroups"), "deny")
        except OSError:
            pass
        _write_text(os.path.join(proc_dir, "uid_map"), "1000 1000 1\n")
        _write_text(os.path.join(proc_dir, "gid_map"), "1000 1000 1\n")
        os.write(go_w, b"1")
    finally:
        os.close(ready_r)
        os.close(go_w)
    waited, stopped = os.waitpid(pid, os.WUNTRACED)
    if waited != pid or not os.WIFSTOPPED(stopped):
        raise SandboxError("final child did not stop for boundary measurement")
    boundary = _boundary_observation(rootfs, pid)
    os.write(boundary_fd, (json.dumps(boundary, sort_keys=True) + "\n").encode("utf-8"))
    os.close(boundary_fd)
    os.kill(pid, signal.SIGCONT)
    _, status_value = os.waitpid(pid, 0)
    if os.WIFEXITED(status_value):
        return os.WEXITSTATUS(status_value)
    if os.WIFSIGNALED(status_value):
        return 128 + os.WTERMSIG(status_value)
    return 125


def _child_init(encoded: str, boundary_fd: int) -> int:
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
    for name in ("home", "tmp"):
        destination = os.path.join(rootfs, "scratch", name)
        _mkdir(destination, 0o700)
        os.chown(destination, 1000, 1000)
    for locator, content in spec.get("scratch_input_files", {}).items():
        destination = os.path.join(rootfs, "scratch", *locator.split("/"))
        _mkdir(os.path.dirname(destination), 0o700)
        with open(destination, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.chown(destination, 1000, 1000)
        os.chmod(destination, 0o400)
    _mount("-t", "proc", "-o", "nosuid,nodev,noexec,hidepid=2", "proc", os.path.join(rootfs, "proc"))
    _mount("-t", "tmpfs", "-o", "mode=0755,nosuid,noexec", "tmpfs", os.path.join(rootfs, "dev"))
    # Keep the chroot's /dev empty.  Candidate stdio descriptors are inherited
    # and measured before exec; exposing writable device paths would create a
    # filesystem authority outside the resolved scratch root.
    for name in ("hosts", "nsswitch.conf", "ld.so.cache"):
        source = os.path.join("/etc", name)
        if os.path.isfile(source):
            shutil.copyfile(source, os.path.join(rootfs, "etc", name))
            os.chmod(os.path.join(rootfs, "etc", name), 0o444)
    resolv = spec.get("resolv_conf_text")
    resolv_path = os.path.join(rootfs, "etc", "resolv.conf")
    if resolv is not None:
        with open(resolv_path, "w", encoding="utf-8") as handle:
            handle.write(resolv)
    elif os.path.isfile("/etc/resolv.conf"):
        shutil.copyfile("/etc/resolv.conf", resolv_path)
    if os.path.exists(resolv_path):
        os.chmod(resolv_path, 0o444)
    return _launch_candidate(spec, rootfs, boundary_fd)


def _spawn_helper(encoded: str, boundary_fd: int, cgroup_path: str) -> int:
    _write_text(os.path.join(cgroup_path, "cgroup.procs"), os.getpid())
    os.setsid()
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
        str(pathlib.Path(__file__).resolve()),
        "--child-init",
        encoded,
        "--boundary-fd",
        str(boundary_fd),
    ]
    os.execvpe(argv[0], argv, SAFE_ENV)
    return 125


def _bounded_communicate(
    process: subprocess.Popen[bytes],
    cgroup: _Cgroup,
    boundary_r: int,
    timeout: float,
    output_limit: int,
) -> tuple[bytes, bytes, bytes, str | None, bool]:
    selector = selectors.DefaultSelector()
    buffers = {"stdout": bytearray(), "stderr": bytearray(), "boundary": bytearray()}
    for name, stream in (("stdout", process.stdout), ("stderr", process.stderr)):
        if stream is not None:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
    os.set_blocking(boundary_r, False)
    selector.register(boundary_r, selectors.EVENT_READ, "boundary")
    setup_started = time.monotonic()
    candidate_started = None
    forced = None
    truncated = False
    while selector.get_map() or process.poll() is None:
        cgroup.observe_current()
        now = time.monotonic()
        if forced is None:
            if candidate_started is not None and now - candidate_started > timeout:
                forced = "timeout"
                cgroup.kill()
            elif candidate_started is None and now - setup_started > BOUNDARY_SETUP_TIMEOUT_SECONDS:
                forced = "boundary_setup_timeout"
                cgroup.kill()
        for key, _event in selector.select(0.03):
            fd = key.fileobj if isinstance(key.fileobj, int) else key.fileobj.fileno()
            try:
                chunk = os.read(fd, 16_384)
            except BlockingIOError:
                continue
            if not chunk:
                selector.unregister(key.fileobj)
                if not isinstance(key.fileobj, int):
                    key.fileobj.close()
                else:
                    os.close(key.fileobj)
                continue
            if key.data == "boundary":
                buffers["boundary"].extend(chunk)
                if len(buffers["boundary"]) > 64 * 1024:
                    forced = "boundary_protocol_error"
                    cgroup.kill()
                elif candidate_started is None and b"\n" in buffers["boundary"]:
                    candidate_started = time.monotonic()
                continue
            total = len(buffers["stdout"]) + len(buffers["stderr"])
            keep = max(0, output_limit - total)
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
    if forced is None and b"\n" not in buffers["boundary"]:
        forced = "boundary_protocol_error"
    return bytes(buffers["stdout"]), bytes(buffers["stderr"]), bytes(buffers["boundary"]), forced, truncated


def classify_termination(
    returncode: int,
    forced: str | None,
    resource_report: Mapping[str, object],
) -> dict[str, object]:
    """Classify only from measured mechanisms; watchdog precedence is absolute."""
    if forced == "timeout":
        return {"classification": "timeout", "termination_source": "parent_watchdog", "signal": SIGKILL_VALUE, "limit_evidence": "watchdog_deadline_exceeded"}
    if forced == "output_limit":
        return {"classification": "output_limit", "termination_source": "parent_output_limiter", "signal": SIGKILL_VALUE, "limit_evidence": "captured_bytes_exceeded_limit"}
    if forced:
        return {"classification": "containment_error", "termination_source": "trusted_parent", "signal": None, "limit_evidence": forced}
    memory_events = resource_report.get("memory_events", {})
    if isinstance(memory_events, Mapping) and int(memory_events.get("oom_kill", 0)) > 0:
        return {"classification": "memory_limit", "termination_source": "cgroup_memory", "signal": SIGKILL_VALUE, "limit_evidence": "memory.events.oom_kill"}
    pids_events = resource_report.get("pids_events", {})
    if isinstance(pids_events, Mapping) and int(pids_events.get("max", 0)) > 0:
        return {"classification": "pid_limit", "termination_source": "cgroup_pids", "signal": None, "limit_evidence": "pids.events.max"}
    if returncode in (-SIGXCPU_VALUE, 128 + SIGXCPU_VALUE):
        return {"classification": "cpu_limit", "termination_source": "rlimit_cpu", "signal": SIGXCPU_VALUE, "limit_evidence": "returncode_SIGXCPU"}
    if returncode == 0:
        return {"classification": "ok", "termination_source": "candidate_exit", "signal": None, "limit_evidence": "exit_zero"}
    observed_signal = -returncode if returncode < 0 else returncode - 128 if 128 < returncode < 256 else None
    return {"classification": "candidate_error", "termination_source": "candidate_exit", "signal": observed_signal, "limit_evidence": "real_nonzero_exit"}


def _read_retained_outputs(writable: str, locators: Sequence[str], byte_limit: int) -> dict[str, bytes]:
    if not locators:
        return {}
    retained = {}
    root_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(writable, root_flags)
    try:
        for locator in locators:
            parts = _safe_locator(locator).split("/")
            directory_fd = os.dup(root_fd)
            try:
                for component in parts[:-1]:
                    next_fd = os.open(
                        component,
                        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
                        dir_fd=directory_fd,
                    )
                    os.close(directory_fd)
                    directory_fd = next_fd
                try:
                    fd = os.open(parts[-1], os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd)
                except FileNotFoundError:
                    continue
                with os.fdopen(fd, "rb") as handle:
                    opened = os.fstat(handle.fileno())
                    if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1 or opened.st_size > byte_limit:
                        raise SandboxError("retained output is unsafe or oversized: %s" % locator)
                    data = handle.read(byte_limit + 1)
                    if len(data) > byte_limit:
                        raise SandboxError("retained output exceeds byte limit: %s" % locator)
                    retained[locator] = data
            except OSError as exc:
                raise SandboxError("retained output path is unsafe: %s" % locator) from exc
            finally:
                os.close(directory_fd)
    finally:
        os.close(root_fd)
    return retained


def _validate_boundary(boundary: Mapping[str, object]) -> None:
    status = boundary.get("status")
    if not isinstance(status, Mapping):
        raise SandboxError("boundary status evidence missing")
    required = {
        "Uid": [1000, 1000, 1000, 1000],
        "Gid": [1000, 1000, 1000, 1000],
        "Groups": [],
        "CapPrm": "0000000000000000",
        "CapEff": "0000000000000000",
        "CapAmb": "0000000000000000",
        "CapBnd": "0000000000000000",
        "NoNewPrivs": 1,
    }
    mismatches = {name: {"expected": expected, "actual": status.get(name)} for name, expected in required.items() if status.get(name) != expected}
    descriptors = boundary.get("descriptor_inventory")
    if not isinstance(descriptors, list) or [item.get("fd") for item in descriptors if isinstance(item, Mapping)] != [0, 1, 2]:
        mismatches["descriptor_inventory"] = {"expected": [0, 1, 2], "actual": descriptors}
    links = boundary.get("network_links")
    if boundary.get("network_links_rc") != 0 or not isinstance(links, list) or len(links) != 1 or "lo" not in links[0] or "DOWN" not in links[0]:
        mismatches["network_links"] = {"expected": "loopback_down_only", "actual": links}
    if mismatches:
        raise SandboxError("boundary evidence mismatch: %s" % json.dumps(mismatches, sort_keys=True))


def run(config: SandboxConfig) -> SandboxResult:
    measured = fingerprint()
    target, scratch = _validate_config(config, measured)
    run_root = tempfile.mkdtemp(prefix="wp99-sandbox-", dir=scratch)
    os.chmod(run_root, 0o700)
    writable = os.path.join(run_root, "writable")
    rootfs = os.path.join(run_root, "rootfs")
    cgroup = None
    process = None
    started = time.monotonic()
    boundary_r = boundary_w = None
    resource_report: dict[str, object] = {}
    cleanup: dict[str, object] = {
        "cgroup_empty": "not_applicable",
        "descendants_gone": "not_applicable",
        "cgroup_removed": "not_applicable",
    }
    stdout = stderr = boundary_raw = b""
    boundary: dict[str, object] = {}
    forced = None
    truncated = False
    returncode = 125
    retained = {}
    try:
        cgroup = _Cgroup(config)
        spec = {
            "target": target,
            "rootfs": rootfs,
            "writable": writable,
            "command": list(config.command),
            "cpu_seconds": config.cpu_seconds,
            "output_bytes": config.output_bytes,
            "resolv_conf_text": config.resolv_conf_text,
            "scratch_input_files": dict(config.scratch_input_files),
        }
        encoded = base64.urlsafe_b64encode(json.dumps(spec, sort_keys=True, separators=(",", ":")).encode("utf-8")).decode("ascii")
        boundary_r, boundary_w = os.pipe()
        argv = [
            sys.executable,
            str(pathlib.Path(__file__).resolve()),
            "--spawn-helper",
            encoded,
            "--boundary-fd",
            str(boundary_w),
            "--cgroup-path",
            cgroup.path,
        ]
        process = subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=run_root,
            env=SAFE_ENV,
            close_fds=True,
            pass_fds=(boundary_w,),
        )
        cgroup.observe(process.pid)
        os.close(boundary_w)
        boundary_w = None
        stdout, stderr, boundary_raw, forced, truncated = _bounded_communicate(
            process, cgroup, boundary_r, config.timeout_seconds, config.output_bytes
        )
        boundary_r = None
        returncode = process.returncode
        resource_report = cgroup.report()
        retained = _read_retained_outputs(writable, config.retained_output_paths, config.output_bytes)
        try:
            decoded_boundary = json.loads(boundary_raw.decode("utf-8"))
        except (UnicodeError, ValueError) as exc:
            if forced is None:
                forced = "boundary_protocol_error"
            boundary = {
                "error": {
                    "name": "BoundaryProtocolError",
                    "message": str(exc),
                },
                "raw_bytes": len(boundary_raw),
            }
        else:
            if not isinstance(decoded_boundary, dict):
                if forced is None:
                    forced = "boundary_protocol_error"
                boundary = {
                    "error": {
                        "name": "BoundaryProtocolError",
                        "message": "trusted boundary report is not an object",
                    },
                    "raw_bytes": len(boundary_raw),
                }
            else:
                boundary = decoded_boundary
                try:
                    _validate_boundary(boundary)
                except SandboxError as exc:
                    if forced is None:
                        forced = "boundary_validation_error"
                    boundary = dict(boundary)
                    boundary["validation_error"] = str(exc)
    finally:
        if boundary_r is not None:
            os.close(boundary_r)
        if boundary_w is not None:
            os.close(boundary_w)
        if cgroup is not None:
            cleanup.update(cgroup.cleanup())
        scratch_deadline = time.monotonic() + 2.0
        scratch_attempts = 0
        while True:
            scratch_attempts += 1
            try:
                shutil.rmtree(run_root)
                cleanup["scratch_removed"] = True
                cleanup["scratch_error"] = None
                break
            except FileNotFoundError:
                cleanup["scratch_removed"] = True
                cleanup["scratch_error"] = None
                break
            except OSError as exc:
                cleanup["scratch_removed"] = False
                cleanup["scratch_error"] = "%s: %s" % (type(exc).__name__, exc)
                if time.monotonic() >= scratch_deadline:
                    break
                time.sleep(0.02)
        cleanup["scratch_removal_attempts"] = scratch_attempts
    termination = classify_termination(returncode, forced, resource_report)
    classification = str(termination["classification"])
    ok = (
        classification == "ok"
        and cleanup.get("cgroup_empty") is True
        and cleanup.get("descendants_gone") is True
        and cleanup.get("cgroup_removed") is True
        and cleanup.get("scratch_removed") is True
    )
    return SandboxResult(
        ok=ok,
        classification=classification,
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        elapsed_seconds=round(time.monotonic() - started, 6),
        output_truncated=truncated,
        fingerprint=measured,
        boundary=boundary,
        termination=termination,
        resource_report=resource_report,
        cleanup=cleanup,
        retained_outputs=retained,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spawn-helper")
    parser.add_argument("--child-init")
    parser.add_argument("--boundary-fd", type=int)
    parser.add_argument("--cgroup-path")
    args = parser.parse_args(argv)
    try:
        if args.spawn_helper:
            if args.boundary_fd is None or not args.cgroup_path:
                return 64
            return _spawn_helper(args.spawn_helper, args.boundary_fd, args.cgroup_path)
        if args.child_init:
            if args.boundary_fd is None:
                return 64
            return _child_init(args.child_init, args.boundary_fd)
    except BaseException as exc:
        print("sandbox trusted setup failed: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 125
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
