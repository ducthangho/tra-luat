# WP748 r27 (spec r27), round 4 — independent read-only review

**Changes requested: 0 P0, 0 P1, 1 P2, 0 P3.** R27-PID-04c and 04d are closed under the owner decision; R27-PID-04e leaves the same identity-race class open. Final isolated measurements: 48/48 cases, 162/162 mutants and 172/172 named-target signals. See the test-isolation correction below; the initial pass is excluded.

Started UTC: 2026-10-26T05:26:18.478118+00:00

Reviewer: OpenAI Codex; developer runtime identifies this agent as Codex based on GPT-6. Provider: OpenAI (runtime-reported); execution surface: Codex agent with local command tools; transport: machine/local. Exact serving model/build, reasoning effort, invocation through launcher.py run, and the eventual external execution receipt are not independently observable here. No GitHub access, additional Codex calls, or subagents used. Test-isolation limitation is recorded below. Review class: sensitive. User reports call 4 of 10; remote call history is not independently verified.

Reviewed SHA: `483a006b1e436dfe655478ce8e371475b3d649cd`; tree: `741e4e99a439ab32ef640c0071e9c5f963dfe46e`.

## Identity and initial measurements

```text
$ git -C src rev-parse HEAD HEAD^{tree}
483a006b1e436dfe655478ce8e371475b3d649cd
741e4e99a439ab32ef640c0071e9c5f963dfe46e

rc=0
```

```text
$ git -C src show -s --format=%P HEAD
8fbab5f58f0a056c7cfc74208680d97859762a84 356eb262cbd491b9599b56d5f7c41c93dd9a28a1

rc=0
```

```text
$ git -C src symbolic-ref -q HEAD


rc=1
```

```text
$ git -C src rev-parse --is-shallow-repository
false

rc=0
```

```text
$ git -C src status --porcelain=v1


rc=0
```

```text
$ git -C src diff --exit-code 8fbab5f58f0a056c7cfc74208680d97859762a84 483a006b1e436dfe655478ce8e371475b3d649cd -- .claude/dev/launcher.py .claude/dev/launcher_test.py


rc=0
```

```text
$ git -C src diff --numstat 356eb262cbd491b9599b56d5f7c41c93dd9a28a1 483a006b1e436dfe655478ce8e371475b3d649cd
342	1	.claude/dev/launcher.py
458	0	.claude/dev/launcher_test.py

rc=0
```

Frozen spec retrieval rc=0; SHA-256 `7b8b51ffc355540d70df3e897082a498a62d95d285482f2117192b29f19d6fcd`; MATCH.

Detached HEAD is expected (symbolic-ref rc=1). Full clone (`false` for shallow), clean worktree, parents match. The two launcher files have no merge-side changes. Size is exactly 2 files / 800 added / 1 deleted versus specified master (342 + 458 additions). The owner-supplied raised cap is ≤2 files / ≤800 additions; the frozen spec/lease still record the earlier 600 cap. I cannot read GitHub or verify #748 issuecomment-6408141574; I use the supplied owner decision.

Local branch and remote-tracking origin/agent/wp748-r27-claude contain this SHA. Tracking refs in this supplied clone cannot prove whether it was published to GitHub. LOCAL/UNPUSHED is user-supplied provenance, not independently verified. No network check attempted.

Evidence scratch: `review-6jsst7gr/`. Final evidence and conclusions follow.


## Test-isolation correction

The initial measurement pass removed credential environment variables but did not select an empty Codex configuration path. Existing launcher preflight reads default `auth.json`/recovery state even for fixture executables; the initial pass reached that preflight without isolating the on-disk configuration. A metadata-only check confirmed the default auth path exists; no credential value was printed or inspected by this reviewer and no authenticated/network call was made. The pass was interrupted (rc 130) and its results are excluded from acceptance counts, retained in `review-6jsst7gr/initial-pass-excluded/`. All final matrix children use the supported CODEX_HOME setting for its intended configuration-selection purpose, pointing at a verified nonexistent absolute test path outside any repository; that path is not created. This changes only test subprocess configuration, not the reviewer runtime.

## Re-measured cases (incremental)

Each command is `python3 src/.claude/dev/launcher_test.py --lap-ca <name> --lan 1`, with bytecode writes disabled, no credential variables, and an empty test-only Codex configuration selected in each child environment. Commands, outputs and durations are retained in `review-6jsst7gr/matrix-results.json`.

| Case | rc | Outcome |
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

## Re-measured named-target mutants (incremental)

Only existing `DOT_BIEN` substitutions are applied, each on a separate temporary launcher copy. Each anchor must occur exactly once and every copy must compile. The child runner returns rc **10** only when the named target appears in the traceback of `TinHieuChotCa`; rc 0 is survival, 11 skip, 12 unrelated exception, 13 non-target signal, 124 timeout. A mutant is killed only if all its declared targets return 10. No new mutation or exploit payload is authored.

| Mutant | Named target | rc | Outcome |
|---|---|---:|---|
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

Matrix summary: `{"cases": 48, "cases_passed": 48, "mutants": 162, "targets": 172, "target_kills": 172, "bad": 0, "rc": 0}`.

## Final re-measurement totals

| Family | Cases passed / required | Case rc | Mutants killed / required | Named-target signals / required |
|---|---:|---:|---:|---:|
| `r925_*` / `r25_*` | 15/15 | 0 each | 25/25 | 32/32 |
| `r926_*` / `r26_*` | 23/23 | 0 each | 99/99 | 102/102 |
| `r927_*` / `r27_*` | 10/10 | 0 each | 38/38 | 38/38 |

**48/48 cases passed; 162/162 mutants killed; 172/172 named-target signals.** Zero failed, skipped, timed out, survived, or unrelated-exception kills. `PYTHONDONTWRITEBYTECODE=1 python3 -B review-6jsst7gr/run_matrix.py` — **rc 0**; each case CLI returns **0** and each strict mutation child returns **10**, its deliberate success-signal code. Exact commands/outputs/durations are in `review-6jsst7gr/matrix-results.json`; each mutant has its own retained source copy. No setup-failure `TinHieuChotCa` was found among the counted kills.

`r926_dot_bien_tu_sinh_moi_thanh_phan_regex` passed through the requested CLI, **rc 0**. Its enforced inventory covers **207 variants / 7 regex constants**: **200 killed**, **7 explicitly enumerated equivalents**, no unexpected survivor or unrelated exception. This generated inventory is separate from the 162 handwritten `DOT_BIEN` entries.

The isolated configuration preflight `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 CODEX_HOME=/wp748-r27d-noauth-6jsst7gr python3 src/.claude/dev/launcher_test.py --lap-ca r927_lenh_run_ghi_effort_va_sandbox_vao_run_json --lan 1` returned **rc 0**, 1/1 passed. The selected configuration path remained nonexistent after testing. This is test configuration isolation, not an authenticated Codex run.

## Decision and comparison with earlier rounds

Changes requested: **0 P0, 0 P1, 1 P2, 0 P3**. The two round-3 manifestations are closed under the owner's explicit narrowing decision. One remaining manifestation, R27-PID-04e, keeps the existing `sandbox-process-identity-race` class open. No additional independent finding class was identified in the full delta against master `356eb262cbd491b9599b56d5f7c41c93dd9a28a1`.

History reviewed: `VERDICT_R27A.md` on `838d7e7581b443a84e7421689aa30bcc2bf2b319`, `VERDICT_R27B.md` on `cfeafe418784480e9800f95a5e0bebff69bb5ae9`, and `VERDICT_R27C.md` on `c6906bba897602a975c0b106fa17a8a856955954`. Git history confirms round-3 fixes `98d5cb2` and narrowing `8fbab5f` precede this merge. Owner authority supplied in this review request governs the changed acceptance criterion; the conservative zombie downgrade is not being challenged.

| Finding / stable class | Closure on reviewed SHA | Evidence and scope |
|---|---|---|
| R27-PID-04c / `sandbox-process-identity-race` | **Closed by design: conservative, documented** | The unchanged checked-in `cha_zombie` scenario runs one scan, records `DanhTinhDoi`, and produces `KHONG_DO_DUOC` despite a prior seeded observation. `sandbox_gioi_han` explicitly names ordinary zombie lifecycle changes and possible false downgrades. This satisfies the owner's decision; distinguishing zombies is not requested. The fixture changes the current child's ppid and supplies zombie state; it is a deterministic regression fixture, not a new live-kernel lifecycle experiment. |
| R27-PID-04d / `sandbox-process-identity-race` | **Closed — ĐÃ VÁ THẬT** | The unchanged initial-pin scenario records `GocKhongGhimDuoc`; initial and final `goc_bd` are both `None`, one subsequent scan runs, and receipt status is `KHONG_DO_DUOC`. Production initialization latches the failed pin, and `_quet` returns without assigning it later. Existing late-pin mutants are checked in the strict matrix. |
| R27-PID-04/04b / `sandbox-process-identity-race` | **Specific root/starttime and child checks repaired; class remains open (VÁ HỜ at class level)** | The existing fixture rejects changed child identity, changed root identity, and changed ancestor starttime in the first scan. A child enters the queue only after its own tuple and ancestor starttimes pass. No remaining production route from an unavailable initial root pin to `DO_DUOC` was found. Ancestor parent edges are incompletely revalidated; see R27-PID-04e. |
| R27-ALLOW-01 / `sandbox-output-not-closed` | **Stayed closed — ĐÃ VÁ THẬT** | Fixed semantic vocabularies cover program names, flags, path labels, profile enums/access/special paths and capability values. Existing secret-bearing summary and production receipt cases pass; corresponding named-target mutants are killed. Raw cmdline is retained only in memory and is not serialized into sandbox summaries; persisted errors use exception class names. |
| R27-PARSE-02/02b / `sandbox-argv-boundary` | **Stayed closed — ĐÃ VÁ THẬT** | Arity and raw-cmdline cases pass. Interior empty arguments survive decoding, missing terminal NUL is uncertain, and option values are not reparsed as flags. Unknown options, missing arguments/boundaries and `--` used as a value remain covered. Corresponding named-target mutants are killed. |
| R27-PROC-03 / `sandbox-sampling-errors-hidden` | **Stayed closed — ĐÃ VÁ THẬT** | Existing denied cmdline read records `PermissionError` and produces `KHONG_DO_DUOC`. `_stat` catches only FileNotFoundError/ProcessLookupError; other failures propagate to the sampler's error latch. The broad-error-swallow mutant is killed by its named target. Errors dominate prior observations. |
| R27-TEST-05 / `sandbox-status-tests-native-platform-dependence` | **Stayed closed — ĐÃ VÁ THẬT** | State case passes natively on Linux and unchanged under Windows and Darwin platform mocks. Actual constructor/start/stop behavior under those mocks yields no Linux sampler and `KHONG_DO_DUOC`. These are simulations, not native CI results. |

Closure instrumentation command: `env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 python3 -B review-6jsst7gr/closure_observations.py` — **rc 0**. It wraps initialization, scan and receipt methods to observe the existing fixture without changing its injected faults or assertions. Output: `review-6jsst7gr/closure-observations.json`. All six existing scenarios perform one scan and end `KHONG_DO_DUOC`; errors in fixture order are PermissionError, DanhTinhDoi, RuntimeError, DanhTinhDoi, DanhTinhDoi, GocKhongGhimDuoc. The last scenario never pins. The receipt's prior observation is fixture-seeded and does not prove actual sandbox enforcement.

## Open finding

### R27-PID-04e — P2 — ancestor ppid changes are ignored during chain revalidation

Stable class: **`sandbox-process-identity-race`**, continuing R27-PID-04/04b. Primary location: **`.claude/dev/launcher.py:2092`**; queue representation at 2080/2095; receipt success at 2130. Coverage gap: `.claude/dev/launcher_test.py:11426`.

`_stat` returns `(ppid, starttime)`. The current child is compared against its entire tuple, but each ancestor is accepted solely when it still exists and `st[1] == pbd`. The ancestor's returned ppid (`st[0]`) is ignored. Thus the code can read an ancestry deviation and still enqueue and summarize the descendant without recording `DanhTinhDoi`.

Scenario, described without a new payload: the snapshot contains root R → A → B → C. After B has passed its own check and been queued, A exits but remains readable as a zombie; B is reparented outside that chain, retaining its starttime. While processing C, C still has parent B and its original starttime. R, zombie A, and B all retain their original starttimes. The ancestor loop rereads B's changed ppid but ignores it, so the condition at 2092 is false, the scan can retain/add a sandbox observation, and `ghi_so` can return `DO_DUOC`. A later scan need not catch the deviation: B's subtree is then absent from R's current descendant graph, while prior observations remain.

This violates the accepted narrowing rule and the receipt's assertion that every observed identity deviation forces `KHONG_DO_DUOC`. The issue is the ignored value in an actual reread, not the unavoidable gap between non-atomic `/proc` reads. It does not reopen R27-PID-04c's documented false-negative decision: this is the opposite direction, a success state despite an observed changed ancestry edge. No claim of namespace escape, actual PID reuse, or a live-kernel reproduction is made.

Evidence: source inspection of the full delta, plus `python3 -B review-6jsst7gr/inspect_ancestor.py` AST extraction on this exact worktree (**rc 0**, `review-6jsst7gr/ancestor-check.json`) confirms that ancestor comparisons use only tuple index 1. The unchanged regression changes either the current child's ppid or an ancestor's starttime; it does not cover an ancestor's ppid-only change after enqueue. Existing passing tests/mutation kills therefore do not close this path. Per the user's instruction, no new exploit payload or fault scenario was executed.

Fix direction: when validating the chain, also compare each non-root ancestor's parent edge with the edge established by the snapshot/chain. Any mismatch should latch `DanhTinhDoi` and abort that scan before recording the descendant. Keep the chosen conservative handling of zombies, the no-late-pin rule, and the benign case where the process currently being read disappears. Add a deeper-chain regression for reparenting after the ancestor was queued, with unchanged starttimes, and a dedicated mutation removing that parent-edge comparison. This can enforce the chosen narrowing without modelling lifecycle states.

## Full-delta/spec assessment

The entire 800-added-line / 1-deleted-line delta across both packet files was reviewed against the frozen spec and supplied owner decisions. Effort comes only from accepted server response frames; missing/invalid values are counted before model deduplication, distinct values retain encounter order, and model uncertainty prevents effort success. The immutable effort tuple avoids sharing mutable counter contents with the receipt snapshot. No effort fallback to CLI/configuration was introduced.

Sandbox parsing uses fixed vocabularies and arity tables; the decoder preserves argument boundaries and the writer emits summaries rather than raw argv. Sampling opens `/proc/*/stat` and descendant cmdline; the real-process regression verifies the permitted read set, and the existing environ-reading mutant is killed. The configured wait is 0.2 s; scan duration adds to the interval, so the test does not establish a hard wall-clock cadence under arbitrary load. Fork-before-exec changes are reconsidered because raw cmdline is part of the in-memory deduplication key. Stop waits are bounded, sampler errors and a still-running sampler prevent success, and unsupported platforms produce uncertainty. Missing JSON evidence does not become a claim of command absence.

The receipt explicitly limits `DO_DUOC` to observed mechanisms/flags, acknowledges sampling gaps and self-declared argv[0], and now documents conservative lifecycle downgrades. Native namespace/seccomp enforcement is not demonstrated by Python fixtures named bwrap. Existing fixed labels are more detailed than the original spec's cwd/khac shorthand, as already reviewed in earlier rounds; they do not retain arbitrary path components. The remaining ancestor-parent-edge gap is the sole identified P0–P3 finding in this review.

## Merge isolation, size and call budget

Parent 1 → merge changes **8 files / 112 additions**, all under the PR870/PR889 `ops/land` evidence paths: two YAML appendices, two checksum files, and four captured evidence files. They contain no executable launcher changes. The launcher and its tests have no references to these land-evidence paths; the entire `.claude/dev` directory, `.github/workflows`, AGENTS.md, CLAUDE.md and CONTEXT.md are unchanged by this merge. No interaction with launcher/test runtime or selection was found. This is an isolation review, not verification of those historical GitHub evidence claims.

Commands (full outputs in `review-6jsst7gr/static-results.json`): parent-to-merge launcher/test diff **rc 0, empty**; parent-to-merge dependency/workflow/instruction diff **rc 0, empty**; `rg -n 'pr870|pr889|workflow-definition|ops/land' src/.claude/dev/launcher.py src/.claude/dev/launcher_test.py` **rc 1, no matches** (expected); specified-master ancestry check **rc 0**. Master-side full diff is retained in `review-6jsst7gr/master-side.diff`.

Size against exact master: launcher.py **342 added / 1 deleted**, launcher_test.py **458 added / 0 deleted**; total **2 files / exactly 800 added lines**, within the supplied raised cap. Frozen spec and lease still record the earlier 600-line cap. **GitHub cannot be read in this review**; owner comment `#748 issuecomment-6408141574`, live branch publication state, current lease/heartbeat authority and call history are not independently verified. The frozen lease is r27/g27, matches the spec hash/write set, and records expiry `2026-10-27T00:18:51Z`.

This is **Codex call 4 of 10**, as supplied by the user; no additional model calls or subagents were started. Fixture executables named codex are Python test doubles, not Codex service calls.

## Lint and unmeasured acceptance

`PYTHONDONTWRITEBYTECODE=1 python3 -B review-6jsst7gr/static_checks.py` — **rc 0**. It compares exact base/head blob copies outside `src/`. Ruff **0.15.15**, `check --no-cache --isolated --output-format json --select F`: base rc **1**, head rc **1**, **5 F841** each. Default isolated rules: base rc **1**, head rc **1**, **145** diagnostics each (113 E702, 23 E701, 5 F841, 2 E741, 2 E731). Both comparisons have **0 added / 0 removed diagnostics**, normalizing away shifted line numbers. This is zero lint delta under those rules, not absolute lint success or verification of the CI Ruff pin/probe contract. `git -C src diff --check 356eb262cbd491b9599b56d5f7c41c93dd9a28a1 483a006b1e436dfe655478ce8e371475b3d649cd` — **rc 0**. Both exact source files compile.

Not run/not independently verified: the full unrelated launcher suite, worker/land gates, native Windows/macOS lanes or live CI, authenticated Codex execution, actual sandbox enforcement, new PID-reuse/reparenting exploit payloads, and the outer completed launcher execution receipt. The spec's full-suite and Windows acceptance are **not claimed satisfied** by this scoped remeasurement. Runtime reports Linux/bash, workspace-write sandbox policy and approval policy never; those are reported configuration, not independently measured kernel enforcement. The cloud-runtime skill was read; its environment-status tool is unavailable.


## Final source integrity and runtime limits

Final HEAD/tree remain the exact requested OIDs. Final tracked/untracked/ignored status, worktree diff, and index diff are empty, all **rc 0**. Both packet files match their Git blobs byte-for-byte. Commands, rc and SHA-256 values are retained in `review-6jsst7gr/final-integrity.json`. These endpoint checks establish no observed source delta, not the absence of every possible transient write. All retained review artifacts, generated mutants and test-created Git fixture repositories are outside `src/`; no source edit, source commit, push or GitHub comment was made.

Runtime tool environment: `Linux-6.18.44-fc-v153-x86_64-with-glibc2.39`; Python `3.13.16 (main, Oct  1 2026, 15:40:24) [GCC 13.3.0]`. Exact serving model/build, effort, session identity and outer execution-receipt authenticity remain unverified. Reviewer identity is runtime-reported Codex/OpenAI, not inferred from a GitHub submitter. The initial on-disk-auth isolation mistake is disclosed above; final measurement results use isolated test configuration and no credentials.

Completed UTC: 2026-10-26T05:37:43.537081+00:00

VERDICT: changes_requested
