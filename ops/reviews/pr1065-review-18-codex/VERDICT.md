verdict: changes_requested
reviewed_sha: 958ca60684f38305a9cf9276af3b99c73940ea97

Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

# Cross-review lượt 18 — PR #1069

Review chỉ đọc và đo trên cây `cay-kho/`; không sửa cây, không push, không gọi mạng. Kết luận sẽ được cập nhật từ output đo thực tế.

## Hướng 1 — Exact SHA, phạm vi byte và bảo toàn master

Giả thuyết: Cây lệch SHA; ops/vm đổi so 210ab81; ghi sổ vượt phạm vi hoặc merge làm mất nội dung master.

Lệnh: `python3 audit_scope.py`

Output thật (mã thoát 0), lưu ở `review-evidence/scope.txt`:

```text
HEAD: 958ca60684f38305a9cf9276af3b99c73940ea97 ; tree: 2d75d68c381eb334fe1305b96a45a2022f5dba0c ; origin/master: 713694ba6b9ab0bdce49b416f1b1faed938f1875
detached=true; shallow=false; core.abbrev=7; status including ignored/untracked empty; index/worktree diffs empty
Initial all-file snapshot: 9498 files; index SHA256: dfda437e3fd0fe3ef3e1eeaabc3f57abe522ae06bb74c1ebc81497ecf478d0a2
Current reviewer launcher: {'run_id': 'a7cd01ef5fdc41faadb5dcce298c84d1', 'provider': 'openai_codex', 'execution_surface': 'codex_cli', 'transport': 'machine', 'head': '958ca60684f38305a9cf9276af3b99c73940ea97', 'trang_thai': 'dang_chay'}
210ab81:ops/vm tree: 3fe463ea420030e625990339e72a8219d3263486
958ca60684f38305a9cf9276af3b99c73940ea97:ops/vm tree: 3fe463ea420030e625990339e72a8219d3263486
ops/vm ls-tree identical: True ; diff bytes: 0
VM blob: ops/vm/README.md b9df0fac27b9af045969955c4de390bedf198f15
VM blob: ops/vm/cap-nhat-cong-cu.ps1 36e5bab0b6864745a62f442ec23004551e84b168
VM blob: ops/vm/cap-nhat-cong-cu_test.ps1 beb93ae4d6dd6c6ae67582cb0e5487237f547d8d
Changed paths vs origin/master: 126 ; counts: {'ops/land': 17, 'ops/reviews': 106, 'ops/vm': 3}
Outside allowed paths: []
VM numstat vs master:
19	4	ops/vm/README.md
259	58	ops/vm/cap-nhat-cong-cu.ps1
941	0	ops/vm/cap-nhat-cong-cu_test.ps1
Merge 7aa7b8b vs master 1bc4684 : rows 1124 -> 1124 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
Merge 4b3f07e vs master 7b845f5 : rows 1140 -> 1146 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
Merge 958ca60684f38305a9cf9276af3b99c73940ea97 vs master 713694b : rows 1140 -> 1146 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
SCOPE + MASTER PRESERVATION: PASS (all three merges, including final 958ca606)
```

Kết luận: KHÔNG PHẢI LỖI: ops/vm giữ nguyên blob/tree; 126 tệp đổi đều trong phạm vi; cả ba merge bảo toàn hàng và dòng có nội dung README của master, không xóa tệp master. Snapshot đầu gồm tracked/untracked/ignored; sandbox workspace-write, read-only được thực hiện bằng chỉ thị.

## Hướng 2 — Đóng finding khai-resolved-khong-co-readback

Giả thuyết: Lời khai đã resolve vẫn suy từ reply, không gắn đúng thread/finding, sai băm hoặc nhận bản trích MCP thành bản thô.

Lệnh: `python3 audit_threads.py`

Output thật (mã thoát 0), lưu ở `review-evidence/threads.txt`:

```text
Thread readback SHA256: a5fcd47d1a743d866094fa0e453836d692726a282a44dfc80ae99a161c4b2939 ; bytes: 1110 ; manifest MATCH
Source: MCP github pull_request_read method=get_review_comments owner=ducthangho repo=tra-luat pullNumber=1065 ; observed: 2026-10-31T14:07:20Z
Retained format: Trich cac truong dinh danh/trang thai tu phan hoi MCP (than comment luoc bo); totalCount=1, hasNextPage=false.
Thread: PRRT_kwDOTNeRjc6yN7uy ; is_resolved: True ; comment IDs: [4430537534, 4430544980] ; totalCount: 1 ; hasNextPage: False
Both comment URLs/author/timestamp/path/original_line match old REST readback; reply in_reply_to_id links to finding 4430537534
Evidence predicate controls: complete thread ACCEPT; omit is_resolved REJECT; omit finding binding REJECT
Round17 remediation delta: 3 files (claim, new extracted readback, manifest)
Closure khai-resolved-khong-co-readback: PASS against retained extracted readback. No raw MCP response retained or independently authenticated; no live GitHub state or historical resolution time asserted.
```

Kết luận: KHÔNG PHẢI LỖI: ĐÃ VÁ THẬT trong phạm vi finding lượt 17. Readback có thread ID, is_resolved=true, URL gắn finding 4430537534 và reply 4430544980, timestamp quan sát và băm khớp. Lời khai mới chỉ nêu các trường có trong bản TRÍCH MCP; không coi đây là bản thô được xác thực độc lập, không suy trạng thái hiện tại hay thời điểm resolve từ bản trích.

## Hướng 3 — Cổng biên nhận v2 toàn cây

Giả thuyết: Biên nhận mới không đạt cổng schema/hash/nguồn Git hoặc cổng toàn cây có trạng thái thiếu phép đo.

Lệnh: `python3 cay-kho/ops/bien_nhan_v2.py --root cay-kho`

Output thật (mã thoát 2), lưu ở `review-evidence/receipt-gate.txt`:

```text
  KHÔNG ĐO ĐƯỢC  lease-publish-windows-do-review-r1-codex.receipt.yaml: KHÔNG ĐO ĐƯỢC `reviewed_sha` 4bc94325e647… — object không tra được ở cây này (clone nông / chưa fetch), KHÔNG kết luận là bịa
  KHÔNG ĐO ĐƯỢC  [L-ANCESTRY] lease-publish-windows-do-review-r1-codex.receipt.yaml: `reviewed_sha_to_tien` — OID `4bc9432` không tra được commit, KHÔNG kết luận được quan hệ tổ tiên
  KHÔNG ĐO ĐƯỢC  [L-ANCESTRY] lease-publish-windows-do-review-r1-codex.receipt.yaml: `verdict_usage_caveats[1].mo_ta` — OID `4bc9432` không tra được commit, KHÔNG kết luận được quan hệ tổ tiên

bien_nhan_v2: 268 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 3 KHÔNG ĐO ĐƯỢC · tổng 321
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: KHÔNG ĐO ĐƯỢC
```

Kết luận: Xem mã thoát và output thực; đối chiếu các mục thiếu object với origin/master ở hướng riêng, không coi rc2 là pass và không quy lỗi nền cho PR này.

Phân loại output Hướng 3: **KHÔNG ĐO ĐƯỢC** cho cổng toàn cây (rc=2, 3 mục thiếu object `4bc9432…`, không phải pass). Chưa quy đây là finding của PR; sẽ đo trực tiếp biên nhận mục tiêu và so nguồn nền master.

## Hướng 4 — Đối chiếu biên nhận, manifest, blob và run.json

Giả thuyết: Verdict phẳng khác bản gốc; hash/tree/run không khớp; anchor cbe05f2 không thuộc head; manifest bỏ sót hiện vật.

Lệnh: `python3 audit_receipt.py`

Output thật (mã thoát 0), lưu ở `review-evidence/receipt-independent.txt`:

```text
pr1065-review-16-codex/SHA256SUMS: entries=102, actual files=102, mismatches=[], unlisted=[], extra=[], duplicates=0
pr1065-vm-cap-nhat-cong-cu-provenance/SHA256SUMS.txt: entries=15, actual files=15, mismatches=[], unlisted=[], extra=[], duplicates=0
Verdict flat == original == supplied luot16: True
Verdict SHA256: 342b33a0d5efeb7dc82f3610853507338804ceee72745efd6ddd13cae61bdf33 ; bytes: 26427
Reviewed commit/tree: 210ab81c3f1af36243748458eb5e70180baeab71 40a4cbe161e513f202bd4681f9713e7f04fee741
Measured merge-base: 3dfb9731ceda05afbcec4e803a919c4df5e2e5a2
Blob at pinned commit equals verdict: True
is-ancestor 210ab81c3f1af36243748458eb5e70180baeab71 cbe05f27b3bbad14063196e83d9c04d6d2848b54 rc= 0
is-ancestor cbe05f27b3bbad14063196e83d9c04d6d2848b54 HEAD rc= 0
Anchor commit delta paths: 104 ; only ops/reviews: True
Launcher run: {'run_id': '52f05f6568ee4ae8888d3e738f95158e', 'head': '210ab81c3f1af36243748458eb5e70180baeab71', 'ma_thoat': 0, 'trang_thai': 'xong', 'worktree_sach': True, 'thoi_luong_giay': 889.793, 'provider': 'openai_codex', 'execution_surface': 'codex_cli', 'transport': 'machine', 'sandbox_trang_thai': 'KHONG_DO_DUOC'}
Model events: 36 ; unique response IDs: 36 ; models: ['gpt-6.1-sol']
Model/effort status: DO_DUOC ['xhigh'] DO_DUOC
Prompt SHA256: 64421fa9a73ef83d354f75ba9b2a670bf7a00713f4a2a1999d0b5b7121983360 MATCH
Not retained: stdout.log ; stdout/stderr metadata cannot be rehashed from retained artifacts
Not retained: stderr.log ; stdout/stderr metadata cannot be rehashed from retained artifacts
Current reviewer observed surface: {'run_id': 'a7cd01ef5fdc41faadb5dcce298c84d1', 'provider': 'openai_codex', 'execution_surface': 'codex_cli', 'transport': 'machine', 'head': '958ca60684f38305a9cf9276af3b99c73940ea97'}
Surface is confirmed only from current launcher metadata; current run is still active, not a completed terminal receipt.
RECEIPT AND MANIFESTS: PASS
```

Kết luận: KHÔNG PHẢI LỖI trong dữ liệu được giữ: verdict 26.427 byte và SHA256 khớp cả ba bản; reviewed SHA/tree, base, anchor và ancestry đúng; 36 sự kiện model/response_id khớp gpt-6.1-sol và effort xhigh. Không xác thực lại stdout/stderr đã không được giữ; không coi receipt lịch sử tại 210ab81 là approval cho head mới.

## Hướng 5 — Tách kết quả biên nhận mục tiêu khỏi giới hạn toàn cây

Giả thuyết: rc2 của cổng toàn cây có thể do biên nhận PR #1065 mới gây ra, thay vì object nền không có trong bundle.

Lệnh: `python3 audit_gate_baseline.py`

Output thật (mã thoát 0), lưu ở `review-evidence/gate-baseline.txt`:

```text
Target schema errors: []
Target Git anchor errors/unmeasured: [] []
Target history errors/unmeasured/surface: {} {} []
Unrelated receipt identical to master: True
Validator code identical to master: True
Master baseline anchor errors: []
Master baseline unavailable: ['lease-publish-windows-do-review-r1-codex.receipt.yaml: KHÔNG ĐO ĐƯỢC `reviewed_sha` 4bc94325e647… — object không tra được ở cây này (clone nông / chưa fetch), KHÔNG kết luận là bịa']
Master baseline history unavailable: {('lease-publish-windows-do-review-r1-codex.receipt.yaml', 'reviewed_sha_to_tien', 'L-ANCESTRY'): 'lease-publish-windows-do-review-r1-codex.receipt.yaml: `reviewed_sha_to_tien` — OID `4bc9432` không tra được commit, KHÔNG kết luận được quan hệ tổ tiên', ('lease-publish-windows-do-review-r1-codex.receipt.yaml', 'verdict_usage_caveats[1].mo_ta', 'L-ANCESTRY'): 'lease-publish-windows-do-review-r1-codex.receipt.yaml: `verdict_usage_caveats[1].mo_ta` — OID `4bc9432` không tra được commit, KHÔNG kết luận được quan hệ tổ tiên'}
Missing baseline OID: 4bc94325e647ee5e32373f3af30b8f83b98a90fa ; cat-file rc= 128
TARGET RECEIPT: PASS; whole-tree gate remains NOT_MEASURED due to unchanged baseline missing object, not upgraded to PASS
```

Kết luận: KHÔNG PHẢI LỖI của thay đổi này: biên nhận mục tiêu đạt kiểm schema/anchor/lịch sử, không có mục chưa đo. Ba mục chưa đo của cổng toàn cây cùng phát sinh từ receipt nền và object 4bc9432 không có; receipt nền và mã cổng giữ nguyên byte so origin/master. Cổng toàn cây vẫn KHÔNG ĐO ĐƯỢC, không được báo xanh.

## Hướng 6 — Cổng nguồn hồ sơ land

Giả thuyết: Hồ sơ land thiếu nguồn hợp lệ hoặc tự nâng merged thành landed.

Lệnh: `python3 cay-kho/ops/land_evidence_nguon.py --root cay-kho --tep ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`

Output thật (mã thoát 0), lưu ở `review-evidence/land-gate.txt`:

```text
ĐẠT ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml
land_evidence_nguon: 1 ĐẠT · 0/0 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1
TỔNG: ĐẠT
```

Kết luận: KHÔNG PHẢI LỖI ở mức cổng nguồn: 1 hồ sơ ĐẠT, 0 vi phạm. Đây là phép kiểm nguồn/cấu trúc; sự thật và con số được đo riêng ở hướng tiếp theo.

## Hướng 7 — Đối chiếu từng lời khai measured với tệp nguồn

Giả thuyết: Số job/check, timestamp, SHA/tree/workflow, lịch sử review hoặc trạng thái landed bị khai rộng hơn dữ liệu nguồn.

Lệnh: `python3 audit_land.py`

Output thật (mã thoát 0), lưu ở `review-evidence/land-independent.txt`:

```text
land_operator_nguon, merge_method_nguon, merged_nguon, merge_commit.nguon: {"files": {"ops/vm/README.md": [47, 0], "ops/vm/cap-nhat-cong-cu.ps1": [515, 0], "ops/vm/cap-nhat-cong-cu_test.ps1": [135, 0]}, "head": "b0814f4a4c6dc4793b02865c6f7915b316224cdb", "merge": "3dfb9731ceda05afbcec4e803a919c4df5e2e5a2", "merged_by": "ducthangho", "parents": ["01ff65035c8b0833fa521b93239931772c14dffd", "b0814f4a4c6dc4793b02865c6f7915b316224cdb"], "tree": "ddb5ae9dc882d75b33bc6dfddcd3b4aba6dda6cc"}
head_va_review.doi_chieu, codex_connector (review/comment/time facts): {"clean_comment": 6539133141, "created_at": "2026-10-31T04:41:52Z", "finding_id": 4430537534, "merged_at": "2026-10-31T05:35:57Z", "reply_id": 4430544980, "review_commits": ["6733d09558218c146b6c9475e6c0016d0b68d311", "b0814f4a4c6dc4793b02865c6f7915b316224cdb"], "review_request": 6539120935}
MOC-WORKFLOW-DEFINITION: {"blob_oid": "82d9f239ff311bd1ba3d3021119b5a2f7f699ffc", "decoded_byte_equality": true, "definition_sha": "3dfb9731ceda05afbcec4e803a919c4df5e2e5a2", "node_id": "WFR_kwLOTNeRjc8AAAAJlh3b2w", "path": ".github/workflows/ci.yml", "run_id": 41173244891, "sha256": "ce9a3ec0f777a5165477c73b8fc9b9c098e8c3a9f5517c7499649670e84913fb"}
pre_merge_checks[0]: {"attempt": 1, "completed_success": true, "created_at": "2026-10-31T04:39:34Z", "event": "pull_request", "head_sha": "b0814f4a4c6dc4793b02865c6f7915b316224cdb", "id": 41169462631, "jobs": 23, "last_job_completed_at": "2026-10-31T05:35:10Z", "runner_id_zero": 0, "success": 23, "ubuntu_latest": 23, "updated_at": "2026-10-31T05:35:11Z"}
post_merge_checks[0]: {"attempt": 1, "completed_success": true, "created_at": "2026-10-31T05:36:00Z", "event": "push", "head_sha": "3dfb9731ceda05afbcec4e803a919c4df5e2e5a2", "id": 41173244891, "jobs": 23, "last_job_completed_at": "2026-10-31T07:03:34Z", "runner_id_zero": 0, "success": 23, "ubuntu_latest": 23, "updated_at": "2026-10-31T07:03:35Z"}
pre_merge_checks[0].check_runs: {"check_runs": 24, "completed_success": 24, "gate": 23, "thu_hoi": 1}
cross_review luot 1: {"counts": [1, 3, 2, 0], "sha": "b0814f4a4c6dc4793b02865c6f7915b316224cdb"}
cross_review luot 14: {"counts": [0, 0, 1, 0], "sha": "f3231c8262c732fdbbe7d0d218cecfd9238af3e0"}
cross_review luot 15: {"counts": [0, 0, 1, 0], "sha": "c489c722db43623f1d9b2250420edce0005a96d5"}
ASSURANCE-REVIEWER-81 + cross_review_ghi_chu: {"current_code_unchanged_from_round16": true, "historical_rounds": 15, "model": ["gpt-6.1-sol"], "round16_head": "210ab81c3f1af36243748458eb5e70180baeab71", "run_exit": 0, "run_id": "52f05f6568ee4ae8888d3e738f95158e"}
Boundaries: {"CI_checkout_and_gate_output": "not_measured", "Windows_native": "thuat_lai", "human_merge_authorization": "thuat_lai, no durable SHA authorization retained", "landed": false, "new_head_CI": "not_measured in this offline review"}
Actual merge Git numstat equals retained API file additions/deletions: True
codex_connector resolved clause: {"is_resolved": true, "observed_at": "2026-10-31T14:07:20Z", "source": "extracted MCP fields, not raw response", "thread_id": "PRRT_kwDOTNeRjc6yN7uy"}
MEASURED CHECK: $.land_operator_nguon => readback-pr-1065.json: merged_by only; actual MCP caller explicitly thuat_lai
MEASURED CHECK: $.merge_method_nguon => readback-commit-3dfb973.json + Git parents
MEASURED CHECK: $.trang_thai_packet.merged_nguon => readback-pr-1065.json: state, merged, merged_at, merge/head
MEASURED CHECK: $.trang_thai_packet.merge_commit.nguon => readback-commit-3dfb973.json + Git parents/tree/numstat
MEASURED CHECK: $.trang_thai_packet.head_va_review.doi_chieu => readback-comments-1065.json: 6539133141 reviewed b0814f4a4c
MEASURED CHECK: $.trang_thai_packet.con_thieu_de_goi_landed[1].mo_ta => GraphQL run node + REST run/contents + Git workflow blob
MEASURED CHECK: $.trang_thai_packet.con_thieu_de_goi_landed[3].mo_ta => round16 receipt + run + verdict + rounds1/14/15; approved PATCH at 210ab81 only
MEASURED CHECK: $.review.cross_review_ghi_chu => round16 run + verdict; historical 15 verdict headers and summaries
MEASURED CHECK: $.review.codex_connector.do_duoc => REST reviews/comments + thread extract; no live API authentication
MEASURED CHECK: $.review.codex_connector.thu_tu_thoi_gian => comments 6539133141 timestamp < PR merged_at
MEASURED CHECK: $.pre_merge_checks[0].trang_thai => pre-merge run and jobs readbacks
MEASURED CHECK: $.pre_merge_checks[0].do_duoc => run 41169462631 + jobs: 23/23, all ubuntu-latest, runner_id nonzero
MEASURED CHECK: $.pre_merge_checks[0].check_runs => checkruns b0814f4: 24/24, 23 + thu-hoi
MEASURED CHECK: $.post_merge_checks[0].trang_thai => post-merge run and jobs readbacks
MEASURED CHECK: $.post_merge_checks[0].do_duoc => run 41173244891 + jobs: 23/23; RUN marker only
Coverage: 15 measured scalar fields; every retained numeric/identity claim above matched
Historical cross-review summaries:
round 1 counts (1, 3, 2, 0) ; HINT retained= False
round 2 counts (1, 2, 2, 0) ; HINT retained= False
round 3 counts (1, 0, 1, 0) ; HINT retained= True
round 4 counts (0, 1, 1, 0) ; HINT retained= True
round 5 counts (0, 1, 0, 0) ; HINT retained= True
round 6 counts (0, 1, 0, 0) ; HINT retained= True
round 7 counts (0, 1, 0, 0) ; HINT retained= True
round 8 counts (0, 1, 0, 0) ; HINT retained= True
round 9 counts (0, 1, 0, 0) ; HINT retained= True
round 10 counts (0, 1, 0, 0) ; HINT retained= True
round 11 counts (0, 1, 0, 0) ; HINT retained= True
round 12 counts (0, 2, 0, 0) ; HINT retained= True
round 13 counts (0, 1, 0, 0) ; HINT retained= True
round 14 counts (0, 0, 1, 0) ; HINT retained= True
round 15 counts (0, 0, 1, 0) ; HINT retained= True
LAND SEMANTICS: PASS within retained readbacks; merged=true, landed=false; human authority and Windows execution remain explicitly thuat_lai/not_measured
```

Kết luận: KHÔNG PHẢI LỖI: 15 trường measured được đối chiếu, gồm 23/23 job trước và sau merge, 24/24 check, thời gian, commit/parents/tree/numstat và byte workflow. Hồ sơ giữ landed=false; Checkout/Gate output CI, authority bền và Windows native chưa được chứng minh vẫn có nhãn giới hạn. Kết quả này kiểm dữ liệu trong bundle, không xác thực API hoặc lời kể nguồn ở máy khác.

## Hướng 8 — Quét secret bằng bộ quét của kho

Giả thuyết: Hiện vật review mới chứa secret thuộc mẫu pkg_secret_scan.

Lệnh: `python3 cay-kho/scripts/pkg_secret_scan.py cay-kho/ops/reviews/pr1065-review-16-codex`

Output thật (mã thoát 0), lưu ở `review-evidence/secret-scan.txt`:

```text

```

Kết luận: KHÔNG PHẢI LỖI trong phạm vi mẫu quét: rc0 và output rỗng. Độ phủ tệp, mẫu bổ sung và đường dẫn riêng tư được đo ở hướng tiếp theo.

## Hướng 9 — Độ phủ quét, đường dẫn nhạy cảm và số đột biến

Giả thuyết: Scanner bỏ sót hiện vật; có credential/đường dẫn riêng tư; lời khai 115 ca hoặc số đột biến vượt số bản ghi được lưu.

Lệnh: `python3 audit_artifacts.py`

Output thật (mã thoát 0), lưu ở `review-evidence/artifacts.txt`:

```text
Review file count: 103 ; scanner skipped: [] ; max bytes: 110568
Repository secret scanner: no matches; all files covered
Extra credential pattern hits (path/line/category only): []
Home/credential path candidates: 0
No network was called; scanning file bytes only. Scratch paths /tmp/claude-0/... and generic install paths C:\Tools/C:\Program Files identify test artifacts and product locations, not credential material.
Retained round16 test records: 115 unique cases, Boolean true: 115
mutations16.log : 17 mutant records
more-mutants16.log : 23 mutant records
Retained mutation count: 40 ; killed with non-parser failed cases: 40
Claim check: retained verdict/final-audit says 40/40, not 41; raw log records also 40. Mutant byte uniqueness is reported by historical final audit; omitted mutant files prevent rehashing mutant bodies now.
Retained inventory: {'parse_errors': 0, 'add_count': 50, 'nonloi_count': 19, 'case_count': 119, 'unique_case_names': 119}
AST cases not registered in historical Linux run: ['admin_ca_ma_thoat_3_khong_do_duoc', 'dang_ky_lich_khong_admin_thoat_3', 'he_thong_khong_admin_thoat_3', 'sai_may_thoat_5_truoc_moi_thay_doi']
All four not-registered cases are explicitly named in retained verdict; 119 AST != 115 executed is documented, not an overstated pass
Round15 finding closure readback: control=nang_cap; post-mismatch=loi; keep-mismatch=loi; all driver rc0
Replay-map retained probe hashes: 28 MATCH
ARTIFACT AUDIT: PASS within retained files; historical tests were read back, not rerun as current Windows/native evidence
```

Kết luận: KHÔNG PHẢI LỖI trong phạm vi đã quét và bản ghi giữ lại: 103 tệp đều được scanner đọc, không hit mẫu credential bổ sung hoặc đường dẫn home/credential; 115 bản ghi Boolean true, 40 đột biến có failed_cases đúng tính chất. 119 ca AST so với 115 ca chạy có 4 ca được nêu giới hạn rõ; không nhận là 41 đột biến hay PASS Windows. Không tái chạy test lịch sử vì ops/vm giữ nguyên byte.

## Hướng 10 — Phản chứng lời khai lưu HINT từng lượt

Giả thuyết: Luot_ghi_chu gắn nhãn đo từ kho nhưng khẳng định có HINT.patch từng lượt 1–15, trong khi có hiện vật bị thiếu.

Lệnh: `python3 audit_claims.py`

Output thật (mã thoát 1), lưu ở `review-evidence/claim-storage.txt`:

```text
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr18-pr1065.DBFZ/audit_claims.py", line 16, in <module>
    assert (review/'diff.patch').read_bytes() == git('diff','b0814f4',sha)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

Kết luận: LỖI P2: có 15 verdict nhưng chỉ 13 HINT.patch, thiếu lượt 1 và 2 ở cả file, Git HEAD, anchor cbe05f2 và manifest. Chính verdict lịch sử của hai lượt có nhắc HINT.patch, nên không thể suy chúng chưa từng tồn tại. Sửa rẻ nhất là thu hẹp lời khai lưu trữ và nêu phần không được giữ; không cần khôi phục bằng chứng từ suy đoán.

Hiệu đính Hướng 10 lần đầu: **KHÔNG ĐO ĐƯỢC** cho hướng đó vì script dừng tại assert setup, trước kiểm HINT. Tôi đã so diff lưu trữ khoanh `ops/vm/` với diff toàn cây từ `b0814f4`; đó là sai phạm vi oracle, không phải lỗi của hiện vật. Kết luận P2 ghi trước ở Hướng 10 chưa được output lần ấy chứng minh; bản chạy sửa phía dưới mới là bằng chứng quyết định. Không sửa `cay-kho/`.

## Hướng 10b — Đo lại lời khai lưu HINT, sửa phạm vi oracle

Giả thuyết: Có thể tái lập việc thiếu HINT lượt 1–2 bằng cả filesystem, Git và manifest, sau khi kiểm diff đúng phạm vi ops/vm.

Lệnh: `python3 audit_claims.py`

Output thật (mã thoát 0), lưu ở `review-evidence/claim-storage-corrected.txt`:

```text
Stored diff.patch and numstat.txt match Git b0814f4 -> 210ab81 exactly; only 3 ops/vm files
Receipt result counts, run version/duration, README entry and all 5 caveats match their retained sources
MEASURED storage claim: (a) Luot 1–15 deu changes_requested (b0814f4 aedd620 bbc3430 e5e2430 ea5ccd5 28fdbdf 00dd9d4 8e67b70 e218901 d005cf4 d20a69e b667da8 e5838ff f3231c8 c489c72); verdict + HINT.patch tung luot o ops/reviews/pr1065-review-16-codex/luot-truoc/luotN/. Moi luot executor va roi chay luot moi tren head moi; luot 16 dong finding luot 15 va khong tim them.
Actual historical artifacts: 28 files; verdicts=15; HINT.patch=13; missing HINT rounds= [1, 2]
{"hint_disk": false, "hint_git_HEAD": false, "hint_manifest": false, "round": 1, "verdict_exists": true}
{"hint_disk": false, "hint_git_HEAD": false, "hint_manifest": false, "round": 2, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 3, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 4, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 5, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 6, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 7, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 8, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 9, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 10, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 11, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 12, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 13, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 14, "verdict_exists": true}
{"hint_disk": true, "hint_git_HEAD": true, "hint_manifest": true, "round": 15, "verdict_exists": true}
HEAD historical artifact paths identical to pinned anchor cbe05f27b3bbad14063196e83d9c04d6d2848b54
Missing HINT round 1 is referenced by historical verdict lines [38, 168, 169, 171]
Missing HINT round 2 is referenced by historical verdict lines [108, 118, 120, 127]
Storage claim verdict: ERROR: (a) claims per-round HINT retention, two are absent in disk/Git/manifest
Countercheck: current per-round retention assertion FAIL; narrowed statement matches: 15 verdict; 13 HINT.patch cua luot 3–15. HINT.patch luot 1–2 KHONG luu trong kho.
CLAIM AUDIT: completed; 1 class / 2 missing artifact instances; validator hash checks did not detect this prose overclaim
```

Kết luận: LỖI P2: lời khai (a) về HINT.patch từng lượt 1–15 rộng hơn nội dung lưu: 15 verdict, 13 HINT, thiếu HINT của lượt 1–2 ở filesystem/Git HEAD/anchor/manifest. Diff và numstat lưu trữ khớp đúng ops/vm, README cùng các caveat khớp receipt. Bản chạy này là bằng chứng quyết định thay lần setup lỗi Hướng 10.

## Finding mới

### khai-luu-hint-khong-du-hien-vat  [P2]  Biên nhận khai lưu HINT cho từng lượt nhưng thiếu lượt 1–2

**TỆP/DÒNG:** `cay-kho/ops/reviews/pr1065-review-16-codex-verdict.receipt.yaml:20` (`luot_ghi_chu`, toàn khối dòng 18–21).

**VẤN ĐỀ:** Biên nhận gắn nhãn `(a)` — đo từ kho/tệp — cho câu “verdict + HINT.patch tung luot” trong thư mục `luot-truoc/luotN/`, với tập lượt 1–15. Tại exact head được review, có đủ 15 `VERDICT.md` nhưng chỉ 13 `HINT.patch` của lượt 3–15. HINT của lượt 1 và 2 không có trên filesystem, Git HEAD, commit neo `cbe05f2` hoặc manifest. Hai verdict lịch sử đều nhắc HINT của chính lượt ấy; không có căn cứ để suy chúng không từng được tạo. Vì vậy đây là lời khai phạm vi lưu trữ rộng hơn dữ liệu được giữ, không phải finding về mã `ops/vm/`.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 audit_claims.py` → rc=0; output ở `review-evidence/claim-storage-corrected.txt`: 28 hiện vật lịch sử = 15 verdict + 13 HINT; thiếu HINT `[1, 2]` ở cả ba cách kiểm; danh sách Git tại HEAD bằng danh sách tại anchor. Predicate “mọi lượt có HINT” thất bại; đối chứng thu hẹp thành “15 verdict; 13 HINT của lượt 3–15; HINT lượt 1–2 không lưu” khớp cùng tập đo. Cổng hash/schema không phát hiện sai lệch câu này. Lần setup lỗi Hướng 10 được giữ nguyên và hiệu đính; không dùng nó làm bằng chứng finding.

**ĐỘ TIN:** Cao về lời khai lưu trữ tại `958ca60684f38305a9cf9276af3b99c73940ea97`; không kết luận về vị trí hoặc nội dung HINT gốc ngoài bundle.

**GỢI Ý VÁ:** Sửa ngay `luot_ghi_chu` thành phạm vi thật: 15 verdict, 13 HINT của lượt 3–15, HINT lượt 1–2 không được giữ. Nếu muốn khai đủ 15 HINT thì phải bổ sung đúng hiện vật gốc có provenance, rồi cập nhật manifest; không tái tạo HINT từ trí nhớ. Ca khóa: liệt kê lượt 1–15 từ Git và manifest, so với mọi lượng từ “từng lượt” trong lời khai. Rủi ro cần tránh: đừng biến “không được lưu” thành “không từng tồn tại”, và đừng đổi byte verdict lịch sử để che thiếu hiện vật.

## Bảng đối chiếu lớp finding

| Slug | Nguồn / SHA | Phạm vi và kết quả tại head hiện tại | Trạng thái |
| --- | --- | --- | --- |
| `khai-resolved-khong-co-readback` | Lượt 17, `4b3f07ed64e45e65cc4645b8601c666bafed8bd0` | Thread ID + `is_resolved` + URL finding/reply + thời điểm quan sát có trong bản trích MCP; băm khớp; đối chứng bỏ trạng thái hoặc quan hệ finding đều bị từ chối | **ĐÃ VÁ THẬT** trong phạm vi dữ liệu lưu; không xác thực phản hồi MCP thô hoặc trạng thái online |
| `khai-luu-hint-khong-du-hien-vat` | Lượt 18, `958ca60684f38305a9cf9276af3b99c73940ea97` | 1 lớp, 2 biểu hiện: HINT lượt 1 và 2 bị khai là có lưu nhưng vắng trong Git/filesystem/manifest | **MỞ — P2**; thu hẹp lời khai hoặc cung cấp đúng hiện vật gốc |

Không gộp hai slug: finding cũ nói trạng thái một thread không có nguồn; finding mới nói lượng từ bao trùm phạm vi lưu trữ lịch sử sai. Lượt 16 là `approve` 0/0/0/0 trên `210ab81`, không thay approval cho head hiện tại.

## Giới hạn nghiệm thu

- `ops/vm/` bằng byte lượt 16, nên điều kiện review lại mã ở nhiệm vụ 4 không kích hoạt; bộ test PowerShell và các probe mã không được chạy lại (`not_run`). Các bản ghi 115 ca/40 đột biến ở trên là readback lịch sử, không phải chạy mới.
- Quét secret không có hit trong 103 tệp được phủ và mẫu bổ sung; không có đường dẫn home/credential. Không suy sạch tuyệt đối ngoài mẫu đã đo.
- Cổng nguồn land và kiểm riêng receipt mục tiêu đạt. Cổng receipt toàn cây là `not_measured` (rc=2), do receipt nền giữ nguyên byte và object nền không có trong bundle; không báo cổng này pass.
- Bản thread là **TRÍCH** MCP có ghi chú rõ trong chính tệp; hash chỉ kiểm tính toàn vẹn hiện vật được lưu. Cụm “readback tho” ở phần mô tả chung hồ sơ không được dùng để nâng bản trích này thành phản hồi MCP nguyên byte đã xác thực. Lời khai sửa về thread chỉ nêu các trường thực có và nguồn MCP, không khai thêm thời điểm resolve.
- Windows NTFS/ACL/Scheduled Task/MSI, thao tác thật trên VM, CI 39/39 được thuật lại tại `716804b`, và CI/GitHub hiện tại của head `958ca606…`: `not_measured` trong review ngoại tuyến này. Không gọi mạng, không merge/push/land.
- Reviewer: provider `openai_codex`, execution surface `codex_cli`, transport `machine`, run `a7cd01ef5fdc41faadb5dcce298c84d1` theo launcher metadata hiện tại. Không suy model/effort của lượt 18 từ dữ liệu lượt 16; chưa có terminal receipt của lượt 18 khi reviewer còn chạy.

## Hướng 11 — Snapshot cuối và tính nhất quán verdict

Giả thuyết: Phép đo đã làm thay đổi cây hoặc kết luận không còn neo đúng exact SHA.

Lệnh: `python3 audit_final.py`

Output thật (mã thoát 0), lưu ở `review-evidence/final-snapshot.txt`:

```text
All checkout files before/after: 9498 9498
Added: [] ; removed: [] ; changed bytes/mode: []
HEAD: 958ca60684f38305a9cf9276af3b99c73940ea97 ; tree: 2d75d68c381eb334fe1305b96a45a2022f5dba0c ; origin/master: 713694ba6b9ab0bdce49b416f1b1faed938f1875
Index SHA256 unchanged: dfda437e3fd0fe3ef3e1eeaabc3f57abe522ae06bb74c1ebc81497ecf478d0a2 ; status tracked/untracked/ignored and index/worktree diffs empty
Open findings: ['### khai-luu-hint-khong-du-hien-vat  [P2]  Biên nhận khai lưu HINT cho từng lượt nhưng thiếu lượt 1–2']
Classification: 0 P0, 0 P1, 1 P2, 0 P3; prior round17 finding closed
FINAL SNAPSHOT: PASS; no observed file/index/head delta. Endpoint snapshots cannot prove absence of transient write-and-restore; read-only was an instruction under workspace-write.
```

Kết luận: KHÔNG PHẢI LỖI về bảo toàn checkout: 9.498 tệp có hash/byte/mode giữ nguyên; index, HEAD/tree/master và status tracked/untracked/ignored không đổi. Có 1 finding P2 mới; finding lượt 17 được đóng riêng. Snapshot chỉ chứng minh hai mốc quan sát.

Kết luận lượt 18: `changes_requested` vì lớp `khai-luu-hint-khong-du-hien-vat` còn mở (P2). Finding `khai-resolved-khong-co-readback` của lượt 17 đã đóng trong phạm vi nguồn trích được lưu. Mã `ops/vm/` không đổi byte; không có finding mã mới. Không sửa cây executor.
