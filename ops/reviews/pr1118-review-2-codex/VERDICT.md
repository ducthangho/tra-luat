verdict: approve
reviewed_sha: 352d31e03bc846cae5b4ee7bc17bbea6830fb64d
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Review độc lập, chỉ đọc và đo trong sandbox; không gọi mạng và không sửa `cay-kho/`.

## Hướng 1 — ĐỐI CHIẾU LƯỢT TRƯỚC

**Giả thuyết:** bản vá chỉ đổi câu chữ, chưa đóng ba finding trên `b13d3ef93724d249b3db6eeef6d3fe43a61b08f9`.

**Lệnh:** sao nguyên hai script `luot1/run/audit_{git_and_claims,readbacks}.py` sang thư mục run này; chạy trên HEAD mới. `audit_git_and_claims_luot1.py` hoàn tất, output ở [recheck-git-luot1.txt](recheck-git-luot1.txt). Script readbacks cũ gặp `ValueError` ở dòng tách `FETCH-LOG.txt`: lượt 2 thêm một dòng ghi giờ không theo định dạng ` -> filename hash`; chưa thể tính lần chạy này là pass. Sẽ sửa riêng parser trong bản sao ngoài kho và đối chiếu thêm nguồn r2.

**Output thật:** HEAD `352d31e03bc846cae5b4ee7bc17bbea6830fb64d`, tree `8d95d1d7baf35a4f3c8d7bc6ceb3995a0f77b3b4`; merge-base `3bdd9877cab2543adc413a32a47decbb585ded97`; diff/numstat khớp snapshot byte-for-byte. Timeline REST vẫn có success `41287486328` (09:07:11Z → 09:23:36Z) trước success `41290009265` (09:42:53Z → 10:22:24Z). Nguồn jobs cũ đếm được 22/23 started_at và 15/23 completed_at trước run.created_at, sớm nhất 09:23:37Z.

| Finding lượt 1 | Đối chiếu trên YAML hiện tại | Phân loại |
|---|---|---|
| `bo-sot-run-thanh-cong-ke-tiep` [P1] | Dòng 210–214 ghi riêng success đầu `41287486328` rồi success kế `41290009265`; giới hạn run đầu ở metadata, không khai có jobs/log | ĐÃ VÁ THẬT về thứ tự; tiếp tục kiểm từng trường bản trích mới |
| `nguyen-nhan-huy-chua-duoc-do` [P2] | Dòng 207–209 ghi nguyên nhân `not_measured`; giả thuyết thay lượt chờ được gắn rõ “Suy luan, KHONG phai phep do”. REST chỉ có cancelled và jobs rỗng | ĐÃ VÁ THẬT |
| `run-head-khong-chung-minh-cay-thuc-chay` [P2] | Dòng 215–218 công khai bất nhất giờ, tách Run khỏi Checkout/Workflow definition/Gate output, ba mốc sau `not_measured`, bỏ khẳng định cây thực chạy | ĐÃ VÁ THẬT về phạm vi phép đo; tiếp tục kiểm nguồn r2 và số đếm |

**Kết luận: KHÔNG PHẢI LỖI** đối với ba biểu hiện cũ đã đối chiếu. Không dùng “đã làm theo HINT” làm bằng chứng. Chưa chốt toàn bộ review vì còn phải kiểm phần trích mới và mọi lời khai trong diff.

Reviewer: Codex/OpenAI qua API, shell cục bộ trong sandbox; context riêng với executor Claude. Không đăng GitHub, không tự khai assurance của một receipt chưa được đo runtime.

## Hướng 2 — Trung thực bản trích, nguồn r2 và tính toàn vẹn

**Giả thuyết:** bản trích mới sai/thiếu job hoặc giờ, và bản cũ không còn đại diện cho nguồn tải lại.

**Lệnh:** `python3 runs/51d6d31f/audit_readbacks_r2.py` (rc 0). Script chỉ đọc repo/raw, ghi TSV ra thư mục run. Đối chiếu mọi trường giữ lại; ánh xạ `merged_by.login`, `head.sha`, `head.ref`, commit parents/tree/files; so tập và thứ tự job ID, kiểm đủ `total_count`, rồi từng trường của từng job. Jobs thành công dùng trực tiếp `raw-rest/jobs-41290009265-r2.json`. So thêm JSON jobs cũ/r2. Kiểm băm nguồn có trong `FETCH-LOG.txt`; dòng ghi chú lượt 2 không có digest được báo riêng, không tính là đã xác minh hash hai nguồn mới.

**Output thật:** `CHECKS 313 KHOP 313 LECH 0` = 304 phép so bản trích + 9 tiền tố băm nguồn. Hai JSON jobs thô cũ/r2 bằng nhau về cấu trúc và giá trị. Script cũ chạy lại nguyên trạng rc 1 đúng lỗi parser đã ghi; script Git cũ rc 0. Output mới: [audit_readbacks_r2.stdout.txt](audit_readbacks_r2.stdout.txt); đầy đủ từng trường/giá trị/nguồn: [readbacks-field-check-r2.tsv](readbacks-field-check-r2.tsv).

| Bản trích | Nguồn thô | Phép so / lệch |
|---|---|---|
| `readback-pr-1111.json` | `pull-1111.json`, 8 trường đã ánh xạ | 8 / 0 |
| `readback-commit-4397ee6.json` | `commit-4397ee6.json`, gồm đủ mảng parents/files | 4 / 0 |
| `readback-run-41285898441.json` | `run-41285898441.json` | 11 / 0 |
| `readback-run-41287486328.json` | `run-41287486328.json` mới | 11 / 0 |
| `readback-run-41290009265.json` | `run-41290009265.json` | 11 / 0 |
| `readback-jobs-41285898441.json` | `jobs-41285898441.json`, total 0, mảng rỗng | 3 / 0 |
| `readback-jobs-41290009265.json` | `jobs-41290009265-r2.json`, đủ 23 ID, 11 trường/job gồm run_id và giờ bắt đầu/kết thúc | 256 / 0 |

**Kết luận: KHÔNG PHẢI LỖI.** Cả bảy bản trích trung thực. Header dòng 16–18 gọi đúng là `BAN TRICH ... khong phai ban tho`, kể cả nguồn mới và hai trường giờ bổ sung; không đánh tráo bản trích thành toàn bộ phản hồi API. Thời điểm tải bản trích không phải thời điểm chụp `raw-rest/`; dấu `~18:40Z` là giờ xấp xỉ, sandbox không có receipt tải bản trích để xác minh chính xác phút đó. Không lấy nó làm bằng chứng kết quả run.

## Hướng 3 — Cổng nguồn, manifest và đúng cây/phạm vi

**Giả thuyết:** HEAD/phạm vi sai, manifest thiếu/hỏng, hoặc cổng không đạt.

**Lệnh:** `git -C cay-kho rev-parse HEAD HEAD^{tree} refs/remotes/origin/master`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho diff --stat 3bdd987 HEAD`; so snapshot diff/numstat bằng script Git. Chạy `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 cay-kho/ops/land_evidence_nguon.py --root cay-kho`, và thêm `--tep ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`. Chạy `sha256sum -c SHA256SUMS.txt` trong thư mục provenance. Tất cả rc 0.

**Output thật:** HEAD/tree như Hướng 1; master snapshot `180039c4b791fba4c89991623151cbb7378fce53`; shallow `false`; `core.abbrev=7`. Diff thật **9 tệp, +471/-4**, chỉ YAML, manifest và **7** bản trích (lượt 1 có 6, lượt 2 thêm run #1108). Snapshot `diff.patch`/`numstat.txt` khớp byte-for-byte. Cổng toàn kho: `75 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 100`, `TỔNG: ĐẠT`; cổng riêng: `1 ĐẠT · 0/0 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1`, `TỔNG: ĐẠT`. Băm **23/23 OK**.

**Kết luận: KHÔNG PHẢI LỖI.** [gate-all.txt](gate-all.txt), [gate-target.txt](gate-target.txt) giữ output thật. Cổng này kiểm nguồn/cấu trúc, không chứng minh các lời khai văn xuôi hoặc đủ bốn mốc CI; các hướng sau kiểm riêng nội dung.

## Hướng 4 — Bảng lời khai merge, SHA và phạm vi ba PR xen giữa

**Giả thuyết:** SHA/cha/tree/phạm vi hoặc comment chốt đã sai; quan hệ tổ tiên bị dùng thay bằng chứng cùng cây.

**Lệnh:** `PYTHONDONTWRITEBYTECODE=1 python3 runs/51d6d31f/audit_claims_r2.py` (rc 0), cùng script Git lượt 1 (rc 0). Dùng `git show`, `git diff --name-status/--numstat`, `git log --first-parent --reverse`, `git merge-base --is-ancestor`; so độc lập với REST PR/commit/comments. [audit_claims_r2.stdout.txt](audit_claims_r2.stdout.txt) và [claims-field-check-r2.tsv](claims-field-check-r2.tsv) giữ **67/67 phép so khớp, 0 lệch**, gồm cả số CI/VM tĩnh ở các hướng sau.

| Lời khai trong diff | Nguồn đo | Khớp/lệch |
|---|---|---|
| Dòng 88: #1111 đã merge 2026-11-01T07:43:08Z | `raw-rest/pull-1111.json`: number 1111, state closed, merged true, merged_at đúng | KHỚP |
| Dòng 89: merge `4397ee616273a97c1503e8359452aef4e78cd75a` | REST PR/commit + Git object | KHỚP |
| Dòng 89: head `f783bee391ada131df8df195acfd3d4c4ae394c9` | REST PR `head.sha`, Git merge parent thứ hai | KHỚP |
| Head đúng comment chốt | `comments-1111.json` ID 6555093642 chứa đủ 40 hex; head commit 07:03:13Z < comment 07:43:02Z < merge 07:43:08Z | KHỚP; caveat về actor vận chuyển vẫn giữ |
| Dòng 90: hai cha `c6dd7b3`, `f783bee` | Git `%P` và REST: `c6dd7b33b4f215809bf281ee1533bc1e8fa6920c`, `f783bee391ada131df8df195acfd3d4c4ae394c9`; tree `e92592f8f3b4523ac2787b60439b73ad520ecf20` khớp | KHỚP |
| #1111 chỉ đổi YAML + provenance | Diff so cha đầu: YAML +39/-14, SHA256SUMS +1/-0, gate-output +474/-0; đúng ba phần tử REST commit | KHỚP |
| Dòng 211: `4397ee6` là tổ tiên `165b27a` | `merge-base --is-ancestor`, rc 0 | KHỚP |
| `4397ee6` ⊂ `3bdd987` ⊂ `180039c` | Hai lệnh tổ tiên đều rc 0 | KHỚP quan hệ, không suy cùng tree |
| Dòng 218: đúng ba PR #1108/#1112/#1109 | First-parent chỉ có `165b27a`, `2cea625`, `3bdd987`, subject tương ứng cả ba PR | KHỚP |
| Dòng 218–219: chỉ thêm bốn tệp `ops/specs/` | #1108: `DIEU-KIEN-MERGE-CONG-r1.md` +140; #1112: `launcher-sandbox-lay-mau-r1.md` +225, `…-r2.md` +242; #1109: `CI-LAN-LUU-TRU-r1.md` +218; mọi deletion 0 và status A | KHỚP từng số hạng |
| Không đụng YAML này hoặc `ops/vm/` | Diff đúng hai phạm vi giữa `4397ee6` và `3bdd987` rỗng | KHỚP |
| Dòng 256: PR bổ sung #1118, nhánh `ccr-5249948c-9epnbs` | `raw-rest/pull-1118.json`: number/branch đúng, open/draft/unmerged; snapshot này còn neo head lượt 1 `b13d3ef…` | KHỚP định danh; không dùng snapshot cũ chứng minh head live |

**Kết luận: KHÔNG PHẢI LỖI.** `reviewed_sha` lấy từ Git HEAD được giao và kiểm với prompt, không lấy head cũ của REST PR #1118. Hồ sơ không khai #1118 đã merge. Không gọi mạng để làm mới snapshot.

## Hướng 5 — Bảng lời khai Run/jobs/giờ và giới hạn phép đo

**Giả thuyết:** số/giờ mới sai, vẫn bỏ sót success ở giữa, hoặc lời khai rộng hơn dữ liệu REST.

**Lệnh:** hai script đo nêu trên; bản trích jobs so nguồn r2 từng trường. Đọc `raw-rest/runs-master-push.json` trong cửa sổ chứa đủ bốn ID; kiểm concurrency tại `4397ee6:.github/workflows/ci.yml`. Snapshot danh sách có 30 phần tử/tổng 1005, không dùng nó khẳng định toàn bộ lịch sử ngoài cửa sổ đã cấp.

| Lời khai trong diff | Nguồn đo | Khớp/lệch |
|---|---|---|
| Dòng 201–206: run 41285898441, push master, ci.yml, REST head 4397ee6, attempt 1, completed/cancelled | `run-41285898441.json`: repo `ducthangho/tra-luat`, event push, path `.github/workflows/ci.yml`, branch master, full SHA khớp Git | KHỚP |
| created 07:43:11Z, updated 09:07:12Z (01-11) | Hai trường cùng tên trong run thô | KHỚP |
| total_count 0; không job/test thất bại được ghi nhận | `jobs-41285898441.json`: `total_count=0`, `jobs=[]`; không chuyển danh sách rỗng thành pass | KHỚP phạm vi quan sát |
| Nguyên nhân huỷ `not_measured` | Run/jobs không có biên nhận lý do huỷ; actor của run không chứng minh actor huỷ | KHỚP nhãn; nguyên nhân thực tế KHÔNG ĐO ĐƯỢC |
| Run #1108 tạo một giây trước updated_at của run huỷ | 09:07:11Z so 09:07:12Z | KHỚP phép trừ; câu thay lượt chờ chỉ là suy luận đã gắn nhãn |
| Dòng 210–212: run 41287486328, head 165b27a, #1108, push, attempt 1, completed/success, 09:07:11Z → 09:23:36Z | `run-41287486328.json` mới + Git subject merge #1108 | KHỚP mọi trường |
| Đây là success đầu, 41290009265 là success kế | Danh sách run theo created_at: 41285898441 cancelled → 41287486328 success → 41289716885 cancelled → 41290009265 success | KHỚP; run bị huỷ ở giữa không phá thứ tự hai success |
| Không tải jobs/log #1108, chỉ metadata Run | Không có hiện vật jobs/log run 41287486328 trong provenance/raw được cấp | KHỚP giới hạn; không suy runner hay checkout của run này |
| Dòng 213–214: 41290009265, push, REST head 3bdd987, #1109, attempt 1, completed/success | Run thô + Git merge subject; created 09:42:53Z, updated 10:22:24Z | KHỚP |
| 23 job, 23 success | Jobs r2: total_count=23, đúng 23 ID khác nhau, 23 conclusion success | KHỚP từng số hạng |
| 23 nhãn ubuntu-latest, mọi runner_id khác 0 | Jobs r2: 23/23 labels đúng `['ubuntu-latest']`, 23/23 runner_id khác 0; run_id/attempt/head từng job khớp run metadata | KHỚP; “Chỉ Ubuntu” là phạm vi 23 job đã đo, không chứng nhận OS run #1108 |
| Dòng 215: 22/23 started_at trước created_at của run; sớm nhất 09:23:37Z | So từng job r2 với `2026-11-01T09:42:53Z` | KHỚP: 22/23, min đúng |
| Dòng 216: 15/23 completed_at cũng sớm hơn | So từng trường completed_at của jobs r2 với cùng created_at | KHỚP: 15/23 |
| Bất nhất giờ nằm ngay trong REST, nguyên nhân chưa đo | Jobs cũ và r2 cùng giá trị; bản trích giữ nguyên cả run_id, head và giờ | KHỚP; không tự sửa giờ hoặc đoán lỗi hệ thống |
| Dòng 217–218: hai success chỉ có mốc Run; ba mốc khác not_measured; không khẳng định cây thực chạy | Hiện vật mới chỉ PR/commit/run/jobs REST; không có checkout log, WorkflowRun.file hoặc output gate cho hai run đó | KHỚP, đúng §10.2.2 |

**Output bổ sung:** concurrency có group workflow/ref và `cancel-in-progress: ${{ github.ref != 'refs/heads/master' }}`. Không lấy cấu hình ấy làm receipt chứng minh nguyên nhân cụ thể. `updated_at` vẫn được gọi đúng tên trường; không nâng thành thời điểm kết thúc job. Các mốc thiếu được khai thiếu, không bị lấp bằng quan hệ tổ tiên hay việc ba PR chỉ thêm spec.

**Kết luận: KHÔNG PHẢI LỖI.** Các số mới đều tái đo đúng; ba finding cũ đã đóng sau khi kiểm cả nguồn r2, không sinh biểu hiện mới cùng lớp trong phạm vi đã rà.

## Hướng 6 — VM sau #1091: tách dữ kiện tĩnh khỏi máy thật

**Giả thuyết:** cập nhật VM sai SHA/băm/lịch so với Git, hoặc kể việc chưa đo thành `measured`.

**Lệnh:** `audit_claims_r2.py` dùng `git show cb39aca:<path>`, SHA-256 bytes, đối chiếu cùng ba tệp ở `40609d4`; `git show -s --format='%H %P %s' 40609d4 cb39aca`; đọc `van_hanh_tren_vm` và mã đăng ký lịch, cùng receipt/verdict #1091. Script rc 0.

| Lời khai trong phần thay thế dòng 231–240 | Nguồn có thể kiểm | Khớp/lệch |
|---|---|---|
| (Cũ, 31-10) bản 6733d09, đăng ký rc=0, 11:32 giờ VM, HeThong 4/4, NguoiDung 11/11 | Chỉ lời kể VM, không có log gốc trong snapshot | KHÔNG ĐO ĐƯỢC; đã gắn `thuat_lai`, giữ rõ mốc cũ |
| Sau #1069 đăng ký rc=6 do DACL rỗng; sửa trong #1091 | Git #1091 có phần reset ACL trước chép; verdict #1091 ghi đúng vấn đề sửa. Sự cố native cụ thể/rc=6 trên máy thật chỉ là lời kể | KHỚP bối cảnh mã; kết quả native KHÔNG ĐO ĐƯỢC |
| #1091 merge `40609d4` | Git commit `40609d4269c8858fc51002687ce035086bbda38e`, cha hai `90b3f1cd9ff8a3459285796da37dc96b8553690e`, subject #1091; receipt lượt 2 approve đúng head đó | KHỚP |
| Bản `cb39aca` thuộc nhánh #1091 | Git tổ tiên cb39aca → 40609d4 rc 0 | KHỚP; không đồng nhất cb39aca với head merge |
| Script băm `8EFC063A…` | Bytes `cb39aca:ops/vm/cap-nhat-cong-cu.ps1`: `8efc063a891916598e398f7e448c295c8a37e12cc1dace5534f1fbcfd26ba927` | KHỚP tiền tố |
| `cong_cu.yaml` băm `71631BB6…` | `cb39aca:ops/cong_cu.yaml`: `71631bb6baf532deeb4847c5ff9c407a50bfdb4fc503621913eb42c719ee92fb` | KHỚP tiền tố |
| `requirements.txt` băm `97733A88…` | `cb39aca:requirements.txt`: `97733a880d95f8a900f39af2bcd1a59a3ecb357dfc928c01c7a06636b1b07657` | KHỚP tiền tố |
| Ba tệp tĩnh này phù hợp bản sửa đã merge | Mỗi tệp so byte cb39aca với 40609d4 đều bằng nhau | KHỚP tệp Git; không chứng minh bytes đang cài trên VM |
| Máy cài tại `C:\Program Files\tra-luat-ops` nay khớp ba băm; đăng ký lại rc=0 | Không có VM hoặc installed bytes để đọc | KHÔNG ĐO ĐƯỢC; câu nằm trong khối `thuat_lai` |
| ACL kế thừa Users RX, Administrators F, SYSTEM F | Không có Get-Acl/native NTFS readback được cấp | KHÔNG ĐO ĐƯỢC; không nhận kiểm mã tĩnh thay kết quả ACL |
| NguoiDung LastTaskResult 0, 11/11 “giu”, log `NguoiDung-20261101-070043.json` | Log chỉ trên VM; không có trong provenance/raw | KHÔNG ĐO ĐƯỢC; nhãn trung thực |
| HeThong CHƯA chạy tay bản mới | Lời kể phiên VM | KHÔNG ĐO ĐƯỢC; không được coi là pass bản mới |
| Lịch Chủ nhật 02:30, hai tuần/lần | Mã cb39aca: `New-ScheduledTaskTrigger -Weekly -WeeksInterval 2 -DaysOfWeek Sunday -At '02:30'` | KHỚP cấu hình mã; lịch thực cài trên VM chưa đo |
| Node 24.22.1 → 26.13.0, Commander Offline, reboot VM, chủ kho giữ Node 26 | Không có log VM trong bundle | KHÔNG ĐO ĐƯỢC; câu sự cố cũ vẫn thuộc cùng khối `thuat_lai` |
| “Mọi số liệu trong đoạn này là thuat_lai”, không lưu tệp trong kho | YAML `trang_thai: thuat_lai`; kiểm danh sách provenance | KHỚP nhãn và giới hạn nguồn |

**Kết luận: KHÔNG PHẢI LỖI** về nhãn, SHA/băm/lịch tĩnh và phạm vi lời khai. **KHÔNG ĐO ĐƯỢC** mọi hành vi VM Windows thật. Việc không có VM không tự là finding vì hồ sơ không nhận phần này là phép đo độc lập. Không nâng các tỷ lệ tác vụ hoặc ACL thành kết quả reviewer đã xác minh.

## Hướng 7 — Header và phần hồ sơ cũ có tự mâu thuẫn không

**Giả thuyết:** header/trạng thái vẫn kể sai landed, áp approval cũ sang head mới, hoặc dùng CI mới thay bốn mốc cũ.

**Lệnh:** đọc toàn bộ YAML 256 dòng; so AST với YAML tại merge-base; kiểm legacy bằng Python đọc JSON/YAML, băm verdict theo receipt, đối chiếu Git, giải mã workflow contents, đếm checkout/log/output và đọc ba khuôn pr721/pr759/pr870. Output kiểm legacy (rc 0) ở [legacy-consistency.txt](legacy-consistency.txt).

**Output thật:** AST chỉ thêm `trang_thai_packet.landed_hieu_luc_tu_do_duoc`, thêm một phần tử mỗi list `post_merge_checks`/`bookkeeping`, đổi `van_hanh_tren_vm.mo_ta`; không lén đổi nhãn/trạng thái cũ. `landed` vẫn bool true; nhãn post-merge `[measured, measured, thuat_lai]`, nhãn VM `thuat_lai`.

| Điểm cần rà, kể cả câu cũ | Nguồn/đối chiếu | Kết quả |
|---|---|---|
| Header `TRANG THAI: merged (3dfb973), landed: true` | REST cũ PR1065/Git đúng merge `3dfb9731ceda05afbcec4e803a919c4df5e2e5a2`; PR1111 đã merge mang landed=true; nguồn bổ sung chỉ rõ mốc 4397ee6 | KHÔNG PHẢI LỖI; không còn câu “chờ chủ kho” trái trạng thái ở hồ sơ này |
| Header nói bốn mốc run **41173244891**, không phải hai run mới | Run cũ push/ci.yml/attempt1, completed/success, 05:36:00Z → 07:03:35Z ngày 31-10; jobs 23/23 success, 23 Ubuntu, 23 runner khác 0; log có 23 job/22 checkout đúng full SHA/122 buớc Run/0 error; kết luận steps 275 success, 10 skipped giữ riêng | KHÔNG PHẢI LỖI trong phạm vi hiện vật giữ lại; không nhầm sang 41290009265 |
| Mốc Workflow definition cũ | GraphQL node databaseId 41173244891, file URL chứa exact 3dfb973, checkSuite cùng OID; Contents blob `82d9f239ff311bd1ba3d3021119b5a2f7f699ffc`, bytes khớp Git, SHA-256 `ce9a3ec0f777a5165477c73b8fc9b9c098e8c3a9f5517c7499649670e84913fb` | KHÔNG PHẢI LỖI; log/GraphQL gốc của run mới không được suy từ nguồn cũ |
| Header assurance trên **bản vá 210ab81**, bản merge b0814f4 từng có 1 P0 | Receipt lượt 16 approve/cross_approved đúng full 210ab81; verdict lượt 1 đúng b0814f4, 1 P0/3 P1/2 P2; receipt lượt 20 approve dcb295a, #1091 lượt 2 approve 90b3f1c; băm bytes verdict của ba receipt đều khớp | KHÔNG PHẢI LỖI; header giữ giới hạn lịch sử, phần thân có mốc sửa tiếp theo |
| `landed_hieu_luc_tu` còn diễn đạt “merge commit của PR ghi sổ” | Trường mới cạnh nó chỉ rõ PR1111/4397ee6; bookkeeping phân biệt “PR ghi sổ landed” 1111 và “ghi sổ bổ sung” 1118 | KHÔNG PHẢI LỖI; không tự chuyển mốc landed sang PR1118 chưa merge |
| Quy tắc exact-head và comment chốt | Comment 6555093642 neo f783bee trước merge #1111; YAML vẫn giữ caveat #566: agent vận chuyển bằng token chủ kho, không đồng nhất actor với chủ kho tự gõ | KHÔNG PHẢI LỖI; không dùng comment #1111 làm authorization cho head #1118 |
| Nợ `DUYET-CHI-TRONG-PHIEN` | Nói duyệt **merge #1065**, khác comment quyết **landed qua #1111** về sau | KHÔNG PHẢI LỖI; không xoá nợ từ nguồn khác phạm vi |
| Nợ `TEST-OPS-VM-CHUA-NOI-CI` | Không thấy `cap-nhat-cong-cu_test.ps1`/`ops/vm/` trong ci.yml hoặc registry CI; metadata 23 job không tự chứng minh bộ test VM đã nối | KHÔNG PHẢI LỖI; nợ giữ đúng phạm vi |
| Nợ khởi động lại Commander | Không có quan sát native mới đóng nợ; đoạn VM không nhận đã đo đường tự khởi động | KHÔNG PHẢI LỖI; trạng thái máy thật KHÔNG ĐO ĐƯỢC |
| Bookkeeping nguồn review/Checkout và PR ghi sổ | Tệp review/provenance vẫn có; mục #1118 chỉ ghi bổ sung, không nhận merge/approval của chính #1118 | KHÔNG PHẢI LỖI |

**Kết luận: KHÔNG PHẢI LỖI.** Không phát hiện câu header hoặc phần cũ nào cần sửa vì trái với phần bổ sung; không có P3 độc lập. `approve` của review này chỉ xét độ đúng hồ sơ ở SHA được giao, không tạo quyền merge/land và không tái chứng nhận native VM hoặc danh tính runtime lịch sử ngoài nguồn đã có.

## Hướng 8 — Kiểm tra kết thúc và artifact bàn giao

**Giả thuyết:** thao tác đo đã làm thay đổi cây được review hoặc kết luận neo nhầm SHA.

**Lệnh:** so inventory SHA-256 mọi tệp ngoài `.git` trước/sau (kể cả tệp ignored nếu có), `GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored`, `git -C cay-kho rev-parse HEAD HEAD^{tree}`, `git -C cay-kho diff --check 3bdd987 HEAD`; các lệnh rc 0. Chi tiết ở [final-check.json](final-check.json), [checkout-before.json](checkout-before.json), [checkout-after.json](checkout-after.json).

**Output thật:** inventory **10168 → 10168 tệp**, added/removed/changed đều `[]`; status gồm untracked/ignored output rỗng; diff-check output rỗng; HEAD/tree giữ nguyên `352d31e03bc846cae5b4ee7bc17bbea6830fb64d` / `8d95d1d7baf35a4f3c8d7bc6ceb3995a0f77b3b4`. Snapshot chứng minh không có delta nội dung ở hai mốc đã đo; không tự chứng minh mọi hành vi trong toàn lịch sử phiên. Sandbox thực tế cho phép ghi workspace; kỷ luật read-only được kiểm bằng phép so nội dung, không khai OS đã khoá riêng checkout.

**Kết luận: KHÔNG PHẢI LỖI.** [HINT.patch](HINT.patch) tồn tại, **0 byte**, vì không còn finding cần gợi ý vá; không có hunk để áp. Không sửa repo, không push, không gọi mạng, không chạy lại CI hoặc VM. Cổng nội dung đã chạy thực và output dương được giữ; lỗi parser của script lượt 1 được ghi riêng, không tính là pass hoặc finding sản phẩm.

## Quyết định cuối

`approve` trên đúng `reviewed_sha` dòng 2. **0 lớp finding còn mở, 0 biểu hiện còn mở**; ba lớp/slug lượt 1 đều **ĐÃ VÁ THẬT** sau khi đối chiếu lại nguồn và rà cả diff. Bảy bản trích khớp nguồn, 23/23 băm OK, cổng riêng/toàn kho ĐẠT. Các giới hạn native VM, nguyên nhân huỷ và ba mốc CI còn thiếu của hai run mới đã được hồ sơ gắn nhãn trung thực; review này không nhận đã đo chúng.
