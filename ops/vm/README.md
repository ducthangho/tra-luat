# ops/vm — công cụ cho VM Windows `tra-luat-win`

`cap-nhat-cong-cu.ps1` cài/nâng cấp bộ công cụ dev trên VM, tương đương bộ mà môi trường cloud của
Claude/Codex có (hook `.claude/hooks/session-start.sh` + `ops/cong_cu.yaml`). Chi tiết thiết kế, an ninh
và mã thoát nằm ở đầu script; tệp này chỉ là cách dùng.

| Tầng | Chạy bằng | Lo phần |
|---|---|---|
| `NguoiDung` (mặc định) | `tlcommander` | claude, codex (npm vào `C:\Tools\npm`) · rg, shellcheck, actionlint (zip có kiểm sha256 vào `C:\Tools\bin`) · PyYAML/jsonschema theo ghim của `ops/cong_cu.yaml` · `requirements.txt` vào venv kho · nlm |
| `HeThong` | SYSTEM | Git, gh, Node LTS, PowerShell 7 trong `C:\Program Files` (installer chính thức, kiểm sha256) |

## Đăng ký lịch 2 tuần/lần (admin, một lần — và chạy lại mỗi khi script đổi)

Chạy **TRÊN VM `tra-luat-win`** (RDP vào VM — không phải laptop), trong PowerShell 7 **Run as administrator** bằng tài
khoản admin (vd `tladmin`). Sai máy thì script dừng mã 5 trước mọi thay đổi (`-MayDich`, mặc định `TRA-LUAT-WIN`). Clone vào TEMP riêng
của admin, KHÔNG chạy từ `C:\work`: `tlcommander` ghi được `C:\work`, nên script ở đó có thể đã bị sửa
ngay trước khi admin chạy nó.

```powershell
$d = Join-Path $env:TEMP "tl-dang-ky-$(Get-Random)"
git clone --depth 1 https://github.com/ducthangho/tra-luat $d
& "$d\ops\vm\cap-nhat-cong-cu.ps1" -DangKyLich
Remove-Item -Recurse -Force $d
```

`-DangKyLich` làm ba việc:
1. chép script + `cong_cu.yaml` + `requirements.txt` vào `C:\Program Files\tra-luat-ops` (chỉ admin ghi);
2. giao `C:\Tools\{npm,Python312,bin}` cho `tlcommander` (owner + Modify) — từ đây coi `C:\Tools` là vùng
   của tài khoản ấy, admin/SYSTEM không chạy công cụ từ đó;
3. đăng ký `TraLuat-CapNhatCongCu-HeThong` (SYSTEM, CN 02:30) và `TraLuat-CapNhatCongCu-NguoiDung`
   (`tlcommander`, S4U — không lưu mật khẩu, CN 03:30), 2 tuần/lần, `StartWhenAvailable` (VM tắt thì chạy
   bù khi bật). `tlcommander` được quyền đọc + chạy hai tác vụ, không sửa được.

## Chạy theo yêu cầu

- Qua Commander (tài khoản `tlcommander`): `Start-ScheduledTask -TaskName TraLuat-CapNhatCongCu-NguoiDung`
  (hoặc `-HeThong`), hoặc chạy thẳng tầng người dùng:
  `& 'C:\Program Files\PowerShell\7\pwsh.exe' -NoProfile -File 'C:\Program Files\tra-luat-ops\cap-nhat-cong-cu.ps1'`
- Chỉ đo, không cài: thêm `-ChiKiem`.
- Nhật ký JSON: tầng NguoiDung ở `C:\Tools\nhat-ky-cap-nhat\`, tầng HeThong ở `C:\ProgramData\tra-luat-cap-nhat\`.
  Đọc trường `ok` và `loi`, đừng tin mã thoát của Task Scheduler một mình.

## Test

`pwsh -NoProfile -File ops/vm/cap-nhat-cong-cu_test.ps1` (cần `python` có PyYAML, hoặc đặt
`$env:TL_TEST_PYTHON`). Không mạng, không cài gì. Chưa nối vào CI — xem mô tả PR.
