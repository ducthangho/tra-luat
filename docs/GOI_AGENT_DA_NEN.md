# Gọi agent đa nền — tất định, không script spawn tự chế

**Phạm vi.** Cách gọi một phiên Claude hoặc Codex sao cho chạy *giống nhau* trên
máy Windows, macOS/Linux, điện thoại (qua phiên remote) và CI — và sao cho khi
hỏng thì hỏng ở chỗ đọc được.

## Nguyên tắc: chốt là của ta, việc gọi agent là của CLI chính thức

Chúng ta **không viết script spawn agent**. Hai CLI chính thức đã làm việc đó và
được nhà cung cấp bảo trì:

| agent | CLI | cài |
|---|---|---|
| Claude | `claude` | `npm install -g @anthropic-ai/claude-code` |
| Codex | `codex` | `npm install -g @openai/codex` |

`\.claude/dev/launcher.py` **không** gọi agent. Nó dựng các chốt quanh *bất kỳ*
lệnh nào rồi chạy lệnh đó. Nghĩa là nó không cần biết agent nào, không có prompt
dựng sẵn, không có logic phiên — CLI đổi giao diện thì ta không phải sửa gì.

Ranh giới đó là cố ý. Một wrapper spawn tự chế sẽ phải bám theo cờ, biến môi
trường và cơ chế xác thực của hai CLI khác nhau, rồi trôi lệch âm thầm — đúng
lớp lỗi mà `## Bài học đắt giá` trong `CLAUDE.md` đã trả giá nhiều lần.

## Trước tiên: đủ công cụ chưa

```bash
python .claude/dev/launcher.py doctor          # người đọc
python .claude/dev/launcher.py doctor --json   # máy đọc
```

Thoát `12` khi thiếu công cụ **bắt buộc** (git, python). Thiếu `claude`/`codex`
chỉ là cảnh báo — có phiên không cần gọi agent nào cả.

Đã đo trong container Claude Code web (12-08-2026): có `python`, `git`, `node`,
`claude`, `rg`; **không có** `codex`, `gh`, `pwsh`. Hook
`.claude/hooks/session-start.sh` cài `codex`, `claude` và `ripgrep` — **không** cài
`gh` và `pwsh`: kho này dùng GitHub qua MCP chứ không qua `gh`, và không còn đường
nào cần PowerShell.

**Không được giả định Windows có `python3`.** Bản cài phổ biến chỉ có `python` và
`py` (bản Microsoft Store thì có thêm `python3`). Đừng bắt cài thêm bí danh —
`doctor` nhận cả ba tên.

## Xác thực `codex` trên nhiều môi trường

`doctor` nói **có `codex`**, không nói **`codex` gọi được**. Hai chuyện khác nhau, và
chuyện thứ hai mới là thứ làm hỏng lượt chạy giữa chừng. Kiểm bằng lời khai của chính nó:

```bash
codex login status        # "Logged in using ChatGPT"  hoặc  "Not logged in"
```

### Đăng nhập ở máy KHÔNG có trình duyệt (container, server)

```bash
codex login --device-auth
```

In ra một link và một mã dùng một lần (hạn **15 phút**). Mở link trên thiết bị bất kỳ,
nhập mã, xong thì tiến trình tự hoàn tất và ghi `~/.codex/auth.json`. Đã đo 14-08-2026
trên container Claude Code web: chạy được, không cần khoá API — dùng thẳng tài khoản
ChatGPT.

> `codex login` **không** kèm `--device-auth` sẽ mở luồng qua trình duyệt cục bộ và
> **treo** ở máy không có trình duyệt. Đã đo: `timeout 30` phải giết nó.

### Để không phải nhập mã lại mỗi phiên

Container phiên remote là **phù du** — thu hồi là mất `~/.codex/auth.json`. Một chốt đòi
thao tác tay mỗi lượt thì sớm muộn bị bỏ qua, nên hook `.claude/hooks/session-start.sh`
khôi phục credential từ biến Environment `CODEX_AUTH_JSON` (base64 của `auth.json`),
đúng khuôn `GITHUB_PAT`.

Lấy chuỗi ấy — **chạy trên MÁY CỦA BẠN**, sau khi đã `codex login` ở đó:

```bash
base64 -w0 ~/.codex/auth.json     # Linux
base64 -i  ~/.codex/auth.json     # macOS
```

rồi dán thẳng vào phần Environment. **Đừng dán vào khung chat với agent, đừng commit,
đừng gửi qua issue/PR** — chuỗi đó chứa refresh token, tương đương mật khẩu tài khoản
ChatGPT của bạn cho mục đích codex. Lộ vào transcript là lộ hẳn, và transcript thì sống
lâu hơn phiên.

Hook có bốn chốt, mỗi cái bịt một đường hỏng đã lường:

| chốt | vì sao |
|---|---|
| không in giá trị, đọc từ **môi trường** chứ không qua đối số | đối số lộ trong `ps` cho mọi tiến trình cùng máy |
| **không đè** khi `codex login status` đã xanh | bản trên đĩa có thể mới hơn biến (codex tự làm mới token); đè bừa là hạ cấp một credential đang tốt |
| kiểm base64 + JSON + khoá `tokens` **trước khi** ghi | biến hỏng mà ghi đè thì đổi "chưa đăng nhập" (dễ đọc) thành "đăng nhập hỏng" (khó đọc) |
| ghi tệp tạm → `chmod 600` → `mv` | không hở khoảnh khắc quyền rộng, không để lại tệp nửa vời nếu chết giữa chừng |

Sau đó hook hỏi lại chính `codex login status` và in dòng đó ra — **bằng chứng dương**,
không suy từ việc "đã ghi tệp xong".

Nếu một ngày chuỗi hết hiệu lực (OpenAI thu hồi hoặc xoay refresh token), triệu chứng là
`Not logged in` dù biến vẫn còn. Chữa: `codex login --device-auth` lại rồi cập nhật biến.

### Codex có thấy `CODEX_AUTH_JSON` không — và cái giá để nó thấy

**Mặc định là KHÔNG**, và lý do không phải cái ai cũng đoán.

Mẫu loại trừ **mặc định** của codex chỉ có **ba**: `*KEY*` · `*SECRET*` · `*TOKEN*`.
`CODEX_AUTH_JSON` **không khớp cái nào**. Biến vô hình vì
`shell_environment_policy.inherit` mặc định chỉ truyền một **tập lõi**, chứ không phải vì
bộ lọc bí mật. (Tôi từng chẩn đoán nhầm là khớp `*AUTH*` — `*AUTH*` là mẫu tự gõ khi thử,
không có trong codex. Đo binary rồi mới ra.)

Lược đồ đầy đủ: `inherit` · `ignore_default_excludes` · `exclude` · `set` · `include_only`.

**Codex KHÔNG cần biến này để xác thực.** Nó đọc `~/.codex/auth.json`. Biến chỉ là *hạt
giống bền* để hook giải mã xuống đĩa **trước khi** codex khởi động. Mở biến ra chỉ thêm
một khả năng: phiên codex **tự tái dựng** được credential, và công cụ của kho chạy *bên
trong* sandbox thôi báo nhầm "không có biến".

#### ĐÃ THU HỒI (cross-review lượt 7, 16-08-2026) — đừng dựng lại

Hook **từng** ghi khối này, và nay hook **gỡ** nó đi:

```toml
[shell_environment_policy]
inherit = "all"                 # <- ĐÃ THU HỒI
exclude = ["GITHUB_PAT", "CLAUDE_CODE_SESSION_ID", …]
```

Lý lẽ bảo vệ nó là "phiên codex cần thấy biến để tự tái dựng credential". **Lý lẽ đó sai
ngay trong chính luồng hook**: khối khôi phục credential chạy TRƯỚC, đã ghi
`$CODEX_AUTH_JSON` ra `~/.codex/auth.json` rồi mới tới khối policy. Từ đó codex đọc
credential từ tệp chuẩn, không cần biến. Và nếu hook không chạy thì policy cũng không được
cài — nên nó **chưa bao giờ** là đường cứu hộ độc lập. Ta đổi **một** credential lấy **cả
môi trường** mà không mua được gì.

`exclude` cũng không cứu được: quét theo **tên** không chứng minh được gì cho `PGPASSWORD`,
`DATABASE_URL`, `REDIS_URL`, `SSH_AUTH_SOCK`, hay biến vendor mới; và nó lỗi thời đúng vào
lúc môi trường đổi — bên quên cập nhật chính là bên đẩy lọt. Danh sách chặn theo tên là
*bằng chứng về cái ta đã nghĩ tới*, không phải bằng chứng an toàn.

Đường thay thế đã đủ và rẻ hơn: **`codex login --device-auth`** đúc credential tại chỗ.

Việc phát hiện nằm ở `.claude/dev/codex_env_policy.py` (tách riêng để test được, `t100`).

**Công cụ KHÔNG ghi vào config của bạn.** Mặc định nó chỉ đọc: thấy khối cũ thì đặt cờ
`~/.codex/tra-luat-CHAN-CODEX` (mọi cửa codex *của kho* fail-close) và in cách chữa. Chạy
`--go` thì nó dựng bản đã gỡ ra `config.toml.tra-luat-da-go` **bên cạnh**; bạn `diff` rồi
tự `mv`. Bản gốc bất khả xâm ở mọi đường.

Lý do: bốn lượt cross-review liên tiếp tìm ra **bảy** lỗi, tất cả cùng thuộc việc tự động
ghi lại config — bảng TOML trùng tên, khớp substring mất dữ liệu, ghi không nguyên tử,
kiểm từng dòng vẫn mất dữ liệu, symlink tên tạm ghi đè tệp khác, CRLF đổi kết thúc dòng
toàn tệp, lost-update. Phần thưởng thì nhỏ: gỡ một khối chính ta thêm vào. Không đáng.

**TUYỆT ĐỐI KHÔNG** dùng `shell_environment_policy.set` để truyền giá trị qua dòng lệnh:
đối số lộ trong `ps` cho mọi tiến trình cùng máy.

### Refresh token XOAY VÒNG — vì sao ảnh chụp chết nhanh

Đây là chỗ đắt nhất, và nó đã cắn hai lần trong một ngày.

Mỗi lần codex làm mới token, nó ghi đè `~/.codex/auth.json` và **vô hiệu bộ cũ**. Chuỗi
base64 trong `CODEX_AUTH_JSON` là **ảnh chụp một thời điểm** — nó chết ngay khi bản trên
đĩa ở *bất kỳ máy nào* được làm mới.

Đo được 16-08-2026: chủ kho đăng nhập lại và dán chuỗi mới
(`last_refresh=2026-08-16T01:58`); hook đưa xuống đĩa **khớp từng byte**; codex vẫn trả
`refresh_token_invalidated`. Tức **ảnh chụp đã chết trước khi tới nơi** — giữa lúc chụp và
lúc dùng đã có một lượt xoay vòng khác.

**Quy trình chép cho đúng:**

1. `codex login` (hoặc `--device-auth`).
2. **Chép base64 NGAY**, trước khi chạy bất kỳ lệnh `codex` nào khác trên máy đó.
3. Dán vào Environment, rồi **mở phiên mới** (biến chỉ nạp lúc phiên khởi động).
4. **Đừng chạy `codex` trên máy cá nhân** trong lúc còn muốn dùng chuỗi đó ở phiên remote —
   mỗi lượt chạy có thể xoay vòng và giết chuỗi đã dán.

### `codex login status` NÓI DỐI — đừng dùng nó làm chốt

Nó chỉ kiểm tệp **đọc được**, không kiểm token còn **sống**. Đo được: trả rc=0
`Logged in using ChatGPT` trong khi mọi lời gọi thật trả 401 `refresh_token_invalidated`.

Đã trả giá **hai lần**:

- `launcher.py` từng dán nhãn `DUNG_DUOC` chỉ vì lệnh đó rc=0. Nay tách ba nhãn:
  `CO_CREDENTIAL` (có tệp, đọc được, chưa hết hạn — **chưa** chứng minh dùng được) ·
  `CHUA_XAC_THUC` (đo được là hỏng) · `DUNG_DUOC` (**chỉ** khi `--kiem-song` gọi thật).
- Hook từng dùng nó cho chốt "đã đăng nhập thì không ghi đè". Hậu quả **đo được**: bản trên
  đĩa đã bị thu hồi, biến có bản mới, mà chốt vẫn kết luận "đã đăng nhập sẵn, GIỮ nguyên"
  và **chặn bản mới** — chốt sinh ra để bảo vệ bản mới hơn lại đi bảo vệ đúng bản đã chết.
  Nay so **`last_refresh`** giữa đĩa và biến: đĩa mới hơn hoặc bằng thì giữ, cũ hơn thì thay.
  Mốc thời gian đo được và không nói dối.

### Khi hook ĐÚNG mà phiên vẫn hỏng — sự cố 15-08-2026

Mọi thứ ở mục trên đã đúng và đã có từ 14-08. Hôm sau một phiên vẫn mất gần trọn ngày
vì `codex login status` trả `Not logged in`, rồi **kết luận** "container không gọi được
codex" và bắt chủ kho chờ một máy khác. Không phải lỗi của hook, cũng không phải của tài
liệu này.

**Nguyên nhân gốc: phiên chạy hook của NHÁNH PACKET, không phải hook trên `master`.**
Nhánh packet rẽ từ `base_sha` cũ hơn commit thêm khối khôi phục credential, nên hook thật
sự chạy là bản chưa có khối ấy. Đo được:

| hook | `sha256` (16) | số lần nhắc `CODEX_AUTH_JSON` |
|---|---|---|
| cây phiên (`claude/wp55-r2g2-executor-…`) | `298d96fe51f70e4e` | **0** |
| `origin/master` | `3c3dd49a8a163479` | **5** |

Nên `codex login status` nói `Not logged in` còn tài liệu nói "hook lo rồi" — **hai câu
cùng đúng**, và đó là kiểu mâu thuẫn khó thấy nhất. `.claude/skills/work-packet/SKILL.md`
cảnh báo sẵn: *"`base_sha` thường cũ hơn công cụ trên nhánh chính, nên cây làm việc của
packet có thể thiếu cả bộ dựng công cụ lẫn hook phiên."*

Nay đo bằng máy thay vì bằng chữ:

```bash
python .claude/dev/launcher.py doctor        # muc `hook-phien` so bam voi origin/master
python .claude/dev/launcher.py moi-truong    # quet bien theo MAU, khong theo ten doan truoc
python .claude/dev/launcher.py chuan-bi      # duong CUU HO khi hook khong chay
```

**Hai lỗi nối tiếp, cùng một hình dạng, đều đã có tiền lệ trong `CLAUDE.md`:**

- Tìm biến bằng **danh sách tên đoán trước** (`OPENAI_API_KEY`, `CODEX_API_KEY`…) nên
  trượt đúng `CODEX_AUTH_JSON`. Y hệt bộ quét secrets lọc theo **phần mở rộng** rồi mù
  với `.env`. *Lọc theo danh sách đoán trước thì mù đúng chỗ thứ cần tìm đang nằm.*
- Ghi base64 **thô** vào `auth.json`, nhận `expected value at line 1 column 1`, rồi đọc
  thành "biến này không dùng được". Câu đó nói **tệp** không phải JSON — nó không hề nói
  **biến** sai.

### ĐÃ ĐẶT ≠ DÙNG ĐƯỢC — biến giữ chỗ

Cùng lượt đo phát hiện container có **năm** biến mang **cùng một chuỗi 14 ký tự** (cùng
vân tay `f07d7417`): `GH_TOKEN` · `GITHUB_TOKEN` · `AWS_ACCESS_KEY_ID` ·
`AWS_SECRET_ACCESS_KEY` · `CLOUDSDK_AUTH_ACCESS_TOKEN`. Credential GitHub **thật** nằm ở
`GITHUB_PAT` (93 ký tự, tiền tố `github_pat_`).

Biến giữ chỗ **tệ hơn** biến chưa đặt: công cụ báo "sai thông tin đăng nhập" thay vì
"chưa đăng nhập", và thông điệp ấy đẩy người đọc đi sai hướng. `moi-truong` gom biến theo
vân tay giá trị để phơi đúng chuyện này — chỉ gom biến **tên khớp mẫu bí mật** và **giá
trị dài ≥ 8**, vì nếu không thì tám biến cùng `"1"` và chín biến cùng `"true"` bị báo oan
(đã đo, đã sửa).

### GitHub: bốn đường, hỏng độc lập

| đường | trạng thái (đo 15-08-2026, container remote) |
|---|---|
| `git` đẩy/kéo HTTPS | **CHẠY** — credential qua `$GIT_CONFIG_KEY_*` |
| công cụ **MCP github** | **CHẠY** — đăng comment, đọc issue |
| REST thẳng `api.github.com` | **CHẶN** — proxy trả `403 GitHub access is not enabled for this session` |
| `gh` CLI | không cài, và **cài cũng vô ích** vì đi đúng đường bị chặn |

403 đó **không** phải thiếu token: `GITHUB_PAT` thật cũng 403, trong khi `/user` trả 200.
Chính sách theo **đường dẫn**, không theo danh tính. Vậy nên "gọi GitHub không được" là
kết luận sai ở container này — phải nói rõ **đường nào**.

### Hai bẫy khi gọi `codex` trực tiếp

- **Nó đọc thêm `stdin`.** Không có gì để đọc thì treo. Luôn `< /dev/null` khi gọi
  không tương tác (launcher đã lo sẵn).
- **Nó từ chối chạy ngoài thư mục git tin cậy**: `Not inside a trusted directory and
  --skip-git-repo-check was not specified`. Chạy trong kho, đừng chạy ở `/tmp`.

## Các chốt

Chạy trước khi gọi agent, hoặc gói luôn lượt gọi:

```bash
# chỉ kiểm, không gọi gì
python .claude/dev/launcher.py check \
  --expected-repo ducthangho/tra-luat \
  --expected-root-commit <sha40> \
  --expected-head <sha40> --expected-ref <nhánh> --require-clean --json

# kiểm rồi gọi CLI chính thức; lệnh đặt sau `--`
python .claude/dev/launcher.py run \
  --run-root ~/.tl-runs --name codex-review \
  --expected-repo ducthangho/tra-luat \
  --prompt-file nhiem_vu.txt --expected-prompt-sha256 <sha256> \
  --deadline-utc 2026-08-13T09:00:00Z \
  -- codex exec -s read-only "Doc tep {PROMPT_FILE} va thuc hien dung theo do."

python .claude/dev/launcher.py status --run-root ~/.tl-runs --id <short_id>
python .claude/dev/launcher.py stop   --run-root ~/.tl-runs --id <short_id>
```

### Ba thứ đã trả giá khi dựng lượt chạy thật (14-08-2026)

**`--run-root` phải nằm NGOÀI kho.** Thư mục chạy không có trong bảng loại trừ của
`release-verify`, nên để trong kho là đẻ `extra_files` và gate đỏ ở chỗ chẳng liên
quan gì tới việc đang làm.

**Vân tay kho đo trên clone NÔNG là vân tay GIẢ.** `git rev-list --max-parents=0 HEAD`
trên clone nông trả về **ranh giới cắt**, không phải commit gốc — và nó trông y hệt
một sha gốc thật. Đo được ca thật: cùng một kho cho `dfb94186…` khi nông (174 commit)
và `394e9346…` sau `git fetch --unshallow` (607 commit). Neo nhầm số đầu thì mọi lượt
chạy trên clone ĐẦY ĐỦ bị chặn oan, còn lượt chạy trên một clone nông khác lại "khớp"
một cách vô nghĩa. Luôn `git rev-parse --is-shallow-repository` **trước** khi lấy vân
tay; `false` rồi mới đo. (Chốt `--expected-root-commit` bắt được ca này — `rc=11`, nêu
cả số mong đợi lẫn số thực tế.)

**Đừng lấy `git worktree` làm workspace cho agent có sandbox.** Worktree để metadata
git ở `.git` của kho chính, tức **ngoài** workspace; sandbox `workspace-write` chỉ cho
ghi trong workspace nên mọi `git fetch`/`git gc` trong worktree bị chặn. Đã đo: phiên
codex báo đúng triệu chứng ấy và phải xoay sang đọc ref local. Cần agent fetch được
thì dựng **clone riêng** (`git clone --no-hardlinks`), chấp nhận tốn đĩa. Worktree vẫn
tốt cho lượt chỉ ĐỌC cây ở một head cố định.

### Bốn thứ đã trả giá ở lượt gọi `codex` thật (16-08-2026)

**`trang_thai=xong` + `ma_thoat=0` KHÔNG nghĩa là việc đã làm.** Lượt gọi reviewer đầu
tiên trả đúng hai trường ấy, và nó chạy **43 giây** rồi thoát — agent dừng ngay ở bước
đầu vì môi trường thiếu quyền, và từ chối làm tiếp. Cả hai trường trong sổ đều xanh:
launcher đo VÒNG ĐỜI TIẾN TRÌNH, nó không biết nội dung công việc và không thể biết.
Thứ tố cáo là thời lượng và kích thước đầu ra, nên từ nay sổ ghi thẳng
`thoi_luong_giay`, `stdout_byte`, `stderr_byte`, và `run` in chúng ngay cạnh dòng
`trang thai`. Đo được sau khi vá, hai lượt có `trang_thai`/`ma_thoat` **giống hệt nhau**:

```
ca rỗng (exit 0 tức thì) : trang thai: xong  ma_thoat=0   thoi luong: 0.007s  stdout=0B
ca làm việc thật         : trang thai: xong  ma_thoat=0   thoi luong: 2.01s   stdout=21B
```

Ai gọi tự động phải tự đặt ngưỡng cho ba số ấy. Không có ngưỡng thì "xong" chỉ là chữ.

**Sandbox `workspace-write` của codex chặn CẢ `.git` LẪN mạng — và hai thứ đó hỏng
khác nhau.** Triệu chứng cụ thể để nhận ra: `git fetch` trả `rc=255` kèm
`.git/FETCH_HEAD: Read-only file system`, còn `git ls-remote` thì lỗi kết nối. Mở đúng
hai chốt, không cần mở toang:

```
-c 'sandbox_workspace_write.network_access=true'
-c 'sandbox_workspace_write.writable_roots=["<workspace>/.git","/tmp"]'
```

`/tmp` cần vì công thức đo trên cây đã merge dựng thư mục tạm. Đo được sau khi thêm:
`fetch_rc=0`, `lsremote_rc=0`. **Đừng nhảy sang
`--dangerously-bypass-approvals-and-sandbox`** dù mô tả của nó khớp hoàn cảnh container
("environments that are externally sandboxed") — mở hai khoá trên là đủ, và giữ được
điều kiện agent không ghi ra ngoài workspace.

**Luôn kèm `--strict-config`.** Gõ sai tên khoá `-c` thì codex BỎ QUA im lặng: lượt chạy
vẫn xanh, sandbox vẫn đóng, và ta tưởng đã mở. `--strict-config` biến chỗ đó thành đỏ.
Cùng họ với "cổng không nói dối, nó vắng mặt".

**`--full-auto` KHÔNG tồn tại ở `codex exec` 0.147.0** — nó trả `rc=2` usage error, tức
lệnh không chạy gì cả. Cờ đúng là `-s <read-only|workspace-write|danger-full-access>`,
và `--approve-for-me` nếu cần tự duyệt. Kiểm bằng `codex exec --help` trên CHÍNH bản
đang cài, đừng chép cờ từ trí nhớ hay từ tài liệu của bản khác.

**Nhắc lại bài học worktree ở trên, vì lượt này đã lặp lại nó.** Đoạn "Đừng lấy
`git worktree` làm workspace cho agent có sandbox" viết từ 14-08 mà lượt 16-08 vẫn dựng
worktree trước rồi mới đổi sang clone. Vân tay nhận ra sớm: trong worktree, `.git` là
một **tệp** trỏ ra ngoài, nên `test -d .git` trả sai. Kiểm một dòng đó trước khi giao
workspace cho agent.

### `codex login status` chỉ đọc TỆP — đòi bằng chứng dương

`codex login status` in `Logged in using ChatGPT` dựa trên `~/.codex/auth.json` chứ
KHÔNG hỏi máy chủ, nên nó báo đăng nhập với một token đã bị thu hồi (đo 16-08-2026).
Hook `session-start.sh` cũng dựa vào lệnh này ở chốt "không ghi đè khi đã đăng nhập",
nên chốt ấy thừa hưởng đúng điểm mù.

Muốn biết token còn sống thì gọi thật một lượt và đòi kết quả:

```bash
codex exec --skip-git-repo-check -C /tmp 'Reply with exactly: PONG'
```

Đòi `rc=0` VÀ chuỗi `PONG` trong đầu ra. Lượt gọi thật in kèm `auth_mode`, tài khoản và
số token đã dùng — đó mới là bằng chứng máy chủ đã nhận, khác hẳn một dòng đọc từ đĩa.

Gọi Claude thì thay phần sau `--` bằng `claude -p "..."`. Không có gì khác đổi.

### `{PROMPT_FILE}` — neo prompt kín *sau* khi sinh con

`--prompt-file` + `--expected-prompt-sha256` mới chỉ khép cửa sổ **trước** lúc chạy:
hash được kiểm lại ngay trước khi sinh con. Nhưng nếu lệnh tự mở lại đường dẫn gốc
(`... "Doc tep nhiem_vu.txt ..."`) thì ai đó đổi nội dung tệp *sau* thời điểm đó vẫn
qua mặt được neo.

Viết `{PROMPT_FILE}` ở đâu trong lệnh thì chỗ đó được thay bằng **bản chụp bất biến**
trong thư mục lượt chạy, nên con đọc đúng thứ đã được hash. Thay ở mọi lần xuất hiện,
kể cả khi lồng trong một đối số lớn (`--file={PROMPT_FILE}`). Sổ ghi
`prompt_kin_hoan_toan: true`; không dùng thì ghi `false` — không giả vờ là đã kín.
Có `{PROMPT_FILE}` mà quên `--prompt-file` thì bị chặn (mã 2), vì nếu không con sẽ
nhận đúng chuỗi `{PROMPT_FILE}` làm đường dẫn.

Bản chụp ghi quyền `0600` và **bị xoá khi con thoát** (prompt có thể chứa bí mật —
đó cũng là lý do sổ không lưu đối số nguyên văn). Cần giữ để truy vết thì
`--giu-ban-chup`.

### Neo theo *kho*, không theo đường dẫn

`--workspace` không bắt buộc: thứ tự là `--workspace` → `$TL_WORKSPACE` → thư mục
hiện tại, rồi luôn hỏi `git rev-parse --show-toplevel`. Đường dẫn tuyệt đối là
thứ **duy nhất không mang được sang máy khác** — phiên remote clone kho vào một
đường dẫn không ai biết trước.

Danh tính kho lấy từ `--expected-repo` (chuẩn hoá qua bốn dạng URL, cắt phần đăng
nhập nên token không lọt ra) và `--expected-root-commit` (vân tay bền nhất: không
đổi khi kho bị đổi tên, chuyển chủ, fork; đọc được không cần mạng).

Nêu **host** (từ 3 đoạn trở lên) thì chốt đòi **bằng nhau tuyệt đối** — kể cả đường
dẫn lồng sâu như `gitlab.com/nhom/nhom-con/kho` (GitLab subgroup) hay GHE nhiều tầng.
Chỉ nêu `owner/repo` thì nó so hai đoạn cuối — nghĩa là bạn chấp nhận không phân biệt
host. Muốn chặt thì nêu host, hoặc dùng commit gốc.

Remote là **đường dẫn địa phương** (`/srv/kho.git`, `D:\ho-so\kho`, UNC) không đọc ra
danh tính nên bị loại khỏi danh sách: kho chỉ có remote kiểu đó sẽ **bị chặn**
(`thuc te (khong co remote)`), không bao giờ khớp nhầm.

## Mã thoát

| mã | nghĩa |
|---|---|
| 0 | qua hết |
| 2 | tham số sai |
| 3 | không phải repo git / git không chạy được |
| 4 · 5 · 6 | HEAD lệch · ref lệch · worktree bẩn |
| 7 · 8 | prompt (thiếu/rỗng/sha lệch) · hạn chót đã qua |
| 10 | không xác định được danh tính tiến trình → **từ chối giết** |
| 11 | kho không đúng |
| 12 | thiếu công cụ bắt buộc |
| 124 | quá hạn **và đã giết được** |
| 125 | quá hạn **nhưng KHÔNG giết được** — cần người can thiệp (`stop` cũng dùng mã này khi giết chưa trọn vẹn) |
| 130 | bị ngắt (Ctrl-C) — đã giết con |
| 141 | đầu ra bị cắt ống ở chỗ không giữ được kết luận (128+SIGPIPE) |
| 1 | mã thoát của con nằm ngoài 0..255; số THẬT ở `ma_thoat_that` trong sổ |

> **Bảng trên KHÔNG dứt khoát với `run`.** Mã thoát của *tiến trình con* được trả
> nguyên vẹn nên nó đè lên mọi mã ở đây: `rc=124` không phân biệt được "launcher
> cưỡng chế hạn chót" với "con tự thoát 124" (con chạy `timeout(1)`, hoặc con là một
> launcher khác). Phía gọi tự động phải đọc `trang_thai` trong `run.json`
> (`xong` · `qua_han` · `bi_ngat` · `da_dung` · `hong`), đừng suy từ mã trần.
> `check`/`status`/`stop`/`doctor` không có con nên với chúng bảng trên là dứt khoát.

Tách 124/125 là có lý do: bản trước trả 124 trong khi tiến trình mẹ lẫn cháu vẫn
sống, nên phía gọi tưởng đã dọn xong.

## Ba đường vào, cùng một lệnh

- **Máy cá nhân** — `cd` vào kho rồi chạy. Trên Windows gọi `python` (đừng cho rằng có `python3`).
- **Điện thoại / Claude Code web** — phiên remote clone kho vào container; hook
  `SessionStart` cài công cụ; lệnh giống hệt vì không có đường dẫn cứng nào.
- **CI** — đặt `TL_WORKSPACE`, còn lại giống hệt.

## Chạy bộ phản chứng

```bash
python .claude/dev/launcher_test.py             # 74 ca
python .claude/dev/launcher_test.py --dot-bien  # 31 đột biến, mỗi cái phải giết đúng ca chỉ định
```

Một số ca tự bỏ qua tuỳ nền và bộ test **nói rõ ca nào**: trên Windows là các ca
cần shim shell hoặc cây tiến trình POSIX; trên Linux chỉ còn `t62` vì
fixture của nó dựng cho `taskkill /T`. (Câu cũ ở đây — "POSIX `killpg` giết theo nhóm
nên không dựng được trạng thái mẹ-chết-cháu-sống" — là **SAI SỰ THẬT**: dựng được, và
`t63`/`t66`/`t67` là ba biến thể của nó.) Đột biến
nhắm vào một ca bị bỏ qua sẽ báo **KHONG DO DUOC** thay vì tính là hỏng — một cổng
không bao giờ xanh được thì người ta sẽ bỏ qua nó.

**Chưa chạy trên Windows thì đường Windows chưa được nghiệm thu** — đúng bài học
"script đa nền phải chạy THẬT trên nền đó".

## Đăng ký hook: đừng để chuỗi lệnh rơi vào PowerShell

Tài liệu chính thức (<https://code.claude.com/docs/en/hooks>):

> The `command` string is passed to a shell: `sh -c` on macOS and Linux, **Git Bash on
> Windows, or PowerShell when Git Bash isn't installed.**

Máy Windows **không có Git Bash** thì chuỗi `bash "$CLAUDE_PROJECT_DIR/..."` được giao
cho PowerShell, ở đó `bash` không tồn tại **và** `$CLAUDE_PROJECT_DIR` là biến
PowerShell chưa định nghĩa nên nở ra **rỗng** — hai lỗi độc lập, cùng hướng. Vì vậy
`.claude/settings.json` ghim `"shell": "bash"` và dùng dạng ngoặc `${CLAUDE_PROJECT_DIR}`.

Chặt hơn nữa thì dùng **exec form** (`args`), không qua shell nào cả — tài liệu khuyến
nghị đúng cho trường hợp có path placeholder: *"Prefer exec form for any hook that
references a path placeholder."* Kho này chưa dùng vì client cũ bỏ qua `args` sẽ chạy
`bash` trần và đọc stdin — mà `PreToolUse` hỏng thì **mọi lệnh Bash chết trước khi
chạy**, đúng bẫy tự khoá đã ghi trong `CLAUDE.md`.

Hook `SessionStart` **không chặn được phiên**: thoát khác 0 chỉ hiện một dòng lỗi,
*Claude không thấy stderr*. Nhưng **stdout của `SessionStart` được đưa vào ngữ cảnh**
— nên bảng `doctor` và dòng `THIEU CONG CU BAT BUOC` phải in ra **stdout**, đừng
"dọn" mấy dòng `echo` đó đi.

## Chế độ hỏi/duyệt của phiên agent — Claude Code, Codex, AG

Bệnh "phiên hỏi xác nhận liên miên, không duyệt thì đứng" đã chữa MỘT lần (commit
`7c51e84`: bỏ `git commit/push` khỏi ask) rồi **tái phát 20-08-2026**. Nguyên nhân
gốc đo được: bản vá cũ sửa `settings.json` COMMITTED, nhưng sau đó một khối ~51 rule
`ask` (mọi git/gh write op) mọc vào `settings.local.json` của checkout chính — tệp
**gitignored, per-checkout**, và **đè lên** allow của bản committed. Worktree mới thì
không có tệp local nên rơi về allowlist tối thiểu → hỏi lại từ đầu. Cộng bài học cũ:
trong don't-ask-mode, rule `ask` thoái hoá thành **DENY cứng** — phiên chết đứng.

Kiến trúc chống tái phát (một chỗ cho mỗi việc, đừng đảo lại):

| tầng | vai | luật |
|---|---|---|
| `settings.json` (committed) | ALLOW rộng cho việc thường ngày + `defaultMode: acceptEdits` | mọi worktree/checkout kế thừa; muốn thêm quyền lâu dài thì thêm VÀO ĐÂY và đi qua PR |
| `pretooluse_guard.py` (hook) | ASK theo HÌNH DẠNG lệnh, quét CẢ CHUỖI | chốt thật nằm đây (force-push, `gh pr merge`, `gh api` mutate, `--dangerously-*`, `--apply`…) — regex không dính bẫy prefix-pattern (`git push origin --force` thoát rule `git push --force:*` nhưng không thoát regex) |
| `deny` trong settings | thứ KHÔNG BAO GIỜ tự chạy | secrets, `rm -rf` |
| `settings.local.json` | **cache máy, KHÔNG phải nơi đặt chốt** | thấy khối `ask` mọc trong này là bệnh đang tái phát — xoá và thăng rule cần thiết vào bản committed |

Nói thẳng giới hạn: RISKY của hook là danh sách HÌNH DẠNG để hỏi lại người giữ,
**không phải hàng rào an ninh** chống kẻ gian ("danh sách cấm không bao giờ đủ") —
phiên agent là người nhà, mục tiêu là chặn tay trót, không phải chặn tấn công.

**Codex.** KHÔNG ghi `~/.codex/config.toml` của người dùng (kiến trúc chốt sau bảy
finding — xem mục Các chốt). Chế độ duyệt truyền BẰNG CỜ theo từng lượt:

```bash
codex exec -s workspace-write --skip-git-repo-check ... - < PROMPT.md   # exec KHONG hoi — khong can -a
codex -a on-failure -s workspace-write                                   # phien tuong tac: chi hoi khi lenh HONG
```

Đừng dùng `--dangerously-bypass-approvals-and-sandbox` (đã ghi ở mục Các chốt);
`-a` chỉ tồn tại ở lệnh top-level, truyền vào `exec` là chết parse.

**Claude Code headless (`claude -p`).** Đừng `--dangerously-skip-permissions` (hook
sẽ hỏi, classifier của harness cũng chặn — đo 20-08). Cấp allowlist HẸP theo lượt:

```bash
claude -p --model claude-fable-5 --effort max \
  --allowedTools "Read" "Glob" "Grep" "Edit" "Write" "Bash(python:*)" ... < PROMPT.md
```

Lưu ý: phiên headless chạy Ở NGOÀI kho (sandbox review) không thừa kế
`settings.json` của kho — allowlist per-run là đường duy nhất. Và **đừng kèm
`--bare`**: nó bỏ qua cả cấu hình xác thực, phiên chết `Not logged in` (đo 20-08).

**Antigravity (AG).** Chế độ duyệt của AG nằm trong CÀI ĐẶT APP (Agent auto-run),
kho không cấu hình hộ được. Khuyến nghị khi mở phiên AG cho packet của kho: bật
auto-run cho lệnh ĐỌC + chạy test; giữ hỏi cho terminal ghi ngoài worktree, mọi thao
tác đẩy/xoá ref, và browse ngoài workspace. Các chốt HÌNH DẠNG ở trên không chạy
trong AG — bù bằng chốt phía kho vẫn còn nguyên: `ops-don-ref` đòi gõ `XOA`/`TAO`,
cổng đăng lease theo danh sách cho phép, và `packet_loop` guard. Con trỏ từ
`AGENTS.md` sang mục này sẽ bổ sung ở packet sau (AGENTS.md nằm trong
RELEASE_MANIFEST — sửa nó kéo theo tái sinh manifest, tránh va write set đang mở).
