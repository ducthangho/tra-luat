# VERDICT — `DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP` (#543) r1/g1, lượt 3

| trường | giá trị |
|---|---|
| `reviewed_sha` | `6eb7175c47796fe87528f4a5ddf8541af51c0201` |
| `base` | `dd274415408bd1c6b4279c8e2cf9671057520f23` |
| lượt trước | `fe9047e`, `changes_requested`, 0 P1 / 1 P2 / 1 P3 |
| **kết luận** | **`approve`** — 0 P1, 0 P2, 0 P3 mở |
| ngày | 2026-09-16 |

---

## ĐỌC ĐIỀU NÀY TRƯỚC — `approve` này có một giới hạn CẤU TRÚC

`approve` ở đây nói: **mọi lớp đã nêu đều đóng, và không tìm thêm được lớp nào.** Nó KHÔNG nói
"đã được xác nhận độc lập", vì hai trong sáu lớp được đóng bằng **bản vá của chính reviewer**:

- `packet_loop.py` của agy lệch bản HINT của tôi đúng **10 dòng** ở lượt 2 (nay **11**, sau một
  dòng sửa số), và thông điệp fail-close là **nguyên văn câu tôi viết**.
- Bộ dò bốn cửa fail-open cũng do tôi viết.

Nên với **LỚP 1** và **LỚP 2**: kết quả đo đúng, nhưng **vòng tròn** — người viết bản vá và người
viết phép thử là một. Muốn đóng thật phải có một lượt của **provider KHÁC**, hoặc một người khác
dựng lại bộ dò từ đầu.

**Bốn lớp còn lại — 3, 4, 5, 6 — là phán đoán độc lập thật**, vì agy tự làm và tôi đo lại bằng
đường riêng. Ba lượt cộng lại, agy vá đúng **4/4** thứ thuộc phần mình.

---

## Đối chiếu ba lượt

| lớp | lượt 1 | lượt 2 | lượt 3 | ai vá |
|---|---|---|---|---|
| **1** FAIL-OPEN nguồn đối chiếu (P1) | 4 cửa `rc=0` | ĐÃ VÁ | giữ nguyên | **reviewer** ⚠ |
| **2** đọc ra ngoài `--root` (P1) | fallback đỡ cho 2 ca test | ĐÃ VÁ | giữ nguyên | **reviewer** ⚠ |
| **3** ca có mặt khác ca có đo (P2) | `chep_12` xanh khi tắt n-gram | ĐÃ VÁ THẬT | **răng còn nguyên** | agy |
| **4** hằng không căn cứ (P3) | ngưỡng 15 không giải thích | vá có số, **1 số hạng trôi** | **ĐÃ ĐÓNG — 6/6 khớp** | agy |
| **5** định danh phantom (P3) | cả hai không tra được | ĐÃ VÁ THẬT | **vẫn đúng trên head mới** | agy |
| **6** ghi ngoài write set (P2) | — | **MỚI** | **ĐÃ ĐÓNG** | agy |

### LỚP 4 — đóng, sáu ngưỡng khớp hết

agy sửa `10` → `11`. Diff trên `packet_loop.py` giữa lượt 2 và 3 **đúng một dòng**, và đúng dòng ấy:

```
-  # Đo trên master: ngưỡng 10 có 10 hits, 11 có 7 hits, 12 có 4 hits,
+  # Đo trên master: ngưỡng 10 có 11 hits, 11 có 7 hits, 12 có 4 hits,
```

Đo lại độc lập trên head lượt 3, nạp `_phang_ca_tep` **từ chính mã sản phẩm**:

| ngưỡng | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---:|---:|---:|---:|---:|---:|
| agy khai | 11 | 7 | 4 | 2 | 0 | 0 |
| đo lại | **11** | **7** | **4** | **2** | **0** | **0** |

**6/6 khớp.** Lượt 2 lệch đúng một số hạng ở đầu dãy; nay hết.

### LỚP 6 — đóng, write set sạch

agy chọn lối ra thứ hai: **dời handoff về** `ops/reviews/doctrine-scan/`. Delta thật sau khi hoà
master (`5097480..6eb7175`) nay **ba đường, tất cả trong write set**:

| đường | numstat | trong write set? |
|---|---|---|
| `.claude/dev/packet_loop.py` | +46 / −10 | ✅ |
| `.claude/dev/packet_loop_test.py` | +90 / −8 | ✅ |
| `ops/reviews/doctrine-scan/handoff-…md` | +43 / −34 | ✅ |

Không còn tệp nào ngoài phạm vi. §5 thoả.

> Nhắc lại phần trách nhiệm của reviewer: LỚP 6 sinh ra vì verdict lượt 1 nói hiện vật nên ở tầng
> đầu mà **quên nói "đừng tự dời"**. Việc dời về đây là đúng theo lease; câu A6 của spec vẫn cần
> sửa, nhưng bằng **revision**, không bằng executor tự đi.

### LỚP 5 — vẫn đúng trên head mới

Handoff đổi nên định danh cũng đổi; đo lại:

| khai | tra được? |
|---|---|
| `head_sha: 020b0b0ada848929451e4613451dde8aabcfe107` | **CÓ** (commit) |
| `tree_oid: 8b3753f0b14eea930a8c2c1bf4e713eb2246b761` | **CÓ** (tree), **khớp** `020b0b0^{tree}` |
| `020b0b0` là tổ tiên của head `6eb7175`? | **CÓ** |

Như lượt 2: `head_sha` khai commit **sản phẩm** chứ không phải đầu nhánh, vì đầu nhánh chính là
commit ghi handoff — cách khai trung thực nhất có thể.

### LỚP 3 — răng còn nguyên sau hai lượt sửa

Đột biến tắt trọn cơ chế n-gram (`if True:` → `if False:`), chạy trên head lượt 3:

| ca | kết quả |
|---|---|
| `doctrine_scan_chep_tron_5_1_bi_chan` | **ĐỎ** |
| `doctrine_scan_chep_doan_ngan_5_1_bi_chan` | **ĐỎ** |
| `doctrine_scan_chep_12_bi_chan` | **ĐỎ** |

Cả ba ca dương đều có răng. *(Hai ca đỏ khác — `moc_dot_bien_phai_khop_DUNG_MOT_CHO` và
`đột biến bo_kiem_chep_protocol` — là tạo tác của chính đột biến tôi dựng, không tính.)*

### LỚP 1 và LỚP 2 — không hồi quy

Bốn cửa fail-open, đo lại trên head lượt 3: cửa 2, 3, 4 đều **`rc=2` + `KHÔNG ĐO ĐƯỢC`**, không
traceback; đối chứng protocol thật **`rc=6`**. Cửa 1 đã đo riêng ở lượt 2 (`rc=2`, `KHÔNG ĐO ĐƯỢC`)
và diff lượt 3 trên `packet_loop.py` **chỉ có một dòng chú thích**, nên nó không đổi.

---

## Cổng trên `6eb7175` — `rc` đọc trực tiếp

| cổng | rc | bằng chứng dương |
|---|---:|---|
| `packet_loop.py doctrine-scan` | 0 | sạch |
| `packet_loop.py adr-song` | 0 | — |
| `packet_loop_test.py` | 0 | **291/291**, hai số bằng nhau |
| `ops/lease_publish_test.py` | 0 | **155/155** |
| `ops/bien_nhan_v2.py` | 0 | — |
| `tl doc-claims-check --strict` | 0 | `core.abbrev=7` |
| `tl release-verify --strict` | 0 | `ok=true`, `expected == checked == 180` |
| `git diff --check` | 0 | — |

**Delta so nền**, cùng rig clone: `dd27441` **282/282** → `6eb7175` **291/291** = **+9 ca, 0 hồi quy**.

---

## Phạm vi của `approve` này

**Nó là điều kiện DỪNG của vòng vá→review, KHÔNG phải merge authorization.** Land cần chỉ thị của
chủ kho.

**Nó KHÔNG thoả A6 của spec.** A6 đòi *"cross-review khác nền (reviewer `claude`)"* với mức
assurance tương ứng; lượt này khai **`advisory_review`** vì không có `session_run_id`, và vì vòng
tròn nói ở đầu. §8:668 cho `sensitive` đòi Codex `cross_approved` hoặc `human_audited`.

**Ba việc còn mở, không việc nào của agy:**

1. **Vòng tròn LỚP 1/LỚP 2** — cần một lượt của provider khác.
2. **A6 của spec** đòi verdict vào `ops/reviews/doctrine-scan/` (thư mục con) — đúng caveat
   `HIEN-VAT-TRONG-THU-MUC-CON-NAM-NGOAI-TAM-BA-CONG` vừa đóng ở `r374`. Cần **revision 2** sửa câu ấy.
3. **`human_audited`** — quyết định của chủ kho, đã chọn từ 16-09 nhưng chưa thực hiện.

## Chưa đo được

| thứ | vì sao |
|---|---|
| LỚP 1/LỚP 2 có thật sự đóng không | reviewer tự chấm bản vá của mình — xem đầu verdict |
| mức assurance | không phóng được reviewer độc lập: `codex` kiểm sống HỎNG `rc=1` + hết quota; `claude` **CHƯA_XÁC_THỰC**; `doctor --kiem-song` `rc=12` |
| CI trên `6eb7175` | chưa có lượt nào; nhánh chưa mở PR |
| có lớp thứ bảy không | ba lượt tìm được sáu lớp. Đó là tập **ĐÃ DUYỆT**, không phải tập **TỒN TẠI** |

Nguồn có thẩm quyền là **tệp có băm** này. Comment GitHub chỉ là bản chiếu.
