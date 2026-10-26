# Cross-review wp835 — lượt 3 (exact-SHA hậu merge, Codex, read-only, lớp `sensitive`)

Bạn là REVIEWER độc lập (họ model openai), phiên MỚI, cho packet **wp835**, Issue #835 của `ducthangho/tra-luat`.
Executor là Claude Code (họ claude). KHÔNG sửa mã trong kho, KHÔNG commit, KHÔNG push, KHÔNG gọi mạng GitHub.
Chỉ ghi kết quả vào thư mục output nêu trong lời gọi.

## Vì sao có lượt này
Packet đã merge qua PR #931 (merge commit `7009ab9`, head `3e46a4b`). Lượt approve trước (lượt 2) neo `87fd761`, KHÁC head
được merge; protocol coi review cũ là stale khi head đổi, nên hồ sơ land ghi §8.1 CHƯA ĐẠT. Chủ kho nâng trần Codex lên 3
để có MỘT lượt review độc lập trên ĐÚNG exact head `3e46a4b` (#835 issuecomment-6406009892). Đây là review nội dung đầy
đủ trên head này, không phải chỉ đối chiếu hash — đừng nhận lời các lượt trước.

## Neo
- Exact head: `3e46a4b790b770e513ab05b0b3faf0dc88796903` (đã checkout detached), tree `11f0c80b6ca510bcf6d0d6fce6c2afdd531842f2`.
- Base diff sản phẩm: cha thứ nhất của merge commit trên head, `5775864b04a18c5afe1aafcbb23e54525ce8a3d8` (= `origin/master` lúc
  merge vào nhánh). Diff cần review: `git diff 5775864 3e46a4b` (2 tệp). Base đóng băng của packet: `d2e3052`.
- Lease g4 (đã rút hạn sau merge): `git show origin/ops/wp835-r4-g4-lease:ops/leases/wp835-r4-g4-claude.yaml`.
- Đặc tả r4 (DELTA trên r3, r3 DELTA trên r2): `git show origin/ops/wp835-r4-g4-lease:ops/specs/wp835-lease-6h-governance-r4.md`,
  sha256 `72bd63610f45a6295e18add2238a0e24d73bedefe8d4d9264608a4ccbef4e05e`; r3 `origin/ops/wp835-r3-g3-lease:ops/specs/wp835-lease-6h-governance-r3.md`
  sha256 `71403df8…6ddc`; r2 `origin/ops/wp835-r2-g2-lease:ops/specs/wp835-lease-6h-governance-r2.md` sha256 `da98e225…7833`.
  Tự băm lại; lệch thì P1 và dừng.
- Verdict hai lượt trước (tham khảo, KHÔNG thay cho phép đo của bạn):
  `origin/ops/wp835-r3-g3-lease:ops/reviews/wp835-r3-g3-claude-review-1-codex-verdict.md` (trên `3785f95`),
  `origin/ops/wp835-r4-g4-lease:ops/reviews/wp835-r4-g4-claude-review-2-codex-verdict.md` (trên `87fd761`).

## Việc
1. Review nội dung đầy đủ của `git diff 5775864 3e46a4b` theo đặc tả r4 (và r3/r2 phần không bị thay): N1, N2, N3, N4, N5, N7.
   - N1: §4 và fallback `review_sla` 360 phút chỉ cho lease MỚI; `lease_until`, generation, bia mộ, exact head,
     heartbeat 15 phút sau `changes_requested` giữ nguyên. So từng câu với `5775864`.
   - N2 `python .claude/dev/packet_loop.py adr-song --root .` rc 0; N3 `doctrine-scan` rc 0 và `git diff --check 5775864 3e46a4b` rc 0.
   - N4 `python scripts/tl.py --selftest` N/N (lượt trước bạn gặp `1729/1731` ở CẢ base lẫn head do ký commit qua MCP
     localhost bị sandbox chặn — nếu gặp lại, đo cùng lệnh trên `5775864` và báo delta).
   - N5 `release-verify RELEASE_MANIFEST.json --strict --json` ok, expected == checked; `doc-claims-check --strict --json` delta 0 so `5775864`.
   - r4 E1: `scripts/tl_selftest.py` và `RELEASE_MANIFEST.json` nguyên byte so `d2e3052`.
   - N7: ADR-0056 giữ `CHƯA KÍCH HOẠT VẬN HÀNH`.
2. Tìm theo LỚP: đổi số ADR-0056 vs ADR-0055 của #919 (dòng §20 `ADR-0052`/`ADR-0055` nguyên byte), thứ tự §20 và khớp
   1:1 tệp ADR, lời khai provenance trong ADR (dòng Trạng thái, câu đo lại tại `d2e3052`, câu write set r4) có rộng hơn
   phép đo không, câu nào trong protocol còn nói thu hồi 30 phút mà bị bỏ sót, mâu thuẫn ADR-0056 với §4/ADR-0017.
3. Xác nhận merge commit `3e46a4b` (cha `87fd761` và `5775864`) không đưa thay đổi sản phẩm nào khác ngoài hai tệp:
   `git diff 5775864 3e46a4b --stat` và `git diff d2e3052 87fd761` so với `git diff 5775864 3e46a4b`.

Đừng tự soạn nội dung dựng đường dẫn thoát khỏi cây thư mục; hướng nào cần thế thì mô tả bằng lời.

## Output (bắt buộc)
Ghi DUY NHẤT tệp `VERDICT.md` vào thư mục output. Dòng đầu đúng một trong hai: `VERDICT: approve` hoặc
`VERDICT: changes_requested`. Kế: `Reviewed commit: 3e46a4b790b770e513ab05b0b3faf0dc88796903`. Rồi finding gắn P0/P1/P2/P3,
tệp:dòng, lệnh đã chạy + output rút gọn, và phép nào KHÔNG chạy được. Approve chỉ khi không còn P0/P1/P2.
