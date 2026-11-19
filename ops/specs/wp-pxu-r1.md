# WP-PXU r1 — Dọn tồn dư sau khi gỡ Proxima, có kiểm soát (đặc tả đóng băng)

- **Packet:** #1409 (con của #1319). Revision 1. Review Class `sensitive`.
- **Căn cứ:**
  - Finding NSIS-2 và kết quả N2/N3 trong `ops/acceptance/wp-nsis/RESULTS.md`: bộ gỡ chính thức Proxima 5.5.0 (`/S /currentuser`) **lần nào cũng để lại** đúng hai thứ:
    - thư mục cài `%LOCALAPPDATA%\Programs\Proxima` rỗng;
    - `%LOCALAPPDATA%\proxima-updater\installer.exe`, 161 754 969 byte, sha256 `959c14c1…`, tức bản sao bộ cài.
  - Logic dọn đã chạy trên OS thật ở N3 (S3c/S4c), driver `NSIS-N3.ps1` sha256 `9191fe1f…`.
  - Chủ kho duyệt ngày 19/11 (khoảng 01:08Z, "Dong y, lam di"): thêm bước dọn tồn dư có kiểm soát vào quy trình gỡ của skill.
- **Ranh giới:**
  - Không sửa `scripts/ProximaControl.psm1`, `scripts/ProximaConfig.psm1`, `scripts/ProximaControl.psd1`, `scripts/Run-Px.ps1`, `scripts/ProximaActivation.psm1`, `config.example.json` hay các test cũ.
  - Hàm mới **không chạy bộ gỡ**, không cài, không mở Proxima, không đụng registry (chỉ đọc). Nó chỉ dọn phần tồn dư **sau khi** bộ gỡ của nhà cung cấp đã xong.
  - Không LIVE, không inference, không đăng nhập.

## 1. Mã mới
Tệp `.agents/skills/proxima-control/scripts/ProximaInstall.psm1`:
- Chạy được trên Windows PowerShell 5.1 và PowerShell 7. `Set-StrictMode -Version 3.0`. Chỉ dùng .NET/BCL và cmdlet có sẵn; không import module khác của skill.
- Export **đúng một** hàm: `Remove-ProximaUninstallResidue`.
- Hàm trả một object có `ok` (bool), `code` (string), `actions` (mảng chuỗi mô tả từng việc **đã làm**), `before`, `after` (kiểm kê), và `error` khi có lỗi. Không ném lỗi ra ngoài: lỗi bất ngờ trả `ok=$false`, `code='NOT_MEASURED'`.

### 1.1 `Remove-ProximaUninstallResidue [-LocalAppData <dir>] [-InstallerSha256 <hex>] [-InstallerBytes <long>] [-ProcessProvider <scriptblock>] [-UninstallKeyProvider <scriptblock>] [-WhatIf]`
- **Mặc định:**
  - `LocalAppData` = `$env:LOCALAPPDATA`. Bắt buộc là đường dẫn tuyệt đối, tồn tại, và không phải reparse point; sai thì `BAD_ARGUMENT`.
  - `InstallerSha256` = `959c14c1ba489deb53bdaa34e83939fb18f9d7ade58a48a03d361ad1dd12ebf8`.
  - `InstallerBytes` = `161754969`.
  - Hai provider mặc định đọc OS thật: `Get-Process`, và các khoá `Uninstall` dưới HKCU, HKLM, HKLM\WOW6432Node.
- **Đích (cố định, suy từ `LocalAppData`, không nhận đường dẫn tuỳ ý):** `InstallDir = <LocalAppData>\Programs\Proxima` · `UpdaterDir = <LocalAppData>\proxima-updater`.
- **Tiền điều kiện.** Trái điều kiện nào thì trả mã tương ứng, **không xoá gì**:
  1. Không có tiến trình nào mà tên (bỏ `.exe`, so không phân biệt hoa thường) là `Proxima`, bắt đầu bằng `Un_`, hoặc bắt đầu bằng `Au_` → nếu có: `UNINSTALL_RUNNING`.
  2. Không có khoá gỡ cài đặt nào mà `DisplayName` bắt đầu bằng `Proxima` → nếu có: `STILL_INSTALLED`.
  3. Không tồn tại `InstallDir\Proxima.exe` → nếu có: `STILL_INSTALLED`.
- **Kiểm `InstallDir`:**
  - Không tồn tại thì không có gì để làm.
  - Là reparse point thì `RESIDUE_UNEXPECTED`.
  - Rỗng hoàn toàn (không tệp, không thư mục con, tính cả mục ẩn/hệ thống) thì xoá **bằng phép xoá không đệ quy**.
  - Còn bất cứ mục nào thì `RESIDUE_UNEXPECTED`, không xoá.
- **Kiểm `UpdaterDir`:**
  - Không tồn tại thì không có gì để làm.
  - Là reparse point thì `RESIDUE_UNEXPECTED`.
  - Phải chứa **đúng một** mục: tệp thường tên `installer.exe` (so không phân biệt hoa thường), không phải reparse point, kích thước = `InstallerBytes`, sha256 = `InstallerSha256` (so không phân biệt hoa thường). Đủ cả thì xoá tệp đó rồi xoá thư mục bằng phép xoá không đệ quy.
  - Lệch bất kỳ điều nào thì `RESIDUE_UNEXPECTED`, không xoá gì trong thư mục đó.
- **Tổ tiên:** `LocalAppData` và `LocalAppData\Programs` không được là reparse point. Vi phạm thì `RESIDUE_UNEXPECTED`.
- **Thứ tự:** kiểm sơ bộ **cả hai** đích trước. Chỉ khi cả hai hoặc vắng mặt hoặc đạt điều kiện thì mới bắt đầu bước xoá; một đích lệch là không xoá gì ở cả hai.
- **Chống đua (bắt buộc, theo P1 của review N3 trong `ops/acceptance/wp-nsis/VERDICT.md`).** Driver N3 xoá updater **đệ quy** dựa trên một ảnh chụp cũ. Hàm này không được làm vậy:
  - **`InstallDir`:** xoá bằng `[IO.Directory]::Delete(path, $false)`. Phép xoá không đệ quy này tự từ chối khi thư mục không rỗng. Nếu lúc xoá thư mục đã có mục mới thì trả `RESIDUE_CHANGED`. Nếu nó đã thành junction thì chỉ gỡ liên kết, không đụng đích; vẫn báo `RESIDUE_CHANGED`.
  - **`UpdaterDir`:** cô lập trước, kiểm sau.
    - Đổi tên **nguyên tử** `UpdaterDir` thành `proxima-updater.pxu-<GUID>` ở cùng thư mục cha.
    - Kiểm lại **trên bản đã cô lập**: không phải reparse point; đúng một mục; mục đó là `installer.exe` hợp lệ về kích thước và băm.
    - Đạt thì xoá tệp, rồi xoá thư mục cô lập bằng phép không đệ quy.
    - Lệch thì đổi tên trả về chỗ cũ và trả `RESIDUE_CHANGED`. Nếu tên cũ đã bị chiếm, để nguyên bản cô lập, trả `RESIDUE_CHANGED`, và ghi đường dẫn của nó vào `actions`.
  - Không lệnh xoá nào dùng `-Recurse` hay `Directory.Delete(path, $true)`.
- **`-WhatIf`:** chạy toàn bộ phần kiểm, trả `code='WOULD_REMOVE'` hoặc `NOTHING_TO_DO` kèm `actions` dự kiến, không xoá gì.
- **Kết quả:**
  - Đã xoá ít nhất một thứ và kiểm kê sau cho thấy cả hai đích đều vắng: `ok=$true`, `code='CLEANED'`.
  - Không có gì để xoá: `ok=$true`, `code='NOTHING_TO_DO'`.
  - Xoá xong mà kiểm kê sau vẫn còn đích: `ok=$false`, `code='CLEAN_INCOMPLETE'`.
  - Các mã khác: `ok=$false`.
- Không xoá bất cứ đường dẫn nào ngoài `InstallDir`, `UpdaterDir` và `UpdaterDir\installer.exe`. Không dùng `-Recurse` ở bất cứ lệnh xoá nào.

## 2. Test
Tệp `.agents/skills/proxima-control/tests/ProximaInstall.Tests.ps1`, cùng phong cách với `ProximaActivation.Tests.ps1`:
- Tham số `-AddonRoot`, `-ScratchRoot`, `-ReportPath`, `-Counterexamples`. Từ chối scratch/report nằm trong cây git.
- Report JSON ghi: `passed`, `total`, `failed_ids`, `setup_error_ids`, edition, culture, `harness_sha256`, `source_hashes`.
- Dựng `LocalAppData` giả trong scratch. Dùng tệp `installer.exe` giả nhỏ, truyền `-InstallerSha256` và `-InstallerBytes` tương ứng; **không cần bộ cài thật**. Provider giả cho tiến trình và khoá registry.
- Ca tối thiểu, đặt mã `PU01…`:
  1. Không có gì → `NOTHING_TO_DO`.
  2. Đủ hai tồn dư đúng chuẩn → `CLEANED`; cả hai đích biến mất; `actions` có 2–3 mục.
  3. Chỉ có thư mục rỗng → `CLEANED`.
  4. Chỉ có updater đúng chuẩn → `CLEANED`.
  5. `InstallDir` còn 1 tệp → `RESIDUE_UNEXPECTED`; updater **không bị đụng**.
  6. `InstallDir` có thư mục con rỗng → `RESIDUE_UNEXPECTED`.
  7. Updater có thêm tệp thứ hai → `RESIDUE_UNEXPECTED`; không mất tệp nào.
  8. `installer.exe` sai băm (cùng kích thước) → `RESIDUE_UNEXPECTED`.
  9. `installer.exe` sai kích thước → `RESIDUE_UNEXPECTED`.
  10. Updater có thư mục con → `RESIDUE_UNEXPECTED`.
  11. `InstallDir` là junction trỏ ra thư mục khác (có tệp) → `RESIDUE_UNEXPECTED`; đích của junction còn nguyên.
  12. Updater là junction → `RESIDUE_UNEXPECTED`.
  13. `installer.exe` là symlink/hardlink tới tệp khác → `RESIDUE_UNEXPECTED` đối với symlink. Với hardlink, ghi lại hành vi (xoá một liên kết không xoá nội dung gốc) và giải thích trong test.
  14. Có tiến trình `Un_A` (giả) → `UNINSTALL_RUNNING`; không xoá gì.
  15. Có khoá `DisplayName='Proxima 5.5.0'` (giả) → `STILL_INSTALLED`.
  16. Còn `Proxima.exe` → `STILL_INSTALLED`.
  17. `-WhatIf` với đủ tồn dư → `WOULD_REMOVE`; không xoá gì.
  18. `LocalAppData` tương đối, không tồn tại, hoặc là junction → `BAD_ARGUMENT`.
  19. Tên viết hoa khác (`INSTALLER.EXE`, `Proxima-Updater`) → xử lý như chuẩn (Windows không phân biệt hoa thường).
  20. Provider ném lỗi → `NOT_MEASURED`; không xoá gì.
  21. Updater bị thêm tệp **sau** lần kiểm sơ bộ nhưng trước khi cô lập (giả lập bằng hook test) → `RESIDUE_CHANGED`; tệp thêm vào còn nguyên; updater được trả về tên cũ.
  21b. `InstallDir` bị thêm tệp sau lần kiểm sơ bộ → `RESIDUE_CHANGED`; tệp còn nguyên.
  21c. `LocalAppData\Programs` là junction → `RESIDUE_UNEXPECTED`.
  22. Kiểm export: module export đúng `Remove-ProximaUninstallResidue`, không thêm tên nào.
- **Phản chứng** (`-Counterexamples`, mã `CU01…`): mỗi phản chứng nạp một bản module đã đột biến **trong scratch** và chứng minh ca đích ĐỎ đúng lý do. Tối thiểu:
  - bỏ kiểm "rỗng" (xoá đệ quy) → PU05/PU06 đỏ;
  - bỏ kiểm băm → PU08 đỏ;
  - bỏ kiểm số mục trong updater → PU07 đỏ;
  - bỏ kiểm reparse point → PU11 đỏ;
  - bỏ tiền điều kiện tiến trình → PU14 đỏ;
  - xoá từng đích ngay khi kiểm xong (không kiểm cả hai trước) → PU05 đỏ;
  - xoá updater đệ quy theo kết quả kiểm sơ bộ, không cô lập (đúng lỗi của driver N3) → PU21 đỏ.
- Hook test: hàm nhận một tham số ẩn `-TestHook <scriptblock>` (không ghi trong SKILL.md). Hook được gọi đúng một lần, giữa bước kiểm sơ bộ và bước xoá/cô lập. Mặc định là `$null`.

## 3. SKILL.md
Thêm mục `## Gỡ cài đặt (Uninstall residue)`, ngắn gọn:
- Quy trình gỡ:
  1. Chạy bộ gỡ của nhà cung cấp `"<dir>\Uninstall Proxima.exe" /currentuser /S`.
  2. Chờ cả tiến trình `Un_*`/`Au_*` tự nhân bản kết thúc (bộ gỡ chạy bất đồng bộ).
  3. Chạy `Remove-ProximaUninstallResidue`, xem trước bằng `-WhatIf`.
- Các mã kết quả. Nêu rõ: `RESIDUE_UNEXPECTED` nghĩa là có thứ ngoài dự kiến, **phải người xem**, không tự xoá tay.
- Giới hạn: chỉ cho bản cài per-user 5.5.0 với băm bộ cài đã biết. Bản khác phải truyền băm tương ứng.

## 4. PASS
- Test trên Desktop, cả Windows PowerShell 5.1 lẫn PowerShell 7, culture `tr-TR` như WP-PXA:
  - mặc định `passed == total`, `failed_ids` và `setup_error_ids` rỗng;
  - với `-Counterexamples`, mỗi CU làm đỏ đúng ca đích vì đúng lý do.
- Chạy lại 4 harness cũ (Activation, Manifest, Config, Control) trên cùng máy: số đếm không đổi so với WP-PXA N2 (Activation 30/30 và 36/36, Manifest 12/12, Config 46/46, Control 38/38).
- Không chạy bộ cài hay bộ gỡ thật trong packet này. Hành vi trên OS thật của logic dọn đã có bằng chứng ở N3.

## 5. Vai, ngân sách, write set
- Executor: Claude Fable 5.2 (subagent). Viết vào staging trong scratch; phiên điều phối chép vào kho và đối chiếu băm. Tối đa 2 lời gọi.
- Reviewer: Codex `gpt-6-astra`, độc lập, chỉ đọc. Review mã trước khi đo, review kết quả sau khi đo. Tối đa 2 lượt.
- Native: Desktop 1 lượt, chạy lại 1 lần khi lỗi dựng.
- Write set (liệt kê từng tệp, không glob):
  - `.agents/skills/proxima-control/scripts/ProximaInstall.psm1`
  - `.agents/skills/proxima-control/tests/ProximaInstall.Tests.ps1`
  - `.agents/skills/proxima-control/SKILL.md`
  - `ops/specs/wp-pxu-r1.md`
  - `ops/leases/wp-pxu-r1-g1-executor.yaml`
  - `ops/acceptance/wp-pxu/RESULTS.md`
  - `ops/acceptance/wp-pxu/VERDICT-code.md`
  - `ops/acceptance/wp-pxu/VERDICT-run.md`
  - `ops/acceptance/wp1319/MATRIX.md`
