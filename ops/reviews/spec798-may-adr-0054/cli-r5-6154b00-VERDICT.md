VERDICT: changes_requested
P0=0 P1=2 P2=4 P3=0

## Lớp hien-vat-hop-le-chua-du-tham-quyen — P1

- biểu hiện: ops/specs/wp796-r5.md:M2 — Biên nhận được đối chiếu assurance và họ model nhưng chưa buộc identity thực tế khớp reviewer/surface trong lease; biên nhận `codex_service` hợp lệ vẫn có thể thỏa điều kiện dành cho `codex_cli`.
- biểu hiện: ops/specs/wp796-r5.md:M5; ops/specs/wp797-r5.md:M3 — Checkpoint có `thao_tac: cho_phep_va_sau_connector` được dùng để cho phép lần đẩy `chu-kho`, dù hiện vật chỉ thể hiện quyền vá.
- vì sao là lỗi theo (b): Hiện vật H đúng schema chưa chứng minh đúng người/bề mặt được giao hoặc đúng thao tác được cấp quyền. ADR-0054 §2 dành cả quyết định vá và quyết định đẩy thêm cho chủ kho; cho phép vá offline chưa mặc nhiên cho phép đẩy.
- hướng sửa ở mức lớp: Đối chiếu identity của biên nhận với lease và khai rõ phạm vi quyền trong checkpoint; quyền đẩy thêm phải được biểu diễn và kiểm riêng. Thêm ca biên nhận lệch surface và checkpoint chỉ cho vá.

## Lớp checkpoint-chu-kho-bi-day-qua-thoi-diem-va — P1

- biểu hiện: ops/specs/wp796-r5.md:M5 — Khi CI thật sự đỏ đồng thời connector có P1 trên cùng H, nhánh `ci-do` vẫn đưa thẳng về `running` mà không qua checkpoint.
- biểu hiện: ops/specs/wp796-r5.md:M5 — Nếu đã mở lại vì CI rồi connector mới báo P0–P2, `mo-lai connector` bị từ chối vì state không còn `approved_pending`, nên không đưa được packet vào `cho_chu_kho`.
- biểu hiện: ops/specs/wp797-r5.md:M3 — Đường `va-ci` chỉ đòi nguồn mở lại là `ci-do`, tiếp tục bỏ qua checkpoint trong hai tình huống trên.
- vì sao là lỗi theo (b): Các bằng chứng đều có thể là readback thật; lỗi nằm ở việc các nhánh phục hồi không bảo toàn yêu cầu dừng trước khi vá khi connector báo P0–P2, trái ADR-0054 §2.
- hướng sửa ở mức lớp: Cho sự kiện connector đưa mọi trạng thái phục hồi liên quan về checkpoint, đồng thời chặn tiếp tục vá/đẩy cho tới khi được duyệt. Kiểm cả trường hợp hai kết quả đồng thời và connector đến sau CI.

## Lớp chuyen-generation-giu-nham-ngu-canh-thuc-thi — P2

- biểu hiện: ops/specs/wp797-r5.md:M2 — Khóa `lease` hiện chứa `lease_id`, `granted_by`, `evidence`, `expires_utc` không thuộc NGỮ CẢNH hoặc ĐẶT LẠI, nên quy tắc “mọi khóa còn lại CHÉP” giữ nguyên lease cũ.
- biểu hiện: ops/specs/wp797-r5.md:A3 — Ca ngữ cảnh mới chỉ kiểm băm và danh tính, chưa kiểm lease mà `begin-attempt` thực sự sử dụng.
- vì sao là lỗi theo (b): State mới có thể mang `lease_id` mới nhưng giữ đối tượng `lease` cũ. Đối chiếu trong bộ nhớ với validator hiện tại cho thấy lease cũ hết hạn bị từ chối rc=8 trong khi lease mới đạt rc=0; việc đọc lease mới chưa bảo đảm ngữ cảnh thực thi đã chuyển.
- hướng sửa ở mức lớp: Dựng lại hoặc xóa toàn bộ dữ liệu lease hiện hành theo một hợp đồng rõ ràng; chỉ chép lịch sử và ngân sách. Thêm ca lease cũ hết hạn, lease mới còn hạn, rồi mở lượt bằng đường lệnh thật.

## Lớp ca-nghiem-thu-khong-phan-biet-dung-sai — P2

- biểu hiện: ops/specs/wp797-r5.md:A4 — Ca `chu-kho` vẫn yêu cầu từ chối khi thiếu “lease/biên nhận mới”, trong khi M3 r5 đã thay điều kiện ấy bằng checkpoint của `chu-kho-duyet`.
- vì sao là lỗi theo (b): Thiếu biên nhận approval có thể làm ca bị chặn trước khi tới chốt checkpoint; bỏ chốt checkpoint vẫn không làm ca đỏ. Ngược lại, thiếu lease mới không phải lý do từ chối một lượt vá cùng generation đã có checkpoint hợp lệ.
- hướng sửa ở mức lớp: Dựng baseline `chu-kho` hợp lệ với đầy đủ approval và lease hiện hành, rồi chỉ bỏ hoặc làm lệch checkpoint. Đột biến chỉ gỡ chốt checkpoint phải khiến đúng ca ấy đỏ.

## Lớp dinh-danh-lop-khong-duoc-chuan-hoa — P2

- biểu hiện: ops/specs/wp796-r5.md:M5 — Nhánh connector nhận ID comment nhưng không định nghĩa ánh xạ sang slug lớp để áp `same_failure_limit`; cùng nguyên nhân xuất hiện lại bằng comment ID mới không có khóa đếm chung.
- biểu hiện: ops/specs/wp797-r5.md:M1, A2 — Ca `{A:[a1], B:[b1]} → {C:[a1,b1]}` có bảng nối được yêu cầu hợp lệ, dù chuẩn hóa cả hai lượt theo `C ← A,B` cho kết quả 1 lớp → 1 lớp và không finding nào đóng.
- vì sao là lỗi theo (b): Phép đếm tái diễn và phép đo giảm lớp không dùng cùng định danh ổn định. Ca gộp trên tính thay đổi cách phân loại thành tiến bộ, trái yêu cầu đối chiếu trên cùng tập finding của protocol §8.3.
- hướng sửa ở mức lớp: Dùng một lớp ánh xạ từ ID bằng chứng sang slug ổn định cho mọi đường ghi finding; áp bảng nối lên cả lượt trước và lượt hiện tại trước khi so sánh. Ca chỉ gộp/đổi tên mà không giảm lớp sau chuẩn hóa phải dừng.

## Lớp generation-moi-khong-co-duong-ghi-push — P2

- biểu hiện: ops/specs/wp797-r5.md:M2–M3 — Sau `accepted(g1) → init(g2) → vá → approve(H2)`, `dau` bị chặn bởi sổ kế thừa, `va-ci` thiếu lần mở lại vì CI, còn `chu-kho` thiếu lần đi qua `chu-kho-duyet`.
- biểu hiện: ops/specs/wp796-r5.md:M5, A6 — `chu-kho-duyet` chỉ chạy ở `cho_chu_kho`; đường khởi tạo generation mới không đưa state tới đó, nên không thể bổ sung checkpoint trực tiếp cho luồng trên.
- vì sao là lỗi theo (b): Đường xử lý finding sau `accepted` tạo được generation mới nhưng không nối tới một loại ghi push hợp lệ. Muốn đi tiếp phải bỏ sổ push hoặc dựng thêm một vòng approve/mở lại không phục vụ bản vá, tiêu thêm ngân sách.
- hướng sửa ở mức lớp: Nối luồng generation mới với checkpoint và quyền ghi lần đẩy tương ứng, giữ nguyên lịch sử push. Thêm ca xuyên suốt từ `accepted(g1)` qua finding muộn tới vá, approve và ghi push thành công ở g2.