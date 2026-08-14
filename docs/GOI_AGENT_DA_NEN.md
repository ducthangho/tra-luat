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

## Gọi `claude` CLI không người trực — xem skill `goi-claude-cli`

Quy cách gọi headless (`claude -p` qua `launcher.py`) nằm ở
`.claude/skills/goi-claude-cli/SKILL.md`: bảng bốn chế độ `--permission-mode` đã đo,
vì sao `bypassPermissions` là ngõ cụt dưới root, bẫy trust im lặng khoá theo đường dẫn
KHO CHÍNH chứ không theo worktree, và vì sao `rc=0` ở đây không chứng minh được gì.
