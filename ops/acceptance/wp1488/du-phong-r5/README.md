# Dự phòng r5 của packet #1488 — chưa phải nhánh PR

Nhánh này giữ an toàn công việc r5 trong lúc lease `wp1488-r5-g5-claude` chưa cấp được (lease `wp1511-r2-g2-claude`
còn giữ `.claude/dev/launcher_test.py` tới 2026-11-26T16:30Z). Chủ kho cho phép đẩy dự phòng (2026-11-26). KHÔNG mở PR
từ nhánh này; khi có lease, đúng lịch sử tới `4cd2ba2` sẽ được đưa lên `claude/ci-github-path-hoan-ghi` (PR #1489).

- Ứng viên đã review: `4cd2ba29acdb1fba5eac2267a17d049fa0880a41` (cha của commit chứa tệp này).
  = `210ceff` (head PR #1489) + merge master `d0868db` (`9390529`) + r5 `e9ac35b` + P3 lượt 6 `4cd2ba2`.
- Đặc tả r5: `wp1488-r5.md` ở đây, sha256 `c27e7b6d14422d892e28840897340b1181c1315d5a79fb393e7958ad61967580`, chủ kho duyệt 2026-11-25
  (AskUserQuestion "Duyệt r5, trần 8"). Chưa có lease g5 ⇒ chưa nằm ở `ops/specs/`.
- Codex lượt 6 (`e9ac35b`): approve, 2 P3 — `VERDICT-luot6-codex.md` (sha256 `7399c368a62f9a7dabd6fa2b26ddb7dec3b336dbdaceabfa972936f1a62e9a6f`).
- Codex lượt 7 (`4cd2ba2`): approve, không finding — `VERDICT-luot7-codex.md` (sha256 `7b1921361d62b5c53375b753f1e8e867003bc179aaca35c093c5bd1602a7bbb8`).
- Đo Linux, hai vế trong cùng một lệnh (2026-11-25T20:58Z–21:21Z): master `d0868db` 455/455 · đột biến 801/801;
  `4cd2ba2` 456/456 · đột biến 830/830 (cùng 2 ca bỏ qua, 7 đột biến chỉ đo được trên Windows).
- Commit merge `9390529` mang tác giả giữ chỗ `x`: giữ nguyên để không đổi SHA đã được review.
