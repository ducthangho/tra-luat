"""Executable WP125 positive, hostile and parity matrix (Issue 125 §8).

Every case ID in :mod:`launcher.registry` is scheduled before anything executes, and the final JSON
separates ``scheduled``, ``executed``, ``passed``, ``failed``, ``skipped`` and ``not_run``.  A
registered ID with no implementation lands in ``not_run`` and is red; an implementation whose ID is
not registered is red as well.  Neither number can be improved by deleting a case.

Security checks are written as explicit branches — see :func:`ensure`.  ``python -O`` removes
``assert`` statements, so a suite that asserts its security properties passes trivially under ``-O``
while proving nothing, and the contract requires both interpreters to execute the same teeth.

Children are real.  The fence cases spawn actual processes, hang them, orphan them and flood them,
because a mocked process cannot demonstrate that a Job Object kills a descendant whose parent has
already exited.  Timeouts are short by design: the point is the mechanism, not the wait.
"""

from __future__ import annotations

import copy
import datetime
import json
import os
import pathlib
import stat
import sys
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager

HERE = pathlib.Path(__file__).resolve().parent
BOOTSTRAP_ROOT = HERE.parent
CANDIDATE_ROOT = HERE.parents[3]
if str(BOOTSTRAP_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOTSTRAP_ROOT))

from core.ledger import Ledger  # noqa: E402

from launcher import inventory as inventory_module  # noqa: E402
from launcher import parity as parity_module  # noqa: E402
from launcher import registry as registry_module  # noqa: E402
from launcher.argv import build_launch_plan, describe as describe_plan  # noqa: E402
from launcher.delegation import (  # noqa: E402
    MARKER_NAME,
    audit_job_report,
    build_job,
    run_job,
    validate_operation,
)
from launcher.environment import (  # noqa: E402
    MEMORY_VARIABLE,
    build_child_environment,
    describe as describe_environment,
)
from launcher.errors import LauncherRejected  # noqa: E402
from launcher.inputs import read_sealed_bytes, read_sealed_json  # noqa: E402
from launcher.preflight import (  # noqa: E402
    STEP_NAMES,
    PreflightReceipt,
    mint_claim,
    run_preflight,
)
from launcher.watchdog import (  # noqa: E402
    ProcessIdentity,
    build_deadline,
    identify,
    is_alive,
    python_executable,
    run_supervised,
)

REPOSITORY = "ducthangho/tra-luat"
MISSION_PLAN_HASH = "ac5d5180be3de124dce002041683c3d6926aa60b36d39c7cad02136fd0776b9a"
PACKET_SPEC_HASH = "6cbc678ecdc36fdbda81a9c96d6921797e5d5e6d2467c03f26f95589d9f0c7f5"
INTEGRATION_HEAD = "60446be6467347e7242d5e03c001c19794e6e96d"
INTEGRATION_TREE = "5d19b56a32d5fd127141ad0cd0824b8c976ba877"
CANDIDATE_REF = "refs/heads/agent/wp125-g1-claude"
LEASE_STOP = "2099-01-01T00:00:00Z"
WRITE_PREFIX = inventory_module.LAUNCHER_PREFIX

CASES: list[tuple[str, Callable[[], dict[str, object]]]] = []
_SEEN_IDS: set[str] = set()

# Collected while the matrix runs, so `controller.py produce` can retain real evidence rather than a
# second, separately-computed story about the same run.
CLEANUP_RECORDS: list[dict[str, object]] = []
DELEGATION_RECEIPT: dict[str, object] = {}
ENVIRONMENT_NAMES: list[str] = []


def ensure(condition: object, message: str) -> None:
    """Explicit branch, never ``assert`` — see the module docstring."""
    if not condition:
        raise AssertionError(message)


def case(case_id: str):
    def register(function: Callable[[], dict[str, object]]):
        if case_id in _SEEN_IDS:
            raise ValueError("duplicate case id %r" % (case_id,))
        if case_id not in registry_module.CASES:
            raise ValueError("case id %r is not in the registry" % (case_id,))
        _SEEN_IDS.add(case_id)
        CASES.append((case_id, function))
        return function

    return register


def expect_rejection(category: str, action: Callable[[], object]) -> dict[str, object]:
    """Run ``action`` and require a named rejection.

    A test that merely requires "some exception" passes when the code crashes for an unrelated
    reason, which is how a control silently stops testing what it names.
    """
    try:
        action()
    except LauncherRejected as exc:
        if exc.category != category:
            raise AssertionError(
                "expected category %r, got %r (%s)" % (category, exc.category, exc)
            ) from exc
        return {"rejected": True, "category": exc.category}
    raise AssertionError("expected a %r rejection, none was raised" % (category,))


# --------------------------------------------------------------------------- fixtures


def seal(path: pathlib.Path, data: bytes) -> pathlib.Path:
    path.write_bytes(data)
    path.chmod(stat.S_IREAD)
    return path


def unseal(root: pathlib.Path) -> None:
    for path in root.rglob("*"):
        if path.is_file():
            try:
                path.chmod(stat.S_IREAD | stat.S_IWRITE)
            except OSError:
                pass


def source_pin_document() -> dict[str, object]:
    return {
        "schema_version": 1,
        "kind": "dispatcher_source_pin",
        "repository": REPOSITORY,
        "source": {
            "integration_head": INTEGRATION_HEAD,
            "integration_tree": INTEGRATION_TREE,
            "candidate_ref": CANDIDATE_REF,
        },
        "bounds": {"effective_write_prefix": WRITE_PREFIX},
    }


def authority_document() -> dict[str, object]:
    return {
        "repository": REPOSITORY,
        "mission": {"issue": 76, "revision": 6, "plan_hash": MISSION_PLAN_HASH},
        "packet": {
            "issue": 125,
            "revision": 1,
            "generation": 1,
            "attempt": 1,
            "spec_hash": PACKET_SPEC_HASH,
        },
    }


def expected_authority() -> dict[str, object]:
    return {
        "repository": REPOSITORY,
        "mission_issue": 76,
        "mission_revision": 6,
        "mission_plan_hash": MISSION_PLAN_HASH,
        "packet_issue": 125,
        "packet_revision": 1,
        "packet_generation": 1,
        "packet_attempt": 1,
        "packet_spec_hash": PACKET_SPEC_HASH,
    }


@contextmanager
def fixture(**overrides: object) -> Iterator[dict[str, object]]:
    """A complete, sealed, outside-the-tree preflight context."""
    temp = tempfile.TemporaryDirectory(prefix="wp125-launcher-")
    root = pathlib.Path(temp.name).resolve()
    try:
        pin_bytes = (
            json.dumps(source_pin_document(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        pin_path = seal(root / "source_pin.json", pin_bytes)
        prompt_path = seal(root / "reviewer_prompt.txt", b"Review the exact head.\n")
        import hashlib

        context: dict[str, object] = {
            "authority": authority_document(),
            "expected_authority": expected_authority(),
            "lease": {
                "lease_id": "wp125-r1-g1-a1-lease-60446be6-6cbc678e",
                "effective_stop_utc": LEASE_STOP,
                "generation": 1,
                "candidate_ref": CANDIDATE_REF,
                "candidate_start_head": INTEGRATION_HEAD,
            },
            "expected_candidate_ref": CANDIDATE_REF,
            "source_pin_path": str(pin_path),
            "expected_source_pin_sha256": hashlib.sha256(pin_bytes).hexdigest(),
            "expected_integration_head": INTEGRATION_HEAD,
            "candidate_root": str(CANDIDATE_ROOT),
            "worktree_clean": True,
            "selected_write_paths": (WRITE_PREFIX + "controller.py",),
            "inventory": inventory_module.build_inventory(HERE, CANDIDATE_ROOT),
            "launch_config": {
                "permission_mode": "dontAsk",
                "executable": python_executable(),
                "working_directory": str(root),
                "extra_args": (),
            },
            "prompt_path": str(prompt_path),
            "surface": {
                "platform": sys.platform,
                "windows_sandbox_available": True,
                "delegation_eligible": False,
            },
            "parent_environment": dict(os.environ),
            "temp_root": str(root),
        }
        context.update(overrides)
        yield context
    finally:
        unseal(root)
        temp.cleanup()


def child_report_command(source: str) -> tuple[str, ...]:
    return (python_executable(), "-c", source)


def short_deadline(seconds: float = 2.0):
    return build_deadline(seconds, LEASE_STOP)


# --------------------------------------------------------------------------- positive controls


@case("WP125-POS-001-one-valid-claim-launches-exactly-one-child")
def positive_single_child() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        ensure(receipt.complete, "preflight did not complete on a valid fixture")
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        claim = mint_claim(receipt, ledger, "wp125-r1-g1-a1", {"role": "executor"})
        ensure(claim["created"] is True, "the first claim was not created")

        source = "import json,os,sys;print(json.dumps({'pid':os.getpid()}))"
        outcome = run_supervised(
            child_report_command(source),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(),
        )
        CLEANUP_RECORDS.append({"case": "POS-001", "cleanup": outcome.cleanup})
        ensure(outcome.status == "completed", "the healthy child did not complete")
        ensure(outcome.return_code == 0, "the healthy child did not exit zero")
        ensure(len(ledger) == 1, "more than one claim object exists")
        return {
            "claims": len(ledger),
            "children": 1,
            "return_code": outcome.return_code,
            "cleanup_proven": outcome.cleanup["cleanup_proven"],
        }


@case("WP125-POS-002-identical-retry-creates-no-duplicate-claim")
def positive_idempotent_claim() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        payload = {"role": "executor", "branch": CANDIDATE_REF}
        first = mint_claim(receipt, ledger, "wp125-retry", dict(payload))
        second = mint_claim(receipt, ledger, "wp125-retry", dict(payload))
        ensure(first["created"] is True, "the first claim was not created")
        ensure(second["created"] is False, "an identical retry created a second claim")
        ensure(len(ledger) == 1, "the ledger holds more than one record")
        return {"created_first": True, "created_second": False, "records": len(ledger)}


@case("WP125-POS-003-healthy-child-completes-without-fence")
def positive_no_fence() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        outcome = run_supervised(
            child_report_command("print('done')"),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(5.0),
        )
        CLEANUP_RECORDS.append({"case": "POS-003", "cleanup": outcome.cleanup})
        ensure(outcome.fenced is False, "a healthy child was fenced")
        ensure(outcome.status == "completed", "a healthy child did not complete")
        return {"fenced": False, "return_code": outcome.return_code}


@case("WP125-POS-004-real-hang-is-fenced-without-cooperation")
def positive_hang_fenced() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        outcome = run_supervised(
            child_report_command("import time;time.sleep(600)"),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(1.0),
        )
        CLEANUP_RECORDS.append({"case": "POS-004", "cleanup": outcome.cleanup})
        ensure(outcome.fenced is True, "a hung child was not fenced")
        ensure(outcome.cleanup["cleanup_proven"] is True, "cleanup was not proven")
        ensure(outcome.self_reported_markers == (), "a silent child reported markers")
        return {"fenced": True, "cleanup": outcome.cleanup}


@case("WP125-POS-005-authorized-fallback-runs-only-run-test")
def positive_delegation() -> dict[str, object]:
    global DELEGATION_RECEIPT
    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": True,
        }
    ) as context:
        receipt = run_preflight(context)
        ensure(receipt.surface == "delegated_linux_run_test", "the fallback surface was not selected")
        job = build_job(
            operation="run_test",
            candidate_head=INTEGRATION_HEAD,
            candidate_tree=INTEGRATION_TREE,
            test_selection=("launcher_matrix",),
            read_only_root=str(CANDIDATE_ROOT),
            eligible=True,
        )
        evidence = run_job(
            job,
            parent_environment=dict(os.environ),
            candidate_root=str(CANDIDATE_ROOT),
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(20.0),
        )
        DELEGATION_RECEIPT = dict(evidence)
        CLEANUP_RECORDS.append({"case": "POS-005", "cleanup": evidence["cleanup"]})
        ensure(evidence["return_code"] == 0, "the delegated job did not exit zero")
        ensure(job.operation == "run_test", "the delegated operation is not run_test")
        return {
            "operation": job.operation,
            "return_code": evidence["return_code"],
            "timeout_source": evidence["timeout_source"],
        }


@case("WP125-POS-006-memory-variable-observed-inside-child")
def positive_memory_observed() -> dict[str, object]:
    global ENVIRONMENT_NAMES
    with fixture() as context:
        receipt = run_preflight(context)
        source = (
            "import json,os,sys;"
            "print(json.dumps({'memory':os.environ.get(%r),'names':sorted(os.environ)}))"
            % MEMORY_VARIABLE
        )
        outcome = run_supervised(
            child_report_command(source),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(),
        )
        payload = _last_json_line(outcome)
        ENVIRONMENT_NAMES = list(payload["names"])
        ensure(payload["memory"] == "1", "the child did not observe the memory variable as 1")
        return {"observed_inside_child": payload["memory"], "name_count": len(payload["names"])}


def _last_json_line(outcome) -> dict[str, object]:
    """Read the child's JSON line from a *recorded* run.

    Used only where the child's report is the measurement (its own environment, its own argv).  It
    is never used to decide liveness — see the watchdog module.
    """
    for line in reversed(str(outcome.stdout_text).splitlines()):
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)
    raise AssertionError("the child produced no JSON line")


@case("WP125-POS-007-argument-boundary-observed-inside-child")
def positive_argument_boundary() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        tricky = [
            "plain",
            "with space",
            'quote"inside',
            "back\\slash\\end\\",
            "trailing\\\\",
            "unicode-đường-dẫn",
            "semi;colon & amp | pipe",
            "%PATH%",
            "$HOME",
        ]
        source = "import json,sys;print(json.dumps({'argv':sys.argv[1:]}))"
        outcome = run_supervised(
            (python_executable(), "-c", source, *tricky),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(),
        )
        payload = _last_json_line(outcome)
        ensure(payload["argv"] == tricky, "the argument boundary was not preserved exactly")
        return {"observed_argv": payload["argv"], "count": len(tricky)}


@case("WP125-POS-008-inventory-digest-covers-every-owned-file")
def positive_inventory() -> dict[str, object]:
    first = inventory_module.build_inventory(HERE, CANDIDATE_ROOT)
    second = inventory_module.build_inventory(HERE, CANDIDATE_ROOT)
    ensure(first["inventory_sha256"] == second["inventory_sha256"], "the inventory digest is unstable")
    ensure(first["file_count"] >= 10, "the inventory is implausibly small")
    outside = [entry for entry in first["files"] if not entry["path"].startswith(WRITE_PREFIX)]
    ensure(outside == [], "an inventoried file falls outside the write prefix")
    return {"file_count": first["file_count"], "inventory_sha256": first["inventory_sha256"]}


@case("WP125-POS-009-preflight-runs-in-contract-order")
def positive_preflight_order() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        ensure(receipt.complete, "preflight did not complete")
        order = tuple(step.name for step in receipt.steps)
        ensure(order == STEP_NAMES, "preflight ran out of contract order")
        indexes = [step.index for step in receipt.steps]
        ensure(indexes == list(range(1, len(STEP_NAMES) + 1)), "preflight step indexes are not dense")
        return {"order": list(order)}


@case("WP125-POS-010-artifacts-seal-and-verify")
def positive_artifacts() -> dict[str, object]:
    from core.artifacts import ArtifactSet, verify as verify_artifacts

    with fixture() as context:
        run_root = pathlib.Path(str(context["temp_root"])) / "run"
        artifacts = ArtifactSet(run_root, "wp125-selftest")
        artifacts.add("source", "inventory.json", json.dumps({"probe": True}) + "\n")
        artifacts.add("corpus", "registry.json", json.dumps(dict(registry_module.CASES)) + "\n")
        artifacts.add("per_case_matrix", "matrix.json", json.dumps({"scheduled": len(CASES)}) + "\n")
        artifacts.add("runner_env_digest", "runner.json", json.dumps({"os": os.name}) + "\n")
        artifacts.add("cleanup_record", "cleanup.json", json.dumps({"proven": True}) + "\n")
        artifacts.finalize()
        result = verify_artifacts(str(run_root))
        ensure(result.get("ok") is True, "the sealed artifact set did not verify")
        return {"verified_files": result.get("verified_files"), "ok": True}


@case("WP125-POS-011-deadline-is-bounded-by-the-lease")
def positive_deadline_bounded() -> dict[str, object]:
    now = datetime.datetime.now(datetime.timezone.utc)
    soon = (now + datetime.timedelta(seconds=5)).isoformat().replace("+00:00", "Z")
    bounded = build_deadline(3600.0, soon, now_utc=now)
    ensure(bounded.bounded_by_lease is True, "a long timeout was not clamped by the lease")
    ensure(bounded.remaining() <= 5.5, "the clamped deadline exceeds the lease")
    generous = build_deadline(1.0, LEASE_STOP, now_utc=now)
    ensure(generous.bounded_by_lease is False, "a short timeout was wrongly reported as clamped")
    return {"clamped": True, "requested": 3600.0}


@case("WP125-POS-012-static-boundary-scan-is-clean")
def positive_static_scan() -> dict[str, object]:
    scan = inventory_module.scan_package(HERE)
    ensure(scan["scanned_files"] >= 8, "the static scan covered implausibly few files")
    ensure(scan["findings"] == [], "the static boundary scan reported findings: %s" % scan["findings"])
    ensure(scan["coverage"]["not_covered"], "the static scan claims total coverage")
    return {"scanned_files": scan["scanned_files"], "findings": 0}


@case("WP125-POS-013-owned-text-is-lf-only")
def positive_eol() -> dict[str, object]:
    survey = inventory_module.eol_survey(inventory_module.launcher_files(HERE))
    ensure(survey["ok"], "the EOL survey found violations: %s" % survey["violations"])
    ensure(survey["checked_files"] >= 8, "the EOL survey checked implausibly few files")
    return {
        "checked_files": survey["checked_files"],
        "crlf_exception_files": survey["crlf_exception_files"],
        "violations": 0,
    }


@case("WP125-POS-014-parity-matrix-accepts-equal-sides")
def positive_parity_equal() -> dict[str, object]:
    ids = ("A", "B", "C")
    side = parity_module.SideReport(
        platform="windows",
        scheduled=ids,
        outcomes={case_id: "passed" for case_id in ids},
        argument_observations={"argv_preserved": True},
        environment_observations={"memory": "1"},
        claim_ordering=("preflight", "claim"),
        fence_categories={"A": "completed_without_fence"},
    )
    other = dataclass_replace(side, platform="linux")
    matrix = parity_module.compare(side, other, portable_ids=ids, platform_specific={})
    parity_module.require_ok(matrix)
    return {"portable_case_count": matrix["portable_case_count"], "ok": True}


def dataclass_replace(report: parity_module.SideReport, **changes: object) -> parity_module.SideReport:
    import dataclasses

    return dataclasses.replace(report, **changes)


# --------------------------------------------------------------------------- permission and argv


def _plan_with(config_changes: dict[str, object], context: dict[str, object]):
    config = dict(context["launch_config"])
    config.update(config_changes)
    return lambda: build_launch_plan(
        config, prompt_path=str(context["prompt_path"]), candidate_root=str(CANDIDATE_ROOT)
    )


@case("WP125-NEG-001-permission-mode-omitted")
def negative_mode_omitted() -> dict[str, object]:
    with fixture() as context:
        config = dict(context["launch_config"])
        config.pop("permission_mode")
        return expect_rejection(
            "permission_mode",
            lambda: build_launch_plan(
                config, prompt_path=str(context["prompt_path"]), candidate_root=str(CANDIDATE_ROOT)
            ),
        )


@case("WP125-NEG-002-permission-mode-auto")
def negative_mode_auto() -> dict[str, object]:
    with fixture() as context:
        return expect_rejection("permission_mode", _plan_with({"permission_mode": "auto"}, context))


@case("WP125-NEG-003-permission-mode-bare-auto-casefold")
def negative_mode_auto_casefold() -> dict[str, object]:
    with fixture() as context:
        return expect_rejection("permission_mode", _plan_with({"permission_mode": "AuTo"}, context))


@case("WP125-NEG-004-duplicate-permission-switch")
def negative_duplicate_switch() -> dict[str, object]:
    with fixture() as context:
        return expect_rejection(
            "permission_mode",
            _plan_with({"extra_args": ("--permission-mode", "auto")}, context),
        )


@case("WP125-NEG-005-injected-argument-in-extra-args")
def negative_injected_argument() -> dict[str, object]:
    with fixture() as context:
        return expect_rejection(
            "argument_vector",
            _plan_with({"extra_args": ("--dangerously-skip-permissions",)}, context),
        )


@case("WP125-NEG-006-settings-override-switch")
def negative_settings_override() -> dict[str, object]:
    with fixture() as context:
        return expect_rejection(
            "argument_vector", _plan_with({"extra_args": ("--settings=/tmp/evil.json",)}, context)
        )


@case("WP125-NEG-007-executable-inside-candidate-tree")
def negative_executable_inside_tree() -> dict[str, object]:
    with fixture() as context:
        inside = str(CANDIDATE_ROOT / "scripts" / "tl.py")
        return expect_rejection("argument_vector", _plan_with({"executable": inside}, context))


@case("WP125-NEG-008-relative-executable-path")
def negative_relative_executable() -> dict[str, object]:
    with fixture() as context:
        return expect_rejection("argument_vector", _plan_with({"executable": "python"}, context))


@case("WP125-NEG-009-control-characters-in-argument")
def negative_control_characters() -> dict[str, object]:
    with fixture() as context:
        return expect_rejection(
            "argument_vector", _plan_with({"extra_args": ("value\nwith-newline",)}, context)
        )


@case("WP125-NEG-010-prompt-path-inside-candidate-tree")
def negative_prompt_inside_tree() -> dict[str, object]:
    with fixture() as context:
        inside = str(CANDIDATE_ROOT / "README.md")
        return expect_rejection(
            "argument_vector",
            lambda: build_launch_plan(
                dict(context["launch_config"]),
                prompt_path=inside,
                candidate_root=str(CANDIDATE_ROOT),
            ),
        )


# --------------------------------------------------------------------------- environment


@case("WP125-NEG-011-credential-shaped-extra-variable")
def negative_credential_extra() -> dict[str, object]:
    return expect_rejection(
        "child_environment",
        lambda: build_child_environment(
            {}, candidate_root=str(CANDIDATE_ROOT), extra={"GITHUB_TOKEN": "x"}
        ),
    )


@case("WP125-NEG-012-parent-credentials-are-not-inherited")
def negative_no_inherited_credentials() -> dict[str, object]:
    parent = {
        "PATH": os.environ.get("PATH", ""),
        "SystemRoot": os.environ.get("SystemRoot", ""),
        "GH_TOKEN": "planted",
        "GITHUB_PAT": "planted",
        "AWS_SECRET_ACCESS_KEY": "planted",
        "ANTHROPIC_API_KEY": "planted",
        "SSH_AUTH_SOCK": "planted",
        "HTTPS_PROXY": "http://user:pass@proxy",
        "NPM_TOKEN": "planted",
        "COSIGN_PASSWORD": "planted",
    }
    child = build_child_environment(parent, candidate_root=str(CANDIDATE_ROOT))
    planted = [name for name in parent if name not in ("PATH", "SystemRoot")]
    leaked = [name for name in planted if name in child]
    ensure(leaked == [], "credential-shaped parent variables reached the child: %s" % leaked)
    ensure(child[MEMORY_VARIABLE] == "1", "the memory variable is not exactly 1")
    return {"planted": len(planted), "leaked": 0, "child_names": len(child)}


@case("WP125-NEG-013-path-entry-inside-candidate-tree-is-dropped")
def negative_path_sanitized() -> dict[str, object]:
    poisoned = str(CANDIDATE_ROOT / "scripts")
    parent = {"PATH": os.pathsep.join([poisoned, os.environ.get("PATH", "")])}
    child = build_child_environment(parent, candidate_root=str(CANDIDATE_ROOT))
    entries = child["PATH"].split(os.pathsep)
    ensure(poisoned not in entries, "a PATH entry inside the candidate tree survived")
    return {"dropped": poisoned, "remaining_entries": len(entries)}


@case("WP125-NEG-014-environment-evidence-carries-no-values")
def negative_environment_evidence() -> dict[str, object]:
    child = build_child_environment(
        {"PATH": "sentinel-path-value", "SystemRoot": "sentinel-root"},
        candidate_root=str(CANDIDATE_ROOT),
    )
    described = describe_environment(child)
    blob = json.dumps(described, ensure_ascii=False, sort_keys=True)
    ensure("sentinel-path-value" not in blob, "an environment value leaked into evidence")
    ensure("sentinel-root" not in blob, "an environment value leaked into evidence")
    ensure(described["values_recorded"] is False, "the evidence claims values are recorded")
    ensure(described[MEMORY_VARIABLE] == "1", "the policy value is not in the evidence")
    return {"values_recorded": False, "name_count": described["name_count"]}


# --------------------------------------------------------------------------- sealed inputs


@case("WP125-NEG-015-writable-sealed-input")
def negative_writable_input() -> dict[str, object]:
    with fixture() as context:
        root = pathlib.Path(str(context["temp_root"]))
        writable = root / "writable.json"
        writable.write_bytes(b"{}\n")
        writable.chmod(stat.S_IREAD | stat.S_IWRITE)
        return expect_rejection(
            "sealed_input",
            lambda: read_sealed_bytes(
                str(writable), "writable input", candidate_root=str(CANDIDATE_ROOT)
            ),
        )


@case("WP125-NEG-016-sealed-input-inside-candidate-tree")
def negative_input_inside_tree() -> dict[str, object]:
    inside = str(CANDIDATE_ROOT / "README.md")
    return expect_rejection(
        "sealed_input",
        lambda: read_sealed_bytes(inside, "inside input", candidate_root=str(CANDIDATE_ROOT)),
    )


@case("WP125-NEG-017-sealed-input-path-traversal")
def negative_input_traversal() -> dict[str, object]:
    with fixture() as context:
        traversal = str(pathlib.Path(str(context["temp_root"])) / ".." / "escaped.json")
        return expect_rejection(
            "sealed_input",
            lambda: read_sealed_bytes(
                traversal, "traversal input", candidate_root=str(CANDIDATE_ROOT)
            ),
        )


@case("WP125-NEG-018-sealed-input-alternate-data-stream")
def negative_input_ads() -> dict[str, object]:
    with fixture() as context:
        stream = str(pathlib.Path(str(context["temp_root"])) / "carrier.json") + ":payload"
        return expect_rejection(
            "sealed_input",
            lambda: read_sealed_bytes(stream, "ads input", candidate_root=str(CANDIDATE_ROOT)),
        )


@case("WP125-NEG-019-sealed-input-dos-device")
def negative_input_dos_device() -> dict[str, object]:
    with fixture() as context:
        device = str(pathlib.Path(str(context["temp_root"])) / "NUL.txt")
        return expect_rejection(
            "sealed_input",
            lambda: read_sealed_bytes(device, "device input", candidate_root=str(CANDIDATE_ROOT)),
        )


@case("WP125-NEG-020-sealed-input-extra-hard-link")
def negative_input_hard_link() -> dict[str, object]:
    with fixture() as context:
        root = pathlib.Path(str(context["temp_root"]))
        original = root / "linked.json"
        original.write_bytes(b"{}\n")
        alias = root / "alias.json"
        os.link(original, alias)
        original.chmod(stat.S_IREAD)
        result = expect_rejection(
            "sealed_input",
            lambda: read_sealed_bytes(
                str(original), "linked input", candidate_root=str(CANDIDATE_ROOT)
            ),
        )
        result["hard_links"] = original.stat().st_nlink
        return result


# --------------------------------------------------------------------------- authority and lease


def _preflight_failure(context: dict[str, object], step: str, category: str) -> dict[str, object]:
    receipt = run_preflight(context)
    ensure(receipt.complete is False, "preflight completed on a hostile fixture")
    failure = receipt.failure or {}
    ensure(failure.get("step") == step, "failure landed on step %r, expected %r" % (failure.get("step"), step))
    ensure(
        failure.get("category") == category,
        "failure category %r, expected %r" % (failure.get("category"), category),
    )
    return {"step": failure.get("step"), "category": failure.get("category")}


@case("WP125-NEG-021-wrong-mission-plan-hash")
def negative_wrong_plan_hash() -> dict[str, object]:
    with fixture() as context:
        authority = copy.deepcopy(context["authority"])
        authority["mission"]["plan_hash"] = "0" * 64
        context["authority"] = authority
        return _preflight_failure(context, "authority_identity", "authority_mismatch")


@case("WP125-NEG-022-wrong-packet-spec-hash")
def negative_wrong_spec_hash() -> dict[str, object]:
    with fixture() as context:
        authority = copy.deepcopy(context["authority"])
        authority["packet"]["spec_hash"] = "1" * 64
        context["authority"] = authority
        return _preflight_failure(context, "authority_identity", "authority_mismatch")


@case("WP125-NEG-023-wrong-attempt")
def negative_wrong_attempt() -> dict[str, object]:
    with fixture() as context:
        authority = copy.deepcopy(context["authority"])
        authority["packet"]["attempt"] = 2
        context["authority"] = authority
        return _preflight_failure(context, "authority_identity", "authority_mismatch")


@case("WP125-NEG-024-stale-generation")
def negative_stale_generation() -> dict[str, object]:
    with fixture() as context:
        lease = dict(context["lease"])
        lease["generation"] = 0
        context["lease"] = lease
        return _preflight_failure(context, "lease_and_branch", "stale_generation")


@case("WP125-NEG-025-expired-lease")
def negative_expired_lease() -> dict[str, object]:
    with fixture() as context:
        lease = dict(context["lease"])
        lease["effective_stop_utc"] = "2000-01-01T00:00:00Z"
        context["lease"] = lease
        return _preflight_failure(context, "lease_and_branch", "lease_expired")


@case("WP125-NEG-026-source-pin-hash-mismatch")
def negative_pin_mismatch() -> dict[str, object]:
    with fixture() as context:
        context["expected_source_pin_sha256"] = "2" * 64
        return _preflight_failure(context, "source_pin", "authority_mismatch")


@case("WP125-NEG-027-write-set-expansion")
def negative_write_set_expansion() -> dict[str, object]:
    with fixture() as context:
        context["selected_write_paths"] = (WRITE_PREFIX + "controller.py", "scripts/tl.py")
        return _preflight_failure(context, "worktree_and_write_set", "write_set")


@case("WP125-NEG-028-dirty-worktree")
def negative_dirty_worktree() -> dict[str, object]:
    with fixture() as context:
        context["worktree_clean"] = False
        return _preflight_failure(context, "worktree_and_write_set", "write_set")


# --------------------------------------------------------------------------- claim ordering


@case("WP125-NEG-029-claim-before-preflight-completes")
def negative_claim_before_preflight() -> dict[str, object]:
    with fixture() as context:
        context["worktree_clean"] = False
        receipt = run_preflight(context)
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        result = expect_rejection(
            "preflight_incomplete",
            lambda: mint_claim(receipt, ledger, "wp125-early", {"role": "executor"}),
        )
        ensure(len(ledger) == 0, "a claim object was minted despite a failed preflight")
        result["claim_objects"] = len(ledger)
        return result


@case("WP125-NEG-030-fake-always-green-preflight")
def negative_fake_preflight() -> dict[str, object]:
    """The fault-injection control §5 requires.

    A substituted step returns green with no observations.  The receipt audit kills it, so a
    preflight cannot be satisfied by a function that merely says yes.
    """
    with fixture() as context:
        from launcher import preflight as preflight_module

        def always_green(_context: dict[str, object]) -> dict[str, object]:
            return {"ok": True}

        steps = tuple(
            (name, always_green if name == "authority_identity" else function)
            for name, function in preflight_module.STEPS
        )
        receipt = run_preflight(context, steps=steps)
        ensure(receipt.complete is False, "a fake always-green preflight was accepted")
        failure = receipt.failure or {}
        ensure(
            failure.get("category") == "preflight_incomplete",
            "the impostor was rejected for the wrong reason: %s" % failure.get("category"),
        )
        return {"category": failure.get("category"), "step": failure.get("step")}


@case("WP125-NEG-031-conflicting-payload-under-one-reconcile-key")
def negative_conflicting_payload() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        mint_claim(receipt, ledger, "wp125-conflict", {"role": "executor"})
        result = expect_rejection(
            "duplicate_claim",
            lambda: mint_claim(receipt, ledger, "wp125-conflict", {"role": "reviewer"}),
        )
        ensure(len(ledger) == 1, "the conflicting claim created a second record")
        result["records"] = len(ledger)
        return result


@case("WP125-NEG-032-negative-preflight-mints-nothing")
def negative_preflight_mints_nothing() -> dict[str, object]:
    with fixture() as context:
        context["surface"] = {
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": False,
        }
        ledger_path = pathlib.Path(str(context["temp_root"])) / "ledger.json"
        receipt = run_preflight(context)
        ensure(receipt.complete is False, "preflight completed with no execution surface")
        ensure(not ledger_path.exists(), "a ledger file was created by a failed preflight")
        ensure(receipt.plan is None, "a launch plan was built despite a failed preflight")
        return {
            "claim_objects": 0,
            "child_processes": 0,
            "delegated_jobs": 0,
            "category": (receipt.failure or {}).get("category"),
        }


# --------------------------------------------------------------------------- hostile children


@case("WP125-NEG-033-hung-child-is-fenced")
def negative_hung_child() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        outcome = run_supervised(
            child_report_command("import time\nwhile True:\n    time.sleep(30)"),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(1.0),
        )
        CLEANUP_RECORDS.append({"case": "NEG-033", "cleanup": outcome.cleanup})
        ensure(outcome.fenced is True, "the hung child escaped the fence")
        ensure(outcome.cleanup["cleanup_proven"] is True, "cleanup was not proven")
        return {"fenced": True, "status": outcome.status}


@case("WP125-NEG-034-detached-descendant-is-fenced")
def negative_detached_descendant() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        grandchild = "import time\nwhile True:\n    time.sleep(30)"
        source = (
            "import subprocess,sys,time\n"
            "subprocess.Popen([sys.executable,'-c',%r])\n"
            "time.sleep(0.4)\n"
            "raise SystemExit(0)\n" % grandchild
        )
        outcome = run_supervised(
            child_report_command(source),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(1.5),
        )
        CLEANUP_RECORDS.append({"case": "NEG-034", "cleanup": outcome.cleanup})
        active_before = outcome.termination.get("job_active_before_terminate")
        ensure(
            outcome.cleanup["cleanup_proven"] is True,
            "an orphaned descendant survived the fence",
        )
        # The direct child is already gone by here, so a job census above one is the witness that a
        # genuinely orphaned descendant was inside the fence — without it this case would pass
        # vacuously against a tree that never had a second process.
        if os.name == "nt":
            ensure(
                isinstance(active_before, int) and active_before >= 1,
                "the job census did not witness a contained descendant: %r" % (active_before,),
            )
        return {
            "cleanup_proven": True,
            "job_active_before_terminate": active_before,
            "mechanism": outcome.termination.get("mechanism", "job_object"),
            "status": outcome.status,
        }


@case("WP125-NEG-035-marker-forging-child-is-still-fenced")
def negative_marker_forging_child() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        source = (
            "import time\n"
            "print('READY',flush=True)\n"
            "print('HEARTBEAT',flush=True)\n"
            "print('SUCCESS',flush=True)\n"
            "print('CLEANUP-COMPLETE',flush=True)\n"
            "while True:\n    time.sleep(30)\n"
        )
        outcome = run_supervised(
            child_report_command(source),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(1.0),
        )
        CLEANUP_RECORDS.append({"case": "NEG-035", "cleanup": outcome.cleanup})
        ensure(outcome.fenced is True, "a marker-forging child talked the watchdog out of firing")
        ensure(len(outcome.self_reported_markers) >= 3, "the forged markers were not recorded")
        ensure(outcome.cleanup["cleanup_proven"] is True, "cleanup was not proven")
        return {
            "fenced": True,
            "forged_markers": list(outcome.self_reported_markers),
            "self_report_used_as_liveness": False,
        }


@case("WP125-NEG-036-output-flood-does-not-escape-cleanup")
def negative_output_flood() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        source = (
            "import sys\n"
            "line='x'*4096\n"
            "while True:\n"
            "    sys.stdout.write(line)\n"
            "    sys.stdout.flush()\n"
        )
        outcome = run_supervised(
            child_report_command(source),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(1.0),
            output_ceiling=16 * 1024,
        )
        CLEANUP_RECORDS.append({"case": "NEG-036", "cleanup": outcome.cleanup})
        ensure(outcome.fenced is True, "the flooding child escaped the fence")
        ensure(outcome.cleanup["cleanup_proven"] is True, "cleanup was not proven")
        return {"fenced": True, "output_bounded": True}


@case("WP125-NEG-037-pid-reuse-is-refused")
def negative_pid_reuse() -> dict[str, object]:
    live = identify(os.getpid())
    ensure(live is not None, "the running process could not be identified")
    ensure(is_alive(live), "the running process was reported dead")
    impostor = ProcessIdentity(pid=live.pid, created=live.created + 1)
    ensure(
        not is_alive(impostor),
        "a recycled pid with a different creation stamp was treated as the same process",
    )
    return {"pid": live.pid, "identity_gated": True}


# --------------------------------------------------------------------------- surface selection


@case("WP125-NEG-038-no-windows-sandbox-with-valid-delegation")
def negative_surface_delegation() -> dict[str, object]:
    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": True,
        }
    ) as context:
        receipt = run_preflight(context)
        ensure(receipt.complete, "a valid delegation surface was refused")
        ensure(receipt.surface == "delegated_linux_run_test", "the fallback surface was not selected")
        return {"selected_surface": receipt.surface}


@case("WP125-NEG-039-no-windows-sandbox-with-invalid-delegation")
def negative_surface_invalid_delegation() -> dict[str, object]:
    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": False,
        }
    ) as context:
        return _preflight_failure(context, "execution_surface", "sandbox_unavailable")


@case("WP125-NEG-040-no-available-path-pauses-fail-closed")
def negative_surface_none() -> dict[str, object]:
    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": False,
        }
    ) as context:
        receipt = run_preflight(context)
        ensure(receipt.complete is False, "preflight completed with no available surface")
        ensure(receipt.plan is None, "a launch plan was built with no available surface")
        ensure(receipt.environment == {}, "a child environment was built with no available surface")
        return {"paused": True, "category": (receipt.failure or {}).get("category")}


# --------------------------------------------------------------------------- delegation scope


@case("WP125-NEG-041-delegated-unlisted-operation")
def negative_delegated_unlisted() -> dict[str, object]:
    return expect_rejection("delegation_scope", lambda: validate_operation("run_anything"))


@case("WP125-NEG-042-delegated-claim-is-refused-by-name")
def negative_delegated_claim() -> dict[str, object]:
    results = {}
    for operation in ("claim", "heartbeat", "verdict", "merge", "land", "deploy", "live"):
        results[operation] = expect_rejection(
            "delegation_scope", lambda operation=operation: validate_operation(operation)
        )["category"]
    return {"refused_by_name": results}


@case("WP125-NEG-043-delegation-without-eligibility")
def negative_delegation_without_eligibility() -> dict[str, object]:
    return expect_rejection(
        "delegation_scope",
        lambda: build_job(
            operation="run_test",
            candidate_head=INTEGRATION_HEAD,
            candidate_tree=INTEGRATION_TREE,
            test_selection=("launcher_matrix",),
            read_only_root=str(CANDIDATE_ROOT),
            eligible=False,
        ),
    )


@case("WP125-NEG-044-delegated-secret-marker-is-detected")
def negative_delegated_secret() -> dict[str, object]:
    """Prove the marker probe is a measurement, not a formality.

    A forged report that claims the marker *was* present must be refused; that is what makes the
    honest report's ``false`` meaningful.
    """
    forged = json.dumps(
        {
            "credential_marker_present": True,
            "credential_shaped_names": [MARKER_NAME],
            "automatic_memory": "1",
        },
        sort_keys=True,
    )
    return expect_rejection(
        "delegation_credential",
        lambda: audit_job_report("WP125-DELEGATED-REPORT " + forged, {"return_code": 0}),
    )


@case("WP125-NEG-045-delegated-test-selection-escape")
def negative_delegated_selection_escape() -> dict[str, object]:
    return expect_rejection(
        "delegation_scope",
        lambda: build_job(
            operation="run_test",
            candidate_head=INTEGRATION_HEAD,
            candidate_tree=INTEGRATION_TREE,
            test_selection=("../../etc/passwd",),
            read_only_root=str(CANDIDATE_ROOT),
            eligible=True,
        ),
    )


# --------------------------------------------------------------------------- parity


def _side(platform_name: str, ids: tuple[str, ...], **changes: object) -> parity_module.SideReport:
    base = {
        "platform": platform_name,
        "scheduled": ids,
        "outcomes": {case_id: "passed" for case_id in ids},
        "argument_observations": {"argv_preserved": True},
        "environment_observations": {"memory": "1"},
        "claim_ordering": ("preflight", "claim"),
        "fence_categories": {ids[0]: "completed_without_fence"},
    }
    base.update(changes)
    return parity_module.SideReport(**base)


@case("WP125-PAR-001-shrunken-denominator-is-red")
def parity_shrunken() -> dict[str, object]:
    ids = ("A", "B", "C")
    matrix = parity_module.compare(
        _side("windows", ids),
        _side("linux", ("A", "B"), outcomes={"A": "passed", "B": "passed"}),
        portable_ids=ids,
        platform_specific={},
    )
    ensure(matrix["ok"] is False, "a shrunken denominator was accepted")
    kinds = {finding["kind"] for finding in matrix["findings"]}
    ensure("shrunken_denominator" in kinds, "the shrunken denominator was not named")
    expect_rejection("parity_mismatch", lambda: parity_module.require_ok(matrix))
    return {"findings": len(matrix["findings"]), "kinds": sorted(kinds)}


@case("WP125-PAR-002-undeclared-not-applicable-is-red")
def parity_undeclared_na() -> dict[str, object]:
    ids = ("A", "B")
    matrix = parity_module.compare(
        _side("windows", ids),
        _side("linux", ids, outcomes={"A": "passed", "B": "skipped"}),
        portable_ids=ids,
        platform_specific={},
    )
    ensure(matrix["ok"] is False, "an undeclared not-applicable case was accepted")
    kinds = {finding["kind"] for finding in matrix["findings"]}
    ensure("undeclared_not_applicable" in kinds, "the undeclared skip was not named")
    return {"kinds": sorted(kinds)}


@case("WP125-PAR-003-outcome-divergence-is-red")
def parity_outcome_divergence() -> dict[str, object]:
    ids = ("A", "B")
    matrix = parity_module.compare(
        _side("windows", ids),
        _side("linux", ids, outcomes={"A": "passed", "B": "failed"}),
        portable_ids=ids,
        platform_specific={},
    )
    ensure(matrix["ok"] is False, "diverging outcomes were accepted")
    kinds = {finding["kind"] for finding in matrix["findings"]}
    ensure("outcome_divergence" in kinds, "the outcome divergence was not named")
    return {"kinds": sorted(kinds)}


@case("WP125-PAR-004-fence-category-divergence-is-red")
def parity_fence_divergence() -> dict[str, object]:
    ids = ("A", "B")
    matrix = parity_module.compare(
        _side("windows", ids),
        _side("linux", ids, fence_categories={"A": "cleanup_unproven"}),
        portable_ids=ids,
        platform_specific={},
    )
    ensure(matrix["ok"] is False, "a fence-category divergence was accepted")
    kinds = {finding["kind"] for finding in matrix["findings"]}
    ensure("fence_category_divergence" in kinds, "the fence divergence was not named")
    return {"kinds": sorted(kinds)}


@case("WP125-PAR-005-forged-success-report-is-red")
def parity_forged_success() -> dict[str, object]:
    """A side that reports success over a set it never scheduled is still red.

    This is the "forged success/cleanup report" case: the outcomes map says everything passed, but
    the scheduled list proves the cases were never run.  Comparing outcomes alone would accept it.
    """
    ids = ("A", "B", "C")
    forged = parity_module.SideReport(
        platform="linux",
        scheduled=(),
        outcomes={case_id: "passed" for case_id in ids},
        argument_observations={"argv_preserved": True},
        environment_observations={"memory": "1"},
        claim_ordering=("preflight", "claim"),
        fence_categories={"A": "completed_without_fence"},
    )
    matrix = parity_module.compare(
        _side("windows", ids), forged, portable_ids=ids, platform_specific={}
    )
    ensure(matrix["ok"] is False, "a forged success report was accepted")
    kinds = {finding["kind"] for finding in matrix["findings"]}
    ensure("shrunken_denominator" in kinds, "the forged report's empty schedule was not caught")
    return {"kinds": sorted(kinds)}


# --------------------------------------------------------------------------- driver


def run_matrix() -> dict[str, object]:
    """Run every registered case and return the machine-readable report."""
    registered = set(registry_module.CASES)
    implemented = {case_id for case_id, _ in CASES}
    not_run = sorted(registered - implemented)
    unknown = sorted(implemented - registered)

    records: list[dict[str, object]] = []
    executed = 0
    failed = 0
    for case_id, function in CASES:
        executed += 1
        try:
            evidence = function()
        except Exception as exc:  # noqa: BLE001 - every failure becomes a named red record
            failed += 1
            records.append(
                {
                    "case_id": case_id,
                    "required_check": registry_module.CASES[case_id],
                    "status": "failed",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
        else:
            if not evidence:
                failed += 1
                records.append(
                    {
                        "case_id": case_id,
                        "required_check": registry_module.CASES[case_id],
                        "status": "failed",
                        "error_type": "EmptyEvidence",
                        "error": "the case returned no evidence",
                    }
                )
            else:
                records.append(
                    {
                        "case_id": case_id,
                        "required_check": registry_module.CASES[case_id],
                        "status": "passed",
                        "evidence": evidence,
                    }
                )

    outcomes = {record["case_id"]: record["status"] for record in records}
    for case_id in not_run:
        outcomes[case_id] = "not_run"

    primary = parity_module.SideReport(
        platform="windows" if os.name == "nt" else sys.platform,
        scheduled=tuple(sorted(registered)),
        outcomes=outcomes,
        argument_observations={"argv_preserved": True},
        environment_observations={"memory": "1"},
        claim_ordering=tuple(STEP_NAMES) + ("claim",),
        fence_categories={
            "WP125-POS-003-healthy-child-completes-without-fence": "completed_without_fence",
            "WP125-POS-004-real-hang-is-fenced-without-cooperation": "fenced_by_controller",
        },
    )
    parity_report = parity_module.compare(
        primary,
        None,
        portable_ids=tuple(sorted(registered)),
        platform_specific=dict(registry_module.PLATFORM_SPECIFIC),
    )

    scheduled = len(registered)
    report: dict[str, object] = {
        "schema_version": 1,
        "suite": "wp125_launcher_matrix",
        "optimized": not __debug__,
        "scheduled": scheduled,
        "executed": executed,
        "passed": executed - failed,
        "failed": failed,
        "skipped": 0,
        "not_run": len(not_run),
        "not_run_cases": not_run,
        "cases_not_in_registry": unknown,
        "registry_coverage": registry_module.check_coverage(),
        "records": records,
        "parity": parity_report,
        "cleanup_records": CLEANUP_RECORDS,
        "delegation": DELEGATION_RECEIPT,
        "environment_names": ENVIRONMENT_NAMES,
    }
    report["ok"] = (
        scheduled > 0
        and executed == scheduled
        and report["passed"] == scheduled
        and failed == 0
        and report["skipped"] == 0
        and report["not_run"] == 0
        and not unknown
        and report["registry_coverage"]["ok"]
        and parity_report["ok"]
    )
    return report


def emit(value: object) -> None:
    """Write the machine-readable report as UTF-8, independent of the console code page.

    The default Windows console here is cp1258, which cannot encode the Vietnamese path used by the
    argument-boundary case — so a plain ``print`` turns a fully green suite into a ``UnicodeEncode``
    crash *after* every case has already passed.  The report is machine output; it must not be
    hostage to whatever the terminal happens to be set to.
    """
    import io

    stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    stream.write("\n")
    stream.flush()
    stream.detach()


def main() -> int:
    report = run_matrix()
    emit(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
