verdict: changes_requested
reviewed_sha: 7b112ad0b546649ecc929a596f5e97149dc81cc8
Reviewed commit: 7b112ad0b546649ecc929a596f5e97149dc81cc8

Ngưỡng packet sensitive: **0 P0/P1/P2/P3**. Còn **1 P2 và 1 P3**, thuộc hai lớp kế thừa. Không approve.

Tree `8506a6943ed079202374b7a06269789fca6e2d55`. SPEC-r2 đã đọc trọn; SHA256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` khớp. Đã đọc hướng dẫn kho và protocol §8/8.3. D1/D2 được duyệt theo erratum trong gói giao; không xét lại chính sách.

Diff từ `1741e0a1ab7ebce4b26912aefadca56ddfcdc691` thực tế có **6 tệp**, không phải 4: hai tệp thêm là drift #676 đã được prompt khai. Tự đo `git diff d7c819f HEAD` chỉ có `ops/lease_publish_test.py` và `ops/specs/t131-deadline-dem-spawn.md`; bốn tệp packet không đổi bởi merge. Diff so `origin/master=89fc4fac8cea65979cc2483043dc8cd07a6e8518` đúng bốn tệp packet. Sổ đăng ký đúng một dòng thêm, không xóa. #668 chưa land; verdict không cho phép bỏ điều kiện tích hợp/land của đặc tả.

Reviewer: Codex/OpenAI, phiên API có shell cục bộ; executor Claude theo gói giao. Không có runtime receipt độc lập chứng minh model/effort/launcher transport: **khong_do_duoc**, không suy assurance từ actor GitHub. Agent `tl_auditor` chỉ đọc ba log dài theo CLAUDE.md §Quy trình sửa code mục 5; không sửa hoặc chạy test. Kết luận/finding do reviewer chính xác lập.

Môi trường: Linux, Python 3.11.15 (workflow khai 3.12), actionlint 1.7.7, ShellCheck 0.9.0, Ruff 0.15.15. Không mạng, không chạy Windows CI hoặc PR thật. Mọi lệnh dùng temp đặt `TMPDIR=/tmp/claude-0/-home-user-tra-luat/7ccc7ea3-39e6-5592-a374-909e124275e1/scratchpad/rv5/tmp`; Python `-B`/`PYTHONDONTWRITEBYTECODE=1`, Ruff `--no-cache`. Fixture registry/selftest dùng `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`; `core.abbrev=7` đã có trong repo. Các đường dẫn/lệnh dưới đây tính từ workspace rv5.

## DOI CHIEU LUOT TRUOC

Nguồn nguyên văn: `goi/LUOT-TRUOC-VERDICT.md`, reviewed SHA `7b8c85631a8945fc0631bfc4e9338ca4584c7e3c`.

| Lớp lượt trước | Kết luận | Bằng chứng tự đo lượt này |
|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` [P2] | **VA HO** ở cấp lớp; hai cửa runner cũ đã vá thật | Hai mutant runner/matrix Windows nay GIET đúng y13 (`out/direct-mutants.log`). 55 biến thể metadata/topology đỏ tại y13. Nhưng y09 vẫn chỉ tìm một dòng trong `run:`; thân run của bước non-PR mới hoàn toàn chưa được khóa. Bản sao thêm một lệnh vô hại vào run selftest vẫn full 55/55 + 111/111, rc=0. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` [P3] | **VA SINH LOI MOI** cùng cơ chế | t97/t98/t99 đã được tách; t96 mới lại bị xếp vào hành vi. Bảng in 36/13/3/3; phân loại đúng theo chức năng là 35/13/3/4. t96 sao lại cùng tập tiền tố thiếu chính nó nên vẫn DAT. |
| `kiem-lease-bo-sot-duong-vao` | **DA VA THAT** trong các cửa đã giao | t20a–g/t21 DAT; còn/hết hạn, .yaml/.yml, hạn hỏng/thiếu và rc đều có phép đo. AST `kiem` chỉ bỏ điều kiện so hạn, vẫn đọc hạn và giữ schema/authority/bia mộ/neo prompt. Scope refs Actions chưa đo. |
| `diff-check-tu-ha-nguong` | **DA VA THAT** theo D1 | Ba probe riêng raw=2, approved=[]; conflict marker vẫn đỏ qua t20c. Chuỗi cấu hình đúng ba ngoại lệ được duyệt. |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | **DA VA THAT** trong phạm vi trước | t22 và sentinel từng ca t22b DAT; bảng kiểm kê chạy t23/t26/t27 trên chính cây merge, lỗi=[] (6.7s). |
| `fixture-lease-phu-thuoc-actor-ci` | **DA VA THAT** | t23 DAT dưới actor lạ, phục hồi môi trường cha; suite giết hai mutant mất cô lập actor. |
| `tin-dung-dot-bien-khong-co-ca-dich` | **DA VA THAT** | t97/t98/t99 DAT; tự kiểm phân hạng []; baseline/rỗng/lạ/iterator/generator/caller/callee được đo. Không có lỗi tín dụng mới được xác lập. |

S3: giữ nguyên slug và lịch sử, không coi tổng suite xanh là đóng lớp. Hai lớp lặp vẫn còn mở; không tự mở vòng tiếp theo hoặc suy quyền land.

## BANG LOP

| Slug | Các biểu hiện/đường vào | Hạng cao nhất còn mở | Vá chung | Phép kiểm đóng lớp |
|---|---|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | Metadata workflow/job/step và thứ tự đã khóa; còn thân run selftest mới và logger non-PR mới | P2 | Khóa nội dung toàn bộ run do packet thêm; giữ kiểm metadata y13 | Nền xanh; trước/sau mỗi thân run phải đỏ đúng assertion; duy trì runner/matrix/source/needs/if/env/shell/with/order/concurrency mutants |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | Nhóm tự kiểm bỏ sót t96; oracle t96 lặp cùng thiếu sót; lời mô tả đầu tệp thiếu ca tự kiểm | P3 | Phân nhóm theo chức năng, cùng cập nhật bộ kiểm độc lập và bảng hiển thị | Đúng thành viên của cả bốn nhóm, không chỉ tổng; đột biến chuyển riêng từng t96–t99 phải đỏ |
| `kiem-lease-bo-sot-duong-vao` | Đuôi/schema/hạn/rc/authority/refs | Đóng local | Giữ validator, không mở rộng miễn hạn | t20/t21; refs Actions khai chưa đo |
| `diff-check-tu-ha-nguong` | Ba whitespace/conflict | Đóng theo D1 | Đúng chuỗi ngoại lệ | Ba probe và conflict |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | Chọn/gọi t23/t26/t27, cwd, rc | Đóng local | Giữ gọi thật và truyền lỗi | Sentinel riêng từng ca + cây merge thật |
| `fixture-lease-phu-thuoc-actor-ci` | Fixture trong tiến trình và validator con | Đóng | Cô lập actor fixture | t23 + hai mutant |
| `tin-dung-dot-bien-khong-co-ca-dich` | Empty/unknown/iterator/baseline/caller/callee | Đóng | Vật hóa tập ca; đòi bằng chứng dương | t97 và tự kiểm phân hạng |

Bảy lớp lịch sử; hai lớp còn mở. Finding YAML có hai cửa cụ thể; finding kiểm kê có biểu hiện ở phân nhóm, oracle và tài liệu, cùng một nguyên nhân.

## BANG SAN

HUONG 1: Fail-close, sự kiện và ghi output
  gia thuyet : SHA/git/đầu ra lỗi hoặc sự kiện không phải PR có thể mở nhanh.
  lenh       : `python3 -B out/probes.py classify`; `(cd cay && python3 -B ops/ci_duong_nhanh_test.py)`.
  output     : t01/t02/t03/t05–t10f/t16–t19b DAT; full CA 55/55, DOT BIEN 111/111, TU KIEM DAT, TONG DAT.
  ket luan   : KHONG PHAI LOI trong miền đo. t03 chứng minh push/dispatch không gọi git; t07 phân biệt diff rỗng.

HUONG 2: Ngữ nghĩa Git ba chấm và allowlist
  gia thuyet : base tiến thêm, rename từ mã sang hồ sơ, hoặc xóa mã làm sai phân loại.
  lenh       : `python3 -B out/probes.py classify`; phép `chay_mot_dot_bien` lưu `out/direct-mutants.log`.
  output     : t11/t12/t13/t14/t15 DAT trên Git thật; mutant toàn allowlist trả DAY_DU => ('GIET','').
  ket luan   : KHONG PHAI LOI local. .py dưới ops/land vẫn nhanh theo Q2; workflow/classifier nằm ngoài allowlist. Fork/rebase trên GitHub thật KHONG DO DUOC.

HUONG 3: Lease, hạn và actor
  gia thuyet : bo_qua_han bỏ thêm schema/authority, bỏ đuôi yml hoặc fixture phụ thuộc actor.
  lenh       : `python3 -B out/probes.py lease`; `python3 -B out/probes.py whitespace`.
  output     : t20a–g/t21/t23 DAT; AST dòng 894: `not bo_qua_han and han <= datetime.now(timezone.utc)`.
  ket luan   : KHONG PHAI LOI theo D2 trong các cửa đo. Không coi clone đủ refs là bằng chứng về runner Actions.

HUONG 4: Whitespace và conflict
  gia thuyet : D1 tắt rộng hơn ba ngoại lệ được duyệt.
  lenh       : `python3 -B out/probes.py whitespace`.
  output     : blank-at-eol, blank-at-eof, space-before-tab từng loại raw=2/current=[]; t20c conflict DAT; config đúng `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab`.
  ket luan   : KHONG PHAI LOI theo D1.

HUONG 5: Dữ liệu thật còn được kiểm ở fast path
  gia thuyet : chỉ giữ tên t23/t26/t27 nhưng không gọi hoặc nuốt lỗi.
  lenh       : `python3 -B out/probes.py lease`; `(cd cay && python3 -B ../goi/kiem_ke.py)`.
  output     : t22b/t22 DAT; ba ca dữ liệu trên cây merge lỗi=[]; 6.7s.
  ket luan   : KHONG PHAI LOI trong phạm vi giao. gate-registry không bị bỏ/cấu trúc giữ nguyên; push/dispatch quay về đầy đủ theo t03/y02/y03.

HUONG 6: YAML metadata và thân run mới
  gia thuyet : khóa topology nhưng run mới vẫn chỉ được kiểm sự hiện diện dòng gọi.
  lenh       : `python3 -B out/probes.py yaml`; chạy `python3 -B cay/ops/ci_duong_nhanh_test.py` qua subprocess với `CI_DUONG_NHANH_CAY` bằng đường dẫn trong `out/body-mutant-path.txt`.
  output     : 55 biến thể metadata đỏ tại y13; mutant thân run selftest thêm `python --version` vẫn mọi y/k DAT, actionlint=0, FULL 55/55 + 111/111 + TU KIEM DAT + TONG DAT, rc=0.
  ket luan   : LOI P2 về chốt hồi quy thiếu khóa đã khai. Probe vô hại chỉ chứng minh thân run còn mở; không phải bằng chứng khai thác hoặc required check giả xanh trên GitHub. 55 biến thể dùng mock cấu trúc, không tự coi tất cả là workflow hợp lệ có thể chạy.

HUONG 7: Harness và tín dụng giả
  gia thuyet : rỗng/lạ/iterator hoặc baseline đỏ vẫn được tính GIET.
  lenh       : `python3 -B out/probes.py credit`.
  output     : t97/t98/t99 DAT; self-check []; suite 5 mẫu rc và 3 mutant thật DAT.
  ket luan   : KHONG PHAI LOI trong các cửa đã đo.

HUONG 8: Độ đúng của phân hoạch và lời khai định lượng
  gia thuyet : ca tự kiểm mới lại được tính vào hành vi.
  lenh       : `python3 -B out/probes.py inventory`; `(cd cay && python3 -B ../goi/kiem_ke.py)`; `(cd cay && python3 -B ../goi/do_lai_so.py)`.
  output     : claimed 36/13/3/3; t96 group=['hanh_vi']; semantic expected 35/13/3/4; lịch sử 345/63/8; lease 113/113.
  ket luan   : LOI P3 về nghĩa của nhóm. Tổng 55, mutant 111 và số lịch sử khớp.

HUONG 9: Lint, đăng ký, manifest và drift
  gia thuyet : expression lỗi bị bỏ qua, test chưa nối hoặc lệch write set do merge.
  lenh       : `actionlint .github/workflows/ci.yml` tại cay và tmp/base-copy; `actionlint tmp/expression-in-run-ci.yml`; registry head/base; Ruff F; release-verify trên tmp/head-copy.
  output     : lint nền/head=0; expression trong comment của run block=1 [expression]; registry 22/22→23/23, cả hai 938/938; sổ diff 1/0; manifest ok=true 180/180 rc=0; Ruff hai tệp mới sạch, tl.py 12 F821 cả hai nền/head, delta=0.
  ket luan   : KHONG PHAI LOI. Probe expression đầu tiên đặt comment YAML ngoài run trả 0 là fixture sai vị trí; đã sửa và đo lại đúng run block, không tính lần đầu là đạt nghiệm thu 8.

HUONG 10: Hint có răng
  gia thuyet : hint chỉ chặn một cửa hoặc làm đỏ nền.
  lenh       : `python3 -B out/hints.py`; `(cd tmp/hint-copy && patch -p0 --fuzz=0 < ../../out/HINT.patch)`; `(cd tmp/hint-copy && python3 -B ops/ci_duong_nhanh_test.py)`.
  output     : y02/y09/t96 nền DAT; bốn biến thể run vô hại trước/sau hai bước: cũ DAT, hint DO; chuyển riêng t96/t97/t98/t99 về hành vi đều DO; full hint 55/55 + 111/111 + TU KIEM DAT + TONG DAT, rc=0.
  ket luan   : KHONG PHAI LOI trong tập A/B. Tám probe ngoài suite chưa được nhập vào DOT_BIEN của hint; executor phải tích hợp chốt hồi quy tương ứng.

## BANG DO

| Khẳng định | Đầu khai/phạm vi | Đo được lượt này | Khớp? |
|---|---|---|---|
| CA và mutant N/N | Suite HEAD | 55/55; 111/111; tự kiểm DAT | Có |
| Phân nhóm ca | phan_hoach_ca, t96, kiem_ke.py | Khai 36 hành vi + 13 YAML + 3 registry + 3 tự kiểm; đúng 35+13+3+4 | **Không**, P3 |
| Mutant theo tệp | kiem_ke.py | Sản phẩm 44; test 9; YAML 56; registry 2 = 111 | Có |
| Mẫu rc/mutant tự kiểm | MAU_RC/TU_KIEM_DOT_BIEN | 5/3, ngoài DOT_BIEN | Có |
| If bước theo job | IF_BUOC_CHUAN | chuan-bi/gate/gate-ops/registry/packet-loop = 3/12/7/0/2 | Có |
| Bước bỏ theo che_do | BO_QUA | gate=5, gate-ops=3, packet-loop=1 | Có |
| Ba ca dữ liệu ~6–7s | Docstring/DO_LAI | Đúng t23/t26/t27; 6.7s, lỗi=[] | Có trên máy này; không suy sang CI |
| 345/63/8 và ~13% | 400 merge first-parent từ 1741e0a, do_lai_so.py | 345/63/8; 8/63≈12.7% | Có; không đo PR thật |
| 113 lease | do_lai_so.py | 113 đạt, 0 trượt trong scope hiện tại | Có |
| 552 ref và 6/113 clone một nhánh | Docstring lịch sử reviewer lượt 1 | Scope hiện tại **557 ref**; chưa dựng lại single-branch để đo 6 | Số 552 được neo lịch sử, không phải số hiện tại; không xác nhận lại số 6 |
| 22→23 registry; 938 phản chứng | DO_LAI, head/base | 22/22→23/23; 938/938 cả hai | Có |
| Đúng một dòng DA_NOI | numstat base/head | 1 thêm, 0 xóa | Có |
| Ruff tl.py 12 F, delta=0 | DO_LAI; origin/master cục bộ | 12 F821 ở base/head; scripts/tl.py không đổi so origin/master; hai tệp mới sạch F | Có |
| AL_VER=4 | Regex nghiệm thu/t152 | 4 | Có; chưa tích hợp #668 |
| Manifest strict | Lệnh lane LAND, bản sao HEAD | ok=true, expected=checked=180, rc=0 | Có |
| Full selftest | Nghiệm thu 10 | 1715/1715, rc=0 | Có |
| 52 phút, G5 46.5 phút; skipped như success | Số API/tài liệu ngoài gói | Không mạng/không PR thật | KHONG DO DUOC; không dùng làm bằng chứng đạt 11 |

Refs tên/OID nằm trong `out/refs.txt`, SHA256 `befeb9ceac7221f5cb9b18a72e62acb51a3c66aa6db5b3d8e457619ec57217fd`. Giữ scope refs riêng với kết quả validator. Không lấy bảng executor làm trần; ngoài lỗi phân nhóm, chưa xác lập thêm khẳng định định lượng của packet bị bỏ sót. “Khóa nguyên văn run mới” là khẳng định sai có finding P2 bên dưới, không phải số đếm.

### chot-yaml-chi-do-su-hien-dien [P2] Hai thân run do packet thêm vẫn nằm ngoài khóa được khai

TEP/DONG: `ops/ci_duong_nhanh_test.py:846` (y09), `:741` (y02), `:898` (khai khóa nguyên văn), `:1025` (y13). Workflow liên quan: bước selftest ở gate-ops và logger non-PR ở chuan-bi.

VAN DE: y13 bỏ toàn bộ `run`; lời giải thích nói run mới đã được y08/y09 khóa nguyên văn. Thực tế y09 chỉ đòi dòng `python ops/ci_duong_nhanh_test.py` có mặt trong danh sách dòng. Nó cho phép mọi nội dung khác trước/sau dòng ấy. y02 kiểm output nhưng không kiểm thân run của bước `che do (push / workflow_dispatch luon day du)`, cũng là bước mới. Hai cửa này nằm **trong phạm vi packet**, không thuộc ngoại lệ run có sẵn.

Chốt metadata mới đã vá runner/matrix thật, nhưng cơ chế “có dòng lệnh tức có thực thi” còn nguyên ở y09. Một thay đổi shell trước/sau có thể làm dòng ấy không được thực thi hoặc thay kết quả bước; logger non-PR có thể làm chuan-bi lỗi và ảnh hưởng chuỗi phụ thuộc. Đây là rủi ro đọc từ cấu trúc mã, **chưa chạy payload vô hiệu hóa**. Theo chỉ thị, chỉ mô tả những hướng đó bằng lời để điều phối viết; không tự soạn nội dung tấn công/thoát cây.

Phản chứng an toàn đã chạy: thêm `python --version` trước dòng selftest, giữ nguyên mọi metadata. Actionlint=0; y01–y13/k01–k03 DAT; full suite **55/55 + 111/111, rc=0**. Nó chứng minh khẳng định khóa toàn thân là sai, **không** chứng minh probe vô hại tự làm CI bỏ test. Trước/sau logger và sau selftest cũng sống qua ca chốt tương ứng trong A/B.

Toàn bộ đường vào thuộc phạm vi: classifier run được y01 khóa; ba run liệt kê bước bỏ được y07 giới hạn từng dòng echo và tập tên; cheap-check run được y08 khóa ba dòng; hai run còn thiếu là selftest và logger non-PR. Metadata workflow/job/step, nguồn OS, ma trận include/exclude, needs, shell, env, with, timeout, if, continue-on-error, thứ tự và concurrency do y13/y10–y12 canh. Thân run **có sẵn**: **NGOAI-PHAM-VI**, không tính vào P.

DA THU VA: có — TEST-only, thêm so sánh toàn thân ở hai cửa, không sửa workflow HEAD:

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@ -744,6 +744,10 @@
     bang(chuan_hoa_if(ra.get("che_do")) == "github.event_name == 'pull_request' && steps.phan-loai.outputs.che_do || 'day_du'",
          f"output che_do phai ve day_du khi khong phai PR hoac rong: {ra.get('che_do')!r}")
     bang("os" in ra and "fromjson" not in str(ra.get("che_do")).lower(), "output os phai con, che_do khong boc fromJson")
+    buoc_khac_pr = tim_buoc(wf, "chuan-bi", "che do (push / workflow_dispatch luon day du)")
+    mong = 'echo "DUONG_NHANH: khong phan loai - su_kien=${SU_KIEN} khong phai pull_request, luon DAY_DU"'
+    bang(str(buoc_khac_pr.get("run", "")).strip() == mong,
+         "than run thong bao non-PR phai khop hop dong; khong them/bot lenh")
 
 
 @ca
@@ -849,6 +853,8 @@
            if DONG_GOI_TEST in [x.strip() for x in str(b.get("run", "")).splitlines()]]
     bang(len(goi) == 1 and goi[0][0] == "gate-ops", f"phai co dung mot buoc `{DONG_GOI_TEST}` o gate-ops, thay {[(j, ten_buoc(b)) for j, b in goi]}")
     b = goi[0][1]
+    bang(str(b.get("run", "")).strip() == DONG_GOI_TEST,
+         "than run selftest phai chi co dung lenh goi test; khong them lenh truoc/sau")
     bang("che_do" not in str(b.get("if", "")) and chuan_hoa_if(b.get("if", "runner.os == 'Linux'")) == "runner.os == 'Linux'",
          f"buoc goi test CUA CHINH PACKET khong duoc bi bo theo che_do (no la cong duy nhat canh cac `if:`): if={b.get('if')!r}")
     bang(b.get("continue-on-error", False) is False, "buoc goi test khong duoc co continue-on-error")
```

CHOT RIENG: selftest trước/sau → y09; logger trước/sau → y02. Đột biến vô hại thêm dòng `python --version` tại từng vị trí đã làm bản cũ DAT/hint DO đúng assertion (`out/hints.log`). Nhập các mutant này vào DOT_BIEN; giữ mutants y01/y07/y08 và topology. Điều phối có thể bổ sung phép đo shell làm mất thực thi, nhưng không nhận nó đã được chạy ở lượt này.

DA THU NGHIEM: `out/probes.py yaml`, `out/body-mutant-full.log`, `out/hints.py`, full `tmp/hint-copy/ops/ci_duong_nhanh_test.py`: bản gốc và hint đều 55/55 + 111/111; mutant vô hại sống trên gốc, bị hint chặn. Patch áp `-p0 --fuzz=0` trên bản sao thành công. Rủi ro: thêm lệnh chẩn đoán hợp lệ về sau cũng đỏ và phải cập nhật hợp đồng qua review; đây là hệ quả của phạm vi khóa đã khai.

DO TIN: cao về lỗ khóa và mutant sống; tác động shell/GitHub cụ thể chỉ được mô tả, chưa chạy.

### bang-do-thieu-neo-va-thieu-kiem-ke [P3] Ca tự kiểm phân hoạch t96 lại bị tính vào nhóm hành vi

TEP/DONG: `ops/ci_duong_nhanh_test.py:1094–1104` (t96), `:1167` (phan_hoach_ca), docstring đầu tệp; consumer `goi/kiem_ke.py`.

VAN DE: bản vá đã tách t97/t98/t99 nhưng thêm t96 để kiểm chính phân hoạch. t96 không kiểm sản phẩm hoặc YAML; nó kiểm harness/inventory, nằm dưới phần “tự kiểm của chính bộ test”. `phan_hoach_ca` chỉ nhận tiền tố t97/t98/t99, nên t96 lọt vào `hanh_vi`. Oracle trong t96 lặp cùng danh sách thiếu và ghim tự kiểm=3, vì vậy tổng/độ phủ vẫn xanh dù nghĩa nhóm sai. Kết quả khai **36 hành vi + 13 YAML + 3 registry + 3 tự kiểm**; đúng là **35+13+3+4=55**. Bản vá chuyển lỗi từ script gói sang chính hàm nguồn duy nhất, chưa đóng lớp.

Các cửa cùng lớp phải đồng bộ: bộ phân nhóm; oracle độc lập; danh sách tự kiểm in ra; docstring t* / t99; mỏ neo mutant khi sửa tập tiền tố. Tổng không giao nhau/phủ kín chỉ kiểm số học, không kiểm nghĩa nhóm.

DA THU VA: có — TEST-only; phần chính của hint:

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
-    doc_lap = {"tu_kiem": [n for n in CA if n.startswith(("t97", "t98", "t99"))],
-               "hanh_vi": [n for n in CA if n.startswith("t") and not n.startswith(("t97", "t98", "t99"))],
+    doc_lap = {"tu_kiem": [n for n in CA if n.startswith(("t96", "t97", "t98", "t99"))],
+               "hanh_vi": [n for n in CA if n.startswith("t") and not n.startswith(("t96", "t97", "t98", "t99"))],
@@
-    bang(sum(len(v) for v in nhom.values()) == len(CA) and len(nhom["tu_kiem"]) == 3, "tong nhom phai bang len(CA); tu_kiem la 3 ca t97/t98/t99")
+    bang(sum(len(v) for v in nhom.values()) == len(CA) and len(nhom["tu_kiem"]) == 4, "tong nhom phai bang len(CA); tu_kiem gom t96/t97/t98/t99")
@@
-        if ten[:3] in ("t97", "t98", "t99"):
+        if ten[:3] in ("t96", "t97", "t98", "t99"):
```

`out/HINT.patch` đầy đủ còn sửa docstring và mỏ neo mutant bỏ t97, để tránh lỗi hạ tầng do neo cũ mất. Bảng DO_LAI nên mô tả nhóm bằng chức năng, không chỉ kể t98/t99. Về lâu dài, khi thêm ca tự kiểm mới phải khai nhóm tường minh và kiểm đúng thành viên; không tiếp tục mặc định mọi t mới là hành vi rồi tin một oracle sao lại cùng quy tắc.

CHOT RIENG: chuyển riêng từng t96/t97/t98/t99 sang hành vi → t96 phải đỏ; đại diện y/k và t hành vi giữ nhóm riêng; mutant mất thành viên/trùng thành viên và mutant else gán y vào hành vi phải đỏ. A/B đã đo riêng bốn ca tự kiểm, các phép độ phủ/else có sẵn vẫn xanh/giết đúng trong full suite hint. Executor nhập mutant t96 mới vào DOT_BIEN, không chỉ sửa 3 thành 4.

DA THU NGHIEM: `python3 -B out/probes.py inventory` xác lập sai 36/13/3/3; `python3 -B out/hints.py` ra 35/13/3/4, bốn mutant chuyển nhóm đều DO; full hint **55/55 + 111/111**, rc=0. Rủi ro còn lại của hint tối thiểu: danh sách tiền tố vẫn cần cập nhật có chủ ý khi thêm ca tự kiểm; metadata nhóm là hướng bền hơn nếu tiếp tục mở rộng suite.

DO TIN: cao.

## NGHIEM THU VA GIOI HAN

| Nghiệm thu | Bằng chứng tự chạy | Kết luận |
|---|---|---|
| 1 | t01 DAT; mutant reviewer ép full cho toàn allowlist GIET | Đạt local |
| 2 | t02 DAT; suite mutant nới scripts/ GIET | Đạt local |
| 3 | t05/t06/t17 DAT; mutant fail-open GIET | Đạt local |
| 4 | t03 DAT, đo không gọi Git cho push/dispatch | Đạt local |
| 5 | t08 DAT; mutant .github/ GIET | Đạt local |
| 6 | Suite mutant gỡ điều kiện PR/đổi if bước nặng GIET | Đạt tiêu chí cụ thể; còn P2 bổ sung ở run mới |
| 7 | y05 DAT; mutants paths/paths-ignore GIET | Đạt local |
| 8 | actionlint nền/head=0 có ShellCheck; comment expression rỗng **trong run block**=1 | Đạt local |
| 9 | Registry 22/22→23/23; 938/938; diff 1/0; mutant gỡ mục/lời gọi GIET tự đo riêng | Đạt local |
| 10 | tl selftest trên tmp/head-copy 1715/1715, rc=0; Ruff F delta=0 so origin/master | Đạt local |
| 11 | Không PR thật, không mạng; không thấy executor khai đã đạt | **CHUA_DO_DUOC** |

M1–M4 có bằng chứng local ở trên; không suy các tổng local thành ba required checks success trên GitHub. Windows, fork/rebase thật, base/head SHA theo mọi subtype, skipped/cancelled/concurrency thực, checkout ref scope và thời gian tiết kiệm đều chưa đo. Symlink/mode và shell injection cần payload mới được giữ ở mô tả theo chỉ thị, không tự soạn. Thân run có sẵn: NGOAI-PHAM-VI.

Đột biến sống sót của reviewer: một bản sao **full suite** thêm lệnh chẩn đoán vô hại trước selftest; bốn biến thể trước/sau hai thân run sống qua chốt tương ứng của bản cũ trong A/B. Không gọi đây là bốn exploit đã chạy, không gộp chúng vào 111 mutant của executor. Hai mutant runner/matrix cũ đã GIET đúng.

Hint chỉ chứa `ops/ci_duong_nhanh_test.py`, đường dẫn repo-relative, đã áp bằng `patch -p0 --fuzz=0` trên bản sao. Nhãn nguyên văn: **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**. Full suite hint đã chạy nhưng không tự cấp quyền commit; tám probe A/B bổ sung chưa nằm trong DOT_BIEN của patch.

`cay/` không bị vá; mọi bản sao/probe/hint nằm trong `tmp/` hoặc `out/`. Kiểm cuối HEAD/tree đúng, tracked/index không delta, `git status --short --ignored` rỗng, băm SPEC-r2 không đổi. Snapshot chỉ chứng minh không có delta quan sát tại hai mốc, không chứng minh lịch sử mọi byte ở giữa. Không commit/push/merge, không sửa đặc tả.

TONG: P0=0 P1=0 P2=1 P3=1
So lop: 7; 2 con mo, 5 dong trong pham vi local da do.
