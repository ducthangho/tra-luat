# WP1319 r2 — Bộ test operator P4 đóng băng chạy trên ASUS (lời khai operator, CHƯA review)

- Đặc tả: `ops/specs/wp1319-r2.md` (sha256 `d1c594aa…`). Lease `wp1319-r2-g1-operator`.
- Máy: ASUS `7404cfba`. Khoá `D:\tl-win\KHOA.txt` giữ từ 08:21:57Z đến khoảng 08:53Z ngày 18/11, đã nhả.
  Kiểm tải trước khi chạy: chỉ thấy python của MCP browser-use.
- Thư mục làm việc: `D:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp1319-r2\`. Không ghi gì vào thư mục raw.
- Python `C:\Python313\python.exe` 3.13.1, đúng bản ghi trong raw P4.

| Bước | Kết quả operator | Marker |
|---|---|---|
| M1: chép mã và đối chiếu băm | passed | 15/15 tệp `code/` + `parent/` khớp `export-manifest` của zip P4 `97e9b78f…` |
| M2: `test_recovery.py` | passed | rc 0, `{"passed": true, "cases": 19, "platform": "win32"}`, `real_application_invocations: 0` |
| M3: `test_native_lock.py` | passed | rc 0, `{"passed": true, "cases": 4}` |
| M3: `test_operator_safety.py` | passed | rc 0, `"passed": true`. Tự ghi: `"Windows_native_lock_and_activation": "not run here"` |
| M3: `test_dependency_pins.py` | passed | rc 0, `"known_exact_sdists": 7`, `"negative_cases": 3`. Tự ghi: `"live_metadata_resolver": false`, `"Windows_build": "not run"` |
| M4: mã sau khi chạy | passed | `changed: []`. Chỉ thêm `result-win32.json`, `native-lock-test-result.json`, `own-hostlock-smoke.txt` |
| M5: đóng băng | passed | zip `74f02bd3009861759d764a9a23b539e67d65bc22a1ed75a4be706e05cf313c2f` (32 tệp, 44 737 byte), MANIFEST `362916fc…`. Quét secret rc 0, **lưu trong tệp** `evidence/M5-secret-scan.json`. Scanner sha256 `fbf9392b…` = bản trên master |

19 ca trong `result-win32.json`:
- success, busy, disk-full, partial-copy, promotion-failure, corrupt-backup, corrupt-staging, existing-destination, ownership-changes, restart-failure;
- prior-source reproduces missing restore;
- controller restores once and retains FAIL;
- same restore on success;
- interruption does not auto-recover;
- wrong profile binding rejected;
- dual failure keeps both causes and the lock;
- dual failure message chain;
- **native locked profile rejects rename** (Windows thật);
- **native simultaneous owner denied** (Windows thật).

Phạm vi do chính mã tự ghi: *"actual controller main AST and real owned filesystem, inert application boundary; not Electron, NSIS, cross-version migration or live ASUS proof"*.
Nghĩa là các ca transaction là **fixture** (lỗi được tiêm qua hàm vá). Chỉ hai ca native dùng API tệp Windows thật trên thư mục tạm.
Gói vẫn nằm trên ASUS, không đưa vào kho công khai.
