# WP748 r12/g12 — Windows registry hook and fast mutant measurement

## Authority, provenance, roles

Issue #748 owner authorization: https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6207072691. The dispatcher must tombstone g11 before activating g12. Preserve the clean g11 product candidate `5dfb3ee79b4548c1ee4513bec89a74c5bd2fa59d`, tree `8743bb72ebcf02767456bb3398a1e6527b6bed36`, as the exact g12 starting commit. Immutable acceptance base: `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. The r8, r9, r11 specs continue to govern all previously required gates except the explicit measurement changes below.

Executor: Claude Code Opus 5.5 (`anthropic_claude`, `claude_code`, local Windows), isolated `agent/wp748-g12-claude` clone. Reviewer: fresh independent Codex session, read-only on exact final Executor head. Sensitive Review Class; cross-provider assurance. Dispatcher owns coordination metadata only. No self-review, merge, land, LIVE, deploy, real credentials or writing outside the effective write set.

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

`.claude/settings.json` and `.claude/hooks/subagent_ghi_detect.py` are outside this set. A proven need to change either requires another revision and generation.

## Diagnoses and required implementation

The g11 full Windows registry on exact head `5dfb3ee79b4548c1ee4513bec89a74c5bd2fa59d` returned rc 1 after 9,088.3 wall seconds; log SHA256 `405911c9383ef5eb9613f5ad33fcd2ae341757f54c35d766e426a9e976d767fd`. The hook child had 43/45 base cases: t12 `unknown`, t21 0/4 with `bash: line 1: : command not found`; cleanup failed. Targeted t12 later passed 10/10, so the full-run cause is unknown. The original Windows Bash chooser selected WSL `C:\Windows\system32\bash.EXE`; selecting Git Bash absolute in a diagnostic produced t21 4/4 with the exact settings hook command. The fast mutant child timed out at 5,400 seconds; containment and cleanup were unconfirmed. Full registry remains failed until a fresh full positive receipt.

1. t12: retain fail-closed `unknown`. First expose exact hook `ly_do` and bounded safe diagnostic context on failure. Reproduce in full hook suite and loaded registry context; fix only the demonstrated cause. Require repeated targeted passes and all 45 base hook cases with unchanged mutation denominator.
2. t21: verify/select Git Bash absolute before Windows WSL Bash when launching the test. Retain exact hook command from `.claude/settings.json` and four environment/event combinations. Add a negative case for unusable or wrong Bash. Check actual Claude hook launch behavior; stop for revision if product hook/settings need changes.
3. Fast mutant test: preserve all 10 product and 239 self mutant names. Split work into bounded shards with exact source and head binding, complete membership, separate rc, start/end time, per-shard log and progress/heartbeat showing current mutant. Merge must reject missing, duplicate, stale or failed shards. Registry may delegate the heavy child only after verifying complete exact-head receipts; otherwise red. Existing 8-way CI shard/merge is a starting point. Raising a timeout or lowering a denominator does not satisfy this objective.
4. Measure on comparable Windows environment that the `ops/nhanh_don_duoc_test.py` critical path is at most 540 seconds, a tenfold reduction against the observed 5,400-second timeout lower bound. Record shard schedule, wall time, peak RAM, reruns and all 249 mutant identities. Parallelism is a hypothesis; if the 10x target fails, report failure and propose another revision rather than claiming acceptance.

## Preflight, gates and stop conditions

Before any Executor write: exact spec hash/ref, base/start head/tree, clean isolated clone, live full refs, unique holder on all twelve paths, valid g12 lease and expiry, provider/model/surface, and g11 tombstone readback. Preserve unrelated dirty worktrees. The dispatcher records heartbeat/progress; 30 minutes without progress requires revocation/generation bump under protocol §3.6.

On committed exact head, run targeted hook t12/t21 and full hook suite, complete fast-mutant shards/merge and 10x timing measurement, full Windows registry with positive per-child receipts and real rc, all r11 Windows symlink and full fast-path gates, lease-publish, doc receipt, G5, selftest, Ruff F delta zero, secret scan and diff check. Run heavy local suites serially unless bounded parallelism is itself the measured fast-mutant design. Do not cancel a registry run solely at an earlier elapsed ceiling when laptop sleep may have intervened; capture actual progress and rc. The prior full lease-publish rc 1 stays rc 1 despite separately passing t35–t40. Distinguish passed, failed, skipped, not_run, not_measured and inconclusive. Required full CI checks on exact pushed candidate and fresh independent read-only review with zero P1/P2 remain mandatory before any separate merge/land request. Changed head invalidates prior gate and review claims.

Stop on stale lease, ref/spec/head drift, holder overlap, provider mismatch, write outside twelve paths, weakened test or missing mutant, absent positive evidence, credential/LIVE/merge/deploy need, or repeated finding at protocol cap.
