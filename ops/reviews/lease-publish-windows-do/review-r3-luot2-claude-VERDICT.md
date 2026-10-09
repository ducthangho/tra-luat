# Review r3 lượt 2 — packet #687 LEASE-PUBLISH-WINDOWS-DO

- reviewer: Sonnet 5.5, effort high (tự khai; không xác thực bằng telemetry)
- nhãn: `advisory_review` (cùng họ Claude với executor)
- reviewed_sha: `9d7a523e80e91ef6aca2c7935f3ee1813fc369f9` (`git rev-parse HEAD` trong cay-kho; cha `f721fb4`)
- spec sha256 đo lại: `SPEC-r3.md` = `d4d6715d9f4129d4ceb7dcb47dfe2ede67b53a01e8ac1df350111de8e627543e` (khớp LEASE-g3 theo r3); SPEC-r1 `87375af3…`, SPEC-r2 `cab12ba9…`
- Môi trường: `PYTHONDONTWRITEBYTECODE=1`; thử nghiệm/đột biến chỉ trên bản sao `mktemp -d -p $R`; không sửa `cay-kho/`.


## Mục 1 — diff-luot-r3b.patch ≡ HINT.patch (ĐẠT)

- `sha256sum diff-luot-r3b.patch` = `74a53928df251fc3cc4dcce7fa2a49794d042ec7b06f04a7a951ddd681f1c6fc` = sha256 `luot-r3/HINT.patch`; `diff diff-luot-r3b.patch luot-r3/HINT.patch` rỗng (BYTE-EXACT, kể cả dòng `index`) ⇒ trùng từng hunk (4 hunk của `ops/lease_publish_test.py`: helper + t193, t194, t203).
- `git diff f721fb4 9d7a523 | diff - diff-luot-r3b.patch` rỗng: patch đúng bằng diff commit; `--stat` 1 tệp, +39/−5. Commit chỉ đụng `ops/lease_publish_test.py`.
- `git diff --check f721fb4 9d7a523` rc=0.

## Phương pháp đột biến

Bản sao `cay-kho` ở `/tmp/claude-0/-home-user-tra-luat/0c469e32-6eae-522a-ad2b-aacdd0027d2d/scratchpad/rv687-r3b/tmp.SYLiniFsZ3/base`, `probe`; đột biến chạy bằng `rv687-r3/mut/mrun.py` + `mdrv.py` (ĐỌC, dùng lại; tôi đã đọc `mdrv.py`: chỉ GIẾT khi ngoại lệ là `TinHieuChotCa` với khung ném cuối `chot` — hoặc `AssertionError` với khung cuối `bang` — VÀ khung của chính ca đích nằm trên traceback; mọi thứ khác là `DO_KHAC`, không tính). Spec mới của tôi: `/tmp/claude-0/-home-user-tra-luat/0c469e32-6eae-522a-ad2b-aacdd0027d2d/scratchpad/rv687-r3b/tmp.SYLiniFsZ3/mut/specA.py` (44 + 8 đột biến), `specH.py`, `specG.py`; mọi neo thế văn bản khớp đúng 1 lần (kiểm bằng script, "anchors done 44"). Mỗi đột biến chạy trong `mktemp -d` mới (mrun tự dọn từng tệp, không `rm -rf`). Số liệu dưới là chạy của lượt này, không lấy từ r3.

## Mục 2 — ba lớp P3 của r3 (đo bằng đột biến; gỡ riêng chốt thì đột biến sống lại)

### L1 (r3) — ca ném BoQuaNen gián tiếp: ĐÃ ĐÓNG cho helper cấp module (3 tầng)
```
L1a-ind-1tang-chua-dky   t193 GIET TinHieuChotCa chot | ... thiếu=['t999_gian_tiep_qua_helper'], thừa=[], lệch cặp=[]
L1b-ind-3tang-chua-dky   t193 GIET TinHieuChotCa chot | ... thiếu=['t999_gian_tiep_3tang']
L1e-GO-chot-uv+1tang     t193 QUA   # gỡ riêng chốt (uv quay về _ca_doc_than_buoc) ⇒ đột biến SỐNG LẠI
L1f-GO-chot-uv+3tang     t193 QUA
L1g-GO-vedonvi-uv        t193 QUA   # gỡ vế đơn vị + bỏ đệ quy: đối chứng
L1h-vedonvi-tang3        t193 GIET  TinHieuChotCa chot | ứng viên phải tính cả ca gọi helper BỌC ... nhiều tầng ...
```
- `t70` QUA ở mọi dòng (đúng thiết kế: `t70` đo bằng `_ca_doc_than_buoc` không đổi). `L1c/L1d` (đăng ký ca mới vào sổ nhưng không cập nhật literal 12 tiền tố) vẫn GIẾT bằng `chot` của `t193` — literal độc lập hoạt động.
- Ứng viên trên cây thật: `_ca_doc_than_buoc`=13 · `_ca_ung_vien_gian_tiep`=14, hơn đúng `t202` (không ném; vô hại). Chu trình/đệ quy tự thân (`_b↔_c`, `_d→_d`) kết thúc nhờ `thay`.

### L2 (r3) — neo đầu dòng của verifier: ĐÃ ĐÓNG
```
L2-V2 t194 GIET chot | vế QUA 'dòng chẩn đoán GIỮA dòng chứa chữ tổng kết/marker/ĐỎ (không neo đầu dòng ⇒ không tính)' bị chặn oan
L2-V4 t194 GIET (cùng chốt) · L2-V5 t194 GIET · L2-V6 t194 GIET
L2-GO-vey+V2 / +V4 / +V5 / +V6  t194 QUA  # gỡ riêng vế "y" ⇒ cả bốn SỐNG LẠI
```
Cả bốn bị giết bằng `chot` của chính `t194`, thông điệp nêu đúng vế.

### L3 (r3) — seam của main(): ĐÃ ĐÓNG cho nền dính + environ/cwd/sys.path/globals (gán lại)
```
L3a-R25L t203 GIET chot | lượt mặc định phải dùng argv + nền thật (posix) + sổ thật ...
L3a-GO-luot5+R25L t203 QUA       # gỡ riêng lượt thứ 5 ⇒ R25L sống lại
L3b-R25F t203 GIET (cùng chốt)
L3c-environ (ghi) / L3d-environ-xoa (pop PATH)  t203 GIET chot | RÒ trạng thái: ['os.environ (nen=nt)', ...]
L3e-cwd  t203 GIET | ['cwd (nen=nt)', ...]
L3f-syspath-insert / L3g-syspath-xoa  t203 GIET | ['sys.path (...)']
L3h-global-rebind-allow / L3i-global-moi-ten / L3j-global-xoa-ten  t203 GIET | ['globals (...)']
R21 R22 R23 R24 R26 R27 L4f  t203 GIET (7/7, chot "rò"/lượt mặc định)
GỠ TỪNG KHOÁ RIÊNG (so sánh bỏ đúng một khoá khỏi `ro`; 4 cặp, `/tmp/claude-0/-home-user-tra-luat/0c469e32-6eae-522a-ad2b-aacdd0027d2d/scratchpad/rv687-r3b/tmp.SYLiniFsZ3/solo.log`):
  GO-os.environ+environ QUA · GO-cwd+cwd QUA · GO-sys.path+syspath QUA · GO-globals+global QUA
  đối chứng (gỡ khoá KHÁC): cả 4 GIET ⇒ bốn khoá chụp độc lập, mỗi khoá có răng riêng
GỠ CẢ BỐN khoá chụp (anh() về 4 khoá, khôi phục an toàn): environ/cwd/sys.path/global đều QUA ⇒ chốt mới là thứ giết chúng.
```

## L-A — Ứng viên của sổ BỎ QUA vẫn mù ca ném qua def/lambda/class LỒNG (cùng họ L1 r3, nhánh tĩnh còn lại) · P4 · mới

**Biểu hiện.** `ops/lease_publish_test.py:3062-3074` (`_ca_ung_vien_gian_tiep.toi`) đi theo `__code__.co_names` của ca và của helper cấp module, KHÔNG xuống mã lồng (`co_consts`). Ca có `def`/`lambda`/`class` cục bộ gọi `_chay_buoc_dang*` ném `BoQuaNen` THẬT dưới `nt` mà không phải ứng viên.

**Phép đo** (probe in-process trên cây `9d7a523`: `exec` ca vào `m.__dict__`, chạy dưới `mock.patch.dict(globals(), nt)` y hệt `nem_nt`):
```
k_direct  candidate=True  | dưới nt: BoQuaNen
k_nested  candidate=False | dưới nt: BoQuaNen     # def _i(): return _chay_buoc_dang_that("x"); _i()
k_lambda  candidate=False | dưới nt: BoQuaNen
k_cls     candidate=False | dưới nt: BoQuaNen
L1i-def-long-chua-dky  t193 QUA  t70 QUA     # ca t999 def lồng, KHÔNG có trong sổ: t193 vẫn XANH trên Linux
```
Đăng ký ca ấy vào sổ làm `t193` ĐỎ `thừa=[…]` (nó không nằm trong `do_duoc`) ⇒ không có lối sửa tại chỗ; Windows sẽ ĐỎ "NGOÀI SỔ". Hướng hỏng là fail-closed, và hiện KHÔNG ca nào trong 198 ca thuộc dạng này (đo: ứng viên 14, `SO_BO_QUA` 12, tập ném đo được = sổ) ⇒ P4 (bẫy bảo trì, không phải lỗi đang xảy ra). Không xếp P3 vì đúng vế spec "ca ném gián tiếp qua HELPER" đã ĐÓNG (L1a/L1b), và lượt r3 đã khai chấp nhận giới hạn tĩnh còn lại.

**Hint patch** (`HINT.patch` hunk 1–2; tính trên `9d7a523`): đi thêm vào `co_consts` có `co_names`; đổi `ngan` thành hàng đợi mã (`__code__`); mở rộng vế đơn vị của `t193` thêm `_n` (def lồng) và `_l` (lambda).
- Đã đo trên cây vá: `t193` `t70` `t203` `t194` đều `1/1`; ứng viên trên cây thật = 13 cũ + `t202` + `t70` (`t70` kéo vào nhờ def lồng thật trong thân nó; nó không ném nên vô hại).
```
H-def-long-chua-dky / H-lambda-long-chua-dky / H-cls-long-chua-dky   t193 GIET chot | sổ phải BẰNG tập ca ĐO được ... thiếu=['t999_...']
H-GO-co_consts (gỡ dòng co_consts)  t193 GIET chot | ứng viên phải tính cả ca gọi helper BỌC ... def/lambda LỒNG ...   # vế đơn vị
```
- Gỡ riêng chốt: không có dòng `co_consts` thì ba ca t999 kia SỐNG (chính là `L1i` trên `9d7a523`: QUA).
- Giới hạn còn lại (khai thẳng): `getattr`/bảng hàm trong dict/`functools.partial`/`importlib` vẫn vô hình với phép quét tĩnh.

## L-B — `anh()` chụp toàn cục bằng `id()` nên mù đổi TẠI CHỖ giá trị khả biến; ngoài phạm vi: sys.modules/umask · P4 · mới

**Biểu hiện.** `ops/lease_publish_test.py:11405-11407`: `"globals": {k: id(v) ...}`. `CA`, `SO_BO_QUA` đã có khoá riêng (so nội dung); nhưng 18 toàn cục khả biến còn lại (`ENV_GITHUB`, `SO_GUARD_DANG`, `_KHONG_CHAY_T191`, `_TD_M2`…) mà `main()` ghi vào TẠI CHỖ giữ nguyên `id` ⇒ vô hình.

**Phép đo** (`specA.py` trên `9d7a523`; mọi dòng chạy `t203`):
```
L3k-global-inplace-dict  (ENV_GITHUB["RO"]=nen)        t203 QUA
L3l-global-inplace-set   (_KHONG_CHAY_T191.add)        t203 QUA
L3m-global-inplace-list  (_TD_M2.append)               t203 QUA
L3n sys.modules[...]=… · L3o os.umask(0o077)           t203 QUA   (ngoài bốn loại spec C1/prompt; khai, không đòi)
```
Sống sót cả TOÀN SUITE: bản `9d7a523` + `ENV_GITHUB["RO"] = nen` trong `main()` ⇒ `rc=0`, `[A]/[B]/ngoài` đều `198/198 đạt; đã chạy=198, bỏ qua=0`, 0 dòng `  ĐỎ  ` (/tmp/claude-0/-home-user-tra-luat/0c469e32-6eae-522a-ad2b-aacdd0027d2d/scratchpad/rv687-r3b/tmp.tvQy7xRbIw/suite-L3k.log). Hôm nay không có mã nào của `main()` ghi vào các dict đó nên là P4 (lỗ phát hiện, không phải lỗi); đúng hình dạng "gán lại tên ≠ đổi tại chỗ" của CLAUDE.md.

**Hint patch** (`HINT.patch` hunk 3; +2/−1): giá trị toàn cục `list/dict/set/bytearray` chụp thêm `repr(v)`: `(id(v), repr(v) if isinstance(v, (list, dict, set, bytearray)) else None)`.
```
G-dict-inplace · G-set-inplace · G-list-inplace · G-dict-xoa-khoa (SO_GUARD_DANG.clear())  t203 GIET chot | RÒ: ['globals (nen=…)', …]
G-GO-repr (gỡ repr, giữ id) + dict-inplace  t203 QUA    # gỡ riêng chốt ⇒ sống lại
```
- Cây vá: `t203` 3/3 lượt riêng `1/1`; toàn suite xem mục Hồi quy.

## Mục 3 — chốt mới có quá chặt/giòn không; đường vào mới

- **Đỏ oan** — không thấy trên `9d7a523`: `t203` chạy riêng 8/8 `1/1`; từ `cwd=/` `1/1`; `--ab-con-noi-bo` `1/1`; `--chi-ca=t20` (5 ca) dưới `PYTHONHASHSEED=7 LANG=C LC_ALL=C python -X dev` `5/5`; `--chi-ca=t193` `1/1`. `anh()` chụp `os.environ`/`sys.path` CHỈ trong cửa sổ các lượt seam của chính `t203` (không đo "ca khác đổi môi trường"), nên một ca khác hợp lệ đổi môi trường TRƯỚC `t203` không làm nó đỏ; chỉ thay đổi XẢY RA GIỮA hai lần chụp (do `main()` hoặc luồng nền) mới đỏ — hôm nay không có luồng nền nào (không đo được luồng nền tương lai).
- Nhược điểm cấu trúc: `id()` + khôi phục `environ`/`cwd`/`sys.path` là mã dọn dẹp nằm TRONG ca (nếu `main()` rò, ca tự gỡ để lượt sau đo sạch, nhưng cũng che hậu quả cho các ca chạy sau `t203` — chấp nhận được: ca đã đỏ).
- **Đường vào mới** từ 39 dòng — không thấy đường xanh giả nào do chính chúng mở (kiểm: chu trình/đệ quy trong BFS kết thúc; `g=None` mặc định = `globals()` thật; `exec` chỉ chạy chuỗi hằng). Hai khoảng trống đo được là L-A và L-B.

## Mục 4 — Hồi quy

- **Toàn suite** trên bản sao nguyên văn `9d7a523` (`python -B ops/lease_publish_test.py`, `PYTHONDONTWRITEBYTECODE=1`, `/tmp/claude-0/-home-user-tra-luat/0c469e32-6eae-522a-ad2b-aacdd0027d2d/scratchpad/rv687-r3b/tmp.SYLiniFsZ3/suite.log`): `rc=0`; dòng ngoài `lease_publish: 198/198 đạt; đã chạy=198, bỏ qua=0`; `[A] … 198/198 đạt; đã chạy=198, bỏ qua=0`; `[B] … 198/198 đạt; đã chạy=198, bỏ qua=0`; 0 dòng `  ĐỎ  ` đầu dòng. `git status` của `cay-kho` sau khi chạy: 0 dòng.
- **Cây vá bằng `HINT.patch`** (sha256 `7fa36324…f8a6`; `git apply --check` lên `9d7a523` OK): toàn suite `rc=0`, `198/198` ở cả ba (ngoài/[A]/[B]), `bỏ qua=0`; số ca không đổi.
- **Mutant `L` của #677** (gỡ hai dòng chốt `lease_id` ở `ops/lease_publish.py:948-949` trên bản sao `9d7a523`): `t195` ĐỎ (assertion "M2 tập (i): nền phải rc=1…"), `t196` ĐỎ ("đột biến L cho rc=0"), `t197` ĐỎ (cùng), `t198` QUA (đối chứng dương). Cả ba đỏ bằng thông điệp assertion của chính ca (đo bằng `--chi-ca=`; driver phân hạng `mdrv` không dùng cho dòng này).
- **S5″**: `git diff --numstat 20ec8d5 HEAD -- ops/lease_publish_test.py` = `482 63` (khớp khai của executor; merge-base `git merge-base 9d7a523 20ec8d5` = `20ec8d5d0e86…`) ≤ 600, còn 118. Cây vá `HINT.patch`: `486 63` (còn 114).
- **ruff `--select F`** (0.15.15, so multiset `(mã, thông điệp, dòng nguồn)`): `20ec8d5` = 9, `9d7a523` = 9, delta `{}` hai chiều.
- **`git diff --check 20ec8d5 HEAD`** rc=0; `git diff --check f721fb4 9d7a523` rc=0. `doctrine-scan --root .`: "sạch — đã quét 10 tệp, 0 chỗ chép doctrine". `ops/lease_publish.py` không đổi trong diff `f721fb4..9d7a523`.
- Windows: KHÔNG ĐO ĐƯỢC (không có nền; spec cấm CI). Lượt seam thứ 5 (`nen="nt"`) đã chạy trên Linux; nhánh `nen="posix"` khi `os.name=="nt"` chưa từng chạy.

## Tổng hợp

### Trạng thái các lớp của r3 (reviewed `f721fb4`)

| lớp r3 | mức r3 | trạng thái ở `9d7a523` | bằng phép đo |
|---|---|---|---|
| L1 ca ném gián tiếp | P3 | ĐÃ ĐÓNG (helper cấp module, 1 và 3 tầng) | L1a/L1b `t193` GIẾT `chot`; L1e/L1f gỡ chốt ⇒ QUA; vế đơn vị GIẾT L1h; còn nhánh lồng ⇒ L-A (P4) |
| L2 neo đầu dòng verifier | P3 | ĐÃ ĐÓNG | V2/V4/V5/V6 `t194` GIẾT `chot`; gỡ vế "y" ⇒ cả bốn QUA |
| L3 R25L + snapshot hẹp | P3+P4 | ĐÃ ĐÓNG R25L và 4 loại rò (gán lại/ghi) | R25L/R25F `t203` GIẾT; environ/cwd/sys.path/globals mỗi loại GIẾT ≥1; gỡ riêng từng khoá ⇒ QUA; còn in-place ⇒ L-B (P4) |
| L4 giòn/nhánh `nt` (P4) | P4 | MANG (Windows KHÔNG ĐO ĐƯỢC) | không đỏ oan trên Linux (mục 3) |
| P4 khác của r3 | P4 | MANG | không đổi bởi 39 dòng |

### Bảng lớp lượt này

| lớp | mức | mới/mang | sửa mã hay hồ sơ |
|---|---|---|---|
| L-A ứng viên sổ BỎ QUA mù def/lambda/class lồng | P4 | mới (nhánh tĩnh còn lại của r3-L1) | sửa mã tuỳ chọn (`HINT.patch` hunk 1–2) hoặc hồ sơ: khai giới hạn |
| L-B `anh()` mù đổi tại chỗ toàn cục khả biến; sys.modules/umask ngoài phạm vi | P4 | mới | sửa mã tuỳ chọn (`HINT.patch` hunk 3) hoặc hồ sơ |
| L4 (r3) nhánh `nt`/Windows chưa từng chạy thật | P4 | mang | hồ sơ (KHÔNG ĐO ĐƯỢC) |

0 P1 · 0 P2 · 0 P3.

VERDICT: PASS
