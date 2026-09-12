verdict: changes_requested
reviewed_sha: 3873173094a3e294b069998ed21dc117d8ad659a
head_da_qua_cross_review_truoc_do: 5c05778219e293ff929e8cb1f1c31aea4120d967
luot: 1 (hậu kiểm trên head đã merge)
so_lan_luot_nay_bi_chet_va_phong_lai: 0

Kết luận chung cho các nhiệm vụ được giao: **0 finding P1 mới · 1 finding P2 · 4 finding P3**. **Finding P2 thuộc lập luận đối chứng của PR #489**, tại commit `8911ea41ed326807cf22c0dacbbff69be9342747`; tệp ấy **không nằm trong HEAD được review**. Trong phần chưa review của chính HEAD: **0 finding P1 · 0 finding P2 · 3 finding P3 nội dung**; thêm **1 finding P3 về độ phủ gói**. Không quy lỗi của tệp viết sau thành lỗi đã tồn tại trong HEAD. `changes_requested` ở đây yêu cầu sửa hồ sơ gom findings trên PR #489, không đề nghị lùi merge hoặc đổi lịch sử.

Tôi **đồng ý** rằng giữ nguyên một tập tệp không thay thế review exact head. Tuy nhiên, không dùng chính việc lượt hậu kiểm này chưa diễn ra trước đây để tạo một vòng yêu cầu review vô hạn. Lượt này đã đọc và đo phần chênh trên đúng HEAD. Những gì xảy ra trước merge vẫn là lịch sử: hậu kiểm và đính chính không hồi tố thành tiền kiểm.

Reviewer: Codex/OpenAI, thực hiện phép đo cục bộ qua công cụ shell trong phiên API, transport machine; độc lập với executor Claude theo phiên hiện tại. Không xác thực model/session runtime của các lượt cũ. Tree HEAD: `e4fa427ab1c92b90ba464d5782d6f116e185cf4f`. Quan sát **0 lần** chết/phóng lại của phiên review; lỗi cú pháp khi soạn một script gợi ý đã sửa trong cùng phiên, không phải một lần phóng lại reviewer.

Đơn vị: `luot` đếm lượt review; trường chết/phóng lại đếm lần. Số hiệu PR/ADR, SHA/hash, số dòng, phiên bản schema, mã thoát và ID là định danh/giá trị kỹ thuật, không phải phép đếm không đơn vị. Các phép đếm dưới đây nêu tệp, dòng, byte, ref nhánh, tag, biên nhận, trường, slug, finding hoặc giây. `N/N` là bằng chứng dương chỉ khi hai số bằng nhau; `ok: true` chỉ xác nhận phép kiểm được mô tả.

Tên rút gọn: **R487-1**, **R487-2** là `ops/reviews/pr487-review-{1,2}-codex-verdict.receipt.yaml`; **V487-1**, **V487-2** là verdict `.md` tương ứng; **INDEX** là `ops/reviews/README.md`. **L489** là `ops/land/pr487-land-evidence.yaml` đọc bằng `git show` tại commit đối chứng `8911ea41ed326807cf22c0dacbbff69be9342747`, bản lưu ở `do-review/pr487-land-evidence-at-8911ea4.yaml`. Mọi số dòng của L489 đều thuộc bản ấy.

Phép đo tái chạy: `python3 -B do-review/audit.py`; `python3 -B do-review/compare_gate.py`. Script thứ hai tạo **4 phép chiếu đầu vào cổng** trong `do-review/gate-inputs/`, chỉ materialize receipt tại SHA và đọc kho object nguồn; **không phải checkout để chạy các cổng khác**. Mã `bien_nhan_v2.py`, `launcher.py`, `AGENTS.md`, protocol khớp byte tại **4/4 SHA đối chứng**. Trên HEAD, tôi còn chạy trực tiếp CLI trong `cay-kho/`; kết quả trùng phép chiếu. Không có thay đổi ref, checkout, cấu hình hoặc nội dung của `cay-kho/`.

## BẢNG ĐO

| khẳng định (tệp:key path) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| Gói: HEAD, tree, detached, sạch | HEAD được chỉ định, cây sạch | OID đầy đủ đúng; detached; porcelain **0 byte**; clone không shallow; **0 ref replace**; `preflight.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Gói: diff/numstat giữa các SHA giao | **4 tệp**, thêm **354 dòng**, bớt **6 dòng** | **2/2 hiện vật** diff/numstat khớp Git; đúng **2 commit** sau head đã approve | ĐO ĐƯỢC+KHỚP | Có |
| Gói: `ARTIFACTS.sha256` | Toàn vẹn đầu vào | **3.168/3.168 tệp** khớp băm; `manifest.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có về byte, không xác thực người sinh |
| EVIDENCE/TSV/ref cục bộ | **314 ref nhánh** mỗi nguồn, không lệch | **314/314 cặp tên+OID** khớp các TSV và Git sau chuẩn hóa tiền tố `refs/heads/`; **62 tag** cục bộ; `refs.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Chỉ snapshot gói |
| EVIDENCE: nguồn máy chủ tại mốc chụp | Snapshot do điều phối khai lấy từ máy chủ | Không truy vấn máy chủ; origin URL là cấu hình, không chứng minh nguồn object | KHÔNG ĐO ĐƯỢC | Không xác minh GitHub |
| Lời khai nguyên byte: `ops/land/pr478-land-evidence.yaml` | Không đổi | **18,859 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Lời khai nguyên byte: `ops/reviews/pr486-hau-kiem-no-review.yaml` | Không đổi | **1,680 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Lời khai nguyên byte: `ops/reviews/pr478-land-review-4-codex-verdict.receipt.yaml` | Không đổi | **8,289 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Lời khai nguyên byte: `ops/reviews/pr478-land-review-4-codex-verdict.md` | Không đổi | **44,074 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Lời khai nguyên byte: `ops/reviews/pr478-land-review-5-codex-verdict.receipt.yaml` | Không đổi | **8,289 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Lời khai nguyên byte: `ops/reviews/pr478-land-review-5-codex-verdict.md` | Không đổi | **44,069 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Lời khai nguyên byte: `ops/reviews/pr478-land-review-6-codex-verdict.receipt.yaml` | Không đổi | **8,224 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| Lời khai nguyên byte: `ops/reviews/pr478-land-review-6-codex-verdict.md` | Không đổi | **35,829 byte** tại mỗi SHA; diff **0 byte**; hash hai bên bằng nhau, `diff.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| R487-2:`phan_them_la_gi`, nghĩa của “ba receipt cũ/ba verdict” | Nhóm tệp cũ giữ nguyên | Kiểm thêm nhóm `pr480-land-review-1/2`, `pr486-hau-kiem-review-1`: **6/6 tệp** receipt/verdict không đổi; biên bản lease cũng không đổi | ĐO ĐƯỢC+KHỚP | Đã kiểm cả cách hiểu nhóm cũ |
| Danh sách nguyên byte có đủ làm inventory thay đổi? | Dùng làm lý do đi tiếp với head mới | Không: INDEX, R487-1, V487-2, R487-2 là **4/4 tệp đổi** không nằm trong danh sách nguyên byte; R487-2 có mô tả phần thêm ở khối khác, nên không kết luận hồ sơ giấu toàn bộ thay đổi | KHAI RỘNG HƠN PHÉP ĐO | Tập con không thay review cả head |
| R487-2:`head_da_approve_khac_head_se_merge.vi_sao_khac`; INDEX:269 | “Không có đường tránh”, hiện vật nằm sau approve | `PROTOCOL`:488,501,517 yêu cầu review khi head đổi; lưu verdict cùng nhánh là lựa chọn vận chuyển, không phải ngoại lệ đã được cấp | KHAI RỘNG HƠN PHÉP ĐO | Đồng ý connector về thiếu review exact head |
| R487-1:`verdict_sha256`, `verdict_bytes` | `f1eb4c78c242ebc748b608e2c09696498050ff6b15c00d629e9ac0233dc08edd`; **43,342 byte** | Băm lại verdict: cùng hash; **43,342/43,342 byte**; `receipts.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| R487-1:`so_p1/so_p2/so_p3`, `verdict` | **0 finding P1 · 2 finding P2 · 6 finding P3**; `changes_requested` | Đếm tiêu đề theo mẫu `^### … [Pn]`; **4/4 trường** khớp thân verdict | ĐO ĐƯỢC+KHỚP | Có |
| R487-1:`reviewed_sha` | `bcbca7bbcea968a662b1ac69bfc9f2a329ed8ae7` | Khớp nguyên OID trong thân verdict; `ok: true` | ĐO ĐƯỢC+KHỚP | Đúng SHA của lượt cũ, không phải HEAD hậu kiểm |
| R487-1:`evidence_url`, ghi chú commit đầu tiên | Blob tại `a0b154d7c8e6491fb53825301ace2d6d4e97ac9f` | URL đúng `/blob/<40 hex>/<path>`; path khớp; `git log --diff-filter=A` ở HEAD và `--all` đều chỉ có **1/1 commit thêm** này; tệp vắng ở parent; blob đúng byte | ĐO ĐƯỢC+KHỚP | Có trong Git, không gọi HTTP |
| R487-2:`verdict_sha256`, `verdict_bytes` | `5f4a73aaa006d0e284474870b7b2275a34c53f0a9d6f915ad53b11ab66721f03`; **36,009 byte** | Băm lại verdict: cùng hash; **36,009/36,009 byte**; `receipts.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Có |
| R487-2:`so_p1/so_p2/so_p3`, `verdict` | **0 finding P1 · 0 finding P2 · 6 finding P3**; `approve` | Đếm tiêu đề theo mẫu `^### … [Pn]`; **4/4 trường** khớp thân verdict | ĐO ĐƯỢC+KHỚP | Có |
| R487-2:`reviewed_sha` | `5c05778219e293ff929e8cb1f1c31aea4120d967` | Khớp nguyên OID trong thân verdict; `ok: true` | ĐO ĐƯỢC+KHỚP | Đúng SHA của lượt cũ, không phải HEAD hậu kiểm |
| R487-2:`evidence_url`, ghi chú commit đầu tiên | Blob tại `edb288e4e95081b83661c94c88addea005d3f121` | URL đúng `/blob/<40 hex>/<path>`; path khớp; `git log --diff-filter=A` ở HEAD và `--all` đều chỉ có **1/1 commit thêm** này; tệp vắng ở parent; blob đúng byte | ĐO ĐƯỢC+KHỚP | Có trong Git, không gọi HTTP |
| V487-2 so bản gói `VERDICT-luot2-tren-5c05778.md` | Chép nguyên verdict | **36.009/36.009 byte**, cùng SHA-256; `classification.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Không có lỗi vận chuyển byte |
| R487-2:`doi_chieu_luot_1` | **3 slug ĐÃ VÁ THẬT · 2 slug VÁ HỜ · 3 slug VÁ SINH LỖI MỚI · 0 slug CHƯA VÁ**, tổng **8 slug** | Đếm đúng phần đối chiếu của verdict, không đếm nhắc lại trong bảng/finding: **8/8 slug** khớp; chi tiết ở `classification.json` | ĐO ĐƯỢC+KHỚP | Nhãn slug không phải severity mới |
| R487-2:comment và diễn giải P2 cũ | Nhãn sinh lỗi mới không tái mở P2 | V487-2:8,26,34 ghi rõ đóng phần P2 cũ; phần mới mức P3; **3/3 vị trí nguồn** cùng nghĩa | ĐO ĐƯỢC+KHỚP | Có |
| R487-1:`nang_luc_do_cua_goi.so_ref` | Sửa **312 ref nhánh** thành **313 ref nhánh** | Scalar đổi đúng; V487-1:32–33 ghi **313 ref nhánh**; V487-2:27,66 cũng yêu cầu số ấy | ĐO ĐƯỢC+KHỚP | Không dùng snapshot mới để xác thực snapshot cũ |
| R487-1:`manifest.ghi_chu` | Vẫn khai mirror **312 ref nhánh** | Trái scalar **313 ref nhánh** và verdict cùng lượt; trường này chưa được sửa ở cả `edb288e` lẫn `3873173` | ĐO ĐƯỢC+LỆCH | Công sửa số ref còn sót |
| R487-1:`so_ref_dinh_chinh`, lịch sử push | Nhánh được đẩy sau gói đầu làm máy chủ tăng ref | Có lời giải thích trong receipt/commit, không có inventory và log đúng sự kiện push để tái đo; snapshot hiện tại **314 ref nhánh** không xác minh nhân quả lịch sử | KHÔNG ĐO ĐƯỢC | Chỉ đo được nội dung lời khai và số trong verdict |
| R487-1:chú thích đầu tệp; INDEX:270 | Rút “khác mọi lượt trước”/“không ai kiểm” | Chú thích R487-1 rút tại `edb288e`; INDEX rút tại `3873173`; **2/2 vị trí** đã rút ở HEAD; câu được nhắc lại chỉ trong ngữ cảnh đính chính | ĐO ĐƯỢC+KHỚP | Công sửa tính duy nhất là thật |
| R487-2:`ba_slug_sinh_loi_moi_va_da_sua_ngay`; INDEX:269 | Cả **3 lệch P3** đã sửa trong commit thêm verdict | `edb288e` chưa đổi INDEX; `3873173` mới sửa INDEX; manifest R487-1 vẫn sai tại HEAD; `repair-history.json` | ĐO ĐƯỢC+LỆCH | Sai cả mốc commit lẫn mức hoàn tất |
| R487-2:9; INDEX:269 so `CLAUDE.md`:722–726 | Chuỗi được dẫn mất **7 lượt review** | Nguồn nói **7 phát hiện lỗi** qua **4 lượt cross-review liên tiếp** | ĐO ĐƯỢC+LỆCH | Đổi sai đơn vị |
| INDEX:hàng mới so R487-2 và V487-2 | Approve; head `5c057782`; **36.009 byte**; **0 finding P1 · 0 finding P2 · 6 finding P3**; phân loại **8 slug** | Các trường identity và phân loại khớp **3/3 nguồn**; lời văn thời điểm sửa và số lượt có lỗi riêng ở trên | ĐO ĐƯỢC+KHỚP | Khớp identity, không phải mọi câu |
| INDEX:271 so receipt `pr480-land-review-2` | NAY có khóa `comment_ban_chieu` | Khóa tồn tại, URL kết thúc `#issuecomment-5600355552`; đã sửa câu phủ định cũ; Git xác định commit thêm khóa `5c05778`, không xác định lúc đăng comment | ĐO ĐƯỢC+KHỚP | Có trong Git |
| INDEX:271:comment bản chiếu | Comment được đăng sau review, là bản rút gọn | Không có response/readback GitHub; sự kiện và nội dung HTTP chưa đo được | KHÔNG ĐO ĐƯỢC | Không biến khóa URL thành xác thực nội dung |
| INDEX:toàn bảng | Thêm hàng verdict, giữ hàng cũ | **91 hàng** hiện tại; **90/90 hàng cũ** đúng thứ tự; **88/88 hàng không sửa** nguyên văn; **0 hàng trùng**; **5/5 hàng** receipt được đo khớp verdict/byte/head/severity; `index.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Về cấu trúc và identity |
| R487-1/R487-2:thời lượng | **1.526,889 giây**, **961,228 giây** | Hiệu timestamp **1.526,889169 giây**, **961,228463 giây**; **2/2 phép làm tròn** khớp; INDEX làm tròn thành **1.527 giây**, **961 giây** đúng | ĐO ĐƯỢC+KHỚP | Số học, không đo lại lần chạy |
| R487-1/R487-2:`model_reviewer_identity`, `tuan_thu_cam_cua_reviewer`, `manifest`, submitter | Runtime, model yêu cầu, prompt/hash stdout/stderr, số lần chết, clean cuối lượt, tác giả vận chuyển | `run.json`, argv, stdout/stderr gốc, prompt cũ, log kết thúc không có trong gói hiện tại; không mở đường dẫn scratchpad ngoài gói; nguồn API bị cấm | KHÔNG ĐO ĐƯỢC | Giữ nhãn attestation, không gọi dữ liệu sai chỉ vì thiếu nguồn |
| R487-2:`nang_luc_do_cua_goi`, `hai_slug_va_ho_con_lai_thanh_no` | Gói cũ **392 lá**, **67 dòng chú thích**, phục hồi **15.439 ký tự** trên **73 lá** | Khớp các số V487-2 đã báo; không có gói/script/output cũ để tái đo số phục hồi; **156 lá** của gói này thuộc đầu vào khác | KHÔNG ĐO ĐƯỢC | Chỉ đối chiếu được lời dẫn; không lấy gói mới bác số cũ |
| `BANG-CAU-TRUC-DAY-DU.tsv` | **156 lá** từ **2 receipt**, không cắt | **156/156 hàng** khớp type/path/toàn giá trị safe-load; **0 lá bị cắt**; `tables.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Giá trị sau YAML parse, không phải byte YAML nguyên văn |
| `BANG-CHU-THICH.tsv` | **21 dòng chú thích** | **21/21 dòng** khớp vị trí và nội dung của **2/2 tệp**; `tables.json`, `ok: true` | ĐO ĐƯỢC+KHỚP | Chỉ comment nguyên dòng |
| Gói:độ phủ bảng | Tự khai ngoài đầu vào: Markdown, comment cuối dòng, ngữ nghĩa trong lá | **8/8 ca thiếu nguồn** đối chứng ở bảng tiếp theo; không coi câu prose đã được giữ trong YAML là bị cắt | ĐO ĐƯỢC+KHỚP | Giới hạn tự khai đúng nhưng vẫn cần hậu kiểm thủ công |
| Git:cha merge thật `f4d74fe` | `7e69b8e` + `3873173` | Cặp OID đầy đủ trong `graph.json`; **2/2 cha** khớp; `da481f9` là tổ tiên của cha thứ nhất, không phải cha trực tiếp | ĐO ĐƯỢC+KHỚP | Nhãn cha cũ đã sai; nhãn sửa đúng |
| L489:`do_lai_tren_kho_du_313_ref`, `ket_luan_ve_a` | Hai cha đều đỏ; **4 vi phạm** ở mỗi cây | Cha thật `7e69b8e`: **86/86 biên nhận** phân loại, **33 biên nhận đạt**, **11 biên nhận miễn trừ**, **42 biên nhận nợ**, **0 vi phạm**; HEAD: **91/91 biên nhận**, **38 biên nhận đạt**, **11 biên nhận miễn trừ**, **42 biên nhận nợ**, **0 vi phạm**; cả hai có `TỔNG: ĐẠT` | ĐO ĐƯỢC+LỆCH | Lời bác không tái lập trong gói đầy đủ |
| L489:cổng trên nền cũ và merge thật | Nền cũ đỏ, merge thật đỏ sẵn | Nền cũ `da481f9`: **86/86 biên nhận** phân loại, **0 vi phạm**; merge thật `f4d74fe`: **91/91 biên nhận**, **0 vi phạm**; `gate-comparison.json`, `ok: true` về đầy đủ đầu vào | ĐO ĐƯỢC+LỆCH | Chưa xác định vì sao môi trường cũ cho số khác |
| L489:`ket_luan_ve_b`, năm neo | Neo thuộc tổ tiên HEAD | **5/5 neo** đúng đường dẫn, blob và commit thêm đầu tiên; **5/5 neo** là tổ tiên HEAD và **5/5 neo** là tổ tiên merge thật | ĐO ĐƯỢC+KHỚP | Bác yêu cầu đổi các neo này trong phạm vi gói |
| L489:merge tổng hợp `372bf9a` | Hàng đo vẫn có trong hồ sơ; bản sửa thừa nhận có thể thiếu object | `git cat-file -e 372bf9adb331218212619fc04763acbedfaa3f3f^{commit}` trả **mã thoát 128**, thông báo `Not a valid object name`; `cat-file -p` cũng không đọc được | KHÔNG ĐO ĐƯỢC | Đo được sự vắng trong gói; không tái chạy cổng trên object ấy |
| L489:132–136,150–151 | Object còn ở container ⇒ lần đo có thật; connector dùng kho thiếu object | Gói không chứa object hoặc log/checkout các phiên nguồn; phép đo hiện tại không chứng minh nguồn gốc khác biệt | KHAI RỘNG HƠN PHÉP ĐO | Giả thuyết chưa được phép dùng như sự kiện |
| Git:merge/master và thời điểm | HEAD đã vào master, mốc merge được nêu trong prompt | `master` cục bộ = `f4d74fed59616ecd5a133fc232275a832dcd95bb`; HEAD là tổ tiên; timestamp commit quy đổi thành `2026-09-09T11:58:30Z`; `graph.json`, `ok: true` cho quan hệ Git | ĐO ĐƯỢC+KHỚP | Timestamp Git không thay xác thực `merged_at` API |
| Các lời khai GitHub/CI/approval/readback/connector | API hoặc lời điều phối thuật lại | Không có quyền dùng mạng; không chứng nhận người bấm merge, trạng thái PR/check, nguyên văn comment hoặc môi trường connector | KHÔNG ĐO ĐƯỢC | Không suy từ Git sang API |
| Cổng receipt trên HEAD | Phép kiểm ngắn được phép | **91/91 biên nhận** phân loại; **38 biên nhận đạt**, **11/11 biên nhận miễn trừ**, **42 biên nhận nợ**; **0 vi phạm**, **0 trường hợp chưa đo**; `TỔNG: ĐẠT` | ĐO ĐƯỢC+KHỚP | Không chứng nhận prose/API |
| `doc-claims-check --strict` | Phép kiểm tài liệu | `ok: true`; **106 tệp** quét, **367 advisory**, **0 cờ cứng** | ĐO ĐƯỢC+KHỚP | Roots mặc định không phủ `ops/reviews`/`ops/land` |
| `doctrine-scan`, `adr-song` | Phép kiểm ngắn được phép | **7 tệp** quét, **0 chỗ chép doctrine**; **46/46 mục ADR** khớp; ngoại lệ trạng thái ADR-0016 được công cụ khai rõ | ĐO ĐƯỢC+KHỚP | Chỉ đúng phạm vi công cụ |
| `.github/workflows/ci.yml` | Không nâng timeout | **1/1 phép so blob** giữa các SHA giao khớp nguyên byte; không sửa tệp | ĐO ĐƯỢC+KHỚP | Không chạy CI |

## PHÂN XỬ CÁC FINDING CONNECTOR TRÊN PR #489

Nguồn tên và mô tả các finding là prompt được giao và commit message `8911ea4`, **không phải response GitHub đã được tôi xác thực**. Đã đối chiếu **6/6 mục** với các tệp trước/sau trong lịch sử Git, giới hạn từng mục như sau:

| finding được dẫn | áp cho HEAD này thế nào? | kết quả hậu kiểm |
|---|---|---|
| P1 `Re-review the exact head that was merged` | Áp cho việc dùng approve `5c05778` đối với `3873173` | Đồng ý về ranh giới review. **2/2 verdict PR #487** đã lưu trước lượt này neo các head trước đó; không có verdict đầy đủ cho HEAD trong bộ hiện vật ấy. Lượt này thực hiện review exact HEAD. Không thể sửa quá khứ để nói đã review trước merge. |
| P1 `Keep #477 pending until post-merge CI is verified` | Thuộc `pr480-land-evidence.yaml` trên nhánh hồ sơ sau merge; tệp vắng ở HEAD | Bản đầu tuyên `landed`; bản sau hạ thành `merged` và CI chưa xác minh. Không nhận câu này là lỗi mới của phần diff HEAD; trạng thái CI thực **KHÔNG ĐO ĐƯỢC**. |
| P2 `Add the required pre-merge evidence` | Thuộc các land evidence viết sau HEAD | Bản đầu thiếu khóa ở **2/2 tệp**; bản sau có **9 mục kiểm/tệp**. Đo được việc thêm trường, không xác thực rằng mọi phép đo đã chạy đúng trước merge; hàng receipt vẫn cần đính chính nguồn. |
| P2 `Measure the actual first parent of PR #487` | Đối chứng lập luận bác về HEAD, không phải dòng có trong HEAD | Đồng ý lỗi nhãn ban đầu; nhãn mới đúng. Nhưng phép đo bổ sung của tôi không hỗ trợ câu “không cha nào exit 0”: **2/2 cha thật** đều có `TỔNG: ĐẠT`. Không giữ nguyên toàn bộ lời bác chỉ vì đã sửa nhãn. |
| P2 `Retain the synthetic merge object` | Đối chứng hàng đo của lập luận, không phải lỗi các neo verdict trong HEAD | Đồng ý về thiếu khả năng tái lập: object không có trong gói. Chỉ ghi giới hạn không có nghĩa đã “retain” object. Không thể phục hồi đúng object từ OID trần trong lượt offline; không tạo một merge khác rồi gán làm `372bf9a`. Có thể bỏ hàng này khỏi căn cứ quyết định và dùng merge thật với dữ liệu được giữ. |
| P2 `Replace the stale unmerged-state assertion` | Thuộc `pr480-land-evidence.yaml`, vắng ở HEAD | Bản đầu nói hiện tại chưa merge trong khi bookkeeping nói đã merge; bản sau chuyển câu chưa merge thành snapshot lịch sử. Đo được sự sửa lời văn; mốc soạn theo API/phiên vẫn chưa xác minh. |

**Về tranh chấp neo:** điều phối đúng ở quan hệ tổ tiên **5/5 neo**; connector không có cơ sở để yêu cầu re-anchor các neo ấy trên gói này. Điều phối không chứng minh được lời bác về mã thoát bằng bảng hiện tại. Còn kết quả cổng của connector trên merge tổng hợp và môi trường của cả hai bên là **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**: thiếu object, thiếu log và cấm mạng. Không chọn một phía rồi suy mọi câu của phía đó đều đúng.

## KHẲNG ĐỊNH CẢ HAI BẢNG BỎ SÓT

“Bỏ sót” dưới đây là thiếu **nguồn/vị trí đối chiếu**: một ý có thể được receipt thuật lại, nhưng bảng không giữ nguồn verdict/INDEX để kiểm ý đó. Không nhận lá văn xuôi đã được bảng đầy đủ giữ là bị mất chữ; cũng không nhận câu ở comment đầu R487-2 là bị bỏ khi nó đã có trong bảng chú thích. `omissions.json`: **8/8 ca** đã kiểm nguồn tồn tại và không thuộc đầu vào của cả hai bảng, `ok: true`.

| vị trí | khẳng định | vì sao cả hai trượt | hệ quả |
|---|---|---|---|
| INDEX:271 | Receipt `pr480-land-review-2` NAY có `comment_ban_chieu` | INDEX và receipt được dẫn ngoài tập đầu vào **2 YAML** | Công sửa thật không được inventory này đối chiếu; cần đọc chéo Git |
| INDEX:271 | Comment là bản rút gọn, không phải nguyên văn | INDEX ngoài đầu vào; không có response API | Một lời khai API vẫn cần nhãn nguồn, không xác thực bằng URL |
| V487-1:33 | Snapshot của đúng lượt có **313/313 ref nhánh** | Verdict nguồn không vào bảng | Không thấy phản chứng trực tiếp cho `manifest.ghi_chu` còn **312 ref nhánh** |
| V487-2:8 | Approve exact SHA không phải thao tác duyệt hoặc quyền merge GitHub | Không đọc chính lời giới hạn của reviewer trong Markdown | Dễ dùng lời thuật ở receipt rộng hơn phạm vi approve |
| V487-2:78 | Cổng cũ phân loại **90/90 biên nhận**, **0 vi phạm** | Verdict ngoài đầu vào | Bỏ nguồn đối chứng có liên quan với lời khai đỏ của điều phối; không tự chứng minh nguyên nhân khác môi trường |
| V487-2:175 | Fixture chiếu dữ liệu giữ **8/8 trường cần kiểm**, **0 marker riêng**, **0 khóa cấm** | Verdict ngoài đầu vào; fixture/output lịch sử không kèm | Chỉ đọc lại được kết quả reviewer đã báo, không tái xác thực lần chạy cũ |
| V487-2:185 | Gói gợi ý lịch sử giữ **90/90 hàng mục lục** | Verdict ngoài đầu vào; bản gợi ý cũ không kèm | Không thể lấy số này làm chứng nhận cho bản vá do điều phối tự thực hiện sau đó |
| `pr486-hau-kiem-no-review.yaml`:4 | Chú thích inline xác định `pr_number` là số hiệu, không phải số lượng | Tệp ngoài đầu vào; safe-load không giữ inline comment | Ví dụ giới hạn loại/đơn vị vẫn chưa được phủ. Không khẳng định tồn tại comment inline bị mất trong chính các receipt đầu vào hiện tại |

### ket-luan-bac-connector-vuot-phep-do-hau-kiem  [P2]  Sửa nhãn cha nhưng vẫn bác bằng kết quả cổng không tái lập được

TỆP/DÒNG: **L489:105–125,132–155,176–177** tại commit đối chứng `8911ea41ed326807cf22c0dacbbff69be9342747`. Đây là finding nhiệm vụ đối chứng PR #489, **không phải tệp có trong reviewed HEAD**.

VẤN ĐỀ: Lập luận bác nói các cha thật đều đỏ và **4 vi phạm** là lỗi cũ. Trong gói được giao, CLI trên HEAD đạt; phép chiếu đầy đủ đầu vào cho cha thật, nền cũ và merge thật cũng đạt. Vì thế sửa `da481f9` thành `7e69b8e` chỉ sửa nhãn, chưa làm câu “không cha nào exit 0” đứng vững trước bên thứ ba. Khối giả thuyết ghi chưa chứng minh môi trường connector, nhưng câu kết lại dùng “một phép đo chạy trong kho thiếu object” như sự kiện; câu object từng còn ở container “nên phép đo có thật” cũng chưa có nguồn độc lập. Đây là căn cứ dùng để bác một cảnh báo P1, nên sai khác làm thay đổi quyết định tin/bác evidence, không chỉ lỗi trình bày. Việc **5/5 neo** đúng vẫn có chứng cứ riêng và phải được giữ.

ĐÃ THỬ VÁ: Giữ bảng lịch sử của điều phối với nhãn **attestation chưa tái lập**, bổ sung kết quả của đúng gói hậu kiểm; rút kết luận chung về mã thoát và nguyên nhân môi trường. Giữ nguyên neo verdict, tách merge tổng hợp thiếu object khỏi merge thật đã đo. Không kết luận điều phối bịa lần chạy, không biến phép đo sau thành bằng chứng đã chạy trước merge. Không thể tái tạo đúng `372bf9a` từ hash trần; gói vá dùng số đo merge thật với nhãn thật.

GÓI VÁ: `cay/ops/land/pr487-land-evidence.yaml` là **toàn bộ nội dung sửa** dựa trên L489, kèm `cay/ops/land/pr487-hau-kiem-3873173-do.json` giữ số liệu/đầu ra cổng và neo Git. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Executor đối chiếu với nhánh PR #489 hiện hành; không chép đè mù nếu nhánh ấy đã đổi sau commit nguồn. Không cần viết lại lịch sử để rút lời kết luận; không thể sửa quá khứ để biến thiếu review thành tiền kiểm.

ĐÃ THỬ NGHIỆM: CLI thật trên HEAD: **91/91 biên nhận** phân loại, `TỔNG: ĐẠT`. Phép chiếu giữ **86/86 receipt** ở mỗi nền cũ/cha thật và **91/91 receipt** ở mỗi HEAD/merge thật; **4/4 tệp mã/luật** nguyên byte tại mỗi SHA; `gate-comparison.json`, `ok: true` về đầu vào. Mỗi cây có **0 vi phạm**; không dựa vào mã thoát trần. YAML gói vá parse được; JSON đối chứng có `ok: true` cho các phép đo được ghi. Không xác minh API hoặc log môi trường khác.

ĐỘ TIN: cao về kết quả Git/cổng trong gói; chưa xác định nguyên nhân lệch với lời thuật các phiên khác. Không nâng điều chưa đo thành cáo buộc về người thực hiện.

### bien-nhan-luot-hai-chep-sai-so-ref  [P3]  Sửa scalar nhưng bỏ sót số ref trong manifest của cùng biên nhận

TỆP/DÒNG: R487-1:108–115,127–129; V487-1:32–33; V487-2:27,66,115–123.

VẤN ĐỀ: `so_ref` đã sửa đúng thành **313 ref nhánh**, nhưng `manifest.ghi_chu` vẫn ghi **312 ref nhánh**. Verdict cùng lượt đã đo **313 ref nhánh**. Lỗi cũ chưa được vá hết; không lấy **314 ref nhánh** của gói hiện tại để kết tội snapshot cũ. Đây là lệch nội bộ mức P3 như lượt trước, không tự nâng thành P2.

ĐÃ THỬ VÁ: Sửa nốt manifest, dẫn đúng verdict của lượt ấy, giữ nguyên identity/hash/SHA. Công rút tính duy nhất ở chú thích R487-1 và hàng INDEX là thật, không phủ nhận công sửa đó.

GÓI VÁ: `cay/ops/reviews/pr487-review-1-codex-verdict.receipt.yaml`, tệp đầy đủ, tự nguyện cho P3. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đối chiếu **3/3 phiên bản** base/commit thêm verdict/HEAD trong `repair-history.json`; **10/10 trường identity** của receipt giữ nguyên trong gợi ý. Bảng đầy đủ đã giữ cả scalar lẫn văn xuôi manifest; lỗi ở đây không phải chuỗi bị cắt.

ĐỘ TIN: cao về nội dung cùng lượt trong Git; không xác thực lịch sử máy chủ.

### khai-va-het-ba-loi-sai-commit  [P3]  Biên nhận mới và mục lục nhận công sửa sớm hơn lịch sử Git

TỆP/DÒNG: R487-2:44–52; INDEX:269; commit `edb288e4e95081b83661c94c88addea005d3f121`; lời này còn được chép sang L489:58–59.

VẤN ĐỀ: Câu “cả ba đã sửa trong chính commit đưa verdict vào kho” sai. Commit đầu tiên chứa verdict sửa receipt, chưa sửa INDEX. Câu phủ định URL và tính duy nhất trong INDEX chỉ được sửa ở `3873173`. Hơn nữa, số ref trong manifest vẫn chưa sửa tại HEAD. Phân bố **3 slug ĐÃ VÁ THẬT · 2 slug VÁ HỜ · 3 slug VÁ SINH LỖI MỚI · 0 slug CHƯA VÁ** của reviewer là đúng; không suy từ đúng phân bố ấy sang điều phối đã sửa hết sau review.

ĐÃ THỬ VÁ: Thay lời nhận hoàn tất bằng mốc commit và phần việc cụ thể; nói rõ manifest còn sai tại HEAD và được đính chính trong hậu kiểm. Đồng bộ receipt, INDEX và bản L489 dùng cùng lời ấy.

GÓI VÁ: R487-2 và INDEX đầy đủ dưới `cay/ops/reviews/`; L489 đi kèm gói P2. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `git show`/diff của **2/2 commit** sau approve và **3/3 snapshot** trong `repair-history.json`; INDEX không đổi ở commit thêm verdict. Gợi ý giữ **91/91 hàng mục lục** cùng thứ tự; không sửa verdict lịch sử.

ĐỘ TIN: cao; phép đo cây/commit trực tiếp, không dựa timestamp GitHub.

### doi-bay-phat-hien-thanh-bay-luot-review  [P3]  Dẫn CLAUDE.md nhưng đổi số phát hiện lỗi thành số lượt review

TỆP/DÒNG: R487-2:7–9; INDEX:269; nguồn `CLAUDE.md`:722–726.

VẤN ĐỀ: Nguồn nói **7 phát hiện lỗi** và **4 lượt cross-review liên tiếp**. Receipt và INDEX lại kể thành **7 lượt**. Đây là sai đơn vị của phép đếm được dùng làm bài học lịch sử. Không cần điều tra runtime các lượt cũ để phát hiện việc dẫn sai chính văn bản trong Git.

ĐÃ THỬ VÁ: Ghi đúng **7 phát hiện lỗi** qua **4 lượt cross-review liên tiếp**, hoặc chỉ giữ trích dẫn về lỗi vá cục bộ; không viết lại `CLAUDE.md`.

GÓI VÁ: R487-2 và INDEX dưới `cay/`, tệp đầy đủ. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: **2/2 vị trí dẫn sai** đối chiếu cùng nguồn. Câu ở đầu receipt đã được bảng chú thích giữ; cái thiếu là nguồn `CLAUDE.md` để kiểm đơn vị và vị trí INDEX. Không ghi nó thành “cả hai bảng bỏ mất nội dung câu”.

ĐỘ TIN: cao về dẫn sai văn bản; không xác minh số lượt runtime thực tế ngoài lời nguồn.

### bang-khang-dinh-bo-chu-thich-va-gioi-han-nguon  [P3]  Đủ lá và comment nguyên dòng vẫn thiếu các nguồn đối chứng Markdown

TỆP/DÒNG: phần đầu `BANG-CAU-TRUC-DAY-DU.tsv`, `BANG-CHU-THICH.tsv`; các vị trí cụ thể trong bảng bỏ sót ở trên.

VẤN ĐỀ: Công giữ đủ dữ liệu là thật: **156/156 lá**, **21/21 dòng chú thích**, không còn cắt đuôi trong tập này. Nhưng tập đầu vào chỉ có **2 receipt**; INDEX là tệp đổi bắt buộc review mà không được đọc, và verdict dùng để kiểm receipt cũng ngoài đầu vào. Tự khai chỗ mù không phải phép kiểm các nguồn bị bỏ. Đây là nợ độ phủ của gói, không phải thêm lỗi logic vào mã sản phẩm hoặc phủ nhận việc không cắt chuỗi.

ĐÃ THỬ VÁ: Đã bổ sung inventory có path/dòng/văn bản và kết quả đối chiếu vào `do-review/omissions.json` cùng bảng ở verdict này. Cần công bố tập đầu vào và giữ source Markdown trước khi trích mệnh đề; khi xử lý inline comment phải phân biệt dấu `#` trong scalar/URL. Không bổ sung vài token rồi tuyên phủ mọi mệnh đề.

GÓI VÁ: P3 không đòi tệp sản phẩm bắt buộc; inventory bổ sung và phép tái dựng giữ trong `do-review/`. Không thay bảng đầy đủ bằng bản parser cắt **160 ký tự** còn nằm trong script v2 của gói.

ĐÃ THỬ NGHIỆM: **156/156 hàng lá**, **21/21 hàng chú thích**, **8/8 ca thiếu nguồn** đã đối chiếu; `tables.json` và `omissions.json` có `ok: true`. Một ca inline ở tệp DEBT ngoài đầu vào được ghi riêng; không dựng ví dụ inline giả trong các receipt đang đọc.

ĐỘ TIN: cao về đầu vào và dữ liệu gói; không tự nhận đã tách hết nghĩa trong văn xuôi.

## GÓI VÁ, BẰNG CHỨNG VÀ ĐIỂM DỪNG

Có **5 tệp đầy đủ** dưới `cay/`: **3 tệp review** sửa từ HEAD, **1 tệp land evidence** sửa từ commit đối chứng PR #489, và **1 tệp JSON** lưu số liệu. Gói P2 gồm land evidence và JSON; các tệp còn lại là gợi ý tự nguyện cho P3. Tất cả mang nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Xem `GOI-VA.md` để biết nguồn từng tệp.

Bản gợi ý giữ **20/20 trường identity** của các receipt, **91/91 hàng INDEX** cùng thứ tự. YAML parse được; JSON đối chứng đọc được. Cổng receipt trên phép chiếu có áp **2 receipt gợi ý** vẫn phân loại **91/91 biên nhận**, gồm **38 biên nhận đạt**, **11/11 biên nhận miễn trừ**, **42 biên nhận nợ**; **0 vi phạm**, `TỔNG: ĐẠT`. Cổng này không đọc lời văn của INDEX/L489 và không chứng nhận nguồn API; các phần ấy được đối chiếu bằng phép đo đã nêu.

Không sửa verdict cũ, không đổi `reviewed_sha` cũ thành SHA mới, không cấp lease, không đăng Issue/PR/comment, không merge, không sửa kho thật, không tăng timeout workflow. Nội dung đã merge có thể được đính chính qua commit mới của PR #489. **Không sửa được bằng patch việc merge đã xảy ra trước review; tuyệt đối không viết lại lịch sử để tạo tiền kiểm giả.** Khi vận chuyển kết quả này, cần ghi rõ đã có lượt hậu kiểm exact HEAD với kết luận và các phạm vi ở đây; không để dòng “chưa có lượt hậu kiểm” tiếp tục làm trạng thái hiện tại, và không gọi có verdict là mọi finding đã được sửa.

**KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho):** GitHub API và CI thực tế; nguyên văn comment/readback; người/tài khoản bấm merge hay duyệt; môi trường/log của connector và điều phối; snapshot/runtime/fixture lịch sử không kèm; phép chạy trên object merge tổng hợp vắng; các bộ test dài, CI và test ngoài danh sách cho phép. Lý do tương ứng là cấm mạng, thiếu object/nguồn hoặc cấm chạy kiểm dài. Không coi `not_run`/không đo được là pass.

Kết thúc: `cay-kho/` giữ đúng HEAD được giao, detached, `status --porcelain` **0 byte**; phép kiểm cuối được lưu tại `do-review/final-integrity.json`. Findings dành cho PR #489 được giao bằng tệp trong gói, chưa đăng ra ngoài.
