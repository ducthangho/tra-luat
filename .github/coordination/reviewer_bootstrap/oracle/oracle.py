"""Direct, differential and behavioural oracle for five protocol schemas."""

from __future__ import annotations

import dataclasses
import hashlib
import importlib.metadata
import json
import os
import pathlib
import random
import shutil
import sys
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
CORE = HERE.parent / "core"
SANDBOX = HERE.parent / "sandbox"
sys.path.insert(0, str(CORE))
from artifacts import ArtifactSet, sha256_file, verify  # noqa: E402

from answer_key import DIALECT, EXPECTED_FILES, PINS, check_contract  # noqa: E402
from corpus import Case, build  # noqa: E402
from engine import inventory, keyword_anchors, schema_shape_errors, validate  # noqa: E402


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


def _load_schemas(target_root: str) -> dict[str, Mapping[str, object]]:
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
    for name in EXPECTED_FILES:
        path = schema_dir / name
        if path.is_symlink() or not path.is_file():
            raise OracleError("schema is not a regular non-symlink file: %s" % name)
        if path.stat().st_size > 1024 * 1024:
            raise OracleError("schema exceeds 1 MiB limit: %s" % name)
        value = _json_no_duplicates(path.read_text(encoding="utf-8"), name)
        if not isinstance(value, dict):
            raise OracleError("schema root is not an object: %s" % name)
        result[name] = value
    return result


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


def _mutation_score(cases: Sequence[Case]) -> dict[str, object]:
    base_hashes = {
        hashlib.sha256(case.raw.encode("utf-8")).hexdigest()
        for case in cases if case.layer == "valid" and not case.held_out
    }
    def decision(fake_id: str, case: Case, index: int) -> bool:
        if fake_id == "always_pass": return True
        if fake_id == "always_fail": return False
        if fake_id == "exact_hash_only": return hashlib.sha256(case.raw.encode("utf-8")).hexdigest() in base_hashes
        if fake_id == "stdout_forger": return not case.expected
        if fake_id == "path_aware_detector": return int(case.case_id[-1], 16) % 2 == 0
        raise AssertionError(fake_id)
    results = []
    for fake_id in ("always_pass", "always_fail", "exact_hash_only", "stdout_forger", "path_aware_detector"):
        killers = [case.case_id for index, case in enumerate(cases) if decision(fake_id, case, index) != case.expected]
        classification = "killed" if killers else "survived"
        results.append({
            "stable_id": fake_id,
            "classification": classification,
            "killing_case_ids": killers[:5],
            "claimed_stdout": "ALL CASES PASS" if fake_id == "stdout_forger" else None,
            "protocol_result_used": True,
        })
    counts = {name: sum(1 for item in results if item["classification"] == name) for name in ("killed", "survived", "masked", "fixture_gap", "anchor_missing")}
    return {"results": results, "counts": counts, "score": "%d/%d" % (counts["killed"], len(results))}


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
    artifact_root: str | None = None,
    runner_report: Mapping[str, object] | None = None,
    seed: int = 8604,
) -> dict[str, object]:
    schemas = _load_schemas(target_root)
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
    mutation = _mutation_score(cases)
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
        "pins": {**PINS, "candidate_head": candidate_head, **_trusted_hashes()},
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
        "healthy_positive_control_ran": any(case.expected and case.layer == "valid" for case in cases),
    }
    report["ok"] = (
        len(schemas) == 5
        and not any(direct_errors.values())
        and not anchor_missing
        and not disagreements
        and not expectation_failures
        and mutation["counts"]["killed"] == 5
        and mutation["counts"]["survived"] == 0
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
        artifact_set.add("runner_env_digest", "runner/environment.json", json.dumps({"runner": runner_report or {}, "differential": engine_metadata}, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        artifact_set.add("cleanup_record", "cleanup/record.json", json.dumps({"oracle_candidate_code_executed": False, "candidate_treated_as_json_data": True, "sandbox_cleanup": (runner_report or {}).get("cleanup", {}) if isinstance(runner_report, Mapping) else {}}, indent=2, sort_keys=True) + "\n")
        artifact_set.finalize()
        sealed = verify(artifact_root)
        report["artifact_manifest"] = sealed
        report["artifact_root"] = os.path.abspath(artifact_root)
        report["ok"] = bool(report["ok"] and sealed["ok"])
    return report
