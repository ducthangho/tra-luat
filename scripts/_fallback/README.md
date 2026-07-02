# scripts/_fallback/ — bản nền TỐI THIỂU, chỉ dùng khi thiếu bản thật

Mục đích: cho overlay **tự chạy** trong phiên trống (ping/boot/manifest/preingest) MÀ
**không đè** bản nền giàu tính năng của bộ skill tra-luat đầy đủ.

Cơ chế: `tl.py`/`contract_check.py` import qua helper `_imp(name)` — chèn `scripts/` GỐC
trước, `_fallback/` sau. ⇒ có `scripts/gas.py` (bản thật) thì DÙNG bản thật; không có thì
rơi xuống `_fallback/gas.py`. Tự thân các script ở đây cũng ưu tiên gas thật (ROOT-precedence).

KHÔNG chép các tệp này ra `scripts/` gốc (sẽ thành đè bản thật). Thiết kế hội tụ với bản
runtime-hotfix của reviewer, khác ở chỗ đặt trong `_fallback/` để an toàn khi cài chồng.
