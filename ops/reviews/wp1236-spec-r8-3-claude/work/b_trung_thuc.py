"""Vế (b) của A14-S6 chạy TRUNG THỰC: tệp chương trình dựng ĐÚNG đường dẫn chữ (word 2 của thân), KHÔNG đổi tên như sinh_r8.py.
So số thân được nhận mà (b) đỏ (DA_CHAY vắng hoặc rc 0) giữa hai cách, cho 26 đột biến m-S15[c]."""
import os, sys, json, subprocess, tempfile, pathlib
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "soan"); sys.path.insert(0, S)
import gram, sinh_r8, dot_bien_r8
SH = {None: ["/usr/bin/bash", "-e"], "bash": ["/usr/bin/bash", "--noprofile", "--norc", "-eo", "pipefail"], "sh": ["/bin/sh", "-e"]}
def chay_that(run, sh):
    w = run.rstrip("\n").split(" ")[1]   # đường dẫn chữ, kể cả ký tự lạ
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d); (p / "bin").mkdir(); os.symlink(sys.executable, p / "bin/python")
        f = p / w; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(sinh_r8.HONG)
        (p / "s.sh").write_text(run)
        rc = subprocess.run(SH[sh] + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d}, capture_output=True, stdin=subprocess.DEVNULL, timeout=20).returncode
        return rc, (p / "DA_CHAY").exists()
kho = sinh_r8.kho(); kq = {}
for ten, f in dot_bien_r8.DB_SINH.items():
    if not ten.startswith("m-S15"): continue
    nhan = [(r, s) for t in kho for s in sinh_r8.SHELL for r in (t, t + "\n") if f(r, s) is None and gram.cu_phap_run(r, s) is not None]
    doi_ten = sum(any(rc == 0 or not dc for _, rc, dc in sinh_r8.chay_tung_thanh_phan(r, s)) for r, s in nhan)
    tt = [chay_that(r, s) for r, s in nhan]
    kq[ten] = {"than_nhan_lech": len(nhan), "b_do_doi_ten": doi_ten, "b_do_trung_thuc": sum(rc == 0 or not dc for rc, dc in tt),
               "trung_thuc_nuot_that": sum(rc == 0 and dc for rc, dc in tt), "trung_thuc_khong_chay": sum(not dc for rc, dc in tt), "vd": nhan[0][0]}
    print(ten, kq[ten])
json.dump(kq, open("b_trung_thuc.json", "w"), ensure_ascii=False, indent=1)
print("dot_bien b bat (doi ten):", sum(v["b_do_doi_ten"] > 0 for v in kq.values()), "| b bat (trung thuc):", sum(v["b_do_trung_thuc"] > 0 for v in kq.values()), "/", len(kq))
