# -*- coding: utf-8 -*-
"""wp726 — ba script shell NLM phán sống/chết bằng canary, không bằng `nlm login --check`, không nuốt mã thoát.

Chạy BẢN THẬT của `nlm-auto-refresh.sh`, `env-reimport.sh`, `nlm-auth-import.sh` bằng `bash` với `TL_ROOT` trỏ
một gốc giả: `scripts/tl.py` giả (vừa là module cho probe canary, vừa là CLI), `nlm`/`gws` giả trên PATH. Đồ giả
GIỮ TRẠNG THÁI qua một tệp JSON — `nlm login --check` LUÔN báo "valid" (false-green), còn canary và mã của
`nlm-auth-stage` là hai biến độc lập — và ghi nhật ký mọi lời gọi. Mọi đồ giả in một chuỗi canh; đầu ra của
script không được chứa nó.
"""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


TEST_ID = "wp726_script_nlm_canary"

_CANH = "SENTINEL-COOKIE-wp726"

_TL_GIA = r'''
import json, os, sys
_ST = os.environ["WP726_STATE"]
_LOG = os.environ["WP726_LOG"]
NLM_CRED_FILEID = "FAKE-NLM-CRED"

def _ghi(dong):
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write(dong + "\n")

def _trang_thai():
    with open(_ST, encoding="utf-8") as f:
        return json.load(f)

def _imp(name):
    return sys.modules[__name__]

def bind(_m):
    return None

def _nlm_canary_notebook(nb):
    return "NB-OFFLINE"

def _nlm_auth_alive(nb, require_notebook_body=False):
    _ghi("canary require_body=%s" % require_notebook_body)
    print("%s canary" % os.environ.get("WP726_CANH", ""))
    if not require_notebook_body:
        return True, "rc0-only"          # probe lỏng = false-green: chỉ phép đo đòi THÂN mới thấy canary thật
    return _trang_thai()["canary"], "OFFLINE"

if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else ""
    _ghi("tl " + " ".join(sys.argv[1:]))
    print("%s tl %s" % (os.environ.get("WP726_CANH", ""), lenh))
    print("%s" % os.environ.get("WP726_CANH", ""), file=sys.stderr)
    if lenh == "ping":
        print('{"ok": true, "version": "offline"}')
    elif lenh == "nlm-auth-stage":
        st = _trang_thai()
        day = st.get("stage_seq")          # chuỗi mã theo thứ tự gọi (vd. 5 rồi 0) — trạng thái, không kịch bản
        if day:
            st["stage_seq"] = day[1:] or day
            with open(_ST, "w", encoding="utf-8") as f:
                json.dump(st, f)
            sys.exit(day[0])
        sys.exit(st["stage_rc"])
    elif lenh == "nlm-auth-load":
        sys.exit(_trang_thai().get("load_rc", 0))
    elif lenh == "doctor":                  # dạng dòng THẬT của doctor: nhãn — chi tiết (chi tiết có thể mang lỗi thô)
        canh = os.environ.get("WP726_CANH", "")
        print("✓ nlm auth (LIVE probe) — PROBE_INCONCLUSIVE (không phải auth): " + canh)
        print("⚠ gws credential — " + canh)
    sys.exit(0)
'''

_CONVERT_GIA = r'''
import pathlib, sys
pathlib.Path(sys.argv[2]).mkdir(parents=True, exist_ok=True)
(pathlib.Path(sys.argv[2]) / "cookies.json").write_text("[]", encoding="utf-8")
'''

_NLM_GIA = '''#!/usr/bin/env bash
echo "nlm $*" >> "$WP726_LOG"
echo "$WP726_CANH"
case "$1 $2" in
  "login --check") echo "Authentication valid. Notebooks found: 7"; exit 0 ;;
esac
exit 0
'''

_GWS_GIA = r'''
import json, os, sys
a = sys.argv[1:]
with open(os.environ["WP726_LOG"], "a", encoding="utf-8") as f:
    f.write("gws " + " ".join(a) + "\n")
with open(os.environ["WP726_STATE"], encoding="utf-8") as f:
    st = json.load(f)
lenh = " ".join(a[:3])
if lenh == "drive files list":
    tep = [{"id": "EXPORT-1", "name": "nlm-auth-x.json", "modifiedTime": "2026-10-01T00:00:00Z"}] if st.get("export") else []
    print(json.dumps({"files": tep}))
elif lenh == "drive files get":
    if "--output" in a:
        with open(a[a.index("--output") + 1], "w", encoding="utf-8") as f:
            f.write('[{"name": "SID", "value": "x", "domain": ".google.com"}]')
    else:
        print("{}")
'''


def _dung_goc(tam, kho):
    goc = tam / "goc"
    (goc / "scripts").mkdir(parents=True)
    (goc / "scripts" / "tl.py").write_text(_TL_GIA, encoding="utf-8")
    (goc / "scripts" / "nlm_auth_convert.py").write_text(_CONVERT_GIA, encoding="utf-8")
    bin_ = tam / "bin"
    bin_.mkdir()
    for ten, noi_dung in (("nlm", _NLM_GIA), ("gws", "#!" + sys.executable + "\n" + _GWS_GIA)):
        p = bin_ / ten
        p.write_text(noi_dung, encoding="utf-8")
        p.chmod(0o755)
    # `nlm-auto-refresh.sh` gọi `./scripts/nlm-auth-import.sh` TƯƠNG ĐỐI gốc ⇒ đặt BẢN THẬT vào gốc giả.
    shutil.copy2(kho / "scripts" / "nlm-auth-import.sh", goc / "scripts" / "nlm-auth-import.sh")
    (tam / "home").mkdir()
    cookie = tam / "cookie.json"
    cookie.write_text('[{"name": "SID", "value": "x", "domain": ".google.com"}]', encoding="utf-8")
    return goc, bin_, cookie


def _bin_khong_nlm(tam, bin_):
    """Thư mục bin chỉ có `gws` giả — dựng ca THIẾU nlm (lượt review 2, F6)."""
    b = tam / "bin_khong_nlm"
    if not b.exists():
        b.mkdir()
        shutil.copy2(bin_ / "gws", b / "gws")
    return b


def _chay(bash, kho, tam, goc, bin_, script, args, trang_thai):
    st = tam / "state.json"
    log = tam / "calls.log"
    st.write_text(json.dumps(trang_thai), encoding="utf-8")
    log.write_text("", encoding="utf-8")
    env = {
        "PATH": (f"{_bin_khong_nlm(tam, bin_)}{os.pathsep}{os.path.dirname(sys.executable)}{os.pathsep}/usr/bin:/bin"
                 if trang_thai.get("khong_nlm") else f"{bin_}{os.pathsep}{os.environ.get('PATH', '')}"),
        "HOME": str(tam / "home"),
        "TL_ROOT": str(goc),
        "TL_PYTHON": sys.executable,
        "TL_TOKEN": "offline-test-token",
        "WP726_STATE": str(st),
        "WP726_LOG": str(log),
        "WP726_CANH": _CANH,
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    r = subprocess.run([bash, str(kho / "scripts" / script), *args], env=env, cwd=str(goc),
                       capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout + r.stderr, log.read_text(encoding="utf-8").splitlines()


def _sach(out, calls):
    """Không lộ chuỗi canh, không có lời gọi `nlm login --check`."""
    return _CANH not in out and not any(c.startswith("nlm login --check") for c in calls)


def _ca(bash, kho):
    kq = {}
    with tempfile.TemporaryDirectory(prefix="wp726_") as td:
        tam = Path(td)
        goc, bin_, cookie = _dung_goc(tam, kho)

        def chay(script, args, canary, stage_rc, **them):
            return _chay(bash, kho, tam, goc, bin_, script, args, {"canary": canary, "stage_rc": stage_rc, **them})

        # nlm-auto-refresh.sh — phán quyết = mã của nlm-auth-stage; rc 4 hỏi lại canary: chỉ ÂM mới là chết (3),
        # không kết luận / lệch nhau là 2 (GitHub review #730, P2)
        for ten, canary, stage_rc, ma in (("tu_dong_song", None, 0, 0), ("tu_dong_chet", False, 4, 3),
                                          ("tu_dong_khong_ro", None, 4, 2), ("tu_dong_lech", True, 4, 2),
                                          ("tu_dong_ha_tang", False, 5, 2)):
            rc, out, calls = chay("nlm-auto-refresh.sh", [], canary, stage_rc)
            n_stage = sum(1 for c in calls if c == "tl nlm-auth-stage")
            kq[ten] = rc == ma and n_stage == 1 and ("NLM CHẾT" in out) == (ma == 3) and _sach(out, calls)

        # nlm-auto-refresh.sh — có export MỚI: import (canary + stage) rồi KHÔNG stage lần hai; chỉ xoá plaintext
        # khi import+stage thành công (lượt review 1, F2)
        # Import hỏng ⇒ thoát 2, KHÔNG stage lần hai, KHÔNG xoá, không báo sống — kể cả stage 5 rồi 0 (review #730, P1)
        for ten, canary, stage, ma, can_stage, can_xoa in (("tu_dong_export_song", True, 0, 0, 1, 1),
                                                           ("tu_dong_export_stage_loi", True, 4, 2, 1, 0),
                                                           ("tu_dong_export_5_roi_0", True, [5, 0], 2, 1, 0),
                                                           ("tu_dong_export_chet", False, 0, 2, 0, 0)):
            them = {"stage_seq": stage} if isinstance(stage, list) else {}
            rc, out, calls = chay("nlm-auto-refresh.sh", [], canary, 0 if them else stage, export=True, **them)
            n_stage = sum(1 for c in calls if c == "tl nlm-auth-stage")
            n_xoa = sum(1 for c in calls if c.startswith("gws drive files delete"))
            kq[ten] = (rc == ma and n_stage == can_stage and n_xoa == can_xoa and ("bundle tươi)" in out) == (ma == 0)
                       and _sach(out, calls))

        # env-reimport.sh — nlm-auth-load lỗi: chỉ báo mã, không in đầu ra lệnh (lượt review 1, F3)
        rc, out, calls = chay("env-reimport.sh", [], True, 0, load_rc=5)
        kq["env_load_loi_khong_lo"] = rc == 0 and "nlm-auth-load lỗi (rc=5)" in out and _sach(out, calls)

        # env-reimport.sh — THIẾU nlm (có/không --check): không được báo "đều sống", rc 4, 0 canary (lượt 2, F6)
        for ten, tham in (("env_thieu_nlm", []), ("env_thieu_nlm_check", ["--check"])):
            rc, out, calls = chay("env-reimport.sh", tham, True, 0, khong_nlm=True)
            kq[ten] = (rc == 4 and "đều sống" not in out
                       and not any(c.startswith("canary") for c in calls) and _sach(out, calls))

        # env-reimport.sh — canary đòi thân đúng notebook
        for ten, canary, ma in (("env_song", True, 0), ("env_chet", False, 3), ("env_khong_ro", None, 4)):
            rc, out, calls = chay("env-reimport.sh", [], canary, 0)
            kq[ten] = (rc == ma and "canary require_body=True" in calls
                       and not any(c.startswith("tl nlm-auth-stage") for c in calls) and _sach(out, calls))

        # nlm-auth-import.sh — bước 4 canary, bước 5 phân biệt rc của stage
        tham = ["--file", str(cookie)]
        for ten, canary, stage_rc, ma, can_stage in (
                ("nhap_chet", False, 0, 4, 0), ("nhap_khong_ro", None, 0, 6, 0), ("nhap_song", True, 0, 0, 1),
                ("nhap_stage_4", True, 4, 5, 1), ("nhap_stage_5", True, 5, 5, 1)):
            rc, out, calls = chay("nlm-auth-import.sh", tham, canary, stage_rc)
            n_stage = sum(1 for c in calls if c == "tl nlm-auth-stage")
            kq[ten] = rc == ma and n_stage == can_stage and _sach(out, calls)
            kq[ten + "_out"] = out
    ok_4_5 = ("canary của lệnh stage KHÔNG dương" in kq.pop("nhap_stage_4_out")
              and "lỗi stage" in kq.pop("nhap_stage_5_out"))
    for k in [k for k in kq if k.endswith("_out")]:
        kq.pop(k)
    kq["nhap_phan_biet_4_5"] = ok_4_5
    return kq


def _bash_nen(kho):
    """`ops/bash_nen.py` của kho (cổng cấm `bash` TRẦN — Issue #570). None khi cây không mang `ops/` (gói phát hành)."""
    p = kho / "ops" / "bash_nen.py"
    if not p.is_file():
        return None
    spec = importlib.util.spec_from_file_location("_wp726_bash_nen", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(tl_module):
    kho = Path(tl_module.__file__).resolve().parent.parent
    bash_nen = _bash_nen(kho)
    if os.name != "posix" or bash_nen is None:
        # Lệch có khai so với spec N6: API fragment chỉ có đúng/sai, không có trạng thái `skipped`. Nền không POSIX
        # (Windows) và cây phát hành (không mang `ops/bash_nen.py`, bộ tìm bash DUY NHẤT được phép) không chạy ca
        # này; ca trả True và in lý do — handoff khai riêng.
        print("[wp726_script_nlm_canary] BỎ QUA (os.name=%s, ops/bash_nen.py %s)"
              % (os.name, "có" if bash_nen else "vắng"), file=sys.stderr)
        return True
    bash, _chan_doan = bash_nen.tim_bash()
    if not bash:
        return False                     # cây dev POSIX mà không có bash dùng được ⇒ ĐỎ, không tha
    kq = _ca(bash, kho)
    return bool(kq) and all(kq.values())
