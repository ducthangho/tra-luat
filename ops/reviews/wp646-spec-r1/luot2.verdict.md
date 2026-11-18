Review độc lập lượt 2 cho Issue #646, revision 1, phạm vi `sensitive`. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached tại đúng OID của `master` cục bộ. SHA-256 bản sửa là `dd1ff3ce182d767e6f6f99f5fd18aad98aa77fbff6e932eb4650d35833ec894e`. Review chạy trên Linux, Python 3.13.18, `openai_codex / codex_cli / machine`. Model phục vụ cụ thể chưa xác minh được.

### Finding lượt 1

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 N5 — đếm token lọt câu đảo nghĩa | Đóng | Script bắt cả ba đột biến đảo nghĩa được yêu cầu. Hai lỗi nghiệm thu mới ghi riêng bên dưới. |
| P2 N4 — `grep -F` khớp nhầm | Đóng | `cmd_kiem_dong` cho 2 hit, rc 0 với `-F`, và 0 hit, rc 1 với `-Fw`. Toàn bộ số hit đã kê trong N4 khớp base. |
| P2 M2 — thiếu phạm vi áp dụng của hạn | Đóng | §3 phân biệt hạn tuyệt đối theo protocol, điều kiện đóng WP ở D4, kiểm hạn khi công bố và hai nhánh miễn riêng chốt hạn. |
| P2 N2 — thiếu phản chứng định danh | Đóng | N2 nêu hai thao tác đột biến cụ thể và dẫn đúng hai ca mẫu. Trên base, `doctrine-scan` rc 0, quét 12 tệp, 0 chỗ chép. `adr-song` rc 0, 66 ADR khớp 66 dòng. |
| P3 M1 — phạm vi grep và hiệu lực ADR-0056 | Đóng | Git grep trên cây tracked xác nhận hit ngoài sáu vị trí nằm ở fixture, tài liệu hoặc hồ sơ. §4 và §20 xác nhận ngưỡng 360 phút áp cho lease mới thuộc hiệu lực ADR-0056. |
| P3 M3 — thiếu nhánh K4 | Đóng | Đã nêu cả review offline và human audit, đều ràng buộc với cùng head. |

### Kết quả chạy

Chạy nguyên script N5 trích từ đặc tả bằng `python -B -c`, truyền protocol và bảy mệnh đề qua file descriptor trong RAM. H thử chèn đủ bảy mệnh đề ngay sau rào YAML §4.

| Ca | Exit code | Bằng chứng |
|---|---:|---|
| Base | 1 | Thiếu `[1, 2, 3, 4, 5, 6, 7]`, băm YAML khớp |
| H thử | 0 | Thiếu `[]`, băm YAML khớp |
| H gói lại ở 60 cột | 0 | Thiếu `[]`, băm YAML khớp |
| Heartbeat tự kích hoạt thu hồi | 1 | Thiếu `[1]` |
| D4 đòi hạn chưa qua | 1 | Thiếu `[3]` |
| Bắt buộc khác `base_sha` | 1 | Thiếu `[6]` |
| Đổi `timestamp` thành `timestamP` trong YAML | 1 | Thiếu `[]`, băm YAML đổi |
| Thêm một byte `0D` trước `0A` ở dòng `heartbeat_at` trong YAML | **0** | Thiếu `[]`, script vẫn in băm base |
| Đặt đủ bảy mệnh đề trong khối mã cuối tệp | **0** | Thiếu `[]`, băm YAML khớp |

N4 chạy bằng `git grep -n` với từng mẫu và pathspec trong đặc tả, neo `HEAD`. Sáu phép `heartbeat_at` riêng lẻ đều 0 hit, rc 1. Hai glob cho 1 hit ở fixture, rc 0. Trong `lease_publish.py`, sáu mẫu `-E` đều 1 hit, rc 0, và `lease_until` 0 hit, rc 1. Trong `ci_duong_nhanh.py`, hai mẫu lần lượt 1 và 4 hit, rc 0. Trong `packet_loop.py`, 12 mẫu `-E` đều 1 hit, rc 0, và `reviewed_sha_required` 0 hit, rc 1.

### Đối chiếu bảy mệnh đề §3

| Mệnh đề | Kết quả |
|---|---|
| 1. `heartbeat_at` | Đúng trên snapshot. Các hit tracked đã đối chiếu thuộc fixture, tài liệu hoặc hồ sơ. |
| 2. 360 phút | Đúng theo §4 và §20. Đây là ngưỡng thu hồi do thiếu tiến triển, áp tay với lease mới thuộc hiệu lực ADR-0056. |
| 3. `lease_until` | Đúng. Protocol đặt hạn tuyệt đối. D4 đọc trường và yêu cầu mốc hạn `<=` thời điểm kiểm để đóng WP. |
| 4. `lease_expires_at_utc` | Đúng. `kiem()` chặn khi hạn đã tới và chốt hạn bật. `_phan_loai_lease` dùng cùng trường cho `ai-dang-giu`. |
| 5. Hai nhánh bỏ chốt hạn | Đúng. `kiem_github` chỉ bỏ chốt ở nhánh đã có dấu đăng. CI dùng `MA_KIEM_HET_HAN` khi hạn đọc được và đã tới. Cả hai vẫn kiểm định dạng hạn. |
| 6. `reviewed_sha_required` | Đúng về mã. `kiem()` đòi có trường và kiểm 40 hex thường sau `strip()`. Quy ước dùng `base_sha` khi chưa có head ứng viên do đặc tả đặt ra. |
| 7. Exact head | Đúng. K0 đối chiếu ref PR, K3 buộc connector theo repo/PR/head, K4 buộc review offline hoặc human audit theo cùng head, và `record-review` so với `reviewing_head_sha`. |

### Finding mới

| Mức | Finding | Cách sửa |
|---|---|---|
| **P2** | **N5 có thể bỏ lọt thay đổi byte YAML.** `open(..., encoding='utf-8')` chuẩn hóa newline. Ca thêm đúng một byte `0D` vào khối YAML vẫn rc 0 và in băm base, vi phạm yêu cầu giữ từng byte. | Đọc và băm lát cắt YAML trực tiếp trên `bytes`. Thêm ca LF → CRLF vào phản chứng. |
| **P2** | **N5 chấp nhận mệnh đề sai vị trí và sai dạng.** Đặt cả bảy mệnh đề trong khối mã cuối tệp vẫn rc 0 dù vùng văn xuôi bắt buộc ở §4 còn nguyên như base. | Giới hạn phép đối chiếu vào vùng giữa rào đóng YAML và đoạn `Lease role: reviewer`. Kiểm văn xuôi trong vùng đó và thêm ca dời cả đoạn ra ngoài §4. |
| **P3** | **N4 còn thiếu đối chứng dương cho các trường trực tiếp.** Danh sách có mẫu đếm tên hàm và nhãn, nhưng không có mẫu dương xác nhận `lease_expires_at_utc` ở nơi đọc hạn hoặc `reviewed_sha_required` ở nơi kiểm dạng. Mẫu CI `bo_qua_han=True` cũng đếm cả diễn giải trong docstring. | Thêm mẫu neo vào câu đọc và câu kiểm trường, cùng lời gọi thật trong `MA_KIEM_HET_HAN`. |

Rà L1–L7 cho thấy hai lỗi chặn thuộc L3/L6. L1 có đơn vị đếm, L2 chiếu M1–M3 vào một tệp, L4 khai đúng `khong_ap_dung`, L5 có mốc đo và yêu cầu đo lại trên base cấp lease, L7 dẫn ADR cho trần và dùng E2 cho duyệt băm.

`doc-claims-check` trên base thoát rc 1 ở khởi động do không có thư mục tạm ghi được, trước khi scanner chạy. Chưa chạy N2 trên H hoặc chạy lại hai phản chứng N2. Trạng thái Git giữ nguyên, hai bản đặc tả vẫn là tệp untracked được cấp cho review. Mọi phép đo trong lượt này đều cục bộ.

KET_LUAN: request_changes
tokens used
77,011
Review độc lập lượt 2 cho Issue #646, revision 1, phạm vi `sensitive`. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached tại đúng OID của `master` cục bộ. SHA-256 bản sửa là `dd1ff3ce182d767e6f6f99f5fd18aad98aa77fbff6e932eb4650d35833ec894e`. Review chạy trên Linux, Python 3.13.18, `openai_codex / codex_cli / machine`. Model phục vụ cụ thể chưa xác minh được.

### Finding lượt 1

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 N5 — đếm token lọt câu đảo nghĩa | Đóng | Script bắt cả ba đột biến đảo nghĩa được yêu cầu. Hai lỗi nghiệm thu mới ghi riêng bên dưới. |
| P2 N4 — `grep -F` khớp nhầm | Đóng | `cmd_kiem_dong` cho 2 hit, rc 0 với `-F`, và 0 hit, rc 1 với `-Fw`. Toàn bộ số hit đã kê trong N4 khớp base. |
| P2 M2 — thiếu phạm vi áp dụng của hạn | Đóng | §3 phân biệt hạn tuyệt đối theo protocol, điều kiện đóng WP ở D4, kiểm hạn khi công bố và hai nhánh miễn riêng chốt hạn. |
| P2 N2 — thiếu phản chứng định danh | Đóng | N2 nêu hai thao tác đột biến cụ thể và dẫn đúng hai ca mẫu. Trên base, `doctrine-scan` rc 0, quét 12 tệp, 0 chỗ chép. `adr-song` rc 0, 66 ADR khớp 66 dòng. |
| P3 M1 — phạm vi grep và hiệu lực ADR-0056 | Đóng | Git grep trên cây tracked xác nhận hit ngoài sáu vị trí nằm ở fixture, tài liệu hoặc hồ sơ. §4 và §20 xác nhận ngưỡng 360 phút áp cho lease mới thuộc hiệu lực ADR-0056. |
| P3 M3 — thiếu nhánh K4 | Đóng | Đã nêu cả review offline và human audit, đều ràng buộc với cùng head. |

### Kết quả chạy

Chạy nguyên script N5 trích từ đặc tả bằng `python -B -c`, truyền protocol và bảy mệnh đề qua file descriptor trong RAM. H thử chèn đủ bảy mệnh đề ngay sau rào YAML §4.

| Ca | Exit code | Bằng chứng |
|---|---:|---|
| Base | 1 | Thiếu `[1, 2, 3, 4, 5, 6, 7]`, băm YAML khớp |
| H thử | 0 | Thiếu `[]`, băm YAML khớp |
| H gói lại ở 60 cột | 0 | Thiếu `[]`, băm YAML khớp |
| Heartbeat tự kích hoạt thu hồi | 1 | Thiếu `[1]` |
| D4 đòi hạn chưa qua | 1 | Thiếu `[3]` |
| Bắt buộc khác `base_sha` | 1 | Thiếu `[6]` |
| Đổi `timestamp` thành `timestamP` trong YAML | 1 | Thiếu `[]`, băm YAML đổi |
| Thêm một byte `0D` trước `0A` ở dòng `heartbeat_at` trong YAML | **0** | Thiếu `[]`, script vẫn in băm base |
| Đặt đủ bảy mệnh đề trong khối mã cuối tệp | **0** | Thiếu `[]`, băm YAML khớp |

N4 chạy bằng `git grep -n` với từng mẫu và pathspec trong đặc tả, neo `HEAD`. Sáu phép `heartbeat_at` riêng lẻ đều 0 hit, rc 1. Hai glob cho 1 hit ở fixture, rc 0. Trong `lease_publish.py`, sáu mẫu `-E` đều 1 hit, rc 0, và `lease_until` 0 hit, rc 1. Trong `ci_duong_nhanh.py`, hai mẫu lần lượt 1 và 4 hit, rc 0. Trong `packet_loop.py`, 12 mẫu `-E` đều 1 hit, rc 0, và `reviewed_sha_required` 0 hit, rc 1.

### Đối chiếu bảy mệnh đề §3

| Mệnh đề | Kết quả |
|---|---|
| 1. `heartbeat_at` | Đúng trên snapshot. Các hit tracked đã đối chiếu thuộc fixture, tài liệu hoặc hồ sơ. |
| 2. 360 phút | Đúng theo §4 và §20. Đây là ngưỡng thu hồi do thiếu tiến triển, áp tay với lease mới thuộc hiệu lực ADR-0056. |
| 3. `lease_until` | Đúng. Protocol đặt hạn tuyệt đối. D4 đọc trường và yêu cầu mốc hạn `<=` thời điểm kiểm để đóng WP. |
| 4. `lease_expires_at_utc` | Đúng. `kiem()` chặn khi hạn đã tới và chốt hạn bật. `_phan_loai_lease` dùng cùng trường cho `ai-dang-giu`. |
| 5. Hai nhánh bỏ chốt hạn | Đúng. `kiem_github` chỉ bỏ chốt ở nhánh đã có dấu đăng. CI dùng `MA_KIEM_HET_HAN` khi hạn đọc được và đã tới. Cả hai vẫn kiểm định dạng hạn. |
| 6. `reviewed_sha_required` | Đúng về mã. `kiem()` đòi có trường và kiểm 40 hex thường sau `strip()`. Quy ước dùng `base_sha` khi chưa có head ứng viên do đặc tả đặt ra. |
| 7. Exact head | Đúng. K0 đối chiếu ref PR, K3 buộc connector theo repo/PR/head, K4 buộc review offline hoặc human audit theo cùng head, và `record-review` so với `reviewing_head_sha`. |

### Finding mới

| Mức | Finding | Cách sửa |
|---|---|---|
| **P2** | **N5 có thể bỏ lọt thay đổi byte YAML.** `open(..., encoding='utf-8')` chuẩn hóa newline. Ca thêm đúng một byte `0D` vào khối YAML vẫn rc 0 và in băm base, vi phạm yêu cầu giữ từng byte. | Đọc và băm lát cắt YAML trực tiếp trên `bytes`. Thêm ca LF → CRLF vào phản chứng. |
| **P2** | **N5 chấp nhận mệnh đề sai vị trí và sai dạng.** Đặt cả bảy mệnh đề trong khối mã cuối tệp vẫn rc 0 dù vùng văn xuôi bắt buộc ở §4 còn nguyên như base. | Giới hạn phép đối chiếu vào vùng giữa rào đóng YAML và đoạn `Lease role: reviewer`. Kiểm văn xuôi trong vùng đó và thêm ca dời cả đoạn ra ngoài §4. |
| **P3** | **N4 còn thiếu đối chứng dương cho các trường trực tiếp.** Danh sách có mẫu đếm tên hàm và nhãn, nhưng không có mẫu dương xác nhận `lease_expires_at_utc` ở nơi đọc hạn hoặc `reviewed_sha_required` ở nơi kiểm dạng. Mẫu CI `bo_qua_han=True` cũng đếm cả diễn giải trong docstring. | Thêm mẫu neo vào câu đọc và câu kiểm trường, cùng lời gọi thật trong `MA_KIEM_HET_HAN`. |

Rà L1–L7 cho thấy hai lỗi chặn thuộc L3/L6. L1 có đơn vị đếm, L2 chiếu M1–M3 vào một tệp, L4 khai đúng `khong_ap_dung`, L5 có mốc đo và yêu cầu đo lại trên base cấp lease, L7 dẫn ADR cho trần và dùng E2 cho duyệt băm.

`doc-claims-check` trên base thoát rc 1 ở khởi động do không có thư mục tạm ghi được, trước khi scanner chạy. Chưa chạy N2 trên H hoặc chạy lại hai phản chứng N2. Trạng thái Git giữ nguyên, hai bản đặc tả vẫn là tệp untracked được cấp cho review. Mọi phép đo trong lượt này đều cục bộ.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T05:02:31Z
