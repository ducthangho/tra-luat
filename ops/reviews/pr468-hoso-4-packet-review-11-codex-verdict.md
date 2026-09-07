# VERDICT — cross-review PR #468, lượt 10

verdict: changes_requested
reviewed_sha: c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355

Kết luận: **changes_requested — 1 P1, 2 P2**. Đối chiếu năm finding lượt 9: **2 ĐÃ VÁ THẬT · 1 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**.

Reviewer: Codex / OpenAI, phiên độc lập qua API, có shell cục bộ. Transport: tệp trong sandbox. Phạm vi đóng theo PROMPT; không mạng, không commit/push, không đăng GitHub. Đường `ops/...` tính từ `cay-kho/`. Đây chưa phải merge authorization.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1]: **CHƯA VÁ** tại 2026-09-07T11:37:58.336896+00:00. Tự quét 90 cặp `(blob,path)`: registry có 2 người giữ (#456 + exec-1r4), ci.yml có 1. Blob #456 chưa bia mộ trên `origin/master` = `8b2103c06687546379a17f6deafc97f1fe0173fd`. Chuỗi #456 → exec-1 → r2 → r3 → r4 có 4/4 cạnh YAML hai chiều trên cây PR (đọc cả bốn lease GATE). Mô phỏng 14:30:06Z/07Z/08Z: registry 2/1/1; ci.yml 1/1/1. Mô hình đặt bia mộ mọi bản #456 cũng đưa registry về 1. Đây là mô phỏng, chưa phải readback sau hạn. Hiện vật: `do-review10/snapshot.json`.

- `manifest-luot8-liet-ke-hien-vat-khong-duoc-giao` [P2]: **VÁ SINH LỖI MỚI** trong gói bàn giao kế tiếp. Lượt8 đã vá thật: `sha256sum -c` rc=0, 69/69. Nhưng gói lượt 9 có đúng 111 tệp thường mà thiếu chính 19 tệp `artifact-repair/rig/...` reviewer lượt 9 đã phục dựng; manifest con vẫn liệt kê chúng và log lịch sử khai rc=0,69/69. Chạy trên cây hiện tại: rc=1,50/69. Tìm được 19/19 byte gốc ở lượt 8; dựng bản sao ngoài checkout đưa gói con về rc=0,69/69. Giữ nguyên slug vì cùng lỗi sao chép hiện vật. Hiện vật: `do-review10/artifact-checks.json`.

- `a2-neo-nen-cu-trai-write-set-hien-tai` [P2]: **ĐÃ VÁ THẬT**. Hàng bảng thứ tự :395 chỉ cho hai run 39 bước làm đối chiếu lịch sử A1/A5; nền A2 là dispatch trước tách tại `start_from_sha`. Khối A2 r3/r4 bằng byte, yêu cầu cùng base/event/lane, không cho dùng lượt khác lane. Chạy lại mô hình trên nền lease 40 bước: dispatch 88/88 bộ ba, PR ubuntu 44/44 QUA; bỏ receipt-v2 mất 2/1 bộ ba, đều ĐỎ. So sai lane lệch 4 thêm/4 mất. Hiện vật: `contract-checks.json`, `prose-checks.json`.
- `bien-do-khac-head-khong-phai-nhieu-runner` [P2]: **VÁ HỜ về đồng bộ hợp đồng**. Toàn GATE r4 và Issue #463 đã phân biệt đúng mẫu, lịch sử và biên thiết kế; A1≤25,00/A5≤135,00 giữ nguyên. Nhưng `viec_trong_lease` r4 :162–164 vẫn dùng “111,08 để đối chiếu nhiễu”, là việc hiện hành, trái spec r4 :103–107/:540. Tự đo hai tree bằng nhau,0 path đổi nhưng event dispatch/push và lane WORKER/LAND khác,86/86 bộ ba với +4/−4; chênh job0,916667/2,266667 phút không tách được nhiễu runner. Thử sửa đúng 1 mỏ neo ở bản sao, giữ ngưỡng và metadata. Hiện vật: `prose-checks.json`, `gate-prose-scan.txt`.
- `quyet-dinh-tiep-h-con-bi-phu-dinh` [P2]: **ĐÃ VÁ THẬT**. Quét toàn văn ba hồ sơ và đọc ngữ cảnh: phần mở đầu :56–59 gắn phủ định với lịch sử lượt 4–7 rồi ghi hiện tại đã chọn1; hàng H :157 ghi đã chọn. Không còn hai phủ định hiện hành của lượt 9. URL quyết định đúng 3/3, Đ1–Đ5 đủ 5/5 và bằng byte bản trước, nháp vẫn 5 null, 2 khối Python H bằng byte. Các câu về selector “không được chọn” hoặc điều kiện ghi lựa chọn vào lease không phủ định quyết định thiết kế. Hiện vật: `h-prose-scan.txt`, `contract-checks.json`, `prose-checks.json`.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| HEAD / abbrev / trạng thái ban đầu | exact reviewed_sha; abbrev=7; sạch | c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355; 7; status rỗng | có |
| Snapshot lease tại 2026-09-07T11:37:58.336896+00:00 | registry=2; ci.yml=1 | 90 cặp blob/path; registry=2; ci.yml=1; 4/4 cạnh thay thế hai chiều | có; P1 mở |
| Hết hạn #456 (mô phỏng) | 14:30:07Z ngày 07-09 | 14:30:06Z/07Z/08Z: registry 2/1/1; ci.yml 1/1/1 | có trong mô hình |
| Diff since9 | patch/numstat đã giao | 141 tệp; +34464/−23; patch và numstat khớp byte; ngoài ops=0 | có |
| Diff full | patch/numstat đã giao | 350 tệp; +90207/−0; patch và numstat khớp byte; ngoài ops=0 | có |
| Spec/lease/Issue #463 | revision 4; hash khai trong lease | `4c542f6b931f62687edd6dca0c5f22c0399ad41f4e80b48e29cdfcd519289cd8`; hash/alias/Issue/blob commit đều khớp; bản chiếu khớp; null=0 | có |
| Spec/lease/Issue #464 | revision 1; hash khai trong lease | `66dcb20d7bc044cc3185074b56152f0f7f737ac2d1a49c225c29a29b144b4917`; hash/alias/Issue/blob commit đều khớp; bản chiếu khớp; null=5 | có |
| Spec/lease/Issue #465 | revision 1; hash khai trong lease | `2abace8588ec2b4e0626c1c77e9c3e0f7e713ecb2ce528b149e6c7f1f0000759`; hash/alias/Issue/blob commit đều khớp; bản chiếu khớp; null=5 | có |
| Spec/lease/Issue #466 | revision 1; hash khai trong lease | `417dce16227687cbb1e642284f39d2f847a617b2d730f7f52aaa58f33c936521`; hash/alias/Issue/blob commit đều khớp; bản chiếu khớp; null=5 | có |
| Lease r4 | 1440 phút; heartbeat=mốc cấp; until=expires; 2 path | 10:17:12Z 07-09 → 10:17:12Z 08-09; 1440 phút; hash write set `0f7b869da648e9b21023e461925efd0d45bca58fb308a8fcc82bc55ad9f66ef0`; ba neo=d28c4b1 | có |
| Receipt lượt 9 (byte/neo) | v2; 29806 B; SHA lượt 9 | 29806 B; SHA256 `fa11cdcfb3fa43d5b54eca50cffd2d8ddf1e8e988db8b778f991a0b924589ec0`; blob 1a33030 đúng; bản chiếu đúng | có; schema v2 đã qua cổng |
| Manifest lượt 6 / lượt 7 / lượt 8 | đầy đủ | rc=0 cả ba; 62/62,66/66,69/69 | có |
| Gói lượt 9 | 111 tệp chép nguyên; reviewer đã phục dựng 69/69 | 111 tệp thường,0 symlink; manifest con `artifact-repair/` rc=1,50/69,thiếu19 | số111 khớp; gói thiếu |
| Phục dựng gói con lượt 9 ngoài checkout | ca khóa manifest phải qua | tìm19/19 bản đúng hash ở lượt 8; bản phục dựng rc=0,69/69 | có trong thử nghiệm |
| A2 r3/r4 | cùng base/event/lane; nền lease 40 bước | khối A2 bằng byte; bảng thứ tự r4 rút nền 39 bước khỏi A2 | có |
| A2 dispatch / PR ubuntu (mô hình) | đủ bước QUA, mất bước ĐỎ | 88/88 và44/44 QUA; bỏ receipt-v2 mất 2/1 bộ ba,ĐỎ; so sai lane+4/−4,ĐỎ | có trong mô hình |
| Hai run lịch sử | cùng tree, khác event/lane | 0 path đổi;86/86 bộ ba,+4/−4; dispatch nhánh426bfc0 so push master1b3caa1 | có |
| Thời lượng nhánh/master | ubuntu24,25/26,52; Windows43,20/42,28 | ubuntu24,25/26,516667; Windows43,20/42,283333 phút | có sau làm tròn |
| Chênh job hai run | 0,92/2,27 phút | Windows0,916667; ubuntu2,266667 | có; không đo được phần runner |
| Mẫu 11 run | 5master+6nhánh;1×39+10×40 bước | đúng 11;5push master+6nhánh;1×39+10×40 bước YAML | có |
| Thống kê Windows mẫu 11 | min40,20/max50,48/biên10,28/median46,02/mean45,84 | 40,200000/50,483333/10,283333/46,016667/45,837879 phút | có sau làm tròn |
| Ngưỡng A1/A5 | ≤25,00 và≤135,00 | giữ nguyên,biên được gọi là thiết kế trong spec; lease còn1 câu “đối chiếu nhiễu” | ngưỡng khớp;câu lease sai |
| Thử đồng bộ lease r4 ngoài checkout | gỡ câu nhiễu,giữ hợp đồng |1 neo duy nhất,1 mục viec_trong_lease đổi;ngưỡng135,00,authority,băm,mốc giữ nguyên | có trong thử nghiệm |
| Quyết định H | chọn1;lease chưa cấp;Đ1–Đ5 ràng buộc | URL3/3;5 điều kiện bằng byte;5 null;2 khối Python bằng byte;0 phủ định hiện hành đã nêu | có |
| lease_publish check r4 | rc0 | rc0,ĐĂNG ĐƯỢC;không chạy2 lớp GitHub (tool tự khai) | có;không chứng nhận A9/authority |
| lease_publish_test |121/121 |rc0,121/121,đã chạy121,bỏ qua0 | có |
| bien_nhan_v2 |TỔNG ĐẠT |rc0;24 v2 ĐẠT,11/11 legacy,42 nợ đóng băng,tổng77,0 vi phạm,0 không đo được | có về schema |
| doctrine-scan / adr-song |rc0/rc0,46/46 |rc0;7 tệp,0 chép doctrine / rc0;46 ADR,46 dòng,khớp1–1 | có |
| doc-claims-check strict |rc0,ok:true |rc0,ok:true | có |
| HEAD/tree và môi trường | SHA được giao; không shallow | tree `799a4b2549d68c6a3ad44cc70f9257e794cd1db8`; shallow=false; origin là HTTPS GitHub, không gọi mạng | có |
| Bốn bản chiếu lease GATE | r1/r2/r3/r4 khớp cây | 4/4 bằng byte; bia mộ r3 lúc10:17:12Z trùng cấp r4 và cùng URL authority | có |
| Neo commit Issue #463/#464 | `1a330305e20a0667fff4954f8542aadd5e375b50` | cả2 blob tại commit này khớp spec hiện tại | có |
| Phản mô hình A2 cũ | nền 39 bước so lease 40 bước gây sai | 86/88 bộ ba: nền cũ bác tách đủ nhưng nhận khi bỏ2 bộ ba receipt-v2; A2 r4 cho kết quả ngược lại | có trong mô hình |
| Nền PR lấy từ dữ liệu lưu | PR có YAML bằng byte nền lease | 3 ứng viên khớp; chọn run34058508426/head82e01a4 gần nhất trong dữ liệu đã giao | có; không khẳng định gần nhất trên GitHub |
| EOL policy toàn cây | EVIDENCE chỉ khai staged ok | rc=0,ok=true; scanned1190,checked1168,skipped22 theo policy,0 vi phạm | mở rộng kiểm,đạt |
| Script tự đo lượt 10 | chạy thật | static_checks,artifact_checks,contract_checks,prose_checks đều rc=0; rc=1 của manifest con được lưu riêng | có |
| Authority/comment r4 | neo r3/5568696936; r4 chưa đăng được | spec,lease và EVIDENCE cùng khai chưa có comment riêng r4; không có readback comment trong bundle | nhất quán; sự kiện/quyền KHÔNG ĐO ĐƯỢC |
| Runtime receipt lượt 9 | model gpt-6-astra;1170,677s;stdout700117B | schema chấp nhận; session/stdout gốc không được giao trong phạm vi này | KHÔNG ĐO ĐƯỢC độc lập |
| Kiểm cuối 2026-09-07T11:50:17.131690+00:00 | cây read-only, exact SHA | HEAD/tree đúng; status/diff/index rỗng; 0 commit sau reviewed_sha | có |
| Manifest hiện vật lượt 10 | chỉ tệp thường, không tmp/symlink | 128/128 tệp khớp SHA-256; gồm VERDICT và hiện vật tự tạo | có |

### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Bản #456 trên ref khác vẫn giữ write set trước hạn

TỆP/DÒNG: `ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml:39` trên `origin/master`, blob `8b2103c06687546379a17f6deafc97f1fe0173fd`; `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:579` (A9); lease r4 `:125` (`thay_the_cho`).

VẤN ĐỀ: Tại 2026-09-07T11:37:58.336896Z, quét snapshot bằng công cụ thật có 90 cặp `(blob,path)`. #456 có hai blob: một đã mang bia mộ trên cây PR, một chưa mang bia mộ vẫn có trên `origin/master` và ref khác. Registry có hai người giữ (#456 và exec-1r4), trái A9 phải còn đúng một. Bốn cạnh #456 → exec-1 → r2 → r3 → r4 đều đúng hai chiều trên cây PR, nhưng không thu hồi bản cũ trên ref khác. `check` r4 vẫn rc=0. EVIDENCE tự khai đúng việc này; đây là finding trạng thái chưa được đóng, không phải cáo buộc executor đã bắt tay trái A9.

ĐÃ THỬ VÁ: Có, mô hình trong bộ nhớ đặt bia mộ #456 → exec-1 cho mọi bản #456, giữ nguyên chuỗi r1/r2/r3/r4: registry từ 2 về 1. Hướng sửa trên kho thật: chủ kho hoàn tất thu hồi/cập nhật mọi ref còn blob cũ rồi fetch/readback, hoặc đo lại sau 14:30:07Z khi #456 hết hạn. Ca khóa: trên cả hai đường write set, công cụ chỉ còn một người giữ là lease r4 và không còn bản #456 CÒN_HẠN chưa bia mộ. Rủi ro: chỉ sửa master hoặc chỉ đọc cây PR bỏ sót ref khác; không đổi bừa tên người kế nhiệm làm gãy chuỗi; mô phỏng hết hạn không thay được readback thật. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review10/static_checks.py` rc=0, gọi `_quet_lease_toan_kho(..., doi_chieu_ref=False)` rồi dùng `_phan_loai_lease`, `_bia_mo_doi_xung`, `_lease_cham_duong` của công cụ thật. Mốc 14:30:06Z/07Z/08Z cho registry 2/1/1, ci.yml 1/1/1. Mô hình thu hồi mọi bản cho 1/1 ở thời điểm đo. `python3 -B ops/lease_publish.py check ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml` trong `cay-kho/`: rc=0, ĐĂNG ĐƯỢC. Dữ liệu và các ref/blob nằm trong `do-review10/snapshot.json`; lệnh check có stdout/metadata riêng. Không gọi `ai-dang-giu` CLI vì đường ấy đối chiếu mạng; phép quét ở đây chỉ chứng nhận snapshot offline.

ĐỘ TIN: cao về snapshot và mô hình thời gian; trạng thái máy chủ trực tiếp, kể cả sau 14:30:07Z, KHÔNG ĐO ĐƯỢC.

### bien-do-khac-head-khong-phai-nhieu-runner  [P2]  Lease r4 còn gọi đối chiếu khác lane là đối chiếu nhiễu

TỆP/DÒNG: `ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml:162–164`; đối chiếu spec r4 `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:11–14`, `:103–107`, `:455–457`, `:540–542`, `:628–634`.

VẤN ĐỀ: Toàn văn spec r4 và Issue #463 đã sửa đúng các câu của lượt 9: mẫu được gọi đúng 5 master + 6 nhánh, hai run lịch sử khác event/lane, biên A1/A5 là thiết kế, không còn cho nới theo nhiễu được cho là đã đo. Nhưng lease r4 MỚI CẤP vẫn giao việc tính billing với “lượt master 34048685345 = 111,08 để đối chiếu nhiễu”. Câu này là một phần của `viec_trong_lease`, không phải chú thích lịch sử. Nó tiếp tục gán ý nghĩa nhiễu cho phép so mà chính spec r4 đã bác. Giữ P2 vì A1 ≤ 25,00 và A5 ≤ 135,00 không bị nới; đây là sai nghĩa và mâu thuẫn giữa hai phần hợp đồng. EVIDENCE bỏ sót câu này.

ĐÃ THỬ VÁ: Có, thử thay đúng một mỏ neo trong bản sao văn bản ngoài checkout: gọi run master là đối chiếu lịch sử, nói rõ cùng tree nhưng khác event/lane và chưa tách phần runner. Chỉ một mục `viec_trong_lease` đổi; ngưỡng 135,00, băm spec/write set, authority, mốc và chuỗi thay thế đều giữ nguyên trong thử nghiệm. Ca khóa: parse YAML rồi kiểm mục billing không còn “đối chiếu nhiễu”; quét và đọc ngữ cảnh toàn spec/Issue/lease hiện hành, xác nhận hai ngưỡng giữ nguyên. Rủi ro: chỉ xóa chữ ở spec lại sót lease; không sửa các lease r1/r2/r3 đã thành lịch sử để che dấu lời khai cũ. Executor tự quyết và ghi audit phù hợp cho thay đổi lease đã cấp. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review10/prose_checks.py` rc=0. Dữ liệu lưu trong kho cho `426bfc0`/`1b3caa1`: tree bằng nhau, 0 path đổi; một run `workflow_dispatch` trên nhánh, một `push` trên master. Hai tập đều 86 bộ ba nhưng có 4 thêm/4 mất ở release-verify WORKER/LAND. Chênh job Windows 0,916667 phút và ubuntu 2,266667 phút khớp số làm tròn, không xác định được thành phần do runner. Mô hình sửa có 1 neo duy nhất và 1 mục YAML đổi. Hiện vật: `do-review10/prose-checks.json`, `gate-prose-scan.txt`, `prose-experiment/`. Không chạy hay tạo bản vá workflow/gate.

ĐỘ TIN: cao về câu lease và sự khác event/lane; nhiễu runner riêng KHÔNG ĐO ĐƯỢC từ mẫu này.

### manifest-luot8-liet-ke-hien-vat-khong-duoc-giao  [P2]  Lượt8 đã đủ nhưng gói lượt 9 lại thiếu 19 tệp đã phục dựng

TỆP/DÒNG: `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair/ARTIFACTS.sha256:48–66`; `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-checks.json:2–7`; `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact_checks.py:10–17`; `EVIDENCE.md:12` của bundle giao reviewer.

VẤN ĐỀ: Gói lượt 8 hiện kiểm đủ 69/69, nhưng phần `artifact-repair/` do reviewer lượt 9 tạo lại mất cả 19 tệp `rig/do-review/` và `rig/source/` khi được chép vào gói lượt 9. Manifest con vẫn cam kết những tệp ấy; script và kết quả lịch sử xác nhận reviewer đã phục dựng và chạy rc=0. Chạy trên gói đã giao nay rc=1, chỉ 50/69. Con số “111 tệp” trong EVIDENCE đúng số tệp hiện có nhưng không chứng minh chép đủ: ít nhất 19 tệp đã tạo còn thiếu. Giữ nguyên slug vì cùng lỗi bàn giao theo manifest tái phát trong gói kế tiếp. Không nâng P1 mất bằng chứng H: toàn bộ 19 tệp có bản đúng hash ở gói lượt 8 đã sửa.

ĐÃ THỬ VÁ: Có, dựng lại gói con ngoài checkout trong `do-review10/artifact9-repair/`: giữ nguyên 50 tệp có sẵn và manifest, bổ sung 19 tệp thường có hash khớp từ gói lượt 8. Executor có thể bổ sung đúng byte đã cam kết vào gói lượt 9. Ca khóa: `sha256sum -c ARTIFACTS.sha256` phải rc=0 cho cả gói lượt 8 và manifest con gói lượt 9; so tập đường dẫn trước/sau sao chép, loại tmp/symlink theo thành phần đường dẫn tương đối, không bỏ cả thư mục `rig/`. Rủi ro: chỉ xóa dòng manifest sẽ làm mất chứng cứ lịch sử; chép theo tên mà không so hash có thể trộn các lượt khác nhau. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review10/artifact_checks.py` rc=0; chương trình gọi `sha256sum -c ARTIFACTS.sha256` thật ở từng gói. Lượt6: 62/62 rc=0; lượt 7: 66/66 rc=0; lượt 8: 69/69 rc=0; lượt 9/artifact-repair: 50/69 rc=1. Gói lượt 9 có 111 tệp thường và 0 symlink. Tìm được 19/19 nguồn đúng hash trong lượt 8; bản sao phục dựng kiểm 69/69 rc=0. Ánh xạ từng đường và hash nằm trong `do-review10/artifact-checks.json`; stdout/stderr của mỗi phép kiểm được lưu. Không sửa checkout và không khai đã chạy lại suite H.

ĐỘ TIN: cao.


## Giới hạn và bàn giao

Đã review hai trục. **Spec:** revision4 (g)(h)(i), bối cảnh hai run, bảng thứ tự, A1/A2/A5 và `chua_do_duoc` #3 nhất quán trong chính spec; lỗi đồng bộ còn ở câu billing của lease r4. A2 r3/r4 bằng byte và mô hình vẫn chặn mất bước. Quyết định H đã được ghi thống nhất, không bị biến thành cấp lease hay hoàn tất Đ1–Đ5. **Standards:** quét toàn snapshot lease, kiểm bốn mắt lease GATE, băm/neo Issue và receipt v2, manifest các gói, phạm vi diff thuần `ops/` và các cổng hồ sơ phù hợp.

**Đánh giá lời khai authority r4:** hồ sơ nói rõ `granted_on_instruction` là comment r3/5568696936, dẫn chỉ thị “không cần hỏi lại” và tiếp tục vòng lặp, đồng thời thú nhận comment riêng r4 chưa đăng được. Lời khai này minh bạch và nhất quán trong các bản được giao; không có cơ sở từ bundle để cáo buộc đã giả một comment r4. Tuy nhiên, nó chưa đủ để reviewer xác nhận trực tiếp nội dung/quyền comment, việc công cụ từng chặn hay sự kiện cấp lease trên GitHub. `check` tự in rằng chưa chạy hai lớp GitHub, nên rc=0 chỉ chứng nhận phần local. Không mặc định đòi một URL mới cho mỗi revision khi hồ sơ đã dẫn ủy quyền tiếp tục; vẫn không cấp authority từ lời khai ấy. Các băm, mốc tương đối, bia mộ r3 và neo commit đã đo được ở local được ghi riêng trong bảng.

**KHÔNG ĐO ĐƯỢC:** GitHub trực tiếp, tập ref máy chủ, master đúng giây cấp r4, nội dung/quyền comment r3 và quyết định H, trạng thái thực sau 14:30:07Z, branch protection, Windows/Actions trước-sau tách thật, hóa đơn và nhiễu runner riêng. Receipt lượt 9 qua schema/hash/neo blob; model/session/timing/stdout gốc chỉ là metadata tự khai chưa được đo lại. Không đổi các giới hạn ấy thành pass.

**Không chạy:** toàn bộ packet_loop_test, registry `--chay`, corpus H1213 ca, suite Windows hoặc triển khai tách job. Phần đổi sau lượt 9 là hồ sơ và hiện vật; hai khối mã H bằng byte bản trước. Không dùng stdout lịch sử làm kết quả suite vừa chạy. Mô hình A2 dựa YAML và TSV đã lưu, không phải run Actions mới. Các tệp thử sửa ở `do-review10/prose-experiment/` và `artifact9-repair/` chỉ là bằng chứng reviewer ngoài checkout.

Lệnh trích/đo được giao trong `do-review10/{static_checks,artifact_checks,contract_checks,prose_checks,run_command}.py`; `contract_checks.py` chuyển thể từ script lượt 9 và đã chạy lại trên r4. Quét văn bản dùng `rg -n -i` với nhóm từ nhiễu/phương sai/biên độ/master/event/lane và chưa/chọn/§12/Đ1–Đ5, rồi đọc ngữ cảnh để tách lời khai hiện hành với lịch sử/selector. Bộ lọc này không chứng minh mọi con số lịch sử của toàn PR; bảng đo chỉ xác nhận những phép đã chạy. Hai phần EVIDENCE bỏ sót được ghi thành finding: câu nhiễu trong lease và manifest con thiếu tệp ở lượt 9.

Hiện vật và stdout/stderr/metadata ở `do-review10/`. Không sửa nhánh executor; không đăng verdict lên GitHub, không ghi receipt/state và không cấp merge authorization, theo phạm vi PROMPT. Người vận chuyển cần giữ nguyên byte và exact reviewed_sha.

verdict: changes_requested
