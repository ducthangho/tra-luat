# Hiện vật đặc tả BUNDLED-GATE-ORACLE-FRESHNESS r5

Packet `wp433` revision 11, Issue #433. Thư mục này là hiện vật dev-side, không vào gói phát hành. Hiện vật của r2–r4 giữ nguyên ở các thư mục bên cạnh.

| tệp | sha256 | vai |
|---|---|---|
| `va.py` | `e909f641791c739e15e4e2112ccda687af2718daffff205959175bc3f6ecd110` | Bản vá chuẩn cho W1 (M1, M2). Mười một thay thế, mỗi thay thế khớp đúng một lần trên base `29c22f7d`. Dùng: `python3 va.py <gốc cây>` |
| `ma_tran_r11.py` | `9314f531cb683d25965deda574a39f60b2cc02777ca389358b0b38e2405d9713` | **Ma trận A2, tự đủ, có thẩm quyền.** 125 đột biến cộng đối chứng: 49 g5, 43 `r11_`, 13 `no_` (nợ, đích rỗng), 20 `a7_`. Dùng: `python3 -B ma_tran_r11.py <clone git>` |
| `doi_chieu_don_dieu.py` | `95671804c21af77486a03da0e7e3f5e7911faccda9578ef0208c8424fc3b890b` | Phép đo A6. Chỉ phủ các ca CỦA MA TRẬN. Ca văng của base được tính là "base giết". Dùng: `python3 doi_chieu_don_dieu.py <ma trận trên base> <ma trận trên C>` |
| `gen_ma_tran.py` | `f34fcf6f071596095a64d4a3513dbfc631b1e8cb1f96205a675bf25524320191` | Chỉ để truy nguồn: script sinh `ma_tran_r11.py`. Script đọc đầu vào theo đường dẫn scratch của phiên soạn. Đầu vào là g5 `ma_tran_dot_bien.py` @ `bf38a110` (sha256 `fcfbc7fb…79b3`) cùng các tệp đột biến của reviewer dưới đây |
| `probe_review_r1.py` · `rv3_muts.py` · `rv3_muts2.py` · `rv4_san.py` | `7940fd2c…`, `a5460db1…`, `5667351a…`, `6743f2dd…` | Đột biến của các lượt review r1, r3 và r4. Chỉ để truy nguồn |
| `ma-tran-nguyen-mau.out` | `30b9e906bc77465ad0db3901f6664c181654f0f8db9eebfe0e5d65a7455ae038` | Đầu ra ma trận trên nguyên mẫu |
| `ma-tran-base.out` | `becf0c2c6f3d2c68a4eafae0c90c09867b533a775b441ff194650988d9e70630` | Đầu ra ma trận trên base |
| `dinh-danh.txt` | `609566a8610c8af2d495de4cf40f895eeeac716368be363f77ffc5f0dd85766a` | Định danh của hai clone |

## Phép đo (21-11-2026, clone dựng trên đĩa)

Hai clone đầy đủ được dựng trong MỘT lệnh, cả hai `shallow=false`:
- `nen` = `29c22f7d`;
- `sau` = `29c22f7d` + `va.py`, commit cục bộ `dfa27d56` (không đẩy).

Hai lượt chạy song song, cùng bắt đầu lúc 16:56:16Z.

**Nguyên mẫu (`sau`).** Kết thúc 17:20:40Z, `rc=0`.
- `DON_DICH: 32/32`.
- `TONG: 125 dot bien + doi chung, sai=0`.

**Base (`nen`).** Kết thúc 17:18:31Z, `rc=1`, `sai=55`, đúng như kỳ vọng.
- A0 khớp cả năm ca:
  - `r11_size_only`, `r11_one_stale_ok` và `r11_missing_ok_narrow` cho `do=` rỗng;
  - `r11_ann_empty` cho `do=V4,V5,V6,V8,V9`;
  - `r11_duplicate` cho `do=V4,V5,V6,V8`.
- 20 ca `r11_` cho `do=` rỗng.
- Bảy ca `r11_rv4_s*`: base giết qua V5/V6, C giết qua V8.

**A6.** `rc=0`, kết quả: `DON_DIEU: base giet 72 ca do duoc; C yeu di 0; C thieu 0`.
- Răng của phép đo kiểm bằng hai đầu ra giả. Ca base có `do=` thì cho `YEU_DI` (kiểm lúc r4). Ca base văng (`VANG`) mà C để sống cũng cho `YEU_DI`, `rc=1`.
