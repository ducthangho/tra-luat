"""Do native Windows cho PR #1420 (#1342 r5, r1d-a1-ii). Chi ghi trong thu muc phien."""
import datetime, hashlib, os, platform, subprocess, sys, time
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1])
HEAD = "2de12d38cda7d4bfe1f6f8c970e7ccd77e44a4de"
HTREE = "0bab340e0fe6661a12e47a1757fe715acb06679d"
BASE = "4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd"
SRC = W / "wp1342-src"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp1342r5-out-{TS}"; OUT.mkdir()
H = W / f"r1342h-{TS}"; B = W / f"r1342b-{TS}"
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
TMP = W / "tmp1342r5"; TMP.mkdir(exist_ok=True)
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP)); ENV.pop("PYTHONUTF8", None)
BD = now()
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
def khoa(v):
    n = datetime.datetime.now(datetime.UTC)
    KHOA.write_text("\t".join([SID, BD, (n + datetime.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #1342 r5 PR #1420: " + v, now()]), encoding="utf-8")
def git(c, *a):
    p = subprocess.run(["git", "-C", str(c), *a], capture_output=True, text=True, encoding="utf-8", errors="replace"); return p.returncode, p.stdout.strip(), p.stderr.strip()
def dung(cay, sha, ten):
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(cay))
    if rc: raise RuntimeError(f"clone {ten}: {e}")
    git(cay, "remote", "set-url", "origin", "https://github.com/ducthangho/tra-luat.git"); git(cay, "config", "core.abbrev", "7")
    rc, _, e = git(cay, "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", sha)
    if rc: raise RuntimeError(f"checkout {ten}: {e}")
    h = git(cay, "rev-parse", "HEAD")[1]; t = git(cay, "rev-parse", "HEAD^{tree}")[1]; s = git(cay, "status", "--porcelain")[1]
    ghi(f"CHOT {ten} sha={h} tree={t} sach=[{s}]")
    if h != sha or s: raise RuntimeError(f"{ten} khong khop")
    return t
def chay(nhan, args, cwd=None, timeout=7200):
    khoa(nhan); a = now(); t0 = time.monotonic()
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, timeout=timeout)
    (OUT / f"{nhan}.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / f"{nhan}.stderr.txt").write_text(p.stderr, encoding="utf-8")
    ghi(f"{nhan} rc={p.returncode} {round(time.monotonic()-t0,1)}s [{a}->{now()}]")
    return p
try:
    khoa("chuan bi")
    import ctypes
    ghi(f"bat_dau={BD} python={sys.version.split()[0]} platform={platform.platform()} admin={ctypes.windll.shell32.IsUserAnAdmin()}")
    for ref in ("agent/wp1342-r5-g1-claude", "master"):
        rc, _, e = git(SRC, "fetch", "-q", "origin", f"+refs/heads/{ref}:refs/remotes/origin/{ref}"); ghi(f"fetch {ref} rc={rc} {e[:200]}")
    if dung(H, HEAD, "HEAD") != HTREE: raise RuntimeError("tree head lech")
    dung(B, BASE, "BASE")
    DR = W / "do_r4.py"; DB = W / "dot_bien_r5.py"
    for f in (DR, DB): ghi(f"sha256 {f.name} {hashlib.sha256(f.read_bytes()).hexdigest()}")
    chay("BASE", [str(DR), str(B), "BASE", str(OUT), "tap"])
    chay("HEAD", [str(DR), str(H), "HEAD", str(OUT), "tap"])
    for n, c in (("LAP-J4", "wp1342_native_job_breakaway_tuong_minh"), ("LAP-J5", "wp1342_native_job_breakaway_ngam"), ("LAP-J12", "wp1342_native_job_long")):
        chay(n, [str(DR), str(H), n, str(OUT), "lap", c, "3"])
    p = chay("DB-KIEM-NEO", [str(DB), str(H / ".claude" / "dev"), "--kiem-neo"]); [ghi("  " + l) for l in p.stdout.splitlines()[-12:]]
    p = chay("DB", [str(DB), str(H / ".claude" / "dev")]); [ghi("  " + l) for l in p.stdout.splitlines()[-25:]]
    ghi(f"sach_sau H=[{git(H,'status','--porcelain')[1]}] B=[{git(B,'status','--porcelain')[1]}]")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
