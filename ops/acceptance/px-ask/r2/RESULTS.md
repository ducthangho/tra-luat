# PX-ASK-SONG r2 — VM, chủ kho chạy lệnh admin: gateway thông, `px ask` vướng định dạng model id; 0 lời gọi model

**Căn cứ:** đặc tả `ops/specs/px-ask-r2.md`, lease `ops/leases/px-ask-r2-g1-operator.yaml`, Issue #1446. Lượt trước: `../r1/RESULTS.md`.

## 1. Kết luận
**`blocked`**: dừng ở bước 4 của đặc tả §2 (chọn model), **trước** `ask -WhatIf` và trước `ask` thật. **0 lời gọi inference.**

Dưới quyền admin, mọi điều kiện runtime của §0 r1 đều thỏa: gateway session 0, exe đúng `<base>\runtime\Proxima.exe`, `px status` HTTP 200,
`px models` trả danh sách. Chỗ chặn mới là **hợp đồng tên model**:
- module 2.0.0 chỉ nhận model id dạng `<provider>/<model>`;
- Proxima trên VM quảng bá id dạng `chatgpt`, `gemini:auto`, `chatgpt:thinking`…, không id nào có `/`.

## 2. Chuẩn bị của phiên (Desktop Commander, tài khoản không admin)
- Bốn tệp module chuyển sang VM dưới dạng zip base64, 4 phần (băm từng phần khớp), zip sha256 `fd85f775…36a0`. Sau khi giải nén, sha256
  từng tệp khớp blob tại `a995f0b`:

| tệp | sha256 |
|---|---|
| `ProximaControl.psd1` | `0c76190d73e2126e2de69185020607f04ef0fb5507836bee211ebdc5d8f2bab6` |
| `ProximaControl.psm1` | `527734a060678f11c95b91c84a36b147f9f5faba0de4a0ff60e8874576f4f668` |
| `ProximaConfig.psm1` | `59abfa860e59af7c596a9e3f60829f8dc1af4a853c5d4ac197c00cc033d76e7d` |
| `Run-Px.ps1` | `03f99881494329cea213714b5e603d83776a7fb57bb153e1a4431d4acc479354` |

- Cấu hình px `px-ask-r2-vm.json` (Local, `basePath` = base đo ở r1), sha256 `d5ca0d47…f6a8`.
- `R2.ps1` sha256 `ae97e324c55ca40848db4e0b4d556f09e4a2f83c19ecf73e0c398f09911f05b8`. Phân tích cú pháp trên VM: 0 lỗi. Script ghi một
  tệp đánh dấu ngay trước `ask` thật và từ chối gọi nếu tệp đã có, nên chạy lại cũng không gọi lần hai.

## 3. Lần chạy của chủ kho (lời khai + phép đo của phiên)
Chủ kho dán vào phiên, chạy trong PowerShell admin trên VM qua RDP (đường hầm IAP 3389):
```text
PS C:\Users\<tài khoản admin>> pwsh -NoProfile -ExecutionPolicy Bypass -File "C:\ProgramData\TraLuatCommander\profile\tl-work\px-ask-r2\R2.ps1"
SHA256 r2-vm.json = 77a2b51a86a4626f86dc4ed37f18bd8e0a2a26a92ea5e9b9381c97cf3fc7e87f
BUOC CUOI: px_models ok=True outcome=ok
DUNG: khong co model dang provider/model
```
- **Đo của phiên** (Desktop Commander, ngay sau đó): sha256 `r2-vm.json` = `77a2b51a…7e87f`, khớp số chủ kho dán. Tệp đánh dấu
  `ask-that-da-goi.marker` **không tồn tại**, tức bước `ask` thật chưa từng được vào. `R2.ps1` trên đĩa vẫn `ae97e324…`.
- JSON thô không vào kho (có đường dẫn hồ sơ). Dữ kiện đã lược từ `r2-vm.json` (`utc_start` 2026-11-20T06:07:53Z, PowerShell 7.6.9):

| bước | kết quả |
|---|---|
| `identity` | `is_admin` true, session 3 (RDP) |
| `gateway_exe` | pid 436, port 3210, session 0, exe `C:\Users\<tài khoản dịch vụ>\ProximaGateway\runtime\Proxima.exe` (đọc được dưới admin; r1 dưới tài khoản không admin thì rỗng) |
| `import` | ProximaControl `2.0.0`, nạp từ `…\px-ask-r2\repo\.agents\skills\proxima-control\scripts\`, băm 4 tệp như bảng mục 2 |
| `px_config` | outcome `ok`, mode `Local`, `targetFingerprint` `867a5e93…78fc` |
| `px_status` | outcome `ok`, `httpStatus` 200 (`GET /api/status`), `authentication: not_verified_by_status` |
| `px_models` | outcome `ok`, 13 id: `perplexity` `chatgpt` `claude` `gemini` `gemini:auto` `gemini:3-8-flash` `gemini:3-1-pro` `gemini:3-5-flash-lite` `chatgpt:auto` `chatgpt:thinking` `chatgpt:instant` `chatgpt:mini` `auto` |
| chọn model | không id nào có `/` ⇒ `model_chosen` null, dừng (đặc tả §2 bước 4) |

## 4. Vì sao `px ask` không thể qua với gateway này (đọc mã, không chạy)
- `Test-PxcModel` (`ProximaControl.psm1`) đòi `Model.StartsWith(Provider + '/')` **và** id khớp đúng một id được quảng bá.
- `Test-PxcProvider` cấm `/` trong provider.
- Không id nào trong 13 id trên có `/`, nên với **mọi** cặp provider/model, `ask` dừng ở `ModelNotAdvertised` trước khi gửi
  `POST /v1/chat/completions`. `px models <provider>` cũng lọc theo tiền tố `provider/`, nên sẽ trả rỗng.
- SKILL.md và help của module ghi `<provider>/<model>`. Định dạng ấy chưa từng được đối chiếu với `/v1/models` của một Proxima thật;
  đây là lần đo đầu tiên. Đây là **finding sản phẩm** của add-on, không phải lỗi cấu hình máy.

## 5. Đã chứng minh / chưa chứng minh
- **Đã đo:** dưới tài khoản admin, đường Local của module 2.0.0 tới được gateway: kiểm runtime (session 0, exe, listener)
  qua; `GET /api/status` 200; `GET /v1/models` 200 và parse được.
- **Chưa đo:** `POST /v1/chat/completions`, tức một câu trả lời model thật qua `px`. Cũng chưa đo việc gateway có đòi `PROXIMA_API_KEY`
  cho lời gọi ấy không (`status` không kiểm xác thực).

## 6. Đường tiếp (chủ kho quyết)
Sửa module để nhận định dạng id thật của Proxima (`<provider>` hoặc `<provider>:<variant>`, có thể chuẩn hoá về một dạng), có test và review
riêng, rồi chạy lại đúng một lời gọi trên VM bằng lệnh admin như r2. Packet đổi mã: không làm trong r2.

## 7. Ngân sách
`R2.ps1`: 1/1 lần chạy (dừng trước bước 6, không cần chạy lại). `ask -WhatIf` 0. `ask` thật **0/1**. Desktop và ASUS: không đụng.
