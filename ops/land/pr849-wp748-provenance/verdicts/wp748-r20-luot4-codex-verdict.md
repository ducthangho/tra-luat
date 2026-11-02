# Independent read-only re-review — WP748 r20/g20, PR #849, round 4

- Reviewer: OpenAI Codex, GPT-6 family as identified by the runtime; exact served model identifier is not exposed. Provider `openai_codex`; execution surface hosted Codex shell tools (`codex_service` in the repository taxonomy); transport `machine`.
- Review started (UTC): 2026-10-19T23:48:10Z.
- Reviewed SHA: `3818bd4a9685e1782afdd7e8a593482f74b663ff`.
- Reviewed tree: `b5d32c370207b8f8a35bdc15c591b9947dc5ae92`.
- Sole parent: `99836157fdffe2681280a8302c8c7396ac5fe4de` (round-3 approved head).
- Local `origin/master`: `94220547cd155c73392e95726e8daf353888b3aa`; tree `e57968d536a0bfd19c868e70fa88392974398073`; parents `b27fe85c9e9593ddbb059808fe4347fe1bd267be` and the reviewed head.
- Scope/authority: user's independent read-only final-head review; no source edits, commits, pushes, GitHub comments, or credentials. Scratch and evidence remain outside `src/`, under `review-r4.RBq39u/`.
- Prior record: read `VERDICT_LUOT3.md`. Its approved disposition includes an explicitly unresolved, previously escalated full-audit-enforcement obligation; this review will not relabel that obligation closed.

## Incremental evidence

- `git -C src status --porcelain=v1` — rc 0; initially empty.
- `git -C src rev-parse HEAD 'HEAD^{tree}' HEAD^ origin/master 'origin/master^{tree}'` — rc 0; identities above.
- `git -C src rev-list --parents -n 1 HEAD` — rc 0; exactly the required single parent.
- `git -C src diff --stat 9983615 3818bd4` and full `diff` — rc 0; exactly two files, four insertions/two deletions. Workflow: two comments plus `gate-cong-cu` timeout 45 → 150. Test: matching scalar in `KHUNG_JOB`.
- `git -C src diff 3818bd4 origin/master --stat` — rc 0; only `.claude/dev/packet_loop_test.py`, 717 insertions/20 deletions.
- `command -v actionlint` — rc 0; `/root/.local/bin/actionlint`.

The entries below were appended incrementally; the completed findings and verdict appear at the end.

- `python3 review-r4.RBq39u/run_logged.py before . python3 review-r4.RBq39u/snapshot.py src review-r4.RBq39u/before.json` — rc 0; captured 4,645 tracked file-content hashes/modes, clean tracked/untracked/ignored status, empty worktree/index diffs, and detached HEAD (`symbolic-ref -q HEAD` rc 1, expected).
- In `src/`: `actionlint .github/workflows/ci.yml` — rc **0**, no diagnostics.
- In `src/`: `PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py` — started; outcome pending. The logging wrapper also disables bytecode writes, confines temporary files to scratch, disables Git prompts/optional locks, and uses empty global/system Git configuration. All subprocess outputs and actual return codes are retained under `review-r4.RBq39u/logs/`.

## Merge equivalence and delta audit

`python3 review-r4.RBq39u/audit.py`, run through the logging wrapper — final rc **0** (`logs/audit-final.json`). Git subcommands and return codes are retained in `logs/audit-git-receipts.json`.

- Merge first parent `b27fe85c9e9593ddbb059808fe4347fe1bd267be` is locally recorded as “Merge pull request #851”; its first parent/common base is `5618020a67709ca6f2c93138905df0aa8d9c2df6`.
- Relative to that common base, PR #849 has exactly **10** modified paths. All **10/10** have identical Git blob OIDs and bytes in the reviewed head, merge `94220547cd155c73392e95726e8daf353888b3aa`, and current checkout:

| PR path | Identical blob OID in head and merge |
|---|---|
| `.agents/skills/work-packet/SKILL.md` | `e5abe03c11e3e6aa30969f7e89fc3b4c874f699c` |
| `.claude/dev/ci_dang_ky_test.py` | `733bdbfadc809e3274df8e313d6454bc058ba3d9` |
| `.claude/dev/doc_receipt_thu_hoi_test.py` | `f5891a6217ff2a3b5fb751094414d326809a7985` |
| `.claude/hooks/subagent_ghi_detect_test.py` | `3b34358e92efc33aa081c6cb41b5cca92621405f` |
| `.claude/skills/work-packet/SKILL.md` | `1f4c73e50cfd7336aec43f0eb90c37190b99131a` |
| `.github/workflows/ci-dot-bien-du.yml` | `686a1e90b8e3256d122cd13d524fe3d323cfe404` |
| `.github/workflows/ci.yml` | `55d06ab452a060b836fdf6fa45ba3408fc44c90c` |
| `ops/ci_duong_nhanh_test.py` | `916d4937bf33b357c9fe16f700ab35c682e68a1a` |
| `ops/lease_publish_test.py` | `eebb240c42cc74c735a0de11a9cf55022f980297` |
| `ops/nhanh_don_duoc_test.py` | `a162e0d26b262794b080c1624b43f3bb986b483b` |

The sole head-to-merge difference, `.claude/dev/packet_loop_test.py`, is also byte-identical to PR #851's merged first-parent version. Thus this verdict covers the PR #849 bytes that landed, without claiming a review of PR #851's changes.

Independent YAML parsing and full-object comparison find exactly one semantic change: `.github/workflows/ci.yml:507`, `jobs.gate-cong-cu.timeout-minutes`, **45 → 150**. Every other job/step timeout, trigger, job/check name, dependency, condition, matrix, environment, and command remains identical. No other file is changed by this commit beyond the companion snapshot. No repository-side required-check definition or context is changed; hosted ruleset state was not queried.

At `ops/ci_duong_nhanh_test.py:2289`, restoring this single AST constant to 45 makes the entire test AST identical to the parent. Case registration, mutation targets, execution, and verdict conditions are unchanged. The exact topology comparison at `:2455` still runs and asserts the job/step configuration.

- Current topology positive control: **1/1** passes.
- Old snapshot (45) against the new workflow (150): fails specifically on `gate-cong-cu`'s timeout, establishing why the snapshot update is necessary.
- **9/9** independent negative controls rejected by `TinHieuChotCa`: old snapshot, reverted timeout, timeout 151, another job timeout changed, gate deleted, job always skipped, empty shard matrix, step always skipped, and removed pull-request trigger. No infrastructure error is counted as a rejection.
- `git -C src diff --check 99836157fdffe2681280a8302c8c7396ac5fe4de 3818bd4a9685e1782afdd7e8a593482f74b663ff` — rc **0**.

Probe transparency: the first reviewer-only audit attempt exited **1** after eight successful negative controls because the probe indexed PyYAML's unquoted `on` key as a string instead of its boolean key `True`. Corrected only the scratch probe, retained the initial `logs/audit.*` evidence, and reran successfully as `audit-final`. This was a reviewer probe error, not a source failure; the separate independent YAML comparison uses `BaseLoader`.

## Prior findings: closure rechecked

`python3 review-r4.RBq39u/closure_probe.py` — rc **0**, measured on Linux / Python **3.13.16**. Only in-memory copies of helper functions were mutated. Positive and negative controls are in `logs/closure.stdout`; stderr contains two pre-existing invalid-escape `SyntaxWarning`s in the unchanged lease test file, not failures.

| Finding / location | Original failure scenario and retained fix | Current evidence |
|---|---|---|
| R2 `mandatory-group-validation`: `ops/nhanh_don_duoc_test.py:5512`, callers `:5508` and `:5873` | Consistent-looking shard receipts could hide missing mandatory cases, absent mutant coverage, or a below-floor mandatory set. Both aggregation paths now call shared `_loi_nhom_bat_buoc`. | **Closed.** **53/53** required groups covered; **43/43** aggregate controls pass, including **3** valid controls. Deleting the shared guard in memory causes exactly **6/6** malformed-table counterexamples to escape, covering targeted/full modes. |
| R3 `shared-ctypes-signature-race`: `ops/lease_publish_test.py:4927`, regression `:13140` | Concurrent waiters could overwrite shared ctypes function signatures while `_khoa_danh_tinh` ran outside the snapshot lock. Both launcher calls now hold `_KHOA_CHUP_CAY_WINDOWS`. | **Closed.** `t220` passes **1/1** with a valid descendant retained; removing either lock independently is rejected **2/2** by the intended case assertion. |
| Connector P2 `ram-pmc-truncated-layout`: `ops/nhanh_don_duoc_test.py:5668`, regression `:4082` | Windows no-job RAM fallback supplied seven SIZE_T fields, so the process-memory call could fail. `_PMC` now has `peak_ws` plus seven trailing SIZE_T fields, eight total. | **Closed.** `r553` positive controls pass **2/2** with native host and Windows-width DWORDs, returning 512 MB. Restoring seven total SIZE_T fields is rejected **2/2** by the intended assertion. |

The full `ops/nhanh_don_duoc_test.py` is byte-identical to round-3 approved `99836157fdffe2681280a8302c8c7396ac5fe4de`; the full `ops/lease_publish_test.py` is byte-identical to round-2 fixed `1e5522383433d1c544ec89585c9ef874aed0138e`. No additional fix is requested for these three findings.

The Windows probes simulate API behavior on Linux; they do not claim native Windows concurrency or native Windows API execution. Prior round-1/2/3 records are available here through `VERDICT_LUOT3.md`; no missing earlier verdict file was assumed read. That record explicitly leaves R1 `full-audit-enforcement` **escalated / unresolved**, with an inherited approval disposition. This delta neither changes that obligation nor establishes external enforcement.

## Completed requested test run and environment blocker

All commands below used the unchanged reviewed checkout unless a scratch path is specified. `S` means `review-r4.RBq39u`; each test/probe command was invoked by `python3 S/run_logged.py <label> <cwd> <command...>`. Its JSON receipt retains actual rc, command, working directory, UTC start, duration, and stdout/stderr paths.

| Command | rc | Measured result |
|---|---:|---|
| In `src/`: `actionlint .github/workflows/ci.yml` | **0** | Passed; actionlint **1.7.7**, no diagnostics |
| In `src/`: `PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py` | **1** | **103/104** cases passed; **0** assertion failures, **1** infrastructure error. **378/383** mutants killed for the intended reason; **5** blocked by a failing baseline fixture. Total: **DO**. Duration **128.068 s**. |
| Same suite's classifier self-check | Included in rc 1 above | **5/5** rc samples and **3/3** actual mutation classification controls passed (`TU KIEM PHAN HANG: DAT`) |
| `python3 S/audit.py` (corrected probe) | **0** | **10/10** PR files byte-identical in merge; **1/1** topology positive control; **9/9** negative controls rejected |
| `python3 S/closure_probe.py` | **0** | R2 **43/43** controls; R3 **1/1** positive and **2/2** negative controls; PMC **2/2** positive and **2/2** negative controls |
| `python3 S/unix_socket_probe.py` | **1** | Standalone `AF_UNIX` stream-socket `bind("review.sock")` denied with `PermissionError: [Errno 1] Operation not permitted` |
| In `S/parent-9983615/`: `PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py --mot-ca t20zo_la_khong_phai_tep_thuong_do` | **4** | Same socket denial on the approved parent, from a `git archive` copy; infrastructure error, not a case-assertion failure |
| `python3 S/snapshot.py src S/after.json` | **0** | Same identity, detached state, clean checkout, and file hashes |
| `cmp S/before.json S/after.json` | **0** | **4,645/4,645** tracked file contents/modes unchanged; status and worktree/index diffs unchanged |

**Blocker B1 — local execution capability, no source severity assigned.** Location: `ops/ci_duong_nhanh_test.py:1702`, `_tao_socket`, reached by `t20zo_la_khong_phai_tep_thuong_do` at `:1779`. Scenario: the fixture creates a Unix-domain socket to test rejection of a non-regular file; this sandbox denies `socket.bind`. A standalone probe reproduces the denial, and the exact approved parent case fails identically. This is independent of the timeout/snapshot change.

The five affected mutants are `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, and `la_khong_theo_symlink`. Each is reported **HONG** because its original target case cannot establish a green baseline. They are **not** counted as killed, survived, or passed. Cross-checking the real suite output against its mutation table confirms **74/74 workflow-targeting mutants** were killed correctly; all five blocked mutants target the unchanged `ops/ci_duong_nhanh.py`. The YAML case category also completed **16/16**; the sole failed case is in the behavior category.

**Remediation:** rerun the unchanged requested full command at SHA `3818bd4a9685e1782afdd7e8a593482f74b663ff` in an execution environment that permits local Unix-domain socket binding, and record complete case/mutant counts (expected suite totals: 104 cases, 383 mutants). No source change, skipped case, fabricated socket, or weakened assertion is proposed. This session's execution policy does not permit privilege escalation. No attempt was made to bypass it.

## Findings P0–P3 and final disposition

**No new P0, P1, P2, or P3 code finding in the reviewed delta.** The timeout change is isolated, the snapshot is the sole required code companion, and the non-vacuity checks remain effective. No gate is removed or made always-skipped by this commit. The three named prior code findings remain closed, with the scenario/fix/evidence recorded above. The inherited R1 external-enforcement escalation remains unresolved as explicitly recorded in round 3; no new enforcement claim is made here.

The verdict is **blocked**, solely because the required full local regression run cannot produce complete passing evidence in this sandbox. The repository's `AGENTS.md` evidence rule says unmeasured results are not passes; the missing **1** case and **5** mutant measurements are therefore not waived. This is not a request for a code fix.

Not run: native Windows execution, hosted CI reruns, remote required-check/ruleset inspection, or a new full audit of all 240 `nhanh_don_duoc_test.py` self-mutants. No credentials, network calls, source edits, reviewed-repository commits/pushes, or GitHub comments were used. Temporary fixture repositories created by the requested suite stayed in the reviewer scratch area.

Review completed (UTC): **2026-10-19T23:53:41Z**. Final reviewed identity remains SHA `3818bd4a9685e1782afdd7e8a593482f74b663ff`, tree `b5d32c370207b8f8a35bdc15c591b9947dc5ae92`, sole parent `99836157fdffe2681280a8302c8c7396ac5fe4de`. Exact merge coverage remains **10/10** PR files in `94220547cd155c73392e95726e8daf353888b3aa`.

VERDICT: blocked
