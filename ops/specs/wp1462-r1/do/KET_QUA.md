# Kết quả đo của executor — wp1462 (B4), attempt 3

Tệp này nằm TRONG H nên KHÔNG ghi SHA của H, cây của H hay numstat của H (handoff §7 và Issue #1462 giữ các số ấy). Kết quả neo bằng sha256 của mã đã chạy:

| tệp | sha256 |
|---|---|
| `.claude/dev/packet_loop.py` | `816f77d10413bbaa744795c09a7e2a1f14b03d927cd0642737a353396cec934b` |
| `.claude/dev/packet_loop_test.py` | `43e32fd96687218aed7b80dd9f96ead8fda88ea2e17544cedfe7f6e8c462ca0c` |
| `ops/specs/wp1462-r1/do/do_b4.py` | `277be0adec490c635b74faa3929d6325839ada44b003bf2fd623f433e6ce9951` |

Nền đo: phiên cloud Linux, 4 nhân, Python 3.13.18, git 2.43.0, clone SẠCH (`.git` là thư mục, object dùng chung qua alternates), base `48d372e14f190dae83a75ccbca8ee9a0b25635c5` (merge-base với `origin/master`). Mọi số dưới đây đo lại ở attempt 3 (sau review mã Codex lượt 2); log thô ngoài kho, đường dẫn ở handoff.

## Tiêu chí 1–2 — A/B (`python ops/specs/wp1462-r1/do/do_b4.py ab i/4`, i = 0..3)

**Kết quả: KHÔNG ĐẠT — khoảng trống nghiệm thu, không phải hồi quy của mã sản phẩm.** Bốn lát rc 1 (`KẾT QUẢ ab: 2 · 2 · 5 · 2 lỗi`). Quần thể đếm bằng máy đếm ở `_c1106` trên CẢ sổ ca bắt buộc của base (1 581 ca: `ca:dat` 1 543, `ca:BoQua` 37, `ca:OSError` 1 = `luong_canonical_chay_that` tại base), không lọc tĩnh. Mỗi lát còn chạy hai tự kiểm (bộ so 14 ca; phép đếm trên sổ ca giả, nay gồm: script tự sửa phải được dựng lại trên TỪNG vế và một byte thừa ở vế head phải làm phép so ĐỎ; ca không tới CLI phải nằm trong danh sách khoảng trống — gỡ một trong bốn chốt ấy làm tự kiểm ĐỎ, đã thử).

| đại lượng (hợp bốn lát) | số |
|---|---|
| ca VÀO `_c1106` tại base (quần thể ĐẾM) | 157 (38 · 39 · 43 · 37) |
| có lời `kiem-merge` so được BYTE | 148 = 147 ca thường + `r1187_overflow_crash_credit` (script do ca tự sửa, nay dựng lại phép sửa trên script của từng vế, chạy cùng một chỗ) |
| 147 ca thường, hai hình dạng fixture | trùng byte rc/stdout/stderr ở hình dạng mới; hình dạng cũ: (a) 3 · (b) 104 · (c) 36 · (z) 4, mọi lời đúng khuôn |
| `r1187_overflow_crash_credit` | rc 1/1, LỆCH BYTE: stderr là traceback và CHỈ khác số dòng khung (`packet_loop.py` của head dài hơn); tiêu chí 1 và lớp (z) của tiêu chí 2 cùng ĐỎ |
| vào bộ dựng mà KHÔNG tới CLI nào | 9 — KHOẢNG TRỐNG, quần thể so 148 < đếm 157 ⇒ ĐỎ |
| lớp (z) | `cong_c_k1_anchor`, `cong_c_k1_khoa_trung`, `cong_c_k1_tag_hong`, `cong_c_k1_yaml_hong` (+ ca tự sửa ở trên) |

Chín ca không tới CLI, vết tại base = vết tại head ở cả hai hình dạng; chuỗi ngoại lệ kết thúc ở lỗi do CHÍNH giàn tiêm (`'injected'`) trước khi `main` của sản phẩm chạy: ba ca `setup` (bộ dựng ném lúc dựng fixture git, chưa có fixture), ba ca `import` (nạp module ném trước `main`), ba ca `dispatch` (`main` bị thay bằng lỗi):

- `r1187_transition_setup_{AssertionError,RuntimeError,TimeoutExpired}`: `vao nem:<lớp>('injected') ca:dat`
- `r1187_transition_import_{AssertionError,RuntimeError,TimeoutExpired}` và `r1187_transition_dispatch_{…}`: `vao nem:CliSapDo<<lớp>('injected') ca:dat`

Tiêu chí 1 đòi số ca được so không nhỏ hơn số ca đếm tại base. Chín ca trên không có đầu ra CLI nào ở CẢ base lẫn head, nên không thể so byte mà không đổi ca; ca tự sửa không thể trùng byte vì traceback mang số dòng. Đóng được hai khoảng trống này cần một quyết định đặc tả (tiêu chí 1 xử lý ca không tới CLI và đầu ra traceback thế nào); executor không tự nới tiêu chí.


## Tiêu chí 8 — phát lại 60 merge (`python ops/specs/wp1462-r1/do/do_b4.py phat-lai`, rc 0)

```
phát lại: 60 merge · bảng sha256 aa932267e766cf3f6e242f35febe3692909f3e909cb510177ba83d780bfc849a · lớp {'khong_giam': 42, 'duong_nhanh': 18} · REST 0 · kho (bản sao riêng) sạch: True
KẾT QUẢ phat-lai: ĐẠT
```

Hàm chạy nay dựng cây tạm bằng `_b4_anh_chup` (byte đọc thô qua `cat-file --batch`, băm lại khớp OID, tự ghi; không checkout): 60/60 lượt khớp đường trực tiếp trên cây thật của `0f9aa2a` (17 529 blob). Hồi quy khung dòng: 60/60 lượt CRLF mô phỏng ra cùng lớp với LF; đối chứng hỏng (CR giữa giá trị) ra `la`.

## Tiêu chí 4 — từng cặp đột biến · ca (`python ops/specs/wp1462-r1/do/do_b4.py dot-bien i/4`, i = 0..3, mỗi lát rc 0)

143 đột biến, 197 cặp, 197 GIET bằng ChotB4; 0 TÍN DỤNG GIẢ, 0 sống sót, 0 đối chứng khác họ đỏ. Mỗi hàng là một đột biến; mọi ca đích của hàng đỏ bằng `ChotB4` của chính ca ấy (GIẾT), trừ khi hàng ghi khác.

| đột biến | ca đích (mỗi ca: lớp ngoại lệ · phân hạng) |
|---|---|
| b4_bc_bo_path | cong_b4_bc_run_path_qua · cong_b4_bc_run_path_chan — ChotB4 · GIET |
| b4_bc_bo_run_id | cong_b4_bc_job_run_khac — ChotB4 · GIET |
| b4_bc_bo_manh_1 | cong_b4_bc_du_thieu_manh_1 · cong_b4_bc_dich_thieu_manh_1 — ChotB4 · GIET |
| b4_bc_bo_manh_5 | cong_b4_bc_du_thieu_manh_5 · cong_b4_bc_dich_thieu_manh_5 — ChotB4 · GIET |
| b4_bc_bo_kieu_buoc | cong_b4_bc_step_ten_khong_chuoi · cong_b4_bc_step_khong_object — ChotB4 · GIET |
| b4_bc_nhieu_buoc | cong_b4_bc_hai_buoc_du — ChotB4 · GIET |
| b4_bc_khong_gop_tep | cong_b4_bc_du_tep_lap · cong_b4_bc_du_tep_hai_trang · cong_b4_bc_du_tep_chong · cong_b4_bc_dich_tep_lap · cong_b4_bc_dich_tep_hai_trang · cong_b4_bc_dich_tep_chong — ChotB4 · GIET |
| b4_chay_khi_k2_do | cong_b4_k2_do_thi_khong_chay — ChotB4 · GIET |
| b4_du_cung_tu_kiem | cong_b4_7a_du_khong_tu_kiem — ChotB4 · GIET |
| b4_la_dat | cong_b4_khong_tep_phan_loai — ChotB4 · GIET |
| b4_bo_bang_chung_dich | cong_b4_dich_thieu_bang_chung — ChotB4 · GIET |
| b4_vang_giam | cong_b4_bien_vang · cong_b4_dich_cong_tac_dong — ChotB4 · GIET |
| b4_bo_rc_git_dir | cong_b4_git_loi — ChotB4 · GIET |
| b4_su_kien_khac | cong_b4_sinh_bo_moi — ChotB4 · GIET |
| b4_git_dir_cua_kho | cong_b4_git_doi_ten_cuc_bo · cong_b4_git_thay_the — ChotB4 · GIET |
| b4_doc_thuoc_tinh_he_thong | cong_b4_git_khong_he_thong — ChotB4 · GIET |
| b4_bo_bam_cay | cong_b4_gia_mao_cay — ChotB4 · GIET |
| b4_han_khac_15 | cong_b4_dc_beta — ChotB4 · GIET |
| b4_hop_dao_cha | cong_b4_sinh_bo_moi — ChotB4 · GIET |
| b4_dao_hai_lop | cong_b4_dc_beta · cong_b4_dc_delta — ChotB4 · GIET |
| b4_tach_moi_kieu_dong | cong_b4_cr_giua_dong — ChotB4 · GIET |
| b4_bo_thieu_che_do | cong_b4_thieu_che_do — ChotB4 · GIET |
| b4_nhan_ngoai_tap | cong_b4_che_do_ngoai_tap · cong_b4_dk_ngoai_tap — ChotB4 · GIET |
| b4_chuoi_cho_phep_lop_kia | cong_b4_dc_beta — ChotB4 · GIET |
| b4_chuoi_lop_khac | cong_b4_bien_lop_khac_gia_tri — ChotB4 · GIET |
| b4_header_phan_biet_hoa_thuong | cong_b4_header_hoa_thuong — ChotB4 · GIET |
| b4_utf8_thay_the | cong_b4_utf8_hong — ChotB4 · GIET |
| b4_bo_kieu_value | cong_b4_value_khong_chuoi — ChotB4 · GIET |
| b4_bien_cam_chi_1 | cong_b4_bien_cam_khac_1 — ChotB4 · GIET |
| b4_bo_header_accept | cong_b4_dc_beta — ChotB4 · GIET |
| b4_gia_tri_khong_cat | cong_b4_gia_tri_dai — ChotB4 · GIET |
| b4_7a_bo_so | cong_b4_7a_master_cu — ChotB4 · GIET |
| b4_7b_so_tien_to | cong_b4_7b_oid_cung_tien_to — ChotB4 · GIET |
| b4_7b_bo_tep_vang | cong_b4_7b_khong_tep — ChotB4 · GIET |
| b4_vc_bo_han_socket | cong_b4_vc_han_socket — ChotB4 · GIET |
| b4_vc_thu_lai | cong_b4_vc_500_khong_thu_lai — ChotB4 · GIET |
| b4_bc_bo_head | cong_b4_bc_run_head_qua · cong_b4_bc_run_head_chan — ChotB4 · GIET |
| b4_bc_bo_attempt | cong_b4_bc_job_attempt_cu — ChotB4 · GIET |
| b4_bc_bo_manh_2 | cong_b4_bc_du_thieu_manh_2 · cong_b4_bc_dich_thieu_manh_2 — ChotB4 · GIET |
| b4_bc_bo_manh_6 | cong_b4_bc_du_thieu_manh_6 · cong_b4_bc_dich_thieu_manh_6 — ChotB4 · GIET |
| b4_bc_bo_job_head | cong_b4_bc_job_head_khac — ChotB4 · GIET |
| b4_bc_bo_buoc_status | cong_b4_bc_buoc_dang_chay — ChotB4 · GIET |
| b4_bc_ten_job_long | cong_b4_bc_ten_job_nen_khac — ChotB4 · GIET |
| b4_k2b_truoc_k7 | cong_b4_thu_tu_sau_k7 — ChotB4 · GIET |
| b4_bo_dong_cong_tac | cong_b4_dc_beta · cong_b4_bien_vang — ChotB4 · GIET |
| b4_bo_tinh_lai | cong_b4_khong_giam · cong_b4_pr_sua_ci_yml — ChotB4 · GIET |
| b4_bo_audit | cong_b4_dich_khong_audit · cong_b4_dich_audit_do — ChotB4 · GIET |
| b4_khong_doc_duoc_giam | cong_b4_rest_nem · cong_b4_json_hong · cong_b4_json_sau · cong_b4_than_la · cong_b4_tien_trinh_thuong — ChotB4 · GIET |
| b4_moi_truong_ke_thua | cong_b4_moi_truong_moi · cong_b4_tc11_c_bo_moi · cong_b4_tc11_c_che_do_dich — ChotB4 · GIET |
| b4_hop_mot_cha | cong_b4_sinh_bo_moi · cong_b4_tc11_b_che_do_dich — ChotB4 · GIET |
| b4_doc_cau_hinh_toan_cuc | cong_b4_git_doi_ten_toan_cuc — ChotB4 · GIET |
| b4_checkout_thay_anh_chup | cong_b4_gia_mao_blob · cong_b4_git_thuoc_tinh_trong_cay — ChotB4 · GIET |
| b4_object_vang_bo_qua | cong_b4_object_vang — ChotB4 · GIET |
| b4_han_pl_khac_120 | cong_b4_han_dac_ta — ChotB4 · GIET |
| b4_cay_hop_la_dau | cong_b4_master_di_truoc — ChotB4 · GIET |
| b4_dau_la_goc | cong_b4_sinh_bo_moi — ChotB4 · GIET |
| b4_cat_khoang_trang | cong_b4_dau_cach_cuoi — ChotB4 · GIET |
| b4_bo_dk_bo_moi_hong | cong_b4_dk_ngoai_tap — ChotB4 · GIET |
| b4_nhanh_kem_dk_dat | cong_b4_nhanh_kem_dk — ChotB4 · GIET |
| b4_updated_at_la_vi_tu | cong_b4_updated_at_cu — ChotB4 · GIET |
| b4_404_moi_nguon | cong_b4_404_thieu_header — ChotB4 · GIET |
| b4_bo_tran_than | cong_b4_than_qua_dai — ChotB4 · GIET |
| b4_nhan_khoa_trung | cong_b4_khoa_trung — ChotB4 · GIET |
| b4_rest_loi_lay_bien_nguoi_goi | cong_b4_rest_nem_bien_nguoi_goi — ChotB4 · GIET |
| b4_bien_cam_ca_khi_rong | cong_b4_bien_cam_rong — ChotB4 · GIET |
| b4_bo_header_user_agent | cong_b4_dc_beta — ChotB4 · GIET |
| b4_hieu_luc_60_phut | cong_b4_dc_beta — ChotB4 · GIET |
| b4_7a_bo_rc_ls_remote | cong_b4_7a_ls_remote_loi — ChotB4 · GIET |
| b4_7b_bo_rc_hash_object | cong_b4_7b_hash_object_loi — ChotB4 · GIET |
| b4_vc_post | cong_b4_vc_get_header — ChotB4 · GIET |
| b4_vc_bo_tran_byte | cong_b4_vc_tran_byte — ChotB4 · GIET |
| b4_vc_ma_200 | cong_b4_vc_404_nguyen_ma · cong_b4_vc_khong_chuyen_huong — ChotB4 · GIET |
| b4_bc_bo_kho | cong_b4_bc_run_kho_qua · cong_b4_bc_run_kho_chan — ChotB4 · GIET |
| b4_bc_bay_manh | cong_b4_bc_thieu_manh_7 · cong_b4_bc_dich_thieu_manh_7 — ChotB4 · GIET |
| b4_bc_bo_manh_3 | cong_b4_bc_du_thieu_manh_3 · cong_b4_bc_dich_thieu_manh_3 — ChotB4 · GIET |
| b4_bc_nhan_trung | cong_b4_bc_manh_trung — ChotB4 · GIET |
| b4_bc_bo_job_status | cong_b4_bc_job_dang_chay — ChotB4 · GIET |
| b4_bc_bo_buoc_conclusion | cong_b4_bc_buoc_failure — ChotB4 · GIET |
| b4_bc_luon_du | cong_b4_bc_job_run_khac · cong_b4_siet_alpha — ChotB4 · GIET |
| b4_audit_truoc_bang_chung | cong_b4_dich_thieu_ca_hai — ChotB4 · GIET |
| b4_bo_co_siet | cong_b4_siet_beta · cong_b4_siet_alpha — ChotB4 · GIET |
| b4_ma_cua_pr | cong_b4_pr_sua_bo_phan_loai — ChotB4 · GIET |
| b4_audit_nhan_mien | cong_b4_dich_mien_khong_thay — ChotB4 · GIET |
| b4_merge_la_dau | cong_b4_master_di_truoc — ChotB4 · GIET |
| b4_bo_I | cong_b4_python_I — ChotB4 · GIET |
| b4_khong_don | cong_b4_dc_alpha · cong_b4_khong_tep_phan_loai · cong_b4_het_han · cong_b4_system_exit — ChotB4 · GIET |
| b4_doc_thuoc_tinh_toan_cuc | cong_b4_git_thuoc_tinh_hop — ChotB4 · GIET |
| b4_bo_kiem_bam | cong_b4_gia_mao_blob · cong_b4_gia_mao_cay — ChotB4 · GIET |
| b4_ghi_ra_ngoai | cong_b4_cay_ra_ngoai — ChotB4 · GIET |
| b4_ngay_theo_dong_ho | cong_b4_ngay_co_dinh — ChotB4 · GIET |
| b4_ma_tu_cay_hop | cong_b4_pr_sua_bo_phan_loai — ChotB4 · GIET |
| b4_bo_cr | cong_b4_crlf_nhan — ChotB4 · GIET |
| b4_bo_utf8 | cong_b4_khong_utf8 — ChotB4 · GIET |
| b4_bo_dk_dich_hong | cong_b4_dk_dich_ngoai_tap — ChotB4 · GIET |
| b4_ca_hai_dk_dat | cong_b4_ca_hai_dk — ChotB4 · GIET |
| b4_nhan_hang_ngoai_json | cong_b4_hang_ngoai_json — ChotB4 · GIET |
| b4_ma_khac_200 | cong_b4_403_tu_choi · cong_b4_302 — ChotB4 · GIET |
| b4_tran_than_chat_hon | cong_b4_than_dung_tran — ChotB4 · GIET |
| b4_bo_goc_object | cong_b4_goc_khong_object — ChotB4 · GIET |
| b4_bo_hang_kho | cong_b4_repo_khac — ChotB4 · GIET |
| b4_token_luon_gui | cong_b4_dc_beta — ChotB4 · GIET |
| b4_gia_tri_khong_json | cong_b4_gia_tri_xuong_dong_dau — ChotB4 · GIET |
| b4_hai_yeu_cau | cong_b4_tc6_bon_tien_trinh — ChotB4 · GIET |
| b4_7a_bo_rc_rev_parse | cong_b4_7a_rev_parse_loi — ChotB4 · GIET |
| b4_7b_bo_rc_rev_parse | cong_b4_7b_rev_parse_loi — ChotB4 · GIET |
| b4_vc_theo_chuyen_huong | cong_b4_vc_khong_chuyen_huong — ChotB4 · GIET |
| b4_vc_bo_han_tuong | cong_b4_vc_han_tuong · cong_b4_vc_eof_tre · cong_b4_vc_khuc_cuoi_tre — ChotB4 · GIET |
| b4_vc_bo_header | cong_b4_vc_get_header — ChotB4 · GIET |
| b4_bc_run_nho_nhat | cong_b4_bc_run_id_lon_nhat_qua · cong_b4_bc_run_id_lon_nhat_chan — ChotB4 · GIET |
| b4_bc_bo_manh_dau | cong_b4_bc_du_thieu_manh_0 · cong_b4_bc_dich_thieu_manh_0 — ChotB4 · GIET |
| b4_bc_bo_manh_4 | cong_b4_bc_du_thieu_manh_4 · cong_b4_bc_dich_thieu_manh_4 — ChotB4 · GIET |
| b4_bc_bo_kieu_list | cong_b4_bc_khong_steps — ChotB4 · GIET |
| b4_bc_bo_job_conclusion | cong_b4_bc_job_failure — ChotB4 · GIET |
| b4_bc_bo_buoc_kia | cong_b4_bc_ca_hai_buoc_success — ChotB4 · GIET |
| b4_bc_buoc_kia_moi_ket_luan | cong_b4_bc_buoc_kia_skipped — ChotB4 · GIET |
| b4_hai_dong_lan_g5 | cong_b4_dc_alpha · cong_b4_khong_giam — ChotB4 · GIET |
| b4_khong_giam_dat | cong_b4_khong_giam · cong_b4_nam_im_khong_giam · cong_b4_tc11_d_bo_moi · cong_b4_tc11_d_che_do_dich — ChotB4 · GIET |
| b4_goc_la_base | cong_b4_goc_la_master — ChotB4 · GIET |
| b4_gia_tri_la_giam | cong_b4_gia_tri_khac · cong_b4_gia_tri_rong · cong_b4_gia_tri_sai_mot_ky_tu — ChotB4 · GIET |
| b4_bo_rc_merge | cong_b4_merge_xung_dot — ChotB4 · GIET |
| b4_bo_han_phan_loai | cong_b4_het_han — ChotB4 · GIET |
| b4_object_vao_kho | cong_b4_dc_alpha · cong_b4_master_di_truoc — ChotB4 · GIET |
| b4_doc_cau_hinh_he_thong | cong_b4_git_khong_he_thong — ChotB4 · GIET |
| b4_bo_bam_blob | cong_b4_gia_mao_blob — ChotB4 · GIET |
| b4_ghi_lien_that | cong_b4_lien_tep · cong_b4_lien_thu_muc — ChotB4 · GIET |
| b4_goc_la_dau | cong_b4_sinh_bo_moi — ChotB4 · GIET |
| b4_khoa_khop_giua_dong | cong_b4_dong_khac_bo_qua — ChotB4 · GIET |
| b4_cat_moi_cr | cong_b4_hai_cr — ChotB4 · GIET |
| b4_bo_rc_phan_loai | cong_b4_rc_khac_0 — ChotB4 · GIET |
| b4_nhan_khoa_lap | cong_b4_che_do_lap · cong_b4_dk_lap — ChotB4 · GIET |
| b4_so_khop_long | cong_b4_gia_tri_hoa_thuong · cong_b4_gia_tri_thua_khoang_trang · cong_b4_gia_tri_xuong_dong_dau — ChotB4 · GIET |
| b4_bien_lop_khac | cong_b4_bien_lop_khac — ChotB4 · GIET |
| b4_200_khong_header | cong_b4_200_thieu_header — ChotB4 · GIET |
| b4_json_tu_byte | cong_b4_utf16 — ChotB4 · GIET |
| b4_bo_name | cong_b4_name_khac — ChotB4 · GIET |
| b4_bo_bien_cam | cong_b4_bien_cam_doc — ChotB4 · GIET |
| b4_token_khong_gui | cong_b4_token — ChotB4 · GIET |
| b4_bo_header_phien_ban | cong_b4_dc_beta — ChotB4 · GIET |
| b4_7a_master_cuc_bo | cong_b4_7a_master_cuc_bo_khac — ChotB4 · GIET |
| b4_7b_bo_so | cong_b4_7b_blob_khac — ChotB4 · GIET |
| b4_7b_bo_oid | cong_b4_7b_khong_phai_oid — ChotB4 · GIET |
| b4_vc_bo_proxy | cong_b4_vc_proxy — ChotB4 · GIET |
| b4_vc_nuot_loi | cong_b4_vc_loi_ket_noi — ChotB4 · GIET |

## Cổng kho và delta thời gian

`packet_loop_test` 4 mảnh, Ruff F, `doctrine-scan`, `adr-song`, tl selftest chạy trên ĐÚNG H nên số đo nằm ở handoff, không ở tệp này. Delta thời gian của `gate-packet-loop-manh` (16 mảnh, CI) là `khong_do_duoc`: executor không đẩy, không dispatch.

## Biên đã soát (B4-S05, đặc tả mục 2–9)

Mỗi biên có ca hai chiều và đột biến riêng ở bảng trên: chỉ số mảnh 0..7 ở cả `du` lẫn `dich` (`b4_bc_bo_manh_dau`, `_1`…`_6`, `b4_bc_bay_manh`) · run `id` lớn nhất · `len(jj) == 1` · `len(c) == 1` · trần thân 65 536 (hai phía) · trần đọc 65 537 · `HIEU_LUC` đúng 1 800 s · hạn REST đúng 15 s (`b4_han_khac_15`) · hạn bộ phân loại đúng 120 s (`b4_han_pl_khac_120`) · OID so trọn 40 ký tự (7b) · `ls-remote` lấy đúng OID đầu. Hai chỗ KHÔNG có đột biến riêng, có lý do: `gia_tri` cắt `[:120]` — đặc tả nói "tối đa 120 ký tự", cắt ngắn hơn vẫn đúng đặc tả; kiểm băm commit M theo riêng loại — `rev-parse …^{commit}` của tự kiểm 7a đã băm lại commit (đo: commit giả ⇒ 7a đỏ trước bước 4), nên bỏ riêng phép kiểm ấy là đột biến tương đương. Không còn `read-tree`/`checkout-index` nào trong hàm chạy, nên không còn chốt mã thoát của chúng.

## Chưa đo (`khong_do_duoc` ở lượt này)

- CI PR Ubuntu, `gate-packet-loop-manh` 16 mảnh, `ci-dot-bien-du.yml` trên H: executor không đẩy, không dispatch.
- Windows thật: khung CRLF chỉ mô phỏng; `cong_b4_*` chưa chạy trên Windows (phép kiểm đường dẫn của `_b4_anh_chup` với tên chứa `\` hay ổ đĩa chưa đo trên Windows).
- Cấu hình/thuộc tính git HỆ THỐNG thật: hàm chạy đặt `GIT_CONFIG_NOSYSTEM=1` và `GIT_ATTR_NOSYSTEM=1`; ca `cong_b4_git_khong_he_thong` đo hai biến tới được tiến trình bộ phân loại, KHÔNG đo bằng tệp hệ thống thật (cần quyền root).
- Object của H và lịch sử (merge-base) mà git của bộ phân loại đọc qua alternates KHÔNG được băm lại; chỉ cây chạy (commit M → cây → blob) được dựng từ byte đã kiểm.
- Bảng `MUTANTS` cũ (ngoài `b4_*`): chạy ở `packet-loop-dot-bien.yml` sau merge.
