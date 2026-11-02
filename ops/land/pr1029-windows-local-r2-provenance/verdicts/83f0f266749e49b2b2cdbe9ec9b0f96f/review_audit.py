"""Read-only checks for the frozen r2 review; outputs are outside cay-kho."""
import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path

SANDBOX = Path(__file__).resolve().parent
ROOT = SANDBOX / "cay-kho"
BASE = "5f3855eaf47e024b6c63f8923f64d8f80c5de707"
HEAD = "9aa725c72b6b38263de366ce34a80fb384a522a0"
PROTO = "docs/PROTOCOL_DA_PHIEN.md"
ADR = "docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md"
SPEC = "ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r2.md"
SPEC_HASH = "4c92ecbf38fb7f5f97ddea64ed4a43f1cbc9e7a826e87fd8c234dc7e25677c2b"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("PASS " + message)


check(git("rev-parse", "HEAD").decode().strip() == HEAD, "exact HEAD")
check(git("rev-parse", "--is-shallow-repository").strip() == b"false", "full clone")
check(not git("status", "--porcelain=v1", "--untracked-files=all"), "clean worktree")
check(git("config", "--get", "core.abbrev").strip() == b"7", "core.abbrev=7")
check(hashlib.sha256((ROOT / SPEC).read_bytes()).hexdigest() == SPEC_HASH, "spec hash")
check(git("show", f"{BASE}:{SPEC}") == (ROOT / SPEC).read_bytes(), "spec bytes at frozen base")
check(git("merge-base", BASE, HEAD).decode().strip() == BASE, "base is ancestor of HEAD")
check(git("diff", BASE, HEAD) == (SANDBOX / "diff.patch").read_bytes(), "diff.patch equals git diff base HEAD byte-for-byte")

numstat = git("diff", "--numstat", BASE, HEAD).decode().splitlines()
stats = [line.split("\t", 2) for line in numstat]
changed = {row[2] for row in stats}
added = sum(int(row[0]) for row in stats)
deleted = sum(int(row[1]) for row in stats)
check(changed == {PROTO, ADR} and len(stats) == 2, "exact write set: 2 files")
lease = (SANDBOX / "lease.yaml").read_text(encoding="utf-8")
lease_paths = re.search(r"(?m)^write_set:\n((?:- .+\n)+)", lease).group(1)
lease_paths = [line[2:] for line in lease_paths.splitlines()]
check(changed == set(lease_paths), "changed paths equal lease.write_set")
encoded = json.dumps(sorted(unicodedata.normalize("NFC", p).casefold() for p in lease_paths), ensure_ascii=False, separators=(",", ":")).encode()
lease_hash = re.search(r"(?m)^write_set_hash: ([0-9a-f]+)$", lease).group(1)
check(hashlib.sha256(encoded).hexdigest() == lease_hash, "lease.write_set_hash")
check(added <= 120, f"size: files={len(stats)}, added={added}, deleted={deleted}")
check(not any(p.startswith("docs/adr/0057-") for p in changed), "ADR-0057 untouched")
subprocess.run(["git", "-C", str(ROOT), "diff", "--check", BASE, HEAD], check=True)
print("PASS git diff --check")

proto = (ROOT / PROTO).read_text(encoding="utf-8")
before = git("show", f"{BASE}:{PROTO}").decode()
row57_before = next(line for line in before.splitlines() if line.startswith("| `ADR-0057` |"))
row57_after = next(line for line in proto.splitlines() if line.startswith("| `ADR-0057` |"))
cells_before = row57_before.split("|")
cells_after = row57_after.split("|")
check(len(cells_before) == len(cells_after) and all(a == b for i, (a, b) in enumerate(zip(cells_before, cells_after)) if i != 2), "ADR-0057 row: only description cell changed")
check(cells_after[2] == cells_before[2].rstrip() + "; phạm vi và khoá sửa bởi `ADR-0058` ", "ADR-0057 description amendment")
rows58 = [line for line in proto.splitlines() if line.startswith("| `ADR-0058` |")]
check(len(rows58) == 1, "exactly one ADR-0058 routing row")
check(rows58[0].split("|")[4].strip() == "không cổng — kỷ luật executor", "ADR-0058 gate cell exact")
pointer_before = "Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057`."
pointer_after = "Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057` và `ADR-0058`."
check(proto.count(pointer_after) == 1, "neutral pointer names both ADRs exactly once")
restored = proto.replace(rows58[0] + "\n", "").replace(row57_after, row57_before).replace(pointer_after, pointer_before)
check(restored == before, "protocol has exactly the three authorized changes, no extra doctrine")

adr = (ROOT / ADR).read_text(encoding="utf-8")
spec = (ROOT / SPEC).read_text(encoding="utf-8")
for label in ("D7", "D8", "D9"):
    ar = next(line for line in adr.splitlines() if line.startswith("| " + label + " |"))
    sr = next(line for line in spec.splitlines() if line.startswith("| " + label + " |"))
    normalize = lambda value: re.sub(r"\s+", " ", value.replace(",", "")).strip()
    check(normalize(ar.split("|")[3]) == normalize(sr.split("|")[3]), label + " measurement cell matches spec (comma/whitespace ignored)")
sessions = sorted(set(re.findall(r"session_[A-Za-z0-9]{16,}", adr)))
check(sessions == sorted(set(re.findall(r"session_[A-Za-z0-9]{16,}", spec))), "all historical session IDs match spec")
print("SESSIONS " + json.dumps(sessions))

for oid in sorted(set(re.findall(r"`([0-9a-f]{7})`", adr))):
    full = git("rev-parse", "--verify", oid + "^{commit}").decode().strip()
    print("COMMIT " + oid + " " + full)
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", full, HEAD], check=True)
for number in ("0017", "0056", "0057"):
    paths = list((ROOT / "docs/adr").glob(number + "-*.md"))
    check(len(paths) == 1, "referenced ADR-" + number + " exists uniquely")

old_adr = next((ROOT / "docs/adr").glob("0057-*.md")).read_text(encoding="utf-8")
for number in range(1, 11):
    check(re.search(r"(?m)^" + str(number) + r"\. \*\*", old_adr) is not None, "ADR-0057 decision §" + str(number) + " exists")

sources = [p for p in git("ls-files").decode().splitlines() if Path(p).suffix in {".py", ".sh", ".ps1", ".yml", ".yaml"} and not p.startswith(("ops/land/", "ops/reviews/"))]
hits = []
terms = re.compile(r"KHOA\.txt|do-luong\.csv|list_devices|tl-win")
for path in sources:
    for n, line in enumerate((ROOT / path).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if terms.search(line):
            hits.append({"file": path, "line": n, "text": line})
print("OPERATIONAL_SOURCE_SCAN " + json.dumps({"files": len(sources), "hits": hits}, ensure_ascii=False))
check(not hits, "no local-device/lock/ledger reference in operational code; historical evidence excluded")
check(not git("status", "--porcelain=v1", "--untracked-files=all"), "worktree still clean after audit")
print("AUDIT PASSED")
