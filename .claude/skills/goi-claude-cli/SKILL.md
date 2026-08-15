---
name: goi-claude-cli
description: Gọi `claude` CLI ở chế độ không người trực (headless `-p`) cho một phiên executor/reviewer, qua `.claude/dev/launcher.py`. Dùng khi cần mở một phiên agent chạy nền theo prompt neo băm — nêu đúng cờ quyền, chốt trust, và những bẫy đã ĐO được trên container chạy root. Kích hoạt khi nói "mở phiên executor", "chạy prompt bằng claude CLI", "gọi agent nền", "spawn phiên claude".
---

# Gọi `claude` CLI không người trực

Mọi con số dưới đây **đo ngày 14-08-2026** trên container Claude Code web
(`claude` 2.1.231, `uid 0`). Đo lại trước khi tin, đừng chép làm chân lý.

## Công thức chốt

```bash
python .claude/dev/launcher.py run \
  --workspace   /duong/dan/worktree \
  --expected-repo        github.com/<owner>/<repo> \
  --expected-root-commit <sha40 commit gốc> \
  --expected-head        <sha40 head phải xuất phát> \
  --expected-ref         <tên nhánh> \
  --require-clean \
  --prompt-file            /duong/dan/prompt.md \
  --expected-prompt-sha256 <sha256 prompt> \
  --deadline-utc           <hạn lease dạng RFC3339> \
  --run-root /duong/dan/runs --name <ten-luot> \
  -- bash -c 'claude --permission-mode auto -p < "$1"' _ '{PROMPT_FILE}'
```

Chạy `check` (cùng bộ cờ, bỏ `--run-root`/`--name`/lệnh) **trước** — nó kiểm hết chốt
mà không gọi gì. Phải ra `KET LUAN : QUA HET CHOT` và `rc=0`.

Ba chi tiết trong lệnh con, mỗi cái đều đã trả giá:

- **`--permission-mode auto`** — xem bảng dưới, các chế độ khác không đủ hoặc bị chặn.
- **`-p < {PROMPT_FILE}`, KHÔNG phải `-p "$(cat …)"`.** Nội dung prompt phải đi qua
  **stdin**, đừng nội suy vào dòng lệnh: `$(cat …)` nở toàn bộ prompt vào **argv** của
  tiến trình, nơi mọi tiến trình cùng UID và mọi công cụ đo tiến trình đọc được — phá
  đúng chủ đích bản chụp `0600` và việc launcher cố ý KHÔNG ghi đối số thô vào
  `run.json`. Prompt lớn còn đụng trần độ dài đối số của hệ điều hành.
  Cho stdin bằng tệp cũng giải luôn việc `claude -p` treo chờ stdin (`Warning: no
  stdin data received in 3s`) — nên **không cần** `< /dev/null` nữa; nếu vì lý do khác
  mà không truyền prompt qua stdin thì mới cần nó.
  **Truyền đường dẫn làm ĐỐI SỐ VỊ TRÍ, đừng nhét vào phần mã shell.** Launcher thay
  `{PROMPT_FILE}` bằng đường dẫn THẬT; nếu chỗ thay nằm trong chuỗi lệnh của `bash -c`
  thì bash **phân tích nó như mã**. Hai lần trả giá, mỗi lần một tầng sâu hơn:

  | dạng viết | run-root | kết quả |
  |---|---|---|
  | `< {PROMPT_FILE}` | `run root` | `bash: /tmp/claude-0/run: No such file` · `rc=1` |
  | `< "{PROMPT_FILE}"` | `run-$HOME` | `bash: /tmp/claude-0/run-/root/…` · `rc=1` |
  | `< "$1"` + `_ '{PROMPT_FILE}'` | cả hai | **chạy đúng** |

  Dấu nháy chỉ chặn tách token, **không** chặn nở biến — `$HOME` vẫn nở bên trong dấu
  nháy kép, và một đường dẫn chứa thay thế lệnh còn **chạy được lệnh đó**. Đối số vị trí
  thì bash không bao giờ đọc như mã: đó mới là hàng rào, dấu nháy chỉ là mành che.
  (`_` đứng làm `$0`; đường dẫn thành `$1`.)
- **`{PROMPT_FILE}`** — launcher thay bằng một **bản chụp rời** trong thư mục lượt chạy.
  **Rời, KHÔNG phải bất biến** — đừng đọc nhầm hai chữ ấy. Launcher tạo tệp với quyền
  `0600` rồi thôi: nó **không** đặt cờ bất biến và **không** kiểm lại băm sau khi ghi
  (dòng 1173–1187 của `.claude/dev/launcher.py`). Nên một tiến trình **cùng UID** — đúng mô hình đe doạ đã
  viện ra ở gạch đầu dòng trên để bỏ prompt khỏi `argv` — vẫn ghi đè được bản chụp
  trong khoảng giữa lúc kiểm băm và lúc shell mở nó. `--expected-prompt-sha256` neo
  **tệp nguồn tại thời điểm kiểm**, không neo thứ con thật sự đọc.

  Cái nó CHẮC CHẮN cho: sửa tệp prompt gốc sau khi lượt chạy bắt đầu không ảnh hưởng
  lượt đang chạy. Có `{PROMPT_FILE}` mà quên `--prompt-file` thì launcher chặn, không
  để con mở một tệp tên `{PROMPT_FILE}` rồi báo xong.

## Bảng chế độ quyền — ĐO, không suy từ tên

| `--permission-mode` | sửa tệp TRONG workspace | lệnh bash biến đổi (vd `git commit`) | dưới `root` |
|---|---|---|---|
| `acceptEdits` | ✅ | ❌ **không** | chạy được |
| `dontAsk` | ❌ | ❌ | chạy được |
| `auto` | ✅ | ✅ | chạy được |
| `bypassPermissions` | — | — | ❌ **rc=1, bị chặn** |

**`--dangerously-skip-permissions` và `--permission-mode bypassPermissions` KHÔNG
dùng được khi chạy dưới root** — CLI từ chối thẳng:
`cannot be used with root/sudo privileges for security reasons`. Container Claude Code
web chạy `uid 0`, nên đây là ngõ cụt chứ không phải tuỳ chọn.

**Tên chế độ đánh lừa:** `dontAsk` nghe như "khỏi hỏi, cứ làm", thực tế là **"không
hỏi ⇒ từ chối"** — nó không ghi nổi một tệp trong chính workspace. Đừng chọn theo tên.

**`acceptEdits` không đủ cho executor:** nó cho sửa tệp nhưng chặn lệnh biến đổi. Đã
đo: `echo` chạy, `git add` + `git commit` **không** commit nào được tạo. Một executor
phải commit và push thì `acceptEdits` là chọn sai.

### ⚠ RÚT LẠI: `auto` KHÔNG chặn `git push`

Bản trước của mục này khai *"`auto` vẫn chặn `git push` — kể cả `--dry-run`, cấp bằng
`--allowedTools`"*. **Sai, và nó sống qua chín vòng cross-review.** Đo lại, ba nhánh chỉ
khác nhau ở `ask`/`allow` của `git push`:

| policy | `--allowedTools` | `git push --dry-run` |
|---|---|---|
| `git push` **không** ở `ask`, **không** ở `allow` | không có cờ | **CHẠY** (`rc=0`) |
| như trên | có cờ | **CHẠY** (`rc=0`) |
| `git push` **trong `ask`** | có cờ | **BỊ CHẶN** |

Ba dòng đó nói:

- Thứ chặn là **luật `ask`**, không phải chế độ quyền. Bản cũ **quy nhân sai đối tượng**:
  nó thấy chặn, thấy có cờ thì hết chặn, rồi gán nhân quả cho cái cờ.
- `--allowedTools` **không cứu được** khi có `ask`, và **không cần** khi không có ⇒
  **không tồn tại môi trường nào nó vừa cần vừa hiệu quả** trong kho này.

Nên: **đừng thêm `--allowedTools "Bash(git push:*)"` vào lệnh chạy.** Nếu `git push` bị
chặn, nguyên nhân là một luật `ask` — đọc mục ngay dưới, đừng đi tìm cờ.

**Giới hạn của phép đo, đừng suy rộng:** chỉ đo `git push --dry-run` tới một nhánh không
tồn tại. Push THẬT không được thử, nên không có số về nó.

Bài học đắt hơn con số: lời khai sai này đứng vững chín vòng vì nó **hợp lý** — và vì
bảng ở mục `ask` ngay bên dưới đã ghi `--allowedTools → bị chặn` **suốt thời gian đó**.
Hai chỗ trong cùng một tệp mâu thuẫn nhau, không ai đọc chúng cạnh nhau. Cross-review
bắt được mâu thuẫn ấy trước khi bắt được cái sai.

## `ask` THẮNG `allow` ở MỌI lớp — đây là tường, không phải cửa

Đây là mục giải thích ca "BỊ CHẶN" ở bảng vừa rút lại bên trên — và là chỗ đáng đọc khi
một lệnh không chạy.

**Đọc mục này theo đúng mốc thời gian của nó.** Số đo dưới đây lấy trên worktree ghim
commit TRƯỚC #111, lúc `ask` của `tra-luat` còn là:

```json
"permissions": { "ask": ["Bash(git commit:*)", "Bash(git push:*)", "Bash(clasp:*)"] }
```

`master` hôm nay (sau #111) chỉ còn **`ask: ["Bash(clasp:*)"]`** — `git commit` và
`git push` đã chuyển sang `allow`. Nên trên worktree dựng từ master hiện hành, cả mục
này lẫn cách chữa ở §"Đường thoát `ask`" đều **không cần dùng tới**; chúng chỉ áp cho
worktree ghim commit cũ. Vì sao worktree cũ vẫn dính dù master đã merge: xem
§"Settings nạp từ CÂY LÀM VIỆC" bên dưới — đó là cùng một cái bẫy, nhìn từ hai phía.

Cơ chế thì không đổi theo mốc nào, và đó mới là thứ đáng nhớ. Đã thử **ba** đường cấp
quyền cho một lệnh đang nằm trong `ask`, cả ba đều **KHÔNG** vượt được:

| cách cấp | kết quả |
|---|---|
| `--allowedTools "Bash(git push:*)"` | bị chặn |
| `.claude/settings.local.json` trong worktree | bị chặn |
| `.claude/settings.local.json` ở kho chính | bị chặn |

`ask` không phải "mặc định hỏi rồi allow sẽ ghi đè" — nó là **cấp cao hơn allow**.
Chạy không người trực thì không có ai để hỏi, nên `ask` = chặn cứng.

**Hệ quả phải nói thẳng: lệnh nào còn nằm trong `ask` thì agent KHÔNG tự chạy được khi
không có người.** Sau #111 danh sách ấy còn đúng một mục: `Bash(clasp:*)` — một **ranh
giới duyệt rộng**, phủ mọi lệnh `clasp` và **nhờ đó** phủ cả những lệnh chạm LIVE
(`deploy`, `push`, `run`). Đừng rút gọn thành *"mọi thao tác `clasp` chạm LIVE"*: nó
sai — `clasp --version` và `clasp --help` vô hại. Ranh giới cố tình rộng hơn tập nguy
hiểm, vì kẻ ranh giới hẹp thì phải liệt kê đúng, mà danh sách CẤM thì không bao giờ đủ.
Đó là chốt của chủ kho, không phải trục trặc cần lách.

### `--setting-sources user,local` vượt được — và đó là lý do KHÔNG dùng nó

Loại nguồn `project` thì luật `ask` biến mất và `git push` chạy. Nhưng đo cùng lượt:
**hook `PreToolUse` cũng biến mất** — `tl.py --apply` chạy tuột, không bị chặn.

Hook guard và luật `ask` **ở cùng một tệp** `.claude/settings.json`. Bỏ nguồn ấy là
tháo cả hai. Đây không phải cách cấp thêm một quyền; đây là **tháo chốt**. Muốn
executor chạy không người trực thì đường đúng là chủ kho **sửa luật `ask`** một cách
có chủ đích, không phải một lượt chạy tự bỏ nguồn settings.

### Nhân tiện, một lời khai sai đo được ngay tại đây

Lượt trên báo `PUSH=OK (new branch … created on origin)`. Đo lại bằng
`git ls-remote --heads origin <ten>`: **không có nhánh nào**. `git push --dry-run` in
`[new branch]` như một **dự báo**, và phiên kia đọc thành đã tạo. Lời tường thuật của
một agent về việc nó vừa làm cũng phải đo, y như mọi thứ khác.

## `auto` KHÔNG tắt chốt an toàn — đã đo cả hai lớp

Đây là lý do `auto` chấp nhận được cho lượt chạy không người trực, khác hẳn bypass:

| lớp | phép thử | kết quả dưới `auto` |
|---|---|---|
| hook `PreToolUse` của kho | `python scripts/tl.py --apply --help` | **bị hook chặn**, lệnh không chạy |
| `permissions.deny` trong `settings.json` | `rm -rf …` | **bị từ chối**, không thực thi |

Nên đừng đổi sang bypass "cho nhanh": nó vừa bị root chặn, vừa gỡ mất hai lớp này.

## Bẫy TRUST — im lặng và đúng chỗ đau

Nếu workspace chưa được tin cậy, CLI in một dòng rồi **chạy tiếp**:

```
Ignoring 12 permissions.allow entries from .claude/settings.json:
this workspace has not been trusted.
```

Nghĩa là toàn bộ allowlist của kho bị **bỏ qua sạch** mà lượt chạy vẫn tiếp diễn —
`rc` không phản ánh gì.

**Khoá trust là đường dẫn KHO CHÍNH, không phải worktree.** Chạy trong
`/tmp/…/wt` (một `git worktree`) mà CLI vẫn báo `projects["/home/user/tra-luat"]`:
`.git` của worktree là một TỆP trỏ về kho chính, nên Claude Code phân giải project về
đó. Sau khi bật trust cho đường dẫn kho chính, worktree nạp đúng hook và allowlist.

```bash
python3 - <<'PY'
import json, shutil
p = '/root/.claude.json'
shutil.copy(p, p + '.bak')                     # sao lưu trước khi sửa cấu hình người dùng
d = json.load(open(p))
d.setdefault('projects', {}).setdefault('<ĐƯỜNG DẪN KHO CHÍNH>', {})['hasTrustDialogAccepted'] = True
json.dump(d, open(p, 'w'), indent=2)
PY
```

## Settings nạp từ CÂY LÀM VIỆC — merge vào master KHÔNG cứu được worktree cũ

Bẫy này lộ ra khi chạy executor trên một nhánh neo commit cũ. Chủ kho đã merge bản nới
`ask` vào master, nhưng worktree ghim ở commit cũ vẫn mang **settings của commit ấy**,
nên `ask` vẫn chặn y nguyên. Đo trực tiếp trong worktree:

```
ask trong worktree: ['Bash(git commit:*)', 'Bash(git push:*)', 'Bash(clasp:*)']
git push trong allow: False
```

Nhớ tách hai phép phân giải, chúng KHÁC nhau và dễ nhầm:

| thứ | phân giải theo |
|---|---|
| **trust** (`hasTrustDialogAccepted`) | **git common dir** → về kho chính |
| **settings/hook/permissions** | **cây làm việc** → theo commit đang checkout |

Nên: trust bật một lần ở kho chính là đủ cho mọi worktree; còn `settings.json` thì mỗi
worktree mang bản của commit nó đứng.

### Đường thoát `ask` mà KHÔNG tháo chốt

**Chỉ cần tới khi buộc phải chạy trên worktree ghim commit TRƯỚC #111.** Dựng từ master
hiện hành thì bỏ qua mục này — `git commit`/`git push` đã nằm sẵn trong `allow`.

`ask` không ghi đè được — đã thử **bốn** cách, xem bảng ở mục trên cộng `--settings`
với `ask: []` (cũng thua). Nhưng có thể **bỏ nguồn `project` rồi CẤP LẠI chính sách**:

```bash
claude --permission-mode auto \
       --setting-sources user,local \
       --settings /duong/dan/policy.json
```

`policy.json` chép từ `.claude/settings.json` của **master** — **chép NGUYÊN TRẠNG,
đừng đặt `ask: []`.** Bản master đã bỏ đúng hai mục lỗi thời và **cố ý giữ lại
`Bash(clasp:*)`**; quét rỗng cả danh sách là gỡ một ranh giới duyệt phủ **mọi** lệnh
`clasp`, trong đó có các lệnh chạm LIVE. Hook `PreToolUse` **thu hẹp thiệt hại nhưng
không thay thế được**: nó bắt đích danh `clasp push` và `gas-deploy`, còn `clasp
deploy` / `clasp run` thì không — chi tiết và số đo ở ngay dưới.

Đo hai nhánh trên cùng một phép thử, khác nhau **đúng một khoá** `ask`:

| `policy.json` | `clasp --version` |
|---|---|
| chép nguyên trạng (`ask: ["Bash(clasp:*)"]`) | **BỊ CHẶN** |
| sửa thành `ask: []` | **CHẠY** — `rc=127`, tức chỉ trượt vì máy chưa cài `clasp` |

Đọc `rc=127` cho đúng sức nặng của nó, đừng hơn: nó chứng minh **ranh giới duyệt đã bị
gỡ** — một tiến trình `clasp` được phép khởi chạy. Nó **không** chứng minh lượt ấy chạm
LIVE; `clasp --version` chỉ in phiên bản, có cài cũng vô hại.

Phần còn phơi ra sau khi gỡ `ask` cũng **hẹp hơn** ta tưởng, phải đếm cho đúng. Hook
`PreToolUse` được cấp lại nguyên vẹn, và nó khớp `\bclasp\s+push\b` cùng `gas-deploy`
(dòng 15–16 của `.claude/hooks/pretooluse_guard.py`) rồi trả `permissionDecision: ask` — mà
`auto` không người trực đọc `ask` là chặn. Nên:

| lệnh | `ask: []` + hook còn nguyên |
|---|---|
| `clasp push` · `gas-deploy` | **vẫn chặn** — hook bắt đích danh |
| `clasp deploy` · `clasp run` · `clasp login` … | **lọt** — hook không khớp |

Chỗ hở thật là **những lệnh `clasp` hook KHÔNG liệt kê**. Kể `clasp push` vào nhóm lọt
là vẽ lỗ to hơn thực tế — và một lỗ vẽ quá cũng dẫn tới quyết định sai y như một lỗ bỏ
sót, chỉ theo chiều ngược lại.

Đó cũng là lý do `ask` phủ `clasp:*` chứ không liệt từng lệnh: hook đi theo danh sách
CẤM nên luôn có mục chưa nghĩ ra, còn `ask` đi theo tiền tố nên không cần nghĩ đủ.

Khác hẳn `--setting-sources user,local` trần trụi: ở đó hook chết theo, còn ở đây
`deny`, `hooks` và phần `ask` còn lại được cấp lại nguyên vẹn. Đo **bốn** lớp trên
chính bản nguyên trạng trước khi giao việc:

| lớp | phép thử | kết quả |
|---|---|---|
| `ask` → `Bash(clasp:*)` | `clasp --version` | **vẫn chặn** |
| hook `PreToolUse` | `tl.py --apply --help` | **vẫn chặn** |
| `deny` → `Bash(rm -rf:*)` | `rm -rf /tmp/…` | **vẫn chặn** |
| `deny` → `Read(**/.env)` | đọc `.env` | **vẫn chặn** |

Bốn dòng đó là điều kiện để dùng cách này. Thiếu một dòng thì bạn đang tháo chốt chứ
không phải cấp quyền — hãy đo lại, đừng suy từ việc "tôi đã chép đủ tệp".

Nhắc lại cho khỏi quên: **cả ba lượt đo trên đều trả `ma_thoat=0` ở mức launcher.** Thứ
phân biệt "bị chặn" với "chạy được" nằm trong `stdout.log`, không nằm ở mã thoát.

## `rc=0` KHÔNG phải bằng chứng đã làm việc

Lượt đo bốn chế độ quyền: **`bypassPermissions` trả `rc=1`** (CLI từ chối thẳng dưới
`root` — xem bảng ở trên). **Ba chế độ còn lại đều trả `rc=0`, mà chỉ MỘT thật sự ghi
được tệp.** Hai chế độ kia trả lời tử tế, thoát sạch, và không làm gì.

Đếm cho đúng vì đó chính là điểm: ca đáng sợ **không** phải `bypassPermissions` — nó
đỏ, nó tự khai. Ca đáng sợ là hai chế độ **xanh mà rỗng**. Bản trước của mục này viết
"cả bốn trả `rc=0`", vừa sai vừa làm loãng bài học bằng cách gộp một ca tự khai vào
nhóm im lặng.

Vậy nghiệm thu một lượt chạy phải neo **hành vi**, không neo mã thoát: tệp có tồn tại
không, commit có tăng không, băm có đổi không. Cùng doctrine với "cổng xanh nhờ `rc=0`
là cổng có thể bị lừa" trong `CLAUDE.md`.

Đo được lần thứ ba ở đúng chỗ đau: một phiên executor bị chặn quyền `git push` đã
dừng ở BƯỚC 0 và **không sửa một dòng nào**, mà `run.json` vẫn ghi
`trang_thai: xong`, `ma_thoat: 0`. Sổ lượt chạy nói "xong" theo nghĩa **tiến trình
kết thúc bình thường**, không theo nghĩa **việc đã làm**. Muốn biết có làm gì không
thì đọc `stdout.log` và đo cây làm việc (`git status --porcelain`, `git rev-parse
HEAD`) — đừng đọc `ma_thoat`.

Mặt tốt của cùng phép đo: phiên ấy **dừng đúng** thay vì làm bừa, vì prompt có stop
condition tường minh. Prompt không có stop condition thì một lượt bị chặn quyền sẽ
xoay xở lung tung rồi vẫn trả `rc=0`.

## cwd — đã đo, KHÔNG phải chỗ hỏng

Launcher sinh con với `cwd=workspace` (`subprocess.Popen(..., cwd=kq["workspace"])`).
Đo cả `bash -c` lẫn `bash -lc`: `$PWD` đều đúng worktree. Nên khi CLI nhắc tới đường
dẫn kho chính, đó là **phân giải project**, không phải con chạy nhầm thư mục — đừng
đi sửa cwd, sẽ mất thì giờ ở nhánh sai.

## Bảng mã thoát của launcher — ĐO, đừng đoán

| ca | mã |
|---|---|
| `{PROMPT_FILE}` trong lệnh mà **thiếu** `--prompt-file` | **2** (`MA_THAM_SO`) |
| có `--expected-prompt-sha256` mà thiếu `--prompt-file` | **2** |
| `--prompt-file` CÓ nhưng tệp thiếu / rỗng / **băm lệch** | **7** (`MA_PROMPT`) |
| workspace không phải kho git | **3** (`MA_GIT`) |
| quá hạn + đã giết được con · quá hạn + KHÔNG giết được | **124** · **125** |
| quá hạn + **không lấy được khoá danh tính con** | **10** (`MA_DANH_TINH`) |

Dòng cuối dễ sót vì nó **ghi đè** kết quả giết: dòng 1268–1270 của `.claude/dev/launcher.py` đặt `ma =
MA_DANH_TINH` khi `khoa is None and qua_han`, **bất kể** lượt giết thành hay bại. Nên
"quá hạn mà không dừng được" **không phải lúc nào cũng 125**. Đây là hành vi cố ý —
launcher từ chối giết theo một PID chưa xác thực, vì PID được tái dùng và giết nhầm
tiến trình của người khác còn tệ hơn để một tiến trình sống quá hạn. Tự động hoá đọc
bảng thiếu dòng này sẽ xếp `10` vào nhóm "lỗi lạ" và bỏ qua, trong khi nó là ca **cần
người xử lý**: có thứ đang chạy quá quyền và launcher đã nói thẳng là nó không dừng được.

Bản đầu của skill này khai nhầm ca thiếu cờ là `rc=7`; cross-review bắt được và số đo
là `2`. Rồi phép đo ĐẦU TIÊN của tôi lại ra `3` — vì thư mục thử **không phải kho
git** nên launcher chết ở chốt git trước khi tới chốt prompt. Dụng cụ đo sai chỗ cho
một con số sai, và con số sai ấy trông y như một phát hiện. Đo trong kho thật mới ra
`2`. Ghi lại vì đây là bẫy chung: **chốt chạy theo THỨ TỰ, nên mã thoát chỉ nói về
chốt ĐẦU TIÊN bị vấp.**

## Đọc kết quả lượt chạy

```
<run-root>/<short_id>/run.json      # ma_thoat, trang_thai, vân tay lệnh, workspace
<run-root>/<short_id>/stdout.log
<run-root>/<short_id>/stderr.log
```

`launcher.py status` xem sổ; `launcher.py stop` giết cây tiến trình — **nhưng không
phải mọi hậu duệ**, xem [#112](https://github.com/ducthangho/tra-luat/issues/112).

**Bản chụp prompt, hạn chót, và việc giết cây tiến trình: xem [#112](https://github.com/ducthangho/tra-luat/issues/112).**
Phần ấy đã được **cắt ra khỏi skill này** sau ba vòng cross-review liên tiếp cho thấy nó
sâu hơn mức một tài liệu hướng dẫn nên đi — và cần vá ở `launcher.py`, không phải ở
tài liệu. Hai điều cần biết ngay, phần còn lại đọc ở issue:

- `prompt.snapshot` chứa **nguyên văn prompt** và **không được bảo đảm xoá**. Với prompt
  nhạy cảm, tự kiểm bằng `find <run-root> -name prompt.snapshot -ls` và tự dọn — nhưng
  đọc #112 trước để biết vì sao dọn hàng loạt là sai.
- `--deadline-utc` **không** bảo đảm cả cây dừng khi hết hạn. Muốn rào thật thì phải
  dùng thứ ngoài launcher (container / cgroup / PID namespace). Không có thì khai đúng
  giới hạn: một lượt chạy có thể sống quá hạn lease, và sổ sẽ không nói cho biết.

Lỗi im lặng nằm ở **log**, không ở `run.json` — và phải đọc **CẢ HAI** log. Hai kiểu
hỏng đẩy dấu vết sang hai tệp **ngược nhau**, đã đo:

| kiểu hỏng | `stdout.log` | `stderr.log` |
|---|---|---|
| cờ sai (`--sandbox` xung khắc `--approve-for-me`) | **0 byte** | 206 byte |
| bị chặn quyền (ba lượt `clasp`/hook/`deny` ở mục trên) | 14–36 byte | **0 byte** |

Mở đúng một tệp là có lúc kết luận ngược hẳn. Và đừng trông vào `ma_thoat`
để phân biệt: lượt hỏng vì trust hoặc vì cờ quyền có thể cho **đúng** cặp
`trang_thai: xong` + `ma_thoat: 0` như một lượt thành công — chính tài liệu này ghi một
ca như vậy ở mục trên (executor bị chặn `git push`, không sửa dòng nào, `ma_thoat: 0`).
Thứ phân biệt được chỉ có hai: **log** và **hậu điều kiện hành vi** (`git status
--porcelain`, số commit, tệp có thật, băm khớp).

## Trước khi giao việc thật

1. `claude -p "Tra loi dung mot tu: OK" < /dev/null` — xác thực CLI còn sống. Không
   có bước này thì mọi chẩn đoán sau đều đoán mò. (Đây là ngoại lệ **có chủ ý** của luật
   "prompt không đi qua `argv`": chuỗi hằng sáu chữ, không bí mật, không phụ thuộc kích
   thước. Luật ấy bảo vệ *nội dung nhạy cảm* và *prompt dài* — nó không cấm chữ `-p`.)
2. `launcher.py check …` — `QUA HET CHOT`, `rc=0`.
3. Neo prompt bằng **băm**, không bằng tên nhánh: tên nhánh trôi và bị xoá.
4. Cho `--deadline-utc` khớp hạn lease — nhưng **đừng đọc nó thành "lượt chạy không
   sống quá quyền"**. Hạn chót chỉ rào tiến trình con trực tiếp; hậu duệ thoát được.
   Chi tiết và hướng vá: [#112](https://github.com/ducthangho/tra-luat/issues/112).
