Bạn là reviewer read-only (Codex CLI) cho một PR đặc tả MỚI của kho tra-luat, trên commit CỤC BỘ 85b5a83 (chưa đẩy). Thư mục làm việc là bản clone ở commit ấy. KHÔNG sửa tệp nào.

Đối tượng: sáu tệp đóng băng (sha256 dưới đây) — phần chung `ops/specs/may-adr-0054-chung.md` và năm đặc tả con `ops/specs/wp812.md` … `wp816.md` (packet #812–#816, tách từ mission #796). Ngữ cảnh: `AGENTS.md`, `CLAUDE.md`, `docs/adr/0054-*.md`, `docs/adr/0050-*.md`, `docs/adr/0052-*.md`, `docs/adr/0053-*.md`, `docs/PROTOCOL_DA_PHIEN.md`, `.claude/dev/packet_loop.py`, `ops/bien_nhan_v2.py`, `ops/lease_publish.py`. Thiết kế gộp trước (wp796/wp797 r1–r10) và lịch sử review của nó ở `ops/reviews/spec798-may-adr-0054/` (nếu có trong clone) chỉ là đầu vào thiết kế.

Các đặc tả này CỐ Ý viết dạng BẤT BIẾN + tiêu chí đo, không mô tả cơ chế; executor chọn cơ chế và review bắt lỗi trên mã thật. Vì vậy finding hợp lệ là: (1) bất biến hay mục tiêu sai/mâu thuẫn nhau hoặc mâu thuẫn ADR/protocol/mã hiện hành (đối chiếu với mã thật); (2) bất biến THIẾU khiến một đường lỗi đã biết (xem lịch sử review) không bị cấm; (3) tiêu chí nghiệm thu không thể đỏ hoặc mâu thuẫn; (4) chia packet sai (write set không kham mục tiêu, phụ thuộc thiếu/vòng); (5) dữ kiện sai (enum, tên lệnh/trường, trạng thái PR). KHÔNG phải finding: "đặc tả chưa mô tả cơ chế X" khi bất biến đã cấm đường lỗi của X.

Review THEO LỚP: khái quát mỗi biểu hiện thành một lớp nguyên nhân, quét mọi biểu hiện cùng lớp trong sáu tệp, báo mỗi lớp một lần kèm danh sách biểu hiện. Hạng theo thang connector.

Đầu ra (chỉ thế này, tiếng Việt):
```
VERDICT: approve | changes_requested
P0=<n> P1=<n> P2=<n> P3=<n>   (đếm theo LỚP)
## Lớp <slug> — P<k>
- biểu hiện: <tệp>:<mục> — <một câu>
- đường lỗi cụ thể:
- hướng sửa ở mức lớp:
```
Lượt CLI trước (trên 42f8551) ra 4 lớp: hien-vat-hop-le-chua-du-tham-quyen (P1), dinh-danh-lop-khong-duoc-chuan-hoa (P1), vi-tu-tap-rong-qua-rong (P2), bat-bien-chung-phu-thuoc-nguoc (P2); bản này vá cả bốn (I2, I3, I5, I7, I10, I11 mới/sửa). Kiểm từng lớp đã đóng chưa (giữ slug nếu còn), rồi quét lớp mới.
approve chỉ khi P0=P1=P2=0.

sha256:
e52d6ce9d675d8ba69b70523ce74308002f29dae4dda9b8db87b0b30c97a8174  ops/specs/may-adr-0054-chung.md
446e8338125e420ee8bafae8542d4203cad0dd639e041fb305e13093ceec19ae  ops/specs/wp812.md
6ebbc12e1d9f84008f65dd779d0f5fd78b6a217bd76a20b87dc258c78f399a0f  ops/specs/wp813.md
05f8c6631e4f477ed8d3cdc593a8477621aa51dd9c2ed0373a01fbcc98851091  ops/specs/wp814.md
52717d8fee1a10120444d9abfe91c183fc4dd104a41291954c6284ff9137d695  ops/specs/wp815.md
1ce5807c2377c17bd19c0a27a72a5994757ba194b6eedb2141f3943cee910bce  ops/specs/wp816.md
