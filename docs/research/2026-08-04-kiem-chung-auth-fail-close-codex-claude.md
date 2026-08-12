# Kiểm chứng xác thực subscription và thiết kế fail-close

- **Ngày đo:** 2026-08-04 (Asia/Saigon)
- **Đối tượng đo tại máy:** Codex CLI `0.146.0`, Claude Code `2.1.221`
- **Phạm vi:** đề xuất trong tệp đính kèm về `--auth chatgpt`, thứ tự ưu tiên
  credential, môi trường tiến trình con, bằng chứng dương, GitHub review/action và
  `internal_llm_provider` của Bernstein.
- **Nguồn:** tài liệu chính thức và mã nguồn upstream; issue do người dùng mở không
  được dùng làm bằng chứng quyết định.

## Kết luận

Đề xuất **đúng ở nguyên tắc**: kiểm biến của shell cha chỉ là bằng chứng âm; gate phải
đo đúng môi trường tiến trình con và phải xác nhận auth subscription bằng output có cấu
trúc. Tuy nhiên có hai sửa đổi quyết định:

1. Codex CLI `0.146.0` **không có** cờ `--auth chatgpt` ở top-level, `login` hoặc
   `exec`. Cơ chế fail-close được upstream hỗ trợ là
   `forced_login_method = "chatgpt"`, kết hợp `codex login status`/`codex doctor
   --json` trong chính environment block sẽ chạy agent.
2. Với default OpenAI provider của `0.146.0`, `codex exec` cho phép
   **`CODEX_API_KEY`** ghi đè auth lưu; mã hiện tại không dùng `OPENAI_API_KEY` làm
   implicit primary auth theo đường này. `OPENAI_API_KEY` vẫn phải bị loại vì custom
   provider, adapter và công cụ con có thể đọc nó. Bug report về
   `OPENAI_API_KEY` ở `0.114.0` không đủ để mô tả hành vi `0.146.0`.

Với Claude, đề xuất đúng: trong `claude -p`, `ANTHROPIC_API_KEY` luôn thắng OAuth
subscription khi hiện diện. Claude interactive hỏi chấp thuận một lần rồi ghi nhớ lựa
chọn. Thứ tự đầy đủ còn đặt cloud-provider flags và `ANTHROPIC_AUTH_TOKEN` cao hơn API
key, nên gate không được chỉ kiểm một biến.

## Bảng phán quyết

| Tuyên bố | Phán quyết | Bằng chứng / điều chỉnh |
|---|---|---|
| Codex CLI hiện có `--auth chatgpt` để ghim auth cho mỗi lần gọi | **Sai** | Help thực tế của `0.146.0` không có cờ này. Parser upstream chỉ có browser/device login, `--with-api-key` và `--with-access-token`. [CLI source `rust-v0.146.0`](https://github.com/openai/codex/blob/rust-v0.146.0/codex-rs/cli/src/main.rs#L426-L469) |
| Cách chính thức để buộc Codex dùng ChatGPT auth | **Đúng nếu dùng config** | Schema nhận `forced_login_method = "chatgpt"`; `codex exec` gọi `enforce_login_restrictions` và thoát lỗi nếu auth đang là API key. [config schema](https://github.com/openai/codex/blob/rust-v0.146.0/codex-rs/core/config.schema.json), [exec enforcement](https://github.com/openai/codex/blob/rust-v0.146.0/codex-rs/exec/src/lib.rs#L484-L500), [auth enforcement](https://github.com/openai/codex/blob/rust-v0.146.0/codex-rs/login/src/auth/manager.rs#L1083-L1114) |
| `OPENAI_API_KEY` luôn âm thầm thắng ChatGPT OAuth trong Codex interactive và `exec` hiện tại | **Sai/quá rộng** | Tag `0.146.0` chỉ áp implicit env override qua `CODEX_API_KEY`; loader ghi rõ biến đó thắng mọi auth. Interactive TUI tắt env override, còn `exec` bật nó. [auth loader](https://github.com/openai/codex/blob/rust-v0.146.0/codex-rs/login/src/auth/manager.rs#L1217-L1230), [exec](https://github.com/openai/codex/blob/rust-v0.146.0/codex-rs/exec/src/lib.rs#L563-L577), [TUI](https://github.com/openai/codex/blob/rust-v0.146.0/codex-rs/tui/src/lib.rs#L554-L569) |
| Có thể xác nhận Codex auth mà không đọc token | **Đúng** | Tài liệu chính thức chỉ dẫn `codex login status`; `codex doctor --json` hiện cũng xuất báo cáo redacted. ChatGPT login và API-key login có billing khác nhau. [OpenAI authentication](https://learn.chatgpt.com/docs/auth) |
| `ANTHROPIC_API_KEY` thắng Claude Max login | **Đúng, có khác biệt interactive/non-interactive** | Trong interactive, người dùng phải approve một lần; trong `-p`, key luôn được dùng khi có. Thứ tự còn gồm cloud provider, `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, OAuth token và `/login`. [Claude authentication](https://code.claude.com/docs/en/authentication), [environment variables](https://code.claude.com/docs/en/env-vars) |
| `Remove-Item Env:X` chứng minh shell sau/orchestrator sạch | **Sai** | Process/User/Machine là các scope khác nhau; User/Machine tồn tại bền vững. Child mặc định kế thừa environment block của parent nhưng parent có thể truyền một block riêng. [PowerShell environment variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables), [Win32 process inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance) |
| AO tự bảo đảm subscription auth | **Sai nếu hiểu tuyệt đối** | AO chạy binary trong worktree, thêm một số biến nhưng nói rõ credential đến từ nơi CLI vốn đọc; AO không pin auth mode. [AO Claude adapter](https://aoagents.dev/docs/plugins/agents/claude-code/), [AO Codex adapter](https://aoagents.dev/docs/plugins/agents/codex/) |
| Bernstein tự loại API key khỏi child | **Sai** | Bernstein tạo filtered env, nhưng adapter Claude chủ động allow `ANTHROPIC_API_KEY`; adapter Codex allow `OPENAI_API_KEY`, `OPENAI_ORG_ID`, `OPENAI_BASE_URL`. Nó cũng giữ HOME/USERPROFILE để CLI đọc login local. [Claude adapter](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/adapters/claude.py), [Codex adapter](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/adapters/codex.py), [env isolation](https://github.com/sipyourdrink-ltd/bernstein/blob/main/src/bernstein/adapters/env_isolation.py) |
| `internal_llm_provider` của Bernstein bắt buộc dùng API riêng | **Sai** | Bernstein cho phép dùng adapter `codex`, `claude`, `ollama` và các adapter khác làm provider nội bộ. Nhưng provider CLI vẫn nhận env theo adapter, nên subscription-only phải được ép ở spawn boundary. [Bernstein README](https://github.com/sipyourdrink-ltd/bernstein#readme), [configuration](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/operations/CONFIG.md) |
| Codex cloud GitHub review có thể giữ lại mà không dùng local API key | **Đúng** | Codex cloud yêu cầu ChatGPT sign-in; GitHub review là cloud integration. Local env gate không chứng minh exact model của cloud reviewer. [OpenAI authentication](https://learn.chatgpt.com/docs/auth), [GitHub code review](https://learn.chatgpt.com/docs/third-party/github) |
| `claude-code-action` có thể dùng OAuth subscription | **Đúng, có điều kiện** | Action hỗ trợ `CLAUDE_CODE_OAUTH_TOKEN` tạo bởi `claude setup-token`; token phải ở GitHub Secret. Không truyền đồng thời API key. Chính sách billing non-interactive hiện hành vẫn phải được theo dõi. [Action setup](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md), [Claude authentication](https://code.claude.com/docs/en/authentication), [billing notice](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) |

## Windows: điều gì thực sự được kế thừa

`$Env:X` là giá trị trong process hiện tại. `Remove-Item Env:X` chỉ sửa block đó và
những child tạo sau sẽ kế thừa bản đã sửa **nếu** parent không truyền block khác. Giá trị
User/Machine vẫn nằm trong registry và có thể xuất hiện trong process mới do một launcher
khác tạo. Ngược lại, thay User/Machine không hồi tố block của process đang chạy.

Vì vậy cần kiểm Process/User/Machine để tìm nguồn cấu hình bền, nhưng gate quyết định phải
kiểm **environment block cuối cùng sau khi orchestrator đã lọc/overlay secret**, ngay trước
`CreateProcess`/`subprocess.Popen`. Bernstein là ví dụ rõ: shell cha sạch không nói lên điều
gì nếu secrets provider overlay lại key; shell cha có key cũng không đồng nghĩa mọi key đều
lọt qua, vì Bernstein dùng allowlist.

## Thiết kế fail-close đã sửa

### Lane Codex local

1. Wrapper dựng một environment block mới theo allowlist; không dùng `Remove-Item` làm gate.
2. Từ chối nếu child env còn `CODEX_API_KEY`, `OPENAI_API_KEY`, `OPENAI_BASE_URL` hoặc env key
   của bất kỳ custom provider nào; pin built-in provider `openai`.
3. Gọi Codex với CLI override ở cấp cao nhất:

   ```powershell
   codex exec --strict-config `
     -c 'forced_login_method="chatgpt"' `
     -c 'model_provider="openai"' `
     -m 'gpt-5.6-sol' <prompt>
   ```

4. Trước spawn thật, trong **cùng child env**, yêu cầu `codex login status` trả đúng
   `Logged in using ChatGPT`; chạy `codex doctor --json` và lưu phần redacted về auth/env.
5. Lưu receipt gồm CLI version, exact argv đã redaction, SHA, hash của danh sách tên biến
   child env, output preflight và exit code. Không lưu giá trị secret.

`forced_login_method` là enforcement, không phải chỉ là phép đo. Nếu key/stored auth sai,
`exec` phải dừng. Cờ tưởng tượng `--auth chatgpt` phải bị loại khỏi mọi prompt/script.

### Lane Claude local

1. Dựng child env mới và loại `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`,
   `ANTHROPIC_BASE_URL`, `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` và
   `CLAUDE_CODE_USE_FOUNDRY`. Với local `/login`, cũng không inject
   `CLAUDE_CODE_OAUTH_TOKEN`.
2. Trong đúng child env, chạy `claude auth status --json`; chỉ tiếp tục khi
   `loggedIn=true`, `authMethod="claude.ai"`, `subscriptionType="max"` (hoặc tier
   subscription được cho phép).
3. Chạy `claude -p` bằng cùng environment block; lưu status JSON đã bỏ email/account id,
   version, model, SHA và exit code vào receipt.

Trên máy đo, preflight đã cho bằng chứng dương đã redaction:

```json
{"loggedIn":true,"authMethod":"claude.ai","subscriptionType":"max"}
```

### AO/Bernstein

- **AO:** cần launcher/shim bao cả preflight và agent command; tài liệu AO không cung cấp
  auth-mode lock. Chỉ kiểm shell trước khi gọi `ao` là chưa đủ.
- **Bernstein:** cần patch/wrapper tại spawn boundary để bỏ provider API variables khỏi
  `extra_keys` và kiểm status trong env mà `build_filtered_env` thực sự trả về. Chỉ cấu hình
  `internal_llm_provider: codex` không tạo ra bảo đảm subscription.
- Cả hai phải fail trước model call nếu receipt preflight thiếu/sai; không fallback sang
  provider khác, tier khác hoặc API key.

## GitHub lanes

- **Codex cloud review:** giữ làm reviewer bổ sung dùng quyền lợi ChatGPT; nó độc lập với
  local env gate và chưa phải bằng chứng exact `gpt-5.6-sol`.
- **Claude Code Action:** chỉ truyền `CLAUDE_CODE_OAUTH_TOKEN`, pin Action bằng commit SHA,
  quyền GitHub read-only và dừng nếu billing policy đổi. GitHub Secrets không tự xuất thành
  env nếu workflow không tham chiếu, nên đừng truyền `ANTHROPIC_API_KEY` vào job.
- GitHub Actions tất định vẫn chạy Windows/Linux trên exact head SHA; các auth receipt không
  thay thế test evidence.

## Chốt kiến trúc

Giữ Protocol D0. Dùng Claude/Codex local làm lane chính; Codex cloud review và Claude OAuth
Action là lane GitHub bổ sung. Chưa đưa AO/Bernstein vào production cho đến khi có spawn
wrapper tạo child env allowlist, enforcement auth và receipt dương như trên.
