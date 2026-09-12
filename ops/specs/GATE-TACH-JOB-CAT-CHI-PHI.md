# Đặc tả packet — GATE-TACH-JOB-CAT-CHI-PHI (revision 12)

- `packet_id`: **GATE-TACH-JOB-CAT-CHI-PHI**; ID bền theo `PROTOCOL §3.2` là `wp<packet_issue>`.
- `packet_issue`: **#463**
- `mission_issue`: **#467** (*"bốn packet treo sau #456: GATE → LO-319 → 2A → 2B"*)
- `revision`: **12** · `generation`: 1 · soạn **11:3xZ 11-09-2026**
- `depends_on`: **`[wp502, wp504]`** — xem `write_set`. **`wp504`** là `WINDOWS-LEASE-SUITE` (lease
  sống, cấp `14:05Z 11-09-2026`), **KHÔNG** còn là `T125-RA-JOB-RIENG`: đặc tả ấy đã **RÚT** vì `#504`
  nhận cùng vấn đề bằng đường chủ kho chọn (song song hoá `t125` trong bộ test, giữ nguyên ngữ nghĩa)
  thay vì tách job. **Packet này không được cấp lease trước khi cả hai land.**
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (`.github/workflows/` — `PROTOCOL §8` loại trừ
  tường minh khỏi patch-as-hint; đây là ĐỊNH NGHĨA của cổng, không phải mã dưới cổng)
- `base_sha`: đo lại tại lúc cấp lease. Ba mỏ neo (`base_sha` · `start_from_sha` ·
  `reviewed_sha_required`) **phải đo lại**, không chép số của lúc soạn.

> **Tệp này KHÔNG thuật lại lịch sử của chính nó.** Vết revision 1–8 và các lượt cross-review nằm ở
> `#463`, `#468`, `#508` và `git log`. Đặc tả là **hợp đồng ở các trường `§3.2`**, không phải nhật ký.
> Mọi câu ở đây phát biểu ở **thì hiện tại** và đang hiệu lực; **không câu nào là "lời khai lịch sử"**.
> Bản trước chồng 9 khối REVISION (`648 → 1056` dòng) và chính lớp ấy sinh ra 4/11 finding của
> cross-review lượt 3 — lớp đã đóng bằng KIẾN TRÚC, không bằng bản vá.

---

## `nguon_cap_viec`

Nợ mà chính `ci.yml` tự khai. `.github/workflows/ci.yml:63`, nguyên văn:

> **NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN**: gate 22 phút và đang lớn dần là **nợ riêng**.

`ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` (`#456`) để dành đúng nợ ấy và khai lý do hoãn: khi
`#456` được soạn, tổng thời gian Windows thật **chưa ai đo** vì job luôn bị cắt ở trần. `#456` đã land
và sinh ra số đo ấy. Packet này là chỗ số đo được dùng.

## Bằng chứng — ba mức, khai riêng, mỗi số một đơn vị

### ĐO ĐƯỢC, có hiện vật tái lập

Mọi phép đo dưới đây là **đọc-only qua REST `/repos/…/actions`**; **không lượt CI nào được phóng**.

| # | khẳng định | giá trị | hiện vật / cách tái lập | đo lúc |
|---|---|---|---|---|
| G1 | job `gate (windows-latest)` trên `push`/`master`, 28 lượt đã kết thúc | **18 `success` · 8 `cancelled` · 2 `failure`** | `do509/do-nen-windows.txt` | 10:5xZ 11-09 |
| G2 | **nền hoàn tất gần nhất** | run `34429604548`, head `28ba133`, `10-09T02:28Z`, job **40,63** phút `success` | cùng hiện vật G1 | 10:5xZ 11-09 |
| G3 | phân rã nền G2 — hai bước packet này tách | `test registry` **13,92** phút (**34,3 %** job) · `packet-loop selftest` **7,42** phút (**18,3 %**) ⇒ cộng **21,34** phút = **52,5 %** | `GET /actions/runs/34429604548/jobs`, `steps[].started_at/completed_at` | 10:5xZ 11-09 |
| G4 | `max(job)` Windows của nền G2 so ngưỡng `A1` | **40,63 > 36,00** ⇒ nền **đã vượt** ngưỡng hiện hành | tính từ G2 | 11:3xZ 11-09 |
| G5 | required status check của `master` **hôm nay** | **đúng MỘT context**: `gate (ubuntu-latest)` | `GET /repos/…/rules/branches/master` ⇒ ruleset `bao-ve-cong-dang-lease` id `20856202`, `enforcement: active` | 10:4xZ 11-09 |
| G6 | toán hạng ngữ cảnh mà `matrix.os` thật sự đọc | `github.event_name` · `github.ref` · `github.event.pull_request.labels.*.name` — **KHÔNG** có `inputs` | `yaml.safe_load` trên `origin/master:.github/workflows/ci.yml` | 10:5xZ 11-09 |
| G7 | `jobs` của `ci.yml` hôm nay | **1** — `gate`; `if` mức job `None`; `timeout-minutes` `60`; **40** bước | cùng phép parse G6 | 10:5xZ 11-09 |
| G8 | phút TÍNH TIỀN của **8** lượt `cancelled` ở G1, **không lượt nào cho kết quả hoàn tất hợp lệ** | Σ thời lượng job = **482,55** phút × hệ số windows `2` = **965,10** phút = **48,3 %** hạn mức Free `2.000` phút/tháng | G1; `run_id` `34576916278` `34568864158` `34563553711` `34552510232` `34549206309` `34439063235` `34033930149` `34023635399` | 11:0xZ 11-09 |

### THUẬT LẠI — số GitHub Actions, `run_id` là mỏ neo truy tìm

| # | khẳng định | giá trị |
|---|---|---|
| G9 | hai lượt `cancelled` có số mức job | `34563553711` **60,52** phút · `34552510232` **60,32** phút |
| G10 | `test registry` trên các lượt sau `#492` | `15,48` · `15,93` · `20,53` · `17,27` · `16,67` phút |

**Phát biểu đúng phạm vi, vì bản trước khai rộng hơn phép đo:** G1 đếm **8** lượt `cancelled` trên
**28** lượt đã kết thúc, và **18** lượt `success`. Bản trước viết *"chưa hoàn tất lần nào"* và
*"bốn lượt chạm trần"* — **cả hai đều sai**, đo được ở G1. Một lượt `cancelled` với
`duration ≈ 60` **không một mình chứng minh** nguyên nhân huỷ là timeout của job; chỉ hai lượt ở G9
có số mức job.

### ƯỚC CÓ ĐIỀU KIỆN — không phải phép đo

Tách hai bước của G3 ra khỏi job `gate`, dưới tải của nền G2:

```
gate              = 40,63 − 21,34            = 19,29 phut
gate-registry     = 13,92 + thiet lap        = 16,67 .. 17,19 phut
gate-packet-loop  =  7,42 + thiet lap        = 10,17 .. 10,69 phut
   thiet lap Windows do lai 11-09-2026: 2,75 .. 3,27 phut
```

⇒ `max(job)` ước **`19,29`–`19,29`** (job `gate` vẫn nặng nhất), so ngưỡng `A1` **`≤ 36,00`**.
**Ước này dùng tải của nền G2.** Dưới tải hôm nay (sau `#492`), job `gate` còn mang bước
`lease-publish selftest` đã phình; **`#504`** land trước mới đưa bước ấy xuống (nghiệm thu của `#504`:
bước 20 ≤ **15** phút) theo hệ số
`1/bội_số` — **không có con số cho bước ấy**, vì bội số Windows chưa ai đo và giá trị thật của bước
là một **cận dưới** (mô hình ba số hạng ở `T125-RA-JOB-RIENG` mục *ƯỚC CÓ ĐIỀU KIỆN* — đặc tả ấy đã
RÚT, nhưng phép đo trong nó vẫn dùng được) —
đó chính là lý do thứ tự hai packet không đảo được.

**Thứ ước này KHÔNG nói:** nó không nói `max(job)` sẽ dưới `36,00`. Chi phí thiết lập của job MỚI
trên Windows **chưa ai đo** (`chua_do_duoc` #1); nếu nó lớn hơn dải trên thì kết luận đổi. `A1` là
phép đo trả lời câu ấy, và `A1` ĐỎ là **KẾT QUẢ ĐO**, không phải thất bại của packet.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng THÊM** — cột `additions` của `git diff --numstat`,
**KHÔNG** phải `adds − deletes`. Thước sai đã trả giá: `+351/−351` có ròng `0` mà `additions = 351 > 300`.

Ước ĐÚNG THƯỚC, từ số đo khối trên `ci.yml`:

| khối phải NHÂN ĐÔI (mỗi job mới một bản) | dòng (kể chú thích) | dòng (bỏ chú thích) |
|---|---:|---:|
| đầu job: `strategy`/`matrix`/`runs-on`/`timeout-minutes`/`env` | 35 | 17 |
| 9 bước thiết lập tới hết bước Ruff | 44 | 33 |
| **một job mới** | **79** | **50** |
| **hai job mới** | **158** | **100** |

Cộng hai bước dời (≈4 dòng), sửa `loi_ruff_ci` (ước +15–25) và phản chứng mới (ước +15)
⇒ **ước `135`–`200` dòng thêm**. Dưới `300`, biên ≥ `100`.

**KHÔNG có lối thoát composite.** Bản trước đề nghị rút phần thiết lập thành
`.github/actions/…` khi chật trần. Lối ấy thêm **một đường dẫn thứ ba** vào write set, tức
**vi phạm chính `A8`** (đòi đúng **2** đường). Một đặc tả không được đồng thời cấm và mời một
phương án. **Vượt `300` ⇒ DỪNG và hỏi chủ kho**, không tự xin ngoại lệ, không tự mở write set.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.github/workflows/ci.yml` | định nghĩa job `gate` và toàn bộ bước của nó (G7: **40** bước hôm nay) |
| 2 | `.claude/dev/ci_dang_ky_test.py` | consumer `loi_ruff_ci` khoá cứng `jobs.gate`; tách job mà không sửa nó thì bước `test registry` tự đỏ |

Không ký tự đại diện. Không đường dẫn nào khác. **2 tệp**, còn **một chỗ trống** dưới trần
`ADR-0044` — chỗ trống ấy là **biên an toàn có chủ đích**, không phải chỗ nhét việc.
Trong tệp #2 chỉ đụng `loi_ruff_ci` và phản chứng của nó; **không** đụng `bang_chung_xanh`, `MOI`,
`MOI_WINDOWS`, `chay_moi` — của `LO-319` và hai packet mutant.

Hai packet **cố ý KHÔNG** nằm ở đây: bản vá bộ chấm đột biến đi bằng
`CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN`; `t125` đi bằng **`#504 WINDOWS-LEASE-SUITE`**.

**Người giữ — đo 09:3xZ 11-09-2026** (sau canh hai nguồn ref, `comm -23` RỖNG):

```
.github/workflows/ci.yml          rc=0   NGƯỜI_GIỮ 0: không có
.claude/dev/ci_dang_ky_test.py    rc=11  NGƯỜI_GIỮ 1: bo-cong-duyet-khac-danh-tinh-exec-2-claude-20260911  (#502)
```

⇒ lease cấp **SAU KHI `#502` land VÀ SAU KHI `#504` land**, không phải sau khi hạn danh
nghĩa trôi. Cấp chồng là tự tạo cửa sổ hai writer. Phiên cấp lease **đo lại**, không chép dòng này.

**Vì sao nối tiếp SAU `#504`.** Không phải vì chồng write set — `#504` **không** ghi `ci.yml` (nó khai
`ci.yml` là ngoài phạm vi) — mà vì **NỀN ĐO**: `A1`/`A5` của packet này cần một lượt Windows **hoàn
tất**, và `#504` là thứ làm nó hoàn tất. Chạy trước `#504` thì vế TRƯỚC của `A5` vẫn `KHÔNG ĐO ĐƯỢC`
(xem `chua_do_duoc` #0).

**Thứ tự chuỗi: `#502 → #504 → GATE → LO → 2A → 2B`.**
*(Sửa 12-09-2026 theo cross-review trên PR #508: dòng này còn dẫn `T125-RA-JOB-RIENG` sau khi
đặc tả ấy đã **RÚT** — người điều phối đọc nó sẽ chờ một packet không còn tồn tại, hoặc xếp
`GATE` khác với `depends_on: [wp502, wp504]` mà chính tệp này khai ở đầu. Đúng lớp "con số/tên
đã trôi mà câu văn còn giữ" mà `hinh_dang_ke_thua` của tệp này đang đếm.)* Tệp #2 cũng nằm trong write set của `LO-319`,
`MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`, `MUTANT-WINDOWS-NHANH-DON-DUOC`; `§5` exclusion theo ĐƯỜNG DẪN
⇒ bốn packet **nối tiếp**. GATE đi trước ba packet kia vì `A7` của chúng viết MỘT LẦN theo bố cục sau
tách (`gate-registry`), thay vì phải giữ hai trường hợp.

## `ngoai_pham_vi`

1. **`timeout-minutes` — CẤM đụng theo CẢ HAI chiều.** Không nâng (đã nâng 2 lần, 3 mức
   `25`→`45`→`60`; `§12` coi lần kế là điều kiện DỪNG), và không hạ để "ép kỷ luật": hạ trần biến một
   job chậm thành một job `cancelled`, tức đổi một vấn đề đọc được thành một vấn đề vô hình.
2. **Chạy CÓ ĐIỀU KIỆN theo diff / nhãn / `paths`.** Đã có đặc tả đóng băng (`CI-FASTPATH-THEO-DIFF.md`)
   và bản triển khai đã bị bỏ (PR #247 đóng). Kho đã trả giá hai lần cho logic điều kiện của workflow.
3. **Song song hoá TRONG `test registry`.** Chạm `chay_moi` — vùng ba packet sau sửa; hiệu quả trên
   Windows chưa đo. Đo trên Linux: tuần tự `400` s, bộ dài nhất `270` s ⇒ trần song song hoá `−32,5 %`.
   **Nợ có tên: `SONG-SONG-HOA-TRONG-TEST-REGISTRY`** — mở packet riêng **SAU KHI có phân rã theo bộ
   trên Windows**. Điều kiện mở ấy là phần của nợ, không phải lời khuyên: mở trước khi có phân rã là
   tối ưu hoá một thứ chưa ai đo.
4. **Cắt vòng lặp đột biến của `packet_loop_test.py`.** Cùng hình dạng bản vá với `#456`, nhưng tệp
   khác. **Nợ có tên: `MUTANT-WINDOWS-PACKET-LOOP`.**
5. **Bỏ bước trùng** — đã đo, **0** bước trùng. Không có gì để làm.
6. **Không đổi tập bước, không đổi lệnh của bước nào. KHÔNG NGOẠI LỆ.** Packet này chỉ đổi bước ấy
   nằm trong **job** nào.
7. **KHÔNG đụng `t125`** — của **`#504 WINDOWS-LEASE-SUITE`**.
8. **KHÔNG chữa phần việc `#492` thêm vào suite `lease-publish`.** Nợ riêng, `chua_do_duoc` #6.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Hai bước nặng nhất (`test registry`, `packet-loop selftest`) chuyển sang job riêng, **cùng ma trận nền** với `gate`. | `write_set` #1 |
| M2 | **Độ phủ không đổi**: tập `(tên bước, nền, conclusion)` sau khi tách bằng đúng tập trước khi tách. | `write_set` #1 |
| M3 | Điều kiện chạy KHÔNG đổi: mọi job mới mang **cùng** `if` mức job (hôm nay: không có), cùng biểu thức ma trận, cùng `timeout-minutes`; mọi bước dời giữ nguyên `if` của nó — kể cả `if:` viết KHÔNG có dấu nội suy. | `write_set` #1 |
| M4 | `timeout-minutes: 60` giữ nguyên trên **mọi** job. | `write_set` #1 |
| M5 | Phút tính tiền tăng thêm được **đo và công bố**, không phải ước. | `write_set` #1 |
| M6 | Bảo vệ nhánh vẫn có cổng: tách job mà không cập nhật ruleset là **tháo cổng bằng một thao tác trông như tối ưu hoá**. | `write_set` #1 |
| M7 | `loi_ruff_ci` tìm bước `test registry` trong **mọi** job và đòi Ruff được cài trong **cùng job**, **trước** bước ấy; không job nào có bước ⇒ lỗi. Tương thích với `ci.yml` chưa tách. | `write_set` #2 |

## `nghiem_thu`

**Ràng buộc chi phí CI (chỉ thị chủ kho 11-09-2026).** Packet này được chi **đúng `N = 2`** lượt
`workflow_dispatch`: **một** lượt nền tại `start_from_sha`, **một** lượt sau tách. Mỗi lần chi ghi
`run_id` vào biên nhận. **Vượt `N` ⇒ revision**, không tự chi thêm. Lượt `pull_request` tự bắn là
**cổng**, không tính vào `N`. **Cấm tuyệt đối lượt "chạy thử xem sao".**
Căn cứ: G8 — **965,10** phút tính tiền (**48,3 %** hạn mức tháng) bị **8** lượt `cancelled` tiêu mà
**không lượt nào cho một kết quả hoàn tất hợp lệ**. *(Nói vậy chứ không nói "thu 0 thông tin":
chính các bước bị cắt đang được dùng làm chẩn đoán trong đặc tả này.)*

**Điều kiện dừng (chỉ thị chủ kho 11-09-2026).** `review_class = sensitive` ⇒ packet chỉ đóng khi
cross-review **`approve`** tường minh. **"0 P1 + 0 P2" KHÔNG đủ**: *"vắng mặt vì sạch"* và *"vắng mặt
vì chưa nhìn tới"* nhìn giống hệt nhau, `approve` mới phân biệt được.
**Chống lách:** một vòng làm finding biến mất bằng cách **thu hẹp phạm vi** phải khai thẳng — thu hẹp
phạm vi là một mục `chua_do_duoc`, **không** phải một bản vá.

---

**A1 (M1) — job dài nhất giảm, đo bằng PHÚT TƯỜNG CỦA JOB.**
Đòi `max(thời lượng job)` trên `windows-latest` **≤ 0,60 × `timeout-minutes`** — hôm nay
`timeout-minutes: 60` ⇒ **≤ 36,00 phút**.

Vì sao neo **biên tương đối** chứ không neo số phút: một ngưỡng tính bằng phút hết hạn trước khi
packet kịp land (tải trôi). Bất biến cần giữ là ***"còn ít nhất 40 % biên dưới trần"***.
Ràng buộc kèm theo để biên tương đối không thành cửa hậu: `timeout-minutes` **giữ nguyên 60** (`A4`).
Nới trần để `0,60 ×` rộng ra là **vi phạm `A4`**, và `§12` coi nâng trần là điều kiện DỪNG.

Đơn vị: **`completed_at − started_at` của JOB**, đọc qua `list_workflow_jobs`; lấy `max` trên **tất
cả** job của lượt, **không** lấy tổng.
**Nền — và phải phân biệt HAI loại nền, vì bản trước gộp chúng:**
- **Nền LỊCH SỬ:** G2 (`34429604548`) — `max(job) = 40,63` phút, `success`. Nó chứng minh job Windows
  **từng** hoàn tất, và `40,63 > 36,00` (G4). **Nó KHÔNG phải nền nghiệm thu**: nó thuộc tải
  **trước `#492`**.
- **Nền NGHIỆM THU:** lượt sinh lại tại `start_from_sha` theo `A5(3)`, dưới tải **hiện tại**. Nền ấy
  **có thể KHÔNG hợp lệ** (xem `chua_do_duoc` #0) — khi đó **DỪNG và hỏi chủ kho**, không mượn
  `40,63`.
**Phép làm ĐỎ:** `max(job)` Windows của lượt sau tách vượt `0,60 ×` trần.
**Đột biến bắt buộc:** gộp hai job mới trở lại `gate` ⇒ `max(job)` phải **tăng trở lại mức chưa
tách của CHÍNH nền nghiệm thu** ⇒ `A1` ĐỎ. **KHÔNG** đòi nó tái tạo `40,63` — số ấy của cây cũ,
tải cũ, và đòi như thế là biến một đột biến thành phép so với một hằng số đã chết.

**Kèm, công bố nhưng KHÔNG đặt ngưỡng** (chưa có nền cùng đơn vị): thời gian đầu-cuối của cả lượt
(`run.created_at → run.updated_at` khi `status = completed`). Đây là phép đo duy nhất thấy được xếp
hàng của nhiều runner; nếu nó **không** giảm dù `max(job)` giảm, đó là kết quả đo, báo chủ kho.
**Không** quy thời gian chờ thành phút tính tiền — chờ không tính tiền.

**A2 (M2) — độ phủ không đổi, đo bằng TẬP HỢP, trên HAI loại cò.**
Lấy `(job, tên bước, nền, conclusion)` của lượt TRƯỚC và lượt SAU; **bỏ cột `job`**, so **tập**
`(tên bước, nền, conclusion)`. Hai tập phải **bằng nhau**. Làm HAI lần:

- lượt `workflow_dispatch` SAU tách trên nhánh packet (cả hai nền) so lượt `workflow_dispatch`
  **TRƯỚC tách trên CÙNG nhánh tại `start_from_sha`** — **cùng base, cùng event, cùng lane**;
  executor phóng lượt nền TRƯỚC khi đẩy commit tách. (Đây là hai lượt của ngân sách `N = 2`.)
- lượt `pull_request` của chính PR packet so lượt `pull_request` gần nhất mà `ci.yml` nền **BẰNG
  BYTE** `ci.yml` của `start_from_sha` — đây là lượt DUY NHẤT chứng minh các job **có mặt trên PR**,
  tức chứng minh không ai đã thêm điều kiện chỉ-dispatch (xem `A3`).

`conclusion` từng mục đọc lại bằng `list_workflow_jobs` khi so, **không** suy từ phép trừ.
Đơn vị: **tập bộ ba**, không phải `wc -l` — hai tập lệch vẫn có thể **cùng lực lượng**.
**Phép làm ĐỎ:** quên chép `if: runner.os != 'Windows'` sang job mới ⇒ một bước đổi `skipped`↔`success`
⇒ tập lệch ⇒ ĐỎ. **Mười** bước có `if:` là mười cơ hội hỏng chỗ này.

**Nhánh nền KHÔNG hợp lệ:** nếu lượt nền bị cắt ⇒ hạ xuống so tập `(tên bước, nền)` (bỏ `conclusion`),
**và** đòi lượt SAU có **0** bước `cancelled`, **và** mọi bước `skipped` giải thích được bằng `if` của
chính nó. Trạng thái khi ấy là **`ĐẠT CÓ ĐIỀU KIỆN`**, ghi thẳng vào biên nhận là *"độ phủ chứng minh
bằng TÊN BƯỚC, không bằng KẾT LUẬN"* — **không** được ghi `ĐẠT` trơn.
**Nhánh hạ vẫn còn răng** với ca *"quên chép bước"* (tập tên lệch), và **mất răng** với ca *"bước đổi
kết luận"* — nói thẳng cái mất. Nhánh này **không** miễn `A5`.

**A3 (M3) — không thêm mặt điều kiện nào, đo bằng CẤU TRÚC.**
**Không** đếm lực lượng tập chuỗi `${{ }}`: đếm delimiter là đếm **CÁCH VIẾT**, không đếm **ĐIỀU
KIỆN**. Phản chứng đã dựng: thêm `if: github.event_name == 'workflow_dispatch'` (**không** dấu nội
suy, cú pháp Actions cho phép) vào `gate-registry` ⇒ tập biểu thức vẫn `6 → 6` ⇒ phép cũ **PASS**, mà
job biến mất trên mọi PR. Thay bằng **ba phép so**:

1. **mức job**: với mỗi job, bộ ba `(if mức job, chuỗi matrix.os sau chuẩn hoá khoảng trắng,
   timeout-minutes)` phải **bằng** bộ ba của `gate`. Hôm nay `gate = (None, fromJSON(…), 60)` (G7).
2. **mức bước, hai nửa** (mỗi nửa mù đúng chỗ nửa kia thấy ⇒ mỗi nửa một đột biến riêng):
   - tập `(tên bước, if của bước)` trên **mọi** job sau tách phải **bằng** tập trước tách.
     **Nói thẳng cái nửa này KHÔNG bắt được:** xoá hẳn một **BẢN SAO** của bước thiết lập khỏi một
     job mới ⇒ tập **KHÔNG** đổi (tập dedup; `gate` vẫn có bước ấy).
   - **tiền tố 9 bước** (theo tên, theo thứ tự) của mỗi job mới phải **bằng** tiền tố 9 bước của
     `gate` — nửa này bắt đúng ca nửa trên bỏ sót.
3. **mức workflow**: `on:` và `concurrency:` không đổi một ký tự (so chuỗi sau
   `yaml.safe_load` + `safe_dump`).

**Chốt cứng `actionlint`, đo bằng TẬP CHẨN ĐOÁN, không bằng `rc`.** Chạy `actionlint` trên `ci.yml`
của `origin/master` và của nhánh packet trong **CÙNG một lệnh, CÙNG môi trường**; ghi phiên bản
`actionlint`/`shellcheck`, `rc`, và **toàn bộ** chẩn đoán hai vế (`-format '{{json .}}'`). Chuẩn hoá
mỗi chẩn đoán thành `(tệp, mã/loại, thông điệp, thân run của bước chứa nó sau chuẩn hoá khoảng
trắng)` — **bỏ số dòng/cột** vì dời bước làm dòng trôi — rồi so **đa tập**: delta phải **RỖNG**.
Vì sao không so `rc`: `rc=1 → rc=1` che được lỗi MỚI (phản mô hình đã đo: vế trước `{SC1003}`, vế sau
`{SC1003, SC2086}`, `rc` cùng `1` ⇒ phép cũ PASS, phép tập ĐỎ).
**Vắng `actionlint`, thiếu `shellcheck`, hay thiếu log một vế ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ**, không phải
delta 0. (Nền đã đo: có `shellcheck` ⇒ `rc=1` một finding `SC1003` tại `ops-don-ref.yml:106`; vắng
⇒ `rc=0` — hai nền khác nhau, nên phiên bản công cụ phải nằm cạnh kết quả.)
**Phản chứng BẮT BUỘC, và nó phải được CHẠY chứ không chỉ được kể:** chèn **một lỗi shellcheck MỚI**
vào một workflow **đã có sẵn một lỗi** ⇒ `rc` vẫn `1` **ở cả hai vế** ⇒ delta đa tập **khác rỗng**
⇒ **ĐỎ**. Đoạn kể phép tính tập ở trên **không thay** được lần chạy ca này: một phép kiểm chưa từng
đỏ thì chưa phải bằng chứng.

**Và: KHÔNG viết cú pháp `${{ }}` trong comment của `run:`** — kho đã bị GitHub từ chối cả tệp vì
đúng chuyện đó (`ops-don-ref.yml`, run `31971137920`, 0 job, `conclusion: failure`).
**Đột biến bắt buộc:** chính ca `if` không delimiter ở trên.

**A4 (M4) — trần không đổi, đo bằng GIÁ TRỊ ĐÃ PARSE của TỪNG job.**
`yaml.safe_load(ci.yml)`; với **mỗi** `job_id` trong danh sách job kỳ vọng của **pha sau packet này**
— **BA**: `gate` · `gate-registry` · `gate-packet-loop` — đòi
`jobs[job_id]["timeout-minutes"] == 60`.
**Thiếu khoá ⇒ ĐỎ.** Giá trị khác `60` ⇒ ĐỎ, kể cả nhỏ hơn. Ngoài ra: **không** `timeout-minutes` nào
ở mức bước.
**Vì sao không đếm chuỗi:** `grep -c 'timeout-minutes: 60'` bằng số job **không** chứng minh từng job
được ghim — một chú thích mang chuỗi ấy cũng được đếm, và một job **thiếu hẳn** khoá **không tạo ra
"giá trị khác 60"** nên lọt sạch. Tổng đúng không chứng minh từng số hạng đúng.
`A4` là **chốt chống cửa hậu của `A1`**: `A1` neo vào `0,60 × timeout-minutes`, nên một job thiếu ghim
là một đường nới biên không ai thấy.
**Phép làm ĐỎ:** bỏ khoá `timeout-minutes` khỏi **một** job ⇒ `A4` phải ĐỎ.

**A5 (M5) — phút tính tiền được ĐO và công bố, neo đúng lượt.**
`Σ(thời lượng job × hệ số nền)` với `windows = 2`, `ubuntu = 1`, cho lượt TRƯỚC và lượt SAU.

**Cạm bẫy phải khai, vì nó trông y hệt thành công:** tính ngây thơ trên lượt `34563553711`:
`60,52 × 2 + 12,38 × 1 = 133,42` — một con số **nhỏ**, trong khi job Windows bị **cắt** và job Ubuntu
**ĐỎ**. Một đại lượng bị **chặn trên** trông hệt một đại lượng **nhỏ**. ⇒ **TÍNH HỢP LỆ trước,
GIÁ TRỊ sau.**

**(1) Điều kiện hợp lệ — với MỖI lượt, theo thứ tự, dừng ở cái đầu tiên hỏng:**

  **(a) tập `(job_id, nền)` đọc được phải BẰNG tập kỳ vọng CỦA CHÍNH LƯỢT ẤY.**

  Ba khái niệm **KHÁC nhau**, không được gộp: `job_id` **cấu trúc** (khoá trong `jobs:`) ·
  **instance** `(job_id, nền)` sau khi giải ma trận · `id` **API** của job trong một lượt.
  Phép so chạy trên **instance**; dùng `id` API thì hai lượt không so được, dùng `job_id` trần thì
  mất chiều nền.

  **Nguồn của tập kỳ vọng, và nó phải TỰ SINH RA ngữ cảnh chứ không nhận một danh sách đoán trước:**

  1. `yaml.safe_load` **chính `ci.yml` tại SHA của định nghĩa workflow ĐÃ THỰC THI lượt ấy** — neo
     vào **SHA bất biến**, **không** neo tên nhánh.
     **`run.head_sha` KHÔNG luôn là SHA ấy.** Với `pull_request_target` (và mọi cò đọc định nghĩa từ
     nhánh base), định nghĩa chạy là của **base**, không của head — kho vừa trả giá đúng chỗ này:
     `ops-thu-hoi-admission.yml` thoát `12` vì `github.workflow_sha` lệch `pull_request.base.sha`.
     ⇒ Lấy SHA định nghĩa từ **chính lượt** (`workflow_sha`/`workflow_ref`), và **kiểm** nó khớp cây
     dùng để giải; không khớp ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ.
  2. **Trích toán hạng theo VỊ TRÍ TRONG YAML, KHÔNG theo dấu nội suy.**
     **Quét `${{ … }}` là SAI, và đo được là sai:** trong job `gate` trên `origin/master` có **10**
     `if` mức bước, trong đó **7 ở dạng TRẦN** (không `${{ }}`) và chỉ **3** có dấu (đo 12:3xZ
     11-09-2026). Phép trích theo delimiter bỏ sót **7/10** — và `A3` ngay dưới đã công nhận dạng
     trần tồn tại, nên hai mục sẽ mâu thuẫn nhau.
     ⇒ **KHÔNG liệt kê vị trí — QUÉT TOÀN TÀI LIỆU rồi FAIL-CLOSE theo SCHEMA.**
     Một danh sách vị trí đoán trước **thua từ trong thiết kế**, và đo được là đã thua: bản trước
     liệt kê `strategy.matrix.*` · `if` mức job · `if` mức bước, trong khi `ci.yml` hôm nay có biểu
     thức ở **7** khoá khác nhau (đo `yaml.safe_load` + duyệt đệ quy, 12:5xZ 11-09-2026):

     ```
     3x steps.if            1x concurrency.group              1x jobs.gate.runs-on
     1x jobs.gate.strategy.matrix.os                          1x steps.env.PR_HEAD_SHA
     1x concurrency.cancel-in-progress                        1x steps.with.name
     ```

     Danh sách cũ phủ **2/7**, và cái bỏ sót gồm **`runs-on: ${{ matrix.os }}`** — đúng khoá
     **quyết định instance**, tức đúng thứ `A5` tựa vào. Cùng gốc *"danh sách CẤM không bao giờ đủ,
     phải đảo thành danh sách CHO PHÉP"*.

     **Phép đúng, hai nửa, và nửa sau mới là chốt:**
     1. **Tập vị trí biểu thức** = mọi scalar trong tài liệu đã parse **chứa `${{`**, **hợp** với
        mọi khoá `if` (mức job và mức bước) **bất kể dạng trần hay có dấu**. Duyệt đệ quy toàn bộ
        cây, không liệt kê khoá.
     2. **SCHEMA VỊ TRÍ ĐƯỢC HỖ TRỢ** khai tường minh trong bản vá. Vị trí nào ở (1) mà **không**
        nằm trong schema ⇒ **ĐỎ**, kèm tên khoá. Đây là chốt trả lời được câu *"đã quét hết chưa"*
        bằng **cấu trúc**, thay vì bằng lời tự khai của bộ giải.
     **Ca khoá:** làm nguồn chọn runner phụ thuộc một toán hạng không giải được, đặt ở một vị trí
     **ngoài** schema (ví dụ `runs-on` nếu schema quên nó) ⇒ phải **ĐỎ**. Ca này phải đỏ **độc lập
     với tập mà bộ giải tự trả về** — nếu nó chỉ đỏ khi bộ giải tự khai thiếu thì chốt vô nghĩa.
     **Về `run:` — bản trước nói sai và tự mâu thuẫn:** comment **của YAML** bị parser bỏ nên không
     bao giờ tới được phép quét này; nhưng dấu `#` **bên trong scalar `run:`** là **một phần của
     scalar** và Actions **có** nội suy nó — chính đặc tả này kể sự cố `ops-don-ref.yml` vì đúng
     chuyện đó. Nên `run:` là **vị trí biểu thức thật**, phải nằm trong schema (hoặc bị từ chối),
     **không** được loại trừ bằng một câu cấm quét.
  3. **Giải từng toán hạng — và "toán hạng" gồm cả HÀM, không chỉ đường dẫn ngữ cảnh.**
     `ci.yml` hôm nay dùng `always()` · `cancelled()` · `contains()` · `fromJSON()` (đo cùng lúc);
     `always()`/`cancelled()` phụ thuộc **trạng thái lượt**, không phải metadata tĩnh.
     Với **mỗi** toán hạng, lấy giá trị từ metadata của **chính lượt ấy**.
     **Toán hạng nào KHÔNG giải được — kể cả vì bộ giải chưa hỗ trợ dạng ấy — ⇒ `KHÔNG ĐO ĐƯỢC`
     ⇒ ĐỎ.**
     **Chốt bắt buộc, vì fail-close chỉ cứu được thứ đã TÌM THẤY:** bộ giải phải khai **tập vị trí
     nó đã quét**; một dạng biểu thức nằm ngoài tập ấy ⇒ **ĐỎ**, không phải im lặng bỏ qua.
     **Ca khoá:** cùng một toán hạng không giải được, đặt lần lượt trong `if` **có** dấu và `if`
     **trần** ⇒ **cả hai** phải `KHÔNG ĐO ĐƯỢC`. Chỉ ca có dấu đỏ ⇒ bộ giải vẫn mù 7/10 ⇒ ĐỎ.
  4. Giải biểu thức dưới ngữ cảnh đó ⇒ tập **instance** ⇒ đó là kỳ vọng.

  **Vì sao KHÔNG được liệt kê một danh sách ngữ cảnh cố định:** bản trước ghi *"`event_name` và
  `inputs`"* — **thiếu** hai toán hạng thật sự được đọc (`ref`, nhãn PR) và **thừa** một toán hạng
  không được đọc (`inputs`). Hai PR cùng `event_name` nhưng khác nhãn `windows` có tập instance
  **khác nhau**; hai `push` khác `ref` cũng vậy. Một danh sách đoán trước **thua từ trong thiết kế** —
  cùng gốc *"danh sách CẤM không bao giờ đủ, phải đảo thành danh sách CHO PHÉP"*, và ở đây lối đảo là
  **đọc toán hạng từ chính biểu thức** thay vì duy trì một danh sách.

  **TUYỆT ĐỐI KHÔNG** lấy kỳ vọng từ danh sách job API đã đọc — làm thế thì điều kiện "bằng nhau"
  **tự chứng minh** và lỗi thiếu job lọt sạch.

  **Phép làm ĐỎ cho chính (a):** bơm một `ci.yml` có 4 job nhưng dữ liệu chỉ trả 3 instance ⇒ phải ĐỎ ·
  bơm một kỳ vọng **suy từ chính dữ liệu** ⇒ ca tự kiểm phải ĐỎ · thêm vào biểu thức một toán hạng
  không giải được từ metadata lượt ⇒ phải `KHÔNG ĐO ĐƯỢC`, **không** được im lặng bỏ qua.

  **(b)** danh sách **không được RỖNG** — *"mọi job đều `success`"* **ĐÚNG RỖNG** với danh sách rỗng,
  và tổng khi ấy là `0`, tức một lượt **không đọc được gì** sẽ cho `Σ = 0` và **lọt qua mọi ngưỡng**;
  **(c)** **phân trang phải cạn** — đọc tới hết, không dừng ở trang đầu;
  **(d)** **cùng `run_attempt`** cho mọi job; trộn attempt ⇒ `KHÔNG ĐO ĐƯỢC`;
  **(e)** **đủ `started_at` và `completed_at`** cho mọi job; thiếu mốc ⇒ `KHÔNG ĐO ĐƯỢC`, không cộng;
  **(f)** rồi mới: **mọi job `conclusion == "success"`**. Một job `cancelled`/`failure`/`timed_out` ⇒
  **`KHÔNG ĐO ĐƯỢC`** ⇒ **ĐỎ**, KHÔNG phải một con số.

  **Vì sao (f) một mình không đủ:** (f) sửa ca *job hỏng CÓ TRONG mẫu*, không sửa ca *job VẮNG khỏi
  mẫu* — mà ca thứ hai mới là ca cho ra **tổng thấp giả**.
  **Phép làm ĐỎ cho (a)–(e):** bỏ một job Windows khỏi mẫu ⇒ `A5` phải `KHÔNG ĐO ĐƯỢC`.

**(2)** Lượt **SAU tách** phải hợp lệ theo (1), rồi công bố `Σ(phút job × hệ số nền)`.
**(3)** Lượt **TRƯỚC** — nền để so — **phải được sinh lại tại lúc thi công** trên `start_from_sha`,
và cũng phải hợp lệ theo (1).

**Một manifest phép đo dùng CHUNG cho `A2` và `A5`** — cùng `run_id`, cùng `run_attempt`, cùng tập
job — để hai tiêu chí không đọc hai mẫu khác nhau rồi cùng báo xanh.

Đơn vị: **phút tính tiền** = Σ phút tường của job × hệ số nền.
**Phép làm ĐỎ:** bất kỳ điều kiện nào của (1) hỏng ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ.
Khi cả hai lượt hợp lệ thì **công bố** `Σ` của cả hai và **tỉ lệ tăng**; **KHÔNG có ngưỡng số** — số
tăng thêm là thứ chủ kho đọc và quyết, không phải thứ một reviewer đối chiếu với một hằng số.
**Tiêu chí này KHÔNG được bỏ dù `A1` xanh.** Packet mua wall clock bằng billing; một lượt đo chỉ nói
nửa đầu là một lời khai thiếu nửa sau, và nửa sau đã giết CI của kho một lần.

**A6 (M6) — cổng không bị tháo khi tách, và nó ĐO ĐƯỢC.**

- **(a) tên khai ra khớp `ci.yml`.** Bản vá in danh sách **context** của job mới.
  **Phép làm ĐỎ:** tên trong `ci.yml` khác tên in ra ⇒ ĐỎ.
- **(b0) MỐC THỜI GIAN — ruleset phải được cập nhật TRƯỚC KHI MERGE.**
  Đọc trạng thái **sau đó** không bảo vệ **lần merge đầu tiên**: chuỗi *merge trước, thêm context
  sau* vẫn thoả phép so tập ở thời điểm cuối, trong khi chính lần merge ấy **không** bị hai job mới
  chặn. Đây là **nghĩa vụ thời gian**, không thay được bằng một phép so tập cuối cùng.
  Đòi lưu vào biên nhận **readback tập context** và **kết quả check trên đúng head được merge**, đo
  **trước** thao tác merge; mục này nằm trong thân Issue như việc chủ kho làm **TRƯỚC** khi merge.
  **Phép làm ĐỎ:** biên nhận chỉ có readback **sau** land ⇒ ĐỎ.
  **Thứ tự an toàn:** job mới phải **đã sinh check đúng tên trên PR** rồi mới chuyển require sang nó.

- **(b) TRẠNG THÁI THẬT của ruleset — đọc được, nên là tiêu chí, không phải lời nhắc.**
  `GET /repos/{owner}/{repo}/rules/branches/master` ⇒ mục `type == "required_status_checks"` ⇒
  `parameters.required_status_checks[].context`. Đòi tập ấy **chứa cả BA**:
  `gate (ubuntu-latest)` · `gate-registry (ubuntu-latest)` · `gate-packet-loop (ubuntu-latest)`.
  **Không đọc được (rc ≠ 200, thiếu trường, thiếu quyền) ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ.**
  **Phép làm ĐỎ:** chạy tiêu chí khi ruleset **chưa** cập nhật ⇒ thiếu context ⇒ ĐỎ. Đây là phép phân
  biệt mà bản trước **không có**: Issue trông y hệt nhau ở hai trạng thái đã-require và chưa-require.

**HAI LUẬT VỀ TÊN, cả hai đo được (G5), sai luật nào cũng hỏng:**

1. **Require theo CONTEXT, không theo `job_id`.** Ruleset lưu **tên check**; với job có ma trận tên
   ấy là `"<tên job> (<nền>)"`, và **`<tên job>` là `job_id` CHỈ KHI job không khai khoá `name:`**.
   Đo trên `origin/master` 12:3xZ 11-09-2026: job `gate` **không** có `name` ⇒ hôm nay đúng là
   `job_id + nền`. Phiên thi công **đo lại** cho từng job mới, không suy từ dòng này.
   Đo được: hôm nay require đúng **`gate (ubuntu-latest)`**. Require chuỗi `gate` trần thì **không
   khớp check nào** — hậu quả **không** phải "cổng trang trí" mà là **PR bị CHẶN vĩnh viễn**: một
   required check không bao giờ báo cáo giữ PR ở trạng thái chờ. Cùng cơ chế với luật 2 ngay dưới.
2. **KHÔNG require một context mà PR thường KHÔNG BAO GIỜ sinh ra.** `matrix.os` (G6) chỉ cho
   `windows-latest` khi `event_name == workflow_dispatch`, hoặc `ref == refs/heads/master`, hoặc PR
   mang nhãn `windows`. PR thường ⇒ **chỉ** `ubuntu-latest`. Require `… (windows-latest)` sẽ **chặn
   vĩnh viễn mọi PR thường**. Đây là lý do cấu trúc khiến hôm nay chỉ có **một** context được require,
   và packet này **giữ nguyên luật ấy**.

**BẢNG CONTEXT THEO PHA — nguồn DUY NHẤT.**
*(Bản chiếu trong `T125-RA-JOB-RIENG` theo đặc tả đã RÚT; chỉ bảng này còn hiệu lực.)*

| pha | job trong `ci.yml` | context require |
|---|---:|---|
| hôm nay (`master`) | **1** — `gate` | `gate (ubuntu-latest)` |
| sau khi `#504` land | **1** — `#504` **không** thêm job nào (nó sửa trong bộ test) | `gate (ubuntu-latest)` |
| **sau khi packet này land** | **3** | thêm `gate-registry (ubuntu-latest)` · `gate-packet-loop (ubuntu-latest)` |

Chủ kho cập nhật ruleset **MỘT lần** — sau khi packet này land. `#504` **không** thêm job nào (nó sửa
trong bộ test), nên pha của nó **không** đổi tập context.
**Bản trước khai HAI lần và BỐN job** vì nó giả định `T125-RA-JOB-RIENG` (đã RÚT) sẽ thêm job
`gate-t125`. Số `4` và nghĩa vụ *"hai lần"* đều **hết hiệu lực** cùng đặc tả ấy.

**A7 (M7) — consumer `loi_ruff_ci` đọc được bố cục mới và vẫn có răng.**
**4** ca — fixture DỰ KIẾN, chưa thi công — đi qua chính `loi_ruff_ci(source)`:

| # | fixture | đầu vào | phải trả | đo trên hàm CŨ |
|---|---|---|---|---|
| 1 | `ruff-ci-chua-tach-tuong-thich-lui` | `ci.yml` hôm nay (chưa tách) | `[]` | `[]` |
| 2 | `ruff-ci-da-tach-dung` | tách đúng: Ruff trong `gate-registry`, trước `test registry` | `[]` | **1** lỗi ← ca đổi màu của packet |
| 3 | `ruff-ci-da-tach-thieu-ruff` | tách, **bỏ** bước Ruff khỏi `gate-registry` | ≥ 1 lỗi | — |
| 4 | `ruff-ci-da-tach-ruff-sau-registry` | tách, Ruff nằm **sau** `test registry` cùng job | ≥ 1 lỗi | — |

Hai phản chứng sẵn có `ruff-pin-required` và `ruff-version-probe-required` giữ nguyên màu.
Đơn vị: **số thông điệp lỗi trả về**.
**Phép làm ĐỎ:** đột biến `loi_ruff_ci` quay về đọc `jobs.gate` ⇒ ca **2** ĐỎ.

**A8 (toàn packet) — không đụng gì khác.** `git diff --numstat` chỉ hiện đúng **2** đường dẫn, cột
`additions` ≤ **300**. Đường thứ ba ⇒ **DỪNG và hỏi chủ kho**, không tự xin ngoại lệ, không tự mở
write set (`§3.2`: *"agent không tự mở write set"*).

**A9 — KHÔNG lease nào còn giữ write set TRƯỚC khi bắt tay.**
`ai-dang-giu` trên **cả hai** đường dẫn, chạy **sau** phép canh hai nguồn ref
(`git ls-remote --heads origin` so `git for-each-ref refs/remotes/origin`, so bằng **TẬP TÊN**, không
bằng `wc -l`; `comm -23` khác rỗng ⇒ **MÙ** ⇒ fail-close).
Đòi: `NGƯỜI_GIỮ 0` cho cả hai, **hoặc** người giữ duy nhất là lease của **chính packet này**.
**Công cụ quét `refs/heads/*`** ⇒ thiếu nhánh cục bộ cho ra `CHAN [12]`, **không phải** `NGƯỜI_GIỮ 0`;
đọc nhầm chỗ này là tự cấp cho mình một câu trả lời sai.
**`check rc=0` KHÔNG thay được phép đo này** — `check` không chặn chồng lấn write set.
Điều kiện bổ sung: **`#502` đã land** và **`#504` đã land** (`depends_on`).

## `hinh_dang_ke_thua`

| hình dạng | số lần | nguồn / đo lúc | vì sao có tiêu chí tương ứng |
|---|---:|---|---|
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức) | `git log -G 'timeout-minutes:' -- .github/workflows/ci.yml`: `9e4f361` · `6d88a2c` · `7657bfd` | lần kế là lần thứ ba ⇒ `§12` điều kiện DỪNG ⇒ `ngoai_pham_vi` #1, và `A4` |
| thêm một mặt ĐIỀU KIỆN vào workflow rồi nó vắng mặt lặng lẽ | **2** | `ci.yml:490-506` · `CLAUDE.md` (mục `paths:`, mục nhãn `windows`) | `paths:` không bắn ở lần đẩy tạo nhánh mới · `pull_request:` thiếu `types:` nên nhãn `windows` không sinh lượt ⇒ `ngoai_pham_vi` #2, `A3` đo bằng cấu trúc |
| cổng vắng mặt trông giống cổng xanh | **≥ 3** | `CLAUDE.md` (dấu bỏ-qua-CI/PR #100 · job `cancelled` · `ops-don-ref.yml` 0 job) | `A2` so TẬP; `A6` tách hai phần và phần (b) **đo** trạng thái thật |
| đại lượng bị **CHẶN TRÊN** trông giống đại lượng **nhỏ** | **1** | `60,52 × 2 + 12,38 = 133,42` trong khi Windows `cancelled`, Ubuntu `failure` | `A5` đòi **TÍNH HỢP LỆ trước, GIÁ TRỊ sau** |
| đếm biểu thức thay vì đếm điều kiện | **1** | bản đầu `A3` của chính đặc tả này | cùng gốc *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"* |
| so `rc` thay vì so tập kết quả | **1** | bản lượt 1 `A3` của chính đặc tả này | một số tổng che được hai tập khác nhau ⇒ `A3` so **đa tập chẩn đoán** |
| **danh sách ngữ cảnh đoán trước vừa THIẾU vừa THỪA** | **1** | đo 10:5xZ 11-09-2026 (G6) | bản trước ghi `event_name` + `inputs`: thiếu `ref` và nhãn PR, thừa `inputs` (**không** được đọc). ⇒ `A5(1)(a)` **trích toán hạng từ chính biểu thức** thay vì duy trì danh sách |
| **lời khai rộng hơn phép đo** | **4** | bản đầu (*"không có chi phí ẩn"*, *"không phải ước lượng"*) · lượt 1 (*"43/43 bước chạy được"*) · **mới, đo 10:5xZ 11-09-2026**: *"job Windows chưa hoàn tất lần nào"* và *"bốn lượt chạm trần"* — G1 đo được **18 `success` / 8 `cancelled`** | mục *"Phát biểu đúng phạm vi"* ở phần bằng chứng; mọi số `cancelled` nay kèm mẫu số |
| **một đặc tả vừa CẤM vừa MỜI cùng một phương án** | **1** | đo 11:3xZ 11-09-2026 | lối thoát composite (`2+1=3`) trái `A8` (đòi đúng **2**). Đã **BỎ HẲN**, không giữ làm gợi ý |

### Ba mục `chua_do_duoc` của `#456` — trạng thái TỪNG MỤC, không gộp

Kế thừa nguyên trạng; packet này **không** đóng thêm mục nào, và **không** được khai gộp là đã đóng.

| mục của `#456` | trạng thái |
|---|---|
| #1 *"tổng thời gian thật của job Windows"* | **ĐÓNG.** `43,20` phút, run `34045664423`, job `success` (đọc 17:41Z 06-09-2026). |
| #3 *"tỉ lệ 3× là đo TỔNG BƯỚC, không đo riêng đột biến"* | **ĐÓNG MỘT PHẦN.** Ước `44,3p → ~14p` cho `test registry`; thật `17,70`. **Vẫn chưa có phân rã theo bộ trên Windows** — đó là điều kiện mở `SONG-SONG-HOA-TRONG-TEST-REGISTRY` (`ngoai_pham_vi` #3). |
| #4 *"không có đường đo Windows tại chỗ"* | **KHÔNG ĐÓNG.** Xem `chua_do_duoc` #2. |

## `chua_do_duoc`

0. **NỀN LỊCH SỬ ≠ NỀN NGHIỆM THU, và nợ về nền hiện tại CHƯA bị bác.**
   G1/G2 bác đúng **một** mệnh đề — *"job Windows chưa hoàn tất lần nào"* — bằng 18 lượt `success`,
   gần nhất `34429604548`. Đó là **nền lịch sử**, và nó **không** chứng minh có một nền **hợp lệ dưới
   tải hiện tại**: cả **6** lượt Windows đã kết thúc **sau `#492`** trong hiện vật đều `cancelled`.
   `A5(3)` đòi **sinh lại** nền tại `start_from_sha` *sau khi* `T125` land, trong khi `T125 A1(b)` cho
   `ĐẠT CÓ ĐIỀU KIỆN` khi Windows **vẫn** `cancelled`. Hai điều ấy có thể cùng xảy ra ⇒ vế TRƯỚC của
   `A5` có thể **vẫn** `KHÔNG ĐO ĐƯỢC` khi packet này tới lượt.
   **Khi đó: DỪNG và hỏi chủ kho** — không chép nền lịch sử `40,63` làm nền nghiệm thu (khác tải),
   và không tự nới `A5`. `A5` hiện **fail-close** (không còn ngoại lệ như bản cũ); fail-close là chặt
   hơn, **không** phải bằng chứng rằng vòng phụ thuộc đã hết.
   **Và đột biến của `A1`** (gộp hai job mới trở lại `gate`) **không tự trở về `40,63`** — số ấy của
   cây cũ, tải cũ; đột biến chỉ phải làm `A1` ĐỎ, không phải khớp một con số lịch sử.

0b. **Tải còn tăng, và không ai canh tốc độ ấy — nợ RỘNG HƠN phần `#492`.**
   Ngoài `+1327` dòng của `#492` (mục #6), chi phí còn tăng **theo số biên nhận**: `t26`+`t27` tốn
   `20,7 ms/biên nhận` (đo 06:0xZ 11-09-2026 trên 118 biên nhận), nhân `≈10` cho nền Windows và nhân
   bội số `t125` ⇒ cỡ `0,6`–`0,7` s/biên nhận trên đường tới hạn. **Mỗi packet ghi sổ thêm biên
   nhận**, nên đại lượng này tăng đơn điệu theo số packet đã land.
   **Chưa có cổng nào canh ngân sách này** — nợ, chưa có tên, ngoài phạm vi packet này.
   Rút nợ xuống chỉ còn phần `#492` là **thu hẹp không có phép đo bác phần còn lại**.

0c. **XUẤT XỨ CỦA SỐ — phân loại lại, vì gói review không chứa hiện vật cho một số ô.**
   Có hiện vật, tái lập được: G1/G2/G3/G4 (`do-nen-hai-nen.txt`, `do-nen-windows.txt`) · bội số
   suite (`benchmark.txt` + `benchmark.sh`) · `prefix 33,97` / `overhead 0,03` (nêu run/job/attempt
   trong `T125-RA-JOB-RIENG`, đặc tả đã RÚT nhưng phép đo còn dùng được).
   **CHỈ THUẬT LẠI, KHÔNG có hiện vật trong kho** — và vì thế **không** được dùng làm nền đã sẵn
   có: `2,75`–`3,27` phút thiết lập Windows · `400`/`270` giây song song hoá Linux ·
   `20,7 ms/biên nhận` trên 118 biên nhận · response của `/rules/branches/master` (`200`,
   ruleset `20856202`) và `403` của `/branches/master/protection`.
   Phiên thi công **đo lại** từng số ấy kèm hiện vật, hoặc khai `KHÔNG ĐO ĐƯỢC` — **không** đưa số
   trần. Một lệnh REST tổng quát **không** tái lập một phép đo quá khứ.

1. **Chi phí thiết lập trên Windows của job MỚI chưa ai đo.** `2,75`–`3,27` phút là đo của **một**
   job đang có, và **không có hiện vật** (mục `0c`). Job mới có thể tốn khác (cache runner, thứ tự cấp máy, ba lần checkout
   `fetch-depth: 0`). Mọi con số ở mục *"ƯỚC CÓ ĐIỀU KIỆN"* là **ước có đơn vị từ số đo cũ**. `A1` và
   `A5` là hai phép đo trả lời câu ấy — và nếu chúng ĐỎ thì đó là **kết quả**, không phải thất bại.
2. **Không có đường đo Windows tại chỗ.** Container Linux; mọi khẳng định về Windows đi qua CI.
   Kế thừa nguyên vẹn từ `#456` `chua_do_duoc` #4.
3. **Nhiễu runner chưa tách khỏi tải.** Chưa có phép so **cùng head, cùng tập bước, cùng event** để
   tách hai thứ. Biên độ quan sát giữa các lượt là **khoảng biến thiên của một mẫu gộp khác tải và
   khác nhánh**, **không** phải phương sai, và **không** là giấy phép nới ngưỡng.
   **Nợ có tên: `NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`.**
4. **Không đo được hệ số nhân thật của Windows.** `×2` lấy từ chú thích `ci.yml:19-23`
   (r245, 13-08-2026), không từ hoá đơn. Nếu hệ số đã đổi thì con số phút tính tiền ở `A5` sai theo hệ
   số ấy — nhưng **chiều** của kết luận (tách job làm **tăng** billing) không đổi.
5. **Xếp hàng và độ trễ đầu-cuối của workflow chưa có nền.** `A1` công bố số này lần đầu; không có
   ngưỡng vì không có lượt nào trước để so cùng đơn vị.
6. **Phần việc `#492` thêm vào suite `lease-publish` KHÔNG ai canh.** `+1327` dòng test trong **một**
   commit làm bước ấy phình `≈ 8,7×` trên Windows. Không cổng nào canh tốc độ tăng của suite —
   **nợ, chưa có tên, ngoài phạm vi** (`ngoai_pham_vi` #8).
7. **Trạng thái ruleset đọc bằng `GITHUB_PAT` của phiên.** `GET /branches/master/protection` trả
   **403** `Resource not accessible by integration` (có `X-GitHub-Request-Id` ⇒ tới GitHub, là vấn đề
   **quyền token**, không phải proxy). Đường dùng được là `/rules/branches/master` (rc `200`).
   **Cảnh báo đã trả giá:** trường `protection` trong `GET /branches/master` trả
   `enforcement_level: "off"`, `contexts: []` — một **bản nhìn suy giảm**, ngược hẳn sự thật đo được ở
   G5. **Chỉ đọc `/rules/branches/master`**; không đọc được thì `KHÔNG ĐO ĐƯỢC`, **không** lùi về
   trường kia.
