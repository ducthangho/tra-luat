"""Bo sung do lai re: ruff F (base vs merge, --no-cache) tren write set, adr-song, doctrine-scan, eol_policy --all tren merge.
Dung: python bo_sung_n.py <clone merge> <clone base> <tep_ra> <duong write set>..."""
import datetime, subprocess, sys
C, B, OUT, WS = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
f = open(OUT, "w", encoding="utf-8")
def chay(cmd, cwd, nhan, cat=None):
    t0 = datetime.datetime.now(datetime.timezone.utc)
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    o = p.stdout + p.stderr
    if cat:
        o = cat(o)
    f.write(f"\n## {t0:%Y-%m-%dT%H:%M:%SZ} (cwd {nhan}) $ {' '.join(cmd)}\n{o}rc={p.returncode}\n"); f.flush()
f.write(f"# bo sung do lai; python {sys.version.split()[0]}; base {subprocess.run(['git','rev-parse','HEAD'],cwd=B,capture_output=True,text=True).stdout.strip()}, merge {subprocess.run(['git','rev-parse','HEAD'],cwd=C,capture_output=True,text=True).stdout.strip()}\n")
chay([sys.executable, "-m", "ruff", "--version"], C, "clone-merge")
for d, n in ((B, "clone-base"), (C, "clone-merge")):
    chay([sys.executable, "-m", "ruff", "check", "--no-cache", "--select", "F", "--output-format", "concise", *WS], d, n)
chay([sys.executable, "-B", ".claude/dev/packet_loop.py", "adr-song", "--root", "."], C, "clone-merge")
chay([sys.executable, "-B", ".claude/dev/packet_loop.py", "doctrine-scan", "--root", "."], C, "clone-merge")
def gon(o):  # giu cac khoa tong ket cua eol_policy, bo danh sach tep
    import json
    try:
        d = json.loads(o)
    except Exception:
        return o
    return json.dumps({k: v for k, v in d.items() if not isinstance(v, list) or len(v) < 20}, ensure_ascii=False) + "\n"
chay([sys.executable, "-B", ".githooks/eol_policy.py", "--all", "--json"], C, "clone-merge", gon)
f.write("\n# HET\n")
