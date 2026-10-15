# WP748 r10/g10 — Windows symlink and remaining gate closure

## Authority and exact candidate

- Packet/Mission #748. Owner revoked stale g9 and authorized revision 10 / generation 10 in Issue comment https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6184129511. G9 tombstone is on `ops/wp748-r9-g9-lease` commit `9b56cbc2d4c0c550dd384fb6632790a8b3c01ca7`. No g9 worker may commit, push or hand off under its revoked lease.
- Lease ID `wp748-r10-g10-claude-windows-20261015`. Immutable acceptance base `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. Start a fresh isolated Windows Executor clone on `agent/wp748-g10-claude` at exact continuation commit `0daeb47f31fef51d6242fc204c003b6431c6d465`, tree `18f72e6d6c3fe4d7222a18e8da8bf8ea1278c8d8`.
- The r8 and r9 specs remain the detailed original gate contracts. This revision keeps their acceptance, sensitive review class, and Windows named-pipe/socket exception. Its operational focus is diagnosing the interrupted Windows symlink gate and t125/t40 without weakening tests, timeouts, skips, or mutant denominator; and recording the validated Windows symlink lesson in the work-packet skills.
- The owner comment authorizes lease preparation and test execution. It grants no merge, land, LIVE or real-credential authority.

## Closed effective write set and roles

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

Executor: Claude Code, provider `anthropic_claude`, model `claude-opus-5-5`, surface `claude_code`, transport `machine/local`, Windows native. Dispatcher writes coordination metadata only. Reviewer: Codex/OpenAI in a fresh independent session, read-only on exact final Executor head. The Executor may not self-review, approve, merge, land, deploy, use LIVE or real credentials, or write outside these paths. Skill edits must describe validated operational behavior, not claim a test passed from an interrupted or earlier-head run.

## G9 diagnosis and preservation

- G9 product head is clean and pushed at `0daeb47f31fef51d6242fc204c003b6431c6d465`. Preserve g9 worktree and any unrelated untracked material until ownership is known. Do not silently cherry-pick or copy stale work.
- G9 `t20zk` log SHA256 `5c198da5da95b338ab297152d8f2d526fa301d9201d1a2ed9af3017177f78fb6` fails in `subprocess.Popen` starting fixture `git init`, before the symlink assertion: `WinError 1455` (paging file too small). It does not prove a symlink logic defect. `t20zm` and `t20zn` were not run. The partial ten-case loop has no complete positive receipt.
- G9 full lease-publish on the committed head returned rc 1, 240/252 passed with 13 platform skips; t125/t40 still require diagnosis. Targeted g8/g9 results are diagnostic only and transfer no gate credit.
- The controller's `gh` credential was invalid at r10 preparation; GitHub connector verified authority and exact remote refs. A credential/tool failure does not become an Executor or gate pass.

## Execution and acceptance

1. Before Executor write, recheck authoritative spec blob/SHA256 and commit, exact refs, base/head/tree, lease generation/expiry, eleven-path holder uniqueness, provider/model/surface and clean new clone. Record real progress. After 30 minutes without progress, revoke and bump generation under protocol §3.6. Lease lasts at most 12 hours from recorded start.
2. Have Claude reproduce each Windows symlink case with a separate command, real exit code and positive receipt: `t20n`, `t20x`, `t20zd`, `t20zf`, `t20q`, `t20zi`, `t20zj`, `t20zk`, `t20zm`, `t20zn`; also include related `t20zl` and `t20zo`. If `CreateProcess` again reports 1455, record environment failure, measure available memory/pagefile through an authorized mechanism and stop concurrent heavy gates. Do not weaken a fixture or mark a partial run passed. Fix only a demonstrated product/test defect inside the write set.
3. Record the validated Windows symlink lesson in both work-packet skill adapters: real file/directory symlinks and `target_is_directory`; Windows target-path behavior; separate rc/positive evidence for each `--mot-ca`; `WinError 1455` before assertion as environment failure; targeted 10/10 does not replace the full suite; Windows named-pipe/mock socket exception is separate from real symlink checks. Do not add an unmeasured claim.
4. Commit Executor edits with provenance in handoff. On exact committed head, rerun the ten symlink cases and full `python -B ops/ci_duong_nhanh_test.py` to rc 0, 104/104, 383/383 mutants and `TONG: DAT`. Run full `python -B ops/lease_publish_test.py` alone to rc 0, retaining t125/t191 950 s limit and reporting 13 platform skips separately. Targeted passes substitute for neither full suite.
5. On the same exact head, run doc receipt full suite 156/156 and 162/162 mutants, G5 `CONG_CU_TEST_BAN_KINH=manh` full suite, Windows registry full suite under 105 minutes with timing and positive markers and no cancelled `subagent_ghi_detect_test.py`, `python -B scripts/tl.py --selftest`, `git diff --check`, Ruff F delta 0 against immutable base, Linux regressions, and `scripts/pkg_secret_scan.py` on the exact write set. Run heavy suites serially. Report `passed`, `failed`, `skipped`, `not_run`, `not_measured`, `inconclusive` distinctly.
6. After local gates and clean handoff, push product branch and create a draft PR into `mission/748/integration`. Full CI matrix on exact candidate must show all required checks success, Windows/Ubuntu full selftest JSON and output SHA256 matching head/tree, Windows registry not cancelled, G5 and gate-ops Windows success. Fresh independent Codex review must find 0 P1/P2 on exact full SHA. Any head change invalidates review and gate claims. Separate exact-candidate authority is required before merge or land.

Stop for stale or missing lease, ref/head/base/spec/holder drift, provider mismatch, required write outside eleven paths, test weakening, memory-pressure kill, missing positive evidence, repeated finding at protocol cap, or any secret/LIVE/merge/deploy requirement. Preserve exact commands, exit codes, logs and hashes at each stop.
