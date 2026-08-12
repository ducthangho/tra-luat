# Kiểm chứng phương án điều phối chỉ dùng Claude Max và ChatGPT Pro

- **Ngày đo:** 2026-08-04 (Asia/Saigon)
- **Phạm vi:** kiểm chứng các tuyên bố trong phương án đính kèm về xác thực,
  billing và khả năng pin model; chỉ dùng tài liệu/mã nguồn chính thức hiện hành.
- **Ràng buộc:** không dùng API trả theo token; giữ GitHub Actions thường cho gate
  tất định; không trao quyền merge/deploy tự động.

## Kết luận

Phương án đính kèm **đúng hướng và tốt hơn phương án lấy `gh-aw` làm model lane**
đối với người chỉ có Claude Max và ChatGPT Pro. Tuy nhiên cần sửa ba điểm quan
trọng:

1. `gh-aw` không dùng được **hai subscription này** cho engine Claude/Codex, nhưng
   nói “`gh-aw` không hỗ trợ subscription” là quá rộng: engine Copilot của nó có
   thể dùng một subscription GitHub Copilot riêng.
2. `anthropics/claude-code-action` hỗ trợ OAuth Pro/Max chính thức, không còn chỉ
   là mẹo cần suy đoán. Dù vậy token dài hạn trong GitHub Secrets và chính sách
   non-interactive đang ở trạng thái “tạm dừng thay đổi”, nên local CLI vẫn là
   lane chính an toàn hơn.
3. Cảnh báo rằng `internal_llm_provider` của Bernstein “nhiều khả năng cần API
   key riêng” là sai ở dạng tổng quát. Bernstein cho phép dùng chính adapter CLI
   `claude`, `codex` hoặc `ollama` cho bước này. Rủi ro PAYG xuất hiện nếu chọn
   provider API hoặc để `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` lọt vào môi trường.

## Bảng phán quyết

| Tuyên bố trong phương án | Phán quyết | Bằng chứng / điều chỉnh |
|---|---|---|
| `gh-aw` không dùng `CLAUDE_CODE_OAUTH_TOKEN`; engine Claude cần API key/WIF và engine Codex cần API key | **Đúng** | Tài liệu auth ghi rõ OAuth Claude không được hỗ trợ; lỗi Codex yêu cầu `OPENAI_API_KEY` hoặc `CODEX_API_KEY`. [gh-aw authentication](https://github.github.com/gh-aw/reference/auth/) |
| Vì vậy `gh-aw` không phù hợp với Claude Max + ChatGPT Pro của người dùng | **Đúng** | Hai subscription đó không xác thực engine Claude/Codex của `gh-aw`. Tuy nhiên engine Copilot có đường subscription GitHub Copilot riêng, nên không nên khái quát thành “không hỗ trợ subscription nào”. [gh-aw authentication](https://github.github.com/gh-aw/reference/auth/) |
| Codex GitHub code review dùng gói ChatGPT, không cần API key | **Đúng** | Giá Codex ghi automatic code review là cloud integration trong Plus; Pro kế thừa Plus. Cùng trang ghi API-key mode không có cloud features như GitHub code review. [Codex pricing](https://developers.openai.com/codex/pricing), [GitHub review setup](https://learn.chatgpt.com/docs/third-party/github) |
| Có thể dùng `@codex review` và auto-review, với luật trong `AGENTS.md` | **Đúng** | Tài liệu chính thức mô tả cả ba cơ chế; review GitHub hiện chỉ đăng P0/P1. [Codex code review in GitHub](https://learn.chatgpt.com/docs/third-party/github) |
| Codex GitHub review chắc chắn chạy đúng `gpt-5.6-sol` do người dùng pin | **Chưa chứng minh** | Tài liệu GitHub-review không công bố nút pin model/reasoning cho review cloud. GPT-5.6 Sol/Terra/Luna có trong Codex trên Pro, nhưng đó không chứng minh service review đang dùng Sol. [GPT-5.6 availability](https://help.openai.com/en/articles/20001354-gpt-5-6-in-chatgpt), [GitHub review setup](https://learn.chatgpt.com/docs/third-party/github) |
| `anthropics/claude-code-action` hỗ trợ `CLAUDE_CODE_OAUTH_TOKEN` từ Pro/Max | **Đúng, chính thức** | Setup guide yêu cầu tạo bằng `claude setup-token`; action khai báo input OAuth tương ứng. [Action setup](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md), [Action inputs](https://github.com/anthropics/claude-code-action/blob/main/docs/usage.md) |
| OAuth Action hiện trừ quota subscription | **Đúng ở thời điểm đo, nhưng có thể đổi** | Anthropic ngày 15-06-2026 tạm dừng cơ chế monthly Agent SDK credit; hiện `claude -p`, Agent SDK và third-party apps vẫn trừ quota subscription. Phần chính sách cũ phía dưới trang chỉ được lưu để tham khảo. [Anthropic billing update](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) |
| OAuth Action hoàn toàn tương đương phiên Claude interactive | **Sai** | Token `setup-token` dùng cho CI/script, chỉ có inference, không tạo Remote Control; `--bare` không đọc token. Token phải nằm trong GitHub Secrets. [Claude Code authentication](https://code.claude.com/docs/en/authentication), [Action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md) |
| `openai/codex-plugin-cc` dùng Codex CLI đã đăng nhập và cho review read-only | **Đúng** | Plugin chính chủ nhận ChatGPT subscription hoặc API key, yêu cầu `codex login`, bọc Codex app server và dùng cùng cấu hình. `/codex:review` và adversarial review đều được mô tả là read-only. [Plugin README](https://github.com/openai/codex-plugin-cc/blob/main/README.md) |
| `/codex:review` cho phép truyền prompt focus và pin model theo mỗi lần gọi | **Sai/thiếu** | Review thường không steerable và không nhận focus text; README không nêu `--model` cho lệnh này. Model/effort mặc định lấy từ `config.toml`; `--model` được nêu cho lane `rescue`, không phải review thường. [Plugin README](https://github.com/openai/codex-plugin-cc/blob/main/README.md) |
| Agent Orchestrator (AO) dùng session của CLI đã đăng nhập | **Đúng về kiến trúc** | AO chạy binary `claude`/`codex` trong worktree và không tự đặt credentials; tài liệu nói credential đến từ nơi CLI vốn đọc. Vì vậy nó dùng subscription nếu CLI đang ở auth subscription và không có API key ưu tiên. [AO Claude adapter](https://aoagents.dev/docs/plugins/agents/claude-code/), [AO Codex adapter](https://aoagents.dev/docs/plugins/agents/codex/) |
| AO không thể làm rò sang API billing | **Sai nếu hiểu tuyệt đối** | AO không khóa auth mode: nó kế thừa auth của CLI/môi trường. Với Claude, `ANTHROPIC_API_KEY` có độ ưu tiên cao hơn login subscription; do đó runner phải fail-close khi phát hiện API key. [Claude Code authentication](https://code.claude.com/docs/en/authentication), [AO Claude adapter](https://aoagents.dev/docs/plugins/agents/claude-code/) |
| Bernstein gọi CLI thật và có thể dùng subscription local | **Đúng có điều kiện** | Mã `main` hiện tại của Codex adapter nhận `~/.codex/auth.json`; Claude adapter gọi Claude CLI và có thể đọc login lưu tại home. Nhưng các adapter cũng truyền qua `OPENAI_API_KEY`/`ANTHROPIC_API_KEY` nếu có, nên phải kiểm auth trước mỗi run. [Bernstein Codex adapter](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/adapters/codex.py), [Bernstein Claude adapter](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/adapters/claude.py) |
| `internal_llm_provider` của Bernstein mặc nhiên cần API key riêng | **Sai** | Config hiện hành cho phép mọi adapter đã đăng ký, gồm `claude`, `codex`, `ollama`; chỉ provider API như `openrouter` mới ghi rõ cần key. Hãy pin `codex` hoặc `claude`, hoặc bỏ LLM decomposition bằng plan YAML đã chuẩn bị. [Bernstein config](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/operations/CONFIG.md), [Bernstein README](https://github.com/sipyourdrink-ltd/bernstein) |
| Max 20x khoảng 900 message mỗi 5 giờ | **Không có bằng chứng chính thức hiện hành** | Anthropic xác nhận Max 5x/20x, cửa sổ 5 giờ và hai giới hạn tuần, nhưng số message phụ thuộc model, context và công cụ. Không nên đóng đinh con số 900. [Claude Max](https://support.claude.com/en/articles/11049741-what-is-the-max-plan) |
| Fable 5 nên chỉ dùng khi phân xử khó để tiết kiệm quota | **Khuyến nghị hợp lý** | Trên Max, Fable 5 nằm trong gói nhưng chỉ dùng tối đa 50% giới hạn tuần mà không trả thêm, cùng chia sẻ tổng weekly limit; cần Claude Code từ 2.1.170. [Fable 5 on your plan](https://support.claude.com/en/articles/15424964-claude-fable-5-on-your-plan) |
| Opus 5 và Fable 5 là ID thật; GPT-5.6 có trong Codex Pro | **Đúng** | ID hiện hành là `claude-opus-5`, `claude-fable-5`; GPT-5.6 Sol/Terra/Luna có trong Codex cho Pro. GPT-5.6 cần Codex CLI từ 0.144.0. [Claude models](https://platform.claude.com/docs/en/about-claude/models/overview), [GPT-5.6 availability](https://help.openai.com/en/articles/20001354-gpt-5-6-in-chatgpt) |

## Topology subscription-only khuyến nghị

```text
GitHub Issue / packet D0
  -> Claude Code local interactive (executor; Opus 5 nếu tài khoản cho phép)
  -> Codex local / openai/codex-plugin-cc (review read-only; pin config)
  -> GitHub Actions thường: test Linux + Windows tại exact head SHA
  -> Codex cloud GitHub review: reviewer bổ sung P0/P1, không coi là exact-model gate
  -> Claude reviewer local hoặc claude-code-action OAuth khi thật sự cần
  -> controller D0 kiểm SHA/evidence
  -> người dùng cho phép push, merge và deploy
```

Bernstein hoặc AO chỉ nên được thêm làm **local session/worktree runner**, không
thay control plane D0. Trước khi chạy, controller phải fail-close nếu thấy
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_BASE_URL` hoặc
`OPENAI_BASE_URL`; sau đó kiểm `claude /status`, `claude /model`, `codex /status`
và dashboard usage. Giới hạn fan-out 1--2 agent vì song song hóa làm cạn quota
nhanh hơn.

`claude-code-action` OAuth là lane cloud subscription hợp lệ, nhưng chỉ nên làm
PoC read-only, pin action SHA, quyền GitHub tối thiểu, không checkout PR head
không tin cậy vào workspace root và không bật full output. Token OAuth dài hạn
phải ở GitHub Secrets. Nếu Anthropic thay đổi lại chính sách non-interactive,
lane này phải tự dừng thay vì chuyển âm thầm sang usage credits.

## Thứ tự thử nghiệm

1. Bật Codex GitHub auto-review và thêm `## Code Review Rules` ngắn trong
   `AGENTS.md`; coi đây là reviewer phụ vì không pin được exact model.
2. PoC `openai/codex-plugin-cc` trên một diff nhỏ bằng `/codex:review --base
   origin/master`; xác nhận read-only và model thực tế trong receipt/status.
3. Nếu cần dashboard nhiều worktree, PoC AO trước; nếu cần routing/audit sâu hơn,
   PoC Bernstein với provider nội bộ pin vào `codex`/`claude`, không dùng default
   không kiểm soát.
4. Chỉ sau đó mới PoC `claude-code-action` OAuth trên workflow read-only; đo quota
   trước/sau và giữ kill switch khi billing policy đổi.
