# Independent review — WP748 r20/g20, PR #849

- Reviewer: OpenAI Codex; model family GPT-6 as identified by the agent runtime. Exact CLI model identifier has not been exposed; no more specific identifier is asserted.
- CLI: `codex-cli 0.163.0`; no model argument was exposed by the ancestor CLI process. Provider `openai_codex`, execution surface `codex_cli`, transport `machine` (local shell tools).
- Reviewed SHA: `9d471d90b959d98142373085e1a504ba1d9a58c3`
- Tree: `8a414308b2277af4548f44f23b96499505026e6a`
- Review started: 2026-10-19 18:06:12 UTC
- Review completed: 2026-10-19 18:17:00 UTC
- Status: complete; three P2 findings, changes requested. No P0/P1 findings or optional P3 findings.

## Identity verification

Ran `git -C src rev-parse HEAD HEAD^{tree} HEAD^1 HEAD^2` (rc 0). All four values exactly match the requested identity. Parent 1: `12430197e76dfb87c0e72796d0299b6faaa8b70b`; parent 2: `5618020a67709ca6f2c93138905df0aa8d9c2df6`.

`git -C src symbolic-ref -q HEAD` produced no branch, consistent with detached HEAD; `git -C src status --porcelain=v1` produced no changes. The checkout is clean.

`git -C src rev-list --parents -n 1 HEAD` confirmed exactly two parents. `git merge-base --is-ancestor` returned 0 for both the acceptance base `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9` and audited commit `a2a358ae6b8649f9e2869f7042c42abf1c98dfd4` against packet parent `12430197e76dfb87c0e72796d0299b6faaa8b70b`. Final HEAD/tree and clean-checkout checks again matched. The unmodified test clone is also clean; only the separate NaN mutant clone contains the two intentional one-line guard mutations. No credentials, remote API, commit, push, or GitHub comment was used.

## Findings

### WP748-R1 — P2 — Full audit is removed from the required CI path without an executable replacement

Location: `.github/workflows/ci.yml:970` (also `.github/workflows/ci-dot-bien-du.yml:13` and `.claude/dev/packet_loop.py:2390`).

Input → wrong output: a normal PR changes `ops/nhanh_don_duoc.py` or its tests. The new unconditional `CI_DANG_KY_DOT_BIEN_MANH` forces registry's plan to `nhe` even for that change; registry requires only the **targeted** shard aggregate. The full audit has only `schedule` and `workflow_dispatch` triggers. The checked-in mandatory-check set contains five `ci.yml` jobs and no full-audit job, and no new consumer requires full-audit success for the candidate SHA. Thus the existing required path can report success with the formerly required full mutant matrix never run on that candidate. The new comments say full audit is mandatory before merge/land/release, but comments do not enforce this obligation.

Evidence: `gate_contract_probe.py` evaluated the actual workflow contracts and registry planner: no fast-shard workflow errors; changed product file → `nhe`; full-audit triggers → schedule/dispatch only; checked-in required checks → only `ci.yml`. No live ruleset or external, packet-specific lease configuration was queried, so this finding is about the checked-in enforcement path, not a claim about an observed GitHub merge.

Suggested fix: before making registry unconditionally light, wire full-audit completion into an enforced acceptance/land check, bound to the exact candidate SHA and requiring explicit success; alternatively retain the previous full coverage on relevant changes. Preserve the targeted PR gate for speed if desired. Add regressions for absent, skipped, failed, stale-SHA, and targeted-only audit evidence, plus a valid full-audit control. Account for the long full-audit runtime when choosing the integration point; do not turn a skipped aggregate into acceptable evidence.

### WP748-R2 — P2 — New shard aggregate drops the required-group and minimum-group checks

Location: `ops/nhanh_don_duoc_test.py:5816` (partition construction at `:5541`).

Input → wrong output: supply otherwise valid shard receipts while the mandatory group set contains a group absent from the test/mutant tables, or falls below `SAN_NHOM`. Both new entry points, `gop_dich(..., du=False)` and `gop_dich(..., du=True)`, return **0**. The prior `gop()` returns **1** for the same invariant violations because `_loi_gop()` explicitly checks required-group coverage and the minimum count. The new `_muc_dich()` checks table consistency but never consults `NHOM_BAT_BUOC` or `SAN_NHOM`. The old self-tests still test the old aggregate/main paths, so they do not restore these checks in the new CI path.

Evidence: synthetic receipt validator controls passed with all three aggregators. Keeping the existing policy and all 52 cases, but omitting the mutant entries targeting required case `r549`, produced `{targeted: 0, full: 0, legacy: 1}`. Changing the in-memory required set to `original | {"r999"}` or `original - {"r549"}` produced the same result. These are validator fixtures, explicitly not claims of mutant execution. The current unmodified tables are complete; the regression is the loss of the guard against incomplete/relaxed tables.

Suggested fix: share the existing required-group coverage/floor validation across both old and new aggregate paths, and preferably reject an invalid table before launching shards. Extend the new aggregate's counterexamples to require rejection of a missing required case, a required case without a mutant, and a group count below the floor, with valid controls in both modes. Keep coverage validation separate from cost estimates so recalibrating shard weights cannot lower the required coverage.

### WP748-R3 — P2 — Windows cleanup still races on the process-identity ctypes signature

Location: `ops/lease_publish_test.py:4924` (call to `thu_hoi._khoa_danh_tinh(q)`; snapshot lock at `:4897`).

Input → wrong output: the two t125 timeout waiters enter `_giu_hau_due_windows()` concurrently. `_chup_cay()` is serialized by the new lock, but the subsequent held-handle identity recheck is outside that lock. `_khoa_danh_tinh()` in `.claude/dev/launcher.py:388` creates a fresh `_FILETIME` class and assigns its pointer types to the process-global `ctypes.windll.kernel32.GetProcessTimes.argtypes` on every call. Another identity recheck, or the other waiter's locked snapshot, can replace those types between assignment and invocation. Cleanup then raises `ctypes.ArgumentError` instead of completing, leaving the Windows gate intermittently red. This is the same shared-ctypes-signature race that the new snapshot lock addresses for `_PROCESSENTRY32W`, still reachable through the new call outside the lock.

Evidence: `windows_identity_race_probe.py` invoked the actual `_giu_hau_due_windows()` and actual launcher `_khoa_danh_tinh()` using harmless Win32 callback substitutes and real ctypes argument checking. Two serial controls held the expected descendant handles. Synchronizing two concurrent signature assignments produced one successful result and one `ArgumentError: expected LP__FILETIME instance instead of pointer to _FILETIME`. This is a deterministic Linux simulation of the race, not a claim of native Windows execution; no real process was terminated by this probe.

Suggested fix: protect **every** launcher identity call in this helper with the same lock as `_chup_cay()`, or eliminate shared mutable ctypes signatures in the launcher with a separately reviewed change. Add a concurrent identity-recheck regression alongside the snapshot-race test, with successful serial controls. Preserve the handle-identity checks and fail-closed errors; swallowing `ArgumentError` or treating an unmeasured descendant as exited would weaken the test.

## Read coverage and workflow review

Read every hunk of `git -C src diff 5618020a 9d471d9`: both work-packet adapters, `.claude/dev/ci_dang_ky_test.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`, `.claude/hooks/subagent_ghi_detect_test.py`, both requested workflows, and the three changed `ops/*_test.py` files. Also read `git -C src show 7a1740c8 12430197` in full. The two post-audit commits were independently reviewed and mutation-tested; no defect was found in their finite-number checks.

`git -C src diff 5618020a 9d471d9 -- ops/cong_cu_test.py ops/bash_nen.py` returned 0 with empty output, reconfirmed at completion. Read the dropped packet-side `cong_cu_test.py` changes and master's retained t23/t49 implementation, CA registration, related t63 check, and CI references. The discarded helper was nested inside t49; no dependency on it was found in the packet's surviving changes. Script entry points, G5 environment variables, eight-shard matrix, and aggregate CLI match master's retained implementation. Four focused G5 cases passed.

The `ci.yml` triggers remain push-to-master, pull_request, and workflow_dispatch, without new path filters. Existing required job names and OS selection remain unchanged: Ubuntu ordinarily; Ubuntu and Windows for dispatch or a PR bearing the Windows label when the workflow runs. New targeted shards use the same OS selection and eight shards, a 30-minute job timeout, and a 540-second measured shard-duration ceiling. The aggregate and registry use `!cancelled()`; registry explicitly rejects unsuccessful aggregate results. The full-audit workflow uses eight Ubuntu shards, 360-minute shard timeouts, and a 10-minute aggregate timeout. Its schedule/manual-only triggering and lack of enforced candidate audit are WP748-R1; its aggregate still relies on default dependency-success execution. Syntax validation passed; hosted execution semantics were not independently exercised.

Windows symlink, named-pipe, WSL selection, and process-handle branches were read. Their native Windows behavior was not measured. The adapter additions correctly label their historical targeted evidence as distinct from a full-suite run. This review does not adopt the earlier Human Audit for either post-audit commit or the merge head.

## Commands actually run

Environment: Linux, Python 3.13.16, actionlint 1.7.7, ShellCheck 0.9.0. Test copies were made with `mktemp -d` inside the workspace. Let `S` denote [review-wp748.6UhOaC](review-wp748.6UhOaC/); exact-head test working directory was `S/src`, and NaN mutation working directory was `S/nan-mutants`. Logs and actual process exit codes are saved in [S/logs](review-wp748.6UhOaC/logs/). The path is also recorded in `REVIEW_SCRATCH_PATH`.

All suite commands used `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1` and workspace-local `TMPDIR`. The isolated registry rerun, lease suite, fast-path suite, shards, and probes additionally used `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_TERMINAL_PROMPT=0`. Tests operated on copies, never the original `src/`.

| Command | rc | Observed result |
|---|---:|---|
| `actionlint .github/workflows/ci.yml .github/workflows/ci-dot-bien-du.yml` | 0 | Both workflows; no diagnostics |
| `git -C src diff --check 5618020a 9d471d9` | 0 | No whitespace errors |
| `python3 .claude/dev/ci_dang_ky_test.py` (initial, before Git isolation) | 1 | Existing temporary-fixture commit failed with Git rc 128; no successful full self-check claimed |
| Same registry command with isolated Git configuration | 0 | Registration 24/24; launcher contracts 4/4; Ruff contracts 3/3; counterexamples 1053/1053; `TỔNG: ĐẠT` |
| `python3 .claude/dev/doc_receipt_thu_hoi_test.py` | 0 | 156/156 cases; 162/162 mutants |
| `python3 .claude/hooks/subagent_ghi_detect_test.py` | 0 | 45/45 cases; 25/25 mutants; `TONG: DAT` |
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 python3 ops/nhanh_don_duoc_test.py` | 0 | Lightweight 8/8 |
| `python3 ops/lease_publish_test.py` | 0 | 265/265; skipped 0, including t217 missing-object case |
| `python3 ops/ci_duong_nhanh_test.py` | 1 | 103/104 cases; 0 assertion failures, 1 infrastructure error; 378/383 mutants; classification self-check passed |
| `NHANH_DON_DUOC_DICH=k/8 NHANH_DON_DUOC_DICH_RA=S/shards/manh-k.json python3 ops/nhanh_don_duoc_test.py`, each k=0..7 | All 0 | Shard item counts: 38/38, 40/40, 37/37, 37/37, 37/37, 38/38, 37/37, 37/37 |
| `python3 ops/nhanh_don_duoc_test.py --gop-dich S/shards` | 0 | 8/8 shards; 52/52 base cases; 239/239 targeted self-mutants; 10/10 product mutants; receipt self-check 35/35; exact reviewed SHA |

The targeted aggregate measured a longest shard duration of 64.37 seconds against 540 seconds, reported peak RAM 115.7 MB, and zero retries. This is Linux targeted evidence, **not** the full mutant audit or a Windows timing result. Remaining shards were orchestrated by `python3 S/run_remaining_shards.py S` (rc 0; up to three concurrent shard processes).

The fast-path suite's one infrastructure error and five affected mutants all reach `t20zo`, whose Unix socket bind is denied with `PermissionError: [Errno 1] Operation not permitted`. `python3 S/merge_and_socket_probe.py S/src` (rc 0 for its G5 assertions) passed both registered t23 cases, t49, and t63 (4/4), and separately reproduced the same t20zo bind failure using both head and master's test implementation. The fast-path suite remains **failed due to the environment**, not passed or skipped; no test was removed to obtain green.

## Mutation and counterexample evidence

- `python3 S/nan_probe.py S/src baseline`: rc 0; aggregate counterexamples 35/35, registry 1053/1053.
- `python3 S/nan_probe.py S/nan-mutants mutated`: rc 0 means both expected negative outcomes were observed. Only the finite-float conjunct in each new numeric guard was removed. Aggregate self-check fell to 31/35 (NaN time/RAM and infinite RAM escaped); registry returned false at 1051/1053 (NaN and positive infinity escaped). Integer and huge-integer controls continued to pass.
- In that mutant copy, `python3 .claude/dev/ci_dang_ky_test.py` returned **1**, with both newly escaping cases and `TỔNG: ĐỎ`. `python3 ops/nhanh_don_duoc_test.py --gop-dich S/shards` also returned **1**, failing its four escaping self-check counterexamples before reading candidate receipts. Thus both post-audit guards are protected by tests that actually go red.
- `python3 S/gate_contract_probe.py S/src S/synthetic-receipts`: rc 0; reproduced R1's actual configuration and R2's three invariant failures, with valid receipt controls. Synthetic receipts are validator inputs only and are kept separately from actual shard receipts.
- `python3 S/windows_identity_race_probe.py S/src`: rc 0; two serial controls passed; forced concurrent interleaving reproduced R3 with one ctypes `ArgumentError` and one successful held-handle result. This is simulation evidence with real ctypes type checking, not native Windows evidence.

## Not run / limitations

No native Windows execution, hosted Actions runs, live required-check/ruleset query, remote packet/lease readback, full 239-by-52 mutant audit, complete G5 suite, or registry `--chay` orchestration was run. No executor-reported result was counted as independent evidence. CLI version was measurable; the exact served model identifier was not exposed. The original checkout remains clean at the requested SHA/tree.

VERDICT: changes_requested
