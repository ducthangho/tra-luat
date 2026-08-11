# ADR-0035 — Điều phối bền vững và selftest phân tầng

- **Trạng thái:** Accepted (2026-08-08, MCR-54-02; chủ kho phê duyệt)
- **Phạm vi:** doctrine và thứ tự triển khai; chưa activate workflow/selector/credential

## Bối cảnh

Hai khoảng trống đang kéo ngược cùng một mục tiêu tự động hóa. Thứ nhất, một Executor kết thúc không làm một
Reviewer độc lập tự xuất hiện; nếu để agent tự gọi agent kế tiếp thì output mô hình vô tình trở thành state
machine và authority. Thứ hai, legacy harness chạy eager 1.696 ca, dùng global state và nhiều subprocess; chạy
full sau mọi packet làm feedback chậm nhưng lọc output hoặc chia modulo hiện tại không giảm công việc và có thể
che order coupling.

Số đo, nguồn và phản lựa chọn nằm trong:

- `docs/research/2026-08-08-tu-dong-hoa-dieu-phoi-da-phien.md`;
- `docs/research/2026-08-08-toi-uu-selftest-gate.md`.

## Quyết định

### Authority và chuỗi vai trò

GitHub Issue/PR/comment/check là durable facts. Một deterministic reconciler single-writer kiểm state revision,
Packet revision/spec hash, generation, lease, exact head/tested SHA, changed paths, gate policy và budget trước
mỗi transition. Agent là worker: Executor phát evidence rồi dừng; reconciler mới chuyển sang `reviewing` và
dispatch một Reviewer mới, read-only, context/worktree độc lập. Reviewer trả stable finding IDs hoặc verdict;
reconciler quyết định rework/frontier tiếp theo. Commit mới hủy evidence và authorization của SHA cũ.

Đây là manager/code orchestration thay vì để agent tự handoff quyền lực: OpenAI mô tả code orchestration là lựa
chọn tất định và dễ dự đoán hơn cho flow có thứ tự, còn Codex subagent guidance khuyên song song hóa việc đọc và
thận trọng với nhiều writer ([OpenAI Agents orchestration](https://openai.github.io/openai-agents-python/multi_agent/),
[Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)). Tối đa hai Executor writer có
write set không giao; Reviewer/gate read-only được chạy song song; integration/land vẫn single-writer.

### GitHub Agentic Workflows

`gh-aw` phù hợp như một provider-neutral worker adapter/canary cho Codex hoặc Claude, không phù hợp làm
authority. Nó còn public preview và workflow được author bằng Markdown rồi compile thành lock workflow; vì vậy
activation phải có pinned/reviewed lock, permission tối thiểu, safe outputs, untrusted-input separation,
feature flag, quota và kill switch ([GitHub Agentic Workflows](https://docs.github.com/en/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows),
[orchestrator/worker pattern](https://github.github.com/gh-aw/patterns/orchestrator-ops/)). Adapter có thể được
thay bằng runner native mà không đổi schema/state. Không dùng chuỗi `workflow_run` làm durable queue/state
machine vì GitHub giới hạn chain và downstream workflow có ranh giới quyền riêng
([GitHub `workflow_run`](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run)).

### Gate selftest

Áp policy T0–T5: targeted inner loop; affected packet gate; exact-head rereview gate; frozen integration/land
full hai OS; canonical/merge-group full hoặc exact-identity reuse; exact release artifact. Classifier và
aggregator luôn chạy. Unknown/unmapped path, runner/catalog/shared state, security/workflow, release/manifest,
EOL hoặc policy change fail closed về full. Evidence reuse chỉ hợp lệ khi SHA/tree, selector policy/catalog,
runner, OS/runtime và artifact identity cùng khớp.

Không activate selector ngay. Thứ tự bắt buộc là instrument duration → tách callable/group và dọn global state
→ parallel full có parity → selector shadow 2–4 tuần song song với full → activate có rollback. T3 và T5 vẫn là
full checkpoints; tối ưu packet loop không hạ release assurance.

### Giai đoạn thủ công

Cho tới khi A5 auto-dispatch được promote, mỗi phiên phải đăng evidence/handoff và kèm prompt có thể sao chép cho
phiên Claude/Codex kế tiếp theo `docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md`. Prompt không cấp lease, approval
hoặc quyền merge; người giữ vẫn tạo phiên mới và exact identity phải được readback trước khi làm.

## Hệ quả và trade-off

- Feedback packet thường giảm sau A2, nhưng full oracle vẫn tốn thời gian ở checkpoint quan trọng.
- Reconciler và catalog/policy có thêm state/evidence cần bảo trì, đổi lại retry idempotent, audit được và không
  phụ thuộc chat sống.
- `gh-aw` giúp thử nhiều provider nhanh nhưng bị cô lập sau adapter vì preview churn và security surface.
- Auto-review không có nghĩa auto-approve/merge: assurance, human audit, land authorization và LIVE/deploy vẫn là
  các cổng riêng.
- Nếu exact identity, classifier hoặc durable state không kiểm được, hệ thống pause/fallback full thay vì đoán.
