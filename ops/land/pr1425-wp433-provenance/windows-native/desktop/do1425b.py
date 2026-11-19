"""PK1 (fragment packet 1) tren BASE c6487ff va HEAD 724a9e5, cung dieu kien, moi ve 2 lan. Chi ghi trong thu muc phien."""
import datetime, os, subprocess, sys
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1]); SRC = W / "wp1342-src"
H = W / "c433c1-20261119T151704Z"
BASE = "c6487ff884c61085c939a75a37c657006ee690f2"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / "wp433c1-out-20261119T151704Z"; TT = OUT / "PK1-BASE-HEAD.txt"
B = W / f"c433c1base-{TS}"; TMP = W / f"tmp433c1b-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
def git(c, *a):
    p = subprocess.run(["git", "-C", str(c), *a], capture_output=True, text=True, encoding="utf-8", errors="replace"); return p.returncode, p.stdout.strip(), p.stderr.strip()
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
KHOA.write_text("\t".join([SID, now(), (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #433 C1 PR #1425: PK1 base vs head", now()]), encoding="utf-8")
try:
    ghi(f"bat_dau={now()} TEMP={TMP}")
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(B)); assert rc == 0, e
    rc, _, e = git(B, "checkout", "-q", "--detach", BASE); assert rc == 0, e
    for ten, c in (("BASE", B), ("HEAD", H)):
        ghi(f"CHOT {ten} sha={git(c, 'rev-parse', 'HEAD')[1]} tree={git(c, 'rev-parse', 'HEAD^{tree}')[1]} sach=[{git(c, 'status', '--porcelain')[1]}]")
    MA = "import importlib.util, sys; sys.path.insert(0, 'scripts'); import tl; s = importlib.util.spec_from_file_location('frag', 'scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py'); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); r = m.run(tl); print('run() ->', r); sys.exit(0 if r else 1)"
    for lan in (1, 2):
        for ten, c in (("BASE", B), ("HEAD", H)):
            t0 = now()
            p = subprocess.run([sys.executable, "-B", "-c", MA], cwd=str(c), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
            (OUT / f"PK1-{ten}-{lan}.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / f"PK1-{ten}-{lan}.stderr.txt").write_text(p.stderr, encoding="utf-8")
            ghi(f"PK1 {ten} lan={lan} rc={p.returncode} [{t0}->{now()}]")
            [ghi("  " + l) for l in (p.stdout.strip().splitlines()[-1:] + [x for x in p.stderr.splitlines() if "ĐỎ" in x or "CA:" in x])]
    ghi(f"sach_sau B=[{git(B, 'status', '--porcelain')[1]}] H=[{git(H, 'status', '--porcelain')[1]}]")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
