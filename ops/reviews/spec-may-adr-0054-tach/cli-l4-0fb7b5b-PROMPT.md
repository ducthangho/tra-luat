Bạn là reviewer read-only (Codex CLI) cho một PR đặc tả MỚI của kho tra-luat, trên commit CỤC BỘ 0fb7b5b (chưa đẩy). Thư mục làm việc là bản clone ở commit ấy. KHÔNG sửa tệp nào.

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
Ba lượt CLI trước: 4 → 3 → 1 lớp. Lượt 3 (trên 188ab99) còn khoi-tao-moi-mau-thuan-duong-cu (P2: ranh giới tương thích ở record-lease; NGỮ CẢNH g2 lấy từ init); bản này vá (I9; #812 M1 hai đường record-lease; #815 M2). Kiểm lớp ấy đã đóng chưa, rồi quét lớp mới trên toàn bộ sáu tệp.
approve chỉ khi P0=P1=P2=0.

sha256:
4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0  ops/specs/may-adr-0054-chung.md
6b8b6c79703bc21949adf006ffc4bb351374254f5a27a0d85ed908ece6511d26  ops/specs/wp812.md
e64acd3bc2681a0ddb3b8253cf4dfa711da16cf77a23259ef85dc7ed8683d4fa  ops/specs/wp813.md
5d98edfef69825d7f8d605580a24eeb293e727c96ac05694ef1b450268df5fca  ops/specs/wp814.md
2c12d8eafea2a077093e8af118a6f99521311118430235515132108320971160  ops/specs/wp815.md
81bd5a5bb4a396c49ea07014f46a3605c91b4cd2aa60e092fb0a8d02510d72b4  ops/specs/wp816.md
