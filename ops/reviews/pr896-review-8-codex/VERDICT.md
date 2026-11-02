verdict: approve
reviewed_sha: fb87110cfab832406984f893e6a4c79fbb932aef
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

## KẾT LUẬN VỀ FINDING CŨ

- P1 `pr490-chua-merge-trai-lich-su-git`: **ĐÃ ĐÓNG**. `ops/land/pr491-r358-ghi-so-land-evidence.yaml:242` ghim lời khai cũ vào `cdd0b1d19439e286fb7a86020ce2d258bafc2102`; dòng 248 đính chính merge `8cee9410e958a6b9d956e080c11878fbd80d9f5f`, đúng cha thứ hai `01e7f77d707cb093b5ba6d9b9d8577f40d025488`. Merge là tổ tiên master ghim, reviewed head lượt 7 và SHA lượt này, cả ba rc=0 (H6).
- P1 `mo-ta-partial-luot6-khong-khop-hien-vat`: **ĐÃ ĐÓNG**. Receipt lượt 6 dòng 126 và README dòng 766 đều mô tả đúng 28.214 byte, 14 mục đo/đối chiếu, vẫn `dang_lam`; không còn câu “chỉ ... một phép đo t26”. Đã đo cả head/prompt giống nhau, rc=1, 349,795 s (H6).
- P2 `surface-tu-khai-khac-ho-so-land-chua-co-caveat`: **ĐÃ ĐÓNG** phần thiếu caveat. #823 dòng 151 và #877 dòng 96 có caveat đúng path/hash/dòng self-claim/head/nguồn. Comment #823 đúng lượt 5, head `5c6c7a8...`, run `b3d8a108`. Không có runtime cùng lượt trong tập nguồn cục bộ để phân xử surface thật; caveat giữ **KHÔNG ĐO ĐƯỢC**, không tự chọn CLI hay service (H6/H8/H14).

Approve đối với bản vá và hai lớp lời khai được giao. Chưa phát hiện finding mới sau các hướng đo dưới đây. Kết quả này không phải quyết định merge/land hoặc chứng thực độc lập model/backend lịch sử.

## BẢNG ĐO

Các lệnh kiểm cổng chạy với cwd `cay-kho/`; driver và log ở `review_evidence/`. Bản sao đột biến được clone cục bộ từ `mirror.git`, ngoài `cay-kho/`, checkout đúng reviewed SHA. Không gọi mạng. Mốc master dùng trong mọi phép so là `3e973a03b151e37cd402e0a723816eeaa8247193`.

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| HEAD, tree, cây sạch, đầy đủ | `fb87110...`, detached, không shallow | `git rev-parse HEAD HEAD^{tree}` → đúng SHA / `a653c501d218f3b72590dc28433c8f78d00643c1`; `git status --porcelain` rỗng; `--is-shallow-repository` → false (H1/H13) | Có |
| Hai commit kể từ lượt 7 | `54021fb` chỉ hiện vật; `fb87110` ghi sổ + hint | `git log 05bc12e..fb87110`; 147 path của `54021fb` đều thuộc hiện vật lượt 7 (H1/H3) | Có |
| Snapshot diff/numstat đúng hai khoảng SHA | delta lượt 7 và toàn PR so master | Tái sinh bằng `git diff`/`--numstat`; cả bốn tệp byte_match=True (H3) | Có |
| Áp nguyên hint lượt 7 | 5 tệp, fuzz=0, cùng commit ghi sổ | `patch --batch --fuzz=0 -p0` trên byte gốc tại `05bc12e` rc=0. 4/5 tệp khớp toàn bộ byte với `fb87110`; README có đúng 6 hàng thêm, không sửa/xóa hàng của hint. Hunk thật thuộc commit `fb87110` (H3) | Có; không gọi README nguyên tệp là byte-exact |
| #490 chưa merge là lời khai lịch sử | Neo `cdd0b1d...`, đính chính merge `8cee941...` | `git show <anchor>:<path>` có câu cũ; `git show -s --format=%P 8cee941`; ancestry tới master/05bc12e/fb87110 đều rc=0, tới mốc cũ rc=1 (H6) | Có |
| Partial lượt 6 | 28.214 byte, 14 mục, dang_lam | Đọc byte/heading: 28.214 byte, 306 dòng, 14 heading đều là mục tiến độ/đo; receipt và README mô tả giống nhau (H6) | Có |
| Run chết lượt 6 | `c0fa33fa`, rc=1, 349,795 s, cùng prompt/head | Đọc hai `run.json`: đúng rc/thời lượng; head và prompt_sha256 bằng run hoàn tất (H6) | Có |
| Partial lượt 7 mới | 361 byte, 3 heading, dang_lam | 361 byte, 13 dòng, 3 heading: kết luận cũ / bảng đo / bảng săn; chưa có phép đo hoặc verdict hoàn tất (H6) | Có |
| Run chết lượt 7 mới | `577bb136`, rc=1, 44,945 s, overloaded | Đọc run JSON + `loi-may-chu.txt`: đúng rc/thời lượng, `server_overloaded`, thông báo capacity; cùng head/prompt với run hoàn tất (H6) | Có |
| #823 caveat đúng lời tự khai | Dòng 6, hash `b6ee86...`, lượt 5 | Đọc dòng 6/hash; comment 6247520447 có lượt 5 / đúng full head / run b3d8a108; không thấy runtime cùng head trong 124 JSON (H6/H8/H14) | Có; surface thật không đo được |
| #877 caveat đúng lời tự khai | Dòng 11, hash `612e86...`, lượt 2 | Đọc dòng 11/hash; `khong_do_duoc.0` đúng lời thuật lại CLI; không thấy runtime cùng head trong 124 JSON (H6/H8) | Có; surface thật không đo được |
| Những đính chính land cũ còn đúng | #832 / #848 / #862 / #849 | Hai run JSON đúng run/head/CLI; hai transcript khác xác nhận CLI ở #862/#849, hồ sơ đã có đính chính (H8) | Có |
| Rà surface rộng hơn tên `run.json` | Tự khai phải khớp nguồn hoặc có caveat | 514 nội dung verdict khác nhau, 555 chỗ nhắc surface; 124 JSON runtime đủ tiêu chí; 19 cặp receipt/runtime không lệch. Đã phân biệt trích finding với tự khai; kiểm riêng cách nói tiếng Việt, Desktop và subagent (H7/H8) | Chưa phát hiện thiếu đính chính mới |
| YAML và caveat IDs | Tệp sửa parse được, không trùng id | Loader bắt duplicate key; 369 YAML parse, 294 receipt, duplicate_ids=[] (H4) | Có |
| Byte verdict không đổi | Hash giữ nguyên | 304 cặp path/hash đều khớp; không có verdict lịch sử bị sửa so master; 272 verdict phẳng có hash khai; 18 cặp bản phẳng/bản gốc byte-equal (H4/H13) | Có |
| Receipt v1 đóng băng | Không đổi allowlist | AST `ALLOWLIST_CUTOVER`=11, `NO_DA_DO`=42; từng byte và hash bằng master và `05bc12e` (H4) | Có |
| Các câu lịch sử/ancestry đã neo | Mốc nguồn và phép so Git đúng | 48 trường ghim đúng commit tạo receipt; 176 phép ancestry rc=0. 35 mô tả trùng văn bản, 13 mô tả diễn giải lại, không gọi là bản sao nguyên văn (H9/H12) | Đúng quan hệ/trạng thái đã đo; không phải tất cả byte-exact |
| Những câu CHƯA review đã được đính chính | Có verdict kế tiếp đúng head | 8 đính chính và 4 review #870/#889: receipt/head/header/hash đúng, verdict kế tiếp chưa tồn tại ở mốc cũ (rc=128 với cat-file); review #870/#889 đều approve (H9/H14) | Có |
| Các câu “chưa merge” của chuỗi #947 | Các head `82359c4`…`fb87110` chưa vào master | `git merge-base --is-ancestor <head> <master>` đều rc=1; so candidate rc=0 (H10) | Có |
| Những trạng thái thuộc khối cũ | #684/#696/#554 là mốc lịch sử | Đọc cả `packet_landed_ghi_chu`, `do_luc`, `CAP_NHAT_1`; không coi “chưa land” là phủ định merge; `bc57bca`→`423b4ba` rc=1 (H10/H12) | Không phát hiện mâu thuẫn mới |
| Receipt/README/land lượt 7 | 43.635 byte, 2 P1 + 1 P2, run `2ca2785d` | Header/hash/tree/prompt/blob neo `54021fb` đúng; run rc=0, 1.144,447 s, 48 sự kiện / 48 response_id, gpt-6.1-sol; 5 hàng caveat README khớp mô tả (H11) | Có đối với dữ liệu ghi trong nguồn |
| Manifest hiện vật lượt 7 | SHA256SUMS | `sha256sum -c SHA256SUMS` rc=0, 145/145 OK (H11) | Có |
| `t26_` riêng | Đạt đủ N/N | rc=0; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (H2/H13) | Có |
| `t27_` riêng | Đạt đủ N/N | rc=0; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (H2/H13) | Có |
| `t138_` riêng | Đạt đủ N/N | rc=0; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (H2/H13) | Có |
| Xóa hàng mục lục lượt 7 trên clone | Ca phải bắt mất hàng | t26 rc=0 1/1; **t27 rc=1 0/1**, đúng lỗi thiếu cột verdict; t138 rc=0 1/1 (H5) | t27 có răng; t26/t138 không có răng với hàng này |
| Xóa hàng caveat README mới trên clone | Ca phải bắt mất hàng | t26 rc=0 1/1; **t27 rc=1 0/1**, đúng lỗi thiếu id cùng verdict; t138 rc=0 1/1 (H5) | t27 có răng; t26/t138 không có răng với hàng này |
| Xóa caveat mới trong receipt trên clone | Đo giới hạn ca hiện có | Cả t26/t27/t138 rc=0, đều 1/1, không skip; phục hồi cây sạch (H5) | Cả ba không có răng với việc xóa caveat khỏi receipt |
| `python3 ops/bien_nhan_v2.py --root .` | Đạt | rc=0; `bien_nhan_v2: 241 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 294`; `TỔNG: ĐẠT` | Có |
| `python3 ops/land_evidence_nguon.py --root .` | Đạt | rc=0; `land_evidence_nguon: 48 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73`; `TỔNG: ĐẠT` | Có |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Sạch | rc=0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` | Có |
| `python3 scripts/tl.py doc-claims-check --json` | `"ok": true` | rc=0; JSON parse được, `ok` đúng boolean true; strict=false (H2/H13) | Có |

## BẢNG SĂN

### HƯỚNG 1: Định danh cây và chuỗi commit

- giả thuyết: SHA/cây/base bị lệch hoặc có thay đổi ngoài đối tượng.
- lệnh và output thật:
```text
$ git rev-parse HEAD
rc=0
fb87110cfab832406984f893e6a4c79fbb932aef

$ git rev-parse HEAD^{tree}
rc=0
a653c501d218f3b72590dc28433c8f78d00643c1

$ git status --porcelain=v1
rc=0

$ git rev-parse --is-shallow-repository
rc=0
false

$ git symbolic-ref -q HEAD
rc=1

$ git rev-parse refs/remotes/origin/master
rc=0
3e973a03b151e37cd402e0a723816eeaa8247193

$ git log --format="%H %s" 05bc12e..fb87110
rc=0
fb87110cfab832406984f893e6a4c79fbb932aef ops: bien nhan cross-review luot 7 #896 + ap HINT luot 7 + khoi luot 7 ho so land
54021fb0a92eae606076606fc83431c486013bdd ops/reviews: hien vat cross-review luot 7 #896 (codex, cham 05bc12e)
```
- kết luận: KHÔNG PHẢI LỖI. HEAD đúng SHA, detached, cây sạch, không shallow; master được ghim theo OID đã đo, không suy trạng thái land từ merge.

### HƯỚNG 2: Ba ca riêng và bốn cổng trên cây gốc

- giả thuyết: cổng xanh chỉ do bỏ qua, số đạt không đủ, hoặc doc-claims không ok.
- lệnh và output thật (log đầy đủ ở `review_evidence/`):
```text
$ python3 ops/lease_publish_test.py --chi-ca=t26_
rc=0
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
$ python3 ops/lease_publish_test.py --chi-ca=t27_
rc=0
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
$ python3 ops/lease_publish_test.py --chi-ca=t138_
rc=0
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
$ python3 ops/bien_nhan_v2.py --root .
rc=0
bien_nhan_v2: 241 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 294
TỔNG: ĐẠT
$ python3 ops/land_evidence_nguon.py --root .
rc=0
land_evidence_nguon: 48 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
$ python3 .claude/dev/packet_loop.py doctrine-scan --root .
rc=0
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
$ python3 scripts/tl.py doc-claims-check --json
rc=0
  "ok": true,
  "strict": false
```
- kết luận: KHÔNG PHẢI LỖI. Đây là phép đo cổng, không tự chứng minh nội dung mọi lời khai.

### HƯỚNG 3: Tái áp hint lượt 7 và đối chiếu byte

- giả thuyết: Hint bị áp thiếu/khác, hoặc snapshot/diff không đúng SHA.
- lệnh: `python3 review_evidence/measure.py history`
- output thật:
```text
diff.patch byte_match=True
numstat.txt byte_match=True
diff-pr947.patch byte_match=True
numstat-pr947.txt byte_match=True
hint_paths=5 apply_rc=0
patching file ops/land/pr491-r358-ghi-so-land-evidence.yaml
patching file ops/land/pr823-wp802-land-evidence.yaml
patching file ops/land/pr877-wp854-land-evidence.yaml
patching file ops/reviews/README.md
patching file ops/reviews/pr896-review-6-codex-verdict.receipt.yaml
ops/land/pr491-r358-ghi-so-land-evidence.yaml full_byte_match=True
ops/land/pr823-wp802-land-evidence.yaml full_byte_match=True
ops/land/pr877-wp854-land-evidence.yaml full_byte_match=True
ops/reviews/README.md full_byte_match=False
ops/reviews/pr896-review-6-codex-verdict.receipt.yaml full_byte_match=True
README beyond hint:
+| `pr896-review-7-codex-verdict.md` | `HINT-LUOT7-AP-CUNG-COMMIT-GHI-SO` | Verdict lich su tren 05bc12e la changes_requested 2 P1 + 1 P2. HINT.patch luot 7 (5 tep) duoc ap NGUYEN (--fuzz=0) trong CHINH commit ghi so bien nhan nay, theo yeu cau chu kho "va cho toi khi het P1, P2, P3". Can verdict moi tren exact SHA ung vien; khong doi ket qua hay byte verdict lich su. |
+| `pr896-review-7-codex-verdict.md` | `LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI` | Run 577bb136 (cung prompt, cung head) ma_thoat 1 sau 44.945 s: transcript codex ghi server_overloaded "Selected model is at capacity" (luot-hong-577bb136/loi-may-chu.txt). luot-hong-577bb136/VERDICT.partial.md do wc luc ghi so: 361 byte, 3 heading, dong dau `verdict: dang_lam`; KHONG duoc tinh la verdict. |
+| `pr896-review-7-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong; phien ghi so do sau luot: HEAD 05bc12e, git status rong. |
+| `pr896-review-7-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (review_evidence/) tham chieu duong dan tuyet doi cua sandbox phien; tai lap can dung lai mirror tai 05bc12e. |
+| `pr896-review-7-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff.patch, diff-pr947.patch, review_evidence/status-inventory.json va status-unanchored.txt (>500 KB) KHONG vao kho; sha256/so byte o OMITTED.txt. |
+| [`pr896-review-7-codex-verdict.md`](pr896-review-7-codex-verdict.md) | [`.receipt.yaml`](pr896-review-7-codex-verdict.receipt.yaml) | KHONG_AP_DUNG (viec chu kho giao truc tiep, khong packet/lease) | `changes_requested` 0/2/1/0 tren `05bc12e` (head PR #947, mang HINT luot 6) · `cross_reviewed` (codex CLI khac ho executor, `launcher.py run 2ca2785d`, lan dau 577bb136 chet vi may chu qua tai; model_phuc_vu DO_DUOC `gpt-6.1-sol` = do_may) · hai finding luot 6 DA DONG; con: P1 #491 khai #490 chua merge, P1 mo ta partial luot 6 sai, P2 #823/#877 tu khai codex_service — HINT.patch luot 7 ap trong chinh commit ghi so bien nhan nay · ban phang nguyen byte cua `pr896-review-7-codex/VERDICT.md`. Chua merge. | `05bc12e2` | 43635 |
54021fb paths=147 only_round7_artifacts=True
prior VERDICT.md stored_byte_match=True
prior HINT.patch stored_byte_match=True
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 4: Toàn vẹn YAML, hash và biên nhận v1

- giả thuyết: Phá YAML, trùng caveat, đổi byte verdict hoặc receipt miễn trừ.
- lệnh: `python3 review_evidence/measure.py integrity`
- output thật:
```text
yaml_parsed=369 receipts=294 duplicate_ids=[]
verdict_path_hashes=304 all_match=True
flat_verdicts=272 unclaimed=[]
frozen_groups={'ALLOWLIST_CUTOVER': 11, 'NO_DA_DO': 42} all_hash_and_bytes_match=True
modified_historical_verdicts=[]
errors=[]
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 5: Đột biến hàng README và caveat mới trên clone

- giả thuyết: Ba ca có sẵn phải thật sự phát hiện mất hàng/caveat mới.
- lệnh: `git clone --no-hardlinks --no-checkout mirror.git <copy>; git checkout --detach fb87110cfab832406984f893e6a4c79fbb932aef; python3 review_evidence/mutations.py`
- output thật:
```text
copy=/tmp/pr896-r8-copy-c2n3k2yh/repo
HEAD=fb87110cfab832406984f893e6a4c79fbb932aef
delete-new-index-row removed_bytes=737
t26 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27 rc=1 !!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: verdict 'pr896-review-7-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó.
  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: verdict 'pr896-review-7-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó.
lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
delete-new-caveat-readme-row removed_bytes=388
t26 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27 rc=1 !!! do t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc README.md: caveat 'LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI' của pr896-review-7-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-7-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.
  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI' của pr896-review-7-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr896-review-7-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.
lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
t138 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
delete-new-receipt-caveat removed_bytes=384
t26 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t138 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
status_after_restore=''
```
- kết luận: KHÔNG PHẢI LỖI hiện hành trong hai lớp săn; t27 có răng với hàng mục lục/cảnh báo README. t26 và t138 không có răng với các hàng đó; cả ba không có răng khi xóa caveat khỏi receipt. Không quy chốt kiểm hình thức thành chốt nội dung.

### HƯỚNG 6: Đóng ba finding cũ và đo lại partial lượt 6/7

- giả thuyết: Đính chính sai SHA/cha merge, dòng surface hoặc số byte/heading.
- lệnh: `python3 review_evidence/closure.py`
- output thật:
```text
ops/land/pr491-r358-ghi-so-land-evidence.yaml anchor_blob_has_old_claim=True
8cee9410e958a6b9d956e080c11878fbd80d9f5f 00e017af102bc8355e0c276d2d813e20620ddb42 01e7f77d707cb093b5ba6d9b9d8577f40d025488 Merge pull request #490 from ducthangho/claude/handoff-tra-luat-repo-2ak5th
git merge-base --is-ancestor 8cee9410e958a6b9d956e080c11878fbd80d9f5f 3e973a03b151e37cd402e0a723816eeaa8247193 rc=0
git merge-base --is-ancestor 8cee9410e958a6b9d956e080c11878fbd80d9f5f 05bc12e2b9008071ca28edbd4574e58644d48220 rc=0
git merge-base --is-ancestor 8cee9410e958a6b9d956e080c11878fbd80d9f5f fb87110cfab832406984f893e6a4c79fbb932aef rc=0
git merge-base --is-ancestor 8cee9410e958a6b9d956e080c11878fbd80d9f5f cdd0b1d19439e286fb7a86020ce2d258bafc2102 rc=1
{"round": 6, "bytes": 28214, "lines": 306, "headings": 14, "measurement_sections": 0, "first": "verdict: dang_lam", "run_id": "c0fa33fa91f34a3db8450d2e75dd6071", "rc": 1, "duration": 349.795, "same_head": true, "same_prompt": true, "readme_description_match": true}
headings=['### Tiến độ phép đo t26', '### Tiến độ phép đo t27', '### Tiến độ phép đo t138', '### Tiến độ phép đo bien_nhan', '### Tiến độ phép đo land', '### Tiến độ phép đo doctrine', '### Tiến độ phép đo doc_claims', '### H1-history', '### H2-integrity', '### H4-review-states', '### H5-remove_new_readme_row', '### H5-remove_new_receipt_caveat', '### H3-ancestry', '### H4-review-states']
caveat=Run c0fa33fa (cung prompt, cung head) ma_thoat 1 sau 349.795 s: transcript codex ghi server_overloaded "Selected model is at capacity". VERDICT.partial.md (28214 byte) van dang_lam, da ghi 14 muc phep do/doi chieu (gom t26, t27, t138, bon cong va cac huong Git/dot bien); KHONG duoc tinh la verdict hoan tat. Hien vat o luot-hong-c0fa33fa/.
{"round": 7, "bytes": 361, "lines": 13, "headings": 3, "measurement_sections": 0, "first": "verdict: dang_lam", "run_id": "577bb13646ce4d458fa5ca650dc6c1af", "rc": 1, "duration": 44.945, "same_head": true, "same_prompt": true, "readme_description_match": true}
headings=['## KẾT LUẬN VỀ FINDING CŨ', '## BẢNG ĐO', '## BẢNG SĂN']
caveat=Run 577bb136 (cung prompt, cung head) ma_thoat 1 sau 44.945 s: transcript codex ghi server_overloaded "Selected model is at capacity" (luot-hong-577bb136/loi-may-chu.txt). luot-hong-577bb136/VERDICT.partial.md do wc luc ghi so: 361 byte, 3 heading, dong dau `verdict: dang_lam`; KHONG duoc tinh la verdict.
ops/land/pr823-wp802-provenance/verdict-luot5/wp802-g1-luot5-codex-verdict.md:6: Reviewer OpenAI Codex; provider `openai_codex`, execution surface `codex_service` (API agent có shell), transport `machine`. Model ID/effort/session ID và danh tính executor thực chạy chưa có receipt độc lập: **KHÔNG ĐO ĐƯỢC**. Không suy surface từ lease, không tự cấp assurance hoặc quyền merge/land. Áp ngưỡng assignment: hết P0/P1 và mọi P2 đóng; P3 mở cần quyết định chủ kho. sha256=b6ee86d0c9e523dfbe87718d12b4d646464e7a8720e9789f071f4aa04d6e3f01
pr823 caveat=[{"id": "SURFACE-TU-KHAI-KHAC-HO-SO-RUNTIME-CHUA-DO-DUOC", "muc": "P2", "verdict_path": "ops/land/pr823-wp802-provenance/verdict-luot5/wp802-g1-luot5-codex-verdict.md", "verdict_sha256": "b6ee86d0c9e523dfbe87718d12b4d646464e7a8720e9789f071f4aa04d6e3f01", "mo_ta": "Verdict luot 5 dong 6 tu khai codex_service; review.so_loi_goi_codex_cli cua ho so nay ghi 5, va review.luot_cuoi.reviewer thuat lai launcher run b3d8a108 cho CHINH luot 5 tren 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456 (readback-comment-6247520447.json). Tai 05bc12e2b9008071ca28edbd4574e58644d48220 khong co run.json/transcript cua dung run de phan xu hai loi khai surface. So luot CLI va loi thuat lai khong thay bang chung runtime. Be mat thuc chay KHONG_DO_DUOC; khong tu chon codex_cli hay codex_service. Giu byte verdict, khong chung thuc model/effort hay nang assurance/quyen merge/land."}]
ops/land/pr877-wp854-provenance/verdicts/wp854-g1-luot2-codex-verdict.md:11: Provider: OpenAI/Codex, model_family=openai; công cụ shell Linux trong phiên agent (`codex_service`, transport=machine). Không tự xác nhận served-model, launcher attestation, GitHub submitter hoặc cấp receipt/assurance. Review theo hai trục spec và standards/security, lớp sensitive; không merge, push, deploy hoặc gọi LIVE. sha256=612e86d854f4a7aad84a5f8e8d5986f58677e1b789d6ad3f176fefd1435cf277
pr877 caveat=[{"id": "SURFACE-TU-KHAI-KHAC-HO-SO-RUNTIME-CHUA-DO-DUOC", "muc": "P2", "verdict_path": "ops/land/pr877-wp854-provenance/verdicts/wp854-g1-luot2-codex-verdict.md", "verdict_sha256": "612e86d854f4a7aad84a5f8e8d5986f58677e1b789d6ad3f176fefd1435cf277", "mo_ta": "Verdict luot 2 dong 11 tu khai codex_service; khong_do_duoc.0 cua ho so nay lai thuat lai cac luot review co header CLI gpt-6.1-sol xhigh. Tai 05bc12e2b9008071ca28edbd4574e58644d48220 khong co run.json/transcript cua chinh luot 2 tren b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb de phan xu hai loi khai surface; cau noi ve header CLI chi la nguon thu cap. Be mat thuc chay KHONG_DO_DUOC; khong tu chon codex_cli hay codex_service. Giu byte verdict, khong chung thuc model/effort hay nang assurance/quyen merge/land."}]
pr823 review={"so_loi_goi_codex_cli": 5, "tran": "loi_khai_co_neo — tran 4 -> 5 lan goi Codex va +1 attempt theo chu kho \"Chọn 1\" (comment 6247229964); vuot tran 6 tep/450 dong (482 dong) theo \"Chọn a\" (comment 6246303988).", "luot_cuoi": {"reviewer": "codex qua launcher.py run, run b3d8a108 (thuat_lai — comment 6247520447: 1092s, ma_thoat 0; commit c25d0f8 ghi nham id run).", "hien_vat": "ops/land/pr823-wp802-provenance/verdict-luot5/", "ket_qua": "thuat_lai — approve, P0=0 P1=0 P2=0 P3=0 tren 5c6c7a8 = head merge."}, "thread": "measured — readback-review-threads-823.json: 0 thread."}
pr877 khong_do_duoc=["Model thuc phuc vu cac luot review KHONG_DO_DUOC (chi co header CLI gpt-6.1-sol xhigh).", "Merge bam tay hay qua mot phien dung credential chu kho: KHONG_DO_DUOC (chi co merged_by)."]
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 7: Lớp tự khai surface trong mọi loại tên verdict và provenance land

- giả thuyết: Còn verdict tự nhận service nhưng run/receipt cùng lượt ghi CLI, chưa đính chính.
- lệnh: `python3 review_evidence/inventory.py; python3 review_evidence/surfaces.py`
- output thật:
```text
distinct_verdict_contents=514 surface_mentions=555
runtime_records_all_json_names=124 surfaces={'codex_cli': 116, 'subprocess': 8}
receipt_runtime_pairs=19 mismatches=[]
service_self_claims=33 finding_or_evidence_only=12
ops/land/pr823-wp802-provenance/verdict-luot5/wp802-g1-luot5-codex-verdict.md => [('ops/land/pr823-wp802-land-evidence.yaml', 'SURFACE-TU-KHAI-KHAC-HO-SO-RUNTIME-CHUA-DO-DUOC')]
ops/land/pr832-wp831-provenance/verdict-luot7/wp831-g1-luot7-codex-verdict.md => [('ops/land/pr832-wp831-land-evidence.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/land/pr848-wp744-provenance/verdicts/wp744-g3-luot1-codex-verdict.md => [('ops/land/pr848-wp744-land-evidence.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/land/pr849-wp748-provenance/verdicts/wp748-r20-luot4-codex-verdict.md => []
ops/land/pr849-wp748-provenance/verdicts/wp748-r20-luot5-codex-verdict.md => []
ops/land/pr862-wp748-r21-provenance/verdicts/wp748-r21-luot1-codex-verdict.md => [('ops/land/pr862-wp748-r21-land-evidence.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/land/pr877-wp854-provenance/verdicts/wp854-g1-luot2-codex-verdict.md => [('ops/land/pr877-wp854-land-evidence.yaml', 'SURFACE-TU-KHAI-KHAC-HO-SO-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.md => [('ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.receipt.yaml', 'KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC')]
ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.md => [('ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.receipt.yaml', 'KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC')]
ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.md => [('ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.receipt.yaml', 'KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC')]
ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.md => [('ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.receipt.yaml', 'KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC')]
ops/reviews/phan-bien-quy-trinh-review-3-codex-verdict.md => [('ops/reviews/phan-bien-quy-trinh-review-3-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/phan-bien-quy-trinh-review-4-codex-verdict.md => [('ops/reviews/phan-bien-quy-trinh-review-4-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/phan-bien-quy-trinh-review-5-codex-verdict.md => [('ops/reviews/phan-bien-quy-trinh-review-5-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-1-codex-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-2-codex-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-2-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-3-codex-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-4-codex-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-5-codex-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-6-codex-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-7-gpt6astra-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr455-bien-nhan-v2-review-8-gpt6astra-verdict.md => [('ops/reviews/pr455-bien-nhan-v2-review-8-gpt6astra-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr460-bien-nhan-v2-review-9-gpt6astra-verdict.md => [('ops/reviews/pr460-bien-nhan-v2-review-9-gpt6astra-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr493-review-5-codex-verdict.md => [('ops/reviews/pr493-review-5-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr526-review-3-codex-verdict.md => [('ops/reviews/pr526-review-3-codex-verdict.receipt.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/pr870-review-2-codex/VERDICT.md => [('ops/reviews/pr870-review-2-codex-verdict.receipt.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/reviews/pr870-review-3-codex/VERDICT.md => [('ops/reviews/pr870-review-3-codex-verdict.receipt.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/reviews/pr889-review-1-codex/VERDICT.md => [('ops/reviews/pr889-review-1-codex-verdict.receipt.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/reviews/pr889-review-2-codex/VERDICT.md => [('ops/reviews/pr889-review-2-codex-verdict.receipt.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/reviews/pr889-review-3-codex/VERDICT.md => [('ops/reviews/pr889-review-3-codex-verdict.receipt.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
ops/reviews/slice-b-c-review-2-codex-verdict.md => [('ops/reviews/pr896-review-4-legacy-caveats.yaml', 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC')]
ops/reviews/thu-hoi-lease-a1a-r2/luot2-VERDICT.md => []
ops/reviews/wp766-r1-g1-exec-review-1-codex/VERDICT.md => [('ops/reviews/wp766-r1-g1-exec-review-1-codex-verdict.receipt.yaml', 'VERDICT-KHAI-SAI-EXECUTION-SURFACE')]
```
- kết luận: KHÔNG PHẢI LỖI mới sau đối chiếu nguồn ở H8/H12. Các trường hợp chưa có caveat có đính chính prose (#849) hoặc không có nguồn đối lập để xác định sai surface (thu-hoi); không dùng chỉ một chuỗi trong finding để quy self-claim.

### HƯỚNG 8: Phân xử các tự khai surface còn lại bằng nguồn cùng lượt

- giả thuyết: Có caveat nhưng trỏ sai run/head/dòng; hoặc nhầm mô tả chung API và CLI.
- lệnh: `python3 review_evidence/surface_sources.py`
- output thật:
```text
pr832-wp831: runtime=1ff81cba41874a218b53275d3cdc1418 head=51ae5c095972611d2c6045bd81786a4fc7e9ca62 surface=codex_cli source_head_run_in_caveat=True
pr848-wp744: runtime=f65e544ef5d64ba7a1e0edb607edcf0a head=23bc189f28ea60f04ca1634b6fe66d02babf12ed surface=codex_cli source_head_run_in_caveat=True
pr862-wp748-r21: transcript=['OpenAI Codex v0.163.0', '--------', 'workdir: /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv21', 'model: gpt-6-astra', 'provider: openai', 'approval: never', 'sandbox: workspace-write [workdir, /tmp, $TMPDIR] (network access enabled)', 'reasoning effort: xhigh', 'reasoning summaries: none', 'session id: 01a157da-2170-7be2-b6d0-053fa8f91aec', '--------'] source_path_in_caveat=True
pr849 correction=measured — verdicts/wp748-r20-luot4-codex-transcript.txt va verdicts/wp748-r20-luot5-codex-transcript.txt (stderr day du cua CLI): dau tep "OpenAI Codex v0.163.0", model gpt-6-astra (model YEU CAU qua -m, CLI tu in; model THUC PHUC VU KHONG_DO_DUOC), provider openai, sandbox workspace-write, session id 01a15690-… (luot 4) / 01a15698-… (luot 5); prompt o verdicts/wp748-r20-luot4-prompt.md va verdicts/wp748-r20-luot5-prompt.md. Be mat THUC: Codex CLI (codex exec) chay trong container cloud cua phien executor, provider openai_codex; KHONG qua bo chot launcher nen KHONG co bien nhan run. Verdict tu ghi "hosted Codex shell tools (codex_service)" la LOI TU PHAN LOAI cua model, mau thuan voi dau tep CLI; ghi ca hai, tin dau tep (connector P1 #857 r4320578811).
pr849 luot4 header=['OpenAI Codex v0.163.0', '--------', 'workdir: /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv4', 'model: gpt-6-astra', 'provider: openai', 'approval: never', 'sandbox: workspace-write [workdir, /tmp, $TMPDIR]', 'reasoning effort: xhigh', 'reasoning summaries: none', 'session id: 01a15690-01c4-7483-bef6-3b1788213468', '--------']
pr849 luot5 header=['OpenAI Codex v0.163.0', '--------', 'workdir: /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv4/l5', 'model: gpt-6-astra', 'provider: openai', 'approval: never', 'sandbox: workspace-write [workdir, /tmp, $TMPDIR, /tmp/claude-0/-home-user-tra-luat/90305cb1-2842-509b-9816-acb554eadd20/scratchpad/rv4/src] (network access enabled)', 'reasoning effort: high', 'reasoning summaries: none', 'session id: 01a15698-9be5-7e30-800f-5db0cba8de91', '--------']
runtime_with_head_5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456=[]
runtime_with_head_b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb=[]
runtime_with_head_981b9ea1d4bfaa0511cfbc8d9bdee9d8c151c86f=[]
thu-hoi-lease-a1a-r2/luot2-VERDICT.md: no linked receipt and no runtime for its head in the 124 JSON records; cannot establish CLI-versus-service contradiction. Not counted as a mismatch finding.
ci-g5 luot5: surface=codex_cli self=dich vu Codex qua API va terminal tools caveats=['KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC']
no-p3-ho-so-exec-review-1-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
no-p3-ho-so-spec-review-1-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
no-p3-ho-so-spec-review-2-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
wp523-r14-review-1-codex-verdict.receipt.yaml desktop_receipt_surface=codex_desktop
wp678-exec-review-1-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
wp678-exec-review-2-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
wp678-exec-review-3-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
wp678-exec-review-4-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
wp698-exec-review-g2-1-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
wp698-exec-review-g2-2-claude-verdict.receipt.yaml subagent_declared_in_mode=True caveat=['SUBAGENT-CUNG-HO-REVIEW-DEFERRED']
receipt_surface_caveat_readme_pairs=24 all_exact_description_rows=False
direct_runtime_or_other_surface_checks=15 all_match=True
```
- kết luận: KHÔNG PHẢI LỖI mới. #849 đã có đính chính ngay trong hồ sơ; ca thu-hoi không có nguồn mâu thuẫn để kết luận surface. Chỉ ghi KHÔNG ĐO ĐƯỢC cho surface thật khi thiếu runtime, không tự chọn một tên.

### HƯỚNG 9: Đo lại mọi mốc lịch sử và đính chính chưa review của các receipt

- giả thuyết: Neo nhầm commit đầu, chép sai câu lịch sử hoặc chỉ sang sai lượt review tiếp.
- lệnh: `python3 review_evidence/states.py anchors`
- output thật:
```text
historical_scalar_fields=48 exact_original_text=35 all_creation_anchor_match=True
ancestry_measurements=176 all_rc0=True
next_review_corrections=8 all_sha_hash_header_match=True
{'source': 'ops/reviews/pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml', 'next': 'pr455-bien-nhan-v2-review-2-codex-verdict.md', 'sha': 'c595292cb63fb8c09d7d7b482cda20f9d5f0917f', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
{'source': 'ops/reviews/pr455-bien-nhan-v2-review-2-codex-verdict.receipt.yaml', 'next': 'pr455-bien-nhan-v2-review-3-codex-verdict.md', 'sha': 'cb212847375c2319fe0ccad3f7c00c90b870e3ba', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
{'source': 'ops/reviews/pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml', 'next': 'pr455-bien-nhan-v2-review-4-codex-verdict.md', 'sha': '4ef73e69d5f3c419634118983723355e25e38305', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
{'source': 'ops/reviews/pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml', 'next': 'pr455-bien-nhan-v2-review-5-codex-verdict.md', 'sha': '670071b700bd97a893d64393ffded0257957d0b3', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
{'source': 'ops/reviews/pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml', 'next': 'pr455-bien-nhan-v2-review-6-codex-verdict.md', 'sha': '5a78c150106ae381461354c77ba2023834330bbd', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
{'source': 'ops/reviews/pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml', 'next': 'pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md', 'sha': 'ca960160b477cd16346a293aaa8752772a9921d4', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
{'source': 'ops/reviews/pr896-review-1-codex-verdict.receipt.yaml', 'next': 'pr896-review-2-codex-verdict.md', 'sha': '8d56009a09af7b3ef93801df105f9483de212cc7', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
{'source': 'ops/reviews/pr915-review-1-codex-verdict.receipt.yaml', 'next': 'pr896-review-2-codex-verdict.md', 'sha': '8d56009a09af7b3ef93801df105f9483de212cc7', 'receipt_sha_match': True, 'header_sha_match': True, 'hash_match': True, 'absent_at_anchor_rc': 128}
```
- kết luận: KHÔNG PHẢI LỖI mới thuộc hai lớp săn. So byte lời diễn giải lịch sử không tự kết luận sai trạng thái; 12 trường wp678 diễn giải lại điều kiện cục bộ/đã đẩy và thời gian, 1 caveat pr508 diễn giải anchor.gioi_han tại mốc (ID caveat chưa có ở commit gốc). Chi tiết original/claimed trong historical-anchors.json; không gọi 48 trường là nguyên văn byte-exact.

### HƯỚNG 10: Quét lớp trạng thái review / áp hint / ancestry / merge

- giả thuyết: Câu phủ định hiện hành đã bị Git hoặc verdict mới bác bỏ.
- lệnh: `python3 review_evidence/states.py scan_status; git merge-base --is-ancestor; git ls-tree`
- output thật:
```text
negative_status_scalars=2203 readme_candidates=519
unreviewed_candidate 17f4a1b85b8d5146c5e6dddbdc40f11111a659f7 receipts=0 verdict_headers=0
unreviewed_candidate efa397eb2515658a1e3e9b4cdfd6e887b492b957 receipts=0 verdict_headers=0
unreviewed_candidate 99aef141796ebce7044c9f5c0c8a1a3b3d673d8e receipts=0 verdict_headers=0
unreviewed_candidate 5a96c1ac8cec1c9958094f92e716941faa47aac5 receipts=0 verdict_headers=0
unreviewed_candidate 888c0d9b68136f384068ecad8e286819bb175044 receipts=0 verdict_headers=0
unreviewed_candidate bf10fab792473bc69dd377c7445978950c4d77a0 receipts=0 verdict_headers=0
unreviewed_candidate 288ad3ea79ef94e061b649effe7bee2c7e2a0a9b receipts=0 verdict_headers=0
unreviewed_candidate b5b6aefa66a8ad037ff34430d0210f3b6873913f receipts=0 verdict_headers=0
unreviewed_candidate 3ddda026da41b0bb162a3785b93dbb953a298203 receipts=0 verdict_headers=0
ancestry 4bc94325e647ee5e32373f3af30b8f83b98a90fa master_rc=1 candidate_rc=1
ancestry 604b8d9a7c5948a9c0690312f1220830d545b52c master_rc=1 candidate_rc=1
ancestry 82359c4deec90edebbaebf9ab9d094902120b567 master_rc=1 candidate_rc=0
ancestry 2e4183bc2dc40e6bc306e377fc442ff0f405bbe0 master_rc=1 candidate_rc=0
ancestry 1a276a15192013fdb1e472db409133b53ac57944 master_rc=1 candidate_rc=0
ancestry d308b0b1bbcb0db2e1624e4eda6431f73ace453f master_rc=1 candidate_rc=0
ancestry 22382d8c800bed7b995d093cdcfdc206360d7fd4 master_rc=1 candidate_rc=0
ancestry 825dab1c8771113caeb3c5b77c61e89e27d7e292 master_rc=1 candidate_rc=0
ancestry 05bc12e2b9008071ca28edbd4574e58644d48220 master_rc=1 candidate_rc=0
ancestry 54021fb0a92eae606076606fc83431c486013bdd master_rc=1 candidate_rc=0
ancestry fb87110cfab832406984f893e6a4c79fbb932aef master_rc=1 candidate_rc=0
ops/specs/wp775.md ls-tree master='' candidate=''
ops/specs/wp484-r8.md ls-tree master='' candidate=''
ops/land/pr696-wp668-land-evidence.yaml historical_context="2026-09-30T10:53Z..11:37Z (worktree claude/bookkeeping-668 @ bc57bca, core.abbrev 7)"
ops/land/pr684-wp677-land-evidence.yaml historical_context="PROTOCOL §10: `landed` la trang thai cua PACKET (ma o exact SHA duoc duyet + hau-merge gate xanh + bookkeeping). PR #684 chi dua SPEC vao master; ma cua packet nam o PR #689 (TAI THOI DIEM merge #684: chua review xong, chua merge). Trang thai hien tai cua #689 KHONG doc tu tep nay. Packet #677 MO tai thoi diem ay. TAI THAO TAC MERGE #684 (~12:39Z): lease thi cong hieu luc la g3 (dot-bien-l-bien-cong-khai-exec-3-claude-20260929, commit d957b90), giu ops/lease_publish_test.py cho executor; ho so nay KHONG thu hoi lease nao. Sau merge (b): g3 bi thay bang g4 luc ~16:5xZ (ops/cap-lease-677-g2 c27a0a2, issues/677#issuecomment-5894685680). Ho so nay KHONG phai readback trang thai lease hien tai — hoi `ai-dang-giu`."
ops/land/pr554-wp541-land-evidence.yaml historical_context={"viec_cua_541_con_treo_luc_cap_nhat": ["Ho so land nay chua vao master — PR dang mo la buoc dau.", "Land authority chua duoc cap. Muc uy_quyen o tren van la XIN, chua la CO.", "Issue #541 van MO, `landed` chua duoc goi.", "PR #569 (bo do mot-tep) van draft.", "Comment human audit 5743814734 con 4 dong duoi do lop trung gian chen vao moi lan ghi (ca POST lan PATCH). 74 dong dau dung tung ky tu ban chu kho duyet. Chi sua duoc tu giao dien GitHub."]}
HINT applied 2e4183b parent_is_c8c1ee0=True
HINT applied 1a276a1 parent_is_77a0a45=True
```
- kết luận: KHÔNG PHẢI LỖI mới qua các đối chiếu này; âm tính về review chỉ có giá trị trong tập hiện vật, không chứng minh ngoài kho không có review. Mốc CAP_NHAT_1, do_luc, packet_landed_ghi_chu được xét theo cả khối; chưa land không được đồng nhất với chưa merge.

### HƯỚNG 11: Lời khai mới của receipt, README và khối land lượt 7

- giả thuyết: Sai số đếm, run/head, SHA manifest, bản chiếu hoặc mốc commit mới.
- lệnh: `python3 review_evidence/new_claims.py; sha256sum -c SHA256SUMS`
- output thật:
```text
{
  "verdict_bytes": 43635,
  "verdict_bytes_match": true,
  "verdict_sha256_match": true,
  "flat_original_byte_match": true,
  "header": [
    "verdict: changes_requested",
    "reviewed_sha: 05bc12e2b9008071ca28edbd4574e58644d48220",
    "Kết quả: 0 P0, 2 P1, 1 P2, 0 P3."
  ],
  "reviewed_tree_match": true,
  "runtime": {
    "run_id": "2ca2785d9e4d4c9ba14492dc17ac2276",
    "head": "05bc12e2b9008071ca28edbd4574e58644d48220",
    "execution_surface": "codex_cli",
    "transport": "machine",
    "ma_thoat": 0,
    "trang_thai": "xong",
    "worktree_sach": true,
    "thoi_luong_giay": 1144.447,
    "model_phuc_vu_trang_thai": "DO_DUOC"
  },
  "runtime_head_match": true,
  "prompt_sha_match": true,
  "model_events": {
    "count": 48,
    "unique_response_ids": 48,
    "models": [
      "gpt-6.1-sol"
    ]
  },
  "evidence_url_commit": "54021fb0a92eae606076606fc83431c486013bdd",
  "evidence_blob_byte_match": true,
  "stdout_hash_and_size_match": true,
  "stderr_hash_and_size_match": true,
  "caveat_readme_rows": [
    {
      "id": "HINT-LUOT7-AP-CUNG-COMMIT-GHI-SO",
      "rows": 1,
      "description_match": true
    },
    {
      "id": "LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI",
      "rows": 1,
      "description_match": true
    },
    {
      "id": "CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY",
      "rows": 1,
      "description_match": true
    },
    {
      "id": "SCRIPT-DO-DOC-DUONG-DAN-SANDBOX",
      "rows": 1,
      "description_match": true
    },
    {
      "id": "TEP-LON-KHONG-VAO-KHO",
      "rows": 1,
      "description_match": true
    }
  ],
  "artifact_manifest": {
    "rc": 0,
    "ok_count": 145,
    "errors": "",
    "non_ok_lines": []
  },
  "review_delta_files": 131,
  "receipt_added_at_current_sha": true,
  "land_receipt_head_verdict_match": true,
  "receipt_commit_parent": "54021fb0a92eae606076606fc83431c486013bdd",
  "artifact_commit_parent": "05bc12e2b9008071ca28edbd4574e58644d48220"
}
```
- kết luận: KHÔNG PHẢI LỖI.


### HƯỚNG 12: Loại trừ báo nhầm từ lời trích, quyết định land và mô tả lịch sử

- giả thuyết: Đọc câu lịch sử như trạng thái hiện hành, hoặc gọi bản tóm tắt là sai byte verdict.
- lệnh: `python3 review_evidence/context_checks.py`
- output thật:
```text
git merge-base --is-ancestor bc57bca 423b4ba rc=1 stderr=''
git merge-base --is-ancestor cc78b33 3ddda02 rc=0 stderr=''
git merge-base --is-ancestor cc78b33 refs/remotes/origin/ops/cap-lease-ci-g5-cong-cu-chia-manh rc=128 stderr='fatal: Not a valid object name refs/remotes/origin/ops/cap-lease-ci-g5-cong-cu-chia-manh'
pr896-review-4-legacy-caveats.yaml => don-nhanh-base-review-1-codex-verdict.receipt.yaml README rows=1 exact_description=True
pr896-review-6-legacy-caveats.yaml => doctor-github-mcp-review-6-codex-verdict.receipt.yaml README rows=1 exact_description=True
pr896-review-6-legacy-caveats.yaml => don-nhanh-base-review-4-claude-verdict.receipt.yaml README rows=1 exact_description=True
pr896-review-6-legacy-caveats.yaml => don-nhanh-base-review-5-claude-verdict.receipt.yaml README rows=1 exact_description=True
ops/land/pr714-wp710-provenance/readback-comment-6080353250.json: created_at=2026-10-09T11:55:41Z body_sha256=8bb668db60cc53e6676a712de1d7dd7dbf7a9689f786c8b4f6eda9e5bbc42bb8
VERDICT — human_audited · approve (ghi sau merge)
Reviewed commit: 888c0d9b68136f384068ecad8e286819bb175044
Review: Codex cross-review g3 lượt 1–3 (changes_requested) rồi g5 lượt 4–9; lượt 9 approve trên 6a8c8b5, 0/0/0 trong sáu tệp (pull/714#issuecomment-6078803297, VERDICT sha256 3524df2f…57fd). Bot Codex trên 888c0d9 hoàn tất 11:09:19Z, không góp ý.
PR đã merge lúc 11:08:11Z TRƯỚC khi có chữ ký này và trước khi bot Codex review xong 888c0d9 — tôi nhận đây là lệch quy trình, ghi lại thay vì coi như chưa xảy ra.
Còn mở: P3 huong-dan-cu-con-lech-sau-va-ngoai-write-set (bốn tệp ngoài write set, packet khác); linux-subreaper-khong-thu-hoi-zombie chưa có phép đo Linux độc lập executor; verdict/HINT lượt 4–9 gốc chưa nằm trong kho (phiên Windows đẩy lên ops/wp710-g5-hien-vat-review).
Khai thẳng phạm vi chữ ký: nó xác nhận "tôi đã đọc và chấp nhận", không phải một lượt dò tìm độc lập.
VERDICT: approve
new land block reviewed_sha=05bc12e2b9008071ca28edbd4574e58644d48220 verdict=changes_requested score=P0 0 / P1 2 / P2 1 / P3 0; con P1/P2 describes that historical review, with hint applied in same block
historical_descriptions_not_verbatim=13; 12 wp678, 1 pr508
pr508 anchor at a639e48: {"loai": "canonical_ancestry", "cuong_do": "trung_binh", "mo_ta": "Blob verdict ghim `9196eaf`. Head đã review là TỔ TIÊN của head nhánh packet (đo `git merge-base --is-ancestor`, cả 5/5 ⇒ CÓ).", "gioi_han": "YẾU HƠN các biên nhận `cao` trong thư mục này: PR #508 **CHƯA merge**, nên quan hệ tổ tiên mới chỉ trong NHÁNH, chưa tới `master` (đo: `HEAD` KHÔNG phải tổ tiên của `origin/master`). Quan hệ ấy chỉ bền nếu land bằng **merge commit hoặc fast-forward**; **squash phá nó** và làm cả 5 `reviewed_sha` thành SHA không tra được. Nâng lên `cao` được sau khi PR land đúng cách.", "pr": 508, "branch": "claude/handoff-tra-luat-repo-2ak5th", "reviewed_sha": "d81f1553c3bc340d1817e3247cdf3292691b720a", "reviewed_base": "b98531e256ea91e20f31b74ac6b9046e8fac8eed", "verdict_blob_commit": "9196eaf70ca0d908b8d23ff26512c4e395e1e997"}
3c7df6d678e11090a1623f871dcd484250a4b68b 2026-09-12T14:16:05+07:00 Merge pull request #508 — dac ta lane CI + packet #513 CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN
ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.md readme_rows=1 both_surface_names=True missing_run_json=True
ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.md readme_rows=1 both_surface_names=True missing_run_json=True
ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.md readme_rows=1 both_surface_names=True missing_run_json=True
ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.md readme_rows=1 both_surface_names=True missing_run_json=True
non_verbatim_README_caveats=['ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.md', 'ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.md', 'ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.md', 'ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.md']
```
- Giới hạn riêng: ref `refs/remotes/origin/ops/cap-lease-ci-g5-cong-cu-chia-manh` không tồn tại trong bộ ref cục bộ; phép so với ref này rc=128, **KHÔNG ĐO ĐƯỢC**, không được tính là pass hay finding. Các phép so OID cố định còn lại có rc thật như trên.
- kết luận: KHÔNG PHẢI LỖI. Sidecar sửa lời khai v1; human decision #714 tự nói không phải lượt dò tìm độc lập; bốn hàng ci-g5 diễn giải đủ hai lời khai và giới hạn runtime. Các câu trong cap_nhat_luot7 thuộc reviewed_sha 05bc12e, không tự khai service hoặc khẳng định bản vá tại fb87110 chưa áp.

### HƯỚNG 13: Kết luận dương N/N và giữ nguyên cây được review

- giả thuyết: Ca báo đạt nhưng thiếu tổng dương, hoặc cây nguồn đã bị đổi trong khi đo.
- lệnh: `python3 review_evidence/final_checks.py`
- output thật:
```text
t26: rc=0 conclusion=lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 positive_equal_counts=True
t27: rc=0 conclusion=lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 positive_equal_counts=True
t138: rc=0 conclusion=lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 positive_equal_counts=True
doc_claims rc=0 parsed_ok_is_true=True
flat_original_pairs=18 all_byte_match=True
$ git -C cay-kho rev-parse HEAD
rc=0
fb87110cfab832406984f893e6a4c79fbb932aef

$ git -C cay-kho rev-parse HEAD^{tree}
rc=0
a653c501d218f3b72590dc28433c8f78d00643c1

$ git -C cay-kho diff --exit-code
rc=0

$ git -C cay-kho status --porcelain=v1 --untracked-files=all
rc=0

required_checks_all_pass=True
```
- kết luận: KHÔNG PHẢI LỖI.

### HƯỚNG 14: Nguồn comment cùng lượt và các đính chính review kế tiếp

- giả thuyết: Caveat mới dẫn nhầm comment/run hoặc đính chính trạng thái chưa review dẫn sai head.
- lệnh: `python3 review_evidence/correction_sources.py`
- output thật:
```text
ops/land/pr823-wp802-provenance/readback-comment-6247520447.json id=6247520447 round5=True head5c6c7a8=True runb3d8a108=True
**Codex lượt 5/5: APPROVE** trên exact head `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` (PR #823). Không còn P0/P1/P2/P3 mở; F2 và F6 của lượt 4 đóng.
- Verdict: nhánh lease `ops/wp802-r1-g1-lease` @ `c25d0f8`, `ops/reviews/wp802-g1-luot5-codex-verdict.md` (launcher run `b3d8a108`, 1092s, `ma_thoat=0`). Lượt 1–4 ở cùng thư mục. Ghi chú: thông điệp commit `c25d0f8` ghi nhầm id run — id đúng là `b3d8a108`.
pr870 luot2: head=06a50c5feea77c2654f31edd26efeed7eeee62f5 expected_match=True verdict=approve header_match=True hash_match=True absent_at_anchor_rc=128
pr870 luot3: head=06a50c5feea77c2654f31edd26efeed7eeee62f5 expected_match=True verdict=approve header_match=True hash_match=True absent_at_anchor_rc=128
pr889 luot2: head=094e8d17ae4dfcf21dca63702c9262267bdc072c expected_match=True verdict=approve header_match=True hash_match=True absent_at_anchor_rc=128
pr889 luot3: head=094e8d17ae4dfcf21dca63702c9262267bdc072c expected_match=True verdict=approve header_match=True hash_match=True absent_at_anchor_rc=128
```
- kết luận: KHÔNG PHẢI LỖI.

## FINDING MỚI

Không có finding mới được xác lập trong hai lớp được giao; không tạo `HINT.patch`.

## GIỚI HẠN VÀ DẤU VẾT ĐO

- Không có run/transcript cùng lượt ở #823/#877 nên không thể xác nhận surface thật; bản vá đã ghi đúng giới hạn này. Trường hợp `thu-hoi-lease-a1a-r2/luot2-VERDICT.md` cũng thiếu nguồn cùng lượt, không đủ chứng cứ để kết luận có mâu thuẫn CLI/service.
- Không có tín hiệu `Codex home is inside a repository` trong ba ca/cổng đã chạy. Phép so một ref nhánh cũ ở H12 rc=128 được giữ là **KHÔNG ĐO ĐƯỢC**; không dùng nó để kết luận ancestry đạt. Các kết luận chính dùng OID cố định.
- Giới hạn “không có răng” của ca thử nằm trong BẢNG ĐO/H5; không quy ca kiểm băm, mục lục hoặc fixture admission thành phép kiểm đúng/sai của prose.
- Driver hướng 9 lần đầu rc=1 do giả định kiểu caveat lịch sử sai. Đã sửa driver và đo lại: 48 trường, 176 phép ancestry; giữ lần thử lỗi và mọi cập nhật tăng dần tại `review_evidence/VERDICT.progress.md`. Đây là lỗi bộ đo của reviewer, không phải lỗi cây được review.
- Tất cả lệnh/counter/raw stdout/stderr của các cổng giữ tại `review_evidence/`. Source HEAD cuối vẫn `fb87110cfab832406984f893e6a4c79fbb932aef`, tree `a653c501d218f3b72590dc28433c8f78d00643c1`, diff rỗng, status kể cả untracked rỗng. Không sửa `cay-kho/`, không push.
