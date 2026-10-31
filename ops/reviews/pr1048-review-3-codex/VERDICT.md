verdict: approved
reviewed_sha: 6f23a4e68805b4af3e2efe77be6e10b513843e93
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Review độc lập lại toàn bộ `diff.patch` trên hai trục **Spec** và **Standards/Security**, theo `run/ba975358/prompt.snapshot`. Ngưỡng áp dụng: chỉ approved khi không còn P0–P3. Không phát hiện finding có bằng chứng còn mở. Không sửa `cay-kho/`.

Provider `openai_codex`; agent Codex dựa trên GPT-6 theo chỉ dẫn phiên; transport `machine`, dùng công cụ shell trực tiếp trong sandbox Linux. Model/effort thực phục vụ từng request, session identity và tên execution surface chuẩn của launcher: **KHÔNG ĐO ĐƯỢC** từ bằng chứng được giao; không suy là `codex_cli` từ tên công cụ. Executor được chỉ thị khai là Claude. Verdict này là kết quả review nội dung cục bộ, không tự tạo receipt `cross_approved`, quyền merge/land hoặc xác nhận CI của GitHub.

## Neo và nguồn các thay đổi sau lượt 2

- HEAD thực tế: `6f23a4e68805b4af3e2efe77be6e10b513843e93`; tree: `fd454a6a3121fead24d812b32de40c89f0a02e34`. Checkout detached, status rỗng, clone đầy đủ, `core.abbrev=7` có sẵn.
- Base đã dùng đúng chỉ thị: `5a174b958a05e13f5c9a968a2596ca37267d0466`. `git diff BASE HEAD` khớp **từng byte** với `diff.patch`, SHA-256 `d36258b796d077d0227235e64d144e071ac12b3200934d4abbcc6e5cc23f6693`; duy nhất `CLAUDE.md`, **+10/−1**.
- `git diff 48b54d89b152871063c7296df33a60308667599e HEAD -- CLAUDE.md` rỗng. Đối chiếu thêm blob với tệp trên đĩa: toàn bộ `CLAUDE.md` giống lượt 2.
- Có **311 path** thay đổi giữa SHA lượt 2 và HEAD. Đối chiếu toàn bộ `git ls-tree -r -z` của ba SHA, gồm mode/type/object ID và trường hợp path vắng mặt: **311/311 path có trạng thái cuối khớp master `5a174b9…`**, không có path nào khác master. So HEAD với master trên toàn cây, ngoài `CLAUDE.md` có **0 khác biệt**. Không phát hiện thay đổi riêng của Executor ngoài `CLAUDE.md`.
- Merge-base của lượt 2 với master mới là `8cdb15a786304bab084b43c8b30c127ae87e2594`. Diff từ merge-base này tới `5a174b9…`, giới hạn `CLAUDE.md`, `docs/` và mọi `*.ps1`, **rỗng**. Diff cùng phạm vi từ lượt 2 tới HEAD cũng rỗng: master mới không thêm/sửa PowerShell, ADR, tài liệu trong `docs/` hay mục bài học đang xét.
- Kiểm object merge `b653574b117fa1496fbf58f09a22a8cbed5cc5dc`: cha thứ hai đúng là HEAD được review.

**Đính chính dữ kiện đầu vào:** `5a174b9…` là **cha thứ hai**, không phải cha thứ nhất của `6f23a4e…`; cha thứ nhất là `48b54d89b152871063c7296df33a60308667599e`. Đây là sai thứ tự cha trong prompt, không phải finding của thay đổi `CLAUDE.md`; không làm đổi base/diff/phạm vi review. Không có đặc tả đóng băng để xác minh revision/generation/spec hash; chỉ thị trực tiếp của chủ kho là authority cho lượt rà này.

## Spec — đối chiếu mọi mệnh đề mới

| Mệnh đề trong `CLAUDE.md` | Bằng chứng và giới hạn trên cây được review |
|---|---|
| Dòng 56: tệp 0 byte hoặc chỉ BOM `EF BB BF` cho `$null` khi đọc `-Raw` | **KHÔNG ĐO ĐƯỢC** hành vi PowerShell. Comment `scripts/deploy-package.ps1:194` nhắc ca rỗng/regex nhưng không thay phép đo; không có fixture/log độc lập cho cả hai loại tệp trong bộ chứng cứ giao này. |
| Dòng 56–58: lỗi của `[regex]::Match`, `.Trim()` và `.StartsWith()` trên `$null` | **KHÔNG ĐO ĐƯỢC** thông báo và hành vi lỗi. Kho có các lời gọi tương ứng, không có kết quả chạy của reviewer để khẳng định thông báo. |
| Dòng 58–60: phép ép biểu thức vẫn `$null`, biến có kiểu hoặc nối chuỗi cho `""`; ngày đo và hai phiên bản PS | **KHÔNG ĐO ĐƯỢC**. Đây là lời khai đo Windows của Executor. Không suy kết quả phép ép từ cú pháp hoặc từ các gate Python. |
| Dòng 60–61: deploy có chốt `$null` ngay sau phép ép | **Kiểm được bằng mã.** `scripts/deploy-package.ps1:195` gán `$txt` qua `[string](Get-Content $f -Raw -Encoding utf8)`; dòng 196 là `if ($null -eq $txt) { $txt = '' }`; dòng 203 mới gọi `[regex]::Match($txt, ...)`. Chốt có thật, đúng vị trí. “An toàn” ở đây được xét trong phạm vi xử lý output rỗng này, không phải bảo đảm mọi lỗi của script. Script đặt `Stop` ở dòng 47. |
| Dòng 61–64: ca `.Trim()` ngoài `try` dưới `Continue`/`Stop`, ca bọc `try`, phản ví dụ `throw` | **Kiểm được phạm vi câu chữ và sự khớp lời khai** trong `ca_if_windows.txt`; **KHÔNG ĐO ĐƯỢC** rc/luồng điều khiển trên PowerShell. Bảng đối chiếu cụ thể ở mục lượt trước bên dưới. |
| Dòng 65: tham chiếu `KHOA.txt` và ADR-0057 | **Kiểm được tham chiếu.** `docs/adr/0057-windows-local-may-chu-kho.md:36–37` định nghĩa `D:\tl-win\KHOA.txt`. `git ls-files -- '*KHOA.txt'` rỗng: đây là tệp vận hành ngoài clone, không phải nguồn bị thiếu. ADR-0058:7–8 sửa phạm vi máy và khoá của ADR-0057; bài học không đặt lại luật hạn khoá/phạm vi nên không mâu thuẫn. |
| Dòng 65: sự cố chờ khoảng bốn phút với khoá chỉ còn BOM | **KHÔNG ĐO ĐƯỢC** từ clone và lời khai được giao. Không có script/log tái lập sự cố đó trong bộ chứng cứ. ADR-0057:61–64 và ADR-0058:54–56 khai chưa có công cụ trong kho thực thi quy ước khoá; lời kể về script của một phiên ngoài kho không tự mâu thuẫn với các khai báo này. |

Các kết luận thực nghiệm chưa đo được ở trên không được ghi là passed. Không có `pwsh` hay `powershell` trong PATH; không dùng kết quả Linux/Python hoặc lời khai Executor để thay phép đo Windows.

## Standards/Security — quét lớp và tính nhất quán

Đối chiếu danh sách `.ps1` từ Git với toàn bộ tệp trên đĩa, gồm tệp ẩn và phần mở rộng không phân biệt hoa thường: **15/15 tệp**, hai danh sách khớp. Đọc **77 dòng có `Get-Content`**, rà các điểm mở phép ép có thể xuống dòng và các ngữ cảnh xử lý tiếp theo; không giới hạn tìm kiếm ở một thứ tự đối số `-Raw`. Có đúng ba mẫu `[string](Get-Content … -Raw …)` trong hai tệp:

| Vị trí | Chốt và ngữ cảnh được kiểm bằng mã |
|---|---|
| `scripts/deploy-package.ps1:195` | Dòng 196 chuẩn hoá `$txt` nếu `$null`, trước regex và xử lý chuỗi. Khớp bài học mới. |
| `scripts/nlm-credential-refresh.ps1:563` | Kết quả đi vào `ConvertFrom-Json`; `catch` đặt `$record = $null`, dòng 564 kiểm `$null` và kiểu đối tượng rồi trả `alive/record_unreadable`. Không dựa riêng vào phép ép để chấp nhận record. |
| `scripts/nlm-credential-refresh.ps1:965` | **Không có chốt `$null` trực tiếp ngay sau phép ép.** Kết quả đi vào `ConvertFrom-Json`; dòng 966–969 chuyển trường sang chuỗi và kiểm notebook ID/thư mục browser. Nằm trong `try` từ dòng 958; `catch` dòng 1053–1055 trả `inconclusive/preflight`, exit 4; preference `Stop` đặt ở dòng 25. Đây là biểu hiện cùng lớp cần nêu, nhưng chưa có bằng chứng vượt xác thực hoặc lỗi an ninh do nó. Không tạo finding chỉ từ việc thiếu chốt trực tiếp, cũng không coi phép ép là bảo đảm chuỗi rỗng. |

Tìm lại trong toàn bộ `CLAUDE.md` và Markdown dưới `docs/` theo `Get-Content`, `$null`, `[string]`, BOM, thông báo lỗi, preference và `KHOA.txt`: không thấy chỉ dẫn khác còn khuyên phép ép biểu thức này để chữa ca đọc tệp rỗng. Các ví dụ đọc VERSION/JSON không khẳng định phép ép chữa `$null`. Master mới không đổi bất kỳ tệp nào trong phạm vi tài liệu/PowerShell này.

Mục `CLAUDE.md:54–67` giữ **ba dấu `·`**, tại dòng 55, 56 và 66; mỗi dấu và mọi dòng nối thụt hai khoảng trắng, không có dòng trắng/rào mã cắt mục. Hai bẫy còn lại giữ nguyên. `git diff --check` rc 0, stdout rỗng. Diff chỉ đổi văn xuôi, không sửa quyền, authority, credential, workflow, gate hay đường ghi dữ liệu.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Slug / nguồn | Kết quả trên `6f23a4e…` | Bằng chứng kiểm độc lập |
|---|---|---|
| `continue-thieu-pham-vi-loi` [P2], lượt 1, SHA `16e992a01c0a4ec8cfcc793dac9c1def5e288ae8` | **ĐÃ VÁ THẬT về lỗi diễn đạt; vẫn đóng** | Tự đọc `CLAUDE.md:61–64`: câu đã giới hạn vào `.Trim()` trên `$null`, trong điều kiện `if`, ngoài `try`, dưới `Continue`; tách `Stop`, ca bọc `try/catch` và phản ví dụ `throw`. Không còn mệnh đề “mọi lỗi trong `if` đều tiếp tục”. Toàn bộ tệp khớp byte với SHA lượt 2. |
| Lượt 2, `VERDICT-luot-2.md`, SHA `48b54d89b152871063c7296df33a60308667599e` | Không có finding còn mở để vá | Lượt này tự kiểm lại toàn diff, nguồn 311 path từ master, quét lớp `.ps1`, tài liệu và ba gate trên đúng HEAD mới; không chỉ kế thừa verdict approved cũ. |

Đối chiếu câu chữ với **lời khai** trong `ca_if_windows.txt` (Executor khai hai bản PS 5.1.26100 và 7.6.9 cho cùng kết quả):

| Ca | `Continue` theo lời khai | `Stop` theo lời khai | Khớp câu sửa |
|---|---|---|---|
| a: `.Trim()` trên `$null` trong điều kiện, ngoài `try` | `BAT_DAU, SAU_IF, KET_THUC`, rc 0 | Chỉ `BAT_DAU`, rc 1 | Có, dòng 61–63 |
| b: điều kiện gọi hàm có `throw`, không bọc `try/catch` | Chỉ `BAT_DAU`, rc 1 | Chỉ `BAT_DAU`, rc 1 | Có, dòng 64, xét trong ca b này |
| c: ca a bọc `try/catch` | `BAT_DAU, CATCH, SAU_TRY, KET_THUC`, rc 0 | Cùng kết quả | Có, dòng 63 |

Phạm vi đóng finding là việc sửa phát biểu quá rộng. **Reviewer KHÔNG ĐO ĐƯỢC 12 ca PowerShell**; bảng trên chỉ đối chiếu văn bản với lời khai, không xác nhận thực nghiệm, cũng không khẳng định một `throw` đã được bắt vẫn dừng toàn script. Không nâng giới hạn đo này thành finding mới khi chưa có bằng chứng sai sự thật hoặc sai luật.

Snapshot trước/sau gate so nội dung SHA-256 và mode của **8.770 tệp**, HEAD/tree, index và status gồm tracked/untracked/ignored: khớp, status rỗng. Sandbox thực tế là `workspace-write`; checkout được giữ read-only bằng thao tác chỉ đọc, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0` và output ở `review_evidence/` bên ngoài `cay-kho/`. Snapshot chỉ chứng minh không có delta tại các mốc quan sát, không chứng minh lịch sử mọi thao tác ghi. Không quan sát/sửa kho nguồn ngoài clone được giao.

Bằng chứng: `review_evidence/static-audit.json`, `supplemental.json`, `checks.json`, snapshot `before.json`/`after.json` và stdout/stderr/metadata rc riêng từng lệnh. Script tái kiểm: `review_evidence/audit.py`.

## Đã chạy

Môi trường **Linux x86_64, Python 3.13.17**. Ba gate bắt buộc chạy trong `/tmp/claude-0/rv/pr1048-review-3/cay-kho` bằng `python3`, với `PYTHONDONTWRITEBYTECODE=1`; cả ba stderr rỗng, không gate nào skipped/not_run.

1. `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` — **rc 0, passed**. Stdout thật:

   ```text
   doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
   ```

2. `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py adr-song --root .` — **rc 0, passed**. Stdout thật:

   ```text
   adr-song: sạch — 57 ADR trên đĩa, 57 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])
   ```

3. `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json` — **rc 0, passed**. Các dòng kết quả trích nguyên từ stdout JSON:

   ```json
   "ok": true,
   "files_scanned": 117,
   "claims_flagged": 381,
   "flags": [],
   "advisory_count": 381,
   "layers_skipped": {},
   ```

   `381` là advisory, không phải lỗi cứng. JSON đầy đủ: `review_evidence/doc-claims-check.stdout`. Gate này không chứng minh các mệnh đề hành vi PowerShell.

Các lệnh dưới đây cũng chạy trong `cay-kho/`, trừ driver Python ghi rõ chạy ở sandbox:

4. `git rev-parse HEAD` — **rc 0**, `6f23a4e68805b4af3e2efe77be6e10b513843e93`; `git rev-parse HEAD^{tree}` — **rc 0**, `fd454a6a3121fead24d812b32de40c89f0a02e34`.
5. `git show -s --format=%H%n%P%n%T 6f23a4e68805b4af3e2efe77be6e10b513843e93` — **rc 0**, xác nhận thứ tự cha nêu trên; `git show -s --format='%H%n%P%n%T%n%s' b653574b117fa1496fbf58f09a22a8cbed5cc5dc` — **rc 0**, cha thứ hai là reviewed SHA.
6. `git merge-base 6f23a4e68805b4af3e2efe77be6e10b513843e93 5a174b958a05e13f5c9a968a2596ca37267d0466` — **rc 0**, `5a174b958a05e13f5c9a968a2596ca37267d0466`; `git merge-base 48b54d89b152871063c7296df33a60308667599e 5a174b958a05e13f5c9a968a2596ca37267d0466` — **rc 0**, `8cdb15a786304bab084b43c8b30c127ae87e2594`.
7. `git diff 5a174b958a05e13f5c9a968a2596ca37267d0466 6f23a4e68805b4af3e2efe77be6e10b513843e93` — **rc 0**, driver so byte với `diff.patch`: **true**. `git diff --numstat` trên cùng cặp SHA — **rc 0**, `10\t1\tCLAUDE.md` (tab biểu diễn bằng `\t`).
8. `git diff 48b54d89b152871063c7296df33a60308667599e 6f23a4e68805b4af3e2efe77be6e10b513843e93 -- CLAUDE.md` — **rc 0**, stdout rỗng. `git ls-tree -r -z` lần lượt trên SHA lượt 2, base và HEAD — **đều rc 0**; driver xác nhận 311 path đổi đều khớp master và HEAD ngoài `CLAUDE.md` không khác master.
9. `git diff --name-status 8cdb15a786304bab084b43c8b30c127ae87e2594 5a174b958a05e13f5c9a968a2596ca37267d0466 -- CLAUDE.md docs/ '*.ps1'` và `git diff --name-status 48b54d89b152871063c7296df33a60308667599e 6f23a4e68805b4af3e2efe77be6e10b513843e93 -- CLAUDE.md docs/ '*.ps1'` — **đều rc 0**, cả hai stdout rỗng.
10. `git ls-files -z -- '*.ps1'` — **rc 0**, 15 tệp. `rg -n -i --hidden --no-ignore -g '!**/.git/**' -g '*.ps1' 'Get-Content' .` — **rc 0**; đối chiếu bằng Python và đọc các ngữ cảnh, kết quả quét lớp ở trên.
11. `rg -n -i --hidden 'Get-Content|Value cannot be null|null-valued|\$null|\[string\]|Ép.*string|ép.*kiểu|BOM|KHOA\.txt|ErrorActionPreference|7\.6\.9|5\.1\.26100' CLAUDE.md docs/ -g '*.md'` — **rc 0**. `rg -l --hidden -g '!**/.git/**' 'KHOA\.txt' .` — **rc 0**. `git ls-files -- '*KHOA.txt'` — **rc 0**, stdout rỗng.
12. `git diff --check 5a174b958a05e13f5c9a968a2596ca37267d0466 6f23a4e68805b4af3e2efe77be6e10b513843e93` — **rc 0**, stdout rỗng.
13. `git rev-parse --is-shallow-repository` — **rc 0**, `false`; `git config --get core.abbrev` — **rc 0**, `7`; `git status --porcelain=v1 --untracked-files=all --ignored` — **rc 0**, stdout rỗng trước/sau gate và khi kiểm lại.
14. Tại sandbox: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py static` và `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py checks` — **đều rc 0**; `diff_matches_patch_bytes=true`, `checkout_unchanged=true`. `shutil.which('pwsh')` và `shutil.which('powershell')` đều trả `None` trong driver **rc 0**. **PowerShell: not_run / KHÔNG ĐO ĐƯỢC**, không tính là passed.
