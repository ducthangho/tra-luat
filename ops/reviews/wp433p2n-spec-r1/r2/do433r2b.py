"""Chan doan + nguyen mau r2 cho hoi quy C1 (PR #1441) tren Windows. argv: W HEAD_DIR BASE_DIR. Giu KHOA, clone moi, moi bien the mot tien trinh."""
import datetime, hashlib, os, subprocess, sys, zipfile
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W, HD, BD0 = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433n-r2-out-{TS}"; OUT.mkdir(); TMP = W / f"t433r2-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
GOI = W / "r2"   # c1_goc.py c1_moi.py c1_chan.py chay_c1.py

import hashlib as _h
A = '    r.xs("W4.loai_o_loi", hop_dong=kq == 1 and err == [_W4 + "ghi lỗi: OSError"] and "✓ gws cred" not in out and r.tu_choi())'
BM = '    r.xs("W4.loai_o_loi", hop_dong=kq == 1 and err == [_W4 + "ghi lỗi: OSError"] * 2 and "✓ gws cred" not in out and r.tu_choi(),\n         w6=" ✓ config " not in out and not os.path.lexists(os.path.expanduser("~/.tra_luat_config.json")))  # WP433 N: W6 cũng từ chối'
PC = '    print("CHAN_DOAN W4.loai_o_loi kq=%r err=%r out=%r cfg=%r" % (kq, err, out, os.path.lexists(os.path.expanduser("~/.tra_luat_config.json"))), file=sys.__stderr__, flush=True)\n'
SHA = {"goc": 'b1f64a8b7e2828aed4f73f25704c652a61522b99f1c6afb2ceebb2258c0995ef', "moi": '0ad98b5b944ade4378940b848a3f4b2f0f8d9cc102f9df4eee6804a87e4e4aae', "chan": 'f9644224898a57753b08b3e34daa153f0e8fe53eab0729a02656adaf9afd9acd'}
CHAY_C1 = '"""Chay fragment C1 (wp433_gws_cred_win_duong) voi bien the duoc chon tren cay chon, moi lan mot tien trinh. argv: cay bien_the(goc|moi|chan) nhan"""\nimport importlib.util, shutil, sys, os, hashlib\nRIG, CAY, BT, NHAN = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]\nsp = importlib.util.spec_from_file_location("rig", RIG); rig = importlib.util.module_from_spec(sp); sp.loader.exec_module(rig)\ndich = os.path.join(CAY, "scripts", "test_fragments", "wp433_gws_cred_win_duong.py")\nnguon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c1_%s.py" % BT)\nshutil.copyfile(nguon, dich)\nprint("=== %s cay=%s bien_the=%s sha=%s" % (NHAN, CAY, BT, hashlib.sha256(open(dich, "rb").read()).hexdigest()[:16]))\nkq, ra = rig.chay_fr(CAY, "wp433_gws_cred_win_duong")\nprint("run=%r" % (kq,)); print(ra)\n'
def dung_goi(head_dir):
    GOI.mkdir(exist_ok=True)
    (GOI / "chay_c1.py").write_text(CHAY_C1, encoding="utf-8")
    g = (head_dir / "scripts" / "test_fragments" / "wp433_gws_cred_win_duong.py").read_bytes().decode("utf-8")
    for ten, s in (("goc", g), ("moi", g.replace(A, BM)), ("chan", g.replace(A, PC + BM))):
        b = s.encode("utf-8"); assert _h.sha256(b).hexdigest() == SHA[ten], ten
        (GOI / ("c1_%s.py" % ten)).write_bytes(b)
os.environ.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
B0 = now()
KHOA.write_text("\t".join([SID, B0, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #433 N r2 chan doan C1", B0]), encoding="utf-8")
try:
    dung_goi(HD)
    for f in sorted(GOI.iterdir()): ghi(f"goi {f.name} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}")
    cay = {}
    for ten, nguon, sha in (("head", HD, "143115a2b43a42f483db8cb0b3aa0a75b68e1d94"), ("base", BD0, "dd1985be73d3cf65f3580f7049039ae3dab50d3d")):
        d = W / f"r2{ten}-{TS}"
        for a in (["clone", "-q", "--no-checkout", str(nguon), str(d)], ["-C", str(d), "checkout", "-q", "--detach", sha]):
            r = subprocess.run(["git", "-c", "core.longpaths=true", *a], capture_output=True, text=True); ghi(f"{ten} git rc={r.returncode} {r.stderr.strip()[-200:]}")
        hh = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD", "HEAD^{tree}"], capture_output=True, text=True).stdout.split()
        ghi(f"{ten} checkout={hh} dir={d}"); assert hh[0] == sha; cay[ten] = d
    for ve, bt, lan in (("head", "goc", 1), ("head", "chan", 1), ("head", "moi", 1), ("head", "moi", 2), ("base", "goc", 1), ("base", "moi", 1), ("base", "chan", 1)):
        t0 = now()
        p = subprocess.run([sys.executable, "-B", str(GOI / "chay_c1.py"), str(W / "wp433n_rig.py"), str(cay[ve]), bt, f"{ve}-{bt}-lan{lan}"], capture_output=True, text=True, encoding="utf-8", errors="backslashreplace")
        (OUT / f"{ve}-{bt}-lan{lan}.txt").write_text(f"[{t0}->{now()}] rc={p.returncode}\n{p.stdout}\n--stderr--\n{p.stderr}", encoding="utf-8")
        run = [l for l in p.stdout.splitlines() if l.startswith("run=")]
        dem = [l for l in p.stdout.splitlines() if "wp433_gws_cred_win_duong] CA" in l]
        ghi(f"{ve} {bt} lan{lan} {run} {dem[-1] if dem else ''}")
        st = subprocess.run(["git", "-C", str(cay[ve]), "checkout", "-q", "--", "scripts/test_fragments/wp433_gws_cred_win_duong.py"], capture_output=True, text=True)
        ghi(f"  khoi phuc rc={st.returncode}")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
    with zipfile.ZipFile(W / f"wp433n-r2-out-{TS}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.iterdir()): z.write(f, f"wp433n-r2-out-{TS}/{f.name}")
