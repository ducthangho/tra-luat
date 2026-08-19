> **Ghi chú port (GLS-B1, 19-08-2026):** Đây là hồ sơ LỊCH SỬ viết ngày 15/16-08-2026 trên nhánh
> `codex/gate-lifecycle` (đã khai tử — bảo tồn tại tag `archive/codex-gate-lifecycle-ec8d08c`, blob gốc
> `99a80208…`). Phần phòng ngừa phía launcher/doctor đã vào master qua bản LÀM LẠI (`ops/gate-lifecycle`,
> PR #141 và các đợt sau — KHÔNG phải qua nhánh này); riêng "SessionStart chuyển sang exec-form gọi bridge
> Python" land CÙNG packet GLS-B1 này. Trạng thái credential mô tả bên dưới là ảnh chụp thời điểm đó,
> có thể đã đổi. Thân tài liệu dưới dòng này giữ nguyên văn.

# Postmortem — launcher, Codex, GitHub và toolchain Windows ngày 15-08-2026

- **Trạng thái:** mã phòng ngừa đã triển khai trên nhánh; `rg`, Claude và GitHub connector dùng được; còn chờ người dùng cấp lại credential cho Codex CLI và GitHub CLI.
- **Phạm vi:** launcher/doctor, Claude Code SessionStart, Codex CLI, GitHub CLI, `rg`, Bash.
- **Không chứa bí mật:** chỉ ghi sự hiện diện/nguồn và mã kết quả; không ghi giá trị token.

## Điều đã xảy ra

Các phép đo trực tiếp ngày 15-08-2026 cho thấy:

| Thành phần | Bằng chứng | Kết luận |
|---|---|---|
| Claude | `claude --version` và `claude auth status` thoát 0 | dùng được |
| Codex | `codex --version` xanh; `codex login status` trả `Not logged in`/rc khác 0 | có binary nhưng không gọi phiên được |
| GitHub CLI | `gh --version` xanh; `gh auth status` báo credential mặc định không hợp lệ | có binary nhưng không gọi GitHub qua `gh` được; không suy rộng sang connector |
| biến GitHub | `GITHUB_PAT` có; `GH_TOKEN`/`GITHUB_TOKEN` không có; ánh xạ PAT sang `GH_TOKEN` vẫn auth đỏ | credential hiện có đã sai/hết hạn, không chỉ sai tên biến |
| ripgrep | tên `rg` trỏ vào `...WindowsApps\OpenAI.Codex...\rg.exe`, CreateProcess trả WinError 5 | có path nhưng không thực thi được |
| Bash | tên `bash` trỏ vào `C:\Windows\System32\bash.exe`, trả `E_ACCESSDENIED`; Git Bash tốt có ở Program Files | shell-form chọn nhầm shim |
| khóa tiến trình | `Get-CimInstance Win32_Process` trả `CimException: Access denied` trong sandbox | deadline/stop không lấy được khóa PID, trả sai 10/125 |
| doctor cũ | báo `rg`/`bash` HỎNG nhưng vẫn in `ĐỦ CÔNG CỤ BẮT BUỘC`; không đo `gh`/auth | fail-open |
| cài `rg` | lệnh gợi ý `winget` thất bại vì máy không có `winget`; `choco install ripgrep` thành công | chỉ ghi một package manager là hướng dẫn không đủ |

`doctor` cũ còn probe tuần tự với timeout riêng cho từng lệnh. Một shim chậm có thể làm lệnh trông như treo hàng chục giây dù cuối cùng có output.

## Tái kiểm tra ngày 16-08-2026

- Mốc bắt đầu tái kiểm tra là HEAD `824517859a1a0974547ff79354df85c1efe9a42e` với launcher `1.1.0`; bản vá auth-envelope trong working tree nâng phiên bản lên `1.1.1`. Trong lúc kiểm tra, `origin/master` tiến thêm hai commit (`672522c`, merge `d5b7bcc`), nên nhánh `codex/gate-lifecycle` hiện diverged: ahead 2, behind 2. Các thay đổi lần này chưa commit; chưa tự merge/rebase vì hai phía cùng chạm launcher/hook.
- `python -B .claude/dev/launcher.py doctor --json` hoàn tất sau khoảng 11 giây, trả rc=12; môi trường được ghi nhận là đã đọc trước resolve/probe. Binary `git`, `python`, `claude`, `codex`, `gh`, `rg`, `bash`, `npm`, `node` đều chạy được. Chỉ auth Codex CLI và `gh` đỏ.
- `claude auth status` thoát 0. Một lời gọi `claude -p` tối giản ở safe mode, tắt tools, đã thật sự nhận phản hồi mô hình và thoát 0; vì vậy Claude không chỉ “có binary” hoặc “có auth trên đĩa”.
- Codex Desktop đang dùng được, nhưng đây không phải bằng chứng cho Codex CLI. `codex login status` vẫn thoát 1; không có `CODEX_AUTH_JSON` hay `OPENAI_API_KEY` trong môi trường đã chụp.
- GitHub connector xác thực được tài khoản `ducthangho` và đọc repo private `ducthangho/tra-luat` với quyền admin/push. Đường connector vì vậy dùng được. Riêng `gh auth status --hostname github.com` vẫn thoát 1; doctor mới đã thử cả `credential_store` lẫn `GITHUB_PAT->GH_TOKEN`, và cả hai đều đỏ.
- `rg 15.2.0` chạy từ `D:\\chocolatey\\bin\\rg.exe`; Git Bash chạy từ `C:\\Program Files\\Git\\bin\\bash.exe`. Resolver không còn dừng ở shim WindowsApps/WSL hỏng đứng trước PATH.

Kết luận tái kiểm tra: resolver executable không regression, nhưng tìm thấy một false-negative trong auth envelope: ánh xạ mù `GITHUB_PAT` cũ có thể che credential store vừa được `gh auth login` sửa. Bản vá thêm hai phản chứng: store phải được thử trước PAT legacy, và container không có store vẫn phải fallback sang PAT. Hai mục đỏ thực tế còn lại là nợ xác thực CLI, không phải nợ cài đặt. GitHub vẫn có connector hoạt động, nhưng bất biến “không một đường độc quyền” yêu cầu sửa cả `gh` thay vì dùng connector để che gate đỏ.

## Nguyên nhân gốc

1. Phạm vi “bắt buộc” chỉ phản ánh thứ launcher Python tự cần (`git`, `python`), không phản ánh năng lực môi trường điều phối.
2. Có binary và auth hợp lệ bị gộp làm một; `gh` hoàn toàn bị bỏ vì giả định connector/MCP luôn có.
3. Resolver tin ứng viên đầu PATH. Binary không chạy được che binary tốt phía sau.
4. Hook dùng shell-form với tên trần `bash`; trên Windows tên này có thể là WSL shim, không phải Git Bash.
5. Bootstrap dùng `command -v` như bằng chứng, không probe thực thi/auth.
6. Hướng dẫn Windows chỉ nêu `winget`, nhưng máy thực tế chỉ có Chocolatey.
7. Nhánh kill-tree Windows dùng PowerShell/WMI làm nguồn PID/creation time; WMI bị sandbox chặn dù tiến trình đích do launcher sinh ra.

## Thay đổi phòng ngừa

- `doctor` chụp môi trường trước resolve/probe; JSON chỉ ghi CÓ/KHÔNG và nguồn credential.
- Nhóm fail-closed: `git`, `python`, `claude`, `codex`, `gh`, `rg`, `bash`.
- Claude/Codex/GitHub có probe auth không tương tác, output được bỏ, chỉ giữ rc/lý do đã rút gọn.
- Mỗi probe có timeout và cả doctor có deadline tổng; hết hạn là đỏ.
- Resolver duyệt mọi mục PATH và fallback nền, tiếp tục sau `Access denied`.
- SessionStart chuyển sang exec-form gọi bridge Python; bridge đọc env trước, probe Bash rồi gọi Git Bash bằng đường dẫn thật.
- Khóa PID và ảnh cây Windows chuyển sang Win32 API trực tiếp (`GetProcessTimes` + Toolhelp32), không còn gọi PowerShell/WMI.
- Hook cài thêm `gh`; thử credential store trước rồi mới ánh xạ kín `GITHUB_PAT` sang `GH_TOKEN` cho đúng một probe fallback; không export PAT cũ để che store.
- Hướng dẫn `rg` Windows có cả Chocolatey và WinGet. Máy này đã cài `ripgrep 15.2.0` bằng Chocolatey; tên trần `rg` hiện chạy được.

## Bất biến phải giữ

1. **Env trước tool:** chụp biến môi trường trước mọi resolve/probe/spawn; không log giá trị credential.
2. **Bằng chứng dương:** path tồn tại không đủ; version phải rc=0 + output, auth phải rc=0 + output.
3. **Không một đường độc quyền:** connector GitHub không loại bỏ `gh`; ứng viên PATH đầu không loại bỏ ứng viên sau; WinGet không loại bỏ Chocolatey.
4. **Fail-closed có giới hạn:** thiếu/hỏng/hết auth hoặc timeout đều trả 12 tại preflight.
5. **Không shell-form cho path placeholder:** project hook dùng exec-form.

## Việc người dùng còn phải làm một lần

- Codex: chạy `codex login --device-auth`, rồi kiểm `codex login status`.
- GitHub: cấp lại token Environment hợp lệ hoặc chạy `gh auth login -h github.com`, rồi kiểm `gh auth status`.
- Sau đó chạy `python .claude/dev/launcher.py doctor --json`; chỉ nhận việc khi `ok=true`.

Launcher không thể và không được tự tạo credential thay người dùng. Thay đổi lần này bảo đảm trạng thái ấy bị chặn sớm, có chẩn đoán rõ và không còn bị báo xanh giả.
