# GitHub CLI nhất quán trên Claude, Codex và local

- **Ngày nghiên cứu:** 2026-08-16 (Asia/Saigon)
- **Mục tiêu:** làm `gh` chạy ổn định trên terminal local Windows/POSIX,
  Claude Code local/cloud và Codex Desktop/CLI sandbox mà không phát tán token
  vào mọi tiến trình con.
- **Bản đo tại máy:** GitHub CLI `2.95.0`, Codex CLI `0.146.0`, Claude
  Code `2.1.233`.
- **Nguồn:** manual, tài liệu và mã nguồn chính thức của GitHub,
  OpenAI và Anthropic. Không đọc hay ghi giá trị token.

## Kết luận

Không có một credential store duy nhất vừa portable vừa an toàn cho cả ba
môi trường. Thiết kế đúng là **một contract chung, nhiều backend auth**:

| Runtime | Backend nên dùng | Bề mặt token |
|---|---|---|
| Local Windows/macOS/Linux có desktop | `gh auth login --web`, OS credential store | Token không ambient |
| Claude native Windows local | Credential store của user chạy Claude | Token không ambient |
| Claude macOS/Linux/WSL2 sandbox | `GH_TOKEN` chế độ `mask`, proxy inject vào `api.github.com` | Shell chỉ thấy sentinel |
| Claude cloud | Ưu tiên built-in GitHub proxy; `gh + GH_TOKEN` chỉ là fallback | Fallback có token trong environment |
| Codex elevated Windows sandbox | Chạy `gh` ở host-user context qua approval | Dùng keyring host, không copy secret |
| Remote/headless tổng quát | Inject `GH_TOKEN` chỉ vào process tree `gh`/`git` | Không ambient |

Launcher phải:

1. chụp **tên/hiện diện** biến môi trường trước khi resolve tool;
2. chọn rõ lane `local-store`, `scoped-env`, hoặc `host-approved`;
3. tách `binary`, `identity`, `network`, `credential` và `capability` thành các
   trạng thái khác nhau;
4. không fallback sau khi một nguồn đã được chọn nhưng không
   hợp lệ;
5. đòi bằng chứng dương `gh auth status` và `gh api user` trong cùng
   environment block sẽ chạy lệnh thật.

## Bằng chứng thực nghiệm hôm nay

Snapshot chỉ ghi có/không:

| Biến | Hiện diện trong process |
|---|---:|
| `GH_TOKEN` | Không |
| `GITHUB_TOKEN` | Không |
| `GITHUB_PAT` | Có |
| `GH_CONFIG_DIR` | Không |

Kết quả dương đã được đo mà không in token:

- ngoài sandbox, `gh auth status` và `gh api user --jq .login` đều xanh
  bằng keyring của tài khoản `ducthangho`;
- ngoài sandbox, map child-only `GH_TOKEN=%GITHUB_PAT%` cũng xanh;
- trong Codex sandbox, cùng probe bị lỗi network `10013`;
- GitHub connector của Codex xác thực `ducthangho` theo một đường độc lập.

Vì vậy nhận định cũ “keyring/PAT invalid” là **false negative do sandbox**.
`CODEX_SANDBOX_NETWORK_DISABLED=1` chỉ là advisory: nó còn được inherit
ngoài sandbox trong phép đo này dù mạng đã chạy. Doctor không được
dùng biến đó thay cho positive network probe.

`GITHUB_PAT` không phải tên biến `gh` chính thức đọc. Chỉ launcher map
nó sang `GH_TOKEN` thì nó mới tham gia auth. Một PAT legacy có thể vô hình
đối với `gh` trực tiếp nhưng lại che store khi launcher map mù.

## Hành vi chính thức của GitHub CLI

### Thứ tự auth

Với `github.com`, thứ tự là `GH_TOKEN` → `GITHUB_TOKEN` → credential đã
lưu. Token env thắng credential store; `gh` không thử store nếu token env bị
thu hồi. Nguồn: [`gh help environment`](https://cli.github.com/manual/gh_help_environment)
và [`ActiveToken` v2.95.0](https://github.com/cli/cli/blob/v2.95.0/internal/config/config.go#L237-L260).

Hệ quả:

- local-store lane phải loại `GH_TOKEN`, `GITHUB_TOKEN`, `GITHUB_PAT` khỏi child;
- scoped-env lane chỉ chấp nhận một nguồn; token sai thì đỏ;
- `GITHUB_PAT` chỉ được map trong lane legacy tường minh.

### Lưu credential và `--with-token`

`gh auth login --web` mặc định lưu token trong system credential store. Nếu
không có keyring hoặc ghi keyring lỗi, `gh` **tự fallback sang plaintext trong
config file**; `--insecure-storage` chủ động chọn plaintext. Nguồn:
[`gh auth login`](https://cli.github.com/manual/gh_auth_login) và
[mã nguồn `Login`](https://github.com/cli/cli/blob/v2.95.0/internal/config/config.go#L322-L359).

Backend chính thức là macOS Keychain, Linux Secret Service/GNOME Keyring và
Windows Wincred; headless thường không có keyring. Xem [ghi chú phát hành
2.24.0](https://github.com/cli/cli/discussions/7109).

`gh auth login --with-token` đọc token qua stdin, không cần đặt trong argv.
Manual yêu cầu PAT classic có tối thiểu `repo`, `read:org`, `gist`, còn
fine-grained PAT nên dùng `GH_TOKEN`. Đường `--with-token` vẫn có thể
lưu credential và plaintext fallback, nên không tối ưu cho container phù du.

### `GH_CONFIG_DIR` không portable hóa keyring

`GH_CONFIG_DIR` chỉ chỉ định file config. Mặc định là
`$XDG_CONFIG_HOME/gh`, `%AppData%/GitHub CLI` trên Windows, rồi
`$HOME/.config/gh`. Nguồn:
[`gh help environment`](https://cli.github.com/manual/gh_help_environment).

Trỏ ba runtime vào cùng `GH_CONFIG_DIR` không biến Wincred/Keychain/Secret
Service thành portable, và có thể biến `hosts.yml` plaintext thành secret dùng
chung. Không chọn thiết kế này.

### Probe phải dùng exit code đúng

```text
gh auth status --active --hostname github.com
gh api user --jq .login
```

Không thêm `--show-token`. Không dùng `gh auth status --json` làm exit gate:
manual nói JSON mode luôn trả `0` khi có auth issue, trừ fatal error. Xem
[`gh auth status`](https://cli.github.com/manual/gh_auth_status).

## Thiết kế theo runtime

### 1. Terminal local Windows/POSIX

Thiết lập một lần dưới đúng OS user:

```text
gh auth login --hostname github.com --web
gh auth status --active --hostname github.com
gh auth setup-git --hostname github.com
```

`gh auth setup-git` cấu hình Git dùng `gh` làm credential helper; API xanh
không tự chứng minh `git fetch/push` xanh. Nguồn:
[`gh auth setup-git`](https://cli.github.com/manual/gh_auth_setup-git).

Sau login, kiểm `gh auth status` để biết token nằm trong keyring hay file;
không suy từ `rc=0` của login rằng nó đã được lưu an toàn. Trên
headless Linux không có keyring, bỏ login persistence và chuyển sang
scoped-env lane.

### 2. Claude Code local

Trên native Windows, Claude Desktop kế thừa User/System environment nhưng không
đọc PowerShell profile. Local Environment Editor mã hóa giá trị khi lưu
nhưng phân phát biến cho mọi local session và preview server. Vì vậy:

- đặt `PATH`/cờ không nhạy cảm ở editor nếu cần;
- không đặt PAT dài hạn tại đó;
- cho Claude dùng credential store của cùng user đã `gh auth login`.

Nguồn: [Claude Desktop environment
configuration](https://code.claude.com/docs/en/desktop#environment-configuration).

Trên macOS/Linux/WSL2, Claude Code có cơ chế tốt hơn khi phải dùng token:
`sandbox.credentials.envVars` với `mode: "mask"`. Tiến trình thấy sentinel,
proxy chỉ thay token thật cho host cho phép; tài liệu có chính ví dụ
`GH_TOKEN` → `api.github.com`. Cấu hình phải ở user/managed settings hoặc
`--settings`; project settings không được phép bật masking/TLS termination.
Bash sandbox này không hỗ trợ native Windows. Xem [Claude Code sandbox:
mask environment variables](https://code.claude.com/docs/en/sandboxing#mask-environment-variables).

`SessionStart` có thể ghi `export` vào `CLAUDE_ENV_FILE`, và mọi lệnh Bash
sau đó sẽ nhận các biến này. Do đó hook chỉ nên ghi `PATH`,
`GH_CONFIG_DIR` hoặc metadata không nhạy cảm; không ghi token. Xem
[Claude hooks reference](https://code.claude.com/docs/en/hooks#persist-environment-variables).

### 3. Claude cloud/remote

Tuyến ưu tiên là built-in GitHub tools. Chúng đi qua GitHub proxy và token
không vào container. `gh` không được cài sẵn. Khi cần lệnh chưa được
built-in tools phủ, ví dụ `gh release` hay `gh workflow run`, Anthropic hướng
dẫn cài `gh` trong setup script, đặt `GH_TOKEN` trong cloud environment và
không chạy `gh auth login`.

Cloud environment hiện chưa có dedicated secrets store; environment variables
hiển thị cho người có quyền sửa environment. Vì vậy `gh` là fallback có
đánh đổi. Dùng fine-grained PAT tối thiểu quyền, expiry ngắn và môi
trường có ít người được sửa. Nguồn: [Claude Code on the web —
GitHub tools and credentials](https://code.claude.com/docs/en/claude-code-on-the-web#work-with-github-issues-and-pull-requests).

### 4. Codex Desktop/CLI sandbox

Codex elevated Windows sandbox dùng dedicated lower-privilege users. Không được giả
định shell sandbox nhìn thấy Wincred, `%AppData%` hay `USERPROFILE` của user
host. `CODEX_HOME` có thể sửa Codex auth nhưng không sửa GitHub auth.
Nguồn: [OpenAI Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox)
và [Codex environment variables](https://learn.chatgpt.com/docs/config-file/environment-variables).

Bằng chứng thực tế hôm nay cho thấy network `10013` xảy ra trước khi có
thể kết luận credential. Vì vậy tuyến ưu tiên là:

1. lệnh `gh` cần mạng được Codex xin approval để chạy ngoài sandbox;
2. launcher scrub cả ba token env, rồi probe credential store trong host-user context;
3. chỉ cho lệnh thật chạy nếu identity, `gh auth status` và API canary cùng
   xác nhận đúng lane;
4. nếu runner ngoài sandbox vẫn là identity khác, fail closed.

Khi bắt buộc chạy `gh` trong sandbox, broker inject `GH_TOKEN` chỉ vào process
tree `gh`, hoặc `git` có credential helper `gh`; không đặt token trong môi
trường chung của Codex. Lane này còn cần network permission. Xem [Codex
config reference: `sandbox_workspace_write.network_access`](https://learn.chatgpt.com/docs/config-file/config-reference#sandbox_workspace_write-network_access).

Codex hardening nên đặt tường minh:

```toml
[shell_environment_policy]
inherit = "core"
ignore_default_excludes = false

[shell_environment_policy.filters]
"GH_TOKEN" = "exclude"
"GITHUB_TOKEN" = "exclude"
"GITHUB_PAT" = "exclude"
"CODEX_AUTH_JSON" = "exclude"
```

Tài liệu Codex hiện nói `ignore_default_excludes` mặc định `true`, nghĩa
là không tự loại tên chứa `KEY`, `SECRET`, `TOKEN`. `set` chạy sau
exclusions và có thể đưa secret trở lại, nên không dùng
`shell_environment_policy.set` để chuyển token. Nguồn: [OpenAI Advanced
Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced#shell-environment-policy).

Codex CLI `0.146.0` trên máy đã được kiểm bằng `--strict-config`:
cả `filters` mới và `exclude` legacy đều được parser chấp nhận.

## Scoped-env launcher

Với remote/headless, không export token toàn session. Launcher dựng một
environment block riêng:

```text
parent snapshot
  ├─ remote-official: child.GH_TOKEN = snapshot.GH_TOKEN
  ├─ remote-legacy:   child.GH_TOKEN = snapshot.GITHUB_PAT
  └─ child chỉ chạy gh/git; sibling processes không nhận token
```

Quy tắc:

- `GH_TOKEN` và `GITHUB_TOKEN` cùng có: báo xung đột, không đoán;
- official token có nhưng sai: đỏ, không fallback;
- `GITHUB_PAT` chỉ map khi lane là `remote-legacy` và không có official token;
- token không vào argv, stdout/stderr, receipt, command log, `CLAUDE_ENV_FILE`
  hay Codex `set`;
- receipt chỉ ghi source name, executable/version, host, exit code, username
  canary, repo permissions và hash danh sách **tên** biến.

Nếu chạy `git` qua `gh auth setup-git`, scoped `GH_TOKEN` phải bao process tree
`git`, vì Git sẽ sinh credential-helper `gh`. Chỉ bơm token vào
`gh auth status` rồi chạy `git push` trong environment khác là gate không có
nghĩa.

## Trạng thái doctor phải tách

Doctor không được gộp mọi probe failure thành `credential_invalid`:

| Trạng thái | Dấu hiệu | Hành động |
|---|---|---|
| `binary_missing` | không resolve/chạy được `gh` | cài/sửa PATH |
| `identity_mismatch` | user/profile không phải lane mong đợi | dừng, chọn host lane |
| `infra_blocked` | socket/network policy chặn, ví dụ `10013` | `needs_host_execution` |
| `credential_missing` | mạng xanh nhưng không có source | login/inject source |
| `credential_invalid` | mạng xanh, GitHub trả auth failure | thu hồi/cấp lại |
| `capability_missing` | user canary xanh nhưng repo/scope không đủ | cấp least privilege |
| `ready` | status + user + repo canary xanh | cho lệnh thật chạy |

Phân loại network phải dựa vào lỗi probe và positive connectivity, không
dựa riêng vào `CODEX_SANDBOX_NETWORK_DISABLED`. Bằng chứng hôm nay đã
chứng minh biến advisory có thể còn tồn tại trong host execution nơi mạng
thực tế chạy được.

## GitHub App có phù hợp không?

GitHub App installation token phù hợp cho automation không cần danh tính người
dùng. Token có thể giới hạn repository/permission và hết hạn sau một giờ.
Nguồn: [GitHub App authentication overview](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app)
và [installation access token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app).

Phương án dài hạn tốt cho automation là broker giữ GitHub App private
key bên ngoài agent, mint token một giờ, rồi inject token vào đúng process
`gh`/`git`. Không biến private key thành env secret của agent.

Không dùng GitHub App như drop-in cho mọi thao tác mang danh tính người
dùng; endpoint và attribution có thể khác user OAuth/PAT. Local developer lane
vẫn nên dùng browser OAuth + OS keyring.

## Ma trận test bắt buộc

Test unit dùng `gh` shim và canary token giả; test integration không in token.

| Ca | Store | Env | Hạ tầng | Kết quả cần |
|---|---|---|---|---|
| T1 local-store | hợp lệ | vắng | mạng xanh | `ready` |
| T2 official che store | hợp lệ | `GH_TOKEN` sai | mạng xanh | `credential_invalid`, không fallback |
| T3 precedence | hợp lệ | `GH_TOKEN` sai, `GITHUB_TOKEN` đúng | mạng xanh | đỏ vì `GH_TOKEN` thắng |
| T4 remote official | vắng | `GH_TOKEN` đúng | mạng xanh | `ready`, chỉ child thấy token |
| T5 remote legacy | vắng | PAT legacy đúng | mạng xanh | xanh sau map child-only |
| T6 local có PAT ambient | hợp lệ | PAT legacy bất kỳ | mạng xanh | store xanh; PAT bị scrub |
| T7 hai official source | bất kỳ | cả hai có | mạng xanh | đỏ do ambiguity |
| T8 keyring khác identity | hợp lệ ở host | vắng | sandbox user | `identity_mismatch` |
| T9 network bị chặn | hợp lệ | bất kỳ | `10013`/policy | `infra_blocked`, không auth-invalid |
| T10 token thu hồi | vắng | token sai | mạng xanh | `credential_invalid`, không fallback |
| T11 JSON mutant | sai | vắng | mạng xanh | test giết `--json` false-green |
| T12 leak | bất kỳ | canary giả | mạng giả | sibling env/log/argv không có canary |
| T13 Claude mask | vắng | token mask | allowed host | shell thấy sentinel |
| T14 Git helper | theo lane | theo lane | mạng xanh | `git ls-remote` cùng process tree xanh |

Mỗi ca integration phải chạy thật trên Windows và POSIX. Receipt cần
ghi account canary và repository đích, không chỉ `rc=0`. Không dùng write
API làm canary.

## Rollout đề nghị

1. **Inventory read-only:** ghi version/path `gh`, OS identity, lane, sự hiện diện
   của tên biến và config path; không ghi giá trị.
2. **Khóa local-store lane:** scrub token env, login dưới đúng user, kiểm
   keyring/file source, chạy API + Git canary.
3. **Khóa launcher:** tách lane và state, fail-closed, thêm T1–T12 và mutation
   cho precedence/JSON false-green.
4. **Claude:** native Windows dùng local store; macOS/Linux/WSL2 dùng official
   masking khi cần env token; cloud ưu tiên built-in proxy.
5. **Codex:** host-approved lane trên Windows thật; điều kiện xanh là đúng
   identity + store + network; không copy `hosts.yml` vào sandbox.
6. **Automation sau cùng:** nếu cần quyền không gắn người dùng, tạo
   GitHub App broker và rollout trước ở read-only repo scope.
7. **Quan sát 7 ngày:** receipt chỉ metadata; rollback về local-store và
   built-in connectors khi lane mới đỏ.

## Những phương án không chọn

- `inherit = "all"` để token lọt vào mọi shell Codex;
- ghi token vào Codex `set` hoặc `CLAUDE_ENV_FILE`;
- đặt PAT ở User/Machine environment trên Windows;
- chia sẻ `hosts.yml` plaintext hay `GH_CONFIG_DIR` giữa các identity;
- copy Wincred của host sang user sandbox;
- token trong argv, repo config, hook output hay receipt;
- official token hỏng rồi lặng lẽ fallback sang store;
- dùng `gh auth status --json` exit code làm gate;
- gọi lỗi socket/network là `credential_invalid`;
- xem GitHub App private key như env secret của agent.

## Phán quyết cho repo

Giữ **store-first chỉ ở local/host lane** và **official-token fail-closed ở
remote lane**. Launcher không nên có một thứ tự fallback chung.

Bản sửa tối thiểu sau nghiên cứu:

1. thêm chọn lane và state tường minh;
2. scrub token env trong local-store/host-approved lane;
3. scoped injection cho `gh` và process tree `git` trong remote lane;
4. khi Codex gặp network `10013`, trả `needs_host_execution`, không kết tội token;
5. Claude cloud dùng built-in proxy trước, `gh + GH_TOKEN` chỉ là fallback;
6. chạy ma trận test + mutation gate trước khi đổi auth hiện tại.
