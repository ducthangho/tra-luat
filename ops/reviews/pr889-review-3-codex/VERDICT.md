verdict: approve
reviewed_sha: 094e8d17ae4dfcf21dca63702c9262267bdc072c
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

## BẢNG ĐO

| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Phạm vi/SHA (toàn diff) | Đo trên e63961f, ngày 23-10-2026; review head đã vá | `git rev-parse HEAD; git show -s --format=fuller e63961f; python3 -B ../review-evidence/measure.py history` → HEAD đúng 094e8d17…; base là tổ tiên, ngày commit base 23-10; ci.yml/cong_cu_test.py/lease_publish_test.py ở base giống byte tại head. H1/H7/H10. | Có về phiên bản; thời điểm từng phép đo lịch sử không thể tái chứng thực |
| Nhánh thứ ba, #878 (CLAUDE.md:164) | #878 bổ sung nhánh windows-only | `python3 -B ../review-evidence/measure_extra.py history-anchored` → trước #878 có 2 mảng literal, tại head có 3; commit 5585abe8499e920e2a6ae8236e70c4096f95e71d và merge 747f983 đều là tổ tiên. H10. | Có |
| Dispatch windows-only (164–165) | Chỉ ["windows-latest"], không Ubuntu | `python3 -B ../review-evidence/measure.py chuanbi` → dispatch windows-only: ["windows-latest"]. Evaluator được trích bằng AST từ chính SHA. H2. | Có |
| Mặc định input (165) | windows-and-ubuntu | `python3 -B ../review-evidence/measure.py chuanbi` → default=windows-and-ubuntu, required=false, type=choice, options có hai giá trị. H2. | Có |
| Dispatch mặc định/vắng/lạ (165) | Mặc định vẫn hai nền | `python3 -B ../review-evidence/measure.py chuanbi` → default/missing/other đều ["ubuntu-latest","windows-latest"]. Giá trị lạ chỉ kiểm biểu thức, không khẳng định API nhận choice ngoài danh sách. H2. | Có |
| Push và PR đối chứng | runner_set chỉ đổi nhánh gọi tay | `python3 -B ../review-evidence/measure.py chuanbi` → push master/PR thường: Ubuntu; PR nhãn windows: Ubuntu+Windows; ép input windows-only không đổi ba ca đối chứng. H2. | Có |
| #879 làm gate Windows chỉ còn một phần (180) | Không phải bản song song đầy đủ | `python3 -B ../review-evidence/measure.py topology; python3 -B ../review-evidence/measure_extra.py history-anchored` → Windows mất mảnh 1..7 và gom; lịch sử be00ef7 thêm đúng thay đổi ấy, là tổ tiên của head. H4/H10. | Có |
| gate-cong-cu, mảnh 0 (181) | Windows chỉ mảnh 0 | `python3 -B ../review-evidence/measure.py topology` → os=[Windows] chỉ [{"os":"windows-latest","manh":0}]; os=hai nền giữ Ubuntu 0..7 và Windows 0. H4. | Có |
| Duyệt ca nền rồi dừng (182) | Windows G5 mảnh chạy qua CA rồi dừng | `python3 -B ../review-evidence/measure.py windows-main` → cả 5 kịch bản đều thăm đủ hai CA giả; cài chốt ném nếu chạm phân mảnh/phóng con/ghi mảnh/cổng cây thật nhưng không chạm. Predicate nt=true, posix/java=false. H6. | Có về đường điều khiển; không giả khai chạy CA thật trên Windows |
| Bỏ qua vì thiếu năng lực (182) | Ca vẫn có thể BỎ QUA | `python3 -B ../review-evidence/measure.py windows-main` → one-skip in BỎ QUA second và rc=0; all-skip rc=1; precheck-skip rc=1. H6. | Có |
| Công thức mẫu số (183) | so_ca = len(CA) - len(bo_qua) | `python3 -B ../review-evidence/measure.py windows-main` → source present=True; một ca bỏ qua trong hai ca cho cong_cu_test: 1/1 đạt, tổng=2, bỏ qua=1. Dòng nguồn 8916. H6. | Có |
| Bán kính chỉ đo Ubuntu trong CI G5 (183) | Windows không có bằng chứng bán kính đầy đủ | `python3 -B ../review-evidence/measure.py windows-main; python3 -B ../review-evidence/measure_extra.py workflow-modes` → gate dùng mode gate (giao vòng đầy đủ cho mảnh); Windows mảnh dùng mode manh nhưng dừng sau CA; gom chỉ Ubuntu. H4/H6/H9. | Có trong phạm vi CI được đoạn văn mô tả |
| gate-cong-cu-gop loại Windows (184) | exclude: windows-latest | `python3 -B ../review-evidence/measure.py topology` → exclude=[{"os":"windows-latest"}], ma trận hai nền sau lọc chỉ Ubuntu. H4. | Có |
| gom với windows-only và if Ubuntu (184–185) | Job skipped vì if đòi ubuntu-latest trong os | `python3 -B ../review-evidence/measure.py topology` → predicate chính xác !cancelled() && contains(fromJson(...),ubuntu-latest) trả false với windows-only cả khi cancelled=false/true; lọc ma trận cho []. H4. | Khớp cấu hình; skipped trên máy chủ là suy luận, KHÔNG ĐO ĐƯỢC lượt chạy thực khi không mạng |
| Các gate* khác ở mức JOB (185) | Vẫn có Windows | `python3 -B ../review-evidence/measure.py topology` → gate=1, gate-ops=1, gate-nhanh-manh=8, gate-nhanh-gop=1, gate-registry=1, gate-packet-loop=1 Windows rows; job-if không đòi Ubuntu. H4. | Có về khả năng được tạo trong ma trận, không bảo đảm job luôn chạy khi hủy/lỗi phụ thuộc |
| Số bước điều kiện OS (185–187) | 6 bước theo runner.os | `python3 -B ../review-evidence/measure.py os-steps` → total=6; runner.os=6; matrix.os=0; đối chiếu quét dòng cũng 6 (430,575,697,786,819,860). H5. | Có |
| Có job chưa phải mọi bước (186–187) | Bước bị tắt hoặc thay riêng Windows | `python3 -B ../review-evidence/measure.py os-steps` → ci-phamvi, upload mảnh, ci-duong-nhanh, don-nhanh, cgroup Linux và lifecycle nền không cgroup có điều kiện OS; Windows bỏ năm bước đầu, dùng bước lifecycle thay cgroup. H5. | Có |
| Câu sửa thêm ngoài hint (187–188) | Lượt xanh chỉ chứng minh ca nền KHÔNG bị bỏ qua đạt | `git diff 8d5cccb HEAD -- CLAUDE.md; python3 -B ../review-evidence/measure.py windows-main` → câu kết đã thu hẹp; one-skip=rc0, 1/1 trên tổng2; one-fail=rc1; all-skip=rc1; dat_windows đòi số ca>0, lỗi=0, số đột biến>0. H6/H7. | Có; không còn suy từ xanh thành tất cả CA đạt |
| Đọc riêng log BỎ QUA (188) | Phải xem riêng ca thiếu năng lực | `python3 -B ../review-evidence/measure.py windows-main` → in BỎ QUA cho CA, BỎ QUA (TIỀN KIỂM) riêng, tổng kết khai bỏ qua và tiền kiểm bỏ qua. H6. | Có; log tổng xanh không liệt kê trong tỷ lệ phần bị trừ |
| Bán kính từ Ubuntu CÙNG head (188–189) | Không lấy bằng chứng từ SHA khác | `python3 -B ../review-evidence/measure_extra.py workflow-modes` → _van_tay trả đúng 094e8d17… và hash test 23dbdeada416…; _gom_manh với header head=000… trả [G-van-tay], errors=1. Bằng chứng giả dựng ngoài repo. H9. | Có; không khẳng định đã có một lượt Ubuntu xanh thật tại SHA này |

## BẢNG SĂN

Đo độc lập tại đúng SHA được yêu cầu; không đọc verdict lượt 2. Các script và tệp bằng chứng nằm ngoài cay-kho/. Lệnh trong bảng được chạy từ cay-kho/; -B tương đương PYTHONDONTWRITEBYTECODE=1 đã dùng khi đo. Output rút gọn có ghi rõ trong từng hướng; log đầy đủ của các phép đo được lưu ở review-evidence/.

HƯỚNG 1: Neo phiên bản và phạm vi bản vá
  giả thuyết : Checkout sai SHA hoặc diff chứa thay đổi ngoài CLAUDE.md.
  lệnh       : (cd cay-kho && git rev-parse HEAD && git status --short && git rev-parse --is-shallow-repository && git config --get core.abbrev); cat numstat.txt; cat diff.patch
  output     : HEAD=094e8d17ae4dfcf21dca63702c9262267bdc072c; git status --short không có dòng nào; shallow=false; core.abbrev=7; numstat: 12 0 CLAUDE.md.
  kết luận   : KHÔNG PHẢI LỖI. Đã neo đúng head, repo sạch, diff chỉ thêm 12 dòng tài liệu. Các phép đo tiếp theo đều thực hiện tại đây, không dùng nhánh master.

HƯỚNG 2: Đánh giá ba nhánh dispatch và các sự kiện khác bằng AST
  giả thuyết : Nhánh windows-only lấn sang push/PR hoặc giá trị mặc định không ra hai nền.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review-evidence/measure.py chuanbi)
  output     : rc=0. Hàm _danh_gia_bieu_thuc_chuan_bi được trích bằng ast.parse/compile từ ops/lease_publish_test.py tại đúng SHA, không import toàn bộ bộ test.

```text
runner_set: default=windows-and-ubuntu; required=false; type=choice; options=[windows-and-ubuntu,windows-only]
dispatch windows-only: ["windows-latest"]
dispatch default: ["ubuntu-latest","windows-latest"]
dispatch missing input: ["ubuntu-latest","windows-latest"]
dispatch other: ["ubuntu-latest","windows-latest"]
push master: ["ubuntu-latest"]
push other ref expression only: ["ubuntu-latest"]
PR ordinary: ["ubuntu-latest"]
PR windows label: ["ubuntu-latest","windows-latest"]
input windows-only cannot alter push/PR: PASS (3 cases)
push trigger: {"branches": ["master"]}
pull_request trigger: null
```
  kết luận   : KHÔNG PHẢI LỖI. Tách rõ: giá trị lạ chỉ được đo trên biểu thức; schema choice không liệt kê giá trị đó. Nhánh push ngoài master chỉ là đánh giá biểu thức, không khẳng định workflow được trigger. Có hai SyntaxWarning về escape có sẵn trong docstring khi ast.parse, không ảnh hưởng rc.

HƯỚNG 3: Cổng doctrine-scan
  giả thuyết : Bổ sung tài liệu sao chép doctrine trái protocol.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .)
  output     : rc=0; doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
  kết luận   : KHÔNG PHẢI LỖI. Log đầy đủ: review-evidence/doctrine.log; mã thoát: review-evidence/doctrine.rc.

HƯỚNG 4: Mở ma trận và điều kiện job độc lập
  giả thuyết : Windows còn mảnh khác 0, job gom vẫn có thể chạy, hoặc gate khác bị loại Windows.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review-evidence/measure.py topology)
  output     : rc=0

```text
gate-cong-cu exclude: [{"os": "windows-latest", "manh": 1}, {"os": "windows-latest", "manh": 2}, {"os": "windows-latest", "manh": 3}, {"os": "windows-latest", "manh": 4}, {"os": "windows-latest", "manh": 5}, {"os": "windows-latest", "manh": 6}, {"os": "windows-latest", "manh": 7}]
gate-cong-cu job-if: None
gate-cong-cu ["windows-latest"] -> [{"os":"windows-latest","manh":0}]
gate-cong-cu ["ubuntu-latest", "windows-latest"] -> [{"os":"ubuntu-latest","manh":0},{"os":"ubuntu-latest","manh":1},{"os":"ubuntu-latest","manh":2},{"os":"ubuntu-latest","manh":3},{"os":"ubuntu-latest","manh":4},{"os":"ubuntu-latest","manh":5},{"os":"ubuntu-latest","manh":6},{"os":"ubuntu-latest","manh":7},{"os":"windows-latest","manh":0}]
gate-cong-cu-gop exclude: [{"os": "windows-latest"}]
gate-cong-cu-gop job-if: ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
gate-cong-cu-gop ["windows-latest"] -> []
gate-cong-cu-gop ["ubuntu-latest", "windows-latest"] -> [{"os":"ubuntu-latest"}]
gop predicate os=['windows-latest'] cancelled=False -> False
gop predicate os=['windows-latest'] cancelled=True -> False
gop predicate os=['ubuntu-latest'] cancelled=False -> True
gop predicate os=['ubuntu-latest'] cancelled=True -> False
gop predicate os=['ubuntu-latest', 'windows-latest'] cancelled=False -> True
gop predicate os=['ubuntu-latest', 'windows-latest'] cancelled=True -> False
MEASURED: YAML exclusions and job predicate false for windows-only, regardless of cancellation.
NOT MEASURED: actual GitHub scheduler conclusion=skipped at this SHA (offline; no API calls).
other gate: windows_rows=1 job-if=None runs-on=${{ matrix.os }}
other gate-ops: windows_rows=1 job-if=None runs-on=${{ matrix.os }}
other gate-nhanh-manh: windows_rows=8 job-if=None runs-on=${{ matrix.os }}
other gate-nhanh-gop: windows_rows=1 job-if=${{ !cancelled() }} runs-on=${{ matrix.os }}
other gate-registry: windows_rows=1 job-if=${{ !cancelled() }} runs-on=${{ matrix.os }}
other gate-packet-loop: windows_rows=1 job-if=None runs-on=${{ matrix.os }}
```
  kết luận   : KHÔNG PHẢI LỖI về cấu hình. KHÔNG ĐO ĐƯỢC trạng thái skipped thực trên máy chủ GitHub vì không mạng; predicate false và ma trận không có Windows là bằng chứng cục bộ, không giả khai đã đọc job run.

HƯỚNG 5: Đếm điều kiện hệ điều hành trên mọi bước YAML
  giả thuyết : Con số 6 sai hoặc bỏ sót if dùng matrix.os.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review-evidence/measure.py os-steps)
  output     : rc=0

```text
gate step=29 ci-phamvi selftest (phan chung — cong co rang): runner.os != 'Windows'
gate-cong-cu step=9 actions/upload-artifact@v4: runner.os != 'Windows'
gate-ops step=9 ci-duong-nhanh selftest (phan loai diff + khoa cau truc if): runner.os == 'Linux'
gate-ops step=12 don-nhanh selftest (chốt xoá nhánh): runner.os != 'Windows'
gate-ops step=13 bo ca gate chay TRONG cgroup duoc uy quyen (Linux): ${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}
gate-ops step=14 gate lifecycle selftest (nen khong co cgroup): ${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}
total: 6
with runner.os: 6
with matrix.os: 0
raw source lines: [[430, "if: runner.os != 'Windows'"], [575, "- if: runner.os != 'Windows'"], [697, "if: runner.os == 'Linux'"], [786, "if: runner.os != 'Windows'"], [819, "if: ${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"], [860, "if: ${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"]]
```
  kết luận   : KHÔNG PHẢI LỖI trong hướng đã đo; đánh giá tổng hợp khi hoàn tất các hướng.

HƯỚNG 6: Phản chứng nhánh Windows bằng AST main thật
  giả thuyết : Nhánh Windows không duyệt hết CA, vẫn chạy đột biến, hoặc bỏ qua chưa bị trừ mẫu số.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review-evidence/measure.py windows-main)
  output     : rc=0

```text
nen_bo_qua_dot_bien(nt,posix,java): [True, False, False]
dat_windows(cases,errors,mutants): [((2, 0, 3), True), ((0, 0, 3), False), ((2, 1, 3), False), ((2, 0, 0), False)]
scenario=all-pass rc=0 visited=['passing', 'second']
cong_cu_test: 2/2 đạt; tổng=2, bỏ qua=0, tiền kiểm bỏ qua=0

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 3 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario=one-skip rc=0 visited=['passing', 'second']
BỎ QUA second: fixture missing capability

cong_cu_test: 1/1 đạt; tổng=2, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 1/1 đạt · ĐỘT BIẾN 3 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario=one-fail rc=1 visited=['passing', 'second']
ĐỎ  second: fixture assertion

cong_cu_test: 1/2 đạt; tổng=2, bỏ qua=0, tiền kiểm bỏ qua=0

TỔNG: CA 1/2 đạt · ĐỘT BIẾN 3 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario=all-skip rc=1 visited=['first_skip', 'second']
BỎ QUA first_skip: fixture missing capability
  BỎ QUA second: fixture missing capability

cong_cu_test: 0/0 đạt; tổng=2, bỏ qua=2, tiền kiểm bỏ qua=0

TỔNG: CA 0/0 đạt · ĐỘT BIẾN 3 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario=precheck-skip rc=1 visited=['passing', 'second']
BỎ QUA (TIỀN KIỂM) precheck: fixture missing
  BỎ QUA (TIỀN KIỂM) precheck: fixture missing

cong_cu_test: 2/2 đạt; tổng=2, bỏ qua=0, tiền kiểm bỏ qua=2

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 3 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
AST source main: so_ca = len(CA) - len(bo_qua) present: True
SCOPE: executes exact AST control flow with synthetic CA on Linux; does not run real Windows CA.
```
  kết luận   : KHÔNG PHẢI LỖI trong hướng đã đo; đánh giá tổng hợp khi hoàn tất các hướng.

HƯỚNG 7: Kiểm SHA lịch sử và câu executor sửa ngoài hint
  giả thuyết : Dẫn e63961f/#878/#879 lệch phiên bản hoặc câu sửa thêm làm rộng kết luận.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review-evidence/measure.py history)
  output     : rc=0

```text
base full: e63961f27b53e66db8e6600009f97d5706743063
base ancestor rc: 0
tree: 55f5edf2f8601c976f390e8994193129a71203a1
patch matches: True
.github/workflows/ci.yml base=head: True
ops/cong_cu_test.py base=head: True
ops/lease_publish_test.py base=head: True
commits base..HEAD:
094e8d1 2026-10-23 docs(CLAUDE.md): (c) thu hep 'ca nen dat tren Windows' — ca BO QUA bi tru khoi mau so (va P2 cross-review codex)
8d5cccb 2026-10-23 docs(CLAUDE.md): (c) do lai 23-10 — nhanh runner_set=windows-only (#878) va Windows chi la MOT PHAN gate (#879)
extra change over 8d5cccb:
diff --git a/CLAUDE.md b/CLAUDE.md
index 44b0bd1..975cd94 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -179,11 +179,14 @@ Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package 
   `runner_set=windows-only` (#878) khi head ĐÃ có lượt PR Ubuntu, để khỏi trả lại 250–330 phút Ubuntu; mặc định vẫn hai nền.
   **Nhưng "gate trên Windows" từ #879 là MỘT PHẦN gate, không phải bản song song** (đo 23-10-2026 trên
   `e63961f`, `exclude:` của ma trận): `gate-cong-cu` trên Windows chỉ còn mảnh 0 và ở đó `cong_cu_test.py`
-  chạy đủ ca nền rồi DỪNG — **bán kính đột biến chỉ đo trên Ubuntu**; `gate-cong-cu-gop` loại hẳn
-  `windows-latest`, và với `windows-only` thì job ấy `skipped` (`if:` đòi `ubuntu-latest` trong `os`). Các job
-  `gate*` còn lại vẫn có mặt trên Windows ở MỨC JOB — nhưng 6 bước trong `ci.yml` mang `if:` theo
-  `runner.os` (tắt hoặc thay riêng trên Windows), nên "có job Windows" chưa phải "mọi bước chạy". Nên một lượt `windows-only` xanh chứng minh **ca nền đạt trên Windows**,
-  KHÔNG chứng minh bán kính đột biến — phần đó phải lấy từ lượt Ubuntu của CÙNG head.
+  duyệt toàn bộ ca nền rồi DỪNG (ca thiếu năng lực vẫn có thể `BỎ QUA`, và bị trừ khỏi mẫu số:
+  `so_ca = len(CA) - len(bo_qua)` ở `ops/cong_cu_test.py`) — **bán kính đột biến chỉ đo trên Ubuntu**;
+  `gate-cong-cu-gop` loại hẳn `windows-latest`, và với `windows-only` thì job ấy `skipped` (`if:` đòi
+  `ubuntu-latest` trong `os`). Các job `gate*` còn lại vẫn có mặt trên Windows ở MỨC JOB — nhưng 6 bước trong
+  `ci.yml` mang `if:` theo `runner.os` (tắt hoặc thay riêng trên Windows), nên "có job Windows" chưa phải "mọi
+  bước chạy". Một lượt `windows-only` xanh chỉ chứng minh **các ca nền KHÔNG bị bỏ qua đạt trên Windows** —
+  phải đọc riêng các dòng `BỎ QUA` trong log — và nó cũng KHÔNG chứng minh bán kính đột biến: phần đó phải lấy
+  từ lượt Ubuntu của CÙNG head.
   Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
   trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
   `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
(Phần tìm lịch sử rộng ban đầu không dùng làm căn cứ; xem HƯỚNG 10 với git log giới hạn reviewed_sha và đối chiếu thay đổi trước/sau #878/#879.)

```
  kết luận   : KHÔNG PHẢI LỖI trong hướng đã đo; đánh giá tổng hợp khi hoàn tất các hướng.

HƯỚNG 8: Cổng doc-claims-check
  giả thuyết : Tài liệu chứa trích dẫn path/SHA/job/test mà cổng có thể bắt.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json)
  output     : rc=0; {"ok": true, "by_layer": {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0, "L6": 0, "L7": 0, "L8": 0, "L9": 0, "L12": 0}, "advisory_count": 381, "layers_skipped": {}, "strict": false}
  kết luận   : KHÔNG PHẢI LỖI. ok=true, không có finding chặn; advisory lịch sử có sẵn được ghi riêng. Log JSON đầy đủ: review-evidence/doc-claims.log.

HƯỚNG 9: Đo cấu hình gọi thật và chốt CÙNG head
  giả thuyết : Job gate Windows còn chạy toàn bộ bán kính hoặc job gom nhận bằng chứng khác HEAD.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review-evidence/measure_extra.py workflow-modes)
  output     : rc=0

```text
callsite: gate step-if= None continue-on-error= False
 command: python ops/cong_cu.py kiem-tra --json ; python ops/cong_cu_test.py
 mode: ('gate', None)
callsite: gate-cong-cu step-if= None continue-on-error= False
 command: python ops/cong_cu.py kiem-tra --json ; python ops/cong_cu_test.py
 mode: ('manh', (0, 8, 'manh/manh-0.txt'))
callsite: gate-cong-cu-gop step-if= None continue-on-error= False
 command: python ops/cong_cu_test.py --gop manh
 mode: gop (artifact consumer)
actual fingerprint: {"head": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "sha256_test": "23dbdeada416cfa960ff4d2d4a85d7cb4bf29d84240a3fe6274edde7b1b5cf76"}
foreign-head artifact:   ĐỎ  gom [G-van-tay]: manh-0.txt đo trên mã KHÁC tiến trình gom (0000000000000000000000000000000000000000/23dbdeada416 ≠ 094e8d17ae4dfcf21dca63702c9262267bdc072c/23dbdeada416) errors= 1
PROVEN: CI main gate delegates full mutation radius; Windows shard stops after baseline; gom uses exact HEAD+test hash.
NOT MEASURED: full Ubuntu mutation pass or Windows runner pass at this SHA; no live CI readback.
```
  kết luận   : KHÔNG PHẢI LỖI trong hướng đã đo; đánh giá tổng hợp khi hoàn tất các hướng.

HƯỚNG 10: Đối chiếu lịch sử chỉ từ reviewed_sha trở về trước
  giả thuyết : Dẫn #878/#879 và ngày 23-10 dựa trên thay đổi sau SHA đang review.
  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review-evidence/measure_extra.py history-anchored)
  output     : rc=0

```text
ancestor: e63961f27b53e66db8e6600009f97d5706743063 rc= 0
ancestor: 5585abe8499e920e2a6ae8236e70c4096f95e71d rc= 0
ancestor: 747f983ccbcaf29a8e5228d09fd05b5a5ab6e479 rc= 0
ancestor: be00ef723eca3fae90932e476d683f233588f2b3 rc= 0
base timestamp: 2026-10-23T11:04:54+07:00 | 2026-10-23T11:04:54+07:00 | Merge pull request #883 from ducthangho/agent/wp879-g1-claude
history <= reviewed_sha #878:
8d5cccb 2026-10-23 docs(CLAUDE.md): (c) do lai 23-10 — nhanh runner_set=windows-only (#878) va Windows chi la MOT PHAN gate (#879)
747f983 2026-10-23 Merge pull request #880 from ducthangho/agent/wp878-g1-claude
ab28423 2026-10-22 wp878(#878): review Codex luot 1 — evaluator tach toan tu ngoai literal/ngoac (P2), ten input theo ngu phap Actions (P3)
52e1f0b 2026-10-22 wp878(#878): ghim topo ci.yml (y13) theo input runner_set; chu thich ra khoi outputs de giu neo dot bien chuan-bi
5585abe 2026-10-22 wp878(#878): ci.yml workflow_dispatch nhan runner_set=windows-only — bo cac job ma tran Ubuntu khi chi can do Windows
history <= reviewed_sha #879:
8d5cccb 2026-10-23 docs(CLAUDE.md): (c) do lai 23-10 — nhanh runner_set=windows-only (#878) va Windows chi la MOT PHAN gate (#879)
e63961f 2026-10-23 Merge pull request #883 from ducthangho/agent/wp879-g1-claude
ab25106 2026-10-23 wp879: t54 khoá hai biên số không của nhánh Windows (Codex lượt 1) (#879)
bc16655 2026-10-23 wp879: neo lại hai đột biến if của gate-cong-cu-gop + đột biến bỏ điều kiện ubuntu (#879)
0c5c4a9 2026-10-23 wp879: cập nhật ghim y11/y12/y13 của ci_duong_nhanh_test cho gate-cong-cu* (#879)
be00ef7 2026-10-23 wp879: gate-cong-cu Windows chỉ chạy ca nền (một job), bán kính đột biến đo trên Ubuntu (#879)
literal branches before #878: 2
literal branches at HEAD: 3
before #878 vs HEAD windows-only : ['ubuntu-latest', 'windows-latest'] -> ['windows-latest']
before #878 vs HEAD windows-and-ubuntu : ['ubuntu-latest', 'windows-latest'] -> ['ubuntu-latest', 'windows-latest']
before #878 vs HEAD unknown : ['ubuntu-latest', 'windows-latest'] -> ['ubuntu-latest', 'windows-latest']
before #879 gate-cong-cu exclude= None job-if= None
at HEAD gate-cong-cu exclude= [{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}] job-if= None
before #879 gate-cong-cu-gop exclude= None job-if= ${{ !cancelled() }}
at HEAD gate-cong-cu-gop exclude= [{'os': 'windows-latest'}] job-if= ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
All history used above is reachable from reviewed_sha; no later file version used.
ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
```
  kết luận   : KHÔNG PHẢI LỖI trong hướng đã đo; đánh giá tổng hợp khi hoàn tất các hướng.

HƯỚNG 11: Kiểm bất biến cuối phiên và whitespace của diff
  giả thuyết : Phép đo làm đổi repository hoặc SHA, hoặc bản vá có lỗi whitespace.
  lệnh       : Các lệnh git dưới đây, cwd=cay-kho/, GIT_OPTIONAL_LOCKS=0.
  output     :

```text
git rev-parse HEAD
rc=0; stdout='094e8d17ae4dfcf21dca63702c9262267bdc072c'; stderr=''
git rev-parse HEAD^{tree}
rc=0; stdout='55f5edf2f8601c976f390e8994193129a71203a1'; stderr=''
git status --porcelain=v1 --untracked-files=all
rc=0; stdout=''; stderr=''
git diff --exit-code
rc=0; stdout=''; stderr=''
git diff --cached --exit-code
rc=0; stdout=''; stderr=''
git diff --check e63961f 094e8d17ae4dfcf21dca63702c9262267bdc072c -- CLAUDE.md
rc=0; stdout=''; stderr=''
```
  kết luận   : KHÔNG PHẢI LỖI. Repository vẫn sạch; không sửa cay-kho/, không commit/push, không gọi mạng.

## KẾT LUẬN

Không có finding P0/P1/P2/P3 trong diff tại reviewed_sha. Phần sửa ở 094e8d1, bao gồm câu kết ngoài hint, khớp phản chứng: xanh 1/1 có thể đến từ tổng 2 ca với một ca BỎ QUA, nên chỉ chứng minh những ca không bị bỏ qua đạt. Tỷ lệ 0/0 hoặc một ca đỏ không cho nhánh Windows trả thành công.

Hai cổng bắt buộc:

- `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **rc=0**; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
- `python3 scripts/tl.py doc-claims-check --json`: **rc=0**, **"ok": true**; 113 tệp; mọi `by_layer` bằng 0; `flags=[]`, `layers_skipped={}`. `claims_flagged=381` đều là advisory (`advisory_count=381`), không phải finding chặn.

Giới hạn phép đo: ma trận, predicate, số bước, mã nguồn và đường điều khiển AST đã đo cục bộ. Không có Windows runner và không có mạng nên không chạy CA thật trên Windows, không đo toàn bộ bán kính Ubuntu, không đọc kết luận scheduler `skipped` hay trạng thái một run GitHub thật tại SHA này. `skipped` trong tài liệu phù hợp điều kiện job đo được; không khai nó thành bằng chứng máy chủ đã readback. Không phát hiện sự thật cục bộ nào trái với mô tả và không coi phần không đo được là đã pass.

Không cần HINT.patch vì không có finding. Không áp patch vào cây thật.

Định danh: reviewer Codex; provider `openai_codex`; execution_surface `codex_service` (có công cụ shell trực tiếp, không phải ChatGPT Web human-mediated); transport `machine`. Không suy model thực tế từ tác giả commit hoặc tên launcher; định danh model máy chủ trả không được kiểm độc lập trong phép đo repo này. Không tự cấp assurance/approval cho state machine hay thao tác land.

`reviewed_tree: 55f5edf2f8601c976f390e8994193129a71203a1`
