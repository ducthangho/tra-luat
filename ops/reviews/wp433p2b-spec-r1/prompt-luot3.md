Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 3, cho đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-B-r1.md` (packet P2b, Issue #433: kiểm dữ liệu W6 trong `cmd_bootstrap`). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM (`/dev/shm` nếu /tmp chỉ đọc) và ghi rõ.

Clone master 11bd0336d00b4a9544e70dcbbe049d372053a3ec, cộng chưa commit: đặc tả cần review (bản 3); `ops/specs/GWS-CRED-DICH-NGOAI-KHO-B-r1-ban2.md` là bản bạn review lượt 2 (sha256 c63c1166…); verdict lượt 1, 2 ở `ops/reviews/wp433p2b-spec-r1/luot{1,2}.verdict.txt`. Script đo ở `ops/reviews/wp433p2b-spec-r1/do/`: `va_ung_vien.py` (dựng nguồn ứng viên prototype bản 2), `do_dot_bien2.py` (bộ chạy tạm 3 ca / 29 lượt / 36 đột biến: `python3 -I do_dot_bien2.py <scripts> <tl_gws ứng viên>`; thêm `--base` để chỉ chạy nền), `do_locale.py` (L1–L3; L1 cần chạy KHÔNG `-I` với `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`), `chay_frag.py`, các `.txt` là output đã ghi.

Quyết định chủ kho là RÀNG BUỘC: phạm vi P2b; Windows/UNC thuộc P2c; §9 Q1 chặn lease không chặn review — không nêu; Q2, Q3 là câu hỏi mở.

Việc:
1. Diff với bản 2. Hai finding lượt 2 (P2 N1b chỉ đo chiều từ chối; P2 M3(c) chưa đo giữ `TL_WEBAPP`): đã đóng THẬT chưa — dựng lại đúng phản chứng bạn đã dùng (ép ASCII khi hàm báo `utf-8`; khôi phục `TL_WEBAPP` trong `except`) trên nguồn ứng viên và bộ chạy mới, xem có đỏ đúng (ca, lượt, nhãn) khai ở §4b dòng 35, 36 không.
2. Sửa có làm vỡ chỗ khác không: đẳng thức N3(c) (3 ca, 29 lượt, 36 đột biến; nền khác `w=1, t=2, v=4`), tổng E 8 / H 28 / posix 4, nhãn `env_token`/`env_web`, `tien_de`, thứ tự lượt, §8.
3. Chỉ nêu finding MỚI nếu là lỗ đo hoặc tự mâu thuẫn có bằng chứng chạy được; không nêu lại finding đã đóng.

Đầu ra stdout: bảng finding lượt 1 (đóng / chưa, kèm phép đo), finding mới P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
