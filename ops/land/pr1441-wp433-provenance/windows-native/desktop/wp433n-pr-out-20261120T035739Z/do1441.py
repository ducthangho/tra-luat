"""Do native #433 N (PR #1441) tren Desktop: D1 D2 D3 D4 bang rig wp433n_rig.py. Chi ghi trong thu muc phien."""
import base64, datetime, gzip, hashlib, os, platform, subprocess, sys
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1])
HEAD, HTREE = "143115a2b43a42f483db8cb0b3aa0a75b68e1d94", "3b200640563c8673fa7faebdc49a41b3028061ee"
BASE = "dd1985be73d3cf65f3580f7049039ae3dab50d3d"
RIG_SHA = "f5bbdb4d141ea917297da2b232447c515776f654cd18372dfb30f2fd86bf39a1"
SRC = W / "wp1342-src"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433n-pr-out-{TS}"; OUT.mkdir()
H = W / f"c441-{TS}"
TMP = W / f"tmp441-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
def git(c, *a):
    p = subprocess.run(["git", "-C", str(c), *a], capture_output=True, text=True, encoding="utf-8", errors="replace"); return p.returncode, p.stdout.strip(), p.stderr.strip()
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
BD = now()
KHOA.write_text("\t".join([SID, BD, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #433 N PR #1441", BD]), encoding="utf-8")
try:
    import ctypes
    ghi(f"bat_dau={BD} python={sys.version.split()[0]} platform={platform.platform()} admin={ctypes.windll.shell32.IsUserAnAdmin()} TEMP={TMP}")
    for spec in ("+refs/heads/agent/wp433-r6-g1-claude:refs/remotes/origin/agent/wp433-r6-g1-claude", "+refs/heads/master:refs/remotes/origin/master"):
        rc, _, e = git(SRC, "fetch", "-q", "origin", spec); ghi(f"fetch {spec.split(':')[0]} rc={rc} {e[:200]}")
    ghi(f"base co mat trong SRC: rc={git(SRC, 'cat-file', '-e', BASE + '^{commit}')[0]}")
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(H)); assert rc == 0, e
    rc, _, e = git(H, "checkout", "-q", "--detach", HEAD); assert rc == 0, e
    git(H, "config", "core.abbrev", "7")
    h, t, s = git(H, "rev-parse", "HEAD")[1], git(H, "rev-parse", "HEAD^{tree}")[1], git(H, "status", "--porcelain")[1]
    ghi(f"CHOT HEAD sha={h} tree={t} sach=[{s}] git_la_thu_muc={(H / '.git').is_dir()} base_trong_H={git(H, 'cat-file', '-e', BASE + '^{commit}')[0]}")
    assert h == HEAD and t == HTREE and not s
    b = gzip.decompress(base64.b64decode(open(W / "rig441.b64").read().strip()))
    ghi(f"sha256 rig {hashlib.sha256(b).hexdigest()} ({len(b)} byte)"); assert hashlib.sha256(b).hexdigest() == RIG_SHA
    RIG = W / "wp433n_rig.py"; RIG.write_bytes(b)
    def chay(ten, *args):
        t0 = now()
        p = subprocess.run([sys.executable, "-B", str(RIG), *args], cwd=str(H), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
        (OUT / f"{ten}.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / f"{ten}.stderr.txt").write_text(p.stderr, encoding="utf-8")
        kl = [l for l in p.stdout.splitlines() if l.startswith("KET LUAN")]
        ghi(f"{ten} rc={p.returncode} [{t0}->{now()}] {kl[-1] if kl else '(khong co KET LUAN) ' + p.stderr.strip()[-300:]}")
    for d in ("D1", "D2", "D3", "D4"):
        chay(d, d)
    ghi(f"sach_sau H=[{git(H, 'status', '--porcelain', '--ignored')[1]}]")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
