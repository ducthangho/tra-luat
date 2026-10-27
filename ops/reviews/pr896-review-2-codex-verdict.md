verdict: changes_requested
reviewed_sha: 8d56009a09af7b3ef93801df105f9483de212cc7
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

## KẾT LUẬN VỀ HAI FINDING CŨ

- P2 pr896-review-1 (t162): **ĐÃ ĐÓNG**. `CLAUDE.md:171` giới hạn t162 ở output `os`, nói rõ phải đọc `exclude`/`if` của từng job và dẫn chốt G5 cho mảnh/gom. Sáu mutant `exclude`/`if`/`needs` của cả hai job `gate-cong-cu*`: t162/t161 vẫn xanh 1/1, G5 đỏ; đổi nhánh output os: t162 đỏ 0/1, t161/G5 xanh. Đổi nguồn os riêng: t161 đỏ. Không còn vế "đọc ca ấy là đọc ma trận HIỆN HÀNH". `git diff --exit-code 3bc4244 8d56009 -- CLAUDE.md`: rc=0, không có diff (Hướng 1, 11, 19).
- P1 pr915-review-1 (surface): **ĐÓNG MỘT PHẦN** khi kiểm đủ mọi verdict như chỉ thị. Hai thể hiện lượt 2 được finding cũ nêu đích danh **đã đóng**: đúng caveat + dòng README, đúng dòng 9 và đúng run. Hai thể hiện lượt 3 cũng được đính chính đúng ở dòng 444/309. Nhưng grep độc lập tìm **5** verdict #870/#889 tự khai `codex_service`; #889 **lượt 1**, dòng 7, vẫn thiếu caveat và hàng README dù run `9f946d71` ghi `codex_cli`. Đếm một P1 cho cùng lớp lỗi còn sót, không mở lại bốn thể hiện đã sửa (Hướng 13, 14; finding cuối tệp).

Cây đã đo có tree `e93305541ae7d7f87fa5c57dd610fa1be829b0f7`. Phạm vi ghi chỉ là thư mục giao việc và scratch `/tmp/pr896-r2-audit-b3269a02/`; mọi mutant/hint áp trên clone local từ `mirror.git`, checkout đúng reviewed SHA. Không gọi mạng/push. Các phép đo dùng Python với `PYTHONDONTWRITEBYTECODE=1`; lệnh git trong harness kế thừa `GIT_OPTIONAL_LOCKS=0`. Không tự đặt tên execution surface cho phiên này.

## BẢNG ĐO

| Khẳng định | Bên giao khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Exact checkout | Head 8d56009; không shallow | `git rev-parse HEAD HEAD^{tree}` đúng SHA/tree trên; `--is-shallow-repository` = false; status rỗng (H1/H19) | Có |
| CLAUDE.md giữ nguyên bản vá P2 | Bằng tại 3bc4244 | `git diff --exit-code 3bc4244 8d56009 -- CLAUDE.md`: rc=0, stdout rỗng | Có |
| t162 đánh giá output os thật | Push, PR thường/nhãn windows, từng runner_set | CLI gốc t162 1/1; đổi nhánh windows-only trả hai nền: t162 rc=1, 0/1; t161/G5 rc=0 (H11) | Có |
| t162 không khóa exclude/if/needs | Phải đọc YAML cấp job | Cả 6 mutant trên hai job mảnh/gom: t162/t161 rc=0, 1/1 (H11) | Có |
| Phạm vi gate-cong-cu* | Phần mảnh/gom có G5 | YAML chỉ có `gate-cong-cu`, `gate-cong-cu-gop`; cả 6 mutant bị `loi_g5_workflow` phát hiện, rc=1, mỗi mutant 1 lỗi | Có, phủ đủ các job tiền tố tại SHA này |
| t161 chỉ giữ cấu trúc | Chung nguồn os, không fromJSON trong output | Đổi os riêng: t161 đỏ 0/1; bọc fromJSON output: t161/t162 đỏ 0/1, G5 xanh; đổi ngữ nghĩa nhánh: t161 xanh (H11) | Có |
| Không còn khai đọc test là ma trận hiện hành | Câu cũ đã bỏ | `rg -n 'đọc ca ấy là đọc ma trận HIỆN HÀNH\|đổi ma trận mà quên ca ấy' CLAUDE.md`: rc=1, không match (H19) | Có |
| Caveat surface cho #870/#889 lượt 2 | Bổ sung ở cả sidecar + README | run 2699e2d8 / d955f9ef đều CLI; verdict dòng 9; hàng README 701/707; text đính chính đúng (H13) | Có |
| Caveat surface cho #870/#889 lượt 3 | Bổ sung tương tự | run 94125115 / 4764bd6f đều CLI; verdict dòng 444/309; hàng README 717/722; text đúng (H13) | Có |
| Caveat đủ mọi verdict cần nó | Phải kiểm hết các *-verdict.md | `grep -nH codex_service ...`: 5 verdict; #889 lượt 1 dòng 7, run 9f946d71 CLI, không caveat/hàng README (H13) | **Không: P1** |
| Chốt khi mất một hàng README | t27 bảo vệ mục lục caveat đã khai | Xoá riêng từng hàng của 4 caveat hiện có: t27 rc=1, 0/1; t26/t138 rc=0, 1/1 (H14) | Có; t26/t138 không có răng với biến thể này |
| Chốt khi mất caveat trong receipt | Không được suy cổng xanh = đủ caveat | Xoá riêng caveat khỏi từng receipt: t26/t27/t138 đều rc=0, 1/1 (H14) | Giới hạn: cả ba không có răng khi caveat chưa được khai |
| Model #870 lượt 3 | 21 sự kiện, 21 response_id; gpt-6.1-sol | Đếm trực tiếp JSON: 21/21, mọi event=response.created, model chỉ gpt-6.1-sol, DO_DUOC (H12) | Có |
| Model #889 lượt 3 | 19 sự kiện, 19 response_id; gpt-6.1-sol | Đếm trực tiếp JSON: 19/19, cùng model/trạng thái (H12) | Có |
| Model #915 lượt 1 | 26 sự kiện, 26 response_id; gpt-6.1-sol | Đếm trực tiếp JSON: 26/26, cùng model/trạng thái (H12) | Có |
| Byte/hash verdict mới | #870 45798 / 0021b5b2…; #889 28705 / c05bc41d…; #915 46455 / 839757cc… | Tính SHA-256 và len(byte): khớp toàn bộ hash đầy đủ trong sidecar; bản phẳng = bản thư mục (H12) | Có |
| reviewed_sha/tree #870 mới | 06a50c5 / 0fa694da… | Dòng 2 verdict = run.head = receipt; git tree đúng 0fa694daf17e10c37fc3e61690531ade4bd528bf (H12) | Có |
| reviewed_sha/tree #889 mới | 094e8d1 / 55f5edf2… | Dòng 2 verdict = run.head = receipt; git tree đúng 55f5edf2f8601c976f390e8994193129a71203a1 (H12) | Có |
| reviewed_sha/tree #915 mới | 2789cbb / 6f299d7f… | Dòng 2 verdict = run.head = receipt; git tree đúng 6f299d7f70269ec32522fc4ea28c9d2d70c5424b (H12) | Có |
| base_sha | Lần lượt 9e9a74b / e63961f / 50a59a9 | Git giải ra đúng OID đầy đủ trong receipt; khớp PROMPT.md; là ancestor, numstat trùng byte (H16) | Có |
| thoi_luong_giay | 741.994 / 533.139 / 690.678 | JSON và hiệu hai timestamp đều đúng ba số ấy; ma_thoat=0, trạng thái xong (H12) | Có |
| prompt_sha256 | 5e69b5fe… / a7e97c93… / 29eba906… | SHA-256 PROMPT.md = từng trường JSON, đủ 64 hex được ghi ở H12 | Có |
| so_p* và verdict | #870/#889 approve 0/0/0/0; #915 changes_requested 0/1/0/0 | Dòng Kết quả + dòng 1 verdict khớp receipt và cap_nhat (H12/H16) | Có |
| evidence_url | cc0a3c9 chỉ mang hiện vật | Cả 3 URL ghim cc0a3c98ff8fee7aefa0e64982fa3532da2877d8; git show blob bằng verdict; 106 tệp đều trong ops/reviews, không receipt/code sản phẩm (H12/H16) | Có |
| Chuỗi commit #915 | 3bc4244 doc +3/-2; 7cfe062 hiện vật 91 tệp; 2789cbb ghi sổ 4 tệp | git diff-tree/numstat đúng 1/91/4 tệp; diff.patch #870/#889 trùng byte Git; diff #915 bỏ khỏi kho tái lập đúng 1334705 byte/hash (H16) | Có |
| Assurance #870/#889 | cross_approved | Approve trên đúng head đã merge; reviewer gpt đọc được từ run; executor claude suy theo provider, giới hạn đã có caveat (H12/H16) | Đủ theo nguồn đã khai; không chứng nhận model executor bằng máy |
| Assurance #915 / #896 | cross_reviewed; reviewer_assurance_81 CHUA DAT | changes_requested 1 P1 nên không nâng cross_approved; không có approve sạch trên 816f439 hoặc trạng thái sửa (H12/H16) | Có tại SHA đang chấm |
| cap_nhat ba hồ sơ | Lượt/provider/verdict/SHA/count/assurance từ receipt | Sáu đối chiếu mỗi hồ sơ đều true (H16) | Có |
| §10.2.2 Run | Push master, attempt 1, success; run 39752735359 / 39921552473 / 39983914661 | Đọc readback-run, đúng head 5f288ea / 6ac385f / 27dcc3b, path ci.yml (H15) | Có, nguồn tồn tại |
| §10.2.2 Checkout | Job 119738461348 / 120319840559 / 120524600728 | Log chứa SHA đúng; jobs đúng run/head, runner_id khác 0, labels Ubuntu; artifact head/tree khớp Git, identity_after bằng identity (H15) | Có, nguồn tồn tại |
| §10.2.2 Gate output | Artifact 12415205903 / 12488609174 / 12515154206 | JSON/output có thật; pass, rc=0, positive_verified=true; marker thật 1731/1731; SHA-256 output khớp (H15) | Có cho bytes JSON/output đã lưu |
| Digest ZIP tải từ REST | Summary nói digest tải về khớp REST | Digest trong readback-artifacts khớp summary; raw ZIP không lưu, không băm lại ZIP được (H15) | **KHÔNG ĐO ĐƯỢC lại raw ZIP**; giới hạn đã ghi zip KHONG kem |
| §10.2.2 Workflow definition / landed | not_measured (403); cả 3 landed=false | Summary + YAML giữ đúng trạng thái thiếu; blob ci.yml ba ref khớp Git chỉ là bằng chứng phụ, không nâng thành definition của run (H15) | Có về giới hạn khai; không lấy 3/4 làm 4/4 |
| SHA256SUMS ba hiện vật mới | Sạch | `sha256sum -c SHA256SUMS`: rc=0, 16/30/54 dòng OK (H12) | Có |
| SHA256SUMS cả lịch sử liên quan | Không sửa byte lịch sử | Tám thư mục review: rc=0, lần lượt 7/31/16/23/22/30/32/54 OK (H17) | Có |
| SHA256SUMS provenance land | Sạch | `sha256sum -c SHA256SUMS.txt`: rc=0, #870 18, #889 21, #896 25 dòng OK (H15) | Có |
| Cây gốc không bị sửa | Reviewer chỉ đọc + đo | Snapshot 7425 tệp thường gồm .git: added=[], removed=[], changed_content_or_mode=[]; git status kể cả ignored rỗng (H19) | Có so snapshot H1 |

Các lệnh gate bắt buộc chạy **tại `cay-kho/`**; rc và kết luận thật:

| Lệnh | rc | Kết luận / bằng chứng dương |
|---|---|---|
| `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t138_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t161_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t162_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | `bien_nhan_v2: 235 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 288`; `TỔNG: ĐẠT` |
| `python3 ops/land_evidence_nguon.py --root .` | 0 | `land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73`; `TỔNG: ĐẠT` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | JSON `"ok": true`, files_scanned=115, claims_flagged=381, advisory_count=381; không gọi 381 advisory là không có claim |

## BẢNG SĂN

Nhật ký được ghi tăng dần trong lúc đo; các mục dưới giữ command và output thật. Các ca gate được ghi riêng để dễ kiểm N/N, không dùng chín ca gate làm chín hướng săn độc lập. Các hướng độc lập gồm định danh Git, phạm vi workflow qua mutant, byte/model của receipt, phủ nghĩa caveat, phản chứng quan hệ receipt–README, nguồn bốn mốc CI, base/diff/cập nhật và kiểm hint.

### HƯỚNG 1: Định danh cây và tính bất biến của bản vá P2

Giả thuyết: HEAD hoặc CLAUDE.md không đúng bản đã giao.

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho diff --exit-code 3bc4244 8d56009 -- CLAUDE.md`; `git -C cay-kho status --short --untracked-files=all`.

Output: HEAD=`8d56009a09af7b3ef93801df105f9483de212cc7`; tree=`e93305541ae7d7f87fa5c57dd610fa1be829b0f7`; diff rc=0, stdout rỗng; status rc=0, stdout rỗng. Đã lưu snapshot 7425 tệp để so cuối lượt.

Kết luận: KHÔNG PHẢI LỖI của định danh/bất biến.

### HƯỚNG 2: Cổng gốc — ops/lease_publish_test.py --chi-ca=t26_

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 ops/lease_publish_test.py --chi-ca=t26_`.

Output thật:
```text
rc=0
>>> vao t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 2026-10-26T04:26:41Z
<<< ra t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 1.835s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-0.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 3: Cổng gốc — ops/lease_publish_test.py --chi-ca=t27_

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 ops/lease_publish_test.py --chi-ca=t27_`.

Output thật:
```text
rc=0
>>> vao t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 2026-10-26T04:26:43Z
<<< ra t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 3.974s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-1.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 4: Cổng gốc — ops/lease_publish_test.py --chi-ca=t138_

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 ops/lease_publish_test.py --chi-ca=t138_`.

Output thật:
```text
rc=0
>>> vao t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 2026-10-26T04:26:48Z
<<< ra t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 0.190s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-2.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 5: Cổng gốc — ops/lease_publish_test.py --chi-ca=t161_

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 ops/lease_publish_test.py --chi-ca=t161_`.

Output thật:
```text
rc=0
>>> vao t161_M3_chot_nguon_duy_nhat_ma_tran_ci 2026-10-26T04:26:48Z
<<< ra t161_M3_chot_nguon_duy_nhat_ma_tran_ci 0.108s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-3.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 6: Cổng gốc — ops/lease_publish_test.py --chi-ca=t162_

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 ops/lease_publish_test.py --chi-ca=t162_`.

Output thật:
```text
rc=0
KHÔNG ĐO ĐƯỢC: biểu thức không khớp hình chuẩn tối giản của chuan-bi: 'fromJSON(\'["ubuntu-latest"]\')'
<<< ra t162_M4_evaluator_toi_gian_chuan_bi 0.067s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-4.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 7: Cổng gốc — ops/bien_nhan_v2.py --root .

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 ops/bien_nhan_v2.py --root .`.

Output thật:
```text
rc=0
bien_nhan_v2: 235 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 288
TỔNG: ĐẠT
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-5.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 8: Cổng gốc — ops/land_evidence_nguon.py --root .

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 ops/land_evidence_nguon.py --root .`.

Output thật:
```text
rc=0
ĐẠT ops/land/pr932-wp748-r26-land-evidence.yaml
ĐẠT ops/land/pr933-wp929-land-evidence.yaml
land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-6.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 9: Cổng gốc — .claude/dev/packet_loop.py doctrine-scan --root .

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 .claude/dev/packet_loop.py doctrine-scan --root .`.

Output thật:
```text
rc=0
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-7.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 10: Cổng gốc — scripts/tl.py doc-claims-check --json

Giả thuyết: cổng có lỗi hoặc không đo đủ ca.

Lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `python3 scripts/tl.py doc-claims-check --json`.

Output thật:
```text
rc=0
{"ok": true, "files_scanned": 115, "claims_flagged": 381, "advisory_count": 381}
```

Log đầy đủ: `/tmp/pr896-r2-audit-b3269a02/gate-8.log`.

Kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 11: Phạm vi thực của t162/t161/G5 bằng đột biến workflow

Giả thuyết: CLAUDE.md còn khai rộng hơn phép đo hoặc bỏ sót job tiền tố gate-cong-cu.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/workflow_mutations.py`. Bản sao local từ mirror.git checkout đúng 8d56009; mỗi mutant chỉ đổi YAML; gọi nguyên CLI `python3 ops/lease_publish_test.py --chi-ca=t162_` / `--chi-ca=t161_`, rồi gọi hàm có sẵn `loi_g5_workflow(yaml.safe_load(ci.yml))` (rc=bool(errors)).

Output thật:
```text
gate-cong-cu* jobs=['gate-cong-cu', 'gate-cong-cu-gop']
MUTANT baseline
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=0; loi_g5_workflow errors=0
MUTANT gate-cong-cu__exclude
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=1; loi_g5_workflow errors=1 | gate-cong-cu: matrix phải đúng os + manh [0, 1, 2, 3, 4, 5, 6, 7] + exclude [{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}], thấy {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'manh': [0, 1, 2, 3, 4, 5, 6, 7]}
MUTANT gate-cong-cu__if
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=1; loi_g5_workflow errors=1 | gate-cong-cu: bước G5 có điều kiện hoặc được phép bỏ qua lỗi
MUTANT gate-cong-cu__needs
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=1; loi_g5_workflow errors=1 | gate-cong-cu: needs/if phải đúng 'chuan-bi'/"${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", thấy []/"${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"
MUTANT gate-cong-cu-gop__exclude
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=1; loi_g5_workflow errors=1 | gate-cong-cu-gop: matrix phải đúng os + exclude [{'os': 'windows-latest'}], thấy {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}
MUTANT gate-cong-cu-gop__if
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=1; loi_g5_workflow errors=1 | gate-cong-cu-gop: needs/if phải đúng ['chuan-bi', 'gate-cong-cu']/"${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}", thấy ['chuan-bi', 'gate-cong-cu']/'${{ false }}'
MUTANT gate-cong-cu-gop__needs
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=1; loi_g5_workflow errors=1 | gate-cong-cu-gop: needs/if phải đúng ['chuan-bi', 'gate-cong-cu']/"${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}", thấy []/"${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}"
MUTANT output_os__windows_only_returns_two
t162 rc=1;   ĐỎ  t162_M4_evaluator_toi_gian_chuan_bi: dispatch windows-only phải chỉ chạy windows-latest, nhận được: ['ubuntu-latest', 'windows-latest'] | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=0; loi_g5_workflow errors=0
MUTANT output_os__wrapped_fromJSON
t162 rc=1;   ĐỎ  t162_M4_evaluator_toi_gian_chuan_bi: ValueError: KHÔNG ĐO ĐƯỢC: biểu thức không khớp hình chuẩn tối giản của chuan-bi: 'fromJSON(\'["ubuntu-latest"]\')' | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=1;   ĐỎ  t161_M3_chot_nguon_duy_nhat_ma_tran_ci: ci.yml thật có output bọc fromJson: ['job \'chuan-bi\' output \'os\' bọc fromJson/fromJSON: \'${{ fromJSON(\\\'["ubuntu-latest"]\\\') }}\' (outputs chỉ nhận chuỗi)'] | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=0; loi_g5_workflow errors=0
MUTANT gate__independent_os
t162 rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t161 rc=1;   ĐỎ  t161_M3_chot_nguon_duy_nhat_ma_tran_ci: ci.yml thật có job lén khai os: riêng: ["job 'gate' khai 'os:' riêng bằng danh sách tĩnh: ['ubuntu-latest'] (không tham chiếu needs.chuan-bi.outputs.os)"] | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
loi_g5_workflow rc=1; loi_g5_workflow errors=1 | gate: env/runs-on/strategy cấp job lệch hình dạng ghim
```

Kết luận: KHÔNG PHẢI LỖI của câu đã vá: t162 chỉ đánh giá output os; t161 bảo vệ nguồn/cấu trúc; G5 bảo vệ cả hai job mảnh/gom hiện có. Câu cũ "đọc ca ấy là đọc ma trận HIỆN HÀNH" không còn trong đoạn.

### HƯỚNG 12: Đo ba biên nhận mới và byte hiện vật

Giả thuyết: số sự kiện/model, hash/bytes, exact SHA/tree/base, thời lượng, prompt, số finding, assurance hoặc evidence_url sai.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/receipt_audit.py`; các lệnh git và `sha256sum -c SHA256SUMS` chạy local, không mạng.

Output thật:
```text
pr870-review-3-codex
model_phuc_vu events=21; distinct response_id=21; event_types=['response.created']; models=['gpt-6.1-sol']; status=DO_DUOC
sha256 actual=0021b5b2f90e0da39a92c11041c3236980acfbbd0b22f46d0044ac8334f16e81; receipt=0021b5b2f90e0da39a92c11041c3236980acfbbd0b22f46d0044ac8334f16e81; bytes=45798/45798; flat==original=True
reviewed_sha=06a50c5feea77c2654f31edd26efeed7eeee62f5; run.head=06a50c5feea77c2654f31edd26efeed7eeee62f5; verdict.line2=reviewed_sha: 06a50c5feea77c2654f31edd26efeed7eeee62f5
reviewed_tree git=0fa694daf17e10c37fc3e61690531ade4bd528bf; receipt=0fa694daf17e10c37fc3e61690531ade4bd528bf; match=True
base_sha=9e9a74b2a396ef458d25c51a5563efafbb45ba0c; head.parents=b38fce83d0e97981012072ca2a2023ac726e5b2e; base_is_parent=False; merge.parents=9e9a74b2a396ef458d25c51a5563efafbb45ba0c 06a50c5feea77c2654f31edd26efeed7eeee62f5
duration run=741.994; timestamp_delta=741.994; ma_thoat=0; trang_thai=xong
prompt_sha256 actual=5e69b5fef7d5d51b7dc86a9946ede84bc4943248ace0145518282fc94f6a1d15; run=5e69b5fef7d5d51b7dc86a9946ede84bc4943248ace0145518282fc94f6a1d15; match=True
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.; receipt.so_p=[0, 0, 0, 0]; verdict=approve; assurance=cross_approved; executor_provider=claude
evidence_commit=cc0a3c98ff8fee7aefa0e64982fa3532da2877d8; blob_matches_current=True; changed_files=106; all_under_reviews=True; yaml_receipts_changed=[]
sha256sum -c SHA256SUMS: rc=0; OK=16; lines=16; stderr=
numstat.txt (trích tối đa 1800 ký tự): 21	9	CLAUDE.md
OMITTED.txt: # Tep KHONG vao kho (>500 KB): sha256  byte  duong_dan_tuong_doi. diff.patch tai lap bang git diff base..head.
053a841624d10d1413e49d82416a9f3f724b8e8d0f7a064298920293e0579ac0  652715  review_evidence/checkout-before.json
pr889-review-3-codex
model_phuc_vu events=19; distinct response_id=19; event_types=['response.created']; models=['gpt-6.1-sol']; status=DO_DUOC
sha256 actual=c05bc41d9232d99a9e0c49199e022a9a64b01227674144da73bf50b9b7ce445f; receipt=c05bc41d9232d99a9e0c49199e022a9a64b01227674144da73bf50b9b7ce445f; bytes=28705/28705; flat==original=True
reviewed_sha=094e8d17ae4dfcf21dca63702c9262267bdc072c; run.head=094e8d17ae4dfcf21dca63702c9262267bdc072c; verdict.line2=reviewed_sha: 094e8d17ae4dfcf21dca63702c9262267bdc072c
reviewed_tree git=55f5edf2f8601c976f390e8994193129a71203a1; receipt=55f5edf2f8601c976f390e8994193129a71203a1; match=True
base_sha=e63961f27b53e66db8e6600009f97d5706743063; head.parents=8d5cccbb13b0b2c5ba1c9bbc4f8af410a19f87b8; base_is_parent=False; merge.parents=daf89615efff9fde33039036ddf7f23ec9cb1c10 094e8d17ae4dfcf21dca63702c9262267bdc072c
duration run=533.139; timestamp_delta=533.139; ma_thoat=0; trang_thai=xong
prompt_sha256 actual=a7e97c9391c2d52c4632cac505f946b496be4b6b3544404dab7f600d0cca0064; run=a7e97c9391c2d52c4632cac505f946b496be4b6b3544404dab7f600d0cca0064; match=True
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.; receipt.so_p=[0, 0, 0, 0]; verdict=approve; assurance=cross_approved; executor_provider=claude
evidence_commit=cc0a3c98ff8fee7aefa0e64982fa3532da2877d8; blob_matches_current=True; changed_files=106; all_under_reviews=True; yaml_receipts_changed=[]
sha256sum -c SHA256SUMS: rc=0; OK=30; lines=30; stderr=
numstat.txt (trích tối đa 1800 ký tự): 12	0	CLAUDE.md
pr915-review-1-codex
model_phuc_vu events=26; distinct response_id=26; event_types=['response.created']; models=['gpt-6.1-sol']; status=DO_DUOC
sha256 actual=839757cc4bdbba080e93f920740e10814e184d8a553b75f43936fd36c5339a23; receipt=839757cc4bdbba080e93f920740e10814e184d8a553b75f43936fd36c5339a23; bytes=46455/46455; flat==original=True
reviewed_sha=2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f; run.head=2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f; verdict.line2=reviewed_sha: 2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f
reviewed_tree git=6f299d7f70269ec32522fc4ea28c9d2d70c5424b; receipt=6f299d7f70269ec32522fc4ea28c9d2d70c5424b; match=True
base_sha=50a59a945026a2ab2f97dc0e7ef7b5a540e17652; head.parents=7cfe06212cb43f92d5753940116079e671d9c385; base_is_parent=False; merge.parents=ba222ffd1615f0d74b59985b9612f725211b62f5 2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f
duration run=690.678; timestamp_delta=690.678; ma_thoat=0; trang_thai=xong
prompt_sha256 actual=29eba9065f370e29962bc520d6b3331669cfe3ef43ea646b29c76c004717ccab; run=29eba9065f370e29962bc520d6b3331669cfe3ef43ea646b29c76c004717ccab; match=True
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.; receipt.so_p=[0, 1, 0, 0]; verdict=changes_requested; assurance=cross_reviewed; executor_provider=claude
evidence_commit=cc0a3c98ff8fee7aefa0e64982fa3532da2877d8; blob_matches_current=True; changed_files=106; all_under_reviews=True; yaml_receipts_changed=[]
sha256sum -c SHA256SUMS: rc=0; OK=54; lines=54; stderr=
numstat.txt (trích tối đa 1800 ký tự): 3	2	CLAUDE.md
17	0	ops/reviews/README.md
987	0	ops/reviews/pr870-review-2-codex-verdict.md
112	0	ops/reviews/pr870-review-2-codex-verdict.receipt.yaml
49	0	ops/reviews/pr870-review-2-codex/PROMPT.md
31	0	ops/reviews/pr870-review-2-codex/SHA256SUMS
3816	0	ops/reviews/pr870-review-2-codex/VERDICT.incremental.md
987	0	ops/reviews/pr870-review-2-codex/VERDICT.md
47	0	ops/reviews/pr870-review-2-codex/diff.patch
0	0	ops/reviews/pr870-review-2-codex/doc-claims-check.stderr
2821	0	ops/reviews/pr870-review-2-codex/doc-claims-check.stdout
0	0	ops/reviews/pr870-review-2-codex/doctrine-scan.stderr
1	0	ops/reviews/pr870-review-2-codex/doctrine-scan.stdout
130	0	ops/reviews/pr870-review-2-codex/evidence-consistency.txt
2883	0	ops/reviews/pr870-review-2-codex/evidence-events-setup.md
60	0	ops/reviews/pr870-review-2-codex/evidence-events.txt
12	0	ops/reviews/pr870-review-2-codex/evidence-gate_scope.txt
17	0	ops/reviews/pr870-review-2-codex/evidence-gates-summary.txt
2837	0	ops/reviews/pr870-review-2-codex/evidence-gates.txt
40	0	ops/reviews/pr870-review-2-codex/evidence-historical.txt
175	0	ops/reviews/pr870-review-2-codex/evidence-history.txt
22	0	ops/reviews/pr870-review-2-codex/evidence-launcher.txt
81	0	ops/reviews/pr870-review-2-codex/evidence-matrix.txt
10	0	ops/reviews/pr870-review-2-codex/evidence-preflight.txt
35	0	ops/reviews/pr870-review-2-codex/evidence-readback.txt
14	0	ops/reviews/pr870-review-2-codex/evidence-sandbox_end.txt
46	0	ops/reviews/pr870-review-2-codex/evidence-scope.txt
27	0	ops/reviews/pr870-review-2-codex/evidence-workflows.txt
61	0	ops/reviews/pr870-review-2-codex/extracted-evaluator.py
1	0	ops/reviews/pr870-review-2-codex/numstat.txt
148	0	ops/reviews/pr870-review-2-codex/review_finalize.py
391	0	ops/reviews/pr870-review-2-codex/review_probe.py
1	0	ops/rev
OMITTED.txt: # Tep KHONG vao kho (>500 KB): sha256  byte  duong_dan_tuong_doi. diff.patch tai lap bang git diff base..head.
14bfd8ec9bb561d2ed4b395acbf044cb573bf251b7b9a4190e109ea02b6bb592  1334705  diff.patch
f900abf33bbb9e22035df6e3d41088577265f1bc42e8c85edf45f1ce037c92d2  987298  review_evidence/snapshot-after.json
f900abf33bbb9e22035df6e3d41088577265f1bc42e8c85edf45f1ce037c92d2  987298  review_evidence/snapshot-before.json
cc0a3c9 changed top roots=['ops/reviews', 'ops/reviews/pr870-review-3-codex', 'ops/reviews/pr870-review-3-codex/review_evidence', 'ops/reviews/pr870-review-3-codex/run', 'ops/reviews/pr889-review-3-codex', 'ops/reviews/pr889-review-3-codex/review_evidence', 'ops/reviews/pr889-review-3-codex/run', 'ops/reviews/pr915-review-1-codex', 'ops/reviews/pr915-review-1-codex/review_evidence', 'ops/reviews/pr915-review-1-codex/run']
```

Kết luận: KHÔNG PHẢI LỖI của các trường đã đối chiếu. `cross_approved` chỉ ở hai lượt approve #870/#889, model reviewer gpt đọc được; executor claude là suy theo provider, giới hạn này đã khai trong caveat. #915 changes_requested giữ cross_reviewed.

### HƯỚNG 13: Kiểm phủ caveat trên TOÀN BỘ verdict #870/#889

Giả thuyết: danh sách bên giao bỏ sót verdict tự khai sai surface.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/surface_audit.py` (gồm grep thật và đọc từng run.json, receipt, README).

Output thật:
```text
$ grep -nH codex_service ops/reviews/pr870*-verdict.md ops/reviews/pr889*-verdict.md
rc=0
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r2b/cay-kho/ops/reviews/pr870-review-2-codex-verdict.md:9:execution_surface: codex_service (agent có công cụ shell; không phải ChatGPT Web)
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r2b/cay-kho/ops/reviews/pr870-review-3-codex-verdict.md:444:Approve về nội dung diff tại exact SHA đã nêu, với 10 hướng săn và bảng đo; không phải merge/land authorization hoặc xác nhận assurance danh tính model của launcher. Provider `openai_codex`, execution surface `codex_service` (agent dùng shell tool trong môi trường cloud, không suy thành codex CLI/Desktop), transport `machine`. Model/effort thực phục vụ từng request và cặp danh tính executor–reviewer không được đo từ công cụ trong checkout này; launcher/chủ thể vận chuyển tự giữ bằng chứng runtime của lượt này.
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r2b/cay-kho/ops/reviews/pr889-review-1-codex-verdict.md:7:Phạm vi: chỉ đọc/đo `cay-kho/`; không mạng, không push, không sửa cây reviewed. Các script và evidence đều ở thư mục cha. Provider `openai_codex`, model family `openai`; phiên Codex có shell cục bộ, không đi qua `codex exec` hay Desktop nên theo phân loại của kho là `execution_surface: codex_service`, `transport: machine`. Không có runtime receipt để machine-verify model/effort/session identity; không tự cấp assurance/approval land. Authority cho review và artifact là chỉ thị trực tiếp trong `runs/9f946d71/prompt.snapshot`.
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r2b/cay-kho/ops/reviews/pr889-review-2-codex-verdict.md:9:Quyền và phạm vi theo chỉ thị trực tiếp `runs/d955f9ef/prompt.snapshot`. Reviewer: Codex, họ model OpenAI/GPT-6; provider `openai_codex`, execution surface `codex_service`, transport `machine` theo phân loại repository cho agent có shell không chạy qua `codex exec`/Desktop. Không có receipt máy để chứng nhận biến thể model/effort hoặc assurance. Không gọi mạng, không push, không sửa `cay-kho/`; chỉ ghi artifact ở thư mục cha.
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r2b/cay-kho/ops/reviews/pr889-review-3-codex-verdict.md:309:Định danh: reviewer Codex; provider `openai_codex`; execution_surface `codex_service` (có công cụ shell trực tiếp, không phải ChatGPT Web human-mediated); transport `machine`. Không suy model thực tế từ tác giả commit hoặc tên launcher; định danh model máy chủ trả không được kiểm độc lập trong phép đo repo này. Không tự cấp assurance/approval cho state machine hay thao tác land.
pr870-review-2-codex: selfclaim_lines=[9]; flat==original=True
run=ops/reviews/pr870-review-2-codex/run/run.json; run_id=2699e2d8b1a54b8e86bfa3efb9a4b61b; execution_surface=codex_cli; lenh.chuong_trinh=codex; receipt.surface=codex_cli
receipt_caveat=True; README_surface_rows=[701]
caveat.mo_ta=Verdict dong 9 tu khai `codex_service`, nhung run.json 2699e2d8 ghi lenh.chuong_trinh=codex va execution_surface=codex_cli; header CLI cung ghi OpenAI Codex v0.163.0. Dinh chinh be mat thanh codex_cli; giu nguyen byte verdict lich su. Day khong phai chung thuc model/effort da phuc vu.
pr870-review-3-codex: selfclaim_lines=[444]; flat==original=True
run=ops/reviews/pr870-review-3-codex/run/run.json; run_id=941251157e4b4a35be82d6daefb390b2; execution_surface=codex_cli; lenh.chuong_trinh=codex; receipt.surface=codex_cli
receipt_caveat=True; README_surface_rows=[717]
caveat.mo_ta=Verdict dong 444 tu khai execution surface `codex_service`, nhung run.json 94125115 ghi lenh.chuong_trinh=codex va execution_surface=codex_cli (launcher.py run -- codex exec). Cung loi pr915-review-1-codex bat o luot 2; dinh chinh be mat thanh codex_cli, giu nguyen byte verdict. Khong anh huong ho model: model_phuc_vu do_may.
pr889-review-1-codex: selfclaim_lines=[7]; flat==original=True
run=ops/reviews/pr889-review-1-codex/run/run.json; run_id=9f946d714c2344fa9691c3d7d4f1b2d9; execution_surface=codex_cli; lenh.chuong_trinh=codex; receipt.surface=codex_cli
receipt_caveat=False; README_surface_rows=[]
pr889-review-2-codex: selfclaim_lines=[9]; flat==original=True
run=ops/reviews/pr889-review-2-codex/run/run.json; run_id=d955f9efb3624041b86dcf97f2624175; execution_surface=codex_cli; lenh.chuong_trinh=codex; receipt.surface=codex_cli
receipt_caveat=True; README_surface_rows=[707]
caveat.mo_ta=Verdict dong 9 tu khai `codex_service`, nhung run.json d955f9ef ghi lenh.chuong_trinh=codex va execution_surface=codex_cli; header CLI cung ghi OpenAI Codex v0.163.0. Cau "khong chay qua codex exec/Desktop" trong verdict khong khop hien vat launcher. Dinh chinh be mat thanh codex_cli; giu nguyen byte verdict lich su. Day khong phai chung thuc model/effort da phuc vu.
pr889-review-3-codex: selfclaim_lines=[309]; flat==original=True
run=ops/reviews/pr889-review-3-codex/run/run.json; run_id=4764bd6fee0645728143c3eb4f1a417b; execution_surface=codex_cli; lenh.chuong_trinh=codex; receipt.surface=codex_cli
receipt_caveat=True; README_surface_rows=[722]
caveat.mo_ta=Verdict dong 309 tu khai execution surface `codex_service`, nhung run.json 4764bd6f ghi lenh.chuong_trinh=codex va execution_surface=codex_cli (launcher.py run -- codex exec). Cung loi pr915-review-1-codex bat o luot 2; dinh chinh be mat thanh codex_cli, giu nguyen byte verdict. Khong anh huong ho model: model_phuc_vu do_may.
service_verdicts=5; verdicts=['pr870-review-2-codex', 'pr870-review-3-codex', 'pr889-review-1-codex', 'pr889-review-2-codex', 'pr889-review-3-codex']; caveat_covered=4; missing=pr889-review-1-codex
```

Kết luận: LỖI — có NĂM verdict, caveat chỉ phủ BỐN. Thiếu #889 lượt 1; bản phẳng và bản thư mục đều có câu sai ở dòng 7; run 9f946d71 và receipt đều ghi codex_cli. Các dòng trích của bốn caveat hiện có (9/9/444/309) đúng nguyên văn nguồn.

### HƯỚNG 14 (pr870-review-2-codex__delete_README_row): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr870-review-2-codex__delete_README_row
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=1;   ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' của pr870-review-2-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr870-review-2-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó. | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI của t27: xoá hàng README khiến t27 đỏ 0/1; t26 và t138 không có răng đối với biến thể này.

### HƯỚNG 14 (pr870-review-2-codex__delete_receipt_caveat): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr870-review-2-codex__delete_receipt_caveat
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI riêng của hợp đồng t26/t27/t138; đây là giới hạn đã đo: xoá caveat khỏi receipt, cả ba vẫn xanh 1/1. Các chốt không có răng đối với caveat CHƯA ĐƯỢC KHAI; không coi cổng xanh là chứng minh đủ caveat. Finding cần sửa là thể hiện bị bỏ sót ở Hướng 13.

### HƯỚNG 14 (pr889-review-2-codex__delete_README_row): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr889-review-2-codex__delete_README_row
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=1;   ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' của pr889-review-2-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr889-review-2-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó. | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI của t27: xoá hàng README khiến t27 đỏ 0/1; t26 và t138 không có răng đối với biến thể này.

### HƯỚNG 14 (pr889-review-2-codex__delete_receipt_caveat): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr889-review-2-codex__delete_receipt_caveat
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI riêng của hợp đồng t26/t27/t138; đây là giới hạn đã đo: xoá caveat khỏi receipt, cả ba vẫn xanh 1/1. Các chốt không có răng đối với caveat CHƯA ĐƯỢC KHAI; không coi cổng xanh là chứng minh đủ caveat. Finding cần sửa là thể hiện bị bỏ sót ở Hướng 13.

### HƯỚNG 14 (pr870-review-3-codex__delete_README_row): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr870-review-3-codex__delete_README_row
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=1;   ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' của pr870-review-3-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr870-review-3-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó. | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI của t27: xoá hàng README khiến t27 đỏ 0/1; t26 và t138 không có răng đối với biến thể này.

### HƯỚNG 14 (pr870-review-3-codex__delete_receipt_caveat): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr870-review-3-codex__delete_receipt_caveat
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI riêng của hợp đồng t26/t27/t138; đây là giới hạn đã đo: xoá caveat khỏi receipt, cả ba vẫn xanh 1/1. Các chốt không có răng đối với caveat CHƯA ĐƯỢC KHAI; không coi cổng xanh là chứng minh đủ caveat. Finding cần sửa là thể hiện bị bỏ sót ở Hướng 13.

### HƯỚNG 14 (pr889-review-3-codex__delete_README_row): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr889-review-3-codex__delete_README_row
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=1;   ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' của pr889-review-3-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr889-review-3-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó. | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI của t27: xoá hàng README khiến t27 đỏ 0/1; t26 và t138 không có răng đối với biến thể này.

### HƯỚNG 14 (pr889-review-3-codex__delete_receipt_caveat): Đột biến caveat trên bản sao

Giả thuyết: mất cảnh báo tại một đầu có thể không bị chốt bắt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/caveat_mutations.py`; mỗi phiên bản gọi RIÊNG `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` trong `/tmp/pr896-r2-audit-b3269a02/copy`.

Output thật:
```text
MUTANT pr889-review-3-codex__delete_receipt_caveat
t26_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t138_ rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

Kết luận: KHÔNG PHẢI LỖI riêng của hợp đồng t26/t27/t138; đây là giới hạn đã đo: xoá caveat khỏi receipt, cả ba vẫn xanh 1/1. Các chốt không có răng đối với caveat CHƯA ĐƯỢC KHAI; không coi cổng xanh là chứng minh đủ caveat. Finding cần sửa là thể hiện bị bỏ sót ở Hướng 13.

### HƯỚNG 15: §10.2.2 — đọc nguồn Run/Checkout/Gate và giới hạn Workflow definition

Giả thuyết: nhãn measured chỉ trỏ một bản thuật lại, nguồn hoặc output không tồn tại/không khớp.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/land_audit.py` — đọc readback-run/jobs/artifacts, log, JSON/output thật; git rev-parse/show; sha256sum -c SHA256SUMS.txt trong ba provenance. Các nguồn nằm ở thư mục CHA của do-1026-*, không nhầm đường tương đối từ summary.

Output thật:
```text
PR #870; provenance=ops/land/pr870-claude-md-bai-hoc-c-provenance
ops/land/pr870-claude-md-bai-hoc-c-provenance/do-1026-5f288ea/bon-moc-10-2-2.txt: exists=True
ops/land/pr870-claude-md-bai-hoc-c-provenance/readback-run-39752735359.json: exists=True
ops/land/pr870-claude-md-bai-hoc-c-provenance/readback-jobs-39752735359.json: exists=True
ops/land/pr870-claude-md-bai-hoc-c-provenance/log-gate-119738461348-trich.txt: exists=True
ops/land/pr870-claude-md-bai-hoc-c-provenance/readback-artifacts-39752735359.json: exists=True
ops/land/pr870-claude-md-bai-hoc-c-provenance/artifact-12415205903/tl-selftest-Linux.json: exists=True
ops/land/pr870-claude-md-bai-hoc-c-provenance/artifact-12415205903/tl-selftest-Linux.out: exists=True
Run: {"id": 39752735359, "run_attempt": 1, "event": "push", "head_sha": "5f288eaf7dd217e9057d2f864dc15278bfd4e597", "conclusion": "success", "path": ".github/workflows/ci.yml"}; head_matches_git=True
Checkout: git.sha=5f288eaf7dd217e9057d2f864dc15278bfd4e597; tree=0fa694daf17e10c37fc3e61690531ade4bd528bf; parents=9e9a74b2a396ef458d25c51a5563efafbb45ba0c 06a50c5feea77c2654f31edd26efeed7eeee62f5; checkout_log_sha_present=True; gate.identity.head_match=True; tree_match=True; identity_after_equal=True
Job: {"id": 119738461348, "name": "gate (ubuntu-latest)", "conclusion": "success", "run_id": 39752735359, "head_sha": "5f288eaf7dd217e9057d2f864dc15278bfd4e597", "runner_id": 1000016456, "labels": ["ubuntu-latest"]}
Gate: status=pass; returncode=0; positive_verified=True; actual_positive_match='== tl selftest 1731/1731 ==\n'; matches_claimed_positive=True; command=['python', 'scripts/tl.py', '--selftest']; runtime={'system': 'Linux', 'machine': 'x86_64', 'python_version': '3.12.15'}
Output: sha256 actual=fff9645aa9d62ab43a5a9c1ee92e4c00540f699ae3fb16a1169941f99b86f8d5; receipt=fff9645aa9d62ab43a5a9c1ee92e4c00540f699ae3fb16a1169941f99b86f8d5; matches=True
Artifact: id=12415205903; digest=sha256:e6ad6f0d8e46f57abe24d3768a8d0e9ea9cb218061a88713b9294b4823ca37b9; workflow_run={"id": 39752735359, "repository_id": 1289195917, "head_repository_id": 1289195917, "head_branch": "master", "head_sha": "5f288eaf7dd217e9057d2f864dc15278bfd4e597"}; summary_has_digest=True; zip_preserved=False
Workflow definition: not_measured — GraphQL WorkflowRun.file tra 403 trong phien Claude Code tren web. Bang chung phu (blob ci.yml tai merge va hai cha) KHONG thay cho exact definition OID. Can chu kho chay `gh api graphql` ngoai phien va dan output.
supplement 5f288ea: blob=55d06ab452a060b836fdf6fa45ba3408fc44c90c; sha256=b65940388af27074eb36d9874563482d3aa41ddcd625b1f07bf512e0a28936a0; recorded_blob_present=True
supplement 5f288ea^1: blob=55d06ab452a060b836fdf6fa45ba3408fc44c90c; sha256=b65940388af27074eb36d9874563482d3aa41ddcd625b1f07bf512e0a28936a0; recorded_blob_present=True
supplement 5f288ea^2: blob=55d06ab452a060b836fdf6fa45ba3408fc44c90c; sha256=b65940388af27074eb36d9874563482d3aa41ddcd625b1f07bf512e0a28936a0; recorded_blob_present=True
sha256sum -c SHA256SUMS.txt: rc=0; OK=18; stderr=
landed=False; assurance_81=DAT
PR #889; provenance=ops/land/pr889-claude-md-bai-hoc-c-provenance
ops/land/pr889-claude-md-bai-hoc-c-provenance/do-1026-6ac385f/bon-moc-10-2-2.txt: exists=True
ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-run-39921552473.json: exists=True
ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-jobs-39921552473.json: exists=True
ops/land/pr889-claude-md-bai-hoc-c-provenance/log-gate-120319840559-trich.txt: exists=True
ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-artifacts-39921552473.json: exists=True
ops/land/pr889-claude-md-bai-hoc-c-provenance/artifact-12488609174/tl-selftest-Linux.json: exists=True
ops/land/pr889-claude-md-bai-hoc-c-provenance/artifact-12488609174/tl-selftest-Linux.out: exists=True
Run: {"id": 39921552473, "run_attempt": 1, "event": "push", "head_sha": "6ac385fdd7325f532ac4b4b6eb861292bfa7e970", "conclusion": "success", "path": ".github/workflows/ci.yml"}; head_matches_git=True
Checkout: git.sha=6ac385fdd7325f532ac4b4b6eb861292bfa7e970; tree=e64cdd92b27a66cbc4f0a91e0f84a4400b83c097; parents=daf89615efff9fde33039036ddf7f23ec9cb1c10 094e8d17ae4dfcf21dca63702c9262267bdc072c; checkout_log_sha_present=True; gate.identity.head_match=True; tree_match=True; identity_after_equal=True
Job: {"id": 120319840559, "name": "gate (ubuntu-latest)", "conclusion": "success", "run_id": 39921552473, "head_sha": "6ac385fdd7325f532ac4b4b6eb861292bfa7e970", "runner_id": 1000017936, "labels": ["ubuntu-latest"]}
Gate: status=pass; returncode=0; positive_verified=True; actual_positive_match='== tl selftest 1731/1731 ==\n'; matches_claimed_positive=True; command=['python', 'scripts/tl.py', '--selftest']; runtime={'system': 'Linux', 'machine': 'x86_64', 'python_version': '3.12.15'}
Output: sha256 actual=1bee4b7ad0128f67820f1e5053635543cd16304647d808efa891a1a0846d3ba6; receipt=1bee4b7ad0128f67820f1e5053635543cd16304647d808efa891a1a0846d3ba6; matches=True
Artifact: id=12488609174; digest=sha256:6334f7215ad4400247081ae9e1c4cf1e6ce24e8a3bf8bb9bdf2507e62f622ba9; workflow_run={"id": 39921552473, "repository_id": 1289195917, "head_repository_id": 1289195917, "head_branch": "master", "head_sha": "6ac385fdd7325f532ac4b4b6eb861292bfa7e970"}; summary_has_digest=True; zip_preserved=False
Workflow definition: not_measured — GraphQL WorkflowRun.file tra 403 trong phien Claude Code tren web. Bang chung phu (blob ci.yml tai merge va hai cha) KHONG thay cho exact definition OID. Can chu kho chay `gh api graphql` ngoai phien va dan output.
supplement 6ac385f: blob=f618cdb469016ac585724d286b498b7e1dcc80ea; sha256=b630260ce676292ced82da65f4cb54ec1dc0f66109901e7c1d61746d21baab06; recorded_blob_present=True
supplement 6ac385f^1: blob=f618cdb469016ac585724d286b498b7e1dcc80ea; sha256=b630260ce676292ced82da65f4cb54ec1dc0f66109901e7c1d61746d21baab06; recorded_blob_present=True
supplement 6ac385f^2: blob=f618cdb469016ac585724d286b498b7e1dcc80ea; sha256=b630260ce676292ced82da65f4cb54ec1dc0f66109901e7c1d61746d21baab06; recorded_blob_present=True
sha256sum -c SHA256SUMS.txt: rc=0; OK=21; stderr=
landed=False; assurance_81=DAT
PR #896; provenance=ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance
ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance/do-1026-27dcc3b/bon-moc-10-2-2.txt: exists=True
ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance/readback-run-39983914661.json: exists=True
ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance/readback-jobs-39983914661.json: exists=True
ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance/log-gate-120524600728-trich.txt: exists=True
ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance/readback-artifacts-39983914661.json: exists=True
ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance/artifact-12515154206/tl-selftest-Linux.json: exists=True
ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-provenance/artifact-12515154206/tl-selftest-Linux.out: exists=True
Run: {"id": 39983914661, "run_attempt": 1, "event": "push", "head_sha": "27dcc3bb67f6115608688a265bd8dcd3aa2a6ecc", "conclusion": "success", "path": ".github/workflows/ci.yml"}; head_matches_git=True
Checkout: git.sha=27dcc3bb67f6115608688a265bd8dcd3aa2a6ecc; tree=e3ddbe87b8c58b5c193d296a4eadcb7321e37bed; parents=b27c729dde77736f3509221b8a8622d0d92fe975 816f43988eb3012726120ad00166a989cc2b9af6; checkout_log_sha_present=True; gate.identity.head_match=True; tree_match=True; identity_after_equal=True
Job: {"id": 120524600728, "name": "gate (ubuntu-latest)", "conclusion": "success", "run_id": 39983914661, "head_sha": "27dcc3bb67f6115608688a265bd8dcd3aa2a6ecc", "runner_id": 1000018501, "labels": ["ubuntu-latest"]}
Gate: status=pass; returncode=0; positive_verified=True; actual_positive_match='== tl selftest 1731/1731 ==\n'; matches_claimed_positive=True; command=['python', 'scripts/tl.py', '--selftest']; runtime={'system': 'Linux', 'machine': 'x86_64', 'python_version': '3.12.15'}
Output: sha256 actual=d5e7ef8450cd6101d40ca2d4f7bde216ff4567b29cbb407826bf2940270ebb56; receipt=d5e7ef8450cd6101d40ca2d4f7bde216ff4567b29cbb407826bf2940270ebb56; matches=True
Artifact: id=12515154206; digest=sha256:b52c9765c5403eb58691fde04b7b3abe0e0ee0bf835a494b0b1066a3253d0464; workflow_run={"id": 39983914661, "repository_id": 1289195917, "head_repository_id": 1289195917, "head_branch": "master", "head_sha": "27dcc3bb67f6115608688a265bd8dcd3aa2a6ecc"}; summary_has_digest=True; zip_preserved=False
Workflow definition: not_measured — GraphQL WorkflowRun.file tra 403 trong phien Claude Code tren web; can chu kho chay `gh api graphql` ngoai phien va dan output.
supplement 27dcc3b: blob=f618cdb469016ac585724d286b498b7e1dcc80ea; sha256=b630260ce676292ced82da65f4cb54ec1dc0f66109901e7c1d61746d21baab06; recorded_blob_present=True
supplement 27dcc3b^1: blob=f618cdb469016ac585724d286b498b7e1dcc80ea; sha256=b630260ce676292ced82da65f4cb54ec1dc0f66109901e7c1d61746d21baab06; recorded_blob_present=True
supplement 27dcc3b^2: blob=f618cdb469016ac585724d286b498b7e1dcc80ea; sha256=b630260ce676292ced82da65f4cb54ec1dc0f66109901e7c1d61746d21baab06; recorded_blob_present=True
sha256sum -c SHA256SUMS.txt: rc=0; OK=25; stderr=
landed=False; assurance_81=CHUA DAT
```

Kết luận: KHÔNG PHẢI LỖI của ba mốc measured: nguồn có trong kho, cùng run/head/job/artifact, output hash và marker khớp. Workflow definition chưa đo và landed=false được khai đúng giới hạn. KHÔNG ĐO ĐƯỢC lại byte ZIP tải về vì ZIP không được lưu (summary đã nói zip KHONG kem); chỉ đối chiếu được digest REST đã lưu và bytes output/JSON đã giải nén. Không gọi mạng để lấp chỗ thiếu.

### HƯỚNG 16: Base, diff, log launcher và khối cap_nhat đối chiếu chéo

Giả thuyết: base đúng tên nhưng sai nội dung diff, commit không chỉ mang hiện vật, hoặc khối cập nhật chép sai receipt.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/git_artifacts_audit.py` — git diff/numstat/diff-tree/merge-base, SHA-256 log, đối chiếu từng trường YAML. Base là base của review, KHÔNG nhất thiết cha trực tiếp của head.

Output thật:
```text
pr870-review-3-codex: base_resolves=9e9a74b2a396ef458d25c51a5563efafbb45ba0c; base_prompt=True; base_is_ancestor rc=0; numstat_bytes_equal=True
diff.patch exact_git_bytes_equal=True; git_bytes=5195
stdout.log bytes actual/run=360/360; sha256_matches_run=True
stderr.log bytes actual/run=39/39; sha256_matches_run=True
checkpoint.json sha256_matches_run=True
pr889-review-3-codex: base_resolves=e63961f27b53e66db8e6600009f97d5706743063; base_prompt=True; base_is_ancestor rc=0; numstat_bytes_equal=True
diff.patch exact_git_bytes_equal=True; git_bytes=3138
stdout.log bytes actual/run=347/347; sha256_matches_run=True
stderr.log bytes actual/run=39/39; sha256_matches_run=True
checkpoint.json sha256_matches_run=True
pr915-review-1-codex: base_resolves=50a59a945026a2ab2f97dc0e7ef7b5a540e17652; base_prompt=True; base_is_ancestor rc=0; numstat_bytes_equal=True
omitted diff.patch declaration=14bfd8ec9bb561d2ed4b395acbf044cb573bf251b7b9a4190e109ea02b6bb592  1334705  diff.patch; git_diff_sha256=14bfd8ec9bb561d2ed4b395acbf044cb573bf251b7b9a4190e109ea02b6bb592; git_diff_bytes=1334705
stdout.log bytes actual/run=227/227; sha256_matches_run=True
stderr.log bytes actual/run=39/39; sha256_matches_run=True
checkpoint.json sha256_matches_run=True
3bc4244: file_count=1; paths_outside_reviews=['CLAUDE.md']
7cfe062: file_count=91; paths_outside_reviews=[]
2789cbb: file_count=4; paths_outside_reviews=[]
cc0a3c9: file_count=106; paths_outside_reviews=[]
cap_nhat #870: {"reviewed_sha": true, "verdict": true, "provider": true, "luot": true, "assurance": true, "so_lop_matches_receipt": true}
cap_nhat #889: {"reviewed_sha": true, "verdict": true, "provider": true, "luot": true, "assurance": true, "so_lop_matches_receipt": true}
cap_nhat #896: {"reviewed_sha": true, "verdict": true, "provider": true, "luot": true, "assurance": true, "so_lop_matches_receipt": true}
```

Kết luận: KHÔNG PHẢI LỖI của các mỏ neo và khối cập nhật; base khớp prompt và numstat, diff tái lập được kể cả tệp quá lớn đã bỏ khỏi kho.

### HƯỚNG 17: Hash cả hiện vật lịch sử liên quan

Giả thuyết: bản vá caveat đã đổi byte verdict/manifest của lượt trước.

Lệnh: `sha256sum -c SHA256SUMS` trong từng thư mục `ops/reviews/pr{870,889,896,915}-review-*-codex/`.

Output thật:
```text
pr870-review-1-codex: rc=0; OK=7; stderr=
pr870-review-2-codex: rc=0; OK=31; stderr=
pr870-review-3-codex: rc=0; OK=16; stderr=
pr889-review-1-codex: rc=0; OK=23; stderr=
pr889-review-2-codex: rc=0; OK=22; stderr=
pr889-review-3-codex: rc=0; OK=30; stderr=
pr896-review-1-codex: rc=0; OK=32; stderr=
pr915-review-1-codex: rc=0; OK=54; stderr=
```

Kết luận: KHÔNG PHẢI LỖI về hash: cả tám thư mục sạch.

### HƯỚNG 18: Kiểm HINT.patch trên bản sao và phản chứng cảnh báo mới

Giả thuyết: hint không áp bằng patch -p0, phá hash hoặc thêm caveat chưa được t27 bảo vệ.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/build_hint.py`. Hint chỉ sửa sidecar + một hàng README.

Output thật:
```text
patch --dry-run -p0 --fuzz=0: rc=0; 'checking file ops/reviews/pr889-review-1-codex-verdict.receipt.yaml\nchecking file ops/reviews/README.md\n'
patch -p0 --fuzz=0: rc=0; 'patching file ops/reviews/pr889-review-1-codex-verdict.receipt.yaml\npatching file ops/reviews/README.md\n'
patched t26_: rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
patched t27_: rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
patched t138_: rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
patched bien_nhan_v2: rc=0; 'bien_nhan_v2: 235 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 288\nTỔNG: ĐẠT'
patched, remove_new_README_row t27_: rc=1;   ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' của pr889-review-1-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr889-review-1-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó. | lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
copy changed_files=['ops/reviews/README.md', 'ops/reviews/pr889-review-1-codex-verdict.receipt.yaml']
preserved ops/reviews/pr889-review-1-codex-verdict.md=True
preserved ops/reviews/pr889-review-1-codex/VERDICT.md=True
preserved ops/reviews/pr889-review-1-codex/SHA256SUMS=True
```

Kết luận: KHÔNG PHẢI LỖI của hint. Đã thử trên bản sao, CHƯA áp trên cây thật; executor phải tự áp/tự đo. Tệp verdict lịch sử, băm, manifest và assurance giữ nguyên.

### HƯỚNG 19: Toàn vẹn cây nguồn cuối lượt và vế văn cũ

Giả thuyết: phép đo đã làm bẩn repo hoặc câu cũ vẫn sót ở chỗ khác trong CLAUDE.md.

Lệnh: băm lại toàn bộ tệp thường (gồm .git) + mode, so snapshot Hướng 1; các lệnh git/rg dưới đây.

Output thật:
```text
snapshot_before_files=7425; after_files=7425
added=[]; removed=[]; changed_content_or_mode=[]
$ git -C cay-kho rev-parse HEAD HEAD^{tree}; rc=0; output='8d56009a09af7b3ef93801df105f9483de212cc7\ne93305541ae7d7f87fa5c57dd610fa1be829b0f7\n'
$ git -C cay-kho status --short --untracked-files=all --ignored; rc=0; output=''
$ git -C cay-kho rev-parse --is-shallow-repository; rc=0; output='false\n'
$ git -C cay-kho diff --exit-code 3bc4244 8d56009 -- CLAUDE.md; rc=0; output=''
$ rg -n đọc ca ấy là đọc ma trận HIỆN HÀNH|đổi ma trận mà quên ca ấy cay-kho/CLAUDE.md; rc=1; output=''
```

Kết luận: KHÔNG PHẢI LỖI về toàn vẹn: không thêm/xoá/đổi nội dung hoặc mode của 7425 tệp thường so với snapshot Hướng 1; status kể cả ignored rỗng, HEAD/tree không đổi. Câu cũ không còn (rg rc=1). Mọi đột biến/hint chỉ ở bản sao ngoài cay-kho/.

## FINDING CÒN MỞ

### verdict-surface-bo-sot-pr889-luot1 [P1] Bản vá caveat bỏ sót verdict #889 lượt 1

TỆP/DÒNG:

- Câu sai: `ops/reviews/pr889-review-1-codex-verdict.md:7` và `ops/reviews/pr889-review-1-codex/VERDICT.md:7`.
- Nguồn phản chứng: `ops/reviews/pr889-review-1-codex/run/run.json:47`; `model_reviewer_identity.surface` trong `ops/reviews/pr889-review-1-codex-verdict.receipt.yaml`.
- Nơi bổ sung: `ops/reviews/pr889-review-1-codex-verdict.receipt.yaml:97` (`verdict_usage_caveats`) và `ops/reviews/README.md:697` (nhóm cảnh báo của lượt 1).

VẤN ĐỀ: Ở đúng `8d56009a09af7b3ef93801df105f9483de212cc7`, không chỉ hai lượt 2 và hai lượt 3 mang lời tự khai `codex_service`. Verdict #889 lượt 1 cũng ghi ở dòng 7 rằng phiên "không đi qua `codex exec` hay Desktop" và là `execution_surface: codex_service`. Nhưng run `9f946d714c2344fa9691c3d7d4f1b2d9` có `lenh.chuong_trinh=codex`, `execution_surface=codex_cli` (dòng 47); sidecar cũng ghi `surface: codex_cli`; header CLI có `OpenAI Codex v0.163.0`. Bản phẳng và bản trong thư mục trùng byte. Cả sidecar lượt 1 và nhóm cảnh báo của nó trong README đều thiếu caveat đính chính surface. Caveat của lượt 2/3 không đính chính được một verdict khác.

Quy tắc tại `ops/reviews/README.md:5` yêu cầu giữ byte verdict và đính chính trong sidecar + bảng cảnh báo; chính bản vá a9bc934 đang áp quy tắc ấy cho cùng lỗi ở bốn lượt khác. Đây là cùng lớp lỗi P1 cũ còn một thể hiện bị bỏ sót, không đếm lại bốn thể hiện đã được đính chính. Mức P1 theo định nghĩa chỉ thị: lời khai về sự thật đo được sai ngay tại SHA được review.

ĐÃ THỬ NGHIỆM: Hướng 13 chạy grep trên mọi `pr870*-verdict.md`/`pr889*-verdict.md`: 5 verdict có tự khai `codex_service`, chỉ 4 có caveat và hàng README; #889 lượt 1 có `receipt_caveat=False; README_surface_rows=[]`. Hướng 2–4 chạy nguyên CLI t26/t27/t138: từng ca rc=0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. Hướng 14 xoá caveat khỏi từng sidecar đang có: cả ba ca vẫn xanh; chỉ xoá hàng README trong khi giữ caveat mới làm t27 đỏ. Vì vậy cổng xanh không chứng minh đủ caveat ngữ nghĩa. Không yêu cầu đổi hợp đồng t27 thành bộ hiểu nghĩa mọi verdict.

GỢI Ý VÁ: `HINT.patch` thêm đúng caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE` vào sidecar lượt 1 và một hàng tương ứng trong README; nêu dòng 7, run 9f946d71, đính chính thành codex_cli, giữ nguyên byte/hash verdict và assurance lịch sử. Chỉ thử patch trên bản sao ngoài kho; không áp trên `cay-kho/`.

ĐỘ TIN: cao.

