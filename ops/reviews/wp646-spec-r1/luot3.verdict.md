Review độc lập lượt 3 cho Issue #646. Đã diff bản 2 với bản hiện hành, SHA-256 `f1950382f2c713bb9e1d0ef6f812fbcca3b4771b996b5f4161c4eff868b0c105`. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Worktree ở detached HEAD đúng OID. Tôi chạy nguyên script N5 bằng `python -B` với bản sao trong RAM và chạy N4 bằng `git grep` trên blob tại `HEAD`. Không ghi tệp hoặc gọi mạng.

| Finding lượt 2 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 N5 đọc YAML ở chế độ văn bản, bỏ lọt CRLF | **Đóng** | H và H gói lại ở 60 cột đều `rc=0`. Thêm một byte `0D` trong YAML hoặc đổi một byte YAML đều `rc=1` do lệch băm. Toàn tệp CRLF `rc=1` do mất neo YAML. |
| P2 N5 nhận mệnh đề sai vị trí hoặc trong khối mã | **Chưa đóng** | Base, dời ra cuối tệp, dời vào khối mã cuối tệp và dời ngay trước `## 5.` đều `rc=1`, thiếu 7/7. Bọc rào và thụt 4 dấu cách trong vùng đều `rc=1`. Ba ca đảo nghĩa đều `rc=1`, thiếu lần lượt mệnh đề 1, 3, 6. Ca ẩn trong HTML bên dưới vẫn xanh. |
| P3 N4 thiếu mẫu dương | **Đóng** | Cả 10 mẫu dương mới đều đúng 1 hit, `rc=0`. Sáu vị trí cổng đều 0 hit `heartbeat_at`, `rc=1`. Phạm vi glob có đúng 1 hit. Mẫu trần `bo_qua_han=True` ở CI vẫn có 4 hit như đặc tả ghi. |

| Mức | Finding lượt 3 | Phản chứng đã chạy |
|---|---|---|
| **P2** | N5 nhận nội dung ẩn trong HTML là văn xuôi. | Ngay sau YAML, chèn `Van dan <!-- ` rồi bảy mệnh đề nguyên văn và đóng ` -->` sau mệnh đề 7. Dòng mở bắt đầu bằng `Van dan`, nên bộ lọc đầu dòng bỏ qua comment. N5 trả `rc=0`, `thieu_menh_de []`, dù cả bảy mệnh đề đều bị ẩn. Cần kiểm các mệnh đề trên văn xuôi hiển thị và thêm ca này vào phản chứng. |
| **P3** | N5 chấp nhận tệp `menh_de.txt` rỗng. | Chạy trên base với đối số 2 rỗng cho `rc=0`, `thieu_menh_de []`. Cần ràng buộc đầu vào với bảy mệnh đề của đặc tả. |
| **P3** | N5 vẫn xanh khi H chứa cả mệnh đề đúng và câu đảo nghĩa. | Giữ bảy mệnh đề rồi thêm câu nói `heartbeat_at` tự kích hoạt thu hồi lease. N5 trả `rc=0`. Reviewer vẫn phải kiểm điều cấm thêm khẳng định ngoài §3. |

Rà L1–L7 không thấy hồi quy mới ngoài L6 ở phép đối chiếu văn xuôi của N5. Không có finding P0 hoặc P1. N1–N3 chưa được chạy lại trong lượt này.

KET_LUAN: request_changes
tokens used
67,922
Review độc lập lượt 3 cho Issue #646. Đã diff bản 2 với bản hiện hành, SHA-256 `f1950382f2c713bb9e1d0ef6f812fbcca3b4771b996b5f4161c4eff868b0c105`. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Worktree ở detached HEAD đúng OID. Tôi chạy nguyên script N5 bằng `python -B` với bản sao trong RAM và chạy N4 bằng `git grep` trên blob tại `HEAD`. Không ghi tệp hoặc gọi mạng.

| Finding lượt 2 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 N5 đọc YAML ở chế độ văn bản, bỏ lọt CRLF | **Đóng** | H và H gói lại ở 60 cột đều `rc=0`. Thêm một byte `0D` trong YAML hoặc đổi một byte YAML đều `rc=1` do lệch băm. Toàn tệp CRLF `rc=1` do mất neo YAML. |
| P2 N5 nhận mệnh đề sai vị trí hoặc trong khối mã | **Chưa đóng** | Base, dời ra cuối tệp, dời vào khối mã cuối tệp và dời ngay trước `## 5.` đều `rc=1`, thiếu 7/7. Bọc rào và thụt 4 dấu cách trong vùng đều `rc=1`. Ba ca đảo nghĩa đều `rc=1`, thiếu lần lượt mệnh đề 1, 3, 6. Ca ẩn trong HTML bên dưới vẫn xanh. |
| P3 N4 thiếu mẫu dương | **Đóng** | Cả 10 mẫu dương mới đều đúng 1 hit, `rc=0`. Sáu vị trí cổng đều 0 hit `heartbeat_at`, `rc=1`. Phạm vi glob có đúng 1 hit. Mẫu trần `bo_qua_han=True` ở CI vẫn có 4 hit như đặc tả ghi. |

| Mức | Finding lượt 3 | Phản chứng đã chạy |
|---|---|---|
| **P2** | N5 nhận nội dung ẩn trong HTML là văn xuôi. | Ngay sau YAML, chèn `Van dan <!-- ` rồi bảy mệnh đề nguyên văn và đóng ` -->` sau mệnh đề 7. Dòng mở bắt đầu bằng `Van dan`, nên bộ lọc đầu dòng bỏ qua comment. N5 trả `rc=0`, `thieu_menh_de []`, dù cả bảy mệnh đề đều bị ẩn. Cần kiểm các mệnh đề trên văn xuôi hiển thị và thêm ca này vào phản chứng. |
| **P3** | N5 chấp nhận tệp `menh_de.txt` rỗng. | Chạy trên base với đối số 2 rỗng cho `rc=0`, `thieu_menh_de []`. Cần ràng buộc đầu vào với bảy mệnh đề của đặc tả. |
| **P3** | N5 vẫn xanh khi H chứa cả mệnh đề đúng và câu đảo nghĩa. | Giữ bảy mệnh đề rồi thêm câu nói `heartbeat_at` tự kích hoạt thu hồi lease. N5 trả `rc=0`. Reviewer vẫn phải kiểm điều cấm thêm khẳng định ngoài §3. |

Rà L1–L7 không thấy hồi quy mới ngoài L6 ở phép đối chiếu văn xuôi của N5. Không có finding P0 hoặc P1. N1–N3 chưa được chạy lại trong lượt này.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T05:12:43Z
