VERDICT: changes_requested
P0=0 P1=7 P2=4 P3=0

## Lớp may-tin-gia-tri-nguoi-goi — P1

- biểu hiện: `ops/specs/wp796-r10.md:M1` — Ref `origin/ops/*`, `granted_by` và một `posted_comment_id` có mặt chưa chứng minh lease đã được người có thẩm quyền đăng.
- biểu hiện: `ops/specs/wp796-r10.md:M3` — Check-run chưa được neo vào repository, workflow và attempt của PR; `app.slug == github-actions` chỉ xác định ứng dụng phát check.
- biểu hiện: `ops/specs/wp796-r10.md:M5`; `ops/specs/wp797-r10.md:M2` — Người gọi vẫn quyết định slug cho comment mới; đường generation mới còn cho chọn riêng một finding muộn.
- đường lỗi cụ thể: Probe `lease_publish.kiem()` nhận ID đăng tự điền `123456`. Đưa lease cùng đặc tả lên nhánh ops đáp ứng các điều kiện M1 còn lại không bổ sung được chứng cứ đăng thật. Với bộ đếm, cùng nguyên nhân xuất hiện dưới hai comment ID mới có thể được gán hai slug khác nhau; finding tái diễn không chạm trần. M2 cũng có thể bỏ qua finding muộn khác khi chỉ tiêu thụ ID được chọn.
- hướng sửa ở mức lớp: Dùng chứng cứ authority đã xác minh, ràng buộc đầy đủ provenance của check-run, và lấy ánh xạ lớp cùng toàn bộ tập finding cần tiêu thụ từ hiện vật được kiểm độc lập. Thêm phản chứng ID đăng giả, check khác workflow/kho, đổi slug qua ID mới và bỏ sót finding muộn.

## Lớp ho-model-sai-enum — P1

- biểu hiện: `ops/specs/wp796-r10.md:M2, A12`; `ops/specs/wp797-r10.md:M1` — Helper được chỉ định không thực hiện đầy đủ phép chuẩn hoá mà đặc tả mô tả, còn bảng mặc định bị dùng thay họ model đã khai.
- đường lỗi cụ thể: Đo trong clone: `_chuan_hoa_provider("codex") == "codex"`, không phải `"openai_codex"`; `HO_MODEL_MAC_DINH` không có `google_antigravity`. Quan trọng hơn, receipt khai reviewer `model_family: gemini` có thể qua `_thieu()`, trong khi tra mặc định theo `openai_codex` vẫn ra `gpt`. Dùng phép suy của M2 sẽ so một họ khác với họ validator thực sự đọc, có thể che việc reviewer cùng họ executor.
- hướng sửa ở mức lớp: Định nghĩa rõ adapter giữa hai schema; dùng bộ giải họ model có xét khai báo thực tế, rồi đối chiếu cả identity Executor lẫn Reviewer với lease. Khoá bằng receipt thật, gồm khai báo đè họ model và reviewer Antigravity.

## Lớp dieu-kien-dung-khong-xet-o-moi-cua — P1

- biểu hiện: `ops/specs/wp796-r10.md:M1, M5b` — `_xet_dung` chỉ liệt kê bộ đếm, không bảo đảm lease chưa bị thay thế hoặc thu hồi.
- biểu hiện: `ops/specs/wp796-r10.md:M3`; `ops/specs/wp797-r10.md:M3` — `accept` và `record-push` không nằm trong các cửa phải kiểm lại điều kiện tiếp tục; quyền generation mới dựa vào lease “đã kiểm lúc init”.
- đường lỗi cụ thể: Probe cho thấy `lease_publish.kiem()` vẫn nhận lease có `da_bi_thay_the`. Lease g1 ấy vẫn có thể thoả M1. Hoặc lease hợp lệ khi init nhưng hết hạn sau approve: các điều kiện được kê cho `record-push` vẫn cho ghi lần đẩy hợp lệ.
- hướng sửa ở mức lớp: Kiểm lease đang hiệu lực, vai trò, generation và spec tại mọi cửa mở quyền; kiểm cả dấu thay thế/thu hồi. Thêm ca lease bị thay hoặc hết hạn giữa init, approve và ghi đẩy.

## Lớp dau-dang-lease-da-bi-go — P1

- biểu hiện: `ops/specs/wp796-r10.md:M1, A12`; `ops/specs/wp797-r10.md:M2` — Đặc tả bắt buộc một dấu ghi ngược mà workflow hiện hành đã bỏ.
- đường lỗi cụ thể: `.github/workflows/ops-publish-lease.yml` chỉ có `contents: read`, chú thích rõ packet #396 đã bỏ bước ghi `posted_comment_id`; bước đăng hiện chỉ in ID. Lease mới được đăng đúng quy trình sẽ thiếu trường M1 bắt buộc và bị từ chối.
- hướng sửa ở mức lớp: Chọn hợp đồng chứng minh việc đăng phù hợp với producer hiện hành và cập nhật dependency/write set tương ứng. Baseline nghiệm thu phải dùng đầu ra thực tế của workflow, không tự chèn dấu đã bị bỏ.

## Lớp tran-ngan-sach-chan-ca-hoan-tat — P1

- biểu hiện: `ops/specs/wp796-r10.md:M5b` — Phép `attempts_used >= attempts_limit` được áp cả khi hoàn tất lượt đang mở.
- biểu hiện: `ops/specs/wp797-r10.md:M1–M2` — Dùng cùng phép dừng cho ghi verdict và chuyển generation mà không phân biệt ngân sách đã cấp với yêu cầu cấp lượt mới.
- đường lỗi cụ thể: Mã hiện hành tăng `attempts_used` khi `begin-attempt`. Với trần 3, lượt thứ ba mở hợp lệ rồi có `attempts_used == 3`; `_xet_dung` tại `record-review` sẽ chuyển `blocked` ngay cả khi lượt ấy trả approve sạch. Tương tự, lời gọi Codex cuối được phép có thể bị chặn khi ghi kết quả.
- hướng sửa ở mức lớp: Phân biệt cửa cấp thêm ngân sách với cửa hoàn tất công việc đã được cấp. Ghi verdict hợp lệ trước khi quyết định còn được tiếp tục hay phải dừng; thêm ca approve thành công đúng lượt cuối.

## Lớp dem-trang-khong-loai-id-trung — P1

- biểu hiện: `ops/specs/wp796-r10.md:_doc_connector` — Số comment bằng `pr_json.comments` hoặc `review_comments` chưa chứng minh đã lấy đủ các object khác nhau.
- biểu hiện: `ops/specs/wp796-r10.md:M3, M5`; `ops/specs/wp797-r10.md:M3` — Mọi cửa dùng vị từ này đều kế thừa khả năng bỏ sót finding.
- đường lỗi cụ thể: PR có hai inline comment: một P1 và một P3. Tệp lấy nhầm cùng trang hai lần chứa `[P3, P3]` vẫn có hai phần tử, khớp `review_comments == 2`; P1 biến mất và `p0p2` có thể rỗng. Chốt khoá JSON trùng không bắt hai object có cùng ID.
- hướng sửa ở mức lớp: Kiểm ID duy nhất theo từng endpoint, từ chối bản ghi trùng/mâu thuẫn và đối chiếu tổng trên tập ID duy nhất. Thêm phản chứng lặp trang che P1 cho mọi cửa tiêu thụ.

## Lớp bien-nhan-offline-vuong-neo-to-tien — P1

- biểu hiện: `ops/specs/wp796-r10.md:M2`; `ops/specs/wp797-r10.md:M1` — Yêu cầu receipt qua validator hiện hành nhưng chưa xác định evidence checkout/ref độc lập với candidate đang được review.
- đường lỗi cụ thể: Verdict review H được tạo sau H và lưu ở commit E. `_neo_git()` hiện đòi commit neo verdict là tổ tiên của `HEAD`; chạy validator trong checkout H sẽ loại E. Hai loại neo khác hiện trả chưa đo được. Probe với hai commit có sẵn xác nhận cùng neo đạt tại evidence head nhưng bị loại tại candidate trước nó.
- hướng sửa ở mức lớp: Quy định rõ nơi đóng băng receipt/verdict và root/ref dùng để kiểm neo; đối chiếu chúng với H mà không đòi hiện vật sinh sau H nằm trong tổ tiên H. Thêm baseline xuyên suốt tạo review sau candidate thật.

## Lớp hop-dong-readback-khong-khop-github — P2

- biểu hiện: `ops/specs/wp796-r10.md:A4, A6` — Fixture dùng `status`, `commit_sha`, `has_any_findings` nhưng chưa định nghĩa phép dẫn xuất các trường ấy từ object GitHub thật.
- biểu hiện: `ops/specs/wp797-r10.md:M2` — Cho phép comment endpoint issue nhưng vẫn yêu cầu `commit_id`.
- đường lỗi cụ thể: Raw issue comment connector lưu trong receipt `wp461-review-1-codex-verdict.receipt.yaml` không có cả bốn trường trên; SHA review nằm trong `body`. Readback thật có thể bị loại trong khi fixture tự dựng đạt, hoặc người gọi phải tự bổ sung dữ liệu mà máy đang tin.
- hướng sửa ở mức lớp: Đóng hợp đồng raw input và phép chuẩn hoá theo từng loại object; xác định nguồn chứng minh completion, SHA và severity. Nghiệm thu bằng raw response đã lưu, không chỉ fixture chuẩn hoá tự tạo.

## Lớp moc-connector-khong-toan-phan — P2

- biểu hiện: `ops/specs/wp796-r10.md:_doc_connector, M3` — Không định nghĩa mốc khi một endpoint chưa có comment connector.
- biểu hiện: `ops/specs/wp797-r10.md:M2, A10` — Phép so finding muộn giả định mốc cùng endpoint luôn có ID và timestamp.
- đường lỗi cụ thể: PR sạch có comment tổng kết ở endpoint issue và không có inline comment. `accept` không thể lấy phần tử lớn nhất cho mốc review; finding inline đầu tiên đến sau đó không có mốc để so, nên đường sang generation mới bị kẹt.
- hướng sửa ở mức lớp: Định nghĩa trạng thái mốc rỗng và luật tiếp nhận object đầu tiên, không bịa timestamp. Thêm ca accepted sạch rồi nhận finding đầu tiên ở endpoint trước đó rỗng.

## Lớp vong-p3-khong-co-duong-vao-sau-approve — P2

- biểu hiện: `ops/specs/wp796-r10.md:M2, M5`; `ops/specs/wp797-r10.md:M1` — Có bộ đếm vòng vá P3 nhưng thiếu chuyển trạng thái để Executor tự chọn vá sau approve còn P3.
- đường lỗi cụ thể: Reviewer approve H với một lớp P3, state thành `approved_pending`. Trước lần đẩy chưa có CI đỏ hoặc connector finding để gọi `mo-lai`; `begin-attempt` không nhận state ấy. Executor không thực hiện được quyền vá thêm mà ADR-0054 §3 cho phép.
- hướng sửa ở mức lớp: Thêm đường mở vòng P3 trước lần đẩy, neo bảng lớp đã xác thực, làm stale approval cũ và giữ nguyên ngân sách. Kiểm chuỗi approve có P3 → chọn vá → review lại cùng các điều kiện dừng.

## Lớp ngoai-le-va-ci-khong-khoa-pham-vi — P2

- biểu hiện: `ops/specs/wp796-r10.md:M5`; `ops/specs/wp797-r10.md:M3` — Quyền `va-ci` chỉ chứng minh từng có check đỏ và connector không còn P0–P2, chưa ràng buộc nội dung bản vá vào ngoại lệ CI.
- đường lỗi cụ thể: Sau `mo-lai ci-do`, Executor sửa CI đồng thời sửa finding P3 hoặc thêm thay đổi sản phẩm trong write set; S được approve lại. Mọi điều kiện `record-push va-ci` vẫn đạt, dù ADR-0054 §1 cấm lần đẩy vá CI mang thêm bản vá finding review.
- hướng sửa ở mức lớp: Đòi hiện vật xác nhận phạm vi vá CI trên cặp H0→S, kèm check đỏ, nguyên nhân và lý do gate local bỏ sót. Bản vá có nội dung ngoài ngoại lệ phải đi checkpoint chủ kho; thêm ca trộn vá CI với vá finding.