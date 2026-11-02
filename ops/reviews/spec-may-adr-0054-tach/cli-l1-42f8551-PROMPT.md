Bạn là reviewer read-only (Codex CLI) cho một PR đặc tả MỚI của kho tra-luat, trên commit CỤC BỘ 42f8551 (chưa đẩy). Thư mục làm việc là bản clone ở commit ấy. KHÔNG sửa tệp nào.

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
approve chỉ khi P0=P1=P2=0.

sha256:
9c3680e754923fab5a9968580cdfa2633797680f00b164bd559d51847892011b  ops/specs/may-adr-0054-chung.md
e5235b40bb33913cb2d847dfb7857b9c8e07e10f787ce44e1918ce8006d902e3  ops/specs/wp812.md
0932ab39508ce455f279bfef3d6ab979e762aeea67f91ddc3c70ec1a5d805d13  ops/specs/wp813.md
a447924c139494c2a5268cf25894239622e97e029f6e009db214b2ec51a94be6  ops/specs/wp814.md
4f71615651715efaf871466a6da6b5ea67a605036dc929c38762986428377372  ops/specs/wp815.md
e9344eb5108ff555665f06b457f8bc455b7b00063e56f2d3141e66289c983d9d  ops/specs/wp816.md
