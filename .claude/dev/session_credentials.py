#!/usr/bin/env python3
"""Secret-safe credential bootstrap for an ephemeral agent session."""
from __future__ import annotations

import argparse
import base64
import contextlib
import errno
import json
import os
import re
import secrets
import select
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from provider_exec import (
    BoundProviderExecutable as _BoundProviderExecutable,
    ProviderExecutableError as _ProviderExecutableError,
    bind_provider_executable,
    bound_provider_source as _shared_bound_provider_source,
    provider_argv as _shared_provider_argv,
    provider_file_identity as _provider_file_identity,
    revalidate_bound_provider as _revalidate_bound_provider,
    trusted_provider_temp_base as _shared_trusted_provider_temp_base,
)

STATUSES = ("missing", "rejected", "network_error", "not_measured", "passed")
SECRET_ENV = ("CODEX_AUTH_JSON", "CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_PAT", "TL_MASTER_KEY")
TOKEN_RE = re.compile(r"sk-ant-oat\d+-[A-Za-z0-9_-]{20,}")
TOKEN_PREFIX = "sk-ant-oat"
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


class UnsafeSecretDestination(OSError):
    """A secret target resolves into this repository."""


# Child processes get an intentionally small operational environment rather
# than a copy of the agent's environment.  In particular, this prevents a
# credential intended for one provider from becoming ambient authority in a
# different provider's CLI.
CHILD_ENV_KEYS = frozenset({
    "PATH", "USER", "LOGNAME", "SHELL", "TERM",
    "TMPDIR", "TMP", "TEMP",
    "LANG", "LANGUAGE", "LC_ALL", "TZ",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
    "http_proxy", "https_proxy", "all_proxy", "no_proxy",
    "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE",
    "PYTHONUTF8", "PYTHONIOENCODING",
    "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT",
})


def _child_env(source, **required: str) -> dict[str, str]:
    """Return benign process settings plus only this child's credential."""
    child = {key: value for key, value in source.items()
             if key in CHILD_ENV_KEYS or key.startswith("LC_")}
    # Keep this invariant explicit even if a secret is accidentally added to
    # CHILD_ENV_KEYS in a future change.
    for key in SECRET_ENV:
        child.pop(key, None)
    child.update(required)
    return child


def _bind_provider_executable(name: str, source) -> _BoundProviderExecutable:
    return bind_provider_executable(
        name, source, repository_root=REPOSITORY_ROOT)


def _provider_argv(bound: _BoundProviderExecutable,
                   arguments: list[str]) -> list[str]:
    return _shared_provider_argv(bound, arguments)


def _bound_provider_source(source, bound: _BoundProviderExecutable) -> dict:
    return _shared_bound_provider_source(source, bound)


def _trusted_provider_temp_base() -> Path:
    return _shared_trusted_provider_temp_base()


def _validate_private_provider_directory(path: Path) -> Path:
    """Validate one process-created private directory, including reparse state."""
    resolved = directory_destination(path).resolve(strict=True)
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode):
        raise OSError("provider directory is a symlink")
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if reparse and getattr(info, "st_file_attributes", 0) & reparse:
        raise OSError("provider directory is a reparse point")
    if os.name == "posix" and stat.S_IMODE(info.st_mode) != 0o700:
        raise OSError("provider directory mode is not 0700")
    return resolved


def _make_private_provider_directory(path: Path) -> Path:
    path.mkdir(mode=0o700)
    return _validate_private_provider_directory(path)


def _private_provider_identity(path: Path) -> tuple[int, int]:
    """Return the identity of one plain allocated root without following it."""
    info = Path(path).lstat()
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if (not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode)
            or (reparse and getattr(info, "st_file_attributes", 0) & reparse)):
        raise OSError("provider cleanup root is linked, reparsed, or not a directory")
    return (info.st_dev, info.st_ino)


def _checked_provider_cleanup(root: Path, identity: tuple[int, int]) -> None:
    """Remove only the exact allocated root and verify that no residual remains."""
    root = Path(root)
    try:
        current = _private_provider_identity(root)
    except FileNotFoundError:
        return
    if current != identity:
        raise OSError("provider cleanup root identity changed")

    # Atomically take the exact verified entry out of its public temp name.
    # Re-check after rename: if the source was swapped between lstat and rename,
    # do not hand the substituted link/reparse point to recursive deletion.
    for _ in range(128):
        tombstone = root.with_name(
            f".{root.name}.cleanup-{secrets.token_hex(12)}")
        try:
            tombstone.lstat()
        except FileNotFoundError:
            break
    else:
        raise OSError("could not allocate provider cleanup tombstone")
    os.replace(root, tombstone)
    if _private_provider_identity(tombstone) != identity:
        raise OSError("provider cleanup root changed during quarantine")

    shutil.rmtree(tombstone)
    try:
        tombstone.lstat()
    except FileNotFoundError:
        pass
    else:
        raise OSError("provider cleanup left a residual root")
    try:
        root.lstat()
    except FileNotFoundError:
        return
    raise OSError("provider cleanup root name was recreated")


@contextlib.contextmanager
def _private_provider_home():
    """Yield a validated disposable provider HOME outside repository control."""
    base = _trusted_provider_temp_base()
    root = None
    root_identity = None
    try:
        root = Path(tempfile.mkdtemp(prefix="tl-provider-home-", dir=base))
        root = _validate_private_provider_directory(root)
        root_identity = _private_provider_identity(root)
        home = _make_private_provider_directory(root / "home")
        _make_private_provider_directory(root / "tmp")
        _make_private_provider_directory(home / ".config")
        local = _make_private_provider_directory(home / ".local")
        _make_private_provider_directory(local / "share")
        _make_private_provider_directory(local / "state")
        _make_private_provider_directory(home / ".cache")
        yield home
    finally:
        if root is not None and root_identity is not None:
            _checked_provider_cleanup(root, root_identity)


def _provider_child_env_for_home(source, home: Path, **required: str) -> dict[str, str]:
    """Bind every provider storage variable to one validated private hierarchy."""
    home = _validate_private_provider_directory(Path(home))
    root = _validate_private_provider_directory(home.parent)
    tmp = _validate_private_provider_directory(root / "tmp")
    config = _validate_private_provider_directory(home / ".config")
    cache = _validate_private_provider_directory(home / ".cache")
    data = _validate_private_provider_directory(home / ".local" / "share")
    state = _validate_private_provider_directory(home / ".local" / "state")
    return _child_env(
        source,
        HOME=str(home),
        XDG_CONFIG_HOME=str(config),
        XDG_CACHE_HOME=str(cache),
        XDG_DATA_HOME=str(data),
        XDG_STATE_HOME=str(state),
        TMPDIR=str(tmp), TMP=str(tmp), TEMP=str(tmp),
        **required,
    )


@contextlib.contextmanager
def _isolated_child_env(source, **required: str):
    """Give one provider a disposable hierarchy plus its explicit credential."""
    with _private_provider_home() as home:
        yield _provider_child_env_for_home(source, home, **required)


def _result(status: str, **details) -> dict:
    if status not in STATUSES:
        raise ValueError(f"invalid status: {status}")
    return {"status": status, **details}


def codex_home(env=None) -> Path:
    env = os.environ if env is None else env
    return Path(env.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def _is_repository_root(candidate: Path) -> bool:
    """Recognize both a worktree and a bare Git repository."""
    if (candidate / ".git").exists():
        return True
    return ((candidate / "HEAD").is_file()
            and (candidate / "objects").is_dir()
            and (candidate / "refs").is_dir()
            and (candidate / "config").is_file())


def _guard_destination(path: Path, *, include_candidate: bool) -> Path:
    """Canonicalize a file or directory target outside every repository.

    This path check is deliberately not the writer's authority.  The writer
    opens the actual parent directory and repeats the repository test by file
    descriptor before it creates a byte.  Callers still use this canonical
    value so a benign alias cannot drift between their own preflight and use.

    File targets begin at their parent.  Directory-valued environment roots
    must include the candidate itself: a directory can itself be a worktree or
    bare repository even when its parent is harmless.
    """
    target = path.expanduser()
    resolved = target.resolve(strict=False)
    start = resolved if include_candidate else resolved.parent
    for candidate in (start, *start.parents):
        if _is_repository_root(candidate):
            raise UnsafeSecretDestination(
                f"refusing repository secret destination: {target}")
    if target.is_symlink():
        raise OSError(f"refusing symlink destination: {target}")
    return resolved


def secret_destination(path: Path) -> Path:
    """Preflight and canonicalize a secret file target."""
    return _guard_destination(path, include_candidate=False)


def directory_destination(path: Path) -> Path:
    """Preflight and canonicalize a delegated directory-valued root."""
    return _guard_destination(path, include_candidate=True)


def _stat_at(directory_fd: int, name: str):
    try:
        return os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def _fd_is_repository_root(directory_fd: int) -> bool:
    dotgit = _stat_at(directory_fd, ".git")
    if dotgit is not None:
        return True
    head = _stat_at(directory_fd, "HEAD")
    objects = _stat_at(directory_fd, "objects")
    refs = _stat_at(directory_fd, "refs")
    config = _stat_at(directory_fd, "config")
    return bool(head and stat.S_ISREG(head.st_mode)
                and objects and stat.S_ISDIR(objects.st_mode)
                and refs and stat.S_ISDIR(refs.st_mode)
                and config and stat.S_ISREG(config.st_mode))


def _directory_flags() -> int:
    required = ("O_DIRECTORY", "O_NOFOLLOW")
    if os.name != "posix" or any(not hasattr(os, name) for name in required):
        # Windows has no stdlib handle-relative create/rename API.  A held
        # directory handle plus pathname operations is still a pathname
        # fallback, so this generation intentionally fails closed there.
        raise OSError("handle-relative secret writer unavailable on this platform")
    return (os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            | getattr(os, "O_CLOEXEC", 0))


def _validate_parent_capability(parent_fd: int) -> None:
    """Walk ``..`` from the opened capability and reject any repository."""
    flags = _directory_flags()
    current = os.dup(parent_fd)
    seen = set()
    primary = None
    primary_traceback = None
    try:
        try:
            while True:
                opened = os.fstat(current)
                identity = (opened.st_dev, opened.st_ino)
                if identity in seen:
                    raise OSError("secret parent ancestry loop")
                seen.add(identity)
                if _fd_is_repository_root(current):
                    raise UnsafeSecretDestination(
                        "refusing repository secret parent capability")
                # Do not consult os.supports_dir_fd.  CPython 3.14 omits working
                # combinations (notably os.replace) from that registry.
                parent = os.open("..", flags, dir_fd=current)
                try:
                    parent_identity = os.fstat(parent)
                except BaseException as exc:
                    parent_traceback = exc.__traceback__
                    try:
                        os.close(parent)
                    except BaseException:
                        pass
                    raise exc.with_traceback(parent_traceback)
                if identity == (parent_identity.st_dev, parent_identity.st_ino):
                    os.close(parent)
                    break
                previous = current
                current = parent
                try:
                    os.close(previous)
                except BaseException as exc:
                    close_traceback = exc.__traceback__
                    try:
                        os.close(current)
                    except BaseException:
                        pass
                    current = -1
                    raise exc.with_traceback(close_traceback)
        except (TypeError, NotImplementedError) as exc:
            raise OSError(
                "directory-relative secret primitives unavailable") from exc
    except BaseException as exc:
        primary = exc
        primary_traceback = exc.__traceback__
    close_error = None
    if current != -1:
        try:
            os.close(current)
        except BaseException as exc:
            close_error = exc
    if primary is not None:
        raise primary.with_traceback(primary_traceback)
    if close_error is not None:
        raise close_error


def _walk_parent_capability(parent: Path, *, create: bool) -> int:
    """Open/create an absolute parent by walking from the POSIX root fd."""
    flags = _directory_flags()
    if not parent.is_absolute():
        raise OSError("secret parent must be absolute")
    components = parent.parts[1:]
    if any(component in ("", ".", "..") for component in components):
        raise OSError("invalid secret parent component")
    try:
        current = os.open(os.path.sep, flags)
    except (TypeError, NotImplementedError) as exc:
        raise OSError("cannot open trusted secret root capability") from exc
    try:
        for component in components:
            try:
                child = os.open(component, flags, dir_fd=current)
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    os.mkdir(component, mode=0o700, dir_fd=current)
                except FileExistsError:
                    # A concurrent creator is accepted only if the following
                    # no-follow open proves it installed a real directory.
                    pass
                except (TypeError, NotImplementedError) as exc:
                    raise OSError(
                        "directory-relative secret mkdir unavailable") from exc
                try:
                    child = os.open(component, flags, dir_fd=current)
                except (TypeError, NotImplementedError) as exc:
                    raise OSError(
                        "directory-relative secret open unavailable") from exc
                except OSError as exc:
                    installed = _stat_at(current, component)
                    if installed is not None and stat.S_ISLNK(installed.st_mode):
                        raise UnsafeSecretDestination(
                            "refusing linked secret parent capability") from exc
                    raise
            except (TypeError, NotImplementedError) as exc:
                raise OSError(
                    "directory-relative secret open unavailable") from exc
            except OSError as exc:
                installed = _stat_at(current, component)
                if installed is not None and stat.S_ISLNK(installed.st_mode):
                    raise UnsafeSecretDestination(
                        "refusing linked secret parent capability") from exc
                raise
            try:
                opened = os.fstat(child)
                if not stat.S_ISDIR(opened.st_mode):
                    raise OSError("secret parent component is not a directory")
                if _fd_is_repository_root(child):
                    raise UnsafeSecretDestination(
                        "refusing repository secret parent capability")
            except BaseException as primary:
                primary_traceback = primary.__traceback__
                try:
                    os.close(child)
                except BaseException:
                    pass
                raise primary.with_traceback(primary_traceback)
            previous = current
            current = child
            try:
                os.close(previous)
            except BaseException as primary:
                # A failed close has ambiguous descriptor state and must not be
                # retried.  The child capability is still ours and must be
                # closed, while the first close failure remains authoritative.
                primary_traceback = primary.__traceback__
                try:
                    os.close(current)
                except BaseException:
                    pass
                current = -1
                raise primary.with_traceback(primary_traceback)
        _validate_parent_capability(current)
    except BaseException as primary:
        primary_traceback = primary.__traceback__
        if current != -1:
            try:
                os.close(current)
            except BaseException:
                pass
        raise primary.with_traceback(primary_traceback)
    return current


def _open_parent_capability(path: Path, *, create: bool) -> int:
    return _walk_parent_capability(path.parent, create=create)


def _checked_secret_destination(path: Path, *, create_parent: bool = True) -> Path:
    """Return a canonical path only after validating its actual parent handle."""
    target = secret_destination(path)
    parent_fd = _open_parent_capability(target, create=create_parent)
    os.close(parent_fd)
    return target


def _read_secret_bytes(path: Path) -> bytes:
    """Read a regular file relative to the validated parent capability."""
    target = secret_destination(path)
    parent_fd = _open_parent_capability(target, create=False)
    fd = -1
    try:
        try:
            fd = os.open(target.name, os.O_RDONLY | os.O_NOFOLLOW,
                         dir_fd=parent_fd)
        except (TypeError, NotImplementedError) as exc:
            raise OSError("relative secret read unavailable") from exc
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            raise OSError("secret source is not a regular file")
        with os.fdopen(fd, "rb") as source:
            fd = -1
            return source.read()
    finally:
        if fd != -1:
            os.close(fd)
        os.close(parent_fd)


def _created_secret_identity(fd: int) -> tuple[int, int]:
    """Bind a just-created inode before any operation that can fail."""
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            raise OSError("created secret target is not a regular file")
        return opened.st_dev, opened.st_ino
    except BaseException as primary:
        primary_traceback = primary.__traceback__
        try:
            os.close(fd)
        except BaseException:
            pass
        raise primary.with_traceback(primary_traceback)


def _write_secret_fd(fd: int, data: bytes,
                     identity: tuple[int, int]) -> None:
    out = None
    primary = None
    primary_traceback = None
    try:
        os.fchmod(fd, 0o600)
        mode = os.fstat(fd)
        if (mode.st_dev, mode.st_ino) != identity:
            raise OSError("created secret identity changed before write")
        if stat.S_IMODE(mode.st_mode) != 0o600:
            raise OSError("secret mode 0600 was not established")
        out = os.fdopen(fd, "wb")
        fd = -1
        out.write(data)
        out.flush()
        os.fsync(out.fileno())
    except BaseException as exc:
        primary = exc
        primary_traceback = exc.__traceback__
    close_error = None
    try:
        if out is not None:
            out.close()
        elif fd != -1:
            os.close(fd)
    except BaseException as exc:
        close_error = exc
    if primary is not None:
        raise primary.with_traceback(primary_traceback)
    if close_error is not None:
        raise close_error


def _unlink_identity(directory_fd: int, name: str,
                     identity: tuple[int, int] | None) -> None:
    if identity is None:
        return
    existing = _stat_at(directory_fd, name)
    if existing is None or (existing.st_dev, existing.st_ino) != identity:
        return
    os.unlink(name, dir_fd=directory_fd)


def _atomic_secret_dirfd(path: Path, data: bytes, *, exclusive: bool) -> Path:
    parent_fd = _open_parent_capability(path, create=True)
    created_name = None
    created_identity = None
    primary = None
    primary_traceback = None
    result = None
    try:
        if exclusive:
            created_name = path.name
            try:
                fd = os.open(created_name,
                             os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=parent_fd)
            except (TypeError, NotImplementedError) as exc:
                raise OSError("relative secret create unavailable") from exc
            created_identity = _created_secret_identity(fd)
            _write_secret_fd(fd, data, created_identity)
            installed = _stat_at(parent_fd, created_name)
            if (installed is None
                    or (installed.st_dev, installed.st_ino) != created_identity
                    or stat.S_IMODE(installed.st_mode) != 0o600):
                raise OSError("exclusive secret target changed during write")
        else:
            for _ in range(128):
                candidate = f".{path.name}.tmp-{secrets.token_hex(12)}"
                try:
                    fd = os.open(candidate,
                                 os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o600, dir_fd=parent_fd)
                except FileExistsError:
                    continue
                except (TypeError, NotImplementedError) as exc:
                    raise OSError("relative secret create unavailable") from exc
                created_name = candidate
                created_identity = _created_secret_identity(fd)
                break
            else:
                raise OSError("could not allocate secret temporary file")
            _write_secret_fd(fd, data, created_identity)
            try:
                existing = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                existing = None
            if existing is not None and stat.S_ISLNK(existing.st_mode):
                raise OSError(f"refusing symlink destination: {path}")
            try:
                os.replace(created_name, path.name,
                           src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
            except (TypeError, NotImplementedError) as exc:
                raise OSError("relative secret replace unavailable") from exc
            installed = _stat_at(parent_fd, path.name)
            if (installed is None
                    or (installed.st_dev, installed.st_ino) != created_identity
                    or stat.S_IMODE(installed.st_mode) != 0o600):
                raise OSError("secret target changed during replace")
        os.fsync(parent_fd)
        created_name = None
        result = path
    except BaseException as exc:
        primary = exc
        primary_traceback = exc.__traceback__
        cleanup_names = []
        if created_name is not None:
            cleanup_names.append(created_name)
        if (not exclusive and created_identity is not None
                and path.name not in cleanup_names):
            # os.replace can succeed before a wrapper or the following parent
            # fsync raises.  Identity comparison makes checking both names safe:
            # an old destination or an attacker replacement is never removed.
            cleanup_names.append(path.name)
        for cleanup_name in cleanup_names:
            try:
                _unlink_identity(parent_fd, cleanup_name, created_identity)
            except BaseException:
                pass
    close_error = None
    try:
        os.close(parent_fd)
    except BaseException as exc:
        close_error = exc
    if primary is not None:
        raise primary.with_traceback(primary_traceback)
    if close_error is not None:
        raise close_error
    return result


def _atomic_secret(path: Path, data: bytes, *, exclusive: bool = False) -> Path:
    """Write only relative to the parent capability that passed validation."""
    path = secret_destination(path)
    return _atomic_secret_dirfd(path, data, exclusive=exclusive)


def codex_destination_check(*, env=None) -> dict:
    source = os.environ if env is None else env
    try:
        target = _checked_secret_destination(codex_home(source) / "auth.json")
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    return _result("passed", credential_file=str(target), secret_printed=False)


def _refresh_timestamp(document: dict) -> datetime | None:
    value = document.get("last_refresh")
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _valid_codex_document(document) -> bool:
    tokens = document.get("tokens") if isinstance(document, dict) else None
    return (isinstance(tokens, dict)
            and any(isinstance(value, str) and value for value in tokens.values()))


def materialize_codex(*, env=None) -> dict:
    source = os.environ if env is None else env
    encoded = source.get("CODEX_AUTH_JSON")
    if not encoded:
        return _result("missing", reason="CODEX_AUTH_JSON")
    target = codex_home(source) / "auth.json"
    checked = codex_destination_check(env=source)
    if checked["status"] != "passed":
        return checked
    target = Path(checked["credential_file"])
    try:
        raw = base64.b64decode(encoded, validate=True)
        parsed = json.loads(raw)
        if not _valid_codex_document(parsed):
            raise ValueError("missing tokens object")
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return _result("rejected", reason="malformed_CODEX_AUTH_JSON")
    try:
        try:
            disk_raw = _read_secret_bytes(target)
            disk = json.loads(disk_raw)
        except FileNotFoundError:
            disk_raw, disk = b"", None
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            disk_raw, disk = b"", None
        if disk_raw == raw:
            return _result("passed", credential_file=str(target), changed=False,
                           secret_printed=False)
        disk_refresh = _refresh_timestamp(disk) if _valid_codex_document(disk) else None
        env_refresh = _refresh_timestamp(parsed)
        if disk_refresh is not None and env_refresh is not None and disk_refresh >= env_refresh:
            return _result("passed", credential_file=str(target), changed=False,
                           reason="on_disk_newer_or_equal", secret_printed=False)
        _atomic_secret(target, raw)
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    return _result("passed", credential_file=str(target), changed=True, secret_printed=False)


def _emit_sanitized(data: str, stream) -> None:
    stream.write(TOKEN_RE.sub("[REDACTED]", data))
    stream.flush()


def _drain_sanitized(pending: str, stream, *, final: bool = False) -> str:
    """Stream safe text while retaining every possible credential prefix.

    Once the literal token prefix appears, nothing through the first non-token
    byte is emitted.  There is deliberately no maximum token length.
    """
    while pending:
        at = pending.find(TOKEN_PREFIX)
        if at >= 0:
            _emit_sanitized(pending[:at], stream)
            candidate = pending[at:]
            end = len(TOKEN_PREFIX)
            while end < len(candidate) and (candidate[end].isalnum() or candidate[end] in "_-"):
                end += 1
            if end == len(candidate) and not final:
                return candidate
            stream.write("[REDACTED]")
            stream.flush()
            pending = candidate[end:]
            continue
        if final:
            _emit_sanitized(pending, stream)
            return ""
        keep = min(len(pending), len(TOKEN_PREFIX) - 1)
        _emit_sanitized(pending[:-keep] if keep else pending, stream)
        return pending[-keep:] if keep else ""
    return ""


def capture_claude(output: Path, *, timeout: int = 300, env=None, input_stream=None,
                   output_stream=None) -> dict:
    """Run ``claude setup-token`` on a real PTY, relay prompts, retain token privately."""
    try:
        output = _checked_secret_destination(output)
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    import pty

    source = os.environ if env is None else env
    input_stream = sys.stdin if input_stream is None else input_stream
    output_stream = sys.stdout if output_stream is None else output_stream
    try:
        bound = _bind_provider_executable("claude", source)
        provider_source = _bound_provider_source(source, bound)
    except _ProviderExecutableError as exc:
        return _result("not_measured", reason=exc.reason)
    try:
        with _isolated_child_env(provider_source) as child:
            master, slave = pty.openpty()
            try:
                argv = _provider_argv(bound, ["setup-token"])
                proc = subprocess.Popen(argv, stdin=slave, stdout=slave,
                                        stderr=slave, env=child, close_fds=True)
            except _ProviderExecutableError as exc:
                os.close(master); os.close(slave)
                return _result("not_measured", reason=exc.reason)
            except OSError:
                os.close(master); os.close(slave)
                return _result("not_measured", reason="provider_spawn_failed")
            os.close(slave)
            deadline, captured, pending = time.monotonic() + timeout, "", ""
            input_fd = None
            try:
                input_fd = input_stream.fileno()
            except (AttributeError, OSError):
                pass
            try:
                while True:
                    if time.monotonic() >= deadline:
                        proc.kill(); proc.wait()
                        return _result("not_measured", reason="timeout")
                    readers = [master] + ([input_fd] if input_fd is not None else [])
                    ready, _, _ = select.select(readers, [], [], .1)
                    if input_fd in ready:
                        chunk = os.read(input_fd, 4096)
                        if chunk:
                            os.write(master, chunk)
                    if master in ready:
                        try:
                            raw = os.read(master, 4096)
                        except OSError as exc:
                            if exc.errno != errno.EIO:
                                raise
                            raw = b""
                        if raw:
                            text = raw.decode("utf-8", "replace")
                            captured += text
                            pending = _drain_sanitized(pending + text, output_stream)
                        elif proc.poll() is not None:
                            break
                    if proc.poll() is not None and master not in ready:
                        break
            finally:
                os.close(master)
                if proc.poll() is None:
                    proc.kill(); proc.wait()
    except OSError:
        # A cleanup failure raised by the context exit overrides any inner
        # would-be success/timeout return and prevents secret materialization.
        return _result("not_measured", reason="provider_storage_unavailable")
    _drain_sanitized(pending, output_stream, final=True)
    found = TOKEN_RE.findall(captured)
    combined = captured.lower()
    if proc.returncode:
        status = _claude_failure_status(combined)
        return _result(status, reason="setup_failed", returncode=proc.returncode)
    if len(found) != 1:
        status = _claude_failure_status(combined)
        if status == "not_measured":
            return _result(status, reason="token_missing_or_ambiguous", returncode=0)
        return _result(status, reason="setup_failed", returncode=0)
    try:
        _atomic_secret(output, (found[0] + "\n").encode())
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    return _result("passed", credential_file=str(output), secret_printed=False)


_CLAUDE_REFUSAL_PATTERNS = tuple(re.compile(pattern) for pattern in (
    r"\b(?:401\s+unauthorized|403\s+forbidden)\b",
    r"\b(?:invalid|expired|revoked)\s+(?:oauth\s+)?(?:token|credentials?|api key)\b",
    r"\b(?:oauth\s+)?(?:token|credentials?|api key)\s+"
    r"(?:is\s+|has\s+)?(?:invalid|expired|revoked|rejected)\b",
    r"\bauthentication\s+(?:failed|rejected|denied)\s*[:\-]?\s*"
    r"(?:invalid|expired|revoked|missing)\s+(?:oauth\s+)?(?:token|credentials?)\b",
    r"\blogin\s+(?:required|rejected|denied)\b",
    r"\bmodel not found\b",
    r"\bmodel access(?: is)? (?:denied|rejected)\b",
    r"\bmodel is not available(?: for (?:this|the) account)?\b",
    r"\bunsupported model\b",
))


def _claude_refusal_evidenced(combined: str) -> bool:
    """Accept only closed credential/model refusal phrases, not broad words."""
    return any(pattern.search(combined) for pattern in _CLAUDE_REFUSAL_PATTERNS)


_TRANSPORT_FAILURE_PATTERNS = tuple(re.compile(pattern) for pattern in (
    r"\bconnection (?:reset|refused|timed out)\b",
    r"\b(?:unable|could not|failed) to connect\b",
    r"\b(?:could not|failed to) resolve (?:host|hostname)\b",
    r"\b(?:name resolution|dns lookup|dns resolution) (?:failed|failure)\b",
    r"\bnetwork is unreachable\b",
    r"\bno route to host\b",
    r"\b(?:socket error|econnreset|econnrefused|etimedout)\b",
    r"\btls handshake (?:failed|failure|timed out)\b",
))


def _transport_failure_evidenced(combined: str) -> bool:
    return any(pattern.search(combined) for pattern in _TRANSPORT_FAILURE_PATTERNS)


def _claude_failure_status(combined: str) -> str:
    if _claude_refusal_evidenced(combined):
        return "rejected"
    if _transport_failure_evidenced(combined):
        return "network_error"
    return "not_measured"


def _exact_marker_present(output: str, marker: str) -> bool:
    return any(line.strip() == marker for line in (output or "").splitlines())


def claude_probe(token_file: Path | None = None, *, timeout=20, env=None) -> dict:
    source = os.environ if env is None else env
    try:
        bound = _bind_provider_executable("claude", source)
    except _ProviderExecutableError as exc:
        return _result("not_measured", reason=exc.reason)
    token = source.get("CLAUDE_CODE_OAUTH_TOKEN")
    if not token and token_file:
        try:
            token = token_file.read_text(encoding="utf-8").strip()
        except OSError:
            return _result("not_measured", reason="credential_file_unreadable")
    if not token:
        return _result("missing", reason="CLAUDE_CODE_OAUTH_TOKEN")
    marker = "TRALUAT-CLAUDE-CREDENTIAL-OK"
    try:
        provider_source = _bound_provider_source(source, bound)
        with _isolated_child_env(
                provider_source, CLAUDE_CODE_OAUTH_TOKEN=token) as child:
            try:
                argv = _provider_argv(
                    bound, ["-p", f"Print exactly: {marker}"])
                p = subprocess.run(argv,
                                   stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                   timeout=timeout, env=child)
            except subprocess.TimeoutExpired:
                return _result("not_measured", reason="timeout")
            except _ProviderExecutableError as exc:
                return _result("not_measured", reason=exc.reason)
            except OSError:
                return _result("not_measured", reason="provider_spawn_failed")
    except OSError:
        return _result("not_measured", reason="provider_storage_unavailable")
    combined = ((p.stderr or "") + "\n" + (p.stdout or "")).lower()
    if p.returncode != 0:
        return _result(_claude_failure_status(combined), returncode=p.returncode)
    if not _exact_marker_present(p.stdout or "", marker):
        status = _claude_failure_status(combined)
        details = {"returncode": 0}
        if status == "not_measured":
            details["reason"] = "marker_missing"
        return _result(status, **details)
    return _result("passed", returncode=0)


def _github_failure_status(stdout: str, stderr: str) -> str:
    """Classify auth only from an HTTP response evidenced as GitHub's."""
    combined = (stdout or "") + "\n" + (stderr or "")
    status_lines = list(re.finditer(
        r"(?mi)^HTTP/\S+\s+(\d{3})\b[^\r\n]*", combined))
    for index, match in enumerate(status_lines):
        block_end = (status_lines[index + 1].start()
                     if index + 1 < len(status_lines) else len(combined))
        block = combined[match.end():block_end]
        header_end = re.search(r"\r?\n\r?\n", block)
        headers = block[:header_end.start()] if header_end else block
        if (int(match.group(1)) in (401, 403, 404)
                and re.search(r"(?mi)^X-GitHub-[^:]+:", headers)):
            return "rejected"
    if _transport_failure_evidenced(combined.lower()):
        return "network_error"
    return "not_measured"


def github_probe(repo: str, *, timeout: int = 20, env=None) -> dict:
    source = os.environ if env is None else env
    try:
        bound = _bind_provider_executable("gh", source)
    except _ProviderExecutableError as exc:
        return _result("not_measured", reason=exc.reason, endpoints={})
    token = source.get("GITHUB_PAT")
    if not token:
        return _result("missing", endpoints={})
    results = {}
    try:
        provider_source = _bound_provider_source(source, bound)
        with _isolated_child_env(provider_source, GH_TOKEN=token) as child:
            for endpoint in ("user", f"repos/{repo}"):
                try:
                    argv = _provider_argv(
                        bound, ["api", endpoint, "--include", "--silent"])
                    p = subprocess.run(argv, capture_output=True,
                                       text=True, timeout=timeout, env=child)
                except subprocess.TimeoutExpired:
                    results[endpoint] = "not_measured"
                except _ProviderExecutableError:
                    results[endpoint] = "not_measured"
                except OSError:
                    results[endpoint] = "not_measured"
                else:
                    results[endpoint] = "passed" if p.returncode == 0 else (
                        _github_failure_status(p.stdout, p.stderr))
    except OSError:
        return _result("not_measured", reason="provider_storage_unavailable", endpoints={})
    vals = set(results.values())
    status = "passed" if vals == {"passed"} else "rejected" if "rejected" in vals else (
        "network_error" if "network_error" in vals else "not_measured")
    return _result(status, endpoints=results)


def tl_bootstrap(env_name: str, secrets_file: Path | None, *, timeout: int = 600, env=None) -> dict:
    source = os.environ if env is None else env
    if secrets_file is None:
        return _result("missing", reason="secrets_file")
    if not source.get("TL_MASTER_KEY"):
        return _result("missing", reason="TL_MASTER_KEY")
    try:
        repository = REPOSITORY_ROOT.resolve(strict=True)
        script = (repository / "scripts" / "tl.py").resolve(strict=True)
        if script.parent.parent != repository:
            return _result("not_measured", reason="unexpected_tl_script")
        resolved_secrets = secret_destination(secrets_file)
        home = str(directory_destination(Path(source.get("HOME") or Path.home())))
        storage = {"HOME": home}
        for key in ("XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME",
                    "GOOGLE_WORKSPACE_CLI_CONFIG_DIR", "TL_CACHE_DIR",
                    "TMPDIR", "TMP", "TEMP"):
            if source.get(key):
                storage[key] = str(directory_destination(Path(source[key])))
        child = _child_env(source, TL_MASTER_KEY=source["TL_MASTER_KEY"], **storage)
        home = Path(child["HOME"])
        delegated_targets = [
            home / ".tra_luat_config.json",
            home / ".notebooklm-mcp-cli" / "auth.json",
            home / ".local" / "bin" / "gws",
            Path(child.get("GOOGLE_WORKSPACE_CLI_CONFIG_DIR")
                 or home / ".config" / "gws") / "credentials.json",
        ]
        for target in delegated_targets:
            secret_destination(target)
        cmd = [sys.executable, str(script), "bootstrap", "--env", env_name,
               "--secrets-file", str(resolved_secrets)]
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=timeout,
                           cwd=repository,
                           env=child)
    except subprocess.TimeoutExpired:
        return _result("not_measured", reason="timeout")
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="cli_missing")
    outcomes = {
        0: ("passed", None),
        1: ("not_measured", "degraded"),
        2: ("not_measured", "precondition"),
        3: ("rejected", "credential_or_bundle_rejected"),
    }
    status, reason = outcomes.get(
        p.returncode, ("not_measured", "unclassified_exit"))
    details = {"returncode": p.returncode}
    if reason is not None:
        details["reason"] = reason
    return _result(status, **details)


def bootstrap_session(repo: str, env_name: str, secrets_file: Path | None,
                      claude_token_file: Path | None, *, env=None) -> dict:
    if secrets_file is None:
        return _result("missing", reason="secrets_file")
    source = os.environ if env is None else env
    components = {
        "codex": materialize_codex(env=source),
        "claude": claude_probe(claude_token_file, env=source),
        "github": github_probe(repo, env=source),
        "tl": tl_bootstrap(env_name, secrets_file, env=source),
    }
    statuses = {x["status"] for x in components.values()}
    overall = "passed" if statuses == {"passed"} else next(
        (s for s in ("rejected", "network_error", "not_measured", "missing") if s in statuses))
    return _result(overall, components=components)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("claude-capture"); c.add_argument("--output", required=True); c.add_argument("--timeout", type=int, default=300)
    g = sub.add_parser("github-probe"); g.add_argument("--repo", default="ducthangho/tra-luat"); g.add_argument("--timeout", type=int, default=20)
    b = sub.add_parser("tl-bootstrap"); b.add_argument("--env", choices=("code", "cowork", "chat"), required=True); b.add_argument("--secrets-file", required=True); b.add_argument("--timeout", type=int, default=600)
    i = sub.add_parser("bootstrap"); i.add_argument("--repo", default="ducthangho/tra-luat"); i.add_argument("--env", choices=("code", "cowork", "chat"), required=True); i.add_argument("--secrets-file", required=True); i.add_argument("--claude-token-file")
    sub.add_parser("codex-materialize")
    sub.add_parser("codex-destination-check")
    sub.add_parser("status")
    a = ap.parse_args(argv)
    if a.command == "codex-materialize": result = materialize_codex()
    elif a.command == "codex-destination-check": result = codex_destination_check()
    elif a.command == "claude-capture": result = capture_claude(Path(a.output), timeout=a.timeout)
    elif a.command == "github-probe": result = github_probe(a.repo, timeout=a.timeout)
    elif a.command == "tl-bootstrap": result = tl_bootstrap(a.env, Path(a.secrets_file) if a.secrets_file else None, timeout=a.timeout)
    elif a.command == "bootstrap": result = bootstrap_session(a.repo, a.env, Path(a.secrets_file) if a.secrets_file else None, Path(a.claude_token_file) if a.claude_token_file else None)
    else: result = _result("not_measured", codex_home=str(codex_home()), present={name: bool(os.environ.get(name)) for name in SECRET_ENV})
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "passed" or a.command == "status" else 3


if __name__ == "__main__":
    raise SystemExit(main())
