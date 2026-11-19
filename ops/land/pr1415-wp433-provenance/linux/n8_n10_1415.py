"""N8 + N10 cho ho so land PR #1415 (#433 P2a): dung HAI clone (base 3b64746, merge 417b593) trong CUNG mot lenh, roi chay tuan tu
`python3 -B scripts/tl.py --selftest` va `python3 -B ops/cloud_agent_creds_test.py` tren ca hai. Dung: python n8_n10_1415.py <goc kho> <thu_muc_lam> <tep_ra>"""
import datetime, os, subprocess, sys
GOC, W, OUT = sys.argv[1:4]
VE = (("base", "3b647461db7c8ded1bddd9aafc5c6aa5eead223f"), ("merge", "417b59397669e6966da2b546537279d15e2ba0c0"))
f = open(OUT, "w", encoding="utf-8")
def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def chay(cmd, cwd, nhan, giu=None):
    t0 = utc(); p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL,
                                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    o = p.stdout + p.stderr
    if giu:
        o = "\n".join(l for l in o.splitlines() if giu(l)) + "\n"
    f.write(f"\n## {t0}->{utc()} ({nhan}) $ {' '.join(cmd)}\n{o}rc={p.returncode}\n"); f.flush()
f.write(f"# {utc()} N8+N10 #1415; hai clone dung trong CUNG mot lenh nay; python {sys.version.split()[0]}\n")
cay = {}
for ten, sha in VE:   # dung ca hai ve TRUOC khi do
    d = os.path.join(W, f"n810-{ten}")
    chay(["git", "clone", "-q", "--shared", GOC, d], W, ten)
    chay(["git", "-C", d, "checkout", "-q", "--detach", sha], W, ten)
    chay(["git", "-C", d, "config", "core.abbrev", "7"], W, ten)
    chay(["git", "-C", d, "rev-parse", "HEAD"], W, ten)
    cay[ten] = d
for ten, _ in VE:
    chay([sys.executable, "-B", "scripts/tl.py", "--selftest"], cay[ten], ten, lambda l: "== tl selftest" in l or "[FAIL]" in l or "wp433_gws" in l)
for ten, _ in VE:
    chay([sys.executable, "-B", "ops/cloud_agent_creds_test.py"], cay[ten], ten, lambda l: not l.startswith("  OK ") )
f.write(f"\n# HET {utc()}\n")
