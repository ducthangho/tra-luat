import hashlib
from pathlib import Path
import re
import sys

def refs(path):
    result = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        oid, ref = line.split("\t")
        if not re.fullmatch(r"[0-9a-f]{40}", oid) or ref in result:
            raise ValueError("invalid or duplicate ref")
        result[ref] = oid
    if not result:
        raise ValueError("empty remote response")
    raw = "".join(f"{result[r]}\t{r}\n" for r in sorted(result)).encode("utf-8")
    print("REFS", len(result), hashlib.sha256(raw).hexdigest())
    return result

before, after = map(refs, sys.argv[1:])
changed = sorted(r for r in before.keys() | after.keys() if before.get(r) != after.get(r))
for ref in changed:
    print(ref, before.get(ref, "ABSENT"), after.get(ref, "ABSENT"), sep="\t")
raise SystemExit(1 if changed else 0)
