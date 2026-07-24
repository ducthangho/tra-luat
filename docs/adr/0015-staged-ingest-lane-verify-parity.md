# ADR-0015 — Lane STAGED: hoãn cổng chất lượng có kỷ luật + verify PARITY + bulk-flip corpus

- **Trạng thái:** Accepted (2026-07-24, r200/v1.35.31 — grill 24-07, user duyệt từng câu 6 quyết định C1-C6)
- **Bối cảnh:**
  - Nhu cầu người dùng (đo từ vận hành thật): lô docx chất lượng cao cần VÀO CORPUS nhanh nhất có thể;
    NLM chậm + hay chết là nguồn phương-sai lớn nhất của phiên nạp (babysit/chạy lại), còn cổng chất
    lượng per-file (đọc toàn văn canonical + verify_gate + quét Điều/chunk) là khoản call lớn nhất sau
    upload — scale theo cỡ file.
  - Hai ràng buộc doctrine phải giữ: CONTEXT.md «Ingest thành công» (dừng trước NLM ⇒ tài liệu chưa được
    nhận là corpus) và ADR-0004 «không được bỏ hậu điều an toàn để đạt ngân sách». Cửa sổ poison
    (dòng chưa-verify mà trích dẫn được) từng gây sự cố loại r182/P6 — không tái phạm.
  - Grill 24-07 bác phương án «corpus=true ngay + marker pending» (đắt: sửa mọi reader, bài học phạm vi
    23-07) và bác «verify nhẹ hơn» (đẻ hai loại verified trong cùng registry).
- **Quyết định:**
  1. **Phân loại cổng theo ADR-0004**: AN TOÀN = dedup tên/số hiệu (đo LIVE) + claim xuyên host +
     convert-readback (đã nằm trong `ingest_commit`, 0 call thêm) — GIỮ tại lúc nạp. CHẤT LƯỢNG = đọc
     toàn văn canonical + verify_gate + quét Điều-trùng/ngưỡng chunk — ĐƯỢC HOÃN, không được BỎ.
  2. **`profile-ingest --staged`** (v1 CHỈ profile-ingest — tiền lệ r198, ingest-local chờ soak): dừng
     ngay sau convert-readback; registry `corpus=false` + note `staged:pending;sq=<source_quality>`;
     KHÔNG đụng NLM. TỪ CHỐI pdf / source_quality=ocr / bảng tính (rc=2 trước side-effect) — phạm vi
     lane là docx digital; S1/PDF_IMAGE của lane thường nguyên vẹn.
  3. **`verify-staged` = VERIFY PARITY**: chạy ĐÚNG bộ cổng đã hoãn, không hơn không kém — lane đổi
     THỜI ĐIỂM kiểm, không đổi TIÊU CHUẨN (so được bằng test: hai lane cùng file phải cùng verdict).
     PASS → **bulk-flip** `corpus=true` + note thật (1 `reg_bulk` journaled — hạ tầng r197, undo cả lô);
     FAIL → Ở LẠI staged (note `staged:fail:<FLAG>`), KHÔNG auto-xóa, KHÔNG NLM, sửa xong đi lane
     thường từng file. File vượt ngưỡng chunk: vẫn flip, flag `needs_chunk_pipeline` — NLM phải đi
     pipeline chunk.
  4. **Flip TRƯỚC NLM, NLM tách hẳn**: sau flip, nạp NLM qua đường r192 giữ nguyên (van 1: ≤4 auto;
     >4 bảng tay khối ≤4 r199 + `nlm-reconcile`), nợ NLM theo dõi bằng `nlm_status` (ADR-0010).
     CONTEXT.md «Ingest thành công» thêm đúng MỘT ngoại lệ: đã qua verify parity thì corpus được flip
     dù NLM còn nợ.
  5. **Marker = cột note** (`staged:` prefix), KHÔNG thêm cột schema registry — tập dò tự thu hẹp khi
     PASS (note hết `staged:*`), re-run FAIL ghi lại cùng giá trị vô hại (idempotency_contract
     `verify_staged`).
- **Hệ quả:**
  - Corpus dùng được sớm hơn ~25-35% wall-clock trên lô docx (ước từ số 24-07 — PHẢI đo tươi), và quan
    trọng hơn: sự cố NLM ra khỏi đường găng nạp — hết babysit.
  - Trade-off chấp nhận: tài liệu staged KHÔNG trích dẫn được (corpus=false) tới khi verify PASS —
    chậm vài phút so với «true ngay», đổi lấy poison window = 0 và không sửa reader nào.
  - Nợ có chủ đích: ingest-local chưa có lane staged (chờ soak, mirror ADR-0014 #6); verify-staged đọc
    toàn văn tuần tự trong process (song song hoá là việc WP7 engine).
