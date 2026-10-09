# Tự kiểm phía executor — spec `THU-HOI-LEASE-A1b` bản nháp 11

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `cd40536` (đã push vì hook đòi push trước khi tự kiểm xong)
- vai: bước tự kiểm của executor, agent `spec-selfcheck-xhigh` (effort **xhigh**, định nghĩa cục bộ, không trong
  kho), read-only; KHÔNG là review, KHÔNG là assurance
- ghi chú hình dạng: tóm lược do phiên điều phối ghi lại, không phải raw output bất biến.

Kết quả: **0 P1 / 4 P2 / 6 P3**

1. [P2] Q18 khai "tập rỗng" chạm ba lượt; §7 đếm 2 ⇒ lần ba thật bị đọc thành đã checkpoint.
2. [P2] executor sửa dòng quyết định chủ kho: Q2 thêm (g) (gốc `65a612a:17` là (a)(c)(d)(h)); Q7 mất "không tự nới".
3. [P2] A5 "chờ chủ kho readback mới" mở đường thứ hai cho fact (g), trái Q2/T3 (facts đóng băng).
4. [P2] A5 mặt đo kho thật: run canonical chạy mã master (mỏ neo rỗng ⇒ 12); seam đòi hồ sơ từ receipt T5 mà T5 không ghi hồ sơ tầng bắt buộc; `:1326` so `git_path` cục bộ.
5. [P3] §7/Q18 dẫn `:1053–1054/1055`; luật đơn vị ở `:1054–1055`; hàng "tiền đề chưa có producer" là 1 lượt.
6. [P3] §2 gán json Q6 cho `do_q6_hk.py`; thật do `do_q6.py` sinh (`79b8ec7`), hợp lệ nhờ `cmp` r3; codex lượt 1–4 đều chạy `do_q6.py`.
7. [P3] dòng 11 "Bản nháp 10 (commit ghi dòng này)" lỗi thời.
8. [P3] §8.6 "nay 445/445" không neo SHA; đo 446 = 446; "tại commit `699057c`" sai nghĩa.
9. [P3] A5 đối chứng âm thiếu `11→0`, `12→0`.
10. [P3] `dong_bang` cho "bác" mà vẫn đóng băng; Q18 không có ID bền; nit A4/Q10 chỗ ghi audit; `_du_bao_check` bắt đầu `:1762`.

Xử lý: vá cả 10 ở bản nháp 12.
