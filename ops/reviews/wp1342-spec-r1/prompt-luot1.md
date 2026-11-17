Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng.

Thư mục làm việc là một git worktree của kho tra-luat trên base master a0702d0 cộng một tệp đặc tả mới:
`ops/specs/WP1174-WINDOWS-BACKEND-r1.md`.

Đọc: đặc tả đó; `.claude/skills/soan-spec/SKILL.md` (luật L1–L7 và mục 4 là chuẩn của một đặc tả); `.claude/dev/packet_loop.py` các hàm `_1174_*` được nêu (dòng 3659–6036); `.claude/dev/packet_loop_test.py` (WP1174_REQUIRED, WP1174_BOTH, `_windows1174`, cơ chế đột biến); `.claude/dev/launcher.py` `_KhoCodex` (khoảng 3825–4070) và Job Object (892–961); `docs/adr/0053-*.md`, `docs/adr/0055-*.md`, `docs/adr/0067-*.md`; `ops/specs/wp1174-c5-adapter-design.md` §8.

Việc:
1. Kiểm từng lời khai SỰ THẬT trong §0 và §4 với mã (dòng, tên hàm, số ca 85/84/12, 279 khoá đột biến). Báo khớp/lệch kèm tệp:dòng.
2. Kiểm đặc tả theo L1–L7 của soan-spec: mỗi mục tiêu chiếu vào write set (L2); mỗi tiêu chí có phép đo làm nó ĐỎ và phép ấy thật sự đỏ được (L3, L6); có câu nào hỏi/báo chủ kho mà không mang mã E (L7); có ngân sách mềm không.
3. Tính khả thi kỹ thuật trên Windows: các API nêu (CreateFileW+FILE_FLAG_OPEN_REPARSE_POINT, GetFileInformationByHandle(Ex), LockFileEx, FlushFileBuffers, CreateHardLinkW, MoveFileExW REPLACE_EXISTING|WRITE_THROUGH, GetVolumeInformationByHandleW, GetDriveTypeW) có đủ để giữ đúng bất biến của bản Linux tương ứng không? Chỗ nào đặc tả khai "tương đương" mà thật ra không (ví dụ: MoveFileExW trên tệp đang mở, CreateHardLinkW cần cùng volume, ChangeTime có trong FILE_BASIC_INFO chứ không trong BY_HANDLE_FILE_INFORMATION, FileIndex 64-bit vs FILE_ID_INFO 128-bit trên ReFS, LockFileEx trên handle có FILE_SHARE flags...).
4. Ước lượng kích thước r1 (dòng thêm) và đánh giá có vừa trần ADR-0053 (≤ 450 dòng thêm, ≤ 6 tệp) không; nếu không, đề xuất cắt.
5. Rủi ro: lớp rẽ nhánh "chỉ dòng rẽ nhánh trong thân hàm Linux" (N2) có khả thi không khi `_1174_persist` gọi `_1174_fsyncdir`/`os.link` bên trong; phép đo N2 bằng AST có đo đúng thứ khai không.

Đầu ra stdout: (1) bảng kiểm sự thật; (2) danh sách finding P0–P3, mỗi cái: chỗ trong đặc tả, vấn đề, đề xuất sửa cụ thể (câu/ô thay thế); (3) ước lượng kích thước. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
