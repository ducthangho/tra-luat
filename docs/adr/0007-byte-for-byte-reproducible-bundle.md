# ADR-0007 — Bundle tái tạo giống byte tuyệt đối, ưu tiên tính tất định hơn kích thước

- **Trạng thái:** Accepted (2026-07-14, phiên audit ingest và tính tất định)
- **Bối cảnh:** Manifest canonical có thể ổn định nhưng ZIP dùng DEFLATE vẫn có thể khác byte giữa phiên bản
  zlib/runtime. Verifier hiện còn có nhánh trả `ok=true` khi `package_hash` sai. Chỉ so nội dung logic không đủ
  để chứng minh artifact được giao chính là artifact đã kiểm thử.
- **Quyết định:**
  1. Bundle mang hai lớp định danh: `content_hash` của manifest canonical và `archive_sha256` của byte ZIP.
  2. Exporter dùng `ZIP_STORED`, cố định root name, thứ tự entry, timestamp, permission, platform flag và UTF-8
     metadata; loại cache, tệp tạm và thời gian build khỏi nội dung được hash.
  3. Release gate build hai lần và yêu cầu SHA-256 giống nhau. Mismatch manifest/package/archive luôn thất bại;
     chế độ strict chỉ quyết định việc chấp nhận tệp thừa, không được nới kiểm tra hash.
- **Phương án đã loại:**
  - *Giữ DEFLATE và chỉ cố định timestamp/thứ tự* — compressed bytes vẫn phụ thuộc implementation/runtime.
  - *Chỉ công bố content hash* — không chứng minh file ZIP được giao không bị đổi metadata hoặc thay byte.
  - *Cho non-strict bỏ qua package hash* — biến kiểm tra toàn vẹn thành advisory và đã tạo thành công giả.
- **Hệ quả:** Bundle lớn hơn nhưng đóng/mở nhanh hơn, dễ so sánh và tái tạo xuyên môi trường. Kênh phân phối phải
  lưu/công bố cả hai hash; mọi thay đổi metadata archive có chủ ý cũng tạo archive hash mới.
