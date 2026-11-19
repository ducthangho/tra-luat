Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 4, cho đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (packet P2a, Issue #433, phạm vi POSIX). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp (nếu /tmp chỉ đọc, dùng thư mục ghi được khác hoặc mô phỏng trong RAM và ghi rõ).

Clone master 3b647461db7c8ded1bddd9aafc5c6aa5eead223f, cộng chưa commit: đặc tả cần review; `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1-ban3.md` là bản bạn review lượt 3; verdict lượt 1–3 ở `ops/reviews/wp433p2a-spec/luot{1,2,3}.verdict.txt`; đặc tả và review packet 1 (`ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md`, `ops/reviews/wp433-spec-r1/`).

Quyết định chủ kho là RÀNG BUỘC, không nêu lại: §2/§9 (P2b, P2c, Q2 thu hẹp cho P2c, Q4 reparse sang P2c — đã quyết), và Q1 mới: trần kích thước của RIÊNG packet này nâng lên ≤ 3 tệp / ≤ 550 dòng thêm (dòng khai `nang_tran` đầu tệp, theo tiền lệ). Q3 chặn lease không chặn review — không nêu.

Việc:
1. Diff với `-ban3.md`. Với từng finding lượt 3 (4 P2, 1 P3): đã đóng THẬT chưa. Riêng sổ lượt N9(b): đếm lại ca/lượt theo cột nền §4 (đặc tả khai 11 ca/46 lượt; 7 ca/27 lượt `posix`, 4 ca/19 lượt `mọi` — khác con số bạn viết ở lượt 3, xác nhận cái nào đúng); các đẳng thức ở N9(c) có tự mâu thuẫn không (`d == 0`, `h == u`, `u ≤ 1`).
2. Đột biến mới 46–52: với MỖI cái, chỉ chạy ca đích theo thứ tự lượt và nhãn đã khai — lượt/nhãn ĐẦU TIÊN đỏ có đúng là đích không (đặc biệt 49 với fixture có `token`, 50 với `_ghi_nguyen_tu_0600` của base khi `cfgdir` là tệp, 51 với W6 gọi cùng writer trước W4, 52 với đường cảnh báo thiếu của base). Đo bằng mã trên base khi được. Cặp 46/47 chung đích có chủ ý — có hợp lý không. Tổng §4b (37; E 5; H 32; posix 21; mọi 16).
3. Năm phản chứng bộ đo (`pc_*`): mỗi phép có đổi đúng một thứ và làm đỏ đúng vế không; tách "tự kiểm phân hạng" và "phản chứng bộ đo" có rõ không.
4. §8 (455–545, giữa ~500) có hợp lý so với trần 550 theo mật độ fragment packet 1 (353 dòng, 18 ca, 30 `_DB`, +448).
5. L1–L7 `.claude/skills/soan-spec/SKILL.md` cho phần mới.

Không nêu lại finding đã đóng. Đầu ra stdout: bảng finding lượt 3 (đóng / chưa), finding mới P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
