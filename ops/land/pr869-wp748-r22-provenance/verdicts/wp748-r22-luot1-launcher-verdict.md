# Independent review — WP748 r22, PR #869

Reviewer runtime identity: “Codex, an agent based on GPT-6.” OpenAI Codex is the reviewer requested by the user. No finer model identifier is exposed by the runtime instructions. I cannot independently attest to the claimed launcher.py run invocation or its external execution receipt from that claim alone.

Review started (UTC): 2026-10-22T07:13:34.774164+00:00

Reviewed head: `056b316c414d35791a6dce00532d4e905c9d17d8`  
Reviewed tree: `3719a976884a7b2a88aca3a5bc3b719f3936eca0`  
Sole parent: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`  
Local origin/master: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`  
HEAD detached: True. Identity verification: PASS.

Scope: `git -C src diff 9e9a74b 056b316`, expected only `ops/nhanh_don_duoc_test.py`. Source checkout is read-only for this review. Scratch archive copies and this report are the only intended writes. No credentials, remote fetch, commits, pushes, or GitHub comments.

Execution platform: Linux x86_64, Python 3.13.16. Windows can only be assessed by reading here.

Status: complete. Changes requested: two P2 findings (F02, F03) and one P3 format issue (F04). Original F01 P2 timing scenarios are fixed. Approval threshold: zero P0/P1/P2, as required by the user.

Archive created (UTC): 2026-10-22T07:14:36.543370+00:00. `git -C src archive --format=tar 056b316c414d35791a6dce00532d4e905c9d17d8` rc=0; extracted to `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22/review-wp748-r22-w0dxZK/head`. Reviewed file byte-identical to Git blob; SHA-256 `6f3497d130a6e081f427f35d9f118febf8f83f063cfa42a7dd87ac109fa83ef3`.

Started `product` at 2026-10-22T07:15:10.840346+00:00: `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py`.

Completed `product` at 2026-10-22T07:15:12.439062+00:00: rc=0. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22/review-wp748-r22-w0dxZK/product.log`.

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

Started `selfchecks` at 2026-10-22T07:15:12.439441+00:00: `NHANH_DON_DUOC_CHI_TU_KIEM=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py`.

Completed `selfchecks` at 2026-10-22T07:15:39.945298+00:00: rc=0. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22/review-wp748-r22-w0dxZK/selfchecks.log`.

```text
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

Started `five_mutants` at 2026-10-22T07:15:39.945879+00:00: `PYTHONUTF8=1 python3 /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22/review-wp748-r22-w0dxZK/five_mutants.py`.

Completed `five_mutants` at 2026-10-22T07:16:01.108937+00:00: rc=0. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22/review-wp748-r22-w0dxZK/five_mutants.log`.

```text
DOT BIEN TU KIEM moc-nhan-sai-dinh-dang | r554 | 1/1
DOT BIEN TU KIEM moc-bo-kiem-dao-nguoc | r554 | 1/1
DOT BIEN TU KIEM moc-bo-kiem-lech-giay | r554 | 1/1
DOT BIEN TU KIEM timeout-chi-giet-con | r555 | 1/1
DOT BIEN TU KIEM ghi-so-gop-dich | r546 | 1/1
FIVE MUTANTS: (5, 0, 0) 5/5 killed for declared target
```

Review checkpoint (UTC 2026-10-22): requested runs passed on Linux: product 8/8, self-checks 55/55, five targeted mutants 5/5 (all rc=0; individual mutant children rc=1 as required). The archive runner uses a minimal environment, UTF-8, bytecode disabled, and global/system Git configuration disabled; fixture operations are local only. No credentials are passed to this runner. Source scope confirmed: one file, 165 insertions / 8 deletions.

Cloud-runtime skill read as required by this environment. No environment_status tool is available in the tool catalog; no credential or secret inspection was attempted. Provider: OpenAI; system-reported surface: API. Observed transport: direct local tools (`functions.exec` / `exec_command`). Exact backend model slug, effort, parent launcher completion/exit status, and independent provider/session attestation are not exposed. This verdict makes no claim to establish the external receipt's assurance level.

Review in progress: inspecting remaining timeout containment and Windows drain paths despite passing baseline/mutation totals.

Additional timing probe: `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python3 review-wp748-r22-w0dxZK/probe_timing.py`, rc=0, writer/parser checks 46/46; collector matrix 46/46, with 3 valid controls. Writer probes call the real receipt writer and clocks while stubbing work results and head lookup; these are synthetic timing/schema checks, not actual full shard performance evidence.

First timeout probe attempt returned rc=1 due to a reviewer simulation setup error: transplanting CPython's Windows `_communicate` method also requires `_readerthread`. Ordinary Linux containment and the separate-session reproduction completed before that AttributeError. This is not a source failure; attempt log is preserved as `review-wp748-r22-w0dxZK/probe_timeout-attempt1.log`. Corrected simulation follows.

## Confirmed findings (recorded 2026-10-22T07:21:28.622296+00:00)

### WP748-R22-F02 — P2 — timeout-descendant-containment (continues WP748-R20-F02)

- Locations: `ops/nhanh_don_duoc_test.py:429` (best-effort Windows tree kill), `:434` (direct-child fallback), `:459` (synchronous pipe close after second timeout), `:416` (POSIX process-group-only termination).
- Scenario / impact: when Windows `taskkill /T /F` is absent, fails, or times out, the fallback only kills the direct child. Descendants retain fixture files and inherited stdout/stderr. After the bounded second `communicate`, `o.close()` has no deadline. CPython's Windows reader thread can still hold the buffered pipe's lock in `fh.read()`, so this close blocks until the descendant closes the pipe. A never-ending descendant can therefore still prevent return of rc 124 indefinitely. `CREATE_NEW_PROCESS_GROUP` is not a Windows Job Object and does not enforce tree lifetime. The existing measurement Job Object is not a per-run kill boundary. No termination verification is performed.
- POSIX scope: the ordinary same-group case is fixed and the own-group guard is explicit. However, a descendant that starts a new session escapes `killpg`. Executed probe: ordinary grandchild stopped, rc 124 in 0.503 s; separate-session grandchild kept updating its heartbeat after rc 124 at 0.752 s (configured run/drain budgets 0.5/0.25 s). Only probe-owned processes were signalled. This disproves the unconditional whole-descendant-tree claim; it is not evidence that every ordinary Git child detaches.
- Windows mechanism evidence: installed CPython 3.13.16 `/usr/lib/python3.13/subprocess.py:1615` reader thread and `:1624` Windows `_communicate` leave readers alive on timeout. Executing those exact methods on Linux pipes with a simulated failed tree kill produced return at 2.099 s for run/drain budgets totalling 0.75 s; return waited for the finite-lived grandchild to finish. This is a mechanism simulation, **not native Windows execution**. Corrected probe rc=0, 9/9 expectations including the two defect reproductions. Log: `review-wp748-r22-w0dxZK/probe_timeout.log`.
- Fix direction: use an owned, enforceable process-tree lifetime boundary (on Windows, a per-run Job Object established before descendants can spawn, with tree termination and bounded verification). Make output collection/abandonment bounded without synchronously closing a stream locked by a live reader. On POSIX either contain/track descendants that detach or explicitly enforce the narrower supported process model. Keep timeout non-passing and preserve rc 124 while reporting incomplete cleanup truthfully; handle kill failures without replacing the timeout result with an uncaught exception. Do not target the reviewer's or unrelated process groups.
- Regression / risks: test failed/unavailable/slow taskkill, a descendant retaining both pipes indefinitely, and a POSIX descendant in another session, under an external watchdog with owned-process cleanup. Verify no live owned descendants and bounded return. Preserve same-group and no-timeout positive controls. Job nesting, handle lifetime, PID reuse, and blocking reader cancellation need explicit coverage; merely adding another kill command is insufficient.

### WP748-R22-F03 — P2 — timeout-mutant-platform-coverage (new)

- Location: `ops/nhanh_don_duoc_test.py:5044`; Windows branch at `:425`; unconditional partition input at `:5721`.
- Scenario / impact: `timeout-chi-giet-con` changes only the POSIX `killpg(...)` line. Windows never executes that line: it takes `taskkill` followed by `p.kill()` in both original and mutant. On a healthy Windows baseline, `r555` therefore stays green under the mutant, its child exits 0, and the mutation gate rejects it (`child rc=0 != 1`). Both targeted and full mutation lists include it. A Windows cleanup failure making the baseline red would not constitute an intended mutant kill either.
- Evidence: original/mutant branch comparison by reading; a dispatch-only Windows mock produced identical original/mutant traces: taskkill, then child.kill, with taskkill rc=0. See `trace_mutants.log`. The Linux requested run killed the mutant correctly, which does not establish Windows mutation coverage.
- Fix direction: mutate the platform-independent tree-cleanup operation so the mutant reliably performs direct-child-only cleanup on each supported OS, or use platform-specific mutants with explicit platform coverage/accounting. Keep the real baseline requirement.
- Regression / risks: require the unmodified `r555` to pass and its timeout mutant to fail specifically at the stopped-heartbeat/containment check on native Windows and POSIX. Do not count unsupported-platform no-op mutants as killed or weaken the required mutation totals.

Final identity/source check at 2026-10-22T07:22:57.586222+00:00: head, tree, sole parent, and origin/master still match. Detached check rc=1 as expected; other Git checks rc=0. Tracked, untracked and ignored status empty; worktree/index diffs empty; `git diff --check` passed. All 4839 archived source entries byte/link-identical to `src/`. Command-level receipt: `review-wp748-r22-w0dxZK/final-identity.json`. This verifies the observed final source contents, not an independently monitored history of every filesystem access.

### WP748-R22-F04 — P3 — timing-receipt-validation (minor lexical residual)

- Location: `ops/nhanh_don_duoc_test.py:5932`, consumed at `:5941`.
- Scenario: replace only the year digits in an otherwise valid timestamp with equivalent non-ASCII decimal digits. The regex uses Unicode `\d`, and CPython's year parser also uses Unicode `\d` then `int`, so it accepts this representation although `_iso_utc` emits ASCII digits. It is the same semantic time, so this does not restore the original material elapsed-time bypass; it contradicts the stated exact writer-format contract.
- Evidence: source-derived, not an executed unusual-payload probe. Installed `/usr/lib/python3.13/_strptime.py:373` defines the four-digit year using `\d`; `:602` converts it with `int`. No unusual encoded payload is authored in this report or probe.
- Fix / regression: make the lexical check ASCII-only (`[0-9]` or the ASCII regex flag), retain a real `_iso_utc` positive control, and reject alternate digit alphabets. Risk is low because the real writer already emits ASCII. This is P3 and does not independently block the user's zero-P2 approval threshold.

## Timing assessment and prior-review comparison

| Earlier finding | Current assessment | Evidence / remaining scope |
|---|---|---|
| WP748-R20-F01, timing-receipt-validation | Original P2 scenarios **ĐÃ VÁ THẬT**; class retains minor P3 F04 | Invalid strings, reversed intervals, and materially inconsistent duration are rejected; the three respective mutants each expose exactly their intended counterexample. No crash in tested non-string timestamps or the existing very-large-integer duration counterexample. |
| WP748-R20-F02, timeout-descendant-containment | **VÁ HỜ** (partially fixed), remains P2 as WP748-R22-F02 | Same-process-group Linux descendant now stops; separate-session Linux descendant survives. Windows tree kill remains best effort and pipe close remains potentially unbounded. Native Windows unavailable. |

`_doc_moc_utc` rejects wrong types before applying its regex, checks the entire string, and lets the calendar parser reject impossible dates. The interval calculation is bounded by Python datetime's supported date range. The duration comparison uses inequalities instead of subtracting a JSON integer from a float, so a very large integer cannot overflow a float conversion here. Booleans and non-finite floats fail `_so_huu_han`. Ordinary malformed values return validation errors rather than throwing in the tested paths. This is not an exhaustive parser/resource-exhaustion audit of arbitrarily large JSON documents.

The real `_iso_utc` millisecond form is accepted. The writer probe exercised `chay_manh_dich` for all eight shards in both modes using the actual clock and serialization code; work-result and head-lookup seams were stubbed, so it supplies timing/schema evidence only. Parser/writer probes: 46/46 expectations met. Existing collector matrix: 46/46 (3 valid controls, 43 negative cases); these are distinct counts from the extra probe.

`LECH_MOC_GIAY = 5` is a declared tolerance, not a measured universal clock-error bound. Timestamp truncation and two-decimal duration rounding together need only roughly 0.006 seconds under an uninterrupted clock; 5 seconds comfortably accommodates those. Inclusive boundary probes passed at ±5 seconds and rejected ±5.001. Consequently a 545-second wall interval with `giay=540` is accepted, intentionally giving that much wall/monotonic slack. The 540-second performance limit remains on the monotonic-derived `giay`, not a strict wall-time ceiling.

A correct writer can still be rejected after a clock step larger than 5 seconds, or after a short run whose wall clock moves backward enough to reverse the timestamps. Arbitrary scheduling delay between the separate monotonic and wall-clock reads can also exceed a fixed tolerance. These are fail-closed measurement outcomes, not proof of a bad workload. Thus no blanket “all writer receipts always pass” claim is justified. Supporting such clock events while retaining reversed/inconsistent-receipt rejection requires additional clock-adjustment evidence or an explicit measurement policy; silently enlarging the tolerance would weaken validation. No new P2 timing bypass was found within the stated tolerance policy.

## Regression cases, mutants, and infrastructure-error accounting

- `r554` is a legitimate collector test. `_muc_dich` requires the complete self-check table to agree with `GIAY_CA_HO_SO`; `main` intentionally narrows `TU_KIEM` for a targeted child. Temporarily using `_TU_KIEM_DAY_DU` supplies the full partition universe expected by the collector, then restores the caller's table in `finally`. It does not replace the validator or force its outcome. It prevents an unrelated incomplete-partition exception from masquerading as a successful timing-mutant kill. This snapshot is test-scoped; it does not repair or hide production collector input. It is not independent evidence about arbitrary later changes to the global case list.
- Three timing mutants: diagnostic replay exposed exactly one accepted counterexample per mutant: malformed timestamps, reversed timestamps, and elapsed-vs-duration mismatch respectively. The valid controls remained valid. The requested runner separately observed the declared `r554` assertion failure, rc 1, and completion proof for each.
- `r555` passes for the ordinary same-group Linux child/grandchild. Under `timeout-chi-giet-con`, a diagnostic replay recorded its four assertions as `[true, true, true, false]`: timeout rc/marker, elapsed bound, and fixture existence passed; the stopped-heartbeat check failed. Thus the Linux kill is for the intended reason. Its current coverage does not establish all-descendant containment or Windows failure-path boundedness, and the mutant is ineffective on Windows (F03).
- `_loi_gop_dich` recording caught `OSError` via `_ghi_ha_tang` is correct. A receipt read failure is an infrastructure failure even if the collector returns an error list; otherwise `r554` can turn an unreadable valid control into an ordinary assertion failure. Malformed JSON remains a `ValueError` validation error. The shared ledger preserves classification through copied modules. Removing the new ledger call made `r546` fail specifically because `r554`, under injected read errors, produced `DO_CHOT` instead of the required infrastructure diagnosis. Captured child output reports `r554(tiem=47)`, not a random unrelated case. Its mutant was killed 1/1 as intended.
- `_TRAN_GIAY_CON is None` retains the previous `subprocess.run` arguments and `check` wrapper; omitting explicit `timeout=None` is equivalent. Additional executed controls verified normal stdout/rc 0, nonzero rc with `check=False`, and assertion with `check=True`: 3/3. Process-group guard stubs verified dedicated-group kill, refusal to kill the own group, and mismatched-group fallback: 3/3. No signal was sent to the reviewer's group. Timeout rc 124 was observed in the normal and residual Linux scenarios; it is not guaranteed if cleanup blocks or an unhandled kill error escapes.

## Completed execution receipt

All requested suites ran from the exact-head `git archive` copy. Logs and scratch scripts are under `review-wp748-r22-w0dxZK/`. No source patch, source commit/push, GitHub comment, credential use, or network fetch was performed. The required tests create their own local fixture repositories and fixture commits as part of their normal execution; no reviewed-repository commit was made.

| Command / scope | rc | N/N / result |
|---|---:|---|
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py` | 0 | **8/8** product cases |
| `NHANH_DON_DUOC_CHI_TU_KIEM=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py` | 0 | **55/55** self-checks |
| `PYTHONUTF8=1 python3 ../five_mutants.py` (absolute path recorded above), calling `chay_dot_bien_tu_kiem(muc=[the five requested entries], chi_dich=True)` | 0 | **5/5** killed; 0 incorrect, 0 unmeasured; each child rc 1 |
| `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python3 review-wp748-r22-w0dxZK/probe_timing.py` | 0 | **46/46** additional checks; existing collector matrix **46/46** |
| `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python3 review-wp748-r22-w0dxZK/probe_timeout.py` (corrected harness) | 0 | **9/9** expectations, including successful defect reproductions; not 9 passing product guarantees |
| Same timeout probe, first harness attempt | 1 | Reviewer setup error (missing transplanted reader method); preserved separately, not credited as a source failure or pass |
| `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python3 review-wp748-r22-w0dxZK/trace_mutants.py` | 0 | **5/5** cause/dispatch checks; confirms three isolated timing failures, the Linux heartbeat failure, and identical Windows original/mutant dispatch |
| Final Git identity, status, worktree/index diff and diff whitespace checks | 0 (detached check 1 expected) | Exact requested identity; clean; **4839/4839** archived source entries unchanged |

Requested-suite UTC intervals: product 07:15:10.840346–07:15:12.439062; self-checks 07:15:12.439441–07:15:39.945298; five mutants 07:15:39.945879–07:16:01.108937, all on 2026-10-22. Full command/time/rc data: `requested-results.json`. Final identity receipt: `final-identity.json`.

Not run: native Windows, the complete mutation catalog, real full-shard performance audit, full repository/release gates, or remote PR/CI readback. Those are not counted as passes. Windows findings are based on source inspection plus explicitly labelled mechanism/dispatch simulations. `launcher.out` and `launcher.err` remained empty when inspected; the enclosing launcher's eventual receipt and exit status must be verified outside this still-running child review.

Review completed (UTC): 2026-10-22T07:24:54.880468+00:00. Open findings: P0=0, P1=0, P2=2, P3=1.

VERDICT: changes_requested
