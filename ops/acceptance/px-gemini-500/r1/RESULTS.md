# PX-GEMINI-500 r1 — vì sao `px ask gemini:auto` trả HTTP 500 (r4): **gateway chưa đăng nhập Google** (`cause_measured`)

**Căn cứ:** đặc tả `ops/specs/px-gemini-500-r1.md`, lease `ops/leases/px-gemini-500-r1-g1-operator.yaml`.
Lượt gốc: `../../px-ask/r4/RESULTS.md` (HTTP 500, ~2026-11-20T07:48:21Z) và `../../px-ask/r5/RESULTS.md` (perplexity HTTP 200, ~07:56:43Z).

## 1. Kết luận
**`cause_measured`.** Proxima trả 500 cho `gemini:auto` vì provider gemini trong profile của gateway **không đăng nhập Google**.
Log stdout của gateway ghi đúng một lượt gemini, gồm route chính lẫn fallback, đều hỏng với cùng lý do `Not logged into Google`,
và đánh dấu lỗi là `terminal` nên gateway không thử lần 2. Đây không phải lỗi của module `px` 2.1.0, không phải lỗi map model,
không phải lỗi upstream của Google.

Lời gọi inference của r1: **0**. Phiên chỉ đọc; không dừng/khởi động gateway, không đổi cấu hình, không mở profile/cookie.

## 2. Tệp đã đọc (VM `f7281f27`, tài khoản `tlcommander`, không admin, đo ~2026-11-20T11:2xZ)
Log là đầu ra của wrapper dịch vụ: `ProximaGateway.xml` khai `<logpath>%BASE%\logs</logpath>`, `<log mode="roll"/>`.
`out.log` và `err.log` đang bị gateway giữ mở. Phiên đọc chúng bằng `FileShare.ReadWrite`. Hai tệp này vẫn đang lớn lên,
nên băm dưới đây là **ảnh chụp lúc đọc**, không tái lập được sau này.

| tệp (`<basePath>\logs\`) | sha256 lúc đọc | ghi chú |
|---|---|---|
| `ProximaGateway.out.log` | `02715add70fec760770f5ca2f35aa2465e08de78fe2c393026f506ff3e637245` | 157 708 byte, 1 812 dòng |
| `ProximaGateway.err.log` | `adb6bad0d1e48910430b3961c4e6c38fb9569f16ca8cf3c2ba70a3642c919039` | 8 689 byte, 107 dòng |
| `ProximaGateway.out.log.old` | `21fb5c51ce9be6e5c7e609f3a76e1f1e61e6b01fe0c96d5934756abca2075701` | lượt chạy trước 18-11 14:39Z, không có ca gemini |
| `ProximaGateway.err.log.old` | `d2ea093a6a027134d5f8113cd77506e9e8ede2b5ac6180a4ac62317387cb1e69` | như trên |

`LastWriteTime` của `out.log`/`err.log` hiện `2026-11-19T06:11Z` và `2026-11-18T14:39Z`, cũ hơn sự kiện. Đó là vì Windows
không cập nhật dấu giờ khi tệp còn handle mở. Nội dung thì có dòng của 20-11 (mục 3). Đừng đọc dấu giờ ấy thành "log không có 20-11".

Không đọc: `profile\` (phiên trình duyệt), `settings.json`, mọi tệp cookie/token/credential.

## 3. Trích đoạn (đã che; log không có dấu giờ)
`ProximaGateway.out.log`, dòng 1665–1682 (bỏ các dòng `[chatgpt] Navigated…`/`Turnstile` xen giữa):
```text
1665: [gemini:auto] API attempt 1/2...
1666: [ProviderAPI] Sending via gemini API (Engine: auto)...
1667: [gemini] Error: [Proxima API] Chat processing failed. Not logged into Google
1668: [gemini] Warn: [Proxima API] Gemini route failed (Not logged into Google). Bounded fallback...
1669: [gemini] Error: [Proxima API] Resilient fallback also failed: Not logged into Google
1670: [gemini:auto] API attempt 1 failed (terminal): Not logged into Google
…
1678: [perplexity] API attempt 1/2...
1679: [ProviderAPI] Sending via perplexity API (Engine: auto)...
1681: [ProviderAPI] [OK] perplexity API response: 2 chars in 1.8s
1682: [perplexity] [OK] API response captured (2 chars) on attempt 1
```
`ProximaGateway.err.log`, dòng 95: `[ProviderAPI] [FAIL] gemini:auto API error: Not logged into Google`.

## 4. Vì sao dòng ấy là lời gọi 07:48Z của r4
Log không có dấu giờ, nên phép gán dựa trên **thứ tự và tính duy nhất**, không dựa trên giờ:
- Tiến trình gateway hiện tại (pid 436) khởi động `2026-11-18T14:39:01Z`. Trong toàn bộ `out.log` của nó chỉ có **2** dòng
  `API attempt N/2...`: một của `gemini:auto` (1665), một của `perplexity` (1678). Số dòng nhắc `gemini:auto` là 2,
  cả hai đều thuộc lượt 1665–1670.
- Nhật ký `results\px-active\` từ 18-11 trở đi chỉ có 2 bản ghi: `0627dacb…` (20-11 07:48:23Z, `gemini:auto`, `unknown`) và
  `4f5a868b…` (20-11 07:56:46Z, `perplexity`, `completed`). Thứ tự và số lượng khớp với log.
- Lượt perplexity trả **2 ký tự**, khớp câu trả lời `OK` của r5.

## 5. Dấu hiệu phụ (đo được, chưa xử lý)
- **Gemini hỏng từ trước r4.** Gom `results\px-active\*.json` theo ngày/model/trạng thái: gemini có bản ghi `returned` tới
  2026-11-09. Từ 13-11, mọi bản ghi gemini (`gemini:3-1-pro` ngày 13, 14, 16-11; `gemini:auto` ngày 20-11) đều `unknown`,
  trong khi perplexity vẫn `returned`. Chưa đo được phiên Google mất đúng lúc nào.
- **ChatGPT cũng đang hỏng xác thực.** `err.log` lặp lại `ChatGPT model discovery failed … HTTP 401 … "Provided authentication
  token is expired. Please try signing in again."`. Từ 11-11, mọi bản ghi chatgpt đều `unknown`. `out.log` cho thấy tab chatgpt lặp
  `Navigated to: https://chatgpt.com/` kèm cảnh báo Cloudflare Turnstile.
- Claude: không có bản ghi px-active nào sau 06-11, nên chưa biết trạng thái.

## 6. Cách chữa (chủ kho tự làm qua RDP; phiên không làm hộ)
Trên VM đã có sẵn script đăng nhập trong `<basePath>`. Phiên đã đọc phần đầu của hai script dưới đây, chưa chạy:
1. PowerShell **admin**: `Stop-Service ProximaGateway`, rồi chờ hết tiến trình `Proxima`.
2. Mở phiên đăng nhập bằng tài khoản **`tlcommander`**: `Login-Providers.ps1` đòi đúng user này để phiên trình duyệt thuộc về
   tài khoản dịch vụ. Script tạm đặt `headlessMode=false` rồi mở cửa sổ Proxima; khi Proxima thoát, nó tự trả về `true`.
   Đăng nhập **Gemini (Google)**, và nên đăng nhập lại **ChatGPT** luôn. Sau đó thoát Proxima hẳn (Exit/Quit ở khay hệ thống).
3. PowerShell **admin**: `<basePath>\Finish-Login-And-Start.ps1`. Script này kiểm cửa sổ đăng nhập đã đóng rồi khởi động dịch vụ.
4. Muốn xác nhận thì cấp **1 lời gọi** `px ask` với `gemini:auto`. Phiên này không gửi lời gọi nào.

## 7. Ngân sách
Lời gọi inference 0/0. Lệnh trên VM: chỉ liệt kê thư mục, băm tệp, đọc log và đọc 2 script; không lệnh nào ghi.
