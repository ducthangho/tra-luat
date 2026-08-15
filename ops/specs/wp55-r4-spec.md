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

base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
start_from_sha: 1a4525a20aa360476a6f59cb157c21097919c457
start_from_note: >-
  KHÔNG dựng lại từ base. Generation 9 đã đóng được sáu finding của lượt 9 và mười tám hình
  dạng của họ K/B/C — bỏ đi là mất công đo đã trả giá. Revision 4 xuất phát từ `1a4525a`,
  giữ mọi chốt cấu trúc, và chỉ thay ĐÚNG hợp đồng AC 19 cộng ba lỗi mã của lượt 10.

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

### AC 19 MỚI — miễn trừ phải được KHAI BÁO, không phải suy đoán

**Scanner không đoán ý nghĩa. Người viết adapter KHAI BÁO ý định, và scanner kiểm khai báo
ấy có đúng hình thức không.**

Một đoạn được miễn trừ khi và chỉ khi nó nằm trong một **khối chứng cứ** đúng khuôn:

```markdown
<!-- ac19:evidence nguồn="CLAUDE.md@2531366:82-83" lý-do="kể lại kết quả đo" -->
Đo được ở `v1.36.68` (PR #104): ba tên tấn công `rc=0` → `rc=4`, người có
thẩm quyền vẫn `rc=0`.
<!-- /ac19:evidence -->
```

Điều kiện, tất cả đều **cơ học**:

1. Mở bằng `<!-- ac19:evidence … -->`, đóng bằng `<!-- /ac19:evidence -->`, **cùng một tệp**.
2. Thuộc tính `nguồn` **bắt buộc**, dạng `<đường-dẫn>@<sha40 hoặc sha ngắn>:<dòng>-<dòng>`.
3. Khối **không được lồng nhau**, và không được để mở tới hết tệp (thiếu thẻ đóng ⇒ ĐỎ, mã
   thoát riêng, không im lặng bỏ qua).
4. Khối tối đa **N dòng** (đề xuất `N = 12`) — miễn trừ là ngoại lệ hẹp, không phải vùng tự do.
5. **Số khối tối đa mỗi tệp: `M`** (đề xuất `M = 3`). Vượt ⇒ ĐỎ. Adapter cần nhiều hơn thế
   thì nó đang chép doctrine chứ không phải kể một phép đo.
6. Ngoài khối chứng cứ, **KHÔNG có miễn trừ nào khác**. Mọi cụm cấm ở mọi hình dạng đều ĐỎ.

**Vì sao khuôn này đóng được, còn các xấp xỉ trước thì không:** scanner chỉ phải trả lời
"đoạn này có nằm giữa hai mốc đúng cú pháp không", một câu hỏi hữu hạn và kiểm được. Kẻ gian
muốn lọt thì phải **tự tay dán một khai báo có nguồn trỏ tới SHA và số dòng cụ thể** — việc
ấy để lại dấu vết kiểm chứng được, và có thể đối chiếu tự động ở bước sau.

**Chiều bắt oan vẫn phải đo, ngang hàng.** Văn xuôi bình thường không chứa cụm cấm phải luôn
`rc=0`; khối chứng cứ hợp lệ phải `rc=0`; và một khối chứng cứ **không chứa cụm cấm nào**
cũng phải `rc=0`, không bị phạt vì thừa.

### Chi phí di trú — ĐÃ ĐO, và kết quả có một cái bẫy

Đây là **thay đổi có phá vỡ**: chỗ nào đang dựa vào miễn trừ ngầm đều phải thêm khối khai
báo. Đo trên sáu tệp `write_set`, đếm số chỗ cụm cấm bị ngắt qua hai dòng:

| tệp | trên nhánh packet `1a4525a` | trên CÂY ĐÃ MERGE |
|---|---|---|
| `CLAUDE.md` | **0** | **1** — dòng 82–83 |
| ba `SKILL.md` | 0 | 0 |

**Cái bẫy nằm ở cột thứ hai.** Chỗ thật duy nhất cần miễn trừ KHÔNG có trên nhánh packet —
nó đến từ `CLAUDE.md` của **master**, thêm sau `base_sha`. Nhánh packet chỉ thêm 10 dòng vào
`CLAUDE.md` và không đụng đoạn ấy.

Hệ quả, và đây là chỗ AC 19 mới giao nhau với AC 20:

- chạy `doctrine-scan` **trên nhánh** sẽ XANH dù chưa di trú gì cả — vì chỗ cần miễn trừ
  không có mặt ở đó;
- chạy trên **cây đã merge** (thứ AC 20 bắt buộc) sẽ ĐỎ nếu chưa bọc khối chứng cứ.

Nên với revision 4, **AC 20 không còn là bước kiểm cuối mà là bước kiểm CHÍNH** của AC 19.
Executor nào chỉ đo trên nhánh sẽ tưởng đã xong trong khi chưa bắt đầu. Spec ghi thẳng điều
này để không ai phải phát hiện lại bằng một lượt review.

**Việc di trú phải làm ở đâu:** `CLAUDE.md` nằm trong `write_set`, nhưng đoạn cần bọc chỉ tồn
tại trên master. Executor phải chọn và KHAI RÕ một trong hai đường, kèm lý do đo được:

1. thêm khối chứng cứ vào `CLAUDE.md` của nhánh packet ở vị trí sao cho sau khi merge nó bọc
   đúng dòng 82–83 — rủi ro: phụ thuộc vị trí, merge lệch là hỏng;
2. đề nghị chủ kho sửa `CLAUDE.md` trên master **trước**, rồi packet rebase lên master mới —
   sạch hơn, nhưng đổi `base_sha` và cần chủ kho ra tay.

Chủ kho chốt đường nào trước khi cấp lease. Đây là quyết định §2, không phải của executor.

---

## Acceptance criteria

### Giữ nguyên AC 1–18, 20, 21 của revision 3

Không đổi câu chữ. AC 18 (danh sách ĐÓNG trước khi vá, mỗi lớp một phản chứng và một đột
biến giết đúng ca đó) đã chứng minh giá trị qua bốn lượt: mỗi lượt danh sách đóng đều tìm ra
nhiều hơn reviewer nêu (18 so với 2, 18 so với 4, 18 so với 9). Giữ nguyên.

### AC 19 — THAY TOÀN BỘ

Xem mục trên. Ba con số `N`, `M`, và dạng của `nguồn` **chủ kho chốt trước khi cấp lease** —
executor không tự chọn.

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

### AC 22 · Khối mã THỤT LỀ là khối mã

`doctrine-indented-code-block-bypass` (lượt 10). Khối thụt ≥4 dấu cách, đứng độc lập (có
dòng trống trước, không phải dòng nối của mục danh sách), là **khối mã CommonMark** và không
được hưởng miễn trừ nào.

Phản chứng bắt buộc cả hai chiều: khối thụt độc lập chứa cụm cấm ⇒ ĐỎ; dòng nối tiếp thụt
sâu của một mục danh sách, là văn xuôi thật ⇒ XANH. Ranh giới giữa hai ca này là chỗ dễ sai,
phải có ca cho cả hai.

### AC 23 · Thứ tự gỡ cấu trúc phải KHÔNG phá cấu trúc còn lại

`doctrine-comment-erases-fence-closer-bypass` (lượt 10). Generation 9 xoá comment HTML
**trước** khi dò hàng rào mã, nên một `<!--` mở bên trong khối mã nuốt luôn rào đóng thật:

```markdown
```html
<!--
```
-->
```

Chốt: mỗi tầng gỡ chỉ được nhìn thấy phần văn bản mà tầng trước **chưa** tuyên bố sở hữu.
Khối mã phải được xác định TRƯỚC, và comment nằm trong khối mã không phải comment.

Phản chứng: ca trên ⇒ ĐỎ; comment thật ngoài khối mã vẫn phải được gỡ ⇒ hành vi cũ giữ nguyên.

### AC 24 · Token markup chỉ tính khi nó THẬT SỰ là markup

`doctrine-html-table-token-context-bypass` (lượt 10). Chuỗi `<table` / `</table>` nằm trong
**thuộc tính có nháy** hoặc trong `<script>`/`<style>` không phải thẻ:

| ca | đòi |
|---|---|
| `<td data-x="</table>">` đóng bảng ngoài | ĐỎ — thẻ trong thuộc tính không đóng bảng |
| `<script>const s = "</table>";</script>` | ĐỎ — như trên |
| `<script>const s="<table>";</script>` rồi văn xuôi | XANH — không mở bảng, không bắt oan |

Ca thứ ba là chiều bắt oan và nó ĐANG ĐỎ trên `1a4525a` — phải xanh lại.

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
- **Đối chiếu tự động `nguồn` của khối chứng cứ** với SHA và số dòng nó trỏ tới. AC 19 mới
  chỉ đòi ĐÚNG CÚ PHÁP, chưa đòi xác minh nội dung. Việc ấy đáng làm nhưng là packet riêng:
  nó cần đọc lịch sử git từ trong scanner, một phụ thuộc mới hẳn.

## Việc chưa làm, phải nói ra

1. **Ba tham số của AC 19 chưa chốt**: `N` (số dòng tối đa mỗi khối), `M` (số khối tối đa
   mỗi tệp), và dạng chính xác của thuộc tính `nguồn`. Đề xuất `N=12`, `M=3`. Chủ kho chốt.
2. **Chi phí di trú ĐÃ đo** (xem bảng ở AC 19): 0 chỗ trên nhánh packet, **1 chỗ trên cây đã
   merge** — `CLAUDE.md` dòng 82–83, đến từ master. Cái CHƯA quyết là **di trú ở đâu**: sửa
   `CLAUDE.md` phía nhánh packet, hay sửa trên master rồi rebase. Chủ kho chốt.
3. **Chưa quyết khối chứng cứ có được nằm trong `CLAUDE.md` hay chỉ trong adapter.**
   `CLAUDE.md` nằm trong write_set nên sửa được, nhưng nó không phải adapter — cần chốt.
   Lưu ý: nếu chốt "chỉ adapter" thì đường di trú số 1 ở AC 19 KHÔNG dùng được, và bắt buộc
   phải đi đường số 2.
4. **Sổ attempts của revision 3 không khớp thực tế** và revision 4 không hồi tố sửa được.
   AC 26 chặn tái diễn, không chữa quá khứ.
