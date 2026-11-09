Human audit — bản ghi theo xác nhận thực tế của chủ kho, PR #1294 / wp1285 r8/g9.

Nguyên văn lời người audit: “Tôi đã đọc và xác nhận approve trên cả 2 trục, hãy đăng cho tôi, sau đó merge, land và ghi sổ”. Xác nhận này trả lời câu hỏi tự đọc hồ sơ H4 và approve cả hai trục spec, standards/security. Người audit: ducthangho, độc lập với tác giả sản phẩm thực tế Codex CLI. Codex dispatcher chỉ ghi/vận chuyển theo yêu cầu, không đóng vai người audit.

```json
{
  "schema": "human_supplemental_exact_head_audit.v1",
  "packet": "wp1285",
  "revision": 8,
  "generation": 9,
  "pr": 1294,
  "reviewed_sha": "ecd8cee3ea6da6513a37a9b9aa6c9db65472e41c",
  "reviewed_tree": "ebe647c4bc68fb75b3ad7319a79ad3bf0f143a70",
  "spec_sha256": "d8195383ceed002d15b9db09e51cae1c4f2d90f0237ef33333cead4d629b26e9",
  "human_reviewer_github": "ducthangho",
  "execution_surface": "manual_audit",
  "transport": "human",
  "personally_read_spec_diff_confirmed": true,
  "review_axes": [
    "spec",
    "standards_security"
  ],
  "verdict": "approve",
  "assurance": "human_audited",
  "source_statement_verbatim": "Tôi đã đọc và xác nhận approve trên cả 2 trục, hãy đăng cho tôi, sau đó merge, land và ghi sổ",
  "source_context": "Direct reply to question asking personal reading and own approval on spec and standards/security for the linked immutable exactH4 r8 bundle. Realhuman statement, not generated model audit.",
  "evidence_bundle": "https://github.com/ducthangho/tra-luat/blob/5dfbfb96b00402f53f1a72187ce98e944dcabfbc/ops/checkpoints/wp1285-r8-human/audit-bundle/HUMAN-AUDIT.md",
  "evidence_bundle_sha256": "8d375e17260e7e4f5cdeb8fa19b6f4e29f488611139e841fa28af3781c274505",
  "accepted_P3": {
    "finding": "WP1285-R7-F01",
    "slug": "manifest-requires-guard-comment-regex",
    "waiver": "https://github.com/ducthangho/tra-luat/pull/1294#issuecomment-6731269220",
    "debt": "https://github.com/ducthangho/tra-luat/issues/1295",
    "fixed": false,
    "blanket_waiver": false
  },
  "other_findings_reported_by_human": [],
  "actual_reading_time": "Confirmed before this owner instruction; exact earlier reading time not measured, no backdating",
  "recorded_at_utc": "2026-11-09T04:00:04.973994+00:00",
  "recorded_by": "Codex dispatcher under explicit owner request to publish, not humanreviewer itself",
  "primary_M5_K4_source": "Actual Codex4 prepush sameH4 originalrun unchanged. This supplemental human audit is recorded now; no claim human-onlyK4 prepush passed.",
  "Claude5_original_failure": "Unchanged changes_requested/fullscopefalse/launcher16; not converted to approve or reused as assurance",
  "merge_land_authority": "Owner explicitly instructs publish then merge/land/bookkeeping, conditional remaining realgates/MCI/M8, no LIVE"
}
```

Approve exactH4 với P3 đã được chủ kho miễn và ghi nợ #1295; nợ chưa vá/đóng. Không miễn lỗi khác/SHA mới. Lượt Claude5 và gate snapshot thất bại giữ nguyên. Quyền merge/land đã cấp; tiếp tục kiểm tra gate/freshrefs/Ready auto-review, normalmerge rồi actualcanonicalMCI/M8/nhảlease/D1–D4. Chưa ghi merged/landed trước khi các bước ấy xảy ra.
