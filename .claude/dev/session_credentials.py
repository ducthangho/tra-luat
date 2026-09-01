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
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

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
    "PATH", "HOME", "USER", "LOGNAME", "SHELL", "TERM",
    "TMPDIR", "TMP", "TEMP",
    "LANG", "LANGUAGE", "LC_ALL", "TZ",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
    "http_proxy", "https_proxy", "all_proxy", "no_proxy",
    "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE",
    "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "CODEX_HOME",
    "XDG_DATA_HOME", "GOOGLE_WORKSPACE_CLI_CONFIG_DIR", "TL_CACHE_DIR",
    "PYTHONUTF8", "PYTHONIOENCODING",
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


def _result(status: str, **details) -> dict:
    if status not in STATUSES:
        raise ValueError(f"invalid status: {status}")
    return {"status": status, **details}


def codex_home(env=None) -> Path:
    env = os.environ if env is None else env
    return Path(env.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def secret_destination(path: Path) -> Path:
    """Return the canonical target only when it is outside this checkout."""
    target = path.expanduser()
    resolved = target.resolve(strict=False)
    repository = REPOSITORY_ROOT.resolve(strict=True)
    if resolved == repository or repository in resolved.parents:
        raise UnsafeSecretDestination(f"refusing repository secret destination: {target}")
    if target.is_symlink():
        raise OSError(f"refusing symlink destination: {target}")
    # Callers must use this value.  Returning the mutable alias after validating
    # ``resolved`` re-opens the parent-link swap that the policy just closed.
    return resolved


@contextlib.contextmanager
def _hold_parent_directory(parent: Path):
    """Prevent replacement of a validated Windows parent while it is in use."""
    if os.name != "nt":
        yield
        return
    import ctypes
    from ctypes import wintypes
    create_file = ctypes.windll.kernel32.CreateFileW
    create_file.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                            wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD,
                            wintypes.HANDLE]
    create_file.restype = wintypes.HANDLE
    close_handle = ctypes.windll.kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL
    # Share read/write but deliberately not delete: rename/replacement of this
    # directory is refused until the secret write completes.
    handle = create_file(str(parent), 0x80, 0x1 | 0x2, None, 3, 0x02000000, None)
    invalid = ctypes.c_void_p(-1).value
    if handle in (None, invalid):
        raise ctypes.WinError()
    try:
        yield
    finally:
        close_handle(handle)


def _write_secret_fd(fd: int, data: bytes) -> None:
    try:
        os.fchmod(fd, 0o600)
    except Exception:
        os.close(fd)
        raise
    with os.fdopen(fd, "wb") as out:
        out.write(data)
        out.flush()
        os.fsync(out.fileno())


def _atomic_secret_dirfd(path: Path, data: bytes, *, exclusive: bool) -> Path:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    parent_fd = os.open(path.parent, flags)
    created_name = None
    try:
        named = os.stat(path.parent, follow_symlinks=False)
        opened = os.fstat(parent_fd)
        if (named.st_dev, named.st_ino) != (opened.st_dev, opened.st_ino):
            raise OSError("validated secret parent changed before use")
        if exclusive:
            created_name = path.name
            fd = os.open(created_name,
                         os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=parent_fd)
            _write_secret_fd(fd, data)
        else:
            for _ in range(128):
                candidate = f".{path.name}.tmp-{secrets.token_hex(12)}"
                try:
                    fd = os.open(candidate,
                                 os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o600, dir_fd=parent_fd)
                except FileExistsError:
                    continue
                created_name = candidate
                break
            else:
                raise OSError("could not allocate secret temporary file")
            _write_secret_fd(fd, data)
            try:
                existing = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                existing = None
            if existing is not None and stat.S_ISLNK(existing.st_mode):
                raise OSError(f"refusing symlink destination: {path}")
            os.replace(created_name, path.name,
                       src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
            created_name = None
        try:
            os.fsync(parent_fd)
        except OSError as exc:
            if exc.errno not in (errno.EINVAL, getattr(errno, "ENOTSUP", errno.EINVAL)):
                raise
        return path
    except Exception:
        if created_name is not None:
            try:
                os.unlink(created_name, dir_fd=parent_fd)
            except OSError:
                pass
        raise
    finally:
        os.close(parent_fd)


def _atomic_secret_path(path: Path, data: bytes, *, exclusive: bool) -> Path:
    """Fallback used while a Windows parent handle prevents path replacement."""
    with _hold_parent_directory(path.parent):
        identity = path.parent.stat()
        parent_id = (identity.st_dev, identity.st_ino)
        if exclusive:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC, 0o600)
            created = path
            try:
                _write_secret_fd(fd, data)
                return path
            except Exception:
                created.unlink(missing_ok=True)
                raise
        fd, name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=path.parent)
        tmp = Path(name)
        try:
            _write_secret_fd(fd, data)
            current = path.parent.stat()
            if (current.st_dev, current.st_ino) != parent_id:
                raise OSError("validated secret parent changed before replace")
            if path.is_symlink():
                raise OSError(f"refusing symlink destination: {path}")
            os.replace(tmp, path)
            os.chmod(path, 0o600)
            return path
        finally:
            tmp.unlink(missing_ok=True)


def _atomic_secret(path: Path, data: bytes, *, exclusive: bool = False) -> Path:
    """Write through the validated parent identity, never through its old alias."""
    path = secret_destination(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path = secret_destination(path)
    if (os.name == "posix" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
            and os.open in os.supports_dir_fd and os.replace in os.supports_dir_fd):
        return _atomic_secret_dirfd(path, data, exclusive=exclusive)
    return _atomic_secret_path(path, data, exclusive=exclusive)


def codex_destination_check(*, env=None) -> dict:
    source = os.environ if env is None else env
    try:
        target = secret_destination(codex_home(source) / "auth.json")
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    return _result("passed", credential_file=str(target), secret_printed=False)


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
        if not isinstance(parsed, dict) or not isinstance(parsed.get("tokens"), dict):
            raise ValueError("missing tokens object")
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return _result("rejected", reason="malformed_CODEX_AUTH_JSON")
    try:
        _atomic_secret(target, raw)
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    return _result("passed", credential_file=str(target), secret_printed=False)


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
        output = secret_destination(output)
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    import pty

    child = _child_env(os.environ if env is None else env)
    input_stream = sys.stdin if input_stream is None else input_stream
    output_stream = sys.stdout if output_stream is None else output_stream
    master, slave = pty.openpty()
    try:
        proc = subprocess.Popen(["claude", "setup-token"], stdin=slave, stdout=slave,
                                stderr=slave, env=child, close_fds=True)
    except OSError:
        os.close(master); os.close(slave)
        return _result("not_measured", reason="cli_missing")
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
    _drain_sanitized(pending, output_stream, final=True)
    found = TOKEN_RE.findall(captured)
    if proc.returncode or len(found) != 1:
        return _result("rejected", reason="setup_failed")
    try:
        _atomic_secret(output, (found[0] + "\n").encode())
    except UnsafeSecretDestination:
        return _result("rejected", reason="secret_destination_in_repository")
    except OSError:
        return _result("not_measured", reason="write_failed")
    return _result("passed", credential_file=str(output), secret_printed=False)


def claude_probe(token_file: Path | None = None, *, timeout=20, env=None) -> dict:
    source = os.environ if env is None else env
    token = source.get("CLAUDE_CODE_OAUTH_TOKEN")
    if not token and token_file:
        try:
            token = token_file.read_text(encoding="utf-8").strip()
        except OSError:
            return _result("not_measured", reason="credential_file_unreadable")
    if not token:
        return _result("missing", reason="CLAUDE_CODE_OAUTH_TOKEN")
    child = _child_env(source, CLAUDE_CODE_OAUTH_TOKEN=token)
    marker = "TRALUAT-CLAUDE-CREDENTIAL-OK"
    try:
        p = subprocess.run(["claude", "-p", f"Print exactly: {marker}"], stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=timeout, env=child)
    except subprocess.TimeoutExpired:
        return _result("not_measured", reason="timeout")
    except OSError:
        return _result("not_measured", reason="cli_missing")
    combined = ((p.stderr or "") + "\n" + (p.stdout or "")).lower()
    refused = any(word in combined for word in ("401", "403", "unauthorized", "authentication",
                                                 "invalid token", "oauth", "login"))
    if p.returncode != 0:
        return _result("rejected" if refused else "network_error", returncode=p.returncode)
    if marker not in (p.stdout or ""):
        return _result("rejected", reason="marker_missing", returncode=0)
    return _result("passed", returncode=0)


def github_probe(repo: str, *, timeout: int = 20, env=None) -> dict:
    source = os.environ if env is None else env
    token = source.get("GITHUB_PAT")
    if not token:
        return _result("missing", endpoints={})
    child = _child_env(source, GH_TOKEN=token)
    results = {}
    for endpoint in ("user", f"repos/{repo}"):
        try:
            p = subprocess.run(["gh", "api", endpoint, "--silent"], capture_output=True,
                               text=True, timeout=timeout, env=child)
        except subprocess.TimeoutExpired:
            results[endpoint] = "network_error"
        except OSError:
            results[endpoint] = "not_measured"
        else:
            low = ((p.stderr or "") + (p.stdout or "")).lower()
            auth_failure = any(x in low for x in ("401", "403", "404", "bad credentials",
                                                   "authentication", "not found"))
            results[endpoint] = "passed" if p.returncode == 0 else (
                "rejected" if auth_failure else "network_error")
    vals = set(results.values())
    status = "passed" if vals == {"passed"} else "rejected" if "rejected" in vals else (
        "not_measured" if vals == {"not_measured"} else "network_error")
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
        child = _child_env(source, TL_MASTER_KEY=source["TL_MASTER_KEY"])
        child["HOME"] = str(secret_destination(Path(child.get("HOME") or Path.home())))
        for key in ("XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME",
                    "GOOGLE_WORKSPACE_CLI_CONFIG_DIR", "TL_CACHE_DIR",
                    "TMPDIR", "TMP", "TEMP"):
            if child.get(key):
                child[key] = str(secret_destination(Path(child[key])))
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
    return _result("passed" if p.returncode == 0 else "rejected", returncode=p.returncode)


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
