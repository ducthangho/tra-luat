verdict: changes_requested
reviewed_sha: 9a99dd8aa137ef118a00671482c29ea2438cbdbb
base_sha: f4d74fed59616ecd5a133fc232275a832dcd95bb
luot: 1
so_lan_luot_nay_bi_chet_va_phong_lai: 0

**1 finding P1 · 4 finding P2 · 6 finding P3.** Bản đính chính đã sửa đúng số cổng tại **6/6 commit**. Tuy nhiên, hồ sơ còn nâng CI của PR thành CI exact head, đưa số hậu kiểm vào tiền kiểm và diễn giải rộng hơn verdict/nguồn Git. Chưa đủ `approve` cho PR #489.

Reviewer: Codex/OpenAI, công cụ shell trong phiên API, transport machine; phiên độc lập với executor Claude theo nhiệm vụ được giao. Không suy model đã phục vụ từ tên tài khoản hoặc model yêu cầu. Quan sát **0 lần** lượt review chết/phóng lại. Đã ghi `VERDICT.md` ngay khi có kết luận rồi hoàn thiện trong cùng lượt.

Đơn vị: `luot` đếm lượt review; trường chết/phóng lại đếm lần. SHA/hash, mã thoát, số PR/ADR, ID và dòng nguồn là định danh/giá trị kỹ thuật. Các số đếm nêu đơn vị tương ứng. Bằng chứng dương `N/N` chỉ được dùng khi tử và mẫu bằng nhau; “biên nhận phân loại” gồm biên nhận v2 đạt, legacy miễn trừ và nợ đóng băng, **không có nghĩa tất cả đạt v2**.

Tên ngắn: **L480** = `ops/land/pr480-land-evidence.yaml`; **L487** = `ops/land/pr487-land-evidence.yaml`; **RH** = `ops/reviews/pr487-hau-kiem-head-review-1-codex-verdict.receipt.yaml`; **V** = verdict `.md` cùng tên; **R1/R2** = `ops/reviews/pr487-review-{1,2}-codex-verdict.receipt.yaml`; **INDEX** = `ops/reviews/README.md`. Mọi dòng nguồn dưới đây ở reviewed SHA, trừ khi ghi rõ commit khác.

Phép đo: `python3 -B phep-do/do-cong.py` dựng phép chiếu đủ receipt + mã/luật từ từng commit, với HEAD riêng và kho object đọc từ gói; kiểm byte đầu vào từng SHA. CLI trên `cay-kho/` chạy trực tiếp. `do-cong-tai-lieu.py` dùng cây tạm đầy đủ từ `git archive` cho các cổng tài liệu. Các thư mục tạm nằm trong gói; không thay checkout, ref hoặc cấu hình của `cay-kho/`. Không dựng một kho nông giả rồi nhận là môi trường điều phối gốc.

## BẢNG ĐO

| khẳng định (tệp:key path) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| Gói: exact HEAD/base/tree/detached/sạch | Theo prompt | HEAD/base đúng; tree `34d7b2213d71d099f6a72158302536bc5dda3847` được ghi đầy đủ trong `phep-do/preflight.json`; porcelain **0 byte**, detached, shallow=false; `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Gói: refs/heads và snapshot | **314 ref nhánh** | **314/314 cặp tên+OID** khớp TSV; **0 ref replace**; `preflight.json` | ĐO ĐƯỢC+KHỚP | Có |
| Gói: diff | **7 tệp**, thêm **877 dòng**, bớt **3 dòng** | Git diff khớp **7/7 tệp** và hai số dòng; `preflight.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Gói: ARTIFACTS.sha256 | Toàn vẹn hiện vật | **3.173/3.173 tệp** khớp băm, **0 tệp lệch**; `manifest.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Gói: EVIDENCE: nguồn máy chủ/mốc chụp | `2026-09-09T13:17:22Z`; snapshot máy chủ | Chỉ đối chiếu được các bản snapshot trong gói. Không đo GitHub trực tiếp; URL origin không chứng minh nguồn object. | KHÔNG ĐO ĐƯỢC | Không kết luận về máy chủ |
| L480:post_merge_checks[8].đính chính; L487:p1_connector…; RH:phat_hien… — `c87b067` | **30 biên nhận v2 đạt**, **0 vi phạm** | **83/83 biên nhận** phân loại = **30 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`, mã thoát 0. **1,842 commit** kể cả chính commit. `bien-nhan.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[8].đính chính; L487:p1_connector…; RH:phat_hien… — `da481f9` | **33 biên nhận v2 đạt**, **0 vi phạm** | **86/86 biên nhận** phân loại = **33 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`, mã thoát 0. **1,845 commit** kể cả chính commit. `bien-nhan.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[8].đính chính; L487:p1_connector…; RH:phat_hien… — `5b96ddc` | **28 biên nhận v2 đạt**, **0 vi phạm** | **81/81 biên nhận** phân loại = **28 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`, mã thoát 0. **1,838 commit** kể cả chính commit. `bien-nhan.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[8].đính chính; L487:p1_connector…; RH:phat_hien… — `7e69b8e` | **33 biên nhận v2 đạt**, **0 vi phạm** | **86/86 biên nhận** phân loại = **33 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`, mã thoát 0. **1,850 commit** kể cả chính commit. `bien-nhan.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[8].đính chính; L487:p1_connector…; RH:phat_hien… — `3873173` | **38 biên nhận v2 đạt**, **0 vi phạm** | **91/91 biên nhận** phân loại = **38 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`, mã thoát 0. **1,858 commit** kể cả chính commit. `bien-nhan.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[8].đính chính; L487:p1_connector…; RH:phat_hien… — `f4d74fe` | **38 biên nhận v2 đạt**, **0 vi phạm** | **91/91 biên nhận** phân loại = **38 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`, mã thoát 0. **1,864 commit** kể cả chính commit. `bien-nhan.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| CLI trực tiếp tại reviewed head | Không có số riêng cho head mới trong đính chính | **92/92 biên nhận** phân loại = **39 biên nhận v2 đạt** + **11/11 biên nhận legacy** + **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`. | ĐO ĐƯỢC+KHỚP | Phép đo mới |
| A/B: vế mirror tại `3873173` | shallow=false; **1.858 commit**; **38 biên nhận đạt**, **0 vi phạm** | **1.858/1.858 commit** theo `rev-list --count`; **91/91 biên nhận** phân loại, `ok: true`. Lệnh đếm bao gồm chính HEAD, không phải số tổ tiên nghiêm ngặt. | ĐO ĐƯỢC+KHỚP | Có |
| A/B: vế kho nông tại `3873173` | shallow=true; **405 commit**; **34 biên nhận đạt**, **4 vi phạm** | Không có kho nông và log gốc. KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): thiếu hiện vật và cấm mạng. | KHÔNG ĐO ĐƯỢC | Không xác nhận hoặc bác số cũ |
| A/B: HEAD trước/sau unshallow | **417 commit** → **1.870 commit** | Exact HEAD của phép A/B này không được khai. `8911ea4` có **1.870 commit** trong Git, nhưng việc trùng số không định danh HEAD lịch sử. Vế **417 commit** và thao tác unshallow không tái đo được. | KHÔNG ĐO ĐƯỢC | Không coi số trùng là chứng minh |
| L480/L487/RH: cơ chế `bien_nhan_v2.py`:805,818 | Object có nhưng quan hệ tổ tiên bị cắt | Đúng mã: `cat-file -e <neo>^{commit}` rồi `merge-base --is-ancestor <neo> HEAD`; mã thoát 1 bị thêm vào lỗi. **2/2 vị trí mã** khớp. Trong kho không nông các neo được đo đều là tổ tiên. Không phải mọi repo nông hoặc mọi commit đều trả sai. | ĐO ĐƯỢC+KHỚP | Có |
| L480/L487/RH: A/B “khác đúng MỘT biến”, kết luận nhân quả | Kho nông tạo lỗi; hai rig chỉ khác độ sâu | Cơ chế phù hợp và kết quả kho đầy đủ khớp; không có manifest/config/log hai rig để chứng nhận chỉ khác độ sâu hoặc nguyên nhân duy nhất. Giữ là lời điều phối thuật lại, không nâng thành đo độc lập. | KHAI RỘNG HƠN PHÉP ĐO | Cần giới hạn nguồn |
| L480:post_merge_checks[8].mau_thuan… | Lời khai `pr478-land-evidence` ĐÚNG; không còn mâu thuẫn | Riêng kết quả cổng tại `c87b067` khớp **83/83 biên nhận**, **0 vi phạm**. Không có cơ sở giữ tiền đề master đỏ. Không xác thực toàn tệp, số API hoặc thời điểm lần chạy cũ. | ĐO ĐƯỢC+KHỚP | Có |
| L480:khong_do_duoc[5] so phần đính chính | Vẫn hỏi nguyên nhân master đỏ; giả thuyết thiếu ref còn sống | Lời cũ còn nguyên tại dòng 239–240, trái khối rút tiền đề đỏ và câu RH “mọi câu … đã sửa”. | ĐO ĐƯỢC+LỆCH | Không |
| L487:p1_connector…finding_khai — vế (a) | Cây merge exit 1, cha exit 0 | Cha thật `7e69b8e` và `3873173`: **2/2 cây** đạt. Merge thật `f4d74fe` cũng đạt. Chỉ xác nhận phần “cha exit 0”; không xác nhận toàn vế (a). | KHAI RỘNG HƠN PHÉP ĐO | Đúng phần cha; phần merge connector chưa đo |
| L487:p1_connector… — vế (b) | **5 receipt mới** fail ancestry; đính chính nói không đúng trong kho đầy đủ | **5/5 neo** đúng path/hash, là tổ tiên head `3873173` và merge thật `f4d74fe`; `five-anchors.json`, `ok: true` từng neo. Không cần đổi neo trên hai cây này. | ĐO ĐƯỢC+KHỚP | Có |
| L487:khong_do_duoc[2]; phạm vi connector | Không còn cần môi trường connector để phán finding | Hai object `a9b9edd014636dd49b208a5e2d37fbe5dfa0c01f` và `372bf9adb331218212619fc04763acbedfaa3f3f` vắng; `cat-file -e …^{commit}` mã thoát 128. Không tái chạy cổng trên chúng. Môi trường không cần để rút lời bác cũ, nhưng vẫn cần để phán toàn bộ finding. | KHAI RỘNG HƠN PHÉP ĐO | Không |
| L480/L487: merge_commit, merge_method, hai cha | `7e69b8e`: `da481f9` + `5b96ddc`; `f4d74fe`: `7e69b8e` + `3873173` | **2/2 cặp cha** khớp OID đầy đủ; topology merge đúng; `graph.json`. Đối số API merge vẫn chưa đo. | ĐO ĐƯỢC+KHỚP | Có |
| L480/L487: post_merge_checks[0,2] | Head vào master, nhánh không có commit ngoài master | Tại mốc merge cố định head là cha thứ hai; **2/2 nhánh** nêu tên có **0 commit** ngoài `f4d74fe`. Ref master đang đo là snapshot, không xác nhận ref hoặc giờ tại lần thao tác. | ĐO ĐƯỢC+KHỚP | Có |
| L480:merged_at; L487:merged_at | `11:39:00Z`; `11:58:30Z` ngày `2026-09-09` | Timestamp committer Git quy đổi đúng **2/2 mốc UTC**. Trường `merged_at` của GitHub API vẫn KHÔNG ĐO ĐƯỢC; không suy từ metadata commit sang API. | ĐO ĐƯỢC+KHỚP | Có |
| L480:authorization_*; L487:authorization_* | Actor `notebyme88`, APPROVED, khác tác giả, đúng SHA; URL review tương ứng | OID duyệt được khai khớp **2/2 head** làm cha thứ hai. Actor/association/trạng thái/commit_id của GitHub và mốc `11:30:29Z`, `11:30:50Z` không có nguồn API độc lập. | KHÔNG ĐO ĐƯỢC | Chỉ khớp OID được khai với Git |
| L480:authorization_ghi_chu — duyệt trước | `afddf7e`, review ID `5151752290`, `08:32:30Z`, DISMISSED sau push | Không có JSON review/push timeline. Sự tồn tại commit không xác nhận lúc push hoặc dismiss. | KHÔNG ĐO ĐƯỢC | Không kết luận |
| Hai tệp: land_operator/merged_by/CAS/ai_thuc_su_bam/session | `ducthangho`, Claude dùng PAT, gọi API với expectedHeadSha và chỉ thị chủ kho | Git không chứng minh ai thực sự gọi API, chủ PAT, lời chỉ thị, CAS hoặc danh tính phiên. Giữ nhãn attestation; không mở dữ liệu ngoài gói. | KHÔNG ĐO ĐƯỢC | Không kết luận |
| L480:cross_review.ket_qua_tung_luot | Lượt 1: **1 P1, 4 P2, 3 P3**; lượt 2: **0 P1, 0 P2, 3 P3** | **2/2 verdict** khớp SHA, kết luận và số finding từng mức; hash/bytes của receipt khớp. Đơn vị của các số là finding; `receipts.json`. | ĐO ĐƯỢC+KHỚP | Có |
| L487:cross_review.ket_qua_tung_luot | Lượt 1: **0 P1, 2 P2, 6 P3**; lượt 2: **0 P1, 0 P2, 6 P3** | **2/2 verdict** khớp SHA, kết luận và số finding từng mức; `receipts.json`. Đơn vị là finding; không cộng nhãn slug thành finding. | ĐO ĐƯỢC+KHỚP | Có |
| L480/L487:doi_chieu_luot_1_tai_luot_2 | L480: **7 thật, 1 hờ, 0 sinh mới, 0 chưa**; L487: **3 thật, 2 hờ, 3 sinh mới, 0 chưa** | Đọc phần đối chiếu trong verdict tương ứng: **8/8 slug** mỗi lượt. Đây là nhãn của slug cũ, không nói mọi việc vá sau đó đã hoàn tất. | ĐO ĐƯỢC+KHỚP | Có |
| L480:cross_review.khop_head_da_merge | Lượt 2 review đúng head `5b96ddc` | SHA trong verdict khớp cha thứ hai của merge: **1/1 OID**. Không có nợ đổi head của riêng lượt này. | ĐO ĐƯỢC+KHỚP | Có |
| L487:head_da_cross_review_khac_head_merge.phan_chenh/phan_them_la_gi | **2 commit** sau approve; tập tài liệu được dẫn nguyên byte | `edb288e`, `3873173` là đúng **2/2 commit**; **8/8 tệp** được liệt kê nguyên byte, `unchanged.json`, `ok: true`. Diff tổng **4 tệp**, thêm **354 dòng**, bớt **6 dòng**. Tập con nguyên byte không thay review head. | ĐO ĐƯỢC+KHỚP | Có |
| L480:cross_review.hien_vat.ghi_chu_vi_tri | Commit đầu tiên chứa tệp có `f4d74fe` là tổ tiên | Commit thêm là `6db5b6c`, cha `7e69b8e`; `f4d74fe` không là tổ tiên. Nhánh nhận merge đó ở `582a436`. Tại reviewed head, các hiện vật review đã có là đúng. | ĐO ĐƯỢC+LỆCH | Sai mốc đầu tiên |
| L480:cross_review.hien_vat.neo_kep và khong_do_duoc | Hai comment bản chiếu rút gọn; REST bị 403; MCP chuẩn hóa | Khóa/URL và lời cảnh báo có thật; nội dung đã đăng, byte readback, proxy và hành vi API lịch sử KHÔNG ĐO ĐƯỢC. Không thử mạng. | KHÔNG ĐO ĐƯỢC | Không xác thực GitHub |
| L480:mot_p3_bat_loi_cua_dieu_phoi | Khoảng `14dab5e..75fe4c4` có **5 commit**; lời rút ở `60d62aa` | Lịch sử và verdict giữ lời rút. Số commit Git không đo số commit đẩy sau duyệt. Timeline push/duyệt chưa đo. | ĐO ĐƯỢC+KHỚP | Đúng giới hạn phép đo |
| L480:pre_merge_checks[0] — CI exact head | Run `34338301656`, PR `5b96ddc`, success | Workflow không ghim checkout head; thiếu run/log chứng minh SHA đã test. Tên “exact head” quá rộng. | KHAI RỘNG HƠN PHÉP ĐO | Không chứng nhận tiền kiểm |
| L480:pre_merge_checks[1] — duyet khac danh tinh | success sau event pull_request_review | Chỉ là lời API được thuật lại; không có JSON check hoặc thời điểm chạy. | KHÔNG ĐO ĐƯỢC | Không chứng nhận tiền kiểm |
| L480:pre_merge_checks[2] — lease_publish | **121/121 ca**; chạy **121 ca**, bỏ qua **0 ca** | Bộ test dài không được phép chạy. `lease_publish.py check` kiểm một lease và không tạo số **121 ca**. Không có log tiền kiểm; không dùng lệnh check thay bộ test. | KHÔNG ĐO ĐƯỢC | Không chứng nhận tiền kiểm |
| L480:pre_merge_checks[3] — doctrine-scan | **7 tệp**, **0 chỗ chép** | Tái chạy trên cây tạm `5b96ddc`: **7/7 tệp** được quét, **0 chỗ chép**. Kết quả hiện tại khớp; thời điểm đã chạy trước merge chưa đo. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L480:pre_merge_checks[4] — adr-song | **46 ADR / 46 dòng** | Tái chạy `5b96ddc`: **46/46 mục ADR**, có ngoại lệ trạng thái ADR-0016. Thời điểm chạy cũ chưa đo. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L480:pre_merge_checks[5] — doc-claims | ok: true; **106 tệp** | Tái chạy `5b96ddc`: `ok: true`, **106 tệp** quét, **367 advisory**, **0 cờ cứng**. Không chứng nhận thời điểm tiền kiểm. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L480:pre_merge_checks[6] — bien_nhan_v2 | **28 biên nhận đạt**, tổng **81 biên nhận**, **0 vi phạm** đặt trong tiền kiểm | Số khớp **81/81 biên nhận**, nhưng lịch sử `8911ea4..e1fd0a3` chứng minh đây là thay số đo lại sau phát hiện kho nông vào mục tiền kiểm; dòng 120 vẫn nói mọi hàng chạy trước merge. | KHAI RỘNG HƠN PHÉP ĐO | Không chứng nhận tiền kiểm |
| L480:pre_merge_checks[7] — cross-review lượt cuối | approve, **0 finding P1, 0 finding P2, 3 finding P3** tại `5b96ddc` | Verdict đúng head và đủ số; sự kiện runtime/thời điểm review trước merge là attestation từ receipt, không có run.json. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L480:pre_merge_checks[8] — CI Windows | not_run vì PR không nhãn và không dispatch | Nhãn/event lịch sử chưa đối chứng. `not_run` được ghi rõ, không bị nhận thành passed; cấu hình có các đường Windows khác. | KHÔNG ĐO ĐƯỢC | Không chứng nhận tiền kiểm |
| L487:pre_merge_checks[0] — CI exact head | PR `3873173` success; không nêu run ID | Cùng thiếu chứng cứ checkout exact head; workflow không ghim ref. Kết quả API chưa đo. | KHAI RỘNG HƠN PHÉP ĐO | Không chứng nhận tiền kiểm |
| L487:pre_merge_checks[1] — duyet khac danh tinh | success sau APPROVED trên `3873173` | Không có JSON check/review. | KHÔNG ĐO ĐƯỢC | Không chứng nhận tiền kiểm |
| L487:pre_merge_checks[2] — phan chung duyet khac danh tinh | success | Không có run ID/SHA/log hay bằng chứng dương; không chứng nhận passed. | KHÔNG ĐO ĐƯỢC | Không chứng nhận tiền kiểm |
| L487:pre_merge_checks[3] — doctrine-scan | **7 tệp**, **0 chỗ chép** | Tái chạy `3873173`: **7/7 tệp**, **0 chỗ chép**; thời điểm cũ chưa đo. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L487:pre_merge_checks[4] — adr-song | **46 ADR / 46 dòng** | Tái chạy `3873173`: **46/46 mục ADR**; ngoại lệ ADR-0016 được khai. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L487:pre_merge_checks[5] — doc-claims | ok: true; **106 tệp** | Tái chạy `3873173`: `ok: true`, **106 tệp**, **367 advisory**, **0 cờ cứng**; không chứng nhận tiền kiểm. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L487:pre_merge_checks[6] — bien_nhan_v2 | **38 biên nhận đạt**, tổng **91 biên nhận**, **0 vi phạm** đặt trong tiền kiểm | **91/91 biên nhận** khớp sau tái đo. Số thay tại `e1fd0a3` sau merge, không chứng minh lần chạy hợp lệ trước merge. | KHAI RỘNG HƠN PHÉP ĐO | Không chứng nhận tiền kiểm |
| L487:pre_merge_checks[7] — cross-review exact head | not_run trước merge | Hai verdict tiền nhiệm neo `bcbca7b` và `5c05778`; không phải `3873173`. Ghi not_run cho tiền kiểm phù hợp hồ sơ, nhưng phần trạng thái hiện tại phải phản ánh hậu kiểm đã có. | ĐO ĐƯỢC+KHỚP | Có trong phạm vi tái đo |
| L487:pre_merge_checks[8] — CI Windows | not_run vì không nhãn/dispatch | Không xác thực nhãn/event API. Không nhập not_run thành passed. | KHÔNG ĐO ĐƯỢC | Không chứng nhận tiền kiểm |
| L480:post_merge_checks[3]; L487:post_merge_checks[3] — lease | **121/121 ca**, không bỏ qua | KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): bộ test dài và log lần chạy không kèm. Không gọi lease check để giả làm phép đo số ca. | KHÔNG ĐO ĐƯỢC | Không kết luận |
| L480/L487:post_merge_checks[4,5] — doctrine/ADR | **7 tệp**, **0 chỗ chép**; **46/46 ADR** | Tái chạy **2/2 cây merge thật**: **7/7 tệp** quét; **46/46 mục ADR**; ngoại lệ ADR-0016. `cong-tai-lieu.json`. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[6] — doc-claims | ok: true; **106 tệp**, **376 advisory** | Tại `7e69b8e`: `ok: true`, **106 tệp**, **367 advisory**, **0 cờ cứng**. Chênh **9 advisory**. Không có log/rig cũ để xác định nguyên nhân, không cáo buộc số lịch sử bịa. | ĐO ĐƯỢC+LỆCH | Khớp ok/số tệp; lệch advisory khi tái đo |
| L487:post_merge_checks[6] — doc-claims | ok: true; **106 tệp** | Tái chạy `f4d74fe`: `ok: true`, **106 tệp**, **367 advisory**, **0 cờ cứng**. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[7] — shellcheck | Chỉ ghi mã thoát 0 | Chạy `shellcheck -f json ops/dung_goi_review.sh`: **0 chẩn đoán**, kết quả `[]`; blob script giữ nguyên trên các mốc liên quan. Hồ sơ cũ chỉ mã thoát chưa phải bằng chứng dương. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[8]; L487:post_merge_checks[7] — receipt | Số sau đính chính đạt | Đã liệt kê riêng từng SHA phía trên; **86/86 biên nhận** tại `7e69b8e`, **91/91 biên nhận** tại `f4d74fe`, đều `TỔNG: ĐẠT`. | ĐO ĐƯỢC+KHỚP | Có |
| L480:post_merge_checks[9]; L487:post_merge_checks[8] — CI sau merge | Không đọc; run `34346689704` cho `7e69b8e`; push tự chạy | Không đọc GitHub, không xác nhận run/trạng thái. `ci.yml` khai push/master và ma trận Ubuntu/Windows; cấu hình trigger không chứng minh một run thực tế đã tồn tại. | KHÔNG ĐO ĐƯỢC | Giữ chưa đo |
| Hai tệp: bỏ chờ CI/Windows đầu tiên/chi phí | Bỏ thời gian chờ, không bỏ runner; PR thường Ubuntu, push thêm Windows; khoảng **26 phút/48 phút**, review **15–25 phút/lượt** | Phần ma trận khớp mã. Đường Windows còn workflow_dispatch/PR nhãn windows. “Đầu tiên”, thời lượng runner, tiết kiệm và chỉ thị vận hành là dữ liệu lịch sử/API chưa đo; chi phí mỗi mắt xích không suy từ một run. | KHÔNG ĐO ĐƯỢC | Khớp cấu hình có điều kiện; không xác thực lịch sử |
| L487:no_review_head_da_merge; RH:no_da_tra; INDEX:269 | Land: NO_CHUA_TRA, chưa có quyết định; receipt/INDEX: ĐÃ TRẢ vì **0 finding P1** | Có verdict hậu kiểm exact head, kết luận changes_requested. **3 nguồn** không đồng nhất. Phải phân biệt đã đọc head với đã approve/đóng findings. Không phủ nhận đã thực hiện lần đọc. | ĐO ĐƯỢC+LỆCH | Không |
| RH:no_da_tra.gioi_han; INDEX:269 — phạm vi finding P2 | Finding P2 lật kết luận đã đưa vào master; không còn finding đủ chặn merge | V:7 nói P2 thuộc `8911ea4` của PR #489, ngoài `3873173`; `8911ea4` không ở base master. **0 finding P1** không thay changes_requested hoặc điều kiện tới approve của chủ kho. | KHAI RỘNG HƠN PHÉP ĐO | Không |
| L480:bookkeeping.trang_thai_cua_477 | merged; CI chưa xác minh; “chưa có” CI exact merge commit | Không tự phong landed là đúng mức thận trọng. Nhưng lý do ghép CI `7e69b8e` của #480 sang #477: evidence cũ ĐÃ KHAI run `34176439015` tại `585c7d5` success hai nền. Không biết lời khai API cũ đúng hay sai. Không dùng CI #480 để phủ định #477. | KHAI RỘNG HƠN PHÉP ĐO | Giữ trạng thái thận trọng; sửa đối tượng bằng chứng |
| Hai tệp: bookkeeping thứ tự và chuỗi | L480 thứ tư, L487 thứ năm; chuỗi #468→#478→#486→#487→#480 | Base có **4/4 tệp YAML land**; head có **6/6 tệp**. Bỏ sót `pr477-dung-goi-review-land-evidence.yaml`. Tuyến #477→#480 khác tuyến #468→#478→#486; liên quan không tạo quan hệ cha/con tuyến tính. | ĐO ĐƯỢC+LỆCH | Không |
| Hai tệp: dẫn PROTOCOL §20 “0 cổng” | ADR về land evidence nằm ô **0 cổng** | Hàng ADR-0034 thực ghi “có nhắc: lease_publish.py×10; packet_loop.py×11”. Đơn vị là số lần nhắc. Nhắc tên không chứng minh cưỡng chế nội dung, nhưng không được gán nguồn này thành ô **0 cổng**. | ĐO ĐƯỢC+LỆCH | Sai nguồn dẫn |
| Hai tệp: bookkeeping A9 | **4 lease**, **4 spec_hash**, revision **1/2/3/4**, generation **1**, cấp trước hạn #456 | **4/4 lease** khai đúng tập revision, **4 hash khác nhau**, cùng generation 1. leased_at ngày `2026-09-07`: `03:37:33Z`, `07:50:35Z`, `09:44:51Z`, `10:17:12Z`, đều trước `14:30:07Z`; `a9.json`, `ok: true`. Chỉ đo nội dung lease; cấp thực tế/quyết định chủ kho chưa đo. | ĐO ĐƯỢC+KHỚP | Có |
| Hai tệp: bookkeeping._kiem_bia_mo | Dùng any(...) và lỗ hổng vẫn nguyên | Mã có `any` tại dòng 606 trong vòng lặp từng lease; có cả test t120/t121. Chỉ sự có mặt của any không chứng minh lỗ hổng. Không chạy bộ phản chứng ngoài danh sách được phép; chưa chứng nhận đóng hoặc mở lỗ hổng. | KHÔNG ĐO ĐƯỢC | Đọc được mã; chưa đo hành vi lỗ hổng |
| L480:bookkeeping nợ README full-gate | Câu “muốn đối chiếu byte gốc phải chạy lại” còn; sửa sẽ lệch manifest | Câu còn tại `ops/reviews/full-gate-pr468-20260907/README.md:57`; sửa byte thì băm thay đổi. Không sửa gói full-gate ngoài phạm vi. Việc khôi phục log thô lịch sử chưa đo. | ĐO ĐƯỢC+KHỚP | Có |
| Hai tệp: bookkeeping lease #482/#483 | Hồ sơ nguyên nhân hạn mức đã có, chưa đủ điều kiện cấp lại | Tệp biên bản tồn tại trong Git, tự hạn chế kết luận từ thông báo lỗi chép lại. Trạng thái FAILED, hạn mức thực tế/khả dụng và nguyên nhân runtime là API không có nguồn thô. “Vì hạn mức” chỉ là attestation, không nguyên nhân duy nhất. | KHÔNG ĐO ĐƯỢC | Khớp có tài liệu/giới hạn; chưa xác thực sự kiện |
| RH:verdict_sha256,verdict_bytes; V so bản gói | `683488f13c912ece73b249660a3ab7731055b4d401b43eb91f0002d3e0b54bb9`; **37.900 byte** | SHA-256 trùng; **37.900/37.900 byte**; bản `VERDICT-hau-kiem-head-487.md` trong gói nguyên byte với V. `receipts.json`. | ĐO ĐƯỢC+KHỚP | Có |
| RH:so_p1/p2/p3,verdict,reviewed_sha | **0 finding P1, 1 finding P2, 4 finding P3**, changes_requested, `3873173…` | Đếm regex `^### … [P1/P2/P3]`: **5/5 tiêu đề**; kết luận và OID đầy đủ khớp thân V. | ĐO ĐƯỢC+KHỚP | Có |
| RH:evidence_url | Blob tại `145574101781909e06eea0d3040c051576a7523a` | URL đúng dạng/path, commit là tổ tiên HEAD, blob khớp băm. Neo hiện tại hợp lệ về nội dung và ancestry; không lỗi integrity. | ĐO ĐƯỢC+KHỚP | Có |
| RH:evidence_url_ghi_chu | `1455741` là commit đầu tiên chứa verdict | `git log --diff-filter=A` ở HEAD và --all đều trả **1/1 commit thêm**: `e1fd0a333109a555af4823fd2b830521d86fafbd`. Đã có toàn bộ **37.900 byte** ở đó; `1455741` không sửa V. | ĐO ĐƯỢC+LỆCH | Sai mốc đầu tiên |
| INDEX:hàng hậu kiểm so RH và V | changes_requested; `3873173`; **37.900 byte**; **0/1/4 finding** theo P1/P2/P3 | **3/3 nguồn** khớp các trường kết luận/SHA/bytes/severity. Lời diễn giải phạm vi và trả nợ có lỗi riêng, không phủ nhận integrity. | ĐO ĐƯỢC+KHỚP | Có |
| INDEX:inventory | Thêm hàng hậu kiểm, cập nhật hàng lượt trước | Từ **91 hàng** lên **92 hàng**; giữ **91/91 hàng cũ** theo thứ tự; **90/90 hàng cũ không sửa** nguyên văn; không có hàng trùng, `index.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| RH:bon_P3_da_va[0] | Số ref manifest đã sửa | R1:manifest.ghi_chu nay **313 ref nhánh**, khớp scalar và verdict đúng lượt. **1/1 vị trí sót** đã sửa; không lấy snapshot mới **314 ref nhánh** để xác nhận máy chủ lượt cũ. | ĐO ĐƯỢC+KHỚP | Có |
| RH:bon_P3_da_va[1]; R2:doi_chieu_luot_1…; L487:cross_review… | Lỗi khai vá hết sai commit đã vá | INDEX đã sửa; R2:47–48 và L487:57–58 vẫn nói cả ba sửa trong commit đưa verdict. **1/3 vị trí** lời khai đã sửa, **2 vị trí** còn sót; `repair-history.json`. | ĐO ĐƯỢC+LỆCH | VÁ HỜ, chưa phải đã vá toàn bộ |
| RH:bon_P3_da_va[2] | Đã đổi “bảy lượt” về **7 phát hiện / 4 lượt** | **2/2 vị trí** được chỉ ra (R2 phần đầu và INDEX) đã sửa; `CLAUDE.md:722–726` đúng hai đơn vị này. Không xác minh runtime ngoài nguồn văn bản. | ĐO ĐƯỢC+KHỚP | Có |
| RH:bon_P3_da_va[3] | Nợ độ phủ chưa vá | Đúng: YAML có đủ lá; INDEX/V ngoài đầu vào. Giữ `da_va: false` là trung thực; nợ vẫn tồn tại. | ĐO ĐƯỢC+KHỚP | Có |
| RH:model_reviewer_identity — số học thời lượng | **1.420,582 giây**; INDEX làm tròn **1.421 giây** | Hiệu timestamp `12:30:43.572583` → `12:54:24.154756` ngày `2026-09-09`: **1.420,582173 giây**; **2/2 cách làm tròn** khớp. Chỉ là số học trên lời khai, không đo lại runtime. | ĐO ĐƯỢC+KHỚP | Có |
| L480/L487:thoi_luong_giay các lượt trước | **1.226,450; 928,758; 1.526,889; 961,228 giây** | Tính hiệu timestamp receipt: **4/4 phép làm tròn** khớp. Nguồn timestamp gốc/run.json không có, nên không xác thực thời gian thực. | ĐO ĐƯỢC+KHỚP | Có |
| RH:runtime/prompt/stdout/stderr/model/session/clean cuối lượt cũ | Model yêu cầu; **699 byte stdout**, **614.405 byte stderr**, mã thoát 0, **0 lần chết**, cây sạch | Không có run.json, stdout/stderr, prompt hoặc log final của lượt cũ để băm lại/xác thực. Đơn vị trường giờ là giây, kích thước là byte; ID/hash chỉ đối chiếu được lời khai. | KHÔNG ĐO ĐƯỢC | Attestation đúng nhãn, chưa đo độc lập |
| RH:nang_luc_do_cua_goi/manifest | Gói cũ **314 ref nhánh**, **156 lá**, **21 dòng chú thích**, **4 tệp** diff | Diff lịch sử **4/4 tệp** kiểm được; số gói cũ khớp lời V, nhưng không có gói/manifest cũ để tái đo ref/lá/comment. Gói hiện tại có đầu vào khác. | KHÔNG ĐO ĐƯỢC | Không thay số cũ bằng số gói mới |
| BANG-CAU-TRUC-DAY-DU.tsv | **512 lá**, **0 lá cắt** | **512/512 hàng** khớp type/path/giá trị safe_load đầy đủ ở **5/5 YAML**; không cắt chuỗi. Đây là giá trị sau parse, không phải byte YAML nguyên văn; `tables.json`, `ok: true`. | ĐO ĐƯỢC+KHỚP | Có |
| BANG-CHU-THICH.tsv | **67 dòng chú thích** | **67/67 dòng ứng viên** khớp vị trí/text sau bỏ thụt đầu dòng. Nhưng **66 dòng** là comment YAML; **1 dòng** L480:97 ở trong folded scalar `ghi_chu_vi_tri`, không phải comment. Đã được bảng lá giữ nữa. | ĐO ĐƯỢC+LỆCH | Khớp dữ liệu; sai phân loại một dòng |
| Hai bảng: độ phủ Markdown/prose/inline | Tự khai chưa phủ hết | **10/10 vị trí nguồn** cụ thể trong bảng bỏ sót dưới đây nằm ngoài đầu vào. Không gọi prose đã giữ nguyên trong lá là mất chữ; thiếu ở cấp tách mệnh đề/nguồn đối chứng. | ĐO ĐƯỢC+KHỚP | Có |
| ci.yml:timeout-minutes | Không được nâng | **1/1 blob workflow** nguyên byte trong diff; giá trị **60 phút**. Không sửa workflow, không gọi CI. | ĐO ĐƯỢC+KHỚP | Có |

## KHẲNG ĐỊNH CẢ HAI BẢNG BỎ SÓT

“Bỏ sót” ở đây gồm nguồn/vị trí không được đưa vào bảng, dù một ý có thể được YAML thuật lại. Tôi không nhận một lá văn xuôi đầy đủ là bị cắt mất. `phep-do/bo-sot.json` giữ nguyên dòng nguồn tại **10/10 vị trí**, `ok: true`.

| vị trí | khẳng định | vì sao cả hai trượt | hệ quả |
|---|---|---|---|
| INDEX:269 | **0 finding P1** trả nợ review head | Markdown ngoài đầu vào | Bỏ vị trí người đọc dễ dùng để quyết định merge; không thay `approve` |
| INDEX:269 | A/B lộ nguyên nhân kho nông, số lịch sử trước/sau | Không trích dòng INDEX | Lời thuật được nhân rộng mà không giữ log A/B đối chứng |
| INDEX:269 | **3/4 finding P3** đã vá | INDEX ngoài bảng | Bỏ một nguồn nhận công trong khi hai vị trí YAML vẫn chưa sửa |
| INDEX:270 | Lịch sử mới: `edb288e` sửa receipt, `3873173` sửa INDEX, manifest sót tới hậu kiểm | Không giữ chính hàng đã sửa | Không thấy công sửa thật và mâu thuẫn với R2/L487 còn nguyên |
| V:7 | Finding P2 thuộc PR #489 tại `8911ea4`, **ngoài head được review** | Verdict ngoài đầu vào | RH gán kết luận P2 thành lỗi đã vào master mà không gặp giới hạn nguồn |
| V:9 | Đã đọc exact head; hậu kiểm không hồi tố thành tiền kiểm | Verdict ngoài đầu vào | Không phân biệt hoàn thành lần đọc với lịch sử trước merge |
| V:69 | **5/5 neo** hợp lệ trên head và merge thật | Verdict ngoài đầu vào | Dễ rút luôn bằng chứng đúng khi sửa lời bác sai |
| V:87 | Có **9 mục tiền kiểm/tệp** không xác nhận chúng đã chạy trước merge | Verdict ngoài bảng | Chính giới hạn này bị bỏ khi đưa kết quả mới vào `pre_merge_checks` |
| V:92 | Merge tổng hợp và môi trường connector chưa đo; không chọn một phía rồi suy mọi câu đúng | Verdict ngoài đầu vào | Bản đính chính vẫn nói không cần môi trường để phán finding |
| V:187 | Không để trạng thái “chưa có hậu kiểm” sống tiếp; có verdict không nghĩa mọi finding đã sửa | Verdict ngoài đầu vào | L487 giữ trạng thái cũ, RH lại đóng rộng hơn; hai chiều đều lệch |

### ci-pr-khong-chung-minh-exact-head  [P1]  Hai land evidence lại nhận CI của PR thành CI exact head

TỆP/DÒNG: L480:122–127; L487:152–155; đối chứng `.github/workflows/ci.yml`:81–86,115.

VẤN ĐỀ: Tên mục khẳng định CI trên exact head đã duyệt, nhưng nguồn chỉ thuật `pull_request` success. Workflow có **1 bước checkout**, không khai `with.ref`; chính comment trong workflow phân biệt `GITHUB_SHA` merge tổng hợp với head PR. Không có log/JSON chứng minh cây test thực là head. Land evidence cũ của #477/#478 đã giới hạn đúng cùng trường hợp này. Đưa lại tên “exact head” có thể cho downstream đi qua điều kiện trước merge bằng bằng chứng của cây khác. Tôi không tuyên đã quan sát runner checkout cây tổng hợp; finding là phạm vi chứng nhận không có bằng chứng hỗ trợ.

ĐÃ THỬ VÁ: Đổi **2/2 mục** thành “CI được báo cho PR có head …”, giữ success ở lớp attestation, ghi checkout SHA chưa đo và các đường Windows có điều kiện. Không sửa workflow hay timeout. Vá chỉ nhãn Windows mà giữ “exact head” không đóng lỗi.

GÓI VÁ: `cay/ops/land/pr480-land-evidence.yaml`, `cay/ops/land/pr487-land-evidence.yaml`, đầy đủ nội dung. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đọc YAML workflow, so blob với base, `workflow.json`, `ok: true` cho cấu hình đã nêu. Gói có **2/2 mục CI** cùng phạm vi với cảnh báo; kiểm chung **15/15 đối chiếu**. CI thực KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): cấm mạng/CI. Phản chứng cần khóa là thay lại tên thành “exact head” mà không có tested SHA/log; bản đó không đủ chứng cứ. Rủi ro vá: đừng xóa kết quả PR có ích hoặc tuyên CI thất bại.

ĐỘ TIN: cao về khai vượt; không kết luận trạng thái run GitHub.

### tien-kiem-bi-thay-bang-so-hau-kiem  [P2]  Số đo sau unshallow không phải cổng đã đạt trước merge

TỆP/DÒNG: L480:115–120,140–142; L487:166–168; lịch sử `8911ea4..e1fd0a3`.

VẤN ĐỀ: Bản sửa đưa kết quả sạch đo sau phát hiện kho nông vào `pre_merge_checks`; L480 vẫn nói **mọi hàng** chạy trước merge. Đính chính tự khai thời điểm đo lại là sau hậu kiểm, và commit sửa chứa số ấy có timestamp sau các merge. Tái chạy commit cũ chứng minh trạng thái cổng của commit đó trong rig mới; không chứng minh quyết định trước merge đã có phép đo hợp lệ. Đây là lỗi provenance/thời điểm, dù số **81/81 biên nhận** và **91/91 biên nhận** đều đúng.

ĐÃ THỬ VÁ: Mục tiền kiểm ghi kết quả hợp lệ lịch sử KHÔNG ĐO ĐƯỢC; giữ số đúng trong khối `do_lai_sau_merge` có tested SHA và nguồn hậu kiểm. Giữ `not_run` cho review/Windows chỉ ở phạm vi lịch sử đã khai; không biến “không đo được” thành “chưa từng chạy”.

GÓI VÁ: Hai tệp land đầy đủ và `cay/ops/land/pr489-review-1-do-cuc-bo.json`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Git diff xác nhận **2/2 hàng** thay số tại commit đính chính; số gate tái đo khớp. Gợi ý giữ **9/9 mục** ở mỗi tệp và phân biệt lớp hậu kiểm. Phản chứng là ghép lại kết quả sạch vào bằng chứng trước merge; gói không làm vậy. Rủi ro: không viết lại lịch sử “failed” thành “not_run”, hoặc gán timestamp mới bịa cho lần chạy cũ.

ĐỘ TIN: cao.

### no-hau-kiem-khong-dong-nghia-approve  [P2]  Trạng thái nợ và phạm vi verdict bị kể khác nhau giữa ba nguồn

TỆP/DÒNG: L487:76–96; RH:35–46; INDEX:269; V:7,9,187.

VẤN ĐỀ: Land evidence vẫn ghi `NO_CHUA_TRA`, chưa có quyết định; receipt nói đã chuyển sang ĐÃ TRẢ vì **0 finding P1** và không còn finding đủ chặn merge. Thực tế đã có verdict exact head, nhưng verdict là `changes_requested`. V còn nói rõ finding P2 thuộc PR #489 ở `8911ea4`, **ngoài head `3873173`**, trong khi RH nói nó lật kết luận đã vào master. Một lần đọc head đã được thực hiện; không được tiếp tục gọi chưa có. Nhưng việc đó cũng không sinh `approve` hoặc xóa findings. Chủ kho của lượt này yêu cầu cross-review tới approve; không thể thay bằng đếm severity.

ĐÃ THỬ VÁ: Đồng bộ trạng thái `DA_HAU_KIEM_CHO_DONG_FINDINGS` giữa land/receipt, INDEX giải thích cùng nghĩa; ghi riêng phạm vi head và nhiệm vụ đối chứng PR #489. Khép phần thiếu lần đọc, giữ phần findings/điều kiện duyệt và lịch sử đã merge trước review. Không yêu cầu lùi merge hoặc vòng review vô hạn chỉ để “review chính receipt”.

GÓI VÁ: L487, RH và INDEX đầy đủ dưới `cay/`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Băm và đếm **5/5 tiêu đề finding** của V; kiểm đúng lời giới hạn V:7; kiểm Git cho `8911ea4` nằm ngoài base. Gói giữ nguyên **24/24 trường identity** của các receipt đã sửa và **92/92 hàng INDEX**; trạng thái giữa nguồn đã đồng nhất. Phản chứng là giữ `NO_CHUA_TRA` hoặc dùng `0 P1` thay verdict. Rủi ro: đừng sửa verdict lịch sử thành approve hay nâng finding P2 ngoài head thành lỗi của head.

ĐỘ TIN: cao.

### ket-luan-bac-connector-vuot-phep-do-hau-kiem  [P2]  Rút lời bác đúng hướng nhưng vẫn vượt phạm vi phép đo connector

TỆP/DÒNG: L487:103–127,213–218; L480:176–197; RH:48–74; INDEX:269.

VẤN ĐỀ: Đây là tiếp diễn slug P2 của hậu kiểm, đã sửa thật về các số cổng. **6/6 commit** đầy đủ đều sạch; rút căn cứ “cha cũng đỏ” là đúng. Tuy nhiên, bản mới tuyên hai rig “khác đúng một biến” mà không kèm rig/log, rồi nói môi trường connector không còn cần để phán finding. Vế (a) ban đầu gồm cả cây merge exit 1 lẫn cha exit 0; mới kiểm được phần cha và merge **thật**. Các object merge tổng hợp được dẫn vắng trong gói. Vế (b) có bằng chứng dương **5/5 neo** hợp lệ ở head/merge thật, nên không cần đổi neo ở đó; không được kéo kết quả sang object vắng. Gói không chứng minh kho nông là nguyên nhân duy nhất của toàn bộ khác biệt. Việc điều phối đã chạy A/B vẫn có thể là thật; tôi phân loại phần lịch sử đó là chưa đối chứng, không gọi nó sai chỉ vì thiếu log.

ĐÃ THỬ VÁ: Giữ toàn bộ số tái đo đúng và lời rút tiền đề sai. Gắn nhãn attestation cho vế kho nông/cặp HEAD chưa định danh, nêu cơ chế mã có điều kiện, phân biệt cha/head/merge thật với merge tổng hợp chưa đo. Giữ neo đúng. Giới hạn câu `pr478-land-evidence` đúng vào riêng kết quả cổng tại `c87b067`; bỏ “cả bốn vế sai” vì chênh số vi phạm giữa các cây sạch vẫn là **0 vi phạm**.

GÓI VÁ: Hai land evidence, RH, INDEX và JSON số đo đầy đủ dưới `cay/`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: **6/6 cây** receipt có `ok: true`; **5/5 neo** khớp byte/path/ancestry trên head và merge thật. Mã tại **2/2 vị trí** được khai khớp. `cat-file -e` xác nhận **2 object** được dẫn không đọc được trong gói; đây không phải bằng chứng object bịa. Không tái tạo vế kho nông. Phản chứng phải giữ: object thiếu ⇒ KHÔNG ĐO ĐƯỢC, không dùng success của merge khác thay nó. Rủi ro vá: không đảo chiều thành “connector đúng hoàn toàn” hoặc xóa công sửa số cổng.

ĐỘ TIN: cao về ranh giới bằng chứng; chưa kết luận nguyên nhân toàn bộ môi trường lịch sử.

### trang-thai-477-ghep-ci-cua-480  [P2]  Bản sửa trạng thái PR #477 dùng nhầm merge commit làm căn cứ

TỆP/DÒNG: L480:247–258; đối chứng `ops/land/pr477-dung-goi-review-land-evidence.yaml`:111–124.

VẤN ĐỀ: Hạ trạng thái khỏi `landed` khi chưa tự xác thực CI là thận trọng hợp lệ. Nhưng giải thích lại lấy việc không đọc run `34346689704` của **#480, merge `7e69b8e`** để nói #477 chưa có CI trên exact merge commit. Hồ sơ #477 đã có lời khai riêng: run `34176439015` tại **`585c7d5`**, Ubuntu/Windows success. Lời API ấy vẫn chưa đo độc lập trong lượt này, nhưng nó tồn tại; không phải “chưa có ai đo”. Các cổng cục bộ được dẫn trong L480 cũng là của `7e69b8e`, không thay cổng `585c7d5`.

ĐÃ THỬ VÁ: Giữ chưa chứng nhận landed ở lượt offline; phân biệt #477/#480 bằng PR và merge SHA, dẫn đúng evidence #477 và nhãn attestation. Không tuyên CI #477 đạt bằng việc đọc một lời khai, cũng không dùng CI #480 để phủ định nó.

GÓI VÁ: `cay/ops/land/pr480-land-evidence.yaml`, đầy đủ. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: **2/2 merge OID** đối chiếu đúng PR trong Git; đọc khối CI cũ tồn tại ở `5b96ddc` và reviewed head. CI/API KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho). Phản chứng là dùng run có SHA khác PR đang đánh giá; cần đối chiếu run→SHA→PR. Rủi ro: không tự đóng trạng thái hoặc đổi định nghĩa landed.

ĐỘ TIN: cao về ghép nhầm bằng chứng; chưa xác thực CI.

### dinh-chinh-van-giu-mau-thuan-da-rut  [P3]  Mục chưa đo vẫn treo tiền đề master đỏ đã bị rút

TỆP/DÒNG: L480:239–240; RH:69–72.

VẤN ĐỀ: Câu hỏi “nguyên nhân master đỏ” và giả thuyết thiếu ref còn nguyên trong `khong_do_duoc`, trái khối đính chính; RH lại tuyên mọi câu sai đã sửa. Đây là sót đồng bộ trong nội dung mới, không phải lỗi cổng.

ĐÃ THỬ VÁ: Đổi mục chưa đo sang kho nông/log A/B gốc, nói tiền đề đỏ đã rút. Không xóa giới hạn thật của môi trường cũ.

GÓI VÁ: L480 và RH đầy đủ trong `cay/`, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: So hai khối trong cùng tệp; phép tái đo **6/6 commit** sạch. Cổng schema vẫn đạt nhưng không kiểm prose này. Phản chứng: giữ một mục đang mở với tiền đề đã rút. Rủi ro: đừng đổi “không còn tiền đề đỏ” thành chứng nhận mọi nguyên nhân lịch sử.

ĐỘ TIN: cao.

### khai-va-het-ba-loi-sai-commit  [P3]  Lỗi đã nhận vá vẫn còn ở biên nhận và land evidence

TỆP/DÒNG: R2:46–54; L487:55–58; RH:85; INDEX:270.

VẤN ĐỀ: Cùng slug của hậu kiểm. INDEX đã sửa thật, nhưng R2 và L487 vẫn khai sửa cả ba trong commit đưa verdict. Git xác nhận `edb288e` chưa sửa INDEX, `3873173` mới sửa INDEX, manifest còn sót tới `1455741`. Vì vậy nhãn RH `da_va: true` chưa đúng cho toàn finding; chỉ **1/3 vị trí** đã sửa. Hai P3 về ref và đơn vị được sửa thật, không nhập chúng vào lỗi này.

ĐÃ THỬ VÁ: Đồng bộ lịch sử ở R2/L487, ghi rõ phần gói gợi ý chưa được executor áp; RH không nhận công trước. Giữ nguyên verdict cũ và nhãn phân bố slug.

GÓI VÁ: R2, L487, RH, INDEX đầy đủ dưới `cay/`, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đối chiếu **3/3 mốc commit** nêu trên và `repair-history.json`; gói giữ **24/24 trường identity** và cổng **92/92 biên nhận** phân loại. Phản chứng là còn một câu hoàn tất sai mốc; kiểm cả scalar lẫn prose. Rủi ro: không dùng commit message làm bằng chứng file đã đổi.

ĐỘ TIN: cao.

### neo-verdict-khong-phai-commit-them-dau  [P3]  Neo đúng blob nhưng khai sai commit đầu tiên chứa verdict

TỆP/DÒNG: RH:29–30; lịch sử V.

VẤN ĐỀ: URL `1455741` trỏ đúng blob và là tổ tiên nên integrity đạt. Nhưng V đã được thêm đầy đủ tại `e1fd0a3`; `1455741` chỉ sửa hồ sơ khác. Commit message nói “verdict + vá” không thay `git log --diff-filter=A`.

ĐÃ THỬ VÁ: Ghim URL vào OID đầy đủ của `e1fd0a3` và sửa ghi chú; giữ hash/bytes/reviewed SHA. Hoặc giữ URL cũ và bỏ “đầu tiên” cũng đóng lỗi, nếu không cần neo lần thêm đầu.

GÓI VÁ: RH đầy đủ trong `cay/`, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: HEAD và --all đều cho **1/1 commit thêm**; blob tại cả hai OID khớp **37.900/37.900 byte**. Gói dùng neo đầu tiên và cổng đạt. Rủi ro: không đổi reviewed SHA thành commit vận chuyển verdict.

ĐỘ TIN: cao.

### lich-su-land-evidence-bo-sot-nhanh-477  [P3]  Mốc thêm tệp, thứ tự và tuyến PR không khớp đồ thị Git

TỆP/DÒNG: L480:10–13,93–101,244–246,259–264; L487:225–226.

VẤN ĐỀ: “Commit đầu tiên chứa tệp có `f4d74fe` là tổ tiên” sai: đầu tiên là `6db5b6c` với cha `7e69b8e`; `f4d74fe` được nhận sau ở `582a436`. L480 đếm thứ tư, L487 thứ năm do bỏ qua evidence #477 đã có: base có **4 tệp**, head **6 tệp**. Tuyến #477→#480 bị ghép thành phần cuối tuyến #468→#478→#486→#487. Sự liên quan review không tạo chuỗi cha/con ấy. Câu hiện vật đã có tại reviewed head vẫn đúng.

ĐÃ THỬ VÁ: Ghi mốc thêm/nhận merge riêng, đếm inventory Git thay thứ tự landed chưa đo, tách tuyến #477 khỏi tuyến #468. Không dùng timestamp commit để suy lịch sử push.

GÓI VÁ: Hai land evidence đầy đủ trong `cay/`, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `log --diff-filter=A`, cha của commit thêm và ancestry; inventory **4/4 tệp** ở base, **6/6 tệp** ở head; `graph.json`, `land-inventory.json`. Phản chứng: đếm bỏ tệp #477 hoặc quy merge sau làm tổ tiên commit trước. Rủi ro: đừng gọi số tệp là số lần land thành công.

ĐỘ TIN: cao.

### dan-protocol-sai-o-cong  [P3]  Hai lời dẫn “0 cổng” không đúng hàng ADR-0034

TỆP/DÒNG: L480:7–8; L487:5–6; `docs/PROTOCOL_DA_PHIEN.md`:1101–1112,1136.

VẤN ĐỀ: §20 không xếp ADR-0034 vào ô “0 cổng”; nó ghi số lần nhắc trong lease_publish/packet_loop. Cột có nhắc không chứng minh thực thi nội dung, nhưng không thể dẫn thành một phép đo vắng cổng. Prompt cũng dẫn cùng tiền đề; tôi dùng văn bản trong cây để phân xử. Các cổng ngắn đã chạy không xác thực prose/API land evidence; việc này không cứu lời dẫn sai.

ĐÃ THỬ VÁ: Dẫn đúng “có nhắc” và giới hạn của proxy; không nâng thành “đã có cổng kiểm nội dung”.

GÓI VÁ: Hai land evidence đầy đủ trong `cay/`, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đọc đúng hàng ADR và chú giải, đối chiếu **2/2 vị trí dẫn**. Phản chứng: gán hàng có nhắc thành vắng cổng. Chưa chạy bộ chứng minh bao phủ toàn bộ bộ kiểm; không khẳng định cơ chế cross-review là duy nhất trên mọi đường.

ĐỘ TIN: cao về sai nguồn dẫn.

### bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon  [P3]  Bảng đủ lá vẫn bỏ nguồn Markdown và đếm một dòng prose thành comment

TỆP/DÒNG: Hai bảng TSV; L480:97; **10 vị trí** ở bảng bỏ sót trên.

VẤN ĐỀ: Giữ đủ **512/512 lá** và không cắt là công sửa thật. Tuy nhiên, INDEX/V là **2 tệp thay đổi bắt buộc review** vẫn ngoài đầu vào. Những giới hạn sắc nhất của verdict không được mang vào bảng để đối chiếu với lời receipt. Thêm nữa, bảng chú thích có **67 dòng ứng viên**, gồm **66 comment YAML** và **1 dòng prose** thuộc folded scalar; regex đầu dòng không đủ phân biệt comment. Tự khai độ phủ còn thiếu là đúng, nhưng không đóng finding cũ.

ĐÃ THỬ VÁ: Bổ sung inventory **10/10 vị trí nguồn** và phép đối chiếu theo dòng trong `phep-do/bo-sot.json`. Hướng sửa lớp: đưa toàn bộ Markdown của diff vào inventory, dùng span token YAML để phân biệt comment với scalar, rồi tách mệnh đề có nguồn; không đổi tên “lá” thành “khẳng định”. Không viết parser hứa hiểu hết ngữ nghĩa.

GÓI VÁ: P3 không đòi tệp sản phẩm. Có inventory/`do-ho-so.py` trong gói; không thay TSV đầu vào gốc. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: **512/512 hàng lá** khớp; **67/67 dòng ứng viên** khớp sau bỏ thụt lề; yaml.scan xác định L480:97 nằm trong scalar dòng 93–101. Không tìm thấy ví dụ inline comment thật bị bỏ trong chính tập YAML này nên không bịa một ca; thiếu hỗ trợ inline vẫn là giới hạn tự khai. Rủi ro: sửa regex đầu dòng mà làm mất dấu `#` trong URL/scalar hoặc nhận dữ liệu lặp thành thêm mệnh đề.

ĐỘ TIN: cao về độ phủ và phân loại; không tự nhận đã tách mọi mệnh đề văn xuôi.

## GÓI VÁ VÀ GIỚI HẠN CUỐI LƯỢT

Có **6 tệp đầy đủ** dưới `cay/`: **2 tệp land evidence**, **2 receipt**, **1 INDEX**, **1 JSON số đo**. Xem `GOI-VA.md`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Gói là gợi ý sửa nội dung; kết quả kiểm gói không phải `approve` cho commit executor chưa tạo.

`python3 -B phep-do/kiem-goi-va.py`: **15/15 đối chiếu** đạt, `ok: true`; giữ **24/24 trường identity** trên các receipt sửa và **92/92 hàng INDEX** cùng thứ tự. Cổng receipt trên phép chiếu áp gợi ý: **92/92 biên nhận** phân loại, **39 biên nhận v2 đạt**, **11/11 biên nhận legacy**, **42 biên nhận nợ**, **0 vi phạm**, **0 trường hợp chưa đo**, `TỔNG: ĐẠT`. Cổng không xác thực prose; các kết luận nội dung dựa đối chiếu nguồn đã nêu.

**KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho):** mọi GitHub API/CI/approval/merged_by/nội dung comment và lịch sử push; kho nông, log A/B, runtime/run.json/argv/stdout/stderr/manifest gói cũ không có; object merge tổng hợp và môi trường connector; bộ test dài, CI và lệnh ngoài danh sách cho phép. Lý do là cấm mạng/chạy dài hoặc thiếu hiện vật. Không chứng nhận passed từ not_run, skipped, mã thoát trần hoặc lời API được thuật lại.

`cay-kho/` giữ exact reviewed SHA, detached, không nông; **314/314 ref nhánh** nguyên trạng và `status --porcelain` **0 byte**. Không commit, sửa ref, cấp lease, đăng ra ngoài, merge hay tăng timeout. Kết quả kiểm cuối lưu tại `phep-do/final-integrity.json`.
