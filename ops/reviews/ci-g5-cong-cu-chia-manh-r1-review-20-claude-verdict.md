<!-- dieu phoi: luot 20 MOI (chu kho: luot 20 an cua 0842283 coi nhu khong co). Reviewer claude -p phien moi read-only, launcher run 19b5defc3d334d40844000a5124157a5, ma_thoat=0, 4651s; modelUsage do duoc: claude-opus-5-5 (+ claude-haiku-4-5 phu tro cua CLI). Assurance same_provider_approved. Noi dung duoi day la NGUYEN VAN VERDICT.md; hint patch nguyen van o tep .patch cung ten. -->

# Cross-review độc lập packet #668 r1 g3 — lượt 20
verdict: changes_requested
reviewed_sha: 0842283e86ef8f575b0c4423a340d8ac300198d0
reviewer: anthropic_claude qua claude -p (phiên mới, read-only) — assurance same_provider_approved (executor cũng là Claude)
tong_ket: 0 P1 · 1 P2 · 0 P3

Neo: `git -C cay-kho rev-parse HEAD` = `0842283e86ef8f575b0c4423a340d8ac300198d0`; `status --porcelain` rỗng (kiểm cả đầu
lẫn cuối lượt); SPEC sha256 = `dd2ada1b…516b15` khớp; baseline `nen` = `f8a7829cc44f…70b`. Mọi phép thử chạy trên bản sao
`/tmp/r20-head`, `/tmp/r20-base`, `/tmp/r20-mut`, `/tmp/r20-hint*`, `/tmp/r20-w4` (`cp -a`, cùng HEAD). Diff
f8a7829..HEAD: 5 tệp, +1967/−49, ≤ trần ~2.000; từ lượt 19 (`9aaeb03`) chỉ `ops/cong_cu_test.py` đổi
(`cfff4d2` +53, `0842283` +35). Không chạy CI, không commit/push, không gọi GitHub.

Hai miền năng lực được đo: nền CÓ symlink (container thật, `_CO_SYMLINK=True`, 413 đột biến) và nền EPERM
(`LD_PRELOAD` một shim libc 2 hàm `symlink`/`symlinkat` trả `EPERM`; `os.symlink` vẫn là
`builtin_function_or_method`, ném `PermissionError` — cùng miền syscall EPERM lượt 19 dùng, KHÔNG phải miền
xoá/đổi thuộc tính đã bị loại; `_CO_SYMLINK=False`, 410 đột biến).

| Lớp | Trạng thái | căn cứ đo |
|---|---|---|
| (1) workflow `ci.yml` + `loi_g5_workflow` | **đóng** | W2/W3 không đổi từ lượt 5 (`b6e0598`). `ci_dang_ky_test.py`: head 1025/1025 `TỔNG: ĐẠT` rc=0, base 938/938 rc=0; mọi dòng của base có mặt nguyên ở head, head thêm đúng 87 ca `p668-*` (delta 0 phần chung). `p637-A7-workflow-that-dat` (ci.yml thật ĐẠT) ĐỎ đúng. `actionlint .github/workflows/ci.yml` rc=0 cả hai cây. |
| (2) `main`/dispatcher | **đóng** | Lưới `_luoi_noi_main` 179 ô (135 k/N, 32 worker, 6 đường, 6 ô nền đỏ). 6 đột biến `f42_*` + 7 `f44_*` qua đủ 56 ca: mỗi cái CHỈ `t54` `giet_that`, đúng ô (ví dụ `f44_nen_n_luy_thua_2` → `noi-nen-2`, `noi-nen-3`, `noi-nen-do`; `f42_worker_du_tran_3` → `noi-du-w4..w16`). Răng F44 nằm ở chính ô `noi-nen-*` (6/7 `f44_*` chỉ bị các ô ấy bắt; `f44_nen_chi_tien_kiem` bị cả `manh_ca_do`/`manh_ca_loi` có sẵn bắt — dư nhưng không hại). A1 trọn: 89 đột biến đích `t54` đều `ok`. |
| (3) `_doc_che_do` | **đóng** (không đổi từ lượt 19) | A1 trọn: 50 đột biến đích `t53` đều `ok` bán kính 1. Không đo lại lưới 458 ô của lượt 19. |
| (4) `_van_tay` | **đóng** (không đổi từ lượt 19) | Như (3), qua A1; gom trên bộ mảnh thật khớp vân tay (GOM 8/8). |
| (5) phân hoạch / gom / CLI / bộ ghi | **đóng** | **A1 đo trọn** (xem H3): 8/8 mảnh rc=0, `--gop` rc=0, `GOM MẢNH 8/8`, 413 dòng `ok`, 0 dòng `ĐỎ`, `lỗi đột biến=0`. Yêu cầu riêng của chủ kho đạt (H4): bỏ / lặp mảnh, mảnh thiếu một đột biến, lặp bản ghi, chuyển mảnh, tên ngoài `DOT_BIEN`, gom với `DOT_BIEN` khác đều ĐỎ đúng thẻ. |
| (6) registry năng lực + đăng ký đột biến theo nền | **CHƯA ĐÓNG** — F45 | Chốt F43 (`_TEN_NANG_LUC` = hiệu hai ảnh) không có đột biến nào canh: gỡ về bộ lọc r19 ⇒ 56/56 qua ở cả hai nền. Bộ quan sát là HIỆU TẬP KHOÁ nên mù trước XOÁ / GHI ĐÈ tên có sẵn trong cửa sổ hai ảnh: 5 phép (True: r3/r4/r5; EPERM: r3f/r4f) sống 56/56. Mọi đột biến năng lực HIỆN CÓ (f24/f35/f37×4/f40×2/f41×4) đều giết đúng `t52` ở miền của nó. |
| (7) `t152`/hook (W4/W5) | **đóng** | `launcher_test.py`: 188/188, 1 bỏ qua (t62, Windows) ở CẢ hai cây, hỏng 0, delta 0. Phản chứng trên bản sao: đổi `AL_VER` của `gate-cong-cu` thành 1.7.6 ⇒ `t152 DO: ci.yml 5 cho phai khop 1.7.7: ['1.7.7', '1.7.6', …]`; xoá khối env ấy ⇒ `t152 DO: … ['1.7.7' ×4]`. Hook chỉ đổi chú thích 4→5. |

## Finding

### F45 (P2) — (6) registry năng lực — chốt F43 không có đột biến canh, và bộ quan sát hiệu-tập-khoá bỏ sót xoá/ghi đè trong cửa sổ đăng ký

Đây là lượt thứ 5 liên tiếp lớp này sinh finding (F37 → F38 → F39/F40 → F41 → F45). Cùng hình dạng ≥ 3 lần ⇒ §9 S3 /
lease `dieu_kien_dung` S3 bảo hỏi chủ kho. Reviewer chỉ ghi nhận điều kiện ấy, không tự quyết.

Đường vào của lớp, liệt kê trọn trước khi kết luận (grep mọi `DOT_BIEN[...] =`, `.pop`, `.update`, `del`, và mọi nhánh
module-level theo nền):
(a) THÊM tên trong khối `if _CO_SYMLINK` / `if not _CO_SYMLINK` — F43 bắt (r2 đo được).
(b) XOÁ tên có sẵn trong cửa sổ `_TRUOC_NANG_LUC … _TEN_NANG_LUC` — **không bắt**.
(c) GHI ĐÈ định nghĩa một tên có sẵn trong cửa sổ — **không bắt**.
(d) gỡ chính bộ quan sát F43 (quay về lọc theo oracle) — **không đột biến nào canh**.
(e) đăng ký theo nền NGOÀI cửa sổ — hiện KHÔNG có trong cây: chỉ có hai khối `_CO_SYMLINK`; nhánh module-level khác duy
nhất là `if sys.version_info >= (3, 12)` ở `_HINH_DANG_BAO_THAN_TRONG`, không chạm `DOT_BIEN`, và có từ baseline.
(f) đổi đầu dò `_do_co_symlink` — t52 so `_CO_SYMLINK` của con với cha; nhánh AttributeError là nợ chủ kho đã khai.
(g) đổi giá trị (neo/thay/đích) của tên năng lực — vòng bán kính tự đo (mỗi tên phải giết đích).

- **kịch bản hỏng:**
  1. (d) Một bản vá sau này đưa `kq["nang_luc"]` về lại
     `sorted(t for t in DOT_BIEN if t in _TEN_SL or t in _TEN_SL_FALSE)` (đúng mã r19). Bộ ca 56/56 xanh, bán kính 413
     xanh. Từ đó mọi tên có điều kiện MỚI nằm ngoài oracle lại lọt: đúng lỗ F41 mở lại mà không cổng nào đỏ. Vì registry
     hiện tại không có đột biến nào THÊM tên ngoài oracle, hai bộ quan sát tương đương trên cây này, nên việc gỡ chốt là
     vô hình. Executor khai "phản chứng F43 trên bản sao … t52 giet_that", nhưng phép ấy KHÔNG được đăng ký vào `DOT_BIEN`.
  2. (b)/(c) Trong khối `if _CO_SYMLINK:` có thêm `DOT_BIEN.pop("g668_gom_bo_tap")`, hoặc
     `DOT_BIEN["g668_gom_bo_tap"] = DOT_BIEN["f24_nhan_symlink"]`. Khi ấy, trên mọi nền có symlink (ubuntu-latest,
     windows-latest), chốt `G-tap` của gom thôi được đo, hoặc bị đo bằng một đột biến khác cùng đích. `_TEN_NANG_LUC`
     không đổi, nên `t52` qua; job gom tính theo `DOT_BIEN` của chính nó (cũng thiếu tên ấy) nên vẫn `GOM MẢNH 8/8`,
     `lỗi đột biến=0`. Một đột biến mất khỏi bán kính mà không có dòng ĐỎ nào.
- **bằng chứng chạy được** (harness `/tmp/r20-tools/mut.py`: nạp module của cây, thêm một mục vào `DOT_BIEN` rồi gọi
  CHÍNH `_do_ban_kinh` ⇒ trạng thái đủ 56 ca; in các ca khác `qua`):
  ```
  # nền CÓ symlink, cây 0842283
  r1_f43_loc_oracle        neo=1 ca=56  khac_qua={}                         # (d) gỡ F43 — SỐNG
  r2_them_ten_la           neo=1 ca=56  t52_: giet_that "đột biến symlink phải theo NĂNG LỰC …"   # (a) — F43 có răng với THÊM
  r3_xoa_trong_khoi_true   neo=1 ca=56  khac_qua={}                         # (b) — SỐNG
  r4_ghi_de_trong_khoi_true neo=1 ca=56 khac_qua={}                         # (c) — SỐNG
  r5_xoa_truoc_anh_sau     neo=1 ca=56  khac_qua={}                         # (b) vô điều kiện — SỐNG
  # nền EPERM, cây 0842283 (t51 tin_dung_gia + t46 bo_qua là nền, có cả ở đối chứng c0 và ở baseline)
  c0_doi_chung             THEM={}
  r1_f43_loc_oracle        THEM={}                                          # SỐNG
  r2_them_ten_la           THEM={t52_: giet_that}
  r3f_xoa_trong_khoi_false THEM={}                                          # SỐNG
  r4f_ghi_de_trong_khoi_false THEM={}                                       # SỐNG
  ```
  Cặp neo/thay nguyên văn (`/tmp/r20-tools/muts_reg.json`, `muts_eperm.json`; mọi neo đếm đúng 1 lần):
  - r1: `    kq["nang_luc"] = [_CO_SYMLINK, sorted(_TEN_NANG_LUC)]\n` → `    kq["nang_luc"] = [_CO_SYMLINK, sorted(t for t in DOT_BIEN if t in _TEN_SL or t in _TEN_SL_FALSE)]\n`
  - r3: `        DOT_BIEN[_ten] = ("ops/cong_cu_test.py", _tim, _thay, "TEP_TEST", _KEM_TEP_TEST, _CA_668[_ca])\nif not _CO_SYMLINK:\n` → chèn `    DOT_BIEN.pop("g668_gom_bo_tap")\n` trước `if not`
  - r4: cùng neo → chèn `    DOT_BIEN["g668_gom_bo_tap"] = DOT_BIEN["f24_nhan_symlink"]\n`
  - r5: `_TEN_NANG_LUC = frozenset(DOT_BIEN) - _TRUOC_NANG_LUC\n` → `DOT_BIEN.pop("g668_gom_bo_tap")\n` + neo
  - r3f/r4f: neo `    DOT_BIEN["f40_false_khong"] = (… _CA_668["t52_"])\n# F43` → chèn `    DOT_BIEN.pop("g668_gom_bo_tap")\n` / `    DOT_BIEN["g668_gom_bo_tap"] = DOT_BIEN["f40_false_khong"]\n` trước `# F43`
- **hint patch** (`goi-y-F45.patch`, +9/−2 ⇒ tổng packet +1976/−51, vẫn ≤ ~2.000; ĐÃ đo trên bản sao `/tmp/r20-hint`;
  chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit):
  ```diff
  +_D45 = 'if not _CO_SYMLINK:\n'   # F45: neo ĐỘC LẬP với dòng quan sát — gỡ chốt quan sát thì neo vẫn còn
   …(bảng _CA_668, trước f27_full_seed)
  +    ('f45_them_ten_la', 't52_', _D45, 'DOT_BIEN["f45_ten_la"] = DOT_BIEN["f45_xoa_ten"]\n' + _D45),
  +    ('f45_xoa_ten', 't52_', _D45, 'DOT_BIEN.pop("f45_them_ten_la")\n' + _D45),
  +    ('f45_ghi_de_ten', 't52_', _D45, 'DOT_BIEN["f45_them_ten_la"] = DOT_BIEN["f45_xoa_ten"]\n' + _D45),
   …
  -_TRUOC_NANG_LUC = frozenset(DOT_BIEN)
  +_TRUOC_NANG_LUC = dict(DOT_BIEN)   # ảnh cả tên VÀ định nghĩa
   …
  -_TEN_NANG_LUC = frozenset(DOT_BIEN) - _TRUOC_NANG_LUC
  +_TEN_NANG_LUC = frozenset(t for t in DOT_BIEN.keys() | _TRUOC_NANG_LUC.keys() if DOT_BIEN.get(t) != _TRUOC_NANG_LUC.get(t))
  ```
  Thiết kế: ba đột biến canh là VÔ ĐIỀU KIỆN (cùng một phép trên cả hai nền, không thêm tên có điều kiện nào, oracle
  `_TEN_SL`/`_TEN_SL_FALSE` giữ nguyên). Chúng được đăng ký TRƯỚC ảnh đầu. Chúng chèn một câu lệnh cột 0 ngay trước
  `if not _CO_SYMLINK:`, tức nằm trong cửa sổ, và neo KHÔNG nằm trên dòng quan sát. Nhờ vậy gỡ chốt quan sát thì đột
  biến canh SỐNG đúng lý do, chứ không chết vì mất neo. Bản nháp đầu của reviewer neo vào dòng quan sát và bị bỏ vì đúng
  lỗi này. Kết quả đo:
  ```
  # cây hint, nền CÓ symlink
  gate (CONG_CU_TEST_BAN_KINH=manh): cong_cu_test: 56/56 đạt · đột biến=416 (giao mảnh) · lỗi đột biến=0 · rc=0
  _TEN_NANG_LUC = 7 tên True như cũ (True) / 4 tên False như cũ (EPERM)
  f45_them_ten_la / f45_xoa_ten / f45_ghi_de_ten : ca=56, CHỈ t52_ giet_that "đột biến symlink phải theo NĂNG LỰC"
  r2/r3/r4/r5 (đo lại, neo quan sát mới)          : CHỈ t52_ giet_that
  # cây hint, nền EPERM
  f45_* ×3, r3f, r4f                               : CHỈ t52_ giet_that (ngoài nền t51/t46)
  f37_dk_luon_dung, f40_false_khong, f41_bo_f40_khong, f41_f40_luon_ra_ngoai : CHỈ t52_ giet_that (không hồi quy)
  gate EPERM: y hệt head EPERM (54/55, tiền kiểm alias bỏ qua, lỗi đột biến=2 từ tự kiểm song song — do môi trường, xem KHÔNG ĐO ĐƯỢC)
  # bậc hai — gỡ chốt, rồi chạy đột biến canh
  hint + r1 (quay về lọc oracle)      : f45_them_ten_la ca=56 khac_qua={}   ⇒ SỐNG ⇒ vòng bán kính ĐỎ ⇒ gỡ F43 bị lộ
  hint + r6 (quay về hiệu tập khoá)    : f45_xoa_ten, f45_ghi_de_ten khac_qua={} ⇒ SỐNG ⇒ gỡ F45 bị lộ (True và EPERM)
  ```
  Chưa đo: A1 trọn 8 mảnh trên cây hint (416 đột biến). Đã đo: gate 56/56, 3 đột biến mới giết đúng một ca trên cả hai
  nền, và 11 đột biến năng lực cũ không đổi hành vi.

## Hướng đã đo

**H1 — Bộ ca của cây, chế độ gate.**
giả thuyết: bản vá F43/F44 làm hồi quy bộ ca. · lệnh: `cd /tmp/r20-head && PYTHONDONTWRITEBYTECODE=1 CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` ·
output: `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0` … `SỐ LIỆU: ca=56 · đột biến=413 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT`, rc=0, 2m53s. ·
kết luận: **56/56**, không phải lỗi.

**H2 — Kiểm neo toàn registry.**
lệnh: nạp module, đếm `tim` trong tệp đích cho mọi mục `DOT_BIEN`. · output: 413 mục (True) / 410 (EPERM), 56 ca; neo ≠ 1
lần chỉ có `bn_khong_gap_noi_hang`(2), `bn_anh_chup_chi_dem_so`(2), `bn_bo_hang_byte`(3) trên `bash_nen.py`, đều là mục
có từ baseline (lượt 19 đã ghi); không có mục `tim == thay`. Neo `_NEN_M`/`_NEN_IN` (F44) và 4 neo F41 đều duy nhất. ·
kết luận: không phải lỗi.

**H3 — A1 trọn tại chỗ (nền có symlink).**
lệnh: `for k in 0..7: CONG_CU_TEST_TIEN_TRINH=3 CONG_CU_TEST_MANH=$k/8 CONG_CU_TEST_MANH_RA=/tmp/r20-shards/manh-$k.txt python ops/cong_cu_test.py`; rồi `python ops/cong_cu_test.py --gop /tmp/r20-shards`. ·
output: `manh 0..7 rc=0` (460–512 s/mảnh, 3 tiến trình); tệp mảnh 53×5 + 52×3 dòng (1 đầu + 52/51 BKCON = 413);
`gop rc=0`, `GOM MẢNH 8/8`, 413 dòng `  ok  `, 0 dòng `  ĐỎ`, `SỐ LIỆU GOM: ca=56 · đột biến=413 · lỗi đột biến=0`. ·
kết luận: A1 ĐẠT trên nền này. Mọi đột biến của cfff4d2 và 0842283 (`f41_*`×2 True, `f42_*`×6, `f44_*`×7) giết đúng
một ca trong vòng bán kính thật.

**H4 — Yêu cầu chủ kho: gom kiểm MỖI đột biến có ĐÚNG MỘT kết quả, theo `DOT_BIEN` của tiến trình gom.**
giả thuyết: gom nhận bộ mảnh thiếu/thừa/lặp. · đọc mã: `_gom_manh` tái tính `phan = [_phan_manh(k, n) …]` từ `DOT_BIEN`
của CHÍNH nó; `G-tap` (tập mảnh = 0..N−1), `G-dem` (đúng 1 tệp/mảnh), `G-phan-hoach` (phủ đúng, rời nhau), rồi
`_nhan_ket_qua_con(phan[k], …)` từ chối tên ngoài nhóm (c), tên lặp (d), thiếu (f); `G-tong` dự phòng. Tên do mảnh tự khai
không được tin (`g668_gom_tin_ten_cua_manh` giết t52). ·
lệnh: `/tmp/r20-tools/gom_variants.sh` — biến thể trên bản sao bộ mảnh THẬT của H3, gom bằng CLI `--gop` của head. ·
output:
```
v0_goc                rc=0 :: GOM MẢNH 8/8 :: SỐ LIỆU GOM: ca=56 · đột biến=413 · lỗi đột biến=0
v1_bo_manh            rc=1 :: ĐỎ gom [G-tap]: tập mảnh [0, 1, 2, 4, 5, 6, 7] ≠ 0..7
v2_lap_manh           rc=1 :: ĐỎ gom [G-dem]: mảnh 3 có 2 tệp: ['manh-3.txt', 'manh-3b.txt']
v3_manh_thieu_mot     rc=1 :: ĐỎ gom [G-ban-ghi]: mảnh 5 (manh-5.txt): thiếu kết quả: ['t14_advisory_keo_tong']
v4_lap_ban_ghi        rc=1 :: ĐỎ gom [G-ban-ghi]: mảnh 5 (manh-5.txt): tên lặp: 't14_advisory_keo_tong'
v5_chuyen_manh        rc=1 :: ĐỎ gom [G-ban-ghi]: mảnh 5 (manh-5.txt): thiếu kết quả: ['t14_advisory_keo_tong']
v6_ten_ngoai_dot_bien rc=1 :: ĐỎ gom [G-ban-ghi]: mảnh 5 (manh-5.txt): tên ngoài nhóm: 'zz_khong_co_trong_dot_bien'
v7 gom trên nền EPERM (DOT_BIEN 410, mảnh đo với 413) rc=1 :: ĐỎ gom [G-ban-ghi]: mảnh 0 (manh-0.txt): tên ngoài nhóm: 'f37_bo_f24'
```
Phản chứng trong cây (t52): `thieu`→G-tap, `thua`/`trung`→G-dem/G-tap, `xoa`→G-ban-ghi, `chuyen`→G-ban-ghi; đột biến
riêng `g668_gom_bo_tap`, `g668_gom_bo_dem`, `g668_gom_bo_phan_hoach`, `g668_gom_tin_ten_cua_manh` đều `ok` trong A1. Ba
chốt (c)/(d)/(f) của bộ nhận dùng chung không có đột biến bán kính (như baseline). Răng của chúng nằm ở tự kiểm song
song trong `main` (`_GIA_BAT_THUONG` c/d/f → `tự kiểm song song (4c/4d/4f)`), chạy ở job `gate`. ·
kết luận: **thoả** yêu cầu chủ kho (nợ "c" của #570); không phải lỗi. Riêng v7 cho thấy: nếu runner mảnh và runner gom
khác năng lực symlink thì gom ĐỎ (fail-closed). Thẻ lỗi lúc ấy là `G-ban-ghi` "tên ngoài nhóm", không nói thẳng "lệch
năng lực"; đây chỉ là chẩn đoán, không đổi kết luận nên không ghi finding.

**H5 — Đột biến bản vá cfff4d2/0842283, từng cái qua đủ 56 ca (nền có symlink).**
lệnh: `mut.py` với mục có sẵn. · output (chỉ ca khác `qua`):
`f42_k_mod_8`, `f42_n_luy_thua_2`, `f42_ra_strip`, `f42_ra_lower`, `f42_worker_manh_tran_3`, `f42_worker_du_tran_3`,
`f44_nen_k_mod_8`, `f44_nen_n_luy_thua_2`, `f44_nen_ra_strip`, `f44_nen_ra_lower`, `f44_nen_ten_n8`,
`f44_nen_in_k_mod_8`, `f44_nen_chi_tien_kiem` → mỗi cái CHỈ `t54_ giet_that` "`main` nối SAI …" với khoá ô đúng chiều bị
phá. `f41_bo_f40_luon`, `f41_f40_khong_ra_ngoai`, `f40_false_luon`, `f37_bo_f24`, `f37_bo_f35`, `f37_dk_dao` → CHỈ `t52_`
"đột biến symlink phải theo NĂNG LỰC". `f24_nhan_symlink` → CHỈ t52 (thẻ G-…), `f35_writer_broken_link` → CHỈ t52 (bộ
ghi). Không có cái nào chết vì `AttributeError`/lỗi vô can. ·
kết luận: chốt F41/F42/F44 có răng, đúng lý do.

**H6 — Như H5, nền EPERM.**
output: đối chứng `c0` chỉ có `t51 tin_dung_gia` + `t46 bo_qua` (nền; lượt 19 đo cả hai ở baseline). `f37_dk_dao`,
`f37_dk_luon_dung`, `f40_false_khong`, `f41_bo_f40_khong`, `f41_f40_luon_ra_ngoai` → thêm đúng `t52_ giet_that`. ·
kết luận: phía False của F41 có răng.

**H7 — Registry năng lực: mọi đường vào.** Xem F45 (a)–(g). · kết luận: **LỖI P2 (F45)**.

**H8 — Hint F45 hai chiều, cả bậc hai.** Xem F45. · kết luận: hint đóng (b)/(c)/(d) trên cả hai nền, không đỏ oan, không
thêm tên có điều kiện.

**H9 — A7 delta.**
- `ruff check --select F` trên W1/W3/W4: head 6 F841 (5 `launcher_test.py`, 1 `cong_cu_test.py` `ci`), base y hệt; `diff` rỗng ⇒ delta 0.
- `actionlint .github/workflows/ci.yml`: rc=0 ở cả hai.
- `ci_dang_ky_test.py`: head 1025/1025, base 938/938, delta phần chung 0 (H-lớp 1).
- `launcher_test.py`: 188/188, 1 bỏ qua cả hai, delta 0; `t152` có răng (lớp 7).
- `ops/lease_publish_test.py`: 185/187 ở CẢ hai vế. Hai ca `t137_M9_workflow_admission…` và `t159_t137_can_do_DU…` ĐỎ
  giống hệt nhau ở head và base (môi trường container), tức delta 0. `t24`/`t31`/`t35`/`t161`/`t162` QUA ở cả hai.
kết luận: A7 delta 0.

**H10 — Hình dạng lỗi lặp.** Lớp (6) sinh finding 5 lượt liền. Lần này reviewer đã liệt kê hết 7 đường vào trước khi
kết luận, thay vì chỉ đo chỗ executor vá. Lỗ còn lại nằm ở (b)/(c)/(d). (e) hiện không tồn tại trong cây. (f) là nợ đã
khai. Hint ở F45 tách chốt quan sát khỏi neo của đột biến canh, để lần gỡ chốt kế tiếp bị bắt đúng lý do.

## KHÔNG ĐO ĐƯỢC
- A1 trọn trên nền EPERM (410 đột biến): chỉ đo 5 phép tự soạn + 5 đột biến có sẵn + 8 phép hint. Gate trên nền EPERM ĐỎ
  vì môi trường ở CẢ head lẫn hint, y hệt nhau: `t51` ĐỎ ở nền, tiền kiểm `python_alias_behavior_test` bỏ qua vì shim
  chặn cả symlink của chính nó, tự kiểm song song (1) lệch ⇒ `lỗi đột biến=2`. Nên không có phép đo "gate EPERM xanh".
- A1 trọn trên cây hint (416 đột biến, 8 mảnh). Chỉ đo gate 56/56 và từng đột biến mới / liên quan qua 56 ca.
- A5 (hành vi cũ, vắng mọi biến, bán kính đủ trong một tiến trình): không chạy theo phân công. A1 trọn thay thế một phần
  về bán kính, không thay phần in bảng của nhánh `du`.
- Lưới 458 ô `_doc_che_do` / 275 ô HEAD của lượt 19: không đo lại. Hai lớp không đổi từ `9aaeb03`; chỉ đo qua A1.
- Đường Windows của mảnh/gom; hành vi `upload-artifact`/`download-artifact` thật; thời gian runner (A9); danh tính người
  ký (#566); effort executor.
- Nền VẮNG thuộc tính `os.symlink` (nhánh AttributeError): chủ kho đã loại (F39), không mô phỏng.
- Không soạn payload ký tự điều khiển/ẩn hay đường thoát khỏi cây; hướng BOM giữa lệnh `run` do lượt 19 mô tả vẫn chưa ai
  dựng, và lượt này cũng không dựng.
