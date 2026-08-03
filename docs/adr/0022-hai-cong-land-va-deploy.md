# ADR-0022 — Hai cổng land và deploy

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Dispatcher được tự chuẩn bị draft land PR khi các packet của mission đã qua worker gate và review policy, nhưng
không được merge. Operation `land prepare` đóng băng mission, tích hợp tuần tự, gán version, hợp nhất changelog
fragment, tái sinh manifest và chạy land gate Windows–Linux. Đây là thao tác chuẩn bị/kiểm chứng, không phải
quyền ghi canonical; skill `land-packets` chỉ là một client local của operation này.

Chỉ operation `land apply` được người có thẩm quyền gọi tường minh cho đúng `mission_id` và `head_sha` mới được
merge canonical sau khi gate xanh. Entry point có thể là skill local, `/land apply` trên GitHub hoặc typed
`workflow_dispatch`; cả ba gọi cùng logic tất định, không gọi model, kiểm head chưa đổi và ghi audit. GitHub
Environment approval bảo vệ job apply. Deploy/publish LIVE là lệnh và phê duyệt riêng, không tự chạy sau merge
và không được suy ra từ apply. Vì vậy quyền canonical và quyền LIVE vẫn là hai cổng độc lập do người dùng giữ.
