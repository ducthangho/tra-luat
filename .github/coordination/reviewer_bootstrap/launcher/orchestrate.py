"""The one trusted path from preflight to a contained child (Issue 125 §5–§6, WP125-RV-004).

Generation 1 had every piece of this sequence and no single place that performed it.  Preflight
built a plan and an environment, the claim was mintable, the watchdog could supervise a command —
but nothing tied them together, so the only callers that ever ran the real sequence were tests, each
assembling it slightly differently.  That is how an ordering invariant rots: not by being violated,
but by never being expressed anywhere a reviewer can point at.

:func:`launch_reviewer` is that place.  It runs the trusted preflight, mints the claim from the
receipt it just produced, and launches exactly the plan that preflight authorised — ``plan.command()``
with ``receipt.environment`` in ``plan.working_directory`` under a deadline bounded by the lease.
Nothing in between can substitute a different vector, because nothing in between is given the
opportunity: the plan object the watchdog receives is the one the receipt carries.

The order is claim-before-launch, and it is enforced by control flow rather than by comment.  If
:func:`~launcher.preflight.mint_claim` raises, no child is created, and the caller can prove zero
children the same way it proves zero claims.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping

from core.ledger import Ledger

from .argv import describe as describe_plan
from .environment import describe as describe_environment
from .errors import reject
from .preflight import (
    PreflightReceipt,
    assert_launch_inputs_unchanged,
    mint_claim,
    run_preflight,
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
            "ordering": [
                "preflight",
                "value_binding",
                "routing_validation",
                "claim",
                "sealed_input_readback",
                "launch",
            ],
        }


def launch_reviewer(
    context: Mapping[str, object],
    *,
    ledger: Ledger,
    reconcile_key: str,
    claim_payload: Mapping[str, object],
    timeout_seconds: float,
    label: str = "reviewer-child",
    delegated_job=None,
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
    if surface == "delegated_linux_run_test":
        _validate_delegated_job(delegated_job)
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

    claim = mint_claim(receipt, ledger, reconcile_key, claim_payload, context=context)

    # WP125-RV-007-R2: the second readback, immediately before anything is spawned or dispatched.
    assert_launch_inputs_unchanged(context, receipt)

    if surface == "delegated_linux_run_test":
        # WP125-RV-008-R2.  The delegated surface goes through the complete existing validator and
        # runner, not a hand-picked command out of the job.  Round 2 pulled `commands[0]` and ran it
        # directly, which skipped the Linux identity check, the read-only-root proof, the credential
        # probe, the per-test real return codes and the cleanup receipt — every control that makes a
        # delegated result mean anything.
        from .delegation import run_job

        evidence = run_job(
            delegated_job,
            parent_environment=dict(context.get("parent_environment") or {}),
            candidate_root=str(context["candidate_root"]),
            working_directory=delegated_job.read_only_root,
            deadline=deadline,
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


def _validate_delegated_job(job: object) -> None:
    """Refuse an unknown or partial delegated job before any claim exists.

    The job is only accepted when it is a real :class:`~launcher.delegation.DelegatedJob` carrying
    the closed operation, a verified read-only root, an exact candidate identity and a non-empty
    declared selection drawn entirely from the closed test map.  "Looks about right" is how a partial
    job becomes a green run.
    """
    from .delegation import DELEGATED_TESTS, DelegatedJob

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
    if not job.test_selection:
        raise reject("delegation_evidence", "the delegated job declares no test selection")
    unknown = [item for item in job.test_selection if item not in DELEGATED_TESTS]
    if unknown:
        raise reject("delegation_scope", "the delegated job names %d unknown tests" % len(unknown))
    if len(job.commands) != len(job.test_selection):
        raise reject("delegation_evidence", "the delegated job is partial: commands do not cover the selection")
    if not job.root_evidence or job.root_evidence.get("writability_probe") != "refused":
        raise reject("delegation_scope", "the delegated job carries no proven read-only root")
    if job.root_evidence.get("head") != job.candidate_head:
        raise reject("delegation_scope", "the delegated root identity does not match the job head")
    if job.root_evidence.get("tree") != job.candidate_tree:
        raise reject("delegation_scope", "the delegated root identity does not match the job tree")
