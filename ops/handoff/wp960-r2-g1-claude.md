# Handoff — packet NO-CAU-LICH-SU-BIEN-NHAN revision 2 (Issue #960)

- Lease: `wp960-r2-g1-claude` → gia hạn thành `wp960-r2-g2-claude` (hết hạn 2026-10-30T14:43Z). Executor: Claude, phiên
  `session_015GtxrbeTfDyFKdj7rb72Uq`. Spec: `ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md` (sha256 `9a155cb9…`). Base `4488444`.
- Trạng thái: **DỪNG — hết trần 8 lời gọi codex, chưa có verdict `approve`**. M-1 CHƯA đạt.

## Đã land / đang mở
- **PR #995 ĐÃ MERGE** (chủ kho, `79dbaf4`) ở head `6dca85f` — toàn bộ code cổng r2 (`ops/bien_nhan_v2.py`) đã ở master.
  Merge diễn ra khi review lượt 5 còn 1 P1 + 1 P2 (đều là ca test thiếu răng) và chưa có approve.
- **PR #1005 (draft, mở)**: `78c138f` + `057abc8` — CHỈ `ops/bien_nhan_v2_test.py`, vá test lượt 5 và lượt 6.
  Cổng tại head PR giống hệt master từng byte. CI xanh trên `78c138f` và `057abc8` (check suite hoàn tất 2026-10-29T06:46Z).
  Tại chỗ trên `057abc8`: **93/93 ca · 135/135 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM**; `bien_nhan_v2 --root .` rc=0,
  nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0.

## Chuỗi cross-review r2 (codex, `launcher.py run`, xhigh)
| lời gọi | lượt | run | head | kết quả |
|---|---|---|---|---|
| 1 | 1 | `237621c6` | `f7659a2` | changes_requested 6 P1 / 1 P2 / 1 P3 |
| 2 | 2 | `5b108d0d` | `ae0d06c` | changes_requested 5 P1 |
| 3 | 3 | `ae2d0a62` | `934a5b0` | CHẾT giữa chừng (container khởi động lại), rc=1, không verdict |
| 4 | 3 | `40802fd7` | `934a5b0` | changes_requested 6 P1 / 1 P2 |
| 5 | 4 | `2997494e` | `3a52e6d` | changes_requested 4 P1 |
| 6 | 5 | `0468976f` | `6dca85f` | changes_requested 1 P1 / 1 P2 (test) |
| 7 | 6 | `c9d2db30` | `78c138f` | changes_requested 2 P1 (test) |
| 8 | 7 | `2cc0012a` | `057abc8` | changes_requested **1 P1 (test)** |

Mọi finding của lượt N đều được lượt N+1 xác nhận ĐÓNG. Số finding: 8 → 5 → 7 → 4 → 2 → 2 → 1; từ lượt 5 chỉ còn ca test
thiếu răng, reviewer xác nhận hành vi cổng đúng trên mọi witness.
Hiện vật review (VERDICT.md, run.json, evidence) đang ở sandbox của phiên (`/tmp/claude-0/rv/wp960-r2-review-*-codex/`) —
CHƯA ghi sổ vào `ops/reviews/` (container có thể bị thu hồi; xem "Việc còn lại").

## Quyết định của chủ kho trong r2 (ghi trên #960)
1. Sau lượt 1 (M-4): vá trong r2. 2. Sau lượt 2: đổi kiến trúc tra git (`_git_do`: chỉ tin khi rc sạch VÀ stderr rỗng).
3. Sau lượt 3: vá nhóm A; **khai nhóm B là tiền đề** (object/commit-graph sai mà git im lặng — cần `git fsck`).
4. Sau lượt 4: vá hẹp; **tiền đề mới**: cấu hình git in cảnh báo ⇒ KHÔNG ĐO ĐƯỢC (CI clone sạch).
5. Sau lượt 5/6: thêm test, dùng tiếp ngân sách. 6. Gia hạn lease 24h (g2).

## Finding còn mở (lượt 7, P1, HÌNH DẠNG `bo-chon-ung-vien`)
`bien-ngoai-cua-so-surface-chua-co-rang`: M4 giới hạn lời tự khai ở đúng {dòng trước, dòng ấy, dòng sau}; nới cận phải
`j+2→j+3` hoặc cận trái `j-1→j-2` vẫn qua 93/93. Hành vi cổng ĐÚNG; thiếu ca khoá biên. Reviewer gửi `HINT.patch` (chỉ tệp
test: hàng `provider`/trích dẫn cách khai báo đúng hai dòng, trước và sau + hai đột biến), sha256 `d21485b0…`, đã dry-run sạch
và tự chạy full suite trên scratch: 93/93 ca · 137/137 đột biến. CHƯA áp vào PR #1005.
Verdict lượt 7 sha256 `ccb7abd2…`.

## Việc còn lại (chủ kho quyết)
- Áp HINT lượt 7 vào PR #1005 (chỉ test) — cần `nang_tran` ngân sách codex nếu muốn verdict `approve` trên head cuối (M-1).
- Ghi sổ hiện vật review r2 vào `ops/reviews/` (biên nhận v2 + README) như tiền lệ PR #985 — PHẢI làm trước khi container
  bị thu hồi, hoặc chấp nhận mất hiện vật.
- Merge PR #1005 hay đóng nó.
