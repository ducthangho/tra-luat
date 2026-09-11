# Đặc tả packet — T125-RA-JOB-RIENG (revision 1)

- `packet_id`: **T125-RA-JOB-RIENG**; ID bền theo `PROTOCOL §3.2` là `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp.)** `§3.2` đòi. Khuyến nghị: cùng mission với `#463`,
  vì hai packet là một chuỗi nối tiếp.
- `revision`: **1** · `generation`: 1 · soạn **09:4xZ 11-09-2026**. Mọi số kèm thời điểm đo (`L5`).
- `depends_on`: **`[wp503]`** — xem `write_set`.
- **Đi TRƯỚC `GATE-TACH-JOB-CAT-CHI-PHI`.** Không phải thứ tự tiện tay: xem `nguon_cap_viec`.

---

## `nguon_cap_viec`

Tách ra từ `GATE-TACH-JOB-CAT-CHI-PHI` **revision 6 → 7** (11-09-2026), sau khi chủ kho gỡ ràng
buộc *"gộp #463"*. Mục tiêu `M8`/`M9` và tiêu chí `A10`/`A11` của r5/r6 chuyển nguyên sang đây.

Lý do tách **không phải** "packet nhỏ dễ review hơn" — nó là **quan hệ phụ thuộc**:

`A1` và `A5` của `#463` đòi một **lượt nền hợp lệ**, tức job `gate (windows-latest)` **chạy trọn**.
Job ấy đang bị trần cắt, nên hai tiêu chí ấy **KHÔNG ĐO ĐƯỢC**, và `A2` mâu thuẫn với `A5` đúng vì
lý do đó (cross-review `#508` lượt 1, P1 `a2-doi-giu-ca-ket-luan-cua-nen-bi-cat`).
**Packet này làm job Windows chạy trọn trở lại ⇒ nền của `#463` đo được ⇒ `#463` nghiệm thu được.**

## Vấn đề — ba mức chứng cứ, khai riêng

**ĐO LẠI ĐƯỢC** (đọc từ cây kho, tái lập offline):

| # | khẳng định | giá trị | thời điểm đo |
|---|---|---|---|
| 1 | `t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor` chạy lại **toàn bộ** suite **hai** lượt trong tiến trình con | đọc mã | 06:0xZ 11-09 |
| 2 | `t125` chiếm bao nhiêu suite | **114,10 s / 173,6 s = 65,7 %** | 06:0xZ 11-09 |
| 3 | bội `TỔNG / B` — `d28c4b1` so `4b5184e` | **3,09** → **3,24** (ổn định) | 06:1xZ 11-09 |
| 4 | `B` (suite chế độ lượt con) — hai ref trên | **24,4 s** → **54,6 s** (+124 %) | 06:1xZ 11-09 |
| 5 | cờ `--ab-con-noi-bo` hiện có làm `t125` `return` mà **vẫn đếm ĐẠT** | đọc mã | 06:3xZ 11-09 |

**THUẬT LẠI** (số GitHub Actions; **không hiện vật nào trong kho**, `run_id` là mỏ neo truy tìm chứ
không thay hiện vật):

| # | khẳng định | giá trị |
|---|---|---|
| 6 | windows job run `34563553711`, bước 1–19 | **33,97** phút |
| 7 | cùng job, bước 20 `lease-publish selftest` | **≥ 26,25** phút, `cancelled` — **bị CẮT, giá trị thật CHƯA BIẾT** |
| 8 | ubuntu job run `34552510232`, bước 21–41 | **5,35** phút — windows **chưa ai đo gần đây** |

**SUY LUẬN CÓ ĐIỀU KIỆN** (đúng chỉ khi nhóm THUẬT LẠI đúng; **ƯỚC, không phải phép đo**):

Bỏ `t125` đưa bước 20 xuống `≈ 26,25 / 3,24 ≈ 8,1` phút. Job Windows khi ấy `≈ 51`–`56` phút tuỳ hệ
số của bước 21–41 (`1,73×` job trọn ÷ `2,35×` cận trên của `packet-loop`) ⇒ **chạy trọn**, biên còn
`3,74`–`8,68` phút.

**Biên ấy MỎNG và đang co.** `B` gấp `2,24` lần trong `4` ngày; nếu tốc độ ấy giữ, biên `5` phút hết
trong khoảng một tuần. Packet này **mua thời gian**, `#463` mới là thứ mua **biên bền** — nó đưa
`test registry` **`15,48`** phút và `packet-loop selftest` **`7,13`** phút khỏi đường tới hạn
(**cùng lượt `34563553711`** với mọi số THUẬT LẠI ở trên). **Đừng đọc packet này thành lời giải cuối.**

> **Bản nháp của chính hai con số này ghi `15,93` và `8,85` — số của lượt `34552510232`, một lượt
> KHÁC.** Ghép số của lượt này với ngữ cảnh của lượt kia đúng là bệnh **ghép sai lượt** mà
> `CLAUDE.md` đã tố cáo, và cross-review `#508` lượt 1 vừa bắt ở đặc tả `GATE` (`114,10/177,0`).
> Bắt được lần này vì đo lại **trước khi đóng băng** chứ không vì đọc kỹ. Ghi lại để mục
> `hinh_dang_ke_thua` có một số hạng thật, không phải một lời hứa.

## `review_class`

**`sensitive`** — chạm `.github/workflows/**` (`§8`: workflow/CI authority). Trần `ADR-0044`:
**≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **2 tệp**, còn **một chỗ trống** làm khoảng an toàn.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.github/workflows/ci.yml` | thêm job `gate-t125`; thêm cờ vào thân `run` của bước `lease-publish selftest` |
| 2 | `ops/lease_publish_test.py` | cờ mới phải được CHÍNH bộ test hiểu — `t125` là một ca trong tệp này, không có đường nào khác |

Không ký tự đại diện. Không đường dẫn nào khác.

**Đo `ai-dang-giu` 09:3xZ 11-09-2026** (sau canh hai nguồn trên KHO NGUỒN, `comm -23` RỖNG):

```
.github/workflows/ci.yml     rc=0   NGƯỜI_GIỮ 0: không có
ops/lease_publish_test.py    rc=11  NGƯỜI_GIỮ 1: m9-fetch-auth-exec-3-claude-20260911   (#503)
```

⇒ `depends_on: [wp503]`; lease cấp **SAU KHI `#503` land**, không phải sau khi hạn danh nghĩa trôi.

## `ngoai_pham_vi`

1. **KHÔNG tách `test registry` hay `packet-loop selftest`** — đó là `#463`. Packet này thêm **đúng
   một** job.
2. **KHÔNG nâng `timeout-minutes`.** `§12` coi việc nâng lần nữa là điều kiện DỪNG (đã nâng **2 lần,
   3 mức**: `25`→`45`→`60`).
3. **KHÔNG hạ răng `t125`, KHÔNG skip nó trên nền nào.** Nó bắt được một lỗi thật (`#396`: rò
   `GITHUB_ACTOR` làm **29** ca đỏ oan) và docstring của nó lập luận đúng vì sao một khẳng định rẻ
   hơn sẽ mù. Packet này đổi **CHỖ NÓ CHẠY**, không đổi **NÓ ĐO GÌ**.
4. **KHÔNG dùng lại cờ `--ab-con-noi-bo`.** Nó làm `t125` `return` **im lặng** và **vẫn đếm ĐẠT** —
   đúng bệnh *"ca có MẶT khác ca có ĐO"*. Phải là cờ **MỚI**, tên khác, ngữ nghĩa khác.
5. **KHÔNG đụng `.claude/dev/ci_dang_ky_test.py`** — của `#463` và ba packet mutant.
6. **KHÔNG đổi lệnh của bước nào khác**, không thêm bước nào ngoài bước `t125` của job mới.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `t125` ra khỏi đường tới hạn của job `gate`: chạy trong **job RIÊNG** `gate-t125`, song song, **cùng ma trận nền**, **cùng `timeout-minutes`**, **cùng `if` mức job**. | `write_set` #1 |
| M2 | Cơ chế bỏ `t125` khỏi lượt chính **FAIL-CLOSE**: thiếu job `gate-t125` ⇒ một cổng **ĐỎ**. | `write_set` #1 |
| M3 | Cờ mới khiến `t125` được đếm là **BỎ QUA CÓ LÝ DO**, **KHÔNG** phải ĐẠT — dòng tổng kết phải khai bỏ qua. | `write_set` #2 |
| M4 | **Độ phủ không đổi**, đo bằng phép chiếu tường minh: tập bước sau = tập bước trước **cộng đúng một phần tử** có tên trong danh sách cho phép. | `write_set` #1 |
| M5 | Branch protection require **cả bốn** job sau khi packet này land — nếu không, kết quả `t125` nằm ngoài hợp đồng bảo vệ nhánh. | `write_set` #1 (phần đo được) |

## `nghiem_thu`

**A1 (M1) — `t125` ra khỏi đường tới hạn, đo bằng THỜI LƯỢNG BƯỚC trên `windows-latest`.**
Bước `lease-publish selftest` trong job `gate` sau tách phải tốn **≤ 0,45 ×** thời lượng của chính
nó ở lượt nền cùng cách. `0,45` suy từ cấu trúc `TỔNG ≈ 3,24 × B` (bỏ `t125` còn `≈ 1/3,24 = 0,31`)
cộng biên — **không** suy từ một con số phút, vì số phút trôi theo tải.
Đơn vị: **giây của BƯỚC**, đọc qua `list_workflow_jobs`.
**Nền phải HỢP LỆ trước khi so** (xem A2 của `#463`, cùng luật): nếu lượt nền có job `cancelled`
hoặc thiếu job, khai **`KHÔNG ĐO ĐƯỢC`** ⇒ ĐỎ. **Ở packet này nền CÓ THỂ vẫn bị cắt** — chính đó là
vấn đề đang chữa. Khi ấy dùng **thời lượng bước** thay cho thời lượng job: bước 20 ở lượt nền có số
đo riêng dù job bị cắt sau đó, miễn bước ấy **đã hoàn tất**; bước nền **chưa hoàn tất** ⇒
`KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ, **không** được lấy giá trị bị cắt làm mẫu số.
**Phép làm ĐỎ:** để `t125` lại trong job `gate` ⇒ tỉ lệ `≈ 1,00` ⇒ ĐỎ.
**Đột biến bắt buộc:** cho job `gate-t125` chạy nhưng **không** cho job `gate` bỏ `t125` ⇒ A1 phải
ĐỎ. Thiếu đột biến ấy thì không biết A1 đang đo **VIỆC BỎ** hay chỉ đo **sự tồn tại của job mới**.

**A2 (M2) — FAIL-CLOSE, hai nửa, mỗi nửa một phản chứng riêng.**
1. **Thiếu job ⇒ ĐỎ.** Xoá job `gate-t125` khỏi `ci.yml` trong khi job `gate` vẫn mang cờ bỏ ⇒ phải
   có một cổng ĐỎ. **Phép làm ĐỎ:** không cổng nào đỏ ⇒ A2 ĐỎ. Đây là chốt chống đúng bệnh
   *"một job CI mặc định SKIP là một cổng KHÔNG TỒN TẠI"* mà kho đã trả giá.
2. **Job có mà KHÔNG chạy `t125` ⇒ ĐỎ.** Giữ job `gate-t125` nhưng đổi lệnh của nó thành một lệnh
   không chạy `t125` ⇒ phải ĐỎ. Nửa này tồn tại vì nửa (1) chỉ đo **SỰ CÓ MẶT** của job, và kho đã
   trả giá **bốn lần** cho việc đếm sự có mặt thay vì khả năng.

**A3 (M3) — cờ mới cho BỎ QUA CÓ LÝ DO, không cho ĐẠT.**
Chạy `ops/lease_publish_test.py` với cờ mới ⇒ dòng tổng kết phải khai **`145/146 · bỏ qua = 1`**
(hoặc mẫu số đúng lúc thi công), và `t125` phải xuất hiện ở danh sách **BỎ QUA** kèm lý do.
**Phép làm ĐỎ:** cờ làm `t125` `return` im lặng rồi được đếm ĐẠT (`146/146`) ⇒ A3 ĐỎ.
**Đối chứng bắt buộc với cờ CŨ:** chạy với `--ab-con-noi-bo` ⇒ nó **vẫn** cho `146/146` (hành vi
hiện tại, không đổi trong packet này) ⇒ chứng minh hai cờ có **ngữ nghĩa khác nhau**, và cờ mới
không phải tên khác của cờ cũ.

**A4 (M4) — độ phủ không đổi, đo bằng TẬP, với phép chiếu TƯỜNG MINH.**
Lấy `(tên bước, nền, conclusion)` của lượt TRƯỚC và lượt SAU. Đòi:
`tập_sau == tập_trước ∪ {bước t125 trong gate-t125}`, và tên bước mới phải nằm trong **danh sách cho
phép khai thẳng trong đặc tả này** — **một phần tử**, không phải một mẫu.
**Phép làm ĐỎ:** thêm bất kỳ bước nào **ngoài** danh sách ⇒ ĐỎ; đổi tên một bước cũ ⇒ ĐỎ; quên chép
`if` của một bước ⇒ bước đổi `skipped`↔`success` ⇒ tập lệch ⇒ ĐỎ.
**Nếu lượt nền KHÔNG hợp lệ** (job bị cắt) ⇒ hạ xuống so tập `(tên bước, nền)`, bỏ cột
`conclusion`, và đòi lượt SAU có **0** bước `cancelled`; trạng thái khi ấy là **`ĐẠT CÓ ĐIỀU KIỆN`**,
ghi thẳng vào biên nhận. **Không** được ghi ĐẠT trơn.

**A5 (M1) — job mới mang ĐÚNG cùng cấu hình, đo bằng GIÁ TRỊ ĐÃ PARSE.**
`yaml.safe_load(ci.yml)`; với `gate-t125` đòi bộ ba `(if mức job, chuỗi matrix.os sau chuẩn hoá
khoảng trắng, timeout-minutes)` **bằng** bộ ba của `gate`. Hôm nay `gate` = `(None, fromJSON(…), 60)`
(đo 07:0xZ 11-09-2026). **Thiếu khoá `timeout-minutes` ⇒ ĐỎ** — không phải chỉ "giá trị khác 60 ⇒
ĐỎ", vì một job thiếu hẳn khoá **không tạo ra giá trị khác**.
**Phép làm ĐỎ:** bỏ `timeout-minutes` khỏi `gate-t125` ⇒ ĐỎ. Chèn `if:` mức job (kể cả viết **không
có** dấu nội suy `${{ }}`) ⇒ ĐỎ.

**A6 (M5) — cổng không bị tháo, hai phần, phần hai KHÔNG đo được từ phiên.**
- (a) **đo được**: bản vá in ra tên job mới đúng dạng chuỗi branch protection dùng.
  **Phép làm ĐỎ:** tên trong `ci.yml` khác tên in ra ⇒ ĐỎ.
- (b) **không đo được từ phiên**: chủ kho phải require **cả bốn** job — `gate` · `gate-registry` ·
  `gate-packet-loop` · `gate-t125`. **Không có phép đo**; phải nằm trong thân Issue như một mục chủ
  kho làm **TRƯỚC** khi merge.
  **Nhắc:** `#463` cũng có nghĩa vụ ấy cho hai job của nó ⇒ chủ kho cập nhật branch protection
  **HAI lần**, mỗi packet một lần. Khai ở cả hai đặc tả để lần thứ hai không bị quên.

**A7 (toàn packet) — `ADR-0044`.** `git diff --numstat` ⇒ đúng **2** đường dẫn, dòng thêm ≤ `300`.
Vượt ⇒ **DỪNG và hỏi chủ kho**, không tự xin ngoại lệ.

**A8 (toàn packet) — suite không tụt.** `ops/lease_publish_test.py` chạy đủ (job `gate` + job
`gate-t125` gộp lại) phải phủ **đúng** tập ca như trước: `145 + 1 = 146` (mẫu số đúng lúc thi công).
Hai số phải **BẰNG NHAU**; không tin `rc=0` suông.

## `hinh_dang_ke_thua`

Chép từ `GATE-TACH-JOB-CAT-CHI-PHI` r7 và từ `CLAUDE.md`; mỗi dòng ghi nguồn trích (`L4`, `L5`).

| hình dạng | số lần đã gặp | trích lúc | ghi chú |
|---|---:|---|---|
| nâng `timeout-minutes` để mua cổng xanh | **2 lần nâng** (3 mức) | trích `#463` r4, đọc lại 09:4xZ 11-09-2026 | `§12` coi lần kế là điều kiện DỪNG ⇒ `ngoai_pham_vi` #2. |
| **một job CI mặc định SKIP là một cổng KHÔNG TỒN TẠI** | **≥ 3** | trích `CLAUDE.md` (dấu bỏ-qua-CI/PR #100 · job `cancelled` · `ops-don-ref.yml` 0 job) | Lý do A2 có **hai nửa**, không phải một. |
| đếm **SỰ CÓ MẶT** của một đường thay vì **KHẢ NĂNG** của nó | **4** | trích `CLAUDE.md` (`t103`, `gh-cli`, `rest-chung`, `shutil.which`) | Lý do A2 nửa (2) và A1 có đột biến riêng. |
| cờ làm một ca `return` im lặng rồi **vẫn đếm ĐẠT** | **1** | đo `--ab-con-noi-bo` 06:3xZ 11-09-2026 | Lý do `ngoai_pham_vi` #4 và A3 có đối chứng cờ cũ. |
| con số trong đặc tả **hết hạn** giữa lúc viết và lúc dùng | **8** | 4 của `#250` + 4 của `#463` r5, trích 09:4xZ 11-09-2026 | Lý do A1 neo **tỉ lệ**, không neo phút. |
| **GHÉP SAI LƯỢT** — tử số của lượt này, mẫu số/ngữ cảnh của lượt kia | **3** | `#463` r5 (`114,10/177,0`, cross-review `#508` lượt 1 bắt) · `r362` (thời lượng `1146s` gán nhầm lượt, trích `CLAUDE.md`) · **chính bản nháp này** (`15,93`/`8,85` của lượt `34552510232` đặt cạnh số của `34563553711`), đo 09:5xZ 11-09-2026 | Lần thứ ba, và lần này **tự bắt được bằng cách đo lại trước khi đóng băng** — không phải bằng đọc kỹ. Chốt rẻ duy nhất đã dùng được: **mỗi con số THUẬT LẠI phải đi kèm `run_id`**, và một đoạn văn chỉ được dùng số của **MỘT** lượt. |

## `chua_do_duoc`

1. **Thời lượng THẬT của bước 20 trên Windows: KHÔNG BIẾT.** Nó bị trần cắt ở `26,25` phút. Mọi con
   số "sau khi bỏ `t125`" trong đặc tả này là **ƯỚC từ cận dưới**, không phải phép đo. Chính packet
   này là thứ làm nó đo được — tức **packet là điều kiện để đo nền của chính nó**. Vòng ấy khai
   thẳng, không giấu: A1 vì vậy so **thời lượng BƯỚC** (đo được cả khi job bị cắt) chứ không so
   thời lượng JOB.
2. **Bước 21–41 trên Windows chưa ai đo gần đây.** Hệ số `1,73×`–`2,35×` là mượn từ bước khác. Nếu
   hệ số thật cao hơn `2,35×`, job vẫn có thể chạm trần **sau khi** packet này land — đó là **KẾT
   QUẢ ĐO**, không phải thất bại: báo chủ kho, đừng nới gì.
3. **Số benchmark không có hiện vật.** `B`, `TỔNG`, `114,10` s chỉ có trong văn xuôi; kho không có
   lệnh benchmark đầy đủ, rig, `rc`, hay mốc từng lượt (cross-review `#508` lượt 1, P2
   `benchmark-moi-thieu-hien-vat-neo-luot`). Phiên thi công phải **bàn giao hiện vật cùng với số**,
   hoặc khai `KHÔNG ĐO ĐƯỢC`.
4. **Biên sau packet này MỎNG.** `3,74`–`8,68` phút ước được, trong khi `B` gấp `2,24` lần trong `4`
   ngày. Packet này **không** đóng được nợ ngân sách CI; `#463` mới làm việc đó. Không ai đang canh
   tốc độ tăng ấy — nợ, chưa có tên, ngoài phạm vi.
