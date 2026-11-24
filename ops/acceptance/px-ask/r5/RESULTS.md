# PX-ASK-SONG r5 — `px ask perplexity` thật trên VM: HTTP 200, outcome `ok` (`ask_ok`)

**Căn cứ:** đặc tả `ops/specs/px-ask-r5.md`, lease `ops/leases/px-ask-r5-g1-operator.yaml`, Issue #1446. Lượt trước: `../r4/RESULTS.md`.

## 1. Kết luận
**`ask_ok`.** Module proxima-control **2.1.0** (`ac9a06d`), ở chế độ Local trên VM, gửi **đúng 1** yêu cầu inference tới Proxima
qua `POST /v1/chat/completions` với model `perplexity`. Kết quả: HTTP **200**, `outcome: ok`, `reportedModel: perplexity`. Câu trả lời,
coi là dữ liệu **không tin cậy**: `OK`. Bản ghi nhật ký `px.active.v1` ở trạng thái `completed`.

Đây là lần đầu `px ask` chạy trọn vẹn và có câu trả lời thật. Lời gọi inference đã dùng ở r5: **1/1**. Tổng cả packet: 2 lời gọi
(r4 `gemini:auto` HTTP 500, r5 `perplexity` HTTP 200).

## 2. Chuẩn bị của phiên (Desktop Commander, không admin)
- Dùng lại clone module của r4 tại `…\px-ask-r4\repo`. Kiểm lại trước khi chạy: `HEAD` = `ac9a06d442000417e37487e271c646aa6162e3c3`,
  `git status --porcelain` rỗng, 4 tệp module khớp blob (`ProximaControl.psd1` `80dd0566…`, `ProximaControl.psm1` `8c0fe392…`,
  `ProximaConfig.psm1` `59abfa86…`, `Run-Px.ps1` `03f99881…`).
- Cấu hình `px-ask-r5-vm.json` (sha256 `d0bbb042…0cde1`, `targetId` `px-ask-r5-vm`, Local, base gateway như r2/r4).
- `R5.ps1` (sha256 `c570d24e912fdff61b85696ccfd1b493f0d04904c804e8b4b00acd80f83018ac`): model chốt cứng `perplexity`; phân tích cú
  pháp 0 lỗi; trước khi chạy không có tệp đánh dấu.

## 3. Lần chạy của chủ kho (lời khai + phép đo của phiên)
Chủ kho dán vào phiên. Lệnh chạy trong PowerShell admin trên VM qua RDP:
```text
PS C:\Users\<tài khoản admin>> pwsh -NoProfile -ExecutionPolicy Bypass -File "C:\ProgramData\TraLuatCommander\profile\tl-work\px-ask-r5\R5.ps1"
What if: Performing the operation "ask" on target "px target 0e1199384edb".
SHA256 r5-vm.json = 744b602b5a0b140753da6648d1757ff750e73c75c5b4b1f7fc806364b1ccbd80
BUOC CUOI: px_ask ok=True outcome=ok
MODEL: perplexity
HTTP: 200 | TRA LOI (khong tin cay): OK
```
**Phiên đo lại ngay sau đó:**
- sha256 `r5-vm.json` = `744b602b…bd80`, khớp số chủ kho dán.
- Tệp đánh dấu có nội dung `2026-11-20T07:56:43.3840498Z`, tức bước ask thật đã vào đúng một lần.
- Nhật ký `<basePath>\results\px-active\4f5a868b-a703-4cfa-948e-bad6f8e117c0.json`:
  `{"schema":"px.active.v1","action":"ask","targetFingerprint":"0e119938…d121","requestedModel":"perplexity","state":"completed"}`.

Dữ kiện từ `r5-vm.json` (07:56:39Z → 07:56:46Z, PowerShell 7.6.9):

| bước | kết quả |
|---|---|
| `identity` | admin, session 3 (RDP) |
| `gateway_exe` | pid 436, port 3210, session 0, exe `<base>\runtime\Proxima.exe` |
| `import` | ProximaControl **2.1.0**, nạp từ clone r4; băm như mục 2 |
| `px_config` | `ok`, Local, fingerprint `0e119938…d121` |
| `px_status` | `ok`, HTTP 200, `authentication: not_verified_by_status` |
| `px_models` | `ok`, 13 id (như r2/r4), có `perplexity` |
| `px_ask_whatif` | `whatif`, `dryRun` true, không dispatch |
| `px_ask` | `dispatched` true, **HTTP 200**, **`outcome` `ok`**, `requestedModel`/`reportedModel` `perplexity`, `answer` `OK`, `recordState` `completed` |

## 4. Đã chứng minh / chưa chứng minh
- **Đã đo:** `px` 2.1.0, chế độ Local, chạy dưới tài khoản admin trên VM, qua mọi kiểm runtime (session 0, exe, listener đúng PID) và
  nhận một câu trả lời model thật qua Proxima. `PROXIMA_API_KEY` không đặt (r1); gateway vẫn nhận lời gọi.
- **Chưa đo:**
  - danh tính hay phiên bản model thật phía upstream (`reportedModel` chỉ là chuỗi gateway trả về);
  - chất lượng câu trả lời (một từ, không tin cậy);
  - nguyên nhân HTTP 500 với `gemini:auto` ở r4;
  - chế độ Remote/WinRM;
  - chạy dưới tài khoản không admin (r1: bị chặn đúng thiết kế, vì không đọc được exe của gateway).

## 5. Ngân sách
`R5.ps1` 1/1 lần chạy; `ask -WhatIf` 1; `ask` thật **1/1**. Không retry, không đổi model.
