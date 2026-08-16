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

from core.artifacts import ArtifactSet, verify as verify_artifacts  # noqa: E402

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


def command_produce(out: str, run_id: str) -> int:
    """Write the retained artifact set for one run and seal it.

    Every category §8 names has a home here.  ``finalize`` refuses to seal a manifest that is missing
    a required category, so a run that failed to collect its cleanup record cannot produce a sealed,
    green-looking artifact set.
    """
    from launcher.selftest import run_matrix

    matrix = run_matrix()
    artifacts = ArtifactSet(out, run_id)

    artifacts.add(
        "source",
        "launcher_inventory.json",
        json.dumps(
            inventory_module.build_inventory(HERE, REPOSITORY_ROOT),
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n",
    )
    artifacts.add(
        "source",
        "static_boundary_scan.json",
        json.dumps(inventory_module.scan_package(HERE), ensure_ascii=False, sort_keys=True, indent=2)
        + "\n",
    )
    artifacts.add(
        "corpus",
        "case_registry.json",
        json.dumps(
            {
                "cases": dict(registry_module.CASES),
                "required_checks": list(registry_module.REQUIRED_CHECKS),
                "platform_specific": dict(registry_module.PLATFORM_SPECIFIC),
                "coverage": registry_module.check_coverage(),
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n",
    )
    artifacts.add(
        "per_case_matrix",
        "case_matrix.json",
        json.dumps(matrix, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    )
    artifacts.add(
        "per_case_matrix",
        "parity_report.json",
        json.dumps(matrix["parity"], ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    )
    artifacts.add(
        "runner_env_digest",
        "runner_fingerprint.json",
        json.dumps(
            {
                "primary": _runner_fingerprint(),
                "delegated": matrix.get("delegation", {}).get("runner"),
                "environment_names": matrix.get("environment_names", []),
                "values_recorded": False,
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n",
    )
    artifacts.add(
        "cleanup_record",
        "watchdog_cleanup.json",
        json.dumps(matrix.get("cleanup_records", []), ensure_ascii=False, sort_keys=True, indent=2)
        + "\n",
    )
    artifacts.add(
        "cleanup_record",
        "delegation_receipt.json",
        json.dumps(matrix.get("delegation", {}), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    )
    manifest = artifacts.finalize()
    _emit(
        {
            "run_id": run_id,
            "run_root": os.path.abspath(out),
            "entries": len(artifacts.entries),
            "manifest": manifest,
            "matrix_ok": matrix["ok"],
            "produced_at_is_recorded": False,
        }
    )
    return RC_OK if matrix["ok"] else RC_VERIFY_RED


def command_verify(root: str) -> int:
    result = verify_artifacts(root)
    _emit(result)
    return RC_OK if result.get("ok") else RC_VERIFY_RED


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
            return command_verify(args.root)
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
