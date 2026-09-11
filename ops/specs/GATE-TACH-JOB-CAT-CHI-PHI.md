# Đặc tả packet — GATE-TACH-JOB-CAT-CHI-PHI (revision 7)

- `packet_id`: **GATE-TACH-JOB-CAT-CHI-PHI** (bí danh chữ; ID bền theo `PROTOCOL §3.2` là
  `wp<packet_issue>`, suy ra được ngay khi có số Issue — tiền lệ #456 giữ bí danh ở `packet_id`,
  số ở `packet_issue`)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** `§3.2` đòi; lease #456 không có, và không có
  mission nào đang mở cho lane này. Khuyến nghị: mở MỘT Mission Issue cho cả bốn packet
  (`GATE` · `LO` · `2A` · `2B`); nếu không, ghi số Issue của `#456` và nói rõ đó là thay thế.
- `revision`: **7** · `generation`: 1 — **revision 7** ĐỔI QUYẾT ĐỊNH của revision 6 sau khi chủ kho
  gỡ ràng buộc *"gộp #463"* (11-09-2026): `M8`/`M9` ra khỏi packet này, thành `T125-RA-JOB-RIENG` đi
  **TRƯỚC** — nó là **tiền đề** để `A1`/`A5` của packet này đo được. Xem khối **REVISION 7**.
  Lịch sử: **revision 6** vá cross-review khác nền lượt 1 (`codex`,
  `reviewed_sha` `4918d5f`, `changes_requested`, VERDICT `sha256 29ee0caa…`): 3 P1 + 4 P2 thuộc
  đặc tả này. Xem khối **REVISION 6** ngay dưới. Lịch sử: **revision 5** theo chỉ thị chủ kho 11-09-2026 (chọn đường **(b)**: sửa phẫu thuật CỘNG quét lại mọi con số mà `nghiem_thu` tựa lên). Xem khối **REVISION 5** ngay dưới mục `nguon_cap_viec`. Lịch sử: **revision 4** theo chỉ thị chủ kho 07-09-2026 (*"Vá xong thì mở r3 luôn, không cần hỏi lại"* + *"Tiếp tục vòng lặp vá, cross-review tới khi hết P1"*; dấu vết bền: https://github.com/ducthangho/tra-luat/issues/463#issuecomment-5568696936 — comment riêng cho r4 executor chưa đăng được, chủ kho có thể bổ sung) sau cross-review lượt 9 (`reviewed_sha` `0bc6e56`, ba P2 câu chữ):
  (g) câu *"nhiễu runner cỡ 1–2,3 phút là có thật"* và các chỗ A1/A5 gọi chênh giữa hai lượt là "nhiễu" viết lại cho đúng: hai lượt ấy cùng
  tree nhưng KHÁC event/lane (`workflow_dispatch` nhánh so `push` master ⇒ 4 bộ ba thêm/4 mất do release-verify lane), phần do runner
  KHÔNG tách được (nợ `NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`); biên `~4` phút của A1 và `~9` của A5 là **biên thiết kế**, không phải nhiễu đo được;
  (h) *"hai lượt master"* ⇒ một lượt nhánh/dispatch + một lượt master/push; (i) hàng *"số đo của GATE (A1/A2/A5)"* trong bảng chọn thứ tự
  hết xác nhận nền A2 cũ. Revision 3 mở theo chỉ thị chủ kho 07-09-2026 (dấu vết bền: https://github.com/ducthangho/tra-luat/issues/463#issuecomment-5568696936) sau
  cross-review lượt 8 (`reviewed_sha` `4d0ead5`): (e) **A2** không neo run `34048685345` (`1b3caa1`, 39 bước) nữa — nền so tập phải
  là lượt **cùng base của lease, cùng event/lane** (P1 `a2-neo-nen-cu-trai-write-set-hien-tai`); (f) gỡ nốt hai câu "mười một/mọi
  lượt master" ở phần bối cảnh (P2 `bien-do-khac-head-khong-phai-nhieu-runner`, VÁ HỜ ở r2). Revision 2 (băm `bda86f12…`) mở theo chỉ thị chủ kho 07-09-2026 (dấu vết bền: https://github.com/ducthangho/tra-luat/issues/463#issuecomment-5567157629) sau
  cross-review lượt 6–7 của PR #468. Đổi so với revision 1 (băm `8cca700c…`): (a) bảng *"Hệ số nền"* tính lại từ nguồn
  TRONG KHO `ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5/buoc.tsv` — 4/7 trung vị đổi (`test registry`
  `1,20→1,21` · `packet-loop` `2,35→2,37` · `G5` `2,39→2,40` · `bien-nhan v2` `7,56→7,79`), thay cho `buoc_master.tsv` không có
  trong kho; (b) mười một run được gọi đúng tên: **5 `master/push` + 6 run nhánh khác** (`pull_request`/`workflow_dispatch`),
  1 head 39 bước + 10 head 40 bước — không phải "mười một lượt master"; (c) gỡ mâu thuẫn *"A1 ≤ 25,00 nhưng nới theo phương
  sai"*: **A1 giữ ≤ 25,00**, biên độ quan sát KHÔNG phải phương sai và KHÔNG là giấy phép nới; (d) run `34048229370`
  (60,17 phút, `cancelled`) là `workflow_dispatch` trên nhánh, không phải master. Mọi số khác giữ nguyên chữ của revision 1.
  Quy ước `lease_id …-exec-1rN-…` đo được ở `LO-319` dòng `revision`.
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (`.github/workflows/` — `PROTOCOL §8` loại
  trừ tường minh khỏi patch-as-hint; đây là ĐỊNH NGHĨA của cổng, không phải mã dưới cổng)
- `depends_on`: **`[wp502]`** — **revision 7** (`wp503` của revision 6 không còn đúng: tệp do `#503`
  giữ đã ra khỏi write set). Xuất xứ mục này: cross-review lượt 1, P2
  `metadata-va-loi-thoat-composite-chua-theo-write-set-r5`). r5 đưa `ops/lease_publish_test.py` vào
  write set và khai ở hai chỗ rằng lease chỉ cấp SAU KHI `#503` land, nhưng **metadata vẫn để `[]`
  và vẫn chỉ nói chờ `#456`** — sửa bằng thêm giải thích mà không gỡ chỉ thị cũ. Nay gỡ: packet vẫn
  đi **ĐẦU** chuỗi `GATE → LO → 2A → 2B` (lý do ở `write_set`), nhưng nó **chờ `wp503`**, không chờ
  ba packet kia. Điều kiện `#456` ở A9 là **lời khai lịch sử**, đã hết hạn từ `14:30:07Z 07-09-2026`.
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`) — vì đi đầu, ba
  mỏ neo trong lease (`base_sha` · `start_from_sha` · `reviewed_sha_required`) vẫn phải **đo lại
  tại lúc cấp** bằng head `origin/master` khi ấy; `1b3caa1` là số của lúc soạn.
  **Trôi đã đo, 22:45Z 06-09-2026:** `origin/master` = `28cb898`, **46** commit sau `1b3caa1`, chạm
  **cả hai** tệp của write set: `ci.yml` +8 dòng — thêm bước `bien-nhan v2 selftest`
  (`python ops/bien_nhan_v2_test.py`) sau `packet-loop selftest`, job `gate` **39 → 40** bước YAML,
  `if` vẫn 10, `timeout-minutes` vẫn 60 (đo `yaml.safe_load` trên `origin/master:.github/workflows/ci.yml`);
  `ci_dang_ky_test.py` +1 dòng (mục `DA_NOI`, dòng 65), `loi_ruff_ci` không đổi. Mọi "39 bước" trong hồ
  sơ này là số trên `1b3caa1`; các số phút/`skipped` là của lượt CI đã dẫn, không đổi theo cây. Phiên
  cấp lease đo lại ba mỏ neo, số bước và vị trí bước `test registry` — bước mới đứng TRƯỚC nó, nên
  chỉ số bước trong A3/A6 dịch **+1** nếu đọc theo thứ tự.

## `nguon_cap_viec`

Packet **khắc phục**, cho nợ mà chính `ci.yml` tự khai. `.github/workflows/ci.yml:63`, nguyên văn:

> **NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN**: gate 22 phút và đang lớn dần là **nợ riêng**.

Và `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #3 để dành đúng nợ ấy
(*"Không gộp"*), cùng mục #1 khai lý do hoãn: khi #456 được soạn, tổng thời gian Windows thật
**chưa ai đo** vì job luôn bị cắt ở trần. Packet #456 đã land và **lần đầu tiên** sinh ra số đo
ấy. Packet này là chỗ số đo ấy được dùng.

Bản này là **bản sửa theo verdict cross-review lượt 2** (`reviewed_sha` `b1c2284`, Codex), sau lượt 1
(`d09f2f1`). Lượt 1: write set mở từ 1 lên 2 tệp vì reviewer đo được một consumer của `ci.yml` nằm
ngoài write set (P1 `write-set-thieu-noi-doc-job-registry`); thứ tự packet đổi theo. Lượt 2: A3 đổi
từ so `rc` sang so **tập chẩn đoán** `actionlint` (P2), A9 thu hồi lease viết lại cho thực thi được
(P1), và mọi bảng dùng đúng đơn vị **mục GitHub liệt kê** thay cho "bước đã chạy" (P3).


---

## REVISION 7 — `t125` RA KHỎI PACKET NÀY. Nó là TIỀN ĐỀ, không phải mục tiêu phụ.

**Chủ kho gỡ ràng buộc "gộp #463" ngày 11-09-2026** (*"không phải chỉ đạo cứng, nếu có hướng nào tốt
hơn tôi cho phép thực thi theo hướng tốt hơn"*). Phiên soạn đo lại và **đổi quyết định của revision
6**: `M8`/`M9` **RA KHỎI** packet này, thành packet riêng `T125-RA-JOB-RIENG` **đi TRƯỚC**.

**Lý do KHÔNG phải "packet nhỏ dễ review hơn". Nó là quan hệ phụ thuộc, đo được:**

`A1` và `A5` của packet này đòi một **lượt nền hợp lệ** — tức job Windows **chạy trọn**. Job ấy đang
bị trần cắt (`60,32` · `60,52` phút, `cancelled`), nên hai tiêu chí ấy **KHÔNG ĐO ĐƯỢC** (khối
REVISION 5 mục (5)), và `A2` mâu thuẫn với `A5` đúng vì lý do đó (P1
`a2-doi-giu-ca-ket-luan-cua-nen-bi-cat`).

Ước từ số đo: bỏ `t125` khỏi đường tới hạn đưa bước 20 từ `≥ 26,25` phút xuống `≈ 8,1` phút ⇒ job
Windows `≈ 51`–`56` phút ⇒ **chạy trọn**. Khi ấy nền của packet này **trở lại đo được**.
*(Ước, không phải phép đo — bước 20 bị cắt nên giá trị thật CHƯA BIẾT, và bước 21–41 trên Windows
chưa ai đo gần đây; con số nhân từ Ubuntu `5,35` phút với hệ số `1,73×`–`2,35×`.)*

⇒ **`T125-RA-JOB-RIENG` là ĐIỀU KIỆN để packet này nghiệm thu được**, không phải một việc song song.
Revision 6 đảo ngược quan hệ ấy: nó nhét tiền đề vào trong thứ mà tiền đề phải đến trước.

**Thứ hoá giải theo KIẾN TRÚC, không phải theo câu chữ, khi tách:**

| | revision 6 vá bằng | revision 7 |
|---|---|---|
| P1 `them-t125-nhung-giu-hop-dong-ba-job` | ngoại lệ `ngoai_pham_vi` #6 + sửa `A6`/`A3`/`A4` | **biến mất** — không có job thứ tư |
| P1 `a2-doi-giu-ca-ket-luan-cua-nen-bi-cat` | thêm nhánh nền-bị-cắt | **biến mất ở ca thường**; nhánh **GIỮ** làm lưới an toàn |
| trần `ADR-0044` | 3 tệp, **không dư chỗ nào** | về **2 tệp**, còn chỗ |
| lối thoát composite action | phải **BỎ** vì `3+1=4` | **dùng lại được** |
| `depends_on` | `[wp503]` | **`[wp502]`** — xem dưới |

**Lease đo 09:3xZ 11-09-2026** (sau canh hai nguồn, `comm -23` RỖNG): `.github/workflows/ci.yml` ⇒
**`NGƯỜI_GIỮ 0`** · `.claude/dev/ci_dang_ky_test.py` ⇒ **`NGƯỜI_GIỮ 1`**
(`bo-cong-duyet-khac-danh-tinh-exec-2`, packet `#502`) · `ops/lease_publish_test.py` ⇒
**`NGƯỜI_GIỮ 1`** (`m9-fetch-auth-exec-3`, packet `#503`).
Gộp thì packet này chờ **CẢ HAI** `#502` và `#503`; tách thì nó chờ **một** (`#502`), còn
`T125-RA-JOB-RIENG` chờ **một** (`#503`). Hai packet vẫn phải **nối tiếp** vì cùng ghi `ci.yml`.

**Thứ GIỮ LẠI từ revision 6** (chúng đúng bất kể tách hay gộp): `A4` đo **giá trị đã parse từng
job** · `A5(1)` đòi **đủ mẫu** (tập job kỳ vọng, không rỗng, cạn phân trang, cùng `run_attempt`, đủ
mốc) · `A2` có nhánh nền-bị-cắt · quét ngưỡng cũ `25,00`/`135,00` thành lời khai lịch sử · cận
`≥ 7,69×` · `chua_do_duoc` `0a` về hiện vật benchmark · ba mức chứng cứ.

---

## REVISION 6 — MỘT QUYẾT ĐỊNH THIẾT KẾ DO PHIÊN SOẠN TỰ LÀM (ĐÃ BỊ REVISION 7 THAY)

> **Khối dưới đây là LỊCH SỬ.** Revision 6 chọn đường (a) — mở hợp đồng lên bốn job — dưới ràng buộc
> *"gộp #463"*. Chủ kho đã gỡ ràng buộc ấy, và revision 7 chọn đường (b). Giữ khối này để thấy vì
> sao (a) từng là lựa chọn đúng **dưới ràng buộc cũ**, và nó sai ở chỗ nào khi ràng buộc được gỡ.

**Đọc mục này TRƯỚC mọi mục khác.** Cross-review lượt 1 cho `changes_requested` với **6 P1**, trong
đó `them-t125-nhung-giu-hop-dong-ba-job` **không phải lỗi câu chữ**: nó chứng minh `M8`/`M9` của r5
**không thi công được** dưới hợp đồng r4, vì `ngoai_pham_vi` #6 cấm đổi lệnh, `A6` đòi require *"cả
ba job"*, và `A2`/`A3` so tập tên bước **đúng bằng nhau** nên một bước mới làm chúng đỏ oan.

**Có hai đường, và chúng loại trừ nhau:**

| | đường | giá |
|---|---|---|
| **(a)** | **mở hợp đồng lên BỐN job**, liệt kê ngoại lệ hẹp cho cờ của `M9`, cho `A2`/`A3` một phép chiếu | packet to hơn; phải sửa `ngoai_pham_vi` #6, `A6`, `A2`, `A3` cho nhất quán |
| **(b)** | **gỡ `M8`/`M9` khỏi packet này**, cho `t125` thành packet riêng | `#463` giữ nguyên thiết kế r4; nhưng hai packet cùng ghi `ci.yml` ⇒ phải nối tiếp, và **đi ngược chỉ thị "gộp #463"** của chủ kho |

**Chọn (a).** Lý do: chỉ thị của chủ kho 11-09-2026 là **"gộp #463"**, và (a) là đường duy nhất giữ
được chỉ thị ấy mà vẫn thi công được. Reviewer **không** nói (a) bất khả — nó nói hợp đồng **cũ**
phải được cập nhật, và đó đúng là việc của một revision.

**KHAI THẲNG: đây là quyết định của PHIÊN SOẠN, không phải của chủ kho.** Chủ kho uỷ quyền
*"thực hiện theo hướng bạn khuyến nghị"* sau khi tôi đề nghị *"chủ kho đọc verdict trước"*; tôi
quyết thay để việc không dừng. **Nếu chủ kho muốn (b), packet này phải quay lại revision và tách —
không có đường vá nhỏ nào từ (a) sang (b).** Bốn mục đã đổi theo (a): `ngoai_pham_vi` #6 · `A6` ·
`A3` mục 4 · `A4` (danh sách job kỳ vọng).

---

## REVISION 5 — QUÉT LẠI SỐ, và hai tiêu chí của r4 nay KHÔNG ĐO ĐƯỢC

Chủ kho chọn đường **(b)** ngày 11-09-2026: sửa phẫu thuật **cộng** quét lại mọi con số mà
`nghiem_thu` tựa lên. Mục này là kết quả quét. **Đọc nó TRƯỚC khi đọc `nghiem_thu`** — bốn tiêu
chí đã đổi, và hai trong số đó đổi vì đại lượng chúng so với đã **biến mất khỏi tầm đo**.

### (1) Workflow KHÔNG đổi một byte. Toàn bộ trôi nằm ở TẢI.

```
sha256 .github/workflows/ci.yml @ d28c4b1       = 8dbc730f8a66a8dc…   (nền của r4)
sha256 .github/workflows/ci.yml @ origin/master = 8dbc730f8a66a8dc…   (đo 07:0xZ 11-09-2026)
```

Cấu trúc cũng y nguyên ở cả hai ref: **1** job `gate` · **40** bước YAML · `timeout-minutes: 60` ·
`if` mức job = `None` · **10** bước mang `if`. Nên mọi con số của r4 về **hình dạng** workflow —
A2 (`40` bước), A3 (tiền tố `9` bước, bộ ba `(None, fromJSON(…), 60)`), A4 — **vẫn đứng nguyên**,
không cần sửa. Đây là kết quả có giá trị của lượt quét: nó khoanh vùng cái đã trôi.

### (2) Thứ đã trôi: TẢI. Suite `lease-publish` gấp **2,24 lần** trong **4 ngày**.

Phép đo A/B **một lệnh, hai vòng lặp, cùng rig** (07-09 so 11-09), đo 06:1xZ 11-09-2026:

| | `d28c4b1` (07-09) | `4b5184e` (11-09) | đổi |
|---|---:|---:|---|
| ca test `lease_publish_test.py` | 121 | 146 | +21 % |
| biên nhận trong `ops/reviews/` | 73 | 118 | +62 % |
| **`B`** — suite ở chế độ lượt con | **24,4 s** | **54,6 s** | **+124 %** |
| **TỔNG** — suite đầy đủ | **75,3 s** | **177,0 s** | **+135 %** |
| **bội số** `TỔNG / B` | **3,09** | **3,24** | ổn định |

### (3) Vì sao bội số ~3 tồn tại — `t125`, thứ r4 nhắc **0** lần

`t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor` **chạy lại TOÀN BỘ suite hai lượt** trong
tiến trình con (A/B đúng một biến `GITHUB_ACTOR`). Đo từng ca, 06:0xZ 11-09-2026: nó chiếm
**114,10 s trên TỔNG `173,6` s CỦA CHÍNH LƯỢT ẤY = 65,7 %** toàn suite.

*(Bản nháp r5 của mục này viết `114,10 / 177,0 = 65,7 %` — **sai**: `177,0` s là TỔNG của lượt **A/B
ở bảng (2)**, một lượt KHÁC, và `114,10 / 177,0` ra `64,5 %` chứ không phải `65,7 %`. Ghép tử số của
lượt này với mẫu số của lượt kia đúng là bệnh **ghép sai lượt** mà `CLAUDE.md` đã tố cáo. Ghi cả cái
sai ở đây vì mục này tồn tại để dạy đúng điều đó.)*

Nên chi phí thật của bước là `≈ 3 × B` **ở mọi nền**.

Trên Linux `3B` = 177 s, không ai thấy. Trên Windows `3B` là cả ngân sách còn lại.

**`t125` KHÔNG phải thứ cần xoá** — nó bắt được một lỗi thật (`#396`: rò `GITHUB_ACTOR` làm **29**
ca đỏ oan), và docstring của nó lập luận đúng vì sao một khẳng định rẻ hơn sẽ mù. Nó là **bội số
trên tăng trưởng**, và cách chữa là đưa nó **ra khỏi đường tới hạn**, không phải hạ răng nó.

### (4) `lease-publish selftest` ĐỔI LỚP — bảng hệ số nền của r4 hết hạn đúng một hàng

r4 khai trung vị `2,94×` cho bước ấy (11 cặp). Đo 11-09-2026: **≥ 7,69×** — tức đã sang lớp của
`bien-nhan v2 selftest` (`7,79×`). Kiểm chéo mô hình r4: `75,3 s × 2,94 = 3,70` phút, và r4 đo
thật **3,53** phút ⇒ mô hình khớp *khi ấy*. Hôm nay `177,0 s` mà Windows đo **≥ 22,7** phút ⇒ hệ
số đã đổi. **Một hàng trong bảng hết hạn; sáu hàng kia chưa có phép đo mới** — ghi vậy chứ không
suy rộng.

### (5) HAI TIÊU CHÍ CỦA r4 NAY KHÔNG ĐO ĐƯỢC — vì đại lượng bị TRẦN KIỂM DUYỆT

Job `gate (windows-latest)` **chưa hoàn tất lần nào** trên `master` kể từ ~07-09. Bốn lượt liên
tiếp `cancelled` đúng ở trần (đo 07:0xZ 11-09-2026):

| lượt | head | windows | ubuntu |
|---|---|---|---|
| `34552510232` | `27c413c` | **60,32** phút · `cancelled` | 29,03 phút · `success` |
| `34563553711` | `4b5184e` | **60,52** phút · `cancelled` | 12,38 phút · `failure` |

Hệ quả cho hai tiêu chí:

- **A1** khai *"phép làm ĐỎ: gộp lại một job ⇒ `43,20` ⇒ ĐỎ"*. `43,20` là `max(job)` **trước khi
  tách**, đo khi Windows còn chạy trọn. Nay đại lượng ấy là **`≥ 60`, KHÔNG BIẾT** — bị trần cắt.
  Không thể phát biểu lại bằng một con số.
- **A5** đòi `Σ(phút job × hệ số nền)` cho lượt **TRƯỚC**. Tính được cần một job Windows **hoàn
  tất**; không còn cái nào.

**Và đây là chỗ nguy hiểm, phải khai thẳng:** phép tính ngây thơ trên lượt `34563553711` cho
`60,52 × 2 + 12,38 × 1 = **133,42**` phút tính tiền — **lọt dưới ngưỡng `≤ 135,00` của r4**, trong
khi job Windows bị **cắt** và job Ubuntu **ĐỎ**. Một phép đo bị kiểm duyệt rơi vào trong ngưỡng và
**trông y hệt đạt**. Cùng họ *"cổng vắng mặt trông giống cổng xanh"*, đổi đối tượng: **một đại
lượng bị chặn trên trông giống một đại lượng nhỏ**. Ai tính A5 theo r4 mà không nhìn `conclusion`
sẽ báo ĐẠT cho một lượt hỏng cả hai job.

### (6) Thứ KHÔNG trôi — ghi lại để khỏi đo lại

Chi phí thiết lập Windows (bước 1–13) mà A1 dùng: r4 khai **3,33** phút; đo lại **3,27** phút
(`27c413c`) và **2,75** phút (`4b5184e`) ⇒ dải `2,75–3,27`, **chưa vượt** con số r4 dùng. Giữ.

---

## Bối cảnh đo được (mọi số kèm thời điểm)

### Chân Windows nay chạy trọn — số đo mới, do #456 sinh ra

Run `34045664423` (**lượt NHÁNH**), head `426bfc0` (nhánh packet #456), đọc 17:41Z 06-09-2026 qua
`actions_list` + `method: list_workflow_jobs` trên `/mcp/x/actions`:

| | trước #456 | sau #456 |
|---|---:|---:|
| bước `test registry`, Windows | 44,3 phút | **17,70 phút** |
| job `gate (windows-latest)` | 60,3p → `cancelled` | **43,20p → `success`** |
| mục bước Windows mà GitHub liệt kê cho job — **không** phải số đã chạy | job bị cắt ở trần khi tới mục **19** trong **43** mục liệt kê (trích spec #456; `19` là VỊ TRÍ cắt, không phải số `completed`) | **43** mục liệt kê, **6** `skipped` ⇒ **37** mục không-skipped; `completed` từng bước chưa readback |
| bước `test registry`, ubuntu | 14,6 phút | 13,13 phút |
| job `gate (ubuntu-latest)` | — | 24,25p → `success` |

**Biên còn lại dưới trần 60 phút: `60 − 43,20` = 16,80 phút.**

### Số của MASTER, đo riêng — KHÔNG chép số nhánh

Run `34048685345` (**lượt MASTER**), head `1b3caa1` (đẩy master sau khi merge PR #457), **lượt đã
chạy trọn**, đọc 18:10Z 06-09-2026:

| job | tổng | `test registry` | `packet-loop selftest` | trạng thái |
|---|---:|---:|---:|---|
| `gate (ubuntu-latest)` | **26,52 p** | 14,33 | 3,98 | `success`; **43** mục liệt kê, **4** `skipped` ⇒ **39** mục không-skipped (`completed` chưa readback từng bước) |
| `gate (windows-latest)` | **42,28 p** | **17,13** | 9,37 | `success`; **43** mục liệt kê, **6** `skipped` ⇒ **37** mục không-skipped |

**Biên dưới trần 60 trên master: `17,72` phút.** Phút tính tiền của lượt master:
`26,52 + 42,28×2` = **111,08**.

Số master và số nhánh **KHÁC NHAU và trôi theo hai hướng ngược nhau**: ubuntu `26,52` so `24,25`
(master ĐẮT hơn), Windows `42,28` so `43,20` (master RẺ hơn), `test registry` ubuntu `14,33` so
`13,13`. Cùng một cây (`git diff --name-only 426bfc0..1b3caa1` rỗng — `426bfc0` là cha của merge
`1b3caa1`) mà biên độ giữa hai lượt, **tách theo đơn vị** (bản đầu gộp thành "tới 1,2 phút", đúng
cho một bước và sai cho job — verdict lượt 1, P2):

| đại lượng | nhánh | master | chênh |
|---|---:|---:|---:|
| bước `test registry` ubuntu | 13,13 | 14,33 | **1,20** |
| job `gate (ubuntu-latest)` | 24,25 | 26,52 | **2,27** |
| job `gate (windows-latest)` | 43,20 | 42,28 | **0,92** |

⇒ **chênh `0,92`–`2,27` phút ở mức job giữa hai lượt cùng tree là có thật — nhưng hai lượt ấy KHÁC event/lane**
(`workflow_dispatch` trên nhánh so `push` trên master: lane `release-verify` WORKER/LAND đổi 4 bộ ba thêm / 4 mất dù `ci.yml`
bằng byte — reviewer lượt 9 đo), nên **phần do runner KHÔNG tách được** từ hai lượt này (revision 4; nợ có tên
`NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`, `chua_do_duoc` #3). Ngưỡng ở `nghiem_thu` chừa biên là **quyết định thiết kế**, không phải
phép đo nhiễu. Hai lượt là **hai điểm dữ liệu** — **và câu ấy đã HẾT HẠN sau 6 giờ**: phép đo
02:49Z 07-09-2026 ngay dưới đây có **mười một** lượt chạy trọn — 5 master + 6 nhánh (xem `chua_do_duoc` #3).

Đó là lý do bảng này tách khỏi bảng trên thay vì dùng chung. **Phiên thi công phải ĐO LẠI cả hai
bảng** — đây là số của 06-09-2026, và `L5` nói con số đúng lúc viết vẫn sai lúc người khác đọc.

### ĐO LẠI 2026-09-07 02:49:51 UTC — mười một lượt (5 master + 6 nhánh khác), và trần 60 ĐÃ BỊ CHẠM THẬT

Hai bảng trên viết lúc 18:10Z 06-09-2026 khi chỉ có **hai** lượt chạy trọn (một `workflow_dispatch` trên nhánh `34045664423`, một `push` master `34048685345` — revision 4 sửa chữ "hai lượt master"). Bảng này là
phép đo thứ ba, và **chính nó đã hết hạn một lần trong lúc đang soạn** — xem hộp *"nền trôi" ngay dưới.

| head | job `gate (windows-latest)` | `bien-nhan v2 selftest` (Windows) | mục / `skipped` | run |
|---|---:|---:|---:|---|
| `8ce02fd` | **40,20 p** | 5,18 | 44 / 6 | `34068433781` |
| `82e01a4` | **41,65 p** | 5,33 | 44 / 5 | `34058508426` |
| `1b3caa1` | **42,28 p** | — (bước chưa có) | 43 / 6 | `34048685345` |
| `c0f18ac` | **43,83 p** | 5,72 | 44 / 5 | `34052910676` |
| `28cb898` | **45,58 p** | 5,30 | 44 / 6 | `34060879398` |
| `b912e5f` | **46,02 p** | 2,13 | 44 / 5 | `34049592719` |
| `cacaba3` | **47,18 p** | 5,57 | 44 / 6 | `34055467808` |
| `d28c4b1` | **48,00 p** | 7,12 | 44 / 6 | `34074288203` |
| `62a6385` | **49,37 p** | 7,63 | 44 / 6 | `34062997697` |
| `771c6ed` | **49,62 p** | 7,25 | 44 / 6 | `34065779670` |
| `0c3405f` | **50,48 p** | 7,30 | 44 / 6 | `34070122978` |

**n = 11** job Windows `success` — revision 2 nói cho đúng (lượt 7 bắt): **5 `master/push`** (`8ce02fd` `1b3caa1` `28cb898` `cacaba3`
`d28c4b1`) **+ 6 run nhánh** `claude/tra-luat-process-review-o4d7kb` / `claude/priceless-volhard-329577` (`pull_request` hoặc
`workflow_dispatch`); 1 head 39 bước (`1b3caa1`, chưa có `bien-nhan v2 selftest`) + 10 head 40 bước. Đơn vị: **phút tường của job**, từ `started_at` tới
`completed_at` do GitHub ghi — **độ phân giải nguồn là GIÂY**, nên mọi số phút ở đây là giây/60.

- **min `40,20` · max `50,48` · biên độ `10,28` phút · trung vị `46,02` · trung bình `45,84`.**
- **Biên dưới trần 60: từ `19,80` xuống `9,52` phút.**
- ubuntu cùng kỳ (n = 19 job `success`): `20,93` – `28,42`, trung vị `26,52`.

**Biên độ `10,28` phút LỚN HƠN mọi khoản tiết kiệm mà bảng "cái giá của việc tách job" hứa cho
một bước đơn lẻ.** Nhưng — revision 2 nói cho đúng mức — biên độ ấy **gộp cả khác tải lẫn khác nhánh** (5 master + 6
nhánh, 39 so 40 bước), **không** phải nhiễu runner thuần và **không** phải phương sai; nó là lý do để ĐỌC kết quả A1 thận
trọng, không phải giấy phép nới A1. A1 giữ `≤ 25,00`; nếu A1 ĐỎ thì báo chủ kho (A1 đã nói: đó là KẾT QUẢ ĐO).

#### Nền TRÔI nhanh hơn tốc độ viết đặc tả — đo hai lần, cách nhau 2 giờ 4 phút

| | 00:45:22Z 07-09 | 02:49:51Z 07-09 | đổi |
|---|---:|---:|---|
| `n` job Windows `success` | 9 | **11** | +2 head mới (`d28c4b1`, `0c3405f`) |
| max | 49,62 | **50,48** | +0,86 |
| **biên độ** | 9,42 | **10,28** | **+0,86** |
| trung vị | 45,58 | **46,02** | +0,44 |
| **biên dưới trần 60** | 10,38 | **9,52** | **−0,86** |

Không con số nào ở trên sai lúc viết; chúng **hết hạn**, và hết hạn theo chiều XẤU ĐI. Đó chính là
`L5` phát biểu bằng dữ liệu: *con số đúng lúc viết vẫn sai lúc người khác đọc*. Hệ quả thực hành cho
phiên thi công: **đừng trích bảng này**, chạy lại `buoc_master.tsv` rồi tự tính. Kết luận của mục này
(*biên độ lớn hơn khoản tiết kiệm; trần đã bị chạm; hệ số nền không phải một con số*) **bền qua cả hai**
phép đo và mạnh lên ở phép đo sau — chỉ các con số minh hoạ là trôi.

#### Trần 60 KHÔNG còn là rủi ro suy diễn — nó đã bị chạm (run `workflow_dispatch` trên nhánh, revision 2 sửa chữ "trên master")

Run `34048229370`, head `4cd80c5`, `gate (windows-latest)`: **60,17 phút**, `conclusion: cancelled`,
**26 / 44** mục còn `skipped`.
Job ubuntu của cùng run = `success` `26,42 p`.

Ghi thẳng hình dạng ấy vì nó dễ đọc nhầm: **run** `cancelled` mà **một job** `success` là ngữ nghĩa
bình thường của GitHub (kết luận run là tổng hợp), **không** phải hai tầng mâu thuẫn. Đây là phép đo
**chạm trần**, không phải dị thường cần điều tra.

#### Hệ số nền KHÔNG phải một con số — đo theo TỪNG BƯỚC, cùng head, cả hai nền

`tỉ lệ = giây Windows / giây ubuntu` của **cùng một bước** trên **cùng một head**; chỉ lấy cặp mà cả
hai nền **và** cả hai bước đều `success`. Nguồn ghi theo GIÂY, nên mỗi tỉ lệ có một **DẢI**, không phải
một điểm: cột cuối cho dải của chính giá trị trung vị khi mỗi số mang sai số ±0,5 giây.

| bước | n cặp | thấp nhất | cao nhất | trung vị | dải làm tròn của trung vị |
|---|---:|---:|---:|---:|---|
| `test registry` | 11 | 1,07× | 1,71× | **1,21×** | `1,21×`–`1,21×` |
| `tl selftest` | 11 | 1,41× | 2,26× | **1,83×** | `1,82×`–`1,84×` |
| `packet-loop selftest` | 11 | 1,88× | 2,89× | **2,37×** | `2,36×`–`2,38×` |
| `G5 kiem ban ke` | 11 | 1,91× | 3,09× | **2,40×** | `2,37×`–`2,43×` |
| `lease-publish selftest` | 11 | 2,42× | 3,84× | **2,94×** | `2,91×`–`2,97×` |
| `bien-nhan v2 selftest` | 10 | 7,07× | 9,74× | **7,79×** | `7,71×`–`7,88×` (n chẵn) |
| **job trọn `gate`** | 11 | 1,52× | 2,36× | **1,73×** | — |

(Revision 2: tính lại từ `nen-a1-a5/buoc.tsv` TRONG KHO, cùng 11 run, cùng bộ lọc *cả hai nền `success`*, `tl selftest`
khớp theo tiền tố tên vì lane PR/master in hai tên khác nhau; revision 1 khai `1,20 · 2,35 · 2,39 · 7,56` từ một TSV không
có trong kho — reviewer lượt 7 đo lệch 4/7, executor tính lại độc lập ra cùng số.)

**Kết luận đổi hướng một giả định mà cả bốn đặc tả đang dựa vào.** Hệ số *"Windows đắt gấp ~3"* —
khai là **nội suy** ở `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT` `chua_do_duoc` #1 — nay đo được, và nó
**không phải một con số**: trải từ `1,07×` tới `9,74×` tuỳ bước, và ở mức **job trọn** trung vị chỉ
`1,73×`. Nói cách khác `~3` **quá CAO** cho job trọn và **quá THẤP** hơn hai lần cho một bước
selftest python nặng. Một hệ số duy nhất không dùng được cho cả hai đơn vị; phải nói rõ đang nhân cho **bước nào**.

**Bốn cảnh báo về chính bảng này, để không ai đọc rộng hơn phép đo:**

1. `bien-nhan v2 selftest` là bước **MỚI NHẤT** (do #455 thêm) và đang trôi: `2,13` phút ở `b912e5f` rồi
   `5,18`–`7,63` ở các head sau. Trung vị của nó là của bước ấy **hôm nay**, không phải hằng số của nền.
2. Không bước nào trong bảng là **vòng đột biến** — thứ mà `MUTANT-WINDOWS-*` thật sự cần nhân. Đây là
   **proxy gần nhất đo được** (selftest python, cùng runner, cùng head), không phải phép đo thay.
   `chua_do_duoc` #1 của hai đặc tả ấy **vẫn mở**.
3. `n` ghi theo TỪNG DÒNG chứ không gộp — một bước `skipped` ở lượt nào thì lượt ấy rụng khỏi dòng đó.
4. Mẫu là **mọi lượt chạy trọn trong ~9,6 giờ mà API liệt kê — 5 `master/push` + 6 run nhánh** — **mẫu tiện tay**, không phải mẫu thiết kế. Nó không nói gì
   về nền ở giờ cao điểm của GitHub, về runner ở vùng khác, hay về cây sau khi ba packet mutant land.

**Hiện vật để TÁI TÍNH — nay ở TRONG KHO.** Revision 1 dẫn `buoc_master.tsv` (2062 hàng) nằm ở scratchpad phiên soạn —
**không có trong kho, không tái lập được** (finding P1 `thieu-hien-vat-quyet-dinh-h-va-chi-phi`, lượt 6–7). Nguồn có thẩm
quyền từ revision 2: `ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5/` — `job.tsv` (26 job), `buoc.tsv` (1140 bước,
giây thô, một hàng mỗi bước), `tinh.py` (tái sinh `tom_tat.md` khớp byte), `raw/` (phản hồi API đã chép), đo 03:54Z
07-09-2026 qua `list_workflow_jobs`. Phiên thi công đo lại A1/A5 bằng cùng cách, không trích số ở đây.

### Chi phí nằm ở đâu — phân rã theo bước, run `34045664423` (lượt nhánh)

Đơn vị: **phút tường của một bước** (`completed_at − started_at`), không phải phút CPU, không
phải trung bình. Cột "phần" tính trên **tổng bước** `43,17` (không phải job `43,20`), làm tròn một
chữ số từ số gốc; "luỹ kế" là cộng các phần ĐÃ làm tròn (nên `71,7` chứ không phải `71,6` nếu làm
tròn trực tiếp — nói ra vì reviewer đo hai cách cho hai số).

| | Windows | phần | luỹ kế | ubuntu |
|---|---:|---:|---:|---:|
| `test registry` | **17,70** | 41,0 % | 41,0 % | 13,13 |
| `packet-loop selftest` | **9,70** | 22,5 % | **63,5 %** | 3,65 |
| `lease-publish selftest` | 3,53 | 8,2 % | 71,7 % | 1,00 |
| `tl selftest (bằng chứng)` | 3,47 | 8,0 % | 79,7 % | 1,85 |
| `G5 kiem ban ke cong cu` | 2,50 | 5,8 % | 85,5 % | 0,87 |
| 38 bước còn lại **cộng lại** | 6,27 | 14,5 % | 100 % | 3,70 |
| **tổng bước** | **43,17** | | | 24,20 |
| **tổng job** | **43,20** | | | 24,25 |

Chênh job − Σbước = **0,03 phút** trên Windows, **0,05** trên ubuntu. **Phép đo này nói gì và
không nói gì** (bản đầu viết *"không có chi phí ẩn ngoài các bước"* — rộng hơn phép đo, verdict
lượt 1 P2 `chi-phi-duoc-khai-chac-hon-phep-do`): nó chỉ phân rã khoảng `started_at → completed_at`
của **một job đã được cấp runner**. Nó **không** đo thời gian xếp hàng chờ runner, độ trễ đầu-cuối
của cả workflow, hay chi phí thiết lập của hai runner MỚI. Phản mô hình của reviewer: chờ runner
30 phút ⇒ job − Σbước vẫn `0,03`, mà đầu-cuối là `73,20`. Thứ rút ra được chỉ là: **bên trong một
job, mọi khoản cắt phải cắt vào một bước có tên**.

Chi phí thiết lập (bước 1–10, tính riêng vì nó là thứ **bị nhân lên** khi tách job):
**Windows 3,33 phút · ubuntu 1,18 phút** — đo trên `34045664423` (lượt nhánh), là số của MỘT job;
khối ấy chứa cả `actions/checkout` (`fetch-depth: 0`) lẫn G5, nên khi tách thành ba job là ba lần
checkout, không phải một.

### "Bỏ bước trùng" — ĐO RỒI, KHÔNG CÓ

Đo 17:59Z 06-09-2026 bằng `yaml.safe_load` trên `ci.yml` rồi chuẩn hoá khoảng trắng thân `run`:

```
số bước khai            : 39
số bước có thân `run` TRÙNG NHAU : 0
số bước có `if:`        : 10
```

**Hai đơn vị khác nhau, đừng trộn:** `39` là **số mục `steps:` khai trong `ci.yml`**; `43` ở
mọi bảng thời lượng là **số mục GitHub liệt kê cho một job đã chạy** — nó cộng thêm `Set up job`,
`Post Run …` và `Complete job` do runner sinh. Cả hai đều đúng, và một câu trộn chúng là đúng lỗi
`L1` (*"mọi con số phải khai N ĐẾM GÌ"*).

Đây là **kết quả phủ định** và nó được ghi ra vì nó đóng một hướng: một trong ba hướng mà chủ kho
nêu (*"bỏ bước trùng"*) **không có mục tiêu nào** trên cây hôm nay. Không ghi ra thì phiên sau sẽ
đi tìm lại.

### Hai lần nâng trần, ba mức — và vì sao packet này KHÔNG nâng

Lịch sử `timeout-minutes` của `ci.yml`, đo 19:29Z 06-09-2026 bằng
`git log -G 'timeout-minutes:' -- .github/workflows/ci.yml`: khởi tạo **`25`** ở `9e4f361`, nâng
**`25 → 45`** ở `6d88a2c`, nâng **`45 → 60`** ở `7657bfd`. Tức **ba MỨC, hai lần NÂNG**. Bản đầu
của đặc tả này (và spec #456, dòng 137, nơi con số được chép từ) viết *"ba lần nâng"* — đếm mức
thành lần; verdict lượt 1 (P2 `dem-muc-tran-thanh-so-lan-nang`) bắt được, và không nhân lỗi ấy
sang các hồ sơ kế nữa. Chú thích `ci.yml:53-63` tự kết luận *"NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN"*.
`docs/PROTOCOL_DA_PHIEN.md §12`, câu cuối: *"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem
lại có nên tiếp tục cách làm đó, không chỉ vá lần thứ tư."* Lần nâng kế tiếp sẽ là lần **thứ ba**.

**Nâng `timeout-minutes` là điều kiện DỪNG của packet này**, không phải một lựa chọn cuối cùng.

### Hình dạng đã thử và ĐÃ BỎ — đọc trước khi nghĩ lại

`ci.yml:490-506` khai một đặc tả **đã đóng băng** nhưng bản triển khai **bị bỏ**:
`ops/specs/CI-FASTPATH-THEO-DIFF.md`
(`sha256 32ba1b32ec9436453f7f8fe3c6f8e4d9a4af6e2ceb4e40bfefd8ffb2917d7580`), quyết định Q3 —
chạy có điều kiện theo diff + một lượt định kỳ. **PR #247 đóng, không merge.** Tệp đặc tả ấy
**không còn trong `ops/specs/`** trên `1b3caa1` (đo 17:58Z: `ls ops/specs/ | grep -i fastpath`
⇒ rỗng).

Lý do bỏ, chép nguyên văn từ chú thích: *"bản thân logic điều kiện là mặt hỏng kho này đã trả giá
HAI lần — workflow có `paths:` không chạy ở lần đẩy tạo nhánh mới, và ma trận theo nhãn không bắn
vì `pull_request:` thiếu `types:`."*

**Hệ quả cho packet này: không thêm một mặt điều kiện nào.** Tách job là thêm **jobs**, không
thêm **điều kiện** — phân biệt ấy là ranh giới của packet, và A3 đo nó bằng CẤU TRÚC chứ không
bằng số đếm (xem A3, lý do ở đó).

### Cái giá của việc tách job — ước CÓ ĐƠN VỊ từ số đo cũ, chưa phải phép đo mới

Chia `gate` thành **ba** job trên **cùng một ma trận nền**:

- `gate` — mọi bước trừ hai bước nặng
- `gate-registry` — thiết lập + `test registry`
- `gate-packet-loop` — thiết lập + `packet-loop selftest`

Số học suy từ bảng phân rã (run `34045664423`). Bản đầu gọi bảng này là *"không phải ước lượng"*;
nói cho đúng: nó là **ước có đơn vị** — mỗi ô là tổng của các số đã đo, nhưng chưa có lượt chạy
nào sau tách để đối chiếu, và ba ô thiết lập giả định runner mới tốn đúng bằng runner cũ. Cột
"sau khi tách" tính từ **tổng bước** (`43,17` / `24,20`), cột "hôm nay" là **job** (`43,20` /
`24,25`) — hai mẫu số khác nhau, và chênh `0,11` giữa chúng sẽ hiện ra ở dòng tổng:

| | Windows hôm nay | Windows sau khi tách | ubuntu hôm nay | ubuntu sau |
|---|---:|---:|---:|---:|
| `gate` | 43,20 | 15,77 | 24,25 | 7,42 |
| `gate-registry` | — | **21,03** | — | 14,31 |
| `gate-packet-loop` | — | 13,03 | — | 4,83 |
| **job dài nhất** | **43,20** | **21,03** | **24,25** | **14,31** |
| **tổng phút tường** | 43,20 | 49,83 | 24,25 | 26,56 |

(Bản đầu in `14,32` / `26,57` / `126,23`; `13,13 + 1,18 = 14,31`, nên ba số ấy lệch `0,01` — finding
P3 lượt 1, sửa ở đây. Tỉ lệ `14,1 %` làm tròn giống nhau ở cả hai cách, tức chỉ kiểm tỉ lệ thì
không thấy lỗi số hạng — đúng bài học *"kiểm SỐ HẠNG, đừng kiểm quan hệ"*.)

- **Wall clock job dài nhất: `43,20` → `21,03` phút Windows = −51,3 %.** Biên dưới trần 60 đi từ
  `16,80` lên `38,97` phút. Đây là số của JOB; thời gian người dùng CHỜ cả workflow còn cộng xếp
  hàng của ba runner, chưa đo.
- **Phút TÍNH TIỀN: tăng.** Windows nhân hệ số **×2** (`ci.yml:19-23`): `43,20×2 = 86,40` →
  `49,83×2 = 99,66`. Cộng ubuntu `24,25 → 26,56`. Tổng một lượt, nền là **lượt NHÁNH
  `34045664423`** (bản đầu gọi nhầm là "một lượt master" — lượt master `34048685345` là `111,08`):
  **`110,65` → `126,22` phút tính tiền = +15,57 (+14,1 %)**. Phân rã cái tăng: thiết lập nhân đôi
  theo hệ số `3,33×2×2 + 1,18×2 = 15,68`, trừ `0,11` chênh job−Σbước cũ bị rơi khi vế sau dùng
  tổng bước ⇒ `15,57`.

Khoản tăng ấy là **ba lần trả tiền thiết lập** thay vì một. Nó không phải hiệu ứng phụ mà là
**chính cái giá** của tách job, và nó đụng đúng chỗ kho này đã chết một lần: `ci.yml:19-24` ghi CI
đứng hình từ 12-08-2026 vì cạn hạn mức 2.000 phút/tháng (số của ghi chú 13-08-2026, không phải
hạn mức hiện tại — chưa đọc lại). **Đây là con số chủ kho phải duyệt, không phải con số phiên thi
công tự nuốt.**

### Consumer của `ci.yml` nằm ngoài `ci.yml` — đo được, và nó đổi write set

`loi_ruff_ci()` (`.claude/dev/ci_dang_ky_test.py:140-158`) chỉ đọc `jobs.gate.steps` và đòi bước
`ci_dang_ky_test.py --chay` đứng **sau** bước cài `ruff==0.15.15` **trong chính danh sách ấy**.
Đo 19:33Z 06-09-2026, dựng YAML ba job trong bộ nhớ từ `ci.yml` hiện tại (9 bước thiết lập tới hết
bước Ruff chép sang mỗi job mới, hai bước nặng dời đi, không đổi lệnh nào):

```
loi_ruff_ci(ci.yml hôm nay)   -> ([], 3)
loi_ruff_ci(ci.yml đã tách)   -> (["CI không provision Ruff trước test registry"], 3)
số lời gọi registry còn trong jobs.gate sau tách: 0
```

Tách đúng M1 ⇒ `gate_i = -1` ⇒ bước `test registry` **tự đỏ** ở mục `RUFF CI`, trên cả hai nền.
Bản đầu chỉ khai `ci.yml` trong write set, nên executor **không thể** sửa consumer này — vi phạm
`L2` (verdict lượt 1, P1). Chữa ở `write_set` dưới đây.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng THÊM** — cột `additions` của
`git diff --numstat`, KHÔNG phải `adds − deletes`. Bản đầu lý luận *"chủ yếu di chuyển nên dòng
thêm ròng thấp"*; sai thước: `+351/−351` có ròng `0` mà `additions = 351 > 300` (verdict lượt 1,
P2). Ước ĐÚNG THƯỚC, từ số đo khối (19:31Z, `sed -n | wc -l` trên `ci.yml` 588 dòng):

| khối phải NHÂN ĐÔI (mỗi job mới một bản) | dòng (kể chú thích) | dòng (bỏ chú thích) |
|---|---:|---:|
| đầu job: `strategy`/`matrix`/`runs-on`/`timeout-minutes`/`env` (`ci.yml:35-69`) | 35 | 17 |
| 9 bước thiết lập tới hết bước Ruff (`ci.yml:70-113`) | 44 | 33 |
| **một job mới** | **79** | **50** |
| **hai job mới** | **158** | **100** |

Cộng hai bước dời (≈4 dòng), sửa `loi_ruff_ci` (hàm hôm nay 19 dòng; ước +15–25) và phản chứng
mới (ước +15) ⇒ **ước `135`–`200` dòng thêm**, tuỳ chép hay không chép chú thích. Dưới `300`,
biên ≥ `100`. **Đo thật bằng `git diff --numstat` trước review; vượt `300` thì DỪNG** — và cách
giảm nếu cần là rút phần thiết lập thành composite action (`.github/actions/…`), tức thêm MỘT tệp
(**2 + 1 = 3**, vẫn ≤ 3), không phải cắt bớt bước.
*(Revision 5 đưa write set lên 3 nên lối thoát này thành `3+1=4` và **vi phạm chính A8** —
cross-review lượt 1, P2 `metadata-va-loi-thoat-composite-chua-theo-write-set-r5`. **Revision 7 trả
write set về 2**, nên nó dùng lại được. Ghi lại cả quãng đường vì nó cho thấy một trần chật làm mất
một phương án hợp lệ.)*

Write set là **2 tệp** (revision 7; bản r5 để sót một câu ghi **2** ngay dưới một bảng có **3** —
cross-review lượt 1 bắt, hàng `X7`. Nay hai con số ấy khớp nhau trở lại).

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.github/workflows/ci.yml` | định nghĩa job `gate` và toàn bộ 39 bước của nó (trên `1b3caa1`; `origin/master` `28cb898` đo 22:45Z 06-09-2026 đã là **40** — xem `base_sha`) |
| 2 | `.claude/dev/ci_dang_ky_test.py` | consumer `loi_ruff_ci` khoá cứng `jobs.gate`; tách job mà không sửa nó thì bước `test registry` tự đỏ (đo 19:33Z) |

**`ADR-0044` cho `sensitive`: ≤ 3 tệp.** Hai đường trên để lại **một chỗ trống** — đó là khoảng an
toàn có chủ đích (revision 7), không phải chỗ để nhét thêm việc. Hai packet **cố ý KHÔNG** nằm ở
đây: bản vá bộ chấm đột biến (`ops/nhanh_don_duoc_test.py`) đi bằng
`CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN`, và `t125` đi bằng `T125-RA-JOB-RIENG`.

**`.claude/dev/ci_dang_ky_test.py` ĐANG BỊ GIỮ** — `ai-dang-giu` 09:3xZ 11-09-2026 (sau canh hai
nguồn, `comm -23` RỖNG) ⇒ `rc=11`, `NGƯỜI_GIỮ 1: bo-cong-duyet-khac-danh-tinh-exec-2-claude-20260911`
(packet `#502`). `.github/workflows/ci.yml` ⇒ **`NGƯỜI_GIỮ 0`**.
Nên `depends_on: [wp502]`, và lease của packet này chỉ được cấp **SAU KHI `#502` land** — không phải
sau khi lease kia hết hạn danh nghĩa. Cấp chồng là tự tạo cửa sổ hai writer, đúng thứ write-set
exclusion sinh ra để chặn.

**Và nối tiếp SAU `T125-RA-JOB-RIENG`**, dù hai packet không chồng write set về mặt tệp thứ hai:
cả hai đều ghi `ci.yml`, nên chúng **không chạy song song được**; cộng thêm lý do ở khối REVISION 7 —
nền của `A1`/`A5` chỉ đo được sau khi `t125` ra khỏi đường tới hạn.

Không ký tự đại diện. Không đường dẫn nào khác. Trong tệp #2 chỉ đụng `loi_ruff_ci` và phản chứng
của nó; **không** đụng `bang_chung_xanh`, `MOI`, `MOI_WINDOWS`, `chay_moi` — đó là của ba packet
sau.

**Hệ quả của tệp #2 — giao write set, đổi thứ tự, và lý do chọn thứ tự này.** Tệp #2 cũng nằm trong
write set của `LO-319-LINUX-BANG-CHUNG-XANH`, `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`,
`MUTANT-WINDOWS-NHANH-DON-DUOC`. `§5`: exclusion theo ĐƯỜNG DẪN, không cấp lease theo vùng dòng ⇒
bốn packet **nối tiếp**, không song song như bản đầu khai. Hai thứ tự khả dĩ, chọn **GATE đi ĐẦU**:

| tiêu chí | GATE đầu (`GATE → LO → 2A → 2B`) | GATE cuối (`LO → 2A → 2B → GATE`) |
|---|---|---|
| số tệp / trần `ADR-0044` | 2 / 3 — như nhau | 2 / 3 |
| số đo của GATE (A1/A2/A5) | đo trên cây **chưa đổi**: nền so tập A2 là lượt `workflow_dispatch` TRƯỚC tách tại `start_from_sha` (r3); hai run 39 bước `34045664423`/`34048685345` chỉ còn là đối chiếu lịch sử cho A1/A5 (revision 4) | nền trôi sau ba packet cắt `test registry` (41 % chi phí Windows) ⇒ đo lại cả bảng |
| A7 của 2A/2B (bước `test registry` trên Windows) | viết MỘT LẦN theo bố cục sau tách (`gate-registry`) — đóng finding `acceptance-phu-thuoc-job-packet-khac-doi` bằng cấu trúc | phải viết "tìm bước theo job tại đúng head" và giữ hai trường hợp |
| giá mỗi lượt `workflow_dispatch` Windows của ba packet sau | job dài nhất ≈ `21` phút (ước) | `43,20` phút |
| phần sửa ở tệp #2 | `loi_ruff_ci` — rời `bang_chung_xanh`; ba packet sau rebase không đụng | như nhau |

Cột giữa thắng ở ba dòng có số; không có dòng nào cột phải thắng. Chuỗi điều phối theo đó:
**`#456 → GATE → LO → 2A → 2B`**. Tiền nhiệm trực tiếp của packet này **chính là #456**, nên đường
(a) *"đợi hết hạn"* của `LO-319` mục *"Lease đang giữ"* dùng đúng mốc `14:30:07Z 07-09-2026` với
`thay_the_cho: []`; đường (b) cấp sớm đòi bia mộ hai chiều **đã commit** và readback mọi ref — xem A9.

Đo 17:46Z, **đo lại 21:00Z 06-09-2026 y hệt**: `ai-dang-giu .github/workflows/ci.yml` ⇒
`NGƯỜI_GIỮ 0: không có`; `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 1:
mutant-khong-chay-tren-windows-…` (#456, còn hạn tới `14:30:07Z 07-09`). Quét hai nguồn 19:29Z và
lại 20:59Z: `ls-remote` **298** · `for-each-ref` **298** · `comm -23` rỗng · `comm -13` rỗng ⇒ không mù.

## `ngoai_pham_vi`

1. **`timeout-minutes` — CẤM đụng, theo cả hai chiều.** Không nâng (hai lần nâng đã có, lần kế là
   lần thứ ba theo `§12`), và cũng không hạ để "ép kỷ luật": hạ trần biến một job chậm thành một
   job `cancelled`, tức đổi một vấn đề đọc được thành một vấn đề vô hình. Trần đứng nguyên ở `60`.
2. **Chạy CÓ ĐIỀU KIỆN theo diff / theo nhãn / theo `paths`.** Đã có đặc tả đóng băng
   (`CI-FASTPATH-THEO-DIFF.md`) và bản triển khai đã bị bỏ (PR #247 đóng). Kho đã trả giá hai lần
   cho logic điều kiện của workflow. Không mở lại trong packet này.
3. **Song song hoá TRONG `test registry`** (`chay_moi` chạy 8 bộ tuần tự). Hướng này cắt cả wall
   clock lẫn billing, nhưng: (a) nó chạm `chay_moi` trong `.claude/dev/ci_dang_ky_test.py` — hàm
   có phản chứng bám chữ ký ("ĐƯỜNG NỐI ĐỂ ĐO"), và là vùng ba packet sau sửa; (b) hiệu quả trên
   Windows **chưa đo được** vì không có phân rã theo bộ trên nền ấy; (c) đo trên Linux 17:47Z
   06-09: tuần tự `400` giây, bộ dài nhất một mình `270` giây ⇒ trần song song hoá là `−32,5 %`.
   **Con số ấy KHÔNG đổi sau hai packet mutant-Windows** — bản đầu viết tổng Linux co về `≈284` s
   và trần còn `≈5 %`, nhưng hai packet ấy giữ nguyên vòng đột biến trên Linux (M6/A6 của cả 2A
   lẫn 2B), nên tổng Linux vẫn `400` s (verdict lượt 1, P2 `tiet-kiem-windows-bi-tru-khoi-linux`).
   **Nợ có tên: `SONG-SONG-HOA-TRONG-TEST-REGISTRY`** — mở packet riêng SAU khi có phân rã theo bộ
   trên Windows.
4. **Cắt vòng lặp đột biến của `packet_loop_test.py`.** Bước ấy tốn **9,70** phút Windows
   (22,5 %) so `3,65` ubuntu; tệp `4.733` dòng và nhắc đột biến ở **169 dòng** (đo 17:43Z
   06-09-2026, mẫu `DOT_BIEN|dot_bien|đột biến` phân biệt hoa/thường; 179 lần xuất hiện). Cùng
   hình dạng bản vá với #456 — nhưng nó là `.claude/dev/packet_loop_test.py`, không phải `ci.yml`.
   **Nợ có tên: `MUTANT-WINDOWS-PACKET-LOOP`.**
5. **Bỏ bước trùng** — đã đo, **0 bước trùng** (xem bối cảnh). Không có gì để làm.
6. **Không đổi tập bước, không đổi lệnh của bước nào. KHÔNG NGOẠI LỆ.** Packet này chỉ đổi bước ấy
   nằm trong **job** nào.
   *(Revision 6 từng mở một ngoại lệ hẹp cho cờ của `M9`, vì `M8`/`M9` khi ấy nằm trong packet này
   và **trái chính điều cấm này** — P1 `them-t125-nhung-giu-hop-dong-ba-job`. **Revision 7 đóng lại
   ngoại lệ ấy** bằng cách chuyển `M8`/`M9` sang packet `T125-RA-JOB-RIENG`. Một điều cấm không có
   ngoại lệ thì không ai phải đoán biên của ngoại lệ.)*
7. **Trong `.claude/dev/ci_dang_ky_test.py`: không đụng gì ngoài `loi_ruff_ci` và phản chứng của
   nó.** `bang_chung_xanh`/`MOI`/`MOI_WINDOWS`/`chay_moi` là của `LO-319` và hai packet mutant.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Hai bước nặng nhất (`test registry`, `packet-loop selftest`) chuyển sang job riêng, cùng ma trận nền với `gate`. | `write_set` #1 |
| M2 | **Độ phủ không đổi**: tập `(tên bước, nền, kết luận)` sau khi tách phải bằng đúng tập trước khi tách. Không bước nào biến mất, không bước nào đổi từ `success` sang `skipped`. | `write_set` #1 |
| M3 | Điều kiện chạy KHÔNG đổi: mọi job mới mang **cùng** `if` mức job (hôm nay: không có), cùng biểu thức ma trận `fromJSON(...)`, cùng `timeout-minutes`; mọi bước dời đi giữ nguyên `if` của nó. Không thêm một mặt điều kiện nào — kể cả `if:` viết KHÔNG có dấu nội suy. | `write_set` #1 |
| M4 | `timeout-minutes: 60` giữ nguyên trên **mọi** job. | `write_set` #1 |
| M5 | Phút tính tiền tăng thêm được **đo và công bố**, không phải ước — nó là số chủ kho đã duyệt trước, và lượt chạy phải xác nhận nó. | `write_set` #1 |
| M6 | Bảo vệ nhánh vẫn có cổng: nếu `gate` đang là required status check thì hai job mới cũng phải được khai, kẻo tách job = tháo cổng. | `write_set` #1 (phần đo được) |
| M7 | `loi_ruff_ci` tìm bước `test registry` trong **mọi** job và đòi Ruff được cài trong **cùng job**, **trước** bước ấy; không job nào có bước ⇒ lỗi. Tương thích với `ci.yml` chưa tách. | `write_set` #2 |
*(revision 5 từng có `M8`/`M9` cho `t125`; **revision 7 chuyển chúng sang packet
`T125-RA-JOB-RIENG`** — xem khối REVISION 7. Packet này **không** đụng `t125`.)*

## `nghiem_thu`

**A1 (M1) — job dài nhất giảm, đo bằng PHÚT TƯỜNG CỦA JOB, kèm đầu-cuối của WORKFLOW.**
`workflow_dispatch` `ci.yml` trên nhánh packet. Đòi: `max(thời lượng job)` trên `windows-latest`
**≤ 0,60 × `timeout-minutes`** — hôm nay `timeout-minutes: 60` nên là **≤ 36,00 phút**.

**REVISION 5 — ngưỡng đổi từ SỐ PHÚT sang BIÊN TƯƠNG ĐỐI, và đây là lý do.** r4 khai `≤ 25,00`,
suy từ `21,03 + ~4`. Cả hai số ấy tính trên nền `B = 24,4 s`; đo lại 11-09-2026 `B = 54,6 s`, tức
**gấp 2,24 lần trong 4 ngày** (khối REVISION 5 mục (2)). Một ngưỡng tính bằng phút **hết hạn trước
khi packet kịp land** — đúng `L5`. Bất biến cần giữ KHÔNG phải *"job dưới 25 phút"* mà là
***"còn ít nhất 40 % biên dưới trần"***; bất biến ấy không trôi theo tải. Số phút tuyệt đối vẫn
phải **công bố** làm đối chiếu, chỉ không còn là tiêu chí.
Ràng buộc kèm theo, để biên tương đối không thành cửa hậu: `timeout-minutes` **giữ nguyên 60** (A4).
Nới trần để `0,60 ×` rộng ra là **vi phạm A4**, và `§12` coi việc nâng trần là điều kiện DỪNG.
Đơn vị: **`completed_at − started_at` của JOB**, đọc qua `actions_list` +
`method: list_workflow_jobs`; lấy `max` trên tất cả job của lượt, không lấy tổng.
**Kèm, công bố nhưng không đặt ngưỡng** (chưa có nền): thời gian đầu-cuối của cả lượt
(`run.created_at → run.updated_at` khi `status = completed`) trước và sau tách. Đây là phép đo duy
nhất thấy được xếp hàng của ba runner; nếu nó KHÔNG giảm dù `max(job)` giảm, đó là kết quả đo, báo
chủ kho. **Không quy thời gian chờ thành phút tính tiền** — chờ không tính tiền, và ta chưa có dữ
liệu billing.
Phép làm ĐỎ: `max(thời lượng job)` trên `windows-latest` vượt `0,60 ×` trần.

**REVISION 5 — phép làm ĐỎ của r4 KHÔNG DÙNG ĐƯỢC NỮA, và phải nói thẳng vì sao.** r4 viết
*"gộp lại một job ⇒ `43,20` ⇒ ĐỎ"*. `43,20` là `max(job)` **trước khi tách**, đo khi Windows còn
chạy trọn. Nay job ấy **chưa hoàn tất lần nào** trên `master` kể từ ~07-09: **hai** lượt có số ở
mức job (`60,32` · `60,52` phút) cộng **hai** lượt nữa chỉ đọc `conclusion` mức RUN — cả bốn là
**THUẬT LẠI**, và `duration ≈ 60` cộng `cancelled` **một mình không phân biệt được nguyên nhân
huỷ** (đo 07:0xZ 11-09-2026; revision 6 theo P2 `so-ci-moi-chua-duoc-khai-la-thuat-lai`). Đại lượng ấy là
**`≥ 60`, KHÔNG BIẾT** — bị trần **kiểm duyệt**, không phải bị đo sai. Nên không phát biểu lại nó
bằng một con số; phép làm ĐỎ nay neo vào **biên tương đối**, thứ không cần biết giá trị "trước".
Và: nếu `max` **không** giảm dù đã tách, đó là **KẾT QUẢ ĐO** (chi phí thiết lập trên Windows lớn
hơn `2,75`–`3,27` phút đã đo lại 11-09-2026) — báo chủ kho, đừng nới gì để ép nó xanh.

**A2 (M2) — độ phủ không đổi, đo bằng TẬP HỢP, không bằng số đếm, trên HAI loại cò.**

**REVISION 6 — A2 PHẢI CÓ NHÁNH CHO NỀN BỊ CẮT, nếu không nó mâu thuẫn với A5** (cross-review lượt
1, P1 `a2-doi-giu-ca-ket-luan-cua-nen-bi-cat`). r5 thừa nhận lượt nền trước tách **vẫn có thể bị
cắt** và cho A5 ghi nền `KHÔNG ĐO ĐƯỢC`; A2 thì không có nhánh ấy, vẫn đòi tập **có cột
`conclusion`** của lượt sau bằng đúng lượt nền. Nhưng đúng trong tình huống r5 xử lý, bước chưa chạy
ở nền là `skipped`/`cancelled` còn sau tách làm đúng phải `success` ⇒ **hai tập không thể bằng
nhau**; ép chúng bằng nhau là phá chính điều kiện *"lượt sau hợp lệ"* của A5. Hai tiêu chí loại trừ
nhau, và bản r5 không thể qua được cả hai cùng lúc.

**Nhánh:** nếu lượt nền **hợp lệ** theo A5(1) ⇒ so **tập bộ ba có `conclusion`** như dưới. Nếu lượt
nền **KHÔNG hợp lệ** ⇒ A2 **hạ xuống** so **tập `(tên bước, nền)`** — bỏ cột `conclusion` — và
**đồng thời** đòi lượt SAU có **0** bước `cancelled` và mọi bước `skipped` của nó **giải thích được
bằng `if` của chính bước ấy**. Trạng thái nghiệm thu khi đó là **`ĐẠT CÓ ĐIỀU KIỆN`**, ghi thẳng
vào biên nhận là *"độ phủ chứng minh bằng TÊN BƯỚC, không bằng KẾT LUẬN, vì nền bị cắt"* — **không**
được ghi là ĐẠT trơn.
**Phép làm ĐỎ của nhánh hạ:** một bước biến mất khỏi lượt sau ⇒ tập tên lệch ⇒ ĐỎ (nhánh hạ vẫn còn
răng với ca *"quên chép bước"*, chỉ mất răng với ca *"bước đổi kết luận"* — nói thẳng cái mất).

Lấy `(job, tên bước, nền, conclusion)` của lượt TRƯỚC và của lượt SAU. Bỏ cột `job`, rồi so **tập**
`(tên bước, nền, conclusion)`. Hai tập phải **bằng nhau**. Làm HAI lần:
- (revision 3 — P1 `a2-neo-nen-cu-trai-write-set-hien-tai`, lượt 8) lượt `workflow_dispatch` SAU tách trên nhánh packet (cả hai
  nền) so với lượt `workflow_dispatch` **TRƯỚC tách trên CÙNG nhánh tại `start_from_sha` của lease** (nền `d28c4b1`: **40** bước
  YAML, có `bien-nhan v2 selftest`) — **cùng base, cùng event, cùng lane**; executor phóng lượt nền ấy TRƯỚC khi đẩy commit tách.
  Run master `34048685345` (`1b3caa1`, 39 bước, `push`) chỉ còn là đối chiếu lịch sử: so với nó thì tách đủ bước **không thể**
  khớp (thiếu bộ ba `bien-nhan v2`) còn bỏ bước ấy lại khớp — reviewer lượt 8 dựng phản mô hình, đúng thứ M2 sinh ra để chặn.
  `conclusion` từng mục đọc lại bằng `list_workflow_jobs` khi so, không suy từ phép trừ; base trôi lúc thi công thì lấy lượt nền
  mới cùng cách, không dùng lượt khác event/lane;
- lượt `pull_request` của chính PR packet (ubuntu) so với lượt `pull_request` gần nhất mà `ci.yml` nền BẰNG BYTE `ci.yml` của
  `start_from_sha` (ví dụ lượt `pull_request` của PR #468 tại head ≥ `2adb681`, đã merge `d28c4b1`) — đây là lượt DUY NHẤT
  chứng minh ba job **có mặt trên PR**, tức chứng minh không ai đã thêm điều kiện chỉ-dispatch (xem A3).
Đơn vị: **tập bộ ba**, không phải `wc -l`. Lý do dùng tập chứ không dùng số đếm là bài học đã đo
của kho: hai tập lệch vẫn có thể cùng lực lượng (`CLAUDE.md`, mục `git for-each-ref`).
Phép làm ĐỎ: quên chép `if: runner.os != 'Windows'` sang job mới ⇒ một bước đổi từ `skipped` sang
`success` (hoặc ngược lại) ⇒ tập lệch ⇒ ĐỎ. Mười bước có `if:` là mười cơ hội để hỏng chỗ này.

**A3 (M3) — không thêm mặt điều kiện nào, đo bằng CẤU TRÚC.**
Bản đầu đếm **lực lượng tập chuỗi biểu thức `${{ }}`** — và reviewer dựng được phản chứng: thêm
`if: github.event_name == 'workflow_dispatch'` (KHÔNG có dấu nội suy, cú pháp Actions cho phép)
vào `gate-registry` ⇒ tập biểu thức vẫn `6 → 6`, A3 cũ **PASS**, mà job biến mất trên mọi PR (đo
lại 19:33Z, đúng như reviewer). Đếm delimiter là đếm CÁCH VIẾT, không đếm ĐIỀU KIỆN. Thay bằng ba
phép so, đã chạy 19:33Z trên YAML tách trong bộ nhớ:
1. **mức job**: với mỗi job, bộ ba `(if mức job, chuỗi `matrix.os`, `timeout-minutes`)` sau chuẩn
   hoá khoảng trắng phải **bằng** bộ ba của `gate`. Hôm nay `gate` = `(None, fromJSON(…), 60)`.
   Đo: YAML tách đúng ⇒ ba job bằng nhau; YAML có `if` chèn ⇒ **bắt được** (bộ ba của
   `gate-registry` khác).
2. **mức bước, hai nửa** (đo 19:59Z trên YAML tách trong bộ nhớ; nửa nào cũng có đột biến riêng
   vì mỗi nửa mù đúng chỗ nửa kia thấy):
   - tập `(tên bước, if của bước)` trên **mọi** job sau tách phải **bằng** tập trước tách. Đo:
     tách đúng ⇒ bằng; thêm `if: false` vào bản sao bước Ruff trong `gate-registry` ⇒ **bắt được**
     (`('cài Ruff 0.15.15 và in probe dương', 'false')` xuất hiện); xoá `if` của bước
     `PR head contains required EOL base` trong `gate` ⇒ **bắt được**. Nhưng **xoá hẳn một BẢN
     SAO** của một bước thiết lập khỏi một job mới ⇒ tập **KHÔNG** đổi (tập dedup; `gate` vẫn có
     bước ấy) — đo được, và bản đầu của mục này viết "bắt được" cho một đột biến chưa từng chạm
     bước nào (bước EOL không nằm trong 9 bước được chép), tức lời khai không có phép đo.
   - **tiền tố 9 bước** (theo tên, theo thứ tự) của mỗi job mới phải **bằng** tiền tố 9 bước của
     `gate`. Đo: tách đúng ⇒ bằng ở cả hai job mới; xoá bản sao Ruff khỏi `gate-registry` ⇒
     **bắt được** (`gate-registry: False`). Với riêng Ruff, A7 (`loi_ruff_ci`) cũng bắt.
3. **mức workflow**: `on:` và `concurrency:` không đổi một ký tự (so chuỗi sau `yaml.safe_load` +
   `safe_dump`).
*(Revision 6 thêm một mục 4 — phép chiếu cho bước MỚI của `M8`. **Revision 7 gỡ** vì packet này
không còn thêm bước nào: `A2`/`A3` trở lại so tập **đúng bằng nhau**, đúng như r4. Phép chiếu ấy
chuyển sang `T125-RA-JOB-RIENG`, nơi nó thật sự cần.)*
Đơn vị: **tập bộ ba / tập cặp**, không phải số đếm. Kèm chốt cứng `actionlint`, đo bằng **TẬP CHẨN
ĐOÁN, không bằng `rc`** (verdict lượt 2, P2 `actionlint-so-rc-che-loi-moi`): chạy `actionlint` trên
`ci.yml` của `origin/master` và của nhánh packet trong CÙNG một lệnh, CÙNG môi trường; ghi phiên bản
`actionlint`/`shellcheck`, `rc`, và **toàn bộ** chẩn đoán hai vế (`-format '{{json .}}'`). Chuẩn hoá
mỗi chẩn đoán thành `(tệp, mã/loại — vd `SC1003`, thông điệp, thân `run` của bước chứa nó sau chuẩn
hoá khoảng trắng)` — **bỏ số dòng/cột** vì dời bước làm dòng trôi — rồi so **đa tập** hai vế: delta
phải **RỖNG** (không mất, không thêm). Vì sao không so `rc`: `rc=1 → rc=1` che được lỗi MỚI — phản
mô hình đo 21:22Z 06-09-2026 trên hàm so thuần: vế trước `{SC1003 existing}`, vế sau
`{SC1003 existing, SC2086 new}`, `rc` cùng `1` ⇒ tiêu chí cũ **PASS**, tiêu chí tập ⇒ **ĐỎ**; cùng
lỗi cũ chỉ đổi số dòng ⇒ tập **PASS** (không đỏ oan); đổi lỗi cũ lấy lỗi mới cùng số lượng ⇒ `rc`
PASS, tập **ĐỎ**. Nền: `CLAUDE.md` đo `rc=1` (một finding `SC1003` tại `ops-don-ref.yml:106`) khi có
`shellcheck`, `rc=0` khi vắng — hai nền khác nhau, nên phiên bản công cụ phải nằm cạnh kết quả.
**Vắng `actionlint`, thiếu `shellcheck` hay thiếu log một vế ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ**, không phải
delta 0 (container soạn bản này: `which actionlint shellcheck` rỗng, 20:59Z — lượt này chỉ đo được
phản mô hình; lượt `actionlint` thật là **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**; `t33` của
`ops/lease_publish_test.py` đòi `actionlint` nhưng không đòi `shellcheck`). Phản chứng bắt buộc: chèn
một lỗi shellcheck mới vào workflow đã có một lỗi ⇒ `rc` vẫn `1` ⇒ delta tập **khác rỗng** ⇒ ĐỎ.
Và: **không viết cú pháp `${{ }}` trong comment của `run:`** — kho đã bị GitHub từ chối
cả tệp vì đúng chuyện đó (`ops-don-ref.yml`, run `31971137920`, 0 job, `conclusion: failure`).
Phép làm ĐỎ: bất kỳ phép so nào lệch. Đột biến bắt buộc: chính ca `if` không delimiter ở trên.

**A4 (M4) — trần không đổi, đo bằng GIÁ TRỊ ĐÃ PARSE của TỪNG job.**
`yaml.safe_load(ci.yml)` rồi với **mỗi** `job_id` trong **danh sách job kỳ vọng** (revision 7: **ba**
tên, xem A6), đòi `jobs[job_id]["timeout-minutes"] == 60`. **Thiếu khoá ⇒ ĐỎ.** Giá trị khác `60` ⇒
ĐỎ, kể cả nhỏ hơn. Ngoài ra: không `timeout-minutes` nào ở **mức bước**.

**REVISION 6 — phép đo cũ đếm CHUỖI, không đo được thứ nó nhận canh** (cross-review lượt 1, P2
`a4-dem-chuoi-khong-phai-timeout-tung-job`). `grep -c 'timeout-minutes: 60'` bằng số job **không**
chứng minh từng job được ghim: một chú thích mang chuỗi ấy cũng được đếm, và một job **thiếu hẳn**
khoá `timeout-minutes` **không tạo ra "giá trị khác 60"** nên lọt sạch. Tổng đúng không chứng minh
từng số hạng đúng — đúng họ `L5` mà chính đặc tả này trích. Và A4 là **chốt chống cửa hậu của A1**:
A1 neo vào `0,60 × timeout-minutes`, nên một job thiếu ghim là một đường nới biên không ai thấy.
**Phép làm ĐỎ mới:** bỏ khoá `timeout-minutes` khỏi **một** job ⇒ A4 phải ĐỎ. Phép cũ **XANH** ở
đúng đột biến ấy — đó là lý do đổi.

**A5 (M5) — phút tính tiền được ĐO và công bố, neo đúng lượt.**
Tính `Σ(thời lượng job × hệ số nền)` với hệ số `windows = 2`, `ubuntu = 1`, cho lượt TRƯỚC và
lượt SAU trên cùng bộ bước.
**REVISION 5 — NỀN CỦA A5 NAY KHÔNG ĐO ĐƯỢC. Tiêu chí phải đổi hình, không được giữ số.**

Nền r4: lượt **nhánh** `34045664423` = **110,65**; lượt **master** `34048685345` = **111,08**; ước
sau tách **126,22** (**+14,1 %**); ngưỡng **≤ 135,00**. Cả bốn số ấy đo 06–07-09-2026 và **giữ
nguyên giá trị lịch sử** — nhưng chúng **không tái lập được hôm nay**: `Σ(phút job × hệ số nền)`
đòi một job Windows **HOÀN TẤT**, mà không còn cái nào (xem A1).

**Cạm bẫy phải khai, vì nó trông y hệt thành công.** Tính ngây thơ trên lượt `34563553711`:
`60,52 × 2 + 12,38 × 1 = **133,42**` — **lọt dưới `≤ 135,00`**, trong khi job Windows bị **cắt** và
job Ubuntu **ĐỎ**. Một đại lượng bị **chặn trên** trông hệt một đại lượng **nhỏ**. Ai đọc A5 của r4
mà không nhìn `conclusion` sẽ báo ĐẠT cho một lượt hỏng cả hai job. Cùng họ *"cổng vắng mặt trông
giống cổng xanh"*.

Hình mới của A5 — ba thứ, và thứ đầu là **điều kiện** của hai thứ sau:
1. **TÍNH HỢP LỆ trước, GIÁ TRỊ sau — và "hợp lệ" đòi ĐỦ MẪU, không chỉ đòi mọi mẫu đều xanh.**
   Với **mỗi** lượt, theo thứ tự, dừng ở cái đầu tiên hỏng:
   a. **tập `(job_id, nền)` đọc được phải BẰNG tập kỳ vọng** (revision 6: bốn job × ma trận nền của
      lượt ấy). Thiếu một job ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ;
   b. **danh sách không được RỖNG** — đây không thừa: *"mọi job đều `success`"* **ĐÚNG RỖNG** với
      danh sách rỗng, và tổng khi ấy là `0`, tức một lượt **không đọc được gì** sẽ cho **`Σ = 0`**
      và **lọt qua mọi ngưỡng**;
   c. **phân trang phải cạn** — đọc tới hết, không dừng ở trang đầu;
   d. **cùng `run_attempt`** cho mọi job trong một lượt; trộn attempt ⇒ `KHÔNG ĐO ĐƯỢC`;
   e. **đủ `started_at` và `completed_at`** cho mọi job; thiếu mốc ⇒ `KHÔNG ĐO ĐƯỢC`, không cộng;
   f. rồi mới: **mọi job `conclusion == "success"`**. Một job `cancelled`/`failure`/`timed_out` ⇒
      **`KHÔNG ĐO ĐƯỢC`** ⇒ **ĐỎ**, KHÔNG phải một con số.

   **REVISION 6 — bản r5 chỉ có (f), và (f) một mình đúng rỗng** (cross-review lượt 1, P1
   `a5-hop-le-chua-doi-du-job-va-du-luot`). r5 sửa được ca *job hỏng CÓ TRONG mẫu*, không sửa ca
   *job VẮNG khỏi mẫu* — mà ca thứ hai mới là ca cho ra **tổng thấp giả**.
   **Phép làm ĐỎ cho chính (a)–(e):** bỏ một job Windows khỏi mẫu ⇒ A5 phải `KHÔNG ĐO ĐƯỢC`; với
   bản r5 nó **ĐẠT** và in một con số nhỏ. Đó là phản chứng bắt buộc.
   **Một manifest phép đo dùng CHUNG cho A2 và A5** — cùng `run_id`, cùng `run_attempt`, cùng tập
   job — để hai tiêu chí không đọc hai mẫu khác nhau rồi cùng báo xanh.
2. Lượt **SAU tách** phải hợp lệ theo (1), rồi công bố `Σ(phút job × hệ số nền)` (`windows = 2`,
   `ubuntu = 1`).
3. Lượt **TRƯỚC** — nền để so — **phải được sinh lại tại lúc thi công** trên `start_from_sha` của
   lease, và cũng phải hợp lệ theo (1). Nếu nó **không thể** hợp lệ (job Windows chưa tách vẫn chạm
   trần), thì đó chính là **kết quả đo**: khai `KHÔNG ĐO ĐƯỢC` cho vế TRƯỚC, công bố vế SAU, và
   **báo chủ kho** — đừng chép lại `110,65` của r4 làm nền, vì nó thuộc một cây và một tải khác.
Đơn vị: **phút tính tiền** = Σ phút tường của job × hệ số nền. Đo lại cả hai nền tại lúc thi công.
**Phép làm ĐỎ (revision 6):** bất kỳ điều kiện nào của (1) hỏng ⇒ **`KHÔNG ĐO ĐƯỢC`** ⇒ ĐỎ. Khi cả
hai lượt hợp lệ thì **công bố** `Σ` của cả hai và **tỉ lệ tăng**; **KHÔNG có ngưỡng số** — `135,00`
của r4 là **lời khai lịch sử**, đã hết hạn cùng nền `110,65` sinh ra nó. Số tăng thêm là thứ chủ kho
đọc và quyết, không phải thứ một reviewer đối chiếu với một hằng số đã chết.
**Tiêu chí này KHÔNG được bỏ dù A1 xanh.** Packet này mua wall clock bằng billing; một lượt đo
chỉ nói nửa đầu là một lời khai thiếu nửa sau, và nửa sau là thứ đã giết CI của kho một lần.

**A6 (M6) — cổng không bị tháo khi tách.**
`docs/PROTOCOL_DA_PHIEN.md` và `ci.yml:206` khai nợ có tên `PLAT-X5-required-status-check`:
selftest **không thể** tự chứng minh job được GitHub gọi. Nên A6 là **hai phần, và phần thứ hai
KHÔNG đo được từ phiên thi công**:
- (a) đo được: bản vá phải in ra danh sách tên job mới, đúng dạng chuỗi mà branch protection dùng;
- (b) **không đo được từ phiên**: branch protection phải được cập nhật để require **cả BA** job —
  `gate` · `gate-registry` · `gate-packet-loop`. Đây là việc của chủ kho.
  **Packet `T125-RA-JOB-RIENG` thêm job thứ TƯ và mang theo nghĩa vụ ấy của riêng nó** — require ba
  trong khi có bốn là để kết quả `t125` nằm ngoài hợp đồng bảo vệ nhánh, đúng cái bẫy mục này mô tả
  ở câu dưới. Hai packet nối tiếp ⇒ chủ kho cập nhật branch protection **HAI lần**, mỗi lần một job
  mới; khai thẳng ở đây để lần thứ hai không bị quên.
Phép làm ĐỎ cho (a): tên job trong `ci.yml` khác tên in ra ⇒ ĐỎ.
Cho (b): **không có phép đo** — ghi thẳng, và nó phải nằm trong thân Issue như một mục chủ kho
phải làm TRƯỚC khi merge. Tách một job đang được require thành ba job mà chỉ require một là
**tháo cổng bằng một thao tác trông như tối ưu hoá** — cùng họ dấu bỏ-qua-CI làm PR #100 có 0
check mà vẫn `mergeable_state: clean`.

**A7 (M7) — consumer `loi_ruff_ci` đọc được bố cục mới và vẫn có răng.**
**4** ca — fixture DỰ KIẾN, chưa thi công, chưa ca nào xanh (reviewer lượt 2 mới đo consumer
trước/sau tách trên YAML trong bộ nhớ, `workflow.json`) — đi qua chính `loi_ruff_ci(source)`:

| # | fixture (tên đề nghị) | đầu vào | phải trả | đo trên hàm CŨ, 19:33Z 06-09 |
|---|---|---|---|---|
| 1 | `ruff-ci-chua-tach-tuong-thich-lui` | `ci.yml` hôm nay (chưa tách) | `[]` | `[]` |
| 2 | `ruff-ci-da-tach-dung` | tách đúng: Ruff trong `gate-registry`, trước `test registry` | `[]` | **1** lỗi ← ca đổi màu của packet |
| 3 | `ruff-ci-da-tach-thieu-ruff` | tách, **bỏ** bước Ruff khỏi `gate-registry` | ≥ 1 lỗi | — |
| 4 | `ruff-ci-da-tach-ruff-sau-registry` | tách, Ruff nằm **sau** `test registry` cùng job | ≥ 1 lỗi | — |

Hai phản chứng sẵn có `ruff-pin-required` và `ruff-version-probe-required` giữ nguyên màu.
Đơn vị: **số thông điệp lỗi trả về**. Phép làm ĐỎ: đột biến `loi_ruff_ci` quay về đọc
`jobs.gate` ⇒ ca thứ hai ĐỎ.

**A8 — không đụng gì khác.** `git diff --numstat` chỉ hiện đúng **3** đường dẫn (revision 5:
`ops/lease_publish_test.py` nhập write set cho M8/M9), và cột thêm ≤ `300`.
**3 tệp là ĐÚNG TRẦN `ADR-0044` cho `sensitive`**, không dư chỗ nào ⇒ đường thứ tư ⇒ **DỪNG và hỏi
chủ kho**, không tự xin ngoại lệ.

**A9 — KHÔNG lease nào còn giữ write set TRƯỚC khi bắt tay, đo trên MỌI bản bằng `ai-dang-giu`.**

**REVISION 5 — người giữ đã ĐỔI, và write set rộng thêm một đường.** Đo 06:40Z 11-09-2026, sau khi
canh hai nguồn ref (`comm -23` RỖNG) và dựng nhánh cục bộ cho mọi nhánh máy chủ — công cụ quét
`refs/heads/*`, nên thiếu nhánh cục bộ cho ra `CHAN [12]` chứ không phải `NGƯỜI_GIỮ 0`, và đọc nhầm
chỗ này là tự cấp cho mình một câu trả lời sai:

```
.github/workflows/ci.yml          rc=0   NGƯỜI_GIỮ 0: không có
ops/lease_publish_test.py         rc=11  NGƯỜI_GIỮ 1: m9-fetch-auth-exec-1-claude-20260911
```

⇒ Người chặn hôm nay là **`#503`** (`M9-FETCH-AUTH`, hạn `17:00:00Z 11-09-2026`), **không** còn là
`#456`. `depends_on: [wp503]`, và lease cấp **SAU KHI #503 land** — không phải sau khi hạn danh
nghĩa trôi qua. Đoạn về `#456` bên dưới giữ nguyên làm **lời khai lịch sử** của r2–r4; mốc
`14:30:07Z 07-09-2026` trong đó **đã qua từ lâu** và không còn là điều kiện của packet này.

*(Lời khai lịch sử r2–r4:)*
`python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py` (và `… .github/workflows/ci.yml`)
phải in `NGƯỜI_GIỮ 1` với tên lease của **packet này**, và **0** dòng mang
`mutant-khong-chay-tren-windows-…` mà thiếu `ĐÃ_BỊ_THAY_THẾ` lẫn `HẾT_HẠN`. Vì packet này đi đầu, tiền
nhiệm trực tiếp của nó **chính là #456**, nên mốc `14:30:07Z 07-09-2026` là mốc đúng cho đường (a)
— đo mô phỏng 21:02Z 06-09-2026 trên tập ref thật: `NGƯỜI_GIỮ 1 → 0` đúng tại giây ấy. Đường (a) đòi
`thay_the_cho: []` — giữ tên #456 ⇒ `check rc=8` tới khi có bia mộ, vì `_kiem_bia_mo` không miễn cho
`HẾT_HẠN` (đo 21:02Z). Đường (b) — cấp trước hạn — đòi bia mộ hai chiều **đã commit** và mọi ref còn
giữ blob cũ được xử với readback: hai nhánh 0-ahead xoá được qua `ops-don-ref.yml`, ba nhánh
`claude/**` với `1/1/38` commit ngoài master thì workflow ấy từ chối — điều kiện đủ ở `LO-319` mục
*"Lease đang giữ"* (b), không chép lại để khỏi trôi. `check rc=0` **không** thay được phép đo này:
`check` không chặn chồng lấn write set (đo 21:02Z: `thay_the_cho: []` + sáu ô điền tạm ⇒ `rc=0` ngay
khi #456 còn giữ).

*(revision 5 từng có `A10`/`A11` cho `M8`/`M9`; **revision 7 chuyển chúng sang packet
`T125-RA-JOB-RIENG`**. Phần dưới đây giữ lại làm lịch sử, KHÔNG còn là tiêu chí của packet này.)*

**~~A10 (M8)~~ — `t125` ra khỏi đường tới hạn, đo bằng THỜI LƯỢNG BƯỚC, không bằng sự có mặt của job.**
Sau tách, bước `lease-publish selftest` trong job `gate` phải tốn **≤ 0,45 ×** thời lượng của chính
nó ở lượt nền cùng cách (biên tương đối, cùng lý do như A1: `0,45` chọn từ cấu trúc `TỔNG ≈ 3 × B`
⇒ bỏ `t125` còn `≈ 1/3`, cộng biên; **không** chọn từ một con số phút).
Đơn vị: **giây của BƯỚC**, đọc qua `list_workflow_jobs`, trên `windows-latest`.
Phép làm ĐỎ: để `t125` lại trong job `gate` ⇒ tỉ lệ `≈ 1,00` ⇒ ĐỎ.
**Đột biến bắt buộc:** cho job `t125` chạy nhưng **không** cho job `gate` bỏ `t125` ⇒ A10 phải ĐỎ —
không có đột biến ấy thì không biết A10 đang đo VIỆC BỎ hay chỉ đo sự tồn tại của job mới.

**A11 (M9) — cơ chế bỏ `t125` phải FAIL-CLOSE, và cờ bỏ KHÔNG được đếm là ĐẠT.**
Hai nửa, mỗi nửa một phản chứng riêng:
1. **Thiếu job ⇒ ĐỎ.** Xoá job `t125` khỏi `ci.yml` trong khi job `gate` vẫn mang cờ bỏ ⇒ phải có
   một cổng ĐỎ. Phép làm ĐỎ: không cổng nào đỏ ⇒ A11 ĐỎ. Đây là chốt chống đúng bệnh
   *"một job CI mặc định SKIP là một cổng KHÔNG TỒN TẠI"* mà kho đã trả giá.
2. **Cờ bỏ ⇒ BỎ QUA có lý do, KHÔNG phải ĐẠT.** Chạy `lease_publish_test.py` với cờ mới ⇒ dòng
   tổng kết phải khai **`145/146 · bỏ qua = 1`**, và `t125` nằm trong danh sách BỎ QUA kèm lý do.
   Phép làm ĐỎ: cờ làm `t125` `return` im lặng rồi được đếm ĐẠT (`146/146`) ⇒ A11 ĐỎ.
   **Cờ `--ab-con-noi-bo` sẵn có KHÔNG được dùng lại cho việc này**: nó làm `t125` `return` và **vẫn
   đếm ĐẠT** — đo được, và đó đúng là bệnh *"ca có MẶT khác ca có ĐO"*. Phải là **cờ MỚI**, tên khác,
   ngữ nghĩa khác.

## `hinh_dang_ke_thua`

Chép từ `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md`, `ops/specs/CI-CAI-JSONSCHEMA-r3.md` và từ
chú thích của chính `ci.yml`. Mỗi dòng ghi thời điểm đo hoặc nguồn trích (L5):

| hình dạng | số lần đã gặp | đo/trích lúc (đọc lại 21:03Z 06-09-2026 trên `b1c2284`) | ghi chú |
|---|---:|---|---|
| **(r5)** con số trong đặc tả **hết hạn** giữa lúc viết và lúc dùng | **8** | 4 của `#250` trích `CLAUDE.md` (`117/100`→`120/110` · `37`→`39` · `3/90`→`3/100` · `4/120`→`5/121`); **4 mới** đo 07:0xZ 11-09-2026 trên chính đặc tả này (`B` `24,4`→`54,6` s · `lease-publish` `2,94×`→`≥7,8×` · nền A5 `110,65` ⇒ KHÔNG ĐO ĐƯỢC · người giữ `#456`⇒`#503`) | Lần thứ **5–8** của cùng một hình dạng, và lần này nạn nhân là **chính packet sinh ra để đo CI**. `§12` đòi xem lại CÁCH LÀM: câu trả lời của r5 là **neo tiêu chí vào BIÊN TƯƠNG ĐỐI** (A1, A10), không vào số phút. |
| **(r5)** đại lượng bị **CHẶN TRÊN** trông giống đại lượng **nhỏ** | **1** | đo 07:0xZ 11-09-2026 | `60,52 × 2 + 12,38 = 133,42` lọt dưới ngưỡng `≤ 135,00` của r4 trong khi job Windows `cancelled` và job Ubuntu `failure`. Lý do A5 của r5 đòi **TÍNH HỢP LỆ trước, GIÁ TRỊ sau**. Cùng họ *"cổng vắng mặt trông giống cổng xanh"*, đổi đối tượng. |
| **(r5)** cờ làm một ca `return` im lặng rồi **vẫn đếm ĐẠT** | **1** | trích `ops/lease_publish_test.py` (`--ab-con-noi-bo`), đọc 06:3xZ 11-09-2026 | Lý do A11 đòi **cờ MỚI** và đòi `t125` hiện ra ở danh sách **BỎ QUA**, không phải ĐẠT. Bệnh *"ca có MẶT khác ca có ĐO"*. |
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức `25`→`45`→`60`) | `git log -G 'timeout-minutes:' -- .github/workflows/ci.yml` chạy lại 21:03Z 06-09-2026: `9e4f361` (2026-07-09) · `6d88a2c` (2026-08-29 03:29Z) · `7657bfd` (2026-08-29 04:49Z) | Bản đầu chép `3` từ #456 (đếm mức). Lần kế là lần thứ ba ⇒ `§12` đòi xem lại CÁCH LÀM; câu trả lời ở đây là **tách job**, không phải trần. Điều kiện DỪNG. |
| thêm một mặt ĐIỀU KIỆN vào workflow rồi nó vắng mặt lặng lẽ | **2** | trích `ci.yml:490-506` và `CLAUDE.md` (mục *"Workflow có `paths:`"*, mục nhãn `windows`), đọc lại 21:03Z 06-09-2026; hai sự kiện GitHub không readback lại | `paths:` không bắn ở lần đẩy tạo nhánh mới · `pull_request:` thiếu `types:` nên nhãn `windows` không sinh lượt chạy. Cộng lần thứ ba suýt xảy ra: `CI-FASTPATH-THEO-DIFF` (PR #247 đóng). ⇒ `ngoai_pham_vi` #2, và A3 đo bằng cấu trúc. |
| cổng vắng mặt trông giống cổng xanh | **≥ 3** | trích `CLAUDE.md` (dấu bỏ-qua-CI / PR #100; job `cancelled`; `ops-don-ref.yml` run `31971137920`), đọc lại 21:03Z 06-09-2026; số run tương ứng không readback từ GitHub ở lượt này | dấu bỏ-qua-CI (PR #100, 0 check `clean`) · job `cancelled` không phải `failure` · `ops-don-ref.yml` bị GitHub từ chối, 0 job. Tất cả là lý do A2 so TẬP và A6 tách hai phần. |
| khai một phép đo là `KHÔNG ĐO ĐƯỢC` rồi để nguyên | **1** | trích `ops/specs/CI-CAI-JSONSCHEMA-r3.md:135-160` (A5), đọc lại 21:03Z 06-09-2026 | #456 sinh ra số đo Windows đầu tiên. Ba mục `chua_do_duoc` của #456 — trạng thái TỪNG MỤC ở bảng dưới. |
| tối ưu hoá CI mà không nêu phút TÍNH TIỀN | **CHƯA XÁC MINH** (bản lượt 2 ghi `1`; rút vì nguồn dẫn không chứng minh LOẠI sự kiện — verdict lượt 3, P3 `thieu-bo-dem-quyet-dinh-billing`, mở lại từ lượt 2) | nguồn duy nhất đã đọc: `ci.yml:19-24` (ghi chú 13-08-2026), đọc lại 21:03Z và 22:3xZ 06-09-2026 — nó ghi MỘT sự cố **cạn quota** (CI đứng hình từ 12-08-2026 vì cạn 2.000 phút/tháng; số của ghi chú, không phải hạn mức hiện tại), KHÔNG ghi một quyết định tối ưu hoá nào, có hay không kèm phút tính tiền | Sự cố cạn quota là sự kiện KHÁC LOẠI với thứ dòng này đếm; ghi riêng ở cột nguồn, không đếm vào cột số. Không đổi thành `0`: "không có nguồn đúng loại" không phải "không xảy ra". Chỉ ghi số khi có biên nhận/quyết định gốc chứng minh đúng thuộc tính "không nêu phút tính tiền". ⇒ A5 (đo và CÔNG BỐ phút tính tiền) vẫn bắt buộc, không phụ thuộc con số này. |
| đếm biểu thức thay vì đếm điều kiện | **1** (bản đầu A3 của chính đặc tả này) | verdict lượt 1, tái hiện 19:33Z; đọc lại 21:03Z 06-09-2026 | Cùng gốc *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"* trong `CLAUDE.md`. |
| so `rc` thay vì so tập kết quả | **1** (bản lượt 1 A3 của chính đặc tả này) | verdict lượt 2; phản mô hình đo 21:22Z 06-09-2026 | Cùng họ với dòng trên: một số tổng che được hai tập khác nhau. Sửa ở A3. |
| lời khai rộng hơn phép đo | **3** (bản đầu: "không có chi phí ẩn", "không phải ước lượng"; bản lượt 1: "43/43 bước chạy được" cho số mục liệt kê) | verdict lượt 1, lượt 2; đọc lại 21:03Z 06-09-2026 | Sửa ở bối cảnh và các bảng (đơn vị "mục liệt kê"). |

### Ba mục `chua_do_duoc` của #456 — trạng thái TỪNG MỤC, không gộp

Bản đầu viết *"ba mục nay đóng được"* trong khi bảng của chính nó ghi ba trạng thái khác nhau
(verdict lượt 1, P2). Đúng là: **1 ĐÓNG · 1 ĐÓNG MỘT PHẦN · 1 KHÔNG ĐÓNG**.

| mục của #456 | trạng thái sau #456 |
|---|---|
| #1 *"tổng thời gian thật của job Windows"* | **ĐÓNG.** `43,20` phút, run `34045664423`, job `success`, 43 mục liệt kê / 6 `skipped` (đọc 17:41Z 06-09). |
| #3 *"tỉ lệ 3× là đo TỔNG BƯỚC, không đo riêng đột biến"* | **ĐÓNG MỘT PHẦN.** Ước `44,3p → ~14p` cho `test registry`; thật là `17,70`. Ước lệch `+26 %` về phía đắt hơn. Vẫn chưa có phân rã theo bộ trên Windows. |
| #4 *"không có đường đo Windows tại chỗ"* | **KHÔNG ĐÓNG.** Vẫn đúng, xem `chua_do_duoc` #2 dưới đây. |

## `chua_do_duoc`

0. **(r5) KHÔNG CÓ NỀN "TRƯỚC KHI TÁCH" HỢP LỆ, và chưa biết bao giờ có lại.** `max(job)` Windows và
   `Σ` phút tính tiền của một lượt **chưa tách** đều đòi job Windows **hoàn tất** — mà nó chạm trần
   **bốn lượt liên tiếp** (đo 07:0xZ 11-09-2026). Nên vế TRƯỚC của A5 có thể **vĩnh viễn** là
   `KHÔNG ĐO ĐƯỢC` cho tới khi packet này land, tức **packet tự nó là điều kiện để đo nền của
   chính nó**. Đó là một vòng, và đặc tả khai thẳng thay vì giấu: A5 mục (3) cho phép công bố vế
   SAU cùng một vế TRƯỚC `KHÔNG ĐO ĐƯỢC`, **không** cho phép chép `110,65` của r4 làm nền.

0a. **(r6) SỐ BENCHMARK KHÔNG CÓ HIỆN VẬT — không ai tái lập được** (cross-review lượt 1, P2
   `benchmark-moi-thieu-hien-vat-neo-luot`). `B` (`24,4`/`54,6` s), `TỔNG` (`75,3`/`177,0` s),
   `114,10` s của `t125`, và tử số `2,44` s của `E1` **chỉ có trong văn xuôi**: kho không có lệnh
   benchmark đầy đủ, cấu hình rig, `rc`, số ca đạt/bỏ qua, hay mốc từng lượt. Reviewer xếp chúng
   **`KHÔNG ĐO ĐƯỢC`** — và đó là nhận xét đúng về **HỒ SƠ**, không phải về con số.
   Hệ quả đã sửa tại chỗ: cận suy được từ `177,0` s và `≥ 22,7` phút là **`≥ 7,69×`**
   (`22,7 × 60 ÷ 177,0 = 7,694915`), **không phải `≥ 7,8×`** như r5 viết.
   **Nợ:** phiên thi công phải bàn giao hiện vật benchmark (lệnh + rig + `rc` + mốc) cùng với số,
   hoặc khai `KHÔNG ĐO ĐƯỢC` — đừng đưa số trần.

0b. **(r5) Tải còn tăng, và không ai đang canh tốc độ ấy.** `B` gấp `2,24` lần trong `4` ngày;
   `t26`+`t27` tốn `20,7 ms/biên nhận` (đo 06:0xZ 11-09-2026 trên 118 biên nhận), nhân `≈10` cho nền
   Windows và nhân `3,24` cho bội `t125` ⇒ `≈ 0,67 s/biên nhận` trên đường tới hạn
   (`20,7 × 10 × 3,24 = 671` ms; bản nháp r5 viết `0,62` — sai số học, sửa tại chỗ). Mỗi packet ghi
   sổ thêm biên nhận. **Chưa có cổng nào canh ngân sách này** — nợ, chưa có tên, không thuộc phạm vi
   packet này.

1. **Chi phí thiết lập trên Windows sau khi tách chưa ai đo.** `3,33` phút là đo của **một** job
   (r5 đo lại: `2,75`–`3,27` phút, 11-09-2026 — chưa vượt).
   Job mới có thể tốn khác (cache runner, thứ tự cấp máy, ba lần checkout `fetch-depth: 0`). Mọi
   con số ở bảng "cái giá" là **ước có đơn vị từ số đo cũ**, không phải phép đo mới. A1 và A5 là
   hai phép đo trả lời câu ấy — và nếu chúng ĐỎ thì đó là kết quả, không phải thất bại.
2. **Không có đường đo Windows tại chỗ.** Container Linux. Mọi khẳng định về Windows đi qua CI.
   Kế thừa nguyên vẹn từ #456 `chua_do_duoc` #4.
3. **ĐÃ ĐÓNG MỘT PHẦN — có mười một lượt (5 master + 6 nhánh), biên độ `10,28` phút.**
   **REVISION 6 — MỌI CÂU "A1 giữ `≤ 25,00`" TRONG MỤC NÀY LÀ LỜI KHAI LỊCH SỬ CỦA r2–r4, KHÔNG CÒN
   HIỆU LỰC.** Ngưỡng hiện hành là **`≤ 0,60 × timeout-minutes`** (A1, revision 5). Bản r5 đổi A1
   nhưng để mục này nói `≤ 25,00` ở **thì hiện tại**, nên hai reviewer có thể đưa verdict khác nhau
   cho cùng một lượt — cross-review lượt 1 bắt (P2 `r5-con-giu-nguong-cu-trong-dieu-kien-hien-hanh`).
   Ở đâu trong tệp này còn `25,00` hay `135,00` thì đọc là **lịch sử**; hợp đồng hiện hành chỉ có
   **một** ngưỡng cho A1 và **không** có ngưỡng số cho A5.
   Bản đầu viết *"chỉ có HAI lượt chạy trọn"*, bản hai *"chín lượt, biên độ 9,42"*, bản ba *"mười một lượt master,
   phương sai… ngưỡng A1 phải nới theo phương sai ĐO ĐƯỢC"*. Revision 2 (lượt 7, P2 `bien-do-khac-head-khong-phai-nhieu-runner`)
   rút câu cuối: biên độ là **khoảng biến thiên của một mẫu tiện tay gộp khác tải và khác nhánh**, không phải phương sai
   và không đo được nhiễu runner riêng. Hệ quả: **A1 đứng nguyên `≤ 25,00`**; kết quả thật được BÁO đúng như đo (A1 đã
   nói ĐỎ là KẾT QUẢ ĐO); muốn ngưỡng khác thì revision có thẩm quyền, không nới tại chỗ. Cái chưa đóng: chưa có phép so
   **cùng head, cùng tập bước, cùng event** để tách nhiễu runner khỏi tải — nợ có tên `NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`.
4. **Thứ tự nay CỐ ĐỊNH, nên nền của packet này đứng yên — nhưng nền của ba packet sau thì
   không.** GATE đi đầu ⇒ A1/A2/A5 đo trên cây chưa bị ba packet mutant-Windows đổi; đổi lại, ba
   packet ấy phải đo A7 của mình trên bố cục ĐÃ TÁCH (`gate-registry`), và đặc tả của chúng đã viết
   như vậy. Vẫn phải ĐO LẠI A1/A5 ngay trước khi merge, vì master có thể trôi vì lý do khác.
5. **Không đo được branch protection từ phiên.** `PLAT-X5-required-status-check`. Xem A6(b).
6. **Không đo được hệ số nhân thật của Windows.** `×2` lấy từ chú thích `ci.yml:19-23`
   (r245, 13-08-2026), không từ hoá đơn. Nếu hệ số đã đổi thì con số phút tính tiền ở A5 sai theo
   hệ số ấy — nhưng **chiều** của kết luận (tách job làm tăng billing) không đổi.
7. **Đường (b) — cấp trước `14:30:07Z 07-09-2026` — chưa có readback nào chứng minh hoàn tất được từ
   packet này** (ba nhánh `claude/**` `1/1/38` commit ngoài master, `ops-don-ref.yml` từ chối). Đường
   (a) đo được bằng công cụ hiện có với đúng mốc ấy vì GATE đi đầu — xem A9 và `LO-319`
   `chua_do_duoc` #5. Chủ kho chọn, ghi vào `granted_on_instruction`.
8. **Xếp hàng và độ trễ đầu-cuối của workflow chưa có nền.** A1 công bố số này lần đầu; không
   có ngưỡng vì không có lượt nào trước để so cùng đơn vị.
