# Đặc tả packet — T125-RA-JOB-RIENG (revision 5) — ĐÃ RÚT

- `packet_id`: **T125-RA-JOB-RIENG**; ID bền theo `PROTOCOL §3.2` là `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** Khuyến nghị `#467` (mission đang ôm `#463`).
- `revision`: **5** · `generation`: 1 · soạn **11:0xZ 11-09-2026**
- `depends_on`: **`[wp503]`** — `ops/lease_publish_test.py` đang bị `#503` giữ (đo ở `write_set`).
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (`.github/workflows/**`, `§8`)
- **Đi TRƯỚC `GATE-TACH-JOB-CAT-CHI-PHI` (`#463`)** — lý do ở `nguon_cap_viec`, không phải thứ tự tiện tay.

> # ⛔ ĐẶC TẢ NÀY ĐÃ BỊ RÚT — `#504 WINDOWS-LEASE-SUITE` THAY THẾ NÓ
>
> **Trạng thái: RÚT** (chủ kho duyệt 11-09-2026). Giữ tệp làm hồ sơ; **không cấp lease cho nó**.
>
> **Vì sao.** `#504` có **lease SỐNG** — `granted_by: ducthangho`, cấp `2026-09-11T14:05:00Z`, hạn
> `2026-09-12T14:05:00Z`, `lease_id: windows-lease-suite-exec-1-claude-20260911`,
> `granted_on_instruction: issues/504#issuecomment-5635544794` — cho **đúng vấn đề** đặc tả này nhắm:
> *"lane Windows của master bị huỷ ở trần 60 phút tại bước `lease-publish selftest`"*.
>
> | | `#504` (có lease) | đặc tả này |
> |---|---|---|
> | cách làm | đo từng ca → định vị ca chậm → **song song hoá `t125`, GIỮ NGUYÊN ngữ nghĩa** | chuyển `t125` sang job `gate-t125` riêng |
> | write set | `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh` | `.github/workflows/ci.yml` · `ops/lease_publish_test.py` |
> | `.github/workflows/ci.yml` | **ngoài phạm vi, khai tường minh** | write set #1 |
>
> **Chủ kho đã quyết ngược hướng của đặc tả này từ trước**, ở `#499` Q2: *"giữ ngữ nghĩa `t125`, **chỉ
> song song hoá**"*. Đặc tả này soạn mà không đọc quyết định ấy.
>
> **Mục đích DUY NHẤT của nó** là làm nền của `#463` đo được (xem `nguon_cap_viec`). `#504` làm đúng
> việc ấy bằng đường chủ kho đã chọn, với nghiệm thu **bước 20 ≤ 15 phút**. Nên đặc tả này **không còn
> mua được gì**, và `#463` nay `depends_on: [wp502, wp504]`.
>
> **Thứ còn dùng được, đừng vứt:** phép đo `N1`–`N13` (nhất là bội số **2,9312** / share **65,88 %** có
> hiện vật hai vế một lệnh — `#504` đo độc lập ra **66 %**, hai đường gặp nhau), mô hình ba số hạng của
> ước job Windows, và `BẢNG CONTEXT THEO PHA`. `#463` và `#504` dùng lại được.
>
> **Giá đã trả, ghi để không lặp:** hai lượt cross-review (4 và 5) đổ vào đặc tả này sau khi `#504` đã
> tồn tại (`04:42Z` 11-09). Phiên soạn **đã thấy `#504` trong danh sách Issue mở** lúc ~12:00 mà không
> mở ra đọc — đúng bệnh *"hỏi chỗ TIỆN TAY thay vì hỏi chỗ KẾT LUẬN ĐƯỢC GHI"* mà `CLAUDE.md` tố cáo.
> **Nếp rút ra: trước khi soạn một đặc tả, quét Issue mở xem đã có packet nào nhận cùng vấn đề chưa —
> `write_set` trống KHÔNG chứng minh việc còn trống.**

> **Tệp này KHÔNG thuật lại lịch sử của chính nó.** Vết revision 1–2 và mười lượt cross-review nằm ở
> PR `#508`, Issue `#463` và `git log`. Đặc tả là **hợp đồng ở các trường `§3.2`**, không phải nhật ký.
> Mọi câu ở đây phát biểu ở **thì hiện tại** và là hợp đồng đang hiệu lực; không câu nào là "lời khai lịch sử".

---

## `nguon_cap_viec`

`t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor` chạy lại **toàn bộ** suite
`ops/lease_publish_test.py` **hai** lượt trong tiến trình con (A/B trên `GITHUB_ACTOR`). Nên bước
`lease-publish selftest` tốn **≈ 2,93 lần** thứ nó cần tốn. **Bội số `2,9312` đo trên LINUX** (N3);
bội số trên `windows-latest` **chưa ai đo** (`chua_do_duoc` #1). Cấu trúc *"chạy lại toàn bộ suite hai
lượt"* đúng trên mọi nền; **con số** thì không được khai là đúng trên mọi nền.

Trên `ubuntu-latest` bội số ấy vô hại (`≈ 2,4` phút). Trên `windows-latest` nó là **toàn bộ biên còn
lại của trần `timeout-minutes: 60`**, và từ `10-09-2026` nó làm job bị cắt (bảng `N1` dưới).

**Packet này đổi CHỖ `t125` CHẠY, không đổi NÓ ĐO GÌ.**

## Bằng chứng — ba mức, khai riêng, mỗi số một đơn vị

### ĐO ĐƯỢC, có hiện vật tái lập

| # | khẳng định | giá trị | hiện vật / cách tái lập | đo lúc |
|---|---|---|---|---|
| N1 | job `gate (windows-latest)` trên `push`/`master`: **28** lượt đã kết thúc | **18 `success` · 8 `cancelled` · 2 `failure`** | `do509/do-nen-windows.txt` — `GET /repos/…/actions/workflows/ci.yml/runs?event=push&branch=master` | 10:5xZ 11-09 |
| N2 | **nền hoàn tất gần nhất** | run `34429604548`, head `28ba133`, `10-09T02:28Z`, job **40,63** phút `success`, bước `lease-publish selftest` **2,97** phút `success` | cùng hiện vật N1 | 10:5xZ 11-09 |
| N3 | bội số `TỔNG / B` của suite | **2,9312** | `do509/benchmark.txt` + `benchmark.sh` — hai vế **trong MỘT lệnh**, `A=150,434` s · `B=51,321` s | 10:57–11:00Z 11-09 |
| N4 | `t125` chiếm bao nhiêu suite | **65,88 %** | cùng hiện vật N3: `(150,434 − 51,321) / 150,434` | 10:57Z 11-09 |
| N5 | cờ `--ab-con-noi-bo` làm `t125` `return` mà **vẫn đếm ĐẠT** | cả hai vế N3 in `146/146 đạt; bỏ qua=0` | `do509/benchmark.txt.veA.log` / `.veB.log` | 11:00Z 11-09 |
| N6 | bước 20 nhảy bậc tại **đúng một commit** | `28ba133` → `0721811` (merge PR `#492`): windows **2,97 → 25,83** phút (**8,70×**); ubuntu **1,22 → 2,35** phút (**1,93×**) | hiện vật N1, hai hàng liền nhau | 10:5xZ 11-09 |
| N7 | bất đối xứng nền của cùng lượng việc thêm vào | windows **+22,86** phút · ubuntu **+1,13** phút ⇒ **20,2×** | tính từ N6 | 10:5xZ 11-09 |
| N8 | PR `#492` thêm vào chính tệp suite | **+1327 / −1** dòng `ops/lease_publish_test.py` | `git diff --numstat 28ba133 0721811` | 10:5xZ 11-09 |
| N9 | required status check của `master` **hôm nay** | **đúng MỘT**: `gate (ubuntu-latest)` | `GET /repos/…/rules/branches/master` ⇒ ruleset `bao-ve-cong-dang-lease` id `20856202`, `enforcement: active` | 10:4xZ 11-09 |
| N10 | toán hạng ngữ cảnh mà `matrix.os` thật sự đọc | `github.event_name` · `github.ref` · `github.event.pull_request.labels.*.name` — **KHÔNG** có `inputs` | `yaml.safe_load` trên `origin/master:.github/workflows/ci.yml` | 10:5xZ 11-09 |
| N11 | phút TÍNH TIỀN của **8** lượt `cancelled` ở N1, **không lượt nào cho kết quả hoàn tất hợp lệ** | Σ thời lượng job = **482,55** phút × hệ số windows `2` = **965,10** phút = **48,3 %** hạn mức Free `2.000` phút/tháng | N1; `run_id` `34576916278` `34568864158` `34563553711` `34552510232` `34549206309` `34439063235` `34033930149` `34023635399` | 11:0xZ 11-09 |

### THUẬT LẠI — số GitHub Actions, `run_id` là mỏ neo truy tìm

| # | khẳng định | giá trị |
|---|---|---|
| N12 | phân rã bước của run `34563553711` (windows, `cancelled`, `60,52` phút) | b14 `packet-loop` **7,13** · b15 `bien-nhan v2` **7,38** · b16 `test registry` **15,48** · b20 `lease-publish selftest` **26,25** `cancelled` |
| N13 | phân rã cùng bước của nền N2 (`34429604548`, `success`) | b14 **7,42** · b15 **6,27** · b16 **13,92** · b20 **2,97** |

### ƯỚC CÓ ĐIỀU KIỆN — không phải phép đo

**Mô hình phải có BA số hạng, và hai trong ba CHƯA ĐO ĐƯỢC.** Job Windows sau khi bỏ `t125` là:

```
job_sau = prefix + buoc20_hoan_tat/boi_so + suffix + overhead
  prefix          = 33,97 phut   DO DUOC   19 buoc truoc b20
  buoc20_hoan_tat = >= 26,25     CAN DUOI  buoc bi CAT dung o day
  suffix          = KHONG BIET             cac buoc sau b20 chua chay het
  overhead        = 0,03 phut    DO DUOC   job tru tong buoc
  boi_so          = KHONG BIET             tren Windows (2,9312 la so LINUX)
```

**Xuất xứ `prefix` và `overhead`** (đo 12:5xZ 11-09-2026, `GET /actions/runs/34563553711/jobs`):
run `34563553711` · job `103150987797` · `run_attempt` `1` · `windows-latest` · `conclusion`
`cancelled` · **44** bước, `lease-publish selftest` ở chỉ số **19**. Tổng `started_at..completed_at`
của 19 bước trước nó = **`33,97`**; `job` = **`60,52`**; Σ mọi bước = **`60,48`**.

**Khe `60,52 − 26,25 = 34,27` so `prefix 33,97` lệch `0,30` — và nó hạch toán TRỌN VẸN:**
`suffix đã chạy` **`0,27`** (các bước dọn có `if: always()` vẫn chạy sau khi job bị huỷ) cộng
`overhead ngoài bước` **`0,03`**. Không có phần nào bị xoá khỏi mô hình.
**Lưu ý `suffix`:** `0,27` là phần **đã chạy** của các bước sau `b20` trên lượt **bị cắt** — nó
**không** phải chi phí của chúng trên một lượt chạy trọn, nơi chúng làm việc thật. Nên `suffix`
của mô hình vẫn **KHÔNG BIẾT**, và **không** được đặt bằng `0,27`.

**Phép trừ thẳng `60,52 − 26,25 + 26,25/2,9312 = 43,23` SAI MÔ HÌNH**, và sai theo **ba** hướng cùng
lúc, cả ba đều làm ước **nhỏ hơn** sự thật:
1. nó lấy `26,25` — một **cận dưới** của bước bị cắt — làm **giá trị thật**;
2. nó ngầm đặt `suffix = 0`, trong khi các bước sau `b20` trên một lượt chạy trọn làm việc thật
   (trên lượt bị cắt chúng chỉ kịp chạy phần dọn, `0,27` phút);
3. nó dùng bội số **Linux** cho một job **Windows**.

**Nên đặc tả KHÔNG khai một con số cho job sau tách.** Thứ khai được: bỏ `t125` làm bước 20 giảm theo
hệ số `1/bội_số`; mọi số hạng khác **để mở** cho tới khi có một lượt Windows **hoàn tất** sau khi
packet land — đó chính là `A1(b)`.

**Và dải `40,20`–`53,53` của 18 lượt `success` (N1) KHÔNG phải đối chiếu độc lập**: cả 18 lượt ấy
nằm **trước** `#492`, tức khác tải. Dùng chúng làm cận cho job sau `#492` là mượn mẫu của một tải
khác — đúng bệnh *"ghép sai lượt"*.

### Thứ KHÔNG được suy ra, nói thẳng

**`t125` KHÔNG phải nguyên nhân của việc job bị cắt.** Nó có mặt trong **cả 18** lượt `success` của
N1, khi bước 20 tốn `2,45`–`3,88` phút. Nguyên nhân trực tiếp là **`#492` thêm `+1327` dòng test**
(N8) vào một suite mà `t125` nhân **2,93** lần (N3). `t125` là **hệ số khuếch đại**, không phải nguồn.

Hệ quả cho phạm vi: packet này cắt **hệ số khuếch đại**, và chỉ thế. Nó **KHÔNG** khai rằng việc ấy
đủ đưa job về dải đã đo — hai trong ba số hạng của mô hình trên **chưa đo được**. Nó **không** chạm
phần việc mới của `#492`, và **không** có cổng nào canh tốc độ tăng của
phần ấy (`chua_do_duoc` #3).

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.github/workflows/ci.yml` | thêm job `gate-t125`; thêm cờ vào thân `run` của bước `lease-publish selftest` |
| 2 | `ops/lease_publish_test.py` | cờ mới phải được CHÍNH bộ test hiểu — `t125` là một ca trong tệp này |

Không ký tự đại diện. Không đường dẫn nào khác. **2 tệp**, còn một chỗ trống dưới trần `ADR-0044`
(`sensitive`: ≤ 3 tệp, ≤ 300 dòng thêm) — chỗ trống ấy là **biên an toàn**, không phải chỗ nhét việc.

**Đo `ai-dang-giu` 09:3xZ 11-09-2026** (sau canh hai nguồn ref trên kho nguồn, `comm -23` RỖNG):

```
.github/workflows/ci.yml     rc=0   NGƯỜI_GIỮ 0: không có
ops/lease_publish_test.py    rc=11  NGƯỜI_GIỮ 1: m9-fetch-auth-exec-3-claude-20260911   (#503)
```

⇒ lease cấp **SAU KHI `#503` land**, không phải sau khi hạn danh nghĩa trôi. Phiên cấp lease **đo
lại**, không chép dòng này.

## `ngoai_pham_vi`

1. **KHÔNG tách `test registry` / `packet-loop selftest`** — đó là `#463`. Packet này thêm **đúng một** job.
2. **KHÔNG nâng `timeout-minutes`.** Đã nâng **2 lần, 3 mức** (`25`→`45`→`60`); `§12` coi lần kế là điều kiện DỪNG.
3. **KHÔNG hạ răng `t125`, KHÔNG skip nó trên nền nào.** Nó bắt được lỗi thật (`#396`: rò `GITHUB_ACTOR`
   làm **29** ca đỏ oan).
4. **KHÔNG dùng lại cờ `--ab-con-noi-bo`** — N5 đo được: nó làm `t125` `return` mà **vẫn đếm ĐẠT**.
   Phải là cờ **MỚI**, tên khác, ngữ nghĩa khác.
5. **KHÔNG đụng `.claude/dev/ci_dang_ky_test.py`** — của `#463`.
6. **KHÔNG đổi lệnh của bước nào khác, không thêm bước nào** ngoài các bước của job mới.
7. **KHÔNG chữa phần việc `#492` thêm vào** (N8). Đó là nợ riêng, `chua_do_duoc` #3.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `t125` ra khỏi đường tới hạn của job `gate`: chạy trong job RIÊNG `gate-t125`, **cùng ma trận nền · cùng `timeout-minutes` · cùng `if` mức job**. | `write_set` #1 |
| M2 | Cơ chế bỏ `t125` khỏi lượt chính **FAIL-CLOSE**: thiếu job `gate-t125`, hoặc job có mà không chạy `t125`, ⇒ một cổng **ĐỎ**. | `write_set` #1 |
| M3 | Cờ mới khiến `t125` được đếm là **BỎ QUA CÓ LÝ DO**, KHÔNG phải ĐẠT. | `write_set` #2 |
| M4 | **Độ phủ không đổi**, đo bằng phép chiếu tường minh có **lực lượng tính được** (A4). | `write_set` #1 |
| M5 | Branch protection require **đúng tập CONTEXT của pha này** — tên **instance**, không phải `job_id` (A6). | `write_set` #1 |

## `nghiem_thu`

**Ràng buộc chi phí, áp cho MỌI tiêu chí dưới đây (chỉ thị chủ kho 11-09-2026):**
**KHÔNG phóng lượt CI / full CI khi chưa đủ điều kiện merge.** Cụ thể: mọi lượt
`workflow_dispatch` mà `A1`/`A2`/`A4` cần chỉ được phóng **sau khi** bản vá đã qua lint/test tại chỗ
**và** đã có cross-review; không phóng lượt để "thử xem". Căn cứ đo được: N11 — **965,10** phút tính
tiền (**48,3 %** hạn mức tháng) bị **8** lượt `cancelled` tiêu mà **không lượt nào cho một kết quả
hoàn tất hợp lệ**. *(Nói "không có kết quả hoàn tất hợp lệ", KHÔNG nói "thu 0 thông tin": chính các
bước bị cắt đang được dùng làm cận dưới và làm chẩn đoán trong đặc tả này.)*
Vi phạm ràng buộc này ⇒ ghi vào biên nhận, không tự bỏ qua.

---

**A1 (M1) — `t125` ra khỏi đường tới hạn, đo bằng TỈ LỆ thời lượng BƯỚC. Hai nền, hai vai.**

Ngưỡng `0,45` suy từ cấu trúc, không từ một con số phút: bỏ `t125` còn `1 / 2,9312 = 0,3412` (N3),
cộng biên ⇒ `0,45`. Đơn vị: **giây của BƯỚC**, đọc qua `list_workflow_jobs`.

- **(a) `ubuntu-latest` — VẾ BẮT BUỘC, và nó ĐO ĐƯỢC NGAY.** Bước `lease-publish selftest` trong job
  `gate` sau tách ≤ **`0,45 ×`** thời lượng của chính nó ở lượt nền cùng `event`, cùng nhánh.
  Mẫu số **tồn tại**: **7** lượt `push`/`master` `success` sau `#492` cho `1,90`–`2,42` phút
  (hiện vật `do-nen-hai-nen.txt`, cửa sổ đo **`10-09T04:55Z` … `11-09T11:06Z`**).
  **Không có nhánh `KHÔNG ĐO ĐƯỢC` ở vế này** — mẫu số có sẵn, nên `KHÔNG ĐO ĐƯỢC` ở đây là **ĐỎ**.
  **Mẫu số phải ĐO LẠI tại lúc thi công, KHÔNG chép dải trên.** Bản trước của chính dòng này khai
  `2,32`–`2,42` trên **5** lượt; đo lại `12:4xZ 11-09-2026` ⇒ **7** lượt, dải `1,90`–`2,42` — hai
  lượt mới nhất (`0bf0ba7`, `fe05fa6`) **nằm ngoài** dải cũ. Con số hết hạn trong đúng một ngày.
  Vì thế `A1(a)` neo vào **tỉ lệ so mẫu số ĐO CÙNG LƯỢT**, và dải trên chỉ là chứng cứ rằng mẫu số
  **tồn tại**, không phải một hằng số để so.
  **Phép làm ĐỎ:** để `t125` lại trong job `gate` ⇒ tỉ lệ `≈ 1,00` ⇒ ĐỎ.
  **Đột biến bắt buộc:** cho job `gate-t125` chạy **nhưng không** cho job `gate` bỏ `t125` ⇒ A1(a)
  phải ĐỎ. Đột biến này phân biệt *đo VIỆC BỎ* với *đo SỰ TỒN TẠI của job mới*, và nó **chạy được**
  vì mẫu số ubuntu có sẵn.
- **(c) BỎ TẢI TRÊN CẢ HAI NỀN — phép chứng minh ĐỘC LẬP VỚI THỜI LƯỢNG, và nó BẮT BUỘC.**
  Vế (a) chỉ đo Ubuntu; vế (b) chỉ đọc `conclusion`. Nên **không vế nào phân biệt** hai triển khai:
  *bỏ `t125` trên cả hai nền* và *bỏ `t125` chỉ trên Ubuntu* — nếu lượt Windows của bản thứ hai tình
  cờ hoàn tất thì cả (a) lẫn (b) đều ĐẠT. `M1` và `ngoai_pham_vi` #3 áp **cả hai nền**, nên phải có
  một phép đo áp cả hai nền.
  Đòi, **cho MỖI nền trong ma trận**, lấy từ `list_workflow_jobs` của lượt sau tách:
  1. **thân `t125` KHÔNG được vào** trong job `gate` của nền ấy — đo bằng **BẰNG CHỨNG THỰC THI**,
     không bằng tên hiển thị:
     - `steps[].name` là **tên hiển thị**, không phải `argv`. Tên bước hiện tại **không chứa cờ**,
       và **ép cờ vào tên là làm `A4` ĐỎ** (đổi tên một bước cũ) — hai tiêu chí sẽ đá nhau. Nên
       **giữ nguyên tên bước**, và **cấm** dùng tên làm bằng chứng.
     - Bằng chứng hợp lệ: dòng tổng kết của chính bộ test (`A3`) khai `t125` ở danh sách **BỎ QUA**,
       **cộng** số tiến trình con A/B mà `gate` phóng cho `t125` **bằng 0**. Cả hai neo
       `(run_id, job_id, run_attempt, head_sha, nền)` và lấy từ log của **đúng job ấy**, ghi đường
       lấy log vào biên nhận.
     - **Hạch toán phải xảy ra TRƯỚC khi vào thân.** Một bản vá đặt việc ghi BỎ QUA **sau** thân
       `t125` sẽ **vừa chạy tải vừa báo bỏ** — nhãn đúng, tải vẫn còn.
       **Ca khoá bắt buộc:** hạch toán-sau-thân ⇒ `A1(c)` phải **ĐỎ**. Thiếu ca này thì (1) chỉ đo
       **NHÃN**, không đo **TẢI**.
     - Và nói thẳng cái `A2c` KHÔNG chứng minh: `A2c` chứng minh **job mới CÓ chạy** `t125`; nó
       **không** chứng minh **job `gate` đã NGỪNG** chạy nó. Hai mệnh đề khác nhau, cần hai phép đo;
  2. job `gate-t125` của **chính nền ấy** tồn tại, `conclusion` **không** phải `skipped`, và bản ghi
     A/B của `A2c` có mặt cho nền ấy;
  3. `gate` và `gate-t125` **KHÔNG** nối bằng `needs`, **kể cả GIÁN TIẾP** qua một job trung gian
     (đóng đồ thị `needs` rồi kiểm không có đường đi giữa hai job) — hai job phải chạy
     **song song**; nối chuỗi thì `t125` vẫn nằm trên đường tới hạn của workflow dù đã ra khỏi job.
  **Phép làm ĐỎ:** giữ `t125` **chỉ trên Windows** (bỏ cờ ở nhánh windows của ma trận) ⇒ (1) hỏng ở
  nền windows ⇒ ĐỎ · cho `gate-t125` `needs: gate` ⇒ (3) ⇒ ĐỎ · để `gate-t125` `skipped` trên một
  nền ⇒ (2) ⇒ ĐỎ.
  **Ba điều kiện này KHÔNG thay được nhau:** (1) đo *đã bỏ*, (2) đo *vẫn chạy ở chỗ mới*, (3) đo
  *ra khỏi đường tới hạn*. Thiếu bất kỳ cái nào là mù đúng một hướng.
  **Đây là phép đo khôi phục nghĩa vụ mà vế Windows bắt buộc cũ đang gánh** — chuyển vế bắt buộc
  sang Ubuntu là **thu hẹp**, và thu hẹp phải được thay bằng một phép đo khác, không được bỏ trống.

- **(b) `windows-latest` — VẾ CÔNG BỐ thời lượng.** Đọc và công bố: thời
  lượng bước `lease-publish selftest` và `conclusion` của job `gate`, ở lượt `push`/`master` đầu tiên
  sau khi packet land.
  - job `success` ⇒ trạng thái **`ĐẠT`**; ghi số vào biên nhận. Từ đây nền của `#463` đo được.
  - job vẫn `cancelled` ⇒ trạng thái **`ĐẠT CÓ ĐIỀU KIỆN`**, ghi thẳng vào biên nhận là *"hệ số
    khuếch đại đã bị cắt (chứng minh ở (a)), nhưng job vẫn chạm trần"*, và **báo chủ kho**.
    **KHÔNG** nới `timeout-minutes` (`ngoai_pham_vi` #2), **KHÔNG** hạ răng `t125` (#3).
    **`ĐẠT CÓ ĐIỀU KIỆN` KHÔNG phải `ĐẠT`** — nó là một trạng thái khác, phải xuất hiện khác trong
    biên nhận, và nó chặn `#463` khỏi khai rằng nền đã sẵn sàng.

**Thứ A1 KHÔNG chứng minh:** nó không chứng minh job Windows sẽ chạy trọn. Vế (a) chứng minh
**việc bỏ đã xảy ra**; vế (b) **báo cáo** hệ quả. Không tiêu chí nào ở đây chứng minh ước ở mục
"ƯỚC CÓ ĐIỀU KIỆN", vì bội số trên Windows chưa ai đo.

**A2 (M2) — FAIL-CLOSE, hai nửa, mỗi nửa một phản chứng riêng.**
1. **Thiếu job ⇒ ĐỎ.** Xoá job `gate-t125` khỏi `ci.yml` trong khi job `gate` vẫn mang cờ bỏ ⇒ phải
   có một cổng ĐỎ. **Phép làm ĐỎ:** không cổng nào đỏ ⇒ A2 ĐỎ.
2. **Job có mà KHÔNG chạy `t125` ⇒ ĐỎ.** Giữ job, đổi lệnh thành lệnh không chạy `t125` ⇒ phải ĐỎ.
   Nửa này tồn tại vì nửa (1) chỉ đo **SỰ CÓ MẶT**; kho đã trả giá **4 lần** cho việc đếm sự có mặt
   thay vì khả năng.

**A2c (M1) — job mới phải THỰC SỰ CHẠY HAI LƯỢT A/B, và PHÉP SO phải còn tác dụng.**
Ba nghĩa vụ, **mỗi nghĩa vụ một đột biến làm ĐÚNG nó đổi màu**:
1. **hai tiến trình con** — `t125` phóng đúng **2** lượt, mỗi lượt một `subprocess` riêng.
   **Đột biến:** bỏ một lượt con ⇒ ĐỎ.
2. **hai lượt khác nhau ĐÚNG MỘT biến** — một lượt không có `GITHUB_ACTOR`, một lượt có; bằng chứng
   phải cho thấy **cả hai** giá trị đã tới lượt con.
   **Đột biến:** đổi biến phân biệt thành một biến vô can ⇒ ĐỎ.
3. **phép so verdict còn tác dụng** — và nghĩa vụ này đòi một ca mà **hai verdict KHÁC NHAU**.
   Ca `r5xx_hai_verdict_lech_phai_lam_t125_do`: dựng hai bộ
   `(rc, n/m, tập ĐỎ, tập BỎ QUA)` **lệch nhau đúng một phần tử**, đưa vào chính hàm so của `t125`,
   đòi nó **ném**. Cộng một ca tích hợp dùng cùng hàm ấy trên đường thật.
   **Đột biến:** biến phép so thành no-op (`return` trước khi so) ⇒ **ca này phải ĐỎ**.
   **Vì sao ca này bắt buộc:** khi hai lượt đều sạch, hai verdict **bằng nhau**, nên bỏ phép so
   **không đổi kết quả gì** — nghĩa vụ (1) và (2) vẫn xanh. Chỉ một ca có hai verdict **lệch** mới
   đo được rằng phép so đang làm việc. Đây đúng bệnh *"đột biến sai chỗ ≠ mã đúng"*.

**A3 (M3) — cờ mới cho BỎ QUA CÓ LÝ DO, không cho ĐẠT.**
Chạy `ops/lease_publish_test.py` với cờ mới ⇒ dòng tổng kết khai **`145/146 · bỏ qua = 1`** (mẫu số
đúng lúc thi công), `t125` xuất hiện ở danh sách **BỎ QUA** kèm lý do.
**Phép làm ĐỎ:** cờ làm `t125` `return` im lặng rồi đếm ĐẠT (`146/146`) ⇒ ĐỎ.
**Đối chứng bắt buộc với cờ CŨ:** chạy `--ab-con-noi-bo` ⇒ **vẫn** `146/146` (N5, hành vi hiện tại,
packet này không đổi) ⇒ chứng minh hai cờ có ngữ nghĩa khác nhau.
**Thứ đối chứng này KHÔNG chứng minh:** nó chỉ chứng minh **hai chế độ hạch toán khác nhau**. Nó
không chứng minh job mới chạy hai subprocess — đó là việc của A2c.

**A4 (M4) — độ phủ không đổi, đo bằng TẬP với LỰC LƯỢNG TÍNH ĐƯỢC.**

Lấy `(tên bước, nền, conclusion)` của lượt TRƯỚC và lượt SAU (bỏ cột `job`). Đòi:

```
tập_sau == tập_trước  ∪  { (tên, nền, conclusion) : tên ∈ TEN_BUOC_MOI, nền ∈ ma_trận_nền }
|tập_sau| − |tập_trước| == |TEN_BUOC_MOI| × |ma_trận_nền|
```

**`TEN_BUOC_MOI` — danh sách LITERAL, khai thẳng ở đây, đúng MỘT phần tử:**

```
TEN_BUOC_MOI = [ "lease-publish t125 A/B (job rieng)" ]
```

(Tên chính xác do phiên thi công chốt và ghi vào biên nhận; **danh sách phải có mặt trong `ci.yml`
và trong biên nhận, và hai bản phải khớp từng ký tự.**)

**Vì sao KHÔNG phải "đúng một phần tử":** phép chiếu bỏ cột `job` nhưng **giữ cột nền**. Với ma trận
hai nền, một tên bước mới sinh **hai** bộ ba. Đòi "thêm đúng một phần tử" là **sai ở chính ma trận
mà `A5` bắt buộc** — nên lực lượng phải **tính**, không phải ghi cứng.

**Các bước THIẾT LẬP chép sang job mới đóng góp 0 phần tử** — vì phép chiếu bỏ cột `job`, một bản sao
cùng tên, cùng nền, cùng `conclusion` **đã nằm trong tập**. Đó là tính chất, không phải kẽ hở:
nếu một bản sao cho `conclusion` KHÁC (ví dụ quên chép `if`), tập **lệch** ⇒ **ĐỎ** — đúng thứ M4
cần bắt.

**Phép làm ĐỎ:** thêm bước ngoài `TEN_BUOC_MOI` ⇒ ĐỎ · đổi tên một bước cũ ⇒ ĐỎ · quên chép `if` của
một bước ⇒ `skipped`↔`success` ⇒ ĐỎ · `|TEN_BUOC_MOI| × |ma_trận_nền|` không khớp hiệu lực lượng ⇒ ĐỎ.
**Nếu lượt nền KHÔNG hợp lệ** (job bị cắt) ⇒ hạ xuống so tập `(tên bước, nền)`, bỏ cột `conclusion`,
**và** đòi lượt SAU có **0** bước `cancelled`, **và** mọi bước `skipped` giải thích được bằng `if`
của chính nó. Trạng thái khi ấy là **`ĐẠT CÓ ĐIỀU KIỆN`**, ghi thẳng vào biên nhận.

**A5 (M1) — job mới mang ĐÚNG cùng cấu hình, đo bằng GIÁ TRỊ ĐÃ PARSE.**
`yaml.safe_load(ci.yml)`; với `gate-t125` đòi bộ ba
`(if mức job, chuỗi matrix.os sau chuẩn hoá khoảng trắng, timeout-minutes)` **bằng** bộ ba của `gate`.
Hôm nay `gate` = `(None, fromJSON(…), 60)` (N10).
**Thiếu khoá `timeout-minutes` ⇒ ĐỎ** — không phải chỉ "giá trị khác 60 ⇒ ĐỎ": một job thiếu hẳn khoá
**không tạo ra giá trị khác**.
**Phép làm ĐỎ:** bỏ `timeout-minutes` khỏi `gate-t125` ⇒ ĐỎ · chèn `if:` mức job (kể cả viết **không**
có dấu nội suy) ⇒ ĐỎ.

**A6 (M5) — cổng không bị tháo, và nó ĐO ĐƯỢC.**

- **(a) tên khai ra khớp `ci.yml`.** Bản vá in danh sách **context** job mới.
  **Phép làm ĐỎ:** tên trong `ci.yml` khác tên in ra ⇒ ĐỎ.
- **(b0) MỐC THỜI GIAN — ruleset phải được cập nhật TRƯỚC KHI MERGE.**
  Đọc trạng thái **sau đó** không bảo vệ **lần merge đầu tiên**: một chuỗi *merge trước, thêm context
  sau* vẫn thoả phép so tập ở thời điểm cuối, trong khi chính lần merge ấy **không** bị job mới chặn.
  Đây là **nghĩa vụ thời gian**, không thay được bằng một phép so tập cuối cùng.
  Đòi lưu vào biên nhận: **readback tập context** và **kết quả check trên đúng head được merge**, đo
  **trước** thao tác merge. Mục này phải nằm trong thân Issue như một việc chủ kho làm **TRƯỚC** khi
  merge.
  **Phép làm ĐỎ:** biên nhận chỉ có readback **sau** land ⇒ ĐỎ.
  **Thứ tự an toàn, để không tự khoá đường merge:** job mới phải **đã sinh ra check với đúng tên ấy
  trên PR** rồi mới chuyển require sang nó — đừng bỏ nghĩa vụ chỉ để tránh trạng thái chờ.

- **(b) TRẠNG THÁI THẬT của branch protection — đọc được, nên là tiêu chí, không phải lời nhắc.**
  Đọc `GET /repos/{owner}/{repo}/rules/branches/master`, lấy mục `type == "required_status_checks"`,
  trường `parameters.required_status_checks[].context` ⇒ tập context đang được require.
  Đòi tập ấy **chứa** `gate (ubuntu-latest)` **và** `gate-t125 (ubuntu-latest)`.
  **Không đọc được (rc ≠ 200, thiếu trường, hoặc thiếu quyền) ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ.**
  **Phép làm ĐỎ:** chạy tiêu chí khi ruleset **chưa** được cập nhật ⇒ thiếu `gate-t125 (ubuntu-latest)`
  ⇒ ĐỎ. Đây là phép phân biệt mà bản trước **không có**: Issue trông y hệt nhau ở hai trạng thái
  đã-require và chưa-require, còn phép đọc này thì không.

**HAI LUẬT VỀ TÊN, cả hai đo được (N9), và sai luật nào cũng hỏng:**

1. **Require theo CONTEXT, không theo `job_id`.** Ruleset lưu **tên check**, và với một job có ma
   trận, tên ấy là `"<tên job> (<nền>)"`. **`<tên job>` là `job_id` CHỈ KHI job không khai khoá
   `name:`** — khai `name:` thì check mang giá trị của `name`, và luật này sai. Đo trên
   `origin/master` 12:3xZ 11-09-2026: job `gate` **không** có khoá `name` ⇒ hôm nay context đúng là
   `job_id + nền`. Phiên thi công **đo lại** điều kiện ấy cho mỗi job mới, không suy từ dòng này.
   Đo được: hôm nay require đúng **`gate (ubuntu-latest)`** — chuỗi có dấu ngoặc và tên nền.
   Require chuỗi `gate` trần thì **không khớp check nào** — và hậu quả **không** phải "cổng trang
   trí" mà là **PR bị CHẶN vĩnh viễn**: một required check không bao giờ báo cáo giữ PR ở trạng thái
   chờ. Cùng cơ chế với luật 2 ngay dưới, nên hai luật phải đọc cùng một cách.
2. **KHÔNG require một context mà PR thường KHÔNG BAO GIỜ sinh ra.** `matrix.os` (N10) chỉ cho
   `windows-latest` khi `event_name == workflow_dispatch`, hoặc `ref == refs/heads/master`, hoặc PR
   mang nhãn `windows`. Một PR thường ⇒ **chỉ** `ubuntu-latest`. Nên require
   `gate-t125 (windows-latest)` sẽ **chặn vĩnh viễn mọi PR thường** — check ấy không bao giờ báo cáo.
   Đây là lý do cấu trúc khiến hôm nay chỉ có **một** context được require, và packet này **giữ
   nguyên luật ấy**.

**BẢNG CONTEXT THEO PHA — nguồn DUY NHẤT, dùng chung với `#463`:**

| pha | job trong `ci.yml` | context require (chỉ nền PR thường sinh ra) |
|---|---:|---|
| hôm nay (`master`) | **1** — `gate` | `gate (ubuntu-latest)` |
| **sau khi `T125-RA-JOB-RIENG` land** | **2** | `gate (ubuntu-latest)` · `gate-t125 (ubuntu-latest)` |
| **sau khi `GATE-TACH-JOB-CAT-CHI-PHI` land** | **4** | thêm `gate-registry (ubuntu-latest)` · `gate-packet-loop (ubuntu-latest)` |

Chủ kho cập nhật ruleset **HAI lần**, mỗi packet một lần, **mỗi lần một tập KHÁC nhau**. Khai ở cả
hai đặc tả để lần thứ hai không bị quên, và để không ai require một job chưa tồn tại.

**A7 (toàn packet) — `ADR-0044`.** `git diff --numstat` ⇒ đúng **2** đường dẫn, cột `additions` ≤ `300`.
Vượt ⇒ **DỪNG và hỏi chủ kho**, không tự xin ngoại lệ.

**A8 (toàn packet) — suite không tụt.** `ops/lease_publish_test.py` chạy đủ (job `gate` + job
`gate-t125` gộp lại) phủ **đúng** tập ca như trước.
**MẪU SỐ PHẢI ĐẾM LẠI, KHÔNG CHÉP.** Mọi số `146` trong đặc tả này là **ảnh chụp tại `0236ca7`**
(cùng lúc chạy benchmark N3); đếm bằng AST trên `HEAD` `d81f155` ⇒ **147** ca `@ca` (đo 13:0xZ
11-09-2026). Suite tăng ca theo từng packet land, nên mẫu số **trôi trong vài ngày**.
Hợp đồng là: `tập ca sau == tập ca trước` (so **TẬP**, không so số đếm), và
`đạt + bỏ qua == |tập ca|` với **hai số BẰNG NHAU**; `bỏ qua = 1` là `t125`.
Hai số phải **BẰNG NHAU**; không tin `rc=0` suông.
**Phép làm ĐỎ:** tập ca thiếu, hoặc tăng ngoài hợp đồng. `145+1` tự nó **không** chứng minh `t125`
có chạy A/B — đó là A2c.

## `hinh_dang_ke_thua`

| hình dạng | số lần | nguồn / đo lúc | vì sao có tiêu chí tương ứng |
|---|---:|---|---|
| một job CI mặc định SKIP là một cổng KHÔNG TỒN TẠI | **≥ 3** | `CLAUDE.md` (dấu bỏ-qua-CI/PR #100 · job `cancelled` · `ops-don-ref.yml` 0 job) | A2 có **hai** nửa |
| đếm **SỰ CÓ MẶT** thay vì **KHẢ NĂNG** | **4** | `CLAUDE.md` (`t103`, `gh-cli`, `rest-chung`, `shutil.which`) | A2 nửa (2); A1(a) có đột biến riêng |
| cờ làm một ca `return` im lặng mà **vẫn đếm ĐẠT** | **1** | N5, đo 11:00Z 11-09-2026 | `ngoai_pham_vi` #4; A3 có đối chứng cờ cũ |
| con số trong đặc tả **hết hạn** giữa lúc viết và lúc dùng | **8** | 4 của `#250` + 4 của `#463`, trích `CLAUDE.md` | A1 neo **tỉ lệ**, không neo phút |
| **GHÉP SAI LƯỢT** — tử số lượt này, mẫu số lượt kia | **3** | `#463` (`114,10/177,0`) · `r362` (`1146s`) · nháp r2 của chính tệp này (`15,93`/`8,85`) | mỗi số THUẬT LẠI mang `run_id` riêng; một đoạn chỉ dùng số của **MỘT** lượt |
| **quan hệ đúng che số hạng sai** | **1** | đo 11:0xZ 11-09-2026 trên chính đặc tả này | bản trước khai đồng thời `bội số 3,24` và `share 65,7 %`. Hai số **không nhất quán**: `65,7 %` hàm ý bội `2,9155`; `3,24` hàm ý share `69,14 %`. Cả ba lượt cross-review đọc qua mà không dừng, vì mỗi số **một mình** trông hợp lý. Nay cả hai lấy từ **một** phép đo (N3/N4) và hiện vật ghi cả hai vế. |
| lời khai rộng hơn phép đo | **1** | đo 11:0xZ 11-09-2026 | bản trước khai *"job Windows chưa hoàn tất lần nào"*; N1 đo được **18** lượt `success`, **11** trong số đó SAU mốc mà bản trước dẫn. Lý do mục "Thứ KHÔNG được suy ra" tồn tại. |

## `chua_do_duoc`

1. **Bội số `2,9312` đo trên LINUX, chưa ai đo trên Windows.** N7 cho thấy hai nền **không** tỉ lệ
   với nhau ở phần việc mới (`20,2×`), nên không được mặc định bội số bằng nhau. Mọi con số
   "sau khi bỏ `t125`" trên Windows là **ƯỚC**. A1 vì thế đặt vế bắt buộc ở **ubuntu** (mẫu số có
   thật) và vế **công bố** ở windows.
2. **Không có đường đo Windows tại chỗ.** Container Linux; mọi khẳng định về Windows đi qua CI.
3. **Phần việc `#492` thêm vào KHÔNG ai canh.** `+1327` dòng test (N8) làm `B` tăng
   `≈ 8,7×` trên Windows trong **một** commit. Packet này cắt hệ số khuếch đại, **không** chạm phần
   ấy. Không cổng nào canh tốc độ tăng của suite — **nợ, chưa có tên, ngoài phạm vi**.
4. **Bội số có thể trôi.** N3 đo tại `0236ca7`; mỗi ca thêm vào suite đổi cả `A` lẫn `B`. Phiên thi
   công **chạy lại `benchmark.sh`** tại `start_from_sha` và ghi số mới vào biên nhận, **không** chép
   `2,9312`.
5. **Trạng thái ruleset đọc bằng `GITHUB_PAT` của phiên.** `GET /branches/master/protection` trả
   **403** `Resource not accessible by integration` (có `X-GitHub-Request-Id` ⇒ tới GitHub, là vấn đề
   **quyền token**, không phải proxy). Đường dùng được là `/rules/branches/master` (rc `200`).
   **Cảnh báo đã trả giá trong chính lượt soạn này:** trường `protection` trong
   `GET /branches/master` trả `enforcement_level: "off"`, `contexts: []` — một **bản nhìn suy giảm**,
   ngược hẳn sự thật. Tin nó là kết luận *"master không require check nào"*. **Chỉ đọc
   `/rules/branches/master`**, và nếu nó không đọc được thì `KHÔNG ĐO ĐƯỢC`, **không** lùi về trường kia.
