**Tiêu đề:** `MUTANT-WINDOWS-NHANH-DON-DUOC — chép hình dạng "cắt đột biến khỏi Windows" của #456`

> **CHƯA ĐỦ ĐIỀU KIỆN BẮT TAY.** Đặc tả đã đóng băng để chủ kho quyết định.
> **Phụ thuộc:** `GATE` → `LO-319` → `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT` → packet này.

## Vấn đề đo được

`ops/nhanh_don_duoc_test.py` chạy **33 s** đủ, **2 s** chỉ-nền ⇒ **93,9 %** thời lượng là vòng đột
biến. Bộ này còn spawn `git archive` + `tar` cho **mỗi** đột biến.

**Điểm quan sát không đổi:** lượt đủ và lượt `NHANH_DON_DUOC_KHONG_DOT_BIEN=1` in **CÙNG MỘT BYTE**
tại chỗ sổ đăng ký đọc (`8/8`, `rc=0`).

**Chưa đo được, riêng của bộ này:** hành vi ống (`Popen ... | tar -x`) trên `windows-latest` **chưa
từng được đo riêng** — nó luôn nằm trong con số gộp của `test registry`. `tar` **có** trên
`windows-latest`, nhưng "có mặt" không phải "hành xử như nhau". Nếu chi phí Windows của bộ này thấp
hơn ước, khoản tiết kiệm nhỏ hơn ước, và `A7` sẽ nói ra.

## Vì sao tách làm HAI packet, không gộp

`ADR-0044`: packet `sensitive` ≤ **3 tệp** và ≤ **300 dòng thêm**. Tiền lệ đo được: **PLAT-M4** (2 tệp)
⇒ 1 vòng review, 1 finding; **PLAT-X4** (4 tệp) ⇒ 3 vòng, 8 finding. Gộp hai bộ vào một packet là mua
thêm hai vòng review.

## Hệ số nền `~3×` là NỘI SUY, và nay đo được là SAI theo cả hai chiều

Ước tiết kiệm của packet này dựa vào giả định *"Windows đắt gấp ~3"*. Đo 02:49Z 07-09-2026 trên **11**
lượt master, tỉ lệ `giây Windows / giây ubuntu` **cùng bước, cùng head**: `test registry` **1,20×** ·
`packet-loop selftest` **2,35×** · `lease-publish selftest` **2,94×** · `bien-nhan v2 selftest`
**7,56×** · **job trọn `1,73×`**. Dải toàn bộ `1,07×` – `9,74×`. Bảng đủ, kèm **dải làm tròn**, ở
`ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md` mục *"Hệ số nền KHÔNG phải một con số"*.

⇒ `~3` **quá CAO** cho job trọn, **quá THẤP hơn hai lần** cho một selftest python nặng. Nhân bằng một
hệ số duy nhất là sai bất kể chọn số nào.

**Nợ VẪN MỞ, nói thẳng:** không bước nào đo được là một **vòng đột biến** — thứ packet này thật sự cần
nhân. Bảng trên là **PROXY gần nhất**, không phải phép đo thay. `A7` là phép đo duy nhất trả lời cho
bộ này, và nếu `A7` ĐỎ thì đó là **kết quả đo**, không phải thất bại.
Nợ có tên **`CHUA-CO-PHAN-RA-THOI-GIAN-THEO-BO-TREN-WINDOWS`**.

## Chưa có `cross_approved`

Lượt cross-review thứ 5 **chết năm lần** vì hạ tầng: proxy egress của container remote **không cho
`WebSocket upgrades`** (khai thẳng trong tài liệu proxy), mà đó là đường tái kết nối của `codex`.
`assurance` của cả bốn packet vẫn dừng ở **lượt 4**. Biên bản:
`ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md`.

---

**Đặc tả đóng băng:** `ops/specs/MUTANT-WINDOWS-NHANH-DON-DUOC.md` @ `b743f1798aba12615f903a11bd451c87e404814e`
**`spec_sha256`:** `417dce16227687cbb1e642284f39d2f847a617b2d730f7f52aaa58f33c936521`
**`base_sha`:** `1b3caa1` · **`depends_on`:** `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT`
**Write set — đo 03:15Z 07-09-2026:** `ai-dang-giu ops/nhanh_don_duoc_test.py` ⇒ **`NGƯỜI_GIỮ 0`**
(canh hai nguồn ref: máy chủ 299 / cục bộ 299, `comm -23` rỗng ⇒ không mù).
**Lease nháp:** `ops/leases/mutant-windows-nhanh-don-duoc-exec-1-claude-20260906.yaml.nhap` (6 ô null)
