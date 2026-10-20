# Independent read-only re-review — WP748 r20/g20, PR #849, round 2

- Reviewer: OpenAI Codex, GPT-6 family as identified by the agent runtime; exact served model identifier is not exposed. Provider `openai_codex`, execution surface local Codex shell tools, transport `machine`.
- Reviewed SHA: `1e5522383433d1c544ec89585c9ef874aed0138e`
- Reviewed tree: `4a4bbf5b3a84a32773ad9b4e798e1d8c4ddc45c3`
- Review started: 2026-10-19 18:30:37 UTC.
- Review completed: 2026-10-19 18:36:56 UTC.
- Disposition: approve under the user's explicit exception for escalated R1; R2/R3 closed, no new findings.
- Scope/authority: user's independent read-only round-2 review instruction; no edits to `src/`, commits, pushes, GitHub comments, or credentials.
- Identity: detached HEAD, initially clean; `git -C src merge-base --is-ancestor 9d471d90b959d98142373085e1a504ba1d9a58c3 HEAD` returned 0. `git -C src rev-parse HEAD HEAD^{tree}` returned the full identifiers above (rc 0).
- Read: `VERDICT_LUOT1.md` and the complete `git -C src diff 9d471d9 1e55223` (rc 0; all three changed files).

## ĐỐI CHIẾU LƯỢT TRƯỚC — finding status

- R1 — P2 — **escalated** to the repository owner per the user's instruction. No enforcement fix is present in this diff; this review will not claim R1 is closed or independently verify external enforcement.
- R2 — P2 — **closed / ĐÃ VÁ THẬT**. Shared validation at `ops/nhanh_don_duoc_test.py:5471`, called by legacy aggregation at `:5468` and targeted/full aggregation at `:5833`, enforces both mandatory coverage and the floor. Independent validator fixtures pass 15/15 scenarios (five table states × three aggregate paths), including valid controls and rejections for missing mutants, an unknown required group, a reduced required-group count, and a missing required case with correspondingly adjusted cost/mutant tables. Invalid receipts match the changed tables; the low-level validator rejects them solely with `nhom bat buoc ...` errors, not incidental partition/hash errors. Both public aggregate entry points reject invalid cases as well. These are synthetic validator fixtures, not evidence of a full mutant audit.
- R3 — P2 — **closed / ĐÃ VÁ THẬT** within the reported Windows lease-test cleanup path. The identity recheck at `ops/lease_publish_test.py:4927` now shares `_KHOA_CHUP_CAY_WINDOWS` with the snapshot at `:4897`. t220 at `:13140` passes 1/1, and removing only the new lock makes it fail 0/1, rc 1, specifically naming `_khoa_danh_tinh` outside the lock. A rebuilt probe using the actual launcher `_khoa_danh_tinh`, actual helper, real ctypes argument checking, and harmless Win32 substitutes passes serial controls 2/2 and each concurrent scenario 2/2. The unlocked copy reproduces one `ctypes.ArgumentError` per pair in both recheck/recheck and recheck/snapshot schedules. Native Windows is not measured.

Stable round-1 classes retained: R1 `full-audit-enforcement` (escalated, not fixed); R2 `mandatory-group-validation` (closed); R3 `shared-ctypes-signature-race` (closed in the reported helper). No new P0–P3 finding has been identified.

## Evidence log

Environment: Linux, Python 3.13.16. The full three-file diff and relevant aggregate, mutation-runner, Windows cleanup, caller, and workflow contexts were reviewed. No executor test result was counted as independently measured evidence.

Scratch: `review-r2.CNd6Jx/`. The requested commands ran directly in `src/`, with `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`, workspace-local `TMPDIR`, and isolated Git configuration (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`). The wrapper records each actual child rc and stdout/stderr in `review-r2.CNd6Jx/logs/`.

| Requested command (cwd `src/`) | rc | Result |
|---|---:|---|
| `PYTHONUTF8=1 python3 ops/lease_publish_test.py --chi-ca=t220` | 0 | 1/1 passed; skipped 0 |
| `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py` | 0 | 8/8 passed |
| `PYTHONUTF8=1 python3 .claude/dev/idiom_py_test.py` | 0 | 7/7 passed; skipped 0; 9/9 self-mutants detected |

The idiom suite reports 526 bare calls outside its defined scope as existing diagnostic debt, not a failure. t220 emits existing SyntaxWarnings at lease-test lines 2961/5104, unrelated to the changed lines. Before testing, a content snapshot covered all 4,645 checkout files outside `.git`, plus HEAD/tree, status including ignored files, and worktree/index diffs; all Git status/diff outputs were empty.

## Negative controls and regression checks

Every mutation is confined to a separate copy under scratch; `prepare_copies.py` asserts unique replacement anchors. Logs retain actual child return codes, including expected failures.

| Command / scope | rc | Observed evidence |
|---|---:|---|
| `python3 S/r2_probe.py src` | 0 | 15/15 independent aggregate scenarios; built-in counterexamples 43/43 (3 valid controls); all 239/239 self-mutant anchors unique outside the table; 24/24 exception-restoration probes; post-fault control 43/43; legacy `gop-bo-kiem-nhom` and `gop-bo-kiem-san` correctly killed 2/2, unmeasured 0 |
| In `src/`: `python3 ops/nhanh_don_duoc_test.py --gop-dich ../S/synthetic-validator-fixtures/valid/targeted` | 0 | 43/43 counterexamples; 8/8 synthetic receipts accepted. Validator control only; printed mutant/case counts are fixture values, not measured execution results |
| In `src/`: `python3 ops/nhanh_don_duoc_test.py --gop-du ../S/synthetic-validator-fixtures/valid/full` | 0 | 43/43 counterexamples; 8/8 synthetic receipts accepted. Validator control only; no full-audit execution claimed |
| In `S/r2-remove-call`: `python3 ops/nhanh_don_duoc_test.py --gop-dich ../synthetic-validator-fixtures/valid/targeted` | 1 (expected) | Removing only the new aggregate helper call lets all six new table counterexamples escape (three in each mode); CLI reports `PHAN CHUNG LOT` and fails before consuming supplied receipts |
| In `S/r2-remove-coverage`: same targeted aggregate command | 1 (expected) | Replacing the helper's missing-group set with `set()` exposes four counterexamples, two in each mode |
| In `S/r2-remove-floor`: `python3 ops/nhanh_don_duoc_test.py --gop-du ../synthetic-validator-fixtures/valid/full` | 1 (expected) | Removing only the floor condition exposes both below-floor counterexamples |
| In `S/r3-unlocked`: `python3 ops/lease_publish_test.py --chi-ca=t220` | 1 (expected) | 0/1 passed, skipped 0; assertion specifically identifies the unlocked launcher identity call |
| `python3 S/r3_race_probe.py src fixed` | 0 | 3/3 expected scenarios; serial 2/2, concurrent identity/identity 2/2, concurrent identity/snapshot 2/2; handles closed 2/2 each |
| `python3 S/r3_race_probe.py S/r3-unlocked unlocked` | 0 | 3/3 expected negative-control outcomes: serial 2/2; each concurrent pair yields one success and one real `ArgumentError: expected LP__FILETIME instance instead of pointer to _FILETIME`; handles closed 2/2 each |
| In `S/idiom-bare`: `python3 .claude/dev/idiom_py_test.py` | 1 (expected) | Restoring the two old bare calls yields 6/7; `khong_con_goi_tran` identifies both exact calls at skill lines 267/268. The suite correctly refuses to publish a mutant score on a failing baseline |
| `git -C src diff --check 9d471d9 1e55223` | 0 | No whitespace errors |

Here `S = review-r2.CNd6Jx`. The `run_logged.py` wrapper records cwd, command, rc, elapsed time, and output in `S/logs/*.json` / `*.log`; it applies the environment documented above.

Exception restoration was tested in both modes for each of the three changed global-table scenarios, injecting a sentinel exception at directory creation, partition calculation, receipt writing, and aggregate validation. Both object identity and content were restored for `NHOM_BAT_BUOC`, `DOT_BIEN_TU_KIEM`, `TU_KIEM`, and `GIAY_CA_HO_SO`. The `finally` at `ops/nhanh_don_duoc_test.py:5932` encloses all operations after a global is replaced. The new triple return from `_phan_chung_gop_dich` has exactly one production caller, updated to unpack three values.

Windows call-site audit: the two direct launcher calls reachable by concurrent Windows cleanup are the snapshot (`ops/lease_publish_test.py:4898`) and held-handle identity recheck (`:4928`); both are locked. Snapshot-internal identity calls in `.claude/dev/launcher.py:555` execute under that same outer lock. The unlocked lease-test call at `:5020` is in the POSIX `killpg`/`getpgid` branch; the calls around `:7294` are inside `if os.name == "posix"`. The remaining threads tail log files, and the main case loop runs sequentially. t125 child suites run in separate processes, with separate ctypes state. No additional concurrent Windows launcher call outside the lock was found in this test process. The helper's other Win32 calls use a per-invocation `ctypes.WinDLL` wrapper and stable wintypes signatures. The launcher itself still uses mutable shared signatures; this scoped closure does not claim to make arbitrary external concurrent launcher callers safe.

R1 remains escalated: reviewed `.github/workflows/ci.yml:970`, `.github/workflows/ci-dot-bien-du.yml:13`, and `.claude/dev/packet_loop.py:2390`; the unconditional light registry path, schedule/manual full audit, and required-check list remain unchanged. Owner action is still needed to enforce successful full-audit evidence on the exact candidate SHA, rejecting absent/skipped/failed/stale or targeted-only evidence. External enforcement and live GitHub settings were not queried.

## Final identity, checkout integrity, and limits

Final `git -C src rev-parse HEAD HEAD^{tree}` returned 0 and the exact reviewed SHA/tree above. Final ancestry check returned 0. `git -C src symbolic-ref -q HEAD` returned 1 with empty output, confirming detached HEAD. `git -C src status --porcelain=v1 --ignored` returned 0 with empty output. `python3 S/snapshot.py src S/after.json` returned 0; `cmp S/before.json S/after.json` returned 0: all 4,645/4,645 file content hashes, ignored/untracked status, HEAD/tree, and worktree/index diffs match. This establishes no observable checkout delta at the two snapshots; it does not claim continuous filesystem immutability. The filesystem permits workspace writes, while this review kept all deliberate writes outside `src/`.

No credentials, network/GitHub operations, source-repository commits, pushes, or comments were used. Required tests used temporary local fixtures; mutation copies and reviewer scripts remain under `S/` for inspection. The round-1 verdict is unchanged.

Not run: native Windows execution, hosted CI, live owner enforcement/rulesets, full lease suite, all targeted execution shards, or the full 239-by-52 mutant audit. Synthetic receipt controls and Windows API simulations are explicitly limited as described above. R1 is still an unresolved enforcement obligation owned by the repository owner; the approval exception is the user's review instruction, not evidence that enforcement exists or authorization to merge/land.

No open P0/P1/P2 findings remain in this review other than escalated R1; no new P3 findings.

VERDICT: approve
