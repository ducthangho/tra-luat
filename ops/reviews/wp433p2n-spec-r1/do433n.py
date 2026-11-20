"""Probe native no wp433-pk1-n84-windows tren Desktop: master 8a72d28, fragment packet 1 ba bien the. Chi ghi trong thu muc phien."""
import datetime, hashlib, os, platform, subprocess, sys
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1]); PROBE_SHA = sys.argv[2]
HEAD = "8a72d28d7a413047733277545fc8547f32010593"
SRC = W / "wp1342-src"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433n-out-{TS}"; OUT.mkdir()
H = W / f"c433n-{TS}"
TMP = W / f"tmp433n-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
def git(c, *a):
    p = subprocess.run(["git", "-C", str(c), *a], capture_output=True, text=True, encoding="utf-8", errors="replace"); return p.returncode, p.stdout.strip(), p.stderr.strip()
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
BD = now()
KHOA.write_text("\t".join([SID, BD, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "probe no #433 pk1-n84-windows", BD]), encoding="utf-8")
try:
    ghi(f"bat_dau={BD} python={sys.version.split()[0]} platform={platform.platform()} TEMP={TMP}")
    rc, _, e = git(SRC, "fetch", "-q", "origin", "+refs/heads/master:refs/remotes/origin/master"); ghi(f"fetch rc={rc} {e[:200]}")
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(H)); assert rc == 0, e
    rc, _, e = git(H, "checkout", "-q", "--detach", HEAD); assert rc == 0, e
    h, t, s = git(H, "rev-parse", "HEAD")[1], git(H, "rev-parse", "HEAD^{tree}")[1], git(H, "status", "--porcelain")[1]
    ghi(f"CHOT HEAD sha={h} tree={t} sach=[{s}]"); assert h == HEAD and not s
    pb = (W / "probe433n.py").read_bytes(); ghi(f"sha256 probe {hashlib.sha256(pb).hexdigest()}"); assert hashlib.sha256(pb).hexdigest() == PROBE_SHA
    for ten in ("goc", "log", "chuan"):
        t0 = now()
        p = subprocess.run([sys.executable, "-X", "utf8", "-B", str(W / "probe433n.py"), ten], cwd=str(H), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
        (OUT / f"{ten}.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / f"{ten}.stderr.txt").write_text(p.stderr, encoding="utf-8")
        kl = [l for l in p.stdout.splitlines() if l.startswith("=== BIEN")]
        ghi(f"{ten} rc={p.returncode} [{t0}->{now()}] {kl[-1] if kl else '(khong co KET QUA) ' + p.stderr.strip()[-300:]}")
    ghi(f"sach_sau H=[{git(H, 'status', '--porcelain', '--ignored')[1]}]")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
