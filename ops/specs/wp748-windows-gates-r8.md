# WP748 r8/g8 — serial Windows gate measurement after g7 resource failure

## Authority and exact candidate

- Packet/Mission #748. Owner revoked g7 and authorized r8/g8 in [Issue comment 6173521545](https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6173521545). This grants a successor Executor lease only after the lease file, gate and holder scan pass. It grants no merge, land, LIVE or real-credential authority.
- Revision 8, generation 8, lease ID `wp748-r8-g8-claude-windows-20261014`. G7 lease `wp748-r7-g7-claude-windows-20261014` was tombstoned on `ops/wp748-r7-g7-lease` commit `c0cb86e1d07b4a45fff40dd0819397570d78e234` after >30 minutes without gate progress under protocol §3.6. G7 Executor process exited. Do not revive g7, push its branch, or reuse its review/gate status as g8 status.
- Immutable acceptance base `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. Start g8 branch `agent/wp748-g8-claude` from exact g7 product commit `61747138161e6b0adbbf6f9d76797d8c825de8df`, tree `c490e9e6cafaa1738ee792407a275773a27194fd`; this commit is clean and changes only `ops/ci_duong_nhanh_test.py`. Its message records the uncommitted g6 diagnostic patch source SHA256 `8575738e7121ce7aecb1b6de26b40a72ab409971ce3ad5821f430a61c0eb625f` and the user-approved Windows socket test limitation. No cherry-pick or silent gate transfer.
- R7 spec `ops/specs/wp748-windows-gates-r7.md` at commit `cc2147ff63b668e76e3951ef1926b3ac017f4819`, SHA256 `a35af7165c33b7661b696dd13eedb40266c2cdbaa56e0ba43a1679d0c7b5bd3d`, remains the detailed acceptance contract. This r8 spec carries its nine-path write set, risk `sensitive`, review class, and all acceptance unchanged except the operational sequencing and g8 identity here. The narrow Windows socket exception remains exactly as authorized in Issue comment 6171400658: real named pipe for path/t82; scoped `os.stat` mock only for the socket leaf on Windows; Linux uses real FIFO/socket.

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

Executor is Claude Code on Windows native, provider `anthropic_claude`, model `claude-opus-5-5`, surface `claude_code`, transport `machine/local`, in the trusted independent clone `D:\Quốc hội\tra-luat\work\wp748-g5-claude` after branch switch and exact-state preflight. Reviewer is Codex/OpenAI in a fresh independent session, read-only on exact Executor head. Dispatcher may write only coordination metadata. No self-review, approval, push/PR before local gates, merge, land, deploy, LIVE or real credentials.

## G7 incident to preserve as evidence, not g8 gate credit

- `python -B ops/ci_duong_nhanh_test.py` on g7 product commit: rc 0, 104/104 cases, 383/383 mutants, `TONG: DAT`; log SHA256 `d3d88041dd269f5a705b61f469b12edf1c4c88cb0a1e4b73169e2ac15bb7a1c6`. Ten targeted symlink cases had passed before that commit; g8 must prove symlinks on its own exact head and full suite separately.
- Doc receipt on g7 product commit: rc 0, 156/156 cases, 162/162 mutants, unresolved 0; log SHA256 `56d5402d5e3aecb7c5d8944ba93fb54ce221a7a82adb2cb57f753d05f5e0c0d9`. Ruff F delta 0 with local ruff 0.15.20; `git diff --check` rc 0.
- Lease-publish full suite on g7: rc 1, 251/252, 13 platform skips because `ops-publish-lease.yml` runs Ubuntu only. `t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor` timed out its child at 950 s while the child was in `t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG`, alongside other heavy suites. A second full run alone was killed by Claude Code memory pressure after t34 and before t35; it is `not_measured`, not pass. RAM free on a 7.63 GB host was 0.73 GB after the kill and 1.38 GB near the g7 no-progress boundary. Do not disable Claude Code pressure protection as a shortcut.
- Registry Windows, G5 strong radius, selftest, Linux regressions, secret scan, CI and review were not run on the g7 product commit. There is no PR, merge or land.

## R8 acceptance and execution order

1. Before any Executor action, verify current refs, exact base/head/tree, this spec SHA256 and commit, lease ID/generation/expiry, nine-path holder uniqueness, provider/surface/model and clean worktree. Stop on drift. Record real heartbeat/progress; after 30 minutes without progress revoke and bump generation under protocol §3.6.
2. Measure available Windows RAM before heavy suites. Aim for at least 2 GB free; run only one heavy suite at a time. If memory is insufficient, stop the dependent gate and record `not_measured`; do not increase timeout, weaken the test, disable pressure protection or claim a partial run as pass.
3. On the exact committed g8 head, re-run the 10 symlink cases **and** full `python -B ops/ci_duong_nhanh_test.py` to rc 0, 104/104, 383/383, `TONG: DAT`. Re-run full lease-publish alone to rc 0, preserving t125/t191 950 s limit and 13 platform skips separately. If it fails again, diagnose within the closed write set and re-run every affected gate on a new exact commit. Do not change test meaning outside the Windows socket exception.
4. Re-run doc receipt full suite 156/156 and 162/162 mutants, G5 `CONG_CU_TEST_BAN_KINH=manh` full suite, Windows registry full suite under 105 minutes with timing/positive markers and no cancelled `subagent_ghi_detect_test.py`, `python -B scripts/tl.py --selftest`, `git diff --check`, Ruff F delta 0 against immutable base, Linux regressions, and `scripts/pkg_secret_scan.py` on the exact write set. Distinguish `passed`, `failed`, `skipped`, `not_run`, `not_measured` and `inconclusive`.
5. After local gates and clean handoff only, push g8 product branch and create a **draft PR** into `mission/748/integration`. Full CI matrix on the exact candidate must have all required checks success, Windows/Ubuntu full selftest JSON and output SHA256 matching head/tree, Windows registry not cancelled, G5 and gate-ops Windows success. Independent Codex review in a fresh session must report 0 P1/P2 on exact full SHA. Any head change invalidates prior review/CI claims. No merge/land/LIVE or real credentials.

## Stop conditions

Stop for stale/missing lease, ref/head/base/spec/holder drift, provider mismatch, need to write outside the nine paths, memory-pressure kill, test semantic change beyond the owner exception, missing positive gate evidence, repeated finding at the protocol cap, or any secret/LIVE/merge/deploy requirement. Preserve logs and exact command/rc/hash at every stop.
