"""Direct, differential and behavioural oracle for five protocol schemas."""

from __future__ import annotations

import datetime
import hashlib
import importlib.metadata
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
CORE = HERE.parent / "core"
SANDBOX = HERE.parent / "sandbox"
if __package__:
    from core.artifacts import ArtifactSet, sha256_file, verify
    from .answer_key import (
        DIALECT, EXPECTED_FILES, INDEPENDENT_ENGINE_PIN, PINS,
        check_contract, verify_pin_readback,
    )
    from .corpus import Case, build
    from .engine import inventory, keyword_anchors, schema_shape_errors, validate
    from .fake_validators import classification_path_proofs, mutation_score
else:
    sys.path.insert(0, str(CORE))
    from artifacts import ArtifactSet, sha256_file, verify  # noqa: E402
    from answer_key import (  # noqa: E402
        DIALECT, EXPECTED_FILES, INDEPENDENT_ENGINE_PIN, PINS,
        check_contract, verify_pin_readback,
    )
    from corpus import Case, build  # noqa: E402
    from engine import inventory, keyword_anchors, schema_shape_errors, validate  # noqa: E402
    from fake_validators import classification_path_proofs, mutation_score  # noqa: E402


class OracleError(RuntimeError):
    pass


_FRESH_RUNNER_CACHE: dict[tuple[str, str, str], Mapping[str, object]] = {}


def _json_no_duplicates(raw: str, locator: str) -> object:
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise OracleError("duplicate JSON key in %s: %s" % (locator, key))
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs)
    except (ValueError, UnicodeError) as exc:
        raise OracleError("invalid JSON in %s: %s" % (locator, exc)) from exc


def _read_regular_schema(path: pathlib.Path, locator: str) -> bytes:
    """No-follow regular-file read with post-open identity verification."""
    try:
        on_disk = os.lstat(path)
        if not stat.S_ISREG(on_disk.st_mode) or on_disk.st_nlink != 1:
            raise OracleError("schema is not a single-link regular file: %s" % locator)
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if (
                not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (on_disk.st_dev, on_disk.st_ino)
                or opened.st_nlink != 1
            ):
                raise OracleError("schema changed identity while opening: %s" % locator)
            if opened.st_size > 1024 * 1024:
                raise OracleError("schema exceeds 1 MiB limit: %s" % locator)
            return handle.read()
    except OracleError:
        raise
    except OSError as exc:
        raise OracleError("schema cannot be read safely: %s: %s" % (locator, exc)) from exc


def _load_schemas(
    target_root: str,
) -> tuple[dict[str, Mapping[str, object]], dict[str, object]]:
    root = pathlib.Path(target_root).resolve()
    schema_dir = root / ".github" / "schemas"
    if not schema_dir.is_dir() or schema_dir.is_symlink():
        raise OracleError("candidate schema directory missing or unsafe: %s" % schema_dir)
    actual = sorted(path.name for path in schema_dir.iterdir() if path.name.endswith(".json"))
    expected = sorted(EXPECTED_FILES)
    if actual != expected:
        raise OracleError("schema inventory mismatch: missing=%s extra=%s" % (
            sorted(set(expected) - set(actual)), sorted(set(actual) - set(expected))))
    result: dict[str, Mapping[str, object]] = {}
    file_digests: dict[str, str] = {}
    bundle = hashlib.sha256()
    for name in EXPECTED_FILES:
        path = schema_dir / name
        raw_bytes = _read_regular_schema(path, name)
        file_digests[name] = hashlib.sha256(raw_bytes).hexdigest()
        bundle.update(name.encode("utf-8") + b"\0" + raw_bytes)
        value = _json_no_duplicates(raw_bytes.decode("utf-8"), name)
        if not isinstance(value, dict):
            raise OracleError("schema root is not an object: %s" % name)
        result[name] = value
    return result, {
        "schema_bundle_sha256": bundle.hexdigest(),
        "schema_file_sha256": file_digests,
    }


def _git(root: pathlib.Path, *args: str, text: bool = True):
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            stderr=subprocess.PIPE,
            text=text,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise OracleError("candidate Git provenance unavailable: %s" % " ".join(args)) from exc


def source_readback(target_root: str, candidate_head: str) -> dict[str, object]:
    """Bind commit/tree/blob objects, checkout state and exact schema bytes."""
    if not isinstance(candidate_head, str) or not re.fullmatch(r"[0-9a-f]{40}", candidate_head):
        raise OracleError("candidate_head must be an exact 40-hex Git oid")
    root = pathlib.Path(target_root).resolve()
    commit = _git(root, "rev-parse", "--verify", "%s^{commit}" % candidate_head).strip()
    checkout_head = _git(root, "rev-parse", "--verify", "HEAD^{commit}").strip()
    if commit != candidate_head or checkout_head != candidate_head:
        raise OracleError("candidate checkout/head does not match declared commit")
    tree = _git(root, "rev-parse", "%s^{tree}" % candidate_head).strip()
    inventory = _git(
        root, "ls-tree", "--name-only", "%s:.github/schemas" % candidate_head
    ).splitlines()
    if sorted(inventory) != sorted(EXPECTED_FILES):
        raise OracleError("candidate Git tree schema inventory mismatch")
    status = _git(root, "status", "--porcelain=v1", "--", ".github/schemas").strip()
    if status:
        raise OracleError("candidate schema checkout is dirty or untracked")
    _, measured = _load_schemas(str(root))
    blob_oids: dict[str, str] = {}
    for name in EXPECTED_FILES:
        locator = ".github/schemas/%s" % name
        blob = _git(root, "rev-parse", "%s:%s" % (candidate_head, locator)).strip()
        git_bytes = _git(root, "cat-file", "blob", blob, text=False)
        disk_bytes = _read_regular_schema(root / locator, name)
        if git_bytes != disk_bytes:
            raise OracleError("candidate schema bytes differ from Git blob: %s" % name)
        blob_oids[name] = blob
    return {
        "candidate_head": candidate_head,
        "candidate_commit_sha": commit,
        "candidate_tree_sha": tree,
        "schema_blob_oids": blob_oids,
        **measured,
    }


def _validate_source_readback(
    measured: Mapping[str, object],
    readback: Mapping[str, object],
    candidate_head: str,
) -> None:
    expected = dict(measured)
    if expected.get("candidate_head") != candidate_head:
        raise OracleError("measured source does not match candidate head")
    if dict(readback) != expected:
        raise OracleError("candidate schema source readback mismatch")


def _validate_runner_report(
    report: Mapping[str, object] | None, candidate_head: str, target_root: str
) -> dict[str, object]:
    if report is not None:
        raise OracleError(
            "external runner report rejected; oracle measures the sandbox in-process"
        )
    runner_sha = sha256_file(SANDBOX / "runner.py")
    resolved_target = str(pathlib.Path(target_root).resolve())
    cache_key = (candidate_head, runner_sha, resolved_target)
    measured_report = _FRESH_RUNNER_CACHE.get(cache_key)
    if measured_report is None:
        try:
            raw = subprocess.check_output(
                [
                    sys.executable,
                    "-B",
                    str(SANDBOX / "selftest.py"),
                    "--candidate-head",
                    candidate_head,
                    "--repo-root",
                    resolved_target,
                ],
                stderr=subprocess.PIPE,
                text=True,
                timeout=90,
            )
            parsed = json.loads(raw)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            raise OracleError("fresh sandbox measurement failed") from exc
        if not isinstance(parsed, Mapping):
            raise OracleError("fresh sandbox measurement is not an object")
        measured_report = parsed
        _FRESH_RUNNER_CACHE[cache_key] = measured_report
    report = measured_report
    tests = report.get("tests")
    if (
        report.get("schema_version") != 1
        or report.get("candidate_head") != candidate_head
        or report.get("ok") is not True
        or not isinstance(tests, list)
        or not tests
        or report.get("passed") != report.get("total")
        or report.get("total") != len(tests)
    ):
        raise OracleError("runner report did not pass a non-empty measured suite")
    source_binding = report.get("candidate_source_binding")
    if (
        not isinstance(source_binding, Mapping)
        or source_binding.get("repo_root") != resolved_target
        or source_binding.get("candidate_commit_sha") != candidate_head
        or source_binding.get("checkout_head_sha") != candidate_head
        or not re.fullmatch(r"[0-9a-f]{40}", str(source_binding.get("candidate_tree_sha", "")))
        or not re.fullmatch(
            r"[0-9a-f]{64}", str(source_binding.get("source_inventory_sha256", ""))
        )
    ):
        raise OracleError("runner report candidate source binding mismatch")
    source_files = source_binding.get("source_files")
    expected_source_files = {
        ".github/coordination/reviewer_bootstrap/sandbox/__init__.py",
        ".github/coordination/reviewer_bootstrap/sandbox/runner.py",
        ".github/coordination/reviewer_bootstrap/sandbox/selftest.py",
    }
    if not isinstance(source_files, Mapping) or set(source_files) != expected_source_files:
        raise OracleError("runner report candidate source inventory mismatch")
    by_name = {
        item.get("name"): item
        for item in tests
        if isinstance(item, Mapping) and isinstance(item.get("name"), str)
    }
    required = {
        "healthy_positive_control",
        "credential_channel_controls",
        "credential_env_argv_cwd_fd_procfs",
        "network_fixture_positive_controls",
        "network_dns_loopback_metadata_unix",
        "memory_hog",
        "cpu_busy_loop",
        "pid_fork_bomb",
        "stdout_flood",
        "timeout_and_descendant_cleanup",
        "target_readonly_escape_and_links",
        "retained_output_intermediate_symlink_rejected",
        "credential_shape_alias_counterexamples",
    }
    missing = sorted(required - set(by_name))
    if missing:
        raise OracleError("runner report missing measured controls: %s" % missing)
    if any(item.get("passed") is not True for item in by_name.values()):
        raise OracleError("runner report contains a failed/fixture-gap control")
    class_matrix = report.get("counterexample_classes")
    expected_class_keys = {
        "sandbox_escape_classes": {
            "network", "dns", "loopback", "metadata", "target_write",
            "path_escape", "fd_leak",
        },
        "resource_classes": {
            "cpu", "memory", "pid", "output", "timeout", "descendant_cleanup",
        },
    }
    if not isinstance(class_matrix, Mapping) or set(class_matrix) != set(expected_class_keys):
        raise OracleError("runner report counterexample class groups mismatch")
    for group, expected_keys in expected_class_keys.items():
        entries = class_matrix.get(group)
        if not isinstance(entries, Mapping) or set(entries) != expected_keys:
            raise OracleError("runner report counterexample class keys mismatch: %s" % group)
        for class_name, entry in entries.items():
            if (
                not isinstance(entry, Mapping)
                or entry.get("passed") is not True
                or entry.get("test_id") not in by_name
                or not isinstance(entry.get("evidence"), Mapping)
                or not entry.get("evidence")
                or by_name[entry["test_id"]].get("passed") is not True
            ):
                raise OracleError(
                    "runner report counterexample class lacks independent evidence: %s"
                    % class_name
                )
    actual_runner_sha = runner_sha
    if report.get("runner_implementation_sha256") != actual_runner_sha:
        raise OracleError("runner report implementation binding mismatch")
    if not re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        str(report.get("run_id", "")),
    ):
        raise OracleError("runner report run_id is missing or malformed")
    try:
        started = datetime.datetime.fromisoformat(str(report["started_at"]))
        completed = datetime.datetime.fromisoformat(str(report["completed_at"]))
    except (KeyError, ValueError) as exc:
        raise OracleError("runner report timestamps are missing or malformed") from exc
    now = datetime.datetime.now(datetime.timezone.utc)
    if (
        started.tzinfo is None
        or completed.tzinfo is None
        or completed < started
        or (completed - started).total_seconds() > 300
        or (now - completed).total_seconds() > 900
        or (completed - now).total_seconds() > 30
    ):
        raise OracleError("runner report is stale, future-dated or implausible")
    measured_executions = sum(isinstance(item.get("result"), Mapping) for item in tests)
    if (
        report.get("sandbox_executions") != measured_executions
        or measured_executions <= 0
        or report.get("healthy_sandbox_execution_count") != 1
    ):
        raise OracleError("runner report does not prove nonzero sandbox execution")
    healthy = by_name["healthy_positive_control"]
    result = healthy.get("result")
    if not isinstance(result, Mapping):
        raise OracleError("healthy positive control lacks a sandbox result")
    fingerprint = result.get("fingerprint")
    cleanup = result.get("cleanup")
    if (
        healthy.get("expected") != "ok"
        or healthy.get("actual") != "ok"
        or result.get("returncode") != 0
        or not isinstance(fingerprint, Mapping)
        or fingerprint.get("distro") != "Ubuntu 24.04.4 LTS"
        or fingerprint.get("kernel") != "6.18.33.2-microsoft-standard-WSL2"
        or fingerprint.get("cgroup") != "v2"
        or not isinstance(cleanup, Mapping)
        or cleanup.get("descendants_gone") is not True
        or cleanup.get("scratch_removed") is not True
    ):
        raise OracleError("healthy positive control is not a measured accepted sandbox run")
    for name, item in by_name.items():
        item_result = item.get("result")
        if isinstance(item_result, Mapping):
            item_cleanup = item_result.get("cleanup")
            if not isinstance(item_cleanup, Mapping) or item_cleanup.get(
                "descendants_gone"
            ) is not True:
                raise OracleError("runner cleanup evidence missing for %s" % name)
    return {
        "healthy_test": healthy,
        "test_names": sorted(by_name),
        "report_sha256": hashlib.sha256(
            json.dumps(report, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "run_id": report["run_id"],
        "candidate_head": candidate_head,
        "sandbox_executions": measured_executions,
        "runner_implementation_sha256": actual_runner_sha,
        "candidate_source_binding": dict(source_binding),
        "counterexample_classes": dict(class_matrix),
        "measured_report": report,
    }


def _engine_metadata() -> dict[str, object]:
    import jsonschema
    package = pathlib.Path(jsonschema.__file__).resolve().parent
    digest = hashlib.sha256()
    files = sorted(path for path in package.rglob("*.py") if path.is_file())
    for path in files:
        digest.update(path.relative_to(package).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
    measured = {
        "name": "python-jsonschema",
        "version": importlib.metadata.version("jsonschema"),
        "digest_sha256": digest.hexdigest(),
        "dialect": DIALECT,
        "implementation_files": len(files),
    }
    if measured != dict(INDEPENDENT_ENGINE_PIN):
        raise OracleError("independent jsonschema engine pin mismatch: %r" % measured)
    return measured


def _differential(schema: Mapping[str, object], document: object) -> tuple[bool, str]:
    import jsonschema
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    diagnostic = "valid" if not errors else "; ".join(
        "%s: %s" % ("/".join(str(x) for x in error.absolute_path), error.message)
        for error in errors[:3]
    )
    return not errors, diagnostic


def _case_matrix(schemas: Mapping[str, Mapping[str, object]], cases: Sequence[Case]):
    matrix = []
    disagreements = []
    expectation_failures = []
    for index, case in enumerate(cases):
        direct_errors = validate(schemas[case.schema_name], case.document)
        direct_valid = not direct_errors
        independent_valid, independent_diagnostic = _differential(
            schemas[case.schema_name], case.document
        )
        if direct_valid != independent_valid:
            disagreements.append(case.case_id)
        if direct_valid != case.expected or independent_valid != case.expected:
            expectation_failures.append(case.case_id)
        matrix.append({
            "schema": case.schema_name,
            "case_id": case.case_id,
            "locator": case.locator,
            "layer": case.layer,
            "held_out": case.held_out,
            "expected": case.expected,
            "order": index,
            "trusted_oracle": {"valid": direct_valid, "rc": 0 if direct_valid else 3, "diagnostic": direct_errors[:3]},
            "independent_engine": {"valid": independent_valid, "rc": 0 if independent_valid else 3, "diagnostic": independent_diagnostic},
        })
    return matrix, disagreements, expectation_failures


def _trusted_hashes() -> dict[str, str]:
    return {
        "answer_key_sha256": sha256_file(HERE / "answer_key.py"),
        "oracle_implementation_sha256": sha256_file(HERE / "oracle.py"),
        "sandbox_implementation_sha256": sha256_file(SANDBOX / "runner.py"),
    }


def evaluate(
    target_root: str,
    *,
    candidate_head: str,
    pin_readback: Mapping[str, object],
    protocol_source: bytes,
    candidate_source_readback: Mapping[str, object],
    artifact_root: str | None = None,
    runner_report: Mapping[str, object] | None,
    seed: int = 8604,
) -> dict[str, object]:
    try:
        protocol_binding = verify_pin_readback(pin_readback, protocol_source)
    except ValueError as exc:
        raise OracleError("pin/source preflight refused evaluation: %s" % exc) from exc
    runner_binding = _validate_runner_report(runner_report, candidate_head, target_root)
    measured_runner_report = runner_binding["measured_report"]
    assert isinstance(measured_runner_report, Mapping)
    runner_tests = measured_runner_report["tests"]
    assert isinstance(runner_tests, list)
    by_name = {
        item["name"]: item
        for item in runner_tests
        if isinstance(item, Mapping) and isinstance(item.get("name"), str)
    }
    schemas, measured_source = _load_schemas(target_root)
    git_source = source_readback(target_root, candidate_head)
    if (
        measured_source.get("schema_bundle_sha256") != git_source.get("schema_bundle_sha256")
        or measured_source.get("schema_file_sha256") != git_source.get("schema_file_sha256")
    ):
        raise OracleError("candidate schema bytes changed during provenance readback")
    _validate_source_readback(git_source, candidate_source_readback, candidate_head)
    if (
        runner_binding["candidate_source_binding"].get("candidate_tree_sha")
        != git_source.get("candidate_tree_sha")
    ):
        raise OracleError("sandbox and oracle candidate tree bindings disagree")
    direct_errors: dict[str, list[str]] = {}
    inventories: dict[str, list[str]] = {}
    all_keywords: set[str] = set()
    for name, schema in schemas.items():
        errors = schema_shape_errors(schema) + check_contract(name, schema)
        direct_errors[name] = errors
        keywords = sorted(inventory(schema))
        inventories[name] = keywords
        all_keywords.update(keywords)
    anchors = keyword_anchors(sorted(all_keywords))
    anchor_missing = sorted(
        key for key, value in anchors.items()
        if not value["valid_passed"] or not value["invalid_failed"]
    )
    cases = build(seed)
    # Candidate schema data must pass the direct local-ref/dialect/shape gate
    # before it reaches any third-party implementation.  This ordering is the
    # network boundary: legacy jsonschema resolvers may fetch a remote $ref.
    direct_gate_failed = any(direct_errors.values()) or bool(anchor_missing)
    if direct_gate_failed:
        matrix, disagreements, expectation_failures = [], [], ["direct_contract_gate_failed"]
    else:
        matrix, disagreements, expectation_failures = _case_matrix(schemas, cases)
    mutation = mutation_score(cases)
    mutation_paths = classification_path_proofs(cases)
    per_schema_counts = {
        name: {
            "total": sum(1 for case in cases if case.schema_name == name),
            "valid": sum(1 for case in cases if case.schema_name == name and case.layer == "valid"),
            "invalid": sum(1 for case in cases if case.schema_name == name and case.layer == "invalid"),
            "semantic_equivalent": sum(1 for case in cases if case.schema_name == name and case.layer == "semantic"),
        }
        for name in EXPECTED_FILES
    }
    engine_metadata = _engine_metadata()
    required_counterexamples = {
        "sandbox_escape_classes": runner_binding["counterexample_classes"]["sandbox_escape_classes"],
        "resource_classes": runner_binding["counterexample_classes"]["resource_classes"],
        "fake_validators": {
            item["stable_id"]: item["classification"] for item in mutation["results"]
        },
        "schema_count": len(schemas),
        "healthy_positive_control_ran": runner_binding["sandbox_executions"] > 0,
        "healthy_sandbox_execution_count": measured_runner_report["healthy_sandbox_execution_count"],
        "keyword_inventory_total": len(all_keywords),
        "corpus_cases_per_schema": per_schema_counts,
        "differential_implementations": 1,
    }
    b1_b6 = {
        "B1_git_commit_tree_blob_binding": git_source["candidate_commit_sha"] == candidate_head,
        "B2_same_fixture_dns_controls": by_name["network_fixture_positive_controls"]["passed"] is True,
        "B3_scratch_materialized_blind_corpus": all(
            item.get("protocol_result_used") is True and item.get("sandbox_executed") is True
            for item in mutation["results"]
        ),
        "B4_fresh_measured_runner_binding": runner_binding["candidate_head"] == candidate_head,
        "B5_nonzero_healthy_sandbox_execution": runner_binding["sandbox_executions"] > 0,
        "B6_five_file_protocol_fakes_killed": mutation["counts"]["killed"] == 5,
    }
    report: dict[str, object] = {
        "ok": False,
        "pins": {
            **PINS,
            "candidate_head": candidate_head,
            "protocol_binding": protocol_binding,
            "candidate_schema_source": git_source,
            **_trusted_hashes(),
        },
        "schema_count": len(schemas),
        "schema_names": sorted(schemas),
        "direct_contract_errors": direct_errors,
        "keyword_inventory": inventories,
        "keyword_inventory_total": len(all_keywords),
        "keyword_anchors": anchors,
        "anchor_missing": anchor_missing,
        "corpus_seed": seed,
        "corpus_counts": per_schema_counts,
        "case_matrix": matrix,
        "differential": {"implementation": engine_metadata, "disagreements": disagreements},
        "expectation_failures": expectation_failures,
        "fake_validators": mutation,
        "mutation_classification_path_proofs": mutation_paths,
        "healthy_positive_control_ran": True,
        "healthy_positive_control_evidence": runner_binding,
        "required_counterexamples": required_counterexamples,
        "B1_B6": b1_b6,
    }
    report["ok"] = (
        len(schemas) == 5
        and not any(direct_errors.values())
        and not anchor_missing
        and not disagreements
        and not expectation_failures
        and mutation["counts"]["killed"] == 5
        and mutation["counts"]["survived"] == 0
        and all(item["passed"] for item in mutation_paths.values())
        and all(b1_b6.values())
    )
    if artifact_root is not None:
        artifact_set = ArtifactSet(artifact_root, "wp86-r5-g5-%s" % candidate_head[:12])
        corpus_payload = [{
            "schema": case.schema_name, "case_id": case.case_id, "locator": case.locator,
            "raw": case.raw, "held_out": case.held_out,
        } for case in cases]
        artifact_set.add("source", "source/pins.json", json.dumps(report["pins"], indent=2, sort_keys=True) + "\n")
        artifact_set.add("corpus", "corpus/objects.json", json.dumps(corpus_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        artifact_set.add("per_case_matrix", "matrix/results.json", json.dumps(matrix, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        artifact_set.add("runner_env_digest", "runner/environment.json", json.dumps({"runner": measured_runner_report, "runner_binding": runner_binding, "differential": engine_metadata}, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        resource_timeout = {
            item["name"]: item.get("result", {}).get("resource_report", {})
            for item in measured_runner_report["tests"]
            if item.get("name") in {
                "memory_hog", "cpu_busy_loop", "pid_fork_bomb",
                "stdout_flood", "timeout_and_descendant_cleanup",
            }
        }
        artifact_set.add("runner_env_digest", "runner/resource-timeout.json", json.dumps(resource_timeout, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        cleanup_evidence = {
            item["name"]: item.get("result", {}).get("cleanup", {})
            for item in measured_runner_report["tests"]
            if isinstance(item, Mapping)
        }
        artifact_set.add("cleanup_record", "cleanup/record.json", json.dumps({"oracle_candidate_code_executed": False, "candidate_treated_as_json_data": True, "sandbox_cleanup": cleanup_evidence}, indent=2, sort_keys=True) + "\n")
        artifact_set.finalize()
        sealed = verify(artifact_root)
        report["artifact_manifest"] = sealed
        report["artifact_root"] = os.path.abspath(artifact_root)
        report["ok"] = bool(report["ok"] and sealed["ok"])
    return report
