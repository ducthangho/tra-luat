# ADR-0062 — ADR-0060 mặc định và đóng băng ADR-0054

- **Trạng thái:** Accepted (có hiệu lực từ commit land ADR này trên first-parent `master`; không hồi tố với packet đã merge).
- **Nguồn:** packet `ADR-0060-MAC-DINH` #1124, đặc tả r3 đã duyệt.

## Bối cảnh

ADR-0060 M10 trước đây chỉ kích hoạt luật merge khi đặc tả có đúng một dòng `dieu_kien_merge` hợp lệ. Packet không có dòng ấy đi theo luật cũ. ADR-0054 được ghi Accepted nhưng chưa từng kích hoạt; các bất biến còn giá trị của nó cần ở protocol chung.

## Quyết định

**N1 — ADR-0060 là luật mặc định.** Mọi packet chưa merge kể từ commit land ADR-0062 đều chịu ADR-0060, dù đặc tả không khai dòng `dieu_kien_merge`. Không có dòng khai thì đạt phép đo dòng khai K1. Nếu có đúng một dòng, OID vẫn phải qua ba phép đo cũ của M10: commit đưa ADR-0060 vào kho, trước commit ấy chưa có tệp ADR-0060, và OID nằm trên first-parent `master`. Từ hai dòng khai trở lên, hoặc một dòng sai, K1 đỏ. Các điều kiện khác của ADR-0060 giữ nguyên.

**N2 — Một luật merge.** Nhánh “packet chưa áp” của bảng ngưỡng §8 protocol hết hiệu lực từ mốc trên; mọi packet chưa merge đi theo ADR-0060. Các bản ghi lịch sử của packet đã merge không được viết lại.

**N3 — ADR-0054 đóng băng.** ADR-0054 chưa từng được kích hoạt và từ nay không kích hoạt. Ba bất biến về cổng tại chỗ trước push, lần push thêm vì CI đỏ và nhánh chỉ chứa sổ sách được chuyển vào `docs/PROTOCOL_DA_PHIEN.md`. Code `MAY-ADR-0054` trong `packet_loop.py` giữ nguyên, ở trạng thái ngữ nghĩa ngưng hoạt động; việc gỡ code đó thuộc packet khác.

**N4 — Phạm vi đếm push.** M5 của ADR-0060 cấm đổi tên ref để tránh đếm một lần push code. Một nhánh chỉ chứa sổ sách (`ops/leases/**`, `ops/specs/**`, biên nhận hoặc bia mộ), không chứa tệp nào thuộc write set code của packet, không phải lần push code. Nhánh chứa bất kỳ tệp nào thuộc write set code phải bị đếm, bất kể tên ref.

## Kiểm chứng

`kiem-merge` K1 thực hiện ba trạng thái dòng khai 0/1/≥2; `packet_loop_test.py` giữ ca OID hợp lệ và hai dòng, thêm ca không dòng cùng đột biến đối chứng. `adr-song` kiểm mốc ADR; `doctrine-scan` kiểm nhất quán protocol. Các cổng Windows và `full_mutant_audit` của packet #1124 giữ nguyên.
