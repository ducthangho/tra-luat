# Inventory đột biến — wp899 r4 lượt 5

Reviewed SHA: `22da28c738e651361274c1264e681a52461dad1e`. GIET chỉ từ rc3/DO đúng ca; không cộng setup/import/permission.

## mutants

Nguồn chi tiết: [mutants/results.json](mutants/results.json).

| mutant | phân hạng | hạng finding | ca đích / giới hạn |
|---|---|---|---|
|A1_xoa_co_attempt|GIET|—|c01_cli_du_co; lỗi vô can: 0|
|A2_bo_so_attempt|GIET|—|c02_attempt_lech; lỗi vô can: 0|
|A3d_lay_sha_dau_tien|GIET|—|c06_checkout_hai_sha; lỗi vô can: 0|
|A3c_thieu_la_do_duoc|GIET|—|c05_checkout_khong_sha; lỗi vô can: 0|
|A3e_lay_head_sha_rest|GIET|—|c07_checkout_push_lech; lỗi vô can: 0|
|A3b_chi_nhan_linux|GIET|—|c04_checkout_windows; lỗi vô can: 0|
|A3g_pr_nhan_moi_sha|GIET|—|c09_checkout_pr_lech; lỗi vô can: 0|
|A3_sha_khong_nguyen_dong|GIET|—|c05_checkout_khong_sha; lỗi vô can: 0|
|A4d_regex_ca_log_job|GIET|—|c13_marker_buoc_khac; lỗi vô can: 0|
|A4b_skipped_la_passed|GIET|—|c11_job_skipped; lỗi vô can: 0|
|A4a_runner_0_la_passed|GIET|—|c10_runner_id_0; lỗi vô can: 0|
|A4c_khong_khop_la_not_measured|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|A4_chep_cung_MOI|GIET|—|c15_moi_mot_nguon; lỗi vô can: 0|
|A4_job_failure_bo_qua|GIET|—|c14_ngoai_moi; lỗi vô can: 0|
|A5_passed_khi_co_path|GIET|—|c16_workflow_def_luon_not_measured; lỗi vô can: 0|
|A6_ghi_thang_vao_out|GIET|—|c17_ghi_nguyen_tu; lỗi vô can: 0|
|A7_bo_dong_dem|GIET|—|c18_dem_not_measured; lỗi vô can: 0|
|A7_gop_rest_vao_12|GIET|—|c19_rest_loi; lỗi vô can: 0|
|M1_chi_doc_trang_dau|GIET|—|c20_du_trang; lỗi vô can: 0|
|F03_dung_khi_du_total|GIET|—|c20_du_trang; lỗi vô can: 0|
|F03_tap_luon_du|GIET|—|c20_du_trang; lỗi vô can: 0|
|F03_trung_id_van_them|GIET|—|c20_du_trang; lỗi vô can: 0|
|F04_jobs_run_khac|GIET|—|c20_du_trang; lỗi vô can: 0|
|F04_artifacts_run_khac|GIET|—|c20_du_trang; lỗi vô can: 0|
|F01_run_thieu_van_passed|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_gate_thieu_van_passed|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_checkout_head_thieu|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F02_search_thay_match|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|A14_kich_ban_tu_dong_mau|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|A15_khoi_la_tap_con|GIET|—|c26_f02_dong_khong_mau; lỗi vô can: 0|
|A16_bo_luat_toan_khoi|GIET|—|c27_f02_yaml_khong_toi_gian; lỗi vô can: 0|
|A16_bo_khop_nguyen_van|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|A17i_cho_env_buoc|GIET|—|c28_che_do_env_buoc; lỗi vô can: 0|
|A17ii_bo_env_job|GIET|—|c29_che_do_env_job; lỗi vô can: 0|
|A17iii_cho_doi_so|GIET|—|c30_che_do_doi_so; lỗi vô can: 0|
|che_do_bo_tien_to_VAR|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|che_do_bo_env_workflow|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|che_do_bo_defaults_workflow|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|che_do_bo_defaults_job|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|che_do_moi_shell|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|A26_bo_GITHUB_ENV|GIET|—|c42_github_env_cung_job; lỗi vô can: 0|
|F11_bo_GITHUB_PATH|GIET|—|c42_github_env_cung_job; lỗi vô can: 0|
|A26_tinh_ca_buoc_i|GIET|—|c42_github_env_cung_job; lỗi vô can: 0|
|A26_GITHUB_ENV_toan_workflow|GIET|—|c42_github_env_cung_job; lỗi vô can: 0|
|F08_git_bo_sha|GIET|—|c34_git_blob_that; lỗi vô can: 0|
|F08_git_luon_vang|GIET|—|c34_git_blob_that; lỗi vô can: 0|
|F02_bo_doi_dong|GIET|—|c35_f02_khoi_khong_tron_ven; lỗi vô can: 0|
|F02_bo_doi_shell|GIET|—|c35_f02_khoi_khong_tron_ven; lỗi vô can: 0|
|F02_cho_mau_sau|GIET|—|c35_f02_khoi_khong_tron_ven; lỗi vô can: 0|
|F02_bo_het_tien_to|GIET|—|c35_f02_khoi_khong_tron_ven; lỗi vô can: 0|
|F02_bo_doi_header|GIET|—|c35_f02_khoi_khong_tron_ven; lỗi vô can: 0|
|A18_head_sha_thay_sha_checkout|GIET|—|c32_workflow_khong_doc_duoc; lỗi vô can: 0|
|A18_yaml_hong_nem|GIET|—|c32_workflow_khong_doc_duoc; lỗi vô can: 0|
|A19_moi_ung_vien_trung_chu|GIET|—|c33_trung_chu_khac_job; lỗi vô can: 0|
|A19_chan_doc_job_khac|GIET|—|c33_trung_chu_khac_job; lỗi vô can: 0|
|A20i_zip_bo_dem_nhom|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|
|A20ii_zip_bo_dem_yaml|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|
|A21_bo_kiem_ten|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|ten_none_bang_none|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|ten_chi_buoc_chay|GIET|—|c45_buoc_skipped_giua; lỗi vô can: 0|
|ten_name_khong_chuoi|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|ten_name_rong_bo_qua|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|ten_v_khong_chuoi|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|ten_rstrip|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|loc_post_khong_cach|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|chay_chi_success|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|dem_chi_khi_thua_nhom|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|
|dem_chi_khi_thieu_rest|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|
|gio_theo_thu_tu_tho|GIET|—|c45_buoc_skipped_giua; lỗi vô can: 0|
|vi_tri_theo_thu_tu_tho|GIET|—|c45_buoc_skipped_giua; lỗi vô can: 0|
|wf_none_khai_passed|GIET|—|c32_workflow_khong_doc_duoc; lỗi vô can: 0|
|gio_match_thay_fullmatch|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|job_hau_to_bat_ky|GIET|—|c39_ghep_job; lỗi vô can: 0|
|job_hau_to_khong_ngoac|GIET|—|c39_ghep_job; lỗi vô can: 0|
|job_cho_x_rong|GIET|—|c39_ghep_job; lỗi vô can: 0|
|gio_bo_kiem_str|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|gio_bo_bat_ValueError|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|job_chi_name_khi_co_name|GIET|—|c39_ghep_job; lỗi vô can: 0|
|L3_number_bool|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_number_float|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_alias_name_bo|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_ma_tran_khac_rong|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_ma_tran_dotall|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_post_o_giua|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_run_rstrip_het|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_run_ep_chuoi|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_bo_dedupe|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_endgroup_startswith|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_shell_khong_cach|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_truoc_bo_buoc_dau|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_truoc_chi_lien_ke|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L3_env_bo_dang|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_env_truthy|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_env_chi_chuoi|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_env_wf_co_mat|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_defaults_wf_truthy|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_defaults_job_truthy|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_shell_bo_pwsh|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_shell_bo_sh|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_shell_null_mac_dinh|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_khoa_bo_id|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_khoa_bo_if|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_khoa_bo_timeout|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L3_khoa_bo_coe|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|O_job_none_and|GIET|—|c39_ghep_job; lỗi vô can: 0|
|O_var_mot_dong_all|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|O_goi_or|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|O_goi_any|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|N_ten_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_ten_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_job_match|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_job_khoang_trang_ngoac|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_ten_run_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_ten_splitlines|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_ten_name_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_rest_ten_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_meta_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_post_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_post_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_concl_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_concl_timed_out|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_env_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_env_v_truthy|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|N_defaults_none|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_github_re_I|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_github_dollar|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_mau_rong|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_header_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_in_lai_strip|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|N_in_lai_rstrip|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|N_group_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_long_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_shell_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_endgroup_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_run_join_rstrip|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|N_run_cr|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_gio_Z_tuy_chon|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_khoa_lower|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_uses_rong|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_uses_job_rong|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_name_present_none|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|N_run_truoc_uses|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_job_escape_alias|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_job_alias_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_job_casefold|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_name_explicit_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_name_explicit_casefold|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_metadata_setup_prefix|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_metadata_complete_prefix|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_metadata_post_suffix|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_ran_neutral_excluded|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_ran_cancelled_excluded|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_env_prefix_empty_suffix|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_env_prefix_casefold|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_mode_step_key_truthy|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_mode_shell_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_mode_shell_casefold|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_mode_prior_requires_ran|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_run_compare_strip_newlines|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_header_lstrip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_shell_lstrip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|L4_number_contiguous|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|
|job_bo_x_str|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|so_number_0|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|so_number_am|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|sy_khong_list|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|dd_run_khong_chuoi|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|A22_bo_kiem_gio|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|A22_khong_cat_giay|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|F09_bo_kiem_lich|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|F09_nhan_offset|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|F09_header_thieu_dung_rest|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|F10_bo_sort|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|F10_bo_number_trung|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|F10_ten_lstrip|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|F10_name_bieu_thuc|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|dang_bo_number|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|dang_buoc_rest_khong_dict|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|dang_buoc_yaml_khong_dict|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|dang_job_khong_dict|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|A23_lay_khoa_dau|GIET|—|c39_ghep_job; lỗi vô can: 0|
|A23_nhan_job_goi_lai|GIET|—|c39_ghep_job; lỗi vô can: 0|
|A23_nhan_bieu_thuc|GIET|—|c39_ghep_job; lỗi vô can: 0|
|A24_bo_luat_nhom_long|GIET|—|c40_nhom_long; lỗi vô can: 0|
|A25i_uses_sinh_marker|GIET|—|c41_buoc_uses; lỗi vô can: 0|
|A25ii_zip_bo_dem_nhom|GIET|—|c41_buoc_uses; lỗi vô can: 0|
|A27_khoi_bang_buoc_khac|GIET|—|c43_khoi_khac_buoc; lỗi vô can: 0|
|F01_steps_chi_la_list|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F05_chieu_khong_an_toan|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F05_luoi_cuoi|GIET|—|c19_rest_loi; lỗi vô can: 0|
|F02_khong_noi_dong|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|F02_cho_moi_co|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|F01_bool_la_int|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_chuoi_rong|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_conclusion_bat_ky|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_labels_rong|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_check_run_bat_ky|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_head_sha_bat_ky|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_head_sha_nhan_newline|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_check_run_nhan_newline|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_artifact_khong_kiem|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F01_phong_bi_khong_kiem|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|F03_bo_kiem_total_doi|GIET|—|c20_du_trang; lỗi vô can: 0|
|F05_than_run_sai_dang|GIET|—|c19_rest_loi; lỗi vô can: 0|
|F05_loi_ghi_mat_dong_dem|GIET|—|c19_rest_loi; lỗi vô can: 0|
|F05_sai_doi_so_mat_dong_dem|GIET|—|c01_cli_du_co; lỗi vô can: 0|
|F05_rest_mat_dong_dem|GIET|—|c19_rest_loi; lỗi vô can: 0|
|F06_redirect_lot_loi|GIET|—|c24_goi_that_loi_va_chuyen_huong; lỗi vô can: 0|
|F06_redirect_mang_token|GIET|—|c24_goi_that_loi_va_chuyen_huong; lỗi vô can: 0|
|vo_can_AttributeError_qua_except_doi_kieu|TIN_DUNG_GIA|— tự kiểm có chủ ý|c03_checkout_linux; lỗi vô can: 0|
|chi_them_chu_thich|SONG_SOT|— tự kiểm có chủ ý|c20_du_trang; lỗi vô can: 0|

## frontier

Nguồn chi tiết: [frontier/results.json](frontier/results.json).

| mutant | phân hạng | hạng finding | ca đích / giới hạn |
|---|---|---|---|
|job_rest_type|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|job_match_search|GIET|—|c39_ghep_job, c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|job_matrix_nonempty|GIET|—|c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|job_dotall_add|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|job_alias_exact_drop|GIET|—|c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|name_use_last_line|GIET|—|c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c37_ghep_lech_ten; lỗi vô can: 0|
|name_rest_strip|GIET|—|c37_ghep_lech_ten, c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|time_drop_type|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|time_year0_drop|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|time_calendar_date_only|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|time_low_strict|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|time_hi_strict|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|time_or_bounds|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|time_low_only|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|time_hi_only|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|rest_number_float|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|rest_number_bool|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|rest_steps_list_drop|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|rest_steps_all_any|GIET|—|c44_ghep_sai_dang, c47_bien_ghep; lỗi vô can: 0|
|yaml_steps_all_any|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|number_sort_desc|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|metadata_keep_setup|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|metadata_keep_complete|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|metadata_post_anywhere|GIET|—|c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_env_shape_drop|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|mode_env_prefix_exact|GIET|—|c29_che_do_env_job, c31_che_do_duong_khac, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_shell_no_pwsh|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_shell_no_sh|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_shell_null_default|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_env_presence_not_value|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|mode_env_job_presence|GIET|—|c29_che_do_env_job, c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_key_id_drop|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_key_if_drop|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_key_timeout_drop|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_key_coe_drop|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_prior_skip_first|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|mode_prior_only_first|GIET|—|c42_github_env_cung_job, c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_prior_only_last|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|mode_prior_include_current|GIET|—|c42_github_env_cung_job; lỗi vô can: 0|
|run_rstrip_all|GIET|—|c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|run_type_coerce|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|dd_group_reverse|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|dd_map_reverse|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|dd_output_dedupe|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|log_group_close_exact|HONG_NEO|— không tạo mutant, không tính sống|; lỗi vô can: 0|
|log_shell_suffix|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|log_nested_before_only|GIET|—|c40_nhom_long; lỗi vô can: 0|
|log_nested_after_only|SONG_SOT|P3|; lỗi vô can: 0|
|log_prefix_drop_ok|GIET|—|c35_f02_khoi_khong_tron_ven; lỗi vô can: 0|
|log_close_ignore_prefix|GIET|—|c35_f02_khoi_khong_tron_ven; lỗi vô can: 0|

## frontier2

Nguồn chi tiết: [frontier2/results.json](frontier2/results.json).

| mutant | phân hạng | hạng finding | ca đích / giới hạn |
|---|---|---|---|
|mode_defaults_wf_truthy|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_defaults_job_truthy|GIET|—|c46_mien_che_do, c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_env_truthy|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|mode_env_string_only|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|number_type_bool_guard_drop|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|number_min_strict|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|header_time_other_group|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|header_window_other_step|GIET|—|c38_ghep_lech_gio, c48_nguyen_van_va_mien; lỗi vô can: 0|
|time_current_end_other_step|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|name_only_first_rest|GIET|—|c37_ghep_lech_ten, c44_ghep_sai_dang, c45_buoc_skipped_giua; lỗi vô can: 0|
|name_only_last_rest|GIET|—|c45_buoc_skipped_giua; lỗi vô can: 0|

## new-frontier

Nguồn chi tiết: [new-frontier/results.json](new-frontier/results.json).

| mutant | phân hạng | hạng finding | ca đích / giới hạn |
|---|---|---|---|
|job_escape_alias|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|job_alias_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|job_casefold|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|name_explicit_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|name_explicit_casefold|GIET|—|c37_ghep_lech_ten, c44_ghep_sai_dang, c47_bien_ghep; lỗi vô can: 0|
|metadata_setup_prefix|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|metadata_complete_prefix|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|metadata_post_suffix|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|ran_neutral_excluded|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|ran_cancelled_excluded|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|env_prefix_empty_suffix|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|env_prefix_casefold|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_step_key_truthy|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_shell_strip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_shell_casefold|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|mode_prior_requires_ran|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|run_compare_strip_newlines|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|header_lstrip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|shell_lstrip|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|number_contiguous|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|

## frontier5

Nguồn chi tiết: [frontier5/results.json](frontier5/results.json).

| mutant | phân hạng | hạng finding | ca đích / giới hạn |
|---|---|---|---|
|wf_env_dict_only|SONG_SOT|P1/F10|; lỗi vô can: 0|
|wf_env_nonempty_only|SONG_SOT|P1/F10|; lỗi vô can: 0|
|job_env_only_first_key|SONG_SOT|P1/F10|; lỗi vô can: 0|
|job_env_only_last_key|GIET|—|c29_che_do_env_job; lỗi vô can: 0|
|mode_last_step|SONG_SOT|P1/F10|; lỗi vô can: 0|
|mode_first_run_step|SONG_SOT|P1/F10|; lỗi vô can: 0|
|mode_first_job|SONG_SOT|P1/F10|; lỗi vô can: 0|
|dd_first_job|SONG_SOT|P1/F10|; lỗi vô can: 0|
|job_match_exact_preference|SONG_SOT|P1/F10|; lỗi vô can: 0|
|job_first_prefix_only|SONG_SOT|P1/F10|; lỗi vô can: 0|
|metadata_first_setup_only|GIET|—|c48_nguyen_van_va_mien; lỗi vô can: 0|
|metadata_complete_last_only|GIET|—|c36_ghep_lech_so, c48_nguyen_van_va_mien; lỗi vô can: 0|
|time_name_first_key|GIET|—|c38_ghep_lech_gio, c48_nguyen_van_va_mien; lỗi vô can: 0|
|time_name_last_key|SONG_SOT|P1/F10|; lỗi vô can: 0|
|time_only_first_group|GIET|—|c38_ghep_lech_gio, c48_nguyen_van_va_mien; lỗi vô can: 0|
|time_only_last_group|SONG_SOT|P1/F10|; lỗi vô can: 0|
|name_skip_first_yaml|SONG_SOT|P1/F10|; lỗi vô can: 0|
|name_skip_last_yaml|GIET|—|c37_ghep_lech_ten, c44_ghep_sai_dang, c48_nguyen_van_va_mien; lỗi vô can: 0|
|rest_sort_lexical|SONG_SOT|P1/F10|; lỗi vô can: 0|
|rest_sort_input|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|rest_number_integral_float|SONG_SOT|P1/F10|; lỗi vô can: 0|
|ghep_zero_groups_reject|SONG_SOT|P1/F10|; lỗi vô can: 0|
|env_false_accept|SONG_SOT|P1/F10|; lỗi vô can: 0|
|env_int_accept|SONG_SOT|P1/F10|; lỗi vô can: 0|
|env_empty_str_accept|SONG_SOT|P1/F10|; lỗi vô can: 0|
|prior_run_only_strings|SONG_SOT|P3|; lỗi vô can: 0|
|prior_github_match|GIET|—|c42_github_env_cung_job, c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|prior_path_suffix|SONG_SOT|P1/F10|; lỗi vô can: 0|
|prior_env_word_boundary|SONG_SOT|P1/F10|; lỗi vô can: 0|
|nested_exact_only|GIET|—|c40_nhom_long; lỗi vô can: 0|
|nested_only_after_shell|SONG_SOT|P3|; lỗi vô can: 0|
|nested_only_before_shell|GIET|—|c40_nhom_long; lỗi vô can: 0|
|header_colored_exact|SONG_SOT|P1/F10|; lỗi vô can: 0|
|header_seconds_18|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|header_seconds_round|GIET+NEM|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 1|
|run_blank_tail_only|SONG_SOT|P1/F10|; lỗi vô can: 0|
|run_trailing_lf_exact|SONG_SOT|P1/F10|; lỗi vô can: 0|
|run_first_group_only|GIET|—|c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi; lỗi vô can: 0|
|run_last_group_only|GIET|—|c13_marker_buoc_khac, c42_github_env_cung_job; lỗi vô can: 0|
|minimal_reverse_lines|GIET|—|c27_f02_yaml_khong_toi_gian, c46_mien_che_do; lỗi vô can: 0|
|minimal_first_line_only|GIET|—|c27_f02_yaml_khong_toi_gian, c46_mien_che_do; lỗi vô can: 0|
|name_uses_strip|SONG_SOT|P1/F10|; lỗi vô can: 0|
|name_run_prefer_uses|GIET|—|c41_buoc_uses, c48_nguyen_van_va_mien; lỗi vô can: 0|
|name_remove_blank_lines|GIET|—|c37_ghep_lech_ten, c48_nguyen_van_va_mien; lỗi vô can: 0|
|name_reject_empty_line|GIET|—|c37_ghep_lech_ten, c48_nguyen_van_va_mien; lỗi vô can: 0|
|env_prefix_value_only|SONG_SOT|P1/F10|; lỗi vô can: 0|

## operators5-target

Nguồn chi tiết: [operators5-target/results.json](operators5-target/results.json).

| mutant | phân hạng | hạng finding | ca đích / giới hạn |
|---|---|---|---|
|L154c13:'is not'->'is'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L154c25:'and'->'or'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L154c38:'is not'->'is'|GIET|—|c29_che_do_env_job; lỗi vô can: 0|
|L154c50:'or'->'and'|GIET|—|c29_che_do_env_job; lỗi vô can: 0|
|L154c53:'any'->'all'|GIET|—|c29_che_do_env_job; lỗi vô can: 0|
|L162c26:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L162c34:'and'->'or'|GIET|—|c32_workflow_khong_doc_duoc; lỗi vô can: 0|
|L162c59:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L166c58:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L166c65:'and'->'or'|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|L166c77:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L166c85:'and'->'or'|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|L166c89:'any'->'all'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L167c16:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L167c23:'and'->'or'|GIET|—|c33_trung_chu_khac_job; lỗi vô can: 0|
|L167c29:'and'->'or'|GIET|—|c33_trung_chu_khac_job; lỗi vô can: 0|
|L167c39:'not in'->'in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L167c48:'and'->'or'|GIET|—|c33_trung_chu_khac_job; lỗi vô can: 0|
|L168c16:'0'->'1'|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L168c32:'=='->'!='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L168c35:'1'->'2'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L168c35:'1'->'0'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L171c14:'in'->'not in'|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L172c46:'and'->'or'|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|L172c56:'not in'->'in'|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|L174c34:'0'->'1'|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L178c45:'19'->'20'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L178c45:'19'->'18'|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|L178c82:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L178c89:'and'->'or'|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|L187c10:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L191c9:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L191c17:'or'->'and'|GIET|—|c39_ghep_job; lỗi vô can: 0|
|L191c27:'in'->'not in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L191c44:'or'->'and'|GIET|—|c39_ghep_job; lỗi vô can: 0|
|L191c56:'is not'->'is'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L191c68:'or'->'and'|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|L191c71:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L191c75:'all'->'any'|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|L191c87:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L193c7:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L193c21:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L193c29:'and'->'or'|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|L193c33:'all'->'any'|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|L193c45:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L193c53:'and'->'or'|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|L193c78:'1'->'2'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L193c78:'1'->'0'|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|L194c12:'and'->'or'|GIET|—|c22_thieu_dinh_danh_khong_passed; lỗi vô can: 0|
|L194c47:'=='->'!='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L196c77:'not in'->'in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L197c11:'and'->'or'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L197c15:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L198c64:'!='->'=='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L199c17:'!='->'=='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L201c16:'!='->'=='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L203c7:'any'->'all'|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|L203c11:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L203c37:'or'->'and'|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|L203c54:'!='->'=='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L205c7:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L205c11:'all'->'any'|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|L205c53:'and'->'or'|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|L206c15:'and'->'or'|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|L206c41:'and'->'or'|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|L206c47:'<='->'<'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L206c52:'<='->'<'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L214c27:'in'->'not in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L214c33:'or'->'and'|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|L214c61:'or'->'and'|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|L214c75:'in'->'not in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L214c80:'or'->'and'|GIET|—|c29_che_do_env_job; lỗi vô can: 0|
|L214c107:'or'->'and'|GIET|—|c28_che_do_env_buoc; lỗi vô can: 0|
|L215c16:'or'->'and'|GIET|—|c28_che_do_env_buoc; lỗi vô can: 0|
|L215c42:'not in'->'in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L216c16:'or'->'and'|GIET|—|c31_che_do_duong_khac; lỗi vô can: 0|
|L216c19:'any'->'all'|GIET|—|c42_github_env_cung_job; lỗi vô can: 0|
|L262c91:'True'->'False'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L262c103:'True'->'False'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L262c120:'True'->'False'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L263c35:'19'->'20'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L263c35:'19'->'18'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L264c18:'and'->'or'|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L264c34:'1'->'2'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L264c34:'1'->'0'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L265c31:'in'->'not in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L266c17:'=='->'!='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L267c26:'False'->'True'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L268c21:'and'->'or'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L271c48:'and'->'or'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L271c52:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L271c60:'and'->'or'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L271c64:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L271c94:'and'->'or'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L272c20:'not'->''|GIET|—|c47_bien_ghep; lỗi vô can: 0|
|L272c37:'or'->'and'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L272c66:'False'->'True'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L274c18:'1'->'2'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L274c18:'1'->'0'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L275c27:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L275c39:'and'->'or'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L275c51:'and'->'or'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L275c55:'not'->''|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L275c72:'and'->'or'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L275c89:'1'->'2'|GIET|—|c27_f02_yaml_khong_toi_gian; lỗi vô can: 0|
|L275c89:'1'->'0'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L275c92:'=='->'!='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L291c17:'0'->'1'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L292c36:'or'->'and'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L294c37:'not in'->'in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L295c11:'not'->''|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L295c26:'is'->'is not'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L295c33:'and'->'or'|GIET|—|c25_f02_env_mang_mau; lỗi vô can: 0|
|L295c49:'and'->'or'|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L295c70:'=='->'!='|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L297c14:'1'->'2'|GIET|—|c27_f02_yaml_khong_toi_gian; lỗi vô can: 0|
|L297c14:'1'->'0'|GIET|—|c27_f02_yaml_khong_toi_gian; lỗi vô can: 0|
|L299c35:'or'->'and'|GIET|—|c28_che_do_env_buoc; lỗi vô can: 0|
|L299c38:'any'->'all'|GIET|—|c46_mien_che_do; lỗi vô can: 0|
|L299c44:'and'->'or'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L299c50:'1'->'2'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L299c50:'1'->'0'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L300c38:'2'->'3'|GIET|—|c44_ghep_sai_dang; lỗi vô can: 0|
|L300c38:'2'->'1'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L300c62:'and'->'or'|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L300c66:'all'->'any'|GIET|—|c23_chi_loi_goi_that; lỗi vô can: 0|
|L302c21:'not in'->'in'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|L302c32:'or'->'and'|GIET|—|c28_che_do_env_buoc; lỗi vô can: 0|
|L303c102:'not in'->'in'|GIET|—|c28_che_do_env_buoc; lỗi vô can: 0|
|L307c98:'0'->'1'|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|

## prior2/extra-r4

Nguồn chi tiết: [prior2/extra-r4/results.json](prior2/extra-r4/results.json).

| mutant | phân hạng | hạng finding | ca đích / giới hạn |
|---|---|---|---|
|baseline|SONG_SOT|— đối chứng đồng nhất, không phải mutant|; lỗi vô can: 0|
|sort_bi_bo|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|kiem_number_bi_bo|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|sap_xep_theo_ten|GIET|—|c13_marker_buoc_khac, c23_chi_loi_goi_that, c31_che_do_duong_khac; lỗi vô can: 0|
|gio_nhan_offset|GIET|—|c38_ghep_lech_gio; lỗi vô can: 0|
|gio_thieu_header_lay_rest|HONG_NEO|— không tạo mutant, không tính sống|; lỗi vô can: 0|
|gio_bo_can_duoi|HONG_NEO|— không tạo mutant, không tính sống|; lỗi vô can: 0|
|gio_bo_can_tren|HONG_NEO|— không tạo mutant, không tính sống|; lỗi vô can: 0|
|a_bo_dem_nhom|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|
|a_bo_dem_yaml|GIET|—|c36_ghep_lech_so; lỗi vô can: 0|
|b_bo_ten|HONG_NEO|— không tạo mutant, không tính sống|; lỗi vô can: 0|
|d_lay_dau|GIET|—|c39_ghep_job; lỗi vô can: 0|
|env_quet_ca_job|GIET|—|c42_github_env_cung_job; lỗi vô can: 0|
|env_bo_PATH|HONG_NEO|— không tạo mutant, không tính sống|; lỗi vô can: 0|
|number_missing_tu_sinh|TIN_DUNG_GIA|—|c44_ghep_sai_dang; lỗi vô can: 1|
|job_ten_name_bi_bo|GIET|—|c39_ghep_job, c47_bien_ghep, c48_nguyen_van_va_mien; lỗi vô can: 0|
|job_khoa_bi_bo|GIET|—|c12_marker_khong_khop; lỗi vô can: 0|
|ten_run_lstrip|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|
|ten_name_khong_kiem_bieu_thuc|GIET|—|c37_ghep_lech_ten; lỗi vô can: 0|

## n_goi_strip_run

P1/F10; SONG_SOT48/48, baseline0 → mutant3 đúng ca. Xem norm-full5.json và norm-head/norm-mutant stdout.
