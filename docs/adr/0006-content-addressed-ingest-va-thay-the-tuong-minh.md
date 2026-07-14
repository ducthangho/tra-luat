# ADR-0006 — Content-addressed ingest và thay thế tường minh

- **Trạng thái:** Accepted (2026-07-14, phiên audit ingest và tính tất định)
- **Bối cảnh:** Resume hiện có thể khớp theo tên và dùng lại Drive/NLM ID của một file khác; cache có thể chọn
  candidate “mới nhất” theo thứ tự filesystem. Tên không chứng minh nội dung, còn tự động chọn/ghi đè làm kết
  quả phụ thuộc thứ tự và có thể thay nhầm văn bản pháp luật.
- **Quyết định:**
  1. Identity ingest là `content_hash + target scope + canonical name + profile`; `plan_hash` ràng buộc identity
     này với toàn bộ tùy chọn thực thi. Resume chỉ khớp identity/plan chính xác, không fallback theo tên.
  2. Cùng identity là no-op sau readback. Cùng canonical name nhưng khác hash là conflict, không tự chọn bản
     mới nhất hoặc ghi đè. Thay thế phải chỉ rõ `--replace-source-id`, lập kế hoạch mới và xác nhận lại.
  3. Cache dùng content-addressed key: cùng hash được deduplicate; khác hash cùng canonical key là conflict.
     `verified` chỉ được đặt sau schema, provenance và quality gate; fallback chưa đủ bằng chứng giữ `staged`.
- **Phương án đã loại:**
  - *Khớp theo tên để resume thuận tiện* — đã tái hiện việc lấy nhầm upload ID khi hai nguồn trùng tên.
  - *Chọn candidate mới nhất* — thứ tự candidate không tất định và thời gian sửa không đại diện cho đúng nội dung.
  - *Tự ghi đè khi khác hash* — xóa mất ý định người dùng và không thể phân biệt cập nhật hợp lệ với nhầm nguồn.
- **Hệ quả:** Pipeline phải hash nguồn và mang identity qua journal/registry/cache; thao tác thay thế dài hơn một
  bước. Hash được tính đúng một lần mỗi run theo ngân sách hiệu năng. Đổi lại retry, resume và deduplicate có thể
  chứng minh đúng nguồn, còn xung đột không bị che bằng heuristic.
