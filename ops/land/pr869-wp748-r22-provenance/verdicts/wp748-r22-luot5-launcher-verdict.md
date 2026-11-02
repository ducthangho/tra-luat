# WP748 r22 — PR #869 — round 5 independent read-only re-review

Review complete: **approve**. No open P0/P1/P2 findings in the requested delta and narrowed contract. Incremental execution evidence is retained below.

- Reviewer: OpenAI Codex, as designated by this session's runtime instructions (GPT-6 family). Exact backend model/build and the external `launcher.py run` receipt/authenticity are not independently verifiable from the supplied context. System-reported surface: API; observed transport: direct local tools (`functions.exec` / `exec_command`). Exact backend model slug/effort and independent session/provider attestation are unavailable. This is not a human-mediated ChatGPT Web review; no GitHub submitter exists because nothing is published.
- Execution: local shell tool, Linux 6.18.44-fc-v140 x86_64, Python 3.13.16. No credentials or connected-service/repository API calls used. Public Microsoft platform documentation was consulted without authentication.
- UTC start: 2026-10-22T10:52:13Z.
- Reviewed SHA: `b9318cc26101d2697be19ac44be5700534ba0256`.
- Reviewed tree: `e499945931af024dbd3b2144c5a30c3788e095ab`.
- Identity preflight: HEAD/tree match; `git symbolic-ref -q HEAD` returns 1 (detached); `git status --short` is empty.
- Previous reviewed SHA: `6e96fefa2353158ba4b9eb405923c044922b56c6`.
- Supplied base: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`. Local `origin/master` actually resolves to `c73af7b0ba751bfbb974f5ba11147ccb555015dc`; the review uses the explicitly requested immutable delta and does not update refs.
- Delta: only `ops/nhanh_don_duoc_test.py`, two commits (`57c54ae3bc79928202afe2993c1bec4ff224395c`, `b9318cc26101d2697be19ac44be5700534ba0256`), 123 insertions / 35 deletions.
- Scope: owner's option (b), narrowed timeout contract; escaped POSIX descendants alone are out of scope. `src/` is read-only. Test runs and probes will use an archive copy under this directory.

## Execution evidence (incremental)

Identity commands above succeeded (rc 0), except the expected detached symbolic-ref result (rc 1). Test results and findings pending.

Archive: `git -C src archive --format=tar b9318cc26101d2697be19ac44be5700534ba0256` rc=0; extracted to `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22e/review-round5-9QNQbs/head`. Reviewed-file SHA-256 `3c1d6c6a730716e8c4ccfc18920f17586056881d877cefe24ea93310b5bdac88`.

Started `product` UTC 2026-10-22T10:54:21.601796+00:00: flags `{'NHANH_DON_DUOC_KHONG_DOT_BIEN': '1'}`, argv `['/usr/bin/python3', 'ops/nhanh_don_duoc_test.py']`, cwd archive, clean credential-free environment, watchdog 120s.

Completed `product`: rc=0, 1.872s, totals `['8/8']`, log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22e/review-round5-9QNQbs/product.log`.

Started `self` UTC 2026-10-22T10:54:23.473897+00:00: flags `{'NHANH_DON_DUOC_CHI_TU_KIEM': '1'}`, argv `['/usr/bin/python3', 'ops/nhanh_don_duoc_test.py']`, cwd archive, clean credential-free environment, watchdog 180s.

Completed `self`: rc=0, 55.355s, totals `['TU KIEM: 56/56']`, log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22e/review-round5-9QNQbs/self.log`.

Started `targeted` UTC 2026-10-22T10:55:18.829638+00:00: flags `{}`, argv `['/usr/bin/python3', '/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22e/review-round5-9QNQbs/mutants.py', 'targeted']`, cwd archive, clean credential-free environment, watchdog 180s.

Completed `targeted`: rc=0, 8.706s, totals `['MUTANTS chi_dich=True: 11/11']`, log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22e/review-round5-9QNQbs/targeted.log`.

Started `full` UTC 2026-10-22T10:55:27.536303+00:00: flags `{}`, argv `['/usr/bin/python3', '/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22e/review-round5-9QNQbs/mutants.py', 'full']`, cwd archive, clean credential-free environment, watchdog 900s.

## Review checkpoint — round-4 reconciliation

Independent API/I/O probes: **78/78**, rc=0 (`review-round5-9QNQbs/probes.py`, results in `probe-results.json`); extra controls **3/3**, rc=0 (`extra_probes.py`). Actual fixture cause replay: **12/12** intended assertion failures across the 11 selected mutants (`trace_causes.py`, `cause-results.json`). These are separate from product/self-suite counts and do not constitute native Windows execution. Full-radius mutation execution is still running.

All line references below are in `ops/nhanh_don_duoc_test.py` at the reviewed SHA.

| Round-4 F02 row / severity | Status | Independent evidence on round 5 |
|---|---|---|
| Unbounded Windows `taskkill` recovery, old :488 — P2 | **Closed** | :483–493 use `TerminateJobObject`, then direct-child kill with a diagnostic on false/Exception. No auxiliary subprocess is called. 24 API-outcome combinations exercise successful/false/throwing termination, successful/denied direct kill, and successful/timed-out/erroring drains. Every case returns 124, uses drain timeout 5.0, and attempts one actual job-handle close. |
| Cleanup exception hides kill failure, omits POSIX exclusion, and claims child killed, old :569/:572/:579 — P2 | **Closed** | :522–528 distinguish kill request from OSError; :575–578 retain cleanup failure and append the POSIX exclusion; :585–586 no longer assert that the child died. 16 POSIX/Windows cleanup-exception combinations preserve rc124 and truthful kill/drain diagnostics. Ten group-operation controls confirm own-group selection, caller/different-group refusal, getpgid/killpg failure reporting and direct-kill outcomes. |
| Suspended-child wait OSError / second-drain error replace rc126/124, old :532–533/:575–576 — P2 | **Closed** | :538–542 return a wait-error diagnostic with rc126; :580–584 catch ordinary drain Exceptions while preserving rc124. Wait success/timeout/OSError controls pass, and the matrices include OSError and ValueError drain failures. No `BaseException` catch was introduced. |
| Popen exception loses failed-close diagnostic, old :580–584 — P2 | **Closed** | :587–596 transfer job ownership to `ve_nem`, close once, attach a CloseHandle note, then re-raise the same spawn exception. Nine normal/timeout/spawn-error × close-success/false/Exception controls confirm one underlying `CloseHandle` attempt and visible failure diagnostics. |

Documentation discrepancies from round 4 are repaired: check=False is explicit at :407–408 (both check modes independently exercised); the exclusion at :413 covers leaving the group via setsid/setpgid; :419–421 condition tree termination on successful close; :466–467 return cleanup responsibility to the caller; :582 states observable drain/wait incompletion; :4327 qualifies the heartbeat claim as before teardown; :5858–5860 identify the CI cause as an unverified hypothesis and place temporary-directory exit before totals/proof. Literal `con bi giet` still appears in fixture prose and negative checks; it no longer appears as the runner's unconditional timeout-result claim. The user's literal “nowhere” wording is therefore broader than the source change, without recreating the old false diagnostic.

F05 (P3, :5801–5802) **remains closed**: the extra probe used the actual mutant grader with valid completion proof, rc1 and the expected assertion set; it returned `(1, 0, 0)` and forwarded the cleanup warning. This does not verify the historical CI root cause.

Eight `KeyboardInterrupt` controls (spawn, initial/second drain, tree cleanup, job termination, direct kill, suspended-child wait, close) propagate the original interrupt and attempt one job close; no interrupt is converted to rc124/126. Eight create/set/assign/resume false/Exception controls fail closed with rc126, no spawn after create/set failure, and no resume after failed assignment. The spawned Windows child carries CREATE_SUSPENDED and successful assignment precedes resume. All are in-memory API mocks of the reviewed implementation.

No new P0/P1/P2 defect has been established at this checkpoint. Detached POSIX descendants remain outside the owner's narrowed contract; their survival is not a finding.

## Mutant soundness and platform reasoning

Selection is mechanical: every entry in `DOT_BIEN_TU_KIEM` whose declared targets intersect `{r555, r556}` — **11 entries**. Each uses the catalog's existing anchor/replacement on a scratch copy; the actual grader verifies unique anchor, child rc1, valid completion proof, no DO_KHAC and an exact declared assertion-failure set. Targeted mode passes **11/11**, with 12/12 declared target failures. Full mode is separately required to detect collateral failures; its final results will follow.

| Mutant | Declared radius | Intended defect actually detected in independent cause replay; line in reviewed source | Windows reasoning |
|---|---|---|---|
| `timeout-chi-giet-con` | r555, r556 | r555 :4382 fails the 4.5-second same-group bound: direct-child kill leaves the pipe-holding grandchild until the five-second drain expires. r556 (c2) :4526 fails missing cleanup/exclusion diagnostics, after the rc124 assertion already passed. `_giet_truc_tiep` handles the injected kill OSError; there is no longer credit from bare `q.kill()` throwing into the outer handler. | Same r556 mock cause. For r555, the grandchild remains in the job until the final close, which occurs after the five-second drain; final job close may stop its heartbeat but cannot repair the already-exceeded 4.5-second bound. |
| `con-treo-wait-loi-thoat` | r556 | (b4) :4488 fails because wait OSError escapes and the fixture sets `p=None`, instead of receiving rc126 with `cho LOI`. | The fixture patches platform/Popen and uses the same failing wait on either host. |
| `popen-nem-mat-ghi-chu-dong` | r556 | (b5) :4503 fails because the original spawn exception has no CloseHandle note. Closing still happens, so this specifically measures diagnostic preservation. | Same ordinary exception/notes semantics; repository CI uses Python 3.12, where `add_note` is available. |
| `don-cay-nem-thieu-ngoai-hop-dong` | r556 | (c2) :4526 fails because the POSIX exclusion is missing while rc124 and other error diagnostics survive. | c2 explicitly simulates POSIX with fake Popen/cleanup; it also runs on Windows. No real POSIX API is invoked in this cell. |
| `thu-output-loi-thoat` | r556 | (c2) :4525 fails because second-drain OSError escapes, replacing rc124. | Same explicit mock path on either host. |
| `ket-thuc-goi-taskkill` | r556 | (w) :4536 detects the inserted helper invocation through the recorded call list. The mocked helper returns normally; credit is not from FileNotFoundError or a native helper failure. (Inserted source is one line longer, so trace records :4537.) | Same actual `_VeWindows.ket_thuc` with fake DLL/child and intercepted helper. This locks the chosen no-helper regression invariant; it does not itself reproduce or time a native Windows hang. |
| `windows-popen-nem-ro-job` | r556 | (b3) :4475 sees zero close calls after the spawn error. The replacement omits the exceptional close after ownership was transferred away from `ve`; `finally` cannot repair it. | Same fake spawn/owner-count assertion on either host. Normal r555 timeout still has its unaffected final-close path. |
| `con-treo-cho-khong-han` | r556 | (b) :4466 detects `wait(None)` instead of `wait(5.0)` after a failed assignment. The fake wait returns immediately, so this proves the missing timeout argument rather than measuring a hang. | Same mock assertion; the corresponding native wait would lack the explicit bound. |
| `windows-khong-job-van-chay` | r556 | (a) :4459 detects removal of the unusable-job admission guard: the fake child is created instead of returning rc126 without spawning. | Measures the no-spawn invariant. The real later assignment guard remains, so this mutant name/kill is not evidence of a native child executing outside a job. |
| `windows-gan-hong-van-chay` | r556 | (b) :4459 detects suppression of the failure branch after assignment/resume failure; fake communicate runs instead of rc126 recovery. | Measures fail-closed handling. A genuinely failed native assignment still leaves the child suspended; this test does not demonstrate execution outside a job. |
| `don-cay-nem-thay-124` | r556 | (c2) :4525 detects the escaping cleanup RuntimeError, replacing the timeout result. It now fails before the later live (c) sleep fixture. | Same platform-independent mocked cause; no collateral native child is needed for this kill. |

Every cause above is an intended `TinHieuChotCa`, not DO_KHAC. Full-radius expectations on Windows are the same declared sets: all ten r556-only changes target paths activated by its explicit failure mocks, and the common timeout-call mutation also affects live r555. This is static reasoning, not a claim that native Windows full-radius tests passed.

Windows control-flow reasoning uses the actual reviewed order: create/configure job → spawn suspended → assign → resume. CREATE_SUSPENDED prevents the primary thread from running until resumed; the mutation delta adds no earlier resume operation. [Microsoft process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags).

Ordinary CreateProcess descendants inherit job association unless breakaway is enabled; this code enables kill-on-close, not breakaway. Creating a new process group does not itself request job breakaway. Closing the final kill-on-close job handle terminates associated processes; successful TerminateJobObject covers associated processes and nested jobs. These facts support the r555 Windows inference and the failure-path review, not a general arbitrary-code containment claim. [Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects), [Microsoft TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject).

Hostile scenarios, in words: a child outlives the configured timeout while its descendant keeps an output pipe open; the descendant changes group/session or is orphaned; job creation/configuration/assignment/resume/termination/close fails; direct kill is denied; output collection or wait raises; an interrupt arrives during recovery. Live runs reuse repository fixtures. Added probes only substitute in-memory API/I/O outcomes; no unusual payload or replacement `taskkill` executable was authored.

## Prior finding classes carried forward

- **F02 overall:** round-4 P2 manifestations are closed on the evidence above. The old detached-POSIX containment demand remains retired by option (b). The removed scanners/PID-identity assembly remain absent; r555 teardown still uses a stop-file request, not numeric-PID signalling. No new unbounded Python wait/drain or out-of-job Windows resume path was found in this delta.
- **F03:** remains closed. The shared call-site mutation has both targets, and c2 now rejects missing contract diagnostics rather than accidentally crediting a thrown bare-kill error.
- **F04:** unchanged by this delta; r554 passes in the complete self suite. No new full timestamp-mutant audit is claimed.
- **F05:** remains closed, with a fresh credited-result warning-forwarding probe.

The unchanged default `_TRAN_GIAY_CON=None` path is outside the activated timeout contract. `check=True` deliberately raises for rc124/126; the returned-result guarantees apply with `check=False`. Interrupts propagate; close-failure notes were measured on ordinary Exception exits, not asserted for every BaseException combination.

Completed `full`: rc=0, 584.447s, totals `['MUTANTS chi_dich=False: 11/11']`, log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22e/review-round5-9QNQbs/full.log`.


## Final execution results

All requested Linux runs completed with rc=0. Product/self selectors were passed exactly as requested; mutant runs called the reviewed `chay_dot_bien_tu_kiem(muc=[entry], chi_dich=...)`, once per selected entry in each mode. Full mode executed the complete 56-case self suite for every mutant. **22/22 mutant executions** were credited with exact target sets, child rc1, valid completion proof, and zero DO_KHAC.

| Command (cwd: archive `head/`) | Actual rc | Positive evidence | Seconds |
|---|---:|---|---:|
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 /usr/bin/python3 ops/nhanh_don_duoc_test.py` | 0 | **8/8** | 1.872 |
| `NHANH_DON_DUOC_CHI_TU_KIEM=1 /usr/bin/python3 ops/nhanh_don_duoc_test.py` | 0 | **TU KIEM: 56/56** | 55.355 |
| `/usr/bin/python3 ../mutants.py targeted` | 0 | **MUTANTS chi_dich=True: 11/11** | 8.706 |
| `/usr/bin/python3 ../mutants.py full` | 0 | **MUTANTS chi_dich=False: 11/11** | 584.447 |

The launcher for these commands is `review-round5-9QNQbs/setup_and_run.py` (overall rc=0). It supplies a clean environment: PATH=/usr/bin:/bin, LANG/LC_ALL=C.UTF-8, PYTHONDONTWRITEBYTECODE=1, PYTHONUNBUFFERED=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1, GIT_TERMINAL_PROMPT=0 and a scratch TMPDIR. No credential variables are inherited. Existing suite fixtures create commits and push to temporary local bare repositories; no reviewed-source commit, remote push, or GitHub comment was made.

| Mutant | Declared = actual failed cases, both modes | Targeted target failures | Full target failures | Full child total |
|---|---|---:|---:|---:|
| `timeout-chi-giet-con` | r555, r556 | 2/2 | 2/2 | 54/56 |
| `con-treo-wait-loi-thoat` | r556 | 1/1 | 1/1 | 55/56 |
| `popen-nem-mat-ghi-chu-dong` | r556 | 1/1 | 1/1 | 55/56 |
| `don-cay-nem-thieu-ngoai-hop-dong` | r556 | 1/1 | 1/1 | 55/56 |
| `thu-output-loi-thoat` | r556 | 1/1 | 1/1 | 55/56 |
| `ket-thuc-goi-taskkill` | r556 | 1/1 | 1/1 | 55/56 |
| `windows-popen-nem-ro-job` | r556 | 1/1 | 1/1 | 55/56 |
| `con-treo-cho-khong-han` | r556 | 1/1 | 1/1 | 55/56 |
| `windows-khong-job-van-chay` | r556 | 1/1 | 1/1 | 55/56 |
| `windows-gan-hong-van-chay` | r556 | 1/1 | 1/1 | 55/56 |
| `don-cay-nem-thay-124` | r556 | 1/1 | 1/1 | 55/56 |

The mutant child totals intentionally contain failed target cases; they are not failing baseline suites. Detailed machine-readable records: `run-results.json`, `targeted-results.json`, `full-results.json`, and all 22 `*-child.log` files under `review-round5-9QNQbs/`.

| Additional command (cwd: this review directory; same credential-free controls) | Actual rc | Evidence |
|---|---:|---|
| `python3 review-round5-9QNQbs/probes.py` | 0 | **78/78** API/I/O lifecycle expectations; `probe-results.json` |
| `python3 review-round5-9QNQbs/extra_probes.py` | 0 | **3/3** F05 warning and check-mode expectations; `extra-probe-results.json` |
| `python3 review-round5-9QNQbs/trace_causes.py` | 0 | **12/12** intended target assertion traces; `cause-results.json` |
| `python3 review-round5-9QNQbs/final_verify.py` | 0 | Exact HEAD/tree, detached state, clean status, source/archive contents; `final-identity.json` |
| `git -C src diff --check 6e96fefa2353158ba4b9eb405923c044922b56c6 b9318cc26101d2697be19ac44be5700534ba0256` | 0 | No whitespace errors |

## Final integrity, limits and finding status

At **2026-10-22T11:05:07.358817+00:00**, HEAD/tree still exactly matched the requested identity; symbolic-ref rc=1 confirmed detached HEAD. Tracked, untracked and ignored status was empty; working/index diffs rc=0; supplied immutable base is an ancestor (rc=0). **4839/4839 files/symlinks in each of `src/` and the test archive matched the reviewed Git archive byte-for-byte or by symlink target.** This verifies observed start/end content, not an independently monitored filesystem-access history. Runtime sandbox mode permits workspace writes; read-only treatment of `src/` was maintained by the operations used.

Native Windows execution is **not_run**; Windows conclusions comprise code review, documented API semantics and explicitly identified mocks. Other catalog mutants, full repository/release gates, actual performance shard executions, external PR/CI state and the historical CI traceback were **not_run/not_verified**. No new hostile executable/payload was authored. The `origin/master` mismatch is disclosed; it does not change the explicitly requested immutable SHA-to-SHA delta.

Reviewer identity is runtime-reported OpenAI Codex/GPT-6 via API/local tools. Exact backend model/effort, independent provider/session attestation and the enclosing `launcher.py run` receipt remain **not independently verifiable** here. `launcher.out` and `launcher.err` were empty at initial inspection and at 2026-10-22T11:04:43Z; the final enclosing receipt is produced outside this review's observation. Nothing in this verdict asserts external publisher/merge authority.

**Finding status:** F02 P2 **closed** for all round-4 rows within option (b); F05 P3 **remains closed**; F03 remains closed; F04 unchanged with r554 passing. **New findings: none. Open P0=0, P1=0, P2=0, P3=0.** No remediation is requested. Approval is limited to the reviewed delta/contract and the disclosed execution evidence.

Review completed UTC: **2026-10-22T11:06:13.205492+00:00**.

VERDICT: approve
