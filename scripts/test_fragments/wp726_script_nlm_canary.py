# -*- coding: utf-8 -*-
"""wp726 — ba script shell NLM phán sống/chết bằng canary, không bằng `nlm login --check`, không nuốt mã thoát.

Chạy BẢN THẬT của `nlm-auto-refresh.sh`, `env-reimport.sh`, `nlm-auth-import.sh` bằng `bash` với `TL_ROOT` trỏ
một gốc giả: `scripts/tl.py` giả (vừa là module cho probe canary, vừa là CLI), `nlm`/`gws` giả trên PATH. Đồ giả
GIỮ TRẠNG THÁI qua một tệp JSON — `nlm login --check` LUÔN báo "valid" (false-green), còn canary và mã của
`nlm-auth-stage` là hai biến độc lập — và ghi nhật ký mọi lời gọi. Mọi đồ giả in một chuỗi canh; đầu ra của
script không được chứa nó.
"""

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
        sys.exit(_trang_thai()["stage_rc"])
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

_GWS_GIA = '''#!/usr/bin/env bash
echo "gws $*" >> "$WP726_LOG"
case "$1 $2 $3" in
  "drive files list") echo '{"files":[]}' ;;
  "drive files get") echo '{}' ;;
esac
exit 0
'''


def _dung_goc(tam, kho):
    goc = tam / "goc"
    (goc / "scripts").mkdir(parents=True)
    (goc / "scripts" / "tl.py").write_text(_TL_GIA, encoding="utf-8")
    (goc / "scripts" / "nlm_auth_convert.py").write_text(_CONVERT_GIA, encoding="utf-8")
    bin_ = tam / "bin"
    bin_.mkdir()
    for ten, noi_dung in (("nlm", _NLM_GIA), ("gws", _GWS_GIA)):
        p = bin_ / ten
        p.write_text(noi_dung, encoding="utf-8")
        p.chmod(0o755)
    (tam / "home").mkdir()
    cookie = tam / "cookie.json"
    cookie.write_text('[{"name": "SID", "value": "x", "domain": ".google.com"}]', encoding="utf-8")
    return goc, bin_, cookie


def _chay(bash, kho, tam, goc, bin_, script, args, trang_thai):
    st = tam / "state.json"
    log = tam / "calls.log"
    st.write_text(json.dumps(trang_thai), encoding="utf-8")
    log.write_text("", encoding="utf-8")
    env = {
        "PATH": f"{bin_}{os.pathsep}{os.environ.get('PATH', '')}",
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

        def chay(script, args, canary, stage_rc):
            return _chay(bash, kho, tam, goc, bin_, script, args, {"canary": canary, "stage_rc": stage_rc})

        # nlm-auto-refresh.sh — phán quyết = mã của nlm-auth-stage
        for ten, stage_rc, ma in (("tu_dong_song", 0, 0), ("tu_dong_chet", 4, 3), ("tu_dong_ha_tang", 5, 2)):
            rc, out, calls = chay("nlm-auto-refresh.sh", [], None, stage_rc)
            n_stage = sum(1 for c in calls if c == "tl nlm-auth-stage")
            kq[ten] = rc == ma and n_stage == 1 and _sach(out, calls)

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


def _tim_bash():
    if os.name != "posix":
        return None
    return shutil.which("bash")


def run(tl_module):
    if os.name != "posix":
        # Lệch có khai so với spec N6: API fragment chỉ có đúng/sai, không có trạng thái `skipped`. Nền không POSIX
        # (Windows) không chạy được ba script này với đồ giả; ca trả True và in lý do — handoff khai riêng.
        print("[wp726_script_nlm_canary] BỎ QUA trên nền không POSIX (os.name=%s)" % os.name, file=sys.stderr)
        return True
    bash = _tim_bash()
    if not bash:
        return False                     # Linux/macOS thiếu bash ⇒ ĐỎ, không tha
    kho = Path(tl_module.__file__).resolve().parent.parent
    kq = _ca(bash, kho)
    return bool(kq) and all(kq.values())
