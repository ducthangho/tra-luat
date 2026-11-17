Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet nhỏ, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng.

Thư mục làm việc: git worktree kho tra-luat trên base master 39ce682 cộng tệp đặc tả `ops/specs/LAUNCHER-PY311-LOC-THU-MUC-r1.md`.

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7, mục 4); `.claude/dev/launcher.py` dòng 270–330 (`_ShutilWin311`, `_thuc_thi`); `.claude/dev/launcher_test.py`: cách đăng ký ca (`CA`, decorator quanh dòng 55–75), bảng `DOT_BIEN` (từ dòng 14590) và cách runner đột biến áp/đếm (tìm hàm chạy DOT_BIEN), các ca `r1335_F6_*`.

Việc:
1. Kiểm từng lời khai sự thật ở §0 với mã (dòng, hành vi). Có thể tự đo hành vi trong bộ nhớ bằng cách import `launcher` và gọi `_ShutilWin311.which` trong thư mục tạm (không ghi vào worktree).
2. Theo L1–L7: tiêu chí nào không thể đỏ; đột biến M2 có khớp ĐÚNG MỘT chỗ trong `launcher.py` không; runner `DOT_BIEN` của `launcher_test.py` có áp đột biến lên `launcher.py` (không phải lên tệp test) và có điều kiện nền nào làm đột biến bị bỏ qua trên Linux/Python 3.11 không; ca đổi cwd tiến trình có an toàn với cách runner chạy ca (song song? cùng tiến trình?) không; đối chứng ở N1 có đúng không.
3. Kích thước ước lượng và lớp review.

Đầu ra stdout: (1) bảng kiểm sự thật; (2) finding P0–P3 (chỗ, vấn đề, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
