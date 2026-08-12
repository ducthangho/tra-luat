# So sánh `github/gh-aw` với Bernstein, Agent Orchestrator và MetaSwarm

- **Ngày đo:** 2026-08-04 (Asia/Saigon)
- **Phạm vi:** đối chiếu đề xuất trong tệp đính kèm với khuyến nghị trước đó dùng
  [`github/gh-aw`](https://github.com/github/gh-aw).
- **Tiêu chí cứng:** Codex GPT-5.6, Claude Code Opus 5 và Fable 5; GitHub; agent code,
  review và test; Windows/local/cloud; bảo mật; độ trưởng thành; ưu tiên dùng Claude Max và
  ChatGPT Pro, không phát sinh API trả theo token.
- **Nguồn:** tài liệu và mã nguồn chính thức của dự án, GitHub API và tài liệu chính thức
  của OpenAI/Anthropic. Bài tổng hợp Augment Code không được dùng làm bằng chứng quyết định.

## Kết luận

**Khi thêm ràng buộc không dùng API trả theo token, lựa chọn thực tế thay đổi: Bernstein là
ứng viên gần yêu cầu nhất cho lane đa model cục bộ, nhưng chỉ nên làm runner đã harden dưới
Protocol D0. GitHub Actions thường vẫn nên giữ vai trò test gate tất định. `github/gh-aw` an
toàn hơn về control plane GitHub, nhưng không phù hợp làm model lane chính bằng hai gói thuê bao.**

Đề xuất trong tệp đúng khi nhận ra các ưu điểm khác biệt của Bernstein: pin model theo vai
trò, worktree biệt lập, quality gate, review pipeline đa model và lineage/receipt kiểm được
offline. Tuy nhiên nó đánh giá thấp bốn khoảng hở có tính quyết định:

1. Cấu hình mẫu dùng **sai model ID** (`fable-5`, `opus-5`, `gpt-5.6-codex`) và dùng khóa
   `review` thay vì role mặc định `reviewer`.
2. GitHub Action của Bernstein cài bản `latest` không pin, rồi mặc định chạy `git add -A`,
   commit và push vào nhánh đang checkout; không có lớp safe-output/protected-file tương
   đương `gh-aw`.
3. Claude adapter của Bernstein chạy `--permission-mode bypassPermissions`; role reviewer
   bỏ Write/Edit nhưng vẫn được `Bash` rộng. Worktree giúp giới hạn hậu quả, nhưng không biến
   reviewer thành read-only cứng.
4. HMAC audit chain là **opt-in**, không luôn bật. Lineage/replay spine luôn ghi, nhưng chính
   README yêu cầu `BERNSTEIN_AUDIT=1` hoặc `bernstein run --audit` để có HMAC chain.
5. Cross-model verifier đang dùng trong lifecycle mặc định là **tắt mặc định và fail-open** khi
   reviewer lỗi hoặc trả kết quả không parse được. `ReviewGate` mới hơn có fail-close/fresh-context,
   nhưng tại ngày đo chưa có production call site ngoài docs/test.

Vì vậy kiến trúc phù hợp nhất với hai gói thuê bao là:

```text
GitHub Issue / packet D0
  -> Bernstein local gọi Claude/Codex CLI đã đăng nhập bằng subscription
  -> worktree/branch biệt lập; mọi quyền ghi GitHub đi qua controller D0
  -> GitHub Actions test tất định Linux + Windows, cùng head SHA
  -> Codex GPT-5.6 Sol reviewer local read-only
  -> Claude Opus 5 reviewer local read-only
  -> coordinator kiểm hai verdict + CI cùng SHA
  -> người dùng cho phép merge/deploy
```

Không dùng GitHub Action auto-commit của Bernstein. Bernstein không nên được trao quyền tự
merge/push vào nhánh chuẩn trước khi qua một PoC hardened.

## 0. Mức phù hợp với Claude Max + ChatGPT Pro

Nếu “GPT Pro Max” nghĩa là **Claude Max + ChatGPT Pro**, cả hai CLI chính thức đều dùng được
với đăng nhập thuê bao: Claude Code có trong Pro/Max và Codex có trong các gói ChatGPT được hỗ
trợ. GPT-5.6 Sol/Terra/Luna đang được phát hành trong Codex cho Plus/Pro và các gói tổ chức;
Codex CLI cần từ `0.144.0`:
[Codex với gói ChatGPT](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan),
[GPT-5.6 trong ChatGPT/Codex](https://help.openai.com/en/articles/20001354-gpt-5-6-in-chatgpt).

Claude Fable 5 có trong Max, chịu giới hạn sử dụng tuần của gói; Claude Code dùng Opus 5 cần
từ `2.1.219`. Phiên bản `2.1.221` người dùng đã cung cấp đạt điều kiện này:
[Claude Code với Pro/Max](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan),
[Fable 5 theo gói](https://support.claude.com/en/articles/15424964-claude-fable-5-on-your-plan),
[cấu hình model Claude Code](https://code.claude.com/docs/en/model-config).

Bernstein và Agent Orchestrator gọi các CLI cài trên máy nên về kỹ thuật có thể dùng phiên đăng
nhập sẵn. Đây không phải quota vô hạn: fan-out nhiều agent sẽ tiêu quota subscription nhanh và
cần smoke test trên tài khoản thật. Để tránh vô tình chuyển sang trả phí API, không truyền
`ANTHROPIC_API_KEY` hoặc `OPENAI_API_KEY` vào runner; Anthropic ghi rõ biến API key sẽ được ưu
tiên hơn subscription login và phát sinh phí API. Ngược lại, các engine Claude/Codex của `gh-aw`
yêu cầu API key/WIF, nên không dùng trực tiếp phiên đăng nhập local của hai gói thuê bao:
[gh-aw engines](https://github.github.com/gh-aw/reference/engines/).

## 1. Tên model: cấu hình trong tệp phải sửa

Ba ID chính thức hiện tại là:

| Yêu cầu | ID chính thức | Nguồn |
|---|---|---|
| Codex GPT-5.6 | `gpt-5.6-sol` (alias `gpt-5.6`) | [OpenAI model catalog](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |
| Claude Opus 5 | `claude-opus-5` | [Anthropic Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5) |
| Claude Fable 5 | `claude-fable-5` | [Anthropic Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) |

Claude Code chấp nhận alias `opus`/`fable` hoặc full model ID, nhưng full ID an toàn hơn khi
cần bằng chứng exact-model; xem [Claude Code subagents](https://code.claude.com/docs/en/sub-agents).

Bernstein có `role_model_policy` và tài liệu nói rõ `model` được truyền xuống CLI:
[configuration reference](https://bernstein.readthedocs.io/en/latest/operations/CONFIG/).
Mã nguồn hiện tại cũng xác nhận:

- Claude adapter chạy `claude --model <model_id>` và pass-through chuỗi không có trong alias
  map: [`claude.py`](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/adapters/claude.py).
- Codex adapter chạy `codex exec ... -m <model>`:
  [`codex.py`](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/adapters/codex.py).

Do đó Bernstein **có khả năng kỹ thuật** pin cả ba model, nhưng adapter alias/comment mặc định
vẫn đang neo Opus 4.7 và GPT-5.5/5.4. Exact support mới là pass-through, chưa phải tổ hợp được
maintainer chứng nhận. Cần `bernstein doctor`, `bernstein test-adapter claude/codex` và một
smoke task thật trên đúng CLI/version/tài khoản.

`effort` không đồng nhất giữa adapter: Claude adapter truyền effort xuống Claude Code, còn Codex
adapter hiện không dùng `model_config.effort`. Vì vậy `effort: high` trong mẫu không chứng minh
Codex đang chạy đúng reasoning level. Mục `role_model_policy.review` cũng không cấu hình verifier
pre-merge; lifecycle dùng role `reviewer`, còn cross-model verifier/review pipeline là cấu hình riêng.

Cấu hình tối thiểu đúng hơn đề xuất đính kèm:

```yaml
role_model_policy:
  manager:
    cli: claude
    model: claude-fable-5
    effort: max
  backend:
    cli: claude
    model: claude-opus-5
    effort: high
  reviewer:
    cli: codex
    model: gpt-5.6-sol
    effort: high
```

Nếu cần hai reviewer Opus và Codex độc lập, nên dùng review pipeline DSL với hai `AgentSpec`,
không chỉ một mục `reviewer` trong `role_model_policy`; xem
[review pipeline](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/operations/review-pipeline.md).

## 2. So sánh trực tiếp

| Tiêu chí | `github/gh-aw` | Bernstein | Agent Orchestrator | MetaSwarm |
|---|---|---|---|---|
| Claude Code + Codex native | **Có** | **Có** | **Có** | Có, nhưng Codex chủ yếu qua shell adapter |
| Pin exact model theo vai trò | **Có**: `engine.model`, một model/workflow | **Có**: `role_model_policy`; review DSL pin từng agent | Worker/orchestrator có `agentConfig.model`; reviewer config hiện chỉ có `harness` | Codex config được mô tả nhưng adapter hiện không truyền `-m`; Claude phụ thuộc host/subagent config |
| Coding agent | Safe-output tạo patch/PR | Agent sửa worktree và merge/push theo runner | Worker/worktree/branch/PR | Workflow implement/TDD/worktree |
| Review độc lập | Ghép workflow Claude/Codex read-only | Review DSL có nhiều stage/model; production verifier mặc định tắt và fail-open | 3 reviewer harness: Claude, Codex, OpenCode | Adversarial review; Codex host tự review tuần tự nếu không có subagent |
| Test | **GitHub Actions tất định**, tách khỏi model | Có janitor/gate; tests/type/security mặc định tắt, phải cấu hình | CI feedback loop; repo tự định nghĩa required checks | TDD/coverage/validate do orchestrator chạy |
| GitHub | **Control plane first-class**, Issue/PR/review/dispatch | Action + `gh`, issue import, PR/autofix/review responder | Tracker/SCM/PR/CI dashboard mạnh | `gh` + PR shepherd, BEADS là state chính |
| Windows local | Agent workflow chạy Linux; Windows test là job Actions riêng | **Native Windows được tài liệu hỗ trợ** | **Native Windows/ConPTY** | Installer cross-platform, nhưng external adapters là Bash; Windows cross-model lane chưa được chứng minh native |
| Cloud | GitHub-hosted Actions | Local mặc định; Cloudflare experimental, hosted service chưa có | Local/desktop; Docker/runtime plugins | Chủ yếu local CLI/plugin |
| Quyền ghi mặc định | **Agent read-only; write job riêng có policy** | Claude bypass permissions; Action auto commit/push | Reviewer được harden; worker dùng quyền CLI thật | Shell scripts/full-auto; prompt/rubric là phần đáng kể của guardrail |
| Audit/provenance | Logs/Actions/audit + safe-output boundaries | **Mạnh nhất về receipt/lineage**; HMAC opt-in | Session/PR state, không có signed lineage tương đương | JSONL/BEADS, không có signed lineage tương đương |
| Độ chín | Chính chủ GitHub, MIT, Public Preview | Apache-2.0, solo-maintained, phát hành nhanh | Apache-2.0, pre-1.0, dashboard trưởng thành nhất | MIT, nhỏ và Claude-centric |

## 3. Bernstein: những gì đã xác minh

### Điểm mạnh có thật

- Dự án tồn tại, Apache-2.0, không archive; tại ngày đo có khoảng 781 stars, 93 forks,
  latest release `v3.13.0` (2026-08-01), còn push trong ngày 2026-08-04:
  [repository](https://github.com/sipyourdrink-ltd/bernstein),
  [releases](https://github.com/sipyourdrink-ltd/bernstein/releases).
- Hỗ trợ Claude Code, Codex và nhiều adapter CLI; mỗi task chạy trong worktree riêng, rồi qua
  lint/type/test gate: [README](https://github.com/sipyourdrink-ltd/bernstein#readme).
- Review pipeline có nhiều stage, parallel agents, model/adapter/effort riêng, aggregation và
  fail-blocks-merge: [review pipeline docs](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/operations/review-pipeline.md).
- Fresh-context `ReviewGate` abstraction ép session mới, model khác khi cấu hình required, chỉ nhận
  `(spec, diff, test_output)` và fail-close khi verdict không parse được:
  [review gate](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/orchestration/review-gate.md).
- Review/lineage receipt có chữ ký Ed25519 và có lệnh verify offline:
  [review receipts](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/operations/review-receipts.md).
- Tài liệu nêu native Windows, process-tree termination và path dài:
  [installation](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/getting-started/install.md).

### Những diễn đạt cần hạ mức

**“Replay byte-identically” không có nghĩa model sẽ sinh cùng code.** Scheduler và task graph có
thể deterministic; LLM, provider state và tool environment vẫn không tất định. Chính Claude
adapter nói suppression compaction chỉ best-effort và fingerprint dùng để **phát hiện** divergence,
không bảo đảm context/model output giống byte. Nên diễn đạt là “deterministic coordination plus
tamper/divergence detection”, không phải end-to-end deterministic code generation.

**“Không có LLM trong vòng điều phối” cần hiểu hẹp.** README nói decomposition dùng một LLM call;
config còn có `internal_llm_provider` cho decomposition, estimation và plan optimization. Sau bước
đó state machine/scheduling là Python. Nguồn:
[README pipeline](https://github.com/sipyourdrink-ltd/bernstein#how-it-works),
[configuration](https://bernstein.readthedocs.io/en/latest/operations/CONFIG/).

**HMAC không mặc định luôn bật.** README hiện phân biệt lineage/replay journal luôn-on với audit
chain opt-in qua `BERNSTEIN_AUDIT=1` hoặc `--audit`:
[README — prove a run](https://github.com/sipyourdrink-ltd/bernstein#prove-a-run).

**Default quality/review yếu hơn bảng trong tệp.** `quality_gates` mặc định bật lint/PII/DLP,
nhưng tests, type check và security scan mặc định tắt. Cross-model verifier cũng tắt mặc định;
khi được bật, implementation hiện approve nếu reviewer ném `RuntimeError` hoặc output không parse
được. `ReviewGate` fail-close ở trên mới là abstraction/docs/unit-test, chưa được gọi trong runtime
lifecycle tại ngày đo. Nguồn:
[quality gates](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/core/quality/quality_gates.py),
[cross-model verifier](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/core/quality/cross_model_verifier.py),
[task lifecycle](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/core/tasks/task_lifecycle.py).
Do đó không thể ghi chung rằng “janitor test/lint/type/PII chặn merge” nếu chưa bật từng gate và
chưa thay/wrap verifier bằng fail-close gate.

**Signed lineage cũng cần hardening.** Lineage có thật và luôn-on ở phiên bản hiện hành, nhưng
`lineage.strict` mặc định false nên lỗi lineage chỉ cảnh báo thay vì chặn write. Xem
[lineage documentation](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/lineage.md).

**GitHub Action không phải least-privilege safe output.** `action.yml` hiện:

- `uv tool install bernstein` không pin version;
- `git add -A` toàn cây;
- tự commit mọi thay đổi và `git push origin HEAD:<current-branch>`;
- chỉ bỏ cơ chế đó khi caller đặt `BERNSTEIN_SKIP_AUTO_COMMIT=true`.

Nguồn: [`action.yml`](https://github.com/sipyourdrink-ltd/bernstein/blob/main/action.yml).
Đây là khác biệt an ninh lớn nhất so với `gh-aw`.

Ngoài ra, tài liệu Action hiện minh họa `sipyourdrink-ltd/bernstein@v4`, trong khi ref `v4` chưa
tồn tại tại ngày đo và latest release là `v3.13.0`. Composite Action cũng không tự cài Claude Code
hay Codex CLI. Cần pin tag/SHA có thật và setup CLI riêng; không copy ví dụ `@v4` nguyên trạng.

## 4. Vì sao `gh-aw` mạnh về control plane nhưng không đứng đầu theo chi phí hiện tại

`gh-aw` hỗ trợ trực tiếp `engine: claude` và `engine: codex`, cùng `engine.model`,
`engine.version`, args và tool allowlist:
[AI engines](https://github.github.com/gh-aw/reference/engines/).

Nó tách model khỏi quyền ghi: agent chạy read-only và chỉ gửi structured request; job riêng có
quyền tối thiểu mới áp thao tác GitHub. Cơ chế này có audit, giới hạn số output, protected files và
allowed-files:
[safe outputs](https://github.github.com/gh-aw/reference/safe-outputs/),
[pull-request safe outputs](https://github.github.com/gh-aw/reference/safe-outputs-pull-requests/).

Nó cũng có primitive ghép worker workflow: `call-workflow` cho deterministic fan-out và
`dispatch-workflow` cho worker async. Vì mỗi agentic workflow có một engine, ta tách Fable executor,
Codex reviewer và Opus reviewer thành ba workflow, rồi bắt mọi kết quả neo cùng head SHA.

Build/test/release hiện hữu không bị thay bằng LLM: `gh-aw` chạy trên GitHub Actions và cho phép
trộn step/job Actions thông thường:
[FAQ](https://github.github.com/gh-aw/reference/faq/).

Khoảng hở của `gh-aw` vẫn phải ghi rõ:

- đang Public Preview;
- cần API key/WIF cho cloud lane, không dùng trực tiếp local subscription login;
- agent job cần Linux container; Windows PowerShell test phải là Actions job riêng;
- một engine/workflow, nên phải tự viết coordinator exact-SHA;
- PR/push từ `GITHUB_TOKEN` không tự kích hoạt CI, cần `workflow_call`/dispatch hoặc token phù hợp.

## 5. Hai ứng viên còn lại trong tệp

### Agent Orchestrator

URL `AgentWrapper/agent-orchestrator` hiện redirect về canonical
[`Untrivial-ai/agent-orchestrator`](https://github.com/Untrivial-ai/agent-orchestrator), không phải
hai dự án khác nhau. Tại ngày đo repo có khoảng 8.8k stars, 1.28k forks, latest `v0.11.2`, còn hoạt
động trong ngày.

Con số 23 worker adapter là đúng theo registry hiện tại:
[`registry.go`](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/backend/internal/adapters/agent/registry/registry.go).
Nó có worktree/PR/CI/reaction/dashboard và native Windows; đây vẫn là lựa chọn local UI tốt nhất.

Nhưng exact-model review còn hở: `AgentConfig` có `model` cho worker/orchestrator, trong khi
`ReviewerConfig` chỉ chứa `harness`:
[`agentconfig.go`](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/backend/internal/domain/agentconfig.go),
[`projectconfig.go`](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/backend/internal/domain/projectconfig.go).
Ba reviewer harness là Claude Code, Codex và OpenCode; reviewer Claude deny Edit/Write/commit/push,
reviewer Codex ép sandbox read-only:
[reviewer registry](https://github.com/Untrivial-ai/agent-orchestrator/blob/main/backend/internal/adapters/reviewer/registry.go).

Kết luận: á quân nếu ưu tiên local subscription + dashboard; chưa phải control plane exact-model
và safe-output tốt bằng `gh-aw`.

### MetaSwarm

MetaSwarm có workflow SDLC đầy đủ nhất trên giấy: 18 persona, 9 phase, TDD, coverage gate,
adversarial review và PR shepherd:
[README](https://github.com/dsifry/metaswarm#readme). Nhưng nó áp đặt BEADS làm source of truth,
xung đột với D0 Issue/packet contract hiện có.

Có hai khoảng hở implementation quan trọng:

1. Tài liệu nói `.metaswarm/external-tools.yaml` có `adapters.codex.model`, nhưng
   `skills/external-tools/adapters/codex.sh` hiện hard-code `DEFAULT_MODEL="gpt-5.3-codex"` để ghi
   log và gọi `codex exec` **không có `-m/--model`**. Vì vậy pin GPT-5.6 qua config chưa được
   implementation chứng minh:
   [external-tools skill](https://github.com/dsifry/metaswarm/blob/main/skills/external-tools/SKILL.md),
   [Codex adapter](https://github.com/dsifry/metaswarm/blob/main/skills/external-tools/adapters/codex.sh).
2. Cross-model adapters là Bash scripts. Installer Node có phát hiện Windows, nhưng chưa có native
   PowerShell adapter hay Windows CI matrix chứng minh external lane; nên ô “Windows ✅” trong tệp
   phải hạ thành “chưa chứng minh, có thể cần Git Bash/WSL”.

Codex-hosted MetaSwarm còn chỉ sequential/self-review theo chính platform guide, không phải independent
subagent review:
[platform adaptation](https://github.com/dsifry/metaswarm/blob/main/skills/start/references/platform-adaptation.md).

## 6. Khuyến nghị thử nghiệm

Không thay Protocol D0 ngay. Chạy hai PoC local tách biệt, đều dùng CLI đã đăng nhập và không
truyền API key:

1. **PoC A — Bernstein local read-only:** pin `v3.13.0`, bật `BERNSTEIN_AUDIT=1`, pin ba full
   model ID, bật tests/type/security và `lineage.strict`, chạy `doctor`/adapter smoke test, review
   một detached worktree và xác minh zero diff cùng receipt offline. Tắt default cross-model
   verifier hoặc bọc bằng fail-close gate cho đến khi runtime wiring được chứng minh.
2. **PoC B — Agent Orchestrator local:** kiểm Claude/Codex harness với credential subscription,
   worktree và CI feedback trên Windows; chỉ cho tạo branch/worktree và nhận review, không auto
   merge. Xác minh riêng exact reviewer model vì cấu hình reviewer hiện chưa pin model first-class.

Chỉ quay lại PoC `gh-aw` cho model lane nếu sau này người dùng chấp nhận ngân sách API riêng.

Chỉ cân nhắc dùng Bernstein cho executor sau khi đã thay/bao `bypassPermissions`, vô hiệu auto
commit/push, thêm allowed-path exact write-set và chứng minh PowerShell 5.1/7 + Unicode path trên máy
thật. Dù chọn tool nào, Protocol D0, exact SHA, positive test evidence và quyền land/deploy của người
dùng vẫn là nguồn chuẩn.
