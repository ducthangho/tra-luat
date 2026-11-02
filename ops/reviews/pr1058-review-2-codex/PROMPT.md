# Cross-review PR #1058 — ghi sổ land packet #1045 (biên nhận 3 lượt Codex + hồ sơ land PR #1047), lượt 2

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `3534a6ec9b343cfa484142b14b7c7db7fd3b6f6e`, đủ `refs/remotes/origin/*` (gồm
  `origin/ops/wp1045-r1-g1-lease`). **Base = `afc82f6d7447eb76fc8adbe46c1be90be88d331f`**. `git diff --name-only afc82f6 HEAD` chỉ được
  chạm `ops/reviews/**` và `ops/land/**`.
- `DIFF.patch` = `git diff afc82f6..HEAD`; `DIFF-LUOT2.patch` = `git diff 5dd347c..HEAD` (vá sau lượt 1, chỉ hồ sơ land).
- `VERDICT-LUOT1.md` — lượt 1 trên `5dd347c`: request_changes, P2 `uy-quyen-land-suy-tu-merge`, P3 `nhan-windows-ke-ca-job-skipped`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua tệp
readback trong `ops/land/pr1047-wp1045-provenance/`; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: tái hiện hai phép đo lượt 1 trên head này ⇒ đòi đã đóng (authorization không còn suy quyền land từ thao tác
   merge và khớp điều kiện (5); câu nhãn Windows tách đúng job skipped, đếm khớp readback-jobs-41099486628.json).
2. Các cổng như lượt 1 (`ops/bien_nhan_v2.py --root .`, `ops/land_evidence_nguon.py --root .`, ca `t26_*`/`t27_*`, `doctrine-scan`,
   `git diff --check`), head so base.
3. Rà lại TOÀN hồ sơ `ops/land/pr1047-wp1045-land-evidence.yaml` tìm câu cùng họ (lời khai rộng hơn tệp nguồn, suy quyền từ thao tác,
   đếm gộp job skipped) mà lượt 1 chưa chỉ; biên nhận + README chỉ cần kiểm không hồi quy.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 3534a6ec9b343cfa484142b14b7c7db7fd3b6f6e`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
