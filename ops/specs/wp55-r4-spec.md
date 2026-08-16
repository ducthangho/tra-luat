# Packet Spec — wp55 revision 4 (F3-03)

**TRẠNG THÁI: BẢN THẢO, CHỜ CHỦ KHO DUYỆT.** Chưa có lease nào neo vào tệp này. Băm của
nó chỉ có hiệu lực sau khi chủ kho chốt và một lease trỏ tới.

## Vì sao phải sang revision 4 — một câu

Bốn lượt cross-review liên tiếp (7, 8, 9, 10) đều tìm ra hình dạng mới của **cùng một**
lỗ, và lượt 10 kết luận nguyên nhân không nằm ở mã: *"tiếp tục thêm marker từ vựng sẽ chỉ
dời cửa lọt"*. AC 19 của revision 3 yêu cầu scanner **phân loại ngữ nghĩa mở** trên văn
xuôi — đó là một hợp đồng không cài đặt được, nên mọi bản vá đều là xấp xỉ và mọi xấp xỉ
đều có phản ví dụ. Revision 4 đổi **hợp đồng**, không vá thêm một lượt trên hợp đồng cũ.

## Con lắc — bằng chứng cho lập luận trên, đo được từng lượt

```
g4    thêm miễn trừ                     ⇒ quá rộng: heading trần lọt rc=0
g5    "chỉ tha khi ngắt dòng"           ⇒ vẫn quá rộng: heading/bullet/bảng/fence lọt
g6    "chỉ tha cho VĂN XUÔI"            ⇒ lọt fence lồng cấp, ô bảng HTML
g7+g8 thêm chốt fence + bảng HTML       ⇒ lọt closer sai, bảng lồng; VÀ bắt oan đuôi tệp
g9    luật CommonMark + dấu hiệu phép đo ⇒ lọt marker ngữ nghĩa, khối mã thụt lề,
                                            comment xoá rào đóng, token trong script
```

Năm lần vá, năm lần lượt sau tìm ra hình dạng mới, và **hai lần** bản vá tự đẻ ra lỗi mới ở
chiều ngược (g8 đầu độc đuôi tệp; g9 comment xoá rào đóng thật). Đó không phải chuỗi xui:
đó là dấu hiệu của một tiêu chí không đóng được.

## Spec

```yaml
schema_version: 1
packet_id: wp55
mission_issue: 54
mission_revision: 6
revision: 4
phase_key: F3-03
spec_path: ops/specs/wp55-r4-spec.md
spec_hash_basis: sha256 của chính tệp này, byte nguyên trạng, không chuẩn hoá gì thêm
supersedes_revision: 3
supersedes_spec_hash: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d

base_sha: 18da1da6a07ab2c86d716cef1d74ff2cd0e3218a
base_sha_note: >-
  ĐÃ LAND, ĐÃ ĐO. Bản viết lại `c47a439` được duyệt nhưng KHÔNG ff được — nó dựng trên
  `2531366` trong khi master tip đã là `d5b7bcc` (đi trước hai commit, PR #116). Rebase lên
  `d5b7bcc` cho `c44b2d4`, và bản rebase cũng đã qua cross-review: `approve`, không finding,
  hai diff giống nhau BYTE-FOR-BYTE kể cả context và hunk header `@@ -79,8 +79,8`.
  `c44b2d4` land qua PR #129 ngày 16-08 bằng MERGE COMMIT (theo nếp master, không ff), nên
  SHA neo là commit merge `18da1da`, KHÔNG phải `c44b2d4`. Điều kiện ff ghi ở bản nháp
  trước đó đã hết hiệu lực đúng như nó tự dự phòng.
  ĐÃ ĐO trên chính `18da1da`, có chứng đường hai chiều:
    scanner r3g5 (CÒN miễn trừ),  tip 18da1da  -> rc=0
    mô phỏng r4  (BỎ miễn trừ),   tip 18da1da  -> rc=0    <- hợp đồng mới, master sạch
    scanner r3g5 (CÒN miễn trừ),  d5b7bcc      -> rc=0
    mô phỏng r4  (BỎ miễn trừ),   d5b7bcc      -> rc=6 CLAUDE.md:82 'người có thẩm quyền'
  Hai dòng cuối là CHỨNG ĐƯỜNG: chúng chứng minh phép mô phỏng thật sự có tác dụng, nên
  `rc=0` ở dòng thứ hai là bằng chứng dương chứ không phải phép đo rỗng.
start_from_sha: b0e3e3b6a4c630ba0652b8fc939025d9c4031c67
start_from_note: >-
  KHÔNG dựng lại từ base. Generation 9 đã đóng được sáu finding của lượt 9 và mười tám hình
  dạng của họ K/B/C — bỏ đi là mất công đo đã trả giá. Revision 4 giữ mọi chốt cấu trúc, và
  chỉ thay ĐÚNG hợp đồng AC 19 cộng ba lỗi mã của lượt 10.
  SỬA 16-08 — bản thảo trước ghi `1a4525a` và ĐÓ LÀ MỘT LỖI CÓ HẠI. Đo được:
    git merge-base --is-ancestor 4085bbf2 1a4525a  ->  SAI (không phải tổ tiên)
    git merge-base --is-ancestor 4085bbf2 b0e3e3b6 ->  ĐÚNG
  `4085bbf2` là bản vá **P1 an ninh** do phiên điều phối đẩy sau lượt 10: `SKILL.md` nối
  `${VAR:+…}` với `${VAR:-…}` nên ở nhánh "đã đặt" nó bung ra CHÍNH GIÁ TRỊ của biến bí mật,
  trong một lệnh hướng dẫn agent chạy với refresh token thật. Xuất phát từ `1a4525a` sẽ
  **mở lại lỗ ấy trong im lặng** — `SKILL.md` nằm trong `write_set` nên nhánh mới sẽ ghi đè
  bản đã vá. Vì thế xuất phát từ `b0e3e3b6` = head nhánh packet = `1a4525a` + `4085bbf2` +
  merge master `d5b7bcc`.
  BÀI HỌC, cùng lớp với cái đã ghi ở `base_sha`: SHA neo cho phép đo và HEAD hiện thời của
  nhánh là hai thứ khác nhau. Lần trước neo vào SHA không còn là tip; lần này suýt neo vào
  SHA chưa bao giờ là tip. Cùng một câu chữa cả ba: **con số này có phải head thật không,
  đo lúc nào?**
must_merge_master_truoc_khi_do: >-
  BẮT BUỘC, không phải tuỳ chọn. `b0e3e3b6` merge master ở mức `d5b7bcc`, mà `CLAUDE.md` của
  `d5b7bcc` vẫn còn `người có thẩm quyền` ở dòng 82. Đo trên chính `b0e3e3b6`:
    r3g5 (còn miễn trừ)  ->  rc=0
    r4   (bỏ miễn trừ)   ->  rc=6  CLAUDE.md:82 'người có thẩm quyền'
  Tức dưới hợp đồng MỚI, nhánh packet ĐỎ vì một dòng KHÔNG PHẢI của nó. Executor phải merge
  master `18da1da` vào nhánh trước khi đo AC 19/AC 20, nếu không sẽ đuổi theo một finding
  mà bản vá đã nằm sẵn trên master.

objective: >-
  Đổi AC 19 từ một hợp đồng NGỮ NGHĨA MỞ ("văn xuôi kể lại kết quả đo") sang một hợp đồng
  CƠ HỌC HỮU HẠN mà scanner kiểm được bằng cấu trúc, rồi sửa mã theo hợp đồng mới. Kèm ba
  lỗi mã thuần của cross-review lượt 10 (khối mã thụt lề, comment xoá rào đóng, token bảng
  trong ngữ cảnh không phải markup), và sửa công thức AC 20 vốn thiếu điều kiện đo.

write_set:
  - type: exact
    path: .claude/skills/work-packet/SKILL.md
  - type: exact
    path: .claude/skills/cross-review/SKILL.md
  - type: exact
    path: .claude/skills/land-packets/SKILL.md
  - type: exact
    path: .claude/dev/packet_loop.py
  - type: exact
    path: .claude/dev/packet_loop_test.py
  - type: exact
    path: CLAUDE.md

depends_on: []
executor: claude
environment: local
risk: normal

attempts_limit: 3
attempts_used: 0
attempts_note: >-
  Trần đếm lại từ 0 cho revision 4 (§12). Revision 3 cạn 3/3 ở verdict lượt 10.
  GHI THẲNG MỘT KHUYẾT: sổ của revision 3 KHÔNG khớp thực tế — bốn commit chạy không lease
  (hai `g6`, cộng `3c4fbc2` và `4270210`) không vào sổ, nên `3/3` thấp hơn số lượt thật.
  Revision 4 thêm AC 26 để chuyện đó không lặp.

reviewer_provider: codex
reviewer_note: executor là claude ⇒ §8 bắt reviewer khác provider
```

---

## Thay đổi CỐT LÕI — AC 19 cũ bị THAY, không phải sửa

### AC 19 cũ (revision 3) — vì sao không cài được

> *một cụm doctrine bị ngắt qua xuống dòng trong **văn xuôi kể lại kết quả đo** KHÔNG được
> tính là chép doctrine*

Vế "văn xuôi kể lại kết quả đo" không có định nghĩa cơ học. Mọi xấp xỉ đã thử và phản ví dụ
đo được của từng cái:

| xấp xỉ | phản ví dụ | lượt bắt |
|---|---|---|
| "có ngữ cảnh doctrine" | heading trần lọt `rc=0` | 6 |
| "không nằm gọn trong một dòng" | `## Người có` / `thẩm quyền` lọt | 7 |
| "có chữ ở hai phía" | `x người có` / `thẩm quyền y` lọt | 9 |
| "có dấu hiệu phép đo" | `Một nửa (1/2) tài liệu chép…` lọt | 10 |

Mỗi xấp xỉ hẹp hơn cái trước, và mỗi cái vẫn có phản ví dụ. Reviewer lượt 10 nói thẳng
hướng đi: *"Revision 4 cần chốt một ngoại lệ cơ học hữu hạn… tiếp tục thêm marker từ vựng
sẽ chỉ dời cửa lọt."*

### AC 19 MỚI — KHÔNG CÒN MIỄN TRỪ NÀO

**Chủ kho chốt 2026-08-15, trực tiếp trong phiên: bỏ hẳn miễn trừ.**

> Cụm trong danh sách cấm KHÔNG được xuất hiện trong tệp bị quét, **ở bất kỳ hình dạng nào**
> — liền một dòng, ngắt qua dòng, trong khối mã, trong bảng, trong tag, sau chuẩn hoá.
> Không có ngoại lệ, không có khối khai báo, không có danh sách tha.
>
> Adapter cần kể lại một phép đo có chứa cụm cấm thì **viết lại câu** cho không còn cụm ấy.

#### Vì sao đường này, sau khi đã soạn xong đường kia

Bản thảo trước của chính spec này đề xuất **khối chứng cứ khai báo**
(`<!-- ac19:evidence nguồn=… -->`), có nguyên mẫu chạy được 9/9. Nó bị bỏ vì một lý do đo
được chứ không phải vì khó cài: **nó không còn người dùng nào.**

Trên toàn cây đã merge có ĐÚNG MỘT chỗ cần miễn trừ — `CLAUDE.md` dòng 82–83 của master.
Chỗ ấy đã được xử lý ở `c47a439` bằng cách **viết lại câu**, không dùng miễn trừ nào, và
cross-review duyệt (`approve`, không finding, xác nhận bản ghi phép đo vẫn đúng nghĩa).
Một cơ chế không có người dùng là một cơ chế **chưa ai kiểm**, và nó sẽ mục trong spec.

#### Cái này đóng được gì — ĐÃ ĐO, không phải suy luận

Mô phỏng bằng cách bỏ hẳn nhánh miễn trừ khỏi scanner `1a4525a`:

| phản ví dụ | lượt bắt | có miễn trừ | KHÔNG miễn trừ |
|---|---|---|---|
| `doctrine-measurement-marker-semantic-bypass` | 10 | `rc=0` | **`rc=6`** |
| `doctrine-indented-code-block-bypass` | 10 | `rc=0` | **`rc=6`** |
| `doctrine-comment-erases-fence-closer-bypass` | 10 | `rc=0` | **`rc=6`** |
| `doctrine-html-table-token-context-bypass` | 10 | `rc=0` | **`rc=6`** |
| wrapper hai ký tự | 9 | `rc=0` | **`rc=6`** |
| heading ngắt dòng | 7 | `rc=0` | **`rc=6`** |

**Cả sáu đóng cùng lúc, không cần vá gì thêm.** Con lắc sáu lần đánh quá đều là con lắc
của MIỄN TRỪ; bỏ miễn trừ thì không còn gì để đánh quá.

#### Mã trở thành chết — cũng đã đo

`_duoc_tha_vi_ngat_dong` (97 dòng), `_dong_khoi_ma` (53), `_dong_bang_html` (70),
`_go_dau_dong_tho` (21), cộng 8 hằng số/regex (`_DAU_HIEU_PHEP_DO`, `_RE_HANG_RAO`,
`_RE_BANG_HTML`, `_RE_MO_BANG`, `_RE_DONG_BANG`, `_RE_MA_INLINE`, `_RE_DAU_DONG_THO`,
`_CO_CHU`, `CUM_NGON_NGU_THUONG`).

**~241 dòng hàm biến mất, ≈16% tệp.** Executor PHẢI xoá chúng, không để lại mã chết —
mã chết là chỗ nấp cho lỗi và là gánh nặng cho mọi lượt review sau.

#### CÁI GIÁ — khai thẳng, đây là chiều bắt oan

Bỏ miễn trừ nghĩa là **văn xuôi thật kể lại phép đo, có cụm cấm ngắt dòng, nay sẽ ĐỎ**.
Đo trên hai ca chiều-tha đang có trong suite:

```
Đo được: ba tên tấn công rc=4, người có␤thẩm quyền vẫn rc=0.        rc=0 -> rc=6
- Kết quả đo cho thấy người có␤thẩm quyền vẫn qua cổng.             rc=0 -> rc=6
```

Cả hai phải **chuyển từ ma trận BẮT-OAN sang ma trận LỌT**, và người viết adapter phải
viết lại câu. Đó không phải hồi quy — đó là hợp đồng mới, khai rõ.

Ca giữ nguyên `rc=0`: trỏ về protocol thay vì chép; bảng Markdown thường; văn bản tiếng
Việt vô hại. Tức chỉ những chỗ **thật sự chứa cụm cấm** mới đỏ.

#### Điều kiện nghiệm thu của AC 19 mới

1. Không tệp nào trong `write_set` chứa cụm cấm ở bất kỳ hình dạng nào — đo cả trên nhánh
   LẪN trên cây đã merge (AC 20).
2. Mọi hàm và hằng số phục vụ miễn trừ bị **xoá**, không phải bị vô hiệu.
3. Suite giữ chiều bắt oan: văn bản không chứa cụm cấm phải `rc=0`, kể cả khi có bảng,
   khối mã, tag, comment, dấu đầu dòng.
4. Hai ca chiều-tha nêu trên chuyển sang ma trận LỌT, kèm lý do ghi tại chỗ.

### Di trú — ĐÃ XONG TRƯỚC revision 4

Chỗ duy nhất trên cây đã merge cần xử lý là `CLAUDE.md` dòng 82–83 của master, và nó đã
được xử lý bằng cách **viết lại câu**:

```
người có / thẩm quyền   →   tên thuộc / danh sách cho phép
```

| | |
|---|---|
| commit ĐƯỢC DUYỆT | `c47a439997e0191427d775636ebadbf3be7e1481`, dựng trên `2531366` |
| commit ĐÃ LAND | `c44b2d4c351cbe7f519e1b46aadf68d45e98af86` — cùng patch, rebase lên `d5b7bcc` |
| cách land | PR #129, **merge commit** `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a` (16-08) |
| phạm vi | 1 tệp, 2 dòng |
| lease review | `wp55-r4-review-viet-lai-codex-20260815` |
| verdict | **`approve`**, không finding, `land_recommendation: fast_forward` |

Reviewer kiểm cả câu hỏi khó nhất — *bản ghi phép đo còn thuật đúng thứ đã đo không* — bằng
cách quay về chính PR #104 (merge `e344e7c`, `VERSION=1.36.68`) và đo lại cổng. Kết luận:
`tên thuộc danh sách cho phép` mô tả đúng cơ chế và kết quả đã đo, không đánh tráo vai trò.

**Một bản trước đã bị bác, và chính nó dẫn tới quyết định bỏ miễn trừ.** Commit `9a5b05c`
bọc chỗ ấy bằng khối chứng cứ AC 19; verdict trả `do_not_land` với finding
`ac19-exemption-wider-than-necessary` — khối miễn 10 dòng để cứu 2 dòng.

**`base_sha` của revision 4 = `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a`** — commit merge của
PR #129, tức tip master sau khi bản viết lại land. KHÔNG phải `c44b2d4`: nó chỉ là commit
*bên trong* PR, và AC 20 đo trên **cây đã merge** nên phải neo vào tip, không neo vào nhánh.

Vì sao không phải `c47a439`: bản ấy dựng trên `2531366`, mà master tip là `d5b7bcc` — đi
trước hai commit (PR #116). **Fast-forward bất khả thi**, dù verdict khuyến nghị đúng chữ
`fast_forward`. Cả executor lẫn reviewer khi ấy đều dùng `2531366` — con số spec neo cho
phép đo AC 20 — mà không đo xem nó có còn là TIP không. Ghi ra để không lặp: **SHA neo cho
phép đo và SHA tip của nhánh là hai thứ khác nhau.**

Rebase lên `d5b7bcc` cho `c44b2d4`, và bản rebase cũng qua cross-review riêng
(`wp55-r4-review-rebase-codex-20260816`): `approve`, không finding, hai diff giống nhau
byte-for-byte kể cả context và hunk header. PR #116 không đụng `CLAUDE.md` nên không nuốt
mất thay đổi nào của họ.

**Đã land 16-08 — nhưng bằng merge commit, không phải fast-forward.** Master theo nếp merge
commit (`Merge pull request #116` ngay trước đó), nên PR #129 land cùng nếp và sinh
`18da1da`. Hệ quả duy nhất, và nó không nhỏ: **`base_sha` là `18da1da`, không phải
`c44b2d4`** — đúng cái bẫy mà chính đoạn trên vừa cảnh báo, chỉ khác một tầng. Lần trước là
*neo vào SHA không còn là tip*; lần này là *neo vào SHA chưa bao giờ là tip*. Cùng một câu
hỏi chữa được cả hai: **con số này có phải tip master không, đo lúc nào?**

## Acceptance criteria

### Giữ nguyên AC 1–18, 20, 21 của revision 3

Không đổi câu chữ. AC 18 (danh sách ĐÓNG trước khi vá, mỗi lớp một phản chứng và một đột
biến giết đúng ca đó) đã chứng minh giá trị qua bốn lượt: mỗi lượt danh sách đóng đều tìm ra
nhiều hơn reviewer nêu (18 so với 2, 18 so với 4, 18 so với 9). Giữ nguyên.

### AC 19 — THAY TOÀN BỘ: bỏ hẳn miễn trừ

Xem mục trên. Không còn tham số `N`/`M`/`nguồn` nào cần chốt — cơ chế khối chứng cứ đã bị
bỏ trước khi có người dùng đầu tiên.

### AC 20 — sửa công thức, không sửa yêu cầu

Yêu cầu giữ nguyên: gate phải đo trên cây ĐÃ MERGE. Nhưng công thức trong revision 3 **thiếu
một điều kiện** và đã được xác nhận từ lượt 6: cây dựng bằng `git archive` không tự chứa kho
git, nên bộ suite cần `GIT_DIR` trỏ về kho thật:

```bash
MASTER=<sha40 bất biến, KHÔNG dùng origin/master>
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary <base>..<head> | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

Đây chính là finding `ac20-archive-tree-suite-not-self-contained` đã hoãn từ verdict lượt 6.
Revision 4 đóng nó bằng cách sửa spec, đúng như `disposition: spec_revision_required`.

### AC 22–24 · RÚT — ba finding của lượt 10 tự đóng khi bỏ miễn trừ

Bản thảo trước có ba AC riêng cho ba lỗi mã của cross-review lượt 10:

| finding_id | AC cũ | vá cái gì |
|---|---|---|
| `doctrine-indented-code-block-bypass` | 22 | `_dong_khoi_ma` |
| `doctrine-comment-erases-fence-closer-bypass` | 23 | thứ tự gỡ trong `_dong_bang_html` |
| `doctrine-html-table-token-context-bypass` | 24 | `_RE_MO_BANG` / `_RE_DONG_BANG` |

**Cả ba chỉ tồn tại để vá cái máy dò cấu trúc phục vụ MIỄN TRỪ.** Bỏ miễn trừ thì máy ấy bị
xoá, và ba lỗi biến mất cùng nó — đã đo: cả ba trả `rc=6` trên bản không miễn trừ, không cần
vá gì thêm.

Giữ ba AC ấy sau khi đã bỏ miễn trừ là **đòi executor vá mã sắp xoá**. Nên chúng RÚT, và
điều kiện nghiệm thu tương ứng gộp vào AC 19 mục 2: *mọi hàm và hằng số phục vụ miễn trừ bị
XOÁ, không phải bị vô hiệu*.

**Ghi lại vì sao chúng từng có mặt:** nếu một revision sau này mở lại miễn trừ dưới bất kỳ
hình thức nào, ba lớp lỗi này quay lại ngay, và ba dòng bảng trên là danh sách kiểm sẵn.

### AC 25 · Suite phải TỰ IN số liệu của chính nó

`packet-suite-mutation-count-mismatch` (lượt 9). Executor khai `39 đột biến`, thật là `38`,
và suite không assert con số nó khai. Đã cài ở g9 và **giữ**: suite in khối `SỐ LIỆU (đếm
bằng máy)` ở cuối; mọi con số vào handoff/commit/lease phải chép từ đó.

Mở rộng ở revision 4: handoff §7 phải mang khối số liệu ấy **nguyên văn**, không gõ lại.

### AC 26 · Không commit nào lên nhánh packet mà không có lease đang sống

Revision 3 có **bốn** commit không lease, và hai trong số đó đẩy khi một lease reviewer đang
neo SHA cũ — làm hỏng lượt review 8, phải huỷ và cấp lại. Sổ vì thế không khớp thực tế.

Chốt, đo được:

```bash
git fetch origin 'refs/heads/ops/*:refs/remotes/origin/ops/*'
# 1. có lease EXECUTOR đang sống, neo đúng head xuất phát, chưa hết hạn?  Không ⇒ DỪNG.
# 2. có lease REVIEWER đang sống neo một SHA trên nhánh này?              Có   ⇒ DỪNG, hỏi.
```

Handoff §7 phải khai `lease_id` mà mỗi commit chạy dưới. Commit không khai được là commit
ngoài sổ, và reviewer được quyền tính đó là finding.

---

## Ba lỗi mã mang sang từ lượt 10 — đã tái lập, kèm lệnh

Executor revision 4 phải tái lập lại, đừng nhận theo lời kể. Ma trận đầy đủ nằm trong
`ops/reviews/wp55-r3-review-10-codex-verdict.md` trên nhánh `ops/wp55-r3-review-10-verdict`.

| finding_id | AC đóng nó | đo trên `1a4525a` |
|---|---|---|
| `doctrine-indented-code-block-bypass` | 22 | `rc=0`, đòi `6` |
| `doctrine-comment-erases-fence-closer-bypass` | 23 | `rc=0`, đòi `6` |
| `doctrine-html-table-token-context-bypass` | 24 | 2 ca `rc=0` đòi `6`; 1 ca `rc=6` đòi `0` |
| `doctrine-measurement-marker-semantic-bypass` | 19 mới | 3 ca `rc=0`, đòi `6` |

---

## Ngoài phạm vi — nêu rõ thay vì im lặng

- **`AGENTS.md`** — chuyển F3-08, chủ kho đã chốt hoãn (đẩy `file_count` 179→180 hoặc buộc
  sửa `release.py`, cả hai kéo manifest + golden vào write-set).
- **Wiring suite vào CI** — gộp vào #52.
- **`land-packets --apply`** — không thực thi trong packet này.
- **Cơ chế miễn trừ dưới MỌI hình thức.** Khối chứng cứ khai báo đã được soạn, dựng nguyên
  mẫu, đo 9/9, rồi BỎ vì không có người dùng. Nguyên mẫu giữ tại
  `ops/specs/wp55-r4-ac19-nguyen-mau.py` với nhãn ĐÃ BỎ — nó là điểm xuất phát nếu sau này
  có ca thật, KHÔNG phải việc của revision 4.

## Việc chưa làm, phải nói ra

1. ~~**`base_sha` chưa điền được.**~~ **XONG 16-08.** Land bằng merge commit qua PR #129, nên
   `base_sha = 18da1da` (tip master), không phải `c44b2d4`. Đã đo hai chiều trên chính tip
   ấy — xem `base_sha_note`. Cảnh báo còn lại: `18da1da` là tip **tại lúc soạn spec**; nếu
   master tiến thêm trước khi cấp lease thì phải đo lại AC 20 trên tip mới, vì AC 20 nói
   *cây đã merge* chứ không nói *cây tại base_sha*.
2. **Chưa đo lại toàn bộ suite dưới hợp đồng mới.** Đã đo sáu phản ví dụ và năm ca chiều-tha
   bằng mô phỏng (bỏ nhánh miễn trừ khỏi scanner `1a4525a`); **chưa** chạy trọn 173 ca. Hai
   ca chiều-tha chắc chắn đỏ và phải chuyển ma trận; có thể còn ca khác. Executor đo, đừng
   chép con số ở đây.
3. **Sổ attempts của revision 3 không khớp thực tế** — bốn commit chạy không lease. Revision
   4 không hồi tố sửa được; AC 26 chỉ chặn tái diễn.
4. **`CODEX_AUTH_JSON` đã bị thu hồi và cấp lại một lần trong phiên 15-08** vì executor in
   nó ra transcript. Hook KHÔNG tự nạp token mới: chốt "không ghi đè khi đã đăng nhập" của
   nó tin `codex login status`, mà lệnh ấy chỉ đọc TỆP chứ không hỏi máy chủ — nên nó báo
   "Logged in" với một token đã chết. Đây là lỗ thật trong hook, **ngoài `write_set`**, chưa
   ai vá. Ghi ở đây để không rơi.

## Những thứ ĐÃ chốt, đừng mở lại nếu không có căn cứ mới

- `N`, `M`, dạng thuộc tính `nguồn` — **không còn ý nghĩa**, cơ chế khối chứng cứ đã bỏ.
- Đường di trú — **đã thực hiện xong**, `c47a439` được duyệt.
- Bỏ hay giữ miễn trừ — **chủ kho chốt BỎ**, sau khi đo được rằng nó không có người dùng.
