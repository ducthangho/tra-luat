# WP-NSIS r1 — Kết quả cài/gỡ bộ cài NSIS chính thức trên Desktop (#1405)

Trạng thái: N1/N1b/N2 đã review (`VERDICT.md`); N3 xem mục cuối. Gói bằng chứng nằm trên Desktop: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp-nsis\freeze\wp-nsis-evidence.zip`, sha256 `be4c21e9f63649e775cc5e9e1750d776365bdc9f3ba2eeefb4ba07822da94eea`, 11 tệp, quét secret rc 0, MANIFEST `4cec5a36…`.

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

## N2: đo lại bằng driver đã sửa (lease g2; chủ kho cấp thêm 1 lượt bằng câu "Làm tiếp đi", 18/11 khoảng 23:29Z)
Gói bằng chứng: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp-nsis\freeze-n2\wp-nsis-n2-evidence.zip`, sha256 `6084f4a764b78d75a4e2bd8d6f440144c4c84f1b29e04fe1868d1b3eaa28322a`, MANIFEST `003f54f3…`, quét secret rc 0.

Driver đã sửa ba điểm:
- lấy đường dẫn cài từ `QuietUninstallString`;
- chờ cả tiến trình `Un_*`/`Au_*` tự nhân bản của bộ gỡ, tối đa 300 s;
- ghi phần tồn dư tách riêng khỏi trạng thái "gỡ chưa xong".

| Bước | Kết quả | Dấu hiệu (`NSIS-N2-progress.log`) |
|---|---|---|
| S0 | sạch | `S0 clean` |
| S1 | đạt | sha256 `959c14c1…`, chữ ký `NotSigned` |
| S2 cài | **đạt** | rc 0, 31 s; `exe` 6990dce4; 3226 tệp; có bộ gỡ; 0 tiến trình |
| S3 gỡ | **xong nhưng để tồn dư** | Tiến trình gốc thoát sau 1 s, gỡ xong sau 5 s. Khoá HKCU, shortcut và `Proxima.exe` đều hết. **Còn lại:** thư mục cài rỗng và `proxima-updater\installer.exe` (161 754 969 byte) |
| S4a cài lại | **đạt** | rc 0, 40 s; manifest **trùng S2** (`2537b108…`) |
| S4b gỡ lần 2 | **xong nhưng để tồn dư** | Xong sau 8 s; tồn dư y hệt S3 |

**Kết luận N2:** cài per-user hoạt động và lặp lại được. Bộ gỡ chính thức gỡ đủ khoá, shortcut và 3226 tệp, nhưng **lần nào cũng để lại** thư mục rỗng cùng một bản sao bộ cài 161 MB. Vì vậy tiêu chí PASS "gỡ sạch" của đặc tả **không đạt**. Đây là hành vi của sản phẩm (finding NSIS-2), không phải lỗi đo.

**Dọn sau đo:** phiên điều phối xoá thư mục rỗng và `proxima-updater` (đã kiểm `installer.exe` có băm = bộ cài). Desktop cuối cùng sạch.

**Lỗi phía điều phối:** trong lệnh dọn một dòng, biến `$L` (đường dẫn) ghi đè `$l` (dòng khoá), vì biến PowerShell không phân biệt hoa thường. Hậu quả là khoá không được nhả, ở cả lần dọn 22:38Z lẫn lần sau N2. Tôi đã nhả tay sau khi khớp nội dung khoá.

Review N2: `request_changes` (xem `VERDICT.md`).

## N3: đo bổ sung các khe đo + thử bước dọn tồn dư có kiểm soát (lease g3; chủ kho duyệt "Dong y, lam di", 19/11 khoảng 01:08Z)
Gói bằng chứng trên Desktop: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp-nsis\freeze-n3\wp-nsis-n3-evidence.zip`, sha256 `fede4bda12e8a5e0aacd9bfbd7909d50fdbdcbddfcc8da57161d254feb941ec5`, MANIFEST `502b4913…`, quét secret rc 0. Driver `NSIS-N3.ps1` sha256 `9191fe1f…`.

Driver mới vá các khe mà review N2 chỉ ra:
- ghi đường dẫn registry đầy đủ (hive), kiểm cả HKLM và WOW6432Node, tính `hkcu_only`;
- ghi `InstallLocation` thô (thực tế `<absent>`: electron-builder per-user không ghi);
- theo dõi tiến trình liên tục suốt lúc cài (115–118 lần lấy mẫu);
- băm phần tồn dư;
- chụp kiểm kê sau bước dọn.

Bước dọn có kiểm soát (S3c/S4c) chỉ làm hai việc:
- xoá thư mục cài **chỉ khi rỗng**;
- xoá `%LOCALAPPDATA%\proxima-updater` **chỉ khi** trong đó có đúng một tệp `installer.exe` với sha256 bằng bộ cài chính thức `959c14c1…`.

| Bước | Kết quả | Dấu hiệu (`NSIS-N3-progress.log`) |
|---|---|---|
| S0 | sạch | `S0 clean` |
| S1 | đạt | sha256 `959c14c1…`, `sig=NotSigned` |
| S2 cài | **đạt** | rc 0, 65 s; `hkcu_only=True`; khoá `HKEY_CURRENT_USER\…\Uninstall\e3679a9c-…`; `install_location_raw=[<absent>]`; exe `6990dce4…`; 3226 tệp; `polls=115 app_seen=0` |
| S3 gỡ | **xong, nhà cung cấp để tồn dư** | Tiến trình gốc thoát sau 2 s, gỡ xong sau 6 s. Còn `residue_dir=True(0)` (thư mục rỗng) và `installer.exe:161754969:959c14c1…`; `vendor_clean=False` |
| S3c dọn | **sạch** | `removed empty install dir; removed proxima-updater (only installer.exe = official installer hash)`; `clean_after=True` |
| S4a cài lại | **đạt** | rc 0, 65 s; `polls=118 app_seen=0`; manifest trùng S2 (`2537b108…`) |
| S4b gỡ lần 2 | **xong, nhà cung cấp để tồn dư** | Gỡ xong sau 5 s; tồn dư y hệt S3 |
| S4c dọn | **sạch** | `clean_after=True` |
| Kết | | `DONE passed=True vendor_uninstall_clean=False procedure_clean=True`; khoá đã nhả cả hai |

**Kết luận N3** (review N3 `request_changes`, xem `VERDICT.md`; bước dọn của driver bị chỉ ra là xoá updater đệ quy, không an toàn trước đua):
- Bộ gỡ chính thức **lần nào cũng để tồn dư**. Tồn dư luôn đúng hai thứ: thư mục cài rỗng, và bản sao bộ cài đã kiểm băm.
- Quy trình "gỡ của nhà cung cấp + bước dọn có kiểm soát" cho kết quả sạch ở cả hai vòng.
- Thêm một quan sát: ngay sau khi cài, `proxima-updater\installer.exe` đã xuất hiện (`S2.after.updater` trong result.json). Tức là bộ cài tự chép mình vào đó khi cài, không phải khi gỡ.

