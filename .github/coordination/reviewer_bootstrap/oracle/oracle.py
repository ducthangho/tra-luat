"""Direct, differential and behavioural oracle for five protocol schemas."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import pathlib
import stat
import sys
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
CORE = HERE.parent / "core"
SANDBOX = HERE.parent / "sandbox"
sys.path.insert(0, str(CORE))
from artifacts import ArtifactSet, sha256_file, verify  # noqa: E402

from answer_key import (  # noqa: E402
    DIALECT,
    EXPECTED_FILES,
    PINS,
    check_contract,
    verify_pin_readback,
)
from corpus import Case, build  # noqa: E402
from engine import inventory, keyword_anchors, schema_shape_errors, validate  # noqa: E402
from fake_validators import (  # noqa: E402
    classification_path_proofs,
    mutation_score,
)


class OracleError(RuntimeError):
    pass


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


def source_readback(target_root: str, candidate_head: str) -> dict[str, object]:
    """Measure exact candidate schema bytes for a trusted dispatcher readback."""
    if not isinstance(candidate_head, str) or not __import__("re").fullmatch(
        r"[0-9a-f]{40}", candidate_head
    ):
        raise OracleError("candidate_head must be an exact 40-hex Git oid")
    _, measured = _load_schemas(target_root)
    return {"candidate_head": candidate_head, **measured}


def _validate_source_readback(
    measured: Mapping[str, object],
    readback: Mapping[str, object],
    candidate_head: str,
) -> None:
    expected = {"candidate_head": candidate_head, **measured}
    if dict(readback) != expected:
        raise OracleError("candidate schema source readback mismatch")


def _validate_runner_report(report: Mapping[str, object] | None) -> dict[str, object]:
    if not isinstance(report, Mapping):
        raise OracleError("measured runner report is required; no default evidence exists")
    tests = report.get("tests")
    if (
        report.get("ok") is not True
        or not isinstance(tests, list)
        or not tests
        or report.get("passed") != report.get("total")
        or report.get("total") != len(tests)
    ):
        raise OracleError("runner report did not pass a non-empty measured suite")
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
    }
    missing = sorted(required - set(by_name))
    if missing:
        raise OracleError("runner report missing measured controls: %s" % missing)
    if any(item.get("passed") is not True for item in by_name.values()):
        raise OracleError("runner report contains a failed/fixture-gap control")
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
    }


def _engine_metadata() -> dict[str, object]:
    import jsonschema
    package = pathlib.Path(jsonschema.__file__).resolve().parent
    digest = hashlib.sha256()
    files = sorted(path for path in package.rglob("*.py") if path.is_file())
    for path in files:
        digest.update(path.relative_to(package).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
    return {
        "name": "python-jsonschema",
        "version": importlib.metadata.version("jsonschema"),
        "digest_sha256": digest.hexdigest(),
        "dialect": DIALECT,
        "implementation_files": len(files),
    }


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
    runner_binding = _validate_runner_report(runner_report)
    schemas, measured_source = _load_schemas(target_root)
    _validate_source_readback(measured_source, candidate_source_readback, candidate_head)
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
    report: dict[str, object] = {
        "ok": False,
        "pins": {
            **PINS,
            "candidate_head": candidate_head,
            "protocol_binding": protocol_binding,
            "candidate_schema_source": measured_source,
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
    )
    if artifact_root is not None:
        artifact_set = ArtifactSet(artifact_root, "wp86-r4-g4-%s" % candidate_head[:12])
        corpus_payload = [{
            "schema": case.schema_name, "case_id": case.case_id, "locator": case.locator,
            "raw": case.raw, "held_out": case.held_out,
        } for case in cases]
        artifact_set.add("source", "source/pins.json", json.dumps(report["pins"], indent=2, sort_keys=True) + "\n")
        artifact_set.add("corpus", "corpus/objects.json", json.dumps(corpus_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        artifact_set.add("per_case_matrix", "matrix/results.json", json.dumps(matrix, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        artifact_set.add("runner_env_digest", "runner/environment.json", json.dumps({"runner": runner_report, "runner_binding": runner_binding, "differential": engine_metadata}, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        resource_timeout = {
            item["name"]: item.get("result", {}).get("resource_report", {})
            for item in runner_report["tests"]
            if item.get("name") in {
                "memory_hog", "cpu_busy_loop", "pid_fork_bomb",
                "stdout_flood", "timeout_and_descendant_cleanup",
            }
        }
        artifact_set.add("runner_env_digest", "runner/resource-timeout.json", json.dumps(resource_timeout, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        cleanup_evidence = {
            item["name"]: item.get("result", {}).get("cleanup", {})
            for item in runner_report["tests"]
            if isinstance(item, Mapping)
        }
        artifact_set.add("cleanup_record", "cleanup/record.json", json.dumps({"oracle_candidate_code_executed": False, "candidate_treated_as_json_data": True, "sandbox_cleanup": cleanup_evidence}, indent=2, sort_keys=True) + "\n")
        artifact_set.finalize()
        sealed = verify(artifact_root)
        report["artifact_manifest"] = sealed
        report["artifact_root"] = os.path.abspath(artifact_root)
        report["ok"] = bool(report["ok"] and sealed["ok"])
    return report
