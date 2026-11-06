# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r4 — lượt 4 (pha spec 2/4, lặp tới khi sạch)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv4/cay-kho`, detached tại reviewed_sha `3646365f965478fbe79be4a975f4eb3075ab405d` (đã merge `origin/master` `d26b36f5…`; merge không đụng spec). Số đo spec neo base `889334fb87c25136a13c6776a40a25b401820e04`.
  READ-ONLY: `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong cây. Lượt này chạy KHÔNG có quyền ghi ngoài thư mục làm việc của bạn.
- Tệp review: `ops/specs/wp1179-c1a1b-r4.md` (sha256 `348340b05edf987d6de1ac504407c9065bfcd2c2c3db15c5f029126596d40188`).
  Lịch sử r1–r3 cùng thư mục; verdict lượt 1–3 và evidence/probe ở `ops/specs/wp1179-c1a1b-r1-do/review-luot{1,2-r2,3-r3}/`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv4/sandbox` (thư mục hiện tại). Muốn dùng probe cũ thì chép vào đây rồi chạy.

## Bối cảnh
Chủ kho (#1179 comment 6686369822): lặp vá spec, mỗi vòng một lượt Codex độc lập, tới khi MỘT lượt cho 0 P1 / 0 P2 / 0 P3; trần lời gọi 10→16, pha spec tối đa 4 lượt (lượt này là thứ 2), pha thi công 3. Quyết định giữ: trần kích thước ≤2 tệp/≤750 dòng; F6 theo nhánh "so OID trước"; phạm vi C1a1b.
Lượt 3 (trên r3) còn F9 P2 `dat-lai-ngan-sach-khi-doi-truc`; r4 sửa ở §0.5, §8, §11.1, §11.2, §10, A21.

## Nhiệm vụ
1. Xác minh F9 đã vá thật, và rằng sáu đường cùng lớp liệt kê ở §0.5 là ĐỦ (tự tìm đường thứ bảy nếu có). Thử quy tắc §8 và A21 bằng bộ đếm thật của `packet_loop.py` trong state giả ở sandbox (như lượt 3).
2. Review TOÀN BỘ r4 theo LỚP (ADR-0060 M2), không chỉ phần đổi: ABI/rc, bảng đóng §2.3 × G6/G7/G8, N6, §2.6, §3, A1–A21, §8/§11 so với ADR-0043/0052/0055/protocol §12, nội nhất quán. Mọi biểu hiện, kể cả P3.
3. Đo lại các con số đo được. Prototype nhỏ trong sandbox được phép; ghi lệnh/rc/output.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv4/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F9; bảng lớp; finding mới `F<n>` (đánh số từ F10; mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất cụ thể); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`. Chỉ `approve` khi 0/0/0.
