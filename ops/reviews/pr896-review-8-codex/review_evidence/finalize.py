from measure import *
import shutil
path=BASE/'VERDICT.md'; accumulated=path.read_text();(OUT/'VERDICT.progress.md').write_text(accumulated)
# Keep the final measurement for each direction; retain all earlier attempts in the progress artifact.
blocks={}
for m in re.finditer(r'(?ms)^### HƯỚNG (\d+):.*?(?=^### HƯỚNG \d+:|\Z)',accumulated):blocks[int(m[1])]=m[0].strip()
blocks[7]=blocks[7].replace('ĐANG PHÂN LOẠI các trường hợp không có caveat; không dùng chỉ một chuỗi trong finding để quy self-claim.','KHÔNG PHẢI LỖI mới sau đối chiếu nguồn ở H8/H12. Các trường hợp chưa có caveat có đính chính prose (#849) hoặc không có nguồn đối lập để xác định sai surface (thu-hoi); không dùng chỉ một chuỗi trong finding để quy self-claim.')
blocks[2]='\n'.join(l for l in blocks[2].splitlines() if 'KHÔNG neo đầu dòng là' not in l)
blocks[11]=blocks[11].replace('\n- Tiến độ hướng 9:', '\n- Tiến độ hướng 9:')
# The failed-driver progress note was appended between H11 and H9; report it once separately.
blocks[11]=re.sub(r'\n- Tiến độ hướng 9:.*', '', blocks[11],flags=re.S)
blocks[12]=blocks[12].replace('- kết luận:', '- Giới hạn riêng: ref `refs/remotes/origin/ops/cap-lease-ci-g5-cong-cu-chia-manh` không tồn tại trong bộ ref cục bộ; phép so với ref này rc=128, **KHÔNG ĐO ĐƯỢC**, không được tính là pass hay finding. Các phép so OID cố định còn lại có rc thật như trên.\n- kết luận:')
pre='''verdict: approve
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

'''
notes='''

## FINDING MỚI

Không có finding mới được xác lập trong hai lớp được giao; không tạo `HINT.patch`.

## GIỚI HẠN VÀ DẤU VẾT ĐO

- Không có run/transcript cùng lượt ở #823/#877 nên không thể xác nhận surface thật; bản vá đã ghi đúng giới hạn này. Trường hợp `thu-hoi-lease-a1a-r2/luot2-VERDICT.md` cũng thiếu nguồn cùng lượt, không đủ chứng cứ để kết luận có mâu thuẫn CLI/service.
- Không có tín hiệu `Codex home is inside a repository` trong ba ca/cổng đã chạy. Phép so một ref nhánh cũ ở H12 rc=128 được giữ là **KHÔNG ĐO ĐƯỢC**; không dùng nó để kết luận ancestry đạt. Các kết luận chính dùng OID cố định.
- Giới hạn “không có răng” của ca thử nằm trong BẢNG ĐO/H5; không quy ca kiểm băm, mục lục hoặc fixture admission thành phép kiểm đúng/sai của prose.
- Driver hướng 9 lần đầu rc=1 do giả định kiểu caveat lịch sử sai. Đã sửa driver và đo lại: 48 trường, 176 phép ancestry; giữ lần thử lỗi và mọi cập nhật tăng dần tại `review_evidence/VERDICT.progress.md`. Đây là lỗi bộ đo của reviewer, không phải lỗi cây được review.
- Tất cả lệnh/counter/raw stdout/stderr của các cổng giữ tại `review_evidence/`. Source HEAD cuối vẫn `fb87110cfab832406984f893e6a4c79fbb932aef`, tree `a653c501d218f3b72590dc28433c8f78d00643c1`, diff rỗng, status kể cả untracked rỗng. Không sửa `cay-kho/`, không push.
'''
path.write_text(pre+'\n\n'.join(blocks[n] for n in sorted(blocks))+notes)
print('verdict=approve counts=0/0/0/0 directions='+str(len(blocks))+' bytes='+str(path.stat().st_size));print('HINT.patch exists='+str((BASE/'HINT.patch').exists()));print('source_status='+repr(git('status','--porcelain=v1','--untracked-files=all').decode()))
