# Postmortem — launcher, Codex, GitHub và toolchain Windows ngày 15-08-2026

- **Trạng thái:** mã phòng ngừa đã triển khai trên nhánh; `rg` local đã phục hồi; còn chờ người dùng cấp lại Codex/GitHub credential.
- **Phạm vi:** launcher/doctor, Claude Code SessionStart, Codex CLI, GitHub CLI, `rg`, Bash.
- **Không chứa bí mật:** chỉ ghi sự hiện diện/nguồn và mã kết quả; không ghi giá trị token.

## Điều đã xảy ra

Các phép đo trực tiếp ngày 15-08-2026 cho thấy:

| Thành phần | Bằng chứng | Kết luận |
|---|---|---|
| Claude | `claude --version` và `claude auth status` thoát 0 | dùng được |
| Codex | `codex --version` xanh; `codex login status` trả `Not logged in`/rc khác 0 | có binary nhưng không gọi phiên được |
| GitHub | `gh --version` xanh; `gh auth status` báo credential mặc định không hợp lệ | có binary nhưng không gọi GitHub được |
| biến GitHub | `GITHUB_PAT` có; `GH_TOKEN`/`GITHUB_TOKEN` không có; ánh xạ PAT sang `GH_TOKEN` vẫn auth đỏ | credential hiện có đã sai/hết hạn, không chỉ sai tên biến |
| ripgrep | tên `rg` trỏ vào `...WindowsApps\OpenAI.Codex...\rg.exe`, CreateProcess trả WinError 5 | có path nhưng không thực thi được |
| Bash | tên `bash` trỏ vào `C:\Windows\System32\bash.exe`, trả `E_ACCESSDENIED`; Git Bash tốt có ở Program Files | shell-form chọn nhầm shim |
| khóa tiến trình | `Get-CimInstance Win32_Process` trả `CimException: Access denied` trong sandbox | deadline/stop không lấy được khóa PID, trả sai 10/125 |
| doctor cũ | báo `rg`/`bash` HỎNG nhưng vẫn in `ĐỦ CÔNG CỤ BẮT BUỘC`; không đo `gh`/auth | fail-open |
| cài `rg` | lệnh gợi ý `winget` thất bại vì máy không có `winget`; `choco install ripgrep` thành công | chỉ ghi một package manager là hướng dẫn không đủ |

`doctor` cũ còn probe tuần tự với timeout riêng cho từng lệnh. Một shim chậm có thể làm lệnh trông như treo hàng chục giây dù cuối cùng có output.

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
- Hook cài thêm `gh`, ánh xạ kín `GITHUB_PAT` sang `GH_TOKEN`, và probe auth cuối phiên.
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
