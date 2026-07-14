# ADR-0005 — Môi trường chạy sở hữu source policy, ingest engine sở hữu bất biến toàn vẹn

- **Trạng thái:** Accepted (2026-07-14, phiên audit ingest và tính tất định)
- **Bối cảnh:** Skill phải chạy trên nhiều môi trường như Claude Chat, Claude Cowork, Codex và CLI, mỗi nơi có
  cơ chế cấp quyền/fetch khác nhau. Hard-code allowlist domain trong skill làm giảm tính di động và nhanh lỗi
  thời; ngược lại, để `ingest_to_cache.py` tự tải URL bất kỳ không giới hạn đã cho phép cả `file://` và làm mờ
  trách nhiệm kiểm soát nguồn.
- **Quyết định:**
  1. Môi trường chạy cung cấp `SourcePolicy` hoặc fetch adapter và quyết định host/scheme nào được phép. Skill
     portable không chứa allowlist domain cố định; standalone CLI có thể chọn policy qua config.
  2. Engine không thay thế chính sách mạng của môi trường, nhưng luôn cưỡng chế các bất biến độc lập với host:
     timeout, giới hạn byte/redirect, streaming, kiểm MIME/magic/hash, không để credential trong URL/log, dọn
     tệp tạm trong mọi nhánh và ghi provider/policy vào journal.
  3. Local file đi qua local-ingest thay vì giả dạng URL `file://`. Nếu môi trường không xác nhận quyền đọc nguồn
     thì engine fail-closed.
- **Phương án đã loại:**
  - *Hard-code allowlist domain trong skill* — không đáp ứng nhu cầu nhiều host và buộc phát hành lại chỉ để đổi
    chính sách của môi trường.
  - *Cho HTTP client trong script tải mọi URL trực tiếp* — bỏ qua quyền của host environment, giới hạn tài nguyên
    và provenance.
  - *Đưa toàn bộ kiểm tra cho môi trường* — môi trường cấp quyền truy cập không thay thế kiểm tra toàn vẹn, giới
    hạn bộ nhớ hoặc cleanup của pipeline ingest.
- **Hệ quả:** Mỗi môi trường cần adapter/policy rõ ràng và test contract; standalone CLI cần cấu hình policy.
  Đổi lại skill hỗ trợ host đa dạng mà không nhân bản chính sách mạng, còn output ingest vẫn có provenance và
  các bảo đảm toàn vẹn giống nhau.
