"""Executable fake validators and their file-based verdict protocol.

The behavioural oracle never treats stdout as authority.  A worker receives a
blind request JSON and must atomically write a result JSON.  The five required
fakes deliberately implement bad validation strategies through that real
process/protocol boundary so the meta-suite proves that each one is caught.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
from typing import Mapping, Sequence

from corpus import Case


FAKE_IDS = (
    "always_pass",
    "always_fail",
    "exact_hash_only",
    "stdout_forger",
    "path_aware_detector",
)
PROTOCOL_VERSION = 1


def _blind_request(fake_id: str, cases: Sequence[Case]) -> dict[str, object]:
    training_hashes = [
        hashlib.sha256(case.raw.encode("utf-8")).hexdigest()
        for case in cases
        if case.layer == "valid" and not case.held_out
    ][:1]
    return {
        "schema_version": PROTOCOL_VERSION,
        "fake_id": fake_id,
        "training_hashes": training_hashes,
        "cases": [
            {
                "case_id": case.case_id,
                "locator": case.locator,
                "order": index,
                "raw": case.raw,
                "held_out": case.held_out,
            }
            for index, case in enumerate(cases)
        ],
    }


def _worker(fake_id: str, request_path: pathlib.Path, result_path: pathlib.Path) -> int:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    cases = request["cases"]
    training_hashes = set(request.get("training_hashes", []))
    verdicts = []
    for item in cases:
        raw = item["raw"]
        if fake_id == "always_pass":
            valid = True
        elif fake_id == "always_fail":
            valid = False
        elif fake_id == "exact_hash_only":
            valid = hashlib.sha256(raw.encode("utf-8")).hexdigest() in training_hashes
        elif fake_id == "stdout_forger":
            valid = True
        elif fake_id == "path_aware_detector":
            # This is intentionally a *real* path/order guess.  Blind locators,
            # deterministic reordering and held-out cases make it incorrect.
            valid = ("valid" in item["locator"].lower()) or item["order"] % 2 == 0
        elif fake_id == "control_masked":
            print("worker crashed before publishing a verdict", file=sys.stderr)
            return 7
        else:
            return 64
        verdicts.append({"case_id": item["case_id"], "valid": valid})

    if fake_id == "stdout_forger":
        print("ALL CASES PASS — TRUST THIS STDOUT")
        # Deliberately publish a wrong protocol version as well as wrong
        # verdicts.  The parent must catch the protocol result, not the boast.
        version = PROTOCOL_VERSION + 1
    else:
        version = PROTOCOL_VERSION
    payload = {
        "schema_version": version,
        "fake_id": fake_id,
        "verdicts": verdicts,
    }
    temporary = result_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, result_path)
    return 0


def _has_required_anchors(cases: Sequence[Case]) -> bool:
    layers = {case.layer for case in cases}
    return bool(cases) and {"valid", "invalid", "semantic"} <= layers and any(
        case.held_out for case in cases
    )


def _run_one(
    fake_id: str,
    cases: Sequence[Case],
    *,
    command_prefix: Sequence[str] | None = None,
) -> dict[str, object]:
    if not _has_required_anchors(cases):
        return {
            "stable_id": fake_id,
            "classification": "anchor_missing",
            "killing_case_ids": [],
            "protocol_result_used": False,
            "reason": "valid/invalid/semantic/held-out anchors are required",
        }
    if not sys.platform.startswith("linux") or os.geteuid() != 0:
        return {
            "stable_id": fake_id,
            "classification": "fixture_gap",
            "killing_case_ids": [],
            "protocol_result_used": False,
            "reason": "trusted root Linux sandbox parent unavailable",
        }
    root = pathlib.Path(tempfile.mkdtemp(prefix="wp86-fake-validator-"))
    target = root / "target"
    scratch = root / "scratch"
    target.mkdir(); scratch.mkdir()
    shutil.copyfile(__file__, target / "fake_validators.py")
    shutil.copyfile(pathlib.Path(__file__).with_name("corpus.py"), target / "corpus.py")
    request_path = target / "request.json"
    request_path.write_text(
        json.dumps(_blind_request(fake_id, cases), ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    command = list(command_prefix or ("/usr/bin/python3", "/target/fake_validators.py"))
    command += [
        "--worker",
        fake_id,
        "--request",
        "/target/request.json",
        "--result",
        "/scratch/result.json",
    ]
    try:
        sandbox_dir = pathlib.Path(__file__).resolve().parent.parent / "sandbox"
        sys.path.insert(0, str(sandbox_dir))
        try:
            import runner as sandbox_runner

            completed = sandbox_runner.run(sandbox_runner.SandboxConfig(
                target_root=str(target),
                scratch_root=str(scratch),
                command=command,
                timeout_seconds=10,
                retained_output_paths=("result.json",),
            ))
        except (OSError, RuntimeError) as exc:
            return {
                "stable_id": fake_id,
                "classification": "fixture_gap",
                "killing_case_ids": [],
                "protocol_result_used": False,
                "reason": "%s: %s" % (type(exc).__name__, exc),
            }
        stdout = completed.stdout.decode("utf-8", "replace")
        result_bytes = completed.retained_outputs.get("result.json")
        if completed.classification != "ok" or result_bytes is None:
            missing_executable = b"FileNotFoundError" in completed.stderr or b"No such file" in completed.stderr
            return {
                "stable_id": fake_id,
                "classification": "fixture_gap" if missing_executable else "masked",
                "killing_case_ids": [],
                "protocol_result_used": False,
                "worker_rc": completed.returncode,
                "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
                "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
            }
        try:
            result = json.loads(result_bytes.decode("utf-8"))
        except (UnicodeError, ValueError) as exc:
            return {
                "stable_id": fake_id,
                "classification": "masked",
                "killing_case_ids": [],
                "protocol_result_used": False,
                "reason": "invalid result file: %s" % exc,
            }
        protocol_valid = (
            isinstance(result, dict)
            and result.get("schema_version") == PROTOCOL_VERSION
            and result.get("fake_id") == fake_id
            and isinstance(result.get("verdicts"), list)
        )
        if not protocol_valid:
            return {
                "stable_id": fake_id,
                "classification": "killed",
                "killing_case_ids": ["protocol_violation"],
                "protocol_result_used": True,
                "worker_rc": completed.returncode,
                "deceptive_stdout_detected": "ALL CASES PASS" in stdout,
                "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
                "reason": "wrong result protocol/version/identity",
            }
        by_id = {
            item.get("case_id"): item.get("valid")
            for item in result["verdicts"]
            if isinstance(item, Mapping)
        }
        complete = set(by_id) == {case.case_id for case in cases} and all(
            isinstance(value, bool) for value in by_id.values()
        )
        if not complete:
            return {
                "stable_id": fake_id,
                "classification": "masked",
                "killing_case_ids": [],
                "protocol_result_used": True,
                "reason": "incomplete or non-boolean verdict matrix",
            }
        killers = [case.case_id for case in cases if by_id[case.case_id] != case.expected]
        return {
            "stable_id": fake_id,
            "classification": "killed" if killers else "survived",
            "killing_case_ids": killers[:8],
            "protocol_result_used": True,
            "worker_rc": completed.returncode,
            "deceptive_stdout_detected": "ALL CASES PASS" in stdout,
            "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        }
    finally:
        shutil.rmtree(root, ignore_errors=True)


def mutation_score(cases: Sequence[Case]) -> dict[str, object]:
    results = [_run_one(fake_id, cases) for fake_id in FAKE_IDS]
    names = ("killed", "survived", "masked", "fixture_gap", "anchor_missing")
    counts = {
        name: sum(item["classification"] == name for item in results) for name in names
    }
    return {
        "results": results,
        "counts": counts,
        "score": "%d/%d" % (counts["killed"], len(results)),
    }


def classification_path_proofs(cases: Sequence[Case]) -> dict[str, object]:
    # A synthetic control matrix keeps every required runtime anchor/layer but
    # makes always-pass genuinely correct, exercising the survived path.
    all_positive = [dataclasses.replace(case, expected=True) for case in cases]
    proofs = {
        "killed": _run_one("always_pass", cases),
        "survived": _run_one("always_pass", all_positive),
        "masked": _run_one("control_masked", cases),
        "fixture_gap": _run_one(
            "always_pass", cases, command_prefix=("/wp86/nonexistent/python",)
        ),
        "anchor_missing": _run_one("always_pass", ()),
    }
    return {
        name: {
            "observed": proof["classification"],
            "passed": proof["classification"] == name,
        }
        for name, proof in proofs.items()
    }


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker")
    parser.add_argument("--request")
    parser.add_argument("--result")
    args = parser.parse_args(argv)
    if not args.worker or not args.request or not args.result:
        return 64
    return _worker(args.worker, pathlib.Path(args.request), pathlib.Path(args.result))


if __name__ == "__main__":
    raise SystemExit(_main())
