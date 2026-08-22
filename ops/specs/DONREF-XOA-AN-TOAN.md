# ĐẶC TẢ ĐÓNG BĂNG — `DONREF-XOA-AN-TOAN`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (§3.2, §4) mới được bắt tay.
> Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**. Sửa đè là làm `spec_sha256` trong lease trỏ
> vào một thứ không còn tồn tại.

`packet_id`: `DONREF-XOA-AN-TOAN`
`packet_issue`: `#217`

## `nguon_cap_viec`

Packet **khắc phục**. Tiền nhiệm: PR `#213` (đóng băng, draft) và biên nhận
`ops/reviews/donref-review-2-codex-verdict.receipt.yaml` (sha256 `0b35d867…` cho verdict lượt 2).

Người giữ kho quyết hướng đi trong phiên 2026-08-21, qua năm câu hỏi của lượt soạn spec. Quyết
định gốc: **KHÔNG tự động hoá việc xoá ref.**

## Quyết định đã chốt — và vì sao

| # | quyết định | căn cứ ĐO ĐƯỢC |
|---|---|---|
| Q1 | **Không tự động hoá.** `ops-don-ref.yml` giữ lệnh cấm. Thay bằng công cụ **chỉ ĐỌC**. | Nhu cầu thật là 17 nhánh, một lần, mà một lệnh `git push origin --delete` giải quyết xong. Hai P1 của `#213` đều sinh ra từ chỗ workflow **giữ quyền phá**; bỏ quyền ấy thì cả lớp rủi ro chết theo **kiến trúc**, đúng tiền lệ `shell_environment_policy` (bốn lượt vá, rồi kết luận: công cụ không ghi vào tệp người dùng nữa). |
| Q2 | Dọn 17 nhánh là **việc riêng, chạy ngay**, không thuộc packet này. | Không phụ thuộc cơ chế nào. Đã đo và giao lệnh cho chủ kho 2026-08-21 (13 nhóm A + 4 nhóm B). |
| Q3 | **Không đụng `ops-don-ref.yml` trên `master`.** | `master` vẫn là bản cấm tuyệt đối — tức đã đúng với Q1. Bản vá của `#213` ở lại trên nhánh đóng băng làm hồ sơ. Sửa `master` để "hoàn nguyên" là sửa thứ chưa từng đổi. |
| Q4 | **Không sửa `CLAUDE.md` trong packet này.** | Câu sai *"đọc lại **đóng** khe"* chỉ tồn tại trên nhánh `#213`; `master` **chưa bao giờ** mang nó. Thứ `master` thiếu là **bài học**, và nó thuộc `#208 (PROTO-02)`. |
| Q5 | Công cụ là **`ops/nhanh_don_duoc.py`**, chạy cục bộ bằng `git` thuần. | Workflow là thứ **có quyền**; script đọc thì không. Đó là toàn bộ điểm của Q1. |
| Q6 | Bất biến: **`behind_by = 0`** so với nhánh mặc định, **kèm khai giới hạn trong chính đầu ra**. | P1 lượt 2 của `#213` (nhánh mặc định lùi sau phép đo) **vẫn đúng** và **KHÔNG được đóng** ở đây. Với công cụ chỉ đọc, hậu quả khác hẳn: nó in lệnh cho người đọc chạy ngay, không phải một workflow tự chạy sau phép đo cũ. Cái phải làm là **khai**, không phải bịt. |
| Q7 | Executor: **`codex`**. | L4 đo được: **năm lần cùng một hình dạng lỗi, cùng một executor** (`claude`). Đổi nền là phép thử rẻ nhất cho giả thuyết "hình dạng bám người viết, không bám bài toán". |

**Ghi chú về lượt chuẩn thuận:** người giữ kho trả lời *"đồng ý cả bốn"* cho một vòng có **năm**
câu (Q3–Q7). Cách đọc duy nhất nhất quán là chuẩn thuận cả năm — mọi khuyến nghị trong vòng ấy
cùng một hướng và không câu nào mâu thuẫn câu nào. Ghi ra vì một con số lệch trong hồ sơ chuẩn
thuận là thứ nửa năm sau không ai giải thích được (L1).

## `review_class`

**`cross_approved`** — mức chặt nhất trong các mức tự động, dù packet **không** chạm
`.github/workflows/` hay bất kỳ đường authority nào.

Lý do fail-closed (§3): đầu ra của công cụ là **một lệnh phá** mà người ta sẽ dán vào terminal.
Công cụ không ghi gì, nhưng **một phân loại sai làm mất commit** y hệt như tự tay xoá nhầm. Rủi
ro nằm ở **đầu ra**, không ở quyền ghi — nên không được hạ mức chỉ vì tệp trông vô hại.

Executor `codex` ⇒ reviewer phải là `claude`.

## `write_set`

Đúng **hai** đường dẫn, cả hai đều **mới**:

```
ops/nhanh_don_duoc.py
ops/nhanh_don_duoc_test.py
```

Không dùng ký tự đại diện. Không tệp nào khác được sửa — kể cả `CLAUDE.md`, kể cả
`.github/workflows/ops-don-ref.yml` (Q3, Q4).

Kích thước dự kiến: **≤ 2 tệp, ≤ 400 dòng thêm**. Ngưỡng ADR-0044 cho packet thường là ≤ 6 tệp và
≤ 1.000 dòng; packet này ở xa dưới. Nêu số để đối chiếu: `#213` đo được **3 tệp, +293/−21**, tức
sát trần 300 của packet `sensitive` — và bản vá cho P1 lượt 2 chắc chắn vượt. Đó là một trong
những lý do nó không được vá tiếp.

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm |
|---|---|
| Sửa `.github/workflows/ops-don-ref.yml` | Q1/Q3. `master` đã đúng. Đụng vào là mở lại đúng bề mặt vừa quyết bỏ. |
| Đóng **P1 lượt 2** (nhánh mặc định lùi sau phép đo) | **CỐ Ý để mở.** Công cụ chỉ đọc không đóng được nó và cũng không cần — nó **khai** ra (mục tiêu 4). Đóng nó đòi CAS nhiều ref trong một workflow có quyền, tức quay lại Q1. |
| `atomic multi-ref lease` (đã đo hai chiều ở `#213`) | Là bản vá cho một workflow **có quyền**. Q1 bỏ hướng ấy. Phép đo giữ trong hồ sơ `#213` để nếu sau này Q1 bị lật thì không phải đo lại. |
| Sửa `CLAUDE.md` | Q4 — thuộc `#208`. |
| Dọn 17 nhánh | Q2 — việc riêng, đã giao. |
| Rà 70 nhánh nhóm C | Việc riêng. Công cụ chỉ **phân loại**, không phán xét nội dung. |
| `ops-publish-lease.yml` thiếu `pull-requests: write` | Đã biết, bản vá riêng. |

## `muc_tieu`

Mỗi mục chiếu vào **một** đường dẫn trong `write_set` (L2).

1. **`ops/nhanh_don_duoc.py`** — phân loại **mọi** nhánh của remote thành ba nhóm bằng `git`
   thuần: **A** = mọi commit đã nằm trong nhánh mặc định · **B** = chỉ còn đúng một commit mà
   nội dung đã bị thay trên nhánh mặc định · **C** = còn commit riêng, **hoặc KHÔNG ĐO ĐƯỢC**.
   Không gọi API, không cần token.
2. **`ops/nhanh_don_duoc.py`** — in một lệnh `git push origin --delete` chứa **đúng** nhóm A và
   B, và **không bao giờ** chứa nhánh mặc định.
3. **`ops/nhanh_don_duoc.py`** — **ba trạng thái, không phải hai**: mọi thứ không đo được rơi vào
   **C** kèm **lý do in ra**, không bao giờ rơi vào A hay B.
4. **`ops/nhanh_don_duoc.py`** — in **khai giới hạn** ngay trong đầu ra: phân loại chỉ đúng tại
   thời điểm đo, vì nhánh mặc định có thể bị ép lùi sau đó (P1 lượt 2 của `#213`), và lệnh in ra
   **không** có phép kiểm nào lúc chạy.
5. **`ops/nhanh_don_duoc_test.py`** — phản chứng dựng **kho bare thật** (không đồ giả diễn kịch
   bản), phủ đủ bảy tiêu chí dưới.

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo nào làm nó ĐỎ** (L3). Mọi đột biến chạy trên **bản sao tạm**.

| # | mục tiêu | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|---|
| T1 | 1 | Fixture `A → S → D`, `nhanh=S`, mặc định`=D` ⇒ `nhanh` vào **A** | đảo chiều phép so tổ-tiên |
| T2 | 1 | `nhanh` có commit riêng ⇒ vào **C** | bỏ phép kiểm commit riêng |
| T3 | 1 | Nhánh có đúng một commit **khác** `posted_comment_id` ⇒ vào **C**, không phải B | nới điều kiện B thành "một commit bất kỳ" |
| T4 | 3 | `git` trả lỗi / ref biến mất giữa chừng ⇒ vào **C** kèm lý do, **không** vào A | coi lỗi là "không có commit riêng" |
| T5 | 2 | Lệnh in ra **không** chứa nhánh nhóm C nào | in cả C vào lệnh |
| T6 | 2 | Lệnh in ra **không** chứa nhánh mặc định, kể cả khi nó trivially là tổ tiên của chính nó | bỏ chốt loại trừ nhánh mặc định |
| T7 | 4 | Đầu ra chứa dòng khai giới hạn | xoá dòng khai |

Ngoài bảy ca: **suite phải `rc=0` với `N/N` hai số bằng nhau**, và mỗi đột biến phải giết **đúng
ca của nó** — một đột biến giết nhiều ca là dấu hiệu ca chưa tách đủ, phải nói ra chứ không làm
tròn thành đạt.

**Tiêu chí KHÔNG đo được, ghi thẳng:** không có ca nào chứng minh lệnh in ra sẽ **chạy đúng trên
máy chủ kho** — phiên này bị proxy chặn xoá ref (403, đo lại 21-08-2026). Xem `chua_do_duoc`.

## `hinh_dang_ke_thua`

Chép từ hồ sơ tiền nhiệm (L4). **Hình dạng: *lời khai rộng hơn phép đo*.**

| lần | packet · lượt | biểu hiện |
|---|---|---|
| 1 | PLAT-X5 · review 1 | `t34` khai **hẹp hơn** thực tế — bốn dạng lọt không được khai |
| 2 | PLAT-X5 · review 2 | chú thích `GOI_WRAPPER_THUC_THI` khai **ngược**: nói bắt được, đo ra không |
| 3 | PLAT-X5 · review 3 | docstring `_cat_chu_thich_run_inline` không nêu `$'…'` |
| 4 | DONREF · review 1 | `CLAUDE.md`: *"đọc lại **đóng** khe"* — chỉ **thu hẹp** |
| 5 | DONREF · review 2 | lease khai là đóng khe, thực tế bảo vệ **nửa** giao dịch |

**Năm lần, cùng một executor (`claude`).** Biên nhận `#213` chỉ đếm 2 vì nó nhìn trong phạm vi
packet mình; đếm xuyên hồ sơ ra 5.

**Chốt cho packet này:** gặp hình dạng ấy **lần thứ sáu** ⇒ **DỪNG, không vá**, xuất handoff và
trả về người giữ kho. Đó là lý do Q7 đổi executor sang `codex`: nếu `codex` cũng mắc, giả thuyết
"hình dạng bám người viết" **sai**, và vấn đề nằm ở đặc tả — lúc ấy sửa đặc tả, đừng sửa mã.

## `chua_do_duoc`

Ghi thẳng, không giấu sau chữ "có thể":

1. **Lệnh in ra chạy đúng trên máy chủ kho hay không** — phiên này không xoá được ref (proxy trả
   403, đo 16-08 và đo lại 21-08-2026). Chỉ chủ kho xác nhận được, sau khi chạy.
2. **P1 lượt 2 vẫn mở** — nhánh mặc định bị ép lùi giữa lúc đo và lúc chủ kho dán lệnh. Công cụ
   **khai** rủi ro này (mục tiêu 4) chứ không đóng. Khe thời gian nay là "vài giây tới vài phút
   của một người", không phải "một workflow chạy sau phép đo cũ" — nhưng nó **không bằng không**.
3. **70 nhánh nhóm C chưa ai rà nội dung.** Công cụ chỉ phân loại; nó **không** nói nhánh nào
   đáng giữ.
4. **Bảy trục của `#213` vẫn chưa ai đo** (tám mutant đã khai, multi-ref dở dang, `actions/checkout`
   credential, lịch sử rời, ngưỡng 250 commit của `compare`, đột biến chèn bước YAML, lập luận
   `M2`). Chúng thuộc hướng đã bị Q1 bỏ, nên **không** trở thành nợ của packet này — nhưng nếu Q1
   bị lật sau này thì chúng vẫn ở đó, chưa đo.
5. **Ngưỡng 250 commit của `compare`** không áp dụng ở đây vì công cụ dùng `git` cục bộ chứ không
   dùng REST — nhưng **chưa đo** hành vi khi kho cục bộ **nông** (`shallow`). Kho này đã trả giá
   một lần vì clone nông làm mỏ neo commit gốc sai. Đây là ca đầu tiên phiên thi hành nên dựng.
