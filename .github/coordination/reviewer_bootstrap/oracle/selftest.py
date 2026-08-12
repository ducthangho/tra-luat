"""Executable direct/differential/provenance/fake-validator counterexamples."""

from __future__ import annotations

import argparse
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
from answer_key import EXPECTED_FILES, PINS  # noqa: E402
from oracle import OracleError, evaluate, source_readback  # noqa: E402

FIXTURE_HEAD = "632401a58cae9452d52bd1548a9233a5a5844184"


def _repo_root() -> pathlib.Path:
    return HERE.parents[3]


def _git_command(repo: pathlib.Path) -> list[str]:
    try:
        subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--git-dir"], stderr=subprocess.DEVNULL)
        return ["git", "-C", str(repo)]
    except (OSError, subprocess.CalledProcessError):
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
    parser.add_argument("--runner-report", required=True, help="measured sandbox JSON evidence; no default is permitted")
    parser.add_argument("--output", help="optional JSON selftest report locator")
    args = parser.parse_args(argv)
    repo = _repo_root()
    runner_report = json.loads(pathlib.Path(args.runner_report).read_text(encoding="utf-8"))
    protocol_source = (repo / PINS["protocol_path"]).read_bytes()
    temp = pathlib.Path(tempfile.mkdtemp(prefix="wp86-oracle-selftest-", dir="/tmp" if os.name != "nt" else None))
    target = temp / "target"
    artifacts = pathlib.Path(args.artifact_root).resolve() if args.artifact_root else temp / "artifacts"
    if artifacts.exists() and any(artifacts.iterdir()):
        raise SystemExit("artifact root must be absent or empty: %s" % artifacts)
    tests = []

    def run(target_path: pathlib.Path, **extra):
        options = {
            "candidate_head": FIXTURE_HEAD,
            "pin_readback": dict(PINS),
            "protocol_source": protocol_source,
            "candidate_source_readback": source_readback(str(target_path), FIXTURE_HEAD),
            "runner_report": runner_report,
        }
        options.update(extra)
        return evaluate(str(target_path), **options)

    try:
        _materialise(target, repo)
        healthy = run(target, artifact_root=str(artifacts))
        tests.append({"name": "healthy_five_schema_oracle", "passed": healthy["ok"] and healthy["healthy_positive_control_ran"], "evidence": {"schema_count": healthy["schema_count"], "inventory": healthy["keyword_inventory_total"], "differential": healthy["differential"], "corpus_counts": healthy["corpus_counts"], "healthy": healthy["healthy_positive_control_evidence"]}})
        fake_results = {item["stable_id"]: item for item in healthy["fake_validators"]["results"]}
        tests.append({"name": "five_fakes_execute_and_are_killed", "passed": healthy["fake_validators"]["score"] == "5/5" and all(item["protocol_result_used"] for item in fake_results.values()), "evidence": healthy["fake_validators"]})
        stdout_forger = fake_results["stdout_forger"]
        tests.append({"name": "stdout_forger_deceives_stdout_but_wrong_protocol_is_rejected", "passed": stdout_forger["classification"] == "killed" and stdout_forger["deceptive_stdout_detected"] is True and stdout_forger["killing_case_ids"] == ["protocol_violation"], "evidence": stdout_forger})
        path_aware = fake_results["path_aware_detector"]
        tests.append({"name": "path_aware_defeated_by_blind_reordered_held_out_cases", "passed": path_aware["classification"] == "killed" and bool(path_aware["killing_case_ids"]) and any(item["held_out"] for item in healthy["case_matrix"] if item["case_id"] in path_aware["killing_case_ids"]), "evidence": path_aware})
        path_proofs = healthy["mutation_classification_path_proofs"]
        tests.append({"name": "mutation_decomposition_runtime_paths", "passed": set(path_proofs) == {"killed", "survived", "masked", "fixture_gap", "anchor_missing"} and all(item["passed"] for item in path_proofs.values()), "evidence": path_proofs})
        tests.append({"name": "manifest_self_verifies_with_resource_timeout", "passed": healthy["artifact_manifest"]["ok"] and healthy["artifact_manifest"]["verified_files"] == 6 and (artifacts / "runner" / "resource-timeout.json").is_file(), "evidence": healthy["artifact_manifest"]})

        zero_artifacts = temp / "zero-run-artifacts"
        try:
            evaluate(str(target), candidate_head=FIXTURE_HEAD, pin_readback=dict(PINS), protocol_source=protocol_source, candidate_source_readback=source_readback(str(target), FIXTURE_HEAD), runner_report=None, artifact_root=str(zero_artifacts))
            zero_rejected = False; zero_error = ""
        except OracleError as exc:
            zero_rejected = True; zero_error = str(exc)
        tests.append({"name": "zero_sandbox_run_is_red_and_unsealed", "passed": zero_rejected and "runner report" in zero_error and not (zero_artifacts / "manifest.json").exists(), "evidence": zero_error})

        corrupt_artifacts = temp / "corrupt-pin-artifacts"
        corrupt = dict(PINS); corrupt["packet_spec_hash"] = "0" * 64
        try:
            evaluate(str(target), candidate_head=FIXTURE_HEAD, pin_readback=corrupt, protocol_source=protocol_source, candidate_source_readback=source_readback(str(target), FIXTURE_HEAD), runner_report=runner_report, artifact_root=str(corrupt_artifacts))
            corrupt_rejected = False; corrupt_error = ""
        except OracleError as exc:
            corrupt_rejected = True; corrupt_error = str(exc)
        tests.append({"name": "corrupted_pin_refuses_before_seal", "passed": corrupt_rejected and "pin" in corrupt_error and not (corrupt_artifacts / "manifest.json").exists(), "evidence": corrupt_error})

        wrong_protocol_artifacts = temp / "wrong-protocol-artifacts"
        try:
            evaluate(str(target), candidate_head=FIXTURE_HEAD, pin_readback=dict(PINS), protocol_source=protocol_source + b"tampered", candidate_source_readback=source_readback(str(target), FIXTURE_HEAD), runner_report=runner_report, artifact_root=str(wrong_protocol_artifacts))
            protocol_rejected = False; protocol_error = ""
        except OracleError as exc:
            protocol_rejected = True; protocol_error = str(exc)
        tests.append({"name": "wrong_protocol_source_refuses_before_seal", "passed": protocol_rejected and "protocol source" in protocol_error and not (wrong_protocol_artifacts / "manifest.json").exists(), "evidence": protocol_error})

        wrong_source = temp / "wrong-source"; shutil.copytree(target, wrong_source)
        stale_readback = source_readback(str(wrong_source), FIXTURE_HEAD)
        path = wrong_source / ".github" / "schemas" / "handoff.schema.json"
        path.write_bytes(path.read_bytes() + b"\n")
        wrong_source_artifacts = temp / "wrong-source-artifacts"
        try:
            evaluate(str(wrong_source), candidate_head=FIXTURE_HEAD, pin_readback=dict(PINS), protocol_source=protocol_source, candidate_source_readback=stale_readback, runner_report=runner_report, artifact_root=str(wrong_source_artifacts))
            source_rejected = False; source_error = ""
        except OracleError as exc:
            source_rejected = True; source_error = str(exc)
        tests.append({"name": "wrong_candidate_source_refuses_before_seal", "passed": source_rejected and "source readback" in source_error and not (wrong_source_artifacts / "manifest.json").exists(), "evidence": source_error})

        missing_target = temp / "missing"; shutil.copytree(target, missing_target); (missing_target / ".github" / "schemas" / EXPECTED_FILES[0]).unlink()
        try: run(missing_target); missing_rejected=False; missing_error=""
        except OracleError as exc: missing_rejected=True; missing_error=str(exc)
        tests.append({"name": "missing_schema_rejected", "passed": missing_rejected and "missing" in missing_error, "evidence": missing_error})

        extra_target = temp / "extra"; shutil.copytree(target, extra_target); (extra_target / ".github" / "schemas" / "sixth.schema.json").write_text("{}")
        try: run(extra_target); extra_rejected=False; extra_error=""
        except OracleError as exc: extra_rejected=True; extra_error=str(exc)
        tests.append({"name": "extra_schema_rejected", "passed": extra_rejected and "extra" in extra_error, "evidence": extra_error})

        remote_target = temp / "remote"; shutil.copytree(target, remote_target)
        path = remote_target / ".github" / "schemas" / "handoff.schema.json"; schema=json.loads(path.read_text()); schema["properties"]["head_sha"]={"$ref":"https://attacker.invalid/schema"}; path.write_text(json.dumps(schema))
        remote = run(remote_target)
        tests.append({"name": "remote_ref_rejected", "passed": bool(remote["direct_contract_errors"]["handoff.schema.json"]), "evidence": remote["direct_contract_errors"]["handoff.schema.json"]})

        unknown_target = temp / "unknown"; shutil.copytree(target, unknown_target)
        path = unknown_target / ".github" / "schemas" / "state.schema.json"; schema=json.loads(path.read_text()); schema["mysteryKeyword"] = True; path.write_text(json.dumps(schema))
        unknown = run(unknown_target)
        tests.append({"name": "new_keyword_anchor_missing", "passed": any("ANCHOR MISSING" in item for item in unknown["direct_contract_errors"]["state.schema.json"]), "evidence": unknown["direct_contract_errors"]["state.schema.json"]})

        tampered = temp / "tampered"; shutil.copytree(artifacts, tampered); (tampered / "corpus" / "objects.json").write_text("tampered")
        tamper_report = verify(str(tampered))
        tests.append({"name": "artifact_content_tamper_rejected", "passed": "corpus/objects.json" in tamper_report["hash_mismatches"], "evidence": tamper_report})
        deleted = temp / "deleted"; shutil.copytree(artifacts, deleted); (deleted / "runner" / "resource-timeout.json").unlink()
        delete_report = verify(str(deleted))
        tests.append({"name": "artifact_delete_names_locator", "passed": "runner/resource-timeout.json" in delete_report["missing_files"], "evidence": delete_report})
    finally:
        shutil.rmtree(temp, ignore_errors=True)
    passed = sum(1 for test in tests if test["passed"])
    report = {"ok": passed == len(tests) and bool(tests), "passed": passed, "total": len(tests), "tests": tests}
    if args.output:
        output = pathlib.Path(args.output).resolve(); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
