Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Thư mục làm việc: clone kho tra-luat ở master 96b6a33d770f7539a3eacbebdc215f87ded4ea7f (đã chứa P2a của #433: `_duong_dich_chuan`, `_dich_cred_gws`, `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_trong_kho_git` trong `scripts/tl_gws.py`; fragment `scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py` và `wp433_nlm_gws_dich_ngoai_kho.py`), cộng (chưa commit):
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-C1-r1.md` — ĐẶC TẢ CẦN REVIEW (packet C1: nhánh Windows của W4/W5 — danh sách cho phép đường Windows thuần `ntpath`, UNC và ổ mạng LUÔN bị từ chối, nối vào `_kiem_dich_ghi`).
- `ops/reviews/wp433p2c-spec-r1/dac-ta-ban4.md` và `luot1–3.verdict.txt` — đặc tả GỘP P2c trước khi tách và ba lượt review của nó. Đây là LƯỢT 5 trong chuỗi ấy; lượt 4 (trên bản C1 trước) ở `ops/reviews/wp433p2c-spec-r1/c1/luot4.verdict.txt`, bản ấy ở `c1/dac-ta-luot4.md`. Chủ kho đã quyết (19-11 ~10:50Z): bỏ hẳn đích qua mạng (UNC, ổ mạng) — phần định danh tệp/C2 và mọi finding về miền định danh SMB KHÔNG còn áp dụng; tách C1 (đặc tả này) và R (vế reparse, đặc tả riêng). Việc đầu tiên: kiểm từng finding LƯỢT 4 đã đóng thật chưa (bảng finding → trạng thái → bằng chứng); với các finding lượt 1–3 thuộc phần đường/C1 chỉ cần xác nhận không tái phát (luật thành phần, Unicode biên, thứ tự kiểm, loại ổ, `subst`, rig D, T3, numstat, neo `tu_kiem_neo_lap`, đột biến 22/q-mặc định…), lập bảng finding → còn áp dụng không → đã đóng trong C1 chưa → bằng chứng.
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` — đặc tả P2a đã land (khuôn).
- `ops/reviews/wp433p2c-spec-r1/c1/nguyen-mau/` — nguyên mẫu bộ phân loại M1/M2 (`nguyen_mau_c1_r2.py`, đầu ra `nm-r2-out-3.1x.txt`), bộ chạy đột biến kiểm lượt đích `do_dot_bien_c1_r2.py` (rc ≠ 0 khi lệch), kết quả `dot-bien-r2-3.1x.txt`; tệp không hậu tố r2 là của bản trước, đo `ntpath` (`do_ntpath.py`, `ntpath-3.1x.txt`). CHẠY lại được (python3.11/3.12/3.13 có trên máy).

Ràng buộc (không tranh luận; chỉ nêu finding nếu KHÔNG thực hiện được như mô tả): quyết định chủ kho — UNC và ổ mạng bị từ chối hẳn; Q4–Q7 theo mặc định đề xuất (luật thành phần chặt, `COM0` bị chặn, khoảng trắng đầu/NBSP/DEL được nhận, R chỉ cam kết những gì `lstat` báo); lệnh shell ADMIN do chủ kho tự chạy. Không có Windows ở đây: hành vi native là lời khai cần ĐO (§4c); hãy kiểm phép đo được mô tả có đủ để làm đỏ/xanh lời khai không. Đừng tự soạn đường dẫn dựng để thoát khỏi cây thư mục — mô tả hướng thử bằng lời.

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `scripts/tl_gws.py` (W4 ~1803–1823, W5 ~1961–1968, `_kiem_dich_ghi` 1173–1187, `_dich_cred_gws` 1201–1210, `_trong_kho_git` 1119–1139); hai fragment wp433 (neo đột biến); `docs/adr/0053*`, `0055*`, `0067*`; `docs/PROTOCOL_DA_PHIEN.md` §10.1.

Việc:
1. Bảng finding lượt 4 (và xác nhận lượt 1–3 không tái phát).
2. Kiểm từng lời khai sự thật §0 bằng đọc/chạy; chạy lại nguyên mẫu và bộ đột biến; ghi lệch.
3. M1/M2: có đúng là danh sách CHO PHÉP; còn đường vào nào để một đích lọt (dạng Windows chưa có lượt, thứ tự kiểm tạo vùng mù, `cwd` lạ, ổ mạng đến từ `cwd`); mỗi mã có đột biến riêng làm đỏ ĐÚNG lượt khai không.
4. M3: nối nhánh nt có giữ neo §0.4 (đếm thử văn bản đề xuất), có phá fragment P2a/packet 1 trên nt không; `subst`/8.3 dựa vào `realpath` có được đo bắt buộc trước land.
5. Theo L1–L7: mỗi N có phép làm đỏ; §4b đánh số, đích, tổng đếm, nền đúng; tự kiểm N4 còn răng, đẳng thức `h == u ≤ 1` đúng; sổ 72 lượt khớp bảng; §4c đủ cụ thể để phiên khác chạy (lệnh, kỳ vọng, nhánh KHÔNG ĐO ĐƯỢC, lệnh ADMIN nguyên văn), điều kiện dừng §6 đo được.
6. Kích thước §8 (348–417) so với mốc P2a (+438: `git diff --numstat 417b593^1 417b593`) và trần 450.

Một finding chỉ nên nêu khi nó làm sai một tiêu chí/đột biến/phép đo cụ thể (ghi rõ cái nào sai và vì sao); đừng nêu đề xuất làm chặt thêm mà đặc tả đã khai là giới hạn ở §2/§8.

Đầu ra stdout: bảng finding cũ, bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
