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
python .claude/dev/launcher.py doctor --cai    # thiếu thì CÀI rồi đo lại
```

Thoát `12` khi thiếu công cụ **bắt buộc** (git, python). Thiếu `claude`/`codex`
chỉ là cảnh báo — có phiên không cần gọi agent nào cả.

`--cai` dùng bảng `cai_lenh` (argv theo nền, thử lần lượt `apt-get` rồi
`sudo apt-get`) rồi **đo lại** — báo cáo là trạng thái sau cùng, không phải lời
hứa "đã chạy lệnh cài". Công cụ không có lệnh cài máy-đọc-được trên nền đang chạy
sẽ vào `khong_tu_cai_duoc`, **không** bị bỏ qua im lặng. Mặc định `--cai` TẮT: tự
cài đè lên máy cá nhân của người dùng là vượt quyền.

### Công cụ của LƯỢT, không phải cờ tĩnh

`doctor` trả lời "máy này có gì". Câu hỏi khác — "**lượt này** cần gì" — hỏi ngay
tại chốt:

```bash
python .claude/dev/launcher.py run --require-tool codex ... -- codex exec ...
```

Thiếu, hoặc có trong PATH mà không chạy được ⇒ thoát `12` **trước khi** sinh con.
Đo được ngày 13-08-2026 trong container remote: `doctor` in `DU CONG CU BAT BUOC`
kèm rc=0 trong khi `codex` vắng mặt — vì `bat_buoc` là thuộc tính của *công cụ*,
mà "cần hay không" lại là thuộc tính của *lượt*. Một cờ tĩnh không nói được cả hai.

### Chạy được ≠ dùng được: chốt xác thực

```bash
--auth-probe '["codex","login","status"]'    # mảng JSON: mọi nền đọc giống nhau
--auth-probe /duong/dan/probe                # hoặc tên chương trình trần
```

Thoát `13` — tách khỏi `12` vì cách chữa khác hẳn: `12` là **cài**, `13` là
**đăng nhập**. Chốt đọc **nội dung** đầu ra chứ không đọc mỗi `rc`: một lệnh
`codex` chưa xác thực in `401 Unauthorized` rồi thoát **rc=0**, và launcher truyền
lại mã con nên sổ ghi `trang_thai: "xong", ma_thoat: 0` — một lượt *không hề chạy*
được ghi thành thành công. Cùng họ với bẫy số 3 ở đầu `launcher.py`.

Không tách chuỗi theo khoảng trắng và không qua shell: quy tắc trích dẫn của
`cmd.exe` khác POSIX, nên mảng JSON là dạng duy nhất đọc giống nhau ở mọi nền.

Đã đo trong container Claude Code web (12-08-2026): có `python`, `git`, `node`,
`claude`, `rg`; **không có** `codex`, `gh`, `pwsh`. Hook
`.claude/hooks/session-start.sh` gọi đúng một lệnh `doctor --cai` — **không** cài
`gh` và `pwsh`: kho này dùng GitHub qua MCP chứ không qua `gh`, và không còn đường
nào cần PowerShell. Hook không chép lại logic cài nữa; bảng công cụ sống một chỗ
duy nhất là `CONG_CU` trong `launcher.py`.

**Hook chỉ chạy nếu kho có mặt lúc phiên khởi động.** Đo được 13-08-2026: phiên
sinh bằng chương trình (`origin: claude_code_mcp_seed`) nhận kho *sau* SessionStart,
nên `settings.json` chưa tồn tại lúc hook đáng lẽ chạy ⇒ container không có `codex`
dù hook viết đúng. Phiên kiểu đó phải tự gọi `doctor --cai` sau khi có kho.

**Không được giả định Windows có `python3`.** Bản cài phổ biến chỉ có `python` và
`py` (bản Microsoft Store thì có thêm `python3`). Đừng bắt cài thêm bí danh —
`doctor` nhận cả ba tên.

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
