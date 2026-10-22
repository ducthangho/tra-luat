import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

OUT = Path(__file__).resolve().parent
rig = Path(tempfile.mkdtemp(prefix="wp766-mutants-")) / "repo"
setup = ["git", "clone", "--quiet", "--no-hardlinks", str(OUT.parent / "rv1"), str(rig)]
subprocess.run(setup, check=True)
print(json.dumps({"setup": setup, "rc": 0}), flush=True)
subprocess.run(["git", "-C", str(rig), "checkout", "--quiet", "--detach",
                "701f41c686cef8456d43528ab9556a6b867cd7d6"], check=True)
test_path = rig / ".claude/dev/launcher_test.py"
launcher_path = rig / ".claude/dev/launcher.py"
original_test, original_launcher = test_path.read_text(), launcher_path.read_text()

def load_test(name):
    spec = importlib.util.spec_from_file_location(name, test_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

module = load_test("pristine")
names = ["chup_cay_khong_fail_closed_trong_cay", "chup_cay_fail_closed_ca_may",
         "pid_gia_quay_ve_ghi_cung"]
entries = {entry[0]: entry for entry in module.DOT_BIEN + module.DOT_BIEN_HARNESS}
records = []
for index, name in enumerate(names):
    test_path.write_text(original_test)
    launcher_path.write_text(original_launcher)
    _, (old, new), targets, *_ = entries[name]
    path = test_path if name == names[-1] else launcher_path
    if path == test_path:
        old, new = "\n" + old, "\n" + new
    source = path.read_text()
    assert source.count(old) == 1, (name, source.count(old))
    path.write_text(source.replace(old, new, 1))
    mutated = load_test(f"mutated_{index}")
    for target in targets:
        argv = [sys.executable, "-B", str(test_path), "--lap-ca", target, "--lan", "1"]
        p = subprocess.run(argv, cwd=rig, capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                           start_new_session=True, timeout=45)
        try:
            with mutated._co_lap_toan_cuc():
                getattr(mutated, target)()
        except BaseException as e:
            exception = type(e).__name__
            detail = str(e)
            is_signal = isinstance(e, mutated.TinHieuChotCa)
        else:
            exception, detail, is_signal = "SURVIVED", "", False
        record = {"name": name, "target": target, "cwd": str(rig), "argv": argv,
                  "rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr,
                  "exception": exception, "detail": detail, "is_signal": is_signal}
        records.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
test_path.write_text(original_test)
launcher_path.write_text(original_launcher)
(OUT / "evidence" / "targeted-mutants.json").write_text(json.dumps(records, ensure_ascii=False, indent=2))
good = all(r["rc"] == 1 and r["is_signal"] and "Traceback" not in r["stdout"] + r["stderr"]
           and f'LAP {r["target"]}: 0/1 qua' in r["stdout"] for r in records)
print(f"TARGETED_MUTANTS={len(records)} assertion_kills={sum(r['is_signal'] for r in records)} OK={good}")
sys.exit(0 if good else 1)
