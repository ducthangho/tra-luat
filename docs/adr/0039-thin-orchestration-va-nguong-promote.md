# ADR-0039 — Thin Orchestration và ngưỡng promote auto-dispatch

- **Trạng thái:** Accepted (2026-08-17, phiên `grill-with-docs`; chủ kho phê duyệt)

Phiên bản đầu tái dùng `launcher.py`, `packet_loop.py`, ba skill và GitHub Issue/PR; không thêm daemon, TUI,
orchestrator tổng quát hoặc dự án ngoài vào critical path. Automation chỉ nắm quyết định tất định; human tiếp tục
chọn Stable Slice, revision thiết kế/Packet/Mission, land và activation authority. Auto-dispatch chỉ được đề nghị
promote sau ít nhất ba Mission thực tế liên tiếp đã landed và canonical readback mà không có stale review/lease,
out-of-effective-write-set hoặc reviewer/publisher identity mismatch; một vi phạm reset chuỗi, và đủ ngưỡng vẫn
cần human approval, negative fixtures, canary cùng kill switch. Cách này chấp nhận thêm thao tác thủ công ở V1 để
giảm bề mặt thay đổi và chỉ trao authority cho đường đã chứng minh năng lực end-to-end.
