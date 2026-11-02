Reviewed commit: cffd44e75ba97af4c99d790704e7478945344ada
Verdict: changes_requested — P0=0 P1=0 P2=5 P3=0

Trạng thái: đang review; dòng verdict sẽ được chốt sau khi hoàn tất phép đo.

- HEAD khớp SHA yêu cầu; worktree sạch.
- SHA-256 đặc tả trên base khớp `6bcac18917516e89119065a249037cb81f13d77b01bb77e7b557f6d23d5c0b07`.
- Diff base → head: chỉ `.claude/dev/packet_loop_test.py`, +335/−19 (A9 đạt).
- Kho nguồn chỉ đọc; mọi bản sao, fixture và log đặt dưới `/tmp` hoặc thư mục ra.

## Finding đã xác nhận (đang tiếp tục quét)

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| tin-dung-giet-sai | P2 | `.claude/dev/packet_loop_test.py:5367–5369` | traceback thực ở F02 bọc JSON object/nested, list/dict repr hoặc tiền tố log, trên cả stdout/stderr: CLI rc12 nhưng được `GIET`; ba đối chứng khác họ xanh | nhận diện traceback độc lập với vỏ trình bày, đồng thời giữ đối chứng tên check hợp lệ; bổ sung tự kiểm và HINT |

Bằng chứng mới: `evidence/wrapped_probe.py`, `wrapped-results.json`, `wrapped-results.log`. Cả JSON scalar và repr scalar được loại đúng; JSON object/nested, list/dict repr và logger prefix đều bị bỏ lọt. Tất cả dùng chính ngoại lệ ValueError do `int()` tại F02, không tạo byte thô, symlink hay đường dẫn thoát cây. Kết luận này giữ slug lớp của lượt 1.

Các đường cũ đã được đo lại: rc ngoài {0,2,12}, stdout, repr scalar, help formatter, AssertionError/BoQua cause/context/from None và ExceptionGroup được loại đúng. Cặp M6 nền xanh; ba đột biến độc lập M5(a)/(b)/(c) đều làm đúng ca tự kiểm đỏ. Các mutant t822 nạp module riêng đều dùng classifier đúng module; danh tính `_TinDungGia` khác nhau không gây sai ở đường hiện có.

## Phủ theo lớp — các finding bổ sung đã đo

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| sha-chi-do-ngan-va-hoa | P2 | `.claude/dev/packet_loop_test.py:5410, 5782, 5832, 5879` | ba mutant regex nhận g–z / nhận 39 / nhận 41 ký tự đều sống 129/129 kg; fixture cùng head/run hợp lệ khác: rc2→0 | thêm ba biên SHA, mỗi mutant ánh xạ K21 |
| id-lon-nhat-chua-do-so-hoc | P2 | `.claude/dev/packet_loop_test.py:5436, 5681, 5889` | `max(..., key=str)` sống 129/129 kg; id9 xanh/id10 đỏ: rc12→0; chiều ngược rc0→12 | thêm cả chiều của biên chữ số, đột biến max theo chuỗi, ánh xạ K30 |
| canh-bao-chi-do-mot-id | P2 | `.claude/dev/packet_loop_test.py:5555–5578, 5885` | hằng count=1 và chỉ liệt kê id đầu đều sống 129/129 kg; hai id suite khác cho cùng rc0 nhưng stderr sai | đo ≥2 id phân biệt, bản lặp và nhiều tên bắt buộc trong cùng ca; K26 |
| chi-kiem-kieu-trang-dau | P2 | `.claude/dev/packet_loop_test.py:5748–5775, 5858–5872` | chỉ kiểm schema run / kiểu suite.id / kiểu total_count ở trang0 đều sống 129/129 kg; trang1 hỏng cho rc12→0 | fixture phân trang cho từng kiểu/hiện diện, các mutant thu hẹp về trang0, nối K05/K07–K15/K37 |

Các dòng trên là thiếu biến thể của thành phần ĐÃ có trong bảng, không phải thành phần hoàn toàn vắng bảng. Chưa xác nhận `kiem-ke-bo-sot` hoặc điều kiện H2=9. Biên nhận nguyên văn nằm trong `evidence/audit-*.json`; giữ cả stdout/stderr của nền và mutant.

Lưu ý công cụ kiểm toán: lượt chạy audit ban đầu dùng mỏ neo SHA quá ngắn, khớp hai chỗ và dừng với lỗi probe. Không dùng lỗi ấy làm finding. Đã siết neo thành toàn dòng `SHA_RE`, đo lại ba mutant thành công; các audit còn lại được chạy bù theo tên.

A8: base/head đều rc0 ở doctrine-scan và adr-song. A10: bare Ruff chạy no-cache, cả hai cùng rc1 vì hai F541 có sẵn; không F401/F821, delta F=0 (`gates.json`, `ruff-*.json`).
