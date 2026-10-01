<!-- dieu phoi: reviewer claude -p phien moi read-only, launcher run bbab3c0006724b2fa0e1caa318e84872, ma_thoat=0, 4433s; modelUsage do duoc: claude-opus-5-5 (+ claude-haiku-4-5 phu tro cua CLI). Assurance same_provider_approved. Noi dung duoi day la NGUYEN VAN VERDICT.md. -->

# Cross-review độc lập packet #668 r1 g3 — lượt 21
verdict: approved
reviewed_sha: cc78b33bd04d158d92c14eca01ad58d6d1dfe146
reviewer: anthropic_claude qua claude -p (phiên mới, read-only) — assurance same_provider_approved (executor cũng là Claude)
tong_ket: 0 P1 · 0 P2 · 0 P3

Neo đầu lượt và cuối lượt: `git -C cay-kho rev-parse HEAD` = `cc78b33bd04d158d92c14eca01ad58d6d1dfe146`,
`status --porcelain` rỗng. `nen` = `f8a7829cc44f…70b`, sạch. SPEC sha256 = `dd2ada1b…516b15`, khớp. Diff f8a7829..HEAD:
5 tệp, +1974/−49, dưới trần ~2.000. Từ `0842283` chỉ `ops/cong_cu_test.py` đổi (+9/−2). Tệp này **trùng từng byte** với
cây hint lượt 20 (`diff /tmp/r20-hint/ops/cong_cu_test.py head/ops/cong_cu_test.py` rỗng), tức executor áp NGUYÊN hint.
Mọi phép thử chạy trên bản sao `/tmp/r20-r21/{head,base,b2-*}` (`cp -a`; cây bậc hai được commit cục bộ trong bản sao
để sạch). Không chạy CI, không commit/push vào cây ứng viên, không gọi GitHub.

Hai nền năng lực:
- CÓ symlink: container thật, `_CO_SYMLINK=True`, 416 đột biến.
- EPERM: dựng lại y hệt lượt 20 — shim `LD_PRELOAD` 2 hàm `symlink`/`symlinkat` trả `EPERM`. `os.symlink` vẫn là
  `builtin_function_or_method` và ném `PermissionError`. `_CO_SYMLINK=False`, 413 đột biến.

| Lớp | Trạng thái | căn cứ đo |
|---|---|---|
| (1) workflow `ci.yml` + `loi_g5_workflow` | **đóng** | W2/W3 không đổi từ lượt 20. `ci_dang_ky_test.py`: head `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT` rc=0; base 938/938 rc=0. `comm` trên dòng đã sort: base có đúng 1 dòng head không có, là chính dòng tổng 938/938; head thêm 88 dòng (87 ca `p668-*` và dòng tổng 1025) ⇒ delta phần chung 0. `actionlint .github/workflows/ci.yml` rc=0 ở cả hai cây. |
| (2) `main`/dispatcher | **đóng** (không hồi quy) | Code không đổi. A1 trọn (H3): mọi `f42_*`/`f44_*` và các đột biến đích `t54` đều `ok`. |
| (3) `_doc_che_do` | **đóng** (không hồi quy) | Code không đổi. A1 trọn: các đột biến đích `t53` đều `ok`. |
| (4) `_van_tay` | **đóng** (không hồi quy) | Code không đổi. Gom trên bộ mảnh thật khớp vân tay: `GOM MẢNH 8/8`. |
| (5) phân hoạch / gom / CLI / bộ ghi | **đóng** (không hồi quy) | **A1 đo trọn**: 8/8 mảnh rc=0, `--gop` rc=0, `GOM MẢNH 8/8`, 416 dòng `  ok  `, 0 dòng `  ĐỎ`, `SỐ LIỆU GOM: ca=56 · đột biến=416 · lỗi đột biến=0`. Mỗi tệp mảnh 53 dòng (1 đầu + 52 BKCON; 8×52 = 416). |
| (6) registry năng lực + đăng ký theo nền | **đóng** | Liệt kê lại trọn các đường vào (a)–(g) và thêm 4 hướng mới (h)–(k) (H4). Bản vá đóng (b)/(c)/(d) trên CẢ HAI nền. Ma trận bậc hai (H5) cho thấy mỗi đột biến canh có răng riêng. Không đường nào trong cửa sổ để lọt một thay đổi lặng lẽ. Hai đường ngoài cửa sổ (n3/n4) là giới hạn thiết kế do chủ kho chốt ở F39 ("không nạp lại, không mô phỏng"), không do bản vá mở ra (H6). |
| (7) `t152`/hook (W4/W5) | **đóng** | `launcher_test.py`: `188/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 0)` rc=0 ở CẢ hai cây (bỏ qua t62, Windows) ⇒ delta 0. W4/W5 không đổi từ lượt 20. Phản chứng `t152` của lượt 20 không đo lại (xem KHÔNG ĐO ĐƯỢC). |

## Finding

Không có finding. Vì sao từng lớp đóng: xem bảng trên và các hướng H1–H9. Riêng lớp (6), là lớp đã sinh finding 5 lượt
liền, căn cứ đóng như sau:
- 3 đột biến canh mới giết ĐÚNG MỘT ca (`t52`) và đúng lý do trên cả hai nền, cả trong vòng bán kính thật (A1).
- Gỡ từng thành phần của chốt F43/F45 thì ít nhất một đột biến canh SỐNG, nên vòng bán kính ĐỎ.
- Không hướng mới nào tạo được thay đổi lặng lẽ trong cửa sổ quan sát.

## Hướng đã đo (mỗi hướng: giả thuyết · lệnh · output · kết luận)

**H1 — Bộ ca của cây, chế độ gate.**
giả thuyết: bản vá F45 làm hồi quy bộ ca. · lệnh: `cd /tmp/r20-r21/head && PYTHONDONTWRITEBYTECODE=1 CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` ·
output: `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0` … `SỐ LIỆU: ca=56 · đột biến=416 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT`, rc=0, `real 2m54s`. ·
kết luận: **56/56**, không phải lỗi.

**H2 — A7 delta.**
- `ruff check --select F` trên `ci_dang_ky_test.py`, `launcher_test.py`, `cong_cu_test.py`: 6 F841 ở mỗi cây, gồm 5 ở
  `launcher_test.py` và 1 `ci` ở `cong_cu_test.py`. Sau khi bỏ số dòng, hai danh sách giống hệt (chỉ lệch số dòng: 6062↔6061,
  2606↔2029) ⇒ delta 0. Commit khai "8 trước / 8 sau"; tập tệp tôi chạy có thể khác, nhưng delta đều bằng 0.
- `actionlint` rc=0 ở cả hai. `ci_dang_ky_test` và `launcher_test`: xem lớp (1) và (7).
kết luận: A7 delta 0.

**H3 — A1 trọn tại chỗ (nền có symlink).**
lệnh: 4 cặp mảnh chạy song song, mỗi mảnh `CONG_CU_TEST_TIEN_TRINH=2 CONG_CU_TEST_MANH=$k/8 CONG_CU_TEST_MANH_RA=/tmp/r20-r21/shards/manh-$k.txt python ops/cong_cu_test.py`; rồi `python ops/cong_cu_test.py --gop /tmp/r20-r21/shards`. ·
output: `manh 0..7 rc=0` (~760 s mỗi cặp), mỗi mảnh `cong_cu_test: 56/56 đạt`; `gop rc=0`;
`GOM MẢNH 8/8` / `BÁN KÍNH ĐỘT BIẾN (416 đột biến, mỗi ca đúng một; 8 mảnh):` / 416 dòng `ok`, 0 dòng `ĐỎ` /
`SỐ LIỆU GOM: ca=56 · đột biến=416 · lỗi đột biến=0`. Ba dòng mới:
```
  ok  f45_them_ten_la → giết đúng 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' · bán kính 1/56
  ok  f45_xoa_ten → giết đúng 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' · bán kính 1/56
  ok  f45_ghi_de_ten → giết đúng 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' · bán kính 1/56
```
kết luận: A1 ĐẠT trên nền này. Lời khai của commit (A1 416/416) khớp với đo độc lập. Không lớp nào hồi quy.

**H4 — Lớp (6): liệt kê trọn các đường vào, đo từng đường.**
Cách liệt kê: grep mọi `DOT_BIEN[...] =`, `.pop/.update/.setdefault/.clear/.popitem`, `del DOT_BIEN`, `DOT_BIEN =` và mọi câu
lệnh điều khiển ở cột 0 (`if/for/try/while/with`). Mutation của `DOT_BIEN` chỉ nằm ở: literal dòng 469; vòng bảng `_CA_668`
(dòng 1869–2256, vô điều kiện); vòng `f36_` (2259); và hai khối `if _CO_SYMLINK:` / `if not _CO_SYMLINK:` (7424–7453), nằm
giữa ảnh `_TRUOC_NANG_LUC` (7422) và dòng quan sát (7456). Các `if`/`try`/`for` cột 0 ở 2966–2977 nằm trong chuỗi
`_BASH_NEN_GIA_DUNG`; `if sys.version_info >= (3, 12)` (3952) không chạm `DOT_BIEN` và có từ baseline.

Thành phần registry, đo bằng `tools/insp.py`, nạp module thật: mọi giá trị là tuple 6 phần tử và mọi phần tử là `str`.
`_KEM_TEP_TEST` là tuple str. Do đó phép `!=` ở dòng quan sát là so sánh GIÁ TRỊ thuần; không có phần tử khả biến hay phần
tử so theo danh tính. Ba `f45_*` ở chỉ số 398–400 < 409 (= `len(_TRUOC_NANG_LUC)`) và nằm trong ảnh trước, nên KHÔNG vào
`_TEN_NANG_LUC`. `_TEN_NANG_LUC` = đúng 7 tên True (nền symlink) / đúng 4 tên False (EPERM). Neo `'if not _CO_SYMLINK:\n'`
(dùng chung cho `f45_*`, `f40_false_luon`, `f40_false_khong`) xuất hiện đúng 1 lần. Neo ≠ 1 chỉ có 3 mục `bn_*` của
`bash_nen.py`, đều có từ baseline.

Harness `/tmp/r20-r21/tools/mut.py` (bản chép của harness lượt 20, đã đọc lại): nạp module của cây, thêm một mục vào
`DOT_BIEN`, rồi gọi CHÍNH `_do_ban_kinh`, cho trạng thái đủ 56 ca; `khac_qua` liệt kê các ca khác `qua`. `tools/nl.py`: áp
đột biến lên bản sao tạm, nạp module, in `_TEN_NANG_LUC` của con. Neo và thay nguyên văn nằm trong
`/tmp/r20-r21/tools/muts.json` và `muts_f.json`. Mọi neo đếm đúng 1 lần (có assert).

Nền CÓ symlink (tất cả `neo=1 ca=56`):
```
đường  tên                              _TEN_NANG_LUC của con                khac_qua
—      c0_doi_chung (đổi chú thích)     7 tên True                           {}
(a)    f45_them_ten_la                  7 + f45_ten_la                       t52_ giet_that "đột biến symlink phải theo NĂNG LỰC …"
(b)    f45_xoa_ten                      7 + f45_them_ten_la                  t52_ giet_that (như trên)
(c)    f45_ghi_de_ten                   7 + f45_them_ten_la                  t52_ giet_that (như trên)
(b)    r3_xoa_trong_khoi_true           7 + g668_gom_bo_tap                  t52_ giet_that   ← lượt 20 SỐNG, nay bị bắt
(c)    r4_ghi_de_trong_khoi_true        7 + g668_gom_bo_tap                  t52_ giet_that   ← lượt 20 SỐNG, nay bị bắt
(b)    r5_xoa_truoc_quan_sat            7 + g668_gom_bo_tap                  t52_ giet_that   ← lượt 20 SỐNG, nay bị bắt
—      f40_false_luon (cùng neo _D45)   —                                    t52_ giet_that   (không hồi quy)
—      f41_bo_f40_luon                  —                                    t52_ giet_that   (không hồi quy)
(h)    n1_anh_la_bi_danh (_TRUOC=DOT_BIEN, không chép)  []                   t52_ giet_that
(h)    n1b_anh_chi_khoa (dict.fromkeys) toàn bộ 416 tên                      t52_ giet_that
(i)    n2_them_gia_tri_None (vô đk)     7 (KHÔNG thấy 'zz_gia_tri_none')     t52_ tin_dung_gia "cửa --tu-kiem-gom hỏng: rc=1", t54_ tin_dung_gia "cửa --tu-kiem-main hỏng"
(i)    n2b_them_None_co_dk (khối True)  7 (KHÔNG thấy)                       như n2
(f)    n5_dau_do_luon_false             CO_SYMLINK=False, 4 tên False        t52_ giet_that "kịch bản hỏng KHÔNG bị đúng chốt bắt …"
(j)    n6_xoa_roi_them_lai_cung_gia_tri 7                                    {}   (no-op: cùng giá trị; chỉ đổi thứ tự khoá)
(e)    n3_ngoai_cua_so_sau (`if _CO_SYMLINK: DOT_BIEN.pop("g668_gom_bo_tap")` SAU dòng quan sát)  7   {}
(e)    n4_ngoai_cua_so_truoc (`if _do_co_symlink(): DOT_BIEN.pop(…)` TRƯỚC ảnh)                    7   {}
(d)    d1_quan_sat_loc_oracle / d6_hieu_tap_khoa / d7_hieu_doi_xung_khoa / d8_chi_khoa_sau (gỡ chốt, dùng làm cây bậc hai)   {} (tương đương trên cây này, như mong)
```
Nền EPERM: đối chứng `c0_doi_chung` cho `t51_ tin_dung_gia` (PermissionError) + `t46_ bo_qua`. Đây là NỀN, có ở MỌI dòng
dưới; bảng chỉ ghi phần THÊM so với nền:
```
f45_them_ten_la / f45_xoa_ten / f45_ghi_de_ten        + t52_ giet_that "đột biến symlink phải theo NĂNG LỰC (mong [False, …"
r3f_xoa_trong_khoi_false / r4f_ghi_de_trong_khoi_false + t52_ giet_that   ← lượt 20 SỐNG, nay bị bắt
r5_xoa_truoc_quan_sat                                 + t52_ giet_that
f37_dk_luon_dung / f40_false_khong / f41_bo_f40_khong / f41_f40_luon_ra_ngoai   + t52_ giet_that (không hồi quy)
n1_anh_la_bi_danh                                     + t52_ giet_that
n2f_them_None_khoi_false                              + t52_ tin_dung_gia, t54_ tin_dung_gia (giàn giáo)
n3f_ngoai_cua_so_sau_false                            {} thêm (đường (e))
d1 / d6 / d7 / d8                                     {} thêm (tương đương, như mong)
```
kết luận từng đường:
- (a) THÊM tên trong cửa sổ: bị bắt, cả hai nền.
- (b) XOÁ: đóng, cả hai nền (r3/r5/r3f và `f45_xoa_ten`).
- (c) GHI ĐÈ bằng giá trị khác: đóng, cả hai nền (r4/r4f và `f45_ghi_de_ten`).
- (d) gỡ bộ quan sát: có đột biến canh (H5).
- (f) đổi đầu dò: `t52` bắt vì năng lực của con ≠ của cha.
- (g) đổi neo/thay/đích của tên năng lực: vòng bán kính tự đo (A1 trọn: mọi tên năng lực `ok`).
- (h) phá ẢNH TRƯỚC (bí danh, hoặc chỉ giữ khoá): ồn, `t52` ĐỎ.
- (i) THÊM tên với giá trị `None` là đường duy nhất bộ quan sát `!=`/`.get` không thấy (`None == .get(tên vắng)`). Hậu quả
  đã đo: không lặng. Hai cửa tự kiểm `--tu-kiem-gom`/`--tu-kiem-main` sập, nên `t52`/`t54` `tin_dung_gia`. Trên cây có
  sẵn n2b (`/tmp/r20-r21/b2-n2b`), gate chạy ra `cong_cu_test: 54/56 đạt` … `lỗi đột biến=1`, rc=1. Nghĩa là một mục
  `None` làm cổng đỏ ở mọi nền chứ không rút một đột biến ra lặng lẽ ⇒ **không phải finding**.
- (j) xoá rồi thêm lại CÙNG giá trị: no-op về hành vi, chỉ đổi thứ tự khoá, tức đổi phân mảnh `i % N`. Gom tính lại phân
  hoạch từ `DOT_BIEN` của chính nó (lượt 20 H4), nên không có hậu quả ⇒ không phải finding.
- Tương tác của 3 đột biến canh với nhau và với `f40_false_luon`/`f40_false_khong` cùng neo: mỗi đột biến được áp RIÊNG.
  `thay` của `f45_*` giữ nguyên `_D45` ở cuối, nên cây đột biến vẫn còn đúng một `if not _CO_SYMLINK:`. Cả 5 đột biến đều
  giết đúng `t52` ở miền của mình, trong mut.py lẫn trong A1 ⇒ không có tương tác hại.

**H5 — Đột biến bản vá, bậc hai: gỡ chốt rồi chạy đột biến canh (cả hai nền).**
Cây bậc hai là bản sao head, sửa ĐÚNG MỘT dòng rồi commit cục bộ:
- d1: `    kq["nang_luc"] = [_CO_SYMLINK, sorted(_TEN_NANG_LUC)]\n` → `    kq["nang_luc"] = [_CO_SYMLINK, sorted(t for t in DOT_BIEN if t in _TEN_SL or t in _TEN_SL_FALSE)]\n` (gỡ F43)
- d6: dòng quan sát → `_TEN_NANG_LUC = frozenset(DOT_BIEN) - frozenset(_TRUOC_NANG_LUC)\n` (gỡ F45, về r19/r20)
- d7: → `_TEN_NANG_LUC = frozenset(DOT_BIEN) ^ frozenset(_TRUOC_NANG_LUC)\n` (thấy xoá, không thấy ghi đè)
- d8: → `_TEN_NANG_LUC = frozenset(t for t in DOT_BIEN if DOT_BIEN.get(t) != _TRUOC_NANG_LUC.get(t))\n` (thấy ghi đè, không thấy xoá)

output (`khac_qua` ngoài nền; nền symlink và EPERM cho CÙNG ma trận):
```
            f45_them_ten_la   f45_xoa_ten       f45_ghi_de_ten
d1 (F43)    SỐNG {}           SỐNG {}           SỐNG {}
d6 (F45)    t52 giet_that     SỐNG {}           SỐNG {}
d7          t52 giet_that     t52 giet_that     SỐNG {}
d8          t52 giet_that     SỐNG {}           t52 giet_that
```
kết luận: gỡ F43 thì `f45_them_ten_la` sống; gỡ F45 thì `f45_xoa_ten` và `f45_ghi_de_ten` sống. Hai phiên bản gỡ nửa vời
(d7/d8), mỗi phiên bản bị đúng MỘT đột biến canh lộ, nên cả ba đột biến canh đều cần thiết và không cái nào thừa. Khi đột
biến canh sống, bán kính ĐỎ ⇒ việc gỡ chốt không còn vô hình. Các đột biến chết đều chết ở `t52` với thông điệp năng lực,
không có `AttributeError`/lỗi vô can (neo `_D45` độc lập với dòng quan sát).

**H6 — Đường (e): đăng ký theo nền NGOÀI cửa sổ.**
giả thuyết: bản vá mở đường mới ngoài cửa sổ. · lệnh: n3/n4/n3f (H4); cây `/tmp/r20-r21/b2-n3`, gate. · output: n3/n4/n3f
`{}`; gate b2-n3: `cong_cu_test: 56/56 đạt` … `đột biến=415 (giao mảnh) · lỗi đột biến=0`, rc=0. · kết luận: đúng như lượt
20 mô tả (e). Đường này có từ trước bản vá và bản vá KHÔNG mở ra nó. Cây hiện không có đăng ký theo nền nào ngoài cửa sổ
(H4, grep). Muốn đóng (e) thì phải quan sát `DOT_BIEN` dưới cả hai giá trị năng lực, tức nạp lại module hoặc mô phỏng nền.
Chủ kho đã loại cách đó sau lượt 17 (F39; chú thích tại `kq["nang_luc"]`: "MỘT ô … không nạp lại, không mô phỏng"). Vì vậy
đây là giới hạn thiết kế đã được quyết, **không phải finding**. Ghi lại để chủ kho biết: một bản vá tương lai đặt
`DOT_BIEN.pop` có điều kiện năng lực NGOÀI hai khối `_CO_SYMLINK` sẽ không bị cổng nào bắt, chỉ review bắt được.

**H7 — Lời khai của commit `cc78b33`.**
Khớp với đo độc lập: gate 56/56 với 416; A1 416 ok; 3 `f45_*` giết đúng `t52` bán kính 1/56; bậc hai d1/d6 (H5); ruff delta 0.
Commit ghi "KHÔNG ĐO ĐƯỢC tại chỗ: nền EPERM"; lượt này đã đo nền EPERM (H4, H5).

**H8 — Không hồi quy các lớp đã đóng.** Chỉ `ops/cong_cu_test.py` đổi, ở 3 chỗ: `_D45`, 3 dòng bảng, ảnh và dòng quan sát.
A1 trọn (H3) phủ mọi đột biến của lớp (2)–(5), và cả 416 đều `ok`.

**H9 — Hình dạng lỗi lặp của lớp (6).** Lượt này liệt kê lại (a)–(g) và thêm (h) phá ảnh, (i) giá trị `None`, (j) xoá rồi
thêm lại cùng giá trị, (k) tương tác cùng neo. Mọi đường TRONG cửa sổ hoặc bị `t52` bắt, hoặc làm cổng đỏ ồn (i), hoặc vô
hại (j). Đường ngoài cửa sổ (e) là giới hạn chủ kho đã chốt. Không đo ra hậu quả lặng nào ⇒ lớp (6) đóng, không ra finding.

## KHÔNG ĐO ĐƯỢC
- A1 trọn trên nền EPERM (413 đột biến, 8 mảnh). Chỉ đo 30 phép qua mut.py trên nền này (7 đột biến có sẵn + 11 tự soạn + 12 bậc hai). Gate EPERM không chạy lại: lượt 20
  đo nó ĐỎ vì môi trường ở cả head lẫn hint (t51, tiền kiểm alias bỏ qua).
- Nền EPERM trên baseline `f8a7829`: không đo lại rằng `t51 tin_dung_gia` / `t46 bo_qua` cũng có ở baseline. Lượt này chỉ
  dựa vào đối chứng `c0` của head (nền có ở mọi dòng, kể cả dòng đối chứng) và phép đo baseline của lượt 20.
- Phản chứng `t152` (đổi/xoá `AL_VER` trong ci.yml): không đo lại. W4/W5 không đổi từ lượt 20; chỉ đo delta `launcher_test` 0.
- `ops/lease_publish_test.py`: không chạy lượt này, vì nằm ngoài write set và không đổi.
- A5 (vắng mọi biến, bán kính đủ trong một tiến trình), đường Windows của mảnh/gom, `upload-artifact`/`download-artifact`
  thật, thời gian runner (A9), danh tính người ký (#566), effort executor.
- Nền VẮNG thuộc tính `os.symlink` (nhánh AttributeError): chủ kho đã loại (F39), không mô phỏng.
- Không soạn payload ký tự điều khiển/ẩn hay đường thoát khỏi cây; hướng BOM giữa lệnh `run` do lượt 19 mô tả vẫn chưa ai dựng.
