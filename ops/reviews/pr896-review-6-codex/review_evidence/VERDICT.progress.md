verdict: dang_lam
reviewed_sha: 22382d8c800bed7b995d093cdcfdc206360d7fd4
Kết quả: đang đo.

## KẾT LUẬN VỀ FINDING CŨ
Đang kiểm tra hai finding lượt 5.

## BẢNG ĐO
Đang thu thập bằng chứng tại reviewed_sha.

## BẢNG SĂN

### HƯỚNG 1: Định danh cây được chấm
- giả thuyết: checkout sai SHA hoặc lịch sử thiếu.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho log --oneline 1a276a1..HEAD`.
- output thật: HEAD `22382d8c800bed7b995d093cdcfdc206360d7fd4`; tree `2424259c815d962a485bbbc52751499ed93ace34`; status rỗng; shallow `false`; hai commit `d308b0b` (hiện vật lượt 5) và `22382d8` (receipt/hint/land).
- kết luận: KHÔNG PHẢI LỖI. Các phép đo sau neo full reviewed_sha ở dòng 2.

### HƯỚNG 2: Tái áp hint lượt 5 và đối chiếu byte
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/audit.py history`
- output thật:
```text
diff.patch: byte_match=True
numstat.txt: byte_match=True
diff-pr947.patch: byte_match=True
numstat-pr947.txt: byte_match=True
hint_paths=10 apply_rc=0
patching file ops/reviews/README.md
patching file ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml
patching file ops/reviews/pr870-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/pr889-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/wp538-review-1-claude-verdict.receipt.yaml
patching file ops/reviews/wp538-review-2-claude-verdict.receipt.yaml
patching file ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
byte_for_byte_matches=9/10
ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml
ops/reviews/pr870-review-1-codex-verdict.receipt.yaml
ops/reviews/pr889-review-1-codex-verdict.receipt.yaml
ops/reviews/wp538-review-1-claude-verdict.receipt.yaml
ops/reviews/wp538-review-2-claude-verdict.receipt.yaml
ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
outside_hint_non_artifact=['ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml', 'ops/reviews/README.md', '"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 10 - HINT tren ban sao.log"', '"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 2 - doi chieu hint.log"', '"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 3 - toan ven.log"', '"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 6 - ancestry va truong con sot.log"', '"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 7 - trang thai da review.log"', '"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 8 - tu khai execution surface.log"', '"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 9 - moc lich su va cau moi.log"']
d308b0b_paths=99 only_round5_artifacts=False
verdict-cu/pr896-review-5-codex-VERDICT.md: stored_byte_match=True
verdict-cu/pr896-review-5-codex-HINT.patch: stored_byte_match=True
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 3: Toàn vẹn YAML, verdict và receipt v1
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/audit.py integrity`
- output thật:
```text
yaml_parsed=294 receipts=292
verdict_path_hashes=294 all_match=True
flat_verdict_files=270 unclaimed=[]
flat_directory_pairs=16 all_match=True
frozen_groups={'ALLOWLIST_CUTOVER': 11} all_hash_and_byte_match=True
modified_historical_verdicts=[]
errors=[]
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 2: Tái áp hint lượt 5 và đối chiếu byte
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/audit.py history`
- output thật:
```text
diff.patch: byte_match=False
numstat.txt: byte_match=False
diff-pr947.patch: byte_match=False
numstat-pr947.txt: byte_match=False
hint_paths=10 apply_rc=0
patching file ops/reviews/README.md
patching file ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml
patching file ops/reviews/pr870-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/pr889-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/wp538-review-1-claude-verdict.receipt.yaml
patching file ops/reviews/wp538-review-2-claude-verdict.receipt.yaml
patching file ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
byte_for_byte_matches=9/10
ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml
ops/reviews/pr870-review-1-codex-verdict.receipt.yaml
ops/reviews/pr889-review-1-codex-verdict.receipt.yaml
ops/reviews/wp538-review-1-claude-verdict.receipt.yaml
ops/reviews/wp538-review-2-claude-verdict.receipt.yaml
ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
README delta beyond hint: 5 added/removed lines
+| `pr896-review-5-codex-verdict.md` | `HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO` | Verdict lich su tren 1a276a1 la changes_requested 2 P1. HINT.patch luot 5 (10 tep) duoc ap NGUYEN (--fuzz=0) trong CHINH commit ghi so bien nhan nay, theo yeu cau chu kho "va cho toi khi het P1, P2, P3". Can verdict moi tren exact SHA ung vien; khong doi ket qua hay byte verdict lich su. |
+| `pr896-review-5-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong; phien ghi so do sau luot: HEAD 1a276a1, git status rong. |
+| `pr896-review-5-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (review_evidence/) tham chieu duong dan tuyet doi cua sandbox phien; tai lap can dung lai mirror tai 1a276a1. |
+| `pr896-review-5-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff-pr947.patch va review_evidence/receipt-status-all.log (>500 KB) KHONG vao kho; sha256/so byte o OMITTED.txt. |
+| [`pr896-review-5-codex-verdict.md`](pr896-review-5-codex-verdict.md) | [`.receipt.yaml`](pr896-review-5-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/2/0/0 tren `1a276a1` (head PR #947, mang HINT luot 4) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 453628b5`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · muc luc luot 3 va P2 surface DA DONG; con: P1 7 truong ancestry sot trong chinh cac receipt luot 4 da neo, P1 pr870/pr889-review-1 con noi head 'khong duoc review lai' — HINT.patch luot 5 ap trong chinh commit ghi so bien nhan nay · ban phang nguyen byte cua `pr896-review-5-codex/VERDICT.md`. Chua merge. | `1a276a15` | 36138 |
outside_hint_non_artifact=['ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml', 'ops/reviews/README.md']
d308b0b_paths=99 only_round5_artifacts=True
verdict-cu/pr896-review-5-codex-VERDICT.md: stored_byte_match=True
verdict-cu/pr896-review-5-codex-HINT.patch: stored_byte_match=True
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 3: Toàn vẹn YAML, verdict và receipt v1
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/audit.py integrity`
- output thật:
```text
yaml_parsed=294 receipts=292
verdict_path_hashes=294 all_match=True
flat_verdict_files=270 unclaimed=[]
flat_directory_pairs=16 all_match=True
frozen_groups={'ALLOWLIST_CUTOVER': 11, 'NO_DA_DO': 42} all_hash_and_byte_match=True
modified_historical_verdicts=[]
errors=[]
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 4: Ba ca riêng và bốn cổng bắt buộc tại cay-kho/
- giả thuyết: cổng đỏ hoặc N/N không đủ.
- lệnh: `python3 review_evidence/run_checks.py` (mỗi command chạy riêng với cwd `cay-kho/`, đặt `PYTHONDONTWRITEBYTECODE=1`).
- output thật:

| lệnh | rc | kết luận stdout |
|---|---|---|
| `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | ; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 |
| `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | ; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 |
| `python3 ops/lease_publish_test.py --chi-ca=t138_` | 0 | ; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | bien_nhan_v2: 239 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 292; TỔNG: ĐẠT |
| `python3 ops/land_evidence_nguon.py --root .` | 0 | land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73; TỔNG: ĐẠT |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | {"ok": true, "strict": false} |

- kết luận: KHÔNG PHẢI LỖI. Cả ba ca riêng là `1/1 đạt; đã chạy=1, bỏ qua=0`. JSON có `ok: true`. Stderr test chỉ có SyntaxWarning, không gặp `Codex home is inside a repository`. Log đầy đủ ở `review_evidence/{t26,t27,t138,bien_nhan_v2,land,doctrine,doc_claims}.{stdout,stderr,rc}`.

### HƯỚNG 2: Tái áp hint lượt 5 và đối chiếu byte
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/audit.py history`
- output thật:
```text
diff.patch: byte_match=True
numstat.txt: byte_match=True
diff-pr947.patch: byte_match=True
numstat-pr947.txt: byte_match=True
hint_paths=10 apply_rc=0
patching file ops/reviews/README.md
patching file ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml
patching file ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml
patching file ops/reviews/pr870-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/pr889-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/wp538-review-1-claude-verdict.receipt.yaml
patching file ops/reviews/wp538-review-2-claude-verdict.receipt.yaml
patching file ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
byte_for_byte_matches=9/10
ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml
ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml
ops/reviews/pr870-review-1-codex-verdict.receipt.yaml
ops/reviews/pr889-review-1-codex-verdict.receipt.yaml
ops/reviews/wp538-review-1-claude-verdict.receipt.yaml
ops/reviews/wp538-review-2-claude-verdict.receipt.yaml
ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
README delta beyond hint: 5 added/removed lines
+| `pr896-review-5-codex-verdict.md` | `HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO` | Verdict lich su tren 1a276a1 la changes_requested 2 P1. HINT.patch luot 5 (10 tep) duoc ap NGUYEN (--fuzz=0) trong CHINH commit ghi so bien nhan nay, theo yeu cau chu kho "va cho toi khi het P1, P2, P3". Can verdict moi tren exact SHA ung vien; khong doi ket qua hay byte verdict lich su. |
+| `pr896-review-5-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong; phien ghi so do sau luot: HEAD 1a276a1, git status rong. |
+| `pr896-review-5-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (review_evidence/) tham chieu duong dan tuyet doi cua sandbox phien; tai lap can dung lai mirror tai 1a276a1. |
+| `pr896-review-5-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff-pr947.patch va review_evidence/receipt-status-all.log (>500 KB) KHONG vao kho; sha256/so byte o OMITTED.txt. |
+| [`pr896-review-5-codex-verdict.md`](pr896-review-5-codex-verdict.md) | [`.receipt.yaml`](pr896-review-5-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/2/0/0 tren `1a276a1` (head PR #947, mang HINT luot 4) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 453628b5`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · muc luc luot 3 va P2 surface DA DONG; con: P1 7 truong ancestry sot trong chinh cac receipt luot 4 da neo, P1 pr870/pr889-review-1 con noi head 'khong duoc review lai' — HINT.patch luot 5 ap trong chinh commit ghi so bien nhan nay · ban phang nguyen byte cua `pr896-review-5-codex/VERDICT.md`. Chua merge. | `1a276a15` | 36138 |
outside_hint_non_artifact=['ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml', 'ops/reviews/README.md']
d308b0b_paths=99 only_round5_artifacts=True
verdict-cu/pr896-review-5-codex-VERDICT.md: stored_byte_match=True
verdict-cu/pr896-review-5-codex-HINT.patch: stored_byte_match=True
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 5: Xoá hàng/caveat mới trên clone độc lập
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `git clone --no-hardlinks --no-checkout mirror.git <tmp>/copy; git -C <copy> checkout --detach 22382d8c800bed7b995d093cdcfdc206360d7fd4; python3 review_evidence/mutations.py`
- output thật:
```text
clone=/tmp/pr896-r6-mutations-bwmr16mi/copy
checkout=22382d8c800bed7b995d093cdcfdc206360d7fd4
[
  {
    "mutation": "remove-round5-index",
    "removed_bytes": 736,
    "cases": {
      "t26": {
        "rc": 0,
        "summary": "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0",
        "error": []
      },
      "t27": {
        "rc": 1,
        "summary": "lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0",
        "error": [
          "!!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: verdict 'pr896-review-5-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó.",
          "  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: verdict 'pr896-review-5-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó."
        ]
      },
      "t138": {
        "rc": 0,
        "summary": "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0",
        "error": []
      }
    }
  },
  {
    "mutation": "remove-round5-caveat-readme",
    "removed_bytes": 366,
    "cases": {
      "t26": {
        "rc": 0,
        "summary": "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0",
        "error": []
      },
      "t27": {
        "rc": 1,
        "summary": "lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0",
        "error": [
          "!!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: caveat 'HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO' của pr896-review-5-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-5-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.",
          "  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO' của pr896-review-5-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-5-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó."
        ]
      },
      "t138": {
        "rc": 0,
        "summary": "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0",
        "error": []
      }
    }
  },
  {
    "mutation": "remove-round5-receipt-caveat",
    "removed_bytes": 362,
    "cases": {
      "t26": {
        "rc": 0,
        "summary": "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0",
        "error": []
      },
      "t27": {
        "rc": 0,
        "summary": "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0",
        "error": []
      },
      "t138": {
        "rc": 0,
        "summary": "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0",
        "error": []
      }
    }
  }
]
status_after_restore=''
```
- kết luận: KHÔNG PHẢI LỖI hiện hành; giới hạn răng được ghi theo từng ca, không suy cổng kiểm đủ ngữ nghĩa.

### HƯỚNG 7: Verdict kế tiếp của các trạng thái chưa review
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/states.py reviews; sha256sum <verdict>; git cat-file -e <historical>:<next-verdict>`
- output thật:
```text
old_eight_count=8
{
  "old_eight": [
    {
      "source": "pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml",
      "verdict": "pr455-bien-nhan-v2-review-2-codex-verdict.md",
      "expected_sha": "c595292cb63fb8c09d7d7b482cda20f9d5f0917f",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "b6f169f69cf719645b93ca0e2bcb4aff16295b2d8a09714ddb4b41beefd45814",
      "hash_match": true,
      "result": "changes_requested",
      "counts": [
        null,
        null,
        null,
        null
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr455-bien-nhan-v2-review-2-codex-verdict.receipt.yaml",
      "verdict": "pr455-bien-nhan-v2-review-3-codex-verdict.md",
      "expected_sha": "cb212847375c2319fe0ccad3f7c00c90b870e3ba",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "9f3c781842913fbffedd9198d88a1e2be2a6eb80a905f293223659a19a7a398c",
      "hash_match": true,
      "result": "approve_with_findings",
      "counts": [
        null,
        null,
        null,
        null
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml",
      "verdict": "pr455-bien-nhan-v2-review-4-codex-verdict.md",
      "expected_sha": "4ef73e69d5f3c419634118983723355e25e38305",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "3708d03a1fd871ac143f74eaacd13fdf943fe5c3e0704b77a23640b13addda1c",
      "hash_match": true,
      "result": "approve_with_findings",
      "counts": [
        null,
        null,
        null,
        null
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml",
      "verdict": "pr455-bien-nhan-v2-review-5-codex-verdict.md",
      "expected_sha": "670071b700bd97a893d64393ffded0257957d0b3",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "331fa1296a6d65e684352de9073f9c7a09b0b970ee1e81974f0f978248dbde8e",
      "hash_match": true,
      "result": "approve_with_findings",
      "counts": [
        null,
        null,
        null,
        null
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml",
      "verdict": "pr455-bien-nhan-v2-review-6-codex-verdict.md",
      "expected_sha": "5a78c150106ae381461354c77ba2023834330bbd",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "0b249313b99c3e6ec66163f6fe9043d0309926ab0b6877c866a4c024f13ae982",
      "hash_match": true,
      "result": "approve_with_findings",
      "counts": [
        null,
        null,
        null,
        null
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml",
      "verdict": "pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md",
      "expected_sha": "ca960160b477cd16346a293aaa8752772a9921d4",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "cee6b762fb08c1724c56ccbb1c6aaef8cedb22eb91b334840aa09f18ef2ebee8",
      "hash_match": true,
      "result": "approve_with_findings",
      "counts": [
        null,
        null,
        null,
        null
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr896-review-1-codex-verdict.receipt.yaml",
      "verdict": "pr896-review-2-codex-verdict.md",
      "expected_sha": "8d56009a09af7b3ef93801df105f9483de212cc7",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "a2b588b64535203f9e481240e7f014ae0f34f84b8a776e646b573666e5bd689f",
      "hash_match": true,
      "result": "changes_requested",
      "counts": [
        0,
        1,
        0,
        0
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr915-review-1-codex-verdict.receipt.yaml",
      "verdict": "pr896-review-2-codex-verdict.md",
      "expected_sha": "8d56009a09af7b3ef93801df105f9483de212cc7",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "a2b588b64535203f9e481240e7f014ae0f34f84b8a776e646b573666e5bd689f",
      "hash_match": true,
      "result": "changes_requested",
      "counts": [
        0,
        1,
        0,
        0
      ],
      "next_absent_at_anchor_rc": 128
    }
  ],
  "new_two_four_reviews": [
    {
      "source": "pr870-review-1",
      "verdict": "pr870-review-2-codex-verdict.md",
      "expected_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6",
      "hash_match": true,
      "result": "approve",
      "counts": [
        0,
        0,
        0,
        0
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr870-review-1",
      "verdict": "pr870-review-3-codex-verdict.md",
      "expected_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "0021b5b2f90e0da39a92c11041c3236980acfbbd0b22f46d0044ac8334f16e81",
      "hash_match": true,
      "result": "approve",
      "counts": [
        0,
        0,
        0,
        0
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr889-review-1",
      "verdict": "pr889-review-2-codex-verdict.md",
      "expected_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612",
      "hash_match": true,
      "result": "approve",
      "counts": [
        0,
        0,
        0,
        0
      ],
      "next_absent_at_anchor_rc": 128
    },
    {
      "source": "pr889-review-1",
      "verdict": "pr889-review-3-codex-verdict.md",
      "expected_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c",
      "receipt_sha_match": true,
      "verdict_header_sha_match": true,
      "hash": "c05bc41d9232d99a9e0c49199e022a9a64b01227674144da73bf50b9b7ce445f",
      "hash_match": true,
      "result": "approve",
      "counts": [
        0,
        0,
        0,
        0
      ],
      "next_absent_at_anchor_rc": 128
    }
  ]
}
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 6: Mốc lịch sử và ancestry của mọi trường đã neo
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/states.py ancestry; git merge-base --is-ancestor <source> <target>; git log --diff-filter=A 22382d8c800bed7b995d093cdcfdc206360d7fd4 -- <receipt>`
- output thật:
```text
historical_fields=48 same_original=35 receipt_added_at_anchor=48
ancestry_measurements=148 all_rc0=True
old_seven=[
  {
    "receipt": "ci-windows-review-5-claude-verdict.receipt.yaml",
    "field": "chuoi_verdict_ghi_chu",
    "anchor": "e32c5643111e001dc0c655c568b445c897ade450",
    "oid": "c2f68987b3f298de12b84cf29a934c7b844c8558",
    "rc_master": 0,
    "rc_candidate": 0
  },
  {
    "receipt": "doctrine-scan-review-1-claude-verdict.receipt.yaml",
    "field": "anchor.gioi_han",
    "anchor": "86169c00beff045b0faed63e39d1a67b9acd1fc1",
    "oid": "bc5d0c6e4d3d5b3cc5d6f8c08ba1c005dd9bdadc",
    "rc_master": 0,
    "rc_candidate": 0
  },
  {
    "receipt": "doctrine-scan-review-2-claude-verdict.receipt.yaml",
    "field": "anchor.gioi_han",
    "anchor": "de0ecd0f912bb131b63ada866672af00129eefd0",
    "oid": "80d816130fda69af75dc1d9ae76f3fc83b837773",
    "rc_master": 0,
    "rc_candidate": 0
  },
  {
    "receipt": "doctrine-scan-review-3-claude-verdict.receipt.yaml",
    "field": "anchor.gioi_han",
    "anchor": "6d59a4394f0e51ace4e02c8f4be13cb649e6871e",
    "oid": "7d8bb69ac02b54075d63a9915e12e6d2bf28b513",
    "rc_master": 0,
    "rc_candidate": 0
  },
  {
    "receipt": "wp538-review-1-claude-verdict.receipt.yaml",
    "field": "anchor.gioi_han",
    "anchor": "ab27f786a45de5df7aae23f7df7b4c4fb8eecb92",
    "oid": "ab27f786a45de5df7aae23f7df7b4c4fb8eecb92",
    "rc_master": 0,
    "rc_candidate": 0
  },
  {
    "receipt": "wp538-review-2-claude-verdict.receipt.yaml",
    "field": "anchor.gioi_han",
    "anchor": "ab27f786a45de5df7aae23f7df7b4c4fb8eecb92",
    "oid": "ab27f786a45de5df7aae23f7df7b4c4fb8eecb92",
    "rc_master": 0,
    "rc_candidate": 0
  },
  {
    "receipt": "wp540-review-1-claude-verdict.receipt.yaml",
    "field": "anchor.gioi_han",
    "anchor": "ab27f786a45de5df7aae23f7df7b4c4fb8eecb92",
    "oid": "ab27f786a45de5df7aae23f7df7b4c4fb8eecb92",
    "rc_master": 0,
    "rc_candidate": 0
  }
]
exceptions={"03f12ac63284dd814dcf14664968af4872ef7f8a": {"3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}, "4bc9432": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 1}, "604b8d9": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 1}, "82359c4": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}, "2e4183b": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}, "1a276a1": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}, "d308b0b": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}
anchor_mismatches=[{"receipt": "ops/reviews/pr508-review-5-codex-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "line": 81, "anchor": "a639e48e3077eb6797f6d793c3d91e7ae290f68a", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "FIELD_NOT_AT_SAME_PATH: TypeError(\"string indices must be integers, not 'str'\")", "claimed": "Năm biên nhận khai `anchor.cuong_do: trung_binh`, yếu hơn các biên nhận `cao` cùng thư mục: PR #508 chưa merge nên quan hệ tổ tiên mới ở trong NHÁNH."}, {"receipt": "ops/reviews/wp678-spec-review-10-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "line": 16, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "(a) sha256 cua `git show 42292b4:ops/specs/lease-id-ep-kieu-yaml-r10.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r10 CHUA co tren master; chi o commit cuc bo cua nhanh claude/spec-wp678-r7.", "claimed": "(a) sha256 cua `git show 42292b4:ops/specs/lease-id-ep-kieu-yaml-r10.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r10 CHUA co tren master; chi o nhanh claude/spec-wp678-r7 (luc review: commit cuc bo; da day len origin 2026-10-07 17:49Z, head luc do 284a03f)."}, {"receipt": "ops/reviews/wp678-spec-review-10-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "line": 95, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "reviewed_sha 42292b4 chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 ~17:5xZ (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do.", "claimed": "reviewed_sha 42292b4 chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 17:49Z (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do."}, {"receipt": "ops/reviews/wp678-spec-review-11-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "line": 16, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "(a) sha256 cua `git show e48423a:ops/specs/lease-id-ep-kieu-yaml-r11.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r11 CHUA co tren master; chi o commit cuc bo cua nhanh claude/spec-wp678-r7.", "claimed": "(a) sha256 cua `git show e48423a:ops/specs/lease-id-ep-kieu-yaml-r11.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r11 CHUA co tren master; chi o nhanh claude/spec-wp678-r7 (luc review: commit cuc bo; da day len origin 2026-10-07 17:49Z, head luc do 284a03f)."}, {"receipt": "ops/reviews/wp678-spec-review-11-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "line": 95, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "reviewed_sha e48423a chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 ~17:5xZ (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do.", "claimed": "reviewed_sha e48423a chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 17:49Z (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do."}, {"receipt": "ops/reviews/wp678-spec-review-12-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "line": 16, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "(a) sha256 cua `git show d5a57c1:ops/specs/lease-id-ep-kieu-yaml-r12.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r12 CHUA co tren master; chi o commit cuc bo cua nhanh claude/spec-wp678-r7.", "claimed": "(a) sha256 cua `git show d5a57c1:ops/specs/lease-id-ep-kieu-yaml-r12.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r12 CHUA co tren master; chi o nhanh claude/spec-wp678-r7 (luc review: commit cuc bo; da day len origin 2026-10-07 17:49Z, head luc do 284a03f)."}, {"receipt": "ops/reviews/wp678-spec-review-12-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "line": 95, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "reviewed_sha d5a57c1 chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 ~17:5xZ (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do.", "claimed": "reviewed_sha d5a57c1 chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 17:49Z (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do."}, {"receipt": "ops/reviews/wp678-spec-review-7-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "line": 16, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "(a) sha256 cua `git show 088511f:ops/specs/lease-id-ep-kieu-yaml-r7.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r7 CHUA co tren master; chi o commit cuc bo cua nhanh claude/spec-wp678-r7.", "claimed": "(a) sha256 cua `git show 088511f:ops/specs/lease-id-ep-kieu-yaml-r7.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r7 CHUA co tren master; chi o nhanh claude/spec-wp678-r7 (luc review: commit cuc bo; da day len origin 2026-10-07 17:49Z, head luc do 284a03f)."}, {"receipt": "ops/reviews/wp678-spec-review-7-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "line": 95, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "reviewed_sha 088511f chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 ~17:5xZ (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do.", "claimed": "reviewed_sha 088511f chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 17:49Z (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do."}, {"receipt": "ops/reviews/wp678-spec-review-8-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "line": 16, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "(a) sha256 cua `git show f958e14:ops/specs/lease-id-ep-kieu-yaml-r8.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r8 CHUA co tren master; chi o commit cuc bo cua nhanh claude/spec-wp678-r7.", "claimed": "(a) sha256 cua `git show f958e14:ops/specs/lease-id-ep-kieu-yaml-r8.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r8 CHUA co tren master; chi o nhanh claude/spec-wp678-r7 (luc review: commit cuc bo; da day len origin 2026-10-07 17:49Z, head luc do 284a03f)."}, {"receipt": "ops/reviews/wp678-spec-review-8-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "line": 95, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "reviewed_sha f958e14 chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 ~17:5xZ (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do.", "claimed": "reviewed_sha f958e14 chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 17:49Z (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do."}, {"receipt": "ops/reviews/wp678-spec-review-9-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "line": 16, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "(a) sha256 cua `git show 2469f3e:ops/specs/lease-id-ep-kieu-yaml-r9.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r9 CHUA co tren master; chi o commit cuc bo cua nhanh claude/spec-wp678-r7.", "claimed": "(a) sha256 cua `git show 2469f3e:ops/specs/lease-id-ep-kieu-yaml-r9.md` = spec_sha256 dong 3 tep verdict = so trong comment ban chieu. Dac ta r9 CHUA co tren master; chi o nhanh claude/spec-wp678-r7 (luc review: commit cuc bo; da day len origin 2026-10-07 17:49Z, head luc do 284a03f)."}, {"receipt": "ops/reviews/wp678-spec-review-9-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "line": 95, "anchor": "62319d945fff81de6396aab6806a4ab349682aba", "same_historical_scalar": false, "receipt_introduced_at_anchor": true, "original": "reviewed_sha 2469f3e chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 ~17:5xZ (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do.", "claimed": "reviewed_sha 2469f3e chi nam tren nhanh claude/spec-wp678-r7 (khong phai master). Nhanh da DAY len origin 2026-10-07 17:49Z (head 284a03f) TRUOC commit bien nhan, nen tra duoc tu clone day du. Nhanh spec la ref TRUOT: xoa nhanh truoc khi r* vao master hoac co ref luu-tru thi bien_nhan_v2 se tra KHONG DO DUOC (rc=2). Comment ban chieu luc review tu khai 'CUC BO, CHUA DAY' — dung o thoi diem do."}]
```
- kết luận: CẦN KIỂM TRA.

### HƯỚNG 8: Tự khai execution surface và nguồn runtime
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/surfaces.py; rg -n -i "codex.service|service/api|execution.surface|surface:" cay-kho/ops/reviews --glob "*-verdict.md" --glob "VERDICT.md"`
- output thật:
```text
verdict_files_repo_wide=413 distinct_content=396
run_json_files=48 parse_errors=[]
receipt_runtime_pairs=17 mismatches=[]
service_self_claim_files=25 missing_correction=[]
other_identity_mentions=71 unknown_distinct_verdicts_with_surface=62
ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.md:130 receipt_surface=codex_cli corrections=[('KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC', 1, False)] runtime=[]
ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.md:194 receipt_surface=codex_cli corrections=[('KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC', 1, False)] runtime=[]
ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.md:125 receipt_surface=codex_cli corrections=[('KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC', 1, False)] runtime=[]
ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.md:14 receipt_surface=codex_cli corrections=[('KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC', 1, False)] runtime=[]
phan-bien-quy-trinh-review-3-codex-verdict.md:15 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
phan-bien-quy-trinh-review-4-codex-verdict.md:13 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
phan-bien-quy-trinh-review-5-codex-verdict.md:12 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-1-codex-verdict.md:7 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-2-codex-verdict.md:9 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-3-codex-verdict.md:9 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-4-codex-verdict.md:9 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-5-codex-verdict.md:9 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-6-codex-verdict.md:9 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md:9 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr455-bien-nhan-v2-review-8-gpt6astra-verdict.md:8 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr460-bien-nhan-v2-review-9-gpt6astra-verdict.md:5 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr493-review-5-codex-verdict.md:8 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr526-review-3-codex-verdict.md:151 receipt_surface=codex_cli corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
pr870-review-2-codex-verdict.md:9 receipt_surface=codex_cli corrections=[('VERDICT-KHAI-SAI-EXECUTION-SURFACE', 1, True)] runtime=['ops/reviews/pr870-review-2-codex/run/run.json']
pr870-review-3-codex-verdict.md:444 receipt_surface=codex_cli corrections=[('VERDICT-KHAI-SAI-EXECUTION-SURFACE', 1, True)] runtime=['ops/reviews/pr870-review-3-codex/run/run.json']
pr889-review-1-codex-verdict.md:7 receipt_surface=codex_cli corrections=[('VERDICT-KHAI-SAI-EXECUTION-SURFACE', 1, True)] runtime=['ops/reviews/pr889-review-1-codex/run/run.json']
pr889-review-2-codex-verdict.md:9 receipt_surface=codex_cli corrections=[('VERDICT-KHAI-SAI-EXECUTION-SURFACE', 1, True)] runtime=['ops/reviews/pr889-review-2-codex/run/run.json']
pr889-review-3-codex-verdict.md:309 receipt_surface=codex_cli corrections=[('VERDICT-KHAI-SAI-EXECUTION-SURFACE', 1, True)] runtime=['ops/reviews/pr889-review-3-codex/run/run.json']
slice-b-c-review-2-codex-verdict.md:19 receipt_surface=None corrections=[('SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC', 1, True)] runtime=[]
wp766-r1-g1-exec-review-1-codex-verdict.md:12 receipt_surface=codex_cli corrections=[('VERDICT-KHAI-SAI-EXECUTION-SURFACE', 1, True)] runtime=['ops/reviews/wp766-r1-g1-exec-review-1-codex/run.json']

```
- kết luận: KHÔNG PHẢI LỖI mới trong inventory; tự khai service được đính chính hoặc caveat thiếu runtime, API/shell chung không đủ phân biệt CLI.

### HƯỚNG 9: Lời khai mới do 22382d8 ghi thêm
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/new_claims.py; sha256sum -c SHA256SUMS; git show <OID>:<path>`
- output thật:
```text
{
  "receipt_verdict_bytes_sha256": {
    "bytes": 36138,
    "hash": "968ebc3859538e79b53bd9ead8e3c9464a0db8c8e83e62a4b7ac7437f0480e9e",
    "matches": true
  },
  "run_id_head_surface": {
    "run_id": "453628b5eeef497eb4505bed3c8247ec",
    "head": "1a276a15192013fdb1e472db409133b53ac57944",
    "ref": "HEAD",
    "execution_surface": "codex_cli",
    "transport": "machine",
    "ma_thoat": 0,
    "trang_thai": "xong",
    "worktree_sach": true,
    "thoi_luong_giay": 1036.087
  },
  "prompt_sha256_match": true,
  "reviewed_tree_match": true,
  "model_events": {
    "count": 36,
    "response_ids": 36,
    "models": [
      "gpt-6.1-sol"
    ]
  },
  "stdout_run_hash_and_byte_match": true,
  "stderr_run_hash_and_byte_match": true,
  "evidence_blob_matches": true,
  "evidence_oid": "d308b0b1bbcb0db2e1624e4eda6431f73ace453f",
  "receipt_addition_commit": [
    "22382d8c800bed7b995d093cdcfdc206360d7fd4"
  ],
  "artifact_commit_parent": "1a276a15192013fdb1e472db409133b53ac57944",
  "receipt_commit_parent": "d308b0b1bbcb0db2e1624e4eda6431f73ace453f",
  "new_caveats_rows": [
    {
      "id": "HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO",
      "rows": 1,
      "exact_description": true
    },
    {
      "id": "CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY",
      "rows": 1,
      "exact_description": true
    },
    {
      "id": "SCRIPT-DO-DOC-DUONG-DAN-SANDBOX",
      "rows": 1,
      "exact_description": true
    },
    {
      "id": "TEP-LON-KHONG-VAO-KHO",
      "rows": 1,
      "exact_description": true
    }
  ],
  "artifact_sha256sums": {
    "rc": 0,
    "ok_count": 97,
    "failed": [],
    "stderr": ""
  },
  "land_round5_sha_and_receipt_match": true
}
```
- kết luận: KHÔNG PHẢI LỖI ở những lời khai mới này; mô tả finding thuộc verdict 1a276a1, không coi là tự khai surface hoặc trạng thái hiện hành của mọi receipt.

### HƯỚNG 10: Mở rộng quét trạng thái ra ngoài danh sách lượt 5
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/inventory.py; python3 review_evidence/negative_ancestry.py; python3 review_evidence/residuals.py; git merge-base --is-ancestor <OID> 3e973a03b151e37cd402e0a723816eeaa8247193; git ls-tree 3e973a03b151e37cd402e0a723816eeaa8247193 -- <receipt>`
- output thật:
```text
inventory: 294 YAML; targeted no-review/no-apply/no-merge/ancestry strings = 179 unanchored candidates + 149 anchored candidates; README candidates = 119 (regex inventory, not finding counts).
ops/reviews/doctor-github-mcp-review-6-codex-verdict.receipt.yaml:146 receipt_khong_khai.0 oid=4920113a639d81385c0f98b1488c0f497776d2ff rc(master,candidate)=[0, 0] schema=1
Không khai rằng `evidence_url` là BỀN. Nó trỏ một commit hiện chỉ được giữ bởi nhánh `ops/**`; xem `evidence_url_han_che` và `truy_xuat_*`. URL ĐÚNG ≠ URL SỐNG LÂU.
ls-tree master: 100644 blob 9f62f975be42408cccb54d3237dff095bda9c7ee	ops/reviews/doctor-github-mcp-review-6-codex-verdict.receipt.yaml
ops/reviews/don-nhanh-base-review-4-claude-verdict.receipt.yaml:60 truy_xuat_ghi_chu oid=03f12ac63284dd814dcf14664968af4872ef7f8a rc(master,candidate)=[0, 0] schema=1
CẢNH BÁO BỀN VỮNG — đọc kỹ. `evidence_url` neo vào một commit chỉ tồn tại trên nhánh `claude/wp55-r2g2-executor-p4tee0`. #150 đã merge TRƯỚC commit này, nên hai verdict lượt 4/5 KHÔNG nằm trong lịch sử `master`. Xoá nhánh ấy ⇒ commit không tra được ⇒ `evidence_url` chết, và ta quay lại đúng tình trạng nợ mà bản ghi này sinh ra để đóng. Muốn bền thì phải land nhánh này vào `master` HOẶC tạo tag `luu-tru/*` trỏ commit. Phiên web KHÔNG tạo được tag (proxy 403) — việc này thuộc chủ kho.
ls-tree master: 100644 blob 249b9998aed5b0aa1d8b4680323133f5ceb9ac66	ops/reviews/don-nhanh-base-review-4-claude-verdict.receipt.yaml
ops/reviews/don-nhanh-base-review-5-claude-verdict.receipt.yaml:73 truy_xuat_ghi_chu oid=03f12ac63284dd814dcf14664968af4872ef7f8a rc(master,candidate)=[0, 0] schema=1
Y HỆT lượt 4: commit chỉ sống trên nhánh `claude/wp55-r2g2-executor-p4tee0`, KHÔNG trong lịch sử `master` (#150 merge TRƯỚC commit này). Xoá nhánh ⇒ link chết ⇒ nợ mở lại. Cần land vào `master` hoặc gắn tag `luu-tru/*`; phiên web không tạo được tag (proxy 403).
ls-tree master: 100644 blob 52ab3cd98bae7136e4c87140030bda08cf130bc4	ops/reviews/don-nhanh-base-review-5-claude-verdict.receipt.yaml
ops/reviews/wp461-review-1-codex-verdict.receipt.yaml:101 anchor.cuong_do oid=ef72264cb268643a89df3e15cf6cb840da92307b rc(master,candidate)=[0, 0] schema=2
candidate ancestry only; canonical inclusion pending — commit verdict ef72264cb268643a89df3e15cf6cb840da92307b (evidence_url) là tổ tiên của head ứng viên hiện hành (nhánh agent/wp461-g8-claude, PR của g8; trước đó #633 head 155bbaa47e6936a81e16537e44e8a9b0c8e8fa60). #625 chỉ còn là nguồn gốc lịch sử. Đường land đang chờ = PR g8, CHỈ bằng merge commit; squash làm mất commit ef72264c nên neo này KHÔNG sống qua squash. Riêng reviewed_sha 5e2851881e810b39ebee6884371e5b3e229a01d7 ĐÃ canonical qua merge commit 6980e5bf04e4e5b8b75e5817578f1aba13f2f5ab (PR #617)
ls-tree master: 100644 blob 2c45c070c8d27220ba87e16ebe576d1713c67065	ops/reviews/wp461-review-1-codex-verdict.receipt.yaml
ops/reviews/wp461-review-1-codex-verdict.receipt.yaml:472 lich_su_ban_ung_vien.ghi_chu oid=ef72264cb268643a89df3e15cf6cb840da92307b rc(master,candidate)=[0, 0] schema=2
Receipt CHUA duoc giao (chua o master). Danh sach = cac ban UNG VIEN truoc commit nay, cu -> moi, sinh tu `git log --reverse --format=%H 541fa6ca9ba78d2669261b528572dbc05b53ea87..c026693d3b0cec663e09f02a5cd195e92d26bb60 -- ops/reviews/wp461-review-1-codex-verdict.receipt.yaml` (DIEM CUOI GHIM = ban ung vien lien truoc ban nay; ban sua sau PHAI chu dong doi diem cuoi, khong dung HEAD^; Codex 4101132071) + sha256 cua `git show <commit>:ops/reviews/wp461-review-1-codex-verdict.receipt.yaml`; ban hien tai khong co mat (tu tham chieu). Thread 4100299339.
ls-tree master: 100644 blob 2c45c070c8d27220ba87e16ebe576d1713c67065	ops/reviews/wp461-review-1-codex-verdict.receipt.yaml
ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml:88 anchor.cuong_do oid=b2134a40243e5cb3ea6d64eaf49a4c9f26794cbc rc(master,candidate)=[0, 0] schema=2
candidate ancestry only; canonical inclusion pending — commit verdict b2134a40243e5cb3ea6d64eaf49a4c9f26794cbc (evidence_url) chỉ ở tổ tiên PR #623, vào master khi PR land bằng merge commit; riêng reviewed_sha 92adc711 ĐÃ canonical qua merge commit c10487410cc502e96e9dd43639f2ddb6af104922 (PR #613)
ls-tree master: 100644 blob fa39099838f3a2be4d85765657df756d733b4afe	ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml
ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml:357 lich_su_ban_ung_vien.ghi_chu oid=b2134a40243e5cb3ea6d64eaf49a4c9f26794cbc rc(master,candidate)=[0, 0] schema=2
Receipt nay CHUA duoc giao (chua o master: `git ls-tree origin/master ops/reviews/wp523-r15-*` rong) — moi ban la ban UNG VIEN trong PR #623; sua truoc khi land khong phai 'sua receipt da giao' (S5 r15 / §8 dong 461-462). Lich su cac ban ung vien ghi o day de noi nguon (thread 4100014487); ban hien hanh la dong cuoi (truoc commit nay).
ls-tree master: 100644 blob fa39099838f3a2be4d85765657df756d733b4afe	ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml
NO_DA_DO covers don-nhanh-base-review-4/5; ALLOWLIST_CUTOVER covers doctor-github-mcp-review-6. No supplementary entry for any of these five receipts at reviewed_sha.
Other review heads: 5a96c1a and 888c0d9 have 0 matching ops/reviews receipts; 4bc9432 and 604b8d9 remain non-ancestors of master and candidate (rc1). Historical finding summaries and land-decision statements excluded.
```
- kết luận: LỖI P1 phu-nhan-ancestry-chi-tren-nhanh-da-cu: 7 trường trong 5 receipt còn sai hiện hành; ba v1 cần sidecar supplementary, không đổi byte.

### HƯỚNG 11: Surface ngoài ops/reviews, đối chiếu đúng lượt trong hồ sơ land
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/land_surfaces.py; read run*.json, exact verdict lines and land.review; sha256sum <verdict>`
- output thật:
```text
runtime JSON inventory includes run-*.json: 120 records (48 literal run.json, including duplicates/snapshots; not 120 independent runs).
ops/land/pr832-wp831-provenance/verdict-luot7/wp831-g1-luot7-codex-verdict.md:6
SELF: Reviewer độc lập OpenAI Codex, họ GPT-6 theo chỉ dẫn runtime; `provider: openai_codex`, `execution_surface: codex_service` (API agent có shell), `transport: machine`. Không đo model variant/effort, launcher receipt hoặc assurance live. Executor Claude theo assignment. Agent `tl_auditor` chỉ đọc hướng dẫn, mã và log theo `CLAUDE.md` §Quy trình sửa code/5; không chạy test hay sửa tệp.
SOURCE: ops/land/pr832-wp831-provenance/verdict-luot7/run.json
{"run_id": "1ff81cba41874a218b53275d3cdc1418", "head": "51ae5c095972611d2c6045bd81786a4fc7e9ca62", "provider": "openai_codex", "execution_surface": "codex_cli", "transport": "machine", "lenh": {"chuong_trinh": "codex", "so_doi_so": 9, "van_tay": "877f1a432e65000c"}}
sha256=1e27ba6bf2c4690a470b7786fe799c850b5924352a85a24460fb5053ff216d28 bytes=17277 same_master=True same_prev=True
ops/land/pr848-wp744-provenance/verdicts/wp744-g3-luot1-codex-verdict.md:36
SELF: - Reviewer: Codex/OpenAI, `model_family: openai`, phiên API có công cụ shell (`execution_surface: codex_service`, `transport: machine`). Họ model theo định danh hệ thống của phiên; không có header CLI/metadata backend riêng để máy đối chứng tên model chi tiết, effort hoặc session ID. Executor Claude theo assignment/commit, không đo lại runtime Executor. Verdict nội dung này không tự ghi transition hay receipt `cross_approved`.
SOURCE: ops/land/pr848-wp744-provenance/verdicts/run-f65e544e.json
{"run_id": "f65e544ef5d64ba7a1e0edb607edcf0a", "head": "23bc189f28ea60f04ca1634b6fe66d02babf12ed", "provider": "openai_codex", "execution_surface": "codex_cli", "transport": "machine", "lenh": {"chuong_trinh": "codex", "so_doi_so": 9, "van_tay": "4c1cfbea38b3652f"}}
sha256=af2b5fa426a7d53755148f4f9711712246afadc91e1d75e5267f8c8023bc3911 bytes=18706 same_master=True same_prev=True
ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-verdict.md:3
SELF: - Reviewer: OpenAI Codex (GPT-6 family as identified by session instructions); provider `openai_codex`; execution surface `codex_service` with local shell tools; transport machine/tool-mediated. Exact serving-model/effort attestation is not independently measured. Independent reviewer in this session; no executor role.
SOURCE: ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-transcript.txt
{"transcript_header": ["OpenAI Codex v0.163.0", "--------", "workdir: /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv21", "model: gpt-6-astra", "provider: openai", "approval: never", "sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)", "reasoning effort: xhigh", "reasoning summaries: none", "session id: 01a157da-2170-7be2-b6d0-053fa8f91aec", "--------", "user", "# Independent read-only review — WP748 r21/g21, PR #862, exact head"]}
sha256=95438373ee2f04a8431e6b10cfd2111144f9744bc54ac114c5670e0652e1ce87 bytes=14181 same_master=True same_prev=True
Two raw run IDs above belong to the exact verdict head and same review round. For #862 round 1, DO NOT borrow run-f0909b38.json: that is round 2 on the same head; the round-1 transcript and land.review.luot_1 identify direct codex exec. No explicit surface correction/caveat for these three verdicts was found in their land evidence or supplementary review caveats.
Excluded: #849 round4/5 are explicitly corrected by review.luot_cuoi.reviewer (LOI TU PHAN LOAI; trust CLI header); run-03c4f6be is round6, not proof for round4/5. #823 round5 and #877 round2: no matching runtime with explicit contrary surface identified; no assertion of actual surface. Generic API/local-shell wording in other verdicts does not establish codex_service.
```
- kết luận: LỖI P1 surface-service-cli-trong-ho-so-land: 3 verdict tự khai service, nguồn CLI của chính lượt chứng minh khác; các băm lịch sử giữ nguyên.

### HƯỚNG 12: Gợi ý vá tài liệu trên bản sao
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/build_hint.py; patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>`
- output thật:
```text
patch_paths=7 dry_run_rc=0 apply_rc=0
checking file ops/land/pr832-wp831-land-evidence.yaml
checking file ops/land/pr848-wp744-land-evidence.yaml
checking file ops/land/pr862-wp748-r21-land-evidence.yaml
checking file ops/reviews/README.md
checking file ops/reviews/pr896-review-6-legacy-caveats.yaml
checking file ops/reviews/wp461-review-1-codex-verdict.receipt.yaml
checking file ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml
clone=/tmp/pr896-r6-mutations-bwmr16mi/copy
 ops/land/pr832-wp831-land-evidence.yaml                   | 11 +++++++++++
 ops/land/pr848-wp744-land-evidence.yaml                   | 11 +++++++++++
 ops/land/pr862-wp748-r21-land-evidence.yaml               | 12 ++++++++++++
 ops/reviews/README.md                                     |  4 ++++
 ops/reviews/wp461-review-1-codex-verdict.receipt.yaml     | 12 ++----------
 ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml | 10 ++--------
 6 files changed, 42 insertions(+), 18 deletions(-)

```
- kết luận: KHÔNG PHẢI LỖI của hint; mới áp trên clone tại reviewed_sha, chưa chạy trên cây thật; không đổi ba receipt v1 hoặc byte verdict.

### HƯỚNG 13: Kiểm lại hint bằng ca có sẵn và bảo toàn byte
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/hint_checks.py`
- output thật:
```text
{
  "t26": {
    "rc": 0,
    "summary": "\nlease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
  },
  "t27": {
    "rc": 0,
    "summary": "\nlease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
  },
  "t138": {
    "rc": 0,
    "summary": "\nlease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
  },
  "bien_nhan_v2": {
    "rc": 0,
    "summary": "bien_nhan_v2: 239 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 292\nTỔNG: ĐẠT"
  },
  "land": {
    "rc": 0,
    "summary": "land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73\nTỔNG: ĐẠT"
  },
  "doctrine": {
    "rc": 0,
    "summary": "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
  },
  "doc_claims": {
    "rc": 0,
    "summary": true
  }
}
Unique-key YAML parse passed; caveat IDs unique; all review verdict bytes and all v1 receipt bytes unchanged; three land verdict hashes unchanged.
```
- kết luận: KHÔNG PHẢI LỖI của hint; kết quả chỉ trên clone.

### HƯỚNG 14: Đối chiếu trạng thái cuối
- giả thuyết: phép đo làm thay đổi cây gốc hoặc để lại đột biến.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored`; cùng lệnh trên clone sau hoàn nguyên đúng các path của hint.
- output thật:
```json
{
  "original": {
    "head": {
      "rc": 0,
      "output": "22382d8c800bed7b995d093cdcfdc206360d7fd4"
    },
    "tree": {
      "rc": 0,
      "output": "2424259c815d962a485bbbc52751499ed93ace34"
    },
    "status_with_ignored": {
      "rc": 0,
      "output": ""
    }
  },
  "copy_restored": {
    "head": {
      "rc": 0,
      "output": "22382d8c800bed7b995d093cdcfdc206360d7fd4"
    },
    "tree": {
      "rc": 0,
      "output": "2424259c815d962a485bbbc52751499ed93ace34"
    },
    "status_with_ignored": {
      "rc": 0,
      "output": ""
    }
  }
}
```
- kết luận: KHÔNG PHẢI LỖI. Cây gốc và clone phục hồi đều sạch, HEAD/tree khớp reviewed_sha.
