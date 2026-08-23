# ĐẶC TẢ PACKET — `LEASE-HOI-TOAN-KHO`

```yaml
packet_id: LEASE-HOI-TOAN-KHO
packet_issue: 244
revision: 1
review_class: sensitive          # ops/lease_publish.py = lease/publish authority (protocol §8), fail-closed
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: 08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9
```

## `nguon_cap_viec`

**KHÔNG có dòng kế hoạch nào cấp việc này** — đã tìm trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`
và `ops/HANG_DOI_PACKET.md`, cả hai đều không nhắc. Packet sinh từ phép đo của phiên `tra-luat-3a`
ngày 22-08-2026, nên nguồn là **sổ nợ + Issue**, ghi thẳng chứ không bịa một dòng kế hoạch:

- `ops/NO_KY_THUAT.md:1004` — nợ mục 18 `CHOT-CHONG-DANG-TRUNG-DOC-DAU-THEO-NHANH`
- nợ có tên `SO-LEASE-KHONG-NAM-MOT-CHO` (`CLAUDE.md`, mục *"SỔ LEASE KHÔNG NẰM MỘT CHỖ"*)
- Issue `#244`

## `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
```

Hai đường dẫn, liệt kê đủ, không ký tự đại diện.

**Kích thước dự kiến — có MỐC NEO đo được, chưa có số của chính packet này.** Phạm vi tương đương gần
nhất là `PLAT-X8` (PR #248), **cùng hai tệp**. Đo bằng khoảng commit, không mượn lời khai của ai:
`08bb4ecd..67a7fbe0` ⇒ **2 tệp / +265/−1**; `08bb4ecd..86a55663` (head sau hai bản vá P1) ⇒
**2 tệp / +313/−1**. Tức **một** mối quan tâm trên vùng này đã **VƯỢT** trần `sensitive` của ADR-0044
(**≤ 3 tệp / ≤ 300 dòng thêm**) — vượt 13 dòng, không phải "chạm".

Đó là mốc neo, **không** phải số của packet này: chưa có diff triển khai nên chưa suy ra được. **Phải đo lại
bằng `git diff --numstat` trước vòng review**, và vượt trần thì dừng để revision thiết kế hoặc khai lý do
theo ADR-0044 — chưa có số đo thì chưa được cấp lease thi hành.

Mốc neo ấy cũng là lý do packet này **không gộp** nợ của packet kia: xem `ngoai_pham_vi`.

**Write set này ĐANG BỊ GIỮ lúc đóng băng đặc tả.** Đo 16:5xZ 22-08-2026 trên 164 ref
(`yaml.safe_load`, fail-close): `plat-x8-exec-2`, `-2r2`, `-2r3` khai đúng hai đường dẫn này, hết hạn
`2026-08-23T14:10:00Z`, và `PLAT-X8` đang chạy thật (PR `#248`, +265/−1 trên đúng hai tệp).

**Đo lại 18:2xZ trên 165 ref: `CÒN_HẠN` lên 5, người giữ vẫn 1.** Chuỗi kéo dài thêm `-2r4` `-2r5`; hạn
**không đổi**. Năm bản ghi, một thẩm quyền — xem `A2c`. Bài học đi kèm: lượt fetch trước đó **mù đúng một
ref** (`claude/ci-bang-phu-thuoc-bam` có trên máy chủ, thiếu ở đệm cục bộ), và thứ bắt được là phép so hai
nguồn ở `M2` chứ không phải mắt người — nên `164` ở trên là số ref **đo được lúc ấy**, không phải số ref
tồn tại. Chính vì vậy `M2` phải chạy **trước** mỗi lượt quét, không phải chạy một lần rồi tin mãi.
**Lease cho packet này chỉ được cấp SAU khi `PLAT-X8` nhả** — land hoặc rút. Đặc tả không phải lease
(protocol §7), nên đóng băng trước là hợp lệ; bắt tay trước thì không.

Cùng lúc còn **8** lease `CÒN_HẠN` khác giao write set (đo **17:38Z**), thuộc `LEASE-DANG-*` — packet ấy
**đã land** (`#238` qua PR `#246`) nên chúng là quyền ghi **đã tiêu**, không phải vật cản. Chúng không tự
khai điều đó; xem `chua_do_duoc`.

**Con số 8 PHÂN RÃ theo giờ — đừng đọc nó như một hằng số.** Cùng phép quét cho **9** lúc 16:5xZ và **8**
lúc 17:38Z, chỉ vì lease hết hạn dần. Bản đầu của mục này đóng băng "9" không kèm thời điểm, rồi
`EVIDENCE.md` ghi "6", rồi đo lại ra "8" — **ba số cho một thứ**, và cross-review lượt 2 bắt đúng chỗ đó
(`dem-lease-dang-sai`). Thứ **không** phân rã là bất biến bên dưới: **`PLAT-X8` đang giữ cả hai đường dẫn**.
Neo quyết định vào bất biến ấy; con số chỉ để đối chiếu, và phải đo lại ngay trước khi cấp lease.

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm ở đây |
|---|---|
| Cổng `t33` đòi `shellcheck` | Packet riêng `T33-DOI-SHELLCHECK`. Chạm tệp khác (`ops/cai_actionlint.sh`), và **không dùng** năng lực "hỏi toàn kho" — gộp vào chỉ làm packet này vượt trần ADR-0044 |
| Đường **thu hồi** lease đã tiêu | Nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`. Packet này chỉ **ĐỌC ĐÚNG** trạng thái, không chế cơ chế huỷ. Cho một packet thu hồi lease của packet khác là dựng đường huỷ đơn phương |
| Sửa dữ liệu 6 lượt đăng thừa đã có | Là **hiện vật lịch sử**. Sửa hậu kỳ làm mất bằng chứng của chính nợ này |
| Đoán quan hệ `thay_the_lease` / `tiep_tuc_lease` | Hai trường ấy trỏ **NGƯỢC** (mới → cũ): muốn biết lease `X` đã chết chưa thì phải quét **mọi** lease xem có cái nào trỏ về `X`. Sửa hướng con trỏ là đổi lược đồ lease — việc khác, packet khác. **`da_bi_thay_the` KHÔNG thuộc nhóm này** — xem `A2c` |

## `muc_tieu`

Mỗi mục chiếu vào **một** đường dẫn trong `write_set` (L2).

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Lệnh `ai-dang-giu <đường-dẫn>`: quét **mọi ref**, trả **ba** trạng thái `CÒN_HẠN` / `HẾT_HẠN` / `KHÔNG_XÁC_ĐỊNH`, dùng bộ phân tích cấu trúc (`yaml.safe_load`), **fail-close**; lease `CÒN_HẠN` mang `da_bi_thay_the` bị **loại khỏi tập người giữ** nhưng vẫn được **in ra** kèm nhãn | `ops/lease_publish.py` |
| **M2** | Trước khi quét, `ai-dang-giu` **so hai nguồn** — `git ls-remote --heads` (máy chủ) với `git for-each-ref` (đệm) — **so bằng TẬP TÊN**, loại ref tượng trưng; thiếu ở phía cục bộ ⇒ `KHÔNG_XÁC_ĐỊNH` | `ops/lease_publish.py` |
| **M3** | Chốt chống đăng trùng (`:236-241`) đọc dấu **TOÀN KHO** thay vì từ bản lease trong cây đang chạy | `ops/lease_publish.py` |
| **M4** | Ca `rXX_` + đột biến cho M1–M3 | `ops/lease_publish_test.py` |

**Đơn vị của mọi con số trong đặc tả này (L1):** "lease" = **cặp (blob, đường dẫn) duy nhất** trên toàn
bộ ref, trừ khi ghi khác. Đếm theo **đường dẫn** cho số khác — đo 18:4xZ 22-08 trên 165 ref: **120** cặp
/ **110** đường dẫn, chênh **10** là **phiên bản thừa**, không phải 10 tệp. Con số nào cũng phải đi kèm
đơn vị. (Bản đầu ghi `117 / 100`: cùng chênh 10, nhưng **cả hai số hạng đã phân rã** — cross-review lượt
4 đo lại mới thấy. Chênh đúng mà số hạng sai thì phép đếm không tái lập được.)

## `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó **ĐỎ** (L3).

**M1** — `A1` Gọi `ai-dang-giu ops/lease_publish.py` trên kho giả có **hai lease còn hạn ở hai ref khác
nhau**, một lease hết hạn và một lease cho đường dẫn khác ⇒ in **đúng tập hai `lease_id` còn hạn của đường
dẫn được hỏi, không thừa không thiếu**, và thoát **khác 0**. ĐỎ khi: đột biến dừng sau lease còn hạn đầu
tiên, nhận nhầm lease hết hạn/khác đường dẫn, bỏ một trạng thái khỏi bảng phân loại, hoặc đổi `sys.exit`
thành `0`.
`A2` Bơm một tệp lease **YAML hỏng** ⇒ `KHÔNG_XÁC_ĐỊNH` **và** mã thoát khác 0. ĐỎ khi: đột biến thay
`raise`/`exit` bằng `|| echo` — đúng cách hỏng lượt 3 của bộ quét hand-roll (fail-**OPEN** trong chốt viết
ra để fail-**CLOSE**).
`A2b` Bơm một lease có `lease_expires_at_utc` **đã qua** ⇒ phân loại **`HẾT_HẠN`**, và lease ấy **không**
xuất hiện trong danh sách chặn. ĐỎ khi: đột biến gộp nhánh `HẾT_HẠN` vào `CÒN_HẠN`, **và** đột biến gộp nó
vào `KHÔNG_XÁC_ĐỊNH` — **hai** đột biến riêng, vì mỗi cái hỏng về một phía.
**Vì sao `A2b` phải có (finding P2 cross-review lượt 1, PR #250):** `A1` chỉ cấp lease đang hoạt động, `A2`
chỉ phủ đường không xác định. Thiếu `A2b` thì một cài đặt **dán nhãn mọi lease hết hạn thành `CÒN_HẠN` hoặc
`KHÔNG_XÁC_ĐỊNH`** vẫn thoả trọn bộ fixture, và câu *"bỏ nhánh `HẾT_HẠN` làm `A1` đỏ"* ở bản đầu là **sai** —
`A1` không đổi màu. `M1` hứa ba trạng thái thì nghiệm thu phải chạm đủ ba.

`A2c` **LEASE CÒN HẠN MÀ ĐÃ CHẾT.** Bơm một chuỗi thay thế: lease `L1` còn hạn mang
`da_bi_thay_the: L2`, và `L2` còn hạn **không** mang trường ấy — cả hai khai cùng đường dẫn được hỏi. ⇒
tập **người giữ** chỉ có `L2`; `L1` vẫn **được in** kèm nhãn đã-bị-thay-thế (im lặng bỏ nó đi thì người
đọc tưởng phép quét sót). ĐỎ khi: đột biến bỏ phép đọc `da_bi_thay_the` (⇒ `L1` lọt vào tập người giữ),
**và** đột biến biến nó thành phép **loại bỏ khỏi đầu ra** (⇒ `L1` biến mất khỏi bản in) — **hai** đột
biến riêng, vì "không phải người giữ" khác "không tồn tại".

**Vì sao `A2c` phải có — đo được lúc 18:2xZ 22-08-2026, SAU khi đặc tả đã đóng băng.** `PLAT-X8` đi từ
**3** lease `CÒN_HẠN` lên **5** trong khoảng một giờ, mà số **người giữ thật vẫn là 1**: `exec-2` → `-2r2`
→ `-2r3` → `-2r4` → `-2r5`, mỗi cái trỏ tới cái sau bằng `da_bi_thay_the`, chỉ `-2r5` không có trường ấy.
Hạn không đổi (`2026-08-23T14:10:00Z`). Bộ quét hand-roll dùng suốt phiên này **đếm cả 5** — nó chưa từng
đọc trường đó. Một `ai-dang-giu` xây theo bản đặc tả **trước** bản vá này sẽ báo *"5 lease đang giữ"* khi
có **1**, tức **chặn nhầm** một packet hợp lệ.

Đây là ảnh gương của P1 lượt 2 (`write-set-khong-ranh`): lần ấy lời khai **rộng hơn** phép đo và cho
qua nhầm; lần này phép đo **rộng hơn** sự thật và chặn nhầm. Cùng một gốc — *đếm bản ghi thay vì đếm
thẩm quyền*.

**Trường này MỚI TINH, và chính nợ của packet này đẻ ra nó.** `da_bi_thay_the` xuất hiện lần đầu ở
`0d35e44` (22-08-2026, lease `PLAT-X8` revision 2), mang `schema_version: 2`, và lý do nó tồn tại nằm
nguyên văn trong tệp lease: chốt chống đăng trùng của `ops/lease_publish.py` trả `rc=9` cho một
`lease_id` đã có `posted_comment_id`, **nên executor không sửa được tệp lease cũ — phải đúc `lease_id`
mới** rồi đánh dấu cái cũ đã chết. Tức: khuyết tật `M3` sinh ra vòng xoay id, vòng xoay id thổi phồng
số lease, và `da_bi_thay_the` là miếng vá thủ công cho hệ quả ấy. Packet này chạm **cả hai đầu** của
cùng một dây chuyền — sửa `M3` sẽ làm vòng xoay thưa đi, nhưng **không** làm `A2c` thừa: lease đã đúc
rồi thì vẫn nằm đó.

**Hệ quả cho người thi hành, phải đọc trước khi cài `A2c`:** đây là **quy ước đang hình thành**, không
phải lược đồ ổn định — **4/120** blob mang nó, tất cả đúc trong cùng một ngày, tất cả bởi **một** packet.
Vậy nên `ai-dang-giu` **không được** coi *vắng `da_bi_thay_the`* là bằng chứng *"còn hiệu lực"*: tuyệt
đại đa số lease trong kho vắng nó vì trường chưa tồn tại lúc chúng được đúc, chứ không phải vì chúng
còn sống. Đọc trường ấy chỉ được phép **thu hẹp** tập người giữ, không bao giờ **mở rộng** — đúng chiều
fail-close.

**Vì sao chuyện này lọt qua ba lượt review:** `ngoai_pham_vi` gạt `da_bi_thay_the` ra cùng rổ với
`thay_the_lease`/`tiep_tuc_lease`, lấy lý do *"trỏ NGƯỢC, đọc xuôi không suy ra được"*. Đo thật thì **hai
họ trỏ ngược chiều nhau**: `r5.thay_the_lease = r4` (mới → cũ, muốn biết `r4` chết chưa phải quét cả kho),
còn `r3.da_bi_thay_the = r4` (**cũ → mới**, mở đúng một tệp là biết). Lý do loại trừ **đúng cho một
trường và sai cho trường kia** — và vì hai tên nằm cùng một ô bảng, không ai tách ra kiểm. Toàn kho có
**4/120** blob lease mang `da_bi_thay_the`, và cả 4 là chuỗi đang chặn chính write set này.

**M2** — `A3` Giả một `ls-remote` trả **thừa một nhánh** so với `for-each-ref` ⇒ `KHÔNG_XÁC_ĐỊNH`.
`A4` Giả chiều ngược lại (thừa ở **cục bộ**) và đặt một lease còn hạn trên một ref chung ⇒ **KHÔNG** báo
động vì ref cục bộ thừa, nhưng vẫn in lease còn hạn và thoát khác 0. ĐỎ khi: đột biến trả thành công sớm
khi thấy ref cục bộ thừa, làm mất lượt quét lease. `A5` Bơm một ref tượng trưng kiểu `origin/HEAD`, đồng
thời đặt một lease còn hạn trên một ref thường ⇒ **không** báo động vì ref tượng trưng, nhưng vẫn in lease
còn hạn và thoát khác 0. ĐỎ khi: bỏ bước loại ref tượng trưng, hoặc trả thành công sớm khi gặp ref tượng
trưng làm mất lượt quét lease.

`A6` **LỰC LƯỢNG BẰNG NHAU, TÊN KHÁC NHAU** — máy chủ và cục bộ cùng `n` ref, nhưng một nhánh cục bộ **cũ**
đã bị xoá trên máy chủ và một nhánh **mới** trên máy chủ chưa fetch. ⇒ **`KHÔNG_XÁC_ĐỊNH`**. ĐỎ khi: đột
biến đổi phép so **tập** thành so `wc -l`.

**`A6` là fixture DUY NHẤT giết được đột biến ấy, và bản đầu của đặc tả này khai sai điều đó** (finding P1
cross-review lượt 1, PR #250). `A3` và `A4` mỗi cái lệch lực lượng đúng **một**, nên một cài đặt **đếm** vẫn
phân biệt được hai chiều (`n_máy_chủ > n_cục_bộ` ⇒ kêu; ngược lại ⇒ im) và thoả cả hai. Câu *"cả A3 lẫn A4
phải đổi màu"* vì thế **sai**.

Đắng ở chỗ: ca lực-lượng-bằng-nhau **chính là** lý do (a) mà cross-review PR #243 đã nêu và tôi đã chép vào
`CLAUDE.md`. Tôi viết nó thành **văn xuôi doctrine** rồi **không** biến nó thành fixture — đúng bài học
*"NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI"*, lần này ở dạng *"viết vào doctrine
mà không viết vào nghiệm thu"*.

**M3** — `A7` Dựng hai nhánh mang **cùng một** `lease_id`, một bản đã có `posted_comment_id`, bản kia
chưa, cùng một lease mồi có `lease_id` **khác** và cũng đã có `posted_comment_id`; chạy cổng trên bản chưa
có ⇒ **`RC_DA_DANG` (9)** cho đúng `lease_id` được hỏi. ĐỎ khi: đột biến đưa phép đọc dấu về chỉ đọc tệp
cục bộ, hoặc coi bất kỳ `posted_comment_id` nào trong kho là dấu của lease được hỏi. **Ca này là phản
chứng của chính nợ mục 18**: không có nó thì không biết đang đo cổng hay đo thứ khác.

**M4** — `A8` Mỗi ca trong `A1` `A2` `A2b` `A2c` `A3` `A4` `A5` `A6` `A7` — liệt kê từng cái, vì `A2b`
và `A2c` không nằm trong dãy số `A1`–`A7` và một dãy viết tắt là chỗ ca lẻ đi lạc — có **ít nhất một đột biến trong mã
sản phẩm `ops/lease_publish.py`** khiến nó đổi màu. Bộ chạy ghi mỏ neo + thay thế của từng đột biến, xác
nhận mỏ neo xuất hiện đúng một lần và xác nhận tệp sau thay thế khác bản gốc, rồi in **cả hai** số (số
đột biến mã sản phẩm đã chạy · số đột biến bị giết) — hai số **bằng nhau**. ĐỎ khi: runner chỉ sửa assertion
trong test, một đột biến không áp được/sống sót, hoặc hai số lệch. Nhắc `t97`: đột biến có thể **chưa từng
chạy** do va chạm `.pyc`; bộ chạy phải tắt ghi bytecode và dùng tên tệp riêng từng đột biến.

## `hinh_dang_ke_thua`

**Nguồn là BIÊN NHẬN, không phải thân Issue** — bản đầu của đặc tả này chép từ thân Issue `#238`
và cross-review lượt 1 (PR #250, P2) bác đúng chỗ đó. Đo trên `ops/reviews/lease-dang-review-5-claude-verdict.receipt.yaml`,
mục `bo-dem-sau-luot-5`:

| | hình dạng | số |
|---|---|---|
| A | lời khai rộng hơn phép đo | **6** |
| B | mượn tiền lệ mà không đo xem nó áp dụng được không | 2 |
| C | phản chứng bắt buộc còn thiếu | 1 |
| D | đặt câu hỏi kiểm chứng ở sai độ phân giải / sai pha | 3 |
| E | khoá theo thứ liệt kê được thay vì theo thứ thật sự chặn | 2 |
| **F** | land trên một nền, đo trên nền khác | **KHÔNG CÓ TRONG BIÊN NHẬN NÀO** |

Hai đính chính so với bản đầu, cả hai đo được:

- **`A` là 6, không phải 7.** Thân Issue ghi 7; biên nhận ghi 6. Biên nhận là hiện vật bền, thân Issue sửa
  được sau lưng — **biên nhận thắng**.
- **`F` không tồn tại trong hồ sơ bền.** Quét **39** biên nhận trên `master` (đo 18:4xZ 22-08; bản đầu
  ghi 37 — mẫu số đã phân rã, kết luận `0` thì không đổi): **0** cái có bộ đếm `F`. Nó chỉ có trong thân
  Issue `#238`.

**Vì sao chỗ này nghiêm trọng hơn một con số lệch:** bản đầu dùng `F = 2` để tuyên bố *"F lần 3 ⇒ DỪNG"* —
tức lấy một số **không có hiện vật** làm **cổng dừng thi công**. Đã bỏ câu ấy. Yêu cầu bằng chứng hai nền
đứng bằng chính `B5`, không cần mượn một bộ đếm chưa ai ghi.

**`A = 6` vẫn là cao nhất, và đúng chỗ nguy hiểm của packet này**: mọi mục tiêu đều là "đọc trạng thái rồi
khai" — đúng loại việc đẻ ra hình dạng A.

## `chua_do_duoc`

1. **Hại thực tế của 6 lượt đăng thừa.** Chưa đếm số comment thật trên PR đích, chưa biết lượt sau có ghi
   đè lượt trước không. REST tới `repos/…` bị proxy chặn 403 từ container này.
2. **Bằng chứng byte thật trên GitHub.** Đọc thân comment/issue qua MCP **bị chuẩn hoá thực thể HTML**
   (đo bởi phiên `#238`). Phép đo *"chỉ khác đúng một dòng `posted_comment_id`"* của packet này **KHÔNG**
   đi qua đường ấy — nó chạy `git cat-file -p` trên blob cục bộ, đã chạy lại và xác nhận — nhưng ai
   đối chiếu lại bằng thân comment sẽ thấy khác, và khác đó là tạo tác của công cụ đọc.
3. **Vì sao chỉ `plat-x5-*` dính.** Đo 18:4xZ 22-08: **100** `lease_id` có `posted_comment_id`, trong đó
   **3** mang **nhiều hơn một** id — cả ba là `plat-x5-*`. (Bản đầu ghi `3/90`: tử số đúng, **mẫu số đã
   phân rã**.) Chưa phân định được là do `PLAT-X5` chạy nhiều lượt review hơn hay do nhánh của nó
   fan-out rộng hơn.
4. **8 lease `LEASE-DANG-*` "đã tiêu" không tự khai điều đó.** Kết luận ấy dựng bằng tay từ hiện vật trên
   master (`kiem_github` = 1, bộ test 73 ca). Không trường nào trong tệp lease nói ra, và trạng thái Issue
   cũng không.
5. **`da_bi_thay_the` chưa được chuẩn hoá ở đâu cả.** Quét `docs/` · `.claude/skills/` · `ops/lease_publish.py`
   ⇒ **0** lần nhắc; nó chỉ tồn tại trong 4 tệp lease do `PLAT-X8` đúc, mang `schema_version: 2`. Nên chưa
   đo được: quy ước này sẽ được protocol thu nhận, hay sẽ chết cùng packet ấy. `A2c` vì thế đọc trường theo
   chiều **thu hẹp** tập người giữ (xem lý do ở `A2c`); nếu protocol sau này chuẩn hoá nó thì tiêu chí không
   phải sửa, chỉ mạnh thêm.
