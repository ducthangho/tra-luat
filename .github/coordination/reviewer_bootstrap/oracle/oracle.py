"""Direct and behavioural oracle driven only by pinned external data."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import pathlib
import random
import re
import subprocess
import sys
import tempfile
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from core import artifacts  # noqa: E402
from oracle import authority, corpus, engine, fake_validators, heldout, safe_io  # noqa: E402
from oracle.trusted_inventory import (  # noqa: E402
    FAKE_VALIDATOR_IDS,
    PINNED_CORPUS_PATH,
    PROTOCOL_SCHEMA_PATHS,
    PROTOCOL_SOURCE_PATH,
    REQUIRED_ESCAPE_KEYS,
    REQUIRED_RESOURCE_KEYS,
    SANDBOX_TEST_IDS,
    TRUSTED_SOURCE_PATHS,
)

OID40 = re.compile(r"[0-9a-f]{40}\Z")


class OracleError(RuntimeError):
    """A trusted input, engine, evidence, or retention invariant failed."""


def _git(root: pathlib.Path, *args: str, binary: bool = False):
    return safe_io.git(root, *args, error=OracleError, binary=binary)


def _read_regular(path: pathlib.Path, label: str, require_readonly: bool = False) -> bytes:
    return safe_io.read_regular_single_link(
        path, label, OracleError, require_readonly=require_readonly
    )


def _strict_json(raw: bytes, label: str) -> object:
    def pairs(values: list[tuple[str, object]]) -> dict[str, object]:
        result = {}
        for key, value in values:
            if key in result:
                raise OracleError("%s has duplicate JSON key %r" % (label, key))
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except OracleError:
        raise
    except (UnicodeError, ValueError) as exc:
        raise OracleError("%s is not strict UTF-8 JSON: %s" % (label, exc)) from exc


def _blob_binding(root: pathlib.Path, head: str, relative: str) -> dict[str, object]:
    disk = _read_regular(root / pathlib.PurePosixPath(relative), relative)
    listing = str(_git(root, "ls-tree", head, "--", relative)).strip()
    if "\t" not in listing:
        raise OracleError("pinned path absent from target commit: %s" % relative)
    meta, returned = listing.split("\t", 1)
    fields = meta.split()
    if len(fields) != 3 or fields[1] != "blob" or returned != relative:
        raise OracleError("pinned path is not one exact Git blob: %s" % relative)
    blob = _git(root, "cat-file", "blob", fields[2], binary=True)
    if blob != disk:
        raise OracleError("checkout bytes differ from Git blob: %s" % relative)
    return {
        "path": relative,
        "mode": fields[0],
        "git_blob": fields[2],
        "sha256": hashlib.sha256(disk).hexdigest(),
        "bytes": len(disk),
        "raw": disk,
    }


def _protocol_observation(repo_root: pathlib.Path, candidate_head: str) -> dict[str, object]:
    binding = _blob_binding(repo_root, candidate_head, PROTOCOL_SOURCE_PATH)
    return {
        "commit_sha": candidate_head,
        "path": PROTOCOL_SOURCE_PATH,
        "file_git_oid": binding["git_blob"],
        "file_sha256": binding["sha256"],
    }


def _target_reachability(root: pathlib.Path, head: str, declared_ref: str) -> dict[str, object]:
    """Đòi bằng chứng commit target VỚI TỚI ĐƯỢC từ một ref.

    Attempt 2 ghim một commit mà `upload-pack` trả "not our ref" và không nằm
    trong kho object nào — mọi bằng chứng oracle khi đó chỉ Executor dựng lại
    được (R1).  Một object không nằm dưới ref nào thì không ai fetch nổi.
    """
    try:
        containing = [
            line.strip()
            for line in str(_git(root, "for-each-ref", "--format=%(refname)", "--contains", head)).splitlines()
            if line.strip()
        ]
    except OracleError:
        containing = []
    tip = None
    try:
        tip = str(_git(root, "rev-parse", "--verify", declared_ref + "^{commit}")).strip()
    except OracleError:
        tip = None
    ancestor = False
    if tip:
        probe = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", head, tip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        ancestor = probe.returncode == 0
    record = {
        "declared_ref": declared_ref,
        "declared_ref_present": tip is not None,
        "declared_ref_tip": tip,
        "head_is_ref_tip_or_ancestor": ancestor,
        "refs_containing_head": containing,
    }
    if not containing and not (tip is not None and ancestor):
        raise OracleError(
            "target checkout head is not reachable from any ref: head=%s declared_ref=%r" % (head, declared_ref)
        )
    return record


def _target_observation(
    target_root: pathlib.Path, target_pin: Mapping[str, object]
) -> tuple[dict[str, object], dict[str, Mapping[str, object]], dict[str, bytes]]:
    root = target_root.resolve()
    top = pathlib.Path(str(_git(root, "rev-parse", "--show-toplevel")).strip()).resolve()
    if top != root:
        raise OracleError("target_root is not the exact Git top-level")
    head = str(_git(root, "rev-parse", "HEAD")).strip()
    tree = str(_git(root, "rev-parse", "HEAD^{tree}")).strip()
    if not OID40.fullmatch(head) or not OID40.fullmatch(tree):
        raise OracleError("target checkout head/tree is not a full lowercase Git oid")
    declared_ref = target_pin.get("ref")
    if not isinstance(declared_ref, str) or not declared_ref:
        raise OracleError("Dispatcher target pin must declare a ref name")
    reachability = _target_reachability(root, head, declared_ref)
    tracked = set(
        line
        for line in str(_git(root, "ls-tree", "-r", "--name-only", head, "--", ".github/schemas")).splitlines()
        if line.endswith(".schema.json")
    )
    if tracked != set(PROTOCOL_SCHEMA_PATHS):
        raise OracleError(
            "target schema set mismatch: missing=%s extra=%s"
            % (sorted(set(PROTOCOL_SCHEMA_PATHS) - tracked), sorted(tracked - set(PROTOCOL_SCHEMA_PATHS)))
        )
    entries = []
    schemas: dict[str, Mapping[str, object]] = {}
    raw_schema_bytes: dict[str, bytes] = {}
    for relative in PROTOCOL_SCHEMA_PATHS:
        entry = _blob_binding(root, head, relative)
        raw = entry.pop("raw")
        schema = _strict_json(raw, relative)
        if not isinstance(schema, dict):
            raise OracleError("schema is not an object: %s" % relative)
        entries.append(entry)
        schemas[relative] = schema
        raw_schema_bytes[relative] = raw
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    inventory = hashlib.sha256(canonical).hexdigest()
    mismatched = [
        name
        for name, pair in (
            ("head", (target_pin.get("head"), head)),
            ("tree", (target_pin.get("tree"), tree)),
            ("schema_inventory_sha256", (target_pin.get("schema_inventory_sha256"), inventory)),
        )
        if pair[0] != pair[1]
    ]
    if mismatched:
        raise OracleError("Dispatcher target pin mismatch: changed=%s" % mismatched)
    observation = {
        "head": head,
        "tree": tree,
        "ref": declared_ref,
        "reachability": reachability,
        "schema_paths": list(PROTOCOL_SCHEMA_PATHS),
        "schema_entries": entries,
        "schema_inventory_sha256": inventory,
    }
    return observation, schemas, raw_schema_bytes


class _IndependentEngine:
    """Bộ máy độc lập dùng để CHẤM các răng keyword, không phải để bỏ phiếu."""

    def __init__(self, module: object):
        self._module = module

    def validate(self, schema: Mapping[str, object], instance: object) -> bool:
        validator = self._module.Draft202012Validator(schema)
        return not list(validator.iter_errors(instance))

    def check_schema(self, schema: Mapping[str, object]) -> bool:
        try:
            self._module.Draft202012Validator.check_schema(schema)
        except self._module.exceptions.SchemaError:
            return False
        return True


def _engine_metadata() -> tuple[dict[str, object], _IndependentEngine]:
    try:
        import jsonschema
    except ImportError as exc:
        raise OracleError("independent JSON Schema implementation is unavailable: %s" % exc) from exc

    package_root = pathlib.Path(jsonschema.__file__).resolve().parent
    digest = hashlib.sha256()
    files = sorted(path for path in package_root.rglob("*.py") if path.is_file())
    for path in files:
        relative = path.relative_to(package_root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    metadata = {
        "name": "python-jsonschema",
        "version": importlib.metadata.version("jsonschema"),
        "digest_sha256": digest.hexdigest(),
        "implementation_files": len(files),
        "dialect": "https://json-schema.org/draft/2020-12/schema",
        "grades_keyword_controls": True,
    }
    return metadata, _IndependentEngine(jsonschema)


def _case_worker(request_path: pathlib.Path, result_path: pathlib.Path) -> int:
    request = _strict_json(_read_regular(request_path, "case request"), "case request")
    if not isinstance(request, dict) or request.get("schema_version") != 1:
        return 2
    schema = request.get("schema")
    if not isinstance(schema, dict):
        return 2
    document = request.get("document")
    local_errors = engine.validate(schema, document)
    try:
        import jsonschema

        validator = jsonschema.Draft202012Validator(schema)
        independent_errors = sorted(
            (
                {"path": list(error.absolute_path), "validator": error.validator}
                for error in validator.iter_errors(document)
            ),
            key=lambda item: (json.dumps(item["path"]), str(item["validator"])),
        )
    except Exception as exc:  # noqa: BLE001
        result_path.write_text(
            json.dumps({"schema_version": 1, "case_id": request.get("case_id"), "error": {"name": type(exc).__name__, "message": str(exc)}}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return 2
    local_valid = not local_errors
    independent_valid = not independent_errors
    agreement = local_valid is independent_valid
    record = {
        "schema_version": 1,
        "case_id": request.get("case_id"),
        "local_valid": local_valid,
        "independent_valid": independent_valid,
        "agreement": agreement,
        "local_errors": local_errors,
        "independent_errors": independent_errors,
    }
    result_path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")
    if not agreement:
        return 4
    return 0 if local_valid else 3


def _run_case(case: corpus.Case, schema: Mapping[str, object]) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="ra02-case-") as tmp:
        root = pathlib.Path(tmp)
        request = root / "request.json"
        result = root / "result.json"
        request.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "case_id": case.case_id,
                    "schema": schema,
                    "document": case.document,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        env = {
            key: value
            for key, value in os.environ.items()
            if key in ("PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "TEMP", "TMP", "LANG")
        }
        proc = subprocess.run(
            [sys.executable, str(pathlib.Path(__file__).resolve()), "--case-worker", str(request), str(result)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
            env=env,
        )
        if not result.is_file():
            return {
                "case_id": case.case_id,
                "schema_path": case.schema_path,
                "expected_valid": case.expected_valid,
                "status": "executed",
                "rc": proc.returncode,
                "passed": False,
                "error": "typed case result missing",
                "stderr_sha256": hashlib.sha256(proc.stderr).hexdigest(),
            }
        typed = _strict_json(result.read_bytes(), "typed case result")
        if not isinstance(typed, dict):
            raise OracleError("typed case result is not an object")
        expected_rc = 0 if case.expected_valid else 3
        passed = (
            proc.returncode == expected_rc
            and typed.get("agreement") is True
            and typed.get("local_valid") is case.expected_valid
            and typed.get("independent_valid") is case.expected_valid
        )
        return {
            "case_id": case.case_id,
            "schema_path": case.schema_path,
            "semantic_group": case.semantic_group,
            "kind": case.kind,
            "expected_valid": case.expected_valid,
            "status": "executed",
            "rc": proc.returncode,
            "passed": passed,
            "typed_result": typed,
            "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(proc.stderr).hexdigest(),
        }


def _read_durable_facts(path: pathlib.Path, floor: Mapping[str, object]) -> dict[str, object]:
    value = _strict_json(_read_regular(path, "durable facts", require_readonly=True), "durable facts")
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise OracleError("durable facts must be a schema_version 1 object")
    if set(value) != {"schema_version", "mission", "packet"}:
        raise OracleError("durable facts must contain exactly mission and packet blocks")
    try:
        return authority.validate_durable_facts(value, floor)
    except authority.AuthorityError as exc:
        raise OracleError("durable facts rejected before oracle execution: %s" % exc) from exc


def _typed(container: Mapping[str, object], key: str, kinds: tuple[type, ...], label: str) -> object:
    """Đọc một trường CÓ KIỂU.

    `value.get(k) < 8` trên một khoá THIẾU ném `TypeError` trần, rc=1, stdout
    rỗng — đúng thứ §6.2 cấm (R4).  Thiếu hoặc sai kiểu phải thành lỗi có tên.
    """
    if key not in container:
        raise OracleError("%s is missing required field %r" % (label, key))
    value = container[key]
    if isinstance(value, bool) and bool not in kinds:
        raise OracleError("%s field %r must not be a boolean" % (label, key))
    if not isinstance(value, kinds):
        raise OracleError(
            "%s field %r must be %s, got %s" % (label, key, "/".join(k.__name__ for k in kinds), type(value).__name__)
        )
    return value


def _runner_observation(
    path: pathlib.Path, candidate_head: str, inventory_digest: str
) -> tuple[dict[str, object], Mapping[str, object], bytes]:
    raw = _read_regular(path, "sandbox report", require_readonly=True)
    value = _strict_json(raw, "sandbox report")
    if not isinstance(value, dict):
        raise OracleError("sandbox report is not an object")
    if value.get("ok") is not True:
        raise OracleError("sandbox report is not green")
    requested = _typed(value, "repeat_requested", (int,), "sandbox report")
    executed_runs = _typed(value, "repeat_executed", (int,), "sandbox report")
    if requested < 8:
        raise OracleError("sandbox report requested %d runs; at least eight are required" % requested)
    if executed_runs != requested:
        raise OracleError(
            "sandbox report executed %d of %d requested runs" % (executed_runs, requested)
        )
    if _typed(value, "same_scheduled_test_ids", (bool,), "sandbox report") is not True:
        raise OracleError("sandbox repeated runs did not schedule the same test IDs")
    if _typed(value, "stable_classifications", (bool,), "sandbox report") is not True:
        raise OracleError("sandbox repeated runs are unstable")
    runs = _typed(value, "runs", (list,), "sandbox report")
    if not runs:
        raise OracleError("sandbox report has no run records")
    fingerprints = []
    for index, run in enumerate(runs):
        label = "sandbox run %d" % index
        if not isinstance(run, Mapping):
            raise OracleError("%s is not an object" % label)
        if run.get("ok") is not True:
            raise OracleError("%s is not green" % label)
        if run.get("candidate_head") != candidate_head:
            raise OracleError("%s candidate head mismatch" % label)
        binding = run.get("candidate_source_binding")
        if not isinstance(binding, Mapping) or binding.get("trusted_source_inventory_sha256") != inventory_digest:
            raise OracleError("%s trusted source digest mismatch" % label)
        if run.get("scheduled_test_ids") != list(SANDBOX_TEST_IDS):
            raise OracleError("%s scheduled test IDs mismatch" % label)
        counts = {
            name: _typed(run, name, (int,), label)
            for name in ("scheduled_total", "executed", "passed", "failed", "skipped", "not_run")
        }
        if not (
            counts["scheduled_total"] == counts["executed"] == counts["passed"] == len(SANDBOX_TEST_IDS)
            and counts["failed"] == counts["skipped"] == counts["not_run"] == 0
        ):
            raise OracleError("%s accounting is not honest N/N: %s" % (label, counts))
        required = run.get("required_counterexamples")
        if not isinstance(required, Mapping):
            raise OracleError("%s required counterexample matrix missing" % label)
        escape = required.get("sandbox_escape_classes")
        resources = required.get("resource_classes")
        if not isinstance(escape, Mapping) or set(escape) != set(REQUIRED_ESCAPE_KEYS):
            raise OracleError("%s escape keys mismatch" % label)
        if not isinstance(resources, Mapping) or set(resources) != set(REQUIRED_RESOURCE_KEYS):
            raise OracleError("%s resource keys mismatch" % label)
        for item in list(escape.values()) + list(resources.values()):
            if not isinstance(item, Mapping) or item.get("passed") is not True or item.get("rc") is None or not item.get("evidence"):
                raise OracleError("%s counterexample lacks real rc or evidence" % label)
        tests = run.get("tests")
        if not isinstance(tests, list):
            raise OracleError("%s has no test records" % label)
        healthy = next(
            (item for item in tests if isinstance(item, Mapping) and item.get("test_id") == "healthy_positive_control"),
            None,
        )
        if healthy is None or not isinstance(healthy.get("result"), Mapping):
            raise OracleError("%s is missing the healthy positive control record" % label)
        fingerprints.append(healthy["result"].get("fingerprint"))
    if any(item != fingerprints[0] for item in fingerprints):
        raise OracleError("runner fingerprint changed across standalone runs")
    canonical = json.dumps(fingerprints[0], sort_keys=True, separators=(",", ":")).encode("utf-8")
    return (
        {
            "runner_fingerprint_sha256": hashlib.sha256(canonical).hexdigest(),
            "sandbox_report_sha256": hashlib.sha256(raw).hexdigest(),
        },
        value,
        raw,
    )


def _resolve_corpus(repo_root: pathlib.Path, corpus_path: str | None) -> tuple[pathlib.Path, bool]:
    """Corpus mặc định là bản ĐÃ GHIM trong cây tin cậy.

    Cho phép trỏ tới bản sao ngoài, nhưng bản sao phải trùng BYTE — một corpus
    riêng chỉ tồn tại trên máy Executor chính là đầu vào không ai kiểm lại được.
    """
    pinned = repo_root / pathlib.PurePosixPath(PINNED_CORPUS_PATH)
    if corpus_path is None:
        return pinned, False
    supplied = pathlib.Path(corpus_path)
    if supplied.resolve() == pinned.resolve():
        return pinned, False
    if corpus.read_bytes(supplied, require_readonly=True) != _read_regular(pinned, PINNED_CORPUS_PATH):
        raise OracleError("supplied corpus differs from the pinned in-tree corpus: %s" % PINNED_CORPUS_PATH)
    return supplied, True


def evaluate(
    *,
    repo_root: str,
    candidate_head: str,
    authority_bundle: str,
    durable_facts: str,
    target_root: str,
    corpus_path: str | None,
    sandbox_report: str,
    output_root: str,
    source_binding: Mapping[str, object],
    target_pin: Mapping[str, object],
    authority_floor: Mapping[str, object],
) -> dict[str, object]:
    root = pathlib.Path(repo_root).resolve()
    if source_binding.get("candidate_head") != candidate_head:
        raise OracleError("pre-import source binding candidate mismatch")
    target_observation, schemas, raw_schema_bytes = _target_observation(
        pathlib.Path(target_root), target_pin
    )
    protocol = _protocol_observation(root, candidate_head)
    facts = _read_durable_facts(pathlib.Path(durable_facts), authority_floor)
    resolved_corpus, external_copy = _resolve_corpus(root, corpus_path)
    corpus_raw = corpus.read_bytes(resolved_corpus, require_readonly=external_copy)
    corpus_sha = hashlib.sha256(corpus_raw).hexdigest()
    runner_observation, runner_report_value, runner_report_raw = _runner_observation(
        pathlib.Path(sandbox_report), candidate_head, str(source_binding["trusted_source_inventory_sha256"])
    )
    # R5: `sandbox_report_sha256` mang uuid4 và mốc thời gian, KHÔNG thể tồn tại
    # trước khi ứng viên chạy — nó không phải thứ niêm phong được.  Giữ lại làm
    # quan sát ghi nhận, nhưng bó niêm phong chỉ so những giá trị tất định.
    sealed_observations = {
        "protocol": protocol,
        "mission": facts["mission"],
        "packet": facts["packet"],
        "candidate": {"head": candidate_head, "tree": source_binding["candidate_tree"]},
        "trusted_source_paths": list(TRUSTED_SOURCE_PATHS),
        "trusted_source_inventory_sha256": source_binding["trusted_source_inventory_sha256"],
        "target_checkout": {"head": target_observation["head"], "tree": target_observation["tree"]},
        "target_schema_paths": list(PROTOCOL_SCHEMA_PATHS),
        "target_schema_inventory_sha256": target_observation["schema_inventory_sha256"],
        "corpus_sha256": corpus_sha,
        "runner_fingerprint_sha256": runner_observation["runner_fingerprint_sha256"],
    }
    recorded_observations = {"sandbox_report_sha256": runner_observation["sandbox_report_sha256"]}
    authority_value = authority.load_and_verify(authority_bundle, sealed_observations)
    loaded = corpus.load(resolved_corpus, corpus_sha, PROTOCOL_SCHEMA_PATHS, require_readonly=external_copy)
    if loaded.target_schema_inventory_sha256 != target_observation["schema_inventory_sha256"]:
        raise OracleError(
            "pinned corpus was authored for a different target schema inventory: corpus=%s measured=%s"
            % (loaded.target_schema_inventory_sha256, target_observation["schema_inventory_sha256"])
        )
    # §8.4: đầu vào GIỮ LẠI đến từ pin niêm phong, không từ nguồn ứng viên.  Bảng
    # tra digest → nhãn dựng từ corpus công khai giải được 34/34 mà không kiểm một
    # keyword nào (SPEC-002); chỉ ca chưa từng công bố mới giết được nó.
    pin_value = _strict_json(
        _read_regular(pathlib.Path(authority_bundle), "Dispatcher pin", require_readonly=True),
        "Dispatcher pin",
    )
    if not isinstance(pin_value, Mapping):
        raise OracleError("Dispatcher pin is not an object")
    held = heldout.load(
        heldout.declaration(pin_value),
        root,
        PROTOCOL_SCHEMA_PATHS,
        target_observation["schema_inventory_sha256"],
        loaded.case_id_registry,
        [corpus.document_digest(case.document) for case in loaded.cases],
    )
    combined_reorder_seed = loaded.reorder_seed ^ held.reorder_seed
    cases = list(loaded.cases) + list(held.cases)
    random.Random(combined_reorder_seed).shuffle(cases)
    heldout_case_ids = set(held.case_ids)
    anchors = loaded.anchors

    engine_metadata, independent = _engine_metadata()
    all_keywords = set()
    shape_errors = {}
    schema_keywords = {}
    for path_name, schema in schemas.items():
        errors = engine.schema_shape_errors(schema)
        if errors:
            shape_errors[path_name] = errors
        schema_keywords[path_name] = engine.keyword_inventory(schema)
        all_keywords.update(schema_keywords[path_name])
    missing_anchors = sorted(all_keywords - set(anchors))
    extra_anchors = sorted(set(anchors) - all_keywords)
    controls = engine.keyword_controls(sorted(all_keywords), independent=independent)
    failed_controls = sorted(
        keyword
        for keyword, record in controls.items()
        if record.get("positive_passed") is not True or record.get("negative_failed") is not True
    )
    if shape_errors or missing_anchors or extra_anchors or failed_controls:
        raise OracleError(
            "schema keyword gate failed: shape=%s missing=%s extra=%s controls=%s"
            % (shape_errors, missing_anchors, extra_anchors, failed_controls)
        )
    by_case = {case.case_id: case for case in cases}
    for keyword, record in anchors.items():
        valid = by_case[record["valid_case_id"]]
        invalid = by_case[record["invalid_case_id"]]
        if valid.expected_valid is not True or invalid.expected_valid is not False:
            raise OracleError("keyword anchor labels are not one valid and one invalid case: %s" % keyword)
        if valid.schema_path != invalid.schema_path:
            raise OracleError("keyword anchor crosses schema boundaries: %s" % keyword)
        if keyword not in schema_keywords[valid.schema_path]:
            raise OracleError("keyword anchor does not target a schema containing the keyword: %s" % keyword)

    # R6: mẫu số là kích thước SỔ ĐĂNG KÝ chốt trước khi chạy, không phải số bản
    # ghi mà vòng lặp tình cờ sinh ra.  Một ca chết vẫn phải hiện ra là not_run.
    registry = tuple(sorted(tuple(loaded.case_id_registry) + held.case_ids))
    scheduled_total = len(registry)
    matrix: list[dict[str, object]] = []
    for case in cases:
        try:
            matrix.append(_run_case(case, schemas[case.schema_path]))
        except Exception as exc:  # noqa: BLE001
            matrix.append(
                {
                    "case_id": case.case_id,
                    "schema_path": case.schema_path,
                    "semantic_group": case.semantic_group,
                    "kind": case.kind,
                    "expected_valid": case.expected_valid,
                    "status": "not_run",
                    "rc": None,
                    "passed": False,
                    "error": {"name": type(exc).__name__, "message": str(exc)},
                }
            )
    recorded_ids = {str(record["case_id"]) for record in matrix}
    missing_records = sorted(set(registry) - recorded_ids)
    unexpected_records = sorted(recorded_ids - set(registry))
    executed = sum(record.get("status") == "executed" for record in matrix)
    passed = sum(record.get("passed") is True for record in matrix)
    failed = sum(record.get("status") == "executed" and record.get("passed") is not True for record in matrix)
    skipped = sum(record.get("status") == "skipped" for record in matrix)
    not_run = scheduled_total - executed - skipped
    mutation = fake_validators.mutation_matrix(cases)
    # Bằng chứng DƯƠNG cho §8.4: mutant thuộc lòng phải chết, và phải chết BỞI ca
    # giữ lại.  "Đã giết đủ 5" thôi thì không phân biệt được phép giết thật với
    # một mutant chết vì lý do khác — reviewer attempt 3 đã bắt đúng chỗ đó.
    memorizer = next(
        (item for item in mutation["records"] if isinstance(item, Mapping) and item.get("fake_id") == "exact_hash_only"),
        None,
    )
    memorizer_affected = sorted(memorizer.get("affected_case_ids") or []) if isinstance(memorizer, Mapping) else []
    memorizer_killed_by_heldout = (
        isinstance(memorizer, Mapping)
        and memorizer.get("disposition") == "killed"
        and bool(memorizer_affected)
        and set(memorizer_affected) <= heldout_case_ids
    )
    ok = (
        scheduled_total > 0
        and not missing_records
        and not unexpected_records
        and executed == scheduled_total
        and passed == scheduled_total
        and failed == skipped == not_run == 0
        and mutation["ok"] is True
        and mutation["killed"] == mutation["total"] == len(FAKE_VALIDATOR_IDS)
        and memorizer_killed_by_heldout
    )
    resource_classification = {
        run.get("run_id"): (run.get("required_counterexamples") or {}).get("resource_classes")
        for run in runner_report_value["runs"]
        if isinstance(run, Mapping)
    }
    raw_process_rc = {
        record["case_id"]: record.get("rc") for record in matrix
    }
    timeout_report = {
        run.get("run_id"): {
            item.get("test_id"): (item.get("result") or {}).get("termination")
            for item in run.get("tests", [])
            if isinstance(item, Mapping)
        }
        for run in runner_report_value["runs"]
        if isinstance(run, Mapping)
    }
    report = {
        "schema_version": 1,
        "ok": ok,
        "authority": authority_value,
        "observations_recorded_not_sealed": recorded_observations,
        "candidate_head": candidate_head,
        "candidate_tree": source_binding["candidate_tree"],
        "trusted_source_inventory_sha256": source_binding["trusted_source_inventory_sha256"],
        "target_checkout": target_observation,
        "schema_count": len(schemas),
        "schema_paths": list(schemas),
        "keyword_count": len(all_keywords),
        "keyword_inventory": sorted(all_keywords),
        "keyword_anchors": anchors,
        "keyword_controls": controls,
        "corpus_sha256": corpus_sha,
        "corpus_locator": PINNED_CORPUS_PATH,
        "corpus_supplied_externally": external_copy,
        "corpus_reorder_seed": loaded.reorder_seed,
        "public_case_ids": list(loaded.case_id_registry),
        "public_case_count": len(loaded.case_id_registry),
        "heldout": {
            "locator": held.path,
            "sha256": held.sha256,
            "produced_by": held.produced_by,
            "source": held.source,
            "case_ids": list(held.case_ids),
            "case_count": len(held.case_ids),
            "label_counts": dict(held.label_counts),
            "reorder_seed": held.reorder_seed,
            "disjoint_from_public_corpus": True,
            "memorizer_killed_by_heldout": memorizer_killed_by_heldout,
            "memorizer_mismatched_case_ids": memorizer_affected,
        },
        "combined_reorder_seed": combined_reorder_seed,
        "case_id_registry": list(registry),
        "scheduled_total": scheduled_total,
        "executed": executed,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "not_run": not_run,
        "missing_case_records": missing_records,
        "unexpected_case_records": unexpected_records,
        "case_matrix": matrix,
        "independent_engine": engine_metadata,
        "fake_validators": mutation,
        "sandbox_report_sha256": runner_observation["sandbox_report_sha256"],
        "runner_fingerprint_sha256": runner_observation["runner_fingerprint_sha256"],
    }
    if not ok:
        raise OracleError(
            "oracle case or mutation matrix is red: scheduled=%d executed=%d passed=%d failed=%d "
            "not_run=%d missing=%s mutation_ok=%s memorizer_killed_by_heldout=%s memorizer_mismatches=%s"
            % (
                scheduled_total,
                executed,
                passed,
                failed,
                not_run,
                missing_records,
                mutation["ok"],
                memorizer_killed_by_heldout,
                memorizer_affected,
            )
        )

    destination = pathlib.Path(output_root)
    if destination.exists() and any(destination.iterdir()):
        raise OracleError("output_root must be absent or empty")
    artifact_set = artifacts.ArtifactSet(destination, "candidate-%s" % candidate_head)
    artifact_set.add(
        "source",
        "trusted-source-and-authority.json",
        json.dumps({"source_binding": source_binding, "authority": authority_value}, ensure_ascii=False, sort_keys=True) + "\n",
    )
    artifact_set.add(
        "source",
        "target-schema-pin.json",
        json.dumps({"target_pin": dict(target_pin), "measured": target_observation}, ensure_ascii=False, sort_keys=True) + "\n",
    )
    artifact_set.add(
        "source",
        "protocol-source.json",
        json.dumps(protocol, ensure_ascii=False, sort_keys=True) + "\n",
    )
    # R1: giữ lại CHÍNH BYTE của năm schema target.  Attempt 2 không giữ, nên khi
    # ref biến mất thì không ai đối chiếu lại được bằng chứng nào.
    for relative, data in raw_schema_bytes.items():
        artifact_set.add("source", "target-schemas/%s" % relative.rsplit("/", 1)[-1], data)
    artifact_set.add("corpus", "corpus.json", corpus_raw)
    # Giữ lại BYTE của bộ ca giữ lại: bí mật chỉ cần thiết TRONG lúc chấm, còn
    # bằng chứng sau đó phải tái lập được, nếu không thì "34 + N ca" lại là lời khai.
    artifact_set.add("corpus", "heldout-corpus.json", held.raw)
    artifact_set.add("per_case_matrix", "oracle-matrix.json", json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n")
    artifact_set.add(
        "per_case_matrix",
        "raw-process-rc.json",
        json.dumps(raw_process_rc, ensure_ascii=False, sort_keys=True) + "\n",
    )
    artifact_set.add("runner_env_digest", "sandbox-runner-report.json", runner_report_raw)
    artifact_set.add(
        "runner_env_digest",
        "resource-classification.json",
        json.dumps(resource_classification, ensure_ascii=False, sort_keys=True) + "\n",
    )
    artifact_set.add(
        "runner_env_digest",
        "timeout-report.json",
        json.dumps(timeout_report, ensure_ascii=False, sort_keys=True) + "\n",
    )
    cleanup_records = [
        {
            "run_id": run["run_id"],
            "cleanup": {
                test["test_id"]: test["result"]["cleanup"]
                for test in run["tests"]
                if isinstance(test.get("result"), dict)
            },
        }
        for run in runner_report_value["runs"]
    ]
    artifact_set.add("cleanup_record", "cleanup-records.json", json.dumps(cleanup_records, sort_keys=True) + "\n")
    artifact_set.finalize()
    verification = artifacts.verify(destination)
    if verification.get("ok") is not True:
        raise OracleError("retained artifact verification failed: %s" % verification)
    report["retention"] = verification
    report["retention_root"] = str(destination.resolve())
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-worker", nargs=2, metavar=("REQUEST", "RESULT"))
    args = parser.parse_args(argv)
    if args.case_worker:
        return _case_worker(pathlib.Path(args.case_worker[0]), pathlib.Path(args.case_worker[1]))
    print("oracle.py must be entered through source_pin.py after external pin verification", file=sys.stderr)
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
