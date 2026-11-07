# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r6 — lượt 6 (pha spec 4/4, lượt CUỐI, lặp tới khi sạch)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv6/cay-kho`, detached tại reviewed_sha `b439048e4ffe15eed0202b0a91b82be2750041af` (đã merge `origin/master` `d26b36f5…`; merge không đụng spec). Số đo spec neo base `889334fb87c25136a13c6776a40a25b401820e04`.
  READ-ONLY: `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong cây. Lượt này chạy KHÔNG có quyền ghi ngoài thư mục làm việc của bạn.
- Tệp review: `ops/specs/wp1179-c1a1b-r6.md` (sha256 `a76b3e98761da2f1e589b73aa8b8b11fe8934c84887190582c9d04b1ab7cc7e2`).
  Lịch sử r1–r5 cùng thư mục; verdict lượt 1–5 và evidence/probe ở `ops/specs/wp1179-c1a1b-r1-do/review-luot{1,2-r2,3-r3,4-r4,5-r5}/`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv6/sandbox` (thư mục hiện tại). Muốn dùng probe cũ thì chép vào đây rồi chạy.

## Bối cảnh
Chủ kho (#1179 comment 6686369822): lặp vá spec, mỗi vòng một lượt Codex độc lập, tới khi MỘT lượt cho 0 P1 / 0 P2 / 0 P3; trần lời gọi 10→16, pha spec tối đa 4 lượt (lượt này là thứ 4, lượt cuối), pha thi công 3. Quyết định giữ: trần kích thước ≤2 tệp/≤750 dòng; F6 theo nhánh "so OID trước"; phạm vi C1a1b.
Lượt 5 (trên r5) còn F13 P2 `phan-loai-vang-va-khong-do-duoc` (A20b gán sai luật đích G8), F14 P2 `dot-bien-tuong-duong-hoac-thieu` (chốt t2 bị t3/t5 che), F15 P3 `huong-dan-cli-khong-khop-parser` (lệnh init sót ở §8); r6 sửa ở §0.7, §2.2 (thứ tự G0→G9), §4 (luật disposition chung + bảng tập đọc của fixture), A13, A20, A20b, A22, §8, và tự liệt kê đường cùng lớp ở §0.7.

## Nhiệm vụ
1. Xác minh F13, F14, F15 đã vá thật, và rằng các danh sách đường cùng lớp ở §0.7 là ĐỦ (tự tìm đường bị sót). Kiểm bảng tập đọc của fixture §4 bằng đồ thị thật dựng trên MOC (mỗi luật đọc đúng các object ấy theo bảng đóng §2.3), và mọi ví dụ luật đích trong A12/A13/A20/A20b khớp bảng.
2. Review TOÀN BỘ r6 theo LỚP (ADR-0060 M2), không chỉ phần đổi: ABI/rc, bảng đóng §2.3 × G6/G7/G8, N6, §2.6, §3, A1–A22 (cả A20b), §8/§11 so với ADR-0043/0052/0055/protocol §12, nội nhất quán. Mọi biểu hiện, kể cả P3.
3. Đo lại các con số đo được. Prototype nhỏ trong sandbox được phép; ghi lệnh/rc/output.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv6/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F13–F15; bảng lớp; finding mới `F<n>` (đánh số từ F16; mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất cụ thể); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`. Chỉ `approve` khi 0/0/0.
