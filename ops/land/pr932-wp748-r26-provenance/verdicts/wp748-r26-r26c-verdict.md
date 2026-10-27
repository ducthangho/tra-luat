# WP748 r26 round 3 independent read-only review

Disposition: **changes requested — 0 P0, 0 P1, 1 P2, 1 P3 open.**

Reviewer: OpenAI Codex, as identified by this session's runtime instructions (GPT-6 based). Provider: `openai_codex`; model family: OpenAI. Observed execution surface: tool-mediated local shell in managed Linux; transport: machine; GitHub submitter: none. Exact serving model/build/effort/session ID, enclosing CLI-versus-service surface, `launcher.py run` invocation, and outer execution receipt are not independently visible or verified. Runtime identity is a declaration, not serving-model attestation. The invocation is requester-reported. No credentials or GitHub authority/CI content were accessed; authority issue #748 issuecomment-6394503720 cannot be read from GitHub in this review.

Review class: sensitive. Reviewed SHA: `97bb4c54b5bd925b88a5fcae03178f79c93a45f5`; tree: `2f8064abfa01cfb19a59c16aab26b47422bfbc59`.

Identity check: `git -C src rev-parse HEAD HEAD^{tree} HEAD^ HEAD^^` returned the expected SHA/tree and parents `143d43fcfe9f2a4b116afd169014ed3d6d598403`, `b306e15a96a4d9d05d2ba4191cbd071fa7820ee7` (rc 0). `rev-parse --is-shallow-repository` returned `false`; status was empty; symbolic-ref emitted no branch; diff name-only returned exactly `.claude/dev/launcher.py` and `.claude/dev/launcher_test.py`.

`src/` was treated read-only. Mutations and review harnesses live only in scratch. This is an independent reviewer session, not executor work; no source edits, source commits, pushes, GitHub comments, or authenticated Codex runs were performed.

Started UTC: 2026-10-25T09:44:47.293207+00:00

## Verified context and first measurements

Local `master` spec lookup rc 128 (path absent); fallback at `origin/ops/wp748-r25-g25-lease` rc 0, SHA-256 **f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb**. Lease read rc 0. The branch contains this exact head locally. Whether the commit has ever been pushed cannot be independently established offline. The user authorizes this independent local review; no live authority/CI claim is made. Repository reviewer guidance and the supplied prior verdicts were read.

Evidence directory: `review-r26c-eay3wkyl/`; command/rc/output/timing ledger: `commands.jsonl`, with individual command records in `logs/`. Test processes use a minimal explicit environment, scratch HOME/TMPDIR, disabled bytecode, no inherited authentication variables, and an absent Codex home. Tests create Git seed commits only inside their disposable fixtures; no reviewed-repository commits are made.

`python3 -B review-r26c-eay3wkyl/review.py integrity`, rc 0: detached check rc 1/empty; tracked/untracked/ignored status rc 0/empty; branch containment includes `agent/wp748-r26-claude`; intervening-history command rc 0/empty.

Size, **not a code finding**: `git -C src diff --numstat <base> HEAD -- .claude/dev/launcher.py .claude/dev/launcher_test.py`, all rc 0:

| Base | launcher + / - | test + / - | Total added / deleted |
|---|---:|---:|---:|
| `e739ac1b74024a20949425c447fb6cf025317c0e` (cumulative, merged part included) | 247 / 4 | 765 / 0 | **1,012 / 4** |
| `b306e15a96a4d9d05d2ba4191cbd071fa7820ee7` (new delta only) | 178 / 68 | 438 / 35 | **616 / 103** |
| `143d43fcfe9f2a4b116afd169014ed3d6d598403` (round 3 alone) | 138 / 64 | 325 / 48 | **463 / 112** |

Exactly two files; cumulative additions exceed v2's 550 ceiling by **462**. Owner escalation is requester-reported, not independently verified. Unrelated master changes are excluded from this packet measurement.

`python3 -B review-r26c-eay3wkyl/review.py targeted`, rc 0: **30/30 cases pass** (15 r925 + 15 r926). Each invokes the requested `python3 src/.claude/dev/launcher_test.py --lap-ca <full-name> --lan 1` and reports `1/1 qua, 0 bo qua, 0 hong`, rc 0. Exact names and outputs: `targeted.json`. Final mutation and independent boundary results follow below.

## Independent closure measurements

`python3 -B review-r26c-eay3wkyl/review.py exec observations observations.py`, rc 0, reuses existing fixtures and safe allowed bytes:

- Prior continuation fixture: **632 bytes in / 632 dropped / 0 stored**, one model, no errors, `mat=1`, `KHONG_DO_DUOC` at **all five caps 256/330/340/350/360**. The former cap-340/350 false completeness is closed. The supplied alignment sweep also passes.
- Other-event fixture: **382 bytes dropped**, one accepted model, no `mat`/`khong_ro`, **DO_DUOC at both cap 190 and 4096**. The former oversized-other-event misclassification is closed.
- Allow-list endings: LF 39/39 bytes stored; CRLF 40/40; CR CR LF 0/41; CR-only 0/39; EOF-cut 0/38. Frame CR-only/EOF-cut count one loss; CRLF yields one model.
- Generic write failure: **264/264 discarded bytes counted**, `RuntimeError`; closed sink: **264/264 counted**, no raw writes. Drop-line counts explicitly mean discarded read chunks.
- Native unbuffered partial I/O (`io.FileIO`, scratch file, process-local `RLIMIT_FSIZE=10`, restored afterward): **43 input, 10 stored, 33 actual unpersisted, 33 reported dropped**, `OSError`. This respects the new syscall contract. The earlier custom sink that writes and then raises within the same `write` call violates that contract and is no longer a valid production counterexample.
- Fake-child persisted-log check: launcher rc 0, **stderr_byte=39**, actual size 39, matching SHA-256 `1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721`; 186 dropped bytes. Run directory contains only `run.json`, `stdout.log`, `stderr.log`.

Supplied mutations: **52/52 mutated launcher copies compile with unique replacements; 62/62 target executions raise target-origin TinHieuChotCa (rc 1)**. No ordinary exception or skip receives mutation credit. `review.py supplied` initially returned rc 1 *after all requested executions*, when it reached an unrelated longer-format DOT_BIEN entry; this was a reviewer-driver unpacking error. The scratch driver was corrected, and `python3 -B review-r26c-eay3wkyl/summarize_mutants.py` rc 0 verifies every expected saved command record and creates `mutations.json`; no missing execution was inferred to pass.

`python3 -B review-r26c-eay3wkyl/extra_mutants.py`, rc 0: the **three round-2 surviving removals are all killed, 3/3** on the current head. Generic write-error count removal fails `r926_ghi_het_dem_dung_phan_chua_ghi` (`byte_bo=4`, expected 33); default-unlatched fail-open fails `r926_ghi_so_truoc_khi_chot_khong_DO_DUOC` (`DO_DUOC`); production late latch with a real 10 s join fails `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC`.

Production-order mutation caveat: both `r26_san_xuat_dong_tep_truoc` and the adapted old late-wait mutant first fail the target's fixture assertion because the second close overwrites the first-close observation. `python3 -B review-r26c-eay3wkyl/review.py exec order_mutant_audit order_mutant_audit.py`, rc 0, diagnostically records all target assertions without stopping at the first: **both also fail the final on-disk-status assertion with `DO_DUOC None`**. Thus the production test does contain the relevant safety assertion; the raw first failure alone should not be described as that final assertion. The supplied object-level order mutant independently fails the final receipt assertion normally. No reviewed test bytes were changed by this diagnostic instrumentation.

A further independent zero-progress-write removal is killed by the existing `tra_0` subcase: it writes all 39 allowed bytes and reports no error, where the test requires zero stored, OSError, and 39 dropped (+4 drain bytes). Unlike the three earlier gaps, this guard lacks its own supplied mutation; the formal coverage finding is detailed below.

## ĐỐI CHIẾU LƯỢT TRƯỚC — each earlier finding

| Finding | Status on this head | Independent evidence |
|---|---|---|
| R25-SEC-01 P1 | Closed for the reported arbitrary-stderr disk path; remains closed. | Exact allow-list and sample-secret run-directory cases pass; unrestricted/prefix/continuation mutations fail. No raw fallback exists. |
| R25-MEAS-02 P2 | Closed for the earlier provenance defect; remains closed. | Provenance/event/UTF-8/nonblank id/model cases pass and mutants fail. Accepted fields come from complete strict JSON receive frames; this is format provenance, not cryptographic server attestation. |
| R25-TEST-03 P2 | **ĐÃ VÁ THẬT for the three round-2 survivors.** | All three re-applied removals now die at named r926 targets; production late-wait diagnostic also confirms the final receipt wrongly becomes DO_DUOC on the mutant. The independent zero-progress guard added in this round has a narrower new P3 gap, R26-TEST-12 below. |
| R25-ROBUST-04 P2 | Closed for unbounded normal/error-drain reads; remains closed. | Both bounded-read cases pass; both unbounded-read mutants fail. Production cap remains 4 MiB per read. |
| R25-EVID-05 P2 | **VÁ HỜ for the completeness class; original alignment hole fixed, whole-line failure gap remains OPEN.** | Old 632-byte fixture at all five caps now has mat=1 / KHONG_DO_DUOC; supplied alignment mutants die. Whole-line parse failure plus nonliteral event encoding bypasses both mat and khong_ro; see the control-flow finding below. |
| R25-RACE-06 P2 | Closed for snapshot/status mismatch; remains closed. | Liveness latches before copies; the ordering and late-resampling cases pass and mutants fail. |
| R25-CONTRACT-07 P2 | Closed under superseding v2; remains closed. | Diagnostic loss is expressly authorized. Non-Codex behavior remains separately tested. |
| R26-ALLOW-08 P3 | Closed; remains closed. | Exact LF/CRLF accepted, repeated CR/partial lines rejected; r26 rstrip mutant dies at CR_CRLF assertion. |
| R26-COUNT-09 P3 | **ĐÃ VÁ THẬT under the actual unbuffered contract.** | Native FileIO short-write/error: 10 persisted + 33 dropped = 43 input. Drain/closed-sink totals correct; dedicated partial-count, write-loop, write-error and unbuffered-open mutants die. |
| R26-EOF-10 P3 | Closed for finish-during-close; remains closed. | Real 10 s production boundary case passes; object close-order mutant reaches the final receipt-status assertion; adapted old production mutation also yields incorrect DO_DUOC. |
| R26-CLASSIFY-11 P3 | **ĐÃ VÁ THẬT for the reported known-other-event regression.** | Same 382 bytes, cap 190 and 4096 both DO_DUOC, no mat/khong_ro; cap sweep and independent prefix/noncandidate/strict-type mutants behave as intended. |
| Unreachable `bo_loc is None` branch note | Removed, without pretending Popen failure now produces model metadata. | Actual absent `codex` with public probe override: rc 2, receipt hong, ma_thoat null, no model/drop keys. The exception still exits before normal completion. No false DO_DUOC. |

Three of the four findings open in round 2 are closed (**3/4**); R25-EVID-05 fixes its measured alignment counterexample but leaves a whole-line parse-failure route in the same incomplete-evidence class. All three supplemental round-2 mutants now die (**3/3**). The additional classification result below was found after the first closure measurements; the table reflects the final assessment.

## Remaining findings

**R25-EVID-05 — P2 — `.claude/dev/launcher.py:1658`, `:1702`–`:1704` — incomplete whole-line evidence can still be reported complete (continued class).**

The single-chunk complete-line branch returns before the unconfirmed-header classifier. `_phan_loai_khung` catches UTF-8/JSON `ValueError` and returns `(None, None)`. If the candidate's event key/value uses JSON escapes, `_RE_UNG_VIEN_GON` does not recognize it literally. A strict decode failure elsewhere in that complete receive record therefore leaves both `mat` and `khong_ro` unchanged; with an earlier accepted model and EOF, `_ket_luan_model` returns **DO_DUOC** despite the discarded unclassifiable response. The multi-chunk/EOF branch has an unknown-header fallback; the complete single-chunk branch does not. v2 explicitly requires incomplete status for unreadable candidate evidence, including UTF-8 damage.

Evidence and limits: `python3 -B review-r26c-eay3wkyl/review.py exec classifier_controls classifier_controls.py`, rc 0, observes the **unchanged supplied fixtures**: escaped-key bad-id/good-id frames both match the receive header and have `literal_candidate=false`; they are handled only by successful JSON parsing. The separate supplied invalid-UTF-8 fixture returns `parsed_kind=null`, `errors=[]`, and is counted only because its key remains literal. `.../review.py exec classifier_failure_seam classifier_failure_seam.py`, rc 0, injects exactly the parser's `(None, None)` failure result for the existing benign escaped-key frame, after an existing accepted frame: the real reader/snapshot/status path reports **DO_DUOC**, one model, **329 dropped bytes**, no loss/unknown counter. This proves the downstream classification gap under that failure result. It is **not** an end-to-end malformed-byte reproduction: combining the encoding and corruption into new attack content was deliberately not performed, as instructed. The raw-input reachability described above follows from the strict-decode catch and literal-only candidate regex.

Fix direction: in `_ket_dong`, retain the distinction between a confirmed other event and an unclassifiable receive record on the complete-line path too. Carry an unknown/failure classification into `khong_ro` or equivalent conservative evidence state when parsing fails, rather than treating absent literal tokens as proof that no model response was lost. Do not weaken strict decoding or persist raw input. Have the executor add a complete-line escaped-event/decoding-failure combination with earlier positive evidence and an independent fallback-removal mutant; the final receipt must remain KHONG_DO_DUOC. Risk: classifying every received non-model format as unknown can create false negatives, so retain explicit confirmed-other-event controls and distinguish “unknown” from positively identified lost candidate. No production patch or new exploit bytes are supplied.

**R26-TEST-12 — P3 — `.claude/dev/launcher_test.py:10829` (guard at `.claude/dev/launcher.py:1686`) — missing independent zero-progress-write mutant.**

The new `_ghi_het` loop has an explicit no-progress guard (`if not n: raise OSError(...)`) and the target has a `tra_0` subcase, but `DOT_BIEN` has no mutation removing *only* that guard. `r26_ghi_khong_lap` discards the returned count, removes the zero-progress check, and marks the entire input written together; it is killed at the earlier **ngan_roi_du** short-write subcase. That kill cannot separately establish the zero-progress guard, contrary to v2's “each new guard has its own mutation” requirement.

Measurement: `python3 -B review-r26c-eay3wkyl/extra_mutants.py`, driver rc 0; `extra_zero_write_guard` removes exactly the two-line no-progress check from a temporary launcher copy (unique match, compiles). Its named target `r926_ghi_het_dem_dung_phan_chua_ghi` returns **rc 1 / TinHieuChotCa at tra_0**: actual stored 39 bytes, errors `[]`, `byte_bo=4`; expected zero stored, OSError, and 43 dropped including the four drained bytes. Thus the existing test is effective; the missing artifact is the independent supplied mutation, not a demonstrated production failure. The full mutation pairs and assertion output are in `extra-mutations.json`.

Fix direction: add a separate zero-progress guard-removal entry in `DOT_BIEN`, targeting the existing test; retain the independent short-write-loop mutant. No production change or new payload is needed. Verify it fails specifically at `tra_0`, not setup/fixture errors. Risk: a fake sink returning zero forever can hang when the guard is removed, so preserve the existing finite zero-then-progress fixture and bounded reviewer/test execution. Priority is P3 because runtime behavior and the target assertion already work; the sensitive packet's explicit independent-mutation acceptance condition remains unmet.

## Required case ledger

For each row, command is `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`; rc **0**, output **1/1 qua, 0 bo qua, 0 hong**.

| Key | Case | Seconds |
|---|---|---:|
| T1 | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0.475 |
| T2 | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 0.331 |
| T3 | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0.325 |
| T4 | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0.291 |
| T5 | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0.294 |
| T6 | `r925_bo_loc_hong_xa_ong_co_gioi_han` | 0.386 |
| T7 | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0.337 |
| T8 | `r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup` | 0.296 |
| T9 | `r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai` | 0.386 |
| T10 | `r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat` | 0.434 |
| T11 | `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 0.345 |
| T12 | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 0.354 |
| T13 | `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 0.33 |
| T14 | `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 0.432 |
| T15 | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0.722 |
| T16 | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0.456 |
| T17 | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0.319 |
| T18 | `r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE` | 0.36 |
| T19 | `r926_ghi_het_dem_dung_phan_chua_ghi` | 0.316 |
| T20 | `r926_ghi_so_truoc_khi_chot_khong_DO_DUOC` | 0.365 |
| T21 | `r926_ket_thuc_chot_luong_TRUOC_khi_dong_tep` | 0.283 |
| T22 | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 0.33 |
| T23 | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 10.426 |
| T24 | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0.319 |
| T25 | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0.49 |
| T26 | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0.446 |
| T27 | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0.476 |
| T28 | `r925_codex_qua_han_van_124_va_giu_khung_da_den` | 3.335 |
| T29 | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 10.519 |
| T30 | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0.374 |

Supplied mutant executions use `python3 -B review-r26c-eay3wkyl/review.py one <scratch-mutant-launcher.py> <case>`; **each rc 1 / target-origin TinHieuChotCa**, never ordinary-error credit. Each mutant changes only its temporary launcher; companion modules are copied unchanged. Target keys refer to the table above.

| Mutant | Targets | Killed/targets |
|---|---|---:|
| `r25_ghi_moi_dong_tron` | T1, T2 | 2/2 |
| `r25_cho_phep_theo_tien_to` | T2 | 1/1 |
| `r25_cho_phep_ca_dong_cut` | T12 | 1/1 |
| `r26_cho_phep_cat_moi_CRLF` | T12 | 1/1 |
| `r25_bo_go_ansi` | T3 | 1/1 |
| `r25_khung_moi_target` | T3 | 1/1 |
| `r25_moi_su_kien` | T3 | 1/1 |
| `r25_nhan_id_model_rong` | T3 | 1/1 |
| `r25_gop_theo_id` | T3 | 1/1 |
| `r25_bo_dem_mat` | T3, T18 | 2/2 |
| `r26_bo_dem_mat_nhieu_doan` | T5, T4, T15 | 3/3 |
| `r26_phan_loai_theo_token` | T18 | 1/1 |
| `r25_parse_khong_can_ca_dong` | T5 | 1/1 |
| `r25_doc_khong_tran` | T4 | 1/1 |
| `r25_xa_ong_khong_tran` | T6 | 1/1 |
| `r26_bo_duoi_vat` | T15 | 1/1 |
| `r26_khong_bo_khoang_trang` | T15 | 1/1 |
| `r26_bo_xac_nhan_su_kien_khac` | T16 | 1/1 |
| `r26_dau_dong_khong_noi` | T16 | 1/1 |
| `r26_loai_khong_utf8_thay_the` | T17 | 1/1 |
| `r26_khong_ro_khong_dem` | T17 | 1/1 |
| `r26_khong_ro_moi_dong_dai` | T10 | 1/1 |
| `r26_utf8_thay_the` | T11 | 1/1 |
| `r25_noi_rust_log_thua_ke` | T25 | 1/1 |
| `r25_khong_bat_trace` | T1 | 1/1 |
| `r25_DO_DUOC_khi_loc_hong` | T24, T7 | 2/2 |
| `r25_DO_DUOC_khi_ong_con_mo` | T24, T29 | 2/2 |
| `r25_DO_DUOC_khi_mat` | T24, T7 | 2/2 |
| `r26_DO_DUOC_khi_khong_ro` | T17 | 1/1 |
| `r25_DO_DUOC_khong_khung` | T24, T26 | 2/2 |
| `r25_so_khong_chuyen_loi` | T7 | 1/1 |
| `r25_so_khong_chuyen_mat` | T7, T14 | 2/2 |
| `r26_so_khong_chuyen_khong_ro` | T17 | 1/1 |
| `r25_bo_chot_luong` | T8 | 1/1 |
| `r26_lay_mau_lai_luong_muon` | T9 | 1/1 |
| `r26_mac_dinh_chua_chot_la_xong` | T20 | 1/1 |
| `r25_doc_ong_khong_han` | T29 | 1/1 |
| `r26_dong_tep_truoc_chot` | T21, T23 | 2/2 |
| `r26_san_xuat_dong_tep_truoc` | T23 | 1/1 |
| `r26_tep_stderr_co_dem` | T23 | 1/1 |
| `r25_bo_loc_hong_khong_xa_ong` | T30 | 1/1 |
| `r26_xa_khong_dem` | T13 | 1/1 |
| `r25_bo_loc_hong_khong_ghi_loi` | T30 | 1/1 |
| `r26_tep_dong_khong_dem` | T13 | 1/1 |
| `r26_ghi_loi_khong_dem` | T19 | 1/1 |
| `r26_ghi_dem_ca_doan` | T19 | 1/1 |
| `r26_ghi_khong_lap` | T19 | 1/1 |
| `r26_luong_hong_lot_ra` | T22 | 1/1 |
| `r26_luong_hong_khong_dong_ong` | T22 | 1/1 |
| `r26_luong_hong_khong_ghi_loi` | T22 | 1/1 |
| `r26_cho_luong_chua_chay` | T22 | 1/1 |
| `r25_loc_ca_luot_khong_phai_codex` | T27 | 1/1 |

Mutation interpretation: `r25_ghi_moi_dong_tron` first fails because it bypasses model parsing; its second target independently detects forbidden disk output. `r25_bo_chot_luong` deletes the latch rather than reversing snapshot order; the ordering case still detects the resulting incomplete snapshot. `r26_san_xuat_dong_tep_truoc` has the fixture-first qualification measured above. `r26_ghi_khong_lap` removes multiple independent write behaviors; its missing focused no-progress companion is R26-TEST-12. The remaining r26 failures correspond to the stated loss, classification, accounting, liveness, or reader-start guards; exact assertion texts and tracebacks are retained in `mutations.json`.

## Security and regression boundary assessment

| Boundary | Established behavior and limits |
|---|---|
| Allow-list to disk | Only exact complete LF/CRLF constant lines enter the write helper; comparisons precede ANSI cleanup. Arbitrary prefixes/suffixes, partial lines, repeated CR and existing sample-secret fixtures are suppressed. No raw trace fallback or trace spool was found. Partial I/O may leave a safe constant prefix; it does not introduce trace bytes. |
| One complete read | A parsed candidate is accepted only with correct provenance, strict UTF-8, eligible event, nonblank id/model; bad eligible metadata counts one loss. **Unclassifiable complete receive records can bypass both counters: open R25-EVID-05.** The escaped-key/UTF-8 controls each pass separately and do not cover their combination. |
| Multiple reads / cross-boundary token | Each physical line is classified once, at LF or EOF. A compacted 64-byte tail carries literal candidate matching across reads; the supplied alignment/whitespace sweeps and old counterexample pass. Bounded reads remain 4 MiB; no large-memory exhaustion test was performed. |
| EOF-cut | Never persisted as an allowed diagnostic or accepted as a complete model frame. Literal candidate fragments count loss; an intact receive header without confirmed type is unknown and blocks DO_DUOC. Unsupported/incomplete headers and alternate token/ANSI encodings remain directions for executor-authored tests, not newly generated attack content or a universal-parser claim. |
| Confirmed other event | For oversized/EOF records without a candidate token, the bounded prefix can confirm a strict unescaped noncandidate type. Known other-event controls across caps pass. Escaped/invalid type prefixes become khong_ro when not confirmable; their supplied independent mutants die. |
| Error drain and writes after close | Errors record exception class names only; the bounded drain counts discarded bytes without persisting them. Generic/partial writes count only the confirmed unwritten remainder. Closed sinks discard the allowed bytes and continue; the production alive-reader latch prevents that late work from certifying timely completion. Counters on an unfinished stream describe the snapshot, not a claimed final total of future bytes. |
| Snapshot and join | `ket_thuc(10)` joins, latches liveness, then closes stderr; `ghi_so` copies models/errors/counters and uses those copies for status and serialization. No-model, error, active-reader, loss and unknown truth-table/target cases pass. Actual inherited-pipe and production finish-during-close tests pass with the 10 s bound. There is no separate EOF timestamp proving a nanosecond-level deadline if descheduled between join return and is_alive; that unmeasured scheduling limit is not misrepresented as a timestamp guarantee. |
| Run directory and other sinks | The persisted fake-child run contains only run.json/stdout.log/stderr.log; its sample-secret scan passes. Atomic receipt writing receives selected metadata/counts, not raw trace. Response id/model are arbitrary nonblank strings under the spec's source contract. stdout and prompt snapshots remain existing direct output/input sinks, and child-owned log stores were not inspected. No universal all-process no-disk certification is claimed. |
| Timeout / tree kill | Full-suite t27/t28/t63/t66/t67/t158–t161 pass (9/9), and the required r925 timeout case retains the frame and asserts 124. `regressions_corrected` independently gives launcher=ledger=125 with giet_tron_ven=false and one retained model after a real successful kill deliberately reported as incompletely confirmed. This exercises the 125 decision without leaving a descendant alive. |
| Windows | creationflags/Job Object/command construction remain unchanged in the delta. Full-suite t79/t80/t81 mocks pass (3/3); codex/codex.exe/codex.cmd/CODEX.CMD detection and exact CRLF bytes were measured. Native Windows process creation, `.cmd` execution, handle inheritance, Job Object behavior and Windows CI are **not_run / unverified**; Linux mocks do not count as that lane. |
| Non-Codex / hashes | Required non-Codex case and r14 pass: no model/drop keys are added, stderr behavior unchanged. Independent Codex hash probe matches stored bytes and hash. stderr_byte/stderr_sha256 still describe the persisted log, not original pipe volume. |
| Popen failure | Public probe override plus nonexistent executable named codex: rc 2; receipt hong, ma_thoat null, no model/drop fields. No false success; removal of the unreachable fallback leaves the actual failure path unchanged. |
| Reader-thread start failure | Actual lenh_run with Thread.start forced to raise RuntimeError closes the pipe and finishes, rather than hanging on an unread pipe. Final receipt is KHONG_DO_DUOC with RuntimeError, stderr size 0; fake Python child returns 120 after broken stderr, which launcher preserves. Drop count zero reflects no successful reads; unread/unwritten child output is not a measured total. Four supplied startup mutants fail the dedicated target. |

`python3 -B review-r26c-eay3wkyl/review.py exec regressions_corrected regressions.py`, rc **0**, records the Popen/start-failure/125 results above. The first scratch regression invocation returned rc 1 because the reviewer wrapper passed the wrong KetGiet constructor arity after successfully killing the child; that driver error was corrected and is not attributed to the reviewed code or counted as a test pass.

## Full Linux suite and acceptance limits

`python3 review-r26c-eay3wkyl/fullsrc/.claude/dev/launcher_test.py --nhat-ky review-r26c-eay3wkyl/full-journal.jsonl` (absolute equivalents in command ledger): **rc 1**, **265/279 executed cases passed**, **289 total, 14 failed, 10 skipped**, **295.888 seconds**. The journal has **289 starts / 289 exits**, ends `XONG TRON VEN`. The suite ran in a disposable full clone of the exact reviewed head so hook/setup cases cannot modify src/. Both reviewed files in that clone match HEAD bytes.

Skipped: two native Windows cases and eight unavailable venv/pip fixtures. Failures concern unavailable CLI capabilities, two read-only /var/tmp fixture paths, and eleven credential-fixture/home/materializer/ancestor checks. Tests use synthetic fixture credentials only; no real credential was inherited, read, or used. Doctor's unauthenticated capability probes reported unavailable GitHub/MCP access; no authority, PR or CI content was read.

`python3 -B review-r26c-eay3wkyl/baseline_failures.py`, driver rc **0**: **14/14 failing cases also fail with the exact base launcher** and the same unchanged head test harness in the disposable full clone. Three case processes return rc 1/target assertion, eleven rc 3/ordinary assertion or OSError; this is comparison evidence, not mutation credit. Full outputs: `baseline-failures.json`. The full suite is **not N/N green**, and no full-baseline green result is claimed. No changed-code regression is attributed to these reproduced baseline failures.

An authenticated live Codex run, live secret-store scan, Windows green lane, current GitHub authority and the enclosing reviewer execution receipt were **not verified**. These acceptance limits and the separate size overage remain owner/executor evidence items; this offline report does not grant merge/land authority.

## Final integrity and disposition

`python3 -B review-r26c-eay3wkyl/final_integrity.py`, rc **0**: required HEAD/tree/parents still match; tracked, untracked and ignored status empty; git diff --quiet, diff --cached --quiet, diff --check for the reviewed delta, and fsck --connectivity-only --no-dangling all rc **0**. Partial-clone/promisor query rc **1**, no matches. Reviewed source bytes match HEAD **2/2**; disposable full-suite copies match **2/2**; all **56/56** supplied/supplementary mutated launcher files compile. AST comparison verifies `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, and `KetGiet` unchanged versus base (**6/6**). Runtime: Linux, Python **3.13.16**.

Source SHA-256: launcher `5e7a87c50c567bf9b82ae4ce5ffd41fbf46821bf04d1ecae86bfba67f647317c`; test `39fad7a9e1ef0a964aa434b1b1b8fced8e6a50b96ef400a9cf0af33644658c94`. Clean initial/final snapshots and byte comparisons show no observed source delta, not a forensic attestation of every intermediate operation. No new exploit payloads were authored; the remaining encoding/corruption direction is described in words and supported by existing-input controls plus a clearly labeled parser-failure seam.

Open: **R25-EVID-05 P2** (whole-line unclassifiable candidate can still certify completeness), **R26-TEST-12 P3** (zero-progress-write guard lacks its own supplied mutant). No P0/P1 established. Required cases **30/30 pass**; supplied mutants **52/52 killed**, **62/62 target signals**, subject to the first-assertion qualifications above. Three round-2 open findings closed; one remains partially fixed. The owner's zero-P0–P3 requirement is not met. Size is separate: **1,012 cumulative additions**, **616 new-delta additions**, **463 round-3-only additions**, exactly two files.

Completed UTC: **2026-10-25 10:00:03 UTC**.

VERDICT: changes_requested
