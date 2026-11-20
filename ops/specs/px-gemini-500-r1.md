# PX-GEMINI-500 r1 — tìm nguyên nhân HTTP 500 của `px ask gemini:auto` (chỉ đọc log Proxima trên VM; đặc tả đóng băng)

- **Packet:** px-gemini-500. Revision 1, generation 1. Role `operator`. Review Class `sensitive`.
- **Căn cứ:**
  - `ops/acceptance/px-ask/r4/RESULTS.md`: module 2.1.0 gửi đúng 1 `POST /v1/chat/completions` model `gemini:auto`
    lúc ~2026-11-20T07:48:21Z, gateway trả HTTP 500, `outcome: unknown`, không thân lỗi.
  - `ops/acceptance/px-ask/r5/RESULTS.md`: cùng đường, model `perplexity`, HTTP 200 (~07:56:43Z).
  - Chủ kho 20-11-2026 (qua phiên điều phối `session_015GtxrapMSm976JLC7Fp1HM`) cho phép đọc log Proxima trên VM để chẩn đoán.
- **Máy đích:** chỉ VM `f7281f27-f79f-40a2-a2f5-b454b58a166a` (`tra-luat-win`), tài khoản `tlcommander` không admin.

## 1. Việc
1. Tìm tệp log của Proxima dưới basePath `C:\Users\tlcommander\ProximaGateway` (hoặc thư mục log của runtime).
2. Đọc các dòng quanh mốc 2026-11-20T07:48Z để tìm lý do 500.
3. Ghi kết luận vào `ops/acceptance/px-gemini-500/r1/RESULTS.md`: nguyên nhân đo được hoặc `KHÔNG ĐO ĐƯỢC`, kèm sha256 tệp log đã đọc.
   Chỉ chép trích đoạn đã che, không chép log thô.
4. Trình chủ kho cách chữa.

## 2. Ranh giới
- **0** lời gọi inference. Muốn thử lại phải xin chủ kho cấp từng lời gọi.
- Không đọc profile/cookie/token/credential của Proxima hay trình duyệt; không in giá trị bí mật.
- Không khởi động lại/dừng gateway, không đăng nhập hộ, không đổi cấu hình, dịch vụ, tài khoản, ACL, firewall, WinRM.
  Không chạy lệnh admin; cần admin thì soạn lệnh để chủ kho tự chạy.
- Không gửi message ra ngoài kho.

## 3. Kết luận và ngân sách
- Kết luận: `cause_measured` · `cause_not_measured` · `blocked`.
- Lời gọi inference: **0**. Review: connector Codex trên PR.

## 4. Write set (không glob)
- `ops/specs/px-gemini-500-r1.md`
- `ops/leases/px-gemini-500-r1-g1-operator.yaml`
- `ops/acceptance/px-gemini-500/r1/RESULTS.md`
