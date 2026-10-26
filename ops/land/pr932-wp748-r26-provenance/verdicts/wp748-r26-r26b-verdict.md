# WP748 r26 round 2 independent read-only review

Disposition: **changes requested — 0 P0, 0 P1, 2 P2, 2 P3 open**. Reviewer: OpenAI Codex, declared by runtime instructions as based on GPT-6; provider `openai_codex`. Observed execution surface: tool-mediated shell in managed Linux; transport: machine. This is not an independently attested serving-model identifier. The exact model build/effort/session ID, enclosing launcher receipt, and whether the outer surface is CLI or service cannot be independently verified from the evidence supplied here. Invocation through `launcher.py run` is requester-reported. Review class: sensitive. Started: 2026-10-25 09:06:12 UTC.

Reviewed commit: `143d43fcfe9f2a4b116afd169014ed3d6d598403`; tree: `da2d70cc9d0cd3ed104813851be3b7a4d5b19ffd`; parent: `b306e15a96a4d9d05d2ba4191cbd071fa7820ee7`.

Identity checks passed: `git -C src rev-parse HEAD HEAD^{tree} HEAD^ --is-shallow-repository` returned those three identifiers and `false` (rc 0). `git -C src symbolic-ref -q HEAD` produced no output (detached HEAD; its individual rc will be captured explicitly below). `git -C src status --short` produced no output. `git -C src branch --contains HEAD` listed detached HEAD and `agent/wp748-r26-claude`. `git -C src diff --name-only b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 143d43fcfe9f2a4b116afd169014ed3d6d598403` listed exactly `.claude/dev/launcher.py` and `.claude/dev/launcher_test.py`.

Scope: no edits to `src/`, no commits/pushes, no GitHub access/comments, no credentials. Local branch containment is verified; the assertion that the commit has never been pushed cannot be independently established offline. Authority #748 issuecomment-6394503720 cannot be read or verified because GitHub access is prohibited. Scratch and this report are the only authorized writes.

## Initial measurements

Evidence directory: `review-r26b.DC4LiT/`. Full command/rc/stdout/stderr/timing ledger: `review-r26b.DC4LiT/commands.jsonl`; per-command JSON in `logs/`. Test subprocesses use a minimal explicit environment, no inherited authentication variables, scratch HOME/TMPDIR, disabled bytecode and an absent `/nonexistent-wp748-r26b-DC4LiT` Codex home. No authenticated Codex process is invoked.

`python3 -B review-r26b.DC4LiT/review.py integrity` rc 0: detached check rc 1/no output; tracked/untracked/ignored status rc 0/empty; identity rc 0/matches; intervening history command rc 0/empty. Spec on `master` is absent (rc 128); fallback at the supplied remote-tracking ref returns rc 0 and SHA-256 `f20615ae559f377150cfd6a9cfd0bce4478bf28ae3d562a674588a9c6f9d4bdb`, matching the requested v2. Lease read rc 0. Repository reviewer guidance read; explicit requester instructions govern this offline review and zero-P0–P3 criterion. The cloud-runtime skill was read; no environment-status tool is available and no network or credential inspection/setup was used.

Size (not a code finding, as instructed): cumulative `git -C src diff --numstat e739ac1b74024a20949425c447fb6cf025317c0e HEAD -- .claude/dev/launcher.py .claude/dev/launcher_test.py` rc 0 reports `172 3 .claude/dev/launcher.py` and `488 0 .claude/dev/launcher_test.py`: **2 files, 660 added, 3 deleted**, exceeding the v2 550-addition ceiling by **110**. New delta only, `git -C src diff --numstat b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 HEAD`, rc 0: `67 31` and `144 18` respectively: **2 files, 211 added, 49 deleted**. The cumulative number is scoped to the packet's two files; intervening unrelated master changes are excluded. The executor's owner escalation is requester-reported, not independently verified.

## Incremental test results and reproduced remaining defect

Required targeted cases: **21/21 pass** (15 `r925_*`, 6 `r926_*`), each exact `python3 src/.claude/dev/launcher_test.py --lap-ca <full-name> --lan 1`, rc 0, `1/1 qua, 0 bo qua, 0 hong`. All **33/33 supplied mutants** compile with each replacement matching exactly once; **40/40 target executions** raise `TinHieuChotCa` in the named target (rc 1, target present in traceback), with no setup-error or skipped kills. Exact targets, assertion messages and tracebacks are in `mutations.json` and `commands.jsonl`. Mutation correctness beyond an exception type is assessed below.

`python3 -B review-r26b.DC4LiT/review.py exec observations observations.py` (measurement child rc 0) reuses the round-1 continuation fixture: one accepted `_r25_khung("response.created", "rk", "mk")`, followed by the existing `b"x" * 256 + khung` fixture. All **632 bytes** are suppressed. Caps **256/330/360**: `mat=1`, `KHONG_DO_DUOC`; caps **340/350**: `{'dong_bo': 3, 'byte_bo': 632}`, no errors, one model, **`DO_DUOC`**. Thus **R25-EVID-05 P2 remains OPEN**: the new header test only recognizes a header at the physical line's beginning; the exact previously reported continuation/candidate-token alignment hole remains. No new attack content was authored; only the supplied harmless frame and existing prefix are reused at finite test caps. Production cap is 4 MiB; this is a branch/alignment measurement, not a live 4 MiB reproduction.

Allow-list endings: LF persists 39 bytes, CRLF 40; CR CR LF persists 0/drops 41; CR-only and no terminator persist 0. Existing failing-sink fixture now consumes/counts all **264/264 bytes**, records `RuntimeError`, and yields `KHONG_DO_DUOC`; closed sink counts all **264/264 bytes**, including the allowed but unwritten lines. Stored-log probe: launcher rc 0, `stderr_byte=39`, actual file 39 bytes, `stderr_sha256` matches. Only `run.json`, `stderr.log`, `stdout.log` appear in that run directory. Full security boundaries and the retained closed-sink liveness qualification follow below.

## Earlier-finding disposition on the reviewed SHA

| Earlier finding | Status | Independent evidence |
|---|---|---|
| R25-SEC-01 P1 | Closed for the earlier arbitrary-stderr disk write. | Exact allow-list/secret-directory tests pass; unrestricted/prefix/partial-line supplied mutants fail their targets. ANSI cleanup occurs after the disk allow-list comparison. No raw fallback is present. |
| R25-MEAS-02 P2 | Closed for the earlier provenance defect. | Exact target/receive position/event/UTF-8/nonempty identity checks pass; corresponding mutants fail. This proves format acceptance, not cryptographic server identity. |
| R25-TEST-03 P2 | **Partially fixed; OPEN (VÁ HỜ).** | UTF-8 now has its own effective mutant; actual `lenh_run` loss integration case passes and kills its mutant. However three independent guard removals survive **21/21 each, 63/63 total**. Details below. |
| R25-ROBUST-04 P2 | Closed for unbounded reads. | Both normal/error-drain read-limit cases pass and both supplied unbounded-read mutants fail. Production bound remains 4 MiB per read. |
| R25-EVID-05 P2 | **Partially fixed; OPEN (VÁ HỜ).** | The new header-at-start test/mutant passes/kills, but the round-1 continuation fixture still yields `DO_DUOC` at caps 340/350. See measured output above and finding below. |
| R25-RACE-06 P2 | Closed for inconsistent snapshot/status. | The liveness value is latched in `cho` before `ghi_so`; copied models/errors/counters feed both status and receipt. Existing ordering case passes. The renamed implementation makes reordering the later local read of the already-latched flag immaterial. |
| R25-CONTRACT-07 P2 | Closed under v2. | Arbitrary diagnostics are intentionally dropped; only exact allowed complete wire forms persist. Non-Codex case remains unchanged. |
| R26-ALLOW-08 P3 | **Closed (ĐÃ VÁ THẬT).** | LF/CRLF accepted, repeated CR rejected; `r26_cho_phep_cat_moi_CRLF` raises target `TinHieuChotCa` at the CR_CRLF assertion. |
| R26-COUNT-09 P3 | **Partially fixed; OPEN (VÁ HỜ).** | Error-drain and closed-file omissions are fixed and their mutants fail. A partially successful write still reports all attempted bytes as dropped: 39 input, 10 stored, 39 reported dropped (actual unpersisted 29). The earlier requested uncertainty handling is absent. |
| R26-EOF-10 P3 | **Closed for finish-during-close (ĐÃ VÁ THẬT).** | Actual 10 s join plus real waiting reader, released during `stderr.log.close()`: head rc 0, 10.0513 s, reader alive at close, finishes during close, receipt `KHONG_DO_DUOC`. The late-sampling supplied mutant is killed by r926. A separate production-call-order mutant recreates `DO_DUOC` in the same scheduling seam, confirming that seam exercises the intended protection. |

## Open findings

**R25-EVID-05 — P2 — `.claude/dev/launcher.py:1679` — `discarded-evidence-reported-complete` (continued).**

The new `_RE_DAU_NHAN` fallback only handles an incomplete chunk beginning at the physical line's start with a whole matching header. It does not fix candidate tokens split across continuation chunks of the already-supplied prefixed-line fixture. At caps 340/350 the report records 632 discarded bytes, one accepted model, no errors, no `mat`, and `DO_DUOC`; caps 330/360 see the same rejected candidate and correctly downgrade. Command: `python3 -B review-r26b.DC4LiT/review.py exec observations observations.py`, child rc 0, exact JSON in `logs/observations.json`. This is the same defect class and existing fixture as round 1, with no new exploit content.

Fix direction: retain bounded lexical/candidate state across reads, independently of the stricter whole-line provenance check used for accepting a model. Include the original continuation fixture and an alignment sweep with a positive frame before loss. Give the cross-boundary guard its own mutant and verify actual final receipt status. Escaped keys/values, partially present headers/type tokens and ANSI sequences across boundaries still need executor-authored coverage; this review does not introduce new payloads for those directions.

**R25-TEST-03 — P2 — `.claude/dev/launcher_test.py:6700`, `:6631`, `:10550`; `.claude/dev/launcher.py:1672`, `:1722`, `:1944` — `unguarded-filter-invariants` (continued).**

All supplied mutations die, but v2's independent-guard requirement is still unmet. `python3 -B review-r26b.DC4LiT/extra_mutants.py` rc 0 applies three unique, compiling replacements to temporary launcher copies only; each survives all 21 required cases (each case rc 0/PASS):

- `extra_write_error_no_count`: removes only `_dem_bo(dem, dong)` from the generic write-exception branch, retaining the re-raise. The existing failing-sink case does not assert its count, and the new counter case only covers read failure and closed-file `ValueError`.
- `extra_no_wait_failopen`: changes only the uninitialized liveness fallback (`self.con_doc is None`) from True to False. No case calls `ghi_so` with positive evidence before any wait and checks that it remains incomplete.
- `extra_production_late_wait`: keeps a real bounded 10 s join but moves production's latch to after file close (`cho(0)`). The new r926 boundary case calls the object directly and never exercises this `lenh_run` ordering. All 21 tests pass, yet `boundaries.py`'s finish-during-close seam gives `DO_DUOC` on this mutant and `KHONG_DO_DUOC` on head, each after an actual 10 s join.

Evidence: `extra-mutations.json` (**3/3 survive; 63/63 case passes**) and `logs/boundaries.json` (child rc 0). Fix direction: add separate supplied mutants/target assertions for generic write-failure accounting and uninitialized liveness; add a production-path finish-during-close test that reads final `run.json`. Preserve separate exception-type/target-origin checking. No implementation patch is proposed in the reviewed tree.

Mutation audit caveat: `r25_chup_truoc_chot_luong` now deletes the latch; it no longer reverses snapshot order, and its target turns red partly because the default liveness is incomplete. `r26_dau_nhan_moi_doan` removes **both** `dau_dong` and `not tron`; its first failing assertion is the mid-line-header control. Thus one textual replacement is not automatically a single independent guard test. The eight supplied `r26_*` target failures otherwise correspond to the named changed behavior, not unrelated setup errors. The broad `r25_ghi_moi_dong_tron` first target fails because model parsing is bypassed; its second target independently fails on actual forbidden disk output.

**R26-COUNT-09 — P3 — `.claude/dev/launcher.py:1671` — `discard-accounting-omissions` (continued, partial-write remainder).**

The new exception accounting assumes that a failed `write` persisted zero bytes. A write can persist a prefix before raising, so the ledger advertises a false exact dropped-byte count. `python3 -B review-r26b.DC4LiT/review.py exec accounting accounting.py`, child rc 0, uses only the existing 39-byte allowed diagnostic and a real scratch file. Its sink writes/flushed the first 10 bytes and then raises `OSError`; real output: `bytes_in=39`, `persisted=10`, `actual_unpersisted=29`, `reported_drop={'dong_bo':1,'byte_bo':39}`, `errors=['OSError']`, `persisted_plus_reported_drop=49`. This is controlled partial-I/O scheduling, not a new exploit payload or a claimed live disk-full event. Error status still prevents successful model certification; no secret is exposed.

Fix direction: account from read totals and confirmed persisted totals after synchronization, or explicitly mark the discard quantity unknown/partial when write success is unknowable. Do not label attempted writes as exact discarded bytes. Add partial-write/error assertions and a dedicated mutation; retain the now-correct drain and closed-sink behavior.

**R26-CLASSIFY-11 — P3 — `.claude/dev/launcher.py:1679` — `noncandidate-reported-as-lost-model-frame` (NEW).**

The new header heuristic classifies any oversized received message as a lost created/completed frame, including a chunk that already visibly identifies a different event. Reusing only existing `_r25_khung` fixtures, an accepted 186-byte `response.created` frame followed by the existing 196-byte `response.output_text.delta` frame at cap 190 yields `mat=1`, `KHONG_DO_DUOC`, reason `1 doan giong khung response.created/completed khong doc duoc; danh sach thieu`. The same bytes at cap 4096 yield `DO_DUOC`; the base launcher at cap 190 also yields `DO_DUOC` with no loss. Commands: `.../review.py exec boundaries boundaries.py` and `.../review.py exec base_compare base_compare.py`, child rc 0. All 382 bytes are dropped in either version; the accepted model list is identical. This is a conservative false negative of measurement availability and an inaccurate specific loss reason, not an unsafe positive certification. Production equivalent is a non-model received record crossing 4 MiB; no such large/live run is claimed.

Fix direction: distinguish confirmed noncandidate event types from ambiguous truncated headers using bounded state. If ambiguity is deliberately treated as incomplete, report uncertainty rather than asserting a lost created/completed frame. Extend the existing other-event control to the oversized case; the current r926 control raises its cap to 4096 and therefore misses this regression. Give the narrower classification guard its own mutant.

## Required test and mutation ledger

Each case below ran `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`; all return `1/1 qua, 0 bo qua, 0 hong`.

| Key | Case | rc | Seconds |
|---|---|---:|---:|
| T1 | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | 0.623 |
| T2 | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 0 | 0.554 |
| T3 | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | 0.557 |
| T4 | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0 | 0.709 |
| T5 | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0 | 0.366 |
| T6 | `r925_bo_loc_hong_xa_ong_co_gioi_han` | 0 | 0.344 |
| T7 | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | 0.351 |
| T8 | `r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup` | 0 | 0.365 |
| T9 | `r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai` | 0 | 0.434 |
| T10 | `r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat` | 0 | 0.347 |
| T11 | `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 0 | 0.327 |
| T12 | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 0 | 0.295 |
| T13 | `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 0 | 0.307 |
| T14 | `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 0 | 0.428 |
| T15 | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | 0.337 |
| T16 | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0 | 0.486 |
| T17 | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0 | 0.502 |
| T18 | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0 | 0.427 |
| T19 | `r925_codex_qua_han_van_124_va_giu_khung_da_den` | 0 | 3.343 |
| T20 | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 0 | 10.617 |
| T21 | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0 | 0.287 |

`python3 -B review-r26b.DC4LiT/review.py supplied`, driver rc 0. Each target executes `python3 -B <scratch>/review.py one <temporary-launcher> <case>`. The wrapper returns rc 1 **only** for a `TinHieuChotCa` whose traceback includes the target case; ordinary errors are rc 3, wrong-target signals rc 4, skips rc 2. **33/33 mutants killed, 40/40 target executions rc 1**, no exceptions miscredited. Both companion Python files are unchanged copies.

| Mutant | Target cases | Killed/targets |
|---|---|---:|
| `r25_ghi_moi_dong_tron` | T1, T2 | 2/2 |
| `r25_cho_phep_theo_tien_to` | T2 | 1/1 |
| `r25_cho_phep_ca_dong_cut` | T12 | 1/1 |
| `r25_bo_go_ansi` | T3 | 1/1 |
| `r25_khung_moi_target` | T3 | 1/1 |
| `r25_moi_su_kien` | T3 | 1/1 |
| `r25_nhan_id_model_rong` | T3 | 1/1 |
| `r25_gop_theo_id` | T3 | 1/1 |
| `r25_bo_dem_mat` | T3, T5, T4 | 3/3 |
| `r25_parse_khong_can_ca_dong` | T5 | 1/1 |
| `r25_doc_khong_tran` | T4 | 1/1 |
| `r25_xa_ong_khong_tran` | T6 | 1/1 |
| `r25_noi_rust_log_thua_ke` | T16 | 1/1 |
| `r25_khong_bat_trace` | T1 | 1/1 |
| `r25_DO_DUOC_khi_loc_hong` | T15, T7 | 2/2 |
| `r25_DO_DUOC_khi_ong_con_mo` | T15, T20 | 2/2 |
| `r25_DO_DUOC_khi_mat` | T15, T7 | 2/2 |
| `r25_DO_DUOC_khong_khung` | T15, T17 | 2/2 |
| `r25_so_khong_chuyen_loi` | T7 | 1/1 |
| `r25_so_khong_chuyen_mat` | T7 | 1/1 |
| `r25_chup_truoc_chot_luong` | T8 | 1/1 |
| `r25_doc_ong_khong_han` | T20 | 1/1 |
| `r25_bo_loc_hong_khong_xa_ong` | T21 | 1/1 |
| `r25_bo_loc_hong_khong_ghi_loi` | T21 | 1/1 |
| `r25_loc_ca_luot_khong_phai_codex` | T18 | 1/1 |
| `r26_lay_mau_lai_luong_muon` | T9 | 1/1 |
| `r26_bo_dau_nhan_cat_doan` | T10 | 1/1 |
| `r26_dau_nhan_moi_doan` | T10 | 1/1 |
| `r26_utf8_thay_the` | T11 | 1/1 |
| `r26_cho_phep_cat_moi_CRLF` | T12 | 1/1 |
| `r26_xa_khong_dem` | T13 | 1/1 |
| `r26_tep_dong_khong_dem` | T13 | 1/1 |
| `r26_so_bo_qua_mat_dau_cuoi` | T14 | 1/1 |

## Security and regression boundaries

| Boundary | Result and scope |
|---|---|
| Raw stderr reaching disk | No arbitrary-byte path was demonstrated through the filter. From the first byte, only complete physical lines exactly equal to the two enumerated allowed LF/CRLF forms reach `write`. Prefix/suffix, invalid UTF-8, repeated CR and partial-line variants are rejected. The sample-secret run-directory scan passes. Partial writes can leave a prefix of the allowed constant and distort drop accounting (R26-COUNT-09), not expose raw trace. |
| Continuation and oversized lines | Continuations are not accepted as whole frames or allowed diagnostics. Every normal/drain read remains bounded to `_TRAN_DONG`. Drop-line counts mean read chunks, explicitly documented, not necessarily physical lines. Candidate state is still chunk-local: R25-EVID-05. Header-at-start fallback now over-classifies known other events: R26-CLASSIFY-11. |
| CR / CRLF | Existing frame with CR-only termination: 186 dropped bytes, no model, `mat=1`, `KHONG_DO_DUOC`. CRLF: 187 dropped bytes, one model, `DO_DUOC`. Exact allowed LF/CRLF comparison is independent of later ANSI cleanup. |
| Reader/error handling | Exception class names, not exception messages/raw lines, enter filter evidence. Error draining does not write to disk and now counts read/discarded chunks. Recorded errors prevent `DO_DUOC`. A closed sink counts its rejected safe line and continues parsing in memory; the production timeout latch prevents that late work from certifying timely completion. |
| Positive evidence and snapshots | No models, recorded filter error, latched active reader, or recognized loss each prevents `DO_DUOC`. Both status and serialized list/counters use copies after liveness latch. When the thread remains active, cross-field copies can reflect slightly different instants, but the latched incomplete status prevents positive completeness certification. No exact final total is claimed for an unfinished stream. |
| Join deadline | Production still calls a 10 s join. Real descendant-held-pipe case completes in 10.617 s and reports incomplete; removing the bound takes 40.523 s and is killed by its timeout assertion. Finish-during-close now fails closed, as measured above. Liveness is sampled immediately after `join`; there is no separate reader EOF timestamp proving a strict nanosecond-level deadline under descheduling between those two operations. |
| Run directory | Real fake-child hash probe has only `run.json`, `stdout.log`, `stderr.log`. `_ghi_so` receives selected model/id/event metadata, statuses and counters, not raw trace. Atomic receipt temporary files do not spool the trace. The supplied secret scan covers all retained files in its run. Model/id remain arbitrary nonblank strings by contract; this is not cryptographic provenance. |
| Other output channels | stdout and prompt snapshots remain existing direct output/input sinks. No authenticated Codex process or child-owned log-store inspection was performed; no universal all-process no-disk guarantee is asserted. New attack payloads for alternate field encodings/framing were not authored. |
| Timeout/kill | Dedicated regression cases t27/t28/t63/t66/t67/t158–t161 all pass. r925 timeout confirms 124 and retained pre-timeout model. `timeout125.py` child rc 0 runs a real successful kill then deliberately reports incomplete confirmation: launcher and ledger 125, `giet_tron_ven=false`, one model retained. This tests the 125 decision, not a genuinely surviving descendant. |
| Windows | Existing `creationflags=CREATE_NEW_PROCESS_GROUP`, Job Object attachment/kill paths and command construction are unchanged in the exact delta. Mocked t79/t80/t81 pass. `codex`, `codex.exe`, `codex.cmd`, `CODEX.CMD` classify true, Python false. CRLF bytes are measured above. Native Windows creationflags/Job Object/`.cmd` execution/handle inheritance and a Windows CI lane were **not run or verified**. |
| Non-Codex and log hashes | Dedicated non-Codex test and r14 hash case pass; non-Codex new fields remain absent, stderr persists normally. Codex hash probe independently shows file size 39, matching `stderr_byte`, and matching SHA-256. These fields measure persisted file bytes, not original pipe volume. |
| New `bo_loc is None` branch | **Unreachable on an ordinary Popen failure.** `lenh_run` catches/records/re-raises at :1878–1885 before reaching :1947–1950. With public `--bo-qua-probe` and a reason, an absent executable named `codex` returns rc 2, receipt `trang_thai=hong`, `ma_thoat=null`, all model/drop fields absent. Without override it is rejected earlier at the spawn probe (rc 15). The same Popen scenario on base gives rc 2/`hong`/absent model status: **no new behavior regression**, but the new branch does not supply the advertised failed-start metadata and is not covered by a reachable-path mutant. If such metadata is intended, it must be recorded before raising in the actual exception path. It never produces `DO_DUOC`. |

Additional regression driver: `python3 -B review-r26b.DC4LiT/review.py regression`, rc 0, **13/13 cases pass**, no skips: the nine timeout/tree-kill cases named above, three Windows mocks and r14. `.../review.py exec boundaries boundaries.py`, `.../review.py exec timeout125 timeout125.py`, `.../review.py exec accounting accounting.py`, `.../review.py exec base_compare base_compare.py` each measurement child rc 0; individual simulated launcher statuses are reported separately, not confused with driver rc.

Full Linux suite used a disposable **full clone** of the exact reviewed commit, with unchanged launcher/test bytes, so hook/setup tests cannot write into `src/`: `python3 review-r26b.DC4LiT/fullsrc/.claude/dev/launcher_test.py --nhat-ky review-r26b.DC4LiT/full-journal.jsonl`, **rc 1**, **256/270 executed passed**, **280 total**, **14 failed**, **10 skipped**, **289.858 s**. Journal ends `XONG TRON VEN`. Two skips require Windows; eight cannot construct the venv/pip fixture. Failures involve absent CLI capability, two read-only `/var/tmp` paths, and eleven fixture-home/materializer/ancestor checks. This is **not** an N/N full-suite acceptance result. The suite's doctor makes unauthenticated capability probes and reports unavailable GitHub/MCP capability; no authority, PR or CI content was read or verified. No real credentials were inherited or used.

Ruff on both files, `python3 -m ruff check --isolated --no-cache --select F <launcher.py> <launcher_test.py>`, returns rc 1 on head and base, the same **five F841 findings**, delta **0**. This is a lint-delta result, not an absolute lint pass. Logs: `logs/ruff_head.json`, `logs/ruff_base.json`.

## Final verification and disposition

`python3 -B review-r26b.DC4LiT/baseline_failures.py`, rc 0: **14/14 full-suite failing cases also fail with the exact base launcher**, using the unchanged head harness/fixtures in the disposable full clone. Three case processes return rc 1 (`TinHieuChotCa`); eleven return rc 3 (ordinary assertion/OSError, deliberately not mutation-kill credit). Evidence: `baseline-failures.json`, per-case logs and `commands.jsonl`. The journal has **280 starts/280 exits**. No full baseline-suite green claim is made.

`python3 -B review-r26b.DC4LiT/final_integrity.py`, rc 0: final HEAD/tree still match the required identities; tracked/untracked/ignored status is empty. `git diff --quiet`, `git diff --cached --quiet`, `git diff --check b306e15a96a4d9d05d2ba4191cbd071fa7820ee7 HEAD`, and `git fsck --connectivity-only --no-dangling` each return rc 0. Partial-clone/promisor config query returns rc 1/no matches. Both reviewed source files match their `git show HEAD:<path>` bytes (**2/2**), as do the full-suite scratch copies (**2/2**). Both copied mutation companions match; all **36/36** supplied/supplementary mutant files compile. AST equality against base confirms `_giet_cay`, `_job_windows`, `_pid_trong_job`, `_la_codex`, `_ghi_so`, and `KetGiet` unchanged. Environment: Linux, Python **3.13.16**, Ruff **0.15.15**.

Source SHA-256: launcher `9a1bf4b4fbd7039d79b16c7c305b41886d0c7336f98aab336c38901aff46cfaa`; test `b90b421b03fa777f15283c716cdc7486c8c2db3bce1cef309b9abdeb491d4f15`. Evidence: `integrity.json`. Clean initial/final snapshots and byte comparisons establish no observed source delta, not a forensic attestation of every intermediate operation. No source edits, source commits, pushes or GitHub comments were made. Tests create seed repositories/commits only within disposable fixtures. No real credentials or authenticated Codex runs were used. Scratch probes reused existing harmless frames/allowed bytes, controlled I/O/scheduling, and source guard removals; no new exploit payloads were authored.

Open findings: **R25-EVID-05 P2**, **R25-TEST-03 P2**, **R26-COUNT-09 P3**, **R26-CLASSIFY-11 P3**. Of the five previously open classes, two are closed (allow-list normalization and finish-during-close), three remain partially fixed; closure ratio **2/5** for this transition, with one new class. No P0/P1 finding is established. The requested zero-P0–P3 criterion is not met. Size remains a separate owner item: **660 cumulative added lines**, **211 new-delta additions**, two files. Windows lane, authenticated live Codex/no-secret acceptance, live authority/CI and the outer execution receipt remain unverified; the report does not confer approval or land authority.

Completed UTC: **2026-10-25 09:19:39 UTC**.

VERDICT: changes_requested
