"""Reviewer Claude vòng 5: (1) các biến thể L* của K01 vòng 4 (sửa TRONG thân hàm, giữ hằng) nay qua kiem_s0 không; (2) phân bố 222/665;
(3) thời gian vế (a) A14-S6; (4) Bash thật trên thân mà biến thể gán-lại-tên nhận (`… || exit 0`). Chạy: python3 -I thu_k01.py"""
import json, os, pathlib, subprocess, sys, tempfile, time
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, "soan"))
import khoa_ast_r8 as K, sinh_r8 as S, gram
G, B0 = K.GOC, '    b = run[:-1] if run.endswith("\\n") else run'
L = {
 "L1_ong_match": G.replace("RE_ONG.fullmatch(b)", "RE_ONG.match(b)"),
 "L3_rstrip": G.replace(B0, '    b = run.rstrip()'),
 "L4_strip": G.replace(B0, '    b = run.strip()'),
 "L5_bo_chu_thich": G.replace(B0, B0 + '\n    b = b.split(" #")[0]'),
 "L6_removesuffix_va": G.replace("RE_DON.fullmatch(b)", 'RE_DON.fullmatch(b.removesuffix(" &"))'),
 "L7_removeprefix_phu_dinh": G.replace("RE_DON.fullmatch(b)", 'RE_DON.fullmatch(b.removeprefix("! "))'),
 "L8_splitlines": G.replace(B0, '    b = run.splitlines()[0] if run else run'),
 "L14_removesuffix_hai_cham": G.replace("RE_DON.fullmatch(b)", 'RE_DON.fullmatch(b.removesuffix(" || :"))'),
 "L15_ham_phu": G.replace("    if RE_DON.fullmatch(b):", "    if _k(b):") + "\n\ndef _k(x):\n    return RE_DON.fullmatch(x)\n",
 "L17_ong_khi_shell_khac": G.replace('return None if shell == "bash" else "ong_khong_bash_tuong_minh"', 'return None'),
}
kq = {k: K.kiem_s0(v) for k, v in L.items()}
for k, v in kq.items():
    print(f"{k:28} {v or 'DAT'}")
chen = S.chen("python ops/m.py w"); print("chen:", len(chen), "lay mau i%3==0:", sum(1 for i in range(len(chen)) if i % 3 == 0))
t = time.time(); th = S.kho(); t1 = time.time()
n = sum(1 for x in th for sh in S.SHELL for r in (x, x + "\n") if gram.cu_phap_run(r, sh) == gram.cu_phap_run(r, sh))
print(f"kho(): {t1 - t:.2f}s; ve (a) so 2 lan tham chieu tren {n} dau vao: {time.time() - t1:.2f}s")
with tempfile.TemporaryDirectory() as d:
    p = pathlib.Path(d); (p / "ops").mkdir(); (p / "bin").mkdir(); os.symlink(sys.executable, p / "bin/python")
    (p / "ops/hong_test.py").write_text("import pathlib, sys; pathlib.Path('DA_CHAY').touch(); sys.exit(1)\n")
    (p / "s.sh").write_text("python ops/hong_test.py || exit 0")
    for sh, lenh in ((None, ["/usr/bin/bash", "-e"]), ("bash", ["/usr/bin/bash", "--noprofile", "--norc", "-eo", "pipefail"]), ("sh", ["/bin/sh", "-e"])):
        r = subprocess.run(lenh + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d}, stdin=subprocess.DEVNULL, capture_output=True)
        print("bash that `python ops/hong_test.py || exit 0`", sh, "rc", r.returncode, "DA_CHAY", (p / "DA_CHAY").exists()); (p / "DA_CHAY").unlink(missing_ok=True)
json.dump(kq, open(os.path.join(D, "thu_k01.json"), "w"), ensure_ascii=False, indent=1)
