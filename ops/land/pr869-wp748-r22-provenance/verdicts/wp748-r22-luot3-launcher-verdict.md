# Independent read-only re-review — WP748 r22, PR #869, round 3

Reviewer identity reported by runtime: “Codex, an agent based on GPT-6.” Provider: OpenAI; system-reported surface: API; observed transport: direct local tools (`functions.exec` / `exec_command`). Exact backend model slug, effort, and independent provider/session attestation are unavailable. The user reports `launcher.py run`; local `launcher.out` and `launcher.err` were empty at start, so the invocation and enclosing final execution receipt cannot be independently verified inside this review.

Reviewed SHA: `c435b790a4c026174e40e54c9738bb462a6c482e`  
Reviewed tree: `4860a9772a7d86d622952099bf7eaa39349dfa29`  
Round-2 comparison: `a56a3219e58ddf4c87cafac1e7357962d643e3db`  
Stated base: `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`.

Identity checks PASS: HEAD/tree match, HEAD detached (`symbolic-ref -q HEAD` rc=1), status empty. Local `origin/master` instead resolves to `c73af7b0ba751bfbb974f5ba11147ccb555015dc`; the prompt's ref equivalence is not true locally. Review remains scoped to the explicit immutable comparison SHAs; no ref is changed or fetched. Delta: one file, three commits, 331 insertions / 86 deletions.

Source is read-only. Authorized output is this report and scratch outside `src/`. No credential inspection/use, source edits, source commits/pushes, or GitHub comments. Required cloud-runtime skill read; no environment_status tool available.

Native Windows execution is unavailable. Windows conclusions will be static reasoning or explicitly labelled simulations, never native passes.

Status: in progress.

Started UTC: 2026-10-22T09:26:23.535258+00:00
Platform: Linux-6.18.44-fc-v140-x86_64-with-glibc2.39; Python 3.13.16.

Archive UTC 2026-10-22T09:26:52.893920+00:00: `git -C src archive --format=tar c435b790a4c026174e40e54c9738bb462a6c482e`, rc=0; extracted to `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22c/review-wp748-r22-round3-Dj8SMQ/head`. Reviewed-file SHA-256 `9b1e660541931ef39ea39144fec8444c013ceb4211642258e049d36193f55d38`.

Started `product` UTC 2026-10-22T09:27:53.635338+00:00: `{'NHANH_DON_DUOC_KHONG_DOT_BIEN': '1'} ['/usr/bin/python3', 'ops/nhanh_don_duoc_test.py']`; archive cwd; minimal credential-free environment; watchdog 90s.

Completed `product`: rc=0, 1.823s, UTC 2026-10-22T09:27:55.458587+00:00. Totals: ['8/8']. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22c/review-wp748-r22-round3-Dj8SMQ/product.log`.

Started `self` UTC 2026-10-22T09:27:55.458958+00:00: `{'NHANH_DON_DUOC_CHI_TU_KIEM': '1'} ['/usr/bin/python3', 'ops/nhanh_don_duoc_test.py']`; archive cwd; minimal credential-free environment; watchdog 150s.

Completed `self`: rc=0, 38.054s, UTC 2026-10-22T09:28:33.513315+00:00. Totals: ['TU KIEM: 57/57']. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22c/review-wp748-r22-round3-Dj8SMQ/self.log`.

Started `targeted` UTC 2026-10-22T09:28:33.514261+00:00: `{} ['/usr/bin/python3', '/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22c/review-wp748-r22-round3-Dj8SMQ/mutants.py', 'targeted']`; archive cwd; minimal credential-free environment; watchdog 180s.

Completed `targeted`: rc=0, 27.866s, UTC 2026-10-22T09:29:01.380673+00:00. Totals: ['MUTANTS chi_dich=True: 9/9']. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22c/review-wp748-r22-round3-Dj8SMQ/targeted.log`.

Started `full` UTC 2026-10-22T09:29:01.381773+00:00: `{} ['/usr/bin/python3', '/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22c/review-wp748-r22-round3-Dj8SMQ/mutants.py', 'full']`; archive cwd; minimal credential-free environment; watchdog 600s.

Review checkpoint: Linux product **8/8**, self **57/57**; targeted and full mutant details are recorded as they complete. `probes.py` rc=0, **18/18 expectations** (includes deliberate defect reproductions, not 18 correctness guarantees); log `review-wp748-r22-round3-Dj8SMQ/probes.log`. All probe signals and Windows API calls were mocked; no real PID reuse or unrelated-process signalling was attempted.

Confirmed remaining **WP748-R22-F02, P2**: `_quet_dau_posix` reads `environ` before `stat` (`ops/nhanh_don_duoc_test.py:458`, `:461`). A PID replacement between those reads attaches the old process's ownership marker to the replacement's starttime. The subsequent pidfd open/identity check then correctly identifies and signals the wrong generation. The stateful mock produced `{101: "501"}` after reading generation 500's marker, then recorded a pidfd signal to replacement generation 501. r555 cleanup shares this discovery path.

Other observed limits: inaccessible per-process environment reads become `{}`; a newly found process at the rescan deadline is omitted from the reported zero-survivor list; the numeric-PID fallback remains racy by design. Windows API mocks confirm ordinary create/set failures do not spawn; assign/resume failures kill then wait and return 126. Popen failure leaks the already-created job, and assign failure followed by kill failure escapes with an unreaped suspended child. Windows layout observed on Linux's matching 64-bit scalar ABI: basic 64 bytes, extended 144 bytes, LimitFlags offset 16, IO offset 64, memory fields starting 112. This is not native Windows execution.

Checkpoint UTC: 2026-10-22T09:32:53.337483+00:00

Completed `full`: rc=0, 357.447s, UTC 2026-10-22T09:34:58.828720+00:00. Totals: ['MUTANTS chi_dich=False: 9/9']. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l22c/review-wp748-r22-round3-Dj8SMQ/full.log`.

## Findings

### WP748-R22-F02 — P2 — timeout-descendant-containment — remains open

The repair is substantial, but it does not close all five round-2 holes. The new ownership-acquisition race can signal an unrelated replacement process even on a platform with pidfds. This alone prevents approval. The following are manifestations of the existing class, not five new independent findings.

| Round-2 hole | Round-3 status | What is repaired / what remains |
|---|---|---|
| 1. Detached orphan discovery | **Narrowed** | The unchanged-marker orphan is now covered by r555's third variant; Linux baseline passes. Missing `/proc` is explicitly reported. A detached orphan that execs with a sanitized environment, or whose environment cannot be read, remains undiscoverable. Nested timed `run()` calls also overwrite the outer marker. The scan itself has the ownership/identity race below. |
| 2. Windows runs without a usable job | **Narrowed; the ordinary fail-open branches are closed** | Create/set failure returns 126 without spawning; assign/resume failure kills and waits without resuming outside the job. Kill-on-close is configured. Failure handling is not complete: failed `Popen` leaks the job; failed kill after failed assignment leaves an unassigned suspended child and raises; the failure wait has no timeout. Native Windows is not run. |
| 3. Cleanup exceptions replace timeout / bypass fixture teardown | **Narrowed** | An exception from `_ket_thuc_cay` now yields rc124 with `LOI don cay` and attempts direct-child kill. The mock and r556 confirm this. It does not finish descendant cleanup on POSIX. r555's cleanup `finally` still begins after `run()` returns, so an escaping spawn/other run error skips it. |
| 4. PID reuse between check and signal | **Narrowed** | Opening a pidfd before the identity check and signalling through it closes the old final check-to-signal gap for a correctly acquired identity. The no-pidfd path still deliberately signals by PID. Worse, the new scan can acquire the wrong identity before the pidfd is opened. |
| 5. r555 kills a PID from a file | **Narrowed** | The unconditional PID-file kill is removed. Linux teardown now uses the marker scan and identity helper, inheriting their acquisition/fallback races; Windows teardown relies on job close and does no PID kill. The fixture's entire spawn/run sequence is still not enclosed by teardown. |

**Ownership acquisition can target a replacement.** Locations: `ops/nhanh_don_duoc_test.py:458`, `:461`, `:463`, `:479`, `:484`, `:486`; r555 consumer `:4423`. The scanner reads an owned process's environment, closes that file, then independently opens the same numeric PID's `stat`. If the process exits and that PID is reused between those reads, the saved marker belongs to the old generation but the saved starttime belongs to the unrelated replacement. The later pidfd is opened for that replacement; its starttime matches the incorrectly saved key, so it is signalled. This is an ownership error before signalling, not a failure of pidfd signalling itself. A stateful mock reproduced exactly this sequence and recorded a signal to the replacement generation. No real unrelated process was signalled.

**Discovery and status remain incomplete.** Locations: `:459`, `:596`, `:619`, `:620`, `:622`, `:627`. A readable `/proc` directory with an unreadable owned process environment is treated as an empty successful scan; the probe returned `{}`. The final rescan is reduced with `or {}`, losing its unsupported/failed status. At the deadline, newly discovered entries are added after `song` was calculated and then the loop exits: the probe found a new process but reported `0 tien trinh da chup con song` without signalling it. Filtering new entries by PID alone also prevents replacing a stale tracked identity with a newly observed identity at that PID. The first enumeration and each complete scan occur outside any per-entry deadline check, so the loop deadline is not a strict total cleanup wall limit.

The environment marker is discovery assistance, not an enforced lifetime boundary. It works for the three supplied heartbeat fixtures. A child can start another executable with a clean environment, and normal nested calls at `:646` replace the outer marker without any hostile behavior. If the intermediate ancestry disappears, neither the outer marker nor its PPID snapshot associates that descendant with the outer run. Linux exposes the initial environment of the current executable, not an authoritative immutable ancestry record; merely calling an environment setter/unsetter need not change the procfs view. [Linux proc_pid_environ documentation](https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html).

**Own-process and unrelated-process safety.** The normal paths generate a fresh 128-bit token and place it only in the child's environment dictionary; they do not put that token in the caller's environment. r555 does the same with its separate token. Exact NUL-separated entry membership avoids the prefix bug, and ordinary caller/ancestor matching is therefore not expected. The process-group guard still excludes the caller's group. However, `_quet_dau_posix` has no self/ancestor exclusion and trusts a matching marker anywhere; the demonstrated cross-generation scan race can select an unrelated process. Token uniqueness does not fix that race. An explicit self exclusion would be useful defense, but would not repair ownership acquisition generally.

**Windows exceptional paths.** Locations: `:542`, `:555`, `:563`, `:584`, `:649`, `:651`, `:653`. The API mocks observed:

- create/set failures: no `Popen`, rc126;
- assign/resume failures with a working child kill: `kill`, `wait(timeout=None)`, rc126;
- termination failure with no taskkill: bounded output drain followed by job close, rc124;
- failed `Popen`: exception, no job close;
- failed assignment followed by failed child kill: exception, no wait, no resume; closing the empty job cannot kill its unassigned child;
- an exception during setting job information: rc126 but the already-created handle is discarded without closing;
- a false return from `CloseHandle`: ignored, the stored handle is cleared, and no close-failure diagnostic is added.

The last three are simulated failure paths, not claims about their native frequency. The ordinary job-creation/assignment fail-open regression is repaired. The broader claim that every failure returns 126 and kills/reaps the child is false. `q.wait()` without a timeout also does not satisfy a bounded-return guarantee.

**Exception handling / parsing.** Locations: `:415`, `:430`, `:461`, `:664`, `:4452`, `:4456`. The scanner parses process `stat` even for environments that do not match. A process name that cannot be decoded by `read_text`, or an unexpectedly short/malformed stat result, can abort global discovery. These hostile-input scenarios were described only; no unusual process-name or byte payload was authored. The new outer catch preserves rc124, but its POSIX emergency cleanup kills only the direct child, so detached descendants can remain. `_giet_dinh_danh` also labels every `pidfd_open` OSError `da chet`, including permission/resource/unsupported-operation errors; the permission-error mock confirmed the misleading label. r555 teardown did not run in the mock where `run` raised before returning.

**Fix direction and regression requirements.** At the discovery/kill boundary, acquire ownership and identity from a consistent process generation and retain the stable handle through signalling; do not combine an environment read from one generation with a later stat from another. If retaining the scan, anchor procfs reads to the same process instance, reject identity changes, distinguish incomplete discovery from empty discovery, and include last-scan arrivals in cleanup and diagnostics. Eliminate the numeric-PID fallback where safe identity cannot be guaranteed. For the chosen all-five closure scope, use an enforceable per-run lifetime boundary or fail before running on unsupported process models; a comment admitting an escape is not closure of option (a).

On Windows, start handle ownership protection before spawning, cover API exceptions as well as false returns, use bounded terminate/reap handling, and retain/report failed handle closure. Put r555 teardown around the complete run/assert sequence. Catch/validate per-process stat parsing failures without disabling the rest of cleanup. Preserve the timeout result while separately reporting incomplete cleanup.

Regression tests should model replacement between environment/stat reads and between identity check/signal; inaccessible proc entries; the final-scan deadline arrival; nested marker replacement; absent pidfd; failed spawn/assign/kill/close; and exceptions before r555 assertions. Retain the three live heartbeat controls and add native Windows baseline/mutant evidence. Repair risks include signalling outside the owned boundary, leaking handles on partial initialization, rejecting legitimate nested jobs, and reintroducing blocked reader-thread pipe closes. Stable-handle and boundary lifecycle tests must accompany the fix.

### WP748-R22-F05 — P3 — temporary-cleanup-diagnostics — new

Locations: `ops/nhanh_don_duoc_test.py:5870`, `:5899`, `:5828` (credited-mutant branch). Owner for remediation: WP748 executor.

`ignore_cleanup_errors=True` is a reasonable way to preserve evidence that all case bodies completed when only temporary-directory removal fails. It does not prove cleanup succeeded or identify why removal failed. A controlled cleanup-failure probe returned a passing case list and wrote the completion proof while the directory remained; the warning appeared on child stderr. A second probe fed a completed expected mutant failure plus that warning to the actual grader: it credited `(1, 0, 0)` and emitted no warning. Thus the claimed stderr reporting is lost in the normal successful mutation-gate output.

This is not evidence of a false assertion-based mutant kill: the cases really completed and the declared assertion still failed. It can hide a separate resource/cleanup failure, including one caused by a surviving process. Keep completion and cleanup outcomes separate, forward the cleanup warning on credited results, and record cleanup status in durable evidence if it is a gate requirement. Add a child-with-valid-proof-and-cleanup-warning test; retain successful cleanup as a positive control. Avoid turning an intentional mutant's expected assertion failure into `not_measured` solely because a bounded, independently diagnosed final directory deletion failed.

The supplied CI root-cause claim is **not independently verified**. I did not fetch CI 39741391940. In the actual round-2 `chay_tu_kiem`, the `TemporaryDirectory` context exits **before** both the totals print and the proof write. Therefore “rmtree after the totals line” is not that function's local ordering; it would need a traceback showing another totals line or another cleanup scope. The outer `chay_dot_bien_tu_kiem` temporary-directory context remains strict. No native Windows handle-release timing was measured.

## Windows structure and platform limits

I cannot run Windows in this environment. I inspected the ctypes fields against Microsoft's definitions and captured their instantiated layout through a mocked DLL call on Linux's matching 64-bit scalar ABI.

`_Co` maps the two signed 64-bit time limits, 32-bit flags, two pointer-sized working-set values, 32-bit process count, pointer-sized affinity, and two final 32-bit classes in the correct order. Observed x64 offsets: **0, 8, 16, 24, 32, 40, 48, 56, 60**; size **64**. The kill-on-close flag is **0x2000**. [Microsoft basic-limit structure](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information).

`_MoRong` correctly follows that structure with six 64-bit IO counters and four pointer-sized memory values. Observed x64: IO at **64**, memory fields at **112, 120, 128, 136**, total **144 bytes**. The equivalent Windows x86 layout is expected to be basic **48**, IO at **48**, memory at **96/100/104/108**, total **112**, based on Windows scalar sizes/alignment; x86 was not executed. I found no field-width/order defect. [Microsoft extended-limit structure](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information).

Suspended creation followed by assignment/resume is appropriate for the ordinary `CreateProcess` descendant model. No breakaway limit is enabled. Closing the last job handle with kill-on-close terminates associated processes, including nested jobs; it is still necessary to handle failed closure and partial initialization. This is the documented job model, not an arbitrary-code security sandbox. [Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects).

## Mutant soundness and radius

Linux measurements: **9/9** killed in each mode, each grader result `(1, 0, 0)`, all 18 mutant children rc1, no `DO_KHAC` cases, no missing completion proof. Full-mode failure sets exactly match the declared targets. These counts cover the requested nine entries, not the entire catalog.

| Mutant | Declared = observed failed cases | Targeted kill | Full kill | Full child self-case total |
|---|---|---:|---:|---:|
| `timeout-chi-giet-con` | r555, r556 | 2/2 | 2/2 | 55/57 |
| `cay-dau-khop-tien-to` | r557 | 1/1 | 1/1 | 56/57 |
| `giet-bo-kiem-danh-tinh` | r557 | 1/1 | 1/1 | 56/57 |
| `windows-khong-job-van-chay` | r556 | 1/1 | 1/1 | 56/57 |
| `windows-gan-hong-van-chay` | r556 | 1/1 | 1/1 | 56/57 |
| `don-cay-nem-thay-124` | r556 | 1/1 | 1/1 | 56/57 |
| `gop-bo-kiem-nhom` | r552 | 1/1 | 1/1 | 56/57 |
| `gop-bo-kiem-san` | r552 | 1/1 | 1/1 | 56/57 |
| `ghi-so-gop-dich` | r546 | 1/1 | 1/1 | 56/57 |

Targeted children report 0/2 for the timeout mutant and 0/1 for each other entry. These expected negative totals describe mutant children, not baseline failures.

Separate cause replay: **6/6** new/changed mutants, seven target-case failures, rc0. The assertion traces establish:

- `timeout-chi-giet-con`: r555 accepts rc124 then fails the **elapsed bound** at `:4460`; r556 fails the missing cleanup-exception diagnostic at `:4538`. On Windows, kill-on-close does eventually terminate the descendant, but it executes after the five-second output drain. The 1.5-second run plus that drain exceeds r555's 4.5-second bound. Therefore it should still be killed for loss of timely tree cleanup, even though the post-return heartbeat may already have stopped. No native Windows pass is claimed.
- `cay-dau-khop-tien-to`: r557 fails its exact-environment-selection assertion at `:4558`. It uses the same fake procfs fixture on both platforms. Real run tokens all have equal fixed length, so the broader prefix predicate does not add another radius in the supplied live fixtures. Replacing the old omitted-scan mutant avoids its POSIX-only orphan failure. This mutant measures exact matching; it does **not** measure immutable ownership or every orphan escape.
- `giet-bo-kiem-danh-tinh`: r557 fails the stale-identity/no-signal assertion at `:4563`, with mocked pidfd APIs on both platforms. It measures removal of the check, not the environment/stat acquisition race or the no-pidfd gap.
- `windows-khong-job-van-chay`: r556's first fake no-job branch returns something other than 126 and fails at `:4523`. The mock is selected on both operating systems.
- `windows-gan-hong-van-chay`: r556 passes its no-job assertions, then fails `:4523` for the fake failed-assignment branch. The mutation evaluates assignment before forcing the abort condition false; it does not merely erase the call. Same mock semantics on both platforms.
- `don-cay-nem-thay-124`: injected RuntimeError escapes `run`; r556 catches it and fails `:4538`. Windows job closure remains in `finally`; on POSIX the mutant can leave the finite sleeping child alive temporarily. The supplemental replay tracked and terminated its own still-live direct child after measuring the failure. This is not an unrelated exception being credited as a kill: the expected behavior under an injected cleanup exception is what r556 asserts.

The two group mutants remove independent shared collector checks and expose r552's missing-required-group / below-floor controls respectively. `ghi-so-gop-dich` removes infrastructure-error recording; r546's injected-read matrix detects the lost diagnosis through r554. Their code and target semantics are platform-independent. r546 invokes other cases under a read-fault matrix but checks infrastructure classification rather than requiring every inner assertion to pass, explaining why the new mutants do not also kill r546. Native Windows full-mode radius is **reasoned, not measured**; Linux full-mode radius is measured exactly.

## Commands, receipts, and final comparison

Scratch: `review-wp748-r22-round3-Dj8SMQ/`. `requested.py` runs the exact commands below in the archive with `env -i` semantics: PATH, LANG, PYTHONUTF8, PYTHONDONTWRITEBYTECODE, GIT_CONFIG_NOSYSTEM, and GIT_CONFIG_GLOBAL only, plus the requested selector. No credentials are inherited. The repository's existing tests create local fixture repositories/fixture commits; no reviewed-source commit or remote operation was performed.

| Command / scope | rc | N/N / result |
|---|---:|---|
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 /usr/bin/python3 ops/nhanh_don_duoc_test.py` | 0 | product **8/8**, 1.823s |
| `NHANH_DON_DUOC_CHI_TU_KIEM=1 /usr/bin/python3 ops/nhanh_don_duoc_test.py` | 0 | self **57/57**, 38.054s |
| `/usr/bin/python3 ../mutants.py targeted` (absolute script path in receipt) | 0 | **9/9**, `chi_dich=True`, 27.866s |
| `/usr/bin/python3 ../mutants.py full` (absolute script path in receipt) | 0 | **9/9**, `chi_dich=False`, 357.447s |
| `python3 review-wp748-r22-round3-Dj8SMQ/probes.py` under the same minimal environment | 0 | final **19/19 expectations**, including reproduced defects; initial version had 18/18 before adding warning-forwarding check |
| `python3 review-wp748-r22-round3-Dj8SMQ/trace_causes.py` under the same minimal environment | 0 | **6/6** cause traces, seven intended target assertions |
| Final Git identity/status/diff checks and archive comparison | 0, except expected detached-ref rc1 | **4839/4839** files/symlinks unchanged; clean tracked/untracked/ignored status |

The full exact commands, environments, start/end UTC timestamps, rc and totals are in `requested-results.json`; raw product/self/targeted/full logs and all 18 individual mutant-child logs are retained. Final identity receipt: `final-identity.json`, UTC **2026-10-22T09:35:46.298828+00:00**. HEAD/tree remain exact; local `origin/master` remains the differing ref documented above. The stated immutable base is an ancestor of HEAD (`merge-base --is-ancestor`, rc0). No checkout/ref was changed.

The source comparison verifies final contents, not an independently monitored history of every filesystem access. Sandbox mode is workspace-write; source read-only scope was maintained by operating on scratch copies. Public Microsoft/Linux documentation was consulted through the web tool; no credentials or remote repository/CI APIs were used.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Source: `VERDICT_LUOT2_a56a321.md`, exact comparison SHA `a56a3219e58ddf4c87cafac1e7357962d643e3db`.

| Finding | Assessment |
|---|---|
| F02 P2, five holes | **VÁ HỜ**, with **VÁ SINH LỖI MỚI** in ownership acquisition: substantial partial fixes, but the environment/stat race newly allows a replacement identity to be adopted. The five statuses and evidence are above. |
| F03, previously closed descriptor no-op | **ĐÃ VÁ THẬT** remains supported: common call-site mutation, corrected two-case target, intended Linux failures in both modes. Windows has a sound elapsed-bound reason to fail; native execution remains unmeasured. |
| F04, previously closed timestamp lexical defect | Unchanged by this delta; the ASCII parser remains present. Baseline r554 passes. The three old timing mutants were not rerun in this round and no fresh full timing audit is claimed. |

Not run: native Windows, all other catalog mutants, eight real shard/performance executions, repository-wide release gates, remote PR/CI readback, or launcher/provider attestation. Hostile scenarios were described in words; additional probes used ordinary existing fixtures and in-memory OS/API outcomes, not unusual payloads.

Threshold: zero P0/P1/P2. Open findings: **P0=0, P1=0, P2=1 (continuing F02), P3=1 (F05)**. All requested Linux executions completed. Approval is withheld for F02, independently of the unmeasured native Windows coverage.

Review completed UTC: 2026-10-22T09:40:02.193186+00:00

VERDICT: changes_requested
