# Independent review — WP748 r26/g26, spec r25 v2, PR #909 merged head, round 1

Disposition: changes requested. Open: **0 P0, 0 P1, 2 P2, 3 P3**. First recorded UTC clock: 2026-10-25T06:50:14Z.

Reviewer: OpenAI Codex. Runtime instructions identify this agent as Codex based on GPT-6; that declaration is not an independent serving-model attestation. Provider: `openai_codex`; execution surface: tool-mediated local shell in managed Linux; transport: machine. The user reports invocation via `launcher.py run`; its enclosing execution receipt and exact serving model are not independently visible/verified. Fresh reviewer context; no executor work. No GitHub submitter.

Identity checked FIRST: `git -C src rev-parse HEAD HEAD^{tree}` returned `b5b6aefa66a8ad037ff34430d0210f3b6873913f` and `6d47f211da364501e75ef4c622b577e619f2a7be`. `git -C src symbolic-ref -q HEAD` produced no output (detached; standalone rc 1 recorded below); `git -C src rev-parse --is-shallow-repository` returned `false`; initial `git -C src status --short` was empty. All requested identity values match.

Read-only scope: no edits to `src/`, commits, pushes, GitHub comments, credentials, authenticated Codex runs, or new exploit payloads. Scratch: `review-scratch.irmJLS/`. Existing fixtures and temporary launcher copies will supply measurements.

Spec lookup `git -C src show master:ops/specs/wp748-r25-launcher-model-phuc-vu-v2.md` returned rc 128 (path absent). Fallback `git show origin/ops/wp748-r25-g25-lease:ops/specs/wp748-r25-launcher-model-phuc-vu-v2.md` returned rc 0; SHA-256 verified below. Lease at the supplied remote ref read successfully, rc 0; r26/g26 explicitly requests initial review of this already-merged head. Authority #748 issuecomment-6394503720 cannot be read/verified on GitHub under this offline review. The user-provided instruction authorizes this review. No claim that live authority, live merge state, Windows CI, or prior live Codex evidence was independently verified.

Size measurement: `git -C src diff --numstat e739ac1b74024a20949425c447fb6cf025317c0e b5b6aefa66a8ad037ff34430d0210f3b6873913f` prints `136 3 .claude/dev/launcher.py` and `362 0 .claude/dev/launcher_test.py`: exactly 2 files, 498 additions, 3 deletions, within v2's 2-file/550-addition ceiling.

Cloud runtime skill read. No `environment_status` tool is available; no network/credential setup used. Repository reviewer instructions read; user instructions control the authorized offline review and zero-P0–P3 criterion.

## Incremental measured results

Spec SHA-256 verified: `f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb`. Standalone detached check rc 1; shallow check rc 0 / `false`; tracked, untracked and ignored initial status all empty. Local merge object `113e0d1beff2b037648681ee1fa59f678cef0eba` has the reviewed SHA as its second parent; `git merge-base --is-ancestor <reviewed SHA> master` rc 0. These are local Git facts, not a GitHub/live-state attestation.

All **15/15 `r925_*` cases pass** on the requested source path: each command `python3 src/.claude/dev/launcher_test.py --lap-ca <full case name> --lan 1` returns rc 0 and `1/1 qua, 0 bo qua, 0 hong`. The inherited-pipe case takes 10.450 s; the timeout case asserts rc 124. Exact commands/output/timings are in `review-scratch.irmJLS/commands.jsonl` and `targeted.log`. Environment uses no inherited authentication variables, disabled bytecode, a scratch HOME/TMPDIR and the verified absent `/nonexistent-wp748-r26-review-irmJLS` Codex home (avoids the sandbox's read-only `/tmp/.git` ancestor restriction).

`python3 review-scratch.irmJLS/observations.py` (minimal environment via `review.py exec observations ...`) returns rc 0. Existing fixture bytes expose a remaining **R25-EVID-05 / P2**: the same positive frame plus existing `b'x' * 256 + khung` continuation fixture is incomplete at every tested cap. At caps 256/330/360 the loss detector reports `mat=1`, `KHONG_DO_DUOC`; at caps **340/350** the candidate marker crosses a read boundary, `mat` is absent, and the result is **`DO_DUOC` with only the first response**. All 645 input bytes are suppressed; no raw-data leak. This reuses supplied harmless frames and changes only the test read cap; no new attack content.

The same probe measures two new contract defects: an allow-listed diagnostic followed by **two CR bytes and LF** persists all 41 bytes (`rstrip` removes every trailing CR/LF before comparison), and an existing error-drain scenario consumes/discards **279 bytes but leaves all drop counters empty**. Severity/fix details and final guard-coverage results follow below.

A disposable full clone at the exact head was used for the full Linux suite so hook tests cannot write into the reviewed `src/`. No mutation is applied to the reviewed checkout; supplied mutants live only in `review-scratch.irmJLS/mutants/`.

## Prior-finding disposition on b5b6aef under spec v2

| Earlier ID (source heads 83d305f / aaad9ab) | Status | Measurement / scope |
|---|---|---|
| R25-SEC-01 P1 — fail-open/pre-lock stderr | **Closed for the reported arbitrary-content write path.** | Main synthetic-secret run-directory scan and exact-allow-list case both rc 0 / 1/1. Arbitrary preamble bytes, non-UTF-8 bytes, prefix/suffix variants, and incomplete safe lines are suppressed. Supplied unrestricted/prefix/partial-line mutants all die. RUST_LOG replacement case rc 0 / 1/1, corresponding mutant dies. A narrower CR normalization defect is separately recorded as R26-ALLOW-08 P3; no arbitrary trace/credential disclosure demonstrated. Child-owned sinks remain unmeasured, not certified. |
| R25-MEAS-02 P2 — wrong target / embedded receive marker | **Closed for the original provenance defect.** | Provenance/event/ANSI/dedup case rc 0 / 1/1; corresponding supplied mutants die. `_RE_KHUNG` anchors timestamp, TRACE, exact target and receive-message position; strict UTF-8 and nonblank id/model checks now exist. This is format provenance, not cryptographic server attestation. |
| R25-TEST-03 P2 — ineffective/missing guard mutants | **Partially fixed; OPEN.** | Old completeness and bounded-error-drain gaps now have effective mutants. All 25 supplied mutants die (32/32 intended case executions, specifically `TinHieuChotCa`). Three additional independent guard removals survive all 15 cases, **45/45 rc 0**, detailed below. |
| R25-ROBUST-04 P2 — unlimited line/error-drain reads | **Closed for the original unbounded-read defect.** | Both bounded-read tests rc 0 / 1/1; `r25_doc_khong_tran` and `r25_xa_ong_khong_tran` each die by intended assertion. Both paths request `_TRAN_DONG`, 4 MiB in production. No exhaustion stress test; retained model-list growth is not claimed bounded. |
| R25-EVID-05 P2 — lost evidence still certified complete | **Partially fixed; OPEN.** | Full candidate tokens on oversized/EOF fragments now increment `mat` and downgrade status. The same existing continuation fixture at cap 340 or 350 splits the token and still yields `DO_DUOC`; see observations and finding below. |
| R25-RACE-06 P2 — receipt copy precedes liveness/status against live list | **Closed for the original mismatch race.** | Ordering case rc 0 / 1/1, reversed-order mutant killed. Liveness is latched before copying models/errors/counters; both status and serialized models use the copies. An active reader remains `KHONG_DO_DUOC`; actual inherited-pipe case passes in 10.450 s. The live-reader copies are not an atomic cross-field snapshot, but they cannot certify completeness because the latched flag is true. |
| R25-CONTRACT-07 P2 — loss of normal stderr violates v1 | **Closed under the explicitly superseding v2 contract.** | `observations.py`: 308 bytes in; only the 39-byte allowed diagnostic retained after a frame and INFO line; 269 dropped bytes, 2 dropped chunks. This is now required policy. No finding is carried forward merely for diagnostic loss accepted by v2. |

## Open findings and remediation directions

**R25-EVID-05 — P2 — `.claude/dev/launcher.py:1664` / `:1605` — class `discarded-evidence-reported-complete` (continued).**

Candidate detection runs independently on each bounded chunk and retains no matching state across chunks. A rejected response whose `"type": "response.created"` or `completed` token straddles the cap is invisible to both searches. One earlier valid frame plus EOF then suffices for `DO_DUOC`, violating v2's no-lost-candidate condition. Existing fixture bytes (one valid frame + the test's `b'x' * 256 + khung`) give **645 input/dropped bytes, 3 dropped chunks, one retained model, no errors, no `mat`, `DO_DUOC`** at cap 340/350. At cap 256/330/360 the same bytes correctly give `mat=1` and `KHONG_DO_DUOC`. This is a small-limit measurement of the production branch, not a claimed live 4 MiB response reproduction.

Fix in `_loc_tung_dong`'s loss classifier: carry bounded lexical state across chunks (including relevant ANSI/JSON-token handling), or mark ambiguous receive records incomplete conservatively. Do not reconstruct/store raw trace on disk or reintroduce unlimited buffering. Add an alignment sweep over the existing candidate fixture and a mutant removing cross-chunk state; include positive evidence before the lost candidate. Also have the executor test escaped JSON keys/values and genuinely truncated type tokens. Risk: indiscriminate matching can turn harmless trace into false loss, so include authentic sanitized normal frame variants as negative controls. No new malformed/forged payload was authored in this review.

**R25-TEST-03 — P2 — `.claude/dev/launcher_test.py:6583`, `:10390`; `.claude/dev/launcher.py:1636`, `:1916` — class `unguarded-filter-invariants` (continued).**

The new strict UTF-8 guard has no supplied mutant. Replacing only `k.group(1).decode("utf-8")` with replacement decoding survives **15/15** cases. The new real-thread test calls `_ghi_ket_qua_model` directly: it does not traverse `lenh_run`'s final handoff. Replacing only `loi_loc` with `[]` in that production call also survives **15/15**; passing `dict(dem_loc, mat=0)` there survives **15/15** while preserving the drop counters checked by the happy-path case. The replacements each match uniquely, compile, and are applied only to separate temporary launcher copies. Thus **3/3 additional mutants survive, 45/45 targeted executions pass**; supplied 25/25 kills do not satisfy v2's every-new-guard requirement.

Fix the targeted harness/table: add strict UTF-8 rejection/loss evidence and a real `lenh_run` integration seam that delivers a valid frame followed by a reader error or known candidate loss, then assert the final on-disk receipt. Give each independent guard its own mutant. Include the R25-EVID-05 alignment guard once implemented. Risk: a test-only helper path can again bypass the production handoff; ensure the test reads the actual final `run.json`, and distinguish intended `TinHieuChotCa` kills from setup exceptions.

**R26-ALLOW-08 — P3 — `.claude/dev/launcher.py:1653` — class `nonliteral-allowlist-comparison` (NEW).**

`dong.rstrip(b"\r\n")` removes an arbitrary run of CR/LF bytes, not one line terminator. The allowed diagnostic plus **CR CR LF** is accepted and all **41 bytes** are persisted, although its content contains an extra CR not present in `_STDERR_CHO_PHEP`. Ordinary LF (39 bytes) and CRLF (40) work. The additional CR is benign in the measurement; this defect admits only that trailing-byte family, and is **not** evidence of a credential leak. It still violates v2's exact allow-list contract and the zero-P3 criterion.

Fix the comparison to enumerate the supported complete wire forms (LF and, if intended, exactly one CRLF) or remove exactly one supported terminator before equality. Keep writing only an exact accepted form. Add a benign repeated-CR negative case and a mutant restoring unrestricted `rstrip`. Risk: accidentally rejecting native CRLF or accepting a partial final line; preserve explicit positive and negative line-ending cases.

**R26-COUNT-09 — P3 — `.claude/dev/launcher.py:1627`, `:1657` — class `discard-accounting-omissions` (NEW).**

Error draining reads and discards bytes without incrementing either drop counter; a safe-line write failure also exits before counting that discarded chunk. Reusing the existing failing-sink pattern with allowed line + existing frame + allowed line consumes **279 bytes**, persists **0**, records `RuntimeError`, but leaves `dem={}` (the receipt reports zero dropped bytes/chunks). A closed output similarly swallows `ValueError` and omits the lost allow-listed bytes. Error state correctly prevents `DO_DUOC` in the failing-sink case; this finding concerns the quantitative receipt, not a security fail-open.

Fix accounting at the reader boundary so successfully read, nonpersisted bytes remain accounted for during error drainage and after close. Define physical lines versus read chunks explicitly; current `stderr_bo_dong` already counts chunks on long lines. If a failed write makes the persisted count unknowable, report that limitation instead of an exact zero. Add failure-after-read and closed-sink counter assertions plus a mutant that skips drain accounting. Risk: double-counting the chunk that triggered failure or implying exact bytes after a partial low-level write; keep stored-log hashes separate from drop accounting.

**R26-EOF-10 — P3 — `.claude/dev/launcher.py:1913`, `:1914`, `:1687` — class `late-eof-certified-within-wait` (NEW; related to but distinct from R25-RACE-06).**

The 10-second join is bounded, but its outcome is not latched until after `f_err.close()`. A reader still alive when the join returns can reach EOF while close executes or the main thread is descheduled, then be certified `DO_DUOC`. The model-list/status mismatch from R25-RACE-06 is fixed; this narrower defect is the v2 requirement that EOF be reached **within the wait limit**.

`python3 review-scratch.irmJLS/late_eof.py`, rc 0, controls scheduling without changing parser/ledger code: a real reader waits on an event, a real `join(timeout=10)` returns after **10.000270 s with `is_alive()==true`**, and a wrapper releases the reader during `stderr.log.close()`. The supplied existing frame is then consumed to EOF; production writes **`DO_DUOC`**, launcher rc 0. The receipt contains the correct one-model list; no missing-model or leak claim is made for this probe. This is a deterministic timing seam, not a claim that ordinary file close normally has a measurable delay.

Fix in `lenh_run`: latch whether the reader completed at the join boundary before closing files or other work, and carry that outcome into the snapshot/status helper. If strict elapsed-time semantics are required, record reader completion time against the deadline. Add a scheduled finish-during-close case and a mutant that resamples liveness late. Risk: conservative false negatives at the boundary; retain the collected subset while marking the measurement incomplete, and keep the 10-second bound.

## Security / evidence boundary matrix

| Boundary | Independently established behavior and remaining limit |
|---|---|
| Exact allowed content, before/after trace | Existing secret fixture and prefix/suffix/non-UTF-8 variants pass. Unknown stderr is dropped from the first byte. No arbitrary preamble path remains. Repeated CR normalization is R26-ALLOW-08. |
| Partial lines, CR, LF and CRLF | EOF fragments are never written as safe diagnostics or parsed as complete frames. Full candidate tokens in a partial frame mark loss. CR-only existing frame: 201 dropped bytes, `mat=1`, `KHONG_DO_DUOC`; CRLF frame: 202 dropped bytes, one model, `DO_DUOC`. A fragment ending before a recognizable candidate token is only discarded; the recognizer cannot establish what a missing suffix would have contained. |
| Oversized records / read boundaries | Reads are bounded, continuation chunks cannot be persisted or parsed as whole frames. `stderr_bo_dong` counts read chunks, not universally physical lines. Candidate-token boundary blindness is R25-EVID-05. No large-memory attack executed. |
| ANSI / strict decoding | ANSI cleanup occurs only after safe-line comparison, so normalization cannot turn arbitrary colored trace into allowed disk output. Provenance test exercises supported ANSI cleanup. UTF-8 decoding is strict in production, but its independent mutant survives: R25-TEST-03. Unsupported framing fails to parse; loss detection is not a full JSON lexer. |
| Candidate false positives / real Codex frames | The supplied other-target and embedded-marker fixtures are rejected as models and counted as loss (two candidates), a conservative result explicitly tested. The candidate regex is unanchored and searches all rejected trace chunks, including potential nested/string/send-frame content; it cannot by itself prove such text is a lost server response. Live/sanitized authentic trace corpus coverage and real-frame false-positive rate were **not measured**. Executor-authored controls should cover those representations as well as escaped JSON and chunk boundaries; no new spoofed payload was generated. The code's codex-cli 0.163.0 observations are executor evidence, not independently rerun here. |
| Error drain / exception messages | Bounded drain consumes the remainder without raw writes; only exception class names are retained. Recorded errors force `KHONG_DO_DUOC`. Missing dropped-byte accounting is R26-COUNT-09. No exception-message secret content is copied by this filter. |
| Output closed while reader survives | Writes to a closed sink raise `ValueError` and are discarded without a raw fallback. Existing frame parsing can continue in memory. Closed-sink probe retains one model and reports only the frame's 201 dropped bytes, omitting the 39 allowed-but-unwritten bytes. Standalone helper can report `DO_DUOC`; production alive-reader protection normally downgrades, with the timing edge in R26-EOF-10. |
| Snapshot and positive evidence | Status uses the same copied model/error/counter values serialized to the receipt. Active-reader truth-table and real inherited-pipe case pass. No-model and recorded-error paths fail closed. Candidate losses can evade the chunk regex; late completion can evade the within-wait condition. |
| `run.json` and its atomic temporary file | Only selected response id/model/event fields, safe reason strings and counts are added. `_ghi_so` serializes that receipt to its unique temp file and replaces `run.json`; it never receives raw trace from the new filter. No trace-spooling temp file introduced. Existing fixture scans every retained run-directory file for its sample secret. Model/id are accepted as nonblank strings by contract, not restricted to a model-name allow-list. |
| `stdout.log`, prompt snapshot, child-owned logs | stdout remains a direct sink; prompt snapshots are existing input artifacts. The filter does not govern Codex-owned log stores or arbitrary child output. No authenticated run, user log-store inspection, live secret scan, or universal all-process no-disk proof is claimed. The fake child produces clean stdout and the run contains only `run.json`, `stdout.log`, `stderr.log` in the hash probe. |

## Regression results and acceptance limits

- **Timeout/tree kill:** full-suite cases t27, t28, t63, t66, t67, t158–t161 pass; the r925 Codex timeout case passes and asserts 124 plus the pre-timeout frame. `timeout125.py` rc 0 performs a real successful kill, then deliberately reports incomplete confirmation through the existing structured result: launcher/ledger **125**, `giet_tron_ven=false`, one model retained. This tests the 125 selector, not an actual surviving descendant or native Windows kill.
- **Windows:** creationflags (`CREATE_NEW_PROCESS_GROUP`), Job Object attachment and kill selector remain unchanged in the exact base diff. Mocked t79/t80/t81 pass. `codex`, `codex.exe`, `codex.cmd`, `CODEX.CMD` classify true; Python false. CRLF bytes measured as above. Native `.cmd` spawning, handle inheritance, creationflags and Job Object behavior were **not run on Windows**; no Windows-lane green claim. The new inherited-pipe case explicitly skips Windows there.
- **Non-Codex:** dedicated test rc 0 / 1/1; stderr persists as before, new keys absent. Source diff preserves non-Codex Popen/env/stderr branches.
- **Stored log evidence:** hash probe rc 0: stored stderr **39 bytes**, `stderr_byte=39`, SHA-256 equal. Full-suite r14 passes. `stderr_byte`/`stderr_sha256` remain measurements of persisted `stderr.log`, not original pipe volume; added drop counters have the R26-COUNT-09 caveat.
- **10-second join:** actual descendant-held-pipe case completes in **10.450 s**, returns `KHONG_DO_DUOC` with open-pipe reason; removing the join bound kills its intended test. The exact wait-boundary edge is R26-EOF-10.
- **Full Linux suite:** exact-head disposable full clone, unchanged launcher/test bytes; command `python3 review-scratch.irmJLS/fullsrc/.claude/dev/launcher_test.py --nhat-ky review-scratch.irmJLS/full-suite-journal.jsonl`, **rc 1**, **250/264 executed passed**, **274 total**, **14 failed**, **10 skipped**, **272.056 s**. Journal contains 274 starts/274 exits and `XONG TRON VEN`. Two skips require Windows; eight cannot build the fixture venv/pypdf setup. Failing cases are one doctor availability case (CLI tools absent from minimal PATH), two `/var/tmp` read-only errors, and eleven fixture home/materializer/ancestor cases. These are not a green acceptance result.
- **Base comparison:** `baseline_failures.py` driver rc 0; all **14/14** failing cases also fail with the exact base launcher selected against the unchanged head harness/fixtures in scratch. Case process codes are three rc 1 (`TinHieuChotCa`) and eleven rc 3 (the reviewer wrapper's distinct code for ordinary assertion/OSError failures); their same failures are retained in logs. No setup failures are counted as mutation kills, and no complete baseline-suite pass is claimed.
- **Bare Ruff:** ruff **0.15.15**; head/base `python3 -m ruff check --isolated --no-cache --select F <launcher.py> <launcher_test.py>` each rc 1, the same **5 pre-existing F841 findings**, delta **0**. This is a measured lint delta, not an absolute lint pass or workflow pin/probe attestation.
- **Size:** exact review-base diff remains **2 files, 498 added, 3 deleted**; 52 additions below v2 ceiling. No current GitHub authority/CI claim; the offline lease/spec and user instruction are the available authority evidence.

## Reproducible test and mutation ledger

Full commands, real process rc, stdout/stderr and timing: `review-scratch.irmJLS/commands.jsonl`; scripts and per-command logs are retained alongside it. Commands below ran through `review.py` with its recorded minimal environment. Driver rc 0 means the measurement completed, not that a failing test passed.

Each targeted row ran `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`; all output `1/1 qua, 0 bo qua, 0 hong`.

| Key | Case | rc | Seconds |
|---|---|---:|---:|
| T1 | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | 0.435 |
| T2 | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 0 | 0.370 |
| T3 | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | 0.276 |
| T4 | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0 | 0.510 |
| T5 | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0 | 0.297 |
| T6 | `r925_bo_loc_hong_xa_ong_co_gioi_han` | 0 | 0.320 |
| T7 | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | 0.310 |
| T8 | `r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup` | 0 | 0.381 |
| T9 | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | 0.261 |
| T10 | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0 | 0.471 |
| T11 | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0 | 0.375 |
| T12 | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0 | 0.386 |
| T13 | `r925_codex_qua_han_van_124_va_giu_khung_da_den` | 0 | 3.320 |
| T14 | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 0 | 10.450 |
| T15 | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0 | 0.307 |

Supplied mutation command: `python3 -B review-scratch.irmJLS/review.py supplied`, driver rc 0. Each table replacement matched once and compiled in its own temporary launcher file; both companions were copied unchanged. Each listed target ran through `python3 <scratch>/review.py one <temporary-launcher> <case>`. All **32/32** target executions returned rc **1 specifically from `TinHieuChotCa`**; no skipped/setup/ordinary-assertion kills. **25/25 supplied mutants killed.**

| Mutant | Intended tests | Killed / intended |
|---|---|---:|
| `r25_ghi_moi_dong_tron` | T1, T2 | 2/2 |
| `r25_cho_phep_theo_tien_to` | T2 | 1/1 |
| `r25_cho_phep_ca_dong_cut` | T2 | 1/1 |
| `r25_bo_go_ansi` | T3 | 1/1 |
| `r25_khung_moi_target` | T3 | 1/1 |
| `r25_moi_su_kien` | T3 | 1/1 |
| `r25_nhan_id_model_rong` | T3 | 1/1 |
| `r25_gop_theo_id` | T3 | 1/1 |
| `r25_bo_dem_mat` | T3, T5, T4 | 3/3 |
| `r25_parse_khong_can_ca_dong` | T5 | 1/1 |
| `r25_doc_khong_tran` | T4 | 1/1 |
| `r25_xa_ong_khong_tran` | T6 | 1/1 |
| `r25_noi_rust_log_thua_ke` | T10 | 1/1 |
| `r25_khong_bat_trace` | T1 | 1/1 |
| `r25_DO_DUOC_khi_loc_hong` | T9, T7 | 2/2 |
| `r25_DO_DUOC_khi_ong_con_mo` | T9, T14 | 2/2 |
| `r25_DO_DUOC_khi_mat` | T9, T7 | 2/2 |
| `r25_DO_DUOC_khong_khung` | T9, T11 | 2/2 |
| `r25_so_khong_chuyen_loi` | T7 | 1/1 |
| `r25_so_khong_chuyen_mat` | T7 | 1/1 |
| `r25_chup_truoc_chot_luong` | T8 | 1/1 |
| `r25_doc_ong_khong_han` | T14 | 1/1 |
| `r25_bo_loc_hong_khong_xa_ong` | T15 | 1/1 |
| `r25_bo_loc_hong_khong_ghi_loi` | T15 | 1/1 |
| `r25_loc_ca_luot_khong_phai_codex` | T12 | 1/1 |

Supplementary mutation command: `python3 -B review-scratch.irmJLS/review.py extra`, driver rc 0. Each of the three code-guard removals described in R25-TEST-03 runs every T1–T15: **15/15 pass per mutant**, all case rc **0**, **0/3 killed**, **45/45 total passes**. No new attack content.

| Other command | rc | Actual result |
|---|---:|---|
| `python3 <scratch>/observations.py` | 0 | Existing fixture/line-ending/counter/hash observations quoted above; full JSON in `logs/observations.log`. |
| `python3 <scratch>/timeout125.py` | 0 | Launcher/ledger 125, incomplete-confirmation result, one model. |
| `python3 <scratch>/late_eof.py` | 0 | Actual 10 s join returns alive; EOF during close; DO_DUOC. |
| `python3 <scratch>/baseline_failures.py` | 0 | All 14 previously failing cases also fail with base launcher; per-case rc 1/3 as explained above. |
| `python3 <scratch>/fullsrc/.claude/dev/launcher_test.py --nhat-ky <scratch>/full-suite-journal.jsonl` | 1 | 250/264 executed passed; 14 failed; 10 skipped; 274/274 start/end records. |
| `python3 -m ruff check --isolated --no-cache --select F <head files>` | 1 | Five F841, no new findings relative to base. |
| Same lint command on base files | 1 | Same five F841. |

## Final integrity and disposition

Final `git -C src rev-parse HEAD HEAD^{tree}` rc **0** returns the same required SHA/tree. `git -C src status --porcelain=v1 --untracked-files=all --ignored` rc **0**, empty; both initial and final tracked/untracked/ignored snapshots are clean. `git diff --quiet`, `git diff --cached --quiet`, and `git diff --check e739ac1b74024a20949425c447fb6cf025317c0e HEAD` each rc **0**. `git fsck --connectivity-only --no-dangling` rc **0**, no output; partial-clone/promisor config query rc **1**, no matches; shallow flag is false.

Final byte comparison against `git show HEAD:<path>` succeeds for **2/2** reviewed files; the full-suite scratch clone matches both files too. SHA-256: launcher `11a8197bfe1fff71d77e68c76ee9213f93ea07bc5ff86cd96546eb3bb202bf18`; test `17f952ce5bd11a6655e10203fe8e05e2874bec820e9328fe235ba7a45d116d21`. Both mutation companions match source; **28/28** temporary mutant sources compile. Evidence: `review-scratch.irmJLS/integrity.json`. Clean snapshots establish no observed delta at the boundaries, not a forensic proof of every possible intermediate write. No source edits or source commits were made; tests create seed commits only in disposable fixture repositories.

No pushes, GitHub comments, authority/PR/CI readback, real credentials, authenticated Codex runs, or newly authored exploit payloads. Synthetic secret fixtures, existing harmless frames, finite benign byte variations, source-guard removals and controlled scheduling/error seams supplied the measurements. Native Windows and the spec's real authenticated Codex/no-secret acceptance remain unmeasured. The enclosing launcher execution receipt, exact serving model/effort/session ID and independent server identity attestation remain unavailable to this reviewer; the runtime declaration and observed local execution are stated at the top, without upgrading them to machine-attested model evidence.

Five open classes/findings: **R25-EVID-05 P2**, **R25-TEST-03 P2**, **R26-ALLOW-08 P3**, **R26-COUNT-09 P3**, **R26-EOF-10 P3**. Totals: **0 P0, 0 P1, 2 P2, 3 P3**. The original P1 stderr fail-open mechanism is closed in the reviewed scope; the user's zero-P0–P3 criterion is not met. Findings concern the already-merged head; fixes belong on the new branch from master as instructed. No approval or land authority is asserted.

Completed UTC: `2026-10-25T07:04:27.327865+00:00`.

VERDICT: changes_requested
