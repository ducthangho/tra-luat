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

## Bước 0 — CÔNG CỤ, làm TRƯỚC khi đọc diff

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

Làm bước này ở ĐẦU phiên, không phải lúc sắp review: phát hiện thiếu `codex` sau khi
đã viết xong thay đổi thì không lùi lại được, và cám dỗ khi ấy là tự duyệt bài của
chính mình — thứ §8 không cho. (Khi cả Claude lẫn Codex hết quota, xem hướng dẫn
Antigravity Reviewer lane trong `AGENTS.md` theo cơ chế `same_provider_approved`.)

## Chọn model/effort theo độ phức tạp

| điểm | model | effort |
|---:|---|---|
| `<= 0` | `claude-opus-5` | `high` |
| `1–2` | `claude-opus-5` | `xhigh` |
| `3–4` | `claude-fable-5` | `xhigh` |
| `>= 5` | `claude-fable-5` | `max` |

Giữa các lượt của cùng packet, truyền bậc lượt trước làm `bac_truoc`: bánh cóc chỉ cho giữ hoặc tăng bậc, không bao giờ cho tụt khi diff còn lại nhỏ đi.

Ba bẫy CLI đã đo 27-08-2026, không phải giả định:

- `--effort khong-ton-tai` chỉ cảnh báo rồi lùi im lặng về mặc định; kết quả không ghi đã lùi.
- `--model claude-khong-ton-tai-9` không chạy review nào nhưng vẫn trả `rc=0`.
- Trong thư mục trống, 2 model hợp lệ cho `is_error=false` và mỗi lượt 1 khoá `modelUsage`; model rác cho `is_error=true`, `modelUsage={}` dù vẫn `subtype=success`. Trong sandbox có kho, cả 6/6 lượt đều thêm khoá phụ `claude-haiku-4-5-20251001`; model rác vẫn có 1 khoá phụ nhưng thiếu model yêu cầu.
  **`rc` và `subtype` cùng nói dối** — bằng chứng dương là `is_error is false` và model yêu cầu có mặt làm khoá hoặc `canonicalModel`; khoá thừa phải được báo ra, không được dùng để từ chối.

Chọn bậc **trước khi phóng**:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" .claude/dev/chon_reviewer.py --review-class sensitive \
  --duong-dan a.py,b.md --so-dong 120 --luot 1 --json
```

Phóng Claude reviewer headless, cấp đúng công cụ cần để review, và giữ JSON nguyên vẹn:

```bash
claude --model <id> --effort <bac> --output-format json --allowedTools Bash Read Write Edit Glob Grep --permission-mode acceptEdits --add-dir <sandbox> -p "$(cat PROMPT.md)" > reviewer.json
```

Đo 27-08-2026: `-p "$(cat TEP)"` và `-p ... < TEP` đều chạy. Không dùng `--dangerously-skip-permissions`: dưới root nó báo *"cannot be used with root/sudo privileges for security reasons"* rồi thoát `rc=1` sau `1.151s`; dùng `--allowedTools` cùng `--permission-mode` như trên để phiên headless gọi được công cụ.

Kiểm `modelUsage` **sau khi phóng**; lệnh gọi đúng vị từ fail-close dùng chung với CI:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -c 'import json,runpy,sys; m=runpy.run_path(".claude/dev/chon_reviewer.py"); print(m["kiem_ket_qua"](sys.argv[1],json.load(open(sys.argv[2],encoding="utf-8"))))' <id> reviewer.json
```

Mục này **KHÔNG thay** `docs/PROTOCOL_DA_PHIEN.md` §8; nó chỉ nói chọn bậc nào và cú pháp đo model thực sự đã chạy.

## Khi PAT là chính tài khoản tác giả PR

`pull_request_review_write` với `event=REQUEST_CHANGES` sẽ bị GitHub từ chối:
*"Can not request changes on your own pull request"* (đo trên PR #141). Đường còn
lại là **comment** (`add_issue_comment`). Verdict đăng kiểu ấy **không** mang trạng
thái review chính thức của GitHub — ghi rõ điều đó trong chính verdict, và nói rõ
nó chưa đủ cho mức assurance nào nếu §8 đòi reviewer có danh tính khác.

Trigger reviewer bot của kho: comment `@codex review` trên PR.

## Lấy diff của ĐÚNG head SHA

```bash
gh pr view 56 --json headRefOid,headRefName,state,statusCheckRollup
gh pr diff 56 > diff.patch
git diff --numstat <base_sha> <head_sha> > numstat.txt
```

Verdict neo `reviewed_sha`; head đổi thì làm lại, đừng review bản đã cũ.

## Dựng mirror trong sandbox — cú pháp nền, và ba chỗ đã gãy thật

Mirror là **clone rời, detached đúng exact head**, không phải worktree của cây đang làm việc:
worktree dùng chung `.git` nên reviewer chạm được nhánh executor, mà lease cấm đúng điều đó.

```bash
git clone -q <nguồn> "$RV"
git -C "$RV" remote set-url origin https://github.com/<chủ>/<kho>   # BẮT BUỘC — xem (1)
git -C "$RV" fetch -q origin <nhánh>
git -C "$RV" checkout -q --detach <exact-sha>
git -C "$RV" status --porcelain    # phải RỖNG trước khi phóng
```

1. **Clone từ ĐƯỜNG DẪN cục bộ để lại `origin` là đường dẫn, và `launcher.py` từ chối với `rc=11`**
   (`kho lech: mong doi github.com/<chủ>/<kho>, thuc te (khong co remote)`). Đúng doctrine *neo theo
   KHO, không theo đường dẫn*: từ một đường dẫn cục bộ không xác minh được danh tính kho. Clone cục
   bộ vẫn nhanh và vẫn nên dùng — chỉ phải `remote set-url` về dạng URL ngay sau đó.
2. **`git fetch origin <nhánh>` gãy nếu nhánh chỉ tồn tại dưới dạng remote-tracking ở nguồn cục bộ**
   (`couldn't find remote ref`). Vô hại khi commit đã có sẵn trong clone, nhưng đừng đọc nó thành
   "sandbox hỏng" — kiểm bằng `rev-parse HEAD`, không bằng mã thoát của `fetch`.
3. **Phiên headless NGOÀI kho không kế thừa `.claude/settings.json`** — nó in
   `Ignoring N permissions.allow entries: this workspace has not been trusted`. Đó là hành vi ĐÚNG
   và nên giữ: quyền của reviewer phải đến từ `--allowedTools` tường minh, không từ cây bị review.

Sau khi phóng, **kiểm reviewer đã tuân cấm**: `git -C "$RV" status --porcelain` rỗng VÀ
`git -C "$RV" log --oneline <head>..HEAD` rỗng, cộng cùng hai phép ấy trên kho THẬT.

## Chạy nền kia trong sandbox

```bash
codex exec -s workspace-write --skip-git-repo-check --cd <sandbox> - < PROMPT.md
```

Sandbox là thư mục ngoài kho, chứa sẵn: `SPEC.md` · `diff.patch` · `numstat.txt` · trích protocol ·
`EVIDENCE.md` (số đo gate — thiếu nó sẽ ra kết luận "KHÔNG ĐO ĐƯỢC") · bản sao cây sau sửa. Trong
prompt phải **cấm đọc ra ngoài thư mục đó**: một lượt chạy phạm vi mở đã quét ra ngoài kho, đọc nhầm
transcript phiên, 40 phút không ra kết luận. `workspace-write` để nó tự đột biến bản sao mà không
chạm kho thật.

### Mirror trong sandbox — khi §8 đòi năng lực đo

§8 quy định KHI NÀO phải cấp và VÌ SAO; đây chỉ là cú pháp dựng. Đặt mirror **BÊN TRONG** sandbox để
ràng buộc "cấm đọc ra ngoài" ở trên vẫn giữ nguyên:

```bash
R=<sandbox>
git clone --quiet --bare --no-local <kho> "$R/kho.git"
git -C "$R/kho.git" fetch --quiet <kho> '+refs/remotes/origin/*:refs/heads/*'   # nap DU ref
git clone --quiet "$R/kho.git" "$R/cay-kho"
git -C "$R/cay-kho" fetch --quiet origin '+refs/heads/*:refs/remotes/origin/*'
git -C "$R/cay-kho" config core.abbrev 7        # BAT BUOC — xem duoi
git -C "$R/cay-kho" checkout --quiet <reviewed_sha>
```

**Ghim `core.abbrev 7` không phải tuỳ chọn.** Clone sạch có kích thước khác cây gốc nên git tự chọn
độ viết tắt khác, và cổng của kho đọc giá trị ấy. Đo được ở lượt review đầu tiên dùng cơ chế này
(PR #252): không ghim ⇒ `git rev-parse --short` trả **8** ⇒ `doc-claims-check --strict` biến năm SHA
dài 8 ký tự từ *advisory* thành **cờ cứng** ⇒ `rc=2`, reviewer báo "cổng bắt buộc không xanh" trong
khi cây gốc `rc=0`. Ghim rồi ⇒ `rc=0`.

**Đối chiếu cổng TRƯỚC khi giao sandbox** — §8 đòi điều này, và nó rẻ:

Hai phép chạy phải ở **CÙNG MỘT COMMIT**, nếu không thì so hai thứ khác nhau: `<kho>` thường đang
đứng ở nhánh khác, và khi ấy một khác biệt THẬT về mã bị dán nhãn nhầm thành "lỗi sandbox". Dựng nền
bằng worktree read-only tại đúng `reviewed_sha`:

```bash
git -C <kho> worktree add --detach /tmp/nen-<reviewed_sha> <reviewed_sha>
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
cd /tmp/nen-<reviewed_sha> && "$PY" scripts/tl.py doc-claims-check --strict; echo "nen     rc=$?"
cd "$R/cay-kho"            && "$PY" scripts/tl.py doc-claims-check --strict; echo "sandbox rc=$?"
git -C <kho> worktree remove /tmp/nen-<reviewed_sha> --force
```

Hai mã thoát lệch ⇒ **lỗi sandbox** cho tới khi chứng minh ngược lại; đừng giao một mirror chưa đối
chiếu, vì mọi finding về cổng từ nó đều đáng ngờ.

Chiều ngược lại KHÔNG đúng: **hai mã thoát bằng nhau chưa chứng minh môi trường tương đương** — nó chỉ
nói cổng ấy không phân biệt được. Ghi trong `EVIDENCE.md` là đã đối chiếu cổng NÀO, đừng khái quát.

**Phép so hai nguồn phải chạy TRÊN KHO NGUỒN, TRƯỚC khi clone** — chạy nó trong sandbox là vô nghĩa ở
**cả hai** trạng thái của `origin`, nhưng vì hai lý do KHÁC NHAU, và reviewer phải ghi đúng lý do của
trạng thái mình đang đứng:
· **trước `set-url`** — `origin` trỏ vào chính mirror vừa tạo, nên `ls-remote` `rc=0` và **đếm head của
chính mirror** (đo được: 201 head), tức không có nguồn có thẩm quyền nào để so;
· **sau `set-url`** — `origin` là URL HTTPS thật nhưng sandbox không ra được mạng, nên `ls-remote`
`rc=128`, **0 dòng**. Nó KHÔNG "đếm mirror": nó không đếm gì cả.
Đừng chép câu của trạng thái kia — đó là chỗ bản trước đã tự mâu thuẫn. Mirror kế thừa đúng cái mù của kho nguồn, nên chỗ duy nhất chặn được
là trước bước clone (luật đầy đủ + lệnh `comm`: `CLAUDE.md`, mục `for-each-ref` đọc bộ đệm):

```bash
cd <kho>
git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort            > /tmp/mc
git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin \
    | grep -v '^HEAD$' | sort                                           > /tmp/cb
comm -23 /tmp/mc /tmp/cb        # CO tren may chu, THIEU cuc bo -> MU, fetch roi hay clone
```

**So bằng TẬP TÊN, không bằng `wc -l`** — hai tập cùng lực lượng vẫn có thể lệch (một nhánh cục bộ đã
bị xoá trên máy chủ cộng một nhánh mới chưa fetch), và `refs/remotes/origin/HEAD` tượng trưng làm số
đếm lệch sẵn 1 mà chẳng ai mù. Bản đầu của chính mục này đếm bằng `wc -l` **ngay dưới một câu trỏ về
doctrine cấm làm thế** — cross-review PR #261 bắt (P1).

Sau khi clone, thứ kiểm được trong sandbox chỉ là *mirror có nhận đủ cái kho nguồn đang có không*:

```bash
diff <(git -C <kho> for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin | grep -v '^HEAD$' | sort) \
     <(git -C "$R/cay-kho" for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin | grep -v '^HEAD$' | sort)
git -C "$R/cay-kho" rev-parse --is-shallow-repository        # phai la false
```

Và nói thẳng trong `EVIDENCE.md` rằng trạng thái GitHub **trực tiếp** là `KHÔNG ĐO ĐƯỢC` từ sandbox.

**LÝ DO phải viết cho đúng — bản trước của chính mục này viết SAI, và cross-review bắt** (P3
`evidence-origin-khong-phai-mirror-cuc-bo`, #309). Nó ghi *"`origin` trong đó là mirror cục bộ, không
phải máy chủ"* — nhưng bước dựng mirror ở trên **BẮT BUỘC** chạy `remote set-url origin
https://github.com/<chủ>/<kho>`. Làm đúng bước ấy thì `origin` là **URL HTTPS thật**, không phải mirror.
Hai mục trong CÙNG một tệp dặn hai điều loại trừ nhau, và **bốn verdict trong kho đã chép lại câu sai**.

Câu đúng, và nó đúng ở **cả hai trạng thái** — trước và sau khi `remote set-url` chạy: sandbox
**không có đường ra mạng**, nên `origin` trỏ đâu cũng không đọc được máy chủ. Trước `set-url` nó là
mirror cục bộ; sau `set-url` nó là URL HTTPS **không gọi tới được**. Cả hai đường đều dẫn tới
`KHÔNG ĐO ĐƯỢC`, nhưng vì **hai lý do khác nhau** — và reviewer phải ghi lý do ĐÚNG với trạng thái
mình đang đứng, chứ đừng chép câu có sẵn.

Hệ quả thực hành: phép so hai nguồn (`ls-remote` ↔ `for-each-ref`) chạy **TRONG** sandbox là vô nghĩa
dù `origin` trông như URL thật. Nói cho chật, vì bản trước viết "nó vẫn chỉ đếm được thứ mirror đã
nhận" và câu ấy SAI sau `set-url`: lúc đó `ls-remote` gọi HTTPS và **thất bại** (`rc=128`, 0 dòng) —
không đếm mirror, không đếm gì. Kết luận đúng cho cả hai trạng thái là **không đo được GitHub từ
sandbox**; chỗ duy nhất chặn được vẫn là **trước bước clone**, trên kho nguồn.

## Khung `VERDICT.md` bắt reviewer sinh ra

§8 quy định mục nào bắt buộc; đây là khung để dán vào `PROMPT.md`:

```
verdict: approve | changes_requested | blocked      <- BA gia tri canonical, xem §13
reviewed_sha: <sha>

## ĐỐI CHIẾU LƯỢT TRƯỚC        <- BO QUA o luot 1; BAT BUOC tu luot 2
- <slug luot truoc>: ĐÃ VÁ THẬT | VÁ HỜ | VÁ SINH LỖI MỚI | CHƯA VÁ — <bang chung TU DO>

## BẢNG ĐO                      <- moi con so da do, KE CA cai khop
| khẳng định | PR khai | đo được | khớp? |

### <slug>  [P1|P2|P3]  <tieu de mot dong>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ VÁ: có/không — <mo ta>
ĐÃ THỬ NGHIỆM: <lenh + ket qua, hoac KHÔNG ĐO ĐƯỢC + ly do>
ĐỘ TIN: cao/vừa/thấp
```

Bảng đo **chỉ liệt kê cái lệch là bảng giấu công** — đòi cả cái khớp.

**Gói vá: đòi CÂY ĐÃ SỬA, đừng đòi diff.** Đo trên bốn lượt của PR #250 và một lượt của #252: định
dạng diff hỏng **2/5 lượt** (đường dẫn hai chiều bất đối xứng ⇒ `patch` từ chối cả gói; hoặc reviewer
sửa thẳng vào cây nên diff đọc thành "đã áp"). Thứ dùng được cả năm lượt là **tệp trong `cay/`**. Nếu
vẫn muốn diff thì bắt sinh đối xứng và tự kiểm:

```bash
diff -u --label a/cay/<tep> --label b/cay/<tep> <ban goc> cay/<tep>
patch --dry-run -p1 -d <cay tam chua BAN GOC> < GOI_Y_VA.diff   # ghi ma thoat vao VERDICT.md
```

## GHI VERDICT LÊN PR — bắt buộc, đây là nơi verdict sống

```bash
gh pr review 56 --request-changes --body-file verdict.md
gh pr review 56 --approve         --body-file verdict.md
gh pr comment 56 --body-file verdict.md          # verdict blocked, hoặc phần bằng chứng dài
```

Không có bước này thì lượt review **không tồn tại** với ai ngoài phiên đang chạy — prompt review
vòng 6 của đợt F2 đã bốc hơi đúng kiểu đó. Nếu `gh` không dùng được, đường tương đương trên nền này
là MCP GitHub (`pull_request_review_write` với `method: create` rồi `submit_pending`); ghi rõ đã dùng
đường nào trong chính verdict.

## Ghi lại lượt review

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py record-review --packet 55 --provider codex \
    --verdict changes_requested \
    --reviewed-sha $(gh pr view 56 --json headRefOid -q .headRefOid) \
    --finding-id url-alias      --finding-desc "mô tả tự do, KHÔNG tham gia phép đếm" \
    --finding-id van-tay-lach   --finding-desc "mỗi lỗi một slug ổn định"
```

`--reviewed-sha` phải là **exact head bạn thực sự đã đọc**, và phải khớp head đã đưa ra review; lệch
thì lệnh thoát khác 0 và không ghi được bản duyệt. Head đổi giữa chừng ⇒ đọc lại, đừng duyệt bản cũ.

`--finding-id` là **khoá đếm**: slug kebab-case do người review đặt và giữ NGUYÊN qua các lượt cho
cùng một lỗi. Mô tả đổi thoải mái. Đặt slug mới cho một lỗi cũ là làm hỏng phép đếm — đó là lý do
khoá không còn là văn xuôi. Slug sai dạng hoặc thiếu thì lệnh thoát khác 0 và không tự đoán từ mô tả.

`--help` cho ý nghĩa từng mã thoát.

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```
