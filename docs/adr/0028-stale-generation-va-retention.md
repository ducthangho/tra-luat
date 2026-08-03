# ADR-0028 — Stale generation và retention

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Khi lease hết hạn hoặc bị thu hồi, dispatcher tăng generation và cố hủy workflow/process cũ. Từ thời điểm đó,
heartbeat, push và handoff mang generation cũ bị từ chối; branch/PR chuyển `stale` và không được tự merge hay tự
cherry-pick sang generation mới. Executor mới có thể đọc diff/ghi chú cũ như bằng chứng tham khảo nhưng phải tự
đánh giá và tạo thay đổi trên branch mới có lease hợp lệ.

State projection và event journal lưu commit SHA cuối của stale generation. Local worktree chỉ được dọn sau khi process đã dừng; remote
branch/PR giữ đến khi mission land hoặc hủy, cộng 30 ngày, rồi mới được tự xóa với audit. Lệnh có thẩm quyền
`/packet preserve` giữ artifact lâu hơn. Chính sách này ưu tiên chống split-brain nhưng vẫn cho phép cứu tri thức
từ lần chạy cũ mà không mặc nhiên tin mã chưa hoàn tất.

Recovery snapshot của mission active giữ theo mức tối đa repo cho phép và được làm mới khi dispatcher chuyển
state; không được coi là lưu trữ vĩnh viễn vì workflow artifact có thể hết hạn hoặc bị xóa cùng workflow run.
Khi mission complete, final state hash được neo vào commit canonical và báo cáo cuối trong Issue; cleanup chỉ bắt
đầu sau khi hai neo này đã đọc lại khớp.
