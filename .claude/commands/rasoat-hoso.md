---
description: Chạy MỘT lượt drain vòng lặp rà soát hồ sơ dự thảo luật (Loop A) — đọc state, rà đơn vị pending, cập nhật sau mỗi đơn vị, đóng gói theo ngưỡng context. Kịch bản gốc references/RASOAT_HOSO_LOOP.md
argument-hint: <tên profile hồ sơ> [--dry-rounds 2]
---

Chạy vòng lặp rà hồ sơ theo `references/RASOAT_HOSO_LOOP.md` (thẻ máy: `references/workflows/rasoat_hoso.json`).

**Đọc TRƯỚC khi chạy** (đừng đoán): `references/RASOAT_HOSO_LOOP.md` §0 ranh giới vai · §2 Loop A ·
§7 đường ghi · §8 đóng gói; `references/RASOAT_PLAN_SCHEMA.md` cho cấu trúc state + hằng số.

Trình tự bắt buộc:

1. **A1 Pha 0** — `tl ping --json`, `tl nlm-auth-status --json`; lượt cần NLM thì canary probe LIVE trước
   (KHÔNG tin mô hình tuổi cookie). Fail chặn đứng ⇒ dừng sớm, báo 1 dòng.
2. **A2 nhận vai** — đọc `_meta/rasoat_state.json`; claim quá hạn 30′ mà `progress_ptr` không nhích thì
   chiếm quyền, còn nhích thì LÙI (không giành).
3. **A3–A7 drain** — mỗi đơn vị: rà 3 tầng → VERIFY → ghi `master/<unit>.json` NGOÀI cây skill → cập nhật
   state NGAY. Ứng viên nạp mới gom vào Q-INGEST (lô, duyệt 1 lần), nguồn NLM vào Q-NLM (worker tuần tự).
4. **A8 đóng gói** — đo tại ranh giới đơn vị: 40% context = ngưng nhận đơn vị SÂU; 60% = đóng gói ngay.
   Nghi thức: đẩy sổ → cập nhật state + note bàn giao → NHẢ claim → `tl manifest`.

Ràng buộc: phiên chính là bên ghi duy nhất; agent `tl-rasoat` read-only (spawn xong hậu kiểm
`tl verify-integrity` + `git status`); KHÔNG tự chạy `--apply` — gom vào Q-APPROVALS để người duyệt cả lô;
KHÔNG `/compact` giữa phiên rà (bàn giao qua file).

$ARGUMENTS
