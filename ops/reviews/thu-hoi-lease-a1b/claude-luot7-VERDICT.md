# Review Claude độc lập — lượt 7 (agent `spec-reviewer-max`) — spec `THU-HOI-LEASE-A1b` bản nháp 12

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `8bba697` (sha256 `3cf20e19…`); `origin/master` `5c79fa2`; 446 = 446 ref
- reviewer: subagent Claude agent `spec-reviewer-max` (định nghĩa cục bộ, bị ignore — effort không phải bằng chứng
  runtime, §8 mục 11), read-only; `same_provider_approved` — bổ sung, KHÔNG thay `human_audited`; KHÔNG tính trần Codex
- ghi chú hình dạng: tóm lược do phiên điều phối ghi lại, không phải raw output bất biến.

VERDICT: changes_requested — **1 P1 / 6 P2 / 6 P3**

- F1 [P1] ô quyết định chủ kho bị executor viết lại: Q1–Q12 khác `65a612a`, Q18 nới "bản nháp này" ở `8bba697`;
  Q18 không neo comment; dòng 9 gán `human_audited` cho Q7 nguyên văn (không có).
- F2 [P2] §7 không phân lớp finding lượt 6; "tập rỗng" chạm lượt 3 (6a#1), "mốc giờ lệch" lượt 4 (6b#2) ⇒ checkpoint.
- F3 [P2] PR dữ liệu / PR revert cờ không land được khi digest trôi (workflow chạy mã master, `bypass_actors = []`).
- F4 [P2] A5 kho thật thoả được bởi map ref do executor tiêm.
- F5 [P2] A4 "(executor không tự thoả được A4)" rộng hơn phép đo — ranh giới chủ kho/agent không đo được.
- F6 [P2] "nguồn Q2" trùng tên (A1b Q2 vs r9 Q2); R8(b) không thoả được ở A1b.
- F7 [P2] lệch r9 Q13: thiếu binding kích hoạt + verifier.
- F8–F13 [P3] dòng lịch sử nháp 10/11 thiếu băm; "ba vòng cả ba Theo khuyến nghị"; "bản nháp 1–4 có hai"; A5 dẫn
  docstring `:1318–1319`; T5 "không đo được" trái §1; effort chỉ dựa trên định nghĩa cục bộ.
- đối chiếu tự kiểm nháp 11: #2, #10 (ID Q18), #1 VÁ HỜ; #7 CHƯA VÁ; #10 (A4/Q10) VÁ SINH LỖI MỚI.

Xử lý: checkpoint lần hai ⇒ chủ kho chọn "vá cơ học rồi tạm dừng". Bản nháp 13 vá F1, F2, F6, F7, F8–F12 và F5
(chỉ phần hạ lời khai); F3, F4, F5 (thiết kế), F13 ghi thành nợ mở §8 mục 8–11.
