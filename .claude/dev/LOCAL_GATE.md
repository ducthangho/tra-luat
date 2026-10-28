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

Kế hoạch mặc định `local_gate_plan.json` gồm self-check của runner, doctrine, bảng ADR và EOL. Đây là preflight rẻ,
không phải full CI hoặc điều kiện merge. Kế hoạch `local_gate_linux_suites.json` chạy thêm các suite
Linux nặng, bắt đầu bằng probe bản kê công cụ và Ruff 0.15.15; nó cũng KHÔNG tuyên bố tương đương toàn workflow hoặc thay nghiệm thu Windows/release.

```bash
python -B .claude/dev/local_gate.py run --expected-head "$head" --plan .claude/dev/local_gate_linux_suites.json --out ../evidence-linux-suites-001
python -B .claude/dev/local_gate.py verify --expected-head "$head" --plan .claude/dev/local_gate_linux_suites.json --out ../evidence-linux-suites-001
```

Chọn phần cần đo bằng `--only doctrine,adr`. Phần không chạy giữ `not_run`; tổng kết trả khác 0
và `verify` từ chối hồ sơ thiếu phần. Không diễn giải kết quả chạy một phần thành toàn bộ đạt.
Sau gián đoạn, đọc biên nhận đã ghi sau từng bước; đo lại phần thiếu vào thư mục MỚI. Chưa có tự động
resume hoặc gộp hai lần chạy thành một bằng chứng đầy đủ.

Checkout phải sạch cả tracked, untracked và ignored. Đặt virtualenv, cache và công cụ ngoài checkout.
Mọi phép Git của runner bỏ các biến `GIT_*` do caller đặt và dùng `--no-optional-locks`.
Runner hỗ trợ linked worktree, nhưng bộ packet-loop có ca bắt buộc standalone clone; dùng clone độc lập để chạy các suite.

Mỗi bước có TMPDIR/TEMP/TMP riêng ngoài checkout và RUFF_CACHE_DIR ngoài checkout.
Plan chỉ được đặt tuning `env.CI_DANG_KY_WORKERS` trong miền chuỗi `1..8`; không kế thừa tuning từ caller.
Plan suite ghim hai worker cho registry; vẫn có thể tốn nhiều thời gian và không tự chia shard.
Không truyền `GIT_CONFIG_*` vào test: nó đè cả cấu hình repo fixture. Nếu cần ghim Git cho
checkout chạy trực tiếp, cấu hình repo-local trước khi chạy; không sửa global của người dùng.
Riêng runtime-selftest chạy qua `_scratch_run` trong clone tạm độc lập ở TMPDIR ngoài checkout,
đúng HEAD/tree nguồn, với core.abbrev=7/autocrlf=false/eol=lf đặt repo-local trong bản sao.
Fixture con vẫn đổi được config riêng. Log ghi HEAD/tree của clone; sau lệnh, HEAD/tree và tracked/
untracked phải giữ nguyên. Chỉ ignored fixture/state được phép đổi trong bản sao và bị dọn khi xong.
Receipt ghi execution_scope=scratch_clone; checkout_unchanged vẫn chỉ checkout nguồn đã giao.
Đây không phải cơ chế resume/gộp bằng chứng; selftest trên bản sao không chứng minh Windows.
Dependency phải cài trước bằng công thức của `ops/cong_cu.yaml`; probe thất bại không phải pass.

Runner không cài dependency, tự push, gọi API hay đọc biến credential của phiên để truyền cho test.
Nó vẫn chạy với quyền của người gọi và HOME hiện tại: KHÔNG phải sandbox bảo mật. Chỉ chạy mã tin cậy.
Plan có quyền chạy lệnh; phải review plan như review script trước khi dùng. Khi verify, plan phải là
bản tin cậy của người kiểm, không lấy plan do người gửi tự thay thế. Băm kiểm toàn vẹn nội dung, không
chứng minh nguồn gốc, danh tính reviewer hoặc rằng người gửi không viết lại toàn bộ hồ sơ.

Mỗi bước chạy qua supervisor Linux riêng bật `PR_SET_CHILD_SUBREAPER`. Supervisor nhận nuôi
hậu duệ mồ côi kể cả khi chúng tách session; sau khi lệnh kết thúc hoặc timeout, nó dọn và reap
con tới khi kernel trả ECHILD. Receipt ghi `containment=linux_subreaper` và `cleanup_complete`.
Không bật được subreaper, thiếu status của supervisor hoặc không dọn xong trong 5 giây là
`not_measured`; dừng plan, giữ các bước còn lại `not_run`. Đây là quản lý vòng đời cho mã tin cậy,
không phải sandbox hay giới hạn quyền của test. Test cố ý đổi cơ chế process/namespace ngoài hợp đồng này.
SIGINT/SIGTERM/SIGHUP cho runner được chuyển tới supervisor, dọn con và ghi receipt kết thúc.
SIGKILL hoặc host chết không chạy được handler: receipt có thể còn `running`, tuyệt đối không coi là pass.
Không tự resume hoặc gộp receipt dở dang. Nếu cleanup không xác nhận được, kiểm tra host trước khi chạy lại.

Trạng thái từng bước: `passed`, `failed`, `not_measured`, `not_run`, `running`.
`passed` đòi rc=0 và mọi marker dương trong plan; không có marker thì thất bại. Timeout là
`not_measured`. Phải đọc log để biết số ca và các ca bỏ qua bên trong suite; rc=0 không chứng minh
Windows hoặc rằng không có ca nội bộ bị bỏ qua. Biên nhận ghi hệ điều hành, Python, Git, SHA/tree,
lệnh, tuning đã ghim, thời lượng và SHA-256 của từng log; không giả run/check ID của GitHub.

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

Verifier từ chối artifact symlink, flag approval/full-CI khác false, boolean giả dạng chuỗi,
OID tree sai định dạng, marker đã lưu sai và cleanup chưa xác nhận. Nó tái đọc marker từ log.
Tree OID chỉ được kiểm định dạng khi verify offline; không xác minh lại object graph hoặc nguồn gốc receipt.
Receipt được ghi bằng tệp tạm duy nhất, fsync rồi replace; không hứa chứng minh chưa từng sửa rồi hoàn nguyên
checkout trong suốt run. Snapshot chỉ phản ánh trạng thái quan sát được ở các mốc.

Kiểm tra bản thân runner: `python -B .claude/dev/local_gate_checks.py`.
