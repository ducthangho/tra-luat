# Ledger MIEN / VI TRI -> o qua consumer L8 (`main` -> L8), do tren ma nguyen ven

Tong: 810 o cua cac bang dot B (ky8) + 8396 phan tu cua bang IMPORT tu bo test dot A (c36). Tat ca DAT (moi o/phan tu da qua phep so cua chinh ca: rc va DUNG danh sach dong L8 voi ky vong viet tu dac ta).

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
| `c35_l8_ngu_phap_tep_danh_gia_qua_cong` | 22 | 3 | 19 |
| `c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong` | 648 | 0 | 648 |

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
| `a129_ten_job_lazy_qua_ho_so` | vi_tri=2 | 36 | 33 | 3 | danh_gia_khong_passed:dong_la ×3 |
| `a131_ten_tep_co_Z` | (ca khong chia vi tri) | 1 | 1 | 0 | — |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=0 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=1 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=2 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=3 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=4 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=5 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=6 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a132_ascii_khoa_landed_qua_ho_so` | vi_tri=7 | 160 | 150 | 10 | landed_khong_loi_khai_gate_output ×10 |
| `a133_lop_dong_mien_qua_ho_so` | truong=url_path | 168 | 68 | 100 | waiver_khong_co_can_cu:url ×100 |
| `a133_lop_dong_mien_qua_ho_so` | truong=url_id | 160 | 1 | 159 | waiver_khong_co_can_cu:readback ×9, waiver_khong_co_can_cu:url ×150 |
| `a133_lop_dong_mien_qua_ho_so` | truong=sha | 160 | 1 | 159 | waiver_khong_co_can_cu:dong_mien ×144, waiver_khong_co_can_cu:sha ×15 |
| `a133_lop_dong_mien_qua_ho_so` | truong=os | 168 | 39 | 129 | waiver_khong_co_can_cu:dong_mien ×129 |
| `a133_lop_dong_mien_qua_ho_so` | truong=nam | 160 | 10 | 150 | waiver_khong_co_can_cu:dong_mien ×150 |
| `a133_lop_dong_mien_qua_ho_so` | truong=thang | 160 | 1 | 159 | waiver_khong_co_can_cu:dong_mien ×150, waiver_khong_co_can_cu:han ×9 |
| `a133_lop_dong_mien_qua_ho_so` | truong=ngay | 160 | 4 | 156 | waiver_khong_co_can_cu:dong_mien ×150, waiver_khong_co_can_cu:han ×6 |
| `a134_lop_dong_ten_tep_qua_ho_so` | vi_tri=thu_muc | 159 | 0 | 159 | tep_danh_gia_khong_hop_le ×159 |
| `a134_lop_dong_ten_tep_qua_ho_so` | vi_tri=run | 159 | 0 | 159 | duong_khong_tep_danh_gia ×149, tep_danh_gia_khong_hop_le ×10 |

## c37 — ba vi tri VAN BAN TU DO cua tep danh gia (bang cua dot B, tep mau mang bam bo sinh gia)

Doc: ly do bo_sinh_la = DUNG ngu phap (duong); ly do khac = SAI ngu phap (am).

| vi tri | so o | duong (bo_sinh_la) | am | ly do am (dem) |
|---|---:|---:|---:|---|
| vung tu do cua dong dau | 160 | 158 | 2 | cr_le ×1, dau_tep_sai ×1 |
| nhan cua dong job | 162 | 158 | 4 | cr_le ×1, dong_la ×3 |
| ten dong skipped dang cu | 163 | 160 | 3 | cr_le ×1, dong_la ×2 |
| ten dong skipped dang v3 | 163 | 160 | 3 | cr_le ×1, dong_la ×2 |

| ca A | tong phan tu qua L8 |
|---|---:|
| `a124_token_ascii_qua_ho_so` | 1733 |
| `a125_ascii_dong_danh_gia` | 3840 |
| `a126_mien_ascii_qua_ho_so` | 52 |
| `a129_ten_job_lazy_qua_ho_so` | 36 |
| `a131_ten_tep_co_Z` | 1 |
| `a132_ascii_khoa_landed_qua_ho_so` | 1280 |
| `a133_lop_dong_mien_qua_ho_so` | 1136 |
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
| 14 | tệp đánh giá 'o=day_du\nJOB 1 x: skipped (khong tinh) x' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la |
| 15 | tệp đánh giá 'ipped -> not_measured (khong suy pass) x' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la |
| 16 | tệp đánh giá 'PUT passed (39/39 job co dau hieu duong)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la,thieu_moc |
| 17 | tệp đánh giá '' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:thieu_moc |
| 18 | tệp đánh giá 'UT: passed (39/39 job co dau hieu duong)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:moc_lap |
| 19 | tệp đánh giá 'T: passed (39/39 jobs co dau hieu duong)' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:dong_la,thieu_moc |
| 20 | tệp đánh giá ': [ops/ci_duong_nhanh.py] che_do=day_du\r' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:xuong_dong_tron |
| 21 | tệp đánh giá ' [ops/ci_duong_nhanh.py] che_do=day_du\rx' | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:cr_le |
| 22 | tệp đánh giá có BYTE không phải UTF-8 | 1 | $.moc_gate_output: danh_gia_khong_passed:danh-gia-gate-output-44669622916.txt:not_measured:khong_phai_utf8 |

## `c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong`

| # | o | rc | dong L8 thuc do |
|---:|---|---:|---|
| 1 | dau '\x00' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 2 | dau '\x01' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 3 | dau '\x02' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 4 | dau '\x03' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 5 | dau '\x04' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 6 | dau '\x05' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 7 | dau '\x06' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 8 | dau '\x07' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 9 | dau '\x08' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 10 | dau '\t' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 11 | dau '\n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dau_tep_sai |
| 12 | dau '\x0b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 13 | dau '\x0c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 14 | dau '\r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:cr_le |
| 15 | dau '\x0e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 16 | dau '\x0f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 17 | dau '\x10' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 18 | dau '\x11' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 19 | dau '\x12' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 20 | dau '\x13' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 21 | dau '\x14' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 22 | dau '\x15' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 23 | dau '\x16' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 24 | dau '\x17' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 25 | dau '\x18' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 26 | dau '\x19' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 27 | dau '\x1a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 28 | dau '\x1b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 29 | dau '\x1c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 30 | dau '\x1d' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 31 | dau '\x1e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 32 | dau '\x1f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 33 | dau ' ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 34 | dau '!' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 35 | dau '"' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 36 | dau '#' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 37 | dau '$' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 38 | dau '%' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 39 | dau '&' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 40 | dau "'" | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 41 | dau '(' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 42 | dau ')' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 43 | dau '*' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 44 | dau '+' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 45 | dau ',' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 46 | dau '-' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 47 | dau '.' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 48 | dau '/' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 49 | dau '0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 50 | dau '1' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 51 | dau '2' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 52 | dau '3' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 53 | dau '4' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 54 | dau '5' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 55 | dau '6' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 56 | dau '7' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 57 | dau '8' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 58 | dau '9' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 59 | dau ':' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 60 | dau ';' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 61 | dau '<' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 62 | dau '=' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 63 | dau '>' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 64 | dau '?' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 65 | dau '@' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 66 | dau 'A' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 67 | dau 'B' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 68 | dau 'C' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 69 | dau 'D' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 70 | dau 'E' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 71 | dau 'F' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 72 | dau 'G' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 73 | dau 'H' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 74 | dau 'I' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 75 | dau 'J' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 76 | dau 'K' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 77 | dau 'L' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 78 | dau 'M' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 79 | dau 'N' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 80 | dau 'O' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 81 | dau 'P' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 82 | dau 'Q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 83 | dau 'R' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 84 | dau 'S' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 85 | dau 'T' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 86 | dau 'U' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 87 | dau 'V' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 88 | dau 'W' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 89 | dau 'X' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 90 | dau 'Y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 91 | dau 'Z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 92 | dau '[' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 93 | dau '\\' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 94 | dau ']' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 95 | dau '^' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 96 | dau '_' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 97 | dau '`' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 98 | dau 'a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 99 | dau 'b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 100 | dau 'c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 101 | dau 'd' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 102 | dau 'e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 103 | dau 'f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 104 | dau 'g' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 105 | dau 'h' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 106 | dau 'i' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 107 | dau 'j' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 108 | dau 'k' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 109 | dau 'l' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 110 | dau 'm' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 111 | dau 'n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 112 | dau 'o' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 113 | dau 'p' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 114 | dau 'q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 115 | dau 'r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 116 | dau 's' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 117 | dau 't' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 118 | dau 'u' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 119 | dau 'v' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 120 | dau 'w' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 121 | dau 'x' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 122 | dau 'y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 123 | dau 'z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 124 | dau '{' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 125 | dau '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 126 | dau '}' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 127 | dau '~' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 128 | dau '\x7f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 129 | dau '\x80' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 130 | dau '\xa0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 131 | dau '¡' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 132 | dau '¢' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 133 | dau '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 134 | dau '¨' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 135 | dau 'ª' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 136 | dau '«' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 137 | dau '¬' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 138 | dau '\xad' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 139 | dau '²' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 140 | dau 'µ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 141 | dau '»' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 142 | dau 'À' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 143 | dau 'ǅ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 144 | dau 'ʰ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 145 | dau '̀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 146 | dau '\u0378' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 147 | dau '҈' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 148 | dau '֊' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 149 | dau '٠' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 150 | dau 'ः' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 151 | dau '༺' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 152 | dau '༻' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 153 | dau 'ᛮ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 154 | dau '\u2028' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 155 | dau '\u2029' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 156 | dau '‿' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 157 | dau '\ue000' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 158 | dau '𐐀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 159 | nhan '\x00' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 160 | nhan '\x01' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 161 | nhan '\x02' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 162 | nhan '\x03' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 163 | nhan '\x04' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 164 | nhan '\x05' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 165 | nhan '\x06' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 166 | nhan '\x07' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 167 | nhan '\x08' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 168 | nhan '\t' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 169 | nhan '\n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dong_la |
| 170 | nhan '\x0b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 171 | nhan '\x0c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 172 | nhan '\r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:cr_le |
| 173 | nhan '\x0e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 174 | nhan '\x0f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 175 | nhan '\x10' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 176 | nhan '\x11' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 177 | nhan '\x12' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 178 | nhan '\x13' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 179 | nhan '\x14' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 180 | nhan '\x15' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 181 | nhan '\x16' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 182 | nhan '\x17' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 183 | nhan '\x18' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 184 | nhan '\x19' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 185 | nhan '\x1a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 186 | nhan '\x1b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 187 | nhan '\x1c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 188 | nhan '\x1d' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 189 | nhan '\x1e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 190 | nhan '\x1f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 191 | nhan ' ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 192 | nhan '!' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 193 | nhan '"' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 194 | nhan '#' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 195 | nhan '$' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 196 | nhan '%' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 197 | nhan '&' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 198 | nhan "'" | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 199 | nhan '(' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 200 | nhan ')' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 201 | nhan '*' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 202 | nhan '+' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 203 | nhan ',' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 204 | nhan '-' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 205 | nhan '.' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 206 | nhan '/' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 207 | nhan '0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 208 | nhan '1' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 209 | nhan '2' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 210 | nhan '3' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 211 | nhan '4' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 212 | nhan '5' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 213 | nhan '6' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 214 | nhan '7' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 215 | nhan '8' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 216 | nhan '9' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 217 | nhan ':' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 218 | nhan ';' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 219 | nhan '<' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 220 | nhan '=' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 221 | nhan '>' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 222 | nhan '?' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 223 | nhan '@' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 224 | nhan 'A' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 225 | nhan 'B' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 226 | nhan 'C' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 227 | nhan 'D' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 228 | nhan 'E' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 229 | nhan 'F' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 230 | nhan 'G' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 231 | nhan 'H' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 232 | nhan 'I' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 233 | nhan 'J' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 234 | nhan 'K' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 235 | nhan 'L' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 236 | nhan 'M' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 237 | nhan 'N' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 238 | nhan 'O' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 239 | nhan 'P' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 240 | nhan 'Q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 241 | nhan 'R' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 242 | nhan 'S' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 243 | nhan 'T' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 244 | nhan 'U' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 245 | nhan 'V' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 246 | nhan 'W' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 247 | nhan 'X' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 248 | nhan 'Y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 249 | nhan 'Z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 250 | nhan '[' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 251 | nhan '\\' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 252 | nhan ']' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dong_la |
| 253 | nhan '^' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 254 | nhan '_' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 255 | nhan '`' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 256 | nhan 'a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 257 | nhan 'b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 258 | nhan 'c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 259 | nhan 'd' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 260 | nhan 'e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 261 | nhan 'f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 262 | nhan 'g' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 263 | nhan 'h' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 264 | nhan 'i' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 265 | nhan 'j' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 266 | nhan 'k' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 267 | nhan 'l' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 268 | nhan 'm' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 269 | nhan 'n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 270 | nhan 'o' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 271 | nhan 'p' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 272 | nhan 'q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 273 | nhan 'r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 274 | nhan 's' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 275 | nhan 't' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 276 | nhan 'u' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 277 | nhan 'v' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 278 | nhan 'w' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 279 | nhan 'x' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 280 | nhan 'y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 281 | nhan 'z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 282 | nhan '{' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 283 | nhan '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 284 | nhan '}' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 285 | nhan '~' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 286 | nhan '\x7f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 287 | nhan '\x80' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 288 | nhan '\xa0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 289 | nhan '¡' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 290 | nhan '¢' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 291 | nhan '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 292 | nhan '¨' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 293 | nhan 'ª' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 294 | nhan '«' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 295 | nhan '¬' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 296 | nhan '\xad' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 297 | nhan '²' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 298 | nhan 'µ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 299 | nhan '»' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 300 | nhan 'À' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 301 | nhan 'ǅ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 302 | nhan 'ʰ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 303 | nhan '̀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 304 | nhan '\u0378' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 305 | nhan '҈' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 306 | nhan '֊' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 307 | nhan '٠' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 308 | nhan 'ः' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 309 | nhan '༺' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 310 | nhan '༻' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 311 | nhan 'ᛮ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 312 | nhan '\u2028' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 313 | nhan '\u2029' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 314 | nhan '‿' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 315 | nhan '\ue000' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 316 | nhan '𐐀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 317 | cu '\x00' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 318 | cu '\x01' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 319 | cu '\x02' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 320 | cu '\x03' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 321 | cu '\x04' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 322 | cu '\x05' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 323 | cu '\x06' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 324 | cu '\x07' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 325 | cu '\x08' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 326 | cu '\t' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 327 | cu '\n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dong_la |
| 328 | cu '\x0b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 329 | cu '\x0c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 330 | cu '\r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:cr_le |
| 331 | cu '\x0e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 332 | cu '\x0f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 333 | cu '\x10' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 334 | cu '\x11' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 335 | cu '\x12' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 336 | cu '\x13' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 337 | cu '\x14' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 338 | cu '\x15' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 339 | cu '\x16' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 340 | cu '\x17' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 341 | cu '\x18' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 342 | cu '\x19' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 343 | cu '\x1a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 344 | cu '\x1b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 345 | cu '\x1c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 346 | cu '\x1d' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 347 | cu '\x1e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 348 | cu '\x1f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 349 | cu ' ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 350 | cu '!' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 351 | cu '"' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 352 | cu '#' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 353 | cu '$' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 354 | cu '%' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 355 | cu '&' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 356 | cu "'" | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 357 | cu '(' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 358 | cu ')' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 359 | cu '*' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 360 | cu '+' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 361 | cu ',' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 362 | cu '-' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 363 | cu '.' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 364 | cu '/' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 365 | cu '0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 366 | cu '1' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 367 | cu '2' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 368 | cu '3' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 369 | cu '4' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 370 | cu '5' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 371 | cu '6' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 372 | cu '7' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 373 | cu '8' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 374 | cu '9' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 375 | cu ':' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 376 | cu ';' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 377 | cu '<' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 378 | cu '=' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 379 | cu '>' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 380 | cu '?' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 381 | cu '@' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 382 | cu 'A' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 383 | cu 'B' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 384 | cu 'C' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 385 | cu 'D' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 386 | cu 'E' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 387 | cu 'F' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 388 | cu 'G' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 389 | cu 'H' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 390 | cu 'I' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 391 | cu 'J' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 392 | cu 'K' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 393 | cu 'L' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 394 | cu 'M' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 395 | cu 'N' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 396 | cu 'O' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 397 | cu 'P' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 398 | cu 'Q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 399 | cu 'R' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 400 | cu 'S' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 401 | cu 'T' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 402 | cu 'U' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 403 | cu 'V' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 404 | cu 'W' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 405 | cu 'X' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 406 | cu 'Y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 407 | cu 'Z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 408 | cu '[' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 409 | cu '\\' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 410 | cu ']' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 411 | cu '^' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 412 | cu '_' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 413 | cu '`' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 414 | cu 'a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 415 | cu 'b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 416 | cu 'c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 417 | cu 'd' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 418 | cu 'e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 419 | cu 'f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 420 | cu 'g' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 421 | cu 'h' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 422 | cu 'i' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 423 | cu 'j' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 424 | cu 'k' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 425 | cu 'l' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 426 | cu 'm' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 427 | cu 'n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 428 | cu 'o' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 429 | cu 'p' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 430 | cu 'q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 431 | cu 'r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 432 | cu 's' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 433 | cu 't' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 434 | cu 'u' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 435 | cu 'v' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 436 | cu 'w' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 437 | cu 'x' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 438 | cu 'y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 439 | cu 'z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 440 | cu '{' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 441 | cu '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 442 | cu '}' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 443 | cu '~' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 444 | cu '\x7f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 445 | cu '\x80' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 446 | cu '\xa0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 447 | cu '¡' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 448 | cu '¢' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 449 | cu '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 450 | cu '¨' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 451 | cu 'ª' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 452 | cu '«' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 453 | cu '¬' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 454 | cu '\xad' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 455 | cu '²' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 456 | cu 'µ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 457 | cu '»' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 458 | cu 'À' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 459 | cu 'ǅ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 460 | cu 'ʰ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 461 | cu '̀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 462 | cu '\u0378' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 463 | cu '҈' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 464 | cu '֊' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 465 | cu '٠' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 466 | cu 'ः' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 467 | cu '༺' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 468 | cu '༻' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 469 | cu 'ᛮ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 470 | cu '\u2028' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 471 | cu '\u2029' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 472 | cu '‿' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 473 | cu '\ue000' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 474 | cu '𐐀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 475 | v3 '\x00' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 476 | v3 '\x01' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 477 | v3 '\x02' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 478 | v3 '\x03' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 479 | v3 '\x04' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 480 | v3 '\x05' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 481 | v3 '\x06' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 482 | v3 '\x07' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 483 | v3 '\x08' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 484 | v3 '\t' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 485 | v3 '\n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dong_la |
| 486 | v3 '\x0b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 487 | v3 '\x0c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 488 | v3 '\r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:cr_le |
| 489 | v3 '\x0e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 490 | v3 '\x0f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 491 | v3 '\x10' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 492 | v3 '\x11' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 493 | v3 '\x12' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 494 | v3 '\x13' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 495 | v3 '\x14' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 496 | v3 '\x15' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 497 | v3 '\x16' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 498 | v3 '\x17' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 499 | v3 '\x18' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 500 | v3 '\x19' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 501 | v3 '\x1a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 502 | v3 '\x1b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 503 | v3 '\x1c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 504 | v3 '\x1d' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 505 | v3 '\x1e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 506 | v3 '\x1f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 507 | v3 ' ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 508 | v3 '!' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 509 | v3 '"' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 510 | v3 '#' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 511 | v3 '$' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 512 | v3 '%' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 513 | v3 '&' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 514 | v3 "'" | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 515 | v3 '(' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 516 | v3 ')' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 517 | v3 '*' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 518 | v3 '+' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 519 | v3 ',' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 520 | v3 '-' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 521 | v3 '.' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 522 | v3 '/' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 523 | v3 '0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 524 | v3 '1' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 525 | v3 '2' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 526 | v3 '3' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 527 | v3 '4' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 528 | v3 '5' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 529 | v3 '6' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 530 | v3 '7' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 531 | v3 '8' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 532 | v3 '9' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 533 | v3 ':' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 534 | v3 ';' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 535 | v3 '<' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 536 | v3 '=' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 537 | v3 '>' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 538 | v3 '?' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 539 | v3 '@' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 540 | v3 'A' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 541 | v3 'B' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 542 | v3 'C' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 543 | v3 'D' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 544 | v3 'E' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 545 | v3 'F' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 546 | v3 'G' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 547 | v3 'H' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 548 | v3 'I' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 549 | v3 'J' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 550 | v3 'K' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 551 | v3 'L' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 552 | v3 'M' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 553 | v3 'N' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 554 | v3 'O' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 555 | v3 'P' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 556 | v3 'Q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 557 | v3 'R' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 558 | v3 'S' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 559 | v3 'T' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 560 | v3 'U' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 561 | v3 'V' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 562 | v3 'W' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 563 | v3 'X' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 564 | v3 'Y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 565 | v3 'Z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 566 | v3 '[' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 567 | v3 '\\' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 568 | v3 ']' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 569 | v3 '^' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 570 | v3 '_' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 571 | v3 '`' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 572 | v3 'a' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 573 | v3 'b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 574 | v3 'c' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 575 | v3 'd' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 576 | v3 'e' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 577 | v3 'f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 578 | v3 'g' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 579 | v3 'h' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 580 | v3 'i' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 581 | v3 'j' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 582 | v3 'k' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 583 | v3 'l' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 584 | v3 'm' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 585 | v3 'n' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 586 | v3 'o' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 587 | v3 'p' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 588 | v3 'q' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 589 | v3 'r' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 590 | v3 's' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 591 | v3 't' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 592 | v3 'u' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 593 | v3 'v' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 594 | v3 'w' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 595 | v3 'x' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 596 | v3 'y' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 597 | v3 'z' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 598 | v3 '{' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 599 | v3 '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 600 | v3 '}' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 601 | v3 '~' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 602 | v3 '\x7f' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 603 | v3 '\x80' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 604 | v3 '\xa0' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 605 | v3 '¡' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 606 | v3 '¢' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 607 | v3 '¦' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 608 | v3 '¨' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 609 | v3 'ª' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 610 | v3 '«' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 611 | v3 '¬' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 612 | v3 '\xad' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 613 | v3 '²' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 614 | v3 'µ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 615 | v3 '»' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 616 | v3 'À' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 617 | v3 'ǅ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 618 | v3 'ʰ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 619 | v3 '̀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 620 | v3 '\u0378' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 621 | v3 '҈' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 622 | v3 '֊' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 623 | v3 '٠' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 624 | v3 'ः' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 625 | v3 '༺' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 626 | v3 '༻' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 627 | v3 'ᛮ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 628 | v3 '\u2028' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 629 | v3 '\u2029' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 630 | v3 '‿' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 631 | v3 '\ue000' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 632 | v3 '𐐀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 633 | dau 'x (danh_gia_gate.py sha256 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb) ' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 634 | dau 'café 𐐀 ) (' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 635 | nhan '' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 636 | nhan 'ubuntu-latest, x y [' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 637 | nhan 'a]b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dong_la |
| 638 | nhan 'a] [b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 639 | cu '' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dong_la |
| 640 | v3 '' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:dong_la |
| 641 | cu 'a: skipped (khong tinh) b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 642 | cu 'a: skipped -> not_measured (khong suy pass) b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 643 | cu 'a: skipped (khong tinh)' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 644 | cu 'café 𐐀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 645 | v3 'a: skipped -> not_measured (khong suy pass) b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 646 | v3 'a: skipped (khong tinh) b' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 647 | v3 'a: skipped -> not_measured (khong suy pass)' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
| 648 | v3 'café 𐐀' | 1 | $.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:bo_sinh_la |
