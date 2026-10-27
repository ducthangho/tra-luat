# WP748 r27 — independent read-only review, round 2

**Changes requested: 2 P2 findings remain open; 0 P0, 0 P1, 0 P3. All 47 required cases and all 167 named-target mutation executions pass.**

Started UTC: 2026-10-26T04:27:41.696138+00:00.

Reviewer: OpenAI Codex. Runtime instructions identify Codex based on GPT-6; Linux/bash tool execution is available. Exact serving model, reasoning effort, outer `launcher.py run` invocation and completed execution receipt are not exposed for independent verification. User reports this is Codex call 2 of 10. No additional model calls or subagents are used. Review class: `sensitive`.

Reviewed SHA: `cfeafe418784480e9800f95a5e0bebff69bb5ae9`; tree: `320857c8d2ed45169e1c39dc1dcf9c7f26f9f94d`.

Identity preflight: PASS. Full non-shallow clone, detached HEAD, clean worktree; expected two parents and round-1 fix ancestry verified. Local branch points to the requested SHA. Cached origin refs also point there; local refs cannot establish live remote publication state or merge motivation. No GitHub/network/credential access is authorized or used.

Frozen spec SHA-256: `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd`. Original lease/spec size cap is 600; the user supplies the newer owner cap of 2 files / 800 added lines (`#748 issuecomment-6408141574`). GitHub cannot be read here, so that authorization and live call/lease/CI state cannot be independently verified.

Evidence directory: `review-r27b.hrx6pfr4/`; exact preflight commands, output and rc: `preflight.json`.

Commands:

- `git -C src rev-parse --is-shallow-repository HEAD HEAD^{tree} HEAD^1 HEAD^2 c92cbd2^ agent/wp748-r27-claude`: rc 0.
- `git -C src symbolic-ref -q HEAD`: rc 1.
- `git -C src status --porcelain=v1 --untracked-files=all --ignored`: rc 0.
- `git -C src diff --exit-code c92cbd20e48445cb2ba174f5992252fe8a9675fa HEAD -- .claude/dev/launcher.py .claude/dev/launcher_test.py`: rc 0.
- `git -C src merge-base --is-ancestor 21fe565633b0fba269f6ab4e2c9df5b70d98ddb2 HEAD`: rc 0.
- `git -C src show origin/ops/wp748-r27-g27-lease:ops/specs/wp748-r27-launcher-effort-sandbox.md`: rc 0.
- `git -C src diff --numstat 21fe565633b0fba269f6ab4e2c9df5b70d98ddb2 HEAD`: rc 0.

Preflight confirms the parent-1-to-merge launcher/test diff is empty and master `21fe565` is an ancestor. The completed master-side interaction review and measurements follow below.


## Round-1 closure and class sweep

Round-1 source: `VERDICT_R27A.md`, SHA `838d7e7581b443a84e7421689aa30bcc2bf2b319`. The round-1 fix `c92cbd20e48445cb2ba174f5992252fe8a9675fa` was read; all results below are re-measured on the requested merge SHA. **Three findings closed; two not closed. Two open P2 classes, zero open P0/P1/P3.** The newly identified manifestations retain their original class/ID history.

| Round-1 ID / class | Closure | Executed measurement and same-class sweep |
|---|---|---|
| R27-ALLOW-01 / `sandbox-output-not-closed` (formerly P1) | **Closed** | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` and the production `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json`: rc 0. `probes.py` additionally passes the existing `_R27_BWRAP` and `_R27_CLS` secret-bearing fixtures through the actual summarizer and `ghi_so`: two summaries, zero strings outside the fixed vocabulary, no supplied secret markers; rc 0. Path labels, bind destinations, both CLS cwd flags, profile type/filesystem/access/network/special-kind values, cap-drop, program names and retained flag names were checked. They now select fixed constants/enums. Effort's nonempty server string rule is separately required by §3.1 and is not an argv allow-list escape. Exceptions persist class names rather than raw messages. The receipt probe is a writer-level measurement; the existing production test uses a simpler process fixture. |
| R27-PARSE-02 / `sandbox-argv-boundary` (P2) | **Not closed** | `r927_ngu_phap_sandbox_theo_bang_so_doi_so`: rc 0; its declared arity/unknown-option/missing-boundary mutants all produce named-target signals. The original direct-list parsing scenarios are repaired. However, the common `/proc` adapter feeding **both** arity tables still deletes empty argv elements. A benign, non-sandbox Python child has five arguments including one empty argument; `_quet` passes four arguments and zero empties to the summarizer, with no sampler error (`probes.py`, rc 0). See R27-PARSE-02b. |
| R27-PROC-03 / `sandbox-sampling-errors-hidden` (formerly P2) | **Closed** | The unchanged `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot`: rc 0, and its cmdline-error mutant is killed by its named target. Its denied cmdline read yields `PermissionError` and `KHONG_DO_DUOC`. The second read path, `_stat`, was independently measured: `PermissionError` and generic `OSError` propagate, are latched by `_chay`, and override a prior valid observation to `KHONG_DO_DUOC`; `FileNotFoundError` and `ProcessLookupError` alone return disappearance, without an error. Probe rc 0. Directory traversal/general thread errors reach the same outer latch. `_dem_lenh_stdout` converts read failure to unknown, not command absence. Failure to read an unrelated process's stat now conservatively prevents successful measurement rather than silently inventing a complete scan. |
| R27-PID-04 / `sandbox-process-identity-race` (P2) | **Not closed** | The unchanged identity target passes and the child-reread/root-pin mutants produce named-target signals. Instrumenting **that same checked-in fixture**, without changing its argv or identity fault, shows child identity change → `DanhTinhDoi`/`KHONG_DO_DUOC`; root change between scans → `RuntimeError`/`KHONG_DO_DUOC`. But its first root-change scan reads starttimes `110819`, then `1`, and still yields no errors and `DO_DUOC`; only its second scan fails. The instrumentation logs existing stat reads, without inserting another stat read. Root and intermediate-ancestor identity checks within a scan remain incomplete. See R27-PID-04b. |
| R27-TEST-05 / `sandbox-status-tests-native-platform-dependence` (formerly P2) | **Closed** | The named `r927_trang_thai_sandbox_moi_nhanh` passes on Linux and, unchanged, under both `platform.system() == Windows` and `Darwin` mocks; probe rc 0. Real constructor/start/stop/receipt calls under those mocks return no sampler thread and `KHONG_DO_DUOC`. The status fixture now explicitly supplies Linux capability. Other new `/proc` cases return a reasoned non-Linux skip; the production test has an explicit non-Linux expectation. These are Linux-hosted simulations, not native Windows/macOS CI evidence. |

Probe command: `python3 -B review-r27b.hrx6pfr4/probes.py` in the same credential-free child environment as the matrix: **rc 0**. Exact invocation and duration are in `probe-command.json`; results are in `probes.json` and `probes.log`. Earlier executions while adding benign probes also returned rc 0; the retained log contains the final complete set. No new sandbox exploit argv, secret payload, or real PID-reuse exploit was authored. The identity fault and secret-bearing argv are reused unchanged from the reviewed test file; the added transport probe only runs an ordinary Python child with an empty argument.

## Open findings on this SHA

### R27-PARSE-02b — P2 — empty argv values are removed before arity parsing

Class/history: `sandbox-argv-boundary`, continuation of R27-PARSE-02, not a new independent class.

Location: `.claude/dev/launcher.py:2061`; downstream `.claude/dev/launcher.py:1924` (`_doc_tuy_chon`).

Scenario: `/proc/<pid>/cmdline` encodes argument boundaries with NUL bytes, including empty argument values. The comprehension's `if x` removes **all** empty elements, not just the final terminator. This alters argument positions before `_BWRAP_ARITY` or `_CLS_ARITY` sees them. For a normal bwrap invocation with an empty `--setenv` value followed by an isolation switch, the adapter deletes the value and the parser consumes that switch as the environment value. It can then successfully parse the rest, omit the applied switch, and leave `khong_ro` unset. Thus `DO_DUOC` can accompany an incorrect summary despite the arity-table fix. Other value-bearing options and both parsers share the adapter.

Measurement: the benign empty-argument round trip records `actual_argc=5`, `actual_empty_arguments=1`, `parser_argc=4`, `parser_empty_arguments=0`, `sampler_errors=[]` (probe rc 0). The bwrap consequence is a static control-flow deduction, described in words; no new sandbox argv payload was executed. The named grammar case passes because it directly calls `_tom_tat_sandbox` with an already-formed list, bypassing this adapter.

Fix direction: correct the cmdline decoder in `_quet`, preserving internal empty arguments and handling only the terminal separator specially. Treat unusable/truncated representations conservatively. Add an integration regression from raw cmdline bytes through the real decoder, both parser families, and receipt status; the regression must fail when empty arguments are filtered again. Keep the existing option-value/delimiter tests. Risk to guard against: retaining a phantom final argument, reinterpreting an empty value as a command boundary, or falsely marking normal command arguments as sandbox flags. This requires repairing the shared input boundary, not adding another arity entry.

### R27-PID-04b — P2 — root and ancestor identity are not validated for the entire scan

Class/history: `sandbox-process-identity-race`, continuation of R27-PID-04. The direct child reread and between-scan root check are real improvements; they do not close the full class.

Location: `.claude/dev/launcher.py:2037` (unchecked root identity in graph construction), `.claude/dev/launcher.py:2044` (enqueue before validation), and `.claude/dev/launcher.py:2054` (checks only the child's immediate tuple).

Scenario: `_quet` pins/checks the root once, then enumerates `/proc` and builds edges keyed by numeric parent PID. The root's stat is read again during enumeration but its new starttime is not compared with the pin. If the root changes identity between those reads, the scan can traverse descendants of the replacement root; each replacement descendant can pass its own `(ppid, starttime)` check. A scan ending at this point reports success, since detection is deferred until the next `_quet`, which may never run. An intermediate parent can likewise change after its validation while a later child still has the same numeric ppid. Further, `hang.append(c)` occurs before validating `c`; disappeared/changed parents do not prune their queued subtree. Those ancestry issues can read or attribute argv outside the originally launched process tree.

Measurement: instrumenting the **existing** identity test records these root-change snapshots:

| Scan | Root stat values read by the original scan | Errors | Receipt status |
|---|---|---|---|
| First | `110819`, `1` | `[]` | `DO_DUOC` |
| Second | `1` | `["RuntimeError"]` | `KHONG_DO_DUOC` |

The first scan is sufficient to expose the remaining false-success window; the checked-in test calls `_chay` a second time before asserting, hiding it. This is deterministic fixture instrumentation, not evidence of actual kernel PID reuse. Intermediate-ancestor/subtree consequences above are static analysis, not newly executed exploits.

Fix direction: in `_quet`, carry identity-qualified ancestry rather than only numeric edges, revalidate the root and relevant ancestor chain across graph/argv collection, and reject a scan whose scope changed. Do not enqueue/traverse a subtree before its parent is validated. Tie the initial root identity to the launched process as early as the allowed mechanism permits; unavailable identity must mean uncertainty. Add a single-scan assertion to the existing root fixture, an ancestor-invalidated-before-child case, and target mutations that bypass those checks. Guard against unbounded retries/cycles, treating ordinary exits as successful observations, and losing fork-before-exec re-observation. Merely adding one final root check would prevent some false receipts but would not by itself protect descendant read scope throughout traversal.

No separate new P0/P1/P2/P3 class was found in the remaining delta. These are newly identified manifestations of the two still-open round-1 classes, not duplicate counts of the already-repaired direct parser and direct-child scenarios.

## Full-delta review, merge isolation, and limits

The complete launcher delta against master `21fe565633b0fba269f6ab4e2c9df5b70d98ddb2`, all 380 added test lines, and the round-1 fix were reviewed. Effort comes from accepted server frames; missing/invalid reasoning is counted before model deduplication; aggregate values retain first-seen order; model measurement failure dominates effort success. No config/CLI fallback was introduced. The implementation transfers each parsed effort into immutable aggregate counters before retaining the existing model entries. Existing stderr allow-list/regex/stream-close behavior remains covered by the re-measured r925/r926 cases and mutants.

Sandbox sampling uses a 0.2-second wait, only stat/cmdline reads in production, bounded join with a latched still-running state, and sanitized summaries. This nominal interval does not guarantee a hard scan-duration bound. Unsupported platforms, sampling errors, unparseable option lists, missing observations with command items, and stdout lacking usable JSON all fail conservatively in the covered paths. The root/ancestry and argv-decoding exceptions are the open findings above. `so_lan` counts distinct PID/starttime/cmdline observations of a summary, not all commands or sample ticks. Fake argv[0] process fixtures verify observation/serialization, not native namespace/seccomp enforcement. The receipt's limitation text explicitly disclaims proof that every command was sandboxed.

The supplied fixed path-label set is exactly `/`, `/tmp`, `/dev`, `/proc`, `workspace`, `trong_workspace`, `to_tien_workspace`, `khac`; profile values come from `_HO_SO_GIA_TRI`. The fixed labels expand the spec's `cwd`/`khac` wording as the user explicitly described, without retaining arbitrary basenames. Unknown flags and incomplete option lists reaching the parser produce `khong_ro`; this does not repair information already lost before parsing.

Parent-1-to-merge changes comprise **139 paths**: `ops/handoff` 1, `ops/land` 21, `ops/leases` 1, `ops/reviews` 114, `ops/specs` 2. They are bookkeeping/evidence (including archived review scripts), not changed launcher dependencies. The master-side comparison from merge base `f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7` to `21fe565` has no changes under `.claude`, `.github`, `scripts`, `tl_core`, or `ops/bash_nen.py`; neither packet file imports/consumes the changed handoff/land/review/spec artifacts. The two packet files are byte-identical from `c92cbd2` to the reviewed merge. No interaction with launcher/test behavior was found. Master ancestry is verified; the asserted admission motivation and unpushed live state cannot be independently established offline. Cached `origin/master` is not used as the review baseline.

Size: `.claude/dev/launcher.py` **303 added / 1 deleted**, `.claude/dev/launcher_test.py` **380 added / 0 deleted**: **2 files / 683 added**, within the user's owner-raised **2 / 800** cap. The frozen spec and original lease still say 600; authority for 800 is the user's supplied `#748 issuecomment-6408141574`, not an independently read GitHub comment. This is **call 2 of 10** as supplied; no subagents or extra Codex/model calls were initiated.

Bare Ruff measured with version **0.15.15** on exact master/head file copies outside `src/`, `--no-cache`, and no repository Ruff configuration found. `--select F`: rc 1 on both, F841=5. Default rules: rc 1 on both, E702=113, E701=23, F841=5, E741=2, E731=2 (145 total). Comparison by file/rule/message/source-line/column, ignoring shifted line numbers: **0 added / 0 removed** for both selections; comparison script rc 0. This is zero lint delta, not absolute lint success or a CI pin/probe-contract result.

Commands and rc for the supporting static review are saved in `static-commands.json` and `ruff-results.json`: `git diff --check 21fe565... HEAD` rc 0; master-side dependency diff rc 0/empty; Ruff version rc 0; each bare lint invocation rc 1 as qualified above. All exact case/target commands, rc, durations and log filenames are in `results.json`.

Not run/verified: full unrelated launcher suite and repository worker/land gates, native Windows/macOS lanes, live GitHub/CI/lease/call-history readback, authenticated Codex child execution, actual bwrap/seccomp enforcement, or the outer launcher's completed signed execution receipt. No absence of native CI evidence is represented as a pass. The runtime declares `workspace-write` with approval policy `never`; actual kernel sandbox enforcement was not independently measured. The cloud runtime skill was read, but no `environment_status` tool is available in this session. No credentials or authenticated services were used.

Source integrity: the final tracked/untracked/ignored status and index/worktree diffs are empty; SHA/tree remain the requested values. Both packet files equal their Git blobs byte-for-byte. Details and SHA-256 values are in `final-integrity.json`. These endpoint checks establish no observed final source delta, not a proof about every possible transient filesystem write. All reviewer artifacts, temp mutants, and test fixture repositories are outside `src/`; no reviewer source edits, source commits, pushes, or GitHub comments were made.


## Re-measurement (incremental)

All child tests use an absent, absolute test-only Codex configuration outside `/tmp`, an environment allow-list excluding credentials, no bytecode writes, and scratch cache/temp paths. The source checkout is read-only. Native host: Linux.

Baseline command per row: `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`.

| Case | rc | Result |
|---|---:|---|
| `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | passed |
| `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 0 | passed |
| `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | passed |
| `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0 | passed |
| `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0 | passed |
| `r925_bo_loc_hong_xa_ong_co_gioi_han` | 0 | passed |
| `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | passed |
| `r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup` | 0 | passed |
| `r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai` | 0 | passed |
| `r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat` | 0 | passed |
| `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 0 | passed |
| `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 0 | passed |
| `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 0 | passed |
| `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 0 | passed |
| `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | passed |
| `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0 | passed |
| `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | passed |
| `r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE` | 0 | passed |
| `r926_ghi_het_dem_dung_phan_chua_ghi` | 0 | passed |
| `r926_ghi_so_truoc_khi_chot_khong_DO_DUOC` | 0 | passed |
| `r926_ket_thuc_chot_luong_TRUOC_khi_dong_tep` | 0 | passed |
| `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 0 | passed |
| `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 0 | passed |
| `r926_tien_to_dong_dai_co_tran_va_noi_qua_doan` | 0 | passed |
| `r926_ket_dong_tien_to_ung_vien_ma_khong_token_la_KHONG_RO` | 0 | passed |
| `r926_ngu_phap_khung_tung_thanh_phan` | 0 | passed |
| `r926_hop_dong_ngu_phap_bo_loc_theo_hanh_vi` | 0 | passed |
| `r926_bo_sinh_bien_the_co_du_phep` | 0 | passed |
| `r926_dot_bien_tu_sinh_moi_thanh_phan_regex` | 0 | passed |
| `r926_ghi_so_chup_rieng_ket_loi_dem` | 0 | passed |
| `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 0 | passed |
| `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | passed |
| `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0 | passed |
| `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0 | passed |
| `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0 | passed |
| `r925_codex_qua_han_van_124_va_giu_khung_da_den` | 0 | passed |
| `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 0 | passed |
| `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0 | passed |
| `r927_effort_do_duoc_tu_khung_may_chu` | 0 | passed |
| `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | passed |
| `r927_effort_khong_do_duoc_khi_model_khong_do_duoc` | 0 | passed |
| `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | passed |
| `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 0 | passed |
| `r927_trang_thai_sandbox_moi_nhanh` | 0 | passed |
| `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` | 0 | passed |
| `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 0 | passed |
| `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 0 | passed |

Strict mutation command per row: `python3 -B <scratch>/worker.py <exact test file> <temp mutant> <named target> mutant`. Worker rc 0 requires `TinHieuChotCa` with the named target in its traceback; survival, skip, unrelated exception, or missing target is failure. Every replacement anchor must occur exactly once and every temporary mutant must compile. Neutral temp-copy production control: rc 0.

| Mutant | Named target | rc | Result |
|---|---|---:|---|
| `r27_trong_ws_chep_ten` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_gia_tri_khong_loc` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_cap_drop_khong_loc` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_ranh_gioi_khong_nhan_hai_gach` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_arity_bo_qua` | `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 0 | kill |
| `r27_co_la_doan_khong_doi_so` | `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 0 | kill |
| `r27_khong_ranh_gioi_van_nhan` | `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 0 | kill |
| `r27_khong_ro_van_do_duoc` | `r927_trang_thai_sandbox_moi_nhanh` | 0 | kill |
| `r27_cmdline_nuot_moi_loi` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 0 | kill |
| `r27_khong_doc_lai_stat` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 0 | kill |
| `r27_goc_khong_ghim` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 0 | kill |
| `r27_effort_khong_kiem_kieu` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_effort_khong_kiem_rong` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_reasoning_khong_kiem_dict` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_bo_dem_effort` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_effort_o_lai_muc_model` | `r927_effort_do_duoc_tu_khung_may_chu` | 0 | kill |
| `r27_effort_chi_gia_tri_dau` | `r927_effort_do_duoc_tu_khung_may_chu` | 0 | kill |
| `r27_effort_khong_xet_model` | `r927_effort_khong_do_duoc_khi_model_khong_do_duoc` | 0 | kill |
| `r27_effort_khong_xet_thieu` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_ten_khong_basename` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_nhan_duong_tra_tho` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_ho_so_khong_loc_duong` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_ho_so_khong_kiem_dict` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_tt_khong_xet_nen` | `r927_trang_thai_sandbox_moi_nhanh` | 0 | kill |
| `r27_tt_bo_qua_loi` | `r927_trang_thai_sandbox_moi_nhanh` | 0 | kill |
| `r27_tt_bo_qua_con_chay` | `r927_trang_thai_sandbox_moi_nhanh` | 0 | kill |
| `r27_tt_khong_doi_json` | `r927_trang_thai_sandbox_moi_nhanh` | 0 | kill |
| `r27_tt_bo_qua_so_lenh` | `r927_trang_thai_sandbox_moi_nhanh` | 0 | kill |
| `r27_dem_moi_item` | `r927_trang_thai_sandbox_moi_nhanh` | 0 | kill |
| `r27_khoa_khong_gom_cmdline` | `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` | 0 | kill |
| `r27_quet_doc_environ` | `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` | 0 | kill |
| `r27_lenh_run_khong_lay_mau` | `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 0 | kill |
| `r27_lenh_run_khong_ghi_so` | `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 0 | kill |
| `r25_ghi_moi_dong_tron` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r25_ghi_moi_dong_tron` | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 0 | kill |
| `r25_cho_phep_theo_tien_to` | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 0 | kill |
| `r25_cho_phep_ca_dong_cut` | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 0 | kill |
| `r26_cho_phep_cat_moi_CRLF` | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 0 | kill |
| `r25_bo_go_ansi` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r25_khung_moi_target` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r25_moi_su_kien` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r25_nhan_id_model_rong` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r25_gop_theo_id` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r25_bo_dem_mat` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r25_bo_dem_mat` | `r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE` | 0 | kill |
| `r26_bo_dem_mat_nhieu_doan` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0 | kill |
| `r26_bo_dem_mat_nhieu_doan` | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0 | kill |
| `r26_bo_dem_mat_nhieu_doan` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_phan_loai_theo_token` | `r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE` | 0 | kill |
| `r25_parse_khong_can_ca_dong` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0 | kill |
| `r25_doc_khong_tran` | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0 | kill |
| `r25_xa_ong_khong_tran` | `r925_bo_loc_hong_xa_ong_co_gioi_han` | 0 | kill |
| `r26_bo_duoi_vat` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_khong_bo_khoang_trang` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_bo_xac_nhan_su_kien_khac` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0 | kill |
| `r26_dau_dong_khong_noi` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0 | kill |
| `r26_loai_khong_utf8_thay_the` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_khong_ro_khong_dem` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_khong_ro_moi_dong_dai` | `r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat` | 0 | kill |
| `r26_utf8_thay_the` | `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 0 | kill |
| `r25_noi_rust_log_thua_ke` | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0 | kill |
| `r25_khong_bat_trace` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r25_DO_DUOC_khi_loc_hong` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | kill |
| `r25_DO_DUOC_khi_loc_hong` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | kill |
| `r25_DO_DUOC_khi_ong_con_mo` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | kill |
| `r25_DO_DUOC_khi_ong_con_mo` | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 0 | kill |
| `r25_DO_DUOC_khi_mat` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | kill |
| `r25_DO_DUOC_khi_mat` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | kill |
| `r26_DO_DUOC_khi_khong_ro` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r25_DO_DUOC_khong_khung` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 0 | kill |
| `r25_DO_DUOC_khong_khung` | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 0 | kill |
| `r25_so_khong_chuyen_loi` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | kill |
| `r25_so_khong_chuyen_mat` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | kill |
| `r25_so_khong_chuyen_mat` | `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 0 | kill |
| `r26_so_khong_chuyen_khong_ro` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r25_bo_chot_luong` | `r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup` | 0 | kill |
| `r26_lay_mau_lai_luong_muon` | `r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai` | 0 | kill |
| `r26_mac_dinh_chua_chot_la_xong` | `r926_ghi_so_truoc_khi_chot_khong_DO_DUOC` | 0 | kill |
| `r25_doc_ong_khong_han` | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 0 | kill |
| `r26_dong_tep_truoc_chot` | `r926_ket_thuc_chot_luong_TRUOC_khi_dong_tep` | 0 | kill |
| `r26_dong_tep_truoc_chot` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 0 | kill |
| `r26_san_xuat_dong_tep_truoc` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 0 | kill |
| `r26_tep_stderr_co_dem` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 0 | kill |
| `r25_bo_loc_hong_khong_xa_ong` | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0 | kill |
| `r26_xa_khong_dem` | `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 0 | kill |
| `r25_bo_loc_hong_khong_ghi_loi` | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0 | kill |
| `r26_tep_dong_khong_dem` | `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 0 | kill |
| `r26_ghi_loi_khong_dem` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 0 | kill |
| `r26_ghi_dem_ca_doan` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 0 | kill |
| `r26_ghi_khong_lap` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 0 | kill |
| `r26_luong_hong_lot_ra` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 0 | kill |
| `r26_luong_hong_khong_dong_ong` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 0 | kill |
| `r26_luong_hong_khong_ghi_loi` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 0 | kill |
| `r26_cho_luong_chua_chay` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 0 | kill |
| `r26_khong_ro_khong_doi_json` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_doc_tron_khong_parse_bo_qua` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_ghi_bo_chot_0_byte` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 0 | kill |
| `r26_mot_doan_bo_dieu_kien_so_doan` | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 0 | kill |
| `r26_doc_tron_khong_ro_ca_su_kien_khac` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0 | kill |
| `r26_doc_tron_khong_ro_khong_doi_json` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_doc_tron_bo_token` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r26_tien_to_ung_vien_tha` | `r926_ket_dong_tien_to_ung_vien_ma_khong_token_la_KHONG_RO` | 0 | kill |
| `r26_tien_to_khong_tran` | `r926_tien_to_dong_dai_co_tran_va_noi_qua_doan` | 0 | kill |
| `r26_tien_to_bo_max` | `r926_tien_to_dong_dai_co_tran_va_noi_qua_doan` | 0 | kill |
| `r26_token_khong_dinh` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_khong_dat_lai_moi_dong` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r26_bo_dong_cut_EOF` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0 | kill |
| `r26_response_khong_kiem_object` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 0 | kill |
| `r26_id_khong_kiem_chuoi` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 0 | kill |
| `r26_id_khong_strip` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 0 | kill |
| `r26_model_khong_kiem_chuoi` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 0 | kill |
| `r26_model_khong_strip` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 0 | kill |
| `r26_ket_thuc_khong_dong_tep` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 0 | kill |
| `r26_khong_ghi_so` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv5_prefix_decoded` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_rv5_dedup_response_id` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv5_dedup_whole` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv5_frame_match_guard` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r26_rv5_parsed_model_guard` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r26_rv5_prefix_match_guard` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_rv5_first_chunk_capture` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_rv5_classify_only_at_lf` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0 | kill |
| `r26_rv5_reason_guard` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 0 | kill |
| `r26_rv5_rust_override_record` | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 0 | kill |
| `r26_rv5_exception_valueerror` | `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 0 | kill |
| `r26_rv5_old_late_production_latch` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv5_optional_counter_init` | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 0 | kill |
| `r26_rv5_retain_caller_counter` | `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv5_candidate_search` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv5_target_only` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r26_rv5_receive_position_only` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 0 | kill |
| `r26_rv5_lf_detection` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 0 | kill |
| `r26_rv5_codex_mode_disabled` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv5_codex_env_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv5_codex_reader_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv5_codex_pipe_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv5_finish_object_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv6_a_ansi_bo_tham_so_hoi` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_a_ansi_bo_trung_gian` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_a_ansi_chi_m` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_b_bo_neo_dau` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv6_b_moc_thoi_gian` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv6_b_muc_TRACE` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_b_khoang_truoc_TRACE` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_b_dau_cach_sau_message` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv6_c_neo_cuoi` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_c_doi_tuong_json` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_d_khoa_type` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_rv6_d_khong_escape` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_rv6_d_dong_nhay` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_rv6_d_khoang_sau_ngoac` | `r926_tien_to_dong_dai_co_tran_va_noi_qua_doan` | 0 | kill |
| `r26_rv6_d_khoang_hai_cham` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0 | kill |
| `r26_rv6_e_bo_completed` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv6_e_cham_bat_ky` | `r926_ngu_phap_khung_tung_thanh_phan` | 0 | kill |
| `r26_rv6_f_chi_dau_cach` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv6_g_duoi_ngan` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv6_h_luong_khong_ansi` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv6_i_tran_dau_nho` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 0 | kill |
| `r26_rv6_j_bo_CRLF` | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 0 | kill |
| `r26_rv6_l_su_kien_bo_completed` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv6_m_dau_json_bo_ngoac` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 0 | kill |
| `r26_rv7_luong_doc_khong_daemon` | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 0 | kill |
| `r26_rv7_tep_stderr_van_ban` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 0 | kill |
| `r26_rv7_khong_chup_ket` | `r926_ghi_so_chup_rieng_ket_loi_dem` | 0 | kill |
| `r26_rv7_khong_chup_loi` | `r926_ghi_so_chup_rieng_ket_loi_dem` | 0 | kill |
| `r26_rv7_khong_chup_dem` | `r926_ghi_so_chup_rieng_ket_loi_dem` | 0 | kill |
| `r25_loc_ca_luot_khong_phai_codex` | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 0 | kill |

## Final measured totals

| Group | Cases passed / run | Mutants with every required signal / total | Named-target signals / executions | rc |
|---|---:|---:|---:|---:|
| r925 / r25 | 15 / 15 | 25 / 25 | 32 / 32 | 0 |
| r926 / r26 | 23 / 23 | 99 / 99 | 102 / 102 | 0 |
| r927 / r27 | 9 / 9 | 33 / 33 | 33 / 33 | 0 |
| Total | 47 / 47 | 157 / 157 | 167 / 167 | 0 |

`python3 -B review-r27b.hrx6pfr4/measure.py`: **rc 0**. No case skips, surviving mutants, unrelated-exception kills, missing targets, failed anchors, or compile failures. Every named-target signal was verified again from its recorded traceback metadata. Neutral temp-copy production control: rc 0. Source/manifest/temporary-mutant integrity script: rc 0.

The required `r926_dot_bien_tu_sinh_moi_thanh_phan_regex` ran on this SHA with `--lan 1`, rc 0, no skip. Its passing per-constant counts and survivor assertions establish **207 generated variants: 200 target-signal kills and exactly 7 documented equivalent survivors**, with no unrelated exceptions credited. These are separate from the 157 hand-written mutants. The sandbox lexical regexes were removed in this fix; no newly added production sandbox regex lies outside that generator.

Mutation qualification: `r26_rv7_tep_stderr_van_ban` reaches its named target signal because the altered text/unbuffered file-open mode prevents launch success; it does not establish later text-stream behavior. Signals are counted exactly as requested, not as proof of every downstream property.

- `git -C src rev-parse HEAD HEAD^{tree}`: rc 0; expected SHA/tree.
- `git -C src status --porcelain=v1 --untracked-files=all --ignored`: rc 0; empty output.
- `git -C src diff --exit-code`: rc 0; empty output.
- `git -C src diff --cached --exit-code`: rc 0; empty output.

Packet-file SHA-256: launcher `1dd72c71143b00eb44b26c5007d5889119814a554369dd76e6b13abfb013a3cb`; tests `0584b7c798868f2839fbec15ba16c51ab507c6067c132ee41d181cc37836c643`.

Completed UTC: 2026-10-26T04:37:39.633883+00:00.

VERDICT: changes_requested
