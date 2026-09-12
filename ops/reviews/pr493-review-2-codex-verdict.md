verdict: changes_requested
reviewed_sha: 9484970f269e09fd9cace3432c19cb90e854c93c

**CÒN P1.** Bản vá đổi cảnh báo thành 11, nhưng README:278 vẫn khai “13 finding … + 5 của bot còn sống lúc merge”; receipt:46 vẫn khai “3 P2 + 10 P3 còn sống lúc merge”. Mâu thuẫn lượt 1 chưa đóng. Kết quả: **1 P1 · 4 P2 · 15 P3** (12 P3 cũ, 3 P3 bỏ sót mới). Không suy cổng xanh thành nội dung đúng hoặc quyền merge.

Reviewer: GPT-6/Codex theo chỉ dẫn phiên; provider OpenAI; execution surface API có shell cục bộ; transport machine. Khác provider executor Claude theo hồ sơ được giao; không có chứng thực độc lập biến thể model/backend. Review trên exact SHA nhánh nháp được người dùng chỉ định; không giả nhận đây đã là head nhánh PR thật. Tree: `5ada023a62738ab69026ccb1ce521b377ab1a5d7`. Không mạng, không push/commit/merge, không tự soạn payload đường dẫn. `cay-kho/` giữ sạch; cổng và đột biến chạy ở `review-current/`, `review-before/`, tệp tạm trong workspace. `actionlint 1.7.7` được thêm bằng THƯ MỤC vào CUỐI PATH; `core.abbrev=7` trên hai bản sao.

Mọi đường dẫn kho dưới đây tương đối với `cay-kho/`; `than-pr-493.md`, `muc-*.md`, bảng và verdict lượt 1 là hiện vật ngoài kho trong workspace. Bằng chứng tự chạy: `review-evidence/measurements.json`, `extra.json`, `gates.json`, `mutations.json`, `omitted.txt`, `rebuilt-table.txt` và các log `.out`. Lệnh đo có trong `measure.py`, `run-gates.py`, `mutate.py`. Một lần mock t33 đặt sai namespace trả AttributeError; không tính là phép đo t33. Lần sửa đúng `patch('shutil.which')` trả AssertionError tiền điều kiện, 0 subprocess (`t33-corrected.out`).

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `no-luc-merge-dem-ca-hai-p2-da-dong`: **VÁ HỜ** — parse verdict = 3 P2 + 10 P3; parse receipt có đúng hai `da_va: true`. ID mới và ô cảnh báo cùng ghi 11, t27 PASS; nhưng receipt:46 và README:278 vẫn khẳng định 13 lúc merge. `13−2=11` chỉ đúng theo attestation sửa thân PR491; không có bản đọc ngược/JSON PR491 để chứng minh hai sửa chữa ấy.
- `nhan-nguon-van-va-than-de-nguyen-khung`: **VÁ HỜ** — CHANGELOG:176 đã ghi BA loại, bảng 6 hàng có hàng đầu 3 ca và nhãn theo ca tại 241–254 đã sửa đúng. Nhưng định nghĩa (a):181 vẫn bao “mọi số Git”, chính 337–339 vẫn bác nó; 275–278 vẫn kể ba lượt không nhãn, 353–357 vẫn gọi probe là đo được. Tiêu đề NĂM đã vá và thân PR vẫn vượt phần đã đóng.
- `dong-chin-p3-khong-deu-can-bo-trich-moi`: **VÁ HỜ** — đọc đủ 10 finding P3 gốc xác nhận 8 lỗi lọc + 1 thiếu input + 1 giới hạn cổng; đoạn 108–125 sửa đúng. Receipt:103–107 và thân PR493:52 vẫn hoãn cả nhóm thiếu input sang công cụ mới. Không có lỗi số học mới trong 8+1+1; lỗi là sửa chưa đồng bộ.
- `nhan-attestation-khong-di-cung-ban-tom-tat`: **VÁ HỜ** — CHANGELOG:53,60–64 có nhãn mới thật; thân PR493:17–28 vẫn giữ các số CI và “ĐO được” không mang nhãn thiếu response. Tái đọc nguồn land evidence có nhãn ở đầu; tìm trong thân PR không thấy nhãn tương ứng cho CI/approval.
- `suy-mat-ref-thanh-mat-object-tuc-thi`: **VÁ HỜ** — đoạn 331–340 sửa đúng giới hạn clone tương lai; tự chạy ancestry rc1, `for-each-ref --contains` vẫn trả đúng 2 ref. Câu “số chết khi nhánh … bị xoá” còn ở CHANGELOG:99, README:19, receipt:121, thân PR493:45.
- `hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap`: **CHƯA VÁ** — git diff giữ nguyên hai tự thuật ở CHANGELOG:84–88,159–165; không có bản nháp 8 hoặc log checkout/verifier 806980/806981. Blob trước/sau đo 809136/815113 byte, không phải chứng cứ bác một bản nháp chưa commit.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — tự đổi đúng 1 byte, size vẫn 815113: release rc2; đổi 1016→1017, tiêu đề 5→6 hoặc phép trừ mới thành 13−2=12: claims đều rc0/ok=true. Phục hồi byte gốc; cổng không đổi mã.
- `bo-sot-pham-vi-ref-va-vat-chat-hoa`: **CHƯA VÁ** — tái tạo bảng ba input bằng byte; CHANGELOG:231,233–236 không chữ số vẫn rơi, gồm giới hạn heads/namespace và vật chất hóa. Snapshot 319/319/319 không biến thành mọi namespace.
- `bo-sot-tu-khai-evidence-va-manifest`: **CHƯA VÁ** — CHANGELOG:236–237 vẫn không được trích: sinh EVIDENCE, cách trích/phần bỏ sót và manifest. Tự băm 3207/3207 hiện vật khớp, không chứng minh sự kiện sinh gói.
- `bo-sot-pham-vi-nen-chua-do`: **CHƯA VÁ** — CHANGELOG:357 không số và còn nằm ngoài slice mới (kết thúc340). Giới hạn Linux+Bash/chưa macOS/Windows native nguyên nghĩa; không đo được hai nền đó.
- `bo-sot-nguong-hai-client`: **CHƯA VÁ** — CHANGELOG:368–369 vẫn ngoài input và không chữ số; đọc CLAUDE:580–581 xác nhận ngưỡng ít nhất hai client. Không gọi mạng.
- `bo-sot-pham-vi-r-va-hai-sentinel`: **CHƯA VÁ** — CHANGELOG:356–357 không chữ số và ngoài input; phạm vi R chính nó/cả hai sentinel vẫn mất. Không dựng probe mới. Hậu quả động KHÔNG ĐO ĐƯỢC từ log được giao.
- `bo-sot-input-than-pr-va-duoi-r358`: **VÁ HỜ** — ba input thật, thêm đủ 40 dòng có số của thân PR493; nhưng hai slice là CHANGELOG:1–150 và151–340, trong khi r359=1–166, r358=167–390. Còn thiếu341–390, **50 dòng**, thay vì32 dòng cuối ở lượt trước; r359 vẫn bị cắt sang slice mang tên r358.
- `bo-sot-hop-dong-phan-loai-nguon`: **CHƯA VÁ** — định nghĩa nguồn đã đổi thành ba loại nhưng bảng vẫn bỏ176,179–185,187 (không chữ số), chỉ giữ các mảnh có số khác. Không còn toàn hợp đồng để kiểm lời hứa nhãn tại chỗ.
- `bo-sot-dieu-kien-chot-so-ci`: **CHƯA VÁ** — CHANGELOG:310–312 đều không số, bị bỏ. Thân PR:19 được trích có `completed` và 0, nhưng không thay thế quy tắc đầy đủ `in_progress ⇒ KHÔNG ĐO ĐƯỢC` và giới hạn suy nguyên nhân.
- `bo-sot-gioi-han-du-lieu-run-json`: **CHƯA VÁ** — CHANGELOG:382–389 ngoài slice; riêng384,389 cũng không số. Parse hai run.json vẫn 35 khóa cấp cao/3 khóa lenh; thêm thân PR493 không đưa đoạn này vào bảng.
- `bo-sot-dieu-kien-kich-hoat-workflow`: **CHƯA VÁ** — CHANGELOG:43,47–49 vẫn bị bỏ. Thân PR493 bổ sung một phần điều kiện qua dòng có số, nhưng dòng về `ready_for_review` không số vẫn rơi. Đọc YAML xác nhận hai workflow có tập sự kiện khác nhau.

Tổng đối chiếu: **6 VÁ HỜ · 11 CHƯA VÁ · 0 ĐÃ VÁ THẬT · 0 VÁ SINH LỖI MỚI** ở cấp toàn finding cũ. Những phần đã sửa đúng vẫn được ghi nhận ở trên; không gọi cả finding đóng khi còn phản ví dụ trong phạm vi gốc.

## BẢNG ĐO

“Có” cho nội dung Git/tệp không chứng minh sự kiện GitHub. Các run ID, timestamp API, danh tính approve và thời lượng lịch sử được đối chiếu với lời khai nguồn nhưng **KHÔNG ĐO ĐƯỢC độc lập** offline. Các dòng cùng khẳng định lặp trong ba hiện vật được gộp; số hiệu PR, ngày và số dòng dùng làm địa chỉ không tự trở thành số lượng.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact SHA/tree | 9484970… | đủ OID như đầu verdict; cây sạch | Có |
| Toàn PR/base | diff.patch, numstat | 8 tệp, +1260/−22; diff byte bằng Git | Có |
| Vá giữa hai lượt | prompt nói thêm ~238 dòng CHANGELOG | +78/−20 CHANGELOG; tổng4 tệp +92/−30, CHANGELOG tăng58 dòng/5977 byte; patch byte bằng Git | Không với mô tả ~238, không quy thành finding của nội dung kho |
| Mã thực thi đổi | không | 8 tệp chỉ hồ sơ, CHANGELOG, manifest; delta lượt2 không sửa mã cổng | Có |
| Toàn vẹn hiện vật | ARTIFACTS.sha256 | 3207/3207 đúng băm | Có; không chứng thực provenance |
| Ref snapshot |319/319/319, lệch0/0| ba TSV bằng byte; heads trong git=319; không shallow | Có tại snapshot, máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Root repo |394e934…|394e93468fc8d84ec20938e6df8fb7ab72b2cc37|Có|
| Chuỗi PR |7, #486 trước #480|first-parent: #468,#477,#478,#486,#480,#487,#489|Có|
| Payload |1016 tệp,+247458 dòng,1 thư mục cấp 1|git diff đúng cả ba, tập cấp 1={ops}|Có|
| Land evidence |6 trước, thêm thứ7|ls-tree c0a5cbe=6,00e017a=6,HEAD=7|Có|
| Head PR491 được merge |2ec6171f…|cha thứ2 merge00e017a đúng OID receipt lượt2|Có quan hệ Git; approval không suy từ cha merge|
| Mốc merge |2026-09-09T17:24:54Z API|Git committer 17:24:53Z, khác trường API merged_at|KHÔNG ĐO ĐƯỢC merged_at; không gọi chênh1 giây là sai|
| Verdict PR491 lượt1 |3 P1/5P2/6P3,14|regex toàn tệp và heading đúng 14|Có|
| Verdict PR491 lượt2 |0P1/3 P2/10 P3,13|regex toàn tệp và heading đúng 13|Có|
| Đối chiếu PR491 |14=7+1+0+6,3 P1 đã vá|đếm marker7/1/0/6; ba slug P1 thuộc nhóm thật|Có về verdict nguồn|
| Verdict PR493 lượt1 mới tự khai |1P1/4P2/12P3|đếm heading VERDICT-LUOT-1.md=1/4/12|Có,17 finding; nhóm năm là P1+P2|
| Năm finding đều lời khai “CHÍNH mục này” |tiêu đề mới|P1 nằm receipt/README; nhãn CI còn thân PR; thân đoạn có nói rộng hơn “hiện vật phiên viết”|Tiêu đề hẹp hơn phạm vi bằng chứng; chi tiết nguồn xem P2 nhãn|
| Tự thú P2 nhãn chỉ hai lỗi |khung2/3, nhãn hàng/ca|đúng hai phần ấy nhưng finding gốc còn ba lượt t33 và probe không nhãn|Tự thú chưa bao trọn; không coi là đã đóng|
| Bốn lời khai rộng +1 mâu thuẫn |4+1|đọc năm finding trước đúng cách gom; không phải5 lỗi mã|Có phân nhóm khái quát, không chứng minh vá xong|
| Hai verdict nguyên byte |35088/36958|đúng size, hash đúng receipt; Git diff lượt2 không đụng verdict|Có|
| SHA256 verdict1 |38d7fb2e…|38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c|Có|
| SHA256 verdict2 |14c726e5…|14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468|Có|
| Commit đầu chứa verdict |34e9d35…|log --diff-filter=A cả hai=34e9d35be0fc52406e3659bfc24c388bf54262cd|Có|
| Caveat/mục lục |4+5=9,2 hàng verdict|receipt đúng4/5 ID; t27 PASS kiểm đúng ô bảng|Có hình thức|
| ID caveat mới |11-con-song-luc-merge|cùng ID trong receipt và README; sai ID một phía làm t27 đỏ|Có đồng bộ; con số11 vẫn có tiền đề attestation|
| Nợ lúc merge |caveat11; nơi khác13+5|13 lúc review, đúng2 da_va:true; phép trừ=11; receipt46/README278 vẫn13|Không, CÒN P1|
| Hai P2 đã sửa trước merge |sửa thân PR491, diff0 dòng|verdict cho đúng hai slug; không có raw body/readback PR491. than-pr-493.md là PR khác|KHÔNG ĐO ĐƯỢC sự kiện; phải nhãn attestation|
| Bot |5P2,3 mới,2 trùng;4 đúng/1 một phần|receipt có5 mục,3 moi:true,2 moi:false và đúng4/1 kết luận|Có với hồ sơ tự khai; review API KHÔNG ĐO ĐƯỢC|
| Phép đếm năm sửa r358 |1 của lượt2+4 bot,bot as-of trùng|5 đối tượng: nhãn nguồn,neo spec,gói,#490,ref; bot ref giao với P3 về bảng nhưng sửa lời khai khác sửa bảng|Có5 đối tượng, chưa phải5 đóng sạch|
| Phân hoạch10 P3 PR491 |8+1+1 mới;9+1 cũ còn chỗ khác|đọc đủ8 bo-sot về regex,1 bo-sot-toan-than-pr về input,1 cổng|8+1+1 đúng; hoãn cả9 còn sai|
| Thân PR được cấp cho script |đầu vào3 hiện vật|script cả3 tái tạo BANG bằng byte; 71+96+40=207 dòng có số|Có; không đồng nghĩa đủ mệnh đề|
| Đóng thiếu input |thêm thân PR|đóng phần bỏ toàn thân PR493:40 dòng có số; không phục hồi body PR491 lịch sử; thiếu đuôi r358 50 dòng|Một phần|
| Ranh giới slice |muc-r359 / muc-r358|thực1–150/151–340; heading r358=167,r356=391|Sai ranh giới, thiếu341–390|
| Quy tắc regex |ít nhất1 chữ số|đúng mã re.search; mệnh đề bằng chữ vẫn giữ nếu cùng dòng có số khác|Có đoạn sửa; docstring script còn diễn đạt quá rộng|
| Số loại nguồn |BA|có(a)(b)(c); (a) vẫn “mọi số Git”, (c) lại là ngoại lệ Git|Đếm3 đúng; phạm vi chưa nhất quán|
| Bảng builder |6 hàng,đầu3 ca|6 hàng dữ liệu,8 ca khi tách đầu; nguồn theo ca hiện bao đủ|Có về cấu trúc|
| Builder rc |4/5/6/4/4/0,mirror1,lệch304/304,giả42|mã/nguồn thuật lại có các ca; không chạy builder có mạng, không tự dựng probe đường dẫn|KHÔNG ĐO ĐƯỢC các sự kiện động lịch sử|
| Công cụ ghim |chỉ actionlint1.7.7,3 công cụ tin PATH|đọc builder/installer phù hợp; bản gói1.7.7 chạy được với shellcheck0.9.0|Có cấu trúc và môi trường hiện tại; không chứng thực installer cũ|
| Manifest c0a5cbe→2ec6171 |8075509→8089302,bcde19d5→d47be343|đọc hai blob đúng;180 mục,ops=0,CHANGELOG có trong kê|Có|
| Manifest lượt1→lượt2 PR493 |8103458→8109435|đúng; tăng5977 bằng tăng CHANGELOG809136→815113|Có|
| Package hash hiện tại |ebd706cb…|ebd706cb9e84f42f657ab455c0c35a2153ef1076e74ed4f1eeb97d789558c250|Có, release xác minh|
| VERSION |1.36.68,không nâng|VERSION1.36.68,không trong delta PR|Có trong phạm vi PR; không tái kiểm từng r337–r356|
| Release strict hiện tại |180/180,ok=true|rc0;failed/errors/extra rỗng;self_match và hash_match true|Có|
| Claims strict hiện tại |ok=true|rc0,ok=true|Có, không đo số thật|
| Lease hiện tại |121/121,chạy121,bỏ0|rc0,đúng 121/121,chạy121,bỏ0|Có|
| Receipt hiện tại |43v2,tổng96,0 vi phạm|43v2+11legacy+42nợ=96;0 vi phạm;0 KHÔNG ĐO ĐƯỢC,rc0|Có|
| Cả4 cổng xanh trên bản sai4af7e29 |release,claims,lease,receipt đều xanh|tự chạy đủ4:rc0/0/0/0;lease121/121;receipt43+11+42=96|Có; không suy mỗi cổng có nhiệm vụ kiểm mọi câu văn|
| Cả4 cổng trên9484970 |xanh|tự chạy đủ4:rc0/0/0/0|Có, P1 vẫn tồn tại|
| Răng byte |1 byte làm đỏ|đổi đúng 1 byte,size 815113 không đổi:rc2,failed chỉCHANGELOG,hash_match=false|Có; khôi phục byte gốc|
| Răng claims |không bắt1016→1017|mutant1017,title5→6,13−2=12 đều rc0/ok=true|Có giới hạn, kể cả số mới|
| t26/t27 |băm/ID phải khớp|control PASS;verdict thêm newline⇒t26 AssertionError;ID chỉREADME đổi⇒t27 AssertionError|Có răng hình thức|
| t27 kiểm số trong ID |ID11|đổi cùng hai nơi sang12⇒t27 PASS|Không kiểm nghĩa11/12; không coi là lỗi mới của cổng|
| t33 vắng công cụ |AssertionError,0 subprocess|mock đúng namespace:AssertionError,call_count0|Có; hàm đã chạy,lint chưa chạy|
| Số ba lượt sai t33/fourth |3 trước+1 thân PR|nguồn có lời tự khai,thiếu chuỗi3 verdict gốc để đếm độc lập|KHÔNG ĐO ĐƯỢC số lịch sử|
| doctrine/adr |rc0/rc0|7 tệp,0 chép doctrine;46ADR/46 hàng,rc0/0|Có|
| OID ngoài canonical |bd32d114 không ancestor2ec6171|merge-base rc1|Có|
| Ref chứa OID mới |2|refs/heads/claude/spec-thu-hoi-lease-va-cap-lai-20260907 và refs/remotes/mirror-cuc-bo/claude/spec-thu-hoi-lease-va-cap-lai-20260907|Có; không chứng minh xóa nhánh là mất object|
| Spec ở bd32d114 |revision9,packet_issue neo ở Issue,lượt8=lời gọi9,0P1/1 P2 S11|đọc spec-r9.md và luot8-VERDICT.md tại OID đúng các giá trị|Có nội dung; authority Issue/lease KHÔNG ĐO ĐƯỢC|
| Thứ tự thời gian Git |bd32d11 11:23:01Z trước ba4a25816:10Z|git show đúng|Có Git; không chứng minh thời điểm tạo PR|
| _kiem_bia_mo |any tại 606|đọc mã đúng;lease suite chạy các ca sẵn có|Có mã; không tạo payload mới|
| Nợ A9 |4 mốc cấp,4 hash,r1/2/3/4,generation1,trước14:30:07|land evidence468/478 lặp đúng các mốc03:37:33/07:50:35/09:44:51/10:17:12;so giờ đều trước hạn|Khớp nội dung và số học; chưa tái kiểm từng blob lease liên ref lượt này|
| Run.json14/15 |35 khóa;lenh 3|parse đúng35 và{chuong_trinh,so_doi_so,van_tay}|Có cấu trúc; không chứng thực model|
| Cận dưới20 finding |ít nhất20|trích98 slug khác tên trong các verdict PR468/477/478/480/486/487/489;extra.json lưu20 nhân chứng|Có cận dưới, không coi98 là kiểm kê lỗi độc lập đầy đủ|
| 1/6 stdout tự đếm;4 lượt hờ;6 mục lỗi #477 |lời nguồn thuật lại|nguồn land evidence ghi các số ấy;không có đủ stdout/verdict/probe gốc để đo chuỗi lịch sử|KHÔNG ĐO ĐƯỢC độc lập;6 mục không phải6 lần độc lập|
| Ubuntu CI merge |44=40+4;20m38s,0hỏng/null|phép cộng44,thời lượng1238s;YAML40 bước khai báo không bằng44 bước API gồm bước hệ thống|Số học đúng;sự kiện KHÔNG ĐO ĐƯỢC|
| Windows CI merge |44=38+6;49m09s,0hỏng/null|phép cộng44,thời lượng2949s|Số học đúng;sự kiện KHÔNG ĐO ĐƯỢC|
| Biên Windows |10m51s dưới60,hẹp hơn11m45s|3600−2949=651;3600−2895=705;hẹp54s|Có số học;2 điểm không chứng minh xu hướng|
| CI cũ #477 |44/44,26m46s/48m15s|nguồn có số này;1606/2895 giây;không raw run/job|KHÔNG ĐO ĐƯỢC sự kiện|
| Nguyên nhân43/4 |chưa xác định;43/1→44/6 khác run|nguồn ghi CHƯA XÁC ĐỊNH;34176439015 khác34169756563;1 khác4|Có nội dung và số học;không chứng minh giả thuyết nguyên nhân|
| Approval/3 đỏ1 xanh/Windows đầu tiên |các ID trong thân PR/land evidence|không JSON thô;chỉ đối chiếu lời tự khai|KHÔNG ĐO ĐƯỢC độc lập|
| Cấu hình cò CI |pull_request không types,push master,Windows có điều kiện,trần60|đọc YAML khớp;workflow duyệt có4 types ở pull_request_target và2 ở pull_request_review|Có cấu hình;không xác minh event server offline|
| edited không bắn/cdd0b1d0gate |sự kiện lịch sử|không có run JSON;lời “GitHub không phát pull_request cho edited” rộng hơn cấu hình tệp không đăng ký|KHÔNG ĐO ĐƯỢC lịch sử;giới hạn nhận định vào workflow này|
| Hai runtime PR491 |696/714s,rc0|receipt có scalar/timestamp tự khai;không run.json gốc|KHÔNG ĐO ĐƯỢC runtime độc lập|
| Tự thú mất vá |806980→806981,checkout mất sửa|không bản nháp/log;byte Git không tái dựng trạng thái chưa commit|KHÔNG ĐO ĐƯỢC;không gọi là bịa|
| Tự thú đếm8 |8,bốn nhóm,cộng nhầm2,lần2 phiên|không bản nháp8/transcript;5+2=7 chưa đủ tái dựng8|KHÔNG ĐO ĐƯỢC nguyên nhân/tần suất|
| Bài học có sẵn |trích CLAUDE|câu bom hẹn giờ tại 692;ngưỡng2client tại580–581|Có văn bản;không chứng minh phiên đã đọc|
| Trạng thái463–467/479/490 |open/chưa merge|chỉ có attestation;không hỏi server|KHÔNG ĐO ĐƯỢC hiện trạng|

### no-luc-merge-dem-ca-hai-p2-da-dong  [P1]  Đổi caveat sang 11 nhưng để nguyên số 13 lúc merge trong khung hồ sơ
TỆP/DÒNG: ops/reviews/README.md:18,278; ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:7,46,83–98,190–198.
VẤN ĐỀ: Cảnh báo mới nói11 và cấm cộng11+5, trong khi hàng mục lục vẫn “13 finding … +5 … còn sống lúc merge”; trường khong_suy_rong vẫn3 P2+10 P3 lúc merge. Đây đúng mâu thuẫn P1 lượt1, không phải trích dẫn verdict nguyên văn. Header receipt cũng giữ “13 finding còn sống” không mốc. Hai da_va:true đều về thân PR491; phép trừ11 hợp phạm vi nếu nhận attestation ấy, nhưng thiếu raw body/readback để chứng minh sự kiện. ID11 đã đồng bộ và số11 không sai số học; nó vẫn đang trình bày kết luận có điều kiện như sự thật đã kiểm.
ĐÃ THỬ VÁ: không — cần đổi mọi câu về nợ lúc merge ở README/receipt, gắn nhãn “theo attestation hai P2 đã sửa”; giữ13 cho lúc review và tách bot khỏi tổng lỗi phân biệt. Không sửa verdict nguyên văn.
ĐÃ THỬ NGHIỆM: measure.py đếm13 heading,parse đúng2 da_va:true; tự đọc cả ô cảnh báo và ô mục lục. t27 control rc0;ID lệch một nơi rc1;ID cùng đổi11→12 rc0. Cổng không bác được mâu thuẫn này.
ĐỘ TIN: cao

### nhan-nguon-van-va-than-de-nguyen-khung  [P2]  Khung ba nguồn vẫn bao mọi số Git và bỏ nhãn ba lượt t33
TỆP/DÒNG: CHANGELOG.md:82–98,130,139–142,176–187,275–278,337–339,353–357; than-pr-493.md:41–43.
VẤN ĐỀ: Thêm loại(c) nhưng định nghĩa(a) vẫn “mọi số Git…ai đọc cũng tái đo được từ kho”; đoạn337 tự bác chính câu ấy. Ba lượt t33 vẫn thiếu nhãn tại chỗ. Probe ở353–357 vẫn “đo được/đo:” dù nhãn xa ở254 thừa nhận không log động. Phần tự thú “hai lỗi trong một” kể khung và hàng/ca nhưng không kể các phản ví dụ còn sống này; tiêu đề NĂM đã vá vẫn quá rộng. Tiêu đề tự thú “CHÍNH mục này” cũng không bao đúng P1 thực ở receipt/README.
ĐÃ THỬ VÁ: không — thu hẹp(a) theo nguồn khả dụng/canonical, gắn nhãn ngay số ba lượt và probe; cập nhật tiêu đề, thân PR và tự thú theo phạm vi thực. Phần bảng6 hàng/8 ca đã đúng, không cần đảo lại.
ĐÃ THỬ NGHIỆM: đọc finding gốc và khối mới,đếm6 hàng/3 ca hàng đầu;mock t33 xác nhận AssertionError/0 subprocess nhưng không chứng minh ba lượt lịch sử. Hai ref OID không canonical được đo trực tiếp.
ĐỘ TIN: cao

### dong-chin-p3-khong-deu-can-bo-trich-moi  [P2]  Phân hoạch mới đúng nhưng receipt và thân PR vẫn hoãn sai phần thiếu input
TỆP/DÒNG: CHANGELOG.md:108–125; ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:99–107; than-pr-493.md:52.
VẤN ĐỀ: 8+1+1 đúng với10 P3 nguồn PR491. Tuy nhiên receipt vẫn nói đóng cả nhóm đòi bộ trích mới; thân PR vẫn “đóng chín cái đầu” đòi công cụ văn xuôi. Thêm input đã thực hiện được bằng script cũ ở gói này càng trực tiếp bác lời hoãn. Không nhầm tám lỗi regex gốc với lỗi thiếu đuôi input mới của PR493; đó là hai phạm vi review khác nhau.
ĐÃ THỬ VÁ: không — đồng bộ phân hoạch và cách xử lý ở receipt/thân PR; cấp đủ đoạn nguồn không cần đợi cổng mới. Một bộ trích mới có thể là giải pháp lâu dài, không phải điều kiện cần để bổ sung các mệnh đề cụ thể hôm nay.
ĐÃ THỬ NGHIỆM: đọc đủ10 P3,đếm9 slug bo-sot,phân loại8 lọc/1 input;script3 input bằng bảng,thêm40 dòng số PR493. Nguồn PR491 ghi33 dòng số thêm khi cấp body thời đó; không lấy40 của PR493 giả làm33 của PR491.
ĐỘ TIN: cao

### nhan-attestation-khong-di-cung-ban-tom-tat  [P2]  CHANGELOG thêm nhãn nhưng thân PR vẫn trình bày CI như đo độc lập
TỆP/DÒNG: CHANGELOG.md:51–64; than-pr-493.md:13–28; ops/land/pr491-r358-ghi-so-land-evidence.yaml:7–10,183.
VẤN ĐỀ: Nhãn mới trong CHANGELOG thật sự có ích, nhưng body được giao vẫn có “ĐO được”,3 đỏ/1 xanh,44 bước,thời lượng và Windows đầu tiên mà không mang giới hạn thiếu response thô. Dẫn tên khong_do_duoc không thay thế nhãn nguồn ngay nhóm số. Không khẳng định số CI sai; finding là cấp chứng cứ bị nâng ở bản tóm tắt. “Cùng nhãn … mục CI trên” tại53 còn trỏ ngược trong khi mục CI nằm dưới.
ĐÃ THỬ VÁ: không — gắn nhãn attestation cùng liên kết nguồn ngay nhóm approval/CI trong body; giữ phép cộng/thời lượng tự tính riêng.
ĐÃ THỬ NGHIỆM: đọc cả ba hiện vật;nhãn thiếu raw có ở land evidence và CHANGELOG,không ở nhóm CI body;phép cộng44 và biên651s đúng. Raw API KHÔNG ĐO ĐƯỢC vì không được giao và cấm mạng.
ĐỘ TIN: cao

### suy-mat-ref-thanh-mat-object-tuc-thi  [P2]  Đính chính dưới mục nợ nhưng vẫn khẳng định xóa nhánh là số chết ở bốn chỗ
TỆP/DÒNG: CHANGELOG.md:99,331–340; ops/reviews/README.md:19; ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:121; than-pr-493.md:45.
VẤN ĐỀ: Đoạn mới phủ nhận suy luận xóa ref làm mất object tức thì, nhưng bốn chỗ khác tiếp tục dùng suy luận ấy như kết luận hiện hành. Đó không phải câu cũ được trích để bác. Hai ref chứa OID khớp số mới; cảnh báo clone tương lai là hợp lý, không chứng minh khả năng thu gom object máy chủ.
ĐÃ THỬ VÁ: không — thay bốn lời khẳng định còn lại bằng giới hạn bảo đảm clone canonical tương lai; giữ phân biệt reachability,ref,object và nguồn snapshot.
ĐÃ THỬ NGHIỆM: merge-base --is-ancestor rc1;for-each-ref --contains trả2 ref như bảng đo. Không xóa ref hoặc dựng payload; không đo GC server.
ĐỘ TIN: cao

### hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap  [P3]  Hai tự thú vẫn thiếu bản nháp và log để kiểm độc lập
TỆP/DÒNG: CHANGELOG.md:84–88,159–165; than-pr-493.md:56–59.
VẤN ĐỀ: Không có log checkout, kết quả verifier806980/806981 hoặc bản nháp tiêu đề8. Cộng hai vào năm cho7, chưa tái dựng được8; “lần thứ hai trong cùng phiên” không đếm được từ Git. Thiếu chứng cứ không chứng minh tự thú sai.
ĐÃ THỬ VÁ: không — gắn nhãn tự thuật chưa có nguyên liệu; cung cấp log/bản nháp nếu còn, không lấy số blob đã commit làm số bản nháp.
ĐÃ THỬ NGHIỆM: git diff4af7e29..9484970 giữ nguyên hai đoạn; manifest/blob lần lượt809136/815113 byte. Đọc CLAUDE:692 khớp bài học. Sự kiện và tần suất KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Các số sai vẫn qua claims dù cổng byte và receipt có răng
TỆP/DÒNG: CHANGELOG.md:1,136; scripts/tl.py; RELEASE_MANIFEST.json.
VẤN ĐỀ: Giới hạn cũ còn nguyên: claims không kiểm phép đếm5 hay phép trừ mới11. Release kiểm toàn vẹn và t27 kiểm liên kếtID, không chứng nhận sự thật văn xuôi. Đây làP3 giới hạn đã biết, không phảiP1 thiết kế cổng.
ĐÃ THỬ VÁ: có — đột biến nội dung trên review-current rồi phục hồi nguyên byte; không tái sinh manifest.
ĐÃ THỬ NGHIỆM: release-exactly-one-byte.out: đúng 1 byte đổi,size 815113,rc2,failed chỉCHANGELOG,hash_match=false. Mutant1017,title6,13−2=12 đều claims rc0. t26/t27 mutant hình thức đỏ; cùngID12 hai nơi t27 vẫn xanh. Cây bản sao sạch cuối đo.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-pham-vi-ref-va-vat-chat-hoa  [P3]  Bảng tiếp tục bỏ phạm vi branch head và bước vật chất hóa
TỆP/DÒNG: CHANGELOG.md:231,233–236; trich_khang_dinh.py:15–18.
VẤN ĐỀ: Các dòng không chữ số chứa phạm vi heads, thiếu tag/namespace vẫn thành công và vật chất hóa ref bị bỏ. Một dòng chứa PR491 được giữ không thay thế các mệnh đề phạm vi ấy.
ĐÃ THỬ VÁ: không — bổ sung cả mệnh đề phạm vi cùng nguồn; không đổi snapshot heads thành mọi ref.
ĐÃ THỬ NGHIỆM: python3 trich_khang_dinh.py muc-r359.md muc-r358-da-va.md than-pr-493.md tái tạo byte bảng. omitted.txt ghi các dòng trên; ba TSV319 bằng nhau. Namespace máy chủ KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-tu-khai-evidence-va-manifest  [P3]  Bảng tiếp tục bỏ hợp đồng sinh evidence và manifest
TỆP/DÒNG: CHANGELOG.md:236–237; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Việc sinh EVIDENCE có cách trích/phần bỏ sót và lập manifest nằm trên dòng không chữ số nên mất khỏi bảng. Băm đúng không thay cho lời khai hợp đồng đầu ra.
ĐÃ THỬ VÁ: không — đưa toàn mệnh đề hợp đồng vào bảng và giữ giới hạn provenance.
ĐÃ THỬ NGHIỆM: measure.py tái trích bằng byte và băm3207/3207 đúng. Không chạy builder gọi mạng; sự kiện sinh gói KHÔNG ĐO ĐƯỢC độc lập.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-pham-vi-nen-chua-do  [P3]  Giới hạn Linux và chưa đo hai nền native vẫn không có trong bảng
TỆP/DÒNG: CHANGELOG.md:357; muc-r358-da-va.md.
VẤN ĐỀ: Dòng không số vừa bị regex bỏ vừa nằm ngoài slice kết thúc340. Nó giới hạn các probe builder, không phủ định CI Windows được thuật lại riêng.
ĐÃ THỬ VÁ: không — cấp đủ r358 và bổ sung trọn giới hạn nền của probe.
ĐÃ THỬ NGHIỆM: Đọc357 và đối chiếu slice1–150/151–340;omitted.txt có dòng này. Lượt này chạy Linux;macOS/Windows native KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-nguong-hai-client  [P3]  Ngưỡng ít nhất hai client tiếp tục bị mất
TỆP/DÒNG: CHANGELOG.md:368–369; CLAUDE.md:580–581.
VẤN ĐỀ: Ngưỡng định lượng bằng chữ nằm ngoài input, và ngay khi nới input vẫn không qua regex. Không được tuyên đã phủ quy tắc chỉ vì thân PR đã được thêm.
ĐÃ THỬ VÁ: không — thêm trọn quy tắc và nguồn vào bảng; không thực hiện client mạng trong review offline.
ĐÃ THỬ NGHIỆM: Đọc CLAUDE:580–581 có ngưỡng;CHANGELOG 368–369 ngoài slice và không chữ số. Việc từng thử hai client lịch sử KHÔNG ĐO ĐƯỢC từ phép đọc này.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-pham-vi-r-va-hai-sentinel  [P3]  Bảng vẫn mất phạm vi R chính nó và hậu quả cả hai sentinel
TỆP/DÒNG: CHANGELOG.md:354–357; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Bây giờ toàn đoạn còn nằm ngoài input; các dòng356–357 không số xác định đối tượng và lượng từ “cả hai” tiếp tục bị bỏ nếu chỉ nới slice. Không đủ một token9.9.9 hoặc tên lệnh để thay mệnh đề này.
ĐÃ THỬ VÁ: không — bổ sung toàn mệnh đề kèm nhãn thuật lại; nếu cần chạy probe mới, điều phối phải chuẩn bị phép đo có sẵn.
ĐÃ THỬ NGHIỆM: Đọc nguồn và so vị trí cuối slice 340;omitted.txt ghi 356–357. Không tự tạo chuỗi đường dẫn;hậu quả động KHÔNG ĐO ĐƯỢC vì thiếu log nguyên liệu.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-input-than-pr-va-duoi-r358  [P3]  Đã thêm thân PR nhưng cắt dòng cố định vẫn làm mất 50 dòng cuối r358
TỆP/DÒNG: muc-r359.md:1–150; muc-r358-da-va.md:1–190; CHANGELOG.md:151–167,341–390; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Ba input có thật; phần bỏ toàn thân PR493 được vá, không phải chỉ đổi nhãn bảng. Nhưng r359 thực kết thúc166, r358 thực167–390. Slice đầu dừng150, slice sau bắt151 và dừng340; phần cuối r358 50 dòng mất cả các con số4 lease,20 finding,1/6 stdout,35 khóa. So lượt trước, đuôi thiếu tăng32→50. Thêm PR493 không chứng minh đã sửa input PR491 lịch sử và không cung cấp bản thân PR491 sau sửa.
ĐÃ THỬ VÁ: không — cắt theo heading thật rồi gọi cùng script với đủ nguồn; bổ sung mệnh đề không số là bước riêng.
ĐÃ THỬ NGHIỆM: measure.py tìm substring nguyên byte:1–150/151–340;heading r358 167,r356 391;table_equal=true;PR493 có40 dòng số được giữ. Đây là đo độc lập đầu vào thực, không nhận lời khai executor.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-hop-dong-phan-loai-nguon  [P3]  Bảng vẫn bỏ định nghĩa và phạm vi ba loại nguồn
TỆP/DÒNG: CHANGELOG.md:176–187; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Bản vá đổi hai loại thành ba nhưng các dòng định nghĩa(c),phạm vi(a)/(b),attestation và lượng từ đều không có số nên mất. Các mảnh có PR493/PR491 không giữ nguyên quan hệ nguồn và mệnh đề.
ĐÃ THỬ VÁ: không — bổ sung toàn khối phân loại, gắn các khẳng định với loại nguồn; đồng thời sửa nội dung toàn xưng theoP2 riêng.
ĐÃ THỬ NGHIỆM: Tái trích3 input bằng byte;omitted.txt bỏ176,179–185,187;đọc đủ khung và 337–339 thấy mâu thuẫn mọiGit/ngoại lệ.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-dieu-kien-chot-so-ci  [P3]  Bảng thiếu đầy đủ điều kiện completed và cách xử lý in_progress
TỆP/DÒNG: CHANGELOG.md:310–312; than-pr-493.md:19.
VẤN ĐỀ: Ba dòng quy tắc không số vẫn rơi. Body mới có một dòng số0 nên giữcompleted, nhưng thiếu nhánh in_progress phải trả KHÔNG ĐO ĐƯỢC và giới hạn không suy nguyên nhân cũ. Do đó sửa input chỉ cải thiện một phần độ phủ.
ĐÃ THỬ VÁ: không — đưa nguyên điều kiện, nhánh phủ định và giới hạn suy luận vào bảng.
ĐÃ THỬ NGHIỆM: Bảng tái dựng có thânPR493:19;không cóCHANGELOG 310–312. Đọc nguồn land evidence cũng có quy tắc. Sự kiện job cũ KHÔNG ĐO ĐƯỢC offline.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-gioi-han-du-lieu-run-json  [P3]  Bảng thiếu cấu trúc run.json cùng giới hạn chứng thực model
TỆP/DÒNG: CHANGELOG.md:382–389; ops/reviews/pr468-hoso-4-packet-review-{14,15}-codex/run.json.
VẤN ĐỀ: Toàn đoạn ngoài input;riêng384 và389 không số chứa danh sách khóa/không argv/không model/tự khai. Đếm35 trongJSON không thay cho việc trích các phủ định thiết yếu này.
ĐÃ THỬ VÁ: không — cấp đủ đoạn rồi thêm nguyên mệnh đề cấu trúc và provenance; không suy model từ provider.
ĐÃ THỬ NGHIỆM: measure.py parse hai tệp 35 khóa cấp cao,lenh 3 khóa. Vị trí382–389 ngoài slice 340;omitted.txt ghi 384,389. Model runtime KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-dieu-kien-kich-hoat-workflow  [P3]  Bảng vẫn bỏ tập sự kiện cần để đối chiếu hai workflow
TỆP/DÒNG: CHANGELOG.md:43,47–49; than-pr-493.md:70–74; .github/workflows/ci.yml; .github/workflows/duyet-khac-danh-tinh.yml.
VẤN ĐỀ: Body được thêm nên một phần điều kiện CI nay được giữ, nhưng câu không số về ready_for_review vẫn rơi. Bảng không giữ toàn tập sự kiện và quan hệ giữa hai workflow. Cấu hình không đăng kýedited không chứng minh GitHub không có event đó.
ĐÃ THỬ VÁ: không — bổ sung đủ tập sự kiện, phạm vi workflow và nhãn sự kiện thuật lại.
ĐÃ THỬ NGHIỆM: extra.json parse YAML bằng BaseLoader:ci pull_request khôngtypes;duyệt pull_request_target có4 types gồmready_for_review,pull_request_review có2 types. Regex bỏ các dòng không số nêu trên;không hỏi server.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-nhan-attestation-ci-moi  [P3]  Nhãn nguồn CI vừa thêm lại bị bảng trích loại bỏ
TỆP/DÒNG: CHANGELOG.md:53,60–61,63; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Cả nhãn loại(b),attestation và câu không kèmresponse thô là các dòng không số. Bảng giữ run ID/thời lượng ngay sau đó và dòng 62 có pr491 trong tên tệp, nhưng không giữ nhãn giới hạn mới. Đây là bỏ sót mới của bảng ở r359, khác finding nội dung thânPR thiếu nhãn và khác khối phân loại nguồn r358.
ĐÃ THỬ VÁ: không — giữ nhãn nguồn cùng nhóm số CI trong đơn vị trích, không chỉ bổ sung thêm dòng run.
ĐÃ THỬ NGHIỆM: omitted.txt ghi 53,60–61,63;rebuilt-table.txt bằng BANG nhưng thiếu các dòng ấy,trong khi67–70 có số được giữ. Số CI lịch sử vẫn KHÔNG ĐO ĐƯỢC độc lập.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-anh-xa-phan-hoach-tam-mot-mot  [P3]  Bảng giữ phép cộng mới nhưng bỏ các nhánh phân loại và cách đóng nợ
TỆP/DÒNG: CHANGELOG.md:111,113–120,123–125; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Dòng8+1+1 được giữ nhưng các nhánhTÁM lọc/MỘT input/MỘT cổng và lời hướng dẫn cấp input không có chữ số nên mất. Dòng119 có sys.argv[1:] còn được giữ, càng cho thấy không phải mọi mệnh đề viết bằng chữ đều bị bỏ. Bảng không đủ ánh xạ từng số với loại lỗi để review chính bản vá phân hoạch.
ĐÃ THỬ VÁ: không — đưa cả phân hoạch cùng giải thích nguyên nhân/cách đóng vào bảng, không chỉ con số8+1+1.
ĐÃ THỬ NGHIỆM: Đối chiếu dòng 111 giữ,113–118/120/123–125 bỏ bằng re.search;đọc10 P3 gốc xác nhận8+1+1 đúng. Đây là finding độ phủ mới, không cáo buộc phép cộng sai.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

### bo-sot-ket-luan-bon-cong-tren-ban-sai  [P3]  Bảng mất chính kết luận không cổng nào bắt năm lời khai sai
TỆP/DÒNG: CHANGELOG.md:153–155; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Hai dòng 153–154 không chữ số chứa lượng từ bốn-trong-năm và không-cổng-nào-bắt-cái-nào bị bỏ;dòng 155 được giữ vì bien_nhan_v2 chỉ còn hai tên cổng và đều XANH. Đơn vị trích không giữ đủ phạm vi cảbốn cổng trênbản sai, dù đây là khẳng định người dùng yêu cầu thực nghiệm.
ĐÃ THỬ VÁ: không — đưa trọn kết luận cùng danh sách4 cổng và SHA phạm vi vào bảng.
ĐÃ THỬ NGHIỆM: Bảng tái trích bỏ153–154,giữ155;gates.json ghi tự chạy4af7e29 đủ release/claims/lease/receipt đều rc0. Nội dung khẳng định này khớp phép đo, nhưng bảng vẫn bỏ sót phạm vi của nó.
ĐỘ TIN: cao về nội dung/độ phủ đo được; sự kiện thiếu nguyên liệu không được chứng nhận.

Kiểm cuối: các byte đột biến đã phục hồi; `git -C cay-kho status --short` và `git -C review-current status --short` rỗng. Hai verdict PR491 giữ nguyên băm. **CÒN P1; chưa đạt điều kiện dừng “hết P1 hoặc approve” cho PR493 tại SHA được review.** Đây không phải lời phủ nhận kết quả hết P1 lịch sử của PR491.
