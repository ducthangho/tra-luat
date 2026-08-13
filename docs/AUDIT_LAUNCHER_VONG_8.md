# Audit launcher vòng 8 — vá bốn khe hở còn treo

Ngày đo: 2026-08-13. Nền tại chỗ: Linux. Đợt này KHÔNG đi tìm lỗi mới — nó vá đúng
năm khe hở mà bản bàn giao vòng 7b đã ghi rõ là **đã biết, chưa vá**, cộng một lỗi
vệ sinh của chính bộ test lộ ra trong lúc vá.

Ranh giới bằng chứng nói trước, vì đó là thứ dễ đọc nhầm nhất ở đây: mọi con số
dưới đây đo trên **Linux**. Bốn khe hở được vá đều là đường Windows, nên phần lớn
bản vá chỉ có **phản chứng giả lập** ở nền này; phép đo thật thuộc về CI
`launcher (Windows thật)` và **chưa chạy tại thời điểm viết**.

## Khe hở đã vá

### #3 — `_khoa_danh_tinh` mất khoá với con ngắn ngủi trên Windows

Con thoát trước khi lần gọi powershell đầu tiên kịp nhìn thì CIM không còn thấy nó
(POSIX không dính vì `/proc/<pid>` còn ở dạng zombie). Sổ ghi `khoa_danh_tinh=null`,
và `stop` lượt đó từ chối vĩnh viễn bằng mã 10 — kể cả khi lượt chạy bình thường.

Vá: đọc thêm khoá từ **handle mà `Popen` đang giữ** (`GetProcessTimes`). Handle sống
qua lúc con thoát, và Windows không tái dùng PID chừng nào còn một handle mở.

Phần nguy hiểm không nằm ở chỗ lấy số, mà ở chỗ **quy đổi**. Hai nguồn khác nhau ba
lần:

| | CIM `CreationDate` | `GetProcessTimes` |
|---|---|---|
| epoch | năm 1 (`.Ticks`) | 1601 (FILETIME) |
| múi giờ | Local | UTC |
| độ phân giải | micro-giây | 100ns |

Quy đổi sai thì khoá **không bao giờ khớp**, và chốt danh tính hoá ra *luôn từ chối
giết* — hỏng âm thầm, tệ hơn hẳn không có chốt. Nên cả ba lệch được khử ở ba chỗ
khác nhau, mỗi chỗ chọn cách rẻ nhất:

- múi giờ khử **tại nguồn** — PowerShell gọi `ToUniversalTime()`. Cố ý không tự suy
  độ lệch múi giờ: nghĩ được tới DST là đã sai rồi;
- epoch khử bằng một hằng số cộng, và hằng số đó được `t84` **tính lại độc lập** bằng
  `datetime` chứ không chép từ mã;
- độ phân giải khử bằng cách hạ cả hai xuống micro-giây (`_khoa_win`).

Thêm một lớp nữa để sai sót còn lại không thể hỏng về phía im lặng: sổ ghi **cả hai**
khoá và `_khop_khoa` chấp nhận khớp bất kỳ. Không nới chốt — cả hai khoá đều nói về
thời điểm khởi động, nên PID bị tái dùng vẫn trượt cả bộ.

### #2 — `stop` không với tới Job Object

Job Object là cơ chế duy nhất trên Windows giữ được hậu duệ **mồ côi**, nhưng handle
của nó chỉ sống trong tiến trình `run`. `stop` là tiến trình khác nên phải rơi về
`taskkill` + ảnh chụp cha-con — đúng hai đường mù với mồ côi.

Vá: job có **TÊN** (`Local\tl-launcher-<run_id>`), tên nằm trong sổ, `stop` mở lại
bằng `OpenJobObjectW`. Kèm theo đó, khi có job thì job là **bằng chứng mạnh hơn ảnh
chụp** trong `_giet_cay`: ảnh chụp trả `{}` cho một cây chỉ còn mồ côi, và bản trước
đọc đó thành "đã tắt".

Mở job không được vẫn không được đọc thành "cây đã sạch": có thể job đã đóng (cờ
`KILL_ON_JOB_CLOSE` khi ấy đã giết cả cây), có thể lượt chạy đó không dựng được job.
Hai nghĩa đều lành nhưng khác nhau, nên đường cũ vẫn chạy tiếp.

### #1 — `Popen` không gán job lúc tạo

Gán job **sau** khi con đã chạy để hở một khoảng rất ngắn; cháu sinh trong khoảng đó
nằm ngoài job vĩnh viễn. Vá: sinh con với `CREATE_SUSPENDED`, gán job, rồi thả.

`Popen` đóng handle luồng chính ngay trong lúc tạo nên không `ResumeThread` được;
`NtResumeProcess` chỉ cần handle **tiến trình**, thứ `Popen` vẫn giữ. Có đường dự
phòng bằng Toolhelp, và nếu cả hai hỏng thì **giết con rồi báo hỏng** — một con treo
mãi sẽ nằm im tới hạn chót rồi lượt chạy khai "quá hạn", tức khai sai nguyên nhân, và
đó là hỏng nặng hơn hẳn khe hở vừa khép.

### #5 — phạm vi fail-closed của `_chup_cay` là suy luận

`t89` dựng cây hai tầng **thật** rồi gọi `_chup_cay` **thật**, chạy trên mọi nền; trên
Windows nó đi qua CIM thật của cả máy. Workflow Windows thêm một probe đếm số tiến
trình thật sự thiếu `CreationDate` trên runner. Suy luận thành số.

### #4 — số ca tự bỏ qua trên Windows

Từ 12 xuống 10. Hai ca lấy lại được vì lý do bỏ qua của chúng không đúng:

- `t33_stop_giet_that` bỏ qua **không nêu lý do**. Nó chạy được trên Windows, chỉ cần
  hỏi "còn sống không" bằng phép đo hợp lệ của nền ấy — và đây đúng là chỗ đáng đo
  nhất sau khi `stop` mở lại được job.
- `t51_ma_thoat_ngoai_khoang` bỏ qua vì "cần tín hiệu POSIX", nhưng ca này không đòi
  tín hiệu — nó đòi một mã thoát ngoài `0..255`, mà Windows có sẵn: tiến trình thoát
  `-1` cho mã thật `4294967295`. Chính docstring của ca lấy Windows làm ví dụ.

Mười ca còn lại cần `SIGTERM`/`SIG_IGN`/`setsid`/nhóm tiến trình, hoặc cần một shim
`git`/`python` không đuôi `.exe` — `CreateProcess` không tra `PATHEXT` cho tên không
đuôi nên `git.cmd` không chặn được lệnh `git`. Chúng ở lại, có lý do.

## Lỗi ngoài danh sách, tìm được trong lúc vá

**Bộ test rò monkeypatch ra module dùng chung.** `m.platform.system = lambda: "Windows"`
trông như sửa bản đang thử, nhưng `m.platform` **chính là** module `platform` của cả
tiến trình test: phép gán đó đổi `platform.system` cho **mọi ca chạy sau**, vĩnh viễn,
không ai khôi phục. `m.subprocess.run` y hệt.

Suốt bảy vòng không ai thấy vì mọi ca đứng sau đều tự giả lập nốt phần còn lại. Nó chỉ
lộ khi có ca **đo thật** — và ca đo thật ấy (`t89`) đã lặng lẽ đo một `platform` giả
cùng một `subprocess` giả, tức đo đúng cái nó vừa được viết ra để không đo. Sửa ở tầng:
`_ep_nen`/`_ep_subprocess` gán vào **tên toàn cục của module đang thử**, bản thật không
bị đụng.

**`_con_song_that` GIẾT thứ nó đang hỏi trên Windows.** Nó rơi xuống `os.kill(pid, 0)`,
mà trên Windows `os.kill` với tín hiệu khác `CTRL_*_EVENT` gọi thẳng `TerminateProcess`
— câu hỏi "còn sống không" tự giết mất đối tượng rồi trả `True` vì không có ngoại lệ
nào. Bẫy này đã được ghi trong nếp kho, và hàm được giới thiệu là đường an toàn để né
nó, nhưng chính nó dính. Nay hỏi bằng `GetExitCodeProcess` (259 = `STILL_ACTIVE`).

## Không vá được ở đây

- Toàn bộ đường Windows: Job Object có tên, `CREATE_SUSPENDED`, `NtResumeProcess`,
  `GetProcessTimes`, `GetExitCodeProcess`. CI `launcher (Windows thật)` phải đo.
- **Nửa múi giờ của phép quy đổi khoá không đo được ngay cả trên CI**: runner GitHub
  chạy ở UTC, nên bỏ `ToUniversalTime()` đi thì hai nguồn vẫn khớp ở đó. Chỗ đó chỉ
  đỏ trên một máy lệch UTC. Nói thẳng ra để không ai đọc `khoa_hai_nguon=khop` thành
  bằng chứng cho cả ba lệch.
- **`CREATE_SUSPENDED` không có đột biến**. Khoảng hở nó khép là một cuộc đua rất
  ngắn, không dựng lại được theo ý muốn; một ca chỉ khẳng định "cờ có mặt trong
  `creationflags`" thì chỉ chứng minh mã nói đúng điều mã nói. Không thêm đột biến
  không giết được ca nào. Nhánh **thả treo hỏng** thì đo được, và `t86` đo nó.
- Job Object thật có hơn 512 PID (nợ từ vòng 7) vẫn chưa dựng.

## Hai công cụ "có mặt" mà không dùng được — đo tại chỗ, 13-08

### `codex`: cài xong, `--version` rc=0, mọi lệnh 401

`doctor` báo `co codex  codex-cli 0.147.0`. Cùng lượt chạy đó, `codex exec` trả
`401`. Đây là lớp nói dối **cao hơn** lớp `which` mà `doctor` đã vá: chạy được
`--version` vẫn chưa phải gọi được.

Nguyên nhân tách làm hai, cả hai đều đo được chứ không suy:

1. **`OPENAI_API_KEY` trong môi trường bị codex bỏ qua.** Đặt biến rồi gọi, OpenAI
   trả đúng chữ `Missing bearer or basic authentication in header` — tức yêu cầu đi
   ra **không mang bearer nào cả**. Đối chứng: `curl` cùng lúc, cùng proxy, với
   `Authorization: Bearer <khoá giả>` thì OpenAI trả `Incorrect API key provided:
   <khoá giả>`. Vậy header đi lọt; codex chỉ không đặt nó.
2. **Khoá phải nằm trong `~/.codex/auth.json`**, ghi bằng `codex login --with-api-key`
   — đọc từ STDIN nên chạy được không cần trình duyệt.

Đã chứng minh hết đường bằng một khoá giả: sau `login`, lỗi đổi từ `Missing bearer`
thành `Incorrect API key provided: sk-thu-n***`. Nghĩa là transport, TLS và proxy
đều thông; thứ duy nhất còn thiếu là một khoá **thật**.

Đối chứng thêm cho câu hỏi "proxy có tự tiêm khoá không": gửi bearer
`proxy-inject` tới `api.openai.com` thì OpenAI trả lại **đúng chuỗi đó** trong
thông báo lỗi ⇒ proxy chuyển tiếp nguyên văn, **không** tiêm khoá OpenAI (khác với
`GH_TOKEN=proxy-inject` vốn được tiêm cho GitHub).

Hook `session-start.sh` nay đăng nhập bằng `OPENAI_API_KEY` nếu có, và **nói ra**
khi không có. Ghi rõ để ai đó cầm `doctor` quyết định: hiện `doctor` vẫn đọc
`codex` là "có" trong đúng lượt mà hook vừa cảnh báo nó chưa đăng nhập — hai dòng
đứng cạnh nhau trong một lần chạy. Ngưỡng "có mặt ⇒ xanh" là của `doctor`, không
sửa ở đây.

Còn một nhiễu vô hại: proxy **không hỗ trợ nâng cấp WebSocket** (README của proxy
nói thẳng), nên codex thử `wss://` 5 lần, in 5 dòng `ERROR ... 401`, rồi mới lùi về
HTTPS. Dễ đọc nhầm thành lỗi xác thực ở tầng mạng — không phải.

### `gh`: cài được, nhưng mọi lời gọi API bị chặn ở tầng phiên

`gh 2.63.2` cài xong chạy được. `gh api repos/{owner}/{repo}` và
`gh workflow run` đều trả `403 GitHub access is not enabled for this session. An
org admin must connect the Claude GitHub App for this organization.`; `gh pr list`
trả `403` từ GraphQL với ghi chú chỉ phục vụ "the pinned set of PR-review
operations". `GH_TOKEN` trong môi trường là chuỗi giữ chỗ `proxy-inject`.

Hệ quả cụ thể: **một phiên như phiên này không mở được PR, không gắn được nhãn
`windows`, không gọi được `workflow_dispatch`.** Chỉ `git push` đi được, vì nó qua
proxy git riêng chứ không qua API. Trước đợt này, điều đó nghĩa là thiết bị đo
Windows tồn tại nhưng phiên remote **không có cách nào chạm tới**.

Nên workflow nhận thêm tiền tố nhánh `do-windows/**` ở cần gạt `push`: đẩy một
commit có dụng tới `.claude/dev/**` lên tiền tố đó là phép đo chạy. Bộ lọc `paths`
vẫn áp — commit không dụng tới các đường đó thì job **không chạy**, và "không chạy"
trông y hệt "xanh".

## Ghi nhận

- Trước sửa, trên commit `b666ded`: `83/83` ca (qua 82, bỏ qua 1) · đột biến `42/42`
  (1 không đo được) · `doctor` rc=0.
- Sau sửa: **`91/91` ca** (qua 88, bỏ qua 3, hỏng 0) · **đột biến `50/50`**
  (2 không đo được trên Linux) · ruff F sạch · 17/17 bước gate `rc=0` ·
  `python3 scripts/tl.py --selftest` ra 1697/1697.
- Ba ca bỏ qua trên Linux là `t62` (fixture Windows, bản POSIX là `t63`) và hai ca
  mới `t90`/`t91` — cả hai đo đúng đường chỉ tồn tại trên Windows.
- `RELEASE_MANIFEST.json` giữ 179 mục: không tệp runtime nào được thêm. Ratchet
  `docs/` nâng đúng 56→57, cây thật 235→236.
