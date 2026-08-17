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

BINDING_KEYS = (
    "schema",
    "run_id",
    "head",
    "tree",
    "test_selection",
    "mission_plan_hash",
    "packet_spec_hash",
    "generation",
    "candidate_branch",
)

# WP125-RV-006-R5.  Every one of these used to be a literal written out here, beside a second copy in
# `launcher.selftest` and a third in the preflight expectations.  Three copies of one identity is
# three chances to drift, and round 4 duly drifted: the retained evidence carried the integration
# commit where the repair base belonged.  Round 5 kept the literals and merely added the pin beside
# them, which fixed nothing structural — a parallel constant table is still parallel when one of the
# tables is called a source pin.
#
# There is now exactly one table.  Everything below is *read from* it and nothing restates a value.
from launcher.sourcepin import PIN as SOURCE_PIN  # noqa: E402

MISSION_PLAN_HASH = SOURCE_PIN.mission_plan_hash
PACKET_SPEC_HASH = SOURCE_PIN.packet_spec_hash
GENERATION = SOURCE_PIN.packet_generation
CANDIDATE_BRANCH = SOURCE_PIN.candidate_ref.split("refs/heads/", 1)[-1]

PACKET_ISSUE = SOURCE_PIN.packet_issue
PACKET_REVISION = SOURCE_PIN.packet_revision
CANDIDATE_REF = SOURCE_PIN.candidate_ref
MISSION_ISSUE = SOURCE_PIN.mission_issue
MISSION_REVISION = SOURCE_PIN.mission_revision
PACKET_ATTEMPT = SOURCE_PIN.packet_attempt
LEASE_ID = SOURCE_PIN.lease_id
LEASE_EFFECTIVE_STOP_UTC = SOURCE_PIN.lease_effective_stop_utc

# WP125-RV-006-R2.  Round 2 checked the *wrapper*: generation, spec hash and branch in the binding
# header.  A payload carrying generation-1 fixture semantics inside a correct generation-2 header
# passed, because nothing looked past the header.  These walk the payload itself.
_G1_MARKERS = (
    "6cbc678ecdc36fdbda81a9c96d6921797e5d5e6d2467c03f26f95589d9f0c7f5",  # generation-1 spec hash
    "agent/wp125-g1-claude",
    "refs/heads/agent/wp125-g1-claude",
)


def _contains_stale_marker(payload: object) -> bool:
    """True when generation-1 identity appears anywhere inside the payload, at any depth."""
    if isinstance(payload, str):
        return any(marker in payload for marker in _G1_MARKERS)
    if isinstance(payload, Mapping):
        if payload.get("generation") in (1, "1"):
            return True
        return any(
            _contains_stale_marker(key) or _contains_stale_marker(value)
            for key, value in payload.items()
        )
    if isinstance(payload, (list, tuple)):
        return any(_contains_stale_marker(item) for item in payload)
    return False


def build_retained_identity(
    *,
    run_id: str,
    identity: Mapping[str, str],
    surface: object,
    runner: object,
    raw_outcomes: object,
) -> dict[str, object]:
    """The one retained identity document, assembled from the one pin plus this run's measurements."""
    return SOURCE_PIN.retained_identity(
        current_head=identity["head"],
        current_tree=identity["tree"],
        sole_parent=identity["sole_parent"],
        write_prefix=inventory_module.LAUNCHER_PREFIX,
        surface=surface,
        runner=runner,
        test_selection=sorted(registry_module.CASES),
        raw_outcomes=raw_outcomes,
        run_id=run_id,
        artifact_identity={
            "required_classes": len(REQUIRED_ARTIFACTS),
            "locators": sorted(locator for locator, _c, _s in REQUIRED_ARTIFACTS),
        },
    )


# The exact nested paths the retained identity must reproduce, and the value each one must hold.
# Expressed as data rather than as a wall of booleans because the round-5 finding was not that a
# comparison was wrong — it was that whole fields (repository, lease stop, integration observation)
# were *absent from the comparison*, which a list of hand-written `and`s hides and a total field
# walk cannot.  Anything the builder puts in the document and this table does not name would be
# unchecked, so :func:`_retained_identity_findings` walks the rebuilt document instead of this list
# and reports every leaf that disagrees.
_RUN_DEPENDENT_PATHS = (
    ("execution", "runner"),
    ("execution", "raw_outcomes"),
    ("execution", "surface"),
)


def _walk(document: object, prefix: tuple[str, ...] = ()) -> dict[tuple[str, ...], object]:
    """Flatten a nested document to leaf-path -> value, so two documents compare totally."""
    flat: dict[tuple[str, ...], object] = {}
    if isinstance(document, Mapping):
        for key, value in document.items():
            flat.update(_walk(value, prefix + (str(key),)))
        if not document:
            flat[prefix] = {}
        return flat
    flat[prefix] = document
    return flat


def _retained_identity_findings(
    payload: object, *, identity: Mapping[str, str], run_id: str | None
) -> list[dict[str, object]]:
    """Compare a retained identity payload, leaf for leaf, against the rebuilt expectation.

    WP125-RV-006-R5.  Round 5's predicate checked a hand-written list of fields and therefore proved
    exactly the fields somebody remembered to write down: the repository, the lease's absolute stop
    and the integration observation were all missing from it, and a nested payload that was valid but
    wrong verified green.  The comparison is now total in one direction — every leaf the builder
    produces must be present and equal — and the run-dependent leaves are the only exceptions, named
    above and checked separately for meaning rather than for value.
    """
    if not isinstance(payload, Mapping) or not payload:
        return [{"kind": "retained_identity_absent"}]

    expected = build_retained_identity(
        run_id=run_id if run_id is not None else str(payload.get("run", {}).get("run_id")),
        identity=identity,
        surface=None,
        runner=None,
        raw_outcomes=None,
    )
    want = _walk(expected)
    have = _walk(payload)
    findings: list[dict[str, object]] = []
    for path, value in sorted(want.items()):
        if path in _RUN_DEPENDENT_PATHS:
            continue
        if path not in have:
            findings.append({"kind": "retained_field_missing", "path": ".".join(path)})
        elif have[path] != value:
            findings.append({"kind": "retained_field_wrong", "path": ".".join(path)})

    # The run-dependent leaves are still required to *mean* something. An absent runner or an absent
    # outcome record is the empty-payload shape round 2 accepted under a correct wrapper.
    execution = payload.get("execution")
    if not isinstance(execution, Mapping):
        findings.append({"kind": "retained_execution_absent"})
        return findings
    if not execution.get("runner"):
        findings.append({"kind": "retained_runner_absent"})
    outcomes = execution.get("raw_outcomes")
    if not _matrix_is_green(outcomes):
        findings.append({"kind": "retained_outcomes_not_green"})
    if execution.get("surface") not in ("windows", "delegated_linux_run_test"):
        findings.append({"kind": "retained_surface_unknown"})
    return findings


def _is_oid(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and value == value.lower()
        and all(char in "0123456789abcdef" for char in value)
    )


def _nonempty(payload: object) -> bool:
    return bool(payload)


def _matrix_is_green(payload: object) -> bool:
    if not isinstance(payload, Mapping):
        return False
    return (
        bool(payload.get("ok"))
        and payload.get("failed") == 0
        and payload.get("skipped") == 0
        and payload.get("not_run") == 0
        and int(payload.get("passed") or 0) > 0
        and payload.get("passed") == payload.get("scheduled")
    )


def _delegation_is_real(payload: object) -> bool:
    """A delegation receipt must carry an executed test with a real return code, or nothing at all.

    An empty mapping used to satisfy the class; it now fails, because "we retained the delegation
    receipt" and "a delegated job ran" were being reported by the same green.
    """
    if not isinstance(payload, Mapping) or not payload:
        return False
    codes = payload.get("return_codes")
    if not (
        isinstance(codes, Mapping)
        and bool(codes)
        and all(isinstance(value, int) for value in codes.values())
        and int(payload.get("tests_executed") or 0) > 0
    ):
        return False
    # WP125-RV-008-R5.  The receipt has to say, in the retained artifact and not only in a case's
    # evidence, whether an authenticated Linux transport really ran or a controller-owned offline
    # double stood in for it.  §7 forbids the two from being reported by one green, and a receipt
    # that simply omits the question reports them by one green.
    transport = payload.get("linux_transport")
    return (
        isinstance(transport, Mapping)
        and transport.get("transport_invoked") is True
        and transport.get("transport_mode") in ("production_linux", "offline_test_double")
        and isinstance(transport.get("is_real_production_linux_transport"), bool)
        and (
            transport["is_real_production_linux_transport"]
            == (transport["transport_mode"] == "production_linux")
        )
    )


def _return_codes_are_real(payload: object) -> bool:
    return isinstance(payload, Mapping) and bool(payload) and all(
        isinstance(value, int) for value in payload.values()
    )


def _predicate(kind: str, function):
    """Adapt a boolean payload predicate to the findings signature every requirement now speaks.

    One signature, so the strict class and the shallow ones cannot be given different treatment by
    accident — which is how round 3's duplicate key made the strict authority predicate dead code.
    """

    def check(payload: object, _run: Mapping[str, object]) -> list[dict[str, object]]:
        return [] if function(payload) else [{"kind": kind}]

    return check


# locator -> the findings a payload produces, empty when it is meaningful
SEMANTIC_REQUIREMENTS = {
    "authority_input.json": lambda payload, run: _retained_identity_findings(
        payload, identity=run["identity"], run_id=run["run_id"]
    ),
    "case_matrix.json": _predicate("matrix_not_green", _matrix_is_green),
    "parity_report.json": _predicate(
        "parity_not_ok", lambda payload: isinstance(payload, Mapping) and bool(payload.get("ok"))
    ),
    "delegation_receipt.json": _predicate("delegation_not_real", _delegation_is_real),
    "return_codes.json": _predicate("return_codes_not_real", _return_codes_are_real),
    "launcher_inventory.json": _predicate("payload_empty", _nonempty),
    "sealed_source_pin.json": _predicate("payload_empty", _nonempty),
    "argument_vector.json": _predicate("payload_empty", _nonempty),
    "environment_names.json": _predicate("payload_empty", _nonempty),
    "watchdog_timing.json": _predicate("payload_empty", _nonempty),
    "watchdog_cleanup.json": _predicate("payload_empty", _nonempty),
    "case_registry.json": _predicate("payload_empty", _nonempty),
    "static_boundary_scan.json": _predicate("payload_empty", _nonempty),
    "runner_fingerprint.json": _predicate("payload_empty", _nonempty),
}

# One key, one predicate. A duplicate is how the strict authority check became unreachable, so the
# table now refuses to be built with a repeat rather than letting the last writer win silently.
if len(SEMANTIC_REQUIREMENTS) != len({locator for locator, _c, _s in REQUIRED_ARTIFACTS}):
    raise RuntimeError(
        "SEMANTIC_REQUIREMENTS does not cover exactly the required artifact classes once"
    )


def _repo_identity() -> dict[str, str]:
    """Head, tree and sole parent of the repository the artifacts describe, measured, not passed in.

    WP125-RV-006-R5 adds the parent.  "This artifact set was produced at head X" and "head X descends
    from exactly the commit we said it would" are different claims, and only the second one can catch
    a set produced from a rewritten or grafted history at a coincidentally-correct head.
    """

    def fail(message: str) -> RuntimeError:
        return RuntimeError(message)

    from launcher.delegation import ambient_trust_env

    previous = os.environ.get("GIT_CONFIG_GLOBAL")
    os.environ["GIT_CONFIG_GLOBAL"] = ambient_trust_env(REPOSITORY_ROOT)["GIT_CONFIG_GLOBAL"]
    try:
        head = safe_git(REPOSITORY_ROOT, "rev-parse", "HEAD", error=fail).strip()
        tree = safe_git(REPOSITORY_ROOT, "rev-parse", "HEAD^{tree}", error=fail).strip()
        parents = safe_git(REPOSITORY_ROOT, "rev-list", "--parents", "-n", "1", "HEAD", error=fail)
        fields = parents.split()
    finally:
        if previous is None:
            os.environ.pop("GIT_CONFIG_GLOBAL", None)
        else:
            os.environ["GIT_CONFIG_GLOBAL"] = previous
    if len(fields) != 2:
        # A merge (or a root commit) is not the shape this Packet's candidate history may have, and
        # reporting "the parent" for a commit with two of them would be a quiet lie.
        raise RuntimeError("the candidate head does not have exactly one parent")
    return {"head": head, "tree": tree, "sole_parent": fields[1]}


def _bound(schema: str, run_id: str, identity: Mapping[str, str], test_selection, payload) -> str:
    """Wrap a payload in the binding header every retained class must carry."""
    document = {
        "schema": schema,
        "run_id": run_id,
        "head": identity["head"],
        "tree": identity["tree"],
        "test_selection": list(test_selection),
        "mission_plan_hash": MISSION_PLAN_HASH,
        "packet_spec_hash": PACKET_SPEC_HASH,
        "generation": GENERATION,
        "candidate_branch": CANDIDATE_BRANCH,
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
    # WP125-RV-006-R5.  Built here, from the one pin and this run's own measurements, rather than
    # accepted from whatever the matrix happened to collect.  The producer and the verifier now call
    # the same builder, so a field can only be omitted from the evidence by being omitted from the
    # comparison in the same edit.
    add(
        "authority_input.json",
        "source",
        "wp125.authority_input.v1",
        build_retained_identity(
            run_id=run_id,
            identity=identity,
            surface=matrix.get("selected_surface"),
            runner=_runner_fingerprint(),
            raw_outcomes={
                "ok": matrix.get("ok"),
                "scheduled": matrix.get("scheduled"),
                "executed": matrix.get("executed"),
                "passed": matrix.get("passed"),
                "failed": matrix.get("failed"),
                "skipped": matrix.get("skipped"),
                "not_run": matrix.get("not_run"),
                "optimized": matrix.get("optimized"),
                "return_codes": matrix.get("return_codes", {}),
            },
        ),
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
        # Generation-2 authority, by value. A retained class that still names generation 1, the old
        # spec hash or the old branch is stale evidence wearing a current filename.
        stale = {
            "mission_plan_hash": (document["mission_plan_hash"], MISSION_PLAN_HASH),
            "packet_spec_hash": (document["packet_spec_hash"], PACKET_SPEC_HASH),
            "generation": (document["generation"], GENERATION),
            "candidate_branch": (document["candidate_branch"], CANDIDATE_BRANCH),
        }
        drifted = [key for key, (actual, want) in stale.items() if actual != want]
        if drifted:
            findings.append(
                {"kind": "stale_authority", "locator": locator, "fields": sorted(drifted)}
            )
            continue
        payload = document.get("payload")
        # A correct generation-2 wrapper around a payload that still carries generation-1 identity is
        # exactly the shape round 2 accepted. The wrapper is checked above; this looks inside.
        if _contains_stale_marker(payload):
            findings.append({"kind": "stale_payload_semantics", "locator": locator})
            continue
        predicate = SEMANTIC_REQUIREMENTS.get(locator)
        semantic = (
            predicate(payload, {"identity": identity, "run_id": document["run_id"]})
            if predicate is not None
            else []
        )
        if semantic:
            findings.append(
                {
                    "kind": "payload_not_meaningful",
                    "locator": locator,
                    "detail": semantic[:8],
                    "detail_count": len(semantic),
                }
            )
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
