verdict: changes_requested
reviewed_sha: 16e992a01c0a4ec8cfcc793dac9c1def5e288ae8
Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

Review độc lập hai trục **Spec** và **Standards/Security**, theo chỉ thị `run/eb133f86/prompt.snapshot`; ngưỡng approved là không còn P0–P3. Provider `openai_codex`, agent Codex dựa trên GPT-6, transport công cụ shell trực tiếp trong sandbox Linux; không dùng phiên/context Executor. Không có bằng chứng độc lập để xác nhận model/effort thực phục vụ hoặc tên execution surface của launcher. Chưa đăng kết quả lên GitHub.

HEAD khớp mốc yêu cầu; tree `da846f35658795cf61c910ea4524e36888e8d0b0`. Base `8cdb15a786304bab084b43c8b30c127ae87e2594`. Diff Git khớp byte với `diff.patch`: duy nhất `CLAUDE.md`, +7/−1. Cây `cay-kho/` sạch trước và sau kiểm tra; không sửa nội dung hoặc cấu hình kho.

### continue-thieu-pham-vi-loi [P2]

**Vị trí:** `cay-kho/CLAUDE.md:61–62`, câu “Dưới `ErrorActionPreference = 'Continue'`, điều kiện `if` ném lỗi thì nhánh bị BỎ QUA và script chạy tiếp”. Trục Spec: câu được viết như một quy tắc chung cho lỗi trong điều kiện, thiếu giới hạn về loại lỗi và ngữ cảnh xử lý lỗi.

**Bằng chứng:** PowerShell phân biệt *statement-terminating* (dừng câu lệnh) với *script-terminating* (dừng script và tháo call stack). `throw` thuộc loại thứ hai; `Continue` không bảo đảm chuyển sang câu tiếp theo cho mọi lỗi. Tài liệu chính thức còn nêu lỗi terminating có thể chuyển điều khiển vào `catch`/`trap`. Vì vậy chỉ riêng giá trị `Continue` chưa đủ làm điều kiện cho kết luận tổng quát trong bài học. Xem [Microsoft — about_Error_Handling, Types of errors](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling?view=powershell-7.6#types-of-errors) và [Microsoft — about_Throw](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_throw?view=powershell-7.6). Đây là đối chiếu đặc tả ngữ nghĩa, không phải kết quả chạy PowerShell của reviewer.

**Hệ quả:** phiên sau có thể dựa vào câu này để giả định lỗi trong điều kiện luôn chỉ bỏ qua nhánh rồi tiếp tục, trong khi điều kiện gọi hàm dùng `throw`, hoặc nằm trong `try`, cần cách xử lý khác. Finding không phủ nhận lời khai về riêng sự cố gọi phương thức trên `$null`.

**Đề xuất sửa:** sửa ngay câu bài học tại `CLAUDE.md:61–62`, giới hạn mô tả vào ca lỗi gọi phương thức trên `$null` đã được Executor đo, nêu ngữ cảnh ngoài `try/catch` nếu đúng với phép đo, và phân biệt dừng câu `if` với dừng toàn script. Tránh biến quan sát của ca đó thành quy tắc cho mọi lỗi. Không cần sửa script triển khai để xử lý finding về câu chữ này.

**Ca kiểm tra đề xuất — NOT_RUN:** trên PowerShell, so ba ca với `Continue`: điều kiện gọi phương thức trên `$null` ở ngoài `try`; điều kiện gọi hàm có `throw`; và ca phương thức trên `$null` được bọc trong `try/catch`. Ghi dấu nhánh, dấu câu sau `if`, dấu `catch`, loại lỗi và phiên bản. Dùng các ca này để xác định chính xác phạm vi câu mô tả; đột biến đưa câu trở lại quy tắc “mọi lỗi đều tiếp tục” phải không phù hợp với bảng kết quả. **KHÔNG ĐO ĐƯỢC** các ca này tại sandbox vì không có `pwsh`/`powershell`.

**Rủi ro khi sửa:** đừng thay bằng quy tắc “mọi lỗi terminating đều dừng cả script”, vì như vậy lại gộp hai lớp lỗi. Việc kiểm các ca trên phục vụ độ chính xác của tài liệu, không mở rộng write set sang mã sản phẩm.

## Đối chiếu các mệnh đề và quét lớp

- **Chốt trong deploy — xác nhận bằng mã:** `scripts/deploy-package.ps1:195` chứa `$txt = if (Test-Path $f) { [string](Get-Content $f -Raw -Encoding utf8) } else { '' }`; dòng 196 ngay sau là `if ($null -eq $txt) { $txt = '' }`; `[regex]::Match($txt, ...)` ở dòng 203. Đoạn sửa mô tả đúng sự tồn tại và vị trí chốt này. Script đặt `$ErrorActionPreference = 'Stop'` ở dòng 47; không đánh đồng cấu hình của nó với lời kể về script chờ khoá.
- **Quét toàn lớp `.ps1`:** rà cả tệp ẩn và đối chiếu danh sách Git, tổng cộng 15 tệp; đọc mọi dòng `Get-Content` để kiểm cả trường hợp khác bố trí đối số. Có đúng ba phép ép `[string](Get-Content ... -Raw ...)`, thuộc hai tệp. Ngoài deploy còn `scripts/nlm-credential-refresh.ps1:563` và `:965`.
  - Dòng 563 chuyển tiếp vào `ConvertFrom-Json`, có `catch` gán `$record = $null`; dòng 564 kiểm `$null` và loại đối tượng, trả trạng thái `alive/record_unreadable`. Đây là chốt từ chối dữ liệu không đọc được, không dựa vào phép ép để bảo đảm chuỗi.
  - Dòng 965 chuyển tiếp vào `ConvertFrom-Json`, **không có chốt `$null` ngay sau**. Dòng 966–969 ép các trường sang chuỗi rồi kiểm `notebook_id` và thư mục browser; cấu hình lỗi nằm trong `try` từ dòng 958, kết thúc bằng `catch` trả `inconclusive/preflight`, exit 4 tại dòng 1053–1055. Script đặt `Stop` ở dòng 24. Bài học mới có liên quan tới phép ép ở đây; không được coi bản thân phép ép là chốt xử lý dữ liệu rỗng. Chưa có bằng chứng rằng đường này vượt qua các bước xác thực hoặc gây lỗi an ninh; không ghi thêm finding từ giả định hành vi chưa chạy.
- **ADR và khoá:** `docs/adr/0057-windows-local-may-chu-kho.md` tồn tại; dòng 36–38 định nghĩa khoá tại `D:\tl-win\KHOA.txt`. Không có tệp `KHOA.txt` được theo dõi trong clone: đây là tệp trên máy Windows ngoài kho, không phải liên kết tới tệp nguồn bị mất. ADR-0058 tồn tại và sửa phạm vi/hạn khoá; đoạn bài học không đặt lại quy tắc khoá nên không mâu thuẫn với sửa đổi đó. ADR-0057:61 và ADR-0058:54 đều khai không có công cụ trong kho đọc khoá; không tìm thấy script chờ khoá được kể trong đoạn sửa.
- **Các kết quả Windows — KHÔNG ĐO ĐƯỢC:** sandbox Linux không tìm thấy `pwsh` hoặc `powershell`. Không xác nhận thực nghiệm các kết quả cho tệp 0 byte/BOM `EF BB BF`, phép ép biểu thức, biến có kiểu, nối chuỗi, thông báo lỗi regex/phương thức, hoặc nhánh `if`. Các phiên bản PS 5.1.26100/7.6.9, ngày đo và sự cố chờ khoảng bốn phút là lời khai chưa tái lập từ clone. Không dùng mô tả PR làm bằng chứng đã chạy; ba gate bên dưới cũng không đo những hành vi này.
- **Tính nhất quán và định dạng:** tìm trong toàn bộ `CLAUDE.md` và Markdown dưới `docs/` không thấy một hướng dẫn khác vẫn khuyên phép ép biểu thức này chữa `$null`. Mục ở dòng 54–64 vẫn có ba dấu `·`, mỗi dấu bắt đầu sau hai khoảng trắng; các dòng nối mới giữ cùng thụt lề, không có dòng trống cắt mục hay rào mã bị mở. `git diff --check` sạch. Không phát hiện hỏng định dạng hoặc thay đổi quyền, secret, workflow hay đường ghi dữ liệu trong diff.

Bằng chứng cục bộ: `review_evidence/static-audit.json` và `review_evidence/checks.json`; stdout/stderr/rc nguyên bản của từng gate nằm cùng thư mục.

## Đã chạy

Môi trường: Linux x86_64, Python 3.13.17; clone đầy đủ (`git rev-parse --is-shallow-repository` → `false`, rc 0), `core.abbrev=7` đã có sẵn (`git config --get core.abbrev` → `7`, rc 0).

Ba lệnh bắt buộc đều chạy với cwd `/tmp/claude-0/rv/pr1048-review-1/cay-kho`, biến môi trường `PYTHONDONTWRITEBYTECODE=1`, bằng driver `run_checks.py` ở sandbox. Cả ba stderr rỗng; không gate nào bị skipped/not_run.

1. `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` — **rc 0, passed**. Dòng stdout thật:

   ```text
   doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
   ```

2. `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py adr-song --root .` — **rc 0, passed**. Dòng stdout thật:

   ```text
   adr-song: sạch — 57 ADR trên đĩa, 57 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])
   ```

3. `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json` — **rc 0, passed**, `ok=true`. Các dòng trích nguyên từ JSON stdout:

   ```json
   "ok": true,
   "files_scanned": 117,
   "claims_flagged": 381,
   "flags": [],
   "advisory_count": 381,
   "layers_skipped": {},
   ```

   `381` là số advisory trong kết quả, không phải 381 lỗi cứng. Xem JSON đầy đủ tại `review_evidence/doc-claims-check.stdout`.

4. `git -C cay-kho rev-parse HEAD` — **rc 0**, `16e992a01c0a4ec8cfcc793dac9c1def5e288ae8`.
5. Trong `cay-kho/`: `git rev-parse HEAD^{tree}` — **rc 0**, `da846f35658795cf61c910ea4524e36888e8d0b0`.
6. Trong `cay-kho/`: `git diff --numstat 8cdb15a786304bab084b43c8b30c127ae87e2594 HEAD` — **rc 0**, `7\t1\tCLAUDE.md` (tab được biểu diễn bằng `\t`). Đối chiếu bằng Python với `diff.patch` cho `diff_patch_matches_git=True`, rc 0.
7. Trong `cay-kho/`: `rg -n -i --hidden --no-ignore -g '!**/.git/**' -g '*.ps1' 'Get-Content' .` — **rc 0**; đọc các vị trí, đối chiếu 15 tệp `.ps1` bằng Git/Python, xác định ba phép ép đã nêu.
8. Trong `cay-kho/`: `rg -n -i 'Get-Content|Value cannot be null|null-valued|Ép.*string|ép.*kiểu|BOM|KHOA\.txt|ErrorActionPreference|7\.6\.9|5\.1\.26100' CLAUDE.md docs/ -g '*.md'` — **rc 0**; kết quả liên quan nằm ở bài học mới, ADR-0057/0058 và các ví dụ đọc JSON trong prompt.
9. Trong `cay-kho/`: `git diff --check 8cdb15a786304bab084b43c8b30c127ae87e2594 HEAD` — **rc 0**, stdout rỗng.
10. Trong `cay-kho/`: `git status --porcelain=v1 --untracked-files=all` — **rc 0**, stdout rỗng sau các gate. Trước gate đã chạy `git status --short --untracked-files=all`, rc 0, stdout cũng rỗng.
11. Kiểm khả dụng bằng `shutil.which('pwsh')` và `shutil.which('powershell')` — driver Python **rc 0**, cả hai trả `None`. **Hành vi PowerShell: not_run / KHÔNG ĐO ĐƯỢC**, không tính là passed. Đã tra cứu tài liệu Microsoft qua công cụ web để đối chiếu ngữ nghĩa cho finding; công cụ web không cung cấp shell rc.
