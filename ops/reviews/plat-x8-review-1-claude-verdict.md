# VERDICT — cross-review lượt 1 của `PLAT-X8` (#225 / PR #248), reviewer `claude`

`reviewed_sha` **`67a7fbe029d3fc9904322eda2452ce8deb5096c3`** · executor `codex` · verdict **`changes_requested`**

## Bản chiếu, không phải nguồn

Bản đăng trên PR #248 là [comment `5381470367`](https://github.com/ducthangho/tra-luat/pull/248#issuecomment-5381470367).
Nó là **issue comment**, KHÔNG mang trạng thái review chính thức của GitHub: PAT là chính tài khoản
tác giả PR nên `REQUEST_CHANGES` bị từ chối. Nếu §8 đòi reviewer có danh tính GitHub khác cho mức
assurance đang nhắm thì chừng này **chưa đủ**.

## HAI CHỖ HỞ CỦA CHÍNH LƯỢT REVIEW NÀY — đọc trước verdict

**1. Reviewer là người soạn đặc tả.** Tôi viết đặc tả bản 5, prompt r3 và lease, rồi review. §2 chỉ
cấm **Executor** tự review, executor là `codex`, nên vai hợp lệ và đây là đường cross-provider duy
nhất. Nhưng verdict này **KHÔNG bảo chứng tính đúng của đặc tả** — tôi mù đúng chỗ đó.

Và nó vừa được ĐO chứ không phải nói khiêm tốn: **hai P1 dưới đây do connector `codex` tìm ra, tôi
đọc qua cả hai.** Tôi đọc cấu trúc mã rồi kết luận *"fail-closed ở mọi nhánh"*, có chạy một phản
chứng — đúng cái phản chứng tôi nghĩ ra. Không nghĩ ra traversal, không nghĩ ra `schema_version`
hỏng. Cùng họ *"nghĩ ra được phép thử mà không chạy nó"*, tệ hơn một bậc: không nghĩ ra thì không
có gì để chạy.

**2. KHÔNG CÓ LEASE REVIEWER.** Lượt này chạy dưới lease **executor** `plat-x8-exec-2r3-codex-20260822`
(nó khai `reviewer: claude`), chứ không có lease `role: reviewer` riêng. Tiền lệ kho có lease reviewer
(`plat-m4-review-3r4-claude-20260821`). Đây là **thiếu sót của phiên điều phối**, khai ra thay vì cấp
lease lùi ngày — cấp sau khi việc đã xong là backdate, và packet này sinh ra chính để chống loại vết giả ấy.

## P1-1 · `duong-di-xuyen-thu-muc-ha-lop` — HẠ LỚP, tái hiện được

```
ops/lease_publish.py                        -> sensitive
docs/adr/../../ops/lease_publish.py         -> systemic     <-- HẠ LỚP
planned:docs/adr/../../ops/lease_publish.py -> systemic     <-- HẠ LỚP
```

**Chỉnh lại mô tả của finding cho khớp phép đo** — finding nêu *"accepts `..`, absolute paths, and
backslashes"*; đo thật thì ba dạng kia ĐÃ fail-closed vì khớp chính xác trượt:

```
/home/user/tra-luat/ops/lease_publish.py    -> sensitive
ops\lease_publish.py                        -> sensitive
./ops/lease_publish.py                      -> sensitive
```

Lỗ **hẹp hơn** mô tả nhưng có thật: chỉ traversal xuyên một **prefix thư mục có trong `_BANG_LOP`**,
và hiện chỉ `docs/adr/` → `systemic` là đích hạ lớp được. Mức hạ `sensitive` → `systemic`.
Nói chính xác vì bảng sẽ được nới: **mỗi mục prefix không-`sensitive` thêm vào bảng là thêm một cửa
traversal.** Chuẩn hoá phải làm TRƯỚC khi tra bảng, không vá từng mục.

## P1-2 · `schema-version-hong-fail-open` — FAIL-OPEN, rộng hơn mô tả

`write_set = ['.claude/dev/launcher.py']` (sensitive), khai `effective_review_class: routine`:

```
schema_version=2        -> CHAN rc=10      đúng
schema_version='2'      -> CHAN rc=10      đúng
schema_version=1        -> QUA             đúng (legacy CÓ CHỦ Ý)
schema_version='v2'     -> QUA (khong chan)   <-- FAIL-OPEN
schema_version='2.0'    -> QUA (khong chan)   <-- FAIL-OPEN
schema_version='abc'    -> QUA (khong chan)   <-- FAIL-OPEN
schema_version=None     -> QUA (khong chan)   <-- FAIL-OPEN
schema_version=[]       -> QUA (khong chan)   <-- FAIL-OPEN
schema_version={'a':1}  -> QUA (khong chan)   <-- FAIL-OPEN
```

Fail-OPEN trong một cổng mà toàn bộ lý do tồn tại là fail-closed. Khớp nguyên văn doctrine kho:
*"Từ chối mà vẫn để đường nguy hiểm chạy tiếp là FAIL-OPEN, không phải thận trọng."*
Nặng hơn: giá trị **hỏng** không phân biệt được với trường **vắng mặt** — đúng lỗi ba trạng thái
(`có` · `không` · **`không đọc được`**), và trạng thái thứ ba đang lặng lẽ thành `không`.

## P2 · `commit-message-mot-dong`

Thông điệp commit một dòng. Nếp kho đòi **LÝ DO + bằng chứng đo được**. Reviewer không tự sửa —
§2 cấm Reviewer push hoặc sửa branch của Executor.

## Những chốt ĐÃ ĐẠT

| chốt | kết quả |
|---|---|
| write set | đúng hai tệp |
| trần ADR-0044 | 2 tệp / **265** dòng thêm (≤3 / ≤300) |
| `A9` | `rc=0`, **82/82**, hai số bằng nhau, ≥ sàn **73** |
| `A12` | run `32584951798` trên exact head — ubuntu **success 31 bước 0 hỏng** · windows **success 31 bước 0 hỏng**. Đo THEO JOB |
| `A11` | executor khai `actionlint rc=0`; container thiếu `shellcheck` ⇒ yếu hơn CI, executor khai thẳng |
| `_BANG_LOP` | danh sách **CHO PHÉP** (`next(..., "sensitive")`) |
| `write_set` thiếu/rỗng/sai kiểu | ⇒ `sensitive` |
| `role: reviewer` | ⇒ `sensitive` **vô điều kiện**, KHÔNG mở `ops/leases/` — Q1 đã thu hồi, đúng |
| role lạ | ⇒ `sensitive` |
| tự quy chiếu vế DƯƠNG | cổng MỚI lên chính lease `…-2r3` ⇒ **`rc=0`** |
| tự quy chiếu vế ÂM | hạ `effective_review_class` `sensitive→systemic` ⇒ **`rc=10`** |

## Bước kế

`attempts_used: 0/3`, vòng canon `0/2` trước lượt này ⇒ còn dư khắc phục. Executor `codex` vá hai P1.

**Chưa đủ để land kể cả sau khi vá:** `ADR-0045` điều kiện **(e) human readback trước land** chưa
xong. Khối `ngoai_le_ADR_0045` trong lease là **preflight thủ công** — `PROTOCOL §20` xếp `ADR-0045`
đúng ô `0 cổng`, không cổng nào canh nó.
