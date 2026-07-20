# THỂ THỨC & KỸ THUẬT TRÌNH BÀY VĂN BẢN — NEO TRI THỨC 4 HỆ (v1.34.77)

> **Vai trò:** reference bắt buộc của skill tra-luat cho mọi việc SOẠN/ĐIỀN/KIỂM văn bản theo thể thức nhà
> nước và của Đảng — cặp đối xứng với `references/VAN_PHONG_HANH_CHINH.md` (văn phong = NỘI DUNG; file này
> = HÌNH THỨC). Là NEO drift-lock cho lệnh `tl the-thuc-check` (R2, kế hoạch
> `D:\Quốc hội\ke-hoach-the-thuc-2026-07-19.md`): hằng `THE_THUC_CRITERIA` trong code phải khớp block
> `NEO-DRIFT-LOCK` cuối file — đổi một phía mà quên phía kia là selftest đỏ.
> **Nguồn:** trích NGUYÊN VĂN từ corpus (verify 2026-07-19). Số liệu KHÔNG được sửa tay khi quy định nguồn
> chưa đổi; quy định đổi = nạp VB mới vào corpus → sửa file này → sửa hằng code → regen golden, một đường.

## 0. NGUỒN CORPUS (drive_id — tra lại bằng `tl doc-text <id>`)

| Hệ | Văn bản | drive_id |
|---|---|---|
| Hành chính | NĐ 30/2020/NĐ-CP chính văn (Đ8, Đ9, Đ25-27) | `1J7wqHmUX3sh3ZLgIqm1YrVUYQWLlTNPjTD1RkneIFd4` |
| Hành chính | NĐ 30/2020 Phụ lục I-VI (docx gốc TNR — nạp lại 19-07, overflow VBQPPL-2) | `1YgArj3UFuC9RY…` (tra `reg-query --sohieu 30-2020-ND-CP` dòng corpus=true row_kind=overflow) |
| VBQPPL | NĐ 78/2025/NĐ-CP (lời văn Chương V Đ60-71) | `1Efh0dU229h75iIGM2kXRGxknci0mOrVFKdD13XCVdl0` |
| VBQPPL | NĐ 187/2025/NĐ-CP (PL I-IV hiện hành) | `19DNiE5Jsk3B3nOUT45FEwgk-xR0e73lqNtRr9KqfjXQ` |
| VBHN | NĐ 250/2026/NĐ-CP | `1w-UfKKEo3gLrNElbdUr…` (tra `reg-query --sohieu 250-2026-ND-CP`) |
| Đảng | QĐ 399-QĐ/TW (thể loại, thẩm quyền, thể thức) | `1jMXEIIaNgsRskFeqruG…` (tra `reg-query --sohieu 399-QD-TW`) |
| Đảng | HD 05-HD/VPTW (kỹ thuật trình bày chi tiết) | `1Lko21mOLzF6xGvP0HAj…` (tra `reg-query --sohieu 05-HD-VPTW`) |
| VBQPPL nhánh QH/UBTVQH/CTN (**HIỆU LỰC**) | NQ 351/2017/UBTVQH14 — GDoc lời văn + **PDF Công báo 287+288 (chú thích lề trên sơ đồ Mẫu 1-16)** | GDoc `19YN7y4_na_G8V3IzJKZEdtHw9M_xuf6W3Uml31k7pLA`; PDF gốc `351_2017_UBTVQH14` (user cấp 19-07 — nguồn số lề) |

**QUAN TRỌNG — quan hệ 78↔187:** Phụ lục I-IV của NĐ 78/2025 **đã bị NĐ 187/2025 THAY THẾ TOÀN BỘ**
(Điều 3 khoản 3 NĐ187, hiệu lực **01/7/2025**); Điều 68 NĐ78 (viện dẫn) áp theo bản sửa của NĐ187. Vì vậy:
quy tắc "chữ" (thành phần, bố cục, đánh số, viện dẫn) đọc ở NĐ78 Đ60-71; mọi thông số "đo được" đọc ở
**Phụ lục I của NĐ 187** — KHÔNG trích phụ lục NĐ78 (bản trong corpus là file đính kèm không bóc được).

**QUAN TRỌNG — NQ 351/2017 VẪN HIỆU LỰC cho VBQPPL của QH/UBTVQH/CTN** (user xác nhận 2026-07-19: chưa có
văn bản thay thế; NĐ78/187 là nghị định của Chính phủ không bãi bỏ được nghị quyết UBTVQH — grep "351"
trong cả 78/187 = 0 hit). Hệ VBQPPL vì vậy TÁCH 2 NHÁNH: **vbqppl_qh** (Luật/Bộ luật/Pháp lệnh/NQ
QH-UBTVQH/NQLT có UBTVQH/Lệnh/QĐ CTN → chuẩn NQ351, §3.4) và **vbqppl** (CP/TTg/Bộ/TANDTC/VKSNDTC/KTNN/
HĐND/UBND → chuẩn NĐ78+PL I NĐ187, §3.2-3.3). Khác biệt đo được lớn nhất: nhánh QH thân văn bản cỡ
**14 CỐ ĐỊNH** (không phải dải 13-14), Quốc hiệu **12 cố định**, Tiêu ngữ **14 cố định**.

## 1. PHÂN LUỒNG 4 HỆ (thứ tự nhận diện của `the-thuc-check --he auto`)

1. Dòng đơn `ĐẢNG CỘNG SẢN VIỆT NAM` (không kèm Quốc hiệu 2 dòng) → **dang**.
2. Số ký hiệu chứa `/VBHN-` → **vbhn**.
3. Số ký hiệu có năm dạng `\d+/\d{4}/…` + tên loại thuộc danh mục VBQPPL → **vbqppl**; trong đó nếu tên
   loại là LUẬT/BỘ LUẬT/PHÁP LỆNH hoặc ký hiệu có QH/UBTVQH/CTN (vd `…/QH15`, `…/UBTVQH15`, `…/CTN`)
   → nhánh **vbqppl_qh** (chuẩn NQ 351/2017 — §3.4).
4. Còn lại (có Quốc hiệu + Tiêu ngữ) → **hanh_chinh**.

Không chắc → người dùng ép `--he`. VB ban hành trước 01/7/2025 (hệ NQ351/NĐ34 cũ): NGOÀI phạm vi kiểm —
chỉ WARN ngày ban hành, không áp ngưỡng cũ (quyết định grill Q6, 2026-07-19).

## 2. HỆ HÀNH CHÍNH — NĐ 30/2020/NĐ-CP + Phụ lục I

### 2.1. Thành phần thể thức (Điều 8)
**9 thành phần chính (k2, bắt buộc):** a) Quốc hiệu và Tiêu ngữ; b) Tên cơ quan, tổ chức ban hành; c) Số,
ký hiệu; d) Địa danh và thời gian ban hành; đ) Tên loại và trích yếu nội dung; e) Nội dung; g) Chức vụ, họ
tên và chữ ký của người có thẩm quyền; h) Dấu, chữ ký số của cơ quan, tổ chức; i) Nơi nhận.
**Bổ sung (k3, tùy loại):** phụ lục; dấu chỉ độ mật/mức độ khẩn/chỉ dẫn phạm vi lưu hành; ký hiệu người
soạn thảo + số lượng bản; địa chỉ cơ quan, email, website, ĐT, Fax.
Ngoại lệ: **công văn** không có tên loại (trích yếu ở ô 5b, sau "V/v"); "Kính gửi" (ô 9a) chỉ với Tờ
trình/Báo cáo (cấp dưới → cấp trên) và Công văn.

### 2.2. Kỹ thuật chung (Phụ lục I, Mục I — nguyên văn)
- Khổ giấy: **A4 (210 mm x 297 mm)**; kiểu trình bày theo chiều dài; bảng biểu không làm phụ lục riêng
  **có thể trình bày theo chiều rộng** (landscape hợp lệ có điều kiện).
- Định lề: "Cách mép trên và mép dưới **20 - 25 mm**, cách mép trái 30 - 35 mm, **cách mép phải 15 - 20 mm**."
- Phông chữ: "Phông chữ tiếng Việt **Times New Roman**, bộ mã ký tự Unicode theo Tiêu chuẩn Việt Nam
  **TCVN 6909:2001**, màu đen."
- Số trang: từ số 1, chữ số Ả Rập, "**cỡ chữ 13 đến 14**, kiểu chữ đứng, được đặt canh giữa theo chiều
  ngang trong phần lề trên của văn bản, không hiển thị số trang thứ nhất."

### 2.3. Bảng cỡ chữ theo thành phần (Phụ lục I Mục II + bảng Mục V)

| Thành phần (ô sơ đồ) | Loại chữ | Cỡ | Kiểu |
|---|---|---|---|
| Quốc hiệu "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" (ô 1) | in hoa | **12–13** | đứng, đậm |
| Tiêu ngữ "Độc lập - Tự do - Hạnh phúc" (ô 1, kẻ ngang dưới dài bằng dòng chữ) | in thường | **13–14** | đứng, đậm |
| Tên CQ chủ quản trực tiếp (ô 2) | in hoa | 12–13 | đứng |
| Tên CQ ban hành (ô 2, kẻ ngang 1/3–1/2 dòng) | in hoa | 12–13 | đứng, đậm |
| Từ "Số:" + ký hiệu (ô 3; `/` giữa số và ký hiệu, `-` giữa nhóm viết tắt; số <10 thêm 0) | thường/hoa | **13** (cố định) | đứng |
| Địa danh, thời gian (ô 4) | in thường | 13–14 | **nghiêng** |
| Tên loại (ô 5a) + trích yếu | in hoa / thường | 13–14 | đứng, đậm |
| Trích yếu công văn (ô 5b, sau "V/v") | in thường | 12–13 | đứng |
| Nội dung (ô 6; thụt đầu dòng 1–1,27 cm; cách đoạn ≥6pt; giãn dòng đơn → tối đa 1,5 lines) | in thường | 13–14 | đứng |
| Phần/Chương/Mục/Tiểu mục/Điều (từ + số, đậm; tiêu đề in hoa đậm) | — | 13–14 | đứng, đậm |
| Khoản (số Ả Rập + `.`) / Điểm (chữ cái + `)`) | in thường | 13–14 | đứng |
| Quyền hạn (TM./Q./KT./TL./TUQ.) + chức vụ người ký (ô 7a) | in hoa | 13–14 | đứng, đậm |
| Họ tên người ký (ô 7b) | in thường | 13–14 | đứng, đậm |
| "Kính gửi" + nơi nhận (ô 9a) | in thường | 13–14 | đứng |
| Từ "Nơi nhận:" (ô 9b) | in thường | **12** (cố định) | nghiêng, đậm |
| Danh sách nơi nhận (đầu dòng `-`, cuối `;`, chốt "Lưu: VT, …") | in thường | **11** (cố định) | đứng |
| Từ "Phụ lục" + số La Mã | in thường | **14** (cố định) | đứng, đậm |
| Tiêu đề phụ lục | in hoa | 13–14 | đứng, đậm |
| Dấu khẩn HỎA TỐC/THƯỢNG KHẨN/KHẨN (khung 30×8/40×8/20×8 mm, mực đỏ) | in hoa | 13–14 | đứng, đậm |
| Chỉ dẫn phạm vi lưu hành (ô 11, khung viền đơn) | in hoa | 13–14 | đứng, đậm |
| Ký hiệu người soạn thảo + số lượng bản (ô 12) | in hoa/số | **11** (cố định) | đứng |
| Địa chỉ CQ/email/website/ĐT/Fax (ô 13) | in thường | 11–12 | đứng |

**Nhất-quán-bậc (footnote bảng Mục V — nguyên văn):** "Cỡ chữ trong cùng một văn bản **tăng, giảm phải thống nhất**, ví dụ: Quốc hiệu cỡ chữ 13, Tiêu ngữ cỡ chữ 14, địa danh và ngày, tháng, năm văn bản cỡ chữ
14 hoặc Quốc hiệu cỡ chữ 12, Tiêu ngữ cỡ chữ 13, địa danh và ngày, tháng, năm văn bản cỡ chữ 13." → bộ
kiểm KHÔNG kiểm dải từng thành phần độc lập; kiểm CẢ VĂN BẢN cùng bậc (cận dưới đồng loạt hoặc cận trên
đồng loạt).

### 2.4. Bản sao (Phụ lục I Phần II)
SAO Y / SAO LỤC / TRÍCH SAO (viết tắt SY/SL/TrS): cụm hình thức sao in hoa 13–14 đậm; bản sao điện tử
định dạng **PDF ≥1.4, ảnh màu, ≥200 dpi, tỷ lệ 100%**, chữ ký số CQ ở ô 14, thông tin cỡ **10**; bản sao
giấy trình bày sau văn bản cần sao, dưới đường kẻ nét liền, 7 thành phần (Đ25 k4 dẫn PL I).

## 3. HỆ VBQPPL — lời văn NĐ 78/2025 (Đ60-71) + thông số PL I NĐ 187/2025

### 3.1. Thành phần thể thức (Đ71 NĐ78)
**Chính (k2):** Quốc hiệu và Tiêu ngữ; tên cơ quan ban hành; số, ký hiệu; địa danh (nếu có); thời gian
thông qua/ban hành; tên loại và trích yếu; nội dung; chức vụ, họ tên, chữ ký; dấu/chữ ký của cơ quan;
nơi nhận (nếu có). **Bổ sung (k3):** phụ lục; dấu độ mật/khẩn; ký hiệu người soạn + số bản; địa chỉ CQ,
email, cổng/trang TTĐT.

### 3.2. Kỹ thuật chung (PL I NĐ187, Mục 1 Phần I — nguyên văn)
- Khổ A4 (210 mm x 297 mm), trình bày chiều dài; bảng biểu có thể chiều rộng.
- Định lề: "Cách mép trên và mép dưới, **mép phải 15 - 20 mi-li-mét (mm)**, **cách mép trái 30 - 35 mi-li-mét (mm)**." ← CHÚ Ý: trên/dưới 15-20 **KHÁC** hệ hành chính (20-25).
- Phông: Times New Roman, Unicode TCVN 6909:2001, màu đen.
- Số trang: số Ả Rập, "**cỡ chữ 13, kiểu chữ đứng, không hiển thị số trang thứ nhất**, đặt canh giữa theo
  chiều ngang trong phần lề trên" ← 13 CỐ ĐỊNH (khác hành chính 13-14).

### 3.3. Cỡ chữ theo thành phần (PL I NĐ187, Phần II-III)

| Thành phần | Loại chữ | Cỡ | Kiểu |
|---|---|---|---|
| Quốc hiệu | in hoa | 12–13 | đứng, đậm (trên cùng bên PHẢI) |
| Tiêu ngữ | in thường | 13–14 | đứng, đậm, kẻ ngang dưới |
| Tên cơ quan ban hành (trên cùng bên TRÁI, kẻ 1/3–1/2) | in hoa | 12–13 | đứng, đậm |
| Từ "Số:" + số / ký hiệu (`/` giữa số-năm-ký hiệu, `-` giữa nhóm; năm đủ 4 số; <10 thêm 0) | thường / in hoa | **13** | đứng |
| **Tên luật, pháp lệnh** | in hoa | **14** (cố định) | đứng, đậm, canh giữa |
| Tên loại VB khác + tên gọi | in hoa 14 / thường 13–14 | 14 / 13–14 | đứng, đậm |
| Địa danh, ngày tháng năm | in thường | 13–14 | nghiêng |
| **Căn cứ ban hành** (mỗi căn cứ xuống dòng, cuối `;`) | in thường | **14** (cố định) | **nghiêng** |
| "QUYẾT NGHỊ:"/"LỆNH:"/"QUYẾT ĐỊNH:" (NQ QH-UBTVQH, lệnh/QĐ CTN) | in hoa | 14 | đứng, đậm, dòng riêng |
| Nội dung (thụt 1–1,27 cm; đoạn ≥6pt; dòng đơn → 1,5 lines) | in thường | 13–14 | đứng |
| Từ "Phần"/"Chương" + số **La Mã** | in thường | 13–14 | đứng, đậm |
| TÊN phần/chương | in hoa | **14** | đứng, đậm |
| Mục/Tiểu mục (từ + số **Ả Rập**; tên in hoa 13–14 đậm) | in thường | 13–14 | đứng, đậm |
| Điều (từ "Điều" + số Ả Rập + `.`; cách lề trái 1–1,27 cm) | in thường | 13–14 | đứng, đậm |
| Khoản (số Ả Rập + `.`) / Điểm (chữ cái tiếng Việt + `)`) | in thường | 13–14 | đứng |
| **Chức vụ người ký** ("TM.", "KT.", "Q." cùng cỡ) | in hoa | **13** (cố định) | đứng, đậm |
| Họ tên người ký | in thường | 13–14 | đứng, đậm |
| Từ "Nơi nhận:" | in thường | 12 | nghiêng, đậm |
| Danh sách nơi nhận (đầu `-`, cuối `;`) | in thường | **11** | đứng |
| Từ "Phụ lục" + số La Mã / tiêu đề phụ lục | thường / in hoa | 13–14 | đứng, đậm |

**Số, ký hiệu VBQPPL (PL I NĐ187 Phần II.3):** luật/NQ QH, pháp lệnh/NQ UBTVQH = *loại + số + năm + viết
tắt CQ + số khóa QH* (khóa bằng **số La Mã**); NQ/TT liên tịch = *số + năm + viết tắt loại + viết tắt các
CQ cùng ban hành*; lệnh/QĐ CTN = *số + năm + viết tắt loại + viết tắt chức danh*; VBQPPL khác = *số + năm
+ viết tắt loại + viết tắt CQ* (vd `250/2026/NĐ-CP`). Đánh số riêng từng loại, bắt đầu 01 mỗi năm.

**Bố cục (Đ63 NĐ78):** phần → chương → mục → tiểu mục → điều → khoản → điểm; đánh số điều bằng số Ả Rập
từ "Điều 1"; mỗi điểm một ý; phần/chương/mục/tiểu mục/điều phải có tên. Số chỉ khóa QH + số thứ tự
phần/chương = **số La Mã** (Đ64 k3).

### 3.4. Nhánh QH/UBTVQH/CTN — NQ 351/2017/UBTVQH14 (**VẪN HIỆU LỰC**, user xác nhận 2026-07-19)

Phạm vi (Đ1): VBQPPL của Quốc hội, UBTVQH, Chủ tịch nước + NQ liên tịch có UBTVQH (KHÔNG gồm Hiến pháp).
Hiệu lực từ 20/5/2017, thay NQ 1139/2007/UBTVQH11; chưa có văn bản thay thế.

| Thành phần (điều NQ351) | Loại chữ | Cỡ | Kiểu |
|---|---|---|---|
| Quốc hiệu (Đ30) | in hoa | **12** (cố định) | đứng, đậm |
| Tiêu ngữ (Đ30; gạch nối giữa các từ, có cách chữ; kẻ ngang dưới) | in thường | **14** (cố định) | đứng, đậm |
| Tên cơ quan ban hành (Đ31; kẻ 1/3–1/2; NQ QH/UBTVQH và lệnh/QĐ CTN: dòng in hoa 14 trên phần căn cứ) | in hoa | **12** | đứng, đậm |
| "Số:"/"… số" + ký hiệu (Đ32; sau "Số" có `:`; <10 thêm 0) | thường / in hoa | **13** | đứng |
| Tên văn bản luật/pháp lệnh (Đ33; tên loại + tên gọi dòng riêng; chú thích "(kèm theo…)" 14 nghiêng) | in hoa / thường | **14** | đứng, đậm |
| Căn cứ ban hành (Đ34; "QUYẾT NGHỊ"/"LỆNH"/"QUYẾT ĐỊNH" in hoa 14 đậm dòng riêng + `:`) | in thường | **14** | nghiêng |
| Nội dung (Đ35; thụt 1–1,27 cm; đoạn ≥6pt; **dòng: đơn hoặc từ 15pt trở lên** — không có trần 1,5 lines) | in thường | **14** (cố định) | đứng |
| Phần/Chương (La Mã) · Mục/Tiểu mục (Ả Rập) · Điều · Khoản · Điểm (chữ cái) — tiêu đề in hoa 14 đậm | — | **14** | đứng (đề mục đậm) |
| Thời điểm QH thông qua (Đ36, dưới điều cuối — luật/NQ QH; khóa QH số La Mã, kỳ họp Ả Rập) | in thường | 14 | nghiêng |
| Địa danh, ngày tháng năm (Đ36 k2 — pháp lệnh/NQ UBTVQH/NQLT/lệnh/QĐ CTN, cùng dòng số ký hiệu) | in thường | 14 | nghiêng |
| Chức vụ người ký (Đ37) | in hoa | **13** | đứng, đậm |
| Từ "Nơi nhận" (Đ38 — NQLT và QĐ CTN) | in thường | **12** | nghiêng, đậm |
| Danh sách nơi nhận (Đ38; "Lưu: HC, …") | in thường | **11** | đứng |
| Số trang (Đ39 k3; VB kèm theo đánh số riêng) | — | **13** | đứng, không trang 1 |

**Khổ giấy/lề/phông (Đ39):** A4 210×297; phông Times New Roman Unicode TCVN 6909:2001; số trang cỡ 13.
**Định lề (Đ39.1 dẫn "theo Phụ lục"; số lấy từ chú thích lề trên sơ đồ Mẫu 1-16, PDF Công báo 287+288,
user cấp 19-07 — nhất quán mọi mẫu):** lề trên **20–25 mm** · lề dưới **20–25 mm** · lề trái **30–35 mm**
· lề phải **15–20 mm** (= trùng hệ hành chính NĐ30). Từ v1.34.76 bộ kiểm nhánh vbqppl_qh áp lề FAIL như
các hệ khác (trước đó WARN dải-hợp vì corpus GDoc thiếu sơ đồ số).

## 4. HỆ VBHN — NĐ 250/2026/NĐ-CP (hiệu lực **01/7/2026**)

**Font/lề/cỡ chữ:** NĐ250 KHÔNG tự quy định — nguyên văn mục I.1: khổ giấy, kiểu trình bày, định lề,
phông, cỡ, kiểu chữ "được thực hiện **tương tự theo quy định của pháp luật về kỹ thuật trình bày văn bản
quy phạm pháp luật**" → dùng ngưỡng hệ VBQPPL (§3). Riêng **số trang: cỡ chữ 13 đến 14** (mục XII).

**Checklist CẤU TRÚC (phần kiểm riêng của hệ VBHN — mục II-XV Phụ lục NĐ250):**
1. **Số, ký hiệu** = `STT/NĂM-ký-xác-thực/VBHN-<viết tắt loại>-<viết tắt CQ ký xác thực>`; số đánh riêng
   theo năm, <10 thêm 0; `/` giữa số-năm, `-` giữa nhóm. Ví dụ nguyên văn: **`01/2026/VBHN-LQ-VPQH`**,
   `01/2026/VBHN-NĐ-BQP`, `01/2026/VBHN-QĐC-BNV`, `01/2026/VBHN-TT-BTP`.
2. **Bảng viết tắt loại (mục II.1):** Bộ luật/Luật QH = **LQ**; Pháp lệnh = PL; Nghị quyết = NQ; NQ của
   UBTVQH = **NQTV**; NQ liên tịch = NL; Lệnh CTN = LC; Quyết định CTN = **QĐC**; Nghị định = NĐ; Quyết
   định = QĐ; Thông tư = TT; Thông tư liên tịch = TL; QĐ của Chủ tịch UBND cấp tỉnh = QĐCT.
3. **Tên VBHN** = tên loại + tên VB được sửa đổi bổ sung; NGAY SAU tên: khối **liệt kê các văn bản được
   hợp nhất** (đủ tên, số, ký hiệu, ngày thông qua/ký, cơ quan, ngày hiệu lực); không hợp nhất các VB sửa
   đổi với nhau.
4. **Chú thích chân trang đánh số** (mục V-XI): ký hiệu số mũ ngay sau đối tượng bị tác động (tên VB/phần/
   chương/mục/điều/khoản/điểm/đoạn/cụm từ); ghi chú cuối trang dưới **đường kẻ ngang**; mẫu câu cố định
   theo loại tác động: "*Điều này được sửa đổi/sửa đổi, bổ sung/thay thế theo quy định tại … của …, có
   hiệu lực kể từ ngày …*" / "*… được bổ sung theo …*" / bãi bỏ / tạm ngưng; riêng **đính chính** ghi
   ngày ban hành văn bản đính chính (không ghi "có hiệu lực").
5. **Khối ký xác thực** (mục XIII) cuối văn bản, ngăn với nội dung bằng đường kẻ ngang dài nét liền:
   "**XÁC THỰC VĂN BẢN HỢP NHẤT**" + địa danh-ngày + chức vụ người ký xác thực + chữ ký, dấu + họ tên;
   "Nơi nhận" có mục đăng Công báo + Cơ sở dữ liệu quốc gia về pháp luật.

## 5. HỆ VĂN BẢN CỦA ĐẢNG — QĐ 399-QĐ/TW + HD 05-HD/VPTW

### 5.1. Thành phần (Đ15 QĐ399 — 9 thành phần bắt buộc)
1) Tiêu đề "ĐẢNG CỘNG SẢN VIỆT NAM"; 2) tên cơ quan ban hành; 3) số và ký hiệu; 4) địa danh và ngày
tháng năm; 5) tên loại và trích yếu; 6) nội dung; 7) quyền hạn, chức vụ, họ tên, chữ ký; 8) dấu của cơ
quan; 9) nơi nhận. (Bổ sung Đ16: phụ lục, dấu mật/khẩn, chỉ dẫn phạm vi phổ biến/dự thảo/tài liệu hội
nghị, ký hiệu người soạn + số bản, thông tin liên hệ.)

**25 thể loại (Đ5 QĐ399):** Cương lĩnh chính trị, Điều lệ Đảng, Chiến lược, Nghị quyết, Quyết định, Chỉ
thị, Kết luận, Quy chế, Quy định, Thông tri, Hướng dẫn, Thông báo, Thông cáo, Tuyên bố, Lời kêu gọi, Báo
cáo, Kế hoạch, Quy hoạch, Chương trình, Đề án, Phương án, Dự án, Tờ trình, Công văn, Biên bản (+ 8 giấy
tờ hành chính Đ6). Thẩm quyền theo cấp: Đ8-13 (NGOÀI phạm vi kiểm format — backlog).

### 5.2. Kỹ thuật trình bày (HD05 Phần II mục IV — nguyên văn; lề ĐƠN TRỊ, không dải)
- Phông: Times New Roman, Unicode TCVN 6909: 2001 (nguồn HD05 in có khoảng trắng sau "6909:"), màu đen.
- Khổ A4; giấy tờ hành chính được dùng A4 hoặc A5.
- **Định lề mặt trước:** lề trên **20 mm** · lề dưới **20 mm** · lề trái **30 mm** · lề phải **15 mm**
  (in 2 mặt: mặt sau đảo trái 15/phải 30).
- Nội dung: dàn đều 2 lề; đầu dòng lùi ~10 mm; Spacing ≥6pt; **Line spacing từ 18pt đến 22pt (Exactly)**;
  kết thúc có dấu chấm.
- Số trang: số Ả Rập, cách mép trên 10 mm, canh giữa, không hiển thị trang thứ nhất.

### 5.3. Bảng cỡ chữ (HD05 Phụ lục 2 — **đã đối chiếu TRỌN bảng 20-07**, bản HD05 ngày 27/5/2026)

| TT | Thành phần | Loại chữ | Cỡ | Kiểu |
|---|---|---|---|---|
| 1 | Tiêu đề "ĐẢNG CỘNG SẢN VIỆT NAM" (góc phải dòng đầu, kẻ ngang dưới dài bằng tiêu đề) | in hoa | **15** | đứng, đậm |
| 2 | Tên CQ cấp trên trực tiếp / tên CQ ban hành (góc trái; dưới có **dấu sao `*`**) | in hoa | **14** | đứng / đứng, đậm |
| 3 | Số và ký hiệu — `Số 127-QĐ/TW` (KHÔNG dấu hai chấm; **`-` trước viết tắt loại, `/` trước viết tắt CQ** — NGƯỢC với nhà nước; QĐ = Quyết định ∪ Quy định; CT=Chỉ thị, CTr=Chương trình, TT=Thông tri, TTr=Tờ trình; CQ đại hội = ĐH) | in thường | **14** | đứng |
| 4 | Địa danh, ngày tháng năm | in thường | 14 | nghiêng |
| 5 | Thể loại văn bản | in hoa | **15-16** | đứng, đậm |
| 5 | Trích yếu nội dung (ngăn với nội dung bằng **5 dấu gạch nối `-----`**) | in thường | **14-15** | đứng, đậm |
| 5 | Trích yếu thể loại công văn | in thường | **12** | nghiêng |
| 6 | Nội dung + Phần/Chương (La Mã hoặc chữ)/Mục (Ả Rập)/Điều/Khoản/Điểm | in thường | **14-15** | đứng (đề mục: đậm) |
| 7 | Quyền hạn (T/M…) / chức vụ / họ tên người ký | in hoa/in hoa/thường | 14 | **đậm / ĐỨNG (KHÔNG đậm) / đậm** |

> **⚠ ĐÍNH CHÍNH DỄ SAI — CHỨC VỤ người ký VB ĐẢNG KHÔNG IN ĐẬM.** HD05 PL2 mục 7 tách rõ: *quyền hạn* (`T/M …`, `K/T …`) = **Đứng, đậm**; *chức vụ* (`BÍ THƯ`, `PHÓ BÍ THƯ`, `CHÁNH VĂN PHÒNG`…) = chỉ **Đứng**. Nhà nước thì NGƯỢC LẠI: NĐ30 PL I II.7.đ và NQ351 Đ37 k1 đều cho quyền hạn VÀ chức vụ **cùng đậm**. Builder để cả hai đậm tới v1.34.93 (lọt vào VB đã giao `BC_74_DU_UBQLV_chuyen_doi_so_moi.docx`); v1.34.94 vá + thêm cờ `TT-CHUC-VU-DAM`. Cùng họ với đính chính "Nơi nhận VB Đảng không đậm" ở §6 — **hai chỗ này là bẫy chéo hai hệ dễ nhầm nhất**.

| 9 | "Kính gửi"/"Kính trình" | in thường | 14 | nghiêng |
| 9 | Từ "Nơi nhận:" (có **gạch chân**) / danh sách nơi nhận | in thường | **14** / **12** | đứng |
| 11 | Dấu chỉ mức độ khẩn | in hoa | 14 | đứng, đậm |
| 12 | Chỉ dẫn phạm vi lưu hành (vd TÀI LIỆU HỘI NGHỊ) / chỉ dẫn dự thảo | in hoa / thường | **12** / 14 | đậm / nghiêng |
| 13 | Ký hiệu người soạn thảo + số bản phát hành | in thường | **11** | đứng |
| 14 | Thông tin liên hệ cơ quan | in thường | **10** | đứng |
| 15 | Số trang văn bản, phụ lục | in thường | **14** | đứng |

Bản sao (HD05 PL 3): dấu "Bản sao văn bản" hình chữ nhật **80 mm x 50 mm, mực đỏ**, chữ in hoa cỡ 13
đậm; ký hiệu bản sao ghi chung **BS**. HD05 thay thế HD 36-HD/VPTW (04/3/2018).

## 6. QUY TẮC XUYÊN HỆ (cho bộ kiểm)

1. **Nhất-quán-bậc cỡ chữ** (§2.3) — áp hệ nhà nước; hệ Đảng dải 14-15 cũng kiểm đồng bậc.
2. Ngày <10 và tháng <3 (hệ hành chính)/số <10 (mọi hệ): thêm số 0 phía trước.
3. Đơn vị đo docx: mm = twips × 25,4 / 1440 (1 mm ≈ 56,69 twips); cỡ chữ pt = w:sz/2 (half-points);
   so dải với dung sai ±1 mm. Cỡ chữ tiếng Việt do `w:sz` chi phối (Latin script), KHÔNG dùng `w:szCs`.
4. Resolve font/cỡ BẮT BUỘC fallback 3 tầng: run (`w:rPr`) → style `Normal` → `docDefaults` — file
   convert thường bỏ trống run (xem §8). Regex XML phải dung sai khoảng trắng (`<w:sz w:val="28" />`).
5. Đa section: kiểm lề từng `sectPr`; section landscape → WARN kèm ghi chú "hợp lệ nếu chứa bảng biểu"
   (NĐ30 I.2 / NĐ187 I.2 đều cho phép).

6. **Quốc hiệu và tên cơ quan/đơn vị ban hành phải nằm gọn trên MỘT dòng (không ngắt dòng)** — khi SOẠN/ĐIỀN, chọn cỡ chữ và độ rộng ô đủ để cả dòng "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" và dòng tên cơ quan/đơn vị (ví dụ "TIỂU BAN LAO ĐỘNG, VIỆC LÀM") không bị vắt sang dòng thứ hai. Thực chứng: quốc hiệu vỡ dòng khi để cỡ 13 trong ô hẹp → đặt khối tiêu đề cỡ 12 (Quốc hiệu 12–13, tên cơ quan 12–13 theo §2.3/§3.3) và nới ô là đủ. Bộ kiểm: WARN `QUOC_HIEU_WRAPPED` / `TEN_CQ_WRAPPED` khi một trong hai bị ngắt dòng.

7. **Thụt đầu dòng áp cho TOÀN VĂN BẢN, trừ bảng** — mọi đoạn thân, KỂ CẢ đề mục (1., 2., …, 3.1., 6.1., …) và gạch đầu dòng, dùng thụt dòng đầu 1 cm (567 twips — ngang mốc "1" trên thước; cận dưới của dải cho phép 1–1,27 cm): DÒNG ĐẦU lùi vào, các DÒNG SAU trở về sát lề trái (căn đều hai biên). Gạch đầu dòng đặt lề trái = 0, thụt dòng đầu = 567 twips (1 cm), ký tự "-" ở vị trí thụt — KHÔNG dùng thụt treo (dòng tiếp KHÔNG thụt theo chữ). Đây là kiểu trình bày của văn bản gốc (NĐ30 ô 6 · NQ351 Đ35). Các bảng (khối tiêu đề, khối chữ ký) KHÔNG áp thụt này.

8. **Giá trị KHUYẾN NGHỊ khi TẠO file (nằm trong dải cho phép — KHÔNG đổi drift-lock §10)** — lề: trên/dưới 20 mm (1134 twips), trái 30 mm (1701 twips), phải 18–20 mm (1017–1134 twips); khối tiêu đề Quốc hiệu + tên cơ quan cỡ 12, Tiêu ngữ cỡ 13, ô đủ rộng để mỗi khối gọn MỘT dòng (tham chiếu: ô trái ~4694, ô phải ~5546 twips); gạch chân dưới tên cơ quan và Tiêu ngữ dùng GẠCH CHÂN CẤP CHỮ (run underline), KHÔNG dùng viền đoạn có thụt lề (làm hẹp vùng chữ → vỡ dòng); thân + đề mục + gạch đầu dòng cỡ 14, thụt dòng đầu 1 cm (567 twips), căn đều hai biên, giãn dòng 1,5. Khi KIỂM (`the-thuc-check`) vẫn áp dải rộng §10 (thụt 1–1,27 cm đều đạt).

9. **HAI GẠCH PHẢI ĐỒNG CẤU TRÚC (§6.9)** — gạch dưới tên cơ quan (ô trái) và gạch dưới Tiêu ngữ (ô phải) PHẢI cùng MỘT cơ chế: **ĐOẠN RIÊNG** chứa NBSP gạch chân, cùng chỉ số đoạn trong ô, cùng cỡ chữ, cùng `line…exact`. KHÔNG dùng gạch-chân-cấp-chữ cho Tiêu ngữ trong khi ô trái dùng đoạn riêng — hai cơ chế khác nhau thì KHÔNG BAO GIỜ ngang nhau. Kiểm: chuỗi `w:line` của 2 ô phải GIỐNG HỆT. **Độ dài gạch TÍNH bằng công thức, KHÔNG căn tay:** `n_NBSP = len(chữ) × K × pt_chữ × tỷ_lệ ÷ (0.25 × pt_gạch)`; `K = 0.62` (IN HOA) | `0.50` (in thường có dấu); NBSP rộng 0.25em; `tỷ_lệ` = **0.42** cho tên cơ quan/trích yếu (giữa dải 1/3–1/2 NĐ30) · **1.00** cho Tiêu ngữ (bằng độ dài dòng chữ, NĐ30 Mục II.1). **TUYỆT ĐỐI KHÔNG vẽ gạch bằng shape/drawing** — kích thước cứng, không co theo chữ mới khi điền mẫu (cờ `TT-GACH-SHAPE`).
10. **BẢNG KHÔNG ĐƯỢC RỘNG HƠN VÙNG CHỮ (§6.10)** — `tblW ≤ pgSz.w − lề trái − lề phải`. Lỗi kinh điển khi chép khung từ mẫu có lề khác: mẫu để `tblW=9531` (hợp lề phải 15mm), chỉnh lề phải lên 20mm thì vùng chữ còn 9071 → **bảng tràn lề ~3mm**. Luôn TÍNH bề rộng bảng từ `sectPr`, không chép hằng số (cờ FAIL `TT-BANG-TRAN-LE`).
11. **CÂN KHOẢNG QUANH GẠCH (§6.11)** — khoảng TRÊN gạch = chiều cao dòng đoạn gạch; khoảng DƯỚI gạch = `Before` của đoạn kế (+ ~2pt đệm dòng). Đặt hai giá trị bằng nhau (khuyến nghị: gạch `line 8pt exact`, đoạn kế `Before 6pt`) thì "Số:…" và "…, ngày… tháng… năm…" không bị hút sát lên gạch.
12. **VIỀN Ô PHẢI `nil` ĐỦ BỐN CẠNH (§6.12)** — khai `<w:tcBorders>` mà chỉ đặt `left/bottom/right = nil`, **sót `top`**, thì cạnh trên kế thừa và hiện thành đường kẻ ngang lạ ngay trên Quốc hiệu. Luôn nil cả `top/left/bottom/right` (cờ `TT-VIEN-O-SOT`).
13. **KHỐI CUỐI VĂN BẢN (§6.13)** — "Nơi nhận" (trái) và khối chữ ký (phải) đặt trong **bảng 2 ô không viền** để cân đối; để đoạn xếp chồng thì dòng chức vụ canh trái còn họ tên canh giữa → lệch. Bảng KHÔNG có "space before" nên phải chèn **đoạn đệm ~12pt phía trên**. Chừa **≥5 dòng trống (~26mm)** giữa chức vụ và họ tên cho chữ ký + dấu tròn (đường kính 36mm). Dọn sạch **đoạn rỗng ở đầu văn bản** kế thừa từ mẫu (cờ `TT-DONG-TRONG-DAU`).

14. **GẠCH ÁP SÁT CHỮ CỦA NHÁNH MÌNH — KHÔNG ép hai nhánh cân số đoạn (§6.14)** — khi tên cơ quan (nhánh trái) dài phải xuống 2 dòng còn Quốc hiệu/tiêu đề (nhánh phải) chỉ 1 dòng, **KHÔNG chèn đoạn đệm rỗng** để ép hai ô cùng số đoạn: đệm sẽ đẩy gạch rơi xuống xa chữ. Hai nhánh **không bắt buộc ngang bằng nhau** khi số dòng lệch, nhưng gạch phải **ôm sát chữ** của nhánh mình — HD05 mục 1.2 định nghĩa gạch là thứ *"ngăn cách tiêu đề với địa danh"*, nên nó phải nằm ngay dưới tiêu đề. (Chỉ khi hai nhánh TỰ NHIÊN cùng số dòng thì §6.9 mới cho gạch ngang nhau.)
15. **CHIỀU CAO DÒNG PHẢI ≥ CỠ CHỮ với đoạn có CHỮ THẬT (§6.15)** — đặt `line…exact` nhỏ hơn cỡ chữ thì Word **cắt ngọn ký tự**: dấu sao (*) 14pt trong dòng 8pt exact chỉ còn lại chân, nhìn như vết bẩn. Chỉ đoạn **GẠCH** (toàn NBSP gạch chân, không nét chữ nhô lên) mới được ép `line` nhỏ (7–8pt). Đoạn có chữ: dùng `atLeast`, hoặc `exact ≥ cỡ chữ`.
16. **CHỦ QUẢN vs BAN HÀNH khi đơn vị trực thuộc ra văn bản (§6.16)** — đơn vị cấp vụ/cục/phòng ra văn bản nhân danh mình thì: dòng trên = **tên cơ quan chủ quản** (in hoa, cỡ 12–13, **đứng, KHÔNG đậm**), dòng dưới = **tên đơn vị ban hành** (in hoa, cỡ 12–13, **ĐẬM**, có gạch dưới 1/3–1/2). Ký hiệu lấy theo **đơn vị ban hành** (vd `Số: 187/BC-CNHT`), người ký ghi **chức vụ đứng một mình** (`VỤ TRƯỞNG`) — KHÔNG dùng `TL.`/`KT.` vì không ký thay ai. Ví dụ đúng: `ỦY BAN QUẢN LÝ VỐN NHÀ NƯỚC TẠI DOANH NGHIỆP` (chủ quản) / `VỤ CÔNG NGHỆ VÀ HẠ TẦNG` (ban hành).

17. **HỆ vbqppl_qh KHÔNG theo bậc cỡ chữ của NĐ30 (§6.17)** — sơ đồ 19 mẫu Phụ lục I NQ 351/2017 quy định **Quốc hiệu 12 · Tiêu ngữ 14** (bậc **+2pt**), riêng Mẫu 16 (quyết định của Chủ tịch nước) là 13/14 (+1pt). Quy tắc "Tiêu ngữ = Quốc hiệu + 1pt" của NĐ30 Mục V **chỉ áp cho hành chính/vbqppl/vbhn** — áp nhầm cho hệ này thì MỌI VBQPPL của Quốc hội đều bị cảnh báo oan (lỗi tồn đến v1.34.85, trong khi NEO cuối file đã ghi đúng `quoc_hieu=12-12 tieu_ngu=14-14`). Đặc trưng khác của hệ: **KHÔNG có gạch dưới tên gọi văn bản**; căn cứ in **nghiêng**; họ tên người ký cỡ **14** trong khi chức vụ cỡ **13**.

18. **BA DẠNG THIẾU THÀNH PHẦN THEO THIẾT KẾ của NQ351 (§6.18)** — không được tính là sai sót:
    - **Luật, bộ luật, nghị quyết của Quốc hội**: KHÔNG có địa danh, ngày tháng ở phần mở đầu (Đ3 k1) — thời điểm Quốc hội thông qua ghi ở CUỐI văn bản, phân cách bằng **đường kẻ ngang liền từ lề trái đến lề phải** (Đ36 k1). Chỉ pháp lệnh, nghị quyết của UBTVQH, nghị quyết liên tịch, lệnh/quyết định của Chủ tịch nước mới có địa danh.
    - **Mẫu 6b, 11b — văn bản ban hành kèm theo nghị quyết**: KHÔNG có số ký hiệu, địa danh, căn cứ; thay vào đó là dòng *"(Ban hành kèm theo Nghị quyết số: … ngày … của …)"* in nghiêng.
    - **Mẫu 14 — phụ lục ban hành kèm theo VBQPPL**: thêm nữa là KHÔNG có Quốc hiệu/Tiêu ngữ và KHÔNG có người ký. ⚠ Bộ kiểm bỏ qua nhánh nhà nước cho dạng này thì phải **chặn hẳn**, đừng để rơi xuống nhánh Đảng đòi "ĐẢNG CỘNG SẢN VIỆT NAM".
    Nhận diện: có chuỗi `(Ban hành kèm theo` ở phần đầu ⇒ dạng kèm theo; thêm điều kiện mở đầu bằng `PHỤ LỤC` ⇒ Mẫu 14. Địa danh: bám ký hiệu CỦA CHÍNH văn bản (match `Số: n/năm/KH` ĐẦU TIÊN) — không bám `QH\d` trôi nổi vì căn cứ hay dẫn *"Luật … số 57/2014/QH13"*.

19. **KHE GIỮA NỘI DUNG VÀ KHỐI KÝ — KHÔNG CÓ QUY ĐỊNH ĐỊNH LƯỢNG (§6.19)** — đã rà NĐ 30/2020 Phụ lục I (Mục II.6.e và Mục IV *Sơ đồ bố trí các thành phần thể thức*) và NQ 351/2017 (Đ35, Đ37): **không văn bản nào ấn định khoảng cách này**. Ràng buộc duy nhất là *"khoảng cách giữa các đoạn văn tối thiểu 6pt"* và giãn dòng (đơn → 1,5 lines ở NĐ30; ≥15pt ở NQ351). Sơ đồ Mục IV vẽ ô 6 (nội dung) và ô 7a (chức vụ người ký) ở **hai băng tách rời** — tức có khe rõ ràng — nhưng chỉ ghi số cho lề trang (20-25 / 30-35 / 15-20mm), không ghi số cho khe. Đo tỷ lệ trên chính sơ đồ (khe ô6→ô7a ÷ chiều cao vùng chữ) ≈ **8,4mm ≈ 24pt** ⇒ lấy làm mặc định của builder (`spec.dem_ky_pt`, sàn 6pt). **Kết luận cho người soạn: đây là lựa chọn trình bày, không phải quy định — 12pt là quá sát, 24-36pt nhìn cân.**

20. **QUỐC HUY (Mẫu 15a/15b/16 NQ351) KHÔNG chèn bằng đoạn rỗng (§6.20)** — chừa chỗ bằng một đoạn văn bản trống thì Word hiển thị đúng là **một dòng trống ngay trên tên cơ quan** (bộ kiểm cờ `TT-DONG-TRONG-DAU`). Quốc huy là **ảnh nổi**, chèn đè lên phía trên khối tiêu đề.

34. **TẤT ĐỊNH HOÁ — BẢNG ĐẶC TẢ THÀNH PHẦN × HỆ (§6.34)** — `_the_thuc_criteria()` (NEO-DRIFT-LOCK cũ) chỉ khoá **ngưỡng SỐ**: cỡ chữ, lề, thụt. Nhưng **mọi lỗi thực chiến 20-07 đều nằm ở thứ KHÔNG được khoá**: kiểu chữ (đậm/nghiêng/gạch chân), canh lề, loại thụt. Bổ sung `_tt_dac_ta()` — mỗi ô là `(cỡ, kiểu, canh, thụt, căn_cứ)` cho **48 thành phần × 3 hệ**, `thut` phân biệt `fl:<tw>` (thụt DÒNG ĐẦU) với `left:<tw>` (thụt TRÁI cả khối). Test `r170` dựng văn bản thật cho từng hệ rồi đối soát **từng thành phần** với bảng ⇒ builder và bảng không thể trôi khỏi nhau; đổi bảng mà không đổi builder (hoặc ngược lại) là test ĐỎ ngay.

    **Ba chỗ ba hệ THỰC SỰ khác nhau — bảng làm chúng hiện rõ, đây đúng là ba lỗi đã mắc:**

    | Thành phần | hành chính | VBQPPL Quốc hội | Đảng |
    |---|---|---|---|
    | `chuc_vu_ky` | đậm | đậm | **in thường** (HD05 PL2 mục 7) |
    | `noi_nhan_tu` | đậm + nghiêng | đậm + nghiêng | **gạch chân**, không đậm |
    | `dieu` | — | thụt **TRÁI** 567 (NQ351 Đ35 k2c *"cách lề trái"*) | thụt **DÒNG ĐẦU** 567 (HD05 6.2.2 *"khi xuống dòng… lùi vào"*) |

    ⚠ Sửa `_tt_dac_ta()` = sửa hành vi builder — **phải kèm căn cứ nguyên văn**, không "chỉnh cho đẹp".

33. **BỐ CỤC THÂN VB ĐẢNG — CHƯƠNG/MỤC CANH GIỮA, ĐIỀU DÀN ĐỀU (§6.33)** — HD05 mục 6.2.3 nguyên văn: *(a)* từ **"Phần"/"Chương"** + số thứ tự trình bày cùng một dòng, **CHÍNH GIỮA hai lề**; **tên** của phần/chương ở **dòng liền kề phía dưới** (cũng chính giữa, in hoa); *(b)* từ **"Mục"** + số thứ tự cũng **chính giữa**, tên mục ở dòng liền kề dưới; *(c)* từ **"Điều"**, số thứ tự và tên điều **cùng một dòng**, số dùng chữ số Ả-rập và **SAU SỐ CÓ DẤU CHẤM (.)** — ví dụ PL2: `Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng`. Điều KHÔNG canh giữa ⇒ theo 6.2.2: **dàn đều hai lề, thụt đầu dòng 10mm**. Cỡ/kiểu (PL2 mục 6): Phần/Chương/Mục/Điều + tên đều **14-15 đứng ĐẬM**; **khoản, điểm 14-15 đứng KHÔNG đậm**. Cờ `TT-CHUONG-CANH-GIUA`. ⚠ Số thứ tự phần/chương dùng **chữ số La Mã hoặc ghi bằng chữ** (`Chương II`, `Phần thứ hai`); mục dùng **Ả-rập** (`Mục 1`).

32. **KHỐI TIÊU ĐỀ MẶC ĐỊNH CHIA ĐÔI (§6.32)** — **đo hình học THẬT của chính file HD 05-HD/VPTW**: `tblGrid` khối tiêu đề = **4612 | 4675** trên vùng chữ 9071 ⇒ **~50/50**, tâm khối phải ở **74,8%**. Nếu chỉ cấp cho ô phải đúng bề rộng tiêu đề cần (hệ Đảng: 4256 = 45,5%) thì ô phải hẹp và **bị đẩy sang phải** — tâm 77,2%, nhìn lệch (user 20-07). Quy tắc: `wr = min(max(need_r, 50%×W), 62%×W)` — **mặc định chia đôi, chỉ NỚI ô phải khi Quốc hiệu/tiêu đề không đủ chỗ một dòng** (§6.6). Hệ nhà nước: Quốc hiệu 34 ký tự cần 58% nên giữ nguyên như cũ, không hồi quy.

> **★ CÁCH LÀM ĐÚNG khi user kêu "lệch":** đừng suy từ nguyên tắc canh giữa — **mở file NGUỒN CHÍNH THỨC ra đo `tblGrid`/`tcW` thật**. Ở ca này tôi đã đo tỷ lệ khối rồi kết luận "đúng chuẩn" (sai), sửa ngắt dòng (đúng nhưng chưa đủ), rồi mới đo hình học HD05 và thấy chênh 45,5% vs 51,5%.

31. **GẠCH CHÂN "Nơi nhận" KHÔNG TRÙM DẤU HAI CHẤM (§6.31)** — HD05 PL2 mục 9 ghi *"Đứng, có gạch chân"*, và cột **Minh hoạ** của chính bảng đó render thành **hai run tách nhau**: `Nơi nhận` (gạch chân) + `:` (KHÔNG gạch chân). Gạch chân cả `Nơi nhận:` là sai. (Hệ nhà nước không có gạch chân — NĐ30 để *nghiêng, đậm*.)

> **★ CÁCH ĐỌC PHỤ LỤC 2 HD05 — cột "Minh hoạ" là BẰNG CHỨNG ĐỊNH DẠNG.** Mỗi ô cột Minh hoạ được render ĐÚNG kiểu chữ mà dòng đó quy định (soi `<w:b/>`, `<w:u >` ở cấp RUN). Đây là cách xác minh mạnh hơn đọc mô tả chữ: `T/M BAN THƯỜNG VỤ`[đậm] · `PHÓ BÍ THƯ`[KHÔNG đậm] · `Nguyễn Văn A`[đậm] · `Nơi nhận`[gạch chân] + `:`[không]. ⚠ **KHÔNG** dùng các bảng minh hoạ khổ nhỏ ở đầu HD05 (bảng 2-7 trong docx) làm chuẩn — chúng là HÌNH thu nhỏ, toàn bộ để 10pt và không đậm gì cả.

27. **KIÊNG DÒNG CHỈ CÓ MỘT TỪ — CÂN DÒNG TÊN CƠ QUAN (§6.27)** ★**KHÔNG CẮT ĐÔI CỤM CỐ ĐỊNH**: chia cân thuần theo độ dài cho ra `ĐẢNG ỦY ỦY BAN VĂN` | `HÓA VÀ XÃ HỘI` — tách đôi *"VĂN HÓA"*, nhìn chật và sai (user 20-07 đối chiếu ảnh HD05 gốc). Quy tắc: (1) cấm điểm cắt phá cụm cố định (`NHÀ NƯỚC`, `VĂN HÓA`, `XÃ HỘI`, `TRUNG ƯƠNG`, `LAO ĐỘNG`, `THƯỜNG VỤ`…); (2) **ưu tiên cắt NGAY SAU từ chỉ loại hình tổ chức** (`BAN`, `ỦY`, `VỤ`, `CỤC`, `SỞ`, `PHÒNG`, `VIỆN`, `KHỐI`, `BỘ`…) tức cắt TRƯỚC phần tên lĩnh vực; (3) rồi mới cân độ dài. Cho ra `ĐẢNG ỦY ỦY BAN` | `VĂN HÓA VÀ XÃ HỘI`. — để Word tự ngắt thì tên cơ quan dài hay rớt lại **một từ trơ trọi** ở dòng cuối (user 20-07: *"rất hạn chế để một dòng chỉ có đúng một từ — kiêng"*). Chủ động chia trước bằng **nhiều ĐOẠN cân nhau tại ranh giới TỪ** (`_tt_can_dong`), mỗi dòng ≥2 từ khi đủ từ. **KHÔNG dùng `<w:br/>`** — r143 cho thấy br cứng làm dính chữ khi bóc text đối chiếu nguyên văn. ⚠ Hệ quả với §6.9: tên cơ quan cân thành 2 đoạn thì ô trái nhiều đoạn hơn ô phải ⇒ chuỗi `w:line` KHÔNG còn trùng khít; đúng theo §6.14 (lệch dòng không bắt buộc ngang nhau) — chỉ cần hai ô dùng **cùng bộ giá trị** chiều cao dòng.

28. **KHÔNG ĐỂ TRANG CHỈ CÓ KHỐI KÝ (§6.28)** — khối ký rơi riêng sang trang mới, phía trên không còn nội dung, là lỗi trình bày nặng. Đặt `<w:keepNext/>` cho **đoạn thân CUỐI** và **đoạn đệm** trước khối ký, `<w:keepNext/>` cho mọi đoạn trong bảng ký, `<w:cantSplit/>` cho hàng của bảng ký ⇒ Word kéo theo ít nhất một đoạn nội dung sang cùng trang với chữ ký.

29. **TỔ CHỨC ĐẢNG ĐÃ KẾT THÚC HOẠT ĐỘNG (§6.29)** — KL 121-KL/TW mục II.2.1 (corpus `1pa5nGnV…`): *"Kết thúc hoạt động của Đảng uỷ Khối các cơ quan Trung ương, Đảng uỷ Khối Doanh nghiệp Trung ương"*; *"Kết thúc hoạt động của các đảng đoàn, ban cán sự đảng ở Trung ương; ở cấp tỉnh"*; thành lập **4 đảng bộ trực thuộc BCH TW**: các cơ quan Đảng Trung ương · **Quốc hội** · Chính phủ · Mặt trận Tổ quốc và các đoàn thể Trung ương (Đảng bộ Quốc hội: QĐ 244-QĐ/TW ngày 24/01/2025). ⇒ tổ chức đảng của **các cơ quan Quốc hội** nay thuộc **Đảng uỷ Quốc hội**, KHÔNG còn thuộc Đảng bộ Khối các cơ quan Trung ương. Cờ `TT-TO-CHUC-HET-HIEU-LUC`.

30. **NHẤT QUÁN KIỂU ĐẶT DẤU (§6.30)** — tiếng Việt chấp nhận cả hai kiểu (`ủy`/`uỷ`, `hóa`/`hoá`, `tòa`/`toà`), nhưng **trong cùng một văn bản phải dùng MỘT kiểu**. Sai điển hình: *"ĐẢNG UỶ ỦY BAN VĂN HOÁ VÀ XÃ HỘI"* — cùng chữ "ủy" mà hai từ cạnh nhau đánh dấu khác nhau (user 20-07). Cờ `TT-CHINH-TA-DAU`. ⚠ Bản HD05 gốc dùng kiểu `uỷ`/`hoá`; văn bản của Uỷ ban dùng kiểu `ủy`/`hóa` — chọn theo cơ quan ban hành rồi giữ nhất quán.

26. **GOOGLE DOCS BỎ `tblCellMar` KHI CHUYỂN ĐỔI — ĐỆM Ô PHẢI KHAI HAI TẦNG (§6.26)** — kho mẫu (`_meta/templates`) lưu **canonical dạng Google Doc**, nên .docx upload lên bị convert. Round-trip: `tblCellMar` (và cả `tcMar`) **bị bỏ hẳn**, trong khi `w:before`/`w:after` của đoạn **sống sót**. Hệ quả: chỉ dựa vào `tblCellMar` thì bản LOCAL đúng còn bản TRÊN DRIVE lại dính nét kẻ. **Khai cả hai**: `tblCellMar` top/bottom (Word dùng, đệm đều trên-dưới) **+** `w:after` cho **đoạn CUỐI của mỗi ô có viền** (Google Docs dùng). Cùng lý do: mọi thứ quan trọng về trình bày mà chỉ nằm ở cấp BẢNG/Ô đều phải kiểm lại sau round-trip; xem thêm §6.22 (viền qua `tblStyle`) và bẫy regex bản Google-export ở §6.24.

25. **Ô CÓ VIỀN PHẢI CÓ ĐỆM DỌC — `tblCellMar` mặc định KHÔNG có top/bottom (§6.25)** — Word chỉ đặt sẵn lề trái/phải cho ô bảng; nếu không khai `<w:top>`/`<w:bottom>` trong `<w:tblCellMar>` thì **dòng cuối của ô dính sát nét kẻ dưới** (user 20-07 gửi ảnh ô "Nội dung"). Khai đệm dọc **6pt = 120 twips** trên và dưới cho MỌI bảng CÓ VIỀN (`spec.dem_o_pt` ở bộ dựng phiếu trình). Bảng **không viền** (khối tiêu đề Quốc hiệu/tên cơ quan) giữ 0 — thêm đệm ở đó sẽ xô lệch khối tiêu đề đã tinh chỉnh theo §6.9-6.11.

24. **PHIẾU TRÌNH — KHỐI ĐẦU VÀ THỤT ĐẦU DÒNG (§6.24)** — *"PHIẾU TRÌNH VĂN BẢN"* cỡ 14 **đậm** canh giữa · *"Kính gửi: …"* cỡ 14 canh giữa **KHÔNG đậm** (mẫu gốc có đậm nhưng Ủy ban yêu cầu bỏ, 20-07) · *"Nội dung: …"* cỡ 14 canh giữa, không đậm, **không thụt**. Trong BẢNG nội dung: **đề mục** (in đậm, vd *"Quá trình thực hiện:"*, *"Đề xuất:"*) và **mọi paragraph** đều thụt đầu dòng **0,8cm** (`spec.thut_bang_cm`, dải chấp nhận 0,8–1cm, ưu tiên 0,8). ⚠ 0,8cm **thấp hơn** dải 1–1,27cm của NĐ30/NQ351 — hợp lệ vì phiếu trình là biểu mẫu NỘI BỘ (§6.21), **đừng áp con số này sang văn bản phát hành**.

23. **BẢNG NỘI DUNG PHIẾU TRÌNH: MỖI CẤP KÝ MỘT DÒNG, Ô PHẢI vMERGE (§6.23)** — mẫu gốc là bảng **4 dòng**: dòng 1 = *"Quá trình thực hiện" + "Đề xuất"*, mỗi cấp ký (Chuyên viên · Phó Vụ trưởng · Ủy viên chuyên trách) **một dòng riêng**; cột phải *"Ý kiến của Chủ nhiệm Ủy ban"* dùng `<w:vMerge w:val="restart"/>` ở dòng 1 và `<w:vMerge/>` ở các dòng sau để thành MỘT ô dọc suốt. Gộp các cấp ký vào chung một ô thì **không có viền ngăn giữa họ** (user 20-07). Khe giữa khối tiêu đề/nội dung và bảng: `spec.dem_bang_pt`, mặc định **18pt** (không có quy định — cùng lý do §6.19).

22. **VIỀN BẢNG CÓ THỂ ĐẾN TỪ `tblStyle`, KHÔNG CHỈ `tblBorders` (§6.22)** — soi một bảng mà chỉ tìm `<w:tblBorders>` là **kết luận sai**: Word thường gắn `<w:tblStyle w:val="TableGrid"/>` trong `<w:tblPr>` và để viền trong `styles.xml`. Mẫu Phiếu trình VHXH đúng kiểu này: bảng nội dung KHÔNG có `tblBorders` trực tiếp nhưng CÓ viền đầy đủ qua style (đã kết luận nhầm "không viền" ngày 20-07, user bắt lại). **Quy trình soi viền:** (1) `tblBorders` trong `tblPr`; (2) nếu không có → đọc `tblStyle` rồi tra `styles.xml`; (3) `tcBorders` ở cấp ô ghi đè cả hai. ⚠ Khi bộ dựng tự sinh `styles.xml` tối thiểu (không có TableGrid) thì **phải đặt viền TRỰC TIẾP** ở cấp ô/bảng, không được trông vào style. ⚠ Đừng dò viền bằng chuỗi `w:val="single"` trơn — nó khớp cả `<w:u w:val="single"/>` (gạch chân tên cơ quan/Tiêu ngữ); dò `<w:top w:val="single"`.

    Phiếu trình: bảng tiêu đề **KHÔNG viền** · bảng nội dung 2 cột **CÓ viền** · bảng tổng hợp ý kiến **CÓ viền**.

21. **PHIẾU TRÌNH — BIỂU MẪU NỘI BỘ, KHÔNG PHẢI VĂN BẢN PHÁT HÀNH (§6.21)** — phiếu trình của Ủy ban (mẫu VHXH, nạp 20-07) không có số ký hiệu, Nơi nhận, dấu, quyền hạn ký kiểu TM./KT. ⇒ **không áp** `TT-SO-KY-HIEU`, `TT-NOI-NHAN`, `TT-CHUC-VU-KY`, `TT-TEN-LOAI`; chỉ áp phần khối tiêu đề và bề rộng bảng. Bố cục 3 khối: tiêu đề 2 ô · bảng 2 cột 70/30 *"quá trình thực hiện + đề xuất + các cấp ký | ý kiến lãnh đạo"* · bảng **TỔNG HỢP Ý KIẾN** 4 cột (STT · Họ và tên · Đồng ý · Góp ý) CÓ viền. ⚠ Mẫu gốc để cả **3 bảng TRÀN lề** (9180 / 10065 / 9180 twips > vùng chữ 9072) — luôn tính bề rộng từ `sectPr` (§6.10).

> **⚠ ĐÍNH CHÍNH DỄ SAI — "Nơi nhận" của VB ĐẢNG KHÔNG IN ĐẬM.** Phụ lục 2 HD05 ghi rõ: từ *"Nơi nhận"* = In thường · cỡ **14** · **"Đứng, có gạch chân"** — không có "đậm". Chỉ hệ NHÀ NƯỚC mới đậm (NĐ30 Mục V: cỡ 12, **nghiêng, đậm**). Danh sách nơi nhận: Đảng cỡ 12 · nhà nước cỡ 11.

> **Sinh ĐÚNG-BY-CONSTRUCTION:** `tl the-thuc-build --spec <json> --out <docx>` cài sẵn §6.6–6.13 cho ba hệ (hành chính NĐ30 · Đảng QĐ399+HD05 · **vbqppl-qh NQ351** — 19 mẫu Phụ lục I, thêm khoá spec `co_quan_ban_hanh`, `can_cu[]`, `tu_lenh`, `thong_qua`, `body[].kieu="giua"`) — bề rộng bảng tính từ lề, độ dài gạch theo công thức, ô phải luôn đủ chứa Quốc hiệu/tiêu đề MỘT dòng (tên cơ quan quá dài thì nhận phần còn lại và xuống dòng — chấp nhận được), tự self-check bằng `the-thuc-check`. ⚠ **Lề mặc định KHÁC NHAU theo hệ**: nhà nước 20/20/30/20mm (§6.8) · **Đảng 20/20/30/15mm ĐƠN TRỊ** (HD05 IV.4.1 — không phải dải, đặt 20mm là SAI); giãn dòng Đảng **18–22pt Exactly áp cho MỌI khối** kể cả tiêu đề/nơi nhận/ký.

## 7. MA TRẬN LOẠI VĂN BẢN → HỆ → MẪU KHUNG

### 7.1. Hành chính — bảng viết tắt (PL III NĐ30: 27 loại + 3 bản sao) & 14 mẫu
Viết tắt: NQ, QĐ, CT, QC, QyĐ, TC, TB, HD, CTr, KH, PA, ĐA, DA, BC, BB, TTr, HĐ, CĐ, BGN, BTT, GUQ, GM,
GGT, GNP, PG, PC, PB (+ SY, TrS, SL).
Mẫu: **1.1** Nghị quyết (cá biệt); **1.2** Quyết định (cá biệt) quy định trực tiếp; **1.3** QĐ quy định
gián tiếp; **1.4** Văn bản có tên loại (mẫu vạn năng: CT/QC/QyĐ/TB/KH/BC/TTr…); **Mẫu 1.5** Công văn;
**1.6** Công điện; **1.7** Giấy mời; **1.8** Giấy giới thiệu; **1.9** Biên bản; **1.10** Giấy nghỉ phép;
**2.1/2.2** Phụ lục VB giấy/điện tử; **3.1/3.2** Bản sao giấy/điện tử.

### 7.2. VBQPPL — mẫu của NĐ 187 (thay toàn bộ mẫu NĐ78)
- **Phụ lục II của NĐ 187** (19 mẫu — QH/UBTVQH/CTN): 01 Bộ luật; 02 Luật; 03 Luật sđbs một luật; 04 Luật
  sđbs nhiều luật; 05 NQ QH; 06 NQ QH (ban hành VB kèm theo); 07 VB kèm NQ QH; 08 NQ sđbs VB của QH;
  09 Pháp lệnh; 10 PL sđbs; 11 NQ UBTVQH; 12 NQ UBTVQH (kèm theo); 13 VB kèm NQ UBTVQH; 14 NQ sđbs VB
  UBTVQH; 15 NQ liên tịch; 16 Lệnh CTN (không điều); 17 Lệnh CTN (theo điều); 18 QĐ CTN; 19 Phụ lục kèm
  VBQPPL.
- **Phụ lục III của NĐ 187** (26 mẫu — CP/TTg/Bộ/TANDTC/VKSNDTC/KTNN/HĐND/UBND/CT UBND tỉnh): 01 NĐ CP
  (trực tiếp); 02 NĐ CP (ban hành kèm); 03 NQ CP; 04 NQLT CP-MTTQ; 05 QĐ TTg (trực tiếp); 06 QĐ TTg
  (kèm); 07 NQ HĐTP TANDTC; 08-09 TT Chánh án; 10-11 TT Viện trưởng; 12-13 TT Tổng KTNN; 14-15 TT Bộ
  trưởng; 16 TTLT; 17-18 NQ HĐND; 19-20 QĐ UBND; 21-22 QĐ CT UBND tỉnh; 23 VBQPPL sđbs MỘT VB; 24 sđbs
  NHIỀU VB; 25 bãi bỏ VB; **Mẫu số 26** Phụ lục kèm VBQPPL.
- **Phụ lục IV của NĐ 187** (12 mẫu hồ sơ chính sách/dự án/dự thảo): 01 Tờ trình chính sách; 02 Tờ trình
  dự án/dự thảo; 03 Báo cáo đánh giá tác động; 04-05 Thuyết minh quy phạm hóa; 06 Bản đánh giá TTHC/phân
  cấp/…; 07 Báo cáo rà soát; 08 Tổng kết thi hành; 09 Thực trạng QHXH; 10 Tổng hợp-tiếp thu-giải trình;
  11-12 Bản so sánh.

### 7.3. Đảng — khung theo HD05 PL 1-2 (sơ đồ ô 1-15 + bảng §5.3); thể loại theo Đ5 QĐ399.

### 7.4. Kho mẫu chung trên Drive (`_meta/templates/` root nền VBQPPL)
10 mẫu seed đợt đầu (grill Q4 duyệt 19-07): hành chính 1.2, 1.4, **1.5**, 1.9 (+1.1 khi cần); VBQPPL
PL III-01, III-05, III-14, III-17, III-19; PL II-02. File docx nguồn gộp lưu `_meta/templates/_nguon-goc/`.

## 8. CẢNH BÁO FILE MẪU BÓC (mổ XML 2026-07-19 — `D:\Quốc hội\bieu-mau-the-thuc\`)

| File | Font render thật | Lề T/B/L/R (mm) | Ghi chú |
|---|---|---|---|
| BIEU_MAU_ND30-2020 | Times New Roman (4115 run) | 28,3/27,5/22,6/22,6 | lề lệch CẢ 4 cạnh so dải chính nó mô tả; 3 section, 1 landscape |
| BIEU_MAU_ND187-2025 | **Arial** (docDefaults; 0 thẻ rFonts) | 10/10/30/20 | chỉ 8 run có w:sz — cỡ chữ không khai báo |
| BIEU_MAU_HD05-VPTW | **Arial** (608 run) | 10/10/30/20 | w:sz thân ~10pt — lệch chuẩn 14-15 |
| PHU_LUC_ND250-2026 | **Arial** (style Normal đè TNR) | 10/10/30/20 | nguyên khối, 0 page-break |

**Hệ quả bắt buộc:** (1) KHÔNG BAO GIỜ seed thẳng các file này làm khung điền — phải qua
`the-thuc-normalize` (lề **20/20/30/15 mm** — bộ giá trị nằm trong dải của CẢ 3 hệ, trùng lề cố định hệ
Đảng; docDefaults → Times New Roman; sz nhà nước 13 / Đảng 14) rồi `the-thuc-check` PASS T1 mới upload;
(2) tiêu chí kiểm lấy từ QUY ĐỊNH (file này), không "học" từ thuộc tính file mẫu; (3) 4 file trên là ca
FAIL tự nhiên để smoke bộ kiểm.

## 9. HỆ CŨ — KHÔNG DÙNG LÀM CHUẨN KIỂM

- ~~NQ 351/2017~~ **ĐÍNH CHÍNH 2026-07-19 (user xác nhận): NQ 351/2017 KHÔNG phải hệ cũ** — vẫn hiệu lực
  cho VBQPPL của QH/UBTVQH/CTN vì chưa có văn bản thay thế (NĐ CP không bãi bỏ được NQ UBTVQH; grep "351"
  trong 78/187 = 0 hit). Chuẩn kiểm nhánh này = §3.4. Registry `hieuluc=can_kiem_tra` → nên cập nhật
  "còn hiệu lực" (data-op riêng khi user duyệt). PL II NĐ187 (19 mẫu QH/CTN) tồn tại SONG SONG — dùng làm
  mẫu tham khảo trình bày, ngưỡng đo lấy theo NQ351 khi xung đột (thân 14 cố định).
- **NĐ 34/2016, 154/2020, 59/2024**: bãi bỏ minh thị tại Đ78 k2 NĐ 78/2025.
- **QĐ 66-QĐ/TW + 223-QĐ/TW** (thay bởi QĐ399); **HD 36-HD/VPTW** (thay bởi HD05).
- VB ban hành trước 01/7/2025: bộ kiểm chỉ WARN "ngày ban hành thuộc hệ quy định cũ", không áp ngưỡng.

## 10. NEO-DRIFT-LOCK (máy-đọc — R2 đối chiếu hằng `THE_THUC_CRITERIA`; KHÔNG sửa tay khi quy định nguồn chưa đổi)

```
hanh_chinh: le_tren_mm=20-25 le_duoi_mm=20-25 le_trai_mm=30-35 le_phai_mm=15-20 font=Times New Roman co_noi_dung=13-14 so_trang=13-14 quoc_hieu=12-13 tieu_ngu=13-14 so_ky_hieu=13 noi_nhan_tu=12 noi_nhan_ds=11 thut_dau_dong_cm=1-1.27 doan_pt_min=6 dong_max_lines=1.5
vbqppl: le_tren_mm=15-20 le_duoi_mm=15-20 le_trai_mm=30-35 le_phai_mm=15-20 font=Times New Roman co_noi_dung=13-14 so_trang=13 quoc_hieu=12-13 ten_luat=14 can_cu=14 chuc_vu_ky=13 noi_nhan_ds=11 thut_dau_dong_cm=1-1.27 doan_pt_min=6 dong_max_lines=1.5
vbqppl_qh: le_tren_mm=20-25 le_duoi_mm=20-25 le_trai_mm=30-35 le_phai_mm=15-20 font=Times New Roman co_noi_dung=14-14 so_trang=13 quoc_hieu=12-12 tieu_ngu=14-14 so_ky_hieu=13 can_cu=14 chuc_vu_ky=13 noi_nhan_tu=12 noi_nhan_ds=11 thut_dau_dong_cm=1-1.27 doan_pt_min=6 dong_min=don_hoac_15pt
vbhn: ke_thua=vbqppl so_trang=13-14 ky_hieu=STT/NAM/VBHN-loai-cq can_co=liet_ke_vb,chu_thich_chan_trang,khoi_xac_thuc
dang: le_tren_mm=20 le_duoi_mm=20 le_trai_mm=30 le_phai_mm=15 font=Times New Roman co_noi_dung=14-15 tieu_de=15 the_loai=15-16 so_ky_hieu=14 noi_nhan_tu=14 noi_nhan_ds=12 lien_he=10 ky_hieu_soan=11 so_trang=14 line_pt=18-22 thut_dau_dong_mm=10 doan_pt_min=6
normalize: le=20/20/30/15 font=Times New Roman sz_nha_nuoc=13 sz_dang=14
```

*(Cập nhật file này: sửa số → chạy selftest thấy r135/r-R2 đỏ → sửa hằng code + regen golden cùng release.)*
