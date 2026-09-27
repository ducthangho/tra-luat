# Review Claude độc lập — lượt 8 (agent `spec-reviewer-max`) — spec `THU-HOI-LEASE-A1b` bản nháp 13

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `b124b64` (sha256 `c2640ba3…`); `origin/master` `5c79fa2`; 448 = 448 ref
- reviewer: subagent Claude (định nghĩa cục bộ bị ignore — effort không là bằng chứng runtime), read-only;
  `same_provider_approved`; lượt Claude CUỐI — từ Q21 chỉ codex là reviewer
- ghi chú hình dạng: tóm lược do phiên điều phối ghi lại, không phải raw output bất biến.

VERDICT: changes_requested — **0 P1 / 4 P2 / 4 P3**

Đối chiếu lượt 7: F1 vá (18/18 ô khớp byte) nhưng sinh biểu hiện mới; F2 vá hờ; F3/F4/F13 nợ §8 khai đúng; F5 vá;
F6 vá phần R8(b), trùng tên vá hờ; F7 sinh lỗi mới; F8/F10/F11/F12 vá; F9 vá ở :7, sinh lỗi mới ở :37.

1. [P2] T7 không thể thoả trước đóng băng: tuple chứa `spec_hash` của chính bản đóng băng và `generation` của lease;
   verifier không có packet sở hữu; M1 còn "T1–T6".
2. [P2] §7 phân lớp lượt 7 thiếu (F2–F13 không slug; F1 ở hai lớp); F4 là lần 4 của "tập rỗng", F5 lần 9 của "nguồn được tin".
3. [P2] Q18-diễn giải giữ phần nới "#657"; thiếu chỗ lệch thật (§7 hiểu Q18 chỉ phủ "mốc giờ lệch"); neo `5853593828` (`5d52ad0b…`).
4. [P2] thiếu hàng cho quyết định checkpoint lần hai; `5853920122` (`b76b3052…`) đã thay nó ⇒ :9–11 trôi.
5. [P3] T7 đo sau `8bba697` nhưng tiêu đề cột ghi "tới trước `4324f2a`"; "= 0 ở A1b" nay = 1.
6. [P3] :37 "Recommended" — nguyên văn là "Theo khuyến nghị".
7. [P3] A5 còn "audit R8(b)" trong khi R8(b) không thoả được ⇒ "xác nhận 0 delta R8(b)".
8. [P3] bảng diễn giải: cột commit "(executor)" sai (`673256e`, `1503ca8`); cột "chiếu vào" trôi (A6→A7, §3→A8, M5/A5); "Q6" trần.
- đo lần hai khớp: 100 run trước 01:50Z = 89 success / 11 failure; annotation Ubuntu 26 (19-10-2026). Trôi: g20 → g21 (`9113c05`).

Xử lý: vá ở bản nháp 14.
