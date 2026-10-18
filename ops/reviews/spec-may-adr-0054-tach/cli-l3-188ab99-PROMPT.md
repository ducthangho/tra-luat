Bạn là reviewer read-only (Codex CLI) cho một PR đặc tả MỚI của kho tra-luat, trên commit CỤC BỘ 188ab99 (chưa đẩy). Thư mục làm việc là bản clone ở commit ấy. KHÔNG sửa tệp nào.

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
Hai lượt CLI trước: lượt 1 ra 4 lớp (đã vá); lượt 2 (trên 85b5a83) ra hien-vat-hop-le-chua-du-tham-quyen (P1: verdict trong biên nhận chưa buộc approve), neo-hien-vat-khong-phan-biet-ngu-canh (P2), khoi-tao-moi-mau-thuan-duong-cu (P2); bản này vá cả ba (I9, I10 sửa; #812 M1/M2). Kiểm từng lớp đã đóng chưa (giữ slug nếu còn), rồi quét lớp mới.
approve chỉ khi P0=P1=P2=0.

sha256:
77be98824a3e043c5dab1f2f4aca7a75289ca1c8ef88a5395cb8b0911776fc53  ops/specs/may-adr-0054-chung.md
156340cfce13410c9a2a3962574308c00cbe140e646fd35b66932d2e77c17dcd  ops/specs/wp812.md
07f493f3323f593716c617226884c46e287856296cdb56421b1c0e67bbbab7b5  ops/specs/wp813.md
69c4f16630ba9f319aeb023e6df0b759a9b64f7eba43d8adbe244fbc8af51645  ops/specs/wp814.md
7b2194d8dd1dbee12a7cd0f4e93d8a6f83d2f8005435a89bfa1d0f9be4df9d80  ops/specs/wp815.md
904ebdd1d2eb645c5ca52f2956845e6acb0dffaf50483e0b86812803c067e31f  ops/specs/wp816.md
