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
import hmac
import json
import pathlib
import secrets
from collections.abc import Callable, Mapping, Sequence

from core.ledger import Ledger

from .argv import build_launch_plan, describe as describe_plan
from .environment import build_child_environment, describe as describe_environment
from .errors import reject
from .inputs import read_sealed_bytes, read_sealed_json
from .sourcepin import PIN
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
        "sealed_config_sha256",
        "sealed_prompt_sha256",
        "launch_inputs_sealed",
    ),
}


@dataclasses.dataclass(frozen=True)
class StepResult:
    name: str
    index: int
    observations: dict[str, object]


# WP125-RV-003, review round 2.  The generation-2 boundary was a module-private sentinel plus a
# `provenance` string, both of which are *fields the caller fills in*.  `from launcher.preflight
# import _SEAL` is one line, and the round-1 review demonstrated a hand-built receipt minting a real
# claim with it.  Naming privacy is not a boundary in a language where every name is reachable.
#
# So authorization is no longer carried on the receipt at all.  Two things replace it:
#
#   1. A controller-held provenance table.  `_run_steps` mints an opaque authorization id for the
#      trusted path only, and records the digest of the observations it just witnessed.  A caller who
#      finds the table cannot make it say anything useful: the id is worthless unless the receipt
#      presented alongside it hashes to the digest recorded against it, so an authorization can never
#      be re-attached to fabricated observations.
#   2. Live re-validation at the durable commit point.  `mint_claim` re-derives the binding itself —
#      re-reading the sealed pin from disk, re-comparing every observation against the caller's pins,
#      and re-checking the lease — so "authorized" means "still true right now", not "was stamped
#      true earlier".
#
# The fault-injection seam mints no authorization, which is why a substituted step map remains
# studiable and remains incapable of reaching a durable operation.
PROVENANCE_TRUSTED = "trusted_run"
PROVENANCE_FAULT_INJECTION = "fault_injection"

SURFACES = frozenset({"windows", "delegated_linux_run_test"})


def _receipt_binding_blob(
    steps: Sequence["StepResult"], plan: object, environment: Mapping[str, str], surface: str
) -> bytes:
    """The complete thing an authorization is about.

    WP125-RV-003-R2.  Round 2 bound only the ordered observations, so the *launch* the receipt
    authorised — its executable, its argument vector, its working directory, its environment, its
    surface — was outside the signature entirely.  A receipt could be re-pointed at a different plan
    after preflight and still present a matching authorization, which is the same forgery the round
    was meant to close, one field further out.  Everything the claim actually licences is in here.
    """
    plan_view: dict[str, object] = {}
    if plan is not None:
        plan_view = {
            "executable": getattr(plan, "executable", None),
            "argv": list(getattr(plan, "argv", ()) or ()),
            "working_directory": getattr(plan, "working_directory", None),
            "prompt_path": getattr(plan, "prompt_path", None),
        }
    document = {
        "steps": [
            {"index": step.index, "name": step.name, "observations": step.observations}
            for step in steps
        ],
        "plan": plan_view,
        # WP125-RV-003-R3: the complete environment — every allowlisted name *and its exact value*.
        # Round 3 signed the name list and the memory flag only, so `PATH` could be repointed, `TEMP`
        # could be moved, and every value the child would actually receive could change while the
        # authorization still verified. A name list is a description of the environment; the values
        # are the environment.
        "environment": sorted((environment or {}).items()),
        "surface": surface,
    }
    return json.dumps(
        document, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str
    ).encode("utf-8")


# WP125-RV-003-R4.  There is no signing capability here any more, and that is the repair.
#
# Round 3 hid a secret in a closure and left the closure callable from module scope.  Round 4 moved
# the secret into an object and put the object *and its capability token* side by side as module
# attributes, so `preflight._AUTHORITY.mint(preflight._MINT_TOKEN, blob)` minted an authorization for
# any bytes at all.  Each round moved the capability somewhere slightly less obvious, and in a
# language where every attribute is reachable that is a losing game: candidate code shares the
# process, so any capability the process holds, the candidate holds.
#
# So the capability is gone.  Authorization is not a token the receipt carries; it is the controller
# re-deriving, at the moment the durable object is created, that the receipt's canonical bytes
# describe a preflight that really passed against the pinned authority and the sealed inputs still on
# disk.  Candidate code can produce observations — it cannot produce a claim, because there is
# nothing to steal that would make an unsatisfying receipt satisfying.


def canonical_receipt_bytes(
    steps: Sequence["StepResult"], plan: object, environment: Mapping[str, str], surface: str
) -> bytes:
    """The complete canonical serialization the controller re-computes at the commit point."""
    return _receipt_binding_blob(steps, plan, environment, surface)


@dataclasses.dataclass(frozen=True)
class PreflightReceipt:
    """The complete, ordered evidence that preflight finished before anything durable happened.

    Carries evidence only.  ``authorization`` is an opaque lookup key into the controller-held
    provenance table; it grants nothing on its own and is meaningless without observations that hash
    to what the controller recorded.
    """

    complete: bool
    steps: tuple[StepResult, ...]
    plan: object
    environment: Mapping[str, str]
    surface: str
    failure: dict[str, object] | None
    authorization: str | None = None

    @property
    def provenance(self) -> str:
        """Descriptive only.  Never consulted when deciding whether a claim may be minted."""
        return PROVENANCE_TRUSTED if self.authorization else PROVENANCE_FAULT_INJECTION

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
    # The executable identity is read from the sealed input, not from a caller-supplied mapping.
    executable = _seal_launch_inputs(context)["document"]["executable"]
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


def _seal_launch_inputs(context: Mapping[str, object]) -> dict[str, object]:
    """Consume the launch configuration as a *sealed* input and bind it exactly (WP125-RV-007).

    Generation 2 took ``launch_config`` and ``prompt_path`` as ordinary values in the context
    mapping: whoever assembled the context chose the executable, the working directory, the variable
    arguments and the prompt.  The candidate is one of the things that assembles contexts, so "the
    reviewed code cannot choose the binary that reviews it" was a comment rather than a control.

    Here the configuration is read through the sealed-input reader — regular file, exactly one hard
    link, no symlink or reparse point, sealed read-only, outside the candidate checkout, no
    traversal, no ADS, no DOS device — and every value that survives is then compared, byte for byte,
    against the sealed document.  A caller-selected executable, switch or prompt path cannot survive
    the comparison, because the comparison's left-hand side never came from the caller.
    """
    sealed_path = context.get("sealed_launch_config_path")
    if not sealed_path:
        raise reject(
            "sealed_input",
            "the launch configuration is not a sealed Dispatcher input",
        )
    raw = read_sealed_bytes(
        str(sealed_path), "sealed launch config", candidate_root=str(context["candidate_root"])
    )
    document = read_sealed_json(
        str(sealed_path),
        "sealed launch config",
        candidate_root=str(context["candidate_root"]),
        required_keys=("permission_mode", "executable", "working_directory", "prompt_path"),
    )
    # WP125-RV-007-R2: the anchors are mandatory. Round 2 checked them only `if expected_sha`, so a
    # context that simply omitted the anchor got an unanchored sealed file and a green step — the
    # control was opt-in, and the party it was protecting against is the one filling in the context.
    expected_sha = context.get("expected_launch_config_sha256")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise reject(
            "sealed_input",
            "the launch configuration carries no Dispatcher-bound SHA-256 anchor",
        )
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != expected_sha:
        raise reject("sealed_input", "the sealed launch config does not match its pinned hash")

    # The prompt is a sealed input in its own right: hashing the configuration proves nothing about
    # the bytes the child will actually be told to read.
    prompt_path = str(document["prompt_path"])
    prompt_bytes = read_sealed_bytes(
        prompt_path, "sealed prompt", candidate_root=str(context["candidate_root"])
    )
    expected_prompt_sha = context.get("expected_prompt_sha256")
    if not isinstance(expected_prompt_sha, str) or len(expected_prompt_sha) != 64:
        raise reject("sealed_input", "the prompt carries no Dispatcher-bound SHA-256 anchor")
    prompt_sha = hashlib.sha256(prompt_bytes).hexdigest()
    if prompt_sha != expected_prompt_sha:
        raise reject("sealed_input", "the sealed prompt does not match its pinned hash")

    # Anything the caller also supplied must be identical to the sealed document, or it is an
    # attempt to steer a value the Dispatcher already fixed.
    supplied = context.get("launch_config")
    if isinstance(supplied, Mapping):
        for key in ("permission_mode", "executable", "working_directory"):
            if key in supplied and supplied[key] != document[key]:
                raise reject(
                    "sealed_input",
                    "caller-supplied launch_config.%s differs from the sealed input" % key,
                )
        for key in ("extra_args", "executable_args"):
            if key in supplied and list(supplied[key]) != list(document.get(key, ())):
                raise reject(
                    "sealed_input",
                    "caller-supplied launch_config.%s differs from the sealed input" % key,
                )
    if context.get("prompt_path") not in (None, prompt_path):
        raise reject("sealed_input", "a caller-selected prompt path differs from the sealed input")

    return {
        "document": document,
        "config_sha256": actual_sha,
        "config_bytes": len(raw),
        "prompt_path": prompt_path,
        "prompt_sha256": prompt_sha,
        "prompt_bytes": len(prompt_bytes),
    }


def assert_launch_inputs_unchanged(
    context: Mapping[str, object], receipt: "PreflightReceipt"
) -> dict[str, object]:
    """Re-read the sealed inputs and refuse if a single byte moved (WP125-RV-007-R2).

    Called immediately before the claim and again immediately before spawn or dispatch.  Preflight
    validating a file once says the file was right *then*; the window between preflight and the
    process actually starting is exactly where a replacement pays off, and it is the window nothing
    was watching.  Both call sites re-open the sealed inputs through the hardened reader and compare
    against the digests the receipt is bound to.
    """
    bound = receipt.steps[len(STEP_NAMES) - 1].observations
    root = str(context["candidate_root"])
    config_raw = read_sealed_bytes(
        str(context["sealed_launch_config_path"]), "sealed launch config readback", candidate_root=root
    )
    config_sha = hashlib.sha256(config_raw).hexdigest()
    if config_sha != bound.get("sealed_config_sha256"):
        raise reject("sealed_input", "the sealed launch config changed after preflight")

    document = json.loads(config_raw.decode("utf-8"))
    prompt_raw = read_sealed_bytes(
        str(document["prompt_path"]), "sealed prompt readback", candidate_root=root
    )
    prompt_sha = hashlib.sha256(prompt_raw).hexdigest()
    if prompt_sha != bound.get("sealed_prompt_sha256"):
        raise reject("sealed_input", "the sealed prompt changed after preflight")

    plan = receipt.plan
    if plan is not None:
        if plan.executable != str(pathlib.Path(document["executable"]).resolve()):
            raise reject("sealed_input", "the bound executable no longer matches the sealed input")
        if plan.prompt_path != str(pathlib.Path(document["prompt_path"]).resolve()):
            raise reject("sealed_input", "the bound prompt path no longer matches the sealed input")
        if plan.working_directory != str(pathlib.Path(document["working_directory"]).resolve()):
            raise reject(
                "sealed_input", "the bound working directory no longer matches the sealed input"
            )
    return {
        "config_sha256": config_sha,
        "prompt_sha256": prompt_sha,
        "readback": "byte_for_byte",
    }


def _step_environment_and_argv(context: Mapping[str, object]) -> dict[str, object]:
    sealed = _seal_launch_inputs(context)
    document = sealed["document"]
    environment = build_child_environment(
        context["parent_environment"],
        candidate_root=context["candidate_root"],
        extra=context.get("extra_environment"),
    )
    # Built from the sealed document, never from the caller's mapping.
    plan = build_launch_plan(
        document,
        prompt_path=sealed["prompt_path"],
        candidate_root=context["candidate_root"],
    )
    # Final binding: the vector that will actually be spawned must name the sealed executable and
    # the sealed prompt, exactly. This is checked after the build so that no later rewrite can slip
    # a different path into a plan that already passed validation.
    if plan.executable != str(pathlib.Path(document["executable"]).resolve()):
        raise reject("sealed_input", "the built vector does not carry the sealed executable")
    if plan.prompt_path != str(pathlib.Path(sealed["prompt_path"]).resolve()):
        raise reject("sealed_input", "the built vector does not carry the sealed prompt path")

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
        "sealed_config_sha256": sealed["config_sha256"],
        "sealed_prompt_sha256": sealed["prompt_sha256"],
        "launch_inputs_sealed": True,
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

    # WP125-RV-006-R4: identity, not shape. Round 4 accepted the candidate start head and tree as
    # merely 40-hex, and `"0" * 40` is 40-hex. They are now compared against the one authoritative
    # source pin, along with repository equality, which was omitted entirely.
    if observed.get("repository") != PIN.repository:
        raise reject("authority_mismatch", "the observed repository is not the pinned repository")
    if observed.get("candidate_start_head") != PIN.repair_base.head:
        raise reject(
            "authority_mismatch",
            "the candidate start head is not the generation-2 repair base",
        )
    start_tree = observed.get("candidate_start_tree")
    if start_tree is not None and start_tree != PIN.repair_base.tree:
        raise reject(
            "authority_mismatch",
            "the candidate start tree is not the generation-2 repair base tree",
        )
    if observed.get("integration_head") == PIN.repair_base.head:
        raise reject(
            "authority_mismatch",
            "the integration observation was adopted as the candidate start; they are not the same commit",
        )
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
    if observed.get("launch_inputs_sealed") is not True:
        raise reject("sealed_input", "the bound receipt does not record sealed launch inputs")
    for key in ("sealed_config_sha256", "sealed_prompt_sha256"):
        value = observed.get(key)
        if not isinstance(value, str) or len(value) != 64:
            raise reject("sealed_input", "the bound receipt carries no %s" % key)

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
            authorization=None,
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
    steps_tuple = tuple(results)
    # The trusted path records that it *is* the trusted path. This is descriptive: `mint_claim`
    # re-derives everything and never takes this on trust, so there is no capability here to steal.
    authorization = PROVENANCE_TRUSTED if provenance == PROVENANCE_TRUSTED else None
    return PreflightReceipt(
        complete=True,
        steps=steps_tuple,
        plan=plan,
        environment=environment,
        surface=surface,
        failure=None,
        authorization=authorization,
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
    *,
    context: Mapping[str, object],
) -> dict[str, object]:
    """The separate commit point.  Re-derives authorization here; trusts no flag.

    ``context`` is required.  Generation 2 authenticated a field on the receipt, which meant the
    commit point believed a claim the caller had written down.  Now the commit point does the work
    again: it re-reads the sealed pin from disk, re-compares every observation against the pins, and
    re-checks the lease.  "Authorized" therefore means "still true at the moment the durable object
    is created", which is the only tense that matters for a fence.

    Idempotent by ``reconcile_key`` via the integrated RA-01 ledger: an identical retry returns the
    existing record and creates nothing.  A *conflicting* payload under the same key is a rejection
    rather than an overwrite, because two different runs answering to one key is precisely the state
    a reconcile key exists to prevent.
    """
    if not isinstance(receipt, PreflightReceipt) or not receipt.complete:
        raise reject("preflight_incomplete", "a claim was attempted before preflight completed")
    if len(receipt.steps) != len(STEP_NAMES) + 1:
        raise reject("preflight_incomplete", "a claim was attempted on a partial preflight receipt")
    if tuple(step.name for step in receipt.steps) != STEP_NAMES + ("value_binding",):
        raise reject("preflight_order", "the receipt does not carry the contract step order")
    if receipt.plan is None or not receipt.environment:
        raise reject("preflight_incomplete", "a claim was attempted without a plan or environment")
    if receipt.surface not in SURFACES:
        raise reject("preflight_incomplete", "a claim was attempted without a selected surface")
    if not isinstance(reconcile_key, str) or not reconcile_key:
        raise reject("duplicate_claim", "the reconcile key must be a non-empty string")
    if not isinstance(context, Mapping) or not context:
        raise reject("preflight_incomplete", "a claim was attempted without the pinned context")

    # WP125-RV-003-R4.  Internal consistency of the canonical bytes, re-derived here rather than
    # attested by a token. A receipt whose plan, environment or surface was swapped after preflight
    # no longer agrees with the observations it carries, and the disagreement is what refuses it.
    canonical = canonical_receipt_bytes(
        receipt.steps, receipt.plan, receipt.environment, receipt.surface
    )
    observed: dict[str, object] = {}
    for step in receipt.steps:
        observed.update(step.observations)

    if receipt.surface != observed.get("selected_surface"):
        raise reject(
            "preflight_incomplete", "the receipt surface disagrees with its own observations"
        )
    if len(receipt.environment) != observed.get("environment_name_count"):
        raise reject(
            "preflight_incomplete", "the receipt environment disagrees with its own observations"
        )
    if receipt.environment.get("CLAUDE_CODE_DISABLE_AUTO_MEMORY") != observed.get(
        "environment_memory_value"
    ):
        raise reject(
            "preflight_incomplete", "the receipt environment value disagrees with its observations"
        )
    plan_argv = getattr(receipt.plan, "argv", None)
    if plan_argv is None or len(plan_argv) != observed.get("argument_count"):
        raise reject("preflight_incomplete", "the receipt plan disagrees with its own observations")
    if getattr(receipt.plan, "executable", None) is None:
        raise reject("preflight_incomplete", "the receipt plan carries no executable")

    # WP125-RV-003-R4.  Re-derivation, not attestation. The controller rebuilds the environment and
    # the launch plan from the sealed inputs it has just re-read, and requires them to equal what the
    # receipt carries — every name and every *value*. A signature could only say "these bytes were
    # blessed once"; this says "these bytes are what the inputs produce right now", which is the
    # claim a commit point actually needs and which no stolen capability can fake.
    rebuilt_environment = build_child_environment(
        context["parent_environment"],
        candidate_root=context["candidate_root"],
        extra=context.get("extra_environment"),
    )
    if dict(rebuilt_environment) != dict(receipt.environment):
        raise reject(
            "child_environment",
            "the receipt environment is not what the sealed inputs rebuild at commit time",
        )
    sealed = _seal_launch_inputs(context)
    rebuilt_plan = build_launch_plan(
        sealed["document"],
        prompt_path=sealed["prompt_path"],
        candidate_root=context["candidate_root"],
    )
    if rebuilt_plan.command() != receipt.plan.command():
        raise reject(
            "sealed_input",
            "the receipt launch vector is not what the sealed inputs rebuild at commit time",
        )
    if rebuilt_plan.working_directory != receipt.plan.working_directory:
        raise reject(
            "sealed_input",
            "the receipt working directory is not what the sealed inputs rebuild at commit time",
        )

    # WP125-RV-007-R2: byte-for-byte readback of the sealed inputs immediately before the claim.
    readback = assert_launch_inputs_unchanged(context, receipt)

    # Live re-validation. Any of these failing means the claim must not exist, whatever was true
    # when preflight ran.
    rebound = _bind_observations_to_pins(context, receipt.steps[: len(STEP_NAMES)])
    recorded = receipt.steps[len(STEP_NAMES)].observations
    if recorded.get("source_pin_rebound_sha256") != rebound["source_pin_rebound_sha256"]:
        raise reject(
            "authority_mismatch",
            "the source pin re-read at commit time differs from the receipt's binding",
        )
    lease = context.get("lease")
    if not isinstance(lease, Mapping):
        raise reject("lease_expired", "the pinned context carries no lease to re-check")
    stop = parse_utc(lease.get("effective_stop_utc"), "lease.effective_stop_utc")
    now = context.get("now_utc") or datetime.datetime.now(datetime.timezone.utc)
    if (stop - now).total_seconds() <= 0:
        raise reject("lease_expired", "the lease reached its absolute stop before the claim")

    record = dict(payload)
    record["preflight_receipt_sha256"] = receipt.receipt_hash()
    record["canonical_receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    record["revalidated_at_commit"] = True
    record["sealed_input_readback"] = readback["readback"]
    created, stored = ledger.record(reconcile_key, record)
    if not created and stored != record:
        raise reject("duplicate_claim", "a conflicting payload already answers to this reconcile key")
    return {"created": created, "record": stored, "reconcile_key": reconcile_key}
