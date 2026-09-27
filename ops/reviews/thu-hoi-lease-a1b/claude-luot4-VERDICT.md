# Review Claude độc lập — lượt 4 — spec `THU-HOI-LEASE-A1b` bản nháp 8

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `dc647bc` (sha256 `0a534b79…`)
- reviewer: subagent Claude mới (general-purpose), read-only; `same_provider_approved` — bổ sung, KHÔNG thay
  `human_audited`; KHÔNG tính vào trần Codex
- thời điểm: 2026-09-27, sau commit `dc647bc` (04:38:49Z)
- ghi chú hình dạng: tóm lược do phiên điều phối ghi lại, không phải raw output bất biến.

VERDICT: changes_requested — **0 P1 / 2 P2 / 2 P3** (+ 1 nit)

Đo lại khớp (qua git/sha256sum): băm nháp 5–8; r9 `465538…`; 76/77 first-parent; giờ commit `7b99230`/`4324f2a`/
`19890bf`/`dc647bc` và mọi mốc T1/§1/§2/verdict lượt 1–3 không muộn hơn commit chứa nó; hạn g20 khớp tệp lease trên
`origin/ops/cap-lease-579-g20`; r9 R8 :383–385; §8.6; Q15 ↔ A5 khớp; M5(c)/(d) nhất quán.

1. [P2] A6 `ai-dang-giu` dẫn "theo M5(c)" — (c) nay chỉ đo MẤT holder; mutant bỏ kết quả discovery giữ tập cũ vẫn xanh.
2. [P2] M5(a)/A5 — tập holder kỳ vọng do ca test tự khai, không phép đo nào làm ĐỎ tập khai sai (chụp output của mã).
3. [P3] A5 cột ĐỎ "holder mới" mâu thuẫn M5(a) (holder mới trong tập khai là hợp lệ).
4. [P3] T1 mốc đo g20 "~23:30Z 26-09" sớm hơn commit `8168297` (23:32:12Z) tạo lease.
- nit: dẫn r9 `:385–386` cho {r4} → {r1..r4}; đúng là `:386–387`.

Không đo được lại (đã tự khai ở §8.6/T2): 441 = 441 lúc 03:08Z; 100/89 run; annotation Ubuntu 26.

Xử lý: vá cả 4 + nit ở bản nháp 9.

**Đính chính (lượt 6b/6c, 27-09):** câu "mọi mốc T1/§1/§2 … không muộn hơn commit chứa nó" ở trên **sai** — `git log -S'02:45Z'` cho thấy "đo 02:45Z" vào ở `52831cc` (02:33:31Z). Câu "đã tự khai ở §8.6/T2" cho 441 = 441 cũng **sai** lúc đó: §8.6 chưa liệt kê nó (thêm ở bản nháp 11).
