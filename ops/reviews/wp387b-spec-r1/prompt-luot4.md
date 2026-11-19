Bạn là reviewer ĐỘC LẬP (họ OpenAI), chỉ đọc, LƯỢT 4. Worktree kho tra-luat ở commit 3b647461db7c8ded1bddd9aafc5c6aa5eead223f. Đối tượng: đặc tả `ops/specs/LAUNCHER-BAM-LOG-NEN-WINDOWS-r1.md` (bản 4, chưa commit). Bản lượt trước: `ops/specs/BAN3-truoc-luot4.md`. Verdict lượt 3 của bạn (5 P2, 2 P3) được tóm tắt ở mục "Lượt 3" của §11.

Việc:
1. `diff -u ops/specs/BAN3-truoc-luot4.md ops/specs/LAUNCHER-BAM-LOG-NEN-WINDOWS-r1.md`; kiểm TỪNG finding lượt 3 đã thực sự đóng, bằng đo/probe trên mã khi cần (thân (e) và `goi()`, `_r387_than_a`/(a′), `_r387_don_dep`, cách runner thay và tách bảng). Ghi rõ finding nào CÒN MỞ.
2. Tìm lỗi MỚI do bản 4 đưa vào: thứ tự (e) mới (e9,e6,e7,e8 trước e1–e5) có làm mutant cũ của A hoặc W1–W6 chết sai nhãn/sống không; (t2) kiểm trace trước; (t3d); `_r387_doi_chung_a` + (t6) + H7; H1–H7 dạng mới; khởi tạo `m._r387_job` và setattr/delattr. Chỉ nêu finding có bằng chứng; phân biệt lỗi chặn đóng băng (đặc tả sai/mâu thuẫn/không đo được) với chi tiết executor tự chốt khi viết mã (đặc tả đã giao rõ cho executor kèm phép đo).
3. L1–L7 (`.claude/skills/soan-spec/SKILL.md`) cho phần đã đổi.

Không sửa tệp nào. Mỗi finding: mức, vị trí, bằng chứng, cách sửa. Kết thúc bằng đúng một dòng cuối: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`.
