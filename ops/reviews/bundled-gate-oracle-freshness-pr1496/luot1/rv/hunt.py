"""Chạy phản chứng ngoài ma trận bằng cùng mã RUN và cùng cách sao cây."""
import argparse
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MATRIX = ROOT / "spec" / "ma_tran_r11.py"
TF = "scripts/tl_core/test_fragments.py"
RL = "scripts/tl_core/release.py"
BODY = '        body = header + lines + [")"]\n'
DECLARATION = 'for k in range(2, len(groups) + 1)).rstrip() + ")")'
RET_RC = '_print_json_or_text(payload, getattr(a, "json", False))\n    return 0 if payload.get("ok") else 2'
EXTRA = '            "extra_shards": extra,\n'
STALE = '            "status": "stale",\n            "error": "GENERATED_BUNDLE_STALE",\n'
SOURCES_CONTRACT = '    if type(raw_entries) is not tuple:\n'
PATHS = ("nen", "sau")

CASES = {
    "control": [],
    "hai_swapped_ast": [(TF, BODY, BODY + '''
        if len(groups) == 1 and len(lines) == 2:
            body[3] = "BUNDLED_FRAGMENT_SOURCES, UNUSED = ("
            body[-1] = "), None"
''')],
    "deu_source_content": [(TF, BODY, BODY + '''
        if len(groups) > 1 and len(lines) == 2 and all(30000 < len(line) < 50000 for line in lines):
            body[4] = body[4].replace("return True", "return None")
''')],
    "lech_assert": [(TF, BODY, BODY + '''
        if index > 1 and any("đ" in line for line in lines):
            body.append("assert True")
''')],
    "lon_nonliteral": [(TF, BODY, BODY + '''
        if any(len(line) > 140000 for line in lines):
            body[3] = "BUNDLED_FRAGMENT_SOURCES = tuple(("
            body[-1] = "))"
''')],
    "deu_manifest_reverse": [(TF, DECLARATION,
                              DECLARATION.replace("range(2, len(groups) + 1)",
                                                  "range(len(groups), 1, -1)"))],
    "loader_relaxes_sources_type": [(TF, SOURCES_CONTRACT,
                                    '    if type(raw_entries) not in (tuple, list):\n')],
    "writer_primary_eol": [(TF, '        (scripts / name).write_bytes(data)\n',
                            '        (scripts / name).write_bytes(data.rstrip(b"\\n") if name == _BUNDLED_MODULE_NAME else data)\n')],
    "extra_duplicate_names": [(RL, EXTRA, '            "extra_shards": extra + extra,\n')],
    "stale_rc_wrong": [(RL, RET_RC, RET_RC.replace("else 2", "else 1"))],
    "absent_shard_empty_field": [(RL, '"actual_bytes": (len(a) if a is not None else None)}',
                                 '"actual_bytes": (len(a) if a is not None else -1)}')],
    "missing_numeric_ok": [(RL, 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}',
                            'return {**payload, "ok": 0, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}')],
    "current_has_error": [(RL, '        "status": "current",\n        "expected_sha256": expected_sha256,\n',
                          '        "status": "current",\n        "error": "GENERATED_BUNDLE_STALE",\n        "expected_sha256": expected_sha256,\n')],
    "stale_wrong_size": [(RL, STALE, STALE + '            "shards": [dict(s, actual_bytes=s["expected_bytes"]) for s in shards] if all(s["actual_bytes"] is not None for s in shards) else shards,\n')],
}


def matrix_run():
    module = ast.parse(MATRIX.read_text())
    return next(ast.literal_eval(node.value) for node in module.body
                if isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "RUN")


def run_case(repo, files, runner, edits):
    with tempfile.TemporaryDirectory(prefix="hunt_", dir=ROOT / "tmp") as temp:
        copy = Path(temp) / "r"
        for rel in files:
            source = repo / rel
            if source.is_file():
                dest = copy / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, dest)
        for rel, before, after in edits:
            path = copy / rel
            source = path.read_text(encoding="utf-8")
            if source.count(before) != 1 or before == after:
                return {"anchor": [rel, source.count(before)]}
            path.write_text(source.replace(before, after), encoding="utf-8", newline="\n")
        process = subprocess.run([sys.executable, "-B", "-c", runner], cwd=copy,
                                 capture_output=True, text=True)
    lines = [line[3:] for line in process.stdout.splitlines() if line.startswith("KQ ")]
    if process.returncode or not lines:
        return {"rc": process.returncode, "exception": process.stderr[-500:]}
    result = json.loads(lines[-1])
    return {"rc": process.returncode, "run": result["run"], "so_nhan": len(result["kq"]),
            "do": [f"V{n}" for n in range(1, 33) if result["kq"].get(f"V{n}") is not True],
            "ly_do": result["ly_do"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lane", choices=PATHS)
    parser.add_argument("cases", nargs="*")
    args = parser.parse_args()
    chosen = args.cases or list(CASES)
    if bad := set(chosen) - CASES.keys():
        parser.error(f"Ca không tồn tại: {bad}")
    repo = ROOT / args.lane
    files = subprocess.check_output(["git", "-C", str(repo), "ls-files", "-z"]).decode().split("\0")[:-1]
    runner = matrix_run()
    missing = False
    for name in chosen:
        result = run_case(repo, files, runner, CASES[name])
        print(name, json.dumps(result, ensure_ascii=False), flush=True)
        missing |= "anchor" in result or result.get("so_nhan") != 32
    return int(missing)


if __name__ == "__main__":
    sys.exit(main())
