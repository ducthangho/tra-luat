# Đặc tả packet — GATE-TACH-JOB-CAT-CHI-PHI

- `packet_id`: **GATE-TACH-JOB-CAT-CHI-PHI**
- `packet_issue`: **(để trống — chủ kho cấp)**
- `revision`: 1
- `generation`: 1
- `executor`: claude · `environment`: cloud
- `review_class`: **sensitive** (`.github/workflows/` — `PROTOCOL §8` loại trừ tường minh khỏi
  patch-as-hint; đây là ĐỊNH NGHĨA của cổng, không phải mã dưới cổng)
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`)

## `nguon_cap_viec`

Packet **khắc phục**, cho nợ mà chính `ci.yml` tự khai. `.github/workflows/ci.yml:63`, nguyên văn:

> **NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN**: gate 22 phút và đang lớn dần là **nợ riêng**.

Và `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md` mục `ngoai_pham_vi` #3 để dành đúng nợ ấy
(*"Không gộp"*), cùng mục #1 khai lý do hoãn: khi #456 được soạn, tổng thời gian Windows thật
**chưa ai đo** vì job luôn bị cắt ở trần. Packet #456 đã land và **lần đầu tiên** sinh ra số đo
ấy. Packet này là chỗ số đo ấy được dùng.

## Bối cảnh đo được (mọi số kèm thời điểm)

### Chân Windows nay chạy trọn — số đo mới, do #456 sinh ra

Run `34045664423`, head `426bfc0` (nhánh packet #456), đọc 17:41Z 06-09-2026 qua `actions_list`
+ `method: list_workflow_jobs` trên `/mcp/x/actions`:

| | trước #456 | sau #456 |
|---|---:|---:|
| bước `test registry`, Windows | 44,3 phút | **17,70 phút** |
| job `gate (windows-latest)` | 60,3p → `cancelled` | **43,20p → `success`** |
| số bước Windows chạy được | 19/43 | **43/43** |
| bước `test registry`, ubuntu | 14,6 phút | 13,13 phút |
| job `gate (ubuntu-latest)` | — | 24,25p → `success` |

**Biên còn lại dưới trần 60 phút: `60 − 43,20` = 16,80 phút.**

### Số của MASTER, đo riêng — KHÔNG chép số nhánh

Run `34048685345`, head `1b3caa1` (đẩy master sau khi merge PR #457), **lượt đã chạy trọn**, đọc
18:10Z 06-09-2026:

| job | tổng | `test registry` | `packet-loop selftest` | trạng thái |
|---|---:|---:|---:|---|
| `gate (ubuntu-latest)` | **26,52 p** | 14,33 | 3,98 | `success`, 43/43 bước, 4 `skipped` |
| `gate (windows-latest)` | **42,28 p** | **17,13** | 9,37 | `success`, 43/43 bước, 6 `skipped` |

**Biên dưới trần 60 trên master: `17,72` phút.** Phút tính tiền của lượt master:
`26,52 + 42,28×2` = **111,08**.

Số master và số nhánh **KHÁC NHAU và trôi theo hai hướng ngược nhau**: ubuntu `26,52` so `24,25`
(master ĐẮT hơn), Windows `42,28` so `43,20` (master RẺ hơn), `test registry` ubuntu `14,33` so
`13,13`. Cùng một cây (`426bfc0` là cha của merge `1b3caa1`, không có thay đổi mã nào giữa hai
lượt về phần gate đo) mà biên độ tới `1,2` phút ⇒ **nhiễu runner cỡ ±1 phút là có thật**, và mọi
ngưỡng ở `nghiem_thu` phải chừa biên cho nó.

Đó là lý do bảng này tách khỏi bảng trên thay vì dùng chung. **Phiên thi công phải ĐO LẠI cả hai
bảng** — đây là số của 06-09-2026, và `L5` nói con số đúng lúc viết vẫn sai lúc người khác đọc.

### Chi phí nằm ở đâu — phân rã theo bước, run `34045664423`

Đơn vị: **phút tường của một bước** (`completed_at − started_at`), không phải phút CPU, không
phải trung bình.

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

Chênh job − Σbước = **0,03 phút** trên Windows, **0,05** trên ubuntu ⇒ **không có chi phí ẩn
ngoài các bước**. Mọi khoản cắt phải cắt vào một bước có tên, không có "phí hạ tầng" nào để tiết
kiệm.

Chi phí thiết lập (bước 1–10, tính riêng vì nó là thứ **bị nhân lên** khi tách job):
**Windows 3,33 phút · ubuntu 1,18 phút**.

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

### Ba lần cùng một hình dạng — và vì sao packet này KHÔNG nâng trần

`ci.yml:53-63` ghi lại đủ: `25` → `45` → `60`, ba lần nâng `timeout-minutes`, và chính chú thích
ấy tự kết luận *"NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN"*. `docs/PROTOCOL_DA_PHIEN.md §12`, câu cuối:
*"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem lại có nên tiếp tục cách làm đó, không chỉ
vá lần thứ tư."*

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
thêm **điều kiện** — phân biệt ấy là ranh giới của packet.

### Cái giá của việc tách job — tính bằng số, không bằng cảm giác

Chia `gate` thành ba job trên **cùng một ma trận nền**:

- `gate` — mọi bước trừ hai bước nặng
- `gate-registry` — thiết lập + `test registry`
- `gate-packet-loop` — thiết lập + `packet-loop selftest`

Số học suy thẳng từ bảng phân rã (run `34045664423`), **không phải ước lượng**:

| | Windows hôm nay | Windows sau khi tách | ubuntu hôm nay | ubuntu sau |
|---|---:|---:|---:|---:|
| `gate` | 43,20 | 15,77 | 24,25 | 7,42 |
| `gate-registry` | — | **21,03** | — | 14,32 |
| `gate-packet-loop` | — | 13,03 | — | 4,83 |
| **job dài nhất** | **43,20** | **21,03** | **24,25** | **14,32** |
| **tổng phút tường** | 43,20 | 49,83 | 24,25 | 26,57 |

- **Wall clock job dài nhất: `43,20` → `21,03` phút Windows = −51,3 %.** Biên dưới trần 60 đi từ
  `16,80` lên `38,97` phút.
- **Phút TÍNH TIỀN: tăng.** Windows nhân hệ số **×2** (`ci.yml:19-23`): `43,20×2 = 86,40` →
  `49,83×2 = 99,66`. Cộng ubuntu `24,25 → 26,57`. Tổng một lượt master:
  **`110,65` → `126,23` phút tính tiền = +15,58 (+14,1 %)**.

Khoản tăng ấy là **ba lần trả tiền thiết lập** thay vì một (`3,33×2 + 1,18×2` phút tường). Nó
không phải hiệu ứng phụ mà là **chính cái giá** của tách job, và nó đụng đúng chỗ kho này đã chết
một lần: `ci.yml:19-24` ghi CI đứng hình từ 12-08-2026 vì cạn hạn mức 2.000 phút/tháng.
**Đây là con số chủ kho phải duyệt, không phải con số phiên thi công tự nuốt.**

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng thêm**. Write set là **1 tệp**.
`ci.yml` hiện **588 dòng**; tách job chủ yếu là **di chuyển** bước, nên dòng thêm ròng dự kiến
thấp. Vượt `300` thì DỪNG trước review.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.github/workflows/ci.yml` | định nghĩa job `gate` và toàn bộ 39 bước của nó |

Không ký tự đại diện. Không đường dẫn nào khác.

**Không giao với ba packet mutant-Windows** (`LO-319-LINUX-BANG-CHUNG-XANH`,
`MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`, `MUTANT-WINDOWS-NHANH-DON-DUOC`) — chúng chạm
`.claude/**` và `ops/nhanh_don_duoc_test.py`. Packet này chạy **song song** được với cả ba.
Đo 17:46Z: `ai-dang-giu .github/workflows/ci.yml` ⇒ `NGƯỜI_GIỮ 0: không có`. Quét hai nguồn:
`ls-remote` **295** ref · `for-each-ref` **295** ref · `comm -23` rỗng ⇒ không mù.

## `ngoai_pham_vi`

1. **`timeout-minutes` — CẤM đụng, theo cả hai chiều.** Không nâng (hình dạng đã hỏng ba lần), và
   cũng không hạ để "ép kỷ luật": hạ trần biến một job chậm thành một job `cancelled`, tức đổi
   một vấn đề đọc được thành một vấn đề vô hình. Trần đứng nguyên ở `60`.
2. **Chạy CÓ ĐIỀU KIỆN theo diff / theo nhãn / theo `paths`.** Đã có đặc tả đóng băng
   (`CI-FASTPATH-THEO-DIFF.md`) và bản triển khai đã bị bỏ (PR #247 đóng). Kho đã trả giá hai lần
   cho logic điều kiện của workflow. Không mở lại trong packet này.
3. **Song song hoá TRONG `test registry`** (`chay_moi` chạy 8 bộ tuần tự). Đây là hướng **rẻ hơn
   về phút tính tiền** vì nó cắt cả wall clock lẫn billing, nhưng: (a) nó chạm
   `.claude/dev/ci_dang_ky_test.py` — giao write set với cả ba packet mutant-Windows, tức nối
   tiếp thêm một lượt; (b) hiệu quả của nó trên Windows **chưa đo được** vì không có phân rã theo
   bộ trên nền ấy; (c) đo trên Linux 17:47Z 06-09: tuần tự `400` giây, mà bộ dài nhất một mình là
   `270` giây ⇒ trần song song hoá là `−32,5 %`, và sau khi hai packet mutant-Windows land thì
   phần cắt được co lại còn `≈ 5 %` (tổng tuần tự ước `284` giây, bộ dài nhất vẫn `270`).
   **Nợ có tên: `SONG-SONG-HOA-TRONG-TEST-REGISTRY`** — mở packet riêng SAU khi có phân rã theo bộ
   trên Windows.
4. **Cắt vòng lặp đột biến của `packet_loop_test.py`.** Bước ấy tốn **9,70** phút Windows
   (22,5 %) so `3,65` ubuntu; tệp `4.733` dòng và nhắc đột biến ở **169** chỗ (đo 17:43Z
   06-09-2026). Cùng hình dạng bản vá với #456, và có lẽ là khoản cắt lớn thứ hai của kho — nhưng
   nó là `.claude/dev/packet_loop_test.py`, không phải `ci.yml`. **Nợ có tên:
   `MUTANT-WINDOWS-PACKET-LOOP`.**
5. **Bỏ bước trùng** — đã đo, **0 bước trùng** (xem bối cảnh). Không có gì để làm.
6. **Không đổi tập bước, không đổi lệnh của bước nào.** Packet này chỉ đổi bước ấy nằm trong
   **job** nào.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Hai bước nặng nhất (`test registry`, `packet-loop selftest`) chuyển sang job riêng, cùng ma trận nền với `gate`. | `write_set` #1 |
| M2 | **Độ phủ không đổi**: tập `(tên bước, nền, kết luận)` sau khi tách phải bằng đúng tập trước khi tách. Không bước nào biến mất, không bước nào đổi từ `success` sang `skipped`. | `write_set` #1 |
| M3 | Điều kiện chạy Windows KHÔNG đổi: mọi job mới dùng CÙNG biểu thức `fromJSON(...)` của `gate` hôm nay (`workflow_dispatch` ∨ `master` ∨ nhãn `windows`). Không thêm một mặt điều kiện nào. | `write_set` #1 |
| M4 | `timeout-minutes: 60` giữ nguyên trên **mọi** job. | `write_set` #1 |
| M5 | Phút tính tiền tăng thêm được **đo và công bố**, không phải ước — nó là số chủ kho đã duyệt trước, và lượt chạy phải xác nhận nó. | `write_set` #1 |
| M6 | Bảo vệ nhánh vẫn có cổng: nếu `gate` đang là required status check thì hai job mới cũng phải được khai, kẻo tách job = tháo cổng. | `write_set` #1 |

## `nghiem_thu`

**A1 (M1) — job dài nhất giảm, đo bằng PHÚT TƯỜNG CỦA JOB.**
`workflow_dispatch` `ci.yml` trên nhánh packet. Đòi: `max(thời lượng job)` trên `windows-latest`
**≤ 25,00 phút**. Ngưỡng ấy suy từ số học `21,03` cộng `~4` phút biên cho nhiễu runner.
Đơn vị: **`completed_at − started_at` của JOB**, đọc qua `actions_list` +
`method: list_workflow_jobs`; lấy `max` trên tất cả job của lượt, không lấy tổng.
Phép làm ĐỎ: gộp lại một job ⇒ `43,20` ⇒ ĐỎ. Và: nếu `max` **không** giảm dù đã tách, đó là
**KẾT QUẢ ĐO** (chi phí thiết lập trên Windows lớn hơn `3,33` phút đã đo) — báo chủ kho, đừng nới
gì để ép nó xanh.

**A2 (M2) — độ phủ không đổi, đo bằng TẬP HỢP, không bằng số đếm.**
Lấy `(job, tên bước, nền, conclusion)` của lượt TRƯỚC (`34048685345`, master `1b3caa1`) và của
lượt SAU trên nhánh packet. Bỏ cột `job`, rồi so **tập** `(tên bước, nền, conclusion)`.
Hai tập phải **bằng nhau**.
Đơn vị: **tập bộ ba**, không phải `wc -l`. Lý do dùng tập chứ không dùng số đếm là bài học đã đo
của kho: hai tập lệch vẫn có thể cùng lực lượng (`CLAUDE.md`, mục `git for-each-ref`).
Nền hôm nay để đối chiếu: ubuntu **43/43** bước chạy, **4** `skipped`; Windows **43/43**,
**6** `skipped` (đo trên `34045664423`).
Phép làm ĐỎ: quên chép `if: runner.os != 'Windows'` sang job mới ⇒ một bước đổi từ `skipped` sang
`success` (hoặc ngược lại) ⇒ tập lệch ⇒ ĐỎ. Mười bước có `if:` là mười cơ hội để hỏng chỗ này.

**A3 (M3) — không thêm mặt điều kiện nào.**
Phép làm ĐỎ: đếm **số biểu thức `${{ }}` điều khiển việc CHẠY** (`if:` mức job/bước, `strategy`,
`concurrency`) trước và sau. Sau khi tách, mỗi job mới được phép mang **bản sao nguyên văn** của
biểu thức ma trận; **số biểu thức KHÁC NHAU** (tập chuỗi sau khi chuẩn hoá khoảng trắng) phải
không tăng.
Đơn vị: **lực lượng tập chuỗi biểu thức phân biệt**, không phải số lần xuất hiện.
Kèm chốt cứng: `actionlint` phải `rc` **không đổi so với `origin/master` đo trong CÙNG một lệnh,
CÙNG một môi trường** — `CLAUDE.md` đã đo `rc=1` khi có `shellcheck` và `rc=0` khi vắng, nên
"delta = 0" mới là tiêu chí, không phải "rc = 0".
Và: **không viết cú pháp `${{ }}` trong comment của `run:`** — kho đã bị GitHub từ chối cả tệp
vì đúng chuyện đó (`ops-don-ref.yml`, run `31971137920`, 0 job, `conclusion: failure`).

**A4 (M4) — trần không đổi.**
Phép làm ĐỎ: `grep -c 'timeout-minutes: 60'` phải bằng **số job**, và không tồn tại
`timeout-minutes` mang giá trị khác. Bất kỳ giá trị khác `60` ⇒ ĐỎ, kể cả nhỏ hơn.

**A5 (M5) — phút tính tiền được ĐO và công bố.**
Tính `Σ(thời lượng job × hệ số nền)` với hệ số `windows = 2`, `ubuntu = 1`, cho lượt TRƯỚC và
lượt SAU trên cùng bộ bước.
Nền đo (`34045664423`): **110,65** phút tính tiền. Dự kiến sau: **126,23** (**+14,1 %**).
Đòi: số đo thật **≤ 135,00** phút tính tiền.
Đơn vị: **phút tính tiền** = Σ phút tường của job × hệ số nền.
Phép làm ĐỎ: vượt `135,00` ⇒ ĐỎ ⇒ tách job đắt hơn dự kiến ⇒ báo chủ kho.
**Tiêu chí này KHÔNG được bỏ dù A1 xanh.** Packet này mua wall clock bằng billing; một lượt đo
chỉ nói nửa đầu là một lời khai thiếu nửa sau, và nửa sau là thứ đã giết CI của kho một lần.

**A6 (M6) — cổng không bị tháo khi tách.**
`docs/PROTOCOL_DA_PHIEN.md` và `ci.yml:206` khai nợ có tên `PLAT-X5-required-status-check`:
selftest **không thể** tự chứng minh job được GitHub gọi. Nên A6 là **hai phần, và phần thứ hai
KHÔNG đo được từ phiên thi công**:
- (a) đo được: bản vá phải in ra danh sách tên job mới, đúng dạng chuỗi mà branch protection dùng;
- (b) **không đo được từ phiên**: branch protection phải được cập nhật để require cả ba job.
  Đây là việc của chủ kho.
Phép làm ĐỎ cho (a): tên job trong `ci.yml` khác tên in ra ⇒ ĐỎ.
Cho (b): **không có phép đo** — ghi thẳng, và nó phải nằm trong thân Issue như một mục chủ kho
phải làm TRƯỚC khi merge. Tách một job đang được require thành ba job mà chỉ require một là
**tháo cổng bằng một thao tác trông như tối ưu hoá** — cùng họ `[skip ci]` làm PR #100 có 0 check
mà vẫn `mergeable_state: clean`.

**A7 — không đụng gì khác.** `git diff --numstat` chỉ hiện đúng **1** đường dẫn.

## `hinh_dang_ke_thua`

Chép từ `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md`, `ops/specs/CI-CAI-JSONSCHEMA-r3.md` và từ
chú thích của chính `ci.yml`:

| hình dạng | số lần đã gặp | ghi chú |
|---|---:|---|
| nâng `timeout-minutes` để mua cổng xanh | **3** (`25`→`45`→`60`) | Điều kiện DỪNG của packet này. `§12` đòi xem lại CÁCH LÀM từ lần thứ ba; câu trả lời ở đây là **tách job**, không phải trần. |
| thêm một mặt ĐIỀU KIỆN vào workflow rồi nó vắng mặt lặng lẽ | **2** | `paths:` không bắn ở lần đẩy tạo nhánh mới · `pull_request:` thiếu `types:` nên nhãn `windows` không sinh lượt chạy. Cộng lần thứ ba suýt xảy ra: `CI-FASTPATH-THEO-DIFF` (PR #247 đóng). ⇒ `ngoai_pham_vi` #2. |
| cổng vắng mặt trông giống cổng xanh | **≥ 3** | `[skip ci]` (PR #100, 0 check `clean`) · job `cancelled` không phải `failure` · `ops-don-ref.yml` bị GitHub từ chối, 0 job. Tất cả là lý do A2 so TẬP và A6 tách hai phần. |
| khai một phép đo là `KHÔNG ĐO ĐƯỢC` rồi để nguyên | **1** (`CI-CAI-JSONSCHEMA-r3` A5) | Đã đóng lại: #456 sinh ra số đo Windows đầu tiên. Ba mục `chua_do_duoc` của #456 nay đóng được — xem dưới. |
| tối ưu hoá CI mà không nêu phút TÍNH TIỀN | **1** | `ci.yml:19-24`: CI đứng hình từ 12-08-2026 vì cạn 2.000 phút/tháng. ⇒ A5 là bắt buộc. |

### Ba mục `chua_do_duoc` của #456 — nay đóng được

| mục của #456 | trạng thái sau #456 |
|---|---|
| #1 *"tổng thời gian thật của job Windows"* | **ĐÓNG.** `43,20` phút, run `34045664423`, 43/43 bước. |
| #3 *"tỉ lệ 3× là đo TỔNG BƯỚC, không đo riêng đột biến"* | **ĐÓNG một phần.** Ước `44,3p → ~14p` cho `test registry`; thật là `17,70`. Ước lệch `+26 %` về phía đắt hơn. Ghi lại vì nó hiệu chỉnh mọi ước theo tỉ lệ về sau. |
| #4 *"không có đường đo Windows tại chỗ"* | **KHÔNG ĐÓNG.** Vẫn đúng, xem `chua_do_duoc` #2 dưới đây. |

## `chua_do_duoc`

1. **Chi phí thiết lập trên Windows sau khi tách chưa ai đo.** `3,33` phút là đo của **một** job.
   Job mới có thể tốn khác (cache runner, thứ tự cấp máy). Mọi con số ở bảng "cái giá" là **số
   học từ số đo cũ**, không phải phép đo mới. A1 và A5 là hai phép đo trả lời câu ấy — và nếu
   chúng ĐỎ thì đó là kết quả, không phải thất bại.
2. **Không có đường đo Windows tại chỗ.** Container Linux. Mọi khẳng định về Windows đi qua CI.
   Kế thừa nguyên vẹn từ #456 `chua_do_duoc` #4.
3. **Chỉ có MỘT lượt master chạy trọn để so.** `34048685345` là lượt master đầu tiên có chân
   Windows `success`; trước đó mọi lượt đều `cancelled` ở trần. Nên `42,28` phút **không có
   phương sai** — không biết nó là điển hình hay là một lượt may. Biên độ `1,2` phút giữa lượt
   nhánh và lượt master là dấu hiệu duy nhất về nhiễu, và một điểm dữ liệu không dựng được phân
   phối. Ngưỡng `≤ 25,00` ở A1 chừa `~4` phút cho chuyện đó; nếu phiên thi công có thêm lượt
   master nào thì **đo lại phương sai trước**, đừng tin một điểm.
4. **Ba packet mutant-Windows sẽ làm nền trôi.** `LO-319`, `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`
   và `MUTANT-WINDOWS-NHANH-DON-DUOC` đều cắt vào `test registry` — tức vào **41 %** chi phí
   Windows mà packet này đang phân rã. Nếu chúng land trước, mọi ngưỡng tuyệt đối ở A1/A5 quá
   lỏng; nếu land sau, chúng làm chính phép đo của packet này cũ đi. **Không có thứ tự nào làm
   con số đứng yên** — nên A1/A5 phải được ĐO LẠI ngay trước khi merge, và ngưỡng phải nêu lượt
   chạy nó neo vào.
5. **Không đo được branch protection từ phiên.** `PLAT-X5-required-status-check`. Xem A6(b).
6. **Không đo được hệ số nhân thật của Windows.** `×2` lấy từ chú thích `ci.yml:19-23`
   (r245, 13-08-2026), không từ hoá đơn. Nếu hệ số đã đổi thì con số phút tính tiền ở A5 sai theo
   hệ số ấy — nhưng **chiều** của kết luận (tách job làm tăng billing) không đổi.
