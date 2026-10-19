"""Observe every self-PID read in the unpatched suite without changing its value."""
import importlib.util
import json
import os
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
rig = Path(json.loads((OUT / "rig-3.13.json").read_text())["base"])
test = rig / ".claude/dev/launcher_test.py"
spec = importlib.util.spec_from_file_location("review_base", test)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
real_getpid = os.getpid
case_names = {f.__name__ for f in module.CA}
observed = []
seen = set()

def observed_getpid():
    frame = sys._getframe(1)
    if Path(frame.f_code.co_filename).name.startswith("launcher"):
        site = frame.f_code.co_name
        if site in ("_chup_cay", "_giet_rieng"):
            cursor = frame
            case = "UNKNOWN"
            while cursor:
                if cursor.f_code.co_name in case_names:
                    case = cursor.f_code.co_name
                    break
                cursor = cursor.f_back
            image = frame.f_locals.get("ra" if site == "_chup_cay" else "anh", {})
            pid = frame.f_locals.get("pid" if site == "_chup_cay" else "q")
            key = (case, site, pid, tuple(sorted(image)))
            if key not in seen:
                seen.add(key)
                record = {"case": case, "site": site, "pid": pid,
                          "snapshot": dict(image), "real_pid": real_getpid()}
                observed.append(record)
                print("OBSERVED " + json.dumps(record, ensure_ascii=False), flush=True)
    return real_getpid()

os.chdir(rig)
os.getpid = observed_getpid
sys.argv = [str(test), "--nhat-ky", str(OUT / "evidence" / "base-audit.journal")]
try:
    rc = module.main()
finally:
    os.getpid = real_getpid
    (OUT / "evidence" / "base-audit.json").write_text(json.dumps(observed, ensure_ascii=False, indent=2))
print("AUDIT_CASES=" + ",".join(sorted({row["case"] for row in observed})), flush=True)
sys.exit(rc)
