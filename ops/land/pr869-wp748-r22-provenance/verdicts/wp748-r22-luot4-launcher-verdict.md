# Independent read-only re-review — WP748 r22, PR #869, round 4

Reviewer identity reported by runtime: “Codex, an agent based on GPT-6.” Provider: OpenAI; system-reported surface: API; observed transport: direct local tools (`functions.exec` / `exec_command`). Exact backend model slug, effort, and independent provider/session attestation are unavailable. The user reports `launcher.py run`; this review cannot independently attest the enclosing launcher invocation or its final execution receipt.

Reviewed SHA: `6e96fefa2353158ba4b9eb405923c044922b56c6`  
Reviewed tree: `045c3b1b1ba270b90fd319621d7d7908bcdbc1e9`  
Round-3 comparison: `c435b790a4c026174e40e54c9738bb462a6c482e`  
Stated base: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`.

Identity checks PASS: exact HEAD/tree match, detached HEAD (`symbolic-ref -q HEAD` rc=1), status empty. Local `origin/master` resolves to `c73af7b0ba751bfbb974f5ba11147ccb555015dc`. No refs fetched or changed. Review is anchored to the immutable SHAs above.

Scope: owner-selected option (b), bounded timeout return, own POSIX group / Windows job, truthful exclusions, Windows failure handling, cleanup exceptions, F05, and the six requested mutants. Detached POSIX descendants alone are explicitly outside this contract. No source writes, commits, pushes, GitHub comments, or credential use. The cloud-runtime skill was read; its environment_status tool is unavailable. Windows cannot be run here; any Windows conclusions are static reasoning or clearly marked mocks.

Status: review in progress.

Started UTC: 2026-10-22T10:17:28.438808+00:00

Platform: Linux-6.18.44-fc-v140-x86_64-with-glibc2.39; Python 3.13.16.

Archive created UTC 2026-10-22T10:18:41.934323+00:00: `git -C src archive --format=tar 6e96fefa2353158ba4b9eb405923c044922b56c6`, rc=0; extracted to `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22d/review-wp748-r22-round4-nK4LuP/head`. Reviewed-file SHA-256 `668c6e235e4fc03387a086d672f56858284b05f29bd5571ab9a89c7f9370e1a9`.

Started `product` UTC 2026-10-22T10:18:42.048132+00:00: `{'NHANH_DON_DUOC_KHONG_DOT_BIEN': '1'} ['/usr/bin/python3', 'ops/nhanh_don_duoc_test.py']`; archive cwd, minimal credential-free environment; watchdog 120s.

Completed `product`: rc=0, 1.722s, totals ['8/8']; log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22d/review-wp748-r22-round4-nK4LuP/product.log`.

Started `self` UTC 2026-10-22T10:18:43.772047+00:00: `{'NHANH_DON_DUOC_CHI_TU_KIEM': '1'} ['/usr/bin/python3', 'ops/nhanh_don_duoc_test.py']`; archive cwd, minimal credential-free environment; watchdog 180s.

Completed `self`: rc=0, 55.486s, totals ['TU KIEM: 56/56']; log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22d/review-wp748-r22-round4-nK4LuP/self.log`.

Started `targeted` UTC 2026-10-22T10:19:39.259645+00:00: `{} ['/usr/bin/python3', '/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22d/review-wp748-r22-round4-nK4LuP/mutants.py', 'targeted']`; archive cwd, minimal credential-free environment; watchdog 240s.

Completed `targeted`: rc=0, 10.357s, totals ['MUTANTS chi_dich=True: 6/6']; log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22d/review-wp748-r22-round4-nK4LuP/targeted.log`.

Started `full` UTC 2026-10-22T10:19:49.618827+00:00: `{} ['/usr/bin/python3', '/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22d/review-wp748-r22-round4-nK4LuP/mutants.py', 'full']`; archive cwd, minimal credential-free environment; watchdog 700s.

Review checkpoint: product **8/8**, self **56/56**, targeted mutants **6/6**. Full mode is running. `probes.py` completed **25/25 expectations**, including deliberate defect reproductions (not 25 correctness guarantees). All API calls and signals in these probes are mocked.

Continuing **F02 (P2), now strictly within option (b)**: the cleanup-exception path omits `NGOAI_HOP_DONG_POSIX`, suppresses an emergency direct-child kill error, and still prints `con bi giet`; a suspended-child wait OSError escapes instead of rc126; a post-timeout drain OSError escapes instead of rc124; `Popen` plus `CloseHandle` failure calls close but hides its diagnostic on the propagating-exception path. Ordinary create/set/assign/resume false returns and exceptions pass the rc126 controls. F05's warning-forwarding probe now passes with a credited `(1, 0, 0)` result.

Checkpoint UTC: 2026-10-22T10:22:30.890484+00:00

Completed `full`: rc=0, 314.427s, totals ['MUTANTS chi_dich=False: 6/6']; log `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22d/review-wp748-r22-round4-nK4LuP/full.log`.

## Finding: WP748-R22-F02 — P2 — partially repaired; still open under option (b)

The removed POSIX descendant scan is **not** a remaining defect. This finding now concerns bounded return, exception-result preservation, and truthful failure reporting, all explicitly retained by the narrowed contract. The following are manifestations of the continuing finding, not a demand to restore full POSIX containment.

| Location in `ops/nhanh_don_duoc_test.py` | Scenario and observed result | Required fix direction |
|---|---|---|
| **:488** (`_VeWindows.ket_thuc`) | `TerminateJobObject` fails, then the `taskkill` helper times out. `subprocess.run(timeout=5)` enters its Windows timeout recovery and calls **`communicate()` without a timeout**. The mock recorded `communicate(5.0) → kill → communicate(None)`. If a helper descendant retains a captured pipe, this path has no return bound and the enclosing job-close `finally` is never reached. | Prefer removing the process-tree helper fallback and report failed job termination, then close the owned job. If a helper is retained, its entire spawn/termination/drain lifecycle needs bounded handling; a `subprocess.run` timeout alone is insufficient. |
| **:569, :572, :579** (`run`) | On POSIX, `_ket_thuc_cay` throws; the emergency direct-child kill also fails with OSError. The kill error is discarded, the required `NGOAI_HOP_DONG_POSIX` text is absent, and stderr still says **`con bi giet`** (“child killed”). rc124 survives, but the claim is false and a failure is hidden. Even when emergency kill succeeds, the cleanup-exception branch omits the required POSIX exclusion. | Build the platform exclusion independently of cleanup success; retain each failure diagnostic; distinguish attempted kill, failed kill, and confirmed termination. Do not emit unconditional success wording. |
| **:532, :533; :575, :576** (`_giet_con_treo`, `run`) | After failed Windows assignment, a bounded `wait()` that raises OSError escapes instead of producing rc126. After an initial timeout and cleanup exception, an OSError in the second `communicate()` escapes instead of producing rc124 with `LOI don cay`. Both paths were reproduced with API/I/O mocks; no claim is made about their native frequency. | Preserve the established 126/124 outcome across ordinary cleanup/wait/drain exceptions and add the new failure to the diagnostic. Keep timeout limits and avoid synchronous closure of reader-owned pipes. |
| **:580–584** (`run`) | A `Popen` exception does now call `ve.dong()`. But if `CloseHandle` also returns false or throws, the error is saved only in `ve.loi`; propagation of the spawn exception skips :583–584. The caller receives only the spawn error, without a note or emitted close-failure diagnostic. Both forms were reproduced. | Report close failure on the exceptional exit as well, for example by attaching it to the propagating exception or an explicit diagnostic sink inside protected finalization. Preserve the original spawn error. |

The helper timeout finding is about a reachable **untimed wait**, not a measured native Windows hang. Hostile-input scenario, in words only: a program found as `taskkill` through PATH starts a descendant that retains its captured output handle; killing that helper does not yield pipe EOF. No such executable or payload was authored. The replay executed Python's actual Windows branch of `subprocess.run` with an in-memory `Popen` substitute. The untimed recovery also appears in [CPython 3.13.16's implementation](https://github.com/python/cpython/blob/v3.13.16/Lib/subprocess.py). Python documents that a `run` timeout includes killing and waiting, and that process creation itself is not generally interruptible. [Python subprocess documentation](https://docs.python.org/3.13/library/subprocess.html).

Regression requirements and repair risks:

- For :488, model failed job termination plus helper timeout/retained output; fail any untimed drain or wait. Removing the fallback reduces cleanup attempts after a job API failure, so report that limitation and still attempt job close. Replacing it must not introduce another helper outside the required lifetime/boundary control.
- For :569–579, pair a successful cleanup control with cleanup-throw/kill-denied and cleanup-throw/drain-error cases on both platforms. Assert exact rc, the POSIX exclusion when applicable, and visible failure details. Over-broad exception handling must not turn a cleanup failure into a claimed success or swallow process-control exceptions such as KeyboardInterrupt.
- For :532, model wait success, TimeoutExpired, and OSError after failed assignment/resume. All ordinary failure outcomes must remain bounded and diagnosed as rc126. Avoid accidentally resuming the suspended process during recovery.
- For :580–584, cross spawn success/failure with close success/false/exception. A failed close must remain externally visible in every cell. Preserve the primary error and avoid blind double-closing of a handle whose lifetime is uncertain.

These probes are in `review-wp748-r22-round4-nK4LuP/probes.py` and `fallback_probe.py`. They alter neither reviewed source nor real OS process identities.

## Narrowed contract assessment and documentation truthfulness

1. **Bounded rc124 return: not universal.** The main POSIX timeout path and normal Windows job path have a five-second post-kill drain limit. The Windows helper recovery above has an untimed drain, and ordinary drain errors can replace rc124. Also, the existing `check=True` API (the default) raises `AssertionError` at :585–586 for rc124; a mock confirmed it. The “returns / does not throw” comments at :401–408 must explicitly state the `check=False` convention, or the implementation must honor the owner's literal unconditional-return requirement. This pre-existing check convention is separate from the demonstrated failures with `check=False`.
2. **Own-group/job boundary: normal paths are sound.** POSIX creates a fresh session, checks `pgid == child pid` and `pgid != caller pgid`, then sends only that group SIGKILL. The removed scanners, PID/starttime helpers, and PID-file teardown cannot select unrelated identities anymore. The Windows normal path creates an unnamed, non-inheritable job, configures kill-on-close, creates suspended, assigns, resumes, and terminates/closes the job. I found no ordinary path that resumes the initial child outside a successfully assigned job. The `taskkill /T` fallback is a separate ancestry-based mechanism, not a job-membership operation; its own native selection safety was not measured, and it should not be described as enforcing the job boundary.
3. **Truthful POSIX exclusion: incomplete.** Normal group success and handled getpgid/killpg OSError paths include `NGOAI_HOP_DONG_POSIX`. The outer cleanup-exception path does not. The unconditional “child killed” line is not justified when killing failed or the bounded wait/drain did not establish exit. The string correctly disclaims detached `setsid` descendants on the normal path; the actual positive guarantee is only the original process group, so it should not imply coverage of a descendant that changes process group within the same session either. Such descendants surviving are **not** raised as a containment defect.
4. **Windows failure handling: substantially repaired, not complete.** Eight controls (create/set/assign/resume × false/error outcome) returned 126 as appropriate; create/set failure did not spawn, assign/resume failure did not communicate or resume further, and the caller killed and waited with timeout 5.0. A kill OSError was reported with rc126; a wait timeout was reported with rc126. `Popen` failure closes the job; normal-return CloseHandle false/exception is reported. The wait-error and exceptional-close-reporting holes above remain.
5. **Cleanup exception → rc124 with `LOI don cay`: passes the supplied r556 scenario, not all cleanup paths.** Initial cleanup exceptions are handled, but an error in the subsequent drain still escapes. The false killed claim and missing POSIX exclusion remain even in some rc124 outcomes.

The group-number-reuse argument at :508 is **sound for this runner's ordinary ownership/reaping model**. `start_new_session=True` makes the child a session and process-group leader. In the inspected CPython implementation, a TimeoutExpired while waiting for captured-pipe EOF leaves that child unreaped; a wait that actually reaps it completes rather than raising TimeoutExpired. This code does not poll/reap before `killpg`. An unreaped child retains its PID, so another process cannot acquire the same leader/group number during this interval. A leader that exits before its pipe-holding descendant is still a zombie until reaped. [Linux wait semantics](https://man7.org/linux/man-pages/man2/wait.2.html), [Linux session creation](https://man7.org/linux/man-pages/man2/setsid.2.html).

That reasoning assumes no external SIGCHLD auto-reaping policy or concurrent independent waiter; this file installs neither. It is not a general guarantee for arbitrary embedding code that reaps another component's children. The own-group guard passed both the ordinary-group and caller-group mock controls. No real PID-reuse experiment or unrelated-process signal was attempted.

Additional documentation discrepancies in this same lifecycle area:

- **:465** says `gan_va_chay(False)` means the child has already been killed. It now only returns false; killing moved to the caller at :558. Direct invocation with failed assignment returned false with **zero** kill calls. Update this postcondition to “still requires caller cleanup.”
- **:418–420** describes closing on every exit as killing the whole tree without distinguishing a failed close. State the successful-close condition and refer to reported failure outcomes.
- **:577** infers “child holds pipe” from TimeoutExpired. That timeout can also occur while waiting for process exit. Prefer the observable fact that output collection/process waiting did not complete within the bound.
- **:4313** says heartbeat stops only when killed, though the new stop-file branch also stops it. The assertion is only intended before teardown; qualify the comment.
- **:5771–5772** retains the historical “rmtree after totals” account. Local `chay_tu_kiem` leaves the temporary-directory context before printing totals at :5805. The remote CI root cause was not verified; this history needs a separately identified scope/traceback or corrected wording.

The principal comments at :407–412, :507–510, and r555's docstring correctly express the owner's intended narrowing. Implementation/diagnostic exceptions above prevent saying it is truthful everywhere.

## Windows ctypes review and execution limits

**I cannot run Windows here.** API-outcome tests use the actual `_VeWindows` Python implementation with fake DLL functions; they are not native Windows tests.

The ctypes field order and widths match Microsoft's basic and extended job-limit definitions: two signed 64-bit time limits, 32-bit flags, pointer-sized size/affinity fields, six 64-bit IO counters, and four pointer-sized memory counters. On this Linux x64 scalar ABI, the captured structure was basic **64 bytes**, extended **144 bytes**, flag offset **16**, IO offset **64**, memory offsets **112/120/128/136**, flag **0x2000**. No layout defect found; Windows x86 and native ABI execution were not measured. [Microsoft basic-limit structure](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information), [Microsoft extended-limit structure](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information).

The pointer-return `CreateJobObjectW` restype avoids handle truncation; pointer arguments are declared for set/assign/terminate/close and resume. Default int returns fit Win32 BOOL and the 32-bit status being checked for resume. Create is called with two null arguments, so its omitted argtypes do not truncate a non-null pointer in this call. Constructor and assignment/resume exceptions now fail closed. The job is unnamed and its handle non-inheritable; ordinary CreateProcess descendants join it and no breakaway flags are enabled. Successful job termination targets associated processes, including nested jobs. This is the documented job model, not an arbitrary-code security sandbox. [Microsoft CreateJobObjectW](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-createjobobjectw), [Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects), [Microsoft TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject).

The initial Windows process handle remains held by `Popen`, which also protects the root process ID against reuse while that handle exists. That does not by itself prove every internal selection made by `taskkill /T` is job-scoped. [Microsoft explanation of process-ID lifetime](https://devblogs.microsoft.com/oldnewthing/20110107-00/?p=11803/).

## F05 — P3 — closed

At **:5714–5715**, the parent now forwards the temporary-cleanup warning before classification, including a credited mutant. An actual-grader probe supplied a valid completion proof, the expected assertion failure, rc1, and a cleanup warning. The result remained **`(1, 0, 0)`**, and parent output included **`CANH BAO ... KHONG don duoc`**. Completion/kill credit and directory-cleanup outcome remain distinct. This closes round-3 F05; it does not establish the unverified historical CI root cause.

## Mutant soundness and radius

Linux: **6/6 killed in `chi_dich=True`; 6/6 killed in `chi_dich=False`**. Every individual result was `(1, 0, 0)`, every mutant child rc1, no DO_KHAC, and exact declared failure sets. These are the six requested mutants, not the complete catalog. The targeted children had 0/2 or 0/1 successful self-cases, as expected for these deliberate mutations.

| Mutant | Declared = observed failed cases | Targeted kill | Full kill | Full child self-case total |
|---|---|---:|---:|---:|
| `timeout-chi-giet-con` | r555, r556 | 2/2 | 2/2 | 54/56 |
| `windows-popen-nem-ro-job` | r556 | 1/1 | 1/1 | 55/56 |
| `con-treo-cho-khong-han` | r556 | 1/1 | 1/1 | 55/56 |
| `windows-khong-job-van-chay` | r556 | 1/1 | 1/1 | 55/56 |
| `windows-gan-hong-van-chay` | r556 | 1/1 | 1/1 | 55/56 |
| `don-cay-nem-thay-124` | r556 | 1/1 | 1/1 | 55/56 |

Cause replay: **7/7 intended target assertions across six mutants**, rc0. The replay used only the existing fixtures, with cleanup of retained direct `Popen` children after each measurement.

- **`timeout-chi-giet-con`:** r555 fails its 4.5-second same-group elapsed bound at :4368: the grandchild retains stdout and the five-second drain is exhausted after the 1.5-second timeout. r556 fails the expected cleanup-exception diagnostic at :4469 because the mutation bypasses the cleanup call entirely. On Windows, job close eventually kills the grandchild, but occurs after the drain; therefore the same elapsed-bound assertion should fail. The POSIX detached cases are no longer required to stop their heartbeat.
- **`windows-popen-nem-ro-job`:** r556 first fails the close-call assertion at :4443 in the fake no-job branch. This is a sound missing-finalization mutation, but its name overstates specificity: it removes closing on **all** exits, and the killing assertion is reached before the Popen-error subcase at :4458. It does not independently certify Popen-plus-close-failure diagnostics. Same mock runs on both platforms. On native Windows, successful TerminateJobObject should keep r555's heartbeat/timing checks passing despite the leaked job handle.
- **`con-treo-cho-khong-han`:** r556 fails :4449 because the recorded wait timeout is None instead of 5.0. The fake wait returns immediately, so killing this mutant measures the required bounded-wait argument without hanging the suite. It does not measure native wait-error handling. Same failure expected on Windows.
- **`windows-khong-job-van-chay`:** r556's fake unusable-job branch fails its rc126 assertion at :4442. It measures the early admission/no-spawn gate. In the real wrapper, the later assignment check still exists, so this kill is not evidence that a native child actually executed outside a job.
- **`windows-gan-hong-van-chay`:** r556 fails :4442 on the fake failed-assignment branch. The replacement evaluates assignment and then suppresses the failure branch. It measures refusing to continue after failed assignment/resume. A real failed assignment leaves a suspended child; the mutant name is not proof that it resumed. Same mock failure expected on Windows.
- **`don-cay-nem-thay-124`:** r556 catches the escaping injected RuntimeError, sets `p=None`, and fails :4469. This is the intended rc124-preservation assertion, not an unrelated infrastructure exception credited as a kill. Windows still executes the job-close finally; POSIX can leave the existing finite sleep fixture alive temporarily under this mutant. The separate cause replay retained and cleaned its own child.

No extra Linux radius was observed. Windows radius is reasoned: r556 mocks are platform-independent; the live r555 difference is the five-second drain versus its 4.5-second bound for the timeout mutant. Removing only final job close should not kill r555 when normal job termination succeeds. Other self-cases do not acquire these timeout-path failures merely from the six replacements. Native Windows full-radius execution remains **not run**, not passed. The removed r557 and its two scan mutants are appropriately retired with the removed scan contract.

## Commands and execution evidence

All four requested runs used the archive copy, with a minimal environment: `PATH=/usr/bin:/bin`, `LANG=C.UTF-8`, `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, plus the indicated selector. No credentials were inherited by these runs. Existing tests created local fixture repositories and fixture commits in temporary directories, not commits in `src/` or remote operations.

The runner is `review-wp748-r22-round4-nK4LuP/requested.py`; exact argv, cwd, environment, UTC start/end, elapsed time, rc, and totals are in `requested-results.json`. `mutants.py` calls the actual `chay_dot_bien_tu_kiem(muc=[entry], chi_dich=...)` for each requested descriptor and retains each child result/log.

| Archive command | rc | N/N | Elapsed |
|---|---:|---|---:|
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 /usr/bin/python3 ops/nhanh_don_duoc_test.py` | 0 | 8/8 | 1.722s |
| `NHANH_DON_DUOC_CHI_TU_KIEM=1 /usr/bin/python3 ops/nhanh_don_duoc_test.py` | 0 | TU KIEM: 56/56 | 55.486s |
| `/usr/bin/python3 ../mutants.py targeted` | 0 | MUTANTS chi_dich=True: 6/6 | 10.357s |
| `/usr/bin/python3 ../mutants.py full` | 0 | MUTANTS chi_dich=False: 6/6 | 314.427s |

Supplementary commands from this directory used the same `env -i` values above:

| Command / scope | rc | Result |
|---|---:|---|
| `python3 review-wp748-r22-round4-nK4LuP/probes.py` | 0 | **25/25 expectations**, including reproduced defects; `probes.log`, `probe-results.json` |
| `python3 review-wp748-r22-round4-nK4LuP/fallback_probe.py` | 0 | **1/1** untimed-Windows-drain expectation; `fallback-results.json` |
| `python3 review-wp748-r22-round4-nK4LuP/trace_causes.py` | 0 | **7/7** target assertion traces, six mutants; `cause-results.json` |
| `python3 review-wp748-r22-round4-nK4LuP/contract_docs_probe.py` | 0 | **2/2** documented-behavior discrepancies; `contract-docs-results.json` |
| Inline Python ctypes layout inspection (no native API execution) | 0 | **1/1** x64 scalar-layout control; `layout-results.json` |

Expectation counts include observing a defect as expected. They are not additional product-pass counts. The twelve mutant-child logs, two per mutant, retain actual rc1 outcomes, totals, and assertion-failure sets. No remote PR/CI readback or launcher attestation was performed. Public platform documentation was consulted via the web tool without user credentials.

## Round-3 finding reconciliation

Source: attached `VERDICT_LUOT3_c435b79.md`, reviewed SHA `c435b790a4c026174e40e54c9738bb462a6c482e`.

| Finding / F02 component | Round-4 status |
|---|---|
| **F02 P2 overall** | **PARTIALLY FIXED; remains open** only for the narrowed-contract defects above. |
| F02 hole 1: detached POSIX discovery/containment | **Retired by owner decision (b)**. The scan is removed; undetected/surviving detached descendants are not themselves defects. Required truthful reporting remains in scope and is incomplete on the exceptional path. |
| F02 hole 2: Windows boundary/failure paths | **Substantially repaired, incomplete**. False/API-exception controls fail closed; set exceptions close the acquired handle; failed Popen closes; kill failure is reported; wait is bounded. Wait errors, exceptional close reporting, and the helper's untimed drain remain. |
| F02 hole 3: cleanup exception / skipped fixture teardown | **Partially fixed**. Ordinary injected cleanup failure preserves rc124. Secondary drain failure and misleading diagnostics remain. r555's whole run/assert sequence is now enclosed by teardown; a simulated spawn exception confirms teardown runs. |
| F02 hole 4: ownership-acquisition and numeric-PID reuse races | **Removed with the scan/identity-kill mechanism**. The ordinary original-group path has the sound unreaped-child argument described above. No replacement ownership is assembled from separate `/proc` reads. |
| F02 hole 5: r555 PID signalling | **Fixed**. Teardown writes `.dung` and waits for stable heartbeat; it sends no signal to a PID. The fixture still writes a `.pid` file but teardown does not consume it. |
| **F05 P3: credited-result cleanup warning hidden** | **Closed**, independently reproduced with valid proof and expected assertion result. |
| F03, previously closed mutant call-site/target problem | **Remains closed**. Common call-site mutation, exact two-case radius, and intended assertion causes confirmed on Linux; Windows reasoned as above. |
| F04, previously closed timestamp lexical issue | Unchanged by this one-file delta; baseline r554 passes. No fresh full timestamp-mutation audit is claimed. |

Not run: native Windows, other catalog mutants, repository-wide release gates, eight actual performance/shard executions, or external GitHub/CI/launcher verification. No unusual hostile payloads were authored; additional failure probes use in-memory OS/API outcomes, and live cause replay reuses existing repository fixtures.

Final source check UTC **2026-10-22T10:30:48.117094+00:00**: exact head/tree unchanged; HEAD detached (expected rc1); tracked/untracked/ignored status empty; immutable base is an ancestor (rc0); **4839/4839 archive files/symlinks unchanged**, no mismatches. Commands and outputs are retained in `final-identity.json`. This verifies final contents, not an independently monitored filesystem-access history. The local `origin/master` discrepancy recorded at the start is not silently treated as equality with the stated base.

Reviewer identity remains runtime-reported Codex/GPT-6 via API/local tools; exact model slug, backend effort, enclosing launcher invocation, and independent execution-receipt attestation cannot be verified here. `launcher.out` and `launcher.err` were both empty at the start. No GitHub submitter identity exists for this review because nothing was published.

Threshold: zero P0/P1/P2. Open findings: **P0=0, P1=0, P2=1 (continuing F02), P3=0 (F05 closed)**. All requested Linux runs completed successfully; their passing mutation counts do not close the independently reproduced exceptional-path defects. The Windows execution limitation is disclosed separately and is not itself the reason for withholding approval.

Review completed UTC: **2026-10-22T10:30:48.118198+00:00**.

VERDICT: changes_requested
