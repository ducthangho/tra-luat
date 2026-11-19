# WP-U8 r1 — Giữ phiên đăng nhập qua backup/restore (#1410)

## Pha A: chuẩn bị (xong 19/11 01:54Z), DỪNG chờ chủ kho
Gói bằng chứng trên Desktop: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\u8\freeze-a\wp-u8-a-evidence.zip`
- sha256 `18e867f8ede207e9c663a4132409fd62ef44591b38667b1275966830a9f87776`, 11 039 byte, 7 tệp.
- MANIFEST `e1a1246d…`.
- Quét secret rc 0. Lần này `secret-scan.json` ghi cả `argv` lẫn đích quét, để đóng khe mà review N3 đã chỉ ra.
- Driver: `U8-A.ps1`, cộng `U8-A2.ps1` cho lần chạy lại bước A2.

| Bước | Kết quả | Dấu hiệu (`U8-A-progress.log`) |
|---|---|---|
| A0 tiền kiểm | sạch | `A0 clean cpu=26% free_mem_mb=2740`. Phạm vi rộng hơn N3: mọi hive, `Programs\proxima*`, `.lnk` có chữ Proxima ở Desktop và Start menu (user và public), tiến trình `Proxima*`/`Un_*`/`Au_*`, `%APPDATA%\Proxima`, `proxima-updater`, profile/backup |
| A1 cài 5.5.0 per-user | **đạt** | rc 0, 59 s; `hkcu_only=True`; `exe=6990dce4…`; `polls=105 app_seen=0` |
| A2 profile + shortcut (lần 1) | **lỗi dựng** | `Unable to save shortcut "…Proxima U8 (profile th?).lnk"`: COM `WScript.Shell` không lưu được tên có ký tự ngoài ANSI. Khoá đã nhả |
| A2 chạy lại (lần chạy lại duy nhất) | **đạt** | Kiểm lại trước khi làm: exe đúng, profile rỗng, 0 tiến trình, không có `%APPDATA%\Proxima`. Shortcut `…\OneDrive\Desktop\Proxima U8 (profile thu).lnk` trỏ `Proxima.exe` với `--user-data-dir="F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\u8\profile-u8"`. **Lệch đặc tả:** tên shortcut dùng ASCII `thu` thay vì `thử` |

**Quan sát thêm (bổ sung cho WP-NSIS):**
- Bộ cài tạo **hai** shortcut: Start menu `Proxima.lnk` **và Desktop** `OneDrive\Desktop\Proxima.lnk`. Driver N1–N3 chỉ kiểm Start menu.
- A0 sạch, tức là lần gỡ ở N3 đã không để lại shortcut Desktop. Nếu shortcut ấy từng được tạo ở N3 thì bộ gỡ đã xoá nó.
- `proxima-updater\installer.exe` (bộ cài, `959c14c1…`) xuất hiện ngay sau khi cài.

**Lưu ý cho chủ kho:** shortcut mặc định `Proxima.lnk` mở app với profile **mặc định** (`%APPDATA%\Proxima`). Phép đo U8 chỉ dùng shortcut `Proxima U8 (profile thu)`.

**Trạng thái (lịch sử, đã được thay thế bởi pha B bên dưới):** đang chờ chủ kho làm các việc sau:
1. Mở shortcut `Proxima U8 (profile thu)`.
2. Tự đăng nhập các provider muốn thử.
3. **Đóng app.**
4. Báo lại.

Phiên điều phối không làm gì thêm trên profile cho tới lúc đó.

## Pha B: operator làm thay theo lệnh chủ kho (19/11, 04:34–05:05Z)
**Lệnh của chủ kho, khoảng 04:31Z:** "Làm giúp tôi U8 trên Desktop đi".

Phiên điều phối mở và đóng app thay chủ kho, nhưng **không đăng nhập** bất kỳ provider nào: đó là credential và 2FA của chủ kho, nằm ngoài quyền được cấp. Vì vậy:
- **vế dữ liệu được đo đầy đủ;**
- **vế đăng nhập: `not_measured`**, vì chưa ai đăng nhập (`loggedIn=false` cho cả 4 provider, trước và sau).

**Lệch so với đặc tả (ghi rõ):**
- (a) Đặc tả để chủ kho mở app; ở đây operator mở bằng `U8-L.ps1`, với `--user-data-dir` trỏ profile thử, và đóng êm bằng `WM_CLOSE` như r4.
- (b) **REST API của Proxima tắt theo mặc định**: không có `rest-port.json`, nên không gọi được `GET /v1/stats` để chứng minh `totalRequests=0`. Không bật REST, vì đó là đổi cấu hình app.
  - Bằng chứng thay thế cho "không inference": chưa provider nào đăng nhập, REST tắt, và operator không nhập gì vào app.
  - Bằng chứng thay thế cho "app sẵn sàng": tìm được 6 cửa sổ app, đóng êm, mã thoát 0, profile có dữ liệu.
- (c) Driver B lỗi dựng ở lần 1 (`Measure-Object -Property` không đọc được khoá hashtable), dừng trước mọi thay đổi. Đã dùng lần chạy lại duy nhất. Trước đó **đã thử bản sửa bằng `-DryRun`** (chỉ đọc).

Gói bằng chứng trên Desktop: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\u8\freeze-b\wp-u8-b-evidence.zip`
- sha256 `eb1688b72b81b6b71542d18a90fe701f2d636bca44fcf5dd0c06297e98d6fda0`, 14 tệp, MANIFEST `69763498…`.
- Quét secret rc 0. **Không chứa tệp nào của profile**; chỉ có manifest tên, kích thước, sha256, cộng các boolean `enabled`/`loggedIn`.

| Bước | Kết quả | Dấu hiệu (`U8-B-progress.log`) |
|---|---|---|
| L1 mở lần đầu | profile được tạo (0 → 21 mục) | 120 s; `closed windows=6 graceful=True exit_code=0`; mặc định cả 4 provider `enabled=true, loggedIn=false` |
| B0 | sạch | Không tiến trình nào dùng profile; cpu 13% |
| B1 snapshot | 12 404 tệp, 180 730 298 byte, 0 reparse point | digest `9201616d…` |
| B2 backup (robocopy `/MIR /COPY:DAT /XJ`) | **đạt** | rc 1; manifest **trùng B1** |
| B3 làm hỏng có kiểm soát | đạt | Đổi tên thành `profile-u8.damaged-20261119T044353Z`; profile gốc không còn |
| B4 restore | **đạt** | rc 1; manifest **trùng B1** (`9201616d…`); boolean giữ nguyên |
| L2 mở lại trên profile đã restore | **đạt (mở được, đóng êm)** | 120 s; `windows=6 graceful=True exit_code=0`; boolean như cũ |
| B7 dọn | đạt | Đã xoá `backup-u8` và `.damaged-…` (mỗi cái 12 404 tệp); có kiểm nằm trong thư mục làm việc và không chứa reparse point. **Giữ** profile (21 mục) và bản cài Proxima |

**Kết luận:**
- **Vế dữ liệu: PASS hẹp** (scoped Desktop, sửa theo P1 của review). Phần đạt là sao chép, khôi phục và mở lại:
  - backup và restore trả đúng từng byte (trùng tên, kích thước, sha256 của 12 404 tệp);
  - app mở lại và đóng êm trên profile đã khôi phục.

  **Chưa đo, và không được miễn:**
  - `GET /v1/stats` 200 và `totalRequests=0` (REST tắt theo mặc định);
  - trạng thái "sẵn sàng" của REST.

  Hai lượt mở app (`U8-L-L1-populate-result.json`, `U8-L-L2-restored-result.json`) tự ghi `passed=false`, đúng với tiêu chí đầy đủ của driver.
- **Vế đăng nhập: `not_measured`.** Profile chưa từng đăng nhập. Muốn đo thì chủ kho tự đăng nhập trên shortcut `Proxima U8 (profile thu)`, rồi chạy lại B1–B4 + L2.
- Bản cài Proxima 5.5.0 và profile thử **vẫn còn trên Desktop**, chờ chủ kho quyết định gỡ hay giữ.

## Pha C: vế đăng nhập (lease g2; 19/11, 07:43–08:31Z)
1. **Chủ kho tự đăng nhập** trên shortcut `Proxima U8 (profile thu)`, đóng app, rồi báo "đã đăng nhập xong, đã đóng app". Phiên điều phối không chạm credential.
2. **Kiểm profile được dùng** (chỉ siêu dữ liệu): profile mặc định `%APPDATA%\Proxima` **không tồn tại**; tệp mới nhất trong profile U8 được ghi lúc 07:43:23Z; mỗi provider có thư mục phiên riêng trong `Partitions` (chatgpt, claude, gemini, perplexity).
3. **Cờ `loggedIn` trong `settings.json` vẫn `false` cho cả 4 provider** dù chủ kho đã đăng nhập. Cờ này **không phản ánh** trạng thái đăng nhập thật, đúng như đặc tả §4 đã cảnh báo, nên không dùng làm bằng chứng.
4. **Đo:**
   - DryRun B1 lúc 07:46Z.
   - Lượt đầu (07:47Z) **dừng ở `HOST_BUSY`**: một phiên khác (`session_015GtxrZk6…`, native #387 / PR #1414) đang giữ khoá F:. Không ghi đè, không chạy chồng; đặt nhắc kiểm lại.
   - Khoá trống lúc 08:20Z thì chạy thật.

| Bước | Kết quả | Dấu hiệu |
|---|---|---|
| B1 snapshot | 12 153 tệp, 303 308 699 byte, 0 reparse point | digest `f20155da…`, **trùng DryRun 07:46Z**, tức profile không đổi từ lúc đăng nhập |
| B2 backup | **đạt** | robocopy rc 1; manifest = B1 |
| B3 làm hỏng | đạt | đổi tên thành `profile-u8.damaged-20261119T082337Z` |
| B4 restore | **đạt** | robocopy rc 1; manifest = B1 (`f20155da…`) |
| B5/B6 chủ kho mở lại trên profile đã restore và quan sát | **giữ được phiên** | Nguyên văn: **"Tất cả còn nhưng Claude đòi verify human, tick xong thì vào được."** (`owner-observation.json`) |
| B7 dọn | đạt | đã xoá `backup-u8` và `.damaged-…` (mỗi cái 12 153 tệp); giữ profile (22 mục) và bản cài |

Gói bằng chứng: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\u8\freeze-c\wp-u8-c-evidence.zip`, sha256 `3310b4d70ea3aed613a074b0f38f5fb298179f6851a298ac86792c5e33387289`, 10 tệp, MANIFEST `814f7e02…`, quét secret rc 0. Không chứa tệp nào của profile.

**Kết luận vế đăng nhập: `quan_sat` (theo đặc tả §4, không có PASS/FAIL).**
- Sau khi backup, làm mất và restore profile, **cả 4 phiên đăng nhập còn hiệu lực** theo quan sát của chủ kho.
- Riêng **Claude** bắt xác minh "verify human" (một lần tick) rồi mới vào. Đây là kiểm tra chống bot phía provider, không phải mất phiên.

**Không đo:**
- không có lời gọi `/v1/stats` (REST tắt mặc định);
- không kiểm phiên bằng máy; nguồn duy nhất là quan sát của chủ kho;
- chỉ thử restore **cùng máy, cùng đường dẫn**; restore sang máy hay đường dẫn khác chưa đo.

