# PX-GEMINI-500 r2 — sau khi đăng nhập lại: `gemini:auto` trả HTTP 200 nhưng chỉ nhờ fallback, chậm và lẫn rác (`fixed_partial`)

> **Đính chính (revision 5, #1457).** Hồ sơ này còn finding P2 chưa vá. Danh sách lớp và finding nằm ở các verdict review §8.3 đăng trên
> Issue #1457: [V1](https://github.com/ducthangho/tra-luat/issues/1457#issuecomment-7048011072) · [V2](https://github.com/ducthangho/tra-luat/issues/1457#issuecomment-7048011557) · [r3](https://github.com/ducthangho/tra-luat/issues/1457#issuecomment-7048537156) · [r4](https://github.com/ducthangho/tra-luat/issues/1457#issuecomment-7053023177).
> Đọc mọi kết luận trong hồ sơ này, kể cả kết luận và nhãn `fixed_partial` ở tiêu đề, như lời khai chưa được xác minh trong kho.
> Nợ chung về định danh vận hành và sổ ngân sách review ghi ở #1471. Nội dung dưới đây giữ nguyên bản đã merge, không sửa.

**Căn cứ:** đặc tả `ops/specs/px-gemini-500-r2.md`, lease `ops/leases/px-gemini-500-r2-g1-operator.yaml`, Issue #1457.
Lượt trước: `../r1/RESULTS.md` (nguyên nhân 500: profile Proxima chưa đăng nhập Google).

## 1. Kết luận
**`fixed_partial`.**
- **Nguyên nhân r1 đã hết.** Sau khi chủ kho đăng nhập lại, log của cả hai lần khởi động gateway không còn dòng
  `Not logged into Google` nào.
- **Gemini trả lời được, nhưng chưa đáng tin.** Lời gọi thứ ba trả HTTP 200 và câu trả lời bắt đầu bằng `OK`. Tuy vậy:
  1. route chính vẫn **treo 20 s** (`Gemini stream stalled`); câu trả lời chỉ có nhờ **fallback**, tổng **43,8 s** cho một từ;
  2. hai lời gọi trước đó cùng cách đăng nhập vẫn 500 vì treo;
  3. câu trả lời **lẫn rác giao diện Gemini**: gateway bắt 252 ký tự, trong đó sau `OK` là một khối `<ElicitationsGroup …>` chứa gợi ý
     câu hỏi tiếp theo. Gợi ý ấy nêu chủ đề có vẻ lấy từ lịch sử trò chuyện của tài khoản Google. Kho **không** chép nguyên văn khối này.
- Lời gọi inference của **phiên: 0**. Ba lời gọi dưới đây do **chủ kho tự chạy**.

## 2. Diễn biến (lời khai của chủ kho + phép đo của phiên)
Chủ kho chạy mọi lệnh trong phiên RDP `tladmin`. Lời gọi đi thẳng tới `http://127.0.0.1:3210/v1/chat/completions`,
prompt `Reply with exactly one word: OK`. Cột "log" là phép đo của phiên qua Desktop Commander.

| # | việc | kết quả chủ kho dán | log gateway |
|---|---|---|---|
| L1 | `Stop-Service` → `runas tlcommander Login-Providers.ps1` → `Finish-Login-And-Start.ps1` | dịch vụ `Running`, pid 10016 (khởi động `2026-11-20T16:20:22Z`) | không còn `Not logged into Google` |
| C1 | `gemini:auto` | **HTTP 500** `Gemini stream stalled: no data received for 25s` (thân lỗi `timestamp` `16:25:51.955Z`) | route chính treo 20 s → fallback treo 25 s → `terminal` |
| C2 | `gemini:3-5-flash-lite` | **HTTP 500** `… stalled … 20s` (`16:28:19.245Z`) | treo 20 s, **không có fallback** |
| L2 | như L1, kèm `-NoExit` và vòng chờ; cửa sổ Proxima có hiện ở session RDP | dịch vụ `Running`, pid 2756 | — |
| C3 | `gemini:auto` | **HTTP 200**, dòng đầu `OK`, kèm một khối `<ElicitationsGroup>` (đã che) | route chính treo 20 s → fallback `[OK] … 252 chars in 43.8s` |

Ở L2, chủ kho không thuật lại những gì đã thấy trong tab Gemini. Vì vậy **không biết** L2 có gỡ được hộp thoại nào không, và C3 đạt có phải
nhờ L2 hay không. Giờ của C3 không được ghi; log gateway không có dấu giờ.

## 3. Tệp đã đọc trên VM (`tlcommander`, không admin; đo ~16:3xZ–16:4xZ)
| tệp | sha256 lúc đọc | ghi chú |
|---|---|---|
| `<basePath>\logs\ProximaGateway.out.log.old` | `c5778caa2d11f909ee771ade126a340ff782e030b75e2284662c0301a53fe99e` | 3 575 byte, 63 dòng; tiến trình pid 10016 (C1, C2) |
| `<basePath>\logs\ProximaGateway.err.log.old` | `370a131281efbd4b92c8c11bf417881df4ea8252b6926dde2e8da0b4154678b4` | 7 130 byte; hai dòng `[FAIL] … stalled` của C1, C2 |
| `<basePath>\logs\ProximaGateway.out.log` | `b6d3cb1a0860ff4400907856af3c8394224963302f659911916dd23aae1f62a5` | 3 287 byte, 60 dòng; pid 2756 (C3); tệp **đang lớn lên**, băm chỉ là ảnh chụp |
| `<basePath>\logs\ProximaGateway.err.log` | `b6d242e99d2fa1a27d461350386570975e7d658f7d898248883ca8c42447deb1` | 6 939 byte; chỉ có lỗi AutoUpdater (404 `latest.yml`), không có lỗi provider |
| `gemini-engine.js` trong `<basePath>\runtime\resources\app.asar` | `1140f71cd9cca5d2a5da12b17d68e1a29c22fad70b7e52831f9e2312e38653cf` | 62 511 byte, 1 431 dòng; trùng băm `integrity` trong header asar; giải nén **trong bộ nhớ**, không ghi ra đĩa |

Proxima bản `5.5.0` (theo `/api/status`). Phiên không đọc `profile\`, `settings.json` hay bất kỳ cookie/token nào.

Trích log C3 (`out.log` dòng 53–58, đã lược):
```text
[gemini:auto] API attempt 1/2...
[gemini] Error: [Proxima API] Chat processing failed. Gemini stream stalled: no data received for 20s
[gemini] Warn: [Proxima API] Gemini route failed (Gemini stream stalled: no data received for 20s). Bounded fallback...
[ProviderAPI] [OK] gemini:auto API response: 252 chars in 43.8s
[gemini:auto] [OK] API response captured (252 chars) on attempt 1
```

## 4. Cơ chế, đọc từ `gemini-engine.js` (số dòng theo tệp trên)
- **Đồng hồ treo** (`_processStreamResponse`, dòng 909–1000): đồng hồ rỗi khởi điểm **20 s** (25 s khi retry, 30 s với engine suy luận;
  dòng 923). Đồng hồ được đặt lại ở **mỗi chunk** (dòng 971). Như vậy `stalled … 20s` nghĩa là trong 20 s **không có byte nào** của
  `StreamGenerate`, chứ không phải parse sai. Riêng lệnh `fetch` có giới hạn chờ header **25 s** (dòng 1239).
- **Ai được fallback** (dòng 1328): `canFallback = !_isRetry && (isAuto || isCode37 || isStreamAbort)`. Thông báo treo không khớp
  `code 37` hay `aborted by Google server`, nên **chỉ `auto` được thử lại**. Điều này khớp với C2 (`3-5-flash-lite` chết ngay sau 20 s).
- **Cắt cụt im lặng (rủi ro, chưa đo):** khi đã thấy một phần câu trả lời (`sawAnswer`), đồng hồ rỗi tụt còn **3,5 s** (dòng 924). Nếu
  hết 3,5 s mà không có chunk mới, vòng đọc dừng; nhánh ném lỗi ở dòng 983 chỉ chạy khi `!sawAnswer`. Kết quả là phần câu trả lời đã có
  được **trả về như thể thành công**. Với câu trả lời dài hoặc mạng chập chờn, đây có thể là câu trả lời bị cụt mà vẫn HTTP 200.
- **Rác `<ElicitationsGroup>`:** `_parseResponse` (dòng 603 trở đi) lấy văn bản từ các khung JSON của luồng mà không lọc thẻ markup
  nào của giao diện Gemini. Khối gợi ý vì thế đi thẳng vào `choices[0].message.content`.
- **Thời gian tới byte đầu là bao nhiêu thì chưa đo được.** Từ C3 chỉ biết: lần gửi đầu không có byte nào trong 20 s; lần fallback có
  dữ liệu trước khi hết đồng hồ 25 s; tổng 43,8 s. Lý do Gemini chậm như vậy (engine suy luận, lịch sử tài khoản, vị trí VM) là **suy đoán**.

## 5. Đề xuất sửa gateway Proxima (chủ kho quyết; phiên không sửa gì)
Proxima là phần mềm bên thứ ba. Sửa `app.asar` tại chỗ sẽ làm lệch băm `integrity` và bị ghi đè khi cập nhật. Vì vậy thứ tự đề xuất là:
**gửi upstream** (chủ kho tự gửi) → **giảm thiểu ở phía ta** → chỉ vá cục bộ nếu chủ kho chấp nhận chi phí bảo trì.

**Sửa trong `gemini-engine.js` (cho upstream):**
1. **Nới và cho cấu hình đồng hồ chờ byte đầu.** Dòng 923 và 1239: đổi 20/25 s thành một giá trị cấu hình được, mặc định ~60 s, đọc từ
   `settings.json` hoặc biến môi trường (ví dụ `PROXIMA_GEMINI_FIRST_BYTE_MS`). Đây là sửa nhỏ nhất, nhắm đúng lỗi C1/C2/C3.
2. **Không trả câu trả lời cụt như thành công.** Ở dòng 983, khi `stalled && sawAnswer` mà chưa thấy khung kết thúc `["e",`, nên
   (a) chờ thêm theo một đồng hồ dài hơn 3,5 s, hoặc (b) đánh dấu `truncated` và trả `finish_reason: "length"` hay lỗi, đừng trả `stop`.
3. **Cho thử lại khi treo với cả model chỉ định.** Dòng 1328: thêm `isStall` (thông báo chứa `stream stalled`) vào điều kiện, và retry
   **cùng engine** thay vì chuyển sang `auto`.
4. **Lọc markup giao diện khỏi văn bản trả về.** Trong `_parseResponse`, bỏ các khối `<ElicitationsGroup …>…</ElicitationsGroup>`
   (và các thẻ cùng họ `<…Group>`/`<…Elicitation …/>`) trước khi trả. Có thể đưa ra metadata riêng nếu cần, không trộn vào `content`.
5. **Ghi log đo được.** Thêm thời gian tới byte đầu, mã HTTP của `StreamGenerate` và dấu giờ ISO cho mỗi dòng log. r1 và r2 đều phải
   gán dòng log cho lời gọi bằng thứ tự, vì log không có giờ.

**Giảm thiểu phía ta, không cần sửa Proxima:**
6. **Tài khoản riêng cho gateway, tắt cá nhân hoá.** Dùng một tài khoản Google chỉ dành cho gateway (hoặc tắt *Gemini Apps Activity* /
   cá nhân hoá trên tài khoản hiện tại), để câu trả lời và gợi ý không kéo theo lịch sử trò chuyện riêng.
7. **Hợp đồng gọi cho `px` / tra-luat:** đặt timeout phía client ≥ 120 s cho `gemini:*`; chỉ dùng `gemini:auto` (model chỉ định không có
   fallback); lọc `<ElicitationsGroup>` trước khi dùng câu trả lời. Việc chạy tự động tiếp tục ưu tiên `perplexity`, đường đã ổn định (r5).
   Mỗi thay đổi ở module `px` là một packet riêng.
8. **ChatGPT:** sau lần đăng nhập lại, `err.log` không còn `HTTP 401 … token is expired` lúc khởi động như ở r1. Đây là suy từ việc lỗi
   **vắng mặt**, chưa có lời gọi chatgpt nào để xác nhận.

## 6. Ngân sách
Phiên: 0 lời gọi inference. Chủ kho: 3 lời gọi thử (C1–C3), 2 lượt đăng nhập/khởi động lại (L1, L2). Lệnh của phiên trên VM chỉ đọc:
liệt kê thư mục, băm tệp, đọc log, giải nén một tệp từ `app.asar` vào bộ nhớ.
