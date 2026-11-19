Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Thư mục làm việc: clone kho tra-luat ở master 3b647461db7c8ded1bddd9aafc5c6aa5eead223f (đã chứa mã packet 1 `NLM-GWS-DICH-NGOAI-KHO`: `_kiem_dich_ghi` trong `scripts/tl_gws.py`, fragment `scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py`), cộng (chưa commit):
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` — ĐẶC TẢ CẦN REVIEW (packet P2a, Issue #433: chốt đích ghi credential gws ở W4 `cmd_bootstrap` và W5 `_gws_auth_load`, ngoài cây kho; danh sách cho phép đường Windows; ghi nguyên tử; hợp đồng lỗi; bit reparse-point).
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1-truoc-tach.md` — bản trước khi tách (có W6), để đối chiếu phần đã chuyển sang P2b.
- `ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md` và `ops/reviews/wp433-spec-r1/` — đặc tả packet 1 và 13 lượt review của nó; học các finding đã bắt.
§9 ghi quyết định chủ kho 2026-11-19: Q1 TÁCH (W6 sang P2b `GWS-CRED-DICH-NGOAI-KHO-B`), Q2 CHO PHÉP UNC đủ `\\server\share` (vẫn từ chối `\\?\`, `\\.\`, `\\server` thiếu share). Đó là ràng buộc, không phải đối tượng tranh luận; chỉ nêu finding nếu quyết định KHÔNG thực hiện được như mô tả. Q3 (comment uỷ quyền bundled) còn mở, chặn lease không chặn review — đừng nêu nó là finding.

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `scripts/tl_gws.py` (W4 quanh `cmd_bootstrap` ~1780, W5 `_gws_auth_load` ~1930, `_kiem_dich_ghi` ~1173, `_ghi_nguyen_tu_0600` nếu có, các hằng hợp đồng lỗi); fragment packet 1 và `scripts/tl_test_fragments_bundled.py`; `docs/adr/0053*`, `docs/adr/0063*` (grammar packet_id); `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r1.md` (tiền lệ hậu tố -A).

Việc:
1. Kiểm từng lời khai sự thật §0 (dòng, hàm, hành vi hiện tại của W4/W5, cụm lỗi, đo môi trường) bằng đọc/chạy mã; ghi lệch.
2. Tách P2a/P2b: phần còn lại có tự đứng được không (không ca/đột biến/nghiệm thu nào của P2a còn trỏ M7/N9w6/N3d/W6-dữ-liệu; §4b đánh số và tổng đếm khớp; N8 tự kiểm còn đo được sau khi bỏ dòng 24–29).
3. M1 danh sách CHO PHÉP đường Windows (ổ `X:\…`, UNC `\\server\share\…`, đường POSIX tuyệt đối): có đúng là CHO PHÉP (không phải danh sách cấm) không; liệt kê HẾT đường vào để một đích lọt ra khỏi chốt hoặc rơi vào cây kho: tương đối, `X:` thiếu gạch, `\\?\`, `\\.\`, `\\server` thiếu share, UNC trỏ về chính máy/ổ chứa kho, `..`, gạch trộn `/` `\`, chữ hoa/thường ổ, symlink/junction/reparse ở thành phần trung gian và cuối, TOCTOU giữa kiểm và ghi, đích đã tồn tại là thư mục/symlink, biến môi trường rỗng/khoảng trắng/NUL. Thiếu chốt/ca/đột biến riêng ⇒ finding.
4. M2 ghi nguyên tử 0600 (W4 và W5): tệp tạm cùng thư mục, fsync, replace, dọn tệp tạm khi lỗi, quyền chỉ POSIX — đường nào chưa có ca.
5. Theo L1–L7: mỗi N có phép đo làm nó đỏ đỏ được không; mỗi đột biến §4b có ca đích phân biệt được với đột biến khác (không hai đột biến chung ca đích mà không có vế riêng), cột E/H nhất quán, tổng đếm đúng; tự kiểm bộ phân hạng (tín dụng giả do `except` đổi kiểu, sai lượt) còn có răng.
6. Ước lượng kích thước §8 (369–456, giữa ~412) có hợp lý so với trần 450 dòng thêm — đếm lại theo fragment packet 1 (353 dòng) và numstat của nó.

Đầu ra stdout: bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
