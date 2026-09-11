# Đặc tả packet — T125-RA-JOB-RIENG (revision 3)

- `packet_id`: **T125-RA-JOB-RIENG**; ID bền theo `PROTOCOL §3.2` là `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** Khuyến nghị `#467` (mission đang ôm `#463`).
- `revision`: **3** · `generation`: 1 · soạn **11:0xZ 11-09-2026**
- `depends_on`: **`[wp503]`** — `ops/lease_publish_test.py` đang bị `#503` giữ (đo ở `write_set`).
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (`.github/workflows/**`, `§8`)
- **Đi TRƯỚC `GATE-TACH-JOB-CAT-CHI-PHI` (`#463`)** — lý do ở `nguon_cap_viec`, không phải thứ tự tiện tay.

> **Tệp này KHÔNG thuật lại lịch sử của chính nó.** Vết revision 1–2 và mười lượt cross-review nằm ở
> PR `#508`, Issue `#463` và `git log`. Đặc tả là **hợp đồng ở các trường `§3.2`**, không phải nhật ký.
> Mọi câu ở đây phát biểu ở **thì hiện tại** và là hợp đồng đang hiệu lực; không câu nào là "lời khai lịch sử".

---

## `nguon_cap_viec`

`t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor` chạy lại **toàn bộ** suite
`ops/lease_publish_test.py` **hai** lượt trong tiến trình con (A/B trên `GITHUB_ACTOR`). Nên bước
`lease-publish selftest` tốn **≈ 2,93 lần** thứ nó cần tốn, trên **mọi** nền.

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
| N11 | phút TÍNH TIỀN bị 8 lượt `cancelled` đốt mà **không thu được thông tin nào** | **723,96** phút (hệ số windows ×2) = **36,2 %** hạn mức Free `2.000` phút/tháng | tính từ N1, 6 lượt từ `10-09T04:55Z` | 11:0xZ 11-09 |

### THUẬT LẠI — số GitHub Actions, `run_id` là mỏ neo truy tìm

| # | khẳng định | giá trị |
|---|---|---|
| N12 | phân rã bước của run `34563553711` (windows, `cancelled`, `60,52` phút) | b14 `packet-loop` **7,13** · b15 `bien-nhan v2` **7,38** · b16 `test registry` **15,48** · b20 `lease-publish selftest` **26,25** `cancelled` |
| N13 | phân rã cùng bước của nền N2 (`34429604548`, `success`) | b14 **7,42** · b15 **6,27** · b16 **13,92** · b20 **2,97** |

### ƯỚC CÓ ĐIỀU KIỆN — không phải phép đo

Nếu bội số N3 (`2,9312`, đo trên Linux) cũng đúng trên `windows-latest` — **chưa ai đo** — thì bỏ
`t125` khỏi bước 20 đưa nó về `26,25 / 2,9312 ≈ **8,96** phút`, và job về
`60,52 − 26,25 + 8,96 ≈ **43,23** phút`.

**Đối chiếu độc lập làm ước này mạnh hơn, nhưng vẫn không biến nó thành phép đo:** `43,23` nằm gọn
trong dải **`40,20`–`53,53`** phút của **18** lượt `success` ở N1. Hai đường tính độc lập gặp nhau.

**Thứ ước này KHÔNG nói:** nó không nói job sẽ chạy trọn. Bội số trên Windows chưa đo (`chua_do_duoc`
#1), và N7 cho thấy hai nền **không** tỉ lệ với nhau ở phần việc mới.

### Thứ KHÔNG được suy ra, nói thẳng

**`t125` KHÔNG phải nguyên nhân của việc job bị cắt.** Nó có mặt trong **cả 18** lượt `success` của
N1, khi bước 20 tốn `2,45`–`3,88` phút. Nguyên nhân trực tiếp là **`#492` thêm `+1327` dòng test**
(N8) vào một suite mà `t125` nhân **2,93** lần (N3). `t125` là **hệ số khuếch đại**, không phải nguồn.

Hệ quả cho phạm vi: packet này cắt hệ số khuếch đại — việc ấy đủ để đưa job về dải đã đo (N2, ước ở
trên). Nó **không** chạm phần việc mới của `#492`, và **không** có cổng nào canh tốc độ tăng của
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
**và** đã có cross-review; không phóng lượt để "thử xem". Căn cứ đo được: N11 — **723,96** phút tính
tiền (**36,2 %** hạn mức tháng) đã bị đốt bởi 8 lượt `cancelled` **không thu được thông tin nào**.
Vi phạm ràng buộc này ⇒ ghi vào biên nhận, không tự bỏ qua.

---

**A1 (M1) — `t125` ra khỏi đường tới hạn, đo bằng TỈ LỆ thời lượng BƯỚC. Hai nền, hai vai.**

Ngưỡng `0,45` suy từ cấu trúc, không từ một con số phút: bỏ `t125` còn `1 / 2,9312 = 0,3412` (N3),
cộng biên ⇒ `0,45`. Đơn vị: **giây của BƯỚC**, đọc qua `list_workflow_jobs`.

- **(a) `ubuntu-latest` — VẾ BẮT BUỘC, và nó ĐO ĐƯỢC NGAY.** Bước `lease-publish selftest` trong job
  `gate` sau tách ≤ **`0,45 ×`** thời lượng của chính nó ở lượt nền cùng `event`, cùng nhánh.
  Mẫu số **tồn tại và ổn định**: `2,32`–`2,42` phút trên 5 lượt `push`/`master` liên tiếp sau `#492`
  (hiện vật N1). **Không có nhánh `KHÔNG ĐO ĐƯỢC` ở vế này** — mẫu số có sẵn, nên
  `KHÔNG ĐO ĐƯỢC` ở đây là **ĐỎ**.
  **Phép làm ĐỎ:** để `t125` lại trong job `gate` ⇒ tỉ lệ `≈ 1,00` ⇒ ĐỎ.
  **Đột biến bắt buộc:** cho job `gate-t125` chạy **nhưng không** cho job `gate` bỏ `t125` ⇒ A1(a)
  phải ĐỎ. Đột biến này phân biệt *đo VIỆC BỎ* với *đo SỰ TỒN TẠI của job mới*, và nó **chạy được**
  vì mẫu số ubuntu có sẵn.
- **(b) `windows-latest` — VẾ CÔNG BỐ, và nó quyết TRẠNG THÁI nghiệm thu.** Đọc và công bố: thời
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
- **(b) TRẠNG THÁI THẬT của branch protection — đọc được, nên là tiêu chí, không phải lời nhắc.**
  Đọc `GET /repos/{owner}/{repo}/rules/branches/master`, lấy mục `type == "required_status_checks"`,
  trường `parameters.required_status_checks[].context` ⇒ tập context đang được require.
  Đòi tập ấy **chứa** `gate (ubuntu-latest)` **và** `gate-t125 (ubuntu-latest)`.
  **Không đọc được (rc ≠ 200, thiếu trường, hoặc thiếu quyền) ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ.**
  **Phép làm ĐỎ:** chạy tiêu chí khi ruleset **chưa** được cập nhật ⇒ thiếu `gate-t125 (ubuntu-latest)`
  ⇒ ĐỎ. Đây là phép phân biệt mà bản trước **không có**: Issue trông y hệt nhau ở hai trạng thái
  đã-require và chưa-require, còn phép đọc này thì không.

**HAI LUẬT VỀ TÊN, cả hai đo được (N9), và sai luật nào cũng hỏng:**

1. **Require theo CONTEXT, không theo `job_id`.** Ruleset lưu tên **instance** `"<job_id> (<nền>)"`.
   Đo được: hôm nay require đúng **`gate (ubuntu-latest)`** — chuỗi có dấu ngoặc và tên nền.
   Require chuỗi `gate` trần thì **không khớp check nào** và cổng thành trang trí.
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
`gate-t125` gộp lại) phủ **đúng** tập ca như trước: `145 + 1 = 146` (mẫu số đúng lúc thi công).
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
