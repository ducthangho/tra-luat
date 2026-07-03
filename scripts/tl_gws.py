#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tl_gws.py — KHỐI LỆNH gws/transport/bootstrap/secrets tách khỏi tl.py để tl.py < ngưỡng kích thước mount
skill (~343KB; tl.py từng bị cắt cụt khi >343KB). Hàm dùng TÊN TRẦN của tl (_gas/_imp/load_creds/hằng GWS_*…)
— nạp vào globals() qua bind(tl_module) gọi từ tl.build_parser. KHÔNG import tl ở top (tránh re-exec/circular).
"""
from __future__ import annotations

# stdlib TƯỜNG MINH (tránh phụ thuộc bind() chèn — vd khi dispatch trực tiếp KHÔNG qua build_parser thì bind chưa
# chạy → 'tempfile/tarfile/...' bare sẽ NameError). bind() chỉ còn chèn tên tl-RIÊNG (_gas/_imp/hằng GWS_*…).
import os
import sys
import re
import json
import stat
import base64
import hashlib
import tarfile
import tempfile
import subprocess  # noqa: F401  (một số hàm import lại cục bộ; giữ ở top cho path bypass-bind)

_BOUND = False
def bind(tl_module):
    """Nạp namespace tl vào module này (1 lần) để các hàm dưới dùng tên trần."""
    global _BOUND
    if _BOUND:
        return
    g = globals()
    for k, v in vars(tl_module).items():
        if not k.startswith("__") and k not in g:
            g[k] = v
    _BOUND = True


_TOKEN_CACHE: dict = {}        # sha256(refresh_token) → (access_token, expiry_epoch). Bỏ 1-roundtrip đổi token/lần tải.
# v1.33.0 (log rà 69 A3): invalid_grant là TERMINAL trong 1 process — cred không tự sống lại giữa chừng.
# Cờ cho caller đọc-hàng-loạt (corpus-audit ×N, _read_doc_text, transport download) SKIP direct-media ngay từ
# doc thứ 2 thay vì retry-fail ~2-20s/doc; gws-ping/doctor canary vẫn gọi thẳng _access_token nên không bị che.
_CRED_AUTH_DEAD = False


def _access_token(cred):
    """Đổi gws cred (authorized_user refresh_token) → OAuth access_token, CACHE trong process tới gần hết hạn.
    Nhờ cache, tải nhiều file (vd loạt config .js/.json) chỉ tốn 1 lần đổi token cho cả loạt."""
    global _CRED_AUTH_DEAD
    import urllib.request as _u, urllib.parse as _up, json as _j, time as _t, hashlib as _h
    c = cred if isinstance(cred, dict) else _j.loads(cred)
    key = _h.sha256(c["refresh_token"].encode()).hexdigest()
    now = _t.time()
    hit = _TOKEN_CACHE.get(key)
    if hit and hit[1] - 60 > now:                    # còn hạn (trừ 60s an toàn)
        return hit[0]
    data = _up.urlencode({"client_id": c["client_id"], "client_secret": c["client_secret"],
                          "refresh_token": c["refresh_token"], "grant_type": "refresh_token"}).encode()
    # v1.31.2 (chẩn đoán LIVE 2026-07-03): lỗi ở đây từng nổi lên chỉ là 'HTTPError 400: Bad Request' ở MỌI đường
    # direct-media → không ai biết là CRED HẾT HẠN (invalid_grant). Đọc body + raise thông điệp tự-chẩn-đoán.
    # Kiến trúc: credentials.json (FILE — nguồn của direct-media) TÁCH RỜI token keyring của gws CLI binary
    # → gws CLI vẫn chạy tốt trong khi file cred hết hạn. Làm mới: `gws auth login` rồi `tl secrets-set --gws`
    # (cập nhật bundle để Cowork cũng nhận cred mới).
    import urllib.error as _ue
    try:
        with _u.urlopen(_u.Request("https://oauth2.googleapis.com/token", data=data), timeout=30) as r:
            j = _j.loads(r.read())
    except _ue.HTTPError as e:
        _body = ""
        try:
            _body = e.read().decode("utf-8", errors="replace")[:200]
        except Exception:
            pass
        if "invalid_grant" in _body:
            _CRED_AUTH_DEAD = True   # v1.33.0: circuit-breaker — caller hàng loạt skip direct-media từ đây
            # v1.32.1 (log rà 119 sửa lại khẳng định SAI 'fallback GAS vẫn đúng'): fallback GAS chỉ cứu DOWNLOAD
            # file (action download b64 — DriveApp); op ĐỌC TEXT (exporttext) CHẾT THEO vì webapp thiếu OAuth scope
            # script.external_request → extract/corpus-audit/header-verify không còn đường Drive nào.
            raise RuntimeError("GWS_CRED_EXPIRED: refresh_token trong ~/.config/gws/credentials.json HẾT HẠN/bị thu hồi "
                               "(invalid_grant) → chạy `gws auth login` trên máy user rồi `tl secrets-set --gws` "
                               "(làm mới bundle cho Cowork). ⚠ Fallback GAS chỉ cứu DOWNLOAD file; op ĐỌC TEXT "
                               "(exporttext) chết theo (webapp thiếu scope script.external_request) — tạm rà verbatim "
                               "qua `tl nlm-content <source_id> --dieu N` (corpus-audit/backfill-title-vn tự thử đường NLM).") from None
        raise RuntimeError(f"GWS_TOKEN_REFRESH_HTTP_{e.code}: {_body or e.reason}") from None
    _TOKEN_CACHE[key] = (j["access_token"], now + float(j.get("expires_in", 3600)))
    return j["access_token"]


def _gws_cred_alive(timeout: float = 20.0) -> tuple[bool, str]:
    """P1 (v1.32.1 — log rà 119: doctor/gws-ping FALSE-GREEN khi refresh_token đã REVOKE): CANARY đổi token THẬT
    từ ~/.config/gws/credentials.json (nguồn direct-media — TÁCH RỜI keyring gws CLI; auth_method=oauth2 KHÔNG
    chứng minh cred sống). 1 POST oauth2 (~200ms); token cache process nên gọi lặp = rẻ. Trả (alive, msg)."""
    cred = _read_gws_cred()
    if not cred:
        return False, "NO_CRED: thiếu ~/.config/gws/credentials.json (direct-media tắt)"
    try:
        _access_token(cred)
        return True, "token OK"
    except Exception as e:  # noqa: BLE001
        return False, str(e)[:240]


def _drive_media_download(file_id, dest, cred, export_mime: str | None = None, timeout: float = 300.0):
    """Tải file Drive bằng DIRECT MEDIA qua HTTP — RAW bytes STREAMING thẳng xuống đĩa: KHÔNG base64
    (không phình 33%), KHÔNG cap 9MB webapp, không nạp vào RAM/context, byte-exact MỌI loại (kể cả text/JSON
    mà gws CLI làm méo). Blob: `alt=media`. Google-native (Doc/Sheet): truyền export_mime (vd text/plain).
    Token cache (_access_token) → tải loạt file chỉ 1 lần đổi token. Trả {ok,path,bytes} hoặc raise."""
    import urllib.request as _u, urllib.parse as _up, shutil as _sh, os as _os
    tok = _access_token(cred)
    if export_mime:
        url = ("https://www.googleapis.com/drive/v3/files/" + _up.quote(file_id)
               + "/export?mimeType=" + _up.quote(export_mime))
    else:
        url = ("https://www.googleapis.com/drive/v3/files/" + _up.quote(file_id)
               + "?alt=media&supportsAllDrives=true")
    req = _u.Request(url, headers={"Authorization": "Bearer " + tok})
    with _u.urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
        _sh.copyfileobj(r, f, length=1 << 20)        # streaming 1MB/chunk — không vào RAM/context
    return {"ok": True, "path": dest, "bytes": _os.path.getsize(dest)}


def _public_curl_download(file_id, dest, timeout: float = 300.0):
    """Tải file PUBLIC (anyone-with-link) qua drive.usercontent → RAW bytes streaming xuống đĩa. NHANH NHẤT cho file
    public (KHÔNG token, KHÔNG b64, allowlist Cowork mở). Raise nếu nhận trang login (file CHƯA public) / lỗi mạng."""
    import urllib.request as _u, shutil as _sh, os as _os
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
    with _u.urlopen(url, timeout=timeout) as r, open(dest, "wb") as f:
        first = r.read(1 << 16)
        low = first[:512].lstrip().lower()
        if low.startswith(b"<!doctype html") or b"<html" in low[:64] or b"accounts.google.com" in first[:2048]:
            raise RuntimeError("Drive trả trang login — file CHƯA public (anyone-with-link)")
        f.write(first)
        _sh.copyfileobj(r, f, length=1 << 20)
    return {"ok": True, "path": dest, "bytes": _os.path.getsize(dest)}


def _public_curl_bytes(file_id, timeout: float = 120.0):
    """Tải file PUBLIC qua drive.usercontent → RAW bytes trong RAM (cho file NHỎ: cred .enc, config). None nếu
    trang login (CHƯA public) / lỗi. Cred .enc nay public → curl raw rồi giải mã bằng token (KHÔNG cần master key)."""
    import urllib.request as _u
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
    try:
        with _u.urlopen(url, timeout=timeout) as r:
            data = r.read()
    except Exception:  # noqa: BLE001
        return None
    low = data[:512].lstrip().lower()
    if low.startswith(b"<!doctype html") or b"<html" in low[:64] or b"accounts.google.com" in data[:2048]:
        return None
    return data


def _fast_drive_fetch(file_id, dest, *, cred=None, label: str = "", env=None, verbose: bool = True):
    """Tải file Drive bằng đường NHANH NHẤT, ĐO THỜI GIAN, ưu tiên theo tốc độ (file bootstrap nay PUBLIC):
      (1) public-curl drive.usercontent — nhanh nhất cho file PUBLIC (không token/b64)
      (2) direct-media alt=media         — nếu có gws cred (raw, không b64)
      (3) GAS webapp `download` (b64)    — fallback cuối (chậm + cap)
    In '[fetch] <label>: <src> <bytes>B <secs>s ✓' để THEO DÕI HIỆU NĂNG. Trả (src, secs). Raise nếu cả 3 fail."""
    import time as _t, os as _os
    errs = []
    t0 = _t.time()
    try:
        r = _public_curl_download(file_id, dest)
        secs = _t.time() - t0
        if verbose:
            print(f"[fetch] {label}: public-curl {r['bytes']}B {secs:.1f}s ✓")
        return "public-curl", secs
    except Exception as e:  # noqa: BLE001
        errs.append(f"public-curl: {type(e).__name__}: {e}")
    cred = cred if cred is not None else _read_gws_cred()
    if cred:
        t0 = _t.time()
        try:
            r = _drive_media_download(file_id, dest, cred)
            secs = _t.time() - t0
            if verbose:
                print(f"[fetch] {label}: direct-media {r['bytes']}B {secs:.1f}s ✓ (public-curl lỗi: {errs[-1][:50]})")
            return "direct-media", secs
        except Exception as e:  # noqa: BLE001
            errs.append(f"direct-media: {type(e).__name__}: {e}")
    t0 = _t.time()
    rr = _imp("transport").drive_op("download", env=env, file_id=file_id, dest=dest)
    if isinstance(rr, dict) and rr.get("ok"):
        secs = _t.time() - t0
        if verbose:
            print(f"[fetch] {label}: GAS-b64 {_os.path.getsize(dest)}B {secs:.1f}s ✓ (đường nhanh đều lỗi)")
        return "GAS-b64", secs
    errs.append(f"GAS: {rr}")
    raise RuntimeError(f"[fetch] {label}: TẤT CẢ đường tải lỗi — " + " | ".join(errs))


def _read_gws_cred():
    """Đọc gws cred (authorized_user JSON) từ ~/.config/gws/credentials.json nếu có — cho direct-media."""
    import os as _os, json as _j
    p = _os.path.join(_os.environ.get("GOOGLE_WORKSPACE_CLI_CONFIG_DIR") or _os.path.expanduser("~/.config/gws"),
                      "credentials.json")
    if _os.path.exists(p):
        try:
            d = _j.loads(open(p, encoding="utf-8").read())
            if d.get("refresh_token") and d.get("client_id"):
                return d
        except Exception:
            pass
    return None


def _strip_keyring_noise(s: str) -> str:
    """A6: bỏ dòng 'Using keyring backend: …' (lib keyring/gws in ra) khỏi output để log không nhiễu."""
    if not s or "keyring" not in s.lower():
        return s
    return "\n".join(ln for ln in s.splitlines() if "using keyring backend" not in ln.lower())


def _gws_run(args: list[str], timeout: float = 20.0):
    """GĐ0: chạy `gws <args>` an toàn → (rc, stdout, stderr). gws thiếu PATH → rc=127.
    KHÔNG raise; boot-check tự diễn giải. KHÔNG in/echo credential (chỉ gọi --version/auth status)."""
    exe = _imp("gws_bridge").gws_exe()       # PATH + ~/.local/bin (Cowork khỏi export PATH mỗi lệnh)
    if not exe:
        return 127, "", "gws not found (PATH / ~/.local/bin)"
    try:
        p = subprocess.run([exe, *args], capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
        # A6: lọc dòng nhiễu 'Using keyring backend: …' (gws/keyring in ra stderr+stdout) → log sạch, dễ thấy lỗi thật.
        return p.returncode, _strip_keyring_noise(p.stdout or ""), _strip_keyring_noise(p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout sau {timeout}s"
    except Exception as e:  # noqa: BLE001
        return 1, "", f"{type(e).__name__}: {e}"


# v1.29.4 (AUDIT #9): CHUẨN HOÁ timeout gws — FAST=probe/boot-check, STD=API đọc thường (sheets/metadata),
# LARGE=download media/file lớn. Trước đây rải 20/45/60/300 tùy chỗ → jitter mạng làm chỗ 45 fail chỗ 60 sống.
GWS_TIMEOUT_FAST = 20.0
GWS_TIMEOUT_STD = 60.0
GWS_TIMEOUT_LARGE = 300.0


# ───────────────── R1: ĐỌC Sheet registry LIVE qua gws (nhóm-D READ gws-primary + GAS fallback) ─────────────────
# gws CLI NAY có Sheets API (values.get) → đọc registry LIVE (bỏ cache đọc GAS ~600s), nhanh ~2× (đo 2026-07-02).
# CHỈ ĐỌC. GHI registry vẫn GAS ĐỘC QUYỀN (LockService khóa 30s + read-modify-write swap nguyên tử +
# business-logic Apps Script) — xem tra-luat-DESIGN-nhomD-gws-primary.md.
def _parse_sheet_values_to_rows(values, cols=None):
    """PURE (test offline): 2D `values` Sheets API (hàng 0 = HEADER) → list[dict] PARITY GAS rowsToObjs_.
    ⚠ PARITY QUAN TRỌNG: GAS rowsToObjs_ gán khóa THEO VỊ TRÍ cột dùng `REG_COLS_[c]` (KHÔNG đọc tên header
    thực) → nếu ai đổi thứ tự cột trong Sheet, GAS vẫn map theo REG_COLS_. Để CÙNG kết quả với manifest (do GAS
    sinh), khi có `cols` (=REGISTRY_SCHEMA_COLS) ta cũng gán khóa THEO VỊ TRÍ `cols[i]` (KHÔNG theo header names —
    tránh lệch khi header có sai khác cỡ chữ/khoảng trắng). Không `cols` → fallback theo header names.
      • mỗi ô ép str; ô THIẾU/None → '' (Sheets bỏ ô ĐUÔI rỗng → phải bù cho đủ);
      • đảm bảo MỌI khóa trong `cols` có mặt (setdefault '');
      • BỎ dòng drive_id rỗng (GAS: `if (o.drive_id) out.push(o)`).
    KHÔNG chuẩn hoá sohieu ở đây — giữ RAW như sheet (giống manifest lưu raw; caller tự norm_sohieu khi khớp)."""
    if not values:
        return []
    header = [str(h).strip() for h in (values[0] or [])]
    keys = list(cols) if cols else header       # GAS-parity: khóa THEO VỊ TRÍ theo schema; else header names
    out = []
    for row in values[1:]:
        o = {}
        for i, key in enumerate(keys):
            o[key] = str(row[i]) if (i < len(row) and row[i] is not None) else ""
        for c in (cols or []):
            o.setdefault(c, "")
        if o.get("drive_id"):
            out.append(o)
    return out


def _gws_sheets_values_get(spreadsheet_id: str, rng: str, timeout: float = GWS_TIMEOUT_STD):
    """R1: đọc DẢI ô Sheet qua gws Sheets API (LIVE). Trả list[list] `values` (có thể rỗng []),
    hoặc None nếu gws lỗi/không sẵn/registryDocId không phải Sheet (→ caller FALLBACK GAS). KHÔNG raise."""
    if not spreadsheet_id or not rng:
        return None
    import json as _j
    params = _j.dumps({"spreadsheetId": spreadsheet_id, "range": rng})
    rc, out, _err = _gws_run(["sheets", "spreadsheets", "values", "get", "--params", params], timeout=timeout)
    if rc != 0 or not out:
        return None
    try:
        d = _j.loads(out[out.index("{"):])   # bỏ preamble không-JSON nếu lọt (vd dòng keyring còn sót)
    except Exception:
        return None
    if not isinstance(d, dict) or "error" in d:   # {"error": {...}} = 404/permission → fallback GAS
        return None
    return d.get("values") or []


def _gws_read_registry_rows(spreadsheet_id: str, cols=None, tab: str = "files", timeout: float = GWS_TIMEOUT_STD):
    """R1: đọc TOÀN BỘ tab registry `files` LIVE qua gws → list[dict] parity GAS regReadAll_.
    Trả None nếu gws lỗi/không sẵn (→ FALLBACK GAS). CHỈ ĐỌC — GHI vẫn GAS."""
    vals = _gws_sheets_values_get(spreadsheet_id, f"{tab}!A:AA", timeout=timeout)
    if vals is None:
        return None
    return _parse_sheet_values_to_rows(vals, cols)


def cmd_gws_ping(a) -> int:
    """GĐ0 — cổng boot transport gws (đối xứng `tl ping` của webapp), env-aware.
    Chat: SKIP (không shell/binary → Drive MCP làm transport); Code/Cowork: kiểm gws trên PATH,
    version == GWS_PINNED_VERSION, và auth đã sẵn (gws auth status → auth_method != none).
    rc: 0 = sẵn sàng (hoặc Chat-skip); 3 = gws lệch pin/chưa auth; 4 = gws thiếu/không chạy được."""
    # Dùng resolver SHELL-AWARE của transport: transport/gws chỉ chạy trong shell ⇒ heuristic KHÔNG
    # trả 'chat' (Cowork không set COWORK vẫn ra 'cowork', không SKIP nhầm). Chat chỉ khi --env/TL_RUNTIME_ENV.
    try:
        env = _imp("transport").runtime_env(getattr(a, "env", None))
    except Exception:
        env = _runtime_env(getattr(a, "env", None))
    want_json = bool(getattr(a, "json", False))
    if env == "chat":
        info = {"ok": True, "runtime_env": "chat", "skip": True, "transport": "drive_mcp",
                "note": "Chat KHÔNG có gws shell → transport Drive qua Drive MCP; gws-ping SKIP (đúng thiết kế)."}
        print(json.dumps(info, ensure_ascii=False, indent=2) if want_json
              else "[gws-ping] env=chat → SKIP (transport = Drive MCP, không cần gws). OK.")
        return 0

    info = {"ok": False, "runtime_env": env, "pinned_version": GWS_PINNED_VERSION,
            "gws_found": False, "version": None, "version_match": False,
            "authed": False, "auth_method": None, "issues": []}

    rc, out, err = _gws_run(["--version"], timeout=15.0)
    if rc == 127:
        info["issues"].append("gws THIẾU trên PATH → cài: npm i -g @googleworkspace/cli@" + GWS_PINNED_VERSION)
        _gws_ping_emit(info, want_json); return 4
    if rc != 0:
        info["issues"].append(f"`gws --version` rc={rc}: {(err or out).strip()[:200]}")
        _gws_ping_emit(info, want_json); return 4
    info["gws_found"] = True
    m = re.search(r"(\d+\.\d+\.\d+)", out)
    info["version"] = m.group(1) if m else (out.strip().splitlines() or [""])[0]
    info["version_match"] = (info["version"] == GWS_PINNED_VERSION)
    if not info["version_match"]:
        info["issues"].append(f"version gws={info['version']} ≠ pin {GWS_PINNED_VERSION} "
                              f"(gws pre-v1.0 hay breaking) → ghim lại: npm i -g @googleworkspace/cli@{GWS_PINNED_VERSION}")

    rc2, out2, err2 = _gws_run(["auth", "status"], timeout=20.0)
    if rc2 == 0 and out2.strip():
        try:
            st = json.loads(out2)
            am = st.get("auth_method")
            info["auth_method"] = am
            info["authed"] = bool(am) and am != "none"
            info["credential_source"] = st.get("credential_source")
        except Exception:
            info["issues"].append("không parse được `gws auth status` JSON")
    else:
        info["issues"].append(f"`gws auth status` rc={rc2}: {(err2 or out2).strip()[:160]}")
    if not info["authed"]:
        info["issues"].append("gws CHƯA auth → Code: `gws auth login`; Cowork: export cred (RUNBOOK §A0) "
                              "+ `export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=<path>`")
    # P1 (v1.32.1 — log rà 119 FALSE-GREEN): auth_method=oauth2 chỉ nói CÓ cấu hình, KHÔNG nói cred còn SỐNG
    # (ca invalid_grant: token revoke mà ping vẫn ✓). CANARY đổi token thật; chết → ĐỎ + hướng refresh.
    _alive, _amsg = _gws_cred_alive()
    info["cred_alive"] = _alive
    if not _alive:
        info["issues"].append(f"CRED CHẾT (canary token): {_amsg} → `gws auth login` rồi `tl secrets-set --gws` "
                              "(Cowork nhận cred mới qua bundle). ⚠ đọc Drive (extract/corpus-audit) CHẾT tới khi refresh "
                              "— tạm rà verbatim qua `tl nlm-content <source_id> --dieu N`.")

    info["ok"] = info["gws_found"] and info["version_match"] and info["authed"] and _alive
    _gws_ping_emit(info, want_json)
    return 0 if info["ok"] else 3


def _gws_ping_emit(info: dict, want_json: bool) -> None:
    if want_json:
        print(json.dumps(info, ensure_ascii=False, indent=2)); return
    mark = "✓" if info["ok"] else "✗"
    print(f"[gws-ping] {mark} env={info['runtime_env']} gws={info.get('version') or '—'} "
          f"(pin {info['pinned_version']}) auth={info.get('auth_method') or 'none'}")
    for it in info["issues"]:
        print(f"  - {it}", file=sys.stderr)
    if not info.get("ok") and info.get("runtime_env") in ("code", "cowork"):
        if info.get("cred_alive") is False:
            # v1.32.1: cred CHẾT ≠ 'chưa nạp' — op ĐỌC Drive (extract/corpus-audit/header-verify) CHẾT
            # (fallback GAS exporttext thiếu scope); chỉ download-manifest/upload còn đường khác.
            print("  ⚠ CRED CHẾT: op ĐỌC Drive sẽ hỏng tới khi `gws auth login` + `tl secrets-set --gws`; "
                  "tạm rà verbatim qua `tl nlm-content` / backfill-title-vn --from-tukhoa (offline).")
        else:
            print("  ℹ gws chưa sẵn → op A/B/C tự [FALLBACK→GAS] (chỉ `upload` cần gws); skill VẪN DÙNG ĐƯỢC.")


def _master_key() -> str:
    return os.environ.get("TL_MASTER_KEY") or ""


def _gws_export_cred() -> bytes | None:
    """Export gws cred (in-process). None nếu gws thiếu/chưa auth."""
    import subprocess as _sp, shutil as _sh
    exe = _imp("gws_bridge").gws_exe()
    if not exe:
        return None
    p = _sp.run([exe, "auth", "export", "--unmasked"], capture_output=True, text=True, timeout=60)
    out = (p.stdout or "").strip()
    return out.encode("utf-8") if (p.returncode == 0 and out) else None


def _secrets_upload(blob: bytes, folder: str, file_id: str | None):
    """Upload bundle: nếu có file_id → update CONTENT tại chỗ (fileId giữ nguyên); else tạo mới."""
    import tempfile
    g = _imp("gws_bridge")
    with tempfile.TemporaryDirectory() as d:
        fp = os.path.join(d, "tl_secrets.enc")
        with open(fp, "wb") as f:
            f.write(blob)
        if file_id:
            r = g.update_content(file_id, fp, mime="application/octet-stream")
            return file_id, r
        r = g.upload("tl_secrets.enc", fp, parents=[folder], mime="application/octet-stream")
        return (r.get("file") or {}).get("id"), r


def _secrets_fetch(a, fid: str):
    """Lấy bytes tl_secrets.enc TỪ DRIVE khi thiếu file local: --secrets-file → webapp GAS (nếu có token) →
    direct-media (nếu có gws cred) → None (cần agent tải MCP). fid mặc định = SECRETS_FILEID (đã bake)."""
    sf = getattr(a, "secrets_file", None)
    if sf and os.path.exists(sf):
        with open(sf, "rb") as f:
            return f.read(), "file"
    if not fid:
        return None, None
    if os.environ.get("TL_TOKEN"):                   # webapp GAS download (id công khai; bundle vẫn mã hoá)
        try:
            r = _gas().get("download", fileId=fid)
            if isinstance(r, dict) and r.get("ok") and r.get("b64"):
                return base64.b64decode(r["b64"]), "webapp"
        except Exception:  # noqa: BLE001
            pass
    try:                                             # direct-media (Code có gws cred; Cowork sau khi có cred)
        with tempfile.TemporaryDirectory() as d:
            dst = os.path.join(d, "s.enc")
            r = _imp("transport").drive_op("download", env=getattr(a, "env", None), file_id=fid, dest=dst)
            if isinstance(r, dict) and r.get("ok"):
                return open(dst, "rb").read(), "direct-media"
    except Exception:  # noqa: BLE001
        pass
    return None, None


_NLM_AUTH_RELS = ("auth.json", "profiles/default/cookies.json", "profiles/default/metadata.json")


def _nlm_auth_files():
    """Thu file auth nlm (profile 'default') từ ~/.notebooklm-mcp-cli → {relpath: text}. SECRET (cookies Google).
    Cho `secrets-stage` gói vào bundle .enc → Cowork ghi lại → nlm chạy headless không cần `nlm login`."""
    base = os.path.expanduser("~/.notebooklm-mcp-cli")
    out = {}
    for rel in _NLM_AUTH_RELS:
        p = os.path.join(base, *rel.split("/"))
        if os.path.exists(p):
            try:
                out[rel] = open(p, encoding="utf-8").read()
            except Exception:
                pass
    return out


def _refresh_nlm_auth():
    """[CODE] Best-effort ÉP nlm refresh cookies TRƯỚC khi gói: `nlm login --check` kích hoạt nlm đọc lại/ tái sinh
    cookie từ browser profile (GHI ĐÈ auth.json) → bundle bắt được cookie MỚI NHẤT. Trả True nếu auth còn hạn."""
    import shutil as _sh, subprocess as _sp
    nx = _sh.which("nlm") or os.path.expanduser("~/.local/bin/nlm")
    if not (os.path.exists(nx) or _sh.which("nlm")):
        return False
    try:
        p = _sp.run([nx, "login", "--check"], capture_output=True, text=True, timeout=120)
        return p.returncode == 0 and "valid" in (p.stdout + p.stderr).lower()
    except Exception:  # noqa: BLE001
        return False


def _nlm_auth_age_days(nlm_auth):
    """Tuổi cookie (ngày) từ extracted_at trong auth.json — để cảnh báo cookie cũ sắp hết hạn (~2–4 tuần)."""
    import time as _t
    try:
        ts = json.loads(nlm_auth.get("auth.json", "{}")).get("extracted_at")
        return (_t.time() - float(ts)) / 86400.0 if ts else None
    except Exception:
        return None


def cmd_secrets_stage(a) -> int:
    """[CODE] Gom {webappUrl, token GAS, gws_cred, nlm_auth} → MÃ HOÁ (TL_MASTER_KEY) → upload Drive (tl_secrets.enc).
    In fileId để baked vào SECRETS_FILEID. Cred/token chỉ ở RAM, KHÔNG plaintext ra Drive/zip."""
    master = _master_key()
    if not master:
        print("[secrets-stage] ✗ thiếu TL_MASTER_KEY — đặt: export TL_MASTER_KEY='<passphrase mạnh>'", file=sys.stderr)
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    # Gói FULL config (webappUrl, token, rootFolderId, registryDocId, manifestId, categories, profiles…)
    # để Cowork mới có đủ — KHÔNG chỉ token (tránh clobber mất key khi bootstrap ghi config).
    cfp = getattr(a, "config", None) or os.path.expanduser("~/.tra_luat_config.json")
    bundle = {}
    if os.path.exists(cfp):
        try:
            bundle = json.load(open(cfp, encoding="utf-8"))
        except Exception:
            bundle = {}
    bundle.setdefault("webappUrl", os.environ.get("TL_WEBAPP", ""))
    bundle.setdefault("token", os.environ.get("TL_TOKEN", ""))
    if not bundle.get("token"):
        print("[secrets-stage] ✗ thiếu webapp token (TL_TOKEN/config) để gói.", file=sys.stderr)
        return 2
    if not getattr(a, "no_gws", False):
        cred = _gws_export_cred()
        if cred:
            bundle["gws_cred"] = cred.decode("utf-8")
        else:
            print("[secrets-stage] ⚠ bỏ qua gws_cred (gws chưa cài/auth ở máy này).", file=sys.stderr)
    if not getattr(a, "no_nlm", False):
        _refresh_nlm_auth()                           # ép nlm tái sinh cookie từ browser profile → gói bản mới nhất
        nlm = _nlm_auth_files()                        # cookies nlm (profile default) — cho Cowork dùng headless
        if nlm:
            bundle["nlm_auth"] = nlm
            age = _nlm_auth_age_days(nlm)
            agestr = f", cookie ~{age:.0f} ngày tuổi" if age is not None else ""
            print(f"[secrets-stage] ✓ gói nlm_auth ({len(nlm)} file{agestr}) — Cowork khỏi `nlm login`.")
        else:
            print("[secrets-stage] ⚠ bỏ qua nlm_auth (chưa `nlm login` ở máy này).", file=sys.stderr)
    blob = _imp("gws_cred_store").encrypt(json.dumps(bundle, ensure_ascii=False).encode("utf-8"), master)
    fid, _ = _secrets_upload(blob, getattr(a, "folder", None) or HOPNAP_FOLDER_ID,
                             getattr(a, "secrets_id", None) or (SECRETS_FILEID or None))
    keys = [k for k in ("webappUrl", "token", "gws_cred", "nlm_auth") if bundle.get(k)]
    print(f"[secrets-stage] ✓ bundle MÃ HOÁ ({len(blob)}B, gồm: {keys}) → Drive id={fid}")
    print(f"  → baked: đặt SECRETS_FILEID = \"{fid}\" trong tl.py (hoặc dùng `bootstrap --secrets-id {fid}`).")
    return 0


def cmd_secrets_set(a) -> int:
    """[CODE] Xoay vòng/đổi secret trong bundle: --gas-token <t> / --webapp <url> / --gws (re-export).
    Tải bundle hiện có → giải mã → cập nhật trường → mã hoá lại → ghi đè TẠI CHỖ (fileId giữ nguyên)."""
    master = _master_key()
    if not master:
        print("[secrets-set] ✗ thiếu TL_MASTER_KEY.", file=sys.stderr)
        return 2
    fid = getattr(a, "secrets_id", None) or os.environ.get("TL_SECRETS_FILEID") or SECRETS_FILEID
    if not fid:
        print("[secrets-set] ✗ chưa có SECRETS_FILEID/TL_SECRETS_FILEID — chạy `secrets-stage` trước.", file=sys.stderr)
        return 2
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    store = _imp("gws_cred_store")
    blob, _src = _secrets_fetch(a, fid)
    if blob is None:
        print("[secrets-set] ✗ không tải được bundle (cần TL_TOKEN hoặc --secrets-file).", file=sys.stderr)
        return 2
    try:
        bundle = json.loads(store.decrypt(blob, master).decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"[secrets-set] ✗ giải mã lỗi: {e}", file=sys.stderr)
        return 3
    changed = []
    if getattr(a, "gas_token", None):
        bundle["token"] = a.gas_token; changed.append("token")
    if getattr(a, "webapp", None):
        bundle["webappUrl"] = a.webapp; changed.append("webappUrl")
    if getattr(a, "gws", False):
        cred = _gws_export_cred()
        if not cred:
            print("[secrets-set] ✗ --gws cần gws đã auth ở máy này.", file=sys.stderr)
            return 3
        bundle["gws_cred"] = cred.decode("utf-8"); changed.append("gws_cred")
    if getattr(a, "nlm", False):                       # refresh cookie nlm tại chỗ (định kỳ ~2–4 tuần)
        _refresh_nlm_auth()
        nlm = _nlm_auth_files()
        if not nlm:
            print("[secrets-set] ✗ --nlm cần `nlm login` ở máy này.", file=sys.stderr)
            return 3
        bundle["nlm_auth"] = nlm; changed.append("nlm_auth")
        age = _nlm_auth_age_days(nlm)
        if age is not None:
            print(f"[secrets-set] nlm cookie ~{age:.0f} ngày tuổi.")
    if not changed:
        print("[secrets-set] ⚠ không có trường nào để đổi (--gas-token/--webapp/--gws/--nlm).", file=sys.stderr)
        return 1
    new = store.encrypt(json.dumps(bundle, ensure_ascii=False).encode("utf-8"), master)
    _secrets_upload(new, getattr(a, "folder", None) or HOPNAP_FOLDER_ID, fid)
    print(f"[secrets-set] ✓ đã đổi {changed} → ghi đè bundle id={fid} ({len(new)}B).")
    return 0


def _ensure_nlm_installed(version: str | None = None):
    """Cài nlm (notebooklm-mcp-cli, PyPI — KHÔNG có binary standalone, pure Python yêu cầu ≥3.11). Trả (ok, msg).
    ƯU TIÊN `uv tool install --python 3.11` → uv TỰ TẢI managed Python 3.11 (vượt rào sandbox Cowork 3.10) +
    venv biệt lập → `nlm` vào ~/.local/bin. uv thiếu → `pip install --user uv` trước. pip-trực-tiếp chỉ khi ≥3.11.
    Cowork CHẶN tải managed Python (no egress astral CDN) → bất khả; khi đó dùng NotebookLM MCP (đã sẵn)."""
    import subprocess as _sp, shutil as _sh
    try:
        nx = _imp("nlm_cli").nlm_exe()
    except Exception:
        nx = _sh.which("nlm")
    if nx:
        return True, f"đã có ({nx})"
    spec = f"notebooklm-mcp-cli=={version}" if version else "notebooklm-mcp-cli"
    # 1) uv (tốt nhất: tự cấp Python ≥3.11)
    uv = _sh.which("uv")
    if not uv:
        try:
            _sp.run([sys.executable, "-m", "pip", "install", "--user", "--upgrade", "uv"],
                    capture_output=True, text=True, timeout=300)
            uv = _sh.which("uv") or os.path.expanduser("~/.local/bin/uv")
            uv = uv if os.path.exists(uv) else None
        except Exception:
            uv = None
    if uv:
        try:
            # `uv tool install --python 3.11 notebooklm-mcp-cli` (đúng lệnh user yêu cầu). BẮT BUỘC --python 3.11:
            # package yêu cầu ≥3.11; thiếu flag → uv resolve system 3.10 → "all versions unsatisfiable" (lỗi Cowork).
            # ★ UV_PYTHON_DOWNLOADS=never: CẤM uv tải python từ astral/GitHub CDN (Cowork CHẶN → STALL ~phút). Khi đó:
            #   system CÓ 3.11 → dùng NGAY (tức thì); system CHỈ 3.10 → FAIL TỨC THÌ → rơi xuống Python public-curl (Drive).
            #   KHÔNG còn chờ astral. (Bỏ luôn `uv python install 3.11` — vô nghĩa khi CDN chặn.)
            env2 = dict(os.environ, UV_PYTHON_DOWNLOADS="never")
            p = _sp.run([uv, "tool", "install", "--python", "3.11", spec],
                        capture_output=True, text=True, timeout=300, env=env2)
            out = (p.stdout or "") + (p.stderr or "")
            try:
                nx2 = _imp("nlm_cli").nlm_exe() or _sh.which("nlm")
            except Exception:
                nx2 = _sh.which("nlm")
            if p.returncode == 0 or nx2 or "already installed" in out.lower():
                return True, f"đã `uv tool install --python 3.11 notebooklm-mcp-cli` (system 3.11){(' → '+nx2) if nx2 else ''}. Auth: `nlm login`."
            uv_err = out[-200:].strip()
        except Exception as e:  # noqa: BLE001
            uv_err = f"{type(e).__name__}: {e}"
    else:
        uv_err = "uv không cài được"
    # 2) Đường DRIVE-PYTHON (tự động, như `tl nlm-install`): uv tải managed Python từ astral CDN bị Cowork CHẶN
    #    → tải Python 3.11 standalone từ DRIVE (egress mở) rồi cài. Đây là đường tin cậy ở Cowork. Best-effort.
    try:
        if cmd_nlm_install(_NS(py_file_id=None, env=None, config=None, profile=None)) == 0:
            try:
                nx3 = _imp("nlm_cli").nlm_exe() or _sh.which("nlm")
            except Exception:
                nx3 = _sh.which("nlm")
            return True, f"đã cài nlm qua Python 3.11 staged từ Drive (uv CDN bị chặn){(' → ' + nx3) if nx3 else ''}."
    except Exception as e:  # noqa: BLE001
        uv_err = f"{uv_err}; staged-python: {type(e).__name__}: {e}"
    # 3) pip trực tiếp — chỉ khi Python ≥3.11 (package yêu cầu ≥3.11)
    if sys.version_info < (3, 11):
        return False, (f"uv lỗi ({uv_err}); pip trực tiếp KHÔNG được vì Python "
                       f"{sys.version_info.major}.{sys.version_info.minor} < 3.11. "
                       f"Chạy `tl nlm-install` (tải Python 3.11 từ Drive), hoặc dùng NotebookLM MCP (đã sẵn).")
    try:
        p = _sp.run([sys.executable, "-m", "pip", "install", "--user", "--upgrade", spec],
                    capture_output=True, text=True, timeout=420)
        if p.returncode != 0:
            return False, f"uv lỗi ({uv_err}); pip cũng lỗi: {(p.stderr or '')[-160:].strip()}"
        return True, "đã pip install notebooklm-mcp-cli (auth: `nlm login`)"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _persist_local_bin_on_path() -> str:
    """2.2 (log rà): ghi `export PATH=~/.local/bin:$PATH` BỀN vào ~/.profile + ~/.bashrc (shell login/non-login
    Cowork) để các phiên SAU thấy nlm trên PATH (bổ trợ cho việc tl tự nối PATH lúc spawn). Idempotent (bỏ qua
    nếu đã có /.local/bin), best-effort (nuốt lỗi), CHỈ POSIX (Windows bỏ qua). Trả thông điệp gọn ('' nếu no-op)."""
    if os.name != "posix":
        return ""
    line = 'export PATH="$HOME/.local/bin:$PATH"   # tra-luat nlm-install'
    done = []
    for fn in ("~/.profile", "~/.bashrc"):
        p = os.path.expanduser(fn)
        try:
            existing = open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""
            if "/.local/bin" in existing:          # đã có (do user/skill) → không nhân bản
                continue
            with open(p, "a", encoding="utf-8") as f:
                f.write(("" if (not existing or existing.endswith("\n")) else "\n") + line + "\n")
            done.append(fn)
        except Exception:
            pass
    return ("PATH ~/.local/bin ghi bền vào " + ", ".join(done)) if done else ""


def _nlm_install_probe(home: str | None = None, nlm_path: str | None = None) -> dict:
    """v1.30.1 (#1 log Cowork): dò TRẠNG THÁI cài nlm từ ĐĨA (idempotent, không mạng) → bước kế tiếp.
    fetch→extract→install→done; artifact bền: tarball `_dl/py311.tar.gz` (md5-verified) + pydir + uv cache.
    home/nlm_path: tham số test offline (mặc định máy thật)."""
    import shutil as _sh
    if nlm_path is None:
        try:
            nlm_path = _imp("nlm_cli").nlm_exe() or _sh.which("nlm") or ""
        except Exception:
            nlm_path = _sh.which("nlm") or ""
    pydir = os.path.join(home or os.path.expanduser("~"), ".local", "python311")
    pybin = os.path.join(pydir, "python", "bin", "python3.11")
    tgz = os.path.join(pydir, "_dl", "py311.tar.gz")
    if nlm_path:
        step = "done"
    elif os.path.exists(pybin):
        step = "install"
    elif os.path.exists(tgz):
        step = "extract"
    else:
        step = "fetch"
    return {"nlm": nlm_path or "", "pydir": pydir, "pybin": pybin, "tgz": tgz,
            "have_pybin": os.path.exists(pybin), "have_tgz": os.path.exists(tgz), "next_step": step}


def _nlm_step_fetch(a, st: dict) -> tuple[bool, str]:
    """Bước 1: tải Python 3.11 standalone về VỊ TRÍ BỀN (`.part` → md5-verify → os.replace) — chết giữa chừng
    KHÔNG để lại tarball hỏng, và bước sau resume khỏi tải lại (trước đây TemporaryDirectory → mất trắng)."""
    import hashlib as _hl
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (Exception, SystemExit):
        pass
    fid = getattr(a, "py_file_id", None) or PY311_FILEID
    os.makedirs(os.path.dirname(st["tgz"]), exist_ok=True)
    part = st["tgz"] + ".part"
    print(f"[nlm-install] tải Python 3.11 standalone (fileId={fid}, ~31MB) — ưu tiên public-curl…")
    try:
        _fast_drive_fetch(fid, part, label="py311", env=getattr(a, "env", None))   # public-curl → direct-media → GAS
    except Exception as e:  # noqa: BLE001
        return False, f"tải lỗi: {e}"
    got = _hl.md5(open(part, "rb").read()).hexdigest()
    if PY311_MD5 and got != PY311_MD5:
        try:
            os.remove(part)
        except Exception:
            pass
        return False, f"md5 LỆCH {got} ≠ {PY311_MD5} (file hỏng/sai bản — đã xóa, tải lại)"
    os.replace(part, st["tgz"])
    return True, f"tải + md5 OK → {st['tgz']}"


def _nlm_step_extract(st: dict) -> tuple[bool, str]:
    """Bước 2: giải nén tarball (đã md5-verify) → pydir; xong DỌN tarball 31MB (pybin là artifact bền của bước này)."""
    import tarfile as _tf
    with _tf.open(st["tgz"]) as t:
        # filter="fully_trusted": tarball ĐÃ md5-verify (đúng bản python-build-standalone chính thức) →
        # CHO PHÉP symlink hợp lệ (vd python/share/terminfo/…). filter="data" (backport 3.10.12) từ chối
        # các symlink này (LinkOutsideDestinationError) dù tarball hợp lệ → giải nén fail.
        try:
            t.extractall(st["pydir"], filter="fully_trusted")
        except TypeError:
            t.extractall(st["pydir"])                      # Python quá cũ chưa có tham số filter (mặc định = trusted)
    if not os.path.exists(st["pybin"]):
        return False, "không thấy python3.11 sau giải nén"
    try:
        os.remove(st["tgz"])
    except Exception:
        pass
    return True, f"giải nén Python → {st['pybin']}"


def _nlm_step_install(st: dict, version: str | None = None) -> tuple[bool, str]:
    """Bước 3: `uv tool install --python <pybin>` (uv KHÔNG tải managed Python — bỏ qua astral CDN; pkg từ PyPI)
    hoặc pip. Bị kill giữa chừng: uv CACHE giữ tiến độ tải gói (đo thật log 2026-07-03: 3 lần gọi là xong) —
    chạy lại CÙNG bước là resume."""
    import subprocess as _sp, shutil as _sh
    spec = f"notebooklm-mcp-cli=={version}" if version else "notebooklm-mcp-cli"
    uv = _sh.which("uv")
    if uv:
        p = _sp.run([uv, "tool", "install", "--python", st["pybin"], spec], capture_output=True, text=True, timeout=600)
    else:
        p = _sp.run([st["pybin"], "-m", "pip", "install", "--user", spec], capture_output=True, text=True, timeout=600)
    out = (p.stdout or "") + (p.stderr or "")
    try:
        nx = _imp("nlm_cli").nlm_exe() or _sh.which("nlm")
    except Exception:
        nx = _sh.which("nlm")
    if p.returncode == 0 or nx:
        return True, f"cài notebooklm-mcp-cli{(' → ' + nx) if nx else ''} (qua Python staged). Auth: `nlm login`."
    return False, f"cài nlm lỗi (bị kill 45s/PyPI chặn? uv cache GIỮ tiến độ — chạy lại): {out[-200:].strip()}"


_NLM_STEP_RC = {"fetch": 2, "extract": 4, "install": 5}    # rc lỗi theo bước (giữ tương thích cũ; md5 nay = 2)


def cmd_nlm_install(a) -> int:
    """[Cowork CHẶN egress astral CDN → uv không tải managed Python được] Cài nlm bằng Python 3.11 STANDALONE
    tải từ Drive (egress Drive MỞ): fetch PY311_FILEID → extract ~/.local/python311 → `uv tool install --python
    <bin>`/pip. Mặc định chạy TRỌN GÓI (env không giới hạn thời gian).
    ★ `--resume` (v1.30.1, #1 log Cowork 45s/lệnh + bwrap --unshare-pid kill tiến trình nền giữa 2 lần bash):
    MỖI LẦN GỌI chạy ĐÚNG 1 BƯỚC kế tiếp (trạng thái dò từ ĐĨA, idempotent) → rc=3 PARTIAL còn bước sau,
    rc=0 xong — LẶP LẠI CÙNG LỆNH tới rc=0 (thường ≤5 lần; bước install tự resume nhờ uv cache).
    `--uv`: egress MỞ → uv tự cài Python 3.11 (hoặc python hệ thống ≥3.11) → KHÔNG tải 31MB từ Drive."""
    if getattr(a, "uv", False):                            # egress mở: ưu tiên uv (python hệ thống ≥3.11 / uv tự cài 3.11)
        ok, msg = _ensure_nlm_installed(getattr(a, "version", None))   # fallback Drive bên trong (gọi lại với uv=False)
        print(f"[nlm-install] {'✓' if ok else '✗'} {msg}", file=(sys.stdout if ok else sys.stderr))
        if ok:
            _pmsg = _persist_local_bin_on_path()
            if _pmsg:
                print(f"[nlm-install] {_pmsg}")
        return 0 if ok else 5

    def _run_step(st: dict) -> tuple[bool, str]:
        if st["next_step"] == "fetch":
            return _nlm_step_fetch(a, st)
        if st["next_step"] == "extract":
            return _nlm_step_extract(st)
        return _nlm_step_install(st, getattr(a, "version", None))

    def _done(st: dict) -> int:
        print(f"[nlm-install] ✓ DONE — nlm sẵn sàng ({st['nlm']}). Auth: `nlm login`.")
        _pmsg = _persist_local_bin_on_path()
        if _pmsg:
            print(f"[nlm-install] {_pmsg}")
        return 0

    if getattr(a, "resume", False):
        st = _nlm_install_probe()
        if st["next_step"] == "done":
            return _done(st)
        print(f"[nlm-install] --resume: bước kế = {st['next_step']} (fetch→extract→install; trạng thái từ đĩa)")
        ok, msg = _run_step(st)
        print(f"[nlm-install] {'✓' if ok else '✗'} {msg}", file=(sys.stdout if ok else sys.stderr))
        if not ok:
            print("[nlm-install] chạy LẠI: `tl nlm-install --resume` — bước lỗi được thử tiếp, tiến độ KHÔNG mất "
                  "(tarball bền + uv cache).", file=sys.stderr)
            return _NLM_STEP_RC[st["next_step"]]
        st2 = _nlm_install_probe()
        if st2["next_step"] == "done":
            return _done(st2)
        if st["next_step"] == "install":     # install OK nhưng nlm chưa thấy trên PATH probe → tin rc=0 (hành vi cũ),
            print("[nlm-install] ✓ install OK nhưng `nlm` chưa thấy trên PATH phiên này — mở shell mới / "
                  "`export PATH=$HOME/.local/bin:$PATH` rồi `nlm login`.")
            return 0                          # KHÔNG trả PARTIAL lặp vô ích trên cùng bước.
        print(f"[nlm-install] PARTIAL — xong '{st['next_step']}', còn '{st2['next_step']}'. "
              f"Chạy LẠI: `tl nlm-install --resume` (rc=3 = còn bước, KHÔNG phải lỗi).")
        return 3
    # đường TRỌN GÓI (giữ hành vi cũ cho env không giới hạn) — tái dùng step-machine + tarball BỀN:
    # bị kill giữa chừng thì lần chạy sau (trọn gói hoặc --resume) tiếp đúng bước dở, không mất tiến độ.
    _prev = None
    while True:
        st = _nlm_install_probe()
        if st["next_step"] == "done":
            return _done(st)
        if st["next_step"] == _prev:         # bước OK mà trạng thái KHÔNG TIẾN (vd install rc=0, nlm chưa trên PATH)
            print("[nlm-install] ✓ bước cuối OK nhưng `nlm` chưa thấy trên PATH phiên này — mở shell mới / "
                  "`export PATH=$HOME/.local/bin:$PATH` rồi `nlm login`.")
            return 0                          # chống lặp vô hạn; tin rc=0 của bước (hành vi cũ)
        ok, msg = _run_step(st)
        print(f"[nlm-install] {'✓' if ok else '✗'} {msg}", file=(sys.stdout if ok else sys.stderr))
        if not ok:
            return _NLM_STEP_RC[st["next_step"]]
        _prev = st["next_step"]


def cmd_nlm_auth_pull(a) -> int:
    """[COWORK] Kéo RIÊNG cookie nlm mới nhất từ bundle .enc → ghi ~/.notebooklm-mcp-cli (refresh giữa phiên, nhẹ
    hơn bootstrap đầy đủ). Nguồn: --secrets-file (project file) → direct-media (gws cred) → webapp. Sau khi ở Code
    chạy `secrets-set --nlm`, gọi lệnh này để Cowork lấy cookie mới mà không cài lại gì."""
    master = _master_key()
    if not master:
        print("[nlm-auth-pull] ✗ thiếu TL_MASTER_KEY.", file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (Exception, SystemExit):
        pass
    fid = getattr(a, "secrets_id", None) or os.environ.get("TL_SECRETS_FILEID") or SECRETS_FILEID
    blob, src = _secrets_fetch(a, fid)
    if blob is None and fid:                       # chưa có --secrets-file/TL_TOKEN → direct-media (gws cred Cowork)
        with tempfile.TemporaryDirectory() as d:
            dst = os.path.join(d, "s.enc")
            try:
                r = _imp("transport").drive_op("download", env=getattr(a, "env", None), file_id=fid, dest=dst)
                if isinstance(r, dict) and r.get("ok"):
                    blob, src = open(dst, "rb").read(), "direct-media"
            except Exception:  # noqa: BLE001
                pass
    if blob is None:
        print("[nlm-auth-pull] ✗ không lấy được bundle (cần --secrets-file / TL_TOKEN / gws cred).", file=sys.stderr)
        return 2
    try:
        bundle = json.loads(_imp("gws_cred_store").decrypt(blob, master).decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"[nlm-auth-pull] ✗ giải mã lỗi: {e}", file=sys.stderr)
        return 3
    nlm = bundle.get("nlm_auth")
    if not nlm:
        print("[nlm-auth-pull] ⚠ bundle chưa có nlm_auth — ở Code chạy `tl secrets-set --nlm` trước.", file=sys.stderr)
        return 1
    nbase = os.path.expanduser("~/.notebooklm-mcp-cli")
    for rel, content in nlm.items():
        dst = os.path.join(nbase, *str(rel).split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(content)
        try:
            os.chmod(dst, 0o600)
        except OSError:
            pass
    age = _nlm_auth_age_days(nlm)
    agestr = f" (~{age:.0f} ngày tuổi)" if age is not None else ""
    print(f"[nlm-auth-pull] ✓ nlm auth {len(nlm)} file → ~/.notebooklm-mcp-cli{agestr} [nguồn {src}]. Kiểm: nlm login --check")
    return 0


def cmd_bootstrap(a) -> int:
    """ENV-AWARE: giải mã bundle (TL_MASTER_KEY) → nạp GAS token (mọi env) + gws binary/cred (Code/Cowork).
    Chat: tl.py không chạy ở Chat thật — lệnh này cho Code/Cowork. Tải bundle: --secrets-file / webapp / MCP."""
    tr = _imp("transport")
    env = tr.runtime_env(getattr(a, "env", None))
    master = _master_key()
    if not master:
        print("[bootstrap] ✗ thiếu TL_MASTER_KEY (export TL_MASTER_KEY=...). "
              "Hoặc dùng cơ chế cũ: gws-bootstrap-cowork (cred keyed by webapp token).", file=sys.stderr)
        return 2
    sf = getattr(a, "secrets_file", None)
    if sf and not os.path.exists(sf):     # B1: --secrets-file trỏ file KHÔNG có → báo RÕ, đừng để FileNotFoundError
        print(f"[bootstrap] ✗ --secrets-file '{sf}' KHÔNG tồn tại. Đặt tl_secrets.enc vào thư mục Context, hoặc bỏ "
              f"--secrets-file để tải qua webapp/direct-media (cần TL_TOKEN/SECRETS_FILEID).", file=sys.stderr)
        return 2
    try:                                  # best-effort: config sẵn (Code) → có TL_TOKEN để webapp-fetch bundle
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (Exception, SystemExit):       # fresh Cowork: chưa có config (load_creds sys.exit) → dùng --secrets-file
        pass
    fid = getattr(a, "secrets_id", None) or os.environ.get("TL_SECRETS_FILEID") or SECRETS_FILEID
    blob, src = _secrets_fetch(a, fid)
    if blob is None:
        print(f"[bootstrap] ✗ chưa lấy được tl_secrets.enc. Cowork: agent tải fileId={fid or '<SECRETS_FILEID>'} "
              f"qua Drive MCP → lưu file → `tl bootstrap --secrets-file <path>`.", file=sys.stderr)
        return 2
    try:
        bundle = json.loads(_imp("gws_cred_store").decrypt(blob, master).decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"[bootstrap] ✗ giải mã lỗi: {e} (TL_MASTER_KEY khác lúc stage?)", file=sys.stderr)
        return 3
    print(f"[bootstrap] env={env} · bundle giải mã OK (nguồn .enc: {src})")
    # 1) FULL config (token + rootFolderId/categories/…) → env + MERGE vào ~/.tra_luat_config.json
    if bundle.get("token"):
        os.environ["TL_TOKEN"] = bundle["token"]
        if bundle.get("webappUrl"):
            os.environ["TL_WEBAPP"] = bundle["webappUrl"]
        cfgp = os.path.expanduser("~/.tra_luat_config.json")
        existing = {}
        if os.path.exists(cfgp):
            try:
                existing = json.load(open(cfgp, encoding="utf-8"))
            except Exception:
                existing = {}
        existing.update({k: v for k, v in bundle.items() if k != "gws_cred"})   # MERGE, không clobber
        try:
            with open(cfgp, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False)
            os.chmod(cfgp, 0o600)
            print(f"[bootstrap] ✓ config (token + {len([k for k in bundle if k!='gws_cred'])} khoá) → env + {cfgp} (chmod 600)")
        except OSError as e:
            print(f"[bootstrap] ✓ token nạp env (ghi config lỗi: {e})")
    else:
        print("[bootstrap] ⚠ bundle thiếu GAS token.", file=sys.stderr)
    # 2) gws (Code/Cowork): binary nếu thiếu + cred từ bundle
    degraded = False                       # B8: theo dõi để exit code phản ánh đúng (không "nuốt" lỗi → trả 0)
    if env in ("code", "cowork"):
        # Ghi gws cred TRƯỚC (để cài binary dùng được direct-media raw thay vì webapp b64).
        if bundle.get("gws_cred"):
            cfgdir = os.environ.get("GOOGLE_WORKSPACE_CLI_CONFIG_DIR") or os.path.expanduser("~/.config/gws")
            os.makedirs(cfgdir, exist_ok=True)
            dest = os.path.join(cfgdir, "credentials.json")
            with open(dest, "wb") as f:
                f.write(bundle["gws_cred"].encode("utf-8"))
            try:
                os.chmod(dest, 0o600)
            except OSError:
                pass
            print(f"[bootstrap] ✓ gws cred → {dest} (chmod 600)")
        else:
            print("[bootstrap] ⚠ bundle thiếu gws_cred — gws sẽ chưa auth (op vẫn fallback GAS).", file=sys.stderr)
            degraded = True
        if bundle.get("nlm_auth"):                     # nạp auth nlm (cookies) → nlm chạy headless, khỏi `nlm login`
            nbase = os.path.expanduser("~/.notebooklm-mcp-cli")
            for rel, content in bundle["nlm_auth"].items():
                dst = os.path.join(nbase, *str(rel).split("/"))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(content)
                try:
                    os.chmod(dst, 0o600)
                except OSError:
                    pass
            age = _nlm_auth_age_days(bundle["nlm_auth"])
            agestr = f" · cookie ~{age:.0f} ngày tuổi" if age is not None else ""
            print(f"[bootstrap] ✓ nlm auth ({len(bundle['nlm_auth'])} file) → ~/.notebooklm-mcp-cli (nlm headless){agestr}")
            if age is not None and age > 14:           # cookie sống ~2–4 tuần → nhắc re-stage ở Code
                print(f"[bootstrap] ⚠ nlm cookie ~{age:.0f} ngày — nếu auth lỗi, ở Code chạy `nlm login` rồi "
                      f"`tl secrets-set --nlm`.", file=sys.stderr)
        if not _imp("gws_bridge").gws_exe() and not getattr(a, "no_gws", False):
            print("[bootstrap] gws chưa có PATH → cài binary (direct-media nếu có cred)…")
            try:
                rc = cmd_gws_bootstrap_cowork(_NS(file_id=None, md5=None, bindir=getattr(a, "bindir", None),
                                                  cred_file_id=None, no_auth=True, config=getattr(a, "config", None),
                                                  profile=getattr(a, "profile", None)))
            except Exception as e:  # noqa: BLE001 — B8: lỗi cài binary KHÔNG được crash câm → ghi nhận degraded
                print(f"[bootstrap] ⚠ cài gws binary lỗi: {type(e).__name__}: {e}", file=sys.stderr); rc = 1
            if rc != 0:
                print("[bootstrap] ⚠ cài gws binary chưa xong (op vẫn fallback GAS).", file=sys.stderr)
                degraded = True
        if not getattr(a, "no_nlm", False):
            try:
                okn, msgn = _ensure_nlm_installed()
            except Exception as e:  # noqa: BLE001
                okn, msgn = False, f"{type(e).__name__}: {e}"
            print(f"[bootstrap] {'✓' if okn else '⚠'} nlm (notebooklm-mcp-cli): {msgn}",
                  file=(sys.stdout if okn else sys.stderr))
    status = "XONG" if not degraded else "XONG (SUY GIẢM — gws/nlm chưa đủ, op chạy fallback GAS)"
    print(f"[bootstrap] ➜ {status} (env={env}). Kiểm: python scripts/tl.py ping ; tl gws-ping --env {env}")
    return 0 if not degraded else 1   # B8: degraded → exit≠0 để caller tự động biết bootstrap chưa trọn


class _NS:
    """Namespace nhẹ để gọi lại cmd_* với tham số dựng sẵn."""
    def __init__(self, **kw):
        self.__dict__.update(kw)


def cmd_gws_auth_stage(a) -> int:
    """[CHẠY Ở CODE] Xuất gws cred → MÃ HOÁ (khoá=webapp token) → upload Drive. In fileId để baked.
    Cred KHÔNG plaintext, KHÔNG vào zip — chỉ bản mã hoá nằm trên Drive riêng của bạn."""
    import subprocess as _sp, shutil as _sh, tempfile
    store = _imp("gws_cred_store")
    token = os.environ.get("TL_TOKEN") or ""
    if not token:
        print("[gws-auth-stage] ✗ thiếu webapp token (TL_TOKEN/config) — không có khoá mã hoá.", file=sys.stderr)
        return 2
    exe = _imp("gws_bridge").gws_exe()
    if not exe:
        print("[gws-auth-stage] ✗ cần gws (đã auth) trên máy này để export cred.", file=sys.stderr)
        return 3
    p = _sp.run([exe, "auth", "export", "--unmasked"], capture_output=True, text=True, timeout=60)
    if p.returncode != 0 or not (p.stdout or "").strip():
        print(f"[gws-auth-stage] ✗ export lỗi: {(p.stderr or '').strip()[:200]}", file=sys.stderr)
        return 3
    blob = store.encrypt((p.stdout or "").strip().encode("utf-8"), token)   # cred chỉ tồn tại trong RAM
    folder = getattr(a, "folder", None) or HOPNAP_FOLDER_ID
    g = _imp("gws_bridge")
    with tempfile.TemporaryDirectory() as d:
        fp = os.path.join(d, "gws_cred.enc")
        with open(fp, "wb") as f:
            f.write(blob)
        r = g.upload("gws_cred.enc", fp, parents=[folder], mime="application/octet-stream")
    fid = (r.get("file") or {}).get("id")
    print(f"[gws-auth-stage] ✓ cred MÃ HOÁ ({len(blob)}B) → Drive id={fid}")
    print(f"  → baked: đặt GWS_CRED_FILEID = \"{fid}\" trong tl.py (hoặc dùng `gws-auth-load --cred-file-id {fid}`).")
    return 0


def _gws_auth_load(token: str, fid: str):
    """Tải gws_cred.enc (webapp download) → giải mã (khoá=token) → ghi ~/.config/gws/credentials.json.
    Trả (ok: bool, msg: str). Dùng bởi cmd_gws_auth_load và bootstrap."""
    import base64
    store = _imp("gws_cred_store")
    if not fid:
        return False, "chưa có GWS_CRED_FILEID — chạy `gws-auth-stage` ở Code trước."
    if not token:
        return False, "thiếu webapp token (khoá giải mã)."
    enc = _public_curl_bytes(fid)            # gws_cred.enc nay PUBLIC → curl raw (nhanh, KHÔNG qua GAS)
    if enc is None:                          # chưa public / lỗi mạng → fallback webapp b64
        r = _gas().get("download", fileId=fid)
        if not isinstance(r, dict) or not r.get("ok") or not r.get("b64"):
            return False, f"download .enc lỗi: {(r or {}).get('error') or r}"
        enc = base64.b64decode(r["b64"])
    try:
        cred = store.decrypt(enc, token)
    except Exception as e:  # noqa: BLE001
        return False, f"giải mã lỗi: {e}"
    cfgdir = os.environ.get("GOOGLE_WORKSPACE_CLI_CONFIG_DIR") or os.path.expanduser("~/.config/gws")
    os.makedirs(cfgdir, exist_ok=True)
    dest = os.path.join(cfgdir, "credentials.json")
    with open(dest, "wb") as f:
        f.write(cred)
    try:
        os.chmod(dest, 0o600)
    except OSError:
        pass
    return True, dest


def cmd_gws_auth_load(a) -> int:
    """[CHẠY Ở COWORK] Nạp gws cred TỰ ĐỘNG: tải bản mã hoá từ Drive → giải mã (webapp token) →
    ~/.config/gws/credentials.json. Zero-setup; gws tự dùng (không cần env). Sau đó `tl gws-ping`."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    token = os.environ.get("TL_TOKEN") or ""
    fid = getattr(a, "cred_file_id", None) or GWS_CRED_FILEID
    ok, msg = _gws_auth_load(token, fid)
    if ok:
        print(f"[gws-auth-load] ✓ nạp gws cred → {msg} (chmod 600). Kiểm: python scripts/tl.py gws-ping --env cowork")
        return 0
    print(f"[gws-auth-load] ✗ {msg}", file=sys.stderr)
    return 2


def _nlm_auth_load(token: str, fid: str):
    """Tải nlm_cred.enc (webapp `download`) → giải mã (khoá=token) → ghi ~/.notebooklm-mcp-cli/{auth.json,profiles/…}.
    Trả (ok, msg). KHÔNG cần master key (mirror _gws_auth_load → nlm headless)."""
    import base64
    store = _imp("gws_cred_store")
    if not fid:
        return False, "chưa có NLM_CRED_FILEID — ở Code (sau `nlm login`) chạy `tl nlm-auth-stage`, rồi điền fileId / env TL_NLM_CRED_FILEID."
    if not token:
        return False, "thiếu webapp token (khoá giải mã)."
    enc = _public_curl_bytes(fid)            # nlm_cred.enc nay PUBLIC → curl raw (nhanh, KHÔNG qua GAS)
    if enc is None:
        r = _gas().get("download", fileId=fid)
        if not isinstance(r, dict) or not r.get("ok") or not r.get("b64"):
            return False, f"download .enc lỗi: {(r or {}).get('error') or r}"
        enc = base64.b64decode(r["b64"])
    try:
        nlm = json.loads(store.decrypt(enc, token).decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        return False, f"giải mã lỗi (token sai/dữ liệu hỏng): {e}"
    if not isinstance(nlm, dict) or not nlm:
        return False, "nlm_cred rỗng/sai định dạng."
    nbase = os.path.expanduser("~/.notebooklm-mcp-cli")
    for rel, content in nlm.items():
        dst = os.path.join(nbase, *str(rel).split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(content)
        try:
            os.chmod(dst, 0o600)
        except OSError:
            pass
    age = _nlm_auth_age_days(nlm)
    return True, f"~/.notebooklm-mcp-cli ({len(nlm)} file" + (f", ~{age:.0f} ngày tuổi" if age is not None else "") + ")"


def cmd_nlm_auth_stage(a) -> int:
    """[CHẠY Ở CODE, sau `nlm login`] Gói cookie nlm → MÃ HOÁ (khoá=webapp token) → upload Drive. In fileId để baked.
    Cho Cowork nạp nlm HEADLESS bằng `nlm-auth-load` KHÔNG cần master key (mirror gws-auth-stage)."""
    store = _imp("gws_cred_store")
    token = os.environ.get("TL_TOKEN") or ""
    if not token:
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (Exception, SystemExit):
            pass
        token = os.environ.get("TL_TOKEN") or ""
    if not token:
        print("[nlm-auth-stage] ✗ thiếu webapp token (TL_TOKEN/config) — không có khoá mã hoá.", file=sys.stderr)
        return 2
    if getattr(a, "refresh", False):
        _refresh_nlm_auth()
    nlm = _nlm_auth_files()
    if not nlm:
        print("[nlm-auth-stage] ✗ chưa có cookie nlm ở máy này — chạy `nlm login` trước.", file=sys.stderr)
        return 3
    blob = store.encrypt(json.dumps(nlm, ensure_ascii=False).encode("utf-8"), token)   # cookie chỉ ở RAM
    folder = getattr(a, "folder", None) or HOPNAP_FOLDER_ID
    g = _imp("gws_bridge")
    with tempfile.TemporaryDirectory() as d:
        fp = os.path.join(d, "nlm_cred.enc")
        with open(fp, "wb") as f:
            f.write(blob)
        r = g.upload("nlm_cred.enc", fp, parents=[folder], mime="application/octet-stream")
    fid = (r.get("file") or {}).get("id")
    age = _nlm_auth_age_days(nlm)
    agestr = f", ~{age:.0f} ngày" if age is not None else ""
    print(f"[nlm-auth-stage] ✓ nlm cookie MÃ HOÁ ({len(nlm)} file, {len(blob)}B{agestr}) → Drive id={fid}")
    print(f"  → baked: đặt NLM_CRED_FILEID = \"{fid}\" trong tl.py (hoặc env TL_NLM_CRED_FILEID / `nlm-auth-load --cred-file-id {fid}`).")
    return 0


def cmd_nlm_auth_load(a) -> int:
    """[CHẠY Ở COWORK] Nạp nlm cookie HEADLESS: tải bản mã hoá từ Drive → giải mã (webapp token) →
    ~/.notebooklm-mcp-cli. KHÔNG cần master key/`nlm login` (mirror gws-auth-load). Sau đó nlm chạy thẳng (không MCP fallback)."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    token = os.environ.get("TL_TOKEN") or ""
    fid = getattr(a, "cred_file_id", None) or os.environ.get("TL_NLM_CRED_FILEID") or NLM_CRED_FILEID
    ok, msg = _nlm_auth_load(token, fid)
    if ok:
        print(f"[nlm-auth-load] ✓ nạp nlm cookie → {msg} (chmod 600). nlm chạy headless. Kiểm: nlm login --check")
        return 0
    print(f"[nlm-auth-load] ✗ {msg}", file=sys.stderr)
    return 2


def cmd_drive_push(a) -> int:
    """[CHẠY Ở MÁY CÓ gws AUTH] Cập nhật NỘI DUNG file Drive (GIỮ fileId) = file local, qua gws update_content.
    Dùng đẩy zip/bundle skill mới lên Drive mỗi lần ship mà KHÔNG đổi fileId → tl_fetch.sh tự lấy bản mới.
    Mặc định fileId = SKILL_FILEID. KHÔNG tạo file mới; chỉ thay nội dung."""
    import mimetypes
    path = getattr(a, "path", None)
    fid = getattr(a, "file_id", None) or SKILL_FILEID
    if not path or not os.path.exists(path):
        print(f"[drive-push] ✗ không thấy file: {path}", file=sys.stderr)
        return 2
    if not fid:
        print("[drive-push] ✗ thiếu --file-id (và SKILL_FILEID trống).", file=sys.stderr)
        return 2
    gb = _imp("gws_bridge")
    if not gb.is_available():
        print("[drive-push] ✗ gws chưa sẵn/auth trên máy này — cần `gws` đã `gws auth login` để thay nội dung Drive.", file=sys.stderr)
        return 3
    mime = "application/zip" if path.lower().endswith(".zip") else (mimetypes.guess_type(path)[0] or "application/octet-stream")
    try:
        r = gb.update_content(fid, path, mime=mime)
    except Exception as e:  # noqa: BLE001
        print(f"[drive-push] ✗ update lỗi: {type(e).__name__}: {e}", file=sys.stderr)
        return 4
    f = (r or {}).get("file") or {}
    # ĐỔI TÊN file Drive (GIỮ fileId): --name <tên> tường minh, hoặc --rename-to-file → lấy tên file upload (basename).
    new_name = getattr(a, "name", None) or (os.path.basename(path) if getattr(a, "rename_to_file", False) else None)
    renamed = ""
    if new_name:
        try:
            gb.rename(fid, new_name)   # rename có ASSERT đọc-lại-tên (v1.22.60) → lỗi sẽ raise rõ
            renamed = f" · đổi tên → '{new_name}'"
        except Exception as e:  # noqa: BLE001
            print(f"[drive-push] ⚠ update OK nhưng ĐỔI TÊN lỗi: {type(e).__name__}: {e}", file=sys.stderr)
    print(f"[drive-push] ✓ Drive id={f.get('id') or fid} ← {os.path.basename(path)} ({os.path.getsize(path)}B){renamed}. "
          f"fileId GIỮ NGUYÊN; tl_fetch.sh sẽ tải bản mới này.")
    return 0


def cmd_gws_bootstrap_cowork(a) -> int:
    """Cài gws trên Cowork bằng 1 LỆNH (sandbox chặn github + no root):
    tải binary MUSL-static từ Drive qua webapp `download` (b64 decode THẲNG xuống đĩa, KHÔNG vào context)
    → md5 verify → giải nén → chmod +x → đặt vào bindir. In dòng PATH + bước nạp credential."""
    import base64, hashlib, tarfile, tempfile, stat, shutil as _sh, platform as _pf, subprocess as _sp
    # Env THỐNG NHẤT: nếu gws ĐÃ CÓ (PATH/bindir, vd Chat/Code có sẵn) → KHỎI TẢI BINARY, chỉ nạp cred. `--force` để ép tải lại.
    if not getattr(a, "force", False) and (_sh.which("gws") or _imp("gws_bridge").gws_exe()):
        _ex = _sh.which("gws") or _imp("gws_bridge").gws_exe()
        print(f"[gws-bootstrap] gws ĐÃ CÓ ({_ex}) → bỏ qua tải binary, chỉ nạp cred.")
        if not getattr(a, "no_auth", False):
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            ok, msg = _gws_auth_load(os.environ.get("TL_TOKEN") or "", getattr(a, "cred_file_id", None) or GWS_CRED_FILEID)
            print(f"[gws-bootstrap] {'✓' if ok else '⚠'} gws cred: {msg}", file=(sys.stdout if ok else sys.stderr))
        return 0
    fid = getattr(a, "file_id", None) or GWS_COWORK_FILEID
    want_md5 = getattr(a, "md5", None) or GWS_COWORK_MD5
    bindir = os.path.expanduser(getattr(a, "bindir", None) or "~/.local/bin")
    mach = _pf.machine()
    if mach not in ("x86_64", "AMD64"):
        print(f"[gws-bootstrap] ⚠ arch={mach} ≠ x86_64 — bản stage là x86_64-musl. aarch64 cần stage bản "
              f"aarch64-unknown-linux-musl (báo để stage).", file=sys.stderr)
    os.makedirs(bindir, exist_ok=True)
    binpath = os.path.join(bindir, "gws")
    with tempfile.TemporaryDirectory() as d:
        tgz = os.path.join(d, "gws.tgz")
        # (0) BUNDLE: gws.tgz đã có sẵn local (tl_fetch.sh giải nén từ bundle) → KHỎI TẢI (md5 vẫn verify bên dưới).
        local = getattr(a, "local_tgz", None) or os.environ.get("TL_GWS_TGZ")
        if local and os.path.exists(local):
            _sh.copyfile(local, tgz)
            src = "local-tgz (bundle — khỏi tải Drive)"
        else:
            # gws binary nay PUBLIC ở Package → ƯU TIÊN public-curl (không cần cred, nhanh nhất); fallback
            # direct-media (nếu có gws cred) → webapp b64 (GAS). _fast_drive_fetch tự đo + chọn đường nhanh.
            try:
                src, _secs = _fast_drive_fetch(fid, tgz, label="gws-bin", env=getattr(a, "env", None))
            except Exception as e:  # noqa: BLE001
                print(f"[gws-bootstrap] ✗ tải lỗi (mọi đường): {e}", file=sys.stderr)
                return 2
        got = hashlib.md5(open(tgz, "rb").read()).hexdigest()
        if want_md5 and got != want_md5:
            print(f"[gws-bootstrap] ✗ md5 LỆCH: {got} ≠ {want_md5} (file hỏng/sai bản)", file=sys.stderr)
            return 3
        print(f"[gws-bootstrap] tải {os.path.getsize(tgz)} bytes · md5 {got} ✓ [{src}]")
        with tarfile.open(tgz) as t:
            m = next((x for x in t.getmembers() if os.path.basename(x.name) == "gws" and x.isfile()), None)
            if not m:
                print("[gws-bootstrap] ✗ không thấy binary 'gws' trong archive", file=sys.stderr)
                return 4
            m.name = "gws"
            try:
                t.extract(m, d, filter="data")   # Python ≥3.12: lọc an toàn (chống path-traversal)
            except TypeError:
                t.extract(m, d)                  # Python <3.12: chưa có tham số filter
            _sh.move(os.path.join(d, "gws"), binpath)
    os.chmod(binpath, os.stat(binpath).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    ver = ""
    try:
        ver = (_sp.run([binpath, "--version"], capture_output=True, text=True, timeout=15).stdout or "").strip().splitlines()
        ver = ver[0] if ver else ""
    except Exception as e:  # noqa: BLE001
        print(f"[gws-bootstrap] ⚠ chưa chạy thử được ({type(e).__name__}: {e}) — bình thường nếu đang ở máy khác OS.", file=sys.stderr)
    print(f"[gws-bootstrap] ✓ đặt {binpath} ({ver or 'binary đã chmod +x'})")
    if not _sh.which("gws"):
        print(f"[gws-bootstrap] ℹ `tl` TỰ tìm gws ở {bindir} (khỏi cần PATH). Gõ `gws` trực tiếp thì: "
              f"export PATH=\"{bindir}:$PATH\"")
    # Nạp credential TỰ ĐỘNG (mã hoá trên Drive, khoá=webapp token) → zero-setup auth, trừ khi --no-auth.
    if not getattr(a, "no_auth", False):
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        ok, msg = _gws_auth_load(os.environ.get("TL_TOKEN") or "", getattr(a, "cred_file_id", None) or GWS_CRED_FILEID)
        if ok:
            print(f"[gws-bootstrap] ✓ nạp gws cred (giải mã) → {msg}")
            print("[gws-bootstrap] ➜ XONG. Kiểm:  python scripts/tl.py gws-ping --env cowork  (auth=ok → rc 0)")
        else:
            print(f"[gws-bootstrap] ⚠ chưa nạp được cred ({msg}) — mang credentials.json thủ công (RUNBOOK §A0.4).", file=sys.stderr)
    else:
        print("[gws-bootstrap] ➜ (--no-auth) tự nạp credential rồi: python scripts/tl.py gws-ping --env cowork")
    return 0


def cmd_download(a) -> int:
    """Tải file Drive → đĩa qua transport (gws PRIMARY cho binary, tự FALLBACK→GAS cho text/JSON raw).
    Nhanh nhất: gws ghi raw (1 hop, không b64, không cap 9MB). Google-native: --export-mime để export."""
    tr = _imp("transport")
    dest = a.out or (a.file_id + ".bin")
    kw = {"file_id": a.file_id, "dest": dest}
    if getattr(a, "export_mime", None):
        kw["export_mime"] = a.export_mime
    try:
        r = tr.drive_op("download", env=getattr(a, "env", None), **kw)
    except Exception as e:  # noqa: BLE001
        print(f"[download] ✗ {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    if not isinstance(r, dict) or not r.get("ok"):
        print(f"[download] ✗ {r}", file=sys.stderr)
        return 2
    print(f"[download] ✓ {r.get('path')} ({r.get('bytes')} bytes)")
    return 0


def cmd_drive_parity(a) -> int:
    """GĐ1 pilot (read-only, nhóm A) — đối chứng get-meta 1 fileId qua gws vs GAS; đo thời gian;
    in spec MCP để Claude đối chứng tay; test fallback gws→GAS (TL_GWS_DISABLE=1). PHẢI KHỚP."""
    import time as _t
    fid = a.file_id
    tr = _imp("transport")
    out = {"op": "files_get", "file_id": fid}
    # gws (PRIMARY)
    g_err = None
    t0 = _t.time()
    try:
        gws_r = tr.via_gws("files_get", file_id=fid)
    except Exception as e:  # noqa: BLE001
        gws_r, g_err = None, f"{type(e).__name__}: {e}"
    out["gws_ms"] = int((_t.time() - t0) * 1000)
    # GAS (FALLBACK path, đối chứng)
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    s_err = None
    t0 = _t.time()
    try:
        gas_r = tr.via_gas("files_get", file_id=fid)
    except Exception as e:  # noqa: BLE001
        gas_r, s_err = None, f"{type(e).__name__}: {e}"
    out["gas_ms"] = int((_t.time() - t0) * 1000)
    gf = (gws_r or {}).get("file")
    af = (gas_r or {}).get("file")
    out["gws_file"], out["gas_file"] = gf, af
    out["gws_err"], out["gas_err"] = g_err, s_err
    match = gf is not None and gf == af
    out["gws_gas_match"] = match
    if gf and af and not match:
        out["diff_fields"] = sorted(k for k in set(gf) | set(af) if gf.get(k) != af.get(k))
    # spec MCP (env Chat) — Claude gọi tool này để hoàn tất đối chứng 3-backend
    out["mcp_spec"] = tr.mcp_spec("files_get", file_id=fid)
    # test fallback: tắt gws → router phải [FALLBACK→GAS] và khớp GAS
    fb = None
    if getattr(a, "test_fallback", False):
        os.environ["TL_GWS_DISABLE"] = "1"
        tr.gws_bridge.reset_cache()
        try:
            fr = tr.drive_op("files_get", env="code", file_id=fid)
            fb = {"fell_back_to_gas": True, "match_gas": (fr or {}).get("file") == af}
        except Exception as e:  # noqa: BLE001
            fb = {"error": f"{type(e).__name__}: {e}"}
        finally:
            os.environ.pop("TL_GWS_DISABLE", None)
            tr.gws_bridge.reset_cache()
    out["fallback_test"] = fb
    if getattr(a, "json", False):
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"[drive-parity] op=files_get file={fid}")
        print(f"  gws : {'OK ' + str(out['gws_ms']) + 'ms' if gf else 'ERR ' + str(g_err)}")
        print(f"  gas : {'OK ' + str(out['gas_ms']) + 'ms' if af else 'ERR ' + str(s_err)}")
        print(f"  gws≡gas : {'✓ KHỚP' if match else '✗ KHÁC ' + str(out.get('diff_fields') or '(thiếu 1 phía)')}")
        if gf:
            print(f"            name={gf.get('name')!r} md5={gf.get('md5')} parents={gf.get('parents')}")
        sp = out["mcp_spec"]
        print(f"  mcp : Claude gọi `{sp.get('tool')}` args={sp.get('args')} rồi so với trên (đối chứng tay)")
        if fb is not None:
            ok = isinstance(fb, dict) and fb.get("match_gas")
            print(f"  fallback(gws OFF): {'✓ →GAS ồn ào, khớp' if ok else fb}")
    return 0 if match else 1


def cmd_transport_info(a) -> int:
    """GĐ4 — in MA TRẬN ĐỊNH TUYẾN transport (OP_GROUP A–E × 3-env) + trạng thái gws. Read-only, tự sinh."""
    tr = _imp("transport")
    gws_av = tr.gws_bridge.availability_detail()
    mcp_tools = tr.mcp_bridge._OP_TOOL
    defer_write = tr.mcp_bridge._DEFER_WRITE
    gas_ok = set(tr._GAS_READ) | set(tr._GAS_B) | set(tr._GAS_C) | set(tr._GAS_D_ACTION)
    no_gas = tr._NO_GAS_FALLBACK
    order = {"A": 0, "B": 1, "C": 2, "D": 3}
    rows = []
    for op, grp in sorted(tr.OP_GROUP.items(), key=lambda kv: (order.get(kv[1], 9), kv[0])):
        if grp == "D":
            cc = "GAS"
        else:
            cc = "gws" if op in no_gas else ("gws→GAS" if op in gas_ok else "gws")
        if grp == "D":
            chat = "defer→shell"
        elif op in mcp_tools:
            chat = "mcp:" + mcp_tools[op][0]
        elif op in defer_write:
            chat = "defer→Code/Cowork"
        else:
            chat = "—"
        rows.append((op, grp, "LÔ" if grp == "C" else "-", cc, chat))
    if getattr(a, "json", False):
        print(json.dumps({"gws": gws_av, "pinned": tr.gws_bridge.PINNED_VERSION,
                          "routing": [dict(op=o, group=g, confirm=c, code_cowork=cc, chat=ch)
                                      for o, g, c, cc, ch in rows]}, ensure_ascii=False, indent=2))
    else:
        av = "✓" if gws_av.get("ok") else "✗"
        print(f"[transport] gws {av} v{gws_av.get('version')} (pin {tr.gws_bridge.PINNED_VERSION}) auth={gws_av.get('auth_method')}")
        print(f"  {'op':14} {'nhóm':5} {'confirm':8} {'Code/Cowork':12} Chat")
        for o, g, c, cc, ch in rows:
            print(f"  {o:14} {g:5} {c:8} {cc:12} {ch}")
        print("  Nhóm: A=read · B=write an toàn · C=write rủi ro (confirm THEO LÔ) · D=business-logic (GAS độc quyền; Chat defer)")
        print("  Code/Cowork: gws PRIMARY, 'gws→GAS'=có fallback GAS ồn ào khi gws chết; 'gws'=không fallback (vd upload binary).")
    return 0


def _extract_dieu_text(text, dieu_no, max_chars: int = 4000):
    """Trích NGUYÊN VĂN 1 Điều (từ 'Điều N.' tới 'Điều kế') — cho E1 so quy phạm. None nếu không thấy."""
    lines = text.splitlines()
    want, start = str(dieu_no), None
    for i, ln in enumerate(lines):
        m = _DIEU_HEAD_RE.match(ln)
        if m and m.group(1) == want:
            start = i
            break
    if start is None:
        return None
    out = [lines[start]]
    for ln in lines[start + 1:]:
        if _DIEU_HEAD_RE.match(ln):
            break
        out.append(ln)
    t = "\n".join(out).strip()
    return (t[:max_chars] + " …[cắt]") if len(t) > max_chars else t


def _fetch_amending_provision(row, entries, config):
    """Trích điều của LUẬT SỬA (online): amending_sohieu → GDoc corpus → _extract_dieu_text(Điều từ vitri)."""
    sh = (row.get("amending_sohieu") or "").replace("-", "/")
    m = re.search(r"Điều\s+(\d+[a-zđ]?)", row.get("amending_vitri") or "")
    if not m:
        return None
    hits = resolve_identity(sh, entries, max_hits=1)
    if not hits:
        return f"(luật sửa {sh} CHƯA có trong corpus — QT-5)"
    txt = _read_doc_text(_entry_drive_id(hits[0][0]), config)
    if not txt:
        return f"(không đọc được {sh})"
    return _extract_dieu_text(txt, m.group(1)) or f"(không thấy Điều {m.group(1)} trong {sh})"


def cmd_overlap(a) -> int:
    """E1+ SO QUY PHẠM: mỗi điểm giao thoa (footnote amendment) của VBHN canonical → trích NGUYÊN VĂN Điều bị sửa
    (bản hợp nhất) + cờ PENDING/đa-luật-sửa/nguồn-thiếu; --with-source trích thêm điều của luật sửa (online).
    Skill cấp nguyên văn 2 phía; Claude phán OVERLAP/CONFLICT (KHÔNG RAG sinh)."""
    from collections import Counter
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception:
        entries = []
    if getattr(a, "text_file", None):
        text = Path(a.text_file).read_text(encoding="utf-8", errors="replace")
    elif getattr(a, "target", None):
        gid = a.target
        if "/" in a.target or not re.fullmatch(r"[A-Za-z0-9_\-]{20,}", a.target):
            hits = resolve_identity(a.target, entries, max_hits=1)
            if hits:
                gid = _entry_drive_id(hits[0][0])
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        text = _read_doc_text(gid, getattr(a, "config", None))
    else:
        print("[overlap] cần <gdocId|số hiệu> hoặc --text-file", file=sys.stderr)
        return 2
    if not text:
        print("[overlap] không đọc được canonical text", file=sys.stderr)
        return 2
    fn = resolve_footnote_amendments(text, entries=entries)
    rows = fn["dieu_level_amendment_map"]
    dcount = Counter(r["dieu"] for r in rows if r.get("dieu"))
    recs = []
    for r in rows:
        d = r.get("dieu")
        rec = {"dieu": d, "khoan": r.get("khoan"), "amending_sohieu": r.get("amending_sohieu"),
               "amending_vitri": r.get("amending_vitri"), "hieu_luc": r.get("hieu_luc"),
               "pending_effect": r.get("pending_effect", False), "multi_amender": dcount.get(d, 0) > 1,
               "def_missing": r.get("def_missing", False),
               "vbhn_text": _extract_dieu_text(text, d) if d else None}
        if getattr(a, "with_source", False) and r.get("amending_sohieu"):
            rec["amending_text"] = _fetch_amending_provision(r, entries, getattr(a, "config", None))
        recs.append(rec)
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "footnote_count": fn["footnote_count"],
                          "pending_effect_count": fn["pending_effect_count"], "overlaps": recs},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"== E1 SO QUY PHẠM · {len(recs)} điểm giao thoa · pending={fn['pending_effect_count']} ==")
    print("  (Skill cấp NGUYÊN VĂN 2 phía; Claude đọc + phán OVERLAP/CONFLICT — KHÔNG RAG sinh)\n")
    for rec in recs:
        flags = []
        if rec["pending_effect"]:
            flags.append("⏳PENDING")
        if rec["multi_amender"]:
            flags.append("⚠ĐA-LUẬT-SỬA")
        if rec["def_missing"]:
            flags.append("nguồn-?")
        fl = (" [" + ", ".join(flags) + "]") if flags else ""
        kh = (" K" + rec["khoan"]) if rec["khoan"] else ""
        print(f"[Điều {rec['dieu']}{kh}] ← {rec['amending_sohieu'] or '?'} ({rec['amending_vitri'] or ''}) "
              f"HL {rec['hieu_luc'] or '?'}{fl}")
        if rec["vbhn_text"]:
            print("  ─ Nguyên văn (VBHN hợp nhất):")
            for ln in rec["vbhn_text"].splitlines():
                print("    " + ln)
        if rec.get("amending_text"):
            print(f"  ─ Nguyên văn luật sửa ({rec['amending_sohieu']}):")
            for ln in rec["amending_text"].splitlines():
                print("    " + ln)
        print()
    return 0
