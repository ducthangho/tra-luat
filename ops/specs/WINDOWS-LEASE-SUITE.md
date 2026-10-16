# ĐẶC TẢ ĐÓNG BĂNG — `WINDOWS-LEASE-SUITE` — **BẢN 1 — ĐÃ CHỐT 11-09-2026** (Q1–Q3 tại #499 comment 5629586342)

| trường | giá trị |
|---|---|
| `packet_id` | `WINDOWS-LEASE-SUITE` |
| `packet_issue` | **#504** (mission #499; `depends_on: M9-FETCH-AUTH` #503) |
| `nguon_cap_viec` | **Packet khắc phục** của A0 (packet #488, PR #492, merge `0721811`). Nợ **#499 C3** (comment `5614089053`, 06:18:50Z 10-09-2026), chủ kho duyệt đề xuất số 2 trong phiên 11-09-2026. |
| `review_class` | **`sensitive`** — `ops/lease_publish_test.py` là gate test (PROTOCOL §8: gate lifecycle). Vế nghiêm ADR-0044: ≤3 tệp, ≤300 dòng thêm. |

**GIỚI HẠN LỜI KHAI:** chứng minh BYTE tới consumer adapter. **Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## VÌ SAO — phép đo, không phải lập luận

Bước 20 `lease-publish selftest` của `ci.yml` (`bash ops/chay_lease_publish_test.sh` → `python ops/lease_publish_test.py`):

| lượt `master` | head | ubuntu bước 20 | windows bước 20 | job windows |
|---|---|---|---|---|
| run `34429604548` (trước A0) | `28ba133` | **73 s** | **2 phút 58 s** | success, 40 phút 38 s |
| run `34439063235` (merge #492 = A0) | `0721811` | **2 phút 21 s** | **≥ 25 phút 50 s, chưa xong** | **cancelled** đúng phút 60 (`timeout-minutes: 60`) |
| run `34549206309` (merge #500) | `c00c88a0` | — (không đọc chi tiết) | — | **cancelled** 02:05:24Z (đọc `list_workflow_runs` 03:1xZ 11-09) |
| run `34552510232` (merge #501) | `27c413c3` | **2 phút 22 s** (02:26:46 → 02:29:08Z) | bắt đầu 02:42:53Z, **≥ 22 phút 52 s chưa xong** | **cancelled** 03:05:45Z — điểm dữ liệu thứ ba (thứ tư nếu tính #500) |

Log bước bị **đệm khối**: dòng cuối xả lúc 05:31:10Z (lượt `0721811`) rồi im tới lúc bị huỷ ⇒ **ca nào chậm/treo:
KHÔNG ĐO ĐƯỢC từ hiện vật CI** (đúng bài học "DÒNG IN CUỐI CÙNG ≠ CA CHẠY CUỐI CÙNG"). Lane PR chỉ chạy ubuntu nên
merge `0721811` là lần đo Windows ĐẦU TIÊN của A0. Gate `master` từ đó **vắng mặt** trên Windows — không đỏ.

**Đo tại chỗ (Linux, container này, cây `826bc36` = nội dung `ops/lease_publish*` trên `27c413c3`, `git diff` rỗng),
xong 02:58Z 11-09-2026, từng ca một bằng `time.monotonic()` quanh `fn()` — tệp
`scratchpad/thoi_gian_ca_linux.txt`, không nằm trong kho:**

```
TỔNG 136,9 s / 146 ca — 146 QUA, 0 ĐỎ, 0 BỎ QUA
 90,286 s  t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor     (66 % tổng)
 14,369 s  t139_A12_catalog_mutant_A0_giet_dung_ly_do_va_ghi_SONG_kem_seam
  4,957 s  t111_allowlist_worktree_nam_trang_thai_va_dot_bien
  3,584 s  t66_moi_guard_co_phan_chung_va_ve_theo_vi_tri
  2,470 s  t113_sau_dot_bien_upstream_va_phan_ky_deu_bi_giet
  1,938 s  t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat
  (140 ca còn lại: mỗi ca < 1,4 s)
```

**`t125` là ca A0** (docstring: chạy lại **TOÀN SUITE hai lượt** bằng `subprocess.run([sys.executable, __file__, CO_AB])`,
`capture_output=True`, **không `timeout=`**, khác nhau đúng một biến `GITHUB_ACTOR`; lượt con bỏ qua chính `t125`).
Nghĩa là thời gian của suite ≈ **3 × (thời gian của mọi ca trừ t125)**: Linux đo được 47 s × 3 ≈ 137 s — khớp.

**Giả thuyết H1 (CHƯA ĐO trên Windows):** nền Windows của A0 (t124–t151, trong đó `t139` nạp lại module 37 lần và mỗi
ca đích lại chạy nhiều `git` con — trên Windows mỗi tiến trình con tốn ~10–20× Linux) đã lớn hơn 3 phút đáng kể, và
`t125` nhân ba nó. Nếu nền Windows sau A0 là ~9 phút thì tổng ≈ 27 phút, đúng vùng "≥ 25 phút 50 s chưa xong". H1
giải thích **chậm**; nó chưa loại trừ **treo** (một `subprocess.run` không `timeout` trong lượt con). Bước 1 của packet
tồn tại để phân biệt hai ca ấy bằng phép đo, không bằng lập luận.

---

## `write_set` — HAI đường

```
ops/lease_publish_test.py        5394 dòng · 146 ca · ca cao nhất t151   (đo 03:04:52Z 11-09-2026, cây 27c413c3)
ops/chay_lease_publish_test.sh     49 dòng
```

**Đã đo ai giữ — 02:54:23Z 11-09-2026, bản sao sạch detach `27c413c3`, hai nguồn ref 324/324, `comm` 0/0:** cả hai
đường **NGƯỜI_GIỮ 0** (HẾT_HẠN: `slice-b-c-exec-1`, `plat-x5-exec-1r4` cho tệp test; `plat-x5-exec-1..1r3` cho wrapper).
Giao thoa với `M9-FETCH-AUTH` và `THU-HOI-LEASE-A1` (cùng tệp test) ⇒ cấp **sau** M9 land, **trước** A1.

## `ngoai_pham_vi`

- **`.github/workflows/ci.yml`** — KHÔNG đụng: không nâng `timeout-minutes` (đã nâng hai lần 25→45→60; lần ba là
  "lặp ba lần, hỏi lại cách làm" — PROTOCOL §12), không đổi ma trận, không thêm bước. Nhật ký ca đi thẳng ra stdout
  của bước (không cần artifact, không cần `if: always()` mới).
- **Bỏ qua / cách ly / quarantine bất kỳ ca nào** — cấm. Ca chậm là ca phải sửa, không phải ca phải tắt.
- **Đổi NGỮ NGHĨA của `t125`** (bỏ A/B toàn suite, thu hẹp tập ca so sánh) — không thuộc packet này nếu chủ kho không
  chọn ở Q2; `t125` là chốt chống rò `GITHUB_ACTOR` do cross-review #396 đòi.
- **`ops/lease_publish.py`** — không đụng.

---

## `muc_tieu` — hai bước, bước 2 phụ thuộc phép đo của bước 1

**M1** *(`ops/lease_publish_test.py`)* — `main()` in **một dòng trước** và **một dòng sau** mỗi ca, `flush=True`:

```
>>> vao  t125_AB_...   2026-09-11T03:10:00Z
<<< ra   t125_AB_...   90.286s QUA|DO|BO_QUA
```

Định dạng cố định, một dòng, tên ca là token thứ hai; dòng tổng kết `lease_publish: N/M đạt` và các dòng `  ĐỎ  …` /
`  BỎ QUA …` **giữ nguyên byte** (regex của `t125` và của `ci_dang_ky_test.py` đọc chúng). Lượt con của `t125` (có `CO_AB`)
in y hệt — đó chính là thứ cho phép định vị ca treo **bên trong** lượt con.

**M2** *(`ops/chay_lease_publish_test.sh`)* — `export PYTHONUNBUFFERED=1` trước `exec python …`, để stdout của bước
CI không còn đệm khối; ghi chú ngay tại dòng ấy vì sao (bài học "DÒNG IN CUỐI CÙNG ≠ CA CHẠY CUỐI CÙNG").

**M3** *(`ops/lease_publish_test.py`)* — ca **`t152_nhat_ky_tung_ca_vao_ra_cap_doi_va_khong_dem`**: chạy chính tệp này
trong tiến trình con với đúng một ca rẻ (đối số `--chi-ca t1…`, thêm nếu chưa có), stdout qua PIPE **không** đọc cho tới
khi tiến trình con kết thúc; khoá: mỗi `>>> vao X` có đúng một `<<< ra X` sau nó, và dòng tổng kết vẫn khớp regex của
`t125`. *Đột biến:* bỏ dòng `<<< ra` ⇒ ĐỎ; bỏ `flush=True` **không** làm ca này đỏ (đệm được xả khi tiến trình kết
thúc) — nên chốt "không đệm" đo ở **M4**, không đo ở đây; ghi thẳng điều đó trong docstring.

**M4** *(phép đo, không phải mã)* — chạy `ci.yml` bằng `workflow_dispatch` trên **ref của PR** (ma trận dispatch có
`windows-latest`; gắn nhãn `windows` KHÔNG tự sinh lượt chạy — `ci.yml` không khai `types: [labeled]`). Đọc log bước 20
của job Windows: hoặc suite XONG (ghi tổng thời gian và 5 ca chậm nhất), hoặc bị huỷ và **dòng `>>> vao` cuối cùng
không có `<<< ra`** nêu đúng ca treo/chậm. Kết quả ghi vào PR **trước** khi làm M5.

**M5** *(`ops/lease_publish_test.py`)* — sửa **đúng ca** M4 chỉ ra. Ba đường đã lường trước, chọn theo số đo:
(a) H1 đúng, `t125` chỉ chậm ⇒ chạy **hai lượt con song song** (`subprocess.Popen` ×2 rồi `communicate`) — giảm ~1/3
tổng thời gian mà không đổi ngữ nghĩa A/B; (b) một `subprocess.run` không `timeout` treo ⇒ thêm `timeout=` **có đơn vị
và có lý do** cho lời gọi ấy và sửa nguyên nhân treo (không phải chỉ thêm timeout); (c) `t139` là ca nặng nhất trên
Windows ⇒ giảm chi phí mỗi mutant (nạp module một lần cho mỗi mutant đã là tối thiểu; cắt số `git` con lặp lại trong
ca đích). Đường nào ngoài ba đường trên ⇒ Q3.

---

## `nghiem_thu`

**A1 (M1, M2, M3)** — `t152` XANH; `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh` ⇒ `147/147` trên Linux, delta so
`origin/master` = 0 ở mọi ca cũ; `python .claude/dev/ci_dang_ky_test.py` XANH (bộ này đọc `lease_publish_test.py` qua
`DA_NOI`, không regex — nhưng phải chạy để chứng minh, không suy).
*Phép đo làm nó ĐỎ:* bất kỳ ca cũ nào đổi màu; `t125` ĐỎ vì regex tổng kết hỏng.

**A2 (M4)** — có **một lượt `workflow_dispatch` trên head PR** với job `gate (windows-latest)`; ghi `run_id`, thời gian
bước 20, và (nếu bị huỷ) tên ca ở dòng `>>> vao` cuối. **Đây là phép đo duy nhất phân biệt "chậm" với "treo"**; thiếu
nó thì M5 là đoán.

**A3 (M5)** — sau vá, lượt `workflow_dispatch` thứ hai: bước 20 Windows **hoàn tất**, thời gian ≤ **15 phút** (Q1), và
ubuntu không chậm đi quá 10 % so với lượt A2. Cả hai lượt ghi vào PR kèm `run_id`.
*Phép đo làm nó ĐỎ:* Windows vẫn bị huỷ, hoặc > 15 phút.

**A4 — gate `master` sau land:** bước 20 Windows của lượt merge `success` — lần đầu kể từ `0721811`.

**A5** — `git diff --numstat`: ≤ 2 tệp, dòng thêm ≤ 300 (vế nghiêm). Bước 1 ước +40; bước 2 chưa ước được — vượt ⇒ DỪNG.

---

## `hinh_dang_ke_thua` (L4)

Chép từ spec cha r9 (biên nhận A0 không mang bộ đếm — cùng ghi nhận như `M9-FETCH-AUTH`):

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | 2 | r9 §1 |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2 |
| "hai cổng bất đồng" | 1 | #473 |
| "nguồn được tin mà chưa xác minh" | 6 | r9 lượt 1–6 |
| **"gate xanh ở lane PR, master đo lần đầu"** (Windows chỉ chạy ở master) | **1** (mới, #499 C3) | run `34439063235` |
| **"nâng trần thay vì chữa nguyên nhân"** (`timeout-minutes` 25→45→60) | **2** (đã có, `ci.yml` r391) | không được thành 3 ở packet này |

## `chua_do_duoc`

- **Ca nào chậm/treo trên Windows** — ba lượt master liên tiếp (`0721811`, `c00c88a0`, `27c413c3`) đều `cancelled`; lượt
  cuối đọc lại lúc 03:1xZ 11-09: kết thúc 03:05:45Z, bước 20 ≥ 22 phút 52 s. Vẫn không có tên ca — đó là việc của M4.
- **Nền Windows sau A0 là bao nhiêu phút** — chưa có số; H1 chỉ là suy từ Linux. A2 là phép đo.
- **Chi phí `workflow_dispatch` Windows** — mỗi lượt ~40 phút máy; packet cần ≥ 2 lượt (A2, A3).
- **Đo tại chỗ trên Linux dùng `time.monotonic()` quanh `fn()` trong cùng tiến trình** — con số của `t125` bao gồm hai
  tiến trình con, nên 90,286 s là thời gian tường; các ca khác không có nhiễu ấy.

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ BA (kể cả `ci.yml`) ⇒ DỪNG.
- **S2** dòng thêm > 300 ⇒ DỪNG.
- **S3** M4 chỉ ra ca treo nằm trong `ops/lease_publish.py` (không phải test) ⇒ DỪNG, revision mở write set qua chủ kho.
- **S4** muốn skip/cách ly/nâng timeout ⇒ DỪNG.
- **S5** `origin/master` chạm một trong hai đường; hoặc `M9-FETCH-AUTH` chưa land / `A1` đã cấp ⇒ DỪNG.
- **S6** trần HAI vòng review (ADR-0043).

## Câu hỏi biên giới — ĐÃ CHỐT (chủ kho: *"Bước 2: Trả lời luôn hộ tôi"* = lấy khuyến nghị; #499 comment 5629586342)

| câu | kết luận |
|---|---|
| Q1 | ngưỡng nghiệm thu bước 20 Windows: **≤ 15 phút** |
| Q2 | **(i)** giữ nguyên ngữ nghĩa A/B toàn suite của `t125`, chỉ song song hoá; (ii) chỉ khi (i) không đạt ngưỡng và có ca riêng chứng minh `t124`/`t139` không đọc actor |
| Q3 | ca treo trong `ops/lease_publish.py` ⇒ **DỪNG**, revision mở write set (S3) |

Nguyên văn ba câu hỏi giữ dưới đây làm hồ sơ:

❓ **Q1 — Ngưỡng nghiệm thu Windows cho bước 20.** Trước A0 là 2 phút 58 s. ➡️ **≤ 15 phút** (đủ chỗ cho ×3 của `t125`
trên nền Windows ~5 phút, và còn cách trần job 60 phút hơn 20 phút cho các bước sau — job Windows trước A0 mất 40 phút 38 s
tổng). Nếu chủ kho muốn về mức cũ (≤ 5 phút) thì gần như chắc phải đổi ngữ nghĩa `t125` — xem Q2.

❓ **Q2 — Có cho phép đổi ngữ nghĩa `t125` không.** Lựa chọn: (i) giữ nguyên A/B TOÀN suite, chỉ song song hoá (M5a);
(ii) lượt con bỏ các ca catalog đột biến (`t124`, `t139`) vì chúng không đọc `GITHUB_ACTOR` — nhưng docstring `t125` ghi
`t124` **từng** đổi tập đích khi rò actor, nên (ii) là nới chốt; ➡️ **(i)**; (ii) chỉ khi A3 không đạt ngưỡng Q1 với (i),
và khi ấy phải có ca riêng chứng minh `t124`/`t139` không đọc actor.

❓ **Q3 — Nếu M4 chỉ ra ca treo là ca A0 KHÁC `t125`/`t139`** (ví dụ `KhoObject` deadline trên Windows) ⇒ sửa ở test hay
mở `ops/lease_publish.py`? ➡️ DỪNG và mở revision với write set thêm `ops/lease_publish.py` (S3) — không sửa "quanh" ở test.
