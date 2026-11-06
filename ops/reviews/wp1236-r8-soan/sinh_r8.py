"""Kho đầu vào SINH TỔ HỢP cho K7-S (ops/specs/wp1236-r8.md, ca A14-S6; reviewer Claude I01 vòng 2 r8).
Sinh tất định: (1) mọi toán tử điều khiển/cấu trúc của Bash ghép toàn bằng LENH hợp lệ; (2) mọi ký tự ngoài tập ở mọi vị trí của
DANG/P/W/dấu tách. Đòi: (a) vị từ được đo == cài đặt tham chiếu gram.py trên MỌI đầu vào sinh; (b) mọi thân được nhận, chạy Bash/sh
thật với chương trình hỏng, phải ĐÃ CHẠY chương trình ấy và rc != 0. Chạy: python3 -I ops/reviews/wp1236-r8-soan/sinh_r8.py"""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import gram
import pathlib, subprocess, tempfile

SHELL_LENH = {None: ["bash", "-e"], "bash": ["bash", "--noprofile", "--norc", "-eo", "pipefail"], "sh": ["sh", "-e"]}
HONG = "import pathlib, sys; pathlib.Path('DA_CHAY').touch(); sys.exit(1)\n"
QUA = "import sys; sys.stdout.write(sys.stdin.read())\n"


def chay_tung_thanh_phan(run, sh):
    """Thân ĐƯỢC NHẬN: với MỖI thành phần ống k, cho chương trình của k hỏng (thoát 1, ghi DA_CHAY), các thành phần khác chép stdin;
    trả [(k, rc, da_chay)]. `bash P.sh` và `pwsh -NoProfile -File P.ps1` được mô phỏng bằng một `bash`/`pwsh` GIẢ trên PATH chạy
    tệp Python cùng tên — container không có pwsh; thứ được đo là ĐƯỜNG NỐI shell, không phải chương trình."""
    import re
    tok = re.findall(r"[^\s|&;()<>]+\.(?:py|sh|ps1)", run)   # mọi tệp chương trình trong thân (kể cả thân do ĐỘT BIẾN nhận)
    out = []
    for k in range(max(len(tok), 1)):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d); (p / "bin").mkdir(); (p / "ops").mkdir()
            os.symlink(sys.executable, p / "bin/python")
            for ten in ("bash", "pwsh"):   # GIẢ: chạy đối số tệp như Python; bash thật của shell ngoài vẫn là /usr/bin/bash
                (p / "bin" / ten).write_text(f"#!/bin/sh\nwhile [ $# -gt 0 ]; do case $1 in -*) shift;; *) exec {sys.executable} \"$@\";; esac; done\n")
                (p / "bin" / ten).chmod(0o755)
            run2, vt = run, 0
            for i, t in enumerate(tok):   # đổi tên tệp của từng thành phần cho riêng, để X | X đo được
                moi = f"ops/_t{i}" + t[t.rindex("."):]
                vt = run2.index(t, vt); run2 = run2[:vt] + moi + run2[vt + len(t):]; vt += len(moi)
                (p / moi).write_text(HONG if i == k else QUA)
            (p / "s.sh").write_text(run2)
            lenh = SHELL_LENH[sh][:]
            lenh[0] = "/usr/bin/bash" if lenh[0] == "bash" else "/bin/sh"
            rc = subprocess.run(lenh + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d},
                                capture_output=True, stdin=subprocess.DEVNULL, timeout=20).returncode
            out.append((k, rc, (p / "DA_CHAY").exists()))
    return out

X, Y = "python ops/hong_test.py", "python ops/qua.py"
LENH = [X, Y, "bash ops/hong.sh", "pwsh -NoProfile -File ops/hong.ps1", f"{X} --json a=b"]
SHELL = [None, "bash", "sh"]
OP2 = ["||", "&&", ";", "&", "|", "|&", "\n", ";;", "&;", "||&", "| |"]   # A op B
TIEN = ["!", "! ", "time ", "exec ", "command ", "builtin ", "eval ", "coproc ", "{ ", "( ", "A=1 ", "-", "--", "./", "/", "~"]
HAU = [" &", "&", " ;", ";", " ||", " |", " #", "#", " \\", "\\", ")", " }", " 2>&1", " >x", " <x", "\n", "\r", " ", "  "]
KT = ";&|!(){}$`'\"\\<>#*?[]~+,@%^= \t\n\r\x00 ο١"


def kho():
    out = []
    for a in LENH:
        for b in LENH:
            for op in OP2:
                for sep in (f" {op} ", op, f"{op} ", f" {op}"):
                    out.append(a + sep + b)
        for t in TIEN:
            out.append(t + a)
        for h in HAU:
            out.append(a + h)
    goc = "python ops/ab.py w"
    for c in KT:
        for i in range(len(goc) + 1):   # chèn c vào MỌI vị trí của một LENH (DANG, P, đuôi, dấu cách, W)
            out.append(goc[:i] + c + goc[i:])
        out.append(goc.replace(" ", c))
    return sorted(set(out))


def main(vi_tu=None):
    vi_tu = vi_tu or gram.cu_phap_run
    lech, nhan, hong, n = [], 0, [], 0
    for than in kho():
        for sh in SHELL:
            for run in (than, than + "\n"):
                n += 1
                a, b = vi_tu(run, sh), gram.cu_phap_run(run, sh)
                if a != b:
                    lech.append((run, sh, a, b))
                if a is None:
                    nhan += 1
                    for k, rc, dc in chay_tung_thanh_phan(run, sh):
                        if rc == 0 or not dc:
                            hong.append((run, sh, k, rc, dc))
    kq = {"dau_vao": n, "nhan": nhan, "lech_tham_chieu": len(lech), "nhan_ma_nuot_loi": len(hong)}
    print(json.dumps(kq, ensure_ascii=False))
    return kq, lech, hong


if __name__ == "__main__":
    kq, lech, hong = main()
    json.dump({"kq": kq, "nhan_ma_nuot_loi": hong[:50]}, open(os.path.join(D, "sinh_r8.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if lech or hong else 0)
