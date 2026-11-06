"""Tính ĐÚNG của K7-S trong môi trường sạch: mọi thân grammar NHẬN, với mỗi thành phần k hỏng (ghi DA_CHAY, thoát 1), chạy đúng ba mẫu
GitHub ⇒ DA_CHAY có VÀ rc != 0. `bash P.sh` dùng /usr/bin/bash THẬT trên một script sh thật; `pwsh` GIẢ CHẶT (chỉ nhận đúng
`-NoProfile -File <tệp>`, lệch thì exit 99) vì container không có pwsh. Không dùng phép đổi tên tệp."""
import os, sys, json, itertools, subprocess, tempfile, pathlib
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "soan"); sys.path.insert(0, S)
import gram
SH = {None: ["/usr/bin/bash", "-e"], "bash": ["/usr/bin/bash", "--noprofile", "--norc", "-eo", "pipefail"], "sh": ["/bin/sh", "-e"]}
PS = ["ops/x", "a", ".", "..", "./b", "a-b/c_d", "x.py", "o.p/q-"]
WS = ["-c", "-e", "-s", "-n", "-h", "-i", "-m", "-x", "-o", "pipefail", "--", "-", "=", ":", ".", "..", "+e".replace("+", "-"), "exit", "true",
      "if", "then", "done", "time", "a=b", "--json", "-Command", "-File", "-NoProfile", "y.py", "z.sh", "-c=1", "::", "-.-"]
def lenh(dang, p, ws):
    pre = {"python": f"python {p}.py", "bash": f"bash {p}.sh", "pwsh": f"pwsh -NoProfile -File {p}.ps1"}[dang]
    return " ".join([pre] + list(ws)), {"python": f"{p}.py", "bash": f"{p}.sh", "pwsh": f"{p}.ps1"}[dang]
def tep(p, dang, hong):
    if dang == "bash": return ("touch \"$OLDPWD_DA\"/DA_CHAY_$$; touch DA_CHAY\nexit 1\n" if hong else "cat\n")
    return ("import pathlib, sys; pathlib.Path('DA_CHAY').touch(); sys.exit(1)\n" if hong else "import sys; sys.stdout.write(sys.stdin.read())\n")
PWSH = "#!/bin/sh\n[ \"$1\" = -NoProfile ] && [ \"$2\" = -File ] || exit 99\nshift 2\nexec {py} \"$@\"\n"
def chay(run, sh, comps, k):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d); (p / "bin").mkdir()
        os.symlink(sys.executable, p / "bin/python")
        (p / "bin/pwsh").write_text(PWSH.format(py=sys.executable)); (p / "bin/pwsh").chmod(0o755)
        os.symlink("/usr/bin/bash", p / "bin/bash")
        for i, (dang, f) in enumerate(comps):
            q = p / f; q.parent.mkdir(parents=True, exist_ok=True)
            if q.exists() and i != k: continue
            q.write_text(tep(f, dang, i == k).replace("touch \"$OLDPWD_DA\"/DA_CHAY_$$; ", ""))
        (p / "s.sh").write_text(run)
        r = subprocess.run(SH[sh] + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d}, capture_output=True, stdin=subprocess.DEVNULL, timeout=20)
        return r.returncode, (p / "DA_CHAY").exists()
than = []
for dang in ("python", "bash", "pwsh"):
    for pp in PS:
        for n in (0, 1, 2):
            for ws in (itertools.product(WS, repeat=n) if n < 2 else [(a, b) for a in WS[:12] for b in WS[-12:]]):
                L, f = lenh(dang, pp, ws); than.append((L, [(dang, f)]))
DON = list(than)
ong = []
mau = [lenh("python", "ops/a", ()), lenh("bash", "ops/b", ("-c",)), lenh("pwsh", "ops/c", ("-e", "x")), lenh("python", "ops/d", ("--json", "a=b")), lenh("bash", "ops/e", ())]
for n in (2, 3):
    for combo in itertools.product(mau, repeat=n):
        if len({f for _, f in combo}) < n: continue
        ong.append((" | ".join(L for L, _ in combo), [({"py": "python", "sh": "bash", "ps1": "pwsh"}[f.rsplit(".", 1)[1]], f) for _, f in combo]))
tong = nhan_sai = hong = 0; vd = []
for body, comps in DON + ong:
    for sh in (None, "bash", "sh"):
        for lf in ("", "\n"):
            run = body + lf
            if gram.cu_phap_run(run, sh) is not None:
                if body in [b for b, _ in DON]: nhan_sai += 1; vd.append(("DON_bi_tu_choi", run, sh))
                continue
            for k in range(len(comps)):
                tong += 1
                rc, dc = chay(run, sh, comps, k)
                if rc == 0 or not dc: hong += 1; vd.append((run, sh, k, rc, dc))
kq = {"than_don": len(DON), "than_ong": len(ong), "luot_chay": tong, "don_bi_tu_choi_sai": nhan_sai, "nhan_ma_khong_truyen_loi": hong, "vd": vd[:10]}
json.dump(kq, open("grammar_sach_v3.json", "w"), ensure_ascii=False, indent=1); print({k: v for k, v in kq.items() if k != "vd"}, vd[:5])
