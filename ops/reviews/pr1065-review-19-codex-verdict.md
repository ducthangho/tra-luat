verdict: changes_requested
reviewed_sha: 43372542cc2480f3b4f8228d824afd509b1054cc

Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

# Cross-review lượt 19 — PR #1069

Phạm vi: chỉ đọc và đo cây `cay-kho/`; không sửa cây, không push, không gọi mạng. Mọi kiểm tra gắn với head nêu trên. Kết quả và bằng chứng được nối thêm sau mỗi hướng thử.

## Khởi tạo

- Giả thuyết: `runs/c5d9680a/prompt.snapshot` xác định đầy đủ phạm vi và quy trình lượt 19.
- Lệnh: `cat runs/c5d9680a/prompt.snapshot`.
- Output: đối tượng `43372542cc2480f3b4f8228d824afd509b1054cc`, yêu cầu kiểm tra finding lượt 17–18, phạm vi diff, biên nhận v2, land evidence, secret scan; ghi tăng dần từ `verdict: dang_lam`.
- Kết luận: KHÔNG PHẢI LỖI — đã khởi tạo biên bản trước khi thực hiện các hướng đo.

## Hướng 1 — Exact SHA, byte ops/vm, phạm vi và bảo toàn master

Giả thuyết: Head sai, ops/vm đổi so 210ab81, ghi sổ vượt phạm vi hoặc các merge làm mất dữ liệu master.

Lệnh: `python3 audit_scope.py`

Output thật (mã thoát 0), lưu ở `review-evidence/scope.txt`:

```text
HEAD: 43372542cc2480f3b4f8228d824afd509b1054cc ; tree: ecebb7d55a972c13b9f58ed38d96eda55c5909d7 ; origin/master: a253c169ed79617b8d1a4754867c336ac72c72c5
detached=true; shallow=false; core.abbrev=7; status including ignored/untracked empty; index/worktree diffs empty
Initial all-file snapshot: 9502 files; index SHA256: 78406676d779f9de5cdfa32a21a267e36e13d55c29fd458381e024067e2e5889
Current reviewer launcher: {'run_id': 'c5d9680afe3a43b18ad2364c5b803632', 'provider': 'openai_codex', 'execution_surface': 'codex_cli', 'transport': 'machine', 'head': '43372542cc2480f3b4f8228d824afd509b1054cc', 'trang_thai': 'dang_chay'}
210ab81:ops/vm tree: 3fe463ea420030e625990339e72a8219d3263486
43372542cc2480f3b4f8228d824afd509b1054cc:ops/vm tree: 3fe463ea420030e625990339e72a8219d3263486
ops/vm ls-tree identical: True ; diff bytes: 0
VM blob: ops/vm/README.md b9df0fac27b9af045969955c4de390bedf198f15
VM blob: ops/vm/cap-nhat-cong-cu.ps1 36e5bab0b6864745a62f442ec23004551e84b168
VM blob: ops/vm/cap-nhat-cong-cu_test.ps1 beb93ae4d6dd6c6ae67582cb0e5487237f547d8d
Changed paths vs origin/master: 128 ; counts: {'ops/land': 17, 'ops/reviews': 108, 'ops/vm': 3}
Outside allowed paths: []
VM numstat vs master:
19	4	ops/vm/README.md
259	58	ops/vm/cap-nhat-cong-cu.ps1
941	0	ops/vm/cap-nhat-cong-cu_test.ps1
Merge 7aa7b8b vs master 1bc4684 : rows 1124 -> 1124 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
Merge 4b3f07e vs master 7b845f5 : rows 1140 -> 1146 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
Merge 958ca60 vs master 713694b : rows 1140 -> 1146 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
Merge 43372542cc2480f3b4f8228d824afd509b1054cc vs master a253c16 : rows 1140 -> 1146 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
SCOPE + MASTER PRESERVATION: PASS (all four merges, including final 43372542)
```

Kết luận: KHÔNG PHẢI LỖI — head/tree và snapshot đã neo; ops/vm bằng byte bản đã approve; tất cả đường dẫn đổi nằm trong phạm vi; bốn merge bảo toàn mọi hàng/dòng có nội dung README của master và không xóa tệp. Không kích hoạt review lại mã PowerShell theo nhiệm vụ 4.

## Hướng 2 — Đóng finding lượt 18 và đo tập hiện vật lịch sử

Giả thuyết: Lời khai mỗi lượt có VERDICT và HINT vẫn thiếu tệp, thiếu băm hoặc nhận hiện vật mới là đã có tại anchor cũ.

Lệnh: `python3 audit_storage.py`

Output thật (mã thoát 0), lưu ở `review-evidence/storage.txt`:

```text
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 6730, "sha256": "0030e7526a59ff58b0db029d23dc19d0f9987e457dcf18c70cbe6c2c3328ae44"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 35577, "sha256": "45d9cb31128d3b0ed839d1a9c7443e5ccc4378eb2bc1c600ed6c4d0904fe7fb6"}, "round": 1}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 9708, "sha256": "010a5d598b2db1130d192cff59b32064aa4de19fd9d18ddbad60eedb60220027"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 26952, "sha256": "7dceed3f172857864e36f708de026e7ea56d038d0305f04c3b5ed137c2084837"}, "round": 2}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 10282, "sha256": "1e0947e58139c0b02dee0e86eb812e0e51a992e8b9e5a7f62c0248a3eb2bce27"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 30358, "sha256": "a80995d95c2d0234b929f6d273644d7c4b6099a58912a2144fe6c63961ab4402"}, "round": 3}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 6862, "sha256": "14491ba9333662f1738f0e4ab6303e210214b59f91113c8b534786f7c659bdda"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 29529, "sha256": "9535d8d85b5ae7368ddb89bdf11746e8177407a7820d83021dccb79ec964fe94"}, "round": 4}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 1744, "sha256": "d3294ae2d8fbc6ad498dbf5799b85caaea47d613f5ea952956c82e656187b46f"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 23680, "sha256": "54487260b822846ab79d5596b2daf769c66ec4bfa5c2c80a4a962134a18ee307"}, "round": 5}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 2963, "sha256": "e699e30a9bd0abd4535a42d16081dca2aca4823cee7e0907953a15784bf2c4e0"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 25387, "sha256": "ab99e4661a900a7473484c4a2719f12a6072ef05dca255ee0a3e90fe820cf6b4"}, "round": 6}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 2035, "sha256": "54eeea4cc1ce2a12090ff67643f5c59aaf4217fd0ba77c8b82911986350012ff"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 20604, "sha256": "6dd5d612749538aab2d1b5e20e9de190565358fb1bfcc52f453f8163112ca58a"}, "round": 7}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 4429, "sha256": "46e96414eeaaaa64d42b4cc12de6fef68495303f67a07f1e6b6351519ec0f78d"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 25751, "sha256": "375300c647f37530f0820d8bf1d9e1d733718f6200c7b8f56735a6dc303de96e"}, "round": 8}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 5325, "sha256": "5d95e7c31af2cd527e35d5c2a271e413bd5a5d2b02a9a364450fbbc1600af022"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 22212, "sha256": "55203f05f7853417d06dd41e67cc7d3b5bacb7354249f5f67bcea047c15d4589"}, "round": 9}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 5015, "sha256": "61c87b873ce8fa842309c4109df30e4a70d8c1a2014d4a20f036ac4053e49a58"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 36266, "sha256": "01ebb27d3d361e9a3651e54a1e38018ae2a3e6d398942dda822f745ff8cda3b5"}, "round": 10}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 5133, "sha256": "3383861346bbfbbe62ab637424fda79d2e2bf34f2b5f4cac429c42bfd80d513d"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 34307, "sha256": "40e88949819462478ae4a4e7cf9530235d4b497794b4a11c31ef86a5186435e3"}, "round": 11}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 4521, "sha256": "f9f07fe04e1284775e5da25f584a69e4cc153942646aff3f31cf12637d6d3050"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 35957, "sha256": "42346aa6e751fd1009c346ab7d1ed71f65cecceba91c91cbf269a7037bad1dcb"}, "round": 12}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 4574, "sha256": "91c067da17695a0506d7fb7b5d52eacd45bc59efdd30da4f4165695bdfd89c84"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 38949, "sha256": "36ae2970103f5a0fd53086dc43b3f7efcc9d0e679028945d216b4895cd4687c3"}, "round": 13}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 6207, "sha256": "62afd445742d87228887e642d99f5b5700cdece598969df1de5550cd73da00ce"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 34208, "sha256": "118fd9f718f81c81f1d50f487cdd426e10258fdd70dbc51cbd4f2162045c654a"}, "round": 14}
{"HINT.patch": {"Git/disk/manifest": "MATCH", "bytes": 5087, "sha256": "8f6cb3af5ff654afc6f1b878a7845b708aed99bb1cd6bc2cdd78db4e685439b8"}, "VERDICT.md": {"Git/disk/manifest": "MATCH", "bytes": 27591, "sha256": "36a01565a3a4a40faea20738dd86de8034c05d1d2fc25614d48fa6224e5e0d25"}, "round": 15}
Historical artifacts: 15 VERDICT.md + 15 HINT.patch = 30 tracked files; all nonempty; Git/disk/SHA256SUMS match
New HINT round 1 parse only (no apply), rc=0: 100	0	vm/cap-nhat-cong-cu_review_test.ps1
New HINT round 2 parse only (no apply), rc=0: 73	0	vm/cap-nhat-cong-cu_dang-ky_probe.ps1 ; 59	0	vm/cap-nhat-cong-cu_dang-ky_test.py ; 15	0	vm/cap-nhat-cong-cu_icacls_stub.py
Bookkeeping delta from round18: ['ops/reviews/pr1065-review-16-codex/SHA256SUMS', 'ops/reviews/pr1065-review-16-codex/luot-truoc/luot1/HINT.patch', 'ops/reviews/pr1065-review-16-codex/luot-truoc/luot2/HINT.patch']
Storage clause receipt.luot_ghi_chu => (a) Luot 1–15 deu changes_requested (b0814f4 aedd620 bbc3430 e5e2430 ea5ccd5 28fdbdf 00dd9d4 8e67b70 e218901 d005cf4 d20a69e b667da8 e5838ff f3231c8 c489c72); verdict + HINT.patch tung luot o ops/reviews/pr1065-review-16-codex/luot-truoc/luotN/. Moi luot executor va roi chay luot moi tren head moi; luot 16 dong finding luot 15 va khong tim them.
Storage clause land.review.cross_review_ghi_chu => measured — luot 16: ops/reviews/pr1065-review-16-codex/run/run.json (head 210ab81, ma_thoat 0) va ops/reviews/pr1065-review-16-codex/VERDICT.md; luot 1–15: ops/reviews/pr1065-review-16-codex/luot-truoc/ (chi verdict + HINT, run cua cac luot ay KHONG luu trong kho). Finding P0/P1 cua luot 1–13 deu sua tren nhanh PR #1069; luot 14–15 chi P2.
Historical run.json files: 0; land explicitly says runs for rounds1-15 are NOT retained
Pinned verdict anchor retains 28 historical paths; current HEAD retains 30. No claim that new HINTs existed at cbe05f2; verdict bytes remain separately anchored.
Round18 closure khai-luu-hint-khong-du-hien-vat: PASS for artifact completeness and storage claims at current HEAD. Original round1-2 sandbox bytes are not separately available for historical source authentication.
```

Kết luận: KHÔNG PHẢI LỖI — ĐÃ VÁ THẬT finding lượt 18: 30/30 tệp lịch sử đầy đủ, không rỗng, khớp Git và manifest; hai patch mới đọc được bằng git apply --numstat, không áp vào cây. Lời khai lưu trữ khớp HEAD; không có run lịch sử và hồ sơ nói rõ giới hạn. Không xác thực nguồn sandbox gốc lượt 1–2 khi nguồn ấy không có trong bundle.

## Hướng 3 — Finding lượt 17 vẫn đóng bằng bản trích thread

Giả thuyết: Trạng thái resolved không gắn finding 4430537534, sai băm hoặc bị suy thành trạng thái live/bản thô MCP.

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

Kết luận: KHÔNG PHẢI LỖI — finding lượt 17 vẫn ĐÃ VÁ THẬT: thread ID, is_resolved=true, finding/reply và SHA256 khớp; bỏ trường trạng thái hoặc quan hệ finding thì phép kiểm từ chối. Nguồn được giữ là TRÍCH trường MCP, không phải phản hồi thô và không xác thực live hay thời điểm resolve.

## Hướng 5 — Biên nhận, manifest, verdict blob và launcher run

Giả thuyết: Manifest thiếu tệp hoặc sai băm; verdict flat khác bản gốc; reviewed_sha/tree/run không khớp; anchor cbe05f2 không phải tổ tiên head.

Lệnh: `python3 audit_receipt.py`

Output thật (mã thoát 0), lưu ở `review-evidence/receipt-independent.txt`:

```text
pr1065-review-16-codex/SHA256SUMS: entries=104, actual files=104, mismatches=[], unlisted=[], extra=[], duplicates=0
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
Current reviewer observed surface: {'run_id': 'c5d9680afe3a43b18ad2364c5b803632', 'provider': 'openai_codex', 'execution_surface': 'codex_cli', 'transport': 'machine', 'head': '43372542cc2480f3b4f8228d824afd509b1054cc'}
Surface is confirmed only from current launcher metadata; current run is still active, not a completed terminal receipt.
RECEIPT AND MANIFESTS: PASS
```

Kết luận: KHÔNG PHẢI LỖI trong dữ liệu lưu: hai manifest phủ đủ và khớp băm; ba bản verdict bằng byte, SHA/tree/base/anchor/ancestry đúng; run.json khớp provider/surface/transport/head/rc/model/effort/prompt. stdout/stderr gốc không được giữ để băm lại; receipt 210ab81 không tự cấp approval cho head mới.

## Hướng 4 — Cổng biên nhận v2 toàn cây

Giả thuyết: Biên nhận ghi sổ không đạt schema/hash/Git hoặc cổng thiếu dữ liệu.

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

Kết luận: KHÔNG ĐO ĐƯỢC cho cổng toàn cây nếu rc=2; không coi thiếu object nền là pass. Đo riêng mục tiêu và nguồn origin/master ở hướng sau để phân biệt lỗi PR với giới hạn bundle.

## Hướng 6 — Cổng nguồn hồ sơ land

Giả thuyết: Hồ sơ land thiếu nguồn, sai schema hoặc khai đóng mốc khi không có tệp.

Lệnh: `python3 cay-kho/ops/land_evidence_nguon.py --root cay-kho --tep ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`

Output thật (mã thoát 0), lưu ở `review-evidence/land-gate.txt`:

```text
ĐẠT ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml
land_evidence_nguon: 1 ĐẠT · 0/0 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1
TỔNG: ĐẠT
```

Kết luận: KHÔNG PHẢI LỖI ở cổng nguồn nếu rc=0 và có bằng chứng dương; ý nghĩa từng lời khai measured được đo độc lập trong hướng tiếp theo, không suy chỉ từ cổng.

## Hướng 7 — Đối chiếu từng measured với readback và Git

Giả thuyết: Số merge/CI/workflow/review hoặc trạng thái landed rộng hơn dữ liệu lưu; một lời khai measured bị bỏ sót.

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
round 1 counts (1, 3, 2, 0) ; HINT retained= True
round 2 counts (1, 2, 2, 0) ; HINT retained= True
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

Kết luận: KHÔNG PHẢI LỖI trong 15 trường measured đã liệt kê: merge/parents/tree/numstat, workflow bytes, 23+23 jobs, 24 check-runs, review IDs/SHA/thời gian và lịch sử verdict đều khớp. merged=true và landed=false; quyền human, Windows native, Checkout/Gate output và CI head mới không được nâng từ thuật lại/không đo thành pass.

## Hướng 8 — Quét secret bằng scanner của repository

Giả thuyết: Hiện vật review mới có secret khớp bảng mẫu của kho.

Lệnh: `python3 cay-kho/scripts/pkg_secret_scan.py cay-kho/ops/reviews/pr1065-review-16-codex`

Output thật (mã thoát 0), lưu ở `review-evidence/secret-scan.txt`:

```text

```

Kết luận: KHÔNG PHẢI LỖI trong mẫu scanner (rc=0, stdout rỗng theo thiết kế); độ phủ tệp, đường dẫn và mẫu credential bổ sung được đo riêng tiếp theo.

## Hướng 9 — Độ phủ quét, đường dẫn và các con số test/đột biến lịch sử

Giả thuyết: Scanner bỏ tệp mới; có credential/đường dẫn nhạy cảm; lời khai 115 ca, 40 mutant, 119 AST hoặc đóng finding lượt 15 vượt phép đo.

Lệnh: `python3 audit_artifacts.py`

Output thật (mã thoát 0), lưu ở `review-evidence/artifacts.txt`:

```text
Review file count: 105 ; scanner skipped: [] ; max bytes: 110568
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

Kết luận: KHÔNG PHẢI LỖI — đủ 105 tệp được quét, không hit secret/credential/home path; log lưu có 115 ca Boolean true và 17+23=40 mutant bị bắt bằng ca fail không phải parser. 119 AST tách rõ 4 ca không đăng ký. Đây là readback lịch sử, không phải chạy lại Windows hay xác thực thân mutant đã OMITTED.

## Hướng 10 — Tách biên nhận mục tiêu khỏi object thiếu của master

Giả thuyết: rc2 của cổng toàn cây có thể do receipt mới chứ không phải dữ liệu nền thiếu trong bundle.

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

Kết luận: KHÔNG PHẢI LỖI của diff — receipt mục tiêu qua riêng schema/Git/history/surface; receipt gây thiếu object và validator bằng byte origin/master. KHÔNG ĐO ĐƯỢC vẫn là kết quả cổng toàn cây (rc2); không nâng thành pass và không gọi mạng để bổ sung object.

## Hướng 11 — Diff lịch sử, dòng README và caveat của receipt

Giả thuyết: Diff/numstat lưu sai gốc; dòng README làm mất caveat hoặc chép sai số verdict/run.

Lệnh: `python3 audit_claims.py`

Output thật (mã thoát 0), lưu ở `review-evidence/receipt-claims.txt`:

```text
Stored diff.patch and numstat.txt match Git b0814f4 -> 210ab81 exactly; only 3 ops/vm files
Receipt result counts, run version/duration, README entry and all 5 caveats match their retained sources
Bookkeeping quantitative clauses: PASS; historical retention separately checked by audit_storage.py
```

Kết luận: KHÔNG PHẢI LỖI — diff.patch/numstat đúng từng byte b0814f4 → 210ab81; 3 tệp ops/vm; 0/0/0/0, phiên bản/thời lượng run, hàng README và đủ 5 caveat khớp nguồn. Tập HINT/verdict đã đo riêng tại Hướng 2.

## Hướng 12 — Nhãn nguồn toàn văn ngoài các trường YAML measured

Giả thuyết: Header của hồ sơ vẫn nhận mọi nguồn measured là readback thô dù nguồn thread tự khai là bản trích MCP.

Lệnh: `python3 audit_provenance_label.py`

Output thật (mã thoát 0), lưu ở `review-evidence/provenance-label.txt`:

```text
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:9: # NHAN: measured = do lai trong phien ghi so tu readback tho (ten tep ghi kem); thuat_lai = loi khai cua phien, KHONG tai
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:11: # Readback tho: ops/land/pr1065-vm-cap-nhat-cong-cu-provenance/ (SHA256SUMS.txt). Moi phep do REST: GET
Measured clause cites: readback-review-threads-1065.json
Retained source declaration: Trich cac truong dinh danh/trang thai tu phan hoi MCP (than comment luoc bo); totalCount=1, hasNextPage=false.
Retained source observed_at: 2026-10-31T14:07:20Z
Thread resolved fact remains supported; raw MCP response is not retained by this extracted JSON
Countercheck current global raw-source definition: CONTRADICTS retained extraction note
Countercheck narrowed header in memory: no raw-source overclaim; YAML semantic fields unchanged
Scope: comments/header were excluded by the 15-scalar YAML walk; this check reads the entire source text
PROVENANCE FORMAT LABEL: 1 overclaim class; raw/extract distinction, not absence of thread evidence or an assertion that is_resolved is false
```

Kết luận: LỖI — định nghĩa measured ở header nhận nguồn thô nhưng lời khai trạng thái thread dùng bản TRÍCH đã lược thân comment. Việc giữ metadata đúng trong JSON không làm lời khai toàn cục trong hồ sơ thành đúng. Đây là lớp provenance mới; không phủ nhận phép đóng finding lượt 17 và không kết luận trạng thái thread sai.

### khai-readback-tho-cho-ban-trich  [P2]  Định nghĩa nguồn measured nhận bản trích MCP thành readback thô

**TỆP/DÒNG:** `cay-kho/ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:9` (định nghĩa nhãn `measured`); dòng 11 tiếp tục gọi thư mục provenance là `Readback tho`. Đối chiếu lời khai `review.codex_connector.do_duoc` ở dòng 127–130 và `cay-kho/ops/land/pr1065-vm-cap-nhat-cong-cu-provenance/readback-review-threads-1065.json:4`.

**VẤN ĐỀ:** Header tuyên bố `measured = do lai trong phien ghi so tu readback tho (ten tep ghi kem)`. Nhưng lời khai measured về thread dẫn `readback-review-threads-1065.json`, tự mô tả `Trich cac truong dinh danh/trang thai tu phan hoi MCP (than comment luoc bo)`. Tệp này giữ được ID, trạng thái và quan hệ comment để đóng finding lượt 17, nhưng không giữ phản hồi MCP thô. Định nghĩa nguồn của hồ sơ vì thế rộng hơn hiện vật thật: người đọc nhận lời khai nguồn thô dù chỉ có bản trích. Đây là khai sai mức bằng chứng (P2 theo prompt), không phải lỗi dữ liệu `is_resolved`, không phải khẳng định thread chưa resolve. Hash khớp chỉ bảo toàn byte của bản trích, không nâng nó thành phản hồi thô.

**ĐÃ THỬ NGHIỆM:** `python3 audit_provenance_label.py`, rc=0, output `review-evidence/provenance-label.txt`: đọc header và lời khai bằng toàn văn + YAML; xác minh tệp trích có băm manifest đúng và `is_resolved=true`; chỉ ra đồng thời định nghĩa nguồn thô và khai báo lược thân comment. Phản chứng thu hẹp hai câu header trong bộ nhớ bỏ mâu thuẫn, trong khi `yaml.safe_load` của cả hồ sơ giữ nguyên. Không ghi vào `cay-kho/`. Cổng nguồn land vẫn rc=0 vì không kiểm ngữ nghĩa comment. Phép duyệt 15 scalar YAML ở Hướng 7 không đọc comment/header; kết quả pass ở hướng ấy chỉ áp cho các trường dữ liệu đã liệt kê, không phủ định lỗi toàn văn này.

**ĐỘ TIN:** Cao về mâu thuẫn giữa lời khai và hiện vật giữ tại exact head; không đo phản hồi MCP nguyên gốc hoặc trạng thái GitHub live.

**GỢI Ý VÁ:**

- **Vá ở đâu:** Header dòng 9–12 của hồ sơ land, nơi định nghĩa nguồn cho mọi nhãn `measured`; bổ sung ngoại lệ ngay nguồn thread ở dòng 130 nếu cần để người đọc không phải suy từ JSON. Không sửa trạng thái thread đã có bằng chứng.
- **Vá thế nào:** Định nghĩa `measured` là đối chiếu tệp nguồn được dẫn với mức bằng chứng đúng theo từng tệp; phân biệt readback REST được giữ và bản trích trường MCP. Nêu bản trích thread quan sát lúc `2026-10-31T14:07:20Z`, phản hồi MCP thô không giữ. Đây là đường vá rẻ nhất; lưu thêm phản hồi thô có nguồn và băm chỉ cần nếu thực sự muốn tiếp tục nhận là nguồn thô.
- **Ca test khóa nó:** Kiểm toàn văn cả header và trường dữ liệu: với nguồn tự khai `Trich ... than comment luoc bo`, không cho định nghĩa chung nhận mọi nguồn measured là thô. `audit_provenance_label.py` đã chạy cặp đối chiếu câu hiện tại / câu thu hẹp trong bộ nhớ; giữ lại ID, `is_resolved`, finding binding và băm khớp làm bằng chứng dương. Đột biến đưa lại định nghĩa nguồn thô phải bị báo sai mức bằng chứng dù các trường thread vẫn khớp.
- **Rủi ro bản vá:** Thu hẹp lời khai nguồn không được đổi `is_resolved=true` thành chưa resolve hoặc hạ toàn bộ dữ liệu REST thành không đo được. Không nhận hash của bản trích làm hash phản hồi thô; không nhận thời điểm quan sát 14:07:20Z thành thời điểm thread được resolve.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp finding | Lượt / SHA nguồn | Phân loại tại head lượt 19 | Bằng chứng tự đo |
|---|---|---|---|
| `khai-luu-hint-khong-du-hien-vat` | Lượt 18 / `958ca60684f38305a9cf9276af3b99c73940ea97` | **ĐÃ VÁ THẬT** | Hướng 2: đủ 15 verdict + 15 HINT, Git/byte/manifest khớp; patch 1–2 đọc được; lời khai lưu trữ đúng tập tệp hiện tại. |
| `khai-resolved-khong-co-readback` | Lượt 17 / `4b3f07ed64e45e65cc4645b8601c666bafed8bd0` | **ĐÃ VÁ THẬT**, vẫn đóng về dữ liệu trạng thái | Hướng 3: thread ID, `is_resolved=true`, quan hệ finding 4430537534/reply 4430544980 và băm đúng; có bản trích nguồn. |
| `khai-readback-tho-cho-ban-trich` | Phát hiện mới lượt 19 / `43372542cc2480f3b4f8228d824afd509b1054cc` | **Lớp mới còn mở, 1 biểu hiện P2** | Hướng 12: định nghĩa toàn cục nguồn thô không khớp định dạng bản trích được giữ. Không tái mở hai lớp cũ. |

Chuyển tiếp lượt 18 → 19: U = {`khai-luu-hint-khong-du-hien-vat`}, F = U, tỷ lệ đóng lớp cũ 1/1 = 100%. Một lớp mới được báo riêng, không đưa vào tử số F. Lượt 16 approve tại `210ab81` có 0 finding; ops/vm giữ nguyên byte nhưng review cũ không tự có hiệu lực với head mới. Không có dấu hiệu bản thêm HINT làm đổi mã sản phẩm hoặc mất hàng master.

## Bảng lớp finding còn mở

| Slug | Nguyên nhân | Biểu hiện | Mức | Điều kiện đóng |
|---|---|---|---|---|
| `khai-readback-tho-cho-ban-trich` | Định nghĩa toàn cục không phản ánh mức nguồn sau khi thêm bản trích MCP | 1: header hồ sơ land dòng 9–11 áp cho lời khai trạng thái thread | P2 | Thu hẹp định nghĩa/khai ngoại lệ bản trích đúng hiện vật; giữ bằng chứng trạng thái và manifest. |

Không phát hiện thêm số liệu `41 đột biến` hoặc lời nhận đã `landed`: hiện vật lượt 16 lưu 40 mutant (17+23), 115 ca Linux thực thi; 119 ca AST và 4 ca không đăng ký được phân biệt. Hồ sơ vẫn `landed: false`, Checkout/Gate output CI còn `not_measured`, Windows và lời duyệt human chỉ thuật lại. Việc nhận dạng provider/model của executor không được coi là phép đo máy độc lập; receipt ghi rõ caveat này.

## Hướng 13 — Kiểm cuối SHA/tree/index, snapshot và số finding

Giả thuyết: Head hoặc dữ liệu checkout đổi trong lúc đo; verdict đếm nhầm finding cũ, giới hạn nền hay lớp mới.

Lệnh: `python3 audit_final.py`

Output thật (mã thoát 0), lưu ở `review-evidence/final-snapshot.txt`:

```text
All checkout files before/after: 9502 9502
Added: [] ; removed: [] ; changed bytes/mode: []
HEAD: 43372542cc2480f3b4f8228d824afd509b1054cc ; tree: ecebb7d55a972c13b9f58ed38d96eda55c5909d7 ; origin/master: a253c169ed79617b8d1a4754867c336ac72c72c5
Index SHA256 unchanged: 78406676d779f9de5cdfa32a21a267e36e13d55c29fd458381e024067e2e5889 ; status tracked/untracked/ignored and index/worktree diffs empty
Open findings: ['### khai-readback-tho-cho-ban-trich  [P2]  Định nghĩa nguồn measured nhận bản trích MCP thành readback thô']
Classification: 0 P0, 0 P1, 1 P2, 0 P3; round17 and round18 findings closed; one new provenance-format class
FINAL SNAPSHOT: PASS; no observed file/index/head delta. Endpoint snapshots cannot prove absence of transient write-and-restore; read-only was an instruction under workspace-write.
```

Kết luận: KHÔNG PHẢI LỖI về toàn vẹn checkout: 9502 tệp và index/SHA/tree/master bằng snapshot đầu; trạng thái tracked/untracked/ignored sạch. Có đúng 1 finding P2 mới; hai lớp cũ đã đóng. Snapshot chỉ chứng minh hai mốc, không chứng minh không từng ghi rồi hoàn nguyên; read-only là chỉ thị trong sandbox workspace-write.

## Trạng thái phép đo và giới hạn

- **passed:** exact head `43372542cc2480f3b4f8228d824afd509b1054cc`, tree `ecebb7d55a972c13b9f58ed38d96eda55c5909d7`; ops/vm bằng byte `210ab81`; 128 đường dẫn đổi (ops/vm 3, ops/land 17, ops/reviews 108) đều đúng phạm vi; cả bốn merge bảo toàn hàng và dòng có nội dung README của master, không xóa tệp master; 15+15 hiện vật lịch sử; manifest review 104/104 và provenance 15/15; verdict 26.427 byte/SHA256, reviewed SHA/tree/base, blob cbe05f2 và ancestry; kiểm riêng receipt mục tiêu; cổng nguồn land 1 ĐẠT/0 vi phạm; đối chiếu 15 trường measured; quét đủ 105/105 tệp review, không hit mẫu secret/credential/đường dẫn home; snapshot đầu/cuối bằng nhau.
- **failed (nội dung):** 1 lớp P2 `khai-readback-tho-cho-ban-trich`: header hồ sơ nhận nguồn measured là thô, trong khi trạng thái thread dựa trên bản trích đã lược thân comment. Các trường thread và số liệu vẫn khớp; không có P0/P1/P3 mới được xác lập.
- **not_measured:** cổng biên nhận v2 toàn cây rc=2, 268 ĐẠT v2 / 11 miễn trừ legacy / 42 nợ / 0 vi phạm / 3 thông báo KHÔNG ĐO ĐƯỢC. Cả ba do receipt nền `lease-publish-windows-do-review-r1-codex.receipt.yaml` thiếu object `4bc94325e647ee5e32373f3af30b8f83b98a90fa`. Đã đo receipt và validator bằng byte origin/master và tái lập thiếu object từ baseline; không coi cổng này là pass hoặc finding của PR.
- **not_measured / not_run:** GitHub live, phản hồi MCP thô trước khi trích thread, nguồn sandbox gốc của HINT lượt 1–2, stdout/stderr gốc lượt 16 không giữ, thân 40 mutant bị OMITTED, Windows native/NTFS/COM/MSI/Task Scheduler, CI mới trên head 43372542. CI 39/39 trên 716804b chỉ là thuật lại trong prompt, không phải phép đo của lượt này. Không chạy mạng/fetch để bù nguồn thiếu.
- **not_run có điều kiện:** không review lại mã hoặc chạy PowerShell vì điều kiện nhiệm vụ 4 không kích hoạt (ops/vm bất biến). Các con số 115/119/40 được đọc lại từ hiện vật lịch sử; không nhận thành test mới.

Reviewer thực tế theo launcher `runs/c5d9680a/run.json`: `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`, run `c5d9680afe3a43b18ad2364c5b803632`. Run còn `dang_chay` lúc quan sát; không tự nhận terminal rc/model/effort chưa có receipt máy hoàn tất. Session/context review này độc lập với executor Claude, không fork context executor. Sandbox thực tế `workspace-write`; checkout read-only theo chỉ thị, không phải OS-enforced. Script và output mới đều nằm ngoài `cay-kho/`; không sửa cây sản phẩm, không push/merge, không gọi mạng. Một số script đo được đọc rồi kế thừa từ lượt 18 và cập nhật tham số head/run hoặc tách phần kiểm còn hiệu lực; mọi output trong verdict này là lần chạy mới tại head lượt 19.

Quyết định: **changes_requested** cho exact head đã nêu, do 1 P2 về mức nguồn bằng chứng. Hai finding lượt 17–18 đã vá thật. Không cấp approval merge/land, không nâng receipt lịch sử hoặc kết quả CI của SHA khác thành evidence cho head hiện tại.

## Hướng 14 — Kiểm định dạng và tham chiếu bằng chứng cuối

Giả thuyết: Header, exact SHA, tổng severity, số heading finding hoặc đường dẫn output cuối bị lệch.

Lệnh: `python3 audit_verdict.py`

Output thật (mã thoát 0), lưu ở `review-evidence/verdict-format.txt`:

```text
Final header/SHA/result MATCH; finding count: 0 P0 / 0 P1 / 1 P2 / 0 P3
All 13 prior output references exist; scanner empty-output convention verified; receipt gate remains NOT_MEASURED; land gate has positive marker
Finding has location/problem/experiment/confidence/remediation; both previous findings explicitly compared; no current-head CI/Windows pass claimed
```

Kết luận: KHÔNG PHẢI LỖI — header/40-hex reviewed_sha và 0/0/1/0 khớp đúng một heading P2; các output tham chiếu tồn tại; phân biệt rc2 biên nhận và marker dương land, cùng quy ước scanner stdout rỗng. Finding đủ vị trí, vấn đề, phép thử, độ tin và bốn phần gợi ý vá.
