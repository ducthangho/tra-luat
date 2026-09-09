verdict: changes_requested
reviewed_sha: bcbca7bbcea968a662b1ac69bfc9f2a329ed8ae7
base_sha: da481f94eee0adf1fe5fc4260a535a9b48fc2627
luot: 1
so_lan_luot_nay_bi_chet_va_phong_lai: 0

Kết luận: **0 finding P1 · 2 finding P2 · 6 finding P3**. Các finding P1 của hậu kiểm PR #486 đã được xử lý trong phạm vi tương ứng; chưa thấy bản vá sinh P1 mới. Tôi yêu cầu sửa các lời khai P2 mới của chính PR #487. Đây là review hồ sơ offline, không phải approval/merge authorization trên GitHub.

**Lời khai “đỏ sẵn” không tái hiện trong mirror.** Base có **33 biên nhận ĐẠT / tổng 86 biên nhận**, head có **36 biên nhận ĐẠT / tổng 89 biên nhận**; cả hai có **0 vi phạm**, **0 trường hợp KHÔNG ĐO ĐƯỢC**. Delta đúng là **0 vi phạm**, nhưng trạng thái được khai sai. **3/3 commit neo** bị nêu tên thực tế nằm trong tập tổ tiên của cả base và head. Kiểm riêng commit land `c87b0679a837055ee4cc33ac48c9adb8d7ad8784` cũng khớp hồ sơ: **30 biên nhận ĐẠT / tổng 83 biên nhận**, **0 vi phạm**. Không có căn cứ từ gói này để kết luận master đang đỏ hoặc land evidence đã che giấu cổng đỏ.

Reviewer: Codex/OpenAI, thực thi lệnh cục bộ qua công cụ API, transport machine; độc lập với phiên executor Claude. Không suy model đã phục vụ từ tài khoản GitHub hoặc từ model được yêu cầu trong receipt. Tree được review: `e0cf09001e8418e5c47aa85fc5a0a13297279ecf`. Quan sát **0 lần** chết/phóng lại trong lượt này. `cay-kho/` giữ detached tại SHA được giao và `status --porcelain` rỗng.

Đơn vị: `luot` là lượt review; bộ đếm chết/phóng lại là lần. SHA, hash, session ID, số hiệu PR/ADR, phiên bản schema, revision/generation, mã thoát và số dòng là định danh/giá trị schema, không phải phép đếm trần. Các số runtime là giây, kích thước là byte, độ phủ Git là ref nhánh hoặc tag, severity đếm finding, đối chiếu sửa đếm slug. “Khớp nội dung nguồn” không xác minh sự kiện mà nguồn thuật lại. `ok: true` chỉ áp dụng phạm vi phép kiểm được ghi kèm.

Tên rút gọn dùng trong các bảng:

- **L**: `ops/DO_VI_SAO_LEASE_482_483_CHET_20260909.md`.
- **R1 / R2 / RH**: `ops/reviews/pr480-land-review-1-codex-verdict.receipt.yaml`, `ops/reviews/pr480-land-review-2-codex-verdict.receipt.yaml`, `ops/reviews/pr486-hau-kiem-review-1-codex-verdict.receipt.yaml`.
- **V1 / V2 / VH**: tệp `.md` cùng tên tương ứng, thay hậu tố `.receipt.yaml`.
- **O4 / O5 / O6**: `ops/reviews/pr478-land-review-{4,5,6}-codex-verdict.receipt.yaml` và verdict `.md` tương ứng khi nói về blob.
- **LAND**: `ops/land/pr478-land-evidence.yaml`; **INDEX**: `ops/reviews/README.md`; **DEBT**: `ops/reviews/pr486-hau-kiem-no-review.yaml`.

Nguồn đối chứng và cách tái chạy nằm trong [do-review/audit.py](do-review/audit.py). Script chỉ đọc Git/cây được review; bản sao để chạy cổng ở SHA khác được dựng dưới `do-review/` bằng archive và Git metadata riêng, dùng object mirror chỉ đọc. Không checkout/reset/chuyển HEAD hay sửa index của `cay-kho/`. Không có `refs/remotes/origin/master` trong clone; phép so dùng exact base đã giao, đồng thời xác nhận `refs/heads/master` trỏ đúng base ấy. Không coi tên remote là bằng chứng đã truy cập máy chủ.

## BẢNG ĐO

| khẳng định (tệp:key path) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| Gói: HEAD, base, trạng thái | Exact SHA đã giao; cây sạch | **2/2 OID** head/base khớp; tree như trên; **0 dòng** porcelain; `preflight.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Diff: `numstat.txt`, `diff.patch` | **13 tệp**, thêm **1.714 dòng**, bớt **81 dòng** | Diff Git tại exact hai SHA khớp danh sách và tổng | ĐO ĐƯỢC+KHỚP | Có |
| Gói: `ARTIFACTS.sha256` | Băm hiện vật đầu vào | **3.160/3.160 tệp** khớp SHA-256; `manifest.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có; không xác thực người sinh gói |
| Prompt: số ref hiện tại | **312 ref nhánh** | **313 ref nhánh** trong clone và mirror; EVIDENCE ghi đúng số này | ĐO ĐƯỢC+LỆCH | Prompt thiếu **1 ref nhánh** |
| EVIDENCE và các TSV ref | **313 ref nhánh** mỗi nguồn, không lệch tập | **313/313 cặp tên+OID** khớp clone, mirror và **3/3 TSV**; **62 tag** cục bộ; `refs.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có về snapshot cục bộ |
| L:56, lần đọc lúc `2026-09-09T09:32Z` | **312 ref nhánh** lịch sử | Gói hiện tại chụp lúc `2026-09-09T10:28:51Z`; không có inventory đúng lần đọc trước | KHÔNG ĐO ĐƯỢC | Không dùng số hiện tại để bác số lịch sử |
| L:57–58, tên nhánh | Vắng hai tên executor, có nhánh cấp lease | **2/2 tên nhánh** vắng trong snapshot; nhánh cấp lease trỏ `a2468831896601c60c216133eac2ba1366fd3254` | ĐO ĐƯỢC+KHỚP | Có, chỉ trong namespace và snapshot này |
| L:21–27,29–34,38–45,71 | Session ID/tags/parent/model, token, USD, status, connection, local branch, summary API | Không có API response hoặc transcript; **66.709 token**, **26.680 token**, **8,898 USD**, **5,127 USD** đều chưa xác minh | KHÔNG ĐO ĐƯỢC | Không gọi mạng; không giả xác thực nguyên văn thông báo lỗi |
| L:26–28, chênh lệch timestamp | **23 phút 04 giây**; **15 phút 56 giây** | **1.384 giây**; **956 giây**; **2/2 phép tính** khớp | ĐO ĐƯỢC+KHỚP | Có về số học; không đo thời gian tính toán liên tục |
| L:44,47–48, Unix epoch | `1788940800` giây Unix thành `2026-09-09T08:00:00Z`; cách lúc đo **1 giờ 32 phút** | Quy đổi đúng; hiệu mốc là **5.520 giây**; **2/2 phép tính** khớp | ĐO ĐƯỢC+KHỚP | Có về mốc được khai |
| L:47–51, trạng thái/nhân quả | Đã reset; nguyên nhân duy nhất; loại lỗi packet/lease/môi trường; bị chặn cùng lúc | Timestamp reset dự kiến không xác nhận quota khả dụng; summary cuối không loại nguyên nhân khác hay xác định cùng thời điểm | KHAI RỘNG HƠN PHÉP ĐO | Không; P2 lease |
| L:55–58, “ba phép đo ấy đúng” | Ref, PR, số comment cùng được xác nhận | Đếm ref không kiểm số PR/comment; không có nguồn API của hai phép còn lại | KHAI RỘNG HƠN PHÉP ĐO | Không |
| L:60–71, công việc/nội dung | Token không chứng minh việc packet; đồng thời khẳng định chưa push, nội dung mất | Giới hạn token đúng về logic. Hai tên ref vắng không chứng minh lịch sử push, vị trí mọi đầu ra hoặc mất nội dung | KHAI RỘNG HƠN PHÉP ĐO | Giới hạn có thật nhưng không sửa các kết luận mạnh ở đoạn trước |
| L:75–80, điều kiện cấp lại | Điều kiện dừng “đã thoả”; đề xuất revision/generation | Chưa xác minh diễn biến phiên, reset thực tế, phục hồi hoặc contract hiện hành | KHAI RỘNG HƠN PHÉP ĐO | Không; đây là kết luận có thể dẫn hành động |
| R1:`verdict_bytes`, `verdict_sha256` | **58.402 byte**, SHA-256 `443acaa6619c3a4b4765b6ca02be1435a78b59806140fe50dd6b9cfdd8a8ee7e` | Byte V1 và băm tính lại đúng; **2/2 trường** khớp | ĐO ĐƯỢC+KHỚP | Có |
| R1:`so_p1/so_p2/so_p3`, `reviewed_sha` | **1 finding P1 · 4 finding P2 · 3 finding P3**; `afddf7efe21e784fd22ed6b5aed399bc9d04a67d` | Đếm tiêu đề `^### … [P…]` và SHA trong thân V1: **4/4 trường** khớp | ĐO ĐƯỢC+KHỚP | Có |
| R1:`evidence_url` | URL blob tại `01c5a2713778d06535bad8e617be70ea4f5fac4d`, commit thêm đầu tiên | Đúng dạng URL; đúng path; log thêm tệp duy nhất ở commit ấy; blob khớp V1; **4/4 phép đối chiếu** khớp | ĐO ĐƯỢC+KHỚP | Có trong Git; không kiểm URL qua HTTP |
| R2:`verdict_bytes`, `verdict_sha256` | **36.408 byte**, SHA-256 `579fa9bb1e667b48b1924464cdccf43d7361296f299fedc89e4d14d8ccb1cee8` | Byte V2 và băm tính lại đúng; **2/2 trường** khớp | ĐO ĐƯỢC+KHỚP | Có |
| R2:`so_p1/so_p2/so_p3`, `reviewed_sha` | **0 finding P1 · 0 finding P2 · 3 finding P3**; `5b96ddc91593e9704ac3265b4e0b688059478cc8` | Tiêu đề finding và SHA trong thân V2: **4/4 trường** khớp | ĐO ĐƯỢC+KHỚP | Có |
| R2:`evidence_url` | URL blob tại `60d62aa60da45fdd7c79bd71dc17a0d2ffc1e439`, commit thêm đầu tiên | Dạng/path/commit thêm/blob: **4/4 phép đối chiếu** khớp | ĐO ĐƯỢC+KHỚP | Có trong Git |
| RH:`verdict_bytes`, `verdict_sha256` | **91.292 byte**, SHA-256 `f3e3d0c57786fa2c23c01a3216bddab3d5583109194e158e944c4b3fd2bdb94c` | Byte VH và băm tính lại đúng; **2/2 trường** khớp | ĐO ĐƯỢC+KHỚP | Có |
| RH:`so_p1/so_p2/so_p3`, `reviewed_sha` | **2 finding P1 · 4 finding P2 · 13 finding P3**; `da481f94eee0adf1fe5fc4260a535a9b48fc2627` | Tiêu đề finding và SHA trong VH: **4/4 trường** khớp; SHA là merge commit trong Git | ĐO ĐƯỢC+KHỚP | Có |
| RH:`evidence_url` | URL blob tại `ee23363171ca0a5218a5d7f067649487470acd0c`, commit thêm đầu tiên | Dạng/path/commit thêm/blob: **4/4 phép đối chiếu** khớp | ĐO ĐƯỢC+KHỚP | Có trong Git |
| R1/R2/RH:`evidence_url_ghi_chu`, bản gốc scratchpad | Băm bản nhập bằng bản gốc; không đổi LF | Đối chiếu được blob nhập với tệp hiện tại. Không có bản scratchpad trước vận chuyển | KHÔNG ĐO ĐƯỢC | Không nâng khớp blob hiện tại thành khớp bản gốc trước nhập |
| R1:thời lượng; INDEX:271 | **1.226,45 giây**, INDEX làm tròn **1.226 giây** | Hiệu mốc **1.226,449952 giây**, làm tròn khớp cả receipt và INDEX | ĐO ĐƯỢC+KHỚP | Có về số học; V1 không có trường thời lượng để đối chiếu nguồn thứ ba |
| R2:thời lượng; INDEX:269 | **928,758 giây**, INDEX **929 giây** | Hiệu mốc **928,758254 giây**, làm tròn khớp | ĐO ĐƯỢC+KHỚP | Có về số học; V2 không ghi thời lượng |
| RH:thời lượng; INDEX:270 | **1.280,648 giây**, INDEX **1.281 giây** | Hiệu mốc **1.280,647831 giây**, làm tròn khớp | ĐO ĐƯỢC+KHỚP | Có về số học; VH không ghi thời lượng |
| R1/R2/RH:`model_reviewer_identity`, `tuan_thu_cam_cua_reviewer` | Provider/surface “ĐO ĐƯỢC”; run ID, prompt, mốc, stdout/stderr hash/byte, không chết, cây sạch | Không có run.json của đúng lượt; trong cây chỉ có run.json của PR #468 lượt thứ 14 và lượt thứ 15. Metadata lịch sử chưa xác minh | KHAI RỘNG HƠN PHÉP ĐO | Phải gắn nguồn attestation như receipt cũ vừa được vá |
| R1/R2/RH:`model_da_chay`, `thread_id`, `github_submitter_identity` | Model thực/thread chưa đo; tài khoản vận chuyển không chứng minh reviewer/authority | Giới hạn model đúng; actor, PAT và phiên vận chuyển GitHub không kiểm được offline | KHÔNG ĐO ĐƯỢC | Không suy danh tính từ tên tài khoản hoặc cấu trúc receipt |
| R1/RH:`comment_ban_chieu_ghi_chu` | Comment rút gọn đủ slug/mức/phép đo; “không mang một lời khai không kiểm được”; neo lịch sử nguyên văn | Không có response/readback. Khai rút gọn không xác minh nội dung. CLAUDE chỉ mô tả trường issue/comment qua MCP, không mọi đường đọc GitHub | KHAI RỘNG HƠN PHÉP ĐO | Không; P2 receipt |
| R2:`anchor.mo_ta` | Có neo comment thứ hai; xem `comment_ban_chieu` | **0 khóa** `comment_ban_chieu` trong R2; không có địa chỉ cho neo ấy | ĐO ĐƯỢC+LỆCH | Không; chỉ xác định được blob |
| RH:5–15, `anchor.gioi_han`; INDEX:270 | Timeline “đo được”; không qua review nào; Running không bao giờ cập nhật; API là phép đo độc lập; closed nên không ai theo dõi | DEBT và VH ghi timeline là chỉ thị/attestation; không có response. Closed không đo người theo dõi | KHAI RỘNG HƠN PHÉP ĐO | Không; hậu kiểm chỉ biết phạm vi nguồn được cung cấp |
| R2:`doi_chieu_luot_1` | **7 slug ĐÃ VÁ THẬT · 1 slug VÁ HỜ · 0 slug VÁ SINH LỖI MỚI · 0 slug CHƯA VÁ**, tổng **8 slug** | **8/8 slug** trong mục đối chiếu V2 khớp phân loại; `doi-chieu.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có; không phải số mệnh đề hay số severity |
| R2:5–10; INDEX:269 | Từ không có nhãn lỗi mới suy “lượt này không tái diễn hình dạng ấy” | V2 còn P3 mới về lời tự kiểm của chính commit vá `5b96ddc`; tập nhãn của slug cũ không bao phủ mọi lỗi mới | KHAI RỘNG HƠN PHÉP ĐO | Không; giữ số đúng, rút suy luận rộng |
| R2:`dinh_chinh_loi_tu_kiem` | `rev-list` không chứng minh số commit đẩy sau duyệt; lời cũ được rút tại commit chứa V2 | Commit `60d62aa` thực sự có lời rút kết luận và giải thích giới hạn; nội dung Git và receipt khớp | ĐO ĐƯỢC+KHỚP | Có về đính chính công khai trong Git |
| R2:`dinh_chinh_loi_tu_kiem.trang_thai` | Lỗi cũng có trong báo cáo gửi chủ kho, “cả hai” đã đính chính | Báo cáo ngoài Git và readback không kèm. Commit đủ chứng minh đã rút câu ấy trong Git, không xác minh việc giao/đọc lại ngoài Git | KHÔNG ĐO ĐƯỢC | Không cáo buộc chưa gửi; chỉ không xác nhận kênh đó |
| R2:`nang_luc_do_cua_goi.so_ref`; INDEX:269 | **312 ref nhánh** của lượt thứ 2 | Chính V2:35 ghi **313 ref nhánh**; receipt/INDEX chép lại số prompt cũ mà V2 đã bác | ĐO ĐƯỢC+LỆCH | Lệch **1 ref nhánh**, độc lập với số ref của gói hiện tại |
| INDEX:269–271, byte/severity/head | Giá trị tổng hợp của ba verdict mới | **3/3 hàng** khớp receipt và verdict ở các trường này; thời lượng chỉ khớp receipt/số học như trên | ĐO ĐƯỢC+KHỚP | Có; không nói mọi prose của hàng đã đúng |
| INDEX:271, phạm vi “tiền kiểm” | “Lượt đầu tiên của kho mà findings CHẶN MERGE” | R1 nói khác các lượt gần đây; V1 xác nhận phạm vi tiền kiểm cụ thể. Không có inventory lịch sử làm căn cứ “đầu tiên của kho” | KHAI RỘNG HƠN PHÉP ĐO | Không xác nhận tính đầu tiên |
| INDEX:toàn bảng | Merge thủ công, giữ hàng cũ và hàng mới | **86/86 hàng cũ** còn đúng thứ tự; thêm **3/3 hàng mới** theo thứ tự R2, RH, R1; tổng **89 hàng**, **0 hàng trùng**, **0 hàng mất** | ĐO ĐƯỢC+KHỚP | Có |
| O4/O5/O6 và INDEX:272–274 | Hạ comment/metadata về attestation | **3/3 receipt** và **3/3 hàng** giữ đúng bản hạ lời khai; không mất ba hàng mới | ĐO ĐƯỢC+KHỚP | Có trong nhóm cũ |
| O4/O5/O6:byte/hash/SHA/count/neo | Các số cũ được bảo toàn | **3/3 verdict** khớp byte/hash tại `718fc41272cf7f9aaa004a70041906aad64a03d0`; SHA/count/INDEX khớp. Byte lần lượt **44.074 byte**, **44.069 byte**, **35.829 byte** | ĐO ĐƯỢC+KHỚP | Có; chi tiết từng trường trong `receipts.json` |
| LAND:`cross_review.hien_vat.neo_kep`; O4/O5/O6:model | Blob đo được; runtime không có nguồn gốc | **3/3 blob** vẫn được công nhận đo trực tiếp; commit neo là tổ tiên base; mốc thời lượng vẫn tính được dù sự kiện runtime là attestation | ĐO ĐƯỢC+KHỚP | Không thấy hạ quá tay ở các trường đã kiểm |
| LAND:`pre_merge_checks[0].ten/gioi_han_exact_head` | Rút CI exact head | Tên và thân cùng giới hạn checkout; workflow có lời giải thích cây merge tổng hợp. Không còn chứng nhận suite trên exact head chỉ từ run liên quan PR | ĐO ĐƯỢC+KHỚP | P1 cũ đã vá trong phạm vi lời khai |
| DEBT và LAND:`authorization_ghi_chu` | Ghi nợ hậu kiểm PR #486, tách khỏi PR #478 | Có bản ghi riêng; exact topology khớp; trạng thái nợ vẫn mở và không hồi tố approval | ĐO ĐƯỢC+KHỚP | P1 ghi nợ đã vá; sự kiện API vẫn là attestation |
| LAND:8–11,86–108,225–234 | Sửa dẫn Protocol, giới hạn tìm hiện vật, neo comment và nhánh vắng | **4/4 nhóm P2 cũ** được hạ đúng trong LAND/O4/O5/O6. Không nâng không tìm thấy thành bất khả phục hồi; không nhận ref vắng là chưa làm việc | ĐO ĐƯỢC+KHỚP | Có ở nhóm cũ; L và receipt mới lại khai vượt |
| LAND:`pre_merge_checks[0].canh_bao_doc_ket_qua`:146–149 | Vừa “đã bị hai lượt sau thay thế”, vừa chưa chứng minh required check được thay thế | Câu khẳng định cũ còn nguyên cạnh câu giới hạn mới | KHAI RỘNG HƠN PHÉP ĐO | P3 cũ vá hờ; không kết luận run đỏ thực sự còn chặn |
| Prompt: cổng receipt base/head | Base **29 biên nhận ĐẠT**, head **32 biên nhận ĐẠT**, mỗi cây **4 vi phạm** | Base **33 biên nhận ĐẠT**, head **36 biên nhận ĐẠT**, mỗi cây **0 vi phạm**; tổng vẫn **86 biên nhận** và **89 biên nhận** | ĐO ĐƯỢC+LỆCH | Lời khai trạng thái/số vi phạm không khớp mirror |
| Prompt: delta cổng | Delta **0 vi phạm** | Tập vi phạm base/head cùng rỗng; delta **0 vi phạm** | ĐO ĐƯỢC+KHỚP | Có; delta đúng không làm trạng thái “đỏ” thành đúng |
| Prompt: ba commit không thuộc tổ tiên master | `0fdd70b9`, `c69eaf2f`, `1d11f250` không phải tổ tiên | **6/6 quan hệ** commit×base/head đúng theo tập `git rev-list`; tắt replace objects. `ancestry.json` có `ok: true` từng quan hệ | ĐO ĐƯỢC+LỆCH | Ba commit thực sự đều là tổ tiên |
| LAND:`post_merge_checks[4]`, cổng tại `c87b067` | **30 biên nhận ĐẠT**, **11 biên nhận miễn trừ**, **42 biên nhận nợ**, tổng **83 biên nhận**, **0 vi phạm** | Tái chạy exact snapshot: **83/83 biên nhận** được phân loại đúng cơ cấu đã khai; **0 vi phạm**, `patch-gates.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có về khả năng tái chạy, không xác thực log lịch sử |
| BANG-CAU-TRUC:đầu vào/lá | **317 lá** từ **5 tệp YAML** | **317/317 lá** và toàn byte TSV khớp tái sinh; `bang.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có về parser, không chứng minh phủ mệnh đề |
| v2:cắt chuỗi | Tự khai trần **160 ký tự/lá** | **55 lá** bị cắt, mất **11.771 ký tự**; giữ toàn văn trong `bang-full.json` | ĐO ĐƯỢC+KHỚP | Tự khai đúng; lỗi mất dữ liệu còn nguyên |
| v2:chú thích | Thừa nhận bỏ chú thích đầu tệp | **58/58 dòng chú thích nguyên dòng** không thành node; riêng receipt mới có **38 dòng**. Còn chú thích cuối dòng DEBT:4 cũng bị bỏ | ĐO ĐƯỢC+KHỚP | Đúng về việc mất comment; tự khai không khôi phục phần bị bỏ |
| BANG-TOKEN:header | **14 “khẳng định”** | Tái sinh **14/14 hit** khớp, chỉ trên **7 dòng nguồn**. Có hit trùng epoch như SHA/ID và mảnh số context bị nhận thành tỷ số | ĐO ĐƯỢC+LỆCH | Khớp hit; không khớp đơn vị mệnh đề |
| Phép ngắn: doc-claims | Bộ kiểm mặc định | `ok: true`, quét **106 tệp**, **367 advisory**; roots không gồm `ops/land` hoặc `ops/reviews` | ĐO ĐƯỢC+KHỚP | Không dùng nó chứng nhận nội dung PR này |
| Phép ngắn: doctrine-scan, adr-song | Kiểm sao chép/đăng ký | Quét **7 tệp**, **0 chỗ chép**; **46/46 mục ADR** khớp đăng ký, công cụ nêu ngoại lệ trạng thái ADR-0016 | ĐO ĐƯỢC+KHỚP | Đúng phạm vi công cụ, không kiểm nhân quả trong prose |
| Gói gợi ý: cổng trên bản sao head đã áp | Không thêm vi phạm cấu trúc | **36 biên nhận ĐẠT**, **11 biên nhận miễn trừ**, **42 biên nhận nợ**, tổng **89 biên nhận**, **0 vi phạm**, `ok: true` | ĐO ĐƯỢC+KHỚP | Chỉ ở bản sao dưới `do-review/`, chưa chạy cây thật |

Các con số `312 ref nhánh` của R1/RH là lời ghi về gói lịch sử và tương thích với nội dung verdict tương ứng; không dùng snapshot hiện tại để sửa chúng thành `313 ref nhánh`. Chỉ R2 bị chính V2 bác rõ. Tương tự, không thay các số token, USD hoặc runtime chưa xác minh bằng số đo của phiên reviewer hiện tại.

## KHẲNG ĐỊNH CẢ HAI BẢNG BỎ SÓT

“Bỏ sót” nghĩa là không giữ đủ mệnh đề cần kiểm. Không gọi một scalar là bị bỏ nếu nó còn trong v2: ví dụ `R2:nang_luc_do_cua_goi.so_ref` vẫn có giá trị, nhưng quan hệ giữa giá trị đó với V2/INDEX chưa được bảng nào đối chiếu. V1 lần này chỉ chạy trên L; v2 chỉ chạy trên các YAML được liệt kê, hoàn toàn không có INDEX hoặc verdict Markdown làm nguồn đối chứng.

| vị trí | khẳng định | vì sao cả hai trượt | hệ quả |
|---|---|---|---|
| R1:5–7 | Tiền kiểm theo chỉ thị của lượt cụ thể, khác các lượt gần đây | Comment ngoài cây YAML; v1 không đọc receipt | Cần giữ đúng phạm vi khi viết INDEX; không tự nâng thành đầu tiên toàn kho |
| R1:9–13 | Bộ lọc đếm hit, tự khai thiên vị không miễn kiểm mệnh đề | V2 bỏ comment; v1 không đọc nguồn này | Mệnh đề đúng cũng mất; bổ sung inventory, không chỉ liệt kê lỗi |
| R2:5–10 | Không có nhãn lỗi mới nên hình dạng bản vá sinh lỗi không tái diễn | Các khóa số được giữ nhưng câu suy luận nằm trong comment | Giữ số phân loại, rút kết luận bao phủ mọi lỗi |
| RH:5–9 | Timeline đã đo; không review nào; Running không bao giờ cập nhật | Toàn bộ là comment; v1 không đọc receipt | Nâng chỉ thị/attestation thành sự kiện được chứng nhận |
| RH:11–15 | Hai phép đo độc lập cho cùng kết luận | Quan hệ độc lập/cùng kết luận nằm trong comment | Reviewer chưa xác minh API; không dùng lời điều phối làm chứng cứ độc lập cho chính nó |
| R1:39–43; RH:41–45 | Không mang lời khai không kiểm được; neo cũ nguyên văn; phạm vi đường đọc | V2 cắt sâu trong giá trị trước phần này; v1 không đọc YAML | Khai rút gọn không thay đối chứng comment |
| R1/RH:`evidence_url_ghi_chu` | Bản nhập bằng bản gốc, không đổi LF | V2 giữ đầu lá, cắt phần chứng nhận vận chuyển; v1 không đọc YAML | Khớp blob hiện tại không xác thực bản trước vận chuyển |
| R1/RH:`model_bang_chung`, `neo_boi_launcher` | Khả năng ghi field của launcher chứng nhận đúng lần chạy | Giá trị dài bị cắt; v1 không đọc receipt | Không có run.json đúng lượt; phải phân biệt mã công cụ với dữ liệu runtime |
| R2:`dinh_chinh_loi_tu_kiem.trang_thai` | YAML không tái mở P1; cả lời commit và báo cáo đã đính chính | V2 cắt phần báo cáo; v1 không đọc receipt | Git đính chính kiểm được; sự kiện giao nhận ngoài Git chưa kiểm được |
| R2:`anchor.mo_ta` và cấu trúc receipt | Neo comment thứ hai phải có địa chỉ đối chiếu | V2 giữ đoạn đầu nhưng không đối chiếu sự vắng mặt của khóa được dẫn; v1 không đọc nguồn | Trường trỏ tới khóa không tồn tại dễ thành chứng nhận neo kép giả |
| LAND:8–11 | “Có nhắc” là proxy, không chứng minh cưỡng chế | Comment bị bỏ sạch; v1 chỉ đọc L | Giới hạn đúng của bản vá cũ không xuất hiện trong bảng |
| LAND:`cross_review.hien_vat.neo_kep` | Blob đo được, comment chỉ attestation, cần phân biệt lớp đọc | V2 cắt phần sau của lá; v1 không đọc LAND | Bảng có thể giữ câu tích cực nhưng mất giới hạn ngay sau |
| LAND:146–149 | Run đã bị thay thế, đồng thời chưa biết required check bị thay thế | V2 cắt trước cả hai câu; v1 không đọc LAND | Cặp khẳng định/giới hạn mâu thuẫn không được báo |
| L:50–51 | Nguyên nhân duy nhất, loại các lỗi khác, cùng thời điểm | V1 không trích quan hệ, v2 không đọc Markdown | Sai phạm vi suy luận dù có các con số API |
| L:60–76 | Chưa push, nội dung mất, điều kiện dừng đã thoả | V1 chỉ giữ mảnh thời lượng; v2 không đọc Markdown | Câu phủ định/khẳng định quan trọng cho cấp lại lease bị bỏ |
| INDEX:269–271 | “Không sinh lỗi mới”, “tiền kiểm đầu tiên”, “PR không ai theo dõi” | Cả hai parser đều không đọc INDEX | Mục lục sinh thêm kết luận ngoài receipt/verdict mà không có hàng bảng tương ứng |
| DEBT:nguồn timeline và chú thích | Số hiệu PR là định danh; timeline là attestation; hậu kiểm không hồi tố approval | V2 bỏ comment cuối dòng và cắt các lá dài; v1 không đọc DEBT | Mất các giới hạn đúng đang ngăn đọc hồ sơ thành approval |

Các hàng cùng nguyên nhân được gộp thành finding dưới đây, không nhân severity theo từng câu. Hai P3 parser cũ vẫn mở; tự khai thiên vị không làm văn bản đã mất quay lại bảng.

### lease-nguyen-nhan-va-dieu-kien-dung-khai-vuot  [P2]  Biên bản loại nguyên nhân khác và tuyên đủ điều kiện cấp lại vượt dữ liệu

TỆP/DÒNG: L:17,36,47–51,55–65,75–80.

VẤN ĐỀ: Phần giới hạn `output_tokens` đúng nhưng không chi phối các kết luận trước/sau nó. Ngay cả giả sử bản chép API đúng, lỗi hạn mức cuối phiên không chứng minh không có lỗi packet/lease/môi trường; mốc reset dự kiến không xác nhận tài khoản đã khả dụng. Snapshot không có hai tên nhánh không loại trường hợp đã push rồi xoá, push tên khác hoặc còn nội dung có thể phục hồi. Vì vậy “nội dung mất”, “không có hiện vật nào được đẩy lên” và “điều kiện dừng đã thoả” đều mạnh hơn nguồn. Đây không chỉ là thiếu mạng: các suy luận vẫn thiếu ngay khi chấp nhận con số API được thuật lại.

ĐÃ THỬ VÁ: Thu hẹp cả tiêu đề, phần nguồn, nhân quả và kết luận hành động; giữ bảng API dưới nhãn attestation và giữ số học đúng. Thêm kết quả ref tại đúng snapshot gói hiện tại, không sửa ngược số ref lịch sử. Điều kiện cấp lại để chưa chứng minh; không cấp lease hoặc đòi chủ kho duyệt việc review đã được giao.

GÓI VÁ: [cay/ops/DO_VI_SAO_LEASE_482_483_CHET_20260909.md](cay/ops/DO_VI_SAO_LEASE_482_483_CHET_20260909.md). **Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.**

ĐÃ THỬ NGHIỆM: Đọc toàn văn L và đối chiếu nguồn; **2/2 khoảng timestamp**, **2/2 phép tính epoch/hiệu reset**, **2/2 tên nhánh** đúng phạm vi. `refs.json` có `ok: true`. Phản chứng logic cụ thể: nhánh từng push rồi bị xoá cho cùng snapshot không có tên, nhưng phủ định kết luận chưa từng push. Không tạo nhánh/phiên thật để thử. Khi executor áp, đọc lại tiêu đề và kết luận cùng phần giới hạn; giữ cặp mốc nguồn để tái tính. Rủi ro bản vá: hạ quá tay số học hoặc tuyên dữ liệu API sai; bản gợi ý tránh cả hai, chỉ hạ mức xác thực và suy luận.

ĐỘ TIN: cao về phạm vi suy luận; không xác minh sự kiện API.

### bien-nhan-moi-lai-nang-attestation-thanh-do-doc-lap  [P2]  Receipt mới tái tạo lỗi nguồn vừa hạ ở receipt cũ

TỆP/DÒNG: R1:34–49,59–64,80–92,135–142; R2:60–75,124–130; RH:5–15,36–54,62–68,134–142; INDEX:269–271.

VẤN ĐỀ: R1/RH rút lời nguyên văn nhưng thay bằng lời “đủ slug, mức, phép đo” và “không mang một lời khai không kiểm được”, trong khi không giao response/readback. Đồng thời chúng gọi comment cũ là nguyên văn, trái mức attestation vừa áp cho O4/O5/O6. R2 còn tuyên neo comment thứ hai mà thiếu hẳn khóa địa chỉ. RH nâng timeline vốn được DEBT/VH ghi là chỉ thị/attestation thành “đo được”, “không bao giờ được cập nhật”, rồi suy PR closed nên không ai theo dõi. Các receipt mới cũng tái dùng câu runtime “ĐO ĐƯỢC từ run.json” dù không lưu đúng run.json. Đây là lỗi nguồn lặp lại ở nhóm hiện vật mới, không phải bằng chứng các API/comment thực sự sai.

R1 còn dẫn finding `neo-comment-khai-vuot-lop-doc` như của “lượt này”, nhưng **8/8 tiêu đề finding** V1 không có slug đó; slug thuộc VH. `CLAUDE.md:127–145` nói về trường thân issue/comment qua máy chủ MCP cụ thể; không cấp phép khái quát mọi đường đọc GitHub. Tại R2, commit `60d62aa` đính chính lời tự kiểm là thật và giữ nguyên công đó; phần báo cáo ngoài Git chỉ chưa xác minh, không mặc định chưa giao.

ĐÃ THỬ VÁ: Tách blob có thể băm khỏi bản gốc scratchpad, runtime, comment và API timeline chưa có nguồn. Gắn attestation đồng bộ trong receipt/INDEX; R2 chỉ khai neo blob khi chưa có địa chỉ comment; chỉ rõ slug nhận xét thuộc VH. Giữ nguyên verdict, các OID/hash/byte/severity và scalar runtime; không giả bổ sung log còn thiếu.

GÓI VÁ: [R1 đã sửa](cay/ops/reviews/pr480-land-review-1-codex-verdict.receipt.yaml), [R2 đã sửa](cay/ops/reviews/pr480-land-review-2-codex-verdict.receipt.yaml), [RH đã sửa](cay/ops/reviews/pr486-hau-kiem-review-1-codex-verdict.receipt.yaml), [INDEX đã sửa](cay/ops/reviews/README.md). **Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.**

ĐÃ THỬ NGHIỆM: Đối chiếu **3/3 receipt**, đọc các run.json có trong cây và thấy chúng thuộc lượt khác. **3/3 bộ identity hiện vật** và scalar runtime được bảo toàn trong gợi ý; INDEX giữ **89/89 hàng** cùng thứ tự, **86/86 hàng cũ** nguyên byte. Bản sao head áp gợi ý chạy cổng receipt: **0 vi phạm**, **0 trường hợp chưa đo**, `patch-gates.json` có `ok: true`; kiểm cấu trúc không chứng minh nội dung comment. Cách khóa phù hợp là lưu response và bước biến đổi của đúng lượt, hoặc giữ nhãn nguồn chưa xác minh; không dùng regex “có disclaimer” thay đọc toàn câu. Rủi ro: xoá công đo Git khi hạ nguồn runtime; bản gợi ý giữ riêng việc blob/commit/đếm finding đo được.

ĐỘ TIN: cao về nguồn thiếu, neo thiếu và mâu thuẫn phạm vi; API lịch sử KHÔNG ĐO ĐƯỢC.

### bien-nhan-luot-hai-chep-sai-so-ref  [P3]  Receipt và INDEX bỏ qua số ref đã được chính verdict đính chính

TỆP/DÒNG: R2:103,115; INDEX:269; V2:35.

VẤN ĐỀ: R2 ghi **312 ref nhánh**; INDEX lặp lại. V2 nói rõ prompt cũ ghi **312 ref nhánh** nhưng đã đo **313 ref nhánh** khớp clone/mirror/TSV. Đây là lệch giữa các nguồn trong kho, không cần dựa vào snapshot mới và không phải bằng chứng R1/RH sai số lịch sử.

ĐÃ THỬ VÁ: Đổi riêng R2 `so_ref` thành **313 ref nhánh** theo V2, sửa lời INDEX và bỏ bản số lặp trong manifest để trỏ về trường nguồn. Giữ số lịch sử của R1/RH.

GÓI VÁ: R2 và INDEX trong `cay/`, cùng gói P2. **Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.**

ĐÃ THỬ NGHIỆM: **3/3 nguồn** receipt/verdict/INDEX được đối chiếu về cùng lượt; `patch-validation.json` xác nhận trường đã sửa và giữ identity. Cách khóa: bắt mỗi số inventory nhận diện đúng lượt/snapshot, không lấy số prompt thay kết quả reviewer. Rủi ro: cập nhật hàng loạt mọi `312` thành `313`; gợi ý chỉ sửa đúng R2.

ĐỘ TIN: cao về lệch nội bộ; không tái chạy gói lịch sử.

### khong-co-nhan-loi-moi-khong-phai-khong-sinh-loi-moi  [P3]  Số nhãn đúng bị nâng thành bảo đảm bản vá không sinh lỗi

TỆP/DÒNG: R2:5–10; INDEX:269; V2:17–26,144–156; commit `5b96ddc91593e9704ac3265b4e0b688059478cc8`.

VẤN ĐỀ: Đếm **8/8 slug cũ** khớp: **7 slug ĐÃ VÁ THẬT**, **1 slug VÁ HỜ**, **0 slug** mang nhãn lỗi mới. Nhưng V2 còn finding mới `doi-chieu-dem-commit-khong-dinh-thoi-diem` về câu tự kiểm do chính commit vá thêm. Số nhãn của tập slug cũ không chứng minh “lượt này không tái diễn” hình dạng bản vá sinh lỗi. Không vì thế sửa số phân loại hoặc tái mở P1 của YAML đã đúng.

ĐÃ THỬ VÁ: Giữ phân loại và kết luận approve tại exact SHA; thay suy luận tổng quát bằng phạm vi “nhãn của slug cũ”, nêu riêng P3 lời tự kiểm mới.

GÓI VÁ: R2 và INDEX trong `cay/`, cùng gói P2. **Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.**

ĐÃ THỬ NGHIỆM: `doi-chieu.json` có `ok: true` cho **8/8 slug**; đối chiếu thêm finding mới và nội dung đính chính của commit `60d62aa`. Cách khóa: giữ riêng bảng trạng thái slug cũ và tập finding mới; chỉ dùng kết luận bao phủ toàn bộ khi đã xét cả hai tập. Rủi ro: đọc P3 mới thành P1 hồi tố; bản gợi ý không làm vậy.

ĐỘ TIN: cao về phạm vi tập đếm và nội dung Git.

### readme-tuyen-tien-kiem-dau-tien-qua-pham-vi-nguon  [P3]  INDEX biến tiền kiểm của lượt cụ thể thành đầu tiên toàn kho

TỆP/DÒNG: INDEX:271; đối chiếu R1:5–7 và phần mở V1.

VẤN ĐỀ: “Lượt đầu tiên của kho mà findings CHẶN MERGE” rộng hơn “khác các lượt gần đây” và chỉ thị tiền kiểm PR #480. Không có inventory lịch sử review/merge làm nguồn cho tính đầu tiên. Đây là kết luận không được chứng minh, không phải tôi đã kiểm GitHub và chứng minh một thứ tự lịch sử ngược lại.

ĐÃ THỬ VÁ: INDEX chỉ nói chủ kho giao tiền kiểm trong phạm vi lượt này. Không sửa lời reviewer gốc hoặc dựng lại các review thiếu hiện vật.

GÓI VÁ: INDEX trong `cay/`, cùng gói P2. **Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.**

ĐÃ THỬ NGHIỆM: Đối chiếu **2/2 nguồn trực tiếp** R1/V1 và hàng INDEX; giữ byte/severity/head của hàng. Cách khóa: mọi từ “đầu tiên”, “mọi”, “không bao giờ” trong mục lục cần nguồn cùng phạm vi hoặc phải thu hẹp. Rủi ro: hạ cả sự thật có chỉ thị tiền kiểm; gợi ý vẫn giữ điều đó.

ĐỘ TIN: cao về sự mở rộng phạm vi; tính đầu tiên lịch sử chưa được xác minh.

### ha-ket-luan-unstable-con-giu-check-da-thay-the  [P3]  Bản hạ lời khai giữ nguyên câu required check đã bị thay thế

TỆP/DÒNG: LAND:146–149; finding cũ `nguyen-nhan-unstable-chua-co-nguon-phan-dinh` ở VH:206–217.

VẤN ĐỀ: Câu “Nó đã bị hai lượt sau thay thế” vẫn ở nguyên trước câu mới “không … coi một run xanh khác tên là bằng chứng required check đã được thay thế”. Đã hạ nguyên nhân unstable, nhưng chưa hạ hết lời chứng nhận thay thế check. Đây là P3 cũ vá hờ, không phải phát hiện một cơ chế CI mới bị phá; mã workflow không đổi.

ĐÃ THỬ VÁ: Thay câu khẳng định bằng lời có hai run xanh được thuật lại, chưa chứng minh context của run đỏ đã bị thay thế. Giữ nguyên run ID và số bước nguồn.

GÓI VÁ: [cay/ops/land/pr478-land-evidence.yaml](cay/ops/land/pr478-land-evidence.yaml), bổ sung tự nguyện cho P3. **Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.**

ĐÃ THỬ NGHIỆM: Đọc **2/2 câu** khẳng định/giới hạn cùng key path; bản sửa parse YAML thành công, giữ cấu trúc. Cách khóa: đọc trọn giá trị `canh_bao_doc_ket_qua`, không chỉ grep câu giới hạn mới. Rủi ro: đảo sang khẳng định run đỏ chắc chắn vẫn chặn; gợi ý cũng không kết luận phía đó. Sự kiện GitHub KHÔNG ĐO ĐƯỢC.

ĐỘ TIN: cao về câu còn sót; không xác minh trạng thái check.

### bang-khang-dinh-token-khong-phai-menh-de  [P3]  Bảng tái sinh đúng nhưng cắt mất nghĩa và gọi hit thành khẳng định

TỆP/DÒNG: `trich_khang_dinh_v2.py:43–44`, `trich_khang_dinh.py:41`; `BANG-CAU-TRUC.tsv`, `BANG-TOKEN.tsv`.

VẤN ĐỀ: V2 giữ **317 lá YAML**, nhưng **55 lá** mất tổng **11.771 ký tự**; các đuôi bị cắt có chính lời “không mang một lời khai không kiểm được”, giới hạn nguồn và quan hệ required check. V1 có **14 hit** trên **7 dòng nguồn**, không phải **14 mệnh đề**: epoch bị gắn đồng thời nhãn SHA/ID; hai mảnh của `context_usage.used_tokens` bị nhận thành tỷ số. Không dùng các tỷ số sai ấy làm bằng chứng dương. Số mất **6.030 ký tự trên 18 lá** thuộc lượt cũ, không phải số đo PR này.

ĐÃ THỬ VÁ: Giữ [toàn bộ lá và đuôi bị cắt](do-review/bang-full.json), [thống kê từng tệp](do-review/bang-stats.json) và inventory mệnh đề thủ công ở trên. Không sửa parser đầu vào để rồi báo nó vốn đã đủ. Hướng sửa công cụ: giữ toàn giá trị, vị trí nguồn và tên đơn vị hit/lá; bước đọc nghĩa vẫn phải riêng.

GÓI VÁ: Không bắt buộc tệp sản phẩm cho P3; dữ liệu bổ sung ở `do-review/`. Hai script đầu vào nguyên trạng.

ĐÃ THỬ NGHIỆM: **317/317 lá**, **14/14 hit** tái sinh byte-identical; `bang.json`, `ok: true`. Kiểm độ dài của từng giá trị trước/sau cắt, không suy mọi prose đều mất. Cách khóa: fixture có phủ định sau trần cắt phải còn toàn văn trong output; giữ ca định danh không bị gọi là đại lượng. Rủi ro: JSON đầy đủ vẫn không tự hiểu nhân quả; không nhận công đã giải quyết ngữ nghĩa bằng đổi định dạng.

ĐỘ TIN: cao; P3 công cụ cũ chưa đóng.

### bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon  [P3]  Chú thích đầu receipt và các lớp ngoài đầu vào không được đối chiếu

TỆP/DÒNG: `trich_khang_dinh_v2.py:37`; khối comment R1:1–13, R2:1–10, RH:1–15; DEBT:4; INDEX:269–274.

VẤN ĐỀ: Safe-load bỏ chú thích ở mọi vị trí. **58 dòng chú thích nguyên dòng** của các YAML đầu vào không thành node, gồm **38 dòng** đầu receipt mới. Chú thích inline tại DEBT:4 cũng mất. V1 chỉ đọc L nên không bổ sung được các câu này. INDEX không phải đầu vào của cả hai parser, trong khi chính nó chứa lời khai mới mạnh hơn nguồn. Đây là độ phủ có thiếu thật dù nhiều câu trong khối comment hoàn toàn đúng.

ĐÃ THỬ VÁ: Lưu [inventory chú thích nguyên dòng](do-review/bang-comments.json), đọc thủ công comment inline và toàn bộ các hàng INDEX thay đổi, bổ sung bảng mệnh đề ở trên. Hướng sửa: lấy vị trí nguồn/comment và khai rõ tập tệp được đọc; không tuyên parser đã phủ toàn diff chỉ từ số lá.

GÓI VÁ: Không bắt buộc cho P3; inventory và bảng đo là hiện vật bổ sung. Các sửa nội dung sai cụ thể đã ở gói P2.

ĐÃ THỬ NGHIỆM: **58/58 dòng** comment nguyên dòng được lưu nguyên văn/vị trí, đối chiếu với dữ liệu safe-load; không gọi phép lấy dòng bắt đầu `#` là parser mọi dạng comment YAML. Cách khóa: giữ fixture comment đầu tệp, giữa tệp và cuối dòng, phân biệt ký tự `#` trong scalar; kiểm inventory đầu vào phải chứa các tệp mục lục đang được thay đổi. Rủi ro: trích comment đúng vẫn không xác thực câu bên trong; việc đó thuộc review nguồn.

ĐỘ TIN: cao; P3 công cụ cũ chưa đóng.

## GÓI VÁ VÀ GIỚI HẠN XÁC MINH

Có **6 tệp đầy đủ** dưới [cay/](cay/), không phải diff. [GOI-VA.md](GOI-VA.md) liệt kê đường dẫn và phạm vi. Nhãn áp dụng cho toàn bộ gói: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

Đã đọc bản gợi ý, parse **4/4 tệp YAML**, giữ **3/3 bộ identity** verdict và scalar runtime, giữ **89/89 hàng INDEX** cùng thứ tự, giữ **86/86 hàng cũ** nguyên byte. Đã chạy cổng receipt trên bản sao head có gợi ý: `ok: true`, **0 vi phạm**. Không có tệp verdict gốc nào dưới `cay/`; không nâng timeout hay sửa workflow. Script sinh gợi ý: [generate_patch.py](do-review/generate_patch.py).

Bản sao kiểm base/head và commit land chỉ xác minh khả năng tái chạy với object trong mirror. Không xác nhận ai từng chạy cổng, log nào từng được gửi, hoặc vì sao môi trường điều phối đã báo đỏ. Với mirror hiện có, câu hỏi đúng là **môi trường/HEAD/độ đầy đủ lịch sử nào đã sinh lời khai bốn vi phạm**, chứ không coi master đỏ là tiền đề. Không có snapshot môi trường điều phối để phân định nguyên nhân sai khác.

Mọi truy vấn GitHub, API quản lý phiên, dữ liệu readback comment, trạng thái quota thực, bản báo cáo ngoài Git, log runtime gốc và bảo vệ ref: **KHÔNG ĐO ĐƯỢC** khi không có mạng/nguồn thô. Bộ test dài, CI, native Windows và thao tác phiên/lease: **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**; không chạy. Các lệnh ngắn đã ghi không được dùng thay bộ test đó. Không có hành động cấp lease, đăng Issue/PR/comment, merge hoặc sửa kho thật.
