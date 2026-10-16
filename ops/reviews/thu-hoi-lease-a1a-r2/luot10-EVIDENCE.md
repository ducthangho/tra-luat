# EVIDENCE — lượt 10 (lời khai phiên soạn `claude`; reviewer tự kiểm lại, đừng tin)

- Head `8eb076b6d5ff41feafa723829d126e2c34c8ba3b` (PR #658). Từ lượt 9 (`3f1bf2e`): thêm `luot9-{PROMPT,VERDICT,EVIDENCE}.md`,
  `luot9-HINT.patch`, `tao_r3.py`; nối mục "Lượt 9/10 — revision 3" vào cuối `HAU-KIEM-CONNECTOR-652.md`
  (`DIFF.luot9-luot10.patch`). `SPEC.md` (r3) **không đổi**: sha256 `ac7e0129…`.
- F19: `luot9-EVIDENCE.md` giữ nguyên byte (là đầu vào reviewer lượt 9 đã đọc); đính chính nằm ở HAU-KIEM.
  `luot9-HINT.patch` KHÔNG áp.
- `tao_r3.py`: trích nguyên văn thân heredoc của lời gọi Bash đã tạo r3, lấy từ transcript JSONL của phiên soạn
  (không có trong sandbox). Phiên soạn đo: `grep -c '^rep('` = 8; chạy trong thư mục có `ops/specs/THU-HOI-LEASE-A1a-r2.md`
  là bản sao r2 ⇒ ghi `ops/specs/THU-HOI-LEASE-A1a-r3.md`, `cmp` với r3 trong kho rc0. sha256 `tao_r3.py` `ce56a45a…`.
- Mirror: 441 head, tập (tên, OID) lệch 0 so `git ls-remote --heads origin` lúc `2026-09-27T03:18:37Z`.
