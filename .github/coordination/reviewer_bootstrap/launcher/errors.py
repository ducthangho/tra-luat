"""Typed, redaction-safe rejection errors for the WP125 launcher and watchdog.

Every fail-closed path in this Packet raises :class:`LauncherRejected` with a stable machine
category.  Categories are the contract; the human message is not.  Tests assert on the category so
that rewording a diagnostic can never silently retire a control.

Diagnostics never interpolate untrusted text.  Issue bodies, PR text, diffs, command output, model
text, repository paths and candidate reports are data; embedding them in an error string is how a
redaction boundary leaks, and how a category becomes attacker-selected.
"""

from __future__ import annotations

# The closed category set.  `validate_category` refuses anything outside it, so a typo raises at the
# raise site instead of inventing a category that no test is watching.
CATEGORIES = (
    "argument_vector",
    "permission_mode",
    "child_environment",
    "sealed_input",
    "preflight_incomplete",
    "preflight_order",
    "authority_mismatch",
    "lease_expired",
    "write_set",
    "stale_generation",
    "duplicate_claim",
    "sandbox_unavailable",
    "delegation_scope",
    "delegation_credential",
    "delegation_evidence",
    "parity_mismatch",
    "watchdog_identity",
    "watchdog_cleanup",
    "artifact_integrity",
)

_CATEGORIES = frozenset(CATEGORIES)


class LauncherRejected(Exception):
    """A fail-closed rejection carrying a stable machine category."""

    def __init__(self, category: str, message: str):
        if category not in _CATEGORIES:
            raise ValueError("unknown launcher rejection category: %r" % (category,))
        self.category = category
        super().__init__(message)


def reject(category: str, message: str) -> LauncherRejected:
    return LauncherRejected(category, message)
