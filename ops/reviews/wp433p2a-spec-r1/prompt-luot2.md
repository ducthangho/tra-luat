Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 2, cho đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (packet P2a, Issue #433). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master 3b647461db7c8ded1bddd9aafc5c6aa5eead223f (đã có mã packet 1: `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600` trong `scripts/tl_gws.py`, fragment `scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py`), cộng chưa commit: đặc tả cần review; `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1-ban1.md` là bản bạn review lượt 1; verdict lượt 1 ở `ops/reviews/wp433p2a-spec/luot1.verdict.txt` (request_changes: 2 P1, 7 P2, 2 P3); `ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md` và `ops/reviews/wp433-spec-r1/` (packet 1).

PHẠM VI ĐÃ THU HẸP (quyết định chủ kho sau lượt 1, ghi §9 Q1 tầng hai và Q2): P2a = W4/W5 trên POSIX + chốt thư mục tổ tiên của `cfgdir`. Danh sách cho phép đường Windows, UNC (chốt bằng so định danh volume+file id với gốc kho tra-luat) chuyển sang P2c. Vì vậy các finding lượt 1 sau đây KHÔNG còn thuộc P2a và không được nêu lại là finding của P2a (chỉ kiểm rằng §2 "Để P2c" đã ghi chúng): P1 "UNC ngoài kho", P2 "dạng đường M1 / dòng 32 / isabs(\\fake)". Q4 (vế reparse M6 xếp sang P2c) là lựa chọn của phiên soạn, ghi ở §9: chỉ nêu finding nếu việc xếp ấy làm P2a SAI hoặc không tự đứng được, không tranh luận việc ưu tiên. Q3 (uỷ quyền bundled) chặn lease không chặn review — không nêu.

Các finding lượt 1 THUỘC P2a phải được ĐÓNG THẬT trong bản này: P1 tổ tiên `cfgdir`; P2 biên `cfgdir`; P2 TOCTOU (khai đúng); P2 fsync + tiêm lỗi theo pha; P2 nhãn/fullmatch/đếm stderr; P2 tự kiểm (nay N9) theo ID/lượt/nền; P2 phản chứng gate (nay N8, N10–N12); P3 §2 phụ thuộc; P3 căn cứ §8.

Việc:
1. Diff bản này với `-ban1.md`. Với từng finding lượt 1 thuộc P2a: đã đóng thật chưa (đo bằng đọc/chạy mã khi được: ví dụ dựng tổ tiên symlink trong /tmp và gọi `_kiem_dich_ghi(dest, "/", tp)` của base để xác nhận luật (b) phủ tổ tiên; kiểm `_ghi_nguyen_tu_0600` thật sự ném/dọn ở từng pha mkstemp/fsync/chmod/replace như N7 giả định).
2. Kiểm lời khai mới ở §0 (B1, §0.4 về luật (b) và writer, dòng §0.1 của `--require-agent-creds`) bằng chạy mã.
3. §4b: với MỖI đột biến, theo thứ tự lượt và thứ tự nhãn đã khai, lượt ĐẦU TIÊN nó làm đỏ có đúng là lượt/nhãn đích không (đặc biệt 12, 15, 16, 19, 20, 21, 23, 33–42); hai đột biến chung (ca, lượt, nhãn) phải có vế riêng; tổng đếm (29; E 5; posix 17; mọi 12) đúng; tự kiểm N9(c) đổi đúng một biến.
4. Hệ quả hành vi của chốt tổ tiên (§8: tổ tiên symlink như /var, /tmp macOS bị từ chối) và nhánh `os.name != "posix"` (không chốt) — có làm P2a sai hay tự mâu thuẫn với M2/M3/N không; ca nền `mọi` có chạy được trên Windows khi chốt bị bỏ qua không.
5. Theo L1–L7 `.claude/skills/soan-spec/SKILL.md`: mỗi N có phép đỏ; mọi chốt là danh sách CHO PHÉP.
6. §8 ước lượng (410–481, giữa ~446) có hợp lý so với trần 450 theo mật độ fragment packet 1 (353 dòng, 18 ca, 30 `_DB`, +448).

Đầu ra stdout: bảng finding lượt 1 (đã đóng / chưa / chuyển P2c đúng), finding mới P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
