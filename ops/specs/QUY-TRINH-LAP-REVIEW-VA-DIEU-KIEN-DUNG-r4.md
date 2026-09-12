# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 4)

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp523`.
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **4** · `generation`: 3 · soạn **12-09-2026**
- `thay_the_cho`: **revision 3** (`spec_sha256`
  `40f39595e0750c84daf7a78232f860ad3724b3e9826f2d361f35cb94ab56fc4b`, đã cấp lease gen 2, đã chạy hai
  lượt cross-review và đã ghi hai biên nhận vào kho ở `6b46012`). r3, r2 và r1 **giữ nguyên trên đĩa
  làm hồ sơ**.
- `depends_on`: **`[]`** · `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**

## `nguon_cap_viec`

Kế thừa r1, r2, r3. Cộng chỉ thị MỚI của chủ kho 12-09-2026 — **chọn phương án (B) hoà giải với PR
#521** — bản chiếu ở
[#issuecomment-5647027599](https://github.com/ducthangho/tra-luat/pull/529#issuecomment-5647027599),
trả lời bản đo xung đột ở
[#issuecomment-5647008786](https://github.com/ducthangho/tra-luat/pull/529#issuecomment-5647008786).

## VÌ SAO PHẢI CÓ r4 — một phép đo, và nó KHÔNG phải lỗi của bên nào

**PR #521 land vào master lúc `2026-09-12T15:31:01Z` và sửa `+247/−147` đúng một tệp:
`.claude/skills/cross-review/SKILL.md`** — tệp mà lease #523 giữ từ `2026-09-12T08:14:57Z`. Số đo:

| phép đo | kết quả |
|---|---|
| `merge-base --is-ancestor origin/master 6b46012` | `rc=1` ⇒ CÓ DRIFT, master đi `85fcbf8 → dc02c9b`, 12 commit |
| `git merge-tree --write-tree 6b46012 dc02c9b` | `rc=1`, `CONFLICT (content)` — **2 hunk**, **82 dòng** trong vùng xung đột |
| delta của #521 trên tệp ấy | `+247 / −147` |
| delta của #523 trên tệp ấy | `+221 / −245` |
| 10 mẫu văn bản của `A1`+`A2` đo trên master sau #521 | **8 vắng / 2 còn** (`review_class`, `sensitive`) |

**Hai hunk là hai chỉ thị TRÁI NHAU, và cả hai đều đúng theo mandate của mình:**

- **#521** (8 lượt cross-review, land `approve` 0/0/0) được giao *gỡ 60 mệnh đề doctrine* — biến
  adapter thành **con trỏ**. Nó thay cả hai vùng bằng một dòng trỏ `§`.
- **#523** (`M1`/`M2`/`M3`) được giao **viết** bảng điều kiện dừng và `BẢNG LỚP` **vào** adapter.

Nên không có phía nào "sai": ba lối ra cơ học đều **mất hành vi được giao** — lấy `theirs` mất trọn
`M1`–`M3`; lấy `ours` hoàn nguyên việc #521 trả 8 lượt review để làm; giữ cả hai đưa lại vào adapter
đúng loại prose mà #521 gỡ, và `doctrine-scan` **không** bắt được (chính lượt 2 của #523 đã đo và đã
viết vào skill: cổng ấy xanh chỉ chứng minh **các cụm CÓ TRONG DANH SÁCH** không bị chép).

Chủ kho chọn **(B)**: giữ **cấu trúc con trỏ** của #521, đưa phần **BẮT BUỘC** của #523 về dạng
**ngắn nhất còn đủ răng**, mỗi mục kèm con trỏ `§` thay vì diễn giải lại. Đó là **đổi acceptance**
(`A1`/`A2` của r1–r3 đòi nội dung nằm TRONG adapter), nên `§3.2` và `§5` đòi **revision mới,
generation mới, cấp lại lease**. r3 không được nới tại chỗ; nó bị **thay**.

**Vụ #521 ghi vào đường dẫn đang bị giữ: chủ kho chốt CHỈ GHI NHẬN.** Quét nội dung mọi
`ops/leases/*` trên **358 ref** ⇒ 36 tệp khớp đường dẫn, **không tệp nào thuộc #521**; `ai-dang-giu`
trả `NGƯỜI_GIỮ 1` và đó là lease của #523. Hai khả năng — #521 không có lease, hoặc lease của nó sống
trên một nhánh `ops/**` đã xoá — **không phân biệt được** từ dữ liệu hiện có. Trạng thái đúng là
**KHÔNG ĐO ĐƯỢC**; nợ `SO-LEASE-KHONG-NAM-MOT-CHO` nay có một thiệt hại đo được. **KHÔNG** mở packet
cho nó, và **KHÔNG** đi tìm thêm — đó là chỉ thị, ghi ra đây để lần sau không ai đọc bản đo thành một
kết luận.

## `nang_tran` — kế thừa r3, KHÔNG nâng thêm

```yaml
nang_tran:
  same_failure_limit: 2 -> 10
  attempts_limit: 3 -> 10
  ai_nang: ducthangho
  can_cu: https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5646812840
  xac_nhan_khuon: 'chủ kho xác nhận "Nâng như #522" — cùng khuôn đã nâng cho #522'
  r4_khong_nang_them: 'r4 KHÔNG xin thêm lượt nào; nó chỉ đổi acceptance theo (B)'
```

Nâng này **KHÔNG** chữa lớp nào; nó chỉ cho phép **đo tiếp**.

## `review_class` và ngưỡng — `ADR-0044` nói cho chật

`sensitive` ⇒ ≤ **3 tệp**, ≤ **300 dòng thêm**. Packet này giữ **đúng hai** tệp SẢN PHẨM.

`ops/reviews/` là **hiện vật review bất biến** — `ci.yml` khai thẳng chúng *"không phải mã sống để CI
chạy"* — nên **KHÔNG** tính vào phép đếm tệp sản phẩm của `ADR-0044`, đúng tiền lệ spec r3 của #522.

**Dòng thêm của phép MERGE không tính vào trần 300.** Một merge commit mang vào toàn bộ delta của
#521; đếm nó thành "dòng thêm của packet" là biến trần `ADR-0044` thành hàm số của việc người khác
làm. Phép đếm đúng là `git diff --numstat <merge commit>..<head>` cho phần packet viết SAU merge, cộng
`git diff --numstat <base trước merge>..<head trước merge>` cho phần đã viết trước — và `A9` dưới đây
nói thẳng cách đo.

## `write_set` — GIỮ NGUYÊN ba đường của r3, không thêm

| # | đường dẫn | kiểu | vì sao |
|---|---|---|---|
| 1 | `.claude/skills/cross-review/SKILL.md` | exact | bên SINH bảng phân hạng và verdict; **cũng là tệp #521 vừa sửa** |
| 2 | `.claude/skills/work-packet/SKILL.md` | exact | bên ĐỌC bảng ấy và quyết vá / merge / dừng |
| 3 | `ops/reviews/` | prefix | `VERDICT.md` + `*.receipt.yaml` + hàng Mục lục của các lượt |

(B) **không** cần đường nào mới. **KHÔNG** đụng `docs/PROTOCOL_DA_PHIEN.md`, `.claude/hooks/**`,
`packet_loop.py`, r1/r2/r3 của chính đặc tả này, hay `VERDICT.md` đã giao.

## `ngoai_pham_vi`

Giữ **nguyên sáu mục của r3**. Thêm:

7. **KHÔNG hoàn nguyên bất kỳ phần nào của #521.** Phép merge chỉ được ĐƯA LẠI phần `A1'`/`A2'` dưới
   đây đòi; mọi dòng khác của #521 giữ **nguyên byte**. Đây là chốt có thể ĐO, xem `A17`.
8. **KHÔNG chép lại nội dung `§` mà con trỏ đã trỏ tới.** Nếu một mục của `A1'`/`A2'` có thể thay bằng
   một con trỏ mà **vẫn** làm ĐỎ được các đột biến đích, thì nó **phải** là con trỏ.

## `muc_tieu`

`M1`–`M12` **giữ nguyên từ r3** (r3 giữ từ r2, r2 giữ `M1`–`M7` từ r1 — **đọc r1 cho định nghĩa đầy
đủ, đừng đọc dòng liệt kê tóm tắt**; chính chỗ ấy đã sinh 1 P1 + 4 P2 ở lượt 1). r4 thêm:

| # | mục tiêu | chiếu vào |
|---|---|---|
| M13 | **Hoà giải, không chọn phía**: `cross-review/SKILL.md` sau merge giữ cấu trúc con trỏ của #521 VÀ mang phần bắt buộc của #523 ở dạng tối thiểu. Không hoàn nguyên #521, không bỏ `M1`–`M3`. | 1 |
| M14 | **Tối thiểu phải CHỨNG MINH được là còn răng**: mỗi chốt rút gọn phải có một đột biến làm tiêu chí đích ĐỎ. Không được nhận *"ngắn hơn mà vẫn đủ"* bằng lời. | 1, 2 |

## `nghiem_thu`

`A3`–`A16` **giữ nguyên từ r1, r2, r3**. `A1` và `A2` **VIẾT LẠI**; `A17`, `A18` **MỚI**.

**A1' (M1, M2, M13) — bảng điều kiện dừng: ba lớp PHÂN BIỆT ĐƯỢC, ở dạng tối thiểu.**
`cross-review/SKILL.md` phải có bảng ánh xạ `review_class → điều kiện dừng` với **đúng ba** hàng; hàng
`sensitive` phải nói **`approve`**, **không** nói *"0 P1 + 0 P2"*. Bảng được phép **rút ngắn tối đa**
và trỏ `§3.2` cho định nghĩa trục `review_class` — điều `A1` của r1 đòi mà r4 **bỏ** là phần diễn giải
văn xuôi quanh bảng; điều r4 **giữ** là chính bảng và câu phân biệt hàng `sensitive`.
**Phép làm ĐỎ (bắt buộc chạy, cả ba):** đổi hàng `sensitive` thành *"hết P1, P2"* ⇒ ĐỎ · gộp `routine`
với `systemic` ⇒ ĐỎ · **thay cả bảng bằng một con trỏ trần** (`"điều kiện dừng: xem §12"`) ⇒ **ĐỎ**.
Phép đo: parse bảng Markdown, đòi tập `review_class` **bằng** `{routine, systemic, sensitive}` và ba
giá trị điều kiện **đôi một khác nhau**.
Ca thứ ba là ca phân biệt r4 với (A): nếu con trỏ trần cũng ĐẠT thì `A1'` không đo gì, và (B) đã tụt
thành (A) mà không ai nói ra.

**A2' (M3, M13) — `BẢNG LỚP` và đơn vị đếm: nghĩa vụ, ở dạng tối thiểu.**
`cross-review/SKILL.md` phải đòi verdict mang mục `BẢNG LỚP` với **ba** cột
`(lop_loi, các slug thuộc lớp, bản vá theo lớp | lý do vá lẻ)`, và phải khai **đơn vị đếm**:
`so_p1`/`so_p2`/`so_p3` đếm **LỚP**, `so_the_hien` đếm **THỂ HIỆN**, `findings_ids` là slug **LỚP**.
`work-packet/SKILL.md` phải đòi vòng vá **ĐỌC** bảng ấy trước khi sửa dòng nào.
Được phép trỏ `§8`/`§12` cho ngưỡng và cho định nghĩa P1/P2/P3; **không** được chép số trần.
**Phép làm ĐỎ (bắt buộc chạy, cả bốn):** bỏ cột `bản vá theo lớp` ⇒ ĐỎ · bỏ bảng đơn vị đếm ⇒ ĐỎ ·
bỏ câu *mỗi finding thuộc đúng một lớp* ⇒ ĐỎ · thay cả mục bằng một con trỏ trần ⇒ **ĐỎ**.

**A17 (M13, ngoại phạm vi 7) — phép merge KHÔNG hoàn nguyên #521, và điều đó ĐO ĐƯỢC.**
Trên head sau merge, `git diff dc02c9b..<head>` chỉ được chứa:
(a) các dòng `A1'`/`A2'` đòi, trong **đúng hai** vùng đã xung đột; (b) delta của `work-packet/SKILL.md`
mà #521 không đụng; (c) `ops/reviews/**`.
**Phép làm ĐỎ:** bất kỳ dòng nào của #521 bị xoá mà `A1'`/`A2'` **không** đòi ⇒ ĐỎ. Đo bằng
`git diff dc02c9b..<head> -- .claude/skills/cross-review/SKILL.md` rồi soi **từng dòng `−`**: mỗi dòng
`−` phải nằm trong một trong hai vùng xung đột và phải có lý do thuộc `A1'`/`A2'`. Số dòng `−` ngoài
hai vùng ấy phải là **0**.

**A18 (M14) — "tối thiểu còn răng" là PHÉP ĐO, không phải lời khai.**
Mọi phép làm ĐỎ của `A1'` và `A2'` (**bảy** ca) phải được **chạy thật**, mỗi ca trên **bản sao tạm**,
phục hồi byte gốc sau mỗi lần, và kết quả ghi vào `EVIDENCE.md` kèm lệnh + output.
**Phép làm ĐỎ của chính `A18`:** một ca nào đó **KHÔNG** làm tiêu chí đích đỏ ⇒ chốt tương ứng **chưa
có răng** ⇒ `A18` ĐỎ, và phải nói thẳng chốt nào chứ không gộp thành *"đã đo"*.
**Đối chứng DƯƠNG bắt buộc:** bản gốc (chưa đột biến) phải ĐẠT cả bảy tiêu chí. Thiếu đối chứng dương
thì bảy ca đỏ không chứng minh được chúng đỏ vì **chốt** chứ không vì phép đo hỏng — đúng bài học
*"đột biến bị giết không phải đột biến bị giết ĐÚNG LÝ DO"*.

**A9 viết lại cho phép MERGE:** hai phép đếm riêng, đừng gộp.
- `git diff --numstat <base trước merge>..<head trước merge>` ⇒ **đúng hai** đường ngoài
  `ops/reviews/`; đây là phần packet đã viết trước khi merge.
- `git diff --numstat <merge commit>..<head cuối>` ⇒ **đúng hai** đường ngoài `ops/reviews/`; đây là
  phần viết SAU merge để hoà giải.
- **TỔNG `additions` của hai phép trên**, cho hai đường sản phẩm, ≤ **300**.
Đường thứ ba nào ngoài `ops/reviews/` ⇒ ĐỎ. **Không** đếm delta mà merge mang vào từ #521.

**Điều kiện dừng:** `sensitive` ⇒ `approve` **tường minh**. Packet này phải là packet đầu tiên tuân
**chính** quy trình nó khai — gồm `M8` (base trôi ⇒ merge base TRƯỚC, rồi review head SAU merge) và
`M10` (`N = 0` trước merge).

**Mọi tiêu chí `A1'`–`A18` phải ĐÚNG Ở CẢ HAI PHÍA của lần merge.** Một tiêu chí chỉ đo được trên bản
nhánh là tiêu chí **chết đúng lúc merge** — đúng bài học *"câu mô tả vị trí của một artefact phải đúng
ở CẢ HAI phía của lần merge"*. Nên mọi phép đo của r4 neo vào **head sau merge**, và nêu `dc02c9b` làm
mốc so thay vì "nhánh mặc định hiện tại".

## `chua_do_duoc`

Giữ **bốn mục của r3** (không cổng nào canh M1–M12; `DIEU-KIEN-VONG-CUOI-KHONG-DO-DUOC`;
`HEAD-DOI-VI-HIEN-VAT-REVIEW`; `grep -i` không đo được tiêu chí văn bản tiếng Việt). Thêm:

5. **`ADAPTER-VUA-CON-TRO-VUA-CO-RANG`** — (B) **giả định** tồn tại một dạng *"ngắn nhất còn đủ răng"*.
   Điều đó **chưa được đo**: chưa ai chứng minh một bảng rút gọn kèm con trỏ `§` vẫn làm ĐỎ đúng những
   đột biến mà bản dài làm ĐỎ. `A18` biến giả định ấy thành phép đo **cho packet này**, nhưng **không**
   chứng minh nó đúng tổng quát cho mọi mục doctrine khác — và nếu `A18` cho thấy một chốt mất răng khi
   rút gọn, thì kết luận đúng là **báo chủ kho**, không phải nới `A1'`/`A2'` cho hết đỏ.
6. **`#521` có lease hay không: KHÔNG ĐO ĐƯỢC, và theo chỉ thị KHÔNG đi tìm thêm.** Xem mục
   *"VÌ SAO PHẢI CÓ r4"*. Đừng đọc bản đo ở comment `5647008786` thành một kết luận về #521.
7. **Lượt cổng tự động trên `6b46012`**: tới lúc soạn r4 **chưa có lượt nào** (`actions_list` lọc theo
   `ci.yml`, head gần nhất của nhánh là `56cfce5`). `M10` cấm gọi tay, nên trạng thái là **KHÔNG ĐO
   ĐƯỢC**, không phải xanh. Lượt cổng của master cho chính commit merge #521 (`dc02c9b`, run
   `34702466800`) kết luận **`cancelled`** — ghi ra vì nó KHÔNG phải bằng chứng master xanh, và cũng
   không phải việc của packet này.
