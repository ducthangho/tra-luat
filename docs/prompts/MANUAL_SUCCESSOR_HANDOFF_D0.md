# Manual successor handoff D0

Dùng mẫu này sau **mọi phiên** cho tới khi deterministic dispatcher + auto-review loop được promote. Người giữ
tạo một task Claude/Codex mới bằng prompt bên dưới; không tiếp tục trong task cũ bằng cách đổi vai.

## Gói handoff bắt buộc

```yaml
schema_version: 1
mission_issue: <number>
packet_issue: <number>
packet_id: wp<number>
revision: <integer>
generation: <integer>
spec_hash: <sha256>
provider: claude | codex | human
role: executor | reviewer | land_operator
session_id: <stable-run-id>
base_sha: <git-oid>
head_sha: <exact-git-oid>
branch: <branch>
pr: <url-or-null>
status: done | needs_followup | blocked
changed_paths: []
gate_tier: T0 | T1 | T2 | T3 | T4 | T5
selector_policy_sha: <git-oid-or-policy-hash>
selected_groups: []
tests: []
full_evidence:
  workflow_run: <url-or-null>
  artifact: <name-or-null>
  output_sha256: <sha256-or-null>
  positive_match: <N/N-or-null>
  validated_identity: <true|false>
findings_closed: []
remaining_work: []
next_role: reviewer | executor | land_operator | human
manual_next_action: <one concrete action>
superseded_identity: <sha/generation-or-null>
stop_conditions: []
```

Trước khi phát prompt, đọc lại remote PR head và Issue projection. `head_sha`, generation, revision và spec hash
không khớp thì ghi `blocked` và không đề nghị worker chọn head/rebase khác. Evidence chỉ hợp lệ cho exact SHA.

## Prompt Reviewer có thể sao chép

```text
Bạn là Reviewer mới, độc lập, chỉ review một đơn vị công việc.

Repo: ducthangho/tra-luat
Mission: #{{MISSION_ISSUE}}
Packet: #{{PACKET_ISSUE}} / {{PACKET_ID}}, revision {{REVISION}}, generation {{GENERATION}}
PR: {{PR_URL}}
Exact head bắt buộc: {{HEAD_SHA}}
Executor provider/session: {{EXECUTOR_PROVIDER}} / {{EXECUTOR_SESSION}}

Preflight fail-closed: đọc trực tiếp Mission, Packet, PR, protocol và Executor evidence; xác minh remote PR head,
spec hash, generation và starting tree đều khớp exact identity trên. Nếu khác, dừng và báo blocker; không tự
rebase/chọn head khác.

Chỉ giữ vai Reviewer: read-only, không sửa file, không push, không chuyển sang Executor/Land Operator, không
approve/merge/deploy. Review hai trục Spec và Standards/Security; kiểm changed paths/evidence và chạy lại gate
read-only phù hợp ở tier {{GATE_TIER}}. Chạy targeted/adversarial probes trước; nếu CI có full artifact đúng exact
head/tree/base/runner/command/OS/runtime, output hash và positive marker thì validate và reuse, không lặp full local. Artifact thiếu/đỏ/stale/mismatch
phải fallback full; một host chỉ chạy một heavy gate. Ghi finding bằng stable ID, severity, file/line/evidence. Đăng verdict
approve|changes_requested|blocked lên Packet và PR, kèm provider/role/session/generation/reviewed exact SHA,
tests và assurance đúng thực tế. Human_audited chỉ dùng khi có GitHub identity bền, độc lập, audit evidence và
verdict cùng neo exact SHA.

Kết thúc bằng handoff theo docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md và một prompt sao chép cho vai kế tiếp.
Nếu changes_requested, next role là Executor phiên mới; nếu approve, next action là chờ reconciler/Approver,
không tự merge.
```

## Prompt Executor rework có thể sao chép

```text
Bạn là Executor mới, chỉ xử lý findings đã ghi cho một Work Packet; không tự review/approve/land/merge/deploy.

Repo: ducthangho/tra-luat
Mission: #{{MISSION_ISSUE}}
Packet: #{{PACKET_ISSUE}} / {{PACKET_ID}}, revision {{REVISION}}, generation {{GENERATION}}
PR/branch: {{PR_URL}} / {{BRANCH}}
Starting exact head bắt buộc: {{HEAD_SHA}}
Stable finding IDs được phép sửa: {{FINDING_IDS}}

Preflight fail-closed: đọc trực tiếp Mission, Packet, PR, review evidence và protocol; xác minh remote head,
generation/spec hash, worktree sạch và effective write set. Nếu drift, permission hoặc scope conflict, dừng và
báo blocker; không tự rebase/chọn head/mở rộng doctrine.

Sửa tối thiểu đúng findings trong effective write set bằng apply_patch. Chạy T0/T1 và gate bắt buộc theo
classifier, targeted-first; unknown/shared/security/release/EOL/policy change phải fallback full. Không lặp full
local nếu CI sẽ chạy nó trên exact new head; trước push đọc lại remote head;
commit/push generation hợp lệ và đăng Executor evidence với exact new head, changed paths, tier/policy/groups,
rc + bằng chứng dương, findings closed và verdict ready_for_rereview. Giữ PR Draft; không merge/LIVE.

Kết thúc bằng handoff theo docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md và prompt Reviewer mới trên new exact head.
```
