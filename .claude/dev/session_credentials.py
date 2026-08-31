#!/usr/bin/env python3
"""Secret-safe bootstrap and live probes for an ephemeral agent session.

Secret values are read from the environment or a 0600 file, are never accepted as
arguments, and are only copied into the environment of the CLI that consumes them.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SECRET_ENV = ("CODEX_AUTH_JSON", "CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_PAT", "TL_MASTER_KEY")
TOKEN_RE = re.compile(r"\b(sk-ant-oat\d+-[A-Za-z0-9_-]{20,})\b")


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
            out.write(data); out.flush(); os.fsync(out.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        tmp.unlink(missing_ok=True)


def capture_claude(output: Path, *, timeout: int = 300, env=None) -> dict:
    """Run the official setup flow and privately retain only its OAuth token."""
    child = dict(os.environ if env is None else env)
    try:
        p = subprocess.run(["claude", "setup-token"], input="", capture_output=True,
                           text=True, timeout=timeout, env=child)
    except subprocess.TimeoutExpired:
        return {"status": "not_measured", "reason": "timeout"}
    except OSError:
        return {"status": "not_measured", "reason": "cli_missing"}
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    found = TOKEN_RE.findall(combined)
    if p.returncode or len(found) != 1:
        return {"status": "rejected" if p.returncode else "malformed", "reason": "setup_failed"}
    _atomic_secret(output, (found[0] + "\n").encode())
    return {"status": "passed", "credential_file": str(output), "secret_printed": False}


def github_probe(repo: str, *, timeout: int = 20, env=None) -> dict:
    """Probe both required endpoints; PAT exists only in each ``gh`` child."""
    source = os.environ if env is None else env
    token = source.get("GITHUB_PAT")
    if not token:
        return {"status": "missing", "endpoints": {}}
    child = dict(source); child["GH_TOKEN"] = token
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
            results[endpoint] = ("passed" if p.returncode == 0 else
                                 "rejected" if "401" in low or "bad credentials" in low
                                 else "network_error")
    vals = set(results.values())
    status = "passed" if vals == {"passed"} else "rejected" if "rejected" in vals else (
        "not_measured" if vals == {"not_measured"} else "network_error")
    return {"status": status, "endpoints": results}


def tl_bootstrap(env_name: str, secrets_file: Path | None, *, timeout: int = 600, env=None) -> dict:
    """Orchestrate the existing tl bootstrap; do not reimplement its crypto/store."""
    source = os.environ if env is None else env
    if not source.get("TL_MASTER_KEY"):
        return {"status": "missing", "reason": "TL_MASTER_KEY"}
    cmd = [sys.executable, "scripts/tl.py", "bootstrap", "--env", env_name]
    if secrets_file:
        cmd += ["--secrets-file", str(secrets_file)]
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=timeout, env=dict(source))
    except subprocess.TimeoutExpired:
        return {"status": "not_measured", "reason": "timeout"}
    except OSError:
        return {"status": "not_measured", "reason": "cli_missing"}
    return {"status": "passed" if p.returncode == 0 else "rejected", "returncode": p.returncode}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("claude-capture"); c.add_argument("--output", required=True); c.add_argument("--timeout", type=int, default=300)
    g = sub.add_parser("github-probe"); g.add_argument("--repo", default="ducthangho/tra-luat"); g.add_argument("--timeout", type=int, default=20)
    b = sub.add_parser("tl-bootstrap"); b.add_argument("--env", choices=("code", "cowork", "chat"), required=True); b.add_argument("--secrets-file"); b.add_argument("--timeout", type=int, default=600)
    s = sub.add_parser("status")
    a = ap.parse_args(argv)
    if a.command == "claude-capture": result = capture_claude(Path(a.output), timeout=a.timeout)
    elif a.command == "github-probe": result = github_probe(a.repo, timeout=a.timeout)
    elif a.command == "tl-bootstrap": result = tl_bootstrap(a.env, Path(a.secrets_file) if a.secrets_file else None, timeout=a.timeout)
    else:
        result = {"status": "not_measured", "codex_home": str(codex_home()),
                  "present": {name: bool(os.environ.get(name)) for name in SECRET_ENV}}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "passed" or a.command == "status" else 3


if __name__ == "__main__":
    raise SystemExit(main())
