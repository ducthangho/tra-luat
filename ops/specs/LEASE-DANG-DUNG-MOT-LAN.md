# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-DUNG-MOT-LAN`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (§3.2, §4) mới được bắt tay.
> Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**. Sửa đè là làm `spec_sha256` trong lease trỏ
> vào một thứ không còn tồn tại.

`packet_id`: `LEASE-DANG-DUNG-MOT-LAN`
`packet_issue`: `#227`

## `nguon_cap_viec`

**KHÔNG phải packet khắc phục.** Không có tiền nhiệm thất bại; đây là lỗi phát hiện bằng quan
sát vận hành, đo trong phiên 2026-08-21 theo yêu cầu *"triển khai đi"* của người giữ kho cho
backlog đã liệt kê.

## Bằng chứng — ĐO, không suy

Bốn phép đo dưới đây chạy 2026-08-21 trên `master` = `cfaccff9`.

### Đ1 — comment lease TRÙNG trên hai issue

Đếm dấu `**Lease \`<lease_id>\`**` (do `dung_than()` sinh, duy nhất theo `lease_id`) trong
comment của từng issue:

| issue | `lease_id` | số comment | đúng ra phải có |
|---|---|---|---|
| #206 | `plat-x5-review-2-claude-20260820` | **4** | 1 |
| #206 | `plat-x5-exec-1r4-codex-20260821` | **3** | 1 |
| #206 | `plat-x5-review-3-claude-20260821` | **2** | 1 |
| #215 | `slice-b-c-review-1-codex-20260821` | **2** | 1 |

**11 comment cho 4 lease ⇒ 7 comment thừa.** Đơn vị: comment issue, đếm bằng `issue_read
get_comments`, `perPage=100`.

### Đ2 — bốn lượt chạy ĐỎ, cùng MỘT lỗi

`ops-publish-lease.yml`, 20 lượt gần nhất, 4 lượt `failure`, **cả bốn** cùng một dòng cuối:

```
gh: Resource not accessible by integration (HTTP 403)
##[error]Process completed with exit code 1.
```

| run | nhánh | lease đang đăng lúc chết | `packet_issue` |
|---|---|---|---|
| `32450181557` | `ops/lease-donref-review-1` | `donref-review-1-codex-20260821` | **#213** |
| `32457401715` | `ops/lease-donref-review-2` | `donref-review-2-codex-20260821` | **#213** |
| `32464062577` | `ops/lease-review-214-216` | `tri-thuc-review-1-codex-20260821` | **#214** |
| `32473767302` | `ops/ho-so-217` | `tri-thuc-review-1-codex-20260821` | **#214** |

### Đ3 — vì sao 403: `packet_issue` trỏ vào một PULL REQUEST

`issue_read get` trả `state: closed` cho **cả** issue lẫn PR, nên trường phân biệt duy nhất là
`html_url`:

| số hiệu | `html_url` chứa | loại |
|---|---|---|
| #55 · #194 · #203 · #206 · #215 · #219 · #217 | `/issues/` | ISSUE |
| **#213** · **#214** · #216 | `/pull/` | **PULL REQUEST** |

`ops-publish-lease.yml` khai `permissions: issues: write` và **cố ý KHÔNG khai `pull-requests`**
(nêu ngay ở đầu tệp như một lớp thu hẹp). `POST /repos/{o}/{r}/issues/{n}/comments` lên một PR
đòi `pull-requests: write` ⇒ 403. Trên `master` có **7** số hiệu `packet_issue` khác nhau, **1**
trong đó là PR (#214) — đơn vị: số hiệu riêng biệt, đếm trên `ops/leases/*.yaml` của `master`.

### Đ4 — chuỗi nhân quả đầy đủ, đo trên MỘT lượt chạy

Run `32464062577` in ra, theo đúng thứ tự:

```
lease slice-b-c-review-1-codex-20260821 ĐĂNG ĐƯỢC — issue #215 …
đã đăng comment 5367564833 lên #215
đã ghi posted_comment_id=5367564833 vào ops/leases/slice-b-c-review-1-codex-20260821.yaml
lease tri-thuc-review-1-codex-20260821 ĐĂNG ĐƯỢC — issue #214 …
gh: Resource not accessible by integration (HTTP 403)
##[error]Process completed with exit code 1.
```

Bước `ghi ngược comment id` có `if: env.DA_DOI == '1'`, nhưng bước **`đăng` đã ĐỎ** ⇒ bước ghi
ngược **không chạy** ⇒ `posted_comment_id` vừa ghi vào cây làm việc **mất theo runner**. Lượt kế
tiếp (`32473767302`) đọc lại tệp KHÔNG có `posted_comment_id`, đăng lại → comment `5368808554`,
rồi **chết đúng chỗ cũ** → lại mất. Đó là lý do trên `master` hôm nay có **4** tệp lease **không**
mang `posted_comment_id`:

```
ops/leases/ag-t0-01b-exec-1r2-antigravity-20260822.yaml
ops/leases/don-nhanh-base-review-6-claude-20260817.yaml
ops/leases/slice-b-c-review-1-codex-20260821.yaml
ops/leases/tri-thuc-review-1-codex-20260821.yaml
```

Bốn tệp ấy là **mìn**: nhánh `ops/**` nào chạm chúng cũng đăng lại một lần nữa.

## Bốn nguyên nhân, và cái nào là GỐC

| mã | nguyên nhân | vai |
|---|---|---|
| R1 | `packet_issue` có thể là PR; workflow không có `pull-requests` ⇒ 403 | **kích hoạt** |
| R2 | Một lease hỏng giết **cả lượt** TRƯỚC bước ghi ngược ⇒ mất bản ghi idempotent của lease **đã đăng** | **khuếch đại** |
| R3 | Bản ghi idempotent là `posted_comment_id` **trong tệp**, tức trạng thái **theo nhánh** | **gốc** |
| R4 | Với nhánh MỚI, mốc so là `merge-base(master, head)..head` ⇒ quét cả lease không do push này viết | **nới rộng** |

R3 là gốc vì nó là **đúng bài học đã có trong `CLAUDE.md`**: *hỏi chỗ TIỆN TAY thay vì hỏi chỗ
KẾT LUẬN ĐƯỢC GHI*. Câu hỏi thật là *"lease này đã đăng chưa"*; chỗ ghi kết luận là **comment
trên issue**, không phải một trường trong bản sao tệp của một nhánh.

## Quyết định đã chốt — và vì sao

| # | quyết định | căn cứ ĐO ĐƯỢC |
|---|---|---|
| Q1 | **KHÔNG thêm `pull-requests: write`.** Thay bằng: cổng **ĐO** số hiệu là Issue hay PR rồi **chặn sớm** lease trỏ PR. | Người giữ kho chọn phương án A, phiên 2026-08-21. Đ3: 6/7 số hiệu đã là Issue; #214 là ngoại lệ duy nhất. Thêm quyền là gỡ một lớp thu hẹp **cố ý** để phục vụ một ngoại lệ — đổi bề mặt vĩnh viễn lấy một ca. |
| Q2 | Idempotent **hỏi GitHub**, không hỏi tệp. Trước khi đăng: trên issue đã có comment mang dấu `**Lease \`<lease_id>\`**` chưa. | R3. Trạng thái theo nhánh không trả lời được câu hỏi xuyên nhánh. Đ1 là bốn lần nó trả lời sai. |
| Q3 | `posted_comment_id` **GIỮ LẠI**, hạ xuống mức *bằng chứng*, không còn là *chốt*. | Xoá nó là mất dấu vết ai đăng comment nào, mà dấu vết ấy đang được dùng trong hồ sơ. Giữ nhưng đừng để nó **một mình** quyết định. |
| Q4 | Một lease bị chặn **KHÔNG** được giết các lease còn lại — nhưng lượt chạy **vẫn phải ĐỎ**. | R2. "Cô lập" mà thành "nuốt lỗi" là biến một cổng đỏ thành cổng vắng mặt — đúng bệnh `[skip ci]` của PR #100. Xử hết, ghi ngược hết, rồi thoát khác 0. |
| Q5 | Bước ghi ngược chạy **kể cả khi bước đăng đỏ** (`if: always()`). | Đ4: đó chính là mắt xích làm mất `posted_comment_id` của lease **đã đăng thành công**. |
| Q6 | **KHÔNG** sửa R4 trong packet này. | Có Q2, mốc so rộng chỉ còn sinh thêm lời gọi `check` trả rc=9 — vô hại. Có Q4, một lease hết hạn lọt vào mốc so cũng không giết lượt chạy (đó là sự cố #195). R4 mất hết răng; sửa nó là tiêu ngân sách dòng của một packet `sensitive` cho một cải thiện thẩm mỹ. |
| Q7 | **KHÔNG** dọn 4 tệp lease thiếu `posted_comment_id` trên `master`. | Có Q2 thì chúng hết là mìn. Sửa tay 4 tệp là ghi một trường mà chú thích của chính nó ghi *"workflow ghi, ĐỪNG sửa tay"*. |
| Q8 | Executor: **`codex`**. Reviewer: **`claude`**. | L4: hình dạng kế thừa đếm được **5 lần, cùng một executor (`claude`)** — xem `hinh_dang_ke_thua`. Cùng lý lẽ đã dùng ở `#217`. |

## `review_class`

**`sensitive`** ⇒ `assurance_target` = **`cross_approved`**.

Chạm `.github/workflows/**` và `ops/lease_publish*.py` — tức **chính cổng đăng lease**, đường
authority theo §8. Phân theo **HẬU QUẢ**, không theo vị trí: bộ kiểm này là thứ duy nhất đứng
giữa một tệp YAML và một comment mang danh nghĩa kho.

## `write_set`

Đúng **ba** đường dẫn, cả ba đều **đã có**:

```
.github/workflows/ops-publish-lease.yml
ops/lease_publish.py
ops/lease_publish_test.py
```

Không ký tự đại diện. Không tệp nào khác được sửa — kể cả `ops/leases/*.yaml` (Q7), kể cả
`CLAUDE.md`, kể cả `ops/reviews/README.md`.

**Ngân sách kích thước — ADR-0044, packet `sensitive`: ≤ 3 tệp và ≤ 300 dòng THÊM.** Ba tệp là
**đúng trần**, không còn chỗ cho tệp thứ tư. Nền đo hôm nay: workflow 248 dòng · `lease_publish.py`
391 dòng · `lease_publish_test.py` 2.110 dòng, **42** ca.

**Nếu executor tính ra sẽ vượt 300 dòng thêm ⇒ DỪNG, xuất handoff, trả về người giữ kho.** Không
được tự chia nhỏ packet, không được tự nới trần. Chia packet là quyết định của người giữ kho
(§2) — và một packet `sensitive` âm thầm phình to là đúng thứ ADR-0044 sinh ra để chặn.

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm |
|---|---|
| Thêm `pull-requests: write` | Q1. Người giữ kho đã chọn hướng ngược lại. |
| Thu hẹp mốc so `merge-base..head` (R4) | Q6. Hết răng sau Q2 + Q4. |
| Sửa 4 tệp lease thiếu `posted_comment_id` | Q7. |
| Đăng lại lease `tri-thuc-review-1` lên #214 | #214 đã **đóng**. Muốn review gói ấy thì mở Issue mới — đó là việc của người giữ kho, không phải của bản vá. |
| Xoá 7 comment trùng đã đăng | Là sửa lịch sử công khai. Người giữ kho quyết; công cụ không tự dọn. |
| Đổi `dung_than()` | Dấu `**Lease \`<lease_id>\`**` mà Q2 dò **chính là** đầu ra của nó. Đổi nó là đổi mỏ neo trong cùng một lần vá, và không phép đo nào bắt được lệch ấy. |

## `muc_tieu`

Mỗi mục chiếu vào **một** đường dẫn trong `write_set` (L2).

1. **`ops/lease_publish.py`** — thêm lớp **ĐO LOẠI SỐ HIỆU**: `packet_issue` là ISSUE, là PR, hay
   **KHÔNG ĐO ĐƯỢC**. Ba trạng thái. `PR` ⇒ CHẶN kèm thông báo nêu thẳng *vì sao* (workflow không
   có `pull-requests`, quy ước là Issue). `KHÔNG ĐO ĐƯỢC` ⇒ **CHẶN**, không phải cho qua.
2. **`ops/lease_publish.py`** — thay chốt idempotent: hỏi **comment trên issue** xem đã có dấu
   `**Lease \`<lease_id>\`**` chưa. Có ⇒ `rc=9` (bỏ qua). Không ⇒ đăng được. **KHÔNG ĐO ĐƯỢC ⇒
   CHẶN**, không đăng. `posted_comment_id` trong tệp vẫn cho `rc=9` như cũ (Q3) — nó là lớp
   **thêm**, không phải lớp **thay**.
3. **`ops/lease_publish.py`** — cả hai lớp trên đi qua **đúng một mối nối** thay được trong test
   (đặt tên rõ ràng, ví dụ `GOI_GH`), mặc định là `gh api` thật. Mối nối ấy **KHÔNG** được chọn
   bằng biến môi trường hay bằng trường trong tệp lease: đầu vào do head kiểm soát mà chọn được
   nguồn dữ liệu của cổng là một lỗ authority.
4. **`ops/lease_publish.py`** — hai lớp mới chỉ áp khi đang chạy trong Actions (`GITHUB_ACTIONS`
   có mặt), đúng tiền lệ của lớp `GITHUB_ACTOR` ngay trong tệp. Khi **không** áp, `check` phải
   **NÓI RA** là lớp ấy vắng — không được im lặng để người đọc tưởng đã kiểm.
5. **`.github/workflows/ops-publish-lease.yml`** — vòng `đăng` **xử hết** danh sách: một lease bị
   chặn không dừng vòng; cuối vòng, nếu có bất kỳ lease nào bị chặn thì **thoát khác 0** (Q4).
6. **`.github/workflows/ops-publish-lease.yml`** — bước `ghi ngược comment id` chạy **kể cả khi
   bước đăng đỏ** (Q5), và vẫn giữ điều kiện "có gì để ghi".
7. **`ops/lease_publish_test.py`** — phản chứng cho cả sáu mục, dùng đồ giả **GIỮ TRẠNG THÁI**.

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo nào làm nó ĐỎ** (L3). Mọi đột biến chạy trên **bản sao tạm**.

| # | mục tiêu | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|---|
| T43 | 1 | Số hiệu là PR ⇒ CHẶN, và thông báo nêu `pull-requests` | coi PR như issue (bỏ phép đo loại) |
| T44 | 1 | Lời gọi đo loại **lỗi** ⇒ CHẶN, **không** đăng | coi lỗi là "chắc là issue" |
| T45 | 1 | Số hiệu là ISSUE ⇒ qua lớp này | chặn mọi số hiệu |
| T46 | 2 | Issue **đã có** comment mang dấu của `lease_id` ⇒ `rc=9`, **không** gọi API đăng | chỉ dò `posted_comment_id` như cũ |
| T47 | 2 | Dấu của **lease khác** trên cùng issue ⇒ **vẫn đăng được** | dò bằng substring lỏng thay vì khớp đúng `lease_id` |
| T48 | 2 | Lời gọi đọc comment **lỗi** ⇒ CHẶN, **không** đăng | coi lỗi là "chưa có comment nào" |
| T49 | 3 | Biến môi trường / trường trong lease **không** đổi được mối nối | cho một biến môi trường chọn mối nối |
| T50 | 4 | Không có `GITHUB_ACTIONS` ⇒ hai lớp vắng **và `check` in ra là chúng vắng** | im lặng bỏ qua |
| T51 | 5 | Danh sách 3 lease, lease **giữa** bị chặn ⇒ lease **thứ ba vẫn được đăng** *và* lượt chạy thoát **khác 0** | (a) `break` khi gặp lease chặn · (b) nuốt lỗi rồi thoát 0 — **hai đột biến riêng** |
| T52 | 6 | Bước đăng ĐỎ ⇒ bước ghi ngược **vẫn chạy** | bỏ `always()` |

Ngoài mười ca: **suite phải `rc=0` với `N/N` hai số bằng nhau** (nền hôm nay 42; sau packet là
52), và mỗi đột biến phải giết **đúng ca của nó**. Một đột biến giết nhiều ca ⇒ ca chưa tách đủ,
**phải nói ra**, không làm tròn thành đạt.

**Đồ giả phải mô phỏng TRẠNG THÁI, không diễn kịch bản** (bài học `ops-don-ref`: 40/40 trong khi
một đột biến xoá hẳn lệnh phá vẫn qua). Cụ thể ở đây: đồ giả `gh` giữ một **danh sách comment
theo issue**; "đăng" **thêm** vào danh sách ấy; T46 phải xanh vì lần hỏi thứ hai **thấy thứ lần
một vừa thêm**, không phải vì kịch bản bảo nó thấy.

**Tiêu chí KHÔNG đo được, ghi thẳng:** T51 và T52 đo **thân bước** trích từ chính tệp YAML
(tiền lệ `t32`), **không** đo một lượt chạy Actions thật. Xem `chua_do_duoc`.

## `hinh_dang_ke_thua`

Chép theo L4. **Hình dạng: *hỏi chỗ TIỆN TAY thay vì hỏi chỗ KẾT LUẬN ĐƯỢC GHI*.**

| lần | ở đâu | biểu hiện |
|---|---|---|
| 1 | 14-08-2026 (a) | "gate xanh" đọc thành "đã review" ⇒ merge #104, #105 khi codex đã đăng finding |
| 2 | 14-08-2026 (b) | `get_reviews` **rỗng** đọc thành "chưa review"; kết luận sạch nằm ở dòng `Reviewed commit:` |
| 3 | 14-08-2026 (c) | "PR xanh" đọc thành "master xanh"; ma trận Windows ghi ở `ci.yml`, không ở check của PR |
| 4 | thiết kế chốt idempotent | hỏi **tệp trong nhánh** thay vì hỏi **comment trên issue** — R3, chính lỗi packet này vá |
| 5 | 21-08-2026, phiên này | kết luận **"#214 là ISSUE đã đóng"** từ `issue_read` (API tiện tay) thay vì từ `html_url` (chỗ ghi câu trả lời). Sai; #214 là **PR**. Chỉ lộ khi đi đọc đúng trường. |

**Năm lần, cùng một tác giả (`claude`).** Lần 5 xảy ra **trong chính phiên soạn đặc tả này**, và
nó là lý do đặc tả có mục Đ3: câu hỏi "nếu thứ tôi đang tìm CÓ THẬT thì nó được ghi ở đâu" là
thứ duy nhất bắt được nó.

**Chốt cho packet này:** gặp hình dạng ấy **lần thứ sáu** ⇒ **DỪNG, không vá**, xuất handoff và
trả về người giữ kho. Q8 đổi executor sang `codex` chính là phép thử cho giả thuyết *"hình dạng
bám người viết, không bám bài toán"* — cùng phép thử đã chạy ở `#217`, ở đó `codex` **không**
mắc.

## `chua_do_duoc`

Ghi thẳng, không giấu sau chữ "có thể":

1. **Không có lượt chạy Actions THẬT nào chứng minh bản vá.** T51/T52 đo thân bước trích từ YAML;
   `t32` là tiền lệ, nhưng nó vẫn không phải một lượt chạy. Bằng chứng thật chỉ có được ở lần
   đăng lease KẾ TIẾP sau khi land.
2. **Khe giữa "hỏi comment" và "đăng comment" vẫn mở.** Hai lượt chạy song song trên hai nhánh
   `ops/**` khác nhau, cùng một lease, cùng hỏi trước khi ai kịp đăng ⇒ vẫn trùng. `concurrency`
   trong workflow gom theo `github.ref`, tức **không** gom hai nhánh khác nhau. Đây là **thu
   hẹp**, không phải **đóng** — nói đúng chữ ấy, đừng khai rộng hơn (chính hình dạng lỗi đã đếm
   5 lần ở packet `#213`).
3. **7 comment trùng đã đăng vẫn nằm đó.** Bản vá chặn lần sau, không dọn lần trước (Q7, ngoài
   phạm vi).
4. **`tri-thuc-review-1-codex-20260821` chưa từng được đăng**, và #214 đã đóng ⇒ gói "vòng lặp
   tri thức" **chưa có lease nào tới tay reviewer**. Đó là nợ vận hành, không phải nợ mã.
5. **Lớp mới không chạy khi gõ tay ở máy** (mục tiêu 4). Nó **khai** ra điều đó, nhưng người đọc
   vẫn có thể lướt qua dòng khai. Không có phép đo nào bắt được việc một con người không đọc.
