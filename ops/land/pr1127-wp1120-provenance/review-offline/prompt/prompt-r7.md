# Review offline độc lập — packet `KIEM-MERGE-M9` r1 (Issue #1120), lượt 7 (lời gọi Codex thứ 7, trần 10 theo ADR-0055@d2e3052)

Bạn là reviewer ĐỘC LẬP (openai_codex), CHỈ ĐỌC: không sửa checkout, không commit/push, không gọi GitHub. Chạy thử trên bản sao tạm.

## Neo
- checkout = cwd, head ứng viên `5f62761` (kiểm `git rev-parse HEAD`). Base `f4b513da5802d439aedbe58ae4a5cd38ff47d6ab`.
- Đặc tả `ops/specs/KIEM-MERGE-M9-r1.md`, sha256 phải là `d18820c854af40a4e0d6ca58f6b8812296a3057b0e7b063f704f5a4cdd7ca442`.
- Lượt 6 đã `KET_LUAN: approve` trên `6c965dc` (không P0–P3). Commit duy nhất sau đó: `git diff 6c965dc 5f62761`.

## Việc
Commit ấy sửa một hồi quy full suite: `moc_dot_bien_phai_khop_DUNG_MOT_CHO` đỏ vì bản vá F25 thêm dòng `        except ValueError:\n`
trùng mốc của đột biến cũ `bien_nhan_bo_nhanh_valueerror`. Bản vá chỉ dời chú thích lên dòng `except` và neo lại đột biến
`m9_mien_phu_quyet_run`. Hãy:
1. Đọc `git diff 6c965dc 5f62761`; xác nhận hành vi không đổi.
2. Chạy chốt mốc toàn bảng: mọi `MUTANTS` có mốc khớp ĐÚNG MỘT chỗ trong `.claude/dev/packet_loop.py` (đo bằng chính ca
   `moc_dot_bien_phai_khop_DUNG_MOT_CHO` qua `chay_suite(..., chi_chay={...})`), rồi các ca `cong_m9_*`, `cong_c_*`.
3. Chạy đột biến `m9_mien_phu_quyet_run` và `bien_nhan_bo_nhanh_valueerror` trên bản sao tạm: ca đích phải chết bằng AssertionError.
4. Chỉ báo finding P0–P2 nếu commit này tạo ra lỗi mới hoặc phá một kết luận lượt 6.

Dòng CUỐI stdout: `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested`.
