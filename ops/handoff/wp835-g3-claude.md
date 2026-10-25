# Handoff wp835 g3 — ADR-0056 ngưỡng thu hồi lease 6 giờ (executor `wp835-r3-g3-claude`)

Packet #835 · revision 3 · generation 3 · `review_class: sensitive` · executor `claude` (phiên cloud mới,
`session_016aK6Uy4CzUZFKnDmoHRQps`) · reviewer `codex`. Phiên giao việc: `session_01FLVLxi5gKZgtVvbuTCEqEn`.
Lease `ops/leases/wp835-r3-g3-claude.yaml` @ `74072a3`. Đặc tả r3 `ops/specs/wp835-lease-6h-governance-r3.md`
sha256 `71403df8…6ddc` (đo lại, khớp); r2 sha256 `da98e225…7833` (đo lại, khớp).
Nhánh `agent/wp835-g3-claude`, base `d2e3052`. **Trạng thái: DỪNG — chờ chủ kho**, vì Codex lượt 1 trả
`changes_requested` với một P2 mà executor KHÔNG có quyền tự đóng (xem "Câu hỏi cho chủ kho").
Nhánh code **CHƯA ĐẨY** (đúng Q3: chỉ đẩy một lần khi N1–N5 đạt VÀ review approve). Commit ứng viên
`3785f9535398db04fb36a5eaa095166a8e048f1e` (tree `fd0c97ff…`) chỉ có trong container executor; bản vá đầy đủ
được chép ở phụ lục cuối tệp này để không mất khi container bị thu hồi.
KHÔNG merge/land/deploy.

## Đã làm
| tệp | việc |
|---|---|
| `docs/PROTOCOL_DA_PHIEN.md` | Port nguyên ba hunk §3.6/§4 + mẫu lease của bản vá r2 (`062292b..a62ba1f`) với `ADR-0055`→`ADR-0056` (áp sạch). Bảng §20: dòng `ADR-0017` sửa như bản vá (trỏ `ADR-0056`); dòng `ADR-0056` thêm tay NGAY SAU dòng `ADR-0055` của #919. Dòng `ADR-0052`/`ADR-0055` nguyên byte so base. |
| `docs/adr/0056-lease-no-progress-six-hours.md` | Mới: tệp ADR r2 đổi số, cộng ba chỗ provenance r3 — dòng Trạng thái (r3/g3, lý do đổi số), câu "đo lại 25-10-2026 tại base `d2e3052`", câu write set. Ngày Accepted giữ `2026-10-19`. Giữ `CHƯA KÍCH HOẠT VẬN HÀNH`. |
| `scripts/tl_selftest.py` | **KHÔNG sửa** — xem "Lệch đặc tả". |
| `RELEASE_MANIFEST.json` | **KHÔNG sửa** — không tệp nào trong gói đổi. |

Diff: 2 tệp, +61 −3 (≤ 4 tệp, ≤ 200 dòng thêm). `.github/coordination/change-impact.v1.json` vắng ở base (đo lại trước khi sửa).

## Lệch đặc tả (executor tự khai, reviewer xác nhận kỹ thuật, CHƯA có thẩm quyền)
D3.3 đòi sửa ratchet `r291_docs_ngoai_goi` "số Markdown dưới `docs/` +1 và cây thật +1, kèm khối KÊ KHAI SLOT";
N4 đòi phản chứng "bỏ sửa ratchet ⇒ r291 ĐỎ". Trên base `d2e3052`, `_c291_docs_ngoai_goi`
(`scripts/tl_selftest.py` ~21771–21985) đã **đóng nợ R291-DAM-SO-CUNG ở packet #794**: số `docs/*.md` TÍNH từ cây
(`ok4`), chỉ số tệp GÓI còn ratchet (`ok3 … == 192`), và chú thích ghi *"Thêm docs KHÔNG kê khai slot ở đây nữa."*
Không còn ratchet docs nào để +1; thêm khối KÊ KHAI SLOT sẽ trái chính chú thích ấy, và đổi băm `tl_selftest.py`
chỉ để buộc tái sinh manifest. Phép đo (full `tl.py --selftest`, mỗi vế một clone `--no-hardlinks`, abbrev 7,
`PYTHONDONTWRITEBYTECODE=1`):

| cây | kết quả | r291 |
|---|---|---|
| head `3785f95` (không sửa `tl_selftest.py`) | `== tl selftest 1731/1731 ==` rc 0, 210,5 s | OK |
| A: head + một `docs/ZZ_PHAN_CHUNG.md` thêm | `1731/1731` rc 0 | OK |
| B: head + ratchet gói `192`→`193` (dòng 21973) | `1730/1731` rc 1, FAIL duy nhất | **FAIL** |

A chứng minh không còn ratchet docs; B chứng minh ca r291 vẫn có răng ở bất biến còn sống (số tệp gói).
Codex lặp lại cùng kết luận bằng probe AST độc lập (`EXTRA_DOC r291 True`, `PACKAGE_RATCHET_192_TO_193 r291 False`).

## Tiêu chí N1–N7 — trạng thái trên `3785f95`
- **N1 ĐẠT** (đối chiếu văn bản): §4 360 phút chỉ cho lease MỚI sau kích hoạt; câu `lease_until` tuyệt đối,
  generation/fencing, bia mộ hai chiều, exact head nêu rõ "KHÔNG đổi"; đoạn `review_sla` (+2 giờ, treo theo review,
  heartbeat 15 phút sau `changes_requested`, hết SLA về đồng hồ thường) chỉ đổi cụm "thu-hồi-30-phút" → "thu-hồi-6-giờ
  (360 phút, …)". Codex so lại sau chuẩn hoá đúng cụm đổi: bằng nhau. Không lease YAML nào đổi.
- **N2 ĐẠT**: `adr-song` rc 0 — 55 ADR, 55 dòng §20, khớp 1–1.
- **N3 ĐẠT**: `doctrine-scan` rc 0 (10 tệp, 0 chỗ chép); `git diff --check` rc 0.
- **N4 MỘT PHẦN**: selftest `1731/1731` (hai số bằng nhau) trên cây = `3785f95`. Phản chứng như chữ spec KHÔNG THỂ
  đạt (không có ratchet docs để bỏ) — thay bằng A/B ở trên, chờ chủ kho chấp thuận. Lưu ý: trong sandbox Codex selftest
  ra `1729/1731` ở CẢ base lẫn head (FAIL `r226_…`, `r268_…` vì `git commit` của fixture rc 128 — công cụ ký commit
  gọi MCP localhost bị sandbox chặn `socket: operation not permitted`); delta 0, là tạo tác môi trường reviewer.
- **N5 ĐẠT**: `release-verify --strict --json` `ok: true`, expected 192 == checked 192; `doc-claims-check --strict`
  rc 2 ở cả base và head với đúng MỘT flag chung `docs/AUDIT_LAUNCHER_VONG_3.md:462 f08e45b SHA_NOT_A_COMMIT`
  (clone nông; `git cat-file -t f08e45b` rc 128) ⇒ đỏ sẵn, delta 0 (advisories 396→394, flag giống hệt).
- **N6 CHƯA ĐO**: chưa đẩy, chưa có lượt CI.
- **N7 ĐẠT**: ADR và dòng §20 giữ `CHƯA KÍCH HOẠT VẬN HÀNH`; không câu nào khai 360 phút đã có hiệu lực vận hành.

## Review
- Codex lượt **1/2** (`launcher.py run` `958a0a8a`, `codex-cli 0.164.0`, `model_reasoning_effort=xhigh`,
  `model_phuc_vu` đo được: `gpt-6.1-sol`, 961,8 s, rc 0) @ `3785f95`: **`changes_requested`**, đúng MỘT finding
  `WP835-R3-01` **P2** `dac-ta-ratchet-docs-da-loi-thoi`: executor đúng kỹ thuật, nhưng D3 + N4 là yêu cầu NỘI DUNG
  tường minh nên cần chủ kho duyệt revision; reviewer trả lời câu hỏi lệch là **(b)**, và khuyên KHÔNG tăng 192→193 hay
  dựng lại ratchet giả. Biểu hiện thứ hai cùng lớp: ADR :41–43 gọi companion là "ratchet đếm tài liệu".
  Không P0/P1/P3. Mọi lớp khác (đổi số, §20, port r2, provenance controller, dòng 1307, N7/ADR-0017) sạch.
  Hồ sơ: `ops/reviews/wp835-r3-g3-claude-review-1-codex-{prompt.md,run.json,verdict.md}` trên nhánh này.
- Ngân sách Codex: **1/2 đã dùng**, còn 1.

## Câu hỏi cho chủ kho (chặn tiến trình)
Chọn một:
1. **Duyệt revision r4** (khuyến nghị, đúng gợi ý reviewer): write set thu về 2 tệp; `tl_selftest.py` và
   `RELEASE_MANIFEST.json` không đổi; N4 = selftest N/N + phản chứng A/B ở trên. Executor sửa ADR :41–43 thành mô tả
   đúng (vd "write set khai bốn tệp; trên base này ratchet docs đã bỏ từ #794 nên hai tệp sau không đổi"), rồi dùng
   lời gọi Codex còn lại cho lượt 2.
2. Giữ chữ D3: thêm một khối chú thích KÊ KHAI SLOT (không đổi số nào) + tái sinh manifest. Reviewer và executor đều
   KHÔNG khuyến nghị — trái chú thích đóng nợ #794, và phản chứng N4 vẫn không đạt được.

## Lỗi khác lộ ra (không vá — Q5)
- Môi trường Codex: ký commit qua MCP localhost làm fixture git của `r226_*`/`r268_*` rc 128 trong sandbox
  `workspace-write` ⇒ reviewer không tái lập được N/N. Nợ môi trường review, không thuộc packet.
- `doc-claims-check --strict` đỏ sẵn trên clone nông (`f08e45b`).
- `/tmp/.git` rỗng: đã kiểm sau lượt Codex — KHÔNG có.

## Phụ lục — bản vá ứng viên `3785f95` (`git format-patch -1`, sha256 tệp `6ac35e5c…8970`)
Tái dựng: lưu khối dưới thành tệp rồi `git checkout -b agent/wp835-g3-claude d2e3052 && git am <tệp>` (SHA commit sẽ khác vì committer date; so tree phải ra `fd0c97ff…`).

~~~~
From 3785f9535398db04fb36a5eaa095166a8e048f1e Mon Sep 17 00:00:00 2001
From: Claude <noreply@anthropic.com>
Date: Sun, 25 Oct 2026 15:14:13 +0000
Subject: [PATCH] =?UTF-8?q?wp835=20r3/g3:=20ADR-0056=20=E2=80=94=20nguong?=
 =?UTF-8?q?=20thu=20hoi=20lease=20khong=20tien=20trien=2030=20->=20360=20p?=
 =?UTF-8?q?hut?=
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit

Port ban va r2/g2 (062292b..a62ba1f) len base d2e3052, doi so ADR 0055 -> 0056
vi 0055 da thuoc ADR tran loi goi Codex cua #919. Dong ADR-0056 them ngay sau
dong ADR-0055 trong bang §20; dong ADR-0052/ADR-0055 giu nguyen. ADR giu
trang thai CHUA KICH HOAT VAN HANH.

Packet #835, lease wp835-r3-g3-claude, spec r3 sha256 71403df8...

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016aK6Uy4CzUZFKnDmoHRQps
---
 docs/PROTOCOL_DA_PHIEN.md                    | 14 ++++--
 docs/adr/0056-lease-no-progress-six-hours.md | 50 ++++++++++++++++++++
 2 files changed, 61 insertions(+), 3 deletions(-)
 create mode 100644 docs/adr/0056-lease-no-progress-six-hours.md

diff --git a/docs/PROTOCOL_DA_PHIEN.md b/docs/PROTOCOL_DA_PHIEN.md
index 2f4853f..76a8a3e 100644
--- a/docs/PROTOCOL_DA_PHIEN.md
+++ b/docs/PROTOCOL_DA_PHIEN.md
@@ -265,6 +265,7 @@ write_set_hash: <sha256>
 generation: <integer>
 heartbeat_at: <timestamp>
 lease_until: <timestamp>
+heartbeat_required_minutes: 360   # lease MỚI cấp sau khi ADR-0056 kích hoạt; lease đã cấp giữ số đã đóng dấu
 ```
 
 Lease `role: reviewer` khai `provider: claude | codex | google_antigravity | human`
@@ -275,13 +276,19 @@ không mang họ model. Lease Executor dự kiến Reviewer AG còn khai
 `reviewer_model_family`, `reviewer_execution_surface`, `reviewer_transport` khi
 đã định tuyến. `cross_approved` nghiêm ngặt cần cả hai actor và họ model xác định.
 
-Sau 30 phút không có tiến triển, dispatcher thu hồi lease, tăng generation rồi mới reroute. Worker cũ sống lại
+Sau 6 giờ (360 phút) không có tiến triển, dispatcher thu hồi lease, tăng generation rồi mới reroute
+(`ADR-0056`; ngưỡng cũ 30 phút của `ADR-0017`). Ngưỡng này chỉ áp cho lease MỚI cấp sau khi `ADR-0056`
+kích hoạt vận hành; lease đã cấp — kể cả WP748 g19 — giữ nguyên byte và giữ `heartbeat_required_minutes`
+đã đóng dấu trong chính nó. Muốn một packet đang chạy hưởng 360 phút thì phải có lease kế nhiệm được
+cấp quyền riêng. `lease_until` tuyệt đối, fencing theo generation, bia mộ hai chiều và vô hiệu theo
+exact head KHÔNG đổi: hết `lease_until` thì lease hết dù còn trong 6 giờ. Worker cũ sống lại
 không thể heartbeat, push hợp lệ hoặc handoff. Branch/PR cũ chuyển `stale`; generation mới được đọc diff cũ nhưng
 không tự cherry-pick. Commit SHA cuối được giữ trong state projection và event journal.
 
 Khi packet vào state `reviewing`, `review_sla` là absolute timestamp do dispatcher/người giữ ghi vào lease/state
 bằng audit bền; mặc định khi đo được là thời điểm vào `reviewing` + 2 giờ. Thiếu trường, không parse được
-hoặc cơ sở giờ mơ hồ thì KHÔNG treo lease; đồng hồ thu-hồi-30-phút tiếp tục chạy theo xử lý fail-closed. Với
+hoặc cơ sở giờ mơ hồ thì KHÔNG treo lease; đồng hồ thu-hồi-6-giờ (360 phút, cùng ngưỡng không tiến triển
+ở trên) tiếp tục chạy theo xử lý fail-closed. Với
 `review_sla` hợp lệ, lease vào chế độ *treo theo review* tối đa tới timestamp đó. Verdict `changes_requested`
 đổ về thì executor phải heartbeat trong 15 phút, không thì thu hồi như thường. Quá `review_sla` mà chưa có verdict:
 lease trở lại đồng hồ thường — phiên ấm là TỐI ƯU HOÁ, không phải quyền.
@@ -1484,7 +1491,7 @@ Lệnh tái lập cột ấy nằm trong `ops/HOAN_THIEN_KE_HOACH_20260822.md` 
 
 | ADR | luật | trạng thái | cổng đã ĐO (22-08-2026) |
 |---|---|---|---|
-| `ADR-0017` | GitHub PR là bàn giao chính; canonical độc quyền phát hành | Accepted | có nhắc: rải khắp — chưa tách được cổng riêng |
+| `ADR-0017` | GitHub PR là bàn giao chính; canonical độc quyền phát hành | Accepted — câu ngưỡng thu hồi *"30 phút không có tiến triển"* **đã bị thay** bởi `ADR-0056` (2026-10-19) cho lease mới; phần còn lại vẫn hiệu lực | có nhắc: rải khắp — chưa tách được cổng riêng |
 | `ADR-0018` | EOL canonical theo loại tệp | Accepted | có nhắc: `ci.yml`×19 |
 | `ADR-0019` | Ba skill, hai adapter, một protocol | Accepted | có nhắc: `packet_loop.py`×31 (`doctrine-scan`) |
 | `ADR-0020` | Ranh giới an ninh cho worker cloud | Accepted | chưa đo |
@@ -1522,6 +1529,7 @@ Lệnh tái lập cột ấy nằm trong `ops/HOAN_THIEN_KE_HOACH_20260822.md` 
 | `ADR-0053` | Trần kích thước packet `sensitive` nâng theo chỉ thị chủ kho 16-10-2026, thay cặp số `sensitive` của `ADR-0044`; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | **0 cổng** |
 | `ADR-0054` | Đẩy nhánh code packet khi đủ điều kiện merge, review offline neo SHA cục bộ, dừng vá khi hết P0/P1/P2 ở mọi class, review tìm theo lớp; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted — chưa kích hoạt, chờ packet máy `MAY-ADR-0054` | **0 cổng** — không bộ đếm số lần đẩy |
 | `ADR-0055` | Trần trục LỜI GỌI Codex mỗi PR nâng theo chỉ thị chủ kho 25-10-2026, thay số của `ADR-0052`; trục LỜI GỌI nay bằng trục VÒNG; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | `packet_loop.py`: cùng bộ đếm trong state như `ADR-0052` — người khởi tạo tự truyền trần; không gì đọc dòng khai `tran_loi_goi_codex:` |
+| `ADR-0056` | Ngưỡng thu hồi lease vì không tiến triển nâng từ 30 lên 360 phút theo chỉ thị chủ kho 19-10-2026, thay đúng câu 30 phút của `ADR-0017`; chỉ áp lease mới, không hồi tố; `lease_until`, generation, bia mộ, exact head và heartbeat 15 phút sau `changes_requested` giữ nguyên | Accepted — chưa kích hoạt vận hành, chờ controller ngoài được đồng bộ và xác minh | **0 cổng** — không controller trong kho mang hằng 30 phút; controller ngoài chưa đo |
 
 ### B. ADR ngoài phạm vi protocol — thuộc `scripts/tl.py` và đường phát hành
 
diff --git a/docs/adr/0056-lease-no-progress-six-hours.md b/docs/adr/0056-lease-no-progress-six-hours.md
new file mode 100644
index 0000000..6bd0eb7
--- /dev/null
+++ b/docs/adr/0056-lease-no-progress-six-hours.md
@@ -0,0 +1,50 @@
+# ADR-0056 — Ngưỡng thu hồi lease vì không tiến triển nâng lên SÁU giờ (360 phút)
+
+- **Trạng thái:** Accepted (2026-10-19, chỉ thị chủ kho `ducthangho`; thi hành bằng packet `wp835`
+  revision 3 · generation 3 (bản vá r2/g2 port lên base mới, đổi số từ 0055 sang 0056 vì 0055 đã thuộc
+  `docs/adr/0055-tran-loi-goi-codex-len-muoi.md`), Issue #835 — không phải một phiên tự nới ngưỡng) ·
+  **CHƯA KÍCH HOẠT VẬN HÀNH**: chờ controller ngoài được đồng bộ và xác minh, xem mục *Hiệu lực*. Tới lúc ấy mọi lease vẫn chịu ngưỡng
+  đã đóng dấu trong chính nó.
+
+Lease không có tiến triển trong **6 giờ (360 phút)** thì dispatcher thu hồi, tăng generation rồi mới
+reroute. ADR này thay **đúng một câu** của `ADR-0017` — câu *"Sau 30 phút không có tiến triển"* — và
+không thay gì khác. Khi `review_sla` thiếu, không parse được hoặc cơ sở giờ mơ hồ, đồng hồ dự phòng
+fail-closed cũng là 6 giờ này, không phải một con số riêng.
+
+## Những gì KHÔNG đổi
+
+- `lease_until` vẫn là timestamp tuyệt đối: hết `lease_until` thì lease hết, kể cả khi chưa đủ 6 giờ
+  không tiến triển. Ngưỡng 6 giờ chỉ là cửa thu hồi SỚM, không gia hạn lease.
+- Fencing theo generation, bia mộ hai chiều (`thay_the_cho` · `da_bi_thay_the`) và vô hiệu theo exact
+  head giữ nguyên.
+- `review_sla` mặc định (vào `reviewing` + 2 giờ) và chế độ *treo theo review* giữ nguyên.
+- Verdict `changes_requested` đổ về thì executor vẫn phải heartbeat trong **15 phút**.
+- `ADR-0017` vẫn hiệu lực ở mọi phần còn lại.
+
+## Không hồi tố
+
+Ngưỡng mới chỉ áp cho lease **mới cấp sau khi kích hoạt**, và lease ấy khai
+`heartbeat_required_minutes: 360`. Lease đã cấp — kể cả WP748 g19 — giữ nguyên byte và giữ
+`heartbeat_required_minutes` đã đóng dấu. Muốn một packet đang chạy hưởng 360 phút thì phải có lease
+kế nhiệm được cấp quyền riêng sau khi ADR này kích hoạt; không sửa lease cũ tại chỗ.
+
+## Hiệu lực
+
+Đo 19-10-2026 bằng quét mã tĩnh tại acceptance base `062292b2c75be8c316a0cf7347290574efa10861`
+của revision 2, đo lại 25-10-2026 tại base `d2e3052d479d140b7e7b91df41ec4914fab7d544` của revision 3:
+không có controller nào **trong kho** mang hằng 30 phút cho việc thu hồi;
+ngưỡng ấy sống trong văn bản protocol và trong trường `heartbeat_required_minutes` của từng lease.
+Controller ngoài (dispatcher) **chưa đo được** từ phiên này. Nên ADR này chưa được khai là đã kích hoạt
+vận hành: chưa xác minh được controller đã đồng bộ thì không cấp lease 360 phút.
+
+`.github/coordination/change-impact.v1.json` (`ADR-0032`) vắng mặt ở cả hai base ấy. Write set của
+packet này (r3: tệp protocol, tệp ADR này, ratchet đếm tài liệu trong `scripts/tl_selftest.py` và
+`RELEASE_MANIFEST.json` tái sinh) là một ngoại lệ đóng tay một-packet do chủ kho duyệt trên Issue #835, không phải một
+closure tính từ policy.
+
+## Vì sao sáu giờ
+
+Đây là **quyết định của chủ kho**, không phải phép tối ưu. Ba mươi phút thu hồi cả những phiên đang
+làm việc thật nhưng chưa ghi heartbeat kịp — một gate dài hoặc một lượt review chéo là đủ để vượt
+ngưỡng — và mỗi lần thu hồi nhầm là một generation mới cộng một lượt handoff. Cái giá của sáu giờ là
+một worker chết thật giữ write set lâu hơn; `lease_until` tuyệt đối vẫn chặn trên cái giá ấy.
-- 
2.43.0

~~~~
