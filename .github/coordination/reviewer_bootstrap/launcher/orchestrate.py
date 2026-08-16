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
from .preflight import PreflightReceipt, mint_claim, run_preflight
from .watchdog import RunOutcome, build_deadline


@dataclasses.dataclass(frozen=True)
class LaunchRecord:
    """Everything one supervised launch produced, in the order it produced it."""

    receipt: PreflightReceipt
    claim: Mapping[str, object]
    outcome: RunOutcome
    launched: str = "windows_reviewer_vector"

    def as_dict(self) -> dict[str, object]:
        return {
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
            "outcome": self.outcome.as_dict(),
            "ordering": ["preflight", "value_binding", "claim", "launch"],
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

    claim = mint_claim(receipt, ledger, reconcile_key, claim_payload, context=context)

    # WP125-RV-009.  The lease stop comes from the observation the trusted preflight validated, not
    # from an argument.  Generation 2 accepted it as a caller parameter, which gave the fence a
    # second, independent source of truth: preflight could validate one stop and the watchdog could
    # be bounded by another, and nothing compared them.  A fence with two clocks has no clock.
    lease_stop = str(receipt.steps[1].observations["lease_effective_stop_utc"])
    deadline = build_deadline(timeout_seconds, lease_stop)

    # Deferred import: the watchdog is already imported for the deadline, but the supervised runner is
    # taken from the module rather than bound at import time so a test can observe the real call.
    from .watchdog import run_supervised

    # WP125-RV-008.  Route on the surface preflight selected.  Generation 2 launched the full
    # Reviewer vector regardless, so a run that had *proved* no usable Windows sandbox existed would
    # still mint and invoke the local model command — the exact operation §7 forbids delegating, run
    # on the surface that was chosen because it may not run it.
    if receipt.surface == "delegated_linux_run_test":
        if delegated_job is None:
            raise reject(
                "delegation_scope",
                "the delegated surface was selected but no closed run_test job was supplied",
            )
        if getattr(delegated_job, "operation", None) != "run_test":
            raise reject(
                "delegation_scope",
                "only the closed run_test operation may be dispatched on the delegated surface",
            )
        command = tuple(delegated_job.commands[0])
        launched = "delegated_run_test"
    else:
        plan = receipt.plan
        if plan is None:
            raise reject("preflight_incomplete", "the trusted receipt carries no launch plan")
        if delegated_job is not None:
            raise reject(
                "delegation_scope",
                "a delegated job was supplied for the Windows surface",
            )
        command = plan.command()
        launched = "windows_reviewer_vector"

    outcome = run_supervised(
        command,
        environment=receipt.environment,
        working_directory=(
            delegated_job.read_only_root
            if receipt.surface == "delegated_linux_run_test"
            else receipt.plan.working_directory
        ),
        deadline=deadline,
        label=label,
    )
    return LaunchRecord(receipt=receipt, claim=claim, outcome=outcome, launched=launched)
