Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Thư mục làm việc: clone kho tra-luat ở master 96b6a33d770f7539a3eacbebdc215f87ded4ea7f (đã chứa P2a của #433 trong `scripts/tl_gws.py`; fragment `scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py`, `wp433_nlm_gws_dich_ngoai_kho.py`), cộng (chưa commit):
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-R-r1.md` — ĐẶC TẢ CẦN REVIEW (packet R: thêm vế reparse point — bit `FILE_ATTRIBUTE_REPARSE_POINT` của `os.lstat` — vào thân `_kiem_dich_ghi`, áp cho mọi người gọi). R phụ thuộc packet C1 đã land.
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-C1-r1.md` — đặc tả C1 (tiền đề, đang review riêng; chỉ đọc để hiểu nhánh nt mà R đi qua — đừng review C1).
- `ops/reviews/wp433p2c-spec-r1/dac-ta-ban4.md`, `luot1–3.verdict.txt` — đặc tả gộp trước khi tách và ba lượt review; vế reparse là M4/N3/N4r/§4b 34–37 ở đó. Chủ kho đã bỏ phần định danh tệp/UNC; finding về miền định danh không áp cho R.
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` — đặc tả P2a (khuôn).

Ràng buộc: chủ kho Q7 — R chỉ cam kết các entry mà `os.lstat` báo bit 1024, không dùng API khác; mount point đo tuỳ chọn bằng shell ADMIN do chủ kho chạy. Không có Windows ở đây: hành vi native là lời khai cần ĐO (§4c); kiểm phép đo được mô tả có đủ làm đỏ/xanh lời khai không. Đừng tự soạn đường dẫn dựng để thoát khỏi cây thư mục — mô tả hướng thử bằng lời.

Đọc: đặc tả R; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `scripts/tl_gws.py` (`_kiem_dich_ghi` 1173–1187 và các người gọi 1210, 1233, 1784); hai fragment wp433 (neo); `docs/adr/0053*`, `0055*`, `0067*`; `docs/PROTOCOL_DA_PHIEN.md` §10.1.

Việc:
1. Kiểm lời khai §0 (dòng, neo, người gọi, hành vi POSIX không đổi) bằng đọc/chạy (có thể áp thử M1 vào bản sao trong RAM và chạy hai fragment wp433 trên Linux).
2. M1 có đúng phạm vi (mọi người gọi, đúng tiền tố họ truyền), có đổi hành vi POSIX hay phá neo nào không.
3. N1–N5, §4b: mỗi tiêu chí có phép làm đỏ; đột biến 1–3 có đích phân biệt và đúng; giả lập `os.lstat` có làm mù phép đo không (vd. so đường sau `normcase(normpath)` khớp được đúng chuỗi người gọi truyền trên POSIX và Windows); tự kiểm N3 có răng; sổ 7 lượt và đẳng thức theo nền đúng.
4. §4c: D2/D3/D4 đủ để phân biệt junction/symlink/mount point, có vế âm, nhánh KHÔNG ĐO ĐƯỢC rõ; điều kiện dừng §6 đo được.
5. Kích thước §8 (184–219) hợp lý.

Một finding chỉ nên nêu khi nó làm sai một tiêu chí/đột biến/phép đo cụ thể; đừng nêu đề xuất làm chặt thêm mà đặc tả đã khai là giới hạn ở §2/§8.

Đây là LƯỢT 3: các bản trước và verdict ở `ops/reviews/wp433p2c-spec-r1/r/dac-ta-luot{1,2}.md`, `r/luot{1,2}.verdict.txt`. Việc đầu tiên: kiểm từng finding lượt 2 đã đóng thật chưa (bảng finding → trạng thái → bằng chứng), rồi mới tìm finding mới.

Đầu ra stdout: bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
