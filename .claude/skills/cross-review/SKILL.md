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
python .claude/dev/packet_loop.py doctrine-scan --root .
```

Dưới đây chỉ có cú pháp của nền.

## Bước 0 — CÔNG CỤ, làm TRƯỚC khi đọc diff

Skill này chạy được hay không phụ thuộc `codex` (hoặc provider reviewer được chỉ định),
mà container phiên **không có sẵn** (đo 17-08-2026: `codex` vắng, `gh` vắng — hook phiên
không chạy vì `CLAUDE_PROJECT_DIR` không được đặt khi kho gắn giữa phiên).

```bash
python .claude/dev/launcher.py doctor            # kiểm tra toàn bộ công cụ (CONG_CU)
npm install -g @openai/codex                     # nếu doctor báo `khong codex`
python .claude/dev/launcher.py chuan-bi          # CODEX_AUTH_JSON -> ~/.codex/auth.json
codex --version                                  # bằng chứng THẬT về phiên bản codex CLI
```

`doctor` in rõ bảng trạng thái `KHA DUNG` và các công cụ còn thiếu — đọc kỹ mục `KHA DUNG`
thay vì chỉ dựa vào mã thoát tiến trình.

Làm bước này ở ĐẦU phiên, không phải lúc sắp review: phát hiện thiếu `codex` sau khi
đã viết xong thay đổi thì không lùi lại được, và cám dỗ khi ấy là tự duyệt bài của
chính mình — thứ §8 không cho. (Khi cả Claude lẫn Codex hết quota, xem hướng dẫn
Antigravity Reviewer lane trong `AGENTS.md` theo cơ chế `same_provider_approved`.)

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

```bash
cd "$R/cay-kho" && python3 scripts/tl.py doc-claims-check --strict; echo "sandbox rc=$?"
cd <kho>        && python3 scripts/tl.py doc-claims-check --strict; echo "goc    rc=$?"
```

Hai mã thoát lệch ⇒ **lỗi sandbox** cho tới khi chứng minh ngược lại; đừng giao một mirror chưa đối
chiếu, vì mọi finding về cổng từ nó đều đáng ngờ.

Kiểm nhanh mirror có đủ ref không (cùng phép so hai nguồn của `CLAUDE.md`):

```bash
git -C "$R/cay-kho" rev-parse --is-shallow-repository        # phai la false
git -C "$R/cay-kho" ls-remote --heads origin | wc -l         # so nhanh
```

`ls-remote` ở đây hỏi mirror cục bộ, không hỏi GitHub — nên nói thẳng trong `EVIDENCE.md` rằng trạng
thái GitHub trực tiếp là `KHÔNG ĐO ĐƯỢC` từ sandbox, kẻo reviewer kết luận từ một ảnh chụp.

## Khung `VERDICT.md` bắt reviewer sinh ra

§8 quy định mục nào bắt buộc; đây là khung để dán vào `PROMPT.md`:

```
verdict: approved | changes_requested
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
python .claude/dev/packet_loop.py record-review --packet 55 --provider codex \
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
