"""Ordered preflight, and the claim that may only follow it (Issue 125 §5).

Seven checks run in a fixed order and every one of them must finish before any durable operation is
minted.  The order is not decoration.  Checking the lease before the authority would let an expired
run be rejected for the wrong reason; checking the sandbox before the write set would let a run that
was never allowed to write anything spend time deciding *where* to write it.  More importantly, a
claim minted mid-preflight is a claim that outlives the reason it was refused.

The hard part of §5 is not running checks — it is proving a check *ran*.  A preflight that returns
``{"ok": true}`` is indistinguishable from a preflight that looked at nothing, and the contract
requires a fault-injection control that kills exactly that impostor.  So a step here does not
return a verdict; it returns the **observations** it made.  The receipt then audits those
observations against a per-step required key set and against the expected values.  A green step with
an empty observation record fails the audit, which is what makes the impostor detectable by machine
rather than by reading the code.

The claim is a separate commit point.  :func:`run_preflight` never writes; :func:`mint_claim`
refuses to run without a complete positive receipt and is the only function here that touches the
ledger.
"""

from __future__ import annotations

import dataclasses
import datetime
import hashlib
import pathlib
from collections.abc import Callable, Mapping, Sequence

from core.ledger import Ledger

from .argv import build_launch_plan, describe as describe_plan
from .environment import build_child_environment, describe as describe_environment
from .errors import reject
from .inputs import read_sealed_bytes, read_sealed_json
from .watchdog import parse_utc

GIT_OID_LENGTH = 40
WRITE_PREFIX = ".github/coordination/reviewer_bootstrap/launcher/"

STEP_NAMES: tuple[str, ...] = (
    "authority_identity",
    "lease_and_branch",
    "source_pin",
    "worktree_and_write_set",
    "trusted_inventory",
    "execution_surface",
    "environment_and_argv",
)

# The observation keys each step must produce.  This table is the teeth of the fault-injection
# control: it is declared next to the steps, so a step that stops observing something has to delete
# its own requirement in the same file, in the same diff, where a reviewer will see it.
REQUIRED_OBSERVATIONS: Mapping[str, tuple[str, ...]] = {
    "authority_identity": (
        "repository",
        "mission_issue",
        "mission_revision",
        "mission_plan_hash",
        "packet_issue",
        "packet_revision",
        "packet_generation",
        "packet_attempt",
        "packet_spec_hash",
    ),
    "lease_and_branch": (
        "lease_id",
        "lease_effective_stop_utc",
        "lease_seconds_remaining",
        "candidate_ref",
        "candidate_start_head",
    ),
    "source_pin": (
        "source_pin_sha256",
        "source_pin_bytes",
        "integration_head",
        "integration_tree",
        "effective_write_prefix",
    ),
    "worktree_and_write_set": (
        "worktree_clean",
        "selected_write_paths",
        "paths_outside_prefix",
    ),
    "trusted_inventory": (
        "launcher_file_count",
        "launcher_inventory_sha256",
        "executable_identity",
    ),
    "execution_surface": (
        "platform",
        "windows_sandbox_available",
        "delegation_eligible",
        "selected_surface",
    ),
    "environment_and_argv": (
        "environment_name_count",
        "environment_memory_value",
        "argument_count",
        "permission_mode",
    ),
}


@dataclasses.dataclass(frozen=True)
class StepResult:
    name: str
    index: int
    observations: dict[str, object]


# WP125-RV-003.  A receipt is an authority object, so it must be unforgeable by construction rather
# than by convention.  This is the RA-03 sealed-snapshot idiom: the seal is a module-private object
# no caller outside this file can name, so `PreflightReceipt(complete=True, ...)` written by hand —
# or by a substituted step map — cannot produce a receipt that `mint_claim` will accept.
_SEAL = object()

# Provenance values. Only `trusted_run` may mint a claim. The fault-injection seam stamps
# `fault_injection` so that a substituted step map can still be *tested* while being structurally
# incapable of reaching a durable operation.
PROVENANCE_TRUSTED = "trusted_run"
PROVENANCE_FAULT_INJECTION = "fault_injection"

SURFACES = frozenset({"windows", "delegated_linux_run_test"})


@dataclasses.dataclass(frozen=True)
class PreflightReceipt:
    """The complete, ordered evidence that preflight finished before anything durable happened."""

    complete: bool
    steps: tuple[StepResult, ...]
    plan: object
    environment: Mapping[str, str]
    surface: str
    failure: dict[str, object] | None
    provenance: str = PROVENANCE_FAULT_INJECTION
    _seal: object = None

    def __post_init__(self):
        if self._seal is not _SEAL:
            raise reject(
                "preflight_incomplete",
                "a preflight receipt was constructed outside the trusted preflight",
            )

    def is_trusted(self) -> bool:
        return self._seal is _SEAL and self.provenance == PROVENANCE_TRUSTED

    def as_dict(self) -> dict[str, object]:
        return {
            "complete": self.complete,
            "step_count": len(self.steps),
            "expected_step_count": len(STEP_NAMES),
            "steps": [
                {"index": step.index, "name": step.name, "observations": step.observations}
                for step in self.steps
            ],
            "selected_surface": self.surface,
            "provenance": self.provenance,
            "failure": self.failure,
        }

    def receipt_hash(self) -> str:
        """A stable digest of the ordered observations, used to bind a claim to *this* preflight."""
        import json

        blob = json.dumps(self.as_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _oid(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != GIT_OID_LENGTH:
        raise reject("authority_mismatch", "%s must be an exact 40-hex git oid" % label)
    if value != value.lower() or any(char not in "0123456789abcdef" for char in value):
        raise reject("authority_mismatch", "%s must be lowercase hexadecimal" % label)
    return value


def _sha256_text(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise reject("authority_mismatch", "%s must be an exact SHA-256" % label)
    if value != value.lower() or any(char not in "0123456789abcdef" for char in value):
        raise reject("authority_mismatch", "%s must be lowercase hexadecimal" % label)
    return value


def _equal(actual: object, expected: object, category: str, label: str) -> object:
    if actual != expected:
        raise reject(category, "%s does not match the pinned authority" % label)
    return actual


# --------------------------------------------------------------------------- the seven steps


def _step_authority_identity(context: Mapping[str, object]) -> dict[str, object]:
    authority = context["authority"]
    expected = context["expected_authority"]
    observed = {
        "repository": authority["repository"],
        "mission_issue": authority["mission"]["issue"],
        "mission_revision": authority["mission"]["revision"],
        "mission_plan_hash": _sha256_text(
            authority["mission"]["plan_hash"], "mission.plan_hash"
        ),
        "packet_issue": authority["packet"]["issue"],
        "packet_revision": authority["packet"]["revision"],
        "packet_generation": authority["packet"]["generation"],
        "packet_attempt": authority["packet"]["attempt"],
        "packet_spec_hash": _sha256_text(authority["packet"]["spec_hash"], "packet.spec_hash"),
    }
    for key, want in expected.items():
        _equal(observed[key], want, "authority_mismatch", key)
    return observed


def _step_lease_and_branch(context: Mapping[str, object]) -> dict[str, object]:
    lease = context["lease"]
    now = context.get("now_utc") or datetime.datetime.now(datetime.timezone.utc)
    stop = parse_utc(lease["effective_stop_utc"], "lease.effective_stop_utc")
    remaining = (stop - now).total_seconds()
    if remaining <= 0:
        raise reject("lease_expired", "the lease has passed its absolute stop")
    if lease.get("generation") != context["expected_authority"]["packet_generation"]:
        raise reject("stale_generation", "the lease names a different generation")
    _equal(lease["candidate_ref"], context["expected_candidate_ref"], "authority_mismatch", "candidate_ref")
    return {
        "lease_id": lease["lease_id"],
        "lease_effective_stop_utc": lease["effective_stop_utc"],
        "lease_seconds_remaining": round(remaining, 3),
        "candidate_ref": lease["candidate_ref"],
        "candidate_start_head": _oid(lease["candidate_start_head"], "candidate_start_head"),
    }


def _step_source_pin(context: Mapping[str, object]) -> dict[str, object]:
    path = context["source_pin_path"]
    raw = read_sealed_bytes(path, "source pin", candidate_root=context["candidate_root"])
    digest = hashlib.sha256(raw).hexdigest()
    _equal(digest, context["expected_source_pin_sha256"], "authority_mismatch", "source pin sha256")
    pin = read_sealed_json(
        path,
        "source pin",
        candidate_root=context["candidate_root"],
        required_keys=("source", "bounds"),
    )
    source = pin["source"]
    bounds = pin["bounds"]
    _equal(
        _oid(source["integration_head"], "integration_head"),
        context["expected_integration_head"],
        "authority_mismatch",
        "integration_head",
    )
    prefix = bounds["effective_write_prefix"]
    _equal(prefix, WRITE_PREFIX, "write_set", "effective_write_prefix")
    return {
        "source_pin_sha256": digest,
        "source_pin_bytes": len(raw),
        "integration_head": source["integration_head"],
        "integration_tree": _oid(source["integration_tree"], "integration_tree"),
        "effective_write_prefix": prefix,
    }


def _step_worktree_and_write_set(context: Mapping[str, object]) -> dict[str, object]:
    clean = context["worktree_clean"]
    if clean is not True:
        raise reject("write_set", "the dedicated worktree is not clean")
    selected: Sequence[str] = tuple(context.get("selected_write_paths", ()))
    outside = sorted(path for path in selected if not path.startswith(WRITE_PREFIX))
    if outside:
        raise reject("write_set", "%d selected paths fall outside the launcher prefix" % len(outside))
    return {
        "worktree_clean": True,
        "selected_write_paths": list(selected),
        "paths_outside_prefix": outside,
    }


def _step_trusted_inventory(context: Mapping[str, object]) -> dict[str, object]:
    inventory = context["inventory"]
    if not isinstance(inventory, Mapping) or not inventory.get("files"):
        raise reject("preflight_incomplete", "the launcher inventory is empty")
    executable = context["launch_config"]["executable"]
    identity = pathlib.Path(executable)
    if not identity.is_absolute():
        raise reject("argument_vector", "the configured executable is not absolute")
    return {
        "launcher_file_count": len(inventory["files"]),
        "launcher_inventory_sha256": _sha256_text(
            inventory["inventory_sha256"], "inventory_sha256"
        ),
        "executable_identity": str(identity),
    }


def _step_execution_surface(context: Mapping[str, object]) -> dict[str, object]:
    surface = context["surface"]
    windows_available = bool(surface["windows_sandbox_available"])
    delegation_eligible = bool(surface["delegation_eligible"])
    if windows_available:
        selected = "windows"
    elif delegation_eligible:
        selected = "delegated_linux_run_test"
    else:
        # §7: neither a usable Windows sandbox nor authorized credential-free delegation means the
        # Packet pauses.  It does not switch environment, weaken containment, or reach for a
        # secret-bearing CI job to keep the run alive.
        raise reject("sandbox_unavailable", "no usable Windows sandbox and no eligible delegation")
    return {
        "platform": surface["platform"],
        "windows_sandbox_available": windows_available,
        "delegation_eligible": delegation_eligible,
        "selected_surface": selected,
    }


def _step_environment_and_argv(context: Mapping[str, object]) -> dict[str, object]:
    environment = build_child_environment(
        context["parent_environment"],
        candidate_root=context["candidate_root"],
        extra=context.get("extra_environment"),
    )
    plan = build_launch_plan(
        context["launch_config"],
        prompt_path=context["prompt_path"],
        candidate_root=context["candidate_root"],
    )
    context_sink = context["_sink"]
    context_sink["environment"] = environment
    context_sink["plan"] = plan
    described_env = describe_environment(environment)
    described_plan = describe_plan(plan)
    return {
        "environment_name_count": described_env["name_count"],
        "environment_memory_value": described_env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"],
        "argument_count": described_plan["argument_count"],
        "permission_mode": described_plan["permission_mode"],
    }


STEPS: tuple[tuple[str, Callable[[Mapping[str, object]], dict[str, object]]], ...] = (
    ("authority_identity", _step_authority_identity),
    ("lease_and_branch", _step_lease_and_branch),
    ("source_pin", _step_source_pin),
    ("worktree_and_write_set", _step_worktree_and_write_set),
    ("trusted_inventory", _step_trusted_inventory),
    ("execution_surface", _step_execution_surface),
    ("environment_and_argv", _step_environment_and_argv),
)


def _audit_observations(name: str, observations: object) -> dict[str, object]:
    """Refuse a step that reports green without having looked at anything.

    This is the fault-injection control §5 requires, expressed as a data check rather than as a code
    review: a substituted always-green step has to fabricate every required key, and fabricating them
    means fabricating values that the later equality checks then compare against the pinned
    authority.
    """
    if not isinstance(observations, Mapping):
        raise reject("preflight_incomplete", "step %s did not return an observation record" % name)
    required = REQUIRED_OBSERVATIONS[name]
    missing = [key for key in required if key not in observations]
    if missing:
        raise reject(
            "preflight_incomplete",
            "step %s observed %d of %d required inputs" % (name, len(required) - len(missing), len(required)),
        )
    empty = [key for key in required if observations[key] is None or observations[key] == ""]
    if empty:
        raise reject("preflight_incomplete", "step %s reported %d empty observations" % (name, len(empty)))
    return dict(observations)


def _bind_observations_to_pins(
    context: Mapping[str, object], results: Sequence[StepResult]
) -> dict[str, object]:
    """Re-verify the finished observations against the pinned expectations (WP125-RV-003).

    This runs *after* the steps and does not trust them.  Generation 1 delegated every equality
    check to the step that produced the value, so a substituted step map could fabricate the required
    keys and every later check would happily compare a fabrication against itself.  Here the caller's
    pins are the left-hand side and the observations are the right-hand side, and the source pin is
    re-read from disk so at least one value cannot be fabricated at all: an impostor that wants to
    pass has to actually hash the sealed file.
    """
    observed: dict[str, object] = {}
    for step in results:
        observed.update(step.observations)

    expected = context["expected_authority"]
    for key, want in dict(expected).items():
        if observed.get(key) != want:
            raise reject("authority_mismatch", "observed %s is not the pinned value" % key)

    if observed.get("candidate_ref") != context["expected_candidate_ref"]:
        raise reject("authority_mismatch", "observed candidate_ref is not the pinned value")
    if observed.get("integration_head") != context["expected_integration_head"]:
        raise reject("authority_mismatch", "observed integration_head is not the pinned value")
    if observed.get("effective_write_prefix") != WRITE_PREFIX:
        raise reject("write_set", "observed write prefix is not the sole permitted prefix")
    if observed.get("worktree_clean") is not True:
        raise reject("write_set", "the bound receipt does not record a clean worktree")
    if observed.get("paths_outside_prefix"):
        raise reject("write_set", "the bound receipt records paths outside the launcher prefix")
    if observed.get("permission_mode") != "dontAsk":
        raise reject("permission_mode", "the bound receipt does not carry the mandated dontAsk")
    if observed.get("environment_memory_value") != "1":
        raise reject("child_environment", "the bound receipt does not carry the memory value 1")
    if observed.get("selected_surface") not in SURFACES:
        raise reject("sandbox_unavailable", "the bound receipt names no known execution surface")

    # Independent re-measurement. The step already hashed the pin; doing it again here means the
    # binding stage has its own evidence rather than a restatement of the step's.
    rebound = hashlib.sha256(
        read_sealed_bytes(
            str(context["source_pin_path"]),
            "source pin rebind",
            candidate_root=str(context["candidate_root"]),
        )
    ).hexdigest()
    if rebound != context["expected_source_pin_sha256"]:
        raise reject("authority_mismatch", "the re-read source pin does not match the pinned hash")
    if observed.get("source_pin_sha256") != rebound:
        raise reject("authority_mismatch", "the observed source pin hash is not the re-read hash")

    return {
        "bound_keys": len(observed),
        "source_pin_rebound_sha256": rebound,
        "independent_rebind": True,
    }


def _run_steps(
    context: Mapping[str, object],
    steps: Sequence[tuple[str, Callable[[Mapping[str, object]], dict[str, object]]]],
    provenance: str,
) -> PreflightReceipt:
    """Shared engine.  Order is enforced for every caller, trusted or injected."""
    if [name for name, _ in steps] != list(STEP_NAMES):
        raise reject("preflight_order", "the preflight step order has drifted from the contract")

    sink: dict[str, object] = {}
    working = dict(context)
    working["_sink"] = sink

    def negative(name: str, index: int, exc: BaseException) -> PreflightReceipt:
        return PreflightReceipt(
            complete=False,
            steps=tuple(results),
            plan=sink.get("plan"),
            environment=sink.get("environment", {}),
            surface="unselected",
            failure={
                "step": name,
                "step_index": index,
                "category": getattr(exc, "category", "preflight_incomplete"),
                "message": str(exc),
            },
            provenance=provenance,
            _seal=_SEAL,
        )

    results: list[StepResult] = []
    for index, (name, function) in enumerate(steps, start=1):
        try:
            observations = _audit_observations(name, function(working))
        except Exception as exc:  # noqa: BLE001 - every failure becomes a named negative receipt
            return negative(name, index, exc)
        results.append(StepResult(name=name, index=index, observations=observations))

    if len(results) != len(STEP_NAMES):
        raise reject(
            "preflight_incomplete",
            "preflight produced %d of %d steps" % (len(results), len(STEP_NAMES)),
        )

    # WP125-RV-003: a complete run must produce a usable plan, environment and surface. Generation 1
    # returned complete=True with plan=None and environment={} whenever the final step was replaced,
    # which is a receipt that says "ready to launch" while carrying nothing to launch.
    plan = sink.get("plan")
    environment = sink.get("environment", {})
    try:
        if plan is None:
            raise reject("preflight_incomplete", "preflight completed without a launch plan")
        if not environment:
            raise reject("preflight_incomplete", "preflight completed without a child environment")
        binding = _bind_observations_to_pins(context, results)
    except Exception as exc:  # noqa: BLE001
        return negative("value_binding", len(STEP_NAMES) + 1, exc)

    surface = str(results[5].observations["selected_surface"])
    results.append(
        StepResult(name="value_binding", index=len(STEP_NAMES) + 1, observations=binding)
    )
    return PreflightReceipt(
        complete=True,
        steps=tuple(results),
        plan=plan,
        environment=environment,
        surface=surface,
        failure=None,
        provenance=provenance,
        _seal=_SEAL,
    )


def run_preflight(context: Mapping[str, object]) -> PreflightReceipt:
    """The production entry point.  Runs the trusted step map, and only that map.

    There is deliberately no ``steps`` parameter.  Generation 1 exposed one whose order guard was
    skipped for exactly the callers that supplied their own steps, so the full seven-function
    substitution it was meant to stop was the one case it never checked.
    """
    return _run_steps(context, STEPS, PROVENANCE_TRUSTED)


def run_preflight_fault_injection(
    context: Mapping[str, object],
    steps: Sequence[tuple[str, Callable[[Mapping[str, object]], dict[str, object]]]],
) -> PreflightReceipt:
    """Test-only seam for substituting steps.

    Substitution stays reachable for the fault-injection controls, but every receipt it produces is
    stamped ``fault_injection`` and :func:`mint_claim` refuses those outright.  So an impostor step
    map can be *studied* and can never mint a durable operation, which is the property §5 actually
    needs — stronger than hiding the seam, because it holds even for a caller who finds it.
    """
    return _run_steps(context, steps, PROVENANCE_FAULT_INJECTION)


def mint_claim(
    receipt: PreflightReceipt,
    ledger: Ledger,
    reconcile_key: str,
    payload: Mapping[str, object],
) -> dict[str, object]:
    """The separate commit point.  Refuses without a complete positive receipt.

    Idempotent by ``reconcile_key`` via the integrated RA-01 ledger: an identical retry returns the
    existing record and creates nothing.  A *conflicting* payload under the same key is a rejection
    rather than an overwrite, because two different runs answering to one key is precisely the state
    a reconcile key exists to prevent.
    """
    if not isinstance(receipt, PreflightReceipt) or not receipt.complete:
        raise reject("preflight_incomplete", "a claim was attempted before preflight completed")
    # WP125-RV-003: authenticate provenance before anything durable happens. A receipt that did not
    # come from the trusted step map is refused here even if every field on it looks perfect.
    if not receipt.is_trusted():
        raise reject(
            "preflight_incomplete",
            "a claim was attempted on a receipt with provenance %r" % (receipt.provenance,),
        )
    if len(receipt.steps) != len(STEP_NAMES) + 1:
        raise reject("preflight_incomplete", "a claim was attempted on a partial preflight receipt")
    if receipt.plan is None or not receipt.environment:
        raise reject("preflight_incomplete", "a claim was attempted without a plan or environment")
    if receipt.surface not in SURFACES:
        raise reject("preflight_incomplete", "a claim was attempted without a selected surface")
    if not isinstance(reconcile_key, str) or not reconcile_key:
        raise reject("duplicate_claim", "the reconcile key must be a non-empty string")

    record = dict(payload)
    record["preflight_receipt_sha256"] = receipt.receipt_hash()
    created, stored = ledger.record(reconcile_key, record)
    if not created and stored != record:
        raise reject("duplicate_claim", "a conflicting payload already answers to this reconcile key")
    return {"created": created, "record": stored, "reconcile_key": reconcile_key}
