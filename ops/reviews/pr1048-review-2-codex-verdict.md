verdict: approved
reviewed_sha: 48b54d89b152871063c7296df33a60308667599e
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Review độc lập toàn bộ diff trên hai trục **Spec** và **Standards/Security**, theo `run/33584cff/prompt.snapshot`. Không phát hiện finding có bằng chứng còn mở. Không sửa `cay-kho/`.

Provider `openai_codex`; agent Codex dựa trên GPT-6 theo chỉ dẫn phiên; transport `machine`, thực hiện trực tiếp qua công cụ shell trong sandbox Linux. Không có biên nhận runtime để xác nhận model/effort từng request hoặc định danh surface của launcher; không tự suy là `codex_cli`. Đây là verdict review cục bộ, không phải authorization merge/land hay receipt assurance trên GitHub.

**Neo đã kiểm:** HEAD khớp SHA yêu cầu; tree `3c283128c5591ba2daaa8ec4830298d44587a042`; base `8cdb15a786304bab084b43c8b30c127ae87e2594` là ancestor của HEAD. Diff Git khớp byte với `diff.patch`: duy nhất `CLAUDE.md`, +10/−1. Diff từ SHA lượt trước cũng khớp byte với `diff-tu-luot-1.patch`. Chỉ thị trực tiếp của chủ kho là phạm vi review; không có đặc tả đóng băng để xác minh revision/generation/spec hash.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Slug lớp / nguồn | Trạng thái trên HEAD hiện tại | Bằng chứng và phạm vi kết luận |
|---|---|---|
| `continue-thieu-pham-vi-loi` [P2], `VERDICT-luot-1.md`, SHA `16e992a01c0a4ec8cfcc793dac9c1def5e288ae8` | **ĐÃ VÁ THẬT về lỗi diễn đạt** | Tự đối chiếu diff và `CLAUDE.md:61–64`: câu mới giới hạn ca tiếp tục vào `.Trim()` trên `$null`, trong điều kiện `if`, ngoài `try`, với `Continue`; tách `Stop`, ca bọc `try/catch`, và phản ví dụ `throw`. Không còn phát biểu rằng mọi lỗi trong `if` đều chỉ bỏ qua nhánh. |

Đối chiếu đủ ba ca, hai preference, hai phiên bản trong `ca_if_windows.txt`:

| Ca do Executor khai đã đo trên PS 5.1.26100 và 7.6.9 | `Continue` | `Stop` | Khớp câu mới |
|---|---|---|---|
| a: `.Trim()` trên `$null` trong điều kiện, ngoài `try` | `BAT_DAU, SAU_IF, KET_THUC`, rc 0 | chỉ `BAT_DAU`, rc 1 | Có, dòng 61–63 |
| b: điều kiện gọi hàm có `throw`, không bọc `try/catch` | chỉ `BAT_DAU`, rc 1 | chỉ `BAT_DAU`, rc 1 | Có, phản ví dụ dòng 64 |
| c: ca a bọc `try/catch` | `BAT_DAU, CATCH, SAU_TRY, KET_THUC`, rc 0 | cùng kết quả | Có, dòng 63 |

Câu mới trình bày các ca cụ thể với ngữ cảnh và phiên bản đo, không biến `Continue` thành bảo đảm chung cho mọi lỗi. Đối chiếu ngữ nghĩa độc lập: PowerShell phân biệt lỗi dừng câu lệnh với lỗi dừng script; `try/catch` xử lý được cả hai, và `throw` có thể được bắt. Vì vậy phản ví dụ `throw` ở đây được xét trong ca b ngoài `try/catch`, không được đọc thành quy tắc rằng `throw` đã bị bắt cũng dừng toàn script. Xem [Microsoft — about_Error_Handling](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling?view=powershell-7.6#types-of-errors) và [Microsoft — about_Throw](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_throw?view=powershell-7.6).

**Giới hạn:** bảng trên là đối chiếu câu chữ với lời khai Executor, không phải reviewer đã chạy 12 ca. **KHÔNG ĐO ĐƯỢC** hành vi PowerShell trong sandbox này. Việc đóng finding về phát biểu quá rộng dựa trên văn bản hiện tại, diff tự kiểm và tài liệu ngữ nghĩa; không nâng lời khai Windows thành kết quả thực nghiệm độc lập.

## Đối chiếu toàn bộ đoạn sửa

- **Chốt trong deploy — kiểm được bằng mã.** `scripts/deploy-package.ps1:195` chứa `$txt = if (Test-Path $f) { [string](Get-Content $f -Raw -Encoding utf8) } else { '' }`; ngay dòng 196 là `if ($null -eq $txt) { $txt = '' }`, trước `[regex]::Match($txt, ...)` ở dòng 203. Mô tả về sự tồn tại, thứ tự và tác dụng chuẩn hoá `$null` của chốt là đúng. Phạm vi “an toàn” ở đây là đường xử lý output rỗng này; script dùng `$ErrorActionPreference = 'Stop'` ở dòng 47.
- **Quét lớp `.ps1` — đủ 15/15 tệp.** Danh sách Git khớp danh sách trên đĩa, có cả tệp ẩn. Rà mọi lần `Get-Content`, không chỉ một thứ tự đối số, rồi tìm điểm mở phép ép có hỗ trợ xuống dòng. Có đúng ba mẫu `[string](Get-Content … -Raw …)` trong hai tệp:
  - `scripts/deploy-package.ps1:195`: chốt `$null` ngay sau như trên.
  - `scripts/nlm-credential-refresh.ps1:563`: đưa vào `ConvertFrom-Json`; `catch` gán `$record = $null`, dòng 564 kiểm `$null` và kiểu đối tượng, trả `alive/record_unreadable` khi không đọc được record.
  - **`scripts/nlm-credential-refresh.ps1:965` không có chốt `$null` ngay sau.** Phép ép được đưa tiếp vào `ConvertFrom-Json`; dòng 966–969 lấy trường có kiểu chuỗi rồi kiểm notebook ID và thư mục browser. Toàn đường nằm trong `try` từ dòng 958; `catch` ở dòng 1053–1055 trả `inconclusive/preflight`, exit 4; preference `Stop` được đặt ở dòng 25. Bài học mới có hệ quả với cách hiểu phép ép ở dòng 965: không được coi nó là bảo đảm chuỗi rỗng. Chưa có bằng chứng đường này bỏ qua xác thực hoặc gây lỗ an ninh; không tạo finding chỉ từ sự vắng mặt của chốt trực tiếp.
- **Các khẳng định hành vi — KHÔNG ĐO ĐƯỢC.** Không có `pwsh`/`powershell`. Reviewer không tái lập được: tệp 0 byte hoặc chỉ BOM `EF BB BF` trả `$null`; lỗi của `[regex]::Match`, `.Trim()` và `.StartsWith()`; kết quả phép ép biểu thức, biến có kiểu và nối chuỗi; rc/luồng điều khiển của các ca `if`. Comment tại `deploy-package.ps1:194` có nhắc ca tệp rỗng/regex, nhưng comment không thay phép đo. Phiên bản, ngày đo và kết quả chuỗi là lời khai của Executor được nêu trong chỉ thị; `ca_if_windows.txt` chỉ bổ sung bảng lời khai cho các ca `if`. Ba gate Python không chứng minh các hành vi này.
- **ADR và tệp khoá — phân biệt nguồn trong kho với tệp ngoài máy.** `docs/adr/0057-windows-local-may-chu-kho.md` tồn tại; dòng 36–38 định nghĩa `D:\tl-win\KHOA.txt`. Không có `KHOA.txt` được Git theo dõi trong clone. Đây là tệp vận hành trên Windows, không phải tệp nguồn bị thiếu. `docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md` cũng tồn tại, sửa phạm vi máy và hạn khoá; bài học không đặt lại các quy tắc ấy. Không xác minh được sự cố chờ khoảng bốn phút hay byte của khoá từ clone. Những lần nhắc `KHOA.txt` trong mã nguồn/tài liệu hiện tại không cung cấp script chờ và log tái lập sự cố này; ADR-0057:61 và ADR-0058:54 đều khai chưa có công cụ trong kho đọc khoá. Lời kể về script của phiên bên ngoài không mâu thuẫn với điều đó.
- **Tính nhất quán và định dạng.** Tìm toàn bộ `CLAUDE.md` và Markdown trong `docs/` theo `Get-Content`, `$null`, `[string]`, BOM, lỗi và preference: không thấy chỉ dẫn khác còn khuyên phép ép biểu thức chữa ca đọc tệp rỗng. Mục `CLAUDE.md:54–67` giữ đúng ba dấu `·`, cùng thụt hai khoảng trắng; các dòng nối giữ thụt lề, không thêm dòng trống hoặc hàng rào mã làm cắt mục. `git diff --check` sạch. Diff chỉ đổi văn xuôi; không phát hiện thay đổi authority, quyền, credential, workflow hoặc đường ghi dữ liệu.

Bằng chứng tự chạy ở `review_evidence/static-audit.json`, `review_evidence/checks.json` và stdout/stderr/rc riêng từng gate. Snapshot nội dung, mode, HEAD/tree, index, diff, tracked/untracked/ignored trước và sau gate khớp nhau: **8.468 tệp**, status rỗng. Đây là bằng chứng không có delta tại các mốc quan sát; không phải chứng minh lịch sử mọi thao tác ghi. Sandbox nền cho phép ghi workspace; reviewer giữ checkout read-only bằng cách chỉ đọc và đặt mọi output ngoài `cay-kho/`.

## Đã chạy

Môi trường: Linux x86_64, Python 3.13.17; clone không shallow; `core.abbrev=7` có sẵn. Ba lệnh bắt buộc chạy tại `/tmp/claude-0/rv/pr1048-review-2/cay-kho`, có `PYTHONDONTWRITEBYTECODE=1`. Cả ba stderr rỗng, không gate nào skipped/not_run.

1. `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` — **rc 0, passed**. Stdout thật:

   ```text
   doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
   ```

2. `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py adr-song --root .` — **rc 0, passed**. Stdout thật:

   ```text
   adr-song: sạch — 57 ADR trên đĩa, 57 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])
   ```

3. `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json` — **rc 0, passed**, `ok=true`. Các dòng trích nguyên từ stdout JSON:

   ```json
   "ok": true,
   "files_scanned": 117,
   "claims_flagged": 381,
   "flags": [],
   "advisory_count": 381,
   "layers_skipped": {},
   ```

   `381` là advisory, không phải lỗi cứng. JSON đầy đủ tại `review_evidence/doc-claims-check.stdout`.

4. `git -C cay-kho rev-parse HEAD` — **rc 0**: `48b54d89b152871063c7296df33a60308667599e`; `git -C cay-kho rev-parse HEAD^{tree}` — **rc 0**: `3c283128c5591ba2daaa8ec4830298d44587a042`.
5. Trong `cay-kho/`: `git merge-base --is-ancestor 8cdb15a786304bab084b43c8b30c127ae87e2594 HEAD` — **rc 0**, stdout rỗng; `git diff --numstat 8cdb15a786304bab084b43c8b30c127ae87e2594 HEAD` — **rc 0**: `10\t1\tCLAUDE.md` (tab biểu diễn bằng `\t`).
6. Trong `cay-kho/`: `git diff 8cdb15a786304bab084b43c8b30c127ae87e2594 HEAD` và `git diff 16e992a01c0a4ec8cfcc793dac9c1def5e288ae8 HEAD` — **cả hai rc 0**. Driver Python đối chiếu byte với hai tệp patch: đều `true`.
7. Trong `cay-kho/`: `git diff --check 8cdb15a786304bab084b43c8b30c127ae87e2594 HEAD` — **rc 0**, stdout rỗng.
8. Trong `cay-kho/`: `git ls-files -z -- '*.ps1'` — **rc 0**, 15 tệp; `rg -n -i --hidden --no-ignore -g '!**/.git/**' -g '*.ps1' 'Get-Content' .` — **rc 0**. Đọc các vị trí và chốt liên quan; lưu `review_evidence/powershell-get-content.stdout`.
9. Trong `cay-kho/`: `rg -n -i 'Get-Content|Value cannot be null|null-valued|Ép.*string|ép.*kiểu|BOM|KHOA\.txt|ErrorActionPreference|7\.6\.9|5\.1\.26100' CLAUDE.md docs/ -g '*.md'` — **rc 0**; `rg -l --hidden -g '!**/.git/**' 'KHOA\.txt' .` — **rc 0**; `git ls-files -- '*KHOA.txt'` — **rc 0**, stdout rỗng.
10. Trong `cay-kho/`: `git rev-parse --is-shallow-repository` — **rc 0**, `false`; `git config --get core.abbrev` — **rc 0**, `7`; `git status --porcelain=v1 --untracked-files=all --ignored` — **rc 0**, stdout rỗng trước/sau gate và lúc kiểm lại.
11. Tại sandbox: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/run_checks.py` và `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/static_audit.py` — **cả hai rc 0**. Driver xác nhận `shutil.which('pwsh')` và `shutil.which('powershell')` đều `None`. **PowerShell: not_run / KHÔNG ĐO ĐƯỢC**, không tính là passed.
12. Đã mở tài liệu Microsoft bằng công cụ web để đối chiếu ngữ nghĩa; công cụ web không có shell rc. Không dùng tra cứu này thay kết quả đo Windows.
