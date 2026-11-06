# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r7 — lượt 7 (lượt thêm 1/2 do chủ kho cấp, `6690435193`, lặp tới khi sạch)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv7/cay-kho`, detached tại reviewed_sha `4f3738ae720fe311a222439307a91307d798d5f3` (đã merge `origin/master` `d26b36f5…`; merge không đụng spec). Số đo spec neo base `889334fb87c25136a13c6776a40a25b401820e04`.
  READ-ONLY: `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong cây. Lượt này chạy KHÔNG có quyền ghi ngoài thư mục làm việc của bạn.
- Tệp review: `ops/specs/wp1179-c1a1b-r7.md` (sha256 `9f9c50b93070838cd3fb6c76a7a10969862d79ee0bc17d1183123345daab56c2`).
  Lịch sử r1–r6 cùng thư mục; verdict lượt 1–6 và evidence/probe ở `ops/specs/wp1179-c1a1b-r1-do/review-luot{1,2-r2,3-r3,4-r4,5-r5,6-r6}/`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv7/sandbox` (thư mục hiện tại). Muốn dùng probe cũ thì chép vào đây rồi chạy.

## Bối cảnh
Chủ kho (#1179 comment 6686369822): lặp vá spec, mỗi vòng một lượt Codex độc lập, tới khi MỘT lượt cho 0 P1 / 0 P2 / 0 P3; trần lời gọi 10→16, pha spec tối đa 4 lượt (đã dùng hết 4; chủ kho cho thêm tối đa 2 — lượt này là thêm 1/2, comment 6690435193), pha thi công 3. Quyết định giữ: trần kích thước ≤2 tệp/≤750 dòng; F6 theo nhánh "so OID trước"; phạm vi C1a1b.
Lượt 6 (trên r6) còn F16 P2 `phan-loai-vang-va-khong-do-duoc`: oracle "chỉ luật đích đổi màu" suy theo vị trí, không theo OID và tài nguyên chung (subtree ops trùng OID; reader cat-file chung chết). r7 sửa ở §0.8 (14 đường cùng lớp), §2.3 (phạm vi cục bộ/chung, tách `E_framing_lech`/`E_reader_chet`, memo chỉ lưu thành công), §2.6, §4 (tập đọc theo (kiểu, OID), oracle độc lập, guard, ca alias), A7, A11, A12 (e–h), A13, A20, A20b, A23.

## Nhiệm vụ
1. Xác minh F16 đã vá thật, và rằng 14 đường cùng lớp ở §0.8 là ĐỦ (tự tìm đường bị sót). Dựng đồ thị thật trên MOC theo ràng buộc fixture r7 và kiểm: bảng `doc(G)` §4 theo OID; ca alias; các ca A12 (e)–(h) và A13 (tổng byte, deadline) bằng một reader prototype có memo chỉ lưu thành công; mỗi đột biến khai ở A12/A13/A23 có đổi màu đúng ca đích không.
2. Review TOÀN BỘ r7 theo LỚP (ADR-0060 M2), không chỉ phần đổi: ABI/rc, bảng đóng §2.3 × G6/G7/G8, N6, §2.6, §3, A1–A23 (cả A20b), §8/§11 so với ADR-0043/0052/0055/protocol §12, nội nhất quán. Mọi biểu hiện, kể cả P3.
3. Đo lại các con số đo được. Prototype nhỏ trong sandbox được phép; ghi lệnh/rc/output.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv7/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F16; bảng lớp; finding mới `F<n>` (đánh số từ F17; mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất cụ thể); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`. Chỉ `approve` khi 0/0/0.
