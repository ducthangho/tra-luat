"""Executable counterexamples for the trusted RA-02 successor oracle."""

from __future__ import annotations

import contextlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterator

HERE = pathlib.Path(__file__).resolve().parent
SOURCE_PIN = HERE / "source_pin.py"


@contextlib.contextmanager
def _trusted_temp_repository() -> Iterator[tuple[pathlib.Path, str, tuple[str, ...]]]:
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle.trusted_inventory import TRUSTED_SOURCE_PATHS
    finally:
        sys.path.pop(0)
    checkout = HERE.parents[3]
    with tempfile.TemporaryDirectory(prefix="ra02-source-pin-") as tmp:
        root = pathlib.Path(tmp)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for relative in TRUSTED_SOURCE_PATHS:
            destination = root / pathlib.PurePosixPath(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(checkout / pathlib.PurePosixPath(relative), destination)
        subprocess.run(
            ["git", "-C", str(root), "add", "--", *TRUSTED_SOURCE_PATHS], check=True
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                "user.name=ra02",
                "-c",
                "user.email=ra02@example.invalid",
                "commit",
                "-qm",
                "trusted-source-fixture",
            ],
            check=True,
        )
        head = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
        yield root, head, TRUSTED_SOURCE_PATHS


def _source_pin_module():
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle import source_pin
    finally:
        sys.path.pop(0)
    return source_pin


def _write_source_pin(
    path: pathlib.Path, binding: dict[str, object], source_paths: tuple[str, ...]
) -> None:
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "candidate": {
                    "head": binding["candidate_head"],
                    "tree": binding["candidate_tree"],
                },
                "trusted_source_paths": list(source_paths),
                "trusted_source_inventory_sha256": binding[
                    "trusted_source_inventory_sha256"
                ],
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    path.chmod(0o444)


def source_pin_rejects_git_blob_byte_mismatch() -> None:
    source_pin = _source_pin_module()
    with _trusted_temp_repository() as (root, head, source_paths):
        relative = source_paths[1]
        changed = root / pathlib.PurePosixPath(relative)
        changed.write_bytes(changed.read_bytes() + b"\n# uncommitted byte mismatch\n")
        try:
            source_pin.measure(str(root), head, source_paths)
        except source_pin.SourcePinError as exc:
            if "bytes differ from the declared Git blob" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("trusted source byte mismatch was accepted")


def source_pin_rejects_symlink_mismatch() -> None:
    source_pin = _source_pin_module()
    with _trusted_temp_repository() as (root, head, source_paths):
        relative = source_paths[1]
        changed = root / pathlib.PurePosixPath(relative)
        target = root / "outside-trusted-source.py"
        target.write_bytes(changed.read_bytes())
        changed.unlink()
        changed.symlink_to(target)
        try:
            source_pin.measure(str(root), head, source_paths)
        except source_pin.SourcePinError as exc:
            if "regular non-symlink file" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("trusted source symlink mismatch was accepted")


def fake_lowercase_commit_cannot_emit_oracle_artifact() -> None:
    source_pin = _source_pin_module()
    with _trusted_temp_repository() as (root, head, source_paths):
        binding = source_pin.measure(str(root), head, source_paths)
        pin = root / "dispatcher-source-pin.json"
        _write_source_pin(pin, binding, source_paths)
        artifact_root = root / "false-oracle-artifact"
        fake_head = "f" * 40 if head != "f" * 40 else "e" * 40
        proc = subprocess.run(
            [
                sys.executable,
                str(SOURCE_PIN),
                "run-oracle",
                "--repo-root",
                str(root),
                "--candidate-head",
                fake_head,
                "--pin",
                str(pin),
                "--durable-facts",
                str(root / "not-read-durable-facts.json"),
                "--target-root",
                str(root),
                "--corpus",
                str(root / "not-read-corpus.json"),
                "--sandbox-report",
                str(root / "not-read-sandbox.json"),
                "--output-root",
                str(artifact_root),
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 2 or "SourcePinError" not in proc.stdout:
            raise AssertionError(
                "fake lowercase commit was not rejected by the bootstrap: rc=%d stdout=%r stderr=%r"
                % (proc.returncode, proc.stdout, proc.stderr)
            )
        if artifact_root.exists():
            raise AssertionError("fake lowercase commit emitted an oracle artifact")


def authority_bundle_rejects_stale_pins() -> None:
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle import authority
    finally:
        sys.path.pop(0)
    observations = {
        "protocol": {
            "commit_sha": "a" * 40,
            "path": "docs/example-protocol.md",
            "file_git_oid": "b" * 40,
            "file_sha256": "c" * 64,
        },
        "mission": {"issue": 301, "revision": 12, "plan_hash": "d" * 64},
        "packet": {
            "issue": 302,
            "revision": 9,
            "generation": 4,
            "spec_hash": "e" * 64,
        },
        "candidate": {"head": "f" * 40, "tree": "1" * 40},
        "trusted_source_paths": ["example/source.py"],
        "trusted_source_inventory_sha256": "2" * 64,
        "target_checkout": {"head": "3" * 40, "tree": "4" * 40},
        "target_schema_paths": ["example/schema.json"],
        "target_schema_inventory_sha256": "5" * 64,
        "corpus_sha256": "6" * 64,
        "runner_fingerprint_sha256": "7" * 64,
    }
    sealed_stale = {
        "schema_version": 1,
        "protocol": {
            "commit_sha": "a" * 40,
            "path": "docs/example-protocol.md",
            "file_git_oid": "b" * 40,
            "file_sha256": "c" * 64,
        },
        "mission": {"issue": 301, "revision": 11, "plan_hash": "d" * 64},
        "packet": {
            "issue": 302,
            "revision": 8,
            "generation": 3,
            "spec_hash": "e" * 64,
        },
        "candidate": {"head": "f" * 40, "tree": "1" * 40},
        "trusted_source_paths": ["example/source.py"],
        "trusted_source_inventory_sha256": "2" * 64,
        "target_checkout": {"head": "3" * 40, "tree": "4" * 40},
        "target_schema_paths": ["example/schema.json"],
        "target_schema_inventory_sha256": "5" * 64,
        "corpus_sha256": "6" * 64,
        "runner_fingerprint_sha256": "7" * 64,
    }
    with tempfile.TemporaryDirectory(prefix="ra02-b2-") as tmp:
        bundle = pathlib.Path(tmp) / "authority.json"
        bundle.write_text(json.dumps(sealed_stale, sort_keys=True) + "\n", encoding="utf-8")
        bundle.chmod(0o444)
        try:
            authority.load_and_verify(bundle, observations)
        except authority.AuthorityError as exc:
            if "mission.revision" not in str(exc) or "packet.revision" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("stale fenced authority bundle was accepted")


def every_inventoried_keyword_has_positive_and_negative_teeth() -> None:
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle import engine
    finally:
        sys.path.pop(0)
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "name": {"type": "string", "pattern": "^ok$", "minLength": 2},
            "values": {"type": "array", "items": {"type": "integer"}, "uniqueItems": True},
        },
        "required": ["name"],
        "additionalProperties": False,
    }
    inventory = engine.keyword_inventory(schema)
    controls = engine.keyword_controls(inventory)
    missing = sorted(keyword for keyword in inventory if keyword not in controls)
    failed = sorted(
        keyword
        for keyword, record in controls.items()
        if record.get("positive_passed") is not True or record.get("negative_failed") is not True
    )
    if missing or failed:
        raise AssertionError("missing=%s failed=%s" % (missing, failed))


def schema_shape_rejects_remote_or_unresolved_refs() -> None:
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle import engine
    finally:
        sys.path.pop(0)
    for ref in ("https://fixture.invalid/schema.json", "#/$defs/missing"):
        errors = engine.schema_shape_errors({"$ref": ref, "$defs": {}})
        if not any("$ref rejected" in error for error in errors):
            raise AssertionError("unsafe ref was not rejected: %s errors=%r" % (ref, errors))


def validator_stderr_cannot_forge_fixture_gap() -> None:
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle import fake_validators
    finally:
        sys.path.pop(0)
    cases = [
        {"case_id": "0" * 16, "document": {"x": 1}, "expected_valid": True},
        {"case_id": "1" * 16, "document": {}, "expected_valid": False},
    ]
    record = fake_validators.run_one("stderr_forger_control", cases, timeout_seconds=3)
    if record["disposition"] == "fixture_gap":
        raise AssertionError(record)
    if record["real_rc"] == 0:
        raise AssertionError("stderr forger did not exercise a real failing process")


def all_five_fake_validators_are_killed_by_blind_case_evidence() -> None:
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle import fake_validators
        from oracle.trusted_inventory import FAKE_VALIDATOR_IDS
    finally:
        sys.path.pop(0)
    cases = [
        {"case_id": "0" * 16, "document": {"x": 1}, "expected_valid": True},
        {"case_id": "1" * 16, "document": {}, "expected_valid": False},
        {"case_id": "2" * 16, "document": {"x": 2}, "expected_valid": True},
        {"case_id": "3" * 16, "document": {"x": None}, "expected_valid": False},
    ]
    matrix = fake_validators.mutation_matrix(cases)
    if matrix["fake_validator_ids"] != list(FAKE_VALIDATOR_IDS):
        raise AssertionError(matrix)
    if matrix["killed"] != matrix["total"] or matrix["total"] != 5 or matrix["ok"] is not True:
        raise AssertionError(matrix)
    if any(record.get("real_rc") != 0 for record in matrix["records"]):
        raise AssertionError("mutation verdict did not retain each real process rc: %r" % matrix)
    expected_ids = sorted(case["case_id"] for case in cases)
    for record in matrix["records"]:
        affected = record.get("affected_case_ids")
        if not isinstance(affected, list) or not affected:
            raise AssertionError("killed fake lacks exact affected case evidence: %r" % record)
        if any(case_id not in expected_ids for case_id in affected):
            raise AssertionError("fake named a case outside the blind corpus: %r" % record)


def source_pin_rejects_fabricated_repository() -> None:
    source_pin = _source_pin_module()
    with _trusted_temp_repository() as (root, trusted_head, source_paths):
        binding = source_pin.measure(str(root), trusted_head, source_paths)
        pin = root / "dispatcher-pin.json"
        _write_source_pin(pin, binding, source_paths)
        fabricated = root / ".github/coordination/reviewer_bootstrap/sandbox/selftest.py"
        fabricated.write_text("print('11/11')\n", encoding="utf-8")
        relative = fabricated.relative_to(root).as_posix()
        subprocess.run(["git", "-C", str(root), "add", "--", relative], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                "user.name=ra02",
                "-c",
                "user.email=ra02@example.invalid",
                "commit",
                "-qm",
                "fabricated-always-green-selftest",
            ],
            check=True,
        )
        fabricated_head = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
        output = root / "forged-sandbox.json"
        proc = subprocess.run(
            [
                sys.executable,
                str(SOURCE_PIN),
                "run-sandbox",
                "--repo-root",
                str(root),
                "--candidate-head",
                fabricated_head,
                "--pin",
                str(pin),
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 2 or "SourcePinError" not in proc.stdout:
            raise AssertionError(proc.stdout + proc.stderr)
        if output.exists() or "11/11" in proc.stdout:
            raise AssertionError("candidate-authored always-green selftest emitted evidence")


def main() -> int:
    tests = (
        source_pin_rejects_fabricated_repository,
        source_pin_rejects_git_blob_byte_mismatch,
        source_pin_rejects_symlink_mismatch,
        fake_lowercase_commit_cannot_emit_oracle_artifact,
        authority_bundle_rejects_stale_pins,
        every_inventoried_keyword_has_positive_and_negative_teeth,
        schema_shape_rejects_remote_or_unresolved_refs,
        validator_stderr_cannot_forge_fixture_gap,
        all_five_fake_validators_are_killed_by_blind_case_evidence,
    )
    passed = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            print("[FAIL] %s -- %s: %s" % (test.__name__, type(exc).__name__, exc))
        else:
            passed += 1
            print("[OK] %s" % test.__name__)
    print("== ra02 oracle selftest %d/%d ==" % (passed, len(tests)))
    return 0 if passed == len(tests) and len(tests) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
