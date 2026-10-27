# WP748 r27 (spec r27), independent review, round 1

Review completed 2026-10-26 03:57:35 UTC. Started 2026-10-26 03:30:03 UTC.

**Changes requested: 0 P0, 1 P1, 4 P2, 0 P3.** Final isolated measurements: 45/45 cases pass (rc 0, no skips); 151/151 hand-written mutants produce all 161/161 named-target `TinHieuChotCa` signals (strict runner rc 0). The regex case also passes its 207-variant checks. Test success does not close the five substantive findings below.

Reviewer: OpenAI Codex; runtime instructions identify the agent as Codex based on GPT-6. Provider: `openai_codex`; execution surface: a tool-enabled Codex agent in a Linux shell (outer `codex_cli` invocation is user-reported); transport: machine (direct tool execution; outer routing not independently verified). The exact serving model, effort, outer launcher invocation and completed execution receipt are not exposed to this reviewer; no claim of independently verifying them. User reports invocation through `launcher.py run`. No GitHub access or authenticated service calls were made. The initial test isolation issue is disclosed below.

Reviewed SHA: `838d7e7581b443a84e7421689aa30bcc2bf2b319`.
Tree: `83d7a94eec77e7a1c1b98ce8b1175607aab7dc5a`.
Review class: `sensitive`.

Identity preflight passed: non-shallow full clone, detached HEAD, clean working tree, parent 1 `f6f2e428c7d8e446d4c3e05f25497c76e184ffc2`, parent 2 and cached `origin/master` `f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7`. Merge base is `8d4638eb8695c7f5628eda7d258f66067e141803`. No cached named branch contains this SHA; branch provenance and whether it is unpushed on the live remote cannot be independently verified offline. The hash is the review identifier.

Commands measured so far:

- `git -C src rev-parse --is-shallow-repository HEAD HEAD^{tree} HEAD^1 HEAD^2 origin/master`: rc 0; exact values above.
- `git -C src symbolic-ref -q HEAD`: rc 1, empty output (expected detached HEAD).
- `git -C src status --porcelain=v1`: rc 0, empty output.
- `git -C src branch -a --contains 838d7e7581b443a84e7421689aa30bcc2bf2b319`: rc 0, detached HEAD only.
- `git -C src merge-base f6f2e428c7d8e446d4c3e05f25497c76e184ffc2 f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7`: rc 0, expected original base.
- `git -C src diff f6f2e428c7d8e446d4c3e05f25497c76e184ffc2 838d7e7581b443a84e7421689aa30bcc2bf2b319 -- .claude/dev/launcher.py .claude/dev/launcher_test.py`: rc 0, empty; merge leaves both packet files unchanged.
- `git -C src diff --numstat f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7 838d7e7581b443a84e7421689aa30bcc2bf2b319`: rc 0; launcher 250 added/1 deleted, tests 255 added/0 deleted; 2 files / 505 added lines, within the stated 2 / 600 cap.
- `git -C src show origin/ops/wp748-r27-g27-lease:ops/specs/wp748-r27-launcher-effort-sandbox.md`: rc 0.
- `git -C src show origin/ops/wp748-r27-g27-lease:ops/leases/wp748-r27-g27-claude-remote-20261026.yaml`: rc 0; r27/g27, correct write set and spec hash, recorded expiry 2026-10-27 00:18:51 UTC. Live lease/heartbeat/authority state cannot be verified offline.

Codex budget: this is call 1 of 10 per the user and the frozen spec's ADR-0055 declaration. No additional Codex calls or subagents initiated. Owner size authorization `#748 issuecomment-6405383674` is recorded in the lease and supplied by the user; GitHub cannot be read in this review, so its live contents are not independently verified.


Measurement isolation correction: the first pass returned 45/45 baseline passes and 161/161 named-target signals, but scrubbed environment variables did not stop the existing launcher from reading default on-disk authentication/rejection state. This was unintended. A metadata-only check confirmed a default auth file exists; no credential value was surfaced to or inspected by the reviewer, and no network authentication was performed. That first pass is retained under `review-r27.OQfDSW/` and is not used as the final isolated acceptance evidence. The final pass selects a separate, empty Codex configuration only for test subprocesses; the reviewer runtime configuration is not changed.

Frozen spec SHA-256 independently measured: `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd`, matching the requested value (git show rc 0, SHA-256 script rc 0).

Runtime policy reports `workspace-write` and approval policy `never`; this is configured policy, not an independent kernel sandbox measurement. Source was treated read-only. Exact serving model/effort, outer execution receipt and actual OS sandbox enforcement remain unverified by this reviewer.

## Substantive findings

These are open findings on the reviewed SHA, not new exploit demonstrations. Additional probes used existing checked-in fixtures, platform mocks, and a benign descendant-read fault. No new exploit payload was authored.

### R27-ALLOW-01 — P1 — `sandbox-output-not-closed`

Location: `.claude/dev/launcher.py:1871` (also 1854–1856, 1878, 1894–1901, 1931–1940); test `.claude/dev/launcher_test.py:11215`.

Scenario: the claimed allow-list accepts arbitrary strings by their spelling. `_nhan_duong_sb` persists a user-chosen single-component workspace basename; `_token_sb` returns any matching lowercase token unchanged, including in profile type/access/network/special-kind fields. Flag names are also copied based only on a regex. A private name or value using these permitted characters therefore survives into `sandbox_quan_sat`, which `ghi_so` writes to the receipt. This is not a guarantee that only approved semantic values can reach `run.json`. In particular, preserving workspace child names contradicts spec §3.2's replacement of paths with fixed labels (`cwd`/`khac`). The checked-in fixture itself demonstrates retained `workspace/.git` and an arbitrary flag (`--la`); the general unchecked value channel follows directly from the return statements. The fake-secret test uses strings whose spaces/case/punctuation make them fail the regex, so it cannot establish the stronger confidentiality claim. It serializes helper results rather than checking a secret-bearing production `run.json`.

Fix: in the summarizers, map paths to fixed approved labels without copying basenames; use explicit semantic sets for retained profile enums and flag/value forms, and discard unknown values. Keep any intentional expansion of the frozen output vocabulary explicit. Add an end-to-end receipt assertion for the complete recursive output vocabulary, including values that happen to satisfy the lexical regex. Guard against the remediation losing required known sandbox flags or leaking data through an error message. No new secret/payload fixture was authored by this reviewer.

### R27-PARSE-02 — P2 — `sandbox-argv-boundary`

Location: `.claude/dev/launcher.py:1911` and `.claude/dev/launcher.py:1926`.

Scenario: the bwrap summarizer recognizes the arity only of bind options and cap-drop. It advances one token over every other argument, including options already present in the fixture such as `--setenv` and `--argv0`. An option-looking value consumed by one of those options is consequently reinterpreted as a sandbox flag. Without a standalone delimiter the entire remaining argv is scanned, including command arguments. The record can report an isolation flag that was an argument value, not an applied option. `sandbox_gioi_han` limits coverage of commands; it does not excuse falsely identifying flags within an observed process.

Fix: parse the supported option grammar with explicit arities and a proven command boundary; if it cannot be parsed, record measurement uncertainty instead of inferring flags. Add cases for values resembling options and a missing/ambiguous command boundary, with a dedicated mutation of the boundary/arity rule. Ensure the fix does not treat a delimiter used as an option value as the command boundary. This scenario is a static control-flow finding; no new argv payload was executed.

### R27-PROC-03 — P2 — `sandbox-sampling-errors-hidden`

Location: `.claude/dev/launcher.py:1994` and `.claude/dev/launcher.py:2004` (status at 2038).

Scenario: every per-process `OSError` is silently treated as a process exiting. This also discards `PermissionError` and genuine read failures. Once any prior sandbox observation exists, a later denied descendant read leaves `self.loi` empty and produces `DO_DUOC`, contrary to the spec's requirement that all sampling attempts succeed. With no observations, the same error can also produce `KHONG_THAY_LENH` when stdout has a non-command JSON event. The r927 status case inserts `PermissionError` into `loi` by hand; it never verifies that `_quet` actually records it.

Measured: `probes.py` seeded one observation using the existing `_R27_BWRAP` fixture, then denied one real benign descendant's cmdline read. Result: denial count 1, `loi == []`, `sandbox_trang_thai == "DO_DUOC"`. Probe rc 0; output in `review-r27.OQfDSW/probes.jsonl`.

Fix: distinguish process disappearance from inaccessible/failed observations, latch sanitized sampling uncertainty, and let it dominate every success/absence status. Exercise real sampler error handling, not just manually populated final state. Ensure ordinary process-exit races do not become blanket failures and unrelated inaccessible processes do not get mistaken for confirmed descendants.

### R27-PID-04 — P2 — `sandbox-process-identity-race`

Location: `.claude/dev/launcher.py:1997`–2010; root identity at `.claude/dev/launcher.py:1970`.

Scenario: the scan builds a parent graph from one set of stat reads and later reads cmdline by numeric PID without validating stat again. A descendant can exit and its PID can be reused between those operations; the new process's cmdline is then attributed to the old descendant/starttime. The root codex PID is not pinned to its own starttime either. The `(pid, starttime, cmdline)` deduplication key prevents a different problem—discarding a later exec—but does not validate the identity or current ancestry of the process whose cmdline was read. This can both manufacture sandbox evidence and read a non-descendant's arguments, beyond the promised scope.

Fix: pin the root's identity and validate child identity/ancestry around each cmdline read using only the permitted stat/cmdline sources; discard and mark uncertain observations whose identity changes. Add deterministic identity-change coverage at the graph/read boundary and a dedicated target mutation. Preserve the current fork-before-exec re-observation behavior, and avoid loops or unbounded retries while the process graph changes. This is a static race finding, not a claim that PID reuse occurred in this review; no PID-reuse exploit was authored.

### R27-TEST-05 — P2 — `sandbox-status-tests-native-platform-dependence`

Location: `.claude/dev/launcher_test.py:11260`–11269.

Scenario: `moi(nen_linux=True)` constructs `_LayMauSandbox` using the real platform. It only overrides `luong` when the argument is false. On Windows/macOS the default object therefore still has `luong is None`, but the first assertion unconditionally expects `DO_DUOC`. Thus a platform-independent status test deterministically fails on both unsupported platforms, even though the production sampler correctly reports `KHONG_DO_DUOC`. This prevents the required green Windows lane.

Measured: the unchanged named test raised `TinHieuChotCa` at its `do_duoc` assertion under both Windows and Darwin platform mocks. In the same probe, direct construction/start/stop/write of the sampler returned `KHONG_DO_DUOC` without a crash for both. These are Linux-hosted simulations; no native Windows/macOS run or CI result is claimed.

Fix: make the status fixture's Linux capability explicit and independent of the host, while testing the real non-Linux constructor separately; retain a reasoned skip only for the genuinely Linux `/proc` case. Verify the named test and its target mutants on native Windows, then verify Linux behavior still observes descendants. Do not repair this by skipping the entire status case on non-Linux platforms.

Finding class ledger: R27-ALLOW-01 / `sandbox-output-not-closed` (P1); R27-PARSE-02 / `sandbox-argv-boundary` (P2); R27-PROC-03 / `sandbox-sampling-errors-hidden` (P2); R27-PID-04 / `sandbox-process-identity-race` (P2); R27-TEST-05 / `sandbox-status-tests-native-platform-dependence` (P2). All are open, from round 1 on the SHA identified above. Closure checks and remediation risks are given with each finding. No previous-round comparison applies.

## Mutation-evidence qualification

The target for `r26_rv7_tep_stderr_van_ban` raises its signal at the launch-success assertion because text mode plus `buffering=0` fails at file open. This is a direct consequence of the mutated file mode, so it is counted under the requested signal rule; it does not demonstrate downstream text-mode streaming or redaction. Similarly, the late-close mutants can first fail their close-timing fixture assertion before the receipt-status assertion. These limits are disclosed rather than treating every signal as proof of every downstream property. No unrelated exception was counted as a final-pass kill, and no extra finding is assigned merely because a valid mutant fails earlier in the affected path.


Isolated setup attempt: a test configuration path under `/tmp` was rejected by the existing launcher because `/tmp/.git` exists in this environment. The resulting missing-run-directory failures are reviewer setup failures, not packet regressions; those counts are excluded. Logs are retained under `review-r27-isolated.CQxG8j/`. The final pass uses an explicitly nonexistent absolute configuration path outside `/tmp`, verified absent; no directory or credential is created there. A production r927 baseline preflight succeeds with this setup.

## Re-measurement (incremental)

All commands run with an empty test-only Codex configuration selected through the supported CODEX_HOME setting (only in child environments), credentials excluded from the subprocess environment, bytecode writes disabled and cache/temp paths outside `src/`. Test-created Git fixtures are scratch-only. Source files are read from the verified SHA. No new exploit payloads were authored.

Baseline command for each row: `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`. Full outputs are in `review-r27-final.f6OPzw/case-<case>.log`.

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
| `r927_trang_thai_sandbox_moi_nhanh` | 0 | passed |
| `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` | 0 | passed |
| `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 0 | passed |

Mutation commands: `python3 review-r27-final.f6OPzw/measure.py worker <temporary-launcher.py> <named-target>`. Each checked-in mutant is applied using its exact first replacement(s), to a uniquely named temporary copy of the reviewed launcher. Each target runs in a fresh subprocess. rc 0 means the named target raised `TinHieuChotCa`; rc 1 survived; rc 2 unrelated exception; rc 3 skipped; rc 124 timeout. Only rc 0 counts as a kill. Details and exception traces are retained in `mutant-*.log`.

| Mutant | Named target | rc | Result |
|---|---|---:|---|
| `r27_effort_khong_kiem_kieu` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_effort_khong_kiem_rong` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_reasoning_khong_kiem_dict` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_bo_dem_effort` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_effort_o_lai_muc_model` | `r927_effort_do_duoc_tu_khung_may_chu` | 0 | kill |
| `r27_effort_chi_gia_tri_dau` | `r927_effort_do_duoc_tu_khung_may_chu` | 0 | kill |
| `r27_effort_khong_xet_model` | `r927_effort_khong_do_duoc_khi_model_khong_do_duoc` | 0 | kill |
| `r27_effort_khong_xet_thieu` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | kill |
| `r27_khong_cat_sau_hai_gach` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_ten_khong_basename` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_nhan_duong_tra_tho` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_ten_con_khong_loc` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_ten_con_nhan_cham_cham` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_token_khong_loc` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
| `r27_cap_drop_khong_loc` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | kill |
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

Measured totals: `{"cases": {"passed": 45}, "mutant_targets": {"kill": 161}, "mutants": 151}`.

## Branch, safety and race assessment

| Requirement | Assessment on this SHA |
|---|---|
| Effort `DO_DUOC` | Correct in the production path: extracted only from accepted server frames, counted before model-frame deduplication, distinct values preserve first-seen order, and measured-model status is required. |
| Missing/invalid effort | Covered by r927: absent reasoning, non-object reasoning, numeric/null/blank effort all downgrade effort while retaining valid model evidence; a duplicate response ID with missing effort is still counted. |
| Model not measured | Covered by r927: no accepted frames and a lost frame both force effort `KHONG_DO_DUOC`; no CLI/config fallback is used. |
| Sandbox `DO_DUOC` | Observation exists, no recorded error, sampler stopped. R27-PROC-03 shows why recorded-error absence does not establish successful reads; R27-PARSE-02 and R27-PID-04 undermine interpretation of the observation. |
| Sandbox `KHONG_THAY_LENH` | Correct for a successful scan with no observation and valid JSON stdout without command_execution. Failures silently ignored by `_quet` can incorrectly take this branch (R27-PROC-03). |
| Non-Linux | Constructor creates no sampler thread; start/stop/write return `KHONG_DO_DUOC`. Windows/Darwin platform simulations pass for the class; the shared status test is broken on those platforms (R27-TEST-05). Native OS results are not measured. |
| `/proc` unavailable / sampler error | Directory-listing or uncaught scan failures reach the thread error list; start failures are caught; recorded errors dominate observations. Per-file permission/I/O errors do not reach that list (R27-PROC-03). |
| Commands present, no sandbox observed | Valid command_execution items produce `KHONG_DO_DUOC` with the short-command/outside-sandbox explanation. Duplicate item IDs are deduplicated. |
| No usable JSON / stdout unreadable | Conservative additional `KHONG_DO_DUOC` branch; it does not assert command absence from plain/non-JSON output. |
| Thread lifetime | Production stops the sampler in `finally`, joins up to 5 seconds, latches `is_alive`, then writes a copied observation/error state. A still-running sampler forces `KHONG_DO_DUOC` even if it later ends. No additional successful-status race identified at this boundary. |
| Fork before exec | Including cmdline in the dedup key permits re-observation after exec; the real Linux r927 test and its named mutant exercise it. Starttime in that key does not solve identity reuse between reads (R27-PID-04). |
| Read scope / environ | Production sampler opens only stat and cmdline; real Linux instrumentation and the supplied environ mutant exercise that boundary. Ancestry derives from an unvalidated snapshot (R27-PID-04). No production environ read was found. The supplied environ mutant ran only against credential-free fixture descendants. |
| Receipt serialization | `ghi_so` serializes summaries from `thay`, not raw cached cmdline tuples from `da`. Nevertheless summaries can retain unapproved data (R27-ALLOW-01), and token-position parsing can mislabel command/value text (R27-PARSE-02). The no-raw-path claim is interpreted for the new sandbox telemetry; pre-existing workspace/artifact fields intentionally contain paths. |
| Spec §3.2 limitation | The receipt explicitly says sampling can miss short commands and does not prove every command was sandboxed. It also acknowledges self-declared argv[0]. The test fixtures deliberately rename Python as bwrap: they establish detection of argv-shaped observations, not actual namespace/seccomp enforcement or a native bwrap binary. `so_lan` counts distinct PID/starttime/cmdline observations, not successful samples or a count of all commands. |

No Linux baseline case returned early or was counted as skipped. The non-Linux early return in the real `/proc` case is explicit and reasoned. The regex generator checks all seven existing stderr regex constants between its source markers: 207 variants in total; its passing assertions establish 200 target-signal kills and the exact seven documented equivalent survivors, with no other exception credited. The three new sandbox regex constants are outside that existing stderr scan range; the 207 count must not be represented as automatic mutation coverage of those constants.

## Merge scope, lint and limits

Master-side diff `8d4638eb8695c7f5628eda7d258f66067e141803..f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7` has 219 paths: 217 under `ops/land/` and only `.claude/dev/packet_loop.py` plus its test as executable changes. Those code changes concern discovering the ADR-0054 activation document by content instead of a fixed number. Neither reviewed launcher file imports or calls this changed logic or consumes these land artifacts. No launcher/test interaction was found. The packet-file diff from parent 1 to the merge is empty. `git merge-base --is-ancestor f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7 838d7e7581b443a84e7421689aa30bcc2bf2b319` returned rc 0, confirming the admission ancestry. The asserted motivation for the merge and live unpushed state cannot be verified from Git objects alone.

Bare Ruff: version `0.15.15`, version probe rc 0. Both selected packet files were checked from exact content copies of master and candidate outside `src/`, with `--no-cache` and no repository Ruff configuration found. Commands for each `<side>` (`master`, `head`):

- `python3 -m ruff check --no-cache --select F --output-format json review-r27.OQfDSW/<side>/launcher.py review-r27.OQfDSW/<side>/launcher_test.py`: rc 1 on both; five existing F841 findings on both.
- `python3 -m ruff check --no-cache --output-format json review-r27.OQfDSW/<side>/launcher.py review-r27.OQfDSW/<side>/launcher_test.py`: rc 1 on both; E702=113, E701=23, F841=5, E741=2, E731=2 (145 total).
- Comparison by filename, rule, message, source-line content and column, ignoring line-number shifts: 0 added / 0 removed for both configurations; comparison script rc 0. Thus the measured lint delta is zero; absolute lint is not green. This does not claim the CI Ruff pin/probe contract ran.

`git -C src diff --check f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7 838d7e7581b443a84e7421689aa30bcc2bf2b319`: rc 0.

Not run: full unrelated launcher suite, full repository worker/land gates, native Windows/macOS execution, GitHub/CI readback, a real authenticated Codex child, or actual enforcement verification of native bwrap/seccomp. The requested r925/r926/r927 cases and r25/r26/r27 mutant targets are reported individually above. No GitHub access, comments, pushes, or source commits were made. This remains Codex review call 1/10; local test repetitions do not invoke another model.

## Final measured totals and execution records

| Group | Baseline cases passed / run | Hand-written mutants with required signals / total | Named-target signals / executions | rc |
|---|---:|---:|---:|---:|
| r925 / r25 | 15 / 15 | 25 / 25 | 32 / 32 | 0 |
| r926 / r26 | 23 / 23 | 99 / 99 | 102 / 102 | 0 |
| r927 / r27 | 7 / 7 | 27 / 27 | 27 / 27 | 0 |
| Total | 45 / 45 | 151 / 151 | 161 / 161 | 0 |

All 45 baseline commands use `--lan 1`; none skipped. Each of the 151 replacement anchors matched exactly once, each temporary mutant compiled, and every declared named target ran in a separate process. Final worker rc 0 means the named target actually raised `TinHieuChotCa`, verified from its traceback; other exceptions were not kills. The regex generator's independent 207 variants are not added to the 151 hand-written mutant count (200 killed, seven declared equivalent).

Execution commands and rc:

- `python3 -B review-r27.OQfDSW/measure.py`: rc 0; initial pass, excluded from final isolated acceptance evidence because of the auth-state issue.
- `python3 -B review-r27-isolated.CQxG8j/measure.py`: rc 1; invalid reviewer setup under `/tmp/.git`, 36 baseline passes/9 failures and 133 signals/28 other exceptions. None of this attempt's results replaces the final pass.
- `python3 -B review-r27-final.f6OPzw/measure.py`: rc 0; final counts above, with only an absent test configuration selected in subprocess environments.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<scratch>/pycache python3 review-r27.OQfDSW/probes.py`: rc 0; records the Windows/Darwin simulations and the reproduced denied-read false success. Native platform test rc is not inferred from this probe.
- Source/manifest integrity script: rc 0; all required cases/targets present exactly once; all 151 temporary copies match their declared replacements; all 161 tracebacks contain the named target; test configuration remains absent.

Machine-readable final commands, rc and durations: `review-r27-final.f6OPzw/results.json`. Per-case/target output: `case-*.log` and `mutant-*.log` in that directory. Final source checks: `review-r27-final.f6OPzw/final-integrity.json`. These are reviewer-generated local execution records; they are not the outer launcher's signed execution receipt.

Final source checks at 2026-10-26 03:57:35 UTC:

- `git -C src rev-parse HEAD HEAD^{tree}`: rc 0; expected SHA/tree.
- `git -C src status --porcelain=v1 --untracked-files=all --ignored`: rc 0; empty output.
- `git -C src diff --exit-code`: rc 0; empty output.
- `git -C src diff --cached --exit-code`: rc 0; empty output.

Both packet files also compare byte-for-byte with the reviewed Git blobs. SHA-256: launcher `7c52847c61a9a37494f7fe3569baea44b9a22474546d510422b72887a1061ccf`; tests `990c830cbd9bb86d36277a5e35f7eae40d9c04480afeac96e0550289fa6dcc03`. Tracked, untracked and ignored status is clean. Snapshot equality does not prove the absence of every possible transient write; it establishes no observed final delta. No reviewer source edits, source commits or pushes were performed.

Size remains 2 files / 505 added lines (250 launcher + 255 tests), within 2 / 600. Call count remains 1 / 10 as reported by the user; prior/live call history and owner GitHub authorization cannot be independently verified offline.

VERDICT: changes_requested
