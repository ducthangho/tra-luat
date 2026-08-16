"""Windows / delegated-Linux parity matrix (Issue 125 §7, closing paragraphs).

Delegation is a fallback, not a substitute.  The failure this module exists to prevent is the one
that looks like success: a Linux run that quietly schedules fewer cases than Windows, or marks the
awkward ones "not applicable", and then reports a clean green that nobody can distinguish from a
clean green over the full set.

So the comparison is on *denominators first*.  A portable case ID that one side never scheduled is
red on that side, whatever the other side did.  A case may only be absent when it appears in the
explicitly declared platform-specific table with a reason — declared in the registry, in advance,
not decided by whichever runner happened to find the case inconvenient.

Outcomes are normalized before comparison because the two platforms genuinely spell some things
differently — a fence category, a return code from a signal.  Normalization is a named mapping so a
reviewer can see exactly which differences were forgiven, rather than trusting that "roughly equal"
meant what they hoped.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping, Sequence

from .errors import reject

# Outcome spellings that mean the same thing on both platforms.  Anything not listed compares
# literally; adding an entry here is a deliberate, reviewable act of forgiveness.
NORMALIZED_OUTCOMES: Mapping[str, str] = {
    "passed": "passed",
    "ok": "passed",
    "failed": "failed",
    "error": "failed",
    "skipped": "skipped",
    "not_run": "not_run",
}

# Fence categories are named identically on both sides on purpose; the mechanism differs (job object
# versus process group) but the *category* is the contract and must not diverge.
FENCE_CATEGORIES = ("fenced_by_controller", "completed_without_fence", "cleanup_unproven")


@dataclasses.dataclass(frozen=True)
class SideReport:
    """One platform's contribution to the matrix."""

    platform: str
    scheduled: tuple[str, ...]
    outcomes: Mapping[str, str]
    argument_observations: Mapping[str, object]
    environment_observations: Mapping[str, object]
    claim_ordering: tuple[str, ...]
    fence_categories: Mapping[str, str]

    def as_dict(self) -> dict[str, object]:
        return {
            "platform": self.platform,
            "scheduled": list(self.scheduled),
            "scheduled_count": len(self.scheduled),
            "outcomes": dict(self.outcomes),
            "argument_observations": dict(self.argument_observations),
            "environment_observations": dict(self.environment_observations),
            "claim_ordering": list(self.claim_ordering),
            "fence_categories": dict(self.fence_categories),
        }


def normalize(outcome: object) -> str:
    if not isinstance(outcome, str):
        raise reject("parity_mismatch", "an outcome is not a string")
    normalized = NORMALIZED_OUTCOMES.get(outcome)
    if normalized is None:
        raise reject("parity_mismatch", "outcome %r has no declared normalization" % (outcome,))
    return normalized


def compare(
    primary: SideReport,
    secondary: SideReport | None,
    *,
    portable_ids: Sequence[str],
    platform_specific: Mapping[str, str],
) -> dict[str, object]:
    """Compare two sides, or record that only the primary side applied.

    ``secondary`` is ``None`` when delegation was never selected — the contract requires delegated
    evidence only when the fallback is used.  That is recorded explicitly as
    ``secondary_side_applicable: false`` rather than by omitting the field, because a missing field
    reads as an oversight and an explicit false reads as a decision.
    """
    portable = tuple(portable_ids)
    if not portable:
        raise reject("parity_mismatch", "the parity matrix declares zero portable cases")

    findings: list[dict[str, object]] = []
    sides = [primary] + ([secondary] if secondary is not None else [])

    for side in sides:
        missing = [case for case in portable if case not in side.scheduled]
        if missing:
            findings.append(
                {
                    "kind": "shrunken_denominator",
                    "platform": side.platform,
                    "missing_case_count": len(missing),
                    "missing_cases": missing,
                }
            )
        undeclared = [
            case
            for case in side.scheduled
            if side.outcomes.get(case) in ("skipped", "not_run") and case not in platform_specific
        ]
        if undeclared:
            findings.append(
                {
                    "kind": "undeclared_not_applicable",
                    "platform": side.platform,
                    "case_count": len(undeclared),
                    "cases": undeclared,
                }
            )

    if secondary is not None:
        for case in portable:
            left = primary.outcomes.get(case)
            right = secondary.outcomes.get(case)
            if left is None or right is None:
                continue
            if normalize(left) != normalize(right):
                findings.append(
                    {
                        "kind": "outcome_divergence",
                        "case": case,
                        primary.platform: left,
                        secondary.platform: right,
                    }
                )
        for label, left_map, right_map in (
            ("argument", primary.argument_observations, secondary.argument_observations),
            ("environment", primary.environment_observations, secondary.environment_observations),
        ):
            for key in sorted(set(left_map) | set(right_map)):
                if left_map.get(key) != right_map.get(key):
                    findings.append(
                        {
                            "kind": "%s_observation_divergence" % label,
                            "key": key,
                            primary.platform: left_map.get(key),
                            secondary.platform: right_map.get(key),
                        }
                    )
        if list(primary.claim_ordering) != list(secondary.claim_ordering):
            findings.append({"kind": "claim_ordering_divergence"})
        for case in sorted(set(primary.fence_categories) | set(secondary.fence_categories)):
            left = primary.fence_categories.get(case)
            right = secondary.fence_categories.get(case)
            if left != right:
                findings.append(
                    {
                        "kind": "fence_category_divergence",
                        "case": case,
                        primary.platform: left,
                        secondary.platform: right,
                    }
                )

    for case, reason in platform_specific.items():
        if not reason:
            findings.append({"kind": "platform_specific_without_reason", "case": case})

    return {
        "portable_case_count": len(portable),
        "secondary_side_applicable": secondary is not None,
        "sides": [side.as_dict() for side in sides],
        "platform_specific": dict(platform_specific),
        "findings": findings,
        "ok": not findings,
    }


def require_ok(matrix: Mapping[str, object]) -> Mapping[str, object]:
    """Turn a red matrix into a named rejection, with a branch rather than ``assert``."""
    if not matrix.get("ok"):
        raise reject(
            "parity_mismatch", "the parity matrix carries %d findings" % len(matrix.get("findings", ()))
        )
    return matrix
