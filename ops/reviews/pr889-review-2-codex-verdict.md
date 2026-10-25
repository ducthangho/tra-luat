verdict: approve
reviewed_sha: 094e8d17ae4dfcf21dca63702c9262267bdc072c
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.
reviewed_tree: 55f5edf2f8601c976f390e8994193129a71203a1
base_sha: e63961f27b53e66db8e6600009f97d5706743063

Đã đo độc lập toàn bộ khẳng định trong 12 dòng thêm của `CLAUDE.md`, kể cả câu executor sửa thêm ngoài HINT.patch lượt trước. Không có finding còn mở. Kết luận này xét tính đúng của tài liệu tại exact SHA trên; không cấp authority merge/land.

Quyền và phạm vi theo chỉ thị trực tiếp `runs/d955f9ef/prompt.snapshot`. Reviewer: Codex, họ model OpenAI/GPT-6; provider `openai_codex`, execution surface `codex_service`, transport `machine` theo phân loại repository cho agent có shell không chạy qua `codex exec`/Desktop. Không có receipt máy để chứng nhận biến thể model/effort hoặc assurance. Không gọi mạng, không push, không sửa `cay-kho/`; chỉ ghi artifact ở thư mục cha.

## BẢNG ĐO

Các lệnh ở cột “đo được” chạy từ gốc `cay-kho/`: `python3 -B ../review_measure.py <hướng>`. Script đọc nguồn bằng `git show` tại full reviewed SHA, trích nguyên hàm bằng AST hoặc đọc YAML; output thật và rc nằm ở BẢNG SĂN. Giả lập nhánh `nt` trên Linux được phân biệt với thực thi native Windows. Kiểm toàn vẹn cuối xác nhận nguồn working tree dùng cho hai cổng khớp byte với Git.

| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Mốc đo, dòng 164/180–181 | 23-10-2026 trên `e63961f` | `history` + HƯỚNG 13: base đầy đủ `e63961f27b53e66db8e6600009f97d5706743063`, commit 23-10; workflow và cong_cu_test byte-identical giữa base và reviewed SHA | Có về mốc nguồn và kết quả tái đo; không chứng nhận phiên đo lịch sử của tác giả |
| Truy nguồn, dòng 164 | #878 thêm nhánh thứ ba | `history`: commit `5585abe` thêm input/nhánh; `52e1f0b` ghim topo; `5585abe` ancestor của reviewed SHA rc=0 | Có; #878 là packet/issue, không phải số PR merge |
| Dispatch chọn đúng input, dòng 164–165 | `runner_set=windows-only` ⇒ `["windows-latest"]` | `dispatch`: evaluator `_danh_gia_bieu_thuc_chuan_bi` trích AST từ `ops/lease_publish_test.py`, áp lên output os thật ⇒ đúng mảng chỉ Windows | Có |
| “KHÔNG có Ubuntu”, dòng 165 | Không có Ubuntu trong output os | `dispatch` + `provenance`: os chỉ Windows; `chuan-bi` vẫn `runs-on: ubuntu-latest` cố định | Có trong phạm vi output os/job ma trận; không phải toàn bộ run không dùng Ubuntu |
| Mặc định input, dòng 165 | `windows-and-ubuntu` | `dispatch`: YAML `default=windows-and-ubuntu`, `required=false`, `type=choice`, options hai giá trị đúng | Có |
| Dispatch mặc định/vắng input, dòng 165 | Vẫn hai nền | `dispatch`: giá trị mặc định, thiếu input, chuỗi rỗng và giá trị khác đều ⇒ `["ubuntu-latest","windows-latest"]` trong evaluator | Có; giá trị khác là đối chứng biểu thức, không khẳng định API cho phép chọn ngoài choice |
| Push/PR, đối chứng ba nhánh | windows-only chỉ ảnh hưởng dispatch | `dispatch`: push master ⇒ Ubuntu; PR thường ⇒ Ubuntu; PR nhãn windows ⇒ hai nền; bơm input windows-only vào push/PR không đổi kết quả | Có; không suy gắn nhãn tự tạo run |
| Câu lịch sử đứng trước | `9e9a74b` dispatch có hai nền | `history`: evaluator áp workflow tại `9e9a74b`, kể cả input windows-only ⇒ hai nền | Không có mâu thuẫn mới; câu lịch sử có neo ngày/SHA, câu mới cập nhật ngay sau |
| Truy nguồn subset Windows, dòng 180 | Từ #879 | `history`: `be00ef7` và `ab25106` ngày 23-10, thông điệp đúng #879 và đều ancestor rc=0; base là merge PR #883 nhánh wp879 | Có; #879 là packet/issue |
| Gate Windows là một phần, dòng 180 | Coverage khác Ubuntu | `matrix`, `steps`, `windows`, `provenance`: mất 7 mảnh Windows, mất gom Windows, có 6 điều kiện bước theo OS, không đo bán kính G5 ở nhánh Windows | Có ở cấu hình và luồng điều khiển |
| `gate-cong-cu`, dòng 181 | Windows chỉ mảnh 0 | `matrix`: 0..7, exclude Windows 1..7; mở matrix windows-only ⇒ đúng một hàng `{os: windows-latest, manh: 0}`; Ubuntu vẫn đủ 0..7 | Có |
| Chế độ G5 thật, dòng 181–182 | Duyệt ca nền rồi dừng | `provenance`: env bước thật → `_doc_che_do` = `('manh',(0,8,'manh/manh-0.txt'))`; `windows`: main AST duyệt hết CA giả rồi return trước phóng con/ghi mảnh | Có về luồng; chưa chạy full CA trên native Windows |
| Thiếu năng lực, dòng 182 | Ca có thể BỎ QUA | `skip_sources`: các lệnh raise thật; `previous_finding`: ca t51 thật với Path giả thiếu /bin/sh phát `BoQuaMoiTruong`, main ghi BỎ QUA và rc=0 khi còn 2 ca đạt | Có; số ca bỏ qua của Windows runner thật chưa đo |
| Mẫu số, dòng 183 | `so_ca = len(CA) - len(bo_qua)` | `skip_sources`: công thức tồn tại; `windows`/`previous_finding`: tổng 3, bỏ qua 1 ⇒ `2/2 đạt`, không phải 2/3 hoặc 3/3 | Có |
| Phạm vi bán kính, dòng 183/188–189 | Chỉ Ubuntu, Windows xanh không chứng minh bán kính | `windows`: các sentinel đột biến/ghi mảnh không bị gọi; `provenance`: gate chính chạy mode gate, các mảnh mode manh, gom chỉ Ubuntu | Có với bán kính `ops/cong_cu_test.py` trong CI này; không diễn giải thành mọi bộ tự đột biến trong kho |
| `gate-cong-cu-gop`, dòng 184 | Loại hẳn Windows | `aggregator`: exclude đúng `{os: windows-latest}`; matrix hai nền chỉ còn hàng Ubuntu | Có |
| Điều kiện job gom, dòng 184–185 | Đòi Ubuntu trong os | `aggregator`: job.if đúng `!cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest')` | Có; còn yêu cầu không bị hủy |
| windows-only ⇒ gom skipped, dòng 184 | Job ấy skipped | `aggregator`: os chỉ Windows ⇒ job.if false ở cả hai trạng thái cancelled; không có hàng Ubuntu. Theo ngữ nghĩa job.if trước matrix, dự kiến skip | Khớp cấu hình; KHÔNG ĐO ĐƯỢC check-run/scheduler thật không mạng |
| Các gate* còn lại, dòng 185 | Còn Windows ở MỨC JOB | `matrix`: gate, gate-cong-cu, gate-ops, gate-nhanh-manh, gate-nhanh-gop, gate-registry, gate-packet-loop đều có hàng Windows; job.if liệt kê trong output | Có ở topo; không bảo đảm cấp runner khi dependency lỗi hoặc run bị hủy |
| Số bước, dòng 185–186 | 6 bước có if theo runner.os | `steps`: duyệt mọi step.if, gồm runner.os hoặc matrix.os; đúng 6 tại ci.yml:430,575,697,786,819,860, không có dạng matrix.os bổ sung | Có, đúng 6 |
| Tắt/thay riêng Windows, dòng 186 | Có job không đồng nghĩa mọi bước chạy | `steps`: hai `!= Windows`, một `== Linux`, một `!= Windows`, cặp lifecycle `== Linux`/`!= Linux` kèm che_do; trên Windows/day_du có 5 điều kiện false và 1 true | Có; lifecycle dùng bước thay thế cho nền không Linux |
| Câu sửa thêm, dòng 187 | Run xanh chỉ chứng minh ca KHÔNG bị bỏ qua đạt | `windows`: 2 pass + 1 skip ⇒ rc=0; all-skip, có ca đỏ, tiền kiểm bỏ qua hoặc bảng đột biến rỗng ⇒ rc=1; `previous_finding` tái hiện bằng t51 thật | Có; đã thu hẹp đúng tập ca thực chạy |
| Đọc log BỎ QUA, dòng 188 | Phải xem riêng các ca chưa đo | `windows`/`previous_finding`: main in riêng tên và lý do BỎ QUA; chúng không tăng số đỏ và bị trừ khỏi mẫu số | Có; đây là yêu cầu đọc evidence, không phải parser tự bảo đảm |
| Ubuntu của CÙNG head, dòng 189 | Không dùng kết quả head khác | `provenance`: `_van_tay` thật trả exact reviewed SHA và sha256 test đúng blob; yêu cầu cùng tested identity phù hợp ràng buộc evidence | Đúng yêu cầu; cặp run thật KHÔNG ĐO ĐƯỢC. PR có thể test synthetic merge, dispatch test ref: cần đối chiếu SHA/tree checkout thực, không chỉ tên nhánh |

## BẢNG SĂN

### HƯỚNG 1: Neo đúng commit và phạm vi thay đổi

- giả thuyết: checkout hoặc diff có thể lệch SHA cần review.
- lệnh (từ `cay-kho/`): `git rev-parse HEAD; git status --short; git rev-parse --is-shallow-repository; git diff e63961f 094e8d1 --stat; git diff 8d5cccb 094e8d1 -- CLAUDE.md`.
- output thật: HEAD `094e8d17ae4dfcf21dca63702c9262267bdc072c`; status rỗng; shallow `false`; `CLAUDE.md | 12 ++++++++++++`, `1 file changed, 12 insertions(+)`; so với `8d5cccb`, đoạn mới thêm điều kiện `BỎ QUA`, công thức mẫu số và sửa câu kết thành `các ca nền KHÔNG bị bỏ qua đạt trên Windows`.
- rc: 0.
- kết luận: KHÔNG PHẢI LỖI. Diff tại đúng SHA, không dùng master hiện tại. Quyền review và write set là chỉ thị `runs/d955f9ef/prompt.snapshot`; reviewer OpenAI Codex, công cụ shell cục bộ qua API, độc lập với executor Claude. Không suy danh tính model từ actor GitHub.

### HƯỚNG 2: Đánh giá os và mặc định runner_set bằng AST

- giả thuyết: Nhánh windows-only có thể lấn push/PR hoặc mặc định không còn hai nền.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py dispatch`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
runner_set={"default": "windows-and-ubuntu", "description": "windows-and-ubuntu (mặc định) hoặc windows-only (bỏ các job ma trận Ubuntu)", "options": ["windows-and-ubuntu", "windows-only"], "required": false, "type": "choice"}
AST source=ops/lease_publish_test.py:_danh_gia_bieu_thuc_chuan_bi
{"event": "workflow_dispatch", "runner_set": "windows-only", "labels": [], "os": ["windows-latest"]}
{"event": "workflow_dispatch", "runner_set": "windows-and-ubuntu", "labels": [], "os": ["ubuntu-latest", "windows-latest"]}
{"event": "workflow_dispatch", "runner_set": "other", "labels": [], "os": ["ubuntu-latest", "windows-latest"]}
{"event": "workflow_dispatch", "runner_set": "", "labels": [], "os": ["ubuntu-latest", "windows-latest"]}
{"event": "workflow_dispatch", "runner_set": null, "labels": [], "os": ["ubuntu-latest", "windows-latest"]}
{"event": "push", "runner_set": null, "labels": [], "os": ["ubuntu-latest"]}
{"event": "push", "runner_set": "windows-only", "labels": [], "os": ["ubuntu-latest"]}
{"event": "pull_request", "runner_set": null, "labels": [], "os": ["ubuntu-latest"]}
{"event": "pull_request", "runner_set": null, "labels": ["windows"], "os": ["ubuntu-latest", "windows-latest"]}
{"event": "pull_request", "runner_set": "windows-only", "labels": [], "os": ["ubuntu-latest"]}
{"event": "pull_request", "runner_set": "windows-only", "labels": ["windows"], "os": ["ubuntu-latest", "windows-latest"]}
PASS: 11 cases; ci.yml at e63961f == reviewed SHA
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 3: Khai triển mọi ma trận gate trên Windows

- giả thuyết: Windows có thể còn mảnh 1..7 hoặc một gate khác cũng mất job.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py matrix`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
os=["windows-latest"] gate-cong-cu=[{"manh": 0, "os": "windows-latest"}]
os=["ubuntu-latest", "windows-latest"] gate-cong-cu=[{"manh": 0, "os": "ubuntu-latest"}, {"manh": 1, "os": "ubuntu-latest"}, {"manh": 2, "os": "ubuntu-latest"}, {"manh": 3, "os": "ubuntu-latest"}, {"manh": 4, "os": "ubuntu-latest"}, {"manh": 5, "os": "ubuntu-latest"}, {"manh": 6, "os": "ubuntu-latest"}, {"manh": 7, "os": "ubuntu-latest"}, {"manh": 0, "os": "windows-latest"}]
os=["ubuntu-latest"] gate-cong-cu=[{"manh": 0, "os": "ubuntu-latest"}, {"manh": 1, "os": "ubuntu-latest"}, {"manh": 2, "os": "ubuntu-latest"}, {"manh": 3, "os": "ubuntu-latest"}, {"manh": 4, "os": "ubuntu-latest"}, {"manh": 5, "os": "ubuntu-latest"}, {"manh": 6, "os": "ubuntu-latest"}, {"manh": 7, "os": "ubuntu-latest"}]
gate: Windows cells=1; job-if=<absent>
gate-cong-cu: Windows cells=1; job-if=<absent>
gate-cong-cu-gop: Windows cells=0; job-if=${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
gate-ops: Windows cells=1; job-if=<absent>
gate-nhanh-manh: Windows cells=8; job-if=<absent>
gate-nhanh-gop: Windows cells=1; job-if=${{ !cancelled() }}
gate-registry: Windows cells=1; job-if=${{ !cancelled() }}
gate-packet-loop: Windows cells=1; job-if=<absent>
PASS: matrix excludes only Windows shards 1..7 and Windows aggregator
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 4: Điều kiện job gom và giới hạn quan sát không mạng

- giả thuyết: windows-only có thể khởi động job gom hoặc sinh lỗi ma trận rỗng.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py aggregator`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
job-if=${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
exclude=[{"os": "windows-latest"}]
{"os": ["windows-latest"], "cancelled": false, "local_job_if": false, "expanded_matrix": []}
{"os": ["windows-latest"], "cancelled": true, "local_job_if": false, "expanded_matrix": []}
{"os": ["ubuntu-latest"], "cancelled": false, "local_job_if": true, "expanded_matrix": [{"os": "ubuntu-latest"}]}
{"os": ["ubuntu-latest"], "cancelled": true, "local_job_if": false, "expanded_matrix": [{"os": "ubuntu-latest"}]}
{"os": ["ubuntu-latest", "windows-latest"], "cancelled": false, "local_job_if": true, "expanded_matrix": [{"os": "ubuntu-latest"}]}
{"os": ["ubuntu-latest", "windows-latest"], "cancelled": true, "local_job_if": false, "expanded_matrix": [{"os": "ubuntu-latest"}]}
PASS: windows-only => if=false, no Ubuntu matrix cell; local inference: job skipped
KHÔNG ĐO ĐƯỢC: actual GitHub check-run conclusion/runner/log at reviewed SHA (no network; no dispatch performed)
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI về cấu hình; KHÔNG ĐO ĐƯỢC trạng thái thực trên GitHub không mạng.

### HƯỚNG 5: Đếm điều kiện OS ở cấp bước bằng YAML

- giả thuyết: Số 6 có thể đếm sót matrix.os hoặc lẫn điều kiện ngoài bước.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py steps`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
1. ci.yml:430 gate / ci-phamvi selftest (phan chung — cong co rang): runner.os != 'Windows'
2. ci.yml:575 gate-cong-cu / actions/upload-artifact@v4: runner.os != 'Windows'
3. ci.yml:697 gate-ops / ci-duong-nhanh selftest (phan loai diff + khoa cau truc if): runner.os == 'Linux'
4. ci.yml:786 gate-ops / don-nhanh selftest (chốt xoá nhánh): runner.os != 'Windows'
5. ci.yml:819 gate-ops / bo ca gate chay TRONG cgroup duoc uy quyen (Linux): ${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}
6. ci.yml:860 gate-ops / gate lifecycle selftest (nen khong co cgroup): ${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}
COUNT=6 (runner.os OR matrix.os in step if; comments/runs-on excluded)
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 6: Chạy nguyên hàm main nhánh Windows với đối chứng

- giả thuyết: Bỏ qua bị tính đạt, không duyệt hết ca hoặc Windows vẫn đo đột biến/ghi mảnh.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py windows`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
nen_bo_qua_dot_bien('nt')=True
nen_bo_qua_dot_bien('posix')=False
nen_bo_qua_dot_bien('java')=False
dat_windows(2, 0, 1)=True
dat_windows(0, 0, 1)=False
dat_windows(2, 1, 1)=False
dat_windows(2, 0, 0)=False
CASE modes=['pass', 'pass', 'skip']; precheck_skip=False; mutant_table_nonempty=True; rc=0; visited=[0, 1, 2]
BỎ QUA baseline_2_skip: capability unavailable (controlled fixture)

cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
CASE modes=['skip', 'skip', 'skip']; precheck_skip=False; mutant_table_nonempty=True; rc=1; visited=[0, 1, 2]
BỎ QUA baseline_0_skip: capability unavailable (controlled fixture)
  BỎ QUA baseline_1_skip: capability unavailable (controlled fixture)
  BỎ QUA baseline_2_skip: capability unavailable (controlled fixture)

cong_cu_test: 0/0 đạt; tổng=3, bỏ qua=3, tiền kiểm bỏ qua=0

TỔNG: CA 0/0 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
CASE modes=['pass', 'fail', 'skip']; precheck_skip=False; mutant_table_nonempty=True; rc=1; visited=[0, 1, 2]
BỎ QUA baseline_2_skip: capability unavailable (controlled fixture)
  ĐỎ  baseline_1_fail: controlled red baseline

cong_cu_test: 1/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 1/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
CASE modes=['pass', 'error', 'skip']; precheck_skip=False; mutant_table_nonempty=True; rc=1; visited=[0, 1, 2]
BỎ QUA baseline_2_skip: capability unavailable (controlled fixture)
  ĐỎ  baseline_1_error: RuntimeError: controlled baseline exception

cong_cu_test: 1/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 1/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
CASE modes=['pass', 'pass', 'skip']; precheck_skip=True; mutant_table_nonempty=True; rc=1; visited=[0, 1, 2]
BỎ QUA (TIỀN KIỂM) precheck: controlled missing capability
  BỎ QUA (TIỀN KIỂM) precheck: controlled missing capability
  BỎ QUA baseline_2_skip: capability unavailable (controlled fixture)

cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=2

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
CASE modes=['pass', 'pass', 'skip']; precheck_skip=False; mutant_table_nonempty=False; rc=1; visited=[0, 1, 2]
BỎ QUA baseline_2_skip: capability unavailable (controlled fixture)

cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 0 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
PASS: unmodified AST main visits all fixtures, skips deducted, zero executed cases/red/precheck/empty mutants fail, no mutation or shard write
SCOPE: Linux controlled execution of Windows branch; real Windows baseline suite NOT RUN
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 7: Nguồn bỏ qua do thiếu năng lực và câu sửa ngoài hint

- giả thuyết: Câu sửa cuối vẫn rộng hơn tập ca nền thực chạy.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py skip_sources`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
["t2_canary_thieu_shellcheck_phai_SUY_GIAM", 248, "actionlint không có trên PATH — cần HÀNH VI THẬT, không giả lập được. Chạy sau khi `ops/cai_cong_cu.sh actionlint` cài để có bằng chứng dương."]
["t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi", 6009, "nền này không có `/bin/sh` để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC"]
["t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi", 6195, "nền này không có `/bin/sleep` để dựng ứng viên TREO — KHÔNG ĐO ĐƯỢC"]
exact denominator formula present=True
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
PASS: capability skips are explicit; both edited statements now limit claim to non-skipped baselines
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 8: Kiểm SHA lịch sử và nguồn #878/#879

- giả thuyết: Tài liệu viện e63961f nhưng cấu hình đã khác tại reviewed SHA.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py history`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
.github/workflows/ci.yml: base-equals-reviewed=True; sha256=b630260ce676292ced82da65f4cb54ec1dc0f66109901e7c1d61746d21baab06
ops/cong_cu_test.py: base-equals-reviewed=True; sha256=23dbdeada416cfa960ff4d2d4a85d7cb4bf29d84240a3fe6274edde7b1b5cf76
ab25106 2026-10-23 wp879: t54 khoá hai biên số không của nhánh Windows (Codex lượt 1) (#879)
be00ef7 2026-10-23 wp879: gate-cong-cu Windows chỉ chạy ca nền (một job), bán kính đột biến đo trên Ubuntu (#879)
52e1f0b 2026-10-22 wp878(#878): ghim topo ci.yml (y13) theo input runner_set; chu thich ra khoi outputs de giu neo dot bien chuan-bi
5585abe 2026-10-22 wp878(#878): ci.yml workflow_dispatch nhan runner_set=windows-only — bo cac job ma tran Ubuntu khi chi can do Windows
5585abe (#878) ancestor_of_reviewed: rc=0
be00ef7 (#879) ancestor_of_reviewed: rc=0
ab25106 (#879) ancestor_of_reviewed: rc=0
9e9a74b historical windows-only dispatch=["ubuntu-latest", "windows-latest"]
PASS: claims dated e63961f still hold at reviewed SHA; #878/#879 ancestry verified
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 9: Cổng doctrine-scan

- giả thuyết: Đoạn mới có thể vi phạm cổng doctrine.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py doctrine`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
COMMAND_RC=0
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 10: Cổng doc-claims-check

- giả thuyết: Đoạn mới có thể chứa tham chiếu cơ học sai.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py doc_claims`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
{
  "ok": true,
  "schema": "doc_claims_check.v1",
  "files_scanned": 113,
  "flags": [],
  "advisory_count": 381,
  "layers_skipped": {},
  "strict": false
}
COMMAND_RC=0
ASSERT ok=true: PASS
Raw JSON: ../review_evidence/doc-claims-check.json (không chạy lại cổng)
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 11: Phạm vi G5, cấu hình chế độ thật và cùng head

- giả thuyết: Một lời khai có thể bị hiểu rộng sang job chuẩn bị hoặc bán kính của bộ test khác.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py provenance`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
_TEN_NEN source=os.name
gate: mode=('gate', None); command='python ops/cong_cu.py kiem-tra --json\npython ops/cong_cu_test.py'
gate-cong-cu: mode=('manh', (0, 8, 'manh/manh-0.txt')); command='python ops/cong_cu.py kiem-tra --json\npython ops/cong_cu_test.py'
gate-cong-cu-gop: mode=--gop; command='python ops/cong_cu_test.py --gop manh'
fixed chuan-bi runner=ubuntu-latest
actual local fingerprint={"head": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "sha256_test": "23dbdeada416cfa960ff4d2d4a85d7cb4bf29d84240a3fe6274edde7b1b5cf76"}
Scope: windows-only removes Ubuntu from os output; chuan-bi itself still uses Ubuntu.
Scope: mutation radius claim concerns cong_cu_test.py; other suites may run their own mutants on Windows.
Same head requires exact tested checkout identity. A PR synthetic merge and a dispatch of its branch may differ.
KHÔNG ĐO ĐƯỢC: paired native Ubuntu/Windows runs and exact checkout identities at this SHA (offline).
PASS: only Ubuntu shards retain the full G5 mutation-radius path in this CI configuration.
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 12: Đối chiếu finding trước bằng ca t51 thật

- giả thuyết: Câu sửa thêm ngoài hint có thể tái tạo overclaim ca nền.
- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py previous_finding`. Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
prior-finding-headers=["### windows-green-does-not-prove-all-baselines  [P2]  Thu hẹp lời khai ca nền đạt: run xanh vẫn có ca bị bỏ qua"]
  BỎ QUA t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi: nền này không có `/bin/sh` để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC

cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
actual t51 with missing /bin/sh + two passing fixtures: rc=0
CLAUDE.md:180:   **Nhưng "gate trên Windows" từ #879 là MỘT PHẦN gate, không phải bản song song** (đo 23-10-2026 trên
CLAUDE.md:181:   `e63961f`, `exclude:` của ma trận): `gate-cong-cu` trên Windows chỉ còn mảnh 0 và ở đó `cong_cu_test.py`
CLAUDE.md:182:   duyệt toàn bộ ca nền rồi DỪNG (ca thiếu năng lực vẫn có thể `BỎ QUA`, và bị trừ khỏi mẫu số:
CLAUDE.md:183:   `so_ca = len(CA) - len(bo_qua)` ở `ops/cong_cu_test.py`) — **bán kính đột biến chỉ đo trên Ubuntu**;
CLAUDE.md:184:   `gate-cong-cu-gop` loại hẳn `windows-latest`, và với `windows-only` thì job ấy `skipped` (`if:` đòi
CLAUDE.md:185:   `ubuntu-latest` trong `os`). Các job `gate*` còn lại vẫn có mặt trên Windows ở MỨC JOB — nhưng 6 bước trong
CLAUDE.md:186:   `ci.yml` mang `if:` theo `runner.os` (tắt hoặc thay riêng trên Windows), nên "có job Windows" chưa phải "mọi
CLAUDE.md:187:   bước chạy". Một lượt `windows-only` xanh chỉ chứng minh **các ca nền KHÔNG bị bỏ qua đạt trên Windows** —
CLAUDE.md:188:   phải đọc riêng các dòng `BỎ QUA` trong log — và nó cũng KHÔNG chứng minh bán kính đột biến: phần đó phải lấy
CLAUDE.md:189:   từ lượt Ubuntu của CÙNG head.
CLAUDE.md:190:   Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
CLAUDE.md:191:   trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
windows-green-does-not-prove-all-baselines: ĐÃ VÁ THẬT in both sentences; extra final-sentence edit preserves the measured scope.
```

- rc: 0.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 13: Kiểm toàn vẹn cuối

- giả thuyết: phép đo/cổng có thể làm bẩn cây reviewed hoặc dùng nguồn khác commit.
- lệnh: các lệnh Git sau chạy tại `cay-kho/`; Python đối chiếu byte của bốn tệp với `git show 094e8d17ae4dfcf21dca63702c9262267bdc072c:<tệp>`.
- output thật:

```text
$ git rev-parse HEAD
094e8d17ae4dfcf21dca63702c9262267bdc072c
rc=0
$ git rev-parse HEAD^{tree}
55f5edf2f8601c976f390e8994193129a71203a1
rc=0
$ git status --porcelain=v1 --untracked-files=all
(stdout rỗng)
rc=0
$ git diff --exit-code
(stdout rỗng)
rc=0
$ git diff --cached --exit-code
(stdout rỗng)
rc=0
$ git hash-object CLAUDE.md
975cd94ff851a3a0ee3aa0493e90184e5f81c874
rc=0
$ git rev-parse HEAD:CLAUDE.md
975cd94ff851a3a0ee3aa0493e90184e5f81c874
rc=0
$ git show -s --format=%H %aI %cI %s e63961f
e63961f27b53e66db8e6600009f97d5706743063 2026-10-23T11:04:54+07:00 2026-10-23T11:04:54+07:00 Merge pull request #883 from ducthangho/agent/wp879-g1-claude
rc=0
reviewed-source-byte-parity=PASS (4 files)
```

- kết luận: KHÔNG PHẢI LỖI. HEAD không đổi; index, worktree và nguồn đo nguyên vẹn.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lưu lịch sử được tìm bằng `git log --all -- ops/reviews/pr889-review-1-codex-verdict.md` tại commit `9ff20c2db8776fbdeedfc95b9ff364afc00a14bc`. Chỉ dùng nguồn ấy để xác định finding cũ; mọi kết luận hiện tại đo trên `094e8d17ae4dfcf21dca63702c9262267bdc072c`, không dùng cấu hình ở commit sau.

| finding lượt trước | phân loại | bằng chứng tự đo tại reviewed SHA |
|---|---|---|
| `windows-green-does-not-prove-all-baselines` [P2] | **ĐÃ VÁ THẬT** | HƯỚNG 6/7/12: nguyên main và ca t51 thật cho 2 đạt + 1 BỎ QUA ⇒ rc=0, mẫu số 2. CLAUDE.md:182–183 giờ nói “duyệt” và công thức trừ ca BỎ QUA; câu sửa thêm tại :187–189 chỉ khẳng định các ca KHÔNG bị bỏ qua và yêu cầu đọc log. Không đổi chính sách skip để làm câu cũ đúng. |

Lớp nguyên nhân: khai quá rộng so với tập ca đã đo. Cả hai biểu hiện của lớp đã được kiểm; 0 lớp/0 biểu hiện còn mở, 0 finding mới. Phần sửa thêm ngoài HINT.patch không sinh lỗi mới.

## GIỚI HẠN VÀ KẾT QUẢ CỔNG

- `passed`: `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, rc=0, “doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine”.
- `passed`: `python3 scripts/tl.py doc-claims-check --json`, rc=0, `"ok": true`, 113 tệp, flags rỗng, 381 advisory lịch sử, không lớp nào skipped. JSON gốc giữ trong `review_evidence/doc-claims-check.json`; không coi scanner xanh là bằng chứng ngữ nghĩa CI.
- `passed`: các phép đo AST/YAML/Git cục bộ, đối chứng nhánh Windows và kiểm toàn vẹn cuối. Không chạy full suite vì đây là thay đổi tài liệu, và không ghi vào cây reviewed.
- `not_run`/`not_measured`: native Windows; actual GitHub job conclusion `skipped`, runner và log của một run tại reviewed SHA; thực thi/giết đột biến Ubuntu; cặp run Ubuntu/Windows cùng tested identity. Không mạng theo yêu cầu. Không coi phần chưa quan sát là passed, cũng không suy ra finding chỉ vì chưa quan sát.
- `HINT.patch`: không tạo vì không có đề xuất vá còn cần thiết.

Biên bản được tạo với `verdict: dang_lam` ngay đầu lượt, nối sau từng hướng thử, sau đó điền bảng đo và đổi verdict khi hoàn tất. Evidence và mã tái lập nằm ngoài `cay-kho/`. Không sửa index, working tree, cấu hình Git hoặc nhánh của executor.
