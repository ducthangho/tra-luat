# Independent review — WP748 r25/g25, PR #909, round 1

Reviewer: OpenAI Codex. Runtime instructions identify this agent as Codex based on GPT-6; this is a runtime declaration, not an independently verified server-model attestation. Provider: `openai_codex`; actual review used tool-mediated local shell execution in a managed Linux environment (`transport: machine`). The user reports invocation through `launcher.py run`; its enclosing execution receipt/run ID and exact serving-model field were not exposed in this directory and could not be independently verified. Installed CLI version is separately measured below. GitHub submitter: none; nothing published. This is a fresh reviewer context, not an executor context.

Requested and observed HEAD: `83d305fbf63d5978189a9796141e3d547a46b2c6`.
Requested and observed tree: `e45f3a1adad806256871ca8c7abc7338a150b705`.
Initial `git -C src status --porcelain=v1`: empty (clean). Detached status is being separately recorded.

Scope: read-only review of `src/`; only this verdict and local scratch evidence may be written. No commits, pushes, GitHub comments, or credential use.

Review started UTC: `2026-10-24T09:52:15Z`.

Identity/preflight evidence: `git -C src symbolic-ref -q HEAD` rc=1, no output (detached); `git -C src merge-base e739ac1b74024a20949425c447fb6cf025317c0e HEAD` rc=0, output `e739ac1b74024a20949425c447fb6cf025317c0e`. Lease base `1c20f3bd6a7ed08114feaf1d91c0790360b8f581` is an ancestor (rc=0). Delta commits: `fea07f1`, `56263ec`, `83d305f`.

`git -C src diff --numstat e739ac1b74024a20949425c447fb6cf025317c0e 83d305fbf63d5978189a9796141e3d547a46b2c6` rc=0:

```text
87  3  .claude/dev/launcher.py
131 0  .claude/dev/launcher_test.py
```

Exactly 2 files, 218 additions, 3 deletions: within ADR-0053's 6-file/450-addition ceiling (also within the older 3-file/300-addition ceiling).

Spec lookup on `master` rc=128: path absent. Fallback `git show origin/ops/wp748-r25-g25-lease:ops/specs/wp748-r25-launcher-model-phuc-vu.md` rc=0; SHA-256 `5f85d350bc78a28693b1cb095bfa2fa62353975c3ba0e714a2a59c6e8e4dafa3` matches. Authority is the spec's quoted #748 issuecomment-6378484722; no authenticated GitHub access used.

Scratch evidence: `review-scratch.Dggq2S/`. Initial test attempts exposed an environment limitation: the sandbox supplies a read-only `/tmp/.git`, so launcher refuses a temporary `CODEX_HOME` beneath `/tmp` (fake Codex child rc=13, `CHAN [13]: CHỜ snapshot Codex mới; không lặp credential đã thất bại`). Initial baseline: 2/5; the 3 fake-Codex cases fail before launch with missing `runs` directories. These are not mutation kills or PR regression evidence. A rerun uses a verified nonexistent `CODEX_HOME` outside `/tmp`, without reading or using credentials. Original logs and command outputs are retained.

Targeted execution complete: baseline **5/5**, no skips; supplied mutants **8/8 killed by intended assertions**, each baseline rc=0 and each mutant rc=1. `commands.jsonl` contains the exact commands, rc, elapsed times, and output. Only launcher copies were mutated; test and policy files were copied unchanged.

Additional guard-removal experiments reuse all five existing tests without adding attack content. **5/5 additional mutants survive (25/25 test executions pass)**: remove ANSI stripping; dedupe by response ID only; remove accepted-event-type validation; omit `not loi_loc` from status; remove the 10-second join bound. These demonstrate gaps in the claim that every guard has an effective mutant.

Benign observation commands:

- `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.Dggq2S/observations.py fixtures`, rc=0: `existing fixture filter: {"kept_bytes": 98, "models": [{"response_id": "resp_q", "model": "gpt-6-astra", "su_kien": "response.created"}], "errors": []}`; `inherited RUST_LOG: codex_core=debug,tungstenite::protocol=trace`; `filtered stderr: {"rc": 0, "bytes": 98, "ledger_bytes": 98, "hash_matches": true}`.
- `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.Dggq2S/observations.py grandchild`, rc=0: `grandchild: {"rc": 0, "elapsed_s": 10.37, "status": "DO_DUOC", "note": "ong stderr con mo sau 10s (hau due giu ong); danh sach co the thieu", "model_count": 1}`. The descendant only sleeps and holds stderr; no attack payload.
- Isolated `/opt/node22/bin/codex --version`, rc=0: `codex-cli 0.163.0` (plus expected warning that the deliberately absent Codex home cannot hold PATH aliases). This verifies the installed CLI, not this review's serving model.

## Findings recorded during review

**R25-SEC-01 — P1 — `.claude/dev/launcher.py:1622` / `:1627` / `:1642` (LỖI, source-proven fail-open classification).** The stream starts in pass-through mode; only the precise timestamp/level regex turns suppression on. Unrecognized trace/debug formatting before a recognized trace, including a timestamp-free line or unsupported leading control sequence, is written verbatim. A recognized INFO/WARN/ERROR line turns suppression off regardless of content. It also exposes subsequent continuations of a previously suppressed multiline record if another record interleaves. These are deterministic branches in the source, not claims that a live credential leak was reproduced. No new exploit payload was authored. Appending the target to arbitrary inherited `RUST_LOG` (`:1776`) also retains other verbose targets; the existing-fixture observation above measured that behavior.

Fix direction: at the capture boundary, use a supported, bounded record format/source whose trace records cannot be confused with ordinary stderr, constrain measurement logging to the required target, and fail closed on ambiguous trace data. Address all output sinks before enabling credential-bearing trace. Preserve normal diagnostics through an explicit safe path. Add fixture/mutant pairs for timestamp-free/unsupported-prefix records, multiline records with timestamp-like continuations, and interleaving with non-trace records; the implementer must author these fixtures. Risk of the fix: over-suppression can discard useful ordinary stderr, so preservation must be tested separately.

**R25-MEAS-02 — P2 — `.claude/dev/launcher.py:1629` (LỖI, missing provenance check).** The parser searches for `Received message ` anywhere in any recognized TRACE/DEBUG line. It never checks the target is `tungstenite::protocol`, nor that the phrase begins the record's actual message. Thus a different enabled target's client-side/echoed content with the same suffix can populate the purported server-response ledger and set `DO_DUOC`. A valid event schema is not proof of its origin. Code inspection confirms `target required by parser: False`; no spoofing payload was generated.

Fix direction: parse and require the exact log envelope/target and receive-event position (prefer a structured receive-event channel), then validate the nested response using strict UTF-8 and nonempty identifiers. Add negative tests for another target, embedded marker, wrong event type and malformed input, plus mutants that remove each check. Risk: format changes must yield `KHONG_DO_DUOC` with a clear reason, rather than silently accepting fallback sources.

**R25-TEST-03 — P2 — `.claude/dev/launcher_test.py:6442` / `:6500` / `:10189` (LỖI, guard coverage is incomplete).** All eight supplied mutants are meaningful and killed, but five additional guard-removal mutants survive all five new tests: ANSI stripping, ID+model dedupe (ID-only mutant), event-type validation, error-aware `DO_DUOC`, and bounded reader join. The crash test calls the reader directly and never tests the final ledger after positive evidence followed by a reader error. The current dedupe fixture never gives the same response ID different models. The timeout case has no descendant holding stderr after the direct child exits.

Fix direction: extend the targeted tests and mutation table to exercise each missing branch, including positive evidence before filter failure and an inherited pipe held past the join limit. Use byte-oriented fixtures on Windows as in the final commit. Risk: timing tests can become flaky; use explicit child/parent synchronization and generous outer test deadlines rather than relying solely on short sleeps.

**R25-ROBUST-04 — P2 — `.claude/dev/launcher.py:1623` / `:1617` (LỖI, unbounded buffering introduced in the supervisor).** Both normal filtering and error draining call `readline()` without a size limit. A long unterminated line must be fully buffered in the launcher before classification; ANSI cleanup, decoding and JSON parsing can allocate further copies. This changes stderr from a direct file sink to unbounded supervisor memory consumption. The benign byte probe confirms `readline_sizes: [-1, -1]` and accepts a 1 MiB line; resource exhaustion itself was deliberately not attempted. A much larger line can exhaust the launcher before it completes deadline enforcement or writes its receipt.

Fix direction: bound the streaming buffer and frame size, drop an oversize record through its delimiter without persisting its tail, and record measurement failure without stopping pipe drainage. Apply the bound in the exception-drain path too. Test a finite harmless oversize record and an unterminated record with a small test limit, with a mutant removing that bound. Risk: truncating a record must never reclassify its remaining bytes as safe stderr, and ordinary diagnostic preservation needs a defined policy.

## Security case matrix and evidence limits

`LỖI` below distinguishes a code-level failure from a live exploit reproduction. No new exploit payload, credential-bearing attack line, forged server event, or exhaustion attack was authored. The supplied synthetic secret fixture and supplied mutants were reused. New probes contain only benign data or code guard removals. `KHÔNG PHẢI LỖI` applies only to the stated measured/supported case; `KHÔNG ĐO ĐƯỢC` is not a pass.

Commands/evidence keys (all source-read commands rc=0):

- **S1:** `nl -ba src/.claude/dev/launcher.py | sed -n '1596,1644p'`, retained in `review-scratch.Dggq2S/filter-source.txt`. Actual relevant output: `_RE_ANSI_B = re.compile(rb"\x1b\[[0-9;]*m")`; `_RE_DAU_LOG = re.compile(rb"^\d{4}-\d\d-\d\dT\S*\s+(TRACE|DEBUG|INFO|WARN|ERROR)\b")`; `bo = False`; `for dong in iter(ong.readline, b""):`; `bo = dau.group(1) in (b"TRACE", b"DEBUG")`; `f_err.write(dong)`.
- **S2:** `nl -ba src/.claude/dev/launcher.py | sed -n '1766,1789p'`, retained in `spawn-source.txt`. Actual relevant output: `stdout=f_out, stderr=subprocess.PIPE if do_model else f_err`; inherited `RUST_LOG` concatenated with `_RUST_LOG_DO_MODEL`.
- **S3:** `nl -ba src/.claude/dev/launcher.py | sed -n '1852,1867p'`, retained in `finish-source.txt`. Actual relevant output: `luong_loc.join(timeout=10)`; `"DO_DUOC" if model_ket and not loi_loc else "KHONG_DO_DUOC"`.
- **B:** `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.Dggq2S/benign_byte_checks.py`, rc=0, output in `benign-byte-checks.log`: EOF fixture `input_bytes=200, output_bytes=0, models=1, errors=[]`; ordinary non-UTF-8 `input_bytes=2, output_bytes=2, byte_preserved=true`; harmless 1 MiB line `input_bytes=1048576, output_bytes=1048576`; both reads request `-1`; `standalone_standard_SGR_removed: True`.
- **T1–T5:** the five exact `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1` commands are recorded in the test table below and in `commands.jsonl`. Each final baseline output is `1/1 qua, 0 bo qua, 0 hong`, rc=0.

| Case / destination | Classification | Command and actual evidence; interpretation |
|---|---|---|
| Recognized timestamped TRACE and DEBUG, ordinary multiline continuation | **KHÔNG PHẢI LỖI** for supplied fixture | T1 rc=0, 1/1. It verifies exact retained stderr bytes, three ordered response entries, and absence of the synthetic secret from every file in the run directory. |
| Multiline continuation that looks like a new INFO/WARN/ERROR record, or continuation after an interleaved ordinary record | **LỖI** (R25-SEC-01) | S1 prints the unconditional level-based reset and subsequent `f_err.write(dong)`. No attack payload executed; logical record boundaries are not tracked. |
| Standard numeric/semicolon ANSI SGR | **KHÔNG PHẢI LỖI** for that syntax | B rc=0: `standalone_standard_SGR_removed: True`. The existing tests do not cover colored records: the ANSI-removal mutant passes 5/5. |
| Other leading ANSI/control formats | **LỖI** when they hide the prefix while suppression is off (R25-SEC-01); emission by this CLI is **KHÔNG ĐO ĐƯỢC** | S1 shows only `ESC [ digits/semicolons m` is stripped. No generalized escape decoder or fail-closed unknown-record branch exists. No new control-sequence attack was constructed. |
| Trace/debug without a recognized timestamp | **LỖI** when suppression is off (R25-SEC-01) | S1: anchored timestamp regex, initial `bo = False`, fall-through write. Conversely an unmarked line immediately after recognized TRACE remains suppressed. Live timestamp-free Codex emission was not claimed. |
| Partial final line / EOF | **KHÔNG PHẢI LỖI** for a complete recognized event missing only newline; incomplete prefix remains R25-SEC-01 | B rc=0: 200 bytes in, zero persisted, one model extracted, no errors. `readline()` returns a final nonempty fragment at EOF. A truncated/malformed JSON body is ignored rather than taken from `-m`. |
| Very long / unterminated line | **LỖI**: no memory bound (R25-ROBUST-04) | B rc=0 processes 1,048,576 bytes, and logs unlimited reads `[-1, -1]`; S1 confirms identical unbounded drain. Actual OOM threshold **KHÔNG ĐO ĐƯỢC**, not stress-tested. |
| Non-UTF-8 bytes | **KHÔNG PHẢI LỖI** for byte preservation/classification; exact malformed-frame evidence **KHÔNG ĐO ĐƯỢC** | B rc=0: two ordinary bytes preserved exactly. S1 operates on bytes, but event decoding uses `decode("utf-8", "replace")`, so malformed model/ID bytes could be silently altered instead of rejected; strict decoding is recommended under R25-MEAS-02. No malformed-event payload generated. |
| Pre-existing `RUST_LOG` enabling another target | **LỖI** relative to the narrowest-target contract (R25-SEC-01) | `observations.py fixtures` rc=0 prints `codex_core=debug,tungstenite::protocol=trace`. Other targets remain enabled; recognized DEBUG still gets dropped, but the exposure/format surface is not constrained. |
| INFO/WARN/ERROR carrying headers or credential text | **LỖI** for such an input (R25-SEC-01); actual occurrence **KHÔNG ĐO ĐƯỢC** | S1 resets suppression to false for each such level and writes the complete original bytes. T1 intentionally confirms normal INFO/WARN preservation; no credential-bearing high-level payload was added. |
| `stdout.log` | **KHÔNG ĐO ĐƯỢC** as a universal no-trace/no-credential guarantee | S2 shows direct, unfiltered stdout. T1 proves only its supplied fake child does not leak the sample there. Official non-interactive Codex behavior puts progress on stderr and the final answer/JSON event stream on stdout; other modes/echoed content were not exercised. [Official non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode) |
| `run.json` | **KHÔNG PHẢI LỖI** for excluding raw fixture lines; provenance remains **LỖI** | T1 rc=0, recursive scan passes; S1 appends only `response_id`, `model`, `su_kien`. Exception text is not serialized, only its class name. Those fields lack source-envelope validation (R25-MEAS-02). |
| Filter-created temp files / run-directory files | **KHÔNG PHẢI LỖI** for supplied fixture and this filter's direct writes | T1 rc=0 scans all run-directory files; S1 contains no temp/spool writer, and suppression precedes `f_err.write`. This is not proof about Codex's own files outside that directory. |
| Codex-owned logs in `CODEX_HOME`, `log_dir`, SQLite or other sinks | **KHÔNG ĐO ĐƯỢC** for the required absolute no-disk guarantee | Official docs confirm local diagnostic stores and opt-in `codex-tui.log`; they distinguish `codex exec` from TUI logging. Launcher only intercepts stderr and does not restrict subcommands or file-log settings. Credential-free `observations.py codex-log-init` attempted `codex -c log_dir=...` with non-TTY stdin: Codex rc=1, `Error: stdin is not a terminal`, `isolated home artifacts: []`. This fails before exercising TUI logging and is not a safe-log result. An earlier `TERM=dumb` attempt also stopped before logging; only CLI alias artifacts were observed. No authenticated/live run or existing personal log store was opened. [Official diagnostic behavior](https://learn.chatgpt.com/docs/config-file/environment-variables), [log directory setting](https://learn.chatgpt.com/docs/config-file/config-reference) |

## Measurement correctness and regression checks

The selected nested field is `event.response.model`, never the CLI `-m` or client turn configuration. The documented server events include `response.created` and `response.completed` with a response object, so the chosen field is appropriate **if** the record is proven to be that server receive event. It establishes the model reported by the server, not an independent attestation of hidden routing/backend identity. Actual authenticated server provenance was not measured here, and the missing log-envelope check is R25-MEAS-02. [Official response streaming schema](https://developers.openai.com/api/reference/resources/responses/streaming-events)

- Dedupe implementation matches `(response_id, model)` and preserves first-arrival order/event name. T1 checks duplicate created/completed for one pair, multiple IDs sharing a model, and two models. Same ID with different models is correct by source inspection but not covered by the supplied fixtures (ID-only mutant survives).
- T2 proves no-event runs are `KHONG_DO_DUOC`, with an empty list and reason despite `-m gpt-mau`. S3 sets `DO_DUOC` only with at least one parsed record and no recorded filter error. A still-open pipe can produce `DO_DUOC` for the observed subset with an explicit incompleteness note; it does not prove every response was observed.
- T5 proves a reader exception records `RuntimeError`, drains the remaining input, and does not write unfiltered remaining lines. Final ledger status after positive evidence followed by a crash is correct by S3 inspection but not tested end-to-end; its guard-removal mutant survives.
- T4 passes with launcher child rc=124 and retains the frame received before termination. Full-suite journal reports passes for `t27`, `t28`, `t63`, `t66`, `t67`, `t158`–`t161` (deadline, descendant kill, setsid and malformed process-name cases). Exit selection `124 if ket_giet.tron_ven else 125`, and the pre-existing missing-identity override, are unchanged. A **Codex-specific 125 scenario was not separately reproduced**. Native Windows 125 test `t62` is skipped on Linux.
- Reader held by a benign sleeping descendant: launcher rc=0 after 10.37 seconds, one observed model, and the explicit open-pipe/incomplete-list note. No indefinite EOF wait in this scenario. Removing the bound is not caught by the five new tests.
- Non-Codex T3 passes: no model keys, trace-looking ordinary stderr remains present. The child environment and file-output path remain unchanged for non-Codex runs.
- `stderr_byte` / `stderr_sha256` still describe the **persisted file**, now the filtered stderr for Codex; they do not describe original raw child stderr volume. The fixture observation measured 98 stored bytes, ledger count 98 and matching hash. Existing `r14_run_json_bam_lai_dung_hai_log` passes for both raw non-Codex logs.
- Windows: `CREATE_NEW_PROCESS_GROUP`, Job Object setup/kill and `codex.cmd` name detection remain in source. Full-suite tests `t79`, `t81`, `t83` pass their simulated/helper paths on Linux. They do not establish native Windows execution. The new Windows fake child is a renamed Python `.exe`, not a `.cmd` wrapper. **Native `creationflags`, Job Object lifecycle, `codex.cmd`, and PR #909's exact-SHA Windows CI are KHÔNG ĐO ĐƯỢC here**; no Windows host or authenticated CI readback was used. The CRLF fixture fix writes raw bytes as intended by source inspection.

## Executed tests and mutants

All test subprocesses use an explicit environment allowlist with no inherited real credentials. Existing tests may use their own inert synthetic authentication fixtures and create disposable Git fixture commits; the reviewed repository was never committed or modified. `PYTHONDONTWRITEBYTECODE=1` prevents test bytecode writes into it. Scripts, full outputs, and exact invocations are in `review-scratch.Dggq2S/commands.jsonl`.

For each baseline below, command is `python3 src/.claude/dev/launcher_test.py --lap-ca NAME --lan 1` (the recorded executable is `/usr/bin/python3`, with absolute source paths):

| ID | NAME | rc / actual result |
|---|---|---|
| T1 | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0; 1/1, 0 skipped, 0 failed |
| T2 | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0; 1/1, 0 skipped, 0 failed |
| T3 | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0; 1/1, 0 skipped, 0 failed |
| T4 | `r925_codex_qua_han_van_124_va_giu_khung_da_den` | 0; 1/1, 0 skipped, 0 failed |
| T5 | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0; 1/1, 0 skipped, 0 failed |

Supplied mutations: `python3 review-scratch.Dggq2S/run_review_tests.py r25`, final driver rc=0, output `BASELINE 5/5; MUTANTS KILLED 8/8`. Every replacement anchor occurs exactly once. Each temp copy is compiled by executing its copied unchanged test harness with the corresponding `--lap-ca NAME --lan 1`. Each mutant returns rc=1 with `0/1 qua, 0 bo qua, 1 hong`:

| Mutant | Target | Actual failing assertion (output excerpt) |
|---|---|---|
| `r25_ghi_ca_dong_trace` | T1 | `stderr.log khong dung cac dong khong phai trace` (trace lines present) |
| `r25_giu_dong_noi_tiep` | T1 | `stderr.log khong dung cac dong khong phai trace` (continuation present) |
| `r25_gop_theo_model` | T1 | `model_phuc_vu sai` (third response omitted) |
| `r25_khong_bat_trace` | T1 | `con khong duoc bat trace` |
| `r25_DO_DUOC_vo_dieu_kien` | T2 | `khong co khung ma van ghi model` |
| `r25_bo_loc_hong_khong_xa_ong` | T5 | `ong chua duoc xa het: con co the treo vi ong day` |
| `r25_bo_loc_hong_khong_ghi_loi` | T5 | `loi bo loc khong duoc ghi: []` |
| `r25_loc_ca_luot_khong_phai_codex` | T3 | `luot khong phai codex co khoa model` |

The first two stop on exact stderr comparison before the later recursive secret scan; they still kill the intended leak, but do not independently prove every scan destination. The trace-enable mutant measures environment injection, not an actual server event. The unconditional-status mutant does not implement a real `-m` fallback, although T2's assertions would reject such a nonempty fallback.

Additional mutation command: `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.Dggq2S/check_missing_guards.py`, rc=0. Actual output: `ADDITIONAL MUTANTS SURVIVED: 5/5`; all 25 underlying test commands rc=0, 1/1 each. The script contains the exact old/new anchors, and only temp `launcher.py` copies change. This is a **test-adequacy failure**, not a successful security result. Remaining guards without a supplied dedicated mutant include valid/empty field validation, receive-marker/source positioning, arrival order/duplicate suppression as such, incomplete-reader note, and the byte/hash behavior on the Codex filtered path.

Full-suite command: `python3 src/.claude/dev/launcher_test.py --nhat-ky <scratch>/full-suite-journal.log`, recorded child **rc=1**, elapsed 250.212 s. Actual final output:

```text
241/254 ca DA CHAY QUA (tong 264, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi
```

Of the 10 skips, 2 require native Windows behavior and 8 report unavailable venv/pip. Two failures attempt to use read-only `/var/tmp`; the other 11 encounter or depend on the sandbox's protected ancestor `/tmp/.git` and credential-store rejection. `CLAUDE.md:919` already documents the latter environment issue. No protected sandbox directories were removed or bypassed.

Base comparison: `PYTHONDONTWRITEBYTECODE=1 python3 review-scratch.Dggq2S/compare_base_failures.py`, driver rc=0. It exports the base's unchanged `.claude` tree to scratch and reruns exactly the 13 failed cases with `--lap-ca NAME --lan 1`. Actual output: `BASE FAILURES: 13/13; skips: 0`; each case rc=1, 0/1. These failures therefore do not establish a regression in this delta. They also do **not** satisfy the required green full Linux suite. Exact names, reasons, commands and outputs are retained in `base-comparison-output.log`, `base-failure-cases.json`, and `commands.jsonl`.

Acceptance evidence still unavailable: green native Windows on this exact SHA, a green full Linux run in a suitable environment, and an authorized real Codex run proving server-response measurement and absence of raw trace in every relevant sink. Per the user's no-credentials constraint, no live authenticated run was attempted.

## Final integrity check and disposition

Completed UTC: `2026-10-24T10:04:35.540674+00:00`. Measured environment: `Linux x86_64`, Python `3.13.16`.

Final `git -C src rev-parse HEAD HEAD^{tree}` rc=0 returns the original full SHA and tree above. `git -C src status --porcelain=v1 --untracked-files=all` rc=0, empty. `git -C src diff --check e739ac1b74024a20949425c447fb6cf025317c0e 83d305fbf63d5978189a9796141e3d547a46b2c6` rc=0, empty. Companion-file integrity: **26/26** copied test/policy files byte-identical to source; **13/13** supplied/additional mutant launcher modules compile. Only verdict/scratch artifacts were written; no source edit, real credential use, repository commit, push, or GitHub comment.

Open findings: **0 P0, 1 P1, 3 P2**. The 5/5 targeted passes and 8/8 supplied mutant kills do not close the source-level security/provenance defects or the additional guard-coverage gaps. Native/live evidence limitations remain explicitly unmeasured.

VERDICT: changes_requested
