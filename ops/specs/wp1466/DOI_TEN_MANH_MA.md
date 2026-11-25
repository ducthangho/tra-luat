# Đổi tên bốn mảnh mã của nguyên mẫu (21-11-2026)

Bốn tệp dưới đây là MẢNH mã để chèn vào `packet_loop.py`, không phải module Python hoàn chỉnh. Vì thế chúng không
parse được. Cổng `ops/bash_nen.py quet` đọc mọi tệp `*.py` trong INDEX và cố ý trả KHÔNG_ĐO_ĐƯỢC (fail-closed) khi gặp
tệp không phân tích được. Nó đã làm `gate (ubuntu-latest)` của PR #1495 đỏ, run `44933307995`.

| tên cũ | tên mới |
|---|---|
| `nguyen-mau-r2/ma_moi.py` | `nguyen-mau-r2/ma_moi.py.txt` |
| `nguyen-mau-r3/ma3.py` | `nguyen-mau-r3/ma3.py.txt` |
| `nguyen-mau-r4/ma4.py` | `nguyen-mau-r4/ma4.py.txt` |
| `nguyen-mau-r5/sc/ma5.py` | `nguyen-mau-r5/sc/ma5.py.txt` |

Nội dung từng tệp giữ nguyên byte. Dòng băm trong `SHA256SUMS` của mỗi thư mục chỉ đổi đường dẫn; kiểm bằng
`sha256sum -c` đều đạt. Script `nguyen-mau-r2/ap_ma.py` vẫn đọc tên cũ `ma_moi.py`. Script ấy được giữ nguyên làm hồ sơ;
muốn chạy lại thì đổi tên tệp về như cũ trên một bản sao. Đặc tả `ops/specs/wp1466.md` không nhắc tới bốn tên này,
nên `spec_hash` không đổi.
