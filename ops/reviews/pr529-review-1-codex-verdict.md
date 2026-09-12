verdict: changes_requested
reviewed_sha: 2c466acaa8e6d3324311784ae14cda7a402b51b8
so_p1: 1  so_p2: 4  so_p3: 0
so_the_hien: 8

## BẢNG SĂN

Các phép đọc dưới đây là probe do reviewer viết từ SPEC, không phải cổng nghiệm thu có sẵn. Đột biến chỉ là văn bản quy trình lành tính; mỗi lần đều phục hồi byte gốc.

HƯỚNG 1: A10 — hai nguyên nhân và nghĩa vụ đo drift
  giả thuyết : Nếu hai nhánh hành động hoặc tính bắt buộc mất mà phép đọc vẫn xanh thì A10 không phân biệt được.
  lệnh       : `python3 probes/review_checks.py 1`
  output     :
```text
gốc A10=True
đột biến giữ câu cũ A10=False
đột biến nghĩa vụ thành nên A10=False
```
  kết luận   : KHÔNG PHẢI LỖI — hai phép ĐỎ đều làm tiêu chí đọc ĐỎ; chưa chứng minh runtime cưỡng chế.

HƯỚNG 2: A11 — bỏ từng mệnh đề hậu merge
  giả thuyết : Nếu bỏ nghĩa vụ CI hoặc ngoại lệ phát hiện lỗi không làm thiếu mệnh đề độc lập thì A11 tự phán sai.
  lệnh       : `python3 probes/review_checks.py 2`
  output     :
```text
gốc: các mệnh đề=['1', '2', '3']
bỏ (ii): còn=['1', '3']
bỏ (iii): còn=['1', '2']
Đọc nghĩa: (i) miễn review do head đổi; (ii) vẫn đo CI; (iii) mở review do phát hiện lỗi. Hai câu giải thích còn lại nhắc lại (ii)/(iii), nên chỉ xoá hàng đánh số chưa xoá hết nghĩa vụ.
```
  kết luận   : KHÔNG PHẢI LỖI — ba nghĩa vụ độc lập có mặt; phép xoá hàng làm ĐỎ cấu trúc, còn phép bỏ nghĩa vụ phải bỏ cả câu giải thích trùng.

HƯỚNG 3: A12 — ngân sách gọi tay và chuỗi CI tuân thủ khác
  giả thuyết : Nếu N mở vẫn đạt, hoặc CI tự động full bị coi là gọi tay cấm, luật phân loại sai.
  lệnh       : `python3 probes/review_checks.py 3`
  output     :
```text
gốc hàng (b): N=0 bắt buộc=True
đột biến N mở: N=0 bắt buộc=False
Chuỗi giả định khác #512: push -> gate tự động có full job -> review -> push sửa -> gate tự động -> approve -> merge -> dispatch CI hậu merge.
Đọc bảng: hai lượt trước merge thuộc (a), 0 lượt (b); hậu merge thuộc (a): ĐẠT.
Đối chiếu #512 chỉ từ lời khai: 0 dispatch + chỉ tự động => ĐẠT. Lịch sử Actions trực tiếp: KHÔNG ĐO ĐƯỢC offline.
```
  kết luận   : KHÔNG PHẢI LỖI — đọc cả bảng với (a) là ngoại lệ rõ cho CI tự động; không tách chữ full CI khỏi ngữ cảnh gọi tay để tạo finding.

HƯỚNG 4: A13 — độ nhạy thực của doctrine-scan
  giả thuyết : Nếu chép trần hoặc §5.1 mà rc vẫn 0 thì phép ĐỎ bắt buộc A13 không hoạt động.
  lệnh       : `python3 probes/review_checks.py 4`
  output     :
```text
gốc: rc=0: doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine
đột biến thêm con số trần: rc=0: doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine
đột biến chép nguyên văn điều kiện §5.1: rc=0: doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine
đối chứng dương cụm §12 đã nằm trong danh sách: rc=6: .claude/skills/work-packet/SKILL.md:220: [nguong-so-stop-conditions] chép doctrine: '3 attempt/packet'
1 chỗ chép doctrine trong adapter. Adapter chỉ được TRỎ về docs/PROTOCOL_DA_PHIEN.md, không nhắc lại nội dung ở đó.
```
  kết luận   : LỖI — cả hai đột biến bị SPEC cấm vẫn rc=0; đối chứng dương rc=6 xác nhận đã chạy đúng scanner.

HƯỚNG 5: M1/A1 — điều kiện dừng khác nhau theo review_class
  giả thuyết : Nếu routine và systemic cùng bị bắt mở vòng khi còn P2 thì luật đã gộp hai điều kiện khác nhau.
  lệnh       : `python3 probes/review_checks.py 5`
  output     :
```text
Bảng review_class -> điều kiện dừng trong cross-review: 0 hàng
từ routine/systemic trong work-packet: False
SPEC r1 M1/A1 giữ nguyên: routine 0 P1 + P2 thành nợ; systemic 0 P1/P2; sensitive approve.
Ca routine: 0 P1, 1 P2 đã ghi nợ, changes_requested. SPEC: đủ điều kiện dừng; bảng work-packet: lớp P2 còn mở => vá rồi mở vòng mới.
Ca sensitive 0 P1/P2 thiếu approve: câu sensitive tường minh vẫn chặn; không coi câu hoặc ở dòng 127 là đủ chứng minh bypass.
```
  kết luận   : LỖI — thiếu bảng ba lớp; luật hành động hiện tại áp P2 cho cả routine.

HƯỚNG 6: M3/A2 — từ đếm lớp đến hợp đồng bàn giao bản vá
  giả thuyết : Nếu bảng chỉ định nghĩa đơn vị đếm mà không buộc ghi kế hoạch đóng lớp thì vòng vá không có dữ liệu M3 đòi.
  lệnh       : `python3 probes/review_checks.py 6`
  output     :
```text
cột lop_loi trong phần BẢNG LỚP/khung verdict: False
cột bản vá theo lớp hoặc lý do vá lẻ: False
mục BẢNG LỚP trong khung verdict: False
Ca độc lập: cùng cơ chế xuất hiện 5 vị trí => 1 slug lớp, so_p2=1, so_the_hien=5: đơn vị đếm áp dụng được.
Nhưng có thể điền hết khung verdict chỉ với TỆP/DÒNG, VẤN ĐỀ, ĐÃ THỬ VÁ: không có ánh xạ thể hiện hoặc kế hoạch đóng lớp; vẫn đủ khung skill, thiếu A2.
```
  kết luận   : LỖI — định nghĩa lớp dùng được; nghĩa vụ bảng remediation cho từng lớp và khung sinh ra thiếu.

HƯỚNG 7: M5/A4 — tráo phân hạng bản vá thành mức nghiêm trọng
  giả thuyết : Nếu đọc PHÂN HẠNG là P1/P2 thay vì VÁ THẬT/VÁ HỜ thì đánh giá hội tụ và chốt dừng sai.
  lệnh       : `python3 probes/review_checks.py 7`
  output     :
```text
công thức VÁ THẬT trong work-packet: False
ngưỡng 50% trong hai skill: False
#508: 4/13=0.307692; 3/12=0.250000; cả hai <0.5=True
SPEC M5: vòng 3 DỪNG/HỎI. Skill: nói chưa hội tụ theo hạng; không có công thức, cửa sổ hai vòng hay hành động tại ngưỡng này.
Đối chứng phân biệt: vòng đầu 10 lớp P2; vá thật 8/10; vòng sau chỉ 2 lớp P2. SPEC: 80%, chưa chạm tín hiệu không hội tụ; câu skill số lỗi giảm mà hạng không giảm: chưa hội tụ.
```
  kết luận   : LỖI — hai phép đo khác nhau và skill không thực hiện chốt dừng đã đóng băng.

HƯỚNG 8: M4/M6/A5 — chuyển lớp còn lỗi thành nợ và cắt tiêu chí
  giả thuyết : Nếu chống thu hẹp chỉ nói bỏ đường dẫn, một lớp có thể biến mất khỏi lần đo kế mà không được ghi là chưa đo.
  lệnh       : `python3 probes/review_checks.py 8`
  output     :
```text
work-packet có chua_do_duoc: False
cross-review có chua_do_duoc: False
Đường trực tiếp: bỏ đường dẫn khỏi diff => work-packet 149-151 gọi là LÁCH và đòi revision: bị chặn.
Đường khác: giữ nguyên hai đường dẫn, bỏ một tiêu chí/phần hành vi còn lỗi, ghi lớp là nợ thuộc packet khác theo 140. Không đổi write set nên câu 150 không kích hoạt; không có nghĩa vụ ghi chua_do_duoc và không tính là vá như A5 đòi.
Protocol §3.2 vẫn buộc revision nếu đổi spec; vì vậy đây là thiếu nghĩa vụ audit/carry-forward trong adapter, không chứng minh đã có quyền sửa spec.
```
  kết luận   : LỖI — thiếu dấu vết bắt buộc cho cắt tiêu chí/phạm vi trong cùng write set; chỉ thị đổi cách làm ở lần ba có mặt.

HƯỚNG 9: Tự áp M8/M10 — phân biệt git facts và Actions facts
  giả thuyết : Nếu lấy quan hệ tổ tiên làm bằng chứng không gọi CI tay, hoặc lấy ref đóng băng làm head GitHub hiện tại, lời khai vượt phép đo.
  lệnh       : `python3 probes/review_checks.py 9`
  output     :
```text
git rev-parse origin/master: rc=0; 85fcbf8aea75f0577f47d7332c02a50f993a9d1b
git merge-base --is-ancestor origin/master HEAD: rc=0; 
git merge-base --is-ancestor 3c7df6d 85fcbf8: rc=0; 
Tệp receipt/run cho #529/#523: không có trong bundle và cây tracked; EVIDENCE chỉ nêu hai run_id và lời khai không gọi tay.
M8: không drift so ref đóng băng được chứng minh; độ mới của ref ngay trước lúc phóng không đo được offline.
M10 tự áp: chưa có event metadata/run history để kiểm 0 workflow_dispatch; KHÔNG ĐO ĐƯỢC, không suy từ git ancestry.
```
  kết luận   : KHÔNG ĐO ĐƯỢC cho thời điểm fetch và lịch sử CI; quan hệ tổ tiên khớp. Không tạo finding chỉ vì sandbox thiếu dữ liệu mạng.

HƯỚNG 10: Khẳng định lịch sử #522 — số hạng và phạm vi hiện vật
  giả thuyết : Nếu ba tệp được đếm đúng nhưng chứa thay đổi sản phẩm, lời khai head đổi chỉ vì hiện vật review vẫn sai.
  lệnh       : `python3 probes/review_checks.py 10`
  output     :
```text
git diff --numstat 7bdd8ad 73558aa rc=0
1	0	ops/reviews/README.md
151	0	ops/reviews/pr526-review-3-codex-verdict.md
163	0	ops/reviews/pr526-review-3-codex-verdict.receipt.yaml
số tệp=3; tất cả ops/reviews=True
Đã đối chiếu tên: README mục lục + verdict lượt 3 + receipt lượt 3. Không có đường dẫn sản phẩm. Trạng thái approve/merge GitHub trực tiếp vẫn chưa đo.
```
  kết luận   : KHÔNG PHẢI LỖI — số 3 và thành phần của nó cùng khớp; không suy trạng thái GitHub từ diff.

## BẢNG ĐO

Phạm vi đo là SHA đóng băng, không phải trạng thái GitHub hiện tại. Lệnh nền và mã thoát từng tiến trình ở `probes/baseline.py`, `probes/baseline-results.json`, output nguyên ở `probes/baseline-*.txt`. Các phép đọc H1–H10 nằm trong `probes/review_checks.py`; kết quả từng hướng đã ghi ngay sau khi chạy. H9 không được dùng để đủ số hướng đã đo: ngay khi loại H9 và mọi phép đo nền, vẫn còn 9 hướng độc lập.

| khẳng định | SPEC/EVIDENCE/PR khai | bạn đo được | khớp? |
|---|---|---|---|
| Exact head | `2c466acaa8e6d3324311784ae14cda7a402b51b8` | `git rev-parse HEAD` đúng SHA; tree `dfc882706fd7134d3509eb0ca29fb59e75998c32` | Có |
| Base | `85fcbf8aea75f0577f47d7332c02a50f993a9d1b` | `origin/master` đúng SHA này; là tổ tiên HEAD, rc=0 | Có, cho ref đóng băng |
| Spec hash | `4ada6921503da3748ef54b019633e440d21a8f23c3c15f7e1064fe8f3ae85a58` | SHA-256 byte `SPEC.md` đúng nguyên giá trị | Có |
| Diff cross-review | 56 thêm, 1 xoá | `git diff --numstat 85fcbf8 HEAD`: 56, 1 | Có, đã kiểm số hạng |
| Diff work-packet | 76 thêm, 0 xoá | Cùng lệnh: 76, 0 | Có, đã kiểm số hạng |
| Tổng diff / A9 | 2 tệp, 132 thêm, 1 xoá; ≤3 tệp, ≤300 thêm | 2 tên đúng write_set SPEC; 56+76=132; diff.patch bằng byte git diff | Có; lease trực tiếp chưa đo |
| Tài liệu docs | 73, không đổi | Đếm tracked `docs/**/*.md`: 73; diff không chạm docs | Có |
| Manifest không bị ảnh hưởng | Tập giao đường dẫn rỗng | Giao tên trong diff với `files[].path` của manifest = `[]` | Có |
| Sandbox | full mirror, abbrev=7, sạch | is-shallow=false; core.abbrev=7; status rỗng trước và sau probe | Có |
| Ref nguồn/mirror | Nguồn 357; thiếu 0, thừa 1 | Mirror sandbox có 358 heads. Không có snapshot danh sách 357 nguồn để so từng tên; không dùng 357+1=358 để chứng minh tập con | KHÔNG ĐO ĐƯỢC quan hệ thiếu/thừa |
| Nền ↔ sandbox | Bốn cổng cùng rc=0 | Tái chạy bốn cổng sandbox rc=0; không đọc kho nguồn ngoài sandbox | KHÔNG ĐO ĐƯỢC nửa nền |
| doctrine-scan | rc=0, quét 7 tệp, 0 chỗ chép | Gốc rc=0, đúng 7 tệp; hai mutant cấm của A13 cũng rc=0 | Khớp output, không khớp kết luận A13 |
| idiom | rc=0, không gọi Python trần trong skill | rc=0, 7 ca, 0 bỏ qua, 9 mutant; TỔNG ĐẠT | Có |
| adr-song | rc=0 | rc=0; 48 ADR/48 dòng, khớp 1–1 | Có |
| doc-claims-check | strict rc=0 | rc=0, `ok=true` | Có |
| release-verify | strict rc=0 | rc=0, `ok=true`, `errors=[]`, hash khớp | Có |
| diff whitespace | rc=0 | `git diff --check 85fcbf8 HEAD` rc=0 | Có |
| lease-publish | 155/155, rc=0 | Không chạy wrapper: có bước cài actionlint có thể dùng mạng/đọc ngoài sandbox. Không coi lời khai là kết quả tự đo | KHÔNG ĐO ĐƯỢC |
| M1/M2/A1 | Ba điều kiện dừng khác nhau; sensitive cần approve | Sensitive có câu bắt buộc approve; bảng ba lớp vắng; routine còn P2 bị lệnh chung bắt review tiếp | Một phần; H5 |
| M3/A2 | Bảng lớp bắt buộc, gán duy nhất, có bản vá theo lớp hoặc lý do vá lẻ | Định nghĩa cơ chế/slug/hạng cao nhất dùng được; thiếu bảng và trường kế hoạch trong khung verdict | Một phần; H6 |
| M4/A3 | Lần ba cấm vá lẻ, đổi cách làm hoặc Rescue | Có chữ CẤM và liệt kê hết đường vào trước sửa; cùng một slug không đếm theo số thể hiện | Có về nghĩa vụ này |
| M5/A4 | Hai vòng liên tiếp tỉ lệ VÁ THẬT <50% ⇒ dừng/hỏi | Không có công thức/ngưỡng/hành động; thay bằng hạng P1/P2. 4/13=30.7692%; 3/12=25% | Không; H7 |
| M6/A5 | Thu hẹp ⇒ chua_do_duoc, không tính là vá; gọi tên cắt tiêu chí | Chỉ nói rõ trường hợp bỏ đường dẫn và đổi write_set; không có nghĩa vụ ghi chua_do_duoc | Không đầy đủ; H8 |
| M7 được M10 sửa / A12 | Ba loại; gọi tay trước merge N=0; #512 đạt | Ba hàng có mặt; mutant mở N làm ĐỎ phép đọc. Chuỗi tự động full job vẫn thuộc (a), dispatch hậu merge thuộc (a) | Có về nghĩa văn bản; lịch sử #512 chưa đo |
| A8 / nợ cưỡng chế | Phải khai chỉ là kỷ luật đọc | Có tuyên bố rõ ở work-packet 191–194 và cross-review 132–134 | Có về khai giới hạn |
| M8/A10 | Phân biệt hai nguyên nhân và phải đo drift trước vòng dự đoán cuối | Gốc đạt phép đọc; giữ câu cũ hoặc đổi phải thành nên đều ĐỎ | Có |
| M9/A11 | Miễn review do head đổi, vẫn CI hậu merge, lỗi thì mở vòng | Ba mệnh đề 160–162 độc lập; câu giải thích lặp lại (ii)/(iii). Chỉ xoá hàng chưa xoá hết nghĩa vụ, nhưng đã thiếu cấu trúc bắt buộc | Có; không tạo finding do câu giải thích lặp |
| A13 có phép ĐỎ | Chép §5.1 hoặc trần ⇒ ĐỎ | Hai mutant rc=0; đối chứng cụm §12 rc=6 | Không; H4 |
| Nội dung chép doctrine ngoài từ khoá | Skill chỉ TRỎ | Work-packet 138 diễn đạt lại luật lần ba của §12; M4/A3 đồng thời đòi nêu luật ấy. Đây là căng thẳng trong SPEC; không tách thành finding nội dung để phạt việc làm đúng M4 | Scanner không chứng minh được “không chép” |
| #522: head đổi vì hiện vật | 7bdd8ad→73558aa, đúng 3 tệp ops/reviews | README + verdict lượt 3 + receipt lượt 3, numstat lần lượt 1/0, 151/0, 163/0 | Có cho số và thành phần |
| #512: hai CI đỏ rồi xanh; ba vòng cuối không dispatch | EVIDENCE/SPEC nêu lịch sử Actions | Git không chứa event/conclusion đầy đủ để tái đo; không gọi mạng | KHÔNG ĐO ĐƯỢC |
| Tự áp M8 | Đo ngay trước phóng, không drift | Hai quan hệ tổ tiên đều rc=0; độ mới ref tại thời điểm phóng không tái dựng được | Khớp DAG; thời điểm KHÔNG ĐO ĐƯỢC |
| Tự áp M10 | Không gọi tay; hai run in_progress | Không có Actions history để chứng minh 0 dispatch hoặc kết luận hiện tại | KHÔNG ĐO ĐƯỢC |
| Lease và PR trực tiếp | Lease có hạn, #529 draft | Bundle không có hồ sơ authority/lease tương ứng; không truy cập GitHub | KHÔNG ĐO ĐƯỢC, không suy thành vi phạm |

Các số của #508 trong H7 là dữ liệu nghiệm thu đóng băng được r1 cung cấp, không phải lịch sử CI/review canon đã tự xác minh. Phép thử độc lập 10 lớp → vá thật 8 → còn 2 lớp cùng P2 dùng để phân biệt hai định nghĩa hội tụ, không được khai thành ca lịch sử có thật.

### sai-dai-luong-hoi-tu  [P1]  M5 bị đổi từ tỉ lệ vá thật thành mức nghiêm trọng, mất chốt dừng

CƠ CHẾ SINH LỚP: Đọc nhầm “phân hạng finding vòng trước” (ĐÃ VÁ THẬT/VÁ HỜ/VÁ SINH LỖI MỚI/CHƯA VÁ) thành severity P1/P2. Hai đại lượng không thay thế nhau; điều kiện hành động bắt buộc từ đại lượng gốc cũng biến mất.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `.claude/skills/work-packet/SKILL.md:146` | Hội tụ đo bằng phân hạng; số lỗi giảm mà hạng không giảm thì chưa hội tụ | Không dùng VÁ THẬT, không công thức hoặc hai vòng liên tiếp; không lệnh DỪNG/HỎI tại ngưỡng M5 |

VẤN ĐỀ: SPEC r2 giữ M5/A4 của r1, nơi định nghĩa rất cụ thể `VÁ THẬT / số finding vòng trước < 50%` trong hai vòng liên tiếp. Skill thay mục tiêu ấy bằng một heuristic khác. Với 8/10 lớp được vá thật và hai lớp còn lại vẫn P2, skill gọi chưa hội tụ chỉ vì hạng không giảm, dù tỉ lệ là 80%. Với mẫu nghiệm thu #508, skill không tính được chốt DỪNG/HỎI ở vòng 3 mà hợp đồng yêu cầu. Đây là lỗi ở quyết định tiếp tục một chuỗi sửa chưa hiệu quả, không chỉ thiếu một phép tính minh hoạ; hạng P1 vì làm mất điều kiện dừng bắt buộc của quy trình dùng cho packet sensitive.

ĐÃ THỬ VÁ: không — không viết patch cho skill điều khiển review/authority. Hướng sửa: thay phép đo severity bằng phép đo phân hạng bản vá theo hợp đồng, xác định mẫu số theo đơn vị lớp đã được chủ kho chỉ thị, rồi ràng hành động dừng/hỏi. Nếu phải đưa nguồn quy tắc ra ngoài write_set để tránh chép doctrine, cần xử lý revision với chủ kho, không âm thầm đổi công thức. Ca khoá: mẫu #508 phải bắn ở vòng 3; ca 80% cùng hạng không được bắn do M5. Rủi ro cần kiểm: đổi đơn vị finding→lớp có thể đổi tỉ lệ; phải giữ ánh xạ thể hiện, không cộng trùng.

ĐÃ THỬ NGHIỆM: `python3 probes/review_checks.py 7` — gốc không có VÁ THẬT/ngưỡng; 4/13=0.307692 và 3/12=0.25; ca đối chứng 80% cho hai kết luận khác nhau.

ĐỘ TIN: cao

### gop-dieu-kien-dung-review-class  [P2]  Luật hành động gộp routine với systemic khi còn P2

CƠ CHẾ SINH LỚP: Mất ánh xạ điều kiện dừng theo class ở đầu ra reviewer và đầu vào executor, rồi dùng một nhánh “còn P1 hoặc P2” chung cho mọi packet.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `.claude/skills/cross-review/SKILL.md:369` | Phần mới hiện thực quy trình đếm/review M1–M7 | Toàn skill có 0 hàng ánh xạ routine/systemic/sensitive sang điều kiện dừng mà A1 bắt buộc |
| `.claude/skills/work-packet/SKILL.md:125` | Dừng theo review_class; dòng 133 bắt vá rồi review khi P1 hoặc P2 còn mở | Không có routine/systemic; routine 0 P1 + P2 đã ghi nợ vẫn bị lệnh chung bắt mở vòng |

VẤN ĐỀ: M1 r1 phân biệt routine (0 P1, P2 thành nợ), systemic (0 P1/P2), sensitive (approve). Câu chỉ nhắc sensitive không cung cấp hai nhánh còn lại; con trỏ §8/§13 cũng không thay bảng nghiệm thu A1. Hậu quả cụ thể là tiêu tốn vòng review của packet routine đã đạt ngưỡng đóng băng. Không báo bypass sensitive: câu đòi approve tường minh vẫn có hiệu lực khi đọc toàn mục.

ĐÃ THỬ VÁ: không — hướng sửa là khôi phục ánh xạ ba lớp và buộc bảng hành động sử dụng nó, giữ nguyên yêu cầu approve của sensitive. Ca khoá dùng cùng verdict 0 P1, 1 P2 có nợ trên ba class: routine đủ điều kiện, systemic chưa đủ, sensitive thiếu approve chưa đủ. Rủi ro: không biến P2 thường thành nợ tự động nếu chưa ghi Issue.

ĐÃ THỬ NGHIỆM: `python3 probes/review_checks.py 5` — 0 hàng ánh xạ; routine/systemic vắng trong work-packet; đã đối chiếu chuỗi nêu trên bằng nghĩa văn bản.

ĐỘ TIN: cao

### thieu-hop-dong-ban-va-theo-lop  [P2]  Định nghĩa lớp có mặt nhưng không buộc bàn giao kế hoạch đóng lớp

CƠ CHẾ SINH LỚP: Thay hợp đồng dữ liệu remediation bằng phần giải thích đơn vị đếm. Bên sinh verdict không bắt xuất bảng, bên nhận mặc định bảng tồn tại nên không kiểm đủ thông tin trước sửa.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `.claude/skills/cross-review/SKILL.md:369` | BẢNG LỚP và slug ổn định | Bảng hiện có chỉ là “trường/đếm gì”; khung verdict ở 400 không có BẢNG LỚP, ánh xạ thể hiện hay cột bản vá theo lớp/lý do vá lẻ |
| `.claude/skills/work-packet/SKILL.md:129` | Bên ĐỌC bảng lớp reviewer sinh ra | Bảng hành động không đòi kiểm bảng remediation đầy đủ trước khi sửa; không đòi lý do nếu phải vá lẻ |

VẤN ĐỀ: M3/A2 đòi mỗi finding thuộc đúng một lớp và mỗi lớp có bản vá đóng lớp hoặc lý do vá lẻ. Phần mới định nghĩa cơ chế, hạng cao nhất và slug rất rõ, áp dụng được vào chính lượt review này; finding không phải “không biết thế nào là lớp”. Lỗi là reviewer có thể điền toàn bộ khung được cung cấp mà không giao phương án đóng lớp, rồi executor vẫn bắt đầu vá. Cơ chế gây vá từng vị trí do reviewer chỉ ra chưa bị hợp đồng đầu ra chặn.

ĐÃ THỬ VÁ: không — hướng sửa là thêm bảng bắt buộc nối một slug lớp với các thể hiện và bản vá theo lớp/lý do vá lẻ; bên executor kiểm đầy đủ trước sửa. Đừng tạo một bộ slug thứ hai mâu thuẫn chỉ thị đếm lớp. Ca khoá: 5 thể hiện cùng cơ chế phải ra 1 lớp/5 thể hiện; thiếu phương án hoặc thể hiện không thuộc lớp nào phải thiếu verdict. Rủi ro: đếm trùng khi cùng một thể hiện bị gán hai lớp.

ĐÃ THỬ NGHIỆM: `python3 probes/review_checks.py 6` — không có cột remediation, không có mục BẢNG LỚP trong khung verdict; ca 1 lớp/5 thể hiện vẫn áp dụng được định nghĩa.

ĐỘ TIN: cao

### mat-dau-vet-thu-hep-pham-vi  [P2]  Chống cắt đường dẫn chưa giữ dấu vết cắt tiêu chí hoặc chuyển lỗi sang nợ

CƠ CHẾ SINH LỚP: Chỉ kiểm sự thay đổi write_set, bỏ nghĩa vụ ghi trạng thái chưa đo và không tính là vá khi phạm vi hành vi/tiêu chí bị cắt trong cùng tập tệp.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `.claude/skills/work-packet/SKILL.md:149` | Thu hẹp là lách, đổi write_set phải revision | Không có nghĩa vụ `chua_do_duoc`/không tính là vá của A5; đoạn 140 cho ghi lớp ngoài khả năng đóng thành nợ packet khác nhưng không nối việc đó với dấu vết lớp còn mở |

VẤN ĐỀ: M6/A5 không chỉ cấm xoá tên tệp khỏi diff; nó bắt khai việc cắt tiêu chí là chưa đo, không phải bản vá. Giữ tên tệp nhưng cắt một nhánh hành vi có finding không làm điều kiện “đổi write set” kích hoạt. Câu tổng quát gọi thu hẹp là lách là đúng, nhưng không cung cấp dấu vết bắt buộc để lượt sau biết lớp còn sống. Protocol vẫn cấm tự đổi spec; finding này không khẳng định đã được cấp quyền cắt spec. Nó chỉ ra lỗ hổng bàn giao khiến một lần thu hẹp có thể bị báo như đã đóng lớp.

ĐÃ THỬ VÁ: không — hướng sửa: mọi thu hẹp hoặc chuyển nợ phải giữ slug, ghi phần `chua_do_duoc`, không đánh dấu ĐÃ VÁ THẬT; cắt tiêu chí cũng áp dụng khi write_set không đổi. Ngoài phạm vi thì nối sang đường revision/Rescue đã có. Ca khoá: bỏ đường dẫn và bỏ tiêu chí trong cùng đường dẫn đều giữ lớp chưa đóng. Rủi ro: phân biệt việc thu hẹp phải xin revision với tái cấu trúc triển khai vẫn đáp ứng đầy đủ acceptance.

ĐÃ THỬ NGHIỆM: `python3 probes/review_checks.py 8` — cả hai skill không có `chua_do_duoc`; đã đối chiếu riêng đường bỏ tệp (bị chặn) và đường cắt tiêu chí (thiếu audit bắt buộc).

ĐỘ TIN: cao về thiếu nghĩa vụ A5; vừa về khả năng executor đọc lệch trong một phiên thực tế.

### phep-do-doctrine-khong-du-rang  [P2]  A13 tự phán đạt bằng scanner không phát hiện hai phép ĐỎ bắt buộc

CƠ CHẾ SINH LỚP: Dùng kết quả không khớp danh sách cụm từ để chứng minh không sao chép quy tắc. Bộ đo phân biệt từ vựng, không phân biệt nội dung quy trình cần cấm.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `EVIDENCE.md:22` | A13: quét 7 tệp, 0 chỗ chép doctrine | Đúng output scanner gốc, nhưng output này cũng xuất hiện sau khi chép điều kiện §5.1 vào skill |
| `EVIDENCE.md:78` | A13 ĐẠT từ rc=0 và grep không thấy trần | Thêm câu trần 10 vòng và chép đoạn điều kiện §5.1 đều rc=0; chưa có bằng chứng âm chứng minh A13 đầy đủ |

VẤN ĐỀ: SPEC A13 dòng 118 đòi hai phép này làm ĐỎ. Probe đã đột biến trực tiếp skill trong bản sao rồi phục hồi byte gốc. Cả hai biến thể vẫn xanh; đối chứng `3 attempt/packet` trả rc=6 nên không phải chạy sai root hoặc bỏ scanner. Đây là thiếu bằng chứng nghiệm thu mà packet dựa vào để tuyên bố đạt, không phải một phát hiện mới về implementation scanner ngoài write_set. Việc scanner vốn có giới hạn không cho phép kết luận A13 đã đủ răng. Cũng không được nâng output “0 chỗ chép” thành chứng minh nội dung mỏng chỉ vì số trần không xuất hiện ở bản gốc.

ĐÃ THỬ VÁ: không — đã thử đột biến nghiệm thu, chưa vá scanner/skill. Hướng xử lý trong phạm vi: thay tự phán toàn bộ A13 bằng bằng chứng đọc nội dung có ca dương/âm chạy được và công bố rõ giới hạn scanner. Nếu hợp đồng buộc chính scanner phải ĐỎ, đó là thay đổi công cụ ngoài write_set, cần owner xử lý revision/dependency; không tự mở phạm vi. Ca khoá: gốc xanh; từng bản sao trần và §5.1 đỏ; con trỏ thuần vẫn xanh. Rủi ro: thêm riêng hai từ khoá chỉ chữa hai mẫu, không chứng minh mọi cách chép nghĩa đã bị chặn.

ĐÃ THỬ NGHIỆM: `python3 probes/review_checks.py 4` — gốc rc=0; mutant trần rc=0; mutant §5.1 rc=0; đối chứng rc=6. Output nguyên ở `probes/h4.txt`.

ĐỘ TIN: cao

## Chốt lượt review

`findings_ids`: `sai-dai-luong-hoi-tu`, `gop-dieu-kien-dung-review-class`, `thieu-hop-dong-ban-va-theo-lop`, `mat-dau-vet-thu-hep-pham-vi`, `phep-do-doctrine-khong-du-rang`.

Đếm theo cơ chế: **5 lớp**, gồm **1 P1 + 4 P2 + 0 P3**; tổng **8 thể hiện** trong các bảng trên. M1/M3/M5/M6 không gộp thành một lớp “thiếu SPEC”: chúng lần lượt làm sai quyết định dừng theo class, mất hợp đồng remediation, dùng sai đại lượng hội tụ và mất dấu vết scope; mỗi cơ chế cần một phép khoá khác nhau.

Reviewer: Codex/OpenAI, phiên độc lập với executor Claude; công cụ shell trong sandbox. Review neo exact SHA ở đầu tệp. Không commit, không gọi mạng, không đăng PR; `VERDICT.md` này là nguồn có thẩm quyền. `git -C cay-kho status --porcelain` sau thử nghiệm rỗng. Các tệp probe là dữ liệu review, không phải bản vá đề nghị áp lên nhánh executor.

**Không approve ở lượt 1.** Các phần khớp và các giới hạn KHÔNG ĐO ĐƯỢC đã được giữ trong bảng; lý do changes_requested là các lớp lỗi nêu trên, không phải vì thiếu dữ liệu GitHub trực tiếp.
