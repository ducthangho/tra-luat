# Inventory reviewer từ SPEC §2–3

Nguồn đóng băng: SPEC.md sha256 bdde0a9bdba79a19fbbc77cfee8311e209b0c91cc16612bb8029167cca186577. Danh sách dưới đây lấy yêu cầu của đặc tả làm đơn vị; số ô bảng toán tử không dùng làm mẫu số độ phủ.

| Nghĩa vụ | Giá trị phải giữ | Chốt / chứng cứ cần đối chiếu |
|---|---|---|
| 2.1.1 tổng | 158 ký tự khác nhau | c37 total/unique; c39 extra/duplicate/nonBMP controls |
| 2.1.1 ASCII | Mỗi U+0000…U+007F đúng một lần (128 giá trị) | Kiểm riêng thay NUL hoặc DEL bằng U+0081, vẫn 158 khác nhau; range đúng trong HEAD chưa chứng minh có phản chứng chống hồi quy |
| 2.1.1 category | Lu Ll Lt Lm Lo Mn Mc Me Nd Nl No Pc Pd Ps Pe Pi Pf Po Sm Sc Sk So Zs Zl Zp Cc Cf Co Cn (29); Cs vắng | c39 từng category; trace phải cho đúng tên thiếu và 0 ô |
| 2.1.1 nonBMP | đúng 1, CR/LF không lọt phần ngoài ASCII | c39 bỏ/thừa/lặp nonBMP, thay bằng ASCII; biên U+FFFF/U+10000 |
| 2.1.2–3 ô | 648 hằng, hai chốt trước ô đầu | c39 bỏ/thừa ô; controls648, negatives0; guard_witnesses dùng consumer thật |
| 2.2.1 số ca | a1241733,a1253840,a12652,a12936,a1311,a1321280,a1331136,a134318 | Tám công thức cố định cấu trúc + miền; c36 đầy đủ; P4/P5 chạy subset được §3 cho phép |
| 2.2.1 khác nhau | chống thay ô bằng bản sao trong lớp lịch sử | probes/excess/distinct_target; không mở rộng sang ô khác không trùng (§8) |
| 2.2.2 miền từng ca | a124:30; a125,a129:trừCs; a126:trừZl,Zp; a132,a133,a134:30; a131 không dùng bộ sinh | c36 tập ký tự từ hồ sơ + bytes provenance thực qua L8; c40 category/nonBMP/control a131 |
| 2.2.3 sổ | 8 ca × bỏ/đổi tên/nhân đôi =24 | c38, trace đúng DO:c36 |
| 2.3.1 bộ1 | cam='—', bo=(), count31, vắng() | Phản chứng sai riêng tại bộ này |
| 2.3.1 bộ2 | cam='', bo=('Cs',), count30, vắngCs | Phản chứng sai riêng tại bộ này |
| 2.3.1 bộ3 | cam='\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029 \t', bo=(), count29, vắngZl/Zp | Phản chứng sai riêng tại bộ này |
| 2.3.1 bộ4 | cam='', bo=(), count31, vắng() | Bỏ/cắt/lặp/thay bộ4 |
| 2.3.1 bộ5 | cam='\r\n', bo=('Cs',), count30, vắngCs | Bỏ/cắt/lặp/thay bộ5; đồng thời thay AST + bảng kỳ vọng để kiểm sự độc lập với SPEC |
| 2.3.1 mỗi bộ | không lặp category, không thuộc cam, >=U0080, cuối ngoàiBMP và duy nhất | a136 từng predicate với negatives và controls biên |
| 2.3.2 tham số | bộ sinh giả phải thực đi qua cùng hàm kiểm | trace cache bật/tắt; function keys khác; a135 standalone |
| 3 sửa trong nhớ | neo văn bản đúng1; rc3 đúngDO; nguyên vẹn xanh | c39 neo0/nhiều; nap_sua; profile mọi chay_ca ở c39/c40/a136 |
| P1 | bỏ từng29 category → c37, nêu category | c39 29 nhánh; không lấy một category thay29 |
| P2 | bỏ nonBMP → c37 | c39 |
| P3 | thừa phần tử hoặc lặp category → c37 | c39 |
| P4 | bỏMn, thật main→L8 ít nhất a129 → c36 | c40/b02_targeted |
| P5 | a129 mất một kiem cấu trúc, thật main→L8 → c36 | c40/b02_targeted |
| P6 | đổi category thành bản sao category khác, giữ số lượng → c36/c37 | c39,c40 |
| P7 | bốn giả: bỏcategory, bỏnonBMP, bỏlọccam, bỏlọcbo_loai → a135 | a136 profile |

So với nghia-vu.md: mục ASCII của executor gộp vào tổng/khác nhau và chỉ thử range±1/cắt một đầu; cần phép thay giữ cardinality. Mục danh tính năm đối số dùng AST và BO_SINH_MONG, chưa có nguồn thứ ba ghim giá trị SPEC khi hai nguồn cùng đổi. Đã tái lập cả hai: replacement NUL/DEL vẫn xanh là R4-02; đồng thời đổi hai nguồn ở bộ3/4/5 vẫn xanh là R4-01. Xem domain-review4.json, ast-review.json và co-drift-witness.json.
