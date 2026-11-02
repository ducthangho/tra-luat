verdict: changes_requested
reviewed_sha: 22382d8c800bed7b995d093cdcfdc206360d7fd4
Kết quả: 0 P0, 2 P1, 0 P2, 0 P3.

## KẾT LUẬN VỀ FINDING CŨ

- P1 `phu-nhan-ancestry-chi-tren-nhanh-da-cu`: **ĐÓNG MỘT PHẦN theo lớp**. Đúng **7/7 trường nêu ở lượt 5 đã đóng**: chín receipt khớp byte với kết quả áp hint; bảy trường có đúng commit ghi receipt và giữ đúng nội dung lịch sử; 14/14 phép đo ancestry tới master ghim và candidate đều rc0 (H2, H6). Quét ngoài danh sách tìm thêm **7 trường ở 5 receipt** còn nói chỉ trên nhánh/chưa vào master như hiện hành (H10). Ba receipt trong số đó là v1 đóng băng: cần supplementary caveat, không sửa byte.
- P1 `trang-thai-chua-review-da-bi-verdict-sau-bac`: **ĐÃ ĐÓNG**. PR870/PR889 lượt 1 đã neo lịch sử cả assurance, caveat và bốn hàng README. Hai mốc `600b6ce90d97d5f606272af137d7153b7b32133c` / `e02d0c31986f6ba5019fef21311a939f2d9c2f17` đúng commit thêm receipt; bốn verdict lượt 2/3 dẫn đúng exact SHA, `approve` 0/0/0/0, băm khớp (H6–H7).

Finding thứ hai của lượt này thuộc lớp surface: **3 verdict trong hồ sơ land** còn tự khai `codex_service`, trái nguồn CLI của chính lượt, chưa có đính chính (H11). Các thể hiện này có từ trước PR #947; nhiệm vụ yêu cầu kiểm cả lớp, không chỉ delta mới. Đếm theo lớp, không đếm mỗi trường/verdict thành một finding riêng.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Candidate và tree | 22382d8, cây đầy đủ | `git rev-parse HEAD HEAD^{tree}`; shallow=false; tree `2424259c815d962a485bbbc52751499ed93ace34` (H1) | Có |
| Hai commit từ lượt 5 | d308b0b chỉ hiện vật; 22382d8 ghi receipt + áp hint | `git diff-tree`, `git show -s --format=%P`: 99 path hiện vật riêng; d308b0b cha 1a276a1; candidate cha d308b0b (H2/H9) | Có |
| Patch/numstat giao kèm | cha→head và toàn PR→master | `audit.py history`: cả 4 tệp byte_match=True, tái sinh với core.quotepath=true (H2) | Có |
| Áp nguyên hint lượt 5 | 10 path, --fuzz=0 | Tái áp trên blob 1a276a1: rc0; 9/9 receipt khớp nguyên byte. README khác đúng 5 hàng bổ sung lượt 5, không thiếu/sửa dòng hint (H2) | Có về nội dung; không nói cả README bằng byte |
| Hiện vật lượt 5 | bản nguyên byte verdict/hint giao kèm | supplied verdict/hint bằng bản lưu; SHA256SUMS 97/97 OK (H2/H9) | Có |
| Bảy trường ancestry cũ | đã neo lịch sử | 7/7 scalar lịch sử khớp tại commit ghi receipt; 7/7 OID và 14/14 ancestry rc0 (H6) | Có |
| Mốc lịch sử mở rộng | commit ghi receipt/phép đo đúng | 48/48 mốc đúng commit thêm receipt; 148/148 phép đo ancestry ghi trong scalar/supplementary tái đo rc0 (H6) | Có về OID/phép đo; không coi paraphrase là bản sao byte |
| Hai trạng thái chưa review cũ | đã dẫn verdict sau | 4/4 verdict lượt 2/3 đúng SHA, header, approve, số finding và hash; chưa có tại hai mốc cũ (H7) | Có |
| Tám trạng thái đã vá trước lượt 5 | đã có mốc và verdict kế tiếp | 8/8 SHA/header/hash khớp, verdict sau vắng tại commit mốc (cat-file rc128) (H7) | Có |
| Lớp ancestry hết | phải quét mọi trường/receipt | 7 trường thuộc 5 receipt còn phủ nhận inclusion; 14 ancestry rc0, cả 5 receipt hiện diện trên master ghim (H10) | **Không — P1** |
| Surface trong ops/reviews | tự khai service phải có caveat | 25 tự khai service đều có đính chính/caveat; 17 cặp receipt/run so được không lệch (H8) | Không tìm thêm lỗi tại các thể hiện này |
| Surface ngoài ops/reviews | cùng lớp, không giới hạn danh sách cũ | #832 lượt 7, #848 lượt 1, #862 lượt 1: tự khai service trái run/receipt + transcript CLI (H11) | **Không — P1** |
| Mô tả finding không phải tự khai | phân biệt nguồn với người nói | #896 lượt 2–5, #915 lượt 1 chỉ trích service khi mô tả finding; không tính thành self claim (H8) | Có |
| Dữ liệu receipt lượt 5 | head/tree, 36 event/36 response ID, gpt-6.1-sol | `new_claims.py`: prompt hash, tree, run log hash/bytes, event count, evidence blob đều khớp (H9) | Có |
| README/land mới lượt 5 | đồng bộ receipt, hint áp cùng commit | 4/4 caveat đúng một hàng và nguyên mô tả; land đúng verdict/SHA/receipt; delta hint cùng 22382d8 (H2/H9) | Có |
| Byte verdict | không sửa hiện vật | 292 receipt; 294 verdict_path/hash chính/lồng khớp; 270 verdict phẳng có băm; 16 cặp phẳng/thư mục bằng byte; 0 verdict lịch sử bị sửa so master (H3) | Có |
| Ba verdict land vừa phát hiện | phải giữ nguyên byte | băm khớp SHA256SUMS; byte bằng cả master lẫn 1a276a1 (H11) | Có |
| YAML/ID caveat | parse được, ID không trùng trong receipt | 294 YAML parse bằng loader từ chối key trùng; errors=[]; 292 receipt không trùng ID (H3) | Có |
| Receipt v1 miễn trừ | byte bất biến | 11 ALLOWLIST_CUTOVER + 42 NO_DA_DO: 53/53 đúng băm và bằng byte master/1a276a1 (H3) | Có |
| t26 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| t27 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| t138 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| Xoá hàng mục lục/caveat README mới | ca nào đỏ | t27 rc1 0/1; t26/t138 rc0 1/1 ở cả hai đột biến (H5) | Chỉ t27 có răng |
| Xoá caveat mới khỏi receipt | ca nào đỏ | cả t26/t27/t138 rc0 1/1 (H5) | **Cả ba không có răng** |
| bien_nhan_v2 tại cay-kho | rc + kết luận | rc0; 239 v2, 11/11 legacy, 42 NỢ, 0 vi phạm/0 không đo, tổng292; TỔNG: ĐẠT (H4) | Đạt |
| land_evidence_nguon tại cay-kho | rc + kết luận | rc0; 47 ĐẠT, 26/28 miễn trừ, 0 vi phạm/0 không đo, tổng73; TỔNG: ĐẠT (H4) | Đạt |
| doctrine-scan tại cay-kho | rc + kết luận | rc0; sạch, 10 tệp, 0 chỗ chép doctrine (H4) | Đạt |
| doc-claims-check tại cay-kho | ok=true | rc0, stdout JSON parse được, `"ok": true`, `"strict": false` (H4) | Đạt |
| HINT mới | patch -p0 sạch trên candidate clone | 7 path; dry-run --fuzz=0 rc0, apply rc0; ba ca 1/1 và bốn cổng rc0, JSON ok=true (H12/H13) | Đã đo trên bản sao |
| Cây gốc cuối | chỉ đọc + đo | HEAD/tree không đổi; status kể cả ignored rỗng; clone hoàn nguyên sạch (H14) | Có |

## BẢNG SĂN

Lệnh đo Git và cổng chạy tại `cay-kho/`, các driver ở thư mục chứa PROMPT.md. Driver và subprocess kiểm tra đặt `PYTHONDONTWRITEBYTECODE=1`. Mọi đột biến nằm trên clone cục bộ từ mirror.git ngoài `cay-kho/`; chỉ đổi tài liệu/biên nhận. Không gọi mạng, push hay sửa cây được chấm. Log/JSON và nhật ký tăng dần ở `review_evidence/`.

### HƯỚNG 1: Định danh cây và lịch sử
- giả thuyết: sai candidate hoặc lịch sử shallow.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho status --porcelain=v1`; `git -C cay-kho log --oneline 1a276a1..HEAD`.
- output thật: HEAD `22382d8c800bed7b995d093cdcfdc206360d7fd4`; tree `2424259c815d962a485bbbc52751499ed93ace34`; shallow `false`; status rỗng; commit `d308b0b`, `22382d8`.
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 2: Tái dẫn xuất hint lượt 5 theo byte
- giả thuyết: hint bị áp thiếu/thừa hoặc lời giao sai delta.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history` (rc0). Lấy 10 blob ở 1a276a1 vào thư mục tạm, áp `patch --batch --fuzz=0 -p0`, so từng byte với candidate; diff README sau áp với candidate.
- output thật, trích `direction-2.log`:
```text
diff.patch: byte_match=True
numstat.txt: byte_match=True
diff-pr947.patch: byte_match=True
numstat-pr947.txt: byte_match=True
hint_paths=10 apply_rc=0
byte_for_byte_matches=9/10
README delta beyond hint: 5 added/removed lines
outside_hint_non_artifact=['ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml', 'ops/reviews/README.md']
d308b0b_paths=99 only_round5_artifacts=True
verdict-cu/pr896-review-5-codex-VERDICT.md: stored_byte_match=True
verdict-cu/pr896-review-5-codex-HINT.patch: stored_byte_match=True
```
- kết luận: KHÔNG PHẢI LỖI. Chín receipt khớp cả tệp. Năm dòng README đều là **thêm**: bốn hàng caveat và một hàng mục lục lượt 5; bốn hàng PR870/PR889 do hint sửa khớp byte. `hint-readme-extra.diff` giữ đầy đủ delta. Git quote tên Unicode được giữ như bản patch giao kèm khi so bốn tệp, không nhầm khác định dạng với sai dữ liệu.

### HƯỚNG 3: Toàn vẹn verdict, YAML và v1
- giả thuyết: sửa hiện vật hoặc receipt đóng băng, YAML/ID hỏng.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity` (rc0); đọc cả Assign và AnnAssign của hai allowlist từ AST, băm byte thật và so blob ở master/1a276a1.
- output thật, trích `direction-3.log`:
```text
yaml_parsed=294 receipts=292
verdict_path_hashes=294 all_match=True
flat_verdict_files=270 unclaimed=[]
flat_directory_pairs=16 all_match=True
frozen_groups={'ALLOWLIST_CUTOVER': 11, 'NO_DA_DO': 42} all_hash_and_byte_match=True
modified_historical_verdicts=[]
errors=[]
```
- kết luận: KHÔNG PHẢI LỖI. `integrity.json` có từng đường dẫn/hash và kết quả so byte. Loader từ chối key YAML trùng; kiểm ID caveat riêng theo receipt.

### HƯỚNG 4: Các ca và cổng bắt buộc tại cây gốc
- giả thuyết: xanh do bỏ ca, N/N lệch hoặc gate không thực chạy.
- lệnh: `python3 review_evidence/run_checks.py` (rc0), phóng riêng từng command dưới đây với cwd `cay-kho/`.
- output thật:

| command | rc | dòng kết luận / JSON |
|---|---|---|
| `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 |
| `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 |
| `python3 ops/lease_publish_test.py --chi-ca=t138_` | 0 | lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | bien_nhan_v2: 239 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 292; TỔNG: ĐẠT |
| `python3 ops/land_evidence_nguon.py --root .` | 0 | land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73; TỔNG: ĐẠT |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | {"ok": true, "strict": false} |

- kết luận: KHÔNG PHẢI LỖI của các cổng. Ba ca đều N/N=1/1, chạy=1, skip=0. Test stderr có SyntaxWarning escape, không gặp `Codex home is inside a repository`. Log `.stdout/.stderr/.rc` và `checks.json` giữ output đầy đủ. Cổng xanh không chứng minh prose đúng.

### HƯỚNG 5: Đột biến hàng và caveat mới
- giả thuyết: các ca sẵn có phát hiện việc mất hàng/caveat lượt 5.
- lệnh: `git clone --no-hardlinks --no-checkout <mirror.git> /tmp/pr896-r6-mutations-bwmr16mi/copy`; `git -C <copy> checkout --detach 22382d8c800bed7b995d093cdcfdc206360d7fd4`; `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/mutations.py` (rc0). Hoàn nguyên giữa từng đột biến.
- output thật từ `mutations.json` và các log:

| đột biến | t26 | t27 | t138 |
|---|---|---|---|
| Xoá hàng mục lục pr896-review-5, 736 byte | rc0 1/1 | **rc1 0/1** | rc0 1/1 |
| Xoá hàng caveat README HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO, 366 byte | rc0 1/1 | **rc1 0/1** | rc0 1/1 |
| Xoá caveat ấy khỏi receipt, 362 byte, YAML vẫn hợp lệ | rc0 1/1 | rc0 1/1 | rc0 1/1 |

- output lỗi thật t27: `verdict 'pr896-review-5-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict'`; đột biến thứ hai báo `caveat 'HINT-LUOT5-AP-CUNG-COMMIT-GHI-SO' ... KHÔNG nằm ở CỘT 'id' trên cùng hàng ...`. Mọi invocation đều chạy=1, skip=0; status sau hoàn nguyên rỗng.
- kết luận: KHÔNG PHẢI LỖI hiện hành trong phạm vi hai lớp được giao; **t26/t138 không có răng với hai hàng README**, t27 có răng. **Cả ba không có răng với việc xoá caveat khỏi receipt.** Không nhận cổng xanh thành bằng chứng caveat đầy đủ.

### HƯỚNG 6: Mốc lịch sử và OID ancestry
- giả thuyết: câu đã neo nhưng neo sai commit receipt hoặc sai phép đo.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py ancestry` (rc0); với từng trường đọc `git show <anchor>:<receipt>`, `git log --diff-filter=A <candidate> -- <receipt>`, chạy `git merge-base --is-ancestor <OID> <target>`.
- output thật: `historical_fields=48`, `receipt_added_at_anchor=48`; `ancestry_measurements=148 all_rc0=True`. Bảy trường mới của lượt 5: `same_historical_scalar=True`, `receipt_introduced_at_anchor=True` cho **7/7**. Dữ liệu cụ thể trích `states-ancestry.json`:

| receipt/trường | commit ghi receipt | OID được đo | rc(master,candidate) |
|---|---|---|---|
| ci-windows-review-5-claude-verdict.receipt.yaml / chuoi_verdict_ghi_chu | `e32c5643111e001dc0c655c568b445c897ade450` | `c2f68987b3f298de12b84cf29a934c7b844c8558` | 0,0 |
| doctrine-scan-review-1-claude-verdict.receipt.yaml / anchor.gioi_han | `86169c00beff045b0faed63e39d1a67b9acd1fc1` | `bc5d0c6e4d3d5b3cc5d6f8c08ba1c005dd9bdadc` | 0,0 |
| doctrine-scan-review-2-claude-verdict.receipt.yaml / anchor.gioi_han | `de0ecd0f912bb131b63ada866672af00129eefd0` | `80d816130fda69af75dc1d9ae76f3fc83b837773` | 0,0 |
| doctrine-scan-review-3-claude-verdict.receipt.yaml / anchor.gioi_han | `6d59a4394f0e51ace4e02c8f4be13cb649e6871e` | `7d8bb69ac02b54075d63a9915e12e6d2bf28b513` | 0,0 |
| wp538-review-1-claude-verdict.receipt.yaml / anchor.gioi_han | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` | 0,0 |
| wp538-review-2-claude-verdict.receipt.yaml / anchor.gioi_han | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` | 0,0 |
| wp540-review-1-claude-verdict.receipt.yaml / anchor.gioi_han | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` | 0,0 |

- kết luận: KHÔNG PHẢI LỖI ở bảy trường đã sửa. So rộng 48 scalar lịch sử có 35 scalar bằng nguyên văn ở bản đầu; các phần diễn giải còn lại không được coi là trích nguyên byte: pr508 caveat được thêm sau, ý ancestry có ở anchor cũ; 12 trường wp678 thay diễn đạt/độ chính xác giờ push. Chỉ xác nhận 48 OID đều là commit thêm receipt và 148 phép đo ancestry đều đúng; không chứng thực giờ push từ lịch sử Git. Không báo sự khác diễn đạt này thành finding thuộc hai lớp được giao. Bảy scalar mà hint lượt 5 sửa khớp đúng bản lịch sử.

### HƯỚNG 7: Verdict kế tiếp và trạng thái chưa review
- giả thuyết: dẫn sai SHA/hash/verdict hoặc mốc lịch sử đặt sau lần review.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews` (rc0); đọc header và receipt, sha256 byte thật; `git cat-file -e <anchor>:<next-verdict>`.
- output thật: `old_eight_count=8`; cả tám có receipt_sha_match, verdict_header_sha_match, hash_match=true, next_absent_at_anchor_rc=128. Bốn review mới được dẫn:

| verdict | reviewed_sha | sha256 | kết quả |
|---|---|---|---|
| pr870-review-2-codex-verdict.md | `06a50c5feea77c2654f31edd26efeed7eeee62f5` | `8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6` | approve 0/0/0/0 |
| pr870-review-3-codex-verdict.md | `06a50c5feea77c2654f31edd26efeed7eeee62f5` | `0021b5b2f90e0da39a92c11041c3236980acfbbd0b22f46d0044ac8334f16e81` | approve 0/0/0/0 |
| pr889-review-2-codex-verdict.md | `094e8d17ae4dfcf21dca63702c9262267bdc072c` | `c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612` | approve 0/0/0/0 |
| pr889-review-3-codex-verdict.md | `094e8d17ae4dfcf21dca63702c9262267bdc072c` | `c05bc41d9232d99a9e0c49199e022a9a64b01227674144da73bf50b9b7ce445f` | approve 0/0/0/0 |

- output thật: cả bốn `receipt_sha_match=true`, `verdict_header_sha_match=true`, `hash_match=true`, `next_absent_at_anchor_rc=128`. `states-reviews.json` giữ toàn bộ 12 entry.
- kết luận: KHÔNG PHẢI LỖI; finding chưa review lượt 5 đã đóng. Không biến verdict lượt 1 thành approve hay nâng assurance. Các câu chưa review khác về `5a96c1a`/`888c0d9` không có receipt ops/reviews nào chấm đúng hai head ấy; không gán review của head trước cho head sau.

### HƯỚNG 8: Surface trong sổ review
- giả thuyết: còn tự khai surface trái receipt/run chưa được caveat.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/surfaces.py` (rc0); `rg -n -i 'codex.service|service/api|execution.surface|surface:' cay-kho/ops/reviews --glob '*-verdict.md' --glob 'VERDICT.md'`.
- output thật, trích `direction-8.log`:
```text
verdict_files_repo_wide=413 distinct_content=396
run_json_files=48 parse_errors=[]
receipt_runtime_pairs=17 mismatches=[]
service_self_claim_files=25 missing_correction=[]
other_identity_mentions=71 unknown_distinct_verdicts_with_surface=62
```
- kết luận: KHÔNG PHẢI LỖI mới trong 25 tự khai của receipt ops/reviews đã kiểm. 15 caveat thiếu runtime (kể cả slice-b-c supplementary) có đúng hàng/mô tả; sáu trường hợp có run đã đính chính; bốn ci-g5 có cảnh báo thiếu runtime. Không tự chọn surface cho nguồn vắng. Nhắc service trong finding không phải self claim; API/shell chung không loại trừ CLI. Các verdict ngoài inventory receipt được kiểm tiếp ở H11, không kết luận hết lớp từ 25 tệp này.

### HƯỚNG 9: Lời khai mới của commit 22382d8
- giả thuyết: chính receipt/README/land mới ghi sai mốc hint hoặc nguồn runtime.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/new_claims.py` (rc0); `sha256sum -c SHA256SUMS` tại thư mục hiện vật lượt 5; so blob evidence URL bằng Git.
- output thật: verdict `36138` byte, sha256 `968ebc3859538e79b53bd9ead8e3c9464a0db8c8e83e62a4b7ac7437f0480e9e`, matches=true; run `453628b5eeef497eb4505bed3c8247ec`, head=1a276a1, ma_thoat=0, worktree_sach=true, thoi_luong=1036.087; model_events count=36, response_ids=36, models=[gpt-6.1-sol]. prompt/tree/stdout/stderr/evidence hash checks đều true. Receipt addition commit=22382d8; evidence commit=d308b0b. SHA256SUMS rc0, ok_count=97, failed=[], stderr rỗng. Bốn caveat mới đều rows=1, exact_description=true; land_round5_sha_and_receipt_match=true.
- kết luận: KHÔNG PHẢI LỖI ở các lời khai mới này. `finding_moi`, kết luận finding cũ và hàng mục lục mô tả kết quả trên **1a276a1**, không phải lời tự khai surface hay khẳng định tất cả receipt còn sai sau áp hint. PR #947 chưa là ancestor master: 1a276a1/d308b0b→master ghim rc1; hướng hiện tại không tự chứng minh landed.

### HƯỚNG 10: Quét rộng trạng thái ngoài danh sách lượt 5
- giả thuyết: vá đúng trường được chỉ tên nhưng còn cùng lớp ở receipt khác.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/inventory.py`; `... negative_ancestry.py`; `... residuals.py` (đều rc0); quét scalar YAML và README; `git merge-base --is-ancestor <OID> <master/candidate>`; `git ls-tree <master> -- <receipt>`.
- output thật: quét 294 YAML; bộ lọc trạng thái cho 179 ứng viên chưa có mốc trong scalar, 149 ứng viên có mốc, 119 hàng README (đây là số regex hit, **không phải finding count**). `residual-status.json` có bảy trường sau:

| receipt : dòng | trường còn sai | OID | rc(master,candidate) |
|---|---|---|---|
| doctor-github-mcp-review-6-codex-verdict.receipt.yaml:146 | receipt_khong_khai.0 | `4920113a639d81385c0f98b1488c0f497776d2ff` | 0,0 |
| don-nhanh-base-review-4-claude-verdict.receipt.yaml:60 | truy_xuat_ghi_chu | `03f12ac63284dd814dcf14664968af4872ef7f8a` | 0,0 |
| don-nhanh-base-review-5-claude-verdict.receipt.yaml:73 | truy_xuat_ghi_chu | `03f12ac63284dd814dcf14664968af4872ef7f8a` | 0,0 |
| wp461-review-1-codex-verdict.receipt.yaml:101 | anchor.cuong_do | `ef72264cb268643a89df3e15cf6cb840da92307b` | 0,0 |
| wp461-review-1-codex-verdict.receipt.yaml:472 | lich_su_ban_ung_vien.ghi_chu | `ef72264cb268643a89df3e15cf6cb840da92307b` | 0,0 |
| wp523-r15-review-1-codex-verdict.receipt.yaml:88 | anchor.cuong_do | `b2134a40243e5cb3ea6d64eaf49a4c9f26794cbc` | 0,0 |
| wp523-r15-review-1-codex-verdict.receipt.yaml:357 | lich_su_ban_ung_vien.ghi_chu | `b2134a40243e5cb3ea6d64eaf49a4c9f26794cbc` | 0,0 |

- output thật: `git ls-tree` master trả blob `9f62f975…` (doctor6), `249b9998…` (don4), `52ab3cd9…` (don5), `2c45c070…` (wp461), `fa390998…` (wp523). Không có supplementary entry cho năm receipt này. Các OID 4bc9432/604b8d9 vẫn rc1 tới master và candidate; các caveat không-ancestor tương ứng không bị báo oan. Các câu thiếu quyết định land, finding lịch sử, quan hệ tới master cũ được ghim, và điều kiện squash/fast-forward không bị đồng nhất thành phủ nhận merge hiện hành.
- kết luận: **LỖI P1** `phu-nhan-ancestry-chi-tren-nhanh-da-cu`; lớp còn bảy trường trong năm receipt.

### HƯỚNG 11: Surface trong provenance land, ghép đúng lượt
- giả thuyết: giới hạn quét ops/reviews và tên literal run.json bỏ lọt self claim khác nguồn.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/runtime_index.py`; `... land_surfaces.py` (rc0); đọc verdict/JSON/transcript/land.review; so SHA256SUMS và byte Git ở master/1a276a1.
- output thật: `runtime_records=120` khi tính cả run-*.json (có bản sao/snapshot, không gọi là 120 run độc lập). Ba đối chiếu:

| verdict tự khai codex_service | nguồn của đúng lượt | output thật |
|---|---|---|
| pr832-wp831-provenance/verdict-luot7/wp831-g1-luot7-codex-verdict.md:6 | verdict-luot7/run.json:82 | run 1ff81cba41874a218b53275d3cdc1418; head 51ae5c095972611d2c6045bd81786a4fc7e9ca62; execution_surface=codex_cli; lenh.chuong_trinh=codex |
| pr848-wp744-provenance/verdicts/wp744-g3-luot1-codex-verdict.md:36 | verdicts/run-f65e544e.json:82 | run f65e544ef5d64ba7a1e0edb607edcf0a; head 23bc189f28ea60f04ca1634b6fe66d02babf12ed; execution_surface=codex_cli; lenh.chuong_trinh=codex |
| pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-verdict.md:3 | transcript của lượt1:1 và land-evidence.yaml:128 | OpenAI Codex v0.163.0; session 01a157da-2170-7be2-b6d0-053fa8f91aec; receipt review.luot_1.reviewer ghi codex exec trực tiếp |

- output thật về byte/hash, đều same_master=True, same_prev=True và khớp SHA256SUMS:

- `wp831-g1-luot7-codex-verdict.md`: 17277 byte, sha256 `1e27ba6bf2c4690a470b7786fe799c850b5924352a85a24460fb5053ff216d28`.

- `wp744-g3-luot1-codex-verdict.md`: 18706 byte, sha256 `af2b5fa426a7d53755148f4f9711712246afadc91e1d75e5267f8c8023bc3911`.

- `wp748-r21-luot1-codex-verdict.md`: 14181 byte, sha256 `95438373ee2f04a8431e6b10cfd2111144f9744bc54ac114c5670e0652e1ce87`.

- kết luận: **LỖI P1** `surface-service-cli-trong-ho-so-land`. Không tìm được caveat/đính chính surface cho ba verdict ấy trong hồ sơ tương ứng. Với #862 **không mượn run-f0909b38 của lượt 2** dù cùng SHA; nguồn chứng minh lượt 1 là transcript và trường luot_1 của receipt land. #849 lượt 4/5 đã có đính chính rõ `LOI TU PHAN LOAI ... tin dau tep` nên không báo lỗi; run-03c4f6be thuộc lượt 6, không dùng làm nguồn lượt 4/5. #823 lượt 5 và #877 lượt 2 không có nguồn runtime đối nghịch đủ để phân xử, nên không tự chọn surface hoặc báo finding chỉ từ tên gọi.

### HƯỚNG 12: Hint trên clone tại candidate
- giả thuyết: gợi ý vá sửa v1/verdict hoặc không áp được trên exact SHA.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py` (rc0); `patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>` tại clone sạch ở 22382d8, rồi áp thật trên clone.
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
```
- kết luận: KHÔNG PHẢI LỖI của hint. Ba v1 dùng sidecar supplementary + ba hàng README. Hai v2 neo các scalar cũ bằng đúng blob commit có thể đọc lại, ghi đo mới. Ba receipt land thêm đính chính của từng verdict, không đổi provenance/verdict. Đây là **gợi ý, chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

### HƯỚNG 13: Cổng sau áp hint trên bản sao
- giả thuyết: hint làm hỏng cổng hoặc hiện vật băm.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/hint_checks.py` (rc0), chạy cùng ba ca riêng và bốn cổng có sẵn ở clone.
- output thật, trích `hint-validation/checks.json`:

- t26: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0

- t27: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0

- t138: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0

- bien_nhan_v2: rc0; bien_nhan_v2: 239 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 292; TỔNG: ĐẠT

- land: rc0; land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73; TỔNG: ĐẠT

- doctrine: rc0; doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine

- doc_claims: rc0; True

- output thật bổ sung: `Unique-key YAML parse passed; caveat IDs unique; all review verdict bytes and all v1 receipt bytes unchanged; three land verdict hashes unchanged.`
- kết luận: KHÔNG PHẢI LỖI của hint theo các phép đo này. Không suy cổng kiểm đủ mọi câu văn hay thay đổi verdict trên SHA thật.

### HƯỚNG 14: Kiểm cây gốc và hoàn nguyên clone
- giả thuyết: quá trình đo để lại thay đổi ngoài phạm vi.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored`; cùng lệnh trên clone sau hoàn nguyên đúng bảy path hint.
- output thật từ `final-state.json`: original và copy_restored cùng HEAD `22382d8c800bed7b995d093cdcfdc206360d7fd4`, tree `2424259c815d962a485bbbc52751499ed93ace34`; mọi rc0, status_with_ignored.output="".
- kết luận: KHÔNG PHẢI LỖI. `cay-kho/` giữ nguyên, clone đã phục hồi sạch.

### phu-nhan-ancestry-chi-tren-nhanh-da-cu [P1] Còn bảy trường ở năm receipt phủ nhận inclusion đã có

TỆP/DÒNG:

- `ops/reviews/doctor-github-mcp-review-6-codex-verdict.receipt.yaml:146`, `receipt_khong_khai[0]`: commit "hiện chỉ được giữ bởi nhánh ops/**".
- `ops/reviews/don-nhanh-base-review-4-claude-verdict.receipt.yaml:60`, `truy_xuat_ghi_chu`: "chỉ tồn tại trên nhánh", "KHÔNG nằm trong lịch sử master".
- `ops/reviews/don-nhanh-base-review-5-claude-verdict.receipt.yaml:73`, cùng trường: "chỉ sống trên nhánh", "KHÔNG trong lịch sử master".
- `ops/reviews/wp461-review-1-codex-verdict.receipt.yaml:101`, `anchor.cuong_do`: "candidate ancestry only; canonical inclusion pending", đường land "đang chờ"; dòng 472, `lich_su_ban_ung_vien.ghi_chu`: "Receipt CHUA duoc giao (chua o master)".
- `ops/reviews/wp523-r15-review-1-codex-verdict.receipt.yaml:88`, `anchor.cuong_do`: cùng "canonical inclusion pending", chỉ ở tổ tiên PR #623; dòng 357: "Receipt nay CHUA duoc giao (chua o master ... rong)".

VẤN ĐỀ: Đây là các scalar phát biểu hiện hành, không có mốc lịch sử cho câu phủ định. 4920113a, 03f12ac, ef72264c và b2134a40 đều đã là tổ tiên của master ghim 3e973a0 và candidate; năm receipt cũng có blob trên master. Doctor6 đã sửa đúng các trường `evidence_url_han_che`/`truy_xuat_*`, nhưng đoạn "hiện chỉ" còn mâu thuẫn với chính chúng; con trỏ sang trường đúng không làm câu ấy thành lịch sử. Ba v1 không có supplementary đính chính tương ứng. Như bảy trường lượt 5, sửa một trường không đóng được cùng lớp ở trường khác. Điều này làm người đọc tiếp tục coi nguồn đã có trên master là nguồn chỉ sống nhờ nhánh hoặc receipt chưa được giao. Không dùng kết quả này để khẳng định Packet landed hay nâng assurance.

ĐÃ THỬ NGHIỆM: H10, `residuals.py` rc0: bảy trường × hai target = **14/14 rc0** cho `git merge-base --is-ancestor`; `git ls-tree 3e973a0 -- <receipt>` trả blob cho **5/5**. JSON có full OID, từng field/dòng và scalar nguyên văn. H3 chứng minh ba v1 nằm trong allowlist đóng băng; hint dùng supplementary cho chúng, không đổi byte.

ĐỘ TIN: cao.

### surface-service-cli-trong-ho-so-land [P1] Ba verdict ngoài sổ review tự khai service trái nguồn CLI

TỆP/DÒNG:

- `ops/land/pr832-wp831-provenance/verdict-luot7/wp831-g1-luot7-codex-verdict.md:6`; nguồn cùng lượt `verdict-luot7/run.json:82`, ID `1ff81cba41874a218b53275d3cdc1418`.
- `ops/land/pr848-wp744-provenance/verdicts/wp744-g3-luot1-codex-verdict.md:36`; nguồn `verdicts/run-f65e544e.json:82`, ID `f65e544ef5d64ba7a1e0edb607edcf0a`.
- `ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-verdict.md:3`; nguồn transcript lượt 1 dòng 1/10 và `ops/land/pr862-wp748-r21-land-evidence.yaml:128` (`review.luot_1.reviewer`).

VẤN ĐỀ: Cả ba đoạn là lời tự khai identity của reviewer, không phải trích finding. Hai run đầu ghi `execution_surface=codex_cli`, `lenh.chuong_trinh=codex` và đúng head của verdict. Lượt 1 #862 có header CLI và receipt land ghi `codex exec` trực tiếp. Không có caveat/đính chính nối lời tự khai `codex_service` với nguồn CLI của chính lượt. Cảnh báo model không đo được hoặc thiếu assurance không đính chính surface. Quét 25 tự khai trong ops/reviews không bao phủ các verdict trong provenance land, nên lớp chưa hết.

ĐÃ THỬ NGHIỆM: H11, `runtime_index.py`/`land_surfaces.py` rc0; kiểm full head/run ID, header, trường review đúng lượt, hash SHA256SUMS và byte Git. Ba băm/byte không đổi so master và 1a276a1. Không dùng run lượt 2 để phân xử lượt 1 #862, không báo #849 đã có đính chính. Hint thêm caveat ở ba land-evidence tương ứng, giữ nguyên verdict.

ĐỘ TIN: cao.

Giới hạn: chỉ xác minh hiện vật và Git tại reviewed_sha được giao. Không chứng nhận trạng thái GitHub hiện hành, model/session bị lược khỏi kho, quyết định land hoặc quyền merge. Các chốt xanh có giới hạn răng đã đo ở H5. HINT.patch đã kiểm sạch trên bản sao; chưa áp vào cay-kho/.
