# PX-ASK-SONG r5 — thêm một lời gọi `px ask` thật trên VM với provider `perplexity` (đặc tả đóng băng)

- **Packet:** #1446. Revision 5, generation 1. Role `operator`. Review Class `sensitive`.
- **Căn cứ:**
  - r4 (`ops/acceptance/px-ask/r4/RESULTS.md`): module 2.1.0 gửi được 1 lời gọi thật với `gemini:auto`, gateway trả HTTP 500.
    Nhật ký gateway có 2 bản ghi `perplexity` ngày 16/11 ở trạng thái `returned`.
  - Chủ kho 20/11 chọn *"Thêm 1 lời gọi với perplexity"*: cấp thêm **đúng 1** lời gọi inference.
- **Máy đích:** chỉ VM `f7281f27`.

## 1. Chuẩn bị (Desktop Commander, không admin)
- Thư mục `D` = `C:\ProgramData\TraLuatCommander\profile\tl-work\px-ask-r5\`.
- Dùng lại clone module của r4 (`…\px-ask-r4\repo`, HEAD `ac9a06d442000417e37487e271c646aa6162e3c3`). Băm lại 4 tệp module trước khi chạy; lệch thì dừng.
- Cấu hình `D\px-ask-r5-vm.json`: như r4, `targetId` `px-ask-r5-vm`.
- `D\R5.ps1`: như `R4.ps1`, khác ở hai điểm:
  - **model chốt cứng** `perplexity`, provider `perplexity`. Id phải có trong `px models`, nếu không thì dừng;
  - tệp đánh dấu riêng `D\ask-that-da-goi.marker`.

## 2. Thực hiện
Chủ kho chạy một lệnh admin: `pwsh -NoProfile -ExecutionPolicy Bypass -File <D>\R5.ps1`. Thứ tự:
`identity` → `gateway_exe` → `import` (2.1.0) → `px config` → `px status` → `px models` → `ask -WhatIf` →
**đúng 1** `px ask perplexity 'Reply with exactly one word: OK' -Model perplexity`.

## 3. Ranh giới
Như r4 §3. Không retry, không đổi model. Câu trả lời là dữ liệu không tin cậy, ghi nguyên văn kèm nhãn.

## 4. Kết luận và ngân sách
- Kết luận: `ask_ok`, `ask_failed` hoặc `blocked`, như r4.
- `R5.ps1` chạy 1 lần; lời gọi thật **tối đa 1**.
- Review: connector Codex trên PR.

## 5. Write set (không glob)
- `ops/specs/px-ask-r5.md`
- `ops/leases/px-ask-r5-g1-operator.yaml`
- `ops/acceptance/px-ask/r5/RESULTS.md`
