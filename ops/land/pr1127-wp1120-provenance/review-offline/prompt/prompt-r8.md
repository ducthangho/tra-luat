# Review offline độc lập — packet `KIEM-MERGE-M9` r1 (Issue #1120), lượt 8 (lời gọi Codex thứ 8, trần 10 theo ADR-0055@d2e3052)

Bạn là reviewer ĐỘC LẬP (openai_codex), CHỈ ĐỌC: không sửa checkout, không commit/push, không gọi GitHub. Chạy thử trên bản sao tạm.

## Neo
- checkout = cwd, head ứng viên `06a5a40` (kiểm `git rev-parse HEAD`), là MERGE commit: cha 1 `5f62761` (đã approve ở lượt 7),
  cha 2 `c82047d` (`origin/master`). Base lease `f4b513da5802d439aedbe58ae4a5cd38ff47d6ab`.
- Đặc tả `ops/specs/KIEM-MERGE-M9-r1.md`, sha256 phải là `d18820c854af40a4e0d6ca58f6b8812296a3057b0e7b063f704f5a4cdd7ca442`.
- Lý do merge: cổng CI `thu-hoi` đòi `origin/master` là tổ tiên của head.

## Việc
1. Xác nhận merge không đổi 5 tệp của write set: `git diff 5f62761 06a5a40 -- .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py
   docs/adr/0060-dieu-kien-merge-va-moc-ready.md .claude/skills/land-packets/SKILL.md ops/specs/KIEM-MERGE-M9-r1.md` phải rỗng; và
   `git diff c82047d 06a5a40 --stat` chỉ gồm đúng 5 tệp ấy.
2. Chạy các ca `cong_m9_*`, `cong_c_*` và chốt `moc_dot_bien_phai_khop_DUNG_MOT_CHO` trên head này (qua `chay_suite(..., chi_chay=...)`).
3. Kiểm phần master mang vào (`.claude/dev/launcher_test.py`, `.claude/dev/codex_cred_test.py`) có tương tác với `packet_loop*.py` không.
4. Chỉ báo P0–P2 nếu merge tạo lỗi mới hoặc phá kết luận lượt 6/7.

Dòng CUỐI stdout: `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested`.
