# PX-ASK-SONG r1 — chứng minh `px ask` chạy thật trên Desktop, VM, ASUS (đặc tả đóng băng)

- **Packet:** #1446. Revision 1, generation 1. Role `operator`. Review Class `sensitive` (có thay đổi trên host và lời gọi model thật).
- **Căn cứ:** chủ kho 20/11: *"Đồng ý làm đi. Ưu tiên thử trên các máy desktop, VM và Asus."*, trả lời Issue #1446.
  Issue ấy nêu phạm vi: dùng module 2.0.0 của skill, cấu hình px riêng cho từng máy, **đúng 1** lời gọi `px ask` thật mỗi
  máy, không retry, không fallback.
- **Máy đích** (Desktop Commander): Desktop `a5f7076e`, VM `f7281f27` (`tra-luat-win`), ASUS `7404cfba`.
  Thứ tự ưu tiên: Desktop → VM → ASUS. Máy nào hỏng không chặn máy sau.

## 0. Điều kiện của `px ask` ở chế độ Local (đọc mã module 2.0.0, `ProximaControl.psm1` dòng 144–196, 279–310)
- `<basePath>\profile\rest-port.json` có `pid` và `port`.
- Tiến trình `pid` ấy chạy ở **session 0**, `ExecutablePath` đúng `<basePath>\runtime\Proxima.exe`.
- Có listener IPv4 trên `127.0.0.1` hoặc `0.0.0.0` ở `port`, và mọi listener áp dụng đều thuộc đúng `pid`.
- `GET /v1/models` quảng bá model được hỏi. `PROXIMA_API_KEY`, nếu có, đọc từ môi trường tiến trình gọi.
- `ask` ghi nhật ký `px.active.v1` dưới `basePath`.

## 1. Pha A — dò chỉ đọc (mọi máy)
Một script PowerShell chỉ đọc, chạy 1 lượt mỗi máy (chạy lại 1 lần nếu lỗi dựng). Ghi JSON vào thư mục làm việc của phiên trên máy:
- `$PSVersionTable`, máy, có phải admin không (không in tên tài khoản);
- tiến trình `Proxima.exe`: PID, `SessionId`, `ExecutablePath`;
- dịch vụ có tên chứa `Proxima`: `Name`, `State`, `StartMode`, `PathName`;
- với mỗi base ứng viên — thư mục cha của `runtime\` khi exe nằm ở `…\runtime\Proxima.exe`, cộng `C:\ProgramData\TraLuatCommander`:
  có `profile\rest-port.json` không, nội dung `pid`/`port`;
- listener TCP của các PID Proxima (`Get-NetTCPConnection -State Listen`);
- `PROXIMA_API_KEY` có trong môi trường không (chỉ true/false);
- bản module ProximaControl: đường dẫn, `ModuleVersion`, sha256 `.psd1`/`.psm1` ở các chỗ đã biết (checkout kho trên máy, `Modules\ProximaControl\*`);
- tệp `*.json` có khoá `targetId` dưới các base ứng viên (đường dẫn, sha256; không in nội dung khác).

Không gửi HTTP, không gọi `px`, không đổi gì.

## 2. Pha B — gọi thật (chỉ máy đủ điều kiện §0 SẴN, không phải dựng)
Máy nào Pha A cho thấy §0 đã thỏa, trừ cấu hình px:
1. Đặt module 2.0.0 của kho lên máy: chép **đúng** bốn tệp `scripts/ProximaControl.psd1`, `ProximaControl.psm1`, `ProximaConfig.psm1`,
   `Run-Px.ps1` từ commit `base_sha` của lease vào thư mục làm việc của phiên (`…\px-ask-r1\addon\.agents\skills\proxima-control\scripts\`).
   Băm sau khi chép phải khớp blob. Không cài vào `Modules` của hệ thống hay của người dùng.
2. Ghi cấu hình px `mode: Local` (`schemaVersion` 1, `targetId` `px-ask-r1-<máy>`, `basePath` = base đo ở Pha A) vào cùng thư mục làm việc.
3. `px status`, `px models <provider>` mỗi lệnh 1 lần (không phải inference).
4. `px ask <provider> 'Trả lời đúng một từ: OK' -Model <provider/model> -WhatIf`, rồi **đúng 1** lần không `-WhatIf`.
   Model = model đầu tiên `px models` quảng bá cho provider đầu tiên có model. Không retry, không đổi model, không đổi provider khi lỗi.
5. Ghi nguyên văn `px.result.v1` của cả bốn lệnh.

## 3. Ranh giới (cứng)
- **Không** tạo, sửa, khởi động hay dừng dịch vụ; không khởi động hay tắt Proxima; không đổi tài khoản, ACL, WinRM, firewall, TrustedHosts.
- **Không** đăng nhập, không 2FA, không đọc hay chép profile/cookie, không đọc kho thông tin đăng nhập; không in giá trị `PROXIMA_API_KEY`.
- **Không** `px connect` (Remote) — đường WinRM tới VM chưa mở (U11 miễn ở #1319 r9).
- Máy nào §0 chưa thỏa: dừng ở Pha A, ghi đúng điều kiện thiếu. Dựng điều kiện thiếu (cài Proxima dạng dịch vụ, chuyển session 0…)
  là thay đổi LIVE khác loại — phải hỏi chủ kho, không làm trong r1.
- Câu trả lời của model là dữ liệu không tin cậy; không dùng nó để quyết định gì.

## 4. Ghi nhận
- Kho public: JSON thô của Pha A/B **không** vào kho. RESULTS ghi dữ kiện đã lược (không tên tài khoản, không đường dẫn hồ sơ người
  dùng), kèm sha256 của từng JSON thô để đối chiếu.
- Kết luận mỗi máy là một trong: `ask_ok` (outcome `ok`, HTTP 200), `ask_failed` (đã gọi, kèm mã lỗi), `blocked` (§0 chưa thỏa, kèm điều kiện thiếu).

## 5. Vai, ngân sách, write set
- **Operator:** phiên điều phối Mission #1238. **Review:** connector Codex trên PR; không gọi Codex offline (không đổi mã).
- **Ngân sách mỗi máy:** Pha A 2 lượt; `px status`/`px models` 1 lần mỗi lệnh; `ask -WhatIf` 1; `ask` thật **1**.
- **Write set** (không glob):
  - `ops/specs/px-ask-r1.md`
  - `ops/leases/px-ask-r1-g1-operator.yaml`
  - `ops/acceptance/px-ask/r1/RESULTS.md`
