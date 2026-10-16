# VERDICT — PR #508 lượt 5 (reviewed_sha d81f155)
KẾT LUẬN: changes_requested
ĐẾM: 3 P1 · 4 P2 · 1 P3

Reviewer: Codex / OpenAI, qua API, shell cục bộ; khác nền với executor Claude theo phân công. `reviewed_sha`: `d81f1553c3bc340d1817e3247cdf3292691b720a`; tree: `9ed43b08a1a6cf070a61b884efaed23126789269`. Thẩm quyền lượt 5 theo PROMPT: `tran_cu=4 · tran_moi=5 · ai_nang=ducthangho`; không tự cấp thêm vòng.

Phạm vi: ba đặc tả trong `cay/`, so với `LUOT4-*`, hiện vật và kho chỉ đọc. Không mạng, không sửa `cay-kho/`, không dựng payload hoặc mutant. Đã chạy đọc Git/AST/YAML và số học Decimal, rc=0; kết quả chính ở `MEASUREMENTS.txt`. Ba bản hiện hành bằng byte với HEAD; ba bản LUOT4 bằng byte với `41e83b5`. Worktree được review sạch. Không chạy benchmark, actionlint, CI, Windows hay bộ kiểm tương lai. Những phép làm đỏ nêu dưới đây là **review mô hình**, trừ phép đếm/tính/đối chiếu văn bản được ghi rõ đã chạy. Hiện vật Actions là bản bàn giao của executor, không phải xác minh máy chủ độc lập.

Quy ước: **C** = `cay/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md`; **G** = `cay/GATE-TACH-JOB-CAT-CHI-PHI.md`; **T** = `cay/T125-RA-JOB-RIENG.md`; **C4/G4/T4** = các bản `LUOT4-*`; **E** = `EVIDENCE.md`. Số dòng của bản hiện hành.

## ĐỐI CHIẾU LƯỢT 4

Đối chiếu đủ **11 slug**, trước khi tổng hợp finding mới: **3 ĐÃ VÁ THẬT · 6 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Phân loại toàn finding; vá được một phần không đóng phần còn lại.

| slug lượt 4 | phân loại | bằng chứng lượt 5 |
|---|---|---|
| `dau-phien-mat-nghia-vu-sinh-moi` | VÁ HỜ | C:M7:135 trả lại NGẪU NHIÊN/SINH MỚI; A5c(1b):211–216 gọi hai lượt nên thực sự đo bộ sinh và bắt hằng số. Nhưng hai lượt không buộc chung một giây; bộ sinh mốc giây có thể qua, bộ đếm tăng cũng qua dù không ngẫu nhiên. |
| `a5-trich-delimiter-van-bo-sot-bieu-thuc` | VÁ HỜ | G:300–325 thêm SHA workflow, if trần, hàm trạng thái và tập vị trí. Tuy nhiên danh sách vị trí vẫn bỏ `runs-on`, `env`, `with`, `run`, `concurrency`; khai tập tự quét không chứng minh nó đầy đủ. Ngay cây hiện hành có biểu thức ngoài tập. |
| `a1-ubuntu-khong-chung-minh-bo-tai-windows` | VÁ HỜ | T:167–188 thêm ba nghĩa vụ theo nền; bỏ cờ Windows, skipped và nối needs trực tiếp đều có hướng đỏ. Nhưng tên bước và nhãn BỎ QUA không chứng minh thân t125 đã không chạy; nguồn jobs không cung cấp argv/log thực thi. Nghĩa vụ song song trở lại, chưa đủ bằng chứng bỏ tải. |
| `mat-moc-require-truoc-merge` | ĐÃ VÁ THẬT | G:372–398/T:277–310 buộc readback + check exact head trước merge; chỉ readback sau land làm đỏ. Hai luật tên đều sửa điều kiện `name:` và hậu quả chặn của required context không tồn tại. Đây là vá hợp đồng, chưa phải chứng nhận ruleset hiện tại. |
| `uoc-moi-bo-mat-phan-duoi-bi-cat` | VÁ SINH LỖI MỚI | T:57–88 trả lại bước hoàn tất chưa biết và suffix chưa biết; bỏ đối chiếu 43,23 đúng. Nhưng mô hình mới gọi prefix 33,97 là đã đo mà không có nguồn và chưa hạch toán chênh 0,30 với 60,52−26,25; G:75–77 vẫn khẳng định T125 đưa bước về 8,96. |
| `billing-tam-luot-dung-tong-sau-luot` | ĐÃ VÁ THẬT | G:48,177–179/T:46,140–143 cùng tám ID. Cộng hiện vật Windows: 482,55×2=965,10; 48,255% làm tròn 48,3%. Đã bỏ “0 thông tin”. Chỉ chứng nhận số học với hệ số giả định, không chứng nhận hoá đơn. |
| `nen-cu-khong-bac-duoc-no-nen-hien-tai` | VÁ HỜ | G:470–481 nhận nợ nền mới, cấm mượn nền lịch sử và buộc dừng. Nhưng A1:200–203 vẫn nói không còn nhánh nền không tồn tại và mutant quay về 40,63. Hai nghĩa đang hiệu lực đối nghịch. |
| `mat-phan-chung-va-no-phan-ra` | ĐÃ VÁ THẬT | G:260–263 bắt chạy phản chứng shellcheck trên nền rc=1; G:148–150 giữ điều kiện có phân rã Windows trước mở packet; G:458–488 trả lại ĐÓNG MỘT PHẦN và nợ tăng theo biên nhận. Không yêu cầu khôi phục các bảng lịch sử không cần thiết. Provenance các số khôi phục xét riêng. |
| `hien-vat-khong-chua-so-dang-duoc-vien-dan` | VÁ HỜ | Hiện vật hai nền có Ubuntu N6/N7/A1(a), registry G3/G10 và attempt. Vẫn thiếu dữ liệu cho prefix 33,97, setup 2,75–3,27, phép 400/270, rig 44 lượt và readback ruleset; N6 còn dẫn nhầm hiện vật N1 chỉ có Windows. |
| `thu-hep-cham-khong-phai-va-kenh` | VÁ HỜ | C:286–297 khai PHẠM VI ĐÃ ĐỔI và chỉ chủ kho đóng phần đối kháng: đúng phần hạch toán. Nhưng C:64–80 vẫn phủ cả lớp “ngẫu nhiên” theo ý định, không theo tập lỗi được đo; không phải đã vá đường sửa khung. |
| `bang-gom-van-khong-phu-hop-dong` | CHƯA VÁ | E tự nhận chưa vá. Đo được E khai 14 run nhưng bảng có 13; C vẫn “Ba ca”/“11” cạnh bốn ca/≥12. Inventory chưa phủ số hiệu lực và số trôi. |

## MẤT MÁT / THU HẸP MỚI Ở LƯỢT 5

| thứ đổi | LUOT4 → LUOT5 | ĐÚNG BỎ / MẤT OAN / THU HẸP CÓ KHAI | bằng chứng |
|---|---|---|---|
| 43,23 làm dự báo job sau tách | T4:56–64 → T:57–79, giữ biểu thức chỉ để bác | ĐÚNG BỎ | Lấy bước bị cắt làm thời lượng hoàn tất và bỏ phần đuôi là sai mô hình; không phải một cận trên hợp lệ cần giữ. Mô hình mới còn lỗi riêng, không cứu được số cũ. |
| Dải 40,20–53,53 làm đối chiếu độc lập | T4:60–61 → T:77–79 | ĐÚNG BỎ | 18 success có thật, nhưng thuộc tải trước #492. Không acceptance nào có quyền dùng dải này làm bảo đảm cho tải mới. G:A1 vẫn có ngưỡng thiết kế 36 và G:A5 vẫn đòi nền mới. |
| “bội số trên mọi nền”, “đủ đưa job về dải đã đo” | T4:22,72 → T:22–24,85–88 | ĐÚNG BỎ | Bỏ lời khai vượt phép đo, không bỏ nghĩa vụ bỏ tải/t125 giữ răng. Tuy nhiên G:76 còn tựa vào dự báo bước 8,96, phải sửa đồng bộ. |
| Mẫu Ubuntu “ổn định”, 5 lượt, dải cũ | T4:134–142 → T:153–162 | ĐÚNG BỎ | 7 mẫu mới kiểm được; không mất ngưỡng 0,45, không mất fail-close hay yêu cầu đo lại. “ĐO CÙNG LƯỢT” cần hiểu là cùng chiến dịch đo A/B, vì một run sau tách không chứa bước trước tách. |
| Sinh dấu và ca 1b | C4:M7/A5c → C:135,211–216 | ĐÚNG BỎ phần M7 yếu cũ | Nghĩa vụ được tăng, không mất tên mutant/lần thử/rc/đóng lượt/chống dòng trùng. Ca mới chưa kiểm đủ tính ngẫu nhiên và mốc giây. |
| Danh sách trích biểu thức | G4:294–299 → G:307–325 | MẤT OAN phần “toàn bộ” nếu danh sách mới được coi là đầy đủ | Bỏ delimiter là đúng; thay bằng chỉ ba loại vị trí và cấm quét run lại loại vị trí có biểu thức thật. Chưa khai đây là hạn chế bộ giải; không được coi là đóng lớp. |
| Phản chứng shellcheck, phân rã #456, nợ biên nhận | G4 thiếu → G:148–150,260–263,458–489 | ĐÚNG BỎ trạng thái thiếu trước | Khôi phục nghĩa vụ/nợ; không xoá ngưỡng, write set hay ngân sách N=2. |
| Mốc require trước merge | G4/T4 thiếu → G:A6(b0)/T:A6(b0) | ĐÚNG BỎ trạng thái thiếu trước | Có điều kiện bằng chứng thời gian và phép bác chỉ-readback-sau. |
| Chống mã sản phẩm đối kháng | Đã bị loại ở C4 → C:286–297 giữ và khai thêm | THU HẸP CÓ KHAI | Không phải thu hẹp mới của lượt 5. Mục 4b thực tế nằm ở `chua_do_duoc`, không phải `ngoai_pham_vi` như PROMPT kể. Dẫn “ngoai_pham_vi/#5” cũng sai vị trí: #5 ở đó nói gpgsign; giới hạn quyền ở `chua_do_duoc` #5. Phần bị loại còn mở. |
| Windows bắt buộc về thời lượng | Đã hạ ở T4 → T thêm A1(c) | THU HẸP CÓ KHAI | Phép bỏ tải độc lập thời lượng là thay thế có lý về thiết kế, nhưng ba điều kiện chưa chứng minh đầy đủ hành vi, xem P1. Không tìm thấy lần thu hẹp thời lượng mới lén thực hiện ở lượt 5. |

Không thấy xoá thêm acceptance, write set hay ngưỡng trần ngoài các thay đổi trên. Kỷ luật “chép lại” bảo toàn được nhiều nghĩa vụ, nhưng các đoạn mới vẫn có diễn giải và số mới; không thể lấy tên phương pháp làm chứng cứ rằng không sinh lỗi.

## BẢNG ĐO

| mục | khai | đo lại / điều kiện | kết quả |
|---|---|---|---|
| Neo/gói | d81f155, tree trong E; ba spec 515/368/299 dòng | Git HEAD/tree khớp; byte bản sao và LUOT4 khớp; numstat ba tệp +84/−14, +82/−21, +19/−5 | KHỚP; không áp write set thi công tương lai vào toàn PR soạn spec |
| G1/N1, nền G2/N2 | 29 lượt; 28 kết thúc; 18/8/2; 40,63 và bước 2,97 | Parse hiện vật Windows: đúng, một hàng chưa kết thúc | KHỚP trong snapshot cũ |
| G8/N11, đủ tám ID | 482,55×2=965,10;48,3% | 60,30+60,33+60,52+60,32+60,28+60,23+60,30+60,27=482,55; ×2=965,10; /2000=48,255% | KHỚP; hệ số 2 và quota 2000 là giả định/chú thích, chưa kiểm billing thực |
| T:A1(a) | 7 Ubuntu success sau #492,1,90–2,42 | ID 34439063235:2,35;34549206309:2,37;34552510232:2,37;34568864158:2,42;34576916278:2,32;34587613400:1,90;34592424868:1,92; tất cả attempt=1 | KHỚP; bỏ 34563553711 failure đúng |
| Bản chụp hai nền | E:14 lượt; metadata đo 12:4xZ | 26 hàng=13 run; có cả run tạo 13:35Z. Không thể toàn bộ là snapshot lúc 12:4xZ | LỆCH inventory/thời điểm; cần mốc cập nhật hoặc tách snapshot |
| Số Windows sau #492 | G:473 nói 6 trong hiện vật | Windows cũ:6; bản hai nền mới:8 đã huỷ. Hai ID mới là 34587613400/34592424868 | Không bác số 6 trong cửa sổ cũ; không được kể như toàn bộ mẫu mới |
| N3/N4/N5 | 150,434/51,321=2,9312;65,88%;146/146 cả hai vế | Decimal:2,9312367257;65,8847069147%;benchmark.txt có tổng kết cả hai vế rc=0 | KHỚP snapshot; log .veA/.veB riêng không được giao, không tái chạy benchmark |
| N6/N7/N8 | 8,70× Windows;1,93× Ubuntu;20,2× delta;+1327/−1 | 25,83/2,97=8,69697;2,35/1,22=1,92623;22,86/1,13=20,23009;git diff đúng 1327/1 | KHỚP, nhưng nguồn Ubuntu phải đổi sang hiện vật hai nền |
| G3/G10 | 13,92+7,42=21,34;34,3/18,3/52,5%;dãy registry | Hai nền run34429604548 có 13,92/7,42; Decimal cho34,2604/18,2624/52,5228%;dãy15,48/15,93/20,53/17,27/16,67 có các hàng tương ứng | KHỚP số; G10 cần ghép ID rõ trong spec |
| N12/N13 phần còn thiếu | b15=7,38/6,27;prefix33,97 | Hiện vật hai nền không có b15 hoặc b1..19. 60,52−26,25=34,27, khác prefix0,30 | KHÔNG ĐỦ NGUỒN; không kết luận prefix bằng34,27 vì có thể có overhead |
| Mô hình T/G | bỏ 43,23; G vẫn8,96 | 26,25/2,9312=8,95538 là phép chia có điều kiện trên cận dưới; không phải dự báo thời lượng Windows hoàn tất | LỆCH nghĩa, xem finding |
| Setup và ước G |2,75–3,27;19,29;16,67–17,19;10,17–10,69 | Các phép cộng/trừ đúng nếu nhận số đầu vào; hiện vật mới không có chi tiết setup | SỐ HỌC ĐÚNG, NGUỒN SETUP THIẾU |
| Workflow G6/G7/A3/A4 |1 job,40 bước,10 if=7 trần+3 có dấu,timeout60,không name | Parse YAML HEAD khớp; runs-on là biểu thức ngoài danh sách quét A5 | KHỚP số, LỆCH độ phủ bộ giải |
| Đơn vị bước |T:suffix21..41 gồm21 bước | YAML có40 bước; bước lease là thứ19 trong YAML. API có thể tính setup thành bước riêng; gói không có inventory API 41 mục của run bị cắt | Chưa chứng minh21 mục chưa chạy; phải ghi đơn vị/API index, không trộn YAML |
| Ước additions G |35/17;44/33;79/50;158/100;135–200 | Khối dòng36–70:35/17;71–114:44/33 khi chỉ bỏ dòng comment, giữ dòng trắng (32 nếu bỏ cả trắng). Tổng đúng;135–200 là dự toán, không phải số đo patch tương lai | KHỚP theo quy ước giữ dòng trắng; cần đo numstat khi thi công |
| G:A1/A4/A5/A8/A9 |0,60×60=36;4 job;2 tệp;≤300;N=2 | Số thiết kế có phép đo cụ thể; pha1→2→4; không cần hiện vật chứng minh một ngưỡng do hợp đồng đặt | CÓ NGUỒN HỢP ĐỒNG |
| T:A1/A3/A7/A8 |1/2,9312≈0,3412;ngưỡng0,45;145+1=146;2 tệp≤300 | Nghịch đảo0,34115293; arithmetic đúng. HEAD có147 hàm test t-số;benchmark cũ146;spec có điều khoản mẫu số lúc thi công | KHỚP công thức, KHÔNG được ghim146 vào triển khai mới |
| C cấu trúc |233 dòng;16 assert=14 ca+2 hạ tầng;8 ca;10 mutant | AST:14 trongT1..T8;nap_tool/chay_dot_bien mỗi hàm1;233 dòng; DOT_BIEN có10 mục | KHỚP nguồn mã |
| C:gpgsign |10/8/1/0 dòng;packet-loop11 lần | Đọc bốn tệp:đúng cả hai đơn vị | KHỚP |
| C:A5c/A6 |4 ca,≥12 nhóm;vẫn “Ba ca” và “11” | Liệt kê1,1b,2,3=4;7 nhóm trước A5c+4+1 nhóm biên=12 | SỐ MỚI ĐÚNG, CHỮ/SỐ CŨ CÒN SÓT |
| C:nợ và ước |44 lượt=12+12+10+10;0 tái hiện;ước150–260;trần300 | Cộng44 đúng;không có rig/log cho0 tái hiện.150–260 là dự toán có khai, không chứng nhận đủ chỗ | THUẬT LẠI chưa tái lập; trần là nghĩa vụ |
| G:nợ khôi phục |400/270;−32,5%;20,7ms×10×bội số≈0,6–0,7s;118 biên nhận | −32,5% và0,606766s tính đúng;không có rig/timing của chính phép đo được dẫn | THIẾU NGUỒN phép đo; không vì vậy đóng nợ |
| G:#456 |43,20 run34045664423;17,70 registry | Kho có hiện vật review cũ `ops/reviews/pr468-hoso-4-packet-review-12-codex/manifest11-layout/do-review10/prose-checks.json` ghi43,2;không dùng nó chứng nhận tải hiện tại.17,70 vẫn cần hàng nguồn cụ thể | KHÔNG báo nhầm43,20 hoàn toàn vô nguồn |
| G5/N9 và HTTP |1 context;ruleset20856202 active;200/403 | Không có response ruleset/protection trong gói; các lệnh là cách lấy lại trạng thái, không khôi phục phép đo lịch sử | CHƯA XÁC MINH; A6 chưa được nghiệm thu thực tế |

Các số hình dạng lịch sử (2 lần nâng/3 mức, các sự cố #355/#359,4 lần đếm có mặt…) được dẫn tới CLAUDE.md/Git như lời thuật lại, không phải số đo hiệu năng mới. Không nhân mỗi số thiếu chứng cứ thành một finding độc lập. Những hằng số acceptance là quyết định hợp đồng, khác với lời khai một phép đo đã xảy ra.

## KIỂM TỪNG TIÊU CHÍ — khả năng ĐỎ

Đây là đánh giá khả năng phân biệt của **đặc tả**, không phải log chạy implementation. “Đỏ được” không có nghĩa đã đạt nghiệm thu. Một tiêu chí có phần bắt lỗi tốt vẫn có thể mù một nghĩa vụ trọng yếu; các phần mù được chỉ rõ.

| tiêu chí | phép phân biệt / kết luận |
|---|---|
| C:A1 | Đổi phân loại sang AssertionError chung làm ca hạ tầng nhận sai nhãn: đỏ được. |
| C:A1b | Hai lượt riêng ép hai assert hạ tầng; đổi một sang chot làm sai nhãn: đỏ được. |
| C:A2 | Tín hiệu thật ngoài dich phải KHÔNG GIẾT; bỏ so tên làm đỏ được. |
| C:A3 | Ba nhãn riêng và từng số hạng; gộp nhãn làm đỏ dù tổng giữ nguyên. |
| C:A4 | Nhật ký gọi2 lần ở hai kịch bản; mất trần retry làm đỏ; cần timeout rig để không treo vô hạn. |
| C:A5 | Hai repo,hai mutant riêng bỏ gpgsign; cả vòng10 mutant trong môi trường ký bắt buộc: đỏ được. |
| C:A5b | Subprocess thật,stdout giả kết quả; đọc stdout làm sai verdict. Ba ca trùng/thiếu/ca lạ đều có điều kiện đỏ. Không bảo vệ quyền ghi cùng interpreter. |
| C:A5c(1) | Chỉ nonce khác; bỏ so nonce làm đúng ca đỏ, các chốt khác không cứu. |
| C:A5c(1b) | Bắt hằng số và phát lại qua hai lượt thật; KHÔNG bảo đảm bắt mốc giây hoặc đo ngẫu nhiên. P1 dưới. |
| C:A5c(2) | Thiếu đóng lượt; gỡ yêu cầu đóng làm đỏ được. |
| C:A5c(3) | Đối số giả tên bị khung gánT3,phải kiểm bản ghi chứ không chỉ verdict cuối; đổi lấy tên từ đối số làm đỏ. Chỉ trong phạm vi emitter hợp tác. |
| C:A6 | Thiếu ca/đột biến riêng làm số ca được tính<12; đỏ được. Cần sửa hai số cũ, không hạ ngưỡng. |
| C:A7 | Một mutant rời GIẾT hoặc ca nền mất khỏi8/8: đỏ được, không tin rc suông. |
| C:A8 | Thêm tệp thứ2 hoặc additions>300 làm đỏ/dừng. |
| G:A1 | max Windows>36 làm đỏ. Gộp job không bảo đảm trở về40,63; yêu cầu mutant và ngân sách2 lượt phải được lập kế hoạch khi thi công, không tự chi thêm CI. |
| G:A2 | Tập bộ ba lệch trên dispatch/PR làm đỏ; nền bị cắt hạ về tập tên+nền và kiểm skipped/cancelled. Nhánh hạ không miễn A5. |
| G:A3(1) | Thêm job-if trần/đổi matrix/timeout làm bộ ba lệch: đỏ được. |
| G:A3(2) | Đổi if làm tập lệch; mất bản sao setup làm tiền tố9 bước lệch: đỏ được. |
| G:A3(3) | Đổi on/concurrency sau parse làm khác: đỏ được trong đơn vị cấu trúc, không phải byte nguyên bản. |
| G:A3 lint | Có phản chứng bắt buộc mới: nền rc1 giữ lỗi cũ, thêm lỗi mới,delta đa tập≠rỗng; so rc-only phải thua. Đỏ được, chưa chạy trong review này. |
| G:A4 | Một trong4 job thiếu/khác timeout60 hoặc timeout mức bước: đỏ được. |
| G:A5(1)(a) mục1 | Workflow SHA không chứng minh được/khác cây giải: đỏ được. Cần thu workflow_sha từ bằng chứng lượt, không giả định API jobs tự có nó. |
| G:A5(1)(a) mục2–3 | If trần/hàm chưa hỗ trợ đỏ được khi đã tìm thấy; các vị trí biểu thức ngoài danh sách chưa có bộ kiểm phủ độc lập. P1. |
| G:A5(1)(a) mục4 | Kỳ vọng độc lập khác instance trả về: đỏ được nếu bộ giải đầy đủ; không được sinh kỳ vọng từ mẫu jobs. |
| G:A5(1)(b–f) | Rỗng/thiếu trang/trộn attempt/thiếu timestamp/job không success đều fail-close; cần từng fixture riêng để phân biệt từng chốt, không chỉ fixture mất một job. |
| G:A5(2–3) | Sau và trước phải hợp lệ;cùng manifest A2;công bố tổng và tỷ lệ. Không có ngưỡng billing là lựa chọn công bố, không phải hằng-đúng về hợp lệ. |
| G:A6(a) | Tên context khai sai với check thực: đỏ được. |
| G:A6(b0) | Readback chỉ sau merge hoặc check sai head không chứng minh mốc trước: đỏ được. Đã khôi phục phép đo thời gian. |
| G:A6(b) | Thiếu một trong4 context/không đọc được: đỏ được. |
| G:A7 | Fixture2 bác consumer cũ;fixture3/4 bác thiếu Ruff/thứ tự sai. Đỏ được; M7 còn buộc không có registry ở mọi job phải lỗi. |
| G:A8 | Tệp thứ3 hoặc additions>300: đỏ/dừng. |
| G:A9 | Thiếu ref,CHAN12,người giữ khác hoặc dependency chưa land: đỏ/dừng. Không chạy canh mạng trong review offline. |
| T:A1(a) | Không bỏ t125,ratio≈1 vượt0,45: đỏ được. Cần chốt hai run/head/attempt của nền và sau; không lấy số lịch sử làm mẫu số cố định. |
| T:A1(c)(1) | Bỏ cờ có thể bị bắt,nhưng tên/log BỎ QUA không quan sát sự vắng mặt của thực thi; nguồn steps.name còn xung đột việc giữ tên A4. P1. |
| T:A1(c)(2) | Thiếu job/skipped/thiếu bản ghi A/B mỗi nền: đỏ được; “không skipped” riêng lẻ không chứng minh success. |
| T:A1(c)(3) | Needs nối hai job làm đỏ được; phải xét reachability khi có job trung gian,không chỉ chuỗi needs trực tiếp. Không có needs chỉ chứng minh được phép chạy đồng thời,không bảo đảm runner sẵn. |
| T:A1(b) | Success/cancelled có trạng thái khác;failure/timed_out/không có job chưa được gán nhánh ĐẠT. Phải giữ chưa đạt, không suy pass từ im lặng. Đây là công bố sau land,không bảo đảm hoàn tất Windows. |
| T:A2(1) | Xoá job riêng trong khi gate bỏ t125 phải có cổng đỏ. |
| T:A2(2) | Job tồn tại nhưng không chạyt125 phải có cổng đỏ; khác phép có mặt. |
| T:A2c(1) | Bỏ một subprocess làm số lượt≠2: đỏ được. |
| T:A2c(2) | Biến vô can không tạo hai giá trị actor ở con: đỏ được. |
| T:A2c(3) | Tuple verdict lệch qua chính hàm so + tích hợp;no-op làm ca đỏ. |
| T:A3 | Return im lặng tính ĐẠT khác BỎ QUA=1: đỏ được về hạch toán;không tự chứng minh chi phí t125 bằng0. |
| T:A4 | Tập trước cộng literal×hai nền;thêm bước/đổi tên/quên if làm đỏ. Hạ nhánh bị cắt mất so conclusion có khai,không miễn kiểm skipped/cancelled sau. |
| T:A5 | Job-if/matrix/timeout khác hoặc thiếu timeout làm đỏ; không thay phép needs ởA1(c). |
| T:A6(a) | Context khai lệch check thực: đỏ được. |
| T:A6(b0) | Readback chỉ sau land làm đỏ;check phải exact head trước merge. |
| T:A6(b) | Thiếu gate/gate-t125 Ubuntu hoặc thiếu response làm đỏ. |
| T:A7 | Sai2 đường hoặc additions>300 làm đỏ/dừng. |
| T:A8 | Tập ca gộp thiếu/thừa làm đỏ;147 ca ở HEAD phải được hạch toán khi thi công,không chép146. |

## NHẤT QUÁN GIỮA BA ĐẶC TẢ

Bảng context **khớp về tập tích luỹ từng pha**: hôm nay `{gate Ubuntu}`; sau T125 thêm `{gate-t125 Ubuntu}`; sau GATE thêm `{gate-registry Ubuntu,gate-packet-loop Ubuntu}`. Số job cùng1→2→4. Hai bảng không bằng byte: T in toàn tập ở pha2,G ghi “thêm”; đây không phải mâu thuẫn nếu đọc tích luỹ. Cả hai gọi mình “nguồn DUY NHẤT” là rủi ro duy trì hai bản sao, chưa đủ thành finding riêng khi dữ liệu đang khớp.

Hai luật tên cùng có điều kiện job không khai `name:` và cùng nói required context không được báo cáo sẽ chặn. Với tên riêng sau này phải đối chiếu tên check thực, không tiếp tục ghép máy móc job_id+nền; điều khoản đo lại đã có. Không dùng mạng nên không chứng nhận hành vi ruleset hiện hành từ lời kể G5/N9.

Đồ thị metadata không có chu trình: C độc lập; #503→T125; #502 và T125→GATE. Chuỗi văn G:134 “#502→T125→GATE” là một thứ tự có thể chọn nhưng **không phải đủ đồ thị**: còn #503→T125, và metadata không bắt #502 phải trước T125. Giữ distinction này khi cấp lease; không cáo buộc có vòng phụ thuộc không tồn tại. Các packet LO/2A/2B ở ngoài ba packet được giao review.

Mâu thuẫn còn chặn là dự báo Windows G:76 đối nghịch T:57–88; nền lịch sử G:A1 đối nghịch chính G:470–481; và phép kiểm tên bước T:A1(c) không tương thích một cách rõ ràng với bảo toàn tên T:A4. Sensitive chỉ đóng bằng approve tường minh, không bằng số finding giảm.

### dau-phien-mat-nghia-vu-sinh-moi  [P1]  Ca mới bắt hằng số nhưng chưa khoá bộ sinh mốc giây hoặc tính ngẫu nhiên

TỆP/DÒNG: C:135,211–216,233–239.

VẤN ĐỀ: Ca1b thật sự dùng hai lượt và bắt bộ sinh hằng số; khác ca1 đúng như executor nói. Nhưng không có ràng buộc thời gian/clock seam. Hai lần sinh nằm ở hai giây khác nhau thì mutant mốc giây cho hai dấu khác và bác bản ghi cũ: ca xanh đúng quy trình được viết. Một bộ đếm tăng cũng đạt toàn ca1b mà không đáp ứng NGẪU NHIÊN. Bởi vậy phép đo phần nghĩa vụ này còn mù, không thể khai đóng lớp sinh dấu bằng riêng ca ấy.

ĐÃ THỬ VÁ: Đã khôi phục M7 và thêm ca1b; chưa sửa code trong review. Cần buộc mutant mốc giây trả cùng tick ở hai lần sinh bằng điều khiển nguồn clock, đồng thời kiểm đường gọi nguồn ngẫu nhiên mới mỗi lượt. Không thay bộ sinh thật bằng fixture tự dựng hai dấu, vì sẽ quay lại chỉ đo phép so.

ĐÃ THỬ NGHIỆM: Review mô hình bằng lời: hai lần sinh ở hai giây liên tiếp; đổi sang bộ đếm tăng. Cả hai vẫn thoả khác dấu/phát lại bị bác. Ca khoá cần bắt cả hằng số lẫn clock bị ghim bằng **đúng ca1b**, và kiểm được không sử dụng bộ đếm thay nguồn ngẫu nhiên. Chưa chạy mutant; không dựng payload.

ĐỘ TIN: Cao về thiếu điều kiện bắt mốc giây và không đo tính ngẫu nhiên; không tuyên ca1b hoàn toàn hằng-đúng.

### a5-trich-delimiter-van-bo-sot-bieu-thuc  [P1]  Tập vị trí tự khai chưa chứng minh quét hết biểu thức

TỆP/DÒNG: G:307–325; `cay-kho/.github/workflows/ci.yml`:31–32,49,120,424.

VẤN ĐỀ: Danh sách strategy.matrix.*,job-if,step-if bỏ ngay runs-on đang chứa biểu thức ở dòng49. Env,with,concurrency cũng có biểu thức hiện hữu. Câu cấm quét run/comment đánh đồng comment YAML không được Actions giải với comment shell nằm trong giá trị run; chính G:265–267 kể Actions xử lý nội suy trong run comment. Không phải phải giải mọi script để đếm instance, nhưng bộ giải phải nhận biết vị trí có ảnh hưởng, giải dependency cần thiết hoặc từ chối dạng chưa hỗ trợ. Hiện tại nó chỉ tự công bố những nơi đã nhìn: không có tập/schema độc lập để so phần chưa nhìn, cũng không có ca nằm ngoài ba loại vị trí.

ĐÃ THỬ VÁ: If trần và hàm đã trở lại, SHA workflow tốt hơn head_sha. Cần kiểm cấu trúc theo schema vị trí được hỗ trợ, nhận diện các vị trí khác và fail-close theo phạm vi ảnh hưởng tới kỳ vọng; phân biệt YAML comment với scalar run. Không thu hẹp “đầy đủ” xuống chỉ những field đang liệt kê rồi tính là đã vá.

ĐÃ THỬ NGHIỆM: Đã đọc YAML thật,10 if gồm7 trần/3 có dấu và runs-on ngoài danh sách. Review mô hình ca khoá bằng lời: làm nguồn lựa chọn runner phụ thuộc một toán hạng không giải được ở vị trí hiện bị bỏ; manifest tự khai vẫn đủ ba loại cũ. Phép nghiệm thu phải bác trường hợp ấy độc lập với tập do bộ giải tự trả. Chưa tạo biểu thức hay chạy parser tương lai.

ĐỘ TIN: Cao; chứng cứ vị trí ngoài tập có sẵn trong cây, không cần giả định một cú pháp mới.

### a1-ubuntu-khong-chung-minh-bo-tai-windows  [P1]  Bằng chứng tên và nhãn chưa đo việc thân t125 không chạy trên Windows

TỆP/DÒNG: T:167–188,226–265; `cay-kho/.github/workflows/ci.yml` bước `lease-publish selftest`.

VẤN ĐỀ: Jobs steps.name là tên hiển thị, không phải lệnh hay argv thực thi; tên hiện tại không có cờ. Nếu bắt buộc thêm cờ vào tên, A4 lại làm đỏ vì đổi tên bước cũ. Nếu giữ tên, chốt phải dựa vào log A3 nhưng spec không chỉ ra đường lấy log và neo vào job/attempt. Kể cả có log BỎ QUA, một lỗi đặt việc hạch toán sau thân t125 vẫn vừa chạy tải vừa báo bỏ; A2c chứng minh job mới chạy,không chứng minh job gate đã ngừng chạy. Ubuntu vẫn có thể bỏ đúng để qua tỷ lệ,trong khi Windows thực hiện cả hai chỗ.

ĐÃ THỬ VÁ: Ba nghĩa vụ mới đúng hướng và có ca riêng cho bỏ cờ/skipped/needs. Cần chứng cứ thực thi theo mỗi nền: với cờ mới, thân t125 không được vào và không phóng hai con A/B trong gate; job riêng vẫn phóng chúng. Giữ tên bước ổn định; thu log/call record qua nguồn thích hợp,neo run/job/attempt/head. Quan hệ lịch chạy phải kiểm cả dependency gián tiếp khi có trung gian.

ĐÃ THỬ NGHIỆM: Đã đọc tên bước thật và hai acceptance T:A1(c)/A4. Review mô hình bằng lời: Windows chạy thân rồi mới ghi BỎ QUA,Ubuntu bỏ trước thân,job riêng chạy A/B đúng trên cả hai. Các nhãn hiện đòi không phân biệt được. Ca khoá phải làm đỏ khi thân t125 còn được vào ở gate Windows dù nhãn vẫn BỎ QUA; chưa chạy Windows/mutant.

ĐỘ TIN: Cao về khác biệt tên/log với thực thi và xung đột tên; chưa đánh giá implementation chưa viết.

### uoc-moi-bo-mat-phan-duoi-bi-cat  [P2]  Mô hình mới thiếu nguồn prefix và dự báo 8,96 vẫn sống ở đặc tả GATE

TỆP/DÒNG: T:57–79; G:65–81,130–132.

VẤN ĐỀ: Bỏ43,23 và dải lịch sử là đúng,không mất một cận hợp lệ. Nhưng prefix33,97 không có trong hiện vật. Ngay trong dữ liệu đang dùng,60,52−26,25=34,27,khác0,30; có thể đó là setup/độ trễ không thuộc bước,nhưng mô hình job phải hạch toán chứ không xoá. Bội số Windows cũng chưa biết nên phát biểu phép tính cũ chắc chắn thấp hơn sự thật cần điều kiện giữ bội số,không được kết luận dấu sai số vô điều kiện. G:76 còn nói T125 land đưa bước về8,96,đối nghịch việc T giữ bước hoàn tất/bội số chưa biết.

ĐÃ THỬ VÁ: Đã thêm các số hạng bị bỏ và gỡ kết luận job hoàn tất. Cần ghi nguồn prefix theo run/attempt/timestamps,thêm overhead nếu không nằm trong prefix/suffix; đồng bộ G thành điều kiện chưa đo. Không trả43,23 về làm giá trị nghiệm thu.

ĐÃ THỬ NGHIỆM: Decimal đã tính34,27,8,95538 và phép chia benchmark. Review mô hình: giữ mọi phần khác,thêm một suffix dương phải tăng tổng; thêm overhead0,30 phải tăng tổng; thay bội số Windows thì hướng so với43,23 không còn cố định. Chưa chạy benchmark/CI,không khẳng định33,97 tự nó là số giả.

ĐỘ TIN: Cao về thiếu nguồn/thiếu hạch toán và mâu thuẫn G/T.

### nen-cu-khong-bac-duoc-no-nen-hien-tai  [P2]  Nợ đã trả lại nhưng acceptance vẫn phủ định nợ ấy

TỆP/DÒNG: G:200–203,355–359,470–481.

VẤN ĐỀ: Chua_do_duoc0 đã nói nền lịch sử khác nền nghiệm thu,cấm mượn40,63 và nói mutant không tự trở về số ấy. A1 vẫn nói “không còn nhánh nền không tồn tại” và gộp job “quay về≈40,63”. Đây là hai câu chỉ dẫn hiện hành ngược nhau,không phải chú thích lịch sử: phần đầu G còn tuyên mọi câu đang hiệu lực. Ca gộp dưới tải sau T125 có thể khác40,63 và vẫn không cho nền hợp lệ; một nền push thành công cũng không tự thay nền dispatch A5.

ĐÃ THỬ VÁ: G:470–481 là cải thiện thực chất về fail-close và xử lý dừng. Cần sửa chính A1 để chỉ gọi40,63 là lịch sử,neo phép mutant vào nền mới và không hứa nó phải tái tạo số cũ; làm mới chứng cứ khi head/đầu vào đổi theo protocol. Không yêu cầu chạy lại vô điều kiện mọi khi master trôi.

ĐÃ THỬ NGHIỆM: Đã đối chiếu hai đoạn trong cùng tệp. Review mô hình: T land ở trạng thái có điều kiện,Windows vẫn cancelled;G:A5 phải đỏ theo đoạn mới trong khi A1 còn tuyên nền không thể thiếu. Đây là phản chứng bằng đúng nhánh hợp đồng cho phép,chưa phóng nền tương lai.

ĐỘ TIN: Cao về mâu thuẫn văn bản; không dự đoán thời lượng triển khai.

### hien-vat-khong-chua-so-dang-duoc-vien-dan  [P2]  Bổ sung hai nền chưa khôi phục đủ provenance số đang có hiệu lực

TỆP/DÒNG: G:45,71,147,465,485,509–515;T:40–45,61–65,362–368;C:57–60,272–278;E:phần Hiện vật.

VẤN ĐỀ: Ubuntu và G3/G10 đã có dữ liệu thật trong gói,không tiếp tục báo thiếu các ô ấy. Phần còn lại chưa có snapshot/log/rig cho setup2,75–3,27,prefix33,97,400/270,20,7ms trên118 biên nhận,44 lượt0 tái hiện và response200/403/ruleset20856202. Một lệnh REST tổng quát không tái lập phép đo quá khứ. N6/N7 còn dẫn N1 là tệp chỉ có Windows. Bản hai nền tự đề đo12:4xZ nhưng chứa lượt tạo13:35Z,không có mốc bổ sung; điều này làm timestamp provenance không nhất quán.

ĐÃ THỬ VÁ: Hiện vật hai nền + attempt là vá thật phần lớn thiếu hụt cũ. Cần chỉ tới từng hàng nguồn hoặc log/rig bất biến cho phần còn lại; nếu chỉ thuật lại thì gắn nhãn đúng và bỏ vai “đã đo/có nền” của số ấy. Giữ nợ hiệu năng có thể đúng dù bỏ những timing chưa chứng minh. Không yêu cầu tái chạy timing mới để hợp thức hoá timing lịch sử.

ĐÃ THỬ NGHIỆM: Đã parse hai bảng,đọc benchmark,kiểm hiện vật review cũ cho43,20,tính các tỷ lệ và đối chiếu các cột có thật. Phép kiểm đỏ là truy mỗi số về hàng chứa đúng run/attempt/đơn vị/thời điểm; các ô nêu trên thiếu. Riêng timestamp13:35 sau12:4x là mâu thuẫn trực tiếp. Không gọi API,không kết luận số ngoài máy chủ bị bịa.

ĐỘ TIN: Cao về thiếu nguồn trong các hiện vật được chỉ dẫn và timestamp; không phủ nhận dữ liệu lịch sử có thể tồn tại ở nơi chưa được giao/chỉ định.

### thu-hep-cham-khong-phai-va-kenh  [P2]  Khai phạm vi đã đổi đúng nhưng vẫn hứa bảo vệ mọi lỗi ngẫu nhiên

TỆP/DÒNG: C:64–80,129,221–231,284–299.

VẤN ĐỀ: Mục4b đã khai đúng rằng đường đối kháng còn mở và chỉ chủ kho đóng. Tuy nhiên ý định “viết với ý định đúng” không tạo ranh giới lỗi: lỗi vô ý cũng có thể sửa trạng thái khung hoặc phát một bản ghi hợp lệ sai nguồn. Nonce và chống trùng chỉ kiểm freshness/cardinality,không chứng minh nguồn. Câu “giết cả lớp giả mạo ngẫu nhiên” và M1 “không giả mạo được” vẫn rộng hơn các ca hạ tầng/stdout/phát lại/emitter được đo. Đây là phần chưa vá của finding cũ,không phải phát hiện một lần thu hẹp mới.

ĐÃ THỬ VÁ: PHẠM VI ĐÃ ĐỔI là cách hạch toán đúng,không tính thành đã chặn. Cần định nghĩa tập lỗi cụ thể được bảo vệ và giới hạn bất kể ý định tác giả; sửa tham chiếu nhầm ngoai_pham_vi/#5. Giữ phần đối kháng ở trạng thái chờ quyết định chủ kho,không tự cấp một packet kiến trúc mới.

ĐÃ THỬ NGHIỆM: Review mô hình bằng lời: một lỗi vô ý làm sai trạng thái tên ca của khung;hai chốt nonce/đúng một dòng không biết trạng thái ấy sai. Ca khoá phải kiểm giới hạn/lời khai không còn bao trùm lớp không được đo,hoặc nếu muốn giữ lời hứa thì điều phối phải dựng phản chứng thích hợp. Không tạo mã sản phẩm hay payload sửa khung.

ĐỘ TIN: Cao về sai phạm vi lời khai; không coi toàn bộ C:A1/A5b/A5c rỗng nghĩa.

### bang-gom-van-khong-phu-hop-dong  [P3]  Inventory chưa bắt được số cũ và mẫu số mới trong chính gói

TỆP/DÒNG: E:bảng Hiện vật và đoạn “CỐ Ý chưa đầy đủ”;C:201,234–239;T:226–232,337–341.

VẤN ĐỀ: E khai14 lượt hai nền trong khi đếm được13;C tăng lên4 ca A5c/≥12 nhóm nhưng vẫn “Ba ca” và“11”. Benchmark146 là snapshot cũ,HEAD147 ca có điều khoản đo lại cứu acceptance nhưng bảng E không kiểm độ trôi. Lượt5 không thay cơ chế gom theo trí nhớ; các lỗi số mới tiếp tục lọt đúng chỗ đã được báo.

ĐÃ THỬ VÁ: Executor tự khai CHƯA VÁ,không có cơ chế inventory mới. Cần bảng mỗi khẳng định định lượng với nguồn/đơn vị/SHA/cửa sổ/trạng thái;kèm liệt kê literal để đối chiếu4 và12. Không giảm ngưỡng≥12 để làm khớp câu cũ.

ĐÃ THỬ NGHIỆM: Đã đếm13 run/26 hàng,147 hàm t-số bằng AST và đọc literal1/1b/2/3. Phép kiểm đỏ: số lượng inventory khác số mục thực;ca không có mutant riêng không được tính. Số146 chưa bị gọi là sai tại SHA benchmark.

ĐỘ TIN: Cao.

## ĐIỀU KIỆN CÒN CHẶN

Ba P1: hoàn thiện phép kiểm bộ sinh dấu; kiểm phủ vị trí biểu thức độc lập với lời tự khai; chứng minh t125 thực sự không chạy trong gate trên từng nền,không dùng tên/nhãn làm đại diện cho hành vi. Bốn P2: sửa mô hình prefix/overhead và dự báo8,96 còn sót; đồng bộ A1 với nợ nền mới; đủ nguồn và timestamp cho số hiệu lực; thu lời hứa CHAM về đúng tập lỗi đo được và giữ phần đối kháng còn mở. P3: cập nhật inventory14→13,các số3/11 cũ và mẫu số suite theo SHA.

Mốc require trước merge, số billing tám lượt và việc khôi phục phản chứng shellcheck/nợ phân rã đã được vá ở mức hợp đồng. Không dùng những phần đã tốt để đóng các blocker còn lại. Verdict lượt này là **changes_requested**, không có approve; cả ba packet sensitive chỉ đóng khi có **approve tường minh** trên exact head phù hợp. Thu hẹp phạm vi không được ghi là vá hành vi cũ.
