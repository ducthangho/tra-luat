verdict: dang_lam
reviewed_sha: 1a276a15192013fdb1e472db409133b53ac57944
Kết quả: đang đo.

## NHẬT KÝ ĐO TĂNG DẦN
- Bắt đầu: đọc `runs/453628b5/prompt.snapshot`; phạm vi chỉ đọc kho `cay-kho/`, mọi đột biến thực hiện trên bản sao ngoài kho; không gọi mạng.

### HƯỚNG 1: Định danh cây và phạm vi
- giả thuyết: kho giao sai OID hoặc thiếu lịch sử.
- lệnh: `git -C cay-kho rev-parse HEAD`; `git -C cay-kho status --short`; đọc `PROMPT.md`, `cay-kho/AGENTS.md` và quy tắc review liên quan.
- output: HEAD `1a276a15192013fdb1e472db409133b53ac57944`; status rỗng. Chỉ thị cho phép đo chỉ đọc và dùng clone để đột biến; output giữ ở ngoài `cay-kho/`.
- kết luận: KHÔNG PHẢI LỖI về OID checkout; các đối chiếu sau đều neo vào OID này.

- Phép đo tại `cay-kho/`: `python3 ops/lease_publish_test.py --chi-ca=t138_` ⇒ rc=0; >>> vao t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 2026-10-26T13:40:23Z / <<< ra t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 0.301s QUA /  / lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0. Log: `review_evidence/t138.stdout` và `.stderr`.

- Phép đo tại `cay-kho/`: `python3 ops/land_evidence_nguon.py --root .` ⇒ rc=0; ĐẠT ops/land/pr932-wp748-r26-land-evidence.yaml / ĐẠT ops/land/pr933-wp929-land-evidence.yaml / land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73 / TỔNG: ĐẠT. Log: `review_evidence/land_evidence_nguon.stdout` và `.stderr`.

- Phép đo tại `cay-kho/`: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ rc=0; doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine. Log: `review_evidence/doctrine.stdout` và `.stderr`.

- Phép đo tại `cay-kho/`: `python3 ops/lease_publish_test.py --chi-ca=t26_` ⇒ rc=0; >>> vao t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 2026-10-26T13:40:23Z / <<< ra t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 2.724s QUA /  / lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0. Log: `review_evidence/t26.stdout` và `.stderr`.

- Phép đo tại `cay-kho/`: `python3 ops/lease_publish_test.py --chi-ca=t27_` ⇒ rc=0; >>> vao t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 2026-10-26T13:40:23Z / <<< ra t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 5.594s QUA /  / lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0. Log: `review_evidence/t27.stdout` và `.stderr`.

- Phép đo tại `cay-kho/`: `python3 scripts/tl.py doc-claims-check --json` ⇒ rc=0; JSON ok=True. Log: `review_evidence/doc_claims.stdout` và `.stderr`.

- Phép đo tại `cay-kho/`: `python3 ops/bien_nhan_v2.py --root .` ⇒ rc=0;  / bien_nhan_v2: 238 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 291 / TỔNG: ĐẠT. Log: `review_evidence/bien_nhan_v2.stdout` và `.stderr`.

### HƯỚNG 2 - doi chieu hint
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history`
- output thật:
```text
diff.patch: byte_match=True
diff-pr947.patch: byte_match=True
numstat.txt: byte_match=True
numstat-pr947.txt: byte_match=True
hint_paths=34 apply_to_parent_rc=1
Hunk #1 FAILED at 294.
1 out of 1 hunk FAILED -- saving rejects to file ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml.rej
Hunk #6 FAILED at 750.
Hunk #7 FAILED at 1039.
2 out of 7 hunks FAILED -- saving rejects to file ops/reviews/README.md.rej
exact_hint_blob_matches=32
EXACT ops/reviews/assurance-ho-model-review-1-claude-verdict.receipt.yaml
EXACT ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml
EXACT ops/reviews/doctrine-scan-review-1-claude-verdict.receipt.yaml
EXACT ops/reviews/doctrine-scan-review-2-claude-verdict.receipt.yaml
EXACT ops/reviews/doctrine-scan-review-3-claude-verdict.receipt.yaml
EXACT ops/reviews/pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml
EXACT ops/reviews/pr455-bien-nhan-v2-review-2-codex-verdict.receipt.yaml
EXACT ops/reviews/pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml
EXACT ops/reviews/pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml
EXACT ops/reviews/pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml
EXACT ops/reviews/pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml
EXACT ops/reviews/pr508-review-1-codex-verdict.receipt.yaml
EXACT ops/reviews/pr508-review-2-codex-verdict.receipt.yaml
EXACT ops/reviews/pr508-review-3-codex-verdict.receipt.yaml
EXACT ops/reviews/pr508-review-4-codex-verdict.receipt.yaml
EXACT ops/reviews/pr508-review-5-codex-verdict.receipt.yaml
EXACT ops/reviews/pr526-review-3-codex-verdict.receipt.yaml
EXACT ops/reviews/pr896-review-1-codex-verdict.receipt.yaml
EXACT ops/reviews/pr896-review-4-legacy-caveats.yaml
EXACT ops/reviews/pr915-review-1-codex-verdict.receipt.yaml
EXACT ops/reviews/r330-rig-quyet-mau-audit-nguoi-verdict.receipt.yaml
EXACT ops/reviews/wp538-review-1-claude-verdict.receipt.yaml
EXACT ops/reviews/wp538-review-2-claude-verdict.receipt.yaml
EXACT ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
EXACT ops/reviews/wp541-review-1-claude-verdict.receipt.yaml
EXACT ops/reviews/wp541-review-2-claude-verdict.receipt.yaml
EXACT ops/reviews/wp678-spec-review-10-claude-verdict.receipt.yaml
EXACT ops/reviews/wp678-spec-review-11-claude-verdict.receipt.yaml
EXACT ops/reviews/wp678-spec-review-12-claude-verdict.receipt.yaml
EXACT ops/reviews/wp678-spec-review-7-claude-verdict.receipt.yaml
EXACT ops/reviews/wp678-spec-review-8-claude-verdict.receipt.yaml
EXACT ops/reviews/wp678-spec-review-9-claude-verdict.receipt.yaml
MANUAL ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml: missing_hint_lines=0 extra_delta_lines=4
EXTRA +  ghi_chu_luot4: >-
EXTRA +    Khoi cap_nhat_20261026_luot4 o tren (ghi tai ff4ab57) noi HINT.patch luot 4 "CHUA ap"; cau ay dung tai ff4ab57 va 77a0a45.
EXTRA +    HINT.patch luot 4 duoc ap o commit ke tiep sau 77a0a45 tren nhanh claude/pr896-review-2-codex (xem git log), theo lua chon
EXTRA +    cua chu kho "Ap nguyen HINT luot 4".
MANUAL ops/reviews/README.md: missing_hint_lines=0 extra_delta_lines=4
EXTRA -| `pr896-review-4-codex-verdict.md` | `HINT-LUOT4-CHUA-AP` | Tai moc ghi so (commit sau a5f1c5e) changes_requested 3 P1 + 1 P2; HINT.patch luot 4 (34 tep, phan lon receipt NGOAI chuoi #896) CHUA ap, cho chu kho quyet pham vi. |
EXTRA +| `pr896-review-4-codex-verdict.md` | `HINT-LUOT4-DA-AP-CAN-VERDICT-MOI` | Verdict lich su tren 2e4183b la changes_requested 3 P1 + 1 P2. Tai moc ghi so ff4ab57 (va 77a0a45) HINT.patch luot 4 (34 tep, phan lon receipt NGOAI chuoi #896) CHUA ap; chu kho chon ap nguyen, va no duoc ap o commit ke tiep sau 77a0a45. Can verdict moi tren exact SHA ung vien; khong doi ket qua hay byte verdict lich su. |
EXTRA -| [`pr896-review-4-codex-verdict.md`](pr896-review-4-codex-verdict.md) | [`.receipt.yaml`](pr896-review-4-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/3/1/0 tren `2e4183b` (head PR #947, mang HINT luot 3) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 9b8d9a76`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · ba finding luot 3 DA DONG (P2 dong 13/13 the hien cu); moi: P1 hang muc luc luot 3 con khai HINT chua ap, P1 8 receipt con noi 'chua review', P1 23 receipt phu nhan ancestry da co, P2 pr526-review-3/slice-b-c-review-2 — phan lon NGOAI chuoi #896; tai moc ghi so HINT.patch luot 4 chua ap · ban phang nguyen byte cua `pr896-review-4-codex/VERDICT.md`. Chua merge. | `2e4183bc` | 39386 |
EXTRA +| [`pr896-review-4-codex-verdict.md`](pr896-review-4-codex-verdict.md) | [`.receipt.yaml`](pr896-review-4-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/3/1/0 tren `2e4183b` (head PR #947, mang HINT luot 3) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 9b8d9a76`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · ba finding luot 3 DA DONG (P2 dong 13/13 the hien cu); moi: P1 hang muc luc luot 3 con khai HINT chua ap, P1 8 receipt con noi 'chua review', P1 23 receipt phu nhan ancestry da co, P2 pr526-review-3/slice-b-c-review-2 — phan lon NGOAI chuoi #896; HINT.patch luot 4 chua ap tai ff4ab57, da ap o commit ke tiep sau 77a0a45 · ban phang nguyen byte cua `pr896-review-4-codex/VERDICT.md`. Chua merge. | `2e4183bc` | 39386 |
outside_hint=["ops/reviews/pr896-review-4-codex-verdict.receipt.yaml"]
commit_after_77a0a45=1a276a15192013fdb1e472db409133b53ac57944
```
- kết luận: Đối chiếu +/- và blob được ghi đầy đủ; đánh giá ngữ nghĩa riêng ở các hướng tiếp theo.

### HƯỚNG 3 - toan ven
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity`
- output thật:
```text
{
  "yaml_parsed": 293,
  "receipts": 291,
  "verdict_hashes_match": 291,
  "flat_directory_pairs": 15,
  "allowlist_counts": {
    "ALLOWLIST_CUTOVER": 11,
    "NO_DA_DO": 42
  },
  "allowlist_matches": 53,
  "parent_changed_verdicts": [],
  "master_modified_old_verdicts": [],
  "supplementary": [
    {
      "path": "ops/reviews/don-nhanh-base-review-1-codex-verdict.receipt.yaml",
      "hash_matches": true,
      "readme_rows": 1,
      "description_matches": true,
      "receipt_same_as_parent": true
    },
    {
      "path": "ops/reviews/slice-b-c-review-2-codex-verdict.receipt.yaml",
      "hash_matches": true,
      "readme_rows": 1,
      "description_matches": true,
      "receipt_same_as_parent": true
    }
  ],
  "errors": []
}
```
- kết luận: KHÔNG PHẢI LỖI nếu errors rỗng; nguồn và byte cũ được đối chiếu độc lập với cổng.

### HƯỚNG 4: Ba ca và bốn bộ kiểm tại cây gốc
- giả thuyết: cổng hỏng hoặc rc xanh thiếu bằng chứng dương.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/run_checks.py` chạy từng lệnh bắt buộc, cwd `cay-kho/`.
- output: t26 rc0 `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`; t27 rc0 cùng dòng kết luận; t138 rc0 cùng dòng kết luận. `bien_nhan_v2` rc0: `238 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 291`, `TỔNG: ĐẠT`. `land_evidence_nguon` rc0: `47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73`, `TỔNG: ĐẠT`. `doctrine-scan` rc0: `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. `doc-claims-check --json` rc0, JSON `"ok": true`, `"strict": false`.
- kết luận: KHÔNG PHẢI LỖI của các cổng; chưa kết luận chúng kiểm đúng ngữ nghĩa mọi câu trạng thái. Có SyntaxWarning `invalid escape sequence '\d'` từ tệp test, không ảnh hưởng kết quả. Log đầy đủ và rc ở `review_evidence/checks.json` và các tệp stdout/stderr/rc tương ứng.

- Đột biến clone `remove-new-pr526-readme-row` ⇒ t26_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0; t27_ rc1 lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0; t138_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0.

- Đột biến clone `remove-new-pr526-receipt-caveat` ⇒ t26_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0; t27_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0; t138_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0.

- Đột biến clone `remove-new-slice-legacy-readme-row` ⇒ t26_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0; t27_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0; t138_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0.

- Đột biến clone `remove-new-slice-supplementary-caveat` ⇒ t26_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0; t27_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0; t138_ rc0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0.

### HƯỚNG 5: Đột biến hàng README và caveat mới
- giả thuyết: t26/t27/t138 xanh đồng nghĩa bảo vệ đủ caveat mới.
- lệnh: clone cục bộ `mirror.git` vào `/tmp/pr896-r5-measure-453628b5/copy`, checkout detached `1a276a15192013fdb1e472db409133b53ac57944`; `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/mutations.py` chỉ đột biến tài liệu/receipt trên clone rồi chạy riêng ba ca.
- output thật: mất hàng README PR526 mới, 480 byte ⇒ t26 rc0 `1/1`, t27 rc1 `0/1`, t138 rc0 `1/1`; t27 báo caveat `SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC` không có ở cùng hàng verdict đúng cột. Khôi phục rồi bỏ riêng caveat PR526 (YAML vẫn parse, danh sách rỗng) ⇒ cả ba rc0 `1/1`. Mất riêng hàng README slice-b-c mới, 473 byte ⇒ cả ba rc0 `1/1`. Khôi phục rồi mất riêng caveat slice-b-c ở supplementary YAML, 627 byte ⇒ cả ba rc0 `1/1`. Mọi lượt đều đã chạy=1, bỏ qua=0. Sau hoàn nguyên, status clone rỗng. Chi tiết: `review_evidence/mutations.json` và các log từng biến thể.
- kết luận: KHÔNG PHẢI LỖI hiện hành của bản vá; đây là giới hạn đã đo. Chỉ t27 có răng với hàng README PR526; t26/t138 không có răng với hàng đó; cả ba không có răng với mất caveat PR526, hàng README supplementary slice-b-c, hoặc caveat supplementary slice-b-c. Không coi các ca xanh là bằng chứng đủ nội dung hay đúng ngữ nghĩa.

### HƯỚNG 6 - ancestry va truong con sot
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py ancestry`
- output thật:
```text
old_23_receipts=23 checks=92 all_rc0=True
historical_receipt_anchors_exist=22/22
residual_unanchored_fields=7
ci-windows-review-5-claude-verdict.receipt.yaml:70 chuoi_verdict_ghi_chu oid=c2f68987b3f298de12b84cf29a934c7b844c8558 rc(master,candidate)=[0, 0]
TEXT Nam verdict deu CHUA land — chung song tren nam nhanh claude/review-548-luot*-20260917 va KHONG phai to tien cua master (do: `merge-base --is-ancestor c2f6898 origin/master` => KHONG). `approve` cua luot 2 DA BI RUT va KHONG song lai; `approve` co hieu luc la cua luot 5.
doctrine-scan-review-1-claude-verdict.receipt.yaml:138 anchor.gioi_han oid=bc5d0c6e4d3d5b3cc5d6f8c08ba1c005dd9bdadc rc(master,candidate)=[0, 0]
TEXT cuong_do thap vi mo neo hien chi la mot nhanh, khong phai tag luu-tru/*. Manh len cao khi #543 land bang merge commit hoac fast-forward; squash pha quan he to tien.
doctrine-scan-review-2-claude-verdict.receipt.yaml:138 anchor.gioi_han oid=80d816130fda69af75dc1d9ae76f3fc83b837773 rc(master,candidate)=[0, 0]
TEXT cuong_do thap vi mo neo hien chi la mot nhanh, khong phai tag luu-tru/*. Manh len cao khi #543 land bang merge commit hoac fast-forward; squash pha quan he to tien.
doctrine-scan-review-3-claude-verdict.receipt.yaml:120 anchor.gioi_han oid=7d8bb69ac02b54075d63a9915e12e6d2bf28b513 rc(master,candidate)=[0, 0]
TEXT cuong_do thap vi mo neo hien chi la mot nhanh, khong phai tag luu-tru/*. Manh len cao khi #543 land bang merge commit hoac fast-forward; squash pha quan he to tien.
wp538-review-1-claude-verdict.receipt.yaml:155 anchor.gioi_han oid=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 rc(master,candidate)=[0, 0]
TEXT `cuong_do: thap` vi mo neo hien CHI la mot nhanh, khong phai tag `luu-tru/*` va khong phai to tien cua `master`. Nhanh xoa duoc va SHA se thanh khong tra duoc. Manh len `cao` khi WP538 land bang merge commit hoac fast-forward; squash pha quan he to tien.
wp538-review-2-claude-verdict.receipt.yaml:158 anchor.gioi_han oid=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 rc(master,candidate)=[0, 0]
TEXT cuong_do thap vi mo neo hien chi la mot nhanh, khong phai tag luu-tru/*. Manh len cao khi WP538 land bang merge commit hoac fast-forward; squash pha quan he to tien.
wp540-review-1-claude-verdict.receipt.yaml:165 anchor.gioi_han oid=ab27f786a45de5df7aae23f7df7b4c4fb8eecb92 rc(master,candidate)=[0, 0]
TEXT cuong_do thap vi mo neo hien chi la mot nhanh, khong phai tag luu-tru/* va khong phai to tien cua master. Manh len cao khi WP540 land bang merge commit hoac fast-forward; squash pha quan he to tien.
ci_windows_five_verdict_blob_oids={"2d8b4fb9e1e122f40011e4fffe87fa6908c5f7fc": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 1}, "7e2ef2e11b204f397a463d6ab824e3f12dfad709": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 1}, "4bc35d3d6dc8a75464255048d50603ceba271667": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 1}, "a45c8dc1c62ea493eb97c64d640727fd08230c13": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 1}, "c2f68987b3f298de12b84cf29a934c7b844c8558": {"3e973a03b151e37cd402e0a723816eeaa8247193": 0, "1a276a15192013fdb1e472db409133b53ac57944": 0}}
excluded_or_historical={"4bc9432": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 1}, "604b8d9": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 1}, "2e4183b": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 0}, "82359c4": {"3e973a03b151e37cd402e0a723816eeaa8247193": 1, "1a276a15192013fdb1e472db409133b53ac57944": 0}}
```
- kết luận: LỖI P1 phu-nhan-ancestry-chi-tren-nhanh-da-cu còn 7 receipt: bản vá neo đúng trường đã chọn nhưng bỏ trường khác. Không suy landed/assurance từ ancestry. 4bc9432 và 604b8d9 không phải ancestor master; hai head PR947 cũng chưa là ancestor master, không báo những câu tương ứng là sai.

### HƯỚNG 7 - trang thai da review
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews`
- output thật:
```text
old_review_caveats_historically_anchored=2 all_next_sha_and_hash_match=True
OLD pr896-review-1-codex-verdict.receipt.yaml anchor=2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f next=pr896-review-2-codex-verdict.md reviewed=8d56009a09af7b3ef93801df105f9483de212cc7 next_verdict_exists_at_anchor_rc=128
OLD pr915-review-1-codex-verdict.receipt.yaml anchor=a9bc9349103adfc971f4a1f7431a9655aecaaefb next=pr896-review-2-codex-verdict.md reviewed=8d56009a09af7b3ef93801df105f9483de212cc7 next_verdict_exists_at_anchor_rc=128
RESIDUAL pr870-review-1-codex-verdict.receipt.yaml
assurance_ghi_chu:27 Khac ho (codex CLI, executor Claude) nhung verdict la `changes_requested`, va KHONG khai cross_approved: (1) head da merge 06a50c5 KHONG duoc review lai (caveat HEAD-MERGE-CHUA-REVIEW-LAI); (2) model thuc chay chi co loi khai header CLI, khong modelUsage; (3) goi codex tran, khong run.json; (4) checkout review khong bi cuong che read-only.
verdict_usage_caveats.0.mo_ta:97 Verdict cham b38fce8; head da merge la 06a50c5 (them commit va P2 bang dung HINT.patch, 3 dong CLAUDE.md). Khong co luot review nao tren 06a50c5 — "da va" la loi khai cua executor, kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check, khong phai verdict cua reviewer.
README:704 | `pr870-review-1-codex-verdict.md` | `HEAD-MERGE-CHUA-REVIEW-LAI` | Verdict cham `b38fce8`; head da merge la `06a50c5` (va P2 bang dung HINT.patch, 3 dong CLAUDE.md) va KHONG duoc review lai. "Da va" la loi khai executor (kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check), khong phai verdict. |
README:1046 | [`pr870-review-1-codex-verdict.md`](pr870-review-1-codex-verdict.md) | [`.receipt.yaml`](pr870-review-1-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | **`changes_requested`** · `cross_reviewed` (codex CLI khac ho executor, `codex exec` tran, khong run.json; header CLI khai `gpt-6.1-sol`/`xhigh`, model thuc chay KHONG DO DUOC) · 0/0/1/0 · P2 `master-windows-bo-sot-dispatch` da va o `06a50c5` bang dung HINT.patch, KHONG review lai · ban phang nguyen byte cua `pr870-review-1-codex/VERDICT.md`. Merge `5f288ea`. | `b38fce83` | 104880 |
LATER {"path": "ops/reviews/pr870-review-2-codex-verdict.md", "reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "matches_oid": true, "verdict": "approve", "hash_matches": true}
LATER {"path": "ops/reviews/pr870-review-3-codex-verdict.md", "reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "matches_oid": true, "verdict": "approve", "hash_matches": true}
RESIDUAL pr889-review-1-codex-verdict.receipt.yaml
assurance_ghi_chu:28 Khac ho (codex CLI, executor Claude), co run.json cua launcher, nhung verdict la `changes_requested` va KHONG khai cross_approved: (1) head da merge 094e8d1 KHONG duoc review lai (caveat HEAD-MERGE-CHUA-REVIEW-LAI); (2) model thuc chay chi co loi khai header CLI, khong modelUsage; (3) checkout review khong bi cuong che read-only.
verdict_usage_caveats.1.mo_ta:104 Verdict cham 8d5cccb; head da merge la 094e8d1 (va P2 bang HINT.patch + sua them mot cau, CLAUDE.md +8/-5 theo `git diff --numstat 8d5cccb 094e8d1`) va KHONG duoc review lai. "Da va" la loi khai executor (kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check + doc ma ops/cong_cu_test.py:8916), khong phai verdict cua reviewer.
README:710 | `pr889-review-1-codex-verdict.md` | `HEAD-MERGE-CHUA-REVIEW-LAI` | Verdict cham `8d5cccb`; head da merge la `094e8d1` (va P2 bang HINT.patch + sua them mot cau) va KHONG duoc review lai. "Da va" la loi khai executor (`patch --fuzz=0` + doctrine-scan/doc-claims-check + doc ma `ops/cong_cu_test.py:8916`), khong phai verdict. |
README:1047 | [`pr889-review-1-codex-verdict.md`](pr889-review-1-codex-verdict.md) | [`.receipt.yaml`](pr889-review-1-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | **`changes_requested`** · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 9f946d71`, run.json trong kho; header CLI khai `gpt-6.1-sol`/`xhigh`, model thuc chay KHONG DO DUOC) · 0/0/1/0 · P2 `windows-green-does-not-prove-all-baselines` da va o `094e8d1`, KHONG review lai · ban phang nguyen byte cua `pr889-review-1-codex/VERDICT.md`. Merge `6ac385f`. | `8d5cccbb` | 75193 |
LATER {"path": "ops/reviews/pr889-review-2-codex-verdict.md", "reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "matches_oid": true, "verdict": "approve", "hash_matches": true}
LATER {"path": "ops/reviews/pr889-review-3-codex-verdict.md", "reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "matches_oid": true, "verdict": "approve", "hash_matches": true}
```
- kết luận: LỖI P1 trang-thai-chua-review-da-bi-verdict-sau-bac: 8/8 thể hiện cũ được neo lịch sử đúng, nhưng còn PR870/PR889 lượt 1 ở assurance, caveat và README. Cả lượt 2 và lượt 3 đã review đúng head bản vá. Giữ nguyên verdict lịch sử và assurance; đây không phải quyền land.

### HƯỚNG 7 - trang thai da review
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews`
- output thật:
```text
old_review_caveats_historically_anchored=8 all_next_sha_and_hash_match=False
OLD pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml anchor=c595292cb63fb8c09d7d7b482cda20f9d5f0917f next=pr455-bien-nhan-v2-review-2-codex-verdict.md reviewed=c595292cb63fb8c09d7d7b482cda20f9d5f0917f next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-2-codex-verdict.receipt.yaml anchor=1cd8ec78e42e32e6ff5af8edcc4660b1e601fd93 next=pr455-bien-nhan-v2-review-3-codex-verdict.md reviewed=cb212847375c2319fe0ccad3f7c00c90b870e3ba next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml anchor=dc92839520092a95f097464f4b9a2a252f0d9132 next=pr455-bien-nhan-v2-review-4-codex-verdict.md reviewed=4ef73e69d5f3c419634118983723355e25e38305 next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml anchor=3cff891b81f02dc22cc7ed8b05799c94ade0fc63 next=pr455-bien-nhan-v2-review-5-codex-verdict.md reviewed=670071b700bd97a893d64393ffded0257957d0b3 next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml anchor=020198a437b7ae0008f466959950d3994adba716 next=pr455-bien-nhan-v2-review-6-codex-verdict.md reviewed=5a78c150106ae381461354c77ba2023834330bbd next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml anchor=e4d8ecce7e583503b5205a038707ea667a81ed43 next=pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md reviewed=ca960160b477cd16346a293aaa8752772a9921d4 next_verdict_exists_at_anchor_rc=128
OLD pr896-review-1-codex-verdict.receipt.yaml anchor=2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f next=pr896-review-2-codex-verdict.md reviewed=8d56009a09af7b3ef93801df105f9483de212cc7 next_verdict_exists_at_anchor_rc=128
OLD pr915-review-1-codex-verdict.receipt.yaml anchor=a9bc9349103adfc971f4a1f7431a9655aecaaefb next=pr896-review-2-codex-verdict.md reviewed=8d56009a09af7b3ef93801df105f9483de212cc7 next_verdict_exists_at_anchor_rc=128
RESIDUAL pr870-review-1-codex-verdict.receipt.yaml
assurance_ghi_chu:27 Khac ho (codex CLI, executor Claude) nhung verdict la `changes_requested`, va KHONG khai cross_approved: (1) head da merge 06a50c5 KHONG duoc review lai (caveat HEAD-MERGE-CHUA-REVIEW-LAI); (2) model thuc chay chi co loi khai header CLI, khong modelUsage; (3) goi codex tran, khong run.json; (4) checkout review khong bi cuong che read-only.
verdict_usage_caveats.0.mo_ta:97 Verdict cham b38fce8; head da merge la 06a50c5 (them commit va P2 bang dung HINT.patch, 3 dong CLAUDE.md). Khong co luot review nao tren 06a50c5 — "da va" la loi khai cua executor, kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check, khong phai verdict cua reviewer.
README:704 | `pr870-review-1-codex-verdict.md` | `HEAD-MERGE-CHUA-REVIEW-LAI` | Verdict cham `b38fce8`; head da merge la `06a50c5` (va P2 bang dung HINT.patch, 3 dong CLAUDE.md) va KHONG duoc review lai. "Da va" la loi khai executor (kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check), khong phai verdict. |
README:1046 | [`pr870-review-1-codex-verdict.md`](pr870-review-1-codex-verdict.md) | [`.receipt.yaml`](pr870-review-1-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | **`changes_requested`** · `cross_reviewed` (codex CLI khac ho executor, `codex exec` tran, khong run.json; header CLI khai `gpt-6.1-sol`/`xhigh`, model thuc chay KHONG DO DUOC) · 0/0/1/0 · P2 `master-windows-bo-sot-dispatch` da va o `06a50c5` bang dung HINT.patch, KHONG review lai · ban phang nguyen byte cua `pr870-review-1-codex/VERDICT.md`. Merge `5f288ea`. | `b38fce83` | 104880 |
LATER {"path": "ops/reviews/pr870-review-2-codex-verdict.md", "reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "matches_oid": true, "verdict": "approve", "hash_matches": true}
LATER {"path": "ops/reviews/pr870-review-3-codex-verdict.md", "reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "matches_oid": true, "verdict": "approve", "hash_matches": true}
RESIDUAL pr889-review-1-codex-verdict.receipt.yaml
assurance_ghi_chu:28 Khac ho (codex CLI, executor Claude), co run.json cua launcher, nhung verdict la `changes_requested` va KHONG khai cross_approved: (1) head da merge 094e8d1 KHONG duoc review lai (caveat HEAD-MERGE-CHUA-REVIEW-LAI); (2) model thuc chay chi co loi khai header CLI, khong modelUsage; (3) checkout review khong bi cuong che read-only.
verdict_usage_caveats.1.mo_ta:104 Verdict cham 8d5cccb; head da merge la 094e8d1 (va P2 bang HINT.patch + sua them mot cau, CLAUDE.md +8/-5 theo `git diff --numstat 8d5cccb 094e8d1`) va KHONG duoc review lai. "Da va" la loi khai executor (kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check + doc ma ops/cong_cu_test.py:8916), khong phai verdict cua reviewer.
README:710 | `pr889-review-1-codex-verdict.md` | `HEAD-MERGE-CHUA-REVIEW-LAI` | Verdict cham `8d5cccb`; head da merge la `094e8d1` (va P2 bang HINT.patch + sua them mot cau) va KHONG duoc review lai. "Da va" la loi khai executor (`patch --fuzz=0` + doctrine-scan/doc-claims-check + doc ma `ops/cong_cu_test.py:8916`), khong phai verdict. |
README:1047 | [`pr889-review-1-codex-verdict.md`](pr889-review-1-codex-verdict.md) | [`.receipt.yaml`](pr889-review-1-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | **`changes_requested`** · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 9f946d71`, run.json trong kho; header CLI khai `gpt-6.1-sol`/`xhigh`, model thuc chay KHONG DO DUOC) · 0/0/1/0 · P2 `windows-green-does-not-prove-all-baselines` da va o `094e8d1`, KHONG review lai · ban phang nguyen byte cua `pr889-review-1-codex/VERDICT.md`. Merge `6ac385f`. | `8d5cccbb` | 75193 |
LATER {"path": "ops/reviews/pr889-review-2-codex-verdict.md", "reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "matches_oid": true, "verdict": "approve", "hash_matches": true}
LATER {"path": "ops/reviews/pr889-review-3-codex-verdict.md", "reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "matches_oid": true, "verdict": "approve", "hash_matches": true}
```
- kết luận: LỖI P1 trang-thai-chua-review-da-bi-verdict-sau-bac: 8/8 thể hiện cũ được neo lịch sử đúng, nhưng còn PR870/PR889 lượt 1 ở assurance, caveat và README. Cả lượt 2 và lượt 3 đã review đúng head bản vá. Giữ nguyên verdict lịch sử và assurance; đây không phải quyền land.

### HƯỚNG 8 - tu khai execution surface
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/surfaces.py; rg -n -i "codex.service|service/api|execution.surface|bề mặt|surface:" cay-kho/ops/reviews --glob "*-verdict.md" --glob "VERDICT.md"`
- output thật:
```text
verdict_files=308 distinct_content=292
run_json_files=47 parse_errors=[]
receipt_runtime_pairs=16 surface_mismatches=[]
service_self_claims=25 missing_caveat=[]
ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.md:130 receipt_surface=codex_cli has_caveat=True runtime_files=[]
ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.md:194 receipt_surface=codex_cli has_caveat=True runtime_files=[]
ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.md:125 receipt_surface=codex_cli has_caveat=True runtime_files=[]
ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.md:14 receipt_surface=codex_cli has_caveat=True runtime_files=[]
phan-bien-quy-trinh-review-3-codex-verdict.md:15 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 15, "line_matches_service_claim": true, "run_ids": ["4f5341d473c8442380dc2182f9cde013"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
phan-bien-quy-trinh-review-4-codex-verdict.md:13 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 13, "line_matches_service_claim": true, "run_ids": ["06ceaec97a1e454a970cda425836dcf1"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
phan-bien-quy-trinh-review-5-codex-verdict.md:12 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 12, "line_matches_service_claim": true, "run_ids": ["12574e98d66c4875b2333fa1adc0bf4c"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-1-codex-verdict.md:7 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 7, "line_matches_service_claim": true, "run_ids": ["ea42cb4174e54db8a581f4a66f43bd2f"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-2-codex-verdict.md:9 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 9, "line_matches_service_claim": true, "run_ids": ["0bc966b1409f4ca39f0f3707bdcb20d8"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-3-codex-verdict.md:9 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 9, "line_matches_service_claim": true, "run_ids": ["32fca3390491423c83e84d37f9904a3b"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-4-codex-verdict.md:9 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 9, "line_matches_service_claim": true, "run_ids": ["d0266c01c4a24dd8a55d02b4ffbdd6b2"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-5-codex-verdict.md:9 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 9, "line_matches_service_claim": true, "run_ids": ["d86357ad0e4b4a6b96a7f5b2e3c1d9f4"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-6-codex-verdict.md:9 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 9, "line_matches_service_claim": true, "run_ids": ["c7af46a4a1e34b0d9d3c86f5b0a2e7d1"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md:9 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 9, "line_matches_service_claim": true, "run_ids": ["035d3cac9f2e4b7188d6a0c53e1b74af"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr455-bien-nhan-v2-review-8-gpt6astra-verdict.md:8 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 8, "line_matches_service_claim": true, "run_ids": ["b7384eee92a045a1b145718ac5310081"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr460-bien-nhan-v2-review-9-gpt6astra-verdict.md:5 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 5, "line_matches_service_claim": true, "run_ids": ["3bfdc70ca03647139a3da914246acd20"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr493-review-5-codex-verdict.md:8 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 8, "line_matches_service_claim": true, "run_ids": ["5f5c24ba", "5f5c24ba292a47d09c3a5d6b66f3b772"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr526-review-3-codex-verdict.md:151 receipt_surface=codex_cli has_caveat=True condition={"declared_line": 151, "line_matches_service_claim": true, "run_ids": ["f466d135", "f466d135534244c1b888c9c0c44811b9"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
pr870-review-2-codex-verdict.md:9 receipt_surface=codex_cli has_caveat=True runtime_files=['ops/reviews/pr870-review-2-codex/run/run.json']
pr870-review-3-codex-verdict.md:444 receipt_surface=codex_cli has_caveat=True runtime_files=['ops/reviews/pr870-review-3-codex/run/run.json']
pr889-review-1-codex-verdict.md:7 receipt_surface=codex_cli has_caveat=True runtime_files=['ops/reviews/pr889-review-1-codex/run/run.json']
pr889-review-2-codex-verdict.md:9 receipt_surface=codex_cli has_caveat=True runtime_files=['ops/reviews/pr889-review-2-codex/run/run.json']
pr889-review-3-codex-verdict.md:309 receipt_surface=codex_cli has_caveat=True runtime_files=['ops/reviews/pr889-review-3-codex/run/run.json']
slice-b-c-review-2-codex-verdict.md:19 receipt_surface=None has_caveat=True condition={"declared_line": 19, "line_matches_service_claim": true, "run_ids": ["8ddb0c6f"], "run_ids_mentioned": true, "matching_runtime_files": [], "readme_rows": 1, "readme_description_matches": true}
wp766-r1-g1-exec-review-1-codex-verdict.md:12 receipt_surface=codex_cli has_caveat=True runtime_files=['ops/reviews/wp766-r1-g1-exec-review-1-codex/run.json']
```
- kết luận: KHÔNG PHẢI LỖI mới trong các tự khai đã tìm: hai thể hiện P2 cũ nay có đính chính và hàng README. Chỉ nhắc service khi mô tả finding không được tính là tự khai; API/shell chung không tự phủ nhận CLI. Không có run đúng ID cho 15 caveat thiếu runtime, không tự chọn surface thực tế; chi tiết từng câu ở surfaces.json và surface-text.log.

### HƯỚNG 7 - trang thai da review
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews`
- output thật:
```text
old_review_caveats_historically_anchored=8 all_next_sha_and_hash_match=True
OLD pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml anchor=c595292cb63fb8c09d7d7b482cda20f9d5f0917f next=pr455-bien-nhan-v2-review-2-codex-verdict.md reviewed=c595292cb63fb8c09d7d7b482cda20f9d5f0917f next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-2-codex-verdict.receipt.yaml anchor=1cd8ec78e42e32e6ff5af8edcc4660b1e601fd93 next=pr455-bien-nhan-v2-review-3-codex-verdict.md reviewed=cb212847375c2319fe0ccad3f7c00c90b870e3ba next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml anchor=dc92839520092a95f097464f4b9a2a252f0d9132 next=pr455-bien-nhan-v2-review-4-codex-verdict.md reviewed=4ef73e69d5f3c419634118983723355e25e38305 next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml anchor=3cff891b81f02dc22cc7ed8b05799c94ade0fc63 next=pr455-bien-nhan-v2-review-5-codex-verdict.md reviewed=670071b700bd97a893d64393ffded0257957d0b3 next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml anchor=020198a437b7ae0008f466959950d3994adba716 next=pr455-bien-nhan-v2-review-6-codex-verdict.md reviewed=5a78c150106ae381461354c77ba2023834330bbd next_verdict_exists_at_anchor_rc=128
OLD pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml anchor=e4d8ecce7e583503b5205a038707ea667a81ed43 next=pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md reviewed=ca960160b477cd16346a293aaa8752772a9921d4 next_verdict_exists_at_anchor_rc=128
OLD pr896-review-1-codex-verdict.receipt.yaml anchor=2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f next=pr896-review-2-codex-verdict.md reviewed=8d56009a09af7b3ef93801df105f9483de212cc7 next_verdict_exists_at_anchor_rc=128
OLD pr915-review-1-codex-verdict.receipt.yaml anchor=a9bc9349103adfc971f4a1f7431a9655aecaaefb next=pr896-review-2-codex-verdict.md reviewed=8d56009a09af7b3ef93801df105f9483de212cc7 next_verdict_exists_at_anchor_rc=128
RESIDUAL pr870-review-1-codex-verdict.receipt.yaml
assurance_ghi_chu:27 Khac ho (codex CLI, executor Claude) nhung verdict la `changes_requested`, va KHONG khai cross_approved: (1) head da merge 06a50c5 KHONG duoc review lai (caveat HEAD-MERGE-CHUA-REVIEW-LAI); (2) model thuc chay chi co loi khai header CLI, khong modelUsage; (3) goi codex tran, khong run.json; (4) checkout review khong bi cuong che read-only.
verdict_usage_caveats.0.mo_ta:97 Verdict cham b38fce8; head da merge la 06a50c5 (them commit va P2 bang dung HINT.patch, 3 dong CLAUDE.md). Khong co luot review nao tren 06a50c5 — "da va" la loi khai cua executor, kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check, khong phai verdict cua reviewer.
README:704 | `pr870-review-1-codex-verdict.md` | `HEAD-MERGE-CHUA-REVIEW-LAI` | Verdict cham `b38fce8`; head da merge la `06a50c5` (va P2 bang dung HINT.patch, 3 dong CLAUDE.md) va KHONG duoc review lai. "Da va" la loi khai executor (kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check), khong phai verdict. |
README:1046 | [`pr870-review-1-codex-verdict.md`](pr870-review-1-codex-verdict.md) | [`.receipt.yaml`](pr870-review-1-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | **`changes_requested`** · `cross_reviewed` (codex CLI khac ho executor, `codex exec` tran, khong run.json; header CLI khai `gpt-6.1-sol`/`xhigh`, model thuc chay KHONG DO DUOC) · 0/0/1/0 · P2 `master-windows-bo-sot-dispatch` da va o `06a50c5` bang dung HINT.patch, KHONG review lai · ban phang nguyen byte cua `pr870-review-1-codex/VERDICT.md`. Merge `5f288ea`. | `b38fce83` | 104880 |
LATER {"path": "ops/reviews/pr870-review-2-codex-verdict.md", "reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "matches_oid": true, "verdict": "approve", "hash_matches": true}
LATER {"path": "ops/reviews/pr870-review-3-codex-verdict.md", "reviewed_sha": "06a50c5feea77c2654f31edd26efeed7eeee62f5", "matches_oid": true, "verdict": "approve", "hash_matches": true}
RESIDUAL pr889-review-1-codex-verdict.receipt.yaml
assurance_ghi_chu:28 Khac ho (codex CLI, executor Claude), co run.json cua launcher, nhung verdict la `changes_requested` va KHONG khai cross_approved: (1) head da merge 094e8d1 KHONG duoc review lai (caveat HEAD-MERGE-CHUA-REVIEW-LAI); (2) model thuc chay chi co loi khai header CLI, khong modelUsage; (3) checkout review khong bi cuong che read-only.
verdict_usage_caveats.1.mo_ta:104 Verdict cham 8d5cccb; head da merge la 094e8d1 (va P2 bang HINT.patch + sua them mot cau, CLAUDE.md +8/-5 theo `git diff --numstat 8d5cccb 094e8d1`) va KHONG duoc review lai. "Da va" la loi khai executor (kiem bang `patch --fuzz=0` + doctrine-scan/doc-claims-check + doc ma ops/cong_cu_test.py:8916), khong phai verdict cua reviewer.
README:710 | `pr889-review-1-codex-verdict.md` | `HEAD-MERGE-CHUA-REVIEW-LAI` | Verdict cham `8d5cccb`; head da merge la `094e8d1` (va P2 bang HINT.patch + sua them mot cau) va KHONG duoc review lai. "Da va" la loi khai executor (`patch --fuzz=0` + doctrine-scan/doc-claims-check + doc ma `ops/cong_cu_test.py:8916`), khong phai verdict. |
README:1047 | [`pr889-review-1-codex-verdict.md`](pr889-review-1-codex-verdict.md) | [`.receipt.yaml`](pr889-review-1-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | **`changes_requested`** · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 9f946d71`, run.json trong kho; header CLI khai `gpt-6.1-sol`/`xhigh`, model thuc chay KHONG DO DUOC) · 0/0/1/0 · P2 `windows-green-does-not-prove-all-baselines` da va o `094e8d1`, KHONG review lai · ban phang nguyen byte cua `pr889-review-1-codex/VERDICT.md`. Merge `6ac385f`. | `8d5cccbb` | 75193 |
LATER {"path": "ops/reviews/pr889-review-2-codex-verdict.md", "reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "matches_oid": true, "verdict": "approve", "hash_matches": true}
LATER {"path": "ops/reviews/pr889-review-3-codex-verdict.md", "reviewed_sha": "094e8d17ae4dfcf21dca63702c9262267bdc072c", "matches_oid": true, "verdict": "approve", "hash_matches": true}
```
- kết luận: LỖI P1 trang-thai-chua-review-da-bi-verdict-sau-bac: 8/8 thể hiện cũ được neo lịch sử đúng, nhưng còn PR870/PR889 lượt 1 ở assurance, caveat và README. Cả lượt 2 và lượt 3 đã review đúng head bản vá. Giữ nguyên verdict lịch sử và assurance; đây không phải quyền land.

### HƯỚNG 9 - moc lich su va cau moi
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/claims.py`
- output thật:
```text
previous_verdict_supplied_equals_flat_and_directory=true
previous_hint_supplied_equals_stored_artifact=true
previous_verdict_bytes_sha256={"bytes": 39386, "sha256": "7357b499ae543c7e80feebae18495e46ce819a3bff5fd3f25cbccb9933e357e8", "matches_receipt": true}
hint_at_82359c4={"parent": "578fb4b69ba52b40516f971824d1080f87345d08", "missing_plus_minus_lines": []}
hint_at_2e4183b={"parent": "c8c1ee015f78fdb143a18cf926f9f3481c2a3dd1", "missing_plus_minus_lines": []}
CHUA_AP_snapshot_8879165={"oid": "887916503161fc1044edf52fd3bfc87cbc79c94c", "caveat_ids": ["HINT-LUOT3-CHUA-AP"], "land_has_block": true}
CHUA_AP_snapshot_c8c1ee0={"oid": "c8c1ee015f78fdb143a18cf926f9f3481c2a3dd1", "caveat_ids": ["HINT-LUOT3-CHUA-AP"], "land_has_block": true}
CHUA_AP_snapshot_ff4ab57={"oid": "ff4ab57b11c94e7a3e12df1f8d8d0b202485951f", "caveat_ids": ["HINT-LUOT4-CHUA-AP"], "land_has_block": true}
CHUA_AP_snapshot_77a0a45={"oid": "77a0a458c6c06f3aafa118953e8e2771daaed911", "caveat_ids": ["HINT-LUOT4-CHUA-AP"], "land_has_block": true}
round_3_readme_and_receipt={"id": "HINT-LUOT3-DA-AP-CAN-VERDICT-MOI", "caveat_rows": 1, "same_description": true, "index_line": 1055, "index": "| [`pr896-review-3-codex-verdict.md`](pr896-review-3-codex-verdict.md) | [`.receipt.yaml`](pr896-review-3-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/2/1/0 tren `82359c4` (head PR #947, mang HINT luot 2) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 513131e0`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · Tai reviewed_sha 82359c4: P1 luot 2 DA DONG; finding moi luc ay la P1 wp766, P1 ho so luot 2 va P2 13 verdict service/API. HINT.patch luot 3 da ap tai 2e4183bc2dc40e6bc306e377fc442ff0f405bbe0 (sau c8c1ee0); can verdict moi tren exact SHA ung vien · ban phang nguyen byte cua `pr896-review-3-codex/VERDICT.md`. Chua merge. | `82359c4d` | 34175 |"}
round_4_readme_and_receipt={"id": "HINT-LUOT4-DA-AP-CAN-VERDICT-MOI", "caveat_rows": 1, "same_description": true, "index_line": 1056, "index": "| [`pr896-review-4-codex-verdict.md`](pr896-review-4-codex-verdict.md) | [`.receipt.yaml`](pr896-review-4-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/3/1/0 tren `2e4183b` (head PR #947, mang HINT luot 3) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 9b8d9a76`; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · ba finding luot 3 DA DONG (P2 dong 13/13 the hien cu); moi: P1 hang muc luc luot 3 con khai HINT chua ap, P1 8 receipt con noi 'chua review', P1 23 receipt phu nhan ancestry da co, P2 pr526-review-3/slice-b-c-review-2 — phan lon NGOAI chuoi #896; HINT.patch luot 4 chua ap tai ff4ab57, da ap o commit ke tiep sau 77a0a45 · ban phang nguyen byte cua `pr896-review-4-codex/VERDICT.md`. Chua merge. | `2e4183bc` | 39386 |"}
new_land_block={"measured_at_sha": "2e4183bc2dc40e6bc306e377fc442ff0f405bbe0", "ghi_chu": "Cau CHUA review lai trong cap_nhat_20261026.cross_review_moi.do_duoc la anh chup luc ghi so truoc luot 2, khong phai trang thai tai 2e4183b. pr896-review-2 da review ban va P2 3bc4244 va caveat a9bc934 tai 8d56009; P2 t162 va hai the hien P1 luot 2 #870/#889 DA DONG. Luot 3 tai 82359c4 kiem them caveat pr889 luot 1. Ket qua cac verdict van changes_requested; khong suy approve/land hay thay don vi land de xuat.", "ghi_chu_luot4": "Khoi cap_nhat_20261026_luot4 o tren (ghi tai ff4ab57) noi HINT.patch luot 4 \"CHUA ap\"; cau ay dung tai ff4ab57 va 77a0a45. HINT.patch luot 4 duoc ap o commit ke tiep sau 77a0a45 tren nhanh claude/pr896-review-2-codex (xem git log), theo lua chon cua chu kho \"Ap nguyen HINT luot 4\"."}
review_2_3_recorded_conclusions={"round2": ["- P2 pr896-review-1 (t162): **ĐÃ ĐÓNG**. `CLAUDE.md:171` giới hạn t162 ở output `os`, nói rõ phải đọc `exclude`/`if` của từng job và dẫn chốt G5 cho mảnh/gom. Sáu mutant `exclude`/`if`/`needs` của cả hai job `gate-cong-cu*`: t162/t161 vẫn xanh 1/1, G5 đỏ; đổi nhánh output os: t162 đỏ 0/1, t161/G5 xanh. Đổi nguồn os riêng: t161 đỏ. Không còn vế \"đọc ca ấy là đọc ma trận HIỆN HÀNH\". `git diff --exit-code 3bc4244 8d56009 -- CLAUDE.md`: rc=0, không có diff (Hướng 1, 11, 19).", "- P1 pr915-review-1 (surface): **ĐÓNG MỘT PHẦN** khi kiểm đủ mọi verdict như chỉ thị. Hai thể hiện lượt 2 được finding cũ nêu đích danh **đã đóng**: đúng caveat + dòng README, đúng dòng 9 và đúng run. Hai thể hiện lượt 3 cũng được đính chính đúng ở dòng 444/309. Nhưng grep độc lập tìm **5** verdict #870/#889 tự khai `codex_service`; #889 **lượt 1**, dòng 7, vẫn thiếu caveat và hàng README dù run `9f946d71` ghi `codex_cli`. Đếm một P1 cho cùng lớp lỗi còn sót, không mở lại bốn thể hiện đã sửa (Hướng 13, 14; finding cuối tệp)."], "round3": "- P1 verdict-surface-bo-sot-pr889-luot1 (lượt 2): **ĐÃ ĐÓNG**. Tại 82359c4, receipt có caveat và README có hàng cảnh báo đúng dòng 7, run `9f946d714c2344fa9691c3d7d4f1b2d9`, run.json:47 `codex_cli`, chương trình `codex`, header `OpenAI Codex v0.163.0`. Verdict 75193 byte, SHA256 `6aa03cacbde6f33a41ba4af60e408b2c742da5959390f28a9cf8420b5cb098f5`, khớp receipt/SHA256SUMS và giữ nguyên từ cha. Tái áp nguyên HINT lượt 2 trên hai tệp ở cha tạo đúng blob của 82359c4. **Lớp lỗi chưa hết toàn kho**: wp766 còn biểu hiện có run JSON bác bỏ, và 13 cặp tự khai service/receipt CLI thiếu điều kiện nguồn được ghi riêng dưới đây."}
successor_after_77a0a45=["1a276a15192013fdb1e472db409133b53ac57944"]
extra_receipt_round4_delta="2\t2\tops/reviews/pr896-review-4-codex-verdict.receipt.yaml"
```
- kết luận: KHÔNG PHẢI LỖI mới ở các câu 1a276a1 thêm/sửa: mốc hint cũ, commit áp, OID, lời kết luận các verdict tiếp theo và supplementary YAML đều khớp dữ liệu được lưu. Câu chưa merge PR947 đo được đúng; chưa land không bị đánh đồng với ancestry. Các trường cũ ngoài hunk còn sai đã ghi ở H6/H7.

### HƯỚNG 10 - HINT tren ban sao
- giả thuyết: kiểm tra độc lập dữ liệu được giao.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py`
- output thật:
```text
changed_files=10; verified_verdict_hashes=291
hint-dry-run rc=0 checking file ops/reviews/wp538-review-2-claude-verdict.receipt.yaml / checking file ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
hint-apply rc=0 patching file ops/reviews/wp538-review-2-claude-verdict.receipt.yaml / patching file ops/reviews/wp540-review-1-claude-verdict.receipt.yaml
hint-t26_ rc=0  / lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
hint-t27_ rc=0  / lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
hint-t138_ rc=0  / lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
hint-bien-nhan-v2 rc=0 bien_nhan_v2: 238 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 291 / TỔNG: ĐẠT
hint-land rc=0 land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73 / TỔNG: ĐẠT
hint-doctrine rc=0 doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
hint-doc-claims rc=0 JSON ok=True
```
- kết luận: KHÔNG PHẢI LỖI của gợi ý theo phép đo: dry-run --fuzz=0 và áp đều sạch; chỉ đổi 9 receipt v2 và README; không đổi verdict/v1/mã cổng. HINT chưa áp vào cây thật; executor tự áp và tự đo.

### HƯỚNG 11: Băm các verdict phẳng và các tham chiếu lồng
- giả thuyết: chỉ kiểm đường dẫn receipt chính có thể bỏ băm lồng của chuỗi verdict ci-windows.
- lệnh: quét đệ quy `verdict_sha256` trong 291 receipt, tính SHA-256 cho mọi `*-verdict.md`; đối chiếu `git diff --name-only 77a0a45 1a276a1 -- 'ops/reviews/*-verdict.md'`.
- output thật: `all_star_verdict_md=269 hash_covered=269`; `untouched_star_verdict_md_parent_to_candidate=True`. Chi tiết: `review_evidence/all-verdict-hashes.json`. Không suy 23 bản `VERDICT.md` trong thư mục không trùng băm receipt phẳng là lỗi: đây không phải các `*-verdict.md` đang được receipt trỏ tới; 15 cặp phẳng/thư mục được xác định là bản nguyên byte đã được so riêng. Phép đo này không tự tạo provenance cho bản phụ.
- kết luận: KHÔNG PHẢI LỖI về byte/băm của mọi verdict phẳng có liên quan.

### HƯỚNG 12: Đối chiếu cuối cùng
- giả thuyết: chạy kiểm tra hoặc tạo hint đã làm bẩn cây gốc.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching`; so status clone sau hoàn nguyên.
- output: HEAD `1a276a15192013fdb1e472db409133b53ac57944`; tree `8ec1b64d4b399303680723bb99d1619ad43485db`; status gốc rỗng (kể cả ignored), status clone sau hoàn nguyên rỗng. HINT 30930 byte, SHA256 `9c400529c2a4026be3049b9b3494221c9961c662d5768b3769a5687cdf52daff`.
- kết luận: KHÔNG PHẢI LỖI; giữ nguyên kho giao review.
