# WP1319 r3 — Chạy lại có chỉnh các bước r1 trên Desktop (lời khai operator, CHƯA review)

- Đặc tả: `ops/specs/wp1319-r3.md` (sha256 `77a6f24b…`). Lease `wp1319-r3-g1-operator`.
- Máy: Desktop `a5f7076e`. Khoá `C:\tl-win` và `F:\tl-win` giữ từ 08:58:00Z đến khoảng 09:35Z ngày 18/11, đã nhả.
- Mã đo: master `13bf69f6`, trên các cây `repo-O1`, `repo-O2`, `repo-O3` mà r1 đã clone. HEAD đã kiểm.
- Gói: `wp1319-r3-evidence.zip` sha256 **`ad9a8a6ea3af924c608ab7381218a370d4c32cc053c595fb36d362cf2fd8fbaf`**, 80 tệp kèm MANIFEST, 262 574 byte. Gói nằm trên Desktop, không vào kho.

| Bước | Kết quả operator | Marker |
|---|---|---|
| R3-N3: 12 lượt (O1/O3 × PS5.1/PS7 × Manifest/Config/Control), luôn `-Counterexamples`, Config và Control luôn `tr-TR` | passed | rc 0 cả 12. Config **46/46**, Control **38/38**, Manifest **12/12** ở mọi tổ hợp, `failed=0`, `cleanup=ok`. Ca `unavailable` (3/1/1) là các ca cần VHD fixture |
| R3-N5: playwright Setup chạy trong tiến trình riêng | passed | `N5-setup.out` có **raw**: `added 3 packages`, `3 packages have verified registry signatures`, `3 packages have verified attestations`, `SETUP OK` |
| R3-N5: Pin, Capture, Cleanup | passed | `PIN OK` (cli 0.1.23, Chromium 157.0.8103.15). Capture `https://example.com/`, request #1 trả 200. `CLEANUP OK` |
| R3-N6: gỡ theo SKILL | passed | 0 tiến trình dùng bản cài. Lock đã cài = lock O3 (`0DA56E1E…`). Đã xoá `install\0.1.0` và `browsers\0.1.0`; **giữ** `runs` và `npm-cache` |
| R3-N6: đo `ms-playwright` (finding) | F1 tái lập | Thêm `daemon\8330401853492c29\tl-pw-8a31fc66b2a1.err` (0 byte), nằm ngoài `TL_PW_ROOT` |
| R3-N7: đóng băng | passed | Quét secret rc 0, **lưu vào** `N7-secret-scan.json`. Scanner sha256 `fbf9392b…` = bản trên master |

r3 nhằm khép bốn finding của review r1: N3 thiếu culture và thiếu counterexamples ở O1; N5 thiếu raw npm; N6 sai tiêu chí; N7 không lưu rc.
r3 **không** chứng minh: hành vi trên gateway thật hoặc WinRM (harness thay backend bằng đồ giả), VM, NSIS, migration, updater.
