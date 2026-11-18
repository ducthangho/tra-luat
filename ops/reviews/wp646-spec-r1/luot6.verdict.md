## Review độc lập lượt 6 · Issue #646

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả `15b17a014f99c687859a5f66a0e5ce6adcd01be4741bdce771b46151c9baf322`. Reviewer thuộc họ OpenAI, phiên Codex qua API, phép đo bằng shell Linux và RAM. Model/effort phục vụ chưa đo được. Không gọi mạng hay ghi vào checkout.

### Finding lượt 5

| Finding | Trạng thái | Bằng chứng lượt 6 |
|---|---|---|
| P2 · N5 nhận bảy mệnh đề trong thuộc tính HTML, link reference, setext heading hoặc ô tiêu đề bảng | **Đóng** | Chạy nguyên script N5 trích từ đặc tả bằng `python -B -c` với blob qua `memfd`. H đúng khối trả `0`. Cả bốn biến thể trả `1` do lệch byte vùng đích. |
| P2 · N5 đỏ oan khi ngắt dòng trước `#646.` | **Đóng** | Biến thể dựng trên khối mới với dòng bắt đầu `#646.` trả `1`. §3 và §9 đã chốt cách xuống dòng theo byte, nên đây là kết quả đúng với hợp đồng mới. |

Base, đảo nghĩa, dời khối ra cuối tệp, CRLF trong vùng, CRLF toàn tệp và thêm câu đều trả `1`. Khi đổi `vung!=ky_vong` thành `ky_vong not in vung`, ca giữ nguyên khối rồi thêm câu trong vùng đổi từ `1` sang `0`. H đúng khối cho numstat `14 0` và N5 in đúng `VUNG_SHA` cùng băm YAML.

### Finding mới

| Mức | Finding | Bằng chứng và điều kiện đóng |
|---|---|---|
| **P2** | **N1 + N5 bỏ lọt thay đổi mode Git.** N1 và §6 khẳng định hai phép đo khóa H thành đúng base cộng khối chèn. | Trong repo trên RAM, tôi dựng hai commit ứng viên có cùng blob, một giữ `100644`, một dùng `git update-index --chmod=+x`. Cả hai cho cùng `git diff --name-only <base>..H`, cùng numstat `14 0` và N5 đều trả `0`. `git diff --summary <base>..H` phân biệt được ca thứ hai với `mode change 100644 => 100755`. §6 vẫn yêu cầu reviewer đọc diff và có thể bắt lỗi này bằng tay. Để khóa bằng phép đo, yêu cầu blob tại H bằng toàn bộ blob kỳ vọng dựng từ base, giữ mode Git của base, và thêm ca đổi mode vào cột phản chứng N1. |
| **P3** | **§6 và §8 còn số liệu từ bản cũ.** | §6 đếm bốn lượt `request_changes` rồi dự kiến lượt approve, dù §9 đã ghi lượt 5 `request_changes`. §8 ghi bản thử thêm 13 dòng, trong khi §0 và phép đo lượt này đều cho 14. Cập nhật số dòng và lấy số lời gọi thực tế từ biên nhận tại điểm chờ E2. |

Không có finding P0 hoặc P1 mới.

### Neo vùng, N4 và L1–L7

- **Neo vùng.** Trên blob base, mỗi neo `## 4.`, `## 5.`, `Lease gồm:` kèm rào YAML và `Lease role: reviewer` xuất hiện đúng một lần theo mẫu byte của script. Vùng base dài 0 byte và cả bảy dòng mệnh đề đều vắng trên base. Tôi chưa tìm thấy biến thể **nội dung blob** ngoài khối vẫn qua N1 + N5 với cấu hình Git mặc định đã thử. Phản chứng ở trên làm đổi cây Git dù blob giữ đúng.
- **N4.** Cả 28 mẫu dương đã khai đều cho 1 hit, `rc=0`. Sáu vị trí cổng đều cho 0 hit `heartbeat_at`, `rc=1`, còn glob rộng cho đúng 1 hit fixture. Xóa lần lượt câu đọc hạn, câu kiểm SHA và lời gọi CI khỏi bản sao làm mẫu dương tương ứng trả `rc=1`, 0 hit. Sau khi xóa lời gọi CI, mẫu trần `bo_qua_han=True` vẫn còn 3 hit. Đọc mã và protocol xác nhận bảy mệnh đề trong phạm vi cổng vận hành. Hai ngoại lệ hạn áp vào nhánh đã đăng và lease lịch sử hết hạn. K0/K3/K4 và `record-review` dùng các neo head như đặc tả mô tả. Việc cho phép `reviewed_sha_required` bằng `base_sha` khi chưa có head ứng viên là quy ước được đặc tả chọn.
- **L1–L7.** L1 có đơn vị đếm, L2 quy về một tệp trong write set, L4 không áp dụng vì đây là packet làm rõ protocol. L3 có phản chứng cho từng tiêu chí và cần bổ sung ca đổi mode của N1. L5 có exact base, băm và mốc đo, với hai số cũ cần sửa như trên. L6 phù hợp với blob đã chốt, ca dương/âm và số hit từng vị trí cổng. Với L7, điểm chờ **E2** duyệt băm phù hợp khi chưa có căn cứ áp dụng ủy quyền cho Mission đã duyệt hướng. Duyệt băm và cấp lease là hai bước thẩm quyền riêng. Tình trạng Mission, lease và biên nhận hiện hành chưa được xác minh trong lượt offline này. N2 và N3 chưa chạy lại trong lượt 6.

KET_LUAN: request_changes
tokens used
88,046
## Review độc lập lượt 6 · Issue #646

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả `15b17a014f99c687859a5f66a0e5ce6adcd01be4741bdce771b46151c9baf322`. Reviewer thuộc họ OpenAI, phiên Codex qua API, phép đo bằng shell Linux và RAM. Model/effort phục vụ chưa đo được. Không gọi mạng hay ghi vào checkout.

### Finding lượt 5

| Finding | Trạng thái | Bằng chứng lượt 6 |
|---|---|---|
| P2 · N5 nhận bảy mệnh đề trong thuộc tính HTML, link reference, setext heading hoặc ô tiêu đề bảng | **Đóng** | Chạy nguyên script N5 trích từ đặc tả bằng `python -B -c` với blob qua `memfd`. H đúng khối trả `0`. Cả bốn biến thể trả `1` do lệch byte vùng đích. |
| P2 · N5 đỏ oan khi ngắt dòng trước `#646.` | **Đóng** | Biến thể dựng trên khối mới với dòng bắt đầu `#646.` trả `1`. §3 và §9 đã chốt cách xuống dòng theo byte, nên đây là kết quả đúng với hợp đồng mới. |

Base, đảo nghĩa, dời khối ra cuối tệp, CRLF trong vùng, CRLF toàn tệp và thêm câu đều trả `1`. Khi đổi `vung!=ky_vong` thành `ky_vong not in vung`, ca giữ nguyên khối rồi thêm câu trong vùng đổi từ `1` sang `0`. H đúng khối cho numstat `14 0` và N5 in đúng `VUNG_SHA` cùng băm YAML.

### Finding mới

| Mức | Finding | Bằng chứng và điều kiện đóng |
|---|---|---|
| **P2** | **N1 + N5 bỏ lọt thay đổi mode Git.** N1 và §6 khẳng định hai phép đo khóa H thành đúng base cộng khối chèn. | Trong repo trên RAM, tôi dựng hai commit ứng viên có cùng blob, một giữ `100644`, một dùng `git update-index --chmod=+x`. Cả hai cho cùng `git diff --name-only <base>..H`, cùng numstat `14 0` và N5 đều trả `0`. `git diff --summary <base>..H` phân biệt được ca thứ hai với `mode change 100644 => 100755`. §6 vẫn yêu cầu reviewer đọc diff và có thể bắt lỗi này bằng tay. Để khóa bằng phép đo, yêu cầu blob tại H bằng toàn bộ blob kỳ vọng dựng từ base, giữ mode Git của base, và thêm ca đổi mode vào cột phản chứng N1. |
| **P3** | **§6 và §8 còn số liệu từ bản cũ.** | §6 đếm bốn lượt `request_changes` rồi dự kiến lượt approve, dù §9 đã ghi lượt 5 `request_changes`. §8 ghi bản thử thêm 13 dòng, trong khi §0 và phép đo lượt này đều cho 14. Cập nhật số dòng và lấy số lời gọi thực tế từ biên nhận tại điểm chờ E2. |

Không có finding P0 hoặc P1 mới.

### Neo vùng, N4 và L1–L7

- **Neo vùng.** Trên blob base, mỗi neo `## 4.`, `## 5.`, `Lease gồm:` kèm rào YAML và `Lease role: reviewer` xuất hiện đúng một lần theo mẫu byte của script. Vùng base dài 0 byte và cả bảy dòng mệnh đề đều vắng trên base. Tôi chưa tìm thấy biến thể **nội dung blob** ngoài khối vẫn qua N1 + N5 với cấu hình Git mặc định đã thử. Phản chứng ở trên làm đổi cây Git dù blob giữ đúng.
- **N4.** Cả 28 mẫu dương đã khai đều cho 1 hit, `rc=0`. Sáu vị trí cổng đều cho 0 hit `heartbeat_at`, `rc=1`, còn glob rộng cho đúng 1 hit fixture. Xóa lần lượt câu đọc hạn, câu kiểm SHA và lời gọi CI khỏi bản sao làm mẫu dương tương ứng trả `rc=1`, 0 hit. Sau khi xóa lời gọi CI, mẫu trần `bo_qua_han=True` vẫn còn 3 hit. Đọc mã và protocol xác nhận bảy mệnh đề trong phạm vi cổng vận hành. Hai ngoại lệ hạn áp vào nhánh đã đăng và lease lịch sử hết hạn. K0/K3/K4 và `record-review` dùng các neo head như đặc tả mô tả. Việc cho phép `reviewed_sha_required` bằng `base_sha` khi chưa có head ứng viên là quy ước được đặc tả chọn.
- **L1–L7.** L1 có đơn vị đếm, L2 quy về một tệp trong write set, L4 không áp dụng vì đây là packet làm rõ protocol. L3 có phản chứng cho từng tiêu chí và cần bổ sung ca đổi mode của N1. L5 có exact base, băm và mốc đo, với hai số cũ cần sửa như trên. L6 phù hợp với blob đã chốt, ca dương/âm và số hit từng vị trí cổng. Với L7, điểm chờ **E2** duyệt băm phù hợp khi chưa có căn cứ áp dụng ủy quyền cho Mission đã duyệt hướng. Duyệt băm và cấp lease là hai bước thẩm quyền riêng. Tình trạng Mission, lease và biên nhận hiện hành chưa được xác minh trong lượt offline này. N2 và N3 chưa chạy lại trong lượt 6.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:06:54Z
