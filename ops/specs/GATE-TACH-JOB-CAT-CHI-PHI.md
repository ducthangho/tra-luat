# Đặc tả packet — GATE-TACH-JOB-CAT-CHI-PHI

- `packet_id`: **GATE-TACH-JOB-CAT-CHI-PHI** (bí danh chữ; ID bền theo `PROTOCOL §3.2` là
  `wp<packet_issue>`, suy ra được ngay khi có số Issue — tiền lệ #456 giữ bí danh ở `packet_id`,
  số ở `packet_issue`)
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** `§3.2` đòi; lease #456 không có, và không có
  mission nào đang mở cho lane này. Khuyến nghị: mở MỘT Mission Issue cho cả bốn packet
  (`GATE` · `LO` · `2A` · `2B`); nếu không, ghi số Issue của `#456` và nói rõ đó là thay thế.
- `revision`: 1 · `generation`: 1 — giữ 1 có chủ ý (nháp thứ ba của revision 1, chưa có Issue nên
  chưa đóng băng; lý do đầy đủ và quy ước `lease_id …-exec-1rN-…` đo được ở `LO-319` dòng `revision`)
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (`.github/workflows/` — `PROTOCOL §8` loại
  trừ tường minh khỏi patch-as-hint; đây là ĐỊNH NGHĨA của cổng, không phải mã dưới cổng)
- `depends_on`: **`[]`** — RỖNG VÌ: packet này đi **ĐẦU** chuỗi nối tiếp `GATE → LO → 2A → 2B`
  (lý do ở `write_set`). Nó chỉ chờ lease #456 được thu hồi (A9), không chờ packet nào.
- `base_sha`: `1b3caa1` (`origin/master`, đo 17:47Z 06-09-2026; `core.abbrev=7`) — vì đi đầu, ba
  mỏ neo trong lease (`base_sha` · `start_from_sha` · `reviewed_sha_required`) vẫn phải **đo lại
  tại lúc cấp** bằng head `origin/master` khi ấy; `1b3caa1` là số của lúc soạn.

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

⇒ **nhiễu runner cỡ `1`–`2,3` phút ở mức job là có thật**, và mọi ngưỡng ở `nghiem_thu` phải chừa
biên cho nó. Hai lượt là **hai điểm dữ liệu**; không dựng được phân phối (xem `chua_do_duoc` #3).

Đó là lý do bảng này tách khỏi bảng trên thay vì dùng chung. **Phiên thi công phải ĐO LẠI cả hai
bảng** — đây là số của 06-09-2026, và `L5` nói con số đúng lúc viết vẫn sai lúc người khác đọc.

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

Chia `gate` thành ba job trên **cùng một ma trận nền**:

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
(3 tệp, vẫn ≤ 3), không phải cắt bớt bước.

Write set là **2 tệp**.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.github/workflows/ci.yml` | định nghĩa job `gate` và toàn bộ 39 bước của nó |
| 2 | `.claude/dev/ci_dang_ky_test.py` | consumer `loi_ruff_ci` khoá cứng `jobs.gate`; tách job mà không sửa nó thì bước `test registry` tự đỏ (đo 19:33Z) |

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
| số đo của GATE (A1/A2/A5) | đo trên cây **chưa đổi** — nền `34045664423`/`34048685345` còn đúng | nền trôi sau ba packet cắt `test registry` (41 % chi phí Windows) ⇒ đo lại cả bảng |
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
6. **Không đổi tập bước, không đổi lệnh của bước nào.** Packet này chỉ đổi bước ấy nằm trong
   **job** nào.
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

## `nghiem_thu`

**A1 (M1) — job dài nhất giảm, đo bằng PHÚT TƯỜNG CỦA JOB, kèm đầu-cuối của WORKFLOW.**
`workflow_dispatch` `ci.yml` trên nhánh packet. Đòi: `max(thời lượng job)` trên `windows-latest`
**≤ 25,00 phút**. Ngưỡng ấy suy từ số học `21,03` cộng `~4` phút biên cho nhiễu runner (chênh job
đo được giữa hai lượt: `0,92`–`2,27`).
Đơn vị: **`completed_at − started_at` của JOB**, đọc qua `actions_list` +
`method: list_workflow_jobs`; lấy `max` trên tất cả job của lượt, không lấy tổng.
**Kèm, công bố nhưng không đặt ngưỡng** (chưa có nền): thời gian đầu-cuối của cả lượt
(`run.created_at → run.updated_at` khi `status = completed`) trước và sau tách. Đây là phép đo duy
nhất thấy được xếp hàng của ba runner; nếu nó KHÔNG giảm dù `max(job)` giảm, đó là kết quả đo, báo
chủ kho. **Không quy thời gian chờ thành phút tính tiền** — chờ không tính tiền, và ta chưa có dữ
liệu billing.
Phép làm ĐỎ: gộp lại một job ⇒ `43,20` ⇒ ĐỎ. Và: nếu `max` **không** giảm dù đã tách, đó là
**KẾT QUẢ ĐO** (chi phí thiết lập trên Windows lớn hơn `3,33` phút đã đo) — báo chủ kho, đừng nới
gì để ép nó xanh.

**A2 (M2) — độ phủ không đổi, đo bằng TẬP HỢP, không bằng số đếm, trên HAI loại cò.**
Lấy `(job, tên bước, nền, conclusion)` của lượt TRƯỚC và của lượt SAU. Bỏ cột `job`, rồi so **tập**
`(tên bước, nền, conclusion)`. Hai tập phải **bằng nhau**. Làm HAI lần:
- lượt `workflow_dispatch` trên nhánh packet (cả hai nền) so với lượt master `34048685345`
  (`1b3caa1`; nền: ubuntu **43** mục liệt kê, **4** `skipped`; Windows **43** mục, **6** `skipped` —
  `conclusion` từng mục đọc lại bằng `list_workflow_jobs` khi so, không suy từ phép trừ);
- lượt `pull_request` của chính PR packet (ubuntu) so với lượt `pull_request` gần nhất trên master
  trước đó — đây là lượt DUY NHẤT chứng minh ba job **có mặt trên PR**, tức chứng minh không ai đã
  thêm điều kiện chỉ-dispatch (xem A3).
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

**A4 (M4) — trần không đổi.**
Phép làm ĐỎ: `grep -c 'timeout-minutes: 60'` phải bằng **số job**, và không tồn tại
`timeout-minutes` mang giá trị khác. Bất kỳ giá trị khác `60` ⇒ ĐỎ, kể cả nhỏ hơn.

**A5 (M5) — phút tính tiền được ĐO và công bố, neo đúng lượt.**
Tính `Σ(thời lượng job × hệ số nền)` với hệ số `windows = 2`, `ubuntu = 1`, cho lượt TRƯỚC và
lượt SAU trên cùng bộ bước.
Nền: lượt **nhánh** `34045664423` = **110,65** (bảng phân rã theo bước chỉ có cho lượt này, nên
mọi số "sau" suy từ nó); lượt **master** `34048685345` = **111,08** (để đối chiếu nhiễu). Ước sau:
**126,22** (**+14,1 %**) từ lượt nhánh. Đòi: số đo thật **≤ 135,00** phút tính tiền
(`126,22 + ~9` biên, tức `~7 %` — rộng hơn nhiễu job đo được `2,27` nhân hệ số).
Đơn vị: **phút tính tiền** = Σ phút tường của job × hệ số nền. Đo lại cả hai nền tại lúc thi công.
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

**A8 — không đụng gì khác.** `git diff --numstat` chỉ hiện đúng **2** đường dẫn, và cột thêm
≤ `300`.

**A9 — lease #456 không còn giữ TRƯỚC khi bắt tay, đo trên MỌI bản bằng `ai-dang-giu`.**
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

## `hinh_dang_ke_thua`

Chép từ `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md`, `ops/specs/CI-CAI-JSONSCHEMA-r3.md` và từ
chú thích của chính `ci.yml`. Mỗi dòng ghi thời điểm đo hoặc nguồn trích (L5):

| hình dạng | số lần đã gặp | đo/trích lúc (đọc lại 21:03Z 06-09-2026 trên `b1c2284`) | ghi chú |
|---|---:|---|---|
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức `25`→`45`→`60`) | `git log -G 'timeout-minutes:' -- .github/workflows/ci.yml` chạy lại 21:03Z 06-09-2026: `9e4f361` (2026-07-09) · `6d88a2c` (2026-08-29 03:29Z) · `7657bfd` (2026-08-29 04:49Z) | Bản đầu chép `3` từ #456 (đếm mức). Lần kế là lần thứ ba ⇒ `§12` đòi xem lại CÁCH LÀM; câu trả lời ở đây là **tách job**, không phải trần. Điều kiện DỪNG. |
| thêm một mặt ĐIỀU KIỆN vào workflow rồi nó vắng mặt lặng lẽ | **2** | trích `ci.yml:490-506` và `CLAUDE.md` (mục *"Workflow có `paths:`"*, mục nhãn `windows`), đọc lại 21:03Z 06-09-2026; hai sự kiện GitHub không readback lại | `paths:` không bắn ở lần đẩy tạo nhánh mới · `pull_request:` thiếu `types:` nên nhãn `windows` không sinh lượt chạy. Cộng lần thứ ba suýt xảy ra: `CI-FASTPATH-THEO-DIFF` (PR #247 đóng). ⇒ `ngoai_pham_vi` #2, và A3 đo bằng cấu trúc. |
| cổng vắng mặt trông giống cổng xanh | **≥ 3** | trích `CLAUDE.md` (dấu bỏ-qua-CI / PR #100; job `cancelled`; `ops-don-ref.yml` run `31971137920`), đọc lại 21:03Z 06-09-2026; số run tương ứng không readback từ GitHub ở lượt này | dấu bỏ-qua-CI (PR #100, 0 check `clean`) · job `cancelled` không phải `failure` · `ops-don-ref.yml` bị GitHub từ chối, 0 job. Tất cả là lý do A2 so TẬP và A6 tách hai phần. |
| khai một phép đo là `KHÔNG ĐO ĐƯỢC` rồi để nguyên | **1** | trích `ops/specs/CI-CAI-JSONSCHEMA-r3.md:135-160` (A5), đọc lại 21:03Z 06-09-2026 | #456 sinh ra số đo Windows đầu tiên. Ba mục `chua_do_duoc` của #456 — trạng thái TỪNG MỤC ở bảng dưới. |
| tối ưu hoá CI mà không nêu phút TÍNH TIỀN | **1** | trích `ci.yml:19-24` (ghi chú 13-08-2026), đọc lại 21:03Z 06-09-2026 — chú thích chỉ ghi sự cố cạn quota, không ghi quyết định thiếu công bố phí | CI đứng hình từ 12-08-2026 vì cạn 2.000 phút/tháng (số của ghi chú, không phải hạn mức hiện tại). ⇒ A5 là bắt buộc. |
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

1. **Chi phí thiết lập trên Windows sau khi tách chưa ai đo.** `3,33` phút là đo của **một** job.
   Job mới có thể tốn khác (cache runner, thứ tự cấp máy, ba lần checkout `fetch-depth: 0`). Mọi
   con số ở bảng "cái giá" là **ước có đơn vị từ số đo cũ**, không phải phép đo mới. A1 và A5 là
   hai phép đo trả lời câu ấy — và nếu chúng ĐỎ thì đó là kết quả, không phải thất bại.
2. **Không có đường đo Windows tại chỗ.** Container Linux. Mọi khẳng định về Windows đi qua CI.
   Kế thừa nguyên vẹn từ #456 `chua_do_duoc` #4.
3. **Chỉ có HAI lượt chạy trọn để so, và chúng là hai điểm dữ liệu.** `34048685345` là lượt master
   đầu tiên có chân Windows `success`; trước đó mọi lượt master đều `cancelled` ở trần. Chênh giữa
   lượt nhánh và lượt master (`0,92` Windows · `2,27` ubuntu ở mức job · `1,20` ở bước registry
   ubuntu) là dấu hiệu duy nhất về nhiễu, và hai điểm không dựng được phân phối. Ngưỡng `≤ 25,00`
   ở A1 chừa `~4` phút; nếu phiên thi công có thêm lượt master nào thì **đo lại phương sai trước**.
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
