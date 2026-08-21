# ĐẶC TẢ — `PLAT-X8`: cổng TÍNH `effective_review_class`, thôi nhận lời khai

Đặc tả này ĐÓNG BĂNG bằng băm. Lease neo vào `spec_sha256`. Sửa nội dung ⇒ băm đổi ⇒ lease trỏ
vào thứ không còn tồn tại, phải đi qua bản sửa đổi mới. Soạn bằng skill `soan-spec`, 21-08-2026.

**BẢN ĐÓNG BĂNG THỨ HAI, 21-08-2026.** Bản đầu (`9cb54a2e4e7c…`) đã đăng ở PR "#226" và ăn **hai
P1** của cross-review lượt 1 (`codex`, neo commit `c9a1b4e90d`); người giữ kho chọn **sửa đặc tả**
thay vì bác hoặc đẩy sang packet sau. Ba chỗ đổi, không chỗ nào là chữ nghĩa: **mục tiêu 6** tra
bằng bộ định danh thay vì `packet_id` một mình (P1 fail-open, đo được **3/5** packet có nhiều lease
executor) · **§6** thêm `A13`/`A14` làm phản chứng cho đúng ca ấy · **§9.3** khai thẳng rằng cổng
KHÔNG đọc `risk` và `diff thật`, hai trong ba đầu vào §8:567 đòi. Bản đầu **không** còn hiệu lực;
nó ở lại trong lịch sử `git` làm bằng chứng, không phải làm bản dùng được.

| khoá | giá trị |
|---|---|
| `packet_id` | `PLAT-X8` |
| `packet_issue` | 225 |
| `nguon_cap_viec` | nợ **#1**: caveat `chot-tinh-class-van-KHONG-TON-TAI` trong `ops/reviews/plat-m4-human-audit-ducthangho-verdict.receipt.yaml`, và caveat `packet-bi-phan-class-SAI` trong `ops/reviews/plat-m4-review-3-claude-verdict.receipt.yaml` |
| `review_class` | **`sensitive`** — chạm `ops/lease_publish.py`, tức `review/land authority` **và** `gate lifecycle`, hai mục §8:572 gọi đích danh. Không có đường đọc nào khác |
| `hinh_dang_ke_thua` | xem §7 — **KHÔNG** `khong_ap_dung` |

## 0. Sự thật chịu tải, và đơn vị của từng con số (L1)

Đo trên `origin/master` = `3db588c`, 21-08-2026.

| phép đo | kết quả | **đơn vị** |
|---|---|---|
| `rg review_class ops/lease_publish.py` | 0 | số dòng khớp |
| `rg effective_review_class ops/lease_publish.py` | 0 | số dòng khớp |
| `rg schema_version ops/lease_publish.py` | 0 | số dòng khớp |
| `rg review_class ops/lease_publish_test.py` | 0 | số dòng khớp |
| lease trong `ops/leases/` | 49 | số tệp `.yaml` |
| lease khai `review_class` | 10 | số tệp |
| lease khai `effective_review_class` | 0 | số tệp |
| trong 10 tệp ấy: `routine` / `systemic` / `sensitive` | 1 / 5 / 4 | số tệp |
| lease **executor** (có `write_set` không rỗng) | 10 | số tệp |
| lease **reviewer** (không có `write_set`) | 39 | số tệp |
| đường dẫn phân biệt trong `write_set` của mọi lease | 15 | số đường dẫn |
| trong đó `ops/lease_publish.py` | 0 | số lần xuất hiện |
| bộ test tại `3db588c` | 42/42 | số ca đạt / số ca chạy |
| tám lần chạm gần nhất tới `ops/lease_publish*` | +50 … +187 | số dòng thêm mỗi commit |

**Mâu thuẫn làm bằng chứng gốc** — hai lease executor, **cùng `write_set`**
(`.claude/dev/launcher.py` + `.claude/dev/launcher_test.py`), khai hai lớp khác nhau:
`ag-t0-01b-exec-1-antigravity-20260821` = `sensitive`; `plat-m4-exec-2-claude-20260821` = `systemic`.
§8:572 gọi đích danh `launcher`. Bốn lease reviewer của `PLAT-M4` chép tiếp `systemic` ⇒ **5 tệp**
lease mang một lời khai sai.

**Bạn giả, ghi để người sau khỏi `rg` rồi kết luận nhầm:** `ops/chatgpt_review/build_bundle.py:165`
có chuỗi `effective_review_class`, nhưng đó là **tên biến cục bộ** — chỉ kiểm enum rồi **chép** giá
trị đã khai vào manifest, không tính gì từ `write_set`. Không liên quan tới trường của §8.

## 1. Bốn quyết định đã chốt (người giữ kho, 21-08-2026, in-session)

| # | quyết | hệ quả kỹ thuật |
|---|---|---|
| Q1 | reviewer lease **kế thừa** lớp từ lease executor **cùng `packet_id`** | cổng phải quét `ops/leases/` tìm nguồn |
| Q2 | fail-closed đúng chữ §8:569 | không suy được ⇒ `sensitive` |
| Q5 | neo forward-only bằng **`schema_version: 2`** | cổng phải bắt đầu đọc `schema_version` (nay đọc 0 dòng) |
| Q6 | không tìm thấy lease executor ⇒ **`sensitive`** | thắt thứ tự cấp lease: executor trước, reviewer sau |

**Vì sao Q5 KHÔNG neo theo `leased_at_utc`:** mốc ngày phải đứng trên một trường **không cổng nào
kiểm**. Chốt *"timestamp không ở tương lai"* thuộc gói spec-gate (mục D), **chưa xây** — và đã tồn
tại một lease khai `leased_at_utc: '2026-08-22T02:05:00Z'`, tức tương lai, hợp lệ với cổng hiện tại.

**Đường thứ ba đã xét và BÁC:** *"có khai thì kiểm, không khai thì tha"*. Fail-open, và nó vô hiệu
hoá chính packet — `PLAT-M4` **có** khai, chỉ khai sai.

## 2. write_set

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

**Hai tệp, không đường dẫn nào khác.** Trần `sensitive` của
`docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md` là ≤3 tệp / ≤300 dòng thêm; chừa một suất
là cố ý, để lượt vá sau verdict không phải xin mở rộng write set.

Đây là lần **đầu tiên** `ops/lease_publish.py` vào một `write_set` (đo: 0/49). Việc mở tệp ấy đã được
người giữ kho duyệt cho gói cưỡng chế kế tiếp (ADR-0044, Q4). Nói thẳng vì cần nói:
`ops/THAM_DINH_CHUNG_CLAUDE_CODEX_KE_HOACH.md:96` từng **cấm** mở tệp ấy cho `W0-R2` — đây là duyệt
MỚI cho mục đích KHÁC, có ghi, không phải lờ đi lệnh cấm cũ.

Lease, prompt và đặc tả này nằm trên nhánh riêng, **không** nằm trên nhánh packet — đã trả giá một
finding P1 vì chuyện đó ở `#195`.

## 3. Va chạm write set — đã đo, xử bằng THỨ TỰ

| packet | trạng thái | đòi | va |
|---|---|---|---|
| `PLAT-X6` (#209) | `state:ready`, **0 lease** | `ops/NO_KY_THUAT.md` + `ops/lease_publish_test.py` | CÓ |
| `PLAT-X7` (#220) | `proposed`, chưa spec, **0 lease** | `ops/lease_publish.py` + `ops/lease_publish_test.py` | CÓ |
| mục **D** spec-gate | chưa mở Issue | `ops/lease_publish*` | CÓ |

Mười lease từng chạm `ops/lease_publish_test.py` đều thuộc `PLAT-X4`/`PLAT-X5`/`SLICE-B-C`, **đã
land**. Nên không lease nào đang giữ hai tệp này ⇒ va chạm là **theo kế hoạch**, không theo lease
đang chạy. Thứ tự chốt: **`PLAT-X8` → `#209` → `PLAT-X7` → mục D**.

## 4. ngoai_pham_vi — CỐ Ý không làm

1. **Không sửa 49 lease cũ.** Forward-only theo Q5. `t23` đòi **mọi** lease thật phải qua cổng; áp
   ngược lại là 49 tệp đỏ cùng lúc. Năm lease sai lớp của `PLAT-M4` **đã** có bản đính chính —
   `ops/DINH_CHINH_REVIEW_CLASS_PLAT_M4.md` — nên hồ sơ đã đúng, chỉ tệp lease giữ nguyên.
2. **Không nới bảng phân loại quá thứ §8 nói NGUYÊN VĂN.** Xem §8 của đặc tả này; nới bảng phải có
   bằng chứng riêng cho từng đường dẫn, và đó là packet khác.
3. **Không đo danh tính model** — đó là `PLAT-X7` (#220), khai `depends_on: [PLAT-X8]`.
4. **Không dựng chốt `spec_path`/`spec_sha256`/timestamp** — đó là mục D.
5. **Không đụng `ops/NO_KY_THUAT.md`.** Nó thuộc write set của `#209`. Nợ sinh ra từ packet này ghi
   vào biên nhận, không vào sổ nợ, cho tới khi `#209` chốt.

## 5. muc_tieu — mỗi dòng chiếu vào một đường dẫn ở `write_set` (L2)

1. Hằng `RC_LOP = 10` (mã 0/2/4/6/8/9 đã dùng hết, đo được ở dòng 38–43). → `ops/lease_publish.py`
2. Bảng `_BANG_LOP`: **DANH SÁCH CHO PHÉP** ánh xạ tiền tố đường dẫn → `routine`/`systemic`. Mọi
   đường dẫn **không khớp** mục nào ⇒ `sensitive`. Không có danh sách cấm. → `ops/lease_publish.py`
3. `_tinh_lop_tu_write_set(write_set)` trả lớp **CAO NHẤT** trong tập
   (`sensitive` > `systemic` > `routine`); `write_set` rỗng hoặc thiếu ⇒ `sensitive`.
   → `ops/lease_publish.py`
4. Tiền tố `planned:` được **cắt bỏ trước khi tra bảng**. Không cắt thì mọi đường dẫn `planned:` rơi
   vào nhánh mặc định — fail-closed đúng chiều nhưng vì **lý do sai**, và bảng thành vô dụng với
   đường dẫn chưa tồn tại. → `ops/lease_publish.py`
5. Lease `role: executor`, `schema_version >= 2`: đòi `write_set` không rỗng; tính lớp; đòi lease khai
   `effective_review_class` **BẰNG** `max(review_class đã khai, lớp tính được)`. Khai thấp hơn ⇒
   `RC_LOP`. Đây là chỗ cưỡng chế §8:567 *"Executor không được hạ lớp."* → `ops/lease_publish.py`
6. Lease `role: reviewer`, `schema_version >= 2`: quét `ops/leases/` tìm lease `role: executor` khớp
   **BỘ ĐỊNH DANH** `(packet_issue, packet_id, generation, spec_sha256_required)` — **KHÔNG** tra bằng
   `packet_id` một mình. Khớp đúng MỘT ⇒ kế thừa `effective_review_class` của nó (Q1). **Không thấy,
   thấy nhiều bản mâu thuẫn, bản tìm thấy không đọc được, hoặc ứng viên THIẾU bất kỳ trường định danh
   nào ⇒ `sensitive`** (Q2, Q6). Ứng viên thiếu trường định danh **không** được hạ xuống làm bản dự
   phòng — thiếu là loại, không phải là tha. → `ops/lease_publish.py`

   **VÌ SAO KHÔNG TRA BẰNG `packet_id` MỘT MÌNH — đây là bản sửa sau P1 của cross-review lượt 1
   (codex, PR "#226"), không phải thiết kế gốc.** Bản gốc giả định mỗi packet có nhiều nhất một lease
   executor. Đo trên `ops/leases/` bác giả định ấy: **3/5 packet có nhiều hơn một** — `PLAT-X5` có
   **4** (`r1`…`r4`), `AG-T0-01B` có **2**, `wp55` có **2** *và hai bản khai `generation` KHÁC nhau*
   (`None` và `2`). Nên tra bằng `packet_id` là chuyện thường gặp chứ không phải ca biên: reviewer sẽ
   thừa kế lớp của một **tiền nhiệm đã chết**, kể cả khi thế hệ hiện tại chưa có lease executor nào —
   tức đi vòng qua đúng nhánh fail-closed của Q6. Chốt "thấy nhiều bản mâu thuẫn ⇒ `sensitive`"
   **không** cứu được ca này: nó chỉ bắn khi các bản KHÁC lớp nhau, còn một tiền nhiệm lớp THẤP đứng
   một mình thì im lặng cấp lớp thấp ấy. Đó là fail-**open**, và nó nằm trong chính cơ chế sinh ra để
   fail-closed.
7. Lease `schema_version: 1` hoặc thiếu trường: **BỎ QUA** chốt lớp, `rc` không đổi. Nếu nó khai
   `leased_at_utc` sau `2026-08-21T00:00:00Z` thì in **CẢNH BÁO** ra stderr, **không** đổi `rc`.
   → `ops/lease_publish.py`
8. Ca `rXX_` khoá từng mục 2–7, và bảng đột biến khoá chúng. → `ops/lease_publish_test.py`
9. `t23` (mọi lease thật phải qua) vẫn **42/42 → N/N**, không tụt số ca, sau khi thêm chốt.
   → `ops/lease_publish_test.py`

## 6. nghiem_thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| A1 | lease executor `schema_version: 2`, `write_set: [.claude/dev/launcher.py]`, khai `review_class: systemic` + `effective_review_class: systemic` ⇒ `rc == RC_LOP` | đột biến: đổi nhánh mặc định của `_tinh_lop_tu_write_set` từ `sensitive` sang `systemic` ⇒ ca ĐỎ |
| A2 | **phản chứng của `PLAT-M4`**: dựng lại đúng nội dung `plat-m4-exec-2-claude-20260821` với `schema_version: 2` ⇒ `rc == RC_LOP`; đổi đúng một trường thành `sensitive` ⇒ `rc == 0` | đột biến: bỏ so sánh `max(khai, tính)` chỉ còn kiểm enum ⇒ ca ĐỎ |
| A3 | lease reviewer `schema_version: 2`, `packet_id: KHONG-CO-EXEC` ⇒ lớp hiệu lực `sensitive` | đột biến: nhánh "không tìm thấy" trả `routine` ⇒ ca ĐỎ |
| A4 | lease reviewer khớp ĐỦ bộ định danh với một executor `sensitive` ⇒ kế thừa `sensitive`; với executor `routine` ⇒ **`routine`** (vế dương phải GIỮ — không có nó thì mọi bản vá "cho chắc" đều biến cổng thành máy trả `sensitive`) | đột biến: bỏ tra định danh, luôn trả `sensitive` ⇒ **vế thứ hai** ĐỎ (vế đầu vẫn xanh — nên ca phải có CẢ HAI vế, một vế không đo được đột biến này) |
| A13 | **tiền nhiệm chết**: một executor `routine` khai `generation: 1`, một reviewer khai `generation: 2`, cùng `packet_id` và `packet_issue` ⇒ **`sensitive`**, KHÔNG kế thừa `routine` | đột biến: tra bằng `packet_id` một mình (thiết kế trước bản sửa) ⇒ ca ĐỎ. Đây là phản chứng của P1 cross-review lượt 1 |
| A14 | executor ứng viên **thiếu** `generation` hoặc `spec_sha256_required` ⇒ `sensitive`, và nó KHÔNG được dùng làm bản dự phòng | đột biến: coi trường thiếu là "khớp mọi giá trị" ⇒ ca ĐỎ. Thiếu là loại, không phải là tha |
| A5 | `write_set: ['planned:ops/chay_lease_publish_test.sh']` phân đúng như bản không có tiền tố | đột biến: bỏ dòng cắt `planned:` ⇒ ca ĐỎ |
| A6 | `write_set: []` và lease thiếu hẳn `write_set` ⇒ cả hai ra `sensitive` | đột biến: coi rỗng là `routine` ⇒ ca ĐỎ |
| A7 | **đột biến NỚI BẢNG**: thêm `.claude/dev/launcher.py → routine` vào `_BANG_LOP` ⇒ ca đích ĐỎ | không có đột biến này thì không biết ca đang đo **bảng** hay đo thứ khác (doctrine `v1.36.68`) |
| A8 | lease `schema_version: 1` y hệt A2 ⇒ `rc == 0`, và stderr **có** chuỗi cảnh báo | đột biến: bỏ chốt `schema_version`, áp cho mọi lease ⇒ ca ĐỎ **và** `t23` ĐỎ (49 lease cũ) |
| A9 | `python3 ops/lease_publish_test.py` ⇒ `rc=0`, `N/N` **hai số bằng nhau**, `N >= 42` | tụt số ca hoặc hai số lệch ⇒ ĐỎ |
| A10 | mọi đột biến A1–A8 chạy trên **BẢN SAO CẢ CÂY** trong thư mục tạm, mỗi đột biến một tên tệp riêng | ghi vào tệp thật rồi khôi phục trong `finally` là bom hẹn giờ đã trả giá; bản sao một tệp làm `HERE` sai và số đo vô nghĩa |
| A11 | `actionlint .github/workflows/*.yml` ⇒ `rc=0` cả 5, **fail-close khi thiếu công cụ** | thay bằng PyYAML ⇒ coi như KHÔNG ĐO ĐƯỢC, ĐỎ |
| A12 | `ready to review` = CI xanh trên **exact head** qua `workflow_dispatch`, **cả hai** job `success` | *"PR xanh"* KHÔNG đủ: `ci.yml` chỉ chạy `ubuntu` cho PR thường |

## 7. hinh_dang_ke_thua (L4)

**Hình dạng kế thừa:** *nhận LỜI KHAI thay cho PHÉP ĐO* — biến thể của *"đếm sự CÓ MẶT thay vì
KHẢ NĂNG"*.

**Bộ đếm chép sang: 6 → packet này là lần thứ 7.** Sáu lần đã ghi, nguồn `#220`:
`which(gh)` · `rest-chung` · `gh auth status` · `mcp-endpoint` · `shutil.which` trong `DUNG_DUOC` ·
đếm cái vỏ công cụ thay vì model đang chạy.

**Khác biệt của lần thứ bảy, và là lý do nó đáng một packet:** sáu lần trước là lỗ **chưa gây hại**.
Lần này đã gây hại, đếm được — **5 tệp** lease sai lớp, **3** lượt review chạy dưới lớp sai, một
packet `sensitive` suýt land bằng `same_provider_approved`.

**KHÔNG kế thừa** bộ đếm `hinh_dang_lap: 3` trong
`ops/reviews/plat-m4-review-2-codex-verdict.receipt.yaml` — đó là hình dạng **khác** (lời gọi review
hỏng vì cách dựng sandbox/bundle). Gộp hai bộ đếm khác hình dạng là làm hỏng chính chốt đếm.

**Trả lời thẳng câu doctrine bắt phải hỏi ở lần thứ ba trở đi** — *"có nên làm việc này không"*, chứ
không phải *"vá thế nào"*: **không nên tiếp tục SUY lớp review từ lời khai.** Packet này bỏ hẳn đường
suy ấy và thay bằng phép TÍNH từ `write_set`. Bộ đếm đang được **trả lời**, không bị lờ.

## 8. Bảng phân loại — thứ packet này KHÔNG dám tự quyết, và con số làm ta phải nói ra

`_BANG_LOP` chỉ được seed bằng thứ §8:572 nói **NGUYÊN VĂN**: `workflow/CI authority` ·
`security/credential boundary` · `dispatcher/reconciler` · `review/land authority` ·
`launcher hoặc gate lifecycle` · `migration dữ liệu và LIVE adapter`.

**Hệ quả, đã đo và phải nói thẳng: 15/15 đường dẫn** từng xuất hiện trong `write_set` của mọi lease
đều ra **`sensitive`** dưới bảng seed ấy — hoặc vì §8 gọi đích danh, hoặc vì rơi vào nhánh mặc định.
Trong 10 lease khai lớp, **6 sẽ bị NÂNG** (1 `routine` + 5 `systemic`), 4 giữ nguyên.

Đây **không** phải lỗi cài đặt; đó là điều Q2=(a) nghĩa là. Nhưng nó có giá vận hành thật: §8 mặc
định *"Codex chỉ nhận Packet `routine`/`systemic` nhỏ"* và *"hết quota mà chưa có human thì pause"* —
mà dưới bảng seed, **không packet nào của kho là `routine`/`systemic`**.

Cần lặp lại vì dễ đọc nhầm: **cổng này mua tính NHẤT QUÁN, không mua tính ĐÚNG của bảng.** Nó chứng
minh *lớp hiệu lực khớp bảng*; nó **không** chứng minh *bảng khớp §8*. Một dòng sai trong bảng là một
lớp sai được cổng **xác nhận** — tệ hơn không có cổng, vì nó biến lời khai sai thành lời khai đã-qua-cổng.
Đó là lý do bảng là danh sách **CHO PHÉP** và lý do A7 tồn tại.

Nới bảng là **ngoài phạm vi** (§4.2): mỗi đường dẫn muốn xuống `routine`/`systemic` phải có lập luận
riêng đối chiếu §8, và đó là quyết định của người giữ kho, không phải của phiên thi hành.

## 9. chua_do_duoc — nói thẳng, không giấu sau chữ "có thể"

1. **Bảng đúng hay không thì packet này không đo được.** Xem §8. Không có phép thử nào trong write
   set biến một dòng bảng sai thành ĐỎ.
2. **Hai cái giá của Q6 chưa đo hết.** (a) Thứ tự cấp lease bị thắt: executor trước, reviewer sau —
   ca thật đã vi phạm (`plat-m4-review-1-codex-20260820` có trước `plat-m4-exec-2-claude-20260821`,
   và kho **không có** `plat-m4-exec-1` nào). (b) Packet do người giữ kho tự làm executor **không bao
   giờ** có lease executor (§2), nên mọi reviewer lease của nó thành `sensitive`. Chưa biết trong 39
   lease reviewer hiện có, bao nhiêu rơi vào (b) — chưa đếm.
3. **Cổng này KHÔNG đọc `risk`, và KHÔNG đọc `diff thật` — hai trong ba đầu vào §8:567 đòi.** Ghi
   sau P1 của cross-review lượt 1 (codex, PR "#226"), và ghi thẳng vì lời khai cũ của đặc tả rộng hơn
   thứ nó làm được. Nguyên văn §8:567: *"Review Class được tính fail-closed từ `risk`, effective write
   set và diff thật."* Đo được: **`risk` KHÔNG TỒN TẠI trong dữ liệu** — `grep '^risk:' ops/leases/` =
   **0/49 tệp** — nên không có gì để đọc; `review_class` khai là thứ gần nhất, và đặc tả này dùng đúng
   nó làm vế `max`. Còn **`diff thật` KHÔNG TỒN TẠI tại thời điểm cổng chạy**: cổng chạy lúc ĐĂNG
   lease, tức TRƯỚC khi executor viết dòng nào. Hệ quả phải nói rõ, không giấu: **một packet khai
   `write_set` sạch rồi diff thật chạm đường nhạy cảm NGOÀI write set vẫn qua cổng này** — nó đo LỜI
   KHAI VỀ PHẠM VI, không đo phạm vi ĐÃ XẢY RA. Đúng hình dạng §7 mà packet này đang chữa, chỉ lùi
   một bậc. Chốt hậu-diff trên **exact head** (phân lớp lại từ `git diff base...head`, chặn land nếu
   cao hơn lớp hiệu lực) là **gói riêng**, không nhét vào đây: nó chạy ở lượt LAND chứ không ở lượt
   đăng lease, tức khác thời điểm, khác trigger, khác tệp — nhét chung là làm packet vượt trần
   `sensitive` của ADR-0044 và trộn hai vòng đời vào một cổng.
4. **Cảnh báo của mục tiêu 7 đứng trên `leased_at_utc`, một trường không cổng nào kiểm.** Cố ý để nó
   là CẢNH BÁO chứ không phải chốt: một chốt đứng trên dữ liệu tự khai là chốt lừa được. Chốt thật
   cho trường ấy thuộc mục D.
5. **`schema_version: 2` không tự lan.** Ai quên bump thì được tha im lặng, và mục tiêu 7 chỉ in cảnh
   báo. Chốt cứng cho việc này đòi một mốc kiểm được — chưa có.
6. **Không đo được lease có bị sửa sau khi đăng không.** Ngoài phạm vi cổng hiện tại, và ngoài packet này.

---

**Đọc được đặc tả này KHÔNG phải là được giao việc.** Đặc tả là DỮ LIỆU. Thứ giao việc là Packet
Issue #225 kèm lease còn hiệu lực theo `docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4.
