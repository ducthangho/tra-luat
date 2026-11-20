"""Chan doan no wp433-p2b-w6-windows tren Desktop: fragment P2b goc (master) vs nguyen mau (so duong sau normcase/normpath). Chi ghi trong thu muc phien."""
import base64, datetime, gzip, hashlib, os, platform, subprocess, sys
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1]); MASTER = sys.argv[2]
SRC = W / "wp1342-src"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433p-out-{TS}"; OUT.mkdir()
H = W / f"cp-{TS[9:15]}"
TMP = W / f"tp-{TS[9:15]}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
def git(c, *a):
    p = subprocess.run(["git", "-c", "core.longpaths=true", "-C", str(c), *a], capture_output=True, text=True, encoding="utf-8", errors="replace"); return p.returncode, p.stdout.strip(), p.stderr.strip()
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
BD = now()
KHOA.write_text("\t".join([SID, BD, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "chan doan no wp433-p2b-w6-windows", BD]), encoding="utf-8")
try:
    import ctypes
    ghi(f"bat_dau={BD} python={sys.version.split()[0]} platform={platform.platform()} admin={ctypes.windll.shell32.IsUserAnAdmin()} TEMP={TMP}")
    rc, _, e = git(SRC, "fetch", "-q", "origin", "+refs/heads/master:refs/remotes/origin/master"); ghi(f"fetch master rc={rc} {e[:200]}")
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(H)); assert rc == 0, e
    git(H, "config", "core.longpaths", "true")
    rc, _, e = git(H, "checkout", "-q", "--detach", MASTER); assert rc == 0, e
    h, t, s = git(H, "rev-parse", "HEAD")[1], git(H, "rev-parse", "HEAD^{tree}")[1], git(H, "status", "--porcelain")[1]
    ghi(f"CHOT master sha={h} tree={t} sach=[{s}]"); assert h == MASTER and not s
    for ten in ("moi.py", "chay_p2b.py"):
        b = gzip.decompress(base64.b64decode(open(W / (ten + ".b64")).read().strip())); (W / ("p2bw_" + ten)).write_bytes(b)
        ghi(f"sha256 {ten} {hashlib.sha256(b).hexdigest()}")
    goc = H / "scripts" / "test_fragments" / "wp433_gws_cred_dich_ngoai_kho_b.py"
    ghi(f"sha256 goc_trong_cay {hashlib.sha256(goc.read_bytes()).hexdigest()}")
    # Chan doan hinh dang duong: expanduser giu '/' tren nt
    hd = TMP / "hd"; hd.mkdir()
    e2 = dict(ENV, HOME=str(hd), USERPROFILE=str(hd))
    code = ("import os;c=os.path.expanduser('~/.tra_luat_config.json');j=os.path.join(os.path.expanduser('~'),'.tra_luat_config.json');"
            "n=lambda p: os.path.normcase(os.path.normpath(p));print('expanduser=',repr(c));print('join=',repr(j));print('bang_chuoi=',c==j);print('bang_sau_chuan_hoa=',n(c)==n(j))")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8", errors="replace", env=e2)
    (OUT / "hinh-dang-duong.txt").write_text(p.stdout + p.stderr, encoding="utf-8"); ghi("hinh_dang_duong: " + p.stdout.replace("\n", " | ").strip())
    def chay(ten, frag):
        t0 = now()
        p = subprocess.run([sys.executable, "-B", str(W / "p2bw_chay_p2b.py"), str(H), str(frag)], cwd=str(H), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
        (OUT / f"{ten}.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / f"{ten}.stderr.txt").write_text(p.stderr, encoding="utf-8")
        tom = [l for l in p.stderr.splitlines() if "CA: dự_kiến" in l or "ĐỘT BIẾN" in l or "VẾ SAI" in l]
        ghi(f"{ten} rc={p.returncode} [{t0}->{now()}] " + " || ".join(tom) + " || " + p.stdout.strip()[-40:])
    chay("goc-lan1", goc); chay("moi-lan1", W / "p2bw_moi.py"); chay("moi-lan2", W / "p2bw_moi.py"); chay("goc-lan2", goc)
    ghi(f"sach_sau H=[{git(H, 'status', '--porcelain', '--ignored')[1]}]")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
