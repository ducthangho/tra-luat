verdict: changes_requested
reviewed_sha: e9211317dadd365ed3efdb9a43eabe479ef54380

**KHÔNG CÒN P1 · KHÔNG CÒN P2 trong phạm vi review · CÒN 3 P3: 2 lớp B và 1 nợ lớp D.** Chưa đạt điều kiện dừng. Tôi áp dụng ngoại lệ người dùng cho phép approve nếu chỉ còn D; lý do `changes_requested` là **hai lỗi B có đối chứng**, không phải nợ D.

Reviewer: Codex/GPT-6 theo cấu hình phiên; provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`. Review độc lập với executor Claude theo chỉ thị được giao; không có chứng thực độc lập backend/model thực phục vụ. Không tự ghi transition `cross_approved` hoặc cấp quyền merge.

Base `27c413c3e531800431cad9db4452d7236505a5a9`; tree `7edca217a0b82f02ece023eeb5976343e0b82591`. Chỉ đọc kho `cay-kho/`; chạy cổng và phản chứng trên các bản sao `review12-current/`, `review12-merge/`, `review12-probes/`. Tất cả scratch/TMPDIR nằm trong workspace; không dùng mạng, không tự soạn chuỗi tấn công đường dẫn. Thêm thư mục actionlint 1.7.7 vào **cuối** PATH, ghim `core.abbrev=7` bằng môi trường khi chạy cổng.

Bằng chứng tự chạy: [measurements.json](review12-evidence/measurements.json), [gates.json](review12-evidence/gates.json), [merge.json](review12-evidence/merge.json), [probes.json](review12-evidence/probes.json), [extra.json](review12-evidence/extra.json), [final-measures.json](review12-evidence/final-measures.json). Script và stdout cùng thư mục. Không nhận output lượt trước làm số đo lượt này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — tự chạy lại ba mutant độc lập tại nội dung exact head: heading r358 `1016→1017`, heading r360 `5→6`, phép trừ `13 − 2 = 11→12`. Mỗi mutant đổi đúng **1 byte**, giữ **891730 byte** CHANGELOG. Cả ba claims `rc=0/ok=true`, cả ba release `rc=2`, failed chỉ CHANGELOG. Đây là nợ D được phép giữ theo chỉ thị lượt này; không dùng nó một mình để yêu cầu sửa tiếp.
- `runtime-pr491-luot2-mat-nhan-khi-chieu`: **ĐÃ VÁ THẬT** — `ops/land/pr491-r358-ghi-so-land-evidence.yaml:105–118` có `canh_bao_doc_ket_qua` ngay sau hàng kết quả: bốn scalar `714,268 s`, `rc=0`, `worktree_sach`, `so_muc_ban` được xếp **ATTESTATION** từ run.json ngoài kho; **0 P1** được tách riêng là đếm heading, SHA đối chiếu Git. Tự đếm verdict lượt 2: **0/3/10**; SHA bằng cha thứ hai của `00e017a`. Nhãn mới **không quá rộng**: không kéo số finding, SHA hay băm verdict xuống hạng runtime. Chú thích :123–126 nói rõ các số cổng lịch sử vẫn là lời ghi nhận thiếu stdout gốc, còn hành vi cổng có thể chạy lại. Tôi không dùng một lần chạy hôm nay để chứng thực lần chạy lịch sử.

Tổng hai slug lượt 11: **1 ĐÃ VÁ THẬT · 1 CHƯA VÁ**. Hai finding B bên dưới thuộc hai vị trí khác; không gọi chúng là lỗi mới do việc gắn nhãn runtime.

## VÉT LỚP B TRÊN NĂM BẢN CHIẾU

**Phép liệt kê “ĐẦY ĐỦ = năm” không đủ cho việc vét lớp B.** Danh sách ấy nêu được năm nơi chứa bản chiếu, nhưng chưa phân loại đúng mọi trường trong PR. Một tệp có thể là nguồn của metadata lần chạy, đồng thời là bản chiếu của verdict/hồ sơ khác.

Hai receipt là ví dụ đo được: `so_p1/so_p2/so_p3`, phân hoạch P3, `doi_chieu_luot_1`, `no_con_lai`, `verdict_usage_caveats` đều chiếu từ verdict hoặc hồ sơ điều phối; không trở thành nguồn gốc chỉ vì tệp có `nguon_cac_scalar_tren`. Receipt lượt 1 còn chiếu hồ sơ pr477 ở `ba_p1_va_thu_dieu_phoi_TU_DO_LAI_truoc_khi_va[2].dieu_phoi_do_lai` và **bỏ giới hạn nguồn**, nêu ở finding thứ hai. Đây là bản chiếu thứ sáu cụ thể người dùng yêu cầu tìm; receipt lượt 2 cũng có các trường bản chiếu, dù các trường đã đối chiếu của nó khớp.

Tập vét thực dụng ở cấp nơi chứa là **bảy**: CHANGELOG (bao cả r358 sửa và r360), land evidence, README, thân PR, thông điệp commit, **hai receipt**. Trong mỗi nơi phải phân loại theo trường/mệnh đề. Hai verdict nguyên văn vẫn là đối chứng không sửa; manifest là tệp sinh. Các bản chép ngoài kho và BANG_KHANG_DINH không phải finding độc lập của cùng một lỗi.

| nơi đã vét | phép đối chiếu và kết quả |
|---|---|
| CHANGELOG r360 và các hunk r358 | Runtime hai lượt có nhãn riêng, số P đúng; 5 đối tượng không bị gọi thành 5 finding đóng sạch; phân hoạch 8+1+1 được ghim là lịch sử. Inventory 13 vị trí và hai đường P3/tổng không còn dùng 4/2 làm kết luận hiện hành. **Hàng lượt 10 mới điền sai phân hoạch và tổng slug**, xem finding. r358 đã giữ “được cho là cùng một job” ở :1199–1203. |
| Land evidence | Hàng runtime đã vá thật; Git, số finding và scalar thiếu log được tách. Các sự kiện API có nhãn đầu tệp; metadata phiên là tự khai, không xác thực danh tính. Không tìm thấy thêm một scalar runtime mất nhãn như lượt 11. |
| README | Hai hàng pr491 :308–309 giữ nhãn toàn khối runtime và tách Git/băm/byte/số heading; 2 hàng mục lục và 9 cảnh báo khớp receipt. Không còn hàng pr489 nguyên văn trùng. Con số 11 mang giới hạn attestation ngay trong hàng. |
| Thân PR | Số Git/gói và 14/13 finding khớp nguồn. Bảng gate ghim **a4bc01d**, có phân biệt head PR **4af7e29**; không lấy 49/102 lịch sử làm số của e921131. Phần hai lượt là tóm tắt chọn lọc đã ghim, không chấm là sai chỉ vì chưa nối tới 11. Chỉ dẫn vét vẫn ghi `CHANGELOG · ops/** · thân PR` (:88), chưa mở cụm; xử lý cùng vấn đề phạm vi quét bên dưới. |
| Thông điệp commit | Trích Git byte-exact. e921131 khai năm số merge đúng. f6df7fb mô tả bản vá runtime đúng, nhưng lặp phép loại receipt khỏi “năm bản chiếu”. Các message 025c6b2/9349bb0/cc21507 còn lời cũ đã được r360 đính chính có neo; không đòi viết lại lịch sử Git. |
| Receipt 1 và 2, mở thêm từ phép kiểm danh sách | Băm, severity, 7/1/0/6, 5+1, 8+1+1 và chín caveat khớp trong phạm vi nêu dưới. **Receipt 1 :57 vẫn bỏ “được cho là cùng một job”**; receipt 2 :80 lại nhắc đúng lỗi ấy. |

Không xem nhãn “tóm tắt” là giấy phép chép sai số: khác với việc không nối dài bảng, hàng lượt 10 **đã điền** kết quả trái nguồn.

## SOI HIỆN VẬT SẼ SỐNG TRONG KHO

**Land evidence — từng hạng nguồn:**

| trường/nhóm | tự đo hoặc giới hạn | kết quả |
|---|---|---|
| `p1_theo_luot`, `luot_cuoi` | Regex **heading** `^### .*\[P[123]\]` trên hai verdict: lượt 1 = 3 P1+5 P2+6 P3; lượt 2 = 0+3+10 | `{1:3,2:0}`, tổng14/13, changes_requested khớp. Regex mọi token được hồ sơ gợi ý cũng cho cùng số trên hai tệp này; không suy nó luôn tương đương đếm heading. |
| `doi_chieu_luot_truoc` | Đếm từng dòng slug với trạng thái in đậm trong verdict2 :12–25 | 7 ĐÃ VÁ THẬT +1 VÁ HỜ +0 VÁ SINH LỖI MỚI +6 CHƯA VÁ =14; đúng đơn vị trạng thái slug. |
| `authorized_head_sha`, `reviewed_sha`, `khop_head_da_merge` | `git show -s --format=%P 00e017a` | Cha thứ hai đúng `2ec6171f7a2e21ae950633f9e328329a355f7a6d`. |
| Land evidence thứ bảy | `git ls-tree -r --name-only 00e017a ops/land/` | Đúng6 tệp trước khi thêm. |
| Commit đầu chứa verdict | `git log --diff-filter=A`; `git diff-tree 34e9d35` | Đúng34e9d35, chỉ thêm hai verdict, chưa có hai receipt. |
| Runtime reviewer | Nhãn :105–118; đối chiếu receipt2 | Đúng hạng ATTESTATION; **KHÔNG ĐO ĐƯỢC** thời lượng/exit/trạng thái sạch lịch sử vì thiếu run.json. |
| Cổng pre/post-merge | Chú thích :123–126 và tự chạy các cổng ở head hiện tại | Phân biệt lời ghi nhận lịch sử với khả năng tái chạy. Các output lịch sử 121/121 không phải lời khai146/146 ở head mới. Không chứng thực lần chạy lịch sử không log. |
| Sự kiện GitHub, approval, CI, actor/thời gian merge, bot, sửa thân PR | Giới hạn nguồn đầu tệp và các cảnh báo cụ thể | **KHÔNG ĐO ĐƯỢC độc lập**: không raw response/readback lịch sử, không mạng. Phép cộng bước/thời lượng tính lại được nhưng không xác thực sự kiện. |
| Metadata provider/session/chỉ thị chủ kho/model | Hồ sơ tự khai; `model_da_chay: KHONG_DO_DUOC`; cảnh báo PAT | Không coi là chứng thực danh tính, authorization hoặc backend. |
| Bookkeeping “11 còn sống lúc merge” | 13 heading lúc review, hai P2 thân PR được điều phối khai đã sửa | Khớp số học có điều kiện; **KHÔNG ĐO ĐƯỢC 11 finding thực còn sống** tại merge vì không có raw body/readback PR491 lúc đó. |

Không thấy thêm lỗi mất nhãn attestation trong land evidence sau bản vá này. Việc metadata được khai trong hồ sơ không biến nó thành chứng thực độc lập; câu trả lời này không cấp authority cho các sự kiện ấy.

**Hai verdict nguyên văn:**

| tệp | byte | SHA-256 | lịch sử |
|---|---:|---|---|
| pr491-review-1-codex-verdict.md | 35088 | `38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c` | 0 commit M; blob đầu bằng byte hiện tại |
| pr491-review-2-codex-verdict.md | 36958 | `14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468` | 0 commit M; blob đầu bằng byte hiện tại |

Cả hai khớp `verdict_bytes/verdict_sha256`; commit thêm đầu tiên là `34e9d35be0fc52406e3659bfc24c388bf54262cd`. `git log --diff-filter=M -- <tệp>` đều rc0, stdout rỗng. Không thấy sửa một byte kể từ khi vào lịch sử đi tới reviewed head. Không xác thực quá trình sinh văn bản trước khi vào Git.

**Hai receipt, t26/t27 và chín caveat:** suite146/146 đạt, gồm t26 băm và t27 quan hệ hàng. Tự kiểm riêng 2/2 hàng mục lục chứa cùng verdict+receipt, 9/9 hàng cảnh báo chứa cùng verdict+ID. Cổng chỉ kiểm quan hệ/băm, không kiểm chân trị lời diễn giải.

| lượt / caveat ID | dòng README | đối chiếu nội dung |
|---|---:|---|
| 1 / HEAD-LUOT-1-KHONG-PHAI-HEAD-DA-MERGE | 37 | ba4a258 khác2ec6171; đúng giới hạn không gán finding head cũ cho master. |
| 1 / SAU-P3-KHONG-DEU-MOT-LOAI-5-cong-1 | 38 | Đọc6 heading P3:5 độ phủ +1 giới hạn cổng; verdict1 :183–188 có ghi nhận dương. |
| 1 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | 39 | Phù hợp giới hạn tự khai của verdict; không chứng thực model yêu cầu là model phục vụ. |
| 1 / phan-cong-CAM-tu-soan-phan-chung | 40 | Khớp phạm vi cấm được verdict thuật lại; không suy không có lỗ từ việc không thử. |
| 2 / changes_requested-KHONG-phai-chua-dat-dieu-kien-dung | 32 | Đúng verdict2 :4:0P1 thỏa điều kiện lịch sử tới hếtP1, vẫn changes_requested. |
| 2 / HET-P1-khong-phai-HET-FINDING-11-con-song-luc-merge | 33 | 13−2=11=1P2+10P3 **nếu** haiP2 thânPR đã sửa. HaiP2 đúng địa chỉ verdict2 :133/:140; phần sửa là attestation, không đếm được từ13 heading. |
| 2 / NAM-FINDING-BOT-la-duong-THU-BA-ba-cai-MOI | 34 | Receipt liệt kê5, có3 mới/2 trùng; hai slug trùng nối được verdict. Git hỗ trợ cặp hash/byte gói; sự kiện bot, review ID và trạng thái#490 **KHÔNG ĐO ĐƯỢC độc lập**. Không cộng11+5. |
| 2 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | 35 | Khớp giới hạn model/build/effort của verdict2 :6. |
| 2 / phan-cong-CAM-tu-soan-phan-chung | 36 | Verdict2 :8 khai cấm; :25/:186 thuật mutant1016/35/revision9. Phân biệt đột biến nội dung với payload bị cấm. |

ID có số11 nhất quán với bookkeeping có điều kiện; không có bằng chứng để thay11 bằng13 hoặc xác nhận11 là phép đo trạng thái merge thật. Riêng bản chiếu nguồn bị sót nằm **ngoài chín caveat**, ở receipt1 :57, nên t26/t27 xanh không đóng nó.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/base | e921131/27c413c | SHA đầy đủ nêu đầu; ancestry rc0 | Có |
| First-parent27c413c..HEAD | chuỗi vá/merge |19 commit;4 merge nhập master:7e236cf,dd4a3ae,9e78e19,e921131 | Có |
| Master tiến từ c00c88a |4 commit |`rev-list --count c00c88a..27c413c`=4 | Có |
| Bản vá lượt11 | tách khỏi merge |b43d4ab→f6df7fb:3tệp,+48/−8 | Đo riêng |
| Phần nhập master | chỉ manifest xung đột |f6df7fb→e921131:7tệp,+1724/−5; tái merge chỉ manifest conflict | Có |
| Toàn PR so base mới | numstat.txt |8tệp,+1690/−26; cộng các cột numstat đúng | Có |
| Patch/numstat/messages | trích Git |4/4 byte-exact | Có |
| Sáu slice CHANGELOG | cắt heading thật |6/6 byte-exact; đầu mục1/98/199/385/940/1060 | Có |
| Bốn bản chép YAML/README | chép từ cây |4/4 byte-exact | Có |
| ARTIFACTS.sha256 | băm gói |3313/3313 khớp | Có |
| Ref snapshot |324/324/324, lệch0 |baTSV bằng nhau;324refs/heads cục bộ | Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Bảng trích |2914 dòng |chạy lại12input byte-exact;2914không rỗng,1848có số | Có trong tập input |
| Thứ tự r |364→363→361→360→359→358→356 |đúng7heading đầu, giảm dần | Có |
| Số r trùng |0 |0 trong tập heading dev-side | Có |
| Hàng cảnh báo |267 |267 theo bảng chính | Có |
| Hàng mục lục |109 |109 theo bảng chính | Có |
| Hàng nguyên văn trùng |0 |0 ở mỗi bảng | Có |
| Nội dung r364 | không bị nuốt |nguyên byte so27c413c; các mục master khác trừ r358 cũng nguyên byte | Có |
| Hàng master được bảo toàn | auto-merge |0hàng master thiếu; cảnh báo258+9=267 và264+3=267; mục lục107+2=109 | Có |
| Manifest tái sinh | không giải tay |tự chạy release-manifest --deterministic:rc0,byte-exact manifest giao | Có về kết quả |
| LandP1 |3/0 |heading3/0;14/13tổng | Có |
| Hai verdict |35088/36958 và băm |2/2khớp;0commitM | Có |
| t26/t27 |2biên nhận,9caveat |2hash,2hàngmục lục,9cặp verdict/ID đúng hàng | Có |
| Bảng cross-review1–11:severity | các bộP1/P2/P3 |11/11khớp | Có |
| Các ô đối chiếu đã điền | nguồn verdict từng lượt |hàng2/3/6/7/8/9khớp; **hàng10sai** | Không tại hàng10 |
| Hàng10 đối chiếu |7/2/0/1,tổng10 |**3/1/0/1,tổng5** | **Không** |
| “Năm bản chiếu đầy đủ” | loại hai receipt |receipt chứa nhiều trường chiếu từ nguồn khác;receipt1:57sót nhãn | **Không** |
| `python3 -B ops/bien_nhan_v2.py` |0vi phạm sau commit |rc0;56v2+11legacy+42nợ=109;0vi phạm,0KHÔNGĐOĐƯỢC | Có |
| `python3 -B ops/lease_publish_test.py` |146/146 |rc0;146/146,đã chạy146,bỏ0 | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` |xanh180/180 |rc0;ok=true;180/180;haihash match;failed/extra/required_missing/errors=[] | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` |xanh |rc0;ok=true;flags=[];còn advisories | Có trong hợp đồng cổng |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` |rc0 |rc0;7tệp,0chỗchépdoctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` |rc0 |rc0;46ADR/46hàng,khớp1–1;tha thiếu trạng thái0016 như output khai | Có |
| Merge chưa commit |2vi phạm,pr500,neod100b6f |rc1;đúng2receipt,54v2/tổng109 | Có |
| Cùng cây,HEAD merge commit |0vi phạm |rc0;56v2/tổng109 | Có |
| Đảo về trạng thái trước | cùng cơ chế |rc1;đúng2vi phạm trở lại | Có |
| Mutant1016→1017 |nợD |claims0/true;release2/false,chỉCHANGELOG | Chưa đóng |
| Mutantheading5→6 |nợD |claims0/true;release2/false,chỉCHANGELOG | Chưa đóng |
| Mutant13−2=11→12 |nợD |claims0/true;release2/false,chỉCHANGELOG | Chưa đóng |
| Kho được review sạch |read-only |status0byte trước/sau;các bản control/probes cũng sạch sau khôi phục | Có |

**Chi tiết hai cách đếm bảng:** parser reviewer lấy bảng liên tục đầu tiên dưới heading thích hợp; parser độc lập gom các khối hàng liên tục rồi nhận bằng header cột. Cả hai ra267/109,0trùng. Tôi cũng thử `_bang` của bộ test: nó trả124 cho cả section Mục lục vì còn gom15hàng bảng phụ dưới đó. Không dùng124 làm số hàng bảng chính; không gọi đây là mất nội dung hay finding mới. Script đo đầu tiên của reviewer từng đếm nhầm bảng phụ cuối section; đã sửa trước kết luận, số cuối có đối chứng độc lập.

**Tái hiện merge và ý nghĩa cổng:** trên bản sao checkout f6df7fb, `git merge --no-commit --no-ff 27c413c` rc1, chỉ `RELEASE_MANIFEST.json` conflict. Điền manifest exact reviewed tree và stage: `git write-tree` bằng `7edca217…`. `d100b6f` không là tổ tiên HEAD cũ(rc1), là tổ tiên MERGE_HEAD và e921131(rc0/0). Cổng đỏ2. Chỉ đổi HEAD sang commit merge đã có, bỏ MERGE_HEAD: cổng xanh0. Đảo lại: đỏ2. Cây index trước/sau vẫn bằng exact tree. Đây là tái dựng, không phải transcript nguyên thủy của executor.

**Có phải khuyết tật cổng?** Có sự lệch đối tượng nếu dùng nó như cổng kiểm *prospective merge*: đọc receipt từ working tree nhưng kiểm ancestry của HEAD cũ (`ops/bien_nhan_v2.py:809–822`). Đó là giới hạn áp dụng cần ghi rõ. Tuy nhiên, hợp đồng hiện hành chủ ý kiểm HEAD, thông báo đỏ nói chính xác “không phải tổ tiên của HEAD”, và tree không có ancestry riêng. Tôi **không xác nhận một khuyết tật P3 mới của hợp đồng kiểm commit** chỉ vì hiện tượng lặp lần thứ tư; không có false-green trên commit được review. Muốn tiền kiểm merge phải nhận commit ứng viên có đủ hai cha hoặc báo rõ chưa đo được pha ấy; không sửa bằng cách nhận mọi object tồn tại hay OR mù với MERGE_HEAD. “Commit rồi đo” không đòi publish/ghi kho thật: một commit ứng viên cục bộ là đủ.

Không chạy CI từ xa, Windows/macOS native hoặc full selftest sản phẩm; không tính chúng là pass. Phạm vi PR là tám tệp hồ sơ/manifest. Không thể xác nhận trạng thái PR trên máy chủ hiện tại từ gói offline.

### doi-chieu-luot10-chep-nham-hang-luot9  [P3]  Hàng lượt 10 vừa bổ sung chép kết quả đối chiếu của lượt 9
LỚP: B
TỆP/DÒNG: CHANGELOG.md:647; bản chép `muc-r360.md:263`; nguồn `VERDICT-LUOT-10.md:16–24`, năm heading finding của `VERDICT-LUOT-9.md`.
VẤN ĐỀ: Hàng10 ghi 7 ĐÃ VÁ THẬT / 2 VÁ HỜ / 0 VÁ SINH LỖI MỚI / 1 CHƯA VÁ, còn chú thích “đối chiếu 10 slug lượt 9”. Tự parse đúng phần ĐỐI CHIẾU của verdict10 cho 5 slug: 3/1/0/1; tập ID đúng bằng 5 finding lượt 9. Dữ liệu 7/2/0/1 là kết quả của verdict 9 đối chiếu 10 slug lượt 8, đã nằm ở hàng ngay trên. Đây là chép nhầm nguồn khi điền ô mới ở f6df7fb, không phải yêu cầu nối dài một bảng chọn lọc. Nó làm sai chính phép đo hội tụ và phóng số đóng thật 3→7.
CÙNG LỚP CÒN Ở ĐÂU: Hàng ngoài kho và dòng BANG_KHANG_DINH tương ứng là bản sao, không tính thêm. Đã so tất cả 11 bộ severity và các ô đối chiếu có số; chỉ ô này lệch nguồn. Message f6df7fb nói lượt11còn2P3 là đúng, không chép phân hoạch sai này.
ĐÃ THỬ VÁ: có — thử trên bản sao: giữ nguyên SHA/severity lượt 10, thay ô thành 3/1/0/1, “đối chiếu 5 slug lượt 9”. Hint ở `review12-evidence/row10-hint.txt`, chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit. Nguy cơ vá: đếm mọi chữ trạng thái trong văn xuôi hoặc lấy verdict 11 đối chiếu 3 slug làm nguồn; phải đếm từng dòng slug của đúng verdict 10. Khi ghi thật cần tái sinh manifest.
ĐÃ THỬ NGHIỆM: `python3 review12-evidence/probes.py`: tập 5 ID bằng finding lượt 9; phép so đầy đủ 4 ô và tổng trả **false với hàng cũ, true với hàng sửa**. Claims trên bản sửa rc0/ok=true; baseline sai cũng xanh. Không viết test sản phẩm chỉ để kiểm ô văn bản này.
ĐỘ TIN: cao

### receipt-pr491-luot1-chieu-cap-run-mat-gioi-han-nguon  [P3]  Biên nhận bị loại khỏi bộ vét vẫn chép cặp run chắc hơn nguồn
LỚP: B
TỆP/DÒNG: ops/reviews/pr491-review-1-codex-verdict.receipt.yaml:53–59; phép loại khỏi tập vét tại CHANGELOG.md:864–868 và message f6df7fb. Nguồn `ops/land/pr477-dung-goi-review-land-evidence.yaml:156–166`; đính chính đã có tại CHANGELOG.md:1199–1203 và receipt lượt2:80.
VẤN ĐỀ: Trường `dieu_phoi_do_lai` viết “Cặp 43/1→44/6 thuộc run 34176439015”. Nguồn chỉ **thuật lại hai mẫu được cho là của cùng một job**, thiếu response trước/sau để đối chứng job/attempt. Receipt2 thậm chí đã chiếu đúng finding rằng câu “thuộc run” chắc hơn nguồn; r358 được sửa theo đó nhưng receipt1 giữ nguyên. Nhãn đầu receipt1 và `nguon_cac_scalar_tren` chỉ phủ runtime reviewer từ run.json, không phủ các mẫuCI của PR477. Việc đọc được con số trong một tệp không chứng minh hai mẫu thuộc cùng job/run thực. Đây là lỗi bảo toàn giới hạn nguồn, không phải chứng minh số run sai.

Phép liệt kê mới gọi hai receipt là NGUỒN nên loại chúng khỏi mọi bản chiếu là nguyên nhân bộ vét tiếp tục bỏ vị trí này. Ngay tên trường `reviewer_khai`/`dieu_phoi_do_lai` và các trườngseverity/caveat cho thấy cần mở từng trường; không thể phân loại một lần cho toàn tệp.
CÙNG LỚP CÒN Ở ĐÂU: `receipt-luot1.yaml:57` và dòng trích là cùng một bản sao. Receipt2 và r358 đã giữ đúng giới hạn; không chấm lại chúng. Thân PR:88 và r360:687–689 còn chỉ dẫn vét bằng cụm `ops/**`; khi sửa inventory phải cập nhật hướng dẫn liên quan, bao cảr358 và hai receipt. Message lịch sử f6df7fb cần đính chính có neo, không viết lại commit.
ĐÃ THỬ VÁ: có — tạo candidate ngoài kho `review12-evidence/receipt1-hint.yaml`: thêm “Theo hồ sơ điều phối… được cho là của cùng một job… thiếu response trước/sau để đối chứng job/attempt”, giữ nguyên hai số run và CHƯA XÁC ĐỊNH. Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit. Đồng thời sửa mô tả tập vét thành phân loại theo trường, đưa hai receipt vào; không gắn ATTESTATION cho băm verdict/Git/sốheading đo được. Nguy cơ vá là kéo toàn bộ trường xuống tự thuật hoặc chỉ sửa danh sách mà để nguyên câu mất giới hạn.
ĐÃ THỬ NGHIỆM: `python3 review12-evidence/extra.py` lưu nguyên văn YAML nguồn/đích; `python3 review12-evidence/final-measures.py` parse candidate thành công, giữ caveat vàhashanchor, giữ hai ID run / CHƯA XÁC ĐỊNH; giới hạn “được cho là” vắng ở trường cũ, có ở candidate. Đối chứng source/receipt 2/r358 xác nhận đây là giới hạn có thật bị bỏ. **KHÔNG ĐO ĐƯỢC** danh tínhjob/attempt thực vì không response gốc. Suite 146/146 và v2 xanh trên trường sai không kiểm được ngữ nghĩa này.
ĐỘ TIN: cao

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Ba sai số vẫn sống qua cổng claims
LỚP: D
TỆP/DÒNG: CHANGELOG.md:577–590,871–877; điểm đột biến:385,698,1060; mã `scripts/tl_core/workflow.py` trong `_doc_claims_check`.
VẤN ĐỀ: Ba mutant giữ kích thước vẫn claims0/true; release chặn băm lệch. Nợ đã khai, ngoài tám tệp diff, không được đóng bởi một bản sửa lời diễn giải. **Nợ này không chặn approve một mình theo ngoại lệ rõ ràng của người dùng lượt12.**
CÙNG LỚP CÒN Ở ĐÂU: các đoạn nợr360, receipt2 phầnP3, thânPR và messageb43d4ab; chúng khai nợ đúng, không tính thành lỗiB riêng.
ĐÃ THỬ VÁ: không sửa mã cổng. Hướng successor: ràng buộc từng loại mệnh đề với nguồn Git/verdict/phép tính trong workflow.py; control xanh, ba mutant đỏ, trích dẫn số sai lịch sử đã rút không bị coi là mệnh đề hiện hành. Nguy cơ: hard-code ba số hoặc coi băm đúng là chân trị đúng.
ĐÃ THỬ NGHIỆM: `python3 review12-evidence/probes.py`:3/3 mutant đổi 1 byte, giữ 891730 byte; claims rc0/ok=true, release rc2/ok=false,failed chỉ CHANGELOG,package_hash_match=false; khôi phục byte gốc trong finally, bản sao sạch.
ĐỘ TIN: cao
