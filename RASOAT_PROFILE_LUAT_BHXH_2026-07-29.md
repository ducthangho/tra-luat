# RÀ SOÁT PROFILE «Luật BHXH» — 29-07-2026

Phiên dev (read-only qua Drive MCP — KHÔNG ghi registry/corpus/NLM). Nguồn đối chiếu:
- `tra_luat_registry.LuatBHXH` (spreadsheet `1yh0fxKk…`, sửa lần cuối 26-07 15:26 UTC) — 91 dòng duy nhất theo `drive_id`.
- `_meta/rasoat_state.json` (27-07 01:20, hồ sơ `h7-3nd-bhxh-2025`) + `_meta/tra_luat_profile.json` (schema v2, fingerprint `19780d61…`).
- Cây thư mục root `1iJmt1GE…` (2 trang liệt kê) + thư mục con `Hồ sơ Luật`, `_meta`.
- Thông tin dự thảo đã thu thập các lượt trước (lưu trong state + bộ tài liệu DUTHAO_* 16-7-2026).

Tiến độ nền: 5/5 đơn vị rà `done` (NĐ 159, 233, 212, đối chiếu 159×158, 158), ~37 phát hiện VD-01..VD-37;
bảng master chốt lượt 3: 3 văn bản / 26 phát hiện / phụ lục 03:3 · 04:17 · Mục F:9; sổ lỗi 14 mục.

---

## A. P1 — chặn kết luận / rủi ro sai nguyên văn

**A1. Registry chứa 2 sheet gần trùng nhau, lệch đúng 3 ô `corpus`.**
Hai khối bảng 91 dòng giống hệt nhau TRỪ 3 dòng NĐ 159/233/212: một sheet `corpus=true`
(sau flip đã duyệt 26-07, journal `source-update-corpus_1785079559_29092`, có undo), sheet kia vẫn `false`
(snapshot chụp trong khoảng 23→26-07). Rủi ro: lệnh/người đọc nhầm sheet cũ sẽ thấy cờ corpus sai.
→ Trên máy LIVE: `tl --profile "Luật BHXH" reg-query --refresh` xác nhận webapp đọc sheet nào là canonical,
rồi xoá/đánh dấu sheet thừa QUA GAS webapp (không sửa tay Sheets, không dùng Sheets MCP).

**A2. Luật gốc bị sửa — Luật BHXH 41/2024/QH15 — vẫn chưa có trong corpus.**
Bản trong kho là DỰ THẢO còn markup, đang nằm `_ZZZ_QUARANTINE_taluat`; bản Công báo 987+988 (25/8/2024,
PDF lớp text thật) đã tải được ở lượt 3 và đang treo `cho_duyet_ghi` (Q-INGEST). Hiện mọi đối chiếu
dự thảo sửa đổi ↔ luật hiện hành phải đi vòng qua VBHN 19-2026-VBHN-VPQH vốn còn cảnh báo
`MARKUP_SUA_DOI strike=2`. Đây là món duyệt ưu tiên số 1 để hồ sơ thẩm tra dự án Luật đứng trên bản BAN HÀNH.

**A3. Bản NĐ 159/2025 trong kho lệch bản Công báo 8 điểm cấp ký tự** (sổ lỗi
`BAN_SAO_ND159_TRONG_KHO_HONG_KY_TU`; đã làm VD-02 bị bác — bản Công báo viết đúng "chuyển", bản kho sai).
Việc thay bằng bản Công báo 853+854 (01/7/2025) đang treo `cho_duyet_ghi`. Chừng nào chưa thay,
mọi trích dẫn nguyên văn NĐ 159 phải neo bản Công báo, không neo bản kho.

**A4. 2 file PDF mồ côi mang tên gây nhầm số hiệu luật hiện hành.**
`DUTHAO_Luat_41_2024_QH15_Du_an_Luat_sua_doi_bo_sung…pdf` và `DUTHAO_Luat_41_2024_QH15_cua_Luat_sua_doi…pdf`
nằm ngay root profile (tải 21-07), KHÔNG có dòng registry, tên ghép "Luat_41_2024_QH15" (số hiệu của luật
đang có hiệu lực) vào một bản DỰ THẢO — vi phạm bài học số hiệu/năm, nguy cơ trích nhầm dự thảo làm luật.
→ Đổi tên chuẩn `DUTHAO_…` không kèm số hiệu luật hiện hành (hoặc quarantine), rồi đăng ký với
`hieuluc=DỰ THẢO — chưa hiệu lực`.

## B. P2 — nhất quán dữ liệu registry

**B1. Từ vựng `hieuluc` trôi:** `Còn hiệu lực` (20) · `Còn` (11) · `con_hieu_luc` (1) · rỗng (45);
nhãn dự thảo có 2 biến thể `DỰ THẢO — chưa hiệu lực` (8) và `DỰ THẢO - hồ sơ trình` (5). Cần chuẩn một bộ.

**B2. `18-2026-VBHN-VPQH` (BLLĐ hợp nhất) có 2 dòng mâu thuẫn:** một `nlm_status=removed_by_user`,
một `pushed` (loai ghi khác nhau: `VBHN` vs `Văn bản hợp nhất`). Trạng thái NLM thật phải neo `nlm-reconcile`.

**B3. Món trùng/thiếu năm đã ghi nhận (26-07, quyết "CHỈ GHI NHẬN"):** cụm `40-VBHN-VPQH` (2 dòng trùng
bản BHYT của `40-2026-VBHN-VPQH`), `89_VBHN-VPQH_670749` (họ 89-2025 Luật MTTQ, trùng canonical),
1 dòng trùng nội dung `89-2026-VBHN-VPQH` (Luật NSNN); `25-VBHN-VPQH` (Luật NHNN) thiếu năm trong sohieu.
Kèm: bản VBHN Luật NSNN trong kho THIẾU khối đầu văn bản → trích dẫn phải kèm năm thủ công.
Chưa dọn — giữ trong sổ để lượt dọn kho riêng, tránh quên.

**B4. 10 dòng «Hồ sơ Luật» (thế hệ dự thảo 16.6.2026) ghi `nlm_status=removed_from_drive` nhưng
file PDF vẫn nằm nguyên trong thư mục con `Hồ sơ Luật`** — trạng thái lệch thực tế. Profile hiện chứa
song song 2 thế hệ dự thảo (16.6 và 16-7-2026); nên gắn note thế hệ/`superseded_by` để không trích nhầm bản cũ.

**B5. 5 dòng sohieu nền không metadata:** `67-2025`, `89-2026`, `24-2026`, `100-2026`, `60-2026-VBHN-VPQH`
trống name/loai/hieuluc — rơi vào từ BASE_SCOPE_HIT (scope nền), ngoài phạm vi hồ sơ; nên gắn note
để khỏi tưởng thiếu dữ liệu profile.

**B6. Chính sách corpus cho tài liệu dự thảo không nhất quán:** 5 tài liệu `DỰ THẢO - hồ sơ trình`
mang `corpus=true` (Bản thuyết minh QPH, BC rà soát chủ trương/điều ước, Bản đánh giá TTHC,
2 DUTHAO_ND kèm theo) trong khi chính `DUTHAO_Luat_sua_doi…16-7` lại `corpus=false`. Đồng thời 12 tệp
«Bản so sánh 16-7» (3 phần) + «Ý kiến góp ý 16-7» (8 phần + mục lục) gắn `hieuluc=Còn hiệu lực` dù là
tài liệu hồ sơ trình → nhãn sai, mâu thuẫn style profile ("dự thảo luôn kèm cảnh báo DỰ THẢO — chưa hiệu lực").

**B7. Nhất quán materialize:** các bản gốc đợt đầu (docx NĐ, pdf ngân hàng…) đều có dòng `thuong`,
nhưng loạt bản gốc từ 09-07 trở đi (SCAN_KY pdf, DUTHAO_*.docx, VBT_BC_7692.pdf, VB_16_7….doc,
CV_10593/10838 pdf, THAMKHAO_ILO C102/C168) không đăng ký. `BC_6193_2026_BNV_CTL….pdf` mồ côi hoàn toàn
(không có cả bản Google Doc). → Chọn một đường: hoặc thôi đăng ký raw toàn kho, hoặc đăng ký nốt + nạp BC 6193.

**B8. Rác vận hành trong spreadsheet:** sheet manifest-summary ghi `generatedAt 2026-06-25, count 43`
(lệch hơn 1 tháng so hiện trạng ~91 dòng); sheet locks còn ~12 dòng `pending` hết hạn từ 21–23/07 chưa dọn.
Chỉ dọn qua webapp/lệnh tl có duyệt.

## C. P3 — vận hành / NLM

- **C1.** NLM notebook `59e8d0de…`: sống nhưng **rotation token hết hạn** (pha0 b5/b6) — CẤM tự chạy
  `nlm-auth-load`; cần người dùng gia hạn trước lượt rà tiếp. Quota `nlm_con_lai=56` là ESTIMATE —
  phải neo `nlm-get`/`nlm-reconcile` LIVE (đúng bài học CLAUDE.md).
- **C2.** NĐ 233 dài 107.144 ký tự > ngưỡng 100k → khi nạp lại NLM phải đi chunk pipeline
  (hiện đang pushed dạng 1 nguồn).
- **C3.** Package LIVE vẫn 1.35.50 (r214 chưa deploy) → trên gói LIVE phải truyền `--folder-id`
  tường minh cho `state-get`/`state-put`.

## D. Kết hợp thông tin Dự thảo Luật sửa đổi, bổ sung Luật BHXH (bản 16-7-2026)

1. **Hồ sơ trình đã khá đủ trong profile** (đúng nhãn DỰ THẢO, corpus=false cho chính dự thảo luật):
   Tờ trình BNV, Bản tổng hợp tiếp thu giải trình 16-7, Bản so sánh thuyết minh (3 phần),
   80 công văn góp ý (8 phần + mục lục tra ngược), BC 7692 tổng kết thi hành, BC 6193 + CV 7728 tiến độ,
   tài liệu họp TTUB 22-7. Khuyết: chính văn bản BC 6193 chưa đăng ký (B7) và luật gốc 41/2024 chưa vào corpus (A2).
2. **Các món rà soát còn mở, ảnh hưởng trực tiếp thẩm tra dự thảo:**
   - VD-12: chưa đóng âm tính "văn bản công bố tiếp tục hiệu lực" cho NĐ 30/2016 — đã xác định dạng văn bản
     cần tìm là NGHỊ QUYẾT CỦA CHÍNH PHỦ (tiền lệ NQ 31/NQ-CP 03/3/2026); vbpl.vn từ chối kết nối ở
     tầng mạng từ môi trường chạy — còn phải tra công báo điện tử + vbpl.vn khi có đường mạng.
   - VD-26: cả 3 NĐ (159/212/233) hiệu lực sớm hơn 45 ngày, 2/3 đăng Công báo SAU ngày hiệu lực 16 ngày —
     cần hồ sơ trình để xác minh trình tự rút gọn ⇒ việc của cơ quan chủ trì, không phải của công cụ.
   - VD-05 (phần còn lại): chưa xác minh NĐ 233 có đi trình tự rút gọn không — giữ mức "nghiên cứu".
3. **Khoảng trống corpus phục vụ đối chiếu quy định chuyển tiếp của dự thảo** (Q-INGEST đang treo):
   `134-2015-NĐ-CP`, `135-2015-NĐ-CP`, `30-2016-NĐ-CP` (còn hiệu lực MỘT PHẦN theo Đ23k5+Đ24k2 NĐ 212),
   danh mục xã đảo/đặc khu (chưa rõ số hiệu — cần người xác định văn bản rồi mới nạp).
4. **Chùm góp ý Điều 122 (đầu tư quỹ)** — Agribank (CV 10593) + Vietcombank (CV 10838) đã vào corpus,
   khớp trục nội dung với unit-003 (NĐ 212) và các góp ý BIDV/UBVHXH đợt 6/2026: dữ liệu phục vụ
   thẩm tra Điều 122 dự thảo đã hội đủ 2 phía (văn bản hiện hành + ý kiến ngân hàng).

## E. Việc cần làm (xếp hạng, mọi thao tác GHI đều chờ duyệt điểm chạm)

| # | Việc | Loại | Cổng |
|---|------|------|------|
| 1 | Duyệt nạp bản Công báo Luật 41/2024 (987+988) thay bản dự thảo quarantine | GHI Drive | duyệt điểm chạm 3 |
| 2 | Duyệt thay bản NĐ 159 bằng Công báo 853+854 | GHI Drive | duyệt điểm chạm 3 |
| 3 | Xử lý 2 PDF `DUTHAO_Luat_41_2024_QH15_*` (đổi tên/quarantine + đăng ký nhãn DỰ THẢO) | GHI | duyệt |
| 4 | LIVE: xác định sheet registry canonical, gỡ sheet trùng (A1) qua webapp | GHI GAS | duyệt |
| 5 | Người dùng gia hạn phiên NLM; sau đó `nlm-reconcile` neo trạng thái (B2, B4, quota) | vận hành | user |
| 6 | Chuẩn hoá vocab `hieuluc` + nhãn DỰ THẢO cho 12 tệp bản so sánh/góp ý (B1, B6) | GHI reg (bulk; field rỗng phải đi `reg_clear`) | duyệt |
| 7 | Đăng ký nốt BC 6193 + quyết chính sách raw-twin (B7) | GHI | duyệt |
| 8 | Dọn locks hết hạn + làm tươi manifest-summary (B8) | GHI GAS | duyệt |
| 9 | Tra NQ Chính phủ cho VD-12 khi có đường mạng tới vbpl.vn/công báo | tra cứu | — |

*Không món nào ở trên được tự chạy trong phiên dev này; báo cáo chỉ ghi nhận bằng chứng đọc được.*
