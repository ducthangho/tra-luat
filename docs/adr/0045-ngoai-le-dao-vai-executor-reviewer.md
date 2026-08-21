# ADR-0045 — Đảo vai executor/reviewer là NGOẠI LỆ CÓ VẾT, không phải mặc định mới

- **Trạng thái:** Accepted (2026-08-21, thẩm định ba bên; chủ kho phê duyệt Q8)

Mặc định giữ nguyên: **Claude Executor, Codex Reviewer** (`ADR-0036`, `ADR-0041`). Codex được làm Executor
cho một packet `sensitive` **chỉ khi** chủ kho chỉ định tường minh trong lease, reviewer khác nền, và có
human readback trước land. Mỗi lần dùng phải để lại vết đọc được bằng máy: lease khai `review_class` và khai
rằng đây là ngoại lệ theo §2. Ceiling 30% cho phần tự-điều-phối của Codex không đổi.

Vì sao cần ADR: ngày 20-08 thực hành đã đi trước văn bản và không tài liệu nào đỡ. `PLAT-X5` giao cho Codex làm
Executor trong khi packet chạm `.github/workflows/**` — `docs/PROTOCOL_DA_PHIEN.md:572` xếp là `sensitive`, và
chính lease thừa nhận điều đó. `ADR-0041:8` cùng `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md:91` giới hạn Codex
Executor ở packet `routine`/`systemic` nhỏ, đóng, write-set độc lập; điều kiện gate §4.2:118 đòi
`effective_review_class in {routine, systemic}`. Hai packet Codex-Executor duy nhất trong kế hoạch (`W0-C1`,
`W1-C2a`) đều đã đánh dấu `[ĐÃ BỎ: lane Codex]`, nên số packet Codex-Executor mà văn bản cho phép là **0**.
Chủ kho có thẩm quyền override theo §2 và đã dùng nó; cái thiếu là bản ghi.

Không cổng nào phát hiện được lệch này, vì `grep review_class ops/leases/plat-*.yaml` trả **không lease nào khai
review class**. Theo `ADR-0038:6` (path không biết hoặc classifier lỗi thì fail-closed thành `sensitive`), vắng
mặt phải bị đọc là `sensitive`. Cưỡng chế: `review_class` vào danh sách trường bắt buộc của cổng đăng lease;
vắng ⇒ `sensitive`; `sensitive` cộng `executor: codex` mà không có khối ngoại lệ do chủ kho ký ⇒ thoát khác 0.

Không suy rộng từ một mẫu. Lượt đảo vai duy nhất cho kết quả tốt — executor `codex` dừng đúng theo điều kiện
phạm vi khi phát hiện đặc tả tự mâu thuẫn, và reviewer `claude` sinh verdict dày nhất ngày, gồm P1 duy nhất —
nhưng đó là một mẫu trên một packet với một prompt cố ý khó hơn, và không có số token/thời lượng cho chiều
ngược để so chi phí. Ba bên thẩm định đều từ chối đổi mặc định dựa trên nó.
