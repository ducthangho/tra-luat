# WP-NSIS r1 — Cài, gỡ, cài lại bộ cài NSIS chính thức của Proxima trên Desktop (đặc tả đóng băng)

- Packet: con của #1319 (Issue sẽ được tạo khi cấp lease). Revision 1. Review Class: `sensitive`.
- Căn cứ:
  - Bảng ma trận `ops/acceptance/wp1319/MATRIX.md`, hàng "NSIS thật".
  - Quyết định của chủ kho ngày 18/11 (mục H.2): "NSIS cài thật trên Desktop (máy thử)", per-user, gỡ sạch sau khi đo.
- Ranh giới:
  - Chỉ làm trên Desktop `a5f7076e` dưới tài khoản Desktop Commander. Cài per-user, không dùng UAC/admin.
  - **Không mở app Proxima đã cài.** Việc kích hoạt và U8 thuộc packet riêng.
  - Không inference. Không đụng VM/gateway. Không LIVE.
  - Bộ cài chỉ lấy từ nguồn chính thức, và phải khớp băm.

## 1. Đầu vào
- Bộ cài: `https://github.com/Zen4-bit/Proxima/releases/download/v5.5.0/Proxima-Setup-5.5.0.exe`.
  - sha256 bắt buộc: `959c14c1ba489deb53bdaa34e83939fb18f9d7ade58a48a03d361ad1dd12ebf8`.
  - Kích thước: 161 754 969 byte.
  - Lệch băm hoặc kích thước thì DỪNG.
- Đối chiếu nội dung: `Proxima.exe` sau khi cài phải có sha256 `6990dce4b0b56e0d999fdc36521e9a57fe7a237348fc5c9d48e74873b742f886` (P4 runtime-after). Manifest đầy đủ của cây đã cài được ghi lại để reviewer so với manifest `official`/`baseline` trên ASUS.

## 2. Bước
- **S0 — Tiền kiểm, chỉ đọc. Gặp bất kỳ điều nào sau đây thì DỪNG để không đè lên cài đặt thật của người dùng:**
  - có khoá gỡ cài đặt `HKCU`/`HKLM` (cả nhánh WOW6432Node) mà `DisplayName` bắt đầu bằng `Proxima`;
  - có thư mục `%LOCALAPPDATA%\Programs\proxima*`;
  - có shortcut Proxima trong Start menu hoặc Desktop;
  - có tiến trình `Proxima*` đang chạy;
  - có `%APPDATA%\Proxima`.

  Ngoài ra kiểm tải máy và giữ khoá `C:\tl-win\KHOA.txt` + `F:\tl-win\KHOA.txt`.
- **S1:** tải về thư mục làm việc rồi kiểm băm và kích thước. Ghi lại `Get-AuthenticodeSignature` (Status, SignerCertificate Subject/Thumbprint, TimeStamper). Đây là phép **đo**, không phải tiêu chí PASS.
- **S2 — Cài:** chạy `Proxima-Setup-5.5.0.exe /S /currentuser` và chờ tiến trình kết thúc (giới hạn 10 phút).
  - Ghi rc, thư mục cài thực tế (lấy từ `InstallLocation` của khoá gỡ cài đặt HKCU), shortcut đã tạo, và các khoá registry mới.
  - Chụp snapshot trước và sau cho: khoá Uninstall HKCU, `%LOCALAPPDATA%\Programs`, Start menu, `%APPDATA%\Proxima`.
  - Băm `Proxima.exe`. Sinh manifest JSON đầy đủ của cây đã cài (rel → bytes, sha256).
  - Kiểm không có tiến trình Proxima nào được khởi chạy sau khi cài (theo dõi 30 s).
- **S3 — Gỡ:** chạy `"<InstallLocation>\Uninstall Proxima.exe" /S /currentuser`, chờ kết thúc.
  - Kiểm thư mục cài, khoá HKCU và shortcut đều đã biến mất.
  - Ghi lại phần còn sót, nếu có (ví dụ thư mục `%APPDATA%`, `%LOCALAPPDATA%\proxima-updater`).
- **S4 — Cài lại rồi gỡ lại**, lặp S2 và S3. Đây là phép đo tính lặp lại: rc, manifest của lần cài thứ hai phải trùng manifest lần đầu, và lần gỡ thứ hai phải sạch.
- **S5:** đóng băng zip + MANIFEST + quét secret (rc ghi vào tệp), nhả khoá, ghi `do-luong.csv`.

## 3. PASS
- S1: băm và kích thước khớp.
- S2: rc 0; có khoá HKCU với `InstallLocation`; `Proxima.exe` = `6990dce4…`; không tiến trình Proxima nào chạy.
- S3: rc 0; thư mục cài, khoá HKCU và shortcut đều không còn.
- S4: manifest lần 2 trùng lần 1; lần gỡ 2 sạch.
- Không có thay đổi nào ngoài các vị trí kể trên. Mọi khác biệt trong snapshot đều phải được liệt kê.

## 4. Vai, ngân sách, write set
- Operator: phiên điều phối (driver PowerShell, không phải mã sản phẩm, nên không có Executor).
- Reviewer: Codex `gpt-6-astra`, chạy trên máy Windows có bằng chứng, chỉ đọc. Tối đa 1 lượt.
- Native: 1 lượt, chạy lại tối đa 1 lần nếu lỗi dựng.
- Write set kho: `ops/specs/wp-nsis-r1.md`, `ops/leases/wp-nsis-r1-g1-operator.yaml`, `ops/acceptance/wp-nsis/RESULTS.md`, `ops/acceptance/wp-nsis/VERDICT.md`, `ops/acceptance/wp1319/MATRIX.md`.
