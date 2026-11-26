# Bảng mệnh đề × toán tử — HEAD `485387fb1e0e6e49837623ba9df7843d5dca782f`

Baseline (bản nguyên vẹn, 4 ca phản chứng): XANH. Tổng 108 đột biến: GIET 104 · TUONG_DUONG 4 · SONG 0 · HONG 0. Bản sao sạch sau khi đo: True.

Ô: ca phản chứng giết (rc 3, `DO:<ca>:`) · `TĐ` = tương đương có lập luận · `SỐNG` · `HỎNG` · `—` = không áp dụng (lý do cuối tệp).

| Mệnh đề | bo | ge | le | ne | gt | lt | dao | cong1 | tru1 | or | yeu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c36.so_phan_tu  `dem[0] - truoc == mong` | c40 | c40 | c40 | c40 | — | — | — | c40 | c40 | c40 | — |
| c36.khac_nhau  `len(van_tay) == mong - lap` | c40 | c40 | c40 | c40 | — | — | — | c40 | c40 | — | — |
| c36.category  `not thieu` | c40 | — | — | — | — | — | c40 | — | — | — | c40 |
| c36.ngoai_bmp  `any(ord(c) > 0xFFFF ...)` | c40 | c40 | — | — | — | — | c40 | c40 | c40 | — | c40 |
| c36.cong_thuc  `... - len(tru or ()) + 1` | — | — | — | — | — | — | — | c40 | c40 | — | — |
| c37.tong  `len(vu_tru) == 158` | c39 | c39 | TĐ | c39 | — | — | — | c39 | c39 | c39 | — |
| c37.khac_nhau  `len(set(vu_tru)) == 158` | c39 | TĐ | c39 | c39 | — | — | — | c39 | c39 | c39 | — |
| c37.category  `not lech` | c39 | — | — | — | — | — | c39 | — | — | — | — |
| c37.lech  `bmp.count(loai) != (loai != "Cs")` | c39 | — | — | c39 | c39 | c39 | c39 | — | — | — | — |
| c37.bien_bmp  `ord(c) <= 0xFFFF` | c39 | — | — | — | — | — | c39 | c39 | c39 | — | — |
| c37.phan_bo_sinh  `vu_tru[128:]` | — | — | — | — | — | — | — | c39 | c39 | — | — |
| c37.so_o  `len(o) == 648` | c39 | c39 | c39 | c39 | — | — | — | c39 | c39 | — | — |
| nap_sua.neo  `nguon.count(cu) == 1` | c39 | c39 | c39 | c39 | — | — | — | c39 | c39 | — | — |
| a135.so_phan_tu  `len(ra) == so` | a136 | a136 | a136 | a136 | — | — | — | a136 | a136 | — | — |
| a135.category_vang  `sorted(...) == sorted(vang)` | a136 | a136 | a136 | a136 | — | — | — | — | — | — | a136 |
| a135.lap_category  `len(bmp) == len(set(bmp))` | a136 | a136 | TĐ | a136 | — | — | — | — | — | — | — |
| a135.thuoc_cam  `not any(c in cam ...)` | a136 | — | — | — | — | — | a136 | — | — | — | a136 |
| a135.tu_0080  `all(ord(c) >= 0x80 ...)` | a136 | a136 | — | — | — | — | a136 | a136 | a136 | — | a136 |
| a135.cuoi.khong_rong  `bool(ra)` | a136 | — | — | — | — | — | a136 | — | — | a136 | — |
| a135.cuoi.vi_tri  `ord(ra[-1]) > 0xFFFF` | a136 | a136 | — | — | — | — | a136 | a136 | a136 | a136 | — |
| a135.cuoi.duy_nhat  `len(ra) - len(bmp) == 1` | a136 | a136 | TĐ | a136 | — | — | — | a136 | a136 | — | — |
| a135.bien_bmp  `ord(c) <= 0xFFFF` | a136 | — | — | — | — | — | a136 | a136 | a136 | — | — |
| a135.gom  `if not dat` / `bang(not lech` | a136 | — | — | — | — | — | a136 | — | — | — | — |

## Từng đột biến

| Mệnh đề | Toán tử | Kết luận | Ca giết | rc | Văn bản thay | Dòng quan sát được |
|---|---|---|---|---|---|---|
| c36.so_phan_tu | bo | GIET | c40 | 3 | `bang(rc == 0,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A thêm một bản sao ô đầu (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.so_phan_tu | ge | GIET | c40 | 3 | `bang(rc == 0 and dem[0] - truoc >= mong,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A thêm một bản sao ô đầu (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.so_phan_tu | le | GIET | c40 | 3 | `bang(rc == 0 and dem[0] - truoc <= mong,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A bỏ Mn (a129) mà c36 không ĐỎ đúng chốt: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a129_ten_job_lazy_qua_ho_so qua main → L8: 35 phần tử KHÁC NHAU (đặc tả: đúng 36)` |
| c36.so_phan_tu | ne | GIET | c40 | 3 | `bang(rc == 0 and dem[0] - truoc != mong,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử (đặc tả: đúng 52), rc=0` |
| c36.so_phan_tu | cong1 | GIET | c40 | 3 | `bang(rc == 0 and dem[0] - truoc == mong + 1,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử (đặc tả: đúng 52), rc=0` |
| c36.so_phan_tu | tru1 | GIET | c40 | 3 | `bang(rc == 0 and dem[0] - truoc == mong - 1,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử (đặc tả: đúng 52), rc=0` |
| c36.so_phan_tu | or | GIET | c40 | 3 | `bang(rc == 0 or dem[0] - truoc == mong,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A thêm một bản sao ô đầu (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.khac_nhau | bo | GIET | c40 | 3 | `bang(True,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A Mn thành bản sao Mc (a126) mà c36 không ĐỎ đúng chốt: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: thiếu general category ['Mn']` |
| c36.khac_nhau | ge | GIET | c40 | 3 | `bang(len(van_tay) >= mong - lap,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn, kỳ vọng gặp lại +1 (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.khac_nhau | le | GIET | c40 | 3 | `bang(len(van_tay) <= mong - lap,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A Mn thành bản sao Mc (a126) mà c36 không ĐỎ đúng chốt: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: thiếu general category ['Mn']` |
| c36.khac_nhau | ne | GIET | c40 | 3 | `bang(len(van_tay) != mong - lap,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử KHÁC NHAU (đặc tả: đúng 52)` |
| c36.khac_nhau | cong1 | GIET | c40 | 3 | `bang(len(van_tay) == mong - lap + 1,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử KHÁC NHAU (đặc tả: đúng 52)` |
| c36.khac_nhau | tru1 | GIET | c40 | 3 | `bang(len(van_tay) == mong - lap - 1,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử KHÁC NHAU (đặc tả: đúng 52)` |
| c36.category | bo | GIET | c40 | 3 | `bang(True,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A Mn thành ký tự Mc KHÁC (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.category | dao | GIET | c40 | 3 | `bang(thieu,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: thiếu general category []` |
| c36.category | yeu | GIET | c40 | 3 | `bang(len(thieu) < len(set(LOAI) - set(tru)),` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A Mn thành ký tự Mc KHÁC (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.ngoai_bmp | bo | GIET | c40 | 3 | `bang(True,` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A ngoài BMP thành U+FFFF (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.ngoai_bmp | ge | GIET | c40 | 3 | `bang(any(ord(c) >= 0xFFFF for c in thay),` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A ngoài BMP thành U+FFFF (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.ngoai_bmp | dao | GIET | c40 | 3 | `bang(any(ord(c) <= 0xFFFF for c in thay),` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A ngoài BMP thành U+FFFF (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.ngoai_bmp | cong1 | GIET | c40 | 3 | `bang(any(ord(c) > 0x10000 for c in thay),` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A ngoài BMP thành U+10000 (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: không có ký tự ngoài BMP` |
| c36.ngoai_bmp | tru1 | GIET | c40 | 3 | `bang(any(ord(c) > 0xFFFE for c in thay),` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A ngoài BMP thành U+FFFF (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36.ngoai_bmp | yeu | GIET | c40 | 3 | `bang(all(ord(c) > 0xFFFF for c in thay),` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: không có ký tự ngoài BMP` |
| c36.cong_thuc | cong1 | GIET | c40 | 3 | `(len(LOAI) - len(tru or ()) + 2)` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử (đặc tả: đúng 53), rc=0` |
| c36.cong_thuc | tru1 | GIET | c40 | 3 | `(len(LOAI) - len(tru or ()) + 0)` | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A nguyên vẹn (a126) mà c36 không XANH: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: 52 phần tử (đặc tả: đúng 51), rc=0` |
| c37.tong | bo | GIET | c39 | 3 | `bang(len(set(vu_tru)) == 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:lặp CHÍNH ký tự ngoài BMP cuối mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 652 (đúng 648)` |
| c37.tong | ge | GIET | c39 | 3 | `bang(len(vu_tru) >= 158 and len(set(vu_tru)) == 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:lặp CHÍNH ký tự ngoài BMP cuối mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 652 (đúng 648)` |
| c37.tong | le | TUONG_DUONG |  | 0 | `bang(len(vu_tru) <= 158 and len(set(vu_tru)) == 158 and not lech,` | `` |
| c37.tong | ne | GIET | c39 | 3 | `bang(len(vu_tru) != 158 and len(set(vu_tru)) == 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.tong | cong1 | GIET | c39 | 3 | `bang(len(vu_tru) == 159 and len(set(vu_tru)) == 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.tong | tru1 | GIET | c39 | 3 | `bang(len(vu_tru) == 157 and len(set(vu_tru)) == 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.tong | or | GIET | c39 | 3 | `bang(len(vu_tru) == 158 or len(set(vu_tru)) == 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:lặp CHÍNH ký tự ngoài BMP cuối mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 652 (đúng 648)` |
| c37.khac_nhau | bo | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:Lu thành ASCII 'A' mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 648 ô,` |
| c37.khac_nhau | ge | TUONG_DUONG |  | 0 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) >= 158 and not lech,` | `` |
| c37.khac_nhau | le | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) <= 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:Lu thành ASCII 'A' mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 648 ô,` |
| c37.khac_nhau | ne | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) != 158 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.khac_nhau | cong1 | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) == 159 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.khac_nhau | tru1 | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) == 157 and not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.khac_nhau | or | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158 or not lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:bỏ ký tự ngoài BMP mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 644 (đúng 648)` |
| c37.category | bo | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:Mn thành ký tự Mc KHÁC mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 648 ô,` |
| c37.category | dao | GIET | c39 | 3 | `bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158 and lech,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.lech | ne | GIET | c39 | 3 | `lech = [loai for loai in LOAI if bmp.count(loai) == (loai != "Cs")]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Mn', 'Mc', 'Me', 'Nd', 'Nl', 'No', 'Pc', 'Pd', 'Ps', 'Pe', 'Pi'` |
| c37.lech | gt | GIET | c39 | 3 | `lech = [loai for loai in LOAI if bmp.count(loai) > (loai != "Cs")]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:bỏ Lu mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 157 ký tự (157 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.lech | lt | GIET | c39 | 3 | `lech = [loai for loai in LOAI if bmp.count(loai) < (loai != "Cs")]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:lặp category Ll mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 159 ký tự (159 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.lech | dao | GIET | c39 | 3 | `lech = [loai for loai in LOAI if bmp.count(loai) != (loai == "Cs")]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Mn', 'Mc', 'Me', 'Nd', 'Nl', 'No', 'Pc', 'Pd', 'Ps', 'Pe', 'Pi'` |
| c37.lech | bo | GIET | c39 | 3 | `lech = []` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:bỏ Lu mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 157 ký tự (157 khác nhau), category lệch [], 1 ngoài BMP` |
| c37.bien_bmp | cong1 | GIET | c39 | 3 | `bmp = [unicodedata.category(c) for c in ngoai if ord(c) <= 0x10000]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:ngoài BMP thành U+10000 mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch ['Lo'], 0 ngoài BMP` |
| c37.bien_bmp | tru1 | GIET | c39 | 3 | `bmp = [unicodedata.category(c) for c in ngoai if ord(c) <= 0xFFFE]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:ngoài BMP thành U+FFFF mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 648 ô,` |
| c37.bien_bmp | dao | GIET | c39 | 3 | `bmp = [unicodedata.category(c) for c in ngoai if ord(c) > 0xFFFF]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch ['Ll', 'Lt', 'Lm', 'Lo', 'Mn', 'Mc', 'Me', 'Nd', 'Nl', 'No', 'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf'` |
| c37.bien_bmp | bo | GIET | c39 | 3 | `bmp = [unicodedata.category(c) for c in ngoai]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch ['Lu'], 0 ngoài BMP` |
| c37.phan_bo_sinh | cong1 | GIET | c39 | 3 | `ngoai = vu_tru[129:]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch ['Cc'], 1 ngoài BMP` |
| c37.phan_bo_sinh | tru1 | GIET | c39 | 3 | `ngoai = vu_tru[127:]` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 158 ký tự (158 khác nhau), category lệch ['Cc'], 1 ngoài BMP` |
| c37.so_o | bo | GIET | c39 | 3 | `bang(True,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:c37 mất một ô rời mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 647 ô,` |
| c37.so_o | ge | GIET | c39 | 3 | `bang(len(o) >= 648,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:c37 thừa một ô rời mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 649 ô,` |
| c37.so_o | le | GIET | c39 | 3 | `bang(len(o) <= 648,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:c37 mất một ô rời mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 647 ô,` |
| c37.so_o | ne | GIET | c39 | 3 | `bang(len(o) != 648,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 648 (đúng 648)` |
| c37.so_o | cong1 | GIET | c39 | 3 | `bang(len(o) == 649,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 648 (đúng 648)` |
| c37.so_o | tru1 | GIET | c39 | 3 | `bang(len(o) == 647,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nguyên vẹn mà c37 không XANH với đúng 648 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 648 (đúng 648)` |
| nap_sua.neo | bo | GIET | c39 | 3 | `bang(True,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nap_sua nhận neo không xuất hiện đúng một lần: '\x00'` |
| nap_sua.neo | ge | GIET | c39 | 3 | `bang(nguon.count(cu) >= 1,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nap_sua nhận neo không xuất hiện đúng một lần: 'import '` |
| nap_sua.neo | le | GIET | c39 | 3 | `bang(nguon.count(cu) <= 1,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nap_sua nhận neo không xuất hiện đúng một lần: '\x00'` |
| nap_sua.neo | ne | GIET | c39 | 3 | `bang(nguon.count(cu) != 1,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nap_sua nhận neo không xuất hiện đúng một lần: '\x00'` |
| nap_sua.neo | cong1 | GIET | c39 | 3 | `bang(nguon.count(cu) == 2,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:neo sửa phải xuất hiện ĐÚNG MỘT lần trong land_evidence_nguon_test.py: 1 lần '("nhan", "", dung),'` |
| nap_sua.neo | tru1 | GIET | c39 | 3 | `bang(nguon.count(cu) == 0,` | `DO:c39_c37_do_khi_bo_sinh_lech_mien:nap_sua nhận neo không xuất hiện đúng một lần: '\x00'` |
| a135.so_phan_tu | bo | GIET | a136 | 3 | `("so_phan_tu", True)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang']` |
| a135.so_phan_tu | ge | GIET | a136 | 3 | `("so_phan_tu", len(ra) >= so)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo loc cam: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029 \t', ()) lệch đặc tả: ['category_vang', 'thuoc_cam']` |
| a135.so_phan_tu | le | GIET | a136 | 3 | `("so_phan_tu", len(ra) <= so)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang']` |
| a135.so_phan_tu | ne | GIET | a136 | 3 | `("so_phan_tu", len(ra) != so)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.so_phan_tu | cong1 | GIET | a136 | 3 | `("so_phan_tu", len(ra) == so + 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.so_phan_tu | tru1 | GIET | a136 | 3 | `("so_phan_tu", len(ra) == so - 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.category_vang | bo | GIET | a136 | 3 | `("category_vang", True)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.category_vang | ge | GIET | a136 | 3 | `("category_vang", sorted(set(LOAI_UNICODE) - set(bmp)) >= sorted(vang))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.category_vang | le | GIET | a136 | 3 | `("category_vang", sorted(set(LOAI_UNICODE) - set(bmp)) <= sorted(vang))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo loc cam: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029 \t', ()) lệch đặc tả: ['so_phan_tu', 'thuoc_cam']` |
| a135.category_vang | ne | GIET | a136 | 3 | `("category_vang", sorted(set(LOAI_UNICODE) - set(bmp)) != sorted(vang))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang']` |
| a135.category_vang | yeu | GIET | a136 | 3 | `("category_vang", set(vang) <= set(LOAI_UNICODE) - set(bmp))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.lap_category | bo | GIET | a136 | 3 | `("lap_category", True)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh Mn thanh ban sao Mc: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang']` |
| a135.lap_category | ge | GIET | a136 | 3 | `("lap_category", len(bmp) >= len(set(bmp)))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh Mn thanh ban sao Mc: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang']` |
| a135.lap_category | le | TUONG_DUONG |  | 0 | `("lap_category", len(bmp) <= len(set(bmp)))` | `` |
| a135.lap_category | ne | GIET | a136 | 3 | `("lap_category", len(bmp) != len(set(bmp)))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['lap_category']` |
| a135.thuoc_cam | bo | GIET | a136 | 3 | `("thuoc_cam", True)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo loc cam: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029 \t', ()) lệch đặc tả: ['so_phan_tu', 'category_vang']` |
| a135.thuoc_cam | dao | GIET | a136 | 3 | `("thuoc_cam", any(c in cam for c in ra))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['thuoc_cam']` |
| a135.thuoc_cam | yeu | GIET | a136 | 3 | `("thuoc_cam", not all(c in cam for c in ra))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo loc cam: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029 \t', ()) lệch đặc tả: ['so_phan_tu', 'category_vang']` |
| a135.tu_0080 | bo | GIET | a136 | 3 | `("tu_0080", True)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh Lu thanh ASCII: rc=0` |
| a135.tu_0080 | ge | GIET | a136 | 3 | `("tu_0080", all(ord(c) > 0x80 for c in ra))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['tu_0080']` |
| a135.tu_0080 | cong1 | GIET | a136 | 3 | `("tu_0080", all(ord(c) >= 0x81 for c in ra))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['tu_0080']` |
| a135.tu_0080 | tru1 | GIET | a136 | 3 | `("tu_0080", all(ord(c) >= 0x7F for c in ra))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh Lu thanh U+007F: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang', 'lap_category']` |
| a135.tu_0080 | yeu | GIET | a136 | 3 | `("tu_0080", any(ord(c) >= 0x80 for c in ra))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh Lu thanh ASCII: rc=0` |
| a135.tu_0080 | dao | GIET | a136 | 3 | `("tu_0080", all(ord(c) < 0x80 for c in ra))` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['tu_0080']` |
| a135.cuoi.khong_rong | bo | GIET | a136 | 3 | `("cuoi_ngoai_bmp", ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh rong: rc=4 HONG:a135_bo_sinh_dung_mien_dac_ta:IndexError: tuple index out of range` |
| a135.cuoi.khong_rong | dao | GIET | a136 | 3 | `("cuoi_ngoai_bmp", not ra and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['cuoi_ngoai_bmp']` |
| a135.cuoi.khong_rong | or | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) or ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo ngoai BMP: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.cuoi.vi_tri | bo | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh ngoai BMP len dau, cuoi la U+FFFF thay dai dien Cn: rc=0` |
| a135.cuoi.vi_tri | ge | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) >= 0xFFFF and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh ngoai BMP len dau, cuoi la U+FFFF thay dai dien Cn: rc=0` |
| a135.cuoi.vi_tri | dao | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) <= 0xFFFF and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['cuoi_ngoai_bmp']` |
| a135.cuoi.vi_tri | cong1 | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0x10000 and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh cuoi la U+10000: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['cuoi_ngoai_bmp']` |
| a135.cuoi.vi_tri | tru1 | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFE and len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh ngoai BMP len dau, cuoi la U+FFFF thay dai dien Cn: rc=0` |
| a135.cuoi.vi_tri | or | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF or len(ra) - len(bmp) == 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh thua mot ngoai BMP: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.cuoi.duy_nhat | bo | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh thua mot ngoai BMP: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.cuoi.duy_nhat | ge | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) >= 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh thua mot ngoai BMP: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135.cuoi.duy_nhat | le | TUONG_DUONG |  | 0 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) <= 1)` | `` |
| a135.cuoi.duy_nhat | ne | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) != 1)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['cuoi_ngoai_bmp']` |
| a135.cuoi.duy_nhat | cong1 | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) == 2)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['cuoi_ngoai_bmp']` |
| a135.cuoi.duy_nhat | tru1 | GIET | a136 | 3 | `("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) == 0)` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['cuoi_ngoai_bmp']` |
| a135.bien_bmp | cong1 | GIET | a136 | 3 | `bmp = [category(c) for c in ra if ord(c) <= 0x10000]` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh cuoi la U+10000: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['lap_category', 'cuoi_ngoai_bmp']` |
| a135.bien_bmp | tru1 | GIET | a136 | 3 | `bmp = [category(c) for c in ra if ord(c) <= 0xFFFE]` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh ngoai BMP len dau, cuoi la U+FFFF thay dai dien Cn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang', 'cuoi_ngoai_bmp']` |
| a135.bien_bmp | dao | GIET | a136 | 3 | `bmp = [category(c) for c in ra if ord(c) > 0xFFFF]` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang', 'cuoi_ngoai_bmp']` |
| a135.bien_bmp | bo | GIET | a136 | 3 | `bmp = [category(c) for c in ra]` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['lap_category', 'cuoi_ngoai_bmp']` |
| a135.gom | dao | GIET | a136 | 3 | `len(ra) - len(bmp) == 1)) if dat]` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh that: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu', 'category_vang', 'lap_category', 'thuoc_cam', 'tu_0080', 'cuoi_ngoai_bmp']` |
| a135.gom | bo | GIET | a136 | 3 | `len(ra) - len(bmp) == 1)) if False]` | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=0` |

## Lập luận tương đương

- **c37.tong / le**: len(set(x)) <= len(x) với mọi x. Vế kế bên đòi len(set(vu_tru)) == 158 nên len(vu_tru) >= 158; cộng `<= 158` ⇒ == 158. Cùng tập chấp nhận với bản gốc.
- **c37.khac_nhau / ge**: len(set(x)) <= len(x). Vế kế bên đòi len(vu_tru) == 158 nên len(set(vu_tru)) <= 158; cộng `>= 158` ⇒ == 158. Cùng tập chấp nhận với bản gốc.
- **a135.lap_category / le**: len(bmp) >= len(set(bmp)) luôn đúng, nên `len(bmp) <= len(set(bmp))` ⇔ `==`.
- **a135.cuoi.duy_nhat / le**: vế trước đòi ord(ra[-1]) > 0xFFFF, tức phần tử cuối KHÔNG thuộc bmp, nên len(ra) - len(bmp) >= 1; cộng `<= 1` ⇒ == 1.

## Không áp dụng

- **ge/le/ne**: chỉ áp cho mệnh đề có phép so == / != / > / >=; mệnh đề dạng `not X`, `any(...)`, `all(...)` thì dùng dao / yeu
- **gt/lt**: chỉ áp cho phép so != (đổi thành một chiều)
- **dao**: chỉ áp cho mệnh đề có `not` hoặc có phép so đảo được mà chưa nằm trong ge/le/ne
- **cong1/tru1**: chỉ áp cho mệnh đề có hằng số
- **or**: chỉ áp cho mệnh đề là một vế của phép `and`; vế cuối của chuỗi `and` dùng chung ô `or` với vế đứng trước nó
- **yeu**: chỉ áp cho lượng từ all/any và quan hệ chứa
