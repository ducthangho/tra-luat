Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 3, cho đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (packet P2a, Issue #433, phạm vi POSIX). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp (nếu /tmp chỉ đọc, dùng thư mục ghi được khác hoặc mô phỏng trong RAM và ghi rõ).

Clone master 3b647461db7c8ded1bddd9aafc5c6aa5eead223f, cộng chưa commit: đặc tả cần review; `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1-ban2.md` là bản bạn review lượt 2; verdict lượt 1 và 2 ở `ops/reviews/wp433p2a-spec/luot1.verdict.txt`, `luot2.verdict.txt`; đặc tả và review packet 1 (`ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md`, `ops/reviews/wp433-spec-r1/`).

Phạm vi và quyết định chủ kho (§2, §9: P2b, P2c, Q2 thu hẹp áp cho P2c, Q4 reparse xếp P2c) là ràng buộc; Q3 chặn lease không chặn review — không nêu.

Việc:
1. Diff với `-ban2.md`. Với từng finding lượt 2 (6 P2, 2 P3): đã đóng THẬT chưa — đo bằng chạy mã khi được (ví dụ `_safe_exc` trên `OSError`/`FileExistsError`/`IsADirectoryError`; `_kiem_dich_ghi` với `goc` thô `.../alias/` so với `goc="/"`; topology fragment dev của selftest).
2. §4b (30 đột biến): với MỖI đột biến, chỉ chạy ca đích, theo thứ tự lượt và thứ tự nhãn đã khai — lượt/nhãn ĐẦU TIÊN đỏ có đúng là đích không (đặc biệt 3, 4, 19, 36, 37, 42–45); không hai đột biến chung (ca, lượt, nhãn); tổng đếm; tự kiểm N9(c).
3. Phần mới: ca gộp nhiều lượt (`trong_kho`, `goc_bieu_dien`, `chuoi_kho`), tách `m1_bien`/`bien_cfgdir`, nhãn `tiem` đọc nhật ký bộ quan sát, đếm lượt bỏ qua trên nền khác ở N9 — có tự mâu thuẫn hay lỗ đo nào không.
4. L1–L7 `.claude/skills/soan-spec/SKILL.md`: mỗi N có phép đỏ độc lập; mọi chốt là danh sách CHO PHÉP.
5. §8 ước lượng (408–479, giữa ~443) có hợp lý so với trần 450 theo mật độ fragment packet 1.

Không nêu lại finding đã đóng. Đầu ra stdout: bảng finding lượt 2 (đóng / chưa), finding mới P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
