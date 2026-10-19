"""Build a matched clone pair and measure the complete launcher suites."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent / "rv1"
BASE = "e0273d31aba78b014aa89297f32ff86f9daf0277"
HEAD = "701f41c686cef8456d43528ab9556a6b867cd7d6"
version = sys.argv[1]
rig = Path(tempfile.mkdtemp(prefix=f"wp766-py{version}-"))
paths = {}
for name, sha in [("base", BASE), ("head", HEAD)]:
    path = rig / name
    for argv in (["git", "clone", "--quiet", "--no-hardlinks", str(SOURCE), str(path)],
                 ["git", "-C", str(path), "checkout", "--quiet", "--detach", sha],
                 ["git", "-C", str(path), "config", "core.abbrev", "7"]):
        p = subprocess.run(argv, capture_output=True, text=True)
        print(json.dumps({"setup": argv, "rc": p.returncode, "stderr": p.stderr}), flush=True)
        p.check_returncode()
    paths[name] = str(path)
(OUT / f"rig-{version}.json").write_text(json.dumps(paths, indent=2))
results = {}
for name in paths:
    journal = OUT / "evidence" / f"full_{version}_{name}.journal"
    output = OUT / "evidence" / f"full_{version}_{name}.log"
    argv = [f"python{version}", "-B", ".claude/dev/launcher_test.py", "--nhat-ky", str(journal)]
    print(json.dumps({"run": argv, "cwd": paths[name]}), flush=True)
    with output.open("w") as stream:
        p = subprocess.run(argv, cwd=paths[name], stdout=stream, stderr=subprocess.STDOUT,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                           start_new_session=True, timeout=1000)
    lines = output.read_text().splitlines()
    ends = [line for line in journal.read_text().splitlines() if line.startswith("<<< ra")]
    failures = [line.split()[3:] for line in ends if " -> HONG:" in line or " -> LOI " in line]
    skipped = [line.split()[3:] for line in ends if " -> BO QUA:" in line]
    results[name] = {"rc": p.returncode, "total": len(ends), "failures": failures,
                     "skipped": skipped, "tail": lines[-12:]}
    print(json.dumps({name: results[name]}, ensure_ascii=False), flush=True)
equal = (results["head"]["total"] == results["base"]["total"] + 1
         and results["head"]["failures"] == results["base"]["failures"]
         and results["head"]["skipped"] == results["base"]["skipped"]
         and results["head"]["rc"] == results["base"]["rc"])
(OUT / "evidence" / f"delta-{version}.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(f"DELTA_EQUAL={equal}", flush=True)
sys.exit(0 if equal else 1)
