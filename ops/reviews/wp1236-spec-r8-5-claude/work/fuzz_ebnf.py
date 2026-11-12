"""Reviewer Claude vòng 5 — tính ĐÚNG của grammar K7-S trong môi trường SẠCH, độc lập với kho sinh của phiên soạn: sinh NGẪU NHIÊN
(hạt cố định) thân THUỘC grammar từ chính EBNF (P, W rút từ đủ bảng ký tự, kể cả `= : - . / _`), kiểm gram.cu_phap_run nhận, rồi chạy
Bash/dash THẬT (env chỉ PATH/HOME, stdin /dev/null) đúng ba dòng lệnh GitHub; với mỗi thành phần k: k hỏng (ghi DA_CHAY, thoát 1), còn lại
chép stdin. Đòi rc != 0 và DA_CHAY ở MỌI lượt. pwsh: giả chặt (như sinh_r8). Chạy: python3 -I fuzz_ebnf.py [N]"""
import json, os, pathlib, random, re, subprocess, sys, tempfile
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, "soan"))
import gram
rd = random.Random(20261107)
PD, PT = "ABCZabcz0189_.", "ABCZabcz0189_./-"
WT = "ABCZabcz0189_./=:-"
def P():
    s = rd.choice(PD) + "".join(rd.choice(PT) for _ in range(rd.randint(0, 8)))
    return s
def W():
    return "".join(rd.choice(WT) for _ in range(rd.randint(1, 6)))
def LENH(i):
    ng = rd.choice(["python", "bash", "pwsh"])
    p = f"k{i}/" + P()   # tiền tố riêng để mỗi thành phần có đường dẫn riêng
    d = {"python": f"python {p}.py", "bash": f"bash {p}.sh", "pwsh": f"pwsh -NoProfile -File {p}.ps1"}[ng]
    return d + "".join(" " + W() for _ in range(rd.randint(0, 3)))
SHELL_LENH = {None: ["/usr/bin/bash", "-e"], "bash": ["/usr/bin/bash", "--noprofile", "--norc", "-eo", "pipefail"], "sh": ["/bin/sh", "-e"]}
HONG = "import pathlib, sys; pathlib.Path('DA_CHAY').touch(); sys.exit(1)\n"
QUA = "import sys; sys.stdout.write(sys.stdin.read())\n"
def chay(run, sh, hong):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d); (p / "bin").mkdir(); os.symlink(sys.executable, p / "bin/python")
        (p / "bin/pwsh").write_text(f"#!/bin/sh\n[ \"$1\" = -NoProfile ] && [ \"$2\" = -File ] && [ -n \"$3\" ] || exit 99\nshift 2; exec {sys.executable} \"$@\"\n")
        (p / "bin/pwsh").chmod(0o755)
        for t in re.findall(r"k\d+/[^ ]+\.(?:py|sh|ps1)", run):
            f = p / t; f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(("touch DA_CHAY; exit 1\n" if t == hong else "cat\n") if t.endswith(".sh") else (HONG if t == hong else QUA))
        (p / "s.sh").write_bytes(run.encode())
        rc = subprocess.run(SHELL_LENH[sh] + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d},
                            capture_output=True, stdin=subprocess.DEVNULL, timeout=20).returncode
        return rc, (p / "DA_CHAY").exists()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
xau, luot, khong_nhan = [], 0, 0
for i in range(N):
    ong = rd.random() < 0.4
    tp = [LENH(j) for j in range(rd.randint(2, 4) if ong else 1)]
    than = " | ".join(tp) + rd.choice(["", "\n"])
    for sh in (["bash"] if ong else [None, "bash", "sh"]):
        if gram.cu_phap_run(than, sh) is not None:
            khong_nhan += 1; continue
        for t in re.findall(r"k\d+/[^ ]+\.(?:py|sh|ps1)", than):
            luot += 1
            rc, da = chay(than, sh, t)
            if not (rc != 0 and da):
                xau.append((than, sh, t, rc, da))
kq = {"than": N, "luot": luot, "khong_nhan": khong_nhan, "xau": len(xau), "vi_du": xau[:5]}
print(json.dumps(kq, ensure_ascii=False))
json.dump(kq, open(os.path.join(D, "fuzz_ebnf.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if xau or khong_nhan else 0)
