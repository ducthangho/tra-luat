"""Executable direct/differential/corpus/fake-validator/oracle counterexamples."""

from __future__ import annotations

import argparse
import copy
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
CORE = HERE.parent / "core"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(CORE))
from artifacts import verify  # noqa: E402
from answer_key import EXPECTED_FILES  # noqa: E402
from oracle import OracleError, evaluate  # noqa: E402

FIXTURE_HEAD = "632401a58cae9452d52bd1548a9233a5a5844184"


def _repo_root() -> pathlib.Path:
    return HERE.parents[3]


def _git_command(repo: pathlib.Path) -> list[str]:
    try:
        subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--git-dir"], stderr=subprocess.DEVNULL)
        return ["git", "-C", str(repo)]
    except (OSError, subprocess.CalledProcessError):
        # A linked Windows worktree's .git file contains a Windows absolute path,
        # which Linux git cannot interpret.  Git-for-Windows can, and is invoked
        # locally through WSL interoperability; no network is involved.
        git_exe = pathlib.Path("/mnt/c/Program Files/Git/cmd/git.exe")
        text = str(repo)
        if text.startswith("/mnt/"):
            drive, rest = text[5], text[7:]
            text = "%s:/%s" % (drive.upper(), rest)
        return [str(git_exe), "-C", text]


def _materialise(root: pathlib.Path, repo: pathlib.Path):
    schema_dir = root / ".github" / "schemas"; schema_dir.mkdir(parents=True)
    for name in EXPECTED_FILES:
        raw = subprocess.check_output(_git_command(repo) + ["show", "%s:.github/schemas/%s" % (FIXTURE_HEAD, name)])
        (schema_dir / name).write_bytes(raw)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", help="retain the healthy sealed artifact set at this locator")
    parser.add_argument("--runner-report", help="sandbox JSON evidence to embed in the runner artifact")
    parser.add_argument("--output", help="optional JSON selftest report locator")
    args = parser.parse_args(argv)
    repo = _repo_root()
    temp = pathlib.Path(tempfile.mkdtemp(prefix="wp86-oracle-selftest-", dir="/tmp" if os.name != "nt" else None))
    target = temp / "target"
    artifacts = pathlib.Path(args.artifact_root).resolve() if args.artifact_root else temp / "artifacts"
    if artifacts.exists() and any(artifacts.iterdir()):
        raise SystemExit("artifact root must be absent or empty: %s" % artifacts)
    runner_report = {"runner": "Ubuntu-Clean", "cleanup": {"descendants_gone": True}}
    if args.runner_report:
        runner_report = json.loads(pathlib.Path(args.runner_report).read_text(encoding="utf-8"))
    tests = []
    try:
        _materialise(target, repo)
        healthy = evaluate(str(target), candidate_head=FIXTURE_HEAD, artifact_root=str(artifacts), runner_report=runner_report)
        tests.append({"name": "healthy_five_schema_oracle", "passed": healthy["ok"], "evidence": {"schema_count": healthy["schema_count"], "inventory": healthy["keyword_inventory_total"], "differential": healthy["differential"], "corpus_counts": healthy["corpus_counts"]}})
        tests.append({"name": "all_five_fake_validators_killed", "passed": healthy["fake_validators"]["score"] == "5/5", "evidence": healthy["fake_validators"]})
        tests.append({"name": "manifest_self_verifies", "passed": healthy["artifact_manifest"]["ok"] and healthy["artifact_manifest"]["verified_files"] == 5, "evidence": healthy["artifact_manifest"]})

        missing_target = temp / "missing"; shutil.copytree(target, missing_target); (missing_target / ".github" / "schemas" / EXPECTED_FILES[0]).unlink()
        try: evaluate(str(missing_target), candidate_head=FIXTURE_HEAD); missing_rejected=False; missing_error=""
        except OracleError as exc: missing_rejected=True; missing_error=str(exc)
        tests.append({"name": "missing_schema_rejected", "passed": missing_rejected and "missing" in missing_error, "evidence": missing_error})

        extra_target = temp / "extra"; shutil.copytree(target, extra_target); (extra_target / ".github" / "schemas" / "sixth.schema.json").write_text("{}")
        try: evaluate(str(extra_target), candidate_head=FIXTURE_HEAD); extra_rejected=False; extra_error=""
        except OracleError as exc: extra_rejected=True; extra_error=str(exc)
        tests.append({"name": "extra_schema_rejected", "passed": extra_rejected and "extra" in extra_error, "evidence": extra_error})

        remote_target = temp / "remote"; shutil.copytree(target, remote_target)
        path = remote_target / ".github" / "schemas" / "handoff.schema.json"; schema=json.loads(path.read_text()); schema["properties"]["head_sha"]={"$ref":"https://attacker.invalid/schema"}; path.write_text(json.dumps(schema))
        remote = evaluate(str(remote_target), candidate_head=FIXTURE_HEAD)
        tests.append({"name": "remote_ref_rejected", "passed": bool(remote["direct_contract_errors"]["handoff.schema.json"]), "evidence": remote["direct_contract_errors"]["handoff.schema.json"]})

        unknown_target = temp / "unknown"; shutil.copytree(target, unknown_target)
        path = unknown_target / ".github" / "schemas" / "state.schema.json"; schema=json.loads(path.read_text()); schema["mysteryKeyword"] = True; path.write_text(json.dumps(schema))
        unknown = evaluate(str(unknown_target), candidate_head=FIXTURE_HEAD)
        tests.append({"name": "new_keyword_anchor_missing", "passed": any("ANCHOR MISSING" in item for item in unknown["direct_contract_errors"]["state.schema.json"]), "evidence": unknown["direct_contract_errors"]["state.schema.json"]})

        tampered = temp / "tampered"; shutil.copytree(artifacts, tampered); (tampered / "corpus" / "objects.json").write_text("tampered")
        tamper_report = verify(str(tampered))
        tests.append({"name": "artifact_content_tamper_rejected", "passed": "corpus/objects.json" in tamper_report["hash_mismatches"], "evidence": tamper_report})
        deleted = temp / "deleted"; shutil.copytree(artifacts, deleted); (deleted / "matrix" / "results.json").unlink()
        delete_report = verify(str(deleted))
        tests.append({"name": "artifact_delete_names_locator", "passed": "matrix/results.json" in delete_report["missing_files"], "evidence": delete_report})
    finally:
        shutil.rmtree(temp, ignore_errors=True)
    passed = sum(1 for test in tests if test["passed"])
    report = {"ok": passed == len(tests) and bool(tests), "passed": passed, "total": len(tests), "tests": tests}
    if args.output:
        output = pathlib.Path(args.output).resolve(); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
