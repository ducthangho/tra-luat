Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 4, cho đặc tả `ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md` (Issue #387), chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong bản sao dưới /tmp (git archive). Không chạy toàn bộ launcher_test; ưu tiên `--lap-ca`.

Worktree master 641108c. `ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1-ban3.md` là bản bạn review lượt 3 (request_changes: P2 dọn fixture bằng PID trần có thể giết nhầm; P2 N5 L3 hai cách chạy native khác quy tắc; P3 M2 thời gian ngủ sau lần dò). Bản hiện tại là bản sửa (§9). Thêm: §6/§8 chốt giữ một packet, không xin nâng trần; numstat >450 trước review ⇒ dừng, revision tách A/B (bản vá thử đo 361 dòng thêm).

Việc: (1) `diff` hai bản; kiểm ba finding lượt 3 đã đóng thật — đặc biệt khoá danh tính `_khoa_danh_tinh(pid)` trong `.claude/dev/launcher.py` (có thật không, so gì, Windows/Linux), ca (z) và đột biến `r387_don_chau_bo_kiem_danh_tinh`. (2) Tìm lỗ mới do các sửa này gây ra. (3) Luật trần/tách mới có nhất quán, phương án A có tự khai các nhánh Darwin/Windows chưa có ca đo. (4) Rà L1–L7.

Đầu ra stdout: bảng finding lượt 3 (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
