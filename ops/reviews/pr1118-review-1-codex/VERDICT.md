verdict: changes_requested
reviewed_sha: b13d3ef93724d249b3db6eeef6d3fe43a61b08f9
Kết quả: 0 P0, 1 P1, 2 P2, 0 P3.

Đang kiểm tra độc lập theo `prompt.snapshot`; chỉ đọc và đo cục bộ, không sửa `cay-kho/`, không gọi mạng.

## Hướng 1 — Neo cây và cổng nguồn/toàn vẹn

**Giả thuyết:** sandbox sai SHA, diff vượt phạm vi, băm hỏng hoặc cổng nguồn không đạt.

**Lệnh:** `git -C ../../cay-kho status --porcelain=v1`; `git -C ../../cay-kho rev-parse HEAD HEAD^{tree} refs/remotes/origin/master`; `git -C ../../cay-kho rev-parse --is-shallow-repository`; `git -C ../../cay-kho diff --stat 3bdd987 HEAD`; `PYTHONDONTWRITEBYTECODE=1 python3 ../../cay-kho/ops/land_evidence_nguon.py --root ../../cay-kho` và thêm `--tep ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`; `sha256sum -c SHA256SUMS.txt` trong provenance. Các lệnh thoát 0.

**Output thật:** worktree sạch; HEAD `b13d3ef93724d249b3db6eeef6d3fe43a61b08f9`, tree `b0054bf730d8aad494e3fb9ad797585ecd77e836`; origin/master `180039c4b791fba4c89991623151cbb7378fce53`; shallow `false`; diff 8 tệp, 378 dòng thêm/4 dòng bỏ, đúng YAML + manifest + 6 bản trích. Cổng toàn kho: `75 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 100`, `TỔNG: ĐẠT`. Cổng riêng: `1 ĐẠT · 0/0 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1`, `TỔNG: ĐẠT`. Băm: 22/22 `OK`, gồm cả 6 tệp mới. Output cổng lưu tại [gate-all.txt](gate-all.txt), [gate-target.txt](gate-target.txt).

**Kết luận: KHÔNG PHẢI LỖI.** Cổng chỉ đo các luật của nó, chưa chứng minh nội dung lời khai đúng hay đủ bốn mốc CI theo §10.2.2. Reviewer thực tế: Codex/OpenAI, công cụ shell cục bộ qua API, context độc lập với executor; không đăng GitHub.

## Hướng 2 — Tính trung thực của sáu bản trích REST

**Giả thuyết:** bản trích thiếu job/trường phục vụ lời khai, sai SHA/giờ/số/trạng thái, hoặc header gọi bản trích là phản hồi thô.

**Lệnh:** `python3 audit_readbacks.py` (script tại thư mục verdict, chỉ đọc JSON). Ánh xạ rõ `merged_by -> merged_by.login`, `head -> head.sha`, `head_ref -> head.ref`; commit dùng `commit.tree.sha`, `parents[*].sha`, `files[*].{filename,additions,deletions}`. Jobs đối chiếu từng trường từng ID, cả thứ tự và tập ID, độ dài so `total_count`; kiểm tiền tố SHA-256 của 9 phản hồi thô theo `FETCH-LOG.txt`.

**Output thật:** `CHECKS 233 KHOP 233 LECH 0` (224 phép so bản trích + 9 băm nguồn). `readback-pr-1111.json`: 8/8; commit: 4/4 (gồm hai mảng đầy đủ); mỗi run: 11/11; jobs run huỷ: 3/3; jobs run thành công: 187/187. Run `41285898441`: `total_count=0`, `jobs=[]`. Run `41290009265`: 23/23 job `success`, 23 nhãn `ubuntu-latest`, 0 job `runner_id=0`, cùng `head_sha=3bdd9877cab2543adc413a32a47decbb585ded97`. Script thoát 0. Bảng từng trường/giá trị/nguồn/kết quả: [readbacks-field-check.tsv](readbacks-field-check.tsv); tóm tắt: [readbacks-summary.txt](readbacks-summary.txt).

**Kết luận: KHÔNG PHẢI LỖI** về phép trích và cách gắn nhãn. Header YAML dòng 13–17 liệt kê đúng sáu ngoại lệ là `BAN TRICH truong tu REST, 2026-11-01`. Không đòi bản trích chứa mọi trường API vì đã khai rõ loại tệp; các trường dùng để khẳng định merge/run/jobs đều có và khớp. Phản hồi thô chụp 18:21:37–18:21:42Z; bản trích được lập trước đó, không nhầm hai thời điểm. Tính đúng của nguyên nhân huỷ và câu “kế tiếp” cần kiểm riêng, không suy từ các JSON khớp này.

## Hướng 3 — Merge ghi sổ, tổ tiên và đúng tập tệp của ba PR xen giữa

**Giả thuyết:** merge/cha/tree/số dòng sai, comment chốt lệch head, hoặc câu “ba PR chỉ thêm spec/ops” bỏ sót thay đổi khác.

**Lệnh:** `python3 audit_git_and_claims.py` (thoát 0); script gọi `git rev-parse`, `git show -s --format=%P`, `git diff --numstat`, `git log --first-parent --reverse` và ba phép `merge-base --is-ancestor`; đọc `raw-rest/comments-1111.json`, PR và commit thô. Output đầy đủ: [git-and-claims-output.txt](git-and-claims-output.txt).

**Output thật:** merge `4397ee616273a97c1503e8359452aef4e78cd75a`, tree `e92592f8f3b4523ac2787b60439b73ad520ecf20`; cha `c6dd7b33b4f215809bf281ee1533bc1e8fa6920c`, `f783bee391ada131df8df195acfd3d4c4ae394c9`, đúng REST. Diff so cha đầu: YAML `+39/-14`, manifest `+1/-0`, `gate-output-41173244891.txt +474/-0`, đúng ba phần tử bản trích. `diff.patch` và `numstat.txt` khớp byte với diff thật so merge-base `3bdd9877cab2543adc413a32a47decbb585ded97`; `core.abbrev=7`.

| Lời khai | Nguồn đo độc lập | Khớp/lệch |
|---|---|---|
| #1111 merge 2026-11-01T07:43:08Z; merge/head full SHA dòng 87–88 | `raw-rest/pull-1111.json` + Git parents/tree | KHỚP |
| Head `f783bee…` đúng comment chốt | Comment `6555093642`, created/updated `2026-11-01T07:43:02Z`, nguyên văn đủ 40 hex; head commit `07:03:13Z` trước comment, merge `07:43:08Z` sau comment | KHỚP; giữ caveat #566 về tác giả vận chuyển |
| Hai cha `c6dd7b3`, `f783bee`; chỉ hồ sơ + provenance | `git show -s` và `git diff --numstat 4397ee6^1 4397ee6` | KHỚP |
| `4397ee6` là tổ tiên của `3bdd987`, rồi `180039c` | Hai lệnh `merge-base --is-ancestor`, đều rc 0 | KHỚP; không suy thành cùng cây |
| Đúng ba PR #1108/#1112/#1109 giữa `4397ee6` và `3bdd987` | First-parent: `165b27a` (#1108), `2cea625` (#1112), `3bdd987` (#1109) | KHỚP |
| Ba PR chỉ thêm spec/ops | #1108: `ops/specs/DIEU-KIEN-MERGE-CONG-r1.md +140/-0`; #1112: `launcher-sandbox-lay-mau-r1.md +225/-0`, `…-r2.md +242/-0`; #1109: `CI-LAN-LUU-TRU-r1.md +218/-0` | KHỚP, chính xác hơn là bốn tệp mới dưới `ops/specs/` |
| Không đụng hồ sơ này hay `ops/vm/` | `git diff --name-status 4397ee6 3bdd987 -- ops/vm/ ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml` | KHỚP: output rỗng |
| #1118 là PR bổ sung trên nhánh `ccr-5249948c-9epnbs` | `raw-rest/pull-1118.json`: number 1118, đúng branch/head reviewed SHA, state open, draft true, merged false | KHỚP; dòng bookkeeping không khai #1118 đã merge |

**Kết luận: KHÔNG PHẢI LỖI.** Các quan hệ Git và phạm vi thay đổi đều đúng. Chúng không chứng minh thứ tự run thành công hay checkout thật trong một job.

## Hướng 4 — Đo lại thứ tự run và nguyên nhân huỷ

**Giả thuyết:** “run kế tiếp đã chạy trọn” và nguyên nhân “bị thay thế bởi push #1108/#1112/#1109” không được dữ liệu thô chứng minh.

**Lệnh:** script `audit_git_and_claims.py`, mục `MASTER RUN TIMELINE`, đọc các phần tử liên quan trong `raw-rest/runs-master-push.json`; đối chiếu run thô và workflow tại `4397ee6:.github/workflows/ci.yml`. Không gọi API mới. Danh sách thô chỉ có 30 run gần nhất trên tổng 1005; cả bốn run cần so dưới đây đều có mặt, nên phản chứng không cần suy toàn bộ lịch sử.

**Output thật (UTC, attempt 1):**

| Run / head | Event / workflow | Kết quả | created_at → updated_at |
|---|---|---|---|
| 41285898441 / 4397ee6 (#1111) | push / `.github/workflows/ci.yml` | completed/cancelled | 07:43:11Z → 09:07:12Z |
| **41287486328 / 165b27a (#1108)** | push / `.github/workflows/ci.yml` | **completed/success** | **09:07:11Z → 09:23:36Z** |
| 41289716885 / 2cea625 (#1112) | push / `.github/workflows/ci.yml` | completed/cancelled | 09:38:32Z → 09:42:55Z |
| 41290009265 / 3bdd987 (#1109) | push / `.github/workflows/ci.yml` | completed/success | 09:42:53Z → 10:22:24Z |

Workflow Git ghi `group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}` và `cancel-in-progress: ${{ github.ref != 'refs/heads/master' }}`. Hai JSON run/jobs chỉ có trạng thái huỷ và danh sách job rỗng, không có trường lý do/actor huỷ. `actor`/`triggering_actor` là actor của run, không là biên nhận thao tác huỷ; `cancel_url` là URL thao tác, không phải bằng chứng thao tác đã gọi.

**Kết luận: LỖI**, gồm hai finding riêng: lời khai thứ tự sai đo được và nguyên nhân chưa được đo.

### bo-sot-run-thanh-cong-ke-tiep  [P1]

**TỆP/DÒNG:** `ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:206` (cụm “Run ke tiep da chay tron la 41290009265”).

**VẤN ĐỀ:** Run `41287486328` trên `165b27a` (#1108) đã completed/success trước run `41290009265`. Vì vậy số run được gọi là “kế tiếp” sai, dù kết quả success của `41290009265` tự nó đúng. Lịch sử bị ghi thành một bước thay thế liên tục, làm mất một run thành công ở giữa.

**ĐÃ THỬ NGHIỆM:** Đọc và sắp theo `created_at` bốn phần tử trong danh sách REST thô; `41287486328` tạo 09:07:11Z, kết thúc 09:23:36Z, trong khi `41290009265` tạo 09:42:53Z. Git xác nhận `165b27a` là merge #1108 ngay sau `4397ee6`.

**ĐỘ TIN:** Cao — phản chứng dương nằm trong snapshot, không suy từ list thiếu/rỗng.

**Gợi ý vá:** Sửa đúng đoạn hậu merge mới, đổi thành “một run thành công sau đó” nếu vẫn chọn `41290009265`, đồng thời ghi nhận run #1108 đã success ở mức REST; không bắt buộc đổi run được chọn để dẫn chứng. Phép khoá là bảng thứ tự trên; câu “kế tiếp” cũ phải bị bác bởi phần tử `41287486328`. Nguy cơ khi vá: đừng nâng run bị bỏ sót thành “đã đo đủ 23/23/checkout” vì snapshot chỉ có metadata tổng hợp của nó, chưa có jobs/logs.

### nguyen-nhan-huy-chua-duoc-do  [P2]

**TỆP/DÒNG:** `ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:205–206`.

**VẤN ĐỀ:** Dữ liệu đo chỉ chứng minh cancelled và 0 job. Câu `measured` lại khẳng định bị thay thế do push của ba PR. Thời điểm run #1108 xuất hiện sát lúc huỷ phù hợp giả thuyết bị thay thế khi chờ, nhưng chưa là biên nhận nguyên nhân; hai run #1112/#1109 còn được tạo muộn hơn lúc run #1111 đã huỷ. Hồ sơ không tách suy luận khỏi phép đo.

**ĐÃ THỬ NGHIỆM:** Kiểm toàn bộ hai JSON run/jobs và so bốn mốc REST trong bảng; đọc concurrency của workflow đúng commit. `cancel-in-progress=false` trên master không tự chứng minh không thể thay một lượt đang chờ, nên finding này KHÔNG khẳng định huỷ tự động là bất khả thi. Snapshot thiếu lý do huỷ, không cho phép chốt một nguyên nhân chắc chắn.

**ĐỘ TIN:** Cao về khoảng trống bằng chứng; nguyên nhân thực tế KHÔNG ĐO ĐƯỢC.

**Gợi ý vá:** Giữ nguyên cancelled/0 job và “không có test thất bại được quan sát”, ghi nguyên nhân `not_measured`, hoặc gắn nhãn rõ đây là suy luận về lượt chờ. Phép khoá: chỉ từ `conclusion=cancelled` + `jobs=[]` không được sinh kết luận nguyên nhân; phải có biên nhận nguyên nhân nếu muốn giữ nhãn measured. Nguy cơ khi vá: đừng biến “không có job” thành gate pass, cũng đừng gọi huỷ là test failed.

## Hướng 5 — Phạm vi phép đo CI, tách run head khỏi checkout thật

**Giả thuyết:** câu “Run này đo CÂY 3bdd987” nâng REST run head thành checkout/tree thực thi khi chưa có đủ mốc.

**Lệnh:** `audit_git_and_claims.py`, các mục `SOURCE TIME ANOMALY` và `EXISTING FOUR ANCHORS`; đối chiếu §10.2.2/§10.2.3/§13.1 với hai bản trích run/jobs mới và danh sách tệp provenance. Đọc `raw-rest/jobs-41290009265.json` cả run_id, attempt, steps, started_at/completed_at, không chỉ trường bản trích giữ lại.

**Output thật:**

| Lời khai/đối tượng | Nguồn | Khớp/lệch và giới hạn |
|---|---|---|
| Run 41285898441: ID, gate/ci.yml, event push, attempt 1, head 4397ee6, completed/cancelled | REST thô của đúng run + bản trích | KHỚP tất cả; không có job để kiểm checkout/output |
| Giờ run huỷ 2026-11-01T07:43:11Z → 09:07:12Z và node_id `WFR_kwLOTNeRjc8AAAAJnNTQyQ` | Hai bản run thô/trích | KHỚP; giờ này là created_at/updated_at, không gọi là giờ test |
| Run 41290009265: ID, gate/ci.yml, push, attempt 1, head 3bdd987, completed/success | REST thô của đúng run + bản trích | KHỚP metadata Run |
| Giờ run thành công 2026-11-01T09:42:53Z → 10:22:24Z và node_id `WFR_kwLOTNeRjc8AAAAJnROKsQ` | Hai bản run thô/trích | KHỚP phép trích; không đồng nghĩa giờ thực thi mọi job |
| 23 job/23 success, ubuntu-latest, runner_id khác 0 | `raw-rest/jobs-41290009265.json`, đủ một trang: 23 trả về = total_count 23, ID/tập/thứ tự khớp | KHỚP; 275 step success, 10 skipped được giữ riêng, không gọi tất cả step là pass |
| Job thuộc run/attempt đã chọn | Toàn bộ 23 trường `run_id=41290009265`, `run_attempt=1` trong REST thô | KHỚP |
| “Run này đo CÂY 3bdd987” | Chỉ REST `head_sha`, jobs metadata; không có log/artifact checkout, GraphQL WorkflowRun.file hay output của run này | **KHAI RỘNG**; thiếu ba mốc độc lập |
| Các giờ trong nguồn run và jobs tự nhất quán | Run created_at/run_started_at đều 09:42:53Z; 22/23 job bắt đầu trước đó, 15/23 job hoàn tất trước đó; sớm nhất 09:23:37Z | **LỆCH TRONG NGUỒN**, nguyên nhân KHÔNG ĐO ĐƯỢC; không quy tội bản trích sửa giờ vì chúng không giữ các giờ job |
| CI Ubuntu không chứng minh Windows | Labels của 23 job; YAML giữ “Chỉ Ubuntu” | KHỚP, nhãn phạm vi đúng |

**Kết luận: LỖI** ở mức khẳng định checkout/tree. Bất nhất giờ của nguồn được ghi nguyên trạng như một giới hạn bổ sung, không tự kết luận job giả, SHA sai hoặc đã biết nguyên nhân. Không thể giải quyết bất nhất này bằng gọi mạng trong phạm vi review được giao.

### run-head-khong-chung-minh-cay-thuc-chay  [P2]

**TỆP/DÒNG:** `ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:208–209` (cụm “Run nay do CAY 3bdd987”).

**VẤN ĐỀ:** Bằng chứng mới chỉ đo Run và metadata jobs. §10.2.2 cấm đồng nhất REST `head_sha` với checkout/tree hoặc workflow-definition SHA. Không có log/artifact in checkout SHA/parents/tree, definition identity của đúng run/attempt, hay command/rc/marker dương của run `41290009265`. Việc `4397ee6` là tổ tiên và `ops/vm/` không đổi chỉ chứng minh quan hệ hai commit và bytes trong Git; nó không chứng minh bytes thực thi trên runner. Vì vậy câu đã viết mạnh hơn phép đo, dù chọn descendant thay vì gọi trực tiếp là test `4397ee6` là cách phân biệt đúng một phần.

**ĐÃ THỬ NGHIỆM:** Kiểm đủ trường trong run/jobs thô, file mới và các tệp provenance có tên run này: chỉ `readback-run-41290009265.json`, `readback-jobs-41290009265.json`. Metadata không chứa output checkout/tree/command. Nguồn còn có bất nhất giờ nêu trên. Đối chứng dương: hồ sơ cũ cho run **41173244891** có GraphQL WorkflowRun.file + blob workflow khớp Git và log trích của đúng run, nên không mượn evidence run cũ để lấp run mới.

**ĐỘ TIN:** Cao về việc thiếu mốc và câu khai quá rộng; checkout thực tế của run mới KHÔNG ĐO ĐƯỢC từ snapshot.

**Gợi ý vá:** Sửa ngay đoạn mới thành “REST run/jobs head_sha là 3bdd987; chỉ đo metadata Run, chưa đo Checkout/Workflow definition/Gate output của run này”. Hoặc thu đủ ba mốc còn thiếu từ đúng run/attempt rồi mới giữ lời khai cây thực chạy. Phép khoá là tách hai nguồn bằng chứng: đổi/mất checkout log mà metadata head vẫn giữ nguyên phải khiến kết luận cây thực thi trở thành not_measured. Nguy cơ khi vá: không hạ/viết lại kết quả lịch sử của run 41173244891, không nâng 23 job success thành mọi bước đã chạy, và không đòi đo Windows từ 23 label Ubuntu.

## Hướng 6 — VM Windows: băm nguồn đo được, trạng thái máy không đo được

**Giả thuyết:** đoạn VM dùng nhãn thuat_lai để che một SHA/băm nguồn sai, hoặc biến quan sát lịch sử thành kiểm chứng hiện tại trên VM.

**Lệnh:** `git show cb39aca:<path>` đưa bytes vào `hashlib.sha256`, so với cùng path ở `40609d4`; `git merge-base --is-ancestor cb39aca 40609d4`; đọc lịch trong script và ghi chú ACL ở `Register-LichCapNhat`. Các phép đo nằm trong `audit_git_and_claims.py`, rc 0. Nguồn của hai tệp cài kèm lần lượt là `ops/cong_cu.yaml`, `requirements.txt` tại gốc kho, không phải tệp dưới `ops/vm/`.

| Lời khai trong dòng 221–230 | Nguồn/phép đo | Khớp/lệch |
|---|---|---|
| Bản sửa thuộc PR #1091, merge `40609d4` | Git merge message và parents của `40609d4269c8858fc51002687ce035086bbda38e` | KHỚP |
| `cb39aca` là bản của nhánh #1091 | Full OID `cb39acab37224f8a9f37a6ec9f63600bb7943874` là tổ tiên merge #1091, rc 0 | KHỚP; không nhầm đó là head cuối của PR |
| Script có prefix `8EFC063A…` | `cb39aca:ops/vm/cap-nhat-cong-cu.ps1` SHA-256 `8efc063a891916598e398f7e448c295c8a37e12cc1dace5534f1fbcfd26ba927`; cùng bytes ở merge #1091 | KHỚP băm nguồn |
| `cong_cu.yaml` prefix `71631BB6…` | `cb39aca:ops/cong_cu.yaml` SHA-256 `71631bb6baf532deeb4847c5ff9c407a50bfdb4fc503621913eb42c719ee92fb`; cùng bytes ở merge #1091 | KHỚP băm nguồn |
| `requirements.txt` prefix `97733A88…` | `cb39aca:requirements.txt` SHA-256 `97733a880d95f8a900f39af2bcd1a59a3ecb357dfc928c01c7a06636b1b07657`; cùng bytes ở merge #1091 | KHỚP băm nguồn |
| Chủ nhật 02:30, hai tuần/lần | Script có `New-ScheduledTaskTrigger -Weekly -WeeksInterval 2 -DaysOfWeek Sunday -At '02:30'` | KHỚP cấu hình mã; lịch thực tế trên VM chưa đo |
| Lỗi rc=6 sau #1069 do `/T` và DACL rỗng; đăng ký lại trên nhánh #1091 rc=0 | Lịch sử sửa code/ghi chú xác nhận loại bản sửa; không có output Windows độc lập | KHÔNG ĐO ĐƯỢC hai rc và diễn biến thực tế; được khai thuat_lai |
| Cũ 31-10, bản 6733d09, rc=0, giờ VM 11:32, HeThong 4/4 và NguoiDung 11/11 | Không có log VM trong snapshot; đoạn mới đánh dấu rõ `(Cu, 31-10)` | KHÔNG ĐO ĐƯỢC quan sát VM; không gọi là trạng thái hiện tại |
| Bản cài `C:\Program Files\tra-luat-ops` khớp ba băm, ACL thừa kế Users RX/Administrators F/SYSTEM F | Chỉ có lời kể, không có bytes/ACL readback từ VM | KHÔNG ĐO ĐƯỢC trên máy; băm nguồn đúng không chứng minh băm bản cài |
| NguoiDung LastTaskResult 0, 11/11 “giu”, log `NguoiDung-20261101-070043.json` | Log không nằm trong kho, YAML nói thẳng điều đó | KHÔNG ĐO ĐƯỢC; không suy thời điểm/OS từ tên log |
| HeThong chưa chạy tay với bản mới | Không có evidence VM; nhãn thuat_lai và câu CHUA rõ ràng | KHÔNG ĐO ĐƯỢC; không bị nâng thành đã chạy |
| Node 24.22.1 → 26.13.0, Commander Offline đến reboot, quyết định giữ Node 26 | Lời kể giữ từ hồ sơ trước, không có log/máy thật | KHÔNG ĐO ĐƯỢC, không cấp tín dụng measured |

**Kết luận: KHÔNG PHẢI LỖI về SHA/băm nguồn và nhãn. KHÔNG ĐO ĐƯỢC trạng thái vận hành VM.** `trang_thai: thuat_lai` và câu “Moi so lieu trong doan nay la thuat_lai … khong luu tep trong kho” phủ rõ các quan sát VM. Không có cơ sở biến việc không đo được máy thành finding về sự thật của lời kể. Đoạn mới đã bỏ câu cũ “CHUA cap nhat len b0814f4” và đánh dấu lịch sử/cập nhật, nên không còn giữ hai trạng thái bản cài đối nhau.

## Hướng 7 — Header, trạng thái landed và phần hồ sơ cũ có còn tự mâu thuẫn không

**Giả thuyết:** phần bổ sung vô tình đổi mốc landed sang #1118, coi comment cũ là duyệt head mới, hoặc để header/nợ cũ mâu thuẫn với nội dung mới.

**Lệnh:** đọc toàn bộ YAML với số dòng, so diff gốc; đọc khuôn `pr870-claude-md-bai-hoc-c-land-evidence.yaml` và `pr759-no-p3-ho-so-land-evidence.yaml`; đối chiếu §7, §10.2.2, §10.2.4, §13.1; kiểm bytes workflow, GraphQL và log trích cũ bằng `audit_git_and_claims.py`; tìm đăng ký test VM trong `.github/workflows/` và `.claude/dev/ci_dang_ky_test.py` bằng `rg`.

| Lời khai/header/trạng thái | Nguồn | Khớp/lệch và phạm vi |
|---|---|---|
| Header hồ sơ PR #1065, lịch hai tuần/lần, merged 3dfb973 | `readback-pr-1065.json`, Git merge 3dfb973; script lịch | KHỚP đối tượng và lịch cấu hình |
| “Không phải packet”, không có Issue/lease/spec_hash | Phạm vi giao trực tiếp trong prompt và khai báo YAML `packet_issue: null`, `packet_id: KHONG_AP_DUNG` | Nhất quán phạm vi; không dùng phép tìm thiếu tệp để chứng minh chưa từng có authority ngoài snapshot |
| Schema tham chiếu §7/§13.1, khuôn pr870 | Các tệp và mục tham chiếu tồn tại, dùng cấu trúc merge/checks/bookkeeping và caveat như khuôn | KHỚP |
| Header `landed: true` và bốn mốc của run **41173244891** | Run cũ completed/success; GraphQL databaseId 41173244891/file URL đúng OID 3dfb973; workflow blob `82d9f239ff311bd1ba3d3021119b5a2f7f699ffc`, SHA-256 `ce9a3ec0f777a5165477c73b8fc9b9c098e8c3a9f5517c7499649670e84913fb`, bytes khớp Git; log trích 23 job, 22 checkout cùng SHA, 122 bước Run; jobs 275 success/10 skipped | KHỚP nội dung các hiện vật cũ; không phải evidence cho run 41290009265 |
| Header assurance trên **bản vá 210ab81** (#1069), bản merge b0814f4 từng changes_requested/P0 | Phần `ASSURANCE-REVIEWER-81` và danh sách review bên dưới phân biệt bản gốc/bản vá; bổ sung không thay đổi đối tượng review | Nhất quán cách phân biệt; không nâng connector sạch thành review đúng mức |
| Nhãn measured/thuat_lai/not_measured và phân loại nguồn header | Header ghi measured là đo từ tệp, sáu JSON mới được gọi rõ BAN TRICH, VM được gọi thuat_lai | KHỚP cách khai loại tệp; không có lỗi gọi sáu bản trích là thô |
| Header nói phần lớn REST tải 31-10, các ngoại lệ mới ngày 01-11 | Các bản trích mới tách riêng đúng ngày; `gate-output-41173244891.txt` tự khai là trích log ngày 01-11 | Không đọc “phần lớn” thành “mọi tệp”. Phương thức/giờ tải lịch sử cũ không được reviewer tái đo; không tự cấp chứng nhận thao tác curl |
| Header TRANG THAI còn đúng không | Header hiện đã `landed: true`, merged 3dfb973; nội dung landed true và comment chốt #1111 khớp | Không có header “chờ chủ kho” cũ cần sửa ở hồ sơ này |
| `landed_hieu_luc_tu` cùng trường mới `_do_duoc` | Trường mới pin #1111/4397ee6; comment 6555093642 pin f783bee, trước merge; bookkeeping phân biệt #1111 và #1118 | Đọc cùng nhau nhất quán: mốc lịch sử là 4397ee6; không tự dời sang merge #1118 tương lai |
| Quy tắc comment head cuối và caveat #566 | Raw comment có đủ 40 hex, tự nói agent đăng hộ, không phải owner tự gõ | KHỚP; không biến thành human_audited hay quyền duyệt b13d3ef |
| `post_merge_checks` và `bookkeeping` là list đủ nội dung, không CHO_DIEN | Cổng riêng L6 ĐẠT; các tệp nguồn và PR xác minh ở các hướng trước | KHỚP cấu trúc. Thêm mục #1118 không khai PR này đã merge hoặc được duyệt |
| Nợ `TEST-OPS-VM-CHUA-NOI-CI` | Không có đăng ký `cap-nhat-cong-cu_test.ps1`/`ops/vm/` trong workflow/registry CI đã tìm | Chưa thấy mâu thuẫn cần sửa: chạy CI khác không tự có nghĩa test VM đã nối CI |
| Nợ `DUYET-CHI-TRONG-PHIEN` và `KHOI-DONG-LAI-COMMANDER-CHUA-DO` | Hồ sơ phân biệt duyệt merge #1065 trước đây với comment chốt landed về sau; trạng thái Commander chỉ có lời kể | Không được tự xoá hai nợ từ bằng chứng mới; quan sát máy thật vẫn KHÔNG ĐO ĐƯỢC |

**Kết luận: KHÔNG PHẢI LỖI** về các điểm nhất quán/historical header đã kiểm. Không phát hiện P3 độc lập cần yêu cầu sửa. Ba finding ở hướng 4–5 là phần phải sửa; cổng nguồn xanh không loại chúng.


## Hướng 8 — Patch gợi ý và kiểm tra kết thúc

**Giả thuyết:** gợi ý không áp được, làm hỏng YAML, hoặc reviewer đã chạm cây được review.

**Lệnh:** tạo `HINT.patch` bằng unified diff với đường dẫn `ops/land/…`, sao riêng một tệp YAML vào `hint-check/` ngoài repo; `patch --dry-run -p0 -d hint-check < HINT.patch`, rồi áp vào bản sao và `yaml.safe_load`; cuối cùng `git -C ../../cay-kho status --porcelain=v1` và `rev-parse HEAD HEAD^{tree}`.

**Output thật:** dry-run `checking file ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`; áp bản sao `patching file …`; cả hai rc 0, không fuzz/reject; `Scratch patched YAML parsed: dict`. Git status cuối output rỗng, HEAD/tree vẫn `b13d3ef93724d249b3db6eeef6d3fe43a61b08f9` / `b0054bf730d8aad494e3fb9ad797585ecd77e836`.

**Kết luận: KHÔNG PHẢI LỖI.** [HINT.patch](HINT.patch) chỉ gợi ý thu hẹp ba lời khai, áp bằng `patch -p0` từ gốc `cay-kho/`; đã kiểm khả năng áp và parse trên bản sao ngoài kho. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Không khai đã chạy gate trên bản vá gợi ý. Không sửa `cay-kho/`, không push, không gọi mạng, không đo VM.

## Quyết định cuối

`changes_requested`: còn **1 P1, 2 P2**, không có P0/P3 độc lập. Sáu bản trích trung thực, toàn bộ băm khớp và cổng nguồn ĐẠT; ba finding nằm ở nội dung diễn giải bằng chứng. Kết luận này chỉ neo vào reviewed SHA ở dòng 2 và các snapshot đã cấp.
