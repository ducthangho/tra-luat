# BÀN GIAO — nguồn Công báo cần tải tay (hồ sơ Luật BHXH), 29-07-2026

Phiên này tải được **PDF** Công báo (host `congbaocdn.chinhphu.vn` bắt tay TLS bình thường) nhưng
**KHÔNG tải được `.doc`**: bản .doc chỉ phát qua API `g7.cdnchinhphu.vn`, và proxy egress của môi trường
này không bắt tay TLS được với host đó (`CERTIFICATE_VERIFY_FAILED` ở cả curl lẫn urllib, kể cả khi
trỏ đúng `--cacert /root/.ccr/ca-bundle.crt` và `--proxy-cacert`). **Không hạ TLS verification** — nên
dừng ở đây và bàn giao link.

`vbpl.vn` cũng không dùng được từ đây (http=000, từ chối ở tầng mạng) — đúng như ghi nhận 27-07.
`thuvienphapluat.vn` trả 403 với mọi fetch server-side (chỉ trình duyệt đã đăng nhập mới tải được).

---

## 1. Luật BHXH — Luật số 41/2024/QH15

Trang Công báo: <https://congbao.chinhphu.vn/van-ban/luat-so-41-2024-qh15-42576.htm>
**Công báo số 987 + 988, ngày 25-8-2024** (khớp số ghi trong sổ).

| Định dạng | Link |
|---|---|
| **DOC** ★ nên lấy | `https://g7.cdnchinhphu.vn/api/download/stream?Url=tm-8mq6BhNw0NbrKRhTDAQWsKg3tuqaY0aWypnY78U6M2BY68Ekp0Gvvr483flbRh8sHLTzOm0qH5bjU20pglJQtNqNXoBHzndKU_vCvAa0y4BLEsTneOyqwWQjRA4zj-S04CCdyEjl2PEN7jT8fMg~~&file_name=2024_987+%2b+988_41-2024-QH15.doc` |
| PDF (đã tải được) | <https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2024/6/42576/51466-1-2024987-98841-2024-qh15.pdf> |
| TVPL (cần đăng nhập VIP) | <https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=41-2024-QH15> |

## 2. Nghị định 159/2025/NĐ-CP (BHXH tự nguyện)

Trang Công báo: <https://congbao.chinhphu.vn/tai-ve-van-ban-so-159-2025-nd-cp-45253-57094>
Số Công báo: <https://congbao.chinhphu.vn/cong-bao-so-853-854-nam-2025-45252> —
**số 853 + 854, ngày 01-7-2025** (khớp sổ).

| Định dạng | Link |
|---|---|
| **DOC** ★ nên lấy | `https://g7.cdnchinhphu.vn/api/download/stream?Url=tm-8mq6BhNw0NbrKRhTDAQWsKg3tuqaY0aWypnY78U6M2BY68Ekp0Gvvr483flbR1a2eRPTxzssBRdELDC06dzIAuBe6FSbczvH2W1tM3eaiH8y24pfe22m2aqPzE16FTiwl3WaG8Lb9LWh6cvyQTA~~&file_name=2025_853+%2b+854_159-2025-N%c4%90-CP.doc` |
| PDF (đã tải được) | <https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/6/45253/57094-1-2025853-854159-2025-nd-cp.pdf> |
| TVPL (cần đăng nhập VIP) | <https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=159-2025-ND-CP> |

> Cách lấy .doc trên máy bạn: mở trang Công báo → nút tải → chọn **.doc** (link g7 ở trên dán thẳng
> vào trình duyệt cũng được). Đưa file vào thư mục bất kỳ rồi bảo tôi đường dẫn.

---

## 3. VÌ SAO phải là .doc, không dùng PDF — đã đo, không suy đoán

Tôi đã thử nạp bản PDF Công báo của Luật 41/2024 qua đường chuẩn (`profile-ingest`, có `--text-file`).
Lệnh chạy `ok:true`, nhưng **bản Google Doc do Drive chuyển từ PDF hỏng cấu trúc**:

| Phép đo (sau khi lọc header Công báo + khối chữ ký số ở CẢ HAI bên) | Kết quả |
|---|---|
| Tiêu đề Điều nhận được | **116 / 141** — mất 25 |
| Điều khớp nguyên văn | 98 / 112 |
| Điều lệch nội dung | 14 (nặng nhất Điều 71 ratio 0.21, Điều 114 ratio 0.22) |

Kiểu hỏng: Drive **dính tiêu đề vào cuối dòng trước** —
`c) Trường hợp khác do Chính phủ quy định. Điều 4. Loại hình, các chế độ bảo hiểm xã hội`
⇒ 25 Điều mất vị trí đầu dòng ⇒ `tl extract --dieu N` trả sai khoảng. Hỏng đúng chức năng lõi.

**Đã xử lý:** bản GDoc hỏng `1ys0cG-Syyjj…` đã `source-delete --apply` (journal
`source-delete_1785312999_6274`), registry trả `count=0` cho `41-2024-QH15`.
**Còn giữ:** file PDF Công báo official `1jBFgBVz4EBtOszmgK1RP00Tyg38TcMcU`
(`Luat_41-2024-QH15_2024_Bao_hiem_xa_hoi.pdf`) nằm ở root profile, CHƯA đăng ký registry —
giữ làm nguồn gốc đối chiếu. Xoá hay đăng ký là quyết định của bạn.

---

## 4. Kết quả đối chiếu ĐÃ LÀM XONG (không cần chờ .doc)

### 4a. Luật 41/2024 — bản quarantine ở kho NỀN so với Công báo: **nội dung TRÙNG KHỚP**

So 141/141 Điều giữa bản Công báo (poppler) và bản quarantine `1Ds95NoIdZ…` sau khi strip markup:
**125 Điều khớp nguyên văn tuyệt đối; 16 Điều lệch nhưng TOÀN BỘ chỉ là dấu câu** —
dấu chấm sau "Mục N" (13 chỗ), một dấu gạch, một chữ hoa/thường, và ký hiệu kết thúc `./.`.
**Không một Điều nào khác nội dung.**

⇒ Hai kết luận: (1) bộ strip-markup của skill chạy ĐÚNG; (2) nạp bản Công báo **không làm đổi câu chữ**,
giá trị nằm ở chỗ gỡ được mối nguy markup và có bản đứng tên BAN HÀNH.

### 4b. NĐ 159/2025 — bản trong kho CÓ LỖI THẬT, đúng như sổ lỗi ghi

So bản Công báo 853+854 với bản đang ở corpus (`1yqsb_Sis4Y…`). **Lỗi chính tả thật của bản kho:**

| Điều | Công báo (ĐÚNG) | Bản trong kho (SAI) |
|---|---|---|
| 5 | có trách nhiệm **chuyển** kinh phí | **chuyến** kinh phí |
| 8 | (n x 12 – m +1) **đến** (n x 12) | (n x 12 - m +1) **đên** (n x 12) |
| 14 | trợ cấp **hằng** tháng (2 chỗ) | trợ cấp **hàng** tháng |
| 5, 18 | trực thuộc **Trung ương** (3 chỗ) | trực thuộc **trung ương** |

**Nhưng KHÔNG phải bản kho tệ mọi mặt** — có hai thứ bản kho GIỮ mà PDF Công báo không có/không bóc được:
- **Công thức Điều 11 và Điều 14**: `pdftotext` xé nát bảng công thức (`Mbq x 2 x N / TChtxh` thành chuỗi
  chữ trộn lẫn); bản GDoc trong kho render đúng.
- **Khối "Nơi nhận"** ở Điều 18: bản kho có đủ, bản Công báo không đăng.

⇒ **Đây chính là lý do cần bản .doc**: nó có đồng thời câu chữ ĐÚNG của Công báo *và* cấu trúc
bảng/công thức tử tế. Thay bằng bản PDF sẽ sửa được 8 lỗi chính tả nhưng làm HỎNG 2 công thức —
đánh đổi không đáng.

---

## 4c. Món #3 — hai PDF "mạo số hiệu": ĐÃ SỬA, và hoá ra còn là BẢN TRÙNG

Mở ra đọc thì tên hai file **sai hẳn so với nội dung**, không chỉ mạo số hiệu:

| drive_id | Tên CŨ (sai) | Thực chất là gì | Tên MỚI |
|---|---|---|---|
| `1GM6QY15…` | `DUTHAO_Luat_41_2024_QH15_Du_an_Luat_sua_doi_bo_sung_mot_so_dieu_cua_Luat_Bao_hiem_xa_hoi.pdf` | **Tờ trình Bộ Nội vụ** `/TTr-BNV`, dự thảo ngày 16/7/2026 | `DUTHAO_TTr-BNV_2026_To_trinh_du_an_Luat_sua_doi_Luat_BHXH_16-7-2026.pdf` |
| `1UeiF7sK…` | `DUTHAO_Luat_41_2024_QH15_cua_Luat_sua_doi_bo_sung_mot.pdf` | **Công văn 7728/BNV-CTL&BHXH ngày 20/7/2026** báo cáo tiến độ | `CV_7728-BNV-CTL-BHXH_2026_Bao_cao_tien_do_du_an_Luat_BHXH.pdf` |

**Và cả hai đều là bản TRÙNG của tài liệu ĐÃ đăng ký** — nên KHÔNG đăng ký mới (đúng dặn dò "không nạp trùng"):

| File mồ côi | Trùng với dòng đã có | Độ giống |
|---|---|---|
| `1GM6QY15…` | `DUTHAO_To_trinh_BNV_Luat_sua_doi_bo_sung_Luat_BHXH_16-7-2026` (`1y1W3xHay…`) | **0.944** |
| `1UeiF7sK…` | `DUTHAO_CV_7728-BNV_gui_UBVHXH_bao_cao_tien_do_Luat_BHXH` (`1tLz300Kz…`) | **0.885**, và ĐÚNG BẰNG 1248 ký tự cả hai bên |

⇒ Đã `rename` qua webapp (rc ok cho cả hai). Rủi ro trích nhầm dự thảo làm luật hiện hành: **đã gỡ**.
Còn lại là quyết định chính sách raw-twin (mục B7 báo cáo chính): đăng ký `loai=thuong` hay để mồ côi.

## 5. Việc tôi sẽ làm ngay khi có file .doc

1. `reg-query --refresh --sohieu <số hiệu>` — dò trùng trước (đã làm: Luật 41 hiện `count=0`).
2. Bóc text, đối chiếu **từng Điều** với bản Công báo PDF đã tải + bản đang ở kho; báo cáo bảng lệch.
3. Kiểm riêng: đủ 141 Điều (Luật 41) / 18 Điều (NĐ 159), `monotonic=True`, công thức Điều 11 & 14 còn nguyên,
   khối "Nơi nhận" còn nguyên.
4. `profile-ingest --staged` (lane docx) → DRY xem `plan_hash` + `chunk_plan` → mới `--apply --confirm yes`
   kèm `--expected-plan-hash`.
5. Đối chiếu lại GDoc SAU khi convert (đúng bước đã bắt được lỗi lần này) rồi mới bàn chuyện `corpus=true`.
