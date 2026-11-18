# WP1319 r4 — Kết quả chạy native trên ASUS (review 2/2: approve_scoped)

Trạng thái lúc 2026-11-18 khoảng 11:05Z:
- Lượt chạy đã **trọn vẹn** từ 10:23:32Z đến 10:29:57Z, `stopped_at: null`.
- Desktop Commander mất kết nối khoảng 10:31–10:56Z, **sau** khi lượt chạy đã xong. Máy không khởi động lại (`LastBootUpTime` 04:05Z).
- Khoá `D:\tl-win\KHOA.txt` đã được harness tự nhả: tệp rỗng, `host_lock_released: true`.
- Không còn tiến trình nào chạy từ `C:\Users\admin\tl-work\wp1319-r4\`.
- Review 2/2 kết luận `approve_scoped` (xem `VERDICT-run.md`). MATRIX đã cập nhật ở mục H.

## Hiện vật (ASUS, ngoài kho)
- Gói đóng băng: `C:\Users\admin\tl-work\wp1319-r4\freeze\wp1319-r4-evidence.zip`.
  - sha256 `cf712bc10783ba5418429e750c8cbfe09f5a5bf87d8cd36a6e54b224a2ae3dcc`, 10 tệp.
  - MANIFEST `42181b74…`.
  - Quét secret rc 0; scanner `fbf9392b…` khớp master.
- `r4_freeze.py` chạy đúng bản `ed7c1fa3…` đã chép lên.
  - Có một lần định vá thêm `inputs\` vào gói nhưng lệnh vá hỏng do PowerShell làm vỡ dấu nháy. Tệp không bị sửa, và freeze đã chạy bằng bản gốc.
  - Vì vậy `inputs\` (`p4-export-manifest.json` `99cfbaf4…`, `p4-code-expected.json` `4298cf46…`, `unittest-win.txt`, `bundle.b64`) **không** nằm trong zip; reviewer đọc trực tiếp trên ASUS.
- Harness `r4_native.py` `3e55da30…`, test `b73b6cc3…` (16/16 đạt trên Windows).
- `p4_code_unchanged: true`, `p4_code_matches_export: true` (15 tệp).

## Kết quả harness (tự khai, **chưa** review)
| Ca | `passed` | Dấu hiệu chính (trích `result.json` / log) |
|---|---|---|
| P0 đối chứng dương | true | `accepted: true`, `verified_files: 3225` |
| A: sửa 1 byte | true | `stage: manifest`, `error: AssertionError('chrome_100_percent.pak')`, `rejection_attributed: true`, `restored_ok: true` |
| B1: đổi kích thước | true | `AssertionError('chrome_200_percent.pak')`, `rejection_attributed: true` |
| B2: thêm tệp lạ `version.dll` | **false** | `accepted: true`, `verified_files: 3225`. **P4 chấp nhận tệp lạ** nằm cạnh `Proxima.exe` (finding) |
| C: feed 5.5.1, sha512 sai | true | Feed `latest.yml` 200, blockmap 404, tải `Proxima-Setup-5.5.1.exe` 200, rồi `[AutoUpdater] Error: sha512 checksum mismatch`. `filter_positive_control: true`, `verified_files: 3225` |
| D1: khoá host trùng | rejected | `winerror: 32` |
| D2: khoá có nội dung | rejected | `size: 17`, `would_raise: HOST_BUSY` |
| D3: kích hoạt Proxima lần hai, cùng profile | **không bị chặn** | Instance hai chạy đủ: `[IPC] Port 19222 in use, trying 19223...`, mở API riêng và updater riêng (cũng tải 5.5.1 rồi bị sha512 từ chối). Không thoát trong 30 s; harness dọn cưỡng bức (`forced_cleanup: true`, `owned_active_after_cleanup: 0`) |
| D tổng | **false** | `first_unaffected: false`, vì instance hai (pid 26124) **ghi đè** `profile-C\rest-port.json`, `ipc-port.json` và `settings.json` (`ipcPort` 19223). Instance một vẫn trả `/v1/stats` và thoát với rc 0. **Sửa P1-1:** cờ `profile_intact: true` chỉ kiểm provider và sentinel; về thực chất, các tệp discovery của profile **đã bị ghi đè**. Phụ lục nằm ở `addendum-profile\` (xem `VERDICT-run.md`) |

Mạng ra ngoài: chỉ có CONNECT tới `fonts.googleapis.com` và `pypi.org`, tất cả bị proxy Deny trả 403. Không có inference; provider tắt.

## Ngân sách
- Codex: 3/3.
- Review: 2/2 (`VERDICT-code.md` request_changes; `VERDICT-run.md` approve_scoped).
- Native: 1 lượt, chưa dùng lần chạy lại.

## Finding của phiên điều phối
- **F-r4-1:** harness không giữ máy thức (`SetThreadExecutionState`). Lần này không ảnh hưởng, vì lượt chạy xong trước khi máy mất kết nối. Cần sửa nếu chạy lại.
