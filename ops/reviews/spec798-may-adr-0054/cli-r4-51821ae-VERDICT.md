VERDICT: changes_requested
P0=0 P1=2 P2=3 P3=0

## Lớp hien-vat-hop-le-chua-du-tham-quyen — P1

- biểu hiện: ops/specs/wp796-r4.md:M2 — Validator xanh và hai họ model khác nhau chưa bảo đảm biên nhận mang assurance mà Packet yêu cầu.
- biểu hiện: ops/specs/wp797-r4.md:M3 — `chu-kho` nhận lease hoặc biên nhận H mới hơn nhưng không buộc hiện vật ấy chứa quyết định của chủ kho cho đúng Packet và thao tác đẩy.
- vì sao là lỗi theo (b)/(c): Validator hiện hữu vẫn nhận biên nhận khai `advisory_review` hoặc `review_deferred`; đã kiểm riêng bằng fixture trong bộ nhớ. Một biên nhận reviewer mới cũng không tự thành checkpoint chủ kho. ADR-0054 và protocol §8 vẫn đòi đúng assurance và đúng authority, dù đầu vào thuộc H.
- hướng sửa ở mức lớp: Kiểm nội dung quyết định ngoài việc validate hiện vật: assurance được phép, vai trò/người quyết định, Packet/generation, SHA và phạm vi thao tác. Thêm ca dùng hiện vật H hợp lệ nhưng sai assurance hoặc sai authority; gỡ từng kiểm tra phải làm ca tương ứng đỏ.

## Lớp checkpoint-chu-kho-bi-day-qua-thoi-diem-va — P1

- biểu hiện: ops/specs/wp796-r4.md:M5 — Connector P0–P2 đưa packet về `running` mà checkpoint chủ kho được chuyển sang lần đẩy tiếp theo.
- biểu hiện: ops/specs/wp797-r4.md:M3 — Nhánh `chu-kho` chỉ kiểm checkpoint khi ghi lần đẩy, sau giai đoạn executor đã có thể vá.
- vì sao là lỗi theo (c): ADR-0054 §2, yêu cầu 2, ghi rõ checkpoint phải có **trước khi vá**. Phân loại `mo-lai` là chuyển thu hẹp quyền không giải quyết mâu thuẫn thời điểm này.
- hướng sửa ở mức lớp: Chặn đường được phép vá cho tới khi có checkpoint đúng scope; có thể dùng trạng thái chờ chủ kho. Kiểm riêng connector P0–P2 và CI đỏ, với ca thiếu checkpoint không được quay vào đường thi công.

## Lớp chuyen-generation-giu-nham-ngu-canh-thuc-thi — P2

- biểu hiện: ops/specs/wp797-r4.md:M2 — Quy tắc chép mọi khóa ngoài danh sách đặt lại giữ cả `spec_hash`, `executor_identity` và `reviewer_identity`, dù lease mới không bị buộc giữ nguyên những giá trị ấy.
- vì sao là lỗi theo (b)/(c): Một generation được cấp hợp lệ có thể đi cùng revision hoặc executor mới theo protocol §3.2. Khi ấy yêu cầu chép nguyên ngữ cảnh cũ xung đột với wp796 M1 phải lấy hash từ lease mới; các consumer cũng tiếp tục đối chiếu danh tính cũ.
- hướng sửa ở mức lớp: Giữ ngân sách và lịch sử, nhưng tái lập toàn bộ ngữ cảnh lease/spec/danh tính từ cấp việc mới. Thêm ca generation mới đổi hash hoặc executor, kiểm ngữ cảnh mới được dùng trong khi ngân sách vẫn được bảo toàn.

## Lớp tu-choi-verdict-lam-mat-lich-su-va-budget — P2

- biểu hiện: ops/specs/wp797-r4.md:M1 — Verdict P3 không giảm hoặc vượt trần bị từ chối với state giữ nguyên từng byte, nên không thể ghi nhận lượt review và bảng lớp vừa thực sự nhận.
- vì sao là lỗi theo (b)/(c): Verdict đã qua schema, exact SHA và receipt validation nhưng không hội tụ là bằng chứng phải dẫn tới stop/checkpoint. Bỏ toàn bộ cập nhật khiến lịch sử và `review_rounds_used` thiếu lượt ấy, trái nghĩa vụ bảo toàn lịch sử/budget ở protocol §8.3 và §12.
- hướng sửa ở mức lớp: Tách lỗi đầu vào khỏi kết quả review hợp lệ chạm stop condition. Kết quả hợp lệ phải được ghi sổ rồi dừng; kiểm trần trước khi cấp lượt tiếp theo. Thêm ca xác nhận verdict không giảm vẫn xuất hiện trong lịch sử và bộ đếm.

## Lớp ca-nghiem-thu-khong-phan-biet-dung-sai — P2

- biểu hiện: ops/specs/wp797-r4.md:A3 — Fixture gọi `accept → record-push --loai dau`, trong khi M3 chỉ cho `dau` chạy ở `approved_pending`; sau `accept` state đã là `accepted`.
- biểu hiện: ops/specs/wp797-r4.md:A3 — Ca tiêu thụ hai lần theo thứ tự được mô tả vẫn từ chối lần hai nhờ `accepted_vo_hieu_boi` khi bỏ khóa, nên chưa chứng minh được đột biến bỏ khóa phải đỏ.
- vì sao là lỗi theo (b): Fixture thứ nhất không thể đạt baseline dương đúng hợp đồng; fixture thứ hai không phân biệt tác dụng của khóa với chốt đã tiêu thụ.
- hướng sửa ở mức lớp: Dựng luồng `approve → record-push dau → accept`; kiểm khóa bằng hai caller đồng thời với điểm đồng bộ xác định. Yêu cầu baseline đạt và từng mutant bị bắt bởi đúng tính chất cần đo.