# `LEASE-TOAN-VEN` — sổ lease mang đúng cái lỗi mà kho vừa bỏ một packet ra để đóng

Ngày 2026-08-28, packet #348 land một `SafeLoader` từ chối khoá trùng YAML — chặn được ở **8/8**
mức, sau bốn lượt cross-review. Cùng ngày, phiên điều phối quét sổ lease và đo được: **chính các
tệp lease đang mang khoá trùng**, `yaml.safe_load` nuốt im lặng, và không cổng nào nhìn vào đó.

Hồ sơ này mở packet cho ba nợ ấy.

**Số dưới đây là số phiên điều phối TỰ ĐO.** Executor đo lại.

---

## Nợ 1 — `ops-publish-lease-THEM-posted_comment_id-thay-vi-THAY`

Workflow `.github/workflows/ops-publish-lease.yml` ghi `posted_comment_id` vào tệp lease sau khi
đăng. Nó **thêm dòng** thay vì **thay giá trị**, nên tệp có hai khoá cùng tên.

Ví dụ đo được — `ops/leases/tach-danh-tinh-github-exec-1r6-codex-20260828.yaml`:

```
170:posted_comment_id:   # workflow ghi, ĐỪNG sửa tay
171:posted_comment_id: 5449260853   # workflow ghi, ĐỪNG sửa tay
```

`yaml.safe_load` trên tệp ấy: **không cảnh báo, không lỗi**, trả `5449260853` (bản cuối thắng).
Hôm nay bản cuối tình cờ đúng — nên nợ này **chưa gây hại**, và phải nói đúng như thế.

Quét toàn sổ, **198 blob lease DUY NHẤT trên 15 nhánh** (`ops/leases/*.yaml`, so bằng blob sha nên
không đếm trùng):

| dạng khoá trùng | số tệp |
|---|---:|
| `posted_comment_id` | **8** |
| `thay_the_cho` + `thay_the_ly_do` | **3** |
| **tổng** | **11** |

Dạng thứ hai đến từ **nguồn khác** (sửa tay, cũ hơn) — đừng gộp hai nguyên nhân làm một.

## Nợ 2 — `lease_publish-doc-bang-safe_load-nen-mu-voi-chinh-thu-no-tao-ra`

`ops/lease_publish.py` đọc lease bằng `yaml.safe_load` ở hai chỗ (`:213`, `:529`). Đó là **đúng cái
lỗi** packet #348 vừa bỏ bốn lượt review ra để đóng — nhưng loader chặt ấy chỉ đọc
`.github/workflows/`. `ops/leases/` **không ai canh**, và đó chính là nơi lỗi đang sống, 11 tệp,
đo được.

Không phải "cùng loại lỗi". Là **cùng một lỗi, ở thư mục bên cạnh**.

## Nợ 3 — `check-long-hon-giao-thuc-va-neo-sha-khong-ai-doi-chieu`

`lease_publish check` cho qua lease **thiếu** `generation`, `spec_hash`, `nang_tran`, và **không
đối chiếu neo sha với thực tế**. Bằng chứng sống, từ chính lease của packet #348:

| revision | `reviewed_sha_required` | `base_sha` | sự thật |
|---|---|---|---|
| r3 | `f715fc2813…` | `f715fc2813…` | `f715fc2` là **merge commit của #344**, tức **base**, không phải head |
| r4 | `f715fc2813…` | `f715fc2813…` | như trên |
| r5 | `f715fc2813…` | `f715fc2813…` | như trên |
| r6 | `f715fc2813…` | `f715fc2813…` | nhánh **đã rebase** lên `6c2e097`; head thật `836b0a7` |

`reviewed_sha_required` bằng đúng `base_sha` — một lỗi **chép**, sinh ở r3 và bê nguyên qua bốn
revision. r6 viết **sau** khi rebase mà `base_sha` vẫn là base cũ. Cả bốn đều đã `check rc=0`, đã
đăng, không ai thấy. Head thật được review và merge là `836b0a7`, base thật `6c2e097`.

Người viết bốn lease ấy là phiên điều phối claude. Nợ này là nợ của chính nó, ghi ra ở đây thay vì
để người sau vấp.

## Nợ 4 — `thu-hoi-lease-chua-co-duong` (kế thừa `AG-T0-01B`)

Không có lệnh nào kết thúc một lease đã cấp. Hệ quả đo được ngày 2026-08-28: hai packet **đã land**
(`#348`, `#351`) vẫn giữ write set của chúng —

```
.claude/dev/duyet_danh_tinh_test.py  rc=11  NGƯỜI_GIỮ 1: tach-danh-tinh-github-exec-1r6-...
.claude/dev/chon_reviewer.py         rc=11  NGƯỜI_GIỮ 1: chon-reviewer-exec-1r8-...
```

— nên **hai packet `DUYET-DANH-TINH-DO-PHU` và `CHON-REVIEWER-DUONG-DAN` không cấp lease được.**
Lease #348 r6 đã ghi hai lần trước rằng nợ này chặn việc thật. Đây là lần **thứ ba**, và lần này nó
chặn hai packet cùng lúc.

Tiền lệ đã ghi sổ, `ops/RUT_LEASE_PLAT_X8_20260821.md`: *"kho vốn không có đường ấy — cơ chế duy
nhất được cài đặt là **chờ hết hạn**"*. Lease `plat-x8` hôm ấy rút được **chỉ vì nó chưa từng được
đăng**; không phải vì có đường rút. Cùng tài liệu, đo ngày 21-08: **10** quyền ghi còn sống sau khi
việc đã xong (lần đo trước: 5). Con số ấy là của 21-08 — **đừng nhắc lại như số hôm nay; đo lại.**

## Hành vi CHƯA KHOÁ trong chính tệp bạn sắp sửa

`ops/RUT_LEASE_PLAT_X8_20260821.md` còn ghi một quan sát về `ops-publish-lease.yml`: bộ lọc
`paths: ops/leases/**.yaml` **có vẻ không đánh giá được khi đẩy tạo NHÁNH MỚI** (không có commit
"before" để so) — đo được **0** lượt chạy trên nhánh mới, trong khi nhánh đã tồn tại có 3 lượt cùng
buổi. Tài liệu ấy tự khai rất rõ đây là **suy luận từ hai quan sát, KHÔNG phải phép đo có phản
chứng**, và chưa ai dựng ca cho nó.

Bạn sắp sửa đúng tệp ấy. **Đừng vá lên một hành vi chưa ai đo.** Hoặc dựng ca cho nó, hoặc khai
rằng bản vá của bạn không phụ thuộc vào hành vi ấy.

---

## Việc

1. Workflow: **thay** `posted_comment_id` thay vì thêm. Kèm ca đòi tệp sau khi ghi hai lần vẫn chỉ
   có **một** khoá.
2. `lease_publish.py`: đọc lease bằng loader từ chối khoá trùng. **Đừng chép** loader của #348 —
   kho có `doctrine-scan` cấm chép; hoặc dùng chung, hoặc khai vì sao phải có bản riêng.
3. `check`: đòi `generation`/`spec_hash`/`nang_tran` đúng như giao thức; và **đối chiếu neo sha** —
   tối thiểu là `reviewed_sha_required` phải tồn tại và **không được bằng** `base_sha`.
4. Mở đường **kết thúc lease**, đủ để hai packet kia chạy được.
5. Chữa 11 tệp đang có khoá trùng — **đọc câu hỏi thật dưới đây trước khi làm việc này.**

## CÂU HỎI THẬT — hồ sơ CỐ Ý không đưa đáp án

Giao thức nói **thay thế, không sửa lease đã đăng** (`§8`). 11 tệp lease đang hỏng là lease **đã
đăng**. Nên việc 5 tự mâu thuẫn với giao thức nếu làm theo nghĩa đen "sửa tệp".

Và có một vòng: nếu chữa bằng cách **thay thế** thì sinh revision mới — mà workflow sẽ lại **thêm**
`posted_comment_id` vào bản mới, tái tạo đúng lỗi. **Thứ tự quan trọng**, và hồ sơ này không quyết
hộ thứ tự ấy.

`(A)` sửa workflow trước, rồi thay thế 11 lease — sạch giao thức, đắt, sinh 11 revision ·
`(B)` chấp nhận 11 tệp cũ hỏng, chỉ chặn từ nay: loader chặt + ca canh, ghi rõ 11 tệp là **nợ đã
biết, không chữa**, kèm lý do ·
`(C)` phân biệt: `posted_comment_id` là trường **do máy ghi sau khi đăng**, có thể lập luận nó
không thuộc phần "đã đăng" bất biến — nếu vậy sửa tại chỗ là hợp lệ. **Lập luận ấy phải được viết
ra và chịu review, không được ngầm định.**

`(A)` nghe đúng nguyên tắc nhất và có thể là lãng phí nhất. `(B)` thành thật nhưng để lại 11 tệp
mà `safe_load` vẫn đọc sai nếu ai đó đọc chúng. **Không được chọn `(A)` chỉ vì nó nghe kỷ luật.**

Câu hỏi thứ hai, độc lập: việc 4 (kết thúc lease) là **thẩm quyền**, không phải cơ chế. Ai được
kết thúc một lease? Người giữ? Chủ kho? Hay chỉ "packet đã land" mới là căn cứ đủ? Kho đã có bài
học *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"* — **đừng làm một lệnh `ket-thuc` mà bất kỳ
phiên nào cũng gõ được rồi gọi đó là thu hồi.**

## write set

- `.github/workflows/ops-publish-lease.yml`
- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

11 tệp trong `ops/leases/` **chỉ vào write set nếu chọn `(A)` hoặc `(C)`** — và khi đó phải là một
revision của lease với danh sách 11 đường **liệt kê đủ**, không phải glob.

## ĐO NGƯỜI GIỮ — cả ba đường đều TRỐNG

`ai-dang-giu` trên bản sao cách ly (244 ref, hai nguồn lệch 0), 2026-08-28:

```
ops/lease_publish.py                      rc=0    (chỉ lease HẾT_HẠN)
ops/lease_publish_test.py                 rc=0    (chỉ lease HẾT_HẠN)
.github/workflows/ops-publish-lease.yml   rc=0    (chỉ lease HẾT_HẠN)
```

**Packet này cấp lease được ngay.** Hai packet kia thì không — và việc 4 của packet này chính là
thứ mở khoá cho chúng. Nên nếu chỉ chạy được một packet, **chạy packet này trước.**

---

# BẢN SỬA ĐỔI 2 — thu hẹp, và SỬA MỘT TIỀN ĐỀ SAI của bản 1

Bản 1 (`sha256 28ce8e1e…`) đã đăng và **giữ nguyên làm hồ sơ**; bản này thay thế nó, không sửa lén.

## Sửa tiền đề sai: nợ 1 KHÔNG nằm trong workflow

Bản 1 xếp `.github/workflows/ops-publish-lease.yml` vào write set cho nợ 1, và chủ kho đã duyệt
phóng packet với phạm vi ấy. **Đo lại thì sai.** Workflow chỉ **gọi**
`python3 ops/lease_publish.py mark`. Phép nối dòng nằm ở **`ops/lease_publish.py:876`
`_ghi_comment_id`**, và `:888` `p.write_text` là **chỗ DUY NHẤT trong toàn kho** ghi vào tệp lease.

Cơ chế đầy đủ, chạy thật chứ không suy luận:

```
safe_load doc: posted_comment_id = None  ->  bool = False
khoa CO MAT trong dict? True
[chay _ghi_comment_id]  =>  tep co HAI dong posted_comment_id
```

Chốt idempotent `:775` hỏi `if lease.get("posted_comment_id"):`. Khoá **có mặt**, giá trị **rỗng**
⇒ `None` ⇒ falsy ⇒ chốt không nổ ⇒ nối dòng thứ hai. Doctrine `None ≠ False` ở dạng thứ ba:
**`None` ≠ VẮNG MẶT**.

Nửa thứ hai của nợ này là của phiên điều phối: **8/8** tệp hỏng có placeholder rỗng ở dòng đầu, cả
8 là lease phiên này viết (#348 r3–r6, #351 r5–r8). Quét `ops/`, `docs/`, `.github/`: không tài
liệu nào bảo viết placeholder ấy. Nửa ấy **đã sửa, không tốn dòng mã** — thôi viết placeholder.

**Hệ quả:** packet này KHÔNG có đường ghi khả dụng cho tới khi `ops/lease_publish.py` được nhả.
Phóng với write set của bản 1 là giao cho executor một phạm vi không chứa chỗ phải sửa — đúng điều
kiện dừng `S1`.

## Nợ 4 (đường THU HỒI) — GỠ KHỎI PACKET NÀY, chuyển sang #385

Phiên giữ #372 mở **Issue #385** cho việc ấy. Phiên này đã cam kết công khai ở #372: nếu họ mở
Issue mới thì gỡ nợ 4 khỏi đây, để không có hai hồ sơ cho một việc. Điều kiện đã thoả.

#385 phủ nó **đầy đủ hơn** bản 1: ba tuyến bằng chứng (21-08 đo 5 quyền ghi sống thừa; 28-08
schema `thay_the_cho` một-chuỗi ép phiên W1-P1 phải viết bia mộ một chiều; phép đếm 6/7 là chuỗi
revision), và đặt đúng câu mà bản 1 cho là quan trọng nhất — *"thu hồi phải ĐÒI BẰNG CHỨNG, không
nhận LỜI KHAI"*, kèm nhận định *"một lệnh `thu-hoi` nhận lời khai thì tệ hơn không có lệnh"*.

Nợ 4 **không còn là việc của packet này**. Đừng thi công nó ở đây.

## Phạm vi còn lại — ba nợ, một đường ghi

| nợ | ở đâu |
|---|---|
| 1 — `_ghi_comment_id` nối vô điều kiện + chốt idempotent hỏi sai câu | `ops/lease_publish.py` |
| 2 — `lease_publish` đọc bằng `yaml.safe_load` nên mù khoá trùng (`:213`, `:529`) | `ops/lease_publish.py` |
| 3 — `check` lỏng hơn giao thức; neo sha không ai đối chiếu | `ops/lease_publish.py` + test |

Ba nợ, **một tệp**. Bản 1 đề nghị hoãn nợ 3; đề nghị ấy **rút lại** — khi cả ba đã cùng một đường
ghi thì tách chúng chỉ tạo thêm hàng đợi, không giảm rủi ro.

## write set (thay thế bản 1)

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

`.github/workflows/ops-publish-lease.yml` **RA KHỎI** write set — không có gì để sửa ở đó.

11 tệp trong `ops/leases/` vẫn chỉ vào write set nếu chọn `(A)`/`(C)` của câu hỏi thật ở bản 1, và
khi ấy phải liệt kê đủ 11 đường. Lưu ý #385 đặt ràng buộc ngược lại cho packet của họ — *"KHÔNG mở
write set sang `ops/leases/**` cùng lúc với việc sửa `ops/lease_publish.py`"* — và lý lẽ ấy áp
dụng cho packet này y hệt. Cân nhắc lại trước khi gộp.

## HÀNG ĐỢI — packet này đứng THỨ BA cho tệp của nó

1. **#372 / PR #383** — đang cross-review, giữ `ops/lease_publish.py` tới `2026-08-29T09:00Z` hoặc
   tới khi land.
2. **#385** — khai thẳng *"Chờ #383 land trước"*; sẽ giữ tiếp cùng tệp.
3. **packet này**.

Đây là dữ kiện để chủ kho quyết, không phải lời than. Một hình dạng đáng cân nhắc: nợ 1 và 2 **có
liên quan trực tiếp** tới #385 — #385 sẽ viết **bộ ghi thứ hai** vào tệp lease (`da_thu_hoi`), và
tiền lệ duy nhất nó nhìn vào chính là `_ghi_comment_id` đang hỏng. Cảnh báo ấy đã gửi #385; việc
có gộp hay không là của họ và chủ kho, packet này **không đòi**.

## Câu hỏi thật của bản 1 — GIỮ NGUYÊN

Câu hỏi về `(A)`/`(B)`/`(C)` cho 11 tệp đã đăng, và bẫy thứ tự *"sửa người ghi TRƯỚC, thay thế 11
tệp SAU"*, **không đổi**. Bản sửa đổi này chỉ đổi write set và bỏ nợ 4.

---

# BẢN SỬA ĐỔI 3 — nhận phép đo `spec_hash` từ Issue #377 (nay đóng vì trùng)

Một phiên khác mở **#377** cho đúng phần `spec_hash` của nợ 3, rồi đóng vì trùng với packet này và
chuyển phép đo sang. Nội dung ấy không nên chỉ sống trong một comment, nên gộp vào đây.

## Phép đo — ĐÃ ĐO LẠI ĐỘC LẬP trên `d4b3045`

| | #377 khai | phiên này đo lại | khớp? |
|---|---:|---:|---|
| lease trong `ops/leases/` | 74 | **74** | ✓ |
| khai `spec_path` | 40 | **37 có giá trị + 3 `null` = 40 khoá** | ✓ (xem chú thích) |
| có `spec_hash` | 2 | **2** | ✓ |
| khai `spec_path: null` | 3 | **3** | ✓ |
| **giao của hai tập** | **0** | **0** | ✓ |

**Chú thích, đọc hẹp lại một dòng:** khối số của #377 liệt kê `40 / 2 / 3` liền nhau nên **dễ đọc
thành một phân hoạch**. Ba tệp `spec_path: null` là **tập con** của 40, không phải hạng mục thứ ba
cộng thêm. Số lease có `spec_path` **mang giá trị thật** là **37**. Kết luận không đổi.

**Không một lease nào trên master vừa nêu đặc tả vừa đóng băng nó.** 37 lease trỏ vào một tệp đặc
tả mà không gì ngăn tệp ấy bị sửa sau khi lease đã cấp; 2 lease (`wp55-r2-review-3/4`) mang băm
**không neo vào tệp nào**; 3 lease (`plat-x5-exec-1*`) khai đặc tả là chữ `null` và cổng vẫn nhận.

Cổng chưa bao giờ hỏi — đo lại và xác nhận:

```
$ grep -n 'spec_hash\|spec_path' ops/lease_publish.py
(khong co ket qua)

ops/lease_publish.py:108
BAT_BUOC = ("packet_issue", "lease_id", "granted_by",
            "lease_expires_at_utc", "reviewed_sha_required")
```

`0/37` không phải kỷ luật kém. Đó là **hình dạng chuẩn của một điều khoản không có ai kiểm** — cùng
họ với `review_rounds_used` (chưa từng tồn tại trong tệp `.py` nào) và với `so-canon` của ADR-0043.

## Sáu chốt cho nợ 3, phần `spec_hash`

1. Có `spec_path` mà thiếu `spec_hash` ⇒ CHẶN.
2. Có `spec_hash` mà thiếu `spec_path` ⇒ CHẶN.
3. `spec_path` là `null` / `~` / rỗng / chỉ khoảng trắng ⇒ CHẶN.
4. Có cả hai ⇒ đọc tệp tại `spec_path` **TỪ REF, KHÔNG từ cây làm việc**, băm sha256, so. Lệch ⇒
   CHẶN, thông điệp nêu **cả hai** băm.
5. `spec_path` trỏ ra ngoài kho, hoặc không tồn tại tại REF ⇒ CHẶN, **mã phân biệt được với (4)**.
6. `spec_hash` không phải 64 hex thường ⇒ CHẶN. `SHA256` regex đã có sẵn ở `ops/lease_publish.py:118`.

## Chốt (4) là chỗ dễ sai nhất — ĐỌC TỪ REF

Kho đã trả giá đúng chỗ này ba lần trong chuỗi `#347` → `#359` → `#378`: `check` đọc từ **REF**,
nên một tệp vừa sửa trong cây làm việc mà chưa commit thì cổng **không thấy**. Ngày 28-08, cấp
lease `r2` cho `#378` bị chặn đúng vì lý do ấy.

Một bản cài đặt đọc `Path(spec_path).read_bytes()` sẽ **xanh trên máy người cấp lease và đỏ trên
CI** — hoặc tệ hơn: xanh ở cả hai trong khi băm chứng nhận một thứ **không có trong lịch sử**.

**Phản chứng bắt buộc, một ca `tNN`:** sửa tệp đặc tả trong cây làm việc **mà không commit**, rồi
chạy `check`. Kết quả phải theo REF, không theo cây.

## Phạm vi — chủ kho đã chốt, và cái giá được nói thẳng

Chủ kho chốt in-session `2026-08-28`: **chỉ chốt NHẤT QUÁN**, không bắt lease nào phải có đặc tả.
Một lease bỏ **cả hai** trường vẫn qua cổng.

Cái giá: **đường né còn nguyên.** Ai không muốn bị đối chiếu băm thì bỏ luôn `spec_path`, và cổng
im. Ghi ra đây để người sau không tưởng nợ 3 đã đóng kín. Việc có bắt buộc đặc tả hay không là
quyết định doctrine (§2), **không thuộc packet này**.

## Ngoài phạm vi — ghi để khỏi bị kéo vào

`docs/PROTOCOL_DA_PHIEN.md:178/184` mô tả state-event comment mang `state_hash` + `prev_event_hash`
và hành vi `paused` khi chain gãy. `git grep` trên `d4b3045`: **0 tệp** cho cả hai. Kho không vận
hành cơ chế đó. Đã có nợ riêng ở PR #380 (`NO_KY_THUAT.md` mục 22). **Không làm ở đây.**
