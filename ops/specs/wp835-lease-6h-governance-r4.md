# Đặc tả packet wp835 — revision r4 (DELTA trên r3): bỏ hai tệp thừa, write set 2 tệp

Đặc tả đóng băng, là DELTA: mọi điều của r3 (`ops/specs/wp835-lease-6h-governance-r3.md` trên `ops/wp835-r3-g3-lease`,
sha256 `71403df80d133e4568cb891ae5ab41de937a9d1d1086a92f7255323568596ddc`) và qua đó của r2 giữ nguyên, TRỪ những điểm
ghi dưới đây. Đặc tả KHÔNG cấp việc: cần Issue #835 + lease r4 còn hiệu lực.

**Trạng thái quyết định:** Codex lượt 1/2 trên head cục bộ `3785f95` (verdict `ops/reviews/wp835-r3-g3-claude-review-1-codex-verdict.md`
trên `ops/wp835-r3-g3-lease@79fd653`) trả `changes_requested` với đúng một P2, WP835-R3-01: D3.3/N4 của r3 đòi nâng ratchet
docs của `r291_docs_ngoai_goi`, nhưng ratchet ấy đã bỏ từ #794 — `_c291_docs_ngoai_goi` chỉ đòi số `.md` dưới `docs/` ≥ 1
(đếm từ cây), và ghim duy nhất còn lại là số tệp trong GÓI (192), không đổi khi thêm một ADR ngoài gói. Lỗi thuộc phiên
điều phối soạn r3. Chủ kho chọn *"Soạn r4, bỏ 2 tệp thừa"* (ghi hộ #835 issuecomment-6399670937).

- `revision`: 4 · `generation`: 4 · base giữ `d2e3052d479d140b7e7b91df41ec4914fab7d544` (master tới `cdc4e80` chỉ thêm `ops/land/**`).
- Executor: CÙNG phiên `session_016aK6Uy4CzUZFKnDmoHRQps` (lease g4 thay g3 bằng bia mộ hai chiều).

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

## Thay đổi so với r3
**E1 — Write set còn 2 tệp** (diff PR ≤ 2 tệp; ≤ 150 dòng thêm): `docs/PROTOCOL_DA_PHIEN.md` và
`docs/adr/0056-lease-no-progress-six-hours.md`. BỎ D3.3 (`scripts/tl_selftest.py`) và D3.4 (`RELEASE_MANIFEST.json`): hai
tệp này phải giữ NGUYÊN byte so với base.
**E2 — N4 mới:** `python scripts/tl.py --selftest` trên ĐÚNG commit sẽ đẩy ⇒ `N/N` hai số bằng nhau. Bỏ vế phản chứng
"bỏ sửa ratchet ⇒ r291 đỏ" (không còn ratchet docs để phản chứng). Ghi kèm dòng ca `r291_docs_ngoai_goi` ĐẠT.
**E3 — N5 mới:** `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` và `expected == checked` VỚI manifest
không sửa; `doc-claims-check --strict --json` delta so base = 0.
**E4 — Ngân sách review không reset:** đã dùng 1/2 lời gọi Codex ở g3 (`ops/reviews/wp835-r3-g3-claude-review-1-codex-*`).
Lượt 2/2 chỉ dùng để xác minh bản vá đã bỏ hai tệp, trên exact head mới. Hết lượt 2 mà chưa approve ⇒ DỪNG, hỏi trên #835.
**E5 — Handoff:** `ops/handoff/wp835-g4-claude.md` trên nhánh lease `ops/wp835-r4-g4-lease`; verdict lượt 2 cũng ghi ở đó.
Có thể chép handoff g3 làm điểm xuất phát.

Mọi điều khác của r3 (D1 đổi số 0056, D2 port tay dòng §20, N1, N2, N3, N6, N7, Q1–Q6) giữ nguyên.
