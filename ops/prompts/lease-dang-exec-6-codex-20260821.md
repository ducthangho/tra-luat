# Prompt EXECUTOR — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **6**

Lease `lease-dang-exec-6-codex-20260821`.

**ĐỌC ĐOẠN NÀY TRƯỚC.** Lượt 5 bạn **DỪNG đúng chốt**, và **bạn đúng**: `T66` của r5 đòi mọi
guard khẳng định *"lease đó không POST"*, nhưng **ba trong tám guard nằm SAU lời gọi POST** — vế
ấy bất khả thi. Phiên điều phối đã đo lại thứ tự trong YAML và xác nhận. Bạn từ chối lách bằng
đồ giả sai trạng thái, từ chối tuyên đóng (thứ sẽ là hình dạng A lần 7), và hoàn nguyên sạch.
**Đó là hành xử đúng, và đặc tả là thứ sai — lần thứ ba liên tiếp.**

**Phần kiến trúc của bạn thì CHẠY**: `M1` ⇒ `65/66` ĐỎ `t64` (phép thử quyết định đạt), `M2`/`M3`
cùng chết, cả sáu đột biến gỡ guard giết `t66`, hai tập guard bằng nhau 8 mục, không mutant đa
sát. **Giữ nguyên ý tưởng ấy.** Chỉ vế khẳng định là phải làm khác.

## Nguồn sự thật

1. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r6.md`** — DELTA, sha256
   `4ee67d54b5504c0b303dad3bf8470c912ad754e6bcda42e8cb4a2866475ba181`
2. r5 `2c8fb5c6…` · r4 `abe7c292…` · r3 `c65d5dbd…` · r2 `3f310582…` — nguyên hiệu lực cho mọi
   thứ r6 không nêu.
3. **Handoff lượt 4 của bạn** `dfada28511f0b63e4922b98fa08b55cb03d57f28faccfb9709b227e316c291b7`.
4. `CLAUDE.md`.

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Việc

### `T66′` — thay `T66`. Vế khẳng định PHỤ THUỘC VỊ TRÍ

Mỗi guard trong sổ có ca **thật**.

**Vế CHUNG, mọi guard:** lease khác **vẫn** được xử · `BI_CHAN` đúng · mã thoát bước đúng.

**Vế PHỤ THUỘC VỊ TRÍ: bạn DẪN XUẤT, đặc tả KHÔNG liệt kê.**

Đây là thay đổi có chủ đích. Ba lượt qua, đặc tả liệt kê vế khẳng định và **sai ba lần**. Lượt
này đặc tả chỉ nêu **bất biến**:

> Mỗi ca khẳng định thứ **QUAN SÁT ĐƯỢC** tại vị trí guard ấy, và **KHAI** thứ không quan sát
> được.

Gợi ý — **không phải mệnh lệnh**, bạn quyết: guard **trước** POST thì *"lease đó chưa gửi lời gọi
POST nào"* quan sát được; guard **sau** POST thì thứ quan sát được là **trạng thái ghi ngược**,
không phải sự vắng mặt của POST.

**Thấy một vế bất khả thi ở guard nào ⇒ KHAI ra và DỪNG ca đó.** Đừng lách bằng đồ giả sai trạng
thái. Bạn đã làm đúng điều này ở lượt 5.

### `T67` — ca khoá cho Q29: VỊ TRÍ phải DẪN XUẤT TỪ YAML

Chuyển một guard **trước** POST thành **sau** POST **trong YAML** ⇒ tập vế của guard ấy phải
**đổi theo**.

**M4** — di chuyển một guard qua bên kia lời gọi POST trong YAML mà **giữ nguyên** tập vế ⇒
**PHẢI ĐỎ**.

**M4 là phép thử quyết định của lượt này.** Không chết ⇒ vị trí đang bị **ghi cứng** ⇒ bạn mới
**dời chỗ ghi cứng** chứ không bỏ nó ⇒ **DỪNG** (chốt đăng ký trong r6).

## KHÔNG làm — một mục MỚI và quan trọng

**KHÔNG đổi thứ tự lệnh trong thân bước `đăng`. KHÔNG thêm rollback. KHÔNG thêm preflight.**

Cửa sổ *"POST xong rồi `mark` hỏng"* là **thuộc tính của thiết kế hiện hành**, không phải khuyết
tật của phép đo. Vá nó là đổi sản phẩm giữa một packet đang đo sản phẩm ấy. **KHAI vào
`chua_do_duoc`**, đừng vá — và nói đúng chữ: thứ **duy nhất** che cửa sổ ấy là `kiem-github` trả
`rc=9` ở lượt sau. **Che, không đóng.**

Cũng giữ nguyên các cấm cũ: `ops/specs/**` · `_doc_gh`/`_kiem_loai_so_hieu`/`_kiem_comment_da_co`
cho nhánh bảng `Q24` xếp *"một phần"* · finding đã đóng · khe race · nợ nền `chay(env=None)`.

## Ngân sách

**≤ 3 tệp, ≤ 660 dòng THÊM** so với `cfaccff9`. Head `b32b4241` đang **`+541`** ⇒ còn **~119 dòng**.
Vượt ⇒ DỪNG + handoff. Dòng xoá không tính.

## Cổng bắt buộc

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` bằng nhau, **≥ 67 ca** |
| cùng suite, ba biến GitHub đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 |
| **M1** thêm guard vào YAML, không đăng ký | **PHẢI ĐỎ** |
| **M2** xoá mục khỏi sổ · **M3** bộ trích trả `[]` | **PHẢI ĐỎ** |
| **M4** dời guard qua bên kia POST, giữ nguyên vế | **PHẢI ĐỎ** — phép thử quyết định |
| gỡ **từng** guard (tám) | ca của guard đó **PHẢI ĐỎ** (`mark`/`body`/`$GITHUB_ENV` hiện sống sót `63/63`) |
| kích thước | ≤ 3 tệp, ≤ 660 dòng thêm — số THẬT |

## Điều kiện DỪNG

- Ngân sách sẽ vượt 660 ⇒ DỪNG + handoff.
- **A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần **4** ⇒ DỪNG.
- **`M4` không giết `T67`** ⇒ **DỪNG** — vị trí đang ghi cứng, tức D lần 4 dưới lớp áo mới.
- Một vế khẳng định **bất khả thi** ở guard nào ⇒ KHAI và DỪNG ca đó, không lách.

## Báo cáo cuối

1. `git diff --numstat cfaccff9..HEAD` — số thật.
2. `N/N`, hai lần chạy.
3. Bảng đột biến: **M1–M4** và **tám** đột biến gỡ guard. Kèm danh sách đa sát.
4. **Bảng vị trí** — với mỗi guard: vị trí **dẫn xuất từ YAML** (trước/sau POST) ↔ tập vế bạn đã
   chọn ↔ thứ **không quan sát được** ở vị trí ấy. In cả tập guard dẫn xuất và sổ đăng ký cạnh nhau.
5. `chua_do_duoc` của riêng bạn, **bắt buộc** gồm cửa sổ *"POST xong, `mark` hỏng"*.
   **"Thu hẹp"** khi chỉ thu hẹp; **"đóng"** chỉ khi có phép đo.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
