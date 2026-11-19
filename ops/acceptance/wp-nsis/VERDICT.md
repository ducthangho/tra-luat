# WP-NSIS r1 — Review độc lập lượt N2 (1/1)

- **Reviewer:** Codex CLI 0.155.1 chạy trên ASUS, gọi với `-m gpt-6-astra`, sandbox chỉ ghi được vào `out`. Model tự khai "GPT-6 (Codex); exact serving variant unavailable", nên ghi **`KHONG_do_duoc`**.
- **Thời gian:** 00:12:46Z–00:14:48Z ngày 19/11, rc 0.
- **Đối tượng:** bộ con chuyển từ Desktop (relay `283dcd14…`, MANIFEST `003f54f3…` của zip `6084f4a7…`) gồm progress log, result.json, kết quả quét secret và driver `NSIS-N2.ps1`.

## Verdict: `request_changes`

| Bước | Phân loại | Ghi chú |
|---|---|---|
| Toàn vẹn bộ con | measured_pass | Bộ con và MANIFEST khớp |
| S0 trong phạm vi driver | measured_pass | Chỉ phủ các đường dẫn, registry và tên tiến trình mà driver chọn |
| S0 "không có gì Proxima" | not_measured | Không có kiểm kê toàn diện, không xét user khác |
| S1 | measured_pass | 161 754 969 byte, đúng sha256, `NotSigned` |
| S2 cài + exe | measured_pass | rc 0, đúng sha256 exe, có bộ gỡ, có shortcut |
| S2 "khoá HKCU có location" | not_measured | Driver không ghi hive registry và `InstallLocation` thô; location suy từ `QuietUninstallString` |
| S2/S4a "không khởi chạy" | not_measured | Chỉ lấy mẫu sau khi cài, không theo dõi việc tạo tiến trình suốt quá trình cài |
| S3 gỡ | **measured_fail** | Gỡ xong (khoá, shortcut, exe đều hết), nhưng còn thư mục rỗng và `installer.exe` 161 754 969 byte |
| S4a cài lại | measured_pass | 3226 tệp; manifest trùng S2 (`2537b108…`), so trên máy chủ |
| S4b gỡ lần 2 | **measured_fail** | Tồn dư y hệt S3 |
| Dọn tay sau đo | not_measured | Không có snapshot kiểm kê sau khi dọn |

**P1**
- **Tiêu chí đóng băng không đạt:** S3/S4 để lại thư mục và `proxima-updater\installer.exe`. Việc dọn tay không đổi FAIL thành PASS. Danh tính `installer.exe` là bản sao bộ cài mới chỉ do operator báo (khi dọn có kiểm băm `959c14c1`), N2 không đo băm của nó.
- **Phép đo còn hở:** `Keys` gộp HKCU và HKLM, không ghi đường dẫn registry; `Loc` dựa vào `QuietUninstallString`; kiểm tiến trình chỉ là lấy mẫu; khi helper của bước cài quá hạn thì driver không báo lỗi.

**P2**
- Hoàn tất bất đồng bộ được tách đúng khỏi tồn dư: ở S4b, lúc `t+5s` vẫn còn `Un_A.exe`, đến 8 s thì sạch. Đây là cận lấy mẫu, không theo dõi cây tiến trình con.
- `NotSigned` là phép đo, không phải tiêu chí FAIL của đặc tả.
- Không chứng minh: cài per-machine, nâng cấp từ bản cũ, rollback, lần chạy đầu tiên, và kiểm kê thay đổi toàn hệ thống.

## Xử lý
- Kết quả FAIL S3/S4 là **hành vi của sản phẩm**: bộ gỡ chính thức để tồn dư. Ghi lại như vậy, không sửa được ở phía operator, trừ khi bổ sung bước dọn có kiểm soát vào quy trình gỡ.
- Phép đo hở ở P1 cần lượt đo mới. Ngân sách native của g2 đã dùng hết, nên cần chủ kho quyết định.
