verdict: changes_requested
reviewed_sha: fae2fb77fc2121af9f94cd026db0179b4e8ed9bc

**KHÔNG CÒN P1 trong phạm vi PR #493 được review.** P1 mâu thuẫn nợ lúc merge đã đóng. Còn **2 P2 · 15 P3**, gồm các nợ cũ và bốn finding mới. Điều kiện dừng “hết P1 hoặc approve” của chủ kho đã đạt nhánh **hết P1**; verdict này không phải `approve`, không cấp quyền merge và không xác nhận CI của nhánh PR thật.

Reviewer: Codex/GPT-6 theo chỉ dẫn phiên; provider OpenAI; execution surface API với shell cục bộ; transport machine. Khác provider executor Claude theo hồ sơ được giao; không có chứng thực độc lập model/backend. Authority review và write set là chỉ thị trực tiếp của người dùng: review exact SHA nhánh nháp, ghi kết quả trong workspace. Không tự chuyển trạng thái kho thành `cross_approved`.

Tree: `d7fafa50360c8d0b225484f1d3a1f9ea57fd23b3`. Không mạng, không commit/push/merge, không tự soạn payload đường dẫn. `cay-kho/` được giữ read-only; các cổng chạy trong bản sao `review-current/`, đối chứng cũ trong `review-before/`; `TMPDIR` đặt trong workspace. Thư mục chứa actionlint 1.7.7 được thêm vào CUỐI PATH; `core.abbrev=7` trên bản sao. Các đường dẫn kho dưới đây tương đối với `cay-kho/`; các tệp gói ở ngay workspace.

Bằng chứng tự đo: [measurements.json](review-evidence/measurements.json), [extra.json](review-evidence/extra.json), [gates.json](review-evidence/gates.json), [mutations.json](review-evidence/mutations.json), [sweep.json](review-evidence/sweep.json), [omitted.txt](review-evidence/omitted.txt), [bảng tái dựng](review-evidence/rebuilt-table.txt). Script: `review-evidence/measure.py`, `run-gates.py`, `run-before.py`, `mutate.py`; stdout/stderr được giữ trong các tệp `.out`. Không dùng số của verdict trước làm kết quả chạy lượt này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `no-luc-merge-dem-ca-hai-p2-da-dong`: **ĐÃ VÁ THẬT** — verdict PR491 có 13 heading = 3 P2 + 10 P3; receipt có đúng hai `da_va: true`. Receipt:7–9,46–51,201–210 và README:18,278 nay phân biệt 13 lúc review/11 lúc merge, bot đếm riêng. Hai điểm giữ P1 lượt 2 đã sửa; số 11 được giới hạn bởi attestation ở receipt:48–50 và mục lục README:278. Phép vét không tìm được bản chiếu hiện hành còn khẳng định 13 lúc merge; các câu còn chứa 13 là mốc review hoặc trích câu sai để bác. **Đóng mâu thuẫn, không chứng nhận sự kiện sửa body PR491.**
- `nhan-nguon-van-va-than-de-nguyen-khung`: **VÁ HỜ** — khung (a) ở CHANGELOG:209–212 đã thu hẹp; số ba lượt và probe có nhãn mới tại39–40,308–309,388–391. Nhưng368–370 vẫn mô tả khung hiện hành là xếp “mọi số Git” vào(a), không nói đó là khung cũ. Chuỗi bị ngắt dòng nên grep nguyên câu bỏ qua. Heading:1 và body:7 cũng vẫn ghi vá5 finding trong r358, trong khi tiêu đề phụ mới phân biệt đối tượng/đóng sạch. Có lỗi mới riêng về trộn hai tập năm, ghi bên dưới.
- `dong-chin-p3-khong-deu-can-bo-trich-moi`: **ĐÃ VÁ THẬT** — đọc đủ10 P3 của verdict PR491:8 lỗi lọc,1 thiếu input,1 giới hạn cổng. CHANGELOG:124–139, receipt:109–119 và body:57 đều có8+1+1 và sửa thiếu input bằng script hiện có. Không còn câu hiện hành “đóng chín cái đầu” hay hoãn toàn nhóm trong các bản chiếu được giao.
- `nhan-attestation-khong-di-cung-ban-tom-tat`: **ĐÃ VÁ THẬT** — CHANGELOG:55–68 và body:17 nay gắn nhãn attestation/thiếu response cho nhóm CI, approval, Windows đầu tiên; body còn tách phép cộng/trừ khỏi sự kiện. Land evidence:8–11 khớp giới hạn ấy. Nhóm số là nguồn thuật lại, không được nâng thành phép đo API độc lập.
- `suy-mat-ref-thanh-mat-object-tuc-thi`: **ĐÃ VÁ THẬT** — CHANGELOG:111–113,362–371, README:19, receipt:125, body:50 đã dùng giới hạn clone canonical tương lai; câu mạnh cũ chỉ còn được trích để bác. Tự chạy ancestry trả1, `for-each-ref --contains` trả đúng2 ref. Không xóa ref hoặc suy về GC máy chủ.
- `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`: **CHƯA VÁ** — CHANGELOG:96–100,185–191 và body:61–62 vẫn thiếu bản nháp “8” và log verifier806980/806981/khôi phục. Blob đã commit đo được815113→818093 byte, không thay thế chứng cứ bản nháp chưa commit.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — trên bản sao exact head, đổi đúng1 byte, giữ818093 byte làm release rc2; đổi1016→1017 và13−2=11→13−2=12 đều claims rc0/ok=true. Mã cổng không đổi trong PR.
- `bo-sot-pham-vi-ref-va-vat-chat-hoa`: **CHƯA VÁ** — CHANGELOG:261,263–265 bị lọc. Receipt/README thêm vào bảng có bổ sung cảnh báo heads/namespace, nhưng không mệnh đề vật chất hóa ref; tìm “vật chất” trong toàn bảng không có. Đây không còn là bỏ TOÀN BỘ phạm vi heads, mà vẫn thiếu phần hợp đồng đã nêu trong slug.
- `bo-sot-tu-khai-evidence-va-manifest`: **CHƯA VÁ** — CHANGELOG:266–267 vẫn bị lọc; bảng không có mệnh đề sinh EVIDENCE kèm cách trích/phần bỏ sót rồi lập manifest. Băm3207/3207 đúng không chứng minh sự kiện dựng gói.
- `bo-sot-pham-vi-nen-chua-do`: **ĐÃ VÁ THẬT** — slice nay gồm cả đoạn; CHANGELOG:391 (=muc-r358:199) có `#493`, nên nguyên câu Linux+Bash/chưa macOS–Windows native được giữ trong bảng. Receipt:193 cũng góp giới hạn nền. Đây là đóng độ phủ câu văn, không phải đã chạy hai nền native.
- `bo-sot-nguong-hai-client`: **CHƯA VÁ** — CHANGELOG:402–403 nay nằm trong input nhưng vẫn không chữ số; bảng không có “HAI client”/“hai client”. Đọc CLAUDE:580–581 xác nhận ngưỡng ít nhất hai client; không gọi client mạng.
- `bo-sot-pham-vi-r-va-hai-sentinel`: **CHƯA VÁ** — CHANGELOG:387–389 nằm trong input nhưng bị lọc: mất phạm vi R chính nó và “cả hai”. Bảng giữ một ca sentinel CÒN ở bảng cổng, không thay thế ca khác bị xóa. Không dựng probe mới; sự kiện động KHÔNG ĐO ĐƯỢC vì không có log gốc.
- `bo-sot-input-than-pr-va-duoi-r358`: **ĐÃ VÁ THẬT** — đo byte: r359=CHANGELOG1–192; r358=193–424; heading kế425. Cả hai slice bằng byte khối heading tương ứng, không thiếu đuôi hoặc lẫn mục. Script nhận đủ5 input; tái tạo bảng bằng byte. Receipt và README ngoài kho cũng bằng byte bản trong kho. Không suy việc này phục hồi body PR491 lịch sử.
- `bo-sot-hop-dong-phan-loai-nguon`: **CHƯA VÁ** — CHANGELOG:202,205–210,213–215,217 vẫn bị lọc. Bảng giữ câu phủ định “mọi số Git” tại211 nhưng mất định nghĩa canonical(a), ngoài canonical(c) và lời hứa nhãn tại chỗ; thêm ba input không cấp nguyên hợp đồng ấy.
- `bo-sot-dieu-kien-chot-so-ci`: **CHƯA VÁ** — CHANGELOG:341–343 vẫn mất. Body:21 giữ completed/0 null; toàn bảng chỉ có in_progress ở chuyện lịch sử hoặc review khác, không có nhánh phải trả KHÔNG ĐO ĐƯỢC và giới hạn suy nguyên nhân của quy tắc này.
- `bo-sot-gioi-han-du-lieu-run-json`: **VÁ HỜ** — đủ đuôi nên35 khóa/3 khóa nay được giữ; README:291–292 bổ sung không argv/model và nhãn attestation. Nhưng CHANGELOG:418,423 vẫn mất: không có danh sách `chuong_trinh`, `so_doi_so`, `van_tay` trong bảng. Parse hai run.json cho35 khóa cấp cao, đúng3 khóa trong `lenh`; bảng vẫn không chứa trọn mệnh đề cấu trúc cần kiểm.
- `bo-sot-dieu-kien-kich-hoat-workflow`: **CHƯA VÁ** — CHANGELOG:45,49–51 và body:96 vẫn bị lọc; toàn bảng không có `ready_for_review`. Parse YAML xác nhận CI khai pull_request không types, duyệt khai4 types pull_request_target và2 types pull_request_review. Không xác nhận sự kiện runner từ cấu hình.
- `bo-sot-nhan-attestation-ci-moi`: **VÁ HỜ** — body:17 nay được giữ trọn, nên bảng có một bản tóm tắt CI mang nhãn đúng. Nhưng bản chiếu r359 vẫn giữ số CI và lọc mất chính nhãn nguồn mới ở CHANGELOG:55,64–65,67; chúng không đi cùng các dòng số của input đó. Đóng finding nội dung body ở trên không đồng nghĩa đóng việc trích nhãn ở mọi bản chiếu.
- `bo-sot-anh-xa-phan-hoach-tam-mot-mot`: **ĐÃ VÁ THẬT** — dù các dòng giải thích r359 vẫn bị lọc, body:57 nay được trích nguyên một dòng chứa đủ8 lỗi lọc/1 thiếu input/1 giới hạn cổng, tên hai slug đặc biệt và cách cấp input không cần công cụ mới. Bảng đã có đủ ánh xạ và cách đóng mà finding này đòi; không yêu cầu mọi câu lặp phải được chép lại.
- `bo-sot-ket-luan-bon-cong-tren-ban-sai`: **CHƯA VÁ** — CHANGELOG:179–180 vẫn bị lọc,181 được giữ vì tên bien_nhan_v2. Không input mới nào đưa nguyên kết luận “không cổng nào bắt cái nào” cùng phạm vi năm lời khai/bốn cổng vào bảng. Tự chạy bốn cổng trên4af7e29 đều rc0, xác nhận câu bị bỏ là một kết quả dương thật.

Tổng: **7 ĐÃ VÁ THẬT · 3 VÁ HỜ · 10 CHƯA VÁ · 0 VÁ SINH LỖI MỚI** cho20 slug cũ. Bản vá source còn phản ví dụ cũ nên xếp VÁ HỜ; lỗi phát sinh độc lập được ghi riêng, không dùng nhãn này để che nó. So với lời khai “15 P3 chưa vá”, ba P3 đã đóng thật (input, nền, ánh xạ), hai P3 cải thiện một phần (run.json, nhãn CI).

## BẢNG ĐO

Các dòng gộp mệnh đề lặp; khớp số học hoặc nội dung tệp không chứng minh sự kiện GitHub. Những hiện vật bị bảng giao việc bỏ vẫn được reviewer đọc trực tiếp. Phép vét có240 hit, gồm cả các câu lịch sử/trích để bác, không phải240 finding.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Head/tree | fae2fb7 trên nhánh nháp | OID đầy đủ và tree như đầu verdict; detached, sạch | Có; head PR thật KHÔNG ĐO ĐƯỢC |
| Root/kho đầy đủ | kho đầy đủ | root394e93468fc8d84ec20938e6df8fb7ab72b2cc37; shallow=false | Có |
| Delta toàn PR |8 tệp,+1309/−26 từ numstat|Git và numstat bằng byte; tổng8,+1309,−26|Có|
| CHANGELOG thêm~276 |phần PR so base|+276/−21 so00e017a; riêng9484970→head +44/−10, tăng34 dòng/2980 byte|Có so base; không phải276 dòng mới ở lượt3|
| Delta lượt2→3 |patch được giao|4 tệp,+69/−24; patch bằng byte Git|Có|
| Prompt sai lượt1 được nhắc lại |+1196/−20 thay+1350/−5|git diff00e017a..4af7e29:8,+1196,−20|Có số sửa; nguồn base cũ của lỗi là tự thuật|
| Loại tệp đổi |hồ sơ/manifest|8 tệp; không sửa mã thực thi hoặc workflow|Có|
| Băm gói |ARTIFACTS.sha256|3207/3207 đúng|Có tính toàn vẹn; không chứng thực quá trình sinh|
| Ref |319/319/319, lệch0/0|3 TSV bằng byte; git heads319|Có snapshot; server hiện tại KHÔNG ĐO ĐƯỢC|
| Phạm vi ref |heads, không tag/namespace khác|đọc builder và EVIDENCE đúng|Có; không suy mọi ref|
| Input theo heading |đủ r359/r358|1–192/193–424; heading kế425; byte-exact|Có, đóng mất đuôi|
| Năm input bảng |thêm receipt và README|83+124+48+121+428=804 dòng có số; output bằng byte|Có; không phải804 mệnh đề độc lập|
| Hai bản chụp receipt/README |bản kho hiện tại|2/2 bằng byte|Có|
| Trích bao gồm cả hai bảng README |cảnh báo và mục lục|có hàng18,19 và278 trong bảng tái dựng|Có|
| Chuỗi merge |7, #486 trước #480|first-parent:#468,#477,#478,#486,#480,#487,#489|Có|
| Payload |1016 tệp,+247458, chỉops|Git đúng; tập thư mục cấp1={ops}|Có|
| Land evidence |6 trước, thứ7 mới|ls-tree c0a5cbe/00e017a/head:6/6/7|Có|
| Head PR491 merge |2ec6171f…|cha thứ2 của00e017a=2ec6171f7a2e21ae950633f9e328329a355f7a6d|Có quan hệ Git; không chứng minh approval|
| Verdict PR491 lượt1 |3P1/5P2/6P3=14|đếm heading đúng|Có|
| Verdict PR491 lượt2 |0P1/3P2/10P3=13|đếm heading đúng|Có|
| Hai verdict nguyên byte |35088/36958, băm receipt|size và SHA256 đều khớp; lượt3 không sửa verdict|Có|
| SHA256 verdict1 |38d7fb2e…|38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c|Có|
| SHA256 verdict2 |14c726e5…|14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468|Có|
| Commit đầu chứa verdict |34e9d35…|log diff-filter=A cả hai=34e9d35be0fc52406e3659bfc24c388bf54262cd|Có|
| Caveat |4+5=9|parse4/5 ID, t27 trong suite đạt|Có|
| Nợ merge |13 review,11 merge; không11+5|13 heading,2 da_va:true;13−2=11; các bản chiếu đã nhất quán|Có về hồ sơ; sửa body lịch sử KHÔNG ĐO ĐƯỢC|
| Bot |5P2,3 mới/2 trùng,4 đúng/1 một phần|parse đúng5,3/2,4/1|Có theo receipt; bot API KHÔNG ĐO ĐƯỢC|
| Phân hoạch10 P3 PR491 |8+1+1|đọc10 slug đúng8 lọc,1 input,1 cổng|Có|
| Review PR493 lượt1/lượt2 |1/4/12 và1/4/15|đếm hai verdict được giao đúng|Có|
| Đối chiếu lượt2 |0 thật,6 hờ,11 chưa|parse17 slug đối chiếu đúng;3 P3 mới không thuộc17|Có|
| Bốn hiện vật chứa năm finding PR493 |CHANGELOG,README,receipt,body|địa chỉ trong verdict2 đúng4 loại hiện vật|Có phạm vi; không chỉCHANGELOG|
| Năm đối tượng r358 đều bị lượt2 chấm VÁ HỜ |CHANGELOG89–92|năm đối tượng PR491/bot khác tập1P1+4P2 PR493|Không, lỗi mới|
| Chỗ sửa P1 lượt trước |CHANGELOG155:“sửa mục CHANGELOG”|patch4af7e29→9484970 còn sửa caveat/ID ởREADME vàreceipt; body73 kể đúng phần đó|Tự thú hẹp hơn lịch sử sửa thật|
| Cross-review “bên trên” |CHANGELOG92|heading cross-review ở144, phía dưới|Không|
| “Lần thứ sáu kho gặp hình dạng ấy” |CHANGELOG149/body73|không có danh sách6 sự kiện và quy tắc đơn vị/khử trùng|KHÔNG ĐO ĐƯỢC con số6|
| “Ba lượt liền” t33 |mới có nhãn thuật lại|nhãn thật ở39–40,308–309; không đủ chuỗi verdict/log lịch sử để đếm|Nhãn đúng giới hạn; số lịch sử KHÔNG ĐO ĐƯỢC|
| Tự thú nháp8/checkout |8;806980/806981|không có bản nháp/log tương ứng|KHÔNG ĐO ĐƯỢC; không suy tự thú sai|
| Khung nguồn |canonical(a),thuật lại(b),ngoài canonical(c)|đầu đã sửa, cuối368–370 vẫn gán khung cũ|Không đồng bộ|
| Bảng builder |6 hàng, hàng đầu3 ca|6 hàng dữ liệu,8 ca khi tách đầu; nhãn theo ca ở277–284|Có cấu trúc; các rc động lịch sử KHÔNG ĐO ĐƯỢC|
| OID ngoài canonical |không ancestor,2 ref chứa|ancestry rc1; đúng hai ref heads/mirror-cuc-bo của nhánh spec|Có; không suy mất object tức thì|
| Manifest c0a5cbe→2ec6171 |8075509→8089302;bcde19d5→d47be343|đọc hai blob đúng|Có|
| Manifest lượt2→3 |8109435→8112415|tăng2980;CHANGELOG815113→818093 cũng tăng2980|Có|
| Package hash head |ffc62c06…|ffc62c064a8b34347ac28fec02be7d3b592b7dc3578ae2c336b2b98424112761|Có, release tự xác minh|
| Release strict head |ok=true,180/180|rc0,ok=true,failed/errors/extra rỗng,hai hash_match=true|Có|
| Claims strict head |ok=true|rc0,ok=true|Có, không đo sự thật số học|
| Lease head |121/121,chạy121,bỏ0|rc0, đúng121/121,chạy121,bỏ0|Có|
| Receipt head |43v2,tổng96,0vi phạm|43+11legacy+42nợ=96;0vi phạm,0KHÔNG ĐO ĐƯỢC;rc0|Có|
| Doctrine/ADR |rc0/0|7 tệp,0chép doctrine;46ADR/46hàng;rc0/0|Có|
| Bốn cổng trên bản sai4af7e29 |đều xanh|tự checkout bản sao,release/claims/lease/receipt đều rc0;lease121/121|Có; log ởreview-evidence/before|
| Một byte có răng |release chặn|đúng1 byte khác,size818093 không đổi;rc2,failed chỉCHANGELOG,hash_match=false|Có|
| Claims kiểm số sai |giới hạn đã khai|1017 và13−2=12 đều rc0/ok=true|Có giới hạn; không coi đó là P1 mới|
| t33 thiếu công cụ |AssertionError trước subprocess|mock shutil.which=None,gọi thẳngt33:AssertionError,0 subprocess|Có hành vi hiện tại; không đo3 lượt lịch sử|
| run.json14/15 |35 khóa cấp cao,lenh3|parse cả2 đúng35 và{chuong_trinh,so_doi_so,van_tay}|Có; model runtime KHÔNG ĐO ĐƯỢC|
| CI/approval lịch sử |3đỏ/1xanh;approval;Windows đầu tiên|nhãn attestation đã có, không raw response được giao|KHÔNG ĐO ĐƯỢC độc lập|
| CI số học |44=40+4,44=38+6;20m38s/49m09s|44/44;1238s/2949s|Có số học, không xác nhận job|
| Biên Windows |10m51s dưới60, hẹp hơn11m45s|3600−2949=651;3600−2895=705;hẹp54s|Có số học;2 điểm không chứng minh xu hướng|
| Workflow |hai tập sự kiện khác nhau|ci:push master,pull_request khôngtypes,dispatch;duyệt:target4types/review2types|Có cấu hình; sự kiện thật KHÔNG ĐO ĐƯỢC|
| Gói được sinh/readback body/đăng verdict |tự khai script/API,byte-exact|băm và bản giao đọc được;không response/log vận chuyển độc lập|KHÔNG ĐO ĐƯỢC provenance|

### nhan-nguon-van-va-than-de-nguyen-khung  [P2]  Đầu khung nguồn đã sửa nhưng cuối vẫn mô tả khung cũ
TỆP/DÒNG: CHANGELOG.md:1,209–212,368–370; than-pr-493.md:7.
VẤN ĐỀ: Đầu mục nay giới hạn(a) theo canonical, nhưng cuối vẫn nói khối đầu “xếp mọi số Git vào(a)” như một lỗi hiện hành. Câu bị xuống dòng giữa “số” và “Git”, nên grep chuỗi một dòng không đủ vét. Heading chính và dòng tóm tắt body cũng chưa theo phân biệt đối tượng được sửa/finding đóng sạch. Đây là phản ví dụ còn sống của finding cũ, dù nhãn ba lượt/probe đã tiến bộ thật.
ĐÃ THỬ VÁ: không — sửa đoạn368 thành mô tả khung TRƯỚC bản vá; đồng bộ heading và body với phạm vi đã chứng minh. Kiểm cả đoạn sau khi nối dòng, rồi đối chiếu định nghĩa(a). Nguy cơ: thay toàn cục làm sai những trích dẫn lịch sử cần giữ; phân biệt câu trích để bác với kết luận hiện hành.
ĐÃ THỬ NGHIỆM: đọc đủ hai đoạn; sweep.json tìm cả chuỗi nhiều dòng; exact diff xác nhận đầu đổi,cuối không đổi. Gate claims xanh không xác nhận nhất quán nội dung.
ĐỘ TIN: cao

### tu-thu-tron-hai-tap-nam-finding  [P2]  Tự thú mới gán kết quả PR493 cho năm đối tượng khác của PR491
TỆP/DÒNG: CHANGELOG.md:86–92,102–119,144–155; than-pr-493.md:45–57,68–75.
VẤN ĐỀ: Sau tiêu đề NĂM ĐỐI TƯỢNG r358, câu “lượt2 phân loại cả năm VÁ HỜ” rồi “danh sách dưới đây giữ nguyên năm đối tượng ấy” gắn kết quả vào tập gồm nhãn lịch sử,OID,gói,#490,heads. Nhưng năm VÁ HỜ mà verdict PR493 nói là P1 nợ merge và4P2 về khung nguồn,phân hoạch,CI,ref. Hai tập không bằng nhau; ví dụ nợ merge không nằm trong danh sách năm r358, còn gói/#490 không có trong năm P1/P2 PR493. Tự thú155 nói chỉ sửa CHANGELOG cũng bỏ qua các sửa README/receipt thật, chính body73 đã kể. Dẫn “cross-review bên trên” ở92 còn sai hướng: heading ở144.
ĐÃ THỬ VÁ: không — tách tên hai tập theo PR/slug, chỉ gán trạng thái cho tập được verdict đánh giá; sửa chỉ dẫn sang mục phía dưới và kể đúng phạm vi patch trước. Kiểm bằng bảng ánh xạ slug nguồn→đối tượng, bảo đảm không chuyển tín dụng giữa hai tập cùng có5 phần tử. Nguy cơ: đổi mọi chữ “năm” thành cùng một nhãn sẽ tái tạo lỗi ở nhóm khác.
ĐÃ THỬ NGHIỆM: đọc10 heading P3 và5 heading P1/P2 PR493, danh sách r358 và diff4af7e29→9484970; các tập có nhân chứng khác nhau như trên. Đây là lỗi nghĩa mới trong hunk thêm lượt3, không phải sai phép cộng.
ĐỘ TIN: cao

### hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap  [P3]  Hai tự thú cũ vẫn không có bản nháp và log đối chứng
TỆP/DÒNG: CHANGELOG.md:96–100,185–191; than-pr-493.md:61–62.
VẤN ĐỀ: Số8, lần thứhai và verifier806980/806981 vẫn chỉ có lời tự kể. Không có nguyên liệu để tái dựng sự kiện khôi phục làm mất bản vá. Blob đã commit không bác được một bản nháp chưa commit.
ĐÃ THỬ VÁ: không — gắn nhãn tự thuật chưa có log tại các câu này; nếu có nguyên liệu, ghim bản nháp và log trong hiện vật riêng. Kiểm liên kết/byte nguồn; tránh dùng số byte head thay số byte bản nháp.
ĐÃ THỬ NGHIỆM: measure.py đọc blob qua git show, cho815113/818093; kiểm hiện vật được giao không có log hai kích thước kể trên. Sự kiện và số lần KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về thiếu chứng cứ, không kết luận tự thú giả

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Cổng claims tiếp tục chấp nhận số lượng và phép trừ sai
TỆP/DÒNG: CHANGELOG.md:1,162,193; scripts/tl.py; RELEASE_MANIFEST.json.
VẤN ĐỀ: Toàn vẹn byte và kiểm cú pháp dẫn chiếu không chứng nhận sự thật của lời khai. Đây là giới hạn cũ được xác nhận, không phải thay đổi mã gây P1.
ĐÃ THỬ VÁ: có — đột biến trên bản sao rồi phục hồi nguyên byte, không sửa cổng. Hướng rẻ: giữ nợ có địa chỉ và kèm script đo từng mệnh đề quan trọng; nếu làm cổng mới phải có mutant số sai bị chặn. Tránh sinh manifest từ mutant rồi gọi đó là chứng cứ nội dung đúng.
ĐÃ THỬ NGHIỆM: python3 -B review-evidence/mutate.py: release một byte rc2; claims1017 và13−2=12 rc0/ok=true. Hai bản cây sạch sau khôi phục.
ĐỘ TIN: cao

### bo-sot-pham-vi-ref-va-vat-chat-hoa  [P3]  Thêm nguồn chưa đưa bước vật chất hóa ref vào bảng
TỆP/DÒNG: CHANGELOG.md:261–265; trich_khang_dinh.py:15–18.
VẤN ĐỀ: Bảng nay có heads/namespace qua receipt/README, nhưng mất câu ref namespace khác vẫn thành công và bước vật chất hóa nhánh. Không có “vật chất” trong toàn804 dòng được giữ.
ĐÃ THỬ VÁ: không — bổ sung nguyên mệnh đề hợp đồng cùng nguồn ở bảng; kiểm phạm vi heads và vật chất hóa là hai ý có mặt. Tránh đổi cảnh báo snapshot thành lời hứa mọi namespace.
ĐÃ THỬ NGHIỆM: tái chạy script5input byte-exact; omitted.txt ghi263–265;3TSV319 bằng byte. Trạng thái máy chủ hiện tại KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-tu-khai-evidence-va-manifest  [P3]  Hợp đồng sinh EVIDENCE và manifest vẫn bị lọc
TỆP/DÒNG: CHANGELOG.md:266–267; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Dòng không chữ số nói sinh EVIDENCE với cách trích/phần bỏ sót và lập manifest không được giữ. Các bảng băm không thay thế hợp đồng này.
ĐÃ THỬ VÁ: không — đưa nguyên đơn vị khẳng định vào bảng kèm vị trí nguồn; kiểm có đủ cả đầu ra và giới hạn. Tránh suy nguồn gốc từ việc băm khớp.
ĐÃ THỬ NGHIỆM: measure.py bỏ266–267; xác minh3207/3207 băm. Không chạy builder có mạng; sự kiện dựng gói KHÔNG ĐO ĐƯỢC độc lập.
ĐỘ TIN: cao

### bo-sot-nguong-hai-client  [P3]  Ngưỡng hai client vào input nhưng vẫn rơi khỏi bảng
TỆP/DÒNG: CHANGELOG.md:402–403; CLAUDE.md:580–581.
VẤN ĐỀ: Sửa ranh giới slice đã đưa quy tắc vào đầu vào; regex vẫn bỏ cả câu mang ngưỡng bằng chữ. Đây là dời nguyên nhân mất dữ liệu từ hai tầng xuống một tầng, chưa đóng finding.
ĐÃ THỬ VÁ: không — bổ sung quy tắc với ngưỡng và điều kiện kết luận; ca kiểm phải tìm toàn mệnh đề, không chỉ chữ client. Tránh tạo cảm giác đã thực hiện hai phép thử mạng.
ĐÃ THỬ NGHIỆM: tái trích5input; tìm cả “HAI client” và “hai client” trong bảng:0. Đọc CLAUDE xác nhận quy tắc; các lần thử lịch sử KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-pham-vi-r-va-hai-sentinel  [P3]  Bảng mất đối tượng R chính nó và lượng từ cả hai
TỆP/DÒNG: CHANGELOG.md:387–389; muc-r358-da-va.md:195–197.
VẤN ĐỀ: Mệnh đề phạm vi của chốt và hậu quả trên cả hai sentinel không số vẫn bị bỏ. Ca sentinel còn nguyên ở bảng builder là một ca khác.
ĐÃ THỬ VÁ: không — bổ sung bằng lời cả phạm vi, hậu quả và nhãn sự kiện thuật lại. Kiểm đủ ba thành phần, không dựng chuỗi đường dẫn mới. Nguy cơ: ghép nhầm nhãn/rc từ ca khác.
ĐÃ THỬ NGHIỆM: script5input giữ bảng builder nhưng bỏ387–389; đọc mã builder hỗ trợ nhận xét tĩnh. Hậu quả động KHÔNG ĐO ĐƯỢC vì không có log probe.
ĐỘ TIN: cao về thiếu mệnh đề

### bo-sot-hop-dong-phan-loai-nguon  [P3]  Bảng vẫn không giữ trọn định nghĩa ba loại nguồn
TỆP/DÒNG: CHANGELOG.md:202–217; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Các định nghĩa(a)/(b)/(c) và lời hứa nhãn tại chỗ bị tách mất; câu phủ định “mọi số Git” còn lại không đủ xác định hợp đồng mới.
ĐÃ THỬ VÁ: không — trích cả khối định nghĩa, gắn loại nguồn vào mệnh đề được đo; kiểm đủ canonical/ngoài canonical/thuật lại. Nguy cơ: biến danh mục nguồn thành chứng thực cho sự kiện chưa đo.
ĐÃ THỬ NGHIỆM: omitted.txt có202,205–210,213–215,217;selected.txt giữ211,216. Tái trích bảng bằng byte.
ĐỘ TIN: cao

### bo-sot-dieu-kien-chot-so-ci  [P3]  Bảng vẫn thiếu nhánh in_progress phải từ chối chốt số
TỆP/DÒNG: CHANGELOG.md:341–343; than-pr-493.md:21.
VẤN ĐỀ: Bảng có completed và0null nhưng không có quy tắc in_progress phải trả KHÔNG ĐO ĐƯỢC, cũng mất giới hạn suy nguyên nhân lịch sử. Một hit in_progress thuộc review khác không thay thế quy tắc này.
ĐÃ THỬ VÁ: không — bổ sung cả hai nhánh và giới hạn suy luận; kiểm mệnh đề cùng phạm vi. Nguy cơ: biến điều kiện đo đúng thành giải thích nguyên nhân run cũ.
ĐÃ THỬ NGHIỆM: tái trích5input bỏ341–343; rà từng hit in_progress trong bảng. Run/API lịch sử KHÔNG ĐO ĐƯỢC offline.
ĐỘ TIN: cao

### bo-sot-gioi-han-du-lieu-run-json  [P3]  Số khóa đã trở lại nhưng danh sách khóa con vẫn mất
TỆP/DÒNG: CHANGELOG.md:417–423; reviews-README.md:291–292.
VẤN ĐỀ: Cấp đủ đuôi và README đã bổ sung35/3 cùng không argv/model; song bảng không có tên ba khóa con ở418. Do đó chưa biểu diễn nguyên mệnh đề cấu trúc đã dùng để bác lời tóm tắt cũ.
ĐÃ THỬ VÁ: không — giữ cả object cha,tên khóa và giới hạn tự khai; ca kiểm parse hai JSON rồi so với đơn vị khẳng định. Tránh lại nói cả run.json chỉ có ba khóa.
ĐÃ THỬ NGHIỆM: measure.py parse cả hai:35 khóa cấp cao,lenh3 khóa; tìm chuong_trinh trong bảng:0. Model backend KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-dieu-kien-kich-hoat-workflow  [P3]  ready_for_review vẫn không xuất hiện trong bảng
TỆP/DÒNG: CHANGELOG.md:45,49–51; than-pr-493.md:92–96; .github/workflows/ci.yml; .github/workflows/duyet-khac-danh-tinh.yml.
VẤN ĐỀ: Bảng giữ phần CI có số nhưng bỏ nguyên tập sự kiện duyệt có ready_for_review. Người đọc bảng không đủ dữ kiện so hai workflow.
ĐÃ THỬ VÁ: không — bổ sung tập sự kiện theo từng workflow, tách cấu hình khỏi sự kiện API. Kiểm bằng parse YAML và so tập; tránh phát biểu GitHub không có event chỉ vì workflow này không đăng ký.
ĐÃ THỬ NGHIỆM: extra.json parse BaseLoader:CI pull_request khôngtypes;duyệt target4types/review2types. Bảng có0 ready_for_review. Không mạng.
ĐỘ TIN: cao

### bo-sot-nhan-attestation-ci-moi  [P3]  Nhãn đã có trong body nhưng bản trích r359 vẫn bỏ nhãn của nó
TỆP/DÒNG: CHANGELOG.md:55,64–67,70–76; than-pr-493.md:17; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Bảng có nhãn đúng của body là cải thiện thật. Tuy nhiên các dòng số của input r359 vẫn mất nhãn(b),attestation,thiếu response ở ngay nguồn; liên kết tên land evidence còn lại không giữ trọn cấp chứng cứ.
ĐÃ THỬ VÁ: không — giữ khối nhãn và nhóm số làm một đơn vị trích, hoặc gắn metadata nguồn cho từng nhóm. Kiểm rằng bỏ nhãn một bản chiếu phải bị phát hiện; tránh coi nhãn xa của input khác tự động áp cho mọi số trùng.
ĐÃ THỬ NGHIỆM: bảng tái dựng giữbody17 nhưng omitted.txt có55,64–65,67; số CI r359 vẫn được giữ. Sự kiện API KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-ket-luan-bon-cong-tren-ban-sai  [P3]  Kết luận bốn cổng xanh trên bản sai vẫn bị tách mất phạm vi
TỆP/DÒNG: CHANGELOG.md:179–181; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Bảng bỏ lượng từ bốn-trong-năm và không-cổng-nào-bắt-cái-nào; chỉ giữ đuôi hai tên cổng. Bảng cổng head hiện tại ở body không thay thế kết luận về bản sai lịch sử.
ĐÃ THỬ VÁ: không — giữ nguyên kết luận với bốn cổng và SHA phạm vi. Kiểm đủ tên/quantifier/SHA; tránh lấy xanh head mới chứng minh xanh head cũ.
ĐÃ THỬ NGHIỆM: run-before.py tự chạy trên4af7e29:release,claims,lease,receipt đều rc0;lease121/121. Tái trích bỏ179–180,giữ181.
ĐỘ TIN: cao

### so-lan-thu-sau-moi-khong-co-phep-dem  [P3]  Số thứ tự thứ sáu mới không có đơn vị và chuỗi nhân chứng
TỆP/DÒNG: CHANGELOG.md:148–149; than-pr-493.md:73.
VẤN ĐỀ: Bản vá vừa thêm “lần thứ sáu kho gặp đúng hình dạng ấy” nhưng không liệt kê sáu sự kiện, phạm vi thời gian hay quy tắc phân biệt lượt/slug/bản chiếu. Verdict trước cho6VÁ HỜ là6slug trong MỘT lượt, không chứng minh đây là lần thứ6 trong lịch sử kho. Các con số ba/bốn lượt được gắn nhãn thuật lại ở nơi khác cũng không đủ để cộng thành6.
ĐÃ THỬ VÁ: không — dùng mô tả định tính “tái diễn”, hoặc ghi nhãn tự thuật và liệt kê sáu mốc có nguồn/đơn vị. Kiểm mỗi mốc và khử trùng; nguy cơ là cộng nhiều hậu quả cùng một lần thành nhiều lần.
ĐÃ THỬ NGHIỆM: sweep.json vét “thứ sáu” trên hiện vật/kho; các hit khác thuộc đối tượng khác. Parse verdict2 cho6slugVÁ HỜ,không phải chuỗi6sự kiện. Con số6 lịch sử KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về thiếu cơ sở, không khẳng định số6 chắc chắn sai

### bo-sot-nhan-ba-luot-vua-them  [P3]  Nhãn thuật lại mới cho ba lượt t33 lại bị bảng loại bỏ
TỆP/DÒNG: CHANGELOG.md:39–40,305–309; trich_khang_dinh.py:15–18.
VẤN ĐỀ: Cả hai nhãn mới “số ba là thuật lại/verdict gốc không có” không có chữ số nên không được trích. Bảng vẫn giữ heading t33 cùng số dòng assertion, làm mất giới hạn mà bản vá source vừa thêm. Đây là bỏ sót mới, khác nhóm CI.
ĐÃ THỬ VÁ: không — giữ nhãn cùng mệnh đề t33/ba lượt trong đơn vị trích. Kiểm đủ nhãn và lý do không đo; tránh biến lần mock hôm nay thành chứng minh ba lượt lịch sử.
ĐÃ THỬ NGHIỆM: omitted.txt có39–40,308–309;selected.txt có305–307. mutate.py chỉ chứng minh AssertionError/0subprocess hôm nay.
ĐỘ TIN: cao

### bo-sot-nhan-probe-vua-them  [P3]  Bảng bỏ chính nhãn phân biệt mã đọc được với sự kiện probe không có log
TỆP/DÒNG: CHANGELOG.md:383–391; muc-r358-da-va.md:191–199.
VẤN ĐỀ: Nhãn mới ở388–390 xác định loại(b),chỉ đọc lại mã,sự kiện động không log⇒KHÔNG ĐO ĐƯỢC đều không chữ số và bị bỏ. Các dòng có rc/version vẫn được giữ;391 giữ giới hạn nền vì có#493, nhưng không cứu nhãn về sự kiện động. Đây là mất cấp chứng cứ mới, tách khỏi finding cũ mất phạm vi R/cả hai sentinel.
ĐÃ THỬ VÁ: không — trích cả nhóm probe bằng lời với metadata nguồn và giới hạn log. Kiểm bảng phân biệt đọc mã/chạy thật; tránh tái tạo payload hoặc gắn rc của ca khác vào nhãn này.
ĐÃ THỬ NGHIỆM: script5input bỏ388–390,giữ385–386,391; bảngbyte-exact. Không chạy probe mới theo ràng buộc người dùng; sự kiện lịch sử KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

Kiểm cuối: `git -C cay-kho status --short` và `git -C review-current status --short` rỗng; exact head giữ nguyên. **KHÔNG CÒN P1; còn yêu cầu sửa P2/P3 như trên.**
