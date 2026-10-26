# WP748 r25/g25 — PR #909 round 2 independent review

Reviewer: OpenAI Codex, as identified by the session runtime instructions. Exact serving model/build and launcher execution-receipt attestation are not independently verified. No credentials used.

Started UTC: 2026-10-24T10:18:15.628941+00:00

Review class: sensitive.
Reviewed SHA: `aaad9ab95ab170df4083e0c8203a88b5bd3b35a9`.
Reviewed tree: `32b6a4394edcee06c3674904b512469f2030c17b`.
Lease base: `1c20f3bd6a7ed08114feaf1d91c0790360b8f581`.
Review delta base: `e739ac1b74024a20949425c447fb6cf025317c0e`.

## Identity / initial evidence

- `git -C src rev-parse HEAD HEAD^{tree}`: rc 0; SHA and tree exactly match.
- `git -C src symbolic-ref -q HEAD`: rc 1; no output, confirming detached HEAD.
- `git -C src status --short`: rc 0; empty.
- `git -C src diff --name-only e739ac1b74024a20949425c447fb6cf025317c0e aaad9ab95ab170df4083e0c8203a88b5bd3b35a9`: rc 0; exactly `.claude/dev/launcher.py` and `.claude/dev/launcher_test.py`.

## Review progress

Identity verified; review and measurements in progress.

Spec lookup: master path absent (rc 128); fallback local ref read rc 0 and SHA-256 `5f85d350bc78a28693b1cb095bfa2fa62353975c3ba0e714a2a59c6e8e4dafa3` matches. Authority is the spec’s cited #748 issuecomment-6378484722; no GitHub/credential access. Master merge-base verified (rc 0); lease base ancestor check rc 0.

Delta: 113+ / 3− launcher, 262+ / 0− tests; total 2 files, 375 additions, 3 deletions, within the user-specified ADR-0053 ceiling 6/450.

Scratch: `review-scratch.wost2on2`. Tests use a minimal subprocess environment, no inherited authentication variables, bytecode writes disabled, and a verified nonexistent CODEX_HOME outside `/tmp` (avoids sandbox `/tmp/.git` rejecting that selector). Fixtures create disposable repositories and inert credentials; no real credentials used.

## Incremental measurements

Every `r925_*` case executed via `python3 src/.claude/dev/launcher_test.py --lap-ca <full-name> --lan 1`: **11/11 passed**, all rc 0, each `1/1 qua, 0 bo qua, 0 hong`. Exact commands/output/timings: scratch `commands.jsonl`. Timeout case passes (asserted child rc 124); inherited-pipe case passes in 10.366 s and asserts `KHONG_DO_DUOC`. Supplied and supplementary mutation measurements are running.

Supplied `r25_*` mutants: **19/19 killed**, **21/21 designated case executions raised `TinHieuChotCa`**, 0 setup errors/skips. Mutation driver rc 0; each kill is recorded as case rc 1. Only temporary launcher copies changed; companion source copied unchanged.

Additional guard removals: **3/3 survive**, **33/33 r925 executions pass**, 0 setup errors/skips. (1) Remove `if dau_dong and tron` from frame parsing; (2) replace bounded exception drain `ong.read(_TRAN_DONG)` with unbounded `ong.read()`; (3) pass `[]` instead of `loi_loc` to the final `_ket_luan_model`. These retain an open R25-TEST-03 coverage gap despite the supplied 19/19 kills.

Benign observations rc 0 (`observations.log`): CRLF frame accepted and fully suppressed; CR-only/no-LF frame suppressed and not accepted; oversized first line suppressed; exception drain reads `[4194304, 4194304]`, reaches EOF, records RuntimeError; persisted stderr is 39 bytes and ledger size/hash match. One valid frame followed by an existing oversized second frame (test cap 201 bytes) yields one model, no errors, **DO_DUOC**, despite missing the second response. Source records discard counts but not evidence incompleteness.

Full Linux suite command: `python3 src/.claude/dev/launcher_test.py --nhat-ky <scratch>/full-suite-journal.jsonl`; **rc 1**, **255/268 executed passed**, total 270, **13 failed**, **2 skipped**; 215.586 s. Journal has 270 entries / 270 exits and `XONG TRON VEN`. Not a green full-suite result. Sandbox `/tmp/.git` exists; baseline isolation is in progress. Native Windows and an authenticated Codex run remain unmeasured; no credentials will be used.

Deterministic scheduling probe `race_observation.py` rc 0: real fake-child frame consumed at EOF between `list(model_ket)` and the final `is_alive()` check yields launcher rc 0, `model_phuc_vu=[]`, `model_phuc_vu_trang_thai=DO_DUOC`, no reason, 201 bytes dropped. The thread scheduler is controlled, not a claim of reproducing the race probabilistically. Parser and final ledger code are unchanged.

## Final assessment — ĐỐI CHIẾU LƯỢT TRƯỚC

Identity refinement: runtime instructions identify **OpenAI Codex, based on GPT-6**; provider `openai_codex`; observed transport is machine/tool-mediated local subprocess execution on Linux x86_64, Python 3.13.16. The user reports `launcher.py run` / Codex CLI invocation. Exact serving model, effort, enclosing session/run ID, and server-response execution receipt were not exposed or independently verified. `launcher.out` in this directory was empty when inspected. This verdict does not turn the user's invocation statement into machine-attested model evidence. No GitHub submitter or publication is involved.

| Round-1 finding | Round-2 status | Independently measured basis |
|---|---|---|
| **R25-SEC-01, P1** — fail-open trace classification | **VÁ HỜ / partially fixed; remains open** | The fixture secret scan, four lock variants, and inherited-RUST_LOG replacement pass. Permanent locking fixes the old INFO/WARN unlock path. Before locking, however, arbitrary complete LF lines still fall through to the disk writer unless two negative recognizers match. The benign byte probe saves unknown non-UTF-8 bytes unchanged. This is not an allow-list of approved safe diagnostics; see the precise residual scope below. No new credential-bearing payload was authored. |
| **R25-MEAS-02, P2** — other target / embedded receive marker accepted | **ĐÃ VÁ THẬT for the original envelope/position defect** | The targeted provenance case passes (rc 0, 1/1), rejecting the supplied other-target and embedded-marker examples; target/position, event-type, ANSI and ID+model mutants all die by `TinHieuChotCa`. `_RE_KHUNG` now anchors the receive envelope. This closes that defect, not every possible source of false or incomplete measurement; R25-EVID-05 and R25-RACE-06 below are separate mechanisms. Strict UTF-8/schema hardening remains a source-observed limitation. |
| **R25-TEST-03, P2** — missing effective guard mutants | **VÁ HỜ / partially fixed; remains open** | The five originally reported gaps now have targeted coverage, and supplied mutants are 19/19 killed. Nevertheless three independently removed guards survive all 11 cases (33/33 passing executions): complete-line parsing gate, bounded error drain, and propagation of actual reader errors into final ledger status. The last gap retains the round-1 concern that helper-only status testing does not prove the end-to-end error path. |
| **R25-ROBUST-04, P2** — unbounded normal/error reads | **ĐÃ VÁ THẬT for buffering; VÁ SINH LỖI MỚI in evidence accounting** | Bounded-read case rc 0, 1/1; removing the normal bound kills its intended test. A benign exception probe records bounded drain sizes `[4194304, 4194304]` and EOF. Oversized/unterminated first records never reach the output file. The memory-bound defect is closed. Dropping an oversized response without marking the measurement incomplete introduces R25-EVID-05; the exception-drain bound still lacks an effective test mutant. |

### Open findings and fix directions

**R25-SEC-01 — P1 — `.claude/dev/launcher.py:1629`, `:1634`, `:1652` — class `pre-lock-fail-open`.**

`khoa=False` initially. Every complete LF-terminated input line that lacks the particular level/target pattern and the ASCII substring `tungstenite` is written verbatim. There is no positive safe-line predicate, validated preamble, or enforced source-format/version boundary. The permanent lock is effective **after a recognized marker**, including across later INFO/WARN records. It does not establish that all earlier lines are safe. An unrecognized first log/continuation or credential-bearing preamble before that marker still takes the file-write branch. Arbitrary prefixes by themselves no longer bypass a marker that remains intact; the residual requires the marker itself to be absent/unrecognized. This distinction avoids incorrectly reopening the already-fixed prefix case.

Measured evidence: `observations.py`, rc 0, preserves the existing 39-byte preamble and also preserves an otherwise unrecognized two-byte non-UTF-8 line byte-for-byte. Source inspection establishes the same unconditional branch for any such line. **This is a source-proven fail-open policy, not a reproduced secret leak from codex-cli 0.163.0.** The supplied secret fixture passes; whether that exact CLI emits an unmarked credential-bearing first record was not measured. Calling the policy an allow-list does not supply that missing invariant.

Fix direction: positively constrain what can be persisted before enabling trace, and make unknown framing fail closed. Preserve diagnostics through an explicitly safe channel/preamble policy; if that cannot satisfy the diagnostic-retention contract, obtain a revised contract. The executor should author first-record/format-ambiguity fixtures and their mutants. Also establish the no-disk guarantee for child-owned log sinks; a stderr interceptor alone cannot prove it for arbitrary Codex modes/configuration.

**R25-TEST-03 — P2 — `.claude/dev/launcher_test.py:6514`, `:6536`, `:6609`, `:10317` — class `unguarded-filter-invariants`.**

The supplied oversized-line mutant named `r25_parse_dong_vuot_tran` removes the *lock trigger*, not the independent `if dau_dong and tron` condition on frame parsing. Its test does not place a complete-looking frame in an unterminated EOF fragment or continuation chunk. The crash fixture checks that draining occurs but never checks drain read sizes. The status helper test injects an error list directly, so it still passes if production stops forwarding `loi_loc`.

Measured: `mutations.py extra`, rc 0, **3/3 mutants survive; 33/33 targeted executions pass**, no skips or setup errors. Exact unique source replacements are retained in that script and in the temporary mutated modules. They remove only the three guards described above. This violates the spec's requirement that every new guard have its own effective mutant.

Fix direction: add separate fixture/assertion/mutant pairs for EOF and chunk-boundary frame completeness, sized reads in the exception path, and an actual collected frame followed by a reader failure through final ledger generation. Include the two final-status scenarios below. Keep fixture payload authoring with the executor.

**R25-EVID-05 — P2 — `.claude/dev/launcher.py:1632`, `:1639`, `:1643`, `:1657` — class `discarded-evidence-reported-complete`. NEW.**

When a record exceeds the read cap, ends without LF, or matches the receive envelope but cannot be decoded/parsed, the parser skips it without setting `loi`. A prior accepted frame plus EOF is therefore sufficient for `DO_DUOC`, even when another response was knowingly discarded. The spec requires the per-response list to retain all observed models, and the new completeness claim cannot be derived from EOF alone.

Measured: `observations.py`, rc 0, reuses the supplied valid frame and the existing oversized-ID fixture, with the test cap set to 201 bytes. Input 466 bytes contains two complete response lines. Output: only `resp_q/gpt-6-astra`, `errors=[]`, three dropped read chunks, **`DO_DUOC` with no reason**. A valid frame followed by its existing unterminated form likewise reports `DO_DUOC`. No new attack content was created. The small bound exercises the same production branch as the 4 MiB cap.

Fix direction: track incomplete/unparseable candidate evidence separately from intentional raw-trace suppression and require no such loss for `DO_DUOC`. Preserve the observed subset with `KHONG_DO_DUOC` and a reason. Normal trace dropping must not itself make every run fail. Strict UTF-8 and meaningful identifier validation belong at this boundary: currently `decode('utf-8', 'replace')` silently changes bytes, an empty ID is allowed, and whitespace-only model strings are truthy. These latter schema directions were inspected, not exercised with newly authored malformed frames.

**R25-RACE-06 — P2 — `.claude/dev/launcher.py:1885`, `:1888`, `:1889` — class `non-atomic-reader-snapshot`. NEW.**

After the timed join, production first copies `model_ket` into the receipt and then samples reader liveness while evaluating status against the **live original list**. A reader finishing in between those operations can add the first/last frame after the receipt copy and return EOF before `is_alive()`. The status then certifies a different list from the one recorded; the receipt can even say `DO_DUOC` with `model_phuc_vu=[]`.

Measured: `race_observation.py`, rc 0, uses an unchanged parser and `lenh_run` with a deterministic scheduling seam. The reader consumes the existing child's real frame/EOF at the final liveness sample. Actual receipt: launcher rc 0, **empty model list, `DO_DUOC`, no reason, 201 bytes dropped**. This demonstrates the interleaving; it does not claim a probabilistic stress reproduction or actual ten-second wait in this controlled probe.

Fix direction: latch the timed-join outcome before taking the final snapshot. If the reader was still active, the receipt must remain incomplete even if it finishes during serialization. Otherwise snapshot only after its completion. Derive status and serialized fields from the same stable snapshot, including error state and counters.

**R25-CONTRACT-07 — P2 — `.claude/dev/launcher.py:1636`, `:1650`; `.claude/dev/launcher_test.py:6468` — class `diagnostics-retention-contract`. NEW.**

**Judgment: a contract violation under the supplied frozen spec, not an automatically acceptable tightening.** Contract §2 explicitly promises that non-trace stderr is retained as before. The new implementation and test instead require discarding every subsequent line, including ordinary error diagnostics; it also drops an ordinary final fragment without LF even before any log marker. This is an observable logging regression. The design is conservative about disclosure after locking, but that does not satisfy the separate retention promise.

Measured: `observations.py`, rc 0, feeds a valid supplied trace frame, the existing INFO fixture, then the existing ordinary 39-byte preamble. All **308 bytes** are dropped, including both non-trace lines. An ordinary CR-only EOF diagnostic is also dropped. The new main fixture explicitly enforces preservation of only the prefix.

Fix direction: use a record/source boundary that supports retaining safe diagnostics, or revise the frozen spec with explicit owner acceptance of this diagnostic loss and revised acceptance tests. Do not restore the old unconditional INFO/WARN unlock, which would reopen the demonstrated security defect.

### Security and completeness matrix

| Path | Result and limit |
|---|---|
| First recognizable trace / later INFO, WARN, continuations | Existing secret fixture and four variants pass; suppression never reopens. The fixture scans every file under the run directory. No real credential scan performed. |
| Before first recognized marker | Arbitrary complete lines still persist; R25-SEC-01. No new credential-bearing attack line generated. |
| Lock recognition / ANSI | Searches every position, strips the broader CSI pattern, and independently searches `tungstenite`. Supplied ANSI fixture passes and ANSI mutant dies. This is not a general terminal-escape decoder; absent/broken-marker formats are a direction for executor-authored testing. |
| Partial final line / no LF | Entire fragment suppressed and never parsed as a frame. With no other frame: `KHONG_DO_DUOC`. With an earlier frame: completeness can be overstated (R25-EVID-05). |
| CRLF | Existing frame converted only to CRLF: 202 input bytes, zero stored, one model, `DO_DUOC`; the ordinary-byte write branch performs no text translation. Native Windows still unmeasured. |
| CR-only / `\r` without `\n` | Neither is a delimiter for binary `readline`. The unterminated chunk locks and is dropped; no frame accepted. Interior CR with a later LF remains within one chunk; searches run over the entire chunk, while the receive regex stays start-anchored. Potential observation loss, no measured raw tail leak. |
| Oversized first line / tail | Benign 200-byte first line with cap 64: zero persisted bytes, including all tail/subsequent text. Reads are bounded; parsing rejects continuation chunks. Discard counter `stderr_bo_dong` counts read chunks here (5 for 2 physical lines), so it is not universally a physical-line count. |
| Encoding | Ordinary non-UTF-8 bytes are preserved before lock; ASCII marker classification is byte-based. Frame decoding uses replacement, not strict UTF-8. Malformed-frame acceptance directions were not executed as new attack content. |
| Exception / error drain | Supplied fixture and direct probe record only exception class, do not persist the remaining input, use bounded `read(4194304)`, reach EOF and return `KHONG_DO_DUOC`. A drain error is suppressed, but the earlier recorded filter error still prevents success. |
| Writes after `f_err.close()` | Actual closed `BytesIO` rejects writes; `ValueError` is swallowed and no raw fallback exists. A reader can still collect frames after close, which matters for R25-RACE-06. The closed-output probe produces a frame with no recorded write error, not a disk leak. |
| `run.json` | Supplied secret absent; only selected event fields retained. Fields are not schema-bounded beyond basic types/truthiness; malformed-field hardening remains unmeasured. Race can make list and status disagree. |
| `stdout.log` | Direct/unfiltered sink. Supplied fake-child run is clean. No universal assertion about echoed trace/credentials or arbitrary child behavior. |
| Codex-owned files / external sinks | Not intercepted or restricted by this delta. No authenticated run, TUI logging exercise, personal log-store inspection, or live secret scan. Executor's reported real-run numbers are unverified evidence, not reviewer measurements. |
| Success without any frame / reader error / pipe still open | Helper truth table and corresponding supplied mutants pass/kill. Actual propagation remains under-tested (R25-TEST-03); incomplete discard and snapshot race remain open. |

### Regression evidence and limits

- **Timeout / kill:** the Codex timeout fixture asserts rc **124** and preserves the frame seen before termination. Full-suite cases `t27`, `t28`, `t63`, `t66`, `t67`, `t158`–`t161` pass. The 124/125 selector and missing-identity override are unchanged versus the base. A separate controlled 125-branch measurement is recorded below; it is not a native Windows kill test.
- **Windows:** source retains `CREATE_NEW_PROCESS_GROUP`, Job Object creation/attachment, the original kill algorithm, and `.cmd` classification. Windows process-control mocked tests `t79`, `t80`, `t81` pass in the full Linux suite. `codex`, `.exe`, `.cmd`, uppercase `.CMD` classify true and Python false in the direct probe. No native `.cmd` spawn, Windows handle inheritance, creationflags, or native Job Object end-to-end run was measured. The two suite skips are `t62` and native SID conversion. The newly added grandchild test also explicitly skips Windows when run there. No Windows lane green claim is made.
- **Non-Codex:** targeted case rc 0, 1/1; original stderr bytes remain and no model/drop keys appear. The non-Codex `Popen` stderr/env path is unchanged. `r14` stored-byte/hash regression passes in the full suite.
- **`stderr_byte` / `stderr_sha256`:** still describe bytes actually persisted in `stderr.log`. Direct fixture: stored **39**, ledger **39**, SHA-256 equal, launcher rc 0. They do not describe original raw pipe volume. Drop counters are additional, and may represent only a snapshot when a pipe remains open.
- **Grandchild-held pipe:** actual subprocess case rc 0, 1/1, **10.366 s**, with `KHONG_DO_DUOC` and open-pipe reason. Removing the ten-second join kills the intended test. The final snapshot race remains distinct.
- **Full Linux acceptance:** **not green here**. All 270 cases entered/exited; 255 passed, 13 failed, 2 skipped. The **same 13 cases also fail with the base launcher selected** and unchanged harness/fixtures (corrected baseline driver, rc 0, each case rc 1). Two hit read-only `/var/tmp`; the others fail within the repository-ancestor fixture-home/materializer boundary. This is baseline/environment evidence, not a waiver or a claim of 268/268. Initial baseline attempt had two missing-hook setup errors; it is retained but superseded by the corrected run that preserves original fixture paths.
- **Bare Ruff lint:** ruff 0.15.15; `python3 -m ruff check --isolated --no-cache --select F <launcher> <launcher_test>` on head and base returns **rc 1 / 5 findings** each. The same five pre-existing findings occur; delta **0**. This is a measured lint delta, not an absolute pass or a workflow pin/probe certification.
- **Size:** 2 files, **375 added / 3 deleted** lines against the exact review base: below the user-requested 6-file/450-addition ceiling. ADR-0053 additionally documents a rollout OID declaration; the frozen spec does not contain that declaration. This review uses the user's explicit 450-line instruction and does not claim the declaration gate was satisfied.

### Reproducible command ledger

All test subprocesses use the minimal credential-free environment described above. Source bytecode writing is disabled. Commands, full stdout/stderr, real subprocess return codes and elapsed times are retained in `review-scratch.wost2on2/commands.jsonl`; individual logs and reviewer harness sources are beside it. Test-created Git seed commits occur only in disposable fixture repositories, never in `src/`.

Each row below ran the exact command `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`.

| Key | Case | rc | Positive output | Seconds |
|---|---|---:|---|---:|
| T1 | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | 1/1 qua; 0 skips; 0 failures | 0.365 |
| T2 | `r925_khoa_tu_dau_hieu_log_dau_tien_khong_mo_lai` | 0 | 1/1 qua; 0 skips; 0 failures | 0.248 |
| T3 | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | 1/1 qua; 0 skips; 0 failures | 0.211 |
| T4 | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0 | 1/1 qua; 0 skips; 0 failures | 0.364 |
| T5 | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | 1/1 qua; 0 skips; 0 failures | 0.267 |
| T6 | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0 | 1/1 qua; 0 skips; 0 failures | 0.392 |
| T7 | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0 | 1/1 qua; 0 skips; 0 failures | 0.413 |
| T8 | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0 | 1/1 qua; 0 skips; 0 failures | 0.354 |
| T9 | `r925_codex_qua_han_van_124_va_giu_khung_da_den` | 0 | 1/1 qua; 0 skips; 0 failures | 3.303 |
| T10 | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 0 | 1/1 qua; 0 skips; 0 failures | 10.366 |
| T11 | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0 | 1/1 qua; 0 skips; 0 failures | 0.234 |

Supplied mutation command: `python3 review-scratch.wost2on2/mutations.py supplied` (invoked by `run_review.run`, minimal environment), driver rc **0**. Every replacement uniquely matched once and compiled. Each listed target failed specifically with `TinHieuChotCa` (case rc **1**), not a setup exception.

| Mutant | Target(s) | Killed / intended |
|---|---|---:|
| `r25_ghi_ca_phan_bi_khoa` | T1 | 1/1 |
| `r25_khoa_mo_lai_theo_dong` | T2 | 1/1 |
| `r25_dau_hieu_chi_o_dau_dong` | T2 | 1/1 |
| `r25_bo_chot_ten_target` | T2 | 1/1 |
| `r25_bo_go_ansi` | T3 | 1/1 |
| `r25_khung_moi_target` | T3 | 1/1 |
| `r25_moi_su_kien` | T3 | 1/1 |
| `r25_gop_theo_id` | T3 | 1/1 |
| `r25_doc_khong_tran` | T4 | 1/1 |
| `r25_parse_dong_vuot_tran` | T4 | 1/1 |
| `r25_noi_rust_log_thua_ke` | T6 | 1/1 |
| `r25_khong_bat_trace` | T1 | 1/1 |
| `r25_DO_DUOC_khi_loc_hong` | T5 | 1/1 |
| `r25_DO_DUOC_khi_ong_con_mo` | T5, T10 | 2/2 |
| `r25_DO_DUOC_khong_khung` | T5, T7 | 2/2 |
| `r25_doc_ong_khong_han` | T10 | 1/1 |
| `r25_bo_loc_hong_khong_xa_ong` | T11 | 1/1 |
| `r25_bo_loc_hong_khong_ghi_loi` | T11 | 1/1 |
| `r25_loc_ca_luot_khong_phai_codex` | T8 | 1/1 |

Supplementary mutation command: `python3 review-scratch.wost2on2/mutations.py extra`, driver rc **0**. The three temporary modules each pass **11/11** existing r925 cases; **0/3 killed**. The runner rc only says the measurement completed; it does not mean the guards are covered.

Other measured commands (all full outputs retained):

| Command | rc | Result |
|---|---:|---|
| `python3 <scratch>/observations.py` | 0 | Bounded read, line endings, suppression, completeness and persisted hash observations; see matrix. |
| `python3 <scratch>/race_observation.py` | 0 | Receipt DO_DUOC with empty serialized model list under controlled interleaving. |
| `python3 <scratch>/timeout125_observation.py` | 0 | Launcher rc 125; ledger rc 125; giet_tron_ven=false; one model retained. Real kill followed by controlled incomplete-confirmation result; not a real surviving-descendant assertion. |
| `python3 <scratch>/baseline_failures.py` | 0 | 13/13 previously failing cases also fail with base launcher; individual rc 1. No whole-baseline-suite claim. |
| `python3 src/.claude/dev/launcher_test.py --nhat-ky <scratch>/full-suite-journal.jsonl` | 1 | 255/268 passed; 13 failures; 2 Windows-only skips; all 270 entered/exited. |
| `python3 -m ruff check --isolated --no-cache --select F src/.claude/dev/launcher.py src/.claude/dev/launcher_test.py` | 1 | Five findings. |
| `python3 -m ruff check --isolated --no-cache --select F <scratch>/base/launcher.py <scratch>/base/launcher_test.py` | 1 | Same five findings; zero delta. |

### Final integrity, evidence limits, disposition

Final `git -C src rev-parse HEAD HEAD^{tree}` rc **0** returns the requested SHA/tree unchanged. `git -C src diff --quiet`, `git -C src diff --cached --quiet`, and `git -C src diff --check e739ac1b74024a20949425c447fb6cf025317c0e HEAD` each return **0**. Final tracked/untracked porcelain status is empty. Both reviewed file bytes match HEAD exactly; **22/22** temporary mutant modules compile; **2/2** copied companions match source.

Ignored status contains `.claude/.packet_state/session-start.ran`, with mtime `2026-10-24T10:20:50.787184+00:00`. No initial ignored-file hash snapshot was taken, so this review does not claim a byte-for-byte before/after audit of every ignored artifact. No source edits, source commits, pushes, GitHub comments, real credential use, or authenticated Codex run were performed. The source was treated as read-only; scratch mutations, simulations and fixture repositories stayed outside it.

The cloud runtime skill was read; no environment-status tool was available in the active tool catalog. No network/credential setup was used. No new exploit payloads were authored: existing fixtures/mutants, harmless bytes, code guard removals and scheduling/error seams supplied the measurements. Unsupported attack-content directions are described in words only.

The five open classes/findings are R25-SEC-01 (P1), R25-TEST-03 (P2), R25-EVID-05 (P2), R25-RACE-06 (P2), and R25-CONTRACT-07 (P2). **0 P0, 1 P1, 4 P2.** Positive targeted/mutation results do not close these mechanisms. Full Linux acceptance, native Windows acceptance, and the executor’s live-run/no-secret claim are not independently green in this environment.

Completed UTC: `2026-10-24T10:30:21.014613+00:00`.

VERDICT: changes_requested
