"""N8 (+ numstat) cho ho so land #1342 r4 (PR #1407), chay trong clone o merge. Dung:
python -X utf8 -B nghiem_thu_1407.py <ruff 0.15.15> <thu_muc_tam>
Ruff --select F: TAP diagnostic (ma, tep, thong diep) tung tep o base e2c3b82, head 46d3907, cha1 d59527f, merge a2c7d75.
numstat: phan packet d135697..46d3907; theo chu e2c3b82..46d3907; PR #1408 e2c3b82..d135697; cha1..merge.
diff --check d135697..46d3907; adr-song; doctrine-scan (rc)."""
import datetime, json, pathlib, subprocess, sys

R, T = sys.argv[1], pathlib.Path(sys.argv[2])
REVS = {"base": "e2c3b82", "head": "46d3907", "cha1": "d59527f", "merge": "a2c7d75"}


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)


print(datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
print("HEAD", git("rev-parse", "HEAD").stdout.strip(), "tree", git("rev-parse", "HEAD^{tree}").stdout.strip())
print(subprocess.run([R, "--version"], capture_output=True, text=True).stdout.strip())
for ten, r in REVS.items():
    d = T / r
    d.mkdir(parents=True, exist_ok=True)
    for f in ("packet_loop.py", "packet_loop_test.py"):
        (d / f).write_bytes(subprocess.run(["git", "show", f"{r}:.claude/dev/{f}"], capture_output=True, check=True).stdout)


def diag(r, f):
    p = subprocess.run([R, "check", "--select", "F", "--output-format", "json", "--isolated", str(T / r / f)], capture_output=True, text=True)
    return sorted((d["code"], f, d["message"]) for d in json.loads(p.stdout or "[]"))


for f in ("packet_loop.py", "packet_loop_test.py"):
    s = {k: diag(r, f) for k, r in REVS.items()}
    print(f"ruff F {f}: " + " ".join(f"{k} {len(v)}" for k, v in s.items())
          + f"; TAP head==base: {s['head'] == s['base']}; TAP merge==cha1: {s['merge'] == s['cha1']}")
    for d in s["base"]:
        print("   base", d)
for nhan, a, b in (("phan packet", "d135697", "46d3907"), ("theo chu", "e2c3b82", "46d3907"),
                   ("PR #1408", "e2c3b82", "d135697"), ("cha1..merge", "d59527f", "a2c7d75")):
    print(f"--- numstat {nhan} {a}..{b}")
    print(git("diff", "--numstat", a, b).stdout.rstrip())
p = git("diff", "--check", "d135697", "46d3907")
print("--- diff --check d135697..46d3907 rc", p.returncode, p.stdout.strip()[:400])
for lenh in ("adr-song", "doctrine-scan"):
    p = subprocess.run([sys.executable, ".claude/dev/packet_loop.py", lenh, "--root", "."], capture_output=True, text=True)
    print(f"--- {lenh} rc {p.returncode}", (p.stdout.strip().splitlines() or [""])[-1][:200])
