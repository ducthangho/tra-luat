# AUDIT CỦA NGƯỜI — `SLICE-B-C` (#215 / PR "#216"), neo `15f824d2`

**BẢN CHIẾU, không phải nguồn có thẩm quyền** — và chiều ấy NGƯỢC với verdict của một mô hình.
Thứ §8 đòi là **danh tính bền trên GitHub**, mà danh tính ấy chỉ tồn tại ở phía GitHub; một tệp
trong kho không mang được nó. **Nguồn là comment `5368471633`**; tệp này để tra ngoại tuyến.

- Người audit: `ducthangho` (`author_association: OWNER`)
- Đăng lúc: `2026-08-21T10:07:58Z`
- Nguồn: https://github.com/ducthangho/tra-luat/pull/216#issuecomment-5368471633

---

## Nguyên văn

## human_audited — SLICE-B-C (#215), người audit: @ducthangho

Tôi tự đọc `git diff origin/master...15f824d -- ops/` (2 tệp: `+110` NO_KY_THUAT.md,
`+93` lease_publish_test.py; riêng lượt vá cuối `+124/−119`) và Issue #215.

Ba chốt tôi soi trực tiếp:

1. **Quyết định BỎ `t42`.** Đây là thu hẹp phạm vi packet — Issue #215 đặt ba việc,
   việc thứ ba nay không còn. Tôi chấp nhận lý lẽ: ba lượt liên tiếp cùng một hình
   dạng lỗi (cross-review 1 tìm đột biến NỚI regex; bản vá đẻ hai docstring tự mâu
   thuẫn + một con số chết ngay trong commit sinh ra nó; cross-review 2 tìm đột biến
   SIẾT regex), và `t42` là một lời khai về một lời khai nên mỗi bản vá lại sinh một
   câu mới có thể trôi.

2. **`t43` có răng và không báo động giả.** Bốn đột biến trên bản sao cả cây: gỡ
   marker đang có → ĐỎ (trước: 43/43 không ai bắt); thêm mục trùng ID → ĐỎ (trước:
   `set` xoá dấu vết); thêm marker không có nhà → ĐỎ; **chèn câu văn xuôi → XANH**
   (trước: đỏ oan). Ca âm quan trọng ngang ba ca dương.

3. **§11 ghi NỢ, không ghi chiến thắng.** Nó nói rõ docstring `t34` vẫn liệt kê năm
   dạng và con số `3/8` mà **không cổng nào canh** cho chúng khớp hành vi thật nữa,
   kèm điều kiện XONG cụ thể và câu dặn đừng dựng lại `t42` nguyên dạng.

Bằng chứng máy tôi đối chiếu, không tự chạy lại: `gate (ubuntu-latest)` success trên
đúng head này (run 32469332687, `09:44:38Z → 09:50:05Z`, 0 bước lỗi); `lease_publish`
42/42; `tl selftest` 1698/1698; năm cổng `tl.py` đều `"ok": true`.

### Hai điều tôi chấp nhận TƯỜNG MINH khi ký

- **Packet giao ÍT HƠN Issue #215 đặt ra.** Việc thứ ba bị bỏ và chuyển thành nợ
  `t34-loi-khai-pham-vi-khong-co-cong` (§11). Mục tiêu gốc — canh cho lời khai phạm
  vi của `t34` không trôi — VẪN CHƯA CÓ CỔNG NÀO.
- **Head cuối chưa qua nhà cung cấp thứ hai.** Hai lượt codex neo `181bd7f` và
  `175e95b`, cả hai CŨ HƠN head này. Chữ ký của tôi THAY cho lượt ba, không cộng
  vào hai lượt kia.

Ghi để không ai đọc nhầm: đây KHÔNG phải một lần hạ ngưỡng. `human_audited` là mức
hợp lệ sẵn của §8 cho class `sensitive`, và không có tệp uỷ quyền nào — khác #204,
nơi `cross_approved` không đạt được nên phải có override có ghi.

VERDICT: approve
Reviewed commit: 15f824d29b6e72b0b8f0bcc14328ba85531280ef
