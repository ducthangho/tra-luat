# Independent review — WP748 r27 (spec r27), round 7

**Approve: 0 P0, 0 P1, 0 P2, 0 P3.** R27-PID-04g is closed. Re-measured on the requested SHA: **50/50 cases passed, 168/168 mutants killed, 178/178 named-target signals**. Exact size is **850 added lines in 2 files**.

Reviewer: OpenAI Codex (`openai_codex`), identified by session developer runtime as an agent based on GPT-6. Observed surface: tool-enabled Codex agent with local shell execution; transport machine/local. Invocation through `launcher.py run` and call 7 of 10 are user-reported. I cannot independently verify the exact serving model/build, actual effort, outer CLI routing, provider/session authenticity, or completed outer execution receipt from inside this active run.

Review Class: sensitive. Started UTC: 2026-10-27 00:59:15 UTC. GitHub cannot be read in this review; owner comments, external call accounting and unpublished status cannot be independently verified. No credentials or network access are used.

Identity verified before substantive review: full, non-shallow clone; detached HEAD `8575a16afd0ec07af1e78af7af9594dd47c6cb54`; tree `955f60055aa2e60b4fa636a92e512dd5ee575f89`; parents `9a50525522cefea64bdda0e366327e7c2c00f5d1` and `7471f95f75d4ed37591e307b281cda55aa0cd6fd`. Parent 1 is a child of round-6 head `60b3055c5eb999dff196aca42c53fa98c3eb641d`; local `origin/master` is parent 2. Local branch and remote-tracking refs for `agent/wp748-r27-claude` point at HEAD; those local refs do not establish publication state. The hash is the review identifier.

Initial identity commands: `git -C src rev-parse --is-inside-work-tree --is-shallow-repository HEAD HEAD^{tree}` rc 0; `git -C src show -s --format='%H%n%T%n%P%n%D' HEAD` rc 0; `git -C src symbolic-ref -q HEAD` rc 1 (expected detached HEAD); `git -C src status --porcelain=v1` rc 0, empty; parent and origin/master queries rc 0. `git -C src diff --exit-code 9a50525522cefea64bdda0e366327e7c2c00f5d1 8575a16afd0ec07af1e78af7af9594dd47c6cb54 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` rc 0, empty.

Frozen spec read with `git -C src show origin/ops/wp748-r27-g27-lease:ops/specs/wp748-r27-launcher-effort-sandbox.md`, rc 0; SHA-256 `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd` matches. Lease on the same ref: `ops/leases/wp748-r27-g28-claude-remote-20261027.yaml`, rc 0; r27/g28, granted 2026-10-27T00:34:07Z, expires 2026-10-28T00:34:07Z, same spec and two-file write set. The lease records the raised ≤2 files / ≤850 added lines cap and 10-call cap. Live authority is not independently verified.

The supplied owner narrowing decision governs: every observed identity deviation must force uncertainty, including ordinary zombie reparenting. Disappearance or different starttime for the process being read is the benign exception. Accepted conservative false negatives are not reopened.

Initial size: `git -C src diff --numstat 7471f95f75d4ed37591e307b281cda55aa0cd6fd 8575a16afd0ec07af1e78af7af9594dd47c6cb54`, rc 0: launcher.py +351/-1; launcher_test.py +499/-0. **2 files / exactly 850 added / 1 deleted**, within the user-supplied owner cap (#748 issuecomment-6409625815).

Scratch and execution records: `review-r27g.VDwwZX/`, outside `src/`. Cloud-runtime skill read; no environment_status tool is available. No network or credential discovery performed. Source is treated read-only, including disabling Python bytecode.

## Re-measured cases

Each exact case ran as `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1` in a minimal credential-free environment, with bytecode disabled and TMPDIR in reviewer scratch. Full argv, output, rc and timing: `review-r27g.VDwwZX/matrix-results.json`.

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

Only checked-in DOT_BIEN replacements were applied to unique temporary launcher copies. Anchors must match exactly once, copies must compile, and every declared target must raise `TinHieuChotCa` with the named target code object in its traceback. Worker rc 10 = that signal; 0 = survivor; 11 = skip; 12 = unrelated exception; 13 = non-target signal; 14 = missing/ambiguous target; 124 = timeout. Only rc 10 counts as a kill.

Worker command: `python3 -B review-r27g.VDwwZX/run_matrix.py worker <temporary-launcher.py> <named-target>`.

| Mutant | Named target | rc | Result |
|---|---|---:|---|
| `r952_bo_ep_kieu_truong_credential` | `r952_auth_json_truong_la_kieu_object_van_doc_duoc` | 10 | TinHieuChotCa: killed |
| `r952_quay_ve_ep_moi_truong_la_chuoi` | `r952_auth_json_truong_la_kieu_object_van_doc_duoc` | 10 | TinHieuChotCa: killed |
| `r27_canh_sau_return_goc_vang` | `r927_canh_cha_doi_giua_hai_luot_quet` | 10 | TinHieuChotCa: killed |
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

Matrix totals: `{"cases_passed": 50, "cases_total": 50, "mutants_killed": 168, "mutants_total": 168, "targets_killed": 178, "targets_total": 178, "case_rcs": {"0": 50}, "target_rcs": {"10": 178}}`.

## Final re-measurement totals

Matrix driver command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 CODEX_HOME=/wp748-r27g-noauth-VDwwZX TMPDIR=<absolute review-r27g.VDwwZX> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27g.VDwwZX/run_matrix.py` — **rc 0**. Individual results above are fresh measurements on this SHA, not carried forward from prior verdicts.

| Cases | Passed / total | rc |
|---|---:|---|
| `r925_*` | 15/15 | all 0 |
| `r926_*` | 23/23 | all 0 |
| `r927_*` | 11/11 | all 0 |
| `r952_*` | 1/1 | all 0 |

| Mutants | Killed / total | Named-target signals | rc |
|---|---:|---:|---|
| `r25_*` | 25/25 | 32/32 | all 10 |
| `r26_*` | 99/99 | 102/102 | all 10 |
| `r27_*` | 42/42 | 42/42 | all 10 |
| `r952_*` | 2/2 | 2/2 | all 10 |

**Totals: 50/50 cases passed (rc 0 each); 168/168 mutants killed; 178/178 named-target TinHieuChotCa signals (rc 10 each). Zero skips, survivors, timeouts, compile failures, unmatched anchors or unrelated exception credits.** Every mutation anchor matched once; each unique copy compiled.

`r926_dot_bien_tu_sinh_moi_thanh_phan_regex` ran through the exact requested CLI with **rc 0** (88.178 s). Its passing assertions enforce **207 generated variants across 7 regex constants**, **200 killed by TinHieuChotCa**, and **7 surviving entries exactly matching the checked-in equivalence list**, with no other-exception credits. These are separate from the 168 hand-defined DOT_BIEN mutants; equivalent survivors are not reported as kills.

## ĐỐI CHIẾU LƯỢT TRƯỚC — closure and class sweep

History considered: `VERDICT_R27A.md` through `VERDICT_R27F.md`, frozen spec r27, g28 lease, and the supplied owner narrowing decision. The previous round's sole open finding, **R27-PID-04g, is closed — ĐÃ VÁ THẬT**. No new P0–P3 finding was identified in the full delta or the requested class sweep.

Independent observation command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 CODEX_HOME=/wp748-r27g-noauth-VDwwZX TMPDIR=<absolute review-r27g.VDwwZX> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27g.VDwwZX/closure_observations.py` — **rc 0**. This wraps the existing fixtures without changing their argv, identity faults, or assertions; it records sampler state before/after each scan and calls the real receipt writer. Detailed evidence: `closure-observations.json` and `closure.log`.

| Finding | Disposition on this SHA | Evidence |
|---|---|---|
| R27-PID-04g | **Closed — measured** | `.claude/dev/launcher.py:2067` reconciles retained edges before the root-absence return at 2076. Existing `goc_mat_chau_doi`: scan 1 retains the descendant without error; scan 2 records exactly `DanhTinhDoi`; the real writer reports `KHONG_DO_DUOC` with that reason. `goc_mat_chau_mat`: scan 2 records no error and retires the missing descendant. The new `r27_canh_sau_return_goc_vang` mutant raises the named target's `TinHieuChotCa` specifically at `goc_mat_chau_doi`, worker rc 10. |
| R27-PID-04f | **Stayed closed** | Both `ra_ngoai` and `vao_goc` retain the descendant in scan 1 and record `DanhTinhDoi` in scan 2. The unchanged control records no errors. The no-comparison and no-history mutants fail at `ra_ngoai`, named-target rc 10. |
| R27-PID-04e | **Stayed closed** | `to_tien_doi_cha` records `DanhTinhDoi` and `KHONG_DO_DUOC` in one scan. Full ancestor tuples are compared at launcher.py:2100; its starttime-only mutant is killed by the named target. |
| R27-PID-04c | **Stayed closed under the accepted decision** | `cha_zombie` records `DanhTinhDoi` and `KHONG_DO_DUOC` in one scan. The receipt explicitly documents ordinary-lifecycle false downgrades. No requirement to distinguish benign zombies is reintroduced. |
| R27-PID-04d | **Stayed closed** | `goc_khong_ghim` retains a None root pin and records `GocKhongGhimDuoc` / `KHONG_DO_DUOC`; late acquisition remains forbidden and the late-pin mutants are killed. |
| R27-PID-04 / 04b | **Stayed closed; no remaining actionable class manifestation found** | Existing current-child, root-reuse and intermediate-ancestor scenarios produce uncertainty on their first scan. Child and chain validation precede enqueue and deduplication. Retained edges are now reconciled even when the root has disappeared. |
| R27-ALLOW-01 | **Stayed closed** | Fixed semantic sets govern program/flag names, path labels, profile values and capabilities. The checked-in BWRAP/CLS secret-bearing fixtures pass byte decoding → summary → real receipt writing: two summaries, zero strings outside the fixed vocabulary, zero fixture secret markers. Named cases and mutants pass. Raw argv is not serialized into the new telemetry. |
| R27-PARSE-02 / 02b | **Stayed closed** | Arity and real-cmdline decoder cases pass. Interior empty arguments are retained; values are consumed by arity; unknown flags, incomplete arguments, absent command boundaries and missing terminal NUL remain uncertain. Corresponding named mutants are killed. |
| R27-PROC-03 | **Stayed closed** | The existing denied-read scenario records `PermissionError` and overrides its prior observation. Only FileNotFoundError/ProcessLookupError are swallowed by `_stat` and cmdline reads; other errors propagate to `_chay`'s persistent error list. The broad-swallow mutant is killed. |
| R27-TEST-05 | **Stayed closed** | The unchanged state case passes on Linux and under Windows/Darwin platform mocks. Constructor/start/stop/writer calls under those mocks create no sampler thread and report `KHONG_DO_DUOC`. These are Linux-hosted simulations, not native OS results. |

Measurement limit: the two-scan fixture uses ordinary descendant processes and does not seed a sandbox observation. Its clean/control receipts are unknown because stdout is empty; this is not misreported as identity failure. The existing status case separately measures that a latched error dominates a prior observation, and its bypass-error mutant is killed. The production branch ordering at 2131–2140 connects these measured properties. No new identity fault, exploit payload or mutant was authored.

## Every early exit in `_quet` and `_chay`

AST extraction independently enumerated three returns, three continues and one explicit raise in `_quet`; `_chay` has no return or continue and has one loop break. Source locations below are on the reviewed SHA. `sampler-ast.txt` and `static-results.json` preserve the enumeration.

| Location | Exit | Comparison / success analysis |
|---|---|---|
| launcher.py:2073 | Return after retained-edge mismatch | `DanhTinhDoi` is appended first. Later cached values can remain unexamined, but the recorded error permanently prevents `DO_DUOC`; this is not a successful bypass. |
| launcher.py:2076 | Return if root absent or initial pin unavailable | Every historical edge has already been reconciled, unless an earlier edge recorded an error and returned. Missing/different-starttime descendants are retired under the accepted exception. A missing initial root pin already has an error from construction. Root absence alone prevents new traversal without discarding a live descendant's observed changed ppid. |
| launcher.py:2078 | Raise on root starttime reuse | `_chay` records `RuntimeError`; no success is possible afterward. This preserves the earlier-closed root-reuse behavior. |
| launcher.py:2096 | Continue when current cmdline read reports disappearance | No cmdline or new identity tuple was returned by that read. Historical snapshot comparisons already ran. This is the explicitly allowed disappearance of the process being read; no successfully read conflicting tuple is ignored here. Other read errors escape to the error latch. |
| launcher.py:2099 | Continue when current stat reread reports disappearance | The current process has vanished. No replacement tuple was returned to compare; the benign exception applies. Historical observed deviations were checked before traversal. |
| launcher.py:2102 | Return on child/ancestor mismatch | `DanhTinhDoi` is appended first. The `or` and `any` short circuits may avoid additional reads once one mismatch is known, but cannot discard an already-read mismatch or leave success reachable. Each ancestor read that is performed is compared in full. |
| launcher.py:2107 | Continue for already-seen `(pid,starttime,cmdline)` | Current child and every ancestor have already passed comparison; the descendant has already been enqueued and its edge retained. Only repeated summary/count work is skipped. |
| launcher.py:2119 | `_chay` break after stop event | The current scan has finished before the wait/break. An in-flight scan is not canceled halfway by stop. Any exception instead appends its class name at 2121. Neither path clears prior errors. |

The snapshot build has no early return/continue; a read/listing/parse failure reaches `_chay` and makes the receipt uncertain. Cache retirement at 2069–2070 compares starttime before discarding an entry; it does not overwrite a same-starttime changed edge. Error lists persist across subsequent scans and take precedence over observations. `ket_thuc` joins the sampler and latches a still-running thread as uncertainty before the writer runs. No exit in the audited production path leaves `DO_DUOC` reachable after an observed deviation.

Initial root pinning retains starttime, not the initial ppid. As in earlier rounds, the production root is the launcher's direct child, so changing its parent normally requires losing the launcher that would write the receipt. No viable new production scenario was identified for promoting that unused initial ppid into a finding. This is distinct from descendants, whose observed parent changes are now retained and checked.

## Full-delta/spec review and merge isolation

Reviewed the complete delta of **351 added / 1 deleted production lines and 499 added test lines** against exact master `7471f95f75d4ed37591e307b281cda55aa0cd6fd`, including parsing, accounting, serialization, thread lifecycle, integration, fixtures and mutations. Saved diff: `review-r27g.VDwwZX/full-delta.patch`. No new P0, P1, P2 or P3 findings. The five historical finding classes are closed in the measured/static scope described above; this is not a proof against every possible future implementation or environment.

Effort is taken only from accepted server response frames. Missing or invalid reasoning/effort leaves model acceptance intact but increments missing-effort accounting. Accounting occurs before model deduplication, so a later incomplete duplicate cannot disappear from the effort decision. Distinct values preserve encounter order; immutable tuples keep the writer's counter snapshot from sharing a mutable effort list. Model uncertainty blocks effort success; CLI/config values are not fallback evidence. Existing filtering, lost-frame, malformed-input, EOF and timeout cases were re-measured.

Sandbox summaries retain fixed semantic values and respect option arity and raw NUL-separated argument boundaries. Unknown parsing results prevent success. Production sampling opens only process stat and descendant cmdline; the existing real-process fixture checks this read set. The checked-in environ-reading mutant executes only against credential-free test descendants. Non-Linux capability, read/start errors, an unfinished sampling thread and missing stdout evidence are handled conservatively. Existing fixture executables named bwrap measure observation/serialization, not actual namespace or seccomp enforcement.

The sampler uses a 0.2-second wait between scans. Scan time and scheduling add to the interval; a hard ≤0.5-second wall-clock bound under arbitrary host load was not established. Short-lived processes can evade sampling, argv[0] is self-declared, and ordinary lifecycle deviations can cause false negatives. These documented limitations are retained. Previously accepted fixed path labels are more detailed than the original cwd/khac shorthand but do not preserve arbitrary path names.

`git -C src diff --exit-code 9a50525522cefea64bdda0e366327e7c2c00f5d1 8575a16afd0ec07af1e78af7af9594dd47c6cb54 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` returns **rc 0, empty**. All **830** merge-side changed paths are under `ops/land` (75) or `ops/reviews` (755). No launcher/test/helper/workflow/configuration source changed on that side. The reviewed launcher/tests do not reference those two directories. `git -C src merge-base --is-ancestor origin/master HEAD` returns rc 0. The r952 auth parser and fixtures are already in exact master and unchanged by this merge; the r952 test uses in-memory INERT data. No launcher/test interaction from the master-side evidence changes was identified. Full path/command evidence: `merge-checks.json` and `static-results.json`.

## Checks, scope and limits

`env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27g.VDwwZX/static_checks.py` — **rc 0**. Both exact source files and base copies compile in memory. `git -C src diff --check 7471f95f75d4ed37591e307b281cda55aa0cd6fd 8575a16afd0ec07af1e78af7af9594dd47c6cb54` — **rc 0**.

Local Ruff is **0.15.15**, matching the pin in the checked-in CI workflows. `python3 -m ruff check --isolated --no-cache --output-format json [--select F] <base/head copies of both files>` returns **rc 1 on both base and head**. F-only: 5 diagnostics each; default rules: 145 each. Comparing file, rule, message, source line and column yields **0 added / 0 removed** for each rule set. This establishes zero lint delta, not absolute lint cleanliness or a live CI/probe-contract result. Exact commands/output are in `static-results.json`.

Not run/not independently verified: the full unrelated launcher suite, native Windows/macOS lanes, live CI/worker/land gates, authenticated Codex execution, kernel sandbox enforcement, publication state and the completed outer execution receipt. The scoped matrix does not certify the spec's full-suite and native-Windows acceptance requirements. GitHub cannot be read here; owner comments and external call accounting remain unverified. This content-review verdict does not confer push, merge, land, or cross-provider assurance authority; the consumer must validate the completed outer receipt and remaining gates separately.

No commits or pushes were made to the reviewed repository, no GitHub comments were posted, and no real credentials, additional model calls or subagents were used. Checked-in CLI test helpers create fixture commits only in temporary repositories outside src. Scratch scripts instrument existing fixtures and apply only checked-in mutant definitions. The source checkout was not edited.

The measured size is exactly **2 files / 850 added / 1 deleted**, satisfying ≤2 files / ≤850 added under the user-supplied owner decision #748 issuecomment-6409625815. This is **call 7 of 10** as reported by the user; no additional Codex calls were initiated. The local g28 lease artifact is current for this run; live lease authority is not independently verified.

## Final source integrity and runtime limits

`env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null python3 -B review-r27g.VDwwZX/final_integrity.py` — **rc 0**. HEAD, tree, both parents and detached/non-shallow state still match. Tracked/untracked/ignored status, worktree diff and index diff are empty. The launcher files match the reviewed Git blobs byte-for-byte, no launcher bytecode cache exists, and the nonexistent test configuration path remains absent. `final-integrity.json` contains individual commands/rcs and file hashes. These endpoint checks establish no observed source delta; they do not certify every possible transient filesystem write. All reviewer artifacts and temporary fixture repositories are outside `src/`.

The first invocation of this reviewer-only verification script returned **rc 1** because it attempted to parse an entire worker stdout as JSON when a target also printed ordinary diagnostic text. The parser was corrected to locate and validate the unique signal record; the same saved results then verified with rc 0. No source or test result was altered and no kill was inferred from this harness error. Original diagnostic: `final-integrity-initial-harness-error.log`.

Runtime reports **Linux 6.18.44-fc-v165 / Python 3.13.16**. Session policy reports workspace-write sandboxing and approval policy never; these are configuration reports, not a kernel-enforcement measurement. The final outer `launcher.py run` receipt is unavailable inside this active review and must be verified after completion. The identity and assurance limitations at the top remain applicable.

Decision: **approve the reviewed content at `8575a16afd0ec07af1e78af7af9594dd47c6cb54`, tree `955f60055aa2e60b4fa636a92e512dd5ee575f89`**. Zero open P0–P3 findings in this review. Full-suite/native-platform/CI and external receipt requirements are not claimed satisfied.

Completed UTC: 2026-10-27T01:10:11.148855+00:00

VERDICT: approve
