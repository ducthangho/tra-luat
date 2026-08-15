"""Executable counterexamples for the trusted RA-02 successor oracle.

Không một hằng Mission / Packet / generation nào được viết trong tệp này (§4.2).
Các ca kiểm thẩm quyền đọc pin hiện hành từ MỘT FIXTURE NGOÀI do Dispatcher soạn
từ raw durable facts (§4.3) rồi DẪN XUẤT các biến thể stale / fenced / trên sàn
từ chính giá trị ngoài đó.  Thiếu fixture là `not_run` có lý do kèm cổng ĐỎ, chứ
không phải một ca tự chấm bằng hằng của chính mình (WP99-R3G3-SPEC-001).
"""

from __future__ import annotations

import argparse
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
CANDIDATE_ROOT = HERE.parents[3]

# Đường dẫn fixture do `main` đặt từ dòng lệnh; `None` nghĩa là chỉ còn biến môi
# trường để hỏi.  Đây là ĐỊA CHỈ, không phải thẩm quyền: nội dung vẫn phải niêm
# phong read-only và nằm ngoài checkout ứng viên.
_AUTHORITY_FIXTURE_PATH: str | None = None


class FixtureUnavailable(RuntimeError):
    """Ca kiểm cần một đầu vào ngoài do Dispatcher cấp, và nó không có ở đây."""


def _authority_fixture():
    module = _module("authority_fixture")
    located = module.locate(_AUTHORITY_FIXTURE_PATH)
    if not located:
        raise FixtureUnavailable(
            "no Dispatcher authority fixture: pass --authority-fixture PATH or set %s; "
            "§4.3 forbids this selftest from supplying its own expected Mission/Packet pins"
            % module.FIXTURE_PATH_ENV
        )
    return module.load(located, CANDIDATE_ROOT)


@contextlib.contextmanager
def _trusted_temp_repository() -> Iterator[tuple[pathlib.Path, str, tuple[str, ...]]]:
    sys.path.insert(0, str(HERE.parent))
    try:
        from oracle.trusted_inventory import TRUSTED_SOURCE_PATHS
    finally:
        sys.path.pop(0)
    checkout = CANDIDATE_ROOT
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
    """Phản chứng chính xác của R3: hai khối RỖNG từng đi qua sạch.

    Sàn đến từ fixture ngoài, không từ hằng của ứng viên — bản trước dựng cả sàn
    lẫn ba bộ facts bằng cùng một nhúm hằng viết tay (SPEC-001).
    """
    oracle = _module("oracle")
    fixture = _authority_fixture()
    with tempfile.TemporaryDirectory(prefix="ra02-r3-") as tmp:
        facts = _sealed_json(pathlib.Path(tmp) / "durable-facts.json", fixture.empty_blocks())
        try:
            oracle._read_durable_facts(facts, dict(fixture.floor))
        except oracle.OracleError as exc:
            if "mission" not in str(exc) or "missing" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("an authority bundle naming no authority at all was accepted")


def durable_facts_reject_authority_below_dispatcher_floor() -> None:
    """Ngữ nghĩa tươi/sàn, đo trên giá trị NGOÀI — không một số hiệu nào ở đây.

    Ca này nói bốn điều và không điều nào phụ thuộc vào một Mission/Packet cụ
    thể: dưới sàn thì chết theo tên trường; Packet đã rào thì chết; Mission lạ
    thì chết; đúng sàn, trên sàn và CHÍNH pin hiện hành của fixture thì phải
    được nhận.  Vế cuối là răng chống trôi: khi durable authority tiến lên,
    Dispatcher sinh lại fixture và ca này nói về thẩm quyền MỚI, chứ không xanh
    mãi với hằng lỗi thời của chính nó.
    """
    oracle = _module("oracle")
    fixture = _authority_fixture()
    floor = dict(fixture.floor)
    with tempfile.TemporaryDirectory(prefix="ra02-floor-") as tmp:
        root = pathlib.Path(tmp)
        stale = _sealed_json(root / "stale-facts.json", fixture.below_floor_facts())
        try:
            oracle._read_durable_facts(stale, floor)
        except oracle.OracleError as exc:
            for needle in ("stale", "mission.revision", "packet.revision", "packet.generation"):
                if needle not in str(exc):
                    raise AssertionError("%r absent from %s" % (needle, exc)) from exc
        else:
            raise AssertionError("authority below the Dispatcher floor was accepted")

        fenced = _sealed_json(root / "fenced-facts.json", fixture.fenced_packet_facts())
        try:
            oracle._read_durable_facts(fenced, floor)
        except oracle.OracleError as exc:
            if "packet.issue names a fenced authority" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a bundle naming a fenced Packet was accepted")

        foreign = _sealed_json(root / "foreign-mission-facts.json", fixture.foreign_mission_facts())
        try:
            oracle._read_durable_facts(foreign, floor)
        except oracle.OracleError as exc:
            if "mission.issue names a fenced authority" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a bundle naming a different Mission was accepted")

        at_floor = _sealed_json(root / "at-floor-facts.json", fixture.at_floor_facts())
        accepted = oracle._read_durable_facts(at_floor, floor)
        if accepted["mission"]["revision"] != floor["mission_revision_min"]:
            raise AssertionError(accepted)
        if accepted["packet"]["generation"] != floor["packet_generation_min"]:
            raise AssertionError(accepted)

        # Sàn là ĐƠN ĐIỆU, không phải bằng nhau: thẩm quyền mới hơn phải qua.
        above = _sealed_json(root / "above-floor-facts.json", fixture.above_floor_facts())
        accepted_above = oracle._read_durable_facts(above, floor)
        if accepted_above["packet"]["revision"] != floor["packet_revision_min"] + 1:
            raise AssertionError(accepted_above)

        current_value = fixture.current_facts()
        current = _sealed_json(root / "current-facts.json", current_value)
        accepted_current = oracle._read_durable_facts(current, floor)
        expected = {"mission": current_value["mission"], "packet": current_value["packet"]}
        if accepted_current != expected:
            raise AssertionError({"accepted": accepted_current, "fixture": expected})


def authority_fixture_is_external_and_binds_the_current_durable_authority() -> None:
    """Fixture phải NGOÀI cây ứng viên và phải niêm phong; cả hai đều đo được.

    Một tệp "fixture" nằm trong checkout thì Executor sửa được, và khi đó nó chỉ
    là hằng của ứng viên đội lốt đầu vào ngoài — đúng thứ §4.3 cấm.
    """
    module = _module("authority_fixture")
    fixture = _authority_fixture()
    if not fixture.produced_by or not fixture.source:
        raise AssertionError("the fixture does not record who produced it: %r" % (fixture,))
    if fixture.current["mission"]["issue"] != fixture.floor["mission_issue"]:
        raise AssertionError("fixture floor and current facts name different Missions")
    if fixture.current["packet"]["issue"] != fixture.floor["packet_issue"]:
        raise AssertionError("fixture floor and current facts name different Packets")

    with tempfile.TemporaryDirectory(prefix="ra02-fixture-") as tmp:
        root = pathlib.Path(tmp)
        inside = root / "authority-fixture.json"
        shutil.copyfile(fixture.path, inside)
        inside.chmod(0o444)
        try:
            module.load(inside, root)
        except module.AuthorityFixtureError as exc:
            if "outside the candidate checkout" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a fixture inside the candidate checkout was accepted")

        # Cánh dương trên CÙNG tệp đó: ca trên đỏ vì đúng lý do vị trí, không
        # phải vì nội dung hỏng.
        elsewhere = root / "elsewhere"
        elsewhere.mkdir()
        again = module.load(inside, elsewhere)
        if again.sha256 != fixture.sha256 or dict(again.floor) != dict(fixture.floor):
            raise AssertionError({"reloaded": again.sha256, "original": fixture.sha256})

        writable = root / "writable-fixture.json"
        shutil.copyfile(fixture.path, writable)
        writable.chmod(0o644)
        try:
            module.load(writable, elsewhere)
        except module.AuthorityFixtureError as exc:
            if "sealed read-only" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("an unsealed authority fixture was accepted")


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
    pinned = CANDIDATE_ROOT / pathlib.PurePosixPath(inventory.PINNED_CORPUS_PATH)
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


def _public_corpus():
    """Corpus CÔNG KHAI đã ghim, đọc y như oracle đọc nó."""
    corpus_module = _module("corpus")
    inventory = _module("trusted_inventory")
    pinned = CANDIDATE_ROOT / pathlib.PurePosixPath(inventory.PINNED_CORPUS_PATH)
    raw = corpus_module.read_bytes(pinned, require_readonly=False)
    loaded = corpus_module.load(
        pinned,
        hashlib.sha256(raw).hexdigest(),
        inventory.PROTOCOL_SCHEMA_PATHS,
        require_readonly=False,
    )
    return corpus_module, loaded


def _heldout_document(tag: str) -> dict[str, object]:
    """Tài liệu chưa từng công bố: khoá riêng, không đụng bất kỳ ca công khai nào."""
    return {"ra02_withheld_probe": tag, "schema_version": 1}


def _sealed_heldout(path: pathlib.Path, cases: list[dict[str, object]], binding: str, seed: int = 7) -> pathlib.Path:
    return _sealed_json(
        path,
        {
            "schema_version": 1,
            "produced_by": "dispatcher-test-double",
            "source": {"note": "selftest fixture"},
            "target_schema_inventory_sha256": binding,
            "reorder_seed": seed,
            "cases": cases,
        },
    )


def heldout_inputs_must_be_declared_sealed_and_truly_withheld() -> None:
    """§8.4: "giữ lại" là thứ ĐO được, không phải một nhãn dán lên tệp.

    Bốn cách gian lận bị chặn ở đây: pin không khai; tài liệu đã nằm trong corpus
    công khai (đổi ID không cứu được); chỉ một nhãn (bộ nhớ đoán một phát là
    trúng cả bộ); và sai mẫu số so với pin.
    """
    heldout = _module("heldout")
    corpus_module, loaded = _public_corpus()
    binding = loaded.target_schema_inventory_sha256
    schema_paths = _module("trusted_inventory").PROTOCOL_SCHEMA_PATHS
    public_ids = list(loaded.case_id_registry)
    public_digests = [corpus_module.document_digest(case.document) for case in loaded.cases]
    published = next(case for case in loaded.cases if case.expected_valid)

    try:
        heldout.declaration({"schema_version": 1})
    except heldout.HeldOutError as exc:
        if "declares no held-out input source" not in str(exc):
            raise AssertionError(str(exc)) from exc
    else:
        raise AssertionError("a Dispatcher pin without a held-out block was accepted")

    good_cases = [
        {
            "case_id": "a1b2c3d4e5f60718",
            "schema_path": published.schema_path,
            "kind": "valid",
            "expected_valid": True,
            "semantic_group": "withheld_valid",
            "document": _heldout_document("valid-probe"),
        },
        {
            "case_id": "b1b2c3d4e5f60719",
            "schema_path": published.schema_path,
            "kind": "invalid",
            "expected_valid": False,
            "semantic_group": "withheld_invalid",
            "document": _heldout_document("invalid-probe"),
        },
    ]

    def _load(path: pathlib.Path, count: int, digest: str | None = None):
        raw = path.read_bytes()
        declared = {
            "path": str(path),
            "sha256": digest or hashlib.sha256(raw).hexdigest(),
            "case_count": count,
        }
        return heldout.load(declared, CANDIDATE_ROOT, schema_paths, binding, public_ids, public_digests)

    with tempfile.TemporaryDirectory(prefix="ra02-heldout-") as tmp:
        root = pathlib.Path(tmp)
        good = _sealed_heldout(root / "heldout.json", good_cases, binding)
        held = _load(good, 2)
        if held.label_counts != {"valid": 1, "invalid": 1} or len(held.cases) != 2:
            raise AssertionError(held)

        leaked = _sealed_heldout(
            root / "leaked.json",
            [
                dict(good_cases[0], document=published.document),
                good_cases[1],
            ],
            binding,
        )
        try:
            _load(leaked, 2)
        except heldout.HeldOutError as exc:
            if "already published in the public corpus" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a published document was accepted as a held-out input")

        reused_id = _sealed_heldout(
            root / "reused-id.json",
            [dict(good_cases[0], case_id=public_ids[0]), good_cases[1]],
            binding,
        )
        try:
            _load(reused_id, 2)
        except heldout.HeldOutError as exc:
            if "also appears in the public corpus" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a public case id was accepted as a held-out id")

        single = _sealed_heldout(root / "single-label.json", [good_cases[0]], binding)
        try:
            _load(single, 1)
        except heldout.HeldOutError as exc:
            if "must carry both labels" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a single-label held-out set was accepted")

        try:
            _load(good, 3)
        except heldout.HeldOutError as exc:
            if "case count disagrees with the Dispatcher pin" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a held-out set disagreeing with its pinned denominator was accepted")

        try:
            _load(good, 2, digest="0" * 64)
        except heldout.HeldOutError as exc:
            if "SHA-256 does not match the Dispatcher pin" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a held-out set with the wrong digest was accepted")

        wrong_binding = _sealed_heldout(root / "wrong-target.json", good_cases, "1" * 64)
        try:
            _load(wrong_binding, 2)
        except heldout.HeldOutError as exc:
            if "different target schema inventory" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("a held-out set authored for other schemas was accepted")


def exact_hash_memorizer_survives_public_cases_and_dies_on_withheld_ones() -> None:
    """Bằng chứng DƯƠNG cho SPEC-002, đo được cả hai chiều.

    Reviewer attempt 3 đã dựng đúng bảng tra digest→nhãn từ corpus công khai và
    khớp 34/34.  Ca này tái lập chính điều đó: trên tập công khai, bộ nhớ-thuộc-
    lòng phải SỐNG SÓT — nếu nó chết ở đây thì phép giết của meta-suite nói về
    một mutant khác chứ không phải kiểu gian lận cần chặn.  Rồi thêm ca giữ lại:
    nó phải CHẾT, và mọi ca làm nó chết phải nằm trong tập giữ lại.
    """
    fake_validators = _module("fake_validators")
    _corpus_module, loaded = _public_corpus()
    public = list(loaded.cases)

    survived = fake_validators.run_one("exact_hash_only", public)
    if survived["disposition"] != "survived":
        raise AssertionError(
            "the public corpus alone no longer lets an exact-hash memorizer through: %r" % survived
        )
    if survived["real_rc"] != 0:
        raise AssertionError(survived)

    withheld = [
        {
            "case_id": "c1b2c3d4e5f6071a",
            "document": _heldout_document("kill-valid"),
            "expected_valid": True,
        },
        {
            "case_id": "d1b2c3d4e5f6071b",
            "document": _heldout_document("kill-invalid"),
            "expected_valid": False,
        },
    ]
    withheld_ids = {case["case_id"] for case in withheld}
    killed = fake_validators.run_one("exact_hash_only", public + withheld)
    if killed["disposition"] != "killed":
        raise AssertionError("withheld cases did not kill the memorizer: %r" % killed)
    affected = set(killed.get("affected_case_ids") or [])
    if not affected:
        raise AssertionError("the kill carries no case evidence: %r" % killed)
    if not affected <= withheld_ids:
        raise AssertionError(
            "the memorizer was killed by public cases it should have memorized: %r" % sorted(affected - withheld_ids)
        )


def authority_floor_key_contract_has_exactly_one_declaration() -> None:
    """WP99-R3G3-STD-001: bootstrap không còn bản sao thứ hai của bảng khoá sàn."""
    source_pin = _source_pin_module()
    inventory = _module("trusted_inventory")
    if hasattr(source_pin, "AUTHORITY_FLOOR_KEYS"):
        raise AssertionError("the bootstrap still declares its own AUTHORITY_FLOOR_KEYS")

    with _trusted_temp_repository() as (root, head, source_paths):
        derived = source_pin.pinned_authority_floor_keys(str(root))
        if derived != inventory.AUTHORITY_FLOOR_KEYS:
            raise AssertionError({"derived": derived, "declared": inventory.AUTHORITY_FLOOR_KEYS})
        binding = source_pin.measure(str(root), head, source_paths)
        pin = root / "dispatcher-pin-with-floor.json"
        pin.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "candidate": {
                        "head": binding["candidate_head"],
                        "tree": binding["candidate_tree"],
                    },
                    "trusted_source_paths": list(source_paths),
                    "trusted_source_inventory_sha256": binding["trusted_source_inventory_sha256"],
                    "target": {
                        "ref": "dispatcher/fixture",
                        "head": "a" * 40,
                        "tree": "b" * 40,
                        "schema_inventory_sha256": "c" * 64,
                    },
                    "authority_floor": {key: 2 for key in derived},
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        pin.chmod(0o444)
        blocks = source_pin.pin_blocks(str(pin), derived)
        if set(blocks["authority_floor"]) != set(derived):
            raise AssertionError(blocks)
        # Bảng khoá là THAM SỐ: đưa bảng khác thì phải chết theo tên, chứng minh
        # hằng cục bộ cũ đã thật sự biến mất chứ không chỉ bị đổi tên.
        try:
            source_pin.pin_blocks(str(pin), derived[:1])
        except source_pin.SourcePinError as exc:
            if "authority_floor must contain exactly" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("pin_blocks ignored the supplied floor key contract")
        try:
            source_pin.pin_blocks(str(pin), ())
        except source_pin.SourcePinError as exc:
            if "non-empty duplicate-free tuple" not in str(exc):
                raise AssertionError(str(exc)) from exc
        else:
            raise AssertionError("an empty floor key contract was accepted")


def main(argv: list[str] | None = None) -> int:
    global _AUTHORITY_FIXTURE_PATH
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority-fixture")
    args = parser.parse_args(argv)
    _AUTHORITY_FIXTURE_PATH = args.authority_fixture
    tests = (
        source_pin_rejects_fabricated_repository,
        source_pin_rejects_git_blob_byte_mismatch,
        source_pin_rejects_symlink_mismatch,
        fake_lowercase_commit_cannot_emit_oracle_artifact,
        authority_bundle_rejects_stale_pins,
        durable_facts_reject_empty_authority_blocks,
        durable_facts_reject_authority_below_dispatcher_floor,
        authority_fixture_is_external_and_binds_the_current_durable_authority,
        authority_floor_key_contract_has_exactly_one_declaration,
        sandbox_report_missing_repeat_fields_is_structured_red,
        keyword_controls_require_independent_engine_agreement,
        pinned_corpus_is_in_tree_and_anchors_are_well_formed,
        heldout_inputs_must_be_declared_sealed_and_truly_withheld,
        exact_hash_memorizer_survives_public_cases_and_dies_on_withheld_ones,
        hardened_reader_parity_between_bootstrap_and_shared_module,
        every_inventoried_keyword_has_positive_and_negative_teeth,
        schema_shape_rejects_remote_or_unresolved_refs,
        validator_stderr_cannot_forge_fixture_gap,
        all_five_fake_validators_are_killed_by_blind_case_evidence,
    )
    # §6.1: mẫu số là kích thước SỔ ĐĂNG KÝ, chốt trước khi chạy.  Một ca thiếu
    # fixture ngoài phải hiện ra là `not_run` CÓ LÝ DO và kéo cổng xuống đỏ, chứ
    # không được biến mất khỏi mẫu số để phần còn lại tự khai N/N.
    scheduled = [test.__name__ for test in tests]
    records: list[dict[str, object]] = []
    passed = failed = not_run = 0
    for test in tests:
        try:
            test()
        except FixtureUnavailable as exc:
            not_run += 1
            records.append(
                {"test_id": test.__name__, "status": "not_run", "passed": False, "reason": str(exc)}
            )
            print("[NOT-RUN] %s -- %s" % (test.__name__, exc))
        except Exception as exc:
            failed += 1
            records.append(
                {
                    "test_id": test.__name__,
                    "status": "executed",
                    "passed": False,
                    "error": {"name": type(exc).__name__, "message": str(exc)},
                }
            )
            print("[FAIL] %s -- %s: %s" % (test.__name__, type(exc).__name__, exc))
        else:
            passed += 1
            records.append({"test_id": test.__name__, "status": "executed", "passed": True})
            print("[OK] %s" % test.__name__)
    accounting = {
        "schema_version": 1,
        "scheduled_test_ids": scheduled,
        "scheduled_total": len(scheduled),
        "executed": passed + failed,
        "passed": passed,
        "failed": failed,
        "skipped": 0,
        "not_run": not_run,
        "authority_fixture_supplied": _AUTHORITY_FIXTURE_PATH is not None
        or bool(os.environ.get("RA02_AUTHORITY_FIXTURE")),
        "tests": records,
        "ok": bool(scheduled) and passed == len(scheduled),
    }
    print(json.dumps(accounting, ensure_ascii=False, sort_keys=True))
    print("== ra02 oracle selftest %d/%d ==" % (passed, len(tests)))
    return 0 if accounting["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
