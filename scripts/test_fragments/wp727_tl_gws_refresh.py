# -*- coding: utf-8 -*-
"""wp727 — `_refresh_nlm_auth` gọi `nlm auth refresh` (không còn `nlm login --check`) và KHÔNG mở được cổng.

N1 argv/timeout · N2 refresh trả True mà canary False/None ⇒ 0 upload, rc 4 (kể cả --refresh --force), canary
True ⇒ đúng 1 upload · N3 lỗi của refresh không lan và không chặn canary · N4 `login --check` trong tl_gws.py chỉ
nằm ở các dòng thuộc danh sách CHO PHÉP.
"""

import argparse
import contextlib
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
        self.stderr = ""


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


def _stage(tg, canary, refresh_rc=0):
    """Chạy `nlm-auth-stage --refresh --force` với nlm giả; trả (rc, số upload, thứ tự sự kiện)."""
    su_kien, upload = [], []

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
                    _stage_enc_upload=lambda *a, **k: (upload.append(1) or ("OFFLINE", True))), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = tg.cmd_nlm_auth_stage(ns)
    finally:
        if env_cu is None:
            os.environ.pop("TL_TOKEN", None)
        else:
            os.environ["TL_TOKEN"] = env_cu
    return rc, len(upload), su_kien


def _n2(tg):
    for canary in (False, None):
        for refresh_rc in (0, 1):
            rc, n_up, su_kien = _stage(tg, canary, refresh_rc)
            if rc != 4 or n_up != 0 or su_kien[:1] != ["refresh"] or "canary" not in su_kien:
                return False
    rc, n_up, su_kien = _stage(tg, True, 0)
    return rc == 0 and n_up == 1 and su_kien.index("refresh") < su_kien.index("canary")


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
    return _n1_n3(tg) and _n2(tg)
