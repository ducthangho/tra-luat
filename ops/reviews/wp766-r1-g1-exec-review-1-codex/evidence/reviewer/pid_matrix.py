import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
paths = json.loads((OUT / "rig-3.13.json").read_text())
t81 = "t81_chup_cay_windows_thieu_creationdate_phai_fail_closed"
r766 = "r766_t81_khong_phu_thuoc_pid_cua_luot_chay"
unexpected = 0
records = []
for version in ("3.12", "3.13"):
    for side, cases in (("base", [t81]), ("head", [t81, r766])):
        for case in cases:
            for pid in ("that", "1", "10", "11", "12", "13", "14", "15", "99999"):
                argv = [f"python{version}", "-B", str(OUT / "ep_pid.py"), pid,
                        "--lap-ca", case, "--lan", "1"]
                p = subprocess.run(argv, cwd=paths[side], capture_output=True, text=True,
                                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                                   start_new_session=True, timeout=45)
                expected = 1 if side == "base" and pid in ("10", "11", "12") else 0
                unexpected += p.returncode != expected
                record = {"python": version, "side": side, "pid": pid, "case": case,
                          "cwd": paths[side], "argv": argv, "rc": p.returncode,
                          "stdout": p.stdout, "stderr": p.stderr}
                records.append(record)
                detail = next((s.strip() for s in p.stdout.splitlines() if "  HONG " in s), "")
                print(f"{version} {side} {case.split('_')[0]} getpid={pid}: rc={p.returncode} {detail}", flush=True)
(OUT / "evidence" / "pid-matrix.json").write_text(json.dumps(records, ensure_ascii=False, indent=2))
print(f"MATRIX commands={len(records)} unexpected={unexpected}", flush=True)
sys.exit(bool(unexpected))
