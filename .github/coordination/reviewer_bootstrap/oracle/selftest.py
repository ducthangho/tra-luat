"""Executable counterexamples for the trusted RA-02 successor oracle."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import pathlib
import re
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

    class _Independent:
        """Người chấm thứ hai; oracle thật dùng `python-jsonschema` ở vị trí này."""

        def validate(self, node, instance):
            return not engine.validate(node, instance)

        def check_schema(self, node):
            return not engine.schema_shape_errors(node)

    controls = engine.keyword_controls(inventory, independent=_Independent())
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
    # Khẳng định DƯƠNG, không phải "khác fixture_gap": một ca chỉ kiểm `!=` vẫn
    # xanh khi nó chẳng đo gì (vd `anchor_missing` với `real_rc: None`).
    if record["disposition"] != "masked":
        raise AssertionError(record)
    if record["real_rc"] != 19:
        raise AssertionError("stderr forger did not exercise the fixture's real exit code: %r" % record)
    if not record.get("affected_case_ids"):
        raise AssertionError("masked verdict carries no affected case evidence: %r" % record)


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


def _module(name: str):
    sys.path.insert(0, str(HERE.parent))
    try:
        module = __import__("oracle.%s" % name, fromlist=[name])
    finally:
        sys.path.pop(0)
    return module


def _sealed_json(path: pathlib.Path, value: object) -> pathlib.Path:
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    path.chmod(0o444)
    return path


def durable_facts_reject_empty_authority_blocks() -> None:
    """Phản chứng chính xác của R3: hai khối RỖNG từng đi qua sạch."""
    oracle = _module("oracle")
    floor = {
        "mission_issue": 76,
        "mission_revision_min": 6,
        "packet_issue": 99,
        "packet_revision_min": 3,
        "packet_generation_min": 3,
    }
    with tempfile.TemporaryDirectory(prefix="ra02-r3-") as tmp:
        facts = _sealed_json(
            pathlib.Path(tmp) / "durable-facts.json",
            {"schema_version": 1, "mission": {}, "packet": {}},
        )
        try:
            oracle._read_durable_facts(facts, floor)
        except oracle.OracleError as exc:
            if "mission" not in str(exc) or "missing" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("an authority bundle naming no authority at all was accepted")


def durable_facts_reject_authority_below_dispatcher_floor() -> None:
    """Sàn hiện hành đến từ pin Dispatcher, và hai vế nằm ở HAI tệp ngoài khác nhau."""
    oracle = _module("oracle")
    with tempfile.TemporaryDirectory(prefix="ra02-floor-") as tmp:
        root = pathlib.Path(tmp)
        floor_path = _sealed_json(
            root / "dispatcher-authority-floor.json",
            {
                "mission_issue": 76,
                "mission_revision_min": 6,
                "packet_issue": 99,
                "packet_revision_min": 3,
                "packet_generation_min": 3,
            },
        )
        floor = json.loads(floor_path.read_text(encoding="utf-8"))
        stale = _sealed_json(
            root / "stale-facts.json",
            {
                "schema_version": 1,
                "mission": {"issue": 76, "revision": 4, "plan_hash": "a" * 64},
                "packet": {"issue": 99, "revision": 2, "generation": 2, "spec_hash": "b" * 64},
            },
        )
        try:
            oracle._read_durable_facts(stale, floor)
        except oracle.OracleError as exc:
            for needle in ("stale", "mission.revision", "packet.revision", "packet.generation"):
                if needle not in str(exc):
                    raise AssertionError("%r absent from %s" % (needle, exc)) from exc
        else:
            raise AssertionError("authority below the Dispatcher floor was accepted")

        fenced = _sealed_json(
            root / "fenced-facts.json",
            {
                "schema_version": 1,
                "mission": {"issue": 76, "revision": 6, "plan_hash": "a" * 64},
                "packet": {"issue": 86, "revision": 6, "generation": 6, "spec_hash": "b" * 64},
            },
        )
        try:
            oracle._read_durable_facts(fenced, floor)
        except oracle.OracleError as exc:
            if "packet.issue names a fenced authority" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a bundle naming the cancelled predecessor Packet was accepted")

        current = _sealed_json(
            root / "current-facts.json",
            {
                "schema_version": 1,
                "mission": {"issue": 76, "revision": 6, "plan_hash": "a" * 64},
                "packet": {"issue": 99, "revision": 3, "generation": 3, "spec_hash": "b" * 64},
            },
        )
        accepted = oracle._read_durable_facts(current, floor)
        if accepted["mission"]["revision"] != 6 or accepted["packet"]["generation"] != 3:
            raise AssertionError(accepted)


def sandbox_report_missing_repeat_fields_is_structured_red() -> None:
    """R4: thiếu `repeat_requested` từng ném `TypeError` trần, rc=1, stdout rỗng."""
    oracle = _module("oracle")
    with tempfile.TemporaryDirectory(prefix="ra02-r4-") as tmp:
        root = pathlib.Path(tmp)
        missing = _sealed_json(root / "no-repeat.json", {"schema_version": 1, "ok": True})
        try:
            oracle._runner_observation(missing, "a" * 40, "b" * 64)
        except oracle.OracleError as exc:
            if "repeat_requested" not in str(exc) or "missing" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a sandbox report without repeat accounting was accepted")

        mistyped = _sealed_json(
            root / "string-repeat.json",
            {"schema_version": 1, "ok": True, "repeat_requested": "8", "repeat_executed": 8},
        )
        try:
            oracle._runner_observation(mistyped, "a" * 40, "b" * 64)
        except oracle.OracleError as exc:
            if "repeat_requested" not in str(exc) or "must be int" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a mistyped repeat count was accepted")


def keyword_controls_require_independent_engine_agreement() -> None:
    """R7: hai răng từng do CHÍNH bộ máy bị chấm tự chấm."""
    engine = _module("engine")

    class _Agreeing:
        def validate(self, schema, instance):
            return not engine.validate(schema, instance)

        def check_schema(self, schema):
            return not engine.schema_shape_errors(schema)

    class _Disagreeing(_Agreeing):
        def validate(self, schema, instance):
            return not super().validate(schema, instance)

    absent = engine.keyword_controls(["type"], independent=None)["type"]
    if absent["positive_passed"] is not False or absent["negative_mode"] != "INDEPENDENT_ENGINE_MISSING":
        raise AssertionError(absent)

    agreed = engine.keyword_controls(["type", "title"], independent=_Agreeing())
    for keyword in ("type", "title"):
        record = agreed[keyword]
        if record["positive_passed"] is not True or record["negative_failed"] is not True:
            raise AssertionError({keyword: record})
        if record["engine_agreement"] is not True:
            raise AssertionError({keyword: record})

    split = engine.keyword_controls(["type"], independent=_Disagreeing())["type"]
    if split["engine_agreement"] is not False or split["positive_passed"] is not False:
        raise AssertionError(split)


def pinned_corpus_is_in_tree_and_anchors_are_well_formed() -> None:
    """R1: corpus không còn là tệp chỉ tồn tại trên máy Executor."""
    corpus_module = _module("corpus")
    inventory = _module("trusted_inventory")
    pinned = HERE.parents[3] / pathlib.PurePosixPath(inventory.PINNED_CORPUS_PATH)
    if inventory.PINNED_CORPUS_PATH not in inventory.TRUSTED_SOURCE_PATHS:
        raise AssertionError("the pinned corpus is not covered by the trusted source inventory")
    raw = corpus_module.read_bytes(pinned, require_readonly=False)
    loaded = corpus_module.load(
        pinned,
        hashlib.sha256(raw).hexdigest(),
        inventory.PROTOCOL_SCHEMA_PATHS,
        require_readonly=False,
    )
    by_case = {case.case_id: case for case in loaded.cases}
    if len(loaded.case_id_registry) != len(loaded.cases) or len(set(loaded.case_id_registry)) != len(loaded.cases):
        raise AssertionError("case registry is not a duplicate-free cover of the corpus")
    if not re.fullmatch(r"[0-9a-f]{64}", loaded.target_schema_inventory_sha256):
        raise AssertionError(loaded.target_schema_inventory_sha256)
    for keyword, record in loaded.anchors.items():
        valid = by_case[record["valid_case_id"]]
        invalid = by_case[record["invalid_case_id"]]
        if valid.expected_valid is not True or invalid.expected_valid is not False:
            raise AssertionError("anchor %s is not one valid and one invalid case" % keyword)
        if valid.schema_path != invalid.schema_path:
            raise AssertionError("anchor %s crosses schema boundaries" % keyword)
    schemas_with_anchors = {by_case[record["valid_case_id"]].schema_path for record in loaded.anchors.values()}
    if not schemas_with_anchors:
        raise AssertionError("corpus declares no keyword anchors")


def hardened_reader_parity_between_bootstrap_and_shared_module() -> None:
    """S6: bản sao cố ý trong bootstrap phải được ĐO, không phải được hứa."""
    source_pin = _source_pin_module()
    safe_io = _module("safe_io")

    class _ParityError(RuntimeError):
        pass

    def shared(path: pathlib.Path, label: str) -> bytes:
        return safe_io.read_regular_single_link(path, label, _ParityError)

    def bootstrap(path: pathlib.Path, label: str) -> bytes:
        return source_pin._read_regular_single_link(path, label)

    def outcome(reader, path: pathlib.Path) -> tuple[str, object]:
        try:
            return ("bytes", reader(path, "parity fixture"))
        except Exception as exc:  # noqa: BLE001
            return ("error", str(exc))

    with tempfile.TemporaryDirectory(prefix="ra02-parity-") as tmp:
        root = pathlib.Path(tmp)
        regular = root / "regular.bin"
        regular.write_bytes(b"parity-bytes\n")
        link = root / "link.bin"
        link.symlink_to(regular)
        hardlinked = root / "hardlinked.bin"
        hardlinked.write_bytes(b"parity-bytes\n")
        second = root / "second-name.bin"
        os.link(hardlinked, second)
        absent = root / "absent.bin"

        divergent = []
        for name, path in (
            ("regular", regular),
            ("symlink", link),
            ("multi_hardlink", hardlinked),
            ("absent", absent),
        ):
            left = outcome(shared, path)
            right = outcome(bootstrap, path)
            if left != right:
                divergent.append({"fixture": name, "shared": left, "bootstrap": right})
        if divergent:
            raise AssertionError("hardened reader implementations diverged: %r" % divergent)
        if outcome(shared, regular)[0] != "bytes" or outcome(shared, link)[0] != "error":
            raise AssertionError("parity matrix did not exercise both a pass and a refusal")


def main() -> int:
    tests = (
        source_pin_rejects_fabricated_repository,
        source_pin_rejects_git_blob_byte_mismatch,
        source_pin_rejects_symlink_mismatch,
        fake_lowercase_commit_cannot_emit_oracle_artifact,
        authority_bundle_rejects_stale_pins,
        durable_facts_reject_empty_authority_blocks,
        durable_facts_reject_authority_below_dispatcher_floor,
        sandbox_report_missing_repeat_fields_is_structured_red,
        keyword_controls_require_independent_engine_agreement,
        pinned_corpus_is_in_tree_and_anchors_are_well_formed,
        hardened_reader_parity_between_bootstrap_and_shared_module,
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
