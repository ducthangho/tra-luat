# ADR-0046 — Mô hình phiên: tác giả xuyên suốt, reviewer mới, cắt ở biên packet

- **Trạng thái:** Accepted (2026-08-22, phiên `phien-tra-luat-5a`; chủ kho phê duyệt trực tiếp)

## Bối cảnh

Hai câu hỏi vẫn bị trộn làm một: *"phiên nào được giữ context lâu"* và *"phiên nào được quyền nói
đã kiểm"*. Trộn chúng dẫn tới hai cách hỏng ngược nhau. Cắt phiên tác giả quá sớm thì mất đúng thứ
đắt nhất packet sản xuất ra — chuỗi lý do vì sao từng con số là con số ấy, vì sao một hướng bị loại;
thứ đó không nằm trong diff và không tái dựng được từ kho. Giữ một phiên làm cả tác giả lẫn reviewer
thì được context nhưng mất tính độc lập, và mất theo kiểu **không nhìn thấy được**: phiên ấy soi mã
theo đúng khung khái niệm đã dựng ra mã.

Đo được ở `PLAT-X8`: hai lượt review đầu do chính phiên soạn đặc tả tự làm. Cả hai kết luận
`approved`/`changes_requested` có bằng chứng chạy được, đúng cú pháp, không lượt nào lười. Cả hai
vẫn bỏ sót một lỗ hạ lớp trong `_BANG_LOP`, vì cả hai hỏi *"mã có khớp bảng không"* — bảng là tiền
đề của chính chúng. Lượt 3, phiên khác, hỏi *"bảng có khớp §8 không"* và tìm ra ngay. Chênh lệch
không phải nỗ lực; nó là **vị trí đứng**.

## Quyết định

1. **Tác giả xuyên suốt một packet.** Phiên soạn đặc tả / điều phối giữ nguyên qua các lượt vá của
   cùng packet. Không cắt giữa chừng để "làm mới context" — chi phí là mất chuỗi lý do, và chuỗi ấy
   không có trong kho.
2. **Reviewer luôn là phiên MỚI.** Mỗi lượt review chạy trong phiên riêng, sandbox riêng, read-only,
   neo `--expected-head` vào exact SHA. Reviewer không được là phiên đã soạn đặc tả hoặc đã vá.
3. **Cắt ở BIÊN PACKET, không cắt giữa packet.** Biên packet là chỗ chuỗi lý do đã kết tinh thành
   hiện vật bền (đặc tả, verdict, biên nhận, nợ có tên). Cắt ở đó mất ít nhất.

## Hệ quả

- Assurance vẫn theo `PROTOCOL §8`: reviewer cùng provider với executor được ghi mức thấp hơn
  cross-provider. ADR này nói về **phiên**, không nới bất kỳ mức assurance nào.
- Một lượt review do phiên tác giả tự làm KHÔNG bị cấm — nó vẫn có ích làm bằng chứng chẩn đoán —
  nhưng phải khai `la_canonical: false` và không tăng `review_rounds_used`.
- Giữ tác giả xuyên suốt làm tăng rủi ro *"tác giả tin mô hình của chính mình"*. Đối trọng là điều
  2 cộng hai luật ở §8 (reviewer phải ĐO được; đối chiếu lượt trước bắt buộc) — ADR này chỉ có
  răng khi hai luật ấy có răng.

## Cưỡng chế

**0 cổng.** Không cổng nào đọc "phiên nào soạn đặc tả". `nguoi_review_phai_khac_phien` trong tệp
lease là **lời khai của người cấp lease**, không phải phép đo — nói thẳng ở đây để không ai đọc một
trường khai thành một chốt đã chạy. Đây là nợ, không phải cài đặt.
