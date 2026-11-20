# Bản tham chiếu đo cho đặc tả `ops/specs/wp1236-r9.md`

Không phải mã thi công. Hai script chỉ dùng để ĐO số trong đặc tả, trên base `8048551` (20-11-2026):

- `thamchieu.py <gốc kho>` — chạy `kiem_tep` (K1–K8 bản nháp) trên mọi `ops/land/**/danh-gia-gate-output-*.txt` ⇒ `do_tep.txt`.
- `do_loi_khai.py <gốc kho>` — chạy luật L8 bản nháp trên mọi `ops/land/*-land-evidence.yaml` ⇒ `do_loi_khai.txt`.
  Bản sửa 2: la_landed ba dạng như kiem_ho_so_land; luật landed bắn cả khi đã có vi phạm khác. Bản sửa 1: có chốt cutover (chạy trước L8), `kiem_mien`, luật `landed`; bộ đọc nhận CRLF đồng nhất; K3 cờ provenance; K5 kết luận khớp.

Chạy: `python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` (cần PyYAML).
