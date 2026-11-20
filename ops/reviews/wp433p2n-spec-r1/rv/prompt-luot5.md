Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp (sandbox có thể chặn thư mục tạm mặc định — dùng TMPDIR=/dev/shm).

Đây là LƯỢT 5. Thư mục làm việc: clone kho tra-luat, HEAD tách ở master 8a72d28d7a413047733277545fc8547f32010593 (tree df0bbe85…), đủ lịch sử và mọi `refs/remotes/origin/*` — dùng `git` để đo lại mọi con số. Cộng (chưa commit):
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-N-r1.md` — ĐẶC TẢ CẦN REVIEW, bản đã sửa sau lượt 4.
- `ops/reviews/wp433p2n-spec-r1/luot1.verdict.txt`, `luot2.verdict.txt`, `luot3.verdict.txt`, `luot4.verdict.txt` — kết luận lượt 1–4 của bạn (lượt 4: 1 P2, 2 P3).
- `ops/reviews/wp433p2n-spec-r1/nguyen-mau/` — NGUYÊN MẪU M2–M4 do phiên điều phối dựng để đo (không phải mã thi công): `ap_proto.py` áp vào bản sao `tl_gws.py`, `nguyen-mau.diff`, `do_neo.py` (đếm neo `_DB`/`_TU_KIEM` của năm fragment base vs bản sao), `chay_fr.py` (chạy `run` năm fragment), `ket-qua-linux.txt` (đầu ra đã đo). Hãy TỰ CHẠY lại: dựng hai bản sao của cây ở `/dev/shm`, áp `ap_proto.py` vào một bản, rồi chạy `do_neo.py` và `chay_fr.py` (cwd = gốc từng bản sao), và `ops/reviews/wp433p2n-spec-r1/tai_hien.py` trên bản nguyên mẫu.
- Bằng chứng §0 cũ: `tai_hien.py`, `probe433n.py`, `desktop-wp433n-out-20261120T012952Z/`.
- Khuôn đã land: đặc tả R/C1 trên nhánh `origin/ops/wp433-p2r-spec`, `origin/ops/wp433-p2c-spec`; fragment R, C1, P2a, P2b, packet 1 trong `scripts/test_fragments/wp433_*`.

Quyết định ĐÃ CHỐT của chủ kho (không review lại lựa chọn): Q1 sửa test; Q2 = A chốt từ gốc (chấp nhận từ chối HOME có tổ tiên liên kết); Q3 bundle không phải dict ⇒ rc 3; Q5 áp cho jar NLM W1–W3. Không có Windows ở đây: hành vi native là lời khai cần ĐO (§4c). Đừng tự soạn đường dẫn dựng để thoát khỏi cây thư mục hay nội dung credential kiểu tấn công — hướng thử cần loại nội dung ấy thì MÔ TẢ BẰNG LỜI.

Việc:
1. Từng finding lượt 4 (và phần còn mở trước đó): đã đóng chưa (bằng chứng chạy được), còn mở gì.
2. Thiết kế M2 mới (`_chot_thu_muc`, chèn dòng, không sửa dòng neo): có bỏ sót tổ tiên nào (HOME tương đối? `~` không giải được? HOME ở gốc ổ nt?), có trùng/thiếu kiểm `.git` so với lời gọi tệp hiện hành, nhánh nt có nhất quán với C1 (`_duong_dich_chuan_nt`, loại ổ) không; thứ tự trong W6 (chốt trước mọi đọc) đúng không; `_dich_jar_nlm` trả lý do cuối có làm đổi cụm/thông báo ở W1–W3 trên ca base nào không.
3. N2–N5, §4b, D2–D4 sau sửa: mỗi tiêu chí/đột biến có phép làm đỏ, đích phân biệt, không tín dụng giả; đột biến 1/4 neo trọn dòng chèn có khớp đúng 1 lần trên NGUYÊN MẪU.
4. Kích thước §8 (~241–292) so với nguyên mẫu (+32/−2 cho `tl_gws.py`; nguyên mẫu CHƯA có nhánh gốc ổ nt — đó là phần +4–8 ước thêm).

Một finding chỉ nên nêu khi nó làm sai một tiêu chí/đột biến/phép đo cụ thể; đừng nêu đề xuất làm chặt thêm mà đặc tả đã khai là giới hạn ở §2/§8.

Đầu ra stdout: bảng đóng finding lượt 4, bảng kiểm sự thật, finding mới P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
