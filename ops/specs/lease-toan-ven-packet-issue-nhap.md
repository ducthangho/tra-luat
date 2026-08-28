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
