Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng.

Thư mục làm việc là một git worktree của kho tra-luat trên base master 39ce682 cộng một tệp đặc tả mới:
`ops/specs/WP1174-WINDOWS-BACKEND-r2.md` (revision 2 = bậc "r1b" của lộ trình trong đặc tả r1).

Bối cảnh: đặc tả r1 (land ở merge ded5d41) đã thêm các hàm `_1174_win_*` đứng riêng ở `.claude/dev/packet_loop.py` (khoảng dòng 6037–6166): bindings đọc, `_1174_win_read`, `_1174_win_volume`. Revision 2 thêm khoá `LockFileEx` và publish `CreateHardLinkW`/`MoveFileExW`, vẫn đứng riêng, chưa nối vào runtime.

Đọc: đặc tả mới; `.claude/skills/soan-spec/SKILL.md` (luật L1–L7, mục 4); `.claude/dev/packet_loop.py`: `_1174_lock` (3989), `_1174_persist` (3945), `_1174_probe` (4037), `_1174_command` (5899), `_1174_runtime` (4801) và toàn bộ khối `_1174_win_*` (6037–6166); `.claude/dev/packet_loop_test.py`: `_new1342`, `_additive1342`, `_wired1342`, `_additive_case1342`, `_native1342` và các ca `wp1342_*` (khoảng 16560–16871); `docs/adr/0053-*.md`, `docs/adr/0055-*.md`, `docs/adr/0063-*.md`, `docs/adr/0067-*.md`.

Việc:
1. Kiểm từng lời khai SỰ THẬT trong §0 với mã (dòng, tên hàm, số dòng 13/43/45, chuyện mọi lệnh lấy khoá và runtime đọc boot_id, chốt `_wired1342` trên cây làm việc phủ được hàm mới). Báo khớp/lệch kèm tệp:dòng.
2. Kiểm theo L1–L7: mỗi mục tiêu chiếu vào write set; mỗi tiêu chí có phép đo làm nó ĐỎ và phép ấy thật sự đỏ được (đặc biệt N2 đo một lần bằng `_additive1342`, N3, N4 và ba đột biến M6: mỗi đột biến có thật sự đổi màu đúng ca đích không, có bị một kiểm khác chặn trước làm ca không đổi màu không); câu hỏi/báo chủ kho có mang mã E; không có ngân sách mềm.
3. Tính khả thi và tương đương Windows: LockFileEx chặn + OVERLAPPED; khoá chia sẻ của tiến trình con có thật sự thất bại 33 khi cha giữ khoá loại trừ; CreateHardLinkW(tên mới, tạm) cùng volume và lỗi khi tên đã có; xoá tệp tạm khi còn hard link; MoveFileExW REPLACE_EXISTING|WRITE_THROUGH khi đích đang được mở bởi tiến trình khác hoặc có hard link khác; `_1174_win_read` (share READ) dùng để đọc lại ngay sau publish; mkstemp trên Windows (handle kế thừa?); thứ tự kiểm `_1174_win_volume(cha)` trước mkstemp; vế "định danh tên sau khi có khoá" (FILE_READ_ATTRIBUTES, share READ|WRITE|DELETE) có mở được khi handle khoá share READ|WRITE không DELETE.
4. Ước lượng kích thước (dòng thêm, mã + test) và đối chiếu trần ADR-0053 (≤ 450 dòng thêm, ≤ 6 tệp).
5. Cách đánh số: revision 2 có hợp grammar ADR-0063 (H1 `# <id> r<N> — …` và dòng `- packet_id: …; revision: N;`) không.

Đầu ra stdout: (1) bảng kiểm sự thật; (2) danh sách finding P0–P3, mỗi cái: chỗ trong đặc tả, vấn đề, đề xuất sửa cụ thể (câu/ô thay thế); (3) ước lượng kích thước. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
