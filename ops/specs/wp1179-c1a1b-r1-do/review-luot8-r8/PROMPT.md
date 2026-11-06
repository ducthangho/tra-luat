# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r8 — lượt 8 (lượt thêm 2/2, LƯỢT CUỐI, `6690435193`, lặp tới khi sạch)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv8/cay-kho`, detached tại reviewed_sha `caa5a0ec6a6bbc699c70dcfbd2541cb9ac9aec73` (đã merge `origin/master` `d26b36f5…`; merge không đụng spec). Số đo spec neo base `889334fb87c25136a13c6776a40a25b401820e04`.
  READ-ONLY: `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong cây. Lượt này chạy KHÔNG có quyền ghi ngoài thư mục làm việc của bạn.
- Tệp review: `ops/specs/wp1179-c1a1b-r8.md` (sha256 `24418d1e68ea46324b8bb9a6cecb44eddcf31dd0e0ad0af39a2a2852f0f88454`).
  Lịch sử r1–r7 cùng thư mục; verdict lượt 1–7 và evidence/probe ở `ops/specs/wp1179-c1a1b-r1-do/review-luot{1,2-r2,3-r3,4-r4,5-r5,6-r6,7-r7}/`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv8/sandbox` (thư mục hiện tại). Muốn dùng probe cũ thì chép vào đây rồi chạy.

## Bối cảnh
Chủ kho (#1179 comment 6686369822): lặp vá spec, mỗi vòng một lượt Codex độc lập, tới khi MỘT lượt cho 0 P1 / 0 P2 / 0 P3; trần lời gọi 10→16, pha spec tối đa 4 lượt (đã dùng hết 4; chủ kho cho thêm tối đa 2 — lượt này là thêm 2/2, lượt cuối, comment 6690435193), pha thi công 3. Quyết định giữ: trần kích thước ≤2 tệp/≤750 dòng; F6 theo nhánh "so OID trước"; phạm vi C1a1b.
Lượt 7 (trên r7) còn F17 P2 `phan-loai-vang-va-khong-do-duoc` (deadline vs luật đủ memo mâu thuẫn giữa §2.3 và §2.6/A13) và F18 P2 `dot-bien-tuong-duong-hoac-thieu` (A12 f không phân biệt xoá memo; A13 tổng byte bị root tree lớn che; alias mượn object qua alternate). r8 sửa ở §0.9 (liệt kê đường cùng lớp), §2.3 (bảng phạm vi tài nguyên chung), §2.6, §4 (oracle, alias mới + guard vị trí lưu), A12 (f, f2), A13, A23(e) guard tiền đề.

## Nhiệm vụ
1. Xác minh F17, F18 đã vá thật, và rằng các danh sách đường cùng lớp ở §0.9 là ĐỦ (tự tìm đường bị sót). Dựng đồ thị thật trên MOC theo fixture r8 (gồm biến thể alias mới và biến thể H1 phóng to) và kiểm bằng reader prototype có memo chỉ lưu thành công: bảng phạm vi §2.3; A12 (e, f, f2, g, h); A13 (tổng byte với guard, deadline cùng thời điểm với f2); ca alias với guard vị trí lưu; mỗi guard A23(e) có ca âm; mỗi đột biến khai ở A12/A13/A23 có đổi màu đúng ca đích không.
2. Review TOÀN BỘ r8 theo LỚP (ADR-0060 M2), không chỉ phần đổi: ABI/rc, bảng đóng §2.3 × G6/G7/G8, N6, §2.6, §3, A1–A23 (cả A20b), §8/§11 so với ADR-0043/0052/0055/protocol §12, nội nhất quán. Mọi biểu hiện, kể cả P3.
3. Đo lại các con số đo được. Prototype nhỏ trong sandbox được phép; ghi lệnh/rc/output.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv8/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F17–F18; bảng lớp; finding mới `F<n>` (đánh số từ F19; mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất cụ thể); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`. Chỉ `approve` khi 0/0/0.
