# WP-PXR r1 — Gỡ Proxima 5.5.0 trên Desktop, dọn tồn dư bằng hàm đã promote, xoá profile thử U8 (đặc tả đóng băng)

- **Packet:** #1416 (con của #1319). Revision 1. Review Class `sensitive`.
- **Căn cứ:**
  - Ngày 19/11 chủ kho hỏi "Có cần gỡ bản cài Proxima hay không", rồi chọn **"Gỡ bản cài + xoá profile thử"**.
  - H.7 trong `ops/acceptance/wp1319/MATRIX.md` chốt quy trình gỡ: bộ gỡ chính thức, chờ `Un_*`/`Au_*`, rồi `Remove-ProximaUninstallResidue`. Hàng này còn thiếu một lần gỡ thật trên máy thật.
  - WP-PXU (#1409) viết hàm. WP-PXL (#1413) đã promote hàm lên Desktop.
  - WP-U8 (#1410) B7 giữ `PROFILE` và bản cài để chờ quyết định này.
- **Ranh giới (cứng):**
  - Chỉ làm trên Desktop `a5f7076e` (DESKTOP-T9R33P2), dưới tài khoản Desktop Commander.
  - Không đụng VM, gateway hay ASUS. Không LIVE ngoài Desktop.
  - **Không inference, không mở Proxima.** Không cài lại Proxima.
  - Không đổi service, tác vụ lập lịch, tài khoản, ACL hay endpoint.
  - **Không chạm credential.** Không đọc nội dung tệp nào trong `PROFILE`; chỉ đếm số tệp, tổng byte và reparse point. Gói bằng chứng không chứa tệp hay tên tệp nào của profile.
  - Không xoá gì ngoài các đích nêu ở §2. Hai `Proxima.lnk` của nhà cung cấp do bộ gỡ tự dọn; nếu còn lại thì **ghi nhận và hỏi chủ kho**, không tự xoá.

## 1. Trạng thái nền đã khảo sát (19/11, 08:49Z, chỉ đọc)
| Mục | Giá trị |
|---|---|
| Khoá gỡ cài đặt | `HKCU\…\Uninstall\e3679a9c-20a6-5662-a494-9328780a14a8`, `DisplayName` = `Proxima 5.5.0`, `QuietUninstallString` = `"C:\Users\ThangHD\AppData\Local\Programs\Proxima\Uninstall Proxima.exe" /currentuser /S`. Không có khoá nào khác tên `Proxima*` ở HKCU, HKLM hay WOW6432Node. |
| Bộ gỡ | `Uninstall Proxima.exe`, 182 706 byte, sha256 `2f2acd0e546b67eabd017b4e1b3ddad5744f9f7af34ea451ebdc560e1f869f8b` |
| Thư mục cài | `%LOCALAPPDATA%\Programs\Proxima`, 3 235 tệp |
| Updater | `%LOCALAPPDATA%\proxima-updater\installer.exe`, 161 754 969 byte (chỉ có đúng tệp này) |
| `%APPDATA%\Proxima` | không có |
| Tiến trình `Proxima*` / `Un_*` / `Au_*` | không có |
| Shortcut | `Desktop\Proxima.lnk` và `Start Menu\Programs\Proxima.lnk` của nhà cung cấp; `Desktop\Proxima U8 (profile thu).lnk` do U8 A2 tạo |
| `PROFILE` | `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\u8\profile-u8`, 12 085 tệp, 287 185 128 byte, 0 reparse point |
| Module | `C:\Users\ThangHD\OneDrive\Documents\PowerShell\Modules\ProximaInstall\ProximaInstall.psm1`, 39 070 byte, sha256 `81c1164bf913b181ae5e8e88a04b4498abd592d1ff2e3a25f6cf24d7ed57a82a` (khớp WP-PXL §1) |
| Khoá host `C:\` và `F:\` | rỗng |

## 2. Bước (driver `PXR.ps1` ở `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\pxr\`)
Có chế độ `-DryRun`: chạy R0 và các phép kiểm, không gọi bộ gỡ, không xoá gì. Phải chạy DryRun và kiểm parse **trước** lượt thật.

- **R0 tiền kiểm.** Lệch bất kỳ điều nào thì DỪNG, không làm gì:
  - Lấy khoá `C:\tl-win\KHOA.txt` và `F:\tl-win\KHOA.txt`: mở handle độc quyền, kiểm rỗng, ghi dòng khoá trên chính handle đó. Có nội dung thì `HOST_BUSY`.
  - Ghi tải máy.
  - Mọi giá trị ở §1 phải khớp, trừ `Desktop\Proxima.lnk` và `Start Menu\…\Proxima.lnk` (chỉ ghi nhận).
  - Không có tiến trình nào mang `--user-data-dir` trỏ tới `PROFILE`.
- **R1 ảnh chụp "trước".**
  - Khoá registry (các giá trị ở §1).
  - Số tệp trong thư mục cài; danh sách updater (tên, byte, sha256).
  - Danh sách shortcut. Riêng shortcut U8 ghi thêm `TargetPath`/`Arguments` qua `WScript.Shell`.
  - Số tệp và tổng byte của `PROFILE`.
- **R2 gỡ.**
  - Chạy đúng `QuietUninstallString` của khoá, bằng `Start-Process -Wait`; ghi mã thoát.
  - Sau đó thăm dò mỗi 2 giây, tối đa 600 giây, tới khi không còn tiến trình `Un_*`/`Au_*`/`Proxima*`. Ghi dòng thời gian (tên tiến trình, PID, lúc thấy, lúc mất).
  - Hết 600 giây mà còn: dừng ở `UNINSTALL_TIMEOUT`, không kill, không dọn.
- **R3 ảnh chụp "sau gỡ".** Ghi lại cùng các mục như R1.
- **R4 dọn tồn dư.**
  - `Import-Module ProximaInstall` (theo tên, từ `PSModulePath`), trong tiến trình `pwsh` mới. Ghi `Path` và băm của module đã nạp; phải là tệp ở §1.
  - Chạy `Remove-ProximaUninstallResidue -WhatIf` và ghi toàn bộ kết quả (JSON).
  - Chỉ khi kết quả là `WOULD_REMOVE`, và `actions` chỉ trỏ tới thư mục cài và `proxima-updater`, thì chạy thật `Remove-ProximaUninstallResidue` và ghi kết quả.
  - Mọi mã khác thì **không** chạy thật, ghi lại nguyên văn, chờ người xem. Riêng `NOTHING_TO_DO` là hợp lệ, và khi đó cũng không chạy thật.
- **R5 xoá shortcut U8.**
  - Chỉ xoá `Desktop\Proxima U8 (profile thu).lnk`. Điều kiện:
    - là tệp thường, không phải reparse point;
    - `TargetPath` là `…\Programs\Proxima\Proxima.exe`;
    - `Arguments` chứa đường dẫn `PROFILE`.
  - Kiểm xong thì xoá, rồi kiểm lại là đã mất.
- **R6 xoá `PROFILE`.**
  - Chỉ chạy khi R2 đã kết thúc sạch (không còn tiến trình). Không phụ thuộc mã R4, vì mục đích là bỏ phiên đăng nhập.
  - Điều kiện xoá:
    - `GetFullPath` đúng bằng đường dẫn ở §1 và nằm dưới `…\u8\`;
    - bản thân thư mục không phải reparse point; quét lại `-Force -Recurse` cũng phải ra 0 reparse point;
    - không tiến trình nào mang `--user-data-dir` trỏ tới nó.
  - Đạt thì `Remove-Item -LiteralPath -Recurse -Force`, rồi kiểm đã mất. Ghi số tệp và byte đã xoá.
  - Các thư mục `evidence-*`, `freeze-*` và tệp `relay-*` của U8 **giữ nguyên**: chúng chỉ chứa tên tương đối, kích thước và băm, đã nằm trong bằng chứng U8.
- **R7 kết.**
  - Ảnh chụp cuối: khoá registry, thư mục cài, updater, shortcut, `%APPDATA%\Proxima`, `PROFILE`, tiến trình.
  - Nhả khoá, chỉ khi nội dung còn đúng dòng mình ghi.
  - Ghi `PXR-progress.log` và `PXR-result.json`.
  - Đóng băng zip + MANIFEST + quét secret bằng `u8_freeze.py` của U8 (đã kiểm: từ chối evidence có tên giống dữ liệu phiên).

## 3. PASS
- R2:
  - bộ gỡ trả mã thoát 0;
  - helper kết thúc trong 600 giây;
  - R3 thấy khoá `e3679a9c-…` đã mất và `Proxima.exe` đã mất.
- R4:
  - `-WhatIf` trả `WOULD_REMOVE`, và lượt thật trả `CLEANED`, `ok=true`, với `after` cho thấy thư mục cài và `proxima-updater` đều đã mất;
  - **hoặc** `-WhatIf` trả `NOTHING_TO_DO`, khi R3 đã thấy bộ gỡ tự dọn hết. Trường hợp này ghi là "quy trình chạy được, hàm không có gì để dọn": nó **không** chứng minh khả năng dọn trên máy thật.
- R5 và R6: shortcut U8 và `PROFILE` đã mất.
- R7: `%APPDATA%\Proxima` vẫn không có; không còn tiến trình Proxima.
- Hai `Proxima.lnk` của nhà cung cấp: ghi kết quả (đã mất hay còn), không tính vào PASS.

## 4. Không hoàn tác được
- Gỡ cài đặt và xoá `PROFILE` là **không hoàn tác**. Phiên đăng nhập ở profile mất hẳn; phía provider có thể vẫn coi phiên còn hiệu lực cho tới khi hết hạn.
- Cài lại Proxima nằm ngoài packet này.

## 5. Vai, ngân sách, write set
- Operator: phiên điều phối. Driver là công cụ đo, không phải mã sản phẩm, nên không có Executor.
- Reviewer: Codex `gpt-6-astra`, độc lập, chỉ đọc, 1 lượt sau R7. Chạy trong container điều phối, trên gói bằng chứng đã chuyển và kiểm băm.
- Native: 1 lượt.
  - Được chạy lại 1 lần chỉ khi lỗi dựng xảy ra **trước** R2.
  - Từ R2 trở đi không chạy lại bộ gỡ. Một bước hỏng sau R2 được làm lại riêng bằng script con, theo đúng điều kiện ở §2, và ghi là sai lệch.
- Write set (không glob):
  - `ops/specs/wp-pxr-r1.md`
  - `ops/leases/wp-pxr-r1-g1-operator.yaml`
  - `ops/acceptance/wp-pxr/RESULTS.md`
  - `ops/acceptance/wp-pxr/VERDICT.md`
  - `ops/acceptance/wp1319/MATRIX.md`
