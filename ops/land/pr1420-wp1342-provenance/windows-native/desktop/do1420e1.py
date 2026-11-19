"""Chay lai rieng e1 (2 lan) bang dot_bien_r5b.py tren cay HEAD da chot cua lan do 20261119T120908Z."""
import datetime, hashlib, os, subprocess, sys
from pathlib import Path
W = Path(sys.argv[1]); SID = "session_015GtxrZk6gmfQKo7g4BfMBS"
H = W / "r1342h-20261119T120908Z"; OUT = W / "wp1342r5-out-20261119T120908Z"; TT = OUT / "E1-LAI.txt"
KHOA = Path(r"F:\tl-win\KHOA.txt"); TMP = W / "tmp1342r5"
now = lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMP=str(TMP), TEMP=str(TMP), TMPDIR=str(TMP)); ENV.pop("PYTHONUTF8", None)
def ghi(s):
    with open(TT, "a", encoding="utf-8") as f: f.write(s + "\n")
if KHOA.read_text(encoding="utf-8-sig").strip(): print("KHOA BAN"); sys.exit(3)
KHOA.write_text("\t".join([SID, now(), (datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "native #1342 r5 PR #1420: e1 lai", now()]), encoding="utf-8")
try:
    DB = W / "dot_bien_r5b.py"
    ghi(f"bat_dau={now()} sha256 dot_bien_r5b.py {hashlib.sha256(DB.read_bytes()).hexdigest()}")
    hs = subprocess.run(["git", "-C", str(H), "rev-parse", "HEAD", "HEAD^{tree}"], capture_output=True, text=True).stdout.split()
    st = subprocess.run(["git", "-C", str(H), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    ghi(f"CHOT HEAD {hs} sach=[{st}]")
    for lan in (1, 2):
        t0 = now()
        p = subprocess.run([sys.executable, "-X", "utf8", "-B", str(DB), str(H / ".claude" / "dev"), "e1"], capture_output=True, text=True,
                           encoding="utf-8", errors="backslashreplace", env=ENV)
        ghi(f"E1 lan={lan} rc={p.returncode} [{t0}->{now()}]")
        for l in p.stdout.splitlines(): ghi("  " + l)
        if p.stderr.strip(): ghi("  STDERR: " + p.stderr.strip()[-800:])
except Exception as e:
    ghi(f"LOI: {type(e).__name__}: {e}")
finally:
    ghi(f"ket_thuc={now()}"); KHOA.write_text("", encoding="utf-8"); ghi("XONG (khoa da nha)")
