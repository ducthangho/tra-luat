# Bản tham chiếu đo cho đặc tả `ops/specs/wp1236-r9.md`

Không phải mã thi công. Hai script chỉ dùng để ĐO số trong đặc tả, trên base `8048551` (20-11-2026):

- `thamchieu.py <gốc kho>` — chạy `kiem_tep` (K1–K8 bản nháp) trên mọi `ops/land/**/danh-gia-gate-output-*.txt` ⇒ `do_tep.txt`.
- `do_loi_khai.py <gốc kho>` — chạy luật L8 bản nháp trên mọi `ops/land/*-land-evidence.yaml` ⇒ `do_loi_khai.txt`.
  Chưa cài `kiem_mien`: mọi `owner_waived` bị đếm là vi phạm.

Chạy: `python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` (cần PyYAML).
