# ADR-0038 — Review Class fail-closed và phân bổ quota Codex

- **Trạng thái:** Accepted (2026-08-17, phiên `grill-with-docs`; chủ kho phê duyệt)

Mỗi Packet khai mức review tối thiểu `routine`, `systemic` hoặc `sensitive`; dispatcher tính lại từ risk,
effective write set và diff thật, lấy mức cao hơn, còn path không biết hoặc classifier lỗi thành `sensitive`.
`sensitive` bắt buộc Codex cross-review hoặc human audit; `systemic` ưu tiên Codex lượt đầu và chỉ dùng lượt hai
khi còn P0/P1, finding cắt ngang hoặc cần xác minh lại; `routine` mặc định dùng phiên Claude độc lập hoặc human.
Executor không được tự hạ lớp và human override phải có audit. Quyết định này hy sinh một số lần pause/fallback
oan để quota reviewer hiếm được dùng tất định ở nơi thay đổi authority, security hoặc nhiều downstream consumer,
thay vì phân bổ theo cảm giác của phiên đang chạy.
