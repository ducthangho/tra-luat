# ADR-0043 — Trần vòng review canon là HAI, và nó chỉ có một chỗ ở

- **Trạng thái:** Accepted (2026-08-21, thẩm định ba bên codex–Claude Fable 5–Claude Opus 5; chủ kho phê duyệt Q5)

Trần canon cho một PR packet là **hai vòng review hợp lệ**. Trục VÒNG (canon, kỷ luật) tách khỏi trục
LỜI GỌI (chi phí) và trục ATTEMPT (số lần tuyên bố DONE); các trần độc lập và trần chạm trước thắng.
Vượt trần phải có khối `nang_tran` khai `ai_nang` thuộc người có thẩm quyền, `can_cu`, `tran_cu` và
`tran_moi`; không có khối ấy thì cổng đăng lease từ chối.

Vì sao cần ADR thay vì một § trong tài liệu kế hoạch: trước ADR này con số sống ở bốn chỗ với hai giá
trị và hai luật ưu tiên loại trừ nhau. `docs/PROTOCOL_DA_PHIEN.md:751` và `docs/adr/0037:5` ghi ba vòng;
`ops/KE_HOACH_THI_CONG_DA_PROVIDER.md:245-248` ghi hai vòng và tự tuyên "điều khoản này thắng"; trong khi
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md:13` tuyên "protocol thắng" và mermaid dòng 156 của chính tệp ấy vẫn
vẽ ba vòng dù dòng 494-498 đã có ghi chú tự sửa. Một phiên đọc protocol trước — đúng như dossier dạy — sẽ
dùng ba vòng một cách ngay tình. Lần đổi canon 3→2 trước đây được ghi trong đúng một tài liệu kế hoạch,
không ADR không MCR, trái `ADR-0034` vốn đòi Mission Change Request cho thay đổi material.

Thi hành: sửa `docs/PROTOCOL_DA_PHIEN.md:751`, `docs/adr/0037:5` và mermaid `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md:156`
để trỏ về ADR này thay vì mang con số riêng. Cưỡng chế bằng `packet_loop.py doctrine-scan` mở rộng sang
`ops/KE_HOACH_*.md` cộng chế độ `so-canon`: tài liệu nào nhắc trần review/attempt/call mà không trỏ một
hằng số duy nhất thì thoát khác 0. Hạ tầng đã đo được là chạy: `doctrine-scan` trên ba tệp kế hoạch hôm
21-08 trả `rc=6` với ba chỗ chép doctrine.

Kèm theo, xoá hai lời khai `ĐO ĐƯỢC` sai đã đo lại: `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md:267-269` viết
`review_rounds_used` "chỉ được khởi tạo và tăng" trong `packet_loop.py`, và `ops/THAM_DINH_AG_T0_03_VA_HOP_NHAT_KE_HOACH.md:394`
dẫn "khởi tạo dòng 638". Đo: `grep -rln "review_rounds_used" --include=*.py .` trả **0 tệp**;
`git log -S"review_rounds_used" -- .claude/dev/packet_loop.py` **rỗng** — cái tên ấy chưa từng tồn tại
trong lịch sử tệp. Nợ thật nặng hơn lời khai: không phải "có bộ đếm mà thiếu trần", mà là không có bộ đếm nào.
