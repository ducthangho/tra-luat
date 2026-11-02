# WP748 r26 — round 10 independent review of final merge head

**Disposition: approve. Open: 0 P0, 0 P1, 0 P2, 0 P3.** Started UTC: 2026-10-25 16:02:39 UTC.

Reviewer: OpenAI Codex, GPT-6-based agent, as identified by runtime/developer instructions; provider `openai_codex`, observed surface tool-mediated local shell, transport `machine`. Exact serving model/build, enclosing launcher invocation and execution receipt are not independently visible. The user reports `launcher.py run`; that report is not a verified receipt. Review Class: sensitive. No GitHub access or credentials will be used.

Identity verified before review: full (non-shallow), clean, detached clone at SHA `0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f`, tree `ba9106b45cc0045b5bd0f56a7f465be771ccf6dc`. Parent 1 `3877d463c0d9b7a0757d051d547c824814601370`; parent 2 and local `origin/master` `cdc4e80bc439fa974775f319dccac5bf2fc955fe`. Local branch `agent/wp748-r26-claude` points to HEAD. Local remote-tracking refs also point at HEAD; they are clone-local data and do not prove the live pushed/unpushed state. The supplied LOCAL/UNPUSHED state cannot be independently verified without the prohibited remote access.

Initial identity commands and real outputs:

```text
$ git -C src rev-parse --show-toplevel --is-shallow-repository HEAD 'HEAD^{tree}' 'HEAD^1' 'HEAD^2' refs/remotes/origin/master
/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r26j/src
false
0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
ba9106b45cc0045b5bd0f56a7f465be771ccf6dc
3877d463c0d9b7a0757d051d547c824814601370
cdc4e80bc439fa974775f319dccac5bf2fc955fe
cdc4e80bc439fa974775f319dccac5bf2fc955fe
[rc 0]
$ git -C src status --short --branch
## HEAD (no branch)
[rc 0]
$ git -C src symbolic-ref -q HEAD
[empty output; rc 1, expected for detached HEAD]
$ git -C src for-each-ref --format='%(refname) %(objectname)' --points-at HEAD
refs/heads/agent/wp748-r26-claude 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
refs/remotes/origin/HEAD 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
refs/remotes/origin/agent/wp748-r26-claude 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
[rc 0]
```

Evidence scratch: `review-r26j-HjiNZnsS/`. Reviewed source remains read-only; bytecode writes will be disabled, fixtures and mutation copies kept outside `src`. No subagents are used. Round-9 findings are closure context only; round-10 execution will be fresh.

## Merge, spec and size verification

```text
$ git -C src diff 3877d463c0d9b7a0757d051d547c824814601370 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f -- .claude/dev/
[empty output]
[rc 0]
```

```text
$ git -C src diff --name-only cdc4e80bc439fa974775f319dccac5bf2fc955fe 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
.claude/dev/launcher.py
.claude/dev/launcher_test.py
[rc 0]
```

```text
$ git -C src diff --numstat cdc4e80bc439fa974775f319dccac5bf2fc955fe 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
183	68	.claude/dev/launcher.py
1007	35	.claude/dev/launcher_test.py
[rc 0]
```

```text
$ git -C src merge-base --is-ancestor cdc4e80bc439fa974775f319dccac5bf2fc955fe 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
[empty output]
[rc 0]
```

The merge preserves the entire `.claude/dev/` tree relative to parent 1, and master is an ancestor. The full delta against parent 2 is exactly the two authorized packet files: **1,190 added / 103 deleted lines**, below the user-supplied **1,300 added-line cap** (110 lines remaining). This invocation is **10/10** according to the user; no additional model call or subagent has been made. The owner authority at #748 issuecomment-6399648861 and the historical call count **cannot be read or independently verified on GitHub** under this review’s restrictions. Those supplied limits supersede the older numeric limits in the checked-in spec/lease.

`git -C src show origin/ops/wp748-r25-g25-lease:ops/specs/wp748-r25-launcher-model-phuc-vu-v2.md` returned rc 0. SHA-256 of the returned spec bytes is **`f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb`**, matching the required value. Full output is in `review-r26j-HjiNZnsS/logs/spec.json`; a readable copy is `spec-v2.md`. The local r26/g26 lease (same ref, `ops/leases/wp748-r26-g26-claude-remote-20261025.yaml`, rc 0) permits review of later local heads, offline before push/gates, and records expiry `2026-10-26T06:48:19Z`. Live authority, revocation/holder state and outer execution receipt remain unverified.

Master-side diff from parent 1 contains **76 paths: 2 docs + 74 `ops/land/` evidence files**. Exact `git diff --name-only` command/output (rc 0) is retained in `logs/master-side-paths.json` and `master-side-paths.txt`. The protocol diff only updates the ADR routing table; ADR-0055 changes the declared review-call cap. The ops additions are evidence/scripts under two land archives; neither launcher nor tests execute those archives.

```text
$ rg -n -F -f /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r26j/review-r26j-HjiNZnsS/master-side-paths.txt src/.claude/dev/launcher.py src/.claude/dev/launcher_test.py src/.claude/dev/codex_cred.py src/.claude/dev/codex_env_policy.py
[empty output]
[rc 1]
```

```text
$ rg -n 'PROTOCOL_DA_PHIEN|0055-tran-loi|pr924-wp923|pr926-wp919|ops/land' src/.claude/dev/launcher.py src/.claude/dev/launcher_test.py src/.claude/dev/codex_cred.py src/.claude/dev/codex_env_policy.py
[empty output]
[rc 1]
```

```text
$ git -C src diff 3877d463c0d9b7a0757d051d547c824814601370 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f -- .claude/dev/codex_cred.py .claude/dev/codex_env_policy.py .claude/hooks/session-start.sh .claude/hooks/session_start.py .claude/settings.json ops/bash_nen.py ops/cong_cu.yaml ops/cong_cu.py ops/cai_cong_cu.sh ops/cai_actionlint.sh scripts/tl_selftest.py requirements.txt .github/coordination/review_receipt.v2.schema.json
[empty output]
[rc 0]
```

The `rg` rc 1 results mean **no matches**, not a failed execution. The broader import/path/read/glob census (`logs/imports-readpaths.json`, rc 0) was inspected: companion Python modules, hooks, tool-install helpers/config, requirements and schema paths remain unchanged. Reads of `/proc`, caller-selected inputs/workspaces, temporary fixtures, run directories and credential guards do not select the new docs/land artifacts. The six regression-boundary definitions `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, `KetGiet` are AST-identical to master. Overall `merge_audit.py` returned **rc 0, MERGE AUDIT PASS**.

Fresh execution uses Python with bytecode writes disabled, a minimal explicitly constructed environment with no credential variables, disabled system/global Git config, and a verified nonexistent fixture HOME at a unique root-level path. No root-level directory is created. All temporary repositories and mutation files are outside `src`; existing test helpers create fixture commits only in those disposable repositories. No source commit is made.

## Fresh measurements on the final merge SHA

`python3 -B review-r26j-HjiNZnsS/review.py targeted` returned **rc 0** and `targeted: 38/38`. It enumerated the required functions both from the AST and the registered `CA` list (same set), then ran **every one of the 38** with `python3 src/.claude/dev/launcher_test.py --lap-ca <full-name> --lan 1`. Every subprocess returned **rc 0** and positive **`1/1 qua, 0 bo qua, 0 hong`**; none skipped. Commands, stdout, stderr, UTC and duration for every case are preserved in `targeted.json` and `logs/case-00.json` through `logs/case-37.json`.

```text
$ python3 src/.claude/dev/launcher_test.py --lap-ca r926_dot_bien_tu_sinh_moi_thanh_phan_regex --lan 1
moi truong: pid=3819 pgid=1 sid=1 truong_nhom=False chung_nhom_voi_cha=True job_control=? ns_pid=pid:[4026532322] init=codex
nhom tien trinh: da tach sang session moi (pgid=3819)
  lan 1/1: qua

LAP r926_dot_bien_tu_sinh_moi_thanh_phan_regex: 1/1 qua, 0 bo qua, 0 hong
[rc 0]
```

```text
$ python3 src/.claude/dev/launcher_test.py --lap-ca r926_bo_sinh_bien_the_co_du_phep --lan 1
moi truong: pid=3818 pgid=1 sid=1 truong_nhom=False chung_nhom_voi_cha=True job_control=? ns_pid=pid:[4026532322] init=codex
nhom tien trinh: da tach sang session moi (pgid=3818)
  lan 1/1: qua

LAP r926_bo_sinh_bien_the_co_du_phep: 1/1 qua, 0 bo qua, 0 hong
[rc 0]
```

`python3 -B review-r26j-HjiNZnsS/review.py mutants` returned **rc 0** and `mutants: 134/134`. All **124/124** `DOT_BIEN` entries named `r25_*` or `r26_*` were freshly applied to unique temporary copies of this SHA’s `launcher.py`. Every replacement matched exactly once and every result compiled. All **134/134 designated target executions** returned **rc 42**, a wrapper code reserved solely for `TinHieuChotCa` with the named target’s actual code object in the traceback. Wrong-origin signals, other exceptions, returns/skips and timeouts are not credited. **0 survivors / 0 unmeasured / 0 wrong-origin or unrelated-error kills.** `mutation-inventory.json` preserves the exact replacements, source hashes, paths and targets; `mutants.json` preserves each command and output; `mutation-reasons.md` lists the actual target assertion for each kill.

Mutation credit is based on the stricter independent wrapper, not the existing broad `chay_dot_bien()` exception catch. A failing setup would also fail the unchanged-copy control. Text-mode sink removal intentionally fails the production unbuffered-file contract; type checks may raise inside the filter, which the target observes as the wrong classification. Those are asserted behavioral regressions, not escaped harness exceptions.

Supplemental neutral-control setup correction: the first neutral-copy batch returned **rc 1** after 28 successful controls because this reviewer set a **100-second outer timeout** on the instrumented regex-generator case. The ordinary required CLI case had already passed in **105.72 seconds**; that timeout was too short. `logs/neutral-driver.json` preserves the failure. It is **not** a source failure or mutation kill. Only the unfinished controls are resumed with a 300-second outer limit; prior successful controls are not rerun or overwritten.

## Substantive review of the full delta against master

Reviewed the complete diff from `cdc4e80bc439fa974775f319dccac5bf2fc955fe` to `0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f` (saved as `review-r26j-HjiNZnsS/full-master.diff`, git rc 0), its surrounding production integration, all added/changed test bodies and the complete selected mutation inventory. This is a substantive review on the merge head, not approval inferred from equal parent-1 blobs.

| Contract / current source anchor | Assessment and fresh evidence |
|---|---|
| Exact stderr allow-list — `.claude/dev/launcher.py:1605`, `:1734` | Only the first chunk of a physical line equal to a complete LF/CRLF constant reaches the sink. Comparison precedes normalization. Partial, prefixed, suffixed, repeated-CR and continuation fixtures are rejected. Sample-secret run-directory scan passes. Broad-write/prefix/continuation/CRLF/routing mutants fail. No new raw trace spool or fallback output path is present. |
| Frame provenance and contents — `launcher.py:1653` | Exact receive header, strict UTF-8/JSON, accepted event set, response object and nonblank string id/model checks precede retention. Dedup uses both response id and model; the first arrival is retained. Source/position/event/type/blank/decode/dedup mutants fail. This verifies log-format provenance, not independent cryptographic server identity. |
| Lost and unknown evidence — `launcher.py:1696`, `:1726` | Complete single-chunk parsing is distinguished from multichunk/EOF-cut classification. Sticky candidate evidence and normalized carry survive the supplied split sweeps; unconfirmed JSON receive headers veto positive measurement through `khong_ro`. The tests distinguish loss, unknown, noncandidate events and non-JSON Ping/Binary records. Each pertinent branch/operand removal in the inventory fails its designated target. |
| Bounded reads and write accounting — `launcher.py:1648`, `:1674`, `:1729` | Normal and error-drain reads are capped at 4 MiB. The first retained chunk is bounded by that cap; subsequent prefix accumulation and 64-byte carry remain bounded. The unbuffered sink loops over short writes, rejects no progress and counts only unwritten bytes; drain and closed-sink paths count discarded bytes. Corresponding mutants fail. `stderr_bo_dong` deliberately counts discarded read chunks, as documented, not necessarily physical lines. |
| EOF, startup and snapshot — `launcher.py:1770`, `:1794`, `:1800` | Reader is daemonized; startup failure records the exception class and closes the pipe. Finalization joins with the 10-second bound, latches liveness before closing the sink, then derives evidence from copied collections. Unlatched state is incomplete. Live readers can no longer yield a positive measurement later. The real finish-during-close and inherited-pipe cases pass; ordering, unbounded-join, daemon, start-failure and each snapshot mutant fail. Counters cover consumed/discarded bytes at snapshot time, not unread future pipe bytes. |
| Production routing and old behavior — `launcher.py:1933`, `:2023` | Binary/unbuffered filtering and exact `RUST_LOG` replacement remain scoped to Codex. Non-Codex stderr and receipt shape pass their explicit case. The pre-existing process-group/Windows flags, kill logic, prompt handling and final log hashing are unchanged; six core helpers are AST-identical to master. Timeout 124 is freshly exercised by the required fake-Codex case. |
| Test strength — `launcher_test.py:6993`, `:7091`, `:7217`, `:7234`, `:11144` | Current production predicates and their boolean operands were checked against the selected registered mutants; an independent AST census finds all seven regex literals and agrees with the generator’s per-literal counts. The generator requires every non-equivalent variant to die, rejects unrelated exceptions and stale exemptions, and has a separate operator-inventory case. Finite mutation coverage is not proof over all possible code edits or inputs. |

The predicate census (`static-audit.json`, 44 control-flow entries including unchanged Windows routing) was inspected against the replacement inventory and source. No additional unguarded policy decision was established in the reviewed filter scope. The regex generator’s operators cover token deletion, character/class/escape widening, whitespace-to-space, word widening, quantifier changes, class-member/negation removal, inward range endpoint changes, mandatory-atom optionalization, atom-plus-quantifier deletion and alternation-branch deletion. Discovery is line-oriented, but the independent AST census confirms that it discovers every literal in the current filter block.

Earlier findings in `VERDICT_R26I.md` are not re-raised. Current-head evidence supports their closure:

- R25-SEC-01, R25-MEAS-02, R25-ROBUST-04, R25-EVID-05, R25-RACE-06, R25-CONTRACT-07: fresh exact-list/provenance/bounded-read/loss/unknown/snapshot/non-Codex cases and targeted mutations support the fixes; v2 authorizes loss of other Codex diagnostics.
- R26-ALLOW-08, R26-COUNT-09, R26-EOF-10, R26-CLASSIFY-11: fresh wire-ending, accounting, close-order and per-physical-line cases pass; their regressions are killed.
- R25-TEST-03 and R26-TEST-12 through R26-TEST-16: all 124 registered mutations compile, match uniquely and fail through the correct target signal, including short/zero writes, late production finalization, constituent predicates, grammar components, daemon, binary sink and the three copies.
- R26-TEST-17: the previously false equivalents are absent from the exception table; the required grammar/generator/operator cases pass. The final observed survivor census is recorded below.

The remaining Popen failure path exits before successful final evidence serialization; absence of `bo_loc` there does not create a false `DO_DUOC`. The liveness latch is a sample immediately following join, not a separate timestamp of EOF within the scheduling interval; no stronger timing guarantee is claimed.

No new exploit payload was authored. Existing supplied fixtures, registered mutants and the existing regex generator were used. Further directions such as longer normalization sequences split across chunks, duplicate/escaped event fields in oversized records and nested candidate-like content were not explored with new payloads; they are unproved directions, not asserted defects or passing tests.

**New findings: none. Open findings: 0 P0, 0 P1, 0 P2, 0 P3.** There is no new finding ID/location/scenario/fix to report. No production patch is proposed.

## Final generated/neutral evidence and regressions

The resumed supplemental command `python3 -B review-r26j-HjiNZnsS/review.py neutral --resume` returned **rc 0**, `neutral: 38/38`. All 38 exact-source temporary-copy controls pass, including all 34 distinct registered-mutant targets. The instrumented generator completed in **96.97 seconds**; its trace records the actual generator’s locals and exception origins without modifying its source or assertions.

Observed generator result: **207 variants = 200 target-origin `TinHieuChotCa` kills + 7 survivors**, with **0 unrelated errors**. Kill attribution is **175** to `r926_hop_dong_ngu_phap_bo_loc_theo_hanh_vi` and **25** to other supplied cases; the contract case alone is not credited with all 200. Per-literal counts: ANSI 29; header 67; complete frame 19; candidate token 33; whitespace 6; prefix classifier 50; JSON header 3. Independent AST discovery agrees **7/7 literals** (`static_audit.py`, rc 0). Observations and exact targets/assertions are in `generated-observations.json`.

All seven survivors exactly match the declared equivalent set, with current reachable-call-site reasons independently checked:

| Equivalent family | Count | Why unchanged in current production calls |
|---|---:|---|
| Remove header start anchor | 1 | All three header consumers use `.match`, which already starts at byte zero. |
| Require trailing whitespace after the closing brace | 1 | Only a complete physical line can reach positive parsing, and its final LF remains after ANSI removal. |
| Match whitespace singly, optionally or with zero-or-more repetition before deleting it | 3 | All whitespace is removed by substitution with empty bytes; empty matches add nothing. |
| Widen/optionalize the prefix opening brace | 2 | A prefix mismatch cannot create an unknown count without the independent exact JSON-header brace check; an actual JSON-header opening brace matches both original and variant. |

Thus R26-TEST-17 remains closed on **this SHA**. Earlier generator omission-control experiments from round 9 were not counted as round-10 executions; this round freshly ran both required generator cases and observed all generated outcomes.

`python3 -B review-r26j-HjiNZnsS/regression.py`: **rc 0**, **9 passed / 1 skipped / 0 failed**. The passes are t27, t28, t63, t66, t79, t80, t81, t83 and r14. t62 explicitly skips on Linux because its fixture is Windows-only. Windows mocks are not native Windows acceptance.

`python3 -B review-r26j-HjiNZnsS/observations.py`: **rc 0**, `OBSERVATIONS PASS`:

- Native unbuffered FileIO under a file-size limit: **43 input bytes = 10 stored + 33 discarded**, with `OSError`, using the existing short-write fixture bytes.
- Fake Codex run: launcher **rc 0**, `DO_DUOC`; stored stderr **39 bytes**, SHA-256 **`1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721`**, **186 bytes discarded**. Both log byte counts and hashes match the receipt. The run directory contains exactly `run.json`, `stderr.log`, `stdout.log`.
- Exit 125 path: the real kill completed, then an in-memory seam withheld whole-tree success attestation. Launcher and receipt both returned **125**, `giet_tron_ven=false`, model status `KHONG_DO_DUOC`; no child was intentionally left running. This supplements, rather than impersonates, native Windows t62.

## Final integrity, identity limits and disposition

`python3 -B review-r26j-HjiNZnsS/final_integrity.py` returned **rc 0**, `FINAL INTEGRITY PASS`. Exact commands and outputs are in `logs/final-*.json` and the human-readable `commands.md` transcript. Final results:

```text
$ git -C src rev-parse HEAD 'HEAD^{tree}' 'HEAD^1' 'HEAD^2' refs/remotes/origin/master refs/heads/agent/wp748-r26-claude
0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
ba9106b45cc0045b5bd0f56a7f465be771ccf6dc
3877d463c0d9b7a0757d051d547c824814601370
cdc4e80bc439fa974775f319dccac5bf2fc955fe
cdc4e80bc439fa974775f319dccac5bf2fc955fe
0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
[rc 0]
```

```text
$ git -C src rev-parse --is-shallow-repository
false
[rc 0]
```

```text
$ git -C src symbolic-ref -q HEAD
[empty output]
[rc 1]
```

```text
$ git -C src status --short --untracked-files=all --ignored
[empty output]
[rc 0]
```

```text
$ git -C src diff --exit-code
[empty output]
[rc 0]
```

```text
$ git -C src diff --cached --exit-code
[empty output]
[rc 0]
```

```text
$ git -C src diff --check cdc4e80bc439fa974775f319dccac5bf2fc955fe 0a2ba0bdc2038d0ddf3a5e4dc7af459ebe5afd4f
[empty output]
[rc 0]
```

```text
$ git -C src config --get-regexp '^(extensions\.partialclone|remote\..*\.promisor)$'
[empty output]
[rc 1]
```

```text
$ git -C src fsck --connectivity-only --no-dangling
[empty output]
[rc 0]
```

Both reviewed source files match their committed bytes. Source SHA-256:

- `launcher.py`: `51342501e0126611f81748f614ef2246a7d87069b57ace67e72200a28862a7a1`
- `launcher_test.py`: `bb329cc82b1c2e511088ebf0a59a982aaba35f4f14f066d14e576a5da1c30592`

All 124 registered temporary mutants were reconstructed from HEAD and byte/hash-compared with the executed files; each compiles. The neutral source and both companion modules match the committed source. The target execution multiset matches every declared r25/r26 target exactly, and every credited signal has the named target’s code object in its traceback. HEAD/tree/parents/branch remain exact, the clone remains detached and non-shallow, no partial-clone/promisor marker is configured, connectivity is valid, and tracked/untracked/ignored status plus worktree/index diffs are empty.

Runtime identity: **OpenAI Codex, GPT-6-based agent**, provider `openai_codex`, model family `openai`; observed tool-mediated local shell on Linux x86_64, Python **3.13.16**, transport `machine`. Exact serving model/build/effort/session attestation, enclosing CLI-versus-service identity and the outer `launcher.py run` receipt are **not independently visible or verified**. No GitHub submitter identity is claimed.

**Not run / unverified:** full Linux repository gates, native Windows execution and Windows CI, authenticated live Codex acceptance, remote CI/check state, live pushed/unpushed status and the owner’s remote authority/call ledger. GitHub cannot be read in this review. The user-supplied 1,300-line and 10-call limits are the authority used here; the measured delta is **1,190 added lines** and this is the supplied **10/10 invocation**. No further Codex invocation was made. The offline review approves the examined exact-SHA code/test delta; it does not certify those external gates or grant merge/land/deploy authority.

No edits to `src`, source commits, pushes, GitHub comments, credential use or subagents occurred. Temporary fixture commits were made by the requested tests outside `src`. Final filesystem integrity supports the read-only review procedure; no independent read-only-mount attestation is claimed.

Evidence index: `commands.md` contains exact commands, real stdout/stderr and return codes; `logs/*.json` additionally record UTC and duration. `targeted.json`, `neutral.json`, `mutants.json`, `mutation-inventory.json`, `mutation-reasons.md`, `generated-observations.json`, `static-audit.json`, `merge-audit.json`, `regression.json`, `observations.json` and `final-integrity.json` preserve the detailed measurements. Drivers and temporary mutation copies remain under `review-r26j-HjiNZnsS/`.

**Final totals: 38/38 required cases passed; 38/38 temporary-copy controls passed; 124/124 registered mutants killed by 134/134 named target signals; 207 generated variants = 200 kills + 7 justified equivalents; 9 additional regressions passed, 1 Windows-only case skipped. New/open findings: 0 P0, 0 P1, 0 P2, 0 P3.**

Completed UTC: **2026-10-25T16:16:41.611952+00:00**.

VERDICT: approve
