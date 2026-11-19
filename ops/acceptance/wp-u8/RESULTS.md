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

**Trạng thái:** đang chờ chủ kho làm các việc sau:
1. Mở shortcut `Proxima U8 (profile thu)`.
2. Tự đăng nhập các provider muốn thử.
3. **Đóng app.**
4. Báo lại.

Phiên điều phối không làm gì thêm trên profile cho tới lúc đó.
