# LLM-KHOAN-DOCX r1: ranh giới khoản của `llm-khai-niem` từ cấu trúc danh sách đánh số .docx (đặc tả đóng băng)

- **Packet:** #1525. Revision 1, generation 1. Role `executor` (Claude), reviewer Codex. Review Class `sensitive` (write set
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
3. Cross-review Codex (trần 5 lời gọi) — kết luận ghi trong `ops/acceptance/llm-khoan-docx/r1/VERDICT.md`.
