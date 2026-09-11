verdict: approve
reviewed_sha: 5b96ddc91593e9704ac3265b4e0b688059478cc8
base_da_review_luot_truoc: afddf7efe21e784fd22ed6b5aed399bc9d04a67d
luot: 2
so_lan_luot_nay_bi_chet_va_phong_lai: 0

Kết luận đã ghi ngay khi đủ căn cứ, nay bổ sung đầy đủ: **0 finding P1, 0 finding P2, 3 finding P3**. P1 của lượt trước đã vá thật; chưa thấy bản vá sinh P1 mới. Theo điều kiện chủ kho “tới hết P1”, lượt này đủ điều kiện dừng vòng sửa P1. Các P3 còn lại thuộc bảng/cách diễn giải của điều phối, không phải blocker P1 của YAML. Đây là verdict review offline, không xác nhận approval/CI/merge trên GitHub và không thực hiện merge.

Reviewer Codex/OpenAI, thực thi lệnh cục bộ qua API; không suy model/effort lịch sử từ tài khoản GitHub. Quan sát 0 lần chết/phóng lại trong lượt này. Tree được review: `30fc43ab8fd2685377a9b25ead5288acc5d17651`.

Phạm vi: `cay-kho/` chỉ đọc; hiện vật mới ở `do-review/` và verdict này. Chỉ thị trực tiếp của chủ kho cho phép review gói này, không cần cấp lease. Không mạng, không chạy bộ test dài, không gọi CI, không nâng `timeout-minutes`. Không sửa mã/bản chiếu/biên nhận trong clone.

Quy ước: `LAND` = `cay-kho/ops/land/pr477-dung-goi-review-land-evidence.yaml`; số dòng trong báo cáo là **định danh vị trí**. SHA, số hiệu PR/ADR, revision, schema, generation, số thứ tự lượt và mã thoát là **giá trị định danh/schema**, không phải phép đếm trần. Đơn vị của metadata đầu tệp: `luot` là lượt review, `so_lan_luot_nay_bi_chet_va_phong_lai` là lần. “Khớp nội dung” chỉ chứng minh nguồn nói điều ấy, không biến sự kiện được thuật lại thành sự kiện đã xác minh. Các `ok: true` chỉ có hiệu lực trong phạm vi phép kiểm ghi kèm.

## ĐỐI CHIẾU LƯỢT 1

- `land-evidence-tong-khong-chung-minh-co-che`: **ĐÃ VÁ THẬT** — LAND:151–179 bỏ “Số ĐÚNG”, “Phần này ĐỨNG VỮNG”, đổi khóa và rút kết luận chứng minh cơ chế. Tái tính tăng **1 bước tổng**, **5 bước skipped**; không suy danh tính/trạng thái từng bước. Phản ví dụ dữ liệu có cùng tổng đầu **43 bước / 1 bước skipped**, nhưng lần lượt **5 bước null** hoặc **0 bước null**, cùng tương thích tổng cuối **44 bước / 6 bước skipped** khi chưa có ràng buộc chuyển trạng thái. `phan-chung-tong.json`: `ok: true`; đây là phản ví dụ logic, không khẳng định GitHub thực hiện mọi chuyển trạng thái của mô hình. `ci-tinh.json` tái đếm **6/6 điều kiện false** trên Windows; YAML mới giữ rõ đây là phép đo tĩnh, khác số skipped API. Không còn lời nâng cặp tổng thành cơ chế đã quan sát trong khối sửa.
- `land-evidence-dem-review-khong-co-verdict`: **ĐÃ VÁ THẬT** — LAND:59–65 ghi nguồn thứ cấp/attestation; LAND:75–77 không dùng boolean để tự đóng nợ. Quét mới **157/157 blob verdict Markdown** reachable trong gói, đọc thủ công **5/5 blob nhắc PR #477**: **3 blob** của PR #478, **1 blob** của PR #480, **1 blob** của PR #486; **0 blob** là verdict gốc PR #477. Số **154 blob** là mốc gói trước, không phải số phải ép khớp gói này. Báo cáo DO-T33 và commit `37d66a6`, `75fe4c4`, `b789e73` đúng là nguồn thuật lại; không đếm chúng như verdict gốc. `verdict-search.json` ghi phạm vi tìm kiếm, không giả chứng minh mọi văn bản có tên khác đều vắng mặt.
- `land-evidence-dan-nham-adr`: **ĐÃ VÁ THẬT** — LAND:4–7 dẫn đúng nghĩa vụ ở ADR-0034 và mẫu Protocol; không suy “không có cổng” từ ADR-0045 nữa. Đọc **2/2 ADR** đối chiếu đúng đối tượng; Protocol:466–488 là mẫu land evidence, §20 ghi ADR-0034 có nhắc trong mã. `adr-song` xác nhận **46/46 mục ADR** khớp đăng ký; phép này không kiểm đúng/sai lời khai land.
- `land-evidence-bookkeeping-chua-neo-moc`: **ĐÃ VÁ THẬT** — LAND:211–216 neo riêng `2aee80a` và `0123ace`. Đọc **2/2 snapshot spec**: revision mang giá trị **6** và **8**; bảng lịch sử tương ứng **6 hàng lời gọi** và **7 hàng lời gọi**. Snapshot mới ghi checkpoint `5578460203` và bộ đếm không reset. `bon-so.json`: `ok: true`; thẩm quyền comment/lời gọi thực tế vẫn KHÔNG ĐO ĐƯỢC.
- `land-evidence-nguon-native-o-ban-khac`: **ĐÃ VÁ THẬT** — LAND:133–137 neo exact commit `b789e73274e7766ac36ff894445b82f051a47f6b`. Đọc **4/4 blob** báo cáo: `75fe4c4`, `afddf7e`, `5b96ddc` không có mục “Nền đã đo, và nền chưa đo”; `b789e73` có mục ấy. `native.json`: `ok: true`. Không dùng đoạn tự khai để xác thực runner lịch sử.
- `land-evidence-nhan-ci-exact-head`: **ĐÃ VÁ THẬT** — LAND:91 đổi thành “CI được báo cho PR có head ...”; LAND:95–96 vẫn rút chứng nhận CI exact head. **2/2 vị trí** tên/cảnh báo nhất quán; giá trị run/kết quả được giữ nguyên. Đọc workflow thấy checkout không khai `ref`; không có response để xác nhận cây thực sự được runner checkout.
- `bang-khang-dinh-token-khong-phai-menh-de`: **VÁ HỜ** — v2 sửa thật việc gọi mẫu số là lá, nhưng không đóng phần mất nghĩa/mức chắc chắn. V1 vẫn ghi **112 “khẳng định”** trong header dù thực tế là **112 hit** trên **60 dòng nguồn**, có **11 chuỗi số** bị bắt đồng thời như SHA/ID và **4 hit** “478 lượt”. V2 giữ **79/79 lá** nhưng cắt **18 lá**, mất **6.030 ký tự**, gồm câu LAND:77 về boolean chỉ là lời khai và LAND:163–166 về cơ chế chưa được chứng minh. `bang.json`: `ok: true` cho tái tạo bảng, không phải chứng nhận độ phủ mệnh đề. Giữ slug cũ, không đếm lại từng câu bị cắt thành finding độc lập.
- `bang-khang-dinh-bo-lop-gia-tri-co-cau-truc`: **ĐÃ VÁ THẬT** — đối với lớp giá trị YAML nêu trong finding: v2 có **14 lá số nguyên**, **1 lá boolean**, **64 lá chuỗi**, tổng **79/79 lá** khớp cây đọc độc lập. Map P1 theo lượt có đủ **6/6 phần tử**; các trường generation, số lượt, p1/p2/p3 và `khop_head_da_merge` đều có hàng. Chuỗi `đã chạy=121, bỏ qua=0` cũng còn nguyên trong lá kết quả. Phần tuple/predicate nằm sâu trong prose vẫn chưa được tách và có thể bị cắt: phần dư ấy được giữ ở slug token ngay trên, không dùng “đủ lá” để khai đã phủ mọi mệnh đề.

**7/8 slug** đóng ở phạm vi lỗi tương ứng; **1/8 slug** còn một phần. Đây là số slug, không phải số severity hay số mệnh đề. Không có slug nào được gắn nhãn “VÁ SINH LỖI MỚI” chỉ vì công cụ còn thiếu độ phủ.

## BẢNG ĐO

Lệnh chính: `python3 -B do-review/audit.py`. Bảng này được đọc/đối chiếu thủ công từ toàn văn LAND; không lấy TSV làm danh sách giới hạn. Giá trị đầy đủ của **79/79 lá**, kèm vị trí nguồn, ở [la-day-du.json](do-review/la-day-du.json); **17/17 dòng chú thích** ở [chu-thich.json](do-review/chu-thich.json). Hai hiện vật này bổ sung văn bản, chưa tự tách hay xác thực ngữ nghĩa.

| khẳng định (key path hoặc dòng) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| `reviewed_sha`, tree | HEAD đã giao | **1/1 OID HEAD** khớp; tree `30fc43ab8fd2685377a9b25ead5288acc5d17651` | ĐO ĐƯỢC | Có |
| Diff từ lượt trước | **1 tệp**, thêm **69 dòng**, bớt **29 dòng** | Diff Git và numstat khớp **2/2 hiện vật** đã giao; `git.json` có `ok: true` | ĐO ĐƯỢC | Có |
| Gói: refs | Prompt nói **312 ref nhánh**; EVIDENCE nói **313 ref nhánh** | Clone, mirror, TSV nguồn có **313/313 ref nhánh** khớp từng cặp tên/OID; `refs.json` có `ok: true` | ĐO ĐƯỢC | Khớp EVIDENCE; prompt lệch **1 ref nhánh** |
| Gói: manifest | Các băm tệp trong ARTIFACTS | **3.035/3.035 tệp** khớp SHA-256; `manifest.json` có `ok: true` | ĐO ĐƯỢC | Có; không xác thực máy chủ |
| `git rev-list --count 14dab5e..75fe4c4` | **5 commit** | **5/5 commit**: `3d2ac9b`, `a6a5222`, `4d4137f`, `37d66a6`, `75fe4c4` | ĐO ĐƯỢC | Có |
| `585c7d5^2` | `75fe4c4` | **1/1 OID cha thứ hai** bằng `75fe4c43c47c9e2a0495f7de46942c9e26320a92` | ĐO ĐƯỢC | Có |
| `0123ace:ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` | `revision: 8` | YAML trong khối spec mang đúng giá trị revision ấy; `bon-so.json` có `ok: true` | ĐO ĐƯỢC | Có |
| “cột lời gọi lớn nhất trong bảng spec” | **7 lời gọi** | **7/7 hàng** trong bảng lịch sử, tính cả lượt `4a` chết; hàng cuối ghi “lời gọi 7” ở cột model/effort | ĐO ĐƯỢC | Có về đại lượng; không có cột riêng tên “lời gọi” |
| Phân biệt lượt/lời gọi/spec kế tiếp | Bảng đến lời gọi thứ **7** | Cột `lượt` kết thúc ở lượt thứ **6**; lời gọi thứ **8** được nói là tương lai ngoài bảng, không được tính là đã gọi | ĐO ĐƯỢC | Có |
| Commit `5b96ddc`, lời tự kiểm | Có **5 commit** nên bản gốc “bốn commit sau khi được duyệt” SAI | Chỉ chứng minh khoảng Git có **5 commit**. Không có mốc push/approval để bác số **4 commit sau duyệt**; YAML:27–30 đã không suy điều này | KHAI RỘNG HƠN PHÉP ĐO | Chưa đủ căn cứ kết luận SAI; P3 bên dưới |
| LAND:3 | Land evidence thứ ba | Lịch sử thêm YAML: `0a0c1a4` → `7ae7619` → `be47638`; **3/3 mốc thêm** đúng thứ tự. `pr478-land-evidence.yaml` được thêm sau, không đổi thứ tự lịch sử | ĐO ĐƯỢC | Có về thứ tự các land evidence YAML, không phải tổng tệp thư mục hiện tại |
| LAND:4–7 | Căn cứ ADR/Protocol | **2/2 ADR** và đoạn mẫu đúng đối tượng; không suy “có nhắc” thành cưỡng chế | ĐO ĐƯỢC | Có |
| LAND:8–11 | API/phiên/CI/review lịch sử là attestation, có ngoại lệ cho nội dung Git | Thân đã ghi riêng nguồn thứ cấp, phép số học, snapshot spec và Git parent; không thấy phép đo Git bị hạ hết thành lời khai | PHẠM VI NGUỒN | Nhất quán khi đọc toàn tệp |
| `schema_version`, `mission_id`, `generation`, `input_packet_generations` | Các giá trị schema/định danh trong YAML | Safe-load đọc được đúng giá trị; danh sách input có **1/1 phần tử**. Không có Packet gốc để xác nhận generation thực | NỘI DUNG / KHÔNG ĐO ĐƯỢC | Có về giá trị; chưa xác minh authority |
| `provider`, `role`, `recorded_by`; `cross_review.*provider/model/effort` | Danh tính/vai/nền thực thi lịch sử | Có trong YAML/commit thuật lại; thiếu runner metadata độc lập | KHÔNG ĐO ĐƯỢC | Không suy runtime từ tên tài khoản |
| `authorized_head_sha`, `authorization_ghi_chu`:25–26 | APPROVED, khác danh tính, đúng head, mốc duyệt | Git xác nhận OID head có trong merge; review API, người duyệt và thời điểm KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC | Không bác sự kiện; giữ nhãn attestation toàn tệp |
| LAND:27–30 | DISMISSED sau head đổi, lỗi lặp lần thứ ba | Git đếm được khoảng commit; dismiss, push, số lần vận hành không có timeline nguồn | KHÔNG ĐO ĐƯỢC | Chưa kết luận lịch sử |
| `merge_commit`, `merge_method` | Merge commit `585c7d5`, phương pháp merge | Git object có **2/2 cha**; hỗ trợ topology merge, không xác nhận đối số API | ĐO ĐƯỢC / GIỚI HẠN API | Khớp topology |
| `merged_at`, `land_operator_neo`, LAND:41–49 | Mốc merge, merged_by, PAT, phiên gọi API, chỉ thị chủ kho, classifier | Không có response/log thao tác gốc được dẫn; chuỗi trong Git chỉ là bản thuật lại | KHÔNG ĐO ĐƯỢC | Chưa xác minh |
| `cross_review.so_luot`, `p1_theo_luot` | **6 lượt review**; P1 mở theo lượt lần lượt **1, 1, 1, 0, 0, 0 finding P1** | Đọc được **6/6 phần tử** map; nguồn thứ cấp hỗ trợ lời thuật. **0 verdict gốc PR #477** trong inventory đã tra | KHÔNG ĐO ĐƯỢC | Không tái đếm trực tiếp được finding |
| `cross_review.luot_cuoi` | Lượt thứ **6**, approve, **0 finding P1**, **0 finding P2**, **2 finding P3**, reviewed SHA `75fe4c4` | Commit `b789e73` ghi đúng lời thuật; không phải verdict gốc | KHÔNG ĐO ĐƯỢC | Khớp nguồn thứ cấp, không phải xác nhận độc lập |
| `khop_head_da_merge`, `ghi_chu_head` | Boolean true là lời khai, chưa đóng nợ độc lập | **1/1 OID head** bằng cha merge; thiếu vế verdict gốc. Phần giới hạn tồn tại đầy đủ trong nguồn | ĐO ĐƯỢC / GIỚI HẠN | Có; TSV v2 cắt phần giới hạn cuối |
| `chuoi_loi_dang_ghi_lai` | **6 mục** bản vá sinh lỗi; không phải tái hiện độc lập | Đếm **6/6 mục** theo dấu phân cách; mục rm nêu nhiều hậu quả. Không đổi thành số sự kiện độc lập | ĐO ĐƯỢC | Có về số mục |
| `chuoi_loi_dang_ghi_lai`:82 | Manifest tăng; lần chốt muộn phá manifest | Các số lịch sử chỉ được thuật lại trong commit; hiệu các tổng khai là **12 tệp** mỗi lần | SỐ HỌC / KHÔNG ĐO ĐƯỢC | Hiệu đúng có điều kiện, chưa xác minh gói lịch sử |
| `pre_merge_checks[0]`, `post_merge_checks[2]` | **121/121 ca đạt**, chạy **121 ca**, bỏ qua **0 ca** | Log t33 có trong cây neo `b416830`/`f77f198`, không phải head/merge đang khai | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): không chạy bộ lease dài |
| `pre_merge_checks[1]`, `post_merge_checks[4]` | Shellcheck lịch sử chỉ ghi `rc=0` | Shellcheck mới trả danh sách **0 chẩn đoán**, wrapper có `ok: true`; **4/4 OID blob script** tại head/merge/hai lượt review giống nhau | ĐO MỚI / GIỚI HẠN LỊCH SỬ | Mã sạch ở phép đo mới; không xác thực rc lịch sử |
| `pre_merge_checks[2]` | Run PR success, **44 bước**, **0 bước hỏng**, **3 bước skipped** | Không response run/job; không có cách suy các số API từ YAML | KHÔNG ĐO ĐƯỢC | Chưa xác minh |
| `pre_merge_checks[2].ten/canh_bao_doc_ket_qua` | Không phải chứng nhận CI exact head/Windows | Nhãn đã thu hẹp; workflow matrix phụ thuộc event/ref/nhãn, checkout không khai ref | ĐO ĐƯỢC CẤU HÌNH | Có về giới hạn bằng chứng; không xác nhận job thực |
| `post_merge_checks[0:1]` | Head vào master, không còn commit ngoài master | Tại mốc merge cố định: **0 commit** ngoài `585c7d5`; cha thứ hai đúng head; `git.json` có `ok: true` | ĐO ĐƯỢC | Có về quan hệ Git; ref master lúc thao tác KHÔNG ĐO ĐƯỢC |
| `post_merge_checks[3]` | **28 biên nhận đạt v2**, **11 biên nhận legacy**, **42 biên nhận nợ**, tổng **81 biên nhận** | Phép cộng ra **81 biên nhận**, `so-hoc.json` có `ok: true`. Chưa chạy validator đầy đủ trong lượt này | SỐ HỌC / KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): cổng receipt ngoài danh sách lệnh được phép |
| `post_merge_checks[5]` | Dựng gói thành công, mỗi nguồn **307 ref**, manifest **3.010/3.010 mục** | Không có gói lịch sử được dẫn. Gói mới có số khác không bác được số cũ | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): builder có mạng/ghi Git |
| `post_merge_checks[6].ket_qua` | Hai nền success; mỗi job **44 bước**, **0 bước hỏng**; Ubuntu **4 bước skipped**, Windows **6 bước skipped** | Không JSON run/job/attempt/steps | KHÔNG ĐO ĐƯỢC | Chưa xác minh |
| LAND:115–117 | Ubuntu **26 phút 46 giây**, Windows **48 phút 15 giây** | Từ các mốc khai: **1.606 giây**, **2.895 giây**; phép trừ đúng có điều kiện | SỐ HỌC | Có; không xác minh mốc API |
| LAND:119–122 | Trần **60 phút**, còn khoảng **11 phút 45 giây**, chưa đóng nợ chi phí | Workflow khai đúng trần; **3.600 giây − 2.895 giây = 705 giây**. Nhãn “sát” không có ngưỡng định lượng riêng | ĐO ĐƯỢC / SỐ HỌC | Có; không thay timeout |
| `khong_do_duoc[0:1]` | Không phân biệt người/phiên từ merged_by; thiếu nguồn thô | Không thể quy người thao tác chỉ từ tên login. Mệnh đề tuyệt đối về mọi trường GitHub không kiểm được offline | KHÔNG ĐO ĐƯỢC | Không coi là nguồn xác thực hành vi API |
| `khong_do_duoc[2]` | Nguồn tự khai native ở `b789e73` | **4/4 blob** so đúng vị trí có/vắng mục; `native.json` có `ok: true` | ĐO ĐƯỢC | Có về nguồn; chưa xác thực nền chạy |
| LAND:149–156 | Phân tích tĩnh **6 điều kiện if sai**, khác số skipped thực | Trên merge `585c7d5`: **40 bước YAML**; Windows **6/6 điều kiện false**, Linux **4/4 điều kiện false** | ĐO ĐƯỢC | Có về tĩnh; không dùng mẫu số YAML thay API |
| `so_da_dinh_chinh` | Điều phối sửa số khai thành **6 bước skipped**, **44 bước tổng**, **0 bước null** | Đọc được lời khai; không response/job ID/attempt/mốc lấy mẫu/danh sách bước | KHÔNG ĐO ĐƯỢC | Đã ghi đúng giới hạn nguồn |
| `co_che_de_xuat_chua_doi_chung` | Cặp tổng chỉ cho chênh lệch, chưa chứng minh cơ chế | Phản chứng cặp tổng `ok: true`; chênh **1 bước tổng**, **5 bước skipped** | ĐO ĐƯỢC LOGIC | Có |
| `nguyen_nhan_cua_lan_doc_43_4` | Sai chép số cũng tương thích, chưa phân định nguyên nhân | Trừ **1 bước tổng**, giữ **4 bước skipped** cho đúng cặp khai; chưa có nguồn chọn giả thuyết nào | ĐO ĐƯỢC LOGIC / GIỚI HẠN API | Có về phản chứng; không phải tái hiện sự kiện |
| `bai_hoc` | Completed, không null, cùng job/attempt, đủ response | Đây là điều kiện đề xuất cho **số cuối cùng**; không phải cổng đã cài hay bằng chứng job lịch sử | QUY TẮC ĐỀ XUẤT | Hợp lý trong phạm vi số cuối cùng |
| `trang_thai_o_468` | Đổi ba khóa, có `nguyen_nhan_that_su`, bốn giả thuyết; verdict đóng finding cụ thể | **3/3 cặp tên khóa** từng khai chắc chắn đã đổi; nội dung có **4/4 giả thuyết**. Nếu đếm mọi khóa khác tập có **4 khóa bỏ / 4 khóa thêm**, vì khối `con_lai_khong_do_duoc` cũng thay bằng `nguyen_nhan_that_su` | ĐO ĐƯỢC NỘI DUNG | Có theo nhóm ba khóa được nêu, không hiểu là tổng mọi thay đổi khóa |
| LAND:190–193 | Verdict PR #478 lượt thứ **6** đóng finding P1 cụ thể, giữ attestation | Đọc blob `7e7e688704f4cecd0119f0800e5464297aeea701`: đúng lời xác nhận đó. Danh tính phiên là lời khai | ĐO ĐƯỢC NỘI DUNG | Có; không đồng nghĩa mọi nợ PR #468 hết |
| `bookkeeping[0]` | Hai nội dung P3 được sửa ở `b789e73`, PR #479 được thuật lại | Diff commit sửa **2/2 nội dung**: t33 đã chạy/đỏ và hợp đồng đầu vào/nền đo. Không có JSON để xác nhận số hiệu/trạng thái PR | ĐO ĐƯỢC NỘI DUNG / GIỚI HẠN API | Có về diff |
| `bookkeeping[1]` | Chỉ actionlint ghim; PATH tin cậy; rm vẫn xoá; không chặn symlink ở R | Đọc script thấy type-P trên PATH và **2/2 lệnh rm** nhắm thư mục con; chốt chỉ nhìn con. Blob không đổi trong **4/4 mốc Git**. Phép thử sentinel/version giả chỉ được thuật lại ở `b789e73` | ĐO TĨNH / KHÔNG ĐO ĐƯỢC LỊCH SỬ | Có về mã; không chạy builder phá dữ liệu |
| `bookkeeping[2]` | `_kiem_bia_mo` vẫn dùng any | Hàm tại LAND head có `any(...)` trong phép tìm lease thay thế; diff lượt này không sửa tệp đó | ĐO ĐƯỢC | Có; không nhận công đã vá mã lease |
| `bookkeeping[2]` | Mốc spec cũ/mới và checkpoint | **2/2 snapshot** đối chiếu được; **7/7 hàng** ở snapshot mới; comment authority chưa xác minh | ĐO ĐƯỢC NỘI DUNG | Có |
| `bookkeeping[3]` | Nợ A9 còn chờ quyết định chủ kho | Được nguồn land PR #468 ghi lại; quyết định hiện thời ngoài Git chưa xác minh | KHÔNG ĐO ĐƯỢC HIỆN THỜI | Không dùng để yêu cầu cấp lại lease/approval trong lượt này |
| Tên khóa cũ | Không để consumer trỏ tên cũ ở cây đang review | Quét **1.713/1.713 tệp tracked**, kể cả tệp ẩn: **0 tệp** chứa `co_che_da_do_duoc`; `key-cu.json` có `ok: true` | ĐO ĐƯỢC | Không tìm thấy consumer hỏng ở HEAD; lịch sử commit còn nhắc tên cũ là hợp lệ |
| BANG-CAU-TRUC.tsv | **79 lá YAML** | Tái sinh byte-identical **79/79 hàng lá**; `bang.json` có `ok: true` | ĐO ĐƯỢC | Có về lá; không phải số mệnh đề |
| BANG-TOKEN.tsv | **112 hit** theo prompt; header gọi khẳng định | Tái sinh byte-identical **112/112 hàng hit**, **60 dòng nguồn**, **11 chuỗi số** bắt đôi, **4 hit** nhầm số PR thành đại lượng | ĐO ĐƯỢC | Khớp số hit; sai tên đại lượng ở header |
| v2: mất văn bản | Docstring thừa nhận cắt **160 ký tự** mỗi giá trị | **18 lá** bị cắt, tổng **6.030 ký tự** mất; `clipped_leaves` lưu nguyên phần bị mất | ĐO ĐƯỢC | Có; tự khai không khôi phục văn bản |
| v2: chú thích | Prompt/docstring nhắc chú thích đầu tệp | Parser bỏ **17/17 dòng chú thích** ở cả đầu và giữa tệp; gồm chú thích đính chính LAND:139–144 | ĐO ĐƯỢC | Tự khai đúng nhưng chưa nói hết vị trí bị bỏ |
| Kiểm mới: actionlint, shellcheck | Phép ngắn được phép | Mỗi công cụ **0 chẩn đoán**; `checks.json` có `ok: true` cùng argv/rc. Không suy CI đã chạy | ĐO MỚI | Có trong phạm vi lint |
| Kiểm mới: adr-song | Đăng ký ADR khớp | **46/46 mục ADR** khớp; có ngoại lệ trạng thái ADR-0016 được tool nêu rõ | ĐO MỚI | Có |
| Kiểm mới: doctrine-scan | Kiểm sao chép doctrine | Quét **7 tệp**, **0 chỗ chép**, `checks.json` có `ok: true` cho phạm vi này | ĐO MỚI | Có; không kiểm nghĩa LAND |
| Kiểm mới: doc-claims-check --strict | Bộ kiểm lời khai tài liệu | `ok: true`, quét **106 tệp**, **367 advisory**. Roots mặc định không gồm `ops/land` | ĐO MỚI | Có; không dùng làm chứng nhận land evidence đúng |

Bốn phép đối chiếu điều phối yêu cầu kiểm lại **4/4 mệnh đề về giá trị đều khớp** (`bon-so.json`: `ok: true`). Hai điểm cần làm rõ không làm chúng lệch số: bảng không có cột độc lập tên “lời gọi”; và số commit trong khoảng không mang theo mốc sự kiện push/approval.

## KHẲNG ĐỊNH CẢ HAI BẢNG BỎ SÓT

“Bỏ sót” ở đây là không giữ đủ câu/quan hệ để kiểm. V1 có thể giữ token số, nhưng mất vị từ/phủ định. V2 có thể giữ key path, nhưng cắt mất đúng câu đó. Những câu còn nguyên trong v2, như “Điều phối không tìm đường vòng ở cả hai lần”, **không** được tính là cả hai cùng bỏ: v2 thật sự đã cải thiện độ phủ ở đó.

| vị trí | khẳng định | vì sao cả hai trượt | hệ quả |
|---|---|---|---|
| LAND:3 | Land evidence thứ ba | Số thứ tự bằng chữ; comment không nằm trong cây YAML | Finding P3 độ phủ chú thích; thứ tự lịch sử đo được |
| LAND:4–7 | ADR-0045 không quy định nghĩa vụ này; “có nhắc” không chứng minh kiểm đúng/sai lời khai | Mệnh đề phủ định/suy luận trong comment; v1 không giữ câu, v2 bỏ comment | Finding P3 độ phủ chú thích; mất căn cứ đã sửa P2 |
| LAND:8–11 | Các nhóm sự kiện là attestation, có ngoại lệ cho Git; Git không thay API | Không có token định lượng cần tìm; v2 bỏ toàn khối giới hạn | Finding P3 độ phủ chú thích; đọc riêng TSV có thể nâng lời khai lên phép đo |
| LAND:139–144 | Kết luận cũ đã bị lan truyền, bị chấm P1 rồi rút; tên khóa cũng là khẳng định | V1 giữ “478 lượt” sai đại lượng, không giữ quan hệ; v2 bỏ comment giữa tệp | Finding P3 độ phủ chú thích; giới hạn tự khai “đầu tệp” còn hẹp |
| LAND:77 | Boolean true chỉ là giá trị điều phối khai, không phải kết luận độc lập đóng nợ | V1 không bắt câu; v2 giữ boolean nhưng cắt câu giới hạn sau ký tự thứ **160** | Slug P3 token còn mở; chính phần giúp đóng P2 bị mất |
| LAND:95–96 | CI PR không chứng minh exact head | V1 chỉ giữ SHA; v2 cắt trước phần kết luận merge tổng hợp/exact head | Cùng P3 token; tên CI mới đã sửa thật nhưng bảng thiếu căn cứ |
| LAND:121–122 | Không nâng trần; success chưa có nghĩa vấn đề chi phí hết | V1 không giữ quan hệ phủ định; v2 cắt phần kết của cảnh báo | Cùng P3 token; mất ràng buộc của chủ kho trong bảng |
| LAND:155–156 | Thiếu danh tính/lấy mẫu/steps; phép đếm if tĩnh không chứng minh skipped thực | Token số còn, câu giới hạn mất; v2 cắt sau đoạn số tổng | Cùng P3 token; không được đọc lá có số như đủ chứng cứ |
| LAND:163–166 | Cặp tổng không chỉ ra bước đổi conclusion; cơ chế là giả thuyết cần đối chứng | V1 không trích quan hệ; v2 cắt trước toàn bộ lập luận này | Cùng P3 token; bảng không cho thấy lý do P1 đã đóng |
| LAND:170–179 | Số học tái tính được, mẫu API là lời khai; không có bản ghi thời điểm trong gói | V1 chỉ giữ một số token; v2 cắt trước phần phân biệt nguồn và phản chứng | Cùng P3 token; không được gom thành “mọi số đều không đo được” |
| LAND:183–184 | Không null không thay completed, cùng job/attempt và đầy đủ response | V1 có token số nhưng không giữ điều kiện cần/đủ; v2 cắt phần này | Cùng P3 token; mất hợp đồng đối chứng |
| LAND:190–192 | Verdict chỉ đóng finding cụ thể, không tuyên mọi nợ hết | V1 không trích câu, còn nhầm số PR thành lượt; v2 cắt trước câu đóng có giới hạn | Cùng P3 token; dễ tái tạo lời kết luận quá rộng của bản cũ |
| LAND:204–208 | PATH được tin, R không được bảo vệ bởi chốt symlink con, sentinel được thuật lại là đã mất | Token version/rc không giữ quan hệ; v2 cắt trước mô tả chốt và hậu quả | Cùng P3 token; phần mã đọc được phải tách khỏi phép chạy lịch sử chưa tái hiện |
| LAND:213–216 | Không dùng revision cũ để chặn hiện tại; checkpoint không reset bộ đếm; API authority chưa xác minh | V1 chỉ giữ commit/comment ID và số; v2 cắt gần đầu mục | Cùng P3 token; mất phần giúp đóng P2 bookkeeping |

Các hàng cùng nguyên nhân được gộp theo slug, không nhân severity theo số câu. Đây là finding **độ phủ** ngay cả khi nội dung câu đúng; không cáo buộc mọi câu bị bỏ là sai.

### bang-khang-dinh-token-khong-phai-menh-de  [P3]  Đủ lá nhưng còn mất phần quyết định nghĩa của lời khai

TỆP/DÒNG: `trich_khang_dinh.py:41`, `trich_khang_dinh_v2.py:44`; `BANG-TOKEN.tsv`, `BANG-CAU-TRUC.tsv`; ví dụ LAND:77,163–166,190–192.

VẤN ĐỀ: V2 đóng lỗi bỏ cả lớp scalar/map/bool. Nó không đóng lỗi đánh đồng đơn vị trích với mệnh đề: header v1 vẫn gọi hit là khẳng định; v2 cắt mất **6.030 ký tự** ở **18 lá**, trong đó có các phủ định/giới hạn nguồn vừa được vá. Đây không chỉ là “prose vẫn chung một lá”: nguyên văn cần để reviewer đánh giá đã không còn trong bảng. Đổi parser có cải thiện thật, nhưng chưa đủ để tuyên hai P3 cũ đều đóng.

ĐÃ THỬ VÁ: bổ sung hiện vật không cắt [la-day-du.json](do-review/la-day-du.json) và inventory mệnh đề ở bảng trên; chạy trên đúng tệp đã giao. Chưa đổi script đầu vào. Sửa công cụ tiếp theo nên giữ toàn bộ giá trị và vị trí nguồn, gọi đúng tên “hit/lá”, rồi có bước đọc thủ công mệnh đề; không tự hứa parser YAML hiểu nhân quả.

GÓI VÁ: không có tệp sửa P1/P2 vì **0 finding P1/P2**. Hiện vật bổ sung là đầu vào review, không phải mã đã chạy trên cây thật.

ĐÃ THỬ NGHIỆM: tái sinh **79/79 hàng lá**, **112/112 hàng hit** byte-identical; đo trực tiếp độ dài trước/sau từng lá. `bang.json` có `ok: true`; `la-day-du.json` giữ phần mất. Ví dụ `land_operator_neo.khac_voi_468` ngắn, còn nguyên trong v2, chứng minh không đánh đồng “không hiểu nghĩa” với “bỏ mọi prose”.

ĐỘ TIN: cao về độ phủ/ký tự bị mất; không thay độ tin của API lịch sử.

### bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon  [P3]  Cả hai bảng làm mất khối giới hạn chi phối toàn hồ sơ

TỆP/DÒNG: `trich_khang_dinh_v2.py:37`; LAND:3–11,139–144.

VẤN ĐỀ: Safe-load bỏ comment ở mọi vị trí. **17/17 dòng comment** không vào bảng cấu trúc; v1 cũng không giữ các mệnh đề về nghĩa vụ, giới hạn và rút kết luận. Docstring tự khai đúng việc mất chú thích, nhưng chỉ nhắc đầu tệp; khối đính chính giữa tệp cũng mất. Đây là mất dữ liệu được thừa nhận, vẫn chưa phải đã sửa lỗi độ phủ.

ĐÃ THỬ VÁ: xuất [chu-thich.json](do-review/chu-thich.json) giữ nguyên dòng/vị trí và đọc tay các khối trong bảng trên. Không gọi phép `startswith('#')` này là parser mọi dạng comment YAML: ở tệp đang xét, các dòng thu được đều là comment cấp ngoài; thuật toán tổng quát còn phải phân biệt ký tự `#` nằm trong chuỗi/block scalar và comment cuối dòng.

GÓI VÁ: không bắt buộc với finding P3; dữ liệu bổ sung đã có trong `do-review/`. Nếu điều phối nhập inventory này: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: đọc toàn văn **219/219 dòng nguồn**, đối chiếu các comment với YAML node/span; thu đủ **17/17 dòng comment**. Header nguồn và khối đính chính đều có trong JSON bổ sung; TSV cấu trúc không có record tương ứng. `bang.json` ghi số đo, `chu-thich.json` cho phép đối chiếu từng dòng.

ĐỘ TIN: cao; đây là P3 công cụ, không phải P1 mới của nội dung LAND.

### doi-chieu-dem-commit-khong-dinh-thoi-diem  [P3]  Đếm đúng khoảng Git nhưng kết luận quá mức về số commit sau duyệt

TỆP/DÒNG: commit message `5b96ddc91593e9704ac3265b4e0b688059478cc8`, gạch đầu dòng tự kiểm `git rev-list`; cùng lời khẳng định trong nhiệm vụ kiểm số. Đối chiếu LAND:27–30 và bản cũ `afddf7e`:21–22.

VẤN ĐỀ: **5 commit** là số đo đúng. Bản cũ nói **4 commit đẩy sau khi được duyệt**, tức đại lượng có điều kiện thời gian/sự kiện. `rev-list` không ghi lúc push, không ghi lúc approval/dismiss và không xác nhận review khi ấy còn là review trên tip. Vì vậy phép đếm không đủ chứng minh lời cũ SAI. Đây là kết luận chưa được chứng minh, không phải bằng chứng số cũ đúng. YAML mới đã xử lý đúng bằng cách nói riêng số commit Git và không suy mốc dismiss; lỗi còn trong lời tự kiểm của điều phối, không làm P1 YAML tái mở.

ĐÃ THỬ VÁ: đính chính ngay tại đây, có thể dùng nguyên văn: “Khoảng `14dab5e..75fe4c4` có **5 commit**; số commit được đẩy sau approval và nguyên nhân/mốc dismiss chưa đối chứng được từ gói.” Không viết lại commit lịch sử.

GÓI VÁ: không bắt buộc với finding P3; bản YAML hiện tại đã có cách viết đúng phạm vi. Không yêu cầu sửa thêm YAML chỉ để chữa câu trong commit message.

ĐÃ THỬ NGHIỆM: liệt kê **5/5 OID commit**, đối chiếu đúng câu gốc và câu mới; `bon-so.json` có `ok: true`. GitHub timeline **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**: cấm mạng, thiếu response/timeline trong gói.

ĐỘ TIN: cao về giới hạn suy luận; không xác nhận số commit sau approval thực tế.

## HỒI QUY, PHẦN CHƯA ĐO VÀ BÀN GIAO

**Đổi khóa:** không tìm thấy chỗ tiêu thụ tên cũ trong **1.713/1.713 tệp tracked** của HEAD. Commit lịch sử/bản cũ trên ref khác có thể nhắc tên cũ hợp lệ; không yêu cầu viết lại lịch sử để làm phép tìm kiếm rỗng.

**Hạ mức bằng chứng:** chưa thấy bản vá làm mất bằng chứng Git/số học đang đứng vững. Quan hệ cha merge, phép đếm commit, điều kiện if tĩnh, nguồn spec/native và phản chứng số học vẫn được tách rõ. Lời khai CI, verdict gốc và thao tác API không có nguồn thô để bảo vệ mức xác nhận cũ. Đặc biệt không dùng nhãn attestation để bác **6 điều kiện if false** đo tĩnh. Quy tắc `in_progress` nên đọc trong phạm vi số kết thúc job: một snapshot có raw đủ nguồn vẫn có thể đo số **tại thời điểm lấy mẫu**, nhưng không cho số cuối cùng; trong gói này cả raw snapshot ấy cũng thiếu.

**Khối giới hạn đầu tệp và phần thân:** các câu APPROVED/CI success/thao tác phiên được phạm vi attestation toàn tệp bao phủ; khối P1 mới còn giới hạn ngay trong từng mục. Các câu mạnh còn lại về API (“mỗi commit ... huỷ phê duyệt”, “không có trường nào ...”) chưa kiểm được, không được dùng như định luật GitHub đã xác minh. Chưa tìm thấy thân mới phủ định khối giới hạn hoặc tái khẳng định cơ chế là đã đo. Việc TSV làm mất khối giới hạn là lỗi biểu diễn đã ghi P3 riêng.

**Giới hạn phép đo:** không có cách xác nhận trực tiếp GitHub CI/review/merged_by/comment từ gói offline. Không tái chạy bộ lease/full-gate, không gọi builder và không chạy cổng receipt ngoài danh sách cho phép. Các công cụ ngắn đã chạy không kiểm ngữ nghĩa toàn LAND; đặc biệt doc-claims-check mặc định không quét `ops/land`. Không coi lệnh chưa chạy là pass, không coi output số học là transcript lịch sử.

Không có gói vá bắt buộc dưới `cay/`, vì không còn finding P1/P2 cần executor sửa trong lượt này. Hai inventory bổ sung và lời đính chính P3 đã nằm trong verdict/gói đo; không sửa kho thật. Trạng thái `cay-kho/` được kiểm lại ở cuối: **0 đường dẫn thay đổi**, `ok: true` trong `do-review/final.json`.
