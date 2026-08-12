# Kiểm chứng `--bare` và cổng xác thực subscription của Claude/Codex

- **Ngày đo:** 2026-08-05 (Asia/Saigon)
- **Binary cục bộ:** Claude Code `2.1.221`; Codex CLI `0.146.0`
- **Phạm vi:** kiểm chứng các tuyên bố trong phương án đính kèm về `--bare`,
  `claude auth status --json`, khoảng hở preflight/executor và tính fail-close của
  `forced_login_method`.
- **Nguồn:** hành vi của đúng binary cục bộ, tài liệu chính thức Anthropic/OpenAI và
  mã nguồn `openai/codex`. Không dùng bài tổng hợp bên thứ ba làm bằng chứng.
- **An toàn:** không in email, organization UUID hay credential; không gửi model request
  Claude trong các phép đo; phản chứng Codex dùng `CODEX_HOME` tạm và API key giả.

## Kết luận

Phương án đính kèm phát hiện đúng lỗ **khác argv/môi trường giữa preflight và
executor**, và đúng rằng `--bare` không dùng OAuth subscription. Tuy nhiên nó sai ở hai
điểm quan trọng:

1. Trên chính máy này, `claude auth status --json` khi đăng nhập subscription **có**
   `subscriptionType`; payload gồm bảy trường. Payload chỉ còn ba trường trong lần gọi
   `--bare` chưa đăng nhập, nên schema là có điều kiện và thiếu trường phải làm gate đỏ.
2. Tính fail-close của Codex không phải suy đoán. Tài liệu OpenAI nói rõ credential sai
   restriction sẽ bị logout và tiến trình thoát; mã nguồn thực thi đúng điều đó trước
   phiên `codex exec`; phản chứng trên binary `0.146.0` cũng trả `rc=1` trước model call.

Ngoài ra, phương án bỏ sót cổng native mạnh hơn cho Claude Code `2.1.212+`: triển khai
**managed settings** gồm `forceLoginMethod: "claudeai"` và `forceLoginOrgUUID`. Hai khóa
này được kiểm ngay khi mỗi tiến trình Claude khởi động và chặn API key/token/helper không
xác minh được organization. Chúng không chặn Bedrock/Vertex/Foundry, nên wrapper vẫn phải
loại các đường cloud-provider và kiểm chính argv/environment sắp spawn.

## Bảng phán quyết

| Tuyên bố | Phán quyết | Bằng chứng / điều chỉnh |
|---|---|---|
| Claude Code `2.1.221` có `--bare` | **Đúng** | `claude --help` cục bộ và [tài liệu headless chính thức](https://code.claude.com/docs/en/headless) đều có cờ này. |
| `--bare` ép dùng API key | **Đúng về rủi ro, nhưng diễn đạt quá tuyệt đối** | Nó bỏ OAuth/keychain; Anthropic auth chỉ còn `ANTHROPIC_API_KEY` hoặc `apiKeyHelper`. Bedrock/Vertex/Foundry vẫn dùng credential riêng. Không có nguồn credential thì nó thất bại, không tự sinh API key. [Headless/bare mode](https://code.claude.com/docs/en/headless) |
| Preflight bình thường có thể xanh nhưng executor `--bare` không còn OAuth | **Đúng, đã tái hiện** | Cùng binary và máy: normal status là `claude.ai/max`; `--bare auth status` trả `rc=1`, `loggedIn=false`, `authMethod=none`. |
| Payload thật không có `subscriptionType` | **Sai trên máy đích** | Normal status có bảy trường: `loggedIn`, `authMethod`, `apiProvider`, `email`, `orgId`, `orgName`, `subscriptionType`. Payload `--bare` chưa đăng nhập chỉ có ba trường đầu. |
| `apiProvider` là tín hiệu thay thế cho `subscriptionType` | **Sai nếu dùng một mình** | Lần `--bare` chưa đăng nhập vẫn báo `apiProvider=firstParty`; gate phải kiểm đồng thời trạng thái, phương thức, provider và plan. |
| `forced_login_method` chưa được tài liệu hóa là fail-close | **Sai** | [OpenAI Authentication](https://developers.openai.com/codex/auth) ghi rõ credential không khớp sẽ bị logout và tiến trình thoát. |
| Cần bơm API key giả để chứng minh Codex không gọi API | **Hợp lý như regression probe, và đã làm an toàn** | Với `CODEX_HOME` tạm, `CODEX_API_KEY` giả và `forced_login_method="chatgpt"`, Codex `0.146.0` trả `rc=1` với thông báo yêu cầu ChatGPT login. |
| Claude chỉ có thể được bảo vệ bằng wrapper preflight | **Sai/thiếu** | Claude Code `2.1.212+` có managed `forceLoginMethod` và `forceLoginOrgUUID`; [tài liệu auth](https://code.claude.com/docs/en/authentication) mô tả exit khi organization sai và chặn API env/token/helper. |

## 1. Kết quả hành vi Claude Code `2.1.221`

### 1.1. Semantics thật của `--bare`

`claude --help` cục bộ mô tả `--bare` là minimal mode, đặt
`CLAUDE_CODE_SIMPLE=1`, bỏ hooks/LSP/plugin sync/attribution/auto-memory/prefetch,
keychain và auto-discovery `CLAUDE.md`. Phần auth nói rõ OAuth và keychain **không bao
giờ được đọc**; Anthropic auth chỉ lấy từ `ANTHROPIC_API_KEY` hoặc `apiKeyHelper` được
truyền qua `--settings`; ba cloud provider dùng credential riêng. Tài liệu Anthropic
cũng nói `--bare` là mode được khuyến nghị cho script nhưng không đọc
`CLAUDE_CODE_OAUTH_TOKEN`: [programmatic/headless](https://code.claude.com/docs/en/headless),
[authentication](https://code.claude.com/docs/en/authentication).

Vì vậy lane subscription không được dùng `--bare`. Nếu cần bỏ customization nhưng vẫn
giữ OAuth, binary `2.1.221` có `--safe-mode`; phép đo
`claude --safe-mode auth status --json` vẫn trả `claude.ai`, `firstParty`, `max`. Đây là
lựa chọn phù hợp hơn cho runner nhận toàn bộ instruction bằng prompt rõ ràng. Nếu runner
cần `CLAUDE.md` của repo, không dùng `--safe-mode`; thay vào đó phải audit các settings
và customization được load.

### 1.2. Schema `auth status --json` là có điều kiện

Không in trường nhận dạng cá nhân, phép đo chỉ giữ tên trường, type và bốn giá trị policy:

```text
claude auth status --json
rc=0
fields=loggedIn,authMethod,apiProvider,email,orgId,orgName,subscriptionType
policy values=true,claude.ai,firstParty,max

claude --bare auth status --json
rc=1
fields=loggedIn,authMethod,apiProvider
policy values=false,none,firstParty,<missing>
```

Điều này giải thích vì sao một môi trường/container chưa đăng nhập có thể chỉ thấy ba
trường. Nó không cho phép kết luận `subscriptionType` không tồn tại trong contract của
binary. Với phiên bản đang pin, gate đúng phải fail-close nếu bất kỳ điều kiện nào sai
hoặc thiếu:

```text
loggedIn         == true
authMethod       == "claude.ai"
apiProvider      == "firstParty"
subscriptionType == "max"
```

Khi nâng Claude Code, phải chạy contract probe lại trước khi nhận schema mới. Không ghi
`email`, `orgId` hoặc `orgName` vào log/Issue; chỉ so sánh organization trong bộ nhớ.

## 2. TOCTOU và cổng Claude native

Nhận xét “status ở process A không chứng minh process B” là đúng. Phản chứng normal so
với `--bare` cho thấy chỉ cần đổi argv là auth semantics đã đổi. Environment, settings,
credential file hoặc provider flags cũng có thể đổi giữa hai process.

Tuy vậy, kết luận “gate phải nằm trong cùng model invocation” chưa chỉ ra primitive thực
tế. Claude không có cờ `--require-subscription` cho một model request. Cách đóng phần lớn
khoảng hở là dùng policy được chính executor kiểm ở startup:

```json
{
  "forceLoginMethod": "claudeai",
  "forceLoginOrgUUID": "<UUID đọc từ status, không ghi log>"
}
```

Theo [Claude authentication](https://code.claude.com/docs/en/authentication), từ
`2.1.212` mọi first-party login path thực thi `forceLoginMethod`; khi dùng cả hai khóa,
CLI thoát nếu credential thuộc organization khác. `ANTHROPIC_API_KEY`,
`ANTHROPIC_AUTH_TOKEN` và `apiKeyHelper` cũng bị chặn vì không thể xác minh membership.
Nhưng cloud-provider sessions không bị chặn và phải được hạn chế bằng cloud IAM hoặc
wrapper.

Trên Windows, policy không thể override nên nằm ở
`C:\Program Files\ClaudeCode\managed-settings.json` hoặc HKLM policy. Tài liệu chính thức
liệt kê vị trí và precedence tại [Claude Code settings](https://code.claude.com/docs/en/configuration).
Tại thời điểm đo, máy này không có managed file/drop-in và không có policy key HKLM/HKCU,
nên cổng native **chưa được triển khai**.

Managed policy biến phần race “credential đổi sang API giữa status và task” thành lỗi
startup thay vì PAYG đối với first-party auth. Phần còn lại cần wrapper:

- tạo một environment block đã kiểm soát; loại `ANTHROPIC_API_KEY`,
  `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL` và các cờ kích hoạt Bedrock/Vertex/Foundry;
- pin/kiểm `CLAUDE_CONFIG_DIR` và không nhận `--settings` tùy ý có `apiKeyHelper`;
- từ chối `--bare`; cân nhắc bắt buộc `--safe-mode` cho lane có prompt self-contained;
- tạo argv ở controller, không nối chuỗi lệnh từ Issue/prompt và không cho caller thêm cờ;
- chạy status với cùng policy/environment ngay trước executor; thiếu trường hoặc JSON lỗi
  là fail; sau đó spawn executor từ chính object argv/environment đã validate;
- xác minh `/status` hoặc `claude doctor` cho thấy nguồn managed settings đang active.

Usage dashboard sau canary là bằng chứng hậu kiểm hữu ích, không thay thế cổng trước khi
gửi request.

## 3. `forced_login_method` của Codex đã được chứng minh fail-close

Ba lớp bằng chứng độc lập cùng hướng:

1. [OpenAI Authentication](https://developers.openai.com/codex/auth) nói thẳng: khi active
   credential không khớp restriction, Codex logout và exit.
2. Trong [`login/src/auth/manager.rs`](https://github.com/openai/codex/blob/main/codex-rs/login/src/auth/manager.rs),
   `enforce_login_restrictions` bật đọc `CODEX_API_KEY`; env key được ưu tiên hơn stored
   auth. Nếu policy cần ChatGPT nhưng thấy API key, hàm gọi logout và trả lỗi.
3. Trong [`exec/src/lib.rs`](https://github.com/openai/codex/blob/main/codex-rs/exec/src/lib.rs),
   `codex exec` gọi hàm enforce trước khi khởi tạo phiên agent; lỗi được in rồi tiến trình
   thoát `1`.

Phản chứng cục bộ, không đụng auth thật:

```text
CODEX_HOME=<empty temporary directory>
CODEX_API_KEY=<fake>
codex exec --skip-git-repo-check \
  -c 'forced_login_method="chatgpt"' 'Reply only OK'

rc=1
ChatGPT login is required, but an API key is currently being used. Logging out.
```

Không có model response; thư mục auth tạm vẫn rỗng và đã được xóa. Do enforcement có tác
dụng phụ logout, production wrapper vẫn phải loại `CODEX_API_KEY` trước khi gọi Codex để
không xóa cache ChatGPT thật. Nên giữ cả bốn lớp:

```text
environment sạch: CODEX_API_KEY/OPENAI_API_KEY và provider overrides không tồn tại
model_provider = "openai"
forced_login_method = "chatgpt"
codex login status trong đúng môi trường con phải báo ChatGPT
```

Regression probe bằng fake key nên chạy với `CODEX_HOME` tạm sau mỗi lần nâng CLI, không
bao giờ chạy trên home auth thật.

## 4. Cổng khuyến nghị cuối cùng

### Claude subscription lane

1. Cài managed `forceLoginMethod="claudeai"` + `forceLoginOrgUUID=<expected>`.
2. Controller dựng allowlist environment và argv; chặn API/helper/base-url/cloud-provider,
   `--bare` và settings không thuộc controller.
3. Dùng cùng `--safe-mode`/model/tool policy cho status và executor nếu prompt là
   self-contained.
4. Bắt buộc quartet `true/claude.ai/firstParty/max`; mọi thiếu/sai đều dừng.
5. Executor tự kiểm managed policy lần nữa khi startup; CI/hậu kiểm chỉ là lớp bổ sung.

### Codex ChatGPT lane

1. Controller loại API/provider env và pin provider OpenAI.
2. Mỗi `codex exec` mang `-c 'forced_login_method="chatgpt"'`.
3. `codex login status` phải báo ChatGPT trong đúng child context.
4. Giữ fake-key regression test bằng isolated `CODEX_HOME` khi đổi version.

Kiến trúc tổng thể D0 → Opus executor → Codex reviewer → deterministic CI → cloud review
bổ sung → Fable adjudicator → human merge không cần đổi. Phần phải đổi là đặt cổng auth
native + wrapper ngay trước từng model lane, không coi một preflight shell rời rạc là bằng
chứng đủ.
