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

Giữa các lượt của cùng packet, truyền bậc lượt trước bằng `--bac-truoc model,effort` (lượt 1 bỏ cờ): bánh cóc chỉ cho giữ hoặc tăng bậc, không bao giờ cho tụt khi diff còn lại nhỏ đi.

Ba bẫy CLI đã đo 27-08-2026, không phải giả định:

- `--effort khong-ton-tai` chỉ cảnh báo rồi lùi im lặng về mặc định; kết quả không ghi đã lùi.
- `--model claude-khong-ton-tai-9` không chạy review nào nhưng vẫn trả `rc=0`.
- Trong 9 lượt, `haiku-4-5` có 8/9, `fable-5` 6/9, `opus-5` 3/9 và `opus-4-8` 2/9; cả hai lượt `opus-4-8` là lượt tụt giữa chừng thật.
  **`rc` và `subtype` cùng nói dối**. Danh tính mỗi mục là `canonicalModel` nếu có, ngược lại là tên khoá; bỏ qua danh tính mang tiền tố phụ `claude-haiku-`, rồi đòi tập danh tính chính bằng đúng `{model yêu cầu}`. Model yêu cầu vắng và model lạ có mặt là hai nhánh lỗi riêng. Không được đòi model phụ có mặt.

Giới hạn đã biết: phép so tập chỉ hỏi model phụ **có mặt**, không hỏi nó **làm gì**; `{fable-5: 500 outputTokens, haiku: 90000}` vẫn ĐẠT. Chưa ai đo phân bố share của model phụ, nên không đặt ngưỡng token ở lượt này; phải đếm trước khi bàn ngưỡng.

Probe ngắn chỉ loại được ca *model hoàn toàn không gọi được*; nó không chứng nhận lượt dài sẽ giữ model. Đo 27-08: probe xanh 3/3 rồi lượt dài vẫn tụt hoàn toàn, nên luôn kiểm `modelUsage` **sau** lượt thật.

Chọn bậc **trước khi phóng**:

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

## Bộ lọc nền cắt lượt giữa chừng — hai chốt ĐÃ ĐO, cả hai bắt buộc

Đo trên 13 lượt của packet #513 (12-09-2026). Bộ lọc nội dung của nền (`flagged for possible
cybersecurity risk`) cắt **3/13 lượt** — và nó cắt đúng lúc reviewer chuyển sang **tự soạn** nội dung
tấn công. Chưa ai biết cách chặn nó. Nhưng hai chốt dưới đây làm hậu quả rẻ hẳn, và cả hai có số.

### 1. BẮT reviewer ghi `VERDICT.md` TĂNG DẦN

| lượt | bị cắt ở | giữ được verdict |
|---|---|---|
| 8 | 154 s | **KHÔNG** — mất trắng, phiên chính phải tự đọc log probe mới cứu được |
| 11 | 437 s | **KHÔNG** — 35 lệnh, 3 lỗi thật, không một dòng verdict |
| 12 | 299 s | **CÓ** — verdict còn nguyên một hướng kèm output thật |

Khác biệt duy nhất giữa lượt 12 và hai lượt kia là ba câu trong prompt:

```
1. NGAY BÂY GIỜ, trước khi đo gì, tạo VERDICT.md với 4 dòng đầu (dùng changes_requested
   và các số 0 làm chỗ giữ).
2. Sau MỖI hướng, ghi ngay khối của hướng đó vào cuối VERDICT.md (`>>` là đủ).
3. CUỐI CÙNG mới sửa 4 dòng đầu cho khớp và thêm phần finding.
```

Đây là chốt chống **mất bằng chứng**, KHÔNG phải chốt chặn bộ lọc — đừng khai nhầm.

### 2. Phân công: reviewer CHẠY và ĐỘT BIẾN, không TỰ SOẠN

Cho phép: chạy phản chứng có sẵn · **đột biến mã CÓ SẴN trong cây** rồi chạy lại · viết probe gọi
thẳng hàm sản phẩm với đầu vào bất thường · đọc mã.
Cấm: soạn payload tấn công/giả mạo. Hướng nào cần thứ đó thì **mô tả BẰNG LỜI kèm công thức tái
hiện**, phiên điều phối viết probe và đo hộ.

Kênh "nêu bằng lời" KHÔNG phải giải pháp hạng hai: **toàn bộ giá trị của lượt 8 đi qua đúng nó** —
nó nêu hai hướng trước khi chết, một hướng hoá ra là lỗi sản phẩm thật.

## BẮT reviewer nộp BẢNG SĂN — nếu không, `approve` chỉ nghĩa là "chưa tìm"

Đo được, cùng packet, hai lượt liền:

| lượt | prompt nói gì | kết quả |
|---|---|---|
| 9 | *"nếu không tìm ra gì thì liệt kê hướng đã thử"* | `approve`, và 4 "hướng đã thử" hoá ra **cả 4 đều là việc bắt buộc ở phần khác của prompt** — không hướng nào độc lập |
| 10 | **bảng SĂN ≥ 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT** | **8 hướng**, **2 lỗi sản phẩm thật** |

Câu *"nếu không thấy thì khai"* cho phép **"chưa tìm"** đi qua như **"đã tìm, không thấy"**. Khối bắt
buộc:

```
HƯỚNG <n>: <tên>
  giả thuyết : <nếu ... thì ... sai>
  lệnh       : <lệnh đã chạy>
  output     : <output thật, cắt gọn>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
```

Kèm ba điều kiện, thiếu cái nào cũng làm bảng mất răng:
- **KHÔNG tính** vào N hướng: đo nền; trỏ vào ca test đã có sẵn; đột biến chỉ nhằm kiểm bản vá lượt trước.
- **Nộp danh sách hướng các lượt TRƯỚC đã đi** và cấm lặp y nguyên — hoặc hướng mới, hoặc biến thể
  chưa ai chạm và phải nói rõ biến thể là gì.
- `approve` mà **thiếu bảng** thì bị coi là `KHÔNG ĐO ĐƯỢC`, bất kể kết luận ghi gì.

Ở lượt XÁC NHẬN, nói thẳng với reviewer rằng **kết luận SẠCH có giá ngang một phát hiện** — kèm câu
*"đừng bới một finding tầng META cho có"* và *"đừng nương tay ở tầng sản phẩm chỉ vì đây là lượt
cuối"*. Không có câu ấy thì một lượt xác nhận dễ trả về finding trang trí.

## Dọn tiến trình mồ côi TRƯỚC mỗi phép đo

Bộ test nào phóng tiến trình con mà bị giết giữa chừng sẽ **bỏ rơi** con của nó. Đo 12-09-2026: hai
lượt bị giết để lại **526 tiến trình `ban_sao_*` còn sống**, RAM `14,5/16 GB`, và mọi phép đo sau đó
chậm theo — suýt thành kết luận *"bộ kiểm chậm 5 lần"* trong khi nguyên nhân thật là một lỗi đệ quy.

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

Dọn xong mới đo, và đo lại **nền** trước khi nghi bản vá của mình.

## Khung `VERDICT.md` bắt reviewer sinh ra

§8 quy định mục nào bắt buộc; đây là khung để dán vào `PROMPT.md`:

```
verdict: approve | changes_requested | blocked      <- BA gia tri canonical, xem §13
reviewed_sha: <sha>

## ĐỐI CHIẾU LƯỢT TRƯỚC        <- BO QUA o luot 1; BAT BUOC tu luot 2
- <slug luot truoc>: ĐÃ VÁ THẬT | VÁ HỜ | VÁ SINH LỖI MỚI | CHƯA VÁ — <bang chung TU DO>

## BẢNG SĂN                     <- BAT BUOC; thieu khoi nay thi `approve` = KHÔNG ĐO ĐƯỢC
HƯỚNG 1: <ten>
  giả thuyết : <neu ... thi ... sai>
  lệnh       : <lenh da chay>
  output     : <output that, cat gon>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
HƯỚNG 2: ...                    <- lap toi DU N huong DOC LAP (N do prompt dat, >= 6)

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
