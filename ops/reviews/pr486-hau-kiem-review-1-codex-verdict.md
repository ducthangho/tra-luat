verdict: changes_requested
reviewed_sha: da481f94eee0adf1fe5fc4260a535a9b48fc2627
base_sha: c87b0679a837055ee4cc33ac48c9adb8d7ad8784
luot: 1
so_lan_luot_nay_bi_chet_va_phong_lai: 0

**2 finding P1 · 4 finding P2 · 13 finding P3.** Một P1 về khai CI exact head; một P1 về sự cố merge PR #486 trước verdict, theo timeline chủ kho cung cấp. Không có lệch ở bộ đếm/kích thước/băm/reviewed SHA của các verdict: **45/45 phép so hiện vật khớp**. Các finding về bảng bỏ sót được đếm riêng theo yêu cầu, không phải các giá trị sai của PR.

Đơn vị metadata: `luot` là lượt hậu kiểm, bộ đếm chết/phóng lại là lần; phiên này có 0 lần chết/phóng lại. SHA, run ID, số hiệu PR/ADR, phiên bản schema/công cụ là mã định danh, không là phép đếm. Reviewer Codex/OpenAI, phiên API có shell cục bộ; transport là tệp trong gói. Không suy model/effort đã phục vụ. Executor Claude theo chỉ thị. Review theo 2/2 trục: đúng hợp đồng và chuẩn nguồn/bằng chứng/thẩm quyền. Authority là chỉ thị trực tiếp của chủ kho; không cấp hoặc tự dựng lease.

`VERDICT.md` đã được ghi sớm ngay khi có kết luận đầu tiên và bổ sung trong cùng lượt. Không mạng, không đọc ngoài gói, không sửa `cay-kho`, không đổi refs hoặc workflow. Gói sửa gồm **6 tệp đầy đủ** dưới [cay/GOI-VA.md](cay/GOI-VA.md), nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

Quy ước đường nguồn: `LAND` = `ops/land/pr478-land-evidence.yaml`; `LAND468` = `ops/land/pr468-hoso-4-packet-land-evidence.yaml`; `V4/V5/V6` = `ops/reviews/pr478-land-review-<lượt>-codex-verdict.md`; `R4/R5/R6` = receipt tương ứng; `README` = `ops/reviews/README.md`. Đường nguồn tính từ `cay-kho/`; số sau dấu hai chấm là số dòng. Khoảng dòng dùng để định vị, không là số đo. Mọi nhãn **ĐO ĐƯỢC + KHỚP** chỉ áp đúng đối tượng mô tả ở cột phép đo; phép tính từ mốc được khai không xác thực mốc lịch sử.

## BẢNG ĐO

| khẳng định (tệp:dòng) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| PROMPT.md:31; Git diff base→reviewed | 8 tệp; 1674 dòng thêm; 0 dòng xoá | 8/8 tệp; 1678 dòng thêm; 0 dòng xoá; sai tổng 4 dòng thêm | ĐO ĐƯỢC + LỆCH | không |
| PROMPT.md:35–40 | 206, 3, 342, 354, 371 dòng; 3 tệp receipt × 134 dòng | 8/8 kích thước dòng khớp git numstat; tổng là 1678 dòng | ĐO ĐƯỢC + KHỚP | có |
| Gói: HEAD/base/status | detached da481f9, base c87b067, kho sạch | HEAD đầy đủ và 2 cha khớp; base là cha thứ nhất; status 0 byte; ok: true | ĐO ĐƯỢC + KHỚP | có |
| EVIDENCE.md:21–27; refs TSV | 312 nhánh mỗi nguồn, 0 dòng lệch | 312/312 nhánh cục bộ; 3/3 TSV có cùng tập tên+OID, 2/2 tệp lệch rỗng; xác thực nội dung TSV | ĐO ĐƯỢC + KHỚP | có |
| EVIDENCE.md:11,21,35 | ref máy chủ đo lại được | Chỉ đối chiếu snapshot đã cung cấp; máy chủ tại thời điểm cũ hoặc mới không truy cập được | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:3–8 | căn cứ land là ADR-0034, khung Protocol; ADR-0045 là ngoại lệ đảo vai | Đọc ADR-0034:17–20 và Protocol:466–488; ADR-0045:5–8 khớp phạm vi; 3/3 đối chiếu nguồn | ĐO ĐƯỢC + KHỚP | có |
| LAND:10; PROMPT.md:45 | Protocol §20 xếp ADR về land evidence vào ô 0 cổng | ADR-0034 ở Protocol:1136 là “có nhắc” với 10 lần nhắc và 11 lần nhắc; §20:1105–1111 cấm đổi proxy/chưa đo thành 0 cổng | ĐO ĐƯỢC + LỆCH | không |
| LAND:13,17; receipts:14,16,20–21 | schema land phiên bản 1, receipt phiên bản 2; role land_operator/reviewer; kind review_delivery_receipt; lượt 4/5/6 | 4/4 YAML đọc được; giá trị role/kind khớp các mẫu Protocol, chỉ kiểm khai báo cấu trúc | ĐO ĐƯỢC + KHỚP | có |
| LAND:14–20; receipts:17–25 | mission gh-467, generation 1, input generation [1], provider/role/session, assurance | Mission/packet là mã định danh; authority, generation lần land, provider/session runtime là tự khai, không có nguồn độc lập | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:23; 28–33 | head duyệt/merge/review cùng mã SHA ff3431f | head trong verdict lượt 6 bằng authorized_head_sha và cha thứ hai c87b067: 3/3 mã SHA khớp; chỉ đối chiếu Git và văn bản | ĐO ĐƯỢC + KHỚP | có |
| LAND:24–30,34–36 | notebyme88, COLLABORATOR, 2 review APPROVED và mốc UTC/commit_id/URL | Không có response review API; mã định danh/URL không chứng minh approval. Hồ sơ đã gắn attestation | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:31–33 | lượt cuối PR #468 review 745d888 còn head merge 17f4a1b; PR #478 không có nợ ấy | Verdict lượt 15 của PR #468 và cha merge 802fc01 xác nhận lệch head; verdict lượt 6 PR #478 khớp ff3431f. Phạm vi câu “lần này” là PR #478 | ĐO ĐƯỢC + KHỚP | có |
| LAND:40,48–49 | merge c87b067, author ducthangho, committer GitHub, cha 585c7d5+ff3431f | Git object khớp 2/2 cha và 2/2 định danh author/committer; không suy actor bấm merge | ĐO ĐƯỢC + KHỚP | có |
| LAND:41–61 | merged_at UTC, merged_by, người/phiên thao tác, chỉ thị, PAT, expectedHeadSha CAS | Không có PR API/request log. Timestamp commit là 04:01:28Z, không dùng nó bác merged_at 04:01:29Z vì khác đại lượng | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:63–76 | 6 lượt là số thứ tự cuối; có hiện vật lượt 4/5/6 | 3/3 verdict hoàn chỉnh tồn tại; số thứ tự cuối là lượt 6, không phải bằng chứng có 6 invocation hoàn tất | ĐO ĐƯỢC + KHỚP | có |
| LAND:73–76,168; receipts:45–80 | provider/surface/prompt/head/băm/mốc “ĐO ĐƯỢC từ run.json” | run.json cho lượt 4/5/6 không kèm; launcher có thể ghi trường không chứng minh lần chạy cụ thể. Hạ về attestation | KHAI RỘNG HƠN PHÉP ĐO | không |
| V4:1–4; R4:26–30,41–43; LAND:78; README:271 | lượt 4: 0 P1, 3 P2, 13 P3; changes_requested | Đếm đúng tiêu đề ^### … [P1/P2/P3]: 16/16 finding; 3/3 nguồn điều phối khớp chính verdict | ĐO ĐƯỢC + KHỚP | có |
| R4:29; README:271 | 44074 byte | 44074 byte; wc -c khớp receipt và README, 2/2 phép so | ĐO ĐƯỢC + KHỚP | có |
| R4:28 | SHA-256 verdict | 2f63bee6843b2139f8bd45bedcda062e789b49b92a6a8d96cfc838de3ba03967 (mã băm SHA-256); ok: true | ĐO ĐƯỢC + KHỚP | có |
| R4:30; LAND:78; V4:2,4 | reviewed SHA/tree của lượt | 5a4dd859ef791ca046aea3af4bab2731883323ec (mã commit); Git tree khớp trường reviewed_tree; 3/3 nguồn về SHA khớp | ĐO ĐƯỢC + KHỚP | có |
| R4:31,34; anchor:112–129 | blob ghim commit đầu 718fc41, canonical ancestry | Byte blob = byte tệp; commit thêm tệp duy nhất trong lịch sử reachable là 718fc41, tổ tiên reviewed_sha; 3/3 phép so | ĐO ĐƯỢC + KHỚP | có |
| R4:65–67; README:271 | 1245.995 giây trong receipt; README làm tròn giây nguyên | Hiệu 2 mốc được khai = 1245.994543 giây; làm tròn receipt và README đúng. Đây là số học có điều kiện | ĐO ĐƯỢC + KHỚP | có |
| R4:60–80; README:271 | run ID c80b9494f4ec46318792a6331be42775; bắt đầu UTC 2026-09-08T01:26:18.128219+00:00; kết thúc UTC 2026-09-08T01:47:04.122762+00:00; 1245.995 giây thực chạy; trạng thái xong, mã thoát 0, 0 lần chết; prompt kín=false | Thiếu run.json, prompt gốc; không xác minh runtime/mốc/deadline. Đơn vị mã thoát = mã trạng thái; không coi mã 0 là pass | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| R4:63,70–73,78 | prompt SHA-256 49452995f2400281f6d2d992b27a086c2ef7240ae044db7ae0e56f649ae38d7f; stdout 370 byte, SHA-256 a52f79914905a5b27d5494e71781a2f21cbb3817fc2f32889133cb4f42e8ebd8; stderr 1164648 byte, SHA-256 528e26eed99166fdd93e0e6d4a52aaa36fcd2d504155eed095a79ee085c7eac9 | Các mã băm có đúng cú pháp không chứng minh đã khớp dữ liệu. Không có prompt/stdout/stderr gốc của đúng lần chạy này | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| R4:87–89,99; README:271 | 309 ref, 62 tag, 0 ref lệch; kích thước thư mục gói | Gói lịch sử không kèm. 312 nhánh/62 tag hiện tại không bác 309 nhánh lịch sử. Verdict có nhắc các số ấy nhưng không thay raw inventory | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| V5:1–4; R5:26–30,41–43; LAND:79; README:270 | lượt 5: 3 P1, 0 P2, 17 P3; changes_requested | Đếm đúng tiêu đề ^### … [P1/P2/P3]: 20/20 finding; 3/3 nguồn điều phối khớp chính verdict | ĐO ĐƯỢC + KHỚP | có |
| R5:29; README:270 | 44069 byte | 44069 byte; wc -c khớp receipt và README, 2/2 phép so | ĐO ĐƯỢC + KHỚP | có |
| R5:28 | SHA-256 verdict | 22cf70d33aac8d7c0dc52501bfa494d1e8301dc17509875589b22ac3aa6760a4 (mã băm SHA-256); ok: true | ĐO ĐƯỢC + KHỚP | có |
| R5:30; LAND:79; V5:2,4 | reviewed SHA/tree của lượt | 9337779b7d61d3b08947982383081de127e7d632 (mã commit); Git tree khớp trường reviewed_tree; 3/3 nguồn về SHA khớp | ĐO ĐƯỢC + KHỚP | có |
| R5:31,34; anchor:112–129 | blob ghim commit đầu 718fc41, canonical ancestry | Byte blob = byte tệp; commit thêm tệp duy nhất trong lịch sử reachable là 718fc41, tổ tiên reviewed_sha; 3/3 phép so | ĐO ĐƯỢC + KHỚP | có |
| R5:65–67; README:270 | 1238.546 giây trong receipt; README làm tròn giây nguyên | Hiệu 2 mốc được khai = 1238.545849 giây; làm tròn receipt và README đúng. Đây là số học có điều kiện | ĐO ĐƯỢC + KHỚP | có |
| R5:60–80; README:270 | run ID a59fff06c2bd49d9a9bba329a60286dd; bắt đầu UTC 2026-09-08T02:58:18.735830+00:00; kết thúc UTC 2026-09-08T03:18:57.281679+00:00; 1238.546 giây thực chạy; trạng thái xong, mã thoát 0, 0 lần chết; prompt kín=false | Thiếu run.json, prompt gốc; không xác minh runtime/mốc/deadline. Đơn vị mã thoát = mã trạng thái; không coi mã 0 là pass | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| R5:63,70–73,78 | prompt SHA-256 151476495aa1be9fec8bdde3f0123a729e37e60fad3f8c4ecf4c9df3f2207c9e; stdout 565 byte, SHA-256 604a34257be2f3badcfae143cbc17e56685a18467a3756c04aa6b4106e354e91; stderr 543792 byte, SHA-256 cf88f039b0a21cec3d29602fea7e70c339abae5d695cdb5d650d6910d75c8060 | Các mã băm có đúng cú pháp không chứng minh đã khớp dữ liệu. Không có prompt/stdout/stderr gốc của đúng lần chạy này | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| R5:87–89,99; README:270 | 309 ref, 62 tag, 0 ref lệch; kích thước thư mục gói | Gói lịch sử không kèm. 312 nhánh/62 tag hiện tại không bác 309 nhánh lịch sử. Verdict có nhắc các số ấy nhưng không thay raw inventory | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| V6:1–4; R6:26–30,41–43; LAND:80; README:269 | lượt 6: 0 P1, 0 P2, 23 P3; approve | Đếm đúng tiêu đề ^### … [P1/P2/P3]: 23/23 finding; 3/3 nguồn điều phối khớp chính verdict | ĐO ĐƯỢC + KHỚP | có |
| R6:29; README:269 | 35829 byte | 35829 byte; wc -c khớp receipt và README, 2/2 phép so | ĐO ĐƯỢC + KHỚP | có |
| R6:28 | SHA-256 verdict | 607fe0a2699af4e9899b3092c9a275f2518eeb5b052eb4408d430ef8188b49a8 (mã băm SHA-256); ok: true | ĐO ĐƯỢC + KHỚP | có |
| R6:30; LAND:80; V6:2,4 | reviewed SHA/tree của lượt | ff3431f11bc0ba3ffa0c3616003f833c3cfc3ebb (mã commit); Git tree khớp trường reviewed_tree; 3/3 nguồn về SHA khớp | ĐO ĐƯỢC + KHỚP | có |
| R6:31,34; anchor:112–129 | blob ghim commit đầu 718fc41, canonical ancestry | Byte blob = byte tệp; commit thêm tệp duy nhất trong lịch sử reachable là 718fc41, tổ tiên reviewed_sha; 3/3 phép so | ĐO ĐƯỢC + KHỚP | có |
| R6:65–67; README:269 | 981.24 giây trong receipt; README làm tròn giây nguyên | Hiệu 2 mốc được khai = 981.240489 giây; làm tròn receipt và README đúng. Đây là số học có điều kiện | ĐO ĐƯỢC + KHỚP | có |
| R6:60–80; README:269 | run ID f6f412507630470f9a996b09d7382e8e; bắt đầu UTC 2026-09-08T03:26:29.271815+00:00; kết thúc UTC 2026-09-08T03:42:50.512304+00:00; 981.24 giây thực chạy; trạng thái xong, mã thoát 0, 0 lần chết; prompt kín=false | Thiếu run.json, prompt gốc; không xác minh runtime/mốc/deadline. Đơn vị mã thoát = mã trạng thái; không coi mã 0 là pass | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| R6:63,70–73,78 | prompt SHA-256 7a3a5190072c3c85e5a77455b7586c11fa937568ee78e0c0ed33aa7855ea7f6a; stdout 394 byte, SHA-256 c16080d6424e060200824a2ea2e27e0735617f68e8749e3f7b5ba3de058578e5; stderr 1062732 byte, SHA-256 f8b35325048c9c97d2cd32453e15a6b693665a44ff4a3e085922b791b1ed2884 | Các mã băm có đúng cú pháp không chứng minh đã khớp dữ liệu. Không có prompt/stdout/stderr gốc của đúng lần chạy này | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| R6:87–89,99; README:269 | 309 ref, 62 tag, 0 ref lệch; kích thước thư mục gói | Gói lịch sử không kèm. 312 nhánh/62 tag hiện tại không bác 309 nhánh lịch sử. Verdict có nhắc các số ấy nhưng không thay raw inventory | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| README:269,271; R4:4; R6:4 | 11/13 P3 và 22/23 P3 là tín dụng độ phủ | Đếm slug bang-do-bo-sot-: 11 finding, 16 finding, 22 finding cho lượt 4/5/6; các tỷ lệ công bố khớp 2/2 tỷ lệ | ĐO ĐƯỢC + KHỚP | có |
| LAND:84–89,166 | không có hiện vật nào; không khôi phục được | Quét tên snapshot không phủ mọi nơi lưu/tên khác/object không reachable. V4:14 đã giới hạn kết luận; lời điều phối bỏ giới hạn | KHAI RỘNG HƠN PHÉP ĐO | không |
| LAND:85–86,166, lịch sử --all | 0 đường dẫn pr478/478-verdict ở phép quét cũ | Hiện tại có 7 đường dẫn mới; tổ tiên 5a4dd85 và base c87b067 đều 0 đường dẫn khớp. Ref inventory lần cũ không kèm nên chưa tái lập đúng --all cũ | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:85,166, GitHub get_comments | 0 comment tại thời điểm đo | Không mạng, JSON thô, mốc chính xác hoặc thông tin phân trang; không kiểm được endpoint lịch sử | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:86–88 | commit 8f7becb/260f7c6/5a4dd85 nói về lượt 1/2/3 | 3/3 commit message có nhắc các lượt; đó là lời điều phối được Git lưu, không độc lập chứng minh phiên reviewer hoặc verdict đã mất | ĐO ĐƯỢC + KHỚP | có |
| LAND:91–93; R4/R5/R6:38,123–124; README:269–271 | comment khớp TỪNG KÝ TỰ sau đọc ngược/diff; 2 neo độc lập | Chỉ xác minh được 3/3 blob; không có response/diff/client. V4/V5/V6 chứa tương ứng 8/4/2 ký tự nhạy với chuẩn hoá HTML; CLAUDE.md:127–143 cảnh báo phép đọc MCP không chứng minh byte GitHub | KHAI RỘNG HƠN PHÉP ĐO | không |
| LAND:95–97; R4/R5/R6:9–12 | lượt 5 đăng muộn hơn 1 ngày, comment ngày 2026-09-09, vì quên đăng | Ngày đơn thuần không chứng minh quá 24 giờ: nếu comment lúc đầu ngày thì chênh so mốc kết thúc được khai chỉ 20 giờ 41 phút 2,718321 giây. Thiếu created_at và log phiên; không bác sự kiện, chưa xác minh thời lượng/lý do | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| PROMPT.md:12–21; LAND:94–97 không có ghi sự cố PR #486 | PR #486 merge khi connector còn Running | Theo chỉ thị chủ kho: mốc UTC 08:54:36 → 08:54:45 → 08:55:09; số học 9 giây và 24 giây khớp 2/2 khoảng. Git chỉ xác minh merge có cha thứ hai 359d38e; không đo được API timeline | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:98–108; README:269–271 | lượt 6 xác nhận đã vá thật 3 P1 lượt 5 | 3/3 slug xuất hiện cùng kết luận trong V6:18–20; nội dung LAND cũ còn các tên trường đã sửa, CHƯA XÁC ĐỊNH, #477 đã merge và P3 README chưa đóng. Không đọc thành mọi nợ PR #468 đã hết | ĐO ĐƯỢC + KHỚP | có |
| LAND:100–104; README:270 | phản ví dụ (44 bước,4 skipped)+(-1 bước,0 skipped)=(43 bước,4 skipped) | Số học đúng 2/2 thành phần; 4 giả thuyết trong LAND cũ. Không xác minh đây là diễn biến thực | ĐO ĐƯỢC + KHỚP | có |
| LAND:110–117 | CI pull_request trên exact head ff3431f | Workflow chỉ có 1 checkout, 0 with.ref; chú thích xác định synthetic merge. Chưa có log checkout SHA/tree; liên quan head khác chạy suite trực tiếp trên head | KHAI RỘNG HƠN PHÉP ĐO | không |
| LAND:115–117,123–125 | run ID/event/job success/failure; 44 bước, 3 skipped, 5 bước, 0 null, 0 hỏng; 2 lượt thay thế | Tất cả là sự kiện GitHub: không có response/job logs; KHÔNG ĐO ĐƯỢC. Không thay bằng số bước YAML | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:119–122 | PR thường chỉ Ubuntu; Windows chạy sau merge | Đọc matrix: PR thường không nhãn windows có 1/1 nền Ubuntu; push master có 2/2 nền; workflow_dispatch và nhãn windows là ngoại lệ đã có trong mã. Không nói Windows chỉ chạy duy nhất push | ĐO ĐƯỢC + KHỚP | có |
| LAND:125–127 | failure cũ là nguyên nhân mergeable_state unstable, đã được thay thế nên không chặn | Không có snapshot check contexts/required checks/timeline để loại nguyên nhân khác hay chứng minh thay thế. Chỉ có lời điều phối | KHAI RỘNG HƠN PHÉP ĐO | không |
| LAND:128–131 | chỉ đếm khi completed và 0 bước conclusion null | Đây là tiêu chí phương pháp, không phải bằng chứng run đã đạt. Kết quả run thật không có nguồn | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:136–138 | head đã vào master; 2 cha; 0 commit nhánh ngoài master | Git xác minh 2/2 cha c87b067; ff3431f có 0 commit ngoài c87b067; nhánh land-468 có 0 commit ngoài reviewed_sha; ok: true. master=c87b067 là snapshot cũ, master gói nay là da481f9 | ĐO ĐƯỢC + KHỚP | có |
| LAND:142–147 | push run 34185511309: mỗi job 44 bước; Ubuntu 4 skipped, Windows 6 skipped; 0 null, 0 hỏng | API runtime không đo được; 40 bước YAML và 10 điều kiện if không phải 44 bước API (có bước runner sinh). Không gọi chênh 4/6 skipped là mâu thuẫn cùng job | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:149–150 | lease suite 121/121 ca, đã chạy 121 ca, bỏ qua 0 ca; mã thoát 0 | KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): không chạy suite dài; không có stdout lịch sử tương ứng c87b067 | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:150–153; cong-cu.txt | actionlint phiên bản 1.7.7, shellcheck phiên bản 0.9.0; có mặt ở lần đo cũ | Công cụ hiện tại có trong gói/PATH nhưng không chứng minh môi trường lần chạy cũ. Hành vi thiếu shellcheck không tái thử ở lượt này | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:155 | 30 receipt đạt v2, 11/11 legacy, 42 nợ, tổng 83 receipt; 0 vi phạm/không đo được | Git tại base có 83/83 receipt: 31 tự khai v2 và 52 tự khai v1; không nhầm số tự khai v2 với số ĐẠT v2. Không chạy validator ngoài danh sách lệnh cho phép; kết quả lịch sử KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho) | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:157 | doc-claims-check ok: true ở base c87b067 | Đo mới trên reviewed_sha: ok: true, 2,853 giây. Không tái xác nhận lần chạy lịch sử hoặc chuyển kết quả giữa SHA | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| Đo mới reviewed_sha, ngoài lời khai lịch sử | doc/doctrine/ADR | doc ok: true; doctrine 7/7 tệp đã quét, 0 chỗ chép; ADR 46/46 dòng; 3/3 phép kiểm có đầu ra dương, không chỉ mã thoát | ĐO ĐƯỢC + KHỚP | có |
| LAND:159–161 | đủ/thiếu tag làm đổi byte stdout không đổi mã thoát | V6 ghi thí nghiệm; lượt này không tạo lại cây/tag vì ngoài nhu cầu kiểm nội dung mới. KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho); khớp lời reviewer không phải đo mới | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:173–174; R4/R5/R6:98–101 | thư mục gói 34 M / 8,3 M / 170 M, script không vào kho | Các thư mục và script lượt 4/5/6 không được lưu tại đường dẫn đã dẫn: 3/3 đường dẫn vắng. Kích thước và ý định loại bỏ chỉ có attestation; M chưa định nghĩa byte thập phân hay nhị phân | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:179–181 | land evidence thứ ba trên master | Base có 2/2 tệp; reviewed có 3/3 tệp; tệp mới là pr478. Land #477 ở nhánh PR #480, không thuộc cây reviewed | ĐO ĐƯỢC + KHỚP | có |
| LAND:180–181; LAND468:344; merge message da481f9 | PR #480 vẫn draft tại thời điểm ghi; PR #477 chưa landed | Commit message reviewed_sha khai #480 đã gỡ draft và được duyệt lúc 08:32:30Z. Đó là attestation mới hơn, không phải API. Không đọc câu lịch sử thành trạng thái hiện tại; không suy landed từ gỡ draft/approved | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:183–184,187 | Mission/4 Issue vẫn open; #475 draft; PR này không nghiệm thu mission | Trạng thái GitHub không có nguồn; diff chỉ là hồ sơ, không có acceptance/runtime mới. Không xác nhận trạng thái Issue từ nội dung Git | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:186–187 | _kiem_bia_mo vẫn any; không đổi mã điều phối | ops/lease_publish.py:607 còn not any; 8/8 tệp diff chỉ là hồ sơ dưới ops/land và ops/reviews; ok: true | ĐO ĐƯỢC + KHỚP | có |
| LAND:189–193 | 4 lease GATE, mốc cấp trước hạn, 4 spec_hash, revision 1/2/3/4, generation 1 | 4/4 tệp lease có generation 1; revision lần lượt 1,2,3,4; 4/4 hash khác nhau; 4/4 mốc cấp trước 2026-09-07T14:30:07Z. ADR-0034:8 đòi generation mới khi đổi contract | ĐO ĐƯỢC + KHỚP | có |
| LAND:189,193 | nợ A9 chờ quyết định chủ kho; hết hạn không hợp thức hoá cấp sớm | Lệch contract đo được; quyết định/ngoại lệ authority và thi công thực tế không có nguồn. Không tự sửa lease hoặc kết luận đã thi công trái phép | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| LAND:195–198 | README:57 còn câu sai, chưa đóng nợ; sửa sẽ đổi checksum | Câu còn nguyên; ARTIFACTS.sha256 tham chiếu README; SHA-256 hiện tại khớp. 1/1 tệp được đối chiếu; không sửa hiện vật cũ chỉ để đóng nợ giả | ĐO ĐƯỢC + KHỚP | có |
| LAND:200–206 | không việc nào được làm vì nhánh chưa tồn tại | Không có nhánh không bao quát công việc chưa push/tên khác/nhánh đã xóa. Kết luận quá phạm vi dù vế thiếu nhánh khớp | KHAI RỘNG HƠN PHÉP ĐO | không |
| LAND:201–203 | 2 lease cấp/hết hạn cùng mốc; 2 nhánh chưa tồn tại | Lease đọc từ ref ops/cap-lease-mu-ref-va-verdict tại a2468831896601c60c216133eac2ba1366fd3254: 2/2 mốc cấp và 2/2 mốc hết hạn khớp; 2/2 nhánh vắng trong 312 heads | ĐO ĐƯỢC + KHỚP | có |
| LAND:203–205 | không PR, mỗi Issue 2 comment; vì sao không đo được, công cụ phiên đã ngắt | PR/comment/công cụ phiên/transcript đều không có trong gói; KHÔNG ĐO ĐƯỢC. Không tự dựng nguyên nhân, không đọc ngoài gói | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| receipts:25–26 | cross_approved cùng changes_requested ở lượt 4/5 | Protocol §8:507 định nghĩa assurance theo cặp provider, verdict là trường riêng. Không nâng thành finding chỉ dựa vào tên cross_approved; danh tính lần chạy vẫn chưa xác minh | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| receipts:34–36,115–129 | cổng chỉ chấp nhận loại neo cho phép, canonical cần blob URL | Đọc bien_nhan_v2.py:511,758–857 xác nhận 3/3 loại neo cho phép và đường đối chiếu URL-path-hash-ancestry. Đây là đọc mã, không phải chạy cổng | ĐO ĐƯỢC + KHỚP | có |
| receipts:37,118–120 | từng bị cổng từ chối 2 lần | Số lần từ chối lịch sử không có log; không thể thay bằng việc cổng hiện có nhánh từ chối | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| receipts:103–110,127–134 | actor ducthangho, tác giả PR; comment sửa/xoá được; blob merge giữ ancestry; không tag lưu-tru | Actor/API/độ bảo vệ ref không đo được; ancestry blob đo được riêng ở trên. Không suy tag bảo vệ hoặc model identity từ việc URL/blob tồn tại | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| TSV/script; 3 nhóm | 193 khẳng định: 86 + 25 + 82 | Tái sinh đúng 193/193 hit regex, 3/3 nhóm; đó là số hit, có ID bị đếm hai lần và số hiệu PR ghép nhầm đơn vị, không phải 193 mệnh đề độc lập | ĐO ĐƯỢC + KHỚP | có |

Nhiệm vụ về các chỗ mềm đã có kết luận tách từng vế trong bảng: thiếu hiện vật là finding về phạm vi; comment là finding về lớp đọc; sự cố PR #486 được ghi nợ riêng; 2/2 nhánh packet vắng nhưng lượng công việc/lý do không đo được; A9 khớp 4/4 lease; draft PR #480 là lời lịch sử và commit message có attestation mới hơn, không xác minh GitHub; số CI/approval/merged_by/merged_at là KHÔNG ĐO ĐƯỢC. Không lấy timestamp commit để thay timestamp API.

Quyết định không trích mọi số trong verdict gốc **không tự nó là lỗi**: đó là hiện vật nguồn và không nên viết lại lời reviewer để làm sạch receipt. Tuy nhiên phải đọc nó để kiểm mọi câu điều phối nói về nó; lượt này đã làm. Tái xác thực tất cả các thí nghiệm cũ là công việc khác; những script/log không kèm không được coi là đã chạy lại.

## KHẲNG ĐỊNH BẢNG BỎ SÓT

| tệp:dòng | khẳng định | vì sao bộ lọc trượt | hệ quả |
|---|---|---|---|
| LAND:10 | 0 cổng | cổng không nằm trong DON_VI | finding dan-protocol-khong-khop-o-khong-cong [P2] |
| LAND:32–33,99; README:269 | KHÔNG có nợ ấy; cả ba ĐÃ VÁ THẬT | khẳng định phi số; bắt 3 P1 không bắt phạm vi chữ “cả ba” | đối chiếu riêng đúng phạm vi PR #478; không lan sang PR #486 |
| LAND:84–89,166 | không hiện vật nào; không khôi phục được | lượng từ/câu phủ định ngoài regex số | finding khong-tim-thay-bi-nang-thanh-khong-ton-tai [P2] |
| LAND:91–93; R4/R5/R6:38,123–124; README:269–271 | khớp TỪNG KÝ TỰ; HAI neo độc lập | số viết chữ và mức bảo đảm không phải đơn vị regex | finding neo-comment-khai-vuot-lop-doc [P2] |
| LAND:200–206 | KHÔNG có việc nào được làm; đừng ghi nguyên nhân khi chưa đo | phủ định và điều kiện không mang số | finding vang-nhanh-khong-chung-minh-chua-lam-viec [P2] |
| LAND:110–112; R4/R5/R6:25 | exact head; assurance/cross_provider/không có lease | thuộc tính/quan hệ ngoài số | finding ci-pull-request-bi-khai-thanh-exact-head [P1]; assurance xem phạm vi protocol |
| LAND:78–80; R4/R5/R6:41–43; README:269–271 | map P1/P2/P3; verdict; reviewed SHA trong chính hiện vật | so_p1: 0 và P1 0 ngược thứ tự regex số-đơn vị | bs-map-ket-qua-ba-nguon [P3] |
| R4/R5/R6:28–29; README:269–271 | SHA-256 và byte verdict | regex SHA tối đa 40 ký tự; số byte đứng trần trong YAML/cột | bs-bam-va-byte-verdict [P3] |
| R4/R5/R6:63–80; LAND:73–76 | băm prompt/stdout/stderr, byte, mã thoát, 0 lần chết | hash dài, key:value trần, ma_thoat khác rc | bs-runtime-va-do-phu-nguon [P3] |
| R4/R5/R6:65–67,79; LAND:29–30,41,95,190,201–202 | mốc UTC, thời lượng, deadline, ngày muộn | định dạng ngày/giờ và key giây không nằm trong mẫu | bs-moc-va-thoi-luong [P3] |
| R4/R5/R6:87–89; LAND:179–181 | số ref/tag/lệch; land evidence thứ BA | giá trị YAML trần và thứ tự viết chữ | bs-inventory-va-thu-tu [P3] |
| LAND:150,155; R4/R5/R6:14,20,64 | đã chạy/bỏ qua; 0 không đo được; 42 nợ; 83 tổng; schema/lượt/prompt kín | đơn vị thiếu, dấu bằng khác rc, boolean | bs-tieu-chi-va-tong-post-merge [P3] |
| LAND:189–193 | 4 lease, 4 spec_hash khác, generation giữ 1 | số viết chữ và số đứng sau key; 1/2 và 3/4 bắt nhầm thành tỷ số | bs-a9-generation-va-hash [P3] |
| LAND:174; R4/R5/R6:98–101 | 34M / 8,3M / 170M và không lưu script tự đo | M không nằm trong đơn vị; câu phủ định không số | bs-kich-thuoc-goi-va-cong-cu-mat [P3] |
| LAND:125–127 | run failure là nguyên nhân unstable; đã thay thế | quan hệ nhân quả phi số | nguyen-nhan-unstable-chua-co-nguon-phan-dinh [P3] |
| PROMPT.md:31 | tổng diff 1674 dòng thêm | prompt không nằm trong tập đầu vào extractor | tong-diff-goi-lech-bon-dong [P3] |
| PROMPT.md:12–21; hồ sơ PR #486 | merge trước verdict hoàn tất; connector Running | prompt ngoài tập đầu vào; không có trường ghi nợ trong diff | pr486-merge-truoc-verdict-chua-duoc-ghi-no [P1] |

### ci-pull-request-bi-khai-thanh-exact-head  [P1]  Hồ sơ tái nhận CI cây merge tổng hợp thành CI trên head đã duyệt
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:110–117.

VẤN ĐỀ: Tiêu đề và tên phép kiểm khẳng định suite đã chạy trên exact head ff3431f. CI dùng actions/checkout không có with.ref; chính ci.yml:114 và :371–399 gọi GITHUB_SHA trên pull_request là synthetic merge. Bước kiểm tổ tiên EOL chỉ kiểm một quan hệ, không đổi checkout cho suite. Không có log checkout SHA/tree. Đây là lỗi lời khai làm mất nợ CI exact head mà verdict trước đã yêu cầu giữ, dù mọi số bước có thể đúng. Không kết luận run đỏ hoặc head có lỗi.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/land/pr478-land-evidence.yaml.

ĐÃ THỬ NGHIỆM: audit.py ghi 1/1 checkout không ghim ref; đọc 2/2 chú thích synthetic merge; gói vá đổi cả tiêu đề và ten, thêm giới hạn exact checkout. Kiểm YAML và khối nguồn: ok: true. Không chạy CI (ràng buộc chủ kho). Rủi ro: hồ sơ có thể được nâng lại sau khi executor có log thật, không suy từ run ID.

ĐỘ TIN: cao.

### pr486-merge-truoc-verdict-chua-duoc-ghi-no  [P1]  PR vận chuyển hồ sơ đã merge khi verdict còn Running nhưng chưa có bản ghi nợ tương ứng
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:94–97; ops/reviews/README.md:269–271; PROMPT.md:12–21.

VẤN ĐỀ: Chỉ thị chủ kho nêu rõ lỗi vận hành PR #486. Hồ sơ tự khai lỗi đăng muộn của PR #478 nhưng không lưu việc PR #486 đã merge trước verdict hoàn tất. Các verdict mới lưu đều review head của PR #478; không verdict nào trong nhóm này review head PR #486. Không dùng câu “Lần này KHÔNG có nợ ấy” của PR #478 để xóa nợ PR #486. Đây là finding hậu kiểm quy trình dựa trên thông tin chủ kho cung cấp, không phải tự đo GitHub; thiếu mạng không biến nó thành approval.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/reviews/pr486-hau-kiem-no-review.yaml; cay/ops/land/pr478-land-evidence.yaml.

ĐÃ THỬ NGHIỆM: Git xác minh cha thứ hai của da481f9 là 359d38e8c449e009acc4123fa6110257ad800949; 3/3 verdict mới neo các head PR #478; số học 2/2 khoảng timeline đúng (9 giây, 24 giây). Timeline thật KHÔNG ĐO ĐƯỢC. Bản vá ghi nguồn attestation và không giả đã đóng nợ; YAML ok: true. Executor phải lưu kết quả hậu kiểm/PR vá; bản ghi không hồi tố approval.

ĐỘ TIN: vừa.

### dan-protocol-khong-khop-o-khong-cong  [P2]  Gán ô không cổng cho ADR về land trái chính bảng được dẫn
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:10–11.

VẤN ĐỀ: Căn cứ nghĩa vụ land ở dòng mở là ADR-0034. Hàng đó trong Protocol:1136 ghi “có nhắc” với 10 lần và 11 lần; phần giải nghĩa phân biệt rõ 0 cổng, proxy có nhắc và chưa đo. Không thể trích §20 thành “xếp các ADR về land evidence vào ô 0 cổng”. Điều này không chứng minh nội dung land evidence đã có cổng; nó chứng minh dẫn nguồn sai và suy rộng. Prompt:45 cũng lặp đúng sai sót này.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/land/pr478-land-evidence.yaml.

ĐÃ THỬ NGHIỆM: Đối chiếu 1/1 hàng ADR-0034 và 3/3 định nghĩa ô. Gói vá rút số 0 cổng, giữ cảnh báo proxy không chứng minh cưỡng chế; YAML ok: true. Rủi ro cần tránh: không đảo thành “đã có cổng kiểm nội dung”.

ĐỘ TIN: cao.

### khong-tim-thay-bi-nang-thanh-khong-ton-tai  [P2]  Phép quét tên snapshot bị dùng để kết luận mất hiện vật không thể phục hồi
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:84–89,166.

VẤN ĐỀ: rev-list --objects --all chỉ phủ object reachable và tên khớp regex. get_comments, ngay cả nếu phản hồi rỗng thật, chỉ nói về endpoint và thời điểm đó; không phủ review objects, tên tệp khác, nơi lưu khác hoặc khả năng phục hồi. V4:14 đã nói đúng giới hạn này nhưng điều phối nâng thành “KHÔNG có hiện vật nào”, “không khôi phục được”. Số 0 đường dẫn lịch sử không bị bác chỉ vì PR này vừa thêm hiện vật.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/land/pr478-land-evidence.yaml.

ĐÃ THỬ NGHIỆM: Quét lại --all: 7/7 đường dẫn trúng là hiện vật mới; tổ tiên 5a4dd85 và base c87b067 có 0 đường dẫn trúng. Không có raw API hoặc inventory all-refs lần cũ. Gói vá thu hẹp phạm vi, giữ nợ chưa có verdict gốc, YAML ok: true. Rủi ro: không được dựng nội dung verdict từ commit message.

ĐỘ TIN: cao.

### neo-comment-khai-vuot-lop-doc  [P2]  Đọc ngược qua lớp chuẩn hoá chưa chứng minh từng ký tự của comment GitHub
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:91–93; receipts lượt 4/5/6:38,123–124; ops/reviews/README.md:269–271.

VẤN ĐỀ: Không có response/diff hoặc tên client đọc lại đi kèm; CLAUDE.md:127–143 đã đo lớp MCP đổi thực thể HTML và yêu cầu client độc lập để kết luận byte GitHub. Bản chuẩn hoá và bản gốc không là cùng đối tượng đo; giải mã thực thể trước so sánh còn có thể làm nhiều chuỗi khác nhau thành cùng chuỗi. Không được nâng lời “đã diff” thành chứng nhận từng ký tự hoặc coi comment là nguồn độc lập đã xác thực. Không khẳng định comment thực tế sai: nó KHÔNG ĐO ĐƯỢC.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/land/pr478-land-evidence.yaml; cay/ops/reviews/pr478-land-review-{4,5,6}-codex-verdict.receipt.yaml và cay/ops/reviews/README.md.

ĐÃ THỬ NGHIỆM: 3/3 verdict chứa ký tự có thể bị biến đổi, tổng tương ứng 8 ký tự/4 ký tự/2 ký tự; 3/3 blob ghim khớp byte. Gói vá đồng bộ 5/5 tệp điều phối, tách blob đo được và comment attestation; YAML và giữ nguyên metadata hiện vật 3/3 receipt: ok: true. Rủi ro: không HTML-unescape mù và không sửa verdict gốc.

ĐỘ TIN: cao.

### vang-nhanh-khong-chung-minh-chua-lam-viec  [P2]  Nhánh vắng và lease hết hạn không chứng minh executor chưa làm việc nào
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:200–205.

VẤN ĐỀ: Hai tên nhánh vắng thật trong snapshot nhưng công việc cục bộ chưa push, nhánh tên khác hoặc nhánh từng tồn tại rồi bị xoá đều tương thích với kết quả đó. Câu “KHÔNG có việc nào được làm” rộng hơn phép đo đầu ra. Chính đoạn sau thừa nhận không đọc được phiên executor nên không có nguồn bổ sung để chốt câu ấy. Không cần và không được đọc transcript ngoài gói để sửa lỗi suy luận.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/land/pr478-land-evidence.yaml.

ĐÃ THỬ NGHIỆM: Đọc lease từ a2468831896601c60c216133eac2ba1366fd3254; 2/2 ngày hết hạn đã qua; 2/2 nhánh vắng trong 312 heads. Gói vá nói “chưa có nhánh đầu ra trong snapshot”, giữ cả lượng việc thật và nguyên nhân ở KHÔNG ĐO ĐƯỢC; YAML ok: true. Rủi ro: không dùng bản vá để tự cấp lại lease.

ĐỘ TIN: cao.

### nguyen-nhan-unstable-chua-co-nguon-phan-dinh  [P3]  Lời giải thích unstable và thay thế required check chưa có bằng chứng phân định
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:125–127.

VẤN ĐỀ: Trạng thái một run cũ và vài run mới không tự xác định run nào quyết định mergeable_state hoặc required-check context nào đã được thay thế. Không có response/timeline để tái xét. Gắn attestation cho số CI chưa biến quan hệ nhân quả này thành phép đo.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/land/pr478-land-evidence.yaml.

ĐÃ THỬ NGHIỆM: Đã đọc toàn pre_merge_checks; không có diagnostic/timeline trong gói. Đã thử thu hẹp câu trong cùng bản vá LAND; YAML ok: true. KHÔNG ĐO ĐƯỢC diễn biến GitHub; không kết luận run cũ thực sự vẫn chặn.

ĐỘ TIN: vừa.

### nguon-run-khong-duoc-luu-nhung-khai-do-duoc  [P3]  Nhận metadata lần chạy là đo được trong khi run gốc không được giao
TỆP/DÒNG: ops/land/pr478-land-evidence.yaml:73–76,168; receipts:45–80; README:269–271.

VẤN ĐỀ: Provider/surface, các mốc và băm có thể được launcher ghi nhưng run.json của đúng lượt không có trong kho. Có verdict không xác minh provider/surface/session của lần chạy. Những run.json PR #468 lượt 14/15 là đối tượng khác, không được dùng thay thế. Sửa câu giới hạn để người sau không đọc có-khả-năng-ghi thành đã-đối-chứng.

ĐÃ THỬ VÁ: có — đã sinh nội dung tệp đầy đủ trong gói, chỉ sửa lời điều phối/ghi nợ; xem cách sửa, ca kiểm và rủi ro bên dưới.

GÓI VÁ: cay/ops/land/pr478-land-evidence.yaml; cay/ops/reviews/pr478-land-review-{4,5,6}-codex-verdict.receipt.yaml và cay/ops/reviews/README.md.

ĐÃ THỬ NGHIỆM: Không có run.json gắn 3/3 run ID mới ở nhóm hiện vật này; kiểm thời lượng chỉ là số học từ receipt. Bản vá gắn nhãn metadata là attestation, giữ các số lịch sử; ok: true.

ĐỘ TIN: vừa.

### bs-map-ket-qua-ba-nguon  [P3]  Bảng bỏ map kết quả mà ba nguồn phải đồng bộ
TỆP/DÒNG: LAND:78–80; receipts:41–43; README:269–271.

VẤN ĐỀ: Bộ lọc bắt số-đơn vị, không bắt so_p1: 0 hoặc P1 0. Comment đầu receipt có vài số nhưng không kiểm map giữa các nơi. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; Đếm tiêu đề và so ba nguồn: 9/9 bộ đếm khớp, 3/3 verdict và 3/3 reviewed SHA khớp. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-bam-va-byte-verdict  [P3]  Bảng bỏ cả byte verdict và SHA-256 bắt buộc của receipt
TỆP/DÒNG: receipts:28–29; README:269–271.

VẤN ĐỀ: SHA-256 dài hơn trần 40 ký tự; byte trong YAML/cột đứng trần. Đây là lớp đo trực tiếp giá trị nhất nhưng bảng không bắt. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; wc -c và SHA-256 khớp 3/3 tệp; các phép đối chiếu hiện vật tổng cộng 45/45. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-runtime-va-do-phu-nguon  [P3]  Bảng bỏ nhiều trường runtime và cờ giới hạn nguồn
TỆP/DÒNG: receipts:63–80.

VẤN ĐỀ: stdout_byte, stderr_byte, ma_thoat, số lần chết và prompt_kin_hoan_toan không theo mẫu. Có số byte lớn lại bị bắt nhầm thành SHA. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; Đọc đủ 3/3 khối; runtime KHÔNG ĐO ĐƯỢC. Không gọi băm đúng độ dài thành băm đã khớp dữ liệu. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-moc-va-thoi-luong  [P3]  Bảng bỏ mốc UTC và phép tính thời lượng trong receipt
TỆP/DÒNG: receipts:65–67,79; LAND:29–30,41,95,190,201–202.

VẤN ĐỀ: Regex không hiểu ISO timestamp và key giây; còn số viết chữ “một ngày”. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; 3/3 phép làm tròn thời lượng receipt khớp: 1245,994543 giây; 1238,545849 giây; 981,240489 giây. Mốc thực/lý do đăng muộn KHÔNG ĐO ĐƯỢC. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-inventory-va-thu-tu  [P3]  Bảng bỏ số tag, ref lệch, thứ tự land evidence và neo topology
TỆP/DÒNG: receipts:87–89; LAND:136–138,179–181.

VẤN ĐỀ: Bare YAML values, số đứng riêng trong lệnh và thứ tự viết chữ không khớp. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; 312/312 heads hiện tại; 62/62 tags cục bộ; base 2/2 tệp land và reviewed 3/3 tệp; các số 309 ref cũ KHÔNG ĐO ĐƯỢC từ inventory hiện tại. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-tieu-chi-va-tong-post-merge  [P3]  Bảng bỏ mẫu số tổng và trạng thái chưa chạy của các phép kiểm
TỆP/DÒNG: LAND:150,155; receipts:14,20,64.

VẤN ĐỀ: Bắt 121/121 nhưng bỏ đã chạy=121, bỏ qua=0; thiếu đơn vị nợ và tổng; không bắt boolean/schema scalar. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; Đếm 83/83 receipt tại base; 86/86 tại reviewed. Không suy 31 receipt tự khai v2 là 30 receipt đã validate. Kết quả suite lịch sử KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho). Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-a9-generation-va-hash  [P3]  Bảng bắt revision như tỷ số nhưng bỏ generation và số lease A9
TỆP/DÒNG: LAND:189–193.

VẤN ĐỀ: “bốn” là chữ; generation giữ 1 không có hậu tố đơn vị; 1/2 và 3/4 là danh sách revision chứ không phải N/N. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; 4/4 lease có generation 1; 4/4 hash khác nhau; revision lần lượt 1–4; 4/4 mốc trước hạn cũ. Lời khai nợ khớp; không vá lease. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-kich-thuoc-goi-va-cong-cu-mat  [P3]  Bảng không bắt kích thước thư mục và quyết định bỏ công cụ reviewer
TỆP/DÒNG: LAND:173–174; receipts:98–101.

VẤN ĐỀ: Đơn vị M ngoài allowlist và câu không lưu script không có số. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; 3/3 thư mục được dẫn không kèm; kích thước 34 M, 8,3 M, 170 M KHÔNG ĐO ĐƯỢC và đơn vị M chưa rõ. Script tối thiểu có thể tách khỏi clone; không giả phục hồi được công cụ gốc. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bs-pham-vi-khong-no-va-da-va  [P3]  Bảng bỏ phạm vi của lời không nợ và đã vá thật
TỆP/DÒNG: LAND:32–33,99; README:269.

VẤN ĐỀ: Số có thể được bắt nhưng lượng từ/phạm vi logic của lời khai không được biểu diễn. Theo yêu cầu chủ kho, khẳng định bị bảng bỏ sót vẫn tính finding kể cả giá trị đúng.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — bổ sung vào BẢNG ĐO và phụ lục hit trong VERDICT.md, không sửa hiện vật reviewer.

ĐÃ THỬ NGHIỆM: python3 -B do-luot1/audit.py; Đối chiếu 3/3 kết luận trong V6 và sửa khung ở LAND cũ; câu không nợ chỉ áp cho head PR #478. Không xóa nợ PR #486 hoặc P3 README gốc. Tái lập bộ lọc 193/193 hit. Cách khóa: đối chiếu theo trường/ý nghĩa thay vì chỉ thêm vài đơn vị vào regex.

ĐỘ TIN: cao.

### bang-193-hit-khong-phai-193-menh-de  [P3]  Số lượng hit regex bị đặt tên như số khẳng định độc lập
TỆP/DÒNG: BANG-KHANG-DINH.tsv:1–196; trich_khang_dinh.py:19–50; PROMPT.md:85.

VẤN ĐỀ: Tái sinh được 193 hit nhưng cùng comment ID bị bắt thành sha và id, ngày trong tên thư mục cũng thành SHA/ID, “#478 lượt 4” sinh “478 lượt”, revision 1/2/3/4 sinh hai tỷ số. Đơn vị thực là hit regex. Tự khai bảng thiếu không chữa được việc gọi hit giả là mệnh đề định lượng; chỉ dùng nó như chỉ mục ứng viên.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — phụ lục giữ đủ hit gốc và gán lại ngữ nghĩa.

ĐÃ THỬ NGHIỆM: audit.py tái sinh 3/3 nhóm, 193/193 hit. Phụ lục phân loại mỗi hit đúng 1 ô và không đếm SHA/ID trùng thành phép đo độc lập.

ĐỘ TIN: cao.

### tong-diff-goi-lech-bon-dong  [P3]  Tổng dòng thêm trong prompt thiếu bốn dòng so với Git và chính bảng thành phần
TỆP/DÒNG: PROMPT.md:31,35–40.

VẤN ĐỀ: Tổng 1674 dòng thêm không khớp git diff. Cộng số thành phần được giao cũng ra 1678 dòng thêm. Đây là lỗi phần giao gói, không phải verdict reviewer hoặc thay đổi mã trong PR.

ĐÃ THỬ VÁ: không sửa tệp kho — đã bổ sung đối chiếu trong bảng/phụ lục; cách sửa bộ giao gói và ca khóa nêu bên dưới.

GÓI VÁ: KHÔNG — sửa số tổng trong lần giao gói kế; giá trị đúng đã ghi trong verdict.

ĐÃ THỬ NGHIỆM: git -C cay-kho diff --numstat c87b067 da481f9; 8/8 hàng thành phần khớp; tổng 1678 dòng thêm, 0 dòng xoá; sai 4 dòng thêm.

ĐỘ TIN: cao.

## PHỤ LỤC — PHÂN LOẠI TỪNG HIT TRONG TSV

Tái sinh **193/193 hit**, gồm 86 hit LAND, 25 hit README và 82 hit receipt. Số dòng README trong TSV là dòng của đoạn trích, đã ánh xạ sang dòng 269–271 của tệp thật. Số dòng receipt là dòng của 3 tệp nối tiếp, mỗi tệp 134 dòng; phụ lục ánh xạ lại từng tệp. Giữ cả hit giả/trùng để người đọc kiểm độ phủ; chúng không là finding mới hay phép đo độc lập. Khi một hit nằm trong mệnh đề rộng hơn, BẢNG ĐO ở trên tách riêng phần quan hệ/phạm vi. Tệp TSV đầy đủ ở [do-luot1/doi-chieu-193-hit.tsv](do-luot1/doi-chieu-193-hit.tsv).

| mục | tệp:dòng | hit gốc | nghĩa/phép đối chiếu | ô | khớp? |
|---|---|---|---|---|---|
| 1 hit | LAND:8 | 478 lượt | Hit nhầm số hiệu PR thành số lượt; văn bản nguồn nhắc PR #478, không khai 478 lượt. | ĐO ĐƯỢC + KHỚP | có |
| 2 hit | LAND:23 | sha:ff3431f11bc0ba3ffa0c3616003f833c3cfc3ebb | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 3 hit | LAND:25 | sha:5137165112 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 4 hit | LAND:25 | id:5137165112 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 5 hit | LAND:28 | sha:ff3431f | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 6 hit | LAND:29 | sha:5137106684 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 7 hit | LAND:29 | id:5137106684 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 8 hit | LAND:30 | sha:5137165112 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 9 hit | LAND:30 | id:5137165112 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 10 hit | LAND:31 | sha:745d888 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 11 hit | LAND:31 | sha:17f4a1b | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 12 hit | LAND:40 | sha:c87b0679a837055ee4cc33ac48c9adb8d7ad8784 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 13 hit | LAND:48 | sha:c87b067 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 14 hit | LAND:49 | sha:585c7d5 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 15 hit | LAND:49 | sha:ff3431f | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 16 hit | LAND:53 | sha:ff3431f | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 17 hit | LAND:60 | sha:ff3431f11bc0ba3ffa0c3616003f833c3cfc3ebb | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 18 hit | LAND:63 | 6 lượt | Chỉ số lượt cuối là lượt 6; có 3/3 verdict gốc được lưu cho lượt 4/5/6. | ĐO ĐƯỢC + KHỚP | có |
| 19 hit | LAND:68 | 478 lượt | Hit nhầm số hiệu PR thành số lượt; văn bản nguồn nhắc PR #478, không khai 478 lượt. | ĐO ĐƯỢC + KHỚP | có |
| 20 hit | LAND:78 | sha:5a4dd859ef791ca046aea3af4bab2731883323ec | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 21 hit | LAND:79 | sha:9337779b7d61d3b08947982383081de127e7d632 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 22 hit | LAND:80 | sha:ff3431f11bc0ba3ffa0c3616003f833c3cfc3ebb | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 23 hit | LAND:85 | 0 comment | Số lịch sử get_comments/all-refs chưa tái lập được; hiện tại 7 đường dẫn mới không bác lần quét cũ. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 24 hit | LAND:85 | 0 đường dẫn | Số lịch sử get_comments/all-refs chưa tái lập được; hiện tại 7 đường dẫn mới không bác lần quét cũ. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 25 hit | LAND:86 | sha:8f7becb | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 26 hit | LAND:86 | sha:260f7c6 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 27 hit | LAND:86 | sha:5a4dd85 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 28 hit | LAND:87 | 478 lượt | Hit nhầm số hiệu PR thành số lượt; văn bản nguồn nhắc PR #478, không khai 478 lượt. | ĐO ĐƯỢC + KHỚP | có |
| 29 hit | LAND:87 | 1/2 | Hit nhầm số hiệu PR thành số lượt; văn bản nguồn nhắc PR #478, không khai 478 lượt. | ĐO ĐƯỢC + KHỚP | có |
| 30 hit | LAND:92 | 14/15 | Chỉ số lượt PR #468 và lời chỉ có blob là nguồn lịch sử; GitHub comment không đo được. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 31 hit | LAND:95 | sha:5598591753 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 32 hit | LAND:95 | id:5598591753 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 33 hit | LAND:102 | 44/4 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 34 hit | LAND:106 | sha:585c7d5 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 35 hit | LAND:107 | sha:17f4a1b | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 36 hit | LAND:108 | sha:20260907 | Hit nhầm ngày trong tên đường dẫn thành SHA/ID; đường dẫn nguồn có thật, không là commit ID. | ĐO ĐƯỢC + KHỚP | có |
| 37 hit | LAND:108 | id:20260907 | Hit nhầm ngày trong tên đường dẫn thành SHA/ID; đường dẫn nguồn có thật, không là commit ID. | ĐO ĐƯỢC + KHỚP | có |
| 38 hit | LAND:110 | sha:ff3431f | Có commit ff3431f không chứng minh suite CI checkout exact head; finding P1. | KHAI RỘNG HƠN PHÉP ĐO | không |
| 39 hit | LAND:115 | 44 bước | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 40 hit | LAND:115 | 3 skipped | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 41 hit | LAND:115 | sha:34183412163 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 42 hit | LAND:115 | id:34183412163 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 43 hit | LAND:116 | 0 bước | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 44 hit | LAND:116 | 0 hỏng | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 45 hit | LAND:116 | sha:34185388550 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 46 hit | LAND:116 | id:34185388550 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 47 hit | LAND:117 | 5 bước | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 48 hit | LAND:117 | 0 null | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 49 hit | LAND:117 | 0 hỏng | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 50 hit | LAND:123 | sha:34183411154 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 51 hit | LAND:123 | id:34183411154 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 52 hit | LAND:133 | sha:c87b067 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 53 hit | LAND:136 | sha:ff3431f | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 54 hit | LAND:136 | sha:c87b067 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 55 hit | LAND:136 | sha:585c7d5 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 56 hit | LAND:138 | sha:20260908 | Hit nhầm ngày trong tên đường dẫn thành SHA/ID; đường dẫn nguồn có thật, không là commit ID. | ĐO ĐƯỢC + KHỚP | có |
| 57 hit | LAND:138 | id:20260908 | Hit nhầm ngày trong tên đường dẫn thành SHA/ID; đường dẫn nguồn có thật, không là commit ID. | ĐO ĐƯỢC + KHỚP | có |
| 58 hit | LAND:142 | sha:34185511309 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 59 hit | LAND:142 | sha:c87b067 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 60 hit | LAND:142 | id:34185511309 | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 61 hit | LAND:143 | 44 bước | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 62 hit | LAND:143 | 4 skipped | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 63 hit | LAND:143 | 0 null | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 64 hit | LAND:143 | 0 hỏng | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 65 hit | LAND:144 | 44 bước | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 66 hit | LAND:144 | 6 skipped | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 67 hit | LAND:144 | 0 null | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 68 hit | LAND:144 | 0 hỏng | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 69 hit | LAND:146 | 4 skipped | 4 skipped/6 skipped là 2 job API; không có raw, không suy sai từ chênh lệch. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 70 hit | LAND:146 | 6 skipped | 4 skipped/6 skipped là 2 job API; không có raw, không suy sai từ chênh lệch. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 71 hit | LAND:150 | 121/121 | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 72 hit | LAND:150 | rc=0 | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 73 hit | LAND:152 | rc=0 | Hành vi thiếu shellcheck không tái thử; mã thoát 0 không phải bằng chứng dương. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 74 hit | LAND:155 | 0 vi phạm | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 75 hit | LAND:155 | 30 ĐẠT | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 76 hit | LAND:155 | 11/11 | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 77 hit | LAND:155 | rc=0 | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 78 hit | LAND:157 | rc=0 | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 79 hit | LAND:157 | ok:true | Kết quả gate lịch sử không có raw tương ứng; không chuyển kết quả đo mới sang lần cũ; ràng buộc chủ kho. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 80 hit | LAND:166 | 0 comment | Số lịch sử get_comments/all-refs chưa tái lập được; hiện tại 7 đường dẫn mới không bác lần quét cũ. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 81 hit | LAND:166 | 0 đường dẫn | Số lịch sử get_comments/all-refs chưa tái lập được; hiện tại 7 đường dẫn mới không bác lần quét cũ. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 82 hit | LAND:191 | 1/2 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 83 hit | LAND:191 | 3/4 | Đối chiếu nội dung/commit/số học hoặc trường lease ở BẢNG ĐO; chỉ đúng phạm vi nguồn cục bộ. | ĐO ĐƯỢC + KHỚP | có |
| 84 hit | LAND:196 | sha:20260907 | Hit nhầm ngày trong tên đường dẫn thành SHA/ID; đường dẫn nguồn có thật, không là commit ID. | ĐO ĐƯỢC + KHỚP | có |
| 85 hit | LAND:196 | id:20260907 | Hit nhầm ngày trong tên đường dẫn thành SHA/ID; đường dẫn nguồn có thật, không là commit ID. | ĐO ĐƯỢC + KHỚP | có |
| 86 hit | LAND:203 | 2 comment | Sự kiện/mã định danh GitHub hoặc invocation lịch sử; không mạng và không raw phù hợp. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 87 hit | README:269 | 981 s | Thời lượng lần chạy thật không đo được; riêng phép làm tròn từ mốc receipt khớp, xem BẢNG ĐO. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 88 hit | README:269 | 3 P1 | Lời tóm tắt về verdict được đối chiếu với V6; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 89 hit | README:269 | 23 P3 | Lời tóm tắt về verdict được đối chiếu với V6; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 90 hit | README:269 | 309 ref | Inventory gói lịch sử không kèm; 312 refs hiện tại không bác 309 refs cũ. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 91 hit | README:269 | 22/23 | Lời tóm tắt về verdict được đối chiếu với V6; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 92 hit | README:269 | sha:ff3431f1 | Lời tóm tắt về verdict được đối chiếu với V6; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 93 hit | README:269 | sha:ff3431f | Lời tóm tắt về verdict được đối chiếu với V6; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 94 hit | README:269 | sha:5578806787 | Comment ID do điều phối khai; cú pháp URL/ID không chứng minh tồn tại hoặc nội dung. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 95 hit | README:269 | id:5578806787 | Comment ID do điều phối khai; cú pháp URL/ID không chứng minh tồn tại hoặc nội dung. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 96 hit | README:270 | 1239 s | Thời lượng lần chạy thật không đo được; riêng phép làm tròn từ mốc receipt khớp, xem BẢNG ĐO. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 97 hit | README:270 | 44 bước | Lời tóm tắt về verdict được đối chiếu với V5; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 98 hit | README:270 | 309 ref | Inventory gói lịch sử không kèm; 312 refs hiện tại không bác 309 refs cũ. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 99 hit | README:270 | 44/4 | Lời tóm tắt về verdict được đối chiếu với V5; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 100 hit | README:270 | sha:9337779b | Lời tóm tắt về verdict được đối chiếu với V5; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 101 hit | README:270 | sha:5598591753 | Comment ID do điều phối khai; cú pháp URL/ID không chứng minh tồn tại hoặc nội dung. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 102 hit | README:270 | id:5598591753 | Comment ID do điều phối khai; cú pháp URL/ID không chứng minh tồn tại hoặc nội dung. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 103 hit | README:271 | 1246 s | Thời lượng lần chạy thật không đo được; riêng phép làm tròn từ mốc receipt khớp, xem BẢNG ĐO. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 104 hit | README:271 | 1 tệp | Lời tóm tắt về verdict được đối chiếu với V4; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 105 hit | README:271 | 13 P3 | Lời tóm tắt về verdict được đối chiếu với V4; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 106 hit | README:271 | 309 ref | Inventory gói lịch sử không kèm; 312 refs hiện tại không bác 309 refs cũ. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 107 hit | README:271 | 11/13 | Lời tóm tắt về verdict được đối chiếu với V4; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 108 hit | README:271 | rc=1 | Lời tóm tắt về verdict được đối chiếu với V4; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 109 hit | README:271 | sha:5a4dd859 | Lời tóm tắt về verdict được đối chiếu với V4; không tái xác thực lần chạy lịch sử trong verdict. | ĐO ĐƯỢC + KHỚP | có |
| 110 hit | README:271 | sha:5577923821 | Comment ID do điều phối khai; cú pháp URL/ID không chứng minh tồn tại hoặc nội dung. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 111 hit | README:271 | id:5577923821 | Comment ID do điều phối khai; cú pháp URL/ID không chứng minh tồn tại hoặc nội dung. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 112 hit | R4:3 | 0 P1 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 113 hit | R4:3 | 3 P2 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 114 hit | R4:3 | 13 P3 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 115 hit | R4:4 | 13 P3 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 116 hit | R4:4 | 11/13 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 117 hit | R4:7 | 14/15 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 118 hit | R4:9 | sha:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 119 hit | R4:9 | id:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 120 hit | R4:15 | sha:20260908 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 121 hit | R4:15 | sha:c80b9494 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 122 hit | R4:15 | id:20260908 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 123 hit | R4:30 | sha:5a4dd859ef791ca046aea3af4bab2731883323ec | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 124 hit | R4:31 | sha:718fc41272cf7f9aaa004a70041906aad64a03d0 | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 125 hit | R4:32 | sha:5577923821 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 126 hit | R4:32 | id:5577923821 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 127 hit | R4:34 | sha:718fc41 | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 128 hit | R4:35 | sha:20260909 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 129 hit | R4:35 | id:20260909 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 130 hit | R4:56 | 14/15 | Số hiệu lượt 14/15 dẫn receipt cũ có trong kho; không là tỷ số và không làm nguồn runtime cho lượt mới. | ĐO ĐƯỢC + KHỚP | có |
| 131 hit | R4:60 | sha:c80b9494 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 132 hit | R4:61 | sha:c80b9494f4ec46318792a6331be42775 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 133 hit | R4:72 | sha:1164648 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 134 hit | R4:77 | sha:394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Commit gốc cục bộ khớp mã được khai; không chứng minh launcher thực đã kiểm nó. | ĐO ĐƯỢC + KHỚP | có |
| 135 hit | R4:77 | sha:5a4dd859ef791ca046aea3af4bab2731883323ec | Đối số expected-head trong lời khai trùng reviewed SHA; việc lệnh thực được gọi không đo được. | ĐO ĐƯỢC + KHỚP | có |
| 136 hit | R4:80 | sha:394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Commit gốc cục bộ khớp mã được khai; không chứng minh launcher thực đã kiểm nó. | ĐO ĐƯỢC + KHỚP | có |
| 137 hit | R4:99 | 309 ref | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 138 hit | R4:123 | sha:5577923821 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 139 hit | R4:123 | id:5577923821 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 140 hit | R5:3 | 3 P1 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 141 hit | R5:3 | 0 P2 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 142 hit | R5:3 | 17 P3 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 143 hit | R5:7 | 14/15 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 144 hit | R5:9 | sha:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 145 hit | R5:9 | id:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 146 hit | R5:15 | sha:20260908 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 147 hit | R5:15 | sha:a59fff06 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 148 hit | R5:15 | id:20260908 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 149 hit | R5:30 | sha:9337779b7d61d3b08947982383081de127e7d632 | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 150 hit | R5:31 | sha:718fc41272cf7f9aaa004a70041906aad64a03d0 | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 151 hit | R5:32 | sha:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 152 hit | R5:32 | id:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 153 hit | R5:34 | sha:718fc41 | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 154 hit | R5:35 | sha:20260909 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 155 hit | R5:35 | id:20260909 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 156 hit | R5:56 | 14/15 | Số hiệu lượt 14/15 dẫn receipt cũ có trong kho; không là tỷ số và không làm nguồn runtime cho lượt mới. | ĐO ĐƯỢC + KHỚP | có |
| 157 hit | R5:60 | sha:a59fff06 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 158 hit | R5:61 | sha:a59fff06c2bd49d9a9bba329a60286dd | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 159 hit | R5:77 | sha:394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Commit gốc cục bộ khớp mã được khai; không chứng minh launcher thực đã kiểm nó. | ĐO ĐƯỢC + KHỚP | có |
| 160 hit | R5:77 | sha:9337779b7d61d3b08947982383081de127e7d632 | Đối số expected-head trong lời khai trùng reviewed SHA; việc lệnh thực được gọi không đo được. | ĐO ĐƯỢC + KHỚP | có |
| 161 hit | R5:80 | sha:394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Commit gốc cục bộ khớp mã được khai; không chứng minh launcher thực đã kiểm nó. | ĐO ĐƯỢC + KHỚP | có |
| 162 hit | R5:99 | 309 ref | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 163 hit | R5:123 | sha:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 164 hit | R5:123 | id:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 165 hit | R6:3 | 0 P1 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 166 hit | R6:3 | 0 P2 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 167 hit | R6:3 | 23 P3 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 168 hit | R6:4 | 1 lượt | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 169 hit | R6:4 | 23 P3 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 170 hit | R6:4 | 22/23 | Đếm tiêu đề finding hoặc nội dung verdict; khớp số công bố. | ĐO ĐƯỢC + KHỚP | có |
| 171 hit | R6:7 | 14/15 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 172 hit | R6:9 | sha:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 173 hit | R6:9 | id:5598591753 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 174 hit | R6:15 | sha:20260908 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 175 hit | R6:15 | sha:f6f41250 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 176 hit | R6:15 | id:20260908 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 177 hit | R6:30 | sha:ff3431f11bc0ba3ffa0c3616003f833c3cfc3ebb | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 178 hit | R6:31 | sha:718fc41272cf7f9aaa004a70041906aad64a03d0 | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 179 hit | R6:32 | sha:5578806787 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 180 hit | R6:32 | id:5578806787 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 181 hit | R6:34 | sha:718fc41 | Reviewed SHA / commit ghim / blob và ancestry khớp Git; 3/3 verdict. | ĐO ĐƯỢC + KHỚP | có |
| 182 hit | R6:35 | sha:20260909 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 183 hit | R6:35 | id:20260909 | Hit là ngày trong tên receipt/nhánh, không phải SHA; tên cục bộ khớp. | ĐO ĐƯỢC + KHỚP | có |
| 184 hit | R6:56 | 14/15 | Số hiệu lượt 14/15 dẫn receipt cũ có trong kho; không là tỷ số và không làm nguồn runtime cho lượt mới. | ĐO ĐƯỢC + KHỚP | có |
| 185 hit | R6:60 | sha:f6f41250 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 186 hit | R6:61 | sha:f6f412507630470f9a996b09d7382e8e | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 187 hit | R6:72 | sha:1062732 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 188 hit | R6:77 | sha:394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Commit gốc cục bộ khớp mã được khai; không chứng minh launcher thực đã kiểm nó. | ĐO ĐƯỢC + KHỚP | có |
| 189 hit | R6:77 | sha:ff3431f11bc0ba3ffa0c3616003f833c3cfc3ebb | Đối số expected-head trong lời khai trùng reviewed SHA; việc lệnh thực được gọi không đo được. | ĐO ĐƯỢC + KHỚP | có |
| 190 hit | R6:80 | sha:394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Commit gốc cục bộ khớp mã được khai; không chứng minh launcher thực đã kiểm nó. | ĐO ĐƯỢC + KHỚP | có |
| 191 hit | R6:99 | 309 ref | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 192 hit | R6:123 | sha:5578806787 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |
| 193 hit | R6:123 | id:5578806787 | Run ID/byte stderr/inventory/comment hay lời vận chuyển lịch sử không có hiện vật độc lập; xem giới hạn nguồn. | KHÔNG ĐO ĐƯỢC | chưa xác minh |

## BẰNG CHỨNG VÀ GIỚI HẠN CHẠY

- [audit.py](do-luot1/audit.py), chạy `python3 -B do-luot1/audit.py`: [audit-result.json](do-luot1/audit-result.json) ghi **45/45 phép so hiện vật**, **3/3 nhóm extractor**, `ok: true`; [facts.json](do-luot1/facts.json) giữ số đo, trường lease, topology và kết quả từng phép so.
- [short_checks.py](do-luot1/short_checks.py), chạy `python3 -B do-luot1/short_checks.py`: [short-checks.json](do-luot1/short-checks.json), stdout/stderr kèm theo. Doc `ok: true`, doctrine **7/7 tệp**, ADR **46/46 dòng**. Chỉ là phép đo mới trên reviewed SHA, không hợp thức hoá run lịch sử.
- [build_hints.py](do-luot1/build_hints.py), chạy `python3 -B do-luot1/build_hints.py`: [hints-check.json](do-luot1/hints-check.json), **8/8 kiểm tra cấu trúc/metadata**, `ok: true`; 5/5 tệp YAML đọc được, 3/3 receipt giữ nguyên 8 trường neo/đếm hiện vật. Đây không phải chạy validator của kho trên cây thật.
- Không chạy lease suite dài, CI, phép thử runtime lịch sử hoặc validator ngoài danh sách lệnh chủ kho cho phép. Các kết quả không đóng bằng phép ngắn đã ghi **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)** cùng lý do trong bảng. Không nâng timeout 60 phút trong workflow.
- `git -C cay-kho status --porcelain` cuối lượt trả **0 byte**; [final-check.json](do-luot1/final-check.json) ghi **21/21 phép kiểm**, `ok: true`, bao gồm head/refs/tag giữ nguyên và đối chiếu gói vá. Lệnh tái lập: `python3 -B do-luot1/final_check.py`. Cổng xanh không chứng minh lời khai đúng; metadata schema và băm không xác thực identity hoặc trạng thái GitHub.
