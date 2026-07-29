# RÀ SOÁT PROFILE «Luật BHXH» — 29-07-2026

Phiên dev — KHÔNG ghi registry/corpus/NLM. **Cập nhật 29-07 (lượt 2): đã có creds LIVE trong env**
(`TL_WEBAPP` + `TL_TOKEN`), nên toàn bộ khẳng định dưới đây đã được **đối chiếu lại bằng webapp thật**
thay vì chỉ đọc render Drive. Máy này không có file config → dùng overlay env
(`TL_PROFILE`/`TL_ROOT_FOLDER_ID`/`TL_META_FOLDER_ID`/`TL_REGISTRY_DOC_ID`/`TL_NOTEBOOK_ID`/`TL_MANIFEST_ID`)
lấy từ marker `_meta/tra_luat_profile.json` — đúng đường r214, chỉ đọc.

Gate LIVE: `doctor` rc=2 (chỉ vì thiếu nlm CLI + gws, credential=env OK) · webapp ping
`live=2.21.2p == expect 2.21.2p` · API_CONTRACT khớp.

Nguồn đối chiếu:
- `tra_luat_registry.LuatBHXH` (spreadsheet `1yh0fxKk…`) — **LIVE: đúng 90 dòng** (`reg-query --refresh`).
- `_meta/rasoat_state.json` (27-07 01:20, hồ sơ `h7-3nd-bhxh-2025`) + `_meta/tra_luat_profile.json` (schema v2, fingerprint `19780d61…`).
- Cây thư mục root `1iJmt1GE…` (2 trang liệt kê) + thư mục con `Hồ sơ Luật`, `_meta`.
- Thông tin dự thảo đã thu thập các lượt trước (lưu trong state + bộ tài liệu DUTHAO_* 16-7-2026).

Tiến độ nền: 5/5 đơn vị rà `done` (NĐ 159, 233, 212, đối chiếu 159×158, 158), ~37 phát hiện VD-01..VD-37;
bảng master chốt lượt 3: 3 văn bản / 26 phát hiện / phụ lục 03:3 · 04:17 · Mục F:9; sổ lỗi 14 mục.

---

## A. P1 — chặn kết luận / rủi ro sai nguyên văn

**~~A1. Registry chứa 2 sheet gần trùng nhau, lệch 3 ô `corpus`.~~ → ĐÃ BÁC BỎ (29-07, đo LIVE).**
Khối bảng thứ hai KHÔNG phải sheet rác mà là **bản sao xoay vòng do thiết kế**: endpoint chỉ-đọc
`reg_bak_list` trả `{current_rows: 90, keep: 5, count: 1, baks: [{tab: "files_bak_20260726152604", rows: 90}]}`.
GAS đặt `REG_BAK_PREFIX_='files_bak_'`, `REG_BAK_KEEP_=5` (KI-27) và chỉ đọc/ghi tab `files` (`REG_TAB_`).
Bản sao chụp lúc 26-07 15:26:04 — đúng thời điểm flip corpus — nên nó GIỮ trạng thái tiền-flip
(`corpus=false`) là **đúng chức năng của một bản sao lùi**, không phải dữ liệu lệch.
Xác nhận thêm: `reg-query --refresh` trả `corpus=true` cho cả 3 NĐ; `reg-query --limit 500` trả đúng
**90 dòng**, khớp 1-1 tập `drive_id` của bản render. "Dòng thứ 91" tôi đếm ở lượt 1 chỉ là **dòng tiêu đề lặp**
của khối thứ hai.
*Nguyên nhân sai:* đọc spreadsheet qua bộ render ngôn ngữ tự nhiên của Drive — nó nối tất cả các tab
lại mà KHÔNG ghi tên tab, nên bản sao lùi trông y hệt một sheet dữ liệu thứ hai. Đây đúng bài học
CLAUDE.md: phải test HÀNH VI, không suy từ chuỗi. **Không có việc gì phải làm cho A1.**

**A2. Luật gốc bị sửa — Luật BHXH 41/2024/QH15 — chưa có trong corpus. ✅ XÁC NHẬN LIVE, và nặng hơn tôi viết.**
Đo trực tiếp: `reg-query --sohieu 41-2024-QH15` trên profile Luật BHXH trả **count=0** — hồ sơ này
KHÔNG có dòng nào cho luật gốc. Bản duy nhất tồn tại nằm ở registry **NỀN (vbqppl)**:
`Luat_41-2024-QH15_Bao_hiem_xa_hoi` (`1Ds95NoIdZ…`), cat `_ZZZ_QUARANTINE_taluat`, `corpus=false`
(thấy qua `--base-also`). Nghĩa là mọi đối chiếu dự thảo sửa đổi ↔ luật hiện hành hiện chỉ còn đường
VBHN `19-2026-VBHN-VPQH` (`row_kind=ref`, `corpus=true`) vốn mang cảnh báo `MARKUP_SUA_DOI strike=2`.
Bản Công báo 987+988 (25/8/2024, PDF lớp text thật) đã tải ở lượt 3, đang treo `cho_duyet_ghi`.
**Đây là món duyệt ưu tiên số 1.**

**A3. Bản NĐ 159/2025 trong kho lệch bản Công báo 8 điểm cấp ký tự** (sổ lỗi
`BAN_SAO_ND159_TRONG_KHO_HONG_KY_TU`; đã làm VD-02 bị bác — bản Công báo viết đúng "chuyển", bản kho sai).
Việc thay bằng bản Công báo 853+854 (01/7/2025) đang treo `cho_duyet_ghi`. Chừng nào chưa thay,
mọi trích dẫn nguyên văn NĐ 159 phải neo bản Công báo, không neo bản kho.

**A4. 2 file PDF mồ côi mang tên gây nhầm số hiệu luật hiện hành. ✅ XÁC NHẬN LIVE.**
`DUTHAO_Luat_41_2024_QH15_Du_an_Luat_sua_doi_bo_sung…pdf` (`1GM6QY15…`) và
`DUTHAO_Luat_41_2024_QH15_cua_Luat_sua_doi…pdf` (`1UeiF7sK…`) nằm ngay root profile (tải 21-07),
đối chiếu với 90 dòng LIVE: **không dòng nào** trỏ tới 2 `drive_id` này. Tên ghép "Luat_41_2024_QH15"
(số hiệu luật ĐANG có hiệu lực) vào một bản DỰ THẢO — vi phạm bài học số hiệu/năm, và càng nguy hiểm
khi A2 cho thấy luật gốc thật KHÔNG có trong hồ sơ: người tra rất dễ vớ nhầm 2 file này làm luật hiện hành.
→ Đổi tên chuẩn `DUTHAO_…` không kèm số hiệu luật hiện hành (hoặc quarantine), rồi đăng ký với
`hieuluc=DỰ THẢO — chưa hiệu lực`.

## B. P2 — nhất quán dữ liệu registry

**B1. Từ vựng `hieuluc` trôi. ✅ XÁC NHẬN LIVE (số y hệt bản đọc render):** `Còn hiệu lực` (20) ·
`Còn` (11) · `con_hieu_luc` (1) · rỗng (45); nhãn dự thảo 2 biến thể `DỰ THẢO — chưa hiệu lực` (8)
và `DỰ THẢO - hồ sơ trình` (5). Cần chuẩn một bộ.

**B2. `18-2026-VBHN-VPQH` — ĐÍNH CHÍNH: không phải "1 dòng mâu thuẫn trạng thái" mà là HAI FILE DRIVE KHÁC NHAU.**
Đo LIVE cho thấy 2 dòng CÙNG tên `VBHN_18-2026-VBHN-VPQH_2026_Bo_luat_Lao_dong`, cùng sohieu, khác `drive_id`:
- `1n1ezVBAsrKz…` — cat `_ZZZ_QUARANTINE_taluat`, `nlm_status=removed_by_user`, cờ `RAW_NAME_NOT_NLM`
- `1gJn-6pjj2IM…` — cat `20`, `nlm_status=pushed`, không cờ

Cả hai `row_kind=ref` (đến từ scope NỀN vbqppl) và `corpus=false` → **ngoài phạm vi hồ sơ này**, cùng rọ với B3;
không ảnh hưởng kết luận rà. Ghi nhận để lượt dọn kho nền xử lý.

**B2b. (MỚI — chênh lệch công cụ, cần xem là CODE-bug hay by-design)** `registry-doctor` báo
`duplicate_sohieu_groups=0` và `duplicate_name_groups=0`, trong khi dữ liệu LIVE có **2 nhóm trùng sohieu**
(`18-2026-VBHN-VPQH` ×2 như trên, và `25-VBHN-VPQH` ×2). Tương tự `missing_sohieu=19` trong khi đếm thẳng
90 dòng ra **56 dòng sohieu rỗng**. Giả thuyết: doctor cố ý loại `row_kind=ref` và `loai='thuong'` khỏi
phép đếm (`25-VBHN-VPQH` ×2 đúng là cặp Google Doc + bản docx gốc — hợp lệ, không phải lỗi).
`sweep` cũng cho `by_sohieu=0` nhưng `by_sohieu_raw=5`, ăn khớp giả thuyết đó.
→ Việc cần làm: **đọc code xác nhận đây là by-design rồi ghi rõ cơ sở đếm vào output** (như `sweep` đã làm với
`corpus_basis`), để lần sau không ai đọc `missing_sohieu=19` mà tưởng chỉ có 19.

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

**B7. Nhất quán materialize. ✅ XÁC NHẬN LIVE — 12/12 file kiểm chứng đều KHÔNG có dòng registry.**
Các bản gốc đợt đầu (docx NĐ, pdf ngân hàng…) đều có dòng `thuong`, nhưng loạt bản gốc từ 09-07 trở đi
thì không. Đối chiếu từng `drive_id` với 90 dòng LIVE, **không dòng nào** trỏ tới:
SCAN_KY pdf · DUTHAO_Luat_sua_doi pdf+docx · DUTHAO_To_trinh docx · DUTHAO_VBT_Ban_tong_hop pdf+docx ·
DUTHAO_VBT_Mot_so docx · DUTHAO_VBT_PL_BC docx · VBT_BC_7692 pdf · VB_16_7_2026_CONG_VAN doc ·
CV_10593 + CV_10838 pdf · THAMKHAO_ILO C102 + C168 · 2 PDF ở A4.
`BC_6193_2026_BNV_CTL….pdf` mồ côi hoàn toàn (không có cả bản Google Doc).
→ Chọn một đường: hoặc thôi đăng ký raw toàn kho, hoặc đăng ký nốt + nạp BC 6193.

**B7b. (MỚI, đo LIVE) Lệch cách đếm corpus giữa client và server:** `sweep` trả `corpus=37`
(luật client: `corpus=='true'` mọi row_kind) nhưng `corpus_server_rule_equiv=22` (luật GAS thật:
trừ `ref` và `loai='thuong'`). Chênh 15 chính là các dòng `ref` mượn từ scope nền + raw twin.
Không phải lỗi, nhưng khi báo cáo "hồ sơ có bao nhiêu văn bản trong corpus" phải nói rõ dùng con số nào —
số đúng cho phạm vi hồ sơ này là **22**.

**B8. Rác vận hành trong spreadsheet:** sheet manifest-summary ghi `generatedAt 2026-06-25, count 43`
— lệch hơn 1 tháng so hiện trạng **90 dòng LIVE**; sheet locks còn ~12 dòng `pending` hết hạn từ 21–23/07
chưa dọn. Chỉ dọn qua webapp/lệnh tl có duyệt. (Bản sao `files_bak_*` thì KHÔNG phải rác — xem A1.)

## C. P3 — vận hành / NLM

- **C1.** NLM notebook `59e8d0de…`: rotation token hết hạn (pha0 b5/b6) — CẤM tự chạy `nlm-auth-load`.
  **Đo LIVE 29-07 nặng thêm:** `doctor` báo `nlm CLI (fast-lane): KHÔNG tìm thấy` trên máy này, và
  `nlm-audit-physical` không kiểm tra được liveness 2 notebook overflow
  (`45739ff7…`, `2d8c2fef…` → `alive:false, error:"nlm CLI không có trên PATH"`). Nghĩa là mọi con số NLM
  trong hồ sơ (kể cả `nlm_status=pushed` của 63 dòng) hiện **chưa neo được LIVE**. Quota `nlm_con_lai=56`
  vẫn chỉ là ESTIMATE. Cần người dùng gia hạn phiên + cài nlm CLI trước lượt rà tiếp.
- **C1b. (MỚI, đo LIVE) `doctor` báo 3 dòng `UNKNOWN_NOTEBOOK_NOT_IN_TOPOLOGY`** — có dòng registry trỏ
  tới `notebook_id` không nằm trong topology đã khai (vd `80742228-ba7a-481c-bd8e-d4115876ed6e`).
  Cần `nlm-reconcile` xác định là notebook cũ đã bỏ hay khai thiếu topology.
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
| ~~4~~ | ~~Gỡ sheet registry trùng~~ — **HUỶ: A1 đã bị bác bỏ, `files_bak_*` là bản sao đúng thiết kế** | — | không làm |
| 5 | Người dùng gia hạn phiên NLM **+ cài nlm CLI**; sau đó `nlm-reconcile` neo trạng thái (C1, C1b, quota) | vận hành | user |
| 6 | Chuẩn hoá vocab `hieuluc` + nhãn DỰ THẢO cho 12 tệp bản so sánh/góp ý (B1, B6) | GHI reg (bulk; field rỗng phải đi `reg_clear`) | duyệt |
| 7 | Đăng ký nốt BC 6193 + quyết chính sách raw-twin (B7) | GHI | duyệt |
| 8 | Dọn locks hết hạn + làm tươi manifest-summary (B8) | GHI GAS | duyệt |
| 9 | Tra NQ Chính phủ cho VD-12 khi có đường mạng tới vbpl.vn/công báo | tra cứu | — |
| 10 | Ghi rõ CƠ SỞ ĐẾM vào output `registry-doctor` (`missing_sohieu`, `duplicate_*`) như `sweep` đã làm với `corpus_basis` (B2b) | sửa code | dev |

*Không món GHI nào được tự chạy trong phiên này. Các lệnh đã chạy đều chỉ-đọc:*
`doctor` · `reg-query [--refresh/--base-also/--limit/--sohieu/--cat]` · `registry-doctor` · `sweep` ·
`profile-list` · `profile-sync` (không `--apply`) · POST `reg_bak_list` (endpoint CHỈ ĐỌC).

---

## F. Bài học phương pháp từ chính lượt rà này

**Đọc spreadsheet qua bộ render ngôn ngữ tự nhiên của Drive là nguồn KHÔNG đáng tin để kết luận cấu trúc.**
Nó nối mọi tab lại mà không ghi tên tab, khiến một **bản sao lùi đúng thiết kế** (`files_bak_20260726152604`)
hiện lên y hệt "sheet dữ liệu thứ hai bị lệch", và khiến **dòng tiêu đề lặp** bị đếm thành một dòng dữ liệu
(91 thay vì 90). Cả hai sai lệch đều tan ngay khi hỏi webapp — nguồn sự thật thật sự.

Quy tắc rút ra, nên áp cho các lượt sau: **mọi khẳng định về registry phải neo `reg-query`/endpoint GAS,
KHÔNG neo bản đọc Drive.** Bản đọc Drive chỉ dùng để phát hiện file mồ côi (thứ webapp không thấy) —
và ngay cả khi đó, kết luận "mồ côi" vẫn phải đối chiếu ngược lại tập `drive_id` LIVE (đã làm ở A4, B7).
