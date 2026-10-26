# Danh mục đột biến — wp899 r4 lượt 7

Kết quả GIET chỉ nói phép đo được liệt kê. GIET+NEM có ít nhất một tín hiệu đúng và ngoại lệ ngoài ca đích; không nhận ngoại lệ làm tín dụng. Bản sao nguồn/neo/thay, command, rc, output và phạm vi đầy đủ trong JSON producer. Các producer trùng neo/thay là lần đo lặp, không cộng thành mutant độc lập.

| producer | số mục / phân hạng |
|---|---|
| mutants/results.json | {'GIET': 255, 'TIN_DUNG_GIA': 1, 'SONG_SOT': 1} |
| historical-targets6/results.json | {'GIET': 77, 'HONG_NEO': 3, 'SONG_SOT': 1} |
| operators6-combined.json | {'GIET+NEM': 29, 'GIET': 101} |
| operator-errors6-results.json | {'TIN_DUNG_GIA': 71} |
| normalization6-results.json | {'GIET': 34, 'TIN_DUNG_GIA': 1} |
| frontier5/results.json | {'GIET': 45, 'SONG_SOT': 1} |
| frontier6/results.json | {'GIET': 64, 'SONG_SOT': 1} |
| frontier6-extra/results.json | {'GIET': 1} |
| frontier6-extra2/results.json | {'GIET': 1} |
| frontier6-extra3/results.json | {'GIET': 1} |
| frontier7/results.json | {'GIET': 22, 'SONG_SOT': 34, 'GIET+NEM': 1} |
| frontier7b/results.json | {'SONG_SOT': 1, 'GIET': 1} |
| reanchored6-results.json | {'GIET': 3} |
| signature6-results.json | {'GIET': 2} |
| prior1/old1/extra-mutants/results.json | {'GIET': 2} |
| prior1/old2/extra-mutants/results.json | {'GIET': 2} |
| prior2/old1/extra-mutants/results.json | {'GIET': 2} |
| prior2/old2/extra-mutants/results.json | {'GIET': 2} |

| producer | mutant | kết quả | ca đích / phạm vi | hạng finding / quyết định |
|---|---|---|---|---|
| mutants/results.json | A1_xoa_co_attempt | GIET | c01_cli_du_co | không mở finding;  |
| mutants/results.json | A2_bo_so_attempt | GIET | c02_attempt_lech | không mở finding;  |
| mutants/results.json | A3d_lay_sha_dau_tien | GIET | c06_checkout_hai_sha | không mở finding;  |
| mutants/results.json | A3c_thieu_la_do_duoc | GIET | c05_checkout_khong_sha | không mở finding;  |
| mutants/results.json | A3e_lay_head_sha_rest | GIET | c07_checkout_push_lech | không mở finding;  |
| mutants/results.json | A3b_chi_nhan_linux | GIET | c04_checkout_windows | không mở finding;  |
| mutants/results.json | A3g_pr_nhan_moi_sha | GIET | c09_checkout_pr_lech | không mở finding;  |
| mutants/results.json | A3_sha_khong_nguyen_dong | GIET | c05_checkout_khong_sha | không mở finding;  |
| mutants/results.json | A4d_regex_ca_log_job | GIET | c13_marker_buoc_khac | không mở finding;  |
| mutants/results.json | A4b_skipped_la_passed | GIET | c11_job_skipped | không mở finding;  |
| mutants/results.json | A4a_runner_0_la_passed | GIET | c10_runner_id_0 | không mở finding;  |
| mutants/results.json | A4c_khong_khop_la_not_measured | GIET | c12_marker_khong_khop | không mở finding;  |
| mutants/results.json | A4_chep_cung_MOI | GIET | c15_moi_mot_nguon | không mở finding;  |
| mutants/results.json | A4_job_failure_bo_qua | GIET | c14_ngoai_moi | không mở finding;  |
| mutants/results.json | A5_passed_khi_co_path | GIET | c16_workflow_def_luon_not_measured | không mở finding;  |
| mutants/results.json | A6_ghi_thang_vao_out | GIET | c17_ghi_nguyen_tu | không mở finding;  |
| mutants/results.json | A7_bo_dong_dem | GIET | c18_dem_not_measured | không mở finding;  |
| mutants/results.json | A7_gop_rest_vao_12 | GIET | c19_rest_loi | không mở finding;  |
| mutants/results.json | M1_chi_doc_trang_dau | GIET | c20_du_trang | không mở finding;  |
| mutants/results.json | F03_dung_khi_du_total | GIET | c20_du_trang | không mở finding;  |
| mutants/results.json | F03_tap_luon_du | GIET | c20_du_trang | không mở finding;  |
| mutants/results.json | F03_trung_id_van_them | GIET | c20_du_trang | không mở finding;  |
| mutants/results.json | F04_jobs_run_khac | GIET | c20_du_trang | không mở finding;  |
| mutants/results.json | F04_artifacts_run_khac | GIET | c20_du_trang | không mở finding;  |
| mutants/results.json | F01_run_thieu_van_passed | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_gate_thieu_van_passed | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_checkout_head_thieu | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F02_search_thay_match | GIET | c23_chi_loi_goi_that | không mở finding;  |
| mutants/results.json | A14_kich_ban_tu_dong_mau | GIET | c25_f02_env_mang_mau | không mở finding;  |
| mutants/results.json | A15_khoi_la_tap_con | GIET | c26_f02_dong_khong_mau | không mở finding;  |
| mutants/results.json | A16_bo_luat_toan_khoi | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| mutants/results.json | A16_bo_khop_nguyen_van | GIET | c25_f02_env_mang_mau | không mở finding;  |
| mutants/results.json | A17i_cho_env_buoc | GIET | c28_che_do_env_buoc | không mở finding;  |
| mutants/results.json | A17ii_bo_env_job | GIET | c29_che_do_env_job | không mở finding;  |
| mutants/results.json | A17iii_cho_doi_so | GIET | c30_che_do_doi_so | không mở finding;  |
| mutants/results.json | che_do_bo_tien_to_VAR | GIET | c31_che_do_duong_khac | không mở finding;  |
| mutants/results.json | che_do_bo_env_workflow | GIET | c31_che_do_duong_khac | không mở finding;  |
| mutants/results.json | che_do_bo_defaults_workflow | GIET | c31_che_do_duong_khac | không mở finding;  |
| mutants/results.json | che_do_bo_defaults_job | GIET | c31_che_do_duong_khac | không mở finding;  |
| mutants/results.json | che_do_moi_shell | GIET | c31_che_do_duong_khac | không mở finding;  |
| mutants/results.json | A26_bo_GITHUB_ENV | GIET | c42_github_env_cung_job | không mở finding;  |
| mutants/results.json | F11_bo_GITHUB_PATH | GIET | c42_github_env_cung_job | không mở finding;  |
| mutants/results.json | A26_tinh_ca_buoc_i | GIET | c42_github_env_cung_job | không mở finding;  |
| mutants/results.json | A26_GITHUB_ENV_toan_workflow | GIET | c42_github_env_cung_job | không mở finding;  |
| mutants/results.json | F08_git_bo_sha | GIET | c34_git_blob_that | không mở finding;  |
| mutants/results.json | F08_git_luon_vang | GIET | c34_git_blob_that | không mở finding;  |
| mutants/results.json | F02_bo_doi_dong | GIET | c35_f02_khoi_khong_tron_ven | không mở finding;  |
| mutants/results.json | F02_bo_doi_shell | GIET | c35_f02_khoi_khong_tron_ven | không mở finding;  |
| mutants/results.json | F02_cho_mau_sau | GIET | c35_f02_khoi_khong_tron_ven | không mở finding;  |
| mutants/results.json | F02_bo_het_tien_to | GIET | c35_f02_khoi_khong_tron_ven | không mở finding;  |
| mutants/results.json | F02_bo_doi_header | GIET | c35_f02_khoi_khong_tron_ven | không mở finding;  |
| mutants/results.json | A18_head_sha_thay_sha_checkout | GIET | c32_workflow_khong_doc_duoc | không mở finding;  |
| mutants/results.json | A18_yaml_hong_nem | GIET | c32_workflow_khong_doc_duoc | không mở finding;  |
| mutants/results.json | A19_moi_ung_vien_trung_chu | GIET | c33_trung_chu_khac_job | không mở finding;  |
| mutants/results.json | A19_chan_doc_job_khac | GIET | c33_trung_chu_khac_job | không mở finding;  |
| mutants/results.json | A20i_zip_bo_dem_nhom | GIET | c36_ghep_lech_so | không mở finding;  |
| mutants/results.json | A20ii_zip_bo_dem_yaml | GIET | c36_ghep_lech_so | không mở finding;  |
| mutants/results.json | A21_bo_kiem_ten | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | ten_none_bang_none | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | ten_chi_buoc_chay | GIET | c45_buoc_skipped_giua | không mở finding;  |
| mutants/results.json | ten_name_khong_chuoi | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | ten_name_rong_bo_qua | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | ten_v_khong_chuoi | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | ten_rstrip | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | loc_post_khong_cach | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | chay_chi_success | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | dem_chi_khi_thua_nhom | GIET | c36_ghep_lech_so | không mở finding;  |
| mutants/results.json | dem_chi_khi_thieu_rest | GIET | c36_ghep_lech_so | không mở finding;  |
| mutants/results.json | gio_theo_thu_tu_tho | GIET | c45_buoc_skipped_giua | không mở finding;  |
| mutants/results.json | vi_tri_theo_thu_tu_tho | GIET | c45_buoc_skipped_giua | không mở finding;  |
| mutants/results.json | wf_none_khai_passed | GIET | c32_workflow_khong_doc_duoc | không mở finding;  |
| mutants/results.json | gio_match_thay_fullmatch | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | job_hau_to_bat_ky | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | job_hau_to_khong_ngoac | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | job_cho_x_rong | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | gio_bo_kiem_str | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | gio_bo_bat_ValueError | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | job_chi_name_khi_co_name | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | L3_number_bool | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_number_float | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_alias_name_bo | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_ma_tran_khac_rong | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_ma_tran_dotall | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_post_o_giua | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_run_rstrip_het | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_run_ep_chuoi | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_bo_dedupe | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_endgroup_startswith | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_shell_khong_cach | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_truoc_bo_buoc_dau | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_truoc_chi_lien_ke | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | L3_env_bo_dang | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_env_truthy | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_env_chi_chuoi | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_env_wf_co_mat | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_defaults_wf_truthy | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_defaults_job_truthy | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_shell_bo_pwsh | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_shell_bo_sh | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_shell_null_mac_dinh | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_khoa_bo_id | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_khoa_bo_if | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_khoa_bo_timeout | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | L3_khoa_bo_coe | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | O_job_none_and | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | O_var_mot_dong_all | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | O_goi_or | GIET | c23_chi_loi_goi_that | không mở finding;  |
| mutants/results.json | O_goi_any | GIET | c23_chi_loi_goi_that | không mở finding;  |
| mutants/results.json | N_ten_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_ten_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_job_match | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_job_khoang_trang_ngoac | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_ten_run_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_ten_splitlines | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_ten_name_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_rest_ten_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_meta_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_post_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_post_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_concl_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_concl_timed_out | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_env_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | D01_null_coi_nhu_vang | GIET | c46_mien_che_do | không mở finding;  |
| mutants/results.json | N_defaults_none | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_github_re_I | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_github_dollar | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_mau_rong | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_header_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_in_lai_strip | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | N_in_lai_rstrip | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | N_group_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_long_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_shell_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_endgroup_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_run_join_rstrip | GIET | c47_bien_ghep | không mở finding;  |
| mutants/results.json | N_run_cr | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_gio_Z_tuy_chon | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_khoa_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_uses_rong | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_uses_job_rong | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_name_present_none | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | N_run_truoc_uses | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_job_escape_alias | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_job_alias_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_job_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_name_explicit_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_name_explicit_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_metadata_setup_prefix | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_metadata_complete_prefix | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_metadata_post_suffix | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_ran_neutral_excluded | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_ran_cancelled_excluded | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_env_prefix_empty_suffix | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_env_prefix_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_mode_step_key_truthy | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_mode_shell_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_mode_shell_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_mode_prior_requires_ran | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_run_compare_strip_newlines | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_header_lstrip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_shell_lstrip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L4_number_contiguous | GIET | c36_ghep_lech_so | không mở finding;  |
| mutants/results.json | L5_wf_env_dict_only | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_wf_env_nonempty_only | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_env_chi_khoa_dau | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_env_chi_khoa_cuoi | GIET | c29_che_do_env_job | không mở finding;  |
| mutants/results.json | L5_env_false_cho_qua | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_env_int_cho_qua | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_env_chuoi_rong_cho_qua | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_env_gia_tri_rong_cho_qua | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_che_do_buoc_run_dau | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_dd_job_dau | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_job_uu_tien_khop_dung | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_job_ten_dai_bo_hau_to | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_gio_completed_cua_buoc_cuoi | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_truoc_chi_run_chuoi | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_github_cuoi_chuoi | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_github_ranh_gioi_tu | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L5_mau_doi_reset | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L5_khoi_rstrip_ca_khoi | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L5_run_bo_mot_lf | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L5_uses_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L5_goi_strip_toan_run | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| mutants/results.json | L5_D01_null_la_vang | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| mutants/results.json | L6_job_ascii_suffix | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_job_alias_truncate | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_job_nonempty_rest_required | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_rest_number_under_100 | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_rest_skipped_time_required | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_time_require_same_day | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_time_reject_year_before_2000 | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_time_accept_invalid_leap_day | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_names_compare_as_strings | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_prior_entire_step_instead_run | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_prior_uses_preferred | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_first_output_line | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_last_output_line | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_output_strip | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_reverse_output | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_endgroup_need_shell_first | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_uncolored_metadata_add_to_echo | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_shell_nonempty | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_color_prefix_only | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_log_color_without_timestamp | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_run_blank_lines_disallowed | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_rest_also_skip_null | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_yaml_empty_workflow_reject | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | L6_rest_number_order_contiguous | GIET | c50_mien_luot6 | không mở finding;  |
| mutants/results.json | job_bo_x_str | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | so_number_0 | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | so_number_am | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | sy_khong_list | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | dd_run_khong_chuoi | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | A22_bo_kiem_gio | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | A22_khong_cat_giay | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | F09_bo_kiem_lich | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | F09_nhan_offset | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | F09_header_thieu_dung_rest | GIET | c38_ghep_lech_gio | không mở finding;  |
| mutants/results.json | F10_bo_sort | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | F10_bo_number_trung | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | F10_ten_lstrip | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | F10_name_bieu_thuc | GIET | c37_ghep_lech_ten | không mở finding;  |
| mutants/results.json | dang_bo_number | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | dang_buoc_rest_khong_dict | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | dang_buoc_yaml_khong_dict | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | dang_job_khong_dict | GIET | c44_ghep_sai_dang | không mở finding;  |
| mutants/results.json | A23_lay_khoa_dau | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | A23_nhan_job_goi_lai | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | A23_nhan_bieu_thuc | GIET | c39_ghep_job | không mở finding;  |
| mutants/results.json | A24_bo_luat_nhom_long | GIET | c40_nhom_long | không mở finding;  |
| mutants/results.json | A25i_uses_sinh_marker | GIET | c41_buoc_uses | không mở finding;  |
| mutants/results.json | A25ii_zip_bo_dem_nhom | GIET | c41_buoc_uses | không mở finding;  |
| mutants/results.json | A27_khoi_bang_buoc_khac | GIET | c43_khoi_khac_buoc | không mở finding;  |
| mutants/results.json | F01_steps_chi_la_list | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F05_chieu_khong_an_toan | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F05_luoi_cuoi | GIET | c19_rest_loi | không mở finding;  |
| mutants/results.json | F02_khong_noi_dong | GIET | c23_chi_loi_goi_that | không mở finding;  |
| mutants/results.json | F02_cho_moi_co | GIET | c23_chi_loi_goi_that | không mở finding;  |
| mutants/results.json | F01_bool_la_int | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_chuoi_rong | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_conclusion_bat_ky | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_labels_rong | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_check_run_bat_ky | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_head_sha_bat_ky | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_head_sha_nhan_newline | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_check_run_nhan_newline | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_artifact_khong_kiem | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F01_phong_bi_khong_kiem | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| mutants/results.json | F03_bo_kiem_total_doi | GIET | c20_du_trang | không mở finding;  |
| mutants/results.json | F05_than_run_sai_dang | GIET | c19_rest_loi | không mở finding;  |
| mutants/results.json | F05_loi_ghi_mat_dong_dem | GIET | c19_rest_loi | không mở finding;  |
| mutants/results.json | F05_sai_doi_so_mat_dong_dem | GIET | c01_cli_du_co | không mở finding;  |
| mutants/results.json | F05_rest_mat_dong_dem | GIET | c19_rest_loi | không mở finding;  |
| mutants/results.json | F06_redirect_lot_loi | GIET | c24_goi_that_loi_va_chuyen_huong | không mở finding;  |
| mutants/results.json | F06_redirect_mang_token | GIET | c24_goi_that_loi_va_chuyen_huong | không mở finding;  |
| mutants/results.json | vo_can_AttributeError_qua_except_doi_kieu | TIN_DUNG_GIA | c03_checkout_linux | tự kiểm có chủ ý: TIN_DUNG_GIA;  |
| mutants/results.json | chi_them_chu_thich | SONG_SOT | c20_du_trang | tự kiểm có chủ ý: SONG_SOT;  |
| historical-targets6/results.json | job_rest_type | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| historical-targets6/results.json | job_match_search | GIET | c39_ghep_job | không mở finding;  |
| historical-targets6/results.json | job_matrix_nonempty | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | job_dotall_add | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | job_alias_exact_drop | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | name_use_last_line | GIET | c26_f02_dong_khong_mau | không mở finding;  |
| historical-targets6/results.json | name_rest_strip | GIET | c37_ghep_lech_ten | không mở finding;  |
| historical-targets6/results.json | time_drop_type | HONG_NEO | c38_ghep_lech_gio | lỗi dựng phép đo; không nhận tín dụng;  |
| historical-targets6/results.json | time_year0_drop | GIET | c38_ghep_lech_gio | không mở finding;  |
| historical-targets6/results.json | time_calendar_date_only | GIET | c38_ghep_lech_gio | không mở finding;  |
| historical-targets6/results.json | time_low_strict | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | time_hi_strict | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | time_or_bounds | GIET | c38_ghep_lech_gio | không mở finding;  |
| historical-targets6/results.json | time_low_only | GIET | c38_ghep_lech_gio | không mở finding;  |
| historical-targets6/results.json | time_hi_only | GIET | c38_ghep_lech_gio | không mở finding;  |
| historical-targets6/results.json | rest_number_float | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | rest_number_bool | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | rest_steps_list_drop | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| historical-targets6/results.json | rest_steps_all_any | GIET | c44_ghep_sai_dang | không mở finding;  |
| historical-targets6/results.json | yaml_steps_all_any | GIET | c44_ghep_sai_dang | không mở finding;  |
| historical-targets6/results.json | number_sort_desc | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | metadata_keep_setup | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | metadata_keep_complete | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | metadata_post_anywhere | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | mode_env_shape_drop | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_env_prefix_exact | GIET | c29_che_do_env_job | không mở finding;  |
| historical-targets6/results.json | mode_shell_no_pwsh | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_shell_no_sh | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_shell_null_default | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_env_presence_not_value | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_env_job_presence | HONG_NEO | c29_che_do_env_job | lỗi dựng phép đo; không nhận tín dụng;  |
| historical-targets6/results.json | mode_key_id_drop | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_key_if_drop | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_key_timeout_drop | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_key_coe_drop | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_prior_skip_first | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | mode_prior_only_first | GIET | c42_github_env_cung_job | không mở finding;  |
| historical-targets6/results.json | mode_prior_only_last | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | mode_prior_include_current | GIET | c42_github_env_cung_job | không mở finding;  |
| historical-targets6/results.json | run_rstrip_all | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | run_type_coerce | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | dd_group_reverse | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | dd_map_reverse | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | dd_output_dedupe | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | log_group_close_exact | HONG_NEO |  | lỗi dựng phép đo; không nhận tín dụng;  |
| historical-targets6/results.json | log_shell_suffix | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | log_nested_before_only | GIET | c40_nhom_long | không mở finding;  |
| historical-targets6/results.json | log_nested_after_only | SONG_SOT | 50 ca; xem JSON | P3 / tương đương; Cấu trúc trước shell đã từ chối nhóm lồng, sau shell hai predicate giống nhau; equivalence.json. |
| historical-targets6/results.json | log_prefix_drop_ok | GIET | c35_f02_khoi_khong_tron_ven | không mở finding;  |
| historical-targets6/results.json | log_close_ignore_prefix | GIET | c35_f02_khoi_khong_tron_ven | không mở finding;  |
| historical-targets6/results.json | mode_defaults_wf_truthy | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_defaults_job_truthy | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_env_truthy | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | mode_env_string_only | GIET | c46_mien_che_do | không mở finding;  |
| historical-targets6/results.json | number_type_bool_guard_drop | GIET | c47_bien_ghep | không mở finding;  |
| historical-targets6/results.json | number_min_strict | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | header_time_other_group | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | header_window_other_step | GIET | c38_ghep_lech_gio | không mở finding;  |
| historical-targets6/results.json | time_current_end_other_step | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | name_only_first_rest | GIET | c37_ghep_lech_ten | không mở finding;  |
| historical-targets6/results.json | name_only_last_rest | GIET | c45_buoc_skipped_giua | không mở finding;  |
| historical-targets6/results.json | job_escape_alias | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | job_alias_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | job_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | name_explicit_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | name_explicit_casefold | GIET | c37_ghep_lech_ten | không mở finding;  |
| historical-targets6/results.json | metadata_setup_prefix | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | metadata_complete_prefix | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | metadata_post_suffix | GIET | c12_marker_khong_khop | không mở finding;  |
| historical-targets6/results.json | ran_neutral_excluded | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | ran_cancelled_excluded | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | env_prefix_empty_suffix | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | env_prefix_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | mode_step_key_truthy | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | mode_shell_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | mode_shell_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | mode_prior_requires_ran | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | run_compare_strip_newlines | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | header_lstrip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | shell_lstrip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| historical-targets6/results.json | number_contiguous | GIET | c36_ghep_lech_so | không mở finding;  |
| operators6-combined.json | L154c17:'in'->'not in' | GIET+NEM | c49_oracle_nhieu_truc | không mở finding;  |
| operators6-combined.json | L154c22:'and'->'or' | GIET+NEM | c49_oracle_nhieu_truc | không mở finding;  |
| operators6-combined.json | L154c42:'is not'->'is' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L154c54:'or'->'and' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L154c57:'any'->'all' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L162c26:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L162c34:'and'->'or' | GIET | c32_workflow_khong_doc_duoc | không mở finding;  |
| operators6-combined.json | L162c59:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L166c58:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L166c65:'and'->'or' | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| operators6-combined.json | L166c77:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L166c85:'and'->'or' | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| operators6-combined.json | L166c89:'any'->'all' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L167c16:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L167c23:'and'->'or' | GIET | c33_trung_chu_khac_job | không mở finding;  |
| operators6-combined.json | L167c29:'and'->'or' | GIET | c33_trung_chu_khac_job | không mở finding;  |
| operators6-combined.json | L167c39:'not in'->'in' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L167c48:'and'->'or' | GIET | c33_trung_chu_khac_job | không mở finding;  |
| operators6-combined.json | L168c16:'0'->'1' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L168c32:'=='->'!=' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L168c35:'1'->'2' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L168c35:'1'->'0' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L171c14:'in'->'not in' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L172c46:'and'->'or' | GIET+NEM | c37_ghep_lech_ten | không mở finding;  |
| operators6-combined.json | L172c56:'not in'->'in' | GIET | c31_che_do_duong_khac | không mở finding;  |
| operators6-combined.json | L174c34:'0'->'1' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L178c45:'19'->'20' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L178c45:'19'->'18' | GIET | c38_ghep_lech_gio | không mở finding;  |
| operators6-combined.json | L178c82:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L178c89:'and'->'or' | GIET | c38_ghep_lech_gio | không mở finding;  |
| operators6-combined.json | L187c10:'is'->'is not' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L191c9:'is'->'is not' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L191c17:'or'->'and' | GIET+NEM | c39_ghep_job | không mở finding;  |
| operators6-combined.json | L191c27:'in'->'not in' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L191c44:'or'->'and' | GIET | c39_ghep_job | không mở finding;  |
| operators6-combined.json | L191c56:'is not'->'is' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L191c68:'or'->'and' | GIET | c44_ghep_sai_dang | không mở finding;  |
| operators6-combined.json | L191c71:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L191c75:'all'->'any' | GIET | c44_ghep_sai_dang | không mở finding;  |
| operators6-combined.json | L191c87:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L193c7:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L193c21:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L193c29:'and'->'or' | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| operators6-combined.json | L193c33:'all'->'any' | GIET | c44_ghep_sai_dang | không mở finding;  |
| operators6-combined.json | L193c45:'is'->'is not' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L193c53:'and'->'or' | GIET+NEM | c44_ghep_sai_dang | không mở finding;  |
| operators6-combined.json | L193c78:'1'->'2' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L193c78:'1'->'0' | GIET | c44_ghep_sai_dang | không mở finding;  |
| operators6-combined.json | L194c12:'and'->'or' | GIET | c22_thieu_dinh_danh_khong_passed | không mở finding;  |
| operators6-combined.json | L194c47:'=='->'!=' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L196c77:'not in'->'in' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L197c11:'and'->'or' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L197c15:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L198c64:'!='->'==' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L199c17:'!='->'==' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L201c16:'!='->'==' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L203c7:'any'->'all' | GIET | c37_ghep_lech_ten | không mở finding;  |
| operators6-combined.json | L203c11:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L203c37:'or'->'and' | GIET | c37_ghep_lech_ten | không mở finding;  |
| operators6-combined.json | L203c54:'!='->'==' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L205c7:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L205c11:'all'->'any' | GIET | c38_ghep_lech_gio | không mở finding;  |
| operators6-combined.json | L205c53:'and'->'or' | GIET+NEM | c38_ghep_lech_gio | không mở finding;  |
| operators6-combined.json | L206c15:'and'->'or' | GIET+NEM | c38_ghep_lech_gio | không mở finding;  |
| operators6-combined.json | L206c41:'and'->'or' | GIET+NEM | c38_ghep_lech_gio | không mở finding;  |
| operators6-combined.json | L206c47:'<='->'<' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L206c52:'<='->'<' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L214c27:'in'->'not in' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L214c33:'or'->'and' | GIET | c31_che_do_duong_khac | không mở finding;  |
| operators6-combined.json | L214c50:'or'->'and' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L214c64:'in'->'not in' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L214c69:'or'->'and' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L214c85:'or'->'and' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L215c16:'or'->'and' | GIET | c28_che_do_env_buoc | không mở finding;  |
| operators6-combined.json | L215c42:'not in'->'in' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L216c16:'or'->'and' | GIET | c31_che_do_duong_khac | không mở finding;  |
| operators6-combined.json | L216c19:'any'->'all' | GIET | c42_github_env_cung_job | không mở finding;  |
| operators6-combined.json | L262c91:'True'->'False' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L262c103:'True'->'False' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L262c120:'True'->'False' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L263c35:'19'->'20' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L263c35:'19'->'18' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L264c18:'and'->'or' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L264c34:'1'->'2' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L264c34:'1'->'0' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L265c31:'in'->'not in' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L266c17:'=='->'!=' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L267c26:'False'->'True' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L268c21:'and'->'or' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L271c48:'and'->'or' | GIET | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L271c52:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L271c60:'and'->'or' | GIET | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L271c64:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L271c94:'and'->'or' | GIET | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L272c20:'not'->'' | GIET | c47_bien_ghep | không mở finding;  |
| operators6-combined.json | L272c37:'or'->'and' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L272c66:'False'->'True' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L274c18:'1'->'2' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L274c18:'1'->'0' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L275c27:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L275c39:'and'->'or' | GIET | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L275c51:'and'->'or' | GIET | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L275c55:'not'->'' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L275c72:'and'->'or' | GIET | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L275c89:'1'->'2' | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| operators6-combined.json | L275c89:'1'->'0' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L275c92:'=='->'!=' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L291c17:'0'->'1' | GIET | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L292c36:'or'->'and' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L294c37:'not in'->'in' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L295c11:'not'->'' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L295c26:'is'->'is not' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L295c33:'and'->'or' | GIET+NEM | c25_f02_env_mang_mau | không mở finding;  |
| operators6-combined.json | L295c49:'and'->'or' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L295c70:'=='->'!=' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L297c14:'1'->'2' | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| operators6-combined.json | L297c14:'1'->'0' | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| operators6-combined.json | L299c35:'or'->'and' | GIET | c28_che_do_env_buoc | không mở finding;  |
| operators6-combined.json | L299c38:'any'->'all' | GIET | c46_mien_che_do | không mở finding;  |
| operators6-combined.json | L299c44:'and'->'or' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L299c50:'1'->'2' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L299c50:'1'->'0' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L300c38:'2'->'3' | GIET+NEM | c44_ghep_sai_dang | không mở finding;  |
| operators6-combined.json | L300c38:'2'->'1' | GIET | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L300c62:'and'->'or' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L300c66:'all'->'any' | GIET+NEM | c23_chi_loi_goi_that | không mở finding;  |
| operators6-combined.json | L302c21:'not in'->'in' | GIET+NEM | c12_marker_khong_khop | không mở finding;  |
| operators6-combined.json | L302c32:'or'->'and' | GIET+NEM | c28_che_do_env_buoc | không mở finding;  |
| operators6-combined.json | L303c102:'not in'->'in' | GIET | c28_che_do_env_buoc | không mở finding;  |
| operators6-combined.json | L307c98:'0'->'1' | GIET | c12_marker_khong_khop | không mở finding;  |
| operator-errors6-results.json | L154c17:'in'->'not in' | TIN_DUNG_GIA | c12_marker_khong_khop | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L154c17:'in'->'not in' | TIN_DUNG_GIA | c13_marker_buoc_khac | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L154c17:'in'->'not in' | TIN_DUNG_GIA | c14_ngoai_moi | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L154c22:'and'->'or' | TIN_DUNG_GIA | c12_marker_khong_khop | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L154c22:'and'->'or' | TIN_DUNG_GIA | c13_marker_buoc_khac | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L154c22:'and'->'or' | TIN_DUNG_GIA | c14_ngoai_moi | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c16:'0'->'1' | TIN_DUNG_GIA | c02_attempt_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c16:'0'->'1' | TIN_DUNG_GIA | c03_checkout_linux | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c16:'0'->'1' | TIN_DUNG_GIA | c04_checkout_windows | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c32:'=='->'!=' | TIN_DUNG_GIA | c22_thieu_dinh_danh_khong_passed | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c32:'=='->'!=' | TIN_DUNG_GIA | c47_bien_ghep | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c32:'=='->'!=' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c35:'1'->'0' | TIN_DUNG_GIA | c22_thieu_dinh_danh_khong_passed | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c35:'1'->'0' | TIN_DUNG_GIA | c47_bien_ghep | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L168c35:'1'->'0' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L171c14:'in'->'not in' | TIN_DUNG_GIA | c02_attempt_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L171c14:'in'->'not in' | TIN_DUNG_GIA | c03_checkout_linux | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L171c14:'in'->'not in' | TIN_DUNG_GIA | c04_checkout_windows | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L172c46:'and'->'or' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L174c34:'0'->'1' | TIN_DUNG_GIA | c02_attempt_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L174c34:'0'->'1' | TIN_DUNG_GIA | c03_checkout_linux | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L174c34:'0'->'1' | TIN_DUNG_GIA | c04_checkout_windows | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L187c10:'is'->'is not' | TIN_DUNG_GIA | c05_checkout_khong_sha | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L187c10:'is'->'is not' | TIN_DUNG_GIA | c06_checkout_hai_sha | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L187c10:'is'->'is not' | TIN_DUNG_GIA | c07_checkout_push_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L191c9:'is'->'is not' | TIN_DUNG_GIA | c22_thieu_dinh_danh_khong_passed | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L191c9:'is'->'is not' | TIN_DUNG_GIA | c47_bien_ghep | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L191c9:'is'->'is not' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L191c17:'or'->'and' | TIN_DUNG_GIA | c22_thieu_dinh_danh_khong_passed | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L191c17:'or'->'and' | TIN_DUNG_GIA | c47_bien_ghep | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L191c17:'or'->'and' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L193c53:'and'->'or' | TIN_DUNG_GIA | c22_thieu_dinh_danh_khong_passed | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L205c53:'and'->'or' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L206c15:'and'->'or' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L206c41:'and'->'or' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L264c18:'and'->'or' | TIN_DUNG_GIA | c02_attempt_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L264c18:'and'->'or' | TIN_DUNG_GIA | c03_checkout_linux | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L264c18:'and'->'or' | TIN_DUNG_GIA | c04_checkout_windows | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L264c34:'1'->'2' | TIN_DUNG_GIA | c06_checkout_hai_sha | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L264c34:'1'->'2' | TIN_DUNG_GIA | c47_bien_ghep | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L264c34:'1'->'2' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L274c18:'1'->'2' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L292c36:'or'->'and' | TIN_DUNG_GIA | c05_checkout_khong_sha | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L292c36:'or'->'and' | TIN_DUNG_GIA | c06_checkout_hai_sha | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L292c36:'or'->'and' | TIN_DUNG_GIA | c07_checkout_push_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c11:'not'->'' | TIN_DUNG_GIA | c02_attempt_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c11:'not'->'' | TIN_DUNG_GIA | c03_checkout_linux | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c11:'not'->'' | TIN_DUNG_GIA | c04_checkout_windows | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c26:'is'->'is not' | TIN_DUNG_GIA | c41_buoc_uses | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c26:'is'->'is not' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c33:'and'->'or' | TIN_DUNG_GIA | c41_buoc_uses | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c33:'and'->'or' | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c49:'and'->'or' | TIN_DUNG_GIA | c02_attempt_lech | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c49:'and'->'or' | TIN_DUNG_GIA | c03_checkout_linux | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L295c49:'and'->'or' | TIN_DUNG_GIA | c04_checkout_windows | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L299c44:'and'->'or' | TIN_DUNG_GIA | c30_che_do_doi_so | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L299c44:'and'->'or' | TIN_DUNG_GIA | c42_github_env_cung_job | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L299c44:'and'->'or' | TIN_DUNG_GIA | c47_bien_ghep | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L300c38:'2'->'3' | TIN_DUNG_GIA | c12_marker_khong_khop | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L300c38:'2'->'3' | TIN_DUNG_GIA | c13_marker_buoc_khac | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L300c38:'2'->'3' | TIN_DUNG_GIA | c14_ngoai_moi | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L300c62:'and'->'or' | TIN_DUNG_GIA | c27_f02_yaml_khong_toi_gian | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L300c62:'and'->'or' | TIN_DUNG_GIA | c30_che_do_doi_so | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L300c62:'and'->'or' | TIN_DUNG_GIA | c42_github_env_cung_job | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L300c66:'all'->'any' | TIN_DUNG_GIA | c27_f02_yaml_khong_toi_gian | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L302c21:'not in'->'in' | TIN_DUNG_GIA | c13_marker_buoc_khac | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L302c21:'not in'->'in' | TIN_DUNG_GIA | c14_ngoai_moi | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L302c21:'not in'->'in' | TIN_DUNG_GIA | c27_f02_yaml_khong_toi_gian | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L302c32:'or'->'and' | TIN_DUNG_GIA | c13_marker_buoc_khac | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L302c32:'or'->'and' | TIN_DUNG_GIA | c14_ngoai_moi | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| operator-errors6-results.json | L302c32:'or'->'and' | TIN_DUNG_GIA | c27_f02_yaml_khong_toi_gian | ngoại lệ vô can; không nhận tín dụng; chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca |
| normalization6-results.json | n_ten_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_ten_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_job_match | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_job_khoang_trang_ngoac | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_ten_run_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_ten_splitlines | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_ten_name_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_rest_ten_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_meta_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_post_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_post_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_concl_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_concl_timed_out | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_env_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_env_v_truthy | TIN_DUNG_GIA | c48_nguyen_van_va_mien | ngoại lệ vô can; không nhận tín dụng;  |
| normalization6-results.json | n_defaults_none | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_github_re_I | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_github_dollar | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_mau_rong | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_header_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_in_lai_strip | GIET | c47_bien_ghep | không mở finding;  |
| normalization6-results.json | n_in_lai_rstrip | GIET | c47_bien_ghep | không mở finding;  |
| normalization6-results.json | n_group_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_long_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_shell_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_endgroup_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_run_join_rstrip | GIET | c47_bien_ghep | không mở finding;  |
| normalization6-results.json | n_run_cr | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_goi_strip_run | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_gio_Z_tuy_chon | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_khoa_lower | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_uses_rong | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_uses_job_rong | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_name_present_none | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| normalization6-results.json | n_run_truoc_uses | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier5/results.json | wf_env_dict_only | GIET | c46_mien_che_do | không mở finding;  |
| frontier5/results.json | wf_env_nonempty_only | GIET | c46_mien_che_do | không mở finding;  |
| frontier5/results.json | job_env_only_first_key | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | job_env_only_last_key | GIET | c29_che_do_env_job | không mở finding;  |
| frontier5/results.json | mode_last_step | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | mode_first_run_step | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | mode_first_job | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | dd_first_job | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | job_match_exact_preference | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | job_first_prefix_only | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | metadata_first_setup_only | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier5/results.json | metadata_complete_last_only | GIET | c36_ghep_lech_so | không mở finding;  |
| frontier5/results.json | time_name_first_key | GIET | c38_ghep_lech_gio | không mở finding;  |
| frontier5/results.json | time_name_last_key | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | time_only_first_group | GIET | c38_ghep_lech_gio | không mở finding;  |
| frontier5/results.json | time_only_last_group | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | name_skip_first_yaml | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | name_skip_last_yaml | GIET | c37_ghep_lech_ten | không mở finding;  |
| frontier5/results.json | rest_sort_lexical | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | rest_sort_input | GIET | c37_ghep_lech_ten | không mở finding;  |
| frontier5/results.json | rest_number_integral_float | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | ghep_zero_groups_reject | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | env_false_accept | GIET | c46_mien_che_do | không mở finding;  |
| frontier5/results.json | env_int_accept | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | env_empty_str_accept | GIET | c46_mien_che_do | không mở finding;  |
| frontier5/results.json | prior_run_only_strings | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | prior_github_match | GIET | c42_github_env_cung_job | không mở finding;  |
| frontier5/results.json | prior_path_suffix | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | prior_env_word_boundary | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier5/results.json | nested_exact_only | GIET | c40_nhom_long | không mở finding;  |
| frontier5/results.json | nested_only_after_shell | SONG_SOT | 50 ca; xem JSON | P3 / tương đương; Cùng predicate log_nested_after_only; không đếm thành lớp mới. |
| frontier5/results.json | nested_only_before_shell | GIET | c40_nhom_long | không mở finding;  |
| frontier5/results.json | header_colored_exact | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier5/results.json | header_seconds_18 | GIET | c12_marker_khong_khop | không mở finding;  |
| frontier5/results.json | header_seconds_round | GIET | c12_marker_khong_khop | không mở finding;  |
| frontier5/results.json | run_blank_tail_only | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier5/results.json | run_trailing_lf_exact | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier5/results.json | run_first_group_only | GIET | c12_marker_khong_khop | không mở finding;  |
| frontier5/results.json | run_last_group_only | GIET | c13_marker_buoc_khac | không mở finding;  |
| frontier5/results.json | minimal_reverse_lines | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| frontier5/results.json | minimal_first_line_only | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| frontier5/results.json | name_uses_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier5/results.json | name_run_prefer_uses | GIET | c41_buoc_uses | không mở finding;  |
| frontier5/results.json | name_remove_blank_lines | GIET | c37_ghep_lech_ten | không mở finding;  |
| frontier5/results.json | name_reject_empty_line | GIET | c37_ghep_lech_ten | không mở finding;  |
| frontier5/results.json | env_prefix_value_only | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier6/results.json | job_nested_parentheses | GIET | c47_bien_ghep | không mở finding;  |
| frontier6/results.json | job_ascii_suffix | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | job_one_suffix_item | GIET | c39_ghep_job | không mở finding;  |
| frontier6/results.json | job_alias_truncate | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | job_only_named_keys | GIET | c39_ghep_job | không mở finding;  |
| frontier6/results.json | job_drop_unmatched_bad_jobs | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier6/results.json | job_requires_nonempty_steps | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier6/results.json | job_nonempty_rest_required | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | rest_number_under_100 | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | rest_number_order_contiguous | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | rest_skipped_time_required | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | name_explicit_nonblank_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | name_uses_fallback_falsy_run | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | name_has_run_uses_prefer | GIET | c41_buoc_uses | không mở finding;  |
| frontier6/results.json | name_crlf_split | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | time_second_start_plus_one | GIET | c12_marker_khong_khop | không mở finding;  |
| frontier6/results.json | time_nonzero_duration | GIET | c12_marker_khong_khop | không mở finding;  |
| frontier6/results.json | time_require_same_day | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | time_reject_leap_day | GIET | c38_ghep_lech_gio | không mở finding;  |
| frontier6/results.json | time_reject_year_before_2000 | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | time_accept_invalid_leap_day | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | time_header_first_position | GIET | c12_marker_khong_khop | không mở finding;  |
| frontier6/results.json | time_skip_middle | GIET | c38_ghep_lech_gio | không mở finding;  |
| frontier6/results.json | names_skip_middle | GIET | c37_ghep_lech_ten | không mở finding;  |
| frontier6/results.json | names_compare_as_strings | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | env_only_keys_str | SONG_SOT | 50 ca; xem JSON | P3 / tương đương; Khoá scalar safe YAML không phải str không có tiền tố CI_DANG_KY_; không ép giết. |
| frontier6/results.json | env_ignore_false_values | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier6/results.json | env_ignore_empty_collections | GIET | c46_mien_che_do | không mở finding;  |
| frontier6/results.json | env_prefix_full_key | GIET | c29_che_do_env_job | không mở finding;  |
| frontier6/results.json | env_suffix_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | prior_entire_step_instead_run | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | prior_uses_preferred | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | prior_ignore_if_empty_env | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier6/results.json | prior_only_last_two | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier6/results.json | prior_only_first | GIET | c42_github_env_cung_job | không mở finding;  |
| frontier6/results.json | prior_case_insensitive | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | step_allow_env_empty | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | step_defaults_null_allowed | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | workflow_defaults_null_allowed | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | mode_no_sh | GIET | c46_mien_che_do | không mở finding;  |
| frontier6/results.json | mode_allow_empty_shell | GIET | c46_mien_che_do | không mở finding;  |
| frontier6/results.json | log_first_output_line | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_last_output_line | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_output_strip | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_reverse_output | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_reject_metadata_after_shell | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | log_endgroup_need_shell_first | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_uncolored_metadata_add_to_echo | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_shell_nonempty | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_color_prefix_only | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | log_color_without_timestamp | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | run_reverse_calls | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| frontier6/results.json | run_sort_calls | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| frontier6/results.json | run_drop_last_call | GIET | c12_marker_khong_khop | không mở finding;  |
| frontier6/results.json | run_no_dedup | GIET | c47_bien_ghep | không mở finding;  |
| frontier6/results.json | run_unknown_omitted | GIET | c13_marker_buoc_khac | không mở finding;  |
| frontier6/results.json | run_unknown_priority | GIET | c46_mien_che_do | không mở finding;  |
| frontier6/results.json | run_blank_lines_disallowed | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | run_blank_counted | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| frontier6/results.json | run_strip_carriage | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | run_strip_match_only | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | rest_post_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | rest_skipped_casefold | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier6/results.json | rest_also_skip_null | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6/results.json | yaml_empty_workflow_reject | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6-extra/results.json | rest_number_min_one_safe | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6-extra2/results.json | job_nested_suffix_pure | GIET | c50_mien_luot6 | không mở finding;  |
| frontier6-extra3/results.json | time_reject_leap_day_safe | GIET | c50_mien_luot6 | không mở finding;  |
| frontier7/results.json | job_key_equals_alias_reject | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier7/results.json | job_alias_suffix_only_key | GIET | c39_ghep_job | không mở finding;  |
| frontier7/results.json | job_suffix_no_dot | GIET | c47_bien_ghep | không mở finding;  |
| frontier7/results.json | job_alias_unicode_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | job_alias_trim | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier7/results.json | job_alias_matches_duplicate_count | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier7/results.json | name_explicit_strip | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier7/results.json | name_explicit_unicode_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | name_uses_whole_value | SONG_SOT | 50 ca; xem JSON | P3 / D02; uses nhiều dòng: chưa có chính sách cho action reference malformed; cần owner chốt so toàn giá trị hoặc từ chối, chưa có runner evidence |
| frontier7/results.json | name_run_empty_first_reject | GIET | c37_ghep_lech_ten | không mở finding;  |
| frontier7/results.json | name_run_strip_cr | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier7/results.json | time_same_year | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | time_same_month | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | time_24h_window | GIET | c50_mien_luot6 | không mở finding;  |
| frontier7/results.json | time_century_leap_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | time_year_9999_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | time_year_0001_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | time_date_only_compare | GIET | c38_ghep_lech_gio | không mở finding;  |
| frontier7/results.json | time_clock_only_compare | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | time_whitespace_strip | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | time_invalid_century_accept | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | rest_number_no_gaps | GIET | c36_ghep_lech_so | không mở finding;  |
| frontier7/results.json | rest_number_metadata_ignored_validation | GIET | c47_bien_ghep | không mở finding;  |
| frontier7/results.json | rest_metadata_time_required | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | rest_filter_post_number_order | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | rest_filter_skipped_uses_only | GIET+NEM | c45_buoc_skipped_giua | không mở finding;  |
| frontier7/results.json | rest_names_only_ran | GIET | c45_buoc_skipped_giua | không mở finding;  |
| frontier7/results.json | rest_number_max_as_count | GIET | c50_mien_luot6 | không mở finding;  |
| frontier7/results.json | mode_env_present_values_only | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | mode_env_empty_key_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | mode_env_unicode_key_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | mode_prior_skip_uses | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | mode_prior_skip_skipped | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| frontier7/results.json | mode_prior_only_unblocked | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| frontier7/results.json | mode_prior_strip_empty_run | SONG_SOT | 50 ca; xem JSON | P3 / tương đương; Thay str(v) bằng str(v or "") chỉ đổi các giá trị falsy; không giá trị nào trong miền yaml.safe_load ấy chứa GITHUB_ENV/PATH. |
| frontier7/results.json | mode_step_shell_nonempty | GIET | c46_mien_che_do | không mở finding;  |
| frontier7/results.json | dd_first_match_lines_only | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_last_match_lines_only | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_blank_output_lines_remove | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_no_output_final_newline | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_dedup_output_lines | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_sort_output_lines | GIET | c50_mien_luot6 | không mở finding;  |
| frontier7/results.json | dd_sort_match_lines | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_wrong_lenh_first_call | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_truncate_path | GIET | c23_chi_loi_goi_that | không mở finding;  |
| frontier7/results.json | dd_step_dedup_paths | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | dd_validated_step_count_calls | GIET | c27_f02_yaml_khong_toi_gian | không mở finding;  |
| frontier7/results.json | log_output_ignore_indented_blank | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | log_header_strip | GIET | c47_bien_ghep | không mở finding;  |
| frontier7/results.json | log_empty_metadata_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | log_second_shell_reject | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | log_output_drop_group_lines | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | log_require_output_nonempty | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | log_require_metadata_no_ansi | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | log_color_run_not_contains_shell | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof7-results.json |
| frontier7/results.json | log_header_full_timestamp_required | SONG_SOT | 50 ca; xem JSON | P3 / tương đương ở đầu ra công khai; Header không có RE_DONG hợp lệ không thể có giờ hợp lệ cho M12(c); hai đường đều không ghép/sinh marker. |
| frontier7/results.json | log_same_header_body_len_reject | GIET | c47_bien_ghep | không mở finding;  |
| frontier7b/results.json | job_suffix_no_dot_pure | SONG_SOT | 50 ca; xem JSON | P1 / F10; 50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; proof-repairs7-results.json |
| frontier7b/results.json | name_run_crlf_first_line | GIET | c48_nguyen_van_va_mien | không mở finding;  |
| reanchored6-results.json | time_drop_type | GIET | c38_ghep_lech_gio | không mở finding;  |
| reanchored6-results.json | mode_env_job_presence | GIET | c46_mien_che_do | không mở finding;  |
| reanchored6-results.json | log_group_close_exact_backward | GIET | c47_bien_ghep | không mở finding;  |
| signature6-results.json | n_env_v_truthy_current | GIET | c46_mien_che_do | không mở finding;  |
| signature6-results.json | env_prefix_value_only_current | GIET | c49_oracle_nhieu_truc | không mở finding;  |
| prior1/old1/extra-mutants/results.json | git_ignore_sha | GIET | c34_git_blob_that | không mở finding;  |
| prior1/old1/extra-mutants/results.json | git_always_unavailable | GIET | c34_git_blob_that | không mở finding;  |
| prior1/old2/extra-mutants/results.json | git_ignore_sha | GIET | c34_git_blob_that | không mở finding;  |
| prior1/old2/extra-mutants/results.json | git_always_unavailable | GIET | c34_git_blob_that | không mở finding;  |
| prior2/old1/extra-mutants/results.json | git_ignore_sha | GIET | c34_git_blob_that | không mở finding;  |
| prior2/old1/extra-mutants/results.json | git_always_unavailable | GIET | c34_git_blob_that | không mở finding;  |
| prior2/old2/extra-mutants/results.json | git_ignore_sha | GIET | c34_git_blob_that | không mở finding;  |
| prior2/old2/extra-mutants/results.json | git_always_unavailable | GIET | c34_git_blob_that | không mở finding;  |
