verdict: changes_requested
reviewed_sha: 05bc12e2b9008071ca28edbd4574e58644d48220
Kết quả: 0 P0, 2 P1, 1 P2, 0 P3.

## KẾT LUẬN VỀ FINDING CŨ

- P1 `phu-nhan-ancestry-chi-tren-nhanh-da-cu`: **ĐÃ ĐÓNG** ở 7/7 trường của 5 receipt nêu lượt 6. Bốn scalar v2 giữ đúng lời khai trong commit `77f272d435b0c23369b2348efa821c760d653036` / `62c2fceecac4d3e114f0ecfcb0980dc67514e0ee`; ba v1 giữ nguyên byte và có đúng supplementary caveat + hàng README. Mọi phép đo ancestry trong các đính chính tái chạy rc0 (H2, H3, H6). Quét lớp rộng hơn còn P1 về câu **PR #490 chưa merge** trong land evidence #491 (H15); không nhập phát hiện mới này vào bảy trường đã sửa.
- P1 `surface-service-cli-trong-ho-so-land`: **ĐÃ ĐÓNG** ở cả 3 verdict #832/#848/#862. Caveat đúng đường dẫn, dòng, hash và nguồn của chính lượt; #862 lượt 1 dùng transcript + land.review.luot_1, không mượn run lượt 2. Verdict không đổi byte (H11). Lớp khai surface còn **P2** ở #823 lượt 5 và #877 lượt 2: hai lời khai trái hồ sơ nhưng không có runtime gốc để chọn bên nào đúng (H12).

Lời khai mới do `05bc12e` thêm cũng được đối chiếu: mô tả `VERDICT.partial.md` của lần hỏng c0fa33fa sai nội dung hiện vật (P1, H16). Đây là kiểm lời giao mới; phần săn mở rộng trạng thái/surface vẫn phân biệt câu hiện hành, bản ghi lịch sử và lời trích khi mô tả finding.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Candidate/tree/master ghim | `05bc12e`, master `3e973a0`, đầy đủ | `git rev-parse`, `--is-shallow-repository`, status; tree `3412a314b129d1ee1473e528a5ec438378ccebe5`, shallow=false, sạch (H1/H17) | Có |
| Hai commit kể từ lượt 6 | `825dab1` chỉ hiện vật; `05bc12e` ghi sổ + áp hint | `git diff-tree`: 122 path của 825dab1 đều là hiện vật lượt 6; cha 825dab1=22382d8, cha 05bc12e=825dab1 (H2/H9) | Có |
| Bốn tệp diff/numstat giao kèm | đúng phạm vi delta và toàn PR | Tái sinh bằng `git -c core.quotepath=true diff`; 4/4 bằng byte (H2) | Có |
| Áp nguyên hint lượt 6 | 7 tệp, fuzz=0 | Tái áp trên blob 22382d8: rc0, 6/7 tệp bằng nguyên byte; README khác đúng 6 hàng **thêm**, gồm 5 caveat + 1 mục lục mới (H2) | Có về nội dung; README không bằng cả tệp |
| Bản verdict/hint lượt 6 | bản lưu nguyên byte | So với verdict-cu; cả hai bằng byte, SHA256SUMS 120/120 OK (H2/H9) | Có |
| Bốn trường v2 được neo | đúng commit và lời khai cũ | `git show <anchor>:<receipt>` và `git log -1`; 4/4 text + anchor khớp (H6) | Có |
| Ba v1 cần supplementary | giữ byte, đủ caveat/README | 3/3 băm, blob mốc, một hàng README và nguyên mô tả khớp (H6) | Có |
| Mốc và ancestry cũ/mới | đính chính đúng quan hệ Git | 48/48 mốc cũ là commit thêm receipt; 176/176 phép ancestry ghi trong các scalar/supplementary rc0 (H6) | Có |
| Đính chính surface land cũ | #832 lượt 7, #848 g3 lượt 1, #862 r21 lượt 1 | Băm/byte và đúng nguồn cùng lượt đều khớp (H11) | Có |
| Trạng thái chưa review đã sửa trước lượt 6 | dẫn verdict sau đúng head | 12/12 đối chiếu header, receipt SHA, băm khớp; verdict sau chưa tồn tại tại mốc cũ (H7) | Có |
| Surface ops/reviews | self-claim khác receipt phải được cảnh báo | 25 tự khai service có caveat/đính chính; 18 cặp receipt/run so được không lệch (H8) | Không tìm thêm lỗi ở các cặp này |
| Surface mở rộng land | các tự khai còn lại phải nhất quán hoặc có caveat | #823: service đối lập sổ 5 lượt CLI; #877: service đối lập lời hồ sơ về header CLI; cả hai thiếu caveat surface, không có run đúng head (H12) | **Không — P2** |
| Trạng thái PR #490 trong land #491 | `PR #479 và #490 chưa merge` | `git show 8cee941`, `merge-base --is-ancestor` tới master/candidate đều rc0, tới mốc cũ cdd0b1d rc1 (H15) | **Không — P1** |
| Lần chạy hỏng c0fa33fa | cùng head/prompt, rc1, 349.795s | Hai run.json khớp head/prompt; có trích lỗi server_overloaded lưu kèm (H16) | Có theo nguồn lưu |
| Nội dung partial của lần hỏng | chỉ dang_lam + một phép đo t26 | `wc -c`, `rg '^### '`: **28.214 byte, 14 mục**, gồm t27, t138, 4 cổng, Git và đột biến (H16) | **Không — P1** |
| Byte verdict trong sổ và caveat | không sửa hiện vật | 301 cặp verdict_path/verdict_sha256 đúng; 271 verdict phẳng có băm; 17 cặp phẳng/thư mục bằng byte; 137 entry manifest verdict đúng; không sửa verdict lịch sử so master (H3/H17) | Có |
| YAML/ID caveat | parse được, không trùng ID trong receipt | 368 YAML parse bằng loader từ chối key trùng; errors=[]; không trùng caveat ID trong từng receipt (H3) | Có |
| V1 miễn trừ băm | byte đóng băng | 11 ALLOWLIST_CUTOVER + 42 NO_DA_DO: 53/53 băm và byte bằng master/22382d8 (H3) | Có |
| t26 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| t27 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| t138 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| Xoá hàng README mới | ca nào đỏ | Xoá hàng mục lục hoặc hàng HINT-LUOT6: chỉ t27 đỏ rc1 0/1; t26/t138 vẫn 1/1 (H5) | Chỉ t27 có răng |
| Xoá caveat mới khỏi receipt | ca nào đỏ | t26/t27/t138 đều rc0 1/1 (H5) | **Cả ba không có răng** |
| bien_nhan_v2 tại cay-kho | rc + kết luận | rc0; 240 v2 + 11 legacy + 42 nợ =293, 0 vi phạm/0 không đo; TỔNG: ĐẠT (H4) | Đạt |
| land_evidence_nguon tại cay-kho | rc + kết luận | rc0; 47 ĐẠT, 26/28 miễn trừ, 0 vi phạm/0 không đo, tổng73; TỔNG: ĐẠT (H4) | Đạt |
| doctrine-scan tại cay-kho | rc + kết luận | rc0; sạch, 10 tệp, 0 chỗ chép doctrine (H4) | Đạt |
| doc-claims-check tại cay-kho | `ok=true` | rc0, stdout JSON có `"ok": true`, `"strict": false` (H4) | Đạt |
| HINT.patch lượt này | áp sạch trên clone exact SHA | 5 tệp, `patch --dry-run --batch --fuzz=0 -p0` rc0; áp thật rc0 (H13) | Đã đo trên bản sao |
| Ca/cổng sau hint | giữ điều kiện dương | Ba ca đều 1/1; bốn cổng rc0, JSON ok=true. Land sau sửa mất một miễn trừ và kiểm đủ luật vẫn ĐẠT (H14) | Đạt trên bản sao |
| Cây được chấm cuối lượt | chỉ đọc | HEAD/tree không đổi, status kể cả ignored rỗng, diff rc0 (H17) | Có |

## BẢNG SĂN

Các lệnh cổng chạy tại `cay-kho/`, trừ khi ghi rõ clone. Driver ở `review_evidence/`, đặt `PYTHONDONTWRITEBYTECODE=1`; chỉ dùng ca có sẵn, phép đọc/băm/Git và sửa tài liệu/biên nhận trên bản sao. Clone từ mirror.git nằm ở `/tmp/pr896-r7-mutations-rblaixtc/copy`, HEAD vẫn ghim 05bc12e. Không gọi mạng, push hoặc sửa cây được chấm. Nhật ký tăng dần giữ tại `review_evidence/VERDICT.progress.md`; log/JSON giữ từng kết quả. Số regex hit chỉ dùng chọn đối tượng đọc, không đếm thành finding.

### HƯỚNG 1: Định danh cây

- giả thuyết: sai SHA, cây bẩn hoặc shallow.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree} refs/remotes/origin/master; git status --porcelain; git log --oneline 22382d8..05bc12e`
- output thật:
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
- kết luận: KHÔNG PHẢI LỖI. Shallow=false và core.abbrev=7 kiểm thêm ở H17.

### HƯỚNG 2: Tái áp hint lượt 6 theo byte

- giả thuyết: lời khai áp nguyên hint sai hoặc thừa/sót hunk.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history`
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
outside_hint_non_artifact=['ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml', 'ops/reviews/README.md']
825dab1_paths=122 only_round6_artifacts=True
verdict-cu/pr896-review-6-codex-VERDICT.md: stored_byte_match=True
verdict-cu/pr896-review-6-codex-HINT.patch: stored_byte_match=True
```
- kết luận: KHÔNG PHẢI LỖI. README có đúng sáu hàng bổ sung; delta đầy đủ tại hint-readme-extra.diff. Các hàng hint thêm nguyên vẹn, sáu tệp khác khớp cả byte.

### HƯỚNG 3: YAML, hash verdict và v1

- giả thuyết: đổi byte hiện vật, phá YAML hoặc sửa v1.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity`
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
- kết luận: KHÔNG PHẢI LỖI. integrity.json chứa từng băm/path; kiểm supplementary và toàn bộ land evidence cùng 293 receipt.

### HƯỚNG 4: Ba ca riêng và bốn cổng tại cây gốc

- giả thuyết: xanh do skip hoặc thiếu kết luận dương.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/run_checks.py`
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
- kết luận: KHÔNG PHẢI LỖI của ca/cổng. Mọi ca chạy=1, skip=0; không gặp Codex home is inside a repository. Log stdout/stderr/rc được giữ riêng.

### HƯỚNG 5: Xoá hàng và caveat mới trên clone

- giả thuyết: ca có sẵn bắt được việc mất thông tin mới.
- lệnh: `git clone --no-hardlinks --no-checkout <mirror.git> /tmp/pr896-r7-mutations-rblaixtc/copy; git -C <copy> checkout --detach 05bc12e2b9008071ca28edbd4574e58644d48220; PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/mutations.py`
- output thật:
```text
remove-round6-index removed_bytes=739
t26 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27 rc=1 lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
!!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: verdict 'pr896-review-6-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó.
remove-round6-caveat-readme removed_bytes=365
t26 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27 rc=1 lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
!!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: caveat 'HINT-LUOT6-AP-CUNG-COMMIT-GHI-SO' của pr896-review-6-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-6-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.
remove-round6-receipt-caveat removed_bytes=361
t26 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t138 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
status_after_restore=''
```
- kết luận: KHÔNG PHẢI LỖI hiện hành thuộc các lớp săn, nhưng giới hạn đã chứng minh: t26/t138 không có răng với hai hàng README; t27 có răng. Cả ba không có răng khi xoá caveat mới khỏi receipt. Đã hoàn nguyên từng đột biến trước khi chuyển hướng.

### HƯỚNG 6: Mốc lịch sử và closure ancestry

- giả thuyết: neo sai OID/commit hoặc phép đo ancestry không đúng.
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
- kết luận: KHÔNG PHẢI LỖI; finding cũ đã đóng. 176 phép gồm target ghi trong câu và master/candidate ghim; không suy Packet đã landed. closure-round6.json giữ bảy trường mới và toàn bộ phép đo.

### HƯỚNG 7: Trạng thái chưa review và verdict kế tiếp

- giả thuyết: các đính chính trước đó dẫn sai head/hash hoặc mốc.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews`
- output thật:
```text
old_eight count=8
pr455-bien-nhan-v2-review-2-codex-verdict.md sha=c595292cb63fb8c09d7d7b482cda20f9d5f0917f receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr455-bien-nhan-v2-review-3-codex-verdict.md sha=cb212847375c2319fe0ccad3f7c00c90b870e3ba receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr455-bien-nhan-v2-review-4-codex-verdict.md sha=4ef73e69d5f3c419634118983723355e25e38305 receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr455-bien-nhan-v2-review-5-codex-verdict.md sha=670071b700bd97a893d64393ffded0257957d0b3 receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr455-bien-nhan-v2-review-6-codex-verdict.md sha=5a78c150106ae381461354c77ba2023834330bbd receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md sha=ca960160b477cd16346a293aaa8752772a9921d4 receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr896-review-2-codex-verdict.md sha=8d56009a09af7b3ef93801df105f9483de212cc7 receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr896-review-2-codex-verdict.md sha=8d56009a09af7b3ef93801df105f9483de212cc7 receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
new_two_four_reviews count=4
pr870-review-2-codex-verdict.md sha=06a50c5feea77c2654f31edd26efeed7eeee62f5 receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr870-review-3-codex-verdict.md sha=06a50c5feea77c2654f31edd26efeed7eeee62f5 receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr889-review-2-codex-verdict.md sha=094e8d17ae4dfcf21dca63702c9262267bdc072c receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
pr889-review-3-codex-verdict.md sha=094e8d17ae4dfcf21dca63702c9262267bdc072c receipt_sha_match=True header_match=True hash_match=True absent_at_anchor_rc=128
```
- kết luận: KHÔNG PHẢI LỖI ở 12 đối chiếu. PR870/PR889 lượt 2/3 đều approve 0/0/0/0 trên đúng head; không biến kết quả lượt 1 thành approve.

### HƯỚNG 8: Surface trong ops/reviews

- giả thuyết: còn self-claim trái receipt/run chưa cảnh báo.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/surfaces.py; python3 review_evidence/runtime_index.py`
- output thật:
```text
verdict_files_repo_wide=415 distinct_content=397
run_json_files=50 parse_errors=[]
receipt_runtime_pairs=18 mismatches=[]
service_self_claim_files=25 missing_correction=[]
other_identity_mentions=71 unknown_distinct_verdicts_with_surface=62
ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.md:130 receipt_surface=codex_cli corrections=[('KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC', 1, False)] runtime=[]
runtime_records=122
```
- kết luận: KHÔNG PHẢI LỖI mới trong 25 tự khai service của sổ review. Chỗ chỉ nhắc service/chatgpt_web khi mô tả finding không phải self-claim. Bốn ci-g5 có caveat thiếu runtime; lời mô tả README không nguyên byte nhưng đã cảnh báo giới hạn nguồn. 122 record bao gồm run-*.json và bản sao, không phải 122 run độc lập. Land ngoài inventory được kiểm tại H11/H12.

### HƯỚNG 9: Nguồn của receipt và land mới lượt 6

- giả thuyết: sai SHA/tree/run/hash/mục lục hoặc hiện vật.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/new_claims.py; sha256sum -c SHA256SUMS`
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
  "artifact_sha256sums": {
    "rc": 0,
    "ok_count": 120,
    "failed": [],
    "stderr": ""
  },
  "land_round6_sha_and_receipt_match": true
}
```
- kết luận: KHÔNG PHẢI LỖI ở các scalar runtime, hash, hiện vật và liên kết đã đo. Năm caveat có đúng một hàng README và nguyên mô tả. Điều này không chứng minh mô tả đúng; câu về partial bị bác ở H16.

### HƯỚNG 10: Quét rộng các trạng thái

- giả thuyết: chỉ sửa danh sách cũ còn bỏ sót câu chưa review/áp/merge trong sổ và land.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/inventory.py; python3 review_evidence/status_checks.py; git merge-base --is-ancestor <OID> <ref>; git ls-tree <ref> -- <spec>`
- output thật:
```text
yaml_paths=368 inventory_counts={'unanchored_candidates': 1759, 'anchored_candidates': 398, 'readme': 517}
17f4a1b85b8d5146c5e6dddbdc40f11111a659f7 receipt_matches=0 verdict_header_matches=0
efa397eb2515658a1e3e9b4cdfd6e887b492b957 receipt_matches=0 verdict_header_matches=0
99aef141796ebce7044c9f5c0c8a1a3b3d673d8e receipt_matches=0 verdict_header_matches=0
5a96c1ac8cec1c9958094f92e716941faa47aac5 receipt_matches=0 verdict_header_matches=0
888c0d9b68136f384068ecad8e286819bb175044 receipt_matches=0 verdict_header_matches=0
bf10fab792473bc69dd377c7445978950c4d77a0 receipt_matches=0 verdict_header_matches=0
288ad3ea79ef94e061b649effe7bee2c7e2a0a9b receipt_matches=0 verdict_header_matches=0
b5b6aefa66a8ad037ff34430d0210f3b6873913f receipt_matches=0 verdict_header_matches=0
3ddda026da41b0bb162a3785b93dbb953a298203 receipt_matches=0 verdict_header_matches=0
4bc94325e647ee5e32373f3af30b8f83b98a90fa rc(master,candidate)=[1, 1]
604b8d9a7c5948a9c0690312f1220830d545b52c rc(master,candidate)=[1, 1]
82359c4deec90edebbaebf9ab9d094902120b567 rc(master,candidate)=[1, 0]
2e4183bc2dc40e6bc306e377fc442ff0f405bbe0 rc(master,candidate)=[1, 0]
1a276a15192013fdb1e472db409133b53ac57944 rc(master,candidate)=[1, 0]
d308b0b1bbcb0db2e1624e4eda6431f73ace453f rc(master,candidate)=[1, 0]
22382d8c800bed7b995d093cdcfdc206360d7fd4 rc(master,candidate)=[1, 0]
825dab1c8771113caeb3c5b77c61e89e27d7e292 rc(master,candidate)=[1, 0]
05bc12e2b9008071ca28edbd4574e58644d48220 rc(master,candidate)=[1, 0]
ops/specs/wp775.md ls-tree master='' candidate=''
ops/specs/wp484-r8.md ls-tree master='' candidate=''
HINT c8c1ee0 -> 2e4183b direct_child=True
HINT 77a0a45 -> 1a276a1 direct_child=True
land provenance verdict status: 103 paths, 82 matched lines
```
- kết luận: Đã phân loại bằng ngữ cảnh và Git; P1 mới về #490 nằm ở H15. Các head kể trên chưa có verdict exact-SHA trong inventory nên không dùng review của ancestor/descendant để bác câu chưa review. Spec wp775/wp484 còn vắng ở cả master/candidate. pr696 có do_luc ghim bc57bca và 2026-09-30; pr684 nói rõ trạng thái TẠI THỜI ĐIỂM merge #684, không được đọc thành hiện tại của #689. Các HINT cũ đã có đính chính riêng ghim mốc. Nội dung verdict provenance là phép đo trên reviewed_sha riêng; câu chưa chạy hint trên KHO không có nghĩa executor chưa áp hint về sau. Số hit bao gồm chứa/chữa trong văn bản không dấu và lời trích; không coi từng hit là lỗi.

### HƯỚNG 11: Closure ba surface land lượt 6

- giả thuyết: đính chính sai nguồn/dòng hoặc dùng run cùng SHA nhưng khác lượt.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/land_round6.py`
- output thật:
```text
ops/land/pr832-wp831-provenance/verdict-luot7/wp831-g1-luot7-codex-verdict.md:6 hash=1e27ba6bf2c4690a470b7786fe799c850b5924352a85a24460fb5053ff216d28 hash_matches_caveat=True same_master=True same_prev=True
source=ops/land/pr832-wp831-provenance/verdict-luot7/run.json
run=1ff81cba41874a218b53275d3cdc1418 head=51ae5c095972611d2c6045bd81786a4fc7e9ca62 surface=codex_cli transport=machine program=codex same_round_head=True caveat_source_head_run_match=True
ops/land/pr848-wp744-provenance/verdicts/wp744-g3-luot1-codex-verdict.md:36 hash=af2b5fa426a7d53755148f4f9711712246afadc91e1d75e5267f8c8023bc3911 hash_matches_caveat=True same_master=True same_prev=True
source=ops/land/pr848-wp744-provenance/verdicts/run-f65e544e.json
run=f65e544ef5d64ba7a1e0edb607edcf0a head=23bc189f28ea60f04ca1634b6fe66d02babf12ed surface=codex_cli transport=machine program=codex same_round_head=True caveat_source_head_run_match=True
ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-verdict.md:3 hash=95438373ee2f04a8431e6b10cfd2111144f9744bc54ac114c5670e0652e1ce87 hash_matches_caveat=True same_master=True same_prev=True
source=ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-transcript.txt
header=['OpenAI Codex v0.163.0', '--------', 'workdir: /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv21', 'model: gpt-6-astra', 'provider: openai', 'approval: never', 'sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)', 'reasoning effort: xhigh', 'reasoning summaries: none', 'session id: 01a157da-2170-7be2-b6d0-053fa8f91aec', '--------', 'user', '# Independent read-only review — WP748 r21/g21, PR #862, exact head']
land_luot1=verdicts/wp748-r21-luot1-codex-transcript.txt: codex exec truc tiep, KHONG bien nhan launcher — KHONG tinh assurance.
source_and_session_in_caveat=True
```
- kết luận: KHÔNG PHẢI LỖI. Cả ba self-claim vẫn nguyên byte và được đính chính rõ. #862 lượt 1 không dùng run-f0909b38 của lượt 2; #849 lượt 4/5 cũng đã có đính chính LOI TU PHAN LOAI trong review.luot_cuoi.reviewer.

### HƯỚNG 12: Surface land có nguồn thứ cấp trái lời tự khai

- giả thuyết: còn trường hợp tương tự slice-b-c-review-2, không có runtime gốc để phân xử.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/unresolved_land_surface.py`
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
- kết luận: LỖI P2 `surface-tu-khai-khac-ho-so-land-chua-co-caveat`. Đo được sự bất nhất văn bản và thiếu caveat; bề mặt thực chạy KHÔNG ĐO ĐƯỢC, không kết tội một lời khai runtime cụ thể là sai. Cảnh báo thiếu model/effort không tự cảnh báo mâu thuẫn surface.

### HƯỚNG 13: Áp hint trên exact candidate clone

- giả thuyết: hint không áp được, sửa v1/verdict hoặc YAML hỏng.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py; patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>`
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
- kết luận: KHÔNG PHẢI LỖI của hint cuối 5 tệp. Nhãn patch-as-hint có trong tệp; chỉ áp trên clone. Một lần dựng helper trước đó thử parse README bằng YAML đã dừng trước apply; đã sửa, dựng lại và kiểm lại bản cuối, không dùng lần kiểm clone sạch ấy làm bằng chứng hint (discarded-hint-builder-attempt.txt).

### HƯỚNG 14: Ca/cổng sau hint cuối

- giả thuyết: hint sửa văn bản nhưng làm hỏng cổng hoặc tính toàn vẹn.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/hint_checks.py (cwd clone với đúng 5 path modified)`
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
- kết luận: KHÔNG PHẢI LỖI của hint. Các kết quả này thuộc clone đã áp bản cuối 5 tệp. Sửa pr491 mất miễn trừ của land_evidence_nguon, nhưng kiểm đầy đủ vẫn đạt: 48 ĐẠT +25 miễn trừ=73; không sửa allowlist để lấy lại miễn trừ.

### HƯỚNG 15: Khẳng định #490 chưa merge

- giả thuyết: nhãn nguồn THUẬT LẠI đã bị dùng thay mốc thời gian.
- lệnh: `git blame -L 241,248 05bc12e -- ops/land/pr491-r358-ghi-so-land-evidence.yaml; git show -s --format="%H %P %s" 8cee941; git merge-base --is-ancestor 8cee941 <cdd0b1d/master/candidate>`
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
- kết luận: LỖI P1 `pr490-chua-merge-trai-lich-su-git`. Không có mốc lịch sử cho hàng đang khai NỢ CŨ còn nguyên. Bản sửa neo lời khai vào cdd0b1d, giữ lịch sử và đính chính quan hệ Git hiện tại; không suy PR479 hay Packet đã landed. Các mô tả bot cùng reviewed head 2ec6171 trong receipt/README là thuật lại phép đối chiếu của lượt đó, không coi là lời tuyên #490 đang mở ngày nay.

### HƯỚNG 16: Mô tả hiện vật mới của lần hỏng

- giả thuyết: receipt mới tóm tắt thiếu nội dung tệp được chính nó trỏ tới.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/failed_run_claims.py; wc -c <VERDICT.partial.md>; rg -n "^### |^verdict:" <VERDICT.partial.md>`
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
- kết luận: LỖI P1 `mo-ta-partial-luot6-khong-khop-hien-vat`. Đo nội dung tệp frozen chứ không suy lần hỏng là review hoàn tất. Dòng dang_lam và việc không tính nó như verdict chốt vẫn đúng; phần chỉ có một t26 sai.

### HƯỚNG 17: Kiểm toàn vẹn cuối

- giả thuyết: cây gốc bị đổi hoặc hint lén sửa hiện vật/receipt v1.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/final_checks.py; git status --porcelain=v1 --untracked-files=all --ignored; git diff --exit-code`
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
- kết luận: KHÔNG PHẢI LỖI. Cây gốc vẫn sạch kể cả ignored; clone có đúng 5 path tài liệu/receipt trong hint; 4 YAML hợp lệ và ID không trùng; 53 v1, mọi verdict giữ nguyên. 137 entry manifest verdict đều khớp, không có đường dẫn vắng.

## FINDING MỚI

### pr490-chua-merge-trai-lich-su-git [P1] Hồ sơ land #491 còn khai #490 chưa merge

TỆP/DÒNG: `ops/land/pr491-r358-ghi-so-land-evidence.yaml:244`, scalar `bookkeeping.4` bắt đầu ở dòng 242.

VẤN ĐỀ: Hàng hiện hành bắt đầu bằng “NỢ CŨ KHÔNG ĐỘNG TỚI”, khai “PR #479 và #490 chưa merge”. #490 đã merge bằng `8cee9410e958a6b9d956e080c11878fbd80d9f5f`, cha thứ hai `01e7f77d707cb093b5ba6d9b9d8577f40d025488`; merge ấy ở cả master ghim và candidate. “THUẬT LẠI” chỉ phân loại nguồn, không nói câu này đúng tại commit/thời điểm cũ nào. Không có caveat/đính chính cho hàng này. Đây là trạng thái Git đo được, không phải yêu cầu quyết định land của chủ kho.

ĐÃ THỬ NGHIỆM: H15: `git merge-base --is-ancestor 8cee941... 3e973a0...` rc0; cùng lệnh tới `05bc12e...` rc0. `git blame` và `git show cdd0b1d...:<path>` cho đúng scalar lịch sử; merge490→cdd0b1d rc1, nên có thể giữ câu ở mốc cũ thay vì trình bày như hiện hành. HINT thêm mốc và đính chính; đã áp sạch và qua cổng trên clone (H13/H14).

ĐỘ TIN: cao.

### mo-ta-partial-luot6-khong-khop-hien-vat [P1] Biên nhận mới khai sai nội dung partial đã lưu

TỆP/DÒNG: `ops/reviews/pr896-review-6-codex-verdict.receipt.yaml:126`; bản chiếu `ops/reviews/README.md:766`. Đối tượng được mô tả: `ops/reviews/pr896-review-6-codex/luot-hong-c0fa33fa/VERDICT.partial.md:7`.

VẤN ĐỀ: Hai chỗ do `05bc12e` thêm khẳng định “VERDICT.partial.md chi co dong dang_lam + mot phep do t26”. Tệp trong đúng SHA được chấm có **28.214 byte và 14 heading phép đo/đối chiếu**, gồm t27, t138, cả bốn cổng, lịch sử/băm/ancestry, đột biến README/caveat. Đây là lời khai mới sai về hiện vật có sẵn để đối chứng; không phải suy đoán về runtime hoặc diễn giải severity của verdict cũ.

ĐÃ THỬ NGHIỆM: H16: `wc -c` → 28214; `rg -n '^### |^verdict:'` → `verdict: dang_lam` + 14 mục, tên/dòng đầy đủ trong failed-run-claims.json. SHA256 partial `1d3f44f96f638c8224656b33385acf074ea2b168286a819dca4acbd0763ef869`. Run hỏng và run được tính có cùng prompt/head, nhưng tệp partial vẫn chưa chốt, không được tính thành verdict hoàn tất. HINT chỉ sửa mô tả ở receipt và README; giữ nguyên mọi hiện vật (H13/H14).

ĐỘ TIN: cao.

### surface-tu-khai-khac-ho-so-land-chua-co-caveat [P2] Hai tự khai service còn thiếu cảnh báo mâu thuẫn với hồ sơ

TỆP/DÒNG:

- `ops/land/pr823-wp802-provenance/verdict-luot5/wp802-g1-luot5-codex-verdict.md:6`; hồ sơ `ops/land/pr823-wp802-land-evidence.yaml:111` và dòng 114.
- `ops/land/pr877-wp854-provenance/verdicts/wp854-g1-luot2-codex-verdict.md:11`; hồ sơ `ops/land/pr877-wp854-land-evidence.yaml:78`.

VẤN ĐỀ: Đây đều là **tự khai của reviewer** `codex_service`, không phải nhắc chuỗi trong finding. #823 đồng thời ghi `review.so_loi_goi_codex_cli: 5`, và `luot_cuoi` nối chính lượt 5 với run b3d8a108/head 5c6c7a8. #877 đồng thời ghi các lượt review chỉ có “header CLI gpt-6.1-sol xhigh”. Hai hồ sơ không cảnh báo sự khác biệt surface; giới hạn hiện có chỉ nói model/effort/attestation. Không có run.json/transcript của chính lượt tương ứng trong cây để quyết định lời nào đúng. Do đó chỉ chấm **P2 thiếu điều kiện nguồn**, không chấm P1 khẳng định bề mặt thực tế sai và không tự đổi thành CLI. Cùng cách xử lý đã có ở supplementary caveat slice-b-c-review-2.

ĐÃ THỬ NGHIỆM: H12: đối chiếu đúng dòng verdict, YAML và comment #6247520447 lưu trong kho; comment khớp lượt 5/head/run. Trong 122 record run*.json (có bản sao) không có record mang hai reviewed head này; `verdict_usage_caveats` của hai hồ sơ đều vắng. Băm hai verdict lần lượt `b6ee86d0c9e523dfbe87718d12b4d646464e7a8720e9789f071f4aa04d6e3f01` và `612e86d854f4a7aad84a5f8e8d5986f58677e1b789d6ad3f176fefd1435cf277`, byte bằng master/22382d8. HINT thêm caveat thiếu nguồn, giữ cả hai lời khai lịch sử và không chọn surface; áp và cổng trên clone đều đạt (H13/H14).

ĐỘ TIN: cao về sự bất nhất và thiếu caveat; **KHÔNG ĐO ĐƯỢC** bề mặt thực chạy.

## GỢI Ý VÁ

`HINT.patch` là dữ liệu gợi ý, **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Năm tệp: land #491, #823, #877; receipt lượt 6 và README. Không đổi verdict, partial, receipt v1 hay allowlist. Đã `patch --dry-run --fuzz=0 -p0` và áp thật trên clone tại exact reviewed_sha, rồi chạy lại đủ ba ca + bốn cổng. SHA256 hint: `65e791768d947ee83be72e846274b0ce59ad6e230a20cb67fb6b5b43255bdff6`.
