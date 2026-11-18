# WP1319 r1 — Kết quả kiểm native trên Desktop (operator, CHƯA review độc lập)

Trạng thái: **raw đã đóng băng, chờ reviewer độc lập**. Đây là lời khai của operator. Nó không phải verdict.

- Máy: Desktop `a5f7076e` (Windows, PS 5.1.26100 + pwsh 7.6.10, Python 3.12.10, Node v26.13.0 / npm 11.20.0).
- Mã đo: `13bf69f6eb797e859619a2062e7c9577e6a9cc0b` (tree `a4cb9057…`).
- Đặc tả: `ops/specs/wp1319-r1.md` (sha256 `deee1b43…`).
- Lease: g1 lúc 16:37Z–22:37Z ngày 17/11, hết hạn khi worker của phiên khởi động lại. g2 cấp lúc 00:00Z ngày 18/11.
- Khoá `C:\tl-win` và `F:\tl-win` được giữ trong lúc chạy và đã nhả lúc 00:35Z ngày 18/11.
- Gói bằng chứng: `wp1319-r1-evidence.zip`, sha256 **`54506f1896a1e12d56e7d241a02179d5d75d65cc3255dd55d8aad70b5f8cf24a`**, 365 726 byte, 131 tệp kèm `MANIFEST.json`. `scripts/pkg_secret_scan.py` trên gói trả rc 0.
- Gói nằm **trên Desktop, ngoài kho**, vì kho công khai còn gói chứa tên tài khoản Windows và hostname.

## Bảng bước

| Bước | Kết luận operator | Marker dương (nguyên văn) | Ghi chú |
|---|---|---|---|
| N1 clone | passed | `head=13bf69f6…` `tree=a4cb9057…` `status_lines=0` | |
| N2 bốn lựa chọn × selftest lõi | passed | O0 `== tl selftest 1777/1777 ==` rc 0 (314 s) · O1 cùng marker rc 0 (319 s) · O2 cùng marker rc 0 (315 s) · O3 cùng marker rc 0 (317 s) | Cả 4 bản: 0 tham chiếu tĩnh từ `scripts/` + `SKILL.md` sang add-on. Lượt 1 hỏng là lỗi dựng (xem dưới) |
| N3 proxima-control, O3, kèm counterexamples, `en-US` | **failed (giữ nguyên)** ở Config; passed ở Manifest và Control | Manifest 12/12 (PS5.1, PS7) · Control 38/38 (PS5.1, PS7) · Config **45/46** rc 1 (PS5.1, PS7) | Ca hỏng duy nhất: `CX-cultural-reserved-device`, tức đột biến sống sót dưới `en-US`. Harness tự ghi rằng ca này chỉ được tính điểm dưới `tr-TR` |
| N3D bổ sung, Config, kèm counterexamples, `tr-TR` | passed | **46/46** rc 0 (PS5.1, PS7) | Phép đo bổ sung, không thay kết quả `en-US` |
| N3 proxima-control, O1, chạy chức năng | passed | Manifest 7/7 · Config 21/21 · Control 26/26 (PS5.1, PS7) | Ca `unavailable` cần VHD fixture, không bật trong r1 |
| N4 WhatIf + target | passed | 12/12. `What if: Performing the operation "status"/"restart"/"stop"` rc 0. Từ chối `ArgumentMissing` (thiếu TargetId, thiếu ConfigPath) và `TargetMismatch` (sai hoa/thường) | Ảnh chụp trước/sau bằng nhau trên cả hai edition. Chỉ dùng cấu hình mẫu `gateway.example.invalid`, không đụng gateway thật. Lượt 1 hỏng là lỗi dựng |
| N5 playwright-browser | passed | `SETUP OK` · npm: 3/3 chữ ký registry + 3/3 attestation · `PIN OK` (cli 0.1.23, playwright 1.65.0-alpha-2026-10-30, Chromium 157.0.8103.15 rev 1252) · capture `https://example.com/` (request #1 trả 200, body/PNG/PDF qua kiểm của SKILL) · `CLEANUP OK` | Chạy bằng pwsh 7 |
| N6 gỡ | passed, kèm **finding** | lock O2 = O3 = bản đã cài (`0DA56E1E…`) · 0 tiến trình dùng bản cài · đã xoá `install`/`browsers`, giữ `runs/` | Phát hiện F1 bên dưới |
| N7 đóng băng | passed | zip `54506f18…`, `secret_scan_rc=0` | |

## Phát hiện
- **F1 (P3): dư lượng ngoài `TL_PW_ROOT`.** Daemon của `@playwright/cli` ghi `%LOCALAPPDATA%\ms-playwright\daemon\<băm>\<phiên>.err` và chạm thư mục `b`. Biến `PLAYWRIGHT_BROWSERS_PATH` không chi phối chỗ này. Cleanup (`close` + `delete-data`) và mục "Gỡ bản cài" của SKILL đều không dọn nó.
  - Lượt này để lại 1 tệp 0 byte. Đã có sẵn 11 tệp cùng loại từ các lượt P2/P3 ngày 08–11/11.
  - Mâu thuẫn với lời khai "thư mục RIÊNG" của SKILL ở mức dư lượng, chưa phải rò rỉ dữ liệu.
  - Không xoá vì nằm ngoài write set.
- **F2 (P3): đặc tả r1 thiếu chỉ định culture.** Đây là lỗi của operator. Chọn `en-US` cho lượt kèm counterexamples tạo ra một rc 1 có chủ đích của harness. Đã bổ sung lượt `tr-TR`.

## Lỗi dựng (giữ làm bằng chứng, không phải FAIL sản phẩm)
1. Desktop Commander được khởi từ pwsh, nên `PSModulePath` có đường module PS7 đứng trước, khiến `powershell.exe` 5.1 không thấy `Get-FileHash`. N3/N4 đặt lại giá trị `Machine`.
2. PS5.1 với `ErrorActionPreference=Stop` biến dòng stderr của tiến trình con thành lỗi dừng. Lỗi này làm hỏng N2 lượt 1 (cảnh báo stderr hợp lệ của selftest) và N4 lượt 1 (lời từ chối đúng của sản phẩm). Mỗi bước dùng đúng 1 lần chạy lại theo lease.
3. Khối SKILL lưu thành tệp UTF-8 không BOM thì vỡ parser PS5.1, nên N5 chạy trên PS7.
4. Worker của phiên khởi động lại hai lần (khoảng 17:20Z–23:58Z), làm g1 hết hạn. Đã cấp g2, giữ nguyên bộ đếm.

## r1 KHÔNG chứng minh
- Updater, restore binary + dữ liệu, file lock, đĩa đầy, rollback thất bại, máy bận / khoá trùng, promotion fence (§11 #6–#10).
- U8 đăng nhập, NSIS thực, migration, LIVE.
- Hành vi trên gateway thật hoặc WinRM thật: harness proxima-control thay mọi backend nguy hiểm bằng đồ giả.
- Capture `example.com` không phải xác minh pháp lý.
- Không có inference nào được gửi.
