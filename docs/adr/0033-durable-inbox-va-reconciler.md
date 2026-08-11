# ADR-0033 — Durable inbox và reconciler

- **Trạng thái:** Accepted (2026-08-03, hợp nhất phản biện cuối)

GitHub Actions concurrency chỉ bảo đảm tối đa một run trong group đang chạy; mặc định pending run cũ có thể bị
pending run mới thay, `queue: max` vẫn có trần 100 và thứ tự chạy không theo thời điểm dispatch. Vì vậy trigger
workflow không phải hàng đợi lossless. Command/handoff phải tồn tại trước thành durable inbox fact có ID trong
Issue/PR; workflow chỉ là wake-up. Một reconciler single-writer đọc fact chưa tiêu thụ theo `(created_at, id)`,
kiểm expected revision/generation/spec hash, áp transition idempotent và ghi `last_consumed_event_id` cùng
full-state checkpoint nối hash.

Dispatcher có thể dùng `concurrency.queue: max` với `cancel-in-progress: false` làm backpressure, không làm nguồn
đúng. Scheduled/manual reconcile bắt lại event khi wake-up bị hủy, queue đầy hoặc runner lỗi. Event sai thứ tự chờ
predecessor hay bị reject có audit; retry cùng ID không tạo transition thứ hai. Sửa/xóa fact đã consume, chain
đứt hoặc projection không dựng lại được đều `paused`, không suy đoán. Trước cloud canary, shadow gate phải chứng
minh burst ít nhất ba event, đảo lịch chạy, retry, edit/delete, queue overflow mô phỏng và recovery khi projection
bị mất.

Mission envelope có `max_inbox_backlog`; chạm trần thì PAUSE nhưng không drop fact. Reconciler đọc theo page hữu
hạn và tự wake lại tới khi backlog rỗng, nên giới hạn tải không biến thành giới hạn mất dữ liệu.
