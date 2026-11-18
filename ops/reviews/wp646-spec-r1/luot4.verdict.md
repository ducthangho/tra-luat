## Review độc lập lượt 4 · Issue #646

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached tại đúng OID của `master`. Bản đặc tả đang review là tệp chưa track, SHA-256 `cba72fdafca8c6666c1ff2751ab6d804868e1ade61a1dbff55a97e6bbfc02935`. Reviewer OpenAI Codex qua phiên API hiện tại, giao verdict qua stdout. Model phục vụ cụ thể và trạng thái Issue từ xa chưa xác minh.

Đã diff với bản 3. Tôi trích nguyên script N5 từ bản sửa và chạy bằng `python3 -B -c` trên Linux, truyền từng bản sao qua `memfd`. Bảy dòng §3 khớp `MD_SHA`. Không gọi mạng hay ghi workspace. Các gate N1–N4 chưa chạy đầy đủ trên H.

| Finding lượt 3 | Trạng thái | Bằng chứng chạy lại |
|---|---|---|
| P2 · Mệnh đề ẩn trong HTML comment mở giữa dòng | **Đóng** | `Van dan <!-- … -->` trả `rc=1`, thiếu 7/7. H đủ bảy mệnh đề kèm comment không đóng cũng trả `rc=1`, báo lỗi comment. |
| P3 · Đầu vào mệnh đề rỗng | **Đóng** | `MD=()`, một dòng rỗng và đổi `360` thành `361` trong script đều trả `rc=1` tại chốt `MD_SHA`. |
| P3 · Thêm câu đảo nghĩa nhắc tên trường | **Đóng** | Thêm câu `` `heartbeat_at` tự kích hoạt thu hồi lease. `` vào H trả `rc=1`, đủ bảy mệnh đề nhưng có `heartbeat_at` ngoài mệnh đề. |

Base trả `rc=1`, thiếu 7/7. H trong đúng vùng và H ngắt lại ở 60 cột đều trả `rc=0`. CRLF toàn tệp, một byte CR trong YAML, sửa byte YAML, dời đoạn ra cuối tệp hoặc sang §5, dời vào khối mã cuối tệp, bọc rào backtick hoặc tilde, và thụt bốn dấu cách đều trả `rc=1`. Ba đột biến đảo nghĩa đều trả `rc=1`, lần lượt thiếu đúng mệnh đề 1, 3 và 6.

## Finding mới

| Mức | Finding | Cách sửa và ca khóa |
|---|---|---|
| **P2** | **N5 xanh khi cả bảy mệnh đề nằm trong mã.** Trong đúng vùng, bọc bảy dòng bằng rào `> ```text` và thêm `> ` vào từng dòng. N5 trả `rc=0`. Bọc cả bảy dòng trong một code span hai backtick mở giữa dòng cũng trả `rc=0`. `pandoc --sandbox -f gfm -t html` 3.1.3 xác nhận ca đầu ra `<blockquote><pre><code>`, ca sau nằm trọn trong `<code>`. N5 kiểm đầu dòng thô rồi tìm chuỗi con, nên cả hai ca vượt điều kiện văn xuôi của §3. | Sửa bước nhận dạng đoạn ở N5 để chỉ đối chiếu trong đoạn văn xuôi cấp ngoài cùng. Loại khối mã, quote và code span bao cả mệnh đề, đồng thời giữ các code span định danh mà §3 yêu cầu. Khóa bằng hai ca xanh giả trên và hai ca dương H gốc, H ngắt 60 cột. Chặn mọi backtick sẽ làm H hợp lệ đỏ oan. |
| **P3** | **Điểm chờ duyệt băm ở §6 thiếu dữ liệu E2.** Dòng cuối có mã E2 nhưng chưa ghi mức đã dùng, quyền còn thiếu và mục đích theo L7 và ADR-0067. | Bổ sung ba dữ liệu vào điểm chờ hiện có, hoặc dẫn rõ nơi yêu cầu duyệt phải ghi chúng. Rà riêng từng điểm hỏi để tránh biến việc bổ sung dữ liệu thành một lần xin duyệt nữa. |

Ca ghép `<!-- ghi chu -->` với rào mở trên cùng dòng trả `rc=1` khi có rào đóng riêng dòng. GFM hiển thị bảy câu dưới dạng đoạn văn và giữ marker mở dưới dạng chữ. Ca có dòng rào nằm hoàn toàn trong comment cũng trả `rc=1` dù GFM hiển thị đủ văn xuôi. Ca sau cho thấy thứ tự kiểm dòng thô có thể loại nội dung hiển thị đúng, nhưng nó vi phạm điều kiện hiện ghi ở N5(3). Chưa xác nhận ca đỏ oan thỏa toàn bộ điều kiện đó.

Giới hạn về câu thêm không nhắc tên trường **chấp nhận được với điều kiện §6 được thực hiện**. Câu “Ngưỡng ấy cũng áp cho mọi lease cũ.” thật sự trả `rc=0`. Với diff dự kiến 13–20 dòng, yêu cầu reviewer đọc toàn bộ vùng và xác nhận bằng chữ là khả thi. Điều đó vẫn để mở finding P2 về phép đo văn xuôi.

Rà nhanh L1–L7: **L1** có đơn vị đếm, **L2** ánh xạ M1–M3 vào đúng một tệp, **L3** N1–N5 đều có phản chứng, **L4** không áp dụng cho packet làm rõ tài liệu, **L5** số đo neo vào thời điểm và base, §6 yêu cầu đo lại, **L6** có cặp base/H, phép ngắt dòng và đếm theo từng mệnh đề, nhưng còn lỗ hổng P2. Tôi đo lại `heartbeat_at` trên sáu vị trí cổng, được 0 hit (`rc=1`), và trong hai glob Python được đúng một hit fixture (`rc=0`). **L7** có căn cứ cho trần gọi và khai E4/E5, còn thiếu dữ liệu E2 như trên.

KET_LUAN: request_changes
tokens used
69,115
## Review độc lập lượt 4 · Issue #646

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout detached tại đúng OID của `master`. Bản đặc tả đang review là tệp chưa track, SHA-256 `cba72fdafca8c6666c1ff2751ab6d804868e1ade61a1dbff55a97e6bbfc02935`. Reviewer OpenAI Codex qua phiên API hiện tại, giao verdict qua stdout. Model phục vụ cụ thể và trạng thái Issue từ xa chưa xác minh.

Đã diff với bản 3. Tôi trích nguyên script N5 từ bản sửa và chạy bằng `python3 -B -c` trên Linux, truyền từng bản sao qua `memfd`. Bảy dòng §3 khớp `MD_SHA`. Không gọi mạng hay ghi workspace. Các gate N1–N4 chưa chạy đầy đủ trên H.

| Finding lượt 3 | Trạng thái | Bằng chứng chạy lại |
|---|---|---|
| P2 · Mệnh đề ẩn trong HTML comment mở giữa dòng | **Đóng** | `Van dan <!-- … -->` trả `rc=1`, thiếu 7/7. H đủ bảy mệnh đề kèm comment không đóng cũng trả `rc=1`, báo lỗi comment. |
| P3 · Đầu vào mệnh đề rỗng | **Đóng** | `MD=()`, một dòng rỗng và đổi `360` thành `361` trong script đều trả `rc=1` tại chốt `MD_SHA`. |
| P3 · Thêm câu đảo nghĩa nhắc tên trường | **Đóng** | Thêm câu `` `heartbeat_at` tự kích hoạt thu hồi lease. `` vào H trả `rc=1`, đủ bảy mệnh đề nhưng có `heartbeat_at` ngoài mệnh đề. |

Base trả `rc=1`, thiếu 7/7. H trong đúng vùng và H ngắt lại ở 60 cột đều trả `rc=0`. CRLF toàn tệp, một byte CR trong YAML, sửa byte YAML, dời đoạn ra cuối tệp hoặc sang §5, dời vào khối mã cuối tệp, bọc rào backtick hoặc tilde, và thụt bốn dấu cách đều trả `rc=1`. Ba đột biến đảo nghĩa đều trả `rc=1`, lần lượt thiếu đúng mệnh đề 1, 3 và 6.

## Finding mới

| Mức | Finding | Cách sửa và ca khóa |
|---|---|---|
| **P2** | **N5 xanh khi cả bảy mệnh đề nằm trong mã.** Trong đúng vùng, bọc bảy dòng bằng rào `> ```text` và thêm `> ` vào từng dòng. N5 trả `rc=0`. Bọc cả bảy dòng trong một code span hai backtick mở giữa dòng cũng trả `rc=0`. `pandoc --sandbox -f gfm -t html` 3.1.3 xác nhận ca đầu ra `<blockquote><pre><code>`, ca sau nằm trọn trong `<code>`. N5 kiểm đầu dòng thô rồi tìm chuỗi con, nên cả hai ca vượt điều kiện văn xuôi của §3. | Sửa bước nhận dạng đoạn ở N5 để chỉ đối chiếu trong đoạn văn xuôi cấp ngoài cùng. Loại khối mã, quote và code span bao cả mệnh đề, đồng thời giữ các code span định danh mà §3 yêu cầu. Khóa bằng hai ca xanh giả trên và hai ca dương H gốc, H ngắt 60 cột. Chặn mọi backtick sẽ làm H hợp lệ đỏ oan. |
| **P3** | **Điểm chờ duyệt băm ở §6 thiếu dữ liệu E2.** Dòng cuối có mã E2 nhưng chưa ghi mức đã dùng, quyền còn thiếu và mục đích theo L7 và ADR-0067. | Bổ sung ba dữ liệu vào điểm chờ hiện có, hoặc dẫn rõ nơi yêu cầu duyệt phải ghi chúng. Rà riêng từng điểm hỏi để tránh biến việc bổ sung dữ liệu thành một lần xin duyệt nữa. |

Ca ghép `<!-- ghi chu -->` với rào mở trên cùng dòng trả `rc=1` khi có rào đóng riêng dòng. GFM hiển thị bảy câu dưới dạng đoạn văn và giữ marker mở dưới dạng chữ. Ca có dòng rào nằm hoàn toàn trong comment cũng trả `rc=1` dù GFM hiển thị đủ văn xuôi. Ca sau cho thấy thứ tự kiểm dòng thô có thể loại nội dung hiển thị đúng, nhưng nó vi phạm điều kiện hiện ghi ở N5(3). Chưa xác nhận ca đỏ oan thỏa toàn bộ điều kiện đó.

Giới hạn về câu thêm không nhắc tên trường **chấp nhận được với điều kiện §6 được thực hiện**. Câu “Ngưỡng ấy cũng áp cho mọi lease cũ.” thật sự trả `rc=0`. Với diff dự kiến 13–20 dòng, yêu cầu reviewer đọc toàn bộ vùng và xác nhận bằng chữ là khả thi. Điều đó vẫn để mở finding P2 về phép đo văn xuôi.

Rà nhanh L1–L7: **L1** có đơn vị đếm, **L2** ánh xạ M1–M3 vào đúng một tệp, **L3** N1–N5 đều có phản chứng, **L4** không áp dụng cho packet làm rõ tài liệu, **L5** số đo neo vào thời điểm và base, §6 yêu cầu đo lại, **L6** có cặp base/H, phép ngắt dòng và đếm theo từng mệnh đề, nhưng còn lỗ hổng P2. Tôi đo lại `heartbeat_at` trên sáu vị trí cổng, được 0 hit (`rc=1`), và trong hai glob Python được đúng một hit fixture (`rc=0`). **L7** có căn cứ cho trần gọi và khai E4/E5, còn thiếu dữ liệu E2 như trên.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T05:28:37Z
