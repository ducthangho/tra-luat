# Lựa chọn nền tảng điều phối lập trình đa model Codex–Claude

- **Ngày đo:** 2026-08-04 (Asia/Saigon)
- **Phạm vi:** dự án mã nguồn mở trên GitHub có thể điều phối Codex và Claude Code trong quy
  trình code → test → review → GitHub.
- **Yêu cầu cứng:** dùng được GPT-5.6 qua Codex CLI/agent, Claude Code với Claude Opus 5 và
  Claude Fable 5; tích hợp GitHub; tách vai trò executor/reviewer; có cổng test/CI.
- **Nguồn:** chỉ tài liệu, repository, release và mã nguồn chính thức của từng dự án/nhà cung
  cấp. Không dùng bài tổng hợp bên thứ ba.
- **Tính chất:** báo cáo nghiên cứu non-normative; Protocol/ADR đã land của `tra-luat` vẫn là
  nguồn quy tắc vận hành.

## 1. Kết luận ngắn

**Lựa chọn tốt nhất cho `tra-luat` là
[GitHub Agentic Workflows (`github/gh-aw`)](https://github.com/github/gh-aw), nhưng phải dùng nó như
control plane GitHub và ghép nhiều workflow, không coi một workflow đơn là cả “đội agent”.**

Lý do chính:

1. Đây là dự án chính chủ GitHub, chạy trên GitHub Actions và hỗ trợ trực tiếp cả
   **Claude Code** lẫn **OpenAI Codex**, không chỉ bọc API chat chung.
2. `engine.model` và `engine.version` cho phép ghim model lẫn phiên bản CLI.
3. Agent mặc định read-only; thao tác ghi GitHub đi qua `safe-outputs` được kiểm tra và job có
   quyền riêng. Cơ chế này phù hợp hơn các orchestrator cho agent tự chạy `git`/`gh` với
   token ghi.
4. Workflow agentic là lớp bổ sung trên Actions; build/test/release tất định hiện có không bị thay
   bằng phán đoán của model.
5. Issue, comment, PR, inline review, consolidated review, dispatch workflow và reusable `workflow_call`
   đều có primitive sẵn.

Không có dự án nào trong số ứng viên đáp ứng **turnkey 100%**. `gh-aw` chọn một
`engine` cho mỗi tệp workflow. Vì vậy pipeline đa model phải được ghép từ các stage riêng và
truyền đúng Issue/PR/SHA giữa chúng. Đây là suy luận từ schema `engine:` số ít và cơ chế
compose chính thức, không phải một tính năng “cross-provider team” có sẵn.

Nếu ưu tiên **local Windows + đăng nhập subscription** thay vì GitHub cloud, lựa chọn thứ hai là
[Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator). Nó có worktree, worker,
reviewer, PR/CI loop và chạy native Windows/Linux, nhưng quyền ghi ít tách biệt hơn `gh-aw` và model
reviewer chưa có pin riêng trong project config.

## 2. Xác minh tên model và khả năng pin

Yêu cầu “Codex 5.6” nên được ghi bằng model ID chính xác:

| Họ model | ID nên pin | Bằng chứng |
|---|---|---|
| GPT-5.6 trên Codex | `gpt-5.6-sol`, `gpt-5.6-terra` hoặc `gpt-5.6-luna` | OpenAI xác nhận ba biến thể trong Codex và yêu cầu Codex CLI từ `0.144.0`: [GPT-5.6 in ChatGPT/Codex](https://help.openai.com/en/articles/20001354-gpt-5-6-in-chatgpt). |
| Claude Opus 5 | `claude-opus-5` | Anthropic công bố API ID và mục tiêu agentic coding/review: [What’s new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5). Claude Code `2.1.219` thêm model này: [release feed](https://github.com/anthropics/claude-code/blob/main/feed.xml). |
| Claude Fable 5 | `claude-fable-5` | Anthropic công bố ID và GA: [Introducing Claude Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5). Claude Code yêu cầu từ `2.1.170`: [release](https://github.com/anthropics/claude-code/releases/tag/v2.1.170). |

Claude Code chấp nhận alias hoặc full ID trong `--model` và frontmatter agent. Tài liệu chính thức nêu
thẳng `claude-opus-5` và alias `fable`; subagent có thể khóa tool bằng allowlist/denylist:
[Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents).

Hai caveat cần ghi vào rollout:

- Khả dụng model còn phụ thuộc plan, region và rollout của tài khoản; việc orchestrator chấp nhận
  chuỗi model không chứng minh tài khoản có entitlement.
- Fable 5 có safety classifier/refusal và Anthropic nêu retention 30 ngày, không có zero-data-retention.
  Không nên đưa mã/dữ liệu nhạy cảm sang Fable trước khi chính sách dữ liệu được phê
  duyệt; xem [tài liệu Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5).

## 3. Ứng viên số 1 — GitHub Agentic Workflows (`github/gh-aw`)

### Mức đáp ứng

| Tiêu chí | Đánh giá | Bằng chứng/khoảng hở |
|---|---|---|
| Codex CLI native | **Đạt** | `engine: codex` là engine chính thức; dùng `OPENAI_API_KEY`. |
| Claude Code native | **Đạt** | `engine: claude`; dùng Claude Code và `ANTHROPIC_API_KEY`. |
| Pin model/CLI | **Đạt** | `engine.model`, `engine.version`, `engine.args` là schema chính thức; pin version giúp build lặp lại được: [AI Engines](https://github.github.com/gh-aw/reference/engines/). |
| GitHub Issue/PR/review | **Đạt mạnh** | Safe outputs hỗ trợ Issue, comment, tạo PR, inline review, `APPROVE`/`REQUEST_CHANGES` và dispatch workflow: [Safe Outputs](https://github.github.com/gh-aw/reference/safe-outputs/). |
| Coding agent | **Đạt** | Agent đề xuất patch; job `create-pull-request` có quyền riêng áp dụng patch và tạo PR. |
| Independent reviewer | **Đạt khi compose** | Tạo workflow review riêng, pin provider/model khác, chỉ cho safe outputs review. Không có “named reviewer team” cross-provider trong một tệp. |
| Testing/CI | **Đạt mạnh** | `gh-aw` chạy trên Actions, cho trộn step tất định và giữ nguyên CI/CD: [FAQ](https://github.github.com/gh-aw/reference/faq/). |
| Security | **Tốt nhất nhóm** | Read-only mặc định, firewall/container, network allowlist, secret redaction, threat detection, safe-output job tách token ghi. |
| Windows/Linux | **Linux cho agent; Windows test tách job** | Agent workflow cần container/firewall và tài liệu chỉ dẫn Linux runner; test PowerShell/Windows phải là Actions job thường riêng. CLI có cả installer `.ps1` và `.sh` trong repo. |
| Độ chín | **Cao nhưng preview** | MIT; repo chính chủ GitHub; public preview; release `v0.84.3` ngày 2026-08-03 và repo còn push trong ngày đo: [releases](https://github.com/github/gh-aw/releases). |

### Mẫu topology nên dùng cho `tra-luat`

```text
GitHub Issue / work packet
          |
          v
Fable 5 executor workflow (write request -> safe-output PR)
          |
          v
deterministic CI (Linux + Windows/PowerShell, exact PR head SHA)
          |
          +--> Codex GPT-5.6 Sol reviewer workflow (read-only)
          |
          +--> Claude Opus 5 reviewer workflow (read-only)
          |
          v
dispatcher reconciles both verdicts + CI at the same head SHA
          |
          v
human-authorized land/deploy gate
```

Model có thể đổi vai trò, nhưng ba invariant không đổi:

1. reviewer không có `create-pull-request`/push safe output;
2. mọi verdict và test evidence phải neo cùng PR head SHA;
3. model không thay thế test tất định hoặc quyền land của người dùng.

### Chi phí thiết lập và rủi ro còn lại

- Cần viết/compile ít nhất ba workflow agentic và một coordinator/gate; không phải cài xong là có
  state machine D0.
- Cloud lane dùng API key/WIF. `gh-aw` không hỗ trợ `CLAUDE_CODE_OAUTH_TOKEN`; đăng nhập Claude
  subscription local không thay cho `ANTHROPIC_API_KEY`: [Authentication](https://github.github.com/gh-aw/reference/auth/).
- PR tạo bằng `GITHUB_TOKEN` mặc định không kích hoạt CI/PR workflow tiếp theo do chốt chống
  recursion của GitHub. Phải compose rõ bằng `workflow_call`/dispatch hoặc cấu hình
  `GH_AW_CI_TRIGGER_TOKEN`; xem [FAQ — triggering CI](https://github.github.com/gh-aw/reference/faq/#why-dont-pull-requests-created-by-agentic-workflows-trigger-my-ci-checks).
- `gh-aw` đang Public Preview; cần pin release/compiler, pin generated action SHA và canary trong trial repo.
- `engine.agent` custom-agent file hiện chỉ áp dụng cho Copilot trong bảng feature. Với Claude/Codex,
  vai trò coder/reviewer/tester nên được định nghĩa bằng workflow/prompt/tool policy, không tuyên bố
  nhầm là custom agent primitive native của `gh-aw`.

## 4. Ứng viên số 2 — Agent Orchestrator

[Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator) là lựa chọn mạnh nhất nếu
muốn một dashboard local và dùng chính các CLI đã login trên máy.

### Điểm mạnh

- Chạy Claude Code và Codex như CLI thật, đọc native session JSONL, hỗ trợ resume, không thay
  chúng bằng provider API chung: [Claude Code adapter](https://aoagents.dev/docs/plugins/agents/claude-code/),
  [Codex adapter](https://aoagents.dev/docs/plugins/agents/codex/).
- Mỗi worker có worktree/branch/PR riêng; daemon theo dõi PR, CI, review và chuyển failure/comment về đúng
  worker: [README](https://github.com/Untrivial-ai/agent-orchestrator).
- GitHub tracker và SCM là plugin first-class; SCM đọc PR, checks, reviews và merge state:
  [project configuration](https://aoagents.dev/docs/configuration/projects/).
- Có reviewer harness riêng cho Claude Code, Codex và OpenCode. Mã reviewer Claude deny Edit/Write/
  NotebookEdit/git commit/push; reviewer Codex thêm sandbox read-only:
  [Claude reviewer](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/backend/internal/adapters/reviewer/claudecode/claudecode.go),
  [Codex reviewer](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/backend/internal/adapters/reviewer/codex/codex.go).
- Desktop build hỗ trợ Windows, Linux và macOS; Windows dùng process runtime thay cho tmux:
  [platform overview](https://aoagents.dev/docs/).
- Apache-2.0; repo push trong ngày đo; latest release `v0.11.2` ngày 2026-07-30:
  [releases](https://github.com/Untrivial-ai/agent-orchestrator/releases).

### Khoảng hở

- `agentConfig.model` ghim được model cho worker/orchestrator, nhưng `ReviewerConfig` trong source hiện chỉ
  có `harness`, không có `model`. Reviewer adapter cũng không truyền model trong `LaunchConfig`:
  [project config source](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/backend/internal/domain/projectconfig.go).
  Do đó pin Fable 5 và Opus 5 cho hai reviewer riêng trong cùng project chưa phải cấu hình first-class;
  dùng default global của Claude CLI chỉ là workaround dễ drift.
- Test là lệnh do worker chạy và CI feedback loop, chưa là test-agent/gate theo contract D0. Repo phải
  tự cấu hình required checks và exact-SHA gate.
- Worker có quyền git/gh thực tế trong worktree. Có isolation và reviewer sandbox, nhưng không tách
  “model đề nghị write” khỏi “job tất định áp write” mạnh như `gh-aw safe-outputs`.
- Dự án còn pre-1.0 và đã đổi owner/package trong năm 2026; pin release và kiểm migration khi
  upgrade là bắt buộc.

## 5. Các runner-up theo mục đích hẹp

### OpenAI Codex plugin for Claude Code — tốt nhất cho local Windows nhẹ

[openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) là dự án chính chủ OpenAI,
Apache-2.0. Nó cho Claude Code gọi Codex review/delegate qua plugin:

- `/codex:review` read-only, `/codex:adversarial-review`, background job và optional Stop-hook review gate;
- `/codex:rescue` cho debug/triển khai, có thể yêu cầu chạy test;
- tham số `--model` được chuyển cho Codex; Claude host/subagent có thể pin Opus/Fable bằng cơ chế
  native của Claude Code.

Bằng chứng: [README và usage](https://github.com/openai/codex-plugin-cc). Latest release quan sát được
là `v1.0.6` ngày 2026-07-08: [releases](https://github.com/openai/codex-plugin-cc/releases).

Nó **không** là GitHub control plane: không có Issue lease/state machine, worktree fleet, PR lifecycle hay
test gate sẵn. Đây là local execution/review adapter tốt, không thay `gh-aw` hoặc Protocol D0.

### AWS Labs CLI Agent Orchestrator — orchestration CLI mạnh, không phù hợp Windows hardened

[awslabs/cli-agent-orchestrator](https://github.com/awslabs/cli-agent-orchestrator) chạy Claude Code,
Codex và nhiều CLI thật trong tmux; có supervisor/developer/reviewer profile, `handoff`/`assign`, workflow
có journal và role reviewer read-only:
[README](https://github.com/awslabs/cli-agent-orchestrator),
[workflows](https://github.com/awslabs/cli-agent-orchestrator/blob/main/docs/workflows.md).

Model Codex được cấu hình trong Codex CLI/profile; Claude native agent có thể giữ model config. Latest
release quan sát là `v2.4.1` ngay 2026-08-04; Apache-2.0:
[releases](https://github.com/awslabs/cli-agent-orchestrator/releases).

Nhược điểm quyết định:

- tmux là prerequisite; Windows phải qua WSL, không native ConPTY/PowerShell;
- không có GitHub Issue/PR/CI state machine first-class tương đương `gh-aw`/Agent Orchestrator;
- Claude và Codex provider mặc định có thể dùng bypass/yolo cho non-interactive session. Phải tạo
  profile an toàn riêng; Codex tool restriction ở tầng CAO chỉ là soft prompt, dù có thể bù bằng
  `codexProfile` sandbox read-only:
  [Codex provider](https://github.com/awslabs/cli-agent-orchestrator/blob/main/docs/codex-cli.md),
  [tool restrictions](https://github.com/awslabs/cli-agent-orchestrator/blob/main/docs/tool-restrictions.md).

### MCO — tốt nhất cho fan-out/so sánh model

[mco-org/mco](https://github.com/mco-org/mco) là neutral dispatcher nhẹ, MIT. Nó gọi Claude Code,
Codex CLI và các CLI khác như subprocess thật; có `mco review` read-only, `mco run` write, parallel,
chain, debate, model pin và JSONL/SARIF:
[README](https://github.com/mco-org/mco/blob/main/README.md). Latest release quan sát `v0.11.0` ngày
2026-07-29: [releases](https://github.com/mco-org/mco/releases).

MCO phù hợp là engine review/fan-out bên dưới D0, nhưng không tự quản Issue/PR, worktree,
lease, exact-SHA promotion hay land. Markdown-PR/SARIF là output, không phải GitHub lifecycle.

### OpenHands — platform rộng, nhưng native CLI cross-provider còn experimental

[OpenHands](https://github.com/OpenHands/OpenHands) có platform code agent, SDK subagent/reviewer và GitHub
Action review PR có inline comment. Review action cho phép backend ACP với Codex/Claude command, nhưng tài liệu
gắn nhãn ACP review là **experimental**, yêu cầu trusted self-hosted runner và tự quản authentication:
[Automated Code Review](https://docs.openhands.dev/openhands/usage/use-cases/code-review).

OpenHands rất tích cực (MIT, latest release quan sát `v1.9.0` ngày 2026-08-03), nhưng không có
bằng chứng first-party cho một stock pipeline phối hợp đồng thời Claude Code Fable 5, Opus 5 và
Codex GPT-5.6 theo code → test → cross-review gate. Setup và attack surface lớn hơn nhu cầu hiện tại.

## 6. Bảng quyết định

| Dự án | Native Claude/Codex | GitHub control plane | Code + review | Test/CI | Windows local | Pin exact model | Security mặc định | Kết luận |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `github/gh-aw` | Tốt | **Rất tốt** | Tốt khi compose | **Rất tốt** | Agent chạy Linux; Windows test tách job | **Có** | **Rất tốt** | **Chọn làm control plane** |
| Agent Orchestrator | **Rất tốt** | Tốt | **Rất tốt** | Tốt | **Có** | Worker/orchestrator có; reviewer còn hở | Khá | Chọn nếu local/dashboard là ưu tiên |
| `openai/codex-plugin-cc` | **Rất tốt** | Thấp | Tốt | Phải ghép ngoài | **Có** | **Có** | Tốt cho review | Local adapter bổ sung |
| AWS CAO | **Rất tốt** | Thấp | **Rất tốt** | Tốt khi tự viết workflow | WSL | **Có** | Mặc định rủi ro | Không chọn cho baseline hardened |
| MCO | **Rất tốt** | Thấp | Tốt | Output tích hợp được CI | Chưa có matrix chính thức rõ | **Có** | Khá | Fan-out/review engine |
| OpenHands | ACP experimental | Tốt | Tốt | Tốt | Cloud/Linux là đường chính | Có qua backend | Khá, setup phức tạp | Theo dõi, chưa chọn |

## 7. Khuyến nghị triển khai

Không thay thế Protocol D0 bằng DSL của một tool. Dùng:

- **D0 Protocol/Issue contract:** nguồn thật về packet, generation, lease, base/head SHA, write set,
  REVIEW_READY/REVIEW_RESULT và human authority.
- **`gh-aw`:** adapter cloud/GitHub để kích hoạt executor/reviewer, áp safe output và nối Actions.
- **GitHub Actions thường:** test tất định Linux + Windows/PowerShell, release verification và exact-SHA gate.
- **`openai/codex-plugin-cc` hoặc Agent Orchestrator:** lane local Windows khi cần subscription auth,
  worktree chỉ có trên máy, test Android–Windows hoặc evidence không thể đưa lên cloud.

Thứ tự rollout an toàn:

1. Prototype trong TrialOps/sidecar, **không** cho ghi repo thật.
2. Pin `gh-aw` release, Claude Code `>=2.1.219` (khuyến nghị canary đúng `2.1.221` đang dùng) và
   Codex CLI `>=0.144.0`; sau canary chuyển tất cả thành version cứng.
3. Land reviewer read-only trước, chỉ cho comment/review safe outputs; xác minh secret redaction và
   exact-head rejection.
4. Land deterministic test coordinator cho Linux + Windows; không để model tự tuyên bố test pass.
5. Sau cùng mới bật executor `create-pull-request`; không bật auto-merge/land/deploy.
6. Chỉ promote khi chứng minh retry, duplicate delivery, stale SHA, concurrent packet, CI failure, model
   refusal/fallback và secret boundary.

## 8. Bằng chứng hoạt động/giấy phép tại ngày đo

Metadata được đọc từ GitHub REST API tại ngày 2026-08-04; số sao/fork chỉ là tín hiệu
hoạt động, không phải thước đo chất lượng:

| Repo | License | Latest release quan sát | Trạng thái |
|---|---|---|---|
| [`github/gh-aw`](https://github.com/github/gh-aw) | MIT | [`v0.84.3`, 2026-08-03](https://github.com/github/gh-aw/releases/tag/v0.84.3) | không archive; push 2026-08-04; ~4.9k stars |
| [Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator) | Apache-2.0 | [`v0.11.2`, 2026-07-30](https://github.com/Untrivial-ai/agent-orchestrator/releases/tag/v0.11.2) | không archive; push 2026-08-04; ~8.8k stars |
| [`openai/codex-plugin-cc`](https://github.com/openai/codex-plugin-cc) | Apache-2.0 | [`v1.0.6`, 2026-07-08](https://github.com/openai/codex-plugin-cc/releases/tag/v1.0.6) | không archive; chính chủ OpenAI |
| [AWS CAO](https://github.com/awslabs/cli-agent-orchestrator) | Apache-2.0 | [`v2.4.1`, 2026-08-04](https://github.com/awslabs/cli-agent-orchestrator/releases/tag/v2.4.1) | không archive; push 2026-08-04 |
| [MCO](https://github.com/mco-org/mco) | MIT | [`v0.11.0`, 2026-07-29](https://github.com/mco-org/mco/releases/tag/v0.11.0) | không archive; push 2026-07-29 |
| [OpenHands](https://github.com/OpenHands/OpenHands) | MIT | [`v1.9.0`, 2026-08-03](https://github.com/OpenHands/OpenHands/releases/tag/v1.9.0) | không archive; push 2026-08-04 |

Không chọn [Z-M-Huang/claude-codex](https://github.com/Z-M-Huang/claude-codex) dù pipeline cũ có
plan/code/review/test khá sát yêu cầu: repo đã archived và README chỉ sang dự án kế nhiệm; không
nên đặt control plane mới lên artifact đã ngừng duy trì.
