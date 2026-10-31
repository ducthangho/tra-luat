# Cross-review packet #1037 `BIEN-NHAN-V2-TEST-IN-CHI-TIET-TIN-DUNG-GIA` r1, lượt 2 (lời gọi CUỐI theo trần lease)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường, detached ở head ứng viên `91466322f705658ed51b80c7c152f6b77f4f90c6`.
  **Base = `757bde561d09738858506aecf5de2f050a5f0d5e`** (origin/master lúc cấp lease).
- `SPEC.md` (sha256 `253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230`).
- `DIFF.patch` = `git diff 757bde5..HEAD` (một tệp `ops/bien_nhan_v2_test.py`); `DIFF-LUOT2.patch` = `git diff 016852a..HEAD`
  (vá sau lượt 1).
- `VERDICT-LUOT1.md` — lượt 1 trên `016852a`: request_changes, P2 `c98-khong-khoa-noi-in-that`, P3 `c98-bo-sot-tran-mac-dinh`,
  P3 `c98-bo-sot-so-dong-nem`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
Đột biến chạy trên BẢN SAO ĐỦ CÂY.

## Thay đổi từ lượt 1 (executor khai — hãy ĐO)
1. P2: `_dot_bien(chi=None)` — `do()` bỏ qua đột biến có tên ngoài `chi` khi `chi` được truyền; `main` gọi không đối số. `c98`
   chạy `_dot_bien(chi={"m81_bo_chot_no_chet"})` qua `contextlib.redirect_stdout`, với ca đích c74 thay bằng ca cùng `__name__` ném
   `AttributeError` ⇒ stdout phải có `chi tiết [tin_dung_gia]` + ngoại lệ + `tệp:dòng in hàm` (dòng lấy từ code object); với c74
   thật ⇒ đúng một dòng. Khôi phục `CA[i]` và `_CA` trong `finally`.
2. P3: trần mặc định kiểm bằng `"y"*2000 + "DUOI5"` không truyền `tran` ⇒ đuôi mất, `còn 5 ký tự`, phần 2000 giữ nguyên.
3. P3: fixture hai khung (`_ca_nem_attr` gọi `_nem_trong`); vị trí đòi đúng `tệp:<co_firstlineno+1> in _nem_trong`.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: chạy lại ĐÚNG ba mutant lượt 1 báo sống (`old_print`, `default_cap_infinite`, `wrong_line`) ⇒ phải chết,
   ĐÚNG chốt của `c98` (đọc tên ca + thông điệp).
2. Toàn suite trên head (`TỔNG: ĐẠT`, `N/N` bằng nhau); log đột biến đạt vẫn giống base từng byte (không in thêm khi đạt).
3. Phần MỚI: `chi` có làm `main` chạy thiếu đột biến nào không (so số dòng đột biến head/base)? `c98` gọi `_dot_bien` lồng có rò
   rỉ (`bnv2`, `CONG`, `CA`, `_CA`, `_TAM_DOT_BIEN`, stdout) sang ca sau không — kể cả khi `_dot_bien` lồng ném lỗi? Tự nghĩ đột biến
   cho phần mới (vd. bỏ khôi phục `CA[i]`; bỏ `redirect_stdout`; kiểm ca đạt mà không đếm số dòng). Báo cái nào SỐNG và vì sao.
4. Phạm vi: diff chỉ `ops/bien_nhan_v2_test.py`; không đụng `ops/bien_nhan_v2.py`. `git diff --check`; ruff F delta 0 so base;
   `doctrine-scan`; `python3 ops/bien_nhan_v2.py --root .`.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 91466322f705658ed51b80c7c152f6b77f4f90c6`.
Dòng 3: `Spec sha256: 253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3 (điều kiện merge của chủ kho tính cả P3). Mỗi khẳng định kèm lệnh và output; không đo được thì
ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
