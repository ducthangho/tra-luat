# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r5 — lượt 5 (pha spec 3/4, lặp tới khi sạch)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv5/cay-kho`, detached tại reviewed_sha `268137452ce1d9e21a4cc635eb9ad4ca7358b57d` (đã merge `origin/master` `d26b36f5…`; merge không đụng spec). Số đo spec neo base `889334fb87c25136a13c6776a40a25b401820e04`.
  READ-ONLY: `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong cây. Lượt này chạy KHÔNG có quyền ghi ngoài thư mục làm việc của bạn.
- Tệp review: `ops/specs/wp1179-c1a1b-r5.md` (sha256 `746c0ef2204eafade6d17933a0050efb8205e9910cf9d82730fb0627f6d3fabd`).
  Lịch sử r1–r4 cùng thư mục; verdict lượt 1–4 và evidence/probe ở `ops/specs/wp1179-c1a1b-r1-do/review-luot{1,2-r2,3-r3,4-r4}/`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv5/sandbox` (thư mục hiện tại). Muốn dùng probe cũ thì chép vào đây rồi chạy.

## Bối cảnh
Chủ kho (#1179 comment 6686369822): lặp vá spec, mỗi vòng một lượt Codex độc lập, tới khi MỘT lượt cho 0 P1 / 0 P2 / 0 P3; trần lời gọi 10→16, pha spec tối đa 4 lượt (lượt này là thứ 3), pha thi công 3. Quyết định giữ: trần kích thước ≤2 tệp/≤750 dòng; F6 theo nhánh "so OID trước"; phạm vi C1a1b.
Lượt 4 (trên r4) còn F10 P2 `dat-lai-ngan-sach-khi-doi-truc` (U_max gán từ status), F11 P2 `phan-loai-vang-va-khong-do-duoc` (thiếu chốt tên entry rỗng…), F12 P3 `huong-dan-cli-khong-khop-parser`; r5 sửa ở §0.6, §2.3, §8, §11.1, §11.2, A20b, A21, A22, và tự liệt kê các đường cùng lớp ở §0.6.

## Nhiệm vụ
1. Xác minh F10, F11, F12 đã vá thật, và rằng các danh sách đường cùng lớp ở §0.6 là ĐỦ (tự tìm đường bị sót). Đối chiếu tập chốt parser §2.3 với `KhoObject.commit`/`KhoObject.tree` của `ops/lease_publish.py` tại base (không thiếu, không thừa). Chạy lại các lệnh CLI §11.2/A22 trên state giả trong sandbox.
2. Review TOÀN BỘ r5 theo LỚP (ADR-0060 M2), không chỉ phần đổi: ABI/rc, bảng đóng §2.3 × G6/G7/G8, N6, §2.6, §3, A1–A22 (cả A20b), §8/§11 so với ADR-0043/0052/0055/protocol §12, nội nhất quán. Mọi biểu hiện, kể cả P3.
3. Đo lại các con số đo được. Prototype nhỏ trong sandbox được phép; ghi lệnh/rc/output.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv5/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F10–F12; bảng lớp; finding mới `F<n>` (đánh số từ F13; mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất cụ thể); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`. Chỉ `approve` khi 0/0/0.
