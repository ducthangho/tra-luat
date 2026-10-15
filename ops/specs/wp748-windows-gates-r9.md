# WP748 r9/g9 — Windows t154 closure and exact-head gates

## Authority and candidate

- Packet/Mission #748. Owner revoked stale g8 and authorized revision 9 / generation 9 in [Issue comment 6181964935](https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6181964935). The g8 tombstone is on `ops/wp748-r8-g8-lease` commit `d6cb9ab4e7ba16eedb0c5b4d35237acad7cdc58d`. No g8 worker may commit, push or hand off under its revoked lease.
- Lease ID `wp748-r9-g9-claude-windows-20261015`. Immutable acceptance base `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. Start a fresh isolated Windows Executor clone on `agent/wp748-g9-claude` at exact commit `61747138161e6b0adbbf6f9d76797d8c825de8df`, tree `c490e9e6cafaa1738ee792407a275773a27194fd`.
- The r8 spec `ops/specs/wp748-windows-gates-r8.md` remains the detailed gate contract. The r7 spec carries the original acceptance. This revision keeps the same nine-path write set, sensitive review class, socket exception and gate obligations. The only scope addition is diagnosis and closure of intermittent Windows t154 grandchild containment without weakening heartbeat proof, timeout or mutant denominator.
- The owner comment authorizes lease preparation and test execution. It grants no merge, land, LIVE or real-credential authority.

## Closed write set and roles

1. `ops/bash_nen.py`
2. `ops/cong_cu_test.py`
3. `ops/lease_publish_test.py`
4. `.claude/dev/ci_dang_ky_test.py`
5. `ops/nhanh_don_duoc_test.py`
6. `.github/workflows/ci.yml`
7. `.github/workflows/ci-dot-bien-du.yml`
8. `ops/ci_duong_nhanh_test.py`
9. `.claude/dev/doc_receipt_thu_hoi_test.py`

Executor: Claude Code, provider `anthropic_claude`, model `claude-opus-5-5`, surface `claude_code`, transport `machine/local`, Windows native. Dispatcher writes coordination metadata only. Reviewer: Codex/OpenAI in a fresh independent session, read-only on exact final Executor head. The Executor may not self-review, approve, merge, land, deploy, use LIVE or real credentials, or write outside these paths.

## G8 source and preservation

- G8 worktree `D:\Quốc hội\tra-luat\work\wp748-g5-claude` remains dirty and stale. Its only tracked diff is an uncommitted Claude patch to `ops/lease_publish_test.py`. Binary diff SHA256 `e6c987ea419a5f0167ca66d36aaad00f07526feeaec5a765189bb07b11231db6`, from g8 HEAD `61747138161e6b0adbbf6f9d76797d8c825de8df`, Claude Opus 5.5 launcher runs `26ef8dba` and `d0d96dc4`. The dispatcher may present this exact patch to the new Executor only after `git apply --check` in the fresh clone and recording provenance. Do not silently cherry-pick it.
- Preserve the five unrelated untracked `.agents/skills/` directories in the g8 worktree; their ownership is unknown. Do not copy them into g9 or delete them.
- G8 symlink targeted 10/10 and prepatch full lease-publish 252/252 with 13 platform skips were diagnostic only. Isolated t154 failed once after that full run: `taskkill` returned 0 while grandchild heartbeat advanced from 4 to 5; a retry passed. G8 uncommitted patch passed targeted t154 6/6 twice and two counterprobes failed as intended. Full suites, CI and independent review were not measured after the patch. None of these results counts as a g9 gate pass.

## Execution and acceptance

1. Before Executor write, recheck exact refs, base/head/tree, spec commit and SHA256, lease generation/expiry, nine-path holder uniqueness, provider/model/surface, and clean new clone. Record real progress. After 30 minutes without progress, revoke and bump generation under protocol §3.6. The lease lasts at most 12 hours from recorded start.
2. Have Claude diagnose the t154 intermittent grandchild failure. Preserve positive evidence that the grandchild was alive before cleanup, exited after cleanup, and its heartbeat stopped; preserve the existing timeout and mutant denominator. Run t154 and its relevant counterprobes before full suites. A test-only repair must still prove real Windows containment behavior.
3. Commit the Executor patch with source provenance in the message/handoff. On exact committed head, rerun the ten symlink cases **and** full `python -B ops/ci_duong_nhanh_test.py` to rc 0, 104/104, 383/383 mutants and `TONG: DAT`. Run full `python -B ops/lease_publish_test.py` alone to rc 0, retaining t125/t191 950 s limit and reporting 13 platform skips separately. A targeted pass does not substitute for either full suite.
4. On the same exact head, run doc receipt full suite 156/156 and 162/162 mutants, G5 `CONG_CU_TEST_BAN_KINH=manh` full suite, Windows registry full suite under 105 minutes with timing and positive markers and no cancelled `subagent_ghi_detect_test.py`, `python -B scripts/tl.py --selftest`, `git diff --check`, Ruff F delta 0 against immutable base, Linux regressions, and `scripts/pkg_secret_scan.py` on the exact write set. Run heavy suites serially to reduce memory pressure; do not disable Claude protection or weaken tests. Report `passed`, `failed`, `skipped`, `not_run`, `not_measured`, and `inconclusive` distinctly.
5. Only after local gates and a clean handoff, push the product branch and create a **draft PR** into `mission/748/integration`. Full CI matrix on exact candidate must show all required checks success, Windows/Ubuntu full selftest JSON and output SHA256 matching head/tree, Windows registry not cancelled, G5 and gate-ops Windows success. Fresh independent Codex review must find 0 P1/P2 on exact full SHA. Any head change invalidates review and gate claims. Separate exact-candidate authority is required before merge or land.

Stop for stale or missing lease, ref/head/base/spec/holder drift, provider mismatch, required write outside nine paths, test weakening, memory-pressure kill, missing positive evidence, repeated finding at protocol cap, or any secret/LIVE/merge/deploy requirement. Preserve exact commands, exit codes, logs and hashes at each stop.
