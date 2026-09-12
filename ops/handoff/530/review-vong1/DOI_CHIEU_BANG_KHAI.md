# Đối chiếu đủ 25 hàng BANG_KHAI

Lệnh/nguồn và mã thoát đầy đủ nằm trong VERDICT cùng các script/log kèm. Các con số lịch sử và phép tái lập trên HEAD được phân biệt, không thay cái này bằng cái kia.

| # | Kết quả đo lại | Kết luận |
|---|---|---|
| 1 | AST hai blob: t125 3, t153 5, t154 10, t155 4, t156 11, t157 6, t158 7, t159 4, t160 9; tổng 59 | Đúng. t159 đã có thêm một chot từ trước, không đếm nhầm vào 59 phép đổi |
| 2 | Không còn bang trong chín ca sau đổi | Đúng: 0 |
| 3 | t162: 10/10, rc=0 | Đúng trên bộ control hiện có; không chứng minh control đủ |
| 4 | Bộ đo cũ thật + base dc02c9b: 7/10, rc=1; lệch t96, Unicode, thông điệp rỗng | Đúng; `logs/old-grader.log` |
| 5 | Gỡ cơ chế cắt bảng: 8/10, rc=1; hai control dương khớp neo 3/2 lần | Đúng; `recount_history.py` |
| 6 | t161: 16 GIET, 0 KHONG_GIET, 0 KDD | Đúng trên bộ mutant hiện có |
| 7 | Bỏ xóa bốn biến: 15 GIET, 1 KDD, rc=1 | Tổng đúng, lời giải thích 157 ca sai; xem lớp chuyên biệt |
| 8 | t163: 7/7 =6 DO +1 XANH, rc=0 | Đúng số; tín dụng M5 có lỗ đọc chuỗi |
| 9 | Trên 540b6f1, bỏ LF đầu neo: 5/6, rc=1 | Đúng, một neo khớp 2; không so với mẫu số 7 của HEAD |
| 10 | Bơm đọc chi_tiet: A2 XANH_SAI, rc=[1,1], t163 6/7 rc=1 | Đúng và có răng; log `a2-reverse.log` |
| 11 | Wrapper nguyên lệnh rc=5 do tar ownership; thêm TAR_OPTIONS=--no-same-owner: ba dòng 158/158, bỏ qua=0, không ĐỎ, rc=0 | A5 đạt với điều kiện sandbox nêu rõ |
| 12 | Hai suite thật có 155/158 dòng `^<<< ra`, hai AST có 155/158 ca | Đúng |
| 13 | doctrine: 7 tệp/0 chỗ chép, rc=0; ADR:48/48, rc=0 (có ngoại lệ ADR-0016 đã khai) | Đúng |
| 14 | diff name-status đúng 1 đường; numstat +802/−61 | Đúng |
| 15 | HEAD:148 comment +67 blank +89 docstring +498 code/data=802 | Hai số exact đúng; hai ước lượng lệch ±1, ghi NỢ định lượng |
| 16 | Lease r2 ghi S2 300→1000; 1000−802=198 | Đúng văn bản offline và diff. Không truy cập receipt GitHub |
| 17 | Lease r2 ghi S6 2→10, lúc cấp 0 lượt; đây là lượt 1/10 theo chỉ thị | Giá trị văn bản đúng. Không xác minh số vòng đã đăng ở GitHub vì cấm mạng |
| 18 | Nền 105.964561s, HEAD317.002692s; +211.038131s, ×2.991592, cả hai rc=0 | Khác lượt lịch sử, có ghi NỢ số đo; không phải regression mới |
| 19 | t125 54.083s→159.517s, +105.434s | Khác lượt lịch sử; source log lịch sử có53.039/160.378 |
| 20 | Cha wrapper mới: t16149.301s, t1622.172s, t16353.542s | t161/t163 khác ở 1 chữ số thập phân; t162 vẫn2.2; source wrapper cũ49.397/2.213/53.670 đúng |
| 21 | Danh sách khai có9 phần tử; đã gỡ thêm7 chốt ngoài danh sách mà cả ba ca vẫn xanh, còn thiếu AssertionError trần và control KHONG_GIET | “9” chỉ đúng như độ dài danh sách, chưa đủ như kiểm kê |
| 22 | Control sẵn có đúng0 lệch khi gỡ từng nửa, cả hai lệch GIET→KHONG_GIET; retry/direct-reader phân biệt được từng nửa | Số đo hẹp đúng, kết luận tương đương quá rộng |
| 23 | Hai regex đã cho đều không có match trong hai tệp: rg rc=1, count=0 | Đúng phép đếm văn bản; không coi grep là một phép thực thi gate |
| 24 | Gương có365 remotes, tổng412 ref; false shallow; không có tập ls-remote độc lập tại thời điểm cấp r2 | 365 hiện tại đúng; quan hệ365/365 và comm rỗng **KHÔNG ĐO ĐƯỢC độc lập** offline, không tự so gương với chính nó |
| 25 |493 lời gọi trên36f68c7; blob thật5acd563297fea3b8e37dedcd750acd8794d68bec | Số đúng, neo13a2af8c sai/không có trong gương |

Nguồn đo: `count_claims.py`, `count_extra.py`, `recount_history.py`, `retry_materialize.py`, `measure_cost.py`, `verify_gates.py`, `probe.py` và các log đi kèm. Driver đo có rc=0 không có nghĩa mọi suite con rc=0; các rc đỏ dự kiến được ghi riêng trong JSONL.
