# Verdict lượt 3 — Packet #551 `ASSURANCE-NEO-VAO-HO-MODEL` (r3/g3)

- **Kết luận:** `changes_requested` — **0 P1 · 1 P2 · 2 P3**. Hai lớp của lượt 2 **ĐÓNG THẬT**
- **Neo `reviewed_sha`:** `6bcf26637ca94fd29039665e34b3f07732b57490`
- **PR:** [#557](https://github.com/ducthangho/tra-luat/pull/557) · nhánh `claude/assurance-ho-model-r2-g2`
- **Lease:** `assurance-ho-model-r3-g3-antigravity` · executor `agy` · reviewer `claude`
- **Thời điểm đo:** `2026-09-18T15:39Z` (phép đo chạy `15:28Z`–`15:39Z`)

## 0. Giới hạn của lượt này

Bản vá do `agy` viết ⇒ phần đối chiếu **triển khai** độc lập thật. Nhưng phiên này soạn cả ba đặc
tả và ghi cả ba lease, nên phần đối chiếu **tiêu chí** vẫn là tự chấm bài mình ra đề — và `S1`/`S2`
của lượt 2 (lỗi của chính đặc tả) **vẫn mở**. Mức cao nhất lượt này mua được: **`advisory_review`**.

## 1. Hai lớp của lượt 2 — ĐÓNG THẬT, đo hai đường độc lập

Rig: probe gọi thẳng `_thieu()`, **KHÔNG lọc thông điệp**, trừ tập lỗi NỀN. Bài học lượt 2: bộ lọc
theo cụm từ đã **mù** với nhánh `khong_do_duoc` và suýt sinh một P1 oan cho executor.

Ca đối chứng: `claude review codex` ⇒ **QUA**; `claude review claude` ⇒ **CHẶN**. Rig sống.

### `P1-MỚI` (bất đối xứng bằng chứng) — ĐÓNG

| ca | kết quả |
|---|---|
| reviewer khai đè model, thiếu bằng chứng | **CHẶN** — *"khai đè model **reviewer** …"* |
| executor khai đè model, thiếu bằng chứng | **CHẶN** — *"khai đè model **executor** …"* |
| `agy` khai `executor_model: gemini-3`, không bằng chứng | **CHẶN** |
| executor `do_may` **thiếu** `model_evidence_ref` | **CHẶN** |
| executor `do_may` **có** `model_evidence_ref` | **QUA** (đối chứng) |
| executor mức **bịa đặt** | **CHẶN** |

Thông điệp nay **ghi rõ vai** (`reviewer` / `executor`) — đúng thứ cần để người đọc biết bên nào
thiếu. Vòng lặp hai vai thay cho hai khối chép đôi: một chốt, hai vai, không còn cửa nào lệch.

### `P2-MỚI` (`HO_MODEL_CHO_PHEP` là hằng số chết) — ĐÓNG

Đột biến **từng phần tử**, không chỉ xoá sạch bảng:

```
bỏ claude  khỏi bảng -> 'claude' ⇒ ''      CÓ ĐIỀU KHIỂN
bỏ gpt     khỏi bảng -> 'gpt'    ⇒ ''      CÓ ĐIỀU KHIỂN
bỏ gemini  khỏi bảng -> 'gemini' ⇒ ''      CÓ ĐIỀU KHIỂN
```

Ở lượt 2, xoá **sạch** bảng mà hành vi **không đổi**. Nay từng họ một đều điều khiển được. Bảng
CHO PHÉP nay là bảng cho phép thật, không phải trang trí.

## 2. Bảng đo — kê CẢ cái khớp

Hai vế dựng trong **MỘT** lệnh, `rc` đọc TRỰC TIẾP.

| cổng | nền `eb15657` | ứng viên `6bcf2663` | delta |
|---|---|---|---|
| `ops/bien_nhan_v2.py` | rc=0 · `125 ĐẠT v2 · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 178` | rc=0 · **cùng số từng chữ** | **0** |
| `ops/bien_nhan_v2_test.py` | rc=0 · `48/48 ca · 63/63 CÓ RĂNG` | rc=0 · `61/61 ca · 73/73 CÓ RĂNG` | +13 ca, +10 đột biến |
| `doctrine-scan` · `doc-claims-check --strict` · `git diff --check` · `release-verify --strict` | rc=0 | rc=0 | 0 |
| `adr-song` | rc=0 · 49/49 | rc=0 · **50/50** khớp 1–1 | +1 |

`A3` **ĐẠT**: số `ĐẠT v2` và `tổng` **không đổi** giữa hai vế ⇒ luật mới không từ chối biên nhận
cũ nào. `A9`: **6 tệp, +223 / −18** — dưới trần 250.

**`M14` đạt mức chặt nhất, lần thứ hai liên tiếp.** Mười đột biến `m62`–`m71`, mỗi cái giết một ca
**KHÁC NHAU**, **tất cả `giet_that`**, không cái nào `tin_dung_gia`. Hai chốt mới của lượt này có
đột biến riêng: `m70 → c59` (khai đè executor thiếu evidence) và `m71 → c61` (xoá `gemini` khỏi
`HO_MODEL_CHO_PHEP`). Không có bộ tương đương.

## 3. Phát hiện

### P2 — Khối `model_executor_identity` **không dùng được theo cách viết tự nhiên**

Refactor gộp hai hàm thành `_giai_ho_va_bc(d, vai)` và mở thêm khối `model_executor_identity`. Nhưng
`pre = f"{vai}_" if vai == "executor" else ""` được áp cho khoá tra **trong CẢ** `sub` lẫn `d`. Hệ
quả đo được:

| viết thế nào | `ho_exec` | kết quả |
|---|---|---|
| `model_executor_identity: {model: gpt-5}` — **song song với khối reviewer** | `<RỖNG>` | **CHẶN** *"không xác định được họ model của executor"* |
| `model_executor_identity: {executor_model: gpt-5}` — **nhân đôi tiền tố** | `gpt` | nhận diện được |
| `model_executor_identity: {provider: openai_codex}` | `gpt` | **QUA** (đối chứng) |

`model_reviewer_identity: {model: …}` **hoạt động** (vì `pre=""`), còn
`model_executor_identity: {model: …}` **không**. Bên trong một khối đã tên là
`model_executor_identity`, đòi khoá phải lại mang tiền tố `executor_` là **dư thừa và bất đối xứng**
với khối kia.

**Vì sao P2 chứ không phải nit:** đây đúng là trường mà `M16` của lease đặt toàn bộ tính chính đáng
của `cross_approved` lên. `agy` viết theo trực giác (song song với khối reviewer) sẽ **trượt**, và
thông điệp lỗi *"không xác định được họ model của executor"* **không hé** rằng vấn đề là **tên
khoá** — nó đọc như "bạn chưa khai", trong khi người ta **đã khai**. Fail-closed nên không nguy
hiểm, nhưng nó dẫn người dùng đi sai hướng ở đúng chỗ quan trọng nhất.

**Đề xuất:** trong `sub`, tra khoá **không tiền tố** cho cả hai vai (`model_family` · `ho_model` ·
`canonical_model` · `model`), giữ tiền tố **chỉ** khi tra ở mức top-level `d`. Kèm một ca
`model_executor_identity: {model: …}` phải QUA, và một đột biến gỡ chốt ấy phải làm ca đó ĐỎ.

### P3-1 — Một người audit thoả cho **cả hai** vai, không khai ra

```
executor khai_co_audit + `nguoi_audit` chỉ ở TOP-LEVEL      -> QUA
executor khai_co_audit + `executor_nguoi_audit` riêng       -> QUA
executor khai_co_audit + KHÔNG có người audit nào           -> CHẶN   (đối chứng)
```

Danh sách khoá của vai `executor` **cố ý** gồm cả `nguoi_audit` / `audit_actor` **không tiền tố**,
nên một trường audit duy nhất bảo chứng cho model của **cả hai** bên. Có lẽ là **chủ ý** — một
biên nhận, một người audit. Nhưng biên nhận khi ấy **không phân biệt được** *"đã audit cả hai
model"* với *"đã audit một model"*, trong khi `cross_approved` sống hay chết ở chỗ hai bên có ĐỘC
LẬP không.

**Đề xuất:** giữ nguyên hành vi nhưng **khai thẳng** trong ADR-0050 rằng một người audit có thể
bảo chứng cả hai vai; hoặc đòi khoá riêng cho vai executor. Chọn đường nào cũng được — điều không
nên là để nó **im lặng**.

### P3-2 — Khoá `model:` ở **top-level** nay tính là "khai đè" của reviewer

Trước `6bcf2663`, override của reviewer **chỉ** đọc trong `model_reviewer_identity`. Nay
`_giai_ho_va_bc(d, "reviewer")` với `pre=""` tra **cả** `d`, nên một khoá top-level `model:` hoặc
`ho_model:` biến biên nhận thành "có khai đè" ⇒ **đòi `model_evidence`**. Đo:

```
thêm khoá top-level `model`     -> CHẶN  "khai đè model reviewer … thiếu mức bằng chứng"
thêm khoá top-level `ho_model`  -> CHẶN
```

Đo trên dữ liệu thật: **0/50** biên nhận `cross_approved` hiện có khoá ấy ⇒ **chưa phải hồi quy**,
và `A3` vẫn đạt. Nhưng `model:` ở top-level là thứ người ta **viết rất tự nhiên**, và luật mới sẽ
bắt họ mà không có gì báo trước. Đây là **nới phạm vi chưa khai**, không phải lỗi hôm nay.

**Đề xuất:** khai trong ADR-0050 rằng khoá top-level cũng tính là khai đè, hoặc bỏ `d` khỏi phạm
vi tra của vai reviewer.

## 4. Hai khuyết tật của ĐẶC TẢ vẫn MỞ — và chúng KHÔNG phải việc của agy

`S1` và `S2` của verdict lượt 2 (`sha256 306ae5d9…`) **chưa được xử**, và không được giao cho agy:

- **`S1`** — `M16` đòi `executor_model` từ *"biên nhận của executor"*, mà kho **chưa từng có** biên
  nhận executor (177 biên nhận đều là `review_delivery_receipt` hoặc không khai kind) và
  `ops/reviews/**` **không** nằm trong write set.
- **`S2`** — `A14` (RỖNG ⇒ CHẶN) và `A3` (delta 0) **loại trừ nhau**: **50/50** biên nhận
  `cross_approved` có mức bằng chứng RỖNG.

Chừng nào hai mục này chưa được chủ kho quyết (revision 4, hay một miễn trừ có tên), packet
**không đạt được `assurance_target: cross_approved`** dù bản vá có sạch đến đâu.

## 5. Chưa đo được

- **`gate (windows-latest)`** — `manual_ci_budget: 0`. **KHÔNG DÙNG PHƯƠNG TIỆN**.
- **Họ model thật của `agy`** ở lượt chạy sinh ra `6bcf2663` — không có bằng chứng máy. `S1` giải
  thích vì sao cơ chế định đóng nó vẫn chưa thi hành được.
- **Lượt CI tự động trên `6bcf2663`** — chưa đọc lúc viết; verdict neo vào **cây**, không neo vào CI.

---

**Nguồn có thẩm quyền là tệp có băm trong kho; mọi bản đăng lên GitHub chỉ là bản chiếu.**
