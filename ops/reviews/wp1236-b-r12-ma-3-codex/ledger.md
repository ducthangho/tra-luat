# Ledger MIEN / VI TRI -> o qua consumer L8 (`main` -> L8), do tren ma nguyen ven

Tong: 160 o cua cac bang dot B (ky8) + 8396 phan tu cua bang IMPORT tu bo test dot A (c36). Tat ca DAT (moi o/phan tu da qua phep so cua chinh ca: rc va DUNG danh sach dong L8 voi ky vong viet tu dac ta).

## Bang dot B (ky8)

| ca | so o | duong (khong dong L8) | am (co dong L8) |
|---|---:|---:|---:|
| `c25_b2_l8_ho_so_moi_duong_khong_tep_danh_gia` | 2 | 1 | 1 |
| `c26_b6_l8_duong_khop_tep_danh_gia` | 3 | 2 | 1 |
| `c27_b7_l8_landed_khong_loi_khai` | 14 | 10 | 4 |
| `c29_b3_l8_mien_tru_theo_ten_va_bam` | 2 | 1 | 1 |
| `c30_b4_l8_module_khong_nap_duoc_la_khong_do_duoc` | 1 | 0 | 1 |
| `c31_b8_l8_chay_sau_chot_cutover` | 1 | 0 | 1 |
| `c32_l8_ma_tran_token_va_khoa_qua_cong` | 67 | 41 | 26 |
| `c34_l8_ma_tran_mien_qua_cong` | 50 | 6 | 44 |
| `c35_l8_ngu_phap_tep_danh_gia_qua_cong` | 20 | 3 | 17 |

## c36 — bang ngu phap luat 8 IMPORT tu `ops/gate_output_doi_chieu_test.py`

| ca A (bo sinh + oracle) | vi tri ngu phap | phan tu | duong | am | ly do L8 quan sat (dem) |
|---|---|---:|---:|---:|---|
| `a124_token_ascii_qua_ho_so` | (ca khong chia vi tri) | 1733 | 39 | 1694 | dinh_dang_loi_khai ×1694 |
| `a125_ascii_dong_danh_gia` | truong=run | 318 | 0 | 318 | danh_gia_khong_passed:bo_sinh_la ×20, danh_gia_khong_passed:cr_le ×2, danh_gia_khong_passed:dau_tep_sai ×296 |
| `a125_ascii_dong_danh_gia` | truong=attempt | 318 | 0 | 318 | danh_gia_khong_passed:bo_sinh_la ×20, danh_gia_khong_passed:cr_le ×2, danh_gia_khong_passed:dau_tep_sai ×296 |
| `a125_ascii_dong_danh_gia` | truong=head | 477 | 0 | 477 | danh_gia_khong_passed:bo_sinh_la ×48, danh_gia_khong_passed:cr_le ×3, danh_gia_khong_passed:dau_tep_sai ×426 |
| `a125_ascii_dong_danh_gia` | truong=bo_sinh | 477 | 0 | 477 | danh_gia_khong_passed:bo_sinh_la ×48, danh_gia_khong_passed:cr_le ×3, danh_gia_khong_passed:dau_tep_sai ×426 |
| `a125_ascii_dong_danh_gia` | truong=job | 318 | 0 | 318 | danh_gia_khong_passed:bo_sinh_la ×21, danh_gia_khong_passed:cr_le ×2, danh_gia_khong_passed:dong_la ×295 |
| `a125_ascii_dong_danh_gia` | truong=conclusion | 501 | 0 | 501 | danh_gia_khong_passed:bo_sinh_la ×81, danh_gia_khong_passed:cr_le ×3, danh_gia_khong_passed:dong_la ×417 |
| `a125_ascii_dong_danh_gia` | truong=log | 477 | 0 | 477 | danh_gia_khong_passed:bo_sinh_la ×48, danh_gia_khong_passed:cr_le ×3, danh_gia_khong_passed:dong_la ×426 |
| `a125_ascii_dong_danh_gia` | truong=skip_cu | 318 | 0 | 318 | danh_gia_khong_passed:bo_sinh_la ×21, danh_gia_khong_passed:cr_le ×2, danh_gia_khong_passed:dong_la ×295 |
| `a125_ascii_dong_danh_gia` | truong=skip_v3 | 318 | 0 | 318 | danh_gia_khong_passed:bo_sinh_la ×21, danh_gia_khong_passed:cr_le ×2, danh_gia_khong_passed:dong_la ×295 |
| `a125_ascii_dong_danh_gia` | truong=dat | 159 | 0 | 159 | danh_gia_khong_passed:bo_sinh_la ×10, danh_gia_khong_passed:cr_le ×1, danh_gia_khong_passed:dong_la,thieu_moc ×148 |
| `a125_ascii_dong_danh_gia` | truong=tong | 159 | 0 | 159 | danh_gia_khong_passed:bo_sinh_la ×10, danh_gia_khong_passed:cr_le ×1, danh_gia_khong_passed:dong_la,thieu_moc ×148 |
| `a126_mien_ascii_qua_ho_so` | (ca khong chia vi tri) | 52 | 34 | 18 | waiver_khong_co_can_cu:dong_mien ×16, waiver_khong_co_can_cu:url ×2 |
| `a133_lop_dong_mien_qua_ho_so` | truong=url_path | 168 | 68 | 100 | waiver_khong_co_can_cu:url ×100 |
| `a133_lop_dong_mien_qua_ho_so` | truong=url_id | 160 | 1 | 159 | waiver_khong_co_can_cu:readback ×9, waiver_khong_co_can_cu:url ×150 |
| `a133_lop_dong_mien_qua_ho_so` | truong=sha | 160 | 1 | 159 | waiver_khong_co_can_cu:dong_mien ×144, waiver_khong_co_can_cu:sha ×15 |
| `a133_lop_dong_mien_qua_ho_so` | truong=os | 168 | 39 | 129 | waiver_khong_co_can_cu:dong_mien ×129 |
| `a133_lop_dong_mien_qua_ho_so` | truong=nam | 160 | 10 | 150 | waiver_khong_co_can_cu:dong_mien ×150 |
| `a133_lop_dong_mien_qua_ho_so` | truong=thang | 160 | 1 | 159 | waiver_khong_co_can_cu:dong_mien ×150, waiver_khong_co_can_cu:han ×9 |
| `a133_lop_dong_mien_qua_ho_so` | truong=ngay | 160 | 4 | 156 | waiver_khong_co_can_cu:dong_mien ×150, waiver_khong_co_can_cu:han ×6 |
| `a129_ten_job_lazy_qua_ho_so` | vi_tri=2 | 36 | 33 | 3 | danh_gia_khong_passed:dong_la ×3 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=0 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=1 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=2 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=3 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=4 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=5 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=6 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=7 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a131_ten_tep_co_Z` | (ca khong chia vi tri) | 1 | 1 | 0 | — |
| `a134_lop_dong_ten_tep_qua_ho_so` | vi_tri=thu_muc | 159 | 0 | 159 | tep_danh_gia_khong_hop_le ×159 |
| `a134_lop_dong_ten_tep_qua_ho_so` | vi_tri=run | 159 | 0 | 159 | duong_khong_tep_danh_gia ×149, tep_danh_gia_khong_hop_le ×10 |

| ca A | tong phan tu qua L8 |
|---|---:|
| `a124_token_ascii_qua_ho_so` | 1733 |
| `a125_ascii_dong_danh_gia` | 3840 |
| `a126_mien_ascii_qua_ho_so` | 52 |
| `a133_lop_dong_mien_qua_ho_so` | 1136 |
| `a129_ten_job_lazy_qua_ho_so` | 36 |
| `a132_ascii_khoa_landed_qua_ho_so` | 1280 |
| `a131_ten_tep_co_Z` | 1 |
| `a134_lop_dong_ten_tep_qua_ho_so` | 318 |
| **tong** | **8396** |

## `c25_b2_l8_ho_so_moi_duong_khong_tep_danh_gia`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | B2 lời khai dương chỉ trích kiem-gate | 1 | $.moc_gate_output: duong_khong_tep_danh_gia |
| 2 | đối chứng: not_measured không đòi gì | 0 | — |

## `c26_b6_l8_duong_khop_tep_danh_gia`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | B6 dương khớp tệp đánh giá và provenance | 0 | — |
| 2 | landed có lời khai dương hợp lệ | 0 | — |
| 3 | đối chứng: thiếu provenance của run | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:provenance_0 |

## `c27_b7_l8_landed_khong_loi_khai`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | landed {'trang_thai_packet': {'landed': True}} | 1 | $: landed_khong_loi_khai_gate_output |
| 2 | landed {'landed': True} | 1 | $: landed_khong_loi_khai_gate_output |
| 3 | landed {'trang_thai_packet': {'landed': False}, 'landed_20261124': {'landed': True}} | 1 | $: landed_khong_loi_khai_gate_output |
| 4 | landed {'trang_thai_packet': {'landed': 1}} | 1 | — |
| 5 | landed {'landed': 1} | 0 | — |
| 6 | landed {'landed_20261124': {'landed': 1}} | 0 | — |
| 7 | landed {'trang_thai_packet': {'landed': False}, 'landed': True} | 0 | — |
| 8 | landed {'trang_thai_packet': 'x', 'landed': True} | 0 | — |
| 9 | landed {'landed_2026112': {'landed': True}} | 0 | — |
| 10 | landed {'landed_20261124x': {'landed': True}} | 0 | — |
| 11 | landed {'xlanded_20261124': {'landed': True}} | 0 | — |
| 12 | landed {'landed_20261124': True} | 0 | — |
| 13 | landed {'trang_thai_packet': {'landed': False}} | 0 | — |
| 14 | landed + lời khai dương VI PHẠM: cả hai vi phạm | 1 | $.moc_gate_output: duong_khong_tep_danh_gia; $: landed_khong_loi_khai_gate_output |

## `c29_b3_l8_mien_tru_theo_ten_va_bam`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | bản sao NGUYÊN BYTE: được miễn L8 (rc 1 là của L1, bản sao không mang provenance) | 1 | — |
| 2 | B3 sửa một byte ⇒ mất miễn trừ, L8 áp | 1 | $: landed_khong_loi_khai_gate_output |

## `c30_b4_l8_module_khong_nap_duoc_la_khong_do_duoc`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | đối chứng: module CỦA GỐC ĐANG KIỂM được dùng (không phải bản cạnh bộ kiểm) | 1 | $: dau_rieng |

## `c31_b8_l8_chay_sau_chot_cutover`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | mất miễn trừ L5 (băm lệch) ⇒ kiểm đủ luật, gồm L8 | 1 | $.post_merge_checks[1].moc_gate_output: dinh_dang_loi_khai; $: landed_khong_loi_khai_gate_output |

## `c32_l8_ma_tran_token_va_khoa_qua_cong`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | lời khai 'passed — danh-gia-gate-output-44669622916.txt' | 0 | — |
| 2 | lời khai 'Measured: ./danh-gia-gate-output-44669622916.txt' | 0 | — |
| 3 | lời khai 'failed — khong trich tep' | 0 | — |
| 4 | lời khai 'failed — danh-gia-gate-output-44669622916.txt' | 1 | $.a[0].Gate-Output: danh_gia_khong_failed:danh-gia-gate-output-44669622916.txt:passed:- |
| 5 | lời khai 'measured — kiem-gate-output.txt' | 1 | $.a[0].Gate-Output: duong_khong_tep_danh_gia |
| 6 | lời khai 'passed — x/../danh-gia-gate-output-44669622916.txt' | 1 | $.a[0].Gate-Output: tep_danh_gia_khong_hop_le:x/../danh-gia-gate-output-44669622916.txt |
| 7 | lời khai 'passed — /danh-gia-gate-output-44669622916.txt' | 1 | $.a[0].Gate-Output: tep_danh_gia_khong_hop_le:/danh-gia-gate-output-44669622916.txt |
| 8 | lời khai 'passed — danh-gia-gate-output-44669622916.txt danh-gia-gate-output-1.txt' | 1 | $.a[0].Gate-Output: tep_danh_gia_khong_hop_le:danh-gia-gate-output-1.txt |
| 9 | lời khai 'owner_waived — khong co url' | 1 | $.a[0].Gate-Output: waiver_khong_co_can_cu:url |
| 10 | lời khai 5 | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 11 | lời khai None | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 12 | lời khai '' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 13 | lời khai 'da do' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 14 | lời khai 'pass' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 15 | lời khai 'not_run' | 0 | — |
| 16 | lời khai 'not_run x' | 0 | — |
| 17 | lời khai 'not_run\tx' | 0 | — |
| 18 | lời khai 'not_run—x' | 0 | — |
| 19 | lời khai 'not_run-x' | 0 | — |
| 20 | lời khai 'not_run:x' | 0 | — |
| 21 | lời khai 'not_run(x' | 0 | — |
| 22 | lời khai 'not_run,x' | 0 | — |
| 23 | lời khai 'not_run.x' | 0 | — |
| 24 | lời khai 'not_run;x' | 0 | — |
| 25 | lời khai 'not_run\n' | 0 | — |
| 26 | lời khai ' \tNOT_MEASURED' | 0 | — |
| 27 | lời khai ' \tNOT_MEASURED x' | 0 | — |
| 28 | lời khai ' \tNOT_MEASURED\tx' | 0 | — |
| 29 | lời khai ' \tNOT_MEASURED—x' | 0 | — |
| 30 | lời khai ' \tNOT_MEASURED-x' | 0 | — |
| 31 | lời khai ' \tNOT_MEASURED:x' | 0 | — |
| 32 | lời khai ' \tNOT_MEASURED(x' | 0 | — |
| 33 | lời khai ' \tNOT_MEASURED,x' | 0 | — |
| 34 | lời khai ' \tNOT_MEASURED.x' | 0 | — |
| 35 | lời khai ' \tNOT_MEASURED;x' | 0 | — |
| 36 | lời khai ' \tNOT_MEASURED\n' | 0 | — |
| 37 | lời khai 'skipped' | 0 | — |
| 38 | lời khai 'skipped x' | 0 | — |
| 39 | lời khai 'skipped\tx' | 0 | — |
| 40 | lời khai 'skipped—x' | 0 | — |
| 41 | lời khai 'skipped-x' | 0 | — |
| 42 | lời khai 'skipped:x' | 0 | — |
| 43 | lời khai 'skipped(x' | 0 | — |
| 44 | lời khai 'skipped,x' | 0 | — |
| 45 | lời khai 'skipped.x' | 0 | — |
| 46 | lời khai 'skipped;x' | 0 | — |
| 47 | lời khai 'skipped\n' | 0 | — |
| 48 | lời khai 'not_run1' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 49 | lời khai 'not_runx' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 50 | lời khai 'not_run_' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 51 | lời khai 'not_run!x' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 52 | lời khai 'not_run/x' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 53 | lời khai 'not_run=x' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 54 | lời khai 'not_run\nx' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 55 | lời khai 'not_run–x' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 56 | lời khai '\nnot_run' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 57 | lời khai 'x not_run' | 1 | $.a[0].Gate-Output: dinh_dang_loi_khai |
| 58 | khoá 'gate_output' | 1 | $.gate_output: dinh_dang_loi_khai |
| 59 | khoá 'MOC GATE-OUTPUT 2' | 1 | $.MOC GATE-OUTPUT 2: dinh_dang_loi_khai |
| 60 | khoá 'gate_out_put' | 1 | $.gate_out_put: dinh_dang_loi_khai |
| 61 | khoá 'gate_output_nguon2' | 1 | $.gate_output_nguon2: dinh_dang_loi_khai |
| 62 | khoá 'x_gate_output_nguon' | 1 | $.x_gate_output_nguon: dinh_dang_loi_khai |
| 63 | khoá 'gate_output_nguon' | 0 | — |
| 64 | khoá 'Gate-Output Nguon_va_gioi_han' | 0 | — |
| 65 | khoá 'moc_gate_output_rc_disposition' | 0 | — |
| 66 | khoá 'gate2output' | 0 | — |
| 67 | khoá 'gate_outpu' | 0 | — |

## `c34_l8_ma_tran_mien_qua_cong`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | miễn hợp lệ, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 0 | — |
| 2 | miễn hợp lệ, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 0 | — |
| 3 | miễn hợp lệ, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 0 | — |
| 4 | miễn hợp lệ, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 0 | — |
| 5 | miễn hợp lệ, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 0 | — |
| 6 | miễn hợp lệ, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 0 | — |
| 7 | miễn url, landed=False: 'ed — d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:url |
| 8 | miễn url, landed=True: 'ed — d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:url; $: landed_khong_loi_khai_gate_output |
| 9 | miễn url, landed=False: 'thangho/tra-luat/issues/1236#issuecomment-123' | 1 | $.gate_output: waiver_khong_co_can_cu:url |
| 10 | miễn url, landed=True: 'thangho/tra-luat/issues/1236#issuecomment-123' | 1 | $.gate_output: waiver_khong_co_can_cu:url; $: landed_khong_loi_khai_gate_output |
| 11 | miễn url, landed=False: 'hangho/tra-luat/issues/1236#issuecomment-1234' | 1 | $.gate_output: waiver_khong_co_can_cu:url |
| 12 | miễn url, landed=True: 'hangho/tra-luat/issues/1236#issuecomment-1234' | 1 | $.gate_output: waiver_khong_co_can_cu:url; $: landed_khong_loi_khai_gate_output |
| 13 | miễn readback, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:readback |
| 14 | miễn readback, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:readback; $: landed_khong_loi_khai_gate_output |
| 15 | miễn readback, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:readback |
| 16 | miễn readback, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:readback; $: landed_khong_loi_khai_gate_output |
| 17 | miễn doc_readback, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:doc_readback |
| 18 | miễn doc_readback, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:doc_readback; $: landed_khong_loi_khai_gate_output |
| 19 | miễn html_url, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:html_url |
| 20 | miễn html_url, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:html_url; $: landed_khong_loi_khai_gate_output |
| 21 | miễn html_url, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:html_url |
| 22 | miễn html_url, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:html_url; $: landed_khong_loi_khai_gate_output |
| 23 | miễn tac_gia, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:tac_gia |
| 24 | miễn tac_gia, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:tac_gia; $: landed_khong_loi_khai_gate_output |
| 25 | miễn tac_gia, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:tac_gia |
| 26 | miễn tac_gia, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:tac_gia; $: landed_khong_loi_khai_gate_output |
| 27 | miễn tac_gia, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:tac_gia |
| 28 | miễn tac_gia, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:tac_gia; $: landed_khong_loi_khai_gate_output |
| 29 | miễn dong_mien, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien |
| 30 | miễn dong_mien, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien; $: landed_khong_loi_khai_gate_output |
| 31 | miễn dong_mien, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien |
| 32 | miễn dong_mien, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien; $: landed_khong_loi_khai_gate_output |
| 33 | miễn dong_mien, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien |
| 34 | miễn dong_mien, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien; $: landed_khong_loi_khai_gate_output |
| 35 | miễn dong_mien, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien |
| 36 | miễn dong_mien, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien; $: landed_khong_loi_khai_gate_output |
| 37 | miễn dong_mien, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien |
| 38 | miễn dong_mien, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:dong_mien; $: landed_khong_loi_khai_gate_output |
| 39 | miễn han, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:han |
| 40 | miễn han, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:han; $: landed_khong_loi_khai_gate_output |
| 41 | miễn han, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:han |
| 42 | miễn han, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:han; $: landed_khong_loi_khai_gate_output |
| 43 | miễn os, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:os |
| 44 | miễn os, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:os; $: landed_khong_loi_khai_gate_output |
| 45 | miễn os, landed=False: 'thangho/tra-luat/issues/1236#issuecomment-123' | 1 | $.gate_output: waiver_khong_co_can_cu:os |
| 46 | miễn os, landed=True: 'thangho/tra-luat/issues/1236#issuecomment-123' | 1 | $.gate_output: waiver_khong_co_can_cu:os; $: landed_khong_loi_khai_gate_output |
| 47 | miễn sha, landed=False: 'thangho/tra-luat/issues/1236#issuecomment-123' | 1 | $.gate_output: waiver_khong_co_can_cu:sha |
| 48 | miễn sha, landed=True: 'thangho/tra-luat/issues/1236#issuecomment-123' | 1 | $.gate_output: waiver_khong_co_can_cu:sha; $: landed_khong_loi_khai_gate_output |
| 49 | miễn sha, landed=False: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:sha |
| 50 | miễn sha, landed=True: '-123 d8cf2ab57f9f25a93cefedcebfb315826b6b78fe' | 1 | $.gate_output: waiver_khong_co_can_cu:sha; $: landed_khong_loi_khai_gate_output |

## `c35_l8_ngu_phap_tep_danh_gia_qua_cong`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | tệp đánh giá 'T: passed (39/39 job co dau hieu duong)\n' | 0 | — |
| 2 | tệp đánh giá ': passed (39/39 job co dau hieu duong)\r\n' | 0 | — |
| 3 | tệp đánh giá ': [ops/ci_duong_nhanh.py] che_do=day_du\n' | 0 | — |
| 4 | tệp đánh giá '# Danh giá' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dau_tep_sai |
| 5 | tệp đánh giá '\n# Danh gia' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dau_tep_sai |
| 6 | tệp đánh giá ' attempt x' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dau_tep_sai |
| 7 | tệp đánh giá 's: [ops/ci_duong_nhanh.py] che_do=day_du' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la |
| 8 | tệp đánh giá 'd: [ops/ci_duong_nhanh.py] che_do=day_du' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la |
| 9 | tệp đánh giá 'd: [ops/ci_duong_nhanh.py] che_do=day_du' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la |
| 10 | tệp đánh giá 'd: [ops/ci_duong_nhanh.py] che_do=day_du' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:job_lap |
| 11 | tệp đánh giá 'nhanh.py] che_do=day_du\nJOB 1 x: skipped' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la |
| 12 | tệp đánh giá '_do=day_du\nJOB 1 x: skipped (khong tinh)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:tap_skip_lech,dong_skip_sai_phien_ban,moc_lech |
| 13 | tệp đánh giá 'skipped -> not_measured (khong suy pass)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:tap_skip_lech,moc_lech |
| 14 | tệp đánh giá 'PUT passed (39/39 job co dau hieu duong)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la,thieu_moc |
| 15 | tệp đánh giá '' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:thieu_moc |
| 16 | tệp đánh giá 'UT: passed (39/39 job co dau hieu duong)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:moc_lap |
| 17 | tệp đánh giá 'T: passed (39/39 jobs co dau hieu duong)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la,thieu_moc |
| 18 | tệp đánh giá ': [ops/ci_duong_nhanh.py] che_do=day_du\r' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:xuong_dong_tron |
| 19 | tệp đánh giá ' [ops/ci_duong_nhanh.py] che_do=day_du\rx' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:cr_le |
| 20 | tệp đánh giá có BYTE không phải UTF-8 | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:khong_phai_utf8 |
