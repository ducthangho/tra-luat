Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 2, cho đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-B-r1.md` (packet P2b, Issue #433: kiểm dữ liệu W6 trong `cmd_bootstrap`). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM (`/dev/shm` nếu /tmp chỉ đọc) và ghi rõ.

Clone master 11bd0336d00b4a9544e70dcbbe049d372053a3ec, cộng chưa commit: đặc tả cần review (bản 2); `ops/specs/GWS-CRED-DICH-NGOAI-KHO-B-r1-ban1.md` là bản bạn review lượt 1 (sha256 cd88fbe9…); verdict lượt 1 ở `ops/reviews/wp433p2b-spec-r1/luot1.verdict.txt`. Script đo ở `ops/reviews/wp433p2b-spec-r1/do/`: `va_ung_vien.py` (dựng nguồn ứng viên prototype bản 2), `do_dot_bien2.py` (bộ chạy tạm 3 ca / 28 lượt / 34 đột biến: `python3 -I do_dot_bien2.py <scripts> <tl_gws ứng viên>`; thêm `--base` để chỉ chạy nền), `do_locale.py` (L1–L3; L1 cần chạy KHÔNG `-I` với `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`), `chay_frag.py`, các `.txt` là output đã ghi.

Quyết định chủ kho là RÀNG BUỘC: phạm vi P2b; Windows/UNC thuộc P2c; §9 Q1 chặn lease không chặn review — không nêu; Q2, Q3 là câu hỏi mở.

Việc:
1. Diff với bản 1. Bảy finding lượt 1 (4 P2, 3 P3): đã đóng THẬT chưa — dựng lại chính phép đo bạn đã dùng (locale ASCII trong tiến trình con, NaN/Infinity, `load_creds` thật đặt env trước W6, nhánh code/cowork, `--require-agent-creds` rc 1/4, dòng jar, bốn đột biến chạm/đọc/ghi/lộ TOK từng `SONG_SOT`, đảo hai lượt) trên nguồn ứng viên bản 2 và bộ chạy mới.
2. Sửa có làm vỡ chỗ khác không: đẳng thức N3(c) (3 ca, 28 lượt, 34 đột biến, `chỉ_posix` trên nền khác 1/1/3), tổng E 8 / H 26 / posix 3, tập khai theo lượt, thứ tự nhãn, mốc "trước", giả lập `sys.getfilesystemencoding` có thật sự đo được điều M1 hứa không, và hai fragment kề bên (đọc `run`, không đọc rc).
3. Chỉ nêu finding MỚI nếu là lỗ đo hoặc tự mâu thuẫn có bằng chứng chạy được; không nêu lại finding đã đóng. Đừng tự soạn đường dẫn hệ tệp bất thường — mô tả bằng lời nếu cần.

Đầu ra stdout: bảng finding lượt 1 (đóng / chưa, kèm phép đo), finding mới P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
