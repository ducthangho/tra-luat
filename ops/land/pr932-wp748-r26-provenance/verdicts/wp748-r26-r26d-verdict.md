# Independent review — WP748 r26, round 4

Disposition: **changes requested — 0 P0, 0 P1, 0 P2, 1 P3 open (two missing mutation entries).** Both findings open in round 3 are fixed.

Review class: sensitive. Reviewer: OpenAI Codex; runtime developer context identifies this agent as Codex based on GPT-6. Provider: `openai_codex`; model family: OpenAI. Observed execution surface: tool-mediated shell in managed Linux; transport: machine; GitHub submitter: none. Exact serving model/build/effort/session ID, enclosing CLI-versus-service surface, launcher invocation, and outer execution receipt are not independently visible or attested. The invocation is requester-reported. No GitHub access or credentials used; authority #748 issuecomment-6394503720 cannot be independently read here.

Reviewed commit: `0fe659e30e151f4ce3dce13789fa6622ca6c6b47`.
Reviewed tree: `9244cf09cfffcbc6e93b439da9e6a31e5a985b56`.
Started UTC: 2026-10-25T10:09:24.157300+00:00.

## Identity gate (passed)

`git -C src rev-parse HEAD 'HEAD^{tree}'` rc=0:
```
0fe659e30e151f4ce3dce13789fa6622ca6c6b47
9244cf09cfffcbc6e93b439da9e6a31e5a985b56
```
`git -C src symbolic-ref -q HEAD` rc=1 (empty; detached).
`git -C src rev-parse --is-shallow-repository` rc=0: `false`.
`git -C src status --porcelain` rc=0: empty.
`git -C src log -1 --format='%H %P'` rc=0:
```
0fe659e30e151f4ce3dce13789fa6622ca6c6b47 97bb4c54b5bd925b88a5fcae03178f79c93a45f5
```

This file was written incrementally as results were measured. Source checkout was treated read-only; executable mutations used temporary copies.

## Context, scope, and size

`python3 -B review-r26d-I2xEzfHg/review.py integrity`, rc 0. Identity, expected ancestry, and exact two-file write set match. `git log --oneline 113e0d1..b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` is empty, rc 0. Local and remote-tracking refs include the named branch; an offline clone's refs do not establish GitHub push status. Local `master` does not exist (spec lookup rc 128); fallback spec read rc 0 and SHA-256 matches **f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb**. Lease read rc 0; its local-head rereview provision matches this task. GitHub authority remains unverified.

Command records and scratch scripts: `review-r26d-I2xEzfHg/`. `initial-logs/` preserves initial integrity and setup-failure results; subsequent command records are in `logs/`.

Size (informational owner item, **not a code finding**), measured with `git -C src diff --numstat <base> HEAD -- .claude/dev/launcher.py .claude/dev/launcher_test.py`, all rc 0:

| Base | launcher added/deleted | tests added/deleted | Total added/deleted |
|---|---:|---:|---:|
| e739ac1b74024a20949425c447fb6cf025317c0e (cumulative, merged portion included) | 251/4 | 785/0 | **1,036/4** |
| b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 (new delta only) | 182/68 | 458/35 | **640/103** |
| 97bb4c54b5bd925b88a5fcae03178f79c93a45f5 (round 4 only) | 12/8 | 23/3 | **35/11** |

Exactly 2 files. Cumulative additions exceed the v2 550 ceiling by **486**. Owner escalation is requester-reported, not independently verified.

## Execution setup and initial unsuccessful pass

Tests run with an explicit minimal environment, bytecode disabled, isolated empty HOME/CODEX_HOME selectors, and scratch TMPDIR; no inherited authentication variables or real credential files. Supplied tests create seed commits in disposable fixtures only; no commits in the reviewed checkout. Native mutation harness error credit is not trusted: the independent wrapper returns rc 1 only for `TinHieuChotCa` with the named target in its traceback; ordinary exceptions are rc 3, wrong-target signals rc 4, skips rc 2.

Initial targeted driver rc 1: **23/30 pass, 7 setup failures**. Initial supplied mutation driver rc 1: 55 compiled mutants, **55/65 target-origin signals**, 10 ordinary setup exceptions, no credit for those exceptions. Empty Codex home was initially beneath the workspace's `.git` marker; `_KhoCodex` rejects that ancestry before fake-child launch. Source was unchanged. The reviewer moved only the empty test-home selector to a fresh `/tmp/wp748-r26d-empty-home-*` directory outside repository ancestry, and restarted the measurements. Initial artifacts remain separately named `initial-*`; they are not silently overwritten or claimed green.

The first relocation also encountered the same setup block: this sandbox has a read-only **`/tmp/.git` marker**, so any CODEX_HOME below `/tmp` is rejected. Second pass: 23/30 targets pass and 55/65 mutation target signals; files retained as `second-*`. The final selector is the verified nonexistent absolute path `/nonexistent-wp748-r26d-fixture-codex-home`; `_dang_cho_snapshot` handles its FileNotFoundError without reading or creating credentials. Isolated HOME and all written scratch remain in writable temporary directories. A one-case preflight of the synthetic-secret fake-child test now returns rc 0 / pass. Full targeted/mutation reruns are proceeding with this setup. No credential/security guard in the reviewed code or test harness was bypassed or edited.

## Successful required executions and round-3 closure

With the corrected empty-home selector:

- `python3 -B review-r26d-I2xEzfHg/review.py targeted`: rc **0**, **30/30** cases, each exact requested `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1` (absolute paths in command ledger), each rc 0 and **1/1 qua, 0 bo qua, 0 hong**; no skips. This is 15 r925 + 15 r926.
- `python3 -B review-r26d-I2xEzfHg/review.py supplied`: rc **0**, **55/55** uniquely matched, compiled temporary launcher mutations; **65/65** executions return rc 1 / target-origin **TinHieuChotCa**. No ordinary exception or skip is counted as a kill. Exact replacements, commands, assertion messages, and tracebacks are in `mutations.json` and `logs/`.
- `python3 -B review-r26d-I2xEzfHg/review.py exec extra_mutants review-r26d-I2xEzfHg/extra_mutants.py`: rc **0**, **5/5** focused removals raise target-origin TinHieuChotCa, including **3/3** surviving extra mutants from round 2, adapted to the current object API. The other two expose the missing registered mutants below.
- `python3 -B review-r26d-I2xEzfHg/regressions.py`: rc **0**, **13/13** selected existing regression cases pass, none skipped (timeout/tree-kill 9, Windows mocks 3, persisted-log hashes 1).

**R25-EVID-05 P2 is closed for all reported counterexamples.** Actual executor-authored round-4 complete-line fixtures now produce `khong_ro=1`, no `mat`, one retained model, and **KHONG_DO_DUOC**: invalid-UTF-8/escaped-key input **329/329 bytes dropped**; truncated-JSON/escaped-key input **314/314 dropped**. This is direct existing-byte execution, not merely a parser-failure seam. `r26_doc_tron_khong_parse_bo_qua` removes only that fallback and fails at `doc tron escape_va_utf8_hong`: **DO_DUOC**, 329 dropped, no unknown counter. The dedicated target raises TinHieuChotCa at launcher_test.py:6806. Shared JSON-header requirement mutant `r26_khong_ro_khong_doi_json` is killed by the Binary/Ping control: cap=256, `khong_ro=2`, incorrectly KHONG_DO_DUOC. Head controls yield DO_DUOC at caps 256 and 4096, no loss/unknown counters.

**R26-TEST-12 P3 is closed.** `r26_ghi_bo_chot_0_byte` removes exactly the zero-progress check, matches once, compiles, and fails at the existing **tra_0** assertion (launcher_test.py:6856), not short-write setup: stored 39 allowed bytes, errors `[]`, only 4 drain bytes dropped, versus expected zero stored, OSError and 43 dropped. The independent short-write-loop mutant still fails earlier at **ngan_roi_du**, so the two behaviors are now separately represented.

`python3 -B review-r26d-I2xEzfHg/review.py exec observations_corrected review-r26d-I2xEzfHg/observations.py`: rc **0**, `OBSERVATIONS PASS`; full numeric observations are in `observations.json`. The first observation run reached and passed all preceding boundaries, then returned rc 2 because the reviewer mistakenly used `--timeout`; the scratch driver was corrected to the real `--deadline-utc` option. That driver error is not a source finding and is retained in `logs/observations.json`.

## New finding — same mutation-coverage class

**R26-TEST-13 — P3 — `.claude/dev/launcher_test.py:10772`, `:10857` (guards at `.claude/dev/launcher.py:1700`, `:1707`) — two independent classification guards lack their own supplied mutation.**

Class: `unguarded-filter-invariants`, continued from **R25-TEST-03**. The three round-2 survivors and the round-3 zero-progress omission are fixed; these are two additional manifestations of the same explicit v2 acceptance requirement, not a new demonstrated production failure.

1. **Single-read acceptance guard:** the sole supplied mutation of `if so_doan == 1 and tron` removes only `tron` (EOF completeness), retaining `so_doan == 1`. No r25/r26 entry removes only the single-read guard while keeping bounded reads and the LF requirement. Independent `extra_single_chunk_acceptance` makes only `if so_doan == 1 and tron` → `if tron`. Its existing target `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` raises **TinHieuChotCa**, rc 1, at line 6539: an oversized response is accepted as a model, with `dong_bo=10`, `byte_bo=470`, no loss. `r25_doc_khong_tran` instead removes the read-size bound, and `r26_bo_dem_mat_nhieu_doan` removes loss counting; neither independently removes this acceptance guard.
2. **Complete-line confirmed-other-event guard:** the new fallback's `loai is None` condition prevents an already parsed other event from becoming unknown. `r26_doc_tron_khong_parse_bo_qua` disables the entire fallback; it does not test losing this qualifier. `r26_bo_xac_nhan_su_kien_khac` targets the separate multi-chunk prefix path. Independent `extra_complete_other_event_guard` removes only `loai is None and` from the complete-line fallback. The existing target `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` raises **TinHieuChotCa**, rc 1, at line 6777: cap **196**, 382 dropped bytes, **khong_ro=1**, incorrectly KHONG_DO_DUOC. Head remains DO_DUOC on the same existing bytes.

Command: the `extra_mutants.py` command above, driver rc 0; both replacements match exactly once and compile; **2/2 intended target signals**. See `extra-mutations.json` for exact pairs and actual output. No new input payload was authored. The production guards and existing tests work; the missing artifacts are independent entries in `DOT_BIEN`, just as for the previous zero-progress finding. Therefore severity is **P3**, not P2.

Fix direction: add one focused `r26_*` mutation per predicate in `DOT_BIEN`, pointing to the existing effective targets, and retain the separate EOF/read-bound/multi-chunk mutants. The tests already supply the necessary controls, so no production change or new attack input is needed. Validate unique anchors, successful compilation, and the specific target assertions above. Main risk is accidentally combining two removals or earning credit for a setup exception; keep each mutation focused and verify TinHieuChotCa origin. No production patch is supplied.

## Earlier-finding status on the exact reviewed head

| Earlier finding | Status | Current measured evidence |
|---|---|---|
| R25-SEC-01 P1 | Closed for the reported arbitrary stderr-to-disk path; stays closed. | Exact-list case and fake-child sample-secret run-directory scan pass; unrestricted/prefix/continuation mutations fail. No raw stderr fallback. |
| R25-MEAS-02 P2 | Closed; stays closed. | Anchored target/receive position, event eligibility, strict UTF-8, nonblank id/model and model-aware dedup targets pass; their mutations fail. This establishes format provenance, not cryptographic server attestation. |
| R25-TEST-03 P2 | All three round-2 surviving removals are closed, **3/3 killed**; broader class has new P3 manifestations R26-TEST-13. | Generic-write-error count removal: target reports only 4 dropped instead of 33. Unlatched fail-open removal: target gets DO_DUOC. Late production latch: actual 10 s join plus close releases reader; target fails, and diagnostic confirms wrong final DO_DUOC. |
| R25-ROBUST-04 P2 | Closed; stays closed. | Both bounded-read cases pass and unbounded-read mutants fail. Production normal reads and error drain request 4 MiB. No memory-exhaustion stress result is claimed. |
| R25-EVID-05 P2 | Closed for reported incomplete-evidence mechanisms, including round-3 whole-line failure. | Prior 632-byte continuation at caps 256/330/340/350/360 always has mat=1 and KHONG_DO_DUOC. Every-cut/whitespace sweeps pass. Round-4 complete unparseable JSON fixtures now have khong_ro=1; removing the exact fallback restores false DO_DUOC and is killed. |
| R25-RACE-06 P2 | Closed; stays closed. | Latch/snapshot and late-resampling cases pass; corresponding mutants fail. Status and serialized fields use the same copied collections after liveness latching. |
| R25-CONTRACT-07 P2 | Closed under superseding v2; stays closed. | Discarding non-allow-listed diagnostics is required by v2. Non-Codex case and persisted-log semantics pass. |
| R26-ALLOW-08 P3 | Closed; stays closed. | LF stores 39 bytes, CRLF stores 40; CR-CR-LF stores 0 of 41; partial/continuation controls are rejected. rstrip mutation fails specifically at CR_CRLF. |
| R26-COUNT-09 P3 | Closed under the actual unbuffered contract; stays closed. | Native FileIO with RLIMIT_FSIZE: 43 input = 10 persisted + 33 counted discarded; OSError recorded. Error-drain count 104/104 and closed-sink count 39/39. Separate drain/closed-sink/error/short-write/count/unbuffered-open mutants fail. |
| R26-EOF-10 P3 | Closed; stays closed. | Production 10 s finish-during-close case and object ordering case pass. Object-order mutant reaches final DO_DUOC assertion; production-order diagnostic also confirms wrong final DO_DUOC. |
| R26-CLASSIFY-11 P3 | Closed for reported other-event regression; stays closed. | Same existing 382 bytes, caps 190 and 4096 both DO_DUOC, no mat/khong_ro. All-cap known-other-event controls and prefix/type-decoding mutations behave as intended. |
| R26-TEST-12 P3 | Closed. | Dedicated zero-progress removal now registered; correct target dies specifically at tra_0, independently of short-write looping. |
| Unreachable `bo_loc is None` note | Remains removed; real failure path explicitly measured. | Missing codex executable through public probe override: rc 2, receipt hong, ma_thoat null, no model/drop keys. No claim that this early-exit path now emits final model metadata. |

Both findings open in round 3 are closed (**2/2**). This does not close the broader every-guard-has-a-mutant acceptance class, because R26-TEST-13 remains open. Earlier reported production fixes remain effective on the measured inputs.

## Mutation interpretation and right-reason checks

`python3 -B review-r26d-I2xEzfHg/review.py exec order_audit review-r26d-I2xEzfHg/order_audit.py`: rc **0**, **3/3** diagnostic expectations. On head, all three original production-case assertions pass. Both `r26_san_xuat_dong_tep_truoc` and the adapted round-2 late-latch removal first fail a fixture observation: a second close overwrites the first-close state. A diagnostic wrapper records all assertions without stopping; both also fail the **final receipt** assertion with **DO_DUOC None**. This diagnostic is not ordinary mutation credit and does not modify source tests. The object-order mutant independently reaches the final receipt assertion in its ordinary target run.

Other qualifications: `r25_ghi_moi_dong_tron` first fails its model-status assertion because it bypasses parsing; its second target independently detects forbidden sample-secret bytes written to disk. `r25_bo_chot_luong` deletes the latch, rather than reversing snapshot order; its target detects the resulting incomplete snapshot. `r26_ghi_khong_lap` removes looping/count handling together with the no-progress check; its short-write failure and the new focused zero-progress companion now prove those separately. Reader-start mutations produce target assertions for uncaught start failure, unclosed pipe, missing recorded error, and joining an unstarted thread; no unrelated exception is credited. All first-assertion texts remain in `mutations.json`.

## Security and regression assessment

| Boundary | Observed behavior and limits |
|---|---|
| Exact allow-list | Only a complete first-chunk byte string in `_STDERR_CHO_PHEP_DONG` reaches `_ghi_het`; raw comparison occurs before ANSI cleanup. Existing prefix/suffix, invalid-byte, CR-only, EOF-cut and continuation fixtures are suppressed. No raw trace spool or fallback was found. A partial disk write can retain a prefix of a permitted constant, not arbitrary trace. |
| Complete physical line | Strict parsed candidate with correct header and nonblank id/model is accepted; malformed candidate metadata counts loss. A complete unparseable JSON receive header now counts unknown even without a literal candidate token. Confirmed other events remain uncounted. The missing formal mutations are R26-TEST-13; no remaining production counterexample was established here. |
| Multiple reads and cross-boundary tokens | One classification at LF/EOF; compacted 64-byte tail plus candidate latch preserves matching across reads; existing cut-position and whitespace sweeps pass. Bounded prefix is used to distinguish known other events from unknown JSON. No universal encoding or adversarial-parser certification is claimed. |
| EOF-cut | Not persisted as an allowed line or accepted as a complete model frame. Literal candidates count loss; recognized unconfirmed JSON receive headers count unknown. Binary/Ping controls remain outside JSON candidate classification. Incomplete/unsupported headers without a candidate signal are not asserted to prove a response existed. |
| Error drain / closed sink | Exceptions record class names only and drain with bounded reads, counting consumed discarded bytes. Closed-sink ValueError counts unwritten allowed bytes. Generic short-write/error accounting matches a real unbuffered FileIO probe. No trace bytes reach the write helper on these paths. |
| Completion and snapshot | DO_DUOC requires positive model evidence, no reader error, latched reader completion, no loss and no unknown evidence. `ket_thuc(10)` joins then samples liveness before closing; `ghi_so` copies collections afterward. Unlatched calls fail closed. Actual inherited-pipe and finish-during-close cases pass. No independent EOF timestamp proves a nanosecond deadline if descheduled between join return and liveness sampling. |
| Run directory / other sinks | Existing sample-secret fake-child scan passes. Independent persisted-log probe yields only `run.json`, `stdout.log`, `stderr.log`; 39 stored stderr bytes, 186 dropped, stored hash **1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721**, matching receipt. Selected response id/model are retained per spec. Unchanged stdout/prompt sinks and child-owned logs are outside a universal no-disk claim. |
| Timeout / kill | Nine selected existing timeout/tree-kill cases pass, plus required r925 Codex timeout asserting 124 and retained model. Independent actual kill followed by deliberately incomplete confirmation gives launcher=receipt **125**, giet_tron_ven=false, one retained model. It tests the 125 selector without leaving a descendant alive. |
| Windows | Three Job Object/process-tree mocks pass; code diff preserves creationflags and Job Object behavior. codex/codex.exe/codex.cmd/CODEX.CMD identification and exact CRLF bytes measured. Native Windows process launch, `.cmd` execution, handle inheritance and Windows CI are **not_run/unverified**. Linux mocks are not the Windows lane. |
| Non-Codex / hashes | Non-Codex required case and r14 hash case pass. No added model/drop keys on non-Codex runs. stderr_byte/stderr_sha256 describe persisted log bytes, not original stderr volume; independent Codex stored-byte/hash comparison matches. |
| Popen failure | Actual absent executable with public override returns rc 2; hong receipt, null ma_thoat, no model/drop fields. Existing early error behavior retained. |
| Reader-thread start failure | Production lenh_run with Thread.start forced to raise RuntimeError closes the read pipe and completes; fake Python child returns 120 on broken stderr, preserved by launcher. Receipt is KHONG_DO_DUOC with RuntimeError and 0 stored stderr bytes. Drop counts cover successful reads only, not child bytes never read. |

Full repository-wide `launcher_test.py` suite is **not_run in this round**; the measured scope is all 30 requested r925/r926 cases plus 13 relevant regressions and independent boundary probes. The previous round's full-suite report is historical, not substituted for a current full-suite pass. No authenticated live Codex run, live credential-store scan, Windows lane, GitHub authority/CI, or outer execution receipt was verified. This read-only review does not authorize merge/land. No new exploit payload was authored; probes reuse supplied fixtures and safe allowed diagnostic bytes.

## Per-case and per-mutant execution ledger

Each required case command: `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`. Every row: rc **0**, **1/1 qua, 0 bo qua, 0 hong**. Full commands and output: `review-r26d-I2xEzfHg/targeted.json`.

| Key | Case | Seconds |
|---|---|---:|
| T1 | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0.49 |
| T2 | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 0.379 |
| T3 | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0.36 |
| T4 | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0.515 |
| T5 | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0.798 |
| T6 | `r925_bo_loc_hong_xa_ong_co_gioi_han` | 0.35 |
| T7 | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0.31 |
| T8 | `r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup` | 0.369 |
| T9 | `r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai` | 0.328 |
| T10 | `r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat` | 0.347 |
| T11 | `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 0.462 |
| T12 | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 0.31 |
| T13 | `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 0.302 |
| T14 | `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 0.573 |
| T15 | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0.801 |
| T16 | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0.402 |
| T17 | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0.371 |
| T18 | `r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE` | 0.344 |
| T19 | `r926_ghi_het_dem_dung_phan_chua_ghi` | 0.323 |
| T20 | `r926_ghi_so_truoc_khi_chot_khong_DO_DUOC` | 0.298 |
| T21 | `r926_ket_thuc_chot_luong_TRUOC_khi_dong_tep` | 0.35 |
| T22 | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 0.429 |
| T23 | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 10.538 |
| T24 | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0.324 |
| T25 | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0.525 |
| T26 | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0.518 |
| T27 | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0.515 |
| T28 | `r925_codex_qua_han_van_124_va_giu_khung_da_den` | 3.438 |
| T29 | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 10.547 |
| T30 | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0.336 |

Each supplied mutation target command: `python3 -B review-r26d-I2xEzfHg/review.py one <temporary-launcher.py> <case>`. Every execution: rc **1**, target-origin **TinHieuChotCa**; see the right-reason qualifications above. All replacements match once and compile.

| Mutant | Target keys | Signals/targets |
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
| `r26_khong_ro_khong_doi_json` | T17 | 1/1 |
| `r26_doc_tron_khong_parse_bo_qua` | T17 | 1/1 |
| `r26_ghi_bo_chot_0_byte` | T19 | 1/1 |
| `r25_loc_ca_luot_khong_phai_codex` | T27 | 1/1 |

Additional regression commands use the same `--lap-ca <case> --lan 1` invocation. Each row rc **0**, **1/1 qua, 0 bo qua, 0 hong**.

| Case | Seconds |
|---|---:|
| `t27_qua_han_thi_giet_va_tra_124` | 2.346 |
| `t28_qua_han_giet_ca_CON_CHAU` | 10.361 |
| `t63_chau_phot_lo_SIGTERM_ma_bao_da_giet_ca_cay_la_noi_doi` | 5.118 |
| `t67_chau_sinh_SAU_luc_chup_van_phai_bi_dem` | 5.091 |
| `t66_chau_setsid_roi_khoi_nhom_van_phai_bi_giet` | 2.866 |
| `t79_job_windows_phai_kiem_ket_qua_dat_gioi_han` | 0.325 |
| `t80_job_pid_tang_buffer_khi_qua_suc_chua` | 0.338 |
| `t81_chup_cay_windows_thieu_creationdate_phai_fail_closed` | 0.373 |
| `r14_run_json_bam_lai_dung_hai_log` | 0.436 |
| `t158_comm_hong_SAU_luc_sinh_qua_han_khong_duoc_124_khi_con_song` | 4.394 |
| `t159_chuong_trinh_ten_tieng_Viet_qua_han_phai_giet_duoc` | 4.39 |
| `t160_giet_cay_chau_setsid_comm_hong_phot_lo_SIGTERM` | 2.787 |
| `t161_giet_cay_me_da_thoat_chau_cung_nhom_comm_hong` | 2.754 |

## Final integrity and disposition

`python3 -B review-r26d-I2xEzfHg/neutral.py`: rc **0**, **30/30** required cases also pass using the unmodified temporary launcher in the same directory and companion-module context as the mutants. Thus temporary-copy layout itself does not account for the reported kills.

`python3 -B review-r26d-I2xEzfHg/review.py exec final_integrity review-r26d-I2xEzfHg/final_integrity.py`: rc **0**. HEAD/tree/parents still match; status including untracked and ignored files is empty; working/staged diff checks, delta whitespace check, and `git fsck --connectivity-only --no-dangling` all rc **0**. Partial-clone/promisor query rc **1**, no matches. Reviewed source bytes match HEAD **2/2**. All **61/61** temporary launcher copies compile (55 supplied mutants, 5 supplemental mutants, 1 neutral copy). AST comparison verifies `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, and `KetGiet` unchanged versus base **6/6**. Runtime: Linux, Python **3.13.16**.

Source SHA-256: launcher **c9a7afbbc45763dc797a506c578d6122b7ff4e2cfae85d72db51c07f5514d7af**; tests **e1f1fb41af4d9367cad31a6ef4d16463def1cc620d2b6b6badeec8e653ecb749**. Initial/final clean checks and source-byte comparison show no observed checkout delta; they are not a forensic attestation of every intermediate operation. No source edits, source commits, pushes, GitHub comments, or credential use were performed.

Final measured scope: **30/30 required cases**, **55/55 supplied mutants**, **65/65 intended target signals**, **3/3 re-applied round-2 extra mutants**, **2/2 additional focused removals**, **13/13 regression cases**, **30/30 neutral-copy controls**. No ordinary exception is credited as a mutation kill; production-order first-assertion caveat is explicitly qualified above. Both round-3 findings are closed; reported earlier production fixes stay closed. Open: **R26-TEST-13 P3**, two missing independent mutation entries, in the continuing R25-TEST-03 class. This is an explicit acceptance-artifact defect; no new production safety failure was demonstrated.

The owner's zero-P0–P3 threshold is not met. Size is a separate owner item: **1,036 cumulative additions**, **640 new-delta additions**, **35 round-4-only additions**, two files. Full-suite/Linux, native Windows, authenticated live acceptance, current GitHub authority/CI and outer receipt limits are recorded above, not treated as passes.

Completed UTC: **2026-10-25T10:25:05.078613+00:00**.

VERDICT: changes_requested
