# Cross-review packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, lượt 7 (lời gọi Codex 7/7 — chủ kho nâng trần lần 2)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## GIỚI HẠN ĐĨA — đọc trước
Đĩa container còn khoảng **350 MB**. Lượt 6 của bạn đã gặp `ENOSPC`. **KHÔNG** sao chép cây kho (không `cp -r`, không `git
clone` thường, không `work/` đủ cây). Làm thẳng trong `cay-kho/` (đã là clone `--shared`). Đột biến dùng cơ chế của chính
bộ test: `_dot_bien_tep` ghi bản sao TẠM của đúng một tệp nguồn; chạy riêng đột biến bằng `_dot_bien(chi={tên})`. Mọi tệp
tạm bạn tạo phải xoá ngay khi xong. Nếu vẫn gặp `ENOSPC`, ghi `KHÔNG ĐO ĐƯỢC` cho phép đo đó, đừng suy.

## Đầu vào trong sandbox
- `cay-kho/` — clone `--shared` (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8` (cha `691cb65`). `origin/master` = `b29da0b`.
- `SPEC.md` (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`).
- `DIFF.patch` — `git diff b29da0b..HEAD`. `DIFF-LUOT7.patch` — `git diff 691cb65..HEAD` (một dòng chú thích).
- `VERDICT-LUOT6.md` — verdict lượt 6 của bạn trên `691cb65`: P1 lượt 5 ĐÃ VÁ THẬT; còn 1 P3
  `chu-thich-nang-ca-thuong-thanh-toan-suite`. `HINT-LUOT6.patch` — bản vá bạn đề xuất (sha256 `fc52cb29…`).

Phạm vi giữ như lượt 5–6 (chủ kho chọn): diff #1021 + phần giải xung đột với #1037 + các ca biên cửa sổ M4 của `c88`.

## Executor khai (hãy ĐO)
- Áp NGUYÊN `HINT-LUOT6.patch`: một dòng chú thích trên `m156`. AST của `ops/bien_nhan_v2_test.py` không đổi so `691cb65`.
- Linux trên `c8a493c`: `bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`.
- Windows CI và Windows local trên `c8a493c` đang chạy; bạn ghi `KHÔNG ĐO ĐƯỢC` cho phần ấy.

## Việc của bạn — ĐO, đừng đọc
1. **ĐỐI CHIẾU LƯỢT TRƯỚC.** P3 lượt 6: so dòng chú thích với nội dung `HINT-LUOT6.patch`, và kiểm câu ấy còn đúng với bằng chứng
   lượt 6 của bạn. So AST `HEAD` với `691cb65` trên hai tệp (đòi giống hệt), và `git diff 691cb65..HEAD` chỉ là một dòng chú thích.
   Phân loại: ĐÃ VÁ THẬT / VÁ HỜ / CHƯA VÁ.
2. Vì AST không đổi, kết luận lượt 6 về P1 `c88`, F1/F2/F3 và giải xung đột còn áp. Vẫn đo lại tối thiểu: toàn suite trong
   `cay-kho` (đòi `TỔNG: ĐẠT`, N/N bằng nhau), và `_dot_bien(chi=…)` cho `m142`, `m147`, `m154`, `m155`, `m156`, `m157` (đòi mỗi cái
   chết đúng ca đích).
3. C6 (`python3 ops/bien_nhan_v2.py --root .` ⇒ `tổng 306`, `TỔNG: ĐẠT`) và C9 (`git diff --name-only b29da0b..HEAD` đúng hai tệp;
   `git diff --check`; ruff `--select F` delta 0 so `b29da0b`; `doctrine-scan --root .`; `rg` glob ⇒ 0 dòng).
4. Có gì khác trong diff #1021 tổng thể mà lượt 5–6 chưa nêu và bạn đo được là lỗi thì báo, kèm mức.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox (thư mục chứa `cay-kho/`)
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8`.
Dòng 3: `Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng tiêu chí, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> —
<hướng vá>` kèm dòng `HÌNH DẠNG:`. Ngưỡng approve: không P0/P1/P2/P3 ở BẤT KỲ phần nào. Mỗi khẳng định kèm lệnh và output; không
đo được thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
