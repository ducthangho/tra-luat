# Hiện vật đặc tả BUNDLED-GATE-ORACLE-FRESHNESS r2

Packet `wp433` revision 11, Issue #433. Thư mục này là hiện vật dev-side và không vào gói phát hành.

| tệp | sha256 | vai |
|---|---|---|
| `va.py` | `67102d02d1a0ad63d9ea822a692ba92fe2d548236dab59873fec26016f8b4965` | Bản vá chuẩn cho W1 (M1, M2). Dùng: `python3 va.py <gốc cây>`. Bảy thay thế, mỗi thay thế khớp đúng một lần trên base `29c22f7d`. |
| `ma_tran_r11.py` | `fc31af216e52611eaa7002ca084d8252ff86b3ad273062515f6f8957323fa069` | Ma trận đột biến A2, gồm 79 đột biến cộng đối chứng. Dùng: `python3 -B ma_tran_r11.py <clone git>`. Mỗi đột biến chạy trên bản sao `git ls-files`, trong một tiến trình mới. |
| `ma-tran-nguyen-mau.out` | `d33618efa5d4a3b73e81d8765094faa3beeb70117f5d5658eaad0b528e4dc08a` | Đầu ra trên nguyên mẫu (xem bên dưới). |
| `ma-tran-base.out` | `f1acc94acecdffe03076b2d01abb78bb0cec2fc480445392fad8c43ed1eb77d1` | Đầu ra trên base, dùng cho A0. |

## Phép đo

Cả hai phép đo dùng clone đầy đủ của `/home/user/tra-luat`, có `shallow=false`.

**Nguyên mẫu.** Clone `29c22f7d`, chạy `va.py`, rồi commit cục bộ thành `4ca625b4` (commit này không được đẩy).
- Thời gian: 13:45:50–14:01:02Z, 21-11-2026.
- `rc=0`. Dòng cuối: `TONG: 79 dot bien + doi chung, sai=0`.

**Base.** Clone `29c22f7d`.
- Thời gian: 14:01:10–14:17:21Z, 21-11-2026.
- `rc=1`, đúng như kỳ vọng.
- Các ca A0 ra đúng như đặc tả:
  - Ba lỗ cũ cho `do=` rỗng: `r11_size_only`, `r11_one_stale_ok`, `r11_missing_ok_narrow`.
  - `r11_ann_empty` cho `do=V4,V5,V6,V8,V9`.
  - `r11_duplicate` cho `do=V4,V5,V6,V8`.
- Trên base, 11 đột biến cùng lớp khác cũng lọt (`do=` rỗng).
- Script dừng bằng `AssertionError` ở ca `a7a_go_giu_do_dai`, vì chuỗi của bản vá không có trên base. Vì vậy các ca `a7*` không chạy trên base. Kết luận A0 không phụ thuộc các ca ấy.
