# `CHON-REVIEWER-DUONG-DAN` — hai nợ P3 của packet #351, và một cái là HỌ CŨ lần thứ tám

Packet #351 (`CHON-REVIEWER-THEO-DO-PHUC-TAP`, PR #354) land 2026-08-28 tại `6c2e097`. Cross-review
lượt 3 ra `approve` kèm **hai nợ P3**. Hồ sơ này mở packet cho đúng hai nợ ấy.

**Số dưới đây là số phiên điều phối TỰ ĐO trên master `d4b3045`.** Executor đo lại.

Nền: `.claude/dev/chon_reviewer_test.py` → `ca=25; đột biến=34`, `TỔNG: ĐẠT`, `rc=0`.

---

## Nợ 1 — `chot-thoat-repo-so-tien-to-chuoi`

`_chuan_hoa_duong` (`chon_reviewer.py:20`):

```python
if chuan.startswith(".."): raise KhongDoDuoc("đường dẫn %r thoát repo; ..." % duong)
```

Phép này hỏi **chuỗi bắt đầu bằng hai dấu chấm không**, trong khi câu cần hỏi là **đường dẫn có
thoát khỏi repo không**. Hai câu ấy khác nhau, và đo được là khác:

| đường dẫn | có thoát thật? | luật hiện tại |
|---|---|---|
| `..` | **có** | chặn ✓ |
| `../x` | **có** | chặn ✓ |
| `../../etc/passwd` | **có** | chặn ✓ |
| `ops/../../x` → `../x` | **có** | chặn ✓ |
| `..foo.py` | **không** — tên tệp hợp lệ | **chặn OAN** ✗ |
| `..a/b.py` | **không** | **chặn OAN** ✗ |
| `...x` | **không** | **chặn OAN** ✗ |
| `ops/..bar.md` | **không** | cho qua ✓ |

Hàng cuối là chỗ lộ ra bản chất: `ops/..bar.md` cũng chứa `..` nhưng **qua**, vì phép đo nhìn
**vị trí 0 của chuỗi**. Nó phân biệt **CÁCH VIẾT**, không phân biệt **CÓ THOÁT HAY KHÔNG** — đúng
họ mà kho này đã gặp **bảy lần** dưới tên *"danh sách cấm đội lốt allow-list"* /
*"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"*. Đây là **lần thứ tám**, ở một packet vừa mới
được cấp `approve`.

Và thông điệp lỗi **nói sai sự thật**: `..foo.py` không thoát đi đâu cả; người đọc bị bảo rằng nó
thoát repo.

Luật đúng — một đường dẫn thoát iff **thành phần đầu** của nó là `..`:

```python
if chuan == ".." or chuan.startswith("../"): raise ...
```

**Đo trước khi đề nghị, đúng doctrine "đếm tập hữu hạn TRƯỚC khi viết luật":**
778 đường dẫn THẬT trong kho (`git ls-files`) — luật cũ từ chối **0**, luật mới từ chối **0**,
**lệch 0**. Bốn ca thoát thật ở bảng trên: **cả bốn vẫn bị chặn**. Ba tên tệp hợp lệ: hết bị chặn
oan.

Nhánh này **không có ca đối chứng nào** — cả chiều chặn lẫn chiều cho qua.

## Nợ 2 — `vung-so-bang-doi-thanh-substring`

`_vung` (`chon_reviewer.py:43-54`) phân loại bằng bốn phép `==` chính xác cộng các `startswith`.
Đổi cả bốn `==` thành `in` (substring) — suite vẫn `25 ca`, `34 đột biến`, `TỔNG: ĐẠT`, `rc=0`.
Mutant **sống**.

Nó không vô hại. Sáu đường dẫn thử, **6/6 đổi phân loại**:

| đường dẫn | master | sau đột biến |
|---|---|---|
| `tmp/.claude/settings.json.bak` | `khong-biet` | `cong` |
| `x/RELEASE_MANIFEST.json` | `khong-biet` | `cong` |
| `docs/PROTOCOL_DA_PHIEN.md.orig` | `tai-lieu` | `giao-thuc` |
| `vendor/.gitignore` | `khong-biet` | `dev` |
| `a/b/.claude/settings.json` | `khong-biet` | `cong` |
| `ops/RELEASE_MANIFEST.json.tmp` | `dev` | `cong` |

`_vung` quyết **bậc review**. Một tệp `.bak` được xếp vào `cong` thì bậc review của cả packet lệch
— và không ca nào thấy.

---

## Việc

1. Sửa `_chuan_hoa_duong` sang phép đo **thành phần đầu**, và sửa thông điệp cho **đúng sự thật**.
2. Ca đối chứng **hai chiều**: bốn ca thoát thật phải ĐỎ; ba tên hợp lệ phải QUA. Kèm đột biến
   canh: quay về `startswith("..")` phải giết đúng ca `..foo.py`.
3. Nợ 2: ca khoá phép `==` — một đường dẫn có tên đích **là hậu tố/tiền tố** của một đường trong
   bảng phải ra `khong-biet`. Đột biến `==` → `in` phải chết.
4. Tự đo lại cả 778 và cả hai bảng trên. Nếu số của bạn khác, **số của bạn thắng** — nói ra.

## CÂU HỎI THẬT — hồ sơ CỐ Ý không đưa đáp án

Nợ 1 sửa được bằng một dòng. Nhưng đây là **lần thứ tám** cùng một họ, và bảy lần trước cũng đều
"sửa được bằng một dòng". Sửa dòng thứ tám không làm lần thứ chín bớt khả năng xảy ra.

`_vung` vẫn là một allow-list **viết trong mã**: bảng vùng nằm rải trong bốn câu `if`, không đếm
được, không đối chiếu được với gì. Câu hỏi:

`(A)` sửa hai dòng, thêm ca, đóng đúng phạm vi hai nợ — rẻ, và không đụng cấu trúc ·
`(B)` đưa bảng vùng ra **dữ liệu khai báo** (tệp riêng, đếm được, có ca đòi mọi mục trong bảng đều
được một ca chạm tới), để hồi quy hình-danh-sách-cấm **không thể vô hình** ·
`(C)` cách khác **bạn đo ra** là tốt hơn.

`(B)` đắt hơn nhiều và có thể là **quá tay cho hai nợ P3** — đó là một lý lẽ thật, không phải cái
cớ. **Không được chọn `(A)` chỉ vì nó rẻ, cũng không được chọn `(B)` chỉ vì nó nghe có nguyên tắc.**
Ai chọn phải viết ra căn cứ ĐO ĐƯỢC.

## write set

- `.claude/dev/chon_reviewer.py`
- `.claude/dev/chon_reviewer_test.py`

Chọn `(B)` thì cần thêm một đường cho tệp bảng — **revision của lease**, không ghi thêm lén.

## ĐO NGƯỜI GIỮ — đang BỊ CHẶN, cùng lý do với `DUYET-DANH-TINH-DO-PHU`

```
.claude/dev/chon_reviewer.py       rc=11   NGƯỜI_GIỮ 1: chon-reviewer-exec-1r8-codex-20260828
.claude/dev/chon_reviewer_test.py  rc=11   NGƯỜI_GIỮ 1: chon-reviewer-exec-1r8-codex-20260828
```

Người giữ là lease của **chính packet #351 đã land**. Kho không có đường thu hồi
(`AG-T0-01B-thu-hoi-lease-chua-co-duong`). **`rc=11` KHÔNG phải "cứ làm đi".**
