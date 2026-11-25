# LLM-KHOAN-DOCX r3: ranh giới khoản của `llm-khai-niem` từ cấu trúc danh sách đánh số .docx (đặc tả đóng băng)

- **Packet:** #1525. Revision 3, generation 1 (thay r2; r1–r2 giữ ở `ops/specs/llm-khoan-docx-r{1,2}.md`). Role `executor` (Claude), reviewer Codex. Review Class `sensitive` (write set
  chạm mã runtime trong gói phát hành: `scripts/tl_core/llm_route.py`, `scripts/tl_core/ops_misc.py`,
  `scripts/tl_core/command_registry.py`).
- **Căn cứ:** Issue #1525 (nợ K1 từ packet #1514, verdict lượt 10 `ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md`).
  Chủ kho trong phiên `session_015GtxrZQYT3Vt8PJdXrjEKg` ngày 25-11-2026: *"Tiếp đi"*, rồi chọn *"Do .docx numPr, cap 5"*.
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

## 3. Test (`scripts/tl_core/llm_route_test.py`, `scripts/tl_selftest.py`)
- Mỗi chốt §2.1 một mẫu chặn (ca `ca_cau_truc_docx_chan`) và một đột biến riêng bị giết bằng `TinHieuChotCa` của ca đích;
  ca `ca_cau_truc_docx_dat`: khoản + điểm đạt, model tách điểm thành khái niệm riêng ⇒ lệch, chữ gạch ngang bị lọc, nhãn
  điểm đặt lại ở khoản sau, dừng ở Điều kế tiếp. Đối chứng `startOverride` đạt.
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
3. Cross-review Codex (trần 5 lời gọi TÍNH CHUNG; r1 dùng 1, r2 dùng 1) — kết luận ghi trong `ops/acceptance/llm-khoan-docx/r1/VERDICT.md`.
