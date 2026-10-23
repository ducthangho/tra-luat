# Independent re-review — WP748 r22, PR #869, round 2

Reviewer identity reported by runtime: “Codex, an agent based on GPT-6.” Provider: OpenAI; system-reported surface: API; observed transport: direct local tools (`functions.exec` / `exec_command`). Exact backend model slug, effort and independent provider/session attestation are not exposed. The user reports `launcher.py run` with an execution receipt; local `launcher.out` and `launcher.err` are empty at start, so I cannot independently verify that invocation or its final receipt.

Reviewed SHA: `a56a3219e58ddf4c87cafac1e7357962d643e3db`  
Reviewed tree: `599f99796caf06fb1c6a0e7615e9df870cdc006f`  
Parent: `056b316c414d35791a6dce00532d4e905c9d17d8`  
Base / local `origin/master`: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`.

Initial identity verification PASS: all four OIDs match, HEAD detached (`symbolic-ref -q HEAD` produced no ref), `git status --short` empty. Source is read-only. Authorized writes: this report and scratch outside `src/`; no credentials, network, GitHub comments, commits or pushes.

Platform: Linux 6.18.44-fc-v140, Python 3.13.16. Native Windows execution unavailable; Windows conclusions will distinguish static reasoning / mocks from native evidence.

The required cloud-runtime skill was read. No `environment_status` tool is available. No credentials or secret contents inspected.

Status: in progress.

Started UTC: 2026-10-22T07:39:07.682468+00:00

Archive UTC 2026-10-22T07:40:29.610306+00:00: `git -C src archive --format=tar a56a3219e58ddf4c87cafac1e7357962d643e3db`, rc=0, extracted to `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22b/review-wp748-r22-round2-KsEuyd/head`. Reviewed file byte-identical to Git blob; SHA-256 `960091c38c3a1be4a8e8ddc48bd9dd826f371a21c32f9e849bbd4a93a8440ae6`. Delta: one file, 213 insertions / 80 deletions.

Started `product` UTC 2026-10-22T07:40:29.807557+00:00: `{'NHANH_DON_DUOC_KHONG_DOT_BIEN': '1'} /usr/bin/python3 ops/nhanh_don_duoc_test.py` (archive cwd; minimal credential-free environment; watchdog 90s).

Completed `product`: rc=0, 1.771s, UTC 2026-10-22T07:40:31.579119+00:00. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22b/review-wp748-r22-round2-KsEuyd/product.log`.

```text
CASE T1: DAT
CASE T2: DAT
CASE T3: DAT
CASE T4: DAT
CASE T5: DAT
CASE T6: DAT
CASE T7: DAT
CASE T8: DAT
8/8

```

Started `selfchecks` UTC 2026-10-22T07:40:31.579584+00:00: `{'NHANH_DON_DUOC_CHI_TU_KIEM': '1'} /usr/bin/python3 ops/nhanh_don_duoc_test.py` (archive cwd; minimal credential-free environment; watchdog 120s).

Completed `selfchecks`: rc=0, 31.112s, UTC 2026-10-22T07:41:02.691330+00:00. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22b/review-wp748-r22-round2-KsEuyd/selfchecks.log`.

```text
TU KIEM r542: DAT
TU KIEM r539: DAT
TU KIEM r540: DAT
TU KIEM r541: DAT
TU KIEM r501: DAT
TU KIEM r502: DAT
TU KIEM r503: DAT
TU KIEM r504: DAT
TU KIEM r505: DAT
TU KIEM r506: DAT
TU KIEM r507: DAT
TU KIEM r508: DAT
TU KIEM r509: DAT
TU KIEM r510: DAT
TU KIEM r511: DAT
TU KIEM r512: DAT
TU KIEM r513: DAT
TU KIEM r514: DAT
TU KIEM r515: DAT
TU KIEM r516: DAT
TU KIEM r517: DAT
TU KIEM r518: DAT
TU KIEM r519: DAT
TU KIEM r520: DAT
TU KIEM r521: DAT
TU KIEM r522: DAT
TU KIEM r523: DAT
TU KIEM r524: DAT
TU KIEM r525: DAT
TU KIEM r526: DAT
TU KIEM r527: DAT
TU KIEM r528: DAT
TU KIEM r529: DAT
TU KIEM r530: DAT
TU KIEM r531: DAT
TU KIEM r532: DAT
TU KIEM r533: DAT
TU KIEM r534: DAT
TU KIEM r535: DAT
TU KIEM r536: DAT
TU KIEM r537: DAT
TU KIEM r538: DAT
TU KIEM r543: DAT
TU KIEM r544: DAT
TU KIEM r545: DAT
TU KIEM r546: DAT
TU KIEM r547: DAT
TU KIEM r548: DAT
TU KIEM r549: DAT
TU KIEM r550: DAT
TU KIEM r551: DAT
TU KIEM r552: DAT
TU KIEM r553: DAT
TU KIEM r554: DAT
TU KIEM r555: DAT
TU KIEM: 55/55

```

Started `targeted` UTC 2026-10-22T07:41:02.691684+00:00: `{} /usr/bin/python3 /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22b/review-wp748-r22-round2-KsEuyd/mutants.py targeted` (archive cwd; minimal credential-free environment; watchdog 180s).

Completed `targeted`: rc=0, 7.612s, UTC 2026-10-22T07:41:10.303801+00:00. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22b/review-wp748-r22-round2-KsEuyd/targeted.log`.

```text
{"mutant": "timeout-chi-giet-con", "chi_dich": true, "child_rc": 1, "markers": ["TU KIEM: 0/1"]}
DOT BIEN TU KIEM timeout-chi-giet-con | r555 | 1/1
{"mutant": "timeout-chi-giet-con", "chi_dich": true, "result": [1, 0, 0], "seconds": 6.613}
{"mutant": "gop-bo-kiem-nhom", "chi_dich": true, "child_rc": 1, "markers": ["TU KIEM: 0/1"]}
DOT BIEN TU KIEM gop-bo-kiem-nhom | r552 | 1/1
{"mutant": "gop-bo-kiem-nhom", "chi_dich": true, "result": [1, 0, 0], "seconds": 0.209}
{"mutant": "gop-bo-kiem-san", "chi_dich": true, "child_rc": 1, "markers": ["TU KIEM: 0/1"]}
DOT BIEN TU KIEM gop-bo-kiem-san | r552 | 1/1
{"mutant": "gop-bo-kiem-san", "chi_dich": true, "result": [1, 0, 0], "seconds": 0.218}
{"mutant": "moc-nhan-sai-dinh-dang", "chi_dich": true, "child_rc": 1, "markers": ["TU KIEM: 0/1"]}
DOT BIEN TU KIEM moc-nhan-sai-dinh-dang | r554 | 1/1
{"mutant": "moc-nhan-sai-dinh-dang", "chi_dich": true, "result": [1, 0, 0], "seconds": 0.141}
{"mutant": "moc-bo-kiem-dao-nguoc", "chi_dich": true, "child_rc": 1, "markers": ["TU KIEM: 0/1"]}
DOT BIEN TU KIEM moc-bo-kiem-dao-nguoc | r554 | 1/1
{"mutant": "moc-bo-kiem-dao-nguoc", "chi_dich": true, "result": [1, 0, 0], "seconds": 0.143}
{"mutant": "moc-bo-kiem-lech-giay", "chi_dich": true, "child_rc": 1, "markers": ["TU KIEM: 0/1"]}
DOT BIEN TU KIEM moc-bo-kiem-lech-giay | r554 | 1/1
{"mutant": "moc-bo-kiem-lech-giay", "chi_dich": true, "result": [1, 0, 0], "seconds": 0.156}
MUTANTS chi_dich=True: 6/6

```

Started `full` UTC 2026-10-22T07:41:10.305015+00:00: `{} /usr/bin/python3 /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22b/review-wp748-r22-round2-KsEuyd/mutants.py full` (archive cwd; minimal credential-free environment; watchdog 360s).

Completed `full`: rc=0, 196.408s, UTC 2026-10-22T07:44:26.712998+00:00. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22b/review-wp748-r22-round2-KsEuyd/full.log`.

```text
{"mutant": "timeout-chi-giet-con", "chi_dich": false, "child_rc": 1, "markers": ["TU KIEM: 54/55"]}
DOT BIEN TU KIEM timeout-chi-giet-con | r555 | 1/1
{"mutant": "timeout-chi-giet-con", "chi_dich": false, "result": [1, 0, 0], "seconds": 32.941}
{"mutant": "gop-bo-kiem-nhom", "chi_dich": false, "child_rc": 1, "markers": ["TU KIEM: 54/55"]}
DOT BIEN TU KIEM gop-bo-kiem-nhom | r552 | 1/1
{"mutant": "gop-bo-kiem-nhom", "chi_dich": false, "result": [1, 0, 0], "seconds": 29.94}
{"mutant": "gop-bo-kiem-san", "chi_dich": false, "child_rc": 1, "markers": ["TU KIEM: 54/55"]}
DOT BIEN TU KIEM gop-bo-kiem-san | r552 | 1/1
{"mutant": "gop-bo-kiem-san", "chi_dich": false, "result": [1, 0, 0], "seconds": 32.574}
{"mutant": "moc-nhan-sai-dinh-dang", "chi_dich": false, "child_rc": 1, "markers": ["TU KIEM: 54/55"]}
DOT BIEN TU KIEM moc-nhan-sai-dinh-dang | r554 | 1/1
{"mutant": "moc-nhan-sai-dinh-dang", "chi_dich": false, "result": [1, 0, 0], "seconds": 33.618}
{"mutant": "moc-bo-kiem-dao-nguoc", "chi_dich": false, "child_rc": 1, "markers": ["TU KIEM: 54/55"]}
DOT BIEN TU KIEM moc-bo-kiem-dao-nguoc | r554 | 1/1
{"mutant": "moc-bo-kiem-dao-nguoc", "chi_dich": false, "result": [1, 0, 0], "seconds": 33.469}
{"mutant": "moc-bo-kiem-lech-giay", "chi_dich": false, "child_rc": 1, "markers": ["TU KIEM: 54/55"]}
DOT BIEN TU KIEM moc-bo-kiem-lech-giay | r554 | 1/1
{"mutant": "moc-bo-kiem-lech-giay", "chi_dich": false, "result": [1, 0, 0], "seconds": 33.734}
MUTANTS chi_dich=False: 6/6

```

Review checkpoint: all requested checks completed on Linux (product 8/8, self 55/55, targeted mutants 6/6, full-case mutants 6/6; all driver rc=0). Every mutant child rc=1, exactly one declared case failed; targeted children 0/1, full children 54/55. The six named mutants, not the entire mutant catalog, were run in both modes.

Additional command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 review-wp748-r22-round2-KsEuyd/probes.py > review-wp748-r22-round2-KsEuyd/probes.log 2>&1`, rc=0, **20/20 probe expectations** (includes expected defect reproductions, not 20 source correctness claims). Scratch probes reuse the repository's heartbeat child and mutate only in-memory functions / OS outcomes. No unusual input payloads authored.

Confirmed open finding: **WP748-R22-F02, P2, `timeout-descendant-containment`**. POSIX one-time PPID snapshot misses a detached grandchild reparented before timeout. Reusing r555 and terminating only its owned direct parent after the heartbeat began yielded rc=124 in 1.753 s (run/drain budgets 1.5/0.25 s), continued grandchild heartbeat, and false `chup 0 hau due ... 0 hau due song`. r555's later assertion detected survival and its cleanup stopped the probe-owned grandchild. Same-group control stopped in 1.554 s. Locations: `ops/nhanh_don_duoc_test.py:408`, `:518`, `:540`.

The same finding still includes Windows uncontained fallbacks (`:464`, `:477`, `:482`, `:489`): mocked job creation / assignment failure proceeds to resume; failed/absent tree termination falls back to direct-child kill. Mocks leave a descendant alive for create/assign/terminate failure. Native Windows not run. Bounded output abandonment improves return liveness, but it does not contain surviving processes. Further details and remediation will follow below.

Omitting only the descendant signal loop at `:531` in scratch memory: same-group variant returned rc124 in 1.553 s, detached variant in 11.552 s with a live descendant and abandoned output. Unchanged r555 correctly failed its 4.5 s bound; fixture cleanup ran. This verifies the new variant detects losing that loop.

Checkpoint UTC: 2026-10-22T07:46:10.604772+00:00

## Final findings

### WP748-R22-F02 — P2 — `timeout-descendant-containment` — remains open

This is the continuing round-1 class, not a new finding ID for each symptom. Five related manifestations remain; the first has a live Linux reproduction and independently blocks approval.

1. **A timeout-time PPID snapshot is not a lifetime boundary.** `ops/nhanh_don_duoc_test.py:408`, `:518`, `:540`. A detached grandchild whose parent exits before the snapshot is already reparented, so the traversal cannot associate it with `q`. It escapes both the original process group and the descendant loop. The live probe described above observes continued heartbeat after rc124 and misleading zero-survivor diagnostics. A descendant born after enumeration has a similar gap (source-derived, not executed). When `/proc` is unavailable, unreadable, or incomplete, `{}` also becomes an unsupported claim of zero survivors; the unavailable-`/proc` mock confirms this. **Fix:** establish per-run ownership before execution that survives reparenting (for example an owned cgroup where supported, or a dedicated supervised subreaper with retained identities and a clearly defined process model). Treat unavailable/incomplete discovery as unverified cleanup, not zero survivors. A repeated late PPID scan alone cannot recover already-lost ancestry.

2. **Windows failure paths still resume or start a process without containment.** `ops/nhanh_don_duoc_test.py:464`, `:477`, `:482`, `:489`, `:504`, `:553`. The healthy sequence is suspended creation → assignment → resume, and the healthy timeout calls `TerminateJobObject`. However, job creation failure still resumes; assignment failure closes the job and then resumes; missing DLL support starts unsuspended. If taskkill is absent, nonzero, or times out, only the direct child is killed. Closing this job handle does not implement a kill-on-close policy: no such limit is configured. Stateful mocks show descendant survival on create/assign/terminate failure with unavailable taskkill. `TerminateJobObject` success is reported without an independent job-membership/active-process verification; failure even produces the misleading `KHONG co job (None)` diagnostic. **Fix:** require a working lifetime boundary before allowing execution, otherwise terminate/reap the still-suspended child and return a distinct infrastructure failure. Keep a bounded emergency path and truthful verification for termination failures. Configure safe job/handle ownership and close handles on failed `Popen` as well (currently `Popen` precedes the `try/finally` at `:557`). Native Windows remains not measured.

3. **Cleanup exceptions can replace the promised timeout result and skip fixture cleanup.** `ops/nhanh_don_duoc_test.py:529`, `:501`, `:566`, `:4325`, `:4332`. `q.kill()` is not protected when the group kill or lookup fails, and the timeout handler does not catch cleanup exceptions. An actual `run(check=False)` dispatch with mocked lookup/kill permission errors raises `PermissionError`, rather than returning rc124. r555's grandchild-cleanup `finally` starts only after `run` returns, so an exception from `run` bypasses that cleanup. `/proc` parsing also has unhandled decoding/value/index failures: a process name containing bytes outside the decoder's accepted encoding can interrupt the global scan; this hostile-input scenario is described only, not authored or executed. **Fix:** keep timeout as the primary result, attach bounded cleanup diagnostics and incomplete-cleanup status, and place owned-process teardown around the entire spawn/run/assert sequence. Do not turn a failure to clean into success, or swallow its diagnostics.

4. **The identity check narrows but does not close PID reuse.** `ops/nhanh_don_duoc_test.py:532`, `:534`. A matching `starttime` is checked before a separate PID-based signal. Exit/reuse between those operations can target a replacement process. The mock model reproduces the signal being applied to a replacement generation; the stale-before-check control correctly skips signalling. No real PID-reuse stress or unrelated-process signalling was attempted. **Fix:** retain a stable process handle/pidfd, verify its identity, and signal through that handle, or use a stable owned containment boundary. Merely checking `starttime` again before a PID-based signal still leaves a race.

5. **r555 teardown ignores identity entirely.** `ops/nhanh_don_duoc_test.py:4303`, `:4344`. Its final cleanup always signals the numeric PID from the file, including after successful tree termination and the 0.9-second heartbeat observation. If that PID is recycled, it can kill an unrelated replacement. This is source-derived; no real replacement process was harmed or used as a target. **Fix:** retain owned process identity/handles for fixture cleanup too, and do not signal a reused PID. This shares the same lifetime/identity correction as item 4.

Regression closure should cover parent exit before timeout, intermediate-parent exit, detached descendants, job creation/assignment/resume/termination failures, unavailable/nonzero/slow taskkill, pipe-retaining descendants, kill permission failures, unsupported `/proc`, and identity changes. Keep the healthy same-group and detached controls. Require bounded return, the correct rc, truthful cleanup status, and no surviving owned processes or signals to replacements. Run native Windows baseline and mutant controls, not only mocks.

Remediation risks: an overbroad cgroup/subreaper or process-group selection can affect unrelated runs; nested Windows jobs may reject assignment; abort-before-resume must not leave a suspended child; stable-handle acquisition must itself verify identity; asynchronous output abandonment can retain reader threads/handles until writers exit. Keep cleanup scoped to the owned run and avoid synchronous pipe close while a reader holds its lock.

## What is fixed, and what was actually measured

- **Normal timeout containment:** unmodified Linux r555 passed both same-group and detached-session variants. Its unchanged baseline was also green in all five full-case runs of non-timeout mutants. The own-group guard (`group == q.pid` and `group != own group`) remains explicit, and the mock verifies no `killpg` call when the groups coincide.
- **Suspension handling:** Windows DLL-load failures select unsuspended creation. Missing/failing resume is caught and attempts direct-child termination. API mocks verify those paths; this is conditional on termination succeeding, not proof that every OS failure can be recovered. Assignment failure resumes without a job, which is the containment issue above.
- **Bounded output:** the explicit synchronous `stdout`/`stderr.close()` after a failed drain is gone. Using the installed CPython 3.13 Windows `_readerthread` and `_communicate` implementations on Linux pipes, the reviewed `run` returned rc124 in **1.751 s** for budgets **1.5/0.25 s**, with both reader threads still alive. r555 detected the surviving grandchild; its cleanup then released both threads. This closes the prior lock-wait mechanism in that simulation. It is not native Windows evidence and does not certify taskkill's native behavior or all exception paths.
- **F03:** `timeout-chi-giet-con` now changes the common call at `:566` via the descriptor at `:5167`. On both branches it skips tree termination and does direct-child-only `q.kill()`. A healthy Windows job does not secretly undo this mutation on `dong()` because kill-on-close is not configured. The grandchild retains the output pipes, so the five-second drain exceeds r555's 4.5-second limit; its heartbeat supplies another check. Dispatch mocks give the same baseline-versus-mutant tree-state difference for POSIX and Windows. Linux target-only and full-case runs both kill exactly r555. The former Windows no-op defect is corrected; **native Windows baseline and mutant execution are not_run**, so a native Windows pass is not claimed.
- **r555 sensitivity / flakiness:** the approximately 60-second heartbeat lifetime exceeds the run, verification, drain, and observation periods, so natural completion cannot explain the ordinary observed pass. Two variants are justified: process-group killing handles the first, and the tracked-descendant loop is needed for the second. Removing only that loop made the detached variant take **11.552 s**, fail the **4.5 s** bound, and report a live descendant. The 1.5-second startup budget and 4.5-second total bound can produce a red result on a heavily stalled runner; missing startup evidence correctly fails rather than passes. The 0.6-second unchanged-heartbeat observation is not proof of death for a stopped/starved process. There is no external watchdog inside r555 itself, so its elapsed-time assertion cannot interrupt a hang; the requested-suite driver had external watchdogs; supplemental live probes reused the finite 60-second fixture. No native Windows or stress/load flakiness measurement was performed. Fix the teardown problems in F02 without weakening the ordinary bound.
- **r554 narrowing is legitimate for this delta.** `:4295` selects exactly one valid control plus the three timing cases; `:4298` enforces 4 total / 1 valid. `_phan_chung_gop_dich(chi=None)` still runs the complete matrix, and the real `gop_dich` caller at `:6276` retains the default. Measured: narrow **4/4** (1 valid, 3 rejected), complete **46/46** (3 valid, 43 rejected). The group validation remains in the shared `_loi_nhom_bat_buoc`, in `_loi_gop_dich`, and under r552's tests. Both group mutants now kill only r552 with r554 green; each timing mutant kills only r554 with r552 green. The new selector does not suppress production validation or hide an observed collector defect.
- **F04:** `:6056` explicitly uses ASCII ranges in all seven digit repetitions plus `re.ASCII`; `_doc_moc_utc` still uses fullmatch and calendar validation. A real `_iso_utc()` value was accepted, and regex token inspection confirmed every digit range is ASCII. Alternate digit-alphabet scenarios are described only; no unusual strings were authored. The reported lexical defect is corrected.

## Commands and counts

All tests ran from the archive, with bytecode disabled, global/system Git configuration disabled, `core.abbrev=7` for the requested suites, and a minimal environment containing no credentials. Existing fixture tests make local fixture repositories; no source commits or remote operations were performed. The full exact command/environment recipes and UTC timing are in `review-wp748-r22-round2-KsEuyd/run_review.py` and `test-receipts.json`.

| Command / scope | Driver rc | Positive result |
|---|---:|---|
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 python3 ops/nhanh_don_duoc_test.py` | 0 | product 8/8 |
| `NHANH_DON_DUOC_CHI_TU_KIEM=1 python3 ops/nhanh_don_duoc_test.py` | 0 | self cases 55/55 |
| `python3 ../mutants.py targeted` | 0 | 6/6 killed, `chi_dich=True` |
| `python3 ../mutants.py full` | 0 | 6/6 killed, `chi_dich=False` |
| `python3 review-wp748-r22-round2-KsEuyd/probes.py` (minimal `env -i`, as recorded above) | 0 | 20/20 expectations, including defect reproductions |
| `python3 review-wp748-r22-round2-KsEuyd/probe_pipe_and_identity.py` (same minimal environment) | 0 | 6/6 expectations, including pipe fix and remaining defects |
| `python3 review-wp748-r22-round2-KsEuyd/probe_windows_fallbacks.py` (same minimal environment) | 0 | 9/9 mocked Windows API/fallback expectations; native Windows not run |

| Mutant | Declared and observed failed case | `chi_dich=True` | `chi_dich=False` |
|---|---|---:|---:|
| `timeout-chi-giet-con` | r555 | 1/1 | 1/1 |
| `gop-bo-kiem-nhom` | r552 | 1/1 | 1/1 |
| `gop-bo-kiem-san` | r552 | 1/1 | 1/1 |
| `moc-nhan-sai-dinh-dang` | r554 | 1/1 | 1/1 |
| `moc-bo-kiem-dao-nguoc` | r554 | 1/1 | 1/1 |
| `moc-bo-kiem-lech-giay` | r554 | 1/1 | 1/1 |

Each of the twelve mutant children exited **1**; target-only children report **0/1** self cases passed, and full-case children **54/55**. Those expected negative child totals are evidence of the mutant kill, not baseline failures. Completion evidence and exact failed-case sets were accepted by the real mutation grader; no unrelated `DO_KHAC` failures. Raw child logs are retained individually in scratch.

Not run: native Windows, the rest of the full mutant catalog, all eight real shard executions/performance receipts, repository-wide release gates, or remote CI/PR inspection. The reported earlier CI failure was supplied by the user, not independently fetched. Current local runs independently verify the two relevant mutants' corrected failure radius. Review threshold is zero P0/P1/P2; one P2 class remains open.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Source: attached `VERDICT_LUOT1_056b316.md`, reviewed SHA `056b316c414d35791a6dce00532d4e905c9d17d8`.

| Finding / stable class | Round-2 assessment | Evidence and remaining scope |
|---|---|---|
| F02 P2 / `timeout-descendant-containment` | **VÁ HỜ** — substantial partial repair, still P2 | Ordinary Linux detached tree and simulated Windows pipe lock repaired; reparented detached tree survives, Windows fallback can remain uncontained, identity/exception/teardown gaps remain. Native Windows unmeasured. |
| F03 P2 / `timeout-mutant-platform-coverage` | **ĐÃ VÁ THẬT for the platform-specific no-op in the descriptor** | Common call-site mutation verified by source and dispatch mocks, Linux killed in both modes. Native Windows execution remains `chua_do_duoc`; this does not claim full native-platform class validation. No remaining no-op defect identified. |
| F04 P3 / `timing-receipt-validation` lexical residual | **ĐÃ VÁ THẬT** | All digit ranges ASCII, real writer accepted, three timing mutants killed in both modes; no new timing-validation defect found. |

One open root-cause class, five related manifestations described above. Historical F01 timing scenarios remain rejected by the real collector counterexamples. This verdict provides local review evidence; it does not certify launcher/provider attestation, remote CI, merge authority, or landing readiness.

Analysis completed UTC: 2026-10-22T07:52:58.687579+00:00

Final source check UTC: 2026-10-22T07:54:03.131399+00:00. Head, tree, parent and local origin/master still match. Detached check rc=1 as expected; all other Git commands rc=0. Tracked/untracked/ignored status empty; worktree/index diffs empty; delta `diff --check` clean. All **4839/4839** archive files/symlinks match the source checkout byte-for-byte / link-for-link. Receipt: `review-wp748-r22-round2-KsEuyd/final-identity.json`. These observations establish no final source delta; they do not independently monitor every historical filesystem access. Sandbox mode is workspace-write; review read-only scope was maintained by operating on the scratch archive.

Final status: complete; changes requested for continuing P2 F02. No P0/P1 findings.

VERDICT: changes_requested
