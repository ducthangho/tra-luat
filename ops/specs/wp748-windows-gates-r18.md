# WP748 r18/g18 — repair registry discovery and finish Windows gates

## Authority, provenance and roles

Owner authorization: https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6243361863 (comment ID 6243361863, exact readback). This revision supersedes expired r17/g17. All r17/r16/r15/r14/r13/r12/r11/r9/r8 acceptance and stop conditions remain, including the two-level mutant gate. The g17 lease must be tombstoned on its source ref and bilaterally linked to g18 before any g18 Executor write. The separately approved three-hour inactivity protocol amendment is not yet effective; apply the current protocol until its governance change is landed and WP748 is revised again.

Immutable acceptance base: `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. The only continuation source is the clean, unpushed g17 product branch `agent/wp748-g17-claude` at commit `b643cfca250497964e2d920dddf6f8eccfb85fce`, tree `b0014831f1de884e49ab97ae1001ce90df4a384a`. Its twelve changed paths from the base equal the effective write set below. Transfer this exact committed source into a fresh isolated clone only after source/destination head, tree, diff, full live refs, holder and worktree checks; record provenance. No gate credit transfers to a changed head.

Executor: Claude Code Opus 5.5 (`anthropic_claude`, `claude_code`, local Windows), sole product writer on `agent/wp748-g18-claude`. Reviewer: fresh independent Codex session, read-only on exact final Executor head; Review Class sensitive and cross-provider assurance. Dispatcher writes only coordination metadata. No self-review, product push before readiness, merge, land, LIVE, deploy or real credentials.

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

Write-set hash (sorted NFC casefold exact paths, compact UTF-8 JSON): `e06292877ba0a66faab54c598f54d9e4845e4c6c41a47a52dc5fd94f850db46d`. `.claude/settings.json` and `.claude/hooks/subagent_ghi_detect.py` remain outside scope. A demonstrated need to edit either requires a new revision/generation.

## Required repair and regressions

On the g17 exact head, full G5 ended rc1: 103/104 baseline cases, with only `k01_so_dang_ky_nhan_muc_da_noi` red; 383/383 mutants were correctly killed. `.claude/dev/ci_dang_ky_test.py:tim(root)` traversed Git-ignored `.codex/hooks/*_test.py` mirror files and classified them as unknown locations. Repair registry discovery within the write set so ignored tool mirrors do not produce false failures, while tracked tests and non-ignored unknown test files still fail closed. Add focused positive and negative regressions. Do not remove or quarantine `.codex/` merely to make the gate green. No g17 G5 result may be claimed as passed.

Full g17 G3 registry ended rc1 under host memory pressure: `subagent_ghi_detect_test.py` failed when `git config gc.auto 0` could not start (Windows `0xC0000142`), and `nhanh_don_duoc_test.py` launch failed with the same status. Seven earlier registry children returned rc0. Preserve their individual receipts and rerun only failed or unmeasured children where composite evidence is allowed; full registry acceptance still requires positive per-child receipts and an actual full-suite rc0 when feasible. Do not call the g17 full G3 passed or cancel a long test solely for elapsed wall time.

Immediate g18 phase per owner direction on 2026-10-18: change only code needed for the red `k01` registry-discovery case and any demonstrated code defect in the two red G3 children. Re-measure those cases with real rc on one committed exact head, including negative tests that keep unknown non-ignored tests visible. An environment-only `0xC0000142` is not a code failure; if it recurs, record it as inconclusive and do not declare the red child fixed. Once all three red cases have positive receipts and no unresolved code red remains, freeze the head and prepare the Human Audit handoff. Human Audit is a separate owner checkpoint; its preparation does not satisfy the independent Codex review, full local gates, CI or mutant audit still required before push/merge/land. Do not run already completed g17 children again solely to fill time.

Historical g17 exact-head positive receipts: G6 full `lease_publish` rc0 (252/252 baseline; t125 A/B 252/252), twelve Windows symlink cases rc0 each, G7 doc receipt rc0, G8a `cong_cu.py kiem-tra --json` rc0, G8b `cong_cu_test.py --manh` rc0, and G9 `tl.py --selftest` rc0. The serial-chain `gates.txt` SHA256 is `99fc2e345166607af2251f51652d52d5963aa8667a8e2b8ceb2170b0dac34d44`. These receipts describe only `b643cfca250497964e2d920dddf6f8eccfb85fce`; rerun required gates on the new committed candidate head.

On the new exact committed head, measure the r17 two-level `targeted_mutant_gate` (52 baseline cases, 239 declared-target self mutants, 10 product mutants, merged membership and real rc), full hook/registry/fast-path/lease-publish suites, all twelve Windows symlink cases, doc receipt, `cong_cu` checks, selftest, Ruff F delta, secret scan and diff check. Keep `passed`, `failed`, `skipped`, `not_run`, `not_measured` and `inconclusive` separate. Required exact-head CI and fresh independent zero-P1/P2 Codex review remain mandatory. The full 239x52 mutant audit is separate and required before merge, land or release; the targeted gate cannot substitute for it. Preserve per-gate command, start/end, real rc, exact head/tree and bounded logs. Heavy local suites run serially unless the fast-mutant design itself measures bounded parallelism.

Product code may be pushed once per PR only after all fixes, complete local gates and independent zero-P1/P2 review. Exact-head CI follows that push. No merge, land or LIVE authority is granted by this Packet.

## Preflight and stop conditions

Before any g18 Executor write, verify this owner comment and spec/ref/hash, g17 source tombstone and g18 bilateral link, a fresh clean isolated clone/branch, exact source/base/head/tree and twelve-path diff, full live refs and unique holder on all twelve paths, valid g18 lease/expiry, provider/model/surface and required capabilities. Stop on mismatch, overlapping lease, stale generation, denied tool, need outside write set or missing positive evidence. Complete expensive read-only checks before lease publication; perform short final checks and start the sole Executor promptly. The current 30-minute no-progress rule and explicit `lease_until` both apply. Do not promote targeted, background or stale evidence to full pass.
