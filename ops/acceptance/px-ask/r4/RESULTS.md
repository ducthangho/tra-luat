# PX-ASK-SONG r4 — một lời gọi `px ask` thật trên VM: đã gửi, gateway trả HTTP 500 (`ask_failed`)

**Căn cứ:** đặc tả `ops/specs/px-ask-r4.md`, lease `ops/leases/px-ask-r4-g1-operator.yaml`, Issue #1446. Lượt trước: `../r2/`, `../r3/`.

## 1. Kết luận
**`ask_failed`.** Module 2.1.0 đi trọn đường Local: kiểm runtime, `/api/status`, `/v1/models`, nhận model `gemini:auto`, gửi **đúng 1**
`POST /v1/chat/completions`. Gateway trả **HTTP 500**. Module báo `outcome: unknown`, không retry, không có câu trả lời.
**Lời gọi inference đã dùng: 1/1.**

Như vậy đã chứng minh `px` 2.1.0 gửi được một yêu cầu inference thật tới Proxima trên VM. **Chưa** chứng minh có câu trả lời model qua `px`.

## 2. Chuẩn bị của phiên (Desktop Commander, tài khoản không admin)
- Clone sạch tại `ac9a06d442000417e37487e271c646aa6162e3c3` (merge PR #1450):
  `git init` + `git -c core.autocrlf=false fetch --depth 1 https://github.com/ducthangho/tra-luat.git <SHA>` + `checkout FETCH_HEAD`.
  `HEAD` đo được = SHA ấy. Băm 4 tệp khớp blob trong kho: `ProximaControl.psd1` `80dd0566…`, `ProximaControl.psm1` `8c0fe392…`,
  `ProximaConfig.psm1` `59abfa86…`, `Run-Px.ps1` `03f99881…`.
- Cấu hình `px-ask-r4-vm.json` sha256 `d60ddb88…d87b`. `R4.ps1` sha256 `f95a4ab4106ec9e727757a5fe7ea7cb55df4ff56710a6db68a1cb3249ad09d73`;
  phân tích cú pháp 0 lỗi; trước khi chạy không có tệp đánh dấu.

## 3. Lần chạy của chủ kho (lời khai + phép đo của phiên)
Chủ kho dán vào phiên. Lệnh chạy trong PowerShell admin trên VM qua RDP:
```text
PS C:\Users\<tài khoản admin>> pwsh -NoProfile -ExecutionPolicy Bypass -File "C:\ProgramData\TraLuatCommander\profile\tl-work\px-ask-r4\R4.ps1"
What if: Performing the operation "ask" on target "px target c0996130eb55".
SHA256 r4-vm.json = 45ea666a1245f43a0ed817ce013fa4a4ffcb887ea2c5d1b3aa9651f09fd8b725
BUOC CUOI: px_ask ok=True outcome=unknown
MODEL: gemini:auto
HTTP: 500 | TRA LOI (khong tin cay):
```
**Phiên đo lại ngay sau đó:**
- sha256 `r4-vm.json` = `45ea666a…8b725`, khớp số chủ kho dán.
- Tệp đánh dấu có nội dung `2026-11-20T07:48:21.5799857Z`, tức bước ask thật đã vào đúng một lần.
- Bản ghi nhật ký `<basePath>\results\px-active\0627dacb-65d9-4e02-8d83-b3117dcc88dd.json`:
  `{"schema":"px.active.v1","action":"ask",…,"requestedModel":"gemini:auto","state":"unknown"}`.

Dữ kiện đã lược từ `r4-vm.json` (07:48:18Z → 07:48:23Z, PowerShell 7.6.9):

| bước | kết quả |
|---|---|
| `identity` | admin, session 3 (RDP) |
| `gateway_exe` | pid 436, port 3210, session 0, exe `<base>\runtime\Proxima.exe` |
| `import` | ProximaControl **2.1.0**, băm như mục 2 |
| `px_config` | `ok`, Local, fingerprint `c0996130…431f` |
| `px_status` | `ok`, HTTP 200 |
| `px_models` | `ok`, 13 id (giống r2) |
| chọn model | `gemini:auto` (id `provider:variant` đầu tiên), provider `gemini` |
| `px_ask_whatif` | `whatif`, `dryRun` true, không dispatch |
| `px_ask` | `dispatched` true, **`httpStatus` 500**, `outcome` `unknown`, `answer` null, `reportedModel` null, `recordState` `unknown` |

## 4. Đọc kết quả
- `outcome: unknown` cho mọi status khác 200 là thiết kế của module (`Invoke-PxcAsk`). Module không retry; thân lỗi không được echo
  (ca X5-01 khoá điều này). Vì vậy **không biết nguyên nhân 500** từ phía `px`.
- Cùng thư mục nhật ký có 2 bản ghi cũ ngày 2026-11-16, `provider`/`model` `perplexity`, `state` `returned`. Schema khác (không có
  khoá `schema`), nên không do module 2.x viết. Đây là dấu hiệu gateway từng trả lời thành công cho perplexity. Nguyên nhân 500 với
  `gemini:auto` (ví dụ phiên gemini trong Proxima chưa đăng nhập hoặc đã hết hạn) là **suy đoán, chưa đo**. r4 không đọc log, profile hay
  cookie của gateway, đúng ranh giới §3.
- Câu trả lời model: không có.

## 5. Ngân sách
`R4.ps1` 1/1 lần chạy; `ask -WhatIf` 1; `ask` thật **1/1** (đã dùng hết). Không retry, không đổi model.

## 6. Đường tiếp (chủ kho quyết)
Muốn có một câu trả lời thật qua `px` thì cần **cấp thêm lời gọi inference**. Ứng viên có dấu hiệu tốt nhất là provider `perplexity`
(id `perplexity`, từng `returned` ngày 16/11). Hoặc chủ kho kiểm phiên gemini trong Proxima trước rồi thử lại `gemini:auto`.
