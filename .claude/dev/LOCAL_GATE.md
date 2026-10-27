# Kiểm thử ngoài GitHub Actions — bản triển khai đầu tiên

Nguồn yêu cầu: chủ kho tắt Actions và giao thi công phương án cloud Linux + Windows local trong phiên ChatGPT.
Phạm vi: bộ chạy và bằng chứng. Không đổi workflow, ruleset, lease của #992, hay năm tệp dự kiến của #999.

## Linux

Dùng clone sạch và commit đã đóng băng. Chạy từ gốc kho, bằng chứng nằm ngoài clone:

```bash
head=$(git rev-parse HEAD)
python -B .claude/dev/local_gate.py run --root . --expected-head "$head" --out ../evidence-linux-001
python -B .claude/dev/local_gate.py verify --expected-head "$head" --out ../evidence-linux-001
```

Kế hoạch mặc định `local_gate_plan.json` chỉ gồm doctrine, bảng ADR và EOL. Đây là preflight rẻ,
không phải full CI hoặc điều kiện merge. Kế hoạch `local_gate_linux_suites.json` chạy thêm các suite
Linux nặng; nó cũng KHÔNG tuyên bố tương đương toàn workflow hoặc thay nghiệm thu Windows/release.

```bash
python -B .claude/dev/local_gate.py run --expected-head "$head" --plan .claude/dev/local_gate_linux_suites.json --out ../evidence-linux-suites-001
python -B .claude/dev/local_gate.py verify --expected-head "$head" --plan .claude/dev/local_gate_linux_suites.json --out ../evidence-linux-suites-001
```

Chọn phần cần đo bằng `--only doctrine,adr`. Phần không chạy giữ `not_run`; tổng kết trả khác 0
và `verify` từ chối hồ sơ thiếu phần. Không diễn giải kết quả chạy một phần thành toàn bộ đạt.
Sau gián đoạn, đọc biên nhận đã ghi sau từng bước; đo lại phần thiếu vào thư mục MỚI. Chưa có tự động
resume hoặc gộp hai lần chạy thành một bằng chứng đầy đủ.

Runner không cài dependency, tự push, gọi API hay đọc biến credential của phiên để truyền cho test.
Nó vẫn chạy với quyền của người gọi và HOME hiện tại: KHÔNG phải sandbox bảo mật. Chỉ chạy mã tin cậy.
Plan có quyền chạy lệnh; phải review plan như review script trước khi dùng. Khi verify, plan phải là
bản tin cậy của người kiểm, không lấy plan do người gửi tự thay thế. Băm kiểm toàn vẹn nội dung, không
chứng minh nguồn gốc, danh tính reviewer hoặc rằng người gửi không viết lại toàn bộ hồ sơ.

Trạng thái từng bước: `passed`, `failed`, `not_measured`, `not_run`, `running`.
`passed` đòi rc=0 và mọi marker dương trong plan; không có marker thì thất bại. Timeout là
`not_measured`. Phải đọc log để biết số ca và các ca bỏ qua bên trong suite; rc=0 không chứng minh
Windows hoặc rằng không có ca nội bộ bị bỏ qua. Biên nhận ghi hệ điều hành, Python, Git, SHA/tree,
lệnh, thời lượng và SHA-256 của từng log; không giả run/check ID của GitHub.

## Windows

Trên Windows thật có PowerShell 7.1+, dùng bộ chạy đã merge từ PR #602:

```powershell
git rev-parse HEAD
pwsh -NoProfile -File .claude/dev/chay-cong-windows.ps1 -Muc day-du -CaiCongCu -ChiTiet
git rev-parse HEAD
git status --short
```

Giữ nguyên nhật ký script báo ở cuối, SHA đầu/cuối và danh sách `KHÔNG CHẠY`/`THAY BẰNG`.
Đây chưa phải receipt cùng schema Linux. Không chạy script PowerShell trên Linux rồi gọi là kiểm Windows.

## Nghiệm thu và lưu bằng chứng

- Actions đã tắt ở cấp repository theo xác nhận của chủ kho. Không xoá YAML lịch sử để qua các test ghim workflow.
- Required checks Actions, cửa `accept`, admission, publish lease và điều kiện CI trong các packet hiện có
  KHÔNG tự đổi. Công cụ này không mở khoá merge hay nhả lease. #992 cần disposition riêng của chủ kho.
- Bước kế tiếp cần packet độc lập: mapping từng obligation cũ sang phép đo mới, verifier độc lập và cập nhật
  protocol/ruleset. Chưa bật status/check thay thế, chưa lấy quyền quản trị GitHub và chưa tự approve.
- Review độc lập vẫn bắt buộc. Local receipt không có giá trị cross-provider approval.
- Chỉ lưu receipt và log cuối cần tái kiểm. Kiểm secret và dữ liệu nhạy cảm trước khi commit/publish log;
  runner không tự công bố. Không xoá bằng chứng gốc của các lượt thất bại đã được dùng để ra quyết định.

Kiểm tra bản thân runner: `python -B .claude/dev/local_gate_checks.py`.
