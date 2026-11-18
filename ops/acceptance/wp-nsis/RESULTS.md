# WP-NSIS r1 — Kết quả cài/gỡ bộ cài NSIS chính thức trên Desktop (#1405)

Trạng thái: **đã đo, CHƯA review độc lập.** Gói bằng chứng nằm trên Desktop: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp-nsis\freeze\wp-nsis-evidence.zip`, sha256 `be4c21e9f63649e775cc5e9e1750d776365bdc9f3ba2eeefb4ba07822da94eea`, 11 tệp, quét secret rc 0, MANIFEST `4cec5a36…`.

## Kết quả
| Bước | Kết quả | Dấu hiệu |
|---|---|---|
| S0 | sạch | Không có khoá, thư mục, appdata, shortcut hay tiến trình Proxima nào trước khi cài |
| S1 tải bộ cài | **đạt** | sha256 `959c14c1…`, 161 754 969 byte. **Authenticode: `NotSigned`**, không có người ký, không có timestamp |
| S2 cài `/S /currentuser` | **đạt** (đo trên bản cài của N1) | Cài vào `%LOCALAPPDATA%\Programs\Proxima`, khoá HKCU `e3679a9c-…`, shortcut Start menu. `Proxima.exe` = `6990dce4…`, 3226 tệp, manifest `2537b108…`, không có tiến trình nào tự chạy |
| S3 gỡ `/currentuser /S` | **không kết luận được** | rc 0 sau 64 s. Khoá HKCU và shortcut đã bị xoá, nhưng thư mục cài và `proxima-updater` vẫn còn. Bộ gỡ NSIS **tự chép mình ra bản tạm (`Un_A.exe`) rồi chạy ngầm** sau khi tiến trình gốc thoát, nên phép đo trong 60 s là chưa đủ |
| S4a cài lại | **đạt** | Thời gian 37 s, `exe` = `6990dce4…`, manifest **trùng S2** (`2537b108…`) |
| S4b gỡ lần 2 | **không chạy** | Driver báo `NO_UNINSTALLER` ngay sau S4a. Rất có thể bộ gỡ S3 đang chạy ngầm đã xoá tệp chen giữa lúc S4a cài, nên các bước bị đan xen |
| Dọn dẹp (operator) | sạch | Bộ gỡ chính thức gỡ khoá HKCU, shortcut và 3226 tệp. Nó **để lại** thư mục cài rỗng và `%LOCALAPPDATA%\proxima-updater\installer.exe` (161 MB, là bản sao bộ cài, `959c14c1…`). Hai thứ này đã được phiên điều phối xoá (`NSIS-cleanup.log`). Desktop sau cùng: không còn dir, updater, khoá hay shortcut |

## Finding
- **NSIS-1:** bộ cài chính thức Proxima 5.5.0 **không được ký số**. Hàng "chữ ký" không thể đạt bằng Authenticode; chỉ còn dựa vào kiểm băm theo nguồn GitHub release.
- **NSIS-2:** gỡ cài đặt **không sạch hoàn toàn**: còn thư mục rỗng và bản sao bộ cài 161 MB trong `proxima-updater`. Bộ gỡ chạy bất đồng bộ (`Un_A.exe`), nên mọi quy trình tự động cài, gỡ hay rollback phải chờ tiến trình con kết thúc, không được chỉ chờ rc của tiến trình gốc.
- **Lỗi driver của phiên điều phối:** dựa vào `InstallLocation` (electron-builder không ghi cho per-user); dùng vòng chờ với `-like '[...]'` (sai cú pháp). Đã dùng lần chạy lại duy nhất.

## Còn thiếu
- S3/S4b cần đo lại, với vòng chờ theo `Un_*.exe` / `Au_*.exe`.
- Review độc lập (1 lượt, Codex) chưa chạy.
