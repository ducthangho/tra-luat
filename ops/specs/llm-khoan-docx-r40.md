# LLM-KHOAN-DOCX r40: ranh giới khoản của `llm-khai-niem` từ cấu trúc danh sách đánh số .docx (đặc tả đóng băng)

- **Packet:** #1525. Revision 40, generation 1 (thay r39; r1–r39 giữ ở `ops/specs/llm-khoan-docx-r{1,…,39}.md`). Role `executor` (Claude), reviewer Codex. Review Class `sensitive` (write set
  chạm mã runtime trong gói phát hành: `scripts/tl_core/llm_route.py`, `scripts/tl_core/ops_misc.py`,
  `scripts/tl_core/command_registry.py`).
- **Căn cứ:** Issue #1525 (nợ K1 từ packet #1514, verdict lượt 10 `ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md`).
  Chủ kho trong phiên `session_015GtxrZQYT3Vt8PJdXrjEKg` ngày 25-11-2026: *"Tiếp đi"*, rồi chọn *"Do .docx numPr, cap 5"*. Sau
  lượt 5 (REQUEST_CHANGES E1–E6), chủ kho chọn *"Raise cap to 7, fix E1–E6"*: trần **7**. Sau lượt 6 (F1 P1: mọi luật cắt
  vùng Điều theo tiền tố đều bị đoạn trích giống tiêu đề đánh lừa), chủ kho chọn *"Docx must contain only that Article"*. Sau lượt 7 (G1–G2 P1, G3–G6 P2), chủ kho chọn
  *"Raise cap to 9, fix G1–G6"*: trần **9**. Sau lượt 9 (J1–J3 P1, J4–J5 P2), chủ kho chọn
  *"Raise cap to 11, fix J1–J5"*: trần **11**. Sau lượt 11 (L1–L2 P1, L3–L5 P2, L6 P3), chủ kho chọn
  *"Push first, then raise cap to 13 and fix L1–L6"*: đẩy `2c91832..fce28fd` TRƯỚC khi có approve (ngoại lệ M5 ADR-0060 do chủ kho
  duyệt, để không mất việc khi container bị thu hồi), trần **13**. Lượt 12 (M1 P1, M2 P2) sửa trong r13 theo cùng quyết định ấy,
  dùng lời gọi CUỐI (13/13); lượt 13 không approve ⇒ DỪNG và báo chủ kho (Review Rescue Checkpoint §12). Lượt 13 (N1 P1, N2 P2,
  N3 P1) REQUEST_CHANGES; tại checkpoint, executor đề xuất đổi chốt `ranh-gioi-khoan` sang CẤM TIỀN TỐ, chủ kho chọn *"Chọn 1"*
  (nâng trần lên **14**, vá N1–N3); nhánh đẩy `fce28fd..fe2d9e8` trước khi vá (giữ việc). Lượt 14 (Q1 P1, Q2 P2)
  REQUEST_CHANGES; chủ kho lại chọn *"Chọn 1"* (nâng trần lên **15**, vá Q1–Q2); nhánh đẩy `fe2d9e8..f5201db` trước khi vá.
  Lượt 15 (R1 P1, R2–R3 P2) REQUEST_CHANGES; executor đề xuất đổi lớp biên ký tự từ chuẩn hoá sang TỪ CHỐI, chủ kho chọn *"Chọn 1"*
  (nâng trần lên **16**); nhánh đẩy `f5201db..8fb9c29` trước khi vá. Lượt 16 (S1 P1, S2–S3 P2) REQUEST_CHANGES; executor đề xuất
  đảo sang danh sách cho phép, chủ kho chọn *"Tôi chọn 1"* (nâng trần lên **17**); nhánh đẩy `8fb9c29..cab5044` trước khi vá.
  Lượt 17 (T1 P1, T2 P2) REQUEST_CHANGES; chủ kho trao quyền ĐỨNG: *"Tiếp tục. Cho phép tự nâng trần, vá theo lớp lỗi cho tới khi
  hết P1, P2 là ít nhất, hết P3 thì tốt"* ⇒ trần **18**, các lượt sau executor tự nâng trần theo quyền ấy; nhánh đẩy
  `cab5044..3781842` trước khi vá. Lượt 18 (U1 P1, U2 P2) REQUEST_CHANGES ⇒ r19 theo quyền đứng ấy (trần **19**); nhánh đẩy
  `3781842..eea72e1` trước khi vá. Lượt 19 (V1–V3 P1, V4 P2) REQUEST_CHANGES; với đường `<số hiệu>` chủ kho chọn *"Giữ đường, chặn
  markup + khai giới hạn"* (V1 chặn bằng `--markup-strict`, V3 khai giới hạn) ⇒ r20 (trần **20**); nhánh đẩy `eea72e1..e1c3015`.
  Lượt 20 (W1/W2/W5 P1, W3/W4 P2) REQUEST_CHANGES; với W1/W3 (bộ đọc dùng chung `tl extract`) chủ kho chọn *"Giữ đường, khai thêm
  giới hạn"* ⇒ r21 (trần **21**); nhánh đẩy `8a685fe..8689b60`. Lượt 21 (X1–X2 P1, X3 P2) REQUEST_CHANGES ⇒ r22 theo quyền đứng
  (trần **22**); nhánh đẩy `8689b60..343b413`.
  Lượt 22 (Y1–Y2 P1, Y3 P2) REQUEST_CHANGES ⇒ r23 theo quyền đứng (trần **23**); nhánh đẩy `343b413..39f2f88`.
  Lượt 23 (Z1–Z2 P1, Z3–Z4 P2) REQUEST_CHANGES ⇒ r24 theo quyền đứng (trần **24**); nhánh đẩy `39f2f88..db06b9c`.
  Lượt 24 (A1 P1, A2 P2) REQUEST_CHANGES ⇒ r25 theo quyền đứng (trần **25**); nhánh đẩy `db06b9c..cc05cb6`.
  Lượt 25 APPROVE với 0 P1, còn B1–B3 P2; chủ kho đòi hết P2 ⇒ r26 theo quyền đứng (trần **26**); nhánh đẩy `cc05cb6..0ae38e9`.
  Lượt 26 APPROVE với 0 P1, còn C1–C2 P2 ⇒ r27 theo quyền đứng (trần **27**); nhánh đẩy `0ae38e9..8a69d6a`.
  Lượt 27 APPROVE với 0 P1, còn D1 P2 ⇒ r28 theo quyền đứng (trần **28**); nhánh đẩy `8a69d6a..cda9439`.
  Lượt 28 APPROVE với 0 P1, còn E1 P2 ⇒ r29 theo quyền đứng (trần **29**); nhánh đẩy `cda9439..599b90c`.
  Lượt 29 (F2 P1, F1 P2) REQUEST_CHANGES ⇒ r30 theo quyền đứng (trần **30**); nhánh đẩy `599b90c..3bfed5f`.
  Lượt 30 (G1 P1, G2 P2) REQUEST_CHANGES ⇒ r31 theo quyền đứng (trần **31**); nhánh đẩy `3bfed5f..a9cf415`.
  Lượt 31 (H1 P1, H2–H3 P2) REQUEST_CHANGES ⇒ r32 theo quyền đứng (trần **32**); nhánh đẩy `a9cf415..f5ce6a2`.
  Lượt 32 APPROVE với 0 P1, còn I1–I2 P2 ⇒ r33 theo quyền đứng (trần **33**); nhánh đẩy `f5ce6a2..38a01cf`.
  Lượt 33 APPROVE với 0 P1, còn J1–J2 P2 ⇒ r34 theo quyền đứng (trần **34**); nhánh đẩy `38a01cf..7042aa1`.
  r35: vá theo LỚP ba lớp P2 của lượt 34 (bộ quét nhãn đầu dòng chung · ngân sách đọc nguồn · kiểm ký tự mọi đoạn) — §2.37.
  r36: Review Rescue §12 — danh sách CHO PHÉP đầu dòng thay danh sách cấm nhãn; ngân sách đọc theo lượt 35 — §2.38.
  r37: khai giới hạn nhãn điểm số trùng số khoản (chủ kho) và khoá vào pham_vi_kiem; ngân sách theo lượt 36 — §2.39.
  r38: danh sách cho phép đòi TỪ TRỌN (chặn nhãn gõ tay chữ tiếng Việt); ngân sách extract/ZIP/bộ đếm theo lượt 37 — §2.40.
  r39: khai giới hạn nhãn nhiều vế (chủ kho) + khoá pham_vi_kiem; ZIP đếm entry thật; bộ chạy extract giữ hạn chót — §2.41.
  r40: thực thi trọn thu hẹp miền nhãn nhiều vế; ZIP64 locator tuyệt đối; hạn chót một nguồn; hai P3 — §2.42.
- **Nền:** nhánh `ccr-89c0d2e2-inanqb` (PR #1517) — packet #1514 r9 (`fcb12b3`) đã dừng ở đó, chưa merge; packet này làm tiếp trên
  CÙNG nhánh và thay lease r9 của #1514 (bia mộ hai chiều). Baseline nghiệm thu `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master).

## 1. Bất biến giữ nguyên
- Kết quả luôn mang `can_nguoi_duyet: true`; `pham_vi_kiem` nói đúng nguồn ranh giới (thô hay cấu trúc).
- Không đổi đường gọi model (`goi`, `duong_api`, `duong_sub`, `_chay_co_moc`). Không thêm cờ CLI mới.
- Điều 3 Luật 134/2025/QH15 (nguồn mất số, 8 khoản một dòng) và ba kết quả đã lưu vẫn đạt 8/8.
- Mọi luật chặn của #1514 r9 trên đường thô giữ nguyên, packet chỉ THÊM điều kiện từ chối ở đường thô.

## 2. Hành vi mới
### 2.1 Đường cấu trúc `.docx` (`llm_route.doc_dieu_docx`, `llm_route.doc_dieu_cau_truc`)
Chỉ thư viện chuẩn (zipfile + ElementTree); đọc thành phần zip qua `read_member_bounded` khi nạp được.
- Lọc markup dự thảo bằng `docx_markup.strip_markup(xml, "strip")` TRƯỚC khi phân tích (như `tl extract`).
- Bộ đếm số chạy theo thứ tự tài liệu theo từng `numId` (`start`, `startOverride`; đặt lại cấp con khi cấp cha tăng). Nhãn
  điểm dựng từ `lvlText` + `numFmt` (`decimal`, `lowerLetter`, `upperLetter`; `bullet` ⇒ `-`).
- Định vị Điều: đúng MỘT đoạn mở bằng `Điều <N>` + `.`/`:`; vùng kết thúc ở đoạn `Điều <số>…` kế tiếp hoặc `Chương|Mục|Phần`.
- Cấp khoản = cấp nhỏ nhất trong các đoạn đánh số của vùng, danh sách khoản = `numId` của đoạn đánh số đầu tiên; định dạng
  cấp khoản phải `decimal`. Đoạn cấp con CÙNG danh sách ⇒ điểm của khoản đang mở (`<nhãn> <chữ>`); đoạn không số mở bằng
  `a)`/`-`/`–`/`•`/`+` sau khoản đầu ⇒ điểm gõ tay của khoản đang mở. Số khoản = số Word hiển thị, phải liên tục từ 1.
- `KhongCauTruc` (mang `van_ban` = chữ của Điều, mỗi đoạn một dòng) khi vùng không có đoạn đánh số tự động ⇒ người gọi lùi về
  đường thô.
- `ValueError` (DỪNG, rc 2) khi: không đúng một tiêu đề Điều; đoạn không số giữa các khoản (không phải điểm gõ tay); bảng
  trong vùng; đoạn đánh số qua style (không có `w:numPr` trực tiếp); số gõ tay trong đoạn đánh số tự động; đoạn đánh số
  thuộc danh sách khác hoặc cấp con trước khoản đầu; số khoản không liên tục từ 1; `lvlOverride` ngoài `startOverride`;
  `numFmt` ngoài danh sách; cấp khoản không `decimal`; đoạn không số trước khoản đầu không phải ĐÚNG MỘT câu dẫn chuẩn
  `_RE_CAU_DAN_TRON` (hoặc vắng).
- `lech_nguyen_van(khai_niem, van_ban, khoan=None)` và `tach_khai_niem(..., khoan=None)`: khi có `khoan` (từ cấu trúc) thì so
  với nó thay cho `tach_khoan(van_ban)`.
### 2.2 CLI `tl llm-khai-niem --tep <tệp>`
- Tệp có chữ ký zip (`PK\x03\x04`) ⇒ đường `.docx`; cần `--dieu N`, không kèm số hiệu (rc 2). Cấu trúc mơ hồ ⇒ rc 2.
  `KhongCauTruc` ⇒ đường thô trên chữ của Điều. `pham_vi_kiem` = `PHAM_VI_KIEM_CAU_TRUC` khi ranh giới từ cấu trúc.
- Tệp khác ⇒ đường văn bản UTF-8 như cũ. Đường `<số hiệu>` (qua `tl extract`) giữ là văn bản thô.
### 2.3 Đường văn bản thô (đóng K1)
`tach_khoan`: BẤT KỲ dòng điểm (`_RE_DIEM`) nào ⇒ None ở MỌI loại nguồn (thay §2.12 của #1514 r9 chỉ áp nguồn mất số); dòng
mở bằng "là" không còn là tiếp dòng (lượt 4 Q3 của #1503) ⇒ ở nguồn có số rơi xuống nhánh "dòng không số" ⇒ None. Đường thô
chỉ nhận khoản ĐÚNG MỘT DÒNG. Giới hạn đã khai: khoản có điểm và tiếp dòng không đọc được từ văn bản thô.

## 2.4 Bổ sung r2 (cross-review lượt 1 — `ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md`) — THAY các điểm tương ứng của §2.1
- **A1 vùng Điều:** duyệt khối theo thứ tự tài liệu, đi vào `w:sdt`/`w:customXml`; đoạn trong bảng vẫn được ĐẾM; bảng, đoạn
  trong bảng hay khối lạ trong vùng ⇒ ValueError, kiểm TRƯỚC khi lùi về đường thô. Tiêu đề Điều có ngắt dòng mềm hoặc được
  đánh số tự động ⇒ ValueError. Đoạn mở bằng `Điều …`/`Chương|Mục|Phần` mà được đánh số tự động ⇒ ValueError (không coi là
  ranh giới).
- **A2 số Word:** numPr HIỆU LỰC = trực tiếp đè style (theo chuỗi `basedOn`); đoạn đánh số qua style được ĐẾM và đọc như đoạn
  có numPr trực tiếp (thay chốt "chặn style" của §2.1). `w:start` vắng ⇒ 0 (mặc định OOXML). `w:lvlRestart`, `w:isLgl`,
  `numStyleLink`/`styleLink` ⇒ danh sách không hỗ trợ. Nhãn cấp khoản phải `decimal` VÀ `lvlText` đúng `%N.` hoặc `%N)` của chính
  cấp ấy.
- **A3 từ nối:** khoản từ cấu trúc mang `đầu khoản` (chữ đoạn mở khoản); `lech_nguyen_van` dò từ nối CHỈ trong đầu khoản.
- **A4 markup:** sau `strip_markup`, chữ còn gạch ngang (theo namespace — mọi tiền tố; theo `rStyle`/`pStyle` qua `basedOn`) hoặc
  còn `w:del`/`w:delText`/`w:moveFrom` trong vùng ⇒ ValueError. Sửa đổi dấu đoạn (`pPr/rPr` chứa `del`/`ins`/`moveFrom`/`moveTo`)
  ở BẤT KỲ đâu trong tài liệu ⇒ ValueError.
- **A5 phạm vi xác thực:** định nghĩa danh sách không hỗ trợ chỉ chặn khi Điều đích dùng danh sách ấy; nhãn chỉ dựng trong vùng.
- **A6 điểm gõ tay:** dấu điểm có thể dính thân (`a)tổ chức`, `-tổ chức`).
- **A7 test:** mỗi chốt trên một mẫu và một đột biến riêng; `startOverride` đo với giá trị khác `start` gốc; ca dương điểm gõ tay.
- **A8:** hướng dẫn đường thô chỉ còn quy tắc một dòng.

## 2.5 Bổ sung r3 (cross-review lượt 2 — `ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md`) — THAY điểm tương ứng §2.1/§2.4
Đổi sang DANH SÁCH CHO PHÉP ở mức phần tử: con của `w:p` (`pPr`, `r`, bookmark/comment/perm/proofErr; đi vào `ins`/`moveTo`/
`hyperlink`/`smartTag`/`customXml`) và con của `w:r` (`rPr`, `t`, `tab`→khoảng trắng, `noBreakHyphen`→`-`, `softHyphen`→rỗng,
`br`/`cr`→ngắt mềm, `lastRenderedPageBreak`/`commentReference`/`annotationRef` bỏ qua). Phần tử khác ⇒ đoạn "lạ".
- **B1:** tiêu đề Điều phải khớp `_RE_TIEU_DE_TRON` trên CẢ đoạn (như đường thô); đoạn ranh giới có chữ đã bỏ/phần tử lạ ⇒ chặn;
  trong vùng: ngắt dòng mềm, đoạn lạ, đoạn đánh số rỗng ⇒ chặn — tất cả kiểm TRƯỚC khi lùi về đường thô.
- **B2:** bảng duyệt theo hàng/ô đúng một lần (bảng lồng); `w:lvl/w:pStyle` ⇒ danh sách không hỗ trợ; khối lạ TRƯỚC Điều ⇒ chặn;
  đoạn TRONG Điều đánh số qua style (không có `numId` trực tiếp) ⇒ chặn (giới hạn đã khai; THAY ca dương style của §2.4 A2) —
  đánh số qua style ngoài Điều vẫn được đếm.
- **B3:** gạch đơn và gạch kép tính RIÊNG qua docDefaults → style đoạn (style đoạn mặc định khi vắng `pStyle`) → style ký tự →
  định dạng trực tiếp; một trong hai còn bật trên chữ ⇒ chặn.
- **B4:** `w:noBreakHyphen` là chữ `-`; phần tử hiển thị chưa hiểu (`w:sym`, trường, hình, chú thích…) ⇒ chặn.
- **B5:** số gõ tay `^\(?\d+\s*[.)](?!\d)` — thân mở bằng số thập phân không bị chặn.
- **B6:** `w:customXmlPr`/`w:sdtPr`/`w:sdtEndPr` là thuộc tính wrapper, bỏ qua.
- **B7:** mỗi chốt một mẫu + một đột biến riêng; ca `ca_cau_truc_docx_bang_truoc_lui` đo riêng thứ tự chốt bảng trước fallback.
- **B8:** hướng dẫn cập nhật theo phạm vi style thực tế.

## 2.6 Bổ sung r4 (cross-review lượt 3 — `ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md`) — THAY điểm tương ứng
- **C1 điểm cắt:** đoạn mở bằng `Điều X.` chỉ là ranh giới khi X là Điều KẾ TIẾP (N+1, hoặc cùng N với hậu tố chữ lớn hơn);
  `Điều X.` khác giữa vùng ⇒ ValueError. Tiêu đề đích có ngắt mềm ⇒ ValueError (kể cả khi chữ khớp mẫu). Đoạn ranh giới có
  chữ đã bỏ, phần tử lạ, hay ngắt mềm ⇒ ValueError (ba chốt riêng).
- **C2 bộ đếm:** trong bảng, hàng/ô bọc trong `w:sdt`/`w:customXml` được duyệt đúng thứ tự, một lần; phần tử lạ trong bảng ⇒ khối
  lạ. Nhãn chữ `lowerLetter`/`upperLetter` kiểu Word: a…z, aa…zz, aaa… (lặp một chữ).
- **C3 dấu phân cách:** mọi đoạn trong vùng qua cùng chốt `_dong_mo_ho` với đường thô (điểm gõ tay bỏ dấu điểm trước khi đo).
- **C4 gạch toggle:** trong chuỗi style (docDefaults, style đoạn, style ký tự, theo `basedOn`), bật ở BẤT KỲ tầng nào ⇒ coi là bật;
  chỉ định dạng TRỰC TIẾP trên run mới tắt tuyệt đối.
- **C5:** `w:sdt` NỘI DÒNG đi vào `w:sdtContent` (bỏ `sdtPr`/`sdtEndPr`); thiếu nội dung ⇒ phần tử lạ.
- **C6:** mỗi chốt một mẫu có nguyên nhân từ chối duy nhất + một đột biến riêng (`numStyleLink` và `styleLink` tách; la/ngắt/chữ
  đã bỏ ở ranh giới tách).
- **C7:** hướng dẫn nêu cả `%N.` và `%N)`.

## 2.7 Bổ sung r5 (cross-review lượt 4 — `ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md`) — THAY điểm tương ứng
- **D1:** Điều KHÔNG có đánh số tự động ⇒ ValueError (BỎ lùi về đường thô `KhongCauTruc` của §2.1/§2.2 — điểm cắt của Điều không
  đánh số chỉ có bằng chứng tiền tố). Có đoạn nào thuộc danh sách khoản (`numId` của khoản) Ở SAU điểm cắt ⇒ ValueError.
- **D2:** `abstractNum` có `restartNumberingAfterBreak` bật ⇒ danh sách không hỗ trợ.
- **D3 (THAY A4/B3/C4 về chữ gạch ngang):** đọc XML GỐC, KHÔNG qua `docx_markup.strip_markup` (regex có thể nuốt ranh giới đoạn).
  Chữ của run có gạch đơn/gạch kép hiệu lực (tính như §2.6 C4) ⇒ BỎ khỏi nguyên văn; `w:del`/`w:delText`/`w:moveFrom` ⇒ bỏ;
  `w:ins`/`w:moveTo` ⇒ giữ. Không còn chặn vì "chữ gạch ngang còn sót". Sửa đổi dấu đoạn vẫn ⇒ ValueError.
- **D4:** tiêu đề đích có phần tử lạ ⇒ ValueError (chốt riêng); phần tử lạ ở cấp hàng/bảng trước Điều ⇒ khối lạ ⇒ ValueError.
- **D5:** gốc `document.xml` không phải `w:document` Transitional (vd Strict) ⇒ ValueError có chẩn đoán — giới hạn đã khai.
- **D6:** chốt dấu phân cách gỡ dấu điểm CHỈ ở đoạn có vai trò điểm gõ tay.

## 2.8 Bổ sung r6 (cross-review lượt 5 — `ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md`) — THAY điểm tương ứng
- **E1 điểm cắt:** đoạn ranh giới (`Điều X.` kế tiếp hoặc `Chương|Mục|Phần …`) phải DUY NHẤT trong tài liệu (khoá = tiền tố tiêu đề,
  so không phân biệt hoa thường, ngoài bảng) và không kết bằng `:`/`;` — nếu không ⇒ ValueError.
- **E2 gạch toggle (THAY §2.6 C4):** đếm số tầng bật (docDefaults + chuỗi style đoạn + chuỗi style ký tự): 0 ⇒ không gạch, 1 ⇒ gạch
  (bỏ chữ), ≥2 ⇒ không giải được ⇒ đoạn lạ (chặn nếu trong Điều). Định dạng trực tiếp trên run là tuyệt đối.
- **E3:** hàng có `w:trPr/w:del|w:ins`, ô có `w:tcPr/w:cellDel|cellIns|cellMerge` ⇒ khối lạ (chặn nếu trước/trong Điều).
- **E4:** `w:tcPr` khác là thuộc tính ô hợp lệ, bỏ qua.
- **E5:** test khoá riêng việc đọc XML gốc (không qua `strip_markup` — regex của nó gộp hai đoạn khi run rỗng tự đóng đứng trước run
  gạch; lỗi ấy nằm ở `scripts/docx_markup.py`, ngoài write set, ghi nợ) và việc bỏ chữ trong `w:moveFrom`.
- **E6:** `ilvl` ngoài 0–8 ở định nghĩa/override ⇒ danh sách không hỗ trợ; ở đoạn ⇒ đoạn lạ, không đếm.

## 2.9 Bổ sung r7 (cross-review lượt 6 — `ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md`) — THAY các điểm tương ứng
- **F1 (THAY mọi luật định vị/cắt vùng §2.1, §2.4 A1, §2.5 B1/B2, §2.6 C1, §2.7 D1, §2.8 E1):** tệp chỉ chứa ĐÚNG Điều cần đọc.
  Đoạn có nội dung ĐẦU TIÊN của tài liệu phải là tiêu đề `Điều <N>` (khớp `_RE_TIEU_DE_TRON`, không đánh số, không ngắt mềm, không
  phần tử lạ); vùng = toàn bộ phần sau tới hết tài liệu. Có đoạn mở bằng `Điều …`/`Chương|Mục|Phần …` trong vùng ⇒ ValueError.
  Bảng hay khối lạ ở BẤT KỲ đâu ⇒ ValueError (không còn duyệt ô bảng để đếm — §2.5 B2/§2.6 C2/§2.8 E3–E4 hết đối tượng).
- **F2:** đoạn không số sau khoản đầu ⇒ ValueError, kể cả điểm gõ tay (THAY §2.4 A6): điểm phải là cấp con tự động cùng danh sách.
  Chốt dấu phân cách đo nguyên chữ mọi đoạn (THAY §2.7 D6).
- **F3:** `numId`/`abstractNumId` (định nghĩa, style, đoạn) chuẩn hoá về số nguyên thập phân; trùng sau chuẩn hoá ⇒ danh sách không
  hỗ trợ.
- **F4:** bộ đếm số thứ tự vượt 999 ⇒ ValueError (phủ cả `start`/`startOverride` lớn).
- **F5:** `ilvl` ngoài 0–8 ở `lvlOverride` có ca + đột biến riêng; chốt `ilvl` ở ĐOẠN bỏ (thừa: đoạn chỉ được đếm khi cấp có trong định
  nghĩa đã giới hạn 0–8, và bước xác thực chặn cấp không định nghĩa).
- **F6:** `w:ptab` ⇒ khoảng trắng; mốc `moveFrom/ToRangeStart/End` được bỏ qua khi CÂN theo `id` toàn tài liệu, lẻ ⇒ ValueError.

## 2.10 Bổ sung r8 (cross-review lượt 7 — `ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md`) — THAY điểm tương ứng
- **G1:** ID (`numId`, `abstractNumId`) chỉ hợp lệ khi là chữ số thập phân ASCII; không hợp lệ ⇒ định nghĩa không ghép được, đoạn trỏ ID
  ấy ⇒ đoạn lạ. Đoạn ở cấp `il` khi một cấp tổ tiên `< il` CHƯA có mục ⇒ ValueError (nhảy cấp); bộ đếm không còn khởi tạo cấp tổ tiên
  từ `start`.
- **G2:** part numbering/styles lấy theo `word/_rels/document.xml.rels` (loại quan hệ `…/numbering`, `…/styles`); không có tệp quan
  hệ ⇒ tên mặc định; quan hệ trỏ ra ngoài, nhiều quan hệ cùng loại, hay part vắng ⇒ ValueError.
- **G3:** hết đối tượng — không còn khởi tạo tổ tiên (G1); mọi giá trị bộ đếm đi qua trần 999.
- **G4:** `w:br` có `w:type="page|column"` là ngắt trình bày (khoảng trắng), không phải ngắt dòng mềm.
- **G5:** đột biến riêng cho điểm gõ tay dạng gạch và cho chuẩn hoá `abstractNumId`.
- **G6:** tiêu đề đích so không phân biệt hoa thường (như `_RE_TIEU_DE_TRON`).

## 2.11 Bổ sung r9 (cross-review lượt 8 — `ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md`) — THAY điểm tương ứng
- **H1:** nhận diện tiêu đề `Điều …` trong vùng KHÔNG phân biệt hoa thường (như tiêu đề đích).
- **H2:** part chính theo quan hệ `officeDocument` của `_rels/.rels` (vắng tệp ⇒ `word/document.xml`; vắng quan hệ/part ⇒
  ValueError); quan hệ numbering/styles đọc từ tệp quan hệ CỦA part chính.
- **H3:** ca riêng + đột biến riêng cho điểm gõ tay dạng gạch, chuẩn hoá `abstractNumId`, part numbering đổi tên.
- **H4:** `numId` lỗi khai qua style được giữ dấu riêng (khác vắng) ⇒ đoạn dùng style ấy là đoạn lạ.
- **H5:** ngắt trang/cột chỉ được nhận khi KHÔNG có chữ sau nó trong đoạn; có chữ sau ⇒ như ngắt dòng mềm (chặn).

## 2.12 Bổ sung r10 (cross-review lượt 9 — `ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md`) — THAY điểm tương ứng
- **J1:** style (theo `basedOn`) mang BẤT KỲ thuộc tính đánh số nào (`numId` hay `ilvl`) ⇒ đoạn đánh số dùng style ấy là "đánh số qua
  style" ⇒ chặn trong Điều, kể cả khi `numId` khai trực tiếp.
- **J2:** phần tử ngoài namespace `w` (vd `mc:AlternateContent`) trong `rPr` của run, trong `pPr`/`numPr` của đoạn ⇒ đoạn lạ; trong
  `rPr`/`pPr` của styles.xml ⇒ ValueError.
- **J3:** `lvlText` chỉ được gồm placeholder `%N` và dấu (không chữ cái) ⇒ nhãn sinh tự động không mang được tiền tố tiêu đề.
- **J4:** ca riêng + đột biến cho việc đọc tệp quan hệ CỦA part chính đã đổi tên.
- **J5:** quy tắc "chữ sau ngắt trang/cột" chỉ tính chữ CÒN HIỆU LỰC (run không gạch).

## 2.13 Bổ sung r11 (cross-review lượt 10 — `ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md`) — THAY điểm tương ứng
- **K1 (THAY §2.12 J2):** BẤT KỲ phần tử namespace markup-compatibility (`mc:`) ở đâu trong part chính, styles hay numbering ⇒ ValueError.
- **K2:** tiêu đề cấu trúc nhận cả số thứ tự viết bằng chữ (`Chương|Mục|Phần` + La Mã | số | `thứ <từ>` | một chữ hoa).
- **K3 (THAY §2.12 J3):** `lvlText` (khác `bullet`) phải khớp TOÀN CHUỖI danh sách cho phép: ít nhất một `%1`–`%9`, ngoài ra chỉ `.` `)`
  `(` `-` `–` và khoảng trắng.
- **K4:** §3 sửa mô tả ca dương theo hợp đồng một Điều.

## 2.14 Bổ sung r12 (cross-review lượt 11 — `ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md`) — THAY điểm tương ứng
- **L1:** kiểu quan hệ so ĐÚNG URI đầy đủ Transitional `http://schemas.openxmlformats.org/officeDocument/2006/relationships/<loại>`.
- **L2:** trong vùng, đoạn mở bằng `Điều <số>` mà CẢ đoạn không kết bằng dấu câu (`.` `;` `:` `,` `!` `?`) là tiêu đề thiếu dấu ⇒ chặn.
- **L3:** `Chương|Mục|Phần` (không phân biệt hoa thường) + số thứ tự: La Mã VIẾT HOA | số | `thứ` + từ số (nhất…mười) | một chữ HOA.
- **L4:** giá trị số nguyên OOXML (`start`, `startOverride`) vắng/sai dạng ⇒ ValueError; `lvlText` thiếu `w:val` ⇒ chuỗi rỗng ⇒ bị
  danh sách cho phép chặn.
- **L5:** part chính đưa BYTES cho parser XML (tự đọc khai báo mã hoá).
- **L6:** hướng dẫn `lvlText` nêu đủ dấu cho phép và ngoại lệ `bullet`.

## 2.15 Bổ sung r13 (cross-review lượt 12 — `ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md`) — THAY điểm tương ứng
- **M1 (THAY §2.14 L2):** tiền tố và hậu tố xét RIÊNG. Trong vùng, đoạn mở bằng `Điều <số>[chữ]` theo sau KHÔNG phải chữ/số
  (khoảng trắng, gạch, hết đoạn…) là tiêu đề thiếu dấu ⇒ chặn, TRỪ KHI đoạn kết bằng dấu câu (`.` `;` `:` `,` `!` `?`), cho phép
  ngoặc/nháy đóng và khoảng trắng phía sau dấu ấy. Dấu câu GIỮA tên Điều không còn làm đoạn thoát chốt.
  Giới hạn đã khai (không phân biệt được bằng hình dạng): tiêu đề thiếu dấu sau số mà lại KẾT bằng dấu câu (`Điều 4 Phạm vi.`) trông
  y hệt dẫn chiếu trong điểm (`Điều 5 của Luật này.`) — hợp đồng một Điều mỗi tệp (§2.9) là chốt cho ca này.
- **M2 (mở rộng §2.14 L4):** mọi thuộc tính cấp/ID đọc dạng số đi qua `_so_nguyen`/kiểm vắng: `w:ilvl` của đoạn (vắng/sai dạng ⇒
  ValueError); `w:ilvl` của style (lỗi ⇒ chỉ chặn khi đoạn dùng style ấy CÓ đánh số); `w:ilvl` của `lvl`/`lvlOverride` và
  `start`/`startOverride` lỗi ⇒ định nghĩa mang `loi`, chặn KHI DÙNG (A5); mốc `moveFrom/moveTo Range*` thiếu `w:id` ⇒ ValueError.
  Không `TypeError` nào thoát ra handler CLI.

## 2.16 Bổ sung r14 (cross-review lượt 13 — `ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md`) — THAY điểm tương ứng
- **N1 (THAY §2.15 M1, §2.14 L2, §2.11 H1):** Review Rescue Checkpoint §12 — bỏ việc NHẬN DIỆN hình dạng tiêu đề. Trong thân Điều,
  đầu đoạn được chuẩn hoá (NFC, bỏ mọi ký tự không phải chữ/số ở đầu — nháy, gạch dưới, ký hiệu); đầu đoạn mở bằng `Điều`
  (`Đ` U+0110 hoặc `Ð` U+00D0, không phân biệt hoa thường) + khoảng trắng tuỳ ý + chữ số ⇒ ValueError, BẤT KỂ ký tự sau số hay
  dấu câu cuối đoạn. `Chương|Mục|Phần` (§2.14 L3) dò trên CÙNG đầu đoạn đã chuẩn hoá. Cái giá đã khai: điểm/khoản MỞ BẰNG dẫn
  chiếu `Điều 5 …` bị chặn (rc 2, không ghép sai); dẫn chiếu giữa đoạn và thuật ngữ `Điều kiện …` (không có số) vẫn đạt.
- **N2:** ID danh sách (`numId`, `abstractNumId`, kể cả qua style) chuẩn hoá bằng CHUỖI (bỏ số 0 đầu), không qua `int()` — ID dài
  bất kỳ ở định nghĩa không dùng không làm hỏng lần đọc (A5).
- **N3 (bổ sung §2.9):** khối con của `body`/`sdtContent`/`customXml` so QName ĐẦY ĐỦ; phần tử ngoài namespace WordprocessingML
  (kể cả trùng tên cục bộ `p`/`tbl`/`sdt`/`customXml` hay tên trong `_KHOI_BO_QUA`) ⇒ khối lạ ⇒ chặn.

## 2.17 Bổ sung r15 (cross-review lượt 14 — `ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md`) — THAY điểm tương ứng
- **Q1 (THAY cách chuẩn hoá đầu đoạn của §2.16 N1):** mọi phép dò tiền tố cấu trúc (`Điều <số>`, `Chương|Mục|Phần`) chạy trên MỘT
  bản chiếu: NFC → bỏ mọi ký tự định dạng Unicode `Cf` (zero-width, soft hyphen…) → mọi ký tự không phải chữ/số (kể cả gạch
  dưới, dấu câu) thành khoảng trắng → gộp khoảng trắng. Chốt số gõ tay (§2.1) dò trên chữ đã NFC + bỏ `Cf` + bỏ khoảng trắng đầu.
  Bản chiếu chỉ để DÒ; nguyên văn đưa model và phép so giữ chữ gốc. Giới hạn đã khai: chữ đồng hình khác hệ chữ (vd Cyrillic) không
  được ánh xạ.
- **Q2:** hướng dẫn không khuyên sửa câu chữ văn bản nguồn để lách chốt; Điều có điểm/khoản mở bằng dẫn chiếu `Điều <số>` phải
  tách khái niệm thủ công.

## 2.18 Bổ sung r16 (cross-review lượt 15 — `ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md`) — THAY điểm tương ứng
- **R1/R3 (THAY phần chuẩn hoá Unicode của §2.17 Q1; Review Rescue Checkpoint §12):** không chuẩn hoá nữa mà TỪ CHỐI. Chữ được coi là
  KHÔNG đọc an toàn khi không ở dạng NFC hoặc chứa ký tự thuộc nhóm Unicode `Cf` (định dạng: zero-width, soft hyphen, BOM giữa chừng,
  điều khiển hướng chữ), `Mn`/`Mc`/`Me` (dấu tổ hợp còn dư sau NFC, bộ chọn biến thể), `Cc`, `Co`, `Cs`, `Cn`.
  · `.docx`: mọi đoạn trong thân Điều như vậy ⇒ ValueError (tiêu đề đã qua danh sách cho phép nguyên đoạn `_RE_TIEU_DE_TRON`).
  · Văn bản thô (`tach_khoan`): BẤT KỲ dòng nào (sau BOM đầu tệp) như vậy ⇒ None (từ chối cả nguồn).
  Bản chiếu dò tiền tố (§2.17) chỉ còn bước "ký tự không phải chữ/số thành khoảng trắng". Giới hạn đã khai: nguồn hợp lệ mang ký tự
  vô hình (vd soft hyphen trong HTML gốc) bị chặn; chữ đồng hình khác hệ chữ không được ánh xạ.
- **R2 (THAY mẫu số gõ tay §2.5 B5):** dạng ngoặc KÍN `(<số>)` ở đầu đoạn đánh số là số gõ tay bất kể ký tự theo sau; `(?!\d)` chỉ bảo vệ
  số thập phân của dạng `<số>.` / `<số>)`.

## 2.19 Bổ sung r17 (cross-review lượt 16 — `ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md`) — THAY điểm tương ứng
- **S1 (THAY §2.18 R1/R3; Review Rescue Checkpoint §12):** DANH SÁCH CHO PHÉP ký tự thay cho danh sách cấm nhóm Unicode. Chữ của Điều
  chỉ được gồm: U+0020–U+007E; nguyên âm tiếng Việt `aăâeêioôơuưy` (hoa/thường) × {không dấu, huyền, sắc, ngã, hỏi, nặng} dạng dựng
  sẵn; `đ` `Đ`; U+00C0–U+00FF trừ `×` `÷` (Latin-1); NBSP U+00A0; tab; và `“ ” ‘ ’ – — … « » § ° ± × ÷ ≤ ≥ € ₫ ‰ • · № ¹ ² ³`.
  Xuống dòng `\n` `\r` chỉ được ở văn bản thô. Ký tự khác ⇒ `.docx`: ValueError; văn bản thô: `tach_khoan` trả None. Dấu tổ hợp tách
  rời nằm ngoài danh sách nên không cần kiểm NFC riêng. Giới hạn đã khai: nguồn hợp lệ mang ký tự ngoài danh sách (chữ Hán, Kirin,
  ký hiệu toán khác, khoảng trắng Unicode khác NBSP) bị chặn — nới danh sách khi gặp ca thật.
- **S2:** kiểm trên chữ GỐC: `.docx` — chữ ghép từ run TRƯỚC khi gộp khoảng trắng, áp cho cả tiêu đề; văn bản thô — toàn văn TRƯỚC
  `splitlines`/`strip`, `tach_khoan` bỏ ĐÚNG MỘT BOM đầu văn bản; CLI `--tep` giải mã `utf-8-sig` (một BOM) rồi chỉ strip khoảng trắng
  ASCII. `lvlText` chỉ nhận dấu cách thường làm khoảng trắng.
- **S3:** `w:permStart`/`w:permEnd` cấp đoạn đã nằm trong danh sách bỏ qua (`_CON_DOAN_BO_QUA`) từ r3; r17 thêm ca dương khoá hành vi.

## 2.20 Bổ sung r18 (cross-review lượt 17 — `ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md`) — THAY điểm tương ứng
- **T1:** MIỀN CHỮ SỐ của mọi chốt cú pháp (tiền tố `Điều <số>`, số thứ tự `Chương|Mục|Phần`, số gõ tay) = chữ số ASCII + `¹²³` —
  số mũ được đổi về chữ số thường TRƯỚC khi dò (`_chieu_so`); nguyên văn giữ số mũ. `¹²³` là các ký tự chữ số DUY NHẤT ngoài ASCII
  trong danh sách cho phép (§2.19).
- **T2:** đường thô có MỘT tầng gỡ BOM (`_bo_mot_bom`, dùng bởi `tach_khoan` và chốt CLI). CLI `--tep` giải mã `utf-8` thường và chỉ
  strip khoảng trắng ASCII; trước khi gọi model, văn bản thô có ký tự ngoài danh sách cho phép (sau đúng một BOM) ⇒ rc 2, KHÔNG
  gọi model. `lay_dieu_qua_extract` chỉ bỏ dòng mốc của `tl extract` và khoảng trắng ASCII. Giới hạn đã khai: `extract_dieu`
  (`extract_cache.py`, ngoài write set, bộ đọc dùng chung của `tl extract`) vẫn `strip()` biên của Điều — ký tự lạ ở ĐÚNG hai đầu
  Điều do bộ đọc ấy cắt không tới được chốt; ký tự ở biên không dịch được ranh giới khoản bên trong.

## 2.21 Bổ sung r19 (cross-review lượt 18 — `ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md`) — THAY điểm tương ứng
- **U1 (THAY §2.20 T1):** `¹²³` RA KHỎI danh sách cho phép (§2.19). Mọi chữ số tới được chốt cú pháp (`.docx` lẫn văn bản thô) đều là
  chữ số ASCII nên `\d` đồng nhất ở mọi chốt; bỏ phép chiếu số mũ. Cái giá đã khai: văn bản có số mũ (`m²`…) bị chặn.
- **U2 (bổ sung giới hạn §2.20 T2, theo quyền revision chủ kho trao):** đường `<số hiệu>` dùng đầu ra của `tl extract` — bộ đọc DÙNG
  CHUNG (`extract_cache.py`, ngoài write set) làm sạch TOÀN văn bản xuất ra TRƯỚC khi lưu cache: xoá ký tự điều khiển C0 trừ `\t`
  `\n` `\r`, xoá DEL, thay surrogate lẻ, `strip()` biên Điều. Ký tự đã bị xoá/thay ở tầng ấy KHÔNG tới được chốt của
  `llm-khai-niem` và không để lại tín hiệu (snapshot cache đã sạch). Đây là GIỚI HẠN ĐÃ KHAI của đường thô `<số hiệu>` (vốn đã mang
  `pham_vi_kiem` thô và `can_nguoi_duyet: true`); đường có ranh giới chắc chắn là `--tep <tệp .docx>`.

## 2.22 Bổ sung r20 (cross-review lượt 19 — `ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md`) — THAY điểm tương ứng
- **V1:** `lay_dieu_qua_extract` gọi `tl extract … --markup-strict`: nguồn mà `tl extract` không chứng minh được đã lọc markup dự thảo
  ⇒ rc 3, không in chữ ⇒ ValueError ⇒ CLI rc 2 TRƯỚC model. Cái giá đã khai: nguồn chỉ đọc được qua text/plain bị chặn. Trạng thái
  markup của snapshot cache do `tl extract` quyết (sidecar chứng nhận của nó).
- **V2:** `docDefaults/pPrDefault/pPr/numPr` có mặt trong styles ⇒ ValueError (bộ đọc không giải số kế thừa từ mặc định đoạn). Cái giá
  đã khai: chặn cả khi mọi đoạn tự khai đánh số trực tiếp.
- **V3 (GIỚI HẠN ĐÃ KHAI, quyết định chủ kho):** đường `<số hiệu>` nhận Điều do `extract_dieu` (bộ đọc dùng chung, ngoài write set) cắt
  theo mốc regex đầu dòng `Điều <số>`; một dòng dẫn chiếu mở bằng `Điều <số>` làm mất các khoản sau nó, phép so không thấy được.
  Đường này vẫn mang `pham_vi_kiem` thô + `can_nguoi_duyet: true`; ranh giới chắc chắn chỉ có ở `--tep <tệp .docx>`.
- **V4 (THAY `_RE_DIEM`):** nhãn điểm của nguồn thô = `a)` · `(a)` · `a.` (một chữ cái thường) · `-` `–` `•` `+` ở đầu dòng — mọi nguồn
  có dòng như vậy ⇒ `tach_khoan` None. Cùng mẫu dùng cho `_tu_noi` (dò từ nối chỉ trước dòng điểm đầu tiên).

## 2.23 Bổ sung r21 (cross-review lượt 20 — `ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md`) — THAY điểm tương ứng
- **W1 + W3 + phần `<số hiệu>` của W2 (GIỚI HẠN ĐÃ KHAI, quyết định chủ kho):** đường `<số hiệu>` tin trạng thái markup do `tl extract`
  báo: bộ lọc của nó chỉ xét gạch TRỰC TIẾP trên run (chữ gạch qua style có thể lọt dù `--markup-strict` cho qua), `--markup-strict`
  chặn cả bản export sạch không có dấu sửa và bản consolidated, bộ chuyển XML→chữ của nó có thể bỏ `w:tab`/`w:br`. Đường này mang
  `pham_vi_kiem` thô + `can_nguoi_duyet: true`; nguyên văn chắc chắn chỉ có ở `--tep <tệp .docx>`. Thông báo trần CAP chỉ đường `.docx`
  (không còn gợi ý `tl cache-build`, vốn cũng đi `--markup-strict`).
- **W2 (đường `.docx`, chính sách r222 của `docx_markup`):** run gạch hiệu lực, hay `w:del`/`w:moveFrom`, mà ruột CHỈ có khoảng trắng ⇒
  GIỮ khoảng trắng ấy (không để hai từ hai bên dính lại); ruột có chữ ⇒ bỏ như cũ.
- **W4 (THAY `_RE_DIEM` §2.22):** nhãn điểm thô = `x)` · `(x)` · `x.` với `x` là MỘT chữ cái lặp lại ≥1 lần (thường hoặc hoa: `a`, `aa`,
  `B`, `BB`) · `-` `–` `•` `+`.
- **W5 (bổ sung A5):** hai `w:lvl` cùng `ilvl`, hay hai `lvlOverride` cùng `ilvl`, trong một định nghĩa ⇒ `loi` ⇒ chặn KHI DÙNG.

## 2.24 Bổ sung r22 (cross-review lượt 21 — `ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md`) — THAY điểm tương ứng
- **X1 (mở rộng §2.23 W2, chính sách r222 `chunk_payload`):** ruột của `w:del`/`w:moveFrom` đọc theo chữ HIỂN THỊ — `t`/`delText` theo
  chữ, `tab`/`ptab`/`br`/`cr` là khoảng trắng, `noBreakHyphen` là `-` — rồi mới xét "chỉ khoảng trắng". `delText` lạc trong run thường
  mà chỉ có khoảng trắng ⇒ giữ. Run gạch đã quy `tab`/`br` về khoảng trắng từ trước.
- **X2 (TRƯỜNG ĐƠN TRỊ):** phần tử con mà bộ đọc lấy bằng phần tử ĐẦU phải xuất hiện ≤ 1 lần. Part chính: `p/pPr`, `r/rPr`,
  `pPr/{pStyle,numPr,rPr}`, `numPr/{numId,ilvl}`, `rPr/{rStyle,strike,dstrike}`; styles: `style/{basedOn,pPr,rPr}`, `pPr/numPr`,
  `numPr/{numId,ilvl}`, `rPr/{strike,dstrike}`, `docDefaults/{rPrDefault,pPrDefault}`, `rPrDefault/rPr`, `pPrDefault/pPr` — vi phạm ⇒
  ValueError cả tệp (cái giá đã khai: kể cả style không dùng). numbering: `lvl/{start,numFmt,lvlText,lvlRestart,isLgl,pStyle}`,
  `num/abstractNumId` — vi phạm ⇒ `loi` của định nghĩa, chặn KHI DÙNG (A5).
- **X3 (mở rộng `_RE_DIEM` §2.23 W4):** thêm nhãn `x-` / `x –` (chữ cái đơn/lặp, thường/hoa, có thể một dấu cách trước gạch) khi sau
  gạch là khoảng trắng; từ ghép `e-mail` không khớp.

## 2.25 Bổ sung r23 (cross-review lượt 22 — `ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md`) — THAY điểm tương ứng
- **Y1 (THAY phần run gạch của §2.23 W2 / §2.24 X1):** run gạch hiệu lực, `w:del`, `w:moveFrom` dùng CÙNG phép đọc ruột (`_ruot_bi_bo`:
  `t`/`delText` theo chữ, `tab`/`ptab`/`br`/`cr` là khoảng trắng, `noBreakHyphen` là `-`). Ruột CHỈ khoảng trắng ⇒ giữ khoảng trắng; ruột
  có chữ (kể cả `delText`) ⇒ bỏ TRỌN, không giữ phân cách nằm trong mẩu đã bỏ.
- **Y2 (mở rộng §2.24 X2):** nút CHỌN VÙNG và khoá style cũng đơn trị: `document/body`, `sdt/{sdtPr,sdtEndPr,sdtContent}` ≤ 1; `w:sdt`
  (khối hay nội dòng) phải có `sdtContent` và chỉ có con trong {`sdtPr`, `sdtEndPr`, `sdtContent`} — sai ⇒ khối/đoạn lạ ⇒ chặn; hai
  style cùng `styleId` ⇒ ValueError.
- **Y3 (THAY `_RE_DIEM`):** NGỮ PHÁP nhãn điểm thô, cùng miền với `_nhan`: `( x )` · `(x.` `x.` `x)` · `x-` `x –` (sau gạch là khoảng trắng) với
  `x` là một chữ cái lặp ≥1 lần, thường/hoa, và khoảng đệm ngang (dấu cách, tab, NBSP) giữa các phần; nhãn thập phân nhiều cấp (`1.1.`,
  `1.2`); `-` `–` `•` `+`.

## 2.26 Bổ sung r24 (cross-review lượt 23 — `ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md`) — THAY điểm tương ứng
- **Z1 (THAY phép đọc ruột §2.25 Y1, DANH SÁCH CHO PHÉP):** trong ruột run gạch / `w:del` / `w:moveFrom`, chỉ `tab`/`ptab`/`br`/`cr` là
  khoảng trắng, `t`/`delText` theo chữ, `noBreakHyphen` là `-`, `softHyphen` và con bỏ qua của run (`rPr`…) không tính; MỌI con khác của
  run (ký hiệu `w:sym`, trường, hình…) và mọi con không phải run của wrapper tính là NỘI DUNG ⇒ mẩu bị bỏ TRỌN.
- **Z2:** gói `.docx` có tên member TRÙNG trong thư mục ZIP ⇒ ValueError (cả gói, trước khi đọc part nào).
- **Z3 (mở rộng `_RE_DIEM` §2.25 Y3):** nhãn thập phân nhiều cấp có thể trong ngoặc và dính thân: `(1.1)`, `1.1.`, `1.2)`, `1.1.Dữ…`.
- **Z4 (§3):** ca riêng cho từng trường đơn trị metadata của content control (`sdtPr`, `sdtEndPr`) kèm đột biến bỏ đúng trường ấy.

## 2.27 Bổ sung r25 (cross-review lượt 24 — `ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md`) — THAY điểm tương ứng
- **A1 (quy tắc Word, cùng r222):** chữ của `w:t`/`w:delText` lấy theo `xml:space` HIỆU LỰC (kế thừa từ tổ tiên; `default` đặt lại): không
  `preserve` ⇒ bỏ khoảng trắng XML (dấu cách, tab, CR, LF) ở HAI BIÊN của phần tử. Áp cho chữ còn hiệu lực, `delText` lạc và ruột bị bỏ
  (run gạch / `w:del` / `w:moveFrom`) — một phép đọc chung (`_chu_t`).
- **A2 (mở rộng `_RE_DIEM` §2.26 Z3):** nhãn thập phân nhiều cấp có thể kết bằng `-` / `–` (`1.1-`, `1.2 –`).

## 2.28 Bổ sung r26 (cross-review lượt 25 — `ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md`, APPROVE còn 3 P2) — THAY điểm tương ứng
- **B1 (THAY `_RE_DIEM`, miền nhãn = miền `_nhan`):** nhãn điểm thô = các placeholder (số thập phân, hoặc một chữ cái lặp thường/hoa) nối
  bằng `.` / `-` / `–` (có khoảng đệm ngang), mở bằng `(` tuỳ chọn, và kết bằng: `.` hoặc `)` (thân có thể dính); `-`/`–` khi sau là khoảng
  trắng hay dấu mở trích dẫn/ngoặc (`“` `"` `‘` `'` `(`); hoặc — chỉ với nhãn số nhiều cấp — ngay sau chữ số khi sau là khoảng trắng, chữ
  cái hay dấu mở trích dẫn/ngoặc. Cộng dấu đầu dòng `-` `–` `•` `+`. NGOÀI MIỀN (giới hạn đã khai, thuộc bước duyệt ranh giới): nhãn
  chỉ ngăn bằng khoảng trắng (`a tổ chức`) không phân biệt được với chữ; từ ghép `e-mail`, viết tắt `Tp.` không khớp.
- **B2 (§3):** ca riêng cho `xml:space="default"` đặt lại kế thừa, ruột bị bỏ và `delText` lạc đọc theo `xml:space` hiệu lực — mỗi tính
  chất một đột biến.
- **B3:** trạng thái ngắt của đoạn (ngắt mềm; "đã có ngắt trang/cột") chỉ ghi SAU khi biết run còn hiệu lực — ngắt nằm trong run gạch
  bị bỏ trọn không làm cả Điều bị từ chối; ngắt còn hiệu lực vẫn chặn như §2.5.

## 2.29 Bổ sung r27 (cross-review lượt 26 — `ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md`, APPROVE còn 2 P2) — THAY điểm tương ứng
- **C1 (THAY tuyên bố miền của §2.28 B1):** dấu nối giữa hai placeholder = MỌI dấu `lvlText` cho phép (`.` `)` `(` `-` `–`, có đệm ngang).
  Miền nhãn nhận diện = các nhãn `_nhan` có ít nhất một dấu trong tập ấy; nhãn chỉ ngăn bằng khoảng trắng nằm ngoài miền (giới hạn đã
  khai). TRƯỚC nhánh số khoản, `tach_khoan` từ chối CẢ nguồn khi có dòng mở bằng số NHIỀU CẤP ở bất kỳ dạng nào (`_RE_NHIEU_CAP`:
  `(`? chữ số, dấu nối có đệm, chữ số — `1.1`, `1. 1`, `1(1)`, `1-1`, `(1.2)`), ở cả nguồn có số và mất số. Cái giá đã khai: khoản mà
  thân mở bằng một số (`2. 1 năm là …`, `1.5 lần là …`) bị chặn.
- **C2:** cờ "phần tử chưa hiểu" của run chỉ ghi vào đoạn SAU khi biết run còn hiệu lực — ký hiệu nằm trong run gạch bị bỏ trọn không
  làm cả Điều bị từ chối; ký hiệu còn hiệu lực vẫn chặn.

## 2.30 Bổ sung r28 (cross-review lượt 27 — `ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md`, APPROVE còn 1 P2) — THAY điểm tương ứng
- **D1 (THAY `_RE_NHIEU_CAP` §2.29 C1):** MỘT ngữ pháp nhãn NHIỀU THÀNH PHẦN ở đầu dòng, xét TRƯỚC mọi cửa nhận số đơn (`tach_khoan`
  từ chối cả nguồn). Placeholder = số, hoặc chữ cái lặp ĐỨNG RIÊNG (không dính chữ cái khác). Dạng: số + (một hay nhiều dấu `.` `)` `(`
  `-` `–`, có đệm) + số (`1.1`, `1. 1`, `1(1)`, `1).1`); số + dấu nối + chữ có dấu theo sau (`1.a.`); chữ + dấu nối + số/chữ (`a-b`,
  `A-1`); số liền chữ / chữ liền số có dấu theo sau (`1a.`, `a1)`). Không phải nhãn: `1. A là …` (khoản số 1 thân mở bằng chữ cái),
  `A1 là …` (mã/hạng), `e-mail`, `Tp.`. Cái giá đã khai: thân khoản mở bằng một số hay mã chữ–số kèm dấu (`2. 1 năm`, `A-1 là`) bị chặn.

## 2.31 Bổ sung r29 (cross-review lượt 28 — `ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md`, APPROVE còn 1 P2) — THAY điểm tương ứng
- **E1 (vị trí dấu của nhãn = vị trí `_nhan` cho phép: ĐẦU · GIỮA · CUỐI):** tiền tố nhãn = mọi dấu `lvlText` (`.` `)` `(` `-` `–`, có đệm)
  đứng trước placeholder đầu — áp cho cả `_RE_NHIEU_CAP` và `_RE_DIEM`. `_RE_DIEM` thêm nhánh: có ÍT NHẤT một dấu ở đầu rồi placeholder
  (số, hoặc chữ cái lặp ĐỨNG RIÊNG) và kết ngay sau placeholder (`.1 …`, `.a …`, `(a …`). Dòng mở bằng dấu rồi một TỪ (`(Hồ sơ) …`,
  `.Hồ …`) không phải nhãn.

## 2.32 Bổ sung r30 (cross-review lượt 29 — `ops/acceptance/llm-khoan-docx/r1/review-29-codex/VERDICT.md`) — THAY điểm tương ứng
- **F2:** đoạn có `pStyle` trỏ style KHÔNG CÓ trong part styles ⇒ đoạn "lạ" (chặn nếu trong Điều) — Word lùi về style đoạn mặc định
  (có thể mang gạch) còn bộ đọc không tính tầng ấy; không đoán fallback.
- **F1 (mở rộng `_RE_NHIEU_CAP` §2.30):** MỘT placeholder (số, hay chữ cái lặp đứng riêng) rồi HAI dấu `lvlText` trở lên (`1..`, `1.)`,
  `a).`) là nhãn — xét trước nhánh số khoản, nên không thành số khoản `1.` kể cả khi số trùng số khoản kế.

## 2.33 Bổ sung r31 (cross-review lượt 30 — `ops/acceptance/llm-khoan-docx/r1/review-30-codex/VERDICT.md`) — THAY điểm tương ứng
- **G1 (mở rộng §2.32 F2, phân giải style THEO LOẠI):** loại style lấy từ `w:type` (vắng ⇒ `paragraph`). `pStyle` trỏ style vắng HOẶC khác
  loại `paragraph` ⇒ đoạn "lạ"; `rStyle` trỏ style khác loại `character` ⇒ đoạn "lạ"; chuỗi `basedOn` nối hai style khác loại ⇒ ValueError.
  (`rStyle` trỏ style vắng: Word bỏ qua, bộ đọc cũng không tính tầng nào — giữ như cũ.)
- **G2 (mở rộng `_RE_NHIEU_CAP`):** số + dấu `lvlText` DÍNH chữ cái lặp đứng riêng (`1.a …`, `2)b …`) là nhãn; nhãn một placeholder nhiều
  dấu (§2.32 F1) không tính `(` ở dấu thứ hai trở đi — `1. (Hồ sơ) là …` là khoản có thân mở bằng cụm ngoặc. `1. a …` (có đệm, không dấu
  sau chữ) vẫn là khoản thân mở bằng chữ cái — vùng giao giữ theo §2.30.

## 2.34 Bổ sung r32 (cross-review lượt 31 — `ops/acceptance/llm-khoan-docx/r1/review-31-codex/VERDICT.md`) — THAY điểm tương ứng
- **H1:** loại HIỆU LỰC của style (vắng `w:type` ⇒ `paragraph`) dùng cho MỌI bước: chọn style đoạn mặc định, kiểm điểm vào đoạn/run,
  kiểm chuỗi `basedOn`.
- **H2 (mở rộng §2.33 G2):** số + (đệm) + dấu `lvlText` + chữ cái lặp DÍNH ngay sau dấu (`2 .a …`, `2 )b …`) là nhãn. Ngoại lệ §2.30 giữ
  nguyên: đệm SAU dấu (`1. a …`) là khoản thân mở bằng chữ cái.
- **H3:** styleId rỗng/vắng hay mở bằng `#` (miền khoá nội bộ của bảng style: `""`, `#numPr_mac_dinh`, `#loai`) ⇒ ValueError có chẩn đoán,
  kể cả style không dùng.

## 2.35 Bổ sung r33 (cross-review lượt 32 — `ops/acceptance/llm-khoan-docx/r1/review-32-codex/VERDICT.md`, APPROVE còn 2 P2) — THAY điểm tương ứng
- **I1 (miền khoá):** mọi tra cứu style (`pStyle`, `rStyle`, chuỗi `basedOn`) chỉ trên tập ID ĐÃ XÁC THỰC là định nghĩa (bảng loại) — không
  bao giờ trúng khoá nội bộ (`""`, `#…`). `pStyle` ngoài tập ⇒ đoạn "lạ" (§2.33); `rStyle`/`basedOn` ngoài tập = style vắng, Word bỏ qua ⇒
  chuỗi dừng (không tầng nào), không traceback.
- **I2 (mở rộng `_RE_NHIEU_CAP`):** số + (đệm) + dấu + HAI placeholder chữ trở lên KỀ NHAU + dấu `lvlText` (`1.ab.`, `1.aB)`) là nhãn. NGOÀI
  MIỀN (giới hạn đã khai): placeholder chữ kề nhau KHÔNG có dấu kết (`1.ab …`) trùng hình dạng thân dính sau số mở bằng một từ ASCII
  (`2.Quy trình …`, đối chứng #1514) — thuộc bước duyệt ranh giới.

## 2.36 Bổ sung r34 (cross-review lượt 33 — `ops/acceptance/llm-khoan-docx/r1/review-33-codex/VERDICT.md`, APPROVE còn 2 P2) — THAY điểm tương ứng
- **J1 + J2 (THAY nhánh I2 §2.35 và nhánh số–chữ §2.30):** MỘT nhánh "số, (đệm/dấu `lvlText` tuỳ ý), DẢI chữ cái (lớp ký tự PHẲNG, không lặp
  lồng nhau ⇒ thời gian tuyến tính), (đệm), DẤU KẾT `.`/`)` hoặc gạch có khoảng trắng sau" là nhãn: `1.ab.`, `1. ab.`, `1ab.`, `1 a.`, `1.a.`.
  Nhánh số–số tách riêng (`1.1`, `1. 1`, `1(1)`, `1).1`). Không phải nhãn: `1. A là …`, `1. e-mail là …`, `1. Ban hành là …`, `2.Quy trình …`.
  Cái giá đã khai: khoản mà thân mở bằng chữ viết tắt ASCII có dấu chấm (`1. Tp. Hồ Chí Minh là …`) bị chặn. Ngoài miền (§2.35 giữ):
  dải chữ KHÔNG có dấu kết.

## 2.37 Bổ sung r35 (cross-review lượt 34 theo LỚP — `ops/acceptance/llm-khoan-docx/r1/review-34-codex/VERDICT.md`, APPROVE còn 3 lớp P2) — THAY điểm tương ứng
Lượt 34 review theo LỚP lỗi kèm hint patch (chỉ thị chủ kho). Mỗi lớp vá tại MỘT điểm chung, không theo từng hình dạng.
- **Lớp `ranh-gioi-khoan` (THAY nhánh J1/J2 §2.36):** MỘT bộ quét đầu dòng `quet_nhan_dau_dong` cho mọi đường thô (`--tep`, chữ của
  `extract`), nguồn có số lẫn mất số, phân loại nhãn TRƯỚC số khoản đơn. Ngữ pháp cùng bảng dấu với `_nhan`: dấu tiền tố* thành phần
  (dải số/chữ placeholder dính nhau) nối bằng dải dấu `.` `)` `(` `-` `–` có đệm, hoặc bằng ĐỆM trước một thành phần. Thành phần được xác
  nhận khi dải dấu sau nó có `.`/`)` hoặc kết ở RANH GIỚI NHÌN THẤY (đệm, hết dòng, dấu mở trích dẫn/ngoặc của thân); dấu nối không ranh
  giới chỉ xác nhận khi thành phần sau nó được xác nhận; chữ số sau một dấu nối được xác nhận không cần dấu kết. Số khoản đơn mà thân mở
  bằng nhãn đã xác nhận (`1. ab. …`, `1.ab-“…`, `1. (a) …`) là nhãn ⇒ từ chối CẢ nguồn. Dải chữ dính chữ ngoài bảng placeholder (`Hồ`)
  là chữ thân. Bảng ngoại lệ (đối chứng đã duyệt, CÙNG cho hai đường): dải HOA ĐẦU + thường (`Tp.`, `Ths.`) là chữ viết tắt — nay
  `1. Tp. Hồ Chí Minh là …` được NHẬN (bỏ cái giá đã khai ở §2.36); `e-mail`, `A1`, `(Hồ sơ)`, `ASEAN (Hiệp hội)`, `2.Quy trình`.
  **Giới hạn đã khai (thêm):** dấu mở của thân và dấu mở kết thúc nhãn chỉ được phân biệt khi còn ranh giới nhìn thấy giữa nhãn và thân
  (`1.ab(Hồ sơ)` là khoản có thân `ab(Hồ sơ)`); dạng trùng với một khoản hợp lệ, nhãn nhiều placeholder dính nhau mà không có dấu phân
  biệt, nhãn ghép hai placeholder khác kiểu chữ (`%1%2` hoa + thường) và nhãn chỉ ngăn bằng khoảng trắng thuộc bước duyệt ranh giới.
- **Lớp `can-tai-nguyen-doc-nguon`:** ngân sách đặt ở ranh giới đọc nguồn, vượt ⇒ lỗi nguồn có kiểm soát (đường thô: không xác minh được;
  CLI: rc 2 TRƯỚC model; .docx: `ValueError`). Trần: văn bản thô 400 000 ký tự (`vuot_ngan_sach`), số khoản 4 chữ số (kiểm trước `int`),
  độ sâu cây XML 128 tầng (duyệt TƯỜNG MINH ngay sau parse, mọi part), nhãn mở rộng 64 ký tự, tổng chữ Điều dựng từ .docx 400 000 ký tự;
  dòng của mỗi khoản gom rồi nối MỘT lần; dấu kết câu xác định bằng QUÉT LÙI một lần (bỏ regex không neo đầu ⇒ bậc hai).
- **Lớp `ranh-gioi-ky-tu`:** kiểm chữ GỐC (`ky_tu_la`) trên MỌI đoạn .docx TRƯỚC khi chọn đoạn có nội dung/tiêu đề — đoạn chỉ có khoảng
  trắng ngoài danh sách (trước tiêu đề, trong vùng, cuối tệp) ⇒ `ValueError`; chữ ngoài miền nằm trọn trong mẩu đã bỏ không tính.
- **Test:** `ca_r35_lop_loi` phủ MIỀN mỗi lớp (bảng hình dạng nhãn × ba vị trí; đối chứng; ngân sách từng đường kèm phép đo thời gian;
  đoạn trắng ngoài miền ba vị trí + đối chứng); mỗi chốt một đột biến riêng; đột biến lớp regex cũ chạy KÈM tắt bộ quét (`_TAT_QUET`) để
  đo riêng từng lớp chốt chồng nhau.

## 2.38 Bổ sung r36 (Review Rescue Checkpoint §12 + cross-review lượt 35 — `ops/acceptance/llm-khoan-docx/r1/review-35-codex/`, verdict tạm REQUEST_CHANGES còn 2 lớp P2, lượt bị ngắt) — THAY điểm tương ứng
**Vì sao đổi cách làm (§12, chủ kho duyệt 26-11-2026).** Lớp `ranh-gioi-khoan` đã xuất hiện ở hầu hết 35 lượt; từ lượt 25 mỗi
lượt một biểu hiện mới (B1 … J1), và cả bộ quét r35 cũng còn khe (lượt 35: dấu đầu dòng `•` `+` sau số khoản; nhãn có dấu chấm
TIỀN TỐ). Nguyên nhân chung: mọi bản vá đều là DANH SÁCH CẤM hình dạng nhãn, phải đoán trước mọi cách viết của `lvlText`. r36 đảo
thành DANH SÁCH CHO PHÉP; executor đã KHÔNG dừng ở lần lặp thứ ba của lớp như §12 đòi — ghi nhận ở đây.
- **Lớp `ranh-gioi-khoan` (THAY §2.28–§2.37 phần nhãn của đường thô):** một dòng thô chỉ được nhận khi đầu dòng thuộc tập:
  `[N.` | `N)` | `(N)`, N 1–4 chữ số, đệm ngang tuỳ ý`]` `[một dấu mở “ " ‘ ( tuỳ ý]` TỪ ĐẦU, với TỪ ĐẦU là dải chữ cái liền
  đầu thân thoả (a) chứa ít nhất một chữ NGOÀI bảng placeholder ASCII+đ — `_nhan` chỉ sinh chữ số, chữ ASCII và dấu `lvlText`, nên
  chữ có dấu thanh/mũ không thể là nhãn; hoặc (b) chữ ASCII dài ≥ 2, không phải một chữ lặp, theo sau là đệm ngang rồi một CHỮ CÁI.
  Mọi đầu dòng khác ⇒ từ chối CẢ nguồn (dùng `--tep <tệp .docx>`). `_RE_NHIEU_CAP` và bộ quét r35 bị gỡ; `_RE_DIEM` chỉ còn dùng
  trong `_tu_noi` (khoản truyền vào nhiều dòng) và `_bo_dau_dong`, không còn quyết ranh giới đường thô.
  **Chặn oan có chủ đích (thay các đối chứng đã duyệt r28–r35):** `Tp. …`, `e-mail …`, `A1 …`, `1. A là …`, `ASEAN (…)`, thân mở
  bằng chữ số, ký hiệu, dấu đầu dòng. **Giới hạn đã khai:** nhãn DÍNH thân không có dấu phân biệt (`(aHồ…`, `aHồ…`) và nhãn chỉ
  ngăn bằng khoảng trắng mà phần sau là chữ (`ab Hồ …`) không phân biệt được với thân — thuộc bước duyệt ranh giới.
- **Lớp `can-tai-nguyen-doc-nguon` (bổ sung §2.37 theo lượt 35):** `--tep` đọc CÓ GIỚI HẠN byte (4 × 400 000) trước khi giải mã;
  `vuot_ngan_sach` chặn cả số đầu dòng quá 4 chữ số ⇒ CLI rc 2 TRƯỚC model ở cả hai đường thô; XML parse TĂNG DẦN, đếm độ sâu (128)
  và số nút (2 000 000) ngay ở sự kiện `start`; chuỗi `basedOn` nhớ theo (style, chỉ số); `lvlText` kiểm độ dài (64) và ngữ pháp
  MỘT vế lặp TRƯỚC khi mở rộng; tổng chữ Điều chốt SỚM trên chữ đoạn rồi chốt cuối với đúng số dấu xuống dòng GIỮA các dòng (Điều
  dựng ra đúng 400 000 ký tự được nhận).
- **Lớp `ranh-gioi-ky-tu`:** lượt 35 xác nhận ĐÃ VÁ THẬT — giữ nguyên §2.37.
- **Test:** `ca_r35_lop_loi` mở rộng (đầu thân ngoài danh sách ở cả hai đường; biên tổng đúng; số nút; nhãn ngắn mở rộng dài; chốt số
  dài trước model); mutant của ngữ pháp nhãn cũ bị gỡ cùng mã của nó, thay bằng mutant cho từng điều kiện của danh sách cho phép và
  từng chốt ngân sách; selftest `r380` thêm ca số 5 chữ số ⇒ rc 2 không gọi model.

## 2.39 Bổ sung r37 (cross-review lượt 36 — `ops/acceptance/llm-khoan-docx/r1/review-36-codex/VERDICT.md`, APPROVE còn 2 lớp P2) — THAY điểm tương ứng
- **Lớp `ranh-gioi-khoan` — GIỚI HẠN ĐÃ KHAI (quyết định chủ kho 26-11-2026, "Khai giới hạn"):** trên văn bản thô, nhãn điểm cấp
  con kiểu số cùng dạng `N.`, `N)` hoặc `(N)` với số khoản có thể trùng một dãy khoản liên tục — khi dãy số sau mất cấp vẫn liên tục
  từ 1 và mọi dòng qua chốt dấu kết, một điểm có thể bị nhận thành khoản riêng; phép so chữ dựa trên phân đoạn đó. Ca thường gặp
  (câu dẫn khoản kết `:` rồi các điểm) vẫn bị chặn vì `:` không kết khoản. Giới hạn được KHOÁ vào tín hiệu đầu ra: `pham_vi_kiem`
  của đường thô nêu nó và chỉ sang `--tep <tệp .docx>` (đường cấu trúc giữ cấp danh sách). Bảng placeholder của danh sách cho phép
  = đúng miền của `_chu_cai` (A–Z, a–z): `đ/Đ` không bao giờ là nhãn nên thuộc nhánh (a) (`Đa dạng …` được nhận).
- **Lớp `can-tai-nguyen-doc-nguon` (bổ sung §2.37–§2.38 theo lượt 36):** tiền kiểm số dài dùng CÙNG quy tắc với `tach_khoan`
  (gỡ một BOM, `splitlines` LF/CRLF/CR); CLI đo ngân sách trên chữ GỐC trước khi bỏ biên; gói `.docx` có trần byte (64 MiB) đo TRƯỚC
  khi mở ZIP và trần số member (2000); MỘT bộ phân giải `basedOn` có nhớ cho mọi hậu tố (cả kết quả vắng) dùng cho bốn thuộc tính —
  vòng lặp ở bất kỳ đâu trong chuỗi ⇒ chặn; số thứ tự âm ⇒ chặn; độ dài nhãn cộng dần theo placeholder TRƯỚC khi dựng chuỗi; tổng
  chữ Điều trừ dần khi thêm từng dòng/nhãn/phân cách (chốt sớm trên chữ đoạn giữ nguyên; Điều đúng 400 000 ký tự được nhận). Đường
  `<số hiệu>`: lượng stdout do bộ đọc chung `tl extract` bảo đảm (trần export ~200 000 ký tự, §2.21), chốt ứng dụng chạy sau nhận.
- **Test:** `ca_r35_lop_loi` thêm ca số âm, chuỗi `basedOn` dài dùng chung (đo thời gian), trần byte gói, tiền kiểm BOM/CR/CRLF, `Đa
  dạng`, và khoá giới hạn trong `pham_vi_kiem`; mutant riêng cho từng chốt.

## 2.40 Bổ sung r38 (cross-review lượt 37 — `ops/acceptance/llm-khoan-docx/r1/review-37-codex/VERDICT.md`, APPROVE còn 2 lớp P2) — THAY điểm tương ứng
- **Lớp `ranh-gioi-khoan` (sửa thiết kế danh sách cho phép §2.38):** lỗ là luật (a) chỉ xét CHỮ của từ đầu mà không xét ký tự ĐỨNG
  SAU nó — nhãn điểm GÕ TAY bằng chữ tiếng Việt (`đ)`, `(đ)`, `đ.`, `đ -`) có chữ ngoài bảng placeholder Word nên được nhận. Nay ở CẢ
  HAI nhánh, từ đầu phải là một TỪ TRỌN: theo sau là đệm ngang rồi một chữ cái hoặc chữ số (`Hồ sơ`, `Điều 3 của …`). Chốt dấu phân
  cách mơ hồ (`_dong_mo_ho`) đo trên CHÍNH span thân mà danh sách cho phép đã chọn, sau khi phân loại — `_bo_dau_dong` không còn cấp
  span riêng cho đường thô. Ba giới hạn đã khai (§2.38–§2.39) giữ nguyên; nhãn chữ tiếng Việt chỉ ngăn bằng khoảng trắng (`đ tổ chức`)
  thuộc giới hạn "nhãn chỉ ngăn bằng khoảng trắng".
- **Lớp `can-tai-nguyen-doc-nguon`:** `tl extract` chạy qua bộ chạy ĐỌC THEO KHỐI có trần byte mỗi ống (1 600 000) — vượt thì giết
  tiến trình và dừng trước model; gói `.docx` đo byte và mở trên CÙNG một handle, số entry đọc từ bản ghi EOCD TRƯỚC khi `ZipFile`
  nạp thư mục trung tâm (ZIP64 ⇒ không hỗ trợ); miền bộ đếm `0..999` chốt NGAY khi cập nhật, mọi kiểu cấp (kể cả bullet); chữ hiệu
  lực cộng dồn và chốt ngay khi phân tích từng đoạn; ngân sách dòng điểm trừ TRƯỚC khi ghép.
- **Test:** bảng nhãn chữ tiếng Việt × hai vị trí × hai đường; đối chứng `Điều 3 của quy chế …`; số âm cấp bullet; bộ chạy extract
  có trần (stdout/stderr); dữ liệu ca dấu phân cách mơ hồ đổi để đầu dòng qua danh sách cho phép (chốt ngoặc vẫn được đo); mutant
  riêng cho từng chốt.

## 2.41 Bổ sung r39 (cross-review lượt 38 — `ops/acceptance/llm-khoan-docx/r1/review-38-codex/VERDICT.md`, APPROVE còn 2 lớp P2) — THAY điểm tương ứng
**Căn cứ — ba quyết định chủ kho (26-11-2026), chép nguyên văn:**
> 1. Lớp `ranh-gioi-khoan` [P2]: THU HẸP MIỀN theo câu khai lượt 38 — "Khi phần mở đầu khoản cũng có hình dạng nhãn điểm nhiều vế, đường thô từ chối cả Điều. Dùng DOCX có cấp danh sách để xác minh." Khoá ca dương/âm ở hai phía miền trong `pham_vi_kiem`.
> 2. Lớp `can-tai-nguyen-doc-nguon` [P2]: VÁ TRONG PR NÀY theo hint lượt 38 (đếm entry thật của thư mục trung tâm ZIP trước `ZipFile`; `_chay_gioi_han` giữ deadline tới `wait(timeout=…)`, thu hồi có hạn, truyền lỗi reader về caller, nối tối đa phần còn lại), kèm ca + đột biến riêng cho từng chốt.
> 3. Trần lời gọi Codex: nâng lên 45 (đã dùng 39). Tới trần mà còn P2 chặn merge thì DỪNG và hỏi chủ kho.

- **Lớp `ranh-gioi-khoan` — THU HẸP MIỀN (quyết định 1):** `_mo_dau_nhieu_ve` (gọi trong `dau_dong_cho_phep`, cả hai đường thô, đầu
  dòng lẫn đầu thân sau số khoản): thân mở bằng [`(`] ≥ 2 VẾ (dải chữ/số) chỉ ngăn bằng đệm ngang, không có chữ "là" trong các vế, rồi
  DẤU KẾT nhãn và còn chữ phía sau ⇒ dòng bị từ chối ⇒ cả Điều. Dấu kết: `.`/`)` mọi độ dài vế; `-`/`–` đứng trước khoảng trắng hay dấu
  mở trích dẫn/ngoặc chỉ khi ≤ 3 vế, mỗi vế ≤ 3 ký tự. Phía ÂM: `ab c. …`, `Ban a) …`, `(Ban a) …`, `(Hồ sơ) là …`, `ab c - …`, `Hồ sơ
  gốc. Dữ liệu là …`. Phía DƯƠNG: cụm từ đứng trước "là" (`Hồ sơ là …`), gạch nối giữa các từ dài (`kinh tế - xã hội`), ngoặc sau từ
  đầu (`Quy chuẩn … (QCVN) là …`, `Hồ sơ (bản chính) là …`), câu trọn một dòng (`Hồ sơ gồm các tài liệu.`). Hai phía khoá trong
  `pham_vi_kiem` của đường thô. `(Hồ sơ) là …` (đối chứng dương r31 G2) nay là ÂM theo quyết định này. Ba giới hạn đã khai
  (§2.38–§2.39) giữ nguyên.
- **Lớp `can-tai-nguyen-doc-nguon` (quyết định 2):** (1) số entry ZIP đếm THẬT, tuần tự từng bản ghi thư mục trung tâm trên đúng vùng
  `zipfile` sẽ đọc, dừng ngay khi vượt 2000, TRƯỚC `ZipFile`; locator ZIP64, vùng ngoài tệp, bản ghi hỏng hay số đếm lệch số khai ⇒
  chặn. (2) `_chay_gioi_han`: MỘT hạn chót phủ tới `wait(timeout=…)`; lỗi đọc trong luồng về người gọi; vượt trần, quá hạn hay lỗi ⇒
  giết + thu hồi có giới hạn rồi dừng trước model; mỗi lần đọc tối đa phần còn lại + 1 byte; đúng trần được nhận.
- **Test:** hai phía miền nhãn nhiều vế × hai vị trí × hai đường; ZIP vượt trần entry với `ZipFile` bị thay bằng stub (chốt chạy
  trước); số khai lệch; tiến trình đóng ống rồi treo ⇒ quá hạn có kiểm soát; đúng trần byte; khoá hai phía miền trong `pham_vi_kiem`;
  mutant riêng cho từng chốt.
- **Bối cảnh nhánh:** trước r39 đã merge `origin/master` (148 commit), xung đột duy nhất `RELEASE_MANIFEST.json` ⇒ sinh lại
  (`release-verify --strict` 187/187).

## 2.42 Bổ sung r40 (review offline lượt 39 trên `9e2f419` — `ops/acceptance/llm-khoan-docx/r1/review-39-codex/VERDICT.md`, APPROVE còn 2 lớp P2 + 2 lớp P3) — THAY điểm tương ứng
**Quy tắc push (ADR-0060 M5/M12, chủ kho nhắc 26-11-2026):** nhánh code đẩy MỘT lần chính, sau khi review offline approve VÀ đủ điều
kiện merge (0 P1, 0 P2, 0 P3 theo yêu cầu chủ kho) trên đúng SHA. Từ r39 ứng viên là commit CỤC BỘ; r35–r38 đã đẩy sai quy tắc này.
- **Lớp `ranh-gioi-khoan` (thực thi trọn quyết định chủ kho 1, §2.41):** `_mo_dau_nhieu_ve` bỏ ngoại lệ "gạch ≤ 3 vế ngắn" — mọi số vế,
  mọi độ dài vế, dấu kết `.` `)` `-` `–` `—`; dấu mở `(` `“` `"` `‘`. Mốc thoát DUY NHẤT là từ nối cấp khoản: vế `là` NGOÀI dấu mở và có
  khoảng trắng theo sau (cùng điều kiện `_RE_LA`) — `là` trong ngoặc/nháy mở hay dính dấu kết không thoát. Hệ quả có chủ đích: dòng mở
  bằng cụm `… - …` (`Phát triển kinh tế - xã hội là …`) bị chặn — dùng `.docx`.
- **Lớp `can-tai-nguyen-doc-nguon`:** locator ZIP64 kiểm ở VỊ TRÍ TUYỆT ĐỐI `EOCD − 20` trên cùng handle (không trong cửa sổ đã đọc);
  `_chay_gioi_han` dùng MỘT hàm thời gian còn lại cho mọi lần chờ luồng và tiến trình, và MỘT nơi quyết nhận thành công (qua hạn ⇒
  không nhận, kể cả khi tiến trình vừa kết thúc).
- **P3 `huong-dan-docx`:** hướng dẫn tách quy tắc `pStyle` / `rStyle` / `basedOn` theo §2.33. **P3 `ghi-chu-write-set`:** `write_set_note`
  bỏ trần số lượt, trỏ danh sách đường dẫn làm nguồn phạm vi duy nhất.
- **Test:** ca âm cho mọi nhóm dấu kết/số vế/vị trí `là`; ZIP có locator ZIP64 "che" trong comment bản ghi thư mục; tiến trình GIẢ
  đo lỗi luồng đọc, kích thước mỗi lần đọc, thu hồi có hạn, và kết quả qua hạn; mutant riêng cho từng chốt.

## 3. Test (`scripts/tl_core/llm_route_test.py`, `scripts/tl_selftest.py`)
- Mỗi chốt §2.1 một mẫu chặn (ca `ca_cau_truc_docx_chan`) và một đột biến riêng bị giết bằng `TinHieuChotCa` của ca đích;
  ca `ca_cau_truc_docx_dat`: khoản + điểm đạt, model tách điểm thành khái niệm riêng ⇒ lệch, chữ gạch ngang bị lọc, nhãn
  điểm đặt lại ở khoản sau, đọc tới HẾT tệp (tệp chỉ chứa một Điều — §2.9; tệp có tiêu đề Điều khác bị chặn). Đối chứng
  `startOverride` đạt.
- §2.3: mẫu nguồn có số và mất số có dòng điểm (mọi dòng kết `.`) ⇒ None; đột biến bỏ chốt phải bị giết. Các ca cũ về khoản có
  điểm chuyển sang đo logic so nguyên văn qua `khoan` cấu trúc (`kh(vb)`).
- Selftest `r1525_llm_khai_niem_tep_docx_cau_truc`: CLI `--tep <.docx>` rc 0 / rc 5 (tách điểm) / rc 2 (thiếu `--dieu`).

## 4. Ngoài phạm vi
- Đường `<số hiệu>` lấy `.docx` từ Drive (cần resolve số hiệu → id trong tiến trình) — packet riêng nếu chủ kho mở.
- Không bump VERSION; không deploy Package.

## 5. Nghiệm thu
1. `python scripts/tl_core/llm_route_test.py`: mọi ca đạt, mọi đột biến bị giết.
2. `python scripts/tl.py --selftest` N/N; `release-verify RELEASE_MANIFEST.json --strict`; `workflow-audit --strict`,
   `golden-test`, `determinism-audit --strict`, `doc-claims-check --strict` rc 0; ruff F delta 0.
3. Cross-review Codex (trần 45 lời gọi TÍNH CHUNG — quyết định chủ kho 3; r1–r33, r35–r39 mỗi bản dùng 1, r34 dùng 2 — lượt 34 chạy lại theo lớp; lượt 35 bị ngắt khi worker khởi động lại; chủ kho cho executor tự nâng trần tới khi hết P1/P2) — kết luận ghi trong `ops/acceptance/llm-khoan-docx/r1/VERDICT.md`.
