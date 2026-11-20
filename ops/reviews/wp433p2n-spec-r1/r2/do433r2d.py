"""Lan 3 nguyen mau r2 (them tiem loi git mot lan). argv: W HEAD_DIR BASE_DIR (clone san tu do433r2b)."""
import datetime, hashlib, os, subprocess, sys, zipfile
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W, HD, BD = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433n-r2d-out-{TS}"; OUT.mkdir(); TMP = W / f"t433r2d-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"; GOI = W / "r2d"
A0 = '    with _thay(r.m, "_loai_o_nt", loi_o):\n        kq, out, err = r.w("W4.loai_o_loi", p("c2"))\n    r.xs("W4.loai_o_loi", hop_dong=kq == 1 and err == [_W4 + "ghi lỗi: OSError"] and "✓ gws cred" not in out and r.tu_choi())'
B0 = '    c6 = pathlib.Path(os.path.expanduser("~/.tra_luat_config.json")); c6_truoc = c6.read_bytes() if os.path.lexists(c6) else None  # noqa: E702\n    with _thay(r.m, "_loai_o_nt", loi_o):\n        kq, out, err = r.w("W4.loai_o_loi", p("c2"))\n    r.xs("W4.loai_o_loi", hop_dong=kq == 1 and err == [_W4 + "ghi lỗi: OSError"] * 2 and "✓ gws cred" not in out and r.tu_choi(),   # WP433 N: W6 cũng từ chối\n         w6=" ✓ config " not in out and (c6.read_bytes() if os.path.lexists(c6) else None) == c6_truoc)'
C0 = '    c6 = pathlib.Path(os.path.expanduser("~/.tra_luat_config.json")); c6_truoc = c6.read_bytes() if os.path.lexists(c6) else None  # noqa: E702\n    with _thay(r.m, "_loai_o_nt", loi_o):\n        kq, out, err = r.w("W4.loai_o_loi", p("c2"))\n    print("CHAN_DOAN W4.loai_o_loi kq=%r err=%r ok_cfg=%r cfg_bang=%r" % (kq, err, " ✓ config " in out, (c6.read_bytes() if os.path.lexists(c6) else None) == c6_truoc), file=sys.__stderr__, flush=True)\n    r.xs("W4.loai_o_loi", hop_dong=kq == 1 and err == [_W4 + "ghi lỗi: OSError"] * 2 and "✓ gws cred" not in out and r.tu_choi(),   # WP433 N: W6 cũng từ chối\n         w6=" ✓ config " not in out and (c6.read_bytes() if os.path.lexists(c6) else None) == c6_truoc)'
A1 = '    kq, _o, _e = r.w("W5.git_loi", p("pk", "gws"), lambda q: q == p("pk", ".git") and _nem(PermissionError("wp433-c1-git")))'
B1 = '    mot = []   # WP433 N: lỗi CHỈ ở lần `lstat` ĐẦU (của `_co_git_nt`) — `_trong_kho_git` (M4) cũng lan lỗi, nên ném mọi lần thì đột biến không đo được\n    kq, _o, _e = r.w("W5.git_loi", p("pk", "gws"), lambda q: q == p("pk", ".git") and not mot and (mot.append(q) or _nem(PermissionError("wp433-c1-git"))))'
SHA = {'goc': 'b1f64a8b7e2828aed4f73f25704c652a61522b99f1c6afb2ceebb2258c0995ef', 'moi3': 'fa87f58b6bb4e064684a2d61f88d96eedce7844b648ad74e145f8abe17f26e4c', 'chan3': '0fd77f1fd12b0b51870224c56aa0f314f6e119947807508e9a3db877210f1e08'}
CHAY_C1 = '"""Chay fragment C1 (wp433_gws_cred_win_duong) voi bien the duoc chon tren cay chon, moi lan mot tien trinh. argv: cay bien_the(goc|moi|chan) nhan"""\nimport importlib.util, shutil, sys, os, hashlib\nRIG, CAY, BT, NHAN = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]\nsp = importlib.util.spec_from_file_location("rig", RIG); rig = importlib.util.module_from_spec(sp); sp.loader.exec_module(rig)\ndich = os.path.join(CAY, "scripts", "test_fragments", "wp433_gws_cred_win_duong.py")\nnguon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c1_%s.py" % BT)\nshutil.copyfile(nguon, dich)\nprint("=== %s cay=%s bien_the=%s sha=%s" % (NHAN, CAY, BT, hashlib.sha256(open(dich, "rb").read()).hexdigest()[:16]))\nkq, ra = rig.chay_fr(CAY, "wp433_gws_cred_win_duong")\nprint("run=%r" % (kq,)); print(ra)\n'
os.environ.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
B = now()
KHOA.write_text("\t".join([SID, B, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #433 N r2d nguyen mau C1", B]), encoding="utf-8")
try:
    GOI.mkdir(exist_ok=True); (GOI / "chay_c1.py").write_text(CHAY_C1, encoding="utf-8")
    cay = {}
    for ten, d, sha in (("head", HD, "143115a2b43a42f483db8cb0b3aa0a75b68e1d94"), ("base", BD, "dd1985be73d3cf65f3580f7049039ae3dab50d3d")):
        hh = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD", "HEAD^{tree}"], capture_output=True, text=True).stdout.split()
        st = subprocess.run(["git", "-C", str(d), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        ghi(f"{ten} {hh} sach=[{st}] dir={d}"); assert hh[0] == sha and not st; cay[ten] = d
    g = (HD / "scripts" / "test_fragments" / "wp433_gws_cred_win_duong.py").read_bytes().decode("utf-8")
    for ten, s in (("goc", g), ("moi3", g.replace(A0, B0).replace(A1, B1)), ("chan3", g.replace(A0, C0).replace(A1, B1))):
        b = s.encode("utf-8"); assert hashlib.sha256(b).hexdigest() == SHA[ten], ten
        (GOI / ("c1_%s.py" % ten)).write_bytes(b); ghi(f"goi c1_{ten}.py sha256={hashlib.sha256(b).hexdigest()}")
    for ve, bt, lan in (("head", "chan3", 1), ("head", "moi3", 1), ("head", "moi3", 2), ("base", "moi3", 1)):
        t0 = now()
        p = subprocess.run([sys.executable, "-B", str(GOI / "chay_c1.py"), str(W / "wp433n_rig.py"), str(cay[ve]), bt, f"{ve}-{bt}-lan{lan}"], capture_output=True, text=True, encoding="utf-8", errors="backslashreplace")
        (OUT / f"{ve}-{bt}-lan{lan}.txt").write_text(f"[{t0}->{now()}] rc={p.returncode}\n{p.stdout}\n--stderr--\n{p.stderr}", encoding="utf-8")
        run = [l for l in p.stdout.splitlines() if l.startswith("run=")]
        dem = [l for l in p.stdout.splitlines() if "wp433_gws_cred_win_duong] CA" in l]
        do = [l[:200] for l in p.stdout.splitlines() if "] ĐỎ " in l or "TIN_DUNG_GIA" in l or "SONG" in l]
        cd = [l[:400] for l in p.stderr.splitlines() if l.startswith("CHAN_DOAN")][:1]
        ghi(f"{ve} {bt} lan{lan} {run} {dem[-1] if dem else ''} do={do} chan_doan={cd}")
        st = subprocess.run(["git", "-C", str(cay[ve]), "checkout", "-q", "--", "scripts/test_fragments/wp433_gws_cred_win_duong.py"], capture_output=True, text=True)
        ghi(f"  khoi phuc rc={st.returncode}")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
    with zipfile.ZipFile(W / f"wp433n-r2d-out-{TS}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.iterdir()): z.write(f, f"wp433n-r2d-out-{TS}/{f.name}")
