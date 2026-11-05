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
import argparse, json, os, re, shutil, stat, subprocess, sys, tempfile, threading, time

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


# ───── r208b (báo cáo 25-07 mục 3.2): THỨ TỰ KHẮC PHỤC AUTH — MỘT nguồn sự thật ─────
# Ca thật 25-07: cookie NLM chết, MỌI thông báo trong skill chỉ hô `nlm login` — lệnh TƯƠNG TÁC,
# KHÔNG chạy được trong Cowork/headless. Đường đúng là `tl nlm-auth-load` (kéo cookie mã hoá từ
# Drive bằng webapp token, KHÔNG cần master key) mà KHÔNG thông báo nào gợi ý; người vận hành mò
# nhiều bước, thử `nlm-auth-pull` thì báo cụt lủn "thiếu TL_MASTER_KEY" không nói lấy ở đâu.
# THỨ TỰ BẤT BIẾN (rẻ→đắt, headless→tương tác); selftest drift-lock giữ mọi thông điệp đi qua đây:
_AUTH_FIX_ORDER = ("tl nlm-auth-load", "tl nlm-auth-pull", "nlm login")
# ── r213 (v1.35.49) ĐỢT 5: NGOẠI LỆ NGỮ CẢNH — chốt mâu thuẫn doctrine phát hiện ở lượt rà 26-07 ──
# Chuỗi trên xếp `nlm-auth-load` ở vị trí (1) trong khi RASOAT_HOSO_LOOP §4b + PHA 0 CẤM tự chạy nó.
# Cả hai đều ĐÚNG, chỉ khác NGỮ CẢNH: (1) là đường bootstrap Cowork/headless — ở đó máy CHƯA có jar
# nào, `nlm-auth-load` là đường duy nhất chạy được không cần browser. Trong LƯỢT RÀ thì ngược lại:
# jar đang sống (hoặc vừa chết), nạp bundle đè lên là quay vòng vô ích, và §4b bắt đi tiếp không-NLM.
# ⇒ KHÔNG đảo thứ tự (đảo là phá đường bootstrap — nghiệm thu r208b), KHÔNG nới §4b (nới là mở lại
# đúng vòng lặp r208c đã đóng). Thêm CÂU TRỪ, vì agent đọc thông báo lỗi thường không đọc doctrine.
# Chốt chặn hạ cấp `_nlm_auth_load_downgrade` (r208c) vẫn giữ: nó chặn ghi đè bằng bản CŨ hơn, nhưng
# KHÔNG chặn được bản mới-hơn-mà-cũng-chết ⇒ câu trừ này là lớp phòng thủ còn thiếu.
_AUTH_FIX_RASOAT_CARVE = ("⚠ ĐANG TRONG LƯỢT RÀ HỒ SƠ (RASOAT_HOSO_LOOP §4b): KHÔNG tự chạy (1)/(2) "
                          "— chuyển chế độ không-NLM và ĐI TIẾP; xác thực để người làm NGOÀI lượt rà.")
AUTH_FIX_HINT = (
    "Lỗi auth NLM — khắc phục THEO THỨ TỰ: (1) `tl nlm-auth-load` (kéo cookie mã hoá từ Drive bằng "
    "webapp token — CHẠY ĐƯỢC HEADLESS, không cần master key); (2) `tl nlm-auth-pull` (cần "
    "TL_MASTER_KEY — biến môi trường máy đã bootstrap, đặt bởi `tl-setup.ps1` hoặc "
    "`export TL_MASTER_KEY='<passphrase>'`); (3) `nlm login` (TƯƠNG TÁC — cần browser, KHÔNG chạy "
    "được trong Cowork/headless). " + _AUTH_FIX_RASOAT_CARVE)
AUTH_FIX_HINT_SHORT = ("🔴 AUTH hết hạn: `tl nlm-auth-load` → `tl nlm-auth-pull` (cần TL_MASTER_KEY) "
                       "→ `nlm login` (tương tác, chỉ khi có browser) · " + _AUTH_FIX_RASOAT_CARVE)


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


def _run_mot(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
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



# ── WP1099 (ADR-0064, spec cloud-setup-p3b-nlm-401-r11): jar chết giữa phiên cloud ⇒ TỰ NẠP CÓ ĐIỀU KIỆN (r208c bác tự nạp vì bundle có thể cũ/cũng chết) ⇒ chỉ nạp khi canary CON (thân `_canary_song` của nlm-auto-refresh.sh) trả 3,
# chỉ `tl nlm-auth-load` (không --force), 1 lần/tiến trình + dấu 600 s (best effort), chỉ chạy lại lệnh ĐỌC cho phép.
NAP_LAI_GAN_NHAT = None            # {trang_thai, ts} của lời gọi `_run` gần nhất đã tới bước "Giới hạn", hoặc None
_NAP_LAI_DA_NAP = False            # trần BẢO ĐẢM: 1 lần nạp mỗi tiến trình (khoá luồng giữ nó đúng cả khi đa luồng)
_NAP_LAI_KHOA = threading.Lock()
_NAP_LAI_HAN_CANARY, _NAP_LAI_HAN_NAP, _NAP_LAI_CUA_SO = 120, 60, 600     # canary: 3 lần × 30 s + 4,5 s chờ
_NAP_LAI_CHO_PHEP = frozenset({("source", "list"), ("source", "get"), ("source", "content"),
                               ("notebook", "get"), ("notebook", "list"), ("notebook", "query")})
_CANARY = ("import sys\nsys.path.insert(0, sys.argv[1])\ntry:\n    import tl\n    tg = tl._imp('tl_gws')\n    tg.bind(tl)\n"
           "    alive, _ = tg._nlm_auth_alive(tg._nlm_canary_notebook(None), require_notebook_body=True)\n"
           "except Exception:\n    alive = None\nsys.exit(0 if alive is True else 3 if alive is False else 2)\n")
_NAP_LAI_THU_MUC = os.path.dirname(os.path.abspath(__file__))

def _tep_dau() -> str:
    return os.path.join(os.path.expanduser("~"), ".notebooklm-mcp-cli", ".tra-luat-nap-lai.json")

# Tệp dấu — MỌI đường I/O (review PR #1197 F01/F05/F06/F07): không chặn, không theo symlink, chỉ tệp thường, ≤ 4 KiB; mọi fd đóng trong `finally`; lỗi ghi ⇒ False (không nạp), lỗi dọn bị nuốt; không đường nào ném ra khỏi `_run`.
def _doc_dau():
    fd = None
    try:
        fd = os.open(_tep_dau(), os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0))
        d = json.loads(os.read(fd, 4096)) if stat.S_ISREG(os.fstat(fd).st_mode) else None
        ts = d.get("ts") if isinstance(d, dict) else None
        return float(ts) if isinstance(ts, (int, float)) and not isinstance(ts, bool) else None
    except Exception:
        return None
    finally:
        _don(lambda: fd is not None and os.close(fd))

def _don(*viec) -> None:
    for v in viec:
        try:
            v()
        except OSError:
            pass

def _ghi_dau(ts: int, ket_qua: str) -> bool:
    p, tam, fd = _tep_dau(), None, None
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True); fd, tam = tempfile.mkstemp(dir=os.path.dirname(p), prefix=".nap-lai-")
        b = json.dumps({"ts": ts, "ket_qua": ket_qua}).encode("utf-8")
        if os.write(fd, b) != len(b): raise OSError("ghi NGẮN tệp dấu (review F08)")  # noqa: E701
        os.close(fd); fd = None
        os.chmod(tam, 0o600); os.replace(tam, p)
        return True
    except Exception:
        _don(lambda: fd is not None and os.close(fd), lambda: tam and os.unlink(tam))
        return False

def _con(argv: list, han: int):
    """(rc, đầu ra gộp) của tiến trình con, hoặc (lý do, "") khi quá hạn/OSError. Không chuyển tiếp đầu ra."""
    env = os.environ.copy()
    env["TL_NLM_NAP_LAI_TAT"] = "1"        # tiến trình con gọi lại nlm_cli thì cơ chế TẮT — không đệ quy
    try:
        p = subprocess.run(argv, cwd=os.path.dirname(_NAP_LAI_THU_MUC), env=env, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=han)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return "quá hạn", ""
    except OSError as e:
        return type(e).__name__, ""

def _canary():
    return _con([sys.executable, "-c", _CANARY, _NAP_LAI_THU_MUC], _NAP_LAI_HAN_CANARY)[0]

def _bao(trang_thai: str, chi_tiet: str) -> None:
    global NAP_LAI_GAN_NHAT
    NAP_LAI_GAN_NHAT = {"trang_thai": trang_thai, "ts": int(time.time())}
    print(f"nlm_nap_lai: {trang_thai} — {chi_tiet}", file=sys.stderr)

def _nap_lai(args: list, timeout: int, dau: tuple) -> tuple[int, str, str]:
    with _NAP_LAI_KHOA:                # luồng thứ hai chờ rồi thấy _NAP_LAI_DA_NAP ⇒ BỎ QUA (review PR #1197 F02)
        return _nap_lai_mot(args, timeout, dau)

def _nap_lai_mot(args: list, timeout: int, dau: tuple) -> tuple[int, str, str]:
    global _NAP_LAI_DA_NAP
    now = time.time()
    ts = _doc_dau()
    if _NAP_LAI_DA_NAP:
        _bao("BỎ QUA", "đã nạp trong tiến trình này"); return dau
    if ts is not None and ts <= now + 60 and now - ts < _NAP_LAI_CUA_SO:
        _bao("BỎ QUA", f"đã nạp lúc {int(ts)}"); return dau
    ma = _canary()
    if ma == 0:
        _bao("BỎ QUA", "canary sống, lỗi không do auth"); return dau
    if ma != 3:
        _bao("KHÔNG ĐO ĐƯỢC", f"canary {ma}"); return dau
    if not _ghi_dau(int(now), "dang_nap"):      # dấu là điều kiện TRƯỚC nạp (F01): không ghi được thì không nạp
        _bao("KHÔNG ĐO ĐƯỢC", "không ghi được tệp dấu"); return dau
    _NAP_LAI_DA_NAP = True
    rc, ra = _con([sys.executable, os.path.join(_NAP_LAI_THU_MUC, "tl.py"), "nlm-auth-load"], _NAP_LAI_HAN_NAP)
    if rc != 0:
        tt, ct = (("TỪ CHỐI HẠ CẤP", "bundle cũ hơn jar") if "TỪ CHỐI HẠ CẤP" in ra
                  else ("KHÔNG ĐO ĐƯỢC", f"nlm-auth-load rc={rc}"))
        _ghi_dau(int(now), tt); _bao(tt, ct); return dau
    ma = _canary()
    if ma != 0:
        tt, ct = (("BUNDLE CŨNG CHẾT", "laptop WP710 cần đăng nhập lại") if ma == 3
                  else ("KHÔNG ĐO ĐƯỢC", f"canary sau nạp {ma}"))
        _ghi_dau(int(now), tt); _bao(tt, ct); return dau
    _ghi_dau(int(now), "da_nap")
    if tuple(args[:2]) not in _NAP_LAI_CHO_PHEP:
        _bao("ĐÃ NẠP, KHÔNG THỬ LẠI (lệnh ghi)", " ".join(args[:2])); return dau
    lai = _run_mot(args, timeout)
    _bao("ĐÃ NẠP, THỬ LẠI ĐẠT" if lai[0] == 0 else f"ĐÃ NẠP, THỬ LẠI VẪN LỖI rc={lai[0]}", " ".join(args[:2]))
    return lai


def _run(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    global NAP_LAI_GAN_NHAT
    NAP_LAI_GAN_NHAT = None
    rc, out, err = kq = _run_mot(args, timeout)
    if (os.environ.get("CLAUDE_CODE_REMOTE") == "true" and os.environ.get("TL_NLM_NAP_LAI_TAT") != "1"
            and rc not in (0, 124, 127)
            and any(t in (err + out).lower() for t in ("auth", "401", "login", "unauthor", "credential"))):
        return _nap_lai(args, timeout, kq)
    return kq


def _kem(d: dict) -> dict:
    if NAP_LAI_GAN_NHAT is not None:
        d["nap_lai"] = NAP_LAI_GAN_NHAT
    return d


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
        return _kem({"ok": False, "rc": rc, "error": f"nlm source list rc={rc}: {(err or out)[:300]}",
                     "fallback": "mcp",
                     "auth_hint": AUTH_FIX_HINT if auth else None})   # r208b 3.2: chuỗi đúng đường, KHÔNG chỉ `nlm login`
    try:
        data = json.loads(out)
    except Exception as e:
        return _kem({"ok": False, "error": f"parse JSON lỗi: {e}", "raw": out[:300], "fallback": "mcp"})
    items = data if isinstance(data, list) else (data.get("sources") or data.get("items") or [])
    return _kem({"ok": True, "count": len(items), "sources": items, "via": "nlm-cli", "skip_freshness": skip_freshness})


def _run_json(args: list[str], timeout: int = 180) -> dict:
    """Chạy lệnh nlm có -j, trả {ok, data} hoặc {ok:False, error, fallback:'mcp'}."""
    if not nlm_available():
        return {"ok": False, "error": "nlm CLI không có trên PATH", "fallback": "mcp"}
    rc, out, err = _run(args, timeout=timeout)
    if rc != 0:
        low = (err + out).lower()
        auth = any(t in low for t in ("auth", "401", "login", "unauthor", "credential"))
        return _kem({"ok": False, "rc": rc, "error": f"nlm rc={rc}: {(err or out)[:300]}", "fallback": "mcp",
                     "auth_hint": AUTH_FIX_HINT if auth else None})   # r208b 3.2
    try:
        return _kem({"ok": True, "data": json.loads(out), "via": "nlm-cli"})
    except Exception:
        return _kem({"ok": True, "text": out, "via": "nlm-cli"})   # vài lệnh trả text thuần


def source_get(source_id: str, timeout: int = 120) -> dict:
    """Chi tiết 1 source (title/source_type/url/char_count)."""
    return _run_json(["source", "get", source_id, "-j"], timeout=timeout)


def source_content(source_id: str, timeout: int = 180) -> dict:
    """Toàn văn raw của source (thay MCP source_get_content; CLI nhanh + không qua server)."""
    return _run_json(["source", "content", source_id, "-j"], timeout=timeout)


def _query_args(notebook_id: str, query: str, source_ids=None) -> list:
    """PURE (r214): dựng argv cho `nlm notebook query` (tách để selftest, không shell).

    ★BUG r214 (đo 26-07, sổ lỗi NLM_QUERY_LOAI_NGUON_KHONG_BAO): bản cũ phát `-s <id>` LẶP LẠI
    cho từng nguồn, nhưng `nlm notebook query --source-ids/-s` là MỘT chuỗi «Comma-separated source
    IDs» (không phải option lặp) ⇒ giá trị SAU đè giá trị TRƯỚC, chỉ nguồn CUỐI sống sót. Đo thật:
    truyền 2 --source-id (212 rồi 233) → `sources_used` chỉ còn 233 = cái CUỐI, rc vẫn 0, không warn
    ⇒ sinh kết luận ÂM TÍNH GIẢ. Nay gộp một `-s` duy nhất bằng dấu phẩy — ĐÚNG khuôn `cross_query`
    (`-n ",".join(...)`) vốn đã dùng trong CHÍNH file này."""
    args = ["notebook", "query", notebook_id, query, "-j"]
    _sids = [str(s).strip() for s in (source_ids or []) if s is not None and str(s).strip()]
    if _sids:
        args += ["-s", ",".join(_sids)]
    return args


def notebook_query(notebook_id: str, query: str, source_ids=None, timeout: int = 240) -> dict:
    """RAG query trên notebook (thay MCP notebook_query). source_ids: scope (CLI nhận CSV — xem _query_args)."""
    return _run_json(_query_args(notebook_id, query, source_ids), timeout=timeout)


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
    return _kem({"ok": False, "rc": rc, "error": f"nlm rc={rc}: {(err or out)[:300]}", "fallback": "mcp",
                 "auth_hint": AUTH_FIX_HINT if auth else None})   # r208b 3.2


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
            return _kem({"ok": True, "source_id": m.group(1), "ready": False, "settle_timeout": True,
                         "via": "nlm-cli", "raw": (out or "").strip()[-200:],
                         "note": f"thôi chờ settle sau {timeout}s (nguồn đang index) — nlm-reconcile cuối lô xác minh"})
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
    return _kem({"ok": True, "source_count": cnt, "title": d.get("title") or d.get("name"), "via": "nlm-cli", "raw": d})


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
