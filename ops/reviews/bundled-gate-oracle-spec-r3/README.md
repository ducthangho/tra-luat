# Hiện vật đặc tả BUNDLED-GATE-ORACLE-FRESHNESS r3

Packet `wp433` revision 11, Issue #433. Thư mục này là hiện vật dev-side, không vào gói phát hành. Hiện vật của r2 giữ nguyên ở `../bundled-gate-oracle-spec-r2/`.

| tệp | sha256 | vai |
|---|---|---|
| `va.py` | `48cb657259b51ba8e93ea277a776eee5621be241a46381d04ddac81d19c09ee9` | Bản vá chuẩn cho W1 (M1, M2), gồm tám thay thế, mỗi thay thế khớp đúng một lần trên base `29c22f7d`. Dùng: `python3 va.py <gốc cây>` |
| `ma_tran_r11.py` | `ae5e27ce3fef651308d151e0aba6d4dbe2924da17f218064ed3fead137b90837` | **Ma trận A2, tự đủ, có thẩm quyền.** Gồm 95 đột biến cộng đối chứng, đích khai sẵn, kiểm `DON_DICH`. Dùng: `python3 -B ma_tran_r11.py <clone git>` |
| `gen_ma_tran.py` | `591726868731542fa76366e3a1106d4746c1ac5003507b534022c7500704dddc` | Chỉ để truy nguồn. Đây là script đã sinh `ma_tran_r11.py`, đầu vào là ma trận g5 (`ops/handoff/wp433/r9-g5/ma_tran_dot_bien.py` @ `bf38a110`, sha256 `fcfbc7fb…79b3`) và `probe_review_r1.py`. Nó đọc đầu vào theo đường dẫn scratch của phiên soạn, nên không chạy lại nguyên trạng được |
| `probe_review_r1.py` | `7940fd2ca6ab78ed0c368a24ff8cdacf3a452aa7462d3820fa463f98620aa24f` | Định nghĩa đột biến của review độc lập r1. Chỉ để truy nguồn |
| `ma-tran-nguyen-mau.out` | `357751b306beab0486b4329ea8554ab3d805867159fb8a4a4a450483e4262253` | Đầu ra trên nguyên mẫu |
| `ma-tran-base.out` | `bf5e22aafbf474831e60ed63619f9723f54401b427c9bf2ed049a07b4c951679` | Đầu ra trên base, dùng cho A0 |

## Phép đo

Hai clone đầy đủ được dựng trong MỘT lệnh, `shallow=false` (dòng định danh lúc 14:49:21Z 21-11-2026):
- `nen` = `29c22f7d`;
- `sau` = `29c22f7d` + `va.py`, commit cục bộ `a8231cdf` (không đẩy).

Hai lượt chạy song song, bắt đầu 14:49:21Z:

**Nguyên mẫu (`sau`).** Kết thúc 15:08:05Z, `rc=0`.
- `DON_DICH: 32/32 khoa co dot bien don dich`.
- `TONG: 95 dot bien + doi chung, sai=0`.

**Base (`nen`).** Kết thúc 15:06:36Z, `rc=1`, `sai=45`, đúng như kỳ vọng.
- A0 khớp cả năm ca:
  - `r11_size_only`, `r11_one_stale_ok` và `r11_missing_ok_narrow` cho `do=` rỗng;
  - `r11_ann_empty` cho `do=V4,V5,V6,V8,V9`;
  - `r11_duplicate` cho `do=V4,V5,V6,V8`.
- Có 20 ca `r11_` cho `do=` rỗng trên base, tức đột biến lọt hoàn toàn: 3 lỗ cũ cộng 17 đột biến cùng lớp.
- Các ca `a7_` cho `KHONG_AP_DUOC` vì chuỗi của bản vá không có trên base. Đây là điều đúng như thiết kế.
