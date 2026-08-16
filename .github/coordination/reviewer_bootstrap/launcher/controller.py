"""Command surface for the WP125 launcher, and the retained artifact set (Issue 125 §8).

This is the trusted side: it owns preflight, the claim, the deadline and the fence.  It is *not* the
privileged deployed controller — §3 is explicit that no reviewed head may hand a controller
executable to a privileged process, so everything here runs offline against the integrated RA-01
fake store and sealed fixtures.

Return codes follow the RA-01 convention so a caller can branch on them without parsing text::

    0   ok
    2   rejected (a named fail-closed category)
    3   verification red
    64  usage error

Artifacts are written through RA-01's :class:`~core.artifacts.ArtifactSet`, which supplies the
durable locator, the per-file SHA-256 and the sealed manifest plus sidecar.  Reusing it rather than
writing a fourth retention layer is deliberate: the categories it requires are the categories an
auditor already knows how to verify, and ``verify`` here is literally RA-01's ``verify``.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import platform
import sys

HERE = pathlib.Path(__file__).resolve().parent
BOOTSTRAP_ROOT = HERE.parent
if str(BOOTSTRAP_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOTSTRAP_ROOT))

from collections.abc import Mapping  # noqa: E402

from core.artifacts import ArtifactSet, verify as verify_artifacts  # noqa: E402
from oracle.safe_io import git as safe_git  # noqa: E402

from launcher import inventory as inventory_module  # noqa: E402
from launcher import parity as parity_module  # noqa: E402
from launcher import registry as registry_module  # noqa: E402
from launcher.environment import COVERAGE as ENVIRONMENT_COVERAGE  # noqa: E402
from launcher.errors import CATEGORIES, LauncherRejected  # noqa: E402

RC_OK = 0
RC_REJECTED = 2
RC_VERIFY_RED = 3
RC_USAGE = 64

REPOSITORY_ROOT = BOOTSTRAP_ROOT.parents[2]


def _emit(value: object) -> None:
    """UTF-8 regardless of the console code page — see ``launcher.selftest.emit`` for why."""
    import io

    stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    stream.write("\n")
    stream.flush()
    stream.detach()


def command_schema() -> int:
    """The machine-readable surface: commands, return codes, rejection categories, checks."""
    _emit(
        {
            "schema_version": 1,
            "packet": "wp125",
            "phase_key": "RA-04",
            "commands": ["schema", "coverage", "inventory", "produce", "verify", "selftest"],
            "return_codes": {
                "ok": RC_OK,
                "rejected": RC_REJECTED,
                "verify_red": RC_VERIFY_RED,
                "usage": RC_USAGE,
            },
            "rejection_categories": list(CATEGORIES),
            "required_checks": list(registry_module.REQUIRED_CHECKS),
            "write_prefix": inventory_module.LAUNCHER_PREFIX,
        }
    )
    return RC_OK


def command_coverage() -> int:
    """What is covered and — the part that matters — what is not."""
    scan = inventory_module.scan_package(HERE)
    _emit(
        {
            "registry": registry_module.check_coverage(),
            "static_boundary": {
                "scanned_files": scan["scanned_files"],
                "findings": scan["findings"],
                "coverage": scan["coverage"],
            },
            "environment": {key: list(value) for key, value in ENVIRONMENT_COVERAGE.items()},
            "platform_specific_cases": dict(registry_module.PLATFORM_SPECIFIC),
        }
    )
    return RC_OK


def command_inventory() -> int:
    _emit(inventory_module.build_inventory(HERE, REPOSITORY_ROOT))
    return RC_OK


def _runner_fingerprint() -> dict[str, object]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "os_name": os.name,
        "optimized": not __debug__,
    }


# WP125-RV-006.  Every retained-artifact class §8 names, as an explicit table.
#
# Generation 1 wrote eight files and relied on RA-01's five *categories* to police them.  Categories
# cannot express "the sealed source pin is present": a run that dropped the pin still satisfied
# `source`, because the inventory was also `source`.  So the manifest sealed cleanly while a class
# the contract requires was simply absent — the failure looked identical to success.
#
# This table is the missing denominator.  `verify` requires each locator by exact name and category,
# and re-reads each file to confirm the binding header inside it still names this run, this head and
# this tree.  Deletion is caught here; modification is caught by RA-01's per-file SHA-256; a file
# swapped between locators is caught by the binding header.
REQUIRED_ARTIFACTS: tuple[tuple[str, str, str], ...] = (
    ("launcher_inventory.json", "source", "wp125.launcher_inventory.v1"),
    ("static_boundary_scan.json", "source", "wp125.static_boundary_scan.v1"),
    ("sealed_source_pin.json", "source", "wp125.sealed_source_pin.v1"),
    ("authority_input.json", "source", "wp125.authority_input.v1"),
    ("argument_vector.json", "source", "wp125.argument_vector.v1"),
    ("case_registry.json", "corpus", "wp125.case_registry.v1"),
    ("case_matrix.json", "per_case_matrix", "wp125.case_matrix.v1"),
    ("parity_report.json", "per_case_matrix", "wp125.parity_report.v1"),
    ("runner_fingerprint.json", "runner_env_digest", "wp125.runner_fingerprint.v1"),
    ("environment_names.json", "runner_env_digest", "wp125.environment_names.v1"),
    ("return_codes.json", "cleanup_record", "wp125.return_codes.v1"),
    ("watchdog_timing.json", "cleanup_record", "wp125.watchdog_timing.v1"),
    ("watchdog_cleanup.json", "cleanup_record", "wp125.watchdog_cleanup.v1"),
    ("delegation_receipt.json", "cleanup_record", "wp125.delegation_receipt.v1"),
)

BINDING_KEYS = ("schema", "run_id", "head", "tree", "test_selection")


def _repo_identity() -> dict[str, str]:
    """Head and tree of the repository the artifacts describe, measured, not passed in."""

    def fail(message: str) -> RuntimeError:
        return RuntimeError(message)

    head = safe_git(REPOSITORY_ROOT, "rev-parse", "HEAD", error=fail).strip()
    tree = safe_git(REPOSITORY_ROOT, "rev-parse", "HEAD^{tree}", error=fail).strip()
    return {"head": head, "tree": tree}


def _bound(schema: str, run_id: str, identity: Mapping[str, str], test_selection, payload) -> str:
    """Wrap a payload in the binding header every retained class must carry."""
    document = {
        "schema": schema,
        "run_id": run_id,
        "head": identity["head"],
        "tree": identity["tree"],
        "test_selection": list(test_selection),
        "payload": payload,
    }
    return json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def command_produce(out: str, run_id: str) -> int:
    """Write the retained artifact set for one run and seal it.

    Every class §8 names has its own locator here, and every file carries the binding header, so a
    later ``verify`` can tell a complete set from a plausible-looking subset.
    """
    from launcher.selftest import run_matrix

    matrix = run_matrix()
    identity = _repo_identity()
    selection = sorted(registry_module.CASES)
    artifacts = ArtifactSet(out, run_id)

    def add(locator: str, category: str, schema: str, payload: object) -> None:
        artifacts.add(category, locator, _bound(schema, run_id, identity, selection, payload))

    add(
        "launcher_inventory.json",
        "source",
        "wp125.launcher_inventory.v1",
        inventory_module.build_inventory(HERE, REPOSITORY_ROOT),
    )
    add(
        "static_boundary_scan.json",
        "source",
        "wp125.static_boundary_scan.v1",
        inventory_module.scan_package(HERE),
    )
    add(
        "sealed_source_pin.json",
        "source",
        "wp125.sealed_source_pin.v1",
        matrix.get("sealed_source_pin", {}),
    )
    add(
        "authority_input.json",
        "source",
        "wp125.authority_input.v1",
        matrix.get("authority_input", {}),
    )
    add(
        "argument_vector.json",
        "source",
        "wp125.argument_vector.v1",
        matrix.get("argument_vector", {}),
    )
    add(
        "case_registry.json",
        "corpus",
        "wp125.case_registry.v1",
        {
            "cases": dict(registry_module.CASES),
            "required_checks": list(registry_module.REQUIRED_CHECKS),
            "platform_specific": dict(registry_module.PLATFORM_SPECIFIC),
            "coverage": registry_module.check_coverage(),
        },
    )
    add("case_matrix.json", "per_case_matrix", "wp125.case_matrix.v1", matrix)
    add("parity_report.json", "per_case_matrix", "wp125.parity_report.v1", matrix["parity"])
    add(
        "runner_fingerprint.json",
        "runner_env_digest",
        "wp125.runner_fingerprint.v1",
        {
            "primary": _runner_fingerprint(),
            "delegated": matrix.get("delegation", {}).get("runner"),
            "delegated_applicable": bool(matrix.get("delegation")),
        },
    )
    add(
        "environment_names.json",
        "runner_env_digest",
        "wp125.environment_names.v1",
        {"names": matrix.get("environment_names", []), "values_recorded": False},
    )
    add(
        "return_codes.json",
        "cleanup_record",
        "wp125.return_codes.v1",
        matrix.get("return_codes", {}),
    )
    add(
        "watchdog_timing.json",
        "cleanup_record",
        "wp125.watchdog_timing.v1",
        matrix.get("watchdog_timing", []),
    )
    add(
        "watchdog_cleanup.json",
        "cleanup_record",
        "wp125.watchdog_cleanup.v1",
        matrix.get("cleanup_records", []),
    )
    add(
        "delegation_receipt.json",
        "cleanup_record",
        "wp125.delegation_receipt.v1",
        matrix.get("delegation", {}),
    )

    manifest = artifacts.finalize()
    _emit(
        {
            "run_id": run_id,
            "run_root": os.path.abspath(out),
            "entries": len(artifacts.entries),
            "required_classes": len(REQUIRED_ARTIFACTS),
            "manifest": manifest,
            "matrix_ok": matrix["ok"],
            "produced_at_is_recorded": False,
        }
    )
    return RC_OK if matrix["ok"] else RC_VERIFY_RED


def verify_bindings(root: str, *, run_id: str | None = None) -> dict[str, object]:
    """Class completeness and binding integrity, on top of RA-01's hash verification."""
    run_root = pathlib.Path(root)
    manifest_path = run_root / "manifest.json"
    findings: list[dict[str, object]] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {
            "ok": False,
            "findings": [{"kind": "manifest_unreadable", "error": str(exc)}],
            "required_classes": len(REQUIRED_ARTIFACTS),
            "verified_classes": 0,
        }

    by_locator = {entry.get("locator"): entry for entry in manifest.get("entries", [])}
    identity = _repo_identity()
    verified = 0

    for locator, category, schema in REQUIRED_ARTIFACTS:
        entry = by_locator.get(locator)
        if entry is None:
            findings.append({"kind": "required_class_missing", "locator": locator, "schema": schema})
            continue
        if entry.get("category") != category:
            findings.append(
                {
                    "kind": "category_mismatch",
                    "locator": locator,
                    "expected": category,
                    "actual": entry.get("category"),
                }
            )
            continue
        try:
            document = json.loads((run_root / locator).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            findings.append({"kind": "class_unreadable", "locator": locator, "error": str(exc)})
            continue
        missing = [key for key in BINDING_KEYS if key not in document]
        if missing:
            findings.append(
                {"kind": "binding_incomplete", "locator": locator, "missing": missing}
            )
            continue
        if document["schema"] != schema:
            findings.append(
                {
                    "kind": "schema_mismatch",
                    "locator": locator,
                    "expected": schema,
                    "actual": document["schema"],
                }
            )
            continue
        if document["head"] != identity["head"] or document["tree"] != identity["tree"]:
            findings.append({"kind": "identity_mismatch", "locator": locator})
            continue
        if run_id is not None and document["run_id"] != run_id:
            findings.append({"kind": "run_mismatch", "locator": locator})
            continue
        if not document["test_selection"]:
            findings.append({"kind": "empty_test_selection", "locator": locator})
            continue
        verified += 1

    return {
        "ok": not findings,
        "findings": findings,
        "required_classes": len(REQUIRED_ARTIFACTS),
        "verified_classes": verified,
    }


def command_verify(root: str, run_id: str | None = None) -> int:
    result = verify_artifacts(root)
    bindings = verify_bindings(root, run_id=run_id)
    combined = dict(result)
    combined["bindings"] = bindings
    combined["ok"] = bool(result.get("ok")) and bool(bindings["ok"])
    _emit(combined)
    return RC_OK if combined["ok"] else RC_VERIFY_RED


def command_selftest() -> int:
    from launcher.selftest import main as selftest_main

    return selftest_main()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="launcher/controller.py", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("schema")
    sub.add_parser("coverage")
    sub.add_parser("inventory")
    produce = sub.add_parser("produce")
    produce.add_argument("--out", required=True)
    produce.add_argument("--run-id", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--root", required=True)
    verify.add_argument("--run-id", required=False, default=None)
    sub.add_parser("selftest")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return RC_USAGE
    try:
        if args.command == "schema":
            return command_schema()
        if args.command == "coverage":
            return command_coverage()
        if args.command == "inventory":
            return command_inventory()
        if args.command == "produce":
            return command_produce(args.out, args.run_id)
        if args.command == "verify":
            return command_verify(args.root, args.run_id)
        if args.command == "selftest":
            return command_selftest()
    except LauncherRejected as exc:
        _emit({"ok": False, "rejected": True, "category": exc.category, "message": str(exc)})
        return RC_REJECTED
    return RC_USAGE


# `datetime` is imported for the lease arithmetic that preflight fixtures build on; keeping the
# import here rather than inside a function documents that this module never stamps an artifact with
# the current time.  Timestamps are the one field guaranteed to differ between two runs, and the
# release-bundle determinism gate compares two runs byte for byte.
_ = datetime

if __name__ == "__main__":
    raise SystemExit(main())
