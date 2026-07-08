# ADR-0002 — bind(tl) copy-globals là giàn giáo di cư, không phải kiến trúc đích

- **Trạng thái:** Accepted (2026-07-09, phiên grilling)
- **Bối cảnh:** Pha B-E tách ~5.300 dòng từ tl.py (21.312 dòng) sang `tl_core/*`. Mỗi module nhận helper
  dùng chung của tl qua `bind(tl_module)` — copy mọi tên của tl vào globals() của module (bỏ tên đã có).
  Ưu điểm đã chứng minh: cắt AST-span NGUYÊN VĂN không phải rewrite tham chiếu, hàm tl là hàm thật nên
  không snapshot-stale, tách 4 pha không vỡ gate nào. Nhược điểm cố hữu: namespace ngầm — IDE/type-checker
  không thấy, người đọc module không biết tên đến từ đâu, lỗi tên-không-tồn-tại chỉ lộ lúc chạy.
  Đích dài hạn đã chốt: tl.py ≈ 2.500 dòng (facade), tiếp tục tách lõi cũ theo lộ trình test-first (I1…In).
- **Quyết định:** Hai giai đoạn.
  1. **Giai đoạn di cư (các pha I1…In):** tiếp tục dùng bind — nó là điều kiện làm extraction rẻ và an toàn.
     Ràng buộc giữ nguyên: module cấm đọc bare mutable-global của tl (khoá bằng test r61).
  2. **Giai đoạn tất toán:** khi helper dùng-chung đã dọn hết về các leaf-module trong tl_core (hết nguy cơ
     import vòng vì tl.py đã mỏng), chuyển DẦN từng module sang `from tl_core.x import y` tường minh;
     bind teo dần về 0. Đích cuối: 0 bind, type-check được toàn bộ tl_core.
- **Phương án đã loại:**
  - *Bind vĩnh viễn* — khoá luôn nhược điểm namespace ngầm vào kiến trúc đích.
  - *Explicit imports ngay từ giờ* — làm mỗi pha tách đắt gấp đôi và dễ sinh import vòng khi tl.py còn 19k dòng.
- **Hệ quả:** Trong giai đoạn di cư, mọi công cụ phân tích tĩnh phải hiểu quy ước bind (đã ghi ở docstring
  từng module). Thứ tự tất toán: leaf trước (deterministic/jsonio đã sẵn explicit), cụm nghiệp vụ sau.
