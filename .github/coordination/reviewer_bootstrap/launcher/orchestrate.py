"""The one trusted path from preflight to a contained child (Issue 125 §5–§6, WP125-RV-004).

Generation 1 had every piece of this sequence and no single place that performed it.  Preflight
built a plan and an environment, the claim was mintable, the watchdog could supervise a command —
but nothing tied them together, so the only callers that ever ran the real sequence were tests, each
assembling it slightly differently.  That is how an ordering invariant rots: not by being violated,
but by never being expressed anywhere a reviewer can point at.

:func:`launch_reviewer` is that place.  It runs the trusted preflight, verifies the claim against the
receipt it just produced, hands that verification to the outside commit adapter, and launches exactly
the plan that preflight authorised — ``plan.command()`` with ``receipt.environment`` in
``plan.working_directory`` under a deadline bounded by the lease.  Nothing in between can substitute
a different vector, because nothing in between is given the opportunity: the plan object the watchdog
receives is the one the receipt carries.

The order is claim-before-launch, and it is enforced by control flow rather than by comment.  If
:func:`~launcher.preflight.verify_claim_authorization` raises, no child is created, and the caller
can prove zero children the same way it proves zero claims.

WP125-RV-003-R5: this module holds no durable store.  ``commit_capability`` is a required keyword
argument supplied by the outside trusted controller; there is no default, no factory, no registry and
no fallback, so importing this module and calling :func:`launch_reviewer` cannot create a claim.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping

from .argv import describe as describe_plan
from .environment import describe as describe_environment
from .errors import reject
from .preflight import (
    ClaimVerification,
    PreflightReceipt,
    assert_launch_inputs_unchanged,
    bind_commit_result,
    run_preflight,
    verify_claim_authorization,
)
from .watchdog import RunOutcome, build_deadline


@dataclasses.dataclass(frozen=True)
class LaunchRecord:
    """Everything one supervised launch produced, in the order it produced it."""

    receipt: PreflightReceipt
    claim: Mapping[str, object]
    outcome: RunOutcome | None
    launched: str = "windows_reviewer_vector"
    delegation_evidence: Mapping[str, object] | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "delegation_evidence": dict(self.delegation_evidence or {}),
            "preflight": self.receipt.as_dict(),
            "preflight_receipt_sha256": self.receipt.receipt_hash(),
            "claim": {
                "created": self.claim.get("created"),
                "reconcile_key": self.claim.get("reconcile_key"),
            },
            "surface": self.receipt.surface,
            "launched": self.launched,
            "model_command_invoked": self.launched == "windows_reviewer_vector",
            "argument_vector": (
                describe_plan(self.receipt.plan) if self.receipt.plan is not None else {}
            ),
            "child_environment": describe_environment(self.receipt.environment),
            "deadline_source": "trusted_preflight_lease_observation",
            "outcome": self.outcome.as_dict() if self.outcome is not None else {},
            # The order this record was actually produced in, named step by step.  WP125-RV-008-R5
            # adds the two transport steps explicitly: an auditor should be able to see that the
            # route was authenticated before the claim *and* again immediately before the dispatch,
            # rather than infer it from the absence of a complaint.
            "ordering": [
                "preflight",
                "value_binding",
                "routing_validation",
                "transport_authentication",
                "claim_verification",
                "claim_commit_by_outside_capability",
                "sealed_input_readback",
                "transport_reauthentication",
                "launch",
            ],
        }


def commit_claim(commit_capability: object, verification: ClaimVerification) -> dict[str, object]:
    """Call the outside adapter, and check that what came back answers this verification.

    Deliberately tiny, and deliberately incapable.  It cannot make an adapter, find one, or proceed
    without one: a missing capability is a named rejection before anything durable, and a capability
    that answers with someone else's record is rejected by
    :func:`~launcher.preflight.bind_commit_result`.
    """
    if commit_capability is None:
        raise reject(
            "claim_authority",
            "no outside commit capability was supplied; a claim cannot be created here",
        )
    if not callable(commit_capability):
        raise reject("claim_authority", "the supplied commit capability is not callable")
    return bind_commit_result(verification, commit_capability(verification))


def launch_reviewer(
    context: Mapping[str, object],
    *,
    commit_capability: object,
    reconcile_key: str,
    claim_payload: Mapping[str, object],
    timeout_seconds: float,
    label: str = "reviewer-child",
    delegated_job=None,
    linux_transport: object = None,
) -> LaunchRecord:
    """Preflight, then claim, then one contained child on the surface preflight selected.

    Returns a :class:`LaunchRecord`.  A failed preflight raises rather than returning a half record,
    because the caller that wants a negative outcome should call :func:`~launcher.preflight.run_preflight`
    directly and inspect the receipt — this function's contract is "a child ran, and here is the
    ordered evidence that it was allowed to".

    ``lease_effective_stop_utc`` is deliberately *not* a parameter — see below.
    """
    receipt = run_preflight(context)
    if not receipt.complete:
        failure = receipt.failure or {}
        raise reject(
            failure.get("category", "preflight_incomplete"),
            "preflight refused at step %s" % failure.get("step"),
        )

    # WP125-RV-009-R2.  Everything about routing and timing is settled *before* the claim commit.
    # Round 2 minted the claim first and only then discovered that the delegated surface had no job,
    # or a job of the wrong shape — so an invalid routing input left a durable claim behind while
    # proving nothing ran.  A claim is the record that a run was authorised; it must not outlive the
    # discovery that the run was never permissible.
    surface = receipt.surface
    delegated_authentication: dict[str, object] | None = None
    if surface == "delegated_linux_run_test":
        delegated_authentication = authenticate_delegated_job(
            delegated_job, context, transport=linux_transport
        )
        launched = "delegated_run_test"
    elif surface == "windows":
        if delegated_job is not None:
            raise reject("delegation_scope", "a delegated job was supplied for the Windows surface")
        if receipt.plan is None:
            raise reject("preflight_incomplete", "the trusted receipt carries no launch plan")
        launched = "windows_reviewer_vector"
    else:
        raise reject("sandbox_unavailable", "the receipt names no known execution surface")

    # WP125-RV-009.  The lease stop comes from the observation the trusted preflight validated, not
    # from an argument.  Generation 2 accepted it as a caller parameter, which gave the fence a
    # second, independent source of truth: preflight could validate one stop and the watchdog could
    # be bounded by another, and nothing compared them.  A fence with two clocks has no clock.
    lease_stop = str(receipt.steps[1].observations["lease_effective_stop_utc"])
    deadline = build_deadline(timeout_seconds, lease_stop)

    verification = verify_claim_authorization(
        receipt, context=context, reconcile_key=reconcile_key, payload=claim_payload
    )
    claim = commit_claim(commit_capability, verification)

    # WP125-RV-007-R2: the second readback, immediately before anything is spawned or dispatched.
    assert_launch_inputs_unchanged(context, receipt)

    if surface == "delegated_linux_run_test":
        # WP125-RV-009-R3: the *same* sealed job is authenticated again immediately before dispatch.
        # The first pass happened before the claim; between then and now a claim was minted and the
        # sealed inputs were re-read, and any of that time is time for the root or the job to move.
        redispatch = authenticate_delegated_job(
            delegated_job, context, transport=linux_transport
        )
        if redispatch["root_evidence"]["head"] != delegated_authentication["root_evidence"]["head"]:
            raise reject("delegation_scope", "the delegated root moved between claim and dispatch")

        # WP125-RV-008-R5.  The authenticated transport is *invoked*.  Round 5 required the transport
        # to be truthy and then ran the job locally, so a Windows controller with a declared Linux
        # route produced a local result wearing a Linux label — which is the one thing §7 forbids
        # outright.  The dispatch below crosses the boundary or it fails closed; there is no third
        # branch, and in particular there is no branch that runs the tests here.
        from .delegation import dispatch_run_test

        evidence = dispatch_run_test(
            redispatch["transport"],
            job=delegated_job,
            context=context,
            deadline=deadline,
            receipt_sha256=verification.receipt_sha256,
            authentication=redispatch,
        )
        return LaunchRecord(
            receipt=receipt,
            claim=claim,
            outcome=None,
            launched=launched,
            delegation_evidence=evidence,
        )

    # Deferred import so a test can observe the real call rather than an import-time binding.
    from .watchdog import run_supervised

    outcome = run_supervised(
        receipt.plan.command(),
        environment=receipt.environment,
        working_directory=receipt.plan.working_directory,
        deadline=deadline,
        label=label,
    )
    return LaunchRecord(receipt=receipt, claim=claim, outcome=outcome, launched=launched)


def authenticate_delegated_job(
    job: object, context: Mapping[str, object], *, transport: object = None
) -> dict[str, object]:
    """Re-derive the delegated job from the controller's own inputs (WP125-RV-008-R3).

    Round 3 checked the job against *itself*: it asked whether the commands covered the selection and
    whether the root evidence agreed with the head the job carried.  A job that was internally
    consistent and entirely fabricated passed every one of those questions, because the answers came
    from the same object being examined.

    Nothing here trusts the job.  The transport envelope is authenticated against the sealed pin,
    every command is reconstructed from the closed test-ID map and compared to what the job carries,
    so a caller-authored command cannot survive.  The read-only root is re-probed live, and the
    candidate commit, tree and credential surface are measured again from the root itself.  The
    runner OS is *not* read from this machine: it is a property of the far side and is measured there
    and re-bound when the evidence comes back (WP125-RV-008-R5).
    """
    from .delegation import (
        DELEGATED_TESTS,
        DelegatedJob,
        authenticate_transport,
        build_expected_commands,
        verify_read_only_root,
    )

    if job is None:
        raise reject(
            "delegation_scope",
            "the delegated surface was selected but no closed run_test job was supplied",
        )
    if not isinstance(job, DelegatedJob):
        raise reject("delegation_scope", "the delegated job is not an authenticated DelegatedJob")
    if job.operation != "run_test":
        raise reject(
            "delegation_scope",
            "only the closed run_test operation may be dispatched on the delegated surface",
        )

    # WP125-RV-008-R5.  An *authenticated transport envelope*, not a truthy value.  Round 4 read
    # `context["delegated_linux_transport"]` and asked only whether it was truthy — the string
    # ``"yes"`` configured a Linux route — and then required the *local* machine to be Linux, which
    # on a Windows controller meant the delegated surface could never be exercised at all and, on a
    # Linux one, meant "local" was silently accepted as "delegated".  Both readings are wrong for the
    # same reason: the runner OS is a property of the far side, so it has to be measured there and
    # returned, not measured here.
    #
    # The envelope is authenticated against the sealed pin below.  If none is configured the surface
    # is environment-unavailable and the run pauses; nothing local stands in for it.
    envelope = transport if transport is not None else context.get("delegated_linux_transport")
    authenticated = authenticate_transport(envelope, context)

    if job.expected_os != "Linux":
        raise reject("delegation_scope", "the delegated job was not built for a Linux runner")

    if not job.test_selection:
        raise reject("delegation_evidence", "the delegated job declares no test selection")
    unknown = [item for item in job.test_selection if item not in DELEGATED_TESTS]
    if unknown:
        raise reject("delegation_scope", "the delegated job names %d unknown tests" % len(unknown))
    if len(set(job.test_selection)) != len(job.test_selection):
        raise reject("delegation_evidence", "the delegated test selection repeats an entry")

    # Live re-probe of the root, and an independent re-measure of the candidate identity.
    root_evidence = verify_read_only_root(
        job.read_only_root,
        candidate_root=str(context["candidate_root"]),
        candidate_head=job.candidate_head,
        candidate_tree=job.candidate_tree,
    )
    if root_evidence["head"] != job.candidate_head or root_evidence["tree"] != job.candidate_tree:
        raise reject("delegation_scope", "the re-measured root identity does not match the job")
    if job.root_evidence.get("head") != root_evidence["head"]:
        raise reject("delegation_scope", "the job carries stale or fabricated root evidence")
    if job.root_evidence.get("tree") != root_evidence["tree"]:
        raise reject("delegation_scope", "the job carries stale or fabricated root evidence")
    if root_evidence["writability_probe"] != "refused":
        raise reject("delegation_scope", "the delegated root is writable at dispatch time")

    # Commands are reconstructed, not inspected. Comparing the job's commands to the closed map is
    # the only way a caller-authored command becomes visible.
    expected = build_expected_commands(job.test_selection, job.read_only_root)
    if tuple(tuple(item) for item in job.commands) != expected:
        raise reject(
            "delegation_scope",
            "the delegated commands are not the ones the closed test map reconstructs",
        )

    return {
        "transport": envelope,
        "transport_identity": authenticated,
        "runner_os_is_measured_at_the_far_side": True,
        "root_evidence": root_evidence,
        "commands_reconstructed": True,
        "selection": list(job.test_selection),
    }
