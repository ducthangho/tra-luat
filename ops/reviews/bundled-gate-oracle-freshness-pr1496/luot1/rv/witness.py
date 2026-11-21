"""Minh chứng trực tiếp cho các phản chứng cùng sống."""
import sys

from hunt import CASES, ROOT, run_case

RUN = r'''
import ast
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, "scripts")
import tl
from tl_core import test_fragments as tf
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
frag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frag)
case = CASE_NAME

with tempfile.TemporaryDirectory(prefix="witness_") as tmp:
    root = Path(tmp)
    scripts = root / "scripts"
    fragments = scripts / "test_fragments"
    fragments.mkdir(parents=True)
    name = frag._M1

    if case == "deu_source_content":
        for index in range(6):
            file = f"wp9001_f{index}.py"
            (fragments / file).write_text(frag._nguon(file, "x" * 40 * 1024), encoding="utf-8")
        tf._BUNDLED_SHARD_LIMIT = 100 * 1024
        shards = tf.generate_bundled_modules(fragments)
        module = ast.parse(shards[0][1])
        first_name, first_source = ast.literal_eval(module.body[1].value)[0]
        result = {"shard_count": len(shards), "shard_bytes": len(shards[0][1]),
                  "first_name": first_name, "last_source_line": first_source.splitlines()[-1]}
    elif case == "loader_relaxes_sources_type":
        fragments.rmdir()
        module = frag._van([("wp9001_a.py", "")]).decode()
        module = module.replace("SOURCES = (\n", "SOURCES = [\n").removesuffix(")\n") + "]\n"
        (scripts / name).write_text(module, encoding="utf-8")
        ids, code, _ = frag._nap(tf, scripts)
        result = {"ids": ids, "error": code}
    elif case in ("missing_numeric_ok", "stale_wrong_size"):
        file = "wp9001_a.py"
        (fragments / file).write_text(frag._nguon(file), encoding="utf-8")
        actual_disk_bytes = None
        if case == "stale_wrong_size":
            (scripts / name).write_bytes(frag._van([(file, "")]) + b"#")
            actual_disk_bytes = (scripts / name).stat().st_size
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = tl.main(["test-fragments-check", "--root", str(root), "--json"])
        payload = json.loads(out.getvalue())
        result = {"rc": rc, "ok": payload["ok"], "ok_type": type(payload["ok"]).__name__,
                  "status": payload["status"], "error": payload["error"]}
        if case == "stale_wrong_size":
            result.update(disk_bytes=actual_disk_bytes, aggregate_bytes=payload["actual_bytes"],
                          shard_bytes=payload["shards"][0]["actual_bytes"])
    else:
        raise AssertionError(case)

print("KQ " + json.dumps({"run": True, "kq": {}, "ly_do": result}))
'''

repo = ROOT / "sau"
files = [str(path.relative_to(repo)) for path in (repo / "scripts").rglob("*.py")]
cases = ("deu_source_content", "loader_relaxes_sources_type", "missing_numeric_ok", "stale_wrong_size")
for name in cases:
    for state, edits in (("control", []), ("mutant", CASES[name])):
        run = RUN.replace("CASE_NAME", repr(name))
        output = run_case(repo, files, run, edits)
        print(name, state, output.get("ly_do", output), flush=True)
        if "ly_do" not in output:
            sys.exit(1)
