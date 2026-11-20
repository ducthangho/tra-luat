"""(1) Chay lai D2 (PR #1441) voi core.longpaths=true qua GIT_CONFIG_* (rig khong doi): lan 1 do 'Filename too long' khi clone base trong TEMP.
(2) Doi chung D4: fragment C1 (win_duong) va P2b (dich_ngoai_kho_b) tren BASE dd1985b va lap lai tren HEAD, moi lan mot tien trinh (ham chay_fr cua rig)."""
import datetime, hashlib, os, subprocess, sys
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1]); TS1 = sys.argv[2]
HEAD = "143115a2b43a42f483db8cb0b3aa0a75b68e1d94"
RIG_SHA = "f5bbdb4d141ea917297da2b232447c515776f654cd18372dfb30f2fd86bf39a1"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433n-pr-out-{TS1}"; H = W / f"c441-{TS1}"
TMP = W / f"t441b-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP),
           GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.longpaths", GIT_CONFIG_VALUE_0="true")
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
BD = now()
KHOA.write_text("\t".join([SID, BD, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #433 N PR #1441 D2 lai", BD]), encoding="utf-8")
try:
    RIG = W / "wp433n_rig.py"; h = hashlib.sha256(RIG.read_bytes()).hexdigest()
    ghi(f"D2-lai bat_dau={BD} rig={h} TEMP={TMP} env them: GIT_CONFIG core.longpaths=true (rig khong doi)"); assert h == RIG_SHA
    hh = subprocess.run(["git", "-C", str(H), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    st = subprocess.run(["git", "-C", str(H), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    ghi(f"D2-lai H={hh} sach=[{st}]"); assert hh == HEAD and not st
    t0 = now()
    p = subprocess.run([sys.executable, "-B", str(RIG), "D2"], cwd=str(H), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    (OUT / "D2-lai.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / "D2-lai.stderr.txt").write_text(p.stderr, encoding="utf-8")
    kl = [l for l in p.stdout.splitlines() if l.startswith("KET LUAN")]
    ghi(f"D2-lai rc={p.returncode} [{t0}->{now()}] {kl[-1] if kl else '(khong co KET LUAN) ' + p.stderr.strip()[-300:]}")
    import importlib.util
    sp = importlib.util.spec_from_file_location("rig441", str(RIG)); rig = importlib.util.module_from_spec(sp); sp.loader.exec_module(rig)
    B = W / f"b441-{TS}"
    for a in (["clone", "-q", "--no-checkout", str(H), str(B)], ["-C", str(B), "checkout", "-q", "--detach", "dd1985be73d3cf65f3580f7049039ae3dab50d3d"]):
        r = subprocess.run(["git", "-c", "core.longpaths=true", *a], capture_output=True, text=True, env=ENV); ghi(f"base git {a[0] if a[0] != '-C' else a[2]} rc={r.returncode} {r.stderr.strip()[-200:]}")
    bh = subprocess.run(["git", "-C", str(B), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(); ghi(f"BASE checkout={bh} dir={B}")
    os.environ.update({k: v for k, v in ENV.items() if k in ("TMP", "TEMP", "TMPDIR", "PYTHONUTF8", "PYTHONIOENCODING", "PYTHONDONTWRITEBYTECODE")})
    with open(OUT / "D4-doi-chung.txt", "w", encoding="utf-8") as f:
        for ve, cay in (("base", B), ("head", H)):
            for lan in (1, 2):
                for ten in ("wp433_gws_cred_win_duong", "wp433_gws_cred_dich_ngoai_kho_b"):
                    t0 = now(); kq, ra = rig.chay_fr(str(cay), ten)
                    f.write(f"===== {ve} lan{lan} {ten} run={kq!r} [{t0}->{now()}]\n{ra}\n"); f.flush()
                    ghi(f"D4-doi-chung {ve} lan{lan} {ten} run={kq!r}")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"D2-lai ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("D2-lai XONG (khoa da nha)")
