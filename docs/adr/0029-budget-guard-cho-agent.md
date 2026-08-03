# ADR-0029 — Budget guard cho agent

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Ngoài trần packet/attempt/depth, mission envelope có mặc định `max_parallel_workers: 2`,
`max_agent_invocations: 30` (executor và reviewer) và `max_cloud_minutes: 360`. Mỗi provider phải có quota
token/chi phí ngày và tháng trong cấu hình canonical; không chấp nhận giá trị unlimited. Dispatcher cảnh báo qua
GitHub ở 80% và chuyển `PAUSE` ở 100%, không tự mua thêm hay đổi provider để lách giới hạn.

Lỗi quota không tính là attempt nội dung nhưng lần gọi/thời gian thực tế vẫn được hạch toán. Local controller cũng
tính invocation và thời gian. Mặc định có thể hạ theo mission; chỉ lệnh có thẩm quyền mới tăng ngân sách và mọi
thay đổi phải có audit. Provider broker là điểm cưỡng chế chi phí mạnh nhất; số liệu trong Issue là nguồn quan
sát và điều phối, không thay thế hard quota của nhà cung cấp.

Các trần là guard độc lập, không phải các mức công suất phải đồng thời đạt được. `max_packets: 20` là trần cấu
trúc chống sinh vô hạn, còn `max_agent_invocations: 30` cố ý có thể PAUSE sớm hơn vì invocation gồm executor lẫn
reviewer; điều này ưu tiên chống hết token/credit. Trước khi cấp lease, dispatcher ước tính số invocation tối thiểu
cho các packet đã biết dưới review policy hiện hành; nếu phần còn lại không đủ thì cảnh báo/PAUSE với lý do
`budget_infeasible`, không để mission dừng “bí ẩn”. State/UI phải hiện `used / reserved / limit`; một invocation
là một request executor/reviewer mà provider đã nhận xử lý. Chỉ người có thẩm quyền mới tăng trần hoặc giảm
assurance.
