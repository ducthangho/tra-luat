verdict: changes_requested
reviewed_sha: b004da995d664343bb1b62125ed49281f2371360

**KHÔNG CÒN P1; CÒN 1 P2.** Vì vậy điều kiện mới **“tiếp tục tới hết P2” CHƯA đạt**. Còn **15 P3**, tính theo phần lỗi còn sống sau đối chiếu, không giữ nguyên severity của phần đã được sửa. Không xác nhận quyền merge hoặc CI nhánh PR thật.

Reviewer: Codex/GPT-6 theo chỉ dẫn phiên; provider OpenAI; execution surface API có shell cục bộ; transport machine. Khác provider executor Claude theo hồ sơ được giao; không có chứng thực độc lập biến thể model/backend. Authority và phạm vi là chỉ thị trực tiếp của người dùng cho lượt 4 này. Không tự ghi trạng thái `cross_approved` vào kho.

Tree tự đo: `5d771044b3e5f249959b340b8e5fee713ac715e9`. `cay-kho/` detached tại exact SHA, giữ read-only. Các cổng chạy trên `review-current/`, đột biến trên `review-mutant/`, đối chứng lịch sử trên `review-before/`; tất cả ở workspace, `TMPDIR` cũng ở workspace. Thêm **thư mục** chứa actionlint 1.7.7 vào **cuối** PATH; đặt `core.abbrev=7` trong các bản sao. Không mạng, không ghi kho thật, không tự soạn payload đường dẫn.

Bằng chứng tự chạy: [measurements.json](review-evidence/measurements.json), [extra.json](review-evidence/extra.json), [sweep.json](review-evidence/sweep.json), [gates.json](review-evidence/gates.json), [mutations.json](review-evidence/mutations.json), [bảng tái dựng](review-evidence/rebuilt-table.txt), [dòng bị bỏ](review-evidence/omitted.txt), [patch lịch sử README/receipt](review-evidence/old-projection-fixes.patch). Script và stdout/stderr được giữ cùng thư mục. Một lượt script đo đầu tiên dừng `IndexError` do giả định verdict PR491 lượt 1 có mục đối chiếu; đã sửa parser và chạy lại thành công, không tính lượt lỗi là bằng chứng đo.

Đường dẫn kho dưới đây tương đối với `cay-kho/`; các hiện vật `muc-*.md`, `than-pr-493.md`, `receipt-luot*.yaml`, `reviews-README.md` và `land-evidence.yaml` nằm tại workspace.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đối chiếu **17 slug còn sống của lượt 3**. Những slug đã đóng trước lượt 4 không được đếm lại thành finding mới.

- `nhan-nguon-van-va-than-de-nguyen-khung`: **VÁ HỜ** — CHANGELOG:393–395 nay ghi rõ “Bản ĐẦU”, “nay đã thu hẹp”, “KHÔNG mô tả khung hiện hành”; heading:1 cũng đã đổi sang ĐỐI TƯỢNG. Nhưng **than-pr-493.md:7 vẫn nguyên “vá 5 finding nằm trong chính mục r358”**, đối nghịch sự phân biệt đối tượng được sửa/finding đóng sạch ở chính body:45. Đây là một địa chỉ tồn tại trong finding lượt 3, không phải yêu cầu mở rộng mới. Còn P2 tại bản tóm tắt thân PR.
- `tu-thu-tron-hai-tap-nam-finding`: **VÁ HỜ** — **lõi trộn tập P2 đã vá thật**: CHANGELOG:96–103 tách A/B, gán kết quả lượt 2 cho B và chỉ dẫn đúng “phía dưới”. Đối chiếu năm mục A ở116–128 với năm heading P1/P2 của VERDICT-LUOT-2 xác nhận các nhân chứng A/B khác nhau. Tuy nhiên phần lịch sử sửa mà finding cũ đã nêu vẫn chưa sửa: CHANGELOG:172–173 nói “tôi sửa mục CHANGELOG rồi tưởng đã xong”, trong khi tự `git diff 4af7e29 9484970` thấy cả README và receipt đã được sửa; body:73 còn kể đúng điều ấy. **Phần dư này là P3** về tự thuật thiếu phạm vi, không còn là P2 gán trạng thái sai giữa hai tập. Không dùng phần đã đóng để tiếp tục tính P2.
- `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`: **CHƯA VÁ** — CHANGELOG:107–111,209–215 và body:61–62 vẫn tự kể bản nháp tám, lần thứ hai, verifier806980/806981 và khôi phục làm mất sửa đổi. Gói không có bản nháp/log tương ứng; Git chỉ cho CHANGELOG818093→820126 byte ở lượt này. Sự kiện nháp **KHÔNG ĐO ĐƯỢC**.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — tự đột biến đúng một byte, giữ820126 byte: release rc2/hash_match=false; claims nhận cả1016→1017 lẫn13−2=11→13−2=12 với rc0/ok=true. Mã cổng không đổi trong delta.
- `bo-sot-pham-vi-ref-va-vat-chat-hoa`: **CHƯA VÁ** — bảng998 dòng giữ giới hạn heads qua receipt/README; vẫn không có “vật chất”. CHANGELOG:289–291 (r358:73–75) bị lọc, mất bước vật chất hóa và phần hợp đồng liên quan namespace.
- `bo-sot-tu-khai-evidence-va-manifest`: **CHƯA VÁ** — CHANGELOG:290–291 vẫn mất lời sinh EVIDENCE với cách trích/phần bỏ sót rồi lập manifest. Sáu hit EVIDENCE trong bảng không mang nguyên hợp đồng ấy; thêm land evidence không cứu phần này.
- `bo-sot-nguong-hai-client`: **CHƯA VÁ** — CHANGELOG:427–428 bị lọc. Cả “HAI client” và “hai client” có0 hit trong bảng; CLAUDE:580–581 vẫn xác nhận ngưỡng ít nhất hai client.
- `bo-sot-pham-vi-r-va-hai-sentinel`: **CHƯA VÁ** — CHANGELOG:412–413 bị lọc, vẫn thiếu phạm vi R chính nó và hậu quả trên cả hai sentinel. Bảng builder có ca sentinel CÒN là ca khác; không lấy ca ấy thay cho mệnh đề bị mất. Không dựng probe mới.
- `bo-sot-hop-dong-phan-loai-nguon`: **CHƯA VÁ** — CHANGELOG:229–240 còn mất định nghĩa ngoài canonical, phạm vi canonical, thuật lại và lời hứa nhãn tại chỗ. Bảng có các mảnh chứa số/PR nhưng không đủ cả hợp đồng; hai input mới không cung cấp phần thiếu đó.
- `bo-sot-dieu-kien-chot-so-ci`: **CHƯA VÁ** — CHANGELOG:365–367 bị lọc. Hai hit in_progress của toàn bảng thuộc câu nguyên nhân cũ và một review PR khác; không có quy tắc in_progress phải trả KHÔNG ĐO ĐƯỢC cùng giới hạn suy nguyên nhân. Land evidence:156 cũng bị lọc.
- `bo-sot-gioi-han-du-lieu-run-json`: **ĐÃ VÁ THẬT** — input mới **receipt-luot1.yaml:64** được giữ nguyên vì có chữ số, chứa35 khóa cấp cao và đủ `chuong_trinh`/`so_doi_so`/`van_tay` trong `lenh`. README:291–292 bổ sung giới hạn argv/model và attestation đã có từ trước. Parse độc lập cả run.json lượt14/15 cho35 khóa cấp cao, đúng ba tên con đó. Đã đủ mệnh đề, dù dòng lặp tại CHANGELOG:443 vẫn bị lọc.
- `bo-sot-dieu-kien-kich-hoat-workflow`: **CHƯA VÁ** — CHANGELOG:45,49–51 và body:96 tiếp tục bị lọc; toàn bảng có0 ready_for_review. Parse YAML: ci có pull_request không types; duyệt có4 types pull_request_target,2 types pull_request_review. Không suy sự kiện runtime từ cấu hình.
- `bo-sot-nhan-attestation-ci-moi`: **CHƯA VÁ** — nhãn của body:17 được giữ, nhưng r359:55,64–65,67 tiếp tục bị bỏ trong khi số tại58–59,71–76 được giữ. Nhãn thiếu response ở land evidence:183 cũng không số và bị lọc. Thêm bản chiếu không gắn lại nhãn cho các dòng số r359.
- `bo-sot-ket-luan-bon-cong-tren-ban-sai`: **CHƯA VÁ** — CHANGELOG:203–204 bị lọc;205 chỉ giữ đuôi tên cổng. Không có nguyên kết luận bốn cổng không bắt năm lỗi trên bản sai trong bảng bảy input. Bảng cổng head hiện tại không thay thế mốc bản sai.
- `so-lan-thu-sau-moi-khong-co-phep-dem`: **CHƯA VÁ** — patch có chạm đoạn chứa câu này, chuyển nó sang CHANGELOG:165–166, nhưng vẫn giữ “lần thứ sáu”; body:73 cũng giữ. Không có đơn vị đếm, sáu mốc và quy tắc khử trùng. Sáu VÁ HỜ trong verdict2 là sáu slug của một lượt, không phải sáu sự kiện. **KHÔNG ĐO ĐƯỢC** số thứ tự lịch sử.
- `bo-sot-nhan-ba-luot-vua-them`: **CHƯA VÁ** — CHANGELOG:39–40,332–333 (r358:116–117) vẫn bị lọc; “số ba” có0 hit trong bảng. Những dòng t33/số dòng assertion còn lại không bảo toàn nhãn thuật lại và thiếu verdict gốc.
- `bo-sot-nhan-probe-vua-them`: **CHƯA VÁ** — CHANGELOG:413–415 mất nhãn(b), giới hạn chỉ đọc mã và không log sự kiện động; bảng có0 “sự kiện động”. Dòng416 còn giới hạn nền nhờ có#493; nó không thay thế nhãn về nguồn sự kiện.

Tổng đối chiếu: **1 ĐÃ VÁ THẬT · 2 VÁ HỜ · 14 CHƯA VÁ · 0 VÁ SINH LỖI MỚI**. Trong15 P3 cũ, **1 đã đóng,14 chưa đóng**; phần dư P3 của slug trộn tập khiến tổng P3 hiện hành là15. **1 P2 thật vẫn còn ở thân PR**, nên việc phân loại phần dư của slug kia không làm đạt điều kiện dừng.

## BẢNG ĐO

“Khớp” chỉ xác nhận đại lượng ghi tại cột đo được. Byte/hash đúng không chứng thực provenance; số học đúng không xác nhận sự kiện GitHub. Lệnh tái đo nằm trong `review-evidence/measure.py`, `extra.py`, `run-gates.py`, `mutate.py`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/tree | b004da995d664343bb1b62125ed49281f2371360 | HEAD đúng; tree5d771044b3e5f249959b340b8e5fee713ac715e9; detached,sạch | Có |
| Kho đầy đủ/root | kho đầy đủ | shallow=false; root394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Có |
| Delta so00e017a | 8 tệp,+1334/−26 | cộng trực tiếp numstat bằng script:8,+1334,−26; numstat và diff byte-exact với Git | Có |
| Delta lượt3→4 | patch kèm gói | 2 tệp,+44/−19:CHANGELOG+39/−14,manifest+5/−5; patch byte-exact | Có |
| Mã/workflow thay đổi | PR hồ sơ | 8 tệp toàn PR chỉ hồ sơ,CHANGELOG,manifest | Có |
| CHANGELOG/manifest tăng byte | manifest mới | CHANGELOG818093→820126,manifest total8112415→8114448; cùng tăng2033 | Có |
| Băm gói | ARTIFACTS.sha256 | 3207/3207 khớp | Có toàn vẹn; provenance KHÔNG ĐO ĐƯỢC |
| Ref snapshot |319/319/319,lệch0/0|3TSV bằng byte; heads trong cây319|Có snapshot; server hiện tại KHÔNG ĐO ĐƯỢC|
| Phạm vi snapshot |heads|EVIDENCE tự giới hạn heads,không tag/namespace khác|Có|
| Slice r359 |heading thật|CHANGELOG1–216,byte-exact|Có|
| Slice r358 |heading thật|CHANGELOG217–449,heading kế450,byte-exact|Có|
| Bảy input |thêm receipt1 và land evidence|93+124+48+81+121+428+103=998 dòng có số,output byte-exact|Có;998 dòng không phải998 mệnh đề độc lập|
| Bốn bản chiếu ngoài kho |receipt1,receipt2,README,land|4/4 byte-exact với bản trong cây|Có|
| Cả hai bảng README |cảnh báo và mục lục|hàng17–25 và278–279 đều trong bảng;4+5 caveat,2 hàng mục lục PR491|Có|
| Năm đối tượng A |nhãn nguồn,neo,gói,#490,mirror|đếm danh sách116–128 đúng5|Có|
| Năm finding B |nợ merge,khung nguồn,phân hoạch,CI,ref|năm heading P1/P2 verdict2 cùng năm slug trong đối chiếu của nó,đều VÁ HỜ|Có qua verdict2; thiếu verdict1 gốc|
| Các nhân chứng A/B khác nhau |nợ merge thuộc B;gói và#490 thuộc A|đọc từng phần tử và phạm vi finding:đúng các quan hệ ấy|Có;không phải tuyên bố hai tập hoàn toàn rời nhau|
| “Hai phần tử không giao” |câu101|thực tế câu liệt kê1 nhân chứng B\A và2 nhân chứng A\B|Hai chiều khác biệt đúng;danh từ đếm “hai phần tử” không chuẩn|
| Trạng thái tập B ở lượt3 |đóng P1 và bốn trong năm|4/5 slug B ĐÃ VÁ THẬT,bao gồm P1;1/5 VÁ HỜ|Khớp nếu P1 nằm trong4;không phải P1 cộng thêm4|
| Tóm tắt body |“vá5 finding nằm trong chính r358”|body7 nguyên;heading CHANGELOG đổi sang ĐỐI TƯỢNG;body45 phân biệt được sửa/đóng sạch|Không đồng bộ;P2 còn sống|
| Tự kể chỗ đã sửa lượt2 |“tôi sửa mục CHANGELOG”|patch4af7e29→9484970 còn sửa README và receipt;body73 kể đúng phần này|Thiếu phạm vi;P3 phần dư|
| Số thứ tự tái diễn |lần thứ sáu|không có6 mốc/đơn vị;patch chuyển câu nhưng giữ số|KHÔNG ĐO ĐƯỢC|
| Bản nháp/tự phục hồi |tám,lần thứhai,806980/806981|không có nháp/log tương ứng|KHÔNG ĐO ĐƯỢC|
| Chuỗi merge |7 PR,#486 trước#480|first-parent:#468,#477,#478,#486,#480,#487,#489|Có|
| Payload |1016 tệp,+247458,chỉops|Git1016,+247458,tập thư mục cấp1={ops}|Có|
| Land evidence |6 cũ,thứ7 mới|ls-tree c0a5cbe/00e017a/head=6/6/7|Có|
| Head merge PR491 |2ec6171f…|cha thứ2 của00e017a=2ec6171f7a2e21ae950633f9e328329a355f7a6d|Có quan hệ Git|
| Verdict PR491 lượt1 |3P1/5P2/6P3=14|đếm heading3/5/6=14|Có|
| Verdict PR491 lượt2 |0P1/3P2/10P3=13|đếm heading0/3/10=13|Có|
| Đối chiếu PR491 lượt2 |7 thật,1 hờ,6 chưa|parse14 dòng slug đúng7/1/6|Có|
| Verdict PR491 bytes |35088/36958|tự đọc đúng35088/36958|Có|
| SHA256 verdict PR491 lượt1 |38d7fb2e…|38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c|Có|
| SHA256 verdict PR491 lượt2 |14c726e5…|14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468|Có|
| Commit đầu chứa hai verdict |34e9d35…|log diff-filter=A cả hai:34e9d35be0fc52406e3659bfc24c388bf54262cd|Có|
| Caveat receipt |4+5=9|parse4 và5 ID;t27 thuộc suite đạt|Có|
| Nợ lúc merge PR491 |13 review,11 merge;bot riêng|13 heading,2 da_va:true,13−2=11;README18/278 vàreceipt7–9/46–51/201–210 nhất quán|Có về hồ sơ;sự kiện sửa body491 KHÔNG ĐO ĐƯỢC|
| Bot |5P2,3 mới/2 trùng,4 đúng/1 một phần|parse đúng5,3/2,4/1|Có theo receipt;bot API KHÔNG ĐO ĐƯỢC|
| Phân hoạch PR491 P3 |8+1+1|đọc10 slug:8 lọc,1 thiếu input,1 giới hạn cổng;body57 giữ đủ ánh xạ|Có|
| OID ngoài canonical |không ancestor,2 ref chứa|ancestry rc1;for-each-ref trả đúng2 ref|Có;không suy về GC hoặc object biến mất|
| Gói c0a5cbe→2ec6171 |8075509→8089302,bcde19d5→d47be343|đọc hai manifest đúng|Có|
| Package hash head |1659afc0…|1659afc06278a331abcd1cad8664168cbe8838191543ab6e14101f1d5c87b40b|Có|
| Release strict |ok=true,180/180|rc0,180/180,failed/errors/extra rỗng,cả hai hash_match=true|Có|
| Claims strict |ok=true|rc0,ok=true|Có trong phạm vi cổng|
| Lease |121/121,chạy121,bỏ0|rc0,121/121,chạy121,bỏ0|Có|
| Receipt |43v2,tổng96,0vi phạm|rc0;43v2+11legacy+42nợ=96;0vi phạm,0KHÔNG ĐO ĐƯỢC|Có|
| Doctrine/ADR |rc0/0|7 tệp,0chép doctrine;46ADR/46hàng;rc0/0|Có|
| Bốn cổng trên bản sai4af7e29 |đều xanh|tự chạy lại:release/claims/lease/receipt đều rc0;release180/180,claimsok=true,lease121/121 bỏ0,receipt96 mục0vi phạm|Có;log riêng tại review-evidence/before/|
| Một byte có răng |release chặn|đổi1 byte,giữ820126 byte;rc2,failed chỉCHANGELOG,hash_match=false|Có|
| Claims không kiểm số học |giới hạn cũ|1017 và13−2=12 đều rc0/ok=true|Có giới hạn;không gán thành P1 mới|
| run.json14/15 |35 khóa cấp cao,3 tronglenh|cả2 đúng35 và{chuong_trinh,so_doi_so,van_tay};receipt1:64 đưa đủ vào bảng|Có;đóng P3 độ phủ|
| Workflow |hai tập kích hoạt khác nhau|ci:push master,pull_request khôngtypes,dispatch;duyệt:target4types/review2types|Có cấu hình;run thật KHÔNG ĐO ĐƯỢC|
| CI/approval lịch sử |3đỏ/1xanh,approval,Windows đầu tiên|nhãn attestation có trong nguồn;không raw response|KHÔNG ĐO ĐƯỢC độc lập|
| CI số học |44=40+4;44=38+6|44/44;20m38s=1238s,49m09s=2949s|Có số học|
| Biên Windows |10m51s,nhỏ hơn mốc48m15s|3600−2949=651s;3600−2895=705s;hẹp54s|Có số học;không xác nhận job/xu hướng|
| Ba lượt t33/probe lịch sử |thuật lại,thiếu log|nhãn source còn nguyên,nhãn bị bảng bỏ|KHÔNG ĐO ĐƯỢC lịch sử;không dựng probe|
| Đọc ngược body/đăng verdict |byte-exact/lượt đã đăng|chỉ có hiện vật body đã giao,không response vận chuyển|KHÔNG ĐO ĐƯỢC provenance|

Bảng ba lượt mới ở CHANGELOG:159–163 được kiểm **từng ô**:

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Hàng1,ô lượt |1|verdict2 gọi nguồn trước là lượt1|Chỉ đối chiếu gián tiếp|
| Hàng1,ô head |4af7e29|Git có commit;verdict2 dùng làm mốc trước|Có commit;neo verdict1 gốc KHÔNG ĐO ĐƯỢC|
| Hàng1,ô verdict |changes_requested|hai verdict sau thuật cùng kết quả|KHÔNG ĐO ĐƯỢC từ verdict1 gốc|
| Hàng1,ô P1/P2/P3 |1/4/12|verdict2 đối chiếu17 slug cũ:1P1+4P2+12P3;khớp gián tiếp|KHÔNG ĐO ĐƯỢC bằng đếm heading verdict1 gốc|
| Hàng1,ô đối chiếu |—|không tuyên bố số|Không có số cần đo|
| Hàng2,ô lượt |2|VERDICT-LUOT-2.md và ngữ cảnh đối chiếu lượt1|Có|
| Hàng2,ô head |9484970|reviewed_sha9484970f269e09fd9cace3432c19cb90e854c93c|Có|
| Hàng2,ô verdict |changes_requested|dòng verdict của tệp|Có|
| Hàng2,ô P1/P2/P3 |1/4/15|đếm heading1/4/15|Có|
| Hàng2,ô đối chiếu |0 thật,6 hờ,11 chưa|parse17 dòng slug:0/6/11|Có|
| Hàng3,ô lượt |3|VERDICT-LUOT-3.md và ngữ cảnh đối chiếu lượt2|Có|
| Hàng3,ô head |fae2fb7|reviewed_shafae2fb77fc2121af9f94cd026db0179b4e8ed9bc|Có|
| Hàng3,ô verdict |changes_requested|dòng verdict của tệp|Có|
| Hàng3,ô P1/P2/P3 |0/2/15|đếm heading0/2/15|Có|
| Hàng3,ô đối chiếu |7 thật,3 hờ,10 chưa|parse20 dòng slug:7/3/10|Có|

**Gói chỉ có hai verdict PR493 gần nhất, không có verdict PR493 lượt1.** Tìm tên tệp trong workspace và lịch sử `git log --all --name-only` không thấy bản gốc PR493 lượt1. Hai verdict `pr491-review-*` là PR491, không thay được nguồn thiếu. Không biến sự trùng khớp gián tiếp thành phép đếm trên “ba tệp verdict”.

Phép vét bắt buộc: tự dùng `re.sub(r"\s+", " ", text)` **trước** `re.findall(re.escape(pat), text)`, trên toàn CHANGELOG, mọi `ops/reviews/*.yaml`, `ops/reviews/*.md`, `ops/land/*.yaml`, và cả bảy hiện vật ngoài kho. Bảng dưới giữ **cả số0**, theo thứ tự năm mẫu người dùng yêu cầu:

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| r359: mọi số Git / chín cái đầu / số chết khi nhánh / 13 finding còn sống lúc merge / cả năm là |đã vét|0 / 0 / 0 / 1 / 1|Hai hit đều là câu sai cũ được trích để bác|
| r358:cùng5 mẫu|đã vét|2 / 0 / 0 / 0 / 0|Cả2 có “bản trước/Bản ĐẦU”,phủ định khung cũ rõ|
| receipt1:cùng5 mẫu|đã vét|0 / 0 / 0 / 0 / 0|Không hit|
| receipt2:cùng5 mẫu|đã vét|0 / 0 / 0 / 0 / 0|Không hit;đọc cả trường nợ vàcaveat|
| README toàn tệp,cả2 bảng:cùng5 mẫu|đã vét|0 / 0 / 0 / 0 / 0|Không hit đúng chuỗi;hàng18 vẫn có trích13 theo cách viết khác,đã gắn“Bản đầu”|
| land evidence:cùng5 mẫu|đã vét|0 / 0 / 0 / 0 / 0|Không hit|
| body:cùng5 mẫu|đã vét|0 / 0 / 0 / 0 / 0|Không hit;**vẫn còn phản ví dụ khác tại dòng7**|
| Toàn CHANGELOG:cùng5 mẫu|đã vét|2 / 0 / 0 / 1 / 1|Đúng tổng hai mục,không thêmhit ở mục cũ|

Không đếm bản slice và bản CHANGELOG thành lỗi riêng. `sweep.json` giữ ngữ cảnh mỗi hit. Câu13 tại185–188 nằm trong danh sách lỗi của các lượt trước, kèm phép trừ11 và mô tả sửa; đọc thêm README18/278 và receipt hiện hành xác nhận nó không phục hồi P1. Các mục khung nguồn/phân hoạch/CI/ref ngay sau đó cũng đang giải thích các finding lịch sử, không phải danh sách trạng thái head mới. **Không có hit không có nghĩa đã đóng finding**: năm regex gợi ý không chứa câu tóm tắt body7.

### nhan-nguon-van-va-than-de-nguyen-khung  [P2]  Tóm tắt thân PR vẫn giữ khẳng định mà heading đã thu hẹp
TỆP/DÒNG: than-pr-493.md:7,45; CHANGELOG.md:1,96–103,393–395.
VẤN ĐỀ: Dòng7 vẫn trình bày kết quả PR là “vá5 finding nằm trong chính mục r358”. Đây chính là khung tóm tắt lượt3 yêu cầu đồng bộ: số5 hiện chỉ được chứng minh là năm đối tượng được đụng tới, còn các finding PR493 phân bố ở nhiều hiện vật và chưa đóng sạch. Tiêu đề chính CHANGELOG đã đổi sang “sửa5 ĐỐI TƯỢNG”; body45 cũng giới hạn “được sửa” không phải “đã đóng sạch”, nhưng giới hạn ấy chưa đi vào phần Việc này là gì. P2 còn ở bản chiếu người đọc dùng để hiểu kết quả PR, không còn ở đoạn nguồn cuối r358. Không khẳng định đã kiểm body GitHub hiện tại; đây là lỗi của body được giao review.
ĐÃ THỬ VÁ: không — sửa body7 theo cùng đơn vị ĐỐI TƯỢNG và giới hạn kết quả đã chứng minh; đồng bộ mọi bản tóm tắt. Ca kiểm: đọc toàn body sau nối dòng, đối chiếu các câu tóm tắt với bảng A/B và trạng thái từng slug; bản chỉ sửa heading CHANGELOG phải bị bác. Nguy cơ: đổi toàn cục chữ finding sẽ làm sai tên finding lịch sử; sửa theo nghĩa từng vị trí.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/measure.py` tái dựng body trong bảng bằng byte; đọc body7/45 và exact delta hai tệp xác nhận body7 vẫn nguyên. Vét năm mẫu gợi ý không khớp câu này, nên không đủ chứng minh đóng finding.
ĐỘ TIN: cao

### tu-thu-tron-hai-tap-nam-finding  [P3]  Tách tập đã đúng nhưng tự thuật chỗ sửa vẫn bỏ README và receipt
TỆP/DÒNG: CHANGELOG.md:96–103,172–173; than-pr-493.md:73.
VẤN ĐỀ: Nhân chứng về hai tập nay đúng: nợ merge thuộc B; gói/payload và#490 thuộc A. Không còn căn cứ giữ P2 trộn trạng thái. Nhưng lời kể “tôi sửa mục CHANGELOG rồi tưởng đã xong”, vốn đã được finding lượt3 chỉ ra, vẫn lược sai phạm vi hành động đã thực hiện. Patch lượt1→2 có sửa cả cảnh báo/ID README và receipt; lỗi thật là sửa chưa đủ trường/bảng trong các tệp ấy. Đây là thiếu chính xác trong tự thuật lịch sử, không làm sai số nợ hiện hành hoặc chuyển trạng thái giữa A/B, nên phần dư chấm P3.
ĐÃ THỬ VÁ: không — sửa câu173 để kể đúng các bản chiếu/trường đã sửa và còn sót. Ca kiểm: đối chiếu từng đường dẫn với `git diff --name-only 4af7e29 9484970` và hunk tương ứng. Nguy cơ: viết lại thành “đã sửa hết README/receipt” sẽ vượt patch; chỉ nói đúng trường được đụng tới.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/extra.py`; `old-projection-fixes.patch` giữ hunk README/receipt; Git cho4 tệp gồm cả hai tệp ấy. Đọc năm mục A và năm heading P1/P2 verdict2 xác nhận lõi trộn tập đã đóng; chỉ dẫn “phía dưới” cũng đúng.
ĐỘ TIN: cao

### hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap  [P3]  Hai tự thú vẫn thiếu bản nháp và log để kiểm độc lập
TỆP/DÒNG: CHANGELOG.md:107–111,209–215; than-pr-493.md:61–62.
VẤN ĐỀ: Bản nháp tám, số thứ tự lần thứhai, cặp806980/806981 và hành vi khôi phục chưa có nguyên liệu độc lập. Blob commit không chứng minh hoặc bác một bản nháp chưa commit.
ĐÃ THỬ VÁ: không — gắn nhãn tự thuật thiếu log tại hai đoạn, hoặc ghim bản nháp/log nếu có. Kiểm byte và nguồn từng mốc; tránh lấy byte head mới thay byte bản nháp.
ĐÃ THỬ NGHIỆM: `extra.py` đọc blob bằng Git:818093→820126. Rà hiện vật và lịch sử được giao không có bản nháp/log hai kích thước ấy. Sự kiện nháp/khôi phục KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về thiếu chứng cứ, không kết luận tự thú giả

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Cổng claims vẫn chấp nhận số lượng và phép trừ sai
TỆP/DÒNG: CHANGELOG.md:186,217; scripts/tl.py; RELEASE_MANIFEST.json.
VẤN ĐỀ: Cổng toàn vẹn byte có răng, còn claims không xác nhận sự thật số học. Giới hạn được khai từ trước; PR không đổi mã cổng nên không chấm thành P1/P2 mới.
ĐÃ THỬ VÁ: có — đột biến trên bản sao rồi phục hồi, không sửa mã sản phẩm. Hướng rẻ là giữ nợ với phép đo độc lập cho các số trọng yếu; nếu xây cổng mới, mutant1017 và phép trừ sai phải đỏ. Nguy cơ: sinh manifest từ số sai rồi dùng băm khớp làm chứng nhận nội dung.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/mutate.py`:release một byte rc2,failed chỉCHANGELOG;claims1017 và13−2=12 đều rc0/ok=true. Cả ba đột biến giữ820126 byte; bản sao sạch sau phục hồi.
ĐỘ TIN: cao

### bo-sot-pham-vi-ref-va-vat-chat-hoa  [P3]  Bảy đầu vào vẫn không đưa bước vật chất hóa vào bảng
TỆP/DÒNG: CHANGELOG.md:287–291; muc-r358-da-va.md:71–75; trich_khang_dinh.py:15–18.
VẤN ĐỀ: Giới hạn heads đã xuất hiện qua các bản chiếu, nhưng câu namespace khác vẫn thành công và bước vật chất hóa nhánh chưa được biểu diễn đủ. “Vật chất” có0 hit trong998 dòng trích.
ĐÃ THỬ VÁ: không — giữ nguyên mệnh đề phạm vi và bước vật chất hóa cùng vị trí nguồn. Kiểm cả hai ý trong bảng sau sinh; tránh đổi cảnh báo snapshot heads thành lời hứa mọi namespace.
ĐÃ THỬ NGHIỆM: `measure.py` tái tạo byte-exact bảy input; `omitted.txt` có r358:73–75. Ba TSV319 dòng bằng byte; máy chủ hiện tại KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-tu-khai-evidence-va-manifest  [P3]  Hợp đồng sinh EVIDENCE và manifest vẫn bị lọc
TỆP/DÒNG: CHANGELOG.md:290–291; muc-r358-da-va.md:74–75; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Bảng giữ một số tên EVIDENCE nhưng không giữ mệnh đề sinh tệp kèm cách trích/phần bỏ sót và lập manifest. Land evidence mới không bổ sung hợp đồng này.
ĐÃ THỬ VÁ: không — trích nguyên câu hợp đồng với nguồn, kiểm đủ đầu ra lẫn phần giới hạn; tránh gọi sự khớp băm là chứng minh builder đã chạy.
ĐÃ THỬ NGHIỆM: `measure.py` ghi hai dòng bị bỏ,3207/3207 băm khớp. Rà6 hit EVIDENCE trong bảng không thấy hợp đồng đầy đủ. Sự kiện dựng gói KHÔNG ĐO ĐƯỢC độc lập, không chạy builder có mạng.
ĐỘ TIN: cao

### bo-sot-nguong-hai-client  [P3]  Ngưỡng ít nhất hai client vẫn mất khỏi bảng
TỆP/DÒNG: CHANGELOG.md:427–428; muc-r358-da-va.md:211–212; CLAUDE.md:580–581.
VẤN ĐỀ: Mệnh đề định lượng bằng chữ đã nằm trong đầu vào nhưng không được bộ lọc giữ. Những số công cụ hoặc tên client ở hàng khác không thay thế ngưỡng trước khi kết luận chính sách.
ĐÃ THỬ VÁ: không — bổ sung cả ngưỡng và điều kiện được kết luận. Ca kiểm tìm nguyên mệnh đề hai client trong bảng; tránh trình bày quy tắc phương pháp như hai lần thử mạng đã thực hiện.
ĐÃ THỬ NGHIỆM: `measure.py` tái trích; cả“HAI client”/“hai client” có0 hit. Đọc CLAUDE xác nhận ngưỡng. Không gọi client mạng.
ĐỘ TIN: cao

### bo-sot-pham-vi-r-va-hai-sentinel  [P3]  Bảng vẫn mất phạm vi R chính nó và lượng từ cả hai
TỆP/DÒNG: CHANGELOG.md:412–413; muc-r358-da-va.md:196–197.
VẤN ĐỀ: Câu xác định phạm vi của chốt và hậu quả trên cả hai sentinel bị bỏ. Bảng builder ghi sentinel còn nguyên trong ca khác không đóng mệnh đề này.
ĐÃ THỬ VÁ: không — bổ sung bằng lời phạm vi, hậu quả và nhãn nguồn cùng một đơn vị. Kiểm đủ ba thành phần; không dựng chuỗi đường dẫn. Nguy cơ: gắn nhầm kết quả một ca khác vào phạm vi đang nói.
ĐÃ THỬ NGHIỆM: `measure.py`,đối chiếu bảng sinh với r358:195–200 và `omitted.txt`;dòng196–197 bị lọc. Hậu quả động KHÔNG ĐO ĐƯỢC vì thiếu log gốc; không chạy probe mới.
ĐỘ TIN: cao về thiếu mệnh đề

### bo-sot-hop-dong-phan-loai-nguon  [P3]  Bảng chưa giữ đủ định nghĩa ba loại nguồn
TỆP/DÒNG: CHANGELOG.md:226–241; muc-r358-da-va.md:10–25.
VẤN ĐỀ: Hợp đồng canonical(a),thuật lại(b),ngoài canonical(c) và lời hứa nhãn tại chỗ tiếp tục mất nhiều dòng. Câu phủ định“mọi số Git” được giữ không định nghĩa đủ hợp đồng.
ĐÃ THỬ VÁ: không — giữ cả khối định nghĩa hoặc gắn metadata nguồn đầy đủ cho mỗi mệnh đề. Kiểm đủ ba loại và giới hạn nhãn; tránh nâng attestation thành bằng chứng sự kiện đã đo.
ĐÃ THỬ NGHIỆM: `measure.py`/`omitted.txt`:r358:13–18,21–23 có các phần bị bỏ; đọc bảng bảy input không có nguồn thay thế đầy đủ. Các source định nghĩa nay nhất quán trong CHANGELOG, lỗi còn ở trích xuất.
ĐỘ TIN: cao

### bo-sot-dieu-kien-chot-so-ci  [P3]  Bảng còn thiếu nhánh in_progress phải từ chối chốt số
TỆP/DÒNG: CHANGELOG.md:365–367; muc-r358-da-va.md:149–151; land-evidence.yaml:156.
VẤN ĐỀ: Bảng có completed và0null ở các bản tóm tắt, nhưng không có quy tắc in_progress⇒KHÔNG ĐO ĐƯỢC và giới hạn suy nguyên nhân. Hai hit in_progress hiện có khác phạm vi.
ĐÃ THỬ VÁ: không — giữ hai nhánh cùng giới hạn suy luận. Ca kiểm phải tìm đủ nhánh từ chối, không chỉ tên trạng thái; tránh dùng quy tắc đo làm giải thích nguyên nhân của run cũ.
ĐÃ THỬ NGHIỆM: `measure.py` bỏ r358:149–151 và land:156. Rà từng hit in_progress trong bảng:chuyện nguyên nhân r359 vàreview PR khác. Run/API lịch sử KHÔNG ĐO ĐƯỢC offline.
ĐỘ TIN: cao

### bo-sot-dieu-kien-kich-hoat-workflow  [P3]  ready_for_review vẫn không có trong bảng trích
TỆP/DÒNG: CHANGELOG.md:45,49–51; than-pr-493.md:96; .github/workflows/ci.yml; .github/workflows/duyet-khac-danh-tinh.yml.
VẤN ĐỀ: Bảng giữ các số CI nhưng mất tập kích hoạt workflow duyệt, không đủ dữ kiện đối chiếu hai workflow. Đây là lỗi độ phủ, không chứng minh một run GitHub đã hoặc chưa xảy ra.
ĐÃ THỬ VÁ: không — thêm tập sự kiện theo từng workflow vào đơn vị trích. Kiểm bằng parse YAML rồi so tập; tránh suy cấu hình của một workflow thành việc nền tảng không phát sự kiện.
ĐÃ THỬ NGHIỆM: `measure.py` dùng YAML BaseLoader:ci pull_request khôngtypes;duyệt target4types/review2types. Tìm ready_for_review trong bảng:0. Không mạng.
ĐỘ TIN: cao

### bo-sot-nhan-attestation-ci-moi  [P3]  Nhãn nguồn r359 vẫn tách khỏi chính nhóm số được trích
TỆP/DÒNG: CHANGELOG.md:55,64–67,71–76; than-pr-493.md:17; land-evidence.yaml:183.
VẤN ĐỀ: Body có nhãn đủ là cải thiện cũ được giữ; thêm land evidence chưa gắn lại nhãn cho các dòng số r359. Dòng nêu thiếu JSON thô trong land evidence mới cũng bị lọc. Không lấy nhãn xa của một input mặc nhiên áp cho mọi bản chiếu.
ĐÃ THỬ VÁ: không — trích nhóm số kèm khối nhãn hoặc metadata liên kết rõ. Ca kiểm bỏ nhãn riêng của r359 phải bị phát hiện dù body còn nhãn. Nguy cơ: ghép nhãn sai nhómrun/approval hoặc biến attestation thành phép đo API.
ĐÃ THỬ NGHIỆM: `measure.py` ghi omitted r359:55,64–65,67 và land:183;bảng giữ body17 cùng các số r35971–76. Sự kiện API KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-ket-luan-bon-cong-tren-ban-sai  [P3]  Kết luận bốn cổng xanh trên bản sai vẫn mất phạm vi
TỆP/DÒNG: CHANGELOG.md:203–205; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Hai dòng đầu chứa lượng từ và kết luận không cổng nào bắt năm lỗi bị bỏ; chỉ đuôi tên cổng được trích. Cổng xanh trên head hiện tại là một khẳng định khác.
ĐÃ THỬ VÁ: không — giữ cả kết luận với tên bốn cổng và SHA bản sai. Kiểm đủ lượng từ/cổng/mốc; tránh lấy log head mới chứng minh head cũ hoặc ngược lại.
ĐÃ THỬ NGHIỆM: `measure.py` xác nhận r359:203–204 bị bỏ,205 được giữ. Đối chứng lịch sử chạy riêng bằng `review-evidence/run-before.py`, không dùng số của verdict3 làm lần chạy lượt4; xem kết quả đối chứng cuối tệp.
ĐỘ TIN: cao

### so-lan-thu-sau-moi-khong-co-phep-dem  [P3]  Số lần thứ sáu được giữ dù đoạn văn đã sửa
TỆP/DÒNG: CHANGELOG.md:165–166; than-pr-493.md:73.
VẤN ĐỀ: Delta sửa đoạn hai lượt thành ba lượt và chuyển câu, nhưng không thêm đơn vị, sáu mốc hoặc quy tắc khử trùng. Sáu VÁ HỜ là sáu slug của một lượt; không suy được số thứ tự lịch sử. Bảng mới tự nó không tạo chứng cứ cho con số sáu.
ĐÃ THỬ VÁ: không — đổi sang mô tả định tính tái diễn, hoặc ghi nhãn tự thuật kèm sáu mốc có nguồn. Ca kiểm đếm mốc và khử trùng theo đơn vị đã khai; nguy cơ cộng nhiều hậu quả của cùng lượt thành nhiều lần.
ĐÃ THỬ NGHIỆM: đọc `diff-luot3-sang-luot4.patch`,khớp“thứ sáu”trong r359/body,parse verdict2 cho6slugVÁ HỜ. Số thứ tự lịch sử KHÔNG ĐO ĐƯỢC;không khẳng định chắc chắn bằng số khác.
ĐỘ TIN: cao về thiếu cơ sở

### bo-sot-nhan-ba-luot-vua-them  [P3]  Nhãn thuật lại của ba lượt t33 vẫn bị bộ lọc bỏ
TỆP/DÒNG: CHANGELOG.md:39–40,332–333; muc-r358-da-va.md:116–117.
VẤN ĐỀ: Hai nhãn nói sốba là thuật lại và verdict gốc vắng mặt không chữ số nên mất; các dòng assertion/t33 vẫn còn. Bảy đầu vào không bổ sung nhãn cùng phạm vi này.
ĐÃ THỬ VÁ: không — giữ nhãn và mệnh đề số lượt chung đơn vị trích. Ca kiểm đủ nhãn,đơn vị và lý do thiếu nguồn; tránh lấy lần chạy hôm nay làm chứng minh ba lượt lịch sử.
ĐÃ THỬ NGHIỆM: `measure.py`/`omitted.txt` ghi bốn dòng bị bỏ;“số ba”có0 hit. Suite121/121 chỉ chứng minh hành vi hiện tại;ba lượt lịch sử KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-nhan-probe-vua-them  [P3]  Bảng vẫn bỏ nhãn phân biệt đọc mã với sự kiện probe
TỆP/DÒNG: CHANGELOG.md:413–416; muc-r358-da-va.md:197–200.
VẤN ĐỀ: Số rc/version và giới hạn nền được trích nhưng nhãn(b),chỉ đọc mã,thiếu log sự kiện động đều bị bỏ. Đây là mất cấp chứng cứ, khác việc mất phạm vi R/cả hai sentinel.
ĐÃ THỬ VÁ: không — giữ cả nhóm probe bằng lời kèm nguồn và giới hạn log. Ca kiểm phân biệt đọc mã/chạy thật trong bảng sinh; không dựng payload mới. Nguy cơ gắn rc của ca khác vào nhãn sự kiện này.
ĐÃ THỬ NGHIỆM: `measure.py` bỏ r358:197–199,giữ200 nhờ#493;toàn bảng có0“sự kiện động”. Sự kiện probe KHÔNG ĐO ĐƯỢC vì không có log gốc.
ĐỘ TIN: cao

Đối chứng lịch sử: `python3 -B review-evidence/run-before.py` trên `4af7e2907e86cfcad10c0d097c4678a800d32c04` trả rc0 cho cả bốn cổng bắt buộc; release180/180,claimsok=true,lease121/121,chạy121/bỏ0,receipt96 mục/0vi phạm. Bằng chứng: [gates.json đối chứng](review-evidence/before/gates.json) và stdout/stderr cùng thư mục. Đây là lần chạy độc lập của lượt4, không lấy log head mới thay log bản sai.

Kiểm cuối: exact head `cay-kho/` không đổi; `git status --porcelain` của cây review và ba bản sao đều rỗng. Đủ17 slug đối chiếu, không thiếu/thừa slug;16 heading finding hiện hành = **0 P1 + 1 P2 + 15 P3**, mỗi finding đủ năm trường bắt buộc. **CÒN P2, chưa đạt điều kiện “tới hết P2”.**
