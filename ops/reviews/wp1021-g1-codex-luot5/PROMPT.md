# Cross-review packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, lượt 5 (lời gọi Codex 5/6 — chủ kho nâng trần 4 → 6)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Vì sao có lượt này
Lượt 4 đã `approve` head `e9e0048`. Sau đó chủ kho chỉ thị thứ tự merge: PR #1041 (packet #1037, cùng sửa
`ops/bien_nhan_v2_test.py`) vào master TRƯỚC (merge `b29da0b`), rồi nhánh #1021 merge master vào và giải xung đột. Head mới
`3883b60` cần một verdict riêng. Chủ kho cũng chọn gộp vào lượt này phần còn nợ của Issue #1011: xác nhận các ca biên cửa sổ M4
của `c88` (P1 lượt 7 `bien-ngoai-cua-so-surface-chua-co-rang` đã vá ở `fc73522` theo `HINT.patch` của reviewer, nhưng CHƯA có
verdict Codex CLI nào xác nhận). Finding ở phần `c88` cũng chặn merge.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `3883b607c2167758065e408f0fa6eeb580472015` (merge commit: cha 1 `e9e0048`, cha 2 `b29da0b`). `origin/master` = `b29da0b`.
- `SPEC.md` — đặc tả đóng băng r2 (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`).
- `DIFF.patch` — `git diff b29da0b..HEAD` (toàn bộ thay đổi của #1021 so master hiện hành; đúng hai tệp).
- `DIFF-MERGE-SO-E9E0048.patch` — `git diff e9e0048..HEAD` trên hai tệp (phần #1041 kéo vào + phần giải xung đột).
- `DIFF-1041.patch` — thay đổi của #1041 trên `ops/bien_nhan_v2_test.py` (cha thứ nhất của `b29da0b` → `b29da0b`).
- `VERDICT-LUOT4.md` — verdict lượt 4 (`approve` trên `e9e0048`). `luot4-probe/` — script bạn tự viết ở lượt 4, chép nguyên.

Ghi chú lease (dữ liệu): nền C6 = `tổng 306`; C7 (Windows local) theo ADR-0057/0058.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến trên BẢN SAO ĐỦ CÂY, mỗi đột biến một tiến trình.

## Executor khai (hãy ĐO)
- Xung đột: một hunk, hai bên cùng chèn ca mới ngay trước `_chay_1` ⇒ giữ cả hai (khối #1021 trước, khối #1037 sau). Ca
  `c98_chon_bien_nhan_…` của #1021 đổi tên thành `c101_chon_bien_nhan_…` (định nghĩa + đích của `m142` + một tham chiếu trong
  docstring `c99`) để khỏi trùng số với `c98_TIN_DUNG_GIA_…` của #1037. `ops/bien_nhan_v2.py` không xung đột.
- Linux trên `3883b60`: `bien_nhan_v2_test: 98/98 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`;
  `bien_nhan_v2 --root .` `tổng 306`, `TỔNG: ĐẠT`; ruff F delta 0.
- CI Ubuntu, Windows dispatch và Windows local trên `3883b60` đang chạy. Bạn không có Windows: phần chỉ Windows ghi `KHÔNG ĐO ĐƯỢC`.

## Việc của bạn — ĐO, đừng đọc
1. **Giải xung đột đúng.** Không mất dòng nào của bên nào: so `HEAD` với từng cha (`e9e0048`, `b29da0b`) trên hai tệp và giải
   thích mọi khác biệt. Mọi ca, mọi đột biến của CẢ HAI packet còn đó và đếm đúng (`len(CA)`, số đột biến thường). Bảng đột biến
   không còn đích trỏ tên ca cũ (`c98_chon…`). Tên ca/đột biến không trùng. Đầu ra mới của #1037 (`_dong_ket_qua_dot_bien`,
   `_vi_tri_nem`, `chi=`) vẫn hoạt động với các đột biến `m142`–`m155` của #1021.
2. **Không đột biến nào mất răng sau merge**: toàn suite trên head (đòi `TỔNG: ĐẠT`, N/N bằng nhau), rồi đột biến lại riêng ít
   nhất `m142`, `m147`, `m154`, `m155` và đòi chết đúng ca đích mới (`c101` cho `m142`). Đối chiếu lượt 4: F1/F2/F3 cũ vẫn đóng.
3. Tiêu chí C1a, C1b, C2, C3, C6, C9 của SPEC trên head mới.
4. **Ca biên cửa sổ M4 của `c88`** (`ops/bien_nhan_v2.py`, dòng `cua = dong_tep[max(0, j - 1):j + 2]`; ca `c88_…` và đột
   biến `m140`/`m141` trong tệp test). Đo: cửa sổ đúng ba dòng (dòng trước, dòng khai, dòng sau), không hơn không kém, cho cả
   `provider` lẫn trích dẫn `tệp:N`; biên đầu tệp (`j = 0`) và cuối tệp; dòng trống/khoảng trắng; nhiều khai báo gần nhau. Tự
   dựng đột biến cho mọi cách nới/thu hẹp/lệch cửa sổ và báo cái nào SỐNG. Xác nhận hoặc bác P1 lượt 7
   `bien-ngoai-cua-so-surface-chua-co-rang`.
5. Phạm vi: `git diff --name-only b29da0b..HEAD` đúng hai tệp write set; `git diff --check` trên hai tệp; ruff `--select F` delta 0
   so `b29da0b`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`;
   `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox (thư mục chứa `cay-kho/`)
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 3883b607c2167758065e408f0fa6eeb580472015`.
Dòng 3: `Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, mục `GIẢI XUNG ĐỘT`, mục `C88 CỬA SỔ M4` (kết luận riêng về P1 lượt 7), bảng tiêu chí,
bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>` kèm dòng `HÌNH DẠNG:` (`loi-do` /
`bo-chon-ung-vien` / `khac`). Ngưỡng approve: không P0/P1/P2/P3 ở BẤT KỲ phần nào (kể cả `c88`). Mỗi khẳng định kèm lệnh và
output; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
