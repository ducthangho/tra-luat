# ADR-0021 — Local controller headless trên Windows

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Packet `local` được thực thi bởi một controller Python duy nhất cài qua Windows Scheduled Task, chạy dưới tài
khoản không có quyền quản trị và không mang credential LIVE. Khi host trực tuyến, controller chỉ nhận packet có
lease/generation hợp lệ từ GitHub, tự tạo branch và worktree riêng rồi gọi `claude -p` hoặc `codex exec` với
prompt đã bàn giao. Nó chịu trách nhiệm heartbeat, worker gate, PR và handoff; worktree chỉ được dọn sau khi PR
đã merge hoặc packet bị hủy có kiểm soát.

Khi host tắt, packet ở nguyên hàng đợi và không bị tự chuyển sang cloud. Không dùng generic self-hosted GitHub
runner vì runner đa dụng mở bề mặt thực thi từ GitHub vào máy cá nhân; local controller chỉ hiểu schema packet,
write set và lệnh agent đã allowlist. Tác vụ tự động là headless worker run, không bảo đảm xuất hiện như chat
tương tác trong ứng dụng Claude/Codex. Remote/chat dành cho người dùng can thiệp khi `PAUSE` hoặc `blocked`.
