"""Chạy Bash THẬT (không đổi tên tệp, tệp dựng đúng đường dẫn trong thân) trên thân mà đột biến sống sót nhận, tham chiếu từ chối."""
import os, sys, json, subprocess, tempfile, pathlib
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "soan"); sys.path.insert(0, S); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gram
from song_sot_v3 import MUT
SH = {None: ["/usr/bin/bash", "-e"], "bash": ["/usr/bin/bash", "--noprofile", "--norc", "-eo", "pipefail"]}
HONG_PY = "import pathlib; pathlib.Path('DA_CHAY').touch(); raise SystemExit(1)\n"
QUA_PY = "import sys; sys.stdout.write(sys.stdin.read())\n"
CA = [  # (đột biến, thân, shell)
 ("v3a_bash_P_khong_trang", "bash ops/hong.sh||true||x.sh", None),
 ("v3b_pwsh_P_khong_trang", "pwsh -NoProfile -File ops/hong.ps1||true||x.ps1", None),
 ("v3c_bash_tuy_chon_truoc_P", "bash -n ops/hong.sh", None),
 ("v3c_bash_tuy_chon_truoc_P", "bash -s ops/hong.sh", None),
 ("v3d_python_tuy_chon_truoc_P", "python -h ops/hong_test.py", None),
 ("v3f_ong_hoac_lenh_cuoi", "python ops/hong_test.py | python ops/qua.py || python ops/qua.py", "bash"),
 ("v3h_ong_cham_than_ve_phai", "python ops/qua.py | ! python ops/hong_test.py", "bash"),
]
kq = []
for ten, than, sh in CA:
    run = than + "\n"
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d); (p / "ops").mkdir(); (p / "bin").mkdir()
        os.symlink(sys.executable, p / "bin/python")
        (p / "ops/hong_test.py").write_text(HONG_PY); (p / "ops/qua.py").write_text(QUA_PY)
        (p / "ops/hong.sh").write_text("touch DA_CHAY\nexit 1\n")
        (p / "ops/hong.ps1").write_text(HONG_PY)
        # container không có pwsh: pwsh GIẢ chạy đối số tệp bằng Python (như sinh_r8.py); bash là /usr/bin/bash THẬT
        (p / "bin/pwsh").write_text(f"#!/bin/sh\nwhile [ $# -gt 0 ]; do case $1 in -*) shift;; *) exec {sys.executable} \"$@\";; esac; done\n"); (p / "bin/pwsh").chmod(0o755)
        (p / "s.sh").write_text(run)
        r = subprocess.run(SH[sh] + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d}, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=20)
        dc = (p / "DA_CHAY").exists()
    x = {"dot_bien": ten, "than": than, "shell": sh, "tham_chieu": gram.cu_phap_run(run, sh), "dot_bien_nhan": MUT[ten](run, sh) is None,
         "rc": r.returncode, "DA_CHAY": dc, "loai": "nuot_that" if r.returncode == 0 and dc else ("khong_chay_rc0" if r.returncode == 0 else "rc_khac_0"),
         "stderr": r.stderr.strip()[:90]}
    kq.append(x); print(json.dumps(x, ensure_ascii=False))
json.dump(kq, open("bash_that_v3.json", "w"), ensure_ascii=False, indent=1)
