---
name: cross-review
description: Review chéo khác nền một PR packet của protocol đa phiên (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; mọi quy tắc review, mức assurance và tiêu chí hoàn tất nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-packet] [so-PR]"
---

# Adapter `cross-review` — Claude Code

**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §8 (mức review, quyền của người review, xử lý quota) và
§13 (trigger, hai trục, dạng verdict, nơi ghi verdict, định nghĩa hoàn tất).

Tệp này **không tóm tắt** những mục trên — đợt đầu của chính adapter này chép §13 rồi ghi sai nơi
đăng verdict. Chốt cơ học:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py doctrine-scan --root .
```

Dưới đây chỉ có cú pháp của nền.

## Kiểm tra công cụ

Skill này chạy được hay không phụ thuộc `codex` (hoặc provider reviewer được chỉ định),
mà container phiên **không có sẵn** (đo 17-08-2026: `codex` vắng, `gh` vắng — hook phiên
không chạy vì `CLAUDE_PROJECT_DIR` không được đặt khi kho gắn giữa phiên).

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/launcher.py doctor            # kiểm tra toàn bộ công cụ (CONG_CU)
npm install -g @openai/codex                     # nếu doctor báo `khong codex`
"$PY"  .claude/dev/launcher.py chuan-bi          # CODEX_AUTH_JSON -> ~/.codex/auth.json
codex --version                                  # bằng chứng THẬT về phiên bản codex CLI
```

`doctor` in rõ bảng trạng thái `KHA DUNG` và các công cụ còn thiếu — đọc kỹ mục `KHA DUNG`
thay vì chỉ dựa vào mã thoát tiến trình.

Về thời điểm preflight, tính độc lập và fallback khi thiếu quota, xem protocol §8/§13
và con trỏ provider trong `AGENTS.md`.

## Cú pháp bộ chọn model/effort

Bảng dưới mô tả các bậc hiện có của `.claude/dev/chon_reviewer.py`; chính sách review
và mức assurance xem protocol §8.

| điểm | model | effort |
|---:|---|---|
| `<= 0` | `claude-opus-5` | `high` |
| `1–2` | `claude-opus-5` | `xhigh` |
| `3–4` | `claude-fable-5` | `xhigh` |
| `>= 5` | `claude-fable-5` | `max` |

`--bac-truoc model,effort` truyền bậc trước cho bộ chọn. Khi nhận cờ này, hàm `chon`
trả bậc không thấp hơn bậc đã truyền; thiếu cờ thì nó không có dữ liệu bậc trước.

Ba bẫy CLI đã đo 27-08-2026, không phải giả định:

- `--effort khong-ton-tai` chỉ cảnh báo rồi lùi im lặng về mặc định; kết quả không ghi đã lùi.
- `--model claude-khong-ton-tai-9` không chạy review nào nhưng vẫn trả `rc=0`.
- Trong 9 lượt, `haiku-4-5` có 8/9, `fable-5` 6/9, `opus-5` 3/9 và `opus-4-8` 2/9; cả hai lượt `opus-4-8` là lượt tụt giữa chừng thật.
  **`rc` và `subtype` không đủ để nhận diện model.** Hàm `kiem_ket_qua` lấy `canonicalModel`
  nếu có, nếu không lấy tên khóa; bỏ danh tính có tiền tố `claude-haiku-`, rồi so tập chính
  với `{model yêu cầu}`. Nó phân biệt model yêu cầu vắng với model lạ có mặt.

Giới hạn của hàm: không đo phần công việc của model phụ;
`{fable-5: 500 outputTokens, haiku: 90000}` vẫn có thể đạt phép so danh tính.

Probe ngắn chỉ loại được ca *model hoàn toàn không gọi được*; nó không chứng nhận lượt dài sẽ giữ model.
Đo 27-08: probe xanh 3/3 rồi lượt dài vẫn tụt hoàn toàn. Lệnh đọc `modelUsage` nằm dưới ví dụ phóng.

Ví dụ gọi bộ chọn:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" .claude/dev/chon_reviewer.py --review-class sensitive \
  --effective-review-class sensitive \
  --duong-dan a.py,b.md --so-dong 120 --luot 2 \
  --bac-truoc claude-fable-5,max --json
```

Nếu lease có `effective_review_class`, đút **cả hai** trường bằng `--review-class` và `--effective-review-class`; bộ chọn tự lấy lớp cao hơn, không lấy `max` bằng tay.

Phóng Claude reviewer headless, cấp đúng công cụ cần để review, và giữ JSON nguyên vẹn:

```bash
claude --model <id> --effort <bac> --output-format json --allowedTools Bash Read Write Edit Glob Grep --permission-mode acceptEdits --add-dir <sandbox> -p < PROMPT.md > reviewer.json
```

Mẫu trên đưa prompt qua stdin; kích thước prompt không cộng vào một đối số argv và nội dung
không nằm trong dòng lệnh tiến trình. Phép đo 27-08-2026 từng chạy được cả dạng argv và stdin,
nhưng không xác định kích thước prompt tối đa. Dưới root, `--dangerously-skip-permissions`
báo *"cannot be used with root/sudo privileges for security reasons"* rồi thoát `rc=1`
sau `1.151s`; ví dụ dùng `--allowedTools` cùng `--permission-mode`.

Cú pháp đọc `modelUsage` từ JSON bằng vị từ dùng chung với CI:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -c 'import json,runpy,sys; m=runpy.run_path(".claude/dev/chon_reviewer.py"); print(m["kiem_ket_qua"](sys.argv[1],json.load(open(sys.argv[2],encoding="utf-8"))))' <id> reviewer.json
```

Mục này **KHÔNG thay** `docs/PROTOCOL_DA_PHIEN.md` §8; nó chỉ nói chọn bậc nào và cú pháp đo model thực sự đã chạy.

## Reviewer là `codex` — model, effort, quota: bốn phép đo, không phải giả định

Bảng bậc ở trên là của reviewer **`claude`**. Khi reviewer là `codex` thì cú pháp và các chỗ gãy khác
hẳn; dưới đây đo 12-09-2026 trên chuỗi #518.

```bash
# Prompt qua STDIN, không qua argv — cùng dạng `- < PROMPT.md` đã dùng ở mục "Chạy nền kia
# trong sandbox". Prompt đặt trong argv có hai chỗ gãy: vượt giới hạn kích thước đối số của
# nền khi diff/evidence lớn, và lộ nguyên văn trên bảng tiến trình suốt lượt chạy.
codex exec -m <model> -c model_reasoning_effort="xhigh" \
  --cd <sandbox> --sandbox workspace-write --skip-git-repo-check - < PROMPT.md
```

**Dạng này KHÔNG dùng được khi bọc bằng `launcher.py run`**: nó cho tiến trình con
`stdin=DEVNULL` (xem `.claude/dev/launcher.py:lenh_run`), nên `codex exec -` nhận EOF.
Đo với `codex-cli 0.154.0`: stdin rỗng làm CLI thoát rc=1, báo `No prompt provided via stdin.`,
chưa chạy review. Bọc bằng launcher thì truyền `--prompt-file` + `--expected-prompt-sha256`
và đưa cho `codex` một chỉ thị NGẮN trỏ vào `{PROMPT_FILE}` (launcher thay bằng đường dẫn
bản chụp), chứ đừng dán cả prompt vào argv.

1. **Trong phép thử #518, `gpt-5.3-codex-spark` từ chối effort `max`.** Thông báo HTTP 400 liệt kê
   `low`, `medium`, `high`, `xhigh`; `xhigh` là mức cao nhất trong danh sách của phép thử đó.
   Danh sách ấy không xác định effort hợp lệ cho model khác.
2. **Ba model bị tài khoản ChatGPT dùng trong #518 từ chối:** `gpt-5.3-codex`, `gpt-5.1-codex-max`,
   `gpt-5-codex`, với lỗi 400 *"not supported when using Codex with a ChatGPT account"*.
   Đây là lỗi khác hết quota; ba lần từ chối không cho biết toàn bộ tập model tài khoản được dùng.
3. **Thuật lại ở #518:** `gpt-6-astra` báo *"try again at Sep 15th"* nhưng một lần gọi sau khoảng
   4 giờ chạy được; khi ấy `gpt-5.3-codex-spark` báo cạn, connector GitHub (`@codex review`) cũng
   từng báo cạn. Các quan sát này chưa xác định quota riêng theo model, số pool hay tính độc lập.
   Probe ngắn chỉ đo khả năng đáp ứng tại lúc gọi, không bảo đảm quota cho cả lượt review;
   thông điệp reset vẫn là dữ liệu do dịch vụ báo. Xử lý quota theo protocol §8.
4. **Đầu `stderr.log` ghi model/effort mà CLI công bố cho lượt chạy.** Xem ngữ cảnh đầu tệp bằng:

```bash
sed -n '1,80p' <run-root>/<short_id>/stderr.log
# rc=0: doc duoc tep (ke ca tep rong), chua xac nhan co header hay du hai truong.
```

Lệnh chỉ in 80 dòng đầu; nếu chưa thấy đủ header CLI thì đọc tiếp log. Chỉ lấy `model:` và
`reasoning effort:` trong header khởi tạo của đúng lượt; dòng cùng tên trong prompt/output
không thay được trường header bị thiếu. Không xác định được header thì chưa đo được hai trường.

Header này không phải thống kê model thực thi mọi yêu cầu như `modelUsage` của lane `claude`.
Hồ sơ `r368` ghi lời khai `xhigh` lệch header `none`; đó là đối chiếu hai nguồn khai,
không đo tác động của effort lên độ phủ review.

### `launcher.py run` có thể còn ghi `dang_chay` sau khi container chết

Theo thuật lại hai lần ở #518, container remote khởi động lại giữa lượt; lúc kiểm lại,
`run.json` vẫn ghi `trang_thai: dang_chay`, `ma_thoat: null` dù PID cũ không còn.
Các phép kiểm dưới đây thu thêm dấu hiệu; chưa chứng minh phải đủ cả ba mới chẩn đoán được:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhan CA BA ten
"$PY" -m json.tool <run>/run.json      # doc pid va khoa_danh_tinh; loi doc != tien trinh chet

# Chay tu goc clone: goi cung ham launcher, khong thay bang `ps -o lstart`.
# Tren Linux, ham doc TOAN ban ghi /proc/<pid>/stat, cat sau dau ')' cuoi cung;
# ten tien trinh co khoang trang, dau ')' hoac xuong dong van duoc xu ly cung cach.
# rc=1 / KHONG_DO_DUOC: ham khong doc duoc khoa; khong suy ra tien trinh da chet.
"$PY" -c 'import runpy,sys; k=runpy.run_path(".claude/dev/launcher.py")["_khoa_danh_tinh"](int(sys.argv[1])); print(k or "KHONG_DO_DUOC"); sys.exit(0 if k else 1)' <pid>
ps -p <pid> -o pid=,stat=   # `Z` = zombie da thoat; PID ton tai KHONG chung minh dung tien trinh

# Hai mau moc gio + kich thuoc, cach nhau mot khoang da dinh — mot mau khong do duoc chuyen dong.
stat -c '%Y %s' <goi>/VERDICT.md; sleep 60; stat -c '%Y %s' <goi>/VERDICT.md

tail -50 <run>/stderr.log   # doc ca log neu can; loi reconnect khong xac dinh trang thai cuoi
```

Thiếu/hỏng sổ hoặc lệnh lỗi là **KHÔNG ĐO ĐƯỢC**; không đọc được khoá không chứng minh đã chết.
So hai khoá của cùng PID trong cùng hệ điều hành, lần khởi động và không gian PID: khác khoá
là dấu hiệu PID đã được tái dùng; khớp khoá chỉ đối chiếu danh tính, chưa xác nhận còn sống.
Đọc cả trạng thái: `Z` là zombie đã thoát dù khoá còn khớp. Các lệnh đọc ở những thời điểm
khác nhau; trạng thái không phải `Z` cũng không chứng minh reviewer còn tiến triển hay đã hoàn tất.

Hai mẫu mốc giờ **giống nhau cũng vẫn là `KHÔNG ĐO ĐƯỢC`**, không phải bằng chứng đã chết: một
reviewer còn sống có thể im giữa hai lần ghi. Chỉ mẫu **đổi** mới chứng minh còn chuyển động.

Ghi `VERDICT.md` tăng dần (mục bên dưới) giúp giữ phần đã ghi khi lượt bị ngắt.
Hai sự cố thuật lại không đo mức lợi ích hay tốc độ mất dữ liệu so với bộ lọc.

### Sandbox của lượt codex ở #518 đã từ chối lệnh dọn thư mục

Lượt đó nhận `Rejected("... rejected: rm -f style commands are not permitted. Use a safer approach")`
khi dùng `rm -rf`. Đây là hành vi của môi trường đã thử, không xác định policy mọi sandbox Codex.
Trong môi trường ấy, có thể dùng `mktemp -d` để dựng chỗ thử. Ví dụ tạo thư mục dưới một gốc
đã chọn: `mktemp -d -p <goc-rieng>`. Lệnh này chỉ tạo thư mục; không thu hiện vật, đặt hạn lưu
hay tự dọn các bản sao.

Các bản sao được giữ lại chiếm dung lượng và lưu cả vật liệu review cũ trên runner sống lâu.
Về quyền ghi, phân công và vòng đời công việc, xem protocol §4/§8/§13 cùng chỉ thị điều phối
của lượt. Adapter này không ấn định bên dọn, tập đường dẫn được phép xoá hoặc hạn lưu.

## Khi PAT là chính tài khoản tác giả PR

`pull_request_review_write` với `event=REQUEST_CHANGES` sẽ bị GitHub từ chối:
*"Can not request changes on your own pull request"* (đo trên PR #141). Đường còn
lại là **comment** (`add_issue_comment`). Comment không mang trạng thái review chính thức
của GitHub. Cách khai transport và xác định assurance xem protocol §8/§13.

Trigger reviewer bot của kho: comment `@codex review` trên PR.

## Lấy diff của ĐÚNG head SHA

Trong ví dụ, `<base_sha>` và `<reviewed_sha>` là hai OID đã chốt cho lượt.
`gh pr view` in metadata tại lúc gọi; hai lệnh Git dùng trực tiếp cặp OID ấy.

```bash
gh pr view 56 --json headRefOid,headRefName,state,statusCheckRollup
git diff <base_sha> <reviewed_sha> > diff.patch
git diff --numstat <base_sha> <reviewed_sha> > numstat.txt
```

Hợp đồng `reviewed_sha` và xử lý khi head đổi: xem protocol §8/§13.

`§8`/`§13` cho hợp đồng, **không** phân xử VÌ SAO head đổi — mà hai nguyên nhân đòi hai hành động
ngược nhau, nên bảng này ở lại:

| head đổi vì | hành động |
|---|---|
| **tác giả đẩy commit mới** vào nhánh packet | bản duyệt cũ hết hiệu lực ⇒ **làm lại** vòng trên head mới |
| **base trôi** (nhánh mặc định tiến lên) | **merge base TRƯỚC**, rồi mở vòng trên head SAU merge |

**Đo `base` trước vòng mà bạn dự đoán sẽ ra `approve`** — nghĩa vụ, không phải gợi ý:

```bash
git merge-base --is-ancestor origin/<nhánh mặc định> HEAD   # rc khác 0 ⇒ CÓ DRIFT
```

Hai nợ CÓ TÊN, chưa ai đóng: `DIEU-KIEN-VONG-CUOI-KHONG-DO-DUOC` (*"dự đoán vòng này là cuối"* là
phán đoán của phiên, không đo được) · `HEAD-DOI-VI-HIEN-VAT-REVIEW` (head đổi vì hiện vật của CHÍNH
lượt review — bảng trên chưa phân xử; xếp vào hàng thứ nhất tạo vòng lặp không bao giờ đóng).

## Dựng mirror trong sandbox — cú pháp nền, và ba chỗ đã gãy thật

Ví dụ dưới dùng clone rời và checkout detached. Worktree dùng chung kho Git với cây nguồn;
quyền reviewer và yêu cầu cách ly xem protocol §8/§13.

```bash
RV=<thu-muc-clone-rieng>
git clone -q <nguồn> "$RV"
git -C "$RV" remote set-url origin https://github.com/<chủ>/<kho>   # BẮT BUỘC — xem (1)
git -C "$RV" fetch -q origin <nhánh>
git -C "$RV" checkout -q --detach <exact-sha>
git -C "$RV" status --porcelain    # in thay đổi Git đang thấy trong worktree
```

1. **Clone từ ĐƯỜNG DẪN cục bộ để lại `origin` là đường dẫn, và `launcher.py` từ chối với `rc=11`**
   (`kho lech: mong doi github.com/<chủ>/<kho>, thuc te (khong co remote)`) khi
   kiểm bằng `--expected-repo`. `remote set-url` đổi chuỗi remote mà chốt này đọc;
   chi tiết các cờ neo kho xem `docs/GOI_AGENT_DA_NEN.md`, mục "Neo theo *kho*, không theo đường dẫn".
2. **`git fetch origin <nhánh>` gãy nếu nhánh chỉ tồn tại dưới dạng remote-tracking ở nguồn cục bộ**
   (`couldn't find remote ref`). Vô hại khi commit đã có sẵn trong clone, nhưng đừng đọc nó thành
   "sandbox hỏng" — kiểm bằng `rev-parse HEAD`, không bằng mã thoát của `fetch`.
3. **Phiên headless NGOÀI kho không kế thừa `.claude/settings.json`** — nó in
   `Ignoring N permissions.allow entries: this workspace has not been trusted`.
   `--allowedTools` ở ví dụ Claude phía trên truyền danh sách công cụ tường minh.

Hai lệnh sau quan sát thay đổi Git còn lại và commit mới ở thời điểm kiểm:
`git -C "$RV" status --porcelain` và `git -C "$RV" log --oneline <head>..HEAD`;
có thể chạy cùng phép đọc trên kho nguồn. Output rỗng không chứng minh cả lượt không ghi:
thay đổi đã hoàn nguyên, tệp bị Git bỏ qua và lịch sử thao tác không nằm trong hai output ấy.

## Chạy nền kia trong sandbox

```bash
codex exec -s workspace-write --skip-git-repo-check --cd <sandbox> - < PROMPT.md
```

Ví dụ bố trí sandbox dùng một thư mục ngoài kho, gồm `SPEC.md`, `diff.patch`, `numstat.txt`,
trích protocol, `EVIDENCE.md` và bản sao cây. Một lượt phạm vi mở từng đọc nhầm transcript
ngoài kho và sau 40 phút chưa có kết luận. Phạm vi đọc/ghi và yêu cầu evidence xem protocol §8/§13.
`--sandbox workspace-write` là cờ chọn chế độ sandbox của CLI.

### Mirror trong sandbox — khi §8 đòi năng lực đo

Điều kiện cấp bản sao và phạm vi sandbox: xem protocol §8/§13. Ví dụ cú pháp đặt mirror
và working clone dưới cùng thư mục `$R`:

```bash
R=<sandbox>
git clone --quiet --bare --no-local <kho> "$R/kho.git"
git -C "$R/kho.git" fetch --quiet <kho> '+refs/remotes/origin/*:refs/heads/*'   # nap DU ref
git clone --quiet "$R/kho.git" "$R/cay-kho"
git -C "$R/cay-kho" fetch --quiet origin '+refs/heads/*:refs/remotes/origin/*'
git -C "$R/cay-kho" config core.abbrev 7        # BAT BUOC — xem duoi
git -C "$R/cay-kho" checkout --quiet <reviewed_sha>
```

`core.abbrev` điều khiển độ dài SHA viết tắt mà `doc-claims-check` đọc.
Phép đo clone PR #252 và yêu cầu cấu hình nằm ở protocol §8; lệnh trên đặt giá trị `7`.

**Cú pháp đối chiếu một cổng trên hai cây tại `reviewed_sha`.**

Yêu cầu đối chiếu môi trường xem protocol §8. Ví dụ worktree nền dưới đây checkout
cùng commit với clone để giảm một nguồn khác biệt khi đọc kết quả:

```bash
git -C <kho> worktree add --detach /tmp/nen-<reviewed_sha> <reviewed_sha>
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
cd /tmp/nen-<reviewed_sha> && "$PY" scripts/tl.py doc-claims-check --strict; echo "nen     rc=$?"
cd "$R/cay-kho"            && "$PY" scripts/tl.py doc-claims-check --strict; echo "sandbox rc=$?"
git -C <kho> worktree remove /tmp/nen-<reviewed_sha> --force
```

Mỗi dòng `echo` in mã thoát của chuỗi `cd && "$PY" ...` ngay trước nó. Nếu `cd` lỗi,
cổng chưa chạy và số in là mã lỗi của `cd`; bản thân `echo` vẫn có thể trả 0. Khi `cd`
thành công, số in là mã thoát của lời gọi Python. Hai mã bằng nhau chưa chứng minh
môi trường tương đương; hai mã khác nhau chưa định vị được nguyên nhân.

**Phạm vi của phép so ref.** Yêu cầu kiểm nguồn và báo cáo giới hạn xem protocol §8 và
`CLAUDE.md`, mục `for-each-ref` đọc bộ đệm. Trong sandbox không mạng, hai trạng thái `origin`
cho hai loại kết quả khác nhau:
· **trước `set-url`** — `origin` trỏ vào chính mirror vừa tạo, nên `ls-remote` `rc=0` và **đếm head của
chính mirror** (đo được: 201 head), tức không có nguồn có thẩm quyền nào để so;
· **sau `set-url`** — `origin` là URL HTTPS thật nhưng sandbox không ra được mạng, nên `ls-remote`
`rc=128`, **0 dòng**. Nó KHÔNG "đếm mirror": nó không đếm gì cả.
Mirror chỉ chứa ref đã được nạp từ nguồn. Ví dụ phép so sau dùng remote của kho nguồn;
nhánh `ls-remote` cần kết nối đến remote đó:

```bash
cd <kho>
git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort            > /tmp/mc
git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin \
    | grep -v '^HEAD$' | sort                                           > /tmp/cb
comm -23 /tmp/mc /tmp/cb        # tên có ở nguồn remote, thiếu ở bộ đệm cục bộ
```

**So bằng TẬP TÊN, không bằng `wc -l`** — hai tập cùng lực lượng vẫn có thể lệch (một nhánh cục bộ đã
bị xoá trên máy chủ cộng một nhánh mới chưa fetch), và `refs/remotes/origin/HEAD` tượng trưng làm số
đếm lệch sẵn 1 mà chẳng ai mù. Bản đầu của chính mục này đếm bằng `wc -l` **ngay dưới một câu trỏ về
doctrine cấm làm thế** — cross-review PR #261 bắt (P1).

Sau khi clone, ví dụ dưới đối chiếu tên và OID của các ref `refs/remotes/origin/*`
(trừ ref tên `HEAD`) giữa kho nguồn và clone. Nó không kiểm mọi namespace ref
hoặc tính toàn vẹn mọi object; dòng cuối chỉ đọc cờ shallow:

```bash
diff <(git -C <kho> for-each-ref --format='%(refname:lstrip=3) %(objectname)' refs/remotes/origin | grep -v '^HEAD ' | sort) \
     <(git -C "$R/cay-kho" for-each-ref --format='%(refname:lstrip=3) %(objectname)' refs/remotes/origin | grep -v '^HEAD ' | sort)
echo "ref diff rc=$?"
git -C "$R/cay-kho" rev-parse --is-shallow-repository        # true/false về shallow
```

Trong sandbox không mạng, các phép đọc này không cập nhật trạng thái GitHub trực tiếp.
Bài học #309 (`evidence-origin-khong-phai-mirror-cuc-bo`): sau `remote set-url`,
`origin` mang URL HTTPS thật; gọi nó là mirror cục bộ là mô tả sai cấu hình. Trước `set-url`,
`ls-remote` tới mirror đọc ref cục bộ; sau `set-url`, lời gọi tới HTTPS có thể thất bại vì mạng.
Hai kết quả này không phải cùng một phép đo nguồn.

## Bộ lọc nền cắt lượt giữa chừng — ghi chép #513

Hồ sơ 13 lượt packet #513 (12-09-2026) ghi bộ lọc nội dung cắt 3 lượt khi reviewer
đang tự soạn nội dung tấn công. Bảng dưới ghi thời điểm ngắt và hiện vật còn lại;
không đo được cơ chế bộ lọc hoặc hiệu quả nhân quả của cách viết prompt.

### Hiện vật còn lại ở ba lượt bị ngắt

| lượt | bị cắt ở | giữ được verdict |
|---|---|---|
| 8 | 154 s | **KHÔNG** — mất trắng, phiên chính phải tự đọc log probe mới cứu được |
| 11 | 437 s | **KHÔNG** — 35 lệnh, 3 lỗi thật, không một dòng verdict |
| 12 | 299 s | **CÓ** — verdict còn nguyên một hướng kèm output thật |

Prompt lượt 12 có ba câu về ghi sớm và cập nhật verdict. Bảng không xác định đây là
khác biệt duy nhất giữa các lượt hoặc cô lập tác động của ba câu đó.

Cú pháp ghi Markdown thông thường: `>` tạo/ghi lại tệp, `>>` nối thêm; đây là thao tác
trên tệp, không đặt trạng thái verdict khởi tạo, lịch cập nhật hay điều kiện hoàn tất.
Hợp đồng verdict và phân công phản chứng xem protocol §8/§13 cùng prompt được giao.

Kênh "nêu bằng lời" KHÔNG phải giải pháp hạng hai: **toàn bộ giá trị của lượt 8 đi qua đúng nó** —
nó nêu hai hướng trước khi chết, một hướng hoá ra là lỗi sản phẩm thật.

## Mẫu trình bày hướng thử

Đo được, cùng packet, hai lượt liền:

| lượt | prompt nói gì | kết quả |
|---|---|---|
| 9 | *"nếu không tìm ra gì thì liệt kê hướng đã thử"* | `approve`, và 4 "hướng đã thử" hoá ra **cả 4 đều là việc bắt buộc ở phần khác của prompt** — không hướng nào độc lập |
| 10 | **bảng SĂN ≥ 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT** | **8 hướng**, **2 lỗi sản phẩm thật** |

Dữ liệu hai lượt cho thấy hai kết quả với hai prompt; không xác lập một tiêu chí
`approve` chung. Ví dụ khối trình bày một hướng thử:

```
HƯỚNG <n>: <tên>
  giả thuyết : <nếu ... thì ... sai>
  lệnh       : <lệnh đã chạy>
  output     : <output thật, cắt gọn>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
```

Các trường trong ví dụ là nhãn trình bày. Số hướng, độ độc lập, xử lý lịch sử và
điều kiện nhận verdict thuộc protocol §8/§13 cùng yêu cầu của lượt.

## Quan sát tiến trình con còn lại

Tiến trình con có thể còn lại khi bộ test bị ngắt; kết quả phụ thuộc cách quản lý vòng đời con.
Đo 12-09-2026: hai lượt bị giết để lại **526 tiến trình `ban_sao_*` còn sống**, RAM `14,5/16 GB`,
và các phép đo sau chậm theo — suýt thành kết luận *"bộ kiểm chậm 5 lần"* trong khi
nguyên nhân thật của sự cố ấy là một lỗi đệ quy.

**Mẫu PHẢI TỰ LOẠI TRỪ.** `pkill -f` khớp **toàn bộ dòng lệnh**, mà trong shell headless dòng lệnh
của chính `bash -c '...'` **chứa cái mẫu bạn vừa gõ** — nên `pkill` giết luôn shell đang chạy nó, và
mọi lệnh phía sau **không bao giờ chạy**. Phản chứng hai chiều, chạy được:

```
bash -c 'pkill -9 -f "mau_xyz"   ; echo CHAY'   -> khong in gi, shell tu chet
bash -c 'pkill -9 -f "[m]au_xyz" ; echo CHAY'   -> CHAY, rc=0
```

Dùng ngoặc vuông (`[b]an_sao_`) hoặc chọn PID con tường minh:

```bash
pkill -9 -f "[m]au_ten_tep_con" 2>/dev/null || true   # `|| true`: pkill tra 1 khi khong khop
ps -eo cmd | grep -c "[m]au_ten_tep_con"              # dem lai de CO SO, dung tin lenh giet
```

**Ghi cả cái sai, vì nguyên nhân sai trong tài liệu tệ hơn không ghi:** bản đầu của mục này đổ cho
*"`pkill` trả 1 khi không khớp nên cắt cả chuỗi"* và chỉ thêm `|| true`. Sai — `|| true` che mã thoát
nhưng **không cứu được một shell đã chết**. Người viết câu ấy vừa bị chính lỗi ấy vài lần trong cùng
phiên mà chẩn đoán nhầm; chỉ lộ khi cross-review dựng phản chứng ở trên. Cùng họ *"kết luận từ một
đường hỏng"*.

Việc dọn và trình tự phép đo theo chỉ thị điều phối của lượt; các lệnh trên chỉ minh họa
chọn tiến trình bằng mẫu và quan sát danh sách còn lại.

## Điều kiện dừng theo `review_class`

Trục `review_class`: xem protocol `§3.2`. Bảng này chỉ ánh xạ nó sang điều kiện dừng.

| `review_class` | điều kiện dừng |
|---|---|
| `routine` | **0 P1**; P2 còn lại thành **nợ CÓ TÊN** trong Issue của packet |
| `systemic` | **0 P1 + 0 P2** |
| `sensitive` | **`approve` tường minh** của reviewer khác nền |

Hàng `sensitive` **KHÔNG** được đọc thành *"hết P1 và P2"*: *"vắng mặt vì sạch"* và *"vắng mặt vì
chưa nhìn tới"* nhìn giống hệt nhau, và chỉ một `approve` phân biệt được hai thứ đó.

## `BẢNG LỚP`

Verdict **phải** mang mục này. **Mỗi finding thuộc ĐÚNG MỘT `lop_loi`** — finding không có lớp thì
verdict **thiếu**, không phải *"chưa phân loại"*.

| `lop_loi` | các slug thuộc lớp | **bản vá theo lớp** \| lý do vá lẻ |
|---|---|---|

Cột thứ ba là cột có răng: mỗi lớp khai **một thay đổi đóng cả lớp**, hoặc khai **lý do** phải vá lẻ.
Bỏ nó thì bảng tụt xuống thành bảng phân loại thuần.

| trường | đếm gì |
|---|---|
| `so_p1` · `so_p2` · `so_p3` | số **LỚP** ở mỗi hạng |
| `so_the_hien` | tổng số **THỂ HIỆN** |
| `findings_ids` | slug của **LỚP**, kebab-case |

Một LỚP = một **cơ chế** sinh cùng hình dạng lỗi; hạng của lớp là hạng **cao nhất** trong các thể
hiện. Slug là **khoá đếm** — giữ NGUYÊN qua các lượt cho cùng một lớp. Ngưỡng lặp lại: xem protocol
`§12`.

**`P1`/`P2`/`P3` KHÔNG có nguồn định nghĩa có thẩm quyền trong kho — nợ `DINH-NGHIA-PHAN-HANG-KHONG-CO-NGUON`.**
Đo được: `§8` chứa `P1` nhưng **không** `P2`/`P3`; `§12` **không** chứa cả ba. Bản trước của dòng này
trỏ *"định nghĩa P1/P2/P3: xem `§8`/`§12`"* và đó là một **con trỏ sai đích** — nó dẫn người đọc tới
nội dung assurance/budget thay cho định nghĩa severity. Dùng ba hạng theo cách chúng đang được dùng
trong `ops/reviews/**`, và **đừng** tự định nghĩa chúng ở đây: một adapter tự định nghĩa thứ doctrine
chưa định nghĩa là dựng một nguồn thứ hai sẽ trôi lệch.

**Reviewer phải GỌI TÊN khi một vòng đóng finding bằng cách CẮT TIÊU CHÍ** hoặc thu hẹp phạm vi, chứ
đừng ghi nhận nó là đã vá.

## Ví dụ trình bày `VERDICT.md`

Hợp đồng verdict và các mục bắt buộc: xem protocol §8/§13. Mẫu dưới chỉ minh họa Markdown;
không phải schema đủ để được chấp nhận.

```
verdict: <giá trị theo protocol §13>
reviewed_sha: <sha>

## ĐỐI CHIẾU LƯỢT TRƯỚC
- <slug>: <kết quả kiểm lại và bằng chứng>

## BẢNG SĂN
HƯỚNG 1: <ten>
  giả thuyết : <neu ... thi ... sai>
  lệnh       : <lenh da chay>
  output     : <output that, cat gon>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
HƯỚNG 2: ...

## BẢNG ĐO
| khẳng định | PR khai | đo được | khớp? |

### <slug>  [P1|P2|P3]  <tieu de mot dong>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ VÁ: có/không — <mo ta>
ĐÃ THỬ NGHIỆM: <lenh + ket qua, hoac KHÔNG ĐO ĐƯỢC + ly do>
ĐỘ TIN: cao/vừa/thấp
```

Cú pháp bảng Markdown trên có thể trình bày cả số khớp và số lệch.

**HINT.patch — kết quả thuật lại của #518 (12-09-2026).** Commit merge
`a8b0cf443ca8475e859ad8ae5e150fce135818d2` ghi bảy lượt review, sáu lượt có finding;
`patch -p0 --fuzz=0` trả rc=0 cho sáu HINT, tổng 13 hunk. Đây là số do phiên điều phối ghi,
không phải log sáu lần áp được đính ở mục này.

Bối cảnh prompt của đợt ấy được liệt kê dưới đây. Số 6/6 tự nó chưa xác định
nguyên nhân khác biệt với #250/#252 hay chứng minh từng điều kiện là cần:

- Định dạng của đợt #518 dùng `patch -p0` từ **gốc cây làm việc** (`cay-kho/`), với đường dẫn
  repo-relative không có tiền tố `a/`–`b/`;
- Để thử cùng chế độ áp `--fuzz=0`: `cd cay-kho && patch -p0 --fuzz=0 --dry-run < ../HINT.patch`.
  Có thể thêm `--verbose` để xem kết quả từng hunk.
- Quyền ghi, cách dùng patch-as-hint và hợp đồng finding: xem `docs/PROTOCOL_DA_PHIEN.md`
  §8/§13. Adapter không đặt thêm quy tắc nghiệm thu theo hunk hay theo lớp.

Để áp thử, dùng clone tạm với cùng lệnh `patch -p0 --fuzz=0` ở trên.
Về tệp phái sinh, xem protocol §9 và `CLAUDE.md`, mục "Quy ước deploy".
Cú pháp sinh manifest tạm nằm ở protocol §10.2 (`release-manifest --root … --out …`);
các cờ được mô tả bởi `--help` của lệnh `scripts/tl.py release-manifest`.

**Lane tệp và lane diff — phép đo #250/#252.** Trên bốn lượt #250 và một lượt #252,
định dạng diff hỏng **2/5 lượt** (đường dẫn hai chiều bất đối xứng, hoặc diff được lấy
sau khi cây đã đổi); tệp trong `cay/` dùng được cả năm lượt. Quyền chọn hiện vật và
hợp đồng patch-as-hint xem protocol §8/§13. Ví dụ sinh diff đối xứng cho layout `cay/`:

```bash
diff -u --label a/cay/<tep> --label b/cay/<tep> <ban goc> cay/<tep> > GOI_Y_VA.diff
patch --dry-run -p1 -d <cay tam chua BAN GOC> < GOI_Y_VA.diff   # kiểm layout cay/
```

## Cú pháp ghi verdict lên PR

```bash
gh pr review 56 --request-changes --body-file VERDICT.md
gh pr review 56 --approve         --body-file VERDICT.md
gh pr comment 56 --body-file VERDICT.md          # verdict blocked, hoặc phần bằng chứng dài
```

Các lệnh `gh` trên ghi review hoặc comment. Với MCP GitHub,
`pull_request_review_write` dùng `method: create` rồi `submit_pending`.
Nơi ghi, khai transport và điều kiện hoàn tất: xem protocol §8/§13.

## Ghi lại lượt review

`<reviewed_sha>` dưới đây là giá trị `reviewed_sha` trong `VERDICT.md` của lượt.
Lệnh dưới truyền trực tiếp OID ấy vào `record-review`.

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py record-review --packet 55 --provider codex \
    --verdict changes_requested \
    --reviewed-sha <reviewed_sha> \
    --finding-id url-alias      --finding-desc "mô tả tự do, KHÔNG tham gia phép đếm" \
    --finding-id van-tay-lach   --finding-desc "mỗi lỗi một slug ổn định"
```

`record-review` kiểm `--reviewed-sha` là OID 40 hex thường và bằng `reviewing_head_sha`
trong state; thiếu/sai/không khớp trả mã khác 0. Quy tắc exact head và xử lý head đổi
thuộc protocol §8/§13.

`--finding-id` nhận slug kebab-case làm khóa đếm; `--finding-desc` là mô tả tự do.
Nhánh kiểm finding chặn slug sai dạng; chỉ đòi có slug với verdict `changes_requested`.
`approve` và `blocked` có thể không có finding; lệnh không suy slug từ mô tả.
Cách giữ danh tính finding qua các lượt xem protocol §8/§12/§13.

`--help` cho ý nghĩa từng mã thoát.

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```
