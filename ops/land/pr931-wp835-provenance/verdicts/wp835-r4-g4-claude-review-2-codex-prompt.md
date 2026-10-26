# Cross-review wp835 r4/g4 — lượt 2/2 (Codex, read-only, lớp `sensitive`)

Bạn là REVIEWER độc lập (họ model openai), phiên MỚI, cho packet **wp835**, Issue #835 của `ducthangho/tra-luat`.
Executor là Claude Code (họ claude). KHÔNG sửa mã trong kho, KHÔNG commit, KHÔNG push, KHÔNG gọi mạng GitHub.
Chỉ ghi kết quả vào thư mục output nêu trong lời gọi. Đây là lời gọi Codex CUỐI cùng của packet (2/2).

## Neo
- Exact head: `87fd7611001ebffd20a87c934fcf578644984b4b` (đã checkout detached; nhánh dự kiến `agent/wp835-g4-claude`).
- Base: `d2e3052d479d140b7e7b91df41ec4914fab7d544`.
- Lease g4: `git show origin/ops/wp835-r4-g4-lease:ops/leases/wp835-r4-g4-claude.yaml`.
- Đặc tả r4 (DELTA trên r3): `git show origin/ops/wp835-r4-g4-lease:ops/specs/wp835-lease-6h-governance-r4.md`,
  sha256 `72bd63610f45a6295e18add2238a0e24d73bedefe8d4d9264608a4ccbef4e05e`.
- r3: `git show origin/ops/wp835-r3-g3-lease:ops/specs/wp835-lease-6h-governance-r3.md`, sha256 `71403df8…6ddc`.
- r2: `git show origin/ops/wp835-r2-g2-lease:ops/specs/wp835-lease-6h-governance-r2.md`, sha256 `da98e225…7833`.
- Verdict lượt 1 (head `3785f95`): `git show origin/ops/wp835-r3-g3-lease:ops/reviews/wp835-r3-g3-claude-review-1-codex-verdict.md`.
- Tự băm lại các đặc tả; lệch thì P1 và dừng.

## Diff
`git diff d2e3052 87fd761` — 2 tệp. Head gồm hai commit: `3785f95` (đã review ở lượt 1) và `87fd761` (chỉ sửa câu
write set trong `docs/adr/0056-lease-no-progress-six-hours.md`, đáp WP835-R3-01: `git diff 3785f95 87fd761`).

## Việc chính (E4 của r4: lượt này xác minh bản vá đã bỏ hai tệp, trên exact head mới)
1. Đóng hay không đóng **WP835-R3-01**: r4 E1/E2 bỏ D3.3/D3.4 và phản chứng ratchet. Kiểm
   `scripts/tl_selftest.py` và `RELEASE_MANIFEST.json` nguyên byte so base; câu write set mới trong ADR (dòng ~40–44)
   có mô tả đúng thực tế và không khai rộng hơn phép đo không.
2. Kiểm lại N1–N7 theo r4 trên head mới (N4 mới: selftest N/N + r291 OK; N5 mới: release-verify strict với manifest
   không sửa + doc-claims delta 0). Executor đo tại chỗ trên `87fd761` — kết quả sẽ nằm trong handoff g4; đừng nhận
   lời, tự chạy những gì sandbox cho phép. Lượt 1 bạn đo selftest `1729/1731` ở CẢ base và head do ký commit qua
   MCP localhost bị sandbox chặn (`r226_*`, `r268_*`); nếu gặp lại, ghi delta so base.
3. Soát thêm theo lớp những gì lượt 1 đã soát (đổi số ADR-0056 vs ADR-0055 của #919; §20; port r2; N7), chỉ cần xác
   nhận commit `87fd761` không làm hỏng điều gì; tìm lớp lỗi mới nếu có, đặc biệt trong đoạn ADR vừa sửa (ví dụ câu
   "Revision 4 (chủ kho duyệt 25-10-2026)" có khớp nguồn thẩm quyền trong lease g4 không).

Đừng tự soạn nội dung dựng đường dẫn thoát khỏi cây thư mục; hướng nào cần thế thì mô tả bằng lời.

## Output (bắt buộc)
Ghi DUY NHẤT tệp `VERDICT.md` vào thư mục output. Dòng đầu đúng một trong hai: `VERDICT: approve` hoặc
`VERDICT: changes_requested`. Kế: `Reviewed commit: 87fd7611001ebffd20a87c934fcf578644984b4b`. Rồi finding gắn
P0/P1/P2/P3, tệp:dòng, lệnh đã chạy + output rút gọn; trạng thái WP835-R3-01 (đóng/còn); phép nào KHÔNG chạy được.
Approve chỉ khi không còn P0/P1/P2.
