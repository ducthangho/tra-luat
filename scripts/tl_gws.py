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
from pathlib import Path  # v1.35.48 r212 (đo 26-07: `import tl_gws` trần → _bundle_meta_blocks_push trả False
# dù thư mục CÓ BUNDLE_META.json) — `Path` là tên duy nhất trong nhóm stdlib còn phải chờ bind(), nên guard
# ADR-0001 nuốt NameError và fail-OPEN ở mọi đường dispatch không qua build_parser. Đúng bẫy mà chính chú
# thích trên đã cảnh báo, chỉ là sót tên.

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
    # → gws CLI vẫn chạy tốt trong khi file cred hết hạn. Làm mới: `gws auth login` rồi `tl secrets-set --gws --nlm`
    # (cập nhật bundle để Cowork cũng nhận cred mới; WP710: `--nlm` bắt buộc khi bundle mang nlm_auth).
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
                               "(invalid_grant) → chạy `gws auth login` trên máy user rồi `tl secrets-set --gws --nlm` "
                               "(v1.33.1: 1 lệnh làm tươi CẢ bundle LẪN file public TẠI CHỖ — Chat/Cowork tự nhận, "
                               "không bake lại; WP710: `--nlm` bắt buộc khi bundle mang nlm_auth, cần jar nlm + canary "
                               "dương ở máy này; máy không có jar ⇒ chỉ-public: `tl gws-auth-stage`). ⚠ Fallback GAS chỉ cứu DOWNLOAD file; op ĐỌC TEXT "
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


# r208b 3.2 (báo cáo 25-07): thông điệp auth của doctor cũng phải chỉ ĐÚNG đường. Đọc thẳng
# `nlm_cli` THẬT (không qua `_imp` — selftest tiêm module giả cho canary, module giả không mang
# hằng này). Bản dự phòng cuối chỉ dùng khi không nạp nổi adapter; drift-lock trong selftest bắt
# MỌI biến thể phải nêu đúng thứ tự nlm-auth-load → nlm-auth-pull → nlm login.
_AUTH_FIX_FALLBACK_GWS = ("🔴 AUTH hết hạn: `tl nlm-auth-load` → `tl nlm-auth-pull` (cần TL_MASTER_KEY) "
                          "→ `nlm login` (tương tác) · ⚠ ĐANG TRONG LƯỢT RÀ HỒ SƠ (RASOAT_HOSO_LOOP §4b): "
                          "KHÔNG tự chạy (1)/(2) — chuyển chế độ không-NLM và ĐI TIẾP")   # r213 ĐỢT 5: câu trừ ngữ cảnh


def _auth_fix_hint_short() -> str:
    try:
        import importlib as _il
        return _il.import_module("nlm_cli").AUTH_FIX_HINT_SHORT
    except Exception:  # noqa: BLE001
        return _AUTH_FIX_FALLBACK_GWS


_NLM_CANARY_KNOWN_KEYS = ("id", "notebook_id", "title", "name", "data", "ok", "error")


_NLM_CANARY_MAX_DEPTH = 64     # = MaxDepth mặc định của System.Text.Json (đo: 64 mức lồng nhận, 65 ném)

# WP714 vòng 4 (Codex lượt 3, lớp `stage-canary-true-khi-than-rong-hoac-sai-id`): title/name "trắng" theo MỘT bảng
# TƯỜNG MINH, không theo `str.strip()` (Python) hay `String.IsNullOrWhiteSpace` (.NET) — hai tập ấy KHÁC nhau (đo:
# U+001C–U+001F là khoảng trắng với Python, không với .NET ⇒ title "\u001c" từng Python=âm / PS=dương). Bảng = mọi
# ký tự `str.isspace()` của Python 3.11 (tập .NET là tập con của nó) cộng các ký tự định dạng độ rộng 0 (U+180E,
# U+200B–U+200D, U+2060, U+FEFF). Wrapper PS giữ ĐÚNG danh sách này ở `$CanaryBlankCodePoints`; selftest
# `wp714_canary_bang_trang_khop_ps` so hai danh sách theo từng số. Title chỉ gồm ký tự trong bảng (kể cả rỗng) = trắng.
_NLM_CANARY_BLANK_CODEPOINTS = (
    0x0009, 0x000A, 0x000B, 0x000C, 0x000D, 0x001C, 0x001D, 0x001E, 0x001F, 0x0020, 0x0085, 0x00A0, 0x1680,
    0x180E, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x200B,
    0x200C, 0x200D, 0x2028, 0x2029, 0x202F, 0x205F, 0x2060, 0x3000, 0xFEFF,
)
_NLM_CANARY_BLANK = frozenset(_NLM_CANARY_BLANK_CODEPOINTS)


def _nlm_canary_blank(s: str) -> bool:
    """Chuỗi chỉ gồm ký tự của `_NLM_CANARY_BLANK_CODEPOINTS` (kể cả chuỗi rỗng) = không có tên."""
    return all(ord(ch) in _NLM_CANARY_BLANK for ch in s)


def _nlm_canary_json_strict(text):
    """WP714 (cross-review PR #714 lớp P1 `stage-canary-true-khi-than-rong-hoac-sai-id`): parse JSON và TỪ CHỐI
    khoá trùng ở MỌI mức — `{"id":"KHAC","id":"<đúng>"}` là trả lời hai nghĩa, `json.loads` âm thầm lấy vế sau.
    WP714 vòng 3 (Codex lượt 2, cùng lớp): `json.loads` mặc định NHẬN cả thứ KHÔNG phải JSON chuẩn — đo:
    `NaN`/`Infinity`/`-Infinity` thành float rồi canary DƯƠNG, upload=1 ở cả ba lệnh. Hợp đồng là JSON RFC 8259
    và phải KHỚP bộ đọc của wrapper PS (`System.Text.Json.JsonDocument`, đo cùng đầu vào trên pwsh 7.4.6):
      · hằng ngoài JSON (`NaN`/`Infinity`/`-Infinity`): PS ném lúc parse ⇒ ở đây `parse_constant` ném;
      · số hợp lệ cú pháp nhưng TRÀN double (`1e400`, số nguyên 400 chữ số): Python ra `inf`/int khổng lồ, PS
        `TryGetDouble` ra ±∞ ⇒ cả hai phía TỪ CHỐI số không hữu hạn. Thử bằng `float()` TRƯỚC `int()` nên không
        phụ thuộc giới hạn `int_max_str_digits` (biến môi trường đổi được giới hạn ấy);
      · surrogate LẺ (`"\\ud800"` dạng thoát) ở khoá hoặc giá trị: Python nhận, PS `GetString()`/`.Name` ném
        ⇒ từ chối ở cả hai.
      · lồng quá 64 mức: PS ném ⇒ ở đây cũng từ chối (Python tự nhận tới ~1000 mức).
    BOM đầu chuỗi, dấu phẩy thừa, chú thích, ký tự điều khiển thô, khoảng trắng ngoài 4 ký tự JSON: hai HÀM đọc
    cùng từ chối khi nhận cùng một chuỗi (đo) — giữ nguyên, có ca khoá trong selftest.
    PHẠM VI của lời khai trên là HÀM ĐỌC, không phải đường tiến trình. Văn bản hàm này nhận đã qua `nlm_cli._run`
    (UTF-8, byte hỏng ⇒ U+FFFD, đổi `\r\n`/`\r`, `_strip_keyring` cắt dòng bằng `splitlines` và bỏ dòng nhiễu
    keyring). Lượt 3 đo được wrapper PS khi ấy đọc stdout bằng StreamReader — BỎ BOM — nên BOM qua tiến trình
    thật từng dương ở wrapper. Từ vòng 4 wrapper đọc BYTE và áp đúng phép biến đổi ấy (`ConvertTo-StageText`);
    selftest `wp714_canary_van_chuyen_khop_nlm_cli` khoá các bảng nó chép. Phép đo qua tiến trình thật chỉ có
    trên Linux/pwsh 7.4.6/Python 3.11; Windows native và CLI `nlm` thật CHƯA đo."""
    import math   # cục bộ: không dựa vào namespace dùng chung của tl.py
    def _no_dup(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                raise ValueError("CANARY_DUPLICATE_KEY")
            seen.add(k)
        return dict(pairs)

    def _no_constant(_name):
        raise ValueError("CANARY_NON_JSON_CONSTANT")

    def _finite_float(s):
        v = float(s)
        if not math.isfinite(v):
            raise ValueError("CANARY_NUMBER_NOT_FINITE")
        return v

    def _finite_int(s):
        if not math.isfinite(float(s)):
            raise ValueError("CANARY_NUMBER_NOT_FINITE")
        return int(s)

    body = json.loads(text, object_pairs_hook=_no_dup, parse_constant=_no_constant,
                      parse_float=_finite_float, parse_int=_finite_int)
    stack = [(body, 1)]
    while stack:                                      # duyệt lặp (không đệ quy) — kiểm độ sâu + surrogate lẻ
        node, depth = stack.pop()
        if isinstance(node, (dict, list)):
            if depth > _NLM_CANARY_MAX_DEPTH:
                raise ValueError("CANARY_TOO_DEEP")
            items = list(node.items()) if isinstance(node, dict) else [(None, v) for v in node]
            for k, v in items:
                if isinstance(k, str) and _has_lone_surrogate(k):
                    raise ValueError("CANARY_LONE_SURROGATE")
                stack.append((v, depth + 1))
        elif isinstance(node, str) and _has_lone_surrogate(node):
            raise ValueError("CANARY_LONE_SURROGATE")
    return body


def _has_lone_surrogate(s: str) -> bool:
    """Cặp surrogate hợp lệ dạng thoát đã được `json` gộp thành MỘT code point; còn lại trong khoảng
    U+D800–U+DFFF nghĩa là surrogate lẻ — thứ .NET không đọc thành chuỗi được."""
    return any(0xD800 <= ord(ch) <= 0xDFFF for ch in s)


def _nlm_canary_level_ok(obj) -> bool:
    """Một mức đối tượng: khoá đã biết chỉ được đúng hoa/thường (`ID`, `Title` = mơ hồ); `ok` có mặt thì phải
    đúng `True`; `error` có mặt thì chỉ được null/false/"". Không phải dict = không dương."""
    if not isinstance(obj, dict):
        return False
    for k in obj:
        if isinstance(k, str) and k.lower() in _NLM_CANARY_KNOWN_KEYS and k not in _NLM_CANARY_KNOWN_KEYS:
            return False
    if "ok" in obj and obj["ok"] is not True:
        return False
    if "error" in obj and not (obj["error"] is None or obj["error"] is False or obj["error"] == ""):
        return False                                  # cùng luật với Get-CanaryLevel của wrapper PS
    return True


def _nlm_canary_body_ok(r, notebook_id: str) -> tuple[bool, str]:
    """WP710 r4/g3 + WP714 (cross-review PR #713/#714, lớp `stage-canary-true-khi-than-rong-hoac-sai-id`): rc=0 của
    `nlm notebook get` KHÔNG phải bằng chứng. Phán xét trên STDOUT THÔ (`r["stdout"]`), KHÔNG trên `raw` của
    `nlm_cli.notebook_get` — hàm ấy bóc phần tử ĐẦU của mảng và vứt phần còn lại, nên `[đúng, sai]` từng thành dương
    (đo PR #714: upload=1 kể cả --force). DANH SÁCH CHO PHÉP — dương CHỈ KHI có ĐÚNG MỘT đối tượng notebook:
      · JSON hợp lệ, không khoá trùng ở mức nào;
      · mức đỉnh là đối tượng, hoặc mảng có ĐÚNG MỘT phần tử là đối tượng;
      · đối tượng không có `id`/`notebook_id` mà có `data` là đối tượng ⇒ bóc `data` MỘT lần (khuôn wrapper PS);
      · mỗi mức đi qua: khoá đã biết đúng hoa/thường, `ok` (nếu có) là `True`, `error` (nếu có) rỗng;
      · có ít nhất một trong `id`/`notebook_id`, và MỌI khoá id có mặt là chuỗi BẰNG ĐÚNG id đang probe;
      · có ít nhất một trong `title`/`name`, và MỌI khoá ấy có mặt là chuỗi KHÔNG trắng theo bảng
        `_NLM_CANARY_BLANK_CODEPOINTS` (không theo `strip()`; xem bảng).
    Mọi dạng khác — kể cả kiểu lạ, hai id mâu thuẫn, mảng nhiều phần tử dù đều đúng — KHÔNG dương. Trả MÃ CỐ ĐỊNH."""
    text = r.get("stdout") if isinstance(r, dict) else None
    if not isinstance(text, str) or not text.strip():
        return False, "CANARY_BODY_ABSENT"
    try:
        body = _nlm_canary_json_strict(text)
    except (ValueError, TypeError, RecursionError):
        return False, "CANARY_BODY_NOT_JSON"
    if isinstance(body, list):
        if len(body) != 1:
            return False, "CANARY_BODY_AMBIGUOUS"
        body = body[0]
    if not _nlm_canary_level_ok(body):
        return False, "CANARY_BODY_AMBIGUOUS"
    if not ({"id", "notebook_id"} & set(body)) and "data" in body:
        body = body["data"]                           # cùng phép bóc `data` như wrapper PowerShell, MỘT lần
        if not _nlm_canary_level_ok(body):
            return False, "CANARY_BODY_AMBIGUOUS"
    ids = [body[k] for k in ("id", "notebook_id") if k in body]
    if not ids or not all(isinstance(v, str) and v == notebook_id for v in ids):
        return False, "CANARY_ID_MISMATCH"
    titles = [body[k] for k in ("title", "name") if k in body]
    if not titles or not all(isinstance(v, str) and not _nlm_canary_blank(v) for v in titles):
        return False, "CANARY_BODY_INCOMPLETE"
    return True, "CANARY_BODY_OK"


def _nlm_canary_raw_get(nc, notebook_id: str, timeout: int) -> dict:
    """WP714: gọi `nlm notebook get <id> -j` qua `nlm_cli._run` để GIỮ STDOUT THÔ cho `_nlm_canary_body_ok`
    (`notebook_get` làm mất phần tử thứ hai trở đi — tệp ấy ngoài write set nên chặn ở đây). Nhánh rc≠0 giữ ĐÚNG
    phép gắn `auth_hint` của `nlm_cli._run_json` để vòng retry/EXPIRED của `_nlm_auth_alive` không đổi nghĩa."""
    rc, out, err = nc._run(["notebook", "get", notebook_id, "-j"], timeout=timeout)
    if rc != 0:
        low = (str(err) + str(out)).lower()
        auth = any(t in low for t in ("auth", "401", "login", "unauthor", "credential"))
        return {"ok": False, "rc": rc, "error": f"nlm rc={rc}: {(err or out)[:300]}",
                "auth_hint": getattr(nc, "AUTH_FIX_HINT", "auth") if auth else None}
    return {"ok": True, "stdout": out}


# WP714 (lớp P1 `stage-error-output-leaks-credential`): mã CỐ ĐỊNH duy nhất được in ra từ cổng stage. Thông điệp
# của `_nlm_auth_alive` mang stderr/stdout THÔ của tiến trình con (có thể chứa cookie) — không bao giờ in nó.
_NLM_PROBE_CODES = ("NLM_CLI_IMPORT_FAIL", "NO_BINARY", "NO_NOTEBOOK", "AUTH_EXPIRED", "PROBE_EXC",
                    "CANARY_BODY_ABSENT", "CANARY_BODY_NOT_JSON", "CANARY_BODY_AMBIGUOUS", "CANARY_ID_MISMATCH",
                    "CANARY_BODY_INCOMPLETE")


def _nlm_probe_code(alive, msg) -> str:
    """(alive, msg) của `_nlm_auth_alive` → MỘT mã trong tập cố định. Chỉ so TIỀN TỐ/khung do mã ta tự viết;
    văn bản con có giả mã nào thì kết quả vẫn là một chuỗi cố định, không phải văn bản con."""
    if alive is True:
        return "LIVE_OK"
    s = msg if isinstance(msg, str) else ""
    for code in _NLM_PROBE_CODES:
        if s.startswith(code) or s.startswith(f"PROBE_INCONCLUSIVE ({code})"):
            return code
    if s.startswith("PROBE_INCONCLUSIVE (transient"):
        return "PROBE_TRANSIENT"
    return "PROBE_INCONCLUSIVE"


def _safe_exc(exc) -> str:
    """WP714: lỗi chỉ được in bằng TÊN LỚP (không `str(e)` — thông điệp có thể mang đường dẫn/token/thân HTTP)."""
    name = type(exc).__name__
    return name if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", name or "") else "Exception"


def _nlm_auth_alive(notebook_id: str, timeout: int = 30,
                    require_notebook_body: bool = False) -> tuple[bool | None, str]:
    """M1 (v1.33.35 — log rà 45 Luật LIVE: nlm-auth-load/doctor/`nlm login --check` báo XANH [rc=0] nhưng
    nlm-get/list/reconcile LIVE đều 'Authentication expired'): CANARY LIVE THẬT cho NLM — gọi 1 lệnh chạm
    server (`nlm notebook get` base notebook) thay vì tin tuổi file / `login --check` (không chứng minh cookie
    Google session còn sống). Tách khỏi `_nlm_auth_age_days` (tuổi file = KHÔNG bằng chứng auth sống).
    Trả (alive, msg): True=auth sống · False=EXPIRED (auth_hint) · None=không kết luận được (thiếu binary/
    mạng/timeout — KHÔNG hạ đỏ oan). Rẻ (1 notebook get ~2s), chỉ gọi khi doctor KHÔNG --offline."""
    try:
        nc = _imp("nlm_cli")
    except Exception as e:  # noqa: BLE001
        return None, f"NLM_CLI_IMPORT_FAIL: {type(e).__name__}"
    if not nc.nlm_available():
        return None, "NO_BINARY: nlm CLI chưa trên PATH (không probe được)"
    if not notebook_id:
        return None, "NO_NOTEBOOK: thiếu base notebook id để probe"
    # MERGE bundle-45c (v1.33.47 — log phiên rà 34 Luật nhánh kia): probe LẦN ĐẦU có thể fail TRANSIENT
    # (network_error / ClientAuthenticationError thoáng qua khi cookie thực SỐNG — nlm-get OK ngay sau) →
    # trước đây doctor kết luận AUTH_EXPIRED rc=2 oan ngay lần đầu. Retry ×3 backoff 1.5s/3s.
    # TINH CHỈNH so bundle (GIỮ giá trị M1): sau 3 lần, auth_hint BỀN → EXPIRED (RED) — bundle xếp
    # 'clientauthentication' vào transient và check transient TRƯỚC auth_hint → cookie chết THẬT (chữ ký
    # ClientAuthenticationError bền, đúng ca v1.33.39) sẽ thành INCONCLUSIVE vĩnh viễn = tái false-green
    # mà M1 sinh ra để diệt. Transient thật đã có 3 cơ hội thành công; bền qua 3 lần + auth_hint = chết thật.
    import time as _t
    _TRANSIENT = ("network", "reach", "timeout", "temporarily", "503", "502", "connection")
    r = {}
    for _att in range(3):
        try:
            # WP714: cổng stage đọc STDOUT THÔ (`notebook_get` vứt phần tử thứ 2+ của mảng); doctor giữ đường cũ.
            r = (_nlm_canary_raw_get(nc, notebook_id, timeout) if require_notebook_body
                 else nc.notebook_get(notebook_id, timeout=timeout))
        except Exception as e:  # noqa: BLE001
            r = {"ok": False, "error": f"PROBE_EXC: {type(e).__name__}: {str(e)[:120]}"}
        if r.get("ok"):
            if require_notebook_body:                 # WP710: cổng stage đòi THÂN đúng notebook, không chỉ rc=0
                _body_ok, _body_msg = _nlm_canary_body_ok(r, notebook_id)
                if not _body_ok:
                    return None, f"PROBE_INCONCLUSIVE ({_body_msg})"
                return True, "LIVE OK (canary body)"
            return True, f"LIVE OK (base notebook {int(r.get('source_count') or 0)} nguồn)"
        if _att < 2:
            _errl = str(r.get("error") or "").lower()
            if r.get("auth_hint") or "clientauthentication" in _errl or any(s in _errl for s in _TRANSIENT):
                _t.sleep(1.5 * (_att + 1))   # backoff 1.5s → 3s
                continue
        break
    # sau retry — auth_hint BỀN → EXPIRED (RED, ưu tiên trước transient); mạng/transient → KHÔNG kết luận
    if r.get("auth_hint"):
        # r208b 3.2: TRƯỚC đây doctor chỉ hô `nlm login` (tương tác — vô dụng ở Cowork/headless), đúng
        # thông điệp đã ngốn nhiều bước của người vận hành 25-07. Nay nêu ĐỦ chuỗi đúng thứ tự.
        return False, ("AUTH_EXPIRED: nlm cookie hết hạn (bền qua 3 lần probe) — " + _auth_fix_hint_short()
                       + "; sau khi có cookie tươi thì `tl nlm-auth-stage`/`secrets-set --nlm` để đẩy vào bundle")
    _errl = str(r.get("error") or "").lower()
    if any(s in _errl for s in _TRANSIENT):
        return None, f"PROBE_INCONCLUSIVE (transient/mạng sau 3 lần — KHÔNG kết luận auth; thử `tl nlm-auth-load` rồi probe lại): {str(r.get('error') or '?')[:140]}"
    return None, f"PROBE_INCONCLUSIVE (không phải auth): {str(r.get('error') or '?')[:160]}"


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
        info["issues"].append(f"CRED CHẾT (canary token): {_amsg} → `gws auth login` rồi `tl secrets-set --gws --nlm` "
                              "(1 lệnh làm tươi CẢ bundle + public tại chỗ; `--nlm` cần jar + canary dương ở máy này; "
                              "máy không có jar ⇒ chỉ-public: `tl gws-auth-stage`). "
                              "⚠ đọc Drive (extract/corpus-audit) CHẾT tới khi refresh "
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
            print("  ⚠ CRED CHẾT: op ĐỌC Drive sẽ hỏng tới khi `gws auth login` + `tl secrets-set --gws --nlm` "
                  "(máy không có jar nlm ⇒ `tl gws-auth-stage`, chỉ đường public); "
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


def _nlm_sync_authjson_from_profile(base):
    """M1b (v1.33.38 — ROOT CAUSE 'stage cookie tươi mà Cowork vẫn Authentication expired'): nlm CLI MỚI ghi
    cookie vào `profiles/default/{cookies.json,metadata.json}` (nguồn authoritative — local canary đọc file này
    nên báo SỐNG) NHƯNG KHÔNG cập nhật `auth.json` root (legacy). → auth.json STALE (cookie hết hạn) trong khi
    profile TƯƠI. `_nlm_auth_files` gói CẢ auth.json stale; Cowork nạp về, nlm CLI ở đó đọc trúng auth.json stale
    → 'Authentication expired' dù đã stage sau `nlm login` mới. Fix: DỰNG LẠI auth.json từ profile TƯƠI trước khi
    gói (cookie format khớp CHÍNH XÁC: domain/expires/name/value/…). Trả text auth.json mới, hoặc None nếu profile
    không đủ dữ liệu / KHÔNG tươi hơn auth.json (giữ nguyên hành vi cũ cho nlm CLI đời cũ chỉ dùng auth.json)."""
    import time as _t
    ck_p = os.path.join(base, "profiles", "default", "cookies.json")
    md_p = os.path.join(base, "profiles", "default", "metadata.json")
    aj_p = os.path.join(base, "auth.json")
    if not (os.path.exists(ck_p) and os.path.exists(md_p)):
        return None
    # chỉ ghi đè khi profile TƯƠI HƠN-hoặc-BẰNG auth.json (mtime) — tránh hạ cấp nếu auth.json mới hơn (đời cũ)
    if os.path.exists(aj_p) and os.path.getmtime(ck_p) < os.path.getmtime(aj_p):
        return None
    try:
        cookies = json.load(open(ck_p, encoding="utf-8"))
        meta = json.load(open(md_p, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    if not isinstance(cookies, list) or not cookies:
        return None
    auth = {"cookies": cookies, "csrf_token": meta.get("csrf_token"),
            "session_id": meta.get("session_id"), "build_label": meta.get("build_label"),
            "extracted_at": _t.time()}
    return json.dumps(auth, ensure_ascii=False)


def _nlm_auth_files():
    """Thu file auth nlm (profile 'default') từ ~/.notebooklm-mcp-cli → {relpath: text}. SECRET (cookies Google).
    Cho `secrets-stage` gói vào bundle .enc → Cowork ghi lại → nlm chạy headless không cần `nlm login`.
    M1b (v1.33.38): auth.json root có thể STALE (nlm CLI mới chỉ ghi profiles/default) → dựng lại từ profile TƯƠI."""
    base = os.path.expanduser("~/.notebooklm-mcp-cli")
    out = {}
    for rel in _NLM_AUTH_RELS:
        p = os.path.join(base, *rel.split("/"))
        if os.path.exists(p):
            try:
                out[rel] = open(p, encoding="utf-8").read()
            except Exception:
                pass
    synced = _nlm_sync_authjson_from_profile(base)   # auth.json TƯƠI dựng từ profile (nếu profile mới hơn)
    if synced is not None:
        out["auth.json"] = synced
    return out


def _refresh_nlm_auth():
    """[CODE] Best-effort làm tươi cookie TRƯỚC khi gói, cùng lệnh wrapper WP710 gọi: `nlm auth refresh`.
    WP727: thay `nlm login --check` (lệnh KIỂM, false-green — không phải lệnh làm tươi). Trả True khi lệnh rc 0;
    giá trị ấy KHÔNG phải bằng chứng sống và KHÔNG được người gọi dùng làm cổng — cổng là canary LIVE chạy SAU
    (`_nlm_files_after_live_canary`). Không in đầu ra con (có thể chứa cookie)."""
    import shutil as _sh, subprocess as _sp
    nx = _sh.which("nlm") or os.path.expanduser("~/.local/bin/nlm")
    if not (os.path.exists(nx) or _sh.which("nlm")):
        return False
    try:
        p = _sp.run([nx, "auth", "refresh"], stdout=_sp.DEVNULL, stderr=_sp.DEVNULL, timeout=120)
        return p.returncode == 0
    except _sp.TimeoutExpired:  # chỉ con TRỰC TIẾP bị giết; trình duyệt headless có thể còn ghi hồ sơ ⇒ người gọi DỪNG
        return None
    except Exception:  # noqa: BLE001
        return False


def _refresh_treo(tag):
    print(f"[{tag}] ✗ `nlm auth refresh` quá 120s — trình duyệt con có thể còn ghi hồ sơ; KHÔNG canary, KHÔNG gói. "
          "Chạy lại khi nó đã dừng.", file=sys.stderr)
    return 2


_NLM_LV_JITTER_S = 120.0     # dung sai đồng hồ (NTP) — mốc "tương lai" trong khoảng này = vừa xác thực xong


def _nlm_lv_age_seconds(lv):
    """PURE (v1.35.65): tuổi (giây) từ `metadata.json.last_validated`, hoặc None nếu mốc KHÔNG DÙNG ĐƯỢC.

    Bug đo 29-07-2026 (sandbox UTC, jar stage từ máy UTC+7): `last_validated` do nlm ghi theo GIỜ CỦA
    MÁY GHI và là ISO **NAIVE** (`2026-07-29T18:04:42`, không tzinfo). Trừ thẳng `datetime.now()` của
    máy ĐỌC = trộn hai múi giờ → lệch 465,6' → `_nlm_auth_age_days` trả **ÂM 0,3 ngày**, `nlm-auth-load`
    in "~-0 ngày tuổi". Sai số bị chặn bởi biên múi giờ thực (UTC-12..UTC+14 ⇒ ≤14h ≈ 0,58 ngày) nên
    KHÔNG lật nổi ngưỡng 14 ngày ở giữa dải; cái ĐẮT nằm ở chỗ khác: (a) in tuổi ÂM là sai hiển nhiên,
    (b) SÁT ngưỡng thì nuốt mất cảnh báo, (c) NẶNG NHẤT — `_nlm_auth_load_downgrade` so tuổi bundle
    (mốc máy STAGE ghi) với tuổi jar cục bộ (mốc máy NÀY ghi): hai gốc thời gian khác nhau ⇒ bundle từ
    máy đi trước LUÔN ra tuổi âm ⇒ luôn "bundle tươi hơn" ⇒ chốt chống hạ cấp r208c 3.1 mở toang.

    Quy tắc: có tzinfo → so tuyệt đối (đúng ở mọi máy); naive & tuổi ≥ 0 → DÙNG (cùng máy: chính xác;
    khác múi: chỉ ĐỘI LÊN ≤14h — lệch về phía cảnh báo SỚM, an toàn) nên mốc 2026-07-05 «ưu tiên
    last_validated» giữ nguyên; naive & mốc ở TƯƠNG LAI quá dung sai đồng hồ → mốc vô nghĩa với đồng hồ
    máy này ⇒ trả None để caller rơi xuống `extracted_at` (epoch — tz-safe), KHÔNG bịa số âm."""
    from datetime import datetime as _dt
    try:
        t = _dt.fromisoformat(str(lv))
    except (TypeError, ValueError):
        return None
    age = ((_dt.now(t.tzinfo) if t.tzinfo else _dt.now()) - t).total_seconds()
    if age >= 0:
        return age
    return 0.0 if age >= -_NLM_LV_JITTER_S else None


def _nlm_auth_age_days(nlm_auth):
    """Tuổi cookie (ngày) — cảnh báo cookie cũ sắp hết hạn (~2–4 tuần).

    Phát hiện 2026-07-05 (refresh token thật): `nlm login --force` re-auth THÀNH CÔNG (account xác nhận,
    session mới) nhưng root `auth.json.extracted_at` KHÔNG được nlm CLI bản mới ghi lại nữa (profile-based
    storage) → age vẫn báo ~19 ngày dù vừa refresh, khiến cảnh báo LUÔN SAI sau khi đã làm đúng việc user được
    khuyên làm. Tín hiệu tươi THẬT nằm ở `profiles/default/metadata.json.last_validated` (ISO, cập nhật mỗi lần
    `nlm login`/`--check` xác thực OK) — ưu tiên đọc đó; fallback `auth.json.extracted_at` (epoch) cho bundle cũ
    không có metadata.json (tương thích ngược).

    v1.35.65: mốc naive lệch múi giờ KHÔNG còn cho ra tuổi âm — xem `_nlm_lv_age_seconds`."""
    import time as _t
    try:
        meta = json.loads(nlm_auth.get("profiles/default/metadata.json", "{}"))
        lv = meta.get("last_validated")
        if lv:
            _a = _nlm_lv_age_seconds(lv)      # None = mốc ở tương lai (lệch múi giờ) → rơi xuống epoch
            if _a is not None:
                return _a / 86400.0
    except Exception:
        pass
    try:
        ts = json.loads(nlm_auth.get("auth.json", "{}")).get("extracted_at")
        return (_t.time() - float(ts)) / 86400.0 if ts else None
    except Exception:
        return None


_NLM_COOKIE_WARN_DAYS = 14


def _nlm_cookie_age_note(age):
    """Log Cowork 2026-07-05 (A): cookie ~19 ngày nạp IM LẶNG (chỉ in tuổi như info) — không ai được nhắc
    re-stage cho tới khi auth chết giữa phiên. Cookie sống ~2–4 tuần → từ _NLM_COOKIE_WARN_DAYS trả chuỗi
    ⚠ CHỦ ĐỘNG để mọi đường nạp/gói (auth-load/auth-pull/stage/bootstrap/doctor) cùng cảnh báo; rỗng khi
    cookie còn trẻ hoặc không rõ tuổi."""
    if age is None or age < _NLM_COOKIE_WARN_DAYS:
        return ""
    return (f" ⚠ cookie ~{age:.0f} NGÀY tuổi (sống ~2–4 tuần) — rủi ro hết hạn giữa phiên; re-stage sớm: "
            "trên máy giữ hồ sơ trình duyệt gốc chạy `pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath <config>` (refresh → canary → stage).")


def _nlm_canary_notebook(entry_notebook: str | None) -> str:
    """WP714 (lớp P2 `trusted-notebook-overwritten-by-stage-config`): notebook mà cổng canary dò, theo thứ tự tin cậy:
      1. `TL_CANARY_NOTEBOOK_ID` — ghim TƯỜNG MINH (wrapper PS đặt). `load_creds`/overlay profile KHÔNG BAO GIỜ ghi
         khoá này (bảng ánh xạ profile chỉ có `TL_NOTEBOOK_ID`…), nên nó sống qua mọi lần nạp credential — kể cả lần
         `tl.main` nạp TRƯỚC khi vào `secrets-set`/`secrets-stage` (hai lệnh không thuộc `_CREDS_LAZY_CMDS`).
      2. `TL_NOTEBOOK_ID` đo ở LỐI VÀO lệnh, TRƯỚC `load_creds` của chính lệnh (đo PR #714: token chỉ có trong config
         ⇒ `load_creds` áp `notebookId` của profile và ghi đè ID wrapper đã truyền ⇒ canary dò notebook KHÁC, rc0).
      3. `TL_NOTEBOOK_ID` hiện tại — tức `notebookId` của profile mà `load_creds` vừa áp (hành vi trước WP714 khi
         không ai ghim).
      4. notebook nền `NLM_BASE_NOTEBOOK`."""
    pin = (os.environ.get("TL_CANARY_NOTEBOOK_ID") or "").strip()
    return (pin or (entry_notebook or "").strip() or (os.environ.get("TL_NOTEBOOK_ID") or "").strip()
            or NLM_BASE_NOTEBOOK)


def _nlm_files_after_live_canary(tag: str, notebook_id: str | None = None):
    """WP710 r4/g3 — CỔNG DUY NHẤT cho MỌI đường đưa credential NLM lên Drive (`nlm-auth-stage`,
    `secrets-set --nlm` [bundle + nlm_cred.enc public], `secrets-stage` [bundle có nlm_auth]).
    Cross-review PR #713 lớp `stage-nlm-ngoai-nlm-auth-stage-khong-qua-canary` đo ở 52f32db: canary CHẾT
    mà `secrets-set --nlm` vẫn upload nlm_cred.enc + bundle, canary_calls=0 — trong khi đó là lệnh được
    hướng dẫn đặt lịch hằng ngày. Cổng ở TỪNG lệnh là danh sách sẽ thiếu; nên đây là đường DUY NHẤT lấy
    được bytes credential để stage: canary dương (`is True`, thân đúng notebook) rồi MỚI đọc jar
    (lớp P3 `ban-chup-credential-doc-truoc-canary`: blob = trạng thái SAU khi canary xác nhận).
    Không có cờ nào bỏ qua được (kể cả `--force`). Trả (files|None, rc, code): rc 4 = canary không dương,
    rc 3 = canary dương nhưng không còn jar để gói. WP714: chỉ in MÃ CỐ ĐỊNH (`_nlm_probe_code`), không bao giờ
    in thông điệp của probe (mang stderr thô của `nlm`). `notebook_id` = giá trị đã ghim ở lối vào lệnh."""
    _nb = _nlm_canary_notebook(notebook_id)
    try:
        _alive, _amsg = _nlm_auth_alive(_nb, require_notebook_body=True)
    except Exception as exc:  # noqa: BLE001
        _alive, _amsg = None, f"PROBE_EXC: {_safe_exc(exc)}"
    _code = _nlm_probe_code(_alive, _amsg)
    if _alive is not True:
        print(f"[{tag}] ✗ TỪ CHỐI STAGE credential NLM: canary chưa xác nhận sống ({_code}).", file=sys.stderr)
        print("  → Stage cookie chết = Cowork/Chat nhận cookie chết (kẹt vòng lặp). Làm tươi ở máy có hồ sơ "
              "trình duyệt gốc rồi chạy lại; không có cờ nào ép stage.", file=sys.stderr)
        return None, 4, _code
    print(f"[{tag}] ✓ verify LIVE trước stage: {_code}")
    files = _nlm_auth_files()
    if not files:
        print(f"[{tag}] ✗ canary sống nhưng không đọc được jar nlm ở máy này.", file=sys.stderr)
        return None, 3, "NO_JAR_AFTER_CANARY"
    return files, 0, _code


def _nlm_bundle_guard(tag: str, bundle: dict, confirmed) -> int:
    """WP714 (lớp P1 `stage-nlm-ngoai-nlm-auth-stage-khong-qua-canary`, phần CÒN HỞ ở PR #714): bất biến đặt ở
    PAYLOAD, ngay trước sink bundle — `nlm_auth` chỉ được rời máy nếu nó LÀ ĐÚNG đối tượng mà cổng canary vừa trả
    trong lượt này (so `is`, không so nội dung). Các nguồn khác của `nlm_auth` — bản đang có trên Drive mà
    `secrets-set` tải về rồi ghi lại, bản nằm sẵn trong config mà `secrets-stage` gói nguyên — đều chưa qua canary
    nên bị chặn (rc 4), không âm thầm gửi lại. Trả 0 khi được phép."""
    if "nlm_auth" in bundle and (confirmed is None or bundle.get("nlm_auth") is not confirmed):
        print(f"[{tag}] ✗ TỪ CHỐI: bundle mang nlm_auth KHÔNG đến từ jar vừa qua canary ở lượt này "
              "(bản tải từ Drive hoặc nằm sẵn trong config) — không gửi lại credential chưa xác nhận.", file=sys.stderr)
        print("  → `--nlm` (secrets-set) để thay bằng jar tươi đã qua canary; `--no-nlm` (secrets-stage) để bỏ hẳn "
              "nlm_auth khỏi bundle.", file=sys.stderr)
        return 4
    return 0


def _nlm_contained(tag: str, body, a) -> int:
    """WP714 (lớp P1 `stage-error-output-leaks-credential`): ranh giới lỗi của ba lệnh stage credential. Ngoại lệ lan
    ra `tl.main` sẽ in traceback kèm thông điệp (đo PR #714: lỗi upload mang sentinel ⇒ leaked=true ở cả ba lệnh).
    Ở đây chỉ in TÊN LỚP; rc 5 = dừng giữa chừng — KHÔNG bảo đảm chưa upload gì (lỗi có thể đến sau sink)."""
    try:
        return body(a)
    except Exception as exc:  # noqa: BLE001
        print(f"[{tag}] ✗ dừng vì lỗi {_safe_exc(exc)} — không in chi tiết (có thể mang credential). Kiểm Drive "
              "trước khi coi là chưa upload gì.", file=sys.stderr)
        return 5


def cmd_secrets_stage(a) -> int:
    """[CODE] Gom {webappUrl, token GAS, gws_cred, nlm_auth} → MÃ HOÁ (TL_MASTER_KEY) → upload Drive (tl_secrets.enc).
    In fileId để baked vào SECRETS_FILEID. Cred/token chỉ ở RAM, KHÔNG plaintext ra Drive/zip."""
    _entry_nb = os.environ.get("TL_NOTEBOOK_ID")      # WP714: ghim TRƯỚC load_creds của lệnh
    return _nlm_contained("secrets-stage", lambda _a: _secrets_stage_body(_a, _entry_nb), a)


def _secrets_stage_body(a, entry_notebook) -> int:
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
    nlm_confirmed = None
    if getattr(a, "no_nlm", False):
        # WP714: `--no-nlm` phải BỎ THẬT — config gói nguyên có thể mang sẵn `nlm_auth` (đo PR #714: --no-nlm vẫn
        # upload nlm_auth của config, 0 canary).
        if bundle.pop("nlm_auth", None) is not None:
            print("[secrets-stage] --no-nlm: đã bỏ nlm_auth có sẵn trong config khỏi bundle.", file=sys.stderr)
    else:
        if _refresh_nlm_auth() is None:               # làm tươi cookie trước khi gói; quá hạn ⇒ DỪNG
            return _refresh_treo("secrets-stage")
        if not _nlm_auth_files():                      # chỉ hỏi CÓ jar không; bytes để gói đọc SAU canary
            # WP714: bundle GHI ĐÈ SECRETS_FILEID — gói thiếu NLM (hoặc gói nlm_auth cũ của config) mà rc0 là âm thầm
            # xoá/đẩy lại credential trên Drive (đo PR #714). Thiếu jar ⇒ DỪNG; chủ ý bỏ NLM thì `--no-nlm`.
            print("[secrets-stage] ✗ chưa có jar nlm ở máy này — bundle sẽ GHI ĐÈ bản trên Drive nên KHÔNG gói "
                  "thiếu/cũ: `nlm login` rồi chạy lại, hoặc `--no-nlm` nếu chủ ý gói không có NLM.", file=sys.stderr)
            return 3
        # WP710 r4/g3: canary không dương thì TỪ CHỐI CẢ LỆNH, không upload gì.
        nlm, _rc_gate, _ = _nlm_files_after_live_canary("secrets-stage", entry_notebook)
        if nlm is None:
            return _rc_gate
        bundle["nlm_auth"] = nlm_confirmed = nlm
        age = _nlm_auth_age_days(nlm)
        agestr = f", cookie ~{age:.0f} ngày tuổi" if age is not None else ""
        print(f"[secrets-stage] ✓ gói nlm_auth ({len(nlm)} file{agestr}) — Cowork khỏi `nlm login`.")
    _rc_guard = _nlm_bundle_guard("secrets-stage", bundle, nlm_confirmed)
    if _rc_guard:
        return _rc_guard
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
    _entry_nb = os.environ.get("TL_NOTEBOOK_ID")      # WP714: ghim TRƯỚC load_creds của lệnh
    return _nlm_contained("secrets-set", lambda _a: _secrets_set_body(_a, _entry_nb), a)


def _secrets_set_body(a, entry_notebook) -> int:
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
        print(f"[secrets-set] ✗ giải mã lỗi: {_safe_exc(e)}", file=sys.stderr)   # WP714: chỉ tên lớp
        return 3
    changed = []
    nlm_confirmed = None
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
        if _refresh_nlm_auth() is None:
            return _refresh_treo("secrets-set")
        if not _nlm_auth_files():                      # chỉ hỏi CÓ jar không; bytes để gói đọc SAU canary
            print("[secrets-set] ✗ --nlm cần `nlm login` ở máy này.", file=sys.stderr)
            return 3
        # WP710 r4/g3: đường này đẩy CẢ bundle LẪN nlm_cred.enc public — cùng cổng canary như nlm-auth-stage,
        # chạy TRƯỚC mọi upload; không dương ⇒ từ chối cả lệnh (kể cả các trường khác đổi cùng lượt).
        nlm, _rc_gate, _ = _nlm_files_after_live_canary("secrets-set", entry_notebook)
        if nlm is None:
            return _rc_gate
        bundle["nlm_auth"] = nlm_confirmed = nlm; changed.append("nlm_auth")
        age = _nlm_auth_age_days(nlm)
        if age is not None:
            print(f"[secrets-set] nlm cookie ~{age:.0f} ngày tuổi." + _nlm_cookie_age_note(age))
    if not changed:
        print("[secrets-set] ⚠ không có trường nào để đổi (--gas-token/--webapp/--gws/--nlm).", file=sys.stderr)
        return 1
    # WP714: bundle tải từ Drive có `nlm_auth` mà lượt này KHÔNG `--nlm` ⇒ ghi lại = gửi lại credential chưa qua
    # canary (đo PR #714: đổi --webapp ⇒ rc0, 0 canary, bundle mang nlm_auth lên lại). Chọn TỪ CHỐI (không tự xoá,
    # không tự thay): canary chỉ chứng minh jar CỤC BỘ, không chứng minh được bytes trên Drive.
    _rc_guard = _nlm_bundle_guard("secrets-set", bundle, nlm_confirmed)
    if _rc_guard:
        return _rc_guard
    new = store.encrypt(json.dumps(bundle, ensure_ascii=False).encode("utf-8"), master)
    _secrets_upload(new, getattr(a, "folder", None) or HOPNAP_FOLDER_ID, fid)
    print(f"[secrets-set] ✓ đã đổi {changed} → ghi đè bundle id={fid} ({len(new)}B).")
    # v1.33.1 (user chốt: CẢ đường bundle LẪN đường public đều phải chạy): 1 lệnh làm tươi CẢ HAI —
    # sau khi bundle xong, đồng bộ luôn file public .enc tương ứng (khoá=webapp token, GHI ĐÈ TẠI CHỖ
    # GWS_CRED_FILEID/NLM_CRED_FILEID → Chat đường public tự nhận). Lỗi public chỉ WARN (bundle ĐÃ tươi,
    # rc vẫn 0); --no-public để bỏ qua chủ đích.
    if not getattr(a, "no_public", False):
        _tok = os.environ.get("TL_TOKEN") or str(bundle.get("token") or "")
        _folder = getattr(a, "folder", None) or HOPNAP_FOLDER_ID
        _pub = []
        if ("gws_cred" in changed or "nlm_auth" in changed) and not _tok:
            print("[secrets-set] ⚠ thiếu webapp token → KHÔNG đồng bộ được đường public (.enc khoá=token); "
                  "chạy riêng `tl gws-auth-stage` / `tl nlm-auth-stage`.", file=sys.stderr)
        else:
            try:
                if "gws_cred" in changed:
                    _stage_enc_upload("gws_cred.enc",
                                      store.encrypt(str(bundle["gws_cred"]).encode("utf-8"), _tok),
                                      _folder, GWS_CRED_FILEID, False)
                    _pub.append(f"gws_cred.enc→{GWS_CRED_FILEID}")
                if "nlm_auth" in changed:
                    _stage_enc_upload("nlm_cred.enc",
                                      store.encrypt(json.dumps(bundle["nlm_auth"], ensure_ascii=False).encode("utf-8"), _tok),
                                      _folder, os.environ.get("TL_NLM_CRED_FILEID") or NLM_CRED_FILEID, False)
                    _pub.append(f"nlm_cred.enc→{os.environ.get('TL_NLM_CRED_FILEID') or NLM_CRED_FILEID}")
            except Exception as e:  # noqa: BLE001
                print(f"[secrets-set] ⚠ đồng bộ public .enc lỗi ({_safe_exc(e)}) — bundle ĐÃ tươi; vá đường public bằng "
                      "`tl gws-auth-stage` / `tl nlm-auth-stage`.", file=sys.stderr)
        if _pub:
            print(f"[secrets-set] ✓ đồng bộ PUBLIC tại chỗ: {', '.join(_pub)} — Chat/Cowork đường public cũng tươi.")
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


def _symlink_nlm_system_path(src: str | None = None, dst: str = "/usr/local/bin/nlm",
                             posix: bool | None = None) -> str:
    """C-1.4 (v1.33.23 — log rà Cowork v1.33.20: installer ghi PATH vào ~/.profile/.bashrc nhưng bash
    NON-INTERACTIVE không source → `nlm` trần 'No such file or directory', chỉ chạy được absolute-path /
    `tl nlm-*`): best-effort SYMLINK ~/.local/bin/nlm → /usr/local/bin/nlm — /usr/local/bin nằm trong PATH
    MẶC ĐỊNH của mọi shell kể cả non-interactive; Cowork chạy root nên ghi được. Idempotent; KHÔNG đè file/
    link có sẵn trỏ chỗ khác (tôn trọng cài đặt ngoài); nuốt lỗi (máy không quyền ghi = no-op); CHỈ POSIX."""
    if not (os.name == "posix" if posix is None else posix):
        return ""
    src = src or os.path.expanduser("~/.local/bin/nlm")
    try:
        if not os.path.exists(src):
            return ""
        if os.path.exists(dst) or os.path.islink(dst):
            return "" if os.path.realpath(dst) == os.path.realpath(src) else \
                f"⚠ {dst} đã tồn tại trỏ chỗ khác — giữ nguyên; dùng `tl nlm-*` (tự nối PATH) nếu `nlm` trần lỗi"
        os.symlink(src, dst)
        return f"symlink {dst} → ~/.local/bin/nlm (bash non-interactive gọi `nlm` trần chạy được)"
    except Exception:  # noqa: BLE001
        return ""


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
            for _pmsg in (_persist_local_bin_on_path(), _symlink_nlm_system_path()):
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
        for _pmsg in (_persist_local_bin_on_path(), _symlink_nlm_system_path()):
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
    print(f"[nlm-auth-pull] ✓ nlm auth {len(nlm)} file → ~/.notebooklm-mcp-cli{agestr} [nguồn {src}]. Kiểm bằng probe LIVE (`tl nlm-auth-status`), KHÔNG bằng `nlm login --check`"
          + _nlm_cookie_age_note(age))
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
            _agenote = _nlm_cookie_age_note(age)       # ngưỡng/thông điệp thống nhất mọi đường nạp (A log 2026-07-05)
            if _agenote:
                print(f"[bootstrap]{_agenote}", file=sys.stderr)
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


def _stage_enc_upload(name: str, blob: bytes, folder: str, fid_inplace: str | None, force_new: bool, g=None):
    """v1.33.1 (log Cowork A1 — vòng đời cred tái diễn): ghi blob .enc lên Drive. MẶC ĐỊNH GHI ĐÈ TẠI CHỖ
    `fid_inplace` (update_content — fileId GIỮ NGUYÊN → đường PUBLIC của Chat/Cowork tự tươi, KHÔNG phải bake
    lại tl.py sau mỗi lần token rụng). force_new/thiếu fid → upload file MỚI (hành vi cũ, in fileId để bake).
    Trả (fid, in_place). Dùng chung gws-auth-stage / nlm-auth-stage / secrets-set đồng-bộ-public."""
    import tempfile as _tf
    g = g or _imp("gws_bridge")
    with _tf.TemporaryDirectory() as d:
        fp = os.path.join(d, name)
        with open(fp, "wb") as f:
            f.write(blob)
        if fid_inplace and not force_new:
            try:
                g.update_content(fid_inplace, fp, mime="application/octet-stream")
            except Exception as e:  # noqa: BLE001  gws chết (vd rc=5 HTTP request failed) → FALLBACK gcloud (OAuth production, GIỮ fileId, verify md5)
                gtok, gerr = _gcloud_access_token()
                if not gtok:
                    # WP714 (lớp `stage-error-output-leaks-credential`): KHÔNG nhúng `{e}`/`gerr` — văn bản lỗi của
                    # gws/gcloud do đầu kia quyết định; chỉ tên lớp + mã cố định đi ra ngoài.
                    raise RuntimeError(
                        f"STAGE_ENC_GWS_FAILED ({_safe_exc(e)}); GCLOUD_FALLBACK_UNAVAILABLE"
                    ) from None
                print(f"[stage-enc] ⚠ gws update lỗi ({_safe_exc(e)}) → [FALLBACK→gcloud] giữ fileId {fid_inplace}…", file=sys.stderr)
                r = _gcloud_drive_update(gtok, fid_inplace, fp, "application/octet-stream")
                if not r.get("ok"):
                    raise RuntimeError("STAGE_ENC_GCLOUD_FAILED") from None
                print(f"[stage-enc] ✓ [gcloud] cập nhật {fid_inplace} (md5 verified).", file=sys.stderr)
            return fid_inplace, True
        r = g.upload(name, fp, parents=[folder], mime="application/octet-stream")
        return (r.get("file") or {}).get("id"), False


def cmd_gws_auth_stage(a) -> int:
    """[CHẠY Ở CODE] Xuất gws cred → MÃ HOÁ (khoá=webapp token) → Drive. v1.33.1: mặc định GHI ĐÈ TẠI CHỖ
    GWS_CRED_FILEID (fileId giữ nguyên — Chat/Cowork `up`/`gws-auth-load` tự nhận bản tươi, không bake lại);
    `--new` tạo file mới (hành vi cũ). Cred KHÔNG plaintext, KHÔNG vào zip — chỉ bản mã hoá trên Drive."""
    import subprocess as _sp
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
    fid, in_place = _stage_enc_upload("gws_cred.enc", blob, getattr(a, "folder", None) or HOPNAP_FOLDER_ID,
                                      getattr(a, "cred_file_id", None) or GWS_CRED_FILEID,
                                      getattr(a, "new", False))
    if in_place:
        print(f"[gws-auth-stage] ✓ cred MÃ HOÁ ({len(blob)}B) → GHI ĐÈ TẠI CHỖ id={fid} (fileId GIỮ NGUYÊN — "
              "Chat/Cowork `tl up`/`gws-auth-load` tự nhận bản tươi, KHÔNG bake lại).")
        return 0
    print(f"[gws-auth-stage] ✓ cred MÃ HOÁ ({len(blob)}B) → Drive id={fid} (file MỚI — --new)")
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


def _nlm_auth_files_raw() -> dict:
    """r208c 3.1: đọc THÔ file auth nlm cục bộ ({relpath: text}) — KHÁC `_nlm_auth_files` ở chỗ KHÔNG
    dựng lại auth.json từ profile. So tươi/cũ phải nhìn đúng cái đang nằm trên đĩa."""
    base = os.path.expanduser("~/.notebooklm-mcp-cli")
    out = {}
    for rel in _NLM_AUTH_RELS:
        p = os.path.join(base, *rel.split("/"))
        try:
            if os.path.exists(p):
                out[rel] = open(p, encoding="utf-8").read()
        except Exception:  # noqa: BLE001
            pass
    return out


def _nlm_auth_load_downgrade(bundle: dict, local: dict) -> tuple:
    """PURE (r208c 3.1): bản bundle sắp ghi đè có CŨ HƠN bản cục bộ không? Trả (is_downgrade, lý_do).

    Mốc so = `_nlm_auth_age_days` (ưu tiên `profiles/default/metadata.json.last_validated`, fallback
    `auth.json.extracted_at`) — đúng tín hiệu tươi mà M1b v1.33.38 đã chốt. Không đọc được MỘT trong
    hai phía ⇒ (False, …): KHÔNG chặn khi không có bằng chứng (máy chưa từng login vẫn nạp được)."""
    _b, _l = _nlm_auth_age_days(bundle or {}), _nlm_auth_age_days(local or {})
    if _b is None or _l is None:
        return False, ("chưa có bản cục bộ để so" if _l is None else "bundle không mang mốc thời gian")
    if _b <= _l:
        return False, f"bundle tươi hơn/bằng (bundle {_b * 1440:.0f}' vs cục bộ {_l * 1440:.0f}')"
    return True, (f"bundle {_b * 1440:.0f}' tuổi vs cục bộ {_l * 1440:.0f}' "
                  f"(cũ hơn {(_b - _l) * 1440:.0f}')")


def _nlm_auth_load(token: str, fid: str, force: bool = False):
    """Tải nlm_cred.enc (webapp `download`) → giải mã (khoá=token) → ghi ~/.notebooklm-mcp-cli/{auth.json,profiles/…}.
    Trả (ok, msg). KHÔNG cần master key (mirror _gws_auth_load → nlm headless).
    r208c 3.1: `force=True` bỏ qua chốt chống hạ cấp (mặc định TỪ CHỐI ghi đè bằng bản cũ hơn)."""
    import base64
    store = _imp("gws_cred_store")
    if not fid:
        return False, "chưa có NLM_CRED_FILEID — trên máy giữ hồ sơ gốc chạy `tl nlm-auth-stage --new` (chỉ upload sau canary LIVE dương), rồi điền fileId / env TL_NLM_CRED_FILEID."
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
    # r208c 3.1: CHỐNG HẠ CẤP. Lệnh này GHI ĐÈ jar cục bộ bằng bản bundle — đo tươi 25-07: bản
    # `auth.json` đem đi stage trễ hơn profile sống 127', `extracted_at` 415', token xoay trong đó
    # hết hạn từ 7,2 GIỜ trước. Nạp bản như vậy đè lên phiên đang sống = TỰ GIẾT cookie tươi. Đây
    # đúng là lý do phải BÁC đề xuất «tự gọi nlm-auth-load khi auth expired» của báo cáo mục 3.1.
    _dg, _why_dg = _nlm_auth_load_downgrade(nlm, _nlm_auth_files_raw())
    if _dg and not force:
        return False, ("TỪ CHỐI HẠ CẤP — " + _why_dg + ". Bản trên Drive CŨ HƠN bản cục bộ: ghi đè sẽ "
                       "LÀM MẤT cookie tươi hơn đang có. Muốn cố ý: `--force`. Đường đúng khi cookie "
                       "chết hẳn: đăng nhập lại trên máy giữ hồ sơ gốc rồi chạy `pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath <config>` (refresh → canary → stage).")
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
    # r208c 3.1: bundle có thể mang sẵn PHIÊN ĐÃ CHẾT — đo tươi 25-07: bản trên Drive chứa đúng token
    # xoay hết hạn −129' y như jar cục bộ, nạp về KHÔNG hồi sinh được gì. Đây chính là lý do vòng lặp
    # «auth expired → tự nlm-auth-load → thử lại» của báo cáo mục 3.1 sẽ quay vòng vô ích. Nói THẲNG.
    _rot_b = ""
    try:
        import importlib as _il_rb
        _rs = _il_rb.import_module("tl_core.nlm_ops")._nlm_rotation_token_state(
            json.loads(nlm.get("profiles/default/cookies.json", "[]")))
        if _rs.get("found") and _rs.get("expired"):
            _rot_b = (f" ⚠ BUNDLE_ROTATION_TOKEN_EXPIRED: {_rs['name']} trong bundle hết hạn "
                      f"{abs(_rs['expires_in_min']):.0f}' trước — bản vừa nạp KHÔNG hồi sinh được phiên; "
                      "phải đăng nhập lại trên máy giữ hồ sơ gốc rồi chạy `pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath <config>` (refresh → canary → stage).")
    except Exception:  # noqa: BLE001 — cảnh báo best-effort, không chặn nạp
        pass
    return True, (f"~/.notebooklm-mcp-cli ({len(nlm)} file"
                  + (f", ~{age:.0f} ngày tuổi" if age is not None else "") + ")"
                  + _nlm_cookie_age_note(age) + _rot_b)


def cmd_nlm_auth_stage(a) -> int:
    """[CHẠY Ở CODE, máy giữ hồ sơ trình duyệt gốc] Gói cookie nlm → MÃ HOÁ (khoá=webapp token) → upload Drive SAU canary
    LIVE dương. In fileId để baked. Quy trình đầy đủ: wrapper `scripts/nlm-credential-refresh.ps1` (WP710).
    Cho Cowork nạp nlm HEADLESS bằng `nlm-auth-load` KHÔNG cần master key (mirror gws-auth-stage)."""
    _entry_nb = os.environ.get("TL_NOTEBOOK_ID")      # WP714: ghim TRƯỚC load_creds (token chỉ ở config)
    return _nlm_contained("nlm-auth-stage", lambda _a: _nlm_auth_stage_body(_a, _entry_nb), a)


def _nlm_auth_stage_body(a, entry_notebook) -> int:
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
    if getattr(a, "refresh", False) and _refresh_nlm_auth() is None:
        return _refresh_treo("nlm-auth-stage")
    if not _nlm_auth_files():                          # tiền kiểm CÓ jar không: hàm này ĐỌC jar vào RAM rồi bỏ; payload được đọc LẠI sau canary dương
        print("[nlm-auth-stage] ✗ chưa có cookie nlm ở máy này — chạy `nlm login` trước.", file=sys.stderr)
        return 3
    # M1c (v1.33.39 — log Cowork: user stage cookie 'mới' [extracted_at TIẾN] nhưng NLM từ chối MỌI endpoint;
    # điều tra local thấy cookie đã CHẾT CẢ Ở MÁY NÀY → stage cookie chết = Cowork nhận cookie chết = kẹt vòng
    # lặp stage-lại-vô-ích). VERIFY LIVE bằng canary notebook_get (KHÔNG tin `nlm login --check` — false-red).
    # WP710: lệnh tự giữ cổng (script shell cũ cũng đi qua đây); --force KHÔNG bỏ qua được; cổng dùng chung
    # với secrets-set --nlm / secrets-stage qua `_nlm_files_after_live_canary`.
    nlm, _rc_gate, _ = _nlm_files_after_live_canary("nlm-auth-stage", entry_notebook)
    if nlm is None:
        return _rc_gate
    blob = store.encrypt(json.dumps(nlm, ensure_ascii=False).encode("utf-8"), token)   # cookie chỉ ở RAM
    # v1.33.1: cùng khuôn gws-auth-stage — mặc định GHI ĐÈ TẠI CHỖ NLM_CRED_FILEID (cookie rụng ~2-4 tuần,
    # mỗi lần re-stage không còn đổi fileId); --new tạo file mới.
    fid, in_place = _stage_enc_upload("nlm_cred.enc", blob, getattr(a, "folder", None) or HOPNAP_FOLDER_ID,
                                      getattr(a, "cred_file_id", None) or os.environ.get("TL_NLM_CRED_FILEID")
                                      or NLM_CRED_FILEID,
                                      getattr(a, "new", False))
    age = _nlm_auth_age_days(nlm)
    agestr = f", ~{age:.0f} ngày" if age is not None else ""
    _agenote = _nlm_cookie_age_note(age)
    if _agenote:      # đang gói cookie ĐÃ GIÀ → nhắc làm tươi theo wrapper WP710 thay vì stage bản sắp chết
        print(f"[nlm-auth-stage]{_agenote}", file=sys.stderr)
    if in_place:
        print(f"[nlm-auth-stage] ✓ nlm cookie MÃ HOÁ ({len(nlm)} file, {len(blob)}B{agestr}) → GHI ĐÈ TẠI CHỖ "
              f"id={fid} (fileId GIỮ NGUYÊN — Cowork `nlm-auth-load` tự nhận bản tươi).")
        return 0
    print(f"[nlm-auth-stage] ✓ nlm cookie MÃ HOÁ ({len(nlm)} file, {len(blob)}B{agestr}) → Drive id={fid} (file MỚI — --new)")
    print(f"  → baked: đặt NLM_CRED_FILEID = \"{fid}\" trong tl.py (hoặc env TL_NLM_CRED_FILEID / `nlm-auth-load --cred-file-id {fid}`).")
    return 0


def cmd_nlm_auth_load(a) -> int:
    """[CHẠY Ở COWORK] Nạp nlm cookie HEADLESS: tải bản mã hoá từ Drive → giải mã (webapp token) →
    ~/.notebooklm-mcp-cli. KHÔNG cần master key/`nlm login` (mirror gws-auth-load). Sau đó nlm chạy thẳng (không MCP fallback)."""
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    token = os.environ.get("TL_TOKEN") or ""
    fid = getattr(a, "cred_file_id", None) or os.environ.get("TL_NLM_CRED_FILEID") or NLM_CRED_FILEID
    ok, msg = _nlm_auth_load(token, fid, force=bool(getattr(a, "force", False)))
    if ok:
        print(f"[nlm-auth-load] ✓ nạp nlm cookie → {msg} (chmod 600). nlm chạy headless. Kiểm bằng probe LIVE (`tl nlm-auth-status`), KHÔNG bằng `nlm login --check`")
        return 0
    print(f"[nlm-auth-load] ✗ {msg}", file=sys.stderr)
    return 2


def _gcloud_exe() -> str | None:
    """v1.33.49 (log local: `gws auth login` LỖI Ở BƯỚC CUỐI sau khi cấp quyền + cred hết hạn nhanh — OAuth
    client của gws CLI ở chế độ Testing: refresh token CHẾT SAU 7 NGÀY + màn consent dễ 403 access_denied):
    gcloud CLI làm nguồn token DỰ PHÒNG — OAuth client của gcloud là PRODUCTION (refresh token bền)."""
    import shutil as _sh
    return _sh.which("gcloud") or _sh.which("gcloud.cmd")


def _gcloud_access_token() -> tuple[str, str]:
    """Access token user gcloud (cần DRIVE SCOPE: `gcloud auth login --enable-gdrive-access`). Trả (token, err)."""
    exe = _gcloud_exe()
    if not exe:
        return "", "gcloud không có trên PATH"
    try:
        r = subprocess.run([exe, "auth", "print-access-token"], capture_output=True, text=True, timeout=30)
    except Exception as e:  # noqa: BLE001
        return "", f"{type(e).__name__}: {e}"
    tok = (r.stdout or "").strip()
    if r.returncode != 0 or not tok:
        return "", ((r.stderr or "").strip()[:200] or f"rc={r.returncode}") + " — `gcloud auth login --enable-gdrive-access`"
    return tok, ""


# r330 — bệnh r327 LẶP Ở ĐƯỜNG GHI: mọi thông điệp hỏng của drive-push đều chỉ sang `gws auth login`,
# nhưng TIMEOUT ≠ MẤT QUYỀN. Người vận hành đọc xong đi cấp quyền lại = mất buổi mà bệnh còn nguyên
# (đúng vết r327 đã trả giá ở phép dò). Ca `r327_probe_error_lo_dien` khoá chuyện này cho phép DÒ;
# đây khoá cho đường GHI + cho chính ROUTE khi phép dò hỏng vì timeout.
_GWS_TIMEOUT_FIX = ("gws TIMEOUT — KHÔNG phải mất quyền, ĐỪNG `gws auth login`. Nâng ngân sách rồi chạy "
                    "lại: TL_GWS_WRITE_TIMEOUT=900 (đường ghi) hoặc TL_GWS_TIMEOUT=900 (sàn chung mọi lệnh gws)")


def _gws_timeout_hint(err: str) -> str:
    """PURE: lỗi gws có phải TIMEOUT không → câu khắc phục ĐÚNG HƯỚNG; rỗng nếu KHÔNG phải timeout
    (đừng đổ oan cho ngân sách khi thật sự mất quyền — sai hướng ngược lại cũng tốn y hệt)."""
    return _GWS_TIMEOUT_FIX if "timeout" in (err or "").lower() else ""


def _drive_push_route(via: str, gws_ok: bool, gcloud_ok: bool, probe_error: str = "") -> tuple[str, str]:
    """PURE (test offline): chọn đường drive-push. auto = gws trước (đường chuẩn), chết → gcloud LOUD.
    probe_error (r330): lý do phép dò gws hỏng — `availability_detail()["probe_error"]` mà r327 đã KHAI
    sẵn nhưng CHƯA AI ĐỌC. Timeout ⇒ lời khuyên phải là NÂNG NGÂN SÁCH, không phải đi xin quyền lại."""
    v = (via or "auto").strip().lower()
    tmo = _gws_timeout_hint(probe_error)
    if v == "gws":
        if gws_ok:
            return "gws", ""
        return "", ((f"{tmo} — hoặc bỏ --via để auto-fallback gcloud") if tmo else
                    "gws chưa sẵn/auth (--via gws ép) — `gws auth login` hoặc bỏ --via để auto-fallback gcloud")
    if v == "gcloud":
        return ("gcloud", "") if gcloud_ok else ("", "gcloud không sẵn/chưa login drive-scope — `gcloud auth login --enable-gdrive-access`")
    if gws_ok:
        return "gws", ""
    if gcloud_ok:
        return "gcloud", ("[FALLBACK→gcloud] " + (tmo if tmo else "gws chưa sẵn/auth")
                          + " → dùng token gcloud (OAuth production, không hạn-7-ngày)")
    return "", ("cả gws lẫn gcloud đều chưa sẵn sàng — (a) " + (tmo if tmo else "`gws auth login`")
                + "; hoặc (b) cài gcloud + `gcloud auth login --enable-gdrive-access` rồi chạy lại.")


def _gcloud_drive_update(token: str, fid: str, path: str, mime: str, new_name: str | None = None) -> dict:
    """PATCH nội dung file Drive (GIỮ fileId) qua REST v3 bằng Bearer token gcloud + VERIFY md5 đọc-lại
    (verified-write doctrine — không tin HTTP 200 trần). new_name → PATCH metadata đổi tên cùng lượt."""
    import urllib.request
    import urllib.error
    data = open(path, "rb").read()

    def _call(url: str, body: bytes, ctype: str) -> dict:
        req = urllib.request.Request(url, data=body, method="PATCH",
                                     headers={"Authorization": f"Bearer {token}", "Content-Type": ctype})
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8", "replace") or "{}")

    try:
        meta = _call(f"https://www.googleapis.com/upload/drive/v3/files/{fid}"
                     f"?uploadType=media&supportsAllDrives=true&fields=id,name,md5Checksum,modifiedTime",
                     data, mime)
        if new_name and (meta.get("name") or "") != new_name:
            meta = _call(f"https://www.googleapis.com/drive/v3/files/{fid}"
                         f"?supportsAllDrives=true&fields=id,name,md5Checksum,modifiedTime",
                         json.dumps({"name": new_name}).encode("utf-8"), "application/json")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:300]
        except Exception:  # noqa: BLE001
            pass
        fix = {401: "token hết hạn/không hợp lệ → `gcloud auth login --enable-gdrive-access` rồi chạy lại",
               403: "thiếu DRIVE SCOPE hoặc account gcloud KHÔNG có quyền sửa file → "
                    "`gcloud auth login --enable-gdrive-access` bằng ĐÚNG account sở hữu Package",
               404: "fileId sai hoặc file không share với account gcloud đang active (`gcloud config get account`)"}
        return {"ok": False, "error": f"HTTP {e.code}: {body}", "fix": fix.get(e.code, "")}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "fix": ""}
    want = hashlib.md5(data).hexdigest()
    got = str(meta.get("md5Checksum") or "")
    ok = (not got) or got == want          # GDoc-native không có md5; zip/binary PHẢI khớp
    return {"ok": ok, "file": meta, "md5_local": want, "md5_drive": got or None,
            **({} if ok else {"error": f"MD5 LỆCH sau upload: local {want} ≠ drive {got} (upload hỏng?)"})}


def _bundle_meta_blocks_push(root) -> bool:
    """v1.33.59 (ADR-0001): cây chứa BUNDLE_META.json = giải nén từ bundle nhánh song song → cấm publish.
    v1.35.48 (r212) — FAIL-CLOSED: bản cũ `except → False` biến MỌI trục trặc thành "cứ publish đi", tức
    guard cấm-publish lại hỏng theo hướng CHO PHÉP. Không đọc được thì CHẶN (người vẫn có `--force`)."""
    try:
        return (Path(root) / "BUNDLE_META.json").exists()
    except Exception:  # noqa: BLE001
        return True


def cmd_drive_push(a) -> int:
    """[CHẠY Ở MÁY CÓ gws HOẶC gcloud AUTH] Cập nhật NỘI DUNG file Drive (GIỮ fileId) = file local.
    v1.33.49: `--via auto|gws|gcloud` — auto = gws trước, gws chết → FALLBACK gcloud LOUD (token
    `gcloud auth print-access-token`, cần `gcloud auth login --enable-gdrive-access` 1 lần; OAuth client
    gcloud là PRODUCTION nên KHÔNG dính hạn-7-ngày Testing như gws). Đường gcloud có VERIFY md5 đọc-lại.
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
    if _bundle_meta_blocks_push(HERE.parent) and not getattr(a, "force", False):
        print("[drive-push] ✗ BLOCKED_BY_BUNDLE_META (ADR-0001): cây này có BUNDLE_META.json — là bản giải nén"
              " từ bundle nhánh song song, KHÔNG được publish. Giao zip bundle cho canonical merge; hoặc --force"
              " nếu CHẮC đây là canonical (xoá BUNDLE_META.json trước).", file=sys.stderr)
        return 3
    via = (getattr(a, "via", None) or "auto").strip().lower()
    gb = _imp("gws_bridge")
    gws_ok = (via != "gcloud") and gb.is_available()
    # r330: đọc LÝ DO phép dò hỏng (r327 khai sẵn `probe_error`) để khuyên ĐÚNG HƯỚNG. Chỉ đọc khi ĐÃ dò
    # — `via=gcloud` cố tình bỏ qua phép dò, gọi availability_detail() ở đó sẽ CHẠY phép dò 120s vô ích.
    perr = "" if via == "gcloud" else (gb.availability_detail().get("probe_error") or "")
    gtok, gerr = ("", "")
    if via == "gcloud" or (via == "auto" and not gws_ok):
        gtok, gerr = _gcloud_access_token()
    route, note = _drive_push_route(via, gws_ok, bool(gtok), probe_error=perr)
    if not route:
        print(f"[drive-push] ✗ {note}" + (f" (gcloud: {gerr})" if gerr else ""), file=sys.stderr)
        return 3
    if note:
        print(f"[drive-push] {note}", file=sys.stderr)
    mime = "application/zip" if path.lower().endswith(".zip") else (mimetypes.guess_type(path)[0] or "application/octet-stream")
    new_name = getattr(a, "name", None) or (os.path.basename(path) if getattr(a, "rename_to_file", False) else None)
    if route == "gws":
        try:
            r = gb.update_content(fid, path, mime=mime)
        except Exception as e:  # noqa: BLE001
            # auto: gws chết GIỮA CHỪNG (thường auth) → thử gcloud trước khi bỏ cuộc (cùng lớp fallback LOUD).
            if via == "auto" and not gtok:
                gtok, gerr = _gcloud_access_token()
            if via == "auto" and gtok:
                print(f"[drive-push] ⚠ gws update lỗi ({type(e).__name__}: {e}) → [FALLBACK→gcloud]…", file=sys.stderr)
                route = "gcloud"
            else:
                # r330: ĐÂY là dòng người vận hành đọc lúc deploy chết. Trước đó nó im về ngân sách nên
                # ca THẬT («gws timeout sau 120.0s» trên gói 2,49MB) đọc như lỗi quyền → đi `gws auth login`.
                _fix = _gws_timeout_hint(f"{type(e).__name__}: {e}")
                print(f"[drive-push] ✗ update lỗi: {type(e).__name__}: {e}"
                      + (f" (gcloud cũng không sẵn: {gerr})" if via == "auto" else "")
                      + (f"\n  KHẮC PHỤC: {_fix}" if _fix else ""), file=sys.stderr)
                return 4
        if route == "gws":
            f = (r or {}).get("file") or {}
            renamed = ""
            if new_name:
                try:
                    gb.rename(fid, new_name)   # rename có ASSERT đọc-lại-tên (v1.22.60) → lỗi sẽ raise rõ
                    renamed = f" · đổi tên → '{new_name}'"
                except Exception as e:  # noqa: BLE001
                    print(f"[drive-push] ⚠ update OK nhưng ĐỔI TÊN lỗi: {type(e).__name__}: {e}", file=sys.stderr)
            print(f"[drive-push] ✓ [gws] Drive id={f.get('id') or fid} ← {os.path.basename(path)} ({os.path.getsize(path)}B){renamed}. "
                  f"fileId GIỮ NGUYÊN; tl_fetch.sh sẽ tải bản mới này.")
            return 0
    r = _gcloud_drive_update(gtok, fid, path, mime, new_name=new_name)
    if not r.get("ok"):
        print(f"[drive-push] ✗ [gcloud] {r.get('error')}" + (f"\n  KHẮC PHỤC: {r['fix']}" if r.get("fix") else ""),
              file=sys.stderr)
        return 4
    f = r.get("file") or {}
    print(f"[drive-push] ✓ [gcloud] Drive id={f.get('id') or fid} ← {os.path.basename(path)} ({os.path.getsize(path)}B)"
          + (f" · đổi tên → '{f.get('name')}'" if new_name else "")
          + f" · md5 VERIFY {'✓ ' + str(r.get('md5_drive')) if r.get('md5_drive') else '(không có — file GDoc-native)'}. "
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
    # v1.34.53 (A5): nhận positional lẫn --file-id (đồng bộ extract/nlm-get); --file-id thắng khi đưa cả 2.
    if not getattr(a, "file_id", None):
        a.file_id = getattr(a, "file_id_pos", None)
    if not a.file_id:
        print(json.dumps({"ok": False, "error": "FILE_ID_REQUIRED",
                          "note": "tl download <fileId> hoặc tl download --file-id <fileId>"}, ensure_ascii=False),
              file=sys.stderr)
        return 2
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
