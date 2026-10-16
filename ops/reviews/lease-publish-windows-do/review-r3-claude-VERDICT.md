# Review r3 — packet #687 LEASE-PUBLISH-WINDOWS-DO

- reviewer: Sonnet 5.5, effort high (tự khai; không xác thực bằng telemetry)
- nhãn: `advisory_review` (cùng họ Claude với executor Opus 5.5)
- reviewed_sha: `f721fb43629a054d2adbc96b3cc748da17481bea` (cay-kho HEAD, đo lại)
- spec sha256 đo lại (SPEC-r3.md): `d4d6715d9f4129d4ceb7dcb47dfe2ede67b53a01e8ac1df350111de8e627543e` — khớp lease g3
- Môi trường: PYTHONDONTWRITEBYTECODE=1; thử/đột biến chỉ trong bản sao `mktemp -d -p .`; không sửa `cay-kho/`.

(Ghi tăng dần.)

## M1 — merge là union (ĐẠT)

Đo bằng AST (`blocks.py`, `m1b.py` trong $R): tách từng khối `def`/`class`/gán cấp module của tệp ở từng rev.
- `t195`–`t202` của HEAD `f721fb4` byte-exact với `20ec8d5` (master có #677): 8/8 `True`.
- `_chay_buoc_dang` + `t51 t53 t54 t56 t57 t58 t59 t60 t62 t63 t64 t65 t66 t67 t68` (mọi khối `t51`–`t68` có thật) byte-exact với `89fc4fac`: `bad []`.
- Mọi khối #677 đổi so `1c23933` (28 tên, gồm `t154`, `t70`, `_chay_buoc_dang_that`, helper `_GH_GIA_THAT`…) đều bằng master trong HEAD; giao "#677 đổi ∩ HEAD≠master" = rỗng.
- Khối HEAD khác master chỉ là 10 tên của #687 (`_ly_do_bo_qua_workflow _chay_main_meta t71 t72 t73 t98 t125 t158 t160 main`); không khối nào của master/89fc vắng khỏi HEAD (`missing []`).
- Phần cấp module ngoài khối: HEAD chỉ THÊM khối chú thích sổ (`SO_BO_QUA`) + dòng trống; không mất dòng nào của master.
- `ops/lease_publish.py`: `git diff --stat` so `59ce2d5`, `20ec8d5`, `89fc4fac` đều rỗng.
- Ghi chú rig: `origin/master` TRONG sandbox `cay-kho` là `c16bec6` (CŨ HƠN #689; `c16bec6` là tổ tiên của `20ec8d5`), nên `git merge-base HEAD origin/master` trong sandbox ra `c16bec6` và numstat `1048 78` (≡ so `89fc4fa`). Đây là tạo tác của bản sao sandbox, không phải finding; S5″ đúng spec đo ở mục 5.

## M2/M3 — sổ BỎ QUA (đo độc lập; phát hiện L-A bên dưới)

Phép đo (script `tmp.DHs6aumXWk/m2/drv.py`, kết quả `tmp.DHs6aumXWk/m2/m2res.json`, trên bản sao `cay-kho` f721fb4): nạp module, ghi đè `_ly_do_bo_qua_workflow` bằng bản gọi gốc với `nen` mặc định `"nt"`, bọc đếm `_chay_buoc_dang`/`_chay_buoc_dang_that`, rồi CHẠY THẬT từng ca trong `CA` (trừ `t125`):

```
198 ca: QUA 183 · THROW(BoQuaNen) 12 · OTHER 2 (t199, t203) · SKIP 1 (t125)
THROW: t51 t59 t60 t62 t63 t66 t68 t195 t196 t197 t198 t200 — cả 12 cùng cặp ('ops-publish-lease.yml','dang'), mỗi ca gọi helper đúng 1 lần
OTHER: t199 và t203 đỏ bằng TinHieuChotCa của chính chúng (mô phỏng ép nt đúng chỗ chúng đo nền thật) — KHÔNG ném BoQuaNen
```
- Tập ném = đúng sổ 12 ca (`SO_BO_QUA`, đọc từ tệp), cặp đúng. `t199` tự bắt nên không đăng ký; `t201 t202 t203` không ném. Khớp lời khai executor; tự đo, không suy từ tên.
- t193 vế sổ/M3 — đột biến của tôi (bản sao tạm, driver in-process: GIẾT chỉ khi ngoại lệ là `TinHieuChotCa`/`bang`, khung ném cuối là `chot`/`bang`, và khung ca đích có trên chuỗi): M1 bỏ kiểm sổ · M4a/b thêm tên · M3a bỏ t196 · M3b thêm t199 · M3c thêm t201 · M3d t200 sai job · P1 chỉ so tệp · P2 chỉ so job · Q bộ giải nổ ⇒ miễn — TẤT CẢ `GIET` ở t193 bằng `chot` (thông điệp nêu đúng ca/cặp). "Đỏ đúng ca ấy / không xanh giả" xác nhận ở nhóm M3.
- **Đường vào khác (gián tiếp)** — xem L-A: `_ca_doc_than_buoc` chỉ nhìn `co_names` TRỰC TIẾP; probe chạy được cho thấy ca ném gián tiếp qua helper vô hình với `t193` VÀ `t70` (cả hai QUA) và không đăng ký được (đăng ký ⇒ `t193` ĐỎ `thừa=[…]`).

## Phương pháp đột biến (dùng cho mọi lớp dưới)

Trên bản sao tạm trong `$R/tmp.DHs6aumXWk/` (mỗi đột biến một thư mục `mktemp`, chỉ chép `ops/*.py|*.sh` + `.github/`, xoá sau khi chạy; một lần hết đĩa do chép cả `ops/specs` — đã dọn bằng xoá từng tệp của chính các thư mục đột biến của tôi, không đụng `cay-kho/`). Phép thế văn bản neo ĐÚNG MỘT lần (`mut/check_anchor.py`: 0 neo lệch). Driver `mut/mdrv.py` chạy ca đích TRONG tiến trình và chỉ cấp GIẾT khi ngoại lệ là `TinHieuChotCa` với khung ném cuối `chot` (hoặc `AssertionError` với khung cuối `bang`) VÀ khung của chính ca đích nằm trên chuỗi traceback; mọi trường hợp khác (`NotImplementedError`, `AttributeError`, `ValueError`…) là `DO_KHAC` = KHÔNG tính giết. Tái lập: `python -B mut/mrun.py <thư-mục-làm-việc-tuyệt-đối> <cây-nền-tuyệt-đối> mut/specN.py`.

Kết quả trên cây nền `f721fb4` (`mut1.log`, `mut2.log`, `mut-hint-all*.log`):
- spec1 — 39 đột biến (14 của r1: M1 M2 M3 M4a/b M5 M6 M7 M8 M9 M10 M11 · R15 R16 R17 R18/19 R20 R21 R22 R23 · ba dạng unsupported U1 U2 U3 · M3a M3b M3c M3d · N1 N2 N3 N4 N5 N6 N7 · P1 P2 · Q · T1 T2): 43 dòng GIẾT đúng assertion của ca đích; 1 `DO_KHAC` (R21 chạy ở `t193`: `NotImplementedError: cannot instantiate 'WindowsPath'` — KHÔNG tính, giống r2; R21 thật bị `t203` GIẾT bằng chốt "rò"); 1 `QUA` đúng thiết kế (R22 chạy ở `t193`; ca đích của R22 là `t203` và nó GIẾT).
- R15 viết lại sát r2 (`R15p`: chỉ tin sổ khi `so is SO_BO_QUA`, nền `nt`) và R20 dạng symlink (`R20p`, so `abspath`): GIẾT ở `t193` bằng vế A4 / A5-symlink. (R15 nguyên văn của tôi ở spec1 chết sớm hơn ở vế `(c/d)` vì rộng hơn R15 của r2 — `R15p` mới là phép phân biệt A4.)
- Đột biến `L` gốc của #677 (gỡ đúng hai dòng chốt `lease_id` trong `_tien_kiem_mien_dang`, `ops/lease_publish.py:949–950`): `t195` GIẾT, `t196` GIẾT, `t197` GIẾT (cả ba bằng `TinHieuChotCa`/`chot`, thông điệp nêu `đột biến L`); `t198` QUA (đối chứng dương, đúng thiết kế).

## L1 — Sổ BỎ QUA đo bằng bộ lọc ứng viên TĨNH nên mù ca ném GIÁN TIẾP · P3 · mới (đường vào thứ ba của r2-L1/M2)

**Trạng thái r2-L1: ĐÃ ĐÓNG** (đo — xem bảng đột biến trên: A1/A2/A2′/A4/A5, M3a–d, R15p, R20/R20p, U1–U3 đều GIẾT bằng `chot` của `t193`). Lớp này là CÒN LỖ MỚI ở chính chốt M2, không phải lỗ cũ.

**Biểu hiện.**
- `ops/lease_publish_test.py:3035` `_ca_doc_than_buoc` chỉ lọc ca có `_chay_buoc_dang`/`_chay_buoc_dang_that` trong `fn.__code__.co_names` TRỰC TIẾP; `:10623` `uv = set(_ca_doc_than_buoc(CA))` rồi `do_duoc` chỉ chạy THẬT `uv`. Hai điểm ném `BoQuaNen` THẬT duy nhất là `:2757` và `:10843` (`grep -n 'raise BoQuaNen'`; ngoài ra chỉ có ca giả `_ca_gia` `:3059` và chuỗi mẫu `:11126`).
- Hệ quả: ca gọi helper bọc (`def _h(): _chay_buoc_dang_that(...)`, ca gọi `_h()`) ném `BoQuaNen` trên Windows nhưng vô hình với `t193` VÀ `t70`; không đăng ký được vì đăng ký ⇒ `t193` ĐỎ (`thừa=[…]`, nó không nằm trong `do_duoc`). Trên Linux xanh, trên Windows ĐỎ "NGOÀI SỔ" không có đường sửa tại chỗ ngoài việc làm helper TRỰC TIẾP. Chiều hỏng là fail-closed (không có xanh giả), nên P3 chứ không P2; executor đã khai giới hạn (BAO-CAO §7) nhưng KHÔNG đưa nó thành ca chạy được — đúng kiểu "nghĩ ra phép thử mà không chạy nó" (CLAUDE.md).
- Hiện trạng 198 ca: đóng bao hàm cấp module cho 15 ứng viên (13 trực tiếp + `t202` + `t70`, `t70` chỉ vì mã LỒNG `def _a(): _chay_buoc_dang`); chạy thật vẫn ra đúng 12 ném ⇒ chưa có ca gián tiếp nào ngày nay. Lỗ là bẫy bảo trì, không phải lỗi đang xảy ra.

**Phép đo tái lập** (`mut/spec3.py`, cây nền `f721fb4`):
```
python -B mut/mrun.py $PWD <cay-kho> mut/spec3.py
IND-chua-dang-ky t193   QUA        |        # thêm @ca t999 gọi _h_gian_tiep() -> _chay_buoc_dang_that("x")
IND-chua-dang-ky t70    QUA        |
IND-dang-ky      t193   GIET  TinHieuChotCa chot | sổ phải BẰNG tập ca ĐO được ném BoQuaNen trên nt, đúng cặp: thiếu=[], thừa=['t999_gian_tiep_qua_helper'], lệch cặp=[]
IND-dang-ky      t70    QUA        |
```
Đóng bao tĩnh theo tên (`m1b`-style, một lệnh Python nạp module): `direct=13 closure=15`, `direct−closure=∅`.

**Hint patch** (`HINT.patch`, hunk 1–2; +16 dòng): thêm `_ca_ung_vien_gian_tiep(cac_ca, g=None)` (BFS theo `co_names` qua hàm cấp module; mã LỒNG không tính nên `t70` không bị kéo vào và `mong` của `t70` giữ nguyên) và đổi `t193:10623` sang dùng nó, kèm một vế đơn vị chạy trên không gian tên giả (`exec("def _a(): _chay_buoc_dang\ndef _h(): _a()\ndef _k(): _h()\ndef _c(): pass", gia)` ⇒ ứng viên == `["_k"]`).
- Ca khoá: vế đơn vị trong `t193`. Đo (`mut/spec7.py`, trên cây đã vá): `HINT-closure-ve-truc-tiep` (bỏ bước đệ quy, chỉ `co_names` trực tiếp) ⇒ `t193` GIẾT `TinHieuChotCa chot` "ứng viên phải tính cả ca gọi helper BỌC…"; `HINT-bo-vong-lap-closure-1-tang` (chỉ theo tên bắt đầu `_a`, mất tầng thứ ba) ⇒ cũng GIẾT cùng chốt.
- Đột biến phải làm ca ĐỎ: `IND-chua-dang-ky` ⇒ `t193` GIẾT `thiếu=['t999_gian_tiep_qua_helper']` (đo trên cây đã vá: `GIET TinHieuChotCa chot`); `IND-dang-ky` chỉ xanh khi cập nhật CẢ literal 12-tiền-tố độc lập (đúng như một ca trực tiếp mới).
- Giới hạn còn lại (khai thẳng): gọi qua `getattr`/bảng hàm/lambda lưu trong dict vẫn vô hình với phép đóng bao tĩnh; chỉ phép quét động MỌI ca (≈5 phút, như executor làm ngoài suite) phủ hết. Không đòi đưa phép quét động vào cổng.

## L2 — Chốt "neo đầu dòng" của verifier không có răng: bốn đột biến bỏ neo SỐNG · P3 · mới

**Trạng thái r2-L2: ĐÃ ĐÓNG** (đo: M5 M6 M7 M9 M10 N1 N2 N3 N4 N6 N7 R16 R17 R18 R19 GIẾT đúng assertion của `t194`/`t160`; dòng chẩn đoán xen giữa marker và CRLF được NHẬN — đột biến N7 làm vế QUA CRLF đỏ). Lớp này là phần B1 của spec còn chưa có răng.

**Biểu hiện.** `_xac_minh_transcript_ab` nói trong docstring và spec r1 §4 B1 "đúng MỘT dòng tổng kết **neo đầu dòng**"; mã neo bốn chỗ: `:4596` (`RE_TONG_KET` `(?m)^lease_publish:`), `:4617` (`^(>>> vao|<<< ra)`), `:4624` (`^<<< ra`), `:4631` (`^  ĐỎ  `). Gỡ riêng từng neo KHÔNG làm ca nào đỏ: vế QUA của `t194` chỉ có dòng chẩn đoán ĐẦU dòng (`chẩn đoán: x` rồi `<<< ra …` ở dòng kế), không có dòng chẩn đoán GIỮA dòng chứa chính chữ marker/tổng kết/ĐỎ. Mức: ca khoá không bảo vệ một lời khai của hợp đồng; hướng hỏng phần lớn là fail-closed (đỏ oan), NHƯNG có một đường XANH GIẢ đo được: với V5 (bỏ neo `^<<< ra`), transcript có dòng `<<< ra tb LA` (hỏng) rồi dòng nhiễu `nhiễu cuối dòng <<< ra tb 0.001s QUA` ⇒ `_xac_minh_transcript_ab` trả `[]` (cây nguyên trả hai lý do: `hỏng trạng thái… hợp lệ=2 kỳ vọng=3` và `tổng kết lệch marker`). Cần nhiễu có chủ đích trong stdout của con nên P3 chứ không P2.

**Phép đo tái lập** (`mut/spec2.py`, cây nền `f721fb4`):
```
V2-tk-khong-neo       t194 QUA   # RE_TONG_KET bỏ ^
V4-su-kien-khong-neo  t194 QUA   # su_kien bỏ ^
V5-ra-khong-neo       t194 QUA   # regex `<<< ra` bỏ ^
V6-do-khong-neo       t194 QUA   # regex ĐỎ bỏ ^
```
**Hint patch** (`HINT.patch` hunk t194; +4 dòng): thêm vế QUA "dòng chẩn đoán GIỮA dòng" — hai dòng nhiễu chèn trước `<<< ra tb`: `chẩn đoán: >>> vao tc ·   ĐỎ  tb: q · lease_publish: 3/3 đạt; đã chạy=3, bỏ qua=0` và `chẩn đoán: <<< ra tc 0.001s QUA`; `_xac_minh_transcript_ab(...) == []` phải giữ.
- Đo trên cây đã vá: V2 V4 V5 V6 đều `GIET TinHieuChotCa chot` "vế QUA 'dòng chẩn đoán GIỮA dòng …' bị chặn oan"; cây nguyên (không đột biến) `t194 1/1`. (Lần thử đầu của tôi đặt tổng kết giữa dòng chưa kết thúc dòng nên V2/V5 còn sống — đã sửa hint: dòng tổng kết PHẢI nằm CUỐI dòng chẩn đoán và dòng `<<< ra tc` PHẢI hợp lệ tới cuối dòng, nếu không regex không neo cũng không khớp.)

## L3 — Seam của `main()`: lượt CUỐI trùng nền thật làm đột biến "nền dính" SỐNG trên Linux; snapshot hẹp hơn tập trạng thái · P3 (R25L) + P4 (environ/cwd/sys.path/globals) · mới / mang một phần từ r2-L4

**Trạng thái r2-L4: MỘT PHẦN.** Đo: R21 `t203` GIẾT bằng chốt "rò" `['os.name (nen=nt)', …]` (không bằng `WindowsPath`); R22 GIẾT `['CA (nen=nt)', 'CA (nen=posix)', …]`; R23 GIẾT `['SO_BO_QUA …']` (và `t193` (e)); R24 (seam ghi `sys.argv`), R26 (`chon` dính), R27 (`so` dính), R25F (nền dính, GHI LẦN ĐẦU) đều GIẾT bằng `chot` của `t203`. Còn hở:

**Biểu hiện (`ops/lease_publish_test.py`).**
- `:11385–11387` bốn lượt seam có `nen` = `nt, posix, nt, posix`. Lượt MẶC ĐỊNH ngay sau đó (`:~11402`) kỳ vọng nền THẬT. Trên Linux nền thật là `posix` = nền của lượt seam CUỐI, nên một `main()` nhớ `nen` của lần gọi gần nhất ("last-wins") cho lượt mặc định đúng nền kỳ vọng ⇒ vô hình. (Trên Windows thì ngược: lượt cuối `posix` ≠ `nt` ⇒ lộ — nhưng Windows không ở trong cổng PR.) Đúng họ lỗi r2-L4 ("seam dính sang lượt kế") mà lượt mặc định sinh ra để chặn.
- `:11378–11379` `anh()` chỉ chụp bốn khoá (`CA`, `SO_BO_QUA`, `os.name`, `sys.argv`) — khớp spec C1 nhưng không phủ `os.environ`, `os.getcwd()`, `sys.path`, các tên toàn cục khác (vd. `NHAN_UBUNTU_CHO_PHEP`, `WORKFLOW_DANG`). Tự liệt kê đường (CLAUDE.md "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA") ⇒ ba đường chưa có chốt riêng.

**Phép đo tái lập** (`mut/spec6.py`, `mut/spec2.py`; cây nền `f721fb4`; mọi dòng chạy ca `t203`):
```
R25L-nen-dinh-LAST-wins        QUA     # nen = nen or _ND.get('n'); if nen: _ND['n']=nen   (SỐNG)
R25F-nen-dinh-FIRST-wins       GIET    chot "lượt mặc định phải dùng argv + nền thật (posix) + sổ thật"
L4a-seam-ghi-environ           QUA     # os.environ["LP_RO_SEAM"]=nen
L4c-seam-chdir                 QUA     # os.chdir("/")
L4e-seam-sys.path.insert       QUA     # sys.path.insert(0,"/tmp")
L4b-seam-ghi-global-allow      QUA(t203) / GIET(t193, t71) — bị bắt NGẪU NHIÊN ở ca khác, không phải chốt "rò"
L4d-seam-ghi-WORKFLOW_DANG     GIET    (bắt ở lượt mặc định)
```
(`L4g` no-op và `L4h` `sys.stdout=sys.__stdout__` bên trong `redirect_stdout` là đột biến TƯƠNG ĐƯƠNG, không tính.)

**Hint patch** (`HINT.patch`, hunk t203; +9 dòng): (i) thêm lượt seam thứ 5 với `nen = "nt" if os.name != "nt" else "posix"` — KHÔNG sửa lượt 4, vì đột biến "chỉ rò khi `nen=='posix'` và `so` khác rỗng" (L4f) cần lượt 4 nguyên vẹn (lần thử đầu của tôi đổi thẳng lượt 4 làm L4f SỐNG trở lại — đã đo, đã bỏ); (ii) `anh()` thêm `os.environ`, `cwd`, `sys.path`, `{tên: id(giá trị)}` của toàn cục không-dunder, và đoạn gỡ rò khôi phục `os.environ`/cwd/`sys.path`.
- Đo trên cây đã vá (`mut-hint-all2.log`, `mut/mx`): R25L GIẾT ở `t203` (chốt lượt mặc định); L4a/L4b/L4c/L4e/L4d GIẾT bằng chốt "rò trạng thái" `['os.environ (nen=…)']` / `['globals (…)']` / `['cwd (…)']` / `['sys.path (…)']`; L4f vẫn GIẾT; cây nguyên `t203 1/1`, và suite đầy đủ (mục Hồi quy dưới).

## L4 — Giòn/chặt oan và nhánh `nt` chưa từng chạy thật · P4 · mới (ghi nhận, không đòi sửa mã)

**Đo được (Linux, cây `f721fb4`, ca chạy riêng `--chi-ca=` rồi cả suite):**
- `t193` 1.19 s · `t194` 0.28 s · `t203` 0.26 s · `t160` 0.39 s · `t70/71/72/73/98` 0.17–0.25 s, tất cả `1/1 đạt; đã chạy=1, bỏ qua=0`.
- Không đỏ oan khi: chạy từ `cwd=/` kèm `GITHUB_ACTOR=ke-la` · đường tệp tương đối (`cd ops; python lease_publish_test.py`) · `python -X dev` · `--nhat-ky=…` · `LANG=C` không `PYTHONUTF8`.
- Đỏ KHÔNG mới (so với `20ec8d5` cùng lệnh — baseline cũng chết, nên không tính): `python -W error` (`SyntaxError: invalid escape sequence '\s'` ở docstring dòng ~2587) và `PYTHONIOENCODING=ascii` (`UnicodeEncodeError` ở `print(_dong_tong_ket…)`).
- `git status` của cây sau khi chạy cả suite: sạch (A4 chỉ ghi vào bản sao module trên cây fixture, không đụng `WORKFLOW_DANG` thật).
- Verifier: dòng chẩn đoán xen giữa marker và CRLF được NHẬN (vế QUA của `t194`; đột biến N7 ⇒ ĐỎ). Đỏ oan DUY NHẤT còn thấy từ đọc mã: một ca in một dòng KHÔNG xuống dòng ngay trước `_nhat_ky_ca("<<< ra …")`, hoặc cháu thừa kế stdout ghi dở dòng, làm `<<< ra` rơi khỏi neo `^` ⇒ `chuỗi vao/ra KHÁC tập ca kỳ vọng`. Hiện 198 ca không ca nào làm vậy (A/B hai con đều `198/198`); Windows: KHÔNG ĐO ĐƯỢC.

**Nhánh `nt` chưa từng chạy thật — chỉ đọc mã, KHÔNG ĐO ĐƯỢC trên Windows (không có nền; spec r3 §5.5 cấm CI).**
- `Path(ex.tep).resolve()` ở hai vế so cặp (`main()`): trên Windows `resolve()` chuẩn hoá hoa/thường và tên ngắn 8.3 cho tệp TỒN TẠI nên hai vế cùng chuẩn; với đường KHÔNG tồn tại không chuẩn hoá hoa/thường ⇒ lệch ⇒ fail-closed (đỏ), không xanh giả. `WindowsPath` KHÔNG xuất hiện vì seam là tham số (`nen=`), không vá `os.name` — R21 chỉ tạo `NotImplementedError` trên POSIX.
- `t193` A5: `symlink_to` trên Windows không đặc quyền ném `OSError` — nhánh in `[t193] A5 vế symlink KHÔNG ĐO` có bắt (`except OSError`); trên runner GitHub (admin) symlink có thể tạo được và vế chạy thật — chưa từng chạy. Vế `..` chạy được ở cả hai nền.
- `t203` lượt mặc định: kỳ vọng `rc==0` + `0/0 đạt; đã chạy=0, bỏ qua=1` khi `os.name=='nt'`; đúng theo `main()` đọc được. Ca này CHÍNH LÀ chốt `nt` của `main()` — chưa chạy thật.
- Windows không đặt `PYTHONUTF8` ở lượt chạy tay: in `ĐỎ/BỎ QUA` có thể `UnicodeEncodeError` (không phải do bản vá này; CI đặt `PYTHONUTF8=1`).
- Kỳ vọng của executor trên Windows (`186/186 đạt; đã chạy=186, bỏ qua=12`) là SUY RA từ sổ 12 ca, chưa đo.
- Sổ BỎ QUA trên Windows phụ thuộc phép đo MÔ PHỎNG (ép `nen='nt'` ở `_ly_do_bo_qua_workflow`); tôi tái dựng độc lập ra cùng 12 ca — cùng giới hạn: một ca ném CHỈ khi `os.name=='nt'` thật ở nơi khác ngoài hai điểm `:2757`/`:10843` thì mô phỏng không thấy (grep `raise BoQuaNen`: ngoài hai điểm ấy chỉ có `_ca_gia` — ca giả).

## Hồi quy (mục 5 của PROMPT)

- **Toàn suite** (bản sao `cay-kho` nguyên văn `f721fb4`, `python -B ops/lease_publish_test.py`, không `--chi-ca`, `env PYTHONDONTWRITEBYTECODE=1`; hai lượt độc lập, lượt hai có `echo rc=$?`): `rc=0`; dòng ngoài `lease_publish: 198/198 đạt; đã chạy=198, bỏ qua=0`; `[A] … 198/198 đạt; đã chạy=198, bỏ qua=0`; `[B] … 198/198 đạt; đã chạy=198, bỏ qua=0`; 0 dòng `  ĐỎ  `. Cây gốc `git status` sau chạy: sạch.
- **Cây đã vá bằng `HINT.patch`** (`sha256 74a53928…c6fc`, áp sạch lên `f721fb4` bằng `patch -p1`, sha tệp kết quả `09cf6c78…816c` khớp cây đo): suite đầy đủ `rc=0`, `198/198 đạt; đã chạy=198, bỏ qua=0`, `[A]`/`[B]` cùng `198/198, bỏ qua=0`, 0 ĐỎ (số ca KHÔNG đổi: hint chỉ thêm vế/chốt trong ca sẵn có).
- **Mutant `L` gốc của #677**: chết ở `t195`, `t196`, `t197` (bằng `chot`), xem bảng đột biến ở trên.
- **S5″**: `git diff --numstat 20ec8d5 HEAD -- ops/lease_publish_test.py` = `448 63` (đo lại; trùng khai của executor) ≤ 600. Cùng lệnh so `89fc4fa` = `1048 78` (tham khảo). Ghi chú rig: trong sandbox `origin/master` là `c16bec6` (tổ tiên cũ của `20ec8d5`, trước #689), nên `git merge-base HEAD origin/master` ở ĐÂY ra `c16bec6` và numstat = `1048 78` — tạo tác bản sao sandbox, KHÔNG phải vượt trần; merge-base đúng theo spec là `20ec8d5` (đã chứa #677, `git merge-base HEAD 20ec8d5` = `20ec8d5`). Cây vá bằng `HINT.patch`: `482 63` (+34 dòng so HEAD), còn dư trần 118.
- **ruff `--select F`** (0.15.15, `--output-format=json`, so multiset `(mã, thông điệp, dòng nguồn, cột)`): `20ec8d5` = 9, `f721fb4` = 9, delta `{}` (cả hai chiều rỗng). Cây vá: 9 (chỉ đếm số lượng, không so multiset).
- **`git diff --check 20ec8d5 HEAD`**: rc 0. `doctrine-scan --root .`: "sạch — đã quét 10 tệp, 0 chỗ chép doctrine". `ops/lease_publish.py` không đổi so `20ec8d5`/`89fc4fa`/`59ce2d5`.
- **Sổ/ca lệch báo cáo?** BAO-CAO-VA khai sổ 12, tập ném 12, suite 198/198 hai vế, S5″ `448 63`, A8 16 khối byte-exact, ruff delta 0: tôi đo lại cả sáu và KHỚP. Không tái dựng được: bảng 53 dòng đột biến của executor chạy bằng bộ driver của họ (`va687/m4_*.py`, KHÔNG có trong sandbox) — tôi dựng bảng độc lập (39 đột biến spec1 + 24 ở spec2/3/5/6: 16·2·4·2, một số là biến thể tương đương/đối chứng) cùng phép phân hạng `TinHieuChotCa`/`chot`; không đối chiếu từng dòng của họ.

## Tổng hợp

### Trạng thái các finding của r2

| finding r2 | trạng thái ở `f721fb4` | bằng phép đo |
|---|---|---|
| L1 hợp đồng skip / bộ giải / ca khoá (P2) | **ĐÃ ĐÓNG** | R15p, R20/R20p, U1–U3, M1–M11 đều GIẾT bằng `chot` của `t193`; A4/A5 chạy thật. Đường thứ ba MỚI ở M2 → L1 bên trên (P3) |
| L2 transcript / verifier (P2) | **ĐÃ ĐÓNG** | R16 R17 R18/R19 + N1–N7 GIẾT bằng `chot`/`bang` của `t194`/`t160`; CRLF + chẩn đoán xen giữa được NHẬN. Răng của "neo đầu dòng" còn thiếu → L2 bên trên (P3) |
| L3 lời khai/provenance báo cáo (P4) | **ĐÃ ĐÓNG** (r2); BAO-CAO r3 đo lại sáu con số khớp | xem mục Hồi quy; Windows vẫn KHÔNG ĐO ĐƯỢC |
| L4 bảo toàn trạng thái seam (P2) | **MỘT PHẦN** | R21 R22 R23 R24 R25F R26 R27 GIẾT bằng chốt "rò"/lượt mặc định; R25L (nền dính, last-wins) SỐNG trên Linux → L3 bên trên (P3) |
| L5 trần kích thước (P2) | **ĐÃ ĐÓNG** (bằng revision spec) | S5″ `448 63` ≤ 600 so `20ec8d5`; tổng `1048 78` so `89fc4fa` chỉ tham khảo |

### Bảng lớp

| lớp | mức | mới/mang | sửa mã hay hồ sơ |
|---|---|---|---|
| L1 — bộ lọc ứng viên của sổ mù ca ném gián tiếp | P3 | mới (đường vào thứ ba của r2-L1/M2; executor đã khai, chưa thành ca chạy) | sửa mã (`HINT.patch`, hunk `_ca_ung_vien_gian_tiep` + vế đơn vị trong `t193`) |
| L2 — "neo đầu dòng" của verifier không có răng (V2/V4/V5/V6 sống; V5 cho xanh giả đo được) | P3 | mới | sửa mã (`HINT.patch`, vế QUA chẩn đoán giữa dòng trong `t194`) |
| L3 — seam: lượt cuối trùng nền thật (R25L sống) + snapshot hẹp (environ/cwd/sys.path/globals) | P3 (R25L) · P4 (còn lại) | mang một phần từ r2-L4 + mới | sửa mã (`HINT.patch`, lượt seam thứ 5 + `anh()` mở rộng) |
| L4 — giòn/đỏ oan & nhánh `nt` chưa chạy thật | P4 | mới | hồ sơ (ghi nhận; Windows KHÔNG ĐO ĐƯỢC) |

Không có P1/P2. Ba lớp P3 đều có hint áp sạch (+34 dòng, S5″ còn 118), đã đo: suite đầy đủ `198/198, bỏ qua=0, rc=0` trên cây vá và mọi đột biến mới của tôi bị GIẾT bằng assertion của ca đích trên cây vá; chỉ đột biến TƯƠNG ĐƯƠNG (L4g no-op, L4h) và đột biến chạy ở ca KHÔNG phải ca đích (R21/R22 ở `t193`, `IND-*` ở `t70`) là không-giết, đúng dự kiến. Phần Windows thật: KHÔNG ĐO ĐƯỢC (không có nền, không CI theo spec r3 §5.5).

Tệp kèm: `HINT.patch` (áp lên `f721fb4`, sha256 `74a53928df251fc3cc4dcce7fa2a49794d042ec7b06f04a7a951ddd681f1c6fc`); công cụ tái lập trong `mut/` (`mdrv.py`, `mrun.py`, `spec1..7.py`) và `blocks.py`/`m1b.py`.

VERDICT: CHANGES_REQUIRED
