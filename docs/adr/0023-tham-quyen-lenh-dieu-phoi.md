# ADR-0023 — Thẩm quyền lệnh điều phối

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Điều khiển từ GitHub web hoặc Android dùng một tập lệnh đóng như `/mission start|pause|resume`,
`/packet retry|cancel|reroute`, `/land prepare` và `/land apply <mission_id> <head_sha>`. Một typed
`workflow_dispatch` có hai input tương đương được phép gọi cùng operation apply. Dispatcher chỉ thi hành khi
actor vừa nằm trong allowlist được bảo vệ trên canonical, vừa có quyền GitHub `maintain` trở lên tại thời điểm
nhận lệnh; quyền được hỏi lại qua API, không suy ra chỉ từ `author_association`, label hoặc nội dung comment.
Apply còn phải khớp head đã freeze, land gate xanh và GitHub Environment approval. Lệnh sai schema, stale head
hay thiếu quyền bị bỏ qua an toàn và mọi quyết định chấp nhận/từ chối đều được ghi audit.

Output của agent — kể cả comment, review và handoff có cấu trúc — chỉ là dữ liệu không mang thẩm quyền. Nó không
thể tăng mission envelope, đổi packet sang LIVE, sửa security paths hoặc tự cấp quyền. Allowlist và parser lệnh
nằm trên canonical, thuộc security paths, nên feature branch và prompt injection không thể thay quy tắc cho lần
chạy hiện tại.
