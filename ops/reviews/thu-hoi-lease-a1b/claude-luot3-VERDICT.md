# Review Claude độc lập — lượt 3 — spec `THU-HOI-LEASE-A1b` bản nháp 7

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `19890bf` (sha256 `40e09b25…`)
- reviewer: subagent Claude mới (general-purpose), read-only; `same_provider_approved` — bổ sung, KHÔNG thay
  `human_audited`; KHÔNG tính vào trần Codex
- thời điểm: 2026-09-27, 04:35–04:38Z (sau commit `19890bf`)
- ghi chú hình dạng: tóm lược do phiên điều phối ghi lại, không phải raw output bất biến.

VERDICT: changes_requested — **0 P1 / 2 P2 / 3 P3**

Đo lại khớp (qua git/sha256sum): sha256 r9/r3/r2/`do_q6_hk.py`/`mut_q6_hk.py`/`q6-do-2026-09-26.json`; băm bản nháp
1–6; 76/77 first-parent; hằng :934–948 và test :5154 trên `67802bf`/`f5bef3a`; workflow :47/:160; numstat A0;
ADR-0044:5; protocol :669/:1079–1089; `git grep` T2 rc=1; A3 chép đúng bảng tiêu chí dương r3 (reviewer dẫn :399–404; đúng là `:401–405` — đính chính ở lượt 6b); giờ
commit mốc `2026-09-10T04:55:37Z`.

1. [P2] M5(c) còn miễn trừ "trừ khi Q6 cho phép" trong khi M5(d) cấm vô điều kiện trên fixture; (a) không khai
   tập holder kỳ vọng — nếu fixture dương thêm holder (r9 :385–386) thì (d) làm chính (a) ĐỎ.
2. [P2] A5/Q15 bỏ mất r9 R8(b): delta mở quyền/mất holder trên kho thật phải có nguồn Q2 hoặc cặp lịch sử đúng
   mốc + audit riêng, không chỉ nguyên nhân + lane dừng + expiry.
3. [P3] mốc giờ đo (04:40Z, 04:45–04:50Z) muộn hơn commit chứa chúng.
4. [P3] §8 mục 6 còn liệt kê hạn #579 g20 và ruleset là chưa đo lần hai.
5. [P3] hai tệp verdict khai kiểm các mục đọc qua GitHub mà không ghi đường/giờ đọc.

Xử lý: vá cả 5 ở bản nháp 8.
