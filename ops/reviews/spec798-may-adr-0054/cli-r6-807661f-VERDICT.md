VERDICT: changes_requested
P0=0 P1=2 P2=3 P3=0

## Lớp hien-vat-hop-le-chua-du-tham-quyen — P1

- biểu hiện: `ops/specs/wp796-r6.md`:M2 — Receipt khai `approve` được đưa vào `approved_pending` mà không kiểm bảng lớp còn P0/P1/P2 hay không.
- biểu hiện: `ops/specs/wp797-r6.md`:M1, M3 — Bảng lớp được đọc nhưng thiếu luật `approve ⇒ P0=P1=P2=0`; `record-push` tiếp tục dựa vào `approved_pending`.
- vì sao là lỗi theo (b)/(c): Receipt có danh tính, assurance và SHA đúng vẫn có thể tự mâu thuẫn giữa `approve` và một lớp P1 còn mở; validator hiện hành không kiểm quan hệ này. Đường đẩy khi đó trái ADR-0054 §1, §3, không cần giả mạo hiện vật.
- hướng sửa ở mức lớp: Dùng chung vị từ đủ điều kiện approval, kiểm cả verdict và các lớp còn mở trước khi cấp `approved_pending`. Thêm ca receipt hợp lệ về cấu trúc và băm nhưng khai `approve` cùng lớp P1; phải bị từ chối.

## Lớp checkpoint-chu-kho-bi-day-qua-thoi-diem-va — P1

- biểu hiện: `ops/specs/wp796-r6.md`:M5 — Nhánh `ci-do` phải phân biệt connector có P0–P2 hay không nhưng chỉ yêu cầu `--connector-comments`, thiếu đầu vào findings mà M3 dùng để đọc hạng.
- biểu hiện: `ops/specs/wp797-r6.md`:M3 — Loại `va-ci` cũng quyết định bỏ qua checkpoint từ riêng tệp summary.
- vì sao là lỗi theo (a)/(b): Summary `completed`, `has_any_findings: true` không phân biệt finding P1 với P3. Hai trường hợp cần quyết định khác nhau nhưng có cùng đầu vào đã đặc tả: máy phải hoặc bỏ checkpoint sai, hoặc chặn nhầm đường vá CI.
- hướng sửa ở mức lớp: Dùng chung phép đọc summary và findings đủ trang, neo cùng SHA, tại mọi cửa quyết định checkpoint. Thêm cặp ca có summary giống nhau nhưng findings lần lượt P1 và P3; kết quả phải khác nhau.

## Lớp chuyen-generation-giu-nham-ngu-canh-thuc-thi — P2

- biểu hiện: `ops/specs/wp797-r6.md`:M2 — `mo_lai_tu_sha` và `checkpoint_day` không thuộc nhóm dựng lại hay đặt lại nên bị chép sang generation mới.
- biểu hiện: `ops/specs/wp796-r6.md`:M5 — Dấu `mo_lai_tu_sha` được dùng để nhận connector từ `running`, khiến dấu mở lại của generation cũ tiếp tục điều khiển generation mới.
- biểu hiện: `ops/specs/wp797-r6.md`:M3 — `chu-kho` chỉ so SHA của `checkpoint_day`, nên checkpoint đã kiểm cho generation cũ có thể được dùng lại khi generation mới giữ nguyên SHA.
- vì sao là lỗi theo (b): Dựng lại toàn bộ lease chưa loại bỏ quyền và dấu thực thi phái sinh từ lease cũ. Checkpoint có phạm vi generation nhưng bản lưu dùng để cấp quyền lại chỉ giữ SHA và băm.
- hướng sửa ở mức lớp: Đặt lại các dấu mở lại và quyền checkpoint khi đổi generation; giữ chúng trong lịch sử riêng. Neo quyền đang dùng vào cả generation và SHA; thêm ca đổi generation nhưng giữ nguyên SHA để bắt việc tái dùng checkpoint cũ.

## Lớp ca-nghiem-thu-khong-phan-biet-dung-sai — P2

- biểu hiện: `ops/specs/wp796-r6.md`:A6 — Yêu cầu mọi lời gọi `chu-kho-duyet` ngoài `cho_chu_kho` bị từ chối, trong khi M5 cho phép `cho_phep_day` tại `approved_pending`.
- biểu hiện: `ops/specs/wp796-r6.md`:A6 — Ca kiểm finding không tồn tại vẫn dùng `--finding-id`, trong khi giao diện M5 đã đổi sang `--finding <id>=<slug>`.
- vì sao là lỗi theo (b): Ca đầu đòi hai kết quả trái nhau cho một lời gọi hợp lệ; ca sau có thể bị argparse chặn trước khi tới phép kiểm đang cần đo.
- hướng sửa ở mức lớp: Tách baseline dương theo từng phạm vi checkpoint, cập nhật đúng giao diện finding, rồi chỉ thay một điều kiện trong mỗi ca âm; đột biến phải làm hỏng chính phép kiểm tương ứng.

## Lớp finding-muon-bo-qua-luat-theo-hang — P2

- biểu hiện: `ops/specs/wp797-r6.md`:M2 — Finding muộn không bị giới hạn hạng nhưng luôn thực hiện `finding_counts[SLUG] += 1`, kể cả P3.
- vì sao là lỗi theo (b): Điều này trái M1 cùng đặc tả: lớp P3 không cộng vào `same_failure_limit`. Một P3 đến muộn có thể đẩy bộ đếm tới trần dù cùng finding ấy trong review thông thường được miễn.
- hướng sửa ở mức lớp: Đọc hạng finding muộn và dùng chung luật cập nhật bộ đếm với các đường khác; luôn giữ lịch sử nhưng không cộng P3 vào same-failure. Thêm ca P3 muộn khi bộ đếm lớp đang ở `limit−1`; bộ đếm phải giữ nguyên.