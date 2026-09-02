#!/usr/bin/env python3
"""Identity-bound executable capabilities for credential-bearing providers."""
from __future__ import annotations

import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
import hashlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PureWindowsPath
from typing import Callable, Mapping, Sequence


class Provider(str, Enum):
    CLAUDE = "claude"
    CODEX = "codex"
    GITHUB = "gh"


class ProviderExecutableError(OSError):
    """The requested executable could not become a closed capability."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


FileIdentity = tuple[int | str, ...]


@dataclass(frozen=True)
class BoundProviderExecutable:
    provider: str
    kind: str
    executable: Path
    launch_support: tuple[Path, ...]
    identities: tuple[tuple[Path, FileIdentity], ...]
    sanitized_path: str
    launch_arguments: tuple[str, ...] = ()

    def argv(self, arguments: Sequence[str]) -> list[str]:
        return provider_argv(self, arguments)

    def revalidate(self) -> None:
        revalidate_bound_provider(self)


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def provider_file_identity(path: Path) -> FileIdentity:
    """Bind a plain file plus metadata that changes on replacement/content edit."""
    if os.name == "nt":
        handle = _open_windows_provider_handle(path)
        try:
            return _windows_provider_identity(handle)
        finally:
            _close_windows_provider_handle(handle)
    info = path.lstat()
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if (not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)
            or (reparse and getattr(info, "st_file_attributes", 0) & reparse)):
        raise ProviderExecutableError("provider_executable_untrusted")
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        getattr(info, "st_mtime_ns", int(info.st_mtime * 1_000_000_000)),
        getattr(info, "st_ctime_ns", int(info.st_ctime * 1_000_000_000)),
    )


def _windows_api():
    """Return the small Win32 file-capability API used by provider launch."""
    import ctypes
    from ctypes import wintypes

    class FileTime(ctypes.Structure):
        _fields_ = (("low", wintypes.DWORD), ("high", wintypes.DWORD))

    class ByHandleFileInformation(ctypes.Structure):
        _fields_ = (
            ("attributes", wintypes.DWORD),
            ("creation_time", FileTime),
            ("last_access_time", FileTime),
            ("last_write_time", FileTime),
            ("volume_serial", wintypes.DWORD),
            ("size_high", wintypes.DWORD),
            ("size_low", wintypes.DWORD),
            ("links", wintypes.DWORD),
            ("file_index_high", wintypes.DWORD),
            ("file_index_low", wintypes.DWORD),
        )

    kernel32 = ctypes.windll.kernel32
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE)
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.GetFileInformationByHandle.argtypes = (
        wintypes.HANDLE, ctypes.POINTER(ByHandleFileInformation))
    kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
    kernel32.ReadFile.argtypes = (
        wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID)
    kernel32.ReadFile.restype = wintypes.BOOL
    kernel32.SetFilePointerEx.argtypes = (
        wintypes.HANDLE, ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_longlong), wintypes.DWORD)
    kernel32.SetFilePointerEx.restype = wintypes.BOOL
    kernel32.SetHandleInformation.argtypes = (
        wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD)
    kernel32.SetHandleInformation.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return ctypes, wintypes, kernel32, ByHandleFileInformation


def _open_windows_provider_handle(path: Path) -> int:
    """Open one non-inheritable read capability denying write/delete sharing."""
    ctypes, wintypes, kernel32, _information = _windows_api()
    handle = kernel32.CreateFileW(
        str(Path(path)),
        0x80000000,             # GENERIC_READ
        0x00000001,             # FILE_SHARE_READ; deny WRITE and DELETE
        None,
        3,                      # OPEN_EXISTING
        0x00200000,             # FILE_FLAG_OPEN_REPARSE_POINT
        None,
    )
    invalid = ctypes.c_void_p(-1).value
    if handle in (None, invalid):
        raise ctypes.WinError()
    if not kernel32.SetHandleInformation(
            wintypes.HANDLE(handle), 0x00000001, 0):  # HANDLE_FLAG_INHERIT
        error = ctypes.WinError()
        kernel32.CloseHandle(wintypes.HANDLE(handle))
        raise error
    return int(handle)


def _close_windows_provider_handle(handle: int) -> None:
    _ctypes, wintypes, kernel32, _information = _windows_api()
    kernel32.CloseHandle(wintypes.HANDLE(handle))


def _windows_provider_identity(handle: int) -> FileIdentity:
    """Hash and identify the exact object addressed by an already-held handle."""
    ctypes, wintypes, kernel32, Information = _windows_api()
    information = Information()
    if not kernel32.GetFileInformationByHandle(
            wintypes.HANDLE(handle), ctypes.byref(information)):
        raise ctypes.WinError()
    if information.attributes & (0x00000010 | 0x00000400):
        raise ProviderExecutableError("provider_executable_untrusted")
    if not kernel32.SetFilePointerEx(
            wintypes.HANDLE(handle), 0, None, 0):  # FILE_BEGIN
        raise ctypes.WinError()
    digest = hashlib.sha256()
    buffer = ctypes.create_string_buffer(1024 * 1024)
    while True:
        count = wintypes.DWORD()
        if not kernel32.ReadFile(
                wintypes.HANDLE(handle), buffer, len(buffer),
                ctypes.byref(count), None):
            raise ctypes.WinError()
        if count.value == 0:
            break
        digest.update(buffer.raw[:count.value])
    file_index = (
        int(information.file_index_high) << 32) | int(information.file_index_low)
    size = (int(information.size_high) << 32) | int(information.size_low)
    last_write = (
        int(information.last_write_time.high) << 32
    ) | int(information.last_write_time.low)
    creation = (
        int(information.creation_time.high) << 32
    ) | int(information.creation_time.low)
    return (
        int(information.volume_serial), file_index, size,
        last_write, creation, digest.hexdigest(),
    )


def _read_windows_provider_file(
        path: Path, expected: FileIdentity, *, maximum: int) -> bytes:
    """Read one bound Windows object while denying concurrent replacement."""
    handle = _open_windows_provider_handle(path)
    try:
        identity = _windows_provider_identity(handle)
        if identity != expected or int(identity[2]) > maximum:
            raise ProviderExecutableError("provider_launch_support_untrusted")
        # Identity hashing left the fresh handle at EOF; read once more for the
        # small npm shim whose bytes define the launch-support plan.
        ctypes, wintypes, kernel32, _information = _windows_api()
        if not kernel32.SetFilePointerEx(wintypes.HANDLE(handle), 0, None, 0):
            raise ctypes.WinError()
        output = bytearray()
        buffer = ctypes.create_string_buffer(min(maximum + 1, 65537))
        while len(output) <= maximum:
            count = wintypes.DWORD()
            if not kernel32.ReadFile(
                    wintypes.HANDLE(handle), buffer, len(buffer),
                    ctypes.byref(count), None):
                raise ctypes.WinError()
            if count.value == 0:
                return bytes(output)
            output.extend(buffer.raw[:count.value])
        raise ProviderExecutableError("provider_launch_support_untrusted")
    finally:
        _close_windows_provider_handle(handle)


def private_provider_directory_acl_available() -> bool:
    """Whether mode=0700 creates private provider directories on this runtime."""
    return (
        os.name == "posix"
        or (os.name == "nt" and sys.version_info >= (3, 13))
    )


def trusted_provider_temp_base() -> Path:
    """Find the process temp tree without trusting caller-controlled temp vars."""
    if os.name == "posix":
        candidate = Path("/tmp")
    elif os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.windll.kernel32
            advapi32 = ctypes.windll.advapi32
            userenv = ctypes.windll.userenv
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            advapi32.OpenProcessToken.argtypes = (
                wintypes.HANDLE, wintypes.DWORD,
                ctypes.POINTER(wintypes.HANDLE))
            advapi32.OpenProcessToken.restype = wintypes.BOOL
            userenv.GetUserProfileDirectoryW.argtypes = (
                wintypes.HANDLE, wintypes.LPWSTR,
                ctypes.POINTER(wintypes.DWORD))
            userenv.GetUserProfileDirectoryW.restype = wintypes.BOOL
            kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
            kernel32.CloseHandle.restype = wintypes.BOOL
            token = wintypes.HANDLE()
            if not advapi32.OpenProcessToken(
                    kernel32.GetCurrentProcess(), 0x0008,
                    ctypes.byref(token)):
                raise ctypes.WinError()
            try:
                size = wintypes.DWORD(0)
                userenv.GetUserProfileDirectoryW(
                    token, None, ctypes.byref(size))
                if not size.value:
                    raise ctypes.WinError()
                buffer = ctypes.create_unicode_buffer(size.value)
                if not userenv.GetUserProfileDirectoryW(
                        token, buffer, ctypes.byref(size)):
                    raise ctypes.WinError()
            finally:
                kernel32.CloseHandle(token)
        except (AttributeError, OSError, ValueError) as exc:
            raise OSError("Windows user profile lookup unavailable") from exc
        candidate = Path(buffer.value) / "AppData" / "Local" / "Temp"
    else:
        raise OSError("private provider storage unsupported on this platform")
    base = candidate.resolve(strict=True)
    info = base.lstat()
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if (not base.is_dir() or stat.S_ISLNK(info.st_mode)
            or (reparse and getattr(info, "st_file_attributes", 0) & reparse)):
        raise OSError("trusted provider temp base is not a plain directory")
    return base


def _forbidden_roots(repository_root: Path) -> tuple[Path, ...]:
    try:
        repository = Path(repository_root).resolve(strict=True)
        temporary = trusted_provider_temp_base().resolve(strict=True)
        process_temporary = Path(tempfile.gettempdir()).resolve(strict=True)
    except OSError as exc:
        raise ProviderExecutableError("provider_executable_untrusted") from exc
    roots = [repository, temporary]
    if os.path.normcase(str(process_temporary)) not in {
            os.path.normcase(str(root)) for root in roots}:
        roots.append(process_temporary)
    return tuple(roots)


def _trusted(path: Path, forbidden: tuple[Path, ...]) -> bool:
    return not any(_within(path, root) for root in forbidden)


def _candidate(alias: Path, forbidden: tuple[Path, ...], *, executable: bool = True):
    try:
        alias_info = alias.lstat()
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if (os.name == "nt"
                and (stat.S_ISLNK(alias_info.st_mode)
                     or (reparse and getattr(
                         alias_info, "st_file_attributes", 0) & reparse))):
            return None
        target = alias.resolve(strict=True)
        if not _trusted(alias, forbidden) or not _trusted(target, forbidden):
            return None
        identity = provider_file_identity(target)
        if executable and os.name == "posix" and not os.access(target, os.X_OK):
            return None
        return alias, target, identity
    except (OSError, ProviderExecutableError):
        return None


def _absolute_path_directories(source: Mapping[str, str],
                               forbidden: tuple[Path, ...]) -> list[Path]:
    raw_path = source.get("PATH")
    if not isinstance(raw_path, str) or not raw_path:
        raise ProviderExecutableError("provider_executable_missing")
    directories: list[Path] = []
    seen: set[str] = set()
    for raw in raw_path.split(os.pathsep):
        if not raw:
            continue
        # PATH is data passed to an executable resolver, not shell syntax.
        # Test the raw spelling before any expansion or ambient-HOME lookup.
        lexical = Path(raw)
        if not lexical.is_absolute():
            raise ProviderExecutableError("provider_executable_untrusted")
        try:
            directory = lexical.resolve(strict=True)
        except OSError:
            continue
        if not directory.is_dir() or not _trusted(directory, forbidden):
            raise ProviderExecutableError("provider_executable_untrusted")
        key = os.path.normcase(str(directory))
        if key not in seen:
            seen.add(key)
            directories.append(directory)
    if not directories:
        raise ProviderExecutableError("provider_executable_untrusted")
    return directories


def _named_support(name: str, directories: list[Path],
                   forbidden: tuple[Path, ...]):
    if (not name or Path(name).name != name
            or not re.fullmatch(r"[A-Za-z0-9_.+\-]+", name)):
        raise ProviderExecutableError("provider_launch_support_untrusted")
    candidate_name = (
        name + ".exe" if os.name == "nt" and not name.lower().endswith(".exe")
        else name)
    candidates = [candidate for directory in directories
                  if (candidate := _candidate(
                      directory / candidate_name, forbidden, executable=True))
                  is not None]
    if len(candidates) != 1:
        raise ProviderExecutableError(
            "provider_launch_support_missing" if not candidates
            else "provider_launch_support_ambiguous")
    return candidates[0]


def _posix_plan(executable: Path, directories: list[Path],
                forbidden: tuple[Path, ...]):
    try:
        with executable.open("rb") as source:
            first = source.readline(4097)
    except OSError as exc:
        raise ProviderExecutableError("provider_launch_support_untrusted") from exc
    if not first.startswith(b"#!"):
        return "direct", (), (), []
    if len(first) > 4096 or not first.endswith((b"\n", b"\r")):
        raise ProviderExecutableError("provider_launch_support_untrusted")
    try:
        words = shlex.split(first[2:].decode("utf-8", "strict").strip())
    except (UnicodeDecodeError, ValueError) as exc:
        raise ProviderExecutableError("provider_launch_support_untrusted") from exc
    if not words or len(words) > 2 or not Path(words[0]).is_absolute():
        raise ProviderExecutableError("provider_launch_support_untrusted")
    interpreter = _candidate(Path(words[0]), forbidden, executable=True)
    if interpreter is None:
        raise ProviderExecutableError("provider_launch_support_untrusted")
    _, interpreter_target, interpreter_identity = interpreter
    identities = [(interpreter_target, interpreter_identity)]
    if interpreter_target.name == "env":
        if len(words) != 2:
            raise ProviderExecutableError("provider_launch_support_untrusted")
        _, support, support_identity = _named_support(
            words[1], directories, forbidden)
        identities.append((support, support_identity))
        return "posix-script", (support,), (), identities
    return ("posix-script", (interpreter_target,), tuple(words[1:]), identities)


def _windows_plan(executable: Path, executable_identity: FileIdentity,
                  directories: list[Path], forbidden: tuple[Path, ...]):
    suffix = executable.suffix.lower()
    if suffix in (".exe", ".com"):
        return "direct", (), (), []
    if suffix != ".cmd":
        raise ProviderExecutableError("provider_launch_support_untrusted")
    try:
        raw = _read_windows_provider_file(
            executable, executable_identity, maximum=65536)
        text = raw.decode("utf-8-sig", "strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise ProviderExecutableError("provider_launch_support_untrusted") from exc
    matches = re.findall(r'(?im)"%dp0%\\([^"\r\n]+?\.js)"\s+%\*\s*$', text)
    if len(matches) != 1:
        raise ProviderExecutableError("provider_launch_support_untrusted")
    relative = PureWindowsPath(matches[0])
    if (relative.is_absolute() or relative.drive or relative.root
            or any(part in ("", ".", "..") for part in relative.parts)):
        raise ProviderExecutableError("provider_launch_support_untrusted")
    script_candidate = _candidate(
        executable.parent.joinpath(*relative.parts), forbidden, executable=False)
    if script_candidate is None:
        raise ProviderExecutableError("provider_launch_support_untrusted")
    _, script, script_identity = script_candidate
    sibling = executable.parent / "node.exe"
    try:
        sibling.lstat()
    except FileNotFoundError:
        _, node, node_identity = _named_support("node", directories, forbidden)
    except OSError as exc:
        raise ProviderExecutableError("provider_launch_support_untrusted") from exc
    else:
        node_candidate = _candidate(sibling, forbidden, executable=True)
        if node_candidate is None:
            raise ProviderExecutableError("provider_launch_support_untrusted")
        _, node, node_identity = node_candidate
    return ("npm-cmd", (node, script), (),
            [(node, node_identity), (script, script_identity)])


def _build_bound(name: str, executable: Path, identity: FileIdentity,
                 directories: list[Path], forbidden: tuple[Path, ...]) \
        -> BoundProviderExecutable:
    identities = [(executable, identity)]
    if os.name == "posix":
        kind, support, launch_arguments, support_identities = _posix_plan(
            executable, directories, forbidden)
    else:
        kind, support, launch_arguments, support_identities = _windows_plan(
            executable, identity, directories, forbidden)
    identities.extend(support_identities)
    return BoundProviderExecutable(
        provider=name, kind=kind, executable=executable,
        launch_support=support, launch_arguments=launch_arguments,
        identities=tuple(identities),
        sanitized_path=os.pathsep.join(str(path) for path in directories))


def bind_provider_executable(name: str, source: Mapping[str, str], *,
                             repository_root: Path) -> BoundProviderExecutable:
    """Discover exactly one provider from a closed absolute PATH capability."""
    if name not in {provider.value for provider in Provider}:
        raise ProviderExecutableError("provider_executable_untrusted")
    forbidden = _forbidden_roots(repository_root)
    directories = _absolute_path_directories(source, forbidden)
    if os.name == "nt":
        raw_extensions = source.get("PATHEXT") or ".COM;.EXE;.BAT;.CMD"
        allowed = {".com", ".exe", ".bat", ".cmd"}
        extensions: list[str] = []
        for extension in raw_extensions.split(";"):
            extension = extension.strip().lower()
            if extension in allowed and extension not in extensions:
                extensions.append(extension)
        names = [name + extension for extension in extensions]
    else:
        names = [name]
    candidates = [candidate for directory in directories for candidate_name in names
                  if (candidate := _candidate(
                      directory / candidate_name, forbidden, executable=True))
                  is not None]
    if not candidates:
        raise ProviderExecutableError("provider_executable_missing")
    if len(candidates) != 1:
        raise ProviderExecutableError("provider_executable_ambiguous")
    _alias, executable, identity = candidates[0]
    return _build_bound(name, executable, identity, directories, forbidden)


def bind_provider_path(name: str, path: Path, source: Mapping[str, str], *,
                       repository_root: Path) -> BoundProviderExecutable:
    """Bind an already policy-identified provider alias/hardlink by identity."""
    if name not in {provider.value for provider in Provider}:
        raise ProviderExecutableError("provider_executable_untrusted")
    forbidden = _forbidden_roots(repository_root)
    candidate = _candidate(Path(path), forbidden, executable=True)
    if candidate is None:
        raise ProviderExecutableError("provider_executable_untrusted")
    _alias, executable, identity = candidate
    directories = _absolute_path_directories(source, forbidden)
    if all(os.path.normcase(str(directory)) != os.path.normcase(str(executable.parent))
           for directory in directories):
        directories.insert(0, executable.parent)
    return _build_bound(name, executable, identity, directories, forbidden)


def revalidate_bound_provider(bound: BoundProviderExecutable) -> None:
    for path, identity in bound.identities:
        try:
            current = provider_file_identity(path)
        except (OSError, ProviderExecutableError) as exc:
            raise ProviderExecutableError("provider_executable_changed") from exc
        if current != identity:
            raise ProviderExecutableError("provider_executable_changed")


def provider_argv(bound: BoundProviderExecutable,
                  arguments: Sequence[str]) -> list[str]:
    """Revalidate immediately before constructing an absolute-only launch."""
    revalidate_bound_provider(bound)
    tail = [str(argument) for argument in arguments]
    if bound.kind == "direct":
        return [str(bound.executable), *tail]
    if bound.kind == "posix-script" and len(bound.launch_support) == 1:
        return [str(bound.launch_support[0]), *bound.launch_arguments,
                str(bound.executable), *tail]
    if bound.kind == "npm-cmd" and len(bound.launch_support) == 2:
        return [str(bound.launch_support[0]), str(bound.launch_support[1]), *tail]
    raise ProviderExecutableError("provider_executable_untrusted")


def bound_provider_source(source: Mapping[str, str],
                          bound: BoundProviderExecutable) -> dict[str, str]:
    child_source = dict(source)
    child_source["PATH"] = bound.sanitized_path
    return child_source


def _acquire_windows_provider_handles(
        bound: BoundProviderExecutable) -> list[int]:
    """Open and validate all launch identities as one process-creation guard."""
    handles: list[int] = []
    try:
        for path, expected in bound.identities:
            handle = _open_windows_provider_handle(path)
            try:
                actual = _windows_provider_identity(handle)
                if actual != expected:
                    raise ProviderExecutableError("provider_executable_changed")
            except BaseException:
                _close_windows_provider_handle(handle)
                raise
            handles.append(handle)
        return handles
    except BaseException as exc:
        for handle in reversed(handles):
            _close_windows_provider_handle(handle)
        if isinstance(exc, ProviderExecutableError):
            raise
        raise ProviderExecutableError("provider_executable_changed") from exc


def _release_windows_provider_handles(handles: Sequence[int]) -> None:
    for handle in reversed(handles):
        _close_windows_provider_handle(handle)


def popen_bound_provider(
        bound: BoundProviderExecutable, arguments: Sequence[str], *,
        _popen_factory: Callable | None = None, **kwargs):
    """Create a provider process while Windows identities remain write-locked.

    Windows handles cover the executable, shim/interpreter, and every launch
    support file.  They are non-inheritable and close immediately after Popen
    returns from CreateProcessW, never for the lifetime of the child.  POSIX
    retains the pre-existing metadata revalidation and Popen behavior.
    """
    factory = subprocess.Popen if _popen_factory is None else _popen_factory
    if os.name != "nt":
        return factory(provider_argv(bound, arguments), **kwargs)
    handles = _acquire_windows_provider_handles(bound)
    try:
        argv = provider_argv(bound, arguments)
        return factory(argv, **kwargs)
    finally:
        _release_windows_provider_handles(handles)


def run_bound_provider(
        bound: BoundProviderExecutable, arguments: Sequence[str], *,
        input=None, capture_output: bool = False, timeout=None,
        check: bool = False, _popen_factory: Callable | None = None, **kwargs):
    """``subprocess.run`` semantics with a Windows hold-through-Popen boundary."""
    if os.name != "nt" and _popen_factory is None:
        return subprocess.run(
            provider_argv(bound, arguments), input=input,
            capture_output=capture_output, timeout=timeout, check=check, **kwargs)
    if input is not None:
        if kwargs.get("stdin") is not None:
            raise ValueError("stdin and input arguments may not both be used")
        kwargs["stdin"] = subprocess.PIPE
    if capture_output:
        if kwargs.get("stdout") is not None or kwargs.get("stderr") is not None:
            raise ValueError(
                "stdout and stderr arguments may not be used with capture_output")
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    process = popen_bound_provider(
        bound, arguments, _popen_factory=_popen_factory, **kwargs)
    with process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            process.kill()
            if sys.platform == "win32":
                exc.stdout, exc.stderr = process.communicate()
            else:
                process.wait()
            raise
        except BaseException:
            process.kill()
            process.wait()
            raise
        returncode = process.poll()
        if check and returncode:
            raise subprocess.CalledProcessError(
                returncode, process.args, output=stdout, stderr=stderr)
    return subprocess.CompletedProcess(process.args, returncode, stdout, stderr)
