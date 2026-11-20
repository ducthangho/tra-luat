# PX-GEMINI-500 r2 — sau khi đăng nhập lại Gemini: ghi các lời gọi thử của chủ kho và đề xuất sửa gateway Proxima (đặc tả đóng băng)

- **Packet:** #1457 (`px-gemini-500`). Revision 2, generation 1. Role `operator`. Review Class `sensitive`.
- **Căn cứ:**
  - r1 (`ops/acceptance/px-gemini-500/r1/RESULTS.md`): HTTP 500 của `gemini:auto` là do profile Proxima chưa đăng nhập Google.
  - 20-11-2026 chiều: chủ kho tự đăng nhập lại qua RDP (hai lượt `Login-Providers.ps1` + `Finish-Login-And-Start.ps1`) và tự chạy
    3 lời gọi thử tới `http://127.0.0.1:3210/v1/chat/completions`. Chủ kho yêu cầu ghi thành r2 theo đúng quy trình và đề xuất sửa gateway.
- **Máy đích:** chỉ VM `f7281f27-f79f-40a2-a2f5-b454b58a166a` (`tra-luat-win`), phiên đọc dưới `tlcommander`, không admin.

## 1. Việc
1. Ghi 3 lời gọi của chủ kho (lời khai: đầu ra chủ kho dán) và đối chiếu với log gateway (phép đo của phiên, chỉ đọc).
2. Đọc mã `gemini-engine.js` trong `runtime\resources\app.asar` (chỉ đọc, giải nén trong bộ nhớ) để tìm cơ chế của lỗi
   `Gemini stream stalled` và của rác trong câu trả lời.
3. Ghi kết luận + đề xuất sửa vào `ops/acceptance/px-gemini-500/r2/RESULTS.md`. Chỉ chép trích đoạn đã che; KHÔNG chép
   nội dung rác của câu trả lời (lộ chủ đề trong lịch sử tài khoản).

## 2. Ranh giới
- Phiên gửi **0** lời gọi inference. Ba lời gọi trong r2 do chủ kho tự chạy.
- Không đọc profile/cookie/token/`settings.json`; không đổi gateway, `app.asar`, cấu hình, dịch vụ, tài khoản. Đề xuất sửa chỉ là văn bản.
- Không gửi gì ra ngoài kho (không mở issue ở kho Proxima).

## 3. Kết luận và ngân sách
- Kết luận: `fixed_partial` · `fixed` · `not_fixed`.
- Lời gọi inference của phiên: **0**. Review: connector Codex trên PR.

## 4. Write set (không glob)
- `ops/specs/px-gemini-500-r2.md`
- `ops/leases/px-gemini-500-r2-g1-operator.yaml`
- `ops/acceptance/px-gemini-500/r2/RESULTS.md`
