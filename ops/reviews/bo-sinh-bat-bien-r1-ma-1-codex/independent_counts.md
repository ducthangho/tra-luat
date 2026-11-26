Suy độc lập từ mã tám ca tại HEAD (không dùng tổng của executor để tạo kỳ vọng):

| Ca | Nguồn từng số hạng | Biểu thức / kết quả |
|---|---|---|
| a124 | Vòng 1 có 3 kiem; miền 128 ASCII +31 đại diện +19 whitespace ngoài ASCII +em dash. Vòng 2 có 7 vị trí của skipped; 128 ASCII +31 đại diện; từ chu_va_so gặp lại 8 category L/N +1 supplementary Lu; thêm long s U+017F và Kelvin U+212A. Cuối hàm 6 hồ sơ rời. | 3*(128+19+1)+7*(128+9+2)+6 +10*31 =1733 |
| a125 | 11 trường có số vị trí {0,mid,last}: run2, attempt2, head3, bo_sinh3, job2, conclusion3, log3, skip_cu2, skip_v3 2, dat1, tong1; tổng24. Trừ 3 conclusion còn21 vị trí dùng Nd và gặp lại1 đại diện Nd; conclusion gặp lại9 đại diện L/N/supplementary. | 24*128+21+3*9 +24*30 =3840 |
| a126 | 7 do rời; chuỗi whitespace dài12; 2 ca hạn; vòng cuối thêm NUL và U+200B. Bộ sinh loại Zl/Zp bởi cam; còn29. | 7+12+2+2 +29 =52 |
| a129 | 6 lời gọi kiem cấu trúc trước vòng; vòng dùng cam CR LF và bo_loai Cs, 30 phần tử. | 6+30=36 |
| a131 | một kiem_ho_so với đường Z/. | 1 |
| a132 | 8 vị trí YYYYMMDD; mỗi vị trí128 ASCII+31 đại diện+1 Nd gặp lại trong chu_so_unicode. | 8*(128+1)+8*31=1280 |
| a133 | 7 trường; mỗi trường128 ASCII+31 đại diện; url_path/os dùng LN gặp lại9, 5 trường còn lại dùng Nd gặp lại1. | 7*128+2*9+5 +7*31=1136 |
| a134 | 2 vị trí thu_muc/run; vòng code point duy nhất, không nối miền nên không đếm lặp. Chỉ ASCII hoặc đại diện qua hồ sơ. | 2*128+2*31=318 |

Tổng 8396. Các số 30 category, miền31/30/29, ASCII128, vị trí cấu trúc là hằng. len(LOAI) đọc hằng chép từ đặc tả, không gọi bộ sinh đang kiểm. Chú thích a124 viết `ſK` thiếu glyph Kelvin U+212A nhưng biểu thức2 và code thực dùng `ſK` đúng; không suy K ASCII là một đại diện cộng thêm.

c37: 4 vị trí *158 +16 ô rời=648. 158=128+29 BMP(category trừ Cs)+1 supplementary. not lech chốt đúng multiplicity BMP; hai điều kiện cardinality chặn ASCII trùng, thiếu/thừa supplementary; CR/LF chỉ có trong ASCII. Hai bang ở dòng900/902 đều nằm trước dòng903 vòng ô.

kiem_bo_sinh: đúng5 bộ (cam,bo_loai); thứ tự count, missing categories, no BMP category duplicate, cam exclusion, >=U+0080, cuối supplementary duy nhất. Tính category không trùng trên phần BMP là phù hợp baseline: extra U+10400 tự lặp Lu nếu tính cả supplementary.
