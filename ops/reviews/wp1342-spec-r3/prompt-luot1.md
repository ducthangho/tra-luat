Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng.

Thư mục làm việc: git worktree kho tra-luat trên master 39ce682, cộng hai tệp đặc tả: `ops/specs/WP1174-WINDOWS-BACKEND-r2.md` (đã đóng băng, chủ kho duyệt, CHƯA thi công — base thật của r3 là master SAU khi r2 land) và `ops/specs/WP1174-WINDOWS-BACKEND-r3.md` (đặc tả cần review: bậc r1c — seed riêng có DACL + BootId Windows, đứng riêng).

Đọc: đặc tả r3 và r2; `.claude/skills/soan-spec/SKILL.md` (L1–L7, mục 4); `.claude/dev/packet_loop.py`: `_1174_seed` (4712), `_1174_runtime` (4801), toàn bộ khối `_1174_win_*` (6037–6166); `.claude/dev/packet_loop_test.py`: `_new1342`, `_additive1342`, `_wired1342`, các ca `wp1342_*`; `.claude/dev/launcher.py` `_KhoCodex._win_private`/`_win_sid`/`_win_security` (khoảng 4030–4110); `docs/adr/0053-*.md`, `0055`, `0063`, `0067`.

Việc:
1. Kiểm lời khai sự thật §0 với mã.
2. Theo L1–L7: mỗi mục tiêu chiếu write set; mỗi tiêu chí có phép đo làm nó ĐỎ thật sự đỏ được (đặc biệt bảng `_1174_win_seed_acl` M5 và đột biến (d)(e) M7 trên Linux; S2/S5/S8 và đột biến (a)(b)(c); N7 khởi động lại VM); mọi câu hỏi/báo/chờ chủ kho mang mã E; không ngân sách mềm.
3. Khả thi và tương đương Windows: GetSecurityInfo trên handle mở GENERIC_READ|READ_CONTROL; dạng SDDL do ConvertSecurityDescriptorToStringSecurityDescriptorW sinh (owner/DACL, cờ P, alias SY, ACE 6 trường, có thể sinh "AI"/"AR" flags?); FileStandardInfo NumberOfLinks qua GetFileInformationByHandleEx (r1 đã bind với argtypes nào?); `between` hook với default None có hợp `_new1342`; DACL cờ ACE rỗng có quá chặt với tệp tạo bằng SetFileSecurity/ConvertStringSecurityDescriptor "D:P(A;;FA;;;<u>)(A;;FA;;;SY)" không; registry BootId: kiểu, WOW64, Fast Startup.
4. Kích thước ước lượng so trần ADR-0053 (≤ 450 dòng thêm).
5. Phụ thuộc r2: r3 có dùng/giả định gì từ r2 (helper `_additive1342r2`, bindings) mà r2 chưa hứa chắc không.

Đầu ra stdout: (1) bảng kiểm sự thật; (2) finding P0–P3 (chỗ, vấn đề, câu thay thế); (3) ước lượng kích thước. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
