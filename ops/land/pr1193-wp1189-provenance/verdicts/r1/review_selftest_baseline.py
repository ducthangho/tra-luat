"""Đối chứng hai ca Git fixture trên base, chỉ ghi bản sao ngoài cây được review."""
import ast
from pathlib import Path
import subprocess
import sys
from review_checks import BASE, ENV, LOGS, REPO, record

copy = LOGS / "base-repo"
subprocess.run(["git", "clone", "--shared", "--no-checkout", str(REPO), str(copy)], env=ENV, check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
subprocess.run(["git", "-C", str(copy), "checkout", "--detach", BASE], env=ENV, check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
subprocess.run(["git", "-C", str(copy), "config", "core.abbrev", "7"], env=ENV, check=True)
sys.path.insert(0, str(copy / "scripts"))
import tl

names = ["_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim", "_c268_l2_trichotomy_theo_trang_thai_object"]
tree = ast.parse((copy / "scripts/tl_selftest.py").read_text())
functions = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name in names}
assert len(functions) == 2
namespace = {"_TL_MODULE": tl, "_ROOT209": copy, "Path": Path}
for node in functions.values():
    exec(compile(ast.Module(body=[node], type_ignores=[]), "baseline-selftest-cases", "exec"), namespace)

import os
results = {}
for mode in ("nguyen_env", "fixture_signing_off"):
    if mode == "fixture_signing_off":
        count = int(os.environ.get("GIT_CONFIG_COUNT", "0"))
        os.environ.update({"GIT_CONFIG_COUNT": str(count+1), f"GIT_CONFIG_KEY_{count}": "commit.gpgsign",
                           f"GIT_CONFIG_VALUE_{count}": "false"})
    results[mode] = {name: bool(namespace[name]()) for name in names}
expected = not any(results["nguyen_env"].values()) and all(results["fixture_signing_off"].values())
record("A5_baseline_two_cases", "PY312 -B review_selftest_baseline.py (hai hàm gốc trích AST nguyên vẹn từ SHA base)",
       0 if expected else 1, str(results), "passed" if expected else "failed",
       base_sha=BASE, baseline_suite="Chỉ hai ca đỏ; không tuyên bố đã chạy trọn selftest trên base.")
assert expected
