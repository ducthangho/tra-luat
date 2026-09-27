# EVIDENCE lượt 4 — lời khai của phiên soạn, KHÔNG phải phép đo của reviewer

## E15. Xử lý lượt 3 (bản nháp 4, commit `33e19c41`)
- Áp `HINT.luot3.patch` của bạn nguyên hunk (SPEC + `do_q6.py`); băm script sau áp = `7402a0bd…`, khớp băm bạn khai.
- Rồi **tự liệt kê mọi trường thuật toán Q6 đọc** (`lease_id`, `thay_the_cho`, `da_bi_thay_the`, `lease_expires_at_utc`) và đóng
  phần còn lại: phần tử `thay_the_cho` phải khớp `LEASE_ID` và không lặp; giá trị `da_bi_thay_the` phải khớp `LEASE_ID`; hạn đọc
  bằng `_doc_han` của cổng (hỏng ⇒ rc3, không Traceback). Kiểm trước trên cây mốc thật: cả 89 tệp qua mọi chốt mới.
- `do_q6.py` sha256 `040bfd0d…`; `--tu-kiem` 24/24 (`tu-kiem-q6-2026-09-26.log`).
- `mut_q6.py` (mới, sha256 `d74c282f…`): ma trận đột biến với tập ca đích KHAI TRƯỚC trong script; Traceback ⇒ LECH.
  Bản in cuối `mut-q6-2026-09-26.log`: 14/14 khớp + gốc sạch, `TAT_CA_KHOP`, rc0. Hai lần đo trước LỆCH (3 Traceback do chốt sau
  đọc giá trị chốt trước giả định đã loại; 2 mutant sống vì fixture thiếu hạn nên chốt hạn che) — đã sửa script/fixture.
- Kho thật: bản in do script bản nháp 4 sinh **byte-equal** `q6-do-2026-09-26.json` (`cmp` rc0, trước 23:45:23Z).

## E16. Mirror
`cay-kho/` detached tại `33e19c4121d32aeb4497c28214d7d3ffa20c9c08`. `origin` là bare CỤC BỘ `kho.git`; tập tên head = máy chủ lúc
23:47:11Z (437 head, `comm -3` rỗng). `master` = `68b552d0` (không đổi so E13 lượt 3).
