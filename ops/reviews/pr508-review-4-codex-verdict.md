# VERDICT — PR #508 lượt 4 (reviewed_sha 41e83b5)
KẾT LUẬN: changes_requested
ĐẾM: 4 P1 · 6 P2 · 1 P3

Reviewer: Codex / OpenAI, bề mặt API, transport machine, shell cục bộ; khác nền với executor Claude theo phân công trong PROMPT.md. `reviewed_sha`: `41e83b54fffc0672268b9512aef1afd4fff57cc7`; tree: `77accc7530e5b920cf379f130d94d9e9c419b2e9`.

Chỉ đọc trong thư mục được giao, không mạng, không sửa `cay-kho/`, không dựng payload tấn công. Đã chạy phép đo đọc AST/YAML, đối chiếu byte Git, đếm hiện vật và số học Decimal; rc=0. Không chạy benchmark, CI, actionlint hoặc mutant. Các phản chứng dưới đây là **review mô hình**, trừ những phép đọc/đếm/tính được ghi rõ là đã chạy. Không lấy câu “đã đo” của executor làm lời khai thực thi của reviewer.

Quy ước dòng: **G** = `cay/GATE-TACH-JOB-CAT-CHI-PHI.md`; **T** = `cay/T125-RA-JOB-RIENG.md`; **C** = `cay/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md`; **G3/T3/C3** = ba tệp `cay/LUOT3-*.md`; **E** = `EVIDENCE.md`.

**(A) Chưa đóng được lớp.** Hợp đồng số job và metadata đã thống nhất. Nhưng ngay trong bản T mới, “2,93 trên mọi nền” và “đủ để đưa job về dải đã đo” vẫn sống cạnh lời khai chưa đo bội số Windows và không bảo đảm chạy trọn. Không cần khối REVISION để tạo lại hai lời khai ngược nhau.

**(B) Có mất mát thực chất.** Đáng chú ý nhất: mất yêu cầu sinh mới dấu phiên, mất thời điểm require trước merge, mất phản chứng shellcheck bắt buộc, và mất hai giới hạn của ước tính từ lượt bị cắt. Một phần khác là thu hẹp phạm vi có khai, nhưng không thể tính là vá finding.

## MẤT MÁT DO VIẾT LẠI

Các hàng gộp theo nghĩa vụ, không đếm mỗi dòng văn bị xoá thành một finding. “ĐÚNG BỎ” bao gồm chuyển nguyên nghĩa vụ tới đúng nơi; cột bằng chứng chỉ ra nơi giữ. Những đoạn dữ liệu cũ không còn được dùng có thể bỏ, nhưng giới hạn vẫn gánh một suy luận hiện hành thì không thể bỏ theo chúng.

| thứ biến mất | tệp/dòng bản cũ | ĐÚNG BỎ / MẤT OAN | bằng chứng |
|---|---|---|---|
| Nhật ký revision, phương án gộp M8/M9 đã bị thay, các mốc SHA/lease #456 hết hiệu lực | G3:10–59,72–172,929–941 | ĐÚNG BỎ | G:7–13,120–137,395–403 giữ đo lại neo, cạnh T125/#502 và canh lease; không cần giữ chỉ thị cũ. |
| A10/A11 gạch bỏ trong GATE | G3:943–965 | ĐÚNG BỎ đối với bản sao | T:A1/A2/A3 giữ việc đo bỏ tải, job phải tồn tại và cờ bỏ phải hạch toán; A2c bổ sung đo A/B. Riêng mất phép đo bỏ tải **Windows** ghi hàng riêng, không coi việc di chuyển tên tiêu chí là đã bảo toàn nó. |
| Những câu ba job/ba runner/mỗi lần thêm một job | G3:683,729,882 | ĐÚNG BỎ | G:A4/A6 và T:A6 nhất quán 1→2→4; lần thêm 1 rồi 2. |
| Lối composite được mời dù write set cấm | G3:558–563 | ĐÚNG BỎ | G:100–103 khai rõ lý do bỏ; A8 giữ đúng hai đường. Đây là bỏ lời mời trái hợp đồng, không phải lén bỏ một acceptance. |
| Các bảng thời lượng tháng 9 đầu kỳ, dải hệ số cũ và mô tả nhánh/master dài | G3:249–437,487–522 | ĐÚNG BỎ phần số liệu không còn dùng | Ngưỡng hiện hành giữ 36 phút; G:A5 vẫn công bố billing; hiện vật cũ còn trong kho. Không tiếp tục mang dải cũ làm cận tương lai. |
| Quy tắc phân biệt số bước YAML với mục API, giải thích độ phân giải giây và mẫu tiện tay | G3:319–325,358–401,448–451 | ĐÚNG BỎ phần thuyết minh cũ, cần giữ đơn vị nơi dùng | G:G7 khai 40 bước YAML; A5 phân biệt job/instance/API. Bảng đo này vẫn phân biệt hai đơn vị. Không tìm thấy một acceptance đếm 40 mục API thay 40 bước YAML. |
| Chưa phân rã theo bộ trên Windows, proxy selftest không phải vòng mutant | G3:388–401,994 | MẤT OAN phần nợ còn mở | G:147 chỉ còn “hiệu quả chưa đo”, bỏ điều kiện mở packet song song **sau khi có phân rã** ở G3:636–637. G3:994 có trạng thái ĐÓNG MỘT PHẦN của #456, không có câu mới bác hay chuyển trạng thái này. Gộp trong finding `mat-phan-chung-va-no-phan-ra`. |
| Nghĩa vụ phản chứng shellcheck mới trên nền đã có lỗi | G3:770–774 | MẤT OAN | G:246–255 giữ phép đa tập nhưng bỏ ca bắt buộc; ca bắt buộc cuối A3 chỉ còn `if` không delimiter. Finding `mat-phan-chung-va-no-phan-ra`. |
| Nhánh A2 nền bị cắt | G3:701–716 | ĐÚNG BỎ bản dài, KHÔNG mất nghĩa vụ | G:222–227 vẫn có nhánh, cùng trạng thái có điều kiện và giới hạn. Không báo nhầm nhánh này bị xoá. |
| Ngoại lệ A5 trước tách bị cắt và nợ #0 về nền hiện tại | G3:857–860,999–1004 | MẤT OAN phần giới hạn còn hiệu lực | G:329–330 đòi nền mới hợp lệ tuyệt đối; G:196–199 dùng lượt trước #492 để tuyên bố không còn nhánh thiếu nền. Lượt cũ chỉ bác mệnh đề “chưa bao giờ hoàn tất”, không chứng minh nền mới. Finding `nen-cu-khong-bac-duoc-no-nen-hien-tai`. |
| Mốc require **TRƯỚC merge** của cả hai packet | G3:884–887; T3:250–254 | MẤT OAN | G:342–373/T:231–265 thêm đọc trạng thái nhưng không còn mốc trước merge; bảng mô tả trạng thái sau land. Finding `mat-moc-require-truoc-merge`. |
| Nghĩa vụ đo lại A1/A5 ngay trước merge | G3:1043–1046 | MẤT OAN phần làm mới khi đầu vào đổi | G:12–13 chỉ đo lại lúc cấp lease, G:A5 lúc thi công. Cần giữ nghĩa vụ khi head/đầu vào phép đo đổi; không đòi chạy lại vô điều kiện khi chỉ master trôi và protocol miễn. Gộp `nen-cu-khong-bac-duoc-no-nen-hien-tai`. |
| #0a thiếu hiện vật benchmark | G3:1006–1014; T3:305–308 | ĐÚNG BỎ đối với benchmark mới | Có `hien-vat/benchmark.txt` và lệnh; T:298–300 buộc đo lại. Không xác thực lại thời lượng cũ bằng hiện vật mới. |
| #0b tăng trưởng suite/biên nhận chưa có người canh | G3:1016–1021 | MẤT OAN phần nợ tổng quát | G:436–438/T:295–297 chỉ giữ phần #492; mất nợ chi phí tăng theo số biên nhận. Các con số proxy cũ có thể bỏ, nhưng nợ không chỉ là #492. Gộp `mat-phan-chung-va-no-phan-ra`. |
| Nhiễu runner, hệ số billing chưa kiểm hoá đơn, không có Windows local, chờ runner | G3:1023–1042,1048–1050,1055–1056 | ĐÚNG BỎ bản dài | G:419–435 giữ đủ bốn giới hạn. |
| Thời lượng thật bước 20 là cận dưới; phần bước 21–41 chưa đo | T3:61–83,295–304 | MẤT OAN | T:56–64 chỉ giữ giả định bội số Linux=Windows, thay phép cộng có phần đuôi bằng trừ thẳng từ job bị cắt. Finding `uoc-moi-bo-mat-phan-duoi-bi-cat`. |
| Biên 3,74–8,68, max mẫu 2,89 bị gọi cận trên thật | T3:77–83,309–311 | ĐÚNG BỎ các số sai | Không còn trong T mới; nhưng phép ước thay thế sinh lỗi mất phần đuôi, không được coi toàn finding đã đóng. |
| Vế bắt buộc Windows của A1 và miễn đo trước land | T3:156–195 | ĐÚNG BỎ miễn đo; MẤT OAN phép phân biệt theo Windows | T:134–155 chuyển bắt buộc sang Ubuntu, khai Windows chỉ công bố. Có khai thu hẹp, nhưng không thay bằng phép chứng minh bỏ tải Windows. Finding `a1-ubuntu-khong-chung-minh-bo-tai-windows`. |
| Một phần tử của phép chiếu A4, thiếu literal và thiếu canh skipped | T3:232–240 | ĐÚNG BỎ | T:189–220 có tên literal, tích số nền, phép dedup và canh skipped; sửa đúng lỗi lực lượng. |
| Chữ “song song” trong M1 T125 | T3:147 | MẤT OAN phần ràng buộc lịch chạy | T:112/A5 không cấm `needs` nối gate với gate-t125; A1 chỉ đo thời lượng một bước. Gộp `a1-ubuntu-khong-chung-minh-bo-tai-windows`; đổi chỗ không tự chứng minh ra khỏi đường tới hạn workflow. |
| Lịch sử 16→14 assert, #463 r5, §12 kích hoạt sai, ngoại lệ ADR của #502 | C3:3–17,123–130,263–276,299–307 | ĐÚNG BỎ | C:94,114–120,129,148–153,254–261 giữ 14+2 và hai chiều 2/1; A8 vẫn dừng khi vượt. |
| Phân loại ba mức chứng cứ của CHAM | C3:21–35 | ĐÚNG BỎ phần lặp; chưa bảo toàn nhãn mọi số | C:19 đánh nhãn log THUẬT LẠI, nhưng các phép 44 lượt ở C:265–272 vẫn không có log/lệnh đầy đủ. Gộp `hien-vat-khong-chua-so-dang-duoc-vien-dan`. |
| Nghĩa vụ **dấu phiên ngẫu nhiên sinh mới mỗi lượt** | C3:150 | MẤT OAN | C:135 chỉ đòi mang/so dấu phiên; A5c(1) chỉ kiểm một dấu khác dựng sẵn. Finding `dau-phien-mat-nghia-vu-sinh-moi`. |
| Chống mã sản phẩm ghi trực tiếp kênh | C3:225–238 | MẤT OAN theo phạm vi cũ; thu hẹp CÓ KHAI | C:62–80,214–224,278–285 loại mã đối kháng khỏi hợp đồng. Sửa sai mô hình quyền là đúng; không phải đã chặn đường cũ. Finding `thu-hep-cham-khong-phai-va-kenh`. |
| Nguyên nhân Errno39 chưa biết, chạy cả vòng mutant trong môi trường ký, hai repo, retry một lần | C3:117–140,149–219,282–297 | ĐÚNG BỎ bản dài | C:108–120,129–135,169–198,265–277 giữ các nghĩa vụ; không mất A5b subprocess thật và ba ca biên. |

## ĐỐI CHIẾU LƯỢT 3

Giữ nguyên **11 slug**. Kết quả: **4 ĐÃ VÁ THẬT · 3 VÁ HỜ · 3 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Phân loại theo finding toàn phần; một tiểu phần đúng không đóng phần còn lại.

| slug lượt 3 | phân loại | bằng chứng lượt 4 |
|---|---|---|
| `lop-ngoai-le-chua-bao-ve-duong-truyen-ket-qua` | VÁ SINH LỖI MỚI | C:A5c(1) nay đổi đúng một biến nên thử được phép so. Nhưng mất sinh mới nonce (C3:150→C:135), còn đường sửa khung được đưa ngoài phạm vi (C:278–285). Không tính rescope là vá. |
| `them-t125-nhung-giu-hop-dong-ba-job` | ĐÃ VÁ THẬT | G:A4 có bốn tên; G:A6/T:A6 nhất quán 1→2→4; không còn lệnh require mỗi lần đúng một job. Phần này thực sự hết lỗi do lịch sử. |
| `a5-hop-le-chua-doi-du-job-va-du-luot` | VÁ HỜ | G:294–303 neo SHA và thêm giải ngữ cảnh, nhưng quét delimiter vẫn bỏ biểu thức `if` không delimiter; fail-close chỉ áp toán hạng đã tìm thấy. |
| `metadata-va-loi-thoat-composite-chua-theo-write-set-r5` | ĐÃ VÁ THẬT | G:7–8 khai wp<T125> và lúc điền; G:100–103 rút composite; C:114–115 giao T125 đúng packet. |
| `so-ci-moi-chua-duoc-khai-la-thuat-lai-trong-spec` | VÁ HỜ | G:57–61 đã rút “bốn lượt/chưa hoàn tất”; nhưng T:22 và T:72 vẫn rộng hơn phép đo ngay cạnh T:63–64,290–293. G3/N6/N7 và nền Ubuntu còn dẫn hiện vật không chứa dữ liệu tương ứng. Lớp lời khai chưa chết. |
| `t125-do-buoc-khong-go-duoc-vong-nen-bi-cat` | VÁ HỜ | T:A1(a) hết miễn đo, đỏ được trên Ubuntu. Vế Windows bị hạ thành success/cancelled sau land, không đo việc bỏ tải riêng Windows; G vẫn coi nền đã có. |
| `uoc-bien-t125-sai-so-hang-va-sai-chieu-can` | VÁ SINH LỖI MỚI | Các cận cũ đã bỏ. T:56–58 lại lấy tổng job bị cắt trừ bước bị cắt và không cộng phần còn lại; mất cảnh báo T3:295–304. |
| `t125-doi-chung-co-cu-chua-chung-minh-than-ca-do` | ĐÃ VÁ THẬT | T:171–178 bắt hai tuple lệch, dùng chính hàm so, thêm tích hợp, no-op phải đổi màu. Implementation tương lai vẫn phải chứng minh đường tích hợp không bỏ hàm so. |
| `t125-a4-mot-phan-tu-khong-phu-hai-nen` | ĐÃ VÁ THẬT | T:194–220 có literal, số nền, dedup setup và canh skipped khi hạ nhánh. Tên chốt lúc thi công phải khớp từng ký tự. |
| `branch-protection-hai-lan-khong-co-phep-do-trang-thai` | VÁ SINH LỖI MỚI | G:346–354/T:235–242 đã có phép đo trạng thái, thiếu trường làm đỏ. Nhưng bỏ nghĩa vụ trước merge; hai luật tên còn mô tả sai hậu quả require tên không tồn tại. |
| `bang-gom-bo-sot-cac-khang-dinh-kiem-duoc` | CHƯA VÁ | E tự khai chưa đầy đủ. Vẫn thiếu các số cấu trúc, hạch toán ca, giới hạn nghiệm thu, scope và nhiều số CHAM; bảng dưới bổ sung. |

## BẢNG ĐO

Các lệnh Git thực hiện đọc; phép xác minh cuối dùng `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` trỏ tên không tồn tại trong cwd, `GIT_OPTIONAL_LOCKS=0`. Không chạy script test của kho. “Khớp hiện vật” không có nghĩa đã xác minh GitHub thật.

| mục | khai | đo lại / điều kiện | kết quả |
|---|---|---|---|
| HEAD/tree, worktree | 41e83b5, sạch | `git rev-parse HEAD HEAD^{tree}` như đầu báo cáo; `git status --porcelain` rỗng | Khớp |
| Byte ba bản mới/cũ | cây hiện hành và lượt 3 | So byte với `git show HEAD:ops/specs/<tệp>` và `git show 0236ca7:ops/specs/<tệp>` | Cả sáu khớp |
| Delta bàn giao | lượt3→4 | Byte patch bằng `git diff 0236ca7 HEAD -- ops/specs` | Khớp; patch gồm **8** spec do cây nền cũng đổi, không chỉ ba tệp review |
| Dòng / REVISION | 1056→445;311→307;307→285;0 khối | `splitlines`, regex đầu heading REVISION | Khớp; G giảm **57,86 %** |
| Băm G/T/C mới | không dùng băm tự gõ của executor | SHA256: G `271bf66a0626bd802dbf9872279432742341b71484e3f139b0a99b4eb2b269fd`; T `533e274c60567c7b856f42107b3e40b4c56edfb37dd0e2a99b39137f3895fef1`; C `34134db96c516cf4bbef9213a3afa2cd5fd821ac276d63b7624fc06c16ca6feb` | Đã tính từ byte |
| G1/N1 | 29 hàng,28 kết thúc;18/8/2 | Parse các hàng bắt đầu run_id: 18 success,8 cancelled,2 failure,1 chưa có kết quả | Khớp |
| G2/N2 | run34429604548;40,63; bước 20 2,97 | Đúng hàng hiện vật; đây là **trước** #492 | Khớp số; không phải nền tại start_from_sha tương lai |
| Dải 18 success | job 40,20–53,53; bước 20 2,45–3,88 | min/max đúng18 hàng success | Khớp |
| G8/N11/E | **8** cancelled ⇒723,96;36,2% | 8 job: **482,55 phút tường ×2 =965,10**; trên mẫu số2000 là **48,255% ≈48,3%** | SAI MẪU; finding |
| N11 sáu lượt sau #492 | có nhắc6 lượt | Sáu run mới nhất:361,98×2=**723,96**;36,198%≈36,2% | Con số thuộc6, không phải8 |
| G3 |13,92+7,42=21,34;34,3%;18,3%;52,5% | Phép cộng và chia40,63 khớp; hiện vật Windows **không có hai bước này** | Số học khớp; thời lượng chưa có chứng cứ trong gói |
| G4/A1 |40,63>36 | Đúng số học; 0,60×60=36 | Không chứng minh mutant ở cây mới trở về40,63 |
| N6/N7 | Win2,97→25,83;Ubu1,22→2,35;8,70×;1,93×;20,2× | Win có hiện vật; Ubu không có. Các thương lần lượt8,6969697;1,9262295;20,2300885 | Khớp số học; phần Ubuntu không truy được về hiện vật dẫn |
| N8 | +1327/−1 | `git diff --numstat 28ba133 0721811 -- ops/lease_publish_test.py` | Khớp |
| N3/N4 |A150,434;B51,321;2,9312;65,88% | A/B=**2,9312367257**; (A−B)/A=**65,8847069147%** | Khớp hiện vật và làm tròn; share là ước từ **hai lần chạy**, không đo riêng t125 trong lượt A |
| Ngưỡng suy T:A1 |1/2,9312=0,3412 | Dùng A/B đầy đủ: B/A=**0,3411529309** | Khớp làm tròn; không suy ra hệ số Windows |
| Benchmark provenance |0236ca7,Python3.11.15,Linux;rc0 cả hai | Có trong benchmark.txt; script ghi lệnh/giờ/rc/tail | Đọc hiện vật, **NOT_RUN**. `.veA.log/.veB.log` không được bàn giao; tail tổng kết có trong txt |
| Hạch toán ca |146 và145+1 | AST tại0236ca7: **146**; tại41e83b5: **147**, thêm t152 từ#503 | Benchmark lịch sử không sai. Khi thi công phải dùng **146+1=147**, theo điều khoản đo lại mẫu số; đối chứng cờ cũ cũng cập nhật |
| T ước mới |26,25/2,9312≈8,96;job≈43,23 |8,9553766376;43,2253766376 | Số học đúng, mô hình thiếu tải chưa chạy |
| T:A1 nền Ubuntu |2,32–2,42 trên5 push/master | Không có cột Ubuntu,run_id năm mẫu,attempt hay timestamp bước trong hiện vật được dẫn | CHƯA XÁC MINH; không được gọi mẫu số có sẵn trong gói |
| G9/G10;T:N12/N13 |60,52/60,32; dãy15,48…16,67; phân rã b14/b15/b16 | Hai thời lượng job và b20 có trong bảng; phần phân rã khác chỉ có văn xuôi/API gợi ý, G10 thiếu ghép từng run | THUẬT LẠI; thiếu hiện vật/lệnh tái tạo đúng mẫu |
| Setup Windows |2,75–3,27 | Có lời kể G3:244–246 gắn hai head; không có timing bước tương ứng trong hiện vật mới | THUẬT LẠI, không phải phép đo lượt4 của reviewer |
| G ước dưới tảiG2 |19,29;16,67–17,19;10,17–10,69 |40,63−21,34=19,29; các phép cộng setup khớp | Ước ba job trên tải trước #492; không đo pha 4 job sau T125 |
| G7/N10 YAML |1 gate;None;60;40 bước;10 if | `yaml.safe_load` trên YAML hiện hành cho đúng các số;0 thân run trùng sau chuẩn hoá | Khớp |
| Toán hạng matrix |event_name/ref/labels;không inputs | Đọc biểu thức matrix.os | Khớp **matrix**; không phải toàn bộ mọi if |
| If không delimiter |phải trích toàn bộ | **7/10** if không delimiter: dòng245,278,319,421,521,541,561 của ci.yml; có runner.os,github.ref vàalways() | Quét delimiter không phủ toàn bộ biểu thức |
| PyYAML/on |so on bằng safe_load/safe_dump | Với loader hiện có, khóa `on` được parse thành boolean **True**, không phải chuỗi `on` | Chưa có implementation để kết luận đã lọt; nghiệm thu phải chỉ rõ loader/khóa, không dùng get('on') rỗng hai vế |
| Hash ci.yml |nguồn hình dạng |SHA256 `8dbc730f8a66a8dc86da9ff487108809b320ba35aa0bdb4bc773da99cd18a22b` | Đã tính |
| Pha/context |1→2→4;require Ubuntu |Dispatch2→4→8 instance;PR thường1→2→4;G thêm1 rồi2 theo chuỗiT/G | Hai bảng khớp nghĩa, **không khớp literal từng dòng**: dòngT-land của G chỉ ghi “thêm”, của T ghi tập đầy đủ |
| G5/N9/ruleset20856202 |active,đúng1 context;API200 và403 | Không có response ruleset/protection,header hoặc snapshot checks trong gói | Không xác minh hiện trạng/HTTP; hợp đồng thiếu trường ⇒ đỏ là có thật |
| Write set/dependency |G2/T2/C1 |G∩T={ci.yml};C rời;hợp4;T chờ503;G chờ502 vàT;C[] | DAG không chu trình; G chuỗi minh hoạ502→T không thay cạnh thực503→T |
| G kích thước |35/17+44/33=79/50;hai158/100;ước135–200 |Đếm khối YAML 35–69, 70–113; số dòng không rỗng/không comment 17, 33; phép nhân khớp | Ước không là additions implementation;trần 300 vẫn phải đo |
| G ngoài phạm vi song song |400 s,270 s,−32,5% |1−270/400=32,5%;không có log phép timing trong gói mới | Chỉ xác minh số học |
| C assert/ca/mutant |14+2=16; 8 ca;10 mutant;233 dòng |AST T1…T8: 1+1+2+1+1+1+2+5=14;hạ tầng 80/198;DOT_BIEN 10;233 dòng | Khớp |
| C gpgsign |10 dòng/11 lần;8;1;0 |Đếm lại bốn tệp cho đúng 10/11, 8/8, 1/1, 0/0 | Khớp |
| C tự kiểm |≥11 nhóm |7 nhóm A1/A1b/A2/A3/A4/A5/A5b + 3 A5c + 1 nhóm 3 ca biên=11 | Khớp cách gộp;A5 đòi2 mutant riêng nên ≥11 mutant là cận tối thiểu, không phải đúng11 |
| C retry / trạng thái |1 lần lại;3 nhãn;tổng 10 |Ca mẫu đòi 2 lần gọi;3 số hạng tổng len(DOT_BIEN) | Hợp đồng đo được;chưa có implementation |
| C44 lượt, 0 tái hiện;80 lượt48đỏ;PID488/19999/20000;Git2.43/2.55 |lời đo trongC:250,265–272 |12+12+10+10=44;không log 44 lượt,không rig tái tạo;con số 80 đã được rút | Chỉ xác thực phép cộng;không tái sử dụng số đỏ đã rút |
| C nguồnErrno39 /0 dòng lịch sử |quét lúc06:0xZ |Lệnh quétkhông neo cây;HEAD nay có chính các spec nhắcErrno39 | Không gọi đây là phép đếm hiện hành;thiếu SHA của mẫu quét lịch sử |
| Khoản billing thực/2000 phút |hệ số×2;hạn mứcFree |Chú thích ci.yml ghi số 13-08;G:432–434 thừa nhận chưa kiểm hoá đơn | Các% là so với mẫu số giả định 2000,không xác nhận quota/hoá đơn hiện tại |

## KIỂM TỪNG TIÊU CHÍ — khả năng ĐỎ

Kiểm **29 heading A** và tách các nhánh quan trọng. “Đỏ được” là khả năng của hợp đồng, không phải kết quả chạy test. Không ép tiêu chí **công bố** phải có ngưỡng hiệu năng, nhưng thiếu dữ liệu hoặc công bố sai phải có trạng thái thất bại rõ.

| tiêu chí | phép phân biệt / kết luận |
|---|---|
| G A1 | Max Windows > 36 làm đỏ. Có răng, nhưng gộp lại không tất yếu trả 40,63 ở cây mới; thiếu nền hiện tại vẫn mở. |
| G A2 | Bỏ bước/đổi if làm tập lệch; nhánh hạ vẫn bắt thiếu tên, mất so conclusion có khai. Cần cùng ngữ cảnh PR gồm nhãn; byte YAML không tự làm hai PR cùng matrix. |
| G A3 | Bộ ba job, tập if, prefix 9, on/concurrency và đa tập lint đều đỏ được. Mất nghĩa vụ chạy mutant shellcheck; không dùng parser làm mất khóa on. |
| G A4 | Thiếu timeout hoặc khác 60 ở bất kỳ một trong bốn job; timeout bước ⇒ đỏ. |
| G A5(1)(a) | Thiếu instance/kỳ vọng tự suy API ⇒ đỏ. **Chưa đủ**: phép trích bỏ if không delimiter; toán hạng bị bỏ không tới nhánh fail-close. |
| G A5(1)(b–f) | Rỗng; chưa cạn trang; trộn attempt; thiếu mốc; job không success đều bị bác. |
| G A5(2–3) | Bắt buộc hai lượt hợp lệ, công bố tổng và tỉ lệ. Đỏ được, nhưng đã đổi cách xử lý nền bị cắt mà không chứng minh điều kiện ấy biến mất. |
| G A6(a) | Tên công bố khác tên check thực ⇒ đỏ; không suy luôn context từ job_id khi YAML có name. |
| G A6(b) | Thiếu context/trường/quyền đọc ⇒ đỏ. Có phép đo mới thật; **mất mốc trước merge**. Cấm require Windows cho PR thường phù hợp matrix hiện có. |
| G A7 | Quay consumer về gate làm ca 2 đỏ; ca 3/4 chặn thiếu Ruff/sai thứ tự; hai mutant pin/probe cũ vẫn bắt buộc. |
| G A8 | Đường thứ ba hoặc additions > 300 ⇒ dừng. |
| G A9 | Có holder khác; thiếu ref/CHAN[12]; dependency chưa land ⇒ đỏ. Không dùng rc=0 của check thay đo overlap. |
| T A1(a) | Tỉ lệ Ubuntu ≈ 1 ⇒ đỏ; thiếu mẫu số ⇒ đỏ. **Hết nhánh miễn đo cũ**; chưa có hiện vật Ubuntu được dẫn. |
| T A1(b) | Success ⇒ ĐẠT, cancelled ⇒ có điều kiện. **Không có phép làm đỏ vì vẫn giữ t125 trên Windows** nếu job hoàn tất; failure/timed_out/missing chưa được ánh xạ. P1 về vế bỏ tải Windows, không gán cả A1 hằng-đúng. |
| T A2(1) | Thiếu gate-t125 trong khi gate bỏ ⇒ phải có cổng đỏ. Pending required check không được tự gọi là một test đã đỏ. |
| T A2(2) | Job hiện hữu nhưng không chạy t125 ⇒ cổng đỏ; không chỉ đếm job. |
| T A2c(1) | Bỏ một subprocess ⇒ đỏ. |
| T A2c(2) | Actor không tới đúng lượt con/đổi biến phân biệt ⇒ đỏ. |
| T A2c(3) | Hai tuple lệch và no-op phép so ⇒ ca âm đỏ; ca tích hợp dùng cùng hàm. Đã bổ sung phép đổi màu cần thiết. |
| T A3 | Cờ mới hạch toán ĐẠT thay BỎ QUA ⇒ đỏ. Cờ cũ là đối chứng hạch toán, không thay A2c; đo mẫu số theo HEAD. |
| T A4 | Sai tên/bộ ba/hiệu lực lượng ⇒ đỏ; một tên × hai nền = hai phần tử. Nhánh hạ bắt thiếu tên/cancelled/skipped không giải thích. |
| T A5 | Thiếu timeout/chèn if job/khác matrix ⇒ đỏ. Bộ ba không đo needs, không tự chứng minh song song. |
| T A6(a) | Tên check thực khác tên công bố ⇒ đỏ. Quy ước job_id+nền chỉ đúng cấu hình hiện có không custom name. |
| T A6(b) | Thiếu một trong hai context/thiếu trường ⇒ đỏ. Phép trạng thái có thật; thiếu mốc trước merge. |
| T A7 | Sai write set/trần additions ⇒ dừng. |
| T A8 | Tập ca thực chạy gộp lại thiếu/thừa ⇒ đỏ; không tin tổng suông. 147 ca hiện hành khác 146 ở benchmark. |
| C A1 | Ngoại lệ hạ tầng ngoài đích; đổi phân loại sang AssertionError ⇒ sai nhãn ⇒ đỏ. |
| C A1b | Ép assert 80 và 198 độc lập; đổi thành chot ⇒ đỏ. |
| C A2 | Chốt thật ở ca ngoài đích; chỉ so lớp bỏ tên ⇒ đỏ. |
| C A3 | Gộp nhãn KHÔNG ĐO ĐƯỢC ⇒ đỏ dù tổng vẫn 10. |
| C A4 | Hai lần không đo được; tháo trần ⇒ số gọi khác 2/không kết thúc ⇒ đỏ. |
| C A5 | Hai repo phải tắt ký; gỡ ghim từng repo ⇒ đỏ; chạy trọn vòng mutant trong rig ký là nghĩa vụ riêng. |
| C A5b | Stdout không là kênh tin; quay về đọc stdout ⇒ đỏ; trùng/thiếu/ca lạ ⇒ KHÔNG ĐO ĐƯỢC, qua subprocess thật. |
| C A5c(1) | Với dấu khác là biến duy nhất, gỡ phép so đổi màu được. **Không thử sinh dấu mới**: dấu tái dùng vẫn qua test trên dữ liệu dựng sẵn. |
| C A5c(2) | Thiếu đóng lượt; gỡ chốt đóng ⇒ ca đỏ. |
| C A5c(3) | Kiểm bản ghi mang T3 thay T1 có thể đỏ; không chỉ kiểm verdict cuối vì hai vế có thể cùng bị bác do trùng. Chỉ đo cơ chế đóng dấu, không xác thực nguồn. |
| C A6 | Thiếu một ca mutant đổi màu ⇒ không được tính ≥ 11. Không tính ca 1 chỉ xanh trên hai vế. |
| C A7 | Tám ca/mười mutant; tụt giết ⇒ đỏ. |
| C A8 | Đường ngoài tệp test/additions > 300 ⇒ dừng. |

Hai bảng context tương đương khi hiểu “thêm” là cộng dồn: `{gate}`, `{gate,gate-t125}`, `{gate,gate-t125,gate-registry,gate-packet-loop}` trên Ubuntu. Chúng không phải hai nguồn literal độc lập cùng đúng nghĩa “DUY NHẤT”; nên chọn một nguồn và một bản chiếu có phép so, nhưng hiện chưa có lệch tập để báo một finding chức năng riêng. DAG metadata: `503→T125→GATE`, `502→GATE`, CHAM độc lập. Không có overlap chưa khai trong ba write set.

### dau-phien-mat-nghia-vu-sinh-moi  [P1]  Mất thuộc tính chống phát lại trong chính lần viết lại

TỆP/DÒNG: C3:150; C:135,203–210,231–232.

VẤN ĐỀ: Bản cũ đòi dấu phiên **ngẫu nhiên sinh mới mỗi lượt**. Bản mới chỉ đòi mang và so dấu. Ca mới làm đúng việc đo phép so một dấu khác, nhưng không kiểm bộ sinh. Mô hình triển khai tái dùng dấu qua hai lần chạy cùng mutant/lần thử/rc sẽ nhận lại bản ghi cũ; vẫn bác dấu khác do fixture dựng và vẫn qua ca “bỏ so dấu”. Lỗi này nằm ngay trong phạm vi chống phát lại ngẫu nhiên đã giữ, không cần mã sản phẩm đối kháng.

ĐÃ THỬ VÁ: Executor sửa đúng tính duy nhất của biến trong fixture nhưng xoá nghĩa vụ tại M7. Cần trả lại thuộc tính sinh mới mỗi lượt và ca kiểm hai lượt thật; không chỉ thêm chữ “nonce”. Test khoá: hai lần chạy cùng định danh nghiệp vụ phải có dấu khác, dùng dấu lần trước phải bị bác. Rủi ro vá: lấy timestamp độ phân giải thấp làm dấu có thể trùng khi chạy nhanh.

ĐÃ THỬ NGHIỆM: Đã tìm toàn bộ “dấu phiên/ngẫu nhiên/sinh mới” và đối chiếu C3/C. Phản chứng tái dùng dấu là review mô hình bằng lời, không tạo bản ghi hay mutant.

ĐỘ TIN: Cao về mất nghĩa vụ và thiếu phép kiểm sinh; chưa có implementation để đo xác suất trùng.

### a5-trich-delimiter-van-bo-sot-bieu-thuc  [P1]  Fail-close không cứu được toán hạng chưa được tìm thấy

TỆP/DÒNG: G:294–299; G:229–234; `cay-kho/.github/workflows/ci.yml`:245,278,319,421,521,541,561.

VẤN ĐỀ: “Trích toàn bộ” được cụ thể bằng quét `${{…}}`, trong khi chính A3 công nhận `if` không delimiter. Đọc cây thật thấy 7/10 if ở dạng đó. Phép trích còn thiếu phụ thuộc hàm trạng thái như always(), không chỉ đường dẫn context. Toán hạng trong một job-if trần không giải được có thể không được đưa vào danh sách cần giải, nên chốt “toán hạng không giải được⇒đỏ” không chạm nó. A3 có thể bắt một số thay đổi cùng PR nhưng không làm A5 tự đủ khi suy kỳ vọng cho từng lượt nền/attempt.

ĐÃ THỬ VÁ: Đã thêm ref/labels và neo SHA, tiến bộ thật. Cần parse theo vị trí biểu thức (matrix, job/step if kể cả dạng trần), phân biệt ngữ cảnh run, matrix/runner và trạng thái phụ thuộc; dạng không hỗ trợ phải đỏ. Ca khoá bằng lời: cùng toán hạng không biết, lần lượt đặt trong if có/không delimiter, cả hai phải KHÔNG ĐO ĐƯỢC. Rủi ro vá: quét chuỗi toàn YAML lại có thể nhận chữ trong run/comment là biểu thức; cần parser hiểu vị trí.

ĐÃ THỬ NGHIỆM: Đã parse YAML và liệt kê các if hiện hữu; không tạo biểu thức hay payload mới. Hướng phản chứng là review mô hình. Việc lấy workflow tại run.head_sha còn cần kiểm đúng SHA workflow đã thực thi cho từng event/attempt; không mặc định mọi PR dùng cùng cây với trường head_sha mà không có chứng cứ.

ĐỘ TIN: Cao về khoảng trống delimiter; chưa khẳng định hành vi runtime của bộ giải chưa viết.

### a1-ubuntu-khong-chung-minh-bo-tai-windows  [P1]  Thu hẹp nền đo làm mất phép phân biệt mục tiêu Windows

TỆP/DÒNG: T3:147,156–195; T:112,129–155,222–229,290–293.

VẤN ĐỀ: Ubuntu có ngưỡng và hết miễn đo, nhưng Windows chỉ còn xét job success/cancelled sau land. Hai triển khai — bỏ t125 trên cả hai nền, hoặc chỉ bỏ trên Ubuntu — có thể cùng đạt nếu lượt Windows của bản thứ hai vẫn hoàn tất. A1(b) không phân biệt chúng, dù M1 và điều cấm skip trên bất cứ nền nào vẫn áp hai nền. ĐẠT CÓ ĐIỀU KIỆN đã được tách chữ đúng, nhưng không khôi phục phép đo bỏ tải Windows; failure/timed_out/thiếu job còn không có nhánh quyết định. M1 cũ yêu cầu song song cũng mất, trong khi bộ ba A5 không kiểm needs.

ĐÃ THỬ VÁ: Executor chuyển vế bắt buộc sang Ubuntu và khai giới hạn ở chua_do_duoc #1. Đây là **thu hẹp có khai**, không phải đã sửa toàn bộ finding cũ. Cần phép chứng minh độc lập với thời lượng rằng gate Windows không còn thực hiện t125, job riêng vẫn thực hiện nó, và không có dependency nối chúng thành chuỗi. Ca khoá: giữ t125 chỉ trên Windows phải làm đỏ. Rủi ro vá: kiểm sự có mặt cờ vẫn mù nếu parser cờ khác hành vi; cần bằng chứng thực thi tương ứng mỗi nền.

ĐÃ THỬ NGHIỆM: Review mô hình từng nhánh A1/A5; không chạy Windows và không dựng mutant. Không gọi toàn A1 hằng-đúng: chỉ vế bảo đảm bỏ tải Windows mất khả năng đỏ theo lỗi đang xét.

ĐỘ TIN: Cao về khoảng trống hợp đồng; không dự báo xác suất Windows hoàn tất sau #492.

### mat-moc-require-truoc-merge  [P1]  Đo trạng thái sau đó không bảo vệ lần merge đầu tiên

TỆP/DÒNG: G3:884–887; T3:250–254; G:342–373; T:231–265.

VẤN ĐỀ: Hai bản cũ bắt cập nhật require TRƯỚC merge. Bản mới thêm endpoint và tập context, nhưng bỏ mốc này; bảng chỉ ghi pha sau land. Mô hình merge khi mới require gate, sau đó thêm context và đọc API, sẽ đạt phép kiểm mới tại thời điểm cuối nhưng lần merge đã không được job mới chặn. Đó là nghĩa vụ thời gian, không được thay bằng phép so tập cuối cùng.

Hai luật tên: dùng context và không require Windows cho PR thường là đúng hướng với YAML hiện hữu. Nhưng “gate trần không khớp check nào ⇒ cổng trang trí” ở G:357–359/T:246–248 không theo ngay ngữ nghĩa required: check bắt buộc không được báo cáo phải làm chờ/chặn, giống lý do cấm context Windows. Không coi đây là đo thực trạng GitHub; gói thiếu snapshot. Context cũng không luôn bằng job_id+nền nếu job có name riêng.

ĐÃ THỬ VÁ: Phép đọc rules/branches và thiếu trường ⇒ đỏ sửa thật phần hằng-đúng cũ. Cần khôi phục mốc trước merge, lưu readback context và kết quả check exact head dùng cho lần merge, rồi có readback sau land nếu cần. Test khoá: chuỗi cập nhật chỉ sau merge phải không được chấp nhận. Rủi ro vá: require tên chưa từng sinh trên PR có thể khoá đường merge; sinh/check tên PR trước khi chuyển require, không bỏ nghĩa vụ để tránh pending.

ĐÃ THỬ NGHIỆM: Đã đối chiếu dòng bị xoá và bảng pha; phản chứng trình tự là review mô hình, không gọi API và không đổi ruleset. Endpoint có đường đọc trong hợp đồng, nhưng lời HTTP 200/enforcement hiện tại chưa kiểm được offline.

ĐỘ TIN: Cao về mất mốc thời gian; hiện trạng máy chủ chưa xác minh.

### uoc-moi-bo-mat-phan-duoi-bi-cat  [P2]  Phép trừ mới bỏ cả tải chưa kịp chạy

TỆP/DÒNG: T3:61–83,295–304; T:51,56–74; G:75–77.

VẤN ĐỀ: 60,52 là job bị cắt ngay bước 20; 26,25 là thời lượng **đã chạy** của bước bị cắt. Công thức 60,52−26,25+26,25/2,9312 không chỉ giả định bội số bằng nhau: nó còn giả định bước 20 thật bằng cận dưới và chi phí phần đuôi chưa chạy bằng 0. Cả hai giới hạn cũ biến mất. Dải 18 success trước #492 không là đối chiếu độc lập cho job đầy đủ sau #492. T:72 còn kết luận “đủ để đưa job về dải đã đo”, ngược T:63–64; T:22 gọi bội số đúng trên mọi nền, ngược T:290–293.

ĐÃ THỬ VÁ: Cận 3,74–8,68 và max mẫu làm cận trên đã bị gỡ. Cần mô hình tổng gồm prefix, thời lượng hoàn tất bước 20 và suffix; chưa đo số hạng nào thì để mở, không dùng cancelled làm giá trị đầy đủ. Ca khoá: thêm một suffix thời lượng dương vào cùng dữ liệu bị cắt phải tăng ước; tăng thời lượng thật bước 20 trong phần chưa quan sát cũng phải đổi kết luận. Rủi ro vá: lại mượn hệ số bước khác làm cận trên.

ĐÃ THỬ NGHIỆM: Decimal tính 8,9553766376 và 43,2253766376: không lỗi số học. Review mô hình: chỉ cần suffix giả định 5 phút, tổng là 48,2253766376 chứ không 43,23, ngay cả khi giữ nguyên mọi giả định thuận lợi khác; không chạy CI.

ĐỘ TIN: Cao; đây là bỏ số hạng, không phải sai số làm tròn.

### billing-tam-luot-dung-tong-sau-luot  [P2]  723,96 phút được gán sai mẫu số

TỆP/DÒNG: G:48,171–175; T:45,120–124; E bảng CI.

VẤN ĐỀ: Bảng có tám cancelled. Tổng 482,55 phút × 2 = 965,10, không phải 723,96. Số 723,96 khớp đúng **sáu** cancelled mới nhất từ 10-09T04:55. Gán nó cho 8 lần lặp lại bệnh ghép sai tập. Đây là số đang làm căn cứ ngân sách CI, không chỉ số minh hoạ. “Thu 0 thông tin” cũng không được chứng minh: ngay các bước bị cắt đang được dùng làm cận và chẩn đoán trong đặc tả.

ĐÃ THỬ VÁ: Executor bổ sung bảng 29 lượt và phân mẫu 18/8/2 nhưng chưa tính tổng trên cùng tập. Cần chọn rõ 8 hoặc 6, ghi run_id và thuật toán cộng, sửa đồng bộ G/T/E; gọi chính xác “không có kết quả hoàn tất hợp lệ”, không gọi 0 thông tin. Rủi ro vá: dùng 6 để giữ số nhỏ mà vẫn kể 8; hoặc khai ước ×2 là hoá đơn thực.

ĐÃ THỬ NGHIỆM: Đã parse và cộng Decimal. Sáu ID: 34576916278,34568864158,34563553711,34552510232,34549206309,34439063235; thêm 34033930149 và 34023635399 thành 8. 965,10/2000=48,255%;723,96/2000=36,198%. Không xác minh quota hiện tại.

ĐỘ TIN: Cao, phản chứng số học trực tiếp từ hiện vật bàn giao.

### nen-cu-khong-bac-duoc-no-nen-hien-tai  [P2]  Có nền lịch sử không bảo đảm nền đúng tải mới

TỆP/DÒNG: G3:857–860,999–1004,1043–1046; G:75–81,196–199,222–227,329–330; T:146–151.

VẤN ĐỀ: 18 success bác đúng mệnh đề “chưa hoàn tất lần nào” và lượt 34429604548 là nền lịch sử có thật. Nhưng sau #492, sáu mẫu đã kết thúc trong hiện vật đều cancelled. G A5 yêu cầu **sinh lại** nền tại start_from_sha sau T125, trong khi chính T cho phép land/ĐẠT CÓ ĐIỀU KIỆN khi Windows vẫn cancelled. Vì thế nợ “nền hiện tại có thể không đo được” chưa bị bác. G A2 vẫn dự phòng nền bị cắt, G A5 mới lại xoá đường xử lý ấy; fail-close là chặt hơn nhưng không phải bằng chứng vòng đã hết. Mutant gộp job trên cây mới cũng không tự trở về 40,63 của cây cũ.

ĐÃ THỬ VÁ: Đã thay dữ liệu phổ quát sai bằng mẫu định danh. Cần tách nền lịch sử khỏi nền nghiệm thu; giữ trạng thái chưa đo được hiện tại, nêu dừng/revision nếu nền mới không hợp lệ và giải quyết quan hệ với T đạt có điều kiện. Không nhất thiết trả lại ngoại lệ cho A5 pass; phải khai rõ thay đổi chuẩn. Giữ làm mới chứng cứ khi head/đầu vào đo đổi theo protocol. Rủi ro vá: dùng lượt cũ có cùng ci.yml nhưng khác tải làm nền mới.

ĐÃ THỬ NGHIỆM: Đã phân nhóm hàng trước/sau #492; đã đọc cả hai nhánh T:A1(b) và G:A2/A5. Phản chứng mô hình: T land nhưng Windows vẫn cancelled là tình huống chính T cho phép; G không có mẫu hợp lệ mới từ đó. Không chạy nền tương lai.

ĐỘ TIN: Cao về suy luận sai từ tồn tại lịch sử sang khả năng hiện tại.

### mat-phan-chung-va-no-phan-ra  [P2]  Rút gọn bỏ ca canh bộ đo và nợ chưa được giải quyết

TỆP/DÒNG: G3:770–774,994,1016–1021,636–637; G:146–148,246–255,419–438.

VẤN ĐỀ: Chốt đa tập actionlint còn nguyên, nhưng **phản chứng bắt buộc** thêm lỗi shellcheck trên nền rc=1 bị xoá; một đoạn kể phép tính tập không thay lần chạy ca đó. Ngoài ra mất trạng thái #456 ĐÓNG MỘT PHẦN về phân rã theo bộ Windows và điều kiện mở việc song song sau phân rã; nợ tăng theo số biên nhận bị rút thành riêng phần #492 mà không có phép đo bác phần còn lại.

ĐÃ THỬ VÁ: Bản mới giữ phần lớn acceptance và một số nợ có tên, nhưng nhóm bị mất không có lý do đóng. Cần đưa ca bắt buộc trở lại A3; giữ/chuyển nợ phân rã và tăng trưởng với chủ thể/điều kiện đóng rõ. Test khoá bằng lời: bộ so lint quay về chỉ so rc phải bị ca thật bác dù cả hai lần rc=1. Rủi ro vá: trả lại cả bảng lịch sử thay vì chỉ nghĩa vụ/nợ, tái sinh kiến trúc cũ.

ĐÃ THỬ NGHIỆM: Đã đối chiếu đoạn bị xoá với toàn A3/chua_do_duoc mới. Review mô hình ca lint; không tạo shell lỗi và không chạy actionlint.

ĐỘ TIN: Cao về mất nghĩa vụ ca; cao về chưa có chứng cứ đóng nợ, không khẳng định số proxy cũ còn đúng.

### hien-vat-khong-chua-so-dang-duoc-vien-dan  [P2]  Mẫu số bắt buộc Ubuntu chưa có trong hiện vật được dẫn

TỆP/DÒNG: T:35–45,134–142; G:39–48,55,71; C:59–60,250,265–272; E các bảng CI/ruleset.

VẤN ĐỀ: Hiện vật do-nen-windows chỉ có job Windows và bước 20 Windows. Nó không chứa 5 mẫu Ubuntu 2,32–2,42 làm căn cứ A1(a), không chứa Ubuntu 1,22/2,35 của N6/N7, không chứa registry/packet-loop của G3. G3 vừa gọi ĐO ĐƯỢC, có hiện vật trong G, vừa là THUẬT LẠI T:N13. Ruleset 20856202/active/HTTP 200/403 cũng chỉ được kể, không có response. Những số khác như 44 lượt không tái hiện CHAM, timing 400/270, dãy G10 không có lệnh/rig/mẫu đủ để tái tạo **đúng lời khai**. Một lệnh API tổng quát hoặc chạy benchmark mới không khôi phục số đo cũ.

ĐÃ THỬ VÁ: Gói mới có bảng Windows và benchmark, cải thiện thật. Cần thêm snapshot có run_id/attempt/timestamp và cột Ubuntu, response rules/checks, log/rig tương ứng; hoặc phân loại đúng THUẬT LẠI/CHƯA XÁC MINH và không dùng làm nền đã sẵn có. Chỗ số không còn cần cho hợp đồng có thể bỏ có khai. Test khoá: truy từng ô về hàng/mốc nguồn, không chỉ kiểm phép chia. Rủi ro vá: ghép cột Ubuntu ở lượt khác để lấp bảng.

ĐÃ THỬ NGHIỆM: Đã đọc toàn bộ ba hiện vật, kiểm danh sách tệp, so với từng ô dẫn; xác nhận không có raw JSON/log hai vế riêng. Riêng tổng kết 146/146 có trong benchmark.txt, nên không kết luận N5 hoàn toàn không chứng cứ. Không mạng theo phạm vi người dùng.

ĐỘ TIN: Cao về thiếu chứng cứ trong gói; không kết luận các số ngoài máy chủ là bịa.

### thu-hep-cham-khong-phai-va-kenh  [P2]  Rút mô hình đối kháng phải giữ finding ở trạng thái phạm vi đã đổi

TỆP/DÒNG: C3:225–238; C:62–80,129,214–224,278–285.

VẤN ĐỀ: A5c(3) cũ đòi bác mã sản phẩm ghi trực tiếp kênh. A5c(3) mới chỉ đo lời gọi đi qua emitter hợp tác, và đưa việc sửa khung ra ngoài phạm vi. Đây là **thu hẹp được khai**, phù hợp việc Python scope không phải miền quyền; nhưng không đóng đường finding cũ. C:79 còn nói hai chốt “giết cả lớp giả mạo ngẫu nhiên”: phân biệt theo ý định tác giả không chứng minh mọi lỗi vô ý đều không thể sửa/hỏng trạng thái khung. M1/A1 còn dùng tên “không giả mạo được” phải được đọc trong một mô hình lỗi cụ thể, không coi nonce là xác thực nguồn.

ĐÃ THỬ VÁ: Executor rút đúng lời khai quyền ghi giả và ghi chua_do_duoc #4/#5. Cần giữ nợ/phạm vi bị loại như thay đổi cần quyết định của chủ kho, không đánh finding ĐÃ VÁ THẬT; định nghĩa những lỗi ngẫu nhiên cụ thể được bảo vệ và ca tương ứng. Nếu vẫn giữ nghĩa vụ cũ, phải thiết kế ranh giới tin cậy thật. Rủi ro vá: chỉ thêm một subprocess nhưng vẫn để test và sản phẩm cùng tiến trình con/kênh có quyền ghi chung, rồi khai đã cô lập.

ĐÃ THỬ NGHIỆM: Đã đọc import tại ops/nhanh_don_duoc_test.py:78–84 và đối chiếu phạm vi cũ/mới. Chỉ review mô hình; không khai thác hay dựng payload. Các ca A1/A5b/A5c trong phạm vi hẹp **vẫn có nghĩa**, không báo chúng đồng loạt rỗng nghĩa.

ĐỘ TIN: Cao về rescope, không đánh giá một kiến trúc cô lập chưa được giao thi công.

### bang-gom-van-khong-phu-hop-dong  [P3]  Bảng bằng chứng vẫn bỏ các số kiểm được ngoài bảng trung tâm

TỆP/DÒNG: E đoạn “Bảng này CỐ Ý chưa đầy đủ”; G:88–98,171–174; T:181–185,267–274; C:94,118–120,226–241,275–277.

VẤN ĐỀ: E vẫn không kiểm inventory trọn hợp đồng: số bước/instance theo pha, write set,≥11 nhóm, 14+2 assert, gpgsign hai đơn vị, N=2, ước additions, mẫu số ca theo SHA. Ví dụ cụ thể đã đo: reviewed HEAD có 147 ca, còn benchmark ở 0236ca7 có 146. Điều khoản “mẫu số lúc thi công” cứu acceptance, nhưng bảng đang dùng trí nhớ không tự thấy độ trôi này.

ĐÃ THỬ VÁ: Executor thêm G/N timing/ruleset, chưa thay cơ chế gom. Cần bảng phủ từng khẳng định định lượng với nguồn/đơn vị/SHA/trạng thái, cập nhật từ dữ liệu; bảng đo trong verdict này là danh sách các mục bổ sung. Ca khoá: một số mới trong acceptance không có hàng evidence phải bị báo thiếu. Rủi ro vá: regex chỉ nhận chữ số Arabic bỏ “hai/bốn” hoặc nhầm số Issue với số đếm.

ĐÃ THỬ NGHIỆM: Đã đọc AST/YAML, tính số học và đối chiếu E; bảng đo phía trên ghi cả khớp/lệch/không đo được. Không nhân thêm finding cho cùng lỗi số học đã đếm riêng.

ĐỘ TIN: Cao.

## ĐIỀU KIỆN CÒN CHẶN

Cần xử lý bốn P1: sinh mới dấu phiên và thử qua hai lượt; trích đủ biểu thức để fail-close; chứng minh bỏ tải trên Windows và quan hệ lịch chạy; khôi phục require trước merge. Sáu P2 cần sửa phép ước thiếu phần đuôi, số billing sai tập, kết luận về nền, nghĩa vụ/phản chứng bị mất, provenance số đo và cách hạch toán rescope CHAM. P3 yêu cầu bảng evidence phủ các số còn hiệu lực.

Không có `approve` trong lượt này. `0 P1 + 0 P2` ở một vòng sau cũng không tự đóng packet sensitive: vẫn cần reviewer approve tường minh trên exact head. Việc chuyển Windows thành công bố hoặc đưa mã đối kháng ra ngoài CHAM phải được giữ tên là **thu hẹp phạm vi**, không ghi là đã sửa hành vi cũ.
