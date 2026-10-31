# Cross-review packet #1045 `CAI-CONG-CU-DAT-THEO-TRANG-THAI` r1, lượt 3 (lease g2: trần 4 lời gọi sau `nang_tran`; đây là lời gọi 3)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường, detached ở head ứng viên `201460203f42485f589add150896f2febc00c027`.
  **Base = `5e458f4751c83a3811642532c5705ba22d0711c0`** (origin/master). `git diff --name-only 5e458f4 HEAD` phải đúng hai tệp.
- `SPEC.md` (sha256 `8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e`).
- `DIFF.patch` = `git diff 5e458f4..HEAD`; `DIFF-LUOT3.patch` = `git diff b07adcc..HEAD` (vá sau lượt 2, chỉ `launcher_test.py`).
- `VERDICT-LUOT2.md` — lượt 2 trên `b07adcc`: request_changes, 1 P3 `source-thieu-khoa-loi-kiem-cuoi` (hai mutant sống:
  `set +e` chèn sau chỗ khôi phục `set -e`; `|| true` sau kiểm cuối của lượt source). Ba finding lượt 1 đã đóng.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
Đột biến chạy trên BẢN SAO ĐỦ CÂY; xoá mỗi bản sao sau khi dùng (~250 MB/bản). `/tmp/.git` rỗng nếu có: ghi điều kiện đo, so
tập ca đỏ head/base.

## Thay đổi từ lượt 2 (executor khai — hãy ĐO)
Ca mới `r1045_bat_buoc_kiem_cuoi_luot_source_hong_thi_dung_ca_loat`: `--bat-buoc` ba công cụ — (1) bắt buộc cài được · (2) công
thức `true`, bản hỏng đầu PATH ⇒ kiểm cuối lượt source DO (lặp với công cụ (2) tuỳ chọn và bắt buộc) · (3) công thức `touch` dấu.
Đòi rc = 2 và dấu của (3) vắng. Hai đột biến mới trong bảng: `wp1045_sh_errexit_tat_sau_eval`, `wp1045_sh_kiem_cuoi_source_nuot_loi`.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: chạy lại ĐÚNG hai mutant lượt 2 báo sống (`extra_source_errexit_off_preserve_shape`,
   `extra_source_final_error_swallowed`, hoặc tương đương đã đăng ký) ⇒ phải CHẾT đúng chốt của ca mới. Chạy ca mới trên
   `cai_cong_cu.sh` của base: đạt hay đỏ, vì sao (đó là hành vi base cần giữ, không phải lỗi).
2. Toàn suite `python3 .claude/dev/launcher_test.py` head/base (`N/N`, tập ca đỏ, số BỎ QUA); `CONG_CU_TEST_BAN_KINH=manh
   python3 ops/cong_cu_test.py` head/base.
3. Toàn bộ 16 đột biến `wp1045_*` trong bảng + 3 đột biến cũ đã neo lại (`wp858_sh_bo_kiem_ten_tran`, `wp858_sh_chon_theo_ma_thoat`,
   `wp868_sh_go_trap_sau_eval`) ⇒ ca đích ĐỎ đúng chốt. Tự nghĩ thêm cho phần còn lại của bản vá; báo cái nào SỐNG và vì sao.
4. Phạm vi: chỉ hai tệp; `git diff --check`; ruff F delta 0; shellcheck delta 0; `doctrine-scan`.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 201460203f42485f589add150896f2febc00c027`.
Dòng 3: `Spec sha256: 8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
