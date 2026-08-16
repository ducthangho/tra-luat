"""The single machine-readable case registry (Issue 125 §8).

One registry owns every required positive, negative and parity case ID.  "One" is the load-bearing
word: when the list of cases lives in the same file as the code that runs them, a case can quietly
stop existing and the denominator shrinks with it, so the suite still reports "all green" over a
smaller set.  Here the registry is declared first and the suite is checked *against* it — a
registered ID with no implementation is ``not_run`` and red, and an implementation with no
registered ID is a duplicate-or-unknown and also red.

Each entry names the required check from the Packet Spec that it serves, so the mapping from the
fifteen ``required_checks`` to executable evidence is data an auditor can read rather than a claim
the README makes.

``PLATFORM_SPECIFIC`` is the *only* place a case may be declared non-applicable, and every entry
carries a reason.  §7 forbids silently marking a required case not applicable; declaring it here, in
advance, with a reason, is the difference between an explicit boundary and a shrinking denominator.
"""

from __future__ import annotations

from collections.abc import Mapping

REQUIRED_CHECKS: tuple[str, ...] = (
    "launcher_source_inventory_and_write_set",
    "permission_mode_and_memory_environment",
    "preflight_before_claim_ordering",
    "controller_watchdog_timeout_and_fence",
    "process_tree_cleanup_and_stale_generation_rejection",
    "windows_sandbox_selection_and_fail_closed",
    "credential_free_delegated_run_test",
    "real_windows_delegated_parity",
    "hostile_input_and_argument_boundary",
    "optimized_python_boundary_controls",
    "eol_policy",
    "repository_selftest",
    "strict_release_verify",
    "release_bundle_determinism",
    "diff_check",
)

# Checks proven outside this suite, by repository gates rather than by launcher cases.  Naming them
# here keeps the mapping total: every required check is either covered by registered cases or is
# explicitly delegated to a named repository gate.
REPOSITORY_GATE_CHECKS: Mapping[str, str] = {
    "repository_selftest": "scripts/tl.py --selftest",
    "strict_release_verify": "scripts/tl.py release-verify --strict",
    "release_bundle_determinism": "two independent scripts/tl.py release-bundle runs",
    "diff_check": "git diff --check",
}

# case_id -> required_check served
CASES: Mapping[str, str] = {
    # -- positive controls (§8 "Positive controls prove ...") -----------------
    "WP125-POS-001-one-valid-claim-launches-exactly-one-child": "preflight_before_claim_ordering",
    "WP125-POS-002-identical-retry-creates-no-duplicate-claim": "preflight_before_claim_ordering",
    "WP125-POS-003-healthy-child-completes-without-fence": "controller_watchdog_timeout_and_fence",
    "WP125-POS-004-real-hang-is-fenced-without-cooperation": "controller_watchdog_timeout_and_fence",
    "WP125-POS-005-authorized-fallback-runs-only-run-test": "credential_free_delegated_run_test",
    "WP125-POS-006-memory-variable-observed-inside-child": "permission_mode_and_memory_environment",
    "WP125-POS-007-argument-boundary-observed-inside-child": "hostile_input_and_argument_boundary",
    "WP125-POS-008-inventory-digest-covers-every-owned-file": "launcher_source_inventory_and_write_set",
    "WP125-POS-009-preflight-runs-in-contract-order": "preflight_before_claim_ordering",
    "WP125-POS-010-artifacts-seal-and-verify": "launcher_source_inventory_and_write_set",
    "WP125-POS-011-deadline-is-bounded-by-the-lease": "controller_watchdog_timeout_and_fence",
    "WP125-POS-012-static-boundary-scan-is-clean": "optimized_python_boundary_controls",
    "WP125-POS-013-owned-text-is-lf-only": "eol_policy",
    "WP125-POS-014-parity-matrix-accepts-equal-sides": "real_windows_delegated_parity",
    # -- permission mode and arguments (§4.1) --------------------------------
    "WP125-NEG-001-permission-mode-omitted": "permission_mode_and_memory_environment",
    "WP125-NEG-002-permission-mode-auto": "permission_mode_and_memory_environment",
    "WP125-NEG-003-permission-mode-bare-auto-casefold": "permission_mode_and_memory_environment",
    "WP125-NEG-004-duplicate-permission-switch": "permission_mode_and_memory_environment",
    "WP125-NEG-005-injected-argument-in-extra-args": "hostile_input_and_argument_boundary",
    "WP125-NEG-006-settings-override-switch": "hostile_input_and_argument_boundary",
    "WP125-NEG-007-executable-inside-candidate-tree": "hostile_input_and_argument_boundary",
    "WP125-NEG-008-relative-executable-path": "hostile_input_and_argument_boundary",
    "WP125-NEG-009-control-characters-in-argument": "hostile_input_and_argument_boundary",
    "WP125-NEG-010-prompt-path-inside-candidate-tree": "hostile_input_and_argument_boundary",
    # -- environment (§4.2) ---------------------------------------------------
    "WP125-NEG-011-credential-shaped-extra-variable": "permission_mode_and_memory_environment",
    "WP125-NEG-012-parent-credentials-are-not-inherited": "permission_mode_and_memory_environment",
    "WP125-NEG-013-path-entry-inside-candidate-tree-is-dropped": "hostile_input_and_argument_boundary",
    "WP125-NEG-014-environment-evidence-carries-no-values": "permission_mode_and_memory_environment",
    # -- sealed inputs (§4.2) -------------------------------------------------
    "WP125-NEG-015-writable-sealed-input": "preflight_before_claim_ordering",
    "WP125-NEG-016-sealed-input-inside-candidate-tree": "preflight_before_claim_ordering",
    "WP125-NEG-017-sealed-input-path-traversal": "preflight_before_claim_ordering",
    "WP125-NEG-018-sealed-input-alternate-data-stream": "preflight_before_claim_ordering",
    "WP125-NEG-019-sealed-input-dos-device": "preflight_before_claim_ordering",
    "WP125-NEG-020-sealed-input-extra-hard-link": "preflight_before_claim_ordering",
    # -- authority, lease, generation (§5) ------------------------------------
    "WP125-NEG-021-wrong-mission-plan-hash": "preflight_before_claim_ordering",
    "WP125-NEG-022-wrong-packet-spec-hash": "preflight_before_claim_ordering",
    "WP125-NEG-023-wrong-attempt": "preflight_before_claim_ordering",
    "WP125-NEG-024-stale-generation": "process_tree_cleanup_and_stale_generation_rejection",
    "WP125-NEG-025-expired-lease": "controller_watchdog_timeout_and_fence",
    "WP125-NEG-026-source-pin-hash-mismatch": "preflight_before_claim_ordering",
    "WP125-NEG-027-write-set-expansion": "launcher_source_inventory_and_write_set",
    "WP125-NEG-028-dirty-worktree": "launcher_source_inventory_and_write_set",
    # -- claim ordering (§5) --------------------------------------------------
    "WP125-NEG-029-claim-before-preflight-completes": "preflight_before_claim_ordering",
    "WP125-NEG-030-fake-always-green-preflight": "preflight_before_claim_ordering",
    "WP125-NEG-031-conflicting-payload-under-one-reconcile-key": "preflight_before_claim_ordering",
    "WP125-NEG-032-negative-preflight-mints-nothing": "preflight_before_claim_ordering",
    # -- hostile children (§6) ------------------------------------------------
    "WP125-NEG-033-hung-child-is-fenced": "controller_watchdog_timeout_and_fence",
    "WP125-NEG-034-detached-descendant-is-fenced": "process_tree_cleanup_and_stale_generation_rejection",
    "WP125-NEG-035-marker-forging-child-is-still-fenced": "controller_watchdog_timeout_and_fence",
    "WP125-NEG-036-output-flood-does-not-escape-cleanup": "process_tree_cleanup_and_stale_generation_rejection",
    "WP125-NEG-037-pid-reuse-is-refused": "process_tree_cleanup_and_stale_generation_rejection",
    # -- surface selection (§7) -----------------------------------------------
    "WP125-NEG-038-no-windows-sandbox-with-valid-delegation": "windows_sandbox_selection_and_fail_closed",
    "WP125-NEG-039-no-windows-sandbox-with-invalid-delegation": "windows_sandbox_selection_and_fail_closed",
    "WP125-NEG-040-no-available-path-pauses-fail-closed": "windows_sandbox_selection_and_fail_closed",
    # -- delegation scope (§7) ------------------------------------------------
    "WP125-NEG-041-delegated-unlisted-operation": "credential_free_delegated_run_test",
    "WP125-NEG-042-delegated-claim-is-refused-by-name": "credential_free_delegated_run_test",
    "WP125-NEG-043-delegation-without-eligibility": "credential_free_delegated_run_test",
    "WP125-NEG-044-delegated-secret-marker-is-detected": "credential_free_delegated_run_test",
    "WP125-NEG-045-delegated-test-selection-escape": "credential_free_delegated_run_test",
    # -- generation-2 review repairs -----------------------------------------
    # Stable finding IDs from the Reviewer relay are preserved in the case names so a disposition can
    # be traced from the finding to the executable counterexample that closes it.
    "WP125-RV-001-closed-extra-name-set-is-accepted": "permission_mode_and_memory_environment",
    "WP125-RV-001-extra-cannot-override-allowlisted-name": "permission_mode_and_memory_environment",
    "WP125-RV-001-extra-case-folded-collision-refused": "permission_mode_and_memory_environment",
    "WP125-RV-001-execution-influencing-extra-refused": "hostile_input_and_argument_boundary",
    "WP125-RV-001-extra-outside-closed-set-refused": "permission_mode_and_memory_environment",
    "WP125-RV-001-extra-value-must-be-identifier-shaped": "hostile_input_and_argument_boundary",
    "WP125-RV-002-declared-test-runs-with-real-return-code": "credential_free_delegated_run_test",
    "WP125-RV-002-failing-declared-test-makes-the-job-red": "credential_free_delegated_run_test",
    "WP125-RV-002-unknown-test-id-refused": "credential_free_delegated_run_test",
    "WP125-RV-002-writable-root-refused": "credential_free_delegated_run_test",
    "WP125-RV-002-missing-root-refused": "credential_free_delegated_run_test",
    "WP125-RV-002-root-identity-mismatch-refused": "credential_free_delegated_run_test",
    "WP125-RV-002-wrong-runner-os-refused-not-fabricated": "real_windows_delegated_parity",
    "WP125-RV-002-credential-marker-absent-inside-real-job": "credential_free_delegated_run_test",
    "WP125-RV-003-seven-function-full-map-mutant-cannot-claim": "preflight_before_claim_ordering",
    "WP125-RV-003-handmade-receipt-cannot-mint-a-claim": "preflight_before_claim_ordering",
    # -- review round 2 ------------------------------------------------------
    "WP125-RV-003-imported-seal-replay-cannot-mint": "preflight_before_claim_ordering",
    "WP125-RV-006-stale-generation-1-authority-is-red": "launcher_source_inventory_and_write_set",
    "WP125-RV-006-empty-delegation-payload-is-red": "launcher_source_inventory_and_write_set",
    "WP125-RV-006-red-matrix-cannot-verify-green": "launcher_source_inventory_and_write_set",
    "WP125-RV-003-commit-point-revalidates-the-sealed-pin": "preflight_before_claim_ordering",
    "WP125-RV-007-caller-selected-executable-cannot-survive-binding": "hostile_input_and_argument_boundary",
    "WP125-RV-007-caller-selected-prompt-cannot-survive-binding": "hostile_input_and_argument_boundary",
    "WP125-RV-007-unsealed-launch-config-is-refused": "preflight_before_claim_ordering",
    "WP125-RV-007-writable-launch-config-is-refused": "preflight_before_claim_ordering",
    "WP125-RV-007-launch-config-hash-drift-is-refused": "preflight_before_claim_ordering",
    "WP125-RV-008-delegated-surface-dispatches-only-run-test": "credential_free_delegated_run_test",
    "WP125-RV-008-delegated-surface-without-a-job-is-refused": "credential_free_delegated_run_test",
    "WP125-RV-009-deadline-has-one-source-the-validated-lease": "controller_watchdog_timeout_and_fence",
    "WP125-RV-010-open-failure-terminates-the-suspended-child": "process_tree_cleanup_and_stale_generation_rejection",
    "WP125-RV-010-assign-failure-terminates-the-suspended-child": "process_tree_cleanup_and_stale_generation_rejection",
    "SPEC-G2-001-bare-forbidden-permission-token-in-trailing-position": "permission_mode_and_memory_environment",
    "SPEC-G2-001-bare-forbidden-permission-token-in-prefix-position": "permission_mode_and_memory_environment",
    "SPEC-G2-001-duplicate-and-conflicting-permission-switches": "permission_mode_and_memory_environment",
    "WP125-G2-GATE-001-delegation-cases-run-from-a-unicode-path-checkout": "real_windows_delegated_parity",
    "WP125-RV-003-value-binding-catches-wrong-plan-hash": "preflight_before_claim_ordering",
    "WP125-RV-003-value-binding-catches-expired-lease": "preflight_before_claim_ordering",
    "WP125-RV-003-value-binding-catches-dirty-worktree": "preflight_before_claim_ordering",
    "WP125-RV-003-complete-receipt-requires-plan-environment-surface": "preflight_before_claim_ordering",
    "WP125-RV-004-orchestration-sequences-preflight-claim-launch": "preflight_before_claim_ordering",
    "WP125-RV-004-vector-observed-through-controlled-fake-executable": "hostile_input_and_argument_boundary",
    "WP125-RV-004-orchestration-refuses-when-preflight-fails": "preflight_before_claim_ordering",
    "WP125-RV-005-failed-job-census-is-red": "controller_watchdog_timeout_and_fence",
    "WP125-RV-005-absent-job-handle-is-red": "controller_watchdog_timeout_and_fence",
    "WP125-RV-005-clean-requires-active-zero-and-clean-identities": "process_tree_cleanup_and_stale_generation_rejection",
    "WP125-RV-006-every-required-artifact-class-is-present": "launcher_source_inventory_and_write_set",
    "WP125-RV-006-deleted-artifact-class-is-red": "launcher_source_inventory_and_write_set",
    "WP125-RV-006-modified-artifact-class-is-red": "launcher_source_inventory_and_write_set",
    "WP125-RV-006-rebound-artifact-identity-is-red": "launcher_source_inventory_and_write_set",
    # -- parity (§7) ----------------------------------------------------------
    "WP125-PAR-001-shrunken-denominator-is-red": "real_windows_delegated_parity",
    "WP125-PAR-002-undeclared-not-applicable-is-red": "real_windows_delegated_parity",
    "WP125-PAR-003-outcome-divergence-is-red": "real_windows_delegated_parity",
    "WP125-PAR-004-fence-category-divergence-is-red": "real_windows_delegated_parity",
    "WP125-PAR-005-forged-success-report-is-red": "real_windows_delegated_parity",
}

# Cases that legitimately do not apply on a platform, each with the reason.  Empty today: every
# registered case runs on both the primary Windows platform and the delegated Linux path, because
# the platform-specific mechanisms (job object versus process group) sit behind a portable API.
PLATFORM_SPECIFIC: Mapping[str, str] = {}

# Cases whose evidence is only obtainable on the primary platform.  These are *scheduled everywhere*
# and simply assert the portable behaviour off Windows; they are listed so the parity comparison can
# explain any mechanism difference without shrinking a denominator.
WINDOWS_MECHANISM_CASES: tuple[str, ...] = (
    "WP125-NEG-034-detached-descendant-is-fenced",
    "WP125-NEG-037-pid-reuse-is-refused",
)

PORTABLE_CASES: tuple[str, ...] = tuple(sorted(CASES))


def check_coverage() -> dict[str, object]:
    """Every required check is either covered by cases or delegated to a named repository gate."""
    covered = set(CASES.values())
    gates = set(REPOSITORY_GATE_CHECKS)
    uncovered = [check for check in REQUIRED_CHECKS if check not in covered and check not in gates]
    unknown = sorted(covered - set(REQUIRED_CHECKS))
    return {
        "required_check_count": len(REQUIRED_CHECKS),
        "case_count": len(CASES),
        "checks_covered_by_cases": sorted(covered),
        "checks_delegated_to_repository_gates": dict(REPOSITORY_GATE_CHECKS),
        "uncovered_required_checks": uncovered,
        "cases_naming_unknown_checks": unknown,
        "ok": not uncovered and not unknown,
    }
