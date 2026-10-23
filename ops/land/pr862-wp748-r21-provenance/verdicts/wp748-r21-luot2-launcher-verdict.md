# WP748 r21 independent read-only review

Review started: 2026-10-22 06:36:13 UTC. Status: completed; final UTC timestamp below.

Reviewer identity: OpenAI Codex. The runtime instructions describe this agent as
“Codex, an agent based on GPT-6”; an exact serving model identifier is not exposed
to this session. Provider: OpenAI (runtime identification); execution surface:
API assistant with local `functions.exec` / `exec_command` tools. The user reports
invocation through repository `launcher.py run`. I cannot independently
verify that outer invocation, the final execution receipt, or the precise serving
model/version. No model identity is inferred from an account or older verdict.
Runtime environment readback (allowlisted identity variables only, rc 0):
`CODEX_SESSION_ID` and `CODEX_THREAD_ID` both report
`01a16252-e014-7ca2-bc8a-3d39b003b4aa`. `CODEX_MODEL`,
`CODEX_EXECUTION_SURFACE`, `CODEX_RUN_ID`, `LAUNCHER_RUN_ID`, and `OPENAI_MODEL`
are not exposed. Effort is also not exposed. Provider-contract label:
`openai_codex`; transport: machine/tool-mediated. The observed API/tool surface
does not establish whether an outer CLI or service invoked this session.

Reviewed SHA: `28e35fd9206cdc8b2b44a39999421934f8437192`.
Reviewed tree: `f886966025dde4e2a850658a5479abbdb5bd762f`.
Sole parent: `3950a0f9fd0a9c29a36a599edc7a2d305619fc27`.
Merge object: `401d4f15362b3270d5dc8437ade3be5ab449eb22`, with the same tree
and parents equal to the reviewed parent and head. Local object evidence verifies
the merge shape; no live GitHub/master claim has been verified.

Authority/scope: this user's read-only review instruction; only
`3950a0f..28e35fd`, one file `ops/lease_publish_test.py`, 31 additions.
Writes are restricted to this verdict and scratch copies outside `src/`.
`VERDICT_TRUOC.md` is an untrusted earlier claim, not review evidence.

Initial command evidence:

- `pwd`: rc 0; verified the requested parent of `src/`.
- `git -C src rev-parse HEAD HEAD^{tree} HEAD^` and
  `git -C src rev-list --parents -n 1 HEAD`: rc 0; exact identities above.
- `git -C src symbolic-ref -q HEAD`: rc 1, confirming detached HEAD (wrapper rc 0).
- `git -C src status --porcelain=v1`: rc 0, empty.
- Merge `rev-parse` and `show --no-patch --format='%H %P'`: rc 0.
- Diff stat: rc 0. First full diff command had a mistyped parent OID and returned
  rc 128; corrected exact-OID diff returned rc 0 and was read independently.
- `git --version`: rc 0, `git version 2.43.0`.
- `python3 --version`: rc 0, `Python 3.13.16`.

Evidence directory: `review-evidence.RDHngm/` (created with `mktemp -d` in this
directory). `git archive --format=tar --output=<evidence>/head.tar
28e35fd9206cdc8b2b44a39999421934f8437192`: rc 0; extracted separate baseline and
three mutant trees. Archive size: 175,319,040 bytes. A content/mode/size/mtime
snapshot of 4,709 source files, full status including ignored/untracked paths,
diff and index listing were captured before execution. No tests run from `src/`.

Update: 2026-10-22 06:40:06 UTC.

At this checkpoint, the requested full suite was running from the baseline archive copy with the exact
command `GITHUB_ACTOR=x PYTHONUTF8=1 python3 -W ignore ops/lease_publish_test.py`.
Its `t125` A/B children were enabled. Final rc and N/N are recorded below.

Targeted command in each separate tree:
`GITHUB_ACTOR=x PYTHONUTF8=1 python3 -W ignore ops/lease_publish_test.py --chi-ca=t221_`.
Measured 2026-10-22 06:38:50–06:38:58 UTC; logs in
`<variant>.t221.stdout`, `<variant>.t221.stderr`, and `t221-results.json`.

| Variant | rc | Passed/executed | Intended diagnostic |
| --- | ---: | ---: | --- |
| Unmodified baseline | 0 | 1/1 | Both local keys and order proxy pass |
| Drop only `maintenance.auto=false` | 1 | 0/1 | Missing local maintenance key, Git config rc 1 |
| Drop only `gc.auto=0` | 1 | 0/1 | Missing local GC key, Git config rc 1 |
| Move both writes immediately after `c0` | 1 | 0/1 | Config newer than `c0` object |

Mutation kills: **3/3**, all at the intended assertion, none skipped.

Independent behavioral probes use `python3 -B -W ignore
review-evidence.RDHngm/probe.py <mode>` with `GITHUB_ACTOR=x PYTHONUTF8=1`.
They delegate Git calls to real Git 2.43.0 and inspect fresh fixtures, not a cache
created before observation. Executed 06:39:59–06:40:06 UTC:

| Mode | rc | N/N and observation |
| --- | ---: | --- |
| `trace-baseline` | 0 | t221 1/1; both local/effective keys before 27/27 commits; 0 maintenance children |
| `trace-after-c0` | 1 | t221 0/1; only 26/27 commits protected; 1 maintenance child from the unprotected first commit |
| `coarse-after-c0` | 0 | t221 1/1 despite genuinely delayed config; modeled two-second mtime resolution |
| `harmless-config-rewrite` | 1 | t221 0/1 after a correct build plus unrelated `git config review.marker true` |

Full commands, timestamps, stdout/stderr and Git trace events are retained in
`probe-results.json`, `<mode>.stdout`, `<mode>.stderr`, and `trace-*.trace.jsonl`.

Finding **F1 — P3 — `mtime-order-proxy`**. Location:
`ops/lease_publish_test.py:5996`–`:6000`; related description at `:5982`.
The test measures final local configuration correctly, but filesystem modification
times do not reliably establish the order in which configuration became effective.
The after-c0 mutant had config mtime `1792651203588936009` and c0 object mtime
`1792651203572119503`; quantizing each existing file's mtime to its two-second
bucket made both `1792651202000000000`, and the unchanged t221 passed 1/1. This is
an explicit filesystem-resolution model, not execution on FAT/Windows. Conversely,
the baseline with config older than c0 failed after an unrelated config write,
although both disabling keys remained correct. The docstring says “reflog” but
the implementation reads filesystem mtimes; config writes have no commit-reflog
entry. Current fixture code does not perform that later unrelated config write,
and native baseline/mutation checks pass, so this is a nonblocking test-quality
and portability defect, not a demonstrated failure of the scoped race fix.
Python explicitly documents that nanosecond-valued stat attributes need not have
nanosecond precision, including two-second FAT32 mtime resolution:
[Python `os.stat_result`](https://docs.python.org/3/library/os.html#os.stat_result).

Fix/debt owner: **WP748 executor/test maintainer**. Replace the timestamp comparison
with observation of a fresh `_mau_t133` construction: before each real commit,
query and assert the local/effective settings, while delegating commands to real
Git. Isolate/reset the template cache for that observation. Retain the final local
value checks and mutation controls. Correct the reflog wording. A strict `<`
comparison or sleeps would not reliably solve the timestamp problem.

Earlier-report comparison: only after independently reading code and running the
requested mutations, I inspected the prior report's claims. It names the same
`mtime-order-proxy` class; the evidence above is newly executed in this run, not
copied from that report. Final findings count and suite result are recorded below.

Maintenance-path review:

- `ops/lease_publish_test.py:5388` sets both repository-local values synchronously
  immediately after successful init and before `add`/`commit c0`. `_g_a0` uses
  `check=True`, so a failed config write aborts fixture creation. `_them_commit`
  and the extra executable-mode commit all use the same repository and do not
  replace or override those keys. `_mau_t133` completes 27 commits before caching
  the template; `t133` copies that template, including its `.git/config`.
- Git 2.55 `commit` calls `run_auto_maintenance`. That path checks
  `maintenance.auto` before creating a maintenance child, so explicit false
  prevents the child itself, regardless of enabled maintenance tasks or detach
  settings. When `maintenance.auto` is absent, this version also falls back to
  `gc.auto`, with zero disabling the child. Thus the two keys are not independently
  necessary on default Git 2.55; mutation rejection enforces the chosen fixture
  invariant. Sources:
  [Git v2.55.0 commit](https://github.com/git/git/blob/v2.55.0/builtin/commit.c#L1837),
  [Git v2.55.0 automatic-maintenance dispatch](https://github.com/git/git/blob/v2.55.0/run-command.c#L1849).
- Git 2.43's dispatcher likewise honors `maintenance.auto=false`; its dispatch
  lacks the newer `gc.auto` fallback. Separately, `gc.auto=0` disables the auto-GC
  work heuristics and covers older auto-GC behavior. Sources:
  [Git v2.43.0 dispatch](https://github.com/git/git/blob/v2.43.0/run-command.c#L1700),
  [Git configuration documentation](https://git-scm.com/docs/git-config/2.55.0#Documentation/git-config.txt-gcauto).
- Git 2.55 maintenance takes the object-store maintenance lock before task
  conditions and detachment, then rolls it back after the tasks. Suppressing
  dispatch avoids the lock lifetime rather than merely making GC do no work.
  [Git v2.55.0 maintenance lock and execution](https://github.com/git/git/blob/v2.55.0/builtin/gc.c#L1683).

Conclusion from source plus observed fixture behavior: the two keys cover all
automatic-maintenance triggers used by this template. The template issues no
explicit `git maintenance run`, starts no scheduled maintenance, and introduces
no higher-priority override. This conclusion does not claim protection against
external scheduled/manual processes or a caller deliberately overriding the keys.
Native Git 2.55 execution and the historical CI race itself have not been measured
in this environment (installed Git is 2.43.0). The referenced CI attempts and live
master state were not fetched or authenticated.

Other completed checks: exact-diff `git diff --check` rc 0; `actionlint -version`
rc 0 reports 1.7.7; `shellcheck --version` rc 0 reports 0.9.0. These version
queries are not represented as standalone lint runs.

Final execution results:

Working directory for the full suite:
`/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l21/review-evidence.RDHngm/baseline`.

```sh
GITHUB_ACTOR=x PYTHONUTF8=1 python3 -W ignore ops/lease_publish_test.py
```

Actual subprocess rc: **0**, retained in `review-evidence.RDHngm/suite.rc` and
confirmed by the completed tool process. First case entered at
2026-10-22 06:37:53 UTC; final case completed at 06:43:51 UTC.

| Execution | Passed/executed | Failed | Skipped |
| --- | ---: | ---: | ---: |
| Requested parent suite, actor `x` | **267/267** | 0 | 0 |
| `t125` child A, actor absent | **267/267** | 0 | 0 |
| `t125` child B, unfamiliar actor | **267/267** | 0 | 0 |

`t125` passed after 193.983 seconds. Each child's command was
`<sys.executable> <baseline>/ops/lease_publish_test.py --ab-con-noi-bo`, launched
by the unchanged suite; t125 validates actual child rc against the transcript.
The child t125 returns without recursive A/B spawning as designed. `t133` and
`t221` passed in all three executions. Independent log validation (Python inline
harness, rc 0) counted all 267 entry/pass markers in each execution, verified
identical case order, and checked all three exact positive summary lines.
Full stdout/stderr are `suite.stdout` and `suite.stderr`; verification results
are `verification.json`. Runtime warnings in subprocess output did not produce
failures or skips.

Final source verification completed at **2026-10-22 06:44:34 UTC**, rc 0:
all **4,709/4,709** source file snapshots match byte hash, size, mode and mtime;
full Git status including ignored/untracked paths, index entries and diff also
match. HEAD/tree/sole parent still match the exact identities above; HEAD remains
detached. `src-before.json` and `src-after.json`, plus paired status/index/diff
artifacts, retain the evidence. `.git` internals were not recursively snapshotted;
index contents and Git identities were checked through Git. These observations
establish no delta between snapshots, not continuous filesystem enforcement.
The runtime sandbox reports `workspace-write`, not a kernel-enforced read-only
mount for `src/`. All test and mutation writes were directed to copies or fixture
temporary directories. No source edits, repository commits/pushes, GitHub writes,
or credential use were performed.

Not run: native Git 2.55/Windows execution, standalone broad release gates, or
live CI/master readback. None are reported as passed. No approval or dependency
installation was requested, and no permission denial affected the review.

Execution-receipt boundary: at the final in-run readback, `launcher.out` and
`launcher.err` were still empty and no completed outer-launcher receipt was
available in this directory. The outer run must finish and attest its actual
model/surface, child/launcher rc, and this stable verdict's path/size/hash before
protocol §8.1 assurance can be assigned. This report is the completed technical
review artifact; it does not fabricate that receipt or claim `cross_approved`.

Final finding count: **P0=0, P1=0, P2=0, P3=1**; one class
(`mtime-order-proxy`), independently re-established on the exact reviewed head.
The user's approval threshold is zero P0/P1/P2. The scoped maintenance fix meets
that threshold; F1 remains named, nonblocking debt with the owner/fix above.

Review completed: 2026-10-22 06:45:45 UTC.

VERDICT: approve
