# WP-PXR r1 — Gỡ Proxima 5.5.0 trên Desktop, dọn tồn dư, xoá profile thử U8 (#1416)

**Căn cứ:**
- Chủ kho hỏi ngày 19/11: "Có cần gỡ bản cài Proxima hay không".
- Chủ kho chọn **"Gỡ bản cài + xoá profile thử"**.
- Đặc tả `ops/specs/wp-pxr-r1.md`; lease `ops/leases/wp-pxr-r1-g1-operator.yaml`.

**Máy:** DESKTOP-T9R33P2, chạy dưới tài khoản Desktop Commander (`thanghd`, Medium integrity), PS 7.6.10. Tải CPU lúc chạy là 11 %.

**Driver:**
- `PXR.ps1`, sha256 `0834dda72b4a5804e80782dfd5f76c67dc5e3c4651661949d50a31fad57c6db1`.
- Tiến trình con `R4.ps1`, sha256 `3a0d30ce617f1d589562ee0daabad02486326c25f9a7bc41d4e6c2974348ef05`.
- Kiểm cú pháp bằng parser PS 7 cho ra 0 lỗi.

## Chạy khô trước (không gỡ, không xoá)
| Lượt | Driver | Kết quả |
|---|---|---|
| dryrun-1 08:57:02Z | `26425641…` (bản đầu) | **`PRECHECK_FAILED`**. Đây là lỗi dựng trong driver, không phải lệch trạng thái máy. Hàm trả một phần tử thì PowerShell mở mảng, nên `$keys.Count` đếm số khoá của dict (4) thay vì 1. Không có gì trên máy bị chạm; khoá đã nhả. |
| (sửa) | `patch1.py` | Bọc `@()` ở 7 chỗ gọi `Get-ProximaKeys`/`Get-WatchProcs`. Băm sau sửa khớp giữa container và Desktop (`0834dda7…`). |
| dryrun-2 08:58:31Z | `0834dda7…` | **`DRYRUN_OK`**: không tiền kiểm nào lệch. `R4.ps1` nạp `ProximaInstall` **theo tên**, đúng đường dẫn và băm `81c1164b…`. Hàm trả **`STILL_INSTALLED`** khi bản cài còn, đúng chốt chặn. |

## Lượt thật (08:58:53Z–08:59:09Z, 1/1)
| Bước | Kết quả |
|---|---|
| R0 tiền kiểm | 0 lệch: đúng 1 khoá HKCU `e3679a9c-…` (`Proxima 5.5.0`, đúng `QuietUninstallString`); bộ gỡ 182 706 byte, sha `2f2acd0e…`; không có tiến trình theo dõi; không có `%APPDATA%\Proxima`; module đúng băm; shortcut U8 đúng đích và đối số; profile 12 085 tệp, 287 185 128 byte, 0 reparse point. Hai khoá host lấy bằng handle độc quyền |
| R2 gỡ | `Uninstall Proxima.exe /currentuser /S`, **mã thoát 0** sau 0,73 s. Helper **`Un_A.exe`** thấy ở 0,8–5,0 s, không thấy `Au_*`. Hết tiến trình ở 9,2 s |
| R3 sau gỡ | Khoá gỡ cài đặt **mất**; `Proxima.exe` **mất**. Tồn dư đúng như WP-NSIS và WP-PXU đã đo: thư mục cài **rỗng** (0 tệp, 0 thư mục con) và `proxima-updater\installer.exe` (161 754 969 byte). Bộ gỡ đã tự xoá **cả hai** `Proxima.lnk` (Desktop và Start menu) |
| R4 `-WhatIf` | **`WOULD_REMOVE`**, gồm 3 hành động, cả 3 nằm trong hai đích (thư mục cài, `proxima-updater`) |
| R4 chạy thật | **`CLEANED`, `ok=true`**. Thư mục cài rỗng đã xoá; `installer.exe` được kiểm và xoá qua handle trong thư mục cách ly `proxima-updater.pxu-4b876e0a…`, rồi thư mục đó bị xoá. `after`: cả hai đích `absent`, `quarantined` rỗng |
| R5 shortcut U8 | Kiểm lại đích và đối số, rồi xoá; đã mất |
| R6 profile thử | Đường dẫn đúng, nằm dưới `u8\`, 0 reparse point, không tiến trình nào dùng. Đã xoá **12 085 tệp / 287 185 128 byte**; đã mất |
| R7 cuối | Không còn khoá `Proxima*`, thư mục cài, `proxima-updater`, shortcut Proxima, `%APPDATA%\Proxima`, tiến trình Proxima hay profile. Hai khoá host nhả đúng nội dung |

Lúc 09:03:08Z, script khảo sát chỉ đọc chạy lại độc lập và cho cùng kết quả.

**Giữ nguyên:** `u8\evidence-*`, `u8\freeze-*`, `u8\relay-*`. Các thư mục này chỉ chứa tên tương đối, kích thước, băm và boolean, là bằng chứng của WP-U8. Module `ProximaActivation`/`ProximaInstall` đã promote (WP-PXL) cũng được giữ.

## Bằng chứng (đóng băng, quét secret rc 0)
- Zip `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\pxr\freeze\wp-pxr-r1-evidence.zip`:
  - sha256 `3a1f04b1f8466014b84d051e6ad9e02a318f50da51d804d821263e73206664c8`, 19 336 byte, 16 tệp;
  - MANIFEST `36a9499e…`.
- Đã chuyển nguyên byte về container điều phối (bọc base64 76 cột, kiểm sha từng khúc 40 dòng). 16/16 tệp khớp MANIFEST.
- Zip **không** chứa tệp hay tên tệp nào của profile.

## Không đo / giới hạn
- **Không đo lại băm `Proxima.exe` (`6990dce4…`) ngay trước khi gỡ.** Điều 3 của tiêu chí H.7 đòi điều này. R0 kiểm khoá, `QuietUninstallString` và băm bộ gỡ, nhưng chỉ kiểm `Proxima.exe` **có mặt**. Băm `6990dce4…` mới được đo lúc cài, ở U8 A1, cùng bản cài này. Nay đã gỡ nên không đo lại được.
- Không đo:
  - tồn dư ngoài các đường dẫn đã chụp: `%TEMP%` của `Un_A.exe`, các khoá registry khác ngoài khoá gỡ cài đặt, cache Electron ngoài `%APPDATA%\Proxima`;
  - đồng bộ OneDrive của thư mục Desktop.
- Phiên đăng nhập phía provider: xoá profile chỉ bỏ cookie trên máy. Máy chủ provider có thể còn coi phiên hợp lệ tới khi hết hạn. Chưa đo.
- Chỉ một lượt, một máy, một phiên bản (5.5.0).
