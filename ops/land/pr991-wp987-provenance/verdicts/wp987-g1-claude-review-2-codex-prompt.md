# Cross-review packet wp987 r1 g1 — lượt 2 (reviewer: codex, review_class: sensitive)

Cùng head ứng viên với lượt 1: `a2e2ebf812f57254affe9344fd02530efa1a0130` (`cay-kho/`, không đổi). Verdict lượt 1 ở
`VERDICT-luot1.md` (cùng thư mục): `blocked`, không P0/P1/P2, phần chặn DUY NHẤT là HƯỚNG 8 — chưa chạy được mẫu
PowerShell vì thiếu `pwsh`.

Phiên điều phối đã cài PowerShell 7.4.6 (bản phát hành chính thức) tại `/opt/pwsh/pwsh` (symlink `/usr/local/bin/pwsh`).
Không có gì trong `cay-kho/` thay đổi.

## Việc
1. Kiểm `pwsh` thật: `/opt/pwsh/pwsh -NoLogo -NoProfile -c '$PSVersionTable.PSVersion.ToString()'`.
2. Chạy lại HƯỚNG 8 bằng chính hiện vật lượt 1 (`review-evidence/powershell-check.ps1`, `check_powershell.py`, fixtures),
   VÀ chạy nguyên văn dòng PowerShell của `.agents/skills/cross-review/SKILL.md` (gán `$Run = Get-Content -Raw -LiteralPath
   $RunJson | ConvertFrom-Json` rồi đọc `$Run.model_phuc_vu`, `$Run.effort_phuc_vu`, `$Run.sandbox_quan_sat` và ba trường
   `*_trang_thai`) trên ít nhất một `run.json` THẬT do launcher ghi: `../runs/da438d8f/run.json` (sổ của chính lượt 1, đã
   kết thúc: `trang_thai: xong`). Đọc tệp ấy chỉ để đo; không sửa.
3. Xác nhận lại nhanh rằng các kết luận lượt 1 còn đúng trên cùng SHA (N1 doctrine-scan, N3 `rg -n 'stderr.log' ...`
   luôn kèm đường dẫn). Không cần chạy lại selftest.
4. Nếu tìm thấy lỗi mới ở bất kỳ hướng nào, ghi như finding thường.

Ghi `VERDICT.md` (ghi đè; giữ cùng dạng lượt 1, thêm mục `## ĐỐI CHIẾU LƯỢT TRƯỚC`). `approve` chỉ khi không còn P0/P1/P2
và không còn phần chặn.
