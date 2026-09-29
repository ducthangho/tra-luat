verdict: changes_requested
reviewed_sha: abcafde0d5ed3ebadabb29d712b2b7325003112c
Reviewed commit: abcafde0d5ed3ebadabb29d712b2b7325003112c

Ngưỡng sensitive áp dụng: **0 P0/P1/P2/P3**. Còn **1 P2 và 1 P3**, thuộc hai lớp kế thừa. HEAD hiện thực thi các ca và in kiểm kê đúng; finding là lỗ chống hồi quy đã tái hiện bằng đột biến, không đánh tráo mutant thành hành vi hiện tại của HEAD.

Tree: `d49a8d03ac32352895df1961c9eb2ab462ca39eb`. Đã đọc trọn SPEC-r2, SHA256 đúng `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57`; áp dụng erratum D1/D2 và chỉ thị timeout trong PROMPT. Diff so `89fc4fac8cea65979cc2483043dc8cd07a6e8518` đúng bốn tệp. So baseline bất biến `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`, hai tệp thêm `ops/lease_publish_test.py`, `ops/specs/t131-deadline-dem-spawn.md` có blob giống hệt master; không phải packet mở rộng write set. DA_NOI đúng 1 thêm/0 xóa. Bằng chứng: `out/scope.json`.

Reviewer: Codex/OpenAI trong phiên API có công cụ shell cục bộ; Executor Claude theo gói giao. Không có receipt runtime độc lập để xác minh model/effort hay loại launcher CLI/Desktop/service, không tự suy từ GitHub actor. Verdict nội dung không cấp quyền land và không xác nhận #668 đã land. Lượt 6 được yêu cầu trực tiếp; không tự cấp thêm vòng review. Lịch sử tái diễn hai lớp phải giữ tại checkpoint S3 của điều phối/chủ kho.

Môi trường: Linux, Python 3.11.15 (CI dùng 3.12), actionlint 1.7.7, ShellCheck 0.9.0, Ruff 0.16.9 (khác pin workflow 0.15.15). Không dùng mạng. Không chạy Windows/GitHub Actions thật. Cây review giữ read-only theo vai trò; mọi bản sao, fixture và hint ở `tmp/`, bằng chứng ở `out/`. Sandbox workspace-write không phải cơ chế read-only riêng cho `cay/`.

Quy ước lệnh: cwd workspace rv6, trừ khi có `cd`; `export TMPDIR="$PWD/tmp"` trước mọi phép dùng temp; Python dùng `-B`/tắt bytecode. Các phép Git fixture của registry và tl selftest chạy lại với `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`, chỉ thay cấu hình tiến trình, không sửa cấu hình repo. Log lần đầu lỗi được giữ. `LOCALAPPDATA="$TMPDIR/local-appdata"` cho tl selftest trên bản sao.

## DOI CHIEU LUOT TRUOC

Nguồn: `goi/LUOT-TRUOC-VERDICT.md`, lượt 5, reviewed SHA `b86c4a35b610cc040b63c5b9a0cf29710329d529`.

| Lớp | Phân loại | Bằng chứng tự đo trên lượt 6 |
|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | **VA HO ở cấp lớp**; các biểu hiện guard/reader lượt 5 **đã vá thật** | `out/closures.log`: ngắt guard, sai toán hạng, bỏ return, doc_wf dùng safe_load đều GIET đúng ca đích. 9 mutant t93 và 5 timeout cũng GIET. Nhưng bỏ `CA[ten]()` trong runner vẫn FULL 61/61 + 144/144, TONG DAT; xem P2. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | **VA HO ở cấp lớp**; bỏ dòng/lặp cùng dòng/đổi dòng của lượt 5 **đã vá thật** | Ba mutant công bố kiểm kê đều GIET đúng t94. In thêm một dòng KIEM KE khác sai số vẫn FULL xanh và t94 đạt. Phân nhóm hiện tại đúng 35/16/3/7; xem P3. |
| `kiem-lease-bo-sot-duong-vao` | **DA VA THAT trong phạm vi local đã giao** | t20a..g/t21/t23 đạt; AST chỉ có một điều kiện dùng bo_qua_han, chính là chốt hạn. Clone đủ: 113/113 lease đạt. Refs runner Actions chưa đo. |
| `diff-check-tu-ha-nguong` | **DA VA THAT theo D1** | Ba phép blank-at-eol/blank-at-eof/space-before-tab đều raw rc=2, checker thực trả []; fixture conflict vẫn đỏ. |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | **DA VA THAT trong phạm vi đã giao** | t22/t22b đạt; ba sentinel thực thi và truyền lỗi; ba ca dữ liệu thật `loi=[]`, khoảng 4.8s trên máy này. |
| `fixture-lease-phu-thuoc-actor-ci` | **DA VA THAT** | t23 đạt dưới actor lạ, khôi phục actor; full suite giết hai mutant cô lập môi trường. |
| `tin-dung-dot-bien-khong-co-ca-dich` | **DA VA THAT ở các cửa đã đo** | t97/t99 đạt; 5 mẫu rc + 3 đột biến tự kiểm đạt; empty/unknown/iterator/generator/baseline đỏ được phân hạng đúng. |

Không đóng lớp bằng tổng suite xanh. Không ghi D1/D2 thành finding chính sách. `dependency-failure-skips-required-checks` giữ trạng thái ĐÓNG theo chỉ thị và phép đo GitHub của chủ kho; không có bằng chứng mới để mở lại.

## BANG LOP

| Slug | Biểu hiện / các đường vào đã rà | Hạng cao nhất còn mở | Vá chung | Phép kiểm đóng lớp |
|---|---|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | Top/workflow/job/step, if, runner/matrix/needs, continue-on-error, timeout, thân run mới, loader, cây nguồn, runner gọi ca, thu kết quả, main, mã thoát tiến trình | P2 | Kiểm từng nối giữa hai tầng bằng sentinel qua caller thật, ngoài kiểm helper; duy trì khóa cấu trúc | y01–y16; 95 probe topology; mutant guard/reader; runner DAT/DO/HONG phải gọi đúng một lần; ca đỏ phải ra process rc=1 |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | Metadata nhóm → AST nghĩa nhóm → tổng/phân rã → định dạng → tập dòng công bố | P3 | Kiểm toàn bộ các dòng mang nhãn KIEM KE, không chỉ số lần xuất hiện của dòng đúng | t96 độc lập số; t94 đòi danh sách dòng neo bằng đúng `[dong_kiem_ke()]`; thiếu/sai/lặp/đúng cộng sai đều đỏ |
| `kiem-lease-bo-sot-duong-vao` | Hạn/schema/authority/đuôi/rc/refs | Không mở local | Dùng cùng validator, chỉ bỏ hạn | t20/t21, AST kiem, đo lease thật; giữ giới hạn refs |
| `diff-check-tu-ha-nguong` | Ba ngoại lệ whitespace và conflict | Không mở | Đúng ba ngoại lệ D1 | Ba đối chứng raw/thực và conflict |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | Tên/call/cwd/rc t23/t26/t27 | Không mở | Giữ đường thực thi dữ liệu thật | t22/t22b và mutant no-call/cwd/rc |
| `fixture-lease-phu-thuoc-actor-ci` | Actor trong tiến trình và subprocess | Không mở | Cô lập fixture | t23 + hai mutant |
| `tin-dung-dot-bien-khong-co-ca-dich` | Đích rỗng/lạ, iterator, baseline, tín hiệu, rc | Không mở | Chỉ cấp GIET từ bằng chứng đúng ca | t97/t99 + tự kiểm phân hạng |

Bảy lớp kế thừa; hai lớp còn mở. Hai biểu hiện sống sót FULL; thêm một cửa truyền rc=1 có chứng cứ tập trung nhưng FULL không sạch (mất neo), phân biệt rõ bên dưới. Thân `run:` của bước CÓ SẴN là NGOAI-PHAM-VI theo chỉ thị, không dùng làm finding.

## BANG SAN

HUONG 1: Phạm vi diff và master drift
  gia thuyet : hai tệp ngoài write set bị packet tự sửa.
  lenh       : `git -C cay diff --name-only 1741e0a HEAD`; `git -C cay diff 89fc4fa HEAD -- ops/lease_publish_test.py ops/specs/t131-deadline-dem-spawn.md`; `git -C cay rev-parse REF:PATH` cho hai phía.
  output     : diff master hai tệp rỗng; các blob bằng nhau; DA_NOI numstat 1/0 (`out/scope.json`).
  ket luan   : KHONG PHAI LOI.

HUONG 2: Ba trạng thái, sự kiện và Git ba chấm
  gia thuyet : git lỗi/SHA thiếu/push/rename/base tiến thêm làm mở đường nhanh sai.
  lenh       : `python3 -B out/probes.py classify`.
  output     : t01..t19 hiện có DAT; Git fixture ba chấm/rename/xóa/object thiếu DAT; python-under-land duong_nhanh; force-full-allowlist ('GIET', '') (`out/classify.log`).
  ket luan   : KHONG PHAI LOI trong miền đo. `.py` dưới prefix là Q2 đã duyệt; fork/rebase/synthetic merge trên GitHub KHONG DO DUOC.

HUONG 3: D1 phạm vi ngoại lệ whitespace
  gia thuyet : tắt rộng hơn ba loại hoặc bỏ luôn conflict marker.
  lenh       : `python3 -B out/probes.py whitespace`.
  output     : blank-at-eol raw=2 actual=[]; blank-at-eof raw=2 actual=[]; space-before-tab raw=2 actual=[]; t20c DAT (`out/whitespace.log`).
  ket luan   : KHONG PHAI LOI theo erratum. Cấu hình literal chỉ có ba ngoại lệ đã duyệt.

HUONG 4: D2 lease và dữ liệu hồ sơ
  gia thuyet : hết hạn miễn thêm chốt khác hoặc ba ca dữ liệu chỉ được in tên.
  lenh       : `python3 -B out/probes.py lease-data`; `(cd cay && python3 -B ../goi/kiem_ke.py)`.
  output     : t20a..g/t21/t22/t22b/t23 DAT; bo_qua_han branches=['not bo_qua_han and han <= datetime.now(timezone.utc)']; ca dữ liệu thật loi=[] | 4.8s (`out/lease-data.log`, `out/inventory.log`).
  ket luan   : KHONG PHAI LOI trong phạm vi đo. T27 kiểm mục lục ops/reviews vẫn được thực thi.

HUONG 5: Topology, if, OS và timeout
  gia thuyet : còn cửa cấp job/bước hoặc runner/matrix/needs làm check biến mất mà test không bắt.
  lenh       : `python3 -B out/probes.py topology`; `python3 -B out/probes.py closures`.
  output     : STRUCTURAL_PROBES 95/95 DO đúng y13; gate-registry-identical True; timeouts 20 [(10, True), (5, True)]; 5 mutant timeout GIET (`out/topology.log`, `out/closures.log`).
  ket luan   : KHONG PHAI LOI ở topology đã đo. Probe cấu trúc dùng mock reader để cô lập assertion; không giả làm chạy Actions.

HUONG 6: Dây nối guard/reader/main lượt 5–6
  gia thuyet : helper đúng nhưng caller không gọi helper vẫn xanh.
  lenh       : `python3 -B out/probes.py closures`.
  output     : y15/t93/t94/t95/t96/t97/t98/t99 DAT; mutant ngắt/sai toán hạng/bỏ return guard, reader safe_load, ba mutant kiểm kê, 9 mutant kết luận/mã thoát đã khai đều GIET đúng (`out/closures.log`).
  ket luan   : KHONG PHAI LOI cho từng biểu hiện cũ; chưa đủ đóng lớp, xem hướng 7.

HUONG 7: Runner có thực sự gọi ca và process có giữ mã lỗi
  gia thuyet : t93 giả runner nên không kiểm nối runner→CA; process chỉ được kiểm với rc=2.
  lenh       : `python3 -B out/mutate.py runner-no-call`; `python3 -B out/mutate.py exit-one`; probe sentinel ghi tại `out/runner-proof.log`; chạy mutant `--mot-ca t93_main_ket_luan_va_ma_thoat_theo_duong_goi_that`.
  output     : runner-no-call FULL rc=0, 61/61 + 144/144, TONG DAT; sentinel HEAD DO/calls=1, mutant DAT/calls=0. exit-one t93 rc=0; FULL process rc=0 nhưng 143/144 và TONG DO vì neo mutant __main__ bị mất (`out/*-full.log`, `out/exit-target.log`).
  ket luan   : LOI P2. Chỉ runner-no-call được gọi là sống sót FULL; exit-one không được đếm thành FULL xanh hoặc GIET đúng lý do.

HUONG 8: Neo công bố kiểm kê có thật sự duy nhất
  gia thuyet : đếm một lần dòng đúng không ngăn một dòng sai khác cùng nhãn.
  lenh       : `python3 -B out/mutate.py inventory-extra`.
  output     : FULL rc=0, 61/61 + 144/144, TONG DAT; đồng thời có dòng đúng và `KIEM KE: ca hanh_vi=999 = 999` (`out/inventory-extra-full.log`).
  ket luan   : LOI P3. HEAD không sai số; chốt tính duy nhất chưa đủ.

HUONG 9: Tín dụng giết mutant
  gia thuyet : lỗi hạ tầng/khác tên/không chạy bị ghi GIET.
  lenh       : `(cd cay && python3 -B ops/ci_duong_nhanh_test.py)`; `python3 -B out/probes.py closures`.
  output     : 144/144; t97/t99 DAT; TU KIEM PHAN HANG DAT (5 mau rc, 3 dot bien that). exit-one bị ghi HONG do mất neo, không GIET (`out/suite.log`, `out/exit-one-full.log`).
  ket luan   : KHONG PHAI LOI ở phân hạng đã đo; rc ngoài cùng là vấn đề khác trong hướng 7.

HUONG 10: Actionlint và đăng ký
  gia thuyet : biểu thức rỗng hoặc mất nối test không làm cổng đỏ.
  lenh       : `(cd cay && actionlint .github/workflows/ci.yml)`; `python3 -B out/probes.py lint`; chạy `.claude/dev/ci_dang_ky_test.py` tại cay và tmp/base với Git fixture không ký.
  output     : actionlint base/head rc=0, shellcheck 0.9.0; mutant comment trong run rc=1 [expression]. Registry base 22/22 → head 23/23; hai bên PHẢN CHỨNG 938/938, TỔNG ĐẠT (`out/registry-*.log`, `out/lint-mutant.log`).
  ket luan   : KHONG PHAI LOI. Lần registry đầu rc=1 vì môi trường ký commit, không phải delta packet.

HUONG 11: Định lượng lịch sử, lease và refs
  gia thuyet : 345/63/8 hoặc 113 lease là số trôi/sai scope.
  lenh       : `(cd cay && python3 -B ../goi/do_lai_so.py)`; `git for-each-ref`; clone local `--single-branch --branch master` và đo lại.
  output     : 345/63/8, 113/113 đạt; cay có 560 refs. Clone một nhánh (22 refs do còn tags/remote aliases) ở master hiện tại có 114 lease/6 trượt (`out/measure.log`, `out/refs.log`, `out/single-ref.log`).
  ket luan   : KHONG PHAI LOI; 552 refs và 6/113 là số lịch sử có scope, không đọc thành số hiện tại. Phạm vi runner GitHub KHONG DO DUOC.

HUONG 12: Hint có bắt đúng và không làm đỏ nền
  gia thuyet : hint lại chỉ đo helper hay đổi phân nhóm sai.
  lenh       : `python3 -B out/build-hint.py`; `python3 -B out/test-hint.py`; `(cd tmp/hint-tree && python3 -B ops/ci_duong_nhanh_test.py)`.
  output     : 4 ca hint nền DAT; sentinel no-call, exit-one, thêm dòng sai đều rc=3 đúng diagnostic; patch dry-run -p0 --fuzz=0 rc=0. FULL hint 63/63 + 144/144, TU KIEM DAT, TONG DAT (`out/hint-ab.log`, `out/hint-full.log`).
  ket luan   : KHONG PHAI LOI trong A/B đã đo. Mutant reviewer đo riêng, chưa thêm vào bảng 144; executor phải tích hợp thành chốt bền.

## BANG DO

| Khẳng định | Đầu khai / phép đo | Đo được | Khớp / giới hạn |
|---|---|---|---|
| CA và DOT BIEN | Output suite HEAD | 61/61; 144/144 | Có |
| Phân nhóm ca | KIEM KE + kiem_ke.py + t96 AST | 35 hành vi + 16 YAML + 3 đăng ký + 7 tự kiểm = 61 | Có |
| Mutant theo tệp | KIEM KE/DOT_BIEN | 44 sản phẩm + 33 test + 65 YAML + 2 sổ = 144 | Có |
| Tự kiểm phân hạng | MAU_RC/TU_KIEM_DOT_BIEN | 5 mẫu rc, 3 mutant thật | Có, ngoài 144 |
| IF_BUOC_CHUAN | kiem_ke.py | 3/12/7/0/2 | Có |
| BO_QUA | kiem_ke.py | 5/3/1 | Có |
| Ba ca dữ liệu ~6–9s | kiem_ke.py thực thi | 3 ca, loi=[], 4.8s | Số đúng; thời gian tùy máy, không suy thời gian CI |
| 345/63/8, ~13% | do_lai_so.py, cửa sổ 400 merge first-parent từ 1741e0a | 345/63/8; 8/63≈12.70% | Có trong scope đã khai |
| 113 lease/0 trượt trên clone đủ | do_lai_so.py | 113/113 | Có |
| 552 refs lịch sử | docstring khai lịch sử; for-each-ref hiện tại | 560 refs; SHA256 danh sách 4d264871cc42a0fa92ef5f6161aaa0bdec9680853700a2d84322b091530f128e | Khác thời điểm, không phải lời khai 552 hiện tại |
| 6/113 clone một nhánh lịch sử | Clone local --single-branch master và đo | master hiện tại 114/6 trượt; checkout baseline 1741e0a: 113/6 trượt | Không suy master hiện tại là cây lịch sử |
| Registry 22→23, 938 phản chứng | Chạy base/head | 22/22→23/23; 938/938 hai bên | Có, cấu hình ký Git fixture phải tắt |
| Một dòng DA_NOI | git numstat | 1/0 | Có |
| Ruff tl.py 12, delta=0 | Bare lint 0.16.9 base/head; blob so master | 12 F821 hai phía; blob tl.py giống master; file mới sạch F | Có; không khai bare lint pin 0.15.15 |
| Actionlint ci.yml | actionlint 1.7.7, ShellCheck 0.9.0 | base/head rc=0; mutant rc=1 | Có; lượt này không chạy toàn bộ workflow |
| AL_VER 4 | rg ci.yml | 4 dòng, đều 1.7.7 | Có; không xác nhận #668 đã land |
| Timeout 10/5/20 | YAML thật + y16/y13 + 5 mutant | checkout=10, classifier=5, job=20; 15<20 | Có cấu trúc; elapsed/runner timeout thật chưa đo |
| release-verify strict | Bản sao head, manifest committed | rc=0, ok=true, errors=[], expected=checked=180 | Có (`out/manifest.log`) |
| Hint suite | Bản sao áp hint | 63/63, 144/144; phân nhóm 35/16/3/9 | Có; không nhầm thành số HEAD |
| 52 phút / G5 46.5 phút | Run API ngoài gói, DO_LAI khai | Không mạng | KHONG DO DUOC; không dùng làm nghiệm thu 11 |

Không phát hiện khẳng định định lượng mới ngoài bảng đã giao mà cần mở một lỗi số liệu độc lập. Lỗ P3 dưới đây nằm ở tính duy nhất của neo công bố, không phải các số HEAD hiện tại sai.

### chot-yaml-chi-do-su-hien-dien [P2] Đường runner gọi ca chưa được kiểm, bỏ thực thi vẫn báo đủ ca đạt

TEP/DONG: `ops/ci_duong_nhanh_test.py:1205` (t93), `:1395` (chay_ca_trong_tien_trinh), `:1777` (main gọi runner), `:1802` (entrypoint).

VAN DE: t93 thay `chay_ca_trong_tien_trinh` bằng đồ giả cho mọi kịch bản. Nó chứng minh main xử lý kết quả giả, chưa chứng minh runner gọi ca. Thay đúng `CA[ten]()` tại dòng 1397 bằng `pass` vẫn FULL rc=0, 61/61, 144/144, TONG DAT. Các phép mutation chạy `--mot-ca`, đường đó gọi CA trực tiếp, nên không đi qua runner đang hỏng. Probe sentinel độc lập: HEAD trả DO và gọi 1 lần; mutant trả DAT và gọi 0 lần. Con số CA đạt của lượt chạy chính có thể được công bố dù ca không thực thi. Đây là cửa nối tiếp của lớp guard có mặt nhưng đường chạy thật chưa được kiểm, không phải lỗi phân loại sản phẩm hiện tại.

Cửa liên quan cùng lớp: t93 chỉ kiểm process exit với đối số lạ (rc=2). Đổi entrypoint để chỉ biến rc=1 thành 0 vẫn qua t93. Full mutant này trả process rc=0 dù TONG DO; báo 143/144 do mất neo của mutant entrypoint cũ. **Không coi đây là full-suite sống sót**: phép phát hiện hiện có là HONG hạ tầng, chưa phải ca đích đỏ vì sai mã thoát. Vì bước CI chỉ gọi Python, rc=0 vẫn là tín hiệu mà CI nhận. Khóa cả đường ca DAT/DO/HONG → runner → main → process.

Các cửa đã liệt kê cho lớp: nguồn cây; decoder YAML; topology workflow/job/step; run mới; đăng ký; runner gọi ca; thu/phân hạng kết quả; số đếm/điều kiện main; mã thoát. Giữ chốt cũ và kiểm nối từng cặp. Thân run cũ ngoài phạm vi. Không tuyên bố lớp đã đóng chỉ từ một sentinel.

DA THU VA: có — `out/HINT.patch` TEST-only, thêm t92 sentinel qua runner thật, t91 tiến trình con thực thi chính stanza __main__ của tệp đang đo với main/runner thật. Chỉ giả các runner mutant/tự kiểm nặng để tránh đệ quy; mỗi kịch bản dùng CA một sentinel, đòi marker đúng một lần và rc 0/1/1. Trích hint:

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
+@ca_tu_kiem
+def t92_runner_thuc_su_goi_ca_va_phan_biet_loi():
+    goi = []
+    for ket_qua in ("DAT", "DO", "HONG"):
+        def sentinel():
+            goi.append(ket_qua)
+            if ket_qua == "DO":
+                raise TinHieuChotCa("review sentinel DO")
+            if ket_qua == "HONG":
+                raise RuntimeError("review sentinel HONG")
+        with mock.patch.dict(CA, {"t_fixture": sentinel}, clear=True):
+            hang, chi_tiet = chay_ca_trong_tien_trinh("t_fixture")
+        bang(hang == ket_qua and goi.count(ket_qua) == 1,
+             f"runner/{ket_qua}: {hang}/{chi_tiet}, calls={goi}")
```

Chốt riêng:
- Runner: không gọi/gọi hai lần/phân hạng sai/nuốt sentinel phải đỏ; ca DAT thật phải xanh. Phần thêm t92 phải được mutation harness chạy qua `--mot-ca`, vì runner hỏng không tự chạy được test của mình.
- Main/process: giữ t93 cho nhánh tổng hợp; thêm ca thực thi entrypoint trong subprocess với ca DAT, TinHieuChotCa, RuntimeError. Đòi process rc=0,1,1 tương ứng và marker thực thi; không chỉ rc=2 đối số lạ. Hint t91 đầy đủ nằm trong patch, đã chạy A/B.
- Bổ sung các mutant đó vào DOT_BIEN bằng neo duy nhất; đừng để chúng chỉ ở script reviewer. Nếu neo entrypoint đổi, cập nhật neo mutant cũ để không nhận HONG thay GIET.

Rủi ro hint: tự kiểm runner có thể đệ quy nếu chạy nguyên toàn suite con; fixture phải cô lập công việc nặng như patch đã thử. Đọc stanza AST cuối tệp giả định entrypoint nằm cuối, nên phải assertion rõ nếu cấu trúc đổi. Hai ca mới phải khai @ca_tu_kiem để t96/kiem_ke.py đếm đúng. Hint không đổi workflow/authority.

DA THU NGHIEM: `out/runner-no-call-full.log` FULL 61/61 + 144/144, TONG DAT; `out/runner-proof.log` calls=1→0. `out/exit-target.log`: mutant exit-one t93 rc=0; `out/exit-one-full.log`: rc=0, 143/144, TONG DO, mất neo (không GIET đúng). `python3 -B out/test-hint.py` bắt runner-no-call đúng marker thiếu, exit-one đúng rc sai bằng rc=3; hint nền đạt. FULL hint 63/63 + 144/144, rc=0.

DO TIN: cao về hai đường gọi đã đo; không cáo buộc workflow HEAD hiện đang bỏ ca.

### bang-do-thieu-neo-va-thieu-kiem-ke [P3] T94 cho phép một dòng kiểm kê sai tồn tại cùng dòng đúng

TEP/DONG: `ops/ci_duong_nhanh_test.py:1252` (t94 đếm đúng chuỗi), `:1789` (main in kiểm kê).

VAN DE: `.splitlines().count(dong_kiem_ke()) == 1` chỉ ràng buộc số bản sao của dòng đúng. Nó không chứng minh có đúng MỘT dòng KIEM KE như hợp đồng đã giao. Thêm `print("KIEM KE: ca hanh_vi=999 = 999")` sau print thật vẫn FULL 61/61 + 144/144, TONG DAT. Artifact mang hai khai báo kiểm kê mâu thuẫn; consumer/người đọc lấy dòng đầu hay cuối có thể nhận số khác nhau. t96 kiểm generator đúng, không thấy dòng phụ ở call-site. Đây vẫn là lớp mất neo đáng tin khi công bố, không tách slug mới và không nói số hiện tại HEAD sai.

DA THU VA: có — giữ kiểm số t96, đổi t94 để thu TẤT CẢ dòng mang nhãn và so danh sách với đúng một phần tử mong đợi:

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
-    bang(rc == 0 and ra.getvalue().splitlines().count(dong_kiem_ke()) == 1,
+    dong = [d for d in ra.getvalue().splitlines() if d.startswith("KIEM KE:")]
+    bang(rc == 0 and dong == [dong_kiem_ke()],
          "main phai in dung mot dong KIEM KE duoc doi chieu doc lap boi t96")
```

Chốt riêng từng cửa: metadata/ý nghĩa nhóm/tổng/phân rã giữ t96; thiếu/sai dòng/lặp cùng dòng giữ mutant cũ; thêm mutant đúng cộng sai (trước hoặc sau) để canh toàn bộ tập neo. Cùng một phép so danh sách bắt cả hai vị trí, không cần whitelist từng số sai. Bổ sung mutant bền vào DOT_BIEN. Rủi ro: chốt này cố ý cấm một dòng diagnostic khác dùng đúng tiền tố KIEM KE; diagnostic phụ cần nhãn khác để không mơ hồ hợp đồng output.

DA THU NGHIEM: `python3 -B out/mutate.py inventory-extra` → FULL rc=0, 61/61 + 144/144, hai dòng KIEM KE, TONG DAT. `python3 -B out/test-hint.py` → baseline t94/t96 rc=0; mutant thêm dòng sai rc=3 đúng t94. FULL hint 63/63 + 144/144, rc=0. Patch TEST-only dry-run `patch -p0 --fuzz=0` đạt.

DO TIN: cao; lỗi chốt bằng chứng, không nâng thành lỗi runtime classifier.

## TIMEOUT, DAC TA VA NGOAI-PHAM-VI

10 phút checkout + 5 phút classifier, job 20 phút là cấu hình hợp lý: tổng hai trần bước 15 phút nhỏ hơn trần job, có 5 phút chênh cho phần công việc khác. Điều này không bảo đảm mọi mạng/repo đủ nhanh; timeout classifier đáng ra thường rộng so với một lệnh Git cục bộ, nhưng không có benchmark Actions để tối ưu số này. y16 bắt bỏ timeout từng bước, bỏ timeout job, trần job 12 phút, checkout 60 phút; y13 khóa chính xác cả cấu trúc.

Với output **vắng/rỗng**, biểu thức đang dùng chắc chắn cho `day_du`: PR && rỗng || day_du; push/dispatch luôn day_du. Giá trị lạ còn nguyên nhưng mọi điều kiện bỏ bước chỉ nhận chính `duong_nhanh`, nên vẫn chạy đầy đủ. `continue-on-error: true` được khóa cho cả hai bước. Script chỉ ghi output sau khi phân loại xong, rồi kết thúc; nhánh Git bị treo trước kết quả chưa ghi output. Đây là phân tích code và bảng chân trị local, **không phải phép tái hiện timeout của Actions**. Không khẳng định mọi lỗi/cancel đều xóa output đã ghi trước đó.

Job timeout/failure: giữ kết luận ĐÓNG từ bốn lần đo thật của chủ kho được PROMPT dẫn (5889459132), không suy required context thiếu là success. Không có phép GitHub mới trong sandbox để mở lại lớp này. Concurrency/needs/OS matrix/registry giữ như baseline, đã đối chiếu cấu trúc. Cancellation, runner unavailable, windows label và context/ruleset thực tế chưa tự đo lượt này.

Allowlist prefix cho `.py` dưới ops/land vẫn nhanh là Q2, không sửa đặc tả. PR tự sửa classifier/workflow là ranh giới review authority được code công khai, không coi classifier là sandbox chống tác giả cố ý. Symlink/path escape/shell injection cần payload ngoài fixture được giao: chỉ mô tả, không tạo nội dung tấn công hay đường thoát cây. Thân run bước CÓ SẴN: **NGOAI-PHAM-VI**, không tính P.

## NGHIEM THU VA GIOI HAN

1. Đạt local: t01 và mutant ép mọi allowlist thành day_du bị GIET đúng.
2. Đạt local: t02 + mutant nới scripts/ bị GIET.
3. Đạt local: t05/t06 thiếu/hỏng SHA/Git; mutant fail-open bị GIET.
4. Đạt local: t03 push/dispatch không gọi Git; mutant gọi Git bị GIET.
5. Đạt local: t08 workflow ngoài prefix; mutant nới .github/ bị GIET.
6. Đạt đối với các mutant đặc tả: gỡ PR guard/luôn bỏ bước nặng bị GIET. Điều này không xóa P2 về nối runner mới tìm ra.
7. Đạt local: quét paths/paths-ignore, mutant tương ứng trong 144 bị GIET.
8. Đạt local: actionlint base/head rc=0 với ShellCheck; comment run chứa biểu thức rỗng rc=1.
9. Đạt local: 22/22→23/23, 938/938 hai bên; DA_NOI 1/0; gỡ đăng ký/gỡ lời gọi workflow đều bị giết.
10. Ruff delta=0 (0.16.9); tl selftest lần đầu 1713/1715 do hai ca tạo commit fixture không tắt ký Git toàn cục. Chạy lại với cấu hình tiến trình như registry; kết quả terminal ghi dưới đây, không gọi lần đầu là pass.
11. **CHUA_DO_DUOC**: không PR thật, không số tiết kiệm thời gian hay ba required check success mới. Không thấy lời khai đã đạt tiêu chí 11 trong gói giao. Không dùng runtime local thay nghiệm thu này.

`out/HINT.patch` chỉ sửa TEST, đường dẫn repo-relative không a/b; nhãn nguyên văn: **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**. Đã thử trên bản sao; không ghi cây thật, không tạo quyền commit. Executor cần tái dẫn xuất và bổ sung mutant bền, không chép mù patch.

## CAP NHAT CUOI

Tất cả phép dùng cho kết luận đã kết thúc:

- `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false LOCALAPPDATA="$TMPDIR/local-appdata" PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/tl.py --selftest` tại `tmp/head-copy` → **1715/1715, rc=0** (`out/tl-selftest-corrected.log`). Hai ca đỏ lần đầu là các fixture tạo commit dưới cấu hình ký toàn cục; chạy lại không sửa mã. Nghiệm thu local 10 đạt với giới hạn Ruff version đã khai.
- Clone local một nhánh master mang 22 refs (còn tags/remote aliases), 114 lease ở tip. Checkout detached baseline `1741e0a`, giữ nguyên phạm vi refs đó, chạy `kiem(bo_qua_han=True)` cho từng lease → **113 tổng, 107 đạt, 6 trượt** (`out/single-lease-baseline.log`). Tái hiện đúng hiệu ứng phạm vi refs; không gọi clone một nhánh là đúng một Git ref, không suy tương đương runner Actions.
- HEAD suite **61/61 + 144/144**, TU KIEM DAT, TONG DAT, rc=0. Hai mutant reviewer sống sót FULL: **runner-no-call**, **inventory-extra**. `exit-one` chỉ qua t93 và trả rc=0; FULL TONG DO do mất neo, đã phân biệt, không cộng vào hai mutant xanh.
- Hint suite **63/63 + 144/144**, TU KIEM DAT, TONG DAT, rc=0; A/B tập trung và patch dry-run đạt. Các mutant mới chưa vào DOT_BIEN của hint, phải được executor tích hợp và tự đo.
- `out/final-check.log`: cây `cay/` sạch tracked/index/untracked/ignored, HEAD/tree/spec giữ nguyên. Snapshot này chứng minh không có delta quan sát được ở mốc cuối so Git và mốc đầu; không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

Giữ **changes_requested** vì 1 P2 và 1 P3. Không tự mở vòng kế, không tạo approval/land authority.

TONG: P0=0 P1=0 P2=1 P3=1
So lop: 7; 2 con mo, 5 khong con finding trong pham vi local da do.
