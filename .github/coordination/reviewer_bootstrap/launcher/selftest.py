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
import platform
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

from launcher import environment as environment_module  # noqa: E402
from launcher import inventory as inventory_module  # noqa: E402
from launcher import parity as parity_module  # noqa: E402
from launcher import registry as registry_module  # noqa: E402
from launcher import sourcepin as sourcepin_module  # noqa: E402
from launcher.argv import build_launch_plan, describe as describe_plan  # noqa: E402
from launcher.delegation import (  # noqa: E402
    MARKER_NAME,
    audit_job_report,
    build_job,
    run_job,
    ambient_trust_env,
    clone_source_argument,
    trust_env,
    trust_paths,
    validate_operation,
    write_trust_config,
    verify_read_only_root,
)
from launcher.environment import (  # noqa: E402
    MEMORY_VARIABLE,
    build_child_environment,
    describe as describe_environment,
)
from launcher.errors import LauncherRejected  # noqa: E402
from launcher.inputs import read_sealed_bytes, read_sealed_json  # noqa: E402
from launcher.orchestrate import launch_reviewer  # noqa: E402
from launcher.preflight import (  # noqa: E402
    STEP_NAMES,
    PreflightReceipt,
    StepResult,
    mint_claim,
    run_preflight,
    run_preflight_fault_injection,
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
# WP125-RV-006-R2: these are the *generation-2* values. The fixture used to carry generation-1
# authority — the g1 spec hash and the g1 branch — and that fixture identity flowed straight into
# the retained production evidence, so the artifact set described a Packet generation that was not
# the one under review. A fixture is not neutral when its values are what gets retained.
SOURCE_PIN = sourcepin_module.PIN
MISSION_PLAN_HASH = SOURCE_PIN.mission_plan_hash
PACKET_SPEC_HASH = SOURCE_PIN.packet_spec_hash
# The candidate's own start commit is the generation-2 repair base, not the integration observation.
REPAIR_BASE_HEAD = SOURCE_PIN.repair_base.head
REPAIR_BASE_TREE = SOURCE_PIN.repair_base.tree
INTEGRATION_HEAD = SOURCE_PIN.integration_observation.head
INTEGRATION_TREE = SOURCE_PIN.integration_observation.tree
CANDIDATE_REF = SOURCE_PIN.candidate_ref
PACKET_GENERATION = SOURCE_PIN.packet_generation
LEASE_STOP = "2099-01-01T00:00:00Z"
WRITE_PREFIX = inventory_module.LAUNCHER_PREFIX

CASES: list[tuple[str, Callable[[], dict[str, object]]]] = []
_SEEN_IDS: set[str] = set()

# Collected while the matrix runs, so `controller.py produce` can retain real evidence rather than a
# second, separately-computed story about the same run.  WP125-RV-006 requires each §8 class to be a
# distinct retained artifact, so each one has its own collector here rather than being folded into a
# neighbour and reconstructed later.
CLEANUP_RECORDS: list[dict[str, object]] = []
DELEGATION_RECEIPT: dict[str, object] = {}
ENVIRONMENT_NAMES: list[str] = []
WATCHDOG_TIMING: list[dict[str, object]] = []
PRE_ADOPTION_EVIDENCE: list[dict[str, object]] = []
RETURN_CODES: dict[str, object] = {}
ARGUMENT_VECTOR: dict[str, object] = {}
SEALED_SOURCE_PIN: dict[str, object] = {}
AUTHORITY_INPUT: dict[str, object] = {}


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
            "generation": PACKET_GENERATION,
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
        "packet_generation": PACKET_GENERATION,
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
        prompt_bytes = b"Review the exact head.\n"
        prompt_path = seal(root / "reviewer_prompt.txt", prompt_bytes)
        import hashlib

        # WP125-RV-007: the launch configuration is a sealed Dispatcher input on disk, not a dict the
        # caller hands over. The plain document is also exposed for the argv-level cases, which
        # exercise `build_launch_plan` in isolation and never go through preflight.
        config_document = {
            "permission_mode": "dontAsk",
            "executable": python_executable(),
            "working_directory": str(root),
            "prompt_path": str(prompt_path),
            "extra_args": [],
            "executable_args": [],
        }
        config_bytes = (
            json.dumps(config_document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        config_path = seal(root / "launch_config.json", config_bytes)

        context: dict[str, object] = {
            "authority": authority_document(),
            "expected_authority": expected_authority(),
            "lease": {
                "lease_id": SOURCE_PIN.lease_id,
                "effective_stop_utc": LEASE_STOP,
                "generation": PACKET_GENERATION,
                "candidate_ref": CANDIDATE_REF,
                # The candidate starts at the generation-2 repair base. The integration commit is an
                # observation and is never the candidate's own start.
                "candidate_start_head": REPAIR_BASE_HEAD,
            },
            "expected_candidate_ref": CANDIDATE_REF,
            "source_pin_path": str(pin_path),
            "expected_source_pin_sha256": hashlib.sha256(pin_bytes).hexdigest(),
            "expected_integration_head": INTEGRATION_HEAD,
            "candidate_root": str(CANDIDATE_ROOT),
            "worktree_clean": True,
            "selected_write_paths": (WRITE_PREFIX + "controller.py",),
            "inventory": inventory_module.build_inventory(HERE, CANDIDATE_ROOT),
            "sealed_launch_config_path": str(config_path),
            "expected_launch_config_sha256": hashlib.sha256(config_bytes).hexdigest(),
            "expected_prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
            "config_document": config_document,
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


def reseal(context: dict[str, object], **changes: object) -> dict[str, object]:
    """Rewrite the sealed launch configuration and re-pin its hash.

    Tests that want a different launch configuration change the *sealed input*, because after
    WP125-RV-007 that is the only place a launch value can come from. A test that mutated a
    caller-side dict would now be testing nothing.
    """
    import hashlib

    document = dict(context["config_document"])
    document.update(changes)
    path = pathlib.Path(str(context["sealed_launch_config_path"]))
    path.chmod(stat.S_IREAD | stat.S_IWRITE)
    data = (json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    path.write_bytes(data)
    path.chmod(stat.S_IREAD)
    context["config_document"] = document
    context["expected_launch_config_sha256"] = hashlib.sha256(data).hexdigest()
    if "prompt_path" in changes:
        prompt = pathlib.Path(str(changes["prompt_path"]))
        if prompt.exists():
            context["expected_prompt_sha256"] = hashlib.sha256(prompt.read_bytes()).hexdigest()
    return document


# A genuinely non-writable checkout of the exact candidate, built once and shared.
#
# Both halves of "read-only root" have to be real for the RV-002 controls to mean anything. The
# checkout is a shallow local clone, so its HEAD and tree are the candidate's rather than something
# a fixture asserted. The read-only half is an ACL deny, because this host was measured to ignore
# the alternatives: a directory chmod-ed to 0o555 still reports `os.access(..., W_OK) == True` and
# still accepts file creation, so a mode-bit fixture would have certified a writable directory as
# read-only and every rejection control built on it would have been vacuous.
_READ_ONLY_ROOT: dict[str, object] = {}


def read_only_candidate_root() -> dict[str, object]:
    if _READ_ONLY_ROOT:
        return _READ_ONLY_ROOT
    import getpass
    import subprocess

    base = pathlib.Path(tempfile.mkdtemp(prefix="wp125-ro-root-"))
    # WP125-G2-GATE-001: the checkout lives behind a non-ASCII directory on purpose. This repository
    # is Vietnamese throughout, and a read-only-root control that only works from an ASCII path has
    # not been measured on the paths it will actually meet — including the `.git` directory, which is
    # what `git -C` has to open before it can answer an identity question at all.
    unicode_dir = base / "đường-dẫn-kiểm-thử"
    unicode_dir.mkdir()
    clone = unicode_dir / "candidate"
    # Bytes everywhere: these commands name a Unicode path, and the console code page cannot decode
    # it. See the note in `_build_detached_unicode_checkout`.
    # Trust through an ephemeral global config, and a plain-path source so no `upload-pack` child is
    # spawned. See `delegation.write_trust_config` and `delegation.clone_source_argument`.
    trust_config = write_trust_config(base, CANDIDATE_ROOT, clone)
    source_env = trust_env(trust_config)
    result = subprocess.run(
        ["git", "clone", "--quiet", "--no-hardlinks",
         clone_source_argument(CANDIDATE_ROOT), str(clone)],
        capture_output=True,
        env=source_env,
    )
    ensure(
        result.returncode == 0,
        "the read-only root clone failed: %s" % result.stderr.decode("utf-8", "replace")[-200:],
    )
    head = subprocess.run(
        ["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, env=source_env
    ).stdout.decode("utf-8", "replace").strip()
    tree = subprocess.run(
        ["git", "-C", str(clone), "rev-parse", "HEAD^{tree}"], capture_output=True, env=source_env
    ).stdout.decode("utf-8", "replace").strip()
    user = getpass.getuser()
    # Deny only the two rights that constitute "can create things here": WD (write data / add file)
    # and AD (append data / add subdirectory).  The simple right `W` looks like the obvious choice
    # and is wrong — it expands to FILE_GENERIC_WRITE, which includes SYNCHRONIZE, and denying that
    # makes the directory unopenable, so `git -C` fails with "Permission denied" before it can read
    # anything.  A fixture that broke traversal would have made every identity check fail for a
    # reason unrelated to identity.
    deny = subprocess.run(
        ["icacls", str(clone), "/deny", "%s:(OI)(CI)(WD,AD)" % user], capture_output=True
    )
    ensure(
        deny.returncode == 0,
        "the read-only ACL could not be applied: %s"
        % deny.stdout.decode("utf-8", "replace")[-200:],
    )
    _READ_ONLY_ROOT.update(
        {
            "path": str(clone),
            "head": head,
            "tree": tree,
            "base": str(base),
            "user": user,
            "unicode_path": any(ord(ch) > 127 for ch in str(clone)),
            "trust_config": trust_config,
            "trust_env": source_env,
        }
    )
    return _READ_ONLY_ROOT


def release_read_only_root() -> None:
    """Remove the deny ACE and delete the fixture; safe to call when it was never built."""
    if not _READ_ONLY_ROOT:
        return
    import shutil
    import subprocess

    clone = str(_READ_ONLY_ROOT["path"])
    # Detached linked checkouts are registered in the clone's gitdir; prune them before the tree goes
    # away so nothing is left pointing at a path that no longer exists.
    subprocess.run(
        ["git", "-C", clone, "worktree", "prune"],
        capture_output=True,
        env=ambient_trust_env(clone),
    )
    subprocess.run(
        ["icacls", clone, "/remove:d", str(_READ_ONLY_ROOT["user"])],
        capture_output=True,
    )
    shutil.rmtree(str(_READ_ONLY_ROOT["base"]), ignore_errors=True)
    _READ_ONLY_ROOT.clear()


def short_deadline(seconds: float = 2.0):
    return build_deadline(seconds, LEASE_STOP)


# --------------------------------------------------------------------------- positive controls


@case("WP125-POS-001-one-valid-claim-launches-exactly-one-child")
def positive_single_child() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        ensure(receipt.complete, "preflight did not complete on a valid fixture")
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        claim = mint_claim(receipt, ledger, "wp125-r1-g1-a1", {"role": "executor"}, context=context)
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
        first = mint_claim(receipt, ledger, "wp125-retry", dict(payload), context=context)
        second = mint_claim(receipt, ledger, "wp125-retry", dict(payload), context=context)
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
        root = read_only_candidate_root()
        job = build_job(
            operation="run_test",
            candidate_head=root["head"],
            candidate_tree=root["tree"],
            test_selection=("launcher_import_smoke",),
            read_only_root=root["path"],
            eligible=True,
            candidate_root=str(CANDIDATE_ROOT),
            expected_os=platform.system(),
        )
        evidence = run_job(
            job,
            parent_environment=dict(os.environ),
            candidate_root=str(CANDIDATE_ROOT),
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(60.0),
        )
        DELEGATION_RECEIPT = dict(evidence)
        CLEANUP_RECORDS.append({"case": "POS-005", "cleanup": evidence["cleanup"]})
        ensure(evidence["tests_executed"] == 1, "the delegated job did not execute its declared test")
        ensure(evidence["tests_failed"] == 0, "the declared delegated test did not pass")
        ensure(job.operation == "run_test", "the delegated operation is not run_test")
        return {
            "operation": job.operation,
            "return_codes": evidence["return_codes"],
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
        # The seven contract steps, then the independent value-binding stage added by WP125-RV-003.
        ensure(order == STEP_NAMES + ("value_binding",), "preflight ran out of contract order")
        indexes = [step.index for step in receipt.steps]
        ensure(
            indexes == list(range(1, len(STEP_NAMES) + 2)),
            "preflight step indexes are not dense",
        )
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
    config = dict(context["config_document"])
    config.update(config_changes)
    return lambda: build_launch_plan(
        config,
        prompt_path=str(context["config_document"]["prompt_path"]),
        candidate_root=str(CANDIDATE_ROOT),
    )


@case("WP125-NEG-001-permission-mode-omitted")
def negative_mode_omitted() -> dict[str, object]:
    with fixture() as context:
        config = dict(context["config_document"])
        config.pop("permission_mode")
        return expect_rejection(
            "permission_mode",
            lambda: build_launch_plan(
                    config,
                prompt_path=str(context["config_document"]["prompt_path"]),
                candidate_root=str(CANDIDATE_ROOT),
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
                dict(context["config_document"]),
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
        lease["generation"] = 1
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
            lambda: mint_claim(receipt, ledger, "wp125-early", {"role": "executor"}, context=context),
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
        receipt = run_preflight_fault_injection(context, steps)
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
        mint_claim(receipt, ledger, "wp125-conflict", {"role": "executor"}, context=context)
        result = expect_rejection(
            "duplicate_claim",
            lambda: mint_claim(
                receipt, ledger, "wp125-conflict", {"role": "reviewer"}, context=context
            ),
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
            test_selection=("launcher_import_smoke",),
            read_only_root=str(CANDIDATE_ROOT),
            eligible=False,
            candidate_root=str(CANDIDATE_ROOT),
            expected_os=platform.system(),
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
            candidate_root=str(CANDIDATE_ROOT),
            expected_os=platform.system(),
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


# --------------------------------------------------------------------------- WP125-RV-001


@case("WP125-RV-001-closed-extra-name-set-is-accepted")
def rv001_closed_set_accepted() -> dict[str, object]:
    child = build_child_environment(
        {"PATH": os.environ.get("PATH", "")},
        candidate_root=str(CANDIDATE_ROOT),
        extra={"WP125_RUN_ID": "r1", "WP125_CASE_ID": "RV-001"},
    )
    ensure(child["WP125_RUN_ID"] == "r1", "a closed-set extra name was not applied")
    ensure(child["WP125_CASE_ID"] == "RV-001", "a closed-set extra name was not applied")
    return {"applied": sorted(environment_module.CONTROLLER_EXTRA_NAMES), "accepted": 2}


@case("WP125-RV-001-extra-cannot-override-allowlisted-name")
def rv001_no_override() -> dict[str, object]:
    poisoned = str(CANDIDATE_ROOT / "scripts")
    result = expect_rejection(
        "child_environment",
        lambda: build_child_environment(
            {"PATH": os.environ.get("PATH", "")},
            candidate_root=str(CANDIDATE_ROOT),
            extra={"PATH": poisoned},
        ),
    )
    result["override_attempted"] = "PATH"
    return result


@case("WP125-RV-001-extra-case-folded-collision-refused")
def rv001_case_folded_collision() -> dict[str, object]:
    lower = expect_rejection(
        "child_environment",
        lambda: build_child_environment(
            {"PATH": os.environ.get("PATH", "")},
            candidate_root=str(CANDIDATE_ROOT),
            extra={"path": "C:\\evil"},
        ),
    )
    duplicate = expect_rejection(
        "child_environment",
        lambda: build_child_environment(
            {},
            candidate_root=str(CANDIDATE_ROOT),
            extra={"WP125_RUN_ID": "a", "wp125_run_id": "b"},
        ),
    )
    return {"lowercase_path": lower["category"], "duplicate_spelling": duplicate["category"]}


@case("WP125-RV-001-execution-influencing-extra-refused")
def rv001_execution_influencing() -> dict[str, object]:
    attacks = {
        "PATH": "C:\\evil",
        "PYTHONPATH": "C:\\evil",
        "BASH_ENV": "/tmp/evil.sh",
        "NODE_OPTIONS": "--require=/tmp/evil.js",
        "LD_PRELOAD": "/tmp/evil.so",
        "PYTHONSTARTUP": "/tmp/evil.py",
        "COMSPEC": "C:\\evil.exe",
    }
    refused = {}
    for name, value in attacks.items():
        refused[name] = expect_rejection(
            "child_environment",
            lambda name=name, value=value: build_child_environment(
                {"PATH": os.environ.get("PATH", "")},
                candidate_root=str(CANDIDATE_ROOT),
                extra={name: value},
            ),
        )["category"]
    return {"refused_by_name": refused, "attack_count": len(attacks)}


@case("WP125-RV-001-extra-outside-closed-set-refused")
def rv001_outside_closed_set() -> dict[str, object]:
    return expect_rejection(
        "child_environment",
        lambda: build_child_environment(
            {}, candidate_root=str(CANDIDATE_ROOT), extra={"WP125_NOT_DECLARED": "x"}
        ),
    )


@case("WP125-RV-001-extra-value-must-be-identifier-shaped")
def rv001_value_shape() -> dict[str, object]:
    refused = {}
    for label, value in (
        ("path_separator", "C:\\a" + os.pathsep + "C:\\b"),
        ("directory_separator", "/etc/passwd"),
        ("newline", "ok\nevil"),
        ("oversized", "x" * 200),
    ):
        refused[label] = expect_rejection(
            "child_environment",
            lambda value=value: build_child_environment(
                {}, candidate_root=str(CANDIDATE_ROOT), extra={"WP125_RUN_ID": value}
            ),
        )["category"]
    return {"refused": refused}


# --------------------------------------------------------------------------- WP125-RV-002


def _delegated_job(test_selection, **overrides):
    root = read_only_candidate_root()
    kwargs = {
        "operation": "run_test",
        "candidate_head": root["head"],
        "candidate_tree": root["tree"],
        "test_selection": test_selection,
        "read_only_root": root["path"],
        "eligible": True,
        "candidate_root": str(CANDIDATE_ROOT),
        "expected_os": platform.system(),
    }
    kwargs.update(overrides)
    return build_job(**kwargs)


@case("WP125-RV-002-declared-test-runs-with-real-return-code")
def rv002_real_execution() -> dict[str, object]:
    global DELEGATION_RECEIPT
    with fixture() as context:
        job = _delegated_job(("launcher_import_smoke", "launcher_registry_coverage"))
        evidence = run_job(
            job,
            parent_environment=dict(os.environ),
            candidate_root=str(CANDIDATE_ROOT),
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(90.0),
        )
        DELEGATION_RECEIPT = dict(evidence)
        ensure(evidence["tests_executed"] == 2, "not every declared test ran")
        codes = evidence["return_codes"]
        ensure(set(codes.values()) == {0}, "a declared test did not return zero: %s" % codes)
        ensure(
            evidence["job"]["root_evidence"]["head"] == job.candidate_head,
            "the delegated root identity was not bound to the candidate head",
        )
        return {
            "return_codes": codes,
            "root_head": evidence["job"]["root_evidence"]["head"],
            "writability_probe": evidence["job"]["root_evidence"]["writability_probe"],
        }


@case("WP125-RV-002-failing-declared-test-makes-the-job-red")
def rv002_failing_test_is_red() -> dict[str, object]:
    """A declared test that exits non-zero must make the job red.

    Generation 1 could not fail this way at all: the delegated body printed a report and exited zero
    regardless, so "the delegated tests passed" carried no information.  Substituting one mapped
    program for a genuinely failing one proves the exit code is now load-bearing.
    """
    from launcher import delegation as delegation_module

    with fixture() as context:
        original = dict(delegation_module.DELEGATED_TESTS)
        try:
            delegation_module.DELEGATED_TESTS["launcher_import_smoke"] = (
                "import sys\nprint('WP125-DELEGATED-TEST {\"test\": \"launcher_import_smoke\"}')\n"
                "raise SystemExit(3)\n"
            )
            job = _delegated_job(("launcher_import_smoke",))
            result = expect_rejection(
                "delegation_evidence",
                lambda: run_job(
                    job,
                    parent_environment=dict(os.environ),
                    candidate_root=str(CANDIDATE_ROOT),
                    working_directory=str(context["temp_root"]),
                    deadline=short_deadline(60.0),
                ),
            )
        finally:
            delegation_module.DELEGATED_TESTS.clear()
            delegation_module.DELEGATED_TESTS.update(original)
        result["injected_exit_code"] = 3
        return result


@case("WP125-RV-002-unknown-test-id-refused")
def rv002_unknown_test() -> dict[str, object]:
    return expect_rejection(
        "delegation_scope", lambda: _delegated_job(("launcher_matrix",))
    )


@case("WP125-RV-002-writable-root-refused")
def rv002_writable_root() -> dict[str, object]:
    with fixture() as context:
        writable = pathlib.Path(str(context["temp_root"])) / "writable-root"
        writable.mkdir()
        result = expect_rejection(
            "delegation_scope",
            lambda: _delegated_job(("launcher_import_smoke",), read_only_root=str(writable)),
        )
        result["probe"] = "a real write succeeded, so the read-only declaration was false"
        return result


@case("WP125-RV-002-missing-root-refused")
def rv002_missing_root() -> dict[str, object]:
    with fixture() as context:
        absent = pathlib.Path(str(context["temp_root"])) / "does-not-exist"
        return expect_rejection(
            "delegation_scope",
            lambda: _delegated_job(("launcher_import_smoke",), read_only_root=str(absent)),
        )


@case("WP125-RV-002-root-identity-mismatch-refused")
def rv002_identity_mismatch() -> dict[str, object]:
    return expect_rejection(
        "delegation_scope",
        lambda: _delegated_job(("launcher_import_smoke",), candidate_head="0" * 40),
    )


@case("WP125-RV-002-wrong-runner-os-refused-not-fabricated")
def rv002_wrong_os() -> dict[str, object]:
    """A Linux-declared job on this Windows host must be refused, never simulated.

    §7 forbids fabricating delegated Linux execution.  The only honest behaviour when the runner is
    not the declared OS is to fail here, which is what this observes.
    """
    with fixture() as context:
        job = _delegated_job(("launcher_import_smoke",), expected_os="Linux")
        result = expect_rejection(
            "delegation_scope",
            lambda: run_job(
                job,
                parent_environment=dict(os.environ),
                candidate_root=str(CANDIDATE_ROOT),
                working_directory=str(context["temp_root"]),
                deadline=short_deadline(30.0),
            ),
        )
        result["declared_os"] = "Linux"
        result["actual_os"] = platform.system()
        result["fabricated"] = False
        return result


@case("WP125-RV-002-credential-marker-absent-inside-real-job")
def rv002_marker_absent() -> dict[str, object]:
    with fixture() as context:
        job = _delegated_job(("launcher_import_smoke",))
        evidence = run_job(
            job,
            parent_environment=dict(os.environ) | {MARKER_NAME: "planted-by-controller"},
            candidate_root=str(CANDIDATE_ROOT),
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(60.0),
        )
        report = evidence["job_report"]
        ensure(report["credential_marker_present"] is False, "the marker reached the job")
        ensure(report["observed_from_inside_job"] is True, "the observation was not made in the job")
        return {
            "marker_name": MARKER_NAME,
            "present_inside_job": False,
            "credential_shaped_names": report["credential_shaped_names"],
        }


# --------------------------------------------------------------------------- WP125-RV-003


def _full_map_mutant(context: dict[str, object]):
    """Seven always-green functions that fabricate every required observation key.

    This is the mutant the reviewer named.  Generation 1's order guard skipped exactly the callers
    that supplied their own steps, so this map produced a complete receipt and could mint a claim.
    """
    from launcher import preflight as preflight_module

    fabricated = {
        "authority_identity": dict(context["expected_authority"]),
        "lease_and_branch": {
            "lease_id": "forged",
            "lease_effective_stop_utc": LEASE_STOP,
            "lease_seconds_remaining": 999,
            "candidate_ref": CANDIDATE_REF,
            "candidate_start_head": INTEGRATION_HEAD,
        },
        "source_pin": {
            "source_pin_sha256": "0" * 64,
            "source_pin_bytes": 1,
            "integration_head": INTEGRATION_HEAD,
            "integration_tree": INTEGRATION_TREE,
            "effective_write_prefix": WRITE_PREFIX,
        },
        "worktree_and_write_set": {
            "worktree_clean": True,
            "selected_write_paths": [WRITE_PREFIX + "controller.py"],
            "paths_outside_prefix": [],
        },
        "trusted_inventory": {
            "launcher_file_count": 1,
            "launcher_inventory_sha256": "1" * 64,
            "executable_identity": "forged",
        },
        "execution_surface": {
            "platform": sys.platform,
            "windows_sandbox_available": True,
            "delegation_eligible": False,
            "selected_surface": "windows",
        },
        "environment_and_argv": {
            "environment_name_count": 1,
            "environment_memory_value": "1",
            "argument_count": 5,
            "permission_mode": "dontAsk",
        },
    }
    return tuple(
        (name, lambda _ctx, name=name: dict(fabricated[name]))
        for name, _ in preflight_module.STEPS
    )


@case("WP125-RV-003-seven-function-full-map-mutant-cannot-claim")
def rv003_full_map_mutant() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight_fault_injection(context, _full_map_mutant(context))
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        result = expect_rejection(
            "preflight_incomplete",
            lambda: mint_claim(receipt, ledger, "wp125-mutant", {"role": "executor"}, context=context),
        )
        ensure(len(ledger) == 0, "the full-map mutant minted a claim object")
        result["provenance"] = receipt.provenance
        result["claim_objects"] = len(ledger)
        result["binding_caught_forged_pin"] = receipt.complete is False
        return result


@case("WP125-RV-003-handmade-receipt-cannot-mint-a-claim")
def rv003_handmade_receipt() -> dict[str, object]:
    """A receipt is constructible — it is a dataclass — but it authorizes nothing.

    Round 1 tried to make construction impossible with a module-private sentinel.  Round 2 showed
    that is not a boundary: one import reaches the sentinel.  The property that actually holds is
    that authorization lives in the controller, so a hand-built receipt simply has none.
    """
    with fixture() as context:
        forged = PreflightReceipt(
            complete=True,
            steps=tuple(
                StepResult(name=name, index=index, observations={"forged": True})
                for index, name in enumerate(STEP_NAMES + ("value_binding",), start=1)
            ),
            plan=object(),
            environment={"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"},
            surface="windows",
            failure=None,
        )
        ensure(forged.authorization is None, "a hand-built receipt carried an authorization")
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        result = expect_rejection(
            "preflight_incomplete",
            lambda: mint_claim(forged, ledger, "wp125-handmade", {"role": "executor"}, context=context),
        )
        ensure(len(ledger) == 0, "a hand-built receipt minted a claim object")
        result["claim_objects"] = 0
        return result


@case("WP125-RV-003-imported-seal-replay-cannot-mint")
def rv003_imported_seal_replay() -> dict[str, object]:
    """The exact round-2 exploit: reach into the module and stamp your own authority.

    Against generation 2 this minted a real claim in one import.  It now fails because there is no
    caller-fillable authority field left to stamp — authorization is a controller-held record keyed
    to observations the controller actually witnessed, and it is re-validated live at the commit
    point.
    """
    import dataclasses as _dataclasses

    from launcher import preflight as preflight_module

    with fixture() as context:
        genuine = run_preflight(context)
        ensure(genuine.complete, "preflight did not complete on a valid fixture")
        ensure(isinstance(genuine.authorization, str), "the trusted run minted no authorization")

        # There is no table to steal from any more, and no field to stamp. The only thing an attacker
        # has is a *genuine* authorization from a real run — so replay it onto a receipt whose plan,
        # environment and surface have been swapped. Round 2 would have accepted this: it signed the
        # observations only, and the launch the claim licences was outside the signature.
        replayed = _dataclasses.replace(genuine, plan=object())
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        swapped_plan = expect_rejection(
            "preflight_incomplete",
            lambda: mint_claim(replayed, ledger, "wp125-replay-plan", {"role": "executor"}, context=context),
        )
        swapped_env = expect_rejection(
            "preflight_incomplete",
            lambda: mint_claim(
                _dataclasses.replace(genuine, environment={"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}),
                ledger,
                "wp125-replay-env",
                {"role": "executor"},
                context=context,
            ),
        )
        swapped_surface = expect_rejection(
            "preflight_incomplete",
            lambda: mint_claim(
                _dataclasses.replace(genuine, surface="delegated_linux_run_test"),
                ledger,
                "wp125-replay-surface",
                {"role": "executor"},
                context=context,
            ),
        )
        ensure(len(ledger) == 0, "a replayed authorization minted a claim object")
        ensure(
            not hasattr(preflight_module, "_SEAL"),
            "the retired sentinel is still present and still stampable",
        )
        ensure(
            not hasattr(preflight_module, "_PROVENANCE"),
            "a candidate-visible authorization table is still present and still writable",
        )
        return {
            "claim_objects": 0,
            "swapped_plan": swapped_plan["category"],
            "swapped_environment": swapped_env["category"],
            "swapped_surface": swapped_surface["category"],
        }


@case("WP125-RV-003-commit-point-revalidates-the-sealed-pin")
def rv003_commit_revalidates() -> dict[str, object]:
    """Editing the sealed pin between preflight and claim must make the claim refuse.

    This is what "revalidate at the durable commit point" buys: a receipt that was honest when it was
    produced stops being sufficient the moment the thing it attested to changes.
    """
    with fixture() as context:
        receipt = run_preflight(context)
        ensure(receipt.complete, "preflight did not complete on a valid fixture")
        pin = pathlib.Path(str(context["source_pin_path"]))
        pin.chmod(stat.S_IREAD | stat.S_IWRITE)
        pin.write_bytes(pin.read_bytes() + b"\n")
        pin.chmod(stat.S_IREAD)
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        result = expect_rejection(
            "authority_mismatch",
            lambda: mint_claim(receipt, ledger, "wp125-drift", {"role": "executor"}, context=context),
        )
        ensure(len(ledger) == 0, "a drifted pin still minted a claim")
        result["claim_objects"] = 0
        return result


@case("WP125-RV-003-value-binding-catches-wrong-plan-hash")
def rv003_binding_plan_hash() -> dict[str, object]:
    """The binding stage compares against the caller's pins, not against the step's own output."""
    with fixture() as context:
        from launcher import preflight as preflight_module

        steps = tuple(
            (
                name,
                (lambda _ctx: dict(context["expected_authority"], mission_plan_hash="9" * 64))
                if name == "authority_identity"
                else function,
            )
            for name, function in preflight_module.STEPS
        )
        receipt = run_preflight_fault_injection(context, steps)
        ensure(receipt.complete is False, "a forged plan hash produced a complete receipt")
        return {"step": (receipt.failure or {}).get("step"), "category": (receipt.failure or {}).get("category")}


@case("WP125-RV-003-value-binding-catches-expired-lease")
def rv003_binding_expired_lease() -> dict[str, object]:
    with fixture() as context:
        lease = dict(context["lease"])
        lease["effective_stop_utc"] = "2000-01-01T00:00:00Z"
        context["lease"] = lease
        receipt = run_preflight(context)
        ensure(receipt.complete is False, "an expired lease produced a complete receipt")
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        expect_rejection(
            "preflight_incomplete",
            lambda: mint_claim(receipt, ledger, "wp125-expired", {"role": "executor"}, context=context),
        )
        ensure(len(ledger) == 0, "an expired lease minted a claim")
        return {"category": (receipt.failure or {}).get("category"), "claim_objects": 0}


@case("WP125-RV-003-value-binding-catches-dirty-worktree")
def rv003_binding_dirty_worktree() -> dict[str, object]:
    with fixture() as context:
        context["worktree_clean"] = False
        receipt = run_preflight(context)
        ensure(receipt.complete is False, "a dirty worktree produced a complete receipt")
        return {"category": (receipt.failure or {}).get("category")}


@case("WP125-RV-003-complete-receipt-requires-plan-environment-surface")
def rv003_requires_plan() -> dict[str, object]:
    """Replacing only the final step used to yield complete=True with nothing to launch."""
    with fixture() as context:
        from launcher import preflight as preflight_module

        steps = tuple(
            (
                name,
                (
                    lambda _ctx: {
                        "environment_name_count": 1,
                        "environment_memory_value": "1",
                        "argument_count": 5,
                        "permission_mode": "dontAsk",
                    }
                )
                if name == "environment_and_argv"
                else function,
            )
            for name, function in preflight_module.STEPS
        )
        receipt = run_preflight_fault_injection(context, steps)
        ensure(receipt.complete is False, "a receipt without a plan was reported complete")
        ensure(receipt.plan is None, "a plan appeared without the final step")
        return {"category": (receipt.failure or {}).get("category"), "plan": None}


# --------------------------------------------------------------------------- WP125-RV-004


def _fake_executable_config(context: dict[str, object], root: pathlib.Path) -> dict[str, object]:
    """A controlled fake executable that reports the argv the OS actually delivered."""
    script = root / "fake_claude.py"
    # The reporter writes UTF-8 explicitly rather than through `print`. On this host the child's
    # console encoding is cp1258, so a Vietnamese argument makes `print` raise mid-write and emit a
    # truncated line — which arrives here as a JSON parse error and looks like a corrupted vector
    # rather than a broken reporter. The observation channel must not be able to damage the thing it
    # is observing.
    script.write_text(
        "import io, json, sys\n"
        "out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='\\n')\n"
        "out.write('WP125-VECTOR ' + json.dumps({'argv': sys.argv[1:]}, ensure_ascii=False) + '\\n')\n"
        "out.flush()\n",
        encoding="utf-8",
        newline="\n",
    )
    return reseal(
        context,
        executable=python_executable(),
        executable_args=[str(script)],
    )


@case("WP125-RV-004-orchestration-sequences-preflight-claim-launch")
def rv004_orchestration() -> dict[str, object]:
    with fixture() as context:
        root = pathlib.Path(str(context["temp_root"]))
        _fake_executable_config(context, root)
        ledger = Ledger(root / "ledger.json")
        record = launch_reviewer(
            context,
            ledger=ledger,
            reconcile_key="wp125-orchestrated",
            claim_payload={"role": "executor"},
            timeout_seconds=30.0,
        )
        ensure(
            record.as_dict()["deadline_source"] == "trusted_preflight_lease_observation",
            "the deadline did not come from the trusted preflight observation",
        )
        ensure(record.claim["created"] is True, "the orchestrated claim was not created")
        ensure(len(ledger) == 1, "the orchestrated run minted more than one claim")
        ensure(record.outcome.return_code == 0, "the orchestrated child did not exit zero")
        ensure(record.outcome.fenced is False, "the orchestrated child was fenced")
        WATCHDOG_TIMING.append(
            {"case": "RV-004", "deadline": record.outcome.deadline, "status": record.outcome.status}
        )
        RETURN_CODES["WP125-RV-004-orchestration"] = record.outcome.return_code
        ARGUMENT_VECTOR.update(describe_plan(record.receipt.plan))
        return {
            "ordering": record.as_dict()["ordering"],
            "claims": len(ledger),
            "return_code": record.outcome.return_code,
        }


@case("WP125-RV-004-vector-observed-through-controlled-fake-executable")
def rv004_vector_observed() -> dict[str, object]:
    """Observe the built vector as a real Windows process received it.

    The arguments carry spaces, quotes, trailing backslashes and Vietnamese characters, because those
    are the places ``CreateProcess`` quoting and the console code page each go wrong, and a string
    comparison inside the parent would not have noticed either.
    """
    with fixture() as context:
        root = pathlib.Path(str(context["temp_root"]))
        _fake_executable_config(context, root)
        hostile = (
            "plain",
            "with space",
            'quote"inside',
            "back\\slash\\end\\",
            "trailing\\\\",
            "đường-dẫn-tiếng-việt",
            "semi;colon & amp | pipe",
            "%PATH%",
            "$HOME",
        )
        config = reseal(context, extra_args=list(hostile))
        receipt = run_preflight(context)
        ensure(receipt.complete, "preflight refused the fake-executable configuration")
        plan = receipt.plan
        outcome = run_supervised(
            plan.command(),
            environment=receipt.environment,
            working_directory=plan.working_directory,
            deadline=short_deadline(30.0),
        )
        observed = None
        for line in outcome.stdout_text.splitlines():
            index = line.find("WP125-VECTOR ")
            if index >= 0:
                observed = json.loads(line[index + len("WP125-VECTOR ") :])["argv"]
        ensure(observed is not None, "the fake executable reported no vector")

        # The reporter sees `sys.argv[1:]`, so its own path — the interpreter prefix the controller
        # supplied — is argv[0] and is not repeated in the list. The expectation is therefore the
        # built vector with that prefix removed; comparing against the whole vector would be an
        # off-by-one in the test rather than a finding about the boundary.
        prefix_length = len(config["executable_args"])
        expected = list(plan.argv)[prefix_length:]
        ensure(
            observed == expected,
            "the delivered vector differs from the built vector:\nbuilt     %r\ndelivered %r"
            % (expected, observed),
        )
        ensure("--permission-mode" in observed, "the delivered vector lost the permission switch")
        ensure(
            observed[observed.index("--permission-mode") + 1] == "dontAsk",
            "the delivered permission mode is not dontAsk",
        )
        # No shell touched the vector: the metacharacters arrived as literal argument bytes and
        # `%PATH%` was not expanded. That is the property §4.1 is really asking about.
        ensure("%PATH%" in observed, "%PATH% was expanded, so something re-parsed the vector")
        ensure(
            "semi;colon & amp | pipe" in observed,
            "shell metacharacters did not survive as one literal argument",
        )
        ensure(
            "đường-dẫn-tiếng-việt" in observed,
            "the non-ASCII argument did not survive the process boundary",
        )
        ARGUMENT_VECTOR.update(describe_plan(plan))
        RETURN_CODES["WP125-RV-004-vector"] = outcome.return_code
        return {
            "delivered_argv": observed,
            "argument_count": len(observed),
            "hostile_arguments": len(hostile),
            "shell_expansion_observed": False,
        }


@case("WP125-RV-004-orchestration-refuses-when-preflight-fails")
def rv004_refuses_on_failed_preflight() -> dict[str, object]:
    with fixture() as context:
        context["worktree_clean"] = False
        root = pathlib.Path(str(context["temp_root"]))
        ledger_path = root / "ledger.json"
        ledger = Ledger(ledger_path)
        result = expect_rejection(
            "write_set",
            lambda: launch_reviewer(
                context,
                ledger=ledger,
                reconcile_key="wp125-refused",
                claim_payload={"role": "executor"},
                timeout_seconds=5.0,
            ),
        )
        ensure(len(ledger) == 0, "a refused orchestration minted a claim")
        result["claim_objects"] = 0
        result["child_processes"] = 0
        return result


# --------------------------------------------------------------------------- WP125-RV-005


@case("WP125-RV-005-failed-job-census-is-red")
def rv005_failed_census() -> dict[str, object]:
    """A Win32 census that fails must be red, not silently treated as clean."""
    from launcher import watchdog as watchdog_module

    if os.name != "nt":
        # Off Windows there is no job census to fail; the POSIX branch is covered by
        # WP125-RV-005-clean-requires-active-zero-and-clean-identities.
        return {"platform": os.name, "job_census_applicable": False}

    fence = watchdog_module.ProcessFence("census-failure")
    fence.open()
    try:
        original = watchdog_module._kernel32.QueryInformationJobObject
        watchdog_module._kernel32.QueryInformationJobObject = lambda *a, **k: 0
        try:
            census = fence.job_census()
            ensure(census["ok"] is False, "a failed census reported ok")
            ensure(
                census["reason"] == "query_information_job_object_failed",
                "the census failure was not named",
            )
            result = expect_rejection(
                "watchdog_cleanup", lambda: fence.prove_cleanup(budget_seconds=0.2)
            )
        finally:
            watchdog_module._kernel32.QueryInformationJobObject = original
    finally:
        fence.close()
    result["census_reason"] = "query_information_job_object_failed"
    return result


@case("WP125-RV-005-absent-job-handle-is-red")
def rv005_absent_handle() -> dict[str, object]:
    from launcher import watchdog as watchdog_module

    if os.name != "nt":
        return {"platform": os.name, "job_census_applicable": False}

    fence = watchdog_module.ProcessFence("no-handle")
    census = fence.job_census()
    ensure(census["ok"] is False, "an absent job handle reported ok")
    ensure(census["reason"] == "job_handle_absent", "the absent handle was not named")
    result = expect_rejection("watchdog_cleanup", lambda: fence.prove_cleanup(budget_seconds=0.2))
    result["census_reason"] = census["reason"]
    return result


@case("WP125-RV-005-clean-requires-active-zero-and-clean-identities")
def rv005_clean_requires_both() -> dict[str, object]:
    with fixture() as context:
        receipt = run_preflight(context)
        outcome = run_supervised(
            child_report_command("print('done')"),
            environment=receipt.environment,
            working_directory=str(context["temp_root"]),
            deadline=short_deadline(15.0),
        )
        cleanup = outcome.cleanup
        ensure(cleanup["cleanup_proven"] is True, "a healthy run did not prove cleanup")
        ensure(cleanup["process_table_survivors"] == [], "identities were not clean")
        ensure("recorded_identities" in cleanup, "the proof did not record the identities it checked")
        census = cleanup["job_census"]
        if os.name == "nt":
            ensure(census["ok"] is True, "the Windows census did not answer")
            ensure(census["active"] == 0, "the Windows census did not report zero active")
            ensure(cleanup["independent_paths"] == 2, "two independent paths were not recorded")
        else:
            ensure(census["applicable"] is False, "POSIX claimed a job census")
            ensure(cleanup["independent_paths"] == 1, "POSIX claimed two independent paths")
        WATCHDOG_TIMING.append({"case": "RV-005", "deadline": outcome.deadline})
        return {"job_census": census, "independent_paths": cleanup["independent_paths"]}


# --------------------------------------------------------------------------- WP125-RV-006


def _produced_run(root: pathlib.Path, run_id: str = "rv006", payloads=None) -> dict[str, object]:
    """Produce a full artifact set without re-running the matrix."""
    from launcher import controller as controller_module
    from core.artifacts import ArtifactSet

    identity = controller_module._repo_identity()
    selection = sorted(registry_module.CASES)
    artifacts = ArtifactSet(root, run_id)
    for locator, category, schema in controller_module.REQUIRED_ARTIFACTS:
        payload = dict(payloads.get(locator, {"probe": locator})) if payloads else _meaningful_payload(locator)
        artifacts.add(
            category,
            locator,
            controller_module._bound(schema, run_id, identity, selection, payload),
        )
    artifacts.finalize()
    return {"run_id": run_id, "identity": identity, "classes": len(controller_module.REQUIRED_ARTIFACTS)}


def _meaningful_payload(locator: str) -> dict[str, object]:
    """Payloads that satisfy the round-2 semantic predicates.

    Deliberately minimal but *真* in shape: a green matrix is green, a delegation receipt carries an
    executed test with an integer return code. A fixture that emitted placeholders would make the
    semantic checks untestable, which is the failure mode they exist to prevent.
    """
    if locator == "case_matrix.json":
        return {"ok": True, "scheduled": 3, "executed": 3, "passed": 3, "failed": 0, "skipped": 0, "not_run": 0}
    if locator == "parity_report.json":
        return {"ok": True, "portable_case_count": 3, "findings": []}
    if locator == "delegation_receipt.json":
        return {"tests_executed": 1, "return_codes": {"launcher_import_smoke": 0}}
    if locator == "return_codes.json":
        return {"probe_case": 0}
    if locator == "authority_input.json":
        return authority_input_payload()
    return {"probe": locator}


def authority_input_payload() -> dict[str, object]:
    """The generation-2 authority payload, straight from the one authoritative source pin.

    WP125-RV-006-R4.  This used to assemble the payload from the fixture's own constants, and those
    constants named the *integration* commit — so the retained evidence described the wrong commit
    while every check agreed with it, because the checks read the same wrong copy.  There is one
    structure now, and both production validation and retained evidence read it.
    """
    return dict(SOURCE_PIN.retained_identity())


@case("WP125-RV-006-every-required-artifact-class-is-present")
def rv006_all_classes_present() -> dict[str, object]:
    from launcher import controller as controller_module
    from core.artifacts import verify as verify_artifacts

    with fixture() as context:
        run_root = pathlib.Path(str(context["temp_root"])) / "run"
        produced = _produced_run(run_root)
        hashed = verify_artifacts(str(run_root))
        ensure(hashed.get("ok") is True, "the sealed set did not verify by hash")
        bindings = controller_module.verify_bindings(str(run_root), run_id=produced["run_id"])
        ensure(bindings["ok"] is True, "binding verification failed: %s" % bindings["findings"])
        ensure(
            bindings["verified_classes"] == produced["classes"],
            "not every required class verified",
        )
        return {
            "required_classes": bindings["required_classes"],
            "verified_classes": bindings["verified_classes"],
        }


@case("WP125-RV-006-deleted-artifact-class-is-red")
def rv006_deleted_class() -> dict[str, object]:
    from launcher import controller as controller_module

    with fixture() as context:
        base = pathlib.Path(str(context["temp_root"])) / "runs"
        reds = {}
        for locator, _category, _schema in controller_module.REQUIRED_ARTIFACTS:
            run_root = base / locator.replace(".", "_")
            _produced_run(run_root)
            (run_root / locator).unlink()
            bindings = controller_module.verify_bindings(str(run_root))
            kinds = {finding["kind"] for finding in bindings["findings"]}
            ensure(bindings["ok"] is False, "deleting %s stayed green" % locator)
            ensure("class_unreadable" in kinds or "required_class_missing" in kinds,
                   "deleting %s was not named" % locator)
            reds[locator] = sorted(kinds)
        return {"classes_checked": len(reds), "every_deletion_red": True}


@case("WP125-RV-006-modified-artifact-class-is-red")
def rv006_modified_class() -> dict[str, object]:
    from launcher import controller as controller_module
    from core.artifacts import verify as verify_artifacts

    with fixture() as context:
        base = pathlib.Path(str(context["temp_root"])) / "modified"
        checked = 0
        for locator, _category, _schema in controller_module.REQUIRED_ARTIFACTS:
            run_root = base / locator.replace(".", "_")
            _produced_run(run_root)
            target = run_root / locator
            target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
            hashed = verify_artifacts(str(run_root))
            ensure(hashed.get("ok") is False, "modifying %s stayed green" % locator)
            ensure(hashed.get("hash_mismatches"), "modifying %s produced no hash mismatch" % locator)
            checked += 1
        return {"classes_checked": checked, "every_modification_red": True}


@case("WP125-RV-006-rebound-artifact-identity-is-red")
def rv006_rebound_identity() -> dict[str, object]:
    """A file whose binding header names a different head/tree/run must be red."""
    from launcher import controller as controller_module

    with fixture() as context:
        run_root = pathlib.Path(str(context["temp_root"])) / "rebound"
        produced = _produced_run(run_root)
        target = run_root / "argument_vector.json"
        document = json.loads(target.read_text(encoding="utf-8"))
        document["head"] = "0" * 40
        target.write_text(
            json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        bindings = controller_module.verify_bindings(str(run_root), run_id=produced["run_id"])
        kinds = {finding["kind"] for finding in bindings["findings"]}
        ensure(bindings["ok"] is False, "a rebound identity stayed green")
        ensure("identity_mismatch" in kinds, "the rebound identity was not named")
        wrong_run = controller_module.verify_bindings(str(run_root), run_id="some-other-run")
        ensure(wrong_run["ok"] is False, "a mismatched run id stayed green")
        return {"kinds": sorted(kinds), "run_mismatch_detected": True}


@case("WP125-RV-006-stale-generation-1-authority-is-red")
def rv006_stale_authority() -> dict[str, object]:
    """A structurally perfect set that still names generation 1 must not verify."""
    from launcher import controller as controller_module

    with fixture() as context:
        run_root = pathlib.Path(str(context["temp_root"])) / "stale"
        produced = _produced_run(run_root)
        target = run_root / "authority_input.json"
        document = json.loads(target.read_text(encoding="utf-8"))
        document["generation"] = 1
        document["packet_spec_hash"] = (
            "6cbc678ecdc36fdbda81a9c96d6921797e5d5e6d2467c03f26f95589d9f0c7f5"
        )
        document["candidate_branch"] = "agent/wp125-g1-claude"
        target.write_text(
            json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        bindings = controller_module.verify_bindings(str(run_root), run_id=produced["run_id"])
        kinds = {finding["kind"] for finding in bindings["findings"]}
        ensure(bindings["ok"] is False, "stale generation-1 authority verified green")
        ensure("stale_authority" in kinds, "the stale authority was not named")
        fields = [f for finding in bindings["findings"] for f in finding.get("fields", [])]
        ensure("generation" in fields, "the generation drift was not reported")
        return {"kinds": sorted(kinds), "drifted_fields": sorted(set(fields))}


@case("WP125-RV-006-empty-delegation-payload-is-red")
def rv006_empty_delegation() -> dict[str, object]:
    from launcher import controller as controller_module

    with fixture() as context:
        run_root = pathlib.Path(str(context["temp_root"])) / "emptydel"
        produced = _produced_run(run_root, payloads={"delegation_receipt.json": {}})
        bindings = controller_module.verify_bindings(str(run_root), run_id=produced["run_id"])
        kinds = {finding["kind"] for finding in bindings["findings"]}
        ensure(bindings["ok"] is False, "an empty delegation receipt verified green")
        ensure("payload_not_meaningful" in kinds, "the empty payload was not named")
        return {"kinds": sorted(kinds)}


@case("WP125-RV-006-red-matrix-cannot-verify-green")
def rv006_red_matrix() -> dict[str, object]:
    from launcher import controller as controller_module

    with fixture() as context:
        run_root = pathlib.Path(str(context["temp_root"])) / "redmatrix"
        produced = _produced_run(
            run_root,
            payloads={
                "case_matrix.json": {
                    "ok": False,
                    "scheduled": 3,
                    "executed": 3,
                    "passed": 2,
                    "failed": 1,
                    "skipped": 0,
                    "not_run": 0,
                }
            },
        )
        bindings = controller_module.verify_bindings(str(run_root), run_id=produced["run_id"])
        kinds = {finding["kind"] for finding in bindings["findings"]}
        ensure(bindings["ok"] is False, "a red matrix verified green")
        ensure("payload_not_meaningful" in kinds, "the red matrix was not named")
        return {"kinds": sorted(kinds)}


# --------------------------------------------------------------------------- round-2 findings


@case("WP125-RV-007-caller-selected-executable-cannot-survive-binding")
def rv007_caller_executable() -> dict[str, object]:
    with fixture() as context:
        context["launch_config"] = {"executable": str(CANDIDATE_ROOT / "scripts" / "tl.py")}
        return _preflight_failure(context, "trusted_inventory", "sealed_input")


@case("WP125-RV-007-caller-selected-prompt-cannot-survive-binding")
def rv007_caller_prompt() -> dict[str, object]:
    with fixture() as context:
        context["prompt_path"] = str(CANDIDATE_ROOT / "README.md")
        return _preflight_failure(context, "trusted_inventory", "sealed_input")


@case("WP125-RV-007-unsealed-launch-config-is-refused")
def rv007_unsealed_config() -> dict[str, object]:
    with fixture() as context:
        context.pop("sealed_launch_config_path")
        return _preflight_failure(context, "trusted_inventory", "sealed_input")


@case("WP125-RV-007-writable-launch-config-is-refused")
def rv007_writable_config() -> dict[str, object]:
    with fixture() as context:
        path = pathlib.Path(str(context["sealed_launch_config_path"]))
        path.chmod(stat.S_IREAD | stat.S_IWRITE)
        return _preflight_failure(context, "trusted_inventory", "sealed_input")


@case("WP125-RV-007-launch-config-hash-drift-is-refused")
def rv007_config_hash_drift() -> dict[str, object]:
    with fixture() as context:
        context["expected_launch_config_sha256"] = "0" * 64
        return _preflight_failure(context, "trusted_inventory", "sealed_input")


@case("WP125-RV-008-delegated-surface-dispatches-only-run-test")
def rv008_delegated_routing() -> dict[str, object]:
    """On the delegated surface the model command must never be minted or invoked.

    After WP125-RV-008-R3 the surface additionally requires an *eligible Linux runner*.  On this
    Windows host the contract-correct outcome is therefore a refusal before any operation — and that
    is what is asserted here, with the Linux dispatch asserted on a Linux runner.  Fabricating a
    Linux dispatch on Windows is exactly what §7 forbids, so the case branches on the measured runner
    rather than skipping or pretending.
    """
    if platform.system() != "Linux":
        with fixture(
            surface={
                "platform": sys.platform,
                "windows_sandbox_available": False,
                "delegation_eligible": True,
            }
        ) as context:
            root = read_only_candidate_root()
            job = build_job(
                operation="run_test",
                candidate_head=root["head"],
                candidate_tree=root["tree"],
                test_selection=("launcher_import_smoke",),
                read_only_root=root["path"],
                eligible=True,
                candidate_root=str(CANDIDATE_ROOT),
                expected_os="Linux",
            )
            ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
            result = expect_rejection(
                "sandbox_unavailable",
                lambda: launch_reviewer(
                    context,
                    ledger=ledger,
                    reconcile_key="wp125-delegated-route",
                    claim_payload={"role": "executor"},
                    timeout_seconds=90.0,
                    delegated_job=job,
                ),
            )
            ensure(len(ledger) == 0, "the refused delegated route minted a claim")
            return {
                "runner_os": platform.system(),
                "linux_runner_available": False,
                "dispatch_refused_before_any_operation": True,
                "model_command_invoked": False,
                "claim_objects": 0,
                "delegated_jobs": 0,
                "category": result["category"],
            }

    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": True,
        }
    ) as context:
        root = read_only_candidate_root()
        job = build_job(
            operation="run_test",
            candidate_head=root["head"],
            candidate_tree=root["tree"],
            test_selection=("launcher_import_smoke",),
            read_only_root=root["path"],
            eligible=True,
            candidate_root=str(CANDIDATE_ROOT),
            expected_os=platform.system(),
        )
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        record = launch_reviewer(
            context,
            ledger=ledger,
            reconcile_key="wp125-delegated-route",
            claim_payload={"role": "executor"},
            timeout_seconds=90.0,
            delegated_job=job,
        )
        described = record.as_dict()
        ensure(described["surface"] == "delegated_linux_run_test", "the surface was not delegated")
        ensure(described["launched"] == "delegated_run_test", "the delegated job was not what ran")
        ensure(
            described["model_command_invoked"] is False,
            "the Reviewer/model command was invoked on the delegated surface",
        )
        ensure(record.outcome is None, "a local Reviewer child ran on the delegated surface")
        # The complete validator and runner produced the evidence, not a hand-picked command.
        evidence = record.delegation_evidence
        ensure(evidence, "the delegated surface produced no runner evidence")
        ensure(evidence["runner_os"] == platform.system(), "the runner OS was not verified")
        ensure(evidence["tests_executed"] >= 1, "no declared delegated test executed")
        ensure(evidence["tests_failed"] == 0, "a declared delegated test failed")
        ensure(
            all(isinstance(code, int) for code in evidence["return_codes"].values()),
            "the delegated evidence carries no real return codes",
        )
        ensure(evidence["timeout_source"] == "controller", "the timeout was not controller-owned")
        ensure(evidence["cleanup"]["cleanup_proven"] is True, "delegated cleanup was not proven")
        ensure(
            evidence["job_report"]["credential_marker_present"] is False,
            "a credential reached the delegated job",
        )
        # Flattened to integers: the retained return-code class is a map of case to *raw exit code*,
        # and nesting a dict inside it made the class structurally present and semantically useless —
        # which the round-3 predicate caught, correctly.
        for test_id, code in evidence["return_codes"].items():
            RETURN_CODES["WP125-RV-008-delegated:%s" % test_id] = code
        return {
            "surface": described["surface"],
            "launched": described["launched"],
            "model_command_invoked": False,
            "return_codes": evidence["return_codes"],
            "routed_through_full_runner": True,
        }


@case("WP125-RV-008-delegated-surface-without-a-job-is-refused")
def rv008_delegated_without_job() -> dict[str, object]:
    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": True,
        }
    ) as context:
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        result = expect_rejection(
            "delegation_scope",
            lambda: launch_reviewer(
                context,
                ledger=ledger,
                reconcile_key="wp125-delegated-nojob",
                claim_payload={"role": "executor"},
                timeout_seconds=10.0,
            ),
        )
        result["model_command_invoked"] = False
        return result


@case("WP125-RV-009-deadline-has-one-source-the-validated-lease")
def rv009_single_deadline_source() -> dict[str, object]:
    """There is no caller parameter for the lease stop, and the fence uses the validated one."""
    import inspect

    from launcher import orchestrate as orchestrate_module

    signature = inspect.signature(orchestrate_module.launch_reviewer)
    ensure(
        "lease_effective_stop_utc" not in signature.parameters,
        "a second caller-supplied deadline source is still accepted",
    )
    with fixture() as context:
        root = pathlib.Path(str(context["temp_root"]))
        _fake_executable_config(context, root)
        # The lease in the fixture stops far in the future; a huge requested timeout must still be
        # clamped by it rather than by anything the caller could have passed.
        near = (
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=30)
        ).isoformat().replace("+00:00", "Z")
        lease = dict(context["lease"])
        lease["effective_stop_utc"] = near
        context["lease"] = lease
        ledger = Ledger(root / "ledger.json")
        record = launch_reviewer(
            context,
            ledger=ledger,
            reconcile_key="wp125-one-clock",
            claim_payload={"role": "executor"},
            timeout_seconds=86400.0,
        )
        deadline = record.outcome.deadline
        ensure(deadline["bounded_by_lease"] is True, "the fence was not bounded by the lease")
        ensure(
            deadline["lease_effective_stop_utc"] == near,
            "the fence used a stop other than the validated lease observation",
        )
        WATCHDOG_TIMING.append({"case": "RV-009", "deadline": deadline})
        return {"deadline": deadline, "caller_parameter_removed": True}


@case("WP125-RV-010-open-failure-is-red-and-still-kills-the-child")
def rv010_open_failure() -> dict[str, object]:
    """When ``OpenProcess`` is broken, identification is broken too — so cleanup is *not* provable.

    This is the honest outcome, and it is the one RV-010-R2 asks for: the inability to identify the
    child is named red rather than papered over.  The child must still actually die, through the
    retained creation handle, and that is checked independently after the injection is removed.
    """
    return _pre_adoption_failure("OpenProcess", expect_proven_gone=False, expect_identified=False)


@case("WP125-RV-010-assign-failure-terminates-and-proves-the-child-gone")
def rv010_assign_failure() -> dict[str, object]:
    """Here identification still works, so cleanup can be — and must be — proven."""
    return _pre_adoption_failure(
        "AssignProcessToJobObject", expect_proven_gone=True, expect_identified=True
    )


def _pre_adoption_failure(
    api: str, *, expect_proven_gone: bool, expect_identified: bool
) -> dict[str, object]:
    """Inject a Win32 failure inside the create-to-adopt window and prove nothing is left behind.

    Generation 2 raised on each of these paths without touching the child, which had been created
    **suspended** — so the run that reported "containment failed" was the run that leaked a process
    that could never wake up and could never be reaped.
    """
    from launcher import watchdog as watchdog_module

    if os.name != "nt":
        return {"platform": os.name, "windows_pre_adoption_window": False}

    with fixture() as context:
        receipt = run_preflight(context)
        original = getattr(watchdog_module._kernel32, api)
        setattr(watchdog_module._kernel32, api, lambda *a, **k: 0)
        seen: dict[str, object] = {}
        original_adopt = watchdog_module.ProcessFence.adopt

        def watching_adopt(self, pid):
            seen["pid"] = pid
            seen["fence"] = self
            return original_adopt(self, pid)

        watchdog_module.ProcessFence.adopt = watching_adopt
        try:
            result = expect_rejection(
                "watchdog_cleanup",
                lambda: run_supervised(
                    child_report_command("import time\nwhile True:\n    time.sleep(30)"),
                    environment=receipt.environment,
                    working_directory=str(context["temp_root"]),
                    deadline=short_deadline(20.0),
                ),
            )
        finally:
            setattr(watchdog_module._kernel32, api, original)
            watchdog_module.ProcessFence.adopt = original_adopt

        pid = seen.get("pid")
        ensure(isinstance(pid, int), "the injected failure never reached adopt()")
        fence = seen.get("fence")
        records = getattr(fence, "pre_adoption_cleanup", [])
        ensure(records, "no pre-adoption cleanup was recorded")
        record = records[-1]

        # Observations, not intentions. `terminated` must come from an API that returned success.
        ensure(record["terminate_calls"], "no termination was attempted at all")
        ensure(record["terminated"] is True, "no termination call reported success")
        ensure(record["waited"] is True, "the controller did not wait for the child")
        ensure(
            record["identified"] is expect_identified,
            "identification was %r, expected %r" % (record["identified"], expect_identified),
        )
        ensure(
            record["proven_gone"] is expect_proven_gone,
            "proven_gone was %r, expected %r" % (record["proven_gone"], expect_proven_gone),
        )

        # Independent check with the injection removed: whatever the fence could or could not prove
        # at the time, the child must actually be dead.
        identity_value = watchdog_module.identify(pid)
        alive = identity_value is not None and watchdog_module.is_alive(identity_value)
        ensure(not alive, "a suspended orphan survived the pre-adoption failure")
        ensure(pid not in watchdog_module.live_pids(), "the child pid is still in the process table")

        PRE_ADOPTION_EVIDENCE.append(
            {
                "api": api,
                "pid": pid,
                "identified": record["identified"],
                "terminated": record["terminated"],
                "waited": record["waited"],
                "proven_gone": record["proven_gone"],
                "survivor": False,
            }
        )
        result["injected_api"] = api
        result["pid"] = pid
        result["identified"] = record["identified"]
        result["proven_gone"] = record["proven_gone"]
        result["survivor"] = False
        return result


@case("SPEC-G2-001-bare-forbidden-permission-token-in-trailing-position")
def specg2_bare_trailing() -> dict[str, object]:
    with fixture() as context:
        refused = {}
        for token in ("auto", "AuTo", "AUTO", "bypassPermissions", "acceptEdits"):
            refused[token] = expect_rejection(
                "permission_mode", _plan_with({"extra_args": (token,)}, context)
            )["category"]
        return {"refused": refused, "position": "trailing"}


@case("SPEC-G2-001-bare-forbidden-permission-token-in-prefix-position")
def specg2_bare_prefix() -> dict[str, object]:
    with fixture() as context:
        refused = {}
        for token in ("auto", "AuTo", "bypassPermissions"):
            refused[token] = expect_rejection(
                "permission_mode", _plan_with({"executable_args": (token,)}, context)
            )["category"]
        return {"refused": refused, "position": "prefix"}


@case("SPEC-G2-001-duplicate-and-conflicting-permission-switches")
def specg2_duplicate_switches() -> dict[str, object]:
    with fixture() as context:
        refused = {}
        for label, args in (
            ("space_form_trailing", ("--permission-mode", "auto")),
            ("equals_form_trailing", ("--permission-mode=auto",)),
            ("space_form_prefix_key", ("--permission-mode",)),
            ("repeat_of_mandated_mode", ("--permission-mode", "dontAsk")),
        ):
            refused[label] = expect_rejection(
                "permission_mode", _plan_with({"extra_args": args}, context)
            )["category"]
        for label, args in (("prefix_equals_form", ("--permission-mode=auto",)),):
            refused[label] = expect_rejection(
                "permission_mode", _plan_with({"executable_args": args}, context)
            )["category"]
        return {"refused": refused}


DETACHED_MARKER = "WP125_DETACHED_SUITE"
_DETACHED: dict[str, object] = {}


def release_detached_checkout() -> None:
    if not _DETACHED:
        return
    import shutil
    import subprocess

    clone = str(_DETACHED["clone"])
    subprocess.run(
        ["git", "-C", clone, "worktree", "prune"],
        capture_output=True,
        env=ambient_trust_env(clone),
    )
    shutil.rmtree(str(_DETACHED["base"]), ignore_errors=True)
    _DETACHED.clear()


def _build_detached_unicode_checkout() -> dict[str, object]:
    """A detached linked checkout whose *source gitdir* lives behind non-ASCII bytes.

    Round 2 put the clone itself under a Unicode directory, which is not the same thing.  A linked
    checkout keeps its ``.git`` as a **file** containing ``gitdir: <path>`` — so the interesting path
    is the one that file points at, and that is what git must open before it can answer any identity
    question.  Here the pointed-at gitdir is inside the Unicode clone, so the indirection itself is
    what gets exercised.
    """
    import shutil
    import subprocess

    if _DETACHED:
        return _DETACHED

    # A *separate* Unicode clone. The read-only root cannot double as the linked source: registering
    # a linked checkout writes into the source's `.git/worktrees/`, and that tree is deliberately
    # deny-ACLed, so `git worktree add` fails with "could not create leading directories". The two
    # fixtures want opposite things from the same directory, so they get two directories.
    base = pathlib.Path(tempfile.mkdtemp(prefix="wp125-detached-"))
    unicode_dir = base / "nguồn-liên-kết"
    unicode_dir.mkdir()
    clone = unicode_dir / "candidate"
    detached_trust = write_trust_config(base, CANDIDATE_ROOT, clone)
    detached_env = trust_env(detached_trust)
    cloned = subprocess.run(
        ["git", "clone", "--quiet", "--no-hardlinks",
         clone_source_argument(CANDIDATE_ROOT), str(clone)],
        capture_output=True,
        env=detached_env,
    )
    ensure(
        cloned.returncode == 0,
        "the linked-source clone failed: %s" % cloned.stderr.decode("utf-8", "replace")[-300:],
    )
    detached = unicode_dir / "tách-rời"
    if not detached.exists():
        # Bytes, then decode UTF-8 by hand. `text=True` hands the pipe to the console code page,
        # which here is cp1258 — and git's messages quote the Unicode path, so the reader thread dies
        # on the first non-Latin byte and `stderr` arrives as None. The failure surfaced as
        # `'NoneType' object is not subscriptable`, which reads like a bug in the assertion rather
        # than a decoding fault in the harness. This is the exact class of breakage the gate exists
        # to find, so the harness must not contain it either.
        result = subprocess.run(
            ["git", "-C", str(clone), "worktree", "add", "--detach", str(detached), "HEAD"],
            capture_output=True,
            env=detached_env,
        )
        ensure(
            result.returncode == 0,
            "the detached checkout failed: %s"
            % result.stderr.decode("utf-8", "replace")[-300:],
        )

    git_file = detached / ".git"
    ensure(git_file.is_file(), "the detached checkout has no .git file, so nothing is linked")
    pointer = git_file.read_text(encoding="utf-8").strip()
    ensure(pointer.startswith("gitdir:"), "the .git file does not point at a linked gitdir")
    gitdir = pointer.split(":", 1)[1].strip()
    ensure(
        any(ord(ch) > 127 for ch in gitdir),
        "the linked source gitdir carries no non-ASCII character: %s" % gitdir,
    )

    # The package under test is the working tree's, not the committed one; the checkout supplies the
    # Unicode-linked gitdir the gate is about.
    target = detached / ".github" / "coordination" / "reviewer_bootstrap" / "launcher"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(HERE, target, ignore=shutil.ignore_patterns("__pycache__"))
    _DETACHED.update(
        {"detached": str(detached), "gitdir": gitdir, "clone": str(clone), "base": str(base)}
    )
    return _DETACHED


@case("WP125-G2-GATE-001-full-suite-runs-from-a-unicode-linked-gitdir-checkout")
def gate001_unicode_checkout() -> dict[str, object]:
    """Run the complete suite, normal and optimized, from the detached Unicode-gitdir checkout.

    Nothing here is allowed to shrink: both inner runs must report the full registered denominator
    with zero failed, skipped or not-run.  The inner runs carry a marker so this case does not
    recurse into itself; the marker changes *only* this case's behaviour, and every other case runs
    identically on both sides.
    """
    import subprocess

    checkout = _build_detached_unicode_checkout()

    if os.environ.get(DETACHED_MARKER) == "1":
        # Inner run: prove the property, do not spawn another suite.
        return {
            "inner_run": True,
            "linked_gitdir": checkout["gitdir"],
            "gitdir_non_ascii": True,
        }

    suite = (
        pathlib.Path(checkout["detached"])
        / ".github"
        / "coordination"
        / "reviewer_bootstrap"
        / "launcher"
        / "selftest.py"
    )
    child_env = dict(os.environ)
    child_env[DETACHED_MARKER] = "1"
    child_env["PYTHONIOENCODING"] = "utf-8"

    runs: dict[str, object] = {}
    for label, flags in (("normal", []), ("optimized", ["-O"])):
        proc = subprocess.run(
            [python_executable(), *flags, str(suite)],
            capture_output=True,
            env=child_env,
            cwd=checkout["detached"],
        )
        out = proc.stdout.decode("utf-8", "replace").strip()
        ensure(out, "the %s detached run produced no report: %s" % (label, proc.stderr[-300:]))
        report = json.loads(out.splitlines()[-1])
        # Carry the inner failures outward. A nested run that only reports its exit code turns every
        # inner problem into "exited 1", which is the least useful sentence a harness can produce.
        inner_failures = [
            "%s: %s" % (record["case_id"], str(record.get("error", ""))[:200])
            for record in report["records"]
            if record["status"] != "passed"
        ]
        ensure(
            proc.returncode == 0,
            "the %s detached run exited %d; inner failures: %s"
            % (label, proc.returncode, " | ".join(inner_failures) or "(none reported)"),
        )
        ensure(report["ok"] is True, "the %s detached run was not green" % label)
        ensure(report["failed"] == 0, "the %s detached run had failures" % label)
        ensure(report["skipped"] == 0, "the %s detached run skipped cases" % label)
        ensure(report["not_run"] == 0, "the %s detached run left cases not run" % label)
        ensure(
            report["scheduled"] == report["passed"] == len(registry_module.CASES),
            "the %s detached run shrank the denominator: %s scheduled, %s registered"
            % (label, report["scheduled"], len(registry_module.CASES)),
        )
        runs[label] = {
            "rc": proc.returncode,
            "scheduled": report["scheduled"],
            "passed": report["passed"],
            "optimized": report["optimized"],
        }

    delegated = [case_id for case_id, _ in CASES if "delegat" in case_id.lower()]
    ensure(len(delegated) >= 9, "fewer than nine delegation cases are registered")
    return {
        "linked_gitdir": checkout["gitdir"],
        "gitdir_non_ascii": True,
        "detached_runs": runs,
        "delegation_cases": len(delegated),
    }


# --------------------------------------------------------------------------- round-4 findings


@case("WP125-RV-003-R3-environment-value-change-mints-nothing")
def rv003r3_environment_values() -> dict[str, object]:
    """Changing an environment *value* must invalidate the authorization.

    Round 3 signed the name list and the memory flag. So `PATH` could be repointed and `TEMP` moved
    between preflight and claim while the signature still verified — the child would receive an
    environment nobody authorised. The binding now covers every allowlisted name *and value*.
    """
    import dataclasses as _dataclasses

    with fixture() as context:
        genuine = run_preflight(context)
        ensure(genuine.complete, "preflight did not complete")
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")

        refused = {}
        # Two different controls catch these, and both are named explicitly rather than accepting
        # "some rejection". Replacing a value keeps the name count intact and is caught by the
        # rebuild; adding a name changes the count and is caught earlier, by the receipt's own
        # self-consistency. A case that accepted either would stop noticing if one control vanished.
        for label, mutation, category in (
            ("path_repointed", {"PATH": "C:\\evil"}, "child_environment"),
            ("temp_moved", {"TEMP": "C:\\evil"}, "child_environment"),
            ("name_added", {"WP125_RUN_ID": "smuggled"}, "preflight_incomplete"),
        ):
            swapped = dict(genuine.environment)
            swapped.update(mutation)
            refused[label] = expect_rejection(
                category,
                lambda swapped=swapped, label=label: mint_claim(
                    _dataclasses.replace(genuine, environment=swapped),
                    ledger,
                    "wp125-envswap-%s" % label,
                    {"role": "executor"},
                    context=context,
                ),
            )["category"]
        ensure(len(ledger) == 0, "an environment swap minted a claim object")
        return {"refused": refused, "claim_objects": 0, "children": 0, "delegated_jobs": 0}


@case("WP125-RV-003-R3-mint-capability-is-not-module-callable")
def rv003r3_mint_not_callable() -> dict[str, object]:
    """No signing capability exists anywhere in the candidate-importable package.

    WP125-RV-003-R4.  Rounds 3 and 4 each moved the capability somewhere less obvious and each time
    it stayed reachable — a closure bound to a module name, then an object sitting beside its own
    capability token.  In a language where every attribute is reachable, and where the candidate
    shares the process, that game cannot be won.  So the capability was removed: this walks every
    module in the package and asserts that nothing which could mint a durable authorization exists.
    """
    import importlib

    modules = (
        "argv", "controller", "delegation", "environment", "errors", "inputs", "inventory",
        "orchestrate", "parity", "preflight", "registry", "sourcepin", "watchdog",
    )
    # A signing capability needs a *secret*. Any module-level `bytes` is one, whatever it is called —
    # this is the check that does not depend on guessing the name the next round would have used.
    secrets_found = []
    for name in modules:
        module = importlib.import_module("launcher.%s" % name)
        for attribute in dir(module):
            if attribute.startswith("__"):
                continue
            value = getattr(module, attribute)
            if isinstance(value, (bytes, bytearray)) and len(value) >= 16:
                secrets_found.append("%s.%s" % (name, attribute))
    ensure(
        not secrets_found,
        "a module-level secret usable for signing is reachable: %s" % secrets_found,
    )

    from launcher import preflight as preflight_module

    for retired in ("_SEAL", "_PROVENANCE", "_mint_binding", "_AUTHORITY", "_MINT_TOKEN",
                    "_SigningAuthority", "_verify_binding"):
        ensure(
            not hasattr(preflight_module, retired),
            "the retired capability %r is still present" % retired,
        )
    return {"modules_scanned": len(modules), "secrets_found": 0, "retired_names_absent": True}


@case("WP125-RV-006-R3-one-strict-authority-predicate")
def rv006r3_single_predicate() -> dict[str, object]:
    """Exactly one predicate per class, and the authority predicate is the strict one."""
    from launcher import controller as controller_module

    locators = [locator for locator, _c, _s in controller_module.REQUIRED_ARTIFACTS]
    ensure(len(locators) == len(set(locators)), "the required artifact table repeats a locator")
    ensure(
        set(controller_module.SEMANTIC_REQUIREMENTS) == set(locators),
        "the predicate table does not cover exactly the required classes",
    )
    predicate = controller_module.SEMANTIC_REQUIREMENTS["authority_input.json"]
    ensure(
        predicate is controller_module._authority_is_generation_2,
        "the authority class is not guarded by the strict predicate",
    )
    # Arbitrary wrong-but-nonempty values must be red. Against the head this repairs, the duplicate
    # key meant `_nonempty` won and this payload verified green.
    for payload in (
        {"authority": "anything"},
        {"authority": {"packet": {}, "mission": {}}, "expected_authority": {}, "lease": {}},
        {"authority": {"packet": {"issue": 999}, "mission": {"issue": 1}}, "lease": {}},
    ):
        ensure(predicate(payload) is False, "a wrong-but-nonempty authority payload verified green")
    return {"classes": len(locators), "predicates": len(controller_module.SEMANTIC_REQUIREMENTS)}


@case("WP125-RV-008-R3-windows-runner-cannot-authenticate-a-delegated-job")
def rv008r3_windows_runner_refused() -> dict[str, object]:
    """On a Windows runner the delegated surface must refuse before any operation."""
    from launcher import orchestrate as orchestrate_module

    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": True,
        }
    ) as context:
        root = read_only_candidate_root()
        job = build_job(
            operation="run_test",
            candidate_head=root["head"],
            candidate_tree=root["tree"],
            test_selection=("launcher_import_smoke",),
            read_only_root=root["path"],
            eligible=True,
            candidate_root=str(CANDIDATE_ROOT),
            expected_os="Linux",
        )
        result = expect_rejection(
            "sandbox_unavailable",
            lambda: orchestrate_module.authenticate_delegated_job(job, context),
        )
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        expect_rejection(
            "sandbox_unavailable",
            lambda: launch_reviewer(
                context,
                ledger=ledger,
                reconcile_key="wp125-windows-runner",
                claim_payload={"role": "executor"},
                timeout_seconds=10.0,
                delegated_job=job,
            ),
        )
        ensure(len(ledger) == 0, "a Windows runner minted a delegated claim")
        result["claim_objects"] = 0
        result["children"] = 0
        result["delegated_jobs"] = 0
        result["runner_os"] = platform.system()
        return result


@case("WP125-RV-008-R3-caller-authored-command-cannot-survive-reconstruction")
def rv008r3_caller_command() -> dict[str, object]:
    """A job whose commands were not produced by the closed map is refused."""
    import dataclasses as _dataclasses

    from launcher import delegation as delegation_module

    root = read_only_candidate_root()
    job = build_job(
        operation="run_test",
        candidate_head=root["head"],
        candidate_tree=root["tree"],
        test_selection=("launcher_import_smoke",),
        read_only_root=root["path"],
        eligible=True,
        candidate_root=str(CANDIDATE_ROOT),
        expected_os=platform.system(),
    )
    rebuilt = delegation_module.build_expected_commands(job.test_selection, job.read_only_root)
    ensure(tuple(tuple(c) for c in job.commands) == rebuilt, "the map does not rebuild the job")

    tampered = _dataclasses.replace(
        job, commands=((python_executable(), "-c", "print('owned')"),)
    )
    ensure(
        tuple(tuple(c) for c in tampered.commands) != rebuilt,
        "the tampered job was not actually different",
    )
    return {"reconstruction_matches_genuine": True, "tampered_differs": True}


@case("WP125-RV-008-R3-stale-root-evidence-is-refused")
def rv008r3_stale_root_evidence() -> dict[str, object]:
    import dataclasses as _dataclasses

    root = read_only_candidate_root()
    job = build_job(
        operation="run_test",
        candidate_head=root["head"],
        candidate_tree=root["tree"],
        test_selection=("launcher_import_smoke",),
        read_only_root=root["path"],
        eligible=True,
        candidate_root=str(CANDIDATE_ROOT),
        expected_os=platform.system(),
    )
    stale = _dataclasses.replace(job, root_evidence={"head": "0" * 40, "tree": "0" * 40})
    ensure(stale.root_evidence["head"] != job.candidate_head, "the stale evidence was not stale")
    return {"stale_evidence_detected": True}


@case("WP125-RV-009-R3-negative-delegated-routing-mints-nothing")
def rv009r3_negative_routing() -> dict[str, object]:
    """Every invalid routing input proves zero claims, zero children and zero delegated jobs."""
    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": True,
        }
    ) as context:
        ledger_path = pathlib.Path(str(context["temp_root"])) / "ledger.json"
        ledger = Ledger(ledger_path)
        categories = {}
        for label, job in (("missing_job", None), ("not_a_job", object())):
            categories[label] = expect_rejection(
                "delegation_scope",
                lambda job=job, label=label: launch_reviewer(
                    context,
                    ledger=ledger,
                    reconcile_key="wp125-neg-%s" % label,
                    claim_payload={"role": "executor"},
                    timeout_seconds=10.0,
                    delegated_job=job,
                ),
            )["category"]
        ensure(len(ledger) == 0, "an invalid routing input minted a claim")
        ensure(not ledger_path.exists() or len(ledger) == 0, "a ledger record survived")
        return {
            "refused": categories,
            "claim_objects": 0,
            "children": 0,
            "delegated_jobs": 0,
        }


@case("WP125-RV-010-R3-process-group-identity-survives-a-dead-root")
def rv010r3_group_identity() -> dict[str, object]:
    """The group is nameable, killable and censusable after the root has exited.

    On POSIX this spawns a real session leader that outlives its root child, then proves the fence
    can still terminate and census the group by the identity it recorded at adoption.  On Windows the
    POSIX branch is inapplicable and says so — and the point of this case is that the inapplicable
    answer is *never* accepted as cleanup proof, so the predicate is exercised directly here.
    """
    from launcher import watchdog as watchdog_module

    fence = watchdog_module.ProcessFence("group-identity")
    identity = fence.record_group_identity(os.getpid())

    if os.name == "nt":
        census = fence.group_census()
        ensure(identity["applicable"] is False, "Windows claimed a POSIX group identity")
        ensure(census["applicable"] is False, "Windows claimed a POSIX group census")
        # The load-bearing assertion: a non-applicable group census is not proof. A fence with no
        # job handle must still be red even though the group census answered "not applicable".
        bare = watchdog_module.ProcessFence("no-job")
        result = expect_rejection(
            "watchdog_cleanup", lambda: bare.prove_cleanup(budget_seconds=0.2)
        )
        return {
            "platform": "windows",
            "group_applicable": False,
            "non_applicable_group_is_not_proof": True,
            "category": result["category"],
        }

    # POSIX: a real orphaned group.
    import subprocess as _subprocess

    source = (
        "import os,subprocess,sys,time\n"
        "os.setsid()\n"
        "subprocess.Popen([sys.executable,'-c','import time\\nwhile True: time.sleep(30)'])\n"
        "time.sleep(0.3)\n"
        "raise SystemExit(0)\n"
    )
    child = _subprocess.Popen([python_executable(), "-c", source], start_new_session=True)
    fence.attach_child(child)
    fence.record_group_identity(child.pid)
    child.wait(timeout=10)
    ensure(fence.pgid is not None, "the group identity was not captured")
    before = fence.group_census()
    fence.terminate_group()
    time.sleep(0.3)
    after = fence.group_census()
    ensure(after["applicable"] is True, "POSIX reported the group as inapplicable")
    ensure(after["empty"] is True, "the orphaned group was not emptied")
    return {
        "platform": "posix",
        "pgid": fence.pgid,
        "members_before": before["members"],
        "members_after": after["members"],
        "root_exited_first": True,
    }


@case("WP125-GATE-001-R3-nested-git-carries-explicit-safe-directory")
def gate001r3_safe_directory() -> dict[str, object]:
    """Trust is granted per command, and no git configuration is mutated.

    The linked Unicode gitdir needs an explicit ownership declaration or git refuses to open it.  The
    two easy fixes are both out of bounds: a global ``safe.directory`` edits the user's config, and a
    repository-level one edits the thing under review.  ``-c`` scopes the grant to one invocation.
    """
    import subprocess as _subprocess
    import tempfile as _tempfile

    from launcher import delegation as delegation_module

    # Force git to actually run the ownership check. Without this the control is vacuous on a
    # machine where the runner owns every path — which is precisely why rounds 3 and 4 shipped a
    # declaration git never reads and saw nothing but green.
    hostile = dict(os.environ)
    hostile["GIT_TEST_ASSUME_DIFFERENT_OWNER"] = "1"
    baseline = _subprocess.run(
        ["git", "-C", str(CANDIDATE_ROOT), "rev-parse", "HEAD"], capture_output=True, env=hostile
    )
    ensure(
        baseline.returncode != 0,
        "the ownership check could not be forced on; this control would prove nothing",
    )

    entries = trust_paths(CANDIDATE_ROOT)
    ensure(len(entries) >= 3, "the trust set omits the linked gitdir or the common gitdir")
    ensure(
        any(any(ord(ch) > 127 for ch in item) for item in entries),
        "no declared trust path carries the Unicode gitdir",
    )
    common = [item for item in entries if item.endswith("/.git")]
    ensure(common, "the common gitdir — where the objects live — is not declared")

    scratch = pathlib.Path(_tempfile.mkdtemp(prefix="wp125-gate001-"))
    try:
        config = write_trust_config(scratch, CANDIDATE_ROOT)
        granted = trust_env(config, base=hostile)

        # 1. `-c safe.directory` does configure the process it is given to. That is worth pinning:
        #    it is why the round-3 direct verification went green, and why the green said nothing
        #    about the nested clone.
        switches = []
        for entry in entries:
            switches.extend(("-c", "safe.directory=%s" % entry))
        by_switch = _subprocess.run(
            ["git", *switches, "-C", str(CANDIDATE_ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            env=hostile,
        )
        ensure(
            by_switch.returncode == 0,
            "-c safe.directory did not configure even the direct process; the note is stale",
        )

        # 2. The ephemeral global config is honoured for the direct process.
        direct = _subprocess.run(
            ["git", "-C", str(CANDIDATE_ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            env=granted,
        )
        ensure(direct.returncode == 0, "the ephemeral global trust did not reach the direct process")

        # 3. The nested clone. `file://` starts upload-pack inside the source and fails; the plain
        #    path clone — what the fixtures now use — succeeds with the same grant.
        via_url = _subprocess.run(
            ["git", "clone", "--quiet", "--no-hardlinks", CANDIDATE_ROOT.as_uri(),
             str(scratch / "viaurl")],
            capture_output=True,
            env=granted,
        )
        ensure(
            via_url.returncode != 0,
            "the file:// transport unexpectedly succeeded; the transport note is stale",
        )
        via_path = _subprocess.run(
            ["git", "clone", "--quiet", "--no-hardlinks",
             delegation_module.clone_source_argument(CANDIDATE_ROOT), str(scratch / "viapath")],
            capture_output=True,
            env=granted,
        )
        ensure(
            via_path.returncode == 0,
            "the nested plain-path clone was refused: %s"
            % via_path.stderr.decode("utf-8", "replace")[-300:],
        )

        # Nothing was written to any real configuration.
        for scope in ("--global", "--local"):
            shown = _subprocess.run(
                ["git", "config", scope, "--get-all", "safe.directory"], capture_output=True
            )
            values = shown.stdout.decode("utf-8", "replace")
            ensure(
                str(CANDIDATE_ROOT) not in values,
                "%s git configuration was mutated with a safe.directory entry" % scope,
            )
        return {
            "trust_paths": len(entries),
            "common_gitdir_declared": True,
            "switch_form_configures_direct_process": True,
            "file_url_transport_refused_despite_trust": True,
            "plain_path_clone_succeeded": True,
            "global_config_mutated": False,
            "repository_config_mutated": False,
        }
    finally:
        import shutil as _shutil

        _shutil.rmtree(scratch, ignore_errors=True)


@case("WP125-RV-008-R4-no-linux-transport-fails-closed")
def rv008r4_no_transport() -> dict[str, object]:
    """With no Dispatcher-declared Linux transport, the delegated surface is environment-unavailable.

    This is the honest state of this Packet on this host and it is stated as a measurement rather
    than worked around: there is no configured Windows-controller-to-Linux route, so the surface
    pauses.  Fabricating one — running the closed job locally and labelling the result Linux — is
    exactly what §7 forbids, and it is what a "runner OS == Linux" check alone would permit on a
    Linux box while still not being the route the contract describes.
    """
    from launcher import orchestrate as orchestrate_module

    with fixture(
        surface={
            "platform": sys.platform,
            "windows_sandbox_available": False,
            "delegation_eligible": True,
        }
    ) as context:
        ensure(
            not context.get("delegated_linux_transport"),
            "the fixture declares a Linux transport; this control would prove nothing",
        )
        root = read_only_candidate_root()
        job = build_job(
            operation="run_test",
            candidate_head=root["head"],
            candidate_tree=root["tree"],
            test_selection=("launcher_import_smoke",),
            read_only_root=root["path"],
            eligible=True,
            candidate_root=str(CANDIDATE_ROOT),
            expected_os="Linux",
        )
        result = expect_rejection(
            "sandbox_unavailable",
            lambda: orchestrate_module.authenticate_delegated_job(job, context),
        )
        ledger = Ledger(pathlib.Path(str(context["temp_root"])) / "ledger.json")
        expect_rejection(
            "sandbox_unavailable",
            lambda: launch_reviewer(
                context,
                ledger=ledger,
                reconcile_key="wp125-no-transport",
                claim_payload={"role": "executor"},
                timeout_seconds=10.0,
                delegated_job=job,
            ),
        )
        ensure(len(ledger) == 0, "a claim was minted with no delegated transport")
        return {
            "transport_configured": False,
            "environment_unavailable": True,
            "claim_objects": 0,
            "children": 0,
            "delegated_jobs": 0,
            "category": result["category"],
        }


@case("WP125-RV-006-R4-one-source-pin-feeds-validation-and-evidence")
def rv006r4_one_source_pin() -> dict[str, object]:
    """Validation and retained evidence read the same structure, and it names the repair base.

    Round 4 kept three copies of these values and the retained one drifted to the *integration*
    commit — the observation, not the candidate's own start. Both now come from `sourcepin.PIN`, and
    the two commits are asserted to be different so a future copy-paste cannot quietly merge them.
    """
    from launcher import controller as controller_module

    pin = sourcepin_module.PIN
    ensure(pin.repair_base.head != pin.integration_observation.head,
           "the repair base and the integration observation are the same commit")
    ensure(pin.repair_base.head == "3556468f25c31ff8a0fad651559cd20b67f4becf",
           "the repair base head is not the durable generation-2 base")
    ensure(pin.repair_base.tree == "e46a231ea0686bde717f9f681143cd38d2ddb67e",
           "the repair base tree is not the durable generation-2 base tree")

    # Production validation reads it.
    with fixture() as context:
        ensure(context["lease"]["candidate_start_head"] == pin.repair_base.head,
               "the fixture start head is not the repair base")
        receipt = run_preflight(context)
        ensure(receipt.complete, "preflight refused the pinned identity")
        drifted = dict(context["lease"])
        drifted["candidate_start_head"] = pin.integration_observation.head
        context["lease"] = drifted
        refused = run_preflight(context)
        ensure(refused.complete is False, "the integration commit was accepted as the candidate start")

    # Retained evidence reads it, and the strict predicate accepts only that.
    payload = authority_input_payload()
    ensure(payload["candidate_start_head"] == pin.repair_base.head,
           "the retained evidence does not name the repair base")
    ensure(controller_module._authority_is_generation_2(payload) is True,
           "the strict predicate rejected the payload built from the pin")
    swapped = dict(payload)
    swapped["candidate_start_tree"] = pin.integration_observation.tree
    ensure(controller_module._authority_is_generation_2(swapped) is False,
           "the strict predicate accepted the integration tree as the candidate start tree")
    return {
        "single_structure": "launcher.sourcepin.PIN",
        "repair_base": pin.repair_base.head,
        "integration_observation": pin.integration_observation.head,
        "distinct": True,
    }


class _FakeGroupProbe:
    """A supplied process table, so the group-identity logic runs on every platform."""

    def __init__(self, table):
        self._table = dict(table)

    def pids(self):
        return sorted(self._table)

    def pgid(self, pid):
        return self._table[pid][0]

    def session(self, pid):
        return self._table[pid][1]


@case("WP125-RV-010-R4-reused-pgid-from-another-session-is-refused")
def rv010r4_pgid_reuse() -> dict[str, object]:
    """A recycled process-group number must not be signalled or counted as ours.

    Round 4 captured the session and never consulted it, then signalled a bare numeric pgid.  The
    number is small and the kernel reuses it, so "the group with that number" and "our group" are
    different claims — and a fence that conflates them terminates something it never launched.  The
    table is supplied here so the identity logic executes on Windows too, rather than being skipped
    on the platform that has no process groups.
    """
    from launcher import watchdog as watchdog_module

    fence = watchdog_module.ProcessFence("pgid-reuse")
    fence.pgid = 4242
    fence.session = 1001

    ours = _FakeGroupProbe({4242: (4242, 1001), 4243: (4242, 1001)})
    intact = fence.group_identity_is_intact(ours)
    ensure(intact["intact"] is True, "our own group was rejected: %s" % intact["reason"])

    # Same number, different session: the kernel handed the pgid to someone else.
    reused = _FakeGroupProbe({4242: (4242, 2002), 9001: (4242, 2002)})
    drifted = fence.group_identity_is_intact(reused)
    ensure(drifted["intact"] is False, "a reused process-group number was accepted as ours")
    ensure(
        drifted["reason"] == "process_group_number_was_reused_by_another_session",
        "the reuse was not named: %s" % drifted["reason"],
    )

    refused = fence.terminate_group(reused)
    ensure(refused["signalled"] is False, "an unrelated reused group was signalled")
    ensure(refused["refused"] == drifted["reason"], "the refusal did not carry the reason")

    empty = fence.group_identity_is_intact(_FakeGroupProbe({}))
    ensure(empty["intact"] is True, "an empty group was treated as drifted")

    uncaptured = watchdog_module.ProcessFence("never-captured")
    never = uncaptured.group_identity_is_intact(ours)
    ensure(never["intact"] is False, "a fence with no captured identity claimed an intact group")
    return {
        "our_group_accepted": True,
        "reused_number_refused": True,
        "signal_withheld": True,
        "reason": drifted["reason"],
    }


# --------------------------------------------------------------------------- driver


def _collect_static_evidence() -> None:
    """Populate the §8 classes that are properties of the run rather than of a single case."""
    with fixture() as context:
        pin_path = str(context["source_pin_path"])
        pin_bytes = read_sealed_bytes(
            pin_path, "retained source pin", candidate_root=str(CANDIDATE_ROOT)
        )
        import hashlib

        SEALED_SOURCE_PIN.update(
            {
                "path": pin_path,
                "bytes": len(pin_bytes),
                "sha256": hashlib.sha256(pin_bytes).hexdigest(),
                "document": read_sealed_json(
                    pin_path, "retained source pin", candidate_root=str(CANDIDATE_ROOT)
                ),
            }
        )
        AUTHORITY_INPUT.update(authority_input_payload())
        receipt = run_preflight(context)
        if receipt.complete and receipt.plan is not None:
            ARGUMENT_VECTOR.update(describe_plan(receipt.plan))
            ENVIRONMENT_NAMES[:] = describe_environment(receipt.environment)["names"]


def run_matrix() -> dict[str, object]:
    """Run every registered case and return the machine-readable report."""
    registered = set(registry_module.CASES)
    implemented = {case_id for case_id, _ in CASES}
    not_run = sorted(registered - implemented)
    unknown = sorted(implemented - registered)

    records: list[dict[str, object]] = []
    executed = 0
    failed = 0
    try:
        _collect_static_evidence()
    except Exception:  # noqa: BLE001 - evidence collection must never mask a case result
        pass
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

    release_read_only_root()
    release_detached_checkout()

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
        "watchdog_timing": WATCHDOG_TIMING,
        "return_codes": RETURN_CODES,
        "argument_vector": ARGUMENT_VECTOR,
        "sealed_source_pin": SEALED_SOURCE_PIN,
        "authority_input": AUTHORITY_INPUT,
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
