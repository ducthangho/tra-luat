verdict: changes_requested
reviewed_sha: 0236ca705aebc46a82428d7b23ccd1b0a2cdb647

Reviewer: Codex, OpenAI; bề mặt API, transport machine, shell cục bộ; khác nền với executor Claude. Tree: `4bb6d2cfe506331de14ade7bc3872e666c538fc8`. Chỉ đọc/ghi trong thư mục được giao, không mạng, không sửa `cay-kho/`, không dựng payload hay đường thoát cây. Chỉ xuất tệp này; không soạn cây vá thay executor.

Quy ước dòng: **G** = `cay/ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md`; **T** = `cay/ops/specs/T125-RA-JOB-RIENG.md`; **C** = `cay/ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md`; **E** = `EVIDENCE.md`. Dòng của đúng các blob tại SHA trên. Các kết luận về khả năng đỏ là review hợp đồng, không phải lời khai đã chạy implementation tương lai. Finding mở: **6 P1 · 4 P2 · 1 P3**.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đọc 12 finding dưới các heading của `VERDICT-LUOT-2.md` trước khi rà tiêu chí và đo số. Không lấy 13 hàng đối chiếu lượt 1 trong verdict ấy làm danh sách lượt 2. Giữ nguyên đủ 12 slug. Kết quả: **3 ĐÃ VÁ THẬT · 8 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 0 CHƯA VÁ**.

| slug lượt 2 | phân loại | bằng chứng lượt 3 |
|---|---|---|
| `doi-ca-assert-ha-tang-thanh-tin-hieu-chot` | **ĐÃ VÁ THẬT** | C:103,144,293–296 thống nhất 14 assert thuộc ca, giữ hai assert hạ tầng; dự toán đổi sang ≥11 nhóm tự kiểm. AST xác nhận 14/16 và vị trí 80/198. Những lần nhắc 16 còn lại giải thích lịch sử, không còn là lệnh đổi 16. |
| `lop-ngoai-le-chua-bao-ve-duong-truyen-ket-qua` | **VÁ HỜ** | M7 C:150 và A5c C:225–238 thêm neo lượt/rc/nonce/đóng lượt. Nhưng C:235–238 vẫn dùng quyền giữ handle trong cùng tiến trình làm ranh giới tin cậy; chưa chặn mã được import can thiệp khung phát. Ca 1 còn không đổi màu theo đột biến được chỉ định: bản ghi của mutant trước vẫn bị phép so mutant bác khi bỏ so nonce. |
| `them-t125-nhung-giu-hop-dong-ba-job` | **VÁ HỜ** | T:149,253–273 và G:785–787,875–880 sửa đúng pha 1→2→4. G:729 vẫn đòi chứng minh ba job trên PR; G:882 nói mỗi lần thêm một job, trái chính hai job thêm lần hai. G:683 còn ba runner. Hạ lỗi còn lại xuống P2: các chốt cứng A4/A6 đã phủ bốn tên. |
| `a5-hop-le-chua-doi-du-job-va-du-luot` | **VÁ HỜ** | G:825–839 đã lấy kỳ vọng từ YAML riêng mỗi vế, phân biệt job cấu trúc/instance/API. Nhưng bộ ngữ cảnh chỉ ghi event_name và inputs, trong khi YAML thật còn dùng github.ref và nhãn PR. Chưa neo ref workflow vào SHA bất biến của attempt. Vì vậy chưa đủ dữ liệu dẫn xuất một tập kỳ vọng duy nhất. |
| `metadata-va-loi-thoat-composite-chua-theo-write-set-r5` | **VÁ HỜ** | A8 G:905 về hai đường; A9 G:922–926 sửa #502 và điều kiện T125 land. Metadata G:38 vẫn chỉ `[wp502]`, không có cạnh T125. Composite được gọi là dùng lại được ở G:558–563, nhưng G:591 cấm đường khác và A8 vẫn đòi đúng hai đường. C:130 còn giao t125 cho #463 r5. |
| `so-ci-moi-chua-duoc-khai-la-thuat-lai-trong-spec` | **VÁ HỜ** | T:93–100 bỏ ghép “mọi số cùng run”; G:215–218 thu hẹp mệnh đề phổ quát. Nhưng G:219 vẫn nói bốn lượt cancelled đúng trần, bảng chỉ hai run; G:690 lại khai chưa hoàn tất lần nào; G:1001 tiếp tục bốn lượt chạm trần. Hai run bổ sung vẫn không định danh và conclusion mức run không xác nhận job timeout. |
| `benchmark-moi-thieu-hien-vat-neo-luot` | **ĐÃ VÁ THẬT** | T:29,39–44 loại rõ hàng timing 2/3/4 khỏi nhóm đọc mã; G:1006–1014 giữ khai không hiện vật; E không còn xếp N7–N9 vào nhóm đọc mã. Đây là sửa phân loại chứng cứ, không phải đã xác thực timing. Cận ≥7,8 còn ở hàng lịch sử G:974 được G:1011–1012 bác rõ, không dùng làm cận hiện hành. |
| `lan-thu-ba-khong-cung-hinh-dang-tin-dung-gia` | **ĐÃ VÁ THẬT** | C:263–276 và C:299–307 cùng chốt cấp thừa 2/cấp thiếu 1, không kích hoạt §12. Không còn đoạn cuối dùng số 3 để đòi thay đổi thẩm quyền. |
| `t125-do-buoc-khong-go-duoc-vong-nen-bi-cat` | **VÁ SINH LỖI MỚI** | T:169–177 cho thiếu mẫu số trước land không làm packet đỏ. Đúng tình huống này, đột biến giữ t125 trong gate tại T:189–191 cũng không có mẫu số và không thể làm phép tỉ lệ đỏ. Sau land vẫn timeout vẫn được ĐẠT ở T:182–185. Vòng cũ được thay bằng cổng trước land không phân biệt bản đúng với bản giữ tải cũ. |
| `uoc-bien-t125-sai-so-hang-va-sai-chieu-can` | **VÁ HỜ** | T:61–83 sửa chiều cận và phép cộng có điều kiện; T:309 lại giữ biên 3,74–8,68 không gắn nhãn lịch sử. T:77 gọi max mẫu 2,89 là “cận trên thật”; nó không chặn hệ số bước 21–41 ở lượt mới. E M5–M7 ghi số hạng đã làm tròn nhưng kết quả dùng số chưa làm tròn. |
| `t125-doi-chung-co-cu-chua-chung-minh-than-ca-do` | **VÁ HỜ** | A2c T:208–217 đã canh hai subprocess và actor tới con, bắt được return sớm/thiếu lượt/đổi biến vô can. Nhưng phần “phép so verdict còn tác dụng” chưa có ca hai verdict khác nhau và đột biến vô hiệu phép so; hai lượt đều sạch cho kết quả giống nhau dù phép so không còn. |
| `bang-gom-bo-sot-cac-khang-dinh-kiem-duoc` | **VÁ HỜ** | E thêm M1–M7 và bảng pha nhưng vẫn không kê số nhóm ca A6, write set/composite, ngữ cảnh thật của matrix và số học cận cũ ở cuối T. Bảng dưới bổ sung các mục ấy, tách phần đo được và phần chỉ thuật lại. |

## BẢNG ĐO

Đã chạy Python đọc AST/CSV, tính số học và băm; Git chỉ dùng lệnh đọc. Cấu hình Git hệ thống bị vô hiệu, cấu hình global trỏ một tên không tồn tại trong cwd, `GIT_OPTIONAL_LOCKS=0`; không sửa config kho. Không chạy `tinh.py` của hiện vật vì nó ghi lại TSV trong `cay-kho/`. Không chạy benchmark hay bộ test có tạo kho tạm. Các phép đo dưới rc=0; một lần `cat cay-kho/.git` báo đó là thư mục, không phải phép xác minh thành công.

| mục | khai | đo lại / điều kiện | kết quả |
|---|---|---|---|
| SHA / tree | 0236ca7 | `0236ca705aebc46a82428d7b23ccd1b0a2cdb647` / `4bb6d2cfe506331de14ade7bc3872e666c538fc8` | Khớp |
| merge-base / master cục bộ | nền của diff | `26e2555d36c48b3c0f625ae50ab2cfb62b6cb858` / `0bf0ba7e926cdd3e189c7ae89cba5894becd3ecd` | Đã đo; không xác nhận remote trực tiếp |
| numstat PR | 3 tệp, +1056/−… | C +307/−0; G +438/−30; T +311/−0 ⇒ **+1056/−30** | Khớp phần đã khai; bổ sung deletes |
| blob và số dòng | ba spec bàn giao | C 307; G 1056; T 311, khớp byte HEAD | Khớp |
| bản lượt 2 / delta | LUOT2 và patch hai SHA | Cả ba LUOT2 khớp blob c1bfabc; patch khớp `git diff c1bfabc HEAD -- ops/specs` | Khớp |
| băm verdict lượt 2 | `2e6e2770…` | `2e6e27707c3a2041fc45e2588ce8d5b302703eb9cfb1d61edef24222097bc938` | Khớp; không xác minh comment đính chính ngoài mạng |
| shallow / abbrev | false / 7 | Git trả false; .git/config ghi 7 | Khớp |
| E M1 | 14 assert T1…T8, toàn tệp16 | AST từng ca: **1+1+2+1+1+1+2+5=14**, toàn tệp16 | Khớp |
| E M2 | nap_tool80 / chay_dot_bien198 | AST đúng hai Assert ở 80/198; hàm tương ứng 78–84 và182–219 | Khớp |
| E M3 | packet-loop min1,88/max2,89/median2,37 | Đúng 11 run của bảng G:304–316, ghép Windows/Ubuntu cùng run và cùng bước; **1,8775510204 / 2,8938547486 / 2,3692946058** | Khớp sau làm tròn; max mẫu không phải cận trên tương lai |
| E M4 | 26,25/3,24=8,10 | **8,1018518519** | Khớp 2 chữ số |
| E M5 | 33,97+8,10+5,35×1,73=51,32735; biên8,67265 | Đúng biểu thức viết ra: **51,32550; 8,67450**. Dùng 26,25/3,24 thay 8,10: **51,32735185; 8,67264815** | Không khớp chính xác; thiếu quy ước giữ độ chính xác trung gian |
| E M6 | h2,35 ⇒54,64435; biên5,35565 | Với8,10: **54,64250; 5,35750**. Với thương đầy đủ: **54,64435185; 5,35564815** | Cùng lỗi M5 |
| E M7 | h2,89 ⇒57,53335; biên2,46665 | Với8,10: **57,53150; 2,46850**. Với thương đầy đủ: **57,53335185; 2,46664815** | Cùng lỗi M5; không phải chứng cứ job sẽ hoàn tất |
| pha master | 1 job gate | YAML HEAD/master/d28c4b1 đều chỉ `gate`,40 bước,timeout60,job-if=None | Khớp cây hiện có |
| pha T / pha G | 2 /4 job | Hợp đồng thêm1 rồi thêm2: **1+1=2; 2+2=4** | Khớp số học thiết kế; chưa có implementation để đo runtime |
| instance theo pha | không kê trong E | Dispatch hai nền ⇒ **2→4→8**; PR không nhãn windows thường một nền ⇒ **1→2→4** | Không được dùng số job cấu trúc thay số instance |
| đầu vào matrix | G A5 chỉ event_name,inputs | YAML còn dùng **github.ref**, **github.event.pull_request.labels.*.name**; không dùng inputs trong biểu thức hiện tại | Không đủ tiền đề |
| hash ci.yml | số lịch sử đối chiếu | HEAD/master/d28c4b1 đều `8dbc730f8a66a8dc86da9ff487108809b320ba35aa0bdb4bc773da99cd18a22b` | Khớp |
| C số ca/số mutant | 8 /10 | AST tám hàm T1…T8, DOT_BIEN10 mục; tệp233 dòng | Khớp |
| C số nhóm mới | ≥11 | A1,A1b,A2,A3,A4,A5,A5b =7; A5c ba ca =3; nhóm ba ca biên =1 ⇒ **11 nhóm** | Khớp cách gộp đã khai; nếu tách từng ca biên là13, không dùng13 để báo sai11 |
| C chữ gpgsign | packet_loop10 dòng11 lần; lease8; bien_nhan1; nhanh0 | Đếm lại **10/11; 8/8; 1/1; 0/0** | Khớp |
| T số ca |145+1=146 | Đếm decorator @ca trong lease_publish_test.py: **146** | Khớp hiện tại; chưa kiểm cờ mới |
| T hai lượt/return cờ cũ | hai subprocess/return vẫn đạt | Đọc dòng4015–4044: hai lời gọi luot; mỗi lời gọi subprocess cùng script+CO_AB, so tuple rc,n/m,tập đỏ,bỏ qua; CO_AB return sớm | Khớp luồng mã; không phải chạy A/B |
| write set từng packet | G2/T2/C1; trần≤3 và≤300 additions | G∩T={ci.yml}; C rời; hợp **4 đường**. Composite thêm1 ⇒G3, nhưng vượt write set/A8 hiện hành của G | Trần mỗi packet không áp vào hợp; lối composite chưa hợp đồng hóa |
| nghĩa vụ require | hai lần | LầnT giữ2 job; lầnG giữ4; số job mới từng lần **1 rồi2** | G:882 “mỗi lần một job mới” sai |
| biên cuối T |3,74–8,68 | Theo tiền đề đã sửa: **5,35564815–8,67264815** | Không khớp T:309 |
| các tỉ lệ timing |65,7%;2,24×;≥7,694915 |114,10/173,6=65,72580645%;54,6/24,4=2,237704918;22,7×60/177=7,694915254 | Chỉ khớp số học; không có hiện vật neo thời lượng |
| mẫu TSV | hiện vật lịch sử | job.tsv26 hàng; buoc.tsv1140 hàng | Đã đếm; không phải hiện vật các run345… |
| C số lượt thử |12+12+10+10=44;0 tái hiện | Tổng44; không có log44 lượt trong phép đo này | Chỉ xác thực phép cộng, không xác thực0 |
| số CI345… / benchmark | thuật lại, không hiện vật | Không truy cập mạng, không tái đo thời lượng cũ bằng lượt mới | KHÔNG ĐO ĐƯỢC |
| doctrine-scan/adr-song/doc-claims/release/golden | executor khai rc0;180=180 | Không chạy lại các gate; không có phép thực thi implementation của ba spec ở đây | NOT_RUN; không coi lời khai là bằng chứng runtime của reviewer |

M3 dùng đúng các run: `34048685345,34049592719,34052910676,34055467808,34058508426,34060879398,34062997697,34065779670,34068433781,34070122978,34074288203`. Phép lọc sơ bộ theo step-success thu thêm run `34048229370` có job cancelled, cho n12/median2,36037952; đã loại khỏi phép đối chiếu cuối. Không dùng mẫu12 ấy để kết luận bảng11 sai. Không lấy số lượt trước làm phép đo lượt này.

### Kiểm từng tiêu chí A — khả năng đỏ, không phải trạng thái test đã chạy

| tiêu chí | phép phân biệt / kết luận |
|---|---|
| C A1 | Ép AssertionError hạ tầng ngoài đích; đổi phân loại về AssertionError phải sai nhãn. Đỏ được. |
| C A1b | Ép từng assert80/198; đổi nó thành chốt phải bị bắt. Đỏ được về hợp đồng; cần đo đường hạ tầng của chính bộ chấm, không chỉ ca con. |
| C A2 | Chốt thật ngoài đích ⇒KHÔNG GIẾT; bỏ so tên làm sai. Đỏ được. |
| C A3 | Ba nhãn riêng và ba số hạng; gộp nhãn làm đỏ dù tổng giữ10. Đỏ được. |
| C A4 | Hai lịch sử thử khác nhau, số gọi=2; mất trần bị phát hiện. Đỏ được; chưa chạy đồ giả. |
| C A5 | Gỡ ghim ở từng repo; chạy cả vòng mutant trong môi trường ký. Đỏ được. Không dựng được môi trường là thiếu nghiệm thu, không được mượn miễn trừ T A1. |
| C A5b | stdout giả và ba biên trùng/thiếu/ca lạ; yêu cầu subprocess thật. Đỏ được trong phạm vi này; không xác thực người ghi kênh. |
| C A5c(1) | **Đột biến chỉ bỏ so nonce không làm ca này đỏ** khi bộ bản ghi giữ tên mutant trước: chốt tên mutant vẫn bác. Chưa chứng minh nonce được canh. |
| C A5c(2) | Thiếu đóng lượt ⇒KHÔNG ĐO ĐƯỢC; bỏ kiểm đóng cho bộ bản ghi còn lại hợp lệ có thể làm ca đỏ. Chốt này có tác dụng riêng. |
| C A5c(3) | Có yêu cầu từ chối mã sản phẩm, nhưng cơ chế giữ/đóng handle không chứng minh quyền phát; việc “báo chủ kho” không phải nghiệm thu ca này. Xem finding P1. |
| C A6 | Đếm11 nhóm có mutant riêng. Đỏ được khi thiếu; A5c(1) chưa có mutant đổi màu hợp lệ nên không thể tự tính đủ bằng danh sách tên. |
| C A7 | Bất kỳ mutant rời nhóm giết, hoặc8/8 hụt, đều đỏ. Đỏ được. |
| C A8 | Một đường ngoài phạm vi hoặc additions>300. Đỏ được. |
| T A1(a) | Có nền hoàn tất thì tỉ lệ>0,45 làm đỏ. **Trong nhánh không nền được khai là tình trạng hiện tại, không có phép tỉ lệ làm đỏ trước land**; giữ tải cũ cũng được miễn. |
| T A1(b) | Không công bố lượt đầu là thiếu nghĩa vụ; nhưng success và timeout đều được chấp nhận, không kiểm hiệu quả tách bằng tỉ lệ. Không sửa được sự mù trước land. |
| T A2(1),(2) | Thiếu job / lệnh không gọi t125. Đỏ được nếu cổng bắt buộc thật sự được chạy; spec chưa phải bằng chứng gate ấy tồn tại. |
| T A2c(1),(2),(3) | Đếm tiến trình và kiểm actor tới con đỏ được bằng hai mutant chỉ định. Phần(3) không có ca verdict lệch để đo tác dụng phép so; bằng chứng hai lượt bằng nhau không phân biệt bỏ so. |
| T A3 | Return bị đếm đạt thay vì bỏ qua; đối chứng cờ cũ. Đỏ được, chỉ canh hạch toán. |
| T A4 | Mất/đổi tên bước đỏ được; nhưng tập thêm đúng một bộ ba không phủ hai nền, tên literal chưa khai. Nhánh hạ đòi0 cancelled song không giải thích skipped như G A2. Xem finding riêng. |
| T A5 | Thiếu timeout/chèn job-if/ma trận khác. Đỏ được. |
| T A6(a) | Tên in ra lệch YAML. Đỏ được. |
| T A6(b) | **Không có phép đọc trạng thái require**, theo đúng câu chữ. Issue có checklist nhưng chủ kho chưa thực hiện vẫn thỏa phần hiện vật. Không có cổng phân biệt hai trạng thái bảo vệ nhánh. |
| T A7 | Sai hai đường hoặc additions>300. Đỏ được. |
| T A8 | Tập ca thiếu/tăng ngoài hợp đồng, không chỉ tổng146. Đỏ được; 145+1 tự nó chưa chứng minh t125 có chạy A/B. |
| G A1 | Max job Windows>36 làm đỏ; ngưỡng tuyệt đối vẫn bắt buộc. “KẾT QUẢ ĐO” không miễn đỏ khi vượt36. |
| G A2 | Hai event, tập lệch làm đỏ; nhánh hạ tên có mất khả năng so conclusion được khai. Nhánh này không miễn G A5. |
| G A3(1),(2),(3) và actionlint | So cấu hình/tập if/tiền tố9/on/concurrency và đa tập chẩn đoán đều có đầu vào làm đỏ; vắng công cụ hoặc log cũng đỏ. Không được mượn T A1(a). |
| G A4 | Thiếu bất kỳ một trong bốn job/timeout hoặc đổi60/timeout bước. Đỏ được, đã sửa lỗi đếm chuỗi. |
| G A5(1)(a) | Kỳ vọng độc lập API bắt được thiếu instance; nhưng nguồn ngữ cảnh chưa đầy đủ. Xem finding giữ slug cũ. |
| G A5(1)(b–f),(2),(3) | Rỗng, thiếu trang, trộn attempt, thiếu mốc, job không success hoặc không công bố đủ hai tổng đều làm đỏ. Không có trần tiền không đồng nghĩa hằng-đúng. |
| G A6(a) | Tên in khác YAML làm đỏ. |
| G A6(b) | Cùng lỗ thiếu phép xác minh trạng thái như T A6(b), lần này bốn job. |
| G A7 | Bốn fixture qua consumer và hai ca ghim Ruff hiện hữu; quay về chỉ đọc jobs.gate làm fixture2 đỏ. Đỏ được. |
| G A8 | Đúng hai đường/≤300 additions. Đỏ được; chính nó bác lối composite đang được quảng bá. |
| G A9 | Có lease còn giữ write set làm đỏ; A9 hiện yêu cầu chờ cả #502 vàT125. Không đo lại trạng thái lease ngoài mạng ở lượt này. |
| G A10/A11 | **Đã thu hồi**, khối G:942–943 ghi rõ lịch sử; không đếm thành tiêu chí còn sống hoặc finding mới. |

Ngoại lệ T A1(a) không được mở rộng sang G A5: G:865 vẫn ghi bất kỳ điều kiện(1) hỏng ⇒ĐỎ. G:862–863 và G:1004 chỉ cho công bố số sau với nền thiếu, không có câu cho packet ĐẠT. C M3 cho thử lại một lần trước khi kết luận cũng không phải miễn nghiệm thu: lần hai vẫn không đo được ⇒suite đỏ. Ngược lại, T:182–185 cho packet ĐẠT dù job sau vẫn timeout mâu thuẫn với lời hứa tạo nền ở T:25 và G:589; G vẫn có thể bị chặn sau khi tiền nhiệm đã land.

### lop-ngoai-le-chua-bao-ve-duong-truyen-ket-qua  [P1]  Neo lượt không xác thực người phát, và ca nonce không đổi màu

TỆP/DÒNG: C:150,225–238; `cay-kho/ops/nhanh_don_duoc_test.py`:78–84.

VẤN ĐỀ: A5c(1) cấy bản ghi của mutant trước rồi yêu cầu chỉ bỏ so dấu phiên là ca đỏ. M7 còn bắt so tên mutant/lần thử/rc; bản ghi ấy vẫn bị từ chối vì mutant khác. Đó là ca xanh cả khi chốt nonce đã bị tháo. A5c(3) thừa nhận mã sản phẩm được import cùng tiến trình nhưng gọi việc chỉ hàm phát giữ handle là “quyền ghi”. Phạm vi biến Python không phải miền quyền độc lập. Đóng handle trước thân ca ngăn cả phát kết quả sau thân ca bằng handle đó; nếu mở/khôi phục đường phát, đặc tả không chứng minh mã sản phẩm không can thiệp được. Hướng vượt rào bằng lời: mã được import có thể tác động trạng thái/hàm phát của khung trong cùng interpreter, tạo kết quả trông như do khung phát cho đúng phiên. Nonce truyền vào cùng miền tin cậy chỉ canh phát lại, không chứng minh nguồn.

ĐÃ THỬ VÁ: Executor thêm M7 và ba ca A5c; chưa có ranh giới quyền thực thi được mô tả. Reviewer không soạn mã tấn công hay vá implementation.

ĐÃ THỬ NGHIỆM: Đọc luồng import trong kho và suy diễn từng chốt M7 khi bỏ riêng so nonce. Không thực thi mutant; nhận xét về quyền ghi là review mô hình, không khai đã khai thác runtime.

ĐỘ TIN: Cao với ca1 không đổi màu và thiếu ranh giới; chưa xác định chi phí một implementation cô lập hợp lệ trong trần300 dòng.

### them-t125-nhung-giu-hop-dong-ba-job  [P2]  Bảng pha đúng nhưng chưa phủ hết các chỉ thị nghiệm thu

TỆP/DÒNG: G:683,729,882; T:264–273; G:785–787,875–880.

VẤN ĐỀ: Bảng pha đã đúng và A4/A6 đã dùng bốn tên. A2 vẫn gọi phép đo PR là chứng minh ba job; mô tả require hai lần vẫn nói mỗi lần một job mới dù lần G thêm hai. Số ba runner ở A1 cũng không diễn tả pha bốn job/hai nền. Đây không phải các câu được khoanh lịch sử như A10/A11. Không báo các phép đo YAML ba job của ngày06-09 là lỗi chỉ vì chúng đo thiết kế cũ có ghi thời điểm.

ĐÃ THỬ VÁ: Executor thay con số tại các chốt chính nhưng không quét hết vùng nghiệm thu.

ĐÃ THỬ NGHIỆM: Rà toàn bộ ba spec bằng tìm chuỗi và đọc ngữ cảnh; đếm pha1+1+2. Không tạo workflow mới.

ĐỘ TIN: Cao; hạ P1 cũ xuống P2 vì hợp đồng bốn tên hiện đã rõ ở chốt cứng.

### a5-hop-le-chua-doi-du-job-va-du-luot  [P1]  Event và inputs chưa đủ để dựng tập kỳ vọng có thẩm quyền

TỆP/DÒNG: G:825–839; `cay-kho/.github/workflows/ci.yml` phần strategy.matrix.os.

VẤN ĐỀ: Chính biểu thức nền còn đọc ref và labels PR. Hai PR cùng event_name/inputs nhưng khác nhãn windows có tập instance khác; hai push khác ref cũng vậy. Chỉ ghi event/inputs không chọn được một kết quả duy nhất. “Ref của lượt” còn chưa chốt SHA workflow bất biến theo attempt; đọc lại tên nhánh sau commit khác có thể tạo kỳ vọng của cây khác. Nếu người đo chọn nhánh Ubuntu-only trong khi lượt thật cần Windows, thiếu Windows có thể khớp kỳ vọng sai. Lấy YAML thay API đã hết tự chứng minh trực tiếp, nhưng chưa hết tiền đề ngầm.

ĐÃ THỬ VÁ: Executor đã tách đúng hai vế và ba loại ID. Phần ngữ cảnh giải biểu thức chưa đủ.

ĐÃ THỬ NGHIỆM: Parse YAML tại HEAD, origin/master cục bộ và d28c4b1, đều cùng biểu thức dùng event/ref/labels. Đối chiếu các toán hạng với danh sách ngữ cảnh trong A5; không truy cập Actions.

ĐỘ TIN: Cao về thiếu ngữ cảnh; trung bình về lựa chọn sai cụ thể của implementation chưa được viết.

### metadata-va-loi-thoat-composite-chua-theo-write-set-r5  [P2]  Cạnh T125 và lối composite vẫn không nằm trong hợp đồng cấu trúc

TỆP/DÒNG: G:38–45,558–563,583–591,905–909,922–926; C:128–130.

VẤN ĐỀ: Metadata chỉ depends_on wp502, dù lời văn bắt T125 land trước; chưa có quy tắc cập nhật cạnh khi cấp packet_issue cho T125. Thêm composite đúng trần3 nhưng sai danh sách hai tệp và sai A8. C còn gán việc t125 cho #463 revision5. Ba write set hiện hữu không tự vi phạm ADR: G2/T2/C1, hợp4 và giao ci.yml là lý do nối tiếp, không phải lý do cộng cả ba packet vào cùng trần.

ĐÃ THỬ VÁ: Executor sửa #503→#502 và A8 ba→hai; chưa khép các bất nhất trên.

ĐÃ THỬ NGHIỆM: So bảng đường dẫn, metadata và các đoạn điều kiện cấp lease; tính2+1=3. Không đo ai đang giữ lease ở máy chủ.

ĐỘ TIN: Cao.

### so-ci-moi-chua-duoc-khai-la-thuat-lai-trong-spec  [P2]  Lời thu hẹp không thu hồi hết lời khai bốn lượt timeout

TỆP/DÒNG: G:215–225,690–695,999–1004.

VẤN ĐỀ: Có hai run được nêu cụ thể. Hai lượt còn lại chỉ được nói đã đọc conclusion mức run, không có run_id và không có chứng cứ nguyên nhân hủy job. Tuy vậy đoạn trên vẫn gọi bốn lượt cancelled đúng trần; đoạn nghiệm thu vẫn “chưa hoàn tất lần nào”. Lời thu hẹp ở215 không phải một điều khoản thu hồi mọi lần nhắc còn lại. Không thể suy timeout Windows từ run cancelled, càng không thể suy một mệnh đề phổ quát từ bốn mẫu.

ĐÃ THỬ VÁ: Executor sửa một đoạn phạm vi và phép ghép run ởT. Sót chính các kết luận đang dùng làm tiền đề.

ĐÃ THỬ NGHIỆM: Đếm các run_id trong bảng và đọc nơi phân biệt run/job. Không xác minh kết luận CI ngoài mạng; không kết luận các sự kiện ấy không xảy ra.

ĐỘ TIN: Cao về hồ sơ thiếu chứng cứ, không đánh giá tính thật của sự kiện ngoài kho.

### t125-do-buoc-khong-go-duoc-vong-nen-bi-cat  [P1]  A1 trước land được miễn cả phản chứng bắt buộc

TỆP/DÒNG: T:25,169–191,297–301; G:587–589,859–867.

VẤN ĐỀ: Trong nhánh không có nền hoàn tất, A1 không có mẫu số cho cả bản đúng lẫn bản giữ t125 trong gate. Cả hai đi vào KHÔNG ĐO ĐƯỢC không đỏ, trái yêu cầu đột biến đó phải làm A1 đỏ. Nếu giữ đột biến là chốt độc lập bắt buộc thì packet vẫn kẹt vì không thực hiện được phép đo; nếu miễn cả nó thì A1 hằng-chấp-nhận trong nhánh hiện tại. Sau land chỉ công bố số và vẫn ĐẠT khi timeout không chứng minh đã bỏ tải. T:25 còn hứa tạo nền chạy trọn; T:300 vẫn nói né bằng thời lượng bước, chính lập luận đã bị rút. T land không bảo đảm điều kiện để G A5 xanh.

ĐÃ THỬ VÁ: Executor công khai giới hạn cận dưới và thêm hai đường; đã biến nghĩa vụ chứng minh hiệu quả trước land thành miễn đo mà chưa có phép phân biệt thay thế trong A1.

ĐÃ THỬ NGHIỆM: Lần từng nhánh hợp đồng với cùng tình trạng nền bị cắt, bản giữ tải cũ và bản tách tải. Đây là phản mô hình bằng lời, không phải chạy Windows hay dựng mutant.

ĐỘ TIN: Cao. Không kết luận mọi A1 ở mọi dữ liệu đều hằng-đúng; chỉ nhánh không nền trước land mà spec đang chọn.

### uoc-bien-t125-sai-so-hang-va-sai-chieu-can  [P2]  Cận cũ còn sống và max mẫu lại được gọi là cận trên thật

TỆP/DÒNG: T:69–83,309–311; E bảng M5–M7.

VẤN ĐỀ: T:309 vẫn khai biên3,74–8,68 như ước hiện hành sau khi đầu tệp rút nó. Max2,89 chỉ là max11 mẫu packet-loop, không là cận trên của bước21–41 hay lượt mới. M5–M7 còn dùng kết quả5 chữ số từ thương đầy đủ nhưng ghi số hạng8,10; sai khác nhỏ0,00185185 phút là lỗi biểu diễn phép tính, không phóng đại thành sai dự báo lớn. Rủi ro chính vẫn là gán thẩm quyền cận trên cho mẫu và giữ biên cũ.

ĐÃ THỬ VÁ: Executor sửa phép cộng lớn và khai giả định26,25 bằng thời lượng thật. Chưa sửa phần cuối và cách diễn đạt max mẫu.

ĐÃ THỬ NGHIỆM: Tính cả thương đầy đủ và số hạng literal; tái lập min/max/median từ đúng11 cặp TSV. Không xác thực timing mới không có hiện vật.

ĐỘ TIN: Cao.

### t125-doi-chung-co-cu-chua-chung-minh-than-ca-do  [P1]  A2c chưa thử khi hai verdict khác nhau

TỆP/DÒNG: T:208–222; `cay-kho/ops/lease_publish_test.py`:4018–4044.

VẤN ĐỀ: A2c buộc hai subprocess, hai môi trường và có câu “phải so”, nhưng các mutant bắt buộc chỉ bỏ một lượt hoặc đổi biến phân biệt. Hai ca ấy không vô hiệu riêng phép so. Khi hai verdict đều sạch, bỏ tác dụng phép so vẫn có hai lượt thật, đúng actor, đúng tuple và cùng kết quả đạt. Đếm hai tiến trình không đo được thuộc tính “rò actor còn làm t125 đỏ” mà dòng222 giao cho A2c.

ĐÃ THỬ VÁ: Executor đã chặn return sớm, bước tiến có thật. Câu tuyên bố phần(3) có tác dụng chưa kèm ca đổi màu đo chính phần(3).

ĐÃ THỬ NGHIỆM: Đọc t125 hiện hữu thấy nó thu và so tuple; đối chiếu từng mutant yêu cầu với ba nghĩa vụ mới. Chỉ phân tích trường hợp hai tuple bằng nhau, không dựng payload/mã mutant.

ĐỘ TIN: Cao về lỗ phép nghiệm thu; chưa khẳng định code hiện tại đã mất phép so.

### t125-a4-mot-phan-tu-khong-phu-hai-nen  [P1]  Phép chiếu độ phủ của T125 chưa có tập bổ sung thực thi được

TỆP/DÒNG: T:140,150,232–240.

VẤN ĐỀ: A4 so tập(tên bước,nền,conclusion), nhưng đòi thêm đúng một phần tử và tên phải nằm trong danh sách literal “khai thẳng trong đặc tả này”. Không có danh sách tên literal ấy. Với ma trận hai nền của M1/A5, một bước t125 mới sinh hai bộ ba khác nhau vì nền khác nhau, không thể là một phần tử. Job mới còn cần thiết lập môi trường; A4 chưa định nghĩa chiếu bản sao thiết lập, trong khi ngoài phạm vi cấm thêm bước khác. Nhánh hạ chỉ đòi0 cancelled, không canh bước bị skipped ngoài ý muốn như G A2. Nghiệm thu độ phủ không có cách hiểu thống nhất cho đường hai nền bắt buộc.

ĐÃ THỬ VÁ: Không có thay đổi lượt3 cho A4; reviewer không viết danh sách thay executor.

ĐÃ THỬ NGHIỆM: Đọc bộ ba và ma trận; đếm hai nền khác nhau cho cùng tên bước. Suy diễn tập hợp, không tạo workflow.

ĐỘ TIN: Cao với thiếu tên literal và lực lượng tập bổ sung; không khẳng định implementation phải dùng số bước setup cụ thể.

### branch-protection-hai-lan-khong-co-phep-do-trang-thai  [P1]  Hai A6(b) chỉ đòi ghi việc cần làm, không xác minh đã làm

TỆP/DÒNG: T:250–258; G:870–887.

VẤN ĐỀ: Cả hai A6(b) tự ghi “không có phép đo”, chỉ buộc mục chủ kho làm trước merge nằm trong Issue. Issue giống hệt nhau trong hai trạng thái đã require đủ và chưa require; A6(a) cũng giống nhau vì chỉ so tên in/YAML. Vì thế nghĩa vụ bảo vệ nhánh thực tế không có phép làm đỏ. Sửa tập require theo pha chữa danh sách, không chữa việc kết quả job mới có thực sự chặn merge. Không phải đòi reviewer offline đọc mạng: đây là chỗ thiếu hợp đồng chứng cứ cho người thực hiện có thẩm quyền sau này.

ĐÃ THỬ VÁ: Executor đã sửa hai tập require thành2 và4, chưa thêm bất kỳ quan sát trạng thái thực nào vào điều kiện nghiệm thu.

ĐÃ THỬ NGHIỆM: Đối chiếu các hiện vật mà A6 đòi trong hai tình trạng đã/chưa require; không gọi API và không thay đổi branch protection.

ĐỘ TIN: Cao về tiêu chí không phân biệt trạng thái; trạng thái GitHub hiện tại KHÔNG ĐO ĐƯỢC.

### bang-gom-bo-sot-cac-khang-dinh-kiem-duoc  [P3]  Bảng bằng chứng vẫn chỉ gom một phần hợp đồng đã đổi

TỆP/DÒNG: E mục M1–M7 và bảng pha; C:241–243; G:558–591,882,905; T:309.

VẤN ĐỀ: Có bảng pha mới nhưng chưa có số instance theo ngữ cảnh; không có phân rã11 nhóm tự kiểm, số đường của lối composite, số job mới mỗi lần require, hoặc biên cuốiT. Bảng đo phía trên ghi riêng từng mục và cả khớp/lệch. Các lỗi chức năng tương ứng đã dùng slug riêng phía trên, không nhân thêm finding chỉ vì cùng một số xuất hiện nhiều nơi. Phần inventory giữ slug P3 lượt2 để không làm sai khoá đếm.

ĐÃ THỬ VÁ: Executor bổ sung M1–M7/bảng pha, vẫn tự khai chọn theo trí nhớ. Một lời tự khai thiếu không xác minh các mục bị thiếu.

ĐÃ THỬ NGHIỆM: So E với các mục định lượng của nghiệm thu hiện hành, đếm lại bằng AST/YAML và số học ở BẢNG ĐO. Không lặp các phép đo lượt2 chưa chạy trong lượt này như bằng chứng mới.

ĐỘ TIN: Cao.
