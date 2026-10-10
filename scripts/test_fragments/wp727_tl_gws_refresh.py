# -*- coding: utf-8 -*-
"""wp727 — `_refresh_nlm_auth` gọi `nlm auth refresh` (không còn `nlm login --check`) và KHÔNG mở được cổng.

N1 argv/timeout · N2 refresh trả True mà canary False/None ⇒ 0 upload, rc 4 (kể cả --refresh --force), canary
True ⇒ đúng 1 upload · N3 lỗi của refresh không lan và không chặn canary · N4 `login --check` trong tl_gws.py chỉ
nằm ở các dòng thuộc danh sách CHO PHÉP (kiểm TĨNH, phụ) · N5 đầu ra THẬT của từng nhánh gợi ý WP727 sửa (tuổi cookie,
load thiếu fileId / hạ cấp / token xoay hết hạn, lệnh load, lệnh pull) không gợi ý `login --check` và không lộ cookie.
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


@contextlib.contextmanager
def _va(module, **thay):
    cu = {k: getattr(module, k) for k in thay}
    try:
        for k, v in thay.items():
            setattr(module, k, v)
        yield
    finally:
        for k, v in cu.items():
            setattr(module, k, v)


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
    if (argv[1:] != ["auth", "refresh"] or "--check" in argv or isinstance(timeout, bool)
            or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0):
        return False

    def treo(a, k):
        raise subprocess.TimeoutExpired(a, k.get("timeout"))

    def hong(a, k):
        raise OSError("no exec")

    return _goi_refresh(tg, treo)[0] is False and _goi_refresh(tg, hong)[0] is False


def _stage(tg, canary, refresh_rc=0, ket_qua_ra=None):
    """Chạy `nlm-auth-stage --refresh --force` với nlm giả, cookie GIÀ (20 ngày ⇒ có in ghi chú tuổi);
    trả (rc, số upload, thứ tự sự kiện). `ket_qua_ra` (list) nhận stdout+stderr của lệnh."""
    su_kien, upload = [], []
    ra, loi = io.StringIO(), io.StringIO()

    def run(argv, **kw):
        su_kien.append("refresh")
        return _Ket(refresh_rc)

    def alive(nb, **kw):
        su_kien.append("canary")
        return canary, "OFFLINE"

    import shutil
    ns = argparse.Namespace(refresh=True, force=True, folder=None, cred_file_id="OFFLINE", new=False,
                            config=None, profile=None)
    env_cu = os.environ.get("TL_TOKEN")
    os.environ["TL_TOKEN"] = "offline-test-token"
    try:
        with _va(subprocess, run=run), _va(shutil, which=lambda name: "/fake/bin/nlm"), \
                _va(tg, _nlm_auth_alive=alive,
                    _nlm_auth_files=lambda: (su_kien.append("jar") or {"auth.json": "offline-jar"}),
                    _stage_enc_upload=lambda *a, **k: (upload.append(1) or ("OFFLINE", True)),
                    _nlm_auth_age_days=lambda _nlm: 20.0), \
                contextlib.redirect_stdout(ra), contextlib.redirect_stderr(loi):
            rc = tg.cmd_nlm_auth_stage(ns)
    finally:
        if env_cu is None:
            os.environ.pop("TL_TOKEN", None)
        else:
            os.environ["TL_TOKEN"] = env_cu
    if ket_qua_ra is not None:
        ket_qua_ra.append(ra.getvalue() + loi.getvalue())
    return rc, len(upload), su_kien


def _n2(tg):
    for canary in (False, None):
        for refresh_rc in (0, 1):
            rc, n_up, su_kien = _stage(tg, canary, refresh_rc)
            if rc != 4 or n_up != 0 or su_kien[:1] != ["refresh"] or "canary" not in su_kien:
                return False
    dau_ra = []
    rc, n_up, su_kien = _stage(tg, True, 0, dau_ra)
    # ĐO ĐẦU RA THẬT (lượt 3, F2c): cookie già ⇒ lệnh in ghi chú tuổi; mọi cách dựng chuỗi (literal, `+`, %, format…)
    # đều hiện ra ở đây — không được có `login --check`, không được lộ chuỗi canh của tiến trình con.
    ra = dau_ra[0]
    return (rc == 0 and n_up == 1 and su_kien.index("refresh") < su_kien.index("canary")
            and "NGÀY tuổi" in ra and "login --check" not in ra and "SENTINEL-COOKIE" not in ra)


def _n4(van_ban):
    """Mọi dòng nhắc `login --check` phải BẰNG NGUYÊN VĂN một dòng cho phép, mỗi dòng cho phép đúng một lần."""
    dung = {neo: 0 for neo in _CHO_PHEP}
    for dong in van_ban.splitlines():
        if "login --check" not in dong:
            continue
        neo = dong.strip()
        if neo not in dung:
            return False
        dung[neo] += 1
    return all(n == 1 for n in dung.values())


# sha256 của TOÀN VĂN mỗi chuỗi Python (sau khi ghép literal liền nhau; f-string: phần hằng + "{}") được phép chứa
# `login --check` — chặn cả gợi ý dương viết tách thành nhiều literal (cross-review lượt 2, F2b).
_CHUOI_CHO_PHEP = frozenset({
    "a4b85ff4f950bfb6229494d8dd99fbfdb412490ad5b2a190971e5cef343a7e05",   # docstring _nlm_auth_alive (M1)
    "73818ecbc71850b0fd01b94be79d0eefb95ca7e78fd9adf941b4ae778bba6264",   # docstring _refresh_nlm_auth (WP727)
    "bdb136eb46706b57fcf701c877904c9f27c0d1f9b7f0b3ed0ca0ee78d02eb0a9",   # thông báo nlm-auth-pull
    "a2e363f715ec74d607f55eb2f4a3821d0f6eda93e0be5e654d8831fc9985d6b5",   # thông báo nlm-auth-load
})


def _phan_f(v):
    """Một mảnh f-string: hằng giữ nguyên; `{hằng}` không chuyển đổi/định dạng thì thay bằng str(hằng) (lượt 4, F2d —
    trước đó mọi `{…}` thành "{}" nên `f"Kiểm: nlm {'login'} --check"` lọt); còn lại không chứng minh được ⇒ "{}"."""
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
        if trai is not None and phai is not None:
            return trai + phai
        return trai if phai is None and trai is not None else phai
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
    """Đầu ra/thông báo THẬT của một nhánh gợi ý: không gợi ý `login --check`, không lộ cookie, và có dấu nhánh
    (`phai_co`) — thiếu dấu nghĩa là nhánh không được đi tới, tức phép đo không đo gì."""
    loi = []
    if "login --check" in van_ban.replace(_PHU_DINH, ""):
        loi.append("gợi ý login --check")
    if _CANH in van_ban:
        loi.append("lộ chuỗi canh cookie")
    loi.extend(f"thiếu dấu nhánh {d!r}" for d in phai_co if d not in van_ban)
    return loi


@contextlib.contextmanager
def _home_tam():
    import tempfile
    cu = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE")}
    with tempfile.TemporaryDirectory() as d:
        try:
            os.environ["HOME"] = os.environ["USERPROFILE"] = d
            yield d
        finally:
            for k, v in cu.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


def _nhanh_goi_y(tg):
    """Chạy offline TỪNG nhánh gợi ý mà WP727 sửa, trả [(tên, văn bản thật, dấu nhánh phải có)].
    Không mạng, không credential: blob mã hoá bằng token giả, HOME tạm, mọi I/O ngoài bị thay."""
    import importlib
    import json
    store = tg._imp("gws_cred_store")
    jar = {"auth.json": _CANH, "profiles/default/cookies.json": "[]"}
    tok = "offline-test-token"
    blob = store.encrypt(json.dumps(jar).encode("utf-8"), tok)
    nlm_ops = importlib.import_module("tl_core.nlm_ops")
    rot = lambda *a, **k: {"found": True, "expired": True, "name": "__Secure-OFFLINE", "expires_in_min": -5.0}
    kq = [("tuoi-cookie", tg._nlm_cookie_age_note(20.0), ("NGÀY tuổi", "nlm-credential-refresh.ps1"))]
    kq.append(("load-thieu-fid", tg._nlm_auth_load(tok, "")[1], ("NLM_CRED_FILEID", "canary")))
    with _home_tam(), _va(tg, _public_curl_bytes=lambda *a, **k: blob, _nlm_auth_files_raw=lambda: {},
                          _nlm_auth_load_downgrade=lambda *a: (True, "OFFLINE-cu-hon")):
        kq.append(("load-ha-cap", tg._nlm_auth_load(tok, "OFFLINE")[1], ("HẠ CẤP", "nlm-credential-refresh.ps1")))
    with _home_tam(), _va(tg, _public_curl_bytes=lambda *a, **k: blob, _nlm_auth_files_raw=lambda: {},
                          _nlm_auth_load_downgrade=lambda *a: (False, ""), _nlm_auth_age_days=lambda _n: 20.0), \
            _va(nlm_ops, _nlm_rotation_token_state=rot):
        kq.append(("load-xoay-het-han", tg._nlm_auth_load(tok, "OFFLINE")[1],
                   ("BUNDLE_ROTATION_TOKEN_EXPIRED", "NGÀY tuổi", "nlm-credential-refresh.ps1")))
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
    return (bool(_vi_pham_dau_ra("Kiểm: nlm login --check.", ()))
            and bool(_vi_pham_dau_ra(_PHU_DINH + "; Kiểm: nlm login --check", ()))
            and bool(_vi_pham_dau_ra("ok " + _CANH, ()))
            and bool(_vi_pham_dau_ra("", ("HẠ CẤP",))))


def run(tl_module):
    tg = tl_module._imp("tl_gws")
    tg.bind(tl_module)      # như tl.build_parser: nạp tên trần (_imp, load_creds…) mà các lệnh stage cần
    van_ban = Path(tg.__file__).read_text(encoding="utf-8")
    if not _n4(van_ban):
        return False
    if _n4(van_ban + "    print('Kiểm: nlm login --check')\n"):     # phản chứng: dòng kiểu cũ phải bị bắt
        return False
    if _n4(van_ban.replace("[nguồn {src}]. Kiểm bằng probe", "[nguồn {src}]. Kiểm: nlm login --check. Kiểm bằng probe", 1)):
        return False            # phản chứng: gợi ý dương chen vào CHÍNH dòng được phép cũng phải bị bắt
    if not _n4_ast(van_ban):
        return False
    if _n4_ast(van_ban + '\nprint("Kiểm: nlm " "login --check")\n'):
        return False            # phản chứng: gợi ý dương tách thành hai literal liền nhau phải bị bắt
    if _n4_ast(van_ban + '\nprint(f"x{1}" + " Kiểm: nlm log" + "in --check")\n'):
        return False            # phản chứng: gợi ý dương nối bằng `+` phải bị bắt (cross-review lượt 3, F2c)
    if _n4_ast(van_ban + "\nx = f\"Kiểm: nlm {'login'} --check\"\n"):
        return False            # phản chứng: `{hằng}` trong f-string phải được thay giá trị (cross-review lượt 4, F2d)
    return _n1_n3(tg) and _n2(tg) and _n5(tg)
