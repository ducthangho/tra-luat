# Cross-review packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, lượt 6 (lời gọi Codex 6/6 — CUỐI CÙNG theo trần đã nâng)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `691cb65388e71afb825aeba3b5cbc5359fc4dac5` (cha `3883b60` = merge master `b29da0b`). `origin/master` = `b29da0b`.
- `SPEC.md` — đặc tả đóng băng r2 (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`).
- `DIFF.patch` — `git diff b29da0b..HEAD` (toàn bộ #1021 so master). `DIFF-LUOT6.patch` — `git diff 3883b60..HEAD` (bản vá sau
  lượt 5, chỉ tệp test).
- `VERDICT-LUOT5.md` — verdict lượt 5 của bạn trên `3883b60`: request_changes, một lớp P1
  `bien-ngoai-cua-so-surface-chua-co-rang` (hai biểu hiện: biên đầu tệp `j = 0`; trích dẫn dòng ngay sau), HÌNH DẠNG
  `bo-chon-ung-vien`. `HINT.patch` — bản gợi ý bạn viết ở lượt 5 (sha256 `994c283d…`).
- `luot5-probe/` — script bạn tự viết ở lượt 5 (`mutation_probe.py`, `window_probe.py`, `hint_probe.py`, `run_mutants.py`,
  `audit_merge.py`, `measure.py`…), chép nguyên. Có thể phải chỉnh đường dẫn/mốc neo; ghi rõ chỉnh gì.

Phạm vi lượt này giữ như lượt 5 (chủ kho chọn): diff #1021 + phần giải xung đột với #1037 + các ca biên cửa sổ M4 của `c88`.
Chủ kho duyệt áp `HINT.patch` và dùng lời gọi cuối này. Ghi chú lease (dữ liệu): nền C6 = `tổng 306`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến trên BẢN SAO ĐỦ CÂY, mỗi đột biến một tiến trình.

## Thay đổi từ lượt 5 (executor khai — hãy ĐO)
- Áp NGUYÊN `HINT.patch` (bỏ tiền tố `verdict: approve` + dòng trống khỏi fixture `c88`; thêm hàng `ii-b-trich-dan-dong-sau`;
  thêm `m156_B4_bo_chan_bien_dau_tep` và `m157_B4_trich_dan_bo_dong_sau`, đích `c88`).
- Thêm ngoài HINT: bốn dòng docstring `c88` và một dòng chú thích trên `m156`. Không đổi `ops/bien_nhan_v2.py`.
- Linux trên `691cb65`: `bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`;
  `m156`, `m157` đều `CÓ RĂNG … c88 = giet_that`; `bien_nhan_v2 --root .` `tổng 306`, `TỔNG: ĐẠT`; ruff F delta 0.
- CI Ubuntu, Windows dispatch và Windows local trên `691cb65` đang chạy. Bạn không có Windows: phần chỉ Windows ghi `KHÔNG ĐO ĐƯỢC`.

## Việc của bạn — ĐO, đừng đọc
1. **ĐỐI CHIẾU LƯỢT TRƯỚC.** Chạy lại đúng phép tái hiện P1 lượt 5: `mutation_probe.py no_clamp --suite`, `skip_first`,
   `citation_drop_next`, rồi toàn bộ 40 đột biến cửa sổ của bạn. Đòi: các đột biến sai hành vi nay chết (ở `c88`, hoặc ca khác thì
   nêu tên), `no_clamp` chết qua TOÀN SUITE; đột biến tương đương được phân loại tương đương. Phân loại P1: ĐÃ VÁ THẬT / VÁ HỜ /
   CHƯA VÁ. Xác nhận lại F1/F2/F3 cũ và kết luận giải xung đột lượt 5 vẫn đúng trên head mới.
2. Bỏ tiền tố khỏi fixture `c88`: các hàng cũ (i)…(ix) có còn đo ĐÚNG thứ chúng định đo không (vd hàng nào giờ ngẫu nhiên
   qua vì lý do khác)? Đo bằng `window_probe.py` hoặc phép tương đương.
3. Toàn suite trên head (đòi `TỔNG: ĐẠT`, N/N bằng nhau). Tiêu chí C1a, C1b, C2, C3, C6, C9 của SPEC.
4. Tự nghĩ đột biến cho phần MỚI và báo cái nào SỐNG, vì sao.
5. Phạm vi: `git diff --name-only b29da0b..HEAD` đúng hai tệp write set; `git diff --check`; ruff `--select F` delta 0 so
   `b29da0b`; `doctrine-scan --root .`; `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox (thư mục chứa `cay-kho/`)
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 691cb65388e71afb825aeba3b5cbc5359fc4dac5`.
Dòng 3: `Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, mục `C88 CỬA SỔ M4`, bảng tiêu chí, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh
tái hiện> — <output> — <hướng vá>` kèm dòng `HÌNH DẠNG:`. Ngưỡng approve: không P0/P1/P2/P3 ở BẤT KỲ phần nào. Mỗi khẳng định kèm
lệnh và output; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
