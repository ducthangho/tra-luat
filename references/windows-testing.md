# Windows testing qua Desktop Commander

Test/build trên Windows qua Desktop Commander: đọc tệp này. Mặc định dùng tra-luat-win; ASUS dùng khi cần tương thích/UI. Luôn chọn deviceId, kiểm hostname/source SHA và tách vùng ghi mỗi run. Commander là transport, không thay Packet/lease hay release gate.

Khoá máy, sổ đo và thư mục phiên theo ADR-0057, ADR-0058, ADR-0059 (kho nguồn, dev-side): đọc các ADR ấy trước mỗi lượt; tệp này không chép lại luật của chúng. Mỗi máy dùng thư mục gốc `tl-win` của chính nó: `D:\tl-win` trên ASUS-LAPTOP, `C:\tl-win` trên tra-luat-win (không có ổ D).

Cập nhật thông tin đã xác minh ngày 2026-10-31 (Asia/Saigon). Kiểm tra trạng thái và phiên bản thực tế mỗi lượt; không coi trạng thái Online hay phiên bản bên dưới là cố định.

## Chọn máy

| Vai trò | Máy | Commander deviceId | Thư mục |
|---|---|---|---|
| Mặc định cho build/test Windows | tra-luat-win | f7281f27-f79f-40a2-a2f5-b454b58a166a | Snapshot: C:\work\tra-luat; vùng làm việc: C:\work\tra-luat-agent; khoá/sổ đo/thư mục phiên: C:\tl-win |
| Kiểm tra tương thích máy cá nhân/UI | ASUS-LAPTOP | 7404cfba-9034-4787-b46b-7c358126a411 | Canonical: D:\Quốc hội\tra-luat; vùng riêng: C:\Users\admin\tl-work; khoá/sổ đo/thư mục phiên: D:\tl-win |

Gọi list_devices và luôn truyền deviceId rõ ràng. Xác minh hostname, tài khoản, PowerShell, thư mục và source SHA trước lệnh ghi/test. Nếu hostname không khớp thì dừng. Máy offline không đồng nghĩa chưa cài Commander; không chạy lại installer/pairing khi chưa kiểm tra.

Commander trên VM chạy dưới TRA-LUAT-WIN\tlcommander, tài khoản thường. Scheduled Task TraLuatRemoteCommander tự khởi động và dùng pairing đã lưu; đã kiểm tra kết nối lại sau stop/start. Không cần ASUS online để điều khiển VM đang chạy. Không nâng Commander lên SYSTEM/admin hay bật SSH/WinRM để vượt lỗi quyền.

PowerShell kiểm tra lúc thiết lập: 7.6.9 Core.
- VM: C:\Program Files\PowerShell\7\pwsh.exe; Machine PATH đã cấu hình.
- ASUS: D:\Program Files\PowerShell\7\pwsh.exe; User PATH và Terminal profile đã kiểm tra.
Truyền shell tuyệt đối khi mở tiến trình nếu shell mặc định lỗi.

## Trình tự test

1. Đọc AGENTS.md, CONTEXT.md, protocol, CLAUDE.md và Packet/lease hiện hành của checkout sẽ sửa; tuân thủ vai trò, write set và exact SHA. Commander là transport, không tự cấp authority.
2. Chọn VM mặc định. Chỉ dùng ASUS khi cần kiểm tra môi trường cá nhân, GUI/Windows client hoặc so sánh lỗi.
3. Tạo checkout/worktree và thư mục kết quả riêng cho từng run trong vùng làm việc được phép. Không sửa canonical ASUS để thử nghiệm; không reset/clean/xóa thay đổi của phiên khác.
4. Xác minh cùng commit, fixture, cấu hình phạm vi và phiên bản dependency khi so sánh hai máy. C:\work\tra-luat trên VM ban đầu là SNAPSHOT v1.36.69 từ ef34d88838bc125727670f494b15213b6c6f0c8d, không phải Git clone; không git pull tại đó và không nhận snapshot là checkout hiện hành. Chuẩn bị source đúng SHA trước test thay đổi mới.
5. Dùng tool-inventory, route-task và --help hiện có trước khi viết helper. Chạy gate phù hợp Packet và phạm vi thay đổi; không coi ping thành build/regression.
6. Ưu tiên test local/read-only. Test ghi dùng dữ liệu test và profile đích đã xác minh, dry-run rồi apply/verify theo skill; không cho hai máy cùng sửa corpus/registry/NLM/LIVE. Hai máy chỉ chạy song song khi nguồn, output và vùng ghi độc lập.
7. Nếu start_process trả PID thì đọc output đến khi kết thúc. Nếu trả call_id thì dùng get_tool_result; không gọi lại thao tác đang pending.
8. Báo hostname/deviceId, source SHA, command, exit code thật, log và passed/failed/skipped/not_run. Khả năng thiếu dependency/auth phải ghi rõ, không tính pass. Không tự land, tăng VERSION, deploy hoặc công bố release.

## Preflight VM và ping chỉ đọc

Dùng shell C:\Program Files\PowerShell\7\pwsh.exe. Kiểm tra hostname = TRA-LUAT-WIN và tài khoản trước:
~~~powershell
hostname
whoami
$PSVersionTable.PSVersion
Get-Command pwsh
& 'C:\work\tra-luat\.venv\Scripts\python.exe' --version
git --version
~~~

Runtime config có sẵn ở C:\ProgramData\tra-luat\runtime.json, tài khoản tlcommander có quyền đọc. Truyền đường dẫn cho CLI, KHÔNG đọc/in nội dung hoặc sao chép secret:
~~~powershell
& 'C:\work\tra-luat\.venv\Scripts\python.exe' 'C:\work\tra-luat\scripts\tl.py' --config 'C:\ProgramData\tra-luat\runtime.json' ping
~~~
Chỉ lặp ping khi tác vụ cần truy cập backend. C:\Tools\tl.cmd là wrapper cùng config. Xác minh hợp đồng API trước mọi action khác.

Đã xác minh khi thiết lập: Commander, khởi động lại, pwsh, Python 3.12.10, import yaml/pypdf/cffi/docx và ping backend 2.21.2p. Chưa hoàn tất full selftest/build/regression. GitHub/Codex user auth trên VM chưa thiết lập; NLM/OCR/native PDF cần kiểm tra riêng. Không suy đăng nhập gcloud đồng nghĩa các công cụ khác đã đăng nhập.

## Vòng đời VM

Compute Engine, không phải Cloud Run Windows:
- Project: ubqlv-202307
- VM: tra-luat-win
- Zone: asia-southeast1-a
- Windows Server 2022; e2-standard-2 (2 vCPU, 8 GiB); boot disk 50 GiB pd-balanced.

Commander không bật được chính VM đang tắt. `gcloud` chỉ dùng cho vòng đời VM (describe/start/stop), không dùng làm đường vào máy nằm ngoài `list_devices` (ADR-0058). Dùng môi trường gcloud đã xác thực và luôn ghi project/zone; không thay config tài khoản toàn cục. ASUS có gcloud tại D:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd.
~~~powershell
& 'D:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd' compute instances describe tra-luat-win --project=ubqlv-202307 --zone=asia-southeast1-a --format='value(status)'
# Chỉ start/stop khi tác vụ đã cho phép thay đổi vòng đời VM:
# ... compute instances start tra-luat-win --project=ubqlv-202307 --zone=asia-southeast1-a
# ... compute instances stop tra-luat-win --project=ubqlv-202307 --zone=asia-southeast1-a
~~~
Ưu tiên stop/start bình thường; không hard reset để xử lý lỗi pairing. Sau start, chờ Commander online rồi kiểm hostname. Stop tiết kiệm compute/license nhưng disk/snapshot vẫn tính phí; không tự dừng khi phiên khác còn dùng.

## Bảo vệ dữ liệu

Allowlist công cụ tệp của Commander (`allowedDirectories`, đo bằng `get_config` ngày 2026-10-31): ASUS chỉ cho phép D:\Quốc hội\tra-luat, C:\Users\admin\tl-work và D:\tl-win; tra-luat-win để rỗng, tức không giới hạn, nên chỉ ghi trong C:\work\tra-luat-agent và C:\tl-win theo kỷ luật. Allowlist không chặn `start_process`; không vượt allowlist qua shell. Không ghi password/token, mã ghép nối, cookie, IP tạm hoặc nội dung runtime config vào skill, log hay báo cáo. Dùng credential đã lưu tại máy; chỉ yêu cầu login nếu công cụ thực sự báo thiếu/hết hạn.
