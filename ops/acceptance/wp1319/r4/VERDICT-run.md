# WP1319 r4 — Review gói bằng chứng sau khi chạy (lượt review 2/2)

- **Reviewer:** Claude subagent mới (general-purpose), chỉ đọc, context mới. Model tự khai `claude-opus-5-5`, effort `KHONG_do_duoc` (phiên điều phối yêu cầu xhigh).
- **Cách review:** đọc tại chỗ trên ASUS qua Desktop Commander, không ghi gì. Script của reviewer nằm ở scratch của phiên điều phối.
- **Đối tượng:** zip `cf712bc10783ba5418429e750c8cbfe09f5a5bf87d8cd36a6e54b224a2ae3dcc` (MANIFEST `42181b74…`, 10 tệp), cộng `inputs\` đọc tại chỗ.
- **Đây là lần đầu có review độc lập trên bản mã đã sửa** (FIX1 mục 1–18, FIX2 mục 1–2). Reviewer xác nhận có mặt đủ, kèm số dòng.

## Verdict: `approve_scoped`
Kết quả đo đứng vững, và hai FAIL (B2, D) được giữ nguyên. Hai chỗ trong phần viết cần sửa (P1-1 và cách ghi D), không cần chạy lại.

## Kiểm toàn vẹn (reviewer đo lại)
- Zip, MANIFEST và cả 10 dòng khớp byte; `testzip` sạch; không có entry thừa.
- `r4_native.py` khớp `3e55da30…`, `r4_freeze.py` khớp `ed7c1fa3…`.
- Quét secret rc 0. Scanner khớp `scripts/pkg_secret_scan.py` trên master (`fbf9392b…`). Reviewer tự quét thêm 11 entry: 0 hit.
- `inputs\p4-export-manifest.json` khớp byte với entry trong zip P4 `97e9b78f…`. `p4-code-expected.json` được reviewer dựng lại và cho cùng kết quả, 15 tệp.

## Phân loại từng ca (của reviewer)
| Ca | Phân loại | Dấu hiệu | Hàng |
|---|---|---|---|
| P0 | measured_pass | `accepted: true`, 3225 tệp | tiền đề |
| A | measured_pass | `AssertionError('chrome_100_percent.pak')`, `rejection_attributed`, `restored_ok`, không có tiến trình | §11 #6 vế âm |
| B1 | measured_pass | `AssertionError('chrome_200_percent.pak')` | §11 #6 vế âm |
| B2 | **measured_fail (lỗi P4)** | `accepted: true`, 3225 tệp, `version.dll` nằm cạnh `Proxima.exe`; lease thật vẫn được cấp | §11 #6 vế âm: tệp thừa **không** bị chặn |
| C | measured_pass | 6 mẫu health đều 0/0. Có `latest.yml`, blockmap trả 404, installer trả 200. `Update available: 5.5.1` rồi `sha512 checksum mismatch` (reviewer tính lại cả hai băm). Không có dòng "has been downloaded" hay "install on quit". `pending\` rỗng. Thoát êm rc 0. Binary và ASAR trùng byte | U4 |
| D1 | measured_pass | `winerror: 32` (OS thật) | §11 #7 |
| D2 | measured_pass (fixture) | `HOST_BUSY` | §11 #7 |
| D3 | **measured_fail (hành vi sản phẩm)** | `Port 19222 in use, trying 19223...`, không có marker single-instance, `active: 7`. Mã JS của app không có `requestSingleInstanceLock` | §11 #7 vế updater trùng |

## Findings
- **P1-1:** `profile_intact: true` chỉ kiểm provider và sentinel. Thực tế instance trùng (pid 26124) đã ghi đè các tệp discovery của profile, nên tiêu chí "dữ liệu profile không hỏng" **không đạt** về thực chất. Phụ lục do phiên điều phối chụp ngày 18/11, lưu tại `C:\Users\admin\tl-work\wp1319-r4\addendum-profile\`:
  - `settings.json`: 524 B, mtime 10:28:53Z, sha256 `17027adb…` (`ipcPort` 19223);
  - `rest-port.json`: `{"port":64335,"pid":26124,…}`, sha256 `6b58db3b…`;
  - `ipc-port.json`: `{"port":19223,"pid":26124,…}`, sha256 `37224af8…`;
  - `ipc-token.json`: 114 B, mtime 10:28:50Z. **Không đọc** nội dung, theo quy tắc kho về tệp `*token*`.
- **P1-2 (lỗi P4):** đường kiểm trước khi spawn chỉ duyệt các tệp có trong manifest, nên tệp thừa cạnh exe vẫn được chấp nhận. Chưa chứng minh Proxima có thực sự nạp DLL đó hay không.
- **P1-3 (sản phẩm):** Proxima không có khoá single-instance. Lần chạy ngoài khoá host sẽ chạy updater song song và ghi đè các tệp discovery của profile.
- **P2:**
  - `result.json` thiếu `first.pid` và lý do cụ thể của từng điều kiện D.
  - `blocked_external_requests` của C lẫn traffic của D3.
  - Chưa ghi việc `pending\` rỗng.
  - Không ghi lại dòng lệnh, đường dẫn export-manifest, và sha của `variant-manifests.json` (reviewer đo được `96383e5d…`; P4 chỉ ràng buộc `Proxima.exe` `6990dce4…`).
  - `inputs\` không có trong zip.
  - Quét secret chỉ phủ thư mục `results/`.
  - Lỗi sha512 bị nổi lên thành `UnhandledPromiseRejectionWarning`.

## Hàng ma trận theo reviewer
- **§11 #6 vế âm → partial.** Artifact bị sửa nội dung hoặc đổi kích thước bị chặn trước khi spawn (real_os, nhưng vòng assert là bản sao `run()` của P4). Tệp thừa thì **không** bị chặn.
- **U4, nhánh sai integrity → passed (scoped, real_os):** bản mới được chào và tải về, bị từ chối vì sha512, không cài.
- **§11 #7 vế updater trùng → partial.** Khoá của operator chặn được lần chạy trùng; Proxima tự nó thì không.

## Chưa chứng minh
- Cài NSIS thật; tải thành công rồi cài khi thoát.
- Kiểm chữ ký số (không tới bước này vì sha512 đã hỏng trước).
- Installer độc hại nhưng mang băm hợp lệ.
- Biến thể `repaired`; đường tải differential.
- Cô lập trọn vẹn thư mục home (known-folder của Electron).
- Lời gọi mạng trực tiếp từ Node (máy không được ngắt mạng vật lý).
- Khoảng trống giữa các lần poll 5 s.
- DLL thừa có thực sự được nạp hay không.
- Mỗi ca chỉ chạy 1 lần, trên máy đang tải (CPU 59%, RAM trống 0,8 GB).
