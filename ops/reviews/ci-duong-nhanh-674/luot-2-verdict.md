verdict: changes_requested
reviewed_sha: 9f9bb132d2eca6d6e80b6fd1dab59e0f12466230
Reviewed commit: 9f9bb132d2eca6d6e80b6fd1dab59e0f12466230

## DOI CHIEU LUOT TRUOC

Ngưỡng chủ kho: **0 P0/P1/P2/P3** mới approve; hai quyết định D1/D2 chưa được phê duyệt. Lượt này chưa đạt. Nguồn lượt trước: `goi/LUOT-TRUOC-VERDICT.md`, SHA `1687c693c622177742807f0a2abd765547b0e748`.

| Slug lượt trước | Phân loại | Bằng chứng tự đo trên head hiện tại |
|---|---|---|
| `kiem-lease-bo-sot-duong-vao` | **VA HO**, đã sửa các cửa bỏ kiểm, còn D2 chờ quyết | `out/lease.log`: `.yaml`/`.yml`, hết/còn hạn sai schema đều CHAN [8]; mutant miễn kiểm hết hạn, bỏ `.yml`, hạn hỏng, bỏ rc đều GIET. Lease hết hạn hợp lệ vẫn khác check trần: raw rc=8, hiện tại không lỗi. Bản vá fixture phát sinh lỗi actor, ghi riêng lớp mới bên dưới. |
| `diff-check-tu-ha-nguong` | **CHUA VA**, D1 chờ quyết, không yêu cầu tự đảo chính sách | `out/whitespace.log`: ba loại whitespace riêng đều raw rc=2, cấu hình hiện tại qua; conflict-marker vẫn bị bắt. |
| `chot-yaml-chi-do-su-hien-dien` | **VA HO** | Bảy cửa cũ y06/y08 đã khóa thật (`out/yaml.log`); cửa nuốt lỗi của chính bước selftest còn mở với `continue-on-error: ${{ true }}` (`out/y09.log`). |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | **VA HO**: runtime đã sửa, chốt chống tái diễn chưa đủ | Xóa README/caveat, mất evidence_url, lệch băm verdict/prompt đều đỏ đúng ở checker mới (`out/data.log`). Nhưng bỏ thao tác gọi ca trong `MA_CHAY_CA` vẫn full 46/46 + 67/67, rồi README mất vẫn qua (`out/mutant-data.log`). |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | **VA HO** | Số 6/113 đã tái lập theo scope một ref; 552 refs là 0/113. Mô tả k01/k02/k03 và năm mẫu rc/ba mutant đã sửa đúng. Bảng giao vẫn ghi 43/55; docstring vẫn t01..t21 dù đã thêm t22; các khẳng định phân rã/thời gian mới vẫn không có trong bảng. |

Không đổi slug để xóa lịch sử. Lỗi actor là lớp mới `fixture-lease-phu-thuoc-actor-ci`, phát sinh từ cách dựng fixture sạch ở lượt 2; không gộp nó vào quyết định D2 về chính sách sản phẩm.

Phạm vi và môi trường:

- Base `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; head tree `ec25fa2d6d5056db53181957f4aba4ee0e3fd387`.
- Đã đọc trọn SPEC-r2; SHA256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` khớp. Đối chiếu CLAUDE.md, AGENTS.md và protocol §8/8.3.
- Đúng bốn tệp trong write set; `ci_dang_ky_test.py` numstat **1 thêm / 0 xóa**, đúng mục DA_NOI. Không sửa checkout `cay/`, không commit/push/land.
- Reviewer: OpenAI Codex, thực thi công cụ máy trong phiên này; không tự có runtime receipt xác minh model/effort hay launcher transport. Executor Claude theo prompt; không suy assurance từ tài khoản GitHub. Đây là verdict nội dung, không phải quyền land.
- Linux/Python 3.11; actionlint 1.7.7, ShellCheck 0.9.0, Ruff 0.15.15. Actions khai Python 3.12. Không mạng, không chạy Windows CI, không gọi PR thật.
- Lệnh dưới tương đối với workspace `rv2`, trừ nơi chỉ rõ `cd cay`. Mọi phép dùng temp đặt `export TMPDIR="$PWD/tmp"` tại workspace; dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`; bản sao và artifact ở `tmp/`, `out/`.
- Sổ đăng ký lần đầu rc=1 vì Git global bật ký commit trong fixture. Đã dựng nền/head trong cùng lệnh và chạy lại với `GIT_CONFIG_COUNT=4 GIT_CONFIG_KEY_3=commit.gpgsign GIT_CONFIG_VALUE_3=false`; cả hai đạt. Chỉ chỉnh môi trường fixture, không đổi cấu hình `cay`.

## BANG LOP

| Slug | Các biểu hiện/cửa vào | Hạng cao nhất còn mở | Phương án chung | Phép kiểm đóng lớp |
|---|---|---|---|---|
| `kiem-lease-bo-sot-duong-vao` | Hai đuôi, hết/còn/hỏng/thiếu hạn, schema, rc; còn khác biệt bỏ hạn D2 và phụ thuộc refs | P2-cho-chu-kho | Giữ kiểm schema/authority/băm; chủ kho quyết riêng ngoại lệ hạn, khai scope refs | Các ca t20e/f/g/t21 + mutant đã đạt; quyết định D2 chưa có |
| `diff-check-tu-ha-nguong` | blank-at-eol, blank-at-eof, space-before-tab trên toàn allowlist | P2-cho-chu-kho | Chủ kho quyết chuẩn whitespace và phạm vi ngoại lệ D1 | Đã đo ba cửa độc lập + conflict; quyết định chưa có |
| `chot-yaml-chi-do-su-hien-dien` | Bảy cửa cũ đã đóng; expression continue-on-error ở bước selftest còn lọt | P2 | Chỉ nhận boolean false/vắng ở mọi chốt cấm nuốt lỗi | Literal true và biểu thức luôn/điều kiện đều phải đỏ đúng y09 |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | Checker đã giữ dữ liệu; suite không thấy bỏ thao tác gọi tất cả hoặc từng t23/t26/t27 | P2 | Kiểm tác dụng thực của từng ca, không chỉ argv và dữ liệu sạch | Ba ca lỗi độc lập; no-call và skip riêng mỗi tên đều đỏ đúng ca mới |
| `fixture-lease-phu-thuoc-actor-ci` | Actor rò vào validator trong tiến trình và validator con | P2 | Cô lập actor riêng ở fixture/test; giữ nguyên authority sản phẩm | Actor khác người cấp: fixture sạch qua; gỡ từng lớp cô lập phải đỏ đúng cửa |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | Bảng 43/55 cũ; t22 bị bỏ trong docstring; bảng thiếu phân rã và ~6 giây; docstring lease còn nói chỉ parse | P3 | Tái lập bảng cùng SHA/refs, cập nhật mọi mô tả liên quan | Inventory t/y/k + tự kiểm + số đo có scope; thay lời khai phải gây lệch phép đối chiếu |

Sáu lớp: năm giữ từ lượt trước, một mới. D1/D2 được gom vào đúng một mục quyết định bên dưới; không đếm lại thành P2 thông thường.

## BANG SAN

### HUONG 1: Phân loại và fail-close

- gia thuyet: thiếu SHA, lỗi git, đầu ra cụt hoặc sự kiện khác PR có thể mở nhanh.
- lenh: `python3 -B out/probes.py classify`.
- output: t01/t02/t03/t05/t06/t07/t08/t09/t10a–f/t11–15/t19a–b đều DAT, rc=0; mutant toàn allowlist thành day_du → `('GIET', '')`.
- ket luan: **KHONG PHAI LOI** trong các cửa đã đo. Thiếu object, rename, tệp ngoài, sự kiện push/dispatch đều được giữ đầy đủ.

### HUONG 2: Ba chấm, tự phân loại và giới hạn tiền tố

- gia thuyet: base tiến thêm hoặc đổi tên từ vùng mã sẽ bị coi là hồ sơ; mã dưới ops/land bị bỏ.
- lenh: `python3 -B out/probes.py classify` (các kho Git thật trong t11–15); `python3 -B ops/ci_duong_nhanh_test.py` trong cay.
- output: t11/t12/t14/t15 DAT; `python-under-land duong_nhanh`; full suite 46/46, 67/67, tự kiểm DAT, TONG DAT, rc=0.
- ket luan: **KHONG PHAI LOI** theo Q2/M1. `.py` dưới bốn prefix vẫn nhanh là luật đã chốt. Sửa chính classifier/workflow mặc định day_du; tác giả sửa cả mã/test là ranh giới review, không phải ranh giới an ninh của classifier. Fork/rebase thật và thay mode/symlink: **KHONG DO DUOC** ở lượt này; không dựng payload thoát cây mới.

### HUONG 3: Hai đuôi lease, schema và hạn

- gia thuyet: `.yml` hoặc hết hạn vẫn miễn các kiểm khác.
- lenh: `python3 -B out/probes.py lease`.
- output: expired-invalid/current-invalid trên `.yaml` và `.yml` đều CHAN [8] thiếu packet_issue/granted_by/reviewed_sha_required; expired-valid raw-check=8 nhưng current-errors=[]; bốn mutant miễn hết hạn/bỏ `.yml`/hạn hỏng/bỏ rc đều GIET; rc=0.
- ket luan: **KHONG PHAI LOI** cho các cửa bỏ schema cũ; **D2 CHO CHU KHO** cho ngoại lệ hạn. t21 còn đo hỏng/thiếu hạn, tệp xóa, tệp không YAML; không suy rằng đã thử mọi boundary thời gian.

### HUONG 4: D1 đo từng loại whitespace

- gia thuyet: cấu hình hiện tại bỏ whitespace ở toàn bộ miền hồ sơ, không riêng nội dung patch.
- lenh: `python3 -B out/whitespace.py`.
- output: blank-at-eol / blank-at-eof / space-before-tab đều `raw_rc 2 current_errors []`; diagnostic lần lượt trailing whitespace / new blank line at EOF / space before tab in indent; conflict-case DAT, rc=0.
- ket luan: **D1 CHO CHU KHO**. Phép hiện tại tránh chặn hồ sơ có whitespace nhưng để qua ba loại mà lệnh trần bắt; dấu xung đột vẫn bị bắt.

### HUONG 5: YAML cũ và cửa biểu thức mới

- gia thuyet: kiểm sự hiện diện cho phép vô hiệu hóa cổng kiểm rẻ hoặc nuốt kết quả selftest.
- lenh: `python3 -B out/probes.py yaml`; `python3 -B out/y09-probe.py`.
- output: y01..y09 DAT; bảy mutant cũ đều GIET. Riêng thêm `continue-on-error: ${{ true }}` vào bước tự kiểm → y01..y09 DAT; k01/k03 rc=0.
- ket luan: **LOI** ở cửa y09; bảy cửa y06/y08 đã đóng. Đây là mutant hợp lệ về cú pháp Actions, không phải lỗi parser/shell.

### HUONG 6: Dữ liệu hồ sơ còn được kiểm trước merge

- gia thuyet: bỏ lease suite vẫn bỏ sót README/caveat/prompt/băm receipt.
- lenh: `python3 -B out/probes.py data` (bản sao ngoài cay).
- output: baseline `[]`, 7.092s; xóa README, xóa dòng bảng caveat, mất evidence_url, thay byte verdict, thay byte prompt → mỗi trường hợp rc=1 đúng assertion; restored `[]`; rc script=0.
- ket luan: **KHONG PHAI LOI** ở runtime hiện tại trên những cửa này. Dòng đã xóa là dòng bảng caveat (không gọi nhầm nó là phép xóa entry mục lục độc lập). Các kiểm mới chạy trên cây, không chỉ lease trong diff.

### HUONG 7: Đột biến thao tác gọi ba ca dữ liệu

- gia thuyet: argv đúng nhưng không gọi ca vẫn qua suite.
- lenh: `python3 -B out/probes.py mutant-data`.
- output: đổi `m[ten]()` thành `m[ten]` trên bản sao → **CA 46/46, DOT BIEN 67/67, TU KIEM DAT, TONG DAT, rc=0**; bỏ README rồi gọi checker mutant → `mutant-delete-index []`.
- ket luan: **LOI**. Mutant sai hành vi sống sót; không phải mutant tương đương. Suite con tự tạo mutant từ nguồn chuẩn; phần CA được chạy với CAY trỏ bản no-call, nên kết luận là 46 ca không bắt no-call, không phải cả 67 mutant đã được dẫn xuất lại từ no-call.

### HUONG 8: Actor của CI ảnh hưởng fixture sạch

- gia thuyet: selftest của mọi PR vô tình đòi người kích hoạt có quyền cấp lease.
- lenh: `GITHUB_ACTOR=notebyme88 python3 -B cay/ops/ci_duong_nhanh_test.py --mot-ca t20a_kiem_re_ho_so_sach_dat`; `python3 -B out/actor-hint.py`.
- output: bản head HONG RuntimeError không tìm thấy lease fixture, rc=4. Chỉ cô lập actor trong tiến trình → t20a/t20d rc=3, diagnostic CHAN [4] ở tiến trình con. Chỉ cô lập con → cả hai rc=4. Cả hai lớp cô lập → cả hai rc=0.
- ket luan: **LOI** mới, hai cửa độc lập. Đây là actor đã được dùng làm ví dụ hồi quy trong lease_publish_test.py; không phải đổi policy sản phẩm.

### HUONG 9: Job/matrix/concurrency, Windows và trạng thái thật

- gia thuyet: nhánh nhanh bỏ cả job, đổi matrix, hoặc vô tình bỏ gate-registry.
- lenh: `python3 -B out/probes.py yaml` (parse YAML base/head và chạy ca cấu trúc).
- output: ba job đều `needs: chuan-bi`; matrix-identical=True; registry-identical=True; fail-fast=False; concurrency cancel-in-progress là `github.ref != 'refs/heads/master'`; pull_request không có types.
- ket luan: **KHONG PHAI LOI** cho delta đã đo. Điều kiện nền Linux/non-Linux nằm nguyên trong if bước nặng, y03 kiểm chính xác. gate-registry vẫn đầy đủ theo Q4. Push/dispatch không chọn nhanh. Nhãn windows chỉ được đọc lúc có event chạy, không tự tạo event labeled. Runner failure/cancellation, GitHub tính skipped, ba required checks và thời gian thật: **KHONG DO DUOC**, không dùng YAML làm bằng chứng success trên GitHub.

### HUONG 10: Lint, registry và manifest

- gia thuyet: YAML parse xanh che lỗi Actions, hoặc test mới không được nối.
- lenh: `python3 -B out/lint-probe.py`; registry trên tmp/base-copy và tmp/head-copy; phép gỡ DA_NOI/lời gọi ở `out/registry-mutants.log`; `python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py` trong cay; selftest và release-verify trên tmp/head-copy.
- output: actionlint base/head rc=0; mutant biểu thức rỗng trong comment run rc=1 [expression]. Registry 22/22 → 23/23, cả hai 938/938, rc=0; gỡ mục → 23/22 + “test sống chưa đăng ký”; gỡ lời gọi → “CI không gọi mục đăng ký”. Ruff tệp mới sạch; tl.py nền/head/origin/master đều 12 F821, cùng byte. Selftest 1715/1715 rc=0. Manifest strict ok=true, expected=checked=180, rc=0.
- ket luan: **KHONG PHAI LOI** trong scope đo. Lệnh release-verify đầu thiếu đối số manifest rc=2 là lỗi gọi của reviewer; đã sửa lệnh thành `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`.

### HUONG 11: Số lịch sử, scope refs và inventory

- gia thuyet: các số mới tiếp tục dùng số cũ hoặc scope khác nhau.
- lenh: `cd cay && python3 -B ../goi/do_lai_so.py`; `python3 -B out/ref-scope.py`; `python3 -B out/probes.py counts`.
- output: 345 merge/63 hồ sơ/8 raw-check đỏ; đầy đủ 552 refs → 113/113 lease đạt; cùng head chỉ một ref → 107/113 đạt, 6 lỗi bia mộ. CA=46 (34 t/9 y/3 k), mutants=67; AL_VER=4. Docstring kiem_lease còn “lease hết hạn chỉ cần YAML-parse”.
- ket luan: **LOI** inventory/bảng đo; khác biệt 6/113 đã được giải thích và tái lập bằng scope, không tiếp tục báo số 6 là bịa/sai mọi môi trường.

## BANG DO

| Khẳng định | Bảng giao khai? | Tự đo được | Khớp? |
|---|---|---|---|
| 43 ca / 55 mutant | Có, vẫn số lượt 1 | 46/46 và 67/67, rc=0 | **Không**, bảng cũ |
| t01..t21, nhánh a-g; y01..y09; k01/k02/k03 | Không | 34 t (gồm t22 và t99), 9 y, 3 k; t04 vắng | **Thiếu**, t22 nằm ngoài mô tả |
| Năm mẫu rc, ba mutant thật của tự kiểm | Không | 5 mẫu; KeyError/TIN_DUNG_GIA, comment/SONG_SOT, nới allowlist/GIET | Mô tả đã sửa đúng, **bảng vẫn bỏ sót** |
| Ba ca dữ liệu t23/t26/t27, ~6 giây | Không | Ba tên đúng; một lần sạch 7.092s trên bản sao không .git | Thiếu bảng; không coi 7.092 so ~6 là hồi quy hiệu năng, không có benchmark chuẩn |
| Registry 22/22 → 23/23; 938/938 | Có | Đúng cả hai vế, rc=0 với fixture Git không ký | Có |
| DA_NOI chỉ thêm một dòng | Có | numstat 1/0, diff đúng một mục | Có |
| actionlint rc=0, ShellCheck 0.9.0 | Có | base/head rc=0, công cụ hiện diện | Có; khác phép chỉ parse YAML |
| Ruff F tl.py 12, delta 0 | Có | base/head/origin/master 12 F821; byte bằng nhau; Ruff 0.15.15 | Có; bare lint rc=1, không gọi “Ruff hoàn toàn xanh” |
| AL_VER 4 | Có | 4 | Có; chưa là baseline sau tích hợp #668 |
| 345/63/8, khoảng 13% | Có | 345/63/8; 8/63 ≈12.70% | Có trong cửa sổ 400 first-parent từ base; không đo tỷ lệ PR tương lai |
| Lease 6/113 | Có nhưng bảng chưa ghi scope mới | 6/113 lỗi trên 1 ref; 0/113 trên 552 refs | Có theo scope; chưa đo refs của Actions |
| 52 phút, G5 46.5 phút; skipped được GitHub coi đạt | Có, khai chưa tự đo | Không PR/mạng | KHONG DO DUOC |
| tl selftest, manifest strict | Spec yêu cầu | 1715/1715; ok=true 180/180 | Đạt local |

Scope refs đầy đủ: 552 dòng từ `git -C cay for-each-ref --format='%(refname) %(objectname)'`, SHA256 `ea84411e0b70a061086877c1d6a4fbcf9fad173329eeebf1dd4452a44f27d579`. Scope hẹp: đúng `refs/heads/review 9f9bb132d2eca6d6e80b6fd1dab59e0f12466230`, SHA256 `3f562c6abbf924d0a289213105f1f0939aa69d6d31b7d57352ab7edd7c1acd18`. Head/tree giống nhau; thay tập refs là biến đo, không phải phép delta mã. Danh sách sáu lease lỗi và diagnostic nằm trong `out/ref-scope.log`.

Nghiệm thu: 1–7 có ca hành vi, cấu trúc và đột biến tự chạy; 8 có base/head + mutant comment; 9 có hai vế và hai mutant đăng ký; 10 có selftest và Ruff delta so origin/master; 11 **CHUA_DO_DUOC**. Không thấy lời khai đã đạt nghiệm thu 11. M1/M3/M4 đạt trong các cửa local đã đo; M2 còn D1/D2 và các thiếu sót kiểm thử dưới đây. Q5/#668 là điều kiện tích hợp phải kiểm lại; verdict này không duyệt head sau rebase/land #668.

## FINDINGS

### fixture-lease-phu-thuoc-actor-ci [P2] Fixture sạch làm mọi PR của actor khác người cấp lease bị đỏ

TEP/DONG: `ops/ci_duong_nhanh_test.py:276`, `:483–499`, `:527`, `:558`; workflow gọi suite ở `.github/workflows/ci.yml:547` ngoài nhánh bỏ theo che_do.

VAN DE: Helper mới tìm lease sạch bằng `lp.kiem()` trong môi trường thật. `kiem()` kiểm GITHUB_ACTOR trước hạn; actor không thuộc người cấp làm mọi ứng viên bị loại và helper ném RuntimeError. Ngay cả sửa cửa này, `chay_that()` vẫn truyền actor vào `MA_KIEM_HET_HAN` của fixture nên ca sạch đỏ vì CHAN [4]. Selftest chạy trên cả PR mã không đổi lease, nên đây là đỏ oan của test, không phải quyết định check lease thật ở D2. Hai caller t20a và t20d đều bị ảnh hưởng; đường chọn fixture trong tiến trình và đường validator con cần khóa riêng.

DA THU VA: **có**, TEST-only trong `out/HINT.patch`, trên tmp/hint-copy. Nhãn: **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
 from pathlib import Path
+from unittest import mock
@@
-    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
+    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "GITHUB_ACTOR"}
@@
-            lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT), bo_qua_han=True)
-            lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT))
+            with mock.patch.dict(os.environ, {k: v for k, v in os.environ.items()
+                                              if k != "GITHUB_ACTOR"}, clear=True):
+                lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT), bo_qua_han=True)
+                lp.kiem(lp._doc_yaml(str(tep)), str(tep), str(ROOT_THAT))
```

Chốt riêng: thêm ca con chạy t20a/t20d dưới actor `notebyme88`, đối chứng không actor và actor người cấp; kiểm actor của tiến trình cha được khôi phục. Gỡ patch.dict trong helper phải làm ca actor đỏ vì không chọn được fixture; giữ patch.dict nhưng bỏ lọc ở môi trường con phải đỏ CHAN [4]. Không xóa GITHUB_ACTOR toàn cục ở đầu suite, không thay quyền của `ops/ci_duong_nhanh.py`/`lease_publish.py`. Artifact hiện có bản vá và phép A/B ngoài suite; executor còn phải tích hợp ca chống tái diễn actor vào suite.

DA THU NGHIEM: `out/actor.log` bản gốc rc=4; `python3 -B out/actor-hint.py` cho hai bản vá nửa vời lần lượt rc=3/rc=4, cả hai lớp → t20a/t20d rc=0. Full TEST hint dưới actor này: **47/47 + 67/67, TONG DAT, rc=0**, `out/hint-full-actor.log`. Ruff F của test hint sạch. Các rc=4 của bản hỏng không được tính là “mutant GIET đúng” của bộ phân hạng hiện tại.

DO TIN: cao.

### chot-yaml-chi-do-su-hien-dien [P2] Cấm nuốt lỗi bằng identity với True bỏ lọt biểu thức Actions

TEP/DONG: `ops/ci_duong_nhanh_test.py:805`, hàm y09.

VAN DE: `b.get("continue-on-error") is not True` chỉ loại boolean True do YAML parse. Biểu thức `${{ true }}` và biểu thức điều kiện là chuỗi, nên lọt. Nếu bước sole selftest đang đỏ, Actions có thể tiếp tục với kết quả bước đã được tha. Cổng registry ở job khác chỉ kiểm lời gọi; không bắt cửa này. Các chốt y06/y08 đã dùng `is False` đúng, y09 bị bỏ sót trong cùng lớp. Không khẳng định workflow hiện tại đã thêm continue-on-error; đây là lỗ phản chứng được giao phải đo.

DA THU VA: **có**, TEST-only cùng HINT.patch.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
-    bang(b.get("continue-on-error") is not True, "buoc goi test khong duoc co continue-on-error")
+    bang(b.get("continue-on-error", False) is False, "buoc goi test khong duoc co continue-on-error")
```

Chốt riêng: literal true; `${{ true }}`; `${{ github.event_name == 'pull_request' }}` phải đỏ đúng y09, còn vắng/false xanh. Thêm ba mutant vào DOT_BIEN. Bảy cửa cũ (continue bước kiểm rẻ, comment hai lệnh, sai shell, continue ở từng required job) đã được đo độc lập, không yêu cầu vá lại.

DA THU NGHIEM: `out/y09.log`: 9/9 ca YAML và k01/k03 xanh với mutant biểu thức true; không chạy full suite riêng cho mutant này. `out/hint.log`: baseline rc=0, cả ba dạng nuốt lỗi rc=3 đúng y09; `patch -p0 --fuzz=0 --dry-run -i out/HINT.patch` trên cây sạch tạm rc=0. Full hint kết quả ở finding trên.

DO TIN: cao.

### dac-ta-bo-mat-kiem-du-lieu-ho-so [P2] Đã khôi phục dữ liệu thật nhưng suite không khóa thao tác gọi ca

TEP/DONG: `ops/ci_duong_nhanh.py:74–76`, `:243–255`; `ops/ci_duong_nhanh_test.py:593–607`.

VAN DE: Lỗ runtime lượt trước đã được sửa: `kiem-re` gọi t23/t26/t27. Tuy nhiên t22 chỉ chạy bộ này trên dữ liệu sạch và kiểm argv/rc qua đồ giả. Thay `m[ten]()` bằng `m[ten]` vẫn in DAT từng tên, rc=0; suite vẫn 46/46 và 67/67; mất README lại xanh. Giữ slug mất kiểm dữ liệu vì cùng tác dụng cần khóa, không yêu cầu sửa SPEC-r2. Không gọi việc chuyển ba ca dữ liệu vào kiểm rẻ là lệch M2; danh sách M2 cho phép giữ thêm kiểm rẻ.

DA THU VA: **có**, bổ sung test thực thi từng ca trong HINT.patch. Dùng ba hàm fixture mang đúng tên, lần lượt chỉ một hàm ném sentinel; gọi qua chính subprocess của checker. Không cần chạy toàn suite lease nặng.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
+@ca
+def t22b_ca_du_lieu_phai_thuc_thi_tung_ca():
+    m = nap_module()
+    with tempfile.TemporaryDirectory(prefix="cdn_data_calls_") as d:
+        root = Path(d)
+        (root / "ops").mkdir()
+        checker = root / "ops/lease_publish_test.py"
+        for dich in m.CA_DU_LIEU:
+            marker = "CHOT_DU_LIEU_" + dich
+            checker.write_text("\n".join(
+                "def " + ten + "():\n    " +
+                ("raise AssertionError(" + repr(marker) + ")" if ten == dich else "pass")
+                for ten in m.CA_DU_LIEU), encoding="utf-8")
+            loi = m.kiem_ca_du_lieu(root, chay_that)
+            bang(len(loi) == 1 and marker in loi[0],
+                 f"{dich}: ca do phai thuc su duoc goi va truyen loi, duoc {loi}")
```

Chốt riêng: mutant no-call toàn bộ và ba mutant bỏ từng tên t23/t26/t27; mỗi mutant phải rc=3 đúng t22b và đúng sentinel/tên ca đích. Giữ t22 kiểm danh sách tên cố định để vòng lặp không trở thành tập rỗng. Dữ liệu thật làm đối chứng: prompt/băm/evidence_url → t23/t26 đỏ; README/caveat → t27 đỏ. Không chỉ đòi đủ ba dòng DAT, vì mutant no-call vẫn in được ba dòng đó. Thêm bốn mutant vào DOT_BIEN khi executor tái dẫn xuất.

DA THU NGHIEM: `out/mutant-data.log` xác nhận mutant sống sót full suite và mất README vẫn `[]`; `out/data.log` xác nhận bản đúng bắt các dữ liệu hỏng. `out/hint.log`: baseline t22b rc=0; no-call và bỏ từng ca đều rc=3 đúng t22b/tên đích. Full hint 47/47, 67/67, rc=0; bốn mutant mới được đo ngoài suite, chưa tự nhận chúng là một phần con số 67.

DO TIN: cao.

### bang-do-thieu-neo-va-thieu-kiem-ke [P3] Bảng giao vẫn ở lượt 1 và bỏ sót lời khai của bản vá

TEP/DONG: `goi/DO_LAI.md:9`, bảng số lease; `ops/ci_duong_nhanh_test.py:5`, `:18–20`; `ops/ci_duong_nhanh.py:203`, `:244–246`.

VAN DE: Bảng vẫn 43/55 trong khi head có 46/67. Sửa mô tả t01..t22 cũ thành t01..t21 rồi thêm t22 trong cùng bản vá làm mô tả lại thiếu. Bảng chưa kiểm kê phân rã t/y/k, năm mẫu rc/ba mutant thật và lời khai mới ba ca/~6 giây. Theo yêu cầu packet, các khẳng định định lượng bị bỏ sót là finding dù bản thân một số đã đúng. Ngoài ra docstring kiem_lease còn “lease hết hạn chỉ cần YAML-parse”, trái trực tiếp cách gọi validator mới. Số 6/113 không còn là finding về không tái lập: đã tái lập 6 lỗi theo scope một ref, 0 lỗi theo scope 552 refs; chỉ bảng chưa cập nhật điều kiện đo.

DA THU VA: **chưa áp phần tài liệu**; đã đo inventory/scope. Hint nội dung:

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
-  1. Hành vi bộ phân loại và bước kiểm rẻ (các ca `t01`..`t21`, gồm nhánh a-g): đồ giả cho ca thuần + KHO GIT THẬT
+  1. Hành vi bộ phân loại và bước kiểm rẻ (t01–t22, không có t04, có các nhánh; t99 tự kiểm riêng): đồ giả + KHO GIT THẬT
```

```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@
-    """Lease CÒN HẠN đổi trong PR phải qua `lease_publish.py check`; lease hết hạn chỉ cần YAML-parse."""
+    """Lease còn hạn qua check; lease hết hạn qua kiem(bo_qua_han=True), vẫn kiểm các chốt khác. D2 chờ chủ kho."""
```

```diff
--- goi/DO_LAI.md
+++ goi/DO_LAI.md
@@
-| 43 ca / 55 dot bien bi giet dung ly do | `python3 ops/ci_duong_nhanh_test.py` (trong `cay/`) | do tren Linux, khong Windows; dot bien la thu executor tu nghi ra |
+| 46 ca / 67 dot bien tren head 9f9bb132d2eca6d6e80b6fd1dab59e0f12466230 | python3 -B ops/ci_duong_nhanh_test.py | Linux; xem phan ra va pham vi mutant ben duoi |
+| Phan ra ca, tu kiem, ba ca du lieu va thoi gian | AST/danh sach CA, DOT_BIEN; do kiem_ca_du_lieu | Ghi SHA, moi truong, scope va log; khong ngoai suy CI |
+| 6/113 va 0/113 lease loi | kiem(bo_qua_han=True) cung head, hai tap refs | Dinh kem danh sach refs + bam, danh sach failure; chua do Actions |
```

Hunk bảng là hướng cập nhật gói bàn giao; không đưa nó vào artifact HINT.patch chỉ dành cho TEST. Executor phải dẫn xuất số mới sau khi thêm test, không ghim 46/67 cho mọi head sau. Chốt riêng: đối chiếu tên ca từ cấu trúc; đổi số hoặc khoảng tên phải bị phát hiện; ghi riêng năm mẫu rc/ba mutant; đo ba ca và thời gian với điều kiện; đổi tập refs phải đổi receipt scope. Không ngoại suy “Actions không có ops refs” từ phép clone một ref — refs thực của runner còn chưa đo.

DA THU NGHIEM: `out/counts.log`, `out/measure.log`, `out/ref-scope.log`, `out/data.log`. Mô tả tự kiểm k và năm/ba đã đúng trên head; phần thiếu bảng/t22 vẫn mở. Chưa có checker tài liệu mới được triển khai; không tuyên bố hint docs đã đóng lớp.

DO TIN: cao về inventory/số đo; không đánh giá thời gian GitHub hay refs Actions chưa quan sát.

## CHO-CHU-KHO-QUYET

**Một mục quyết định chung, hai hàng P2-cho-chu-kho. Không yêu cầu executor tự vá D1/D2, không coi lời khai đã xin quyết định là phê duyệt.**

| Quyết định / slug | Hạng | Tác động hiện tại tự đo | Phần chưa quyết |
|---|---|---|---|
| D1 / `diff-check-tu-ha-nguong` | **P2-cho-chu-kho** | Cấu hình tinh chỉnh cho qua cả ba loại whitespace mà raw --check trả 2, kể cả `.md` ngoài patch; conflict vẫn đỏ. Lịch sử raw bắt 8/63 PR hồ sơ trong scope đo. | Đây là tránh đỏ với whitespace có chủ ý hoặc để lọt lỗi whitespace tùy chuẩn chủ kho chọn; chữ trần M2 chưa cấp ngoại lệ. Chưa có quyết định đóng băng phạm vi/chuẩn mới. |
| D2 / `kiem-lease-bo-sot-duong-vao` | **P2-cho-chu-kho** | Lease hợp lệ đã hết hạn: raw check=8, hiện tại đạt; hết hạn sai schema vẫn đỏ ở cả hai đuôi. Một ref có 6/113 lỗi bia mộ, 552 refs 0/113: có thể đỏ do thiếu scope refs. | Bỏ hạn là khác check trần. Không thấy lọt schema qua hai cửa cũ; không chứng minh mọi semantics check tương đương ở GitHub. Cần quyết định ngoại lệ hạn và khai phạm vi refs/đối xử khi không đủ dữ liệu. |

TEP/DONG D1: `ops/ci_duong_nhanh.py:66`, `:174–185`; D2: `:70–73`, `:202–240`.

DA THU VA: không đảo chính sách D1/D2. Đã thử các mutant chốt lân cận trên bản sao; `.yml`, hết hạn sai schema, bỏ rc đều bị giết đúng. Hint **khai báo quyết định**, không phải sửa cấu hình:

```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@
-đúng là lệch đặc tả; ĐANG CHỜ QUYẾT ĐỊNH CỦA CHỦ KHO ở Issue #674, không tự coi là đã duyệt):
+đúng là lệch đặc tả; ĐANG CHỜ QUYẾT ĐỊNH CỦA CHỦ KHO ở Issue #674, không tự coi là đã duyệt).
+Lượt 2: D1 bỏ ba loại whitespace trên toàn allowlist; D2 giữ schema nhưng bỏ hạn.
+Lỗi bia mộ còn phụ thuộc refs: cùng head, 1 ref = 6/113 lỗi; 552 refs = 0/113 lỗi.
+Chưa đo scope refs của Actions; các số này không tự cấp ngoại lệ đặc tả:
```

Chốt riêng D1: giữ ba phép whitespace tách biệt và conflict-marker; sau quyết định, chiều assertion/mutant phải phản ánh đúng chuẩn được duyệt, không tự nhận mutant khôi phục lệnh raw là lỗi spec. Chốt riêng D2: giữ cả đuôi, các trạng thái hạn, schema/authority/băm và rc; đối chứng lease sạch hết hạn/còn hạn; đo cùng dữ liệu với phạm vi refs cụ thể. Chưa dựng phép tấn công/thoát cây mới. Quyết định phải ở hồ sơ chủ kho, không chỉ đổi docstring thành “đã duyệt”.

DA THU NGHIEM: `python3 -B out/whitespace.py`, `python3 -B out/probes.py lease`, `python3 -B out/ref-scope.py`, `cd cay && python3 -B ../goi/do_lai_so.py` đều hoàn tất rc=0 và có output kể trên. DO TIN: cao trong phạm vi local.

## DOT BIEN SONG SOT VA HINT

- **Sống sót full suite:** bỏ `()` trong `MA_CHAY_CA`; 46/46 và 67/67, rc=0; checker mất chức năng bắt README hỏng.
- **Sống sót ca cấu trúc/registry đã chạy:** continue-on-error biểu thức true ở bước selftest; y01..y09 và k01/k03 xanh. Không khai đã chạy full suite riêng cho mutant này.
- Mutant comment tương đương trong tự kiểm sống sót là **đúng kỳ vọng**, không phải finding. Lỗi KeyError vô can được phân hạng TIN_DUNG_GIA, không đếm GIET.
- HINT.patch chỉ sửa `ops/ci_duong_nhanh_test.py`; nhãn **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**. Dry-run `patch -p0 --fuzz=0` thành công. Hai ca mới/sửa được đo baseline rồi mutant riêng; toàn bản hint chạy dưới actor khác người cấp: 47/47, 67/67, tự kiểm DAT, TONG DAT, rc=0. Bốn mutant data và ba mutant y09 mới đo ngoài bộ 67; phải tích hợp khi executor vá.
- Không tạo artifact patch workflow/authority; không ghi thay Spec-r2. Các diff trong finding là hint, không phải commit được duyệt.

## KIEM TRA CUOI

HEAD và tree giữ nguyên; tracked diff=0, index diff=0; `git status --porcelain --ignored` không có dòng. Băm SPEC-r2 giữ nguyên. Selftest sinh dữ liệu trong `tmp/head-copy`, không chạy trong checkout đọc-only. Trạng thái ignored được đọc sau khi đã bắt đầu vài suite, không có snapshot băm mọi ignored trước test; không tuyên bố chứng minh chưa từng có ghi rồi hoàn nguyên. Các số ở đây lấy từ log đã kết thúc; `out/PROGRESS.md` lưu phần ghi tăng dần trước khi tổng hợp.

Không approve, không merge/land. Protocol §8 giới hạn hai lượt Codex/PR: lượt 2 còn finding thì chuyển checkpoint/chủ kho quyết cách tách hoặc sửa thiết kế, không tự mở lượt Codex tiếp theo. Mọi quyết định sau đó vẫn phải neo đúng SHA và giữ assurance của packet sensitive.

TONG: P0=0 P1=0 P2=3 P2-cho-chu-kho=2 P3=1
So lop: 6 (5 ke thua, 1 moi). Ba P2 thong thuong + hai P2 cho chu kho + mot P3; khong dem trung D1/D2.
