# Independent review — WP748 r27, round 5

**Changes requested: 0 P0, 0 P1, 1 P2, 0 P3.** R27-PID-04e is closed; R27-PID-04f identifies a remaining ancestry-comparison gap between scans. Re-measured: 48/48 cases, 163/163 mutants, 173/173 named-target signals.

Reviewer: OpenAI Codex (`openai_codex`), identified by the session developer runtime as an agent based on GPT-6. Execution surface observed: tool-enabled Codex agent on Linux; transport: machine/local tool execution. Outer `codex_cli` routing is user-reported. Shell tool execution is available in this session. An exact deployed model version and the outer `launcher.py run` receipt are not independently visible yet; invocation through that launcher is user-supplied context. No credentials or GitHub access used.

Review Class: sensitive. User reports this is Codex call 5 of 10; external call accounting and GitHub comment #748 issuecomment-6408141574 cannot be verified here.

Identity verified at 2026-10-26T05:49:35.706651+00:00:

- Reviewed SHA: `c6f6ef6cc6555c01b008a7c22266589b454d1653`.
- Tree: `fc2512558e0c7cfc921f419fa1ddba093a5f7fbc`.
- Full clone (`--is-shallow-repository=false`); detached HEAD (`symbolic-ref -q HEAD`, rc 1 as expected); clean worktree.
- Local branch `agent/wp748-r27-claude` points at the reviewed SHA. Single parent: `483a006b1e436dfe655478ce8e371475b3d649cd`.
- Parent is a merge with master `356eb262cbd491b9599b56d5f7c41c93dd9a28a1` as second parent; `merge-base --is-ancestor` for that master and HEAD returned rc 0.
- The clone has remote-tracking `origin/HEAD` and `origin/agent/wp748-r27-claude` refs at the reviewed SHA. Local remote-tracking refs alone do not establish publication to GitHub. Local/unpushed status beyond the clone is user attestation and cannot be independently established without accessing the upstream, which is prohibited.

Work is restricted to this verdict and scratch outside `src/`.

Frozen spec SHA-256 matches `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd` (`git show`, rc 0; SHA-256 check, rc 0). Lease: r27/g27, expected spec hash and two-file write set, recorded expiry `2026-10-27T00:18:51Z`. GitHub and current lease/heartbeat state cannot be verified. User-supplied narrowing decision and raised cap govern this review; frozen spec/lease still state the earlier 600-line cap.

`git -C src diff --numstat 356eb262cbd491b9599b56d5f7c41c93dd9a28a1 HEAD`, rc 0: launcher.py +342/-1, launcher_test.py +458/-0. Exactly 2 files / 800 additions, within the supplied cap. One earlier command mistyped the base OID and returned rc 128; it was corrected before any delta analysis.

Cloud runtime skill read; no `environment_status` tool is available. No network or credential discovery performed.

## Re-measured cases

All commands run on the verified source SHA, with credential-free child environments, bytecode writes disabled, and temporary files outside `src/`. `CODEX_HOME` is used only for its intended child configuration-selection purpose, pointing at a verified nonexistent path outside any repository. No authenticated Codex execution occurs.

Command for every row: `python3 src/.claude/dev/launcher_test.py --lap-ca <case> --lan 1`. Full commands, durations and output are retained in `review-r27e.TYUXfY/matrix-results.json`.

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
| `r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that` | 0 | passed |
| `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 0 | passed |

## Re-measured named-target mutants

Only checked-in `DOT_BIEN` replacements are used. Each anchor must occur exactly once; every mutant is written to its own temporary launcher copy and compiled. The strict child returns rc 10 only for `TinHieuChotCa` whose traceback includes the named target; rc 0 is survival, 11 skip, 12 unrelated exception, 13 non-target signal, 14 missing target, 124 timeout. A mutant is counted killed only when every declared target returns 10.

Child command: `python3 -B review-r27e.TYUXfY/run_matrix.py worker <temporary-launcher.py> <named-target>`.

| Mutant | Named target | rc | Result |
|---|---|---:|---|
| `r27_to_tien_chi_so_bd` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 10 | TinHieuChotCa: killed |
| `r27_goc_ghim_tre` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 10 | TinHieuChotCa: killed |
| `r27_cmdline_bo_doi_so_rong` | `r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that` | 10 | TinHieuChotCa: killed |
| `r27_cmdline_khong_nul_van_tin` | `r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that` | 10 | TinHieuChotCa: killed |
| `r27_khong_xac_thuc_to_tien` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 10 | TinHieuChotCa: killed |
| `r27_goc_ghim_muon` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 10 | TinHieuChotCa: killed |
| `r27_trong_ws_chep_ten` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_gia_tri_khong_loc` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_cap_drop_khong_loc` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_ranh_gioi_khong_nhan_hai_gach` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_arity_bo_qua` | `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 10 | TinHieuChotCa: killed |
| `r27_co_la_doan_khong_doi_so` | `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 10 | TinHieuChotCa: killed |
| `r27_khong_ranh_gioi_van_nhan` | `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 10 | TinHieuChotCa: killed |
| `r27_khong_ro_van_do_duoc` | `r927_trang_thai_sandbox_moi_nhanh` | 10 | TinHieuChotCa: killed |
| `r27_cmdline_nuot_moi_loi` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 10 | TinHieuChotCa: killed |
| `r27_khong_doc_lai_stat` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 10 | TinHieuChotCa: killed |
| `r27_goc_khong_ghim` | `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 10 | TinHieuChotCa: killed |
| `r27_effort_khong_kiem_kieu` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r27_effort_khong_kiem_rong` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r27_reasoning_khong_kiem_dict` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r27_bo_dem_effort` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r27_effort_o_lai_muc_model` | `r927_effort_do_duoc_tu_khung_may_chu` | 10 | TinHieuChotCa: killed |
| `r27_effort_chi_gia_tri_dau` | `r927_effort_do_duoc_tu_khung_may_chu` | 10 | TinHieuChotCa: killed |
| `r27_effort_khong_xet_model` | `r927_effort_khong_do_duoc_khi_model_khong_do_duoc` | 10 | TinHieuChotCa: killed |
| `r27_effort_khong_xet_thieu` | `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r27_ten_khong_basename` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_nhan_duong_tra_tho` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_ho_so_khong_loc_duong` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_ho_so_khong_kiem_dict` | `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 10 | TinHieuChotCa: killed |
| `r27_tt_khong_xet_nen` | `r927_trang_thai_sandbox_moi_nhanh` | 10 | TinHieuChotCa: killed |
| `r27_tt_bo_qua_loi` | `r927_trang_thai_sandbox_moi_nhanh` | 10 | TinHieuChotCa: killed |
| `r27_tt_bo_qua_con_chay` | `r927_trang_thai_sandbox_moi_nhanh` | 10 | TinHieuChotCa: killed |
| `r27_tt_khong_doi_json` | `r927_trang_thai_sandbox_moi_nhanh` | 10 | TinHieuChotCa: killed |
| `r27_tt_bo_qua_so_lenh` | `r927_trang_thai_sandbox_moi_nhanh` | 10 | TinHieuChotCa: killed |
| `r27_dem_moi_item` | `r927_trang_thai_sandbox_moi_nhanh` | 10 | TinHieuChotCa: killed |
| `r27_khoa_khong_gom_cmdline` | `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` | 10 | TinHieuChotCa: killed |
| `r27_quet_doc_environ` | `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` | 10 | TinHieuChotCa: killed |
| `r27_lenh_run_khong_lay_mau` | `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 10 | TinHieuChotCa: killed |
| `r27_lenh_run_khong_ghi_so` | `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 10 | TinHieuChotCa: killed |
| `r25_ghi_moi_dong_tron` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r25_ghi_moi_dong_tron` | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 10 | TinHieuChotCa: killed |
| `r25_cho_phep_theo_tien_to` | `r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace` | 10 | TinHieuChotCa: killed |
| `r25_cho_phep_ca_dong_cut` | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 10 | TinHieuChotCa: killed |
| `r26_cho_phep_cat_moi_CRLF` | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 10 | TinHieuChotCa: killed |
| `r25_bo_go_ansi` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r25_khung_moi_target` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r25_moi_su_kien` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r25_nhan_id_model_rong` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r25_gop_theo_id` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r25_bo_dem_mat` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r25_bo_dem_mat` | `r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE` | 10 | TinHieuChotCa: killed |
| `r26_bo_dem_mat_nhieu_doan` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 10 | TinHieuChotCa: killed |
| `r26_bo_dem_mat_nhieu_doan` | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 10 | TinHieuChotCa: killed |
| `r26_bo_dem_mat_nhieu_doan` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_phan_loai_theo_token` | `r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE` | 10 | TinHieuChotCa: killed |
| `r25_parse_khong_can_ca_dong` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 10 | TinHieuChotCa: killed |
| `r25_doc_khong_tran` | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 10 | TinHieuChotCa: killed |
| `r25_xa_ong_khong_tran` | `r925_bo_loc_hong_xa_ong_co_gioi_han` | 10 | TinHieuChotCa: killed |
| `r26_bo_duoi_vat` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_khong_bo_khoang_trang` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_bo_xac_nhan_su_kien_khac` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 10 | TinHieuChotCa: killed |
| `r26_dau_dong_khong_noi` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 10 | TinHieuChotCa: killed |
| `r26_loai_khong_utf8_thay_the` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_khong_ro_khong_dem` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_khong_ro_moi_dong_dai` | `r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat` | 10 | TinHieuChotCa: killed |
| `r26_utf8_thay_the` | `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 10 | TinHieuChotCa: killed |
| `r25_noi_rust_log_thua_ke` | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 10 | TinHieuChotCa: killed |
| `r25_khong_bat_trace` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khi_loc_hong` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khi_loc_hong` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khi_ong_con_mo` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khi_ong_con_mo` | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khi_mat` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khi_mat` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 10 | TinHieuChotCa: killed |
| `r26_DO_DUOC_khi_khong_ro` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khong_khung` | `r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien` | 10 | TinHieuChotCa: killed |
| `r25_DO_DUOC_khong_khung` | `r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m` | 10 | TinHieuChotCa: killed |
| `r25_so_khong_chuyen_loi` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 10 | TinHieuChotCa: killed |
| `r25_so_khong_chuyen_mat` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 10 | TinHieuChotCa: killed |
| `r25_so_khong_chuyen_mat` | `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_so_khong_chuyen_khong_ro` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r25_bo_chot_luong` | `r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup` | 10 | TinHieuChotCa: killed |
| `r26_lay_mau_lai_luong_muon` | `r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai` | 10 | TinHieuChotCa: killed |
| `r26_mac_dinh_chua_chot_la_xong` | `r926_ghi_so_truoc_khi_chot_khong_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r25_doc_ong_khong_han` | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_dong_tep_truoc_chot` | `r926_ket_thuc_chot_luong_TRUOC_khi_dong_tep` | 10 | TinHieuChotCa: killed |
| `r26_dong_tep_truoc_chot` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_san_xuat_dong_tep_truoc` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_tep_stderr_co_dem` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r25_bo_loc_hong_khong_xa_ong` | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 10 | TinHieuChotCa: killed |
| `r26_xa_khong_dem` | `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 10 | TinHieuChotCa: killed |
| `r25_bo_loc_hong_khong_ghi_loi` | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 10 | TinHieuChotCa: killed |
| `r26_tep_dong_khong_dem` | `r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem` | 10 | TinHieuChotCa: killed |
| `r26_ghi_loi_khong_dem` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 10 | TinHieuChotCa: killed |
| `r26_ghi_dem_ca_doan` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 10 | TinHieuChotCa: killed |
| `r26_ghi_khong_lap` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 10 | TinHieuChotCa: killed |
| `r26_luong_hong_lot_ra` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_luong_hong_khong_dong_ong` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_luong_hong_khong_ghi_loi` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_cho_luong_chua_chay` | `r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_khong_ro_khong_doi_json` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_doc_tron_khong_parse_bo_qua` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_ghi_bo_chot_0_byte` | `r926_ghi_het_dem_dung_phan_chua_ghi` | 10 | TinHieuChotCa: killed |
| `r26_mot_doan_bo_dieu_kien_so_doan` | `r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han` | 10 | TinHieuChotCa: killed |
| `r26_doc_tron_khong_ro_ca_su_kien_khac` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 10 | TinHieuChotCa: killed |
| `r26_doc_tron_khong_ro_khong_doi_json` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_doc_tron_bo_token` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r26_tien_to_ung_vien_tha` | `r926_ket_dong_tien_to_ung_vien_ma_khong_token_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_tien_to_khong_tran` | `r926_tien_to_dong_dai_co_tran_va_noi_qua_doan` | 10 | TinHieuChotCa: killed |
| `r26_tien_to_bo_max` | `r926_tien_to_dong_dai_co_tran_va_noi_qua_doan` | 10 | TinHieuChotCa: killed |
| `r26_token_khong_dinh` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_khong_dat_lai_moi_dong` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r26_bo_dong_cut_EOF` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 10 | TinHieuChotCa: killed |
| `r26_response_khong_kiem_object` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 10 | TinHieuChotCa: killed |
| `r26_id_khong_kiem_chuoi` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 10 | TinHieuChotCa: killed |
| `r26_id_khong_strip` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 10 | TinHieuChotCa: killed |
| `r26_model_khong_kiem_chuoi` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 10 | TinHieuChotCa: killed |
| `r26_model_khong_strip` | `r926_response_hong_tung_vi_tu_tinh_mat_khong_loi` | 10 | TinHieuChotCa: killed |
| `r26_ket_thuc_khong_dong_tep` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_khong_ghi_so` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_prefix_decoded` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_rv5_dedup_response_id` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_dedup_whole` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_frame_match_guard` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r26_rv5_parsed_model_guard` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r26_rv5_prefix_match_guard` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_rv5_first_chunk_capture` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_rv5_classify_only_at_lf` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 10 | TinHieuChotCa: killed |
| `r26_rv5_reason_guard` | `r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai` | 10 | TinHieuChotCa: killed |
| `r26_rv5_rust_override_record` | `r925_rust_log_thua_ke_bi_GHI_DE_khong_noi` | 10 | TinHieuChotCa: killed |
| `r26_rv5_exception_valueerror` | `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_old_late_production_latch` | `r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv5_optional_counter_init` | `r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc` | 10 | TinHieuChotCa: killed |
| `r26_rv5_retain_caller_counter` | `r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv5_candidate_search` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv5_target_only` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r26_rv5_receive_position_only` | `r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien` | 10 | TinHieuChotCa: killed |
| `r26_rv5_lf_detection` | `r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_codex_mode_disabled` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_codex_env_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_codex_reader_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_codex_pipe_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv5_finish_object_guard` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv6_a_ansi_bo_tham_so_hoi` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_a_ansi_bo_trung_gian` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_a_ansi_chi_m` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_b_bo_neo_dau` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv6_b_moc_thoi_gian` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv6_b_muc_TRACE` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_b_khoang_truoc_TRACE` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_b_dau_cach_sau_message` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv6_c_neo_cuoi` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_c_doi_tuong_json` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_d_khoa_type` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_rv6_d_khong_escape` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_rv6_d_dong_nhay` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_rv6_d_khoang_sau_ngoac` | `r926_tien_to_dong_dai_co_tran_va_noi_qua_doan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_d_khoang_hai_cham` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 10 | TinHieuChotCa: killed |
| `r26_rv6_e_bo_completed` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv6_e_cham_bat_ky` | `r926_ngu_phap_khung_tung_thanh_phan` | 10 | TinHieuChotCa: killed |
| `r26_rv6_f_chi_dau_cach` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv6_g_duoi_ngan` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv6_h_luong_khong_ansi` | `r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv6_i_tran_dau_nho` | `r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran` | 10 | TinHieuChotCa: killed |
| `r26_rv6_j_bo_CRLF` | `r926_cho_phep_chi_dung_LF_hoac_mot_CRLF` | 10 | TinHieuChotCa: killed |
| `r26_rv6_l_su_kien_bo_completed` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv6_m_dau_json_bo_ngoac` | `r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO` | 10 | TinHieuChotCa: killed |
| `r26_rv7_luong_doc_khong_daemon` | `r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC` | 10 | TinHieuChotCa: killed |
| `r26_rv7_tep_stderr_van_ban` | `r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat` | 10 | TinHieuChotCa: killed |
| `r26_rv7_khong_chup_ket` | `r926_ghi_so_chup_rieng_ket_loi_dem` | 10 | TinHieuChotCa: killed |
| `r26_rv7_khong_chup_loi` | `r926_ghi_so_chup_rieng_ket_loi_dem` | 10 | TinHieuChotCa: killed |
| `r26_rv7_khong_chup_dem` | `r926_ghi_so_chup_rieng_ket_loi_dem` | 10 | TinHieuChotCa: killed |
| `r25_loc_ca_luot_khong_phai_codex` | `r925_khong_phai_codex_giu_nguyen_so_va_stderr` | 10 | TinHieuChotCa: killed |

Matrix totals: `{"cases": 48, "passed": 48, "mutants": 163, "killed": 163, "targets": 173, "signals": 173, "rc": 0}`.

## Final re-measurement counts

| Family | Cases passed / required | Case rc | Mutants killed / required | Named-target signals / required |
|---|---:|---:|---:|---:|
| `r925_*` / `r25_*` | 15/15 | 0 each | 25/25 | 32/32 |
| `r926_*` / `r26_*` | 23/23 | 0 each | 99/99 | 102/102 |
| `r927_*` / `r27_*` | 10/10 | 0 each | 39/39 | 39/39 |

**48/48 cases passed; 163/163 mutants killed; 173/173 named-target signals.** Zero skips, timeouts, surviving mutants, unrelated exceptions, or non-target signals. Matrix driver **rc 0**; all baseline case commands **rc 0**; all strict mutant children **rc 10** (the explicitly assigned kill code). Every mutant anchor was unique and every copy compiled. The complete signal/traceback audit is `review-r27e.TYUXfY/signal-audit.json`.

Matrix command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 CODEX_HOME=/wp748-r27e-noauth-TYUXfY TMPDIR=/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27e/review-r27e.TYUXfY GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27e.TYUXfY/run_matrix.py` — **rc 0**. Selected test configuration was verified nonexistent before and after; it was never created. No default authentication preflight was used for test launches.

`r926_dot_bien_tu_sinh_moi_thanh_phan_regex` ran through the requested CLI, **rc 0**. Its enforced inventory is **207 variants across 7 regex constants: 200 killed through TinHieuChotCa, 7 explicitly enumerated equivalents**, no unexpected survivor or unrelated-exception credit. These generated variants are separate from the 163 hand-written `DOT_BIEN` entries. The case verifies per-regex counts and the exact equivalent-survivor set.

Mutation-evidence qualification: `r26_rv7_tep_stderr_van_ban` triggers the named target's launch-success assertion because its text mode with zero buffering prevents the output file from opening. This is a direct consequence of that mutation, not evidence of downstream text-stream filtering. Late-close mutants can fail their close-timing fixture assertion before receipt status is checked. These signals meet the specified rule; no arbitrary process failure was counted as a kill.

## Decision and closure

**Changes requested: 0 P0, 0 P1, 1 P2, 0 P3.** The specific R27-PID-04e within-scan defect is closed. R27-PID-04f is a remaining manifestation of the same `sandbox-process-identity-race` class at the boundary between scans. The owner's narrowing decision is accepted, including ordinary-zombie false downgrades; the finding concerns success after an observed change.

| Prior finding | Closure on this SHA | Evidence |
|---|---|---|
| R27-PID-04e | **Closed — measured** | `to_tien_doi_cha` executes one scan, latches `DanhTinhDoi`, and writes `KHONG_DO_DUOC`. The dedicated `r27_to_tien_chi_so_bd` mutant fails in precisely this scenario: its named target raises `TinHieuChotCa`, strict child rc 10, with `loi=[]` and `DO_DUOC` in the diagnostic. The queue carries `(pid, (ppid,starttime))` for root and every descendant; line 2092 compares the full reread tuple. |
| R27-PID-04c | **Stayed closed under the owner decision** | Existing `cha_zombie` fixture produces `DanhTinhDoi` / `KHONG_DO_DUOC` in one scan. The receipt explicitly documents conservative lifecycle downgrades. This accepted tradeoff is not reopened. |
| R27-PID-04d | **Stayed closed** | Existing `goc_khong_ghim` fixture records `GocKhongGhimDuoc`; initial and final pin are both `None`; the later scan cannot recover a missing initial pin. Both late-pin mutants are killed. |
| R27-PID-04 / 04b | **Previously repaired paths stayed closed; class remains open** | Current-child tuple changes, root starttime reuse, and intermediate-ancestor starttime changes are rejected in the first scan. Every current-chain reread is now compared in full, before enqueue and deduplication. Cross-scan ancestry history remains unvalidated; see 04f. |
| R27-ALLOW-01 | **Stayed closed** | Fixed semantic vocabularies still cover program/flag names, paths, profile enums and capabilities. Existing secret-bearing BWRAP/CLS fixtures pass through raw-byte decoding, summary and receipt writing: 2 summaries, 0 strings outside the fixed vocabulary, 0 supplied secret markers. Production receipt and named mutants pass the requested checks. Raw argv is not serialized. |
| R27-PARSE-02 / 02b | **Stayed closed** | Arity and actual cmdline decoding cases pass. Empty arguments are preserved; unknown options, missing values/boundaries and missing terminal NUL remain uncertain; option values are not reinterpreted as flags. Corresponding named mutants are killed. |
| R27-PROC-03 | **Stayed closed** | Existing denied-read scenario latches `PermissionError` and downgrades despite a prior observation. Independent `_stat` checks propagate PermissionError/OSError and treat only FileNotFoundError/ProcessLookupError as disappearance. Broad-error-swallow mutant is killed. |
| R27-TEST-05 | **Stayed closed** | State case passes on Linux and unchanged under Windows/Darwin platform mocks. Actual constructor/start/stop/write under those mocks produces no sampler thread and `KHONG_DO_DUOC`. These are Linux-hosted simulations, not native platform CI. |

Closure observation command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 CODEX_HOME=/wp748-r27e-noauth-TYUXfY TMPDIR=<review scratch> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27e.TYUXfY/closure_observations.py` — **rc 0**. It instruments the existing fixture without changing its injected scenarios or assertions. All seven scenarios execute one scan and end `KHONG_DO_DUOC`. The complete observations and source AST extraction are in `review-r27e.TYUXfY/closure-observations.json`. Seeded observations in that fixture are test data, not evidence of actual namespace/seccomp enforcement.

## New finding

### R27-PID-04f — P2 — changed ancestry observed in a later scan is accepted without comparison

Stable class: `sandbox-process-identity-race`. Location: **`.claude/dev/launcher.py:2060`**, with graph rebuilding at 2071–2080, deduplication at 2097–2099 and success at 2130–2131. Coverage gap: `.claude/dev/launcher_test.py:11438` creates a new sampler per scenario, and line 11442 performs only one scan.

**Scenario:** scan 1 validates root R → A → B while B has `(ppid=A,starttime=s)` and records a sandbox observation. Between scans, A exits and B is reparented, retaining its PID/starttime; B remains readable throughout. Scan 2 actually reads B's new `(ppid=X,starttime=s)` into `info`. If X is outside R's tree, B is omitted from traversal; if X is another ancestor inside R's tree, B is validated against the newly rebuilt graph. Neither route compares the newly observed parent edge to the edge accepted in scan 1. With no other error, earlier `thay` remains, `loi` stays empty, and `ghi_so` can return `DO_DUOC`.

**Why this violates the accepted decision:** both differing parent values were read by this sampler, and the process whose identity changed has not vanished. The user-supplied rule requires every observed identity deviation, including normal reparenting, to produce uncertainty. The rule is enforced within a scan but not across scans. This is not a demand to detect an unobserved event between reads, to prove every command is sandboxed, or to distinguish benign zombies. It does not claim the earlier sandbox observation was fabricated; it identifies a success state after the later observed deviation that the narrowed contract requires to dominate that observation.

**Evidence:** static control/data-flow review on the exact SHA, supported by the recorded AST extraction: `info`, `con`, and `hang` are local and rebuilt on every `_quet`; the only persistent non-root deduplication key is `(pid,starttime,cmdline)`, which omits the old parent edge and never produces a mismatch error. `thay` and errors persist, so the no-error success branch remains reachable. Instrumenting the unchanged identity fixture confirms that all seven scenarios cover one scan only. This new scenario was **not executed**; no new exploit payload or identity-fault fixture was authored, as instructed.

**Fix direction:** preserve the last validated identity/parent tuple for previously observed live descendants in `_LayMauSandbox`, and reconcile newly read tuples before rebuilding/filtering the descendant tree. A changed tuple must latch `DanhTinhDoi` even when the new parent removes the PID from the traversed subtree. Keep the current full-chain checks, failed-initial-pin behavior, and the explicitly accepted disappearance exception. Do not silently replace an old tuple with a new one before checking it.

**Regression direction:** use one sampler over at least two scans: first establish an observation and ancestry; next present the same still-readable descendant with unchanged starttime and changed ppid, both outside and inside the root's subtree. Require `DanhTinhDoi` / `KHONG_DO_DUOC` immediately and after a later clean scan. A dedicated mutant that drops the retained comparison or overwrites the old tuple first must be killed by the named target's `TinHieuChotCa`. Preserve a control for unchanged ancestry and for an actually vanished current process. These are descriptions only, not new payloads.

**Remediation risks:** retain only the identity information needed for reconciliation, retire entries consistently with the approved disappearance rule, avoid unbounded history, and prevent PID reuse from being mistaken for a silently refreshed identity. Conservative lifecycle downgrades are accepted; accidentally erasing a latched deviation or broadly treating every historical PID as permanently live would be regressions.

## Full-delta/spec assessment

Reviewed the full delta against master `356eb262cbd491b9599b56d5f7c41c93dd9a28a1`, both files, and the frozen spec plus supplied owner decisions. The round-5 commit changes the chain representation/comparison, adds its fixture/mutant, and compresses the recursive test vocabulary walker; that walker still enumerates dict keys/values and list members. No independent additional P0–P3 class was identified.

Effort comes only from accepted server response frames; missing/invalid effort is counted before model deduplication, distinct values preserve encounter order, and model uncertainty prevents effort success. Immutable tuples avoid a mutable counter list being shared with the writer snapshot. There is no CLI/config fallback. Existing model/filter tests and their strict mutants remain effective.

Sandbox output is reduced to fixed semantic values. The option arity tables and raw decoder preserve boundaries. Production sampling reads only `/proc/*/stat` and descendant cmdline; the real-process fixture checks the permitted read set, and the existing environ-reading mutant is killed. That mutant reads only credential-free test-process environments. Sampling waits 0.2 s between scans; scan duration adds to the interval, so no hard wall-clock cadence under arbitrary host load was proved. Thread shutdown is bounded; recorded errors, a live sampler at closure, unsupported platforms, and uncertain argv prevent `DO_DUOC`. Missing stdout JSON evidence does not become a claim that no command ran.

The within-scan sweep covers child reread, every ancestor tuple (root included), disappearance, ordinary error propagation, early returns, enqueue order and deduplication. Recorded errors are never cleared, and the writer checks them before success. The remaining actionable omission is loss of previously validated parent edges between scans, described above. Initial root pinning still retains only starttime; in the production call the root is the launcher's direct child, so parent loss normally terminates the very launcher that would write the receipt. That mechanically unused initial ppid was not inflated into a separate finding without a viable production scenario.

Receipt limits still explicitly acknowledge short-lived commands, self-declared argv[0], and conservative lifecycle downgrades. Python fixtures named bwrap exercise observation and serialization, not actual namespace/seccomp enforcement. Fixed path labels are more detailed than the frozen spec's original cwd/khac shorthand, as already accepted in earlier rounds; they do not copy arbitrary path components.

## Lint and other acceptance limits

Pinned local `python3 -m ruff` reports **0.15.15**, matching the version recorded in CI. On exact base/head blob copies outside `src/`, `check --isolated --no-cache --output-format json --select F` returns **rc 1 on both**, with the same 5 F841 diagnostics. Default isolated rules return **rc 1 on both**, with the same 145 diagnostics (113 E702, 23 E701, 5 F841, 2 E741, 2 E731). Normalization uses file/rule/message/source-line/column rather than shifted line numbers: **0 added / 0 removed** in both comparisons. This is zero lint delta, not absolute lint cleanliness.

`python3 -B review-r27e.TYUXfY/static_checks.py` with the isolated environment — **rc 0**. Both exact files compile. `git -C src diff --check 356eb262cbd491b9599b56d5f7c41c93dd9a28a1 c6f6ef6cc6555c01b008a7c22266589b454d1653` — **rc 0**. Full commands and outputs are in `review-r27e.TYUXfY/static-results.json`; full delta in `full-delta.patch`.

Tool-selection correction: the first lint command used PATH's `/root/.local/bin/ruff`, version 0.16.8. Its default rules produced 231 base / 259 head diagnostics (+28), causing the initial comparison driver to return **rc 1**; `--select F` was already zero delta. That measurement is retained in `static-results-unpinned.json` and is not reported as the pinned CI result. The locally installed Python module provided the required 0.15.15; no package download or source change was needed.

Not run/not independently verified: the full unrelated launcher suite, native Windows/macOS lanes, live CI or worker/land gates, actual Codex execution, actual sandbox enforcement, and the outer completed execution receipt. The spec's full-suite and Windows acceptance are not claimed satisfied by the requested scoped matrix. No GitHub access is available/permitted; no commit, push, GitHub comment, credential use, or new exploit payload occurred. No additional Codex/model calls or subagents were started. Fixture executables named codex are Python test doubles.

Size: exactly **2 files / 800 added lines / 1 deleted line**, meeting the user-supplied raised cap associated with `#748 issuecomment-6408141574`. This is **Codex call 5 of 10** per the user; GitHub authority, live branch publication status, current lease/heartbeat state, and external call history remain unverified.

## Final source integrity

Final HEAD/tree and single parent remain exactly the requested OIDs; master ancestry check rc 0, full-clone check rc 0, detached-HEAD check rc 1 as expected. Final tracked/untracked/ignored status, worktree diff and index diff are empty, all rc 0. Both reviewed files match their Git blobs byte-for-byte; no source bytecode cache exists. Exact commands, rc and file SHA-256 values are retained in `review-r27e.TYUXfY/final-integrity.json`. Endpoint checks establish no observed source delta; they do not certify absence of every possible transient write. All reviewer artifacts and test fixture repositories are outside `src/`.

Runtime tools report Linux 6.18.44 / Python 3.13.16. The session reports workspace-write sandbox policy and approval policy never; these are configuration reports, not an independent kernel-enforcement measurement. Exact serving model/build, effort, session/launcher identity and outer execution-receipt authenticity cannot be independently verified here. This verdict does not self-certify cross-provider assurance or land approval.

Completed UTC: 2026-10-26T06:01:01.115531+00:00

VERDICT: changes_requested
