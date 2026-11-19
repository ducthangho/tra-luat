Bạn là reviewer ĐỘC LẬP (họ OpenAI), chỉ đọc. Thư mục làm việc là worktree của kho tra-luat ở commit 3b647461db7c8ded1bddd9aafc5c6aa5eead223f (origin/master). Đối tượng review: ĐẶC TẢ packet `ops/specs/LAUNCHER-BAM-LOG-NEN-WINDOWS-r1.md` (tệp chưa commit, chỉ nằm trong worktree này). Đây là packet B của #387: mở phép "đợi cây tiến trình chết trước khi băm log" (đã làm cho Linux ở packet A, land e4fdf09) sang Windows bằng Job Object; Darwin bị chủ kho loại khỏi phạm vi (giữ hành vi A, nợ `wp387-darwin-chua-do`).

Việc phải làm, theo thứ tự:
1. Kiểm §0 bằng ĐO trên mã thật (`.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`): số dòng, hàm, nguyên văn, số ca, số mục đột biến. Lời khai nào sai thì nêu số đúng kèm lệnh bạn đã chạy.
2. Kiểm luật L1–L7 trong `.claude/skills/soan-spec/SKILL.md` trên đặc tả.
3. Kiểm §4b (bảng đường vào/đột biến) có ĐỦ không: liệt kê mọi đường vào mà thay đổi M1–M5 mở ra (hàm đợi, quyết xoá prompt, mốc ket_thuc, fixture bắt tay job, teardown/CloseHandle, nền khác) và đối chiếu với bảng. Với từng đột biến: mẫu tìm có khớp ĐÚNG MỘT chỗ trong mã sau khi áp M1–M4 không (luật `t117`); ca đích có thật sự ĐỎ dưới đột biến đó không (lý luận trên mã ca và hàm), hay đột biến SỐNG / chết vì lý do vô can (tín dụng giả). Bạn có thể dựng bản vá thử trong /tmp nếu sandbox cho phép; nếu không, lý luận và nói rõ "không chạy được".
4. Kiểm tính khả thi trên Windows: bắt tay `job-da-gan`, teardown chờ job rỗng rồi CloseHandle, `os.killpg` thiếu, `San.rmtree(ignore_errors=True)`, mở 9 ca (đặc biệt (a),(c),(d),(f),(g),(h),(i)) — có ca nào vẫn ĐỎ oan hay BỎ QUA trên Windows không. Xác nhận finding cũ P2 (teardown nuốt lỗi/không kiểm CloseHandle) và P3 (đếm BO QUA trên log Linux thay vì Windows) đã thực sự đóng.
5. Ước lượng kích thước có hợp lý so với trần 450 dòng thêm (ADR-0053) không.

Không sửa tệp nào trong kho. Mỗi finding: mức (P1/P2/P3), vị trí trong đặc tả, bằng chứng (lệnh + output hoặc dẫn dòng mã), và cách sửa đề xuất.

Kết thúc bằng đúng một dòng cuối: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`.
