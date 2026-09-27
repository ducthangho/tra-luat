# Review Claude độc lập — lượt 6b (đo lại số / băm / dòng / mốc) — spec `THU-HOI-LEASE-A1b` bản nháp 10

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `e009b99` (sha256 `af86b561…`); `ls-remote` 445 = 445 cục bộ lúc đo
- reviewer: subagent Claude (general-purpose), ngữ cảnh mới, read-only; `same_provider_approved` — bổ sung, KHÔNG thay
  `human_audited`; KHÔNG tính vào trần Codex
- ghi chú hình dạng: tóm lược do phiên điều phối ghi lại, không phải raw output bất biến.

VERDICT: changes_requested — **0 P1 / 0 P2 / 5 P3**

Khớp: băm 10 bản nháp + `59916b0`; r9/r3/r2/`do_q6_hk`/`mut_q6_hk`/`q6-do…json`; 76/77 first-parent; giờ commit;
mốc so `git log -S` (03:08Z/441 vào ở `699057c` 03:11Z …); hằng :934–948, :5154, workflow :47/:160; protocol
:669/:1075–1076/:1079–1089; r9 :382–387; r3 :401–405; số P trong lịch sử khớp verdict.

1. [P3] dòng 9 / §7 — bản nháp 1 ghi trần **4**, không phải 10 (`65a612a:9`).
2. [P3] `claude-luot4-VERDICT.md` khai sai "mọi mốc không muộn hơn commit" (02:45Z trong `52831cc` 02:33:31Z).
3. [P3] T2 / §8.6 — 441 = 441 một người đo, không đo lại được, §8.6 không liệt kê.
4. [P3] §2 — số Q6 dẫn từ lượt codex chạy `do_q6.py` (bị Q9 vô hiệu); neo vào `q6-do-2026-09-26.json`.
5. [P3] `claude-tu-kiem-nhap10.md` chỉ neo `a4010f4` (không nhánh nào chứa); thêm sha256 `9e6df411…` + cha `fc26d8d`.
- nit: `claude-luot3-VERDICT.md` dẫn r3 :399–404 (đúng :401–405); tên hình dạng "mốc giờ lệch" phải phủ cả "sớm hơn hiện vật".

Xử lý: vá ở bản nháp 11.
