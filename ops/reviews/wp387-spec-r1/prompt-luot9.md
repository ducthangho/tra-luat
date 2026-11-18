Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 9 (trần 10), cho đặc tả packet A `ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md` (Issue #387), chưa có mã. Packet B `ops/specs/LAUNCHER-BAM-LOG-NEN-DARWIN-WINDOWS-r1.md` không review. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM (/dev/shm).

Worktree master 641108c. `-r1-ban8.md` là bản A bạn review lượt 8 (A: P2 N4 đòi OK cho mục kế thừa `124_khi_chau_con_song` vốn KHONG DO DUOC trên Linux). Bản hiện tại chỉ sửa N4 (+§0/§9): cho phép đúng sáu mục KHONG DO DUOC kế thừa base (năm `windows` + `124_khi_chau_con_song`), dòng cuối runner phải `DOT BIEN: N/N dat  (6 khong do duoc tren nen nay)`; rà toàn bảng base ghi ở §0.

Việc — CHỈ: (1) Kiểm finding lượt 8 đã đóng (đối chiếu DOT_BIEN base: đúng sáu mục KHONG DO DUOC trên Linux, không thiếu không thừa; con số 6 khớp cách runner đếm). (2) Diff ban8 → bản hiện tại không đưa lỗi P0–P2 mới. Không mở lại phần đã đóng.

Đầu ra stdout: bảng finding lượt 8 (đóng/chưa), finding mới P0–P3 chỉ trong phần đã đổi. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Approve khi packet A không còn P0–P2.
