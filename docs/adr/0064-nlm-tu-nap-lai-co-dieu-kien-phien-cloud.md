# ADR-0064 — NLM tự nạp lại jar có điều kiện ở phiên cloud

- **Trạng thái:** Accepted
- **Nguồn:** packet `CLOUD-SETUP-P3B-NLM-401` #1099, đặc tả `ops/specs/cloud-setup-p3b-nlm-401-r11.md` (sha256 `fcd75e67…52a5`).

## Bối cảnh

Quyết định r208c (chú thích quanh `_nlm_auth_load` và chốt chống hạ cấp `_nlm_auth_load_downgrade` trong `scripts/tl_gws.py`; điều cấm ở §4b của `references/RASOAT_HOSO_LOOP.md` và gạch "Sửa xác thực" của `references/QUY_TRINH_RA_SOAT_3_TANG.md`) bác việc tự nạp jar khi hết hạn: bundle có thể CŨ hơn hoặc CŨNG CHẾT, nên vòng nạp-thử-lại quay vô ích. Tiền đề đã đổi: laptop chạy WP710 mỗi 30 phút và từ wp726 chỉ stage `nlm_cred.enc` sau canary LIVE dương, nên nguồn ấy thường tươi hơn bản trong `tl_secrets.enc` mà phiên Claude Code web nạp một lần lúc bootstrap; chốt chống hạ cấp vẫn còn. Phiên cloud không có trình duyệt, nên khi jar chết giữa phiên thì mọi lệnh `nlm` chỉ trả `auth_hint` rồi rơi về MCP.

## Quyết định

ADR này thay r208c ở đúng một điểm, "tự nạp khi hết hạn", và chỉ cho phiên cloud. Cơ chế nằm trong `nlm_cli._run`:

- Chỉ áp dụng khi biến môi trường CLAUDE_CODE_REMOTE có giá trị true.
- Chỉ nạp khi canary _nlm_auth_alive trong tiến trình con trả mã 3 (jar đã chết).
- Chỉ nạp từ nlm_cred.enc bằng tl.py nlm-auth-load, không dùng cờ --force.
- Mỗi tiến trình nạp tối đa 1 lần; cửa sổ 600 giây giữa các tiến trình là best effort, không bảo đảm khi cạnh tranh.
- Chỉ tự chạy lại các lệnh đọc trong danh sách cho phép.
- Nạp xong mà vẫn lỗi xác thực thì dừng và làm theo §4b của RASOAT_HOSO_LOOP.md.

Điều cấm dành cho AGENT không đổi (agent không tự gõ `nlm-auth-load` trong lượt rà; `_AUTH_FIX_RASOAT_CARVE` giữ nguyên).

## Hệ quả

Canary chỉ xét lần thử CUỐI của `_nlm_auth_alive` (chuỗi trộn kết thúc bằng lỗi auth có thể gây một lần nạp thừa) và tệp dấu không có khoá giữa tiến trình; chủ kho chấp nhận cả hai (04-11-2026). `nlm_cred.enc` LIVE đủ tươi hay không chỉ đo được bằng M1.

## Cưỡng chế

Fragment selftest `wp1099_nlm_nap_lai` (ca A1–A13, D1–D3 và bảng đột biến); bảng §20 của protocol đăng ký ADR này (`adr-song`).
