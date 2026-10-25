# Đặc tả packet wp835 — revision r3 (DELTA trên r2): ADR ngưỡng thu hồi lease 6 giờ, đổi số sang ADR-0056, write set 4 tệp

Đặc tả đóng băng, là DELTA: mọi điều của r2 (`ops/specs/wp835-lease-6h-governance-r2.md` trên `ops/wp835-r2-g2-lease`,
sha256 `da98e225c1e0bb419b83c368d2b3112309bd95316a4787c18f91f79bdbc57833`) giữ nguyên, TRỪ những điểm ghi dưới đây.
Đặc tả KHÔNG cấp việc: cần Issue #835 + lease r3 còn hiệu lực.

**Trạng thái quyết định** (ghi hộ #835 issuecomment-6397870294 và #919 issuecomment-6399079847): chủ kho chọn
*"Land #835 + sửa số"*, *"Đổi #835 sang ADR-0056"*, *"Thêm hai tệp"* (`tl_selftest.py` + manifest) và *"Rút gạn phiên
#919 cho #835 ngay"*. Lease r2 hết hạn 2026-10-19T13:59Z; bản vá r2 (`agent/wp835-g2-claude` `a62ba1f`) CHƯA từng được
review approve.

- `revision`: 3 · `generation`: 3 · base = `origin/master` `d2e3052d479d140b7e7b91df41ec4914fab7d544` (sau #919, PR #926).
- `review_class`: **sensitive** · executor `claude` (phiên cloud MỚI) · reviewer `codex` ⇒ `cross_approved`.
- Nhánh: `agent/wp835-g3-claude`, rẽ từ base. Ngoại lệ closure thủ công của chủ kho (r1/r2) vẫn áp: base vẫn
  không có `.github/coordination/change-impact.v1.json` (đo lại trước khi sửa; thấy có thì DỪNG).

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

## Thay đổi so với r2
**D1 — Đổi số ADR 0055 → 0056.** Số 0055 trên base đã thuộc `docs/adr/0055-tran-loi-goi-codex-len-muoi.md` (#919),
và `.claude/dev/packet_loop.py` (`ADR0055_TEP`) đang chờ một ADR kích hoạt `ADR-0054` mang tên 0055 (nợ riêng của #816,
KHÔNG thuộc packet này). Tệp mới là `docs/adr/0056-lease-no-progress-six-hours.md`. Mọi chỗ trong bản vá nhắc
`ADR-0055` theo nghĩa "ngưỡng lease 6 giờ" đổi thành `ADR-0056`; mọi chỗ nhắc `ADR-0055` của #919 giữ nguyên.

**D2 — Nguồn bản vá.** Port nội dung `git diff 062292b a62ba1f` (2 tệp, +58 −3) lên base mới. Phần §3.6/§4 và mẫu lease
áp sạch. Phần bảng §20 KHÔNG áp sạch vì #919 đã thêm dòng `ADR-0055` vào đúng chỗ: port tay — dòng `ADR-0017` sửa như
bản vá (trỏ `ADR-0056`), thêm dòng `ADR-0056` NGAY SAU dòng `ADR-0055` hiện có; không đụng dòng `ADR-0052`/`ADR-0055`.
Ngày Accepted trong ADR giữ `2026-10-19` (ngày chỉ thị gốc) và ghi thêm thi hành bằng `wp835` r3/g3.

**D3 — Write set 4 tệp** (diff PR ≤ 4 tệp; ≤ 200 dòng thêm):
1. `docs/PROTOCOL_DA_PHIEN.md` — chỉ các chỗ bản vá r2 chạm, cộng dòng §20 theo D2.
2. `docs/adr/0056-lease-no-progress-six-hours.md` — tệp mới.
3. `scripts/tl_selftest.py` — CHỈ ratchet của `r291_docs_ngoai_goi`: số Markdown dưới `docs/` +1 và cây thật +1, kèm
   khối chú thích `KÊ KHAI SLOT` theo đúng nếp các mục trước (vd mục packet #784 r2 — ADR-0054).
4. `RELEASE_MANIFEST.json` — tái sinh bằng `python scripts/tl.py release-manifest --deterministic --out RELEASE_MANIFEST.json`
   (chỉ vì băm `scripts/tl_selftest.py` đổi; `file_count` phải giữ nguyên).

Handoff `ops/handoff/wp835-g3-claude.md` và verdict Codex ghi trên NHÁNH LEASE `ops/wp835-r3-g3-lease`, không vào diff PR.

## Tiêu chí hoàn tất (thay mục gate của r2)
- **N1** §4 và fallback `review_sla`: 360 phút cho lease MỚI; `lease_until`, generation, bia mộ, exact head, heartbeat
  15 phút sau `changes_requested` giữ nguyên (so câu base/head, ghi vào handoff).
- **N2** `python .claude/dev/packet_loop.py adr-song --root .` rc 0 (bảng §20 khớp 1:1 tệp ADR; không trùng số).
- **N3** `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `git diff --check` rc 0.
- **N4** `python scripts/tl.py --selftest` trên ĐÚNG commit sẽ đẩy ⇒ `N/N` hai số bằng nhau (bài học R291-DAM-SO-CUNG).
  Phản chứng: bản sao bỏ sửa ratchet ⇒ `r291_docs_ngoai_goi` ĐỎ.
- **N5** `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked`;
  `python scripts/tl.py doc-claims-check --strict --json` delta so base = 0.
- **N6** `ci.yml` lượt PR XANH trên head cuối, đọc bằng check run.
- **N7** Không tuyên bố ngưỡng 360 phút đã kích hoạt vận hành: ADR giữ `CHƯA KÍCH HOẠT VẬN HÀNH` như r2.

## Q đã chốt
- **Q1** Codex qua `.claude/dev/launcher.py run`, lớp `sensitive`, tối đa **2** lời gọi (lease ghi cùng số); verdict trên nhánh lease.
- **Q2** Attempt tối đa 2. **Q3** Không merge/land/deploy; PR DRAFT, đẩy MỘT lần khi N1–N5 đạt và review approve.
- **Q4** Master tiến mà chạm một trong 4 tệp ⇒ DỪNG, hỏi trên #835; không chạm ⇒ merge master (không rebase, không force-push).
- **Q5** Lỗi khác lộ ra ⇒ ghi handoff, KHÔNG vá. **Q6** Test ngoài write set đỏ ⇒ DỪNG, hỏi trên #835.
