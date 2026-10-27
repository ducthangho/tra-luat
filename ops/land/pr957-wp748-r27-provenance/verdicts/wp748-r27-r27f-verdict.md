# Independent review — WP748 r27 (spec r27), round 6

**Changes requested: 0 P0, 0 P1, 1 P2, 0 P3.** R27-PID-04f's root-present scenarios are repaired; R27-PID-04g identifies an early return that still bypasses an observed descendant change when the root has disappeared. Re-measured on the requested SHA: **50/50 cases, 167/167 mutants, 177/177 named-target signals**. Merge isolation and size checks passed.

Reviewer: OpenAI Codex (`openai_codex`), identified by the session developer runtime as an agent based on GPT-6. Observed surface: tool-enabled Codex agent with local shell execution; transport: machine/local. Invocation through `launcher.py run` and outer `codex_cli` routing are user-reported. The exact deployed serving model/build, actual effort, completed outer execution receipt and provider/session authenticity cannot be independently verified from inside this run.

Review Class: sensitive. Started UTC: 2026-10-27 00:38:00 UTC. User reports call 6 of 10. No GitHub access is available/permitted; external call accounting, owner comments and unpushed status are not independently verified. No credentials are used.

Identity verified before substantive review:

- SHA `60b3055c5eb999dff196aca42c53fa98c3eb641d`.
- Tree `029f054aeef6cea2cc3c74c80197d2ea25b0b87f`.
- Parents `fc5d235eaaf6af910ecfd81871ff19411c81f069` and `3e973a03b151e37cd402e0a723816eeaa8247193`.
- `git -C src rev-parse --is-shallow-repository HEAD HEAD^{tree}`: rc 0, false, expected OIDs.
- `git -C src show -s --format='%H%n%T%n%P%n%D' HEAD`: rc 0, expected identities, detached HEAD.
- `git -C src symbolic-ref -q HEAD`: rc 1 as expected for detached HEAD (initial shell wrapper normalized this expected status to rc 0).
- `git -C src status --porcelain=v1`: rc 0, empty.
- `git -C src branch -a --contains HEAD`: rc 0, only detached HEAD; local branch provenance is user-reported, and the hash is the reviewed identifier.

Frozen spec: `git -C src show origin/ops/wp748-r27-g27-lease:ops/specs/wp748-r27-launcher-effort-sandbox.md`, rc 0. SHA-256 matches `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd`. Lease read from the same ref, rc 0: r27/g27, two-file write set; expiry 2026-10-27T00:18:51Z has passed. Per the explicit review instruction, pending owner g28 renewal does not block this read-only review or this Codex call. No lease is renewed here.

The supplied owner narrowing decision governs: every observed identity deviation requires `DanhTinhDoi` and `KHONG_DO_DUOC`, including ordinary zombie reparenting; disappearance/different starttime for the process being read is the accepted benign case. The supplied raised size cap is ≤2 files / ≤850 added lines, owner #748 issuecomment-6409625815; the frozen spec's older cap is superseded for this review.

Initial size measurement: `git -C src diff --numstat 3e973a03b151e37cd402e0a723816eeaa8247193 60b3055c5eb999dff196aca42c53fa98c3eb641d`, rc 0: launcher.py +351/-1; launcher_test.py +493/-0. **2 files / 844 added / 1 deleted; within cap.**

Cloud runtime skill read; no `environment_status` tool is available. No network or credential discovery performed. Scratch: `review-r27f.VechV5/`, outside `src/`.

## Re-measured cases

Each row uses `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1` on the verified SHA, with a minimal credential-free environment, bytecode disabled, and TMPDIR outside src. Full commands/output/rc are in `review-r27f.VechV5/matrix-results.json`.

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
| `r952_auth_json_truong_la_kieu_object_van_doc_duoc` | 0 | passed |
| `r927_effort_do_duoc_tu_khung_may_chu` | 0 | passed |
| `r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC` | 0 | passed |
| `r927_effort_khong_do_duoc_khi_model_khong_do_duoc` | 0 | passed |
| `r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep` | 0 | passed |
| `r927_ngu_phap_sandbox_theo_bang_so_doi_so` | 0 | passed |
| `r927_trang_thai_sandbox_moi_nhanh` | 0 | passed |
| `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` | 0 | passed |
| `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` | 0 | passed |
| `r927_canh_cha_doi_giua_hai_luot_quet` | 0 | passed |
| `r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that` | 0 | passed |
| `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` | 0 | passed |

## Re-measured named-target mutants

Only checked-in DOT_BIEN replacements are used, each on a distinct temporary launcher copy. Every anchor is required to be unique and every copy compiles. Strict worker rc 10 means TinHieuChotCa with the named target code object in the traceback. rc 0 = survivor, 11 = skip, 12 = unrelated exception, 13 = non-target signal, 14 = missing/ambiguous target, 124 = timeout. A mutant is killed only if every declared target yields rc 10.

Command: `python3 -B review-r27f.VechV5/run_matrix.py worker <temporary-launcher.py> <named-target>`.

| Mutant | Named target | rc | Result |
|---|---|---:|---|
| `r952_bo_ep_kieu_truong_credential` | `r952_auth_json_truong_la_kieu_object_van_doc_duoc` | 10 | TinHieuChotCa: killed |
| `r952_quay_ve_ep_moi_truong_la_chuoi` | `r952_auth_json_truong_la_kieu_object_van_doc_duoc` | 10 | TinHieuChotCa: killed |
| `r27_canh_khong_doi_chieu` | `r927_canh_cha_doi_giua_hai_luot_quet` | 10 | TinHieuChotCa: killed |
| `r27_canh_khong_ghi` | `r927_canh_cha_doi_giua_hai_luot_quet` | 10 | TinHieuChotCa: killed |
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

Matrix totals: `{"cases": 50, "passed": 50, "mutants": 167, "killed": 167, "targets": 177, "signals": 177, "rc": 0}`.

## Final re-measurement counts

| Family | Cases passed / required | Case rc | Mutants killed / required | Named-target signals / required |
|---|---:|---:|---:|---:|
| `r925_*` / `r25_*` | 15/15 | 0 each | 25/25 | 32/32 |
| `r926_*` / `r26_*` | 23/23 | 0 each | 99/99 | 102/102 |
| `r927_*` / `r27_*` | 11/11 | 0 each | 41/41 | 41/41 |
| `r952_*` / `r952_*` | 1/1 | 0 each | 2/2 | 2/2 |

**50/50 cases passed; 167/167 mutants killed; 177/177 named-target signals.** Matrix driver **rc 0**. All baseline commands returned **rc 0** with exactly `1/1 qua, 0 bo qua, 0 hong`; every mutant child returned **rc 10**, assigned only by the strict worker after catching the named target's `TinHieuChotCa`. No skipped cases, timeouts, survivors, unrelated exceptions, non-target signals or fixture-discovery failures received kill credit. All mutation anchors were unique and copies compiled.

Matrix command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 CODEX_HOME=/wp748-r27f-noauth-VechV5 TMPDIR=<absolute review-r27f.VechV5> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27f.VechV5/run_matrix.py` — **rc 0**. `CODEX_HOME` selects a verified nonexistent test configuration path; it was still nonexistent after the matrix. No runtime credential configuration was changed. All fixture executables named codex are test doubles, and synthetic r952 token strings are inert.

`python3 -B review-r27f.VechV5/audit_results.py` — **rc 0**. The audit checks complete inventory coverage, per-target return codes, signal identity, named target traceback frame, and absence of fixture-discovery signals. Full traces/messages: `signal-audit.json`. Full argv, output and duration for every command: `matrix-results.json`; progress log: `matrix.log`.

`r926_dot_bien_tu_sinh_moi_thanh_phan_regex` ran through the requested CLI and returned **rc 0**. Its enforced inventory is **207 variants across 7 regex constants: 200 killed via TinHieuChotCa and 7 explicitly enumerated equivalents**. The case checks exact per-constant counts, the exact equivalent-survivor set and absence of unrelated exceptions. These generated variants are separate from the 167 hand-written DOT_BIEN mutants.

Mutation-evidence qualification: `r26_rv7_tep_stderr_van_ban` triggers its target's launch-success assertion because the changed text mode with zero buffering prevents the output file from opening. Late-close mutants can trigger a close-timing assertion before receipt status is checked. These are named-target signals caused by the mutations and satisfy the requested kill rule; they are not credited as proof of downstream behavior beyond the assertion actually reached.

## Merge resolution and packet isolation

`python3 -B review-r27f.VechV5/merge_checks.py` — **rc 0**. Full commands/rc and comparisons are retained in `merge-results.json`; original patches are `full-delta.patch`, `merge-resolution.patch`, `round6-fix.patch`, and `master-r952.patch`.

- `git -C src show --cc 60b3055c5eb999dff196aca42c53fa98c3eb641d`, rc 0: the combined conflict hunk preserves the incoming r952 entries and the packet's r27 tests/mutants.
- Merge base of the two parents is `9372ecd93bd95350c90dfc75d3f0d014b4f932ed`. For **each** of the two packet files, the ordered added/deleted source lines in `9372ecd..fc5d235` equal those in `3e973a0..60b3055` exactly. The converse comparison also holds: the master-side edits `9372ecd..3e973a0` equal `fc5d235..60b3055` exactly. Context/line-number changes are excluded; no added/deleted code is excluded.
- The full delta against master changes only `.claude/dev/launcher.py` and `.claude/dev/launcher_test.py`. Exact master and fix `60b9209bc91138b4b0a82518d98ae84543dd61ad` are ancestors, both `merge-base --is-ancestor` commands rc 0.
- AST equality independently confirms `_doc_auth_bytes` and `_credential_id` match master, while `_LayMauSandbox`, effort parsing/counting/conclusion, stderr writer, sandbox summary and `lenh_run` match parent 1.
- The r952 change restricts string-type checking to the four consumed token fields, preserving extra metadata. It neither supplies nor changes effort/sandbox observations. It does share the enclosing launcher module and pre-launch credential path, but r27 adds no call/data flow to `_doc_auth_bytes`; the merged auth functions are unchanged from master. The r952 fixture uses only in-memory `INERT` data. Its case and both mutants were re-measured on this SHA. No r952/r27 merge interaction was identified.

## Comparison with prior findings

History reviewed: `VERDICT_R27A.md` through `VERDICT_R27E.md`. Round 5's open finding is R27-PID-04f on `c6f6ef6cc6555c01b008a7c22266589b454d1653`; this review evaluates its fix on the requested merged head. The owner narrowing decision is accepted, including ordinary-zombie false downgrades.

| Finding | Closure on this SHA | Evidence |
|---|---|---|
| R27-PID-04f | **Reported root-present scenarios closed — measured; class remains open** | One sampler per scenario, two scans: `ra_ngoai` and `vao_goc` retain validated edges after scan 1, then latch exactly `DanhTinhDoi` in scan 2. The independent receipt observation yields `KHONG_DO_DUOC` with `DanhTinhDoi` as its reason. The unchanged control has no errors in either scan. `r27_canh_khong_doi_chieu` and `r27_canh_khong_ghi` both fail the named target at `ra_ngoai: loi=[]`, strict worker rc 10. Root absence still bypasses the reconciliation: R27-PID-04g below. |
| R27-PID-04e | **Stayed closed — ĐÃ VÁ THẬT for the reported within-scan defect** | Existing `to_tien_doi_cha` records `DanhTinhDoi` and writes `KHONG_DO_DUOC` in one scan. `r27_to_tien_chi_so_bd` raises its named target's `TinHieuChotCa`, rc 10, specifically for this scenario with erroneous `DO_DUOC`. Full `(ppid,starttime)` tuples of every reread ancestor are compared at launcher.py:2100. |
| R27-PID-04c | **Stayed closed under owner decision** | Existing `cha_zombie` scenario records `DanhTinhDoi` and `KHONG_DO_DUOC`; documented conservative lifecycle downgrades remain. This accepted tradeoff is not reopened. |
| R27-PID-04d | **Stayed closed** | Existing `goc_khong_ghim` records `GocKhongGhimDuoc`; the pin remains None and the later scan cannot adopt a new identity. Both late-pin mutants are killed. |
| R27-PID-04 / 04b | **Previously repaired paths stayed closed; class not closed** | Current-child identity changes, root starttime reuse, intermediate-ancestor starttime changes, and ancestor-edge rereads are rejected before enqueue/deduplication. The seven existing identity/error scenarios each reach `KHONG_DO_DUOC` in one scan. R27-PID-04g is another missed comparison in the same class. |
| R27-ALLOW-01 | **Stayed closed** | Fixed semantic vocabularies cover program/option names, path labels, profile types/access/network/special kinds and capability summaries. Existing secret-bearing BWRAP and CLS fixtures passed raw-byte decoder → summary → receipt: 2 summaries, 0 strings outside the fixed vocabulary, no supplied secret markers. Named cases and mutants passed. Raw argv is not serialized. |
| R27-PARSE-02 / 02b | **Stayed closed** | Arity and raw-cmdline cases pass; values are consumed according to arity, interior empty arguments are preserved, and unknown options/missing values/missing boundaries/missing terminal NUL remain uncertain. Named mutants are killed. |
| R27-PROC-03 | **Stayed closed** | Existing denied cmdline read latches `PermissionError` and overrides a prior observation. `_stat` catches only FileNotFoundError/ProcessLookupError; other failures propagate to `_chay`'s error list. The broad-error-swallow mutant is killed. |
| R27-TEST-05 | **Stayed closed** | State case passes on Linux and unchanged under Windows/Darwin platform mocks. Constructor/start/stop/write under those mocks creates no sampler thread and reports `KHONG_DO_DUOC`. These are Linux-hosted simulations, not native platform CI. |

Closure observation command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 CODEX_HOME=/wp748-r27f-noauth-VechV5 TMPDIR=<absolute review-r27f.VechV5> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27f.VechV5/closure_observations.py` — **rc 0**. `closure-observations.json` records the existing fixtures without changing their injected faults or assertions. The new two-scan fixture does not seed a sandbox observation or assert a receipt itself: its control receipts are unknown because stdout is empty, not because of an identity error. The unchanged status case separately establishes that a latched error dominates a previous observation. Those limits are not hidden by the aggregate pass count.

## New finding

### R27-PID-04g — P2 — root disappearance bypasses reconciliation of already-read live descendants

Stable class: **`sandbox-process-identity-race`**, continuing R27-PID-04/04b/04e/04f. Primary location: **`.claude/dev/launcher.py:2068`**; skipped comparison begins at 2072; success is at 2139. Coverage gap: **`.claude/dev/launcher_test.py:11501`** roots every new two-scan scenario in the still-running test process.

**Scenario:** an earlier scan validates a descendant D, caches `(ppid=R,starttime=s)` in `self.canh`, and records a sandbox observation. The launched root R then exits and is reaped while D survives and is reparented. A scan already in progress reads D's fresh `(ppid=X,starttime=s)` into `info` and finds R absent. The return at 2068–2069 happens before the retained-edge loop. The changed value for the still-identical D has been read, but never compared. `self.loi` remains empty and the earlier observation remains. After the sampler stops, `ghi_so` can therefore take its `DO_DUOC` branch.

This can occur at ordinary shutdown: `lenh_run` waits/reaps the root at 2348/2352, then calls `sandbox.ket_thuc(5)` at 2372. Setting the stop event does not cancel an in-flight `_quet`; that scan can finish with a root-absent snapshot. The condition is a previously observed descendant remaining present with the same starttime and a changed ppid. Root absence by itself is not being proposed as an error.

**Why actionable under the accepted decision:** the vanished process is R, whereas the observed changed process is D, which is still present and has the same starttime. The allowed disappearance/PID-reuse exception for the process being read cannot justify ignoring D's two observed parent values. This finding concerns success after an observed deviation, not an unobservable transition between samples and not a demand to distinguish ordinary zombies. It does not claim a namespace escape or that every command must be sampled.

**Evidence and limits:** static control/data-flow proof on the exact merged SHA. The full `/proc` scan populates `info` at 2062–2066; root absence returns at 2068–2069; cached descendant comparison is later at 2072–2078. No earlier/later code compares those cached edges on this return path or clears the prior observation. The receipt checks recorded errors before success, but this path records none. The unchanged two-scan fixture and dedicated mutants measure the root-present paths only. `sampler-ast.txt` preserves the reviewed control flow. **No new root-exit fault scenario or exploit payload was authored or executed**; runtime frequency is unmeasured.

**Fix direction:** reconcile all previously validated descendants against the fresh snapshot before any root-absence early return. Preserve the accepted rule: missing descendant or different starttime retires that descendant's historical entry; same starttime with changed ppid latches `DanhTinhDoi`. Root absence can still prevent new traversal without suppressing already-observed deviations. Keep failed-initial-pin, root-reuse and full-chain checks, and never clear an existing error.

**Regression direction, in words:** use one sampler with a prior validated edge and observation; on the next snapshot make the root absent while the retained descendant is still present with the same starttime and changed ppid. Require `DanhTinhDoi` and `KHONG_DO_DUOC` immediately and at final receipt. Include controls where the root disappears but the descendant is actually gone/different-starttime, and the existing root-present clean and moved-edge controls. A dedicated mutant that restores the early return ahead of reconciliation should be killed by that named target's `TinHieuChotCa`. No such payload or new mutant was created here.

**Remediation risks:** moving reconciliation must not turn every root exit into an error or treat a reused descendant PID as the old process. It must still inspect all retained edges, including ones no longer in the current root subtree, and must not overwrite/drop a same-starttime changed edge before comparison. Keep history retirement bounded and retain conservative error dominance.

Class ledger: **1 open class / 1 newly reported manifestation / maximum P2**: `sandbox-process-identity-race` (history R27-PID-04 through 04g). The supplied fix genuinely repairs the reported root-present 04f scenarios, but does not close the class (**VÁ HỜ at class level**). The other four prior classes remain closed in the measured/static scope above. Overall: **0 P0, 0 P1, 1 P2, 0 P3**.

## Full-delta/spec assessment

Reviewed the full 844-addition/two-file delta against exact master `3e973a03b151e37cd402e0a723816eeaa8247193`, including production integration, tests and mutants, against the frozen spec and supplied owner decisions. No other independent P0–P3 finding was identified.

Effort is extracted only from accepted server response frames. Invalid/missing effort remains None while the frame still counts for model; effort counting occurs before model deduplication, so a later incomplete duplicate cannot be hidden. Distinct values preserve encounter order. Immutable tuples prevent the writer's shallow counter snapshot from sharing a mutable effort list. Model uncertainty blocks effort success; no CLI/config fallback was introduced. The existing model/filter matrix and generated regex case continue to pass.

Sandbox summaries use fixed semantic values and arity tables; no raw command or arbitrary path component is written to the new summary fields. The sampler reads only stat and descendant cmdline in production; the real-process case checks that read set, and the supplied environ-reading mutant runs only with credential-free test descendants. Non-Linux, failed reads/thread startup, incomplete thread shutdown and uncertain parsing all prevent success. Unknown/missing stdout JSON does not become a claim that no command ran. Timing is a 0.2-second wait plus scan duration; a hard maximum scan-to-scan interval under arbitrary host load was not established.

The identity sweep covered initialization, global snapshot collection, retained-edge retirement/comparison, subtree rebuilding, child and full-chain rereads, enqueue order, deduplication, error persistence, stop/join and receipt status. Changed descendant starttime in the historical cache is retired under the supplied exception; within-scan changed tuples still conservatively latch uncertainty. Any latched error survives later clean scans and dominates observations. The remaining ignored-value path is the root-absent return described in 04g. Initial root pinning stores only starttime; in production that root is the launcher's direct child, so losing its parent would normally terminate the writer itself. As in round 5, that unused initial ppid was not promoted into a separate finding without a viable production scenario.

The documented measurement limits remain: short-lived processes may escape sampling, argv[0] is self-declared, and ordinary lifecycle deviations may cause false downgrades. Fixtures named bwrap exercise observation/serialization, not actual namespace/seccomp enforcement. Previously accepted fixed path labels remain more detailed than the spec's original cwd/khac shorthand without retaining arbitrary names.

## Lint and acceptance limits

`env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27f.VechV5/static_checks.py` — **rc 0**. Both exact source files compile in memory. `git -C src diff --check 3e973a03b151e37cd402e0a723816eeaa8247193 60b3055c5eb999dff196aca42c53fa98c3eb641d` — **rc 0**.

Local `python3 -m ruff --version` reports **0.15.15**, matching the pin found in the checked-in CI workflows. Bare lint ran on exact base/head blob copies outside src: `python3 -m ruff check --isolated --no-cache --output-format json [--select F] <two files>`. Both F-only runs returned **rc 1**, with the same 5 F841 diagnostics. Both default-rule runs returned **rc 1**, with the same 145 diagnostics (113 E702, 23 E701, 5 F841, 2 E741, 2 E731). Comparing file/rule/message/source-line/column: **0 added / 0 removed** for each rule set. This meets zero lint delta; it is not absolute lint cleanliness or a live CI pin/probe-contract result. Exact commands and output: `static-results.json`.

Not run/not independently verified: full unrelated launcher suite, native Windows/macOS lanes, live CI/worker/land gates, authenticated Codex execution, actual kernel sandbox enforcement, and completed outer execution receipt. The spec's full-suite and native-Windows acceptance are not claimed satisfied by this scoped matrix. GitHub cannot be read here; owner comments, live publication state, g28 renewal and external call history remain unverified. No commits/pushes/comments were made to the reviewed repository; existing test helpers create fixture commits only in temporary repositories outside src, as required by their CLI tests. No credentials or additional Codex/model calls were used, no subagents were started, and no new exploit payload was authored.

Size remains **2 files / 844 added / 1 deleted**, within the supplied ≤2/≤850 cap (#748 issuecomment-6409625815). This is call **6 of 10** per the user. Lease `wp748-r27-g27` expired at **2026-10-27T00:18:51Z**; the user-authorized read-only review proceeds while g28 renewal awaits owner action. This verdict does not renew the lease or confer land/push authorization.

## Final source integrity and runtime limits

`python3 -B review-r27f.VechV5/final_integrity.py` — **rc 0**. HEAD, tree and both parents remain exactly the required identities. Detached-HEAD check returns rc 1 as expected; non-shallow and master-ancestry checks return rc 0. Final tracked/untracked/ignored status, worktree diff and index diff are empty, all rc 0. Both reviewed files match their Git blobs byte-for-byte, no launcher/test bytecode cache is present, and the selected nonexistent test-configuration path remains absent. Exact commands, rc, byte sizes and SHA-256 values are in `final-integrity.json`. Endpoint checks establish no observed source delta; they do not certify absence of every possible transient write. All reviewer artifacts and temporary fixture repositories are outside `src/`.

Runtime reports Linux 6.18.44 / Python 3.13.16. Session policy reports workspace-write sandboxing and approval policy never; these are configuration reports, not an independent kernel-enforcement measurement. The reviewer identity and execution surface limitations stated at the top still apply. The final outer `launcher.py run` receipt is unavailable from this active review and must be verified after completion by its consumer. This verdict does not self-certify provider/session authenticity, cross-provider assurance or land approval.

Completed UTC: 2026-10-27T00:48:21.364982+00:00

VERDICT: changes_requested
