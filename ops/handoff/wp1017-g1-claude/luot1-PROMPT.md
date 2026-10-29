# Cross-review packet #1017 `BIEN-NHAN-V2-TEST-WINDOWS` r1, lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `b2e2410a4b9215480aee6771c1ba8a15a6e14160`. Base `e9967f07b95c6458afc63dabf4a5c0494e90eca7` = `origin/master` lúc cấp lease.
- `SPEC.md` — đặc tả đóng băng (sha256 `e1e709be14e2e7c2a81de39c3acf2666c746e7146116dee669cadee4dad8ed19`).
- `DIFF.patch` — `git diff e9967f0..HEAD` (đúng một tệp `ops/bien_nhan_v2_test.py`).

Trước phép đo: `git config core.abbrev 7`; Python dùng `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

## Ngữ cảnh
Run CI 40833816523, job `gate-ops (windows-latest)`: `bien_nhan_v2_test` 90/93 trên Windows — c93 và c91 `KHÔNG ĐO ĐƯỢC
[gian_giao]`, c96 `ĐỎ`. Executor khai ba gốc lỗi: (1) `write_text`/`text=True` đổi `\n`→`\r\n` trên Windows làm gãy SHA ghim
(c93: `5cfd3f5e87ecd0877a62d75e22c3cf005d842524` / `70363d663b5f549bdc70e2b0ce3838c2ad43ffd7` trong log); (2) Windows báo tên
quá dài là ENOENT (c91); (3) git giả `#!/bin/sh` không đuôi, `CreateProcess` chỉ tìm `git.exe` (c96). Bạn KHÔNG có Windows:
những gì chỉ Windows mới kiểm được thì ghi `KHÔNG ĐO ĐƯỢC`, đừng suy.

## Việc của bạn — ĐO, đừng đọc
1. `python3 ops/bien_nhan_v2_test.py` trên head (đòi `TỔNG: ĐẠT`, `N/N` hai số bằng nhau) và trên base (bản `git archive`).
2. Gốc lỗi (1): dựng lại trên Linux bằng byte CRLF xem có ra đúng hai SHA của log không — đó là bằng chứng nền-độc-lập duy nhất.
3. Đột biến TRÊN BẢN SAO ĐỦ CÂY (bộ test đọc `.claude/dev/launcher.py`; bản sao chỉ `ops/` là rig hỏng):
   - tắt biến thể THẬT (nguồn `run_json_ten_qua_dai` trả None; probe c96 coi như thất bại) để mô phỏng đường Windows, rồi áp
     m116 (`_vang`: `except OSError: return True`) ⇒ c91 phải ĐỎ ở `run_json_lstat_loi_tiem`; áp m125 (`_git_do` bỏ chốt rc) ⇒
     c96 phải ĐỎ ở biến thể `tiem`. Đối chứng: không đột biến sản phẩm ⇒ cả hai qua.
   - tự nghĩ đột biến khác cho phần thêm mới (ví dụ `_tiem_lstat` không gỡ `Path.lstat`, tiêm khớp mọi lệnh thay vì lệnh
     khớp mẫu, probe luôn coi là bọc được) và báo cái nào SỐNG.
   Đọc TÊN CA, nhánh và THÔNG BÁO, không chỉ mã thoát: chết vì lỗi vô can là tín dụng giả.
4. Nhánh tiêm có thể làm ca XANH RỖNG không? (vd. tiêm không tới được mã đang đo, `Path.lstat` bị vá mà `_vang` gọi đường khác,
   `bnv2` bị thay bởi module đột biến nên tiêm vá nhầm module.) Rò rỉ: `Path.lstat`/`bnv2._chay_git` có chắc được trả lại khi
   ca ném lỗi không?
5. `print` "GHI CHÚ" là đủ để người đọc thấy nhánh nào KHÔNG đo trên một nền chưa, hay số ca `N/N` sẽ đọc thành đo đủ?
6. Phạm vi: diff chỉ chạm `ops/bien_nhan_v2_test.py`; không đụng `ops/bien_nhan_v2.py`. `git diff --check`; ruff F delta 0
   (`ruff check --select F`, so base); `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `python3 ops/bien_nhan_v2.py --root .`.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: b2e2410a4b9215480aee6771c1ba8a15a6e14160`.
Dòng 3: `Spec sha256: e1e709be14e2e7c2a81de39c3acf2666c746e7146116dee669cadee4dad8ed19`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3 (điều kiện merge của chủ kho nay tính cả P3). Mỗi khẳng định kèm lệnh và output;
không đo được thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
