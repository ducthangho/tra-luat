"""Direct and behavioural oracle driven only by pinned external data."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tempfile
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from core import artifacts  # noqa: E402
from oracle import authority, corpus, engine, fake_validators  # noqa: E402
from oracle.trusted_inventory import (  # noqa: E402
    FAKE_VALIDATOR_IDS,
    PROTOCOL_SCHEMA_PATHS,
    REQUIRED_ESCAPE_KEYS,
    REQUIRED_RESOURCE_KEYS,
    SANDBOX_TEST_IDS,
    TRUSTED_SOURCE_PATHS,
)

PROTOCOL_SOURCE_PATH = "docs/PROTOCOL_DA_PHIEN.md"
OID40 = re.compile(r"[0-9a-f]{40}\Z")


class OracleError(RuntimeError):
    """A trusted input, engine, evidence, or retention invariant failed."""


def _git(root: pathlib.Path, *args: str, binary: bool = False):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    if proc.returncode != 0:
        stderr = proc.stderr if isinstance(proc.stderr, str) else proc.stderr.decode("utf-8", "replace")
        raise OracleError("git %s failed rc=%d: %s" % (" ".join(args), proc.returncode, stderr.strip()))
    return proc.stdout


def _read_regular(path: pathlib.Path, label: str, require_readonly: bool = False) -> bytes:
    try:
        before = path.lstat()
    except OSError as exc:
        raise OracleError("%s cannot be inspected: %s" % (label, exc)) from exc
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode) or before.st_nlink != 1:
        raise OracleError("%s must be a single-link regular non-symlink file" % label)
    if require_readonly and before.st_mode & 0o222:
        raise OracleError("%s must be sealed read-only" % label)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as handle:
        opened = os.fstat(handle.fileno())
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise OracleError("%s changed identity while opening" % label)
        return handle.read()


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


def _target_observation(target_root: pathlib.Path) -> tuple[dict[str, object], dict[str, Mapping[str, object]]]:
    root = target_root.resolve()
    top = pathlib.Path(str(_git(root, "rev-parse", "--show-toplevel")).strip()).resolve()
    if top != root:
        raise OracleError("target_root is not the exact Git top-level")
    head = str(_git(root, "rev-parse", "HEAD")).strip()
    tree = str(_git(root, "rev-parse", "HEAD^{tree}")).strip()
    if not OID40.fullmatch(head) or not OID40.fullmatch(tree):
        raise OracleError("target checkout head/tree is not a full lowercase Git oid")
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
    schemas = {}
    for relative in PROTOCOL_SCHEMA_PATHS:
        entry = _blob_binding(root, head, relative)
        schema = _strict_json(entry.pop("raw"), relative)
        if not isinstance(schema, dict):
            raise OracleError("schema is not an object: %s" % relative)
        entries.append(entry)
        schemas[relative] = schema
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    observation = {
        "head": head,
        "tree": tree,
        "schema_paths": list(PROTOCOL_SCHEMA_PATHS),
        "schema_inventory_sha256": hashlib.sha256(canonical).hexdigest(),
    }
    return observation, schemas


def _engine_metadata() -> dict[str, object]:
    import jsonschema

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
    return {
        "name": "python-jsonschema",
        "version": importlib.metadata.version("jsonschema"),
        "digest_sha256": digest.hexdigest(),
        "implementation_files": len(files),
        "dialect": "https://json-schema.org/draft/2020-12/schema",
    }


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
    except Exception as exc:
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
            "rc": proc.returncode,
            "passed": passed,
            "typed_result": typed,
            "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(proc.stderr).hexdigest(),
        }


def _read_durable_facts(path: pathlib.Path) -> dict[str, object]:
    value = _strict_json(_read_regular(path, "durable facts", require_readonly=True), "durable facts")
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise OracleError("durable facts must be a schema_version 1 object")
    if set(value) != {"schema_version", "mission", "packet"}:
        raise OracleError("durable facts must contain exactly mission and packet blocks")
    return {"mission": value["mission"], "packet": value["packet"]}


def _runner_observation(path: pathlib.Path, candidate_head: str, inventory_digest: str) -> tuple[dict[str, object], object, bytes]:
    raw = _read_regular(path, "sandbox report", require_readonly=True)
    value = _strict_json(raw, "sandbox report")
    if not isinstance(value, dict) or value.get("ok") is not True:
        raise OracleError("sandbox report is not green")
    if value.get("repeat_requested") < 8 or value.get("repeat_executed") != value.get("repeat_requested"):
        raise OracleError("sandbox report lacks at least eight completed standalone runs")
    if value.get("same_scheduled_test_ids") is not True or value.get("stable_classifications") is not True:
        raise OracleError("sandbox repeated runs are unstable")
    runs = value.get("runs")
    if not isinstance(runs, list) or not runs:
        raise OracleError("sandbox report has no run records")
    fingerprints = []
    for run in runs:
        if not isinstance(run, dict) or run.get("ok") is not True:
            raise OracleError("sandbox run is not green")
        if run.get("candidate_head") != candidate_head:
            raise OracleError("sandbox run candidate head mismatch")
        binding = run.get("candidate_source_binding")
        if not isinstance(binding, dict) or binding.get("trusted_source_inventory_sha256") != inventory_digest:
            raise OracleError("sandbox run trusted source digest mismatch")
        if run.get("scheduled_test_ids") != list(SANDBOX_TEST_IDS):
            raise OracleError("sandbox scheduled test IDs mismatch")
        if not (
            run.get("scheduled_total") == run.get("executed") == run.get("passed") == len(SANDBOX_TEST_IDS)
            and run.get("failed") == run.get("skipped") == run.get("not_run") == 0
        ):
            raise OracleError("sandbox run accounting is not honest N/N")
        required = run.get("required_counterexamples")
        if not isinstance(required, dict):
            raise OracleError("sandbox required counterexample matrix missing")
        escape = required.get("sandbox_escape_classes")
        resources = required.get("resource_classes")
        if not isinstance(escape, dict) or set(escape) != set(REQUIRED_ESCAPE_KEYS):
            raise OracleError("sandbox escape keys mismatch")
        if not isinstance(resources, dict) or set(resources) != set(REQUIRED_RESOURCE_KEYS):
            raise OracleError("sandbox resource keys mismatch")
        for item in list(escape.values()) + list(resources.values()):
            if not isinstance(item, dict) or item.get("passed") is not True or item.get("rc") is None or not item.get("evidence"):
                raise OracleError("sandbox counterexample lacks real rc or evidence")
        healthy = next(item for item in run["tests"] if item["test_id"] == "healthy_positive_control")
        fingerprints.append(healthy["result"]["fingerprint"])
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


def evaluate(
    *,
    repo_root: str,
    candidate_head: str,
    authority_bundle: str,
    durable_facts: str,
    target_root: str,
    corpus_path: str,
    sandbox_report: str,
    output_root: str,
    source_binding: Mapping[str, object],
) -> dict[str, object]:
    root = pathlib.Path(repo_root).resolve()
    if source_binding.get("candidate_head") != candidate_head:
        raise OracleError("pre-import source binding candidate mismatch")
    target_observation, schemas = _target_observation(pathlib.Path(target_root))
    protocol = _protocol_observation(root, candidate_head)
    facts = _read_durable_facts(pathlib.Path(durable_facts))
    corpus_raw = _read_regular(pathlib.Path(corpus_path), "corpus", require_readonly=True)
    corpus_sha = hashlib.sha256(corpus_raw).hexdigest()
    runner_observation, runner_report_value, runner_report_raw = _runner_observation(
        pathlib.Path(sandbox_report), candidate_head, str(source_binding["trusted_source_inventory_sha256"])
    )
    observations = {
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
        **runner_observation,
    }
    authority_value = authority.load_and_verify(authority_bundle, observations)
    cases, anchors, reorder_seed, _digest = corpus.load(
        corpus_path, corpus_sha, PROTOCOL_SCHEMA_PATHS
    )

    all_keywords = set()
    shape_errors = {}
    schema_keywords = {}
    for path, schema in schemas.items():
        errors = engine.schema_shape_errors(schema)
        if errors:
            shape_errors[path] = errors
        schema_keywords[path] = engine.keyword_inventory(schema)
        all_keywords.update(schema_keywords[path])
    missing_anchors = sorted(all_keywords - set(anchors))
    extra_anchors = sorted(set(anchors) - all_keywords)
    controls = engine.keyword_controls(sorted(all_keywords))
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

    matrix = [_run_case(case, schemas[case.schema_path]) for case in cases]
    passed = sum(record["passed"] is True for record in matrix)
    mutation = fake_validators.mutation_matrix(cases)
    engine_metadata = _engine_metadata()
    ok = (
        bool(matrix)
        and passed == len(matrix)
        and mutation["ok"] is True
        and mutation["killed"] == mutation["total"] == len(FAKE_VALIDATOR_IDS)
    )
    report = {
        "schema_version": 1,
        "ok": ok,
        "authority": authority_value,
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
        "corpus_reorder_seed": reorder_seed,
        "scheduled_total": len(matrix),
        "executed": len(matrix),
        "passed": passed,
        "failed": len(matrix) - passed,
        "skipped": 0,
        "not_run": 0,
        "case_matrix": matrix,
        "independent_engine": engine_metadata,
        "fake_validators": mutation,
        "sandbox_report_sha256": runner_observation["sandbox_report_sha256"],
        "runner_fingerprint_sha256": runner_observation["runner_fingerprint_sha256"],
    }
    if not ok:
        raise OracleError("oracle case or mutation matrix is red")

    destination = pathlib.Path(output_root)
    if destination.exists() and any(destination.iterdir()):
        raise OracleError("output_root must be absent or empty")
    artifact_set = artifacts.ArtifactSet(destination, "candidate-%s" % candidate_head)
    artifact_set.add("source", "trusted-source-and-authority.json", json.dumps({"source_binding": source_binding, "authority": authority_value}, ensure_ascii=False, sort_keys=True) + "\n")
    artifact_set.add("corpus", "corpus.json", corpus_raw)
    artifact_set.add("per_case_matrix", "oracle-matrix.json", json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n")
    artifact_set.add("runner_env_digest", "sandbox-runner-report.json", runner_report_raw)
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
