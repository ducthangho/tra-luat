# WP748 r27 / spec r27 — independent review, round 3

Review complete: changes requested (2 P2 manifestations in 1 class). Reviewer: OpenAI Codex, as identified by this session’s system/developer runtime context. The exact serving model/build and an independent launcher execution receipt have not yet been verified. User states this is Codex call 3 of 10; no additional Codex calls or subagents will be launched. Review class: sensitive.

Started UTC: 2026-10-26T04:50:51.235028+00:00

Reviewed SHA: `c6906bba897602a975c0b106fa17a8a856955954`; tree: `9ee009dec3e52802b654176b7d7ecb3d6d5ed8b3`.

Read-only scope: no source edits, commits, pushes, GitHub reads/comments, or credential use. Scratch: `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4`. GitHub cannot be read in this review under the user’s constraint; issue comment and remote publication state cannot be independently checked.

## Identity commands

`git -C src rev-parse HEAD HEAD^{tree}` — rc 0

```text
c6906bba897602a975c0b106fa17a8a856955954
9ee009dec3e52802b654176b7d7ecb3d6d5ed8b3
```

`git -C src symbolic-ref -q HEAD` — rc 1

```text
(no output)
```

`git -C src rev-parse --is-shallow-repository origin/master agent/wp748-r27-claude` — rc 0

```text
false
cebb5b22e1ebf369a70234662b7e9355bdd5095e
c6906bba897602a975c0b106fa17a8a856955954
```

`git -C src show -s --format=%P HEAD` — rc 0

```text
f310af45d2bd571b296f6125e6caa81d7a3774e0 cebb5b22e1ebf369a70234662b7e9355bdd5095e
```

`git -C src merge-base --is-ancestor cebb5b22e1ebf369a70234662b7e9355bdd5095e HEAD` — rc 0

```text
(no output)
```

`git -C src diff --exit-code f310af45d2bd571b296f6125e6caa81d7a3774e0 c6906bba897602a975c0b106fa17a8a856955954 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` — rc 0

```text
(no output)
```

`git -C src status --porcelain=v1` — rc 0

```text
(no output)
```

Identity matches the required hash, tree, two parents, full clone, detached HEAD, branch pointer, and master ancestry. Detached `symbolic-ref` rc 1 is expected. Local remote-tracking refs are not evidence of remote publication. The specified merge diff is empty.

## Frozen inputs and size (initial measurement)

`git -C src show origin/ops/wp748-r27-g27-lease:ops/specs/wp748-r27-launcher-effort-sandbox.md` — rc 0; output `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4/spec.md`; SHA-256 `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd`.

`git -C src show origin/ops/wp748-r27-g27-lease:ops/leases/wp748-r27-g27-claude-remote-20261026.yaml` — rc 0; output `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4/lease.yaml`; SHA-256 `e91e7d2a644e161c0f09761155e9f5f63a287dee85371dfaa2501a52889b130f`.

`git -C src diff cebb5b22e1ebf369a70234662b7e9355bdd5095e c6906bba897602a975c0b106fa17a8a856955954` — rc 0; output `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4/delta.diff`; SHA-256 `14e1d8f6e476c00a303e9f72b77b01eb5f7ed9665d57006e930f4b9f575ec0ac`.

`git -C src show 5217887 f310af4` — rc 0; output `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4/fixes.diff`; SHA-256 `9660319b6f658bc42dad2dedee80db15305851afc2586ced274a78d3b4752237`.

`git -C src diff --stat f310af45d2bd571b296f6125e6caa81d7a3774e0 c6906bba897602a975c0b106fa17a8a856955954` — rc 0; output `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4/master-side.txt`; SHA-256 `56e4279f51446201fc85d075e2dc831f9be1ac3bb47b42b57fb6566b531d1da8`.

`git -C src diff --numstat cebb5b22e1ebf369a70234662b7e9355bdd5095e c6906bba897602a975c0b106fa17a8a856955954` — rc 0; output `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4/size.txt`; SHA-256 `e52f1fade1859252df423a009af9a6c7b3fff0013b19831f4e7c82e0e96aaa34`.

## Re-measured cases (incremental)

Credential-free Linux subprocesses; bytecode disabled; scratch temp/cache and an absent test-only Codex configuration. Case command: `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1`. Exact argv, rc, duration and log are in `/tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rvL/r27c/r27-review-1w5wvcc4/results.json`.

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

## Re-measured named-target mutations (incremental)

Only the checked-in `DOT_BIEN` substitutions were applied, to separate scratch copies of launcher.py. The child runner returns **rc 10** only for `TinHieuChotCa` with the named target present in its traceback; rc 0 means survival, rc 11 skip, rc 12 unrelated exception, rc 13 non-target signal. Anchors must occur exactly once and compile must succeed. A kill requires every declared named target to meet the strict signal rule.

| Mutant | Named target | rc | Result |
|---|---|---:|---|
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

Matrix summary: `{"cases": 48, "cases_passed": 48, "mutants": 161, "targets": 171, "target_kills": 171, "bad": 0, "rc": 0}`.

## Decision and comparison with the previous rounds

**Changes requested: 2 open P2 manifestations in 1 existing root-cause class; 0 P0, 0 P1, 0 P3.** The exact empty-argument defect is closed. The reported single-scan root/ancestor checks now work, but the process-identity/lifecycle class is not closed: normal zombie teardown is misclassified, and an unavailable initial root identity is still adopted later.

History anchors: round 1 `VERDICT_R27A.md`, `838d7e7581b443a84e7421689aa30bcc2bf2b319`; round 2 `VERDICT_R27B.md`, `cfeafe418784480e9800f95a5e0bebff69bb5ae9`. Both `5217887906a354452bcd76b7da23778ec63ecf46` and `f310af45d2bd571b296f6125e6caa81d7a3774e0` were inspected. All current measurements use the requested merge SHA, not a pre-merge copy.

| Finding / stable class | Closure on this SHA | Executed evidence and class sweep |
|---|---|---|
| R27-PARSE-02b / `sandbox-argv-boundary` | **Closed — ĐÃ VÁ THẬT** | `r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that` and `r927_ngu_phap_sandbox_theo_bang_so_doi_so`: rc 0. Both empty-argument and missing-terminal-NUL mutants are killed by the named target with `TinHieuChotCa` (child rc 10). Independent ordinary Python argv round trip: 5 arguments, 1 interior empty argument retained. Both unchanged `_R27_BWRAP` and `_R27_CLS` fixtures pass through the actual byte decoder and produce the same summaries as their list inputs. Missing NUL, option/value arity, `--` in a value, command boundary, unknown flag and truncated argument cases were checked; no further actionable parser manifestation found. |
| R27-PID-04b / `sandbox-process-identity-race` | **Not closed — VÁ HỜ at class level** | The reported within-scan defects are corrected: the existing identity target returns rc 0; root-pin, ancestor-validation and child-reread mutants all raise the named target's `TinHieuChotCa`, rc 10. Instrumenting that unchanged fixture records **one scan per scenario**, with `PermissionError`, `DanhTinhDoi`, `RuntimeError`, `DanhTinhDoi`, all `KHONG_DO_DUOC`. Root-reuse fixture reads the pinned starttime then `1` in its first scan, and fails immediately. Children are enqueued only after child and chain validation. However, the additional startup and ordinary-exit measurements below leave this same class open (R27-PID-04c/d). |
| R27-ALLOW-01 / `sandbox-output-not-closed` | **Stayed closed — ĐÃ VÁ THẬT** | Allow-list and production receipt cases rc 0; their named mutants are killed by `TinHieuChotCa`. Independent byte-decoder → summary → writer measurement on the unchanged secret-bearing fixtures gives 2 summaries, 0 strings outside the fixed vocabulary, and no existing fixture secret markers. Bind destinations, cwd flags, profile enum/path values, capability values, program names and option names are reduced to fixed constants. No newly authored secret/exploit argv was used. |
| R27-PROC-03 / `sandbox-sampling-errors-hidden` | **Stayed closed — ĐÃ VÁ THẬT** | Existing denied-read fixture rc 0, cmdline-swallow mutant killed, rc 10. Independent `_stat` checks propagate `PermissionError` and generic `OSError`; only `FileNotFoundError`/`ProcessLookupError` return disappearance. General scan errors reach `_chay`'s latch and override earlier observations. The zombie false error below is a lifecycle classification defect, not a regression to swallowed I/O errors. |
| R27-TEST-05 / `sandbox-status-tests-native-platform-dependence` | **Stayed closed — ĐÃ VÁ THẬT** | Native Linux state-case rc 0. The unchanged state fixture also passes under Windows and Darwin platform mocks. Actual constructor/start/stop/writer calls under those mocks have no sampler thread and yield `KHONG_DO_DUOC`. These are simulations on Linux, not native platform CI. |

Independent probe command: `python3 -B r27-review-1w5wvcc4/probes.py` — **rc 0**; exact absolute argv/duration in `probe-command.json`, observations in `probes.json`, output in `probes.log`. The first probe run and the expanded final run both returned rc 0; the final retained run includes three paired normal-exit controls. The final run uses an environment allow-list without credential variables. The probes reuse the checked-in identity fault fixture and sandbox argv fixtures, plus ordinary Python child processes; they do not attempt live PID reuse or create new exploit payloads.

## Open findings

### R27-PID-04c — P2 — an exited but unreaped parent poisons a normal run's sandbox measurement

Stable class: `sandbox-process-identity-race` (continuation of R27-PID-04/04b).

Location: `.claude/dev/launcher.py:2085`; contributing parser at `.claude/dev/launcher.py:2050`; receipt downgrade at `.claude/dev/launcher.py:2124`.

Scenario: a normal descendant parent exits while its child remains alive, for example a shell/helper that leaves a background child. Linux reparents the child while the dead parent may still have a readable `/proc/<pid>/stat` in state `Z`. The child's starttime is unchanged; only its ppid changes. `_stat` discards process state, so `self._stat(cha) is not None` treats the zombie as a living parent and appends `DanhTinhDoi`. That error is permanent for the run: even a previously valid sandbox observation is downgraded to `KHONG_DO_DUOC`. Whether the launcher/supervisor has reaped the parent yet becomes an accidental determinant of measurement success. This contradicts the intended quiet handling of ordinary ancestor exit.

Measurement: three ordinary process-tree runs, with real kernel stat bytes and no forged PID/starttime/argv, produced the following; three controls differ only by reaping the exited parent before the sampler's reread. The prior valid sandbox observation was seeded from the unchanged checked-in `_R27_BWRAP` summary to isolate receipt aggregation; this is not an authenticated Codex run or proof of actual namespace enforcement.

| Timing | Runs | Parent state before reread | Child starttime | Errors | Receipt |
|---|---:|---|---|---|---|
| Parent exited, not yet reaped | 3/3 | `Z` | unchanged | `DanhTinhDoi` | `KHONG_DO_DUOC` |
| Same exit, parent reaped before reread | 3/3 | `Z` observed, then reaped | unchanged | none | `DO_DUOC` |

`probes.json` preserves the individual ppid/starttime values (e.g. ppid 79 → 1 with starttime `244874` unchanged). Probe rc 0 means the assertions confirming this bug and its controls passed, not that production behavior is correct. This establishes that ordinary lifecycle events can spuriously invalidate measurement; it does not establish how frequently an authenticated Codex session encounters the race.

Fix direction: retain enough `/proc/stat` process-state information to distinguish a live identity, an exited/zombie identity and a missing entry. Treat ordinary reparenting after a verified ancestor exit as disappearance and discard the affected observation/subtree without latching an identity-reuse error. Continue to reject actual starttime changes and I/O failures. Add a synchronized live-parent → zombie → reaped regression, with unchanged child starttime and a previous valid observation, plus controls for real identity changes. Guard against an overly broad fix that suppresses reuse or permission errors just because a parent is gone; compare identity changes separately from ppid changes and lifecycle state.

### R27-PID-04d — P2 — a missing initial root identity is silently acquired during a later scan

Stable class: `sandbox-process-identity-race`; the initial-binding part of R27-PID-04b remains incomplete.

Location: `.claude/dev/launcher.py:2062`, fed by `.claude/dev/launcher.py:2029`.

Scenario: if the initial `_stat(pid)` returns disappearance, `goc_bd` remains `None` and no uncertainty is latched. A later scan assigns the starttime of whichever process then owns that numeric PID. The validation chain is now rooted in that later identity, not an identity established immediately after spawning the intended child. If the original process has disappeared and the PID becomes visible again with a new owner, that owner and its descendants can satisfy all subsequent checks. Thus the implementation still has the original late-pin path for the unavailable-initial-identity case; it cannot justify attributing a later observation to the launched child in that case.

Measurement: `python3 -B r27-review-1w5wvcc4/unavailable_pin.py` — **rc 0** (`unavailable-pin-command.json`). It reuses `r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ` unchanged, injecting only **one unavailable initial root lookup**. Observed: initial pin `null`, later pin `265945`, errors `[]`, 1 observation, `sandbox_trang_thai=DO_DUOC`. No replacement process or new sandbox argv was authored. This measures acceptance without the initial anchor. Actual kernel PID reuse and attribution to a replacement were **not executed**; that consequence is the control-flow inference described above, not an empirical exploit claim.

Fix direction: distinguish “initial identity unavailable” from “identity not initialized yet.” Once initialization cannot bind the launched root, do not recover trust by assigning a later PID occupant; stop attribution and record measurement uncertainty as appropriate. Keep the existing early-pin path and same-scan chain comparisons. Add a regression that the unavailable initial lookup cannot later produce attributed `DO_DUOC`, while a normal pinned root still can. Preserve non-Linux behavior, ordinary fast-exit handling, and I/O failure reporting; do not turn transient process disappearance into fabricated root identity.

These are **2 manifestations / 1 open class**, both P2. No additional independent P0–P3 class was identified in the full packet delta.

## Full-delta/spec review and conservative-state assessment

The review covers the full 779-added-line packet delta against exact master `cebb5b22e1ebf369a70234662b7e9355bdd5095e`, including the added tests and mutation table, and the round-2 fixes.

Effort is taken from accepted server frames only; invalid/missing reasoning leaves model acceptance intact but increments the missing-effort count before model deduplication. First-seen distinct effort values are retained in an immutable tuple, then copied into the receipt. Model failure dominates effort success. The r925/r926 remeasurement covers the unchanged stderr allow-list, filtering, close/join and lost-frame behavior; no config/CLI fallback for measured effort was added.

Sandbox summaries use fixed labels/enums and two arity tables. Raw cmdline stays in memory for deduplication and is not serialized; summaries and exception class names are written. The sampler's production reads are limited to `/proc/*/stat` and descendant `cmdline`; the checked-in real process test verifies no `environ` access. Its synthetic `argv[0]` fixture tests observation and serialization, not namespace/seccomp enforcement. The configured wait is 0.2 seconds; scan cost adds to the effective interval, so this is not a hard wall-clock guarantee under arbitrary host load. Thread stop is bounded and a still-running sampler prevents `DO_DUOC`.

A genuinely disappeared ancestor ending a scan quietly does not itself create a new observation: the current child is not enqueued or attributed until validation passes. Earlier validated observations may remain `DO_DUOC`, which is consistent with the explicitly limited claim “a sandbox mechanism was observed,” not “every command was sandboxed.” With no observation and stdout command items, the result remains `KHONG_DO_DUOC`. Detected root/ancestor identity changes now invalidate success within that scan. However, quiet handling is incomplete for zombies (04c), and a root never anchored at initialization can still be accepted later (04d). Accordingly the tested conservative exit path is reasonable, but the overall implementation still permits both spurious unknown status and an insufficiently anchored success path.

The fixed path labels (`/`, `/tmp`, `/dev`, `/proc`, `workspace`, `trong_workspace`, `to_tien_workspace`, `khac`) are more detailed than the frozen spec's `cwd`/`khac` shorthand; this was already explicit in the round-2 accepted allow-list repair. They do not retain arbitrary path components. The receipt limitation explicitly acknowledges sampling gaps and self-declared argv[0]. No claim is made that repeated `/proc` reads constitute an atomic kernel snapshot.

## Merge isolation, size and call budget

Parent-1 → merge changes only `.claude/dev/ci_dang_ky_test.py` (one registry entry), new `ops/ci_provenance.py`, and its new tests: 3 files / 2045 additions. The entry registers the provenance test's own output contract; it does not change launcher test selection or its output contract. The new module is standalone CI evidence tooling; neither launcher file imports or refers to it or the changed registry. The launcher, its test, companion modules, Linux shell helper and launcher Windows workflow are byte-unchanged by this merge. No interaction with launcher/test runtime was found. This is an interaction review, not a separate audit of the new master's CI provenance feature.

Measured commands: specified parent-to-merge launcher/test diff **rc 0, empty**; dependency/workflow comparison **rc 0, empty**; `rg -n 'ci_provenance|ci_dang_ky_test'` over both launcher files **rc 1, no matches** (expected). Master ancestry is verified. Merge motivation and remote publication status cannot be established offline.

Size against the requested master: launcher.py **342 added / 1 deleted**; launcher_test.py **437 added / 0 deleted**; total **2 files / 779 added**, within **2 files / 800 added**. The frozen spec and original lease still state 600. The effective 800-line cap is the user's supplied owner authorization, `#748 issuecomment-6408141574`; **GitHub cannot be read in this review**, so that comment's live contents were not independently verified. The local lease matches revision/generation 27 and the frozen spec hash and expires at `2026-10-27T00:18:51Z`; live lease/heartbeat authority was not queried.

This is **Codex call 3 of 10**, as supplied by the user. No additional Codex calls or subagents were started. Python fixture executables named codex are test doubles, not model calls. Live call history cannot be verified without the prohibited remote access.

## Measurement totals, commands and limits

| Family | Cases passed / required | Baseline rc | Mutants killed / required | Target signals / required |
|---|---:|---:|---:|---:|
| `r925_*` / `r25_*` | 15/15 | 0 each | 25/25 | 32/32 |
| `r926_*` / `r26_*` | 23/23 | 0 each | 99/99 | 102/102 |
| `r927_*` / `r27_*` | 10/10 | 0 each | 37/37 | 37/37 |

Total: **48/48 cases passed**, **161/161 mutants killed**, **171/171 named-target signals**; **0 failed, 0 skipped, 0 timeouts, 0 unrelated-exception kills**. Matrix driver command `python3 -B r27-review-1w5wvcc4/run_matrix.py` — **rc 0**. Each strict mutation child returned rc **10**, the review runner's deliberately assigned code for a `TinHieuChotCa` from its named target; this is not an ordinary successful exit. Source anchors occurred exactly once and every mutated copy compiled. The stock mutation runner was not trusted to count arbitrary exceptions as kills. Full per-case/per-target rc tables appear above; exact commands and logs are in `results.json`.

`r926_dot_bien_tu_sinh_moi_thanh_phan_regex` ran through the requested CLI and passed, **rc 0**. Its enforced inventory is 207 generated variants across all 7 regex constants: 200 killed through its `TinHieuChotCa` path and 7 explicitly listed equivalents, with no unexpected survivor or unrelated exception. These generated variants are separate from the 161 hand-written `DOT_BIEN` entries.

Bare Ruff: **0 added / 0 removed diagnostics** relative to exact master, on external exact-blob copies, Ruff **0.15.15**, `--no-cache`, no repository Ruff config found. `--select F`: rc **1** on base and head, **5 F841** each. Default rules: rc **1** on base and head, **145** each (E702 113, E701 23, F841 5, E741 2, E731 2). Diagnostic comparison uses file/rule/message/source-line/column, excluding shifted line numbers. This is zero lint delta, not absolute lint success and not a CI Ruff pin/probe result. `python3 -B r27-review-1w5wvcc4/static_checks.py` completed rc **0**; individual commands and outputs are in `static-results.json` and `ruff-results.json`. `git diff --check cebb5b22e1ebf369a70234662b7e9355bdd5095e HEAD`: **rc 0**.

Not run / not verified: the complete unrelated launcher suite, worker/land gates, native Windows/macOS lanes, authenticated Codex execution, native bwrap/seccomp enforcement, actual PID-reuse exploitation, live GitHub/CI state, and the completed outer launcher execution receipt. The spec's full-suite and Windows-lane acceptance are therefore **not claimed satisfied** by these scoped measurements. The user explicitly prohibited GitHub/credential access; no network calls or credential operations were performed. Scratch fixture repositories created by the existing tests are outside `src/`; no source commits or source edits were made.

Reviewer identity: provider **OpenAI**, agent **Codex**, runtime instructions say **based on GPT-6**. Actual tool execution is Linux/bash (Python 3.13.16; kernel 6.18.44-fc-v153). The precise served model, reasoning effort, session identity, outer `launcher.py run` command and execution-receipt authenticity are not independently exposed here. The user supplies the launcher invocation claim; this report does not upgrade that to verified runtime model evidence. The runtime declares `workspace-write`, approval policy `never`; actual kernel sandbox enforcement was not separately verified. The cloud-runtime skill was read at startup; its environment-status tool is unavailable.

## Final source integrity

Final `git status --porcelain=v1 --untracked-files=all --ignored`, worktree diff and index diff are empty, all **rc 0**. Final HEAD/tree still equal the requested OIDs; both packet files match their Git blobs byte-for-byte. Commands, rc and file SHA-256 values are in `final-integrity.json`. These endpoint checks show no observed source delta; they do not prove the absence of every possible transient write by an executed test. All review artifacts and retained mutants are outside `src/`.

Completed UTC: 2026-10-26T05:02:27.613100+00:00

VERDICT: changes_requested
