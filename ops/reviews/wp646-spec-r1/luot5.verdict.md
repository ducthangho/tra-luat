Review độc lập lượt 5 cho Issue #646. Đã đối chiếu hai bản bằng `diff -u` (`rc=1`, có thay đổi) và chạy nguyên script N5 trích từ từng đặc tả bằng `python -B` trên bản sao trong RAM. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. HEAD ở trạng thái detached, trùng các ref `master` và `origin/master` cục bộ. Bản đặc tả được review có SHA-256 `79fdd57d283af2fa6494e80602253c385c68e049dc88a7ba7f0971a10b4aa5e9`. Môi trường Linux, `openai_codex / codex_cli / machine`, chưa đo được model phục vụ. Phiên chạy chỉ đọc và offline.

| Finding lượt 4 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — N5 nhận bảy mệnh đề trong blockquote chứa rào | Đóng | Bản 4 `rc=0`. Bản 5 `rc=1`, báo vùng không phải văn xuôi cấp ngoài cùng. |
| P2 — N5 nhận bảy mệnh đề trong code span hai backtick mở giữa dòng | Đóng | Bản 4 `rc=0`. Bản 5 `rc=1`, báo thiếu cả bảy mệnh đề. |
| P3 — Điểm chờ E2 ở §6 thiếu dữ liệu | Đóng | §6 đủ ba mục theo L7 và ADR-0067 cho việc đóng băng đặc tả: mức tiêu hao lấy từ biên nhận khi hỏi, một comment duyệt `spec_sha256` còn thiếu, và mục đích dùng băm để neo lease g1. Cụm “lượt approve sắp tới” là dự kiến. Mức đã dùng phải lấy từ biên nhận thực tế. |

H dựng từ đúng bảy mệnh đề §3 và H ngắt 60 cột đều `rc=0`, với danh sách mệnh đề thiếu và trường thừa đều rỗng. Cả 131 độ rộng nguyên từ 30 đến 160 cột đều xanh. Base và các đột biến lượt 2–4 chạy lại đều `rc=1`: đảo nghĩa mệnh đề 1/3/6, sửa byte YAML, CRLF, dời sai vùng, rào, thụt lề, comment HTML, blockquote, danh sách, tiêu đề ATX, code span bọc ngoài, sửa hoặc làm rỗng mệnh đề nhúng, và câu thêm có tên trường. Câu thêm không nhắc tên trường vẫn `rc=0` đúng giới hạn đã ghi. Diff của H thử chỉ thêm bảy mệnh đề §3.

### Finding mới

| Mức | Vị trí | Phản chứng và yêu cầu sửa |
|---|---|---|
| **P2** | N5 — đối chiếu chuỗi ngoài văn xuôi | Gọi `M` là bảy dòng §3 nối bằng dấu cách. Bốn ca đều cho N5 `rc=0`, thiếu `[]`, thừa `[]`: `Dẫn <span title='M'></span>.`, `Dẫn.` rồi dòng trống và `[ref]: /local "M"`, `M` rồi dòng `===`, và `Dẫn \| M` rồi dòng `--- \| ---`. `pandoc --sandbox -f gfm -t html` trả `rc=0` và xác nhận mệnh đề lần lượt nằm trong thuộc tính HTML, biến mất khỏi phần hiển thị, nằm trong `<h1>`, và nằm trong ô tiêu đề bảng. N5 cần xác nhận mệnh đề thuộc đoạn văn xuôi cấp ngoài cùng. Thêm cả bốn ca âm. |
| **P2** | N5 — ngắt dòng làm H hợp lệ đỏ oan | Thêm câu dẫn `Xem Issue #646.` trước mệnh đề 1 cho `rc=0`. Chỉ ngắt dòng ngay trước `#646.` thì `rc=1`, do `KHOI` chặn mọi dòng bắt đầu bằng `#`. Pandoc dựng hai bản thành cùng đoạn `<p>`. Ca này vi phạm cam kết ngắt dòng tự do ở §3 và L6(b). Thêm cặp ca dương và phân biệt dấu `#` trong văn xuôi với dấu mở tiêu đề ATX. |

Rà L1–L7: L1 có đơn vị đếm. L2 ánh xạ M1–M3 vào đúng một tệp. L3 có ca âm cho N1–N5, nhưng N5 còn lọt các ca trên. L4 ghi `khong_ap_dung` phù hợp. L5 có mốc đo, exact base và yêu cầu đo lại. L6 có đối chứng base/H, đối chiếu từng mệnh đề và mẫu theo vị trí cổng, nhưng còn hai finding P2. L7 có mã E2 và đủ dữ liệu cho điểm chờ duyệt băm, cùng khai báo phạm vi E4/E5. N1–N4 được rà ở mức đặc tả, chưa chạy toàn bộ gate trên một commit H. Issue và biên nhận từ xa chưa được xác minh trong phiên offline.

KET_LUAN: request_changes
tokens used
60,309
Review độc lập lượt 5 cho Issue #646. Đã đối chiếu hai bản bằng `diff -u` (`rc=1`, có thay đổi) và chạy nguyên script N5 trích từ từng đặc tả bằng `python -B` trên bản sao trong RAM. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. HEAD ở trạng thái detached, trùng các ref `master` và `origin/master` cục bộ. Bản đặc tả được review có SHA-256 `79fdd57d283af2fa6494e80602253c385c68e049dc88a7ba7f0971a10b4aa5e9`. Môi trường Linux, `openai_codex / codex_cli / machine`, chưa đo được model phục vụ. Phiên chạy chỉ đọc và offline.

| Finding lượt 4 | Trạng thái | Bằng chứng |
|---|---|---|
| P2 — N5 nhận bảy mệnh đề trong blockquote chứa rào | Đóng | Bản 4 `rc=0`. Bản 5 `rc=1`, báo vùng không phải văn xuôi cấp ngoài cùng. |
| P2 — N5 nhận bảy mệnh đề trong code span hai backtick mở giữa dòng | Đóng | Bản 4 `rc=0`. Bản 5 `rc=1`, báo thiếu cả bảy mệnh đề. |
| P3 — Điểm chờ E2 ở §6 thiếu dữ liệu | Đóng | §6 đủ ba mục theo L7 và ADR-0067 cho việc đóng băng đặc tả: mức tiêu hao lấy từ biên nhận khi hỏi, một comment duyệt `spec_sha256` còn thiếu, và mục đích dùng băm để neo lease g1. Cụm “lượt approve sắp tới” là dự kiến. Mức đã dùng phải lấy từ biên nhận thực tế. |

H dựng từ đúng bảy mệnh đề §3 và H ngắt 60 cột đều `rc=0`, với danh sách mệnh đề thiếu và trường thừa đều rỗng. Cả 131 độ rộng nguyên từ 30 đến 160 cột đều xanh. Base và các đột biến lượt 2–4 chạy lại đều `rc=1`: đảo nghĩa mệnh đề 1/3/6, sửa byte YAML, CRLF, dời sai vùng, rào, thụt lề, comment HTML, blockquote, danh sách, tiêu đề ATX, code span bọc ngoài, sửa hoặc làm rỗng mệnh đề nhúng, và câu thêm có tên trường. Câu thêm không nhắc tên trường vẫn `rc=0` đúng giới hạn đã ghi. Diff của H thử chỉ thêm bảy mệnh đề §3.

### Finding mới

| Mức | Vị trí | Phản chứng và yêu cầu sửa |
|---|---|---|
| **P2** | N5 — đối chiếu chuỗi ngoài văn xuôi | Gọi `M` là bảy dòng §3 nối bằng dấu cách. Bốn ca đều cho N5 `rc=0`, thiếu `[]`, thừa `[]`: `Dẫn <span title='M'></span>.`, `Dẫn.` rồi dòng trống và `[ref]: /local "M"`, `M` rồi dòng `===`, và `Dẫn \| M` rồi dòng `--- \| ---`. `pandoc --sandbox -f gfm -t html` trả `rc=0` và xác nhận mệnh đề lần lượt nằm trong thuộc tính HTML, biến mất khỏi phần hiển thị, nằm trong `<h1>`, và nằm trong ô tiêu đề bảng. N5 cần xác nhận mệnh đề thuộc đoạn văn xuôi cấp ngoài cùng. Thêm cả bốn ca âm. |
| **P2** | N5 — ngắt dòng làm H hợp lệ đỏ oan | Thêm câu dẫn `Xem Issue #646.` trước mệnh đề 1 cho `rc=0`. Chỉ ngắt dòng ngay trước `#646.` thì `rc=1`, do `KHOI` chặn mọi dòng bắt đầu bằng `#`. Pandoc dựng hai bản thành cùng đoạn `<p>`. Ca này vi phạm cam kết ngắt dòng tự do ở §3 và L6(b). Thêm cặp ca dương và phân biệt dấu `#` trong văn xuôi với dấu mở tiêu đề ATX. |

Rà L1–L7: L1 có đơn vị đếm. L2 ánh xạ M1–M3 vào đúng một tệp. L3 có ca âm cho N1–N5, nhưng N5 còn lọt các ca trên. L4 ghi `khong_ap_dung` phù hợp. L5 có mốc đo, exact base và yêu cầu đo lại. L6 có đối chứng base/H, đối chiếu từng mệnh đề và mẫu theo vị trí cổng, nhưng còn hai finding P2. L7 có mã E2 và đủ dữ liệu cho điểm chờ duyệt băm, cùng khai báo phạm vi E4/E5. N1–N4 được rà ở mức đặc tả, chưa chạy toàn bộ gate trên một commit H. Issue và biên nhận từ xa chưa được xác minh trong phiên offline.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T05:35:54Z
