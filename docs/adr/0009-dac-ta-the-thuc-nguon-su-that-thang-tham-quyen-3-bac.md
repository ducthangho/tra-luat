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
  thực tế đòi) · **bước 4 ✅ 2026-07-21** (đo lũ — kết quả + 5 quyết định Đ1-Đ5 bên dưới; hồ sơ
  `D:\Quốc hội\do-lu-2026-07-21\BAO-CAO-DO-LU-2026-07-21.md`) · **vòng 2 bước 1** vá bảng theo Đ2
  ✅ r175 (v1.35.5) · **bước 5 nối bộ kiểm ✅ r176 (v1.35.6, 2026-07-21) — TRÌNH TỰ 5 BƯỚC HOÀN TẤT**.
- **Bước 5 — thi hành (r176):** lớp đặc tả `_the_thuc_check_dac_ta` nối vào `the-thuc-check` sau T3,
  sinh finding `TT-DT-<Ô>-<CO|KIEU|CANH|THUT>`; parser production mở kênh `dt` per-đoạn (kế thừa
  style đủ tầng); classifier port NGUYÊN TRẠNG từ bộ kiểm nháp (6 bẫy oan đã vá giữ đủ) + vá oan
  mới lộ khi quét sổ: neo `thong_qua` siết theo công thức Đ36 k1 «<loại> này được Quốc hội … thông
  qua» (thân Lệnh công bố hết bị gán nhầm). Điều kiện Đ3/Đ4/Đ5 thi hành đúng nguyên văn (Đ4 nhường
  trọn `co` khối đầu ở MỌI hệ — chấp nhận kẽ hanh_chinh cờ tay chỉ đo bậc tương đối, hồ sơ trong
  docstring). Mức Đ1: B1/B2→WARN · B3→INFO · ô tin-cậy-thấp→INFO; không FAIL. Sổ `_BAT_DUOC` r173
  mở 1→51 ô đúng cơ chế tự-cưỡng-chế; 8 gap còn lại có hồ sơ tại comment r173. **Nghiệm thu** (129
  file, baseline @v1.35.5): tầng 1 qua PRODUCTION = 0 TT-DT tuyệt đối (19 NQ351 · 15 HD05 · builder);
  lớp A 876→856 — diff per-ô đúng 5 dòng, 100% quy về Đ4 (−9 TT-BAC-CO-CHU, −4 TT-CHUC-VU-DAM) và
  Đ5 (−7 trich_yeu·kieu); lớp B 3.905→0 (Đ3); lớp C 46→42. Chống-trùng kiểm tay: mỗi hiện tượng
  đúng MỘT finding cờ tay, không TT-DT trùng. Việc mở sau (không chặn ADR): nhận diện cong_van hệ
  Đảng chưa có tiêu chí máy (HD05 không dùng «V/v») — biến thể dang.cong_van chưa kích hoạt được
  từ bộ kiểm; trục kiểu/canh/thụt của builder vẫn inline (r170+r173 khoá ngoài, nối nốt nếu thực
  tế đòi).
- **Bước 4 — số liệu đo (bộ kiểm nháp NGOÀI repo, skill v1.35.4):** Tầng 1: sản phẩm builder tự
  dựng 4 hệ/biến thể = **0 finding** (trùng kết luận byte-match r174); 33 mẫu chuẩn = 15 finding,
  đối chiếu tay **không cái nào là lỗi mẫu — toàn bộ là khiếm khuyết của BẢNG** (thiếu ô câu ban
  hành/«Xét đề nghị»; nhóm CTN cỡ khác; ô không biểu diễn được ngoại lệ Mẫu 16; nhóm «kèm theo»
  chưa có ô; `dieu` đặc tả cấp đoạn trong khi HD05/NĐ30/NQ351 quy định cấp RUN). Tầng 2: 129 file
  thật, khớp 105/111 dòng báo cáo nền 19-07; lớp A (49 VB hoàn chỉnh) = **1.214 finding**, trong
  đó hai văn bản nền xếp «đạt chuẩn hoàn toàn» ăn 85 và 57 finding — bằng chứng chốt Đ1. Lớp phụ
  lục = 4.575 finding thì 4.403 rơi ô `than` (nhiễu thuần). Chính phiên đo bắt 6 nguồn cảnh báo
  oan của bản nháp (lũ 7.779 → 5.842 sau vá) — giá trị của «đo trước, phán sau».
- **Bước 4 — 5 quyết định user duyệt (2026-07-21, duyệt cả gói):**
  - **Đ1** — KHÔNG thăng FAIL ô nào vòng này; toàn bộ lớp đặc tả vào ở WARN (B3 → INFO). Không ô
    nào đạt zero-oan: ô đuôi dính cả văn bản đã phát hành, ô lớn đang oan vì bảng thiếu ô.
  - **Đ2** — quay bước 1 vá bảng TRƯỚC khi nối (thi hành r175): ô khối căn cứ đầy đủ (câu «… ban
    hành …», dòng «Xét/Theo đề nghị»), ô đề mục thân bài, ô trích yếu công văn V/v, biểu diễn
    ngoại lệ theo mẫu (Mẫu 16, nhóm CTN), đặc tả `dieu` cấp RUN.
  - **Đ3** — bước 5 CHỈ áp lớp đặc tả cho file nhận diện được khối đầu (có Quốc hiệu/tiêu đề
    Đảng); phụ lục/phụ biểu bỏ qua lớp này.
  - **Đ4** — chống báo trùng với cờ viết tay hiện có (TT-BAC-CO-CHU, TT-CHUC-VU-DAM,
    TT-CHUONG-CANH-GIUA, TT-KHOAN-DAM): một hiện tượng chỉ một finding.
  - **Đ5** — CÁCH LY `trich_yeu·kieu` (đậm,nghiêng vs đậm) chờ nguyên văn NĐ30 PL I II.5 — cùng
    giỏ với ca `QĐi` vs `QĐ` chờ HD05 3.2. Không đoán.
- **Vòng 2 bước 1 (r175) — nội dung vá bảng:** (a) vbqppl_qh +3 ô đo từ mẫu chuẩn B1:
  `cau_ban_hanh` (14 nghiêng, «Quốc hội ban hành Luật … .»), `co_quan_ban_hanh` (14 đậm giữa —
  dòng chủ thể «CHỦ TỊCH / NƯỚC CHXHCNVN», «ỦY BAN THƯỜNG VỤ QUỐC HỘI» sau trích yếu; tầng-1 lộ:
  3 finding chuc_vu_ky 14pt hoá ra bản nháp gán nhầm dòng này — chữ ký thật 13pt khớp bảng),
  `tu_lenh` (14 đậm giữa — «QUYẾT ĐỊNH:»/«NAY …:»); ô `can_cu` mở nghĩa gồm dòng «Xét/Theo đề
  nghị …». (b) `de_muc_than` hanh_chinh (B3 — NĐ30 không ấn định đề mục tự do; INFO vĩnh viễn)
  và dang (B2* — reference §5 TT-6 «đề mục: đậm»). (c) Bảng BIẾN THỂ MẪU mới
  `_tt_dac_ta_bien_the()` — trục thứ ba (mẫu/biến thể) chồng lên (thành phần × hệ): override
  Mẫu 16 quốc hiệu 13 (B1 sơ đồ); biến thể công văn hanh_chinh (ô 5b NĐ30: trích yếu V/v 12-13
  đứng, B2*) và dang (TT-5: 12 nghiêng, B2*) kèm `bo` tên loại/trích yếu; nhóm «kèm theo» (Mẫu
  6b/11b/14) VẪN CÁCH LY — chưa đủ căn cứ từng ô, production tiếp tục dùng `_kem_theo`/`_phu_luc`.
  (d) `dieu` cả 3 hệ: kiểu `dam` → **`dam:tien_to`** (văn phạm mới: thuộc tính áp cho TIỀN TỐ
  «Điều N.» + tên điều; nội dung inline sau đó phải Đứng — khớp r171 và cơ chế `dam_dau` builder).
  Chưa hệ nào đổi ngưỡng số ⇒ builder byte-identical (không đụng `_tt_co_build`/`_CHON`).
- **Phương án đã bác:** giữ hiện trạng + đổi cách gọi tên (bảng chỉ là tài liệu) — bác vì chấp nhận
  vùng cố tình lệch ADR-0003 ngay tại vùng giao sản phẩm cho Ủy ban; nối thẳng bộ kiểm trước khi vá
  bảng — bác vì nối bảng đang sai vào bộ kiểm là sản xuất finding sai hàng loạt.
- **Hệ quả:** `the-thuc-check` sau bước 5 sẽ sinh finding mới trên file hôm nay "sạch" (kể cả bộ đã
  giao); bước 4 tồn tại để đo và duyệt cơn lũ đó TRƯỚC khi nối, chống lặp lại tiền lệ cảnh báo oan
  Quốc huy. GHI_CHU/tài liệu chỉ được tuyên bố "0 finding" khi có lệnh kiểm chạy lại được.
- **Hậu kiểm 2026-07-21 (r177) — ĐÓNG GIỎ CÁCH LY «chờ nguyên văn»:** cả hai ca phân xử bằng
  nguyên văn B1 từ corpus, đúng trình tự «không đoán» của Đ5.
  - **Đ5 `trich_yeu·kieu`:** NĐ30 PL I II.5.b *«Trích yếu nội dung văn bản … trình bày bằng chữ
    in thường, cỡ chữ từ 13 đến 14, kiểu chữ đứng, đậm»* + HD05 PL2 mục 5 *«Trích yếu nội dung
    văn bản | In thường | 14-15 | Đứng, đậm»* ⇒ bảng GIỮ «dam», cách ly GỠ; «đậm,nghiêng» đo được
    trong thực chiến là lệch chuẩn thật. Mức INFO (trich_yeu thuộc nhóm tin-cậy-thấp Đ1 — chưa
    thăng FAIL, vẫn chờ duyệt zero-oan như mọi ô). Sổ r173 `_BAT_DUOC` 51→53 ô; test r176 (d)
    lật chiều: đậm+nghiêng PHẢI ra `TT-DT-TRICH-YEU-KIEU` INFO.
  - **Ca `QĐi` vs `QĐ` (cùng giỏ):** HD05 3.1.2.a *«Trường hợp chữ cái đầu các âm tiết của tên
    loại văn bản trùng nhau thì thống nhất ký hiệu một số tên loại văn bản như sau: Quyết định,
    Quy định: QĐ»* + ví dụ 3.1.2.b(ii) *«Quy định của UBKTTW — Số 23-QĐ/UBKTTW»*; `QĐi` không
    tồn tại trong toàn văn HD05. `ABBR_DANG` + §5.3 vốn đã đúng — sửa phía SẢN PHẨM:
    `Mau_Dang_05_Quy_dinh.docx` `-QĐi/ĐU` → `-QĐ/ĐU`. Đính chính hồ sơ: bảng viết tắt ở HD05
    **mục 3.1.2**, không phải 3.2 như ghi chú r176 (3.2 = kỹ thuật trình bày số-ký-hiệu).
