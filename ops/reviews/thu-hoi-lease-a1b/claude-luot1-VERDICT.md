# Review Claude độc lập — lượt 1 — spec `THU-HOI-LEASE-A1b` bản nháp 5

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `699057c` (sha256 `468dd6761ba5edf1bbe2f54224b15e02ce9e0006bb23a9041cc4acd90e8119f2`)
- reviewer: subagent Claude (general-purpose), ngữ cảnh mới, read-only; nhãn `same_provider_approved` — bổ sung,
  KHÔNG thay `human_audited` cho phạm vi nhạy cảm; KHÔNG tính vào trần Codex (protocol §8 `:669`, §12 `:1079–1089`)
- thời điểm: 2026-09-27, hoàn tất trước merge `7b99230` (04:30Z)
- ghi chú hình dạng: đây là **tóm lược do phiên điều phối ghi lại** từ báo cáo của subagent, không phải raw output
  bất biến; transcript subagent không nằm trong kho.

VERDICT: changes_requested — **0 P1 / 6 P2 / 2 P3**

Đo lại khớp: hằng A0 :934/:942/:944/:948 (cả `67802bf` và `f5bef3a`); numstat A0 141+919+1327; `git log --all --
ops/thu-hoi/` = 0; 76 first-parent `0721811..67802bf` (77 tới `f5bef3a`); workflow :47/:160; test :5154; hạn #579
g20 (đọc tệp lease qua git); protocol :669, :1079–1089; sha256 r9. Bản vá trần 2 + checkpoint và approve neo `52831cc` đúng.

1. [P2] dòng 7/27(Q9)/105(A3) — neo A1a r2 đã bị r3 (`f5bef3a`, `ac7e0129…`) thay; r3 cấm chạy `do_q6.py`/`mut_q6.py`,
   phải dùng `do_q6_hk.py` (`0ec537e4…`); clock "lúc bật" trái r3 (clock = giờ commit mốc) và làm A3 không thể ĐỎ.
2. [P2] dòng 103(A1) vs 73 — facts đo lại "trong thân PR" mâu thuẫn với biên nhận trong write set; thân PR là bản chiếu sửa được.
3. [P2] Q12/T4/A7 — lần đo ruleset trước lease không vai nào được ghi vào `bien-nhan-thi-cong.md`.
4. [P2] A7/Q3 — hẹp hơn r9 Q10(d): thiếu `merge_queue` và đường push thẳng.
5. [P2] M5/A5 — thiếu chốt delta ngoài bảng (`0→11`, `0→12`, `8→12`) và điều kiện nhận holder mới (r9 R8).
6. [P2] T2 — luật phục hồi bootstrap không có quyết định chủ kho trong §0.
7. [P3] Q2/T3 — sha256 thân comment phụ thuộc đường đọc (MCP chuẩn hoá thực thể HTML).
8. [P3] A8 — ADR-0044 `sensitive` là ≤ 3 tệp **và** ≤ 300 dòng, numstat gồm cả biên nhận.

Xử lý: vá cả 8 ở bản nháp 6 (`4324f2a`).
