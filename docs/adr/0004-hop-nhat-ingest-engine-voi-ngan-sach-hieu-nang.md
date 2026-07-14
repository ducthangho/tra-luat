# ADR-0004 — Hợp nhất các đường ingest bằng engine chung có ngân sách hiệu năng

- **Trạng thái:** Accepted (2026-07-14, phiên audit ingest và tính tất định)
- **Bối cảnh:** `ingest`, `ingest-local`, `profile-ingest`, ZIP và `ingest_to_cache.py` đang tự điều phối
  các bước ghi, readback, resume và báo lỗi. Các đường này đã drift: cùng một hậu điều có nơi fail-closed,
  có nơi báo thành công khi thiếu kết quả; identity và confirmation cũng không đồng nhất. Duy trì riêng từng
  luồng làm tăng lỗi, nhưng hợp nhất thiếu kiểm soát có thể tăng số API call và độ trễ.
- **Quyết định:**
  1. Dùng một ingest engine sở hữu state machine `plan → confirm → stage → write → readback → commit/journal`,
     identity, idempotency và quy tắc fail-closed. Adapter Drive/registry/NLM/cache chỉ sở hữu I/O.
  2. Giữ các entrypoint CLI hiện có dưới dạng adapter tương thích và chuyển tuần tự sang engine; `ingest` cũ
     có cảnh báo deprecation. Không chuyển đổi kiểu big-bang.
  3. `ingest_to_cache.py` chỉ được đọc/ghi cache; không tạo, chuyển đổi hoặc dọn tài liệu Drive ngầm.
  4. An toàn không cho phép bỏ readback bắt buộc để đổi lấy tốc độ. Hiệu năng được bảo vệ bằng memo hóa hash
     và metadata trong một run, batch các thao tác tương thích, đúng một readback cần thiết cho mỗi resource
     đã đổi, concurrency có giới hạn cho ZIP và benchmark có ngân sách phát hành. Cụ thể: hash mỗi nguồn đúng
     một lần mỗi run bằng streaming có bộ nhớ giới hạn; mỗi resource tối đa một write và một readback bắt buộc
     cho mỗi giai đoạn thành công (retry được đếm riêng); registry dùng bulk write khi ingest batch; ZIP mặc định
     4 worker và hợp nhất kết quả theo thứ tự canonical; contract test khóa số API call; median benchmark local
     không được chậm hơn baseline cùng máy quá 15%.
- **Phương án đã loại:**
  - *Tiếp tục vá riêng từng lệnh* — giữ nguyên nguyên nhân gây drift và nhân bản test/invariant.
  - *Hợp nhất big-bang* — phạm vi regression quá lớn và không có đường so sánh hành vi từng entrypoint.
  - *Giảm readback để đạt tốc độ cũ* — tái tạo lỗi thành công giả, trái quyết định fail-closed.
- **Hệ quả:** Parser, workflow cards, registry lệnh, journal và test phải được di trú đồng bộ; các script gọi
  apply trực tiếp phải thêm kế hoạch/xác nhận. Số API call có thể tăng ở luồng trước đây không readback, nhưng
  call trùng lặp phải bị loại và regression hiệu năng phải được đo ở gate thay vì suy đoán.
