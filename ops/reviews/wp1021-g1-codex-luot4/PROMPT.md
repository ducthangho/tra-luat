# Cross-review packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, lượt 4 (lời gọi Codex 4/4 — CUỐI CÙNG theo lease)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `e9e0048b48ab610fee1246368b4f134c1ac4ae76`. Base (lúc cấp lease) `757bde561d09738858506aecf5de2f050a5f0d5e` = `origin/master`.
- `SPEC.md` — đặc tả đóng băng r2 (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`).
- `DIFF.patch` — `git diff 757bde5..HEAD`; `DIFF-LUOT4.patch` — `git diff 8d9e3e3..HEAD` (bản vá sau lượt 3, chỉ tệp test).
- `VERDICT-LUOT1.md` (`99c463d`), `VERDICT-LUOT2.md` (`5efa311`), `VERDICT-LUOT3.md` (`8d9e3e3`, request_changes: một P3
  `loi-do-thieu-chot-oserror-ngoai-permissionerror`; F1/F2 lượt 2 ĐÃ VÁ THẬT).
- `luot3-probe/` — các script bạn tự viết ở lượt 3 (`extra_mutate.py`, `errno_probe.py`, `fs_probe.py`, `c100_audit.py`,
  `review_new.py`, `boundary_oracle.py`, `measure.py`…), chép nguyên. Có thể phải chỉnh đường dẫn/mốc neo; ghi rõ chỉnh gì.

Chủ kho đã duyệt làm tiếp sau chốt dừng `bo-chon-ung-vien` của SPEC (30-10-2026). Ghi chú lease (dữ liệu): nền C6 = `tổng 306`;
C7 (Windows local) theo ADR-0057/0058. Đây là lời gọi CUỐI (4/4): không còn lượt sau trong trần này.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến trên BẢN SAO ĐỦ CÂY, mỗi đột biến một tiến trình.

## Thay đổi từ lượt 3 (executor khai — hãy ĐO)
1. Mã sản phẩm `ops/bien_nhan_v2.py` KHÔNG đổi so `8d9e3e3`.
2. `ops/bien_nhan_v2_test.py`: `import errno`; `c99` chốt (4) tiêm cả `PermissionError(EACCES)` lẫn `OSError(EIO)` ở phép liệt kê;
   `c100` chốt (5) và (6) tiêm cả hai lớp ấy ở `is_dir`/`.git exists` (bộ `OS_LOI`). Đột biến mới `m154` (`_hoi_trang_thai` chỉ
   bắt `PermissionError` ⇒ đích `c100`) và `m155` (phép liệt kê chỉ bắt `PermissionError` ⇒ đích `c99`).

## Bằng chứng ngoài sandbox (dữ liệu, không phải phép đo của bạn)
- Executor đo Linux trên `e9e0048`: `bien_nhan_v2_test: 97/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`;
  `bien_nhan_v2 --root .` `tổng 306`, `TỔNG: ĐẠT`; ruff F delta 0 (F541 sẵn có dời 1677 → 1678 vì thêm một dòng import).
- CI Ubuntu và Windows dispatch trên `e9e0048` đang chạy. Bạn không có Windows: phần chỉ Windows ghi `KHÔNG ĐO ĐƯỢC`.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: với F3 lượt 3, chạy lại ĐÚNG phép tái hiện của bạn (`extra_mutate.py narrow_helper --suite`,
   `extra_mutate.py narrow_listing`, `errno_probe.py … EIO|ESTALE`). Đòi: cả hai mutant thu hẹp nay CHẾT đúng chốt (`c100` cho
   helper, `c99` cho liệt kê), đọc tên ca + thông báo, không chỉ rc. Phân loại: ĐÃ VÁ THẬT / VÁ HỜ / CHƯA VÁ. Đồng thời xác nhận
   F1/F2 lượt 2 vẫn đóng (không bị bản vá tệp test làm hở lại).
2. Toàn suite trên head (đòi `TỔNG: ĐẠT`, N/N bằng nhau).
3. Tiêu chí C1a, C1b, C2, C3, C6, C9 của SPEC trên head mới.
4. Tự nghĩ đột biến cho phần MỚI của lượt này và báo cái nào SỐNG. `OS_LOI` có tiêm thật cả hai lớp (đo số lượt trúng theo lớp)?
   Chốt có qua vì lý do khác (ví dụ `OSError(EIO)` bị Python tự đổi thành lớp con nào đó) không? Có rò rỉ thay thế `Path.*` không?
5. Phạm vi: diff chỉ hai tệp write set; `git diff --check`; ruff `--select F` delta 0 so base;
   `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox (thư mục chứa `cay-kho/`)
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: e9e0048b48ab610fee1246368b4f134c1ac4ae76`.
Dòng 3: `Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng tiêu chí, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> —
<hướng vá>` kèm dòng `HÌNH DẠNG:` (`loi-do` / `bo-chon-ung-vien` / `khac`). Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm
lệnh và output; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
