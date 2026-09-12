verdict: changes_requested
reviewed_sha: c1bfabc52616dc37b086e5462424aed0be3439f9

Reviewer: Codex, OpenAI, qua API và shell cục bộ; độc lập với executor Claude. Tree: `5d251820bab05dc1871726571d6383c9c5840b71`. Không gọi mạng, không sửa `cay-kho/`, không dựng payload hoặc đường thoát cây. Không tạo cây vá: đây là review hợp đồng, chưa thi công một thiết kế thay thế.

Quy ước dòng: **G** = `cay/ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md`; **T** = `cay/ops/specs/T125-RA-JOB-RIENG.md`; **C** = `cay/ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md`. Các số dòng là của đúng ba blob tại SHA trên. Finding đang mở: **5 P1 · 6 P2 · 1 P3**. Phân loại “đã vá” dưới đây nói về đặc tả, không phải xác nhận một implementation chưa có.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc `VERDICT-LUOT-1.md` trước các tài liệu khác; kiểm thêm hai bản đối chiếu và delta, đều khớp Git.

- `doi-ca-assert-ha-tang-thanh-tin-hieu-chot`: **VÁ HỜ** — M1 C:142 và A1b C:162–169 đã chỉ đúng 14 chốt/2 assert hạ tầng. Nhưng C:101 vẫn ghi “16 assert trần của 8 ca”, C:268–270 vẫn dự toán việc đổi **16** assert cùng **5** ca/5 đột biến. Chỉ thị cũ chưa gỡ sạch; lỗi còn lại hạ xuống P2 vì M1/A1b hiện đã chỉ đúng tập cần chuyển.
- `lop-ngoai-le-chua-bao-ve-duong-truyen-ket-qua`: **VÁ HỜ** — M6 C:147 và A5b C:205–213 sửa được tin stdout và thêm thử subprocess thật, trùng/thiếu/ca lạ. Chưa quy định ai có quyền ghi kênh riêng, cách cô lập mã được thử khỏi kênh, hay neo kết quả vào mutant/lượt thử hiện tại. Tệp riêng hoặc fd riêng tự nó không xác thực nguồn phát.
- `fixture-ky-commit-con-mot-kho-chua-phu`: **ĐÃ VÁ THẬT** — C:145,194–203 phủ cả `work` và `src`, hai đột biến gỡ ghim riêng, kèm chạy TRỌN suite dưới môi trường ký commit. Không còn đường nghiệm thu chỉ chạy tám ca rồi bỏ vòng tạo `src`. Chưa xác thực runtime vì PR chỉ có đặc tả.
- `them-t125-nhung-giu-hop-dong-ba-job`: **VÁ SINH LỖI MỚI** — G:652–653 gỡ M8/M9, G:906–907 thu hồi cả A10/A11 bằng một đoạn có phạm vi rõ, G:632–637 đóng ngoại lệ đổi lệnh: những phần này đã gỡ thật. Nhưng T đi trước nên sau T có **2** job, sau G có **4**, không có trạng thái cuối chỉ ba job. T:108,163–167 lại đòi require bốn job ngay trước khi T merge, trong đó hai job chỉ do G sau đó tạo. G:774–775/A6 lại gọi danh sách kỳ vọng ba job. Lỗi hợp đồng số job chưa biến mất, chỉ đổi chỗ.
- `a2-doi-giu-ca-ket-luan-cua-nen-bi-cat`: **ĐÃ VÁ THẬT** đối với lỗi cũ — G:699–706 đã định nghĩa nhánh bỏ cột conclusion, giải thích skipped và khai ĐẠT CÓ ĐIỀU KIỆN. G:831–834 nay quy định rõ bất kỳ điều kiện A5(1) hỏng đều ĐỎ. Vì vậy không còn buộc nền cancelled và sau success phải có bộ ba bằng nhau. Giới hạn: A2 hạ chỉ chứng minh tên/nền, không chứng minh tương đương kết luận; nó không cứu được nghiệm thu toàn packet khi A5 vẫn đỏ. M2 G:646 phải được đọc cùng ngoại lệ A2, không được dùng nhãn có điều kiện để tuyên bố toàn bộ M2 đã chứng minh.
- `a5-hop-le-chua-doi-du-job-va-du-luot`: **VÁ HỜ** — G:804–823 có đủ các chốt mới không rỗng, cạn phân trang, attempt, timestamp, manifest dùng chung. Nhưng (a) không định nghĩa độc lập tập kỳ vọng theo từng vế: vẫn nói “revision 6: bốn job” cho MỖI lượt, trong khi A4/A6 nói ba, và nền sau T thực tế hai. Cũng chưa neo cách dẫn xuất ma trận kỳ vọng vào cây/event/input có thẩm quyền. So bằng một tập kỳ vọng sai không chứng minh đủ tải.
- `a4-dem-chuoi-khong-phai-timeout-tung-job`: **ĐÃ VÁ THẬT** — G:773–785 đã thay đếm chuỗi bằng đọc khóa từng job, thiếu khóa đỏ, khác 60 đỏ, cấm timeout mức bước. Lỗi danh sách job chưa phủ `gate-t125` thuộc finding hợp đồng số job ở trên, không đếm lại thành lỗi phép parse.
- `r5-con-giu-nguong-cu-trong-dieu-kien-hien-hanh`: **ĐÃ VÁ THẬT** — G:994–999 thu hồi rõ MỌI 25,00/135,00 còn lại về lịch sử; G:659,667 chốt 0,60×60=36; G:831–834 rút ngưỡng 135 và chốt nền không hợp lệ ⇒ ĐỎ. A5 không có ngưỡng tiền vẫn đỏ được khi thiếu dữ liệu hợp lệ hoặc không công bố đủ kết quả; không phải tiêu chí hằng-đúng.
- `metadata-va-loi-thoat-composite-chua-theo-write-set-r5`: **VÁ HỜ** — bảng write set G:560–563 về hai tệp và phép 2+1=3 ở G:548–553 đúng số học. Nhưng A8 G:870–873 vẫn đòi đúng ba đường, gọi `lease_publish_test.py` là tệp thứ ba; metadata G:35 nói wp502 nhưng G:40 và A9 G:887–890 vẫn đòi wp503. Cạnh phụ thuộc vào packet T mới cũng chưa có trong metadata. Lối composite được nói là dùng được trong khi G:581 vẫn cấm mọi đường khác bảng.
- `so-ci-moi-chua-duoc-khai-la-thuat-lai-trong-spec`: **VÁ HỜ** — C:21–32 đã gắn nhãn đúng; T:37–44 có run_id cho bảng mới. G chỉ thêm lời THUẬT LẠI ở A1 G:680–684, chưa thu hồi các khẳng định rộng G:208–209,962–966 về “bốn lượt” và “chưa hoàn tất lần nào”. Hai lượt bổ sung vẫn không có run_id, conclusion mức run không chứng minh job Windows bị timeout. T:55 còn khai mọi số THUẬT LẠI phía trên cùng run `34563553711`, trái chính T:44 (`34552510232`).
- `benchmark-moi-thieu-hien-vat-neo-luot`: **VÁ HỜ** — G:969–977/T:199–202 thừa nhận không hiện vật, cận 7,694915 sửa đúng tại G:974–975. Nhưng EVIDENCE N7–N9 và T:27–34 vẫn phân loại timing là “ĐO LẠI ĐƯỢC từ cây kho”; chưa có hiện vật nào neo các số vào cùng lượt/rig. G:937 còn số ≥7,8 trong bảng kể hình dạng. Chuyển nghĩa vụ bàn giao sang phiên thi công không biến dữ liệu hiện nay thành đã kiểm được.
- `lan-thu-ba-khong-cung-hinh-dang-tin-dung-gia`: **VÁ HỜ** — hai hàng C:238–239 phân đúng hai chiều: cấp thừa 2, cấp thiếu 1; C:247 rút §12 đúng. Nhưng C:272–275 vẫn nói hàng đầu đếm 3 và dùng §12 để đặt quyết định đổi cách làm trước chủ kho. Chính đoạn kết còn hiệu lực phủ định lời rút phía trên. Các hàng “rút lời”, “lời khai rộng”, “đồ giả” phía dưới không bị cộng vào hai chiều này; không có căn cứ báo chúng là gộp nhầm, dù cú pháp bảng đã bị ngắt bởi văn xuôi.
- `bang-gom-bo-sot-cac-khang-dinh-kiem-duoc`: **VÁ HỜ** — đơn vị gpgsign và số dòng GATE trôi đã được giải thích tại C:122–134; N1–N17 vẫn bỏ sót số tệp trong A8, số job theo từng pha, các số hạng tạo N16, số ca mới ở dự toán, và nhiều khẳng định lịch sử có thể kiểm. BẢNG ĐO dưới đây ghi cả khớp lẫn không khớp; không tái dùng kết quả lượt 1 như phép đo lượt 2.

## BẢNG ĐO

Các phép đọc Git dùng `git -C cay-kho`, không fetch, không gọi `ls-remote`, không chạy gate có thể ghi vào mirror. Đặt `HOME`/`XDG_CONFIG_HOME` của tiến trình đo về thư mục hiện tại, `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`; không sửa cấu hình kho. Timing cũ không thể được xác thực bằng một benchmark mới khác rig. “Khớp số học” không xác nhận đầu vào.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| HEAD / tree | `c1bfabc52616dc37b086e5462424aed0be3439f9` | HEAD đúng; tree `5d251820bab05dc1871726571d6383c9c5840b71` | Có |
| merge-base với origin/master cục bộ | base theo merge-base | `26e2555d36c48b3c0f625ae50ab2cfb62b6cb858`; origin/master `e82af37fe66629d5378ac56fc689e24db26594fa` | Đã đo cục bộ; không xác thực master trực tiếp |
| numstat | 3 tệp, +881/−30 | C +275/−0; G +401/−30; T +205/−0 | Có |
| ba bản `cay/` | C r2, G r7, T r1 | Khớp byte blob HEAD; lần lượt 275, 1019, 205 dòng | Có |
| bản đối chiếu / patch lượt 1→2 | G r5, C r1; delta hai SHA | Hai bản khớp blob `4918d5f`; patch khớp `git diff 4918d5f HEAD -- ops/specs` | Có |
| băm verdict lượt 1 | `29ee0caa…` | `29ee0caae25debde66740f5c63f502f83c2c5df2adbd489c468b120cdb2bcf37` | Có |
| mirror | is-shallow=false, abbrev=7 | `false`, repo-local `7` | Có; không chứng minh đủ ref máy chủ |
| N1 — assert trong T1…T8 / toàn tệp | 14 / 16 | AST: 1+1+2+1+1+1+2+5=14; toàn tệp 16 | Có |
| N2 — hai assert hạ tầng | nap_tool:80, chay_dot_bien:198 | AST đúng hai vị trí | Có |
| N3 — tạo và commit repo thứ hai không tắt ký | 186–192 | `git init` src:186; config tên/mail:187–188; commit:192; không ghim gpgsign | Có |
| N4 — gpgsign packet_loop_test | 10 dòng / 11 lần | 10 / 11 | Có |
| N5 — hash ci.yml d28c4b1 = origin/master | `8dbc730f8a66a8dc…` | Cả hai `8dbc730f8a66a8dc86da9ff487108809b320ba35aa0bdb4bc773da99cd18a22b` | Có |
| N6 — hình dạng workflow hai ref N5 | 1 job; 40 bước; timeout 60; job if None; 10 step-if | YAML parse đúng cả năm số/giá trị ở cả hai ref; job là gate | Có |
| N7 — timing t125 / toàn suite | 114,10 s / 173,6 s = 65,7%; nhóm ĐO LẠI ĐƯỢC | 65,72580645% từ số khai; không có log, rig hoặc mốc lượt cho hai thời lượng | Chỉ khớp số học; sai phân nhóm chứng cứ |
| N8 — TỔNG/B tại d28c4b1 → 4b5184e | 3,09 → 3,24 | 75,3/24,4=3,086065574; 177,0/54,6=3,241758242 | Chỉ khớp số học; bốn timing không tái đo được |
| N9 — B / tốc độ tăng | 24,4 → 54,6 s; 2,24× | 2,237704918×; tăng 123,77049% | Chỉ khớp số học; không xác thực hai thời lượng |
| N10 — Windows bước 1–19 | 33,97 phút, run 34563553711 | THUẬT LẠI; không hiện vật | Không tái đo được |
| N11 — Windows bước 20 | ≥26,25 phút, cancelled, run 34563553711 | THUẬT LẠI; nếu đúng là bước bị cắt thì không phải thời lượng hoàn tất | Không tái đo được; không được dùng làm mẫu số hoàn tất |
| N10+N11 so thời lượng job | job 60,52 phút, cùng run 34563553711 | 33,97+26,25=60,22; còn 0,30 phút cho khoảng ngoài bước | Nhất quán nội tại; không xác thực CI |
| N12 — Windows test registry | 15,48 phút, run 34563553711 | THUẬT LẠI; ≤33,97 của bước 1–19 | Nhất quán nội tại |
| N13 — Windows packet-loop | 7,13 phút, run 34563553711 | THUẬT LẠI; 15,48+7,13=22,61 ≤33,97 | Nhất quán nội tại |
| N14 — Ubuntu bước 21–41 | 5,35 phút, run 34552510232 | THUẬT LẠI; thuộc lượt khác N10–N13 | Run_id được khai; T:55 lại nói cùng lượt là sai |
| N15 — 26,25/3,24 | ≈8,10 phút, ƯỚC | 8,101851852 phút | Đúng phép chia; không suy được giá trị trung tâm/cận trên từ cận dưới |
| N16 — job và biên | ≈51–56 phút; biên 3,74–8,68 | Với CHÍNH số hạng ghi: 33,97+26,25/3,24+5,35×[1,73;2,35] = [51,32735185;54,64435185]; biên [5,35564815;8,67264815] | Không; đầu 56/3,74 không sinh từ các số hạng đã khai |
| N17 — cận hệ số | ≥7,694915× | 22,7×60/177=7,694915254 | Đúng số học có điều kiện; ≥22,7 thiếu run_id rõ tại G:202 |
| tăng số ca lease / số receipt ở d28c4b1 → 4b5184e | 121→146 (+21%); 73→118 (+62%) | Đếm decorator @ca và receipt: 121→146; 73→118; tăng 20,6612% / 61,6438% | Có |
| tăng TỔNG ở hai ref trên | 75,3→177,0 (+135%) | Tăng 135,05976% từ số khai | Chỉ khớp số học |
| hình thức t125 / cờ CO_AB | hai lần chạy toàn suite; return vẫn tính đạt | Hai lời gọi `luot`, mỗi lời gọi cùng script với CO_AB; nhánh return:4015–4016; main tăng qua:5373 | Có về luồng mã, chưa phải chạy đo |
| C:101 / C:268 — assert của tám ca / số đổi | 16 / 16 | 14 thuộc ca; 2 hạ tầng | Không |
| C:268–270 — quy mô tự kiểm dự toán | 5 ca + 5 mutant | A6 hiện đòi ≥8 nhóm ca, A5 đòi hai đột biến riêng; A5b còn ba ca biên | Không còn cùng thiết kế |
| C:101 — chay_dot_bien / kho_bare | 182–219 / 25–66 | AST đúng hai khoảng; cả tệp 233 dòng | Có |
| C — DOT_BIEN / ca sản phẩm | 10 / 8 | AST DOT_BIEN có 10 mục; T1…T8 có 8 hàm | Có |
| C — gpgsign các bộ còn lại | lease 8; bien_nhan 1; nhanh_don 0 dòng | 8/1/0 dòng, cũng 8/1/0 lần xuất hiện | Có |
| C — số lượt không tái hiện | 12+12+10+10=44; 0 tái hiện | Tổng 44; không có log thực nghiệm từng lượt | Khớp số học, không xác thực 0 |
| C — phân loại lịch sử | cấp thừa 2 / cấp thiếu 1; rút §12 | Hai hàng 238–239 đúng phân loại; đoạn 272 vẫn đếm hàng 1 là 3 | Không nhất quán |
| G — write set / composite | bảng 2; thêm 1 thành 3 | 2+1=3, trong trần ADR; A8 vẫn đòi 3 tệp và gọi tệp #3 là lease_publish_test.py | Số học đúng, hợp đồng sai |
| T — write set | 2 tệp | ci.yml + lease_publish_test.py | Có |
| C — write set | 1 tệp | nhanh_don_duoc_test.py | Có |
| hợp write set ba packet | mỗi packet có trần riêng | G∩T={ci.yml}; C rời cả hai; hợp 4 đường | Không tự vi phạm ADR vì 4 là hợp của ba packet |
| số job theo thứ tự đã chọn | T require 4; G kỳ vọng 3; A5 nhắc 4 | Nền 1; T thêm đúng1 ⇒2; G thêm đúng2 ⇒4; dispatch hai nền tương ứng 2→4→8 instance nếu đủ hai nền | Không |
| metadata dependency | G [wp502]; T [wp503] | Đúng với hai lời khai người giữ tệp thứ hai; G thiếu cạnh T; G:40/A9 vẫn gọi wp503 | Chưa biểu diễn chuỗi đầy đủ; không xác thực lease trực tiếp |
| G — A1 | 0,60×60=36 phút | 36; 1/3,24=0,308641975 cho lập luận T A1 | Khớp số học |
| G — trôi nền 1b3caa1→28cb898 | 46 commit; 39→40 bước; step-if10, timeout60 | Git count 46; YAML 39→40; if10 và timeout60 cả hai; thân run trùng0 cả hai | Có |
| G — lịch sử timeout | 25→45→60; hai lần nâng | Blob 9e4f361:25; 6d88a2c:45; 7657bfd:60 | Có |
| G — consumer Ruff | loi_ruff_ci:140–158, 19 dòng | AST 140–158; đọc jobs.gate.steps | Có |
| G — packet_loop_test | 4.733 dòng; 169 dòng / 179 lần nhắc mutant | 4733 / 169 / 179 với mẫu DOT_BIEN hoặc dot_bien hoặc đột biến | Có |
| hiện vật lịch sử | job.tsv26 / buoc.tsv1140 | CSV đếm 26 / 1140 hàng dữ liệu | Có |
| mẫu 11 Windows được G liệt kê | 5 master+6 nhánh; min40,20/max50,48/median46,02/mean45,84 | Lọc đúng 11 head: 5+6; 40,20 / 50,48 / 46,02 / 45,83727273 | Có |
| phép đọc toàn TSV, trước khi lọc mẫu | Không phải mẫu 11 của bảng | 12 Windows success: min40,20/max50,48/median45,80/mean45,6175; có thêm run 34045664423 | Đo bổ sung; KHÔNG dùng mẫu 12 để báo sai bảng 11 |
| G:317 — Ubuntu mẫu lịch sử | n19; 20,93–28,42; median26,52 | TSV bàn giao chỉ có 13 Ubuntu success: 20,93–27,68; median26,52; mean25,866923; không đủ mẫu19 | Chưa xác thực n19/max28,42; không suy chúng sai từ mẫu khác |
| hệ số registry, mẫu11, n/min/max/median/dải | 11 / 1,07 / 1,71 / 1,21 / 1,21–1,21 | Tính lại từ giây: đúng cả 6 số | Có |
| hệ số tl selftest, mẫu11 | 11 / 1,41 / 2,26 / 1,83 / 1,82–1,84 | Đúng cả 6 số; ghép theo tiền tố tên | Có |
| hệ số packet-loop, mẫu11 | 11 / 1,88 / 2,89 / 2,37 / 2,36–2,38 | Đúng cả 6 số | Có |
| hệ số G5, mẫu11 | 11 / 1,91 / 3,09 / 2,40 / 2,37–2,43 | Đúng cả 6 số | Có |
| hệ số lease-publish, mẫu11 | 11 / 2,42 / 3,84 / 2,94 / 2,91–2,97 | Đúng cả 6 số | Có |
| hệ số bien-nhan, mẫu11, 10 cặp hợp lệ | 10 / 7,07 / 9,74 / 7,79 / 7,71–7,88 | Đúng cả 6 số | Có |
| hệ số job trọn, mẫu11 | 11 / 1,52 / 2,36 / 1,73 | 11 / 1,523966 / 2,358815 / 1,726829 | Có sau làm tròn |
| T:49 — hệ số packet-loop | 2,35 là “cận trên” | Bảng nguồn G:359 ghi min1,88/max2,89/median2,37; dải median2,36–2,38 | Không phải cận trên của mẫu này |
| phép tính thử mẫu12 trước khi lọc, n/min/max/median/dải | Không phải số PR khai | registry:12/1,07/1,71/1,23/1,22–1,23; tl:12/1,41/2,26/1,85/1,84–1,86; packet-loop:12/1,88/2,89/2,37/2,37–2,38; G5:12/1,91/3,09/2,41/2,38–2,44; lease:12/2,42/3,84/2,98/2,95–3,01; bien-nhan vẫn như mẫu10 ở trên | Đo bổ sung, không dùng mẫu khác báo lỗi PR |
| tổng tiền lịch sử | 110,65 run34045664423; 111,08 run34048685345 | 43,20×2+24,25=110,65; 42,28×2+26,52=111,08 | Có |
| run34045664423 — 5 bước nặng Windows | 17,70;9,70;3,53;3,47;2,50 | 17,7;9,7;3,533333;3,466667;2,5 phút từ giây | Có |
| cùng run — 5 bước Ubuntu | 13,13;3,65;1,00;1,85;0,87 | 13,133333;3,65;1;1,85;0,866667 | Có |
| cùng run — phần còn lại / tổng bước | Win6,27/43,17; Ubuntu3,70/24,20 | 6,266667/43,166667; 3,70/24,20 | Có |
| thiết lập cũ run34045664423 | 3,33 Win /1,18 Ubuntu, bước1–10 | 3,333333/1,183333; nếu lấy1–13:3,366667/1,183333 | Có cho tập cũ; so số mới1–13 không phải cùng thước |
| G:240–241 — thiết lập mới | 3,27 head27c413c;2,75 head4b5184e | THUẬT LẠI; ghép qua bảng run tại G:213–214 tương ứng 34552510232/34563553711 | Chưa đo; head không thay run_id khi có nhiều lượt cùng head |
| bảng chi phí sau tách lịch sử | 14,31;26,56;126,22; +14,1% | 13,13+1,18=14,31;7,42+14,31+4,83=26,56;49,83×2+26,56=126,22; tăng14,0714%; setup15,68 | Có về số học trên các số đã làm tròn |
| tổng ngây thơ run34563553711 | 60,52×2+12,38=133,42 | 133,42 | Có về số học; không chứng minh chạy đủ tải |
| E1/E2 được giữ lại trong G | 2,44s/118=20,7ms; ×10×3,24≈0,67s | 20,677966ms; từ20,7:0,67068s | Khớp số học; 2,44s chưa có hiện vật, ×10 là giả định |
| sửa mẫu số t125 lịch sử | 114,10/177,0 không phải65,7% | 64,46327684%; đổi sang173,6 cho65,72580645% | Đúng số học; chưa chứng minh cùng lượt |
| đối chiếu cổng executor | rc0;4/4; release180=180 | Không chạy lại; đây là lời khai bàn giao | Chưa xác thực runtime; không coi là bằng chứng nghiệm thu ba implementation |

Dòng mẫu12 ghi rõ để tránh lặp chính lỗi “ghép sai lượt”: phép tính sơ bộ trên TOÀN TSV và phép tính trên 11 head được chỉ danh là hai mẫu khác nhau. Các hàng hệ số dùng mẫu11 mới là phép đối chiếu PR.

Lệnh/phương pháp thực chạy, đều rc=0: `git rev-parse HEAD HEAD^{tree} origin/master`; `git merge-base HEAD origin/master`; `git diff --numstat <base> HEAD`; `git show <ref>:<path>`; `git ls-tree -r --name-only <ref> ops/reviews`; `git rev-list --count 1b3caa1..28cb898`; Python `hashlib.sha256`, `ast.parse` đếm Assert/decorator/FunctionDef/List, `yaml.safe_load` đọc từng jobs.gate, `csv.DictReader` và `statistics` tính lại TSV. Hai bảng dữ liệu đọc từ `cay-kho/ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5/`. Không chạy mã mutant hoặc suite sản phẩm.

## KIỂM TỪNG TIÊU CHÍ CÓ THỂ ĐỎ

Có **27** tiêu chí hiện hành, tính A1b/A5b riêng: C10 + G9 + T8. A10/A11 của G được thu hồi cùng nhau tại G:906–907, dù chỉ tiêu đề A10 được gạch chữ; không đếm chúng là tiêu chí thứ 28/29. Không tìm thấy tiêu chí toàn phần nào hằng-đúng. “Đỏ được” không đồng nghĩa “đủ chứng minh mục tiêu”, cũng không chứng minh tồn tại bản thi công xanh đồng thời dưới các mâu thuẫn hiện tại.

| tiêu chí | trạng thái thế giới làm ĐỎ | giới hạn còn lại |
|---|---|---|
| C A1 | nhận AssertionError hạ tầng là GIẾT thay vì KHÔNG ĐO ĐƯỢC | Ca lớp ngoại lệ không xác thực nguồn/kênh |
| C A1b | một trong hai assert hạ tầng được tính tín hiệu chốt | M1 đúng, dự toán cuối tệp vẫn nói16 |
| C A2 | chốt của ca ngoài đích được tính GIẾT | Neo tên chưa neo người ghi kết quả |
| C A3 | gộp nhãn hoặc in sai một số hạng dù tổng10 | Có răng; phải đo từng số hạng |
| C A4 | số lần chạy không bằng2 hoặc hai lần không đo được mà suite xanh | Cần giới hạn thời gian cho phép thử bỏ trần; hiện chưa khai |
| C A5 | src không tắt ký, hoặc trọn suite chết dưới môi trường ký | Hai repo và vòng mutant đã phủ đúng |
| C A5b | dòng stdout giả được parser tính GIẾT; hoặc kết quả thiếu/trùng/ca lạ vẫn hợp lệ | Chưa canh ghi trực tiếp/replay kênh riêng |
| C A6 | thiếu một nhóm ca có mutant riêng đã chạy đỏ | Dự toán5 ca cuối tệp chưa cập nhật; “đúng một mutant” phải đối chiếu A5 có hai phản chứng |
| C A7 | bất kỳ mutant nào rời giết=10, hoặc mất một ca sản phẩm | 8/8 là ca sản phẩm; tự kiểm mới phải có danh mục riêng để không bị giấu khỏi tổng |
| C A8 | tệp thứ hai hoặc additions301 | Có răng; ADR áp riêng packet |
| G A1 | max Windows >36 phút | Không cần mẫu số trước để kiểm ngưỡng này; lập luận coi nền trọn là tiền đề của A1 quá rộng |
| G A2 | mất tên bước/nền; ở nhánh thường, kết luận đổi | Nhánh hạ mất khả năng kiểm tương đương kết luận; không làm A5 xanh |
| G A3 | thêm if, mất tiền tố thiết lập, đổi on/concurrency hoặc delta chẩn đoán khác rỗng | So mọi job với gate hiện tại chưa tự chứng minh gate giữ cấu hình nền |
| G A4 | một job trong danh sách thiếu timeout hoặc khác60 | Cách parse đúng, danh sách ba job thiếu job đã có từ T |
| G A5 | thiếu job của tập kỳ vọng đã chốt, trộn attempt, thiếu mốc, có failure, hoặc không công bố đủ số | Tập kỳ vọng chưa chốt đúng từng vế; không có ngưỡng tiền không làm tiêu chí hằng-đúng |
| G A6 | tên công bố không khớp; chủ kho chưa require job cần thiết | Phần quyền bên ngoài có thể không đạt, nhưng không đo bằng công cụ phiên; thứ tự hai lần cập nhật sai |
| G A7 | loi_ruff_ci lại chỉ đọc jobs.gate | Có răng, phản chứng bố cục cũ/mới |
| G A8 | 2 tệp thay vì “đúng3”, hoặc additions301 | Đỏ được nhưng đang đỏ oan cho chính write set r7 |
| G A9 | lease còn giữ write set hoặc chưa đạt phụ thuộc bắt buộc | Nội dung phụ thuộc chưa đồng bộ metadata |
| T A1 | ratio bước>0,45; hoặc bước nền không hoàn tất | Ca nền được thuật lại chính là trường hợp thứ hai; xem finding vòng nghiệm thu |
| T A2(1) | xóa job trong khi main vẫn bỏ t125 mà không cổng nào đỏ | Chỉ đo hiện diện cấu trúc |
| T A2(2) | đổi lệnh job sang lệnh không chạy t125 mà không cổng nào đỏ | Đóng được ca lệnh thay thế ấy, chưa chứng minh thân t125 chạy đủ hai lượt A/B |
| T A3 | cờ mới im lặng đếm t125 ĐẠT, hoặc mất lý do bỏ qua | Cờ cũ cho kết quả khác chỉ chứng minh khác cách hạch toán đầu ra |
| T A4 | thêm tên bước ngoài allowlist hoặc mất tên bước cũ | Chưa có danh sách tên literal như T:145 hứa; nhánh hạ chỉ cấm cancelled, không kiểm lý do skipped như G A2 |
| T A5 | gate-t125 thiếu timeout hoặc bộ ba khác gate | So với gate hiện tại không tự chứng minh cả hai giữ cấu hình trước |
| T A6 | tên mới in sai; chủ kho không cập nhật required checks | Đòi require hai job chưa tồn tại ở pha T |
| T A7 | 3 đường hoặc additions301 | Có răng; đúng2 chặt hơn trần ADR3 |
| T A8 | thiếu một ca so tập nền hoặc số145+1 không bằng146 | Danh tính và số ca không chứng minh thân ca thực sự đo; coi mẫu số lúc thi công, không ghim146 vĩnh viễn |

Hai hàng T A2 là hai nửa của MỘT A2; tổng vẫn là27.

## ĐÁNH GIÁ TÁCH PACKET VÀ HỢP ĐỒNG CHUNG

Tách phần giảm thời lượng lease-publish khỏi phần dời registry/packet-loop là một lựa chọn thiết kế có thể hợp lý. Không có bằng chứng ở đây buộc phải quay lại gộp. Nhưng lý do “đã chứng minh T là tiền đề đủ để G nghiệm thu” chưa đứng: A1 G hiện kiểm ≤36 mà không cần thời lượng nền làm mẫu số; A5 mới cần nền hợp lệ. T chưa chứng minh cả gate và job t125 riêng chạy trọn, lại chấp nhận ở T:196–198 rằng gate vẫn timeout sau T “không phải thất bại”. Vì vậy T land không kéo theo nền G đo được.

Phép né bằng thời lượng BƯỚC chỉ hợp lệ khi bước nền đã hoàn tất rồi job mới bị cắt ở bước sau. T tự mô tả trường hợp ngược lại: chính bước20 bị cắt. T sau sửa không thể cung cấp thời lượng của bước20 TRƯỚC sửa. Đổi đại lượng không giải vòng này.

Theo thứ tự đã chọn, hình dạng phải được hiểu là `gate` → `gate + gate-t125` → `gate + gate-t125 + gate-registry + gate-packet-loop`. T và G giao đúng một đường `ci.yml` nên phải nối tiếp và nền G phải chứa kết quả T. C rời write set của cả hai, có thể làm riêng về quyền ghi, nhưng thay C có thể đổi tải registry: phép so thời gian vẫn phải khai SHA/tải. Không cộng 1+2+2 rồi dùng tổng ấy để báo vượt ADR một packet; cũng không lấy +881 dòng của PR đặc tả làm số additions của một implementation tương lai.

`[wp503]` của T khớp lời khai người giữ `lease_publish_test.py`. `[wp502]` của G chỉ biểu diễn người giữ consumer Ruff; nó chưa biểu diễn phụ thuộc chức năng/thứ tự vào T. T chưa có packet_issue, nên chưa thể điền một ID wp mới chính xác; không được vì thế coi đồ thị dependency hiện tại là đầy đủ. Không xác thực quyền sở hữu lease trực tiếp khi không có mạng.

Nghĩa vụ branch protection bị đặt sai pha: T yêu cầu cả bốn trước merge dù chỉ sinh job thứ hai; G về sau lại liệt kê ba và coi T như thứ thêm thứ tư sau nó. Nếu hiểu thao tác G là thay danh sách, có nguy cơ bỏ gate-t125; nếu hiểu cộng thêm thì vẫn phải chỉ rõ kế thừa check T. Dòng “mỗi lần một job mới” G:847–848 cũng sai số hạng: T thêm một, G thêm hai.

### doi-ca-assert-ha-tang-thanh-tin-hieu-chot  [P2]  M1 đã chỉ đúng 14 nhưng chỉ thị đổi 16 còn sống ở cuối đặc tả
TỆP/DÒNG: C:101,142,162–169,268–270.
VẤN ĐỀ: Sửa đúng M1 và thêm A1b chưa làm toàn hợp đồng nhất quán. Dự toán vẫn nêu “16 assert trần đổi sang chot()” và 5 ca/5 mutant, không gắn nhãn lịch sử; bảng write_set vẫn gán16 cho8 ca. Theo M1 mới phải đổi14 và giữ2. Đây là lỗi cũ còn sót, không phải finding mới mang tên khác. Hạ P1→P2 vì A1b hiện đã bắt chính bản thi công đổi nhầm hai assert.
ĐÃ THỬ VÁ: không — chỉ kiểm bản sửa executor, không viết cây triển khai.
ĐÃ THỬ NGHIỆM: Python `ast.parse` trên blob HEAD; đếm theo từng FunctionDef ⇒ T1…T8 có14, nap_tool:80 và chay_dot_bien:198 mỗi nơi1. Đối chiếu `nl -ba` C ⇒ chỉ thị16 còn tại268. rc=0, không chạy mutant.
ĐỘ TIN: cao

### lop-ngoai-le-chua-bao-ve-duong-truyen-ket-qua  [P1]  Kênh riêng chưa có hợp đồng xác thực nguồn và lượt phát kết quả
TỆP/DÒNG: C:147,205–213; mã nền `cay-kho/ops/nhanh_don_duoc_test.py:78–84,172–181,208–211`.
VẤN ĐỀ: A5b đã bắt đúng đường giả stdout qua subprocess thật. Nhưng M6 cho phép một tệp kết quả được truyền đường dẫn vào lượt con hoặc fd riêng mà không hạn chế mã được thử tiếp cận nó. `nap_tool` còn import mã sản phẩm trong chính tiến trình chạy ca. Hướng phản chứng bằng lời: mã được thử ghi hoặc thay nội dung trên chính kênh được tin; hoặc đưa một bộ kết quả đủ ca, duy nhất mỗi ca, nhưng thuộc mutant/lần thử trước. Những kết quả ấy không cần có dòng trùng, thiếu, ca lạ và không cần đi qua stdout. Đặc tả chưa neo mutant ID/lần retry, quyền ghi, hoàn tất lượt và rc vào record. Di chuyển chuỗi sang kênh khác không chứng minh người phát được tin. Không khẳng định đã khai thác một implementation chưa tồn tại.
ĐÃ THỬ VÁ: không — chưa chốt mô hình tin cậy của kênh trong hợp đồng.
ĐÃ THỬ NGHIỆM: đọc M6/A5b và các hàm nền bằng `sed`; xác nhận import trong tiến trình ca và subprocess/parser hiện hữu. KHÔNG ĐO ĐƯỢC parser mới vì chỉ có đặc tả; không dựng nội dung giả hay payload.
ĐỘ TIN: cao về thiếu hợp đồng; vừa về đường hiện thực cụ thể

### them-t125-nhung-giu-hop-dong-ba-job  [P1]  Thứ tự T125 rồi GATE không thể có tập job mà hai bản nghiệm thu đang yêu cầu
TỆP/DÒNG: T:9,88–89,104–108,160–167; G:74–110,577–579,652–653,774–775,842–848,906–907.
VẤN ĐỀ: T thêm đúng1 job lên nền1 ⇒2; G sau đó thêm2 ⇒4. Vì vậy “không có job thứ tư” ở G:99 sai ngay dưới kiến trúc mới, dù chính G không tạo job ấy. T A6 đòi require gate-registry/gate-packet-loop trước khi chúng được G tạo; G A4/A6 dùng danh sách3 bỏ gate-t125 đã tồn tại. Hai lần cập nhật branch protection bị mô tả theo thứ tự ngược với thứ tự packet. M8/M9 và A10/A11 đã thu hồi thật, ngoại lệ đổi lệnh đã gỡ; không báo các đoạn lịch sử ấy như lỗi còn hiệu lực. Lỗi còn lại là hợp đồng toàn workflow/required checks không theo trạng thái kế thừa.
ĐÃ THỬ VÁ: không — chưa viết lại hợp đồng chuyển trạng thái thay executor.
ĐÃ THỬ NGHIỆM: parse YAML nền ⇒ đúng1 job gate. Đối chiếu T ngoai_pham_vi#1/M1 và G M1 ⇒ cộng1 rồi cộng2 =2 rồi4. Đọc danh sách A6 của cả hai ⇒ T yêu cầu4 trước, G liệt kê3 sau. Không tạo workflow thử, không gọi GitHub.
ĐỘ TIN: cao

### a5-hop-le-chua-doi-du-job-va-du-luot  [P1]  Tập kỳ vọng chưa có nguồn đúng và chưa phân biệt bố cục trước với sau
TỆP/DÒNG: G:774–775,804–823,826–828; T:88–89.
VẤN ĐỀ: Các chốt (b)–(f) không sửa được một tập kỳ vọng sai ở (a). Nếu dùng nguyên “bốn job” cho MỖI lượt thì nền sau T chỉ có2 sẽ luôn bị đánh thiếu. Nếu dùng A6 ba job thì lượt sau4 bị loại hoặc job T bị rơi khỏi phép tính. Nếu executor tự suy kỳ vọng từ chính danh sách job đã đọc thì điều kiện bằng nhau trở thành tự chứng minh và lỗi thiếu job vẫn lọt. Nếu lấy matrix từ YAML ứng viên mà không đối chiếu cây/event/input nền, ma trận kỳ vọng có thể mất cùng nền với dữ liệu thực, làm thiếu Windows trông hợp lệ. Manifest dùng chung A2/A5 giúp nhất quán mẫu nhưng không xác thực nguồn của kỳ vọng. Chưa có quy tắc phân biệt job ID cấu trúc, job instance theo matrix và job ID API theo lượt để phép so thực hiện duy nhất.
ĐÃ THỬ VÁ: không — cần hợp đồng mẫu theo từng pha trước khi có bộ thu thập để sửa.
ĐÃ THỬ NGHIỆM: đọc toàn A5 và A4/A6 bằng `sed`; suy tập nền2/sau4 từ write set và M1. Phản mô hình chỉ mô tả bằng lời; KHÔNG ĐO ĐƯỢC việc thu đủ trang/attempt từ CI, không tạo phản hồi API giả.
ĐỘ TIN: cao

### metadata-va-loi-thoat-composite-chua-theo-write-set-r5  [P2]  A8 và A9 vẫn thi hành write set cùng phụ thuộc của revision đã bỏ
TỆP/DÒNG: G:35–41,548–581,870–890,1014–1017.
VẤN ĐỀ: Bảng r7 cho2 đường nhưng A8 đòi đúng3, gọi đường thứ3 là lease_publish_test.py của M8/M9 đã gỡ. Bản thi công đúng write set vì thế đỏ A8. Lối composite2+1=3 đã hết vi phạm trần ADR, nhưng đường composite vẫn không nằm trong bảng được cho phép, G:581 cấm đường khác. Metadata wp502 mâu thuẫn câu chờ wp503 ở ngay phần giải thích và A9; chuyện #456 hết hạn vẫn còn được đưa thành phương án chủ kho chọn ở chua_do_duoc#7. Cạnh G phụ thuộc T cũng chưa được biểu diễn. Không thể xác nhận scheduler giữ thứ tự bằng metadata hiện tại.
ĐÃ THỬ VÁ: không — không tự cấp ID packet T hoặc mở write set.
ĐÃ THỬ NGHIỆM: đếm bảng G write_set=2; đọc A8=3; tính composite2+1=3. Đọc ADR-0044 ⇒ trần3/300 theo packet, exclusion theo đường. Đối chiếu metadata/A9 bằng `rg` và `nl -ba`. rc=0.
ĐỘ TIN: cao

### so-ci-moi-chua-duoc-khai-la-thuat-lai-trong-spec  [P2]  Nhãn mới chưa thu hồi lời khẳng định rộng và phép ghép lượt vẫn còn
TỆP/DÒNG: G:82–90,200–209,240–241,680–687,962–966; T:42–55,187.
VẤN ĐỀ: G đã nhận duration+cancelled không phân biệt nguyên nhân hủy, nhưng vẫn tuyên bố mọi lượt master từ ~07-09 chưa hoàn tất và bốn lượt bị trần cắt. Hai run bổ sung chỉ có lời kể conclusion RUN, không run_id/job conclusion; không suy được Windows timeout từ đó. ≥22,7 ở G:202 cũng không neo run_id rõ. T:55 nói các số THUẬT LẠI phía trên cùng run34563553711 trong khi Ubuntu5,35 ở T:44 thuộc34552510232. Dùng số Ubuntu lượt khác trong mô hình có điều kiện không tự sai; khai chúng cùng lượt là sai và trái chốt T:187. Cách gắn nhãn C hiện đã đúng, không báo lại phần đó.
ĐÃ THỬ VÁ: không — không có quyền hay hiện vật để bổ sung các lượt CI thiếu.
ĐÃ THỬ NGHIỆM: `rg -n 'THUẬT LẠI|7,8|7,69'` G; đối chiếu bảng G:213–214 và T:42–55. KHÔNG ĐO ĐƯỢC CI gốc do không mạng/không log. Kiểm số N10+N11=60,22≤60,52 chỉ cho nhất quán nội tại.
ĐỘ TIN: cao

### benchmark-moi-thieu-hien-vat-neo-luot  [P2]  N7–N9 vẫn được bán như số tái lập offline dù đặc tả thừa nhận không có hiện vật
TỆP/DÒNG: `EVIDENCE.md` nhóm ĐO LẠI ĐƯỢC N7–N9; T:27–34,199–202; G:173–183,937,969–977.
VẤN ĐỀ: Đọc mã tái lập được cấu trúc gọi hai lượt, không tái lập được timing của lượt đã mất. Các số114,10/173,6,24,4/54,6,75,3/177 không có lệnh đầy đủ, rig, rc, mốc hay số ca từng lượt. T nói cùng lúc chúng tái lập offline và chúng không có hiện vật. Phép chia đúng không xác thực cặp tử/mẫu cùng lượt, chính lỗi review cũ đang đòi vá. Cận≥7,694915 sửa đúng nhưng hàng G:937 vẫn kể≥7,8 như số đo. Không kết luận timing sai; kết luận hồ sơ chưa chứng minh chúng.
ĐÃ THỬ VÁ: không — không thể tạo lại chứng cứ lịch sử bằng lượt benchmark mới.
ĐÃ THỬ NGHIỆM: Python chia lại tất cả N7–N9/N17, kết quả ở BẢNG ĐO. Đọc chua_do_duoc xác nhận chính executor khai thiếu hiện vật. Không chạy benchmark khác rig để thay số cũ.
ĐỘ TIN: cao

### lan-thu-ba-khong-cung-hinh-dang-tin-dung-gia  [P2]  Đã tách hai chiều nhưng đoạn kết vẫn dùng lần thứ ba để kích hoạt §12
TỆP/DÒNG: C:238–250,272–275.
VẤN ĐỀ: Bảng mới phân loại đúng: hai lần cấp tín dụng giả không cộng với một lần từ chối ghi công. Tuy vậy mục chua_do_duoc#4 vẫn bảo dòng đầu đếm3 và đặt câu trả lời đổi cách làm dưới §12. Đây chính là lỗi cũ còn nguyên tại nơi quyết định thẩm quyền, không phải một trường hợp mới cần slug khác. Khối lịch sử được kể ở C:241–245 đã gắn là r1; mục272–275 không có nhãn ấy và vẫn phát biểu ở hiện tại.
ĐÃ THỬ VÁ: không — chỉ kiểm sự nhất quán của phân loại và lời rút.
ĐÃ THỬ NGHIỆM: đọc nguyên C:231–275 và phần kế thừa trong CLAUDE.md; đếm bảng2/1 rồi đối chiếu câu “dòng1 đếm3”. Không cần dựng mutant hay tái chạy CI.
ĐỘ TIN: cao

### t125-do-buoc-khong-go-duoc-vong-nen-bi-cat  [P1]  A1 của packet tiền đề vẫn không có mẫu số hợp lệ trong chính ca cần chữa
TỆP/DÒNG: T:20–23,112–124,191–198; G:82–93,657–685,826–834.
VẤN ĐỀ: T A1 cấm dùng thời lượng bước chưa hoàn tất làm mẫu số và cho KHÔNG ĐO ĐƯỢC⇒ĐỎ. N11 và T:191 tự nói chính bước20 bị cắt ở26,25. Cách “bước có số đo riêng dù job bị cắt sau đó” chỉ áp khi bước đã xong; không áp được ca đang bàn. Đo bước sau bản sửa không đo được bước trước bản sửa, nên câu T:193–195 không tháo vòng tự phụ thuộc. Đầu A1 còn cấm mọi nền có job cancelled rồi sau đó lại cho ngoại lệ bước hoàn tất, cần đọc theo ngoại lệ hẹp; ngay cả đọc thuận lợi ấy vẫn không cứu bước20. G A1 hiện kiểm ngưỡng36 độc lập với nền trước, nên lý do tách vì CẢ A1/A5 cần nền trọn cũng quá rộng. T:197–198 cho phép gate còn timeout mà không coi thất bại; T hoàn thành vì thế chưa bảo đảm tiền đề A5 của G.
ĐÃ THỬ VÁ: không — không tự nới timeout hay thay hợp đồng nghiệm thu để phá vòng.
ĐÃ THỬ NGHIỆM: đối chiếu T A1 với N11/T chua_do_duoc#1 bằng đọc tệp. Phản mô hình là chính dữ liệu executor khai: step20 cancelled⇒mẫu số bị cấm⇒A1ĐỎ. KHÔNG ĐO ĐƯỢC thời lượng hoàn tất lịch sử; không gọi mạng.
ĐỘ TIN: cao về mâu thuẫn hợp đồng; dữ liệu CI đầu vào vẫn chỉ THUẬT LẠI

### uoc-bien-t125-sai-so-hang-va-sai-chieu-can  [P2]  Khoảng biên 3,74–8,68 không suy được từ những số đang ghi
TỆP/DÒNG: `EVIDENCE.md` N15–N16; T:46–55,191–204; G:87–90.
VẤN ĐỀ: T đã khai ƯỚC, nhưng phép tính vẫn sai: cộng33,97 +26,25/3,24 +5,35×h với h∈[1,73;2,35] cho job51,32735–54,64435 và biên5,35565–8,67265, không cho56,26 hoặc3,74. Không phải sai số làm tròn0,01. Thêm nữa26,25 là cận dưới của bước cũ; chia cho một hệ số giả định không tạo cận trên của bước mới. Đổi bước cũ thành một thời lượng lớn hơn vẫn phù hợp dữ liệu bị cắt và có thể làm job sau quá60. Hệ số2,35 cũng không phải “cận trên packet-loop” của bảng nguồn (max2,89; median2,37). Vì thế mệnh đề “⇒ chạy trọn” không được suy ra dù chấp nhận toàn bộ số THUẬT LẠI. Dự báo biên hết trong một tuần còn thiếu mô hình tăng trưởng; tăng2,24× trong4 ngày của hai phép đo không xác lập tốc độ tương lai.
ĐÃ THỬ VÁ: không — chưa có phép đo mới để chọn hệ số hay khoảng thời lượng có căn cứ.
ĐÃ THỬ NGHIỆM: Python tính `33.97 + 26.25/3.24 + 5.35*f` và lấy60 trừ kết quả, f=1.73/2.35. Tái tính mẫu11 TSV cho packet-loop ⇒ min1,88/max2,89/median2,37. Không dựng tải hoặc timing giả.
ĐỘ TIN: cao

### t125-doi-chung-co-cu-chua-chung-minh-than-ca-do  [P1]  Phản chứng của job mới chưa canh hai lượt A/B thật trong t125
TỆP/DÒNG: T:92–96,126–140,172–174; mã nền `cay-kho/ops/lease_publish_test.py:4015–4041,5368–5391`.
VẤN ĐỀ: A2(2) mạnh hơn kiểm có job: nó bắt một lệnh thay thế không gọi t125. Nhưng một bộ kiểm chỉ xác nhận lệnh được phép có thể qua phản chứng ấy mà không kiểm thân ca có chạy đủ hai suite con hay phép so verdict còn tác dụng. Hướng phản chứng bằng lời: giữ nguyên job và lệnh gọi t125, làm thân t125 trả về trước khi thực hiện A/B; báo t125 đạt ở job riêng và báo bỏ qua có lý do ở job chính. A3 vẫn phân biệt được hai chuỗi tổng kết; A8 vẫn có thể thấy đủ tên145+1; A1 vẫn đo main nhẹ hơn. Đối chứng với CO_AB chỉ chứng minh hai chế độ hạch toán khác nhau, không chứng minh job mới thực hiện hai subprocess, không chứng minh hai lượt cùng tập ca chỉ khác actor, và không chứng minh rò actor còn làm t125 đỏ. Mục ngoài phạm vi cấm hạ răng là đúng nhưng chưa có nghiệm thu chức năng khóa lời hứa ấy. Không gọi các A2/A3 là hằng-đúng: chúng đỏ được ở những lỗi hẹp đã nêu, nhưng chưa nghiệm thu được việc chuyển chính phép đo A/B.
ĐÃ THỬ VÁ: không — chưa có implementation bộ chọn ca/cờ mới để sửa hoặc thử.
ĐÃ THỬ NGHIỆM: đọc AST/luồng t125 và main: CO_AB return vẫn tăng qua; hai lời gọi luot mới thực thi phép đo actor. Đối chiếu tất cả T A1–A8 không thấy phản chứng làm lệch actor hoặc bỏ một lượt A/B qua job riêng. KHÔNG ĐO ĐƯỢC cờ mới; chỉ mô tả phản chứng bằng lời.
ĐỘ TIN: vừa

### bang-gom-bo-sot-cac-khang-dinh-kiem-duoc  [P3]  N1–N17 vẫn chưa kê các số hạng và nghĩa vụ đã đổi theo revision
TỆP/DÒNG: `EVIDENCE.md`, mục SỐ MỚI và TRẦN CỦA BẠN; C:101,216–218,268–275; G:774–775,806–807,847–848,870–873; T:142–150.
VẤN ĐỀ: Bảng gom không kê được các khẳng định kiểm tại chỗ mà review này đã đo: số tệp đúng2 so A8đòi3, số job1→2→4, mỗi lần thêm1/2, số ca mới≥8 so dự toán5, số assert14 so cuối tệp16, bộ hệ số tạo N16, và số2/1 so lời kích hoạt3. Các lỗi có tác động đã tách ở finding trên, không cộng lần thứ hai vào số P1/P2. Các khẳng định bổ sung khớp cũng được ghi trong BẢNG ĐO: OID/blob/delta,146 ca/118 receipt, TSV và mẫu11, lịch sử timeout, phân rã chi phí, consumer Ruff, số dòng/nhắc mutant. Thiếu định tính bổ sung: T A4 hứa một allowlist tên bước literal “khai thẳng trong đặc tả này” nhưng chưa đưa danh sách có tên chính xác và ánh xạ mỗi nền; nhánh nền hỏng chỉ cấm cancelled, không đòi skipped có lý do như G A2. Việc có thể kiểm tên không đồng nghĩa phép chiếu đã được đặc tả đủ để hai người thi công giống nhau.
ĐÃ THỬ VÁ: không — chỉ bổ sung danh mục đo vào verdict theo yêu cầu, không sửa EVIDENCE.
ĐÃ THỬ NGHIỆM: các lệnh Git/AST/YAML/CSV/số học đã liệt kê dưới BẢNG ĐO; tất cả phép đọc/đo cục bộ rc=0. Không nhận n19 Ubuntu là sai chỉ vì mẫu bàn giao có13; không nhận mẫu12 Windows là đối chứng cho bảng11.
ĐỘ TIN: cao

Không báo lại `thu-hoi` đỏ. Đọc `cay-kho/.github/workflows/ops-thu-hoi-admission.yml` thấy `pull_request_target` và checkout `github.event.pull_request.base.sha`, phù hợp cơ chế biên bản mô tả. Không có bằng chứng cục bộ bác lập luận ấy; tình trạng PR505/comment5630646283 chưa xác minh trực tiếp và không được nâng thành đã xác minh.
