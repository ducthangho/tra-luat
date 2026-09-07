**Tiêu đề:** `MUTANT-WINDOWS-SUBAGENT-GHI-DETECT — chép hình dạng "cắt đột biến khỏi Windows" của #456`

> **CHƯA ĐỦ ĐIỀU KIỆN BẮT TAY.** Đặc tả đã đóng băng để chủ kho quyết định.
> **Phụ thuộc:** `GATE-TACH-JOB-CAT-CHI-PHI` → `LO-319-LINUX-BANG-CHUNG-XANH` → packet này.

## Vấn đề đo được

`.claude/dev/subagent_ghi_detect_test.py` chạy **88 s** đủ, **3 s** khi chỉ chạy nền
(`NHANH_DON_DUOC_KHONG_DOT_BIEN=1`-tương đương) ⇒ **96,6 %** thời lượng là vòng đột biến. Bộ này có
**ba kênh đột biến** (22 + 6 + 1) — nhiều hơn `pretooluse` một bậc, vốn chỉ có một.

#456 đã chứng minh hình dạng bản vá: **cắt vòng đột biến khỏi chân Windows, giữ bằng chứng dương theo
nền**. Đo được trên #456: bước `test registry` Windows **44,3 → 17,70** phút.

**Điểm quan sát không đổi:** lượt chạy đủ và lượt chỉ-nền in **CÙNG MỘT BYTE** tại chỗ sổ đăng ký
đọc (`8/8`, `rc=0`) — nên bản vá **không** làm sổ đăng ký thấy khác đi.

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

**Đặc tả đóng băng:** `ops/specs/MUTANT-WINDOWS-SUBAGENT-GHI-DETECT.md` @ `b743f1798aba12615f903a11bd451c87e404814e`
**`spec_sha256`:** `2abace8588ec2b4e0626c1c77e9c3e0f7e713ecb2ce528b149e6c7f1f0000759`
**`base_sha`:** `1b3caa1` · **`depends_on`:** `LO-319-LINUX-BANG-CHUNG-XANH`
**Write set — đo 03:15Z 07-09-2026:** `ai-dang-giu .claude/dev/subagent_ghi_detect_test.py` ⇒
**`NGƯỜI_GIỮ 0`** (canh hai nguồn ref: máy chủ 299 / cục bộ 299, `comm -23` rỗng ⇒ không mù).
**Lease nháp:** `ops/leases/mutant-windows-subagent-ghi-detect-exec-1-claude-20260906.yaml.nhap` (6 ô null)
