"""Typed fake-validator mutation protocol with real child return codes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))
from oracle.trusted_inventory import FAKE_VALIDATOR_IDS  # noqa: E402

PROTOCOL_VERSION = 1


def _worker(fake_id: str, request_path: pathlib.Path, result_path: pathlib.Path) -> int:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    cases = request.get("cases", [])
    if fake_id == "stderr_forger_control":
        print("FileNotFoundError: printed by an untrusted validator", file=sys.stderr)
        return 19
    if fake_id == "stdout_forger":
        print(json.dumps({"protocol_version": PROTOCOL_VERSION, "results": [], "ok": True}))
        return 0
    results = []
    for index, case in enumerate(cases):
        case_id = case.get("case_id")
        if fake_id == "always_pass":
            valid = True
        elif fake_id == "always_fail":
            valid = False
        elif fake_id == "exact_hash_only":
            if index >= max(1, len(cases) // 2):
                continue
            digest = hashlib.sha256(
                json.dumps(case.get("document"), sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).digest()
            valid = bool(digest[0] & 1)
        elif fake_id == "path_aware_detector":
            valid = bool(case.get("schema_path"))
        else:
            return 64
        results.append({"case_id": case_id, "valid": valid})
    result_path.write_text(
        json.dumps(
            {"protocol_version": PROTOCOL_VERSION, "fake_id": fake_id, "results": results},
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


def _case_fields(case: object) -> tuple[str, object, bool]:
    if isinstance(case, Mapping):
        return str(case["case_id"]), case.get("document"), bool(case["expected_valid"])
    return str(getattr(case, "case_id")), getattr(case, "document"), bool(getattr(case, "expected_valid"))


def run_one(fake_id: str, cases: Sequence[object], timeout_seconds: float = 5.0) -> dict[str, object]:
    expected = {}
    request_cases = []
    for case in cases:
        case_id, document, expected_valid = _case_fields(case)
        expected[case_id] = expected_valid
        request_cases.append({"case_id": case_id, "document": document})
    if not expected or not any(expected.values()) or all(expected.values()):
        return {
            "fake_id": fake_id,
            "disposition": "anchor_missing",
            "real_rc": None,
            "affected_case_ids": sorted(expected),
            "evidence": "both valid and invalid blind cases are required",
        }
    with tempfile.TemporaryDirectory(prefix="ra02-fake-") as tmp:
        root = pathlib.Path(tmp)
        request = root / "request.json"
        result = root / "result.json"
        request.write_text(
            json.dumps({"protocol_version": PROTOCOL_VERSION, "cases": request_cases}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        env = {
            key: value
            for key, value in os.environ.items()
            if key in ("PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "TEMP", "TMP", "LANG")
        }
        try:
            proc = subprocess.run(
                [sys.executable, str(pathlib.Path(__file__).resolve()), "--worker", fake_id, str(request), str(result)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                env=env,
            )
        except FileNotFoundError as exc:
            return {"fake_id": fake_id, "disposition": "fixture_gap", "real_rc": None, "affected_case_ids": sorted(expected), "evidence": str(exc)}
        except subprocess.TimeoutExpired as exc:
            return {"fake_id": fake_id, "disposition": "masked", "real_rc": None, "affected_case_ids": sorted(expected), "evidence": "trusted watchdog timeout: %s" % exc}
        record: dict[str, object] = {
            "fake_id": fake_id,
            "real_rc": proc.returncode,
            "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(proc.stderr).hexdigest(),
            "typed_result_present": result.is_file(),
            "affected_case_ids": [],
        }
        if proc.returncode != 0:
            record["disposition"] = "masked"
            record["affected_case_ids"] = sorted(expected)
            record["evidence"] = "validator process exited nonzero; stderr content is not classified"
            return record
        if not result.is_file():
            record["disposition"] = "killed"
            record["affected_case_ids"] = sorted(expected)
            record["evidence"] = "typed result artifact missing; stdout cannot substitute"
            return record
        try:
            typed = json.loads(result.read_text(encoding="utf-8"))
            predictions = typed["results"]
            if typed.get("protocol_version") != PROTOCOL_VERSION or not isinstance(predictions, list):
                raise ValueError("protocol shape mismatch")
            by_id = {
                item["case_id"]: item["valid"]
                for item in predictions
                if isinstance(item, dict) and type(item.get("valid")) is bool
            }
            if len(by_id) != len(predictions) or set(by_id) != set(expected):
                raise ValueError("result IDs are missing, duplicate, or unexpected")
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            record["disposition"] = "killed"
            predictions_value = locals().get("predictions")
            present_ids = set()
            if isinstance(predictions_value, list):
                present_ids = {
                    item.get("case_id")
                    for item in predictions_value
                    if isinstance(item, dict)
                    and item.get("case_id") in expected
                    and type(item.get("valid")) is bool
                }
            record["affected_case_ids"] = sorted(set(expected) - present_ids) or sorted(expected)
            record["evidence"] = "typed result rejected: %s" % exc
            return record
        mismatches = [case_id for case_id in sorted(expected) if by_id[case_id] is not expected[case_id]]
        record["disposition"] = "killed" if mismatches else "survived"
        record["mismatched_case_ids"] = mismatches
        record["affected_case_ids"] = mismatches
        record["evidence"] = "blind per-case comparison"
        return record


def mutation_matrix(cases: Sequence[object]) -> dict[str, object]:
    records = [run_one(fake_id, cases) for fake_id in FAKE_VALIDATOR_IDS]
    return {
        "fake_validator_ids": list(FAKE_VALIDATOR_IDS),
        "records": records,
        "killed": sum(record["disposition"] == "killed" for record in records),
        "total": len(records),
        "ok": bool(records) and all(record["disposition"] == "killed" for record in records),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", nargs=3, metavar=("FAKE_ID", "REQUEST", "RESULT"))
    args = parser.parse_args(argv)
    if args.worker:
        return _worker(args.worker[0], pathlib.Path(args.worker[1]), pathlib.Path(args.worker[2]))
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
