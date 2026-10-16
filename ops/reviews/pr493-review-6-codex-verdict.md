verdict: changes_requested
reviewed_sha: 2c57e99a35c542b3098cf701be12809e44b0b5dd

**KHÔNG CÒN P1; KHÔNG CÒN P2 trong phạm vi review; CÒN 10 P3. Điều kiện “tới hết P3” CHƯA ĐẠT.** Trong 14 P3 lượt 5: **11 ĐÃ VÁ THẬT · 2 VÁ HỜ · 0 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Có thêm 7 P3 về lời khai/bản chiếu hiện hành. Không tính bản sao của cùng lỗi thành finding riêng.

Reviewer: Codex/GPT-6 theo cấu hình phiên, provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`; độc lập với executor Claude theo hồ sơ được giao. Không chứng thực độc lập model/backend. Đây là cross-provider review theo §8, không tự ghi state `cross_approved`, không cấp quyền merge. Authority và điều kiện dừng lấy từ chỉ thị trực tiếp của người dùng lượt 6.

Chỉ đọc/ghi trong workspace, không mạng, không tự soạn payload đường dẫn. `cay-kho/` được giữ read-only; tree `559825ae6c4d0c563cfc71b705fa2219eca0e9d3`, detached, full history. Cổng chạy trên `review-current/`; đột biến trên `review-mutant/`; đối chứng ancestry trên `review-state/`. `TMPDIR` nằm trong workspace; đặt `core.abbrev=7` trên bản sao và thêm thư mục actionlint 1.7.7 vào **cuối** PATH.

Bằng chứng/lệnh tái lập: [measure.py](review-evidence/measure.py), [measurements.json](review-evidence/measurements.json), [extra.json](review-evidence/extra.json), [gates.json](review-evidence/gates.json), [probes.json](review-evidence/probes.json), [final-measures.json](review-evidence/final-measures.json). Stdout/stderr và script đi cùng trong `review-evidence/`. Dòng `CHANGELOG.md` bên dưới tính trong `cay-kho/`; dòng các slice/thân PR tính trong workspace.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Phép quyết định cho bộ trích: chạy chính `trich_khang_dinh.py` với đúng tám đầu vào, theo thứ tự header của bảng; so byte toàn output, rồi kiểm **từng dòng không rỗng tại đúng số dòng trong đúng section**, không chỉ tìm từ khóa. Kết quả 1692/1692, không thiếu dòng nào. Đọc cả phần nối dòng và nhãn nguồn của từng đoạn dưới đây; không coi số dòng là số mệnh đề.

- `tu-thu-tron-hai-tap-nam-finding`: **VÁ HỜ** — CHANGELOG:207–210 nay dẫn đúng lượt 3=P2, lượt 4=P3, khớp heading verdict gốc tại lượt3:109/lượt4:145. CHANGELOG:193–196 đã đổi khái quát thành “đều để sót”. Nhưng `than-pr-493.md:80` vẫn khẳng định cả năm chỉ sửa MỘT bản chiếu. Tự `git diff 4af7e29 9484970 -- ops/reviews/README.md ops/reviews/pr491-review-2-codex-verdict.receipt.yaml`: P1 sửa cả README và receipt, đúng phản ví dụ lượt 5. Phần trộn tập A/B đã đóng không bị mở lại.
- `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`: **VÁ HỜ** — CHANGELOG:250–255 có nhãn tự thuật thiếu log, và có nhắc cả nháp “tám”. Tuy nhiên khối kể nháp riêng ở127–131 không có nhãn/chỉ dẫn tới đó; quan trọng hơn, thân PR:68–69 vẫn kể cả hai sự kiện không kèm giới hạn. Nhãn “cho cả mục này” đặt dưới heading247 không tự đi theo bản chiếu thân PR. Sự kiện nháp/khôi phục vẫn **KHÔNG ĐO ĐƯỢC**, thiếu nháp và log gốc.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — đoạn153–159 ghi rõ nợ và điều kiện đóng, nhưng không sửa cổng. Tự thử ba thay đổi, mỗi ca đúng một byte, giữ833444byte: số1016→1017, số5→6 ở tiêu đề, phép13−2=11→12 đều claims rc0/ok=true; release trên ca1016→1017 rc2, failed chỉ CHANGELOG. Ghi nợ chính xác là cải thiện tài liệu, không làm điều kiện đóng của chính nợ ấy đạt.
- `bo-sot-pham-vi-ref-va-vat-chat-hoa`: **ĐÃ VÁ THẬT** — giữ trọn r358:69–78, gồm thiếu tag/namespace vẫn thành công và vật chất hoá `refs/heads/*`. “vật chất hoá” xuất hiện1lần trong bảng; không còn dòng bị lọc ở đoạn này.
- `bo-sot-tu-khai-evidence-va-manifest`: **ĐÃ VÁ THẬT** — r358:73–78 giữ cả sinh EVIDENCE, cách trích/phần bỏ sót, lập manifest và giới hạn công cụ. Bảng có2hit “cách trích”; đã kiểm hit đúng nguồn, không dùng tên tệp đơn lẻ thay hợp đồng.
- `bo-sot-nguong-hai-client`: **ĐÃ VÁ THẬT** — r358:209–214 giữ điều kiện phải thử ít nhất HAI client trước khi gọi là chính sách; bảng có1hit “HAI client”. Không suy thành hai phép thử mạng đã chạy.
- `bo-sot-pham-vi-r-va-hai-sentinel`: **ĐÃ VÁ THẬT** — r358:195–200 giữ đối tượng R chính nó, lượng từ cả hai và hậu quả, liền với giới hạn nguồn. Chỉ đọc nội dung và kiểm bảo toàn dòng; không dựng probe đường dẫn.
- `bo-sot-hop-dong-phan-loai-nguon`: **ĐÃ VÁ THẬT** — r358:10–25 giữ toàn bộ định nghĩa ba loại, phạm vi canonical/ngoài canonical và lời hứa nhãn tại chỗ; không mất những dòng13–18/21–23 như trước.
- `bo-sot-dieu-kien-chot-so-ci`: **ĐÃ VÁ THẬT** — r358:145–151 và land:156 đều có trong section tương ứng; giữ nhánh in_progress phải trả KHÔNG ĐO ĐƯỢC cùng giới hạn suy nguyên nhân. Bảng có4hit in_progress; không dùng các hit khác thay nhánh điều kiện này.
- `bo-sot-dieu-kien-kich-hoat-workflow`: **ĐÃ VÁ THẬT** — r360:62–72 và thân:101–103 giữ tập sự kiện; ready_for_review có2hit. Parse YAML xác nhận CI pull_request không types; workflow duyệt có4types target và2types review.
- `bo-sot-nhan-attestation-ci-moi`: **ĐÃ VÁ THẬT** — r360:75–100 giữ nhãn(b) riêng cho nhóm duyệt và nhóm CI; land:183 giữ câu thiếu response thô. Số và nhãn đều ở đúng section, không mượn nhãn thân PR để bù.
- `bo-sot-ket-luan-bon-cong-tren-ban-sai`: **ĐÃ VÁ THẬT** — r360:243–245 giữ đủ “không cổng nào”, “đều XANH trên bản sai” cùng bốn tên cổng; các SHA lịch sử/bảng lượt1–3 cũng không mất. Đây là đóng lỗi bảo toàn nội dung bảng; không dùng log head mới chứng nhận lần chạy lịch sử. Bốn cổng tại4af7e29 đã được lượt5 báo đo; lượt6 không chạy lại mốc đó.
- `bo-sot-nhan-ba-luot-vua-them`: **ĐÃ VÁ THẬT** — r360:54–60 và r358:113–117 giữ số ba, nhãn thuật lại và lý do không có verdict gốc. Số lượt lịch sử vẫn KHÔNG ĐO ĐƯỢC độc lập; bảng nay giữ đúng giới hạn này.
- `bo-sot-nhan-probe-vua-them`: **ĐÃ VÁ THẬT** — r358:195–200 giữ nhãn(b), chỉ đọc mã, sự kiện động thiếu log và giới hạn nền; “sự kiện động” có2hit. Không chạy probe mới hoặc gán log ca khác cho sự kiện cũ.

**Kết luận riêng về kiến trúc:** bỏ bộ lọc thực sự đóng cả11slug cũ, không chỉ phần lớn. Không có slug cũ nào còn bị thiếu input. Đơn vị DÒNG và phạm vi đầu vào được tự khai đúng ở docstring:16–23. Nhưng điều này không chứng minh đã chọn đủ nguồn cho những khẳng định MỚI; xem finding về thông điệp commit.

## BẢNG ĐO

“Khớp” chỉ áp cho đại lượng đo được; băm không chứng nhận provenance, số học không chứng thực API.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact HEAD/tree | 2c57e99 | SHA đầy đủ đúng; tree559825ae…; shallow=false, detached, status rỗng | Có |
| Delta so master c31d8f1 | 8tệp,+1383/−26 | Cộng8hàng numstat=1383/26; chỉ CHANGELOG,manifest,land,README,2verdict,2receipt | Có |
| Hai patch và numstat | được sinh từ Git | Cả3tệp byte-exact với git diff tương ứng | Có |
| Master đã merge vào head | c31d8f1 là base | merge-base --is-ancestor c31d8f1 HEAD rc0;7e236cf có hai cha f5098dd và c31d8f1 | Có |
| Master đi trước17commit | từ00e017a | rev-list --count=17; riêng first-parent=2 (#490,#494) | Có;17không phải17merge |
| First-parent PR so base mới | chuỗi sửa PR493 | 9commit:34e9d35,cdd0b1d,4af7e29,9484970,fae2fb7,b004da9,f5098dd,7e236cf,2c57e99 | Có |
| Giữ các heading | r360,r359,r358 | CHANGELOG dòng1,264,384; ba slice byte-exact | Có |
| Phạm vi r359 của master |39tệp,c0a5cbe..8cee941 |39tệp,+7834/−9 | Có |
| Tích hợp README |6hàng#490+2hàng#491 | Đếm riêng bảng Mục lục=6+2; không mất hàng | Có |
| Manifest sau merge | tái sinh,strict xanh | release rc0,ok=true,180/180;hai hash_match=true;failed/errors/extra=[] | Có toàn vẹn; lịch sử thao tác tái sinh là lời khai |
| CHANGELOG/package mới | manifest hiện hành |833444byte;package_hash=87d9f1a1226d627316e56efb44adbca624de9b09e510f3fb7fd2c1e4c5f367f0 | Có |
| Hash gói | ARTIFACTS.sha256 |3243/3243khớp | Có toàn vẹn |
| Bốn bản chiếu | receipt1/2,README,land |4/4byte-exact với tệp trong cây | Có |
| Bộ trích |1692dòng,0bị loại |218+97+200+74+156+214+523+210=1692;1096có số;output byte-exact;0dòng nguồn thiếu | Có trong8input |
| Giới hạn bộ trích |dòng,không phải mệnh đề;input do người gọi chọn |docstring khai cả hai và không phân biệt trích dẫn để bác | Có |
| Số383dòng trong message head |“cùng hai hiện vật”,không ghim mốc |r359+r358 tạif5098dd=383; r360+r358 tại7e236cf=400,tạihead=418 | Chỉ tái lập383trên mốc cũ; message thiếu định danh đầu vào/mốc |
| Các verdict PR493 lượt1–5 |1/4/12;1/4/15;0/2/15;0/1/15;0/0/14 |Đếm heading gốc trong5tệp giao đúng cả5bộ;SHA đều khớp | Có trong gói,không đồng nghĩa có trong repo |
| Hiện vật5lượt trong r360 |heading và mở đầu khai giữ5lượt |PR chỉ thêm2verdict PR491;không cópr493-* trong tree | Không;P3 |
| Hai verdict PR491 |3/5/6 và0/3/10 |heading=14 và13;35088/36958byte;hash38d7fb2e…/14c726e5… | Có |
| Hai receipt PR491 |v2 hợp lệ,t26/t27 |Cả2hash khớp;4+5caveat có trong README;full lease suite đạt;v2 toàn kho0vi phạm | Có |
| Bien_nhan head |message:49v2/tổng102 |rc0;49v2+11legacy+42nợ=102;0vi phạm;0KHÔNG ĐO ĐƯỢC | Có |
| Bien_nhan “trên head này” trong thân PR |43v2/tổng96 |49v2/tổng102 | Không;P3 |
| Nền master c31d8f1 |47v2,0vi phạm |rc0;47v2+11legacy+42nợ=100;0vi phạm | Có |
| Claims strict |ok=true |rc0,ok=true | Có trong phạm vi cổng |
| Lease |121/121,chạy121,bỏ0 |rc0,121/121,chạy121,bỏ0 | Có |
| Doctrine/ADR |sạch |rc0/0;7tệp,0chép;46ADR/46hàng khớp1–1 | Có |
| Đột biến một byte |release chặn |giữ833444byte;rc2,failed chỉCHANGELOG;package_hash_match=false | Có |
| Ba đột biến số |claims không bắt |1016→1017,số5→6 ởheading,13−2=11→12: cả3rc0/ok=true | Có;P3 vẫn sống |
| Land evidence trước/sau |master7tệp,chưa cópr491 |ls-tree c31d8f1=7;head=8,thêm đúngpr491 | Có |
| Lệnh nguyên văn dùng origin/master |đo7tệp |Gói không có remote-tracking ref này:rc128; dùng exact c31d8f1 được7 | Không chạy nguyên văn; dữ kiện tái lập bằng SHA đóng băng |
| #491 nằm ngoài chuỗi đóng |chuỗi chấm dứt#490,không sinh hồ sơ riêng#490 |pr489:416–452 miễn đúng PR land evidence cho#490;#491 là ghi sổ,khác đối tượng | Khớp nội dung quyết định được lưu |
| ADR-0034 |cần bookkeeping cho land |ADR:17–21 đòi evidence/post-merge gate/bookkeeping;không đòi một PR kế nhiệm riêng | Có;không biến thành luật đẻ PR vô hạn |
| Sáu anchor #490 |đúng trênmaster,sai trênHEAD trước merge |63c639a,f7872ac,c42fc74,dccce0a,16663ca,2f783bc: cả6rc1 trênf5098dd;rc0 trênc31d8f1 vàhead | Có |
| Sáu vi phạm do trạng thái đo |merge chưa commit gây6lỗi |Cây tệp7e236cf + HEADf5098dd:rc1,đúng6lỗi ancestry;giữ tệp,HEAD7e236cf:rc0,0lỗi | Có về cơ chế;không chứng nhận log phiên gốc |
| Phân vai “chỗ duy nhất cùng nói” |chỉ#491 merge00e017a |Còn cùng nói39tệp/cùngrange,#490merge và đóngchuỗi | Không;P3 |
| Va chạm bc78656 |lần trước phát hiện TRƯỚC khi viết |Cảbc78656^1 và^2 đã có headingr355;merge message kể giải hai xung đột | Không;P3 |
| Ref snapshot |319heads |for-each-ref refs/heads=319;EVIDENCE khai rõ giới hạn heads và ảnh chụp cục bộ | Có cục bộ;server hiện tại KHÔNG ĐO ĐƯỢC |
| Workflow |hai tập kích hoạt khác nhau |Parse YAML:CI pull_request khôngtypes;duyệt target4types/review2types | Có cấu hình;runtime GitHub KHÔNG ĐO ĐƯỢC |
| CI/approval lịch sử |3đỏ/1xanh,Windows49m09,… |Chỉ có attestation,không response/log gốc | KHÔNG ĐO ĐƯỢC độc lập |
| Số học CI |44=40+4=38+6;biên10m51 |Hai tổng44;3600−2949=651giây;biên cũ705giây,chênh54giây | Có số học,không suy xu hướng |
| Đọc ngược title/body;chỉ thị đóngchuỗi |executor thuật lại |Có snapshot thân PR và lời chỉ thị trong YAML;không raw readback/chỉ thị gốc | KHÔNG ĐO ĐƯỢC provenance |

Lời “6 vi phạm là tạo tác của trạng thái đo” thực tế nằm trong **message7e236cf**, không nằm trong r360 như hướng đào gọi. Phản chứng A/B chỉ đổi HEAD trên cùng cây tệp sau merge, nên xác nhận được nguyên nhân của **đúng sáu lỗi ancestry này**. Không phát hiện câu đó bảo lãnh mọi lỗi merge hay mọi gate. Không biến một cổng đỏ đúng với HEAD cũ thành “cổng sai”.

Quyết định đóng chuỗi có phạm vi cụ thể là #490 không sinh hồ sơ kế nhiệm của chính nó. Không thấy bằng chứng văn bản cấm mọi bookkeeping của PR khác. Vì vậy **không chấm P3** cho việc lập land evidence #491; điều đó cũng không chứng nhận authorization/CI trên GitHub hiện tại.

### tu-thu-tron-hai-tap-nam-finding  [P3]  Khái quát sai vẫn sống trong thân PR
TỆP/DÒNG: than-pr-493.md:80; CHANGELOG.md:193–196,207–214.
VẤN ĐỀ: Lỗi severity đã sửa thật, nhưng bản chiếu thân PR vẫn nói cả năm chỉ sửa MỘT bản chiếu, ngay trước ví dụ sửa cả README lẫn receipt. Cùng slug lượt5, cùng phản ví dụ, không nâng thành P2 vì trạng thái A/B hiện hành không còn bị trộn.
ĐÃ THỬ VÁ: không — đổi khái quát ở thân PR theo phạm vi Git chứng minh, rồi vét trên văn bản đã nối dòng của mọi bản chiếu; không chỉ tìm trong CHANGELOG.
ĐÃ THỬ NGHIỆM: `git diff 4af7e29 9484970 -- ops/reviews/README.md ops/reviews/pr491-review-2-codex-verdict.receipt.yaml` cho hunk ở cả hai tệp; đối chiếu hai heading verdict gốc=P2/P3. Log trong measurements.json/extra.json.
ĐỘ TIN: cao.

### hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap  [P3]  Nhãn thiếu log chưa đi cùng cả hai bản tự thuật
TỆP/DÒNG: CHANGELOG.md:127–131,247–255; than-pr-493.md:68–69.
VẤN ĐỀ: Nhãn mới ở mục cuối không sửa bản chiếu thân PR. Hai lời kể về nháp “tám”, lần thứhai và khôi phục806980/806981 vẫn được dẫn trực tiếp ở đó mà không báo thiếu log. Mục nháp phía trên cũng không chỉ tới nhãn cuối. Thiếu nguồn không có nghĩa lời kể giả; lỗi là cấp chứng cứ không đi cùng lời kể.
ĐÃ THỬ VÁ: không — gắn nhãn tự thuật thiếu log tại mỗi khối kể, hoặc dẫn rõ tới nhãn chung bao phủ đúng hai sự kiện; không dùng byte head mới chứng minh nháp cũ.
ĐÃ THỬ NGHIỆM: đọc r360:127–131/247–263 và thân:66–69, so với bản vá chỉ thêm nhãn ở cuối CHANGELOG. KHÔNG ĐO ĐƯỢC nháp/transcript/lần khôi phục vì không có hiện vật gốc.
ĐỘ TIN: cao về lỗi nhãn,không kết luận sự kiện là giả.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Nợ cổng có địa chỉ nhưng phản chứng đóng vẫn xanh
TỆP/DÒNG: CHANGELOG.md:153–159; scripts/tl.py và cổng doc-claims-check được gọi.
VẤN ĐỀ: Điều kiện mới tự ghi là ba mutant phải ĐỎ; đo lại cảba vẫn XANH. Phần mã cổng không nằm trong delta8tệp. Không thể đóng finding về khả năng kiểm số chỉ bằng việc khai đúng giới hạn đó, nhất là điều kiện dừng nay tới hếtP3.
ĐÃ THỬ VÁ: có — thử ba đột biến trên review-mutant, khôi phục byte sau từng ca; chưa sửa mã cổng. Hướng đóng: cổng kiểm các khẳng định trọng yếu dựa trên dữ liệu có nguồn, và chứng minh cảba mutant bị bác; phải giữ bản không đột biến xanh.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/probes.py`: cảba đổi1byte/giữ833444byte, claims rc0/ok=true; release cađếm rc2/hash_match=false/failed chỉCHANGELOG. Chi tiết probes.json và mutant-*.out.
ĐỘ TIN: cao.

### doi-so-r-con-sot-ban-chieu  [P3]  Đổi heading sang r360 nhưng các chỉ dẫn vẫn trỏ r359
TỆP/DÒNG: CHANGELOG.md:88–89,117,236; than-pr-493.md:1,9,66,82.
VẤN ĐỀ: Những câu hiện hành “chính r359 đang sửa cho r358”, “Đây là thứ r359 sửa”, tiêu đề/thân PR “Mục r359” và bài học “đã đưa vào r359” nay chỉ sang mục master khác nội dung. Không phải mọi hit r359 đều sai: khối va chạm và câu kể “bản đầu” cần giữ số lịch sử. Vấn đề là các tham chiếu hiện hành chưa đổi, phá đúng phân vai vừa thêm.
ĐÃ THỬ VÁ: không — cập nhật từng tham chiếu hiện hành sangr360, giữr359 khi chỉ mục master hoặc mốc lịch sử có nhãn; không thay toàn cục.
ĐÃ THỬ NGHIỆM: `rg -n 'r359|r360' muc-r360.md than-pr-493.md`; ba slice khớp byte với heading thật tại1/264/384. Đọc ngữ cảnh phân biệt tham chiếu hiện hành với trích dẫn lịch sử.
ĐỘ TIN: cao.

### phan-vai-khai-duy-nhat-vuot-noi-dung  [P3]  Hai mục còn trùng nội dung ngoài merge PR491
TỆP/DÒNG: CHANGELOG.md:13–24; muc-r359-cua-master.md:3–5,19,25,36–37,90–100; message7e236cf.
VẤN ĐỀ: Câu “chỗ duy nhất hai mục cùng nói” sai: r360 tự nhắc39tệp/c0a5cbe..8cee941 giống r359, kể #490 đãland/merge và quyết định chuỗi dừng#490 mà r359 cũng kể. Lặp để định vị phạm vi là hợp lý; khẳng định chỉ trùng đúng một sự kiện mới là lỗi.
ĐÃ THỬ VÁ: không — thu hẹp thành phạm vi bổ sung chính của r360 và thừa nhận các sự kiện nền dùng chung; không cần xóa ngữ cảnh hữu ích chỉ để làm đúng lượng từ “duy nhất”.
ĐÃ THỬ NGHIỆM: đối chiếu nguyên văn cảhai slice; `git diff --shortstat c0a5cbe 8cee941` xác nhận39tệp; `git show -s --format=%B 7e236cf` cho cùng lời khẳng định trong message. Có nhiều phản ví dụ ngoài00e017a.
ĐỘ TIN: cao.

### va-cham-r-ke-sai-thoi-diem-cu  [P3]  Va chạm bc78656 cũng xảy ra sau khi đã viết mục
TỆP/DÒNG: CHANGELOG.md:9–11; message7e236cf, khối VA CHẠM SỐ r.
VẤN ĐỀ: Đối chiếu “lần trước phát hiện TRƯỚC khi viết” không được Git hỗ trợ và bị hai cha merge bác trực tiếp: bc78656^1 đã chứa mục r355 về fixture nền; bc78656^2 đã chứa mục r355 về biên nhận v2. Message bc78656 kể hòa giải CHANGELOG và tái sinh manifest, đổi số mục có sẵn. Sai ở khác biệt thời điểm, không sai việc đã từng chiếm số.
ĐÃ THỬ VÁ: không — bỏ đối chiếu trước/sau không đúng; mô tả cảhai lần phải hòa giải hai mục đã tồn tại. Không suy thời điểm tâm lý “phát hiện” từ message nếu không có log.
ĐÃ THỬ NGHIỆM: `git show bc78656^1:CHANGELOG.md`, `git show bc78656^2:CHANGELOG.md`, `git show -s --format=%B bc78656`; cảhai headingr355 có trước merge. Đầu hai blob lưu trong measurements.json.
ĐỘ TIN: cao.

### hien-vat-nam-luot-khong-khop-write-set  [P3]  Mở đầu khai giữ hiện vật năm lượt nhưng PR chỉ nhập hai lượt
TỆP/DÒNG: CHANGELOG.md:1,3–4; numstat.txt:5–8.
VẤN ĐỀ: Heading/mở đầu mới khai “hiện vật5/năm lượt cross-review”. Delta chỉ thêm hai verdict và hai receipt PR491. Tree không cópr493-review-*; chính mục dưới chỉ tóm tắt ba lượtPR493, không chứa nguyên văn năm verdict. Năm VERDICT-LUOT-1..5 có trong gói scratch giao reviewer, nhưng không trở thành hiện vật bền trong repo qua PR này. Cần phân biệt hai phạm vi ấy khi mô tả thứ mục/PR giữ.
ĐÃ THỬ VÁ: không — gọi đúng hai lượtPR491 được nhập kho; nếu muốn nói năm lượtPR493 trong gói, chỉ rõ địa chỉ/phạm vi gói, không gán chúng cho write set hiện tại.
ĐÃ THỬ NGHIỆM: `git ls-tree -r --name-only HEAD ops/reviews/` lọcpr491/pr493 chỉ trả4tệp của2lượtPR491; numstat cũng chỉ thêm4tệp ấy. Đếm năm verdict ngoài cây là5, phân biệt được bằng extra.json.
ĐỘ TIN: cao.

### than-pr-khai-so-cong-cua-head-cu  [P3]  Bảng cổng “trên head này” còn số 43/96 trước merge
TỆP/DÒNG: than-pr-493.md:86,94.
VẤN ĐỀ: Bảng có phạm vi “trên head này” nhưng giữ43ĐẠTv2/tổng96 của trước merge master. Head2c57e99 có49/tổng102; đây là sáu receipt#490 mới nhập. Message head khai đúng không sửa được bảng thân PR đọc ngược. Lỗi báo cáo số, không phải gate đang đỏ.
ĐÃ THỬ VÁ: không — cập nhật dòng số theo exact head hoặc ghim rõ SHA cũ và bổ sung kết quả mới; không chỉ bỏ tên head để biến số cũ thành không kiểm được.
ĐÃ THỬ NGHIỆM: `python3 -B ops/bien_nhan_v2.py` trên review-current rc0,49v2+11legacy+42nợ=102; master riêng47/100. Logs receipt.out và final-measures.json.
ĐỘ TIN: cao.

### bo-sot-khang-dinh-moi-trong-commit  [P3]  Đầu vào bỏ cả nguồn của phép đo sáu vi phạm và số cổng mới
TỆP/DÒNG: BANG_KHANG_DINH.txt (danh sách8section); message7e236cf và2c57e99; trich_khang_dinh.py:20–23.
VẤN ĐỀ: “6vi phạm do trạng thái đo” và phép thử sáu anchor hai chiều chỉ nằm trong message merge; “49ĐẠTv2/tổng102” chỉ nằm trong message head, trong khi bản chiếu thân còn43/96. Cảhai message không được truyền vào script. Bỏ regex không thể đưa những mệnh đề/quan hệ này vào bảng. Việc một vài SHA anchor có mặt qua receipt khác không giữ được phép so hai chiều hay kết luận sáu lỗi. Đây là lỗi THIẾU ĐẦU VÀO mới, không tái mở11slug cũ đã đóng.
ĐÃ THỬ VÁ: không — xuất message commit liên quan thành hiện vật có neo SHA, thêm vào đầu vào và kiểm đoạn kết luận cùng đối tượng/mốc; giữ tự khai giới hạn, không chỉ thêm các từ khóa số.
ĐÃ THỬ NGHIỆM: `git show -s --format=%B 7e236cf` vàHEAD; script final-measures.py xác nhận táminput không có “6 vi phạm”, “49 ĐẠT v2”, “tổng 102”. Đã tự chạy A/B xác nhận dữ kiện bị bỏ có thật và đo lại được. Xem commit_only/merge_uncommitted trong final-measures.json.
ĐỘ TIN: cao.

### mo-ta-bo-trich-va-no-khong-theo-kip-ban-va  [P3]  Lời mô tả bộ trích còn trạng thái cũ và lượng từ quá rộng
TỆP/DÒNG: CHANGELOG.md:161–179; than-pr-493.md:64; trich_khang_dinh.py:6–11; message2c57e99.
VẤN ĐỀ: Khối “Chưa vá” và thân PR vẫn mô tả script đang giữ dòng có số, phải đợi công cụ mới cho tám lỗi, dù script giao lượt này đã giữ cả văn xuôi. Muốn giữ phân hoạch lịch sử phải ghim “ở lượt2/bản cũ” và ghi trạng thái mới. Ngược lại, docstring/message mới lại khẳng định bản cũ vứt sạch MỌI mệnh đề định lượng viết bằng chữ. Chính r360:165–167 đã bác cách nói ấy: dòng có chữ số khác vẫn được giữ. Ví dụ r358:113 nói “ba lần lặp” cùng `t33`, regex cũ giữ nó. Do đó triển khai đã tiến bộ nhưng các mô tả phạm vi/trạng thái không nhất quán.
ĐÃ THỬ VÁ: không — ghim phân hoạch8+1+1 vào mốc lịch sử, cập nhật trạng thái sau bỏ lọc; thu hẹp “mọi mệnh đề bằng chữ” thành “các dòng không có chữ số”. Giữ nguyên sự khác nhau giữa thiếu đầu vào và lọc dòng.
ĐÃ THỬ NGHIỆM: tái dựng1692dòng cho bản mới; `re.search(r'\d', dòng113 của muc-r358-da-va.md)` trảTrue dù có định lượng “ba lần lặp”. Kết quả trong extractor-history.json; đọc khối161–179 và thân64 xác nhận lời mô tả cũ còn ở thì hiện hành.
ĐỘ TIN: cao.

**Kết luận exact SHA: 0 P1 · 0 P2 · 10 P3; changes_requested.** Các cổng được yêu cầu đã đạt nhưng không thay thế kiểm đúng lời khai. Những phần GitHub/log gốc không được giao đã ghi KHÔNG ĐO ĐƯỢC, không coi là pass và cũng không tự coi là lỗi. Không sửa kho thật, không đăng review hoặc thực hiện merge.
