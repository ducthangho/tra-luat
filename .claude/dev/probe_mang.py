#!/usr/bin/env python3
"""Phân loại ba kênh mạng; UNKNOWN là KHÔNG_ĐO_ĐƯỢC, không phải bị chặn."""
import errno
import json
import re
import socket
import subprocess
import sys
import urllib.error
import urllib.request
LOT = "LOT"
POLICY_DENIED = "POLICY_DENIED"
ENDPOINT_ERROR = "ENDPOINT_ERROR"
TIMEOUT = "TIMEOUT"
TOOL_ERROR = "TOOL_ERROR"
UNKNOWN = "UNKNOWN"
DNS_ERROR = "DNS_ERROR"
REPOSITORY_ERROR = "REPOSITORY_ERROR"
AUTH_ERROR = "AUTH_ERROR"
def chuan(raw) -> str:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "replace")
    text = " ".join(str(raw).split())
    text = re.sub(r"https?://\S+", "[URL]", text, flags=re.I)
    return re.sub(r"(?i)(token|password|authorization)=\S+", r"\1=[REDACTED]", text)[:240]
def kq(lop, stage, raw="", rc=None):
    return {"lop": lop, "stage": stage, "raw": chuan(raw), "rc": rc}
def phan_loai_loi(exc, stage, endpoint=False):
    if isinstance(exc, urllib.error.HTTPError):
        lop = AUTH_ERROR if exc.code in (401, 403) else ENDPOINT_ERROR
        return kq(lop, stage, f"HTTPError code={exc.code}")
    reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
    raw = f"{type(reason).__name__} errno={getattr(reason, 'errno', None)}: {reason}"
    if isinstance(reason, (TimeoutError, socket.timeout)):
        return kq(TIMEOUT, stage, raw)
    if isinstance(reason, socket.gaierror):
        return kq(DNS_ERROR, stage, raw)
    if isinstance(reason, PermissionError) or getattr(reason, "errno", None) in (errno.EPERM, errno.EACCES):
        return kq(POLICY_DENIED, stage, raw)
    if endpoint and isinstance(reason, ValueError):
        return kq(ENDPOINT_ERROR, stage, raw)
    return kq(UNKNOWN, stage, raw)
def kenh_socket_loopback():
    """Ghi đúng giai đoạn create/bind/listen; loopback không phải egress."""
    s, stage = None, "create"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stage = "bind"
        s.bind(("127.0.0.1", 0))
        stage = "listen"
        s.listen(1)
        return kq(LOT, "done")
    except Exception as exc:  # socket_channel
        return phan_loai_loi(exc, stage)
    finally:
        if s is not None:
            try:
                s.close()
            except Exception:
                pass
def kenh_urlopen(url="https://api.github.com", timeout=5.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            resp.read(1)
        return kq(LOT, "done")
    except Exception as exc:  # url_channel
        return phan_loai_loi(exc, "urlopen", endpoint=True)
def phan_loai_git(stderr: str):
    s = chuan(stderr).lower()
    bang = [
        (AUTH_ERROR, ("authentication failed", "could not read username", "publickey", "authorization failed")),
        (REPOSITORY_ERROR, ("repository not found", "does not appear to be a git repository")),
        (DNS_ERROR, ("could not resolve host", "name or service not known")),
        (TIMEOUT, ("timed out", "timeout")),
        (ENDPOINT_ERROR, ("bad/illegal format", "unsupported protocol")),
        (POLICY_DENIED, ("operation not permitted", "network is unreachable", "permission denied")),
    ]
    return next((lop for lop, mau in bang if any(x in s for x in mau)), UNKNOWN)
def kenh_git_ls_remote(url="https://github.com/ducthangho/tra-luat.git", timeout=10.0):
    try:
        p = subprocess.run(["git", "ls-remote", url, "HEAD"], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout)
        if p.returncode == 0:
            return kq(LOT, "done", rc=0)
        return kq(phan_loai_git(p.stderr), "ls-remote", p.stderr, p.returncode)
    except FileNotFoundError as exc:  # git_channel
        return kq(TOOL_ERROR, "spawn", exc)
    except subprocess.TimeoutExpired as exc:
        return kq(TIMEOUT, "ls-remote", exc)
    except Exception as exc:
        return phan_loai_loi(exc, "ls-remote")
def main():
    cac_kenh = {"socket_loopback": kenh_socket_loopback(), "urlopen": kenh_urlopen(),
                "git_ls_remote": kenh_git_ls_remote()}
    for ten, x in cac_kenh.items():
        legacy = int(x["lop"] != LOT)
        print(f"{ten}={legacy} class={x['lop']} stage={x['stage']} rc={x['rc']} "
              f"raw={json.dumps(x['raw'], ensure_ascii=False)}")
    return int(any(x["lop"] == UNKNOWN for x in cac_kenh.values()))
if __name__ == "__main__":
    sys.exit(main())
