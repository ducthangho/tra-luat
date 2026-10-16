verdict: approve
reviewed_sha: f5098dd69e1f998f81165734340b500f0940034b

**KHÔNG CÒN P1; KHÔNG CÒN P2 trong phạm vi đã review. Điều kiện “tiếp tục tới hết P2” ĐÃ ĐẠT.** Còn **14 P3**: 13 nợ chưa vá và một lỗi dẫn sai mức độ lịch sử phát sinh khi sửa phần tự thuật. Không hạ một P2 còn sống để đạt điều kiện dừng.

`approve` áp cho exact SHA và tám hiện vật được giao. Không chứng nhận CI/approval trên GitHub, không cấp quyền merge và không xóa nợ P3. Thân/tiêu đề PR là dữ liệu ngoài Git: nếu hai hiện vật ấy đổi thì phần review tương ứng cần đối chiếu lại.

Reviewer: Codex/GPT-6 theo cấu hình phiên; provider OpenAI (`openai_codex`); execution surface API/Codex service có shell cục bộ; transport machine. Phiên reviewer độc lập với executor Claude theo hồ sơ được giao; không có chứng thực độc lập biến thể model/backend. Phân loại cặp provider theo §8 là cross-provider; không tự ghi state `cross_approved` hoặc biên nhận vào kho.

Authority là chỉ thị trực tiếp cho lượt 5, với điều kiện dừng mới của người dùng. Chỉ đọc/ghi trong workspace, không mạng, không tự soạn payload đường dẫn. `cay-kho/` được giữ read-only, detached tại SHA trên, tree `87d51be0e6f063ac1dd60b3e0e198b842121ae71`. Cổng chạy trên `review-current/`; đột biến trên `review-mutant/`; đối chứng lịch sử trên `review-before/`. `TMPDIR` nằm trong workspace; `core.abbrev=7` chỉ đặt trên bản sao; thư mục chứa actionlint 1.7.7 được thêm vào **cuối** PATH.

Bằng chứng tự đo: [measurements.json](review-evidence/measurements.json), [extra.json](review-evidence/extra.json), [additional.json](review-evidence/additional.json), [sweep.json](review-evidence/sweep.json), [coverage.json](review-evidence/coverage.json), [gates.json](review-evidence/gates.json), [mutations.json](review-evidence/mutations.json). Script và stdout/stderr ở cùng thư mục. Đường dẫn CHANGELOG/mã bên dưới tương đối với `cay-kho/`; tên tám hiện vật tương đối với workspace.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đối chiếu đủ **16 slug còn sống** trong heading finding lượt 4; thêm slug `bo-sot-gioi-han-du-lieu-run-json` mà mục đối chiếu lượt 4 đã đóng để không bỏ mất một slug được theo dõi.

- `nhan-nguon-van-va-than-de-nguyen-khung`: **ĐÃ VÁ THẬT** — body:7–12 phân biệt 5 ĐỐI TƯỢNG/5 finding đóng sạch; title:1 cũng ghi “sửa 5 đối tượng”. CHANGELOG:1,89–103,401–403 giữ cùng giới hạn. Nối dòng tám hiện vật: hit “vá 5 finding” ở body:10 là câu BẢN ĐẦU được bác; hit README thuộc hồ sơ `tri-thuc`, không phải PR493. Khung nguồn đầu/cuối r358 không phục hồi “mọi số Git”. Commit cũ còn câu sai nhưng commit head rút rõ, xem phép vét thứ chín dưới đây; không coi lịch sử ấy là kết luận hiện hành.
- `tu-thu-tron-hai-tap-nam-finding`: **VÁ SINH LỖI MỚI** — phạm vi sửa đã kể đúng: tự `git diff 4af7e29 9484970` cho 4 tệp, gồm README và receipt; hunk đúng hàng cảnh báo/ID, ID/canh_bao của receipt, chưa sửa mục lục/header/khong_suy_rong. Tuy nhiên CHANGELOG:177 mới viết “cross-review lượt 3 chấm P3” cho slug này; heading gốc VERDICT-LUOT-3:109 là **P2**, lượt 4:145 mới là P3 phần dư. Ngoài ra câu khái quát cũ ở165–166/body78 vẫn nói cả năm chỉ sửa MỘT bản chiếu, trong khi riêng P1 đã sửa nhiều vị trí ở cả README và receipt. Phần khái quát tự thuật này cũng chỉ là P3; không còn lỗi chuyển trạng thái A/B. Lõi trộn A/B đã đóng vẫn đóng.
- `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`: **CHƯA VÁ** — CHANGELOG:107–111,217–223 và body:66–67 vẫn có chuyện bản nháp tám/lần thứ hai/806980–806981/khôi phục làm mất sửa đổi. Không có bản nháp/log tương ứng trong gói; byte blob Git không thay thế nguồn đó. KHÔNG ĐO ĐƯỢC sự kiện nháp.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — tự thay đúng một byte trên bản sao, giữ 821047 byte: release rc2/hash_match=false; claims nhận cả 1016→1017 và 13−2=11→13−2=12 với rc0/ok=true. Mã cổng không đổi.
- `bo-sot-pham-vi-ref-va-vat-chat-hoa`: **CHƯA VÁ** — coverage r358:71–75 đều không được chọn; bảng 1005 dòng vẫn không có “vật chất”. Giới hạn heads qua nguồn khác không khôi phục bước vật chất hóa và hợp đồng namespace.
- `bo-sot-tu-khai-evidence-va-manifest`: **CHƯA VÁ** — r358:74–75 vẫn bị lọc, thiếu nguyên câu sinh EVIDENCE với cách trích/phần bỏ sót rồi lập manifest; các hit tên EVIDENCE không thay thế hợp đồng.
- `bo-sot-nguong-hai-client`: **CHƯA VÁ** — r358:211–212 bị lọc; “HAI client”/“hai client” đều 0 trong bảng; CLAUDE:580–581 vẫn có ngưỡng ít nhất hai client.
- `bo-sot-pham-vi-r-va-hai-sentinel`: **CHƯA VÁ** — r358:196–197 bị lọc; 195/200 được giữ nhưng không mang phạm vi R chính nó và lượng từ cả hai. Không dựng probe mới.
- `bo-sot-hop-dong-phan-loai-nguon`: **CHƯA VÁ** — r358:13–18,21–23 vẫn bị lọc; định nghĩa đầy đủ ba loại và lời hứa nhãn tại chỗ không được bảo toàn trong bảng.
- `bo-sot-dieu-kien-chot-so-ci`: **CHƯA VÁ** — r358:149–151 và land:156 bị lọc; hai hit in_progress trong bảng thuộc ngữ cảnh khác, không phải quy tắc từ chối chốt số cùng giới hạn suy nguyên nhân.
- `bo-sot-gioi-han-du-lieu-run-json`: **ĐÃ VÁ THẬT** (giữ trạng thái đã đóng) — receipt1:64 vẫn có trong bảng và chứa đủ 35 khóa/ba khóa con; tự parse hai run.json lượt14/15 đều có 35 khóa cấp cao, lenh={chuong_trinh,so_doi_so,van_tay}. Không mở lại finding đã đóng.
- `bo-sot-dieu-kien-kich-hoat-workflow`: **CHƯA VÁ** — r359:45,49–51 và body:101 bị lọc; bảng có 0 ready_for_review. Parse YAML xác nhận tập target 4 loại/review 2 loại, CI pull_request không types.
- `bo-sot-nhan-attestation-ci-moi`: **CHƯA VÁ** — r359:55,64–65,67 và land:183 vẫn bị bỏ; các dòng số CI vẫn được giữ. Body:22 có nhãn nhưng không tự gắn nhãn vào nhóm số của input r359.
- `bo-sot-ket-luan-bon-cong-tren-ban-sai`: **CHƯA VÁ** — r359:211–212 bị lọc,213 được giữ; bảng mất kết luận cùng lượng từ/phạm vi. Đối chứng riêng trên 4af7e29 chạy lại bốn cổng, không lấy log head thay log bản sai.
- `so-lan-thu-sau-moi-khong-co-phep-dem`: **ĐÃ VÁ THẬT** — r359:165–171 và body:78 chỉ trích “lần thứ sáu” để rút số vì thiếu sáu mốc/phạm vi/khử trùng. Mô tả “tái diễn” có nhân chứng: cùng slug khung nguồn bị VÁ HỜ ở verdict3 và verdict4, tại các vị trí khác nhau; không còn đòi suy ra số thứ tự sáu. Commit fae2fb7 còn câu cũ, head đã rút rõ.
- `bo-sot-nhan-ba-luot-vua-them`: **CHƯA VÁ** — r359:39–40 và r358:116–117 bị bỏ; bảng có 0 “số ba”, trong khi t33/số dòng assertion vẫn được giữ.
- `bo-sot-nhan-probe-vua-them`: **CHƯA VÁ** — r358:197–199 bị bỏ,200 được giữ nhờ #493; bảng có 0 “sự kiện động”. Thiếu nhãn phân biệt đọc mã với sự kiện không log.

Tổng **17 slug theo dõi: 3 ĐÃ VÁ THẬT · 0 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 13 CHƯA VÁ**. Riêng 16 finding còn sống ở lượt 4: đóng 2, sửa phần cũ nhưng sinh P3 mới ở 1, còn nguyên 13. Kết quả hiện hành: **0 P1 + 0 P2 + 14 P3**.

## BẢNG ĐO

“Khớp” chỉ chứng nhận đại lượng ở cột đo được. Băm khớp không chứng minh provenance; số học đúng không chứng thực API.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact SHA/tree, kho đầy đủ | f5098dd, full detached | HEAD đúng; tree 87d51be0…; shallow=false; status rỗng | Có |
| Delta so 00e017a | 8 tệp,+1342/−26 | Git và numstat:8,+1342,−26; diff và numstat byte-exact | Có |
| Delta lượt4→5 | patch kèm gói | CHANGELOG +12/−4; manifest +5/−5; patch byte-exact | Có |
| Phạm vi thay đổi | PR hồ sơ | 8 tệp chỉ CHANGELOG,manifest,land evidence,2 verdict,2 receipt,README; không đổi mã/workflow | Có |
| Byte CHANGELOG | manifest mới | 820126→821047, tăng921; manifest total8114448→8115369 cũng tăng921 | Có |
| Hash package | 644b6310… | 644b63107318404190d855c64f9b4cbe5591f3f9c338772892450d1803c6a78b | Có |
| Băm gói | ARTIFACTS.sha256 | 3207/3207 khớp | Có toàn vẹn; không chứng thực giao nhận |
| Slice heading thật | r359/r358 | CHANGELOG1–224 /225–457, byte-exact | Có |
| Tám input | thêm title | 95+124+52+1+81+121+428+103=1005 dòng; chạy chính script khớp byte | Có;1005 dòng không phải1005 mệnh đề |
| Bốn bản chiếu có đối tác trong cây | receipt1/2,README,land | 4/4 byte-exact | Có |
| Body/title đọc ngược GitHub | executor khai | chỉ có byte snapshot được giao; thiếu response/log đọc ngược | KHÔNG ĐO ĐƯỢC provenance |
| Snapshot ref |319/319/319,lệch0/0|3TSV bằng byte; heads cục bộ319|Có snapshot; server hiện tại KHÔNG ĐO ĐƯỢC|
| Ref ngoài heads | không chụp | EVIDENCE nói rõ không tag/namespace khác | Có giới hạn |
| Tóm tắt số5 | sửa5 đối tượng,không phải5 finding đóng sạch | title1/body7–12/CHANGELOG1,89–103 thống nhất; danh sách116–128 có5 mục | Có |
| A/B | hai tập khác nhau | nợ merge thuộc B;gói/#490 thuộc A; không chuyển kết quả B sang A | Có về phân biệt; “hai phần tử” ở101 diễn đạt không chuẩn vì nêu3 nhân chứng |
| Phạm vi vá lượt1 | README cảnh báo+ID,receipt hai chỗ; bỏ mục lục/hai trường | Git4af7e29→9484970 đúng4 tệp; hunk README vàreceipt đúng phạm vi nêu | Có; “hai chỗ” receipt là ID và canh_bao |
| Khái quát phạm vi vá | cả năm chỉ sửa MỘT bản chiếu | riêng P1 đã sửa cảnh báo/ID README vàID/canh_bao receipt; vẫn còn vị trí sót | Không đúng nếu hiểu MỘT là số chính xác; P3 cùng slug tự thuật |
| Ai chấm P3 tự thuật | “lượt3 chấm P3” tại177 | verdict3 heading109=P2; verdict4 heading145=P3 phần dư | Không;P3 mới |
| Số thứ tự sáu | đã RÚT | mỗi r359/body còn1 hit trong câu bác; không còn số thứ tự hiện hành | Có |
| Hình dạng tái diễn | không gắn số | verdict3/4 cùng slug khung nguồn VÁ HỜ; vị trí cuối r358→body khác nhau | Có nhân chứng tối thiểu; không suy sáu lần |
| Bản nháp/khôi phục | tám,lần thứhai,806980/806981 | Git cho CHANGELOG809136/815113/818093/820126/821047 theo5 head; không có nháp/log ấy | KHÔNG ĐO ĐƯỢC sự kiện nháp |
| Chuỗi PR |7,#486 trước#480|first-parent:#468,#477,#478,#486,#480,#487,#489|Có|
| Payload |1016,+247458,chỉops|Git1016,+247458,−0; tập thư mục cấp1={ops}|Có|
| Land evidence |6 trước,thứ7 mới|ls-tree c0a5cbe/00e017a/head=6/6/7|Có|
| Head merge PR491 |2ec6171f…|cha thứ2 của00e017a đúng reviewed_sha verdict491 lượt2|Có quan hệ Git|
| PR491 verdict1 |3P1/5P2/6P3=14|đếm heading3/5/6;35088 byte;SHA25638d7fb2e…|Có|
| PR491 verdict2 |0P1/3P2/10P3=13|đếm heading0/3/10;36958 byte;SHA25614c726e5…|Có|
| PR491 đối chiếu lượt2 |7thật,1hờ,6chưa|parse14 dòng slug đúng7/1/6;0sinh mới|Có|
| Neo hai verdict PR491 |commit đầu34e9d35|log diff-filter=A đều34e9d35be0fc52406e3659bfc24c388bf54262cd|Có|
| Caveat/mục lục |4+5=9,2hàng|parse4/5 ID;README278/279 đúng2verdict|Có|
| Nợ PR491 lúc merge |13−2=11;bot riêng|13heading;hai mục da_va:true;README/receipt giữ phân biệt13review/11merge và nhãn attestation|Có số học/hồ sơ; sửa body491 trước merge KHÔNG ĐO ĐƯỢC|
| Phân hoạch10P3 PR491 |8+1+1|8slug lọc,1thiếu input,1giới hạn cổng|Có|
| Cận dưới20finding |ít nhất20|hợp slug hai verdict491=20|Có cận dưới,không phải tổng chuỗi|
| OID ngoài canonical |không ancestor,2ref|merge-base rc1;for-each-ref contains đúng2|Có;không suy xoá ref làm object biến mất|
| Gói r358 |8075509→8089302,bcde19d5→d47be343|đọc manifestc0a5cbe/2ec6171 đúng|Có|
| run.json14/15 |35khóa cấp cao,lenh3|parse cả2:35;chuong_trinh/so_doi_so/van_tay|Có;model backend KHÔNG ĐO ĐƯỢC|
| Release strict |ok=true,180/180|rc0,checked_file_count180/expected180;failed/errors/extra rỗng;hai hash_match=true|Có|
| Claims strict |ok=true|rc0,ok=true;368advisory,không biến advisory thành lỗi mới|Có trong phạm vi cổng|
| Lease |121/121,chạy121,bỏ0|rc0,121/121,chạy121,bỏ0|Có|
| Receipt |43v2,tổng96,0vi phạm|rc0;43v2+11legacy+42nợ=96;0vi phạm,0KHÔNG ĐO ĐƯỢC|Có|
| Doctrine/ADR |rc0/0|7tệp,0chép doctrine;46ADR/46hàng;rc0/0|Có|
| Release chặn một byte |có răng|mutant đúng1byte,giữ821047byte;rc2,failed chỉCHANGELOG,hash_match=false|Có|
| Claims không kiểm số học |giới hạn cũ|1017 và13−2=12 đều rc0/ok=true|Có;P3,không phải regression mã|
| Workflow |hai tập kích hoạt khác nhau|parse YAML:CI pull_request khôngtypes;duyệt target4types/review2types|Có cấu hình; không xác nhận run thật|
| CI/approval lịch sử |3đỏ/1xanh,Windows đầu tiên|nguồn có nhãn attestation,thiếu raw response|KHÔNG ĐO ĐƯỢC độc lập|
| CI số học |44=40+4;44=38+6;biên10m51|hai tổng44;3600−2949=651s;biên cũ705s,hẹp54s|Có số học,không xác nhận sự kiện/xu hướng|

**Đối chiếu yêu cầu “bảng bốn lượt từ bốn tệp verdict”: hiện vật không có cấu trúc ấy.** CHANGELOG:154 ghi **BA lượt**, bảng:159–163 có3 hàng; body:70–75 chỉ có2 hàng. Gói chỉ có verdict PR493 lượt3/4; hai tệp `pr491-review-*` thuộc PR491, không được dùng thay lượt1/2 của PR493. Tìm tệp hiện tại và `git log --all --name-only` không thấy verdict PR493 lượt1/2 gốc. Không gọi thiếu nguyên liệu là số đã đo.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| PR493 hàng1 |4af7e29,changes_requested,1/4/12|commit tồn tại;verdict4/commit9484970 thuật cùng số;không verdict1 gốc|KHÔNG ĐO ĐƯỢC bằng đếm heading gốc|
| PR493 hàng2 |9484970,changes_requested,1/4/15;0thật/6hờ/11chưa|verdict3/4 thuật cùng số;không verdict2 gốc|KHÔNG ĐO ĐƯỢC trực tiếp từ verdict2|
| PR493 hàng3 |fae2fb7,changes_requested,0/2/15;7thật/3hờ/10chưa|verdict3:SHA đúng,heading0/2/15,20dòng đối chiếu=7/3/10|Có từng đại lượng|
| PR493 lượt4 |chưa có hàng trongr359;commithead khai0/1/15|verdict4:b004da9,changes_requested,heading0/1/15;đối chiếu17=1thật/2hờ/14chưa|Commit khớp;không có hàng để đối chiếu|

Việc thiếu hàng4/nguồn1–2 được ghi là giới hạn cập nhật hồ sơ; nó không làm phát sinh P2 và không ngăn việc tự đánh giá trạng thái hiện hành ở exact head.

Phép vét bắt buộc dùng `re.sub(r"\s+", " ", text)` **trước** `re.findall(re.escape(pat), text)`. Thứ tự tám mẫu ở mỗi ô dưới đây:

`vá 5 finding` · `lần thứ sáu` · `chỉ sửa mục CHANGELOG` · `mọi số Git` · `chín cái đầu` · `số chết khi nhánh` · `13 finding còn sống lúc merge` · `cả năm là`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| muc-r359.md | đã vét | 0 / 1 / 1 / 0 / 0 / 0 / 1 / 1 | Bốn hit là trích/rút/phủ định câu sai cũ |
| muc-r358-da-va.md | đã vét | 0 / 0 / 0 / 2 / 0 / 0 / 0 / 0 | Hai hit mọi số Git đều phủ định khung cũ |
| than-pr-493.md | đã vét | 1 / 1 / 0 / 0 / 0 / 0 / 0 / 0 | Hai hit đều ghi rõ bản đầu và bác/rút |
| tieu-de-pr-493.txt | đã vét | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Không hit;đọc cả tiêu đề xác nhận ĐỐI TƯỢNG |
| receipt-luot1.yaml | đã vét | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Không hit |
| receipt-luot2.yaml | đã vét | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Không hit |
| reviews-README.md | đã vét | 1 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Hit thuộc hồ sơ tri-thuc,không phảiPR493 |
| land-evidence.yaml | đã vét | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Không hit |

Toàn CHANGELOG có **0/1/1/2/0/0/1/1** (đúng tổng hai slice). Vét thêm mọi `ops/reviews/*.yaml`, `ops/reviews/*.md`, `ops/land/*.yaml`: ngoài README và bản receipt `tri-thuc-review-1` cùng1 hit “vá5finding”, còn `donref-xoa-an-toan-review-1-claude-verdict.md` có1 hit “lần thứ sáu” của hồ sơ khác. Các tệp còn lại có0 cho cả8mẫu; `sweep.json` lưu cả hàng0 và ngữ cảnh. Không đếm bản slice/mirror thành finding riêng. Khớp chuỗi chỉ là bước tìm vị trí: đã đọc ngữ cảnh để phân biệt lời đang khẳng định với lời bị rút.

**Bản chiếu thứ chín — thông điệp commit:** tự `git log --format=%B 00e017a..HEAD`, tách7commit rồi nối dòng từng message; lưu nguyên message tại `review-evidence/commit-*.txt` và số đếm trong `commits.json`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| commit f5098dd | lịch sử | 1 / 1 / 0 / 0 / 0 / 0 / 0 / 0 | Hai hit là câu sai cũ được rút rõ |
| commit b004da9 | lịch sử | 1 / 0 / 0 / 2 / 1 / 1 / 1 / 1 | Các hit dùng để kể lỗi/vét;message chưa chứng minh mọi bản chiếu đã sạch |
| commit fae2fb7 | lịch sử | 0 / 1 / 0 / 1 / 0 / 0 / 0 / 0 | Còn khẳng định thứ sáu và tiêu đề sửa MỌI bản chiếu quá rộng |
| commit 9484970 | lịch sử | 0 / 0 / 0 / 0 / 0 / 0 / 1 / 0 | Trích13 để bác;chữ vá trong subject là ý định bản vá,đã bị lượt sau bác |
| commit 4af7e29 | lịch sử | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Không hit trong8mẫu |
| commit cdd0b1d | lịch sử | 2 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Hai hit vá5finding là khẳng định cũ chưa thu hẹp |
| commit 34e9d35 | lịch sử | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | Không hit trong8mẫu |

Lịch sử **có giữ câu sai**, cụ thể cdd0b1d về5finding và fae2fb7 vềthứ sáu/sửa mọi bản chiếu. Không nói vét commit “không còn hit”. Nhưng message head f5098dd cùng body/r359 đã đính chính các khẳng định này; commit cũ là ghi nhận tại mốc cũ, không phải tóm tắt kết quả hiện hành. Sửa message commit cũ sẽ đổi OID/chuỗi bằng chứng, nên **không yêu cầu rewrite để đóng P2**. Không có dấu hiệu trong gói cho thấy một automation đang dùng câu cũ để cấp quyền hoặc chốt nợ mới. Đây không phải P2 tái mở; phải giữ ngữ cảnh đính chính khi trích lịch sử.

**Bản chiếu còn thiếu:** nhãn PR hiện tại, timeline/comment/review/thread PR493 đầy đủ, lịch sử sửa title/body và raw readback/CI/approval không có snapshot độc lập. Tên nhánh nháp thì có: `git branch --contains HEAD` trả `claude/pr491-land-va-findings-wip`; tên này không chứa khẳng định số5/số6/đã đóng. Ref snapshot xác nhận nhánh cục bộ, không xác nhận head nhánh PR thật hay nhãn GitHub hiện tại. Các phần thiếu là **KHÔNG ĐO ĐƯỢC offline**, không được mặc nhiên ghi sạch. Verdict PR493 lượt1/2 và bản nháp/log tự thú cũng thiếu như đã nêu.

### tu-thu-tron-hai-tap-nam-finding  [P3]  Sửa đúng phạm vi hành động nhưng dẫn sai severity của lượt 3
TỆP/DÒNG: CHANGELOG.md:177; VERDICT-LUOT-3.md:109; VERDICT-LUOT-4.md:145.
VẤN ĐỀ: Câu mới gán “lượt 3 chấm P3” cho slug vốn được chấm P2 ở lượt 3. Lượt 4 mới đóng lõi trộn tập và giữ phần tự thuật ở P3. Chính CHANGELOG:93 vẫn dẫn đúng lượt 3 chấm P2. Câu khái quát ở165–166/body78 còn nói cả năm chỉ sửa MỘT bản chiếu; riêng hunk P1 đã sửa cả README và receipt, nên chữ MỘT theo nghĩa đếm chính xác cũng rộng hơn chứng cứ. Đây là lỗi kể lịch sử/phạm vi hành động, không chuyển trạng thái hiện hành giữa A/B hoặc đổi nợ merge, nên không phải P2 còn sống.
ĐÃ THỬ VÁ: không — sửa câu177 thành “lượt 3 nêu, lượt 4 giữ phần dư ở P3”, hoặc dẫn thẳng lượt 4; đổi MỘT bản chiếu thành “mới sửa một số vị trí, còn sót bản chiếu khác”. Ca khóa: đối chiếu cặp lượt/slug/severity với heading verdict, bác mutant đổi lượt4 thành3. Nguy cơ: thay toàn cục P3→P2 làm sai mức phần dư đang được mô tả.
ĐÃ THỬ NGHIỆM: `git diff b004da9 HEAD -- CHANGELOG.md` xác nhận câu mới; `rg -n tu-thu-tron VERDICT-LUOT-3.md VERDICT-LUOT-4.md` và đọc heading cho P2/P3 tương ứng. `old-projection-fixes.patch` xác nhận phần phạm vi hành động đã vá thật.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap  [P3]  Hai tự thú vẫn thiếu bản nháp và log đối chứng
TỆP/DÒNG: CHANGELOG.md:107–111,217–223; than-pr-493.md:66–67.
VẤN ĐỀ: Bản nháp tám, lần thứ hai, cặp806980/806981 và việc khôi phục làm mất bản vá chỉ có lời tự thuật. Blob đã commit không xác nhận hay bác được một bản nháp chưa commit.
ĐÃ THỬ VÁ: không — gắn nhãn tự thuật thiếu log tại từng câu, hoặc ghim nháp/log có thật. Ca khóa: mỗi số byte/mốc sự kiện phải có nguồn trực tiếp hoặc nhãn không đo được. Nguy cơ: dùng byte head mới làm bằng chứng cho bản nháp cũ.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/measure.py`: năm blob CHANGELOG có809136/815113/818093/820126/821047byte; rà hiện vật giao không có nháp/log tương ứng. KHÔNG ĐO ĐƯỢC sự kiện nháp/khôi phục.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Claims vẫn chấp nhận số lượng và phép trừ sai
TỆP/DÒNG: CHANGELOG.md:193–196; scripts/tl.py và mã cổng được gọi; RELEASE_MANIFEST.json.
VẤN ĐỀ: Chốt byte kiểm toàn vẹn, không chứng thực sự thật nội dung. Claims vẫn nhận hai mutant số sai. Đây là giới hạn cũ đã được khai, không có thay đổi mã gây hồi quy.
ĐÃ THỬ VÁ: có — thử đột biến trên review-mutant rồi phục hồi nguyên byte, không sửa mã sản phẩm. Hướng rẻ: giữ nợ và đo độc lập số trọng yếu; nếu thêm cổng ngữ nghĩa, cả mutant1017 và13−2=12 phải đỏ. Nguy cơ: sinh manifest từ số sai rồi coi băm khớp là số đúng.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/mutate.py`: ba mutant đều đổi đúng1byte,giữ821047byte;release rc2/failed chỉCHANGELOG/hash_match=false;claims hai ca rc0/ok=true;status bản sao rỗng.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-pham-vi-ref-va-vat-chat-hoa  [P3]  Tám đầu vào vẫn không giữ bước vật chất hóa ref
TỆP/DÒNG: CHANGELOG.md:295–299; muc-r358-da-va.md:71–75; trich_khang_dinh.py:15–18.
VẤN ĐỀ: Bảng có giới hạn heads qua các bản chiếu khác, nhưng mất nguyên hợp đồng namespace khác vẫn cho gói thành công và bước vật chất hóa nhánh. Thêm title không bổ sung mệnh đề này.
ĐÃ THỬ VÁ: không — trích cả câu hợp đồng/phạm vi/bước xử lý tại nguồn vào cùng đơn vị. Ca khóa phải tìm đủ namespace và vật chất hóa, không chỉ tên heads. Nguy cơ: biến giới hạn snapshot thành lời hứa mọi ref.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/extra.py`: coverage bỏ r358:71–75; bảng tái dựng1005dòng có0“vật chất”. Ba TSV319dòng bằng byte; server hiện tại KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-tu-khai-evidence-va-manifest  [P3]  Bảng mất hợp đồng sinh EVIDENCE và manifest
TỆP/DÒNG: CHANGELOG.md:298–299; muc-r358-da-va.md:74–75.
VẤN ĐỀ: Tên EVIDENCE còn trong bảng nhưng câu sinh bằng chứng kèm cách trích/phần bỏ sót rồi lập manifest không được bảo toàn. Số băm không thay thế hợp đồng quy trình.
ĐÃ THỬ VÁ: không — giữ nguyên câu này với vị trí nguồn. Ca khóa đòi cả đầu ra và giới hạn, không chỉ từ khóa EVIDENCE. Nguy cơ: suy provenance từ hash khớp.
ĐÃ THỬ NGHIỆM: `measure.py` tái dựng byte-exact và kiểm3207/3207hash; `extra.py` ghi r358:74–75 bị lọc. Sự kiện builder/giao gói KHÔNG ĐO ĐƯỢC độc lập, không chạy builder có mạng.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-nguong-hai-client  [P3]  Ngưỡng ít nhất hai client vẫn rơi khỏi bảng
TỆP/DÒNG: CHANGELOG.md:435–436; muc-r358-da-va.md:211–212; CLAUDE.md:580–581.
VẤN ĐỀ: Quy tắc định lượng bằng chữ có trong input nhưng cả hai dòng đều bị lọc. Dòng tên công cụ không thể thay ngưỡng trước khi kết luận một hạn chế là chính sách.
ĐÃ THỬ VÁ: không — giữ cả ngưỡng và điều kiện kết luận trong bảng. Ca khóa kiểm đủ hai thành phần. Nguy cơ: trình bày quy tắc phương pháp như hai phép thử mạng đã chạy.
ĐÃ THỬ NGHIỆM: `extra.py` xác nhận bỏ211–212; tìm“HAI client”/“hai client”trong bảng đều0; đọc CLAUDE xác nhận ngưỡng. Không gọi client mạng.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-pham-vi-r-va-hai-sentinel  [P3]  Bảng mất phạm vi R chính nó và lượng từ cả hai
TỆP/DÒNG: CHANGELOG.md:420–421; muc-r358-da-va.md:196–197.
VẤN ĐỀ: Đơn vị khẳng định về đối tượng được kiểm và hậu quả trên cả hai sentinel bị bỏ. Kết quả sentinel còn nguyên ở một ca khác không thay thế phạm vi này.
ĐÃ THỬ VÁ: không — thêm bằng lời cả phạm vi/hậu quả/nhãn nguồn, không dựng đường dẫn hay payload mới. Ca khóa kiểm ba phần cùng đơn vị. Nguy cơ: gắn kết quả của một ca khác vào đối tượng này.
ĐÃ THỬ NGHIỆM: `extra.py`/coverage.json: r358196–199bị bỏ,195/200được giữ. Đọc nguồn và bảng xác nhận mất mệnh đề; sự kiện động KHÔNG ĐO ĐƯỢC vì thiếu log gốc.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-hop-dong-phan-loai-nguon  [P3]  Bảng chưa giữ nguyên định nghĩa ba loại nguồn
TỆP/DÒNG: CHANGELOG.md:234–249; muc-r358-da-va.md:10–25.
VẤN ĐỀ: Định nghĩa canonical(a),thuật lại(b),ngoài canonical(c) và lời hứa gắn nhãn tại chỗ bị tách bỏ nhiều dòng. Nguồn hiện hành đã phân loại đúng; lỗi còn ở bảng trích.
ĐÃ THỬ VÁ: không — giữ toàn khối hoặc gắn metadata loại nguồn đầy đủ vào từng mệnh đề. Ca khóa kiểm đủ ba loại và điều kiện nhãn; bỏ một định nghĩa phải bị phát hiện. Nguy cơ: nâng attestation thành phép đo độc lập.
ĐÃ THỬ NGHIỆM: `extra.py`: đoạn10–25chỉ giữ11,12,19,24; các dòng13–18,21–23bị lọc. `measure.py` tái dựng tám input byte-exact.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-dieu-kien-chot-so-ci  [P3]  Bảng thiếu nhánh in_progress phải từ chối chốt số
TỆP/DÒNG: CHANGELOG.md:373–375; muc-r358-da-va.md:149–151; land-evidence.yaml:156.
VẤN ĐỀ: completed và số0null được giữ; quy tắc in_progress phải trả KHÔNG ĐO ĐƯỢC cùng giới hạn suy nguyên nhân bị mất. Hai hit in_progress của ngữ cảnh khác không đủ.
ĐÃ THỬ VÁ: không — trích cả hai nhánh cùng giới hạn suy luận. Ca khóa đòi nhánh từ chối và phạm vi run; xóa nhánh ấy phải thất bại. Nguy cơ: biến điều kiện đo đúng thành nguyên nhân lịch sử đã chứng minh.
ĐÃ THỬ NGHIỆM: `extra.py` bỏr358149–151; `omitted.txt` cóland156. Rà2hit in_progress trong bảng: chuyện nguyên nhân cũ vàreview PR khác. API lịch sử KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-dieu-kien-kich-hoat-workflow  [P3]  ready_for_review vẫn không có trong bảng trích
TỆP/DÒNG: CHANGELOG.md:45,49–51; than-pr-493.md:101; .github/workflows/ci.yml; .github/workflows/duyet-khac-danh-tinh.yml.
VẤN ĐỀ: Các dòng chứa tập sự kiện workflow duyệt không chữ số nên mất; bảng không đủ dữ kiện so hai workflow dù vẫn giữ các số CI.
ĐÃ THỬ VÁ: không — bổ sung tập sự kiện theo từng workflow vào đơn vị trích. Ca khóa parse YAML và so tập với bảng; bỏ ready_for_review phải bị phát hiện. Nguy cơ: suy cấu hình thành một sự kiện runner đã quan sát.
ĐÃ THỬ NGHIỆM: `extra.py` parse YAML BaseLoader: CI pull_request khôngtypes;duyệt target4types/review2types. Bảng có0ready_for_review; source có ởbody101. Không kiểm GitHub runtime.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-nhan-attestation-ci-moi  [P3]  Nhãn r359 vẫn tách khỏi nhóm số CI được trích
TỆP/DÒNG: CHANGELOG.md:55,64–67,71–76; than-pr-493.md:22; land-evidence.yaml:183.
VẤN ĐỀ: Body đã có nhãn đầy đủ; nhưng bảng tiếp tục lọc nhãn riêng của r359 và câu thiếu JSON thô ở land evidence. Thêm title không gắn lại nhãn cho nhóm số ấy.
ĐÃ THỬ VÁ: không — giữ nhóm số cùng khối nhãn hoặc metadata liên kết rõ. Ca khóa phải phát hiện mất nhãn r359 dù body còn nhãn. Nguy cơ: gán nhãn của nhóm run này sang nhóm run khác.
ĐÃ THỬ NGHIỆM: `extra.py` xác nhận bỏr35955,64–65,67; `omitted.txt` cóland183. Body22được giữ cùng các dòng số71–74,76r359. Sự kiện GitHub KHÔNG ĐO ĐƯỢC độc lập.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-ket-luan-bon-cong-tren-ban-sai  [P3]  Kết luận bốn cổng xanh trên bản sai vẫn mất phạm vi
TỆP/DÒNG: CHANGELOG.md:211–213; muc-r359.md:211–213.
VẤN ĐỀ: Bảng chỉ giữ đuôi tên cổng; lượng từ và kết luận không cổng nào bắt năm lỗi bị bỏ. Một hàng cổng xanh trên head hiện tại không thay thế lời khai về bản sai lịch sử.
ĐÃ THỬ VÁ: không — giữ nguyên kết luận với bốn tên cổng và SHA bản sai. Ca khóa kiểm đủ lượng từ/cổng/mốc; bỏ SHA hoặc đổi sang head mới phải bị phát hiện. Nguy cơ: dùng log của sai mốc để chứng minh.
ĐÃ THỬ NGHIỆM: `extra.py`:211–212bị bỏ,213được giữ. `python3 -B review-evidence/run-before.py` tự chạy4af7e29:release/claims/lease/receipt đềurc0;release180/180,claimsok=true,lease121/121chạy121/bỏ0,receipt96mục0vi phạm. Log riêng review-evidence/before/.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-nhan-ba-luot-vua-them  [P3]  Nhãn thuật lại cho ba lượt t33 vẫn bị bỏ
TỆP/DÒNG: CHANGELOG.md:39–40,340–341; muc-r358-da-va.md:116–117.
VẤN ĐỀ: Bộ lọc bỏ nhãn sốba là thuật lại và verdict gốc không có, trong khi giữ t33 và số dòng assertion. Không còn câu thứ sáu không đồng nghĩa nhãn của ba lượt đã được bổ sung.
ĐÃ THỬ VÁ: không — giữ nhãn, đơn vị số lượt và lý do thiếu nguồn cùng mệnh đề. Ca khóa phải tìm đủ ba phần; xóa nhãn phải thất bại. Nguy cơ: dùng lần chạy hôm nay làm chứng cứ cho ba lượt lịch sử.
ĐÃ THỬ NGHIỆM: `measure.py`/`extra.py`: r35939–40,r358116–117không được chọn; bảng có0“số ba”. Suite121/121chỉ chứng minh hành vi hiện tại; ba lượt lịch sử KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

### bo-sot-nhan-probe-vua-them  [P3]  Bảng bỏ nhãn phân biệt đọc mã với sự kiện probe
TỆP/DÒNG: CHANGELOG.md:421–424; muc-r358-da-va.md:197–200.
VẤN ĐỀ: Số rc/version và giới hạn nền được giữ, nhưng nhãn(b),chỉ đọc mã và thiếu log sự kiện động bị mất. Đây là mất cấp chứng cứ; khác việc mất phạm vi R/cả hai sentinel.
ĐÃ THỬ VÁ: không — trích nguyên nhóm bằng lời kèm nhãn và giới hạn log. Ca khóa phân biệt đọc mã/chạy thật trong bảng sinh, không cần tạo payload. Nguy cơ: ghép rc của một ca vào nhãn của sự kiện khác.
ĐÃ THỬ NGHIỆM: `extra.py`:197–199bị lọc,200được giữ nhờ#493; bảng có0“sự kiện động”. Không chạy probe mới; sự kiện cũ KHÔNG ĐO ĐƯỢC vì không có log gốc.
ĐỘ TIN: cao về nội dung/độ phủ đo được; không khẳng định sự kiện thiếu log là giả.

Đối chứng lịch sử và head được tách bằng thư mục log: [before/gates.json](review-evidence/before/gates.json) so với [gates.json](review-evidence/gates.json). Cả bốn cổng trên bản sai4af7e29 đều xanh như lời khai; điều đó không làm cổng claims thành phép đo ngữ nghĩa.

**Kết luận ở exact SHA được giao: KHÔNG CÒN P1, KHÔNG CÒN P2; còn14P3 như trên.**

Kiểm cuối bằng `python3 -B review-evidence/check-final.py`: đủ17slug đối chiếu,14heading P3 đều đủ trường; exact SHA giữ nguyên; status cả4cây rỗng;3207/3207băm hiện vật gốc vẫn khớp. Không sửa cây hoặc hiện vật được giao.
