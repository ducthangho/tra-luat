verdict: changes_requested
reviewed_sha: a4bc01dc45520629cb889da506a10925a3ecd2b0

**KHÔNG CÒN P1; KHÔNG CÒN P2 trong phạm vi review; CÒN 9 P3. Điều kiện “tới hết P3” CHƯA ĐẠT.** Đối chiếu 10 slug lượt 6: **4 ĐÃ VÁ THẬT · 3 VÁ HỜ · 2 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Sáu slug còn mở và ba finding mới được trình bày bên dưới; không đếm bản chiếu của cùng lỗi thành finding riêng.

Reviewer: Codex/GPT-6 theo cấu hình phiên, provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`; khác executor Claude theo hồ sơ được giao. Không chứng thực độc lập model/backend. Authority và điều kiện dừng lấy từ chỉ thị trực tiếp lượt 7. Đây là cross-provider review theo §8, không tự ghi state `cross_approved`, không cấp quyền merge.

Exact tree: `2e318548b571502e9a39389b7f16da52f397ced7`. `cay-kho/` detached, không shallow, sạch trước và sau đo; chỉ đọc cây này. Cổng chạy trên `review-current/`, đột biến trên `review-mutant/`, đối chứng lịch sử trên `review-state/`; tất cả trong workspace. Không mạng, không tự soạn payload đường dẫn. `TMPDIR` trong workspace, `core.abbrev=7` qua cấu hình môi trường của các phép đo; thư mục actionlint 1.7.7 được thêm vào **cuối** PATH.

Bằng chứng tái lập: `review-evidence/measure.py`, `run.py`, `probes.py`, `extra.py`; kết quả tương ứng `measurements.json`, `gates.json`, `probes.json`, `extra.json`, cùng stdout/stderr `.out`. `r359-classification.tsv` phân loại từng hit trong phép vét 74 dòng. Dòng `CHANGELOG.md` dưới đây tính trong `cay-kho/`; `muc-r360.md` có cùng số dòng. Các tên hiện vật khác tính từ workspace.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `tu-thu-tron-hai-tap-nam-finding`: **ĐÃ VÁ THẬT** — thân PR:86 nay viết “để SÓT ít nhất một bản chiếu”, thừa nhận sửa cả README lẫn receipt. Tự `git diff 4af7e29 9484970 -- ops/reviews/README.md ops/reviews/pr491-review-2-codex-verdict.receipt.yaml` thấy cả hai tệp thay đổi. CHANGELOG:235–241 dẫn đúng lượt 3=P2, lượt 4=P3, khớp heading hai verdict gốc. Phân biệt tập A/B vẫn giữ đúng; không mở lại lỗi đã đóng.
- `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`: **VÁ HỜ** — thân PR:72 đã gắn nhãn thiếu log cho đúng hai gạch đầu dòng:73–75. Nhưng khối nháp riêng CHANGELOG:139–146 vẫn không có nhãn hay chỉ dẫn tới nhãn ở:298. Đo delta lượt 6→7: đoạn ấy chỉ đổi cách gọi số lịch sử `r359`; chưa sửa điểm còn lại được lượt 6 chỉ đích danh. Nháp “tám”, sự kiện lần thứ hai và khôi phục 806980/806981 vẫn KHÔNG ĐO ĐƯỢC vì thiếu hiện vật gốc.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — CHANGELOG:175–179 nay khai rõ nợ chưa đóng, cổng tương lai, mã ngoài write set; đó là đính chính phạm vi có thật. Tuy nhiên phép thử đóng finding không đổi: trên bản sao exact head, ba mutant riêng biệt, mỗi ca đổi đúng một byte, đều claims `rc=0, ok=true`; release trên ca 1016→1017 `rc=2`, chỉ CHANGELOG thất bại. Không gọi nợ đã khai đúng là cổng đã sửa, cũng không coi PR đã được phép sửa mã ngoài write set.
- `doi-so-r-con-sot-ban-chieu`: **ĐÃ VÁ THẬT** — các chỉ dẫn hiện hành đã đổi sang `r360`/“mục này”. Sáu dòng còn `r359` trong r360 là:14 (va chạm),22,23,29,30 (mục master),141 (số lịch sử có nhãn). Thân PR còn hai dòng:13,75, cả hai nói rõ số ban đầu. Toàn bộ `rg -n 'r359' *.md` trước khi tạo verdict có 74 dòng: 59 ở verdict lịch sử, 6 ở r360, 2 ở thân PR, 5 ở prompt, 1 tên hiện vật trong EVIDENCE, 1 heading master. Từng hit đã phân loại trong TSV; “sáu hit” đúng cho r360, không phải toàn bộ gói. Chỉ dẫn tới một mục không tồn tại trong thân PR là finding mới riêng bên dưới.
- `phan-vai-khai-duy-nhat-vuot-noi-dung`: **VÁ SINH LỖI MỚI** — đã bỏ lượng từ “duy nhất”. Nhưng CHANGELOG:28–31 nay nói cả hai mục cùng kể “#490 đã land” và không mâu thuẫn. Đọc nguyên mục master:90–100 thấy chính nó ghi **#490 dừng ở merged, không phải landed**, hậu-merge gate chưa đủ bằng chứng. Trong ba mục được liệt kê thêm, phạm vi 39 tệp/range và quyết định đóng chuỗi khớp; trạng thái land không khớp. Không chấm thêm lỗi chỉ vì phép đếm chủ đề không có đơn vị duy nhất; chấm mệnh đề trạng thái bị nguồn phủ định.
- `va-cham-r-ke-sai-thoi-diem-cu`: **VÁ SINH LỖI MỚI** — tự đọc `git show 22b6339:CHANGELOG.md` và `git show cacaba3:CHANGELOG.md`: đúng là hai heading r355 khác nội dung đã tồn tại trước merge. `git diff bc78656^1 bc78656` xác nhận đổi 3 chỗ trong CHANGELOG và 4 chỗ launcher_test, kể cả r355b→r356b. Nhưng suy tiếp “cùng thời điểm phát hiện”, “tức … bị phát hiện lúc merge” ở:16–19 không được hai blob chứng minh. Git xác nhận thời điểm sửa đã ghi nhận; không xác nhận lần đầu người vận hành nhận ra va chạm. Bản vá thay một lời kể thời điểm không có nguồn bằng lời kể khác.
- `hien-vat-nam-luot-khong-khop-write-set`: **ĐÃ VÁ THẬT** — heading và mở đầu:1–11 nay tách hiện vật hai lượt PR491 khỏi phần tóm tắt PR493. Tự `git ls-tree -r --name-only HEAD ops/reviews/`: có đúng 2 verdict + 2 receipt pr491 được thêm bởi PR; **0 pr493-review-***. Nội dung PR493 trong mục là tóm tắt chọn lọc: bảng kết quả chi tiết vẫn chỉ có lượt 1–3, các lượt 4–6 được nhắc trong phần diễn giải. Không đọc lời “tóm tắt” thành cam kết chứa nguyên văn sáu verdict.
- `than-pr-khai-so-cong-cua-head-cu`: **VÁ HỜ** — cặp 49/102 tại thân PR:100 khớp phép chạy trên a4bc01d. Nhưng tiêu đề bảng:92 vẫn là “trên head này”, không ghim nhánh nháp/SHA đang đo. Theo trạng thái PR do người dùng và EVIDENCE giao, GitHub head vẫn 4af7e29; tự chạy tại SHA đó được **43/96**. Gói giao reviewer đã khai lệch, còn chính thân PR độc lập chưa khai. Sai số đã được thay bằng đúng số của nhánh khác mà chưa sửa phạm vi của bảng.
- `bo-sot-khang-dinh-moi-trong-commit`: **ĐÃ VÁ THẬT** — tự sinh `git log --format='%H%n%B%n---' c31d8f1..HEAD`: khớp nguyên byte `thong-diep-commit.txt`, gồm 11 commit, không chỉ hai message được gọi tên. Chạy bộ trích với 9 input theo header bảng: output byte-exact, 367 dòng không rỗng của message có mặt; cả “6 vi phạm”, “49 ĐẠT v2”, “tổng 102” đều có. Đọc cả đoạn sáu anchor và kết luận, không chỉ ba từ khóa. Đây là cách chữa tổng quát cho message trong range, không phải chèn ba chuỗi. **Không** đóng toàn bộ lớp “mọi metadata Git”: notes, thông điệp tag, metadata ngoài range không được xuất bởi lệnh này. Không thấy một khẳng định PR cụ thể còn bị thiếu từ những nguồn đó để chấm thêm P3; docstring cũng không hứa bao phủ chúng.
- `mo-ta-bo-trich-va-no-khong-theo-kip-ban-va`: **VÁ HỜ** — CHANGELOG:196–206 và thân PR:68 đã ghim phân hoạch cũ vào lịch sử và thu hẹp đúng điều kiện regex. Nhưng **docstring thật** `trich_khang_dinh.py:7–8` vẫn viết “moi menh de dinh luong viet BANG CHU bi vut sach”. Tự kiểm dòng113 của r358: “ba lần lặp” cùng `t33`, `re.search(r'\d', dòng)` trả True. Đây chính là phản ví dụ cũ còn nguyên, không phải finding mới do suy diễn. Lời executor “docstring đã bỏ” không khớp hiện vật được giao.

## BẢNG ĐO

“Khớp” chỉ áp cho đại lượng có nguồn đo tương ứng. Hash không chứng nhận provenance; phép trừ đúng không chứng nhận hai số hạng là dữ liệu thật.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/tree | a4bc01d | a4bc01dc45520629cb889da506a10925a3ecd2b0 / 2e318548b571502e9a39389b7f16da52f397ced7; detached, full history, sạch | Có |
| Delta so c31d8f1 | 8 tệp hồ sơ | Lệnh awk được yêu cầu trên numstat: **8 tep, +1431/-26** | Có |
| Write set | CHANGELOG, manifest, land, README, 2 verdict, 2 receipt | Đúng 8 đường dẫn, không có mã cổng | Có |
| Delta lượt 6→7 | sửa hồ sơ | Chỉ CHANGELOG và manifest; thân PR/script là hiện vật ngoài cây | Có |
| Hai patch, numstat, message | trích Git | Cả 4 tệp khớp nguyên byte output Git | Có |
| Heading/slice | r360/r359/r358 | Heading dòng 1/312/432; cả 3 slice byte-exact | Có |
| Bốn bản chiếu trong cây | land, README, receipt1/2 | 4/4 byte-exact | Có |
| Ancestry base | master c31d8f1 đã vào head | `merge-base --is-ancestor c31d8f1 HEAD`: rc0 | Có |
| First-parent PR | chuỗi ghi sổ và sửa | 11 commit: 34e9d35, cdd0b1d, 4af7e29, 9484970, fae2fb7, b004da9, f5098dd, 7e236cf, 2c57e99, cdd5891, a4bc01d | Có |
| Master đi trước từ 00e017a | 17 commit | `rev-list --count 00e017a..c31d8f1`=17 | Có; không phải 17 merge first-parent |
| Phạm vi r359 | 39 tệp, c0a5cbe..8cee941 | `git diff --shortstat`=39 tệp,+7834/−9 | Có |
| Phạm vi r358 | 1016 tệp,+247458 | `git diff --shortstat b416830 c0a5cbe`=1016,+247458 | Có |
| Hai số hạng gói r358 | 8075509→8089302, bcde19d5→d47be343 | Tự đọc manifest tại c0a5cbe và 2ec6171: khớp cả hai byte count và hai hash | Có |
| Manifest head | 180 tệp, tổng 8132226 | CHANGELOG 837904 byte; package hash f6e1bf8881c692cb58a11ff1476918f81a1eeb10a8126652bf1da1372ca5cac7 | Có |
| ARTIFACTS.sha256 | toàn vẹn hiện vật | 3265/3265 khớp | Có; không chứng minh nguồn GitHub |
| Ref snapshot | 319/319/319, lệch0 | So **tập tên+OID** của 3 TSV và Git heads: đều319, bằng nhau | Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Phạm vi ref | chỉ có snapshot heads | Có tag trong object store, nhưng không có snapshot server tags để so | Khớp giới hạn; không hiểu thành “kho không có tag” |
| Bộ trích | 2103 dòng,0 loại | 259+97+200+77+210+156+214+523+367=2103 dòng không rỗng;1341 có số; output byte-exact | Có trong 9 input |
| Ba chuỗi commit-only | đã vào bảng | Cả3 có; toàn bộ367 dòng không rỗng của11message được xuất | Có |
| Nối dòng | đơn vị vẫn là dòng | Cụm “3 chỗ trong CHANGELOG + 4 chỗ trong launcher_test.py” (giữ backtick quanh tên tệp) không khớp raw, khớp sau `re.sub(r'\s+',' ',s)` | Có giới hạn được tự khai; không phải dòng nguồn bị mất |
| Lịch sử PR493 lượt1–6 | số findings các lượt | Đếm heading: 1/4/12;1/4/15;0/2/15;0/1/15;0/0/14;0/0/10; SHA khớp cả6 | Có trong gói |
| PR491 P1 theo lượt | {1:3,2:0} | Đếm heading hai verdict:3/5/6 và0/3/10, tổng14/13 | Có, đo độc lập được |
| Verdict1 hash/byte | 35088,38d7fb2e… | 35088;38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c | Có |
| Verdict2 hash/byte | 36958,14c726e5… | 36958;14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468 | Có |
| Commit đầu chứa verdict | 34e9d35 | `git log --diff-filter=A` trả cùng OID đầy đủ cho cả2 | Có |
| t26/t27 | băm và mục lục+caveat | Control PASS/PASS; đổi byte verdict làm t26 AssertionError LỆCH BĂM; đổi ID ô cảnh báo làm t27 AssertionError đúng caveat | Có cả hai chiều |
| Caveat PR491 | 4+5,9 hàng đúng verdict | Parse receipt và ô bảng:9/9 cùng hàng đúng tên verdict và ID | Có |
| ID “…11-con-song-luc-merge” | 13−2=11 | 13 finding đo từ verdict;2 `da_va` theo receipt; ID/README khớp11 | Số học có; hai sửa thân PR lịch sử KHÔNG ĐO ĐƯỢC, đã gắn nhãn attestation |
| Bien_nhan head | 49/102,0vi phạm | rc0;49v2+11legacy+42nợ=102;0vi phạm,0KHÔNG ĐO ĐƯỢC | Có |
| Bien_nhan master | 47/100 | Chạy trên c31d8f1: rc0,47/100 | Có |
| Bien_nhan GitHub head trong gói | 4af7e29 | Chạy trên4af7e29: rc0,43/96; thân PR lại49/102 mà không ghim draft SHA | Không khớp phạm vi “head này” |
| release strict | ok,180/180 | rc0;expected=checked=180;hai hash_match=true;failed/extra_files/errors=[] | Có |
| doc-claims strict | ok | rc0,ok=true | Có trong phạm vi cổng |
| lease suite | 121/121 | rc0,121/121;đã chạy121,bỏ0; actionlint hiện diện | Có |
| doctrine/ADR | rc0/0 | rc0/0;7tệp,0chép;46ADR/46hàng, khớp1–1 | Có |
| Ba mutant số | vẫn xanh | Mỗi ca đổi1byte,giữ837904byte; cả3 claims rc0,ok=true | Có; nợ cổng vẫn mở |
| Một mutant byte | release chặn | rc2;hash_match=false;failed chỉCHANGELOG, cùng size837904 | Có |
| Sáu anchor#490 | đúng trên master, sai trên head trước merge | Cả6: rc1 trênf5098dd,rc0 trênc31d8f1 vàhead | Có |
| Sáu lỗi do trạng thái đo | cây merge,HEAD chưa merge | Cùng cây tệp7e236cf: đặtHEAD=f5098dd⇒rc1,đúng6lỗi ancestry;HEAD=7e236cf⇒rc0,0lỗi | Có cơ chế; không chứng nhận transcript phiên gốc |
| Va chạm cũ | hai cha đã cór355;đổi3+4 | Hai blob xác nhận;diff đổi đúng3chỗCHANGELOG+4chỗlauncher | Có các số hạng |
| Thời điểm phát hiện va chạm | cùng lúc merge | Blob/commit không ghi thời điểm lần đầu nhận ra | KHÔNG ĐO ĐƯỢC |
| Ba phần chồng lấn thêm | 39tệp,#490land,đóngchuỗi | Hai phần phạm vi/đóngchuỗi khớp; r359 phủ định landed#490 | Không |
| Land evidence đếm theo mốc | trước6;master mới7 | ls-tree00e017a=6,c31d8f1=7,head=8; thêm pr491 ởPR này | Có; “thứ bảy” trong hồ sơ là thứ tự lịch sử, không tổng ởhead |
| #491 ngoài chuỗi đóng | không sinh mắt xích cho#490 | pr489:416–452 miễn PR evidence cho chính#490; #491 là ghi sổ đối tượng khác | Khớp phạm vi văn bản; không tự chứng thực chỉ thị gốc |
| CI/approval lịch sử | sốrun/job,thời lượng,người duyệt | Không raw response/log,không mạng | KHÔNG ĐO ĐƯỢC độc lập |
| Số học CI |44;biênWindows10m51 |40+4=38+6=44;3600−2949=651s;so705s hẹp54s | Có số học; không kiểm được số hạng runtime |
| Lỗi printf | format bắt đầu bằng“-” bị bác | `bash --noprofile --norc -c` với nội dung vô hại:rc2,stdout rỗng,invalid option;format `%s`⇒rc0,nội dung đủ | Có cơ chế |
| Comment lịch sử |29793→27683,hụt2110,4dòng mất |29793−27683=2110;verdict6 trong gói26029byte,không phải hai comment payload cần đo | KHÔNG ĐO ĐƯỢC hai số hạng/nội dung comment |
| Endpoint MCP | chỉ3tool comment,không sửa được | Không có inventory của endpoint/session ấy trong gói | KHÔNG ĐO ĐƯỢC |
| Thân PR đọc ngược | GitHub chứa bản được giao | Không mạng/response thô | KHÔNG ĐO ĐƯỢC provenance; đã review nội dung snapshot |

Giới hạn GitHub không làm review exact draft SHA bị blocked: người dùng đã chỉ định rõ đối tượng a4bc01d và cho phép review offline. Việc cố ý chưa push cũng không tự là một finding. **Lỗi P3 là thân PR không mang theo sự phân biệt ấy**, nên độc giả GitHub nhận số đo của nhánh nháp dưới tên head hiện hành. Trước khi dùng verdict cho một transition, phải đối chiếu exact head theo §8; verdict này không review thay 4af7e29.

Không tìm thấy căn cứ để coi evidence #491 là mắt xích thứ bảy bị cấm: văn bản đóng chuỗi miễn riêng PR kế nhiệm cho #490, không cấm ghi sổ lần land của một PR khác. Đồng thời không dùng điều đó để nâng trạng thái #490 thành landed. Những command xanh ở bảng cũng không chứng nhận toàn bộ CI đã chạy; trạng thái CI thật vẫn KHÔNG ĐO ĐƯỢC.

### hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap  [P3]  Khối nháp “tám” vẫn đứng ngoài nhãn nguồn
TỆP/DÒNG: CHANGELOG.md:139–146,298–303; than-pr-493.md:72–75.
VẤN ĐỀ: Bản chiếu thân PR đã sửa đúng, nhưng khối tự thuật nháp ở CHANGELOG vẫn kể số nhóm, nguyên nhân cộng nhầm và “lần thứ hai” như sự kiện không kèm giới hạn. Nhãn ở cuối dưới heading khác không tự phủ khối riêng này. Đây là phần còn sống mà lượt 6 đã chỉ ra.
ĐÃ THỬ VÁ: không — gắn nhãn tự thuật thiếu log hoặc dẫn rõ nhãn chung ngay tại khối139–146. Kiểm mọi bản chiếu sau nối dòng; giữ riêng Git facts. Nguy cơ sửa: kéo cả dữ kiện Git đo được xuống attestation bằng một nhãn quá rộng.
ĐÃ THỬ NGHIỆM: đọc `git diff 2c57e99 a4bc01d -- CHANGELOG.md` và snapshot thân PR. Khối nháp chỉ đổi cách gọi sốr; KHÔNG ĐO ĐƯỢC sự kiện cũ vì không có nháp/transcript.
ĐỘ TIN: cao về lỗi gắn nhãn; không kết luận lời kể là giả.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Tiêu chí đóng nợ cổng vẫn chưa đạt
TỆP/DÒNG: CHANGELOG.md:168–179; write set trong numstat.txt.
VẤN ĐỀ: Lời khai nợ đã trung thực hơn, nhưng ba phản chứng của finding lượt 6 vẫn xanh. Điều kiện người dùng là tới hếtP3, không phải tới lúc mọi P3 được ghi thành nợ. Không phải lỗi mới do PR này gây ra; là finding được yêu cầu theo dõi mà chưa có thay đổi hành vi.
ĐÃ THỬ VÁ: có — thử ba mutant riêng trên bản sao và khôi phục sau từng ca; không sửa mã cổng. Cách đóng về hành vi: successor có write set phù hợp kiểm các khẳng định bằng dữ liệu Git/verdict có nguồn, giữ control xanh và làm cả ba mutant đỏ. Nguy cơ sửa: hard-code ba số hoặc kiểm nhầm câu trích dẫn lịch sử thay vì mệnh đề hiện hành. Không tự mở rộng PR hồ sơ này để vá mã.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/probes.py`;1016→1017,heading5→6,13−2=11→12: mỗi ca1byte,837904byte,cả3claims rc0/ok=true. Release cađầu rc2,failed chỉCHANGELOG.
ĐỘ TIN: cao.

### phan-vai-khai-duy-nhat-vuot-noi-dung  [P3]  Đoạn phân vai gán “landed #490” cho nguồn phủ định landed
TỆP/DÒNG: CHANGELOG.md:14,28–31; muc-r359-cua-master.md:90–100; thong-diep-commit.txt:49–52.
VẤN ĐỀ: Câu “cũng kể #490 đã land … cả ba đều có trong r359” sai ở chính trạng thái nó gán cho nguồn. r359 nói rõ “merged, không phải landed”, chưa đủ bằng chứng hậu-merge gate. Vì vậy câu tiếp theo “không phải kết luận mâu thuẫn” cũng sai. Ba phần liệt kê không phải ba mệnh đề đều khớp: phạm vi và quyết định đóng chuỗi có, landed không có.
ĐÃ THỬ VÁ: không — đổi trạng thái sang merged tại bản hiện hành và đính chính message bằng văn bản có neo commit, không viết lại lịch sử. Kiểm các hit#490 kèm merged/landed trên hai mục sau nối dòng. Nguy cơ sửa: đổi ngược cả lời chỉ thị lịch sử “cho phép land” hoặc làm mất phân biệt ủy quyền với trạng thái đã đạt.
ĐÃ THỬ NGHIỆM: hai slice byte-exact; đọc r359:90–100 và ADR-0034:17–21. Git xác nhận merge8cee941, không cung cấp hậu-merge gate còn thiếu.
ĐỘ TIN: cao.

### va-cham-r-ke-sai-thoi-diem-cu  [P3]  Hai cha đã có mục không chứng minh lúc đầu phát hiện va chạm
TỆP/DÒNG: CHANGELOG.md:16–19; thong-diep-commit.txt:44–47.
VẤN ĐỀ: Hai blob chứng minh mục đã viết trước merge; diff chứng minh đổi số được ghi ở merge. Chúng không đo được sự kiện “phát hiện”, càng không chứng minh “cùng thời điểm … không khác”. Người vận hành có thể đã nhận ra trước khi ghi commit hòa giải. Lượt 6 cũng đã cảnh báo không suy thời điểm tâm lý từ message.
ĐÃ THỬ VÁ: không — chỉ khẳng định hai mục đã tồn tại và đổi số được ghi trong bc78656; nếu giữ sự kiện nhận ra thì gắn nhãn tự thuật thiếu log. Ca khóa: đối chiếu mỗi mệnh đề với blob/diff hay transcript tương ứng. Nguy cơ sửa: tiếp tục dùng thời gian commit làm thời gian nhận thức/sự kiện shell.
ĐÃ THỬ NGHIỆM: `git show 22b6339:CHANGELOG.md`, `git show cacaba3:CHANGELOG.md`, `git log -5 bc78656^1`, `git diff bc78656^1 bc78656 -- CHANGELOG.md .claude/dev/launcher_test.py`; headingr355 cảhai,đổi3+4 đúng. Thời điểm nhận ra: KHÔNG ĐO ĐƯỢC, không transcript.
ĐỘ TIN: cao về giới hạn chứng cứ; không khẳng định thời điểm kể là sai thực tế.

### than-pr-khai-so-cong-cua-head-cu  [P3]  Số của nhánh nháp vẫn được gắn nhãn head PR
TỆP/DÒNG: than-pr-493.md:92–100; EVIDENCE.md:57–60.
VẤN ĐỀ: Cập nhật43/96→49/102 đúng cho drafta4bc01d nhưng không đúng headGitHub4af7e29 trong trạng thái được giao. Snapshot thân PR không ghi a4bc01d, tên nhánh nháp hay lời báo lệch bên cạnh bảng. Người chỉ đọc PR không có EVIDENCE của gói để giải mã “head này”.
ĐÃ THỬ VÁ: không — ghim bảng cổng vào SHA đầy đủ và nói rõ headPR chưa được đẩy tới đó; khi push cuối cùng thì đối chiếu lại. Ca khóa: đọc thân PR độc lập và kiểm testSHA/PRhead/branch. Nguy cơ sửa: ghim nhãn rồi để số tiếp tục trôi theo lần push kế tiếp. Không cần push mỗi lượt để sửa lời khai này.
ĐÃ THỬ NGHIỆM: `python3 -B ops/bien_nhan_v2.py` trên bản saoa4bc01d⇒49/102;4af7e29⇒43/96,đều rc0. Tìm trong thân PR không thấy a4bc01d. GitHub live KHÔNG ĐO ĐƯỢC vì cấm mạng; dùng trạng thái chụp được người dùng giao, không giả đã hỏi API.
ĐỘ TIN: cao trong trạng thái gói được giao.

### mo-ta-bo-trich-va-no-khong-theo-kip-ban-va  [P3]  Docstring vẫn giữ nguyên lượng từ bị bác ở lượt 6
TỆP/DÒNG: trich_khang_dinh.py:6–11; CHANGELOG.md:202–206; thong-diep-commit.txt:56–60.
VẤN ĐỀ: Docstring thật vẫn nói mọi mệnh đề định lượng bằng chữ bị vứt sạch. Đó không phải cách regex cũ hoạt động: một dòng có chữ số khác được giữ. CHANGELOG đã giải thích đúng ngay phản ví dụ này, nên bản giao gồm hai lời mô tả trái nhau. Thêm input message không chữa docstring.
ĐÃ THỬ VÁ: không — sửa chính docstring thành “bỏ các dòng không có chữ số”; vét cả hướng dẫn và message đính chính theo đơn vị mệnh đề. Ca khóa: một dòng chỉ có định lượng bằng chữ và một dòng cùng định lượng ấy có `t33`; bộ lọc cũ chỉ loại dòng đầu. Nguy cơ sửa: nhầm bỏ dòng trắng với mất khẳng định, hoặc biến kiểm đủ9input thành hứa phủ mọi nguồn.
ĐÃ THỬ NGHIỆM: chạy bộ trích mới tái tạo2103dòng; `re.search(r'\d', muc-r358 dòng113)`=True dù chứa “ba lần lặp”. Lời docstring hiện tại đọc trực tiếp từ tệp, không suy từ message nói đã sửa.
ĐỘ TIN: cao.

### printf-khai-do-duoc-khong-co-payload-goc  [P3]  Bài học mới gắn nhãn đo được cho comment không có hiện vật
TỆP/DÒNG: CHANGELOG.md:278–284,298–303; thong-diep-commit.txt:2–9,19–21.
VẤN ĐỀ: Tiêu đề “ĐO ĐƯỢC” và “đo hai chiều” áp cho29793byte dự tính,27683byte đã đến, bốn dòng mất và mục rỗng. Gói không có hai payload hay response đọc ngược. Tái hiện lỗi format chỉ chứng minh cơ chế, không chứng minh comment lịch sử chứa gì. Nhãn “TỰ THUẬT, KHÔNG CÓ LOG” bên dưới lại chỉ giải thích nháp/checkout cũ, không giải quyết sự đối lập với tiêu đề đo được của câu mới. Số2110 chỉ là hiệu hai số tự khai.
ĐÃ THỬ VÁ: không — tại chính đoạn mới, tách cơ chế shell tái hiện được khỏi sự kiện comment thuật lại; hoặc giao payload trước/sau cùng response có neo commentID để reviewer so byte/nội dung. Ca khóa: đo riêng hai số hạng và bốn dòng, không chỉ hiệu. Nguy cơ sửa: dùng verdict26029byte làm payload comment, hoặc coi comment đính chính là response của comment bị hụt.
ĐÃ THỬ NGHIỆM: probe vô hại `printf` dạng format bắt đầu dấu trừ⇒rc2,stdout rỗng; dạng `%s`⇒rc0,nội dung đủ. KHÔNG ĐO ĐƯỢC29793/27683 và mục rỗng do thiếu hiện vật; verdict lượt6 có26029byte, không đủ để suy hai giá trị kia.
ĐỘ TIN: cao về thiếu nguồn/nhãn; không kết luận sự kiện là bịa.

### ket-luan-thieu-tool-khong-co-inventory  [P3]  Liệt kê ba tool không chứng minh endpoint không có cách sửa comment
TỆP/DÒNG: CHANGELOG.md:294–296; thong-diep-commit.txt:18–21.
VẤN ĐỀ: “endpoint MCP của kho chỉ có … không có công cụ sửa comment” là kết luận về toàn bộ năng lực endpoint/session, không phải lời “phiên này chưa tìm thấy”. Gói không có inventory/discovery response, tên phiên bản endpoint hoặc log phép thử làm căn cứ cho lượng từ “chỉ”. Ba tên được liệt kê đều là thao tác thêm, nhưng từ đó không suy ra tập công cụ đã được vét cạn. Không khẳng định ngược rằng endpoint ấy chắc chắn có tool sửa.
ĐÃ THỬ VÁ: không — thu hẹp thành khả năng phiên đã tìm thấy, ghi đây là tự thuật; nếu cần kết luận vắng công cụ thì kèm inventory đầy đủ có mốc và tiêu chí tìm. Ca khóa: so tập tool thực sự được công bố thay vì ba tên đã nhớ. Nguy cơ sửa: dùng inventory một endpoint/phiên hiện tại để chứng minh phiên lịch sử.
ĐÃ THỬ NGHIỆM: đọc toàn đoạn và message; gói không có inventory của endpoint tương ứng. KHÔNG ĐO ĐƯỢC khả năng endpoint lịch sử, không mạng; không sử dụng bộ tool của phiên reviewer làm đối chứng cho phiên executor.
ĐỘ TIN: cao về phép suy vượt nguồn; chưa biết chân trị của việc endpoint thiếu tool.

### than-pr-tro-muc-va-cham-khong-ton-tai  [P3]  Chỉ dẫn giải thích đổi số trỏ tới mục vắng trong thân PR
TỆP/DÒNG: than-pr-493.md:13.
VẤN ĐỀ: Câu “xem phần Va chạm số r dưới” chỉ tới một phần không tồn tại trong snapshot thân PR. Phần đó ở CHANGELOG:13, không ở phía dưới trong PR. Đổi số chính đã đúng, nhưng đường dẫn đọc để kiểm lý do đổi số vẫn sai địa chỉ.
ĐÃ THỬ VÁ: không — dẫn rõ tới CHANGELOG mục r360 bằng đường dẫn/anchor có thật, hoặc đưa đoạn cần dẫn vào thân PR. Ca khóa: kiểm từng chỉ dẫn “trên/dưới/xem mục” với heading của chính bản chiếu. Nguy cơ sửa: anchor bị trôi khi đổi số tiếp hoặc dẫn tới nhánh master chưa có r360.
ĐÃ THỬ NGHIỆM: đọc tất cả heading của than-pr-493.md; không có phần Va chạm số r; cụm ấy chỉ xuất hiện trong câu chỉ dẫn. CHANGELOG có phần tương ứng ở:13.
ĐỘ TIN: cao.

**Kết luận exact SHA: 0 P1 · 0 P2 · 9 P3; changes_requested.** Cổng đã chạy đạt nhưng không chứng minh toàn bộ lời khai đúng. Không sửa kho thật, không đăng review, không push hoặc merge.
