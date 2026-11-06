# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r9 — lượt 9 (lượt XÁC MINH duy nhất, `6691581371`, lặp tới khi sạch)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv9/cay-kho`, detached tại reviewed_sha `3408591b7b318578a17c9b1ba00c1b87cee4f688` (đã merge `origin/master` `d26b36f5…`; merge không đụng spec). Số đo spec neo base `889334fb87c25136a13c6776a40a25b401820e04`.
  READ-ONLY: `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong cây. Lượt này chạy KHÔNG có quyền ghi ngoài thư mục làm việc của bạn.
- Tệp review: `ops/specs/wp1179-c1a1b-r9.md` (sha256 `c9bc8acac6710f8395b4ca88c69ef39dfaa1b3acbf468aa0eea2b3f7d530ef74`).
  Lịch sử r1–r8 cùng thư mục; verdict lượt 1–8 và evidence/probe ở `ops/specs/wp1179-c1a1b-r1-do/review-luot{1,2-r2,3-r3,4-r4,5-r5,6-r6,7-r7,8-r8}/`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv9/sandbox` (thư mục hiện tại). Muốn dùng probe cũ thì chép vào đây rồi chạy.

## Bối cảnh
Chủ kho (#1179 comment 6686369822): lặp vá spec, mỗi vòng một lượt Codex độc lập, tới khi MỘT lượt cho 0 P1 / 0 P2 / 0 P3; trần lời gọi 10→16, pha spec tối đa 4 lượt (đã dùng hết 4; chủ kho cho thêm tối đa 2 — đã thêm 2; chủ kho cho thêm 1 lượt xác minh r9, comment 6691581371 — lượt này), pha thi công 3. Quyết định giữ: trần kích thước ≤2 tệp/≤750 dòng; F6 theo nhánh "so OID trước"; phạm vi C1a1b.
Lượt 8 (trên r8) còn F19 P2 `dot-bien-tuong-duong-hoac-thieu`: (a) đột biến "reader chết là lỗi cục bộ" sống trên ca A12(e), ca (h) phân biệt được; (b) đột biến "đánh giá lại luật đã hoàn tất" của A12(f) không đổi vector, đột biến đúng là "ghi đè kết quả đã hoàn tất thành unknown". Chủ kho cho r9 CHỈ vá cơ học hai điểm ấy ở cột đột biến A12 và thêm hai đường vào danh sách cùng lớp (§0.10); oracle không đổi.

## Nhiệm vụ
1. Xác minh F19 đã vá thật: trên đồ thị thật và reader prototype, đột biến "lỗi cục bộ, không restart" bị ca A12(h) giết; đột biến "ghi đè kết quả đã hoàn tất" bị A12(f) giết; restart vẫn bị (e)/(h) giết; xoá memo vẫn bị (f2) giết. Kiểm diff r8→r9 không đổi oracle nào.
2. Review TOÀN BỘ r9 theo LỚP (ADR-0060 M2), không chỉ phần đổi: ABI/rc, bảng đóng §2.3 × G6/G7/G8, N6, §2.6, §3, A1–A23 (cả A20b), §8/§11 so với ADR-0043/0052/0055/protocol §12, nội nhất quán. Mọi biểu hiện, kể cả P3.
3. Đo lại các con số đo được. Prototype nhỏ trong sandbox được phép; ghi lệnh/rc/output.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv9/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F19; bảng lớp; finding mới `F<n>` (đánh số từ F20; mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất cụ thể); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`. Chỉ `approve` khi 0/0/0.
