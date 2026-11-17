Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 2, cho ĐẶC TẢ `ops/specs/WP1174-WINDOWS-BACKEND-r1.md` trong thư mục làm việc (worktree base a0702d0, đặc tả là tệp untracked). CHỈ ĐỌC; không ghi tệp; không gọi mạng.

Lượt 1 (bạn) trả `request_changes` với chín P2 (rẽ nhánh contextmanager; AST mù byte; runner MUTANTS bộ ba; junction không chứng minh cờ reparse; N3 chốt OS có thể xanh vì tầng khác; hợp đồng handle/định danh; publication/volume; probe khai sẵn; dự toán vượt trần) và hai P3 (trục vòng ADR-0048; timestamp/base/nguồn quyết định). Bạn đề xuất cắt r1 xuống bindings + open/read + volume NTFS + test.

Người soạn đã viết lại: r1 chỉ còn `_1174_win_read` và `_1174_win_volume`/`_1174_win_platform` ĐỨNG RIÊNG, KHÔNG nối vào runtime (vì `_1174_read` còn được hook đọc trạng thái ở packet_loop.py:1419 dùng, nối sẽ đổi hành vi Windows ngoài WP1174); N2 so BYTE mọi định nghĩa có ở base; bảng đột biến riêng `MUTANTS_WIN1342`; lock/publish/probe sang r1b.

Việc:
1. Với từng finding lượt 1: đóng / chưa đóng / không còn áp dụng (vì cắt phạm vi), kèm chỗ trong đặc tả mới.
2. Kiểm lời khai sự thật mới (§0, M2, M3: dòng 1419, 12021/12095/12105, schema bộ ba, launcher 4020–4041) với mã.
3. Kiểm theo L1–L7 của `.claude/skills/soan-spec/SKILL.md`; đặc biệt mỗi tiêu chí N1–N9 có phép đỏ thật sự đỏ được và đỏ đúng nguyên nhân (L3, L6).
4. Kỹ thuật M2/M3: cờ, share mode, mở lại tên, FileBasicInfo/FileAttributeTagInfo, GetVolumePathNameW + GetDriveTypeW + đối chiếu serial — đủ và đúng chưa; lỗ nào còn.
5. Dự toán kích thước r1 mới so trần ADR-0053.

Đầu ra stdout: bảng đóng finding; finding mới P0–P3 kèm câu thay thế cụ thể; dự toán. Dòng CUỐI đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes` (approve chỉ khi không còn P0–P2).
