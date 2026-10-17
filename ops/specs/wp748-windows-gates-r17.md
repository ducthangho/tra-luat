# WP748 r17/g17 — complete Windows gates on preserved exact head

## Authority, provenance, roles

Owner authorization: https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6231338050 (comment ID 6231338050, exact readback). This revision supersedes stale r16/g16 without changing its two-level gate, twelve-path write set, provider or other acceptance. All r16/r15/r14/r13/r12/r11/r9/r8 requirements and stop conditions remain. The g16 bilateral tombstone must be effective before any g17 Executor write. The g16 product clone is clean at its exact source head/tree, unpushed, and has no PR or review.

Immutable acceptance base: `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. Continuation source: unpushed g16 product branch `agent/wp748-g16-claude` at commit `19683a0b81ba33010fbee4e5a03631d3023a76b7`, tree `aa2f3a35d2ef1244ec50f6220b7e68618cdc87ac`, clean index/worktree. It contains three committed g16 changes and exactly twelve paths changed from the acceptance base, matching the effective write set below. g17 may transfer only this exact committed source head into a fresh isolated clone after source/destination head, tree, diff, write-set and holder checks; record provenance. No previous gate credit transfers to a changed head.

Executor: Claude Code Opus 5.5 (`anthropic_claude`, `claude_code`, local Windows), sole writer in fresh `agent/wp748-g17-claude` clone. Reviewer: fresh independent Codex session, read-only on exact final Executor head. Review Class remains sensitive with cross-provider assurance. Dispatcher writes only coordination metadata. No self-review, merge, land, LIVE, deploy or real credentials.

## Effective Executor write set

1. `ops/bash_nen.py`
2. `ops/cong_cu_test.py`
3. `ops/lease_publish_test.py`
4. `.claude/dev/ci_dang_ky_test.py`
5. `ops/nhanh_don_duoc_test.py`
6. `.github/workflows/ci.yml`
7. `.github/workflows/ci-dot-bien-du.yml`
8. `ops/ci_duong_nhanh_test.py`
9. `.claude/dev/doc_receipt_thu_hoi_test.py`
10. `.claude/skills/work-packet/SKILL.md`
11. `.agents/skills/work-packet/SKILL.md`
12. `.claude/hooks/subagent_ghi_detect_test.py`

`.claude/settings.json` and `.claude/hooks/subagent_ghi_detect.py` remain outside scope. A demonstrated need to edit either requires another revision and generation.

## Two-level fast-mutant acceptance

### `targeted_mutant_gate` — each PR candidate

Run all 52 baseline self-check cases, all 239 named self mutants against their declared target cases, and all 10 named product mutants. Every self mutant must have a nonempty declared target set. Preserve all 249 distinct mutant identities and fail-closed behavior: a failing baseline, missing target, missing or duplicate mutant, stale source/head, absent proof, child failure, timeout, uncertain containment or unmeasured shard makes the gate red. Test result classification must distinguish `passed`, `failed`, `skipped`, `not_run`, `not_measured` and `inconclusive`.

Each bounded shard must emit an exact source/head hash, target-case manifest, separate real rc, start/end time, progress naming the current mutant/case, bounded log, peak RAM and rerun count. Merge must verify full membership and every shard receipt before reporting a score. The full 249-identity gate's measured critical path on comparable Windows must be at most 540 seconds. Parallelism, theoretical case counts and increased timeouts alone do not prove this target. The 52-case read-only profile on g12 took 274.8 seconds, rc0; its JSON SHA256 is `e74ad9320eb92c31868d2039a114241382d810ea7eaefdc5e3e13e21cc5b45a0`.

The targeted gate measures the declared causal tests for each self mutant. It does not establish that non-target cases remain green under every mutant. Its receipts and UI text must never call it the full mutant audit.

### `full_mutant_audit` — before merge, land or release

Run the original all-52-cases-under-each-of-239-self-mutants matrix and all 10 product mutants separately on a suitable runner against the exact candidate SHA. Preserve individual names, real rc, bounded progress and complete positive receipts. A missing, failed, stale or unmeasured audit blocks merge, land and release. No targeted receipt can substitute for it. If the machine cannot complete the audit, report the limit and leave those actions blocked; do not silently reduce the matrix.

## Hook, registry and other gates

Resolve Windows registry t12/t21 under r12 rules. Retain fail-closed `unknown`; the intermittent t12 full-registry cause remains unproven. The g16 exact head has positive targeted t12/t21 receipts (10/10 each, rc0) and targeted mutant gate receipts (52/52 baseline, 239/239 declared-target self mutants, 10/10 product mutants, merged rc0, critical path 339.81 seconds). Verify their command, rc, exact head/tree and environment before credit. The g16 full hook suite logged 45 baseline cases and eleven mutant kills, then ended without rc; classify it inconclusive and measure the missing work with explicit composite limitations or run a new full suite. Do not rerun completed cases merely because the host slept. Confirm actual hook transport and negative Bash capability cases. Full Windows registry needs positive per-child receipts and real rc. Do not cancel a long registry merely because laptop sleep increased elapsed wall time; retain progress and actual rc. The prior full lease-publish rc1 stays rc1 despite separate t35–t40 passes.

On committed exact head, run all r12/r11/r9/r8 gates: full registry, Windows symlink and fast-path suites, lease-publish, doc receipt, G5, selftest, Ruff F delta zero, secret scan and diff check. Run heavy local suites serially unless bounded parallelism is itself the measured fast-mutant design. Required CI checks on the exact pushed candidate and fresh independent read-only review with zero P1/P2 are mandatory. Changed head invalidates review and gate claims.

Push product code once per PR only after fixes, complete local gates and independent zero-P1/P2 review. Exact-head CI and the separate full mutant audit remain prerequisites for any later merge/land request. No merge, land or LIVE authority is granted here.

## Preflight and stop conditions

Before any g17 Executor write, verify owner comment, spec/ref/hash, g16 tombstone and bilateral readback, fresh isolated clone and branch, exact source/base/head/tree, clean destination, committed source provenance, live full refs, unique holder on all twelve paths, valid g17 lease/expiry, and provider/model/surface. The missing `agent/wp484-g7-claude` remote-ref cache entry must be repaired and the holder scan conclusive. Stop on any mismatch, overlap, stale generation, denied tool, need outside write set, missing positive evidence, or repeated finding at protocol cap. Complete expensive read-only ref/holder/preflight work before publishing the g17 lease; then perform short final checks and start the sole Executor promptly. The 30-minute no-progress lease rule still applies. Do not report targeted or background evidence as full pass.
