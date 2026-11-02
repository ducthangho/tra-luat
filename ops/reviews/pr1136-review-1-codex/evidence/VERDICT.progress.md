Verdict: request_changes
Reviewed commit: 1a87a863174ef104b2df8bc98b77724fb6796d9b

Đang đo; verdict tạm thời, chưa kết luận finding. Chưa hoàn tất điều kiện approve.
Các phép đo dùng PYTHONDONTWRITEBYTECODE=1 và core.abbrev=7 qua audit.gitconfig trong sandbox; chỉ ghi trong sandbox/bản sao tạm.

Đo cổng (lệnh chạy tại work/base hoặc work/head; log đầy đủ evidence/gates.json):

| Cổng | base rc | HEAD rc |
|---|---:|---:|
| bien-nhan | 0 | 0 |
| land | 0 | 0 |
| direct | 0 | 0 |
| doctrine | 0 | 0 |
| diff-ci | 0 | 0 |
| diff-default | 0 | 2 |

Đối chiếu byte — `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py`:
```json
{
  "counted": {
    "source_count": 86,
    "stored_count": 81,
    "mismatch": [],
    "generated_or_unknown": [],
    "missing_source": [
      "DIFF.patch",
      "evidence/history-attempt1.json",
      "evidence/history.json",
      "evidence/original-before.json",
      "launcher.err"
    ],
    "undeclared_missing": [],
    "omitted_mismatch": [],
    "declared_but_not_missing": [],
    "sha256sum_rc": 0,
    "manifest_count": 89,
    "manifest_uncovered": [],
    "manifest_extra": [],
    "manifest_duplicates": []
  },
  "failed": {
    "source_count": 8,
    "stored_count": 6,
    "mismatch": [],
    "generated_or_unknown": [],
    "missing_source": [
      "DIFF.patch",
      "launcher.err"
    ],
    "undeclared_missing": [],
    "omitted_mismatch": [],
    "declared_but_not_missing": [],
    "sha256sum_rc": 0,
    "manifest_count": 7,
    "manifest_uncovered": [],
    "manifest_extra": [],
    "manifest_duplicates": []
  },
  "flat": {
    "matches": true,
    "sha256": "c601112323513db31e0aefc40340672d69fba39567e3f8639b3ebdd53fd321e6",
    "bytes": 20188
  },
  "diff_reproduction": {
    "bytes": 946152,
    "sha256": "b3cd603ebe29f46e0d614306e3d050f77fa3a653eadd31cf12c6dc3c1fe760d2",
    "matches_a": true,
    "matches_b": true
  },
  "whitespace": {
    "sha256": "5f3cdf640f3de69333ac6364b42cdf52a6bc5bad5873f8386b1ab85b56e667bb",
    "bytes": 5382,
    "source_matches": true,
    "trailing_whitespace_lines": [
      2,
      3,
      4,
      6,
      28,
      50,
      58,
      61,
      62,
      64,
      71,
      75,
      76,
      80
    ]
  }
}
```

Đột biến — `python3 mutate_receipt.py` đổi riêng ký tự đầu verdict_sha256 của biên nhận mới trên work/mutant, rồi hồi nguyên:
```json
[
  {
    "name": "bien-nhan",
    "command": [
      "python3",
      "ops/bien_nhan_v2.py",
      "--root",
      "."
    ],
    "rc": 1,
    "errors": [],
    "tail": [
      "",
      "bien_nhan_v2: 295 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 1 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 349",
      "câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0"
    ]
  },
  {
    "name": "direct",
    "command": [
      "python3",
      "/tmp/claude-0/-home-user-tra-luat/67a05166-68ea-5948-af9b-66d84beeae6e/scratchpad/review1136a/direct_gates.py",
      "."
    ],
    "rc": 1,
    "errors": [
      "t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi FAIL pr1131-review-1-codex-verdict.receipt.yaml: LỆCH BĂM — biên nhận khai d601112323513db31e0aefc40340672d69fba39567e3f8639b3ebdd53fd321e6, tệp 'ops/reviews/pr1131-review-1-codex-verdict.md' thực c601112323513db31e0aefc40340672d69fba39567e3f8639b3ebdd53fd321e6. Tệp verdict là NGUYÊN VĂN của reviewer: hoặc bạn vừa sửa nhầm nó, hoặc biên nhận chưa cập nhật. Đừng ghi đè băm cho hết đỏ trước khi biết là ca nào."
    ],
    "tail": [
      "t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi FAIL pr1131-review-1-codex-verdict.receipt.yaml: LỆCH BĂM — biên nhận khai d601112323513db31e0aefc40340672d69fba39567e3f8639b3ebdd53fd321e6, tệp 'ops/reviews/pr1131-review-1-codex-verdict.md' thực c601112323513db31e0aefc40340672d69fba39567e3f8639b3ebdd53fd321e6. Tệp verdict là NGUYÊN VĂN của reviewer: hoặc bạn vừa sửa nhầm nó, hoặc biên nhận chưa cập nhật. Đừng ghi đè băm cho hết đỏ trước khi biết là ca nào.",
      "t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc PASS",
      "t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen PASS",
      "DIRECT total=3 failed=1"
    ]
  }
]
```

Biên nhận/README — `python3 audit_receipt.py` → 85 đối chiếu, mismatches=[{'field': 'base_sha', 'expected': '180039c4b791fba4c89991623151cbb7378fce53', 'observed': 'c165a5d0d4048e10e7da875f2ba7524136fb5735', 'matches': False}]; README +5/-0; toàn bộ giá trị đo tại evidence/receipt.json. Chi tiết 401/credential rev 3: KHÔNG ĐO ĐƯỢC từ log đã lưu.

Biên nhận/README — `python3 audit_receipt.py` → 85 đối chiếu, mismatches=[]; README +5/-0; toàn bộ giá trị đo tại evidence/receipt.json. Chi tiết 401/credential rev 3: KHÔNG ĐO ĐƯỢC từ log đã lưu.

CI local — `python3 audit_ci.py`: kết quả đầy đủ tại evidence/ci.json; {'base_function': [], 'head_function': [], 'local_kiem_re_rc': 0, 'local_kiem_re_stdout': 'DUONG_NHANH: toan bo 93 tep doi khop allowlist ops/{land,leases,reviews,specs}/** - dung duong nhanh\nDUONG_NHANH: kiem-re DAT (93 tep doi, 0 loi)\n', 't20d': 'PASS', 'ast_scan_files': 154, 'ast_parse_errors': []}

Kiểm tra cuối — `python3 finish_integrity.py`:
```json
{
  "files_before": 10905,
  "files_after": 10905,
  "added": [],
  "removed": [],
  "modified": [],
  "head": "1a87a863174ef104b2df8bc98b77724fb6796d9b",
  "status": ""
}
```
