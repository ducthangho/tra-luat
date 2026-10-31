# Cross-review packet #1045 `CAI-CONG-CU-DAT-THEO-TRANG-THAI` r1, lượt 2 (lời gọi CUỐI theo trần lease)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường, detached ở head ứng viên `b07adcc2c37215fcb152c94890b9c43f7032bd18`.
  **Base = `5e458f4751c83a3811642532c5705ba22d0711c0`** (origin/master hiện tại; nhánh đã merge nó ở `dcfef4d` để qua check
  `thu-hoi` — merge ấy chỉ mang `ops/land/**` của master). `git diff --name-only 5e458f4 HEAD` phải đúng hai tệp.
  Base lúc cấp lease là `059a4a5` (cha master của merge), không khác về hai tệp này.
- `SPEC.md` (sha256 `8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e`).
- `DIFF.patch` = `git diff 5e458f4..HEAD`; `DIFF-LUOT2.patch` = thay đổi trong write set kể từ head lượt 1 `daedfb7`.
- `VERDICT-LUOT1.md` — lượt 1 trên `daedfb7`: request_changes, P2 `m2-bi-errexit-cat-truoc-thong-bao`, P3
  `recipe-bat-errexit-bi-vo-hieu`, P3 `source-thieu-khoa-don-tam-va-ma-goc`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
Đột biến chạy trên BẢN SAO ĐỦ CÂY; xoá mỗi bản sao sau khi dùng (mỗi bản ~250 MB — lượt trước đĩa đã đầy vì giữ lại). Nếu
`/tmp/.git` rỗng tồn tại thì ghi điều kiện đo, so tập ca đỏ head/base như lượt 1.

## Thay đổi từ lượt 1 (executor khai — hãy ĐO)
1. P2: nhánh gọi trực tiếp thu rc của `kiem-tra --chi … --json` (`|| RC_KT=$?`) rồi `RC_KT≠0 || ! cong_cu_dat` ⇒ dòng stderr nêu
   tên + `exit 3`. Lượt `source` giữ dòng kiểm trần như base.
2. P3: dòng eval về nguyên dạng base; quanh nó `set +e` … `RC_CAI=$?` … `set -e` ở shell cha (không còn `||`).
3. P3: rig `_wp1045_chay` đặt TMPDIR riêng; ca `--bat-buoc` đòi không còn `cai_cong_cu.*` sau hai lượt source; ca bắt buộc hỏng
   dùng `exit 47` và đòi rc == 47. Ca mới (e) DO, (f) bắt buộc vắng, (g) công thức tự bật `set -e`. Đột biến mới:
   `wp1045_sh_kiem_cuoi_tran_duoi_errexit`, `wp1045_sh_eval_trong_ngu_canh_dieu_kien`, `wp1045_sh_source_khong_don_tam`,
   `wp1045_sh_rc_cai_mat_ma`; `wp1045_sh_bo_thoat_3`/`wp1045_sh_thoat_3_ca_luot_source` neo lại.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: tái hiện đúng ba phép đo của lượt 1 (probe DO/bắt buộc vắng; recipe `set -e; false; echo …`; hai mutant
   `extra_source_no_cleanup`, `extra_rc1_preserve_shape`) trên head này ⇒ đòi đã vá, và mutant nay CHẾT đúng chốt.
2. Toàn suite `python3 .claude/dev/launcher_test.py` head/base (`N/N`, tập ca đỏ); `CONG_CU_TEST_BAN_KINH=manh python3
   ops/cong_cu_test.py` head/base.
3. Phần mới: `set +e`/`set -e` quanh eval trong lượt `source` của `--bat-buoc` có làm lệch errexit của shell cha sau đó không (vd.
   lỗi ở công cụ kế tiếp còn dừng như base không)? `exit 3` mới có đổi mã mà người gọi thật (`ci.yml` các bước `cai_cong_cu.sh <tên>`,
   `ops/codex_cloud_setup.sh`) dựa vào không? Tự nghĩ đột biến cho phần mới; báo cái nào SỐNG và vì sao.
4. Phạm vi: chỉ hai tệp; `git diff --check`; ruff F delta 0; shellcheck delta 0; `doctrine-scan`.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: b07adcc2c37215fcb152c94890b9c43f7032bd18`.
Dòng 3: `Spec sha256: 8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
