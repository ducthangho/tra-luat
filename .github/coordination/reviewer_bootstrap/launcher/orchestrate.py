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

    def as_dict(self) -> dict[str, object]:
        return {
            "preflight": self.receipt.as_dict(),
            "preflight_receipt_sha256": self.receipt.receipt_hash(),
            "claim": {
                "created": self.claim.get("created"),
                "reconcile_key": self.claim.get("reconcile_key"),
            },
            "argument_vector": describe_plan(self.receipt.plan),
            "child_environment": describe_environment(self.receipt.environment),
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
    lease_effective_stop_utc: str,
    label: str = "reviewer-child",
) -> LaunchRecord:
    """Preflight, then claim, then one contained child.  Refuses at the first failure.

    Returns a :class:`LaunchRecord`.  A failed preflight raises rather than returning a half record,
    because the caller that wants a negative outcome should call :func:`~launcher.preflight.run_preflight`
    directly and inspect the receipt — this function's contract is "a child ran, and here is the
    ordered evidence that it was allowed to".
    """
    receipt = run_preflight(context)
    if not receipt.complete:
        failure = receipt.failure or {}
        raise reject(
            failure.get("category", "preflight_incomplete"),
            "preflight refused at step %s" % failure.get("step"),
        )

    claim = mint_claim(receipt, ledger, reconcile_key, claim_payload)

    deadline = build_deadline(timeout_seconds, lease_effective_stop_utc)
    plan = receipt.plan
    if plan is None:
        raise reject("preflight_incomplete", "the trusted receipt carries no launch plan")

    # Deferred import: the watchdog is already imported for the deadline, but the supervised runner is
    # taken from the module rather than bound at import time so a test can observe the real call.
    from .watchdog import run_supervised

    outcome = run_supervised(
        plan.command(),
        environment=receipt.environment,
        working_directory=plan.working_directory,
        deadline=deadline,
        label=label,
    )
    return LaunchRecord(receipt=receipt, claim=claim, outcome=outcome)
