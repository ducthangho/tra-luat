---
name: cross-review
description: Adapter review packet trên nền Claude Code. Provider, assurance và quyền của lượt lấy từ Packet và docs/PROTOCOL_DA_PHIEN.md; tệp này chỉ chứa cú pháp, công cụ và con trỏ.
argument-hint: "[so-issue-packet] [so-PR]"
---

# Adapter `cross-review` — Claude Code

**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §8 (mức review, quyền của người review, xử lý quota) và
§13 (trigger, hai trục, dạng verdict, nơi ghi verdict, định nghĩa hoàn tất) · §8.1–§8.3
(bootstrap, receipt, cache và lịch sử lớp) · §10.2.1–§10.2.3 (CI plan/provenance).
Packet áp `ADR-0060`: điều kiện severity, tìm theo lớp, phân loại Windows và cách gọi connector đọc ở ADR-0060 (M1–M3, M6).

Tệp này **không tóm tắt** những mục trên — đợt đầu của chính adapter này chép §13 rồi ghi sai nơi
đăng verdict. Chốt cơ học:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py doctrine-scan --root .
```

Dưới đây chỉ có cú pháp của nền.

`$SOURCE` là đường dẫn tuyệt đối checkout/code đã cấp; `$SCRATCH` là thư mục tuyệt đối
riêng của run ngoài checkout (§8.1–§8.2). Các ví dụ xuất/đọc hiện vật dùng cùng hai biến
này, kể cả khi cwd ở nơi khác. `$MODEL`, `$EFFORT`, `$PROMPT`, `$SANDBOX` lấy từ assignment.

## Kiểm tra công cụ

Đo tool trong phiên đang chạy; lần đo container ngày 17-08-2026 không quyết định capability
của phiên mới. Bootstrap và quyền cài/trust xem protocol §8.1; ví dụ chỉ probe:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/launcher.py doctor            # kiểm tra toàn bộ công cụ (CONG_CU)
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
"$PY" -B "$SOURCE/.claude/dev/chon_reviewer.py" --review-class sensitive \
  --effective-review-class sensitive \
  --duong-dan a.py,b.md --so-dong 120 --luot 2 \
  --bac-truoc claude-fable-5,max --json
```

Nếu lease có `effective_review_class`, đút **cả hai** trường bằng `--review-class` và `--effective-review-class`; bộ chọn tự lấy lớp cao hơn, không lấy `max` bằng tay.

Phóng Claude reviewer headless, cấp đúng công cụ cần để review, và giữ JSON nguyên vẹn:

```bash
claude --model "$MODEL" --effort "$EFFORT" --output-format json \
  --permission-mode default --add-dir "$SANDBOX" -p < "$PROMPT" > "$SCRATCH/reviewer.json"
```

Mẫu trên đưa prompt qua stdin; kích thước prompt không cộng vào một đối số argv và nội dung
không nằm trong dòng lệnh tiến trình. Phép đo 27-08-2026 từng chạy được cả dạng argv và stdin,
nhưng không xác định kích thước prompt tối đa. Dưới root, `--dangerously-skip-permissions`
báo *"cannot be used with root/sudo privileges for security reasons"* rồi thoát `rc=1`
sau `1.151s`; ví dụ dùng permission mode mặc định. Quyền/capability bootstrap theo §8.1.

Cú pháp đọc `modelUsage` từ JSON bằng vị từ dùng chung với CI:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -B -c 'import json,pathlib,runpy,sys; m=runpy.run_path(str(pathlib.Path(sys.argv[1])/".claude/dev/chon_reviewer.py")); print(m["kiem_ket_qua"](sys.argv[2],json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))))' "$SOURCE" "$MODEL" "$SCRATCH/reviewer.json"
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
4. **Model/effort/sandbox của lượt đọc từ `run.json` mà `launcher.py run` ghi, KHÔNG từ `stderr.log`.**
   Tên trường lấy theo `.claude/dev/launcher.py` (`_BoLocStderr.ghi_so`, `_LayMauSandbox.ghi_so`):

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -B -c 'import json,sys; r=json.load(open(sys.argv[1],encoding="utf-8")); [print(k,"=",json.dumps(r.get(k),ensure_ascii=False)) for k in ("model_phuc_vu","model_phuc_vu_trang_thai","model_phuc_vu_ly_do","effort_phuc_vu","effort_phuc_vu_trang_thai","effort_phuc_vu_ly_do","sandbox_quan_sat","sandbox_trang_thai","sandbox_ly_do")]' <run-root>/<short_id>/run.json
```

Chỉ `*_trang_thai` = `DO_DUOC` mới là đo được; trạng thái khác thì đọc `*_ly_do`
(`sandbox_trang_thai` còn có `KHONG_THAY_LENH`). Launcher tự đặt `RUST_LOG` để bắt khung
`response.created`/`response.completed` của máy chủ; `sandbox_quan_sat` lấy mẫu `/proc` (chỉ Linux);
không thấy tiến trình sandbox thì launcher đọc sự kiện `--json` trên stdout để phân biệt.
`codex-cli` 0.164 không in header `model:`/`reasoning effort:` vào `stderr.log` (lượt wp923 g2: 39 byte);
header, nếu có, chỉ là lời khai phụ để đối chiếu —
vắng header không có nghĩa là chưa đo được. Cờ `-m`/`-c model_reasoning_effort` là cấu hình yêu cầu.

`model_phuc_vu` là danh sách model theo từng khung response, không phải `modelUsage` của lane `claude`.
Hồ sơ `r368` ghi lời khai `xhigh` lệch header `none`; đó là đối chiếu hai nguồn khai,
không đo tác động của effort lên độ phủ review.

### `launcher.py run` có thể còn ghi `dang_chay` sau khi container chết

Theo thuật lại hai lần ở #518, container remote khởi động lại giữa lượt; lúc kiểm lại,
`run.json` vẫn ghi `trang_thai: dang_chay`, `ma_thoat: null` dù PID cũ không còn.
Các phép kiểm dưới đây thu thêm dấu hiệu; chưa chứng minh phải đủ cả ba mới chẩn đoán được:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhan CA BA ten
"$PY" -m json.tool <run>/run.json      # doc pid va khoa_danh_tinh; loi doc != tien trinh chet

# Nguon launcher tu SOURCE da cap, khong thay bang `ps -o lstart`.
# Tren Linux, ham doc TOAN ban ghi /proc/<pid>/stat, cat sau dau ')' cuoi cung;
# ten tien trinh co khoang trang, dau ')' hoac xuong dong van duoc xu ly cung cach.
# rc=1 / KHONG_DO_DUOC: ham khong doc duoc khoa; khong suy ra tien trinh da chet.
"$PY" -B -c 'import pathlib,runpy,sys; k=runpy.run_path(str(pathlib.Path(sys.argv[1])/".claude/dev/launcher.py"))["_khoa_danh_tinh"](int(sys.argv[2])); print(k or "KHONG_DO_DUOC"); sys.exit(0 if k else 1)' "$SOURCE" "$PID"
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

Cú pháp trigger bot qua comment là `@codex review`; quyền dispatch và provider của lượt ở
Packet/protocol §8/§13. Cú pháp này không chứng minh model/effort của bot.

## Lấy diff của ĐÚNG head SHA

Trong ví dụ, `<base_sha>` và `<reviewed_sha>` là hai OID đã chốt cho lượt.
`gh pr view` in metadata tại lúc gọi; `$BASE_SHA` và `$REVIEWED_SHA` chứa hai OID ấy.

```bash
gh pr view 56 --json headRefOid,headRefName,state,statusCheckRollup
git -C "$SOURCE" diff "$BASE_SHA" "$REVIEWED_SHA" > "$SCRATCH/diff.patch"
git -C "$SOURCE" diff --numstat "$BASE_SHA" "$REVIEWED_SHA" > "$SCRATCH/numstat.txt"
```

Hợp đồng `reviewed_sha` và xử lý khi head đổi: xem protocol §8/§13.

## Dựng mirror trong sandbox — cú pháp nền, và ba chỗ đã gãy thật

Ví dụ dưới dùng clone rời và checkout detached. Worktree dùng chung kho Git với cây nguồn;
quyền reviewer và yêu cầu cách ly xem protocol §8/§13.

```bash
# REMOTE, RV, BRANCH, REVIEWED_SHA lấy từ assignment; bước bootstrap (§8.1).
git -c core.longpaths=true clone --no-checkout "$REMOTE" "$RV"
git -C "$RV" remote get-url origin
git -C "$RV" config core.abbrev 7
git -C "$RV" config core.longpaths true
git -C "$RV" fetch -q origin "$BRANCH"
git -C "$RV" checkout -q --detach "$REVIEWED_SHA"
git -C "$RV" rev-parse HEAD 'HEAD^{tree}'
git -C "$RV" status --porcelain=v1 --untracked-files=all --ignored=matching
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
   Đọc lỗi trust thực và xử lý bootstrap theo §8.1, không tự chuyển sang acceptEdits.

Hai lệnh sau quan sát thay đổi Git còn lại và commit mới ở thời điểm kiểm:
`git -C "$RV" status --porcelain=v1 --untracked-files=all --ignored=matching`
và `git -C "$RV" log --oneline <head>..HEAD`;
có thể chạy cùng phép đọc trên kho nguồn. Output rỗng không chứng minh cả lượt không ghi:
thay đổi đã hoàn nguyên và lịch sử thao tác không nằm trong hai output ấy. Đo bytes của
ignored/untracked bằng snapshot hash riêng theo §8.2; status chỉ cho biết tên/trạng thái.

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
# R, SOURCE, REMOTE, REVIEWED_SHA do bootstrapper điền từ assignment (§8.1).
git clone --quiet --bare --no-local "$SOURCE" "$R/kho.git"
git -C "$R/kho.git" fetch --quiet "$SOURCE" '+refs/remotes/origin/*:refs/heads/*'
git clone --quiet "$R/kho.git" "$R/cay-kho"
git -C "$R/cay-kho" fetch --quiet origin '+refs/heads/*:refs/remotes/origin/*'
git -C "$R/cay-kho" remote set-url origin "$REMOTE"  # endpoint thật trong assignment (§8.1)
git -C "$R/cay-kho" config core.abbrev 7        # BAT BUOC — xem duoi
git -C "$R/cay-kho" checkout --quiet "$REVIEWED_SHA"
```

`core.abbrev` điều khiển độ dài SHA viết tắt mà `doc-claims-check` đọc.
Phép đo clone PR #252 và yêu cầu cấu hình nằm ở protocol §8; lệnh trên đặt giá trị `7`.

**Cú pháp đối chiếu một cổng trên hai cây tại `reviewed_sha`.**

Yêu cầu đối chiếu môi trường xem protocol §8. Ví dụ worktree nền dưới đây checkout
cùng commit với clone để giảm một nguồn khác biệt khi đọc kết quả:

```bash
# NEN là clone đối chứng đã bootstrap ngoài repo được review (§8.1).
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
cd "$NEN"                && "$PY" scripts/tl.py doc-claims-check --strict; echo "nen     rc=$?"
cd "$R/cay-kho"            && "$PY" scripts/tl.py doc-claims-check --strict; echo "sandbox rc=$?"
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
set -o pipefail
git -C "$SOURCE" ls-remote --heads origin | sed 's#.*refs/heads/##' | sort > "$SCRATCH/remote-head-names.txt"
git -C "$SOURCE" for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin \
    | grep -v '^HEAD$' | sort > "$SCRATCH/cached-head-names.txt"
comm -23 "$SCRATCH/remote-head-names.txt" "$SCRATCH/cached-head-names.txt"
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

## Ví dụ trình bày `VERDICT.md`

Hợp đồng verdict và các mục bắt buộc: xem protocol §8/§13. Mẫu dưới chỉ minh họa Markdown;
không phải schema đủ để được chấp nhận.

```
verdict: <giá trị theo protocol §13>
reviewed_sha: <sha>

## ĐỐI CHIẾU LƯỢT TRƯỚC
- <slug>: <kết quả kiểm lại và bằng chứng>

## BẢNG LỚP
| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| <slug> | <IDs> | <hạng> | <nguồn> | <phương án/lý do> | <command, kết quả, chưa đo> |

## BẢNG SĂN
HƯỚNG 1: <ten>
  giả thuyết : <neu ... thi ... sai>
  lệnh       : <lenh da chay>
  output     : <output that, cat gon>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
HƯỚNG 2: ...

## BẢNG ĐO
| khẳng định | PR khai | đo được | khớp? |

### <slug>  [P0|P1|P2|P3]  <tieu de mot dong>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ VÁ: có/không — <mo ta>
ĐÃ THỬ NGHIỆM: <lenh + ket qua, hoac KHÔNG ĐO ĐƯỢC + ly do>
ĐỘ TIN: cao/vừa/thấp
```

Cú pháp bảng Markdown trên có thể trình bày cả số khớp và số lệch.
Bảng lớp và quy tắc phân hạng theo protocol §8.3; tín hiệu hội tụ/checkpoint theo
§12; hợp đồng gợi ý cách vá và patch-as-hint theo §7/§8.

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
diff -u --label "a/cay/$FILE" --label "b/cay/$FILE" "$SOURCE/$FILE" "$SCRATCH/cay/$FILE" > "$SCRATCH/GOI_Y_VA.diff"
patch --dry-run -p1 -d "$SCRATCH/cay-tam" < "$SCRATCH/GOI_Y_VA.diff"   # kiểm layout cay/
```

## Cú pháp ghi verdict lên PR

```bash
gh pr review 56 --request-changes --body-file "$SCRATCH/VERDICT.md"
gh pr review 56 --approve         --body-file "$SCRATCH/VERDICT.md"
gh pr comment 56 --body-file "$SCRATCH/VERDICT.md"  # verdict blocked, hoặc phần bằng chứng dài
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

**`gh` có thể KHÔNG có trên nền đang chạy.** Đo 21→24-09-2026: container của một phiên review
không có `gh`, và hệ quả không dừng ở lệnh này — `ops/lease_publish.py kiem-github` trả
`rc=8: KHÔNG ĐO ĐƯỢC loại số hiệu: không gọi được gh api`. `rc=8` ấy **không phải một phán
quyết**, nó là một khoảng trống công cụ; đọc nó thành "cổng chặn" là khai rộng hơn phép đo.
Đường vòng chỉ cần token và HTTP; endpoint logs trả 302 sang host lưu trữ KHÁC nên phải theo
redirect (curl ≥ 7.58 tự bỏ `Authorization` khi đổi host — đừng thêm `--location-trusted`, kể cả
qua `~/.curlrc`: một dòng `location-trusted` ở đó đưa token theo sang host lưu trữ, nên `-q` đứng
ĐẦU TIÊN để curl bỏ qua tệp ấy).
Thiếu `-f` thì 401/403/404 vẫn `rc=0` và tệp chứa JSON lỗi thay cho log. CÓ `-f` thì lỗi
KHÔNG ghi tệp — tệp CÙNG TÊN còn nguyên log của lần tải TRƯỚC (của job khác, hoặc bản cắt ngang
`rc=18` của chính job ấy), đọc y hệt log thật; nên mỗi LƯỢT tải một thư mục MỚI (`mktemp -d`). Một tệp
cố định theo job chưa đủ: `$SCRATCH` là của cả run, hai lượt tải CÙNG job song song thì lượt sau xoá tệp
của lượt trước rồi ghi lại, và lượt xong trước in `rc=0` trỏ vào bản ĐANG GHI DỞ, cụt mất dòng cuối. Đừng
suy "không cần token" từ một `200` trong phiên web: proxy của phiên TỰ CHÈN credential GitHub
(đo 30-09-2026, không header: `/rate_limit` báo limit 15000, `/user` 200). Ẩn danh thật
(`--noproxy`, limit 60, egress là một DẢI IP dùng chung): 22/25 lượt `403` cạn hạn mức, 3/25 lượt
còn hạn mức ⇒ `404 Not Found` kèm `x-github-request-id`, cho đúng job mà bản có credential tải
được (200) — nên khối dưới đòi token.
`: "${GITHUB_PAT:?}"` chỉ dừng shell KHÔNG tương tác — dán vào terminal thì dòng sau
vẫn chạy — nên chốt nằm trong CÙNG một `if`. Token vào curl qua STDIN (`-H @-`, `printf` là
builtin): `-H "Authorization: …"` để nguyên token trong argv (`ps`, `/proc/<pid>/cmdline`) suốt lượt tải:

```bash
J="<id>"
if [ -n "${GITHUB_PAT:-}" ] && [ -n "${SCRATCH:-}" ] && mkdir -p "$SCRATCH" \
  && JD="$(mktemp -d "$SCRATCH/job-$J.XXXXXX")"; then
  OUT="$JD/job-$J.log"
  printf 'Authorization: Bearer %s\n' "$GITHUB_PAT" | curl -q -fsS -L -H @- \
    "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/$J/logs" -o "$OUT"; echo "rc=$? $OUT"
else echo "KHONG_DO_DUOC: GITHUB_PAT hoac SCRATCH rong, hoac khong tao duoc thu muc tai"; fi
```

**MÀU KHÔNG PHẢI NGUYÊN NHÂN.** `conclusion=failure` chỉ nói lượt chạy kết thúc khác 0. Nó không
nói cổng hỏng, và nó không nói hai lượt đỏ trên cùng một nhánh là cùng một bệnh. Phân loại TỪNG
lượt đỏ bằng log của chính nó **trước khi đếm**.

Đã trả giá đúng chỗ này: một lượt rà 40 lần chạy `ops-publish-lease.yml` (30 xanh, 10 đỏ —
danh sách ở #619) đọc 10 lượt đỏ thành "cổng chập chờn 25%". Mở log từng lượt thì **6/10 là
cổng từ chối ĐÚNG** (`CHAN [8]` thiếu bia mộ, hoặc `thay_the_cho` sai); **2/10** là `CHAN [8]`
"lease đã hết hạn" trên lease ĐÃ có bản chiếu của bot (#461 g2/r2, #579 g4) — đúng hình dạng
`rc=8` che `rc=9` mà `kiem_github` trên `master` đã chữa (cùng đầu vào, `master` trả `rc=9`
bỏ qua), tức lỗi CỔNG chứ không phải từ chối đúng; chỉ **2/10** là lệch A/B thật — 2/40 lượt,
khoảng 5%. THÔNG ĐIỆP cũng chưa phải nguyên nhân: "hết hạn" đúng về dữ kiện mà vẫn có thể là
cổng hỏng — kiểm cả trạng thái đã-đăng trước khi xếp loại. Chuỗi "đỏ rồi xanh trên
cùng nhánh" cũng bị đọc nhầm: nội dung giữa hai lượt KHÁC nhau (người ta thêm bia mộ rồi đẩy
lại), nên nó chứng minh cổng hoạt động chứ không chứng minh gì về tính tất định.

## `ai-dang-giu` — `rc=12` là lệnh TỪ CHỐI TRẢ LỜI, không phải câu trả lời

Lệnh quét mọi ref cục bộ (`refs/heads/*` lẫn `refs/remotes/*`). Một nhánh **cục bộ** tụt sau
upstream **trong cache** (`refs/remotes/*`) làm nó trả `rc=12 NHÁNH_CỤC_BỘ_TỤT_SAU` — nó đang
nói "tôi không đo được", không nói "không ai giữ". Đo 24-09-2026: cùng một đường cho `rc=12`,
rồi `rc=11 NGƯỜI_GIỮ 1` ngay sau khi cập nhật ref.

Lệnh KHÔNG so SHA với máy chủ: `ls-remote` chỉ để đối chiếu TÊN nhánh. Cache cũ mà nhánh cục
bộ bằng cache thì nó trả lời từ dữ liệu cũ — có thể `rc=0 NGƯỜI_GIỮ 0` trong khi máy chủ đã có
lease giữ đường ấy. Nên `rc=0` chỉ đọc thành "không ai giữ" khi bước 1 của khối dưới in
`CACHE_TUOI` (bước ấy chỉ ĐỌC, không ghi ref). `CACHE_TUOI` đòi tập (SHA, tên) HAI phía BẰNG
nhau: nhánh máy chủ đã xoá mà cache còn giữ (bootstrap chữa bằng `fetch --prune`) vẫn góp lease
và bia mộ vào câu trả lời — bia mộ trỏ tới lease chỉ còn trên nhánh ấy đổi `rc=12` thành
`rc=0 NGƯỜI_GIỮ 0`; `ls-remote` `rc=0` mà RỖNG không phải bằng chứng — máy chủ thật luôn có
nhánh mặc định. Tập ấy mới chỉ là `refs/remotes/origin`, còn lệnh đọc cả `refs/heads/*` và
`refs/remotes/<remote khác>/*`: nhánh cục bộ chưa đẩy, nhánh không upstream sót lại sau
`fetch --prune`, hay một remote thứ hai cũng góp lease và bia mộ y hệt. Nên bước 1 còn đòi mọi
ref ngoài origin trỏ đúng một đầu nhánh máy chủ (dòng `refs/…` trong `CACHE_CU`). Lệnh chỉ bỏ ref có TÊN
kết thúc bằng `/HEAD`; symref khác (vd `refs/heads/x` → `refs/tags/y`, hay `refs/remotes/origin/z`
→ một tag) nó đọc nội dung ĐÍCH, nên cả hai phép so tính symref theo SHA ĐÍCH và chỉ bỏ tên `…/HEAD`
mà lệnh cũng bỏ.

Lệnh còn so KHỚP ĐÚNG chuỗi (`_lease_cham_duong`: `strip()` rồi bỏ `planned:`, CHỈ ở phía lease), còn write
set là đường dẫn HOẶC prefix thư mục `…/` (protocol §5): hỏi `ops/reviews/x/a.md` KHÔNG thấy lease giữ
`ops/reviews/x/`, hỏi `planned:a.md` KHÔNG thấy lease giữ `a.md` — `CACHE_TUOI` rồi `rc=0 NGƯỜI_GIỮ 0`. Bước 2
bỏ `planned:`, hỏi đường ấy kèm `/` (tên thư mục gõ thiếu `/`), chính nó rồi mọi thư mục cha `…/`, và KHÔNG hỏi dạng
mà khớp đúng chuỗi không trả lời được: prefix `…/` hay thư mục CÓ trong checkout mà thiếu `/` cuối (lease giữ tệp
BÊN DƯỚI nó không hiện), `/…` `./` `//` `..` `\` `C:/…` hay `-…`. `rc=0` chỉ chứng minh một điều: không lease CÒN
HẠN, chưa bị thay thế nào có mục CHUỖI của write_set DẠNG DANH SÁCH (sau `strip()` và bỏ `planned:`) BẰNG ĐÚNG một
chuỗi đã hỏi, đọc bằng mã của `origin/master` (khối dưới) — mọi khác
biệt khác, ở phía hỏi LẪN phía lease, vẫn `rc=0` dù có người giữ. Đã đo, KHÔNG phải danh sách đủ: thư mục CHƯA có
trong checkout, gõ thiếu `/`, mà lease giữ tệp bên dưới nó; khác hoa/thường hay dạng Unicode (§5 case-fold và chuẩn
hoá NFC, lệnh thì không); ký tự trắng khác ở hai đầu — `\r`, NBSP, U+3000…: 26 ký tự `str.isspace()` ngoài dấu
cách, tab, xuống dòng (`read` chỉ bỏ dấu cách/tab, `strip()` bỏ cả chúng); và mục lease khác dạng chuẩn —
`docs\a.md`, `./docs/a.md`, `docs//a.md`, `planned: docs/a.md`, hay cả write_set là MỘT chuỗi đơn
`write_set: docs/a.md` (cổng đăng chỉ dùng `write_set` để xếp lớp, không từ chối dạng nào) — hỏi `docs/a.md` không
thấy.

Thông điệp lỗi nêu **nhánh và upstream thật**, không nhất thiết là `origin/<cùng tên>` — từ git 2.36:
trước đó (`worktree list -z` chưa có) nhánh TỤT_SAU dừng ở `KHÔNG_XÁC_ĐỊNH: git worktree list --porcelain -z
rc=129` (vẫn `rc=12`), không nêu nhánh, không in lệnh chữa — đo 2.30.2 · 2.34.1 · 2.35.0.
Lệnh chữa do `ai-dang-giu` in ra đã phân biệt nhánh rảnh với nhánh đang được worktree giữ:
worktree sạch nhận `git -C <worktree> merge --ff-only`; nhánh rảnh nhận `git branch -f` **KHÔNG
kèm `-C`** và không mang SHA kỳ vọng — tương đối với cwd của người CHẠY nó chứ không với
`--root`: chạy nguyên văn từ kho khác là ép nhánh cùng tên của KHO ĐÓ, có thể làm rơi commit
chưa đẩy. Bên bootstrap chạy nó dưới dạng `fetch .` neo đúng `<root>` (khối thứ hai dưới đây).
Nếu báo phân kỳ hoặc `KHÔNG_PHÁT_LỆNH_CHỮA`, không thay bằng một lệnh `branch -f` tự dựng.
Thời điểm cập nhật ref và checkout chỉ đọc xem protocol §8.1–§8.2; chuyển chẩn đoán cho
bên dựng bootstrap để cập nhật đúng upstream, rồi nhận lại snapshot. Ví dụ đọc lại từ
checkout đã cấp (kho đích được neo tường minh, kể cả khi cwd ở nơi khác; `GIT_DIR` và họ
biến ấy trong môi trường đè cả `git -C` lẫn `--root`, nên gỡ chúng TRƯỚC CẢ HAI bước):

```bash
PY="$(command -v python3 || command -v python || command -v py)"
unset GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR GIT_REPLACE_REF_BASE   # đè -C/--root, dời refs/replace: gỡ trước CẢ HAI bước
git -C "$SOURCE" ls-remote --get-url origin | sed -E 's#://[^/@]*@#://***@#'   # endpoint đang hỏi, che userinfo (§8.1)
# 1) CHỈ ĐỌC: tập (SHA, tên) máy chủ phải BẰNG tập cache, cả hai chiều (ai-dang-giu chỉ so TÊN, một chiều).
if MC="$(git -C "$SOURCE" ls-remote --heads origin)" && [ -n "$MC" ]; then
  SV="$(printf '%s\n' "$MC" | awk 'NF{sub("^refs/heads/","",$2); print $1" "$2}' | LC_ALL=C sort)"
  CB="$(git -C "$SOURCE" for-each-ref --format='%(objectname) %(refname:lstrip=3)' refs/remotes/origin \
    | awk 'NF && $2!="HEAD"' | LC_ALL=C sort)"
  LECH="$(LC_ALL=C comm -3 <(printf '%s\n' "$SV") <(printf '%s\n' "$CB"))"
  # ref NGOÀI origin mà ai-dang-giu vẫn đọc (refs/heads/*, remote khác): SHA phải là đầu một nhánh máy chủ.
  # Lọc theo TÊN */HEAD như lệnh, KHÔNG theo symref: symref khác nó đọc nội dung ĐÍCH (vd refs/tags/*).
  NGOAI="$(awk 'NR==FNR{if(NF)s[$1];next} NF && index($2,"refs/remotes/origin/")!=1 && substr($2,length($2)-4)!="/HEAD" && !($1 in s)' <(printf '%s\n' "$MC") \
    <(git -C "$SOURCE" for-each-ref --format='%(objectname) %(refname)' refs/heads refs/remotes))"
  # CACHE_TUOI đòi BẰNG CHỨNG DƯƠNG: SV khác rỗng và BẰNG CB. LECH rỗng thì chưa đủ — thiếu awk/sort/comm cũng cho rỗng.
  [ -n "$SV" ] && [ "$SV" = "$CB" ] && [ -z "$LECH$NGOAI" ] && echo "CACHE_TUOI" || printf 'CACHE_CU (sat le: chi may chu co; thut TAB: chi cache co; refs/: ref ngoai may chu):\n%s\n%s\n' "$LECH" "$NGOAI"
else echo "KHONG_DO_DUOC: ls-remote hong hoac rong"; fi
# 2) rc=0 chỉ là "không ai giữ" khi bước 1 in CACHE_TUOI; refs/replace cục bộ đổi được nội dung lease, info/grafts
#    (GIT_NO_REPLACE_OBJECTS KHÔNG tắt nó) biến PHÂN_KỲ thành TỤT_SAU: tắt cả hai (tệp /dev/null/grafts không thể có).
#    Git < 2.42: core.useReplaceRefs=true ở BẤT KỲ tầng config nào bật lại replace bất chấp biến ấy ⇒ đòi refs/replace RỖNG.
#    Đường dẫn được chứa $ ? * [ ` ; và dấu cách: để trần thì $/glob hỏi sang đường KHÁC (rc=0 dù đường thật đang bị
#    giữ), ; và dấu cách tách lệnh. Điền NGUYÊN VĂN vào heredoc nháy đơn; rỗng hay còn dạng <…> (quên điền) ⇒ không hỏi.
#    `read` KHÔNG kèm `IFS=`: bỏ khoảng trắng đầu/cuối như `ai-dang-giu` strip() mục write_set (giữ lại ⇒ rc=0 giả).
#    Lệnh khớp ĐÚNG chuỗi, write set là path/prefix: bỏ `planned:` như phía lease, hỏi `$D/` (tên thư mục gõ
#    thiếu `/`), chính nó rồi mọi thư mục cha `…/` (dừng ở rc khác 0 đầu tiên); prefix `…/`, thư mục CÓ trong
#    checkout hay dạng không chuẩn thì khớp đúng chuỗi không trả lời được ⇒ không hỏi.
#    Mã đọc lease lấy từ origin/master (bước 1 vừa so với máy chủ), KHÔNG từ checkout: checkout là cây ỨNG VIÊN
#    (§8.1) — ứng viên sửa ops/lease_publish.py, hay thêm ops/yaml.py (thư mục của script đứng đầu sys.path), thì
#    tự trả rc=0. Chép vào thư mục MỚI của riêng lượt này (`mktemp -d`) trong $SCRATCH: $SCRATCH là của cả run, nên một
#    đường cố định bị lượt chạy song song (hai lời gọi cùng lúc) ghi đè giữa chừng ⇒ Python chạy tệp RỖNG, rc=0 mà không
#    in NGƯỜI_GIỮ. SCRATCH rỗng hay không đọc được blob ⇒ không hỏi.
read -r D <<'TEN:'
<duong>
TEN:
D="${D#planned:}"
if RP="$(git -C "$SOURCE" for-each-ref refs/replace/)" && [ -z "$RP" ] && [ -n "${D##<*>}" ] && [ -n "${SCRATCH:-}" ] \
  && mkdir -p "$SCRATCH" && LP_DIR="$(mktemp -d "$SCRATCH/lp-origin-master.XXXXXX")" && LEASE_PY="$LP_DIR/lease_publish.py" \
  && git -C "$SOURCE" cat-file blob refs/remotes/origin/master:ops/lease_publish.py > "$LEASE_PY"; then
  case "$D" in
    -*|/*|[A-Za-z]:/*|./*|../*|.|..|*/|*//*|*/./*|*/../*|*/.|*/..|*\\*) echo "KHONG_DO_DUOC: prefix …/ hoac duong dan khong chuan" ;;
    *) if [ -d "$SOURCE/$D" ]; then echo "KHONG_DO_DUOC: thu muc co trong checkout ma thieu / cuoi, tuc prefix …/"; else
       M=0; P="$D/"
       while :; do
         GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null/grafts "$PY" -B "$LEASE_PY" ai-dang-giu "$P" --root "$SOURCE" || { M=$?; break; }
         case "$P" in "$D/") P="$D" ;; */*/) P="${P%/*/}/" ;; */?*) P="${P%/*}/" ;; *) break ;; esac
       done; echo "rc=$M"; fi ;;
  esac
  rm -rf -- "$LP_DIR"
else echo "KHONG_DO_DUOC: refs/replace khong rong/khong doc duoc, duong dan rong/chua dien, SCRATCH rong, hoac khong lay duoc lease_publish.py cua origin/master"; fi
```

Bên bootstrap chữa nhánh rảnh `<nhanh>` về `<upstream>` (cả hai lấy từ chẩn đoán) bằng `fetch .`
KHÔNG kèm `+`: git đòi fast-forward trên đầu nhánh HIỆN TẠI (commit cục bộ chưa có ở upstream ⇒
`rejected`) và từ chối nhánh đang được BẤT KỲ worktree nào checkout, kể cả worktree chính của
`<root>` — "rảnh" lúc chẩn đoán chưa chắc còn rảnh lúc chữa. Chốt từ chối ấy PHỤ THUỘC phiên bản
git (đo 30-09-2026): 2.30.2 và 2.34.1 (mặc định Ubuntu 22.04) trả `rc=0` và CẬP NHẬT nhánh đang
checkout ở worktree LIÊN KẾT (`status` ở đó hiện `D` đúng lease vừa về, y hệt `update-ref` dưới
đây), cả nhánh đang rebase/bisect ở đó hay ở worktree chính; 2.35.0, 2.36.0, 2.37.0, 2.37.2,
2.39.2, 2.43.0 từ chối (phép kiểm mọi worktree có từ 2.35.0). Nên khối dưới KHÔNG chạy với git < 2.35.
Phép so fast-forward đọc commit QUA `refs/replace` và `info/grafts` (đo: graft đầu upstream lên commit
chưa đẩy ⇒ `ai-dang-giu` báo TỤT_SAU thay vì PHÂN_KỲ, `fetch .` trả `rc=0`, commit rơi khỏi nhánh),
còn `GIT_DIR` đè `-C` (đo: trỏ kho khác ⇒ `rc=0`, nhánh của kho ĐÓ đổi, `<root>` đứng yên) — nên
khối tắt cả ba như hai bước trên. `GIT_NO_REPLACE_OBJECTS` chỉ thắng config từ git 2.42: trước đó
`core.useReplaceRefs=true` ở BẤT KỲ tầng nào (kho, global, `-c`) bật lại replace (đo 30-09-2026: bước 2
trên 2.30.2 · 2.34.1 · 2.35.0 · 2.41.0 in `CACHE_TUOI` rồi `rc=0 NGƯỜI_GIỮ 0` cho lease đang giữ; `fetch .`
trên 2.35.0 · 2.41.0 và `merge --ff-only` do chẩn đoán in ra trên 2.41.0 trả `rc=0`, commit rơi) — nên
bước 2 đòi `refs/replace` RỖNG và khối dưới thêm `-c core.useReplaceRefs=false`. Đừng thay bằng `update-ref <mới>
<cũ>`: nó so được giá trị cũ nhưng KHÔNG từ chối nhánh đang checkout — HEAD của worktree ấy nhảy,
index và tệp đứng yên, `status` hiện staged NGƯỢC đúng các commit upstream (lease vừa về hiện
thành `D`), và `commit` kế tiếp xoá lại chúng:

```bash
unset GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR   # đè -C như ở khối trên
# Tên nhánh HỢP LỆ được chứa $ ` ' " ; — điền TÊN THÔ (phần "<nhánh> -> <upstream>" của chẩn đoán) vào heredoc nháy đơn: không khai triển gì.
# Delimiter mang `:` — ký tự tên ref KHÔNG được chứa. `TEN` trần là tên nhánh HỢP LỆ: điền nó sẽ đóng heredoc sớm.
IFS= read -r N <<'TEN:'
<nhanh>
TEN:
IFS= read -r U <<'TEN:'
<upstream>
TEN:
case "$(git version)" in
  "git version 1."*|"git version 2."[0-9].*|"git version 2."[12][0-9].*|"git version 2.3"[0-4].*)
    echo "KHONG_CHAY: $(git version) < 2.35 khong tu choi nhanh dang checkout o worktree khac hay dang rebase/bisect" ;;
  *) # fetch TẠO nhánh đích khi chưa có (quên điền <nhanh> ⇒ rc=0, nhánh rác, nhánh thật đứng yên): đòi CẢ HAI ref có sẵn.
     if git -C "<root>" show-ref --verify --quiet -- "refs/heads/$N" "$U"; then
       GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null/grafts \
         git -C "<root>" -c core.useReplaceRefs=false fetch --no-write-fetch-head . "$U:refs/heads/$N"; echo "rc=$?"
     else echo "KHONG_CHAY: refs/heads/$N hoac $U khong co san trong <root> (quen dien ten?)"; fi ;;
esac
```

## Provenance CI

Theo protocol §10.2.2, `$RUN_NODE_ID` lấy từ raw REST response của đúng run. Query dưới
dùng với `gh api` trong Bash hoặc PowerShell; `query.graphql` đặt ngoài checkout:

```graphql
query($id: ID!) {
  node(id: $id) {
    ... on WorkflowRun {
      databaseId
      runAttempt
      event
      file { path repositoryFileUrl }
    }
  }
}
```

```bash
gh api graphql -F query=@"$SCRATCH/query.graphql" -f id="$RUN_NODE_ID" > "$SCRATCH/workflow-run.json"
```

Mẫu trên chạy trong phiên có GraphQL. Phiên Claude Code trên web bị 403 nên phải nhờ chủ kho chạy; lệnh đưa
cho chủ kho theo mục *"Lệnh `gh api graphql` đưa cho chủ kho chạy"* của `CLAUDE.md` (máy chủ kho là `cmd`, mẫu
trên vỡ ở đó). Đọc mục ấy từ `origin/master` ngay trước khi soạn lệnh — phiên mở từ trước có thể đang giữ bản cũ.

`WorkflowRun.file` nullable; cấu trúc tham chiếu ở [GitHub Actions GraphQL](https://docs.github.com/en/graphql/reference/actions).
Phân loại missing/errors và kiểm OID của URL theo §10.2.2. Khi đã xác minh repo/path/OID,
dùng `git -C "$SOURCE" cat-file blob "$DEFINITION_OID:$WORKFLOW_PATH"` lấy bytes và SHA-256 bằng Python;
không lấy blob từ checkout hiện tại. Fetch object thuộc bước bootstrap/cấp dữ liệu §8.1.
Jobs của đúng attempt: `gh api --paginate --slurp "repos/ducthangho/tra-luat/actions/runs/$RUN_ID/attempts/$ATTEMPT/jobs?per_page=100"`.
`--slurp` giữ các page thành mảng ngoài; không parse output nhiều page như một JSON object.

## Ruff và cache

Hai lệnh Python sau minh họa hai phép đo riêng của protocol §8.2, trỏ checkout đã cấp;
`$SCRATCH` nằm ngoài cây. Lệnh contract gọi consumer hiện hữu, không chạy toàn suite:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$SCRATCH/pycache"
"$PY" -B -c 'import pathlib,runpy,sys; m=runpy.run_path(str(pathlib.Path(sys.argv[1])/".claude/dev/ci_dang_ky_test.py")); errors,count=m["loi_ruff_ci"](); print("RUFF_CONTRACT",count,errors); sys.exit(bool(errors) or count == 0)' "$SOURCE"
"$PY" -m ruff check --no-cache --select F "$SOURCE/scripts/tl.py"
```

Rc của từng command được ghi riêng; điều kiện delta/bare lint và tiêu chí mutant riêng
ở protocol §8.2/§10.2.3. Snapshot: `git diff --binary`, `git diff --cached --binary`,
`git ls-files --others --exclude-standard`, `git ls-files --others --ignored --exclude-standard`;
ghép với SHA/tree và hash bytes của files theo §8.2, không chỉ dùng output status rỗng.

## Vận chuyển verdict và đọc lại

Protocol §7 quy định receipt; ví dụ Python body-file/raw JSON/exact readback trong
`.claude/skills/work-packet/SKILL.md`, mục “Body file và exact readback”, dùng được khi
đăng verdict dạng Issue comment theo assignment. `gh pr review --body-file` ở trên
không tự tạo delivery receipt; review đã đăng đọc qua endpoint PR reviews đúng object ID.
