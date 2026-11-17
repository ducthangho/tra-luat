Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng.

Thư mục làm việc: git worktree kho tra-luat trên base master 39ce682 cộng tệp đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r2.md` (bản sửa sau review lượt 2). Kết quả review lượt 1 và lượt 2 của bạn ở `ops/specs/.luot1-review.txt`, `ops/specs/.luot2-review.txt`.

Việc:
1. G1 (lượt 2) đã đóng chưa: M1 nói rõ phạm vi dùng của sáu API; N6 quy định chạy riêng đột biến B1 và không tính lỗi L2 thay cho B1.
2. Soát toàn đặc tả lần cuối theo L1–L7 của `.claude/skills/soan-spec/SKILL.md` và theo các finding F1–F7 đã đóng: có ô nào mâu thuẫn nhau, phép đỏ nào không thể đỏ, lời khai sự thật nào lệch mã (đối chiếu `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`), câu hỏi/báo/chờ chủ kho nào thiếu mã E.

Đầu ra stdout: (1) G1 đóng/chưa kèm bằng chứng; (2) finding MỚI P0–P3 nếu có (chỗ, vấn đề, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
