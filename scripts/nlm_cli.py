#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nlm_cli.py — adapter gọi CLI `nlm` (package notebooklm-mcp-cli, jacob-bd) TRỰC TIẾP trong
Claude Code/Cowork, KHÔNG qua MCP server.

Vì sao: MCP `source_list_drive` ép freshness → timeout ~4 phút trên notebook lớn. CLI
`nlm source list <nb> --drive --skip-freshness` làm cùng việc trong ~4s (đo thật: 299 nguồn/4.0s).

Gate: chỉ dùng khi `nlm` có trên PATH + auth OK; nếu không trả {"ok": False, "fallback": "mcp"}
để caller quay lại MCP notebook_get hoặc hỏi người dùng. CLI auth tự refresh CSRF khi 401; nếu
session hết hạn hẳn cần `nlm login` (TƯƠNG TÁC — không chạy headless được).
"""
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys

# Group E1 (log rà): subprocess nlm/keyring rò dòng "Using keyring backend: keyring" lẫn stdout → VỠ json.loads.
# CHỈ bỏ dòng nhiễu keyring THUẦN (KHÔNG chứa ký tự cấu trúc JSON {}[]) → không bao giờ nuốt thân JSON
# (vd dòng lỗi `{"error":"Using keyring backend failed"}` có '{' → GIỮ). Đồng bộ tinh thần tl_gws._strip_keyring_noise.
_KEYRING_NOISE_RE = re.compile(r"(?i)(using\s+keyring\s+backend|keyring\.backends?|no\s+recommended\s+backend)")


def _strip_keyring(s: str) -> str:
    if not s:
        return s
    kept = [ln for ln in s.splitlines()
            if not (_KEYRING_NOISE_RE.search(ln) and not any(c in ln for c in "{}[]"))]
    return "\n".join(kept)


def _local_bin_paths() -> list[str]:
    """Thư mục thường chứa `nlm` sau `pip install --user`/`uv tool install` mà shell non-login (Cowork)
    KHÔNG có trên PATH: ~/.local/bin + user-base bin/Scripts (POSIX/Windows)."""
    import site
    paths = [os.path.expanduser("~/.local/bin")]
    ub = getattr(site, "USER_BASE", None)
    if ub:
        paths.append(os.path.join(ub, "bin"))       # POSIX
        paths.append(os.path.join(ub, "Scripts"))   # Windows
    seen, out = set(), []
    for p in paths:
        if p and p not in seen:
            seen.add(p); out.append(p)
    return out


def _augmented_path() -> str:
    """PATH hiện tại ĐÃ NỐI ~/.local/bin (+ user-base bin) lên đầu — để tìm/chạy nlm dù shell thiếu PATH đó."""
    extra = os.pathsep.join(_local_bin_paths())
    cur = os.environ.get("PATH", "")
    return extra + (os.pathsep + cur if cur else "")

# UTF-8 hardening (Windows codepage / tiếng Việt)
for _s in (getattr(sys, "stdout", None), getattr(sys, "stderr", None)):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def nlm_exe():
    """Tìm `nlm` KHÔNG chỉ dựa PATH: TL_NLM_BIN → PATH → ~/.local/bin → /usr/local/bin.
    Cowork: pip install --user đặt nlm ở ~/.local/bin (shell không-login có thể KHÔNG có PATH đó)."""
    cand = os.environ.get("TL_NLM_BIN")
    if cand and os.path.exists(cand):
        return cand
    # 2.2 (log rà): tìm nlm với PATH ĐÃ NỐI ~/.local/bin (+ user-base bin) — shell non-login (Cowork) thiếu
    # PATH đó nên `which('nlm')` trần trả None → doctor báo đỏ → NLM rơi MCP (chậm). Nối path → tìm được ngay.
    w = shutil.which("nlm", path=_augmented_path())
    if w:
        return w
    for p in (os.path.expanduser("~/.local/bin/nlm"), os.path.expanduser("~/.local/bin/nlm.exe"),
              "/usr/local/bin/nlm"):
        if os.path.exists(p):
            return p
    return None


def nlm_available() -> bool:
    return nlm_exe() is not None


def _run(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    exe = nlm_exe() or "nlm"
    # 2.2: truyền env với PATH ĐÃ NỐI ~/.local/bin (+ user-base bin) → bản thân nlm gọi tool con (uv/python)
    # vẫn thấy; không phụ thuộc shell người dùng đã export PATH hay chưa.
    env = os.environ.copy()
    env["PATH"] = _augmented_path()
    try:
        p = subprocess.run([exe] + args, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace", env=env)
        # E1: lọc nhiễu keyring khỏi CẢ stdout (để json.loads sạch) lẫn stderr (thông điệp lỗi sạch).
        return p.returncode, _strip_keyring(p.stdout or ""), _strip_keyring(p.stderr or "")
    except FileNotFoundError:
        return 127, "", "nlm không có (PATH / ~/.local/bin) — pip install notebooklm-mcp-cli"
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout {timeout}s"


def source_list(notebook_id: str, skip_freshness: bool = True, drive: bool = True,
                profile: str | None = None, timeout: int = 120) -> dict:
    """Liệt kê nguồn của notebook qua CLI (FAST PATH). Trả:
       {ok:True, count:N, sources:[{id,title,type,url,is_stale}]} hoặc {ok:False, error, fallback:'mcp'}."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    args = ["source", "list", notebook_id, "-j"]
    if drive:
        args.append("-d")
    if skip_freshness:
        args.append("-S")
    if profile:
        args += ["-p", profile]
    rc, out, err = _run(args, timeout=timeout)
    if rc != 0:
        low = (err + out).lower()
        auth = any(t in low for t in ("auth", "401", "login", "unauthor", "credential"))
        return {"ok": False, "rc": rc, "error": f"nlm source list rc={rc}: {(err or out)[:300]}",
                "fallback": "mcp",
                "auth_hint": "Lỗi auth: chạy `nlm login` (TƯƠNG TÁC) rồi thử lại." if auth else None}
    try:
        data = json.loads(out)
    except Exception as e:
        return {"ok": False, "error": f"parse JSON lỗi: {e}", "raw": out[:300], "fallback": "mcp"}
    items = data if isinstance(data, list) else (data.get("sources") or data.get("items") or [])
    return {"ok": True, "count": len(items), "sources": items, "via": "nlm-cli", "skip_freshness": skip_freshness}


def _run_json(args: list[str], timeout: int = 180) -> dict:
    """Chạy lệnh nlm có -j, trả {ok, data} hoặc {ok:False, error, fallback:'mcp'}."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    rc, out, err = _run(args, timeout=timeout)
    if rc != 0:
        low = (err + out).lower()
        auth = any(t in low for t in ("auth", "401", "login", "unauthor", "credential"))
        return {"ok": False, "rc": rc, "error": f"nlm rc={rc}: {(err or out)[:300]}", "fallback": "mcp",
                "auth_hint": "Lỗi auth: `nlm login`." if auth else None}
    try:
        return {"ok": True, "data": json.loads(out), "via": "nlm-cli"}
    except Exception:
        return {"ok": True, "text": out, "via": "nlm-cli"}   # vài lệnh trả text thuần


def source_get(source_id: str, timeout: int = 120) -> dict:
    """Chi tiết 1 source (title/source_type/url/char_count)."""
    return _run_json(["source", "get", source_id, "-j"], timeout=timeout)


def source_content(source_id: str, timeout: int = 180) -> dict:
    """Toàn văn raw của source (thay MCP source_get_content; CLI nhanh + không qua server)."""
    return _run_json(["source", "content", source_id, "-j"], timeout=timeout)


def notebook_query(notebook_id: str, query: str, source_ids=None, timeout: int = 240) -> dict:
    """RAG query trên notebook (thay MCP notebook_query). source_ids: scope (nếu CLI hỗ trợ -s)."""
    args = ["notebook", "query", notebook_id, query, "-j"]
    for sid in (source_ids or []):
        args += ["-s", sid]
    return _run_json(args, timeout=timeout)


# ───────────── NLM WRITE qua CLI (thay MCP source_add/delete/sync — đúng directive CLI-first) ─────────────
# LƯU Ý: `nlm source add/delete/sync` KHÔNG hỗ trợ `-j` (chỉ `source list` có) → parse text output.
import re as _re
_SID_RE = _re.compile(r"Source ID:\s*([0-9a-fA-F-]{36})")


def _add_args(notebook_id: str, drive_id=None, url=None, file=None, text=None,
              doc_type="doc", title=None, wait=True, timeout=600) -> list:
    """PURE: dựng argv cho `nlm source add` (tách để selftest, không shell). KHÔNG có -j."""
    args = ["source", "add", notebook_id]
    if drive_id:
        args += ["--drive", drive_id, "--type", doc_type]
    elif url:
        args += ["--url", url]
    elif file:
        args += ["--file", file]
    elif text is not None:
        args += ["--text", text]
    if title:
        args += ["--title", title]
    if wait:
        args += ["--wait", "--wait-timeout", str(timeout)]
    return args


def _auth_fail(rc: int, out: str, err: str) -> dict:
    low = (err + out).lower()
    auth = any(t in low for t in ("auth", "401", "login", "unauthor", "credential"))
    return {"ok": False, "rc": rc, "error": f"nlm rc={rc}: {(err or out)[:300]}", "fallback": "mcp",
            "auth_hint": "Lỗi auth: chạy `nlm login` rồi thử lại." if auth else None}


def source_add(notebook_id: str, drive_id=None, url=None, file=None, text=None,
               doc_type="doc", title=None, wait=True, timeout=120) -> dict:
    """Thêm nguồn qua CLI `nlm source add` (thay MCP). Trả {ok, source_id, title, ready} hoặc {ok:False, fallback:'mcp'}.
    F5 van 3 (r192): mặc định CHỜ SETTLE TỐI ĐA 120s (trước 600s — đo 23-07: nguồn nhỏ 30-90s, 343k ký tự
    >10' client-timeout nhưng ĂN server-side) — quá ngưỡng thì THÔI CHỜ chứ KHÔNG huỷ (nguồn đang index);
    rc≠0 mà output ĐÃ có Source ID ⇒ add THÀNH CÔNG, chỉ hết giờ chờ → ok=True + settle_timeout=True
    (caller ghi deferred, cuối lô `nlm-reconcile` xác minh); subprocess hard-kill ở timeout+30s → rc=124
    kèm note 'có thể đã ăn server-side' (ĐỪNG add lại mù — reconcile là đường vét)."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    if not (drive_id or url or file or text is not None):
        return {"ok": False, "error": "source_add cần drive_id|url|file|text"}
    rc, out, err = _run(_add_args(notebook_id, drive_id, url, file, text, doc_type, title, wait, timeout), timeout=timeout + 30)
    m = _SID_RE.search(out or "")
    if rc != 0:
        if m:   # van 3: add đã trả Source ID — chỉ là CLI bỏ chờ/hết giờ settle, KHÔNG phải fail
            return {"ok": True, "source_id": m.group(1), "ready": False, "settle_timeout": True,
                    "via": "nlm-cli", "raw": (out or "").strip()[-200:],
                    "note": f"thôi chờ settle sau {timeout}s (nguồn đang index) — nlm-reconcile cuối lô xác minh"}
        r = _auth_fail(rc, out, err)
        if rc == 124:
            r["settle_timeout"] = True
            r["note"] = ("client-timeout — add CÓ THỂ đã ăn server-side: ĐỪNG add lại mù; "
                         "chờ ≥60s rồi `tl nlm-reconcile` xác minh/link.")
        return r
    return {"ok": True, "source_id": (m.group(1) if m else None), "ready": "(ready)" in out,
            "via": "nlm-cli", "raw": out.strip()[-200:]}


def source_delete(source_id: str, timeout: int = 120) -> dict:
    """Xóa nguồn qua CLI `nlm source delete -y` (VĨNH VIỄN — caller phải xác nhận người dùng trước)."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    rc, out, err = _run(["source", "delete", source_id, "-y"], timeout=timeout)
    return {"ok": rc == 0, "rc": rc, "via": "nlm-cli", "raw": (out or err).strip()[-200:]} if rc == 0 else _auth_fail(rc, out, err)


def source_sync(source_id: str, timeout: int = 240) -> dict:
    """Đồng bộ nguồn Drive (sync) qua CLI."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    rc, out, err = _run(["source", "sync", source_id], timeout=timeout)
    return {"ok": rc == 0, "rc": rc, "via": "nlm-cli", "raw": (out or err).strip()[-200:]} if rc == 0 else _auth_fail(rc, out, err)


def notebook_create(title: str, timeout: int = 180) -> dict:
    """P3 (v1.34.25): tạo notebook NLM — CHỈ dùng trong ngữ cảnh TẠO PROFILE (điều-kiện-kép nới CÓ KIỂM SOÁT,
    grilling 2026-07-10: --create-notebook --confirm yes); caller PHẢI journal + readback notebook_get."""
    return _run_json(["notebook", "create", title, "--json"], timeout=timeout)


def chat_configure(notebook_id: str, prompt: str, goal: str = "custom", timeout: int = 180) -> dict:
    """P3 (Q5): đặt System Prompt cho notebook (`nlm chat configure <nb> --goal custom --prompt ...`,
    prompt ≤10000 chars theo CLI). Fail → caller ghi manual_required, KHÔNG chặn promote."""
    return _run_json(["chat", "configure", notebook_id, "--goal", goal, "--prompt", prompt],
                     timeout=timeout)


def notebook_get(notebook_id: str, timeout: int = 120) -> dict:
    """Chi tiết notebook qua CLI `nlm notebook get -j` (thay MCP notebook_get). Trả {ok, source_count, title, raw}.
    Dùng lấy SỐ NGUỒN VẬT LÝ cho slot/preflight trước khi source_add."""
    r = _run_json(["notebook", "get", notebook_id, "-j"], timeout=timeout)
    if not r.get("ok"):
        return r
    d = r.get("data") or {}
    if isinstance(d, list):
        d = d[0] if d else {}
    srcs = d.get("sources") or d.get("source_ids") or []
    cnt = d.get("source_count")
    if cnt is None and isinstance(srcs, list):
        cnt = len(srcs)
    return {"ok": True, "source_count": cnt, "title": d.get("title") or d.get("name"), "via": "nlm-cli", "raw": d}


def cross_query(query: str, notebooks=None, tags=None, all_notebooks: bool = False, timeout: int = 360) -> dict:
    """Cross-notebook query qua CLI `nlm cross query` (thay MCP cross_notebook_query) — tra cứu XUYÊN SHARD VBQPPL.
    notebooks: list id/tên (—notebooks). KHÔNG có -j → trả text thô (verify nguyên văn sau, KHÔNG nhận RAG làm gốc)."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    if not (notebooks or tags or all_notebooks):
        return {"ok": False, "error": "cross_query cần notebooks|tags|all_notebooks"}
    args = ["cross", "query", query]
    if notebooks:
        args += ["-n", ",".join(notebooks)]
    if tags:
        args += ["-t", ",".join(tags)]
    if all_notebooks:
        args.append("-a")
    rc, out, err = _run(args, timeout=timeout)
    if rc != 0:
        return _auth_fail(rc, out, err)
    return {"ok": True, "answer_text": out.strip(), "via": "nlm-cli",
            "note": "RAG xuyên shard — định vị; verify nguyên văn từ cache/raw."}


def source_rename(source_id: str, title: str, notebook_id: str, timeout: int = 120) -> dict:
    """Đổi tên nguồn qua CLI `nlm source rename` (thay MCP source_rename). Đồng bộ tên NLM = tên Drive (NGUYÊN TẮC §0.7)."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    rc, out, err = _run(["source", "rename", source_id, title, "-n", notebook_id], timeout=timeout)
    return {"ok": rc == 0, "rc": rc, "via": "nlm-cli", "raw": (out or err).strip()[-200:]} if rc == 0 else _auth_fail(rc, out, err)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="nlm_cli", description="Adapter CLI nlm (fast NLM read)")
    ap.add_argument("notebook_id")
    ap.add_argument("--no-skip-freshness", action="store_true", help="bật lại freshness (chậm)")
    ap.add_argument("--no-drive", action="store_true")
    ap.add_argument("--profile", "-p")
    ap.add_argument("--quiet", "-q", action="store_true", help="chỉ in id")
    a = ap.parse_args(argv)
    r = source_list(a.notebook_id, skip_freshness=not a.no_skip_freshness,
                    drive=not a.no_drive, profile=a.profile)
    if a.quiet and r.get("ok"):
        for s in r["sources"]:
            print(s.get("id", ""))
    else:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
