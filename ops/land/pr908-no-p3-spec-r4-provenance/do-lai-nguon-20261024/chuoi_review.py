"""Trich tu 3 spec tai merge SHA: moi muc 'Va sau review ...' -> reviewed_sha, sha256 VERDICT/HINT, so lop. Doc bang git show."""
import re, subprocess, sys
M = sys.argv[1]
for f in ["no-p3-lease-spec-hash-r4.md", "no-p3-cong-cu-ho-so-r4.md", "no-p3-dang-ky-ci-r2.md"]:
    t = subprocess.run(["git", "show", f"{M}:ops/specs/{f}"], capture_output=True, text=True, check=True).stdout
    print(f"## {f}")
    for m in re.finditer(r"^## (Vá sau review[^\n]*)\n(.*?)(?=^## |\Z)", t, re.M | re.S):
        body = m.group(2)
        rs = re.search(r"`reviewed_sha` `([0-9a-f]{40})`", body)
        v = re.search(r"VERDICT sha256 `([0-9a-f]{64})`", body)
        h = re.search(r"HINT sha256 `([0-9a-f]{64})`", body)
        n = re.search(r"(\d+) P1 · (\d+) P2 · (\d+) P3", body)
        print(f"{m.group(1)} | reviewed {rs.group(1)[:12] if rs else '-'} | VERDICT {v.group(1)[:16] if v else '-'} | HINT {h.group(1)[:16] if h else '-'} | {'/'.join(n.groups()) if n else '-'}")
