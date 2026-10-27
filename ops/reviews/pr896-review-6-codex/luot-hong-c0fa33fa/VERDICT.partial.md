verdict: dang_lam
reviewed_sha: 22382d8c800bed7b995d093cdcfdc206360d7fd4
Kết quả: đang đo.

Đã bắt đầu đọc prompt.snapshot. Chỉ đọc cây cay-kho/; mọi đột biến sẽ thực hiện trên bản sao ngoài cay-kho/.

### Tiến độ phép đo t26

Lệnh tại cay-kho/: `python3 ops/lease_publish_test.py --chi-ca=t26_`. rc=0.

```text
>>> vao t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 2026-10-26T14:03:41Z
<<< ra t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 2.655s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r6/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r6/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
```

### Tiến độ phép đo t27

Lệnh tại cay-kho/: `python3 ops/lease_publish_test.py --chi-ca=t27_`. rc=0.

```text
>>> vao t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 2026-10-26T14:03:41Z
<<< ra t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 5.227s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r6/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r6/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
```

### Tiến độ phép đo t138

Lệnh tại cay-kho/: `python3 ops/lease_publish_test.py --chi-ca=t138_`. rc=0.

```text
>>> vao t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 2026-10-26T14:03:41Z
<<< ra t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 0.397s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r6/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r6/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
```

### Tiến độ phép đo bien_nhan

Lệnh tại cay-kho/: `python3 ops/bien_nhan_v2.py --root .`. rc=0.

```text

bien_nhan_v2: 239 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 292
TỔNG: ĐẠT
```

### Tiến độ phép đo land

Lệnh tại cay-kho/: `python3 ops/land_evidence_nguon.py --root .`. rc=0.

```text
ĐẠT ops/land/pr931-wp835-land-evidence.yaml
ĐẠT ops/land/pr932-wp748-r26-land-evidence.yaml
ĐẠT ops/land/pr933-wp929-land-evidence.yaml
land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
```

### Tiến độ phép đo doctrine

Lệnh tại cay-kho/: `python3 .claude/dev/packet_loop.py doctrine-scan --root .`. rc=0.

```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
```

### Tiến độ phép đo doc_claims

Lệnh tại cay-kho/: `python3 scripts/tl.py doc-claims-check --json`. rc=0.

```text
    },
    "note": "tập tra cứu = CHANGELOG.md + references/changelog_archive/*.md, quét toàn văn; dưới sàn ⇒ advisory (khuyết của sổ, không phải trích dẫn sai)"
  },
  "strict": false
}
```

### H1-history

- giả thuyết: đo lại khẳng định được giao và tìm thể hiện cùng lớp.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history`
- output thật:
```text
{
  "head": "22382d8c800bed7b995d093cdcfdc206360d7fd4",
  "tree": "2424259c815d962a485bbbc52751499ed93ace34",
  "status": "",
  "shallow": "false",
  "diff.patch": {
    "bytes_equal": true
  },
  "numstat.txt": {
    "bytes_equal": true
  },
  "diff-pr947.patch": {
    "bytes_equal": true
  },
  "numstat-pr947.txt": {
    "bytes_equal": true
  },
  "commits": [
    "22382d8c800bed7b995d093cdcfdc206360d7fd4 ops: bien nhan cross-review luot 5 #896 + ap HINT luot 5 + khoi luot 5 ho so land",
    "d308b0b1bbcb0db2e1624e4eda6431f73ace453f ops/reviews: hien vat cross-review luot 5 #896 (codex, cham 1a276a1)"
  ],
  "clone_rc": 0,
  "hint_apply_rc": 0,
  "flat_verdict_equals_supplied": true,
  "hint_equals_stored": true,
  "hint_files": 10,
  "exact_hint_blob_matches": 9,
  "extra_diff": [
    {
      "path": "ops/reviews/README.md",
      "expected_sha256": "c837f5fcac72128180b7e401e337426a593d7bc00e6719125532ae8451688383",
      "actual_sha256": "672a3e4a4c69717a7e88b5d0316b43eb8469e3f11028ca5c8e5e32c86ecba78c",
      "byte_match": false,
      "diff": "--- after_hint\n+++ 22382d8\n@@ -758,6 +758,10 @@\n | `pr896-review-4-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong; phien ghi so do sau luot: HEAD 2e4183b, git status rong. |\n | `pr896-review-4-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (review_evidence/) tham chieu duong dan tuyet doi cua sandbox phien; tai lap can dung lai mirror tai 2e4183b. |\n | `pr896-review-4-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff-pr947.patch (>500 KB) KHONG vao kho; sha256/so byte o OMITTED.txt. |\n+| `pr896-review-5-codex-verdict.md` | `HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO` | Verdict lich su tren 1a276a1 la changes_requested 2 P1. HINT.patch luot 5 (10 tep) duoc ap NGUYEN (--fuzz=0) trong CHINH commit ghi so bien nhan nay, theo yeu cau chu kho \"va cho toi khi het P1, P2, P3\". Can verdict moi tren exact SHA ung vien; khong doi ket qua hay byte verdict lich su. |\n+| `pr896-review-5-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong; phien ghi so do sau luot: HEAD 1a276a1, git status rong. |\n+| `pr896-review-5-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (review_evidence/) tham chieu duong dan tuyet doi cua sandbox phien; tai lap can dung lai mirror tai 1a276a1. |\n+| `pr896-review-5-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff-pr947.patch va review_evidence/receipt-status-all.log (>500 KB) KHONG vao kho; sha256/so byte o OMITTED.txt. |\n \n ## Mục lục\n \n@@ -1054,6 +1058,7 @@\n | [`pr896-review-2-codex-verdict.md`](pr896-review-2-codex-verdict.md) | [`.receipt.yaml`](pr896-review-2-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/1/0/0 tren `8d56009` (head da merge #946, mang ban va P2 `3bc4244` + ban va P1 `a9bc934`) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run b3269a02`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · P2 luot 1 DA DONG; tai reviewed_sha 8d56009, P1 pr915-review-1 DONG MOT PHAN vi receipt pr889-review-1 chua co caveat surface; HINT.patch da ap tai 82359c4 (receipt + README), can verdict moi tren exact SHA ung vien · ban phang nguyen byte cua `pr896-review-2-codex/VERDICT.md`. Merge `21fe565`. | `8d56009a` | 66095 |\n | [`pr896-review-3-codex-verdict.md`](pr896-review-3-codex-verdict.md) | [`.receipt.yaml`](pr896-review-3-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/2/1/0 tren `82359c4` (head PR #947, mang HINT luot 2) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 513131e0`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · Tai reviewed_sha 82359c4: P1 luot 2 DA DONG; finding moi luc ay la P1 wp766, P1 ho so luot 2 va P2 13 verdict service/API. HINT.patch luot 3 da ap tai 2e4183bc2dc40e6bc306e377fc442ff0f405bbe0 (sau c8c1ee0); can verdict moi tren exact SHA ung vien · ban phang nguyen byte cua `pr896-review-3-codex/VERDICT.md`. Chua merge. | `82359c4d` | 34175 |\n | [`pr896-review-4-codex-verdict.md`](pr896-review-4-codex-verdict.md) | [`.receipt.yaml`](pr896-review-4-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/3/1/0 tren `2e4183b` (head PR #947, mang HINT luot 3) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 9b8d9a76`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · ba finding luot 3 DA DONG (P2 dong 13/13 the hien cu); moi: P1 hang muc luc luot 3 con khai HINT chua ap, P1 8 receipt con noi 'chua review', P1 23 receipt phu nhan ancestry da co, P2 pr526-review-3/slice-b-c-review-2 — phan lon NGOAI chuoi #896; HINT.patch luot 4 chua ap tai ff4ab57, da ap o commit ke tiep sau 77a0a45 · ban phang nguyen byte cua `pr896-review-4-codex/VERDICT.md`. Chua merge. | `2e4183bc` | 39386 |\n+| [`pr896-review-5-codex-verdict.md`](pr896-review-5-codex-verdict.md) | [`.receipt.yaml`](pr896-review-5-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/2/0/0 tren `1a276a1` (head PR #947, mang HINT luot 4) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 453628b5`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · muc luc luot 3 va P2 surface DA DONG; con: P1 7 truong ancestry sot trong chinh cac receipt luot 4 da neo, P1 pr870/pr889-review-1 con noi head 'khong duoc review lai' — HINT.patch luot 5 ap trong chinh commit ghi so bien nhan nay · ban phang nguyen byte cua `pr896-review-5-codex/VERDICT.md`. Chua merge. | `1a276a15` | 36138 |\n \n ### Tám hàng `don-nhanh-*` — chuỗi ĐẦU TIÊN của bảng này KHÔNG có hàng `approve` nào\n \n"
    }
  ]
}
```
- kết luận: Đang đối chiếu ngữ nghĩa.

### H2-integrity

- giả thuyết: đo lại khẳng định được giao và tìm thể hiện cùng lớp.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity`
- output thật:
```text
{
  "yaml_parsed": 294,
  "receipt_count": 292,
  "verdict_hashes_matched": 292,
  "twins": 16,
  "nested_hash_pairs": 294,
  "frozen_counts": {
    "ALLOWLIST_CUTOVER": 11,
    "NO_DA_DO": 42
  },
  "frozen_matched": 53,
  "modified_old_verdicts": [],
  "errors": []
}
```
- kết luận: KHÔNG PHẢI LỖI nếu errors rỗng; băm và byte kiểm trực tiếp.

### H4-review-states

- giả thuyết: đo lại khẳng định được giao và tìm thể hiện cùng lớp.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/measure_states.py reviews`
- output thật:
```text
ops/reviews/pr870-review-1-codex-verdict.receipt.yaml luot_ghi_chu=Luot duy nhat; P2 duoc va o 06a50c5 bang dung HINT.patch, KHONG co luot review lai tren 06a50c5.
corrected_fields={"assurance_ghi_chu": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}, "HEAD-MERGE-CHUA-REVIEW-LAI": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}}
LATER {"path": "ops/reviews/pr870-review-2-codex-verdict.md", "receipt_reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
LATER {"path": "ops/reviews/pr870-review-3-codex-verdict.md", "receipt_reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "0021b5b2f90e0da39a92c11041c3236980acfbbd0b22f46d0044ac8334f16e81", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
readme_rows=2 anchored_and_later_oid=True
ops/reviews/pr889-review-1-codex-verdict.receipt.yaml luot_ghi_chu=Luot duy nhat; P2 duoc va o 094e8d1 bang HINT.patch + mot cau ngat dong, KHONG co luot review lai tren 094e8d1.
corrected_fields={"assurance_ghi_chu": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}, "HEAD-MERGE-CHUA-REVIEW-LAI": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}}
LATER {"path": "ops/reviews/pr889-review-2-codex-verdict.md", "receipt_reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
LATER {"path": "ops/reviews/pr889-review-3-codex-verdict.md", "receipt_reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "c05bc41d9232d99a9e0c49199e022a9a64b01227674144da73bf50b9b7ce445f", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
readme_rows=2 anchored_and_later_oid=True
prior_eight=2 all_sha_hash_match=True
```
- kết luận: LỖI P1 cùng slug trang-thai-chua-review-da-bi-verdict-sau-bac: luot_ghi_chu của hai receipt vẫn phủ nhận hai lượt review đã có; các trường/hàng mà hint nhắm đã sửa đúng.

### H5-remove_new_readme_row

- giả thuyết: đo lại khẳng định được giao và tìm thể hiện cùng lớp.
- lệnh: `python3 review_evidence/mutations.py; trên clone từ mirror.git ở /tmp/pr896-r6-v5mpiqks/copy, HEAD=22382d8c800bed7b995d093cdcfdc206360d7fd4`
- output thật:
```text
{
  "mutation": "remove_new_readme_row",
  "copy_head": "22382d8c800bed7b995d093cdcfdc206360d7fd4",
  "change": "| `pr896-review-5-codex-verdict.md` | `HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO` | Verdict lich su tren 1a276a1 la changes_requested 2 P1. HINT.patch luot 5 (10 tep) duoc ap NGUYEN (--fuzz=0) trong CHINH commit ghi so bien nhan nay, theo yeu cau chu kho \"va cho toi khi het P1, P2, P3\". Can verdict moi tren exact SHA ung vien; khong doi ket qua hay byte verdict lich su. |",
  "tests": [
    {
      "test": "t26",
      "rc": 0,
      "summary": [
        "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
      ],
      "failure_lines": []
    },
    {
      "test": "t27",
      "rc": 1,
      "summary": [
        "lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0"
      ],
      "failure_lines": [
        "!!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: caveat 'HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO' của pr896-review-5-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-5-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.",
        "  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO' của pr896-review-5-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-5-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó."
      ]
    },
    {
      "test": "t138",
      "rc": 0,
      "summary": [
        "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
      ],
      "failure_lines": []
    }
  ]
}
```
- kết luận: Xóa hàng: chỉ t27 dự kiến đỏ. Xóa caveat: nếu cả ba vẫn xanh, chúng không có răng cho mất caveat này; không coi rc0 là kiểm được tính đầy đủ/ngữ nghĩa.

### H5-remove_new_receipt_caveat

- giả thuyết: đo lại khẳng định được giao và tìm thể hiện cùng lớp.
- lệnh: `python3 review_evidence/mutations.py; trên clone từ mirror.git ở /tmp/pr896-r6-v5mpiqks/copy, HEAD=22382d8c800bed7b995d093cdcfdc206360d7fd4`
- output thật:
```text
{
  "mutation": "remove_new_receipt_caveat",
  "copy_head": "22382d8c800bed7b995d093cdcfdc206360d7fd4",
  "change": "remove verdict_usage_caveats[id=HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO]",
  "tests": [
    {
      "test": "t26",
      "rc": 0,
      "summary": [
        "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
      ],
      "failure_lines": []
    },
    {
      "test": "t27",
      "rc": 0,
      "summary": [
        "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
      ],
      "failure_lines": []
    },
    {
      "test": "t138",
      "rc": 0,
      "summary": [
        "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
      ],
      "failure_lines": []
    }
  ]
}
```
- kết luận: Xóa hàng: chỉ t27 dự kiến đỏ. Xóa caveat: nếu cả ba vẫn xanh, chúng không có răng cho mất caveat này; không coi rc0 là kiểm được tính đầy đủ/ngữ nghĩa.

### H3-ancestry

- giả thuyết: đo lại khẳng định được giao và tìm thể hiện cùng lớp.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/measure_states.py ancestry`
- output thật:
```text
historically_anchored_ancestry_fields=36
receipt_add_anchors_correct=36/36
historical_scalar_quoted=24/36
ancestry_checks_all_rc0=True
round5_seven_fields=7
ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml chuoi_verdict_ghi_chu anchor=e32c5643111e001dc0c655c568b445c897ade450 oid=c2f68987b3f298de12b84cf29a934c7b844c8558 rc=[0, 0, 0, 0]
ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml anchor.gioi_han anchor=86169c00beff045b0faed63e39d1a67b9acd1fc1 oid=bc5d0c6e4d3d5b3cc5d6f8c08ba1c005dd9bdadc rc=[0, 0, 0, 0]
ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml anchor.gioi_han anchor=de0ecd0f912bb131b63ada866672af00129eefd0 oid=80d816130fda69af75dc1d9ae76f3fc83b837773 rc=[0, 0, 0, 0]
ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml anchor.gioi_han anchor=6d59a4394f0e51ace4e02c8f4be13cb649e6871e oid=7d8bb69ac02b54075d63a9915e12e6d2bf28b513 rc=[0, 0, 0, 0]
ops/reviews/wp538-review-1-claude-verdict.receipt.yaml anchor.gioi_han anchor=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 oid=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 rc=[0, 0, 0, 0]
ops/reviews/wp538-review-2-claude-verdict.receipt.yaml anchor.gioi_han anchor=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 oid=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 rc=[0, 0, 0, 0]
ops/reviews/wp540-review-1-claude-verdict.receipt.yaml anchor.gioi_han anchor=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 oid=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 rc=[0, 0, 0, 0]
exceptions=[{"file": "ops/reviews/wp678-spec-review-10-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "42292b4219901137607d3fd9adda26d49f7cfd5e", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-10-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "42292b4219901137607d3fd9adda26d49f7cfd5e", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-11-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "e48423a2719f64a5dfa2f85363874dfadf6c10f8", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-11-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "e48423a2719f64a5dfa2f85363874dfadf6c10f8", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-12-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "d5a57c1ac152c344eef1c3b2cfdee310bba35200", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-12-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "d5a57c1ac152c344eef1c3b2cfdee310bba35200", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-7-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "088511f1fd75faf9bf01f0cf8da037a14fa6d22d", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-7-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "088511f1fd75faf9bf01f0cf8da037a14fa6d22d", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-8-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "f958e147754bed8e9e7034dd28450681f19c3db0", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-8-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "f958e147754bed8e9e7034dd28450681f19c3db0", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-9-claude-verdict.receipt.yaml", "field": "spec_ghi_chu", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "2469f3ebed51dc228319cf375d7912bf7dbc0947", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}, {"file": "ops/reviews/wp678-spec-review-9-claude-verdict.receipt.yaml", "field": "verdict_usage_caveats.0.mo_ta", "historical_anchor": "62319d945fff81de6396aab6806a4ab349682aba", "is_receipt_add_commit": true, "old_scalar_quoted": false, "measured_oid": "2469f3ebed51dc228319cf375d7912bf7dbc0947", "ancestry_rc": {"101263f": 0, "2e4183b": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0, "3e973a03b151e37cd402e0a723816eeaa8247193": 0, "22382d8c800bed7b995d093cdcfdc206360d7fd4": 0}}]
```
- kết luận: ĐÃ ĐÓNG bảy thể hiện ancestry lượt 5 nếu mọi mốc và rc khớp; không suy landed/assurance từ quan hệ Git.

### H4-review-states

- giả thuyết: đo lại khẳng định được giao và tìm thể hiện cùng lớp.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/measure_states.py reviews`
- output thật:
```text
ops/reviews/pr870-review-1-codex-verdict.receipt.yaml luot_ghi_chu=Luot duy nhat; P2 duoc va o 06a50c5 bang dung HINT.patch, KHONG co luot review lai tren 06a50c5.
corrected_fields={"assurance_ghi_chu": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}, "HEAD-MERGE-CHUA-REVIEW-LAI": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}}
LATER {"path": "ops/reviews/pr870-review-2-codex-verdict.md", "receipt_reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
LATER {"path": "ops/reviews/pr870-review-3-codex-verdict.md", "receipt_reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "0021b5b2f90e0da39a92c11041c3236980acfbbd0b22f46d0044ac8334f16e81", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
readme_rows=2 anchored_and_later_oid=True
ops/reviews/pr889-review-1-codex-verdict.receipt.yaml luot_ghi_chu=Luot duy nhat; P2 duoc va o 094e8d1 bang HINT.patch + mot cau ngat dong, KHONG co luot review lai tren 094e8d1.
corrected_fields={"assurance_ghi_chu": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}, "HEAD-MERGE-CHUA-REVIEW-LAI": {"historical_anchor_matches": true, "old_scalar_quoted": true, "later_oid_present": true}}
LATER {"path": "ops/reviews/pr889-review-2-codex-verdict.md", "receipt_reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
LATER {"path": "ops/reviews/pr889-review-3-codex-verdict.md", "receipt_reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "sha_matches": true, "verdict_header_matches": true, "verdict": "approve", "counts": [0, 0, 0, 0], "sha256": "c05bc41d9232d99a9e0c49199e022a9a64b01227674144da73bf50b9b7ce445f", "hash_matches": true, "exists_at_historical_anchor_rc": 128}
readme_rows=2 anchored_and_later_oid=True
prior_eight=8 all_sha_hash_match=True
```
- kết luận: LỖI P1 cùng slug trang-thai-chua-review-da-bi-verdict-sau-bac: luot_ghi_chu của hai receipt vẫn phủ nhận hai lượt review đã có; các trường/hàng mà hint nhắm đã sửa đúng.
