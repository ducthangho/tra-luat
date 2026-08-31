#!/usr/bin/env python3
"""Secret-safe credential bootstrap for an ephemeral agent session."""
from __future__ import annotations

import argparse
import base64
import errno
import json
import os
import re
import select
import subprocess
import sys
import tempfile
import time
from pathlib import Path

STATUSES = ("missing", "rejected", "network_error", "not_measured", "passed")
SECRET_ENV = ("CODEX_AUTH_JSON", "CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_PAT", "TL_MASTER_KEY")
TOKEN_RE = re.compile(r"sk-ant-oat\d+-[A-Za-z0-9_-]{20,}")
TOKEN_PREFIX = "sk-ant-oat"


def _result(status: str, **details) -> dict:
    if status not in STATUSES:
        raise ValueError(f"invalid status: {status}")
    return {"status": status, **details}


def codex_home(env=None) -> Path:
    env = os.environ if env is None else env
    return Path(env.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def _atomic_secret(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise OSError(f"refusing symlink destination: {path}")
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=path.parent)
    tmp = Path(name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        tmp.unlink(missing_ok=True)


def materialize_codex(*, env=None) -> dict:
    source = os.environ if env is None else env
    encoded = source.get("CODEX_AUTH_JSON")
    if not encoded:
        return _result("missing", reason="CODEX_AUTH_JSON")
    try:
        raw = base64.b64decode(encoded, validate=True)
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError("not an object")
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return _result("rejected", reason="malformed_CODEX_AUTH_JSON")
    target = codex_home(source) / "auth.json"
    try:
        _atomic_secret(target, raw)
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
    import pty

    child = dict(os.environ if env is None else env)
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
    _atomic_secret(output, (found[0] + "\n").encode())
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
    child = dict(source, CLAUDE_CODE_OAUTH_TOKEN=token)
    child.pop("ANTHROPIC_API_KEY", None)
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
    child = dict(source, GH_TOKEN=token)
    for key in ("GITHUB_PAT", "GITHUB_TOKEN"):
        child.pop(key, None)
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
    if not source.get("TL_MASTER_KEY"):
        return _result("missing", reason="TL_MASTER_KEY")
    cmd = [sys.executable, "scripts/tl.py", "bootstrap", "--env", env_name]
    if secrets_file:
        cmd += ["--secrets-file", str(secrets_file)]
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=timeout, env=dict(source))
    except subprocess.TimeoutExpired:
        return _result("not_measured", reason="timeout")
    except OSError:
        return _result("not_measured", reason="cli_missing")
    return _result("passed" if p.returncode == 0 else "rejected", returncode=p.returncode)


def bootstrap_session(repo: str, env_name: str, secrets_file: Path | None,
                      claude_token_file: Path | None, *, env=None) -> dict:
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
    b = sub.add_parser("tl-bootstrap"); b.add_argument("--env", choices=("code", "cowork", "chat"), required=True); b.add_argument("--secrets-file"); b.add_argument("--timeout", type=int, default=600)
    i = sub.add_parser("bootstrap"); i.add_argument("--repo", default="ducthangho/tra-luat"); i.add_argument("--env", choices=("code", "cowork", "chat"), required=True); i.add_argument("--secrets-file"); i.add_argument("--claude-token-file")
    sub.add_parser("status")
    a = ap.parse_args(argv)
    if a.command == "claude-capture": result = capture_claude(Path(a.output), timeout=a.timeout)
    elif a.command == "github-probe": result = github_probe(a.repo, timeout=a.timeout)
    elif a.command == "tl-bootstrap": result = tl_bootstrap(a.env, Path(a.secrets_file) if a.secrets_file else None, timeout=a.timeout)
    elif a.command == "bootstrap": result = bootstrap_session(a.repo, a.env, Path(a.secrets_file) if a.secrets_file else None, Path(a.claude_token_file) if a.claude_token_file else None)
    else: result = _result("not_measured", codex_home=str(codex_home()), present={name: bool(os.environ.get(name)) for name in SECRET_ENV})
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "passed" or a.command == "status" else 3


if __name__ == "__main__":
    raise SystemExit(main())
