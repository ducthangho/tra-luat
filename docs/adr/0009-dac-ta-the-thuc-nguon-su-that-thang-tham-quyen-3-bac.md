# ADR-0009 — Đặc tả thể thức là nguồn sự thật duy nhất; thang thẩm quyền 3 bậc khi nguồn lệch nhau

- **Trạng thái:** accepted (2026-07-21) — quyết định đã chốt, dây nối thi hành theo trình tự bên dưới.
- **Bối cảnh:** Giá trị thể thức (cỡ/kiểu/canh/thụt) đang được ghi ở BA nơi không đọc nhau: bảng
  `_tt_dac_ta()`, hằng số trong builder, hằng số trong bộ kiểm — đúng lớp bug "nhiều nguồn sự thật
  cùng ghi" mà ADR-0003 đã bác. Đo thực tế 2026-07-20: bộ kiểm chỉ bắt 1/5 đột biến vi phạm bảng;
  file test "0 finding" theo GHI_CHU thực chất có 2 finding thật + 1 vi phạm quy ước chưa có cờ.
  Tuyên bố chất lượng không được máy canh thì trôi im lặng. Hiệu năng KHÔNG phải yếu tố: đọc bảng
  1,1µs / lần kiểm 5ms mỗi file (đo in-process, 14 mẫu).
- **Quyết định 1 — nguồn sự thật:** `_tt_dac_ta()` trở thành nguồn sự thật duy nhất về trình bày
  từng thành phần × hệ; builder và bộ kiểm cùng ĐỌC bảng, không bên nào hard-code giá trị riêng.
  Trình tự thi hành bắt buộc, không đảo: (1) vá bảng → (2) khoá test 100% số ô → (3) nối builder
  → (4) đo "lũ finding" trên corpus thật → (5) nối bộ kiểm. Phạm vi: 3 hệ hiện có (hanh_chinh,
  vbqppl_qh, dang); hai hệ `vbqppl`/`vbhn` KHAI TRẮNG TƯỜNG MINH (bộ kiểm trả lời "chưa đặc tả",
  không giả vờ kiểm), lấp sau nếu có nhu cầu thật.
- **Quyết định 2 — thang thẩm quyền khi nguồn lệch nhau:** B1 văn bản gốc (NĐ30/NQ351/HD05 nguyên
  văn) thắng tuyệt đối → B2 reference có trích § cụ thể thắng code → B3 quy ước nội bộ: được dùng
  nhưng BUỘC mang nhãn "quy ước, không phải căn cứ pháp lý", cấm trà trộn với ô có căn cứ. Mỗi ô
  đặc tả phải tự khai bậc. Ô không xếp được bậc → cách ly (không dùng để build/kiểm), không đoán.
- **Quyết định 3 — mức nghiêm trọng buộc vào bậc thẩm quyền:** finding sinh từ ô B1/B2 khởi điểm
  **WARN**, chỉ thăng **FAIL theo từng ô** sau khi bước 4 xác nhận ô đó không cảnh báo oan trên corpus
  thật — quyền thăng do user duyệt từng ô, không tự động. Ô B3 sinh **INFO vĩnh viễn** — nguyên tắc:
  không đánh trượt văn bản của người khác bằng quy ước nội bộ của mình. Ô cách ly không sinh finding.
  Cờ viết tay hiện có giữ nguyên mức; lớp đặc tả chỉ cộng thêm. Chuẩn thăng FAIL = **zero-oan
  tuyệt đối**: mọi finding của ô trên corpus ngâm (111 file thật, diff với báo cáo nền 19-07, kế
  thừa phân lớp dự thảo) phải được đối chiếu tay xác nhận lỗi thật; MỘT cảnh báo oan → ô ở lại
  WARN kèm hồ sơ nguyên nhân. Bác ngưỡng tỷ lệ ("oan <X%") vì chi phí bất đối xứng: một lần đánh
  trượt oan trước Ủy ban đắt hơn mọi ô nằm lại WARN. Ô thiếu bằng chứng thăng ở WARN vô hạn — đó
  là kết cục đúng. Riêng 33 mẫu chuẩn + sản phẩm tự build kỳ vọng 0 finding lệch bảng: finding ở
  tầng này = builder↔bảng đá nhau = bug chặn tại bước 3-4, không phải chuyện thăng cấp.
- **Quyết định 4 — selftest đột biến hai chiều, gate GIỮ 9 bước:** bước 2 khoá bảng bằng CẢ HAI
  chiều: chiều thuận (builder sinh đúng ô khai — mở rộng r170 từ 28 lên 48/48 ô) và chiều nghịch
  (per-ô: phá thuộc tính trong docx mẫu in-RAM → bộ kiểm PHẢI kêu, không kêu = selftest đỏ).
  Chiều nghịch là máy-canh-cho-máy-canh: bằng chứng duy nhất rằng dây nối bảng→bộ kiểm còn sống
  sau refactor. Căn cứ thực nghiệm 2026-07-20: 5 đột biến tay → bộ kiểm hiện bắt 1/5. Đột biến là
  NỘI DUNG của bước selftest, không phải bước gate mới — cấu trúc gate 9 bước không đổi. Chi phí
  đo được: ~48 ô × 5ms ≈ +0,5s selftest.
- **Ca B3 đầu tiên đã phán:** lề phải văn bản nhà nước = 20mm (NĐ30 cho dải 15-20; chọn 20 vì mọi
  sản phẩm đã giao build ở 20mm — normalize sửa theo build để idempotent, không âm thầm đổi lề file
  cũ; và giữ khoảng cách nhận diện với hệ Đảng đơn trị 15mm). Dòng "le=…/15" ở §8 NEO sửa theo.
- **Tiến độ thi hành:** bước 1 ✅ r172 (v1.35.2) · bước 2 ✅ r173 (v1.35.3, sổ-hai-chiều) · bước 3
  ✅ r174 (v1.35.4 — **trục CỠ CHỮ** dẫn xuất từ bảng qua `_tt_co_build`, byte-identical; trục
  kiểu/canh/thụt vẫn inline trong builder nhưng bị r170+r173 khoá từ ngoài — nối nốt ở bước 5 nếu
  thực tế đòi) · bước 4 đo lũ ⏳ · bước 5 nối bộ kiểm ⏳.
- **Phương án đã bác:** giữ hiện trạng + đổi cách gọi tên (bảng chỉ là tài liệu) — bác vì chấp nhận
  vùng cố tình lệch ADR-0003 ngay tại vùng giao sản phẩm cho Ủy ban; nối thẳng bộ kiểm trước khi vá
  bảng — bác vì nối bảng đang sai vào bộ kiểm là sản xuất finding sai hàng loạt.
- **Hệ quả:** `the-thuc-check` sau bước 5 sẽ sinh finding mới trên file hôm nay "sạch" (kể cả bộ đã
  giao); bước 4 tồn tại để đo và duyệt cơn lũ đó TRƯỚC khi nối, chống lặp lại tiền lệ cảnh báo oan
  Quốc huy. GHI_CHU/tài liệu chỉ được tuyên bố "0 finding" khi có lệnh kiểm chạy lại được.
