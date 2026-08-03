# ADR-0030 — Definition of done của mission

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Khi mọi packet đã `integrated`, acceptance gate xanh và draft land PR sẵn sàng, mission chuyển
`awaiting_land`, gửi thông báo GitHub/Android và ngừng sinh phiên mới. Trạng thái này không phải complete vì thay
đổi chưa vào canonical và vẫn cần người có thẩm quyền gọi operation `land apply` cho đúng mission/head SHA.
Operation có client local lẫn GitHub/Android nhưng không tự merge và không gọi model.

Mission chỉ `complete` sau khi canonical chứa kết quả, land gate được kiểm lại xanh, không còn lease/packet mở
và báo cáo cuối đã ghi mức review, budget, audit cùng cleanup schedule. Merge commit canonical phải neo
`mission_id` và final state hash đã kiểm với journal; cleanup chỉ chạy sau readback hai giá trị này. Deploy không
mặc nhiên thuộc definition of done; chỉ mission có acceptance criteria yêu cầu LIVE mới chờ cổng deploy riêng.
Nếu land thất bại, mission quay về `paused` hoặc tạo packet sửa lỗi trong envelope, không được đánh dấu hoàn tất giả.
