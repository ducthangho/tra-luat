#!/usr/bin/env python3
"""Do lai cac con so ma executor #674 khai trong ops/ci_duong_nhanh.py (docstring) va trong bao cao.
Chay trong `cay/` (clone day du). KHONG ghi gi. Gioi han khai o DO_LAI.md."""
import glob, subprocess, sys
sys.dont_write_bytecode = True
BASE = sys.argv[1] if len(sys.argv) > 1 else "1741e0a1ab7ebce4b26912aefadca56ddfcdc691"
AL = ("ops/land/", "ops/leases/", "ops/reviews/", "ops/specs/")

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

merges = sh("git", "log", "--merges", "--first-parent", "-n", "400", "--format=%H %P", BASE).stdout.split("\n")
tot = fast = bad = 0
for l in merges:
    p = l.split()
    if len(p) != 3:
        continue
    m, a, b = p
    r = subprocess.run(["git", "diff", "--name-only", "--no-renames", "-z", f"{a}...{b}"], capture_output=True)
    if r.returncode:
        continue
    fs = [x for x in r.stdout.decode("utf-8", "surrogateescape").split("\0") if x]
    tot += 1
    if fs and all(f.startswith(AL) for f in fs):
        fast += 1
        if sh("git", "diff", "--check", f"{a}...{b}").returncode:
            bad += 1
print(f"[1] merge 2-cha (first-parent, toi da 400 gan nhat tu {BASE[:7]}) do duoc diff: {tot}; toan allowlist: {fast}; "
      f"trong do `git diff --check` NGUYEN BAN do: {bad}")

sys.path.insert(0, "ops")
import lease_publish as lp  # noqa: E402
ok = xau = 0
for f in sorted(glob.glob("ops/leases/*.yaml")):
    try:
        lp.kiem(lp._doc_yaml(f), f, ".", bo_qua_han=True)
        ok += 1
    except Exception:
        xau += 1
print(f"[2] ops/leases/*.yaml trong cay hien tai: {ok + xau} tep; kiem(bo_qua_han=True) dat {ok}, truot {xau}")
