"""Do native #433 R (PR #1431) tren Desktop: D1 D2 D4 D5 D5-hang D5-u1 D3-truoc + D3-don (khong mountvol). Chi ghi trong thu muc phien."""
import base64, datetime, gzip, hashlib, os, platform, re, subprocess, sys
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1])
HEAD, HTREE = "e5e118483792981addb30006c900b10fd2e3b72f", "4d710fbb62be7b82c4b3f4308ed2a4ada6d952b0"
RIG_SHA = "4ada07de1abe7ff17b14df6751fef9fff1490c0fa44abd5f935e32fa83c9b894"
SRC = W / "wp1342-src"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433r-out-{TS}"; OUT.mkdir()
H = W / f"c433r-{TS}"
TMP = W / f"tmp433r-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
def git(c, *a):
    p = subprocess.run(["git", "-C", str(c), *a], capture_output=True, text=True, encoding="utf-8", errors="replace"); return p.returncode, p.stdout.strip(), p.stderr.strip()
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
BD = now()
KHOA.write_text("\t".join([SID, BD, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #433 R PR #1431", BD]), encoding="utf-8")
try:
    import ctypes
    ghi(f"bat_dau={BD} python={sys.version.split()[0]} platform={platform.platform()} admin={ctypes.windll.shell32.IsUserAnAdmin()} TEMP={TMP}")
    rc, _, e = git(SRC, "fetch", "-q", "origin", "+refs/heads/agent/wp433-r5-g1-claude:refs/remotes/origin/agent/wp433-r5-g1-claude"); ghi(f"fetch rc={rc} {e[:200]}")
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(H)); assert rc == 0, e
    rc, _, e = git(H, "checkout", "-q", "--detach", HEAD); assert rc == 0, e
    h, t, s = git(H, "rev-parse", "HEAD")[1], git(H, "rev-parse", "HEAD^{tree}")[1], git(H, "status", "--porcelain")[1]
    ghi(f"CHOT HEAD sha={h} tree={t} sach=[{s}] git_la_thu_muc={(H / '.git').is_dir()}")
    assert h == HEAD and t == HTREE and not s
    b = gzip.decompress(base64.b64decode(open(W / "rig433r.b64").read().strip()))
    ghi(f"sha256 rig {hashlib.sha256(b).hexdigest()}"); assert hashlib.sha256(b).hexdigest() == RIG_SHA
    RIG = TMP / "wp433r_rig.py"; RIG.write_bytes(b)
    def chay(ten, *args):
        t0 = now()
        p = subprocess.run([sys.executable, "-B", str(RIG), *args], cwd=str(H), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
        (OUT / f"{ten}.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / f"{ten}.stderr.txt").write_text(p.stderr, encoding="utf-8")
        kl = [l for l in p.stdout.splitlines() if l.startswith("KET LUAN")]
        ghi(f"{ten} rc={p.returncode} [{t0}->{now()}] {kl[-1] if kl else '(khong co KET LUAN) ' + p.stderr.strip()[-300:]}")
        return p
    for d in ("D1", "D2", "D4", "D5", "D5-hang", "D5-u1"):
        chay(d, d)
    p = chay("D3-truoc", "D3-truoc")
    m = re.findall(r"wp433r-[^\s'\"]*", p.stdout)
    Tdir = next((str(Path(x)) for x in re.findall(r"[A-Za-z]:\\[^\s'\"]*wp433r-[^\s'\"\\]*", p.stdout)), None)
    ghi(f"D3 T={Tdir!r} (khong gan mountvol: phan [ADMIN] tuy chon, bo qua)")
    if Tdir: chay("D3-don", "D3-don", Tdir)
    ghi(f"sach_sau H=[{git(H, 'status', '--porcelain', '--ignored')[1]}]")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
