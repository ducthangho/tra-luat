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

Thoát `12` khi thiếu công cụ **bắt buộc** (hoặc có mặt mà phép `xac_thuc` khai trong
`CONG_CU` đo được là SAI), **và cả khi** `rg` hoặc `git` ở trạng thái
`BI_CHE`. Tập bắt buộc lấy từ `CONG_CU` trong `.claude/dev/launcher.py` (`_bat_buoc`),
và nó **theo nền**, không phải một danh sách chung:

| công cụ | máy người dùng | phiên remote (`CLAUDE_CODE_REMOTE=true`) | CI (`GITHUB_ACTIONS`/`CI`) |
|---|---|---|---|
| `git` · `python` · `rg` · `bash` | bắt buộc | bắt buộc | bắt buộc |
| `claude` · `codex` | bắt buộc | bắt buộc | tuỳ chọn |
| `gh` | bắt buộc | tuỳ chọn | tuỳ chọn |

`BI_CHE` (wp802, `_AP_DUNG_BI_CHE`, chỉ áp cho `rg` và `git`): bản TÊN TRẦN — bản shell
gọi khi agent gõ `rg`/`git` — hỏng, trong lúc một bản khác trên máy vẫn chạy được.
`doctor` in `THIEU rg (BI_CHE: co cai, ban ten tran hong)` kèm cách chữa: đưa thư mục
bản tốt lên trước trong PATH, hoặc gỡ bản hỏng. Agent gõ tên trần, nên "máy có một bản
chạy được" không cứu được lệnh của nó. Công cụ ngoài bảng chỉ là cảnh báo.

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
| 12 | thiếu công cụ bắt buộc (bảng theo nền ở mục "Trước tiên: đủ công cụ chưa"), hoặc `rg`/`git` `BI_CHE` (tên trần hỏng, bản khác chạy được) |
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

#### `Bash(x:*)` KHỚP TIỀN TỐ CHUỖI LỆNH — nên nó chặn OAN gần hết phép đo thật (đo 24-08-2026)

Câu "cấp allowlist HẸP theo lượt" ở trên **đúng về ý định và sai về hậu quả**, và nó đã làm hỏng
**ba lượt cross-review liên tiếp** trong một phiên. Luật `Bash(git:*)` không khớp *"lệnh nào có
chạy `git`"*; nó khớp *"chuỗi lệnh BẮT ĐẦU bằng `git`"*, nên mọi thứ có **ống, `;`, `>`, `$( )`,
heredoc, hay gán biến đứng trước** đều **không khớp gì cả**. Đo được trong một lượt mà allowlist
đã có đủ `Bash(git:*)` `Bash(python3:*)` `Bash(cd:*)` `Bash(echo:*)`:

```text
git ls-remote --heads origin 2>/dev/null | sed 's#...#' | sort > /tmp/mc   TU CHOI
echo "may chu: $(git ls-remote --heads origin | wc -l)"                    TU CHOI
python3 - <<'PY' ... PY                                                    TU CHOI
M=8ba8acaa; echo ...; git merge-base --is-ancestor $M HEAD                 TU CHOI
cd "$(git rev-parse --show-toplevel)"; python3 - <<'PY' ...                TU CHOI
```

*(Lượt ấy còn một lệnh thứ sáu bị từ chối — `bash /tmp/refscan.sh` — nhưng nó **khác nguyên nhân**:
allowlist lượt đó không có `Bash(bash:*)`, tức bị chặn vì thiếu tên chương trình chứ không vì lệnh
ghép. Ghi tách vì gộp nó vào năm ca trên là **lời khai rộng hơn phép đo** — cross-review bắt đúng
chỗ này.)*

Chốt của Claude Code làm **đúng** — luật tiền tố không bao được phần còn lại của lệnh ghép nên nó
từ chối thay vì đoán. Cái sai ở phía ta: **allowlist theo tên chương trình phân biệt CÁCH VIẾT,
không phân biệt THẨM QUYỀN**, đúng hình dạng kho đã đếm nhiều lần — lần này nó cắn chính bộ đo của
mình. Và hậu quả không dừng ở "thiếu vài phép đo": mỗi lần bị từ chối, reviewer viết lại lệnh rồi
thử tiếp, vòng lặp ấy làm context phình. Ba lượt, **cùng prompt, cùng exact head**:

| allowlist | lượt hội thoại | bị từ chối | cache đọc | kết cục |
|---|---:|---:|---:|---|
| liệt kê theo tên lệnh | 78 | 5 | 10,8 M | `api_error` — mất trắng |
| nới thêm `cd`/`bash`/`sh` | 85 | 10 | 12,8 M | `api_error` — mất trắng |
| **`Bash` trần** | **45** | **1** | **3,7 M** | **`completed`, verdict đầy đủ** |

**Ba con số ấy KHÔNG tái lập được từ kho** — đọc từ `usage` và `permission_denials` trong
`stdout.log` của ba lượt, mà các tệp ấy nằm trong scratchpad của phiên, **không được git theo dõi**.
Bảng trên là *chứng cứ đã đo*, không phải *phép đo bạn chạy lại được*.

**Nhân quả thì CHƯA chứng minh:** ba lượt khác nhau ở **cả** allowlist **lẫn** thời điểm chạy, nên
không loại được yếu tố phía dịch vụ — đây là **tương quan có neo**. Nói chắc được chỉ là: allowlist
rộng cho ít lượt hơn, ít bị từ chối hơn, ít context hơn, và là cấu hình duy nhất trong ba cho ra
verdict. Giá trước khi tìm ra: ~$39 và ba lượt chạy.

**Nên làm.** Phiên **reviewer read-only** trong clone rời: cấp `Bash` **trần** cộng đúng những công
cụ MCP chỉ đọc mà lượt ấy cần:

```bash
claude -p --model opus --effort max --permission-mode acceptEdits \
  --allowedTools Read Glob Grep Bash \
      mcp__github__pull_request_read mcp__github__issue_read mcp__github__get_file_contents \
  --output-format json < PROMPT.md
```

Và **đừng gọi đó là siết an ninh** — nó chưa từng là. Giữ danh sách hẹp ở đây không mua được an
toàn, chỉ mua được một verdict mỏng hơn, hoặc không có verdict nào.

#### NĂM HẠNG bằng chứng — đọc mục dưới bằng từ vựng này, kẻo lại viết ra những câu chỏi nhau

**Phạm vi của từ vựng này:** nó áp cho các **control của mục này** — BA control TRONG BẢNG, đo ở vỏ phiên
điều phối, thành NĂM mệnh đề TRONG BẢNG (`--allowedTools` và cặp credential mỗi cái được đo ở
hai cấu hình); văn xuôi dưới bảng mang thêm BA mệnh đề nữa; phép đếm đầy đủ nằm ngay sau bảng năm hạng.
Mục mạng/sandbox codex và mục hai pha reviewer ĐÃ ĐƯỢC TÁCH sang **packet `MANG-SANDBOX-CODEX`,
Issue #334** — đó là NEO DUY NHẤT cho chỗ tách; mọi câu "packet kia" phía dưới đều trỏ về đây, và
đừng chép trạng thái động của nó vào tệp này. Cái ĐI theo lát cắt là SỐ ĐO đầy đủ, probe và bảng
hai pha. Cái Ở LẠI là ĐÚNG MỘT mệnh đề về mạng sandbox: nó nằm TRONG phạm vi từ vựng này, mang
nhãn, và được đếm Ở ĐÂY — nên điều kiện đo của nó cũng phải nằm ngay cạnh nó như mọi mệnh đề khác.
Chỗ khác trong tệp dùng chữ *ranh giới* / *cưỡng chế* theo nghĩa thường (phân công giữa
launcher và CLI ở đầu tệp; hạn chót của launcher; và *"ranh giới cắt"* là thuật ngữ Git của clone
nông) — những chỗ ấy **không** mang hạng, và nói ra ở đây để không ai đi gắn nhãn nhầm.

Vì sao cần từ vựng này: bản đầu của mục dưới tự mâu thuẫn trong sáu chục dòng — khai *"không
tầng nào bó được"*, rồi gọi một tầng là *"hàng rào thật, có sẵn"*, rồi dùng nó làm cột **cưỡng
chế**, rồi bảo *đừng dựa vào nó như một bảo đảm an ninh*. Cả bốn câu đều dựa trên phép đo có
thật; thứ trôi không phải số liệu mà là **HẠNG của bằng chứng**. NĂM hạng — và **đơn vị được xếp
hạng là một MỆNH ĐỀ KÈM ĐIỀU KIỆN ĐO**, không phải một control trần: cùng một control mang hạng
KHÁC NHAU ở hai cấu hình. Mục dưới có ví dụ: hàng `--allowedTools` tách làm hai vì luật hẹp và
`Bash` trần cho hai hạng khác nhau. Mọi mệnh đề sau đây mang đúng một nhãn:

| hạng | nghĩa | được gọi là |
|---|---|---|
| **cơ chế đã xác minh — chiều ĐÓNG** | biết nó chặn BẰNG GÌ, và đã đo được nó chặn | *ranh giới*, *hàng rào* |
| **cơ chế đã xác minh — chiều MỞ** | biết vì sao nó KHÔNG chặn, và đã đo | KHÔNG được gọi là ranh giới; nó giải thích một chỗ HỞ |
| **quan sát chưa rõ cơ chế** | lặp lại được, nhưng chưa ai đo CƠ CHẾ ⇒ chưa biết có bền không | *quan sát* — kèm phiên bản và điều kiện đo |
| **máy phát hiện** | không ngăn được gì; nó TỐ CÁO sau khi việc đã xảy ra | *máy phát hiện* |
| **chưa xếp được** | không rơi gọn vào bốn hàng trên | phải GỌI TÊN là chưa xếp được, không im lặng bỏ qua |

**Mục này dùng BA trên năm hạng — nhưng KHÔNG phải ba hạng mà bản trước tưởng.** Đơn vị đếm là
**lần GẮN NHÃN cho một mệnh đề**, không phải số lần xuất hiện của cụm chữ. TÁM mệnh đề mang nhãn:
năm hàng bảng, cộng mệnh đề cơ chế proxy ambient, mệnh đề bộ-ba-với-quyền-ghi, và mệnh đề mạng
sandbox ở đoạn khai chỗ tách. Đếm ra: `chiều ĐÓNG` ×1 · `chiều MỞ` ×5 · `chưa xếp được` ×2 ·
`máy phát hiện` ×0 · `quan sát chưa rõ cơ chế` ×0.
Mệnh đề thứ tám ấy TỪNG bị bỏ khỏi phép đếm vì "bằng chứng ở chỗ khác" — đó là mở đúng cái ngoại lệ
mà cam kết trên cấm. Nay nó mang nhãn VÀ có điều kiện đo ngay cạnh nó, lấy từ phép A/B đã có sẵn
trong chính tệp này; thứ ở packet kia chỉ là số đo ĐẦY ĐỦ, không phải chỗ dựa của nhãn.

Bản trước của chính đoạn này khai `chiều ĐÓNG` **bằng KHÔNG** rồi dựng cả một lập luận trên đó —
rằng ô rỗng ấy chứng minh "không control nào bó được". Cross-review bác: có mệnh đề THẬT SỰ đóng.
Ghi lại vì bài học đắt hơn con số: **quan hệ tổng còn đúng không chứng minh các số hạng còn đúng**.
Số hạng-được-dùng vẫn là ba trước và sau khi sửa, nên mọi phép kiểm đếm-theo-quan-hệ đều xanh
trong khi danh tính từng hạng đã đổi hết.

Điều đáng nói nay KHÁC hẳn, và mạnh hơn: **có thứ đóng thật — nhưng nó không đóng ĐÚNG THỨ đang
bàn.** Luật hẹp `Bash(x:*)` đóng HÌNH DẠNG lệnh: đo được, fail-closed, và **không chạm quyền ghi
vào kho**. Nên
luận điểm đúng của mục là *chưa đo được control nào bó được quyền ghi*, với lượng từ cố ý yếu vì
hai ô `chưa xếp được` là hai mệnh đề chưa chốt.

`máy phát hiện` rỗng cũng là kết luận, không phải sót: bộ ba từng bị gọi là máy phát hiện hoá ra
KHÔNG tố cáo sự kiện đang bàn. `quan sát chưa rõ cơ chế` rỗng vì lý do riêng của TỪNG mệnh đề chưa
chốt, không phải một lý do chung: hàng `workspace-write` không mang phiên bản lẫn số lần lặp, mà
hạng ấy đòi lặp lại được; mệnh đề bộ-ba-với-quyền-ghi thì chưa ai đo CƠ CHẾ. Thiếu điều kiện thì
chỗ của chúng là ô dư, không phải hạng gần nhất. Bảng giữ đủ năm hàng vì nó là **từ vựng dùng
chung**; đừng đọc số hàng thành số hạng đã dùng.

Luật đọc: **quan sát theo phiên bản KHÁC bất biến an ninh.** Chỉ được gọi một thứ là *ranh giới*
sau khi xác minh cơ chế **và đo được nó chặn**; trước đó nó là *quan sát*, và quan sát thì có hạn dùng.

Hàng cuối tồn tại vì cross-review bắt được: bản đầu của bảng này chỉ có ba hàng, tự xưng *"mọi câu
dưới đây mang đúng một nhãn"*, rồi **sai ngay ở ví dụ của chính nó** — cơ chế proxy chèn credential
là thứ đã xác minh theo chiều MỞ, không thoả định nghĩa "đo được fail-close" của hàng đầu.
**Một bảng phân loại tự xưng phủ hết mà không có ô dư thì không thể phủ hết**; ô dư là chỗ để cái
chưa xếp được LỘ RA thay vì bị nhét bừa vào hàng gần nhất.

#### Ba CONTROL thường bị coi là hàng rào, NĂM mệnh đề trong bảng — đo Ở VỎ PHIÊN ĐIỀU PHỐI: CHƯA đo được control nào bó được QUYỀN GHI VÀO KHO (24-08-2026)

Phạm vi của mục này là **vỏ phiên điều phối** (`claude`, `Bash` trần), và thứ bị đo là **quyền ghi
vào kho** — không phải "bó" nói chung. Phân biệt ấy quan trọng: HAI hàng `--allowedTools` dưới đây CÓ
chặn, nhưng nó chặn theo **hình dạng lệnh**, không theo **thẩm quyền**, nên nó chặn oan phép đo mà
không chặn được đường ghi. Hàng `codex` trong bảng là **phép đo đối chứng ở vỏ phiên**, và chỉ
có MỘT — bảng này chưa bao giờ có hai. Bản trước viết *"Hai hàng `codex`"*: sai từ đầu, không phải
sai do lát cắt. Sửa lần đầu còn tệ hơn, vì nó giải thích rằng hàng thứ hai "đã theo mục mạng sang
packet kia" — **bịa một nguyên nhân cho một con số sai**, đúng lỗi mà chính tệp này lên án. Đối
chiếu được: bảng có ĐÚNG một hàng `codex` ở `48cf331`, `f16b6bf`, `88bd4f2` và `6d0a183`.

Kết quả **bên trong sandbox codex khác hẳn**, và mục ấy — cùng mục hai pha reviewer — ĐÃ TÁCH sang
packet riêng. Lý do tách là một phép đếm, không phải cảm tính: bốn vòng cross-review liên tiếp đều
sinh finding về mục mạng/sandbox (tám finding), trong khi mọi tiêu chí khác của packet này đã đạt
từ vòng ba. Mệnh đề còn đứng mà không cần bảng số nào — và nó MANG NHÃN như mọi mệnh đề khác:
**socket và url của sandbox: `network_access=true` MỘT MÌNH đảo cả hai từ `POLICY_DENIED` sang
`LOT`** ⇒ **cơ chế đã xác minh — chiều MỞ**, phạm vi CHỈ hai kênh này; hạng MỞ không phải ranh
giới (định nghĩa ở trên) — nó giải thích VÌ SAO không chặn, không tuyên bố có chặn. `git` KHÔNG
vào phạm vi nhãn này.
ĐIỀU KIỆN ĐO nằm NGAY ĐÂY, không ở packet kia — mục `sandbox workspace-write` phía trên đo A/B
trên CÙNG một lệnh: mặc định `git ls-remote` lỗi kết nối; sau khi bật **HAI** cờ cùng lúc
(`network_access` và `writable_roots`) thì `lsremote_rc=0`. Điều kiện: codex CLI trong container
này, sandbox `workspace-write`, vỏ phiên điều phối; số phụ thuộc phiên bản và cấu hình.
Bằng chứng MỞ cho SOCKET/URL riêng, đo lại SAU KHI packet `MANG-SANDBOX-CODEX` (#334) land: bốn
tổ hợp (a)-(d) ở `docs/MANG_SANDBOX_CODEX.md` giữ `writable_roots` cố định và chỉ đảo
`network_access` — một mình cờ đó lật socket/url từ `POLICY_DENIED` sang `LOT`, không phải tổ hợp
hai cờ như phép đo `git ls-remote` ở trên; trỏ sang tệp đó, không chép bảng về đây. `git` ở trạng
thái đóng mang lớp `KHÔNG_ĐO_ĐƯỢC` trong CHÍNH tệp ấy — phiên đo chưa tách được sandbox chặn khỏi
việc không nối tới proxy loopback của chính phiên đo — nên với `git`, VÌ SAO không chặn vẫn chưa
biết; giữ `KHÔNG_ĐO_ĐƯỢC`, không gộp vào nhãn MỞ trên. Loopback không phải egress: cờ này gate
capability socket rộng hơn hai phép HTTPS ra ngoài, nên MỞ chỉ xác minh phạm vi cờ cấu hình đã đo,
không xác minh một ranh giới mạng nói chung. Số đo đầy đủ, probe và bảng hai pha nằm ở
`docs/MANG_SANDBOX_CODEX.md` (#334) — **đừng chép chúng về đây**.

Cross-review dựng remote bare tạm rồi push từ trong phiên "read-only": `rc=0`, ref được tạo, và
`--require-clean` **vẫn báo sạch**. Đo tiếp BA control ấy — năm hàng, vì `--allowedTools` vào bảng
hai lần (luật hẹp / `Bash` trần) và credential cũng hai lần (xoá khỏi env / token rác), đúng theo
luật đơn vị ở trên: đếm CONTROL thì gom theo cơ chế, đếm MỆNH ĐỀ thì tách theo điều kiện đo.

| tầng | phép đo | kết quả |
|---|---|---|
| `--allowedTools`, luật hẹp `Bash(x:*)` | gặp lệnh ghép | không khớp gì ⇒ **cơ chế đã xác minh — chiều ĐÓNG**, nhưng CHỈ đóng HÌNH DẠNG lệnh ghép (cơ chế khớp tiền tố, năm lệnh `TỪ CHỐI` đo ở mục trên); nó KHÔNG bó quyền ghi |
| `--allowedTools`, `Bash` trần | cùng lệnh ghép | khớp mọi thứ ⇒ **cơ chế đã xác minh — chiều MỞ** |
| `codex -s workspace-write` | ghi tệp **ngoài** cây | **`rc=0`** — tệp ngoài cây bị ghi đè thật ⇒ **CHƯA XẾP ĐƯỢC**: đo được nó KHÔNG chặn, nhưng chưa ai đo CƠ CHẾ vì sao — `docs/MANG_SANDBOX_CODEX.md` (#334) chỉ đo mạng/socket/proxy, không đo đối tượng ghi-ngoài-cây này |
| xoá `GITHUB_PAT` `GH_TOKEN` `GITHUB_TOKEN` `GIT_CONFIG_*` khỏi env | `git push --dry-run` lên GitHub | **`rc=0`** — vẫn đẩy được ⇒ **cơ chế đã xác minh — chiều MỞ** |
| nhét **token RÁC** vào URL đẩy | cùng lệnh | **`rc=0`** ⇒ **cơ chế đã xác minh — chiều MỞ** |

HAI dòng cuối cùng một cơ chế, và dòng chót là dòng quyết định: **proxy egress bỏ qua credential client gửi và tự chèn credential
của nó** — nên "cấp token đọc riêng cho reviewer" cũng vô dụng, credential là **ambient ở mức
container**. Đây là **cơ chế đã xác minh — chiều MỞ**: ta biết vì sao nó không chặn.
Bản đầu còn viết *"ranh giới thật là clone rời + `--require-clean` + kiểm cây sạch"*. Câu ấy SAI
về hạng, nhưng bản sửa đầu tiên cũng sai: nó gọi cả ba là **máy phát hiện**, trong khi phản chứng
nằm ngay trên — push ĐÃ tạo ref mà `--require-clean` **vẫn báo sạch**, tức nó KHÔNG tố cáo. Đúng
cách là hỏi **hạng cho ĐỐI TƯỢNG NÀO**. Với đối tượng của mục này — **quyền ghi/push vào kho** —
bộ ba ấy là **CHƯA XẾP ĐƯỢC**: đo được nó không tố cáo, nhưng chưa ai đo vì sao, nên cũng không
gọi được là chiều MỞ.

Còn `--require-clean` với một đối tượng KHÁC — việc chạy một lượt trên cây bẩn — thì **hạng của
nó không được xếp ở đây**, kể cả khi có vẻ hiển nhiên. Mục này chỉ đo **quyền ghi vào kho**, nên
mọi kết luận về đối tượng khác phải nằm ở mục nói về vòng đời lượt chạy, mang phép đo riêng của
nó. Câu này cố ý KHÔNG khẳng định control ấy bó hay không bó: khẳng định ở đây là lại thêm một
mệnh đề vào một phạm vi đã tuyên bố không chứa nó — đúng lỗi cả mục sinh ra để chữa.

Với phiên **executor có quyền ghi**, danh sách hẹp vẫn hợp lý: ở đó ta muốn giới hạn *hình dạng
việc*, và executor có `settings.json` của kho làm nền.

#### Bản in cuối cùng của phiên headless LÀ sản phẩm — không có lượt sau

Cùng đợt đo, một lượt review khác thoát `rc=0`, `subtype: success`, `stop_reason: end_turn`, cây
làm việc sạch — **188 lượt hội thoại, 105 911 token đầu ra, 31 phút** — rồi in đúng một câu:
*"I'll pick this up when the probe lands."* Không có probe nào; `claude -p` không có cơ chế chạy
nền. Toàn bộ công việc mất sạch.

Hỏng kiểu này **trông y hệt thành công** ở mọi tín hiệu ta quen nhìn (`rc`, `is_error`, `subtype`,
cây sạch); chỉ đọc **nội dung** bản in mới thấy rỗng. `rc=0` của một lượt agent **không phải bằng
chứng có sản phẩm** — phải đo chính sản phẩm. Chốt rẻ, đã dùng lại và hiệu nghiệm: nói thẳng trong prompt rằng bản in cuối LÀ sản phẩm bàn giao,
không có lượt sau; còn ~20% ngân sách thì **dừng đo và viết kết luận** với những gì đã có; ô nào
chưa xong thì ghi `KHÔNG_ĐO_ĐƯỢC` kèm lý do — **đó là câu trả lời hợp lệ, im lặng thì không**; và
lệnh nào bị từ chối quyền thì ghi vào mục *"chỗ không đo được"* rồi **đi tiếp**, đừng bỏ cả hướng đo.

**Antigravity (AG).** Chế độ duyệt của AG nằm trong CÀI ĐẶT APP (Agent auto-run),
kho không cấu hình hộ được. Khuyến nghị khi mở phiên AG cho packet của kho: bật
auto-run cho lệnh ĐỌC + chạy test; giữ hỏi cho terminal ghi ngoài worktree, mọi thao
tác đẩy/xoá ref, và browse ngoài workspace. Các chốt HÌNH DẠNG ở trên không chạy
trong AG — bù bằng chốt phía kho vẫn còn nguyên: `ops-don-ref` đòi gõ `XOA`/`TAO`,
cổng đăng lease theo danh sách cho phép, và `packet_loop` guard. Con trỏ từ
`AGENTS.md` sang mục này sẽ bổ sung ở packet sau (AGENTS.md nằm trong
RELEASE_MANIFEST — sửa nó kéo theo tái sinh manifest, tránh va write set đang mở).
