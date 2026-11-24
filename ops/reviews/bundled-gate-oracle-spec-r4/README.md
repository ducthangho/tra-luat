# Hiện vật đặc tả BUNDLED-GATE-ORACLE-FRESHNESS r4

Packet `wp433` revision 11, Issue #433. Thư mục này là hiện vật dev-side, không vào gói phát hành. Hiện vật của r2 và r3 giữ nguyên ở các thư mục bên cạnh.

| tệp | sha256 | vai |
|---|---|---|
| `va.py` | `fc7486b9391c83499e5ff4affeae084ba6cb2894275c8673260a55378870b466` | Bản vá chuẩn cho W1 (M1, M2). Gồm chín thay thế, mỗi thay thế khớp đúng một lần trên base `29c22f7d`. Dùng: `python3 va.py <gốc cây>` |
| `ma_tran_r11.py` | `2e064306ed99829bccaaaf331a7186bb592b9a775320594b690bceebbc68034f` | **Ma trận A2, tự đủ, có thẩm quyền.** Gồm 115 đột biến cộng đối chứng: 49 g5, 33 `r11_`, 13 `no_` (nợ, đích rỗng) và 20 `a7_`. Đích khai sẵn, kiểm `DON_DICH`. Dùng: `python3 -B ma_tran_r11.py <clone git>` |
| `doi_chieu_don_dieu.py` | `2b823806a45ba7470cb3e0cbc5fd6b1e54fe9810b94e29851c16416a4dba9fd7` | Phép đo A6. Dùng: `python3 doi_chieu_don_dieu.py <ma trận trên base> <ma trận trên C>` |
| `gen_ma_tran.py` | `7b7afa08b40cff3d07ffafa86bbd4ad73fcc0056cb84594f85818a0baa24f391` | Chỉ để truy nguồn: đây là script sinh `ma_tran_r11.py`. Script đọc đầu vào theo đường dẫn scratch của phiên soạn. Đầu vào: g5 `ma_tran_dot_bien.py` @ `bf38a110` (sha256 `fcfbc7fb…79b3`), `probe_review_r1.py`, `rv3_muts*.py` |
| `probe_review_r1.py` | `7940fd2ca6ab78ed0c368a24ff8cdacf3a452aa7462d3820fa463f98620aa24f` | Đột biến của review r1. Chỉ để truy nguồn |
| `rv3_muts.py` · `rv3_muts2.py` | `a5460db1…c6dd` · `5667351a…96d4` | Đột biến của review r3. Chỉ để truy nguồn |
| `ma-tran-nguyen-mau.out` | `f3d11c1542f6e57aef41cb95a3173b13abd5c5aa8196ad4b011b6dbbd0ab07c9` | Đầu ra ma trận trên nguyên mẫu |
| `ma-tran-base.out` | `c0765e0fc78adf94f5662431f863f5a99f51f969044d305df8eac8814f078504` | Đầu ra ma trận trên base |
| `dinh-danh.txt` | `579950df9a981da70bbce54a399e57e1a25764c98d0ee6ff379e1b1179c2effa` | Định danh hai clone |

## Phép đo (21-11-2026)

Hai clone đầy đủ được dựng trong MỘT lệnh, cả hai `shallow=false`:
- `nen` = `29c22f7d`;
- `sau` = `29c22f7d` + `va.py`, commit cục bộ `223d938a` (không đẩy).

Hai lượt ma trận chạy song song, cùng bắt đầu lúc 15:53:46Z.

**Nguyên mẫu (`sau`).** Kết thúc 16:17:46Z.
- `rc=0`.
- `DON_DICH: 32/32`.
- `TONG: 115 dot bien + doi chung, sai=0`.

**Base (`nen`).** Kết thúc 16:15:55Z.
- `rc=1`, `sai=48`, đúng như kỳ vọng.
- A0 khớp cả năm ca:
  - `r11_size_only`, `r11_one_stale_ok` và `r11_missing_ok_narrow` cho `do=` rỗng;
  - `r11_ann_empty` cho `do=V4,V5,V6,V8,V9`;
  - `r11_duplicate` cho `do=V4,V5,V6,V8`.
- 20 ca `r11_` cho `do=` rỗng.
- Các ca `a7_` không áp được trên base. Điều này đúng như thiết kế.

**A6.** Lệnh: `doi_chieu_don_dieu.py ma-tran-base.out ma-tran-nguyen-mau.out`.
- `rc=0`.
- Kết quả: `DON_DIEU: base giet 62 ca do duoc; C yeu di 0; C thieu 0`.
- Phép đo có răng: sửa một đầu ra giả để `r11_m1` có `do=` rỗng thì script trả `rc=1` và in `YEU_DI r11_m1_chi_so_tien_to`. Phép thử này chạy trên đầu ra r3.
