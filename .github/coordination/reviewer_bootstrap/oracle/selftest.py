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
SANDBOX = HERE.parent / "sandbox"
if __package__:
    from core.artifacts import verify
    from .answer_key import EXPECTED_FILES, PINS, check_contract
    from .fixture_schemas import SCHEMA_FIXTURES
    from .engine import inventory, keyword_anchors, schema_shape_errors
    from .oracle import OracleError, evaluate, source_readback
else:
    sys.path.insert(0, str(HERE)); sys.path.insert(0, str(CORE))
    from artifacts import verify  # noqa: E402
    from answer_key import EXPECTED_FILES, PINS, check_contract  # noqa: E402
    from fixture_schemas import SCHEMA_FIXTURES  # noqa: E402
    from engine import inventory, keyword_anchors, schema_shape_errors  # noqa: E402
    from oracle import OracleError, evaluate, source_readback  # noqa: E402


def _git(root: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def _materialise(root: pathlib.Path) -> str:
    schema_dir = root / ".github" / "schemas"; schema_dir.mkdir(parents=True)
    for name in EXPECTED_FILES:
        (schema_dir / name).write_text(SCHEMA_FIXTURES[name] + "\n", encoding="utf-8")
    sandbox_dir = root / ".github" / "coordination" / "reviewer_bootstrap" / "sandbox"
    sandbox_dir.mkdir(parents=True)
    for name in ("__init__.py", "runner.py", "selftest.py"):
        shutil.copy2(SANDBOX / name, sandbox_dir / name)
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "WP86 Synthetic Fixture")
    _git(root, "config", "user.email", "wp86-fixture@invalid.example")
    _git(root, "add", ".github/schemas", ".github/coordination/reviewer_bootstrap/sandbox")
    subprocess.check_call(
        ["git", "-C", str(root), "commit", "--quiet", "-m", "synthetic five-schema candidate"],
        env={**os.environ, "GIT_AUTHOR_DATE": "2026-08-12T00:00:00Z", "GIT_COMMITTER_DATE": "2026-08-12T00:00:00Z"},
    )
    return _git(root, "rev-parse", "HEAD")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", help="retain the healthy sealed artifact set at this locator")
    parser.add_argument("--output", help="optional JSON selftest report locator")
    args = parser.parse_args(argv)
    protocol_repo = HERE.parents[3]
    protocol_source = (protocol_repo / PINS["protocol_path"]).read_bytes()
    temp = pathlib.Path(tempfile.mkdtemp(prefix="wp86-oracle-selftest-", dir="/tmp" if os.name != "nt" else None))
    target = temp / "target"
    artifacts = pathlib.Path(args.artifact_root).resolve() if args.artifact_root else temp / "artifacts"
    if artifacts.exists() and any(artifacts.iterdir()):
        raise SystemExit("artifact root must be absent or empty: %s" % artifacts)
    tests = []
    fixture_head = _materialise(target)

    def run(target_path: pathlib.Path, **extra):
        options = {
            "candidate_head": fixture_head,
            "pin_readback": dict(PINS),
            "protocol_source": protocol_source,
            "candidate_source_readback": source_readback(str(target_path), fixture_head),
            "runner_report": None,
        }
        options.update(extra)
        return evaluate(str(target_path), **options)

    try:
        healthy = run(target, artifact_root=str(artifacts))
        tests.append({"name": "healthy_five_schema_oracle", "passed": healthy["ok"] and healthy["healthy_positive_control_ran"] and all(healthy["B1_B6"].values()), "evidence": {"schema_count": healthy["schema_count"], "inventory": healthy["keyword_inventory_total"], "differential": healthy["differential"], "corpus_counts": healthy["corpus_counts"], "healthy": healthy["healthy_positive_control_evidence"], "required_counterexamples": healthy["required_counterexamples"], "B1_B6": healthy["B1_B6"]}})
        measured_runner = healthy["healthy_positive_control_evidence"]["measured_report"]
        source_binding = measured_runner.get("candidate_source_binding", {})
        expected_source_paths = {
            ".github/coordination/reviewer_bootstrap/sandbox/__init__.py",
            ".github/coordination/reviewer_bootstrap/sandbox/runner.py",
            ".github/coordination/reviewer_bootstrap/sandbox/selftest.py",
        }
        tests.append({
            "name": "standalone_sandbox_binds_repo_checkout_tree_and_source_bytes",
            "passed": (
                source_binding.get("candidate_commit_sha") == fixture_head
                and source_binding.get("checkout_head_sha") == fixture_head
                and isinstance(source_binding.get("candidate_tree_sha"), str)
                and len(source_binding.get("candidate_tree_sha", "")) == 40
                and set(source_binding.get("source_files", {})) == expected_source_paths
                and all(
                    isinstance(item, dict)
                    and len(item.get("git_blob_oid", "")) == 40
                    and len(item.get("sha256", "")) == 64
                    and item.get("byte_count", 0) > 0
                    for item in source_binding.get("source_files", {}).values()
                )
            ),
            "evidence": source_binding,
        })
        required = healthy["required_counterexamples"]
        expected_escape = {
            "network", "dns", "loopback", "metadata", "target_write",
            "path_escape", "fd_leak",
        }
        expected_resource = {
            "cpu", "memory", "pid", "output", "timeout", "descendant_cleanup",
        }
        class_groups = {
            "sandbox_escape_classes": expected_escape,
            "resource_classes": expected_resource,
        }
        class_matrix_ok = True
        for group, expected_keys in class_groups.items():
            entries = required.get(group, {})
            class_matrix_ok = class_matrix_ok and set(entries) == expected_keys
            class_matrix_ok = class_matrix_ok and all(
                isinstance(item, dict)
                and isinstance(item.get("test_id"), str)
                and bool(item["test_id"])
                and isinstance(item.get("evidence"), dict)
                and bool(item["evidence"])
                and item.get("passed") is True
                for item in entries.values()
            )
        tests.append({
            "name": "required_counterexamples_exact_class_mapping",
            "passed": class_matrix_ok,
            "evidence": {group: required.get(group) for group in class_groups},
        })
        fake_results = {item["stable_id"]: item for item in healthy["fake_validators"]["results"]}
        tests.append({"name": "five_fakes_execute_and_are_killed", "passed": healthy["fake_validators"]["score"] == "5/5" and all(item["protocol_result_used"] for item in fake_results.values()), "evidence": healthy["fake_validators"]})
        stdout_forger = fake_results["stdout_forger"]
        tests.append({"name": "stdout_forger_deceives_stdout_but_wrong_protocol_is_rejected", "passed": stdout_forger["classification"] == "killed" and stdout_forger["deceptive_stdout_detected"] is True and stdout_forger["killing_case_ids"] == ["protocol_violation"], "evidence": stdout_forger})
        path_aware = fake_results["path_aware_detector"]
        tests.append({"name": "path_aware_defeated_by_blind_reordered_held_out_cases", "passed": path_aware["classification"] == "killed" and bool(path_aware["killing_case_ids"]) and bool(path_aware["held_out_killing_case_ids"]) and path_aware["kill_count"] == len(path_aware["killing_case_ids"]), "evidence": path_aware})
        path_proofs = healthy["mutation_classification_path_proofs"]
        tests.append({"name": "mutation_decomposition_runtime_paths", "passed": set(path_proofs) == {"killed", "survived", "masked", "fixture_gap", "anchor_missing"} and all(item["passed"] for item in path_proofs.values()), "evidence": path_proofs})
        tests.append({"name": "manifest_self_verifies_with_resource_timeout", "passed": healthy["artifact_manifest"]["ok"] and healthy["artifact_manifest"]["verified_files"] == 6 and (artifacts / "runner" / "resource-timeout.json").is_file(), "evidence": healthy["artifact_manifest"]})

        fabricated_artifacts = temp / "fabricated-runner-artifacts"
        try:
            evaluate(str(target), candidate_head=fixture_head, pin_readback=dict(PINS), protocol_source=protocol_source, candidate_source_readback=source_readback(str(target), fixture_head), runner_report={"ok": True, "runner": "Ubuntu-Clean"}, artifact_root=str(fabricated_artifacts))
            fabricated_rejected = False; fabricated_error = ""
        except OracleError as exc:
            fabricated_rejected = True; fabricated_error = str(exc)
        tests.append({"name": "fabricated_runner_report_is_red_and_unsealed", "passed": fabricated_rejected and "external runner report rejected" in fabricated_error and not (fabricated_artifacts / "manifest.json").exists(), "evidence": fabricated_error})

        corrupt_artifacts = temp / "corrupt-pin-artifacts"
        corrupt = dict(PINS); corrupt["packet_spec_hash"] = "0" * 64
        try:
            evaluate(str(target), candidate_head=fixture_head, pin_readback=corrupt, protocol_source=protocol_source, candidate_source_readback=source_readback(str(target), fixture_head), runner_report=None, artifact_root=str(corrupt_artifacts))
            corrupt_rejected = False; corrupt_error = ""
        except OracleError as exc:
            corrupt_rejected = True; corrupt_error = str(exc)
        tests.append({"name": "corrupted_pin_refuses_before_seal", "passed": corrupt_rejected and "pin" in corrupt_error and not (corrupt_artifacts / "manifest.json").exists(), "evidence": corrupt_error})

        wrong_protocol_artifacts = temp / "wrong-protocol-artifacts"
        try:
            evaluate(str(target), candidate_head=fixture_head, pin_readback=dict(PINS), protocol_source=protocol_source + b"tampered", candidate_source_readback=source_readback(str(target), fixture_head), runner_report=None, artifact_root=str(wrong_protocol_artifacts))
            protocol_rejected = False; protocol_error = ""
        except OracleError as exc:
            protocol_rejected = True; protocol_error = str(exc)
        tests.append({"name": "wrong_protocol_source_refuses_before_seal", "passed": protocol_rejected and "protocol source" in protocol_error and not (wrong_protocol_artifacts / "manifest.json").exists(), "evidence": protocol_error})

        wrong_source = temp / "wrong-source"; shutil.copytree(target, wrong_source)
        stale_readback = source_readback(str(wrong_source), fixture_head)
        path = wrong_source / ".github" / "schemas" / "handoff.schema.json"
        path.write_bytes(path.read_bytes() + b"\n")
        wrong_source_artifacts = temp / "wrong-source-artifacts"
        try:
            evaluate(str(wrong_source), candidate_head=fixture_head, pin_readback=dict(PINS), protocol_source=protocol_source, candidate_source_readback=stale_readback, runner_report=None, artifact_root=str(wrong_source_artifacts))
            source_rejected = False; source_error = ""
        except OracleError as exc:
            source_rejected = True; source_error = str(exc)
        tests.append({"name": "wrong_candidate_source_refuses_before_seal", "passed": source_rejected and ("dirty" in source_error or "source readback" in source_error) and not (wrong_source_artifacts / "manifest.json").exists(), "evidence": source_error})

        try:
            source_readback(str(target), "0" * 40)
            arbitrary_rejected = False; arbitrary_error = ""
        except OracleError as exc:
            arbitrary_rejected = True; arbitrary_error = str(exc)
        tests.append({"name": "arbitrary_40hex_candidate_rejected", "passed": arbitrary_rejected and "provenance" in arbitrary_error, "evidence": arbitrary_error})

        standalone_fake_output = temp / "standalone-fake-head-green-evidence.json"
        standalone = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SANDBOX / "selftest.py"),
                "--repo-root",
                str(target),
                "--candidate-head",
                "0" * 40,
                "--output",
                str(standalone_fake_output),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        try:
            standalone_error = json.loads(standalone.stdout)
        except ValueError:
            standalone_error = {}
        tests.append({
            "name": "standalone_sandbox_arbitrary_40hex_is_red_and_unretained",
            "passed": (
                standalone.returncode != 0
                and standalone_error.get("ok") is False
                and standalone_error.get("error", {}).get("name")
                == "CandidateProvenanceError"
                and not standalone_fake_output.exists()
            ),
            "evidence": {
                "rc": standalone.returncode,
                "stdout": standalone_error,
                "stderr": standalone.stderr,
                "green_evidence_exists": standalone_fake_output.exists(),
            },
        })

        wrong_checkout = temp / "wrong-checkout"; shutil.copytree(target, wrong_checkout)
        (wrong_checkout / "unrelated.txt").write_text("different tree\n", encoding="utf-8")
        _git(wrong_checkout, "add", "unrelated.txt")
        subprocess.check_call(
            ["git", "-C", str(wrong_checkout), "commit", "--quiet", "-m", "different checkout"],
            env={**os.environ, "GIT_AUTHOR_DATE": "2026-08-12T00:01:00Z", "GIT_COMMITTER_DATE": "2026-08-12T00:01:00Z"},
        )
        try:
            source_readback(str(wrong_checkout), fixture_head)
            checkout_rejected = False; checkout_error = ""
        except OracleError as exc:
            checkout_rejected = True; checkout_error = str(exc)
        tests.append({"name": "wrong_checkout_tree_rejected", "passed": checkout_rejected and "checkout/head" in checkout_error, "evidence": checkout_error})

        forged_readback = source_readback(str(target), fixture_head)
        forged_readback["candidate_tree_sha"] = "f" * 40
        try:
            evaluate(str(target), candidate_head=fixture_head, pin_readback=dict(PINS), protocol_source=protocol_source, candidate_source_readback=forged_readback, runner_report=None)
            forged_tree_rejected = False; forged_tree_error = ""
        except OracleError as exc:
            forged_tree_rejected = True; forged_tree_error = str(exc)
        tests.append({"name": "forged_tree_readback_rejected", "passed": forged_tree_rejected and "source readback" in forged_tree_error, "evidence": forged_tree_error})

        missing_target = temp / "missing"; shutil.copytree(target, missing_target); (missing_target / ".github" / "schemas" / EXPECTED_FILES[0]).unlink()
        try: run(missing_target); missing_rejected=False; missing_error=""
        except OracleError as exc: missing_rejected=True; missing_error=str(exc)
        tests.append({"name": "missing_schema_rejected", "passed": missing_rejected and ("missing" in missing_error or "dirty" in missing_error), "evidence": missing_error})

        extra_target = temp / "extra"; shutil.copytree(target, extra_target); (extra_target / ".github" / "schemas" / "sixth.schema.json").write_text("{}")
        try: run(extra_target); extra_rejected=False; extra_error=""
        except OracleError as exc: extra_rejected=True; extra_error=str(exc)
        tests.append({"name": "extra_schema_rejected", "passed": extra_rejected and ("extra" in extra_error or "dirty" in extra_error), "evidence": extra_error})

        remote_target = temp / "remote"; shutil.copytree(target, remote_target)
        path = remote_target / ".github" / "schemas" / "handoff.schema.json"; schema=json.loads(path.read_text()); schema["properties"]["head_sha"]={"$ref":"https://attacker.invalid/schema"}; path.write_text(json.dumps(schema))
        remote_errors = schema_shape_errors(schema) + check_contract("handoff.schema.json", schema)
        tests.append({"name": "remote_ref_rejected", "passed": any("remote" in item for item in remote_errors), "evidence": remote_errors})

        unknown_target = temp / "unknown"; shutil.copytree(target, unknown_target)
        path = unknown_target / ".github" / "schemas" / "state.schema.json"; schema=json.loads(path.read_text()); schema["mysteryKeyword"] = True; path.write_text(json.dumps(schema))
        unknown_anchors = keyword_anchors(sorted(inventory(schema)))
        unknown_proof = unknown_anchors.get("mysteryKeyword", {})
        tests.append({"name": "new_keyword_anchor_missing", "passed": unknown_proof.get("valid_passed") is False and unknown_proof.get("invalid_failed") is False, "evidence": unknown_proof})

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
