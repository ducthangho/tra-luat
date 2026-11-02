# Cross-review packet #1045 `CAI-CONG-CU-DAT-THEO-TRANG-THAI` r1, lượt 1 (trần lease: 2 lời gọi)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép đo của chính
bạn. KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC), detached ở head ứng viên `daedfb75e524fa6adc3d68db63b500c2d6c53730`.
  **Base = `059a4a5a080a98270973ef9ce23a38dad5aa2f38`** (origin/master lúc cấp lease). Đo phạm vi bằng base này.
- `SPEC.md` — đặc tả đóng băng (sha256 `8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e`).
- `DIFF.patch` — `git diff 059a4a5..HEAD` (`ops/cai_cong_cu.sh`, `.claude/dev/launcher_test.py`).

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến chạy trên BẢN SAO ĐỦ CÂY. Trước khi đo `launcher_test`
sau một lượt Codex khác, kiểm `ls -d /tmp/.git` (thư mục RỖNG ấy làm đỏ 11 ca `r484_*` — CLAUDE.md), có thì ghi điều kiện đo.

## Bối cảnh
CI Windows run 41069257658 attempt 1: `bash ops/cai_cong_cu.sh shellcheck` in `'shellcheck' ten tran da DAT, giu nguyen PATH` cạnh
`shellcheck: KHONG_DO_DUOC` rồi XANH; bước `G5 probe` đỏ `thieu shellcheck`. Executor khai gốc lỗi: bộ chọn tin rc=0 của
`kiem-tra --chi`, mà `tong_hop` (`ops/cong_cu.py`) chỉ nâng `KHONG_DO_DUOC` khi `bat_buoc: true` (#498, hợp đồng — không đổi).

## Việc của bạn — ĐO, đừng đọc
1. Toàn suite `python3 .claude/dev/launcher_test.py` trên head và base (`N/N`, số BỎ QUA); `CONG_CU_TEST_BAN_KINH=manh python3
   ops/cong_cu_test.py` trên head và base. Thiếu công cụ ⇒ KHÔNG ĐO ĐƯỢC, đừng suy.
2. Phản chứng: chạy `r1045_*` trên bản sao có `ops/cai_cong_cu.sh` của base ⇒ ca nào đỏ, đỏ vì sao.
3. Đột biến trên bản sao: 7 đột biến `wp1045_*` trong bảng (và 3 đột biến cũ đã neo lại) ⇒ ca đích ĐỎ đúng chốt (đọc tên ca +
   thông điệp). Tự nghĩ thêm: `cong_cu_json_dung` bỏ kiểm `ten`/`len(c) == 1`; `RC_CAI` mất mã gốc (luôn 1); nhánh `return 0` của
   lượt source không xoá `$TAM_CAI`; `--bat-buoc` với công cụ BẮT BUỘC hỏng mà rc khác mã cũ. Báo cái nào SỐNG và vì sao.
4. Ngữ nghĩa shell: `( set +e; eval … ) > tệp || RC_CAI=$?` có đổi errexit bên trong subshell không, và mã thoát cuối của script
   có còn bằng mã của lệnh hỏng như trước (CLAUDE.md: bài học `( eval )` vs `$( eval )`)? `return 0` trong lượt `source`, `exit` ở
   lời gọi trực tiếp — đúng chỗ chưa? Đầu ra CRLF của python Windows (`t23` của `cong_cu_test`) qua `cong_cu_json_dung` có vỡ không?
5. Hồi quy: có đường gọi nào (CI `ci.yml`, `ci-dot-bien-du.yml`, `launcher-windows.yml`, `ops/codex_cloud_setup.sh`, hook phiên)
   giờ ĐỎ/XANH khác trước theo cách không mong muốn? Đặc biệt `bash ops/cai_cong_cu.sh rg|shellcheck|actionlint` trên Linux có
   công cụ sẵn.
6. Phạm vi: chỉ hai tệp; không đụng `ops/cong_cu.py`/`ops/cong_cu.yaml`/`ci.yml`. `git diff --check`; ruff F delta 0 so base;
   `shellcheck ops/cai_cong_cu.sh` delta 0; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: daedfb75e524fa6adc3d68db63b500c2d6c53730`.
Dòng 3: `Spec sha256: 8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3 (điều kiện merge của chủ kho tính cả P3). Mỗi khẳng định kèm lệnh và output; không đo được thì
ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
