# Suy độc lập số phần tử gặp lại — HEAD ef82ed9

Đọc trực tiếp tám hàm của test A; không lấy tổng executor làm kỳ vọng. `lap` là số lần xuất hiện trừ số hồ sơ/provenance khác nhau, không phải số nhóm có lặp.

| Ca | Số phần tử qua L8 | Phân rã số gặp lại | Khác nhau |
|---|---:|---|---:|
| a124 | 3*(128+19+1)+7*(128+9+2)+6+10*31 = 1733 | 3*3 + 7*9 + 6 + 6 = **84** | 1649 |
| a125 | 24*128+21+3*9+24*30 = 3840 | 21 + 3*9 + 23 = **71** | 3769 |
| a126 | 7+12+2+2+29 = 52 | **0** | 52 |
| a129 | 6+30 = 36 | **0** | 36 |
| a131 | 1 | **0** | 1 |
| a132 | 8*(128+1)+8*31 = 1280 | 8 + 7 = **15** | 1265 |
| a133 | 7*128+2*9+5+7*31 = 1136 | 2*9 + 5 + 5 = **28** | 1108 |
| a134 | 2*128+2*31 = 318 | **0** | 318 |

- **a124:** vòng thứ nhất có ba dạng chuỗi; trong 19 khoảng trắng ngoài ASCII, đúng ba đại diện Zs/Zl/Zp đã nằm trong `dai_dien`, tạo 3*3 lần gặp lại. Vòng thứ hai có bảy vị trí của `skipped`; tập chữ/số gặp lại tám đại diện BMP L*/N* cộng U+10400, tạo 7*9. Ký tự ASCII gốc ở mỗi vị trí cho lại `skipped` bảy lần, dư sáu. Sáu ô cuối đều đã xuất hiện: `ſkipped` (vòng thay ký tự), `skipped\n`, `skipped\u0085`, `\u00a0skipped`, `skipped\nx`, `skipped\u2003x` (vòng ba dạng). Không thêm trùng giữa dạng prefix, suffix có x và suffix trống.
- **a125:** 11 trường có số vị trí `{0, giữa, cuối}` là 2,2,3,3,2,3,3,2,2,1,1 = 24. Trừ ba vị trí conclusion còn 21, mỗi vị trí gặp lại một đại diện Nd. Ba vị trí conclusion gặp lại chín đại diện L/N kể cả ngoài BMP. Ở mỗi vị trí có đúng một ký tự ASCII giữ nguyên cả tệp: 24 bản gốc cùng hồ sơ/provenance, dư 23. Những thay đổi không phải ký tự gốc nằm ở vị trí khác nhau nên không đồng nhất byte.
- **a126:** bảy ô rời khác nhau; 12 whitespace được đưa vào lý do, không có trong miền helper vì nằm trong `cam`; hai ô `han` khác chúng; miền helper có 29 ký tự và thêm NUL/U+200B, hai ký tự này khác đại diện Cc U+0080/Cf U+00AD. Tổng 52 bộ byte khác nhau.
- **a129:** sáu lời gọi cấu trúc cho sáu bộ byte khác nhau; 30 phần tử helper chèn ký tự ngoài ASCII vào đầu tên và cuối dòng, không trùng các ô cấu trúc hoặc nhau. Hồ sơ YAML giống nhau ở nhiều ô nhưng provenance khác: phải tính cả hai.
- **a131:** một phần tử duy nhất.
- **a132:** tám vị trí của `20261120`. Mỗi vị trí gặp lại Nd giữa helper và `chu_so_unicode`, dư tám. Ký tự gốc từng vị trí cho cùng khoá `landed_20261120` tám lần, dư bảy. Các lần thay khác vị trí còn lại khác khoá.
- **a133:** hai trường url_path/os dùng miền L/N nên mỗi trường gặp lại chín đại diện; năm trường url_id/sha/nam/thang/ngay dùng Nd, mỗi trường gặp lại một. Sáu trường trừ os có đúng một ASCII tái tạo cặp URL/dòng gốc, dư năm. os luôn thêm `,{c}x`, không có ô gốc và không trùng trường khác.
- **a134:** một lần duyệt code point cho mỗi trong hai vị trí; không nối hai miền nên không gặp lại đại diện. Chuỗi thư mục `x{c}x/…` và run `…-{c}23.txt` khác nhau.

Tổng 8396 phần tử; số gặp lại 198; tổng khác nhau theo từng ca 8198. Không khẳng định tổng khác nhau xuyên các ca vì `van_tay` phải được xoá trước mỗi ca.

## Unicode và các hằng mới

`unicode_probe.py` lấy nguyên hàm helper bằng AST từ HEAD và chạy riêng dưới `/usr/bin/python3.12` và `python3` (3.13.18). Hai runtime báo Unicode 15.0.0 / 15.1.0; năm danh sách đại diện, category, thuộc tính whitespace/isdecimal và 19 whitespace ngoài ASCII trùng từng phần tử. Mỗi miền đầy đủ có chín đại diện L/N, một Nd, ba đại diện whitespace; miền có cam loại Zl/Zp còn một whitespace. Xem `unicode-312.json`, `unicode-313.json`.

Các hằng 158,648, số vị trí và số bản gốc lặp dựa trên cấu trúc code. Phần 19/9/1/3 dùng thuộc tính Unicode của các đại diện và whitespace: không phải bất biến cho mọi phiên bản Unicode tương lai, nhưng đã đo bằng nhau giữa đúng hai phiên bản liên quan CI/executor. Tăng tổng số code point L/N/Nd trong Unicode không tự tăng số qua L8 vì điều kiện chỉ chọn ASCII/đại diện (và hai ký tự đặc biệt ſ/K ở a124). Không ghim byte YAML giữa các runtime: dấu vân tay chỉ so các phần tử trong cùng lần chạy.

Phạm vi ledger: count_audit.py thu hồ sơ/provenance tại consumer kiem_ho_so của test A, gọi tiếp module A thật, ghi từng lần gặp lại; đây là phép suy/đếm độc lập dòng đầu vào. Việc cùng tám dòng đi thật qua main→L8 được kiểm bằng c36 đầy đủ trong suite và bằng c36 trên Python3.12. Không gọi ledger A là một lần instrument toàn8396 lời gọi main.
