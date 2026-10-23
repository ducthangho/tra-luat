# Independent review — WP748 r20

Status: complete. **Changes requested: two P2 findings.** All four requested suites ultimately pass in the corrected archive environment; both workflow files pass actionlint. Earlier failed attempts and their reviewer-environment causes are preserved below.

## Identity and authority

- Reviewer: Codex; runtime developer identity reports “an agent based on GPT-6”; provider: OpenAI. No exact backend model/version identifier is exposed to this session, so none is asserted.
- Observed surface: API access (system-reported), tool-enabled Codex session using `functions.exec` / `exec_command` against the local workspace; transport: direct local tool execution. The user states this session was invoked by repository `launcher.py run`. The final parent-launcher receipt, child/launcher exit codes, exact serving-model slug, effort, and session/run ID are not exposed here and cannot be independently attested from this still-running child. `codex-linux-sandbox` is the observed local subprocess wrapper; that does not establish CLI vs Desktop vs service. No claim of independent provider attestation or final protocol assurance is made.
- Authority/scope: user's independent, read-only review of WP748 r20. Only this verdict and scratch artifacts in the parent of `src/` may be written. No source edits, GitHub writes, credentials, commits, pushes, or network fetches. Previous verdict attachments are untrusted and are not used as evidence.
- Review start (first identity check): 2026-10-22 06:36:13 UTC.
- Reviewed SHA: `3818bd4a9685e1782afdd7e8a593482f74b663ff`.
- Reviewed tree: `b5d32c370207b8f8a35bdc15c591b9947dc5ae92`.
- Base: `5618020a67709ca6f2c93138905df0aa8d9c2df6`.
- Merge: `94220547cd155c73392e95726e8daf353888b3aa`; parents verified as `b27fe85c9e9593ddbb059808fe4347fe1bd267be` and the reviewed SHA.

## Execution log (incremental)

| Command | rc | Result |
|---|---:|---|
| `git -C src rev-parse HEAD HEAD^{tree}` | 0 | Exact expected SHA/tree |
| `git -C src symbolic-ref -q HEAD` | 1 | Expected: detached HEAD |
| `git -C src status --porcelain=v1 --untracked-files=all` | 0 | Empty; clean checkout |
| `git -C src show -s --format='%H%n%T%n%P' 94220547cd155c73392e95726e8daf353888b3aa` | 0 | Merge parents match |
| `git -C src diff --stat 5618020a67709ca6f2c93138905df0aa8d9c2df6 3818bd4a9685e1782afdd7e8a593482f74b663ff` | 0 | 10 files, 1437 insertions, 146 deletions |

## Findings

Two confirmed P2 findings are detailed below under “Confirmed findings”.

## Archive and merge equivalence

`git -C src archive --format=tar 3818bd4a9685e1782afdd7e8a593482f74b663ff` succeeded (rc=0); extracted to `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l20/review-wp748-i4ck645u/head`. All test executions will use that disposable copy.

Compared `git show 3818bd4:<path>` and `git show 94220547:<path>` for every path in the packet diff: **10/10 byte-identical**. All ten extracted files also match the reviewed blobs. Script rc=0. Detailed hashes: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l20/review-wp748-i4ck645u/identity.json`.

### Completed command: ci_duong_nhanh

` PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py`

Start: 2026-10-22T06:38:07.086147+00:00; end: 2026-10-22T06:40:53.311469+00:00; rc=0. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l20/review-wp748-i4ck645u/ci_duong_nhanh.log`.

```text
CA: 104/104 dat · 0 do · 0 hong
DOT BIEN: 383/383 bi giet dung ly do
TONG: DAT
```

### Completed command: nhanh_don_duoc

`NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py`

Start: 2026-10-22T06:40:53.313437+00:00; end: 2026-10-22T06:40:55.233946+00:00; rc=0. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l20/review-wp748-i4ck645u/nhanh_don_duoc.log`.

```text
8/8
```

## Review progress — 2026-10-22 UTC

Read all ten file diffs against the requested base, plus surrounding producer/consumer code. Read the locally available packet r20 and inherited r16 specs from `origin/ops/wp748-r20-g20-lease` at `54aca2344b87443c6a97ccc7d355d51000a26265`; no network was used. The r16 spec expressly authorizes the targeted/full split, so that split alone is not a finding. Current executable tables contain 53 baseline self-checks, 240 self mutants, and 10 product mutants (the added r553 explains the increase).

Independent receipt probe: `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python3 review-wp748-i4ck645u/probe_contracts.py`, rc=0. Existing collector counterexamples: 43/43, with three valid controls. New probes show `_loi_gop_dich` accepts invalid timestamps, end-before-start timestamps, and a 900-second timestamp span with `giay=0`; classification and final finding are under review. These are synthetic receipt probes, not real shard execution or performance evidence.

`git -C src merge-base --is-ancestor 5618020a67709ca6f2c93138905df0aa8d9c2df6 origin/master`: rc=0. Runtime tool subprocesses are enclosed by executable `codex-linux-sandbox`; this does not reveal the serving model or conclusively distinguish the user-facing Codex surface. `launcher.out` and `launcher.err` are presently empty. The parent launcher's final receipt/rc cannot yet be independently verified from inside this still-running review.

### Completed command: doc_receipt_thu_hoi

` PYTHONUTF8=1 python3 .claude/dev/doc_receipt_thu_hoi_test.py`

Start: 2026-10-22T06:40:55.234584+00:00; end: 2026-10-22T06:41:07.124760+00:00; rc=0. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l20/review-wp748-i4ck645u/doc_receipt_thu_hoi.log`.

```text
doc_receipt_thu_hoi tests: 156/156 ca QUA · 162/162 dot bien GIET
```

## Confirmed findings

### WP748-R20-F01 — P2 — timing-receipt-validation

- Location: `ops/nhanh_don_duoc_test.py:5849` (timestamp check), `:5870` (critical-path calculation).
- Scenario: `_loi_gop_dich` accepts any nonempty strings as start/end times and uses only the separately supplied `giay` to enforce the 540-second limit. A complete, correctly partitioned eight-shard receipt set with matching source hashes/head can have `bat_dau=ket_thuc="invalid"`, reversed timestamps, or timestamps spanning 900 seconds with `giay=0`; `gop_dich` returns 0 and prints `targeted_mutant_gate: DAT` in all three cases. Thus corrupt/inconsistent measurement evidence can satisfy the new performance gate. This is a receipt-validation defect, not evidence that the real Windows gate exceeded its budget.
- Evidence: `probe_time_gate.py` uses the unmodified archive module with synthetic receipts. The initial probe used a documented head-identity seam; it was repeated after adding exact Git metadata, using the real `_git_head()` with no identity mock, with identical results. Positive control passes; all three negative cases incorrectly pass. Script rc=0 means the reproduction succeeded, not that these negative cases are acceptable. Full output from the real-head repetition is in `review-wp748-i4ck645u/probe_time_gate_real_head.log`.
- Fix: parse start/end as timezone-qualified UTC datetimes, reject impossible/reversed values, and reject material inconsistency between elapsed time and the recorded interval before granting performance credit. Use an explicit tolerance or an independently validated monotonic interval for permitted clock adjustments.
- Regression test: keep the real-format valid receipt control and add each of these three negative cases to the collector's counterexamples for targeted and full modes; only targeted mode should enforce the 540-second budget.
- Risk of fix: avoid false failures from millisecond rounding or declared clock adjustments; do not silently reinterpret an invalid time as zero.

### WP748-R20-F02 — P2 — timeout-descendant-containment

- Location: `ops/nhanh_don_duoc_test.py:405`–`:411` (new timeout wrapper), used with the new shard deadlines at `:5766`.
- Scenario: `subprocess.run(..., timeout=...)` kills only its direct child. The timed process here is often a Python test harness which itself launches Git/other subprocesses. Its descendants can keep running and retaining fixture files/pipe handles after the wrapper reports `rc=124` and “con bi giet”. On Windows the runtime's timeout cleanup additionally calls `communicate()` without a new timeout, so a surviving descendant holding the inherited output pipe can prevent the configured deadline from returning at all. This undermines the new bounded-shard design and Windows timeout recovery.
- Evidence: `probe_timeout.py` launches only probe-owned processes, sets the timeout to 0.6 seconds, and observes return code 124 in approximately 0.6 seconds while the grandchild heartbeat keeps increasing afterward. The probe explicitly kills its grandchild in `finally`. Linux behavior is executed evidence; the Windows unbounded-drain consequence is code-derived from the installed Python `subprocess.run` implementation and has not been executed on Windows.
- Fix: run the harness in an owned process group/job, terminate its complete descendant tree on timeout, then perform bounded output collection and verify termination before deleting fixtures or continuing. Preserve timeout/unmeasured as a failing result. Reuse the repository's existing containment approach where practical; do not kill arbitrary or reused PIDs.
- Regression test: a child spawns a heartbeat-writing grandchild that inherits stdout; after timeout assert a bounded return, non-passing result, stopped heartbeat, and no live owned descendant. Exercise the native Windows path as well as POSIX.
- Risk of fix: process identity and group ownership must be checked to avoid terminating unrelated processes; cleanup itself must retain a deadline.

### Completed command: subagent_ghi_detect

` PYTHONUTF8=1 python3 .claude/hooks/subagent_ghi_detect_test.py`

Start: 2026-10-22T06:41:07.126174+00:00; end: 2026-10-22T06:45:01.514684+00:00; rc=1. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l20/review-wp748-i4ck645u/subagent_ghi_detect.log`.

```text
  ok   t7_agent_ngoai_tap_khong_bi_ap_luat                  agent ngoai tap -> ket_qua=None rc=0 anh_chup=0 (mong doi None/0/0)
  ok   t8_ca_hai_agent_deu_duoc_do                          2 agent x ghi -> changed 2/2
  ok   t10_agent_id_doc_hai_bi_tu_choi                      agent_id doc hai -> unknown 4/4
  DO   t21_lenh_hook_chay_duoc_khi_CLAUDE_PROJECT_DIR_KHONG_DAT lenh hook chay duoc o 2 su kien x 2 nen -> dung 2/4; SAI: ["SubagentStart/khong dat: rc=2 stdout=RONG stderr=/usr/bin/python3: can't open file '/tmp/claude-0/-home-user-tra-luat/90305cb1-28", "SubagentStop/khong dat: rc=2 stdout=RONG stderr=/usr/bin/python3: can't open file '/tmp/claude-0/-home-user-tra-luat/90305cb1-28"]
TONG: CA 44/45 dat
TONG: DIEM DOT BIEN BI TU CHOI — nen co 1 ca DO SAN (t21_lenh_hook_chay_duoc_khi_CLAUDE_PROJECT_DIR_KHONG_DAT). Sua nen xanh truoc, roi moi doc duoc so dot bien.
TONG: DO
```

### Completed command: actionlint

` PYTHONUTF8=1 actionlint .github/workflows/ci.yml .github/workflows/ci-dot-bien-du.yml`

Start: 2026-10-22T06:45:01.516402+00:00; end: 2026-10-22T06:45:01.693119+00:00; rc=0. Log: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/l20/review-wp748-i4ck645u/actionlint.log`.

```text

```

### Archive-only hook failure and reproduction correction

The first full hook suite returned rc=1, **44/45**, because t21 intentionally uses `git rev-parse --show-toplevel` when `CLAUDE_PROJECT_DIR` is unset. The plain archive has no `.git`, so Git resolved the enclosing review workspace and Python attempted to open its nonexistent `.claude/hooks` path. Mutation scoring was explicitly refused because the baseline was red; this attempt is not a pass.

Verified that all 4,645 archive source files still matched the original snapshot. Added Git metadata only to the disposable archive: `git init -q`; an `objects/info/alternates` pointer to the read-only `src` object store; `git update-ref --no-deref HEAD 3818bd4a9685e1782afdd7e8a593482f74b663ff`; `git read-tree 3818bd4a9685e1782afdd7e8a593482f74b663ff`. All commands rc=0. No commit was created, no remote configured, and no source bytes changed. Scratch HEAD/tree now match exactly and scratch `git status --porcelain=v1 --untracked-files=all` is empty. A corrected full hook rerun follows.

## Additional completed verification

All executed in the disposable archive or by scratch probes importing its unmodified files:

| Actual command | rc | Evidence |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python3 .claude/dev/ci_dang_ky_test.py` | 0 | Registration 24/24; launcher contract 4/4; Ruff installation/probe contract 3/3; counterexamples 1053/1053. This is not the full `--chay` registry execution and not bare Ruff lint. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python3 review-wp748-i4ck645u/lease_focused.py` | 0 | 6/6 targeted lease cases; skipped 0: t49, t133, t139, t154, t217 missing-blob case, t220. Includes native Linux cleanup plus the platform-independent Windows ctypes-lock mock. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python3 review-wp748-i4ck645u/probe_contracts.py` | 0 | Existing collector counterexamples 43/43; new r553 case 1/1; its named memory-layout mutant 1/1 killed. Three independent invalid-time probes accepted, as detailed in F01. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python3 review-wp748-i4ck645u/probe_time_gate.py` | 0 | Real-head repetition: valid control 1/1 accepted; invalid receipts 3/3 also accepted (the defect). Synthetic receipts, not real shard scores. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python3 review-wp748-i4ck645u/probe_timeout.py` | 0 | Timeout reproduction 1/1: rc124 at 0.602 s; grandchild heartbeat 5→9 afterward; cleanup performed by the probe. |
| `git -C src diff --check 5618020a67709ca6f2c93138905df0aa8d9c2df6 3818bd4a9685e1782afdd7e8a593482f74b663ff` | 0 | No whitespace errors. |

Environment: Linux x86_64; Python 3.13.16; Git 2.43.0; GNU Bash 5.2.21; actionlint 1.7.7; PyYAML 6.0.1; jsonschema 4.26.0. Installed dependency versions are reported as measured; no dependency was installed. CI's PyYAML pin is 6.0.3, so this is not an exact CI environment reproduction.

Not run/not measured: native Windows tests and timing; full Windows registry/G5; the full lease suite; the full 240-self-mutant matrix; actual eight-shard PR/full-audit execution; live GitHub required-check status, branch protection, or owner approval; bare Ruff lint. The requested lightweight branch command intentionally disables mutation testing and supplies only 8/8 product-case evidence. The hook suite tests synthetic detector payloads and does not prove that the platform invokes the hook or enforces SubagentStop exit 2.

## Scope assessment

- Windows fixture changes preserve the reviewed assertions: t217 makes the loose object writable before deletion; executable-mode fixtures assert the Git index mode; symlink fixtures create actual links and still fail when the capability is absent. The Windows socket branch explicitly remains a logic-only simulation, not native socket evidence. Native Windows behavior was not rerun here.
- The t133 cache builds one fixture graph but copies it afresh before each invocation; the t191 change compiles the freshly written mutant bytes once while still creating new module namespaces. The focused lease run exercises t133 and its t139 mutation catalog.
- The added Git-ignore filter preserves tracked tests and fails closed if Git cannot measure ignore status. The new registry dependency/result checks reject failed/skipped shard aggregation. Contract tests and mutation tests remain present; full-audit execution is separately scheduled/manual as authorized by the inherited r16 spec. No conclusion about actual GitHub branch protection or a completed candidate full audit is possible offline.
- Complete packet diff artifact: `review-wp748-i4ck645u/packet.diff`, 143,241 bytes, SHA-256 `db25e7080739676549a745e629edb3175845d8098bb7489eb5d3ea0d2acdb17b`; generated with `git -C src diff --no-ext-diff --no-textconv 5618020a67709ca6f2c93138905df0aa8d9c2df6 3818bd4a9685e1782afdd7e8a593482f74b663ff`, rc=0.

Review classes: F01 = timing-receipt-validation (P2); F02 = timeout-descendant-containment (P2). No P0/P1 findings identified. Earlier attached verdicts were neither read nor copied. This is a review of the specified code, not permission to merge, land, or release.

### Full hook rerun with exact Git metadata

`PYTHONUTF8=1 python3 .claude/hooks/subagent_ghi_detect_test.py` (also `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`), rc=1. Start: 2026-10-22T06:47:00.304925+00:00; end: 2026-10-22T06:50:33.537440+00:00.

```text
TONG: CA 45/45 dat · DOT BIEN 24/25 bi giet
TONG: DO
```

Log: `review-wp748-i4ck645u/subagent_ghi_detect_with_git.log`.

### Second hook attempt: reviewer environment interference

The metadata-corrected run returned rc=1: baseline 45/45, hook mutants 24/25; `m2_bo_no_optional_locks` survived. This was caused by the review runner's own extra `GIT_OPTIONAL_LOCKS=0`, which masks the effect of removing `--no-optional-locks`. A direct A/B probe of t13 against that mutant returned `(True, index unchanged)` with the override and `(False, index changed)` with it unset, rc=0 for the probe. This is not classified as a packet defect. The final full rerun explicitly unsets that variable; all source files and Git identity are retained. Both failed attempts remain failed in this log.

### Full hook rerun with exact Git metadata and no lock override

`PYTHONUTF8=1 python3 .claude/hooks/subagent_ghi_detect_test.py` (also `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS` unset), rc=0. Start: 2026-10-22T06:51:22.520813+00:00; end: 2026-10-22T06:55:05.428987+00:00.

```text
TONG: CA 45/45 dat · DOT BIEN 25/25 bi giet
TONG: DAT
```

Log: `review-wp748-i4ck645u/subagent_ghi_detect_final.log`.

## Final execution summary

| Requested check | Final rc | Positive evidence |
|---|---:|---|
| `PYTHONUTF8=1 python3 ops/ci_duong_nhanh_test.py` | 0 | 104/104 cases; 383/383 mutants killed |
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py` | 0 | 8/8; mutation phase not run as requested |
| `PYTHONUTF8=1 python3 .claude/dev/doc_receipt_thu_hoi_test.py` | 0 | 156/156 cases; 162/162 mutants killed; 9 equivalents verified, 0 unresolved |
| `PYTHONUTF8=1 python3 .claude/hooks/subagent_ghi_detect_test.py` | 0 | 45/45 cases; 25/25 hook mutants; 11/11 test-harness mutants and 1/1 settings mutant killed |
| `actionlint .github/workflows/ci.yml .github/workflows/ci-dot-bien-du.yml` | 0 | 2/2 workflow files; no diagnostics |
| Per-path `git show` byte comparison of reviewed head against merge `94220547cd155c73392e95726e8daf353888b3aa` | 0 | 10/10 identical |

The extra environment used by the archive runner was `PYTHONDONTWRITEBYTECODE=1`; the initial runner also set `GIT_OPTIONAL_LOCKS=0`, whose interference with the hook mutation phase is documented above. The final hook invocation unsets that variable. No case or assertion was disabled to obtain the final result.

Final verification UTC: 2026-10-22T06:55:13.640438+00:00. Reviewed SHA/tree remain `3818bd4a9685e1782afdd7e8a593482f74b663ff` / `b5d32c370207b8f8a35bdc15c591b9947dc5ae92`. Source regular-file content comparison: **4645/4645 unchanged**. `GIT_OPTIONAL_LOCKS=0 git -C src status --porcelain=v1 --untracked-files=all --ignored`, `git -C src diff --name-only`, and `git -C src diff --cached --name-only` all return rc=0 with empty output. These endpoint checks prove no observed content delta; they do not attest every intermediate filesystem operation.

No source edits, commits, pushes, GitHub comments, credential use, or network fetches were performed. Changes are confined to this verdict and review scratch artifacts in the parent directory. The parent launcher must still finalize and verify its execution receipt after this child exits; this document does not fabricate that receipt or assert unmeasured model/session assurance.

Final finding count: P0=0; P1=0; **P2=2**; P3=0. The severity threshold for approval is not met.

VERDICT: changes_requested
