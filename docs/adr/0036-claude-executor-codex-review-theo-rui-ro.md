# ADR-0036 — Claude Executor mặc định, Codex review theo rủi ro

- **Trạng thái:** Superseded một phần bởi ADR-0041 (vai trò Codex Executor); review policy còn hiệu lực

Claude Code dùng model `opus`, effort `max` là Executor code mặc định. Bản gốc giới hạn Codex ở Reviewer read-only trên
exact PR head cho Packet có giá trị hoặc rủi ro cao, tối đa hai lượt mỗi PR: một review đầu và một rereview sau
khi Executor đã gom các bản vá. Nếu lượt hai chưa approve thì không tiếp tục đốt quota Codex; Packet đi qua
checkpoint tách phần đã ổn hoặc xem lại thiết kế. Packet thường có thể fallback sang một phiên Claude mới độc
lập với mức `same_provider_approved`, hoặc sang `human_audited`; phạm vi nhạy cảm vẫn phải có Codex
cross-review hoặc human audit. Quyết định này ưu tiên chất lượng Executor và giữ quota reviewer hiếm cho nơi nó
đổi được quyết định, đồng thời không cho fallback tự nhận mức assurance cao hơn bằng chứng thật.

Ngân sách tách `codex_review_calls_used` (lời gọi review đã bắt đầu sinh output/token),
`codex_executor_calls_used` và `review_rounds_used` (verdict hợp lệ). Review cap không vay executor ceiling và
ngược lại.
Timeout hoặc output sai schema vẫn tiêu call; preflight/permission/rate-limit trước generation thì không. Output
sai schema fail-closed và không được auto-retry hay đổi session để lách trần hai call.
