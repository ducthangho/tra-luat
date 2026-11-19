"""Do native #433 C1 (PR #1425) tren Desktop: tat-ca + D5. Chi ghi trong thu muc phien. D10 lam rieng (can chu kho chay lenh admin)."""
import base64, datetime, gzip, hashlib, os, platform, subprocess, sys
from pathlib import Path
SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
W = Path(sys.argv[1])
HEAD, HTREE = "724a9e55727c82cc0c5ad7d3c4479cfb69be791b", "e942f6a320ed927ffcf85310e75929ac4443a4fe"
RIG_SHA = "48166acbd82b0a9243129c727d7dd8fece0b679e155506d4c6470866f7f11794"
SRC = W / "wp1342-src"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
OUT = W / f"wp433c1-out-{TS}"; OUT.mkdir()
H = W / f"c433c1-{TS}"
TMP = W / f"tmp433c1-{TS}"; TMP.mkdir()
KHOA = Path(r"F:\tl-win\KHOA.txt"); TT = OUT / "TOM-TAT.txt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP))
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
def git(c, *a):
    p = subprocess.run(["git", "-C", str(c), *a], capture_output=True, text=True, encoding="utf-8", errors="replace"); return p.returncode, p.stdout.strip(), p.stderr.strip()
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
BD = now()
KHOA.write_text("\t".join([SID, BD, (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #433 C1 PR #1425: tat-ca + D5", BD]), encoding="utf-8")
try:
    import ctypes
    ghi(f"bat_dau={BD} python={sys.version.split()[0]} platform={platform.platform()} admin={ctypes.windll.shell32.IsUserAnAdmin()} TEMP={TMP}")
    rc, _, e = git(SRC, "fetch", "-q", "origin", "+refs/heads/agent/wp433-r4-g1-claude:refs/remotes/origin/agent/wp433-r4-g1-claude"); ghi(f"fetch rc={rc} {e[:200]}")
    rc, _, e = git(SRC, "clone", "-q", "--no-checkout", str(SRC), str(H)); assert rc == 0, e
    rc, _, e = git(H, "checkout", "-q", "--detach", HEAD); assert rc == 0, e
    h, t, s = git(H, "rev-parse", "HEAD")[1], git(H, "rev-parse", "HEAD^{tree}")[1], git(H, "status", "--porcelain")[1]
    ghi(f"CHOT HEAD sha={h} tree={t} sach=[{s}] git_la_thu_muc={(H / '.git').is_dir()}")
    assert h == HEAD and t == HTREE and not s
    b = gzip.decompress(base64.b64decode(open(W / "rig433c1.b64").read().strip()))
    ghi(f"sha256 rig {hashlib.sha256(b).hexdigest()}"); assert hashlib.sha256(b).hexdigest() == RIG_SHA
    RIG = TMP / "wp433c1_rig.py"; RIG.write_bytes(b)
    def chay(ten, args):
        t0 = now()
        p = subprocess.run(args, cwd=str(H), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
        (OUT / f"{ten}.stdout.txt").write_text(p.stdout, encoding="utf-8"); (OUT / f"{ten}.stderr.txt").write_text(p.stderr, encoding="utf-8")
        ghi(f"{ten} rc={p.returncode} [{t0}->{now()}]"); return p
    p = chay("TAT-CA", [sys.executable, "-B", str(RIG), "tat-ca"])
    i = p.stdout.find("TỔNG KẾT"); [ghi("  " + l) for l in (p.stdout[i:] if i >= 0 else p.stdout[-3000:]).splitlines()[:60]]
    MA = "import importlib.util, sys; sys.path.insert(0, 'scripts'); import tl; s = importlib.util.spec_from_file_location('frag', 'F'); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); r = m.run(tl); print('run() ->', r); sys.exit(0 if r else 1)"
    for ten, f in (("D5-C1", "scripts/test_fragments/wp433_gws_cred_win_duong.py"), ("D5-P2A", "scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py"), ("D5-PK1", "scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py")):
        p = chay(ten, [sys.executable, "-B", "-c", MA.replace("'F'", repr(f))])
        [ghi("  " + l) for l in (p.stdout.strip().splitlines()[-2:] + p.stderr.strip().splitlines()[-6:])]
    ghi(f"sach_sau H=[{git(H, 'status', '--porcelain', '--ignored')[1]}]")
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
