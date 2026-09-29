verdict: changes_requested
reviewed_sha: 7b8c85631a8945fc0631bfc4e9338ca4584c7e3c
Reviewed commit: 7b8c85631a8945fc0631bfc4e9338ca4584c7e3c

Ngưỡng sensitive theo chỉ thị: **0 P0/P1/P2/P3**. Hiện có **1 P2 và 1 P3**, cùng hai lớp đã có lịch sử. Không approve.

Base `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; tree HEAD `1acd2b6f1306c124e44e15db8432366b56a18478`. SPEC-r2 đọc trọn, SHA256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` khớp. Đã đọc quy tắc kho và protocol §8/8.3. Bốn tệp diff đúng write set; sổ đăng ký đúng một dòng thêm/không xóa. Không sửa `cay/`, không commit/push/merge.

Reviewer: Codex/OpenAI theo danh tính phiên, dùng công cụ shell của phiên API; executor Claude theo gói giao. Không có runtime receipt độc lập để chứng minh model/effort/launcher transport; không suy assurance từ GitHub actor. Verdict này là kết quả review nội dung, không phải quyền land.

Môi trường Linux, Python 3.11.15; workflow khai 3.12. actionlint 1.7.7 có ShellCheck 0.9.0, Ruff 0.15.15. Không mạng, không Windows CI, không PR thật. Mọi lệnh bên dưới tính từ workspace rv4 trừ khi chỉ rõ cwd. Lệnh dùng temp đều đặt `TMPDIR="$PWD/tmp"`; Python `-B`/`PYTHONDONTWRITEBYTECODE=1`, Ruff `--no-cache`. Sổ đăng ký và full selftest dùng `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`; core.abbrev=7 ở cấu hình repo, không ép qua môi trường.

## DOI CHIEU LUOT TRUOC

Nguồn `goi/LUOT-TRUOC-VERDICT.md`, lượt 3, SHA `3d12524b21a6a932a71606f290676186e7d3be7d`. Giữ nguyên slug; quyết định D1/D2 đã duyệt theo prompt/erratum Issue #674 comment 5887720007, không xét lại chính sách.

| Lớp/finding lượt trước | Kết luận lượt này | Bằng chứng tự đo |
|---|---|---|
| `kiem-lease-bo-sot-duong-vao` / D2 | **DA VA THAT** trong các cửa đã giao; phần chờ chủ kho đã được giải quyết | `out/lease-data.log`: sạch đạt; còn/hết hạn sai schema bị chặn; `.yaml`/`.yml`, hạn hỏng/thiếu, rc được kiểm bởi t20/t21. `out/extra.log`: AST `kiem` chỉ bỏ nhánh so hạn, vẫn đọc hạn; suite giết các mutant bỏ kiểm lease/đuôi/rc. Scope refs Actions vẫn chưa đo. |
| `diff-check-tu-ha-nguong` / D1 | **DA VA THAT** theo erratum, không đòi đảo chính sách | `out/extra.log`: từng loại blank-at-eol/blank-at-eof/space-before-tab raw=2, actual=[]; conflict marker vẫn đỏ; cấu hình bằng đúng ba ngoại lệ được duyệt. |
| `chot-yaml-chi-do-su-hien-dien` | **VA HO** | y06/y11 khóa cả tiền nhiệm và mọi job; y12 khóa các if bước; bộ chuẩn giết mutant cũ. Nhưng đổi runner của gate-ops vẫn qua full 53/53 + 95/95 và actionlint; bước selftest chỉ Linux không còn đủ điều kiện chạy. Finding P2 bên dưới. |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | **DA VA THAT** trong phạm vi trước | t22 chạy dữ liệu thật, t22b sentinel từng t23/t26/t27 đều đỏ đúng; mutant no-call/bỏ ca/cwd sai/nuốt lỗi bị giết. Không dùng rc-only để suy sentinel đã gọi. |
| `fixture-lease-phu-thuoc-actor-ci` | **DA VA THAT** | t23 chạy với actor lạ, phục hồi actor cha; hai mutant bỏ lọc env con/bỏ patch.dict đều bị giết trong suite. Không thay authority validator sản phẩm. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | **VA SINH LOI MOI** trong cùng lớp | Đã kiểm kê riêng 5 mẫu rc/3 mutant thật và bỏ số ghim. Nhưng `kiem_ke.py` gán 3 ca tự kiểm vào nhóm “t hành vi”: khai 38, phân hoạch thực 35+3. Finding P3 bên dưới. |
| `tin-dung-dot-bien-khong-co-ca-dich` | **DA VA THAT** | `out/credit.log`: t97 DAT (empty/unknown/iterator/generator, caller/callee, baseline đỏ sẵn); tu-kiem=[]; các mutant gỡ vật hóa/cấm rỗng/baseline đều GIET đúng trong 95/95. |

## BANG LOP

| Slug | Các biểu hiện/cửa vào | Hạng cao nhất còn mở | Phương án vá chung | Phép kiểm đóng lớp |
|---|---|---|---|---|
| `kiem-lease-bo-sot-duong-vao` | Đuôi, schema, hạn, rc, authority/refs | Đóng trong phạm vi local đã giao | Giữ validator và scope được duyệt | Ma trận t20/t21, mutants; khai refs Actions chưa đo |
| `diff-check-tu-ha-nguong` | Ba whitespace và conflict marker | Đóng theo D1 | Giữ đúng chuỗi cấu hình | Ba probe độc lập + conflict |
| `chot-yaml-chi-do-su-hien-dien` | Job/step if và nuốt lỗi đã khóa; đầu vào runner/matrix/source/topology chưa khóa | P2 | Kiểm cả điều kiện lẫn nguồn giá trị quyết định bước bắt buộc có chạy | Baseline xanh; source OS, runner, matrix trực tiếp/include/exclude, needs có chốt/mutant riêng |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | Chọn/gọi t23/t26/t27, cwd/rc | Đóng trong phạm vi trước | Giữ ba ca dữ liệu thật và sentinel từng ca | t22/t22b và mutant riêng |
| `fixture-lease-phu-thuoc-actor-ci` | Fixture trong tiến trình và validator con | Đóng | Cô lập actor ở fixture | t23 và hai mutant |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | Lời khai/nhóm đếm không đồng nghĩa; tự kiểm bị tính vào hành vi | P3 | Phân hoạch có tên rõ ràng và không giao nhau | 35 hành vi + 12 YAML + 3 đăng ký + 3 tự kiểm = 53; mẫu đại diện từng nhóm |
| `tin-dung-dot-bien-khong-co-ca-dich` | Empty/unknown/iterator/caller/callee/baseline | Đóng | Vật hóa trước đọc, đòi bằng chứng dương | t97 + tự kiểm và mutant của harness |

Bảy lớp kế thừa; hai lớp còn mở. S3: hai lớp lặp chưa được đóng chỉ bằng tổng suite xanh. Không tự mở vòng review tiếp theo; quyền xử lý checkpoint thuộc điều phối/chủ kho.

## BANG SAN

HUONG 1: Ba trạng thái và sự kiện
  gia thuyet : SHA/git/đầu ra lỗi hoặc sự kiện không phải PR có thể mở nhanh.
  lenh       : `python3 -B out/probes.py classify`; `cd cay && python3 -B ops/ci_duong_nhanh_test.py`
  output     : t01/t02/t03/t05/t06/t07/t08/t09/t10/t16/t17/t18/t19 DAT; force-full=('GIET',''); chuẩn CA 53/53, DOT BIEN 95/95, TU KIEM DAT, TONG DAT, rc=0.
  ket luan   : KHONG PHAI LOI trong miền đo. Allowlist nới, fail-open, push gọi git, ghi output sai có mutant riêng bị giết.

HUONG 2: Ba chấm, rename, xóa, miền prefix
  gia thuyet : base tiến thêm hoặc rename từ mã sang hồ sơ làm sai phân loại.
  lenh       : `python3 -B out/probes.py classify`
  output     : t11/t12/t13/t14/t15 DAT trên Git thật; python-under-land: duong_nhanh; sửa classifier/workflow vào day_du qua t08.
  ket luan   : KHONG PHAI LOI theo M1/Q2. `.py` dưới prefix vẫn nhanh là chính sách đã chốt. PR sửa chính bộ phân loại/workflow thuộc ranh giới review. Fork/rebase thật trên GitHub: KHONG DO DUOC.

HUONG 3: Lease và actor
  gia thuyet : bỏ hạn kéo theo bỏ schema/đuôi/rc hoặc làm fixture phụ thuộc người chạy.
  lenh       : `python3 -B out/probes.py lease-data`; `python3 -B out/extra.py`
  output     : t20a..t20g/t21/t23 DAT; AST chỉ một nhánh `if not bo_qua_han and han <= ...`; hàm vẫn gọi schema, authority, bia mộ, neo prompt và đọc hạn.
  ket luan   : KHONG PHAI LOI trong các cửa đo; D2 được duyệt. Không tuyên bố refs của Actions bằng clone đủ.

HUONG 4: Whitespace và conflict
  gia thuyet : D1 bỏ thêm lỗi ngoài ba loại cho phép.
  lenh       : `python3 -B out/extra.py`
  output     : ba loại riêng đều raw=2/current=[]; `conflict-marker DAT`; cấu hình `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab`.
  ket luan   : KHONG PHAI LOI theo D1.

HUONG 5: Dữ liệu thật còn được kiểm ở fast path
  gia thuyet : ba hàm dữ liệu chỉ được in tên mà không gọi, hoặc gọi sai cây/nuốt lỗi.
  lenh       : `python3 -B out/probes.py lease-data`; `cd cay && python3 -B ../goi/kiem_ke.py`
  output     : t22b DAT cho sentinel riêng từng ca; t22 DAT; `ba ca du lieu tren kho that: loi=[] | 8.6s`; mutants tương ứng bị giết trong suite.
  ket luan   : KHONG PHAI LOI trong phạm vi đo. gate-registry giữ nguyên cấu trúc và vẫn chạy; push/dispatch trở về đầy đủ theo t03/y02/y03.

HUONG 6: Điều kiện YAML và nguồn runner
  gia thuyet : if Linux giữ nguyên nhưng nguồn runner không còn Linux, bộ tự kiểm vẫn xanh.
  lenh       : `python3 -B out/probes.py yaml`
  output     : nền y01..y12/k01..k03 DAT; mutant `gate_ops_runner_windows` actionlint=0, FULL rc=0, 53/53 + 95/95 + TU KIEM DAT + TONG DAT.
  ket luan   : LOI P2. Đây là mutant trên bản sao, không phải khẳng định HEAD đang chạy Windows. Mutant `gate_ops_matrix_windows` cũng actionlint=0 và FULL rc=0, 53/53 + 95/95 + TU KIEM DAT + TONG DAT.

HUONG 7: Harness và tín dụng giả
  gia thuyet : empty/iterator bị tiêu thụ hoặc ca nền đỏ vẫn được ghi GIET.
  lenh       : `python3 -B out/probes.py credit`
  output     : t97/t98/t99 DAT; `tu-kiem []`; chuẩn 5 mẫu rc, 3 mutant thật DAT.
  ket luan   : KHONG PHAI LOI trong các cửa trước đây và baseline đỏ đã đo.

HUONG 8: Kiểm kê định lượng
  gia thuyet : đếm theo cấu trúc vẫn gán sai nhóm ca.
  lenh       : `cd cay && python3 -B ../goi/kiem_ke.py`; `python3 -B out/extra.py`
  output     : bảng khai `t hanh vi=38,y=12,k=3`; độc lập `t=35,y=12,k=3,tu_kiem=3`; MAU_RC=5, TU_KIEM_DOT_BIEN=3.
  ket luan   : LOI P3 về nghĩa của nhóm, không phải sai tổng 53 hay bỏ sót lại 5/3.

HUONG 9: Lint và đăng ký
  gia thuyet : parser YAML bỏ qua biểu thức hỏng; test mới chưa nối vào cổng.
  lenh       : `cd cay && actionlint .github/workflows/ci.yml`; `python3 -B out/probes.py lint`; chạy ci_dang_ky_test trên head và base-copy.
  output     : HEAD actionlint=0, ShellCheck 0.9.0; mutant expression rỗng rc=1 `[expression]`; base ĐĂNG KÝ 22/22, head 23/23, cả hai PHẢN CHỨNG 938/938/TỔNG ĐẠT; diff sổ 1 thêm/0 xóa.
  ket luan   : KHONG PHAI LOI. Lần đầu registry lỗi ký Git là rig; chạy lại sau khi tắt ký cho fixture đã đạt.

HUONG 10: Hint có răng
  gia thuyet : hint chỉ khóa cửa Windows vừa thấy và bỏ các cửa cùng cơ chế.
  lenh       : `python3 -B out/hints.py`; `cd tmp/head-copy && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch`
  output     : `hint baseline DAT`; 22 biến thể runner/needs/matrix/include/exclude/source bị chốt bắt đúng; patch dry-run rc=0.
  ket luan   : KHONG PHAI LOI trong A/B tập trung của hint. Đây không phải full suite sau hint; topology mutant có vòng chỉ là thử assertion, không tính là workflow hợp lệ sống sót.

## BANG DO

| Khẳng định | Đầu khai / phạm vi | Đo được | Khớp? |
|---|---|---|---|
| CA N/N; mutant M/M; tự kiểm | Bộ test HEAD | 53/53; 95/95; 5 mẫu rc + 3 mutant thật DAT | Có |
| Phân rã ca | `goi/kiem_ke.py:10–12` | Khai 38 hành vi; thực 35 hành vi, 3 tự kiểm, 12 YAML, 3 đăng ký | **Không**, P3 |
| Mutant phân theo tệp | kiem_ke | Python sản phẩm 44; TEST 7; YAML 42; đăng ký 2; tổng 95 | Có |
| If bước / bước nặng | kiem_ke và hằng test | If theo job: 3/12/7/0/2; bước bỏ gate=5, gate-ops=3, packet-loop=1 | Có |
| Ba ca dữ liệu ~6–7s | DO_LAI, phụ thuộc máy | Đo 8.6s / 8.81s, kết quả [] | Số ca đúng; thời gian là ước lượng, không coi chênh máy là hồi quy |
| Lịch sử 345/63/8 | 400 merge first-parent từ base 1741e0a | do_lai_so.py: 345/63/8 | Có; không phải phép đo PR thật |
| Lease 113, scope 552 ref | do_lai_so.py/DO_LAI | Ref count=552; tên/OID lưu out/refs.txt, SHA256 13dd07b227c223015305ff70e78e20b38a0d48be91acb54bddf1dbab075d4515; `113 tep; dat 113, truot 0`, rc=0 | Không suy từ số refs sang tính đầy đủ của GitHub |
| 6/113 ở clone một nhánh | Lịch sử reviewer, đã khai scope | Chưa dựng lại clone một nhánh lượt này | KHONG DO DUOC trong phép đã chạy; không gọi 6 là số kho đầy đủ |
| Đăng ký 22→23, phản chứng 938 | Head/base cùng suite | 22/22→23/23; 938/938 cả hai | Có |
| Một dòng DA_NOI | git diff --numstat base HEAD | 1/0 | Có |
| Ruff tl.py 12 F, delta=0 | origin/master cục bộ 89fc4fac8cea65979cc2483043dc8cd07a6e8518 | 12 F821 ở base/head; scripts không đổi so origin/master; hai tệp mới sạch F | Có |
| AL_VER 4 | Regex t152 | 4 | Có; không khai #668 đã tích hợp |
| Manifest strict | scripts/tl.py release-verify trên bản sao HEAD | ok=true, expected_file_count=checked_file_count=180, rc=0 | Có |
| 52 phút, G5 46,5 phút; GitHub skipped | Lịch sử run/API/tài liệu ngoài gói | Không mạng; không PR mới | KHONG DO DUOC; không lấy làm bằng chứng nghiệm thu 11 |

Các log nằm trong `out/`; script probe và hint cũng lưu ở đó. Không có lời khai định lượng bị bỏ sót mới được xác lập ngoài lỗi phân nhóm nêu trên. Không dùng bảng của executor làm trần tìm kiếm. Lần gọi do_lai_so sai cwd đầu tiên đã lỗi ModuleNotFoundError, được chạy lại đúng cwd; không lấy output 0/0/0 của lần sai làm kết luận.

### chot-yaml-chi-do-su-hien-dien [P2] Chốt giữ if Linux nhưng không giữ đường chọn runner để bước tự kiểm thực sự chạy

TEP/DONG: `ops/ci_duong_nhanh_test.py:845` (y09), `:914` (y11), `:923` (y12); cấu hình liên quan `.github/workflows/ci.yml:492` và `:553`.

VAN DE: y09 yêu cầu bước selftest mang `runner.os == 'Linux'`; y12 đóng băng chuỗi if; cả hai bỏ qua nguồn runner thực. Chỉ đổi `gate-ops.runs-on` từ `${{ matrix.os }}` thành `windows-latest`, giữ toàn bộ if/run, vẫn qua actionlint và full suite. Khi chạy trên Windows, biểu thức Linux không cho bước gọi test chạy. Nếu ma trận vẫn ghi ubuntu-latest, nhãn job còn có thể ghi ubuntu trong khi runner là Windows. Điều này phá hợp đồng M3 rằng test của packet phải nối vào job bắt buộc ngoài đường bị bỏ, và giữ nguyên cơ chế cũ “có dòng điều kiện/lời gọi” thay cho kiểm có thực thi. Đây là lỗ chốt chống hồi quy; HEAD hiện tại vẫn dùng runner đúng. Không khẳng định đã đo conclusion/success trên GitHub hay đã chạy Windows.

Cả lớp cần xét: (1) nguồn `chuan-bi.outputs.os`; (2) consumer `strategy.matrix.os`; (3) `matrix.include`/`exclude` có thể loại/ghi đè Linux; (4) `runs-on` đọc sai ma trận; (5) `needs` trỏ sai nguồn/chuỗi phụ thuộc; cùng các job/step if và continue-on-error đã khóa ở lượt này. Cửa shell/defaults/env làm thay đổi thực thi chưa có phép đo hành vi đầy đủ; không tự soạn payload vô hiệu hóa shell hay thoát cây, theo chỉ thị. Không tuyên bố hint dưới đây giải quyết mọi biến đổi shell.

DA THU VA: có — TEST-only, hint khóa hợp đồng định tuyến chung thay vì thêm riêng chuỗi cấm Windows. Không đề nghị sửa workflow HEAD đang đúng.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
+@ca
+def y13_dinh_tuyen_runner_khong_lam_mat_ca_linux():
+    wf = doc_wf()
+    cb = wf["jobs"]["chuan-bi"]
+    bang(cb.get("runs-on") == "ubuntu-latest" and "strategy" not in cb and "needs" not in cb,
+         "chuan-bi: runner/topology phai giu nhu hop dong")
+    os_chuan = "(github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '[\"ubuntu-latest\",\"windows-latest\"]' || '[\"ubuntu-latest\"]'"
+    bang(chuan_hoa_if(cb.get("outputs", {}).get("os")) == os_chuan,
+         "chuan-bi: output os phai bao dam Linux tren moi su kien")
+    for job in (*BAT_BUOC, "gate-registry"):
+        cau = wf["jobs"][job]
+        bang(cau.get("needs") == "chuan-bi", f"{job}: sai duong phu thuoc")
+        bang(cau.get("runs-on") == "${{ matrix.os }}", f"{job}: runner khong doc matrix.os")
+        bang(cau.get("strategy") == {"fail-fast": False, "matrix": {
+            "os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}},
+            f"{job}: matrix khong doc tron output os, hoac co include/exclude/ghi de")
```

Chốt riêng và mutant cần nhập vào DOT_BIEN: source output mất Linux; chuan-bi đổi runner; mỗi consumer đổi runs-on; mỗi consumer đặt matrix chỉ Windows; thêm include/exclude; đổi needs. `out/hints.py` đã đo A/B các cửa đó qua cấu trúc (22 biến thể). Hai mutant workflow hợp lệ dùng cho full suite nằm ở `tmp/gate_ops_runner_windows` và `tmp/gate_ops_matrix_windows`. Với needs, chọn đồ thị hợp lệ khi thêm vào suite; mutant có vòng bị actionlint bắt không phải bằng chứng riêng của chốt này. Nếu #668 thay topology, cập nhật hợp đồng cùng review tích hợp, không nới tùy ý.

DA THU NGHIEM: `python3 -B out/probes.py yaml` — runner mutant FULL rc=0, 53/53 + 95/95, actionlint=0. `python3 -B out/hints.py` — nền DAT; 22 biến thể DO bằng TinHieuChotCa đúng lời giải thích; dry-run patch rc=0. Chưa chạy full suite sau hint và chưa thêm đầy đủ mutant vào DOT_BIEN trong hint; executor tự tích hợp, đo lại.

Rủi ro hint: ghim topology có thể đỏ khi đổi cấu trúc CI hợp lệ; cần cập nhật có review, đặc biệt sau #668. `out/HINT.patch` chỉ chứa TEST, nhãn **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**.

DO TIN: cao về lỗ kiểm cấu trúc và mutant sống sót; giới hạn GitHub/Windows như đã khai.

### bang-do-thieu-neo-va-thieu-kiem-ke [P3] Bảng đếm mới vẫn gộp ba ca tự kiểm vào nhóm hành vi

TEP/DONG: `goi/kiem_ke.py:10–12`; `goi/DO_LAI.md` dòng “MỌI TẤT CẢ số lượng”. Đây là lỗi gói bằng chứng, không mở write set kho.

VAN DE: biểu thức Counter định loại t97/t98/t99 khỏi nhánh `t`, nhưng nhánh else trả lại `k[0]`, cũng là `t`. Output ghi rõ “t hành vi” = 38, sau đó lại liệt kê ba ca tự kiểm riêng. Phân hoạch đúng: **35 hành vi + 12 YAML + 3 đăng ký + 3 tự kiểm = 53**. Tổng 53 không sai; lỗi là số và nghĩa của phân rã không khớp. Đã sửa cửa thiếu 5/3 của lượt trước, nhưng thước đo mới sinh lỗi cùng lớp.

DA THU VA: có — thử trên bản sao `tmp/kiem_ke_hint.py`; người dựng bundle sửa script/bảng, không sửa SPEC-r2 hay cây executor.

```diff
--- goi/kiem_ke.py
+++ goi/kiem_ke.py
@@
-nhom = collections.Counter(("t" if k[0] == "t" and k[:3] != "t97" and k[:3] != "t98" and k[:3] != "t99" else k[0]) for k in CA)
+nhom = collections.Counter("tu_kiem" if k[:3] in ("t97", "t98", "t99") else k[0] for k in CA)
```

Chốt riêng: mẫu một t hành vi, mỗi t97/t98/t99, một y và một k; đòi nhóm đúng cho từng tên và tổng hợp đúng, không chỉ tổng=len(CA). Đột biến trả nhánh else cũ phải đỏ. Các inventory khác (95 theo tệp, 5/3 tự kiểm phân hạng, if/bước bỏ) giữ phép đối chiếu riêng; không dùng tổng 53 để chứng minh tất cả đúng. Nên bổ sung nhãn `tu_kiem` vào dòng chú giải output.

DA THU NGHIEM: `cd cay && python3 -B ../goi/kiem_ke.py` khai 38/12/3; `python3 -B out/extra.py` đo 35/12/3/3. Hint chạy thật in `t=35,y=12,k=3,tu_kiem=3`; A/B tập đại diện: bản cũ DO, hint DAT, mutant trả lại nhánh cũ DO (`out/inventory-hint.log`, `out/inventory-ab.log`). Rủi ro: phân nhóm bằng tiền tố phải được sửa khi có loại ca mới; tốt hơn metadata nhóm rõ ràng nếu suite tiếp tục mở rộng.

DO TIN: cao.

## NGHIEM THU VA GIOI HAN

1–5: t01/t02/t03/t05/t06/t08, Git thật và mutants đã tự chạy. Mutant toàn allowlist→day_du riêng của reviewer cũng GIET.

6–7: mutant gỡ điều kiện PR/luôn bỏ bước nặng/paths/paths-ignore đều bị giết trong 95/95. Lỗ bổ sung runner là finding P2, không phủ nhận các ca bắt buộc đã chạy.

8: actionlint rc=0 có ShellCheck; expression rỗng rc=1 đúng diagnostic.

9: base 22/22, head 23/23, 938/938 cả hai; diff 1/0; mutant gỡ mục/lời gọi bị giết đúng k/y.

10: Ruff F delta=0 so origin/master cục bộ; full tl selftest trên bản sao HEAD đạt **1715/1715**, rc=0 (`out/tl-selftest.log`).

11: **CHUA_DO_DUOC**; cần PR thật chỉ đổi hồ sơ. Không thấy gói giao khai đã đạt 11. Không suy tiết kiệm thời gian từ số cũ hoặc số ca.

Không đo GitHub thực: required checks success/skipped/cancelled; concurrency; fork/rebase và base SHA theo sự kiện; scope refs runner. Không chạy Windows theo chỉ thị. Hướng symlink/mode đặc biệt và shell injection cần nội dung mới được giữ ở mô tả, không tự soạn payload. Các giới hạn này không được chuyển thành passed.

## CAP NHAT CUOI

Tất cả phép dùng làm kết luận đã kết thúc:

- `export TMPDIR="$PWD/tmp" PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false; (cd tmp/head-copy && python3 -B scripts/tl.py --selftest)` → **1715/1715**, rc=0.
- `(cd cay && python3 -B ../goi/do_lai_so.py)` → **345/63/8**, **113/113 lease đạt**, rc=0. Bản đo full refs không xác minh số 6 của clone một nhánh; scope đã khai riêng.
- Hai mutant reviewer **SỐNG SÓT full suite**: `gate_ops_runner_windows` và `gate_ops_matrix_windows`, mỗi bản **53/53 + 95/95 + TU KIEM DAT + TONG DAT**, rc=0; actionlint=0. Không nhận tổng mutant của executor làm bằng chứng hai mutant reviewer đã bị giết.
- `out/hints.log`: hint TEST nền xanh, 22 biến thể đỏ đúng assertion; patch dry-run -p0 --fuzz=0 rc=0. Hint inventory sửa phân nhóm đúng và mutant quay lại logic cũ đỏ. Chưa chạy toàn suite với hint TEST; không khai hint đã sẵn sàng commit.
- `out/final-check.log`: HEAD/tree đúng; tracked/index diff rc=0; `git status --short --ignored` rỗng; băm SPEC-r2 giữ nguyên. Đây là kiểm trạng thái cuối, không phải snapshot chứng minh mọi byte ở mọi thời điểm; các phép sinh dữ liệu chạy trong tmp, không vá cây review.

D1/D2 không còn finding chính sách. Nghiệm thu local 1–10 đã có bằng chứng chạy; vẫn changes_requested do hai finding bổ sung. Nghiệm thu 11 chưa đo. Không tự mở lượt 5 hay suy quyền land từ verdict này.

TONG: P0=0 P1=0 P2=1 P3=1
So lop: 7; 2 con mo, 5 dong trong pham vi da do.
