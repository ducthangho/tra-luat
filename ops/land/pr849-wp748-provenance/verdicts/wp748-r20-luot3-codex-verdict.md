# Independent read-only re-review — WP748 r20/g20, PR #849, round 3

- Reviewer: OpenAI Codex, GPT-6 family as identified by this runtime; exact served model identifier is not exposed. Provider `openai_codex`, execution surface local Codex shell tools, transport `machine`.
- Review started: 2026-10-19T18:44:17Z (UTC).
- Reviewed SHA: `99836157fdffe2681280a8302c8c7396ac5fe4de`.
- Reviewed tree: `b05dcbfeccba9d836c7b9cf106b60861bd6f9626`.
- Parent: `1e5522383433d1c544ec89585c9ef874aed0138e`, exactly the requested round-2 baseline.
- Authority/scope: user's independent, read-only, delta-only review. `src/` is initially clean and detached. No source edits, commits, pushes, GitHub comments, or credentials are authorized or needed. Reviewer artifacts and disposable copies are outside `src/`, inside this workspace.
- Read round-2 approval in `VERDICT_LUOT2.md`; its previously escalated enforcement obligation is unchanged and outside this delta.

## Evidence recorded so far

- `git -C src status --porcelain=v1`: rc 0, empty.
- `git -C src rev-parse HEAD 'HEAD^{tree}' HEAD^`: rc 0, identifiers above.
- `git -C src symbolic-ref -q HEAD`: rc 1, empty (expected for detached HEAD).
- `git -C src diff --stat 1e55223 9983615` and `git -C src diff 1e55223 9983615`: rc 0; read the complete one-file delta, 45 insertions / 4 deletions in `ops/nhanh_don_duoc_test.py`.

Evidence below was appended incrementally as measured; review is now complete.

## Measured layout and regression evidence (incremental)

Scratch: `review-r3.W0wKSk/`. Logs and JSON command receipts are in its `logs/` directory. Commands use `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`, scratch-local `TMPDIR`, isolated Git global/system configuration, and disabled terminal prompts. Initial snapshot recorded all 4,645 files outside `.git`, clean tracked/untracked/ignored status, HEAD/tree/parent, detached state, and empty worktree/index diffs.

- Requested baseline: `cd src && NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py` — rc **0**, **8/8** passed. This light mode does not execute `r553`; that case is measured separately.
- `python3 review-r3.W0wKSk/layout_probe.py` — rc **0**. Eight documented-layout models passed (**8/8**, four structures × Win32/Win64 widths); baseline `r553` controls passed **2/2**; deliberately wrong layouts were rejected **12/12**, using native Linux DWORD and simulated Win64 DWORD widths.
- Wrong layouts: six, seven, or nine total SIZE_T slots; `peak_ws` moved to the second or last SIZE_T slot; or `peak_ws` moved before the page-fault DWORD. Rejections are `TinHieuChotCa` for `r553`, not import errors or other infrastructure failures. For six/seven slots, traced fake psapi returns 0, the actual helper returns `(None, "KHONG DO DUOC: API tra 0")`, and the case fails. For nine slots and the DWORD reorder, the fake can return success but the exact-eight assertion rejects the layout.

Microsoft's [PROCESS_MEMORY_COUNTERS definition](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters) documents two DWORDs followed by eight SIZE_T values. At `ops/nhanh_don_duoc_test.py:5668`, `peak_ws` plus seven trailing slots correctly represents that layout; `x6` supplies `PeakPagefileUsage`. Windows DWORD is 32 bits, and SIZE_T follows pointer width ([Windows data types](https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types)). Derived sizes: Win64 **72 bytes**, `peak_ws` offset **8**; Win32 **40 bytes**, offset **8**. The prior Win64 layout was 64 bytes. On this Linux host DWORD is 8 bytes: the fixed helper is 80 bytes and the old one 72 bytes, so a naive absolute 72-byte fake would miss the defect. The new slot-relative test distinguishes them correctly.

The unchanged job-path structs at `ops/nhanh_don_duoc_test.py:5656–5666` also match their documented fields and order: [IO_COUNTERS](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-io_counters), [JOBOBJECT_BASIC_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information), and [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information). Independently calculated/measured sizes are `_IO` 48/48, `_CB` 64/48, `_EXT` 144/112 bytes (Win64/Win32); `peak_j` offsets 136/108. `c_longlong` represents each LARGE_INTEGER, `c_ulonglong` each I/O counter, and `c_size_t` the SIZE_T/ULONG_PTR fields. These are ABI models on Linux, not native Windows execution.

## Completed commands and counts

All measurements ran on Linux, Python 3.13.16. `S` below means `review-r3.W0wKSk`; each probe was run through `python3 S/run_logged.py <label> <cwd> <command...>` so its actual exit status and output are retained.

| Command / measurement | rc | Result |
|---|---:|---|
| In `src/`: `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 PYTHONUTF8=1 python3 ops/nhanh_don_duoc_test.py` | 0 | **8/8** product cases passed |
| `python3 S/mutant_probe.py` → `chay_dot_bien_tu_kiem([ram-pmc-thieu-truong])`, default `chi_dich=False`, in a two-file scratch copy | 0 | **1/1** self-mutant killed, result `(1, 0, 0)`; mutant child rc **1** expected, **52/53** passed, only `r553` emits `DO_CHOT`; wrong-reason failures **0**, unmeasured **0** |
| `python3 S/layout_probe.py` | 0 | **8/8** structure/architecture models; **2/2** positive `r553` controls; **12/12** deliberate bad layouts rejected |
| `python3 S/raw_api_probe.py` | 0 | **5/5** Win64-width raw-buffer scenarios, detailed below |
| `python3 S/table_probe.py` | 0 | **240/240** anchors unique outside the table; **240/240** unique mutant names; **53/53** required cases/cost entries/target coverage; **14/14** complete disjoint partitions; **43/43** aggregate counterexamples including 3 valid controls; deleting the floor exposes exactly **2/2** below-floor cases |
| Repository-wide 52/239 literal search (command below) | 0 | 1,753 literal matches retained in `S/count-literals.txt`; executable/configuration uses inspected for coupling to this suite |
| `git -C src diff --check 1e55223 9983615` | 0 | No whitespace errors |

Literal-search command: `rg -n --hidden -g '!**/.git/**' '\b(52|239)\b' src > review-r3.W0wKSk/count-literals.txt`.

The named-mutant child log is retained in `S/logs/mutant-children.json`: it ran every registered case, printed `TU KIEM: 52/53`, exited 1, and had empty stderr. The runner validated its completion proof and exact failing-case set. This is one mutant across all 53 cases, **not** a 240-mutant audit.

The independent raw-buffer probe writes values at documented byte offsets, not via the helper's field names. It verifies no-job fallback returns **512 MB** from offset 8, despite a different current working-set value at offset 16; the job path returns **1024 MB** from offset 136, despite a different process peak at offset 128; failed or zero-peak job queries fall back to 512 MB; the old seven-slot buffer is rejected. The real helper passes the computed structure byte size to [GetProcessMemoryInfo](https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getprocessmemoryinfo) and uses information class 9 for [QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject), consistent with those API contracts. These five results are simulated API evidence; no native Windows process was run.

## Coverage, anchors, and count-dependent behavior

The independent anchor audit excludes the top-level `DOT_BIEN_TU_KIEM` AST assignment and counts each anchor separately in the source prefix and suffix, matching the runner's permitted mutation regions. All **240/240** entries have exactly one occurrence. The new anchor at `ops/nhanh_don_duoc_test.py:4926` uniquely selects the struct declaration at `:5669`.

`TU_KIEM`, `NHOM_BAT_BUOC`, `GIAY_CA_HO_SO`, and declared self-mutant targets agree on **53/53** cases. Both `_muc_dich` modes yield **303** work items: **53** cases + **240** self-mutants + **10** product mutants. For every allowed shard count, 2 through 8, both modes produce complete, disjoint partitions (**14/14** configurations). The required-group validator returns no errors for the current tables.

At `ops/nhanh_don_duoc_test.py:5960`, the new `SAN_NHOM - 1` fixture contains exactly **52 real, covered cases**. It has no missing/unknown group, and fails solely because the required-group count is below 53. The complete built-in counterexample set passes **43/43**. Removing only the floor guard in a separate copy lets precisely `nhom-duoi-san` and `nhom-duoi-san (du)` escape; the other cases remain correct. This verifies that the rewritten counterexample still detects deletion of the floor guard in both modes.

No executable limit, loop, membership check, parser, or partition in this suite or its CI callers was found to rely on the old 52/239 totals. Remaining references are commentary/docstrings/history, unrelated values, and the pre-existing informational full-audit label `DU 52 ca moi con` at `ops/nhanh_don_duoc_test.py:6001`. That label is stale, but its actual numerator/denominator and execution derive from the tables; it does not truncate execution or break aggregation and is not raised as a finding. The named-mutant child independently demonstrates 53-case execution.

## Findings P0–P3 and ĐỐI CHIẾU LƯỢT TRƯỚC

**No new P0, P1, P2, or P3 finding in this delta.**

- Connector P2, class `ram-pmc-truncated-layout`: **closed / ĐÃ VÁ THẬT**. Location: `ops/nhanh_don_duoc_test.py:5669`. Scenario: Windows `job=None` fallback previously supplied a seven-SIZE_T buffer and could not measure RAM. Fix present: add the eighth SIZE_T (`PeakPagefileUsage`), preserving `peak_ws` at the documented offset. Independent layout, raw-buffer, direct-case, and named-self-mutant checks above verify the fix and regression protection. No additional fix is requested.
- Round-2 R1, `full-audit-enforcement`: remains **escalated / CHƯA VÁ**, with the prior approval disposition inherited from `VERDICT_LUOT2.md`; this one-file delta does not change enforcement. No claim that external enforcement now exists.
- Round-2 R2, `mandatory-group-validation`: closure retained. The affected counterexample and shared validator were rechecked here; coverage is now 53/53, and both below-floor modes retain their failure behavior.
- Round-2 R3, `shared-ctypes-signature-race`: closure retained from round 2; its source is unchanged by this delta. Its separate concurrency probes were not rerun.

No credentials, source edits, commits, pushes, GitHub connector calls, or GitHub comments were used. Only public Microsoft documentation was fetched. Not run: native Windows tests, hosted CI, live enforcement inspection, full targeted shards, or all 240 self-mutants. `r553` is a focused regression test, not an exhaustive proof against every conceivable malformed ABI; the independent documented-offset checks supplement it.

## Final identity and checkout integrity

Review completed: **2026-10-19T18:49:40Z** (UTC). Final identity checks return the same reviewed SHA `99836157fdffe2681280a8302c8c7396ac5fe4de`, tree `b05dcbfeccba9d836c7b9cf106b60861bd6f9626`, and sole parent `1e5522383433d1c544ec89585c9ef874aed0138e`.

`python3 S/snapshot.py src S/after.json` — rc **0**; `cmp S/before.json S/after.json` — rc **0**. All **4,645/4,645** file-content hashes match, and tracked/untracked/ignored status, HEAD/tree/parent, detached state, worktree diff, and index diff are unchanged. `git -C src rev-list --parents -n 1 HEAD` — rc **0**, exactly the reviewed commit and the single required parent. Actual command receipts are in `S/logs/final-integrity.json`. The workspace sandbox permits writes; the review deliberately kept writes outside `src/`. Matching snapshots prove no observable delta at those two times, not continuous filesystem immutability.

VERDICT: approve
