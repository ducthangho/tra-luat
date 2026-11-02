# Independent review — WP748 r21/g21, PR #862

- Reviewer: OpenAI Codex (GPT-6 family as identified by session instructions); provider `openai_codex`; execution surface `codex_service` with local shell tools; transport machine/tool-mediated. Exact serving-model/effort attestation is not independently measured. Independent reviewer in this session; no executor role.
- Started UTC: 2026-10-20T05:48:10Z.
- Reviewed SHA: `28e35fd9206cdc8b2b44a39999421934f8437192`.
- Reviewed tree: `f886966025dde4e2a850658a5479abbdb5bd762f`.
- Sole parent: `3950a0f9fd0a9c29a36a599edc7a2d305619fc27`, matching local `origin/master`.
- Scope: user-authorized read-only review of the one-file diff in `ops/lease_publish_test.py`; write only this verdict and throwaway review artifacts outside `src`. No credentials, GitHub mutations, commits, or pushes.
- Environment: Linux x86_64, Git 2.43.0, Python 3.13.16, PyYAML 6.0.1, actionlint 1.7.7, ShellCheck 0.9.0. Version probes returned rc 0. Git 2.55 runner failure and run ID are supplied context, not independently authenticated evidence.

## Evidence collected

1. `git -C src status --short` — rc 0; no changes.
2. `git -C src rev-parse HEAD HEAD^{tree} HEAD^ origin/master` and `git -C src show -s --format='%H%n%T%n%P%n%s' HEAD` — rc 0; identity and sole parent match the values above.
3. `git -C src diff --stat 3950a0f 28e35fd` and full file diff — rc 0; exactly one file, 31 insertions, no deletions.
4. `git --version` — rc 0; `git version 2.43.0`.
5. `git -C src symbolic-ref -q HEAD` — rc 1, confirming detached HEAD.
6. Created `review-r21.vqkj0L/head` using `git -C src archive 28e35fd9206cdc8b2b44a39999421934f8437192 | tar -x -C …/head` — rc 0. All executable review work used copies.
7. Public, unauthenticated `curl -q -fL --max-time 60 https://codeload.github.com/git/git/tar.gz/refs/tags/v2.55.0 -o …/git-2.55.0.tar.gz` — rc 22, HTTP 403. No credentials or bypass attempted. Git 2.55 execution is not measured; versioned primary sources are accessible through the web reader.

## Root cause and scope

The hypothesis is strongly supported by upstream source. Git 2.55's commit completion calls `run_auto_maintenance` after writing the commit/index. [Git 2.55 commit.c, lines 1830–1839](https://github.com/git/git/blob/v2.55.0/builtin/commit.c#L1830-L1839).

`prepare_auto_maintenance` returns before starting a child when `maintenance.auto=false`. Otherwise it constructs `maintenance run --auto` with `--detach` by default; `gc.auto` is a fallback when `maintenance.auto` is unset. [Git 2.55 run-command.c, lines 1849–1883](https://github.com/git/git/blob/v2.55.0/run-command.c#L1849-L1883).

Maintenance locks `<object-directory>/maintenance`, runs foreground work, daemonizes, runs background work, then releases the lock. This happens even if task thresholds ultimately select no background work. The lock API appends `.lock`, giving `.git/objects/maintenance.lock` in this fixture. Therefore the parent command can return while this file is still being removed, matching the reported `copytree` enumeration/open race. [Git 2.55 gc.c, lines 1683–1722](https://github.com/git/git/blob/v2.55.0/builtin/gc.c#L1683-L1722), [lockfile.c](https://github.com/git/git/blob/v2.55.0/lockfile.c).

The POSIX daemonization code explicitly transfers temporary-file ownership to the child before the parent exits, so parent exit does not remove the lock first. [Git 2.55 setup.c, lines 2045–2078](https://github.com/git/git/blob/v2.55.0/setup.c#L2045-L2078). The A/B asymmetry is consistent with scheduling variation; the supplied failure alone does not demonstrate actor-dependent Git behavior.

Git 2.43's maintenance task loop lacks that maintenance-level detach step; its tiny repository normally stays below GC thresholds. This explains why a green 2.43 run does not disprove the supplied 2.55 failure. [Git 2.43 gc.c, lines 1237–1288](https://github.com/git/git/blob/v2.43.0/builtin/gc.c#L1237-L1288).

The fix at `ops/lease_publish_test.py:5388` is sufficient for this auto-maintenance race under ordinary fixture configuration. It acts before all 27 commits; setting the keys later would not cancel a child already launched. The review does not claim to have reproduced the original runner race.

## Mutation results — Git 2.43, native filesystem

Runner: `python3 review-r21.vqkj0L/run-mutants.py`; each variant invokes `GITHUB_ACTOR=x PYTHONUTF8=1 python3 -W ignore ops/lease_publish_test.py --chi-ca=t221_` in its own copied tree. Results and complete failure messages are preserved in `review-r21.vqkj0L/mutants.log` and `mutant-*.log`.

| Variant | rc | N/N | Observed assertion |
|---|---:|---:|---|
| Exact source baseline | 0 | 1/1 | Pass |
| Remove `maintenance.auto=false` only | 1 | 0/1 | Local maintenance config absent (`rc=1`, empty output) |
| Remove `gc.auto=0` only | 1 | 0/1 | Local GC config absent (`rc=1`, empty output) |
| Move both config writes immediately after `c0` | 1 | 0/1 | Config mtime later than `c0` object |
| Move both config writes after `c2` | 1 | 0/1 | Config mtime later than `c0` object |

All four requested regression variants fail for the intended assertion here. This is configuration-policy coverage, not proof that each key is independently necessary on every Git version.

## Findings

No P0, P1, or P2 defect identified in the scoped maintenance fix.

**P3 — `t221` uses file freshness as an ordering proxy (`mtime-order-proxy`).** Location: `ops/lease_publish_test.py:5996`–`:6000`; related inaccurate “reflog” description at `:5982`. Scenario: on a coarse filesystem, config written after the first commit can have the same timestamp as that commit object and pass `<=`. Conversely, any later harmless config rewrite makes the correctly ordered fixture fail. The current fixture has no such subsequent config write, so this is a nonblocking portability/maintenance weakness, not a demonstrated current-runner failure.

- Executed `python3 -W ignore review-r21.vqkj0L/probe.py coarse-after-c0`: rc 0, **1/1**, despite the delayed-config mutant. Actual config mtime `1792475566542999320` was later than c0 `1792475566535799082`; quantizing both existing files to two-second granularity yielded `1792475566000000000`, and `t221` passed. This models timestamp resolution; it is not a Windows execution. Python documents that `st_mtime_ns` does not guarantee nanosecond precision and FAT32 mtime has two-second resolution. [Python stat documentation](https://docs.python.org/3/library/os.html#os.stat_result).
- Executed `python3 -W ignore review-r21.vqkj0L/probe.py benign-config-rewrite`: rc 1, **0/1**, at the ordering assertion after adding only `core.abbrev=7` to an already correctly built template. Both maintenance keys remained disabled.
- Equal timestamps avoid false failures caused solely by coarse granularity, but weaken regression detection; changing `<=` to `<` would create false failures. No normal checkout/reset/update-index operation in this template currently rewrites `.git/config`. Windows itself is not evidence of failure; Windows execution and native filesystem timing were not measured.
- Suggested fix/debt: owner **WP748 executor/test maintainer**. Replace the mtime comparison with an observation around a fresh fixture build: delegate all Git calls to real Git, and immediately before each commit query the real effective/local config and assert both settings. Reset or isolate `_MAU_T133` so the observer cannot inspect only a cached fixture. Retain the final local-value checks and the four mutation controls. Describe the observation accurately; Git config changes are not recorded in the commit reflog. No sleeps or strict timestamp comparison are needed.

## Actual Git subprocess evidence

`python3 -W ignore review-r21.vqkj0L/probe.py trace-head` — rc 0. Real Git Trace2 plus a delegating observer recorded one init, two config writes, 26 adds, 27 commits, 23 resets, 23 checkouts, 24 rev-parses, one rev-list, and one update-index. Both keys were disabled immediately before **27/27 commits**, including `c0`. Git emitted **zero child_start events** during this fixture build.

`python3 -W ignore review-r21.vqkj0L/probe.py trace-parent` — rc 0. The parent file came directly from `git show 3950a0f9fd0a9c29a36a599edc7a2d305619fc27:ops/lease_publish_test.py` (rc 0), outside `src`. The same fixture produced **27 `git maintenance run --auto --quiet` children** on Git 2.43. The parent does not pass `--detach` on this version. These are fixture probes, not additional full-suite runs; N/N is not applicable.

Logs: `trace-head.log`, `trace-parent.log`, their JSON result files, and `trace-head.jsonl` / `trace-parent.jsonl` under `review-r21.vqkj0L`.

## Remaining writers and other callers

- `maintenance.auto=false` blocks the shared auto-maintenance dispatch, including maintenance commit-graph/repack work. `gc.auto=0` also disables the heuristics of an explicit legacy `gc --auto`, including pack-count thresholds; it does not disable manual `git gc`. [Git GC configuration](https://github.com/git/git/blob/v2.55.0/Documentation/config/gc.adoc).
- The separate `git_test_write_commit_graph_or_die` call in commit is guarded by Git's test environment variable and writes synchronously; it is not another detached worker. [Git commit-graph.c, lines 28–39](https://github.com/git/git/blob/v2.55.0/commit-graph.c#L28-L39).
- The fixture's `init`, `add`, `reset`, `checkout -B`, `update-index`, `rev-list`, and `rev-parse` paths do not themselves dispatch auto-maintenance. Their ordinary index/ref writes finish before `_g_a0` returns. No fetch, receive, explicit GC, explicit maintenance, or scheduler registration occurs in `_mau_t133`/`_them_commit`. Source review: [init](https://github.com/git/git/blob/v2.55.0/builtin/init-db.c), [add](https://github.com/git/git/blob/v2.55.0/builtin/add.c), [reset](https://github.com/git/git/blob/v2.55.0/builtin/reset.c), [checkout](https://github.com/git/git/blob/v2.55.0/builtin/checkout.c), [update-index](https://github.com/git/git/blob/v2.55.0/builtin/update-index.c), [rev-list](https://github.com/git/git/blob/v2.55.0/builtin/rev-list.c), [rev-parse](https://github.com/git/git/blob/v2.55.0/builtin/rev-parse.c).
- These two keys are not a general ban on background processes. Inherited `core.fsmonitor=true` can independently start `fsmonitor--daemon` on supported platforms, and custom hooks/templates or explicit scheduled/manual maintenance are independent. `_g_a0` still inherits Git configuration/environment. For a stronger guarantee across arbitrary developer configurations, initialize with an empty template and isolated Git config/environment, disable `core.fsmonitor` before index operations, and exclude custom hooks. No such active writer was observed here, and none is required for the reported default Linux runner failure. This is an existing fixture-isolation boundary, not a regression introduced by this diff. [Git fsmonitor configuration](https://git-scm.com/docs/git-config/2.55.0#Documentation/git-config.txt-corefsmonitor), [independent daemon start path](https://github.com/git/git/blob/v2.55.0/fsmonitor-ipc.c#L54-L116).
- Direct `_kho_do_thi` users: `t129` (5555), `t130` (5617), `t131` (5659), `t132` (5756), `_mau_t133` (5817), `t138` (6365), `t140` (6526), `t143` (6580), `t144` (6600), `t145` (6639), `t146` (6671), `t147` (6729), `t149` (6782), `t151` (6849), and `t192` (10707), all in `ops/lease_publish_test.py`. `t133` and the `t139` mutation matrix share the cached template indirectly. No users were found in other Python files (`rg` rc 1, no matches).
- The other 14 test callers now get two local config entries and suppressed automatic housekeeping. Their commit/tree/blob data and intended assertions are unchanged. Several explicitly require loose objects, so avoiding automatic repacking is helpful. The local clone used by `t132` does not inherit source-repository config; this patch does not claim to disable maintenance in every unrelated test repository.

## Full-suite result

Executed in the exact-head archive:

```sh
cd review-r21.vqkj0L/head
GITHUB_ACTOR=x PYTHONUTF8=1 python3 -W ignore ops/lease_publish_test.py
```

- **rc 0; 267/267 passed; 0 skipped**, from 2026-10-20T05:49:30Z to 2026-10-20T05:55:33Z.
- `t125` passed in 184.081 seconds. Child A (without actor) and child B (with actor) each reported **267/267, 0 skipped**; `t125` validated their return codes/transcripts and equality.
- `t133` and `t221` passed in the parent and both A/B children. The other `_kho_do_thi` consumers also passed.
- Raw evidence: `review-r21.vqkj0L/full-suite.log`; process return code additionally saved in `full-suite.rc`.
- No sandbox block affected the requested suite or benign local probes. The optional Git 2.55 archive download was blocked with HTTP 403 as recorded above. Git 2.55 execution, Windows execution, and authentication of the supplied GitHub run are **not_run/not_measured**, not passes. No hostile payloads were authored.

## Final identity and integrity

At **2026-10-20T05:56:12Z**, repeated `git --no-optional-locks -C src rev-parse HEAD HEAD^{tree} HEAD^ origin/master` — rc 0, unchanged identity above. `status --porcelain=v1 --untracked-files=all --ignored`, `diff --exit-code`, and `diff --cached --exit-code` — all rc 0, empty. Full-SHA parent/head name-only diff — rc 0, still exactly `ops/lease_publish_test.py`.

The review's filesystem-content snapshot and final comparison matched **4,709/4,709 files** outside `.git` (comparison rc 0); no tracked, untracked, or ignored checkout changes were observed. The tested archive's `ops/lease_publish_test.py` remains byte-identical to `src`, SHA-256 `cb407cff187ebb62b17284054370bfc80222fae821f91e5fab7f235253108cf0`. Full command/results are in `review-r21.vqkj0L/final-integrity.json`. These checks establish observed content equality, not a history of every filesystem metadata operation.

Recommendation: approve this exact SHA for the scoped race fix. Zero P0–P2 findings; one nonblocking P3 test-quality debt with owner and remediation above. This technical review is not merge/land authorization.

VERDICT: approve
