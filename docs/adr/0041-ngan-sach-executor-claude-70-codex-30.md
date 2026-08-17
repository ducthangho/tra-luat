# ADR-0041 — Ngân sách Executor Claude tối thiểu 70%, Codex tối đa 30%

- **Trạng thái:** Accepted (2026-08-17, phiên `grill-with-docs`; chủ kho phê duyệt)
- **Thay thế:** phần ADR-0036 nói Codex chỉ làm Reviewer

Claude Code `opus`, effort `max` vẫn là Executor mặc định. Mỗi Mission dành ít nhất 70% ngân sách Executor dự
kiến cho Claude và đặt ceiling Codex Executor ở 30%; đây không phải chỉ tiêu phải dùng hết và tỷ lệ Codex thực có
thể bằng 0 khi quota thấp. Codex chỉ nhận Packet `routine`/`systemic` nhỏ, đóng, write-set độc lập sau khi đã
reserve ngân sách tối đa hai Codex review cho các PR `sensitive`. PR do Codex code phải được phiên Claude mới độc
lập hoặc human review; Codex không review code mình. Ngân sách đo bằng invocation/token ceiling dự kiến của
Mission, không đếm số Packet, để một Packet lớn không giả thành cùng trọng lượng với Packet nhỏ.
