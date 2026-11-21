# Kết quả đo của executor — wp1462 (B4)

Tệp này nằm TRONG H nên KHÔNG ghi SHA của H, cây của H hay numstat của H (xem handoff §7 và Issue #1462). Kết quả neo bằng sha256 của mã đã chạy:

| tệp | sha256 |
|---|---|
| `.claude/dev/packet_loop.py` | `066eeb689a64fab7a06fce8a46fafaeb1e2ecd44deb550f3e9cada759e708d6e` |
| `.claude/dev/packet_loop_test.py` | `bbff0c21a18d4b1498f0a0e129884c6223d75b58e88843b8601c6420abb247e2` |
| `ops/specs/wp1462-r1/do/do_b4.py` | `de8a7ab54d91c160cb326aaf0aa5819376dc7f0b1cd2b5f65cb127f4a7771fbe` |

Nền đo: phiên cloud Linux, 4 nhân, Python 3.13.18, git 2.43.0; base = `48d372e14f190dae83a75ccbca8ee9a0b25635c5` (merge-base với `origin/master`). Mọi lệnh chạy từ gốc kho; log thô nằm ngoài kho (đường dẫn ở handoff). Lượt đo này là attempt 2 (sau review mã Codex lượt 1); mọi số dưới đây đo lại, không chép từ lượt trước.

## Tiêu chí 1–2 — A/B (`python ops/specs/wp1462-r1/do/do_b4.py ab i/4`, i = 0..3 song song, mỗi lát rc 0 `KẾT QUẢ ab: ĐẠT`)

Quần thể ĐẾM bằng máy đếm ở `_c1106`, chạy CẢ sổ ca bắt buộc của base trên nền này (bộ lọc nền của `main()`), không lọc tĩnh; lượt vào bộ dựng và kết cục được ghi TRƯỚC khi runner chạy. Mỗi lát còn chạy hai tự kiểm: bộ so (14 ca) và phép đếm (sổ ca giả: ca tới bộ dựng qua `dict(CASES)`, ngoại lệ lúc dựng, ngoại lệ ở runner, script do ca tự sửa, lời gọi runner không `state_dir`; khôi phục lọc tĩnh hay bỏ kết cục ngoại lệ ⇒ ĐỎ).

| đại lượng (hợp bốn lát) | số |
|---|---|
| ca của sổ base đã chạy có máy đếm | 1581 |
| kết cục ca tại base | `ca:BoQua` 37, `ca:OSError` 1, `ca:dat` 1543 |
| ca VÀO `_c1106` tại base | 157 = 147 ca thường + 10 ca riêng |
| lần vào `_c1106` / lời `kiem-merge` so được byte | 157 / 147 |
| tiêu chí 2, lời theo lớp | (a) 3 · (b) 104 · (c) 36 · (z) 4 |
| lớp (z) | `cong_c_k1_anchor`, `cong_c_k1_khoa_trung`, `cong_c_k1_tag_hong`, `cong_c_k1_yaml_hong` |

Ca thường: mọi lần vào đều cho một lời `kiem-merge` so được, ca đạt; cả hai hình dạng fixture của head so được đúng số lời ấy. Ca riêng: có lần vào không cho lời so được (bộ dựng ném trước CLI, runner chuyển trạng thái ném, hoặc ca chạy script do chính nó sửa); với chúng phép so là VẾT (dãy vào · so · ném · script lạ:rc · kết cục ca) của head phải trùng vết base ở hình dạng mới, và trùng (trừ kết cục ca) ở hình dạng cũ:

- `r1187_overflow_crash_credit`: `vao la:1 ca:dat`
- `r1187_transition_dispatch_AssertionError`: `vao nem:CliSapDo ca:dat`
- `r1187_transition_dispatch_RuntimeError`: `vao nem:CliSapDo ca:dat`
- `r1187_transition_dispatch_TimeoutExpired`: `vao nem:CliSapDo ca:dat`
- `r1187_transition_import_AssertionError`: `vao nem:CliSapDo ca:dat`
- `r1187_transition_import_RuntimeError`: `vao nem:CliSapDo ca:dat`
- `r1187_transition_import_TimeoutExpired`: `vao nem:CliSapDo ca:dat`
- `r1187_transition_setup_AssertionError`: `vao nem:AssertionError ca:dat`
- `r1187_transition_setup_RuntimeError`: `vao nem:RuntimeError ca:dat`
- `r1187_transition_setup_TimeoutExpired`: `vao nem:TimeoutExpired ca:dat`

Tên 157 ca vào `_c1106`: `cong_c_fixture_crlf`, `cong_c_k0_pr_head`, `cong_c_k1_anchor`, `cong_c_k1_git_loi`, `cong_c_k1_hai_dong`, `cong_c_k1_hash`, `cong_c_k1_khoa_trung`, `cong_c_k1_khong_dong`, `cong_c_k1_l2`, `cong_c_k1_mot_dong_sai`, `cong_c_k1_tag_hong`, `cong_c_k1_yaml_hong`, `cong_c_k2_ci_do`, `cong_c_k3_original_tien_to`, `cong_c_k3_p1`, `cong_c_k3_p2_commit_doi`, `cong_c_k3_p2_original_head`, `cong_c_k4_changes`, `cong_c_k4_head`, `cong_c_k4_ma_thoat`, `cong_c_k4_stdout`, `cong_c_k5_offline`, `cong_c_k5_p3_khong_mien`, `cong_c_k5_p3_mien`, `cong_c_k5_phu_dinh`, `cong_c_k5_sai_nguoi`, `cong_c_k5_thua`, `cong_c_k6_dev_thieu`, `cong_c_k6_dev_xanh`, `cong_c_k6_land_py_unknown`, `cong_c_k6_luu_tru`, `cong_c_k6_md_chu_khoa`, `cong_c_k6_mien`, `cong_c_k6_ps1_docs`, `cong_c_k6_rong`, `cong_c_k6_skipped`, `cong_c_k6_symlink`, `cong_c_k6_thieu_id`, `cong_c_k6_tu_khoa_py`, `cong_c_k6_unknown_chot`, `cong_c_m6_hai_thieu`, `cong_c_merge_du`, `cong_m9_attempt_2`, `cong_m9_dev_khong_run`, `cong_m9_dev_mien`, `cong_m9_dev_run_xanh`, `cong_m9_docs_khong_readback`, `cong_m9_hai_run_hai_tep`, `cong_m9_job_attempt_bool`, `cong_m9_job_attempt_float`, `cong_m9_job_attempt_khac`, `cong_m9_job_dang_chay`, `cong_m9_job_dau_dang_chay`, `cong_m9_job_failure`, `cong_m9_job_giua_dang_chay`, `cong_m9_job_giua_float`, `cong_m9_job_rong`, `cong_m9_job_run_id_bool`, `cong_m9_job_run_id_float`, `cong_m9_job_run_khac`, `cong_m9_job_sau_float`, `cong_m9_job_sau_run_id_float`, `cong_m9_job_thieu_run_id`, `cong_m9_jobs_tron_run`, `cong_m9_jobs_trung_tep`, `cong_m9_m6_hai_thieu`, `cong_m9_mien_crlf`, `cong_m9_mien_dau_khoang_trang`, `cong_m9_mien_duoi_tab`, `cong_m9_mien_ky_tu_tach`, `cong_m9_mien_sai_nguoi`, `cong_m9_mien_sha_khac`, `cong_m9_mien_sha_rut_gon`, `cong_m9_nguoi_khac_run_xanh`, `cong_m9_nhom_jobs_dung_run`, `cong_m9_nhom_khac_do_van_dat`, `cong_m9_ops_md_khong`, `cong_m9_pham_vi_ops_py`, `cong_m9_pham_vi_tep_sau`, `cong_m9_pham_vi_workflow`, `cong_m9_ranh_gioi_pham_vi`, `cong_m9_run_attempt_bool`, `cong_m9_run_attempt_float`, `cong_m9_run_dang_chay`, `cong_m9_run_do`, `cong_m9_run_head_khac`, `cong_m9_run_sai_tep`, `cong_m9_run_thieu_attempt_truoc`, `cong_m9_run_xanh_o_giua`, `cong_m9_trang_jobs_thieu`, `cong_m9_trang_thieu`, `k3s_any_findings`, `k3s_badge_ngoai_mien`, `k3s_badge_p1`, `k3s_bot_khac`, `k3s_bot_khac_marker_hong`, `k3s_code_review_nhan_legacy`, `k3s_code_review_sai_kieu`, `k3s_comment_that_sach`, `k3s_completed_null`, `k3s_cu_vs_head`, `k3s_flags_chuoi`, `k3s_flags_so`, `k3s_hai_neo_khop_cu`, `k3s_hai_neo_khop_head`, `k3s_hai_neo_mau_thuan`, `k3s_json_hong`, `k3s_json_sau`, `k3s_legacy_hong`, `k3s_nhieu_marker`, `k3s_running`, `k3s_running_badge_p1`, `k3s_running_co_ket_luan_khac`, `k3s_running_null`, `k3s_running_sai_kieu`, `k3s_running_vs_head`, `k3s_security_bo_qua`, `k3s_security_nhan_legacy`, `k3s_sha_cu`, `k3s_sha_cu_khong_kiem_flags`, `k3s_sha_hoa`, `k3s_sha_khoang_trang`, `k3s_sha_null`, `k3s_sha_tien_to`, `k3s_status_sai_kieu`, `k3s_thieu_code_review`, `k3s_unresolved`, `r1187_cli_bad_human_good_model`, `r1187_cli_both_valid`, `r1187_cli_conflict`, `r1187_cli_datetime_max`, `r1187_cli_datetime_min`, `r1187_cli_human`, `r1187_cli_missing_model_run`, `r1187_cli_missing_model_stdout`, `r1187_cli_missing_remote`, `r1187_cli_missing_transition`, `r1187_cli_neither`, `r1187_cli_p3_block`, `r1187_cli_p3_waive`, `r1187_cli_transition`, `r1187_cli_transition_bad`, `r1187_overflow_crash_credit`, `r1187_transition_dispatch_AssertionError`, `r1187_transition_dispatch_RuntimeError`, `r1187_transition_dispatch_TimeoutExpired`, `r1187_transition_import_AssertionError`, `r1187_transition_import_RuntimeError`, `r1187_transition_import_TimeoutExpired`, `r1187_transition_setup_AssertionError`, `r1187_transition_setup_RuntimeError`, `r1187_transition_setup_TimeoutExpired`, `stdout_cp1252`, `stdout_cp1258`, `wp1254_cli_conversion`, `wp1254_cli_late`, `wp1254_cli_wrong_number`.

## Tiêu chí 8 — phát lại 60 merge (`python ops/specs/wp1462-r1/do/do_b4.py phat-lai`, rc 0)

```
phát lại: 60 merge · bảng sha256 aa932267e766cf3f6e242f35febe3692909f3e909cb510177ba83d780bfc849a · lớp {'khong_giam': 42, 'duong_nhanh': 18} · REST 0 · kho (bản sao riêng) sạch: True
không lệch
KẾT QUẢ phat-lai: ĐẠT
```

Đo trên bản sao bare RIÊNG của kho, với hàm chạy đã cách ly git (GIT_DIR tạm, cấu hình toàn cục tạm, `core.symlinks=false`). Hồi quy khung dòng: 60/60 lượt CRLF mô phỏng (`TextIOWrapper(newline="\r\n")`) ra cùng lớp với LF; đối chứng hỏng (CR giữa giá trị `che_do`) ra `la`.

## Tiêu chí 4 — từng cặp đột biến · ca (`python ops/specs/wp1462-r1/do/do_b4.py dot-bien`, rc 0)

125 đột biến `b4_*`, 171 cặp, 171 GIẾT bằng `ChotB4` của chính ca đích, 0 TÍN DỤNG GIẢ, 0 sống sót, 0 đối chứng khác họ đỏ.

| đột biến | ca đích | lớp ngoại lệ | phân hạng |
|---|---|---|---|
| b4_bc_bo_path | cong_b4_bc_run_path_qua | ChotB4 | GIET |
| b4_bc_bo_path | cong_b4_bc_run_path_chan | ChotB4 | GIET |
| b4_bc_bo_head | cong_b4_bc_run_head_qua | ChotB4 | GIET |
| b4_bc_bo_head | cong_b4_bc_run_head_chan | ChotB4 | GIET |
| b4_bc_bo_kho | cong_b4_bc_run_kho_qua | ChotB4 | GIET |
| b4_bc_bo_kho | cong_b4_bc_run_kho_chan | ChotB4 | GIET |
| b4_bc_run_nho_nhat | cong_b4_bc_run_id_lon_nhat_qua | ChotB4 | GIET |
| b4_bc_run_nho_nhat | cong_b4_bc_run_id_lon_nhat_chan | ChotB4 | GIET |
| b4_bc_bo_run_id | cong_b4_bc_job_run_khac | ChotB4 | GIET |
| b4_bc_bo_attempt | cong_b4_bc_job_attempt_cu | ChotB4 | GIET |
| b4_bc_bay_manh | cong_b4_bc_thieu_manh_7 | ChotB4 | GIET |
| b4_bc_bay_manh | cong_b4_bc_dich_thieu_manh_7 | ChotB4 | GIET |
| b4_bc_nhan_trung | cong_b4_bc_manh_trung | ChotB4 | GIET |
| b4_bc_bo_kieu_list | cong_b4_bc_khong_steps | ChotB4 | GIET |
| b4_bc_bo_kieu_buoc | cong_b4_bc_step_ten_khong_chuoi | ChotB4 | GIET |
| b4_bc_bo_kieu_buoc | cong_b4_bc_step_khong_object | ChotB4 | GIET |
| b4_bc_bo_job_head | cong_b4_bc_job_head_khac | ChotB4 | GIET |
| b4_bc_bo_job_status | cong_b4_bc_job_dang_chay | ChotB4 | GIET |
| b4_bc_bo_job_conclusion | cong_b4_bc_job_failure | ChotB4 | GIET |
| b4_bc_nhieu_buoc | cong_b4_bc_hai_buoc_du | ChotB4 | GIET |
| b4_bc_bo_buoc_status | cong_b4_bc_buoc_dang_chay | ChotB4 | GIET |
| b4_bc_bo_buoc_conclusion | cong_b4_bc_buoc_failure | ChotB4 | GIET |
| b4_bc_bo_buoc_kia | cong_b4_bc_ca_hai_buoc_success | ChotB4 | GIET |
| b4_bc_khong_gop_tep | cong_b4_bc_du_tep_lap | ChotB4 | GIET |
| b4_bc_khong_gop_tep | cong_b4_bc_du_tep_hai_trang | ChotB4 | GIET |
| b4_bc_khong_gop_tep | cong_b4_bc_du_tep_chong | ChotB4 | GIET |
| b4_bc_khong_gop_tep | cong_b4_bc_dich_tep_lap | ChotB4 | GIET |
| b4_bc_khong_gop_tep | cong_b4_bc_dich_tep_hai_trang | ChotB4 | GIET |
| b4_bc_khong_gop_tep | cong_b4_bc_dich_tep_chong | ChotB4 | GIET |
| b4_bc_ten_job_long | cong_b4_bc_ten_job_nen_khac | ChotB4 | GIET |
| b4_bc_luon_du | cong_b4_bc_job_run_khac | ChotB4 | GIET |
| b4_bc_luon_du | cong_b4_siet_alpha | ChotB4 | GIET |
| b4_bc_buoc_kia_moi_ket_luan | cong_b4_bc_buoc_kia_skipped | ChotB4 | GIET |
| b4_chay_khi_k2_do | cong_b4_k2_do_thi_khong_chay | ChotB4 | GIET |
| b4_k2b_truoc_k7 | cong_b4_thu_tu_sau_k7 | ChotB4 | GIET |
| b4_audit_truoc_bang_chung | cong_b4_dich_thieu_ca_hai | ChotB4 | GIET |
| b4_hai_dong_lan_g5 | cong_b4_dc_alpha | ChotB4 | GIET |
| b4_hai_dong_lan_g5 | cong_b4_khong_giam | ChotB4 | GIET |
| b4_du_cung_tu_kiem | cong_b4_7a_du_khong_tu_kiem | ChotB4 | GIET |
| b4_bo_dong_cong_tac | cong_b4_dc_beta | ChotB4 | GIET |
| b4_bo_dong_cong_tac | cong_b4_bien_vang | ChotB4 | GIET |
| b4_bo_co_siet | cong_b4_siet_beta | ChotB4 | GIET |
| b4_bo_co_siet | cong_b4_siet_alpha | ChotB4 | GIET |
| b4_khong_giam_dat | cong_b4_khong_giam | ChotB4 | GIET |
| b4_khong_giam_dat | cong_b4_nam_im_khong_giam | ChotB4 | GIET |
| b4_khong_giam_dat | cong_b4_tc11_d_bo_moi | ChotB4 | GIET |
| b4_khong_giam_dat | cong_b4_tc11_d_che_do_dich | ChotB4 | GIET |
| b4_la_dat | cong_b4_khong_tep_phan_loai | ChotB4 | GIET |
| b4_bo_tinh_lai | cong_b4_khong_giam | ChotB4 | GIET |
| b4_bo_tinh_lai | cong_b4_pr_sua_ci_yml | ChotB4 | GIET |
| b4_ma_cua_pr | cong_b4_pr_sua_bo_phan_loai | ChotB4 | GIET |
| b4_goc_la_base | cong_b4_goc_la_master | ChotB4 | GIET |
| b4_bo_bang_chung_dich | cong_b4_dich_thieu_bang_chung | ChotB4 | GIET |
| b4_bo_audit | cong_b4_dich_khong_audit | ChotB4 | GIET |
| b4_bo_audit | cong_b4_dich_audit_do | ChotB4 | GIET |
| b4_audit_nhan_mien | cong_b4_dich_mien_khong_thay | ChotB4 | GIET |
| b4_gia_tri_la_giam | cong_b4_gia_tri_khac | ChotB4 | GIET |
| b4_gia_tri_la_giam | cong_b4_gia_tri_rong | ChotB4 | GIET |
| b4_gia_tri_la_giam | cong_b4_gia_tri_sai_mot_ky_tu | ChotB4 | GIET |
| b4_vang_giam | cong_b4_bien_vang | ChotB4 | GIET |
| b4_vang_giam | cong_b4_dich_cong_tac_dong | ChotB4 | GIET |
| b4_khong_doc_duoc_giam | cong_b4_rest_nem | ChotB4 | GIET |
| b4_khong_doc_duoc_giam | cong_b4_json_hong | ChotB4 | GIET |
| b4_khong_doc_duoc_giam | cong_b4_json_sau | ChotB4 | GIET |
| b4_khong_doc_duoc_giam | cong_b4_than_la | ChotB4 | GIET |
| b4_khong_doc_duoc_giam | cong_b4_tien_trinh_thuong | ChotB4 | GIET |
| b4_merge_la_dau | cong_b4_master_di_truoc | ChotB4 | GIET |
| b4_bo_rc_merge | cong_b4_merge_xung_dot | ChotB4 | GIET |
| b4_bo_rc_git_dir | cong_b4_git_loi | ChotB4 | GIET |
| b4_moi_truong_ke_thua | cong_b4_moi_truong_moi | ChotB4 | GIET |
| b4_moi_truong_ke_thua | cong_b4_tc11_c_bo_moi | ChotB4 | GIET |
| b4_moi_truong_ke_thua | cong_b4_tc11_c_che_do_dich | ChotB4 | GIET |
| b4_bo_I | cong_b4_python_I | ChotB4 | GIET |
| b4_bo_han_phan_loai | cong_b4_het_han | ChotB4 | GIET |
| b4_su_kien_khac | cong_b4_sinh_bo_moi | ChotB4 | GIET |
| b4_hop_mot_cha | cong_b4_sinh_bo_moi | ChotB4 | GIET |
| b4_hop_mot_cha | cong_b4_tc11_b_che_do_dich | ChotB4 | GIET |
| b4_khong_don | cong_b4_dc_alpha | ChotB4 | GIET |
| b4_khong_don | cong_b4_khong_tep_phan_loai | ChotB4 | GIET |
| b4_khong_don | cong_b4_het_han | ChotB4 | GIET |
| b4_khong_don | cong_b4_system_exit | ChotB4 | GIET |
| b4_object_vao_kho | cong_b4_dc_alpha | ChotB4 | GIET |
| b4_object_vao_kho | cong_b4_master_di_truoc | ChotB4 | GIET |
| b4_git_dir_cua_kho | cong_b4_git_smudge_cuc_bo | ChotB4 | GIET |
| b4_git_dir_cua_kho | cong_b4_git_thay_the | ChotB4 | GIET |
| b4_doc_cau_hinh_toan_cuc | cong_b4_git_smudge_toan_cuc | ChotB4 | GIET |
| b4_doc_cau_hinh_toan_cuc | cong_b4_git_cau_hinh_la_van_nhanh | ChotB4 | GIET |
| b4_lien_trong_cay_tam | cong_b4_lien_tep | ChotB4 | GIET |
| b4_lien_trong_cay_tam | cong_b4_lien_thu_muc | ChotB4 | GIET |
| b4_ngay_theo_dong_ho | cong_b4_ngay_co_dinh | ChotB4 | GIET |
| b4_goc_la_dau | cong_b4_sinh_bo_moi | ChotB4 | GIET |
| b4_hop_dao_cha | cong_b4_sinh_bo_moi | ChotB4 | GIET |
| b4_cay_hop_la_dau | cong_b4_master_di_truoc | ChotB4 | GIET |
| b4_ma_tu_cay_hop | cong_b4_pr_sua_bo_phan_loai | ChotB4 | GIET |
| b4_khoa_khop_giua_dong | cong_b4_dong_khac_bo_qua | ChotB4 | GIET |
| b4_dao_hai_lop | cong_b4_dc_beta | ChotB4 | GIET |
| b4_dao_hai_lop | cong_b4_dc_delta | ChotB4 | GIET |
| b4_dau_la_goc | cong_b4_sinh_bo_moi | ChotB4 | GIET |
| b4_bo_cr | cong_b4_crlf_nhan | ChotB4 | GIET |
| b4_cat_moi_cr | cong_b4_hai_cr | ChotB4 | GIET |
| b4_tach_moi_kieu_dong | cong_b4_cr_giua_dong | ChotB4 | GIET |
| b4_cat_khoang_trang | cong_b4_dau_cach_cuoi | ChotB4 | GIET |
| b4_bo_utf8 | cong_b4_khong_utf8 | ChotB4 | GIET |
| b4_bo_rc_phan_loai | cong_b4_rc_khac_0 | ChotB4 | GIET |
| b4_bo_thieu_che_do | cong_b4_thieu_che_do | ChotB4 | GIET |
| b4_bo_dk_bo_moi_hong | cong_b4_dk_ngoai_tap | ChotB4 | GIET |
| b4_bo_dk_dich_hong | cong_b4_dk_dich_ngoai_tap | ChotB4 | GIET |
| b4_nhan_khoa_lap | cong_b4_che_do_lap | ChotB4 | GIET |
| b4_nhan_khoa_lap | cong_b4_dk_lap | ChotB4 | GIET |
| b4_nhan_ngoai_tap | cong_b4_che_do_ngoai_tap | ChotB4 | GIET |
| b4_nhan_ngoai_tap | cong_b4_dk_ngoai_tap | ChotB4 | GIET |
| b4_nhanh_kem_dk_dat | cong_b4_nhanh_kem_dk | ChotB4 | GIET |
| b4_ca_hai_dk_dat | cong_b4_ca_hai_dk | ChotB4 | GIET |
| b4_so_khop_long | cong_b4_gia_tri_hoa_thuong | ChotB4 | GIET |
| b4_so_khop_long | cong_b4_gia_tri_thua_khoang_trang | ChotB4 | GIET |
| b4_so_khop_long | cong_b4_gia_tri_xuong_dong_dau | ChotB4 | GIET |
| b4_chuoi_cho_phep_lop_kia | cong_b4_dc_beta | ChotB4 | GIET |
| b4_updated_at_la_vi_tu | cong_b4_updated_at_cu | ChotB4 | GIET |
| b4_nhan_hang_ngoai_json | cong_b4_hang_ngoai_json | ChotB4 | GIET |
| b4_bien_lop_khac | cong_b4_bien_lop_khac | ChotB4 | GIET |
| b4_chuoi_lop_khac | cong_b4_bien_lop_khac_gia_tri | ChotB4 | GIET |
| b4_404_moi_nguon | cong_b4_404_thieu_header | ChotB4 | GIET |
| b4_ma_khac_200 | cong_b4_403_tu_choi | ChotB4 | GIET |
| b4_ma_khac_200 | cong_b4_302 | ChotB4 | GIET |
| b4_200_khong_header | cong_b4_200_thieu_header | ChotB4 | GIET |
| b4_header_phan_biet_hoa_thuong | cong_b4_header_hoa_thuong | ChotB4 | GIET |
| b4_bo_tran_than | cong_b4_than_qua_dai | ChotB4 | GIET |
| b4_tran_than_chat_hon | cong_b4_than_dung_tran | ChotB4 | GIET |
| b4_json_tu_byte | cong_b4_utf16 | ChotB4 | GIET |
| b4_utf8_thay_the | cong_b4_utf8_hong | ChotB4 | GIET |
| b4_nhan_khoa_trung | cong_b4_khoa_trung | ChotB4 | GIET |
| b4_bo_goc_object | cong_b4_goc_khong_object | ChotB4 | GIET |
| b4_bo_name | cong_b4_name_khac | ChotB4 | GIET |
| b4_bo_kieu_value | cong_b4_value_khong_chuoi | ChotB4 | GIET |
| b4_rest_loi_lay_bien_nguoi_goi | cong_b4_rest_nem_bien_nguoi_goi | ChotB4 | GIET |
| b4_bo_hang_kho | cong_b4_repo_khac | ChotB4 | GIET |
| b4_bo_bien_cam | cong_b4_bien_cam_doc | ChotB4 | GIET |
| b4_bien_cam_chi_1 | cong_b4_bien_cam_khac_1 | ChotB4 | GIET |
| b4_bien_cam_ca_khi_rong | cong_b4_bien_cam_rong | ChotB4 | GIET |
| b4_token_luon_gui | cong_b4_dc_beta | ChotB4 | GIET |
| b4_token_khong_gui | cong_b4_token | ChotB4 | GIET |
| b4_bo_header_accept | cong_b4_dc_beta | ChotB4 | GIET |
| b4_bo_header_user_agent | cong_b4_dc_beta | ChotB4 | GIET |
| b4_gia_tri_khong_json | cong_b4_gia_tri_xuong_dong_dau | ChotB4 | GIET |
| b4_bo_header_phien_ban | cong_b4_dc_beta | ChotB4 | GIET |
| b4_gia_tri_khong_cat | cong_b4_gia_tri_dai | ChotB4 | GIET |
| b4_hieu_luc_60_phut | cong_b4_dc_beta | ChotB4 | GIET |
| b4_hai_yeu_cau | cong_b4_tc6_bon_tien_trinh | ChotB4 | GIET |
| b4_7a_master_cuc_bo | cong_b4_7a_master_cuc_bo_khac | ChotB4 | GIET |
| b4_7a_bo_so | cong_b4_7a_master_cu | ChotB4 | GIET |
| b4_7a_bo_rc_ls_remote | cong_b4_7a_ls_remote_loi | ChotB4 | GIET |
| b4_7a_bo_rc_rev_parse | cong_b4_7a_rev_parse_loi | ChotB4 | GIET |
| b4_7b_bo_so | cong_b4_7b_blob_khac | ChotB4 | GIET |
| b4_7b_so_tien_to | cong_b4_7b_oid_cung_tien_to | ChotB4 | GIET |
| b4_7b_bo_rc_hash_object | cong_b4_7b_hash_object_loi | ChotB4 | GIET |
| b4_7b_bo_rc_rev_parse | cong_b4_7b_rev_parse_loi | ChotB4 | GIET |
| b4_7b_bo_oid | cong_b4_7b_khong_phai_oid | ChotB4 | GIET |
| b4_7b_bo_tep_vang | cong_b4_7b_khong_tep | ChotB4 | GIET |
| b4_vc_post | cong_b4_vc_get_header | ChotB4 | GIET |
| b4_vc_theo_chuyen_huong | cong_b4_vc_khong_chuyen_huong | ChotB4 | GIET |
| b4_vc_bo_proxy | cong_b4_vc_proxy | ChotB4 | GIET |
| b4_vc_bo_han_socket | cong_b4_vc_han_socket | ChotB4 | GIET |
| b4_vc_bo_tran_byte | cong_b4_vc_tran_byte | ChotB4 | GIET |
| b4_vc_bo_han_tuong | cong_b4_vc_han_tuong | ChotB4 | GIET |
| b4_vc_bo_han_tuong | cong_b4_vc_eof_tre | ChotB4 | GIET |
| b4_vc_bo_han_tuong | cong_b4_vc_khuc_cuoi_tre | ChotB4 | GIET |
| b4_vc_nuot_loi | cong_b4_vc_loi_ket_noi | ChotB4 | GIET |
| b4_vc_thu_lai | cong_b4_vc_500_khong_thu_lai | ChotB4 | GIET |
| b4_vc_ma_200 | cong_b4_vc_404_nguyen_ma | ChotB4 | GIET |
| b4_vc_ma_200 | cong_b4_vc_khong_chuyen_huong | ChotB4 | GIET |
| b4_vc_bo_header | cong_b4_vc_get_header | ChotB4 | GIET |

## Cổng kho — `packet_loop_test` (4 mảnh `packet_loop_test_manh.py --manh i/4`, mọi mảnh rc 0, `TỔNG: ĐẠT`)

| vế | ca đã chạy | đạt/đạt-được | BỎ QUA | tổng giây 4 mảnh | giây tường |
|---|---|---|---|---|---|
| base (đo ở attempt 1, cùng base) | 1579 | 1541/1541 | 38 | 3306 | 1469 |
| head (cùng hai băm trên) | 1743 | 1705/1705 | 38 | 3690 | 1484 |

N sau = N trước + số ca mới: 1743 = 1579 + 164. Delta thời gian là `khong_do_duoc`: hai vế đo ở hai lượt khác nhau, máy có tiến trình khác chạy cùng lúc.

## Chưa đo (`khong_do_duoc` ở lượt này)

- CI PR Ubuntu, `gate-packet-loop-manh` 16 mảnh, `ci-dot-bien-du.yml` trên H: executor không đẩy, không dispatch.
- Windows thật: khung CRLF mới chỉ mô phỏng trên Linux; các ca `cong_b4_*` chưa chạy trên Windows.
- Cấu hình git HỆ THỐNG không được cách ly ở hàm chạy: nó không phải đầu vào của người gọi (B-4), và không ca nào trong bộ dựng được nó mà không cần quyền root, nên một chốt cho nó sẽ không có đột biến giết được.
- Bảng `MUTANTS` cũ (ngoài `b4_*`): chạy ở `packet-loop-dot-bien.yml` sau merge.
