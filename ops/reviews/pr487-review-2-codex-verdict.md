verdict: approve
reviewed_sha: 5c05778219e293ff929e8cb1f1c31aea4120d967
base_da_review_luot_truoc: bcbca7bbcea968a662b1ac69bfc9f2a329ed8ae7
base_sha: da481f94eee0adf1fe5fc4260a535a9b48fc2627
luot: 2
so_lan_luot_nay_bi_chet_va_phong_lai: 0

**Kết luận: 0 finding P1 · 0 finding P2 · 6 finding P3 còn mở ở lượt này. Hai finding P2 cũ đã đóng trong phạm vi lời khai nguồn và điều kiện cấp lại lease. Bản vá có sinh lỗi hồ sơ mới ở mức P3; không thể nói “không sinh lỗi mới”.** Tôi approve exact SHA trên trong phạm vi review offline được giao. Đây không phải thao tác duyệt hoặc quyền merge trên GitHub. Điều kiện hết finding P1 của chủ kho đã đạt từ lượt trước; các finding P3 dưới đây không được nâng thành yêu cầu lặp vô hạn.

Reviewer: Codex/OpenAI, chạy lệnh cục bộ qua công cụ API, transport machine; khác phiên executor Claude. Không xác thực model/session của các lượt cũ từ tài khoản vận chuyển. Tree được đo: `650ca654ea9fc91cdcd18337f7eb61a1bf00cf1a`. Quan sát **0 lần** chết/phóng lại. Cây review giữ detached, porcelain **0 byte**.

Đơn vị: `luot` đếm lượt; trường chết/phóng lại đếm lần. SHA/hash, số hiệu PR/ADR, session ID, mã thoát, schema, revision/generation và số dòng là định danh hoặc giá trị schema. Các phép đếm còn lại luôn nêu đơn vị: finding, slug, trường, tệp, hàng, dòng, lá, hit, ref nhánh, tag, ký tự hoặc byte. Cặp `N/N` chỉ là bằng chứng dương khi hai số bằng nhau; các tỷ lệ phân bố không phải kết quả pass. `ok: true` trong hiện vật chỉ xác nhận phép kiểm được mô tả, không xác thực mọi sự kiện nguồn.

Tên rút gọn:

- **L**: `ops/DO_VI_SAO_LEASE_482_483_CHET_20260909.md`.
- **R1 / R2 / RH / R487**: `ops/reviews/pr480-land-review-1-codex-verdict.receipt.yaml`, `pr480-land-review-2-codex-verdict.receipt.yaml`, `pr486-hau-kiem-review-1-codex-verdict.receipt.yaml`, `pr487-review-1-codex-verdict.receipt.yaml`.
- **V1 / V2 / VH / V487**: verdict `.md` tương ứng, cùng thư mục.
- **INDEX**: `ops/reviews/README.md`; **LAND**: `ops/land/pr478-land-evidence.yaml`; **DEBT**: `ops/reviews/pr486-hau-kiem-no-review.yaml`.

Lệnh tái đo: `python3 do-review/audit.py` và `python3 do-review/supplement.py`, chạy từ gốc gói. Chúng chỉ đọc `cay-kho/`; kết quả ghi dưới `do-review/` và gợi ý dưới `cay/`. Git tắt replace objects và optional locks. Phần phép chiếu API trong script thứ hai dùng fixture tổng hợp, không giả làm response API thật.

## ĐỐI CHIẾU LƯỢT 1

- `lease-nguyen-nhan-va-dieu-kien-dung-khai-vuot`: **ĐÃ VÁ THẬT** — L:1–10,43–60,64–99 đã thu hẹp đồng bộ tiêu đề, nguồn, nhân quả, lịch sử push và điều kiện cấp lại. Không còn tuyên hạn mức đã khả dụng hoặc loại trừ lỗi khác. Tái tính **2/2 khoảng timestamp**, **2/2 phép quy đổi/hiệu reset**; giữ số học đúng mà không chứng nhận nguồn API. Snapshot hiện tại xác nhận **2/2 tên nhánh** dự kiến vắng; không dùng nó xác thực snapshot lịch sử. `special.json` và `refs.json`: `ok: true`.
- `bien-nhan-moi-lai-nang-attestation-thanh-do-doc-lap`: **VÁ SINH LỖI MỚI** — phần P2 cũ đã vá thật: **3/3 receipt cũ** hạ runtime/comment/timeline về đúng nguồn; **2/2 verdict nguồn** xác nhận chuyển slug đúng; khóa comment vắng ở `bcbca7b`, có ở `5c05778`. Nhưng phần điều phối bổ sung khóa không cập nhật INDEX:270, nơi vẫn khẳng định “Receipt chưa có URL comment bản chiếu”. Đây là lệch nội bộ mới **mức P3**, không phải P2 về chứng nhận comment đã tái phát. `special.json`: `ok: true`; `omissions.json:index_missing_url`: `ok: true`.
- `bien-nhan-luot-hai-chep-sai-so-ref`: **VÁ SINH LỖI MỚI** — R2:108–112 và INDEX:270 đã sửa đúng thành **313 ref nhánh** theo V2. Nhưng R487:106,120 và INDEX:269 lại ghi **312 ref nhánh**, trái **313 ref nhánh** mà V487:32–33 đã đính chính. Giữ slug vì cùng lỗi lấy số prompt thay kết quả verdict, nay chuyển sang biên nhận mới. Đối chiếu **2/2 verdict nguồn** V2/V487, không lấy snapshot lượt này để bác lịch sử.
- `khong-co-nhan-loi-moi-khong-phai-khong-sinh-loi-moi`: **ĐÃ VÁ THẬT** — R2:5–7 và INDEX:270 đã phân biệt nhãn của slug cũ với finding mới. V2 có đủ **8/8 slug** được phân loại như receipt: **7 slug ĐÃ VÁ THẬT**, **1 slug VÁ HỜ**, **0 slug VÁ SINH LỖI MỚI**, **0 slug CHƯA VÁ**; đồng thời còn finding `doi-chieu-dem-commit-khong-dinh-thoi-diem`. Lời đính chính của commit `60d62aa` vẫn còn; không phủ nhận công sửa đó.
- `readme-tuyen-tien-kiem-dau-tien-qua-pham-vi-nguon`: **VÁ SINH LỖI MỚI** — INDEX:272 đã thu hẹp tiền kiểm về chỉ thị của lượt cụ thể. Nhưng INDEX:269 và R487:5–7 lại mở rộng sang “khác mọi lượt trước” và “không ai kiểm những con số ấy trước lượt này”. VH đã review hồ sơ/biên nhận/mục lục của điều phối; V2 đã bắt lời tự kiểm của điều phối. Hai phản chứng này không cho phép tuyên tính duy nhất toàn lịch sử. Đây là cùng lỗi khái quát quá phạm vi nguồn, mức P3.
- `ha-ket-luan-unstable-con-giu-check-da-thay-the`: **ĐÃ VÁ THẬT** — LAND:146–151 đã bỏ câu run đỏ “đã bị hai lượt sau thay thế”, nói rõ chưa chứng minh required-check context được thay thế; câu giới hạn kế tiếp cùng nghĩa. **2/2 câu** nhất quán sau sửa. Không kết luận ngược rằng run đỏ chắc chắn vẫn chặn. Sự kiện GitHub vẫn KHÔNG ĐO ĐƯỢC.
- `bang-khang-dinh-token-khong-phai-menh-de`: **VÁ HỜ** — công sửa mất đuôi là thật: bảng đầy đủ giữ **392/392 lá**, **0 lá** bị cắt; phục hồi **15.439 ký tự** giá trị trên **73 lá**. Nhưng bảng token vẫn gọi **20 hit** trên **10 dòng nguồn** là “khẳng định”, vẫn có tỷ số giả `392/1`, `175/1` và epoch bị gắn cả SHA/ID. Không đóng toàn slug chỉ từ việc thêm bảng đầy đủ. `tables.json`: `ok: true` về tái sinh, không về ngữ nghĩa token.
- `bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon`: **VÁ HỜ** — giữ đúng **67/67 dòng** chú thích nguyên dòng của **6/6 tệp YAML** là sửa thật. Nhưng comment cuối dòng DEBT:4 vẫn mất; INDEX và các verdict Markdown vẫn ngoài đầu vào; L chỉ đi qua token regex. Đây là các lớp thiếu đã được lượt trước nêu rõ, rộng hơn việc chưa tách mệnh đề trong một lá. `tables.json` và **7/7 ca bỏ sót** trong `omissions.json`: `ok: true`.

Tổng phân loại **8/8 slug**: **3 slug ĐÃ VÁ THẬT · 2 slug VÁ HỜ · 3 slug VÁ SINH LỖI MỚI · 0 slug CHƯA VÁ**. Đây là số trạng thái slug, không phải severity. Nhãn sinh lỗi mới ở slug P2 thứ hai chỉ nói phát sinh mâu thuẫn INDEX mức P3; phần P2 cũ đã được đóng.

## BẢNG ĐO

| khẳng định (tệp:key path) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| Gói: HEAD/master/detached | Exact head/base đã giao, cây sạch | **2/2 OID** khớp; detached; porcelain **0 byte**; `preflight.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Gói: diff từ lượt trước | `numstat-luot1-den-luot2.txt`, `diff-sau-luot1.patch` | **2/2 tệp** khớp byte với Git; đổi **8 tệp**, thêm **582 dòng**, bớt **144 dòng**; `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Gói: `ARTIFACTS.sha256` | Hash đầu vào | **3.162/3.162 tệp** khớp; `manifest.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có về tính toàn vẹn, không xác thực người sinh |
| Prompt: refs/heads hiện tại | **312 ref nhánh** | Clone và mirror đều **313 ref nhánh**; không sửa ref để ép khớp prompt | ĐO ĐƯỢC+LỆCH | Lệch **1 ref nhánh** |
| EVIDENCE/TSV: tập ref tại mốc chụp `2026-09-09T11:03:40Z` | **313 ref nhánh**, không lệch | **313/313 cặp tên+OID** khớp clone/mirror và **3/3 TSV** sau chuẩn hóa đúng cột; **62 tag** cục bộ; `refs.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có về snapshot cục bộ; không xác minh máy chủ |
| L:66,69: số ref lịch sử | **312 ref nhánh** lúc đọc API; hậu kiểm ghi **313 ref nhánh** ở mốc khác | V487 xác nhận lời thuật hậu kiểm; không có inventory của lần đọc API để tái đo | KHÔNG ĐO ĐƯỢC | Không thay số lịch sử bằng số hiện tại |
| L:70–72: tên nhánh và OID cấp lease | Vắng hai tên; ref cấp lease trỏ `a2468831896601c60c216133eac2ba1366fd3254` | **2/2 tên nhánh** vắng trong snapshot hiện tại; OID ref khớp; `refs.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có, giới hạn đúng snapshot/namespace |
| L:35,54–55: số học | **23 phút 04 giây**, **15 phút 56 giây**; epoch thành mốc UTC; hiệu **1 giờ 32 phút** | **1.384 giây**, **956 giây**, `2026-09-09T08:00:00Z`, **5.520 giây**; **4/4 phép tính** khớp | ĐO ĐƯỢC+KHỚP | Không xác thực timestamp API |
| L:28–41,48–51,85: API phiên | Session/model/status/connection, token, chi phí, summary; đã gắn attestation | Không có response nguồn; kể cả `FAILED`/`IDLE` cũng chưa phân định được quan hệ thời điểm/trường API | KHÔNG ĐO ĐƯỢC | Không nhận là sự kiện đã đo |
| L:58–60,78–99: nhân quả và cấp lại | Chưa loại trừ lỗi khác, chưa chứng minh lịch sử push/mất nội dung/đủ điều kiện cấp lại | Cả phần giải thích và kết luận đều đã giới hạn; số học không được dùng thay xác thực nguồn | ĐO ĐƯỢC+KHỚP | P2 cũ đóng |
| R1:`verdict_bytes`, `verdict_sha256`, `so_p*`, `reviewed_sha` | **58.402 byte**; **1 finding P1 · 4 finding P2 · 3 finding P3** | Băm đúng `443acaa6619c3a4b4765b6ca02be1435a78b59806140fe50dd6b9cfdd8a8ee7e`; đếm lại tiêu đề và SHA khớp; `receipts.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| R2:các trường identity verdict | **36.408 byte**; **0 finding P1 · 0 finding P2 · 3 finding P3** | Băm đúng `579fa9bb1e667b48b1924464cdccf43d7361296f299fedc89e4d14d8ccb1cee8`; số finding và SHA khớp | ĐO ĐƯỢC+KHỚP | Có |
| RH:các trường identity verdict | **91.292 byte**; **2 finding P1 · 4 finding P2 · 13 finding P3** | Băm đúng `f3e3d0c57786fa2c23c01a3216bddab3d5583109194e158e944c4b3fd2bdb94c`; số finding và SHA khớp | ĐO ĐƯỢC+KHỚP | Có |
| R487:các trường identity verdict | **43.342 byte**; **0 finding P1 · 2 finding P2 · 6 finding P3**; reviewed SHA lượt trước | Băm đúng `f1eb4c78c242ebc748b608e2c09696498050ff6b15c00d629e9ac0233dc08edd`; SHA và tiêu đề finding khớp; `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| R1/R2/RH/R487:`evidence_url` | Commit đầu tiên chứa verdict; đúng path/blob | **4/4 neo** khớp: `01c5a2713778d06535bad8e617be70ea4f5fac4d`, `60d62aa60da45fdd7c79bd71dc17a0d2ffc1e439`, `ee23363171ca0a5218a5d7f067649487470acd0c`, `a0b154d7c8e6491fb53825301ace2d6d4e97ac9f`. Log thêm tệp trong lịch sử reachable, blob và parent của commit thêm đều đối chứng được | ĐO ĐƯỢC+KHỚP | Có trong Git; không gọi HTTP |
| R1/R2/RH/R487:`anchor` | Blob/commit là nguồn đối chứng trong Git | **4/4 commit neo** thuộc tổ tiên exact head; không có câu hạ băm, đếm finding hoặc quan hệ Git này thành attestation | ĐO ĐƯỢC+KHỚP | Không thấy hạ quá tay ở nhóm đã kiểm |
| R1/R2/RH:các scalar ngoài văn xuôi | Giữ identity/runtime; chỉ sửa số ref R2 | **3/3 receipt** giữ các scalar số/bool cũ, ngoại trừ đúng `R2:nang_luc_do_cua_goi.so_ref` từ **312 ref nhánh** thành **313 ref nhánh** | ĐO ĐƯỢC+KHỚP | Có; source runtime vẫn chưa xác thực |
| R1/R2/RH/R487:thời lượng | **1.226,45 giây**; **928,758 giây**; **1.280,648 giây**; **1.526,889 giây** | Hiệu timestamp lần lượt **1.226,449952 giây**, **928,758254 giây**, **1.280,647831 giây**, **1.526,889169 giây**; **4/4 phép tính** khớp mức làm tròn | ĐO ĐƯỢC+KHỚP | Số học, không phải đo lại lần chạy |
| R487:`evidence_url_ghi_chu`, bản gốc | Bản gốc trước vận chuyển chưa xác thực | `VERDICT-luot1.md` trong gói và V487 hiện tại là **2/2 tệp** cùng hash/byte. Điều này không chứng minh lịch sử trước vận chuyển của scratchpad gốc | KHÔNG ĐO ĐƯỢC | Hạ nguồn lịch sử này hợp lý; không hạ băm blob |
| R1:`comment_ban_chieu_ghi_chu`, slug nguồn | Slug thuộc hậu kiểm PR #486 | V1 có **8/8 tiêu đề finding** được kiểm, không chứa slug; VH có **19/19 tiêu đề finding** được kiểm, chứa đúng slug ở VH:180; **2/2 đối chiếu nguồn** khớp | ĐO ĐƯỢC+KHỚP | Đã sửa ghép sai lượt |
| R2:`comment_ban_chieu`, lịch sử khóa | Bổ sung sau review, không bác finding | **0 khóa** ở SHA trước; **1 khóa** ở SHA hiện tại; commit thêm khóa đúng `5c05778`; `special.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Vá thiếu khóa thật |
| R2:`comment_ban_chieu_ghi_chu`, sự kiện đăng | Comment đăng sau khi biên nhận được viết; bản rút gọn | Không có response/readback GitHub; Git chỉ định ngày thêm khóa trong hồ sơ, không định thời điểm đăng comment | KHÔNG ĐO ĐƯỢC | Không dùng lịch sử khóa xác thực lịch sử GitHub |
| INDEX:270 đối chiếu R2:138 | Receipt chưa có URL | R2 đã có khóa URL; INDEX vẫn phủ định | ĐO ĐƯỢC+LỆCH | P3 mới do cập nhật không đồng bộ |
| R2:`doi_chieu_luot_1`, comment mở đầu | Phân loại slug cũ, không chứng nhận toàn bộ bản vá | **8/8 slug** khớp V2; finding tự kiểm mới được nhắc riêng | ĐO ĐƯỢC+KHỚP | P3 suy rộng từ nhãn đã đóng |
| R2:`dinh_chinh_loi_tu_kiem` | Đính chính công khai trong commit `60d62aa`; báo cáo ngoài Git chưa đối chứng | Thông điệp commit còn lời rút kết luận về số commit sau duyệt; receipt giữ đúng phạm vi | ĐO ĐƯỢC+KHỚP | Có trong Git |
| R2/INDEX: số ref lượt cũ | **313 ref nhánh** theo V2 | Khớp câu V2:36; không cập nhật hàng loạt R1/RH theo gói mới | ĐO ĐƯỢC+KHỚP | Công sửa được giữ |
| R487:`nang_luc_do_cua_goi.so_ref`, `manifest`; INDEX:269 | **312 ref nhánh** | V487:32–33 ghi prompt sai, thực đo **313 ref nhánh** | ĐO ĐƯỢC+LỆCH | Cùng lỗi lặp ở receipt mới |
| INDEX:272: phạm vi tiền kiểm | Chỉ thị tiền kiểm của lượt cụ thể | Không còn “đầu tiên của kho”; giữ phạm vi nguồn V1/R1 | ĐO ĐƯỢC+KHỚP | Câu cũ đã sửa |
| R487:5–7; INDEX:269 | Khác mọi lượt trước; chưa ai kiểm số liệu | VH đã review hồ sơ/receipt/INDEX của điều phối; V2 đã review lời tự kiểm; không có inventory cùng phạm vi “mọi/chưa ai” | KHAI RỘNG HƠN PHÉP ĐO | P3 khái quát lại phát sinh |
| INDEX:toàn bảng | Giữ hàng cũ, nhập hàng verdict mới | **90 hàng verdict** hiện tại; **89/89 hàng cũ** còn đúng thứ tự; **86/86 hàng không thuộc ba hàng sửa** nguyên byte; **3/3 hàng R2,RH,R1** vẫn đúng thứ tự; thêm **1 hàng R487** ở đầu; **0 hàng trùng**, **0 hàng mất**; `index.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có về cấu trúc, không phải toàn bộ lời văn |
| INDEX:269–272:cột byte | Byte của các verdict | **4/4 cột byte** đúng: **43.342 byte**, **36.408 byte**, **91.292 byte**, **58.402 byte** | ĐO ĐƯỢC+KHỚP | Không có lỗi byte verdict |
| R487:`duong_manh_hon_da_can_nhac_va_khong_lam` | Tránh lưu response vì usage/cost; giữ attestation | Tránh công bố response đầy đủ là hợp lý; không có response để kiểm thành phần thật; phép chiếu chọn trường có thể bỏ usage/cost | KHAI RỘNG HƠN PHÉP ĐO | Lý do chưa loại được mọi phương án lưu bằng chứng |
| R487:lý do dữ liệu tài khoản đối chiếu L:36–38 | Việc đưa dữ liệu sử dụng vào kho thuộc chủ kho | L đã thuật lại **2 giá trị output token**, **2 giá trị chi phí**, **2 cặp used/capacity**; lý do mới không phân biệt dữ liệu đã có và dữ liệu sẽ công bố thêm | ĐO ĐƯỢC+KHỚP | Đo được sự hiện diện, không xác thực các giá trị API |
| Bảng đầy đủ:các hàng dữ liệu | Không cắt **392 lá** từ **6 tệp YAML** | **392/392 hàng** khớp toàn giá trị sau safe-load và escape xuống dòng; **0 lá** cắt; `tables.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Công sửa mất đuôi là thật |
| Prompt:chênh hai TSV | **35.694 ký tự** | Đúng chênh toàn tệp, gồm header/cột đường dẫn; phần giá trị mất ở bảng cũ chỉ **15.439 ký tự** trên **73 lá**; chênh kích thước file là **39.039 byte** | ĐO ĐƯỢC+KHỚP | Không gọi chênh toàn TSV là số nghĩa được phục hồi |
| Bảng chú thích | **67 dòng** từ **6 tệp**, không cắt | **67/67 dòng** nguyên dòng khớp vị trí và nội dung; gồm **13 dòng R1**, **9 dòng R2**, **15 dòng RH**, **10 dòng R487**, **1 dòng DEBT**, **19 dòng LAND** | ĐO ĐƯỢC+KHỚP | Chỉ comment nguyên dòng |
| Prompt/bảng đầy đủ:phạm vi lớp mù còn lại | Tự khai còn lớp mù mệnh đề trong lá | Comment inline DEBT:4 vắng; INDEX/verdict không thành đầu vào; L chỉ có token | KHAI RỘNG HƠN PHÉP ĐO | Còn lớp mù ngoài nội dung trong lá |
| Bảng token:header | **20 “khẳng định”** | **20/20 hit** tái sinh nguyên byte; chỉ trên **10 dòng nguồn**; tỷ số giả và nhãn kép epoch vẫn còn | ĐO ĐƯỢC+LỆCH | Hit không phải mệnh đề; không dùng tỷ số giả làm bằng chứng dương |
| Cổng receipt tại exact head | Kiểm cấu trúc và neo | **90/90 biên nhận** được phân loại: **37 biên nhận ĐẠT**, **11 biên nhận miễn trừ**, **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp KHÔNG ĐO ĐƯỢC** | ĐO ĐƯỢC+KHỚP | Không chứng nhận prose/API |
| Cổng `doc-claims-check --strict` | Phép kiểm ngắn được phép | `ok: true`, quét **106 tệp**, **367 advisory**, **0 cờ cứng** | ĐO ĐƯỢC+KHỚP | Roots mặc định không phủ `ops/reviews`/`ops/land` |
| `doctrine-scan`, `adr-song` | Kiểm doctrine và đăng ký ADR | Quét **7 tệp**, **0 chỗ chép**; **46/46 mục ADR** khớp; công cụ công khai ngoại lệ trạng thái ADR-0016 | ĐO ĐƯỢC+KHỚP | Chỉ đúng phạm vi cổng |
| `.github/workflows/ci.yml` | Không tăng timeout, không đổi workflow | **2/2 phép so blob** với base và SHA lượt trước khớp byte | ĐO ĐƯỢC+KHỚP | Không cần chạy CI cho lời khai này |

## KHẲNG ĐỊNH CẢ BỐN BẢNG BỎ SÓT

“Bỏ sót” ở đây đòi thiếu nội dung hoặc thiếu nguồn cụ thể để xét khẳng định; không gọi lá dài đã được bảng đầy đủ giữ lại là bị cắt. Đặc biệt, lời khái quát ở comment R487:5–7 đã vào bảng chú thích: bảng có giữ một câu không có nghĩa câu đó đúng. Tôi không tính nó là câu cả bốn bảng bỏ sót.

| vị trí | khẳng định | vì sao cả bốn trượt | hệ quả |
|---|---|---|---|
| DEBT:4 | `pr_number` là số hiệu PR, không phải số lượng PR | Safe-load bỏ comment inline; bảng chú thích chỉ nhận dòng bắt đầu `#`; bảng token chỉ đọc L | Mất đơn vị/loại định danh mà chính chủ kho yêu cầu; thuộc P3 chú thích |
| INDEX:270 | “Receipt chưa có URL comment bản chiếu” | INDEX không là đầu vào của bảng nào; khóa URL được giữ ở bảng YAML nhưng không có câu INDEX đối chiếu | Lệch mới giữa mục lục và receipt lọt qua cả bốn bảng; thuộc P3 neo comment |
| L:32 | Model cấu hình và model đã phục vụ đều là `claude-fable-5-1` | L không qua safe-load/comment extractor; token regex không bắt model hoặc quan hệ cấu hình/phục vụ | Mệnh đề về danh tính thực chưa đo được, vẫn cần giữ nhãn nguồn; thuộc P3 độ phủ |
| L:36 | Các phiên sinh **66.709 token** và **26.680 token** | Đơn vị token ngoài danh sách regex; không có hàng token cho dòng nguồn này; các bảng còn lại không đọc L | Mất trọn giá trị API, không chỉ chưa tách mệnh đề; thuộc P3 độ phủ |
| L:37 | Chi phí **8,898 USD** và **5,127 USD** | Regex không bắt đơn vị USD; L ngoài các bảng YAML/comment | Dữ liệu tài khoản đã có trong hồ sơ nhưng không hiện trong inventory, ảnh hưởng đánh giá lý do từ chối lưu nguồn; thuộc P3 độ phủ và lý do lưu nguồn |
| L:56 | Số học không xác nhận hạn mức đã reset hoặc tài khoản khả dụng | Không có token định lượng trong câu; L ngoài bảng cấu trúc/comment | Giới hạn đúng vừa vá vẫn không được giữ trong bảng; thuộc P3 độ phủ |
| L:86–87 | Hồ sơ không cấp quyền mở lại phiên hoặc gửi thông điệp | Mệnh đề không số, không thuộc đầu vào YAML/comment | Bỏ giới hạn hành động đúng; thuộc P3 độ phủ |

Các trường hợp trên có **7/7 ca** đối chứng nguồn tồn tại và vắng trong từng bảng, `omissions.json`, `ok: true`. Chúng được gộp theo nguyên nhân trong finding, không nhân severity theo từng câu. Ngoài ra, quan hệ R487:106 ↔ V487:32–33 bị thiếu phía nguồn V487: bảng có scalar **312 ref nhánh**, nhưng không trích verdict được dẫn để phát hiện nó trái số đã đính chính. Đây là lớp thiếu đầu vào và đối chiếu liên tệp, không chỉ là chưa tách văn xuôi trong một lá.

### bien-nhan-moi-lai-nang-attestation-thanh-do-doc-lap  [P3]  Bổ sung neo trong receipt nhưng mục lục vẫn phủ định sự có mặt của khóa

TỆP/DÒNG: INDEX:270; R2:138–156; khác biệt từ `bcbca7b` đến `5c05778`.

VẤN ĐỀ: Bổ sung `comment_ban_chieu` là sửa thật, không phải bác hoặc xóa dấu finding cũ. `yaml.safe_load` trên blob trước cho **0 khóa**, blob hiện tại cho **1 khóa**; `git log -G '^comment_ban_chieu:'` định commit bổ sung. Nhưng INDEX vẫn nói “Receipt chưa có URL comment bản chiếu”. Đọc câu này theo hiện trạng receipt là sai ngay trong gói. Không cần mạng để bác câu về sự có mặt của khóa. Việc comment thật được đăng lúc nào, có tồn tại hay đúng nội dung không vẫn KHÔNG ĐO ĐƯỢC; không dùng commit thêm khóa hợp thức hóa các sự kiện ấy.

ĐÃ THỬ VÁ: Bản gợi ý chỉ thay câu INDEX bằng việc receipt đã bổ sung địa chỉ sau review, giữ toàn bộ sự kiện GitHub ở mức attestation. Phần P2 cũ về nguồn đã đóng; mức hiện tại hạ xuống P3 vì chỉ còn mâu thuẫn mục lục.

GÓI VÁ: [cay/ops/reviews/README.md](cay/ops/reviews/README.md), tệp đầy đủ. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `special.json`, `omissions.json`, `hint-validation.json` đều có `ok: true` theo phạm vi; giữ **90/90 hàng** trong gợi ý, không sửa receipt để làm nó thiếu khóa trở lại. Rủi ro: đổi câu thành comment đã được xác thực; gợi ý tránh điều đó.

ĐỘ TIN: cao về Git và văn bản; không xác minh GitHub.

### bien-nhan-luot-hai-chep-sai-so-ref  [P3]  Sửa số ref của receipt cũ rồi chép lại số sai vào receipt mới

TỆP/DÒNG: R487:106,120; INDEX:269; V487:32–33. Đối chứng công sửa R2:108–112 và V2:36.

VẤN ĐỀ: Biên nhận mới ghi **312 ref nhánh**, chính verdict nó nhận ghi prompt thiếu **1 ref nhánh** và đã đo **313 ref nhánh**. INDEX cũng lặp số sai. Đây là lỗi nội bộ cùng lượt, không phải tranh luận giữa các snapshot. Công sửa R2 là đúng và không bị rút; lỗi chuyển sang hiện vật mới.

ĐÃ THỬ VÁ: Sửa số và diễn giải của R487/INDEX theo V487; nêu rõ inventory cũ chưa kèm. Không sửa R1/RH theo số của lượt khác.

GÓI VÁ: [cay/ops/reviews/pr487-review-1-codex-verdict.receipt.yaml](cay/ops/reviews/pr487-review-1-codex-verdict.receipt.yaml) và INDEX trong `cay/`, tệp đầy đủ. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đếm và đọc đúng **2/2 verdict nguồn** V2/V487. `hint-validation.json`: **8/8 trường identity verdict** giữ nguyên; YAML parse được; `ok: true`. Cách khóa: lấy số từ verdict của đúng receipt, không từ prompt điều phối. Không gọi snapshot hiện tại là bằng chứng về lịch sử cũ.

ĐỘ TIN: cao về lệch giữa các hiện vật trong Git.

### readme-tuyen-tien-kiem-dau-tien-qua-pham-vi-nguon  [P3]  Bỏ tính đầu tiên ở hàng cũ nhưng thêm lại tính duy nhất ở hàng mới

TỆP/DÒNG: R487:5–7; INDEX:269; so INDEX:272, VH:219–284 và V2:144–156.

VẤN ĐỀ: Câu tiền kiểm đầu tiên đã thu hẹp đúng. Nhưng “khác mọi lượt trước” lại khái quát lịch sử từ một phạm vi review hiện tại; VH đã kiểm metadata/byte/độ phủ/mục lục của hồ sơ điều phối, V2 đã bắt chính lời tự kiểm của điều phối. Việc đây là tập tệp hoặc lượt mới không làm loại đối tượng ấy thành duy nhất. Câu “không ai kiểm những con số ấy” cũng không có nguồn đủ để biết mọi lần kiểm trước đó. Không quy động cơ cho người viết; lỗi nằm ở phạm vi phát biểu.

ĐÃ THỬ VÁ: Giữ mô tả cụ thể đối tượng lượt này, bỏ các lượng từ “mọi”, “không ai”; không sửa lời verdict lịch sử.

GÓI VÁ: R487 và INDEX trong `cay/`, tệp đầy đủ. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đọc **2/2 nguồn phản chứng** VH/V2; xác nhận bản gợi ý giữ identity và cấu trúc bảng bằng `hint-validation.json`, `ok: true`. Không cần kiểm toàn lịch sử để bác một khái quát đã có phản chứng; riêng phát biểu “chưa ai” chỉ kết luận chưa được chứng minh.

ĐỘ TIN: cao về phạm vi nguồn; không điều tra hành vi người dùng ngoài Git.

### bang-khang-dinh-token-khong-phai-menh-de  [P3]  Đã giữ đủ giá trị nhưng token vẫn bị trình bày thành khẳng định

TỆP/DÒNG: `trich_khang_dinh.py:25–41`; `trich_khang_dinh_v2.py:43–44`; `BANG-TOKEN.tsv:1–11`; header bảng đầy đủ.

VẤN ĐỀ: Không còn lỗi cắt đuôi trong bảng mới: **392/392 lá** khớp giá trị safe-load. Bảng cũ cố ý giữ để so thì không phải regression. Nhưng bảng token vẫn đếm **20 hit** trên **10 dòng nguồn**, trong đó dòng L:38 bị đọc thành `392/1`, `175/1`, mặc dù số có dấu cách phân nhóm là **233.392 token / 1.000.000 token** và **212.175 token / 1.000.000 token**. Epoch trên **2 dòng nguồn** bị gắn đồng thời nhãn SHA và ID. Header gọi đó là “khẳng định” vẫn sai đơn vị. Tự khai không hiểu ngữ nghĩa không sửa được các giá trị giả này.

ĐÃ THỬ VÁ: Giữ dữ liệu đầy đủ có kiểu/path trong `leaves-full.json`; báo riêng hit và dòng nguồn. Sửa tiếp nên gọi bảng là inventory hit, không dùng hit làm tỷ số hoặc mệnh đề đã xác thực. Bảng đầy đủ cũng là giá trị đã qua safe-load, không phải byte YAML nguyên văn. Hai script trong gói tái sinh được bảng cắt/token; chưa kèm lệnh gốc sinh bảng đầy đủ/chú thích, dù reviewer đã tái dựng được các hàng bằng script độc lập.

GÓI VÁ: Không bắt buộc tệp sản phẩm cho P3; phép tái dựng và dữ liệu nằm ở `do-review/audit.py`, `tables.json`, `leaves-full.json`. Không đề nghị bỏ bảng đầy đủ hoặc hồi quy về bảng cắt.

ĐÃ THỬ NGHIỆM: **392/392 lá**, **20/20 hit** khớp nguồn sinh tương ứng; `tables.json`, `ok: true`. Chênh **35.694 ký tự** đúng khi so toàn TSV, không phải số ký tự giá trị cứu được; phép so đồng dạng giá trị cho **15.439 ký tự** trên **73 lá**. Không tạo finding giả cho con số chênh toàn tệp đúng này.

ĐỘ TIN: cao về byte, độ dài và các phản chứng token.

### bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon  [P3]  Đã lấy comment nguyên dòng nhưng vẫn thiếu comment cuối dòng và nguồn Markdown

TỆP/DÒNG: `BANG-CHU-THICH.tsv`; DEBT:4; INDEX:269–272; L:32,36–38,56,86–87; V487:32–33.

VẤN ĐỀ: Bảng chú thích mới không phải parser mọi vị trí comment YAML. Nó giữ đúng **67 dòng** bắt đầu bằng `#`, nhưng bỏ chú thích inline xác định `pr_number` là số hiệu. INDEX không được đọc bởi bảng nào, nên câu sai về URL sau khi bổ sung khóa không có trong inventory. Các mệnh đề API và giới hạn mới trong L vẫn ngoài bảng đầy đủ; regex mất token/USD/model và các câu không số. Thiếu đầu vào là lớp mù khác với chưa tách mệnh đề bên trong lá. Lượt trước đã nêu cả inline comment lẫn INDEX, nên chưa thể đóng slug này.

ĐÃ THỬ VÁ: Bổ sung inventory các mệnh đề bị bỏ ở bảng trên và `omissions.json`. Hướng công cụ: công bố tập tệp đầu vào, lấy INDEX và các verdict nguồn liên quan; giữ cả comment inline đúng cú pháp, phân biệt dấu `#` trong scalar; lưu dòng nguồn Markdown đầy đủ trước khi trích token. Không chỉ thêm vài đơn vị vào regex rồi tuyên phủ ngữ nghĩa.

GÓI VÁ: Không bắt buộc cho P3; dữ liệu chứng cứ ở `do-review/`. Gợi ý INDEX sửa riêng lỗi nội dung, không tự nhận sửa toàn parser.

ĐÃ THỬ NGHIỆM: **67/67 dòng** comment được giữ đúng; **7/7 ca bỏ sót** đã đối chiếu từng bảng và dòng gốc, `ok: true`. Cách khóa tiếp theo phải có comment đầu/giữa/cuối dòng và kiểm danh sách tệp đọc; tránh gọi mọi dấu `#` là comment YAML.

ĐỘ TIN: cao; không dựa vào giả định về API.

### ly-do-du-lieu-tai-khoan-bo-qua-ban-trich-chon-truong  [P3]  Tránh response thô không buộc phải bỏ mọi bằng chứng có thể tái kiểm

TỆP/DÒNG: R487:63–67; L:36–38; R1:40–41.

VẤN ĐỀ: Lý do đứng vững để không tự công bố toàn response thô; tôi không yêu cầu công bố nó. Nhưng chưa đứng vững như lý do loại luôn phương án bằng chứng mạnh hơn. Có thể chiếu theo danh sách trường cho phép, giữ timestamp/trạng thái/mã loại lỗi/mốc reset cần thiết, bỏ `usage`, `cost_usd`, credential và văn xuôi tự do ở mọi cấp. L đã thuật lại chính số token và chi phí, nên hồ sơ còn cần phân biệt dữ liệu hiện có với dữ liệu thêm. Không có response thật trong gói để xác minh nó chứa trường nào hoặc điều phối đã đọc gì; không đủ bằng chứng gọi đây là “cái cớ” theo nghĩa cố ý.

ĐÃ THỬ VÁ: Dựng phép chiếu từ fixture tổng hợp, cho trường tài khoản/credential cả ở gốc và trong cấu trúc lồng. Giữ **8/8 trường cần kiểm** trong ví dụ, **0 marker dữ liệu riêng** và **0 khóa cấm** ở đầu ra, `projection-demo.json`, `ok: true`. Đây chứng minh có đường kỹ thuật, không chứng nhận nguồn API. Khi có quyền và nguồn thực: lưu bản trích cùng phiên bản client, lệnh/phép biến đổi, thời điểm đọc, phạm vi loại bỏ và SHA-256 của bản trích. Người đọc tái kiểm được phần đã giữ; tính xác thực API và phần bị loại vẫn phải ghi giới hạn. Băm bản trích không tự chứng minh nguồn gốc; không cần đưa băm response bí mật vào kho để thực hiện phép kiểm này.

GÓI VÁ: R487 trong `cay/` sửa lý do thành lựa chọn chưa thực hiện; mã minh họa tại `do-review/supplement.py`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Không có response thật hoặc dữ liệu tài khoản mới được ghi vào gói gợi ý.

ĐÃ THỬ NGHIỆM: Fixture được chạy thật; kiểm marker và khóa lồng thay vì chỉ xóa khóa gốc. Đây là phép chiếu với schema ví dụ, chưa phải bộ lọc dùng trực tiếp cho API chưa được xem. Bản trích do cùng điều phối tạo vẫn không phải phép đo độc lập của reviewer về sự kiện máy chủ. Giữ attestation ở hồ sơ hiện tại là hợp lệ, nên finding này không tái mở P2 lease.

ĐỘ TIN: cao về khả năng chiếu dữ liệu và nội dung đã có trong kho; không xác minh response hoặc động cơ của điều phối.

## GÓI GỢI Ý VÀ GIỚI HẠN

Có **2 tệp đầy đủ** dưới `cay/`, tự nguyện cho các finding P3: INDEX và R487. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Bản gợi ý giữ **8/8 trường identity verdict** của R487 và **90/90 hàng mục lục**, YAML parse được; không sửa verdict gốc. Chưa chạy cổng trên bản gợi ý; kiểm cổng receipt ở trên thuộc cây head được review. Mã và kết quả đều ở `do-review/`; không yêu cầu người đọc tin `rc=0` đơn độc.

Không có finding P1/P2 còn mở nên không có gói vá bắt buộc cho mức ấy. Các hiện vật nguồn được giữ nguyên. Không dùng `approve` để tuyên API, CI thực tế, author identity hoặc lịch sử comment đã được xác minh.

**KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho):** mọi truy vấn GitHub và API quản lý phiên; readback comment; thời điểm đăng comment thực; usage/cost gốc; nguyên nhân toàn bộ diễn biến phiên; khả năng phục hồi; điều kiện cấp lại lease hiện hành; bộ test dài và CI. Lý do: không mạng, thiếu response/transcript đúng lượt và không được chạy bộ kiểm dài. Không có thao tác cấp lease, gửi thông điệp, đăng Issue/PR, merge hoặc sửa kho thật. Không đổi timeout workflow. Các phép Git/số học/cổng ngắn chỉ chứng nhận phạm vi đã ghi.
