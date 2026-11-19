# WP-U8 r1 — Giữ phiên đăng nhập Proxima qua backup/restore profile (đặc tả đóng băng)

- **Packet:** #1410 (con của #1319). Revision 1. Review Class `sensitive`.
- **Căn cứ:**
  - Hàng U8 và mục H.2 trong `ops/acceptance/wp1319/MATRIX.md`.
  - `ops/acceptance/wp1319/DESIGN.md` §D4.
  - Quyết định của chủ kho ngày 18/11: "chủ kho tự đăng nhập/2FA trên profile thử; phiên điều phối không chạm credential, chỉ đo việc giữ phiên qua backup/restore". Chủ kho nói "Đồng ý, làm đi" ngày 19/11: chuẩn bị tới điểm đăng nhập.
- **Ranh giới (cứng):**
  - Chỉ làm trên Desktop `a5f7076e` (DESKTOP-T9R33P2), dưới tài khoản Desktop Commander, cài per-user. Không đụng VM/gateway hay ASUS. Không LIVE.
  - **Không inference.** Không gửi bất kỳ yêu cầu chat/completion nào tới Proxima hay provider. Chỉ được gọi REST `GET /v1/stats` (không sinh request tới provider). Ngoài ra không gọi endpoint REST nào khác.
  - **Không chạm credential.**
    - Phiên điều phối không nhập, không đọc, không in, không phân tích nội dung cookie/token/session.
    - Tệp profile chỉ được **chép nguyên byte** và **băm**. Riêng `settings.json` được đọc **duy nhất** các trường boolean `providers.<tên>.enabled` và `providers.<tên>.loggedIn`.
    - Không có tệp profile nào, kể cả bản sao, rời khỏi Desktop. Gói bằng chứng chỉ chứa tên tương đối, kích thước, sha256 và các boolean nói trên.
  - Không tự đăng nhập, không 2FA, không chép profile từ máy khác. Chủ kho tự đăng nhập trong app.
  - Không dùng `%APPDATA%\Proxima` mặc định: mọi lần mở app đều mang `--user-data-dir=<PROFILE>`.

## 1. Đường dẫn
- Thư mục làm việc: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\u8\`.
- `PROFILE` = `<làm việc>\profile-u8`. `BACKUP` = `<làm việc>\backup-u8`. `DAMAGED` = `<làm việc>\profile-u8.damaged-<UTC>`.
- Shortcut `Proxima U8 (profile thử).lnk` trên Desktop của user, trỏ `<InstallDir>\Proxima.exe --user-data-dir="<PROFILE>"`.

## 2. Pha A — chuẩn bị, rồi DỪNG
- **A0 tiền kiểm, chỉ đọc.** Gặp bất kỳ điều nào sau đây thì DỪNG:
  - có khoá gỡ cài đặt (HKCU, HKLM, WOW6432Node) mà `DisplayName` bắt đầu bằng `Proxima`;
  - có `%LOCALAPPDATA%\Programs\proxima*`;
  - có shortcut Proxima trong Start menu hoặc Desktop;
  - có tiến trình tên `Proxima*`, `Un_*` hoặc `Au_*`;
  - có `%APPDATA%\Proxima`;
  - có `PROFILE` hoặc `BACKUP`.

  Ngoài ra ghi tải máy và lấy khoá `C:\tl-win\KHOA.txt` + `F:\tl-win\KHOA.txt` theo ADR-0057/58/59.
- **A1 cài:**
  - Bộ cài `Proxima-Setup-5.5.0.exe` lấy từ thư mục làm việc của WP-NSIS; bắt buộc sha256 `959c14c1…`, 161 754 969 byte. Chạy `/S /currentuser` và chờ cả helper.
  - Kiểm `Proxima.exe` = `6990dce4…`.
  - Ghi lại khoá HKCU, thư mục cài, và trạng thái `proxima-updater`.
  - Theo dõi tiến trình trong lúc cài: không được có tiến trình app nào.
- **A2 dựng profile thử:** tạo `PROFILE` rỗng và tạo shortcut. **Không mở app.**
- **A3:** nhả khoá, ghi `A-progress.log`/`A-result.json`, đóng băng zip + MANIFEST + quét secret.
- **DỪNG.** Báo chủ kho rằng có thể mở shortcut, tự đăng nhập các provider muốn thử, rồi **đóng app** và báo lại. Phiên điều phối không làm gì thêm cho tới khi chủ kho báo "đã đăng nhập xong và đã đóng app".

## 3. Pha B — đo giữ phiên (chỉ sau khi chủ kho báo)
- **B0:**
  - Lấy khoá.
  - Kiểm không còn tiến trình nào có `--user-data-dir` trỏ tới `PROFILE`. Còn thì DỪNG và nhờ chủ kho đóng app; không tự kill.
  - Ghi tải máy.
- **B1 snapshot "trước":**
  - Manifest của `PROFILE`: rel → bytes, sha256. Dùng `-Force` để thấy tệp ẩn. Không theo reparse point; gặp reparse point thì ghi lại.
  - Đọc các boolean `loggedIn`/`enabled` từ `settings.json`.
- **B2 backup:** `robocopy PROFILE BACKUP /MIR /COPY:DAT /R:1 /W:1 /XJ`. Ghi rc robocopy (< 8 là đạt). Manifest của `BACKUP` phải trùng manifest B1.
- **B3 làm hỏng có kiểm soát:** đổi tên `PROFILE` thành `DAMAGED` (không xoá), rồi kiểm `PROFILE` không còn.
- **B4 restore:** `robocopy BACKUP PROFILE /MIR /COPY:DAT /R:1 /W:1 /XJ`. Manifest của `PROFILE` phải trùng B1.
- **B5:** nhả khoá. Nhờ chủ kho mở shortcut, quan sát từng provider còn đăng nhập hay không **mà không gửi câu hỏi nào**, rồi đóng app.

  Trong lúc app mở, phiên điều phối được:
  - đọc `rest-port.json` trong `PROFILE` rồi gọi `GET /v1/stats` tối đa 3 lần, để ghi `totalRequests` (kỳ vọng 0, chứng minh không có inference);
  - đọc lại các boolean trong `settings.json`.
- **B6:** chủ kho báo kết quả quan sát theo từng provider. Phiên điều phối ghi lại **nguyên văn** câu báo đó.
- **B7 dọn:**
  - Xoá `DAMAGED` và `BACKUP` (chứa phiên đăng nhập), chỉ sau khi đã ghi xong bằng chứng. Xoá **không đệ quy theo đường dẫn tuỳ ý**: chỉ xoá đúng hai thư mục này, và chỉ sau khi kiểm chúng nằm dưới thư mục làm việc và không phải reparse point.
  - `PROFILE` và bản cài Proxima: **giữ nguyên**, chờ chủ kho quyết định có gỡ hay không.
- **B8:** đóng băng zip + MANIFEST + quét secret. Zip **không** chứa tệp nào của profile.

## 4. PASS / ghi nhận
- **Vế dữ liệu (PASS):**
  - robocopy rc < 8 ở cả B2 và B4;
  - manifest B2 == B1 và B4 == B1 (tập tên, kích thước, sha256);
  - app mở lại được trên profile đã restore (có `rest-port.json` mới, `GET /v1/stats` trả 200);
  - `totalRequests` = 0.
- **Vế đăng nhập (`quan_sat`, không có PASS/FAIL):** ghi lời chủ kho theo từng provider, kèm các boolean `loggedIn` trước và sau. Phiên mất sau restore là **kết quả hợp lệ, phải ghi lại**, không phải lỗi phải giấu.
- **Không được suy:** boolean `loggedIn` là cờ ứng dụng tự ghi, không chứng minh cookie còn hiệu lực. Không được dùng nó thay cho quan sát của chủ kho.

## 5. Vai, ngân sách, write set
- Operator: phiên điều phối. Driver PowerShell là công cụ đo, không phải mã sản phẩm, nên không có Executor.
- Reviewer: Codex `gpt-6-astra`, độc lập, chỉ đọc, 1 lượt sau pha B. Chạy trên máy Windows nếu có; không thì trong container điều phối với bộ con bằng chứng đã chuyển và kiểm băm.
- Native:
  - pha A: 1 lượt, chạy lại 1 lần khi lỗi dựng;
  - pha B: 1 lượt, chạy lại 1 lần khi lỗi dựng.
- Write set (không glob):
  - `ops/specs/wp-u8-r1.md`
  - `ops/leases/wp-u8-r1-g1-operator.yaml`
  - `ops/acceptance/wp-u8/RESULTS.md`
  - `ops/acceptance/wp-u8/VERDICT.md`

  `MATRIX.md` **không** nằm trong write set, vì lease WP-PXU (#1409) đang giữ nó. MATRIX sẽ được cập nhật dưới lease WP-PXU hoặc lease sau.
