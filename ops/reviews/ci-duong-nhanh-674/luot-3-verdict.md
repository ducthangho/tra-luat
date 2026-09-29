verdict: changes_requested
reviewed_sha: 3d12524b21a6a932a71606f290676186e7d3be7d
Reviewed commit: 3d12524b21a6a932a71606f290676186e7d3be7d

## DOI CHIEU LUOT TRUOC

Nguồn: `goi/LUOT-TRUOC-VERDICT.md`, lượt 2, reviewed SHA `9f9bb132d2eca6d6e80b6fd1dab59e0f12466230`. Ngưỡng áp dụng: **0 P0/P1/P2/P3**; D1/D2 chưa được phê duyệt. Giữ stable slug, không xóa lịch sử bằng đổi tên.

| Lớp lượt trước | Kết luận | Bằng chứng tự đo lượt này |
|---|---|---|
| `kiem-lease-bo-sot-duong-vao` | **VA HO** — cửa schema/đuôi đã đóng, D2 còn chờ | `out/lease.log`: `.yaml`/`.yml`, hết/còn hạn sai schema đều CHAN [8]; hết hạn hợp lệ raw=8, hiện tại=[]; t21 kiểm hạn hỏng/thiếu và rc. `out/suite.log`: mutant miễn hết hạn/bỏ `.yml`/bỏ rc bị giết. |
| `diff-check-tu-ha-nguong` | **CHUA VA** — D1 chờ chủ kho, không yêu cầu tự đảo chính sách | `out/whitespace.log`: cả ba loại whitespace raw=2/current=[]; dấu xung đột vẫn đỏ đúng. |
| `chot-yaml-chi-do-su-hien-dien` | **VA HO** — cửa continue-on-error cũ đóng; còn cửa job tiền nhiệm | `out/yaml.log`: literal/biểu thức true/biểu thức điều kiện ở selftest đều GIET. Nhưng thêm `if: false` vào `chuan-bi` vẫn 50/50 + 82/82, rc=0, actionlint=0 (`out/yaml-extra.log`). |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | **DA VA THAT** trong phạm vi đã chỉ ra | `out/data.log`: nền []; mất README/evidence_url, sai băm verdict/prompt đều đỏ đúng. `out/yaml.log` và suite: no-call, bỏ từng t23/t26/t27 đều GIET; t22b thực thi sentinel từng ca. |
| `fixture-lease-phu-thuoc-actor-ci` | **DA VA THAT** | t23 dưới actor khác người cấp đạt, giữ lại actor cha; gỡ riêng lọc môi trường con hoặc patch.dict trong tiến trình đều GIET đúng t23 (`out/lease.log`, `out/yaml.log`). Không đổi authority của validator sản phẩm. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | **VA HO** | Đã bỏ số cứng 43/55, thêm t98, sửa docstring lease và scope refs. Bảng vẫn thiếu kiểm kê riêng lời khai **5 mẫu rc + 3 đột biến thật** của tự kiểm; xem finding P3 và `out/inventory.log`. |

Phạm vi/môi trường:

- Base `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; head tree `01bcb32b8dc7b4a54993925cd19fd97edd8e48ec`.
- Đã đọc trọn SPEC-r2; SHA256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` khớp. Đã đọc AGENTS.md, CLAUDE.md, protocol §8/8.3 và verdict trước.
- Đúng bốn tệp write set; `.claude/dev/ci_dang_ky_test.py` đúng **1 thêm/0 xóa**, thêm mục DA_NOI, không đổi logic.
- Reviewer: OpenAI Codex theo danh tính phiên, thực thi shell qua công cụ của phiên API. Không có runtime receipt độc lập xác minh model/effort/launcher transport; không suy assurance từ GitHub actor. Executor Claude theo gói giao. Đây là verdict nội dung, không phải approval assurance hay quyền land.
- Linux, Python 3.11.15; Actions khai Python 3.12. actionlint 1.7.7, ShellCheck 0.9.0, Ruff 0.15.15. Không mạng, không Windows CI, không PR thật.
- Các lệnh tương đối từ workspace `rv3`, trừ nơi ghi `cd cay`. Mọi phép dùng temp đặt `export TMPDIR="$PWD/tmp"` ở workspace; Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`; Ruff `--no-cache`.
- Chỉ ghi scratch `out/`, `tmp/`; không vá `cay/`, không commit/push/merge. Full selftest chạy trong `tmp/head-copy` vì có thể sinh dữ liệu. Git ký commit chỉ bị tắt trong môi trường fixture; không sửa global config.

## BANG LOP

| Slug | Các biểu hiện/cửa vào | Hạng cao nhất còn mở | Phương án chung | Phép kiểm đóng lớp |
|---|---|---|---|---|
| `kiem-lease-bo-sot-duong-vao` | `.yaml`/`.yml`; hạn còn/hết/hỏng/thiếu; schema/rc; dữ liệu refs | P2-cho-chu-kho | Giữ validator; khai ngoại lệ hạn và scope refs; D2 do chủ kho quyết | Ma trận lease + mutant riêng từng cửa; quyết định D2 còn thiếu |
| `diff-check-tu-ha-nguong` | blank-at-eol, blank-at-eof, space-before-tab; conflict-marker đối chứng | P2-cho-chu-kho | Chủ kho quyết chuẩn whitespace/phạm vi D1 | Ba probe độc lập + conflict; quyết định D1 còn thiếu |
| `chot-yaml-chi-do-su-hien-dien` | Nuốt lỗi ở step/job đã khóa; `if:` job tiền nhiệm chuan-bi chưa khóa | P2 | Kiểm đường phụ thuộc dẫn tới required jobs, gồm tiền nhiệm | Nền xanh, chuan-bi false/literal/expression đỏ đúng y06; các cửa cũ giữ đỏ |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | README, evidence, băm prompt/verdict; no-call, bỏ từng ca | Đóng trong phạm vi | Giữ gọi t23/t26/t27 và chốt tác dụng thực | Dữ liệu bẩn + sentinel riêng + mutant đều đỏ |
| `fixture-lease-phu-thuoc-actor-ci` | Chọn fixture trong tiến trình; validator con; phục hồi actor cha | Đóng | Cô lập actor ở fixture, không hạ authority sản phẩm | Hai mutant cô lập đều GIET đúng t23 |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | Bảng bỏ kiểm kê 5 mẫu/3 mutant tự kiểm; các số cũ đã sửa | P3 | Bổ sung inventory có lệnh/scope cho mọi lời khai định lượng | AST kiểm riêng 5/3; đối chiếu bảng; t98 hiện không canh số này |
| `tin-dung-dot-bien-khong-co-ca-dich` | Ca đích rỗng; iterator cạn trong runner; iterator cạn ở caller main | P2 | Vật hóa và xác thực tập đích trước lần duyệt đầu ở cả caller/callee | Comment vô hại luôn SONG_SOT; tập rỗng HONG; runner và main đều không được cấp GIET rỗng |

Bảy lớp: sáu kế thừa, một mới. Năm lớp còn mở, hai lớp đã đóng trong phạm vi đo. Hai quyết định chủ kho chỉ được đếm trong mục riêng bên dưới.

## BANG SAN

HUONG 1: Phân loại và fail-close
  gia thuyet : SHA thiếu/hỏng, git lỗi/đầu ra cụt hoặc sự kiện khác PR có thể mở nhanh.
  lenh       : `python3 -B out/probes.py classify`; bộ chuẩn `cd cay && python3 -B ops/ci_duong_nhanh_test.py`.
  output     : các t01/t02/t03/t05..t19 đã chọn đều DAT; `all-allowlist-wrong: ('GIET', '')`; chuẩn 50/50, 82/82, TU KIEM PHAN HANG DAT, TONG DAT, rc=0.
  ket luan   : KHONG PHAI LOI trong các cửa local đã đo. Các đường dẫn biên dùng phản chứng có sẵn; không tự soạn payload thoát cây.

HUONG 2: Ba chấm, rename, tự phân loại, miền tiền tố
  gia thuyet : nhánh đích tiến thêm hoặc đổi tên tệp mã sang hồ sơ làm sai đường chọn.
  lenh       : `python3 -B out/probes.py classify` (kho Git thật t11–t15).
  output     : t11/t12/t13/t14/t15 DAT; `python-under-land: duong_nhanh`; sửa workflow/classifier được t08 bắt về day_du.
  ket luan   : KHONG PHAI LOI theo M1/Q2. `.py` dưới bốn prefix vẫn nhanh là quyết định spec. PR sửa cả classifier/test/workflow là ranh giới review, không phải bộ classifier tự chứng thực. Fork/rebase trên GitHub, symlink/mode đặc biệt: KHONG DO DUOC; không dựng payload mới.

HUONG 3: Lease theo đuôi/schema/hạn và actor
  gia thuyet : `.yml` hoặc hết hạn có thể bỏ luôn schema; fixture sạch vẫn phụ thuộc actor.
  lenh       : `python3 -B out/probes.py lease`; `python3 -B out/probes.py yaml`.
  output     : expired-invalid/current-invalid trên cả hai đuôi đều CHAN [8] thiếu packet_issue/granted_by/reviewed_sha_required; expired-valid raw=8/current=[]; t21 và t23 DAT; hai mutant lọc actor GIET.
  ket luan   : KHONG PHAI LOI với các cửa bỏ schema và fixture actor trước đây; ngoại lệ hết hạn là D2 CHO CHU KHO.

HUONG 4: Whitespace từng loại và xung đột
  gia thuyet : ngoại lệ D1 rộng hơn patch/verdict, cho qua lỗi ở mọi tệp hồ sơ.
  lenh       : `python3 -B out/probes.py whitespace`.
  output     : blank-at-eol, blank-at-eof, space-before-tab đều `raw=2 current=[]`; diagnostic raw đúng từng loại; t20c conflict DAT.
  ket luan   : D1 CHO CHU KHO — đạt theo chính sách hiện tại, để lọt theo lệnh trần; chủ kho phải chọn chuẩn. Không tự gọi mọi whitespace là lỗi nội dung.

HUONG 5: YAML, job tiền nhiệm và required checks
  gia thuyet : bỏ cả chuan-bi làm chuỗi needs không chạy mà kiểm cấu trúc vẫn xanh.
  lenh       : `python3 -B out/yaml-extra.py`; `python3 -B out/probes.py yaml`.
  output     : mutant chuan-bi if:false: y01..y10/k01..k03 rc=0; actionlint=0; FULL rc=0, 50/50 + 82/82. Thêm needs gate-registry vào chuan-bi bị actionlint=1 vì vòng needs, không tính là mutant sống sót hợp lệ.
  ket luan   : LOI của chốt YAML ở cửa tiền nhiệm. Cửa continue-on-error literal/expression cũ đã đóng. Không khẳng định workflow HEAD đã có if:false, và không khẳng định đã đo conclusion skipped trên GitHub.

HUONG 6: Dữ liệu hồ sơ và thao tác gọi ca thật
  gia thuyet : checker chỉ in tên DAT nhưng không gọi ca hoặc bỏ t27 khi fast path.
  lenh       : `python3 -B out/data-probe.py`; `python3 -B out/probes.py yaml`.
  output     : nền []; mất README/evidence_url, sai băm verdict/prompt đều lỗi rc=1 với diagnostic đúng; no-call, bỏ t23/t26/t27 GIET. t22b đo sentinel riêng từng hàm qua subprocess.
  ket luan   : KHONG PHAI LOI sau bản vá này trong phạm vi đã đo. gate-registry không bị thay cấu trúc, đúng Q4; push/dispatch vẫn chạy suite nặng.

HUONG 7: Tín dụng đột biến không có ca đích
  gia thuyet : all() trên tập rỗng hoặc iterator đã tiêu thụ báo GIET dù không ca nào chạy trên mutant.
  lenh       : `python3 -B out/credit-probe.py`.
  output     : cùng đột biến chỉ thêm comment: tuple => SONG_SOT; empty => GIET; iterator => GIET. main với tập mutant kiểm soát gồm đúng một mutant vô hại: cả empty và iterator đều CA 50/50, DOT BIEN 1/1, TU KIEM PHAN HANG DAT, TONG DAT, rc=0.
  ket luan   : LOI. Đây là phép thay tập mutant có chủ đích để kiểm harness; không phải tuyên bố bộ 82 hiện tại có ca đích rỗng.

HUONG 8: Lint thật, registry, manifest và delta
  gia thuyet : YAML parse đủ nhưng Actions expression sai; test mới chưa nối sổ; bare Ruff phát sinh lỗi.
  lenh       : `python3 -B out/lint-probe.py` (actionlint head/base và mutant expression rỗng trong comment run trên bản sao); `python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py`; registry ở cay và tmp/base-copy; `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`.
  output     : actionlint head/base=0 với ShellCheck có mặt; mutant rc=1 unexpected end of input [expression]. Ruff mới=0; tl.py head/base=12 F821, diagnostics chuẩn hóa bằng nhau. Registry 22/22 -> 23/23, cả hai 938/938. Manifest ok=true, 180/180, rc=0.
  ket luan   : KHONG PHAI LOI. Bare Ruff tl.py vẫn rc=1 vì nợ nền, delta=0; không gọi lint toàn kho xanh. Blob tl.py head/base/origin/master cùng 41df6dc665e5abd2a977c0b46127daea6e8797fa.

HUONG 9: Số lịch sử và phạm vi refs
  gia thuyet : 345/63/8 và 6/113 là số trôi hoặc không tái lập được.
  lenh       : `cd cay && python3 -B ../goi/do_lai_so.py`; `python3 -B out/ref-scope.py`; `python3 -B out/probes.py counts`; `python3 -B out/inventory.py`.
  output     : 345/63/8; full 552 refs: 113/113 lease đạt; cùng head với 1 ref: 6/113 lỗi bia mộ. CA 50 = 35 t + 10 y + 3 k + 2 self; mutants 82; 5 mẫu rc + 3 mutant thật; ca dữ liệu 6.643 giây.
  ket luan   : KHONG PHAI LOI với các số đã giao, đúng scope; LOI P3 với kiểm kê 5/3 còn thiếu trong bảng. Refs/thời lượng Actions thật KHONG DO DUOC.

HUONG 10: Linux/Windows, log, concurrency và lỗi chuẩn bị
  gia thuyet : mode lạ bỏ bước nặng; thay điều kiện OS/cancellation làm thiếu required checks.
  lenh       : `python3 -B out/probes.py yaml`; đọc `git -C cay diff 1741e0a HEAD -- .github/workflows/ci.yml`.
  output     : y02/y03/y04/y06/y07/y08/y09/y10 DAT; bốn job đều needs chuan-bi, không if cấp job ở HEAD; BO_QUA có 5 gate, 3 gate-ops, 1 packet-loop; log liệt kê khớp đúng. Concurrency không đổi. Selftest packet chỉ chạy Linux, kiem-re shell bash; điều kiện cgroup giữ Linux và nhánh bù giữ khác Linux.
  ket luan   : KHONG PHAI LOI về cấu trúc đã đo. Không chạy Windows; không suy skipped là success. Continue-on-error tại hai bước chuẩn bị giữ fallback day_du khi lệnh thất bại; runner/job hỏng/cancel không được đo bằng phép này. Log liệt kê mọi bước nặng theo danh sách, kể cả bước vốn không áp cho OS hiện tại; không coi đó là bằng chứng từng bước đã chạy.

## BANG DO

| Khẳng định | Đã khai trong bảng giao? | Đo được | Khớp? |
|---|---|---|---|
| Suite N/N, M/M | Có, không ghim số | 50/50, 82/82, tự kiểm DAT | Có cho tập chuẩn; chưa đủ chứng minh harness an toàn với tập đích hỏng |
| Phân rã t/y/k/self | Có | 35/10/3/2 = 50 | Có |
| Tự kiểm có 5 mẫu rc và 3 mutant thật | **Thiếu kiểm kê riêng** | AST=5/3; tự kiểm [] | Số đúng; bảng thiếu là finding theo yêu cầu packet |
| Ba ca dữ liệu khoảng 6–7 giây | Có | 6.643 giây trên cây thật; một đối chứng bản sao 6.97 giây | Có trong môi trường này |
| 22/22 -> 23/23, phản chứng 938/938 | Có | Đúng, cả hai rc=0 | Có |
| DA_NOI chỉ 1 dòng thêm | Có | numstat 1/0 | Có |
| actionlint rc=0, ShellCheck 0.9.0 | Có | Base/head 0; công cụ 0.9.0; mutant rỗng 1 | Có |
| Ruff F tl.py 12, delta 0 | Có | Head/base 12; blob origin/master bằng nhau | Có; bare rc=1 |
| AL_VER 4 dòng | Có | 4 bằng regex | Có tại head này; phải đo lại sau #668 |
| 345 merge/63 hồ sơ/8 whitespace, ~13% | Có | 345/63/8; 8/63=12.70% | Có trong 400 merge first-parent từ base, không phải tỷ lệ PR tương lai |
| Lease 6/113 một ref; 0/113 với 552 refs | Có | Cả hai tái lập cùng head | Có; chưa đo refs Actions |
| G5 46.5 phút/52 phút; GitHub coi skipped đạt | Có, khai giới hạn | Không có mạng/PR thật | KHONG DO DUOC, không dùng làm positive evidence |
| tl selftest | Spec yêu cầu | Môi trường sạch 1715/1715, rc=0 | Đạt; lượt đầu 1714/1715 là lỗi rig đã cô lập |
| Manifest strict | Spec yêu cầu | ok=true, expected=checked=180 | Có |

Tập refs lưu ở `out/refs-one.txt` và `out/refs-full.txt`; SHA256 lần lượt `65985e8eee133f712f020294728aa19ad7336ae17f7e508d4789bc49e34403c8` và `47d1e85d26491f2ac5c15a20ab60c5d69025b9f61f57c563487bb950685c6719`. Phép một-ref ở đây là fetch exact head vào nhánh review, không tự gọi đó là quan sát runner Actions.

## FINDINGS

### chot-yaml-chi-do-su-hien-dien [P2] Chốt required job bỏ sót điều kiện của job tiền nhiệm chuan-bi

TEP/DONG: `ops/ci_duong_nhanh_test.py:798` (y06), `:718` (y01); `.github/workflows/ci.yml:35` và các `needs: chuan-bi`.

VAN DE: y06 chỉ cấm if ở ba required jobs; y01 kiểm các step chuẩn bị, không kiểm if ở chính job. Thêm `if: false` ở chuan-bi vẫn qua toàn bộ suite và actionlint. Các job phụ thuộc không thể cung cấp bằng chứng thực thi khi tiền nhiệm bị bỏ; chính cổng test mới cũng thuộc chuỗi đó. Đây là thiếu độ phủ của chốt được giao, không phải khẳng định HEAD đã vô hiệu hóa CI. Giữ slug vì vẫn là kiểm sự hiện diện mà bỏ đường làm cổng không chạy.

DA THU VA: có — TEST-only, thêm tiền nhiệm vào kiểm y06, tại bản sao tạm. Không sửa workflow HEAD.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
-    for job in BAT_BUOC:
+    for job in ("chuan-bi", *BAT_BUOC):
         bang(job in wf["jobs"], f"thieu job bat buoc {job}")
```

Chốt riêng: literal false, expression false và điều kiện sự kiện ở chuan-bi; mọi if ở ba required jobs; continue-on-error job/step; bước selftest/kiem-re; các điều kiện bước nặng và log. Cửa tiền nhiệm cần mutant riêng trong DOT_BIEN, không chỉ mở rộng assertion. Hint trên khóa mọi if của chuan-bi bằng cấu trúc; đã thử literal/expression false. Đồ thị needs vòng bị actionlint chặn, không được nhận tín dụng cho y06. Biến đổi runner/matrix hoặc shell để vô hiệu hóa lệnh là hướng kiểm bổ sung; chưa tự soạn payload vô hiệu hóa shell, không khai đã đóng toàn bộ hành vi Actions.

DA THU NGHIEM: `python3 -B out/yaml-extra.py`: mutant sống sót FULL 50/50 + 82/82, rc=0; actionlint=0. `python3 -B out/hints.py`: baseline y06 rc=0; literal/expression false rc=3 đúng `DO:y06...:chuan-bi...`; patch dry-run -p0 --fuzz=0 rc=0.

DO TIN: cao về lỗ chốt local; không đo conclusion trên GitHub.

### tin-dung-dot-bien-khong-co-ca-dich [P2] Harness cấp GIET khi không còn ca đích để chạy trên bản đột biến

TEP/DONG: `ops/ci_duong_nhanh_test.py:1128` (chay_mot_dot_bien), `:1144` (all trên hang), `:1210` (main duyệt dich trước runner).

VAN DE: `dich=()` không chạy ca gốc hoặc ca đột biến, nhưng `all(h[1] == "GIET" for h in hang)` trên list rỗng là True. Iterator một phần tử bị vòng baseline tiêu thụ rồi cho cùng kết quả; khi đi qua main, vòng kiểm tên lại tiêu thụ nó trước runner. Đối chứng comment vô hại vốn SONG_SOT đổi thành GIET, main báo 1/1 bị giết đúng + TONG DAT. Các tuple của 82 mutant hiện tại đều hợp lệ; không phủ nhận lần đo 82/82. Lỗi nằm ở hợp đồng xác minh tín dụng và thiếu tự kiểm cho trạng thái không có bằng chứng dương.

DA THU VA: có — TEST-only, xác thực tập đích khác rỗng, tên tồn tại, vật hóa trước lần đọc đầu tại cả caller/callee.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
 def chay_mot_dot_bien(ten, tep_va_ham, dich):
+    dich = tuple(dich)
+    if not dich or any(ten not in CA for ten in dich):
+        return "HONG", "tap ca dich rong hoac khong hop le"
     tep, ham = tep_va_ham
@@
     for ten, tv, dich in DOT_BIEN:
+        dich = tuple(dich)
         for d in dich:
```

Chốt riêng cần tích hợp: (1) empty ở runner → HONG; gỡ kiểm rỗng phải đỏ; (2) iterator/generator ở runner với comment vô hại → SONG_SOT; gỡ vật hóa runner phải đỏ; (3) iterator qua main không được bị vòng kiểm tên tiêu thụ — cần đối chứng mutant thật vẫn GIET và comment vẫn không GIET; gỡ vật hóa main phải đỏ đúng hợp đồng, không chỉ đòi rc khác 0; (4) tên ca không tồn tại → HONG; (5) tuple hợp lệ và mutant thực sự bị chốt bắt giữ GIET. Một lựa chọn khác là chỉ nhận tuple/list và từ chối mọi iterator ở boundary; phải khai hợp đồng nhất quán, không để iterator cạn thành tập rỗng hợp lệ.

DA THU NGHIEM: `python3 -B out/credit-probe.py`: tuple SONG_SOT; empty/iterator GIET; main empty/iterator đều 50/50 + 1/1 + TU KIEM DAT + rc=0. `python3 -B out/hints.py`: tuple/iterator SONG_SOT; empty/unknown HONG; main empty/iterator đều 50/50 + 0/1 + TU KIEM DAT + rc=1. Đây là tập mutant kiểm soát một phần tử, không phải chạy lại toàn bộ 82 với hint. Không dùng lỗi phụ của self-check làm lý do giết: log cuối có TU KIEM PHAN HANG DAT ở cả hai lượt main hint.

DO TIN: cao.

### bang-do-thieu-neo-va-thieu-kiem-ke [P3] Bảng giao còn bỏ lời khai định lượng của tầng tự kiểm

TEP/DONG: `goi/DO_LAI.md:7–18`; `ops/ci_duong_nhanh_test.py:20–22`, `:1151–1174`.

VAN DE: Bảng mới đã sửa số ca, phân rã và thời gian nhưng không liệt kê riêng lời khai NĂM mẫu rc và BA đột biến thật; dòng “t98/t99 (tự kiểm)” không phải inventory của hàm `tu_kiem_phan_hang`, và chạy suite chỉ in DAT, không in hai số này. AST đo đúng 5/3. Đây không phải số sai; yêu cầu packet quy định mỗi khẳng định định lượng bảng bỏ sót là finding, và lớp này đã được nhắc ở lượt trước. t98 hiện chỉ tìm số dạng N/N ca/đột biến và khoảng tNN..tMM, không bắt số bằng chữ NĂM/BA.

DA THU VA: không sửa gói giao hay spec; đã chạy inventory độc lập. Hint cập nhật bảng do người dựng bundle thực hiện, không mở write set kho.

```diff
--- goi/DO_LAI.md
+++ goi/DO_LAI.md
@@
+| Tu kiem phan hang: 5 mau rc + 3 dot bien that | AST ham tu_kiem_phan_hang: dem tuple cua vong rc va list kiem; chay ham, doi [] | khong gom vao 82 DOT_BIEN; sai ten ca moi do bang mau rc, chua co mutant that |
```

Chốt riêng: kiểm số tuple mẫu rc; kiểm số phần tử list mutant tự kiểm; kiểm kết quả của chúng; đối chiếu lời khai theo đúng source/SHA. Đột biến đổi số lượng một trong hai tập hoặc lời khai tương ứng phải làm phép đối chiếu đỏ; t98 hiện tại không thay được phép này. Không yêu cầu thay đặc tả đóng băng.

DA THU NGHIEM: `python3 -B out/inventory.py` → `rc samples 5 real mutants 3`; `python3 -B out/probes.py counts` → `self-check []`. Chưa triển khai checker đối chiếu bảng mới; không khai hint tài liệu đã đóng lớp.

DO TIN: cao về thiếu inventory; số đo hiện tại khớp.

## CHO-CHU-KHO-QUYET

Một mục chung, hai hàng **P2-cho-chu-kho**. Không yêu cầu executor tự vá hoặc đảo hai chính sách này. Chưa có quyết định chủ kho thì không tính chúng là đã duyệt.

| Quyết định / slug | Hạng | Tác động hiện tại tự đo | Phần chờ chủ kho |
|---|---|---|---|
| D1 / `diff-check-tu-ha-nguong` | P2-cho-chu-kho | Ba loại whitespace raw=2/current=[] trên tệp `.md` thuộc allowlist, không chỉ patch. Conflict vẫn đỏ. Scope lịch sử có 8/63 diff hồ sơ bị raw bắt. | Theo cấu hình hiện tại: đạt; theo chữ trần M2: để lọt whitespace. Cấm tuyệt đối có thể đỏ với whitespace có chủ ý. Cần quyết chuẩn và phạm vi ngoại lệ. |
| D2 / `kiem-lease-bo-sot-duong-vao` | P2-cho-chu-kho | Lease hết hạn hợp lệ raw check=8/current=[]; hết hạn sai schema vẫn CHAN [8] ở cả hai đuôi. Một ref có 6/113 lỗi bia mộ, đủ 552 refs có 0/113. | Hiện tại bỏ chốt hạn để hồ sơ lịch sử qua, lệch check trần. Có thể đỏ do thiếu dữ liệu refs. Cần quyết ngoại lệ hạn và cách xử lý scope thiếu; không suy schema tương đương tuyệt đối trong mọi môi trường GitHub. |

TEP/DONG: D1 `ops/ci_duong_nhanh.py:66`, `:175`; D2 `:69–73`, `:204–241`.

DA THU VA: không đảo chính sách. Cửa `.yml`, hết hạn sai schema, hạn hỏng/thiếu và bỏ rc đã có phản chứng được tự chạy. Hint chỉ bổ sung lời khai có điều kiện, không phải tự cấp quyết định:

```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@
 đúng là lệch đặc tả; ĐANG CHỜ QUYẾT ĐỊNH CỦA CHỦ KHO ở Issue #674, không tự coi là đã duyệt):
+  Lượt 3: D1 cho qua ba loại whitespace trên toàn allowlist; D2 giữ schema nhưng bỏ hạn.
+  Phạm vi refs Actions chưa đo; 1 ref/552 refs là hai phép local trên cùng head.
```

Chốt riêng D1: ba whitespace độc lập + conflict; sau quyết định mới đổi kỳ vọng/mutant theo chuẩn được duyệt. Chốt riêng D2: hai đuôi × còn/hết/hỏng/thiếu hạn, schema/authority/băm, lỗi tiến trình/rc; đối chứng lease sạch; scope refs ghi bằng tập tên/OID và băm. Không coi “mutant khôi phục lệnh raw bị giết” là chứng minh raw trái SPEC-r2.

DA THU NGHIEM: `out/probes.py whitespace`, `out/probes.py lease`, `goi/do_lai_so.py`, `out/ref-scope.py`: kết quả ghi ở bảng săn; tất cả phép đã hoàn tất. DO TIN: cao trong phạm vi local.

## NGHIEM THU VA GIOI HAN

- M1/M3/M4: đạt các ca local đã chạy; M2 có đủ bước nặng/log/kiểm rẻ, còn D1/D2 lệch chữ trần chưa quyết và chốt YAML cần bổ sung.
- Nghiệm thu 1–5: ca t01/t02/t03/t05/t06/t08 và mutants tương ứng đã chạy; hướng all-allowlist thành day_du có mutant độc lập GIET.
- Nghiệm thu 6–7: các mutant bỏ điều kiện PR, luôn-bỏ bước nặng, paths/paths-ignore đều GIET trong bộ 82; lỗ bổ sung ở chuan-bi vẫn là finding.
- Nghiệm thu 8: actionlint + ShellCheck có mặt; mutant expression rỗng rc=1 đúng lỗi expression.
- Nghiệm thu 9: nền 22/22, head 23/23, cả hai 938/938; DA_NOI diff 1/0; mutant gỡ mục và gỡ lời gọi đã chạy trong bộ 82 và đỏ đúng k01/k02/k03/y09.
- Nghiệm thu 10: **ĐẠT local**: selftest 1715/1715, rc=0 (`out/tl-selftest-clean-env.log`); Ruff delta=0 so origin/master, bare tl.py còn 12 F821 nền.
- Nghiệm thu 11: **CHUA_DO_DUOC**, không có PR thật; không thấy lời khai của executor rằng đã đạt 11. Không tự dùng thời gian 52 phút lịch sử làm nghiệm thu mới.
- Điều kiện tích hợp #668/Q5 cần đo lại trên head sau tích hợp; verdict không tự chuyển sang head đó. Không chỉnh spec hay mở phạm vi test Windows.
- Hướng symlink/thoát cây và shell vô hiệu hóa cần payload mới chỉ mô tả bằng lời để điều phối bổ sung; không tự soạn nội dung đó. Không dùng việc chưa đo làm pass.

## DOT BIEN SONG SOT VA HINT

- Sống sót FULL suite: thêm `if: false` vào chuan-bi, 50/50 + 82/82 + TONG DAT, actionlint=0.
- Comment vô hại vốn phải sống sót, nhưng được cấp GIET khi đích rỗng/iterator cạn; tập kiểm soát main báo 1/1. Đây là tín dụng giả, không phải mutant sửa chức năng thật.
- Thêm needs gây vòng bị actionlint bắt: không tính là lỗ sống sót hợp lệ; không nhận nó làm bằng chứng y06 có răng.
- Các cửa lượt trước: continue-on-error selftest, no-call dữ liệu và cô lập actor đều GIET đúng trong các phép đã chạy.
- `out/HINT.patch` chỉ thay tệp TEST. Nhãn: **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**. `patch -p0 --fuzz=0 --dry-run` trên bản sạch tạm rc=0. Hint đã đo A/B tập trung, chưa chạy full bộ 82 của hint; executor phải tích hợp chốt/mutant riêng và chạy gate.

## KIEM TRA CUOI

Full selftest đã hoàn tất: `export TMPDIR="$PWD/tmp" PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false; (cd tmp/head-copy && python3 -B scripts/tl.py --selftest)` → **1715/1715, rc=0**. `core.abbrev=7` nằm trong cấu hình repo của bản sao, không ép bằng biến môi trường.

Lượt đầu `out/tl-selftest.log` là 1714/1715 vì reviewer đặt `GIT_CONFIG_KEY_0=core.abbrev` ở môi trường: ca r226 cố đổi repo tạm sang 8 nhưng bị môi trường đè lại 7. `python3 -B out/abbrev-probe.py` chạy chính thân ca trích từ AST: env-pin=False, repo-pin=True. Không tính lỗi rig này thành hồi quy của executor; đã chạy lại toàn suite để xác nhận.

`out/final-snapshot.log`: **2443 tệp, content_delta=[]**; HEAD/tree đúng như đầu báo cáo; tracked/index diff rc=0; `git status --short --ignored` rỗng; băm SPEC-r2 không đổi. Snapshot băm đầu được lấy sau khi một số suite đã khởi động, nên không tuyên bố nó chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên. Các lệnh đã dùng bytecode-off/no-cache; snapshot không thấy dữ liệu phát sinh trong checkout. Sandbox thực tế workspace-write; checkout được đối xử read-only theo vai trò, không giả khai cơ chế filesystem buộc read-only.

Các log dùng cho kết luận đã kết thúc. `out/PROGRESS.md` giữ phần ghi tăng dần trước khi tổng hợp. Full hint không được khai là đã chạy; chỉ bộ chuẩn, mutant reviewer, và A/B tập trung đã chạy như mô tả. Ngưỡng severity chưa đạt, D1/D2 chưa được chủ kho quyết; không approve/merge/land. Lượt 3 này theo chỉ thị trực tiếp đã giao; không tự mở thêm lượt review hoặc suy quyền vượt budget/assurance cho bước kế tiếp.

TONG: P0=0 P1=0 P2=2 P2-cho-chu-kho=2 P3=1
So lop: 7 (6 ke thua, 1 moi); 5 lop con mo, 2 lop da dong trong pham vi do. Khong dem trung D1/D2.
