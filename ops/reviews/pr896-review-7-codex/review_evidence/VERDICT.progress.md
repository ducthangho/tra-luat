verdict: dang_lam
reviewed_sha: 05bc12e2b9008071ca28edbd4574e58644d48220
Kết quả: đang đo.

Đang thực hiện độc lập theo PROMPT.md; chỉ đọc cây cay-kho, mọi đột biến sẽ đặt trên bản sao /tmp.

## BẢNG SĂN

HƯỚNG 1: Định danh cây và lịch sử thay đổi

- giả thuyết: checkout lệch SHA hoặc có sửa ngoài commit.
- lệnh/output thật:
```text
$ git rev-parse HEAD HEAD^{tree} refs/remotes/origin/master
05bc12e2b9008071ca28edbd4574e58644d48220
3412a314b129d1ee1473e528a5ec438378ccebe5
3e973a03b151e37cd402e0a723816eeaa8247193
rc=0
$ git status --porcelain
rc=0
$ git log --oneline 22382d8..05bc12e
05bc12e ops: bien nhan cross-review luot 6 #896 + ap HINT luot 6 + khoi luot 6 ho so land
825dab1 ops/reviews: hien vat cross-review luot 6 #896 (codex, cham 22382d8)
rc=0
```
- kết luận: KHÔNG PHẢI LỖI; đúng SHA, worktree sạch, hai commit 825dab1 và 05bc12e. Danh sách tệp đổi lưu trong review_evidence/00-preflight.log.

### HƯỚNG 2: Tái áp hint lượt 6 và đối chiếu byte
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/audit.py history`
- output thật:
```text
diff.patch: byte_match=True
numstat.txt: byte_match=True
diff-pr947.patch: byte_match=True
numstat-pr947.txt: byte_match=True
hint_paths=7 apply_rc=0
patching file ops/land/pr832-wp831-land-evidence.yaml
patching file ops/land/pr848-wp744-land-evidence.yaml
patching file ops/land/pr862-wp748-r21-land-evidence.yaml
patching file ops/reviews/README.md
patching file ops/reviews/pr896-review-6-legacy-caveats.yaml
patching file ops/reviews/wp461-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml
byte_for_byte_matches=6/7
ops/land/pr832-wp831-land-evidence.yaml
ops/land/pr848-wp744-land-evidence.yaml
ops/land/pr862-wp748-r21-land-evidence.yaml
ops/reviews/pr896-review-6-legacy-caveats.yaml
ops/reviews/wp461-review-1-codex-verdict.receipt.yaml
ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml
README delta beyond hint: 6 added/removed lines
+| `pr896-review-6-codex-verdict.md` | `HINT-LUOT6-AP-CUNG-COMMIT-GHI-SO` | Verdict lich su tren 22382d8 la changes_requested 2 P1. HINT.patch luot 6 (7 tep) duoc ap NGUYEN (--fuzz=0) trong CHINH commit ghi so bien nhan nay, theo yeu cau chu kho "va cho toi khi het P1, P2, P3". Can verdict moi tren exact SHA ung vien; khong doi ket qua hay byte verdict lich su. |
+| `pr896-review-6-codex-verdict.md` | `LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI` | Run c0fa33fa (cung prompt, cung head) ma_thoat 1 sau 349.795 s: transcript codex ghi server_overloaded "Selected model is at capacity". VERDICT.partial.md chi co dong dang_lam + mot phep do t26; KHONG duoc tinh la verdict. Hien vat o luot-hong-c0fa33fa/. |
+| `pr896-review-6-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong; phien ghi so do sau luot: HEAD 22382d8, git status rong. |
+| `pr896-review-6-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (review_evidence/) tham chieu duong dan tuyet doi cua sandbox phien; tai lap can dung lai mirror tai 22382d8. |
+| `pr896-review-6-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff.patch, diff-pr947.patch va review_evidence/status-inventory.json (>500 KB) KHONG vao kho; sha256/so byte o OMITTED.txt. |
+| [`pr896-review-6-codex-verdict.md`](pr896-review-6-codex-verdict.md) | [`.receipt.yaml`](pr896-review-6-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/2/0/0 tren `22382d8` (head PR #947, mang HINT luot 5) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 7a86ed4f`, lan dau c0fa33fa chet vi may chu qua tai; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · hai finding luot 5 DA DONG; con: P1 7 truong ancestry o 5 receipt khac, P1 3 verdict trong provenance land tu khai codex_service — HINT.patch luot 6 ap trong chinh commit ghi so bien nhan nay · ban phang nguyen byte cua `pr896-review-6-codex/VERDICT.md`. Chua merge. | `22382d8c` | 32324 |
outside_hint_non_artifact=['ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml', 'ops/reviews/README.md']
825dab1_paths=122 only_round6_artifacts=True
verdict-cu/pr896-review-6-codex-VERDICT.md: stored_byte_match=True
verdict-cu/pr896-review-6-codex-HINT.patch: stored_byte_match=True
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 3: Toàn vẹn YAML, verdict và receipt v1
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/audit.py integrity`
- output thật:
```text
yaml_parsed=368 receipts=293
verdict_path_hashes=301 all_match=True
flat_verdict_files=271 unclaimed=[]
flat_directory_pairs=17 all_match=True
frozen_groups={'ALLOWLIST_CUTOVER': 11, 'NO_DA_DO': 42} all_hash_and_byte_match=True
modified_historical_verdicts=[]
errors=[]
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 4: Ba ca riêng và bốn cổng tại cay-kho
- giả thuyết: gate xanh do bỏ ca hoặc rc không phản ánh kết quả.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/run_checks.py` chạy riêng 7 lệnh có sẵn.
- output thật:
```text
python3 ops/lease_publish_test.py --chi-ca=t26_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t27_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t138_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/bien_nhan_v2.py --root . | rc=0 | bien_nhan_v2: 240 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 293
TỔNG: ĐẠT
python3 ops/land_evidence_nguon.py --root . | rc=0 | land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
python3 .claude/dev/packet_loop.py doctrine-scan --root . | rc=0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
python3 scripts/tl.py doc-claims-check --json | rc=0 | {"ok": true, "strict": false}
```
- kết luận: KHÔNG PHẢI LỖI. Log đầy đủ và rc tại review_evidence/*.stdout/*.stderr/*.rc; checks.json.

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

### HƯỚNG 9: Lời khai mới do 05bc12e ghi thêm
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/new_claims.py; sha256sum -c SHA256SUMS; git show <OID>:<path>`
- output thật:
```text
{
  "receipt_verdict_bytes_sha256": {
    "bytes": 32324,
    "hash": "d36248f584d4a3fb2c55a677587ee003ba1e338dd1701a50e48b4c59e2f0e346",
    "matches": true
  },
  "run_id_head_surface": {
    "run_id": "7a86ed4f591e4a50954f81d550f4d437",
    "head": "22382d8c800bed7b995d093cdcfdc206360d7fd4",
    "ref": "HEAD",
    "execution_surface": "codex_cli",
    "transport": "machine",
    "ma_thoat": 0,
    "trang_thai": "xong",
    "worktree_sach": true,
    "thoi_luong_giay": 1457.827
  },
  "prompt_sha256_match": true,
  "reviewed_tree_match": true,
  "model_events": {
    "count": 39,
    "response_ids": 39,
    "models": [
      "gpt-6.1-sol"
    ]
  },
  "stdout_run_hash_and_byte_match": true,
  "stderr_run_hash_and_byte_match": true,
  "evidence_blob_matches": true,
  "evidence_oid": "825dab1c8771113caeb3c5b77c61e89e27d7e292",
  "receipt_addition_commit": [
    "05bc12e2b9008071ca28edbd4574e58644d48220"
  ],
  "artifact_commit_parent": "22382d8c800bed7b995d093cdcfdc206360d7fd4",
  "receipt_commit_parent": "825dab1c8771113caeb3c5b77c61e89e27d7e292",
  "new_caveats_rows": [
    {
      "id": "HINT-LUOT6-AP-CUNG-COMMIT-GHI-SO",
      "rows": 1,
      "exact_description": true
    },
    {
      "id": "LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI",
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
    "ok_count": 120,
    "failed": [],
    "stderr": ""
  },
  "land_round6_sha_and_receipt_match": true
}
```
- kết luận: KHÔNG PHẢI LỖI ở những lời khai mới này; mô tả finding thuộc verdict 22382d8, không coi là tự khai surface hoặc trạng thái hiện hành của mọi receipt.

### HƯỚNG 8: Tự khai execution surface và nguồn runtime
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `python3 review_evidence/surfaces.py; rg -n -i "codex.service|service/api|execution.surface|surface:" cay-kho/ops/reviews --glob "*-verdict.md" --glob "VERDICT.md"`
- output thật:
```text
verdict_files_repo_wide=415 distinct_content=397
run_json_files=50 parse_errors=[]
receipt_runtime_pairs=18 mismatches=[]
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

### HƯỚNG 5: Xoá hàng/caveat mới trên clone độc lập
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `git clone --no-hardlinks --no-checkout mirror.git <tmp>/copy; git -C <copy> checkout --detach 05bc12e2b9008071ca28edbd4574e58644d48220; python3 review_evidence/mutations.py`
- output thật:
```text
clone=/tmp/pr896-r7-mutations-rblaixtc/copy
checkout=05bc12e2b9008071ca28edbd4574e58644d48220
[
  {
    "mutation": "remove-round6-index",
    "removed_bytes": 739,
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
          "!!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: verdict 'pr896-review-6-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó.",
          "  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: verdict 'pr896-review-6-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó."
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
    "mutation": "remove-round6-caveat-readme",
    "removed_bytes": 365,
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
          "!!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: caveat 'HINT-LUOT6-AP-CUNG-COMMIT-GHI-SO' của pr896-review-6-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-6-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.",
          "  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'HINT-LUOT6-AP-CUNG-COMMIT-GHI-SO' của pr896-review-6-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-6-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó."
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
    "mutation": "remove-round6-receipt-caveat",
    "removed_bytes": 361,
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

### HƯỚNG 6: Đóng finding ancestry lượt 6 và đo lại các mốc cũ
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/closure_round6.py; git show <anchor>:<receipt>; git log -1 <anchor> -- <receipt>; git merge-base --is-ancestor <OID> <target>`
- output thật:
```text
round6_historical_fields=4 all_text_and_anchor_match=True
round6_v1_corrections=3 all_frozen_hash_row_match=True
older_historical_fields=48 all_anchor_adds_receipt=True
all_ancestry_measurements=176 all_rc0=True
ops/reviews/wp461-review-1-codex-verdict.receipt.yaml / anchor.cuong_do anchor=77f272d435b0c23369b2348efa821c760d653036 source=ef72264cb268643a89df3e15cf6cb840da92307b rc=[0, 0, 0, 0]
ops/reviews/wp461-review-1-codex-verdict.receipt.yaml / lich_su_ban_ung_vien.ghi_chu anchor=77f272d435b0c23369b2348efa821c760d653036 source=ef72264cb268643a89df3e15cf6cb840da92307b rc=[0, 0, 0, 0]
ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml / anchor.cuong_do anchor=62c2fceecac4d3e114f0ecfcb0980dc67514e0ee source=b2134a40243e5cb3ea6d64eaf49a4c9f26794cbc rc=[0, 0, 0, 0]
ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml / lich_su_ban_ung_vien.ghi_chu anchor=62c2fceecac4d3e114f0ecfcb0980dc67514e0ee source=b2134a40243e5cb3ea6d64eaf49a4c9f26794cbc rc=[0, 0, 0, 0]
ops/reviews/doctor-github-mcp-review-6-codex-verdict.receipt.yaml / receipt_khong_khai.0 anchor=b9d6a8199d343e4c0458501f636d4b39e423c950 source=4920113a639d81385c0f98b1488c0f497776d2ff rc=[0, 0, 0, 0]
ops/reviews/don-nhanh-base-review-4-claude-verdict.receipt.yaml / truy_xuat_ghi_chu anchor=f99c6f172a8bc7bb641a07d6499299bca906c611 source=03f12ac63284dd814dcf14664968af4872ef7f8a rc=[0, 0, 0, 0]
ops/reviews/don-nhanh-base-review-5-claude-verdict.receipt.yaml / truy_xuat_ghi_chu anchor=f99c6f172a8bc7bb641a07d6499299bca906c611 source=03f12ac63284dd814dcf14664968af4872ef7f8a rc=[0, 0, 0, 0]

```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 11: Đính chính surface của ba verdict provenance land
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/land_round6.py; sha256sum <verdict>; read same-round run JSON/transcript and land.review.luot_1`
- output thật:
```text
corrected_land_verdicts=3
ops/land/pr832-wp831-provenance/verdict-luot7/wp831-g1-luot7-codex-verdict.md:6
SELF: Reviewer độc lập OpenAI Codex, họ GPT-6 theo chỉ dẫn runtime; `provider: openai_codex`, `execution_surface: codex_service` (API agent có shell), `transport: machine`. Không đo model variant/effort, launcher receipt hoặc assurance live. Executor Claude theo assignment. Agent `tl_auditor` chỉ đọc hướng dẫn, mã và log theo `CLAUDE.md` §Quy trình sửa code/5; không chạy test hay sửa tệp.
HASH: 1e27ba6bf2c4690a470b7786fe799c850b5924352a85a24460fb5053ff216d28 hash_matches_caveat=True same_prev=True same_master=True
SOURCE: ops/land/pr832-wp831-provenance/verdict-luot7/run.json
run=1ff81cba41874a218b53275d3cdc1418 head=51ae5c095972611d2c6045bd81786a4fc7e9ca62 surface=codex_cli transport=machine program=codex same_round_head=True caveat_source_head_run_match=True
CAVEAT: Verdict dong 6 tu khai execution_surface codex_service, nhung ops/land/pr832-wp831-provenance/verdict-luot7/run.json (run 1ff81cba41874a218b53275d3cdc1418, head 51ae5c095972611d2c6045bd81786a4fc7e9ca62, lenh.chuong_trinh=codex) ghi execution_surface=codex_cli, transport=machine. Dinh chinh be mat cua CHINH luot nay thanh codex_cli. Giu nguyen byte verdict lich su; khong chung thuc model/effort hay nang assurance/quyen merge/land.
ops/land/pr848-wp744-provenance/verdicts/wp744-g3-luot1-codex-verdict.md:36
SELF: - Reviewer: Codex/OpenAI, `model_family: openai`, phiên API có công cụ shell (`execution_surface: codex_service`, `transport: machine`). Họ model theo định danh hệ thống của phiên; không có header CLI/metadata backend riêng để máy đối chứng tên model chi tiết, effort hoặc session ID. Executor Claude theo assignment/commit, không đo lại runtime Executor. Verdict nội dung này không tự ghi transition hay receipt `cross_approved`.
HASH: af2b5fa426a7d53755148f4f9711712246afadc91e1d75e5267f8c8023bc3911 hash_matches_caveat=True same_prev=True same_master=True
SOURCE: ops/land/pr848-wp744-provenance/verdicts/run-f65e544e.json
run=f65e544ef5d64ba7a1e0edb607edcf0a head=23bc189f28ea60f04ca1634b6fe66d02babf12ed surface=codex_cli transport=machine program=codex same_round_head=True caveat_source_head_run_match=True
CAVEAT: Verdict dong 36 tu khai execution_surface codex_service, nhung ops/land/pr848-wp744-provenance/verdicts/run-f65e544e.json (run f65e544ef5d64ba7a1e0edb607edcf0a, head 23bc189f28ea60f04ca1634b6fe66d02babf12ed, lenh.chuong_trinh=codex) ghi execution_surface=codex_cli, transport=machine. Dinh chinh be mat cua CHINH luot nay thanh codex_cli. Giu nguyen byte verdict lich su; khong chung thuc model/effort hay nang assurance/quyen merge/land.
ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-verdict.md:3
SELF: - Reviewer: OpenAI Codex (GPT-6 family as identified by session instructions); provider `openai_codex`; execution surface `codex_service` with local shell tools; transport machine/tool-mediated. Exact serving-model/effort attestation is not independently measured. Independent reviewer in this session; no executor role.
HASH: 95438373ee2f04a8431e6b10cfd2111144f9744bc54ac114c5670e0652e1ce87 hash_matches_caveat=True same_prev=True same_master=True
SOURCE: ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-transcript.txt
header=['OpenAI Codex v0.163.0', '--------', 'workdir: /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv21', 'model: gpt-6-astra', 'provider: openai', 'approval: never', 'sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)', 'reasoning effort: xhigh', 'reasoning summaries: none', 'session id: 01a157da-2170-7be2-b6d0-053fa8f91aec', '--------', 'user', '# Independent read-only review — WP748 r21/g21, PR #862, exact head']
luot1=verdicts/wp748-r21-luot1-codex-transcript.txt: codex exec truc tiep, KHONG bien nhan launcher — KHONG tinh assurance.
source_and_session_in_caveat=True
CAVEAT: Verdict luot 1 dong 3 tu khai codex_service, nhung ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-transcript.txt bat dau bang OpenAI Codex v0.163.0, session 01a157da-2170-7be2-b6d0-053fa8f91aec; review.luot_1.reviewer cua ho so nay ghi codex exec truc tiep. Dinh chinh be mat luot 1 thanh codex_cli. Khong dung run-f0909b38.json cua LUOT 2 de chung minh luot 1. Giu nguyen byte verdict lich su; khong chung thuc model/effort hay nang assurance/quyen merge/land.

```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 12: Hai tự khai service còn trái hồ sơ land, nguồn runtime vắng
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/unresolved_land_surface.py; read exact verdict headers, YAML review/khong_do_duoc, saved same-round comment; index all run*.json`
- output thật:
```text
unresolved_land_surface_disagreements=2
ops/land/pr823-wp802-provenance/verdict-luot5/wp802-g1-luot5-codex-verdict.md:6
SELF: Reviewer OpenAI Codex; provider `openai_codex`, execution surface `codex_service` (API agent có shell), transport `machine`. Model ID/effort/session ID và danh tính executor thực chạy chưa có receipt độc lập: **KHÔNG ĐO ĐƯỢC**. Không suy surface từ lease, không tự cấp assurance hoặc quyền merge/land. Áp ngưỡng assignment: hết P0/P1 và mọi P2 đóng; P3 mở cần quyết định chủ kho.
head=5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456 hash=b6ee86d0c9e523dfbe87718d12b4d646464e7a8720e9789f071f4aa04d6e3f01 same_master=True same_prev=True
LAND review.so_loi_goi_codex_cli=5; luot_cuoi.reviewer=codex qua launcher.py run, run b3d8a108 (thuat_lai — comment 6247520447: 1092s, ma_thoat 0; commit c25d0f8 ghi nham id run).; ket_qua=thuat_lai — approve, P0=0 P1=0 P2=0 P3=0 tren 5c6c7a8 = head merge.; saved_comment_round_and_head_match=True
matching_run_records=0 surface_caveats=[]
LIMITS: ['Log day du cac job CI KHONG luu; chi readback run/job/check-run.', 'gate-registry (ubuntu-latest) cua run 39112158391 chua xong luc ghi (ban dau); 19-10 da doc lai: xanh (readback-jobs-39112158391-cuoi.json).', 'stderr/transcript luot review Codex KHONG luu; model thuc chay KHONG_DO_DUOC.']
ops/land/pr877-wp854-provenance/verdicts/wp854-g1-luot2-codex-verdict.md:11
SELF: Provider: OpenAI/Codex, model_family=openai; công cụ shell Linux trong phiên agent (`codex_service`, transport=machine). Không tự xác nhận served-model, launcher attestation, GitHub submitter hoặc cấp receipt/assurance. Review theo hai trục spec và standards/security, lớp sensitive; không merge, push, deploy hoặc gọi LIVE.
head=b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb hash=612e86d854f4a7aad84a5f8e8d5986f58677e1b789d6ad3f176fefd1435cf277 same_master=True same_prev=True
LAND khong_do_duoc.0=Model thuc phuc vu cac luot review KHONG_DO_DUOC (chi co header CLI gpt-6.1-sol xhigh).
matching_run_records=0 surface_caveats=[]
LIMITS: ['Model thuc phuc vu cac luot review KHONG_DO_DUOC (chi co header CLI gpt-6.1-sol xhigh).', 'Merge bam tay hay qua mot phien dung credential chu kho: KHONG_DO_DUOC (chi co merged_by).']
No actual execution surface selected: CLI references are secondary declarations without matching run.json/transcript. The measured defect is missing qualification of contradictory surface declarations, not proved runtime falsity.
```
- kết luận: LỖI P2 surface-tu-khai-khac-ho-so-land-chua-co-caveat; không đủ nguồn để kết luận bề mặt thực chạy hoặc nâng thành P1.

### HƯỚNG 10: Quét rộng trạng thái review/áp hint/merge trong sổ và land
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/inventory.py; python3 review_evidence/status_checks.py; git merge-base --is-ancestor <OID> <master/candidate>; git ls-tree <ref> -- <spec>; compare exact verdict reviewed_sha`
- output thật:
```text
yaml_paths=368 inventory_counts={'unanchored_candidates': 1759, 'anchored_candidates': 398, 'readme': 517}
No-review negatives checked against flat receipts AND verdict headers in ops/reviews + land provenance:
17f4a1b85b8d5146c5e6dddbdc40f11111a659f7 receipts=0 verdict_headers=0
efa397eb2515658a1e3e9b4cdfd6e887b492b957 receipts=0 verdict_headers=0
99aef141796ebce7044c9f5c0c8a1a3b3d673d8e receipts=0 verdict_headers=0
5a96c1ac8cec1c9958094f92e716941faa47aac5 receipts=0 verdict_headers=0
888c0d9b68136f384068ecad8e286819bb175044 receipts=0 verdict_headers=0
bf10fab792473bc69dd377c7445978950c4d77a0 receipts=0 verdict_headers=0
288ad3ea79ef94e061b649effe7bee2c7e2a0a9b receipts=0 verdict_headers=0
b5b6aefa66a8ad037ff34430d0210f3b6873913f receipts=0 verdict_headers=0
3ddda026da41b0bb162a3785b93dbb953a298203 receipts=0 verdict_headers=0
4bc94325e647ee5e32373f3af30b8f83b98a90fa ancestry rc(master,candidate)=[1, 1]
604b8d9a7c5948a9c0690312f1220830d545b52c ancestry rc(master,candidate)=[1, 1]
82359c4deec90edebbaebf9ab9d094902120b567 ancestry rc(master,candidate)=[1, 0]
2e4183bc2dc40e6bc306e377fc442ff0f405bbe0 ancestry rc(master,candidate)=[1, 0]
1a276a15192013fdb1e472db409133b53ac57944 ancestry rc(master,candidate)=[1, 0]
d308b0b1bbcb0db2e1624e4eda6431f73ace453f ancestry rc(master,candidate)=[1, 0]
22382d8c800bed7b995d093cdcfdc206360d7fd4 ancestry rc(master,candidate)=[1, 0]
825dab1c8771113caeb3c5b77c61e89e27d7e292 ancestry rc(master,candidate)=[1, 0]
05bc12e2b9008071ca28edbd4574e58644d48220 ancestry rc(master,candidate)=[1, 0]
ops/specs/wp775.md ls-tree master='' candidate=''
ops/specs/wp484-r8.md ls-tree master='' candidate=''
HINT history {'historical': 'c8c1ee015f78fdb143a18cf926f9f3481c2a3dd1', 'apply_commit': '2e4183bc2dc40e6bc306e377fc442ff0f405bbe0', 'apply_parent': 'c8c1ee015f78fdb143a18cf926f9f3481c2a3dd1', 'direct_child': True}
HINT history {'historical': '77a0a458c6c06f3aafa118953e8e2771daaed911', 'apply_commit': '1a276a15192013fdb1e472db409133b53ac57944', 'apply_parent': '77a0a458c6c06f3aafa118953e8e2771daaed911', 'direct_child': True}
Land provenance status scan: 415 distinct paths; supplementary matches classified with context. pr696.do_luc pins bc57bca and 2026-09-30; pr684.packet_landed_ghi_chu explicitly says TAI THOI DIEM merge #684 and current #689 state must not be read from that file. Findings narrated under reviewed_sha are historical; absent CI or land authority is not a claim of unmerged Git state.

```
- kết luận: KHÔNG PHẢI LỖI mới về trạng thái trong các đối chiếu nêu trên; các bản ghi lịch sử có mốc được giữ nguyên, không suy trạng thái land từ Git.

### HƯỚNG 15: PR #490 còn bị ghi chưa merge trong một hàng bookkeeping hiện hành
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `git blame -L 241,248 05bc12e2b9008071ca28edbd4574e58644d48220 -- ops/land/pr491-r358-ghi-so-land-evidence.yaml; git show -s --format="%H %P %s" 8cee9410e958a6b9d956e080c11878fbd80d9f5f; git merge-base --is-ancestor 8cee9410e958a6b9d956e080c11878fbd80d9f5f <cdd0b1d/master/candidate>; Python read YAML bookkeeping.4`
- output thật:
```text
{
  "path": "ops/land/pr491-r358-ghi-so-land-evidence.yaml",
  "field": "bookkeeping.4",
  "line": 244,
  "text": "NỢ CŨ KHÔNG ĐỘNG TỚI: `_kiem_bia_mo` dùng `any(...)` trong `ops/lease_publish.py:606` vẫn nguyên trên master · nợ A9 (bốn lease GATE cấp trước hạn #456, `generation` giữ 1, lệch `ADR-0034`) chờ quyết định chủ kho · Issue #463–#467 còn `open` · PR #479 và #490 chưa merge. Bốn câu này là THUẬT LẠI theo hồ sơ chuỗi #468→#489, trừ câu về `any(...)` đã đo lại trên `origin/master`; trạng thái Issue/PR chưa hỏi lại API trong đợt này.",
  "original_anchor": "cdd0b1d19439e286fb7a86020ce2d258bafc2102",
  "same_scalar_at_original": true,
  "merge490": "8cee9410e958a6b9d956e080c11878fbd80d9f5f 00e017af102bc8355e0c276d2d813e20620ddb42 01e7f77d707cb093b5ba6d9b9d8577f40d025488 Merge pull request #490 from ducthangho/claude/handoff-tra-luat-repo-2ak5th",
  "ancestry": [
    {
      "target": "cdd0b1d19439e286fb7a86020ce2d258bafc2102",
      "rc": 1
    },
    {
      "target": "3e973a03b151e37cd402e0a723816eeaa8247193",
      "rc": 0
    },
    {
      "target": "05bc12e2b9008071ca28edbd4574e58644d48220",
      "rc": 0
    }
  ],
  "current_original_has_history_marker": false,
  "master_blob": "100644 blob 1d97784146c8c031e1dbba14c8db5ea560d58bff\tops/land/pr491-r358-ghi-so-land-evidence.yaml"
}
```
- kết luận: LỖI P1 pr490-chua-merge-trai-lich-su-git; nhãn THUẬT LẠI chỉ phân loại nguồn, chưa neo trạng thái vào mốc lịch sử.

### HƯỚNG 13: Gợi ý vá tài liệu trên clone exact SHA
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py; patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>; patch --batch --fuzz=0 -p0 -i <HINT.patch>`
- output thật:
```text
patch_paths=3 dry_run_rc=0 apply_rc=0
checking file ops/land/pr491-r358-ghi-so-land-evidence.yaml
checking file ops/land/pr823-wp802-land-evidence.yaml
checking file ops/land/pr877-wp854-land-evidence.yaml
YAML parsed; 3/3 applied files byte-match intended text. No receipt v1 or verdict modified.
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 14: Đo lại hint bằng ca và cổng sẵn có trên clone
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/hint_checks.py; seven existing commands with cwd <copy>`
- output thật:
```text
python3 ops/lease_publish_test.py --chi-ca=t26_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t27_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t138_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/bien_nhan_v2.py --root . | rc=0 | bien_nhan_v2: 240 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 293
TỔNG: ĐẠT
python3 ops/land_evidence_nguon.py --root . | rc=0 | land_evidence_nguon: 48 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
python3 .claude/dev/packet_loop.py doctrine-scan --root . | rc=0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
python3 scripts/tl.py doc-claims-check --json | rc=0 | {"ok": true, "strict": false}
```
- kết luận: KHÔNG PHẢI LỖI của hint.

### HƯỚNG 16: Lời khai mới về hiện vật của lần chạy hỏng
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/failed_run_claims.py; wc -c <VERDICT.partial.md>; rg -n "^### |^verdict:" <VERDICT.partial.md>; compare failed/counting run JSON`
- output thật:
```text
{
  "failed_run_id": "c0fa33fa91f34a3db8450d2e75dd6071",
  "same_head_as_counted_run": true,
  "same_prompt_as_counted_run": true,
  "rc": 1,
  "duration": 349.795,
  "partial_first_line": "verdict: dang_lam",
  "partial_bytes": 28214,
  "partial_sha256": "1d3f44f96f638c8224656b33385acf074ea2b168286a819dca4acbd0763ef869",
  "partial_h3_count": 14,
  "partial_h3_titles": [
    "Tiến độ phép đo t26",
    "Tiến độ phép đo t27",
    "Tiến độ phép đo t138",
    "Tiến độ phép đo bien_nhan",
    "Tiến độ phép đo land",
    "Tiến độ phép đo doctrine",
    "Tiến độ phép đo doc_claims",
    "H1-history",
    "H2-integrity",
    "H4-review-states",
    "H5-remove_new_readme_row",
    "H5-remove_new_receipt_caveat",
    "H3-ancestry",
    "H4-review-states"
  ],
  "error_excerpt": "\"error\":{\"message\":\"Selected model is at capacity. Please try a different model.\",\"codex_error_info\":\"server_overloaded\"}\n",
  "receipt_description": "Run c0fa33fa (cung prompt, cung head) ma_thoat 1 sau 349.795 s: transcript codex ghi server_overloaded \"Selected model is at capacity\". VERDICT.partial.md chi co dong dang_lam + mot phep do t26; KHONG duoc tinh la verdict. Hien vat o luot-hong-c0fa33fa/.",
  "readme_lines": [
    766
  ]
}
```
- kết luận: LỖI P1 mo-ta-partial-luot6-khong-khop-hien-vat: receipt và README mới khai chỉ một phép đo t26, trong khi tệp có 14 mục; vẫn dang_lam và không phải verdict hoàn tất.

### HƯỚNG 14: Đo lại hint bằng ca và cổng sẵn có trên clone
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/hint_checks.py; seven existing commands with cwd <copy>`
- output thật:
```text
python3 ops/lease_publish_test.py --chi-ca=t26_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t27_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t138_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/bien_nhan_v2.py --root . | rc=0 | bien_nhan_v2: 240 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 293
TỔNG: ĐẠT
python3 ops/land_evidence_nguon.py --root . | rc=0 | land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
python3 .claude/dev/packet_loop.py doctrine-scan --root . | rc=0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
python3 scripts/tl.py doc-claims-check --json | rc=0 | {"ok": true, "strict": false}
```
- kết luận: KHÔNG PHẢI LỖI của hint.

### HƯỚNG 13: Gợi ý vá tài liệu trên clone exact SHA
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py; patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>; patch --batch --fuzz=0 -p0 -i <HINT.patch>`
- output thật:
```text
patch_paths=5 dry_run_rc=0 apply_rc=0
checking file ops/land/pr491-r358-ghi-so-land-evidence.yaml
checking file ops/land/pr823-wp802-land-evidence.yaml
checking file ops/land/pr877-wp854-land-evidence.yaml
checking file ops/reviews/README.md
checking file ops/reviews/pr896-review-6-codex-verdict.receipt.yaml
YAML parsed; 5/5 applied files byte-match intended text. No receipt v1 or verdict modified.
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 14: Đo lại hint bằng ca và cổng sẵn có trên clone
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/hint_checks.py; seven existing commands with cwd <copy>`
- output thật:
```text
python3 ops/lease_publish_test.py --chi-ca=t26_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t27_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t138_ | rc=0 | 
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/bien_nhan_v2.py --root . | rc=0 | bien_nhan_v2: 240 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 293
TỔNG: ĐẠT
python3 ops/land_evidence_nguon.py --root . | rc=0 | land_evidence_nguon: 48 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
python3 .claude/dev/packet_loop.py doctrine-scan --root . | rc=0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
python3 scripts/tl.py doc-claims-check --json | rc=0 | {"ok": true, "strict": false}
```
- kết luận: KHÔNG PHẢI LỖI của hint.

### HƯỚNG 17: Toàn vẹn cuối cây gốc và bản sao hint
- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/final_checks.py; git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored; git diff --exit-code; sha256sum <verdict manifests>`
- output thật:
```text
{
  "reviewed_tree_unchanged": {
    "rev-parse HEAD HEAD^{tree}": {
      "rc": 0,
      "stdout": "05bc12e2b9008071ca28edbd4574e58644d48220\n3412a314b129d1ee1473e528a5ec438378ccebe5\n",
      "stderr": ""
    },
    "status --porcelain=v1 --untracked-files=all --ignored": {
      "rc": 0,
      "stdout": "",
      "stderr": ""
    },
    "diff --exit-code": {
      "rc": 0,
      "stdout": "",
      "stderr": ""
    },
    "rev-parse --is-shallow-repository": {
      "rc": 0,
      "stdout": "false\n",
      "stderr": ""
    },
    "config core.abbrev": {
      "rc": 0,
      "stdout": "7\n",
      "stderr": ""
    }
  },
  "clone_changed_paths": [
    "ops/land/pr491-r358-ghi-so-land-evidence.yaml",
    "ops/land/pr823-wp802-land-evidence.yaml",
    "ops/land/pr877-wp854-land-evidence.yaml",
    "ops/reviews/README.md",
    "ops/reviews/pr896-review-6-codex-verdict.receipt.yaml"
  ],
  "hint_yaml_parsed_unique_ids": 4,
  "hint_receipt_readme_description_match": true,
  "hint_modified_verdicts": [],
  "hint_frozen_v1_unchanged": 53,
  "manifest_summary": {
    "manifest_verdict_entries": 137,
    "all_match": true,
    "missing": [],
    "mismatches": []
  },
  "hint_sha256": "65e791768d947ee83be72e846274b0ce59ad6e230a20cb67fb6b5b43255bdff6"
}
```
- kết luận: KHÔNG PHẢI LỖI.
