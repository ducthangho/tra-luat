verdict: changes_requested
reviewed_sha: b86c4a35b610cc040b63c5b9a0cf29710329d529
Reviewed commit: b86c4a35b610cc040b63c5b9a0cf29710329d529

Ngưỡng sensitive: **0 P0/P1/P2/P3**. Còn **1 P2, 1 P3**, thuộc hai lớp đã có lịch sử. Các lỗi được xác lập ở độ phủ chốt chống hồi quy: HEAD hiện có gọi loader nghiêm, có chặn cây khác và có in kiểm kê; không đánh tráo mutant thành hành vi đang hỏng trên HEAD.

Tree `9050f6f1323451e66e5c8f639fcf559f77164623`. SPEC-r2 đã đọc trọn, SHA256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` đúng. Diff review so master `89fc4fac8cea65979cc2483043dc8cd07a6e8518`: đúng bốn tệp được giao. So baseline bất biến `1741e0a1ab7ebce4b26912aefadca56ddfcdc691` thêm `ops/lease_publish_test.py` và `ops/specs/t131-deadline-dem-spawn.md`; cả hai giống hệt master, không phải thay đổi packet. `.claude/dev/ci_dang_ky_test.py` đúng 1 thêm/0 xóa vào DA_NOI.

Reviewer: Codex/OpenAI, phiên API có công cụ shell cục bộ; executor Claude theo gói giao. Không có runtime receipt độc lập về model/effort/transport launcher; không suy assurance từ GitHub actor. Review nội dung này không tạo quyền land, không xác nhận #668 đã land.

Môi trường: Linux, Python 3.11.15 (workflow dùng 3.12), actionlint 1.7.7, ShellCheck 0.9.0, Ruff cài sẵn 0.16.9 (khác pin workflow 0.15.15). Không mạng, không Windows CI, không PR thật. Bare Ruff bên dưới dùng 0.16.9 nhất quán cả nền/head; không khai đã chạy bare lint bằng pin 0.15.15.

Quy ước lệnh: cwd là workspace rv5 trừ lệnh ghi `cd`; trước mọi phép dùng temp đã đặt `TMPDIR="$PWD/tmp"`, `PYTHONDONTWRITEBYTECODE=1`. Test dùng Git fixture còn đặt `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`; repo có core.abbrev=7. Mọi bản sao/mutant/hint nằm trong `tmp/`, bằng chứng trong `out/`. Không sửa `cay/`, không commit/push/merge. `out/final-check.log`: tracked/index/untracked/ignored sạch, HEAD/tree/spec giữ nguyên; đây là đối chiếu trạng thái quan sát, không phải bằng chứng chưa từng ghi rồi hoàn nguyên trong lịch sử.

## DOI CHIEU LUOT TRUOC

Nguồn: `goi/LUOT-TRUOC-VERDICT.md`, lượt 4, SHA `7b8c85631a8945fc0631bfc4e9338ca4584c7e3c`. Hai finding còn mở được giữ slug. Các lớp đã đóng cũng được kiểm lại để tránh hồi quy. D1/D2 là erratum đã duyệt theo chỉ thị, không ghi finding chính sách.

| Lớp | Kết luận | Bằng chứng reviewer tự đo |
|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | **VA HO ở cấp lớp**; hai biểu hiện runner/matrix của lượt 4 **đã vá thật** | `out/yaml.log`: runner và matrix chỉ Windows đều rc=3, đúng y13; `out/topology.log`: 31/31 thay đổi cấu trúc bị bắt. y14/y15/t95 bắt mutant có sẵn. Tuy nhiên, ngắt lời gọi guard từ main hoặc đổi reader thực sang safe_load vẫn FULL xanh 58/58 + 123/123; xem P2. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | **VA HO ở cấp lớp**; lỗi phân nhóm của lượt 4 **đã vá thật** | AST decorator độc lập cho 35/15/3/5, sáu mutant phân nhóm/số đếm đỏ đúng t96. Nhưng bỏ lời gọi in neo KIEM KE khỏi main vẫn FULL xanh; xem P3. |
| `kiem-lease-bo-sot-duong-vao` | **DA VA THAT** trong phạm vi local đã giao | t20a..g/t21 đạt, lease còn/hết hạn, schema, hai đuôi, hạn hỏng/thiếu, rc; AST `kiem` chỉ dùng bo_qua_han ở một điều kiện so hạn. Scope refs Actions vẫn chưa đo. |
| `diff-check-tu-ha-nguong` | **DA VA THAT** theo D1 | Ba probe riêng blank-at-eol/blank-at-eof/space-before-tab: raw=2, thực=[]; conflict fixture vẫn đỏ. Chuỗi cấu hình đúng ba ngoại lệ. |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | **DA VA THAT** trong phạm vi trước | t22/t22b đạt; từng sentinel t23/t26/t27 được gọi và truyền lỗi; ca dữ liệu thật `loi=[]`. Suite giết no-call, bỏ tên, cwd sai, nuốt ngoại lệ. |
| `fixture-lease-phu-thuoc-actor-ci` | **DA VA THAT** | t23 với actor lạ đạt và khôi phục actor; hai mutant bỏ cô lập trong fixture/env con bị giết. |
| `tin-dung-dot-bien-khong-co-ca-dich` | **DA VA THAT** | t97/t99 đạt; tu_kiem_phan_hang=[]; empty/unknown/iterator/generator/caller/callee/baseline đỏ có đối chứng. |

Không đóng hai lớp tái diễn bằng tổng suite xanh. Kết quả S3 tiếp tục yêu cầu checkpoint của điều phối/chủ kho; verdict này không tự mở thêm lượt review.

## BANG LOP

| Slug | Các biểu hiện/cửa vào | Hạng cao nhất còn mở | Phương án vá chung | Phép kiểm đóng lớp |
|---|---|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | Workflow/job/step if; continue-on-error; source OS/matrix/include/exclude/runner/needs; defaults/env/shell/timeout/uses/thứ tự; thân run mới; loader; nguồn cây được đo | P2 | Giữ khóa cấu trúc, thêm kiểm hành vi qua chính entry point sử dụng guard/reader | y11–y15; 31 probe cấu trúc; main từ chối cây khác trước suite; doc_wf thực từ chối cả khóa trùng và gộp; mutant ngắt từng đường gọi phải đỏ đúng |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | Metadata nhóm, AST, tổng/phân rã, chuỗi kiểm kê, lời gọi in vào output thật | P3 | Kiểm dữ liệu và nơi công bố dữ liệu; không dùng kết quả hàm dựng chuỗi làm bằng chứng đã in | t96 kiểm nghĩa/số; test main capture stdout đòi đúng một dòng neo; mutant bỏ/đổi dòng in phải đỏ |
| `kiem-lease-bo-sot-duong-vao` | Đuôi/schema/hạn/rc/authority/refs | Không mở local | Giữ validator, chỉ bỏ hạn theo D2 | t20/t21 + mutants; khai riêng refs Actions chưa đo |
| `diff-check-tu-ha-nguong` | Ba ngoại lệ whitespace/conflict | Không mở | Giữ D1 đúng phạm vi | Ba đối chứng raw/thực + conflict |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | Tập tên/call/cwd/rc ba ca dữ liệu | Không mở | Thực thi ca dữ liệu thật | t22/t22b/sentinel và mutants |
| `fixture-lease-phu-thuoc-actor-ci` | Actor trong fixture và subprocess | Không mở | Cô lập môi trường fixture | t23 + hai mutants |
| `tin-dung-dot-bien-khong-co-ca-dich` | Rỗng/lạ/iterator/baseline/rc sai tên | Không mở | Đòi bằng chứng dương và phân hạng đúng | t97/t99 + 5 mẫu rc/3 mutant thật |

Bảy lớp kế thừa; hai còn mở với ba biểu hiện mới được đo. `dependency-failure-skips-required-checks` là đầu mối DAC TA/NGOAI-PHAM-VI được phân tích riêng, không tính vào P hay số lớp finding. Thân run của bước có sẵn ngoài packet được giữ NGOAI-PHAM-VI như chỉ thị; không dùng nó tạo finding.

## BANG SAN

HUONG 1: Ba trạng thái, sự kiện và output
  gia thuyet : thiếu SHA/git lỗi/đầu ra cụt hoặc push/dispatch có thể mở nhanh.
  lenh       : `python3 -B out/probes.py classify`; `(cd cay && python3 -B ops/ci_duong_nhanh_test.py)`
  output     : t01/t02/t03/t05/t06/t07/t08/t09/t10/t16/t17/t18/t19 DAT; force_full_allowlist=('GIET',''); FULL CA 58/58, DOT BIEN 123/123, TU KIEM DAT, TONG DAT, rc=0.
  ket luan   : KHONG PHAI LOI trong miền đã đo. Mutant nới scripts/.github/ops, fail-open, gọi Git ở push, ghi output sai đều có phép giết riêng.

HUONG 2: Ngữ nghĩa Git ba chấm, rename/xóa và prefix
  gia thuyet : base tiến thêm hoặc rename mã sang hồ sơ làm phân loại sai.
  lenh       : `python3 -B out/probes.py classify`
  output     : t11/t12/t13/t14/t15 DAT trên kho Git thật; python-under-land: duong_nhanh.
  ket luan   : KHONG PHAI LOI theo M1/Q2. `.py` trong allowlist vẫn nhanh là chính sách. Sửa classifier/workflow nằm ngoài allowlist; khả năng PR tự sửa chính sách thuộc review authority, không phải ranh giới chống tác giả cố ý. Fork/rebase GitHub thật KHONG DO DUOC.

HUONG 3: Lease còn/hết hạn, schema, đuôi và actor
  gia thuyet : D2 bỏ thêm chốt khác hoặc fixture phụ thuộc người bấm CI.
  lenh       : `python3 -B out/probes.py lease-data`
  output     : t20a..g/t21/t23 DAT; bo_qua_han branches=['not bo_qua_han and han <= datetime.now(timezone.utc)'].
  ket luan   : KHONG PHAI LOI ở các cửa đã đo. Hàm vẫn kiểm schema, authority, bia mộ, reviewed SHA, lớp review, neo prompt và parse hạn.

HUONG 4: D1 không bỏ rộng hơn ba loại whitespace
  gia thuyet : cấu hình nới whitespace làm mất conflict check.
  lenh       : `python3 -B out/probes.py whitespace`
  output     : blank-at-eol raw=2 actual=[]; blank-at-eof raw=2 actual=[]; space-before-tab raw=2 actual=[]; t20c DAT.
  ket luan   : KHONG PHAI LOI theo erratum D1.

HUONG 5: Dữ liệu hồ sơ còn được kiểm khi bỏ suite nặng
  gia thuyet : t23/t26/t27 chỉ được in tên hoặc đọc nhầm cây.
  lenh       : `python3 -B out/probes.py lease-data`; `(cd cay && python3 -B ../goi/kiem_ke.py)`
  output     : t22/t22b DAT; ba ca du lieu tren kho that: loi=[] | 5.5s (may nay).
  ket luan   : KHONG PHAI LOI trong miền đo. Gate-registry không thay đổi so master. T27 vẫn giữ kiểm mục lục review, push/dispatch trở về các bước đầy đủ.

HUONG 6: Topology và điều kiện YAML
  gia thuyet : y13 còn bỏ sót source OS, matrix, runner, defaults hoặc khóa thực thi.
  lenh       : `python3 -B out/probes.py yaml`; `python3 -B out/topology.py`
  output     : y01..y15/k01..k03 DAT; mutant runner/matrix rc=3 đúng y13; STRUCTURAL_PROBES: 31/31; y11/y12 bắt if job/step; y14 bắt exit trước test/exit ở che-do/bước thêm ngoài bảng.
  ket luan   : KHONG PHAI LOI cho topology đã đo. 31 probe dùng cấu trúc đã parse và mock reader để đo assertion riêng, không khai mọi biến thể là workflow GitHub hợp lệ hay đã chạy Windows. Các full-mutant về đường gọi reader được tách ở hướng 7.

HUONG 7: Dây nối guard/reader thực
  gia thuyet : helper còn đúng nhưng entry point không dùng helper thì suite vẫn xanh.
  lenh       : `python3 -B out/probes.py guard-call`; `python3 -B out/more-mutants.py loader-call`; `python3 -B out/hints.py`
  output     : guard-call FULL rc=0, 58/58 + 123/123; loader-call FULL rc=0, 58/58 + 123/123. HEAD main foreign CAY rc=2/rejected=True/entered-suite=False; mutant rejected=False/entered-suite=True. Reader HEAD REJECTED khóa trùng, mutant ACCEPTED.
  ket luan   : LOI P2, cùng lớp chot-yaml. Probe main dùng runner giả/CA rỗng để tránh đệ quy; FULL xanh trên mỗi bản mutant là phép chạy suite riêng, không suy từ probe giả.

HUONG 8: Phân nhóm và neo bảng đo
  gia thuyet : nhóm đã đúng nhưng bỏ công bố kiểm kê mà suite vẫn báo đạt.
  lenh       : `python3 -B out/probes.py inventory`; `(cd cay && python3 -B ../goi/kiem_ke.py)`; `python3 -B out/more-mutants.py inventory-print`
  output     : AST độc lập 35/15/3/5; sáu mutant t96 đều rc=3 đúng tên; inventory-print FULL rc=0, 58/58 + 123/123, TONG DAT, không có KIEM KE.
  ket luan   : LOI P3 về neo output, không phải số hiện tại sai.

HUONG 9: Tín dụng giết mutant
  gia thuyet : lỗi vô can/tập đích rỗng hoặc baseline đỏ bị tính thành GIET.
  lenh       : `python3 -B out/probes.py credit`
  output     : t97/t99 DAT; tu_kiem_phan_hang=[]; FULL báo 5 mẫu rc, 3 mutant thật DAT.
  ket luan   : KHONG PHAI LOI ở các cửa đo; không lấy rc=0 riêng làm bằng chứng suite đạt.

HUONG 10: Actionlint và đăng ký thật
  gia thuyet : biểu thức trống trong run không bị bắt hoặc test mới chưa nối cổng.
  lenh       : `(cd cay && actionlint .github/workflows/ci.yml)`; `python3 -B out/probes.py lint`; chạy `ci_dang_ky_test.py` ở cay và tmp/base (git archive 1741e0a).
  output     : actionlint nền/head rc=0; comment trong run có biểu thức rỗng rc=1 [expression]; đăng ký 22/22→23/23, phản chứng 938/938 cả hai; numstat 1/0.
  ket luan   : KHONG PHAI LOI. Lần probe đầu đặt comment ngoài scalar run là fixture sai và rc=0; log sửa đúng là out/lint-mutant-corrected.log.

HUONG 11: chuan-bi failure/cancelled/timeout và concurrency
  gia thuyet : dependency bị lỗi làm các check required không chạy.
  lenh       : script đối chiếu `git show {1741e0a,89fc4fa,HEAD}:.github/workflows/ci.yml` và parse YAML (`out/dependency.log`).
  output     : cả ba mốc required dependencies={'gate':'chuan-bi','gate-ops':'chuan-bi','gate-packet-loop':'chuan-bi'}; concurrency giống nhau; HEAD thêm checkout/phan-loai có continue-on-error=True và fallback day_du; gate-registry identical=True.
  ket luan   : KHONG DO DUOC conclusion/check protection trên GitHub; phần topology gốc có sẵn từ #548, không gán thành lỗi mới của executor. Phân tích DAC TA bên dưới.

HUONG 12: Hint bắt đúng hồi quy đã tìm
  gia thuyet : hint chỉ kiểm helper mới hoặc gây đỏ vô can.
  lenh       : `python3 -B out/hints.py`; `(cd tmp/head-copy && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch)`.
  output     : HINT BASE t94/t95/y15/t96 DAT; HINT MUTANT guard-call, guard-wrong-operand, loader-call, inventory-print DO đúng assertion; dry-run rc=0.
  ket luan   : KHONG PHAI LOI trong A/B tập trung. Lần thử đầu neo __file__ vào cây cũ khiến t96 đọc thiếu ca mới, đã sửa rig sang bản sao hint-tree; không tính lần sai đó là lỗi sản phẩm. Kết quả full hint cập nhật cuối tệp. Lần chạy lại rig còn gặp pack Git read-only khi copy đè bản sao đã có; đã tái sử dụng bản sao đó, không đổi permission hay cây review (out/hints-repeat-setup-error.log).

## BANG DO

| Khẳng định / nguồn khai | Đầu đo | Kết quả tự đo | Khớp / giới hạn |
|---|---|---|---|
| CA, DOT BIEN, TU KIEM, TONG | Suite HEAD, out/suite.log | 58/58, 123/123, DAT, DAT; rc=0 | Có |
| Phân rã nhóm | AST decorator độc lập, t96, kiem_ke.py, KIEM KE thật | 35 hành vi + 15 YAML + 3 đăng ký + 5 tự kiểm = 58 | Có trên HEAD; đường công bố còn lỗ P3 |
| Mutant theo tệp | DOT_BIEN/kiểm kê | 44 sản phẩm + 17 TEST + 60 YAML + 2 sổ = 123 | Có |
| Tự kiểm phân hạng | MAU_RC/TU_KIEM_DOT_BIEN, chạy thực | 5 mẫu rc, 3 mutant thật | Có; ngoài 123 |
| IF_BUOC_CHUAN / BO_QUA | kiem_ke.py + reader YAML | If 3/12/7/0/2; bước bỏ 5/3/1 | Có |
| Ba ca dữ liệu, ~6–9s | kiem_ke.py | 3 ca, loi=[], 5.5s | Số đúng; thời gian phụ thuộc máy, không suy Actions |
| 345/63/8 và ~13% | do_lai_so.py, out/measure.log | 345 diff đo được, 63 toàn prefix, 8 raw --check đỏ; 8/63≈12.70% | Có, trong cửa sổ 400 merge first-parent từ 1741e0a; không phải PR thật |
| 113 lease | do_lai_so.py | 113/113 đạt, 0 trượt | Có ở clone được cấp |
| 552 ref trong số đo lịch sử | docstring khai rõ scope cũ; for-each-ref lượt này | 556 ref; out/refs.txt SHA256 6cd7e0e947d76682a643f2f26acc680e7f9cf5a73525de1ed128b44ad5892aef | Không gọi 552 là số hiện tại; không suy completeness của GitHub |
| 6/113 ở clone một ref | Lời khai lịch sử có giới hạn | Không dựng lại clone single-branch lượt này | CHUA_DO_DUOC, không lấy làm nghiệm thu local |
| Đăng ký 22→23 / phản chứng 938 | Chạy base/head | 22/22→23/23; 938/938 cả hai | Có |
| Một dòng DA_NOI | Git numstat baseline/head | 1/0 | Có |
| Ruff tl.py 12 F, delta=0 | Ruff 0.16.9 nền/head | 12 F821 cả hai; scripts/tl.py không đổi so origin/master=89fc4fa; hai tệp mới sạch F | Có với version local, không nhận là bare lint 0.15.15 |
| actionlint toàn bộ workflow | Base/head cùng actionlint 1.7.7 + ShellCheck 0.9.0 | Cùng rc=1, một SC1003 tại ops-don-ref.yml:117 | Delta=0, ngoài packet; out/actionlint-base-all.log |
| AL_VER 4 | Regex t152 trên ci.yml | 4 | Có; không khai #668 đã tích hợp |
| Manifest strict | release-verify RELEASE_MANIFEST.json --strict --json trên bản sao | rc=0, ok=true, expected_file_count=checked_file_count=180 | Có, không đổi manifest |
| 52 phút, G5 46,5 phút / GitHub skipped | Run/API/tài liệu ngoài gói | Không mạng, không PR thật | KHONG DO DUOC; không đạt nghiệm thu 11 trước land |
| Three reviewer mutants survive | Ba log full riêng | guard-call, loader-call, inventory-print đều 58/58 + 123/123, rc=0 | Hai lớp finding; không gộp vào mutant executor đã giết |

Không xác lập số phân nhóm sai mới trên HEAD. Finding bảng đo hiện là mất neo thật mà không bị test phát hiện. Các con số lịch sử đã được khai scope/giới hạn, không đổi chúng thành khẳng định hiện tại để tạo lỗi giả.

### chot-yaml-chi-do-su-hien-dien [P2] Chốt mới chỉ được kiểm qua helper, ngắt đường gọi thật vẫn qua toàn suite

TEP/DONG: `ops/ci_duong_nhanh_test.py:1110` (y15), `:1177` (t95); các đường gọi cần bảo vệ ở `:735` (doc_wf), `:1655` (main).

VAN DE: y15 đưa văn bản phản chứng trực tiếp vào `doc_wf_tu`, còn t95 gọi trực tiếp `loi_cay_duoi_do`. Do vậy chúng chứng minh helper còn đúng, chưa chứng minh các entry point thực sự sử dụng helper. Hai cửa cùng cơ chế đã đo:

1. **Nguồn cây:** xóa bốn dòng gọi/xử lý `loi_cay_duoi_do` khỏi main. Helper và t95 nguyên vẹn. FULL xanh; main với CAY khác đi vào suite thay vì trả rc=2 trước khi chạy. Cửa tương đương là gọi helper với ROOT_THAT ở cả hai đối số, hoặc bỏ nhánh return khi helper báo lỗi. Đây là hàng rào bảo đảm phép đo y* đang kiểm đúng cây chứa test.
2. **Nguồn cấu trúc YAML:** đổi duy nhất reader `doc_wf()` từ `doc_wf_tu(...)` sang `yaml.safe_load(...)`. Helper nghiêm và y15 nguyên vẹn. FULL xanh; reader thực chấp nhận fixture khóa trùng có sẵn của y15. Hai dạng cần chặn riêng là khóa trùng và khóa gộp `<<`; cách sửa phải đi qua reader mà y* thật dùng. Không cần tự tạo payload mới.

Đây tiếp tục là lớp “có guard/lời gọi ở một nơi không chứng minh đường chạy thật được bảo vệ”, không tách slug theo hai hàm vừa thấy. Các cửa workflow cấp top/job/step, source OS, runner, matrix/include/exclude/needs, body run của bước packet, đăng ký ca đã có phép đo riêng; không yêu cầu đóng băng thân run cũ ngoài scope. P2 là lỗ chống hồi quy trong các chốt được giao rõ để đóng lớp, không khẳng định HEAD hiện đang chấp nhận cây khác hay khóa trùng.

DA THU VA: có — TEST-only. Hint giữ helper tests và kiểm thêm caller. Trích diff cụ thể:

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
-        with contextlib.suppress(TinHieuChotCa):
-            doc_wf_tu(vb)
-            bat = True
+        with tempfile.TemporaryDirectory(prefix="cdn_yaml_reader_") as d:
+            cay_tam = Path(d)
+            tep = cay_tam / ".github" / "workflows" / "ci.yml"
+            tep.parent.mkdir(parents=True)
+            tep.write_text(vb, encoding="utf-8")
+            with mock.patch.dict(globals(), {"CAY": cay_tam}, clear=False):
+                with contextlib.suppress(TinHieuChotCa):
+                    doc_wf()
+                    bat = True
@@
 def t95_lan_chay_day_du_chi_do_kho_chua_test():
     bang(loi_cay_duoi_do(ROOT_THAT, ROOT_THAT) == "", "kho that phai duoc nhan")
     bang(loi_cay_duoi_do(Path(tempfile.gettempdir()), ROOT_THAT) != "", "cay khac kho chua test phai bi tu choi o lan chay day du")
+    import io
+    with tempfile.TemporaryDirectory(prefix="cdn_main_scope_") as d:
+        ra, err = io.StringIO(), io.StringIO()
+        with mock.patch.dict(globals(), {"CAY": Path(d), "CA": {}}, clear=False), \
+             mock.patch.dict(globals(), {"chay_tap_dot_bien": lambda _: (0, []),
+                                         "tu_kiem_phan_hang": lambda: []}, clear=False), \
+             contextlib.redirect_stdout(ra), contextlib.redirect_stderr(err):
+            rc = main([])
+        bang(rc == 2 and "CAY DUOI DO KHAC KHO CHUA TEST" in err.getvalue()
+             and "CA:" not in ra.getvalue() and "TONG:" not in ra.getvalue(),
+             "main phai tu choi cay ngoai TRUOC khi chay/in ket qua suite")
```

Chốt riêng: main cây đúng vẫn chạy; cây khác trả 2, diagnostic đúng và không in CA/TONG; ngắt call, truyền sai operand, bỏ return phải làm t95 đỏ. Reader: baseline thật parse được, cả hai fixture trùng/gộp phải đỏ qua doc_wf; chuyển reader sang safe_load phải làm y15 đỏ. Đưa các mutant này vào DOT_BIEN bằng neo duy nhất; không chỉ thêm test mà bỏ mutant. Hint đã thử guard-call, sai operand, bỏ return, reader-call; cả bốn đỏ đúng. Executor cần bổ sung các cửa này vào bảng mutant bền.

DA THU NGHIEM: `out/guard-call.log`, `out/loader-call.log`: mỗi mutant FULL rc=0, 58/58 + 123/123, TONG DAT. `out/hints-final.log`: baseline t95/y15 DAT, ba mutant tương ứng DO đúng TinHieuChotCa. Probe entry point: HEAD foreign-CAY rc=2/rejected=True/entered-suite=False; mutant rejected=False/entered-suite=True. Reader khóa trùng HEAD REJECTED, mutant ACCEPTED. Các phép entry point dùng bản sao và fixture có sẵn, không sửa cây review.

DO TIN: cao về lỗ caller coverage đã đo; không tuyên bố GitHub đã chạy workflow khóa trùng hoặc tác giả PR đã khai thác nó.

### bang-do-thieu-neo-va-thieu-kiem-ke [P3] Kiểm kê đúng trong hàm nhưng bỏ neo khỏi output thật vẫn báo TONG DAT

TEP/DONG: `ops/ci_duong_nhanh_test.py:1184` (t96), `:1293` (dong_kiem_ke), `:1673` (main in kiểm kê); `goi/DO_LAI.md` và `goi/kiem_ke.py` dùng dòng đó làm neo khai báo.

VAN DE: phần phân nhóm lượt trước đã sửa đúng bằng metadata và đối chiếu AST. Tuy nhiên t96 gọi `dong_kiem_ke()` trực tiếp để kiểm số. Xóa riêng dòng `print(dong_kiem_ke())` ở main vẫn FULL rc=0, 58/58 + 123/123 + TU KIEM DAT + TONG DAT, không có KIEM KE. Vì vậy bộ test không giữ hợp đồng “neo của mọi bảng số là dòng được in cùng suite”; `kiem_ke.py` có thể tiếp tục in số từ hàm nhưng artifact suite đã mất neo. Lớp cần đóng gồm khai metadata → nghĩa nhóm → tổng/phân rã → định dạng dòng → xuất dòng thật; bốn đoạn đầu đạt, đoạn cuối chưa có chốt. Không cáo buộc con số HEAD đang sai.

DA THU VA: có — thêm ca tự kiểm capture output `main([])`, dùng runner con giả để tránh gọi suite đệ quy; vẫn dùng CA/DOT_BIEN thật và t96 làm thước số độc lập.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
+@ca_tu_kiem
+def t94_main_in_dong_kiem_ke_that():
+    import io
+    ra = io.StringIO()
+    with mock.patch.dict(globals(), {
+        "CAY": ROOT_THAT,
+        "chay_ca_trong_tien_trinh": lambda _: ("DAT", ""),
+        "chay_tap_dot_bien": lambda _: (len(DOT_BIEN), []),
+        "tu_kiem_phan_hang": lambda: [],
+    }, clear=False), contextlib.redirect_stdout(ra):
+        rc = main([])
+    bang(rc == 0 and ra.getvalue().splitlines().count(dong_kiem_ke()) == 1,
+         "main phai in dung mot dong KIEM KE duoc doi chieu doc lap boi t96")
+
```

Chốt riêng: thiếu dòng, đổi dòng ở call site, hoặc in hai lần đều phải đỏ; ghép với t96 để thay sai số trong generator cũng đỏ. Mutant tối thiểu đã đo là bỏ `print(dong_kiem_ke())`; thêm vào DOT_BIEN và giữ mutant sai nhóm/sai số vốn có. Ca mới phải khai @ca_tu_kiem, để AST không tái tạo lỗi phân nhóm cũ.

DA THU NGHIEM: `python3 -B out/more-mutants.py inventory-print` → FULL rc=0, 58/58 + 123/123, không KIEM KE (`out/inventory-print-full.log`). `python3 -B out/hints.py` → hint baseline t94/t96 DAT, bỏ print DO đúng assertion (`out/hints-final.log`). Không lấy output dựng bằng tay làm neo.

DO TIN: cao. Đây là lỗ bảo vệ bằng chứng, hạng P3; không nâng thành lỗi runtime phân loại.

## DAC TA / NGOAI-PHAM-VI: dependency-failure-skips-required-checks

Đo diff cho thấy job chuan-bi, nguồn os, needs của cả ba job và concurrency đã có trên baseline trước packet. Việc một dependency không thành công làm consumer không chạy là đầu mối phải kiểm trên GitHub; conclusion required-check và quyền merge không đo được offline, không khai chúng đã tái hiện.

**Rủi ro mới do #674 thêm:** tiền nhiệm trước chỉ `run: true`, nay có checkout đầy đủ và chạy Python từ cây PR. Thêm phụ thuộc mạng/đọc repo/thời gian và mã vào tiền nhiệm làm tăng cơ hội timeout/runner failure; continue-on-error giải lỗi bước thông thường, không chứng minh job luôn kết thúc thành công khi runner/job bị hủy. Bước che-do dùng echo trên non-PR được y14 khóa, không thêm công việc dài đáng kể. Không có dữ liệu Actions để định lượng phần tăng.

**Phần có sẵn từ #548:** runner không nhận job, cancellation, dependency failure và đồ thị needs; concurrency hủy lượt cũ cũng giữ nguyên. Không gán toàn bộ rủi ro này thành P của executor. Cách sửa gốc `if: always()` cấp job kèm guard trạng thái dependency đụng luật cấm if cấp job (`loi_g5_workflow`, ngoài write set logic DA_NOI) và topology đóng băng. Cần authority/spec revision hoặc successor packet: required jobs chạy guard kiểm needs.result/ma trận, trạng thái thiếu/failure/cancelled phải có bằng chứng thất bại phù hợp; rồi thử trên PR thật với tiền nhiệm fail/timeout/cancel và kiểm cả check conclusion lẫn ruleset. Không tự yêu cầu executor sửa spec r2 hoặc mở write set.

## NGHIEM THU VA GIOI HAN

1–5: chạy độc lập t01/t02/t03/t05/t06/t08 cùng các ca Git thật; suite giết các mutant nới allowlist/fail-open/push/workflow. Mutant force-all-allowlist-full của reviewer cũng GIET.

6–7: các mutant gỡ PR guard, luôn bỏ bước nặng, thêm paths/paths-ignore bị giết đúng trong 123/123; y11–y14 và các probe bổ sung có log. Những ca này đạt không phủ nhận hai cửa caller P2.

8: actionlint HEAD rc=0 với ShellCheck 0.9.0; fixture sửa đúng chèn biểu thức trống bên trong run → rc=1 [expression].

9: base 22/22, head 23/23, cả hai 938/938; DA_NOI 1/0. Mutant gỡ mục và gỡ lời gọi bị giết bởi đúng k/y trong suite.

10: Ruff F delta=0 bằng Ruff local 0.16.9. Full tl selftest lần đầu 1714/1715 do một ca cố ghi `/root/tra-luat` trên filesystem read-only; không phải delta packet. Chạy lại với LOCALAPPDATA nằm trong scratch; kết quả terminal được cập nhật dưới đây.

11: **CHUA_DO_DUOC**, cần PR thật chỉ đổi hồ sơ với log DUONG_NHANH, ba check success và số đo thời gian. Không thấy lời khai đã đạt nghiệm thu 11 trong gói giao. Không ngoại suy tiết kiệm thời gian từ số test.

Không chạy Windows; không đo fork/rebase/synthetic merge thực, runner refs, trạng thái GitHub required-check, sự kiện con, thời gian/cancel thực. Symlink/mode và shell/YAML injection ngoài các fixture được giao: không dựng nội dung tấn công hay đường thoát cây; hướng cần payload mới chỉ mô tả, không coi là passed.

`out/HINT.patch` chỉ sửa TEST, đường dẫn repo-relative, dry-run `patch -p0 --fuzz=0` đạt; nhãn: **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**. Hint chưa thêm các mutant mới vào DOT_BIEN; executor phải tích hợp chúng và tự đo. A/B reviewer không tạo authority commit.

## CAP NHAT CUOI

Tất cả phép dùng làm kết luận đã kết thúc:

- `LOCALAPPDATA="$PWD/tmp/local-appdata" python3 -B tmp/head-copy/scripts/tl.py --selftest` → **1715/1715**, rc=0 (`out/tl-selftest-corrected.log`). Không sửa test; chỉ đưa đường dữ liệu mặc định vào scratch qua biến cấu hình được sản phẩm hỗ trợ. Lần đầu bị EROFS vẫn được giữ trong log. Nghiệm thu local 1–10 có bằng chứng; giới hạn Ruff version đã khai.
- `(cd tmp/hint-tree && python3 -B ops/ci_duong_nhanh_test.py)` trên bản sao áp hint → **59/59**, **123/123**, KIEM KE **35/15/3/6**, TU KIEM DAT, TONG DAT, rc=0 (`out/hint-full.log`). Đây là hint thử trên bản sao, không phải code đã sửa ở cây review. Các mutant reviewer chưa nằm trong bảng 123, đã được đo A/B riêng.
- `python3 -B out/hints.py` lần cuối → baseline t94/t95/y15/t96 DAT; **7 mutant** caller/output DO đúng: ngắt guard, sai operand, bỏ return, reader safe_load, thiếu dòng, sai dòng, hai dòng. `out/hints-final.log` giữ diagnostic thật. Patch TEST-only dry-run -p0 --fuzz=0 đạt.
- Ba mutant reviewer **SỐNG SÓT full suite trước hint**: guard-call, loader-call, inventory-print; mỗi bản rc=0, 58/58 + 123/123, TONG DAT. Không lấy 123/123 để tuyên bố đã giết chúng.
- actionlint tất cả workflow: base/head cùng một SC1003 có sẵn trong ops-don-ref.yml; riêng ci.yml rc=0 cả hai. Không gán lỗi nền vào packet.
- Trạng thái cây review cuối: sạch tracked/index/untracked/ignored; HEAD/tree/spec đúng. Mọi hiện vật thay đổi của reviewer ở out/tmp.

D1/D2 không còn finding chính sách. Rủi ro dependency được ghi DAC TA/NGOAI-PHAM-VI, không tính P. Giữ **changes_requested** do hai finding có bằng chứng ở trên; không tự mở thêm vòng review, không suy quyền land.

TONG: P0=0 P1=0 P2=1 P3=1
So lop: 7; 2 con mo, 5 dong trong pham vi local da do. Ba bieu hien moi trong hai lop con mo.
