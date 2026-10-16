verdict: changes_requested
reviewed_sha: 025c6b2d2e89e71ea2bf5b2d0167fdd04566428e

**KHÔNG CÒN P1; KHÔNG CÒN P2 trong phạm vi review; CÒN 10 P3. Điều kiện “tới hết P3” CHƯA ĐẠT.** Đối chiếu chín slug lượt 7: **7 ĐÃ VÁ THẬT · 0 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Tám finding mới nằm ở kiểm kê lần quét, bản chiếu và nhãn nguồn; hai finding mang slug cũ là nợ cổng và phần dư mới của bản vá `printf`.

Reviewer: Codex theo cấu hình phiên; provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`. Khác executor Claude theo hồ sơ được giao; không chứng thực độc lập backend/model. Review theo §8 và chỉ thị trực tiếp lượt 8, không tự ghi state `cross_approved`, không cấp quyền merge.

Exact tree: `81514e78990f091bd8c98542de90719ed974cf5c`. `cay-kho/` detached, đầy đủ lịch sử, sạch trước và sau đo. Chỉ đọc cây này; chạy cổng trên `review-current/`, đột biến trên `review-mutant/`, đối chứng lịch sử trên `review-state/`. Không mạng; không tự soạn payload đường dẫn. Các bản sao và `TMPDIR=review-tmp/` đều trong workspace. Thư mục actionlint 1.7.7 được thêm cuối PATH; `core.abbrev=7` qua môi trường phép đo.

Bằng chứng tái lập nằm trong `review-evidence/`: `measure.py`, `run.py`, `probes.py`, `extra.py`, `targeted.py`; kết quả `measurements.json`, `gates.json`, `probes.json`, `extra.json`, `targeted.json`, `printf-boundary.json` và stdout `.out`. `units.json` giữ đơn vị đoạn/hàng bảng sau nối dòng, kèm tệp và dòng nguồn. Dòng `CHANGELOG.md` dưới đây là dòng trong `cay-kho/`, đồng thời khớp `muc-r360.md`; các tên hiện vật khác tính từ workspace.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`: **ĐÃ VÁ THẬT** — r360:152–157 có nhãn riêng cho khối nháp; thân PR:72–75 giữ nhãn riêng cho hai gạch đầu dòng; r360:390–407 gắn nhãn cho câu chuyện khôi phục. Đọc từng đoạn, không mượn nhãn ở heading khác. Nháp “tám”, transcript checkout và cặp 806980/806981 vẫn **KHÔNG ĐO ĐƯỢC**, đúng giới hạn nay được khai; không đòi lời tự thuật phải trở thành phép đo mới đóng lỗi nhãn.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — chạy ba mutant riêng trên exact tree: mỗi ca đổi một byte, giữ 847716 byte; cả ba claims `rc=0, ok=true`. Release ca 1016→1017 `rc=2`, chỉ CHANGELOG hỏng. Delta chỉ tám tệp hồ sơ; không sửa cổng. Khai nợ đúng không đóng nợ.
- `phan-vai-khai-duy-nhat-vuot-noi-dung`: **ĐÃ VÁ THẬT** — r360:28–42 nay nói **merge** #490, không nói nguồn r359 xác nhận landed. `git diff --shortstat c0a5cbe 8cee941` trả 39 tệp, +7834/−9; mục r359:90–100 xác nhận merged và phủ định landed, nêu thiếu hậu-merge gate. Ba điểm giao nhau hiện được kể đúng. Lần thay thứ ba **đứng trong phạm vi Git/nội dung nguồn đo được**, không thay bằng lời kể nhận thức mới. Lỗi khai công phát hiện ở phần kiểm kê mới được chấm riêng bên dưới.
- `va-cham-r-ke-sai-thoi-diem-cu`: **ĐÃ VÁ THẬT** — tự đọc hai blob `22b6339:CHANGELOG.md`, `cacaba3:CHANGELOG.md`: hai mục r355 khác nhau đều có trước merge. Đọc diff `bc78656^1..bc78656` thấy đổi số tại 3 chỗ CHANGELOG và 4 chỗ launcher_test, gồm r355b→r356b. r360:17–25 và message mới:30–34 chỉ kết luận thời điểm **ghi nhận sửa**, nói rõ không đo được lúc **nhận ra**. Đây là sửa thật lần thứ ba.
- `than-pr-khai-so-cong-cua-head-cu`: **ĐÃ VÁ THẬT** — thân PR:92–104 ghim full SHA a4bc01d, khai nhánh nháp và head GitHub 4af7e29. Tự chạy bien_nhan trên hai bản sao: lần lượt 49/102 và 43/96, đều rc0. Bảng lịch sử không bị giả làm số đo head 025c6b2. Trạng thái GitHub thật hiện tại **KHÔNG ĐO ĐƯỢC**, cấm mạng.
- `mo-ta-bo-trich-va-no-khong-theo-kip-ban-va`: **ĐÃ VÁ THẬT** — docstring thật:9–16 nay nói bỏ **dòng không có chữ số**, giữ phản ví dụ “ba lần … t33”. Regex cũ giữ dòng ấy; mô tả mới khớp r360:218–226. Chạy script với chín đầu vào tái tạo nguyên byte bảng 2234 dòng không rỗng; không chỉ tin lời message “đã sửa”.
- `printf-khai-do-duoc-khong-co-payload-goc`: **VÁ SINH LỖI MỚI** — phần sự kiện ở r360:365–371 đã phân loại đúng: không có hai payload, 2110 chỉ là hiệu hai số tự khai. Nhưng phần cơ chế mới:360–363 khái quát thành format **bắt đầu bằng `-` ⇒ rc2/stdout rỗng**. Tự chạy `printf '-'` được rc0, stdout `-`; ca `printf '- example\n'` mới rc2/stdout rỗng. Giữ slug để theo dõi phần dư do bản vá sinh ra, không tái mở lỗi thiếu nhãn sự kiện đã đóng.
- `ket-luan-thieu-tool-khong-co-inventory`: **ĐÃ VÁ THẬT** — r360:381–388 thu hẹp thành công cụ **phiên tìm thấy**, không còn suy ba tên thành tập endpoint đầy đủ; yêu cầu inventory có mốc thời gian để kết luận vắng mặt. Inventory lịch sử **KHÔNG ĐO ĐƯỢC**, không có trong gói. Không xem lời tự thuật đã có giới hạn là một phép inventory thất bại mới.
- `than-pr-tro-muc-va-cham-khong-ton-tai`: **ĐÃ VÁ THẬT** — thân PR:13 nay chỉ đúng **CHANGELOG.md, mục r360**, còn nói rõ khối không nằm trong thân PR. Đọc heading và khối r360:13–26 thấy đích tồn tại. Không còn chỉ dẫn “dưới” vào khoảng trống của chính bản chiếu.

## KIỂM PHÉP GỘP LỚP

**Không phải một phân hoạch gồm đúng bốn hình dạng loại trừ nhau.** A phân loại theo quan hệ mệnh đề–bằng chứng; B theo quan hệ nguồn–bản chiếu; C theo việc nguồn phủ định trạng thái được gán; D theo hành vi cổng. A và C không đồng nhất: thiếu transcript khác với có nguồn phủ định. B có thể đồng thời gây A/C khi bản chiếu làm mất giới hạn nguồn. D độc lập: có thể mô tả nợ hoàn toàn trung thực nhưng cổng vẫn không phát hiện sai số.

Đối với chín slug cũ, phép gộp dùng được như nhãn điều tra, nhưng **không thay được tiêu chí đóng riêng**. Trong B, số cổng sai mốc phải kiểm SHA; chỉ dẫn rỗng phải kiểm đích trong bản chiếu; docstring sai phải đối chiếu hành vi regex. Một thao tác “cập nhật bản chiếu” không tự chứng minh cả ba. Thực tế lần này cả ba đã được sửa đúng theo từng tiêu chí.

Phần mở rộng lớp có ba vấn đề:

- Nhãn “cho cả mục này” kéo số Git xuống tự thuật là lỗi **phạm vi nhãn**, không đúng nguyên văn định nghĩa A “khung đo được áp cho sự kiện không hiện vật”: đó là chiều sai ngược lại. Không nên dùng một nhãn A để xóa ranh giới giữa nâng và hạ hạng nguồn. Bản vá cụ thể ở khối nháp/checkout lần này vẫn hợp lý.
- Bảng chỉ tóm tắt lượt 1–3 **không tự là lỗi**. Lượt 7 đã đọc nó như tóm tắt chọn lọc; nguồn không bị gán sai chỉ vì không chép toàn bộ. Bổ sung lượt 4–7 hữu ích, nhưng không đủ căn cứ tự ghi thêm một “lỗi đã vá”. Tương tự, không chấm riêng thân PR:77–86 chỉ chọn hai lượt đầu để minh họa năm bản vá sót; các ô ấy đúng, các đoạn khác đã nhắc lượt sau. Câu mở đầu r360 đếm toàn phạm vi thành sáu lại khác: đó là số hiện hành chưa theo bảng bảy lượt, finding bên dưới.
- R359 phủ định **landed #490**, không phủ định **landed #494**. Thay “PR #494 land” bằng “merge” là cách thu hẹp an toàn, nhưng chưa chứng minh nó là một thể hiện C. Và câu “một phiên khác land #490 rồi #494” **đã được lượt 7 chỉ tại dòng 14**, không phải phát hiện thêm chưa ai chấm.

**Cách quét của lượt này:** tách đoạn/hàng bảng/YAML theo cấu trúc, nối whitespace rồi đọc mệnh đề với chủ thể, mốc và nguồn của nó. Đi từ nguồn ra bản chiếu: bảy verdict → bảng/tóm tắt; receipt → ô runtime; hai blob cha → chuyện va chạm; r359 → trạng thái #490; các hàng kiểm kê → tổng và danh sách “thừa”. Tách phát biểu hiện hành khỏi trích dẫn sai để bác và message lịch sử. Bộ trích được kiểm bảo toàn toàn bộ dòng ở đúng section; không coi một hit từ khóa là đủ.

Quét A không còn sự kiện nháp/comment/inventory cũ đứng trong khung “đo được”. Quét B còn một số lượt cũ và bốn ô runtime bị thu hẹp nhãn nguồn khi chiếu ra README; riêng hai ô#489 là bản cũ được thêm lặp ngay sau hàng đã sửa đúng trên master. Quét C đóng trạng thái #490 cũ nhưng tìm thấy chính phần mới khai sai trạng thái “chưa được reviewer chỉ”. Quét D tái hiện cả ba mutant sống. Ngoài bốn nhãn ấy có E (khái quát điều kiện chạy) và F (kiểm kê không bảo toàn tổng). Mỗi sự kiện runtime riêng có finding riêng; việc lặp lại cùng sự kiện ở r360 được chỉ cùng finding, không cộng lần nữa theo số bản sao.

**Đọc từng hunk lượt 7→8:** đổi land→merge và giới hạn Git là đúng; nhãn khối nháp là đúng; bỏ “duy nhất” thu hẹp đúng phạm vi; bảng bảy lượt đúng số; nhãn sự kiện printf và giới hạn inventory đúng. Phần kiểm kê mới sai tổng/nguồn/vị trí, còn câu cơ chế printf mới rộng hơn ca đã đo. Không thấy nhãn mới kéo phần va chạm Git hay bảng verdict xuống hạng tự thuật: nhãn cuối nay nêu đối tượng riêng, phần nháp có nhãn tại chỗ.

**Bảng lượt 1–7 và điều kiện dừng:** cả bảy SHA, verdict và bộ ba số finding đều khớp. Verdict lượt 3:4 ghi hết P1; lượt 4:4 chuyển sang hết P2 nhưng còn một P2; lượt 5:4 đạt hết P2 và approve; lượt 6:4 và 7:4 yêu cầu hết P3, vẫn còn P3. Vì thế lời giải thích tại r360:250–252 **được các verdict chứng minh**, không phải lỗi lịch sử. Chỉ thị gốc của chủ kho vẫn là nội dung các verdict thuật lại; tôi không có transcript riêng để xác thực cuộc trao đổi ấy.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/tree | 025c6b2 | Full SHA đúng; tree 81514e78990f091bd8c98542de90719ed974cf5c; detached, shallow=false, status rỗng | Có |
| Delta so c31d8f1 | tám tệp hồ sơ | Lệnh awk yêu cầu: **8 tep, +1528/-26**; bằng git diff --numstat | Có |
| Hai patch, numstat, message | trích từ Git | 4/4 nguyên byte với lệnh Git tương ứng | Có |
| Write set | không mã cổng | CHANGELOG, manifest, land, README, hai verdict, hai receipt | Có |
| Heading | r360/r359/r358 | Dòng 1/409/529; tiếp theo r356:762, r355:857 | Có |
| Ba slice | cắt theo heading thật | 3/3 nguyên byte | Có |
| Land, README, receipt1/2 | bản chiếu trong cây | 4/4 nguyên byte | Có |
| ARTIFACTS.sha256 | toàn vẹn | 3266/3266 khớp | Có; không chứng thực API |
| Ref snapshot | 319/319/319, lệch0 | Ba tập tên+OID bằng nhau và bằng refs/heads Git sau chuẩn hóa tiền tố | Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Base đã tích hợp | c31d8f1 là tổ tiên | merge-base --is-ancestor: rc0 | Có |
| First-parent c31d8f1..HEAD | chuỗi PR | 12 commit, thứ tự cũ→mới: 34e9d35, cdd0b1d, 4af7e29, 9484970, fae2fb7, b004da9, f5098dd, 7e236cf, 2c57e99, cdd5891, a4bc01d, 025c6b2 | Có |
| Hiện vật PR491/PR493 trong ops/reviews | hai lượt PR491; không verdict PR493 | Hai verdict + hai receipt PR491; không pr493-review-* | Có |
| Land theo mốc | trước thêm #491: sáu ở00e017a, bảy ởmaster mới | ls-tree -r: 6 tại00e017a, 7 tạic31d8f1, 8 tạiHEAD | Có |
| Phạm vi r359 | 39 tệp,c0a5cbe..8cee941 | 39,+7834/−9 | Có |
| Phạm vi r358 | 1016 tệp,+247458 | git diff b416830..c0a5cbe đúng cả hai | Có |
| Va chạm cũ | hai cha có r355; đổi3+4 | Hai blob và diff xác nhận | Có; thời điểm nhận ra KHÔNG ĐO ĐƯỢC |
| Trạng thái nguồn #490 | merged, chưa đủ landed | r359:90–100 đúng như trích | Có |
| PR491 verdict1 | 3/5/6;35088 byte | Regex heading 3/5/6,35088,sha256 38d7fb2e… | Có |
| PR491 verdict2 | 0/3/10;36958 byte | Regex heading 0/3/10,36958,sha256 14c726e5… | Có |
| Commit đầu chứa hai verdict | 34e9d35 | log --diff-filter=A trả 34e9d35be0fc52406e3659bfc24c388bf54262cd cho cả hai | Có |
| PR493 lượt1 | 4af7e29; changes_requested;1/4/12 | Cùng SHA đầy đủ và số heading1/4/12 | Có |
| PR493 lượt2 | 9484970; changes_requested;1/4/15 | Cùng SHA đầy đủ và số heading1/4/15 | Có |
| PR493 lượt3 | fae2fb7; changes_requested;0/2/15 | Cùng SHA đầy đủ và số heading0/2/15 | Có |
| PR493 lượt4 | b004da9; changes_requested;0/1/15 | Cùng SHA đầy đủ và số heading0/1/15 | Có |
| PR493 lượt5 | f5098dd; approve;0/0/14 | Cùng SHA đầy đủ và số heading0/0/14 | Có |
| PR493 lượt6 | 2c57e99; changes_requested;0/0/10 | Cùng SHA đầy đủ và số heading0/0/10 | Có |
| PR493 lượt7 | a4bc01d; changes_requested;0/0/9 | Cùng SHA đầy đủ và số heading0/0/9 | Có |
| Lý do approve rồi changes_requested | đổi ngưỡng P1→P2→P3 | Phần mở đầu verdict3/4/5/6/7 xác nhận đúng lịch ngưỡng | Có trong nguồn verdict |
| Bộ trích | 2234 dòng không rỗng,1411 có số | 343+97+200+78+210+156+214+523+413=2234; output nguyên byte | Có cho chín input; không phải số mệnh đề |
| Kiểm kê lớp | 8→12;4 thừa | Các hàng số là8→13; danh sách thừa có2+1+2=5 | Không |
| Phát hiện thêm #490 | chưa ai chấm câu VA CHẠM | Verdict7:101 đã chỉ CHANGELOG:14 | Không |
| Message mới, vị trí C | r360 ba chỗ land | Bản cũ r360 hai chỗ; chỗ thứ ba được r360 mới nêu nằm thân PR và nói#494 | Không |
| Manifest head | 180 tệp,8142038 byte | Tổng và hash387f04e3… khớp; CHANGELOG847716 byte | Có |
| release strict | ok,180/180 | rc0,ok=true,hai hash_match=true;failed/extra_files/errors rỗng | Có |
| doc-claims strict | ok | rc0,ok=true | Có trong phạm vi cổng |
| lease suite |121/121,bỏ0 | rc0;121/121 đạt;đã chạy121,bỏ0 | Có |
| bien_nhan head |49/102,0vi phạm | rc0;49v2+11legacy+42nợ=102;0vi phạm,0KHÔNG ĐO ĐƯỢC | Có |
| bien_nhan a4bc01d /4af7e29/master |49/102;43/96;47/100 | Chạy trên ba bản checkout: đúng,rc0 cả ba | Có |
| doctrine-scan | sạch | rc0;7tệp,0chép doctrine | Có |
| adr-song | sạch | rc0;46ADR/46hàng,khớp1–1 | Có |
| Ba đột biến số | vẫn xanh | 1016→1017 dòng529;5→6 dòng1;11→12 dòng287;đúng1byte/ca;claims rc0/ok=true cả3 | Có; D chưa đóng |
| Byte mutant bị release chặn | chỉ CHANGELOG hỏng | rc2,ok=false,failed chỉCHANGELOG,hash_match=false,kích thước không đổi | Có |
| Cơ chế printf với `- example` | rc2,stdout rỗng | Tái hiện đúng;format%s rc0,nội dung đủ | Có |
| Khái quát mọi format bắt đầu dấu trừ | rc2,stdout rỗng | `printf '-'`:rc0,stdout `-` | Không |
| Payload comment lịch sử |29793→27683,hụt2110 | Số học đúng;không hai payload/response | KHÔNG ĐO ĐƯỢC sự kiện; nay nhãn đúng |
| Inventory endpoint lịch sử | chỉ thứ phiên tìm thấy | Không inventory/discovery response | KHÔNG ĐO ĐƯỢC; nay giới hạn đúng |
| README hai hàng#489 | không khai việc thêm bản cũ lặp | Verdict4892 ở284/288,verdict4891 ở285/289; hai hàng trước có nhãn toàn runtime, hai hàng sau chỉ model/effort | Không nhất quán |
| Runtime4911/4912/4891/4892 |696/714/1560/983s và trạng thái chạy | Receipt khai nguồn run.json ngoài kho;không log gốc | KHÔNG ĐO ĐƯỢC; nhãn bị mất ở bốn hàng README |
| GitHub body, approval, CI lịch sử | snapshot và lời đọc API | Không mạng/raw response | KHÔNG ĐO ĐƯỢC độc lập; băm không chứng thực provenance |

Không coi các message cũ đã được đoạn hiện hành bác rõ là finding còn sống chỉ vì chúng bất biến trong Git. Không dùng việc xóa một tag trên bản sao rồi vẫn đọc được blob để kết luận khả năng fetch từ máy chủ tương lai: phép thử ấy chỉ đo object store cục bộ. Không chứng nhận toàn bộ CI thật từ sáu cổng chạy tại chỗ.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Ba phép sai số vẫn qua cổng claims
LỚP: D
TỆP/DÒNG: CHANGELOG.md:185–197,346–351; scripts/tl_core/workflow.py:1163,1430,1488.
VẤN ĐỀ: Cả ba tiêu chí phản chứng vẫn chưa đạt. Đây là nợ cũ được yêu cầu theo dõi tới hết P3, không phải hồi quy mới. Mã thực thi claims nằm trong workflow.py và được tl.py đưa ra qua handler; không nên hiểu “đòi sửa tl.py” là chỉ có duy nhất một tệp có thể chữa.
CÙNG LỚP CÒN Ở ĐÂU: Cùng ba phản chứng được kể tại receipt-luot1:74–76, thân PR:68 và message mới:23–25; không có bằng chứng đóng hành vi ở bản chiếu nào.
ĐÃ THỬ VÁ: không sửa sản phẩm — đã tạo từng mutant trên bản sao rồi khôi phục. Cách vá: packet kế nhiệm có write set phù hợp kiểm số dựa vào Git/verdict và nguồn có mốc; giữ control xanh, buộc cả ba mutant đỏ. Nguy cơ: hard-code ba con số, hoặc kiểm nhầm câu lịch sử/trích dẫn. Không mở rộng PR hồ sơ để vá cổng thay executor.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/probes.py`: cả3 claims rc0/ok=true; release cađầu rc2,failed chỉCHANGELOG. Sáu control trong `run.py` đều đạt.
ĐỘ TIN: cao

### printf-khai-do-duoc-khong-co-payload-goc  [P3]  Bản vá khái quát điều kiện lỗi printf quá rộng
LỚP: E — lấy kết quả của một đầu vào cụ thể làm kết luận cho toàn bộ lớp đầu vào.
TỆP/DÒNG: CHANGELOG.md:360–363.
VẤN ĐỀ: Câu mới nói format bắt đầu bằng dấu trừ dẫn tới invalid option, rc2,stdout rỗng. Đầu vào chỉ gồm dấu trừ bác mệnh đề ấy. Lượt7 đo một format dấu trừ kèm nội dung cụ thể, không đo mọi format có tiền tố ấy. Phần sự kiện không payload đã được chữa thật.
CÙNG LỚP CÒN Ở ĐÂU: Đã vét các đoạn printf trong r360/message; các câu dạng cụ thể `- …` không bị coi là toàn xưng. Không tìm thêm một mệnh đề hiện hành khác cùng lỗi điều kiện này.
ĐÃ THỬ VÁ: không — ngay phần cơ chế nêu chính xác ca `- example` đã chạy, dùng “có thể bị parse như tùy chọn”; giữ cách dựng `%s` hiện có. Khóa bằng ca lỗi, ca dấu trừ đơn và ca `%s`; nguy cơ sửa là hạ cả cơ chế đo được thành tự thuật, hoặc bỏ khuyến nghị dựng chuỗi đúng.
ĐÃ THỬ NGHIỆM: Bash --noprofile --norc: `printf '-'` rc0/stdout `-`; `printf '- example\n'` rc2/stdout rỗng; `printf '%s\n' '- example'` rc0/nội dung đủ. Kết quả trong `printf-boundary.json`.
ĐỘ TIN: cao

### kiem-ke-lop-tong-muoi-hai-khong-khop-hang  [P3]  Tổng 12 không bằng các số hạng của chính bảng
LỚP: F — kiểm kê trộn đơn vị hoặc không bảo toàn tổng giữa danh sách, bảng và kết luận.
TỆP/DÒNG: CHANGELOG.md:308,315–328,333,338–339; thong-diep-commit.txt:2,12–22,38–39.
VẤN ĐỀ: A6+B4+C3=13, không phải12; phần “bốn thể hiện thừa” liệt kê2A+1B+2C=5. Cột reviewer là số slug, còn cột sau đếm vị trí/thể hiện, chưa có bảng định danh để khử trùng. Vì vậy cũng chưa thể chỉ đổi12→13 rồi gọi đó là số lỗi thật đã vá: bảng chọn lọc và phân loại#494 còn cần xét lại.
CÙNG LỚP CÒN Ở ĐÂU: Cùng tổng12 được chiếu vào subject và phần giới hạn message mới; đã tìm đủ các bản chiếu của tổng này trong phạm vi giao.
ĐÃ THỬ VÁ: không — lập inventory từng mệnh đề/vị trí, có ID và nguồn trước/sau; đếm cùng một đơn vị rồi sinh bảng/tổng từ đó. Khóa bằng phép tổng và tính duy nhất của ID. Nguy cơ: đổi số cho khớp số học nhưng giữ phần tử không phải lỗi hoặc đếm lại một vị trí đã được chỉ.
ĐÃ THỬ NGHIỆM: `python3 -B review-evidence/targeted.py` parse ba hàng thật, trả before_sum8,after_sum13; đọc danh sách ngay dưới xác nhận năm mục mô tả.
ĐỘ TIN: cao

### phat-hien-them-da-co-trong-verdict-bay  [P3]  Câu land ở khối va chạm đã được reviewer chỉ đích danh
LỚP: C
TỆP/DÒNG: CHANGELOG.md:322,327–333; VERDICT-LUOT-7.md:100–103.
VẤN ĐỀ: Phần mới nhận câu “một phiên khác land #490 rồi #494” là phần thừa “không ai chấm”, “chỉ khác đoạn văn”. Nhưng TỆP/DÒNG của finding phân vai lượt7 đã ghi **CHANGELOG.md:14,28–31**; dòng14 chính là câu này. Mốc baseline “được chỉ” đã nuốt một vị trí reviewer nêu, làm sai kết luận hiệu quả quét thêm. Lỗi này độc lập với tổng13/12: sửa phép cộng vẫn không biến vị trí đã nêu thành mới.
CÙNG LỚP CÒN Ở ĐÂU: Message mới:20–22 mang cùng phân hoạch1→3; trạng thái#490 trong phần phân vai hiện hành đã sửa đúng. Nhãn cuối mục cũng được verdict7 nêu địa chỉ, nhưng tôi không dùng riêng việc trùng địa chỉ để suy mọi nhận xét mới về nhãn đều đã được chấm.
ĐÃ THỬ VÁ: không — đánh dấu câu dòng14 là vị trí cũ của slug phân vai; tách “số slug” khỏi “số vị trí reviewer chỉ”. Khóa bằng bảng nối từng vị trí về trích đoạn verdict7. Nguy cơ: đếm lại cả trích dẫn lịch sử của câu sai thành một phát hiện mới.
ĐÃ THỬ NGHIỆM: Đọc nguyên văn `VERDICT-LUOT-7.md:101` và `git show a4bc01d:CHANGELOG.md`, dòng14; hai bên trỏ đúng cùng câu. `extra.json` giữ trích địa chỉ gốc.
ĐỘ TIN: cao

### message-moi-chieu-ba-cho-vao-sai-tep  [P3]  Message mới đặt cả ba vị trí land vào r360
LỚP: B
TỆP/DÒNG: thong-diep-commit.txt:20–22; CHANGELOG.md:327–328.
VẤN ĐỀ: Message mới viết “r360 ba chỗ viết land”. Danh sách hiện hành của chính tác giả lại có hai chỗ trong r360 và một trong thân PR. Chỗ thân PR nói#494; nguồn r359 phủ định landed#490 không tự phủ định landed#494. Đây là bản chiếu mới sai vị trí và phạm vi đối tượng, dù hai câu phân vai/va chạm đã sửa đúng.
CÙNG LỚP CÒN Ở ĐÂU: Phân loại vị trí thân PR thành C còn ở bảng/giải thích r360:319,327–328. Câu chỉ dẫn thân PR:13 nay trỏ đúng CHANGELOG, không còn lỗi đích rỗng.
ĐÃ THỬ VÁ: không — đính chính message bằng văn bản mới có neo025c6b2; inventory ghi riêng tệp, mệnh đề và PR được nói tới. Khóa bằng đối chiếu từng hàng inventory với blob/bản chiếu gốc. Nguy cơ: viết lại lịch sử hoặc coi thiếu bằng chứng landed#494 là nguồn phủ định landed#494.
ĐÃ THỬ NGHIỆM: `git log --format='%H%n%B%n---' c31d8f1..HEAD` khớp message nguyên byte; diff lượt7→8 đổi hai câu land trong CHANGELOG; danh sách mới tự đặt vị trí còn lại ở thân PR.
ĐỘ TIN: cao

### mo-dau-r360-van-dem-sau-luot  [P3]  Số lượt ở khai phạm vi chưa theo bảng bảy lượt
LỚP: B
TỆP/DÒNG: CHANGELOG.md:7–11,230–248.
VẤN ĐỀ: Khai phạm vi mở đầu vẫn là “Sáu lượt cross-review của chính PR#493 … được tóm tắt trong mục này”; cùng mục nay có bảng **BẢY** lượt, thêm chính verdict7. Câu sáu không ghim mốc lịch sử hay nói “sáu lượt đầu”, nên phần mô tả phạm vi hiện tại vẫn giữ số của head trước. Đây là phần sót của cập nhật số lượt, không phải yêu cầu mọi ví dụ lịch sử phải chứa đủ bảy lượt.
CÙNG LỚP CÒN Ở ĐÂU: Message cdd5891:111 nói sáu ở mốc cũ là đúng lịch sử, không chấm lại. Bảng hai lượt ở thân PR là tóm tắt câu chuyện năm bản vá đầu, không đếm thành finding thứ hai.
ĐÃ THỬ VÁ: không — đổi khai phạm vi thành bảy hoặc bỏ số và dẫn bảng có mốc. Khóa bằng đối chiếu câu mở với tập lượt trong bảng, không grep mỗi chữ “sáu”. Nguy cơ: thay cả số sáu trong message lịch sử/đoạn nói sáu lượt trước.
ĐÃ THỬ NGHIỆM: `measure.py` đếm bảy verdict và xác nhận bảy hàng SHA/sốfinding; đọc dòng9 vẫn sáu, diff lượt này không sửa câu ấy.
ĐỘ TIN: cao

### runtime-pr491-luot1-mat-nhan-khi-chieu  [P3]  Thời lượng và rc lượt 1 bị để ngoài nhãn attestation
LỚP: B
TỆP/DÒNG: reviews-README.md:287; muc-r360.md:55; receipt-luot1.yaml:6,88–106.
VẤN ĐỀ: Receipt phân loại **mọi scalar runtime** từ run.json ngoài kho là attestation. Hàng mục lục chỉ giữ “Model/effort là ATTESTATION”, còn696s vàrc0 đứng ngoài phạm vi nhãn; hàng đường review r360 cũng chép chúng không kèm giới hạn ấy. Số finding/băm đo được trong cùng hàng càng cần phân biệt rõ với số runtime không có hiện vật.
CÙNG LỚP CÒN Ở ĐÂU: Cùng sự kiện ở r360:55; ba sự kiện runtime riêng khác ở ba finding tiếp theo. Đây là cùng kiểu bỏ mất giới hạn khi tóm tắt mà các hàng#490/#487 trong README đã tránh bằng nhãn **toàn bộ khối runtime**.
ĐÃ THỬ VÁ: không — sửa nhãn ngay hai bản chiếu thành thời lượng/rc/model là attestation từ run.json không kèm; giữ Git/hash/sốheading là đo được. Khóa bằng ánh xạ trường runtime từ receipt sang từng ô bản chiếu. Nguy cơ: nhãn “cả hàng” kéo số Git và sốfinding xuống tự thuật.
ĐÃ THỬ NGHIỆM: `targeted.py` đối chiếu hàng287 với `nguon_cac_scalar_tren` receipt:106; gói không có run.json của dc136619. 695.9 làm tròn696 chỉ đúng số học, **KHÔNG ĐO ĐƯỢC** thời lượng/rc lịch sử độc lập.
ĐỘ TIN: cao

### runtime-pr491-luot2-mat-nhan-khi-chieu  [P3]  Lượt 2 giữ nhãn model nhưng mất nhãn trạng thái chạy
LỚP: B
TỆP/DÒNG: reviews-README.md:286; muc-r360.md:56; receipt-luot2.yaml:134–152.
VẤN ĐỀ: 714s,rc0,“chạy trọn ngay lần đầu” là dữ liệu runtime theo receipt, không phải điều rút ra từ verdict/hash. README chỉ gắn nhãn model/effort; r360 cũng không chuyển giới hạn nguồn của thời lượng/rc sang hàng tóm tắt. Đọc băm verdict hoặc đếm13heading không kiểm được lần chạy ấy.
CÙNG LỚP CÒN Ở ĐÂU: Cùng sự kiện ở r360:56; ba sự kiện khác được tách finding riêng. Nhãn attestation của CI ở r360:110 trở đi không phủ ngược bảng đường review.
ĐÃ THỬ VÁ: không — đưa nhãn đầy đủ theo đúng trường runtime từ receipt ra hàng286 và hàngr360; hoặc giao log có băm/neo đúng run. Khóa bằng đối chiếu714.268/rc/so_lan_chet với nhãn bản chiếu. Nguy cơ: coi sự có mặt của verdict là chứng minh chạy trọn ngay lần đầu.
ĐÃ THỬ NGHIỆM: `targeted.py` giữ nguồn receipt có `nguon_cac_scalar_tren` và hàng286; không có run.json của46d8686e. 714.268 làm tròn714 đúng; runtime lịch sử **KHÔNG ĐO ĐƯỢC** độc lập.
ĐỘ TIN: cao

### runtime-pr489-luot1-mat-nhan-khi-chieu  [P3]  Hàng PR489 lượt 1 cũng bỏ giới hạn nguồn thời lượng
LỚP: B
TỆP/DÒNG: reviews-README.md:285,289; cay-kho/ops/reviews/pr489-review-1-codex-verdict.receipt.yaml:90,135.
VẤN ĐỀ: Hàng được thêm trong delta PR ghi1560s,“chạy trọn ngay lần đầu”, nhưng chỉ đánh dấu model/effort là attestation. Receipt nguồn nói rõ scalar runtime là attestation từ run.json ngoài kho. **Ngay dòng285 đã có một hàng cùng verdict, cùng SHA, nhãn toàn runtime ĐÚNG; dòng289 là bản cũ bị thêm lặp lại.** Đây là bản chiếu lỗi còn sống ngay cạnh bản đã sửa, không chỉ là thiếu chú thích ở một ô riêng.
CÙNG LỚP CÒN Ở ĐÂU: Ba hàng4911/4912/4892 đã tách finding; nguồn receipt của4891 tự khai giới hạn đúng.
ĐÃ THỬ VÁ: không — bỏ hàng cũ lặp289, giữ hàng285 đã đủ nhãn; nếu cần hợp nhất nội dung thì kiểm từng trường và giữ nhãn theo nguồn. Khóa bằng tính duy nhất verdict_path+reviewed_sha trong mục lục và source-map trường runtime; nguy cơ sửa là làm mất phân biệt metadata runtime và bằng chứng Git.
ĐÃ THỬ NGHIỆM: `git diff --unified=0 c31d8f1 HEAD -- ops/reviews/README.md` xác nhận hàng thuộc delta; `targeted.py` nối nó tới receipt:90/135. Không log gốc: **KHÔNG ĐO ĐƯỢC** thời lượng/trạng thái chạy.
ĐỘ TIN: cao

### runtime-pr489-luot2-mat-nhan-khi-chieu  [P3]  Hàng PR489 lượt 2 lặp lại nhãn runtime bị thu hẹp
LỚP: B
TỆP/DÒNG: reviews-README.md:284,288; cay-kho/ops/reviews/pr489-review-2-codex-verdict.receipt.yaml:144,212.
VẤN ĐỀ: Hàng ghi983s và“chạy trọn ngay lần đầu” ngoài nhãn chỉ dành cho model/effort. Nguồn nói mọi scalar runtime là attestation, run.json không vào kho. **Dòng284 đã có cùng verdict/SHA với nhãn toàn runtime đúng; dòng288 thêm lặp bản cũ thiếu nhãn.** Bốn hàng có cùng hình dạng nhưng đây là sự kiện khác, cần được sửa riêng trong lần quét lớp.
CÙNG LỚP CÒN Ở ĐÂU: Ba sự kiện khác ở ba finding trên; các hàng#490/#487 đã có nhãn toàn runtime là đối chứng đúng, không chấm lại chúng.
ĐÃ THỬ VÁ: không — bỏ hàng cũ lặp288, giữ hàng284 đã đủ nhãn; kiểm không mất nội dung riêng nếu hợp nhất. Khóa bằng tính duy nhất verdict_path+reviewed_sha và đối chiếu từng trường đã chiếu với phạm vi nhãn. Nguy cơ: sửa riêng983s rồi để sót cụm“chạy trọn ngay lần đầu”.
ĐÃ THỬ NGHIỆM: Delta Git xác nhận hàng được thêm; `targeted.py` giữ hàng và hai nhãn nguồn receipt. Không run.json tương ứng, nên **KHÔNG ĐO ĐƯỢC** runtime lịch sử độc lập.
ĐỘ TIN: cao

**Kết luận trên exact SHA: 0 P1 · 0 P2 · 10 P3, `changes_requested`.** Các sửa nội dung chính của lượt7 phần lớn đã đóng thật; phép kiểm kê“8→12” chưa đứng vững và nợ cổng vẫn sống. Không ghi vào kho thật, không đăng review và không thay ref của `cay-kho/`.
