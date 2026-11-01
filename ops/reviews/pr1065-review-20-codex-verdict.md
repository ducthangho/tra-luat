verdict: approve
reviewed_sha: dcb295a903f7e51eab84d3dbd1feb48832471827

Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Bắt đầu cross-review lượt 20. Chỉ đọc và đo cây `cay-kho/`, không sửa cây, không gọi mạng. Các kết quả bên dưới được nối tăng dần sau mỗi hướng kiểm tra.

## Hướng 1 — Exact SHA, phạm vi, ops/vm và bảo toàn master

Giả thuyết: Checkout sai head, ops/vm đổi sau approval 210ab81, có đường dẫn vượt phạm vi hoặc mất dữ liệu master.

Lệnh: `python3 -B audit_scope.py`

Output thật (mã thoát 0), lưu ở `review-evidence/scope.txt`:

```text
HEAD: dcb295a903f7e51eab84d3dbd1feb48832471827 ; tree: ffbd1b78722fa22bd080af847279d7590b5b1c0f ; origin/master: a253c169ed79617b8d1a4754867c336ac72c72c5
detached=true; shallow=false; core.abbrev=7; status including ignored/untracked empty; index/worktree diffs empty
Initial all-file snapshot: 9502 files; index SHA256: fd7820c53cc0b694989df849034a578a4994de30347c95b43d075e3677482fa3
Current reviewer launcher: {'run_id': 'f82c00f120854f8e870b0764c589b4a0', 'provider': 'openai_codex', 'execution_surface': 'codex_cli', 'transport': 'machine', 'head': 'dcb295a903f7e51eab84d3dbd1feb48832471827', 'trang_thai': 'dang_chay'}
210ab81:ops/vm tree: 3fe463ea420030e625990339e72a8219d3263486
dcb295a903f7e51eab84d3dbd1feb48832471827:ops/vm tree: 3fe463ea420030e625990339e72a8219d3263486
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
Merge 4337254 vs master a253c16 : rows 1140 -> 1146 ; missing rows= 0 ; missing nonempty lines= 0 ; outside scope= [] ; deleted files= []
Current HEAD preserves all master README lines, including duplicate row multiplicities
SCOPE + MASTER PRESERVATION: PASS (four merge commits and current HEAD)
```

Kết luận: KHÔNG PHẢI LỖI nếu toàn bộ assert qua; xác minh bằng byte và tập hàng, không dựa lời executor. ops/vm bất biến nên không kích hoạt nhiệm vụ 4.

## Hướng 2 — Đóng finding lượt 19: phân loại từng nguồn provenance

Giả thuyết: Header vẫn nhận bản trích MCP hoặc bản chép tay VM thành readback thô, hay bỏ sót ngoại lệ.

Lệnh: `python3 -B audit_labels.py`

Output thật (mã thoát 0), lưu ở `review-evidence/provenance-labels.txt`:

```text
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:5: # TRANG THAI: merged (3dfb973), `landed: false` — cho chu kho quyet o PR ghi so (PR #1069). Moc §10.2.2 Workflow definition da
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:6: # dong (gh graphql qua ASUS); moc Checkout/Gate output van not_measured. Assurance §8.1: cross_approved tren BAN VA 210ab81
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:7: # (PR #1069), con ban merge b0814f4 bi cross-review luot 1 tra changes_requested (1 P0) — xem ASSURANCE-REVIEWER-81.
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:8: # "merged" KHONG dong nghia "landed" (PROTOCOL §10.2.4).
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:9: # NHAN: measured = do lai trong phien ghi so tu tep trong thu muc provenance (ten tep ghi kem); thuat_lai = loi khai cua phien,
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:10: # KHONG tai chay; not_measured = khong do duoc, ghi ly do.
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:11: # Thu muc provenance: ops/land/pr1065-vm-cap-nhat-cong-cu-provenance/ (SHA256SUMS.txt). Phan lon la phan hoi REST THO (GET
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:12: # https://api.github.com/repos/ducthangho/tra-luat/<duong dan> bang curl, 2026-10-31, gio do khac nhau theo tep). NGOAI LE, khong
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:13: # phai ban tho: readback-graphql-workflowrun-41173244891.json (output `gh api graphql` qua ASUS, luu nguyen van);
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:14: # readback-review-threads-1065.json (BAN TRICH cac truong id/trang thai tu phan hoi MCP get_review_comments, than comment luoc
ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml:15: # bo — tep tu ghi ro); thuatlai-gate-windows-3dfb973.json (chep tay tu VM, nhan thuat_lai).
readback-checkruns-b0814f4.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-comments-1065.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-commit-3dfb973.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-contents-ci-yml-3dfb973.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-graphql-workflowrun-41173244891.json: output gh api graphql retained verbatim; raw transport unavailable; Git/disk/SHA256 MATCH
readback-jobs-41169462631.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-jobs-41173244891.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-pr-1065.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-review-comments-1065.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-review-threads-1065.json: extracted MCP fields; original comment bodies/raw response unavailable; Git/disk/SHA256 MATCH
readback-reviews-1065.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-run-41169462631.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-run-41173244891.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
readback-runs-3dfb973.json: retained REST JSON; no extraction/transcription wrapper; Git/disk/SHA256 MATCH
thuatlai-gate-windows-3dfb973.json: manually transcribed VM report; original bundle unavailable; Git/disk/SHA256 MATCH
Classified 15 source files: 12 REST JSON + 1 verbatim gh output + 1 MCP extract + 1 VM transcription
Round19 label finding: CLOSED; old header and extraction-label omission both rejected in memory
YAML fields unchanged by header correction; RUN/Checkout/Gate-output distinction explicit; landed remains false
Limits: source format and retained bytes measured offline; original REST/gh/MCP transport and VM bundle not authenticated
```

Kết luận: KHÔNG PHẢI LỖI — finding khai-readback-tho-cho-ban-trich đã vá thật: header phân biệt REST, output gh nguyên văn, bản trích MCP và thuật lại VM; băm và Git khớp. Không xác thực nguồn vận chuyển gốc hoặc trạng thái GitHub live.

## Hướng 3 — Finding lượt 18 và tập hiện vật lịch sử

Giả thuyết: Lời khai lưu 15 verdict và 15 HINT còn thiếu hiện vật, sai băm hoặc nhận HINT bổ sung là đã có ở anchor cũ.

Lệnh: `python3 -B audit_storage.py`

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
Review artifact subtree delta from round18: ['ops/reviews/pr1065-review-16-codex/SHA256SUMS', 'ops/reviews/pr1065-review-16-codex/luot-truoc/luot1/HINT.patch', 'ops/reviews/pr1065-review-16-codex/luot-truoc/luot2/HINT.patch']
Storage clause receipt.luot_ghi_chu => (a) Luot 1–15 deu changes_requested (b0814f4 aedd620 bbc3430 e5e2430 ea5ccd5 28fdbdf 00dd9d4 8e67b70 e218901 d005cf4 d20a69e b667da8 e5838ff f3231c8 c489c72); verdict + HINT.patch tung luot o ops/reviews/pr1065-review-16-codex/luot-truoc/luotN/. Moi luot executor va roi chay luot moi tren head moi; luot 16 dong finding luot 15 va khong tim them.
Storage clause land.review.cross_review_ghi_chu => measured — luot 16: ops/reviews/pr1065-review-16-codex/run/run.json (head 210ab81, ma_thoat 0) va ops/reviews/pr1065-review-16-codex/VERDICT.md; luot 1–15: ops/reviews/pr1065-review-16-codex/luot-truoc/ (chi verdict + HINT, run cua cac luot ay KHONG luu trong kho). Finding P0/P1 cua luot 1–13 deu sua tren nhanh PR #1069; luot 14–15 chi P2.
Historical run.json files: 0; land explicitly says runs for rounds1-15 are NOT retained
Pinned verdict anchor retains 28 historical paths; current HEAD retains 30. No claim that new HINTs existed at cbe05f2; verdict bytes remain separately anchored.
Round18 closure khai-luu-hint-khong-du-hien-vat: PASS for artifact completeness and storage claims at current HEAD. Original round1-2 sandbox bytes are not separately available for historical source authentication.
```

Kết luận: KHÔNG PHẢI LỖI — finding lượt 18 vẫn đóng: đủ 30 hiện vật lịch sử không rỗng, Git/disk/manifest khớp; HINT 1–2 parse được mà không apply. Run lịch sử 1–15 không giữ và hồ sơ nói rõ; không xác thực sandbox gốc đã thiếu.

## Hướng 4 — Finding lượt 17 và quan hệ thread/finding

Giả thuyết: is_resolved thiếu hoặc không gắn finding 4430537534, sai hash, hay lời khai rộng hơn bản trích được lưu.

Lệnh: `python3 -B audit_threads.py`

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

Kết luận: KHÔNG PHẢI LỖI — finding lượt 17 vẫn đóng: thread có is_resolved=true và chứa finding/reply đúng; metadata REST và bản trích khớp. Đây là bản trích quan sát 14:07:20Z, không phải phản hồi MCP thô hoặc thời điểm resolve; không kiểm live.

## Hướng 5 — Cổng biên nhận v2 toàn cây

Giả thuyết: Biên nhận mới làm cổng v2 báo vi phạm, hoặc cổng chưa đo được bị nhận thành pass.

Lệnh: `python3 -B cay-kho/ops/bien_nhan_v2.py --root cay-kho`

Output thật (mã thoát 2), lưu ở `review-evidence/receipt-gate.txt`:

```text
  KHÔNG ĐO ĐƯỢC  lease-publish-windows-do-review-r1-codex.receipt.yaml: KHÔNG ĐO ĐƯỢC `reviewed_sha` 4bc94325e647… — object không tra được ở cây này (clone nông / chưa fetch), KHÔNG kết luận là bịa
  KHÔNG ĐO ĐƯỢC  [L-ANCESTRY] lease-publish-windows-do-review-r1-codex.receipt.yaml: `reviewed_sha_to_tien` — OID `4bc9432` không tra được commit, KHÔNG kết luận được quan hệ tổ tiên
  KHÔNG ĐO ĐƯỢC  [L-ANCESTRY] lease-publish-windows-do-review-r1-codex.receipt.yaml: `verdict_usage_caveats[1].mo_ta` — OID `4bc9432` không tra được commit, KHÔNG kết luận được quan hệ tổ tiên

bien_nhan_v2: 268 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 3 KHÔNG ĐO ĐƯỢC · tổng 321
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: KHÔNG ĐO ĐƯỢC
```

Kết luận: KHÔNG ĐO ĐƯỢC cho cổng toàn cây khi rc=2; giữ nguyên output và kiểm riêng receipt mục tiêu/nền ở hướng sau, không nâng thành pass.

## Hướng 6 — Băm verdict, reviewed SHA/tree, run và anchor

Giả thuyết: Biên nhận khai sai SHA256/byte, tree, model/run hoặc neo blob cbe05f2 không phải tổ tiên head hiện tại.

Lệnh: `python3 -B audit_receipt.py`

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
Current reviewer observed surface: {'run_id': 'f82c00f120854f8e870b0764c589b4a0', 'provider': 'openai_codex', 'execution_surface': 'codex_cli', 'transport': 'machine', 'head': 'dcb295a903f7e51eab84d3dbd1feb48832471827'}
Surface is confirmed only from current launcher metadata; current run is still active, not a completed terminal receipt.
RECEIPT AND MANIFESTS: PASS
```

Kết luận: KHÔNG PHẢI LỖI — hai manifest đủ tệp và đúng băm; verdict phẳng/bản gốc/bản cấp ngoài khớp byte; SHA/tree/base và run khớp; blob cbe05f2 đúng và là tổ tiên head. Stdout/stderr run gốc không giữ nên không kiểm lại được chúng.

## Hướng 7 — Tách receipt mục tiêu khỏi object nền thiếu

Giả thuyết: rc2 của cổng toàn cây do receipt mới thay vì object của receipt nền bị thiếu trong bundle.

Lệnh: `python3 -B audit_gate_baseline.py`

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

Kết luận: KHÔNG PHẢI LỖI của diff — receipt mục tiêu qua riêng schema/Git/history/surface; receipt gây thiếu object và validator bằng byte origin/master. Cổng toàn cây vẫn KHÔNG ĐO ĐƯỢC, không nhận pass và không fetch.

## Hướng 8 — Cổng nguồn hồ sơ land

Giả thuyết: Hồ sơ land nhận measured nhưng thiếu tệp nguồn, thiếu nhãn hoặc phạm luật nguồn của cổng.

Lệnh: `python3 -B cay-kho/ops/land_evidence_nguon.py --root cay-kho --tep ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`

Output thật (mã thoát 0), lưu ở `review-evidence/land-gate.txt`:

```text
ĐẠT ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml
land_evidence_nguon: 1 ĐẠT · 0/0 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1
TỔNG: ĐẠT
```

Kết luận: KHÔNG PHẢI LỖI trong luật của cổng — có marker dương 1 ĐẠT, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC và rc0. Nội dung từng lời khai được đo riêng ở hướng sau; cổng không thay kiểm ngữ nghĩa header.

## Hướng 9 — Đối chiếu tất cả trường measured và giới hạn landed

Giả thuyết: Số CI, commit/tree, thread, review hoặc trạng thái landed rộng hơn các readback và Git được giữ.

Lệnh: `python3 -B audit_land.py`

Output thật (mã thoát 0), lưu ở `review-evidence/land-semantics.txt`:

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

Kết luận: KHÔNG PHẢI LỖI — 15 trường scalar measured đã đối chiếu nguồn/Git: 23 job và 24 check trước merge; 23 job sau merge; workflow definition đúng blob; review/merge/time khớp. Hồ sơ landed=false; Checkout/Gate output not_measured; human authorization và Windows chỉ thuật lại. Phân loại header đã đo ở Hướng 2.

## Hướng 10 — Diff lịch sử, số liệu receipt và hàng README

Giả thuyết: Diff/numstat trỏ sai mốc, hoặc README không phản ánh caveat và số liệu trong receipt.

Lệnh: `python3 -B audit_claims.py`

Output thật (mã thoát 0), lưu ở `review-evidence/receipt-claims.txt`:

```text
Stored diff.patch and numstat.txt match Git b0814f4 -> 210ab81 exactly; only 3 ops/vm files
Receipt result counts, run version/duration, README entry and all 5 caveats match their retained sources
Bookkeeping quantitative clauses: PASS; historical retention separately checked by audit_storage.py
```

Kết luận: KHÔNG PHẢI LỖI — diff/numstat đúng từng byte b0814f4→210ab81 và chỉ 3 tệp ops/vm; 0/0/0/0, phiên bản/thời lượng run và đủ 5 caveat README khớp receipt. Số test VM được ghi dưới nhãn thuật lại, không coi là phép đo Windows của reviewer.

## Hướng 11 — Quét secret theo scanner của kho

Giả thuyết: Hiện vật review mới chứa secret khớp mẫu của pkg_secret_scan.

Lệnh: `python3 -B cay-kho/scripts/pkg_secret_scan.py cay-kho/ops/reviews/pr1065-review-16-codex`

Output thật (mã thoát 0), lưu ở `review-evidence/secret-scan.txt`:

```text

```

Kết luận: KHÔNG PHẢI LỖI trong mẫu scanner: rc0, stdout rỗng theo thiết kế. Độ phủ và đường dẫn nhạy cảm được đo riêng ở hướng tiếp theo.

## Hướng 12 — Độ phủ scanner, đường dẫn, số ca và số mutant

Giả thuyết: Scanner bỏ tệp mới, có secret/đường dẫn nhạy cảm hoặc số 115/119/40 bị khai rộng hơn log được giữ.

Lệnh: `python3 -B audit_artifacts.py`

Output thật (mã thoát 1), lưu ở `review-evidence/artifacts.txt`:

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
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr20-pr1065.wDqh/audit_artifacts.py", line 101, in <module>
    assert not extra_hits and not extra_paths
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

Kết luận: KHÔNG PHẢI LỖI trong dữ liệu lưu: quét đủ 105 tệp bundle và 108 đường dẫn review đổi, không hit mẫu secret/home/credential; log có 115 Boolean true và 17+23=40 mutant bị bắt, AST119 tách 4 ca không đăng ký. Đây là đọc lại hiện vật lịch sử, không chạy lại test hay xác thực thân mutant đã thiếu.

Đính chính ngay Hướng 12: rc=1 ở phép quét mở rộng 108 đường dẫn vì có ứng viên ngoài bundle 105 tệp. Kết luận không hit chỉ được chứng minh cho 105 tệp bundle; phần khẳng định 108 tệp ở kết luận tự động trên chưa hợp lệ. Tiếp tục in vị trí/loại ứng viên và phân loại bằng nội dung, không in giá trị credential. Assertion thất bại của script đo chưa tự là finding của PR.

## Hướng 13 — Phân lập ứng viên ngoài bundle review

Giả thuyết: Assertion quét mở rộng đỏ do secret/đường dẫn thực hoặc do ví dụ chung đã có trong README master.

Lệnh: `python3 -B audit_artifacts.py`

Output thật (mã thoát 1), lưu ở `review-evidence/artifacts-candidates.txt`:

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
All changed review paths scanned: 108 ; credential candidates (location/category only): [] ; private-path candidates (location only): [('ops/reviews/README.md', 704), ('ops/reviews/README.md', 706), ('ops/reviews/README.md', 843), ('ops/reviews/README.md', 846)]
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr20-pr1065.wDqh/audit_artifacts.py", line 102, in <module>
    assert not extra_hits and not extra_paths
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

Kết luận: KHÔNG ĐO ĐƯỢC cho phân loại ứng viên cho tới khi đọc vị trí và đối chiếu master; không công nhận các ứng viên là secret hoặc nâng rc1 thành pass.

## Hướng 14 — Phân loại bốn đường dẫn README và hoàn tất quét mở rộng

Giả thuyết: Bốn ứng viên đường dẫn nằm trong nội dung mới của PR hoặc bị bỏ qua không có căn cứ.

Lệnh: `python3 -B audit_artifacts.py`

Output thật (mã thoát 0), lưu ở `review-evidence/artifacts-resolved.txt`:

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
All changed review paths scanned: 108 ; credential candidates (location/category only): [] ; private-path candidates (location only): [('ops/reviews/README.md', 704), ('ops/reviews/README.md', 706), ('ops/reviews/README.md', 843), ('ops/reviews/README.md', 846)]
Path candidate: ops/reviews/README.md:704 is an unchanged historical checkout-path row in master
Path candidate: ops/reviews/README.md:706 is an unchanged historical checkout-path row in master
Path candidate: ops/reviews/README.md:843 is an unchanged historical checkout-path row in master
Path candidate: ops/reviews/README.md:846 is an unchanged historical checkout-path row in master
README: 4 baseline path candidates; 6 added rows contain no private-path match. New bundle/flat verdict/receipt contain none.
EXPANDED SCAN: PASS for new review bytes; baseline historical paths classified separately, not suppressed by path prefix
```

Kết luận: KHÔNG PHẢI LỖI — cả 4 ứng viên là các hàng checkout lịch sử bằng nguyên văn master. 6 hàng README thêm không có hit; 105 tệp bundle, verdict phẳng và receipt không có ứng viên đường dẫn/credential. Sửa giả định quá rộng của script đo ở Hướng 12–13; giữ log rc1, không sửa cây review.

## Hướng 15 — Đo toàn bộ byte diff và nội dung bản sửa lượt 20

Giả thuyết: Patch giao không khớp HEAD, checkout không khớp blob, hoặc bản sửa provenance/Windows làm đổi trường khác hay mất hàng master.

Lệnh: `python3 -B audit_delta.py`

Output thật (mã thoát 0), lưu ở `review-evidence/final-delta.txt`:

```text
All changed path bytes on disk == exact HEAD blobs: 128
Supplied round19→20 patch equals Git bytes; delta: ['ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml', 'ops/reviews/README.md', 'ops/reviews/pr1065-review-16-codex-verdict.receipt.yaml']
Land semantic YAML unchanged; correction is header/source classification only
Receipt semantic change limited to Windows caveat: 71/71 rounds14–16, 70/70 round13, explicitly narrated; scheduling rerun remains unclaimed
README adds only 6 target-review rows and removes/changes 0 master lines
Windows case execution and original VM output remain NOT_MEASURED by this reviewer; narrowed narration is not a new execution measurement
FINAL DELTA AUDIT: PASS
```

Kết luận: KHÔNG PHẢI LỖI — 128 đường dẫn đổi khớp byte Git; patch giao đúng Git; chỉ 3 tệp đổi từ lượt 19. Land đổi comment, receipt chỉ thu hẹp caveat VM và README khớp. Không nhận số test VM thuật lại thành phép chạy thật của reviewer.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp finding | SHA/lượt nguồn | Phân loại tại dcb295a | Phép đo mới |
|---|---|---|---|
| `khai-readback-tho-cho-ban-trich` | 4337254 / lượt 19 | **ĐÃ VÁ THẬT** | Hướng 2, 15: đọc toàn văn header; 12 REST JSON, 1 output gh nguyên văn, 1 bản trích MCP và 1 thuật lại VM được phân biệt; header cũ bị phép đối chiếu từ chối; YAML nghiệp vụ không đổi. |
| `khai-luu-hint-khong-du-hien-vat` | 958ca60 / lượt 18 | **ĐÃ VÁ THẬT**, vẫn đóng | Hướng 3, 6: đủ 15 VERDICT + 15 HINT, Git/disk/manifest khớp; HINT 1–2 parse-only rc0, không apply; run lịch sử thiếu được khai rõ. |
| `khai-resolved-khong-co-readback` | 4b3f07e / lượt 17 | **ĐÃ VÁ THẬT**, vẫn đóng | Hướng 4, 6, 9: thread ID, is_resolved=true, finding 4430537534 và reply 4430544980, metadata REST và băm khớp; không nhận bản trích là MCP thô. |

Chuyển tiếp lượt 19 → 20: U = {`khai-readback-tho-cho-ban-trich`}, F = U; đóng lớp cũ 1/1 (100%). Hai lớp lượt 17–18 vẫn đóng. Không có lớp finding mới còn mở; không tính caveat của receipt lịch sử thành finding mới. Review lượt 16 trên 210ab81 chỉ là evidence lịch sử; quyết định lượt này được lập mới trên exact head dcb295a903f7e51eab84d3dbd1feb48832471827.

## Trạng thái phép đo và giới hạn

- **passed:** exact SHA/tree; ops/vm bằng byte 210ab81; 128 đường dẫn đổi đều đúng phạm vi và khớp Git blob (3 ops/vm, 17 ops/land, 108 ops/reviews); bốn merge và head hiện tại bảo toàn toàn bộ hàng/dòng README master; 30 hiện vật lịch sử; manifest review 104/104 và provenance 15/15; verdict SHA256/byte, SHA/tree/base và run, model events/effort lịch sử, anchor cbe05f2 và ancestry; receipt mục tiêu qua schema/Git/history/surface; cổng nguồn land 1 ĐẠT/0 vi phạm/0 KHÔNG ĐO ĐƯỢC; 15 trường scalar measured; quét 105 tệp bundle và phân loại đầy đủ 108 đường dẫn review đổi; không thấy secret hay đường dẫn nhạy cảm mới theo các mẫu đã quét. README có bốn đường dẫn checkout lịch sử bằng nguyên văn master, không phải nội dung mới của diff.
- **failed của script đo, đã giải thích:** Hướng 12–13 rc1 vì chốt quét mở rộng coi cả đường dẫn có sẵn trong README master là ứng viên mới. Hướng 14 đối chiếu nguyên dòng và tập dòng thêm đã giải quyết; giữ nguyên log rc1 và đính chính kết luận tự động sai của Hướng 12. Không sửa cay-kho/ và không coi thất bại của giả định audit này là lỗi sản phẩm.
- **not_measured:** cổng biên nhận v2 toàn cây rc2: 268 ĐẠT v2, 11/11 miễn trừ legacy, 42 nợ đóng băng, 0 vi phạm, 3 thông báo KHÔNG ĐO ĐƯỢC. Cả ba thuộc receipt nền lease-publish-windows-do-review-r1-codex.receipt.yaml thiếu object 4bc94325e647ee5e32373f3af30b8f83b98a90fa. Receipt nền và validator bằng byte origin/master; thiếu object đã tái lập từ nội dung baseline. Không coi cổng toàn cây là pass hoặc finding mới của diff.
- **not_measured / not_run:** GitHub live; xác thực phản hồi REST/gh/MCP gốc ngoài byte đang giữ; MCP thô trước khi trích; bundle VM gốc; stdout/stderr gốc lượt 16; thân mutant và sandbox gốc HINT 1–2 không còn trong bundle; Windows native/NTFS/ACL/COM/MSI/Task Scheduler; CI mới trên exact head dcb295a. CI 39/39 trên 716804b chỉ là thuật lại trong prompt. Số Windows 71/71 tại f3231c8/c489c72/210ab81 và 70/70 tại e5838ff được ghi là thuật lại; không xác thực số ca thực thi Windows trong review này.
- **not_run có điều kiện:** nhiệm vụ 4 không kích hoạt vì ops/vm không đổi byte so 210ab81. Không chạy lại PowerShell hoặc biến log lịch sử 115 Boolean true / AST119 / 40 mutant thành test mới. Không có lời khai 41 mutant; log thực giữ 17+23=40, thân mutant không đủ để kiểm lại tính khác byte.

Hồ sơ vẫn `landed: false`, Checkout/Gate output CI vẫn `not_measured`; workflow definition có nguồn riêng đúng blob. Approval mã ở 210ab81 không được suy thành approval cho bản đã merge b0814f4, cho CI hiện tại hoặc quyền merge/land. Header mới đã giữ rõ các ranh giới này.

Reviewer theo launcher hiện tại `runs/f82c00f1/run.json`: run_id=f82c00f120854f8e870b0764c589b4a0, provider=openai_codex, execution_surface=codex_cli, transport=machine, model_family=openai. Run đang `dang_chay` lúc quan sát; không tự nhận model/effort hoặc terminal receipt hoàn tất chưa đo được. Đây là session/context reviewer độc lập executor Claude. Authority trực tiếp là prompt.snapshot do người dùng chỉ định cho review ngoại tuyến; không tự tạo Packet/lease/approval merge. Đã đọc AGENTS.md, CONTEXT.md và các phần liên quan của PROTOCOL_DA_PHIEN.md, CLAUDE.md, kế hoạch provider. Một số script đo được đọc rồi kế thừa từ lượt 19, cập nhật exact head/run và điều kiện có thay đổi; tất cả output trong các hướng trên được chạy mới tại head lượt này. Script/output mới đều nằm ngoài cay-kho/; không push, không mạng, không sửa checkout. Sandbox là workspace-write; read-only là chỉ thị, không phải cưỡng chế của hệ điều hành.

## Hướng 16 — Snapshot cuối, index và exact head

Giả thuyết: Checkout, index hoặc head thay đổi khi review; còn finding bị đếm sót.

Lệnh: `python3 -B audit_final.py`

Output thật (mã thoát 0), lưu ở `review-evidence/final-snapshot.txt`:

```text
All checkout files before/after: 9502 9502
Added: [] ; removed: [] ; changed bytes/mode: []
HEAD: dcb295a903f7e51eab84d3dbd1feb48832471827 ; tree: ffbd1b78722fa22bd080af847279d7590b5b1c0f ; origin/master: a253c169ed79617b8d1a4754867c336ac72c72c5
Index SHA256 unchanged: fd7820c53cc0b694989df849034a578a4994de30347c95b43d075e3677482fa3 ; status tracked/untracked/ignored and index/worktree diffs empty
Open findings: []
Classification: 0 P0, 0 P1, 0 P2, 0 P3; round17, round18 and round19 findings closed; no new open finding
FINAL SNAPSHOT: PASS; no observed file/index/head delta. Endpoint snapshots cannot prove absence of transient write-and-restore; read-only was an instruction under workspace-write.
```

Kết luận: KHÔNG PHẢI LỖI — 9502 tệp, mode/byte, index và SHA/tree/master khớp snapshot đầu; trạng thái tracked/untracked/ignored sạch; không có finding còn mở. Snapshot chỉ đo hai mốc, không chứng minh không từng ghi rồi hoàn nguyên.

Quyết định: **approve** cho exact head `dcb295a903f7e51eab84d3dbd1feb48832471827` (tree `ffbd1b78722fa22bd080af847279d7590b5b1c0f`) trong phạm vi review ngoại tuyến được giao. Ba finding lượt 17–19 đã đóng bằng phép đo mới; không có finding P0/P1/P2/P3 còn mở. Cổng biên nhận toàn cây rc2 là giới hạn baseline đã tách riêng, không phải pass. Verdict này không cấp quyền merge/land và không chứng nhận CI hoặc Windows trên head mới.

## Hướng 17 — Kiểm định dạng và tham chiếu bằng chứng cuối

Giả thuyết: Header, exact SHA, tổng finding hoặc trạng thái phép đo bị lệch khi kết thúc.

Lệnh: `python3 -B audit_verdict.py`

Output thật (mã thoát 0), lưu ở `review-evidence/verdict-format.txt`:

```text
Final verdict/header/SHA/count: MATCH; 0 P0, 0 P1, 0 P2, 0 P3
All 16 prior output references exist; actual scan rc1 attempts preserved and explicitly corrected after baseline classification
All 3 previous finding classes explicitly CLOSED; no new open finding
Target receipt and land source gate PASS; whole-tree receipt gate remains NOT_MEASURED, not upgraded to PASS
Current SHA and clean read-only checkout reconfirmed; CI/Windows/live state remain unmeasured
```

Kết luận: KHÔNG PHẢI LỖI — header approve và reviewed_sha đúng; 0/0/0/0; mọi output tham chiếu tồn tại; giữ nguyên rc1 của thử quét rộng và đính chính, cùng giới hạn rc2 toàn cây. Checkout vẫn sạch trên exact SHA.
