# Cross-review packet #1037 `BIEN-NHAN-V2-TEST-IN-CHI-TIET-TIN-DUNG-GIA` r1, lượt 1 (trần lease: 2 lời gọi)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép đo của chính
bạn. KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC), detached ở head ứng viên `016852ae7acc22a75bae9505febd1697a1ab79ba`.
  **Base = `757bde561d09738858506aecf5de2f050a5f0d5e`** (origin/master lúc cấp lease). Đo phạm vi bằng base này.
- `SPEC.md` — đặc tả đóng băng (sha256 `253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230`).
- `DIFF.patch` — `git diff 757bde5..HEAD` (đúng một tệp `ops/bien_nhan_v2_test.py`).

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến chạy trên BẢN SAO ĐỦ CÂY (bộ test đọc `.claude/dev/launcher.py`).

## Bối cảnh
Laptop Windows chủ kho, head `7b92e5c`: toàn suite `bien_nhan_v2_test` cho `m81_bo_chot_no_chet → c74_A5_… = tin_dung_gia` đúng một
lần, chạy riêng 22/22 `giet_that`; không truy được vì `do()` chỉ in `mo_ta`, bỏ `ct`, và `_chay_1` chỉ giữ `type: msg`. Bản vá:
`_vi_tri_nem` (khung trong cùng), `_dong_chi_tiet` (tt + ct đủ dòng, trần 2000 + dấu cắt; đạt ⇒ rỗng), `_dong_ket_qua_dot_bien`
(toàn bộ những gì `do()` in), ca `c98`.

## Việc của bạn — ĐO, đừng đọc
1. Toàn suite `python3 ops/bien_nhan_v2_test.py` trên head (đòi `TỔNG: ĐẠT`, `N/N` bằng nhau) và trên base (`git archive` hoặc
   worktree) để so số ca/đột biến. Log của đột biến ĐẠT phải y hệt base ngoài phần thêm mới (không in thêm dòng nào).
2. Mô phỏng ca laptop trên bản sao: làm `m81 → c74` chết vì một ngoại lệ không phải chốt (vd. `AttributeError` khi `bnv2` là module
   đột biến) rồi đọc LOG thật: có tên ngoại lệ, thông điệp, vị trí ném không? Phân hạng `tin_dung_gia` và mã thoát có giữ nguyên?
3. Đột biến trên bản sao: bỏ vị trí ném; `_dong_chi_tiet` luôn rỗng; dây nối `_dong_ket_qua_dot_bien` bỏ chi tiết; bỏ trần; chỉ
   dòng đầu; in cả khi đạt ⇒ `c98` ĐỎ đúng chốt. Tự nghĩ thêm (vd. vị trí lấy khung NGOÀI cùng thay vì trong cùng; `do()` quay về
   `print` cũ không gọi hàm mới). Báo cái nào SỐNG và vì sao.
4. `c98` gọi `_chay_1` lồng trong ca: `_CA` có được khôi phục để `bang()` sau đó vẫn gắn đúng `ca_nguon` không (thử làm một `bang`
   sau lời gọi lồng ĐỎ ⇒ phải là `giet_that`, không phải `tin_dung_gia`)? Có rò rỉ toàn cục nào không?
5. Phạm vi: diff chỉ `ops/bien_nhan_v2_test.py`; không đụng `ops/bien_nhan_v2.py`. `git diff --check`; ruff F delta 0 so base;
   `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `python3 ops/bien_nhan_v2.py --root .`.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 016852ae7acc22a75bae9505febd1697a1ab79ba`.
Dòng 3: `Spec sha256: 253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3 (điều kiện merge của chủ kho tính cả P3). Mỗi khẳng định kèm lệnh và output; không đo được thì
ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
