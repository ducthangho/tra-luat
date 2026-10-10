# -*- coding: utf-8 -*-
"""wp727 — `_refresh_nlm_auth` gọi `nlm auth refresh` (không còn `nlm login --check`) và KHÔNG mở được cổng.

N1 argv/timeout · N2 canary False/None ⇒ 0 upload rc 4 (kể cả --refresh --force), True ⇒ 1 upload; refresh quá hạn ⇒
DỪNG · N3 lỗi refresh không lan · N4 `login --check` chỉ ở dòng/chuỗi CHO PHÉP (tĩnh, phụ) · N5 đầu ra THẬT của từng
nhánh gợi ý WP727 sửa không gợi ý `login --check` và không lộ cookie.
"""

import argparse
import ast
import contextlib
import hashlib
import io
import math
import os
from pathlib import Path
import subprocess
from unittest import mock


TEST_ID = "wp727_tl_gws_refresh"

_CHO_PHEP = (      # NGUYÊN VĂN từng dòng (đã strip) được phép nhắc `login --check` — so CẢ DÒNG, không chuỗi con
    '"""M1 (v1.33.35 — log rà 45 Luật LIVE: nlm-auth-load/doctor/`nlm login --check` báo XANH [rc=0] nhưng',
    'server (`nlm notebook get` base notebook) thay vì tin tuổi file / `login --check` (không chứng minh cookie',
    'WP727: thay `nlm login --check` (lệnh KIỂM, false-green — không phải lệnh làm tươi). Trả True khi lệnh rc 0;',
    'print(f"[nlm-auth-pull] ✓ nlm auth {len(nlm)} file → ~/.notebooklm-mcp-cli{agestr} [nguồn {src}]. Kiểm bằng probe LIVE (`tl nlm-auth-status`), KHÔNG bằng `nlm login --check`"',
    '# lặp stage-lại-vô-ích). VERIFY LIVE bằng canary notebook_get (KHÔNG tin `nlm login --check` — false-red).',
    'print(f"[nlm-auth-load] ✓ nạp nlm cookie → {msg} (chmod 600). nlm chạy headless. Kiểm bằng probe LIVE (`tl nlm-auth-status`), KHÔNG bằng `nlm login --check`")',
)


class _Ket:
    def __init__(self, rc):
        self.returncode = rc
        self.stdout = "SENTINEL-COOKIE-wp727"
        self.stderr = "SENTINEL-COOKIE-wp727-err"


_va = mock.patch.multiple      # thay thuộc tính tạm, tự trả lại kể cả khi lỗi


def _goi_refresh(tg, hanh_vi):
    nhat_ky = []

    def run(argv, **kw):
        nhat_ky.append((list(argv), kw))
        return hanh_vi(argv, kw)
    import shutil
    ra, loi = io.StringIO(), io.StringIO()
    with _va(subprocess, run=run), _va(shutil, which=lambda name: "/fake/bin/nlm"), \
            contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi):
        try:
            kq = tg._refresh_nlm_auth()
        except Exception:  # noqa: BLE001 — lỗi lan ra khỏi refresh là VI PHẠM N3, đo thành giá trị riêng
            kq = "LAN_LOI"
    if ra.getvalue() or loi.getvalue():
        kq = "IN_DAU_RA"        # helper không được in gì (đầu ra con có thể mang cookie)
    return kq, nhat_ky


def _n1_n3(tg):
    ok_true, log1 = _goi_refresh(tg, lambda a, k: _Ket(0))
    ok_false, _ = _goi_refresh(tg, lambda a, k: _Ket(1))
    if not (ok_true is True and ok_false is False and len(log1) == 1):
        return False
    argv, kw = log1[0]
    timeout = kw.get("timeout")
    if (argv[1:] != ["auth", "refresh"] or {kw.get("stdout"), kw.get("stderr")} != {subprocess.DEVNULL} or isinstance(timeout, bool)
            or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0):
        return False

    def treo(a, k):
        raise subprocess.TimeoutExpired(a, k.get("timeout"))
    def hong(a, k):
        raise OSError("no exec")
    return _goi_refresh(tg, treo)[0] is None and _goi_refresh(tg, hong)[0] is False   # quá hạn ⇒ None: người gọi DỪNG


def _stage(tg, canary, refresh_rc=0, ket_qua_ra=None):
    """`nlm-auth-stage --refresh --force`, nlm giả, cookie 20 ngày; trả (rc, số upload, sự kiện); `ket_qua_ra` nhận đầu ra."""
    su_kien, upload = [], []
    ra, loi = io.StringIO(), io.StringIO()

    def run(argv, **kw):
        su_kien.append("refresh")
        if refresh_rc == "treo":
            raise subprocess.TimeoutExpired(argv, kw.get("timeout"))
        return _Ket(refresh_rc)
    def alive(nb, **kw):
        su_kien.append("canary")
        return canary, "OFFLINE"
    import shutil
    ns = argparse.Namespace(refresh=True, force=True, folder=None, cred_file_id="OFFLINE", new=False,
                            config=None, profile=None)
    with mock.patch.dict(os.environ, {"TL_TOKEN": "offline-test-token"}), _va(subprocess, run=run), \
            _va(shutil, which=lambda name: "/fake/bin/nlm"), \
            _va(tg, _nlm_auth_alive=alive,
                _nlm_auth_files=lambda: (su_kien.append("jar") or {"auth.json": "offline-jar"}),
                _stage_enc_upload=lambda *a, **k: (upload.append(1) or ("OFFLINE", True)),
                _nlm_auth_age_days=lambda _nlm: 20.0), \
            contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi):
        rc = tg.cmd_nlm_auth_stage(ns)
    if ket_qua_ra is not None:
        ket_qua_ra.append(ra.getvalue() + loi.getvalue())
    return rc, len(upload), su_kien


def _n2(tg):
    for canary in (False, None):
        for refresh_rc in (0, 1):
            rc, n_up, su_kien = _stage(tg, canary, refresh_rc)
            if rc != 4 or n_up != 0 or su_kien[:1] != ["refresh"] or "canary" not in su_kien:
                return False
    rc, n_up, su_kien = _stage(tg, True, "treo")       # refresh quá hạn: cây con có thể còn ghi hồ sơ (review #731)
    if rc != 2 or n_up != 0 or su_kien != ["refresh"]:
        return False
    dau_ra = []
    rc, n_up, su_kien = _stage(tg, True, 0, dau_ra)
    # ĐO ĐẦU RA THẬT (lượt 3, F2c): mọi cách dựng chuỗi đều hiện ra ở đây — không `login --check`, không lộ chuỗi canh.
    ra = dau_ra[0]
    return (rc == 0 and n_up == 1 and su_kien.index("refresh") < su_kien.index("canary")
            and "NGÀY tuổi" in ra and "login --check" not in ra and "SENTINEL-COOKIE" not in ra)


def _n4(van_ban):
    """Mọi dòng nhắc `login --check` phải BẰNG NGUYÊN VĂN một dòng cho phép, mỗi dòng cho phép đúng một lần."""
    return sorted(d.strip() for d in van_ban.splitlines() if "login --check" in d) == sorted(_CHO_PHEP)


# sha256 TOÀN VĂN mỗi chuỗi Python được phép chứa `login --check` (sau ghép literal / f-string / `+`; lượt 2, F2b).
_CHUOI_CHO_PHEP = frozenset({
    "a4b85ff4f950bfb6229494d8dd99fbfdb412490ad5b2a190971e5cef343a7e05",   # docstring _nlm_auth_alive (M1)
    "73818ecbc71850b0fd01b94be79d0eefb95ca7e78fd9adf941b4ae778bba6264",   # docstring _refresh_nlm_auth (WP727)
    "bdb136eb46706b57fcf701c877904c9f27c0d1f9b7f0b3ed0ca0ee78d02eb0a9",   # thông báo nlm-auth-pull
    "a2e363f715ec74d607f55eb2f4a3821d0f6eda93e0be5e654d8831fc9985d6b5",   # thông báo nlm-auth-load
})


def _phan_f(v):
    """Mảnh f-string: hằng giữ nguyên; `{hằng}` trần ⇒ str(hằng) (lượt 4, F2d); còn lại không chứng minh được ⇒ "{}"."""
    if isinstance(v, ast.Constant):
        return v.value
    if (isinstance(v, ast.FormattedValue) and isinstance(v.value, ast.Constant) and v.conversion == -1
            and v.format_spec is None and isinstance(v.value.value, (str, int, float))):
        return str(v.value.value)
    return "{}"


def _van_tinh(n):
    """Giá trị chuỗi TĨNH của một biểu thức (không eval): hằng, f-string (phần biến thành "{}"), và phép `+` của chúng."""
    if isinstance(n, ast.Constant) and isinstance(n.value, str):
        return n.value
    if isinstance(n, ast.JoinedStr):
        return "".join(_phan_f(v) for v in n.values)
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
        trai, phai = _van_tinh(n.left), _van_tinh(n.right)
        return trai + phai if None not in (trai, phai) else (phai if trai is None else trai)
    return None


def _n4_ast(van_ban):
    """Mọi chuỗi Python (kể cả ghép literal và nối `+`) chứa `login --check` phải là một chuỗi cho phép."""
    cay = ast.parse(van_ban)
    con_cua_f = {id(v) for n in ast.walk(cay) if isinstance(n, ast.JoinedStr) for v in n.values}
    gap = set()
    for n in ast.walk(cay):
        if id(n) in con_cua_f:
            continue
        chuoi = _van_tinh(n)
        if chuoi is not None and "login --check" in chuoi and not isinstance(n, ast.BinOp):
            gap.add(hashlib.sha256(chuoi.encode("utf-8")).hexdigest())
        elif chuoi is not None and "login --check" in chuoi:
            # phép `+` chỉ được phép nếu một vế của nó đã là chuỗi cho phép (thông báo pull: f-string + ghi chú tuổi)
            vế = [_van_tinh(n.left), _van_tinh(n.right)]
            if not any(v and hashlib.sha256(v.encode("utf-8")).hexdigest() in _CHUOI_CHO_PHEP for v in vế):
                return False
    return gap == set(_CHUOI_CHO_PHEP)


# Câu PHỦ ĐỊNH được phép xuất hiện trong đầu ra (thông báo pull/load); bóc nó ra rồi mới tìm gợi ý dương.
_PHU_DINH = "KHÔNG bằng `nlm login --check`"
_CANH = "SENTINEL-COOKIE-wp727"


def _vi_pham_dau_ra(van_ban, phai_co):
    """Không gợi ý `login --check`, không lộ cookie, có dấu nhánh `phai_co` (thiếu ⇒ nhánh không được đi tới)."""
    return ((["gợi ý login --check"] if "login --check" in van_ban.replace(_PHU_DINH, "") else [])
            + (["lộ chuỗi canh cookie"] if _CANH in van_ban else [])
            + [f"thiếu dấu nhánh {d!r}" for d in phai_co if d not in van_ban])


@contextlib.contextmanager
def _home_tam():
    import tempfile
    with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {"HOME": d, "USERPROFILE": d}):
        yield d


def _nhanh_goi_y(tg):
    """Chạy offline TỪNG nhánh gợi ý WP727 sửa (blob token giả, HOME tạm, không mạng) ⇒ [(tên, văn bản, dấu nhánh)]."""
    import importlib
    import json
    store = tg._imp("gws_cred_store")
    jar = {"auth.json": _CANH, "profiles/default/cookies.json": "[]"}
    tok = "offline-test-token"
    blob = store.encrypt(json.dumps(jar).encode("utf-8"), tok)
    nlm_ops = importlib.import_module("tl_core.nlm_ops")
    rot = lambda *a, **k: {"found": True, "expired": True, "name": "__Secure-OFFLINE", "expires_in_min": -5.0}
    kq = [("tuoi-cookie", tg._nlm_cookie_age_note(20.0), ("NGÀY tuổi", "pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath"))]
    kq.append(("load-thieu-fid", tg._nlm_auth_load(tok, "")[1], ("NLM_CRED_FILEID", "canary")))
    with _home_tam(), _va(tg, _public_curl_bytes=lambda *a, **k: blob, _nlm_auth_files_raw=lambda: {},
                          _nlm_auth_load_downgrade=lambda *a: (True, "OFFLINE-cu-hon")):
        kq.append(("load-ha-cap", tg._nlm_auth_load(tok, "OFFLINE")[1], ("HẠ CẤP", "pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath")))
    with _home_tam(), _va(tg, _public_curl_bytes=lambda *a, **k: blob, _nlm_auth_files_raw=lambda: {},
                          _nlm_auth_load_downgrade=lambda *a: (False, ""), _nlm_auth_age_days=lambda _n: 20.0), \
            _va(nlm_ops, _nlm_rotation_token_state=rot):
        kq.append(("load-xoay-het-han", tg._nlm_auth_load(tok, "OFFLINE")[1],
                   ("BUNDLE_ROTATION_TOKEN_EXPIRED", "NGÀY tuổi", "pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath")))
    ra = io.StringIO()
    ns = argparse.Namespace(config=None, profile=None, cred_file_id="OFFLINE", force=False)
    with _va(tg, load_creds=lambda *a, **k: None, _nlm_auth_load=lambda *a, **k: (True, "OFFLINE-msg")), \
            contextlib.redirect_stdout(ra), contextlib.redirect_stderr(ra):
        tg.cmd_nlm_auth_load(ns)
    kq.append(("lenh-load", ra.getvalue(), ("[nlm-auth-load] ✓", "nlm-auth-status")))
    goi = store.encrypt(json.dumps({"nlm_auth": jar}).encode("utf-8"), "offline-master")
    ra = io.StringIO()
    ns = argparse.Namespace(config=None, profile=None, secrets_id="OFFLINE", env=None)
    with _home_tam(), _va(tg, _master_key=lambda: "offline-master", load_creds=lambda *a, **k: None,
                          _secrets_fetch=lambda *a, **k: (goi, "OFFLINE"), _nlm_auth_age_days=lambda _n: 20.0), \
            _va(nlm_ops, _nlm_rotation_token_state=lambda *a, **k: {"found": False}), \
            contextlib.redirect_stdout(ra), contextlib.redirect_stderr(ra):
        tg.cmd_nlm_auth_pull(ns)
    kq.append(("lenh-pull", ra.getvalue(), ("[nlm-auth-pull] ✓", "NGÀY tuổi", "nlm-auth-status")))
    return kq


def _n5(tg):
    nhanh = _nhanh_goi_y(tg)
    if any(_vi_pham_dau_ra(van_ban, dau) for _ten, van_ban, dau in nhanh):
        return False
    # Phản chứng cho chính bộ kiểm: gợi ý dương kiểu cũ, lộ cookie, hoặc nhánh không được đi tới đều phải bị bắt.
    return all(_vi_pham_dau_ra(x, d) for x, d in (("Kiểm: nlm login --check.", ()), ("ok " + _CANH, ()),
                                                   (_PHU_DINH + "; Kiểm: nlm login --check", ()), ("", ("HẠ CẤP",))))


def run(tl_module):
    tg = tl_module._imp("tl_gws")
    tg.bind(tl_module)      # như tl.build_parser: nạp tên trần (_imp, load_creds…) mà các lệnh stage cần
    van_ban = Path(tg.__file__).read_text(encoding="utf-8")
    phan_chung_dong = (van_ban + "    print('Kiểm: nlm login --check')\n",        # dòng kiểu cũ
                       van_ban.replace("[nguồn {src}]. Kiểm bằng probe",           # chen vào CHÍNH dòng được phép
                                       "[nguồn {src}]. Kiểm: nlm login --check. Kiểm bằng probe", 1))
    phan_chung_ast = (van_ban + '\nprint("Kiểm: nlm " "login --check")\n',         # hai literal liền nhau (F2b)
                      van_ban + '\nprint(f"x{1}" + " Kiểm: nlm log" + "in --check")\n',   # nối `+` (lượt 3, F2c)
                      van_ban + "\nx = f\"Kiểm: nlm {'login'} --check\"\n")             # `{hằng}` (lượt 4, F2d)
    goi = van_ban.count("_refresh_nlm_auth()") - 1   # trừ dòng `def`; MỌI người gọi phải dừng khi refresh quá hạn
    return (goi == 3 == van_ban.count("_refresh_nlm_auth() is None") and _n4(van_ban) and not any(map(_n4, phan_chung_dong)) and _n4_ast(van_ban)
            and not any(map(_n4_ast, phan_chung_ast)) and _n1_n3(tg) and _n2(tg) and _n5(tg))
