verdict: changes_requested
reviewed_sha: a5464c3e84c9ef0ce4aec99e81749b2611976def
reviewed_tree: e02b0d40ab05d0f257e5206f3627e6a11d1cc708
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: OpenAI (tự khai)
reviewer_model: GPT-6 (tự khai; runtime attestation KHÔNG ĐO ĐƯỢC)
reviewer_execution_surface: Codex local sandbox (tự khai)
reviewer_transport: local tools (tự khai)

`changes_requested`: suite Windows độc lập xanh, nhưng còn **hai lớp P3 nằm trong sáu tệp write set**: các lời giải thích về thứ tự đọc jar và nghĩa của `stage_failure` vẫn sai trong tài liệu, và mục bảo trì cũ của RUNBOOK vẫn hướng người đọc tới `nlm login` định kỳ thay cho `nlm auth refresh` trên máy giữ browser profile gốc. Lớp hướng dẫn cũ **ngoài** write set vẫn cần Packet khác. Hai lớp lịch sử thiếu phép đo command-level/Linux được giữ là chưa nghiệm thu, **không** biến thiếu phép đo thành lỗi mã. Không cấp assurance, lease, admission, LIVE, approval hay land authority từ verdict này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

`Get-FileHash -Algorithm SHA256 SPEC.md,VERDICT_LUOT_TRUOC.md` → `A51164CF4BB0B3F41D4C01EF56A522C339CAAC008F2D855B3819A3EBB642BC0B`, `6BD5460CA787381256234C28E82BEAE49AB0F0E7E05FBC4AD3C84018F0334A43`, đúng hai hash được giao. `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'` → head/tree ở đầu verdict. `git -C cay-kho diff --numstat cde2ef4 a5464c3 -- <sáu path>` → changelog `1/1`, RUNBOOK `1/1`, Tests `18/0`, wrapper `3/2`, `tl_gws.py` `1/1`, `tl_selftest.py` không đổi. `git -C cay-kho apply --reverse --check -p0 <HINT_LUOT_TRUOC.patch>` → rc0. Lệnh `git log --ancestry-path cde2ef4..a5464c3` chỉ có head: **không có merge commit giữa đúng hai SHA này** như PROMPT nói; merge `186e6d5` nằm trước `505a483`. Đây là sai lệch mô tả phạm vi trong PROMPT, không phải finding sản phẩm.

| slug lớp cũ | phân loại trên head này | lệnh và output tự đo |
|---|---|---|
| `lookup-null-khong-duoc-suite-khoa` [P3] | **ĐÃ VÁ THẬT** | Reverse-check hint cũ rc0; `pwsh -NoProfile -File review-record-probe.ps1` → head `pid=4242 outside_job=True tree_unconfirmed=True`, mutant `pid= outside_job= tree_unconfirmed=True`; suite gốc `passed=34 failed=0`, rc0. Hunk Tests `:1198-1215` thực sự đòi PID/cờ khi process null. |
| `khai-rong-hon-phep-do-trong-changelog-runbook` [P3] | **VÁ HỜ** | Ba câu lượt trước đã sửa tại changelog `:99`, RUNBOOK `:752`, wrapper `:671-674`, `tl_gws.py:1747`. Nhưng RUNBOOK `:735-737` vẫn nói `stage_failure` nghĩa lệnh đã gọi; `review-prestart-probe.ps1` → `rc=6 status=stage_failure step=stage stage_calls=0 calls=--version,auth,notebook`. Changelog `:8` và RUNBOOK `:837` vẫn nói jar chỉ đọc sau canary; `review-jar-order-probe.py` → `rc=4 events=read_files,canary reader_has_read_call=True`. |
| `huong-dan-cu-con-lech-sau-va-ngoai-write-set` [P3] | **CHƯA VÁ** | `git diff --name-only cde2ef4 a5464c3 -- <bốn path cũ>` rỗng; `rg -n 'nlm login|login --check|nlm-auth-stage'` vẫn cho `scripts/tl_core/cli.py:145`, `scripts/nlm-auto-refresh.sh:76-85`, `references/COWORK_PROJECT.md:83,94`, `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`. **Cả bốn ở ngoài sáu path lease; cần Packet khác.** |
| `khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con` [P2 lịch sử] | **ĐÃ VÁ THẬT** cho fixture Windows đã đo | Suite Windows `34/0`, rc0, gồm ca z1 con treo ngoài Job và holder Job rỗng; mã `Write-OperationRecord` `:513-519`, `Get-RecordVerdict` `:569`, `Invoke-BoundedJob` `:669-679` giữ PID/cờ và không lấy số đếm Job rỗng làm chứng cứ cho con ngoài Job. OS Job API tự lỗi chưa đo. |
| `stage-da-goi-nhung-bao-inconclusive` [P2 lịch sử] | **ĐÃ VÁ THẬT** cho đường stage đã chạy | Suite gốc z2 `34/0`; mutant riêng làm nhánh `Exit-IfBlocked` bỏ qua `ran`: C# compile warning-as-error PASS, full suite rc1 tại Tests `:1315`, output `rc=5 status=inconclusive step=tree_containment reason=job_unknown`. Head giữ rc6 khi stage đã chạy mà Job không đo được. Lỗi trước tạo con cũng rc6/0 call; đó là lớp tài liệu ở trên. |
| `stdin-nul-chua-duoc-khoa-bang-test` [P3 lịch sử] | **ĐÃ VÁ THẬT** trong fixture Windows | `review-handle-order.py` → `handle_slots=3 list_size_three=True order_ok=True`; source `:233-271` có NUL trong list, stdin=NUL, giải phóng sau CreateProcess; suite `34/0` có ca `stdin_eof` và z1 chặn rò stdout. Không tái chạy NUL mutant lượt trước. |
| `stage-canary-true-khi-than-rong-hoac-sai-id` [P2 lịch sử thiếu phép đo] | **VÁ HỜ / chưa đóng độc lập** | `tl_gws.py` chỉ đổi chú thích. `python review-stage-gate-probe.py` trên đúng hai hàm với dependency giả: `force=True alive=True rc=0 uploads=1`; `False/None rc=4 uploads=0`; đây là body-level. Full `tl.py --selftest`/command-level dừng do temp sandbox, không có phép đo 101/168 byte Linux. **Không thấy biểu hiện mã sai mới; không nâng thành finding.** |
| `linux-subreaper-khong-thu-hoi-zombie` [P2 lịch sử thiếu phép đo] | **CHƯA VÁ / KHÔNG ĐO ĐƯỢC việc đóng** | Không có đổi mã Linux ở diff; `wsl.exe -d Ubuntu-Clean -u root -- pwd` → `Access is denied. Error code: Wsl/Service/E_ACCESSDENIED`, rc=-1. Không có phép đo bốn chu kỳ zombie hoặc Linux suite độc lập. **Không suy lỗi sản phẩm từ việc WSL bị chặn.** |

Các hướng cũ chưa đo khác: user/phiên Windows thứ hai, lỗi Job API do OS thật, ma trận quote/backslash đầy đủ. Chúng vẫn `KHÔNG ĐO ĐƯỢC`; suite/projection không thay cho môi trường thật.

## SPEC r4

| mục | đạt / một phần / chưa đạt / KHÔNG ĐO ĐƯỢC | căn cứ |
|---|---|---|
| 1. Host refresh | một phần | Wrapper có thứ tự/timeout và fake Windows suite; không gọi CLI/browser profile thật hay lấy fingerprint LIVE. |
| 2. Canary notebook | một phần | Suite fake Windows và bảng 35 ký tự khớp; parity Linux 101 dạng/168 byte, notebook thật chưa đo. |
| 3. Cổng `tl nlm-auth-stage` | một phần | Probe đúng thân hai hàm với `--force` True→upload1, False/None→0; full command/selftest chưa đo vì temp sandbox. Tiền kiểm có đọc jar vào RAM trước canary; upload vẫn sau canary dương trong probe. |
| 4. Windows thứ tự, lock, test | một phần | Native Windows suite `34/0`, rc0; mutant `ran` đỏ đúng ca; lỗi Job API do OS thật chưa đo. |
| 5. Trạng thái tách biệt | một phần | Suite fake kiểm nhãn; pre-start stage fault → rc6/0 call, stage đã chạy + Job unknown → rc6 (mutant đảo nhánh đỏ). RUNBOOK còn nói sai ở phần tổng quan. |
| 6. Keepalive/tiếp quản | một phần | Suite gốc chạy các ca native mutex, Job, z1; user/phiên Windows thứ hai và OS fault chưa đo. |
| 7. r209/manifest ứng viên | một phần | `tl_selftest.py:21616-21663` còn tám assertion và negative probe, tệp không đổi giữa hai head; full selftest/manifest candidate count chưa tự chạy hết vì `WinError 5` ở temp. Không sửa committed manifest. |
| 8. Gate/handoff | KHÔNG ĐO ĐƯỢC | Targeted Windows/diff/secret/ruff có rc riêng; full Python gate, Linux, CI/admission, LIVE/Drive và land thiếu phép đo hợp lệ trong sandbox. |

## BẢNG ĐO

`KHÔNG ĐO ĐƯỢC` là giới hạn phép đo, không phải kết luận mã sai. Không đọc credential, không gọi `nlm` thật, mạng hay Drive.

| khẳng định | PR/Executor khai | đo được | khớp? |
|---|---|---|---|
| Exact head/tree, Spec/verdict cũ | SHA trong bundle | `HEAD=a5464c3e84c9ef0ce4aec99e81749b2611976def`; tree `e02b0d40ab05d0f257e5206f3627e6a11d1cc708`; hai hash tệp khớp | khớp |
| Phạm vi g5 vòng 3 | năm path đổi, `tl_selftest.py` không đổi; hai chú thích runtime | `git diff --numstat cde2ef4 a5464c3 -- <sáu>` → `1/1,1/1,18/0,3/2,1/1,0`; hai tệp runtime chỉ đổi chú thích. Base→head giao write set đúng 6 path, tổng PR 162 path. | khớp; merge không nằm giữa hai head như PROMPT khai |
| HINT lượt trước áp nguyên | `git apply` rc0 | `git apply --reverse --check -p0` trên head rc0 | hunk khớp; thao tác lịch sử không quan sát trực tiếp |
| Windows suite | `34 passed, 0 failed`, rc0, 5m37s | `pwsh -NoProfile -File cay-kho/scripts/nlm-credential-refresh.Tests.ps1` → `passed=34 failed=0`, rc0, **540.5 s** | count/rc khớp; elapsed không tái lập, không coi là lỗi |
| Linux suite | `34/0`, rc0, 573 s, WSL pwsh 7.4.6 | WSL probe → `Wsl/Service/E_ACCESSDENIED`, rc=-1 | KHÔNG ĐO ĐƯỢC |
| Executor mutant I1 | “GIẾT ĐÚNG LÝ DO” | Probe cùng hunk: head PID/cờ có, mutant mất PID/cờ; full `mut7.py` không chạy vì nó tạo temp ngoài sandbox và dọn tiến trình Python toàn máy. Mutant **riêng** của reviewer ở `ran` compile PASS, full suite rc1 đúng z2. | I1 full-suite KHÔNG ĐO ĐƯỢC; hành vi hunk khớp |
| Full Python selftest | `1728/1728`, rc0 | `python scripts/tl.py --selftest` với `TEMP/TMP/TMPDIR` trong sandbox → rc1 sau 5.5 s tại `tl_selftest.py:346`, `PermissionError [WinError 5] ...\selftest-r3`; probe `tempfile.mkdtemp()` rồi `mkdir child` cũng WinError 5. Checkout vẫn sạch. | KHÔNG ĐO ĐƯỢC do sandbox; không quy cho sản phẩm |
| Ruff F trước/sau | cùng tập, delta 0 | `ruff check --select F --output-format json` → trước/sau cùng 97 diagnostics, 29 cặp `(code,message)` khác nhau, symmetric delta 0; cả hai rc1 do nợ lint nền | delta khớp; “31 dòng gộp” của commit không cùng cách đếm, KHÔNG ĐO ĐƯỢC theo đúng metric đó |
| `diff --check`, secret scan | rc0 trên năm/sáu path | `git diff --check cde2ef4 a5464c3 -- <năm>` rc0; base→head sáu path rc0; `pkg_secret_scan.py` trên bản sao sáu path rc0/output rỗng | khớp trong scope đã khai |
| Bản ghi null và ca z | PID từ CreateProcess, `outside_job` kể cả lookup null | `review-record-probe.ps1` head `pid=4242 outside_job=True`, mutant mất cả hai; suite `34/0` chạy ca z1/z2; mutant `ran` đỏ tại z2 với rc5/inconclusive sai | khớp fixture; OS fault thật chưa đo |
| Thứ tự handle/`NUL` | đúng ba handle, NUL stdin, giải phóng sau CreateProcess | `review-handle-order.py` → `handle_slots=3 list_size_three=True order_ok=True`; C# warning-as-error PASS trước mutant; suite stdin EOF/z1 xanh | khớp code/fixture; không đo handle leak ở mọi OS fault |
| Bảng trắng, ngưỡng số | 35 codepoints; timeout 120 s, lock 10 s, interval 3600 s, default 1 cycle, quarantine 900 s, fingerprint 16 hex, lý do 8–200 ký tự, Job wait 5 s | Hai bảng exact sequence bằng nhau, cùng 35; source wrapper `:12-22,:623-636,:960-971`, fingerprint `:343,:969` có các hằng/điều kiện tương ứng; suite fake dùng nhiều ngưỡng rút ngắn | khớp mã tĩnh; thời lượng mặc định KHÔNG ĐO ĐƯỢC |
| `stage_failure` luôn đã gọi stage | Câu RUNBOOK `:736`; dòng bảng `:752` đã sửa | `review-prestart-probe.ps1` → rc6/stage_calls0; `:752` đúng, `:736` sai | **lệch tài liệu** |
| Jar chỉ đọc sau canary | changelog `:8`, RUNBOOK `:837`; chú thích code `:1747` đã sửa | `_nlm_auth_files` đọc file ở `tl_gws.py:747`; `review-jar-order-probe.py` → `read_files,canary` khi gate âm; `review-stage-gate-probe.py` True→`read_files,canary,read_files,upload` | **lệch tài liệu**, không thấy upload trước canary |
| Bảo trì định kỳ | RUNBOOK `:203-205` chỉ `nlm login`/headless rồi `secrets-set --nlm` | RUNBOOK `:696-697` và Spec yêu cầu `nlm auth refresh` trên host gốc, canary rồi stage; cùng một RUNBOOK tự mâu thuẫn | **lệch hướng dẫn** |
| Số lịch sử | 101/168 parity Linux, 4 chu kỳ zombie, 13 phút pipe, drift 2.9s/130s và 7.0s/256s; GWS 60/60/30, 9/9, 2/2, 14/14, throughput/timing cũ | không có rig/đầu vào hoặc WSL độc lập; không tái lập các lượt lịch sử trong sandbox | KHÔNG ĐO ĐƯỢC; không suy sai chỉ vì chưa đo |
| LIVE/lease/admission/CI | Executor tự khai chưa làm hoặc thiếu receipt | Không gọi mạng/LIVE, không có receipt độc lập trong bundle | `not_measured`; không suy `passed` |

## BẢNG SĂN

Các hướng S1–S8 là tám giả thuyết độc lập của lượt này. S1/S2 đi sâu hơn lớp tài liệu lượt trước bằng **câu khác còn sót**, S4 dùng mutant `ran` mới, S5 xem đường giải phóng handle thay vì chỉ sự hiện diện của list. Không dùng mutant không biên dịch làm tín dụng.

| hướng: giả thuyết | lệnh / output thật | kết luận |
|---|---|---|
| **S1.** Tổng quan RUNBOOK vẫn đồng nhất `stage_failure` với “đã gọi stage”, dù dòng bảng mới cho phép pre-start 0 call. | `rg -n 'stage_failure|lệnh stage ĐÃ' cay-kho/references/RUNBOOK.md` → `:736` câu cũ, `:752` câu mới; `pwsh -NoProfile -File review-prestart-probe.ps1` → `rc=6 status=stage_failure step=stage stage_calls=0 calls=--version,auth,notebook`. | **LỖI tài liệu** ở lớp cũ; projection không gọi CLI thật. |
| **S2.** Chú thích Python đã sửa nhưng changelog/RUNBOOK vẫn khẳng định không đọc jar trước canary. | `rg -n 'read the credential jar only|trước khi đọc jar|_nlm_auth_files'` → changelog `:8`, RUNBOOK `:837`, code `:1747`; `python review-jar-order-probe.py` → `rc=4 events=read_files,canary reader_has_read_call=True`; `review-stage-gate-probe.py` False/None upload0. | **LỖI tài liệu**; không có bằng chứng upload trước canary. |
| **S3.** Đoạn bảo trì cũ trong cùng RUNBOOK có thể bỏ qua đường refresh của WP710. | `rg -n 'Bảo trì ~2|nlm auth refresh' cay-kho/references/RUNBOOK.md` → `:203-205` bảo trì bằng `nlm login`/headless, `:696-697` quy trình `nlm auth refresh`→canary→stage. | **LỖI hướng dẫn** mới trong write set. |
| **S4.** `ran` chỉ hiện trong source, suite không bắt hồi quy nếu stage đã chạy bị báo `inconclusive`. | Bản sao đổi duy nhất `if ($step -eq 'stage' -and $result.ran)`→`... $false`; `Add-Type -WarningAction Stop -ErrorAction Stop` → `compile=PASS`; `pwsh -NoProfile -File review-ran-mutant/nlm-credential-refresh.Tests.ps1` → suite rc1, 487.4 s, Tests `:1315`: `rc=5 status=inconclusive step=tree_containment reason=job_unknown`. Suite gốc rc0/34. | **KHÔNG PHẢI LỖI** ở head; ca z2 thực sự ép phân loại `ran`. |
| **S5.** Handle list có thể đúng số nhưng đóng NUL/list trước khi CreateProcess dùng xong, hoặc quên đóng write ends. | `python review-handle-order.py` → `handle_slots=3 list_size_three=True order_ok=True`; source `:233-271` xếp NUL, ba slots, Update, std handles, CreateProcess, Delete/Free/Close; suite gốc `34/0` có stdin EOF và z1. | **KHÔNG PHẢI LỖI** trong source/fixture đã đo; lỗi handle do OS thật KHÔNG ĐO ĐƯỢC. |
| **S6.** Con số “35 ký tự” trong changelog/RUNBOOK có thể lệch giữa Python và PowerShell. | `python review-blank-table.py` → `python_count=35 ps_count=35 exact_sequence_equal=True`, rc0. | **KHÔNG PHẢI LỖI** trong hai bảng hiện tại. |
| **S7.** Claim ruff/diff/secret có thể là xanh giả do scope hoặc so khác metric. | `ruff check --select F --output-format json` trên `tl_gws.py` cũ/mới → 97/97 diagnostics, 29/29 unique pairs, delta0 (cả hai rc1); `git diff --check` sáu path rc0; `pkg_secret_scan.py` bản sao sáu path rc0. | **KHÔNG PHẢI LỖI** với scope/metric ghi rõ; không gọi ruff rc1 là pass. |
| **S8.** Câu “merge master giữa hai lượt” và số path write set có thể làm reviewer đo nhầm diff. | `git log --ancestry-path cde2ef4..a5464c3` → chỉ `a5464c3`; parent trực tiếp `cde2ef4`; `git diff --name-only cde2ef4 a5464c3` → 5 path; base→head trong write set → 6/6, toàn PR 162 path. | **LỖI mô tả trong PROMPT**, không phải lỗi sản phẩm; đo diff hai head đúng năm path. |
| **S9.** Linux/selftest có thể xác nhận các lớp lịch sử chưa đóng. | `wsl.exe -d Ubuntu-Clean -u root -- pwd` → `Wsl/Service/E_ACCESSDENIED`, rc-1; Python selftest với temp trong sandbox → `WinError 5` tạo `selftest-r3`, rc1. `chay-linux.sh` nguyên bản ghi `/opt`, `/root`, `/tmp` ngoài phạm vi. | **KHÔNG ĐO ĐƯỢC** các hành vi Linux/full Python; không quy lỗi cho head. |

## FINDING THEO LỚP

### khai-rong-hon-phep-do-trong-changelog-runbook  [P3]  Hai lời khẳng định tuyệt đối vẫn lệch mã

TỆP/DÒNG: `references/RUNBOOK.md:735-737,752,835-838`; `changelog.d/wp-710.md:4-9`; liên hệ `scripts/nlm-credential-refresh.ps1:1041-1047`, `scripts/tl_gws.py:737-753,1747-1757`.

VẤN ĐỀ: Trên **head này**, câu tổng quan RUNBOOK nói rc6 nghĩa lệnh stage đã được gọi, trái chính dòng trạng thái mới và projection pre-start rc6/0 call. Changelog và RUNBOOK cũng còn nói chỉ đọc jar sau canary, dù tiền kiểm `nlm-auth-stage` đọc jar vào RAM trước khi gọi cổng. Đây là **lỗi lời khai tài liệu** trong hai path write set; các probe không cho thấy upload khi canary âm, và không biến giới hạn command-level thành lỗi mã.

ĐÃ THỬ VÁ: có — `HINT.patch` sửa ba câu tài liệu, không đụng tệp runtime nhạy cảm. Nếu Executor muốn thay đổi chính tiền kiểm thay vì sửa lời mô tả, cần tự thiết kế/đo hành vi đó dưới Packet; reviewer không soạn patch runtime.

ĐÃ THỬ NGHIỆM: `review-prestart-probe.ps1` rc6/stage_calls0; `review-jar-order-probe.py` `read_files,canary`; `review-stage-gate-probe.py` False/None upload0, True upload1. HINT `git apply --check` và áp trên bản sao rc0; `patch.exe --dry-run` KHÔNG ĐO ĐƯỢC do sandbox (chi tiết dưới).

ĐỘ TIN: cao về mâu thuẫn và đường mã; không suy tần suất lỗi pre-start thật.

### runbook-bao-tri-cu-bo-qua-refresh  [P3]  Mục bảo trì cũ vẫn chỉ dẫn login định kỳ

TỆP/DÒNG: `references/RUNBOOK.md:191-205,696-697`.

VẤN ĐỀ: Phần bootstrap dùng `nlm login` lần đầu là hợp lý. Riêng câu **bảo trì định kỳ** `:203-205` vẫn bảo chạy `nlm login` hoặc dựa vào headless refresh rồi `tl secrets-set --nlm`. Mục WP710 sau đó và Spec r4 xác định thao tác refresh là `nlm auth refresh` trên máy giữ browser profile gốc, xác nhận canary dương trước stage; lỗi xác thực mới cần đăng nhập lại. Hai hướng dẫn trong cùng RUNBOOK mâu thuẫn, khiến người vận hành có thể bỏ đường `nlm auth refresh` của quy trình mới. Cổng riêng của `secrets-set --nlm` vẫn kiểm canary trước upload. Đây là **lỗi tài liệu trong write set**, không chứng minh code đã stage sai.

ĐÃ THỬ VÁ: có — `HINT.patch` sửa câu bảo trì để dùng refresh→canary, nêu login tương tác khi refresh báo lỗi xác thực, và giữ cổng canary riêng của `secrets-set --nlm`.

ĐÃ THỬ NGHIỆM: `rg -n 'Bảo trì ~2|nlm auth refresh' references/RUNBOOK.md` → `:203-205` so với `:696-697`; HINT trên bản sao `git apply --check`/apply rc0. Không gọi CLI thật.

ĐỘ TIN: cao về mâu thuẫn tài liệu; không đo LIVE.

### huong-dan-cu-con-lech-sau-va-ngoai-write-set  [P3]  Hướng dẫn cũ ngoài lease còn lệch workflow

TỆP/DÒNG: `scripts/tl_core/cli.py:145`; `scripts/nlm-auto-refresh.sh:76-85`; `references/COWORK_PROJECT.md:83,94`; `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`.

VẤN ĐỀ: Bốn path **ngoài sáu tệp write set** vẫn chỉ `nlm login`/`login --check`, hoặc nuốt rc của `nlm-auth-stage`; cần Packet khác với owner/write set riêng. Không quy lỗi này cho Executor vòng 3 vì không có quyền sửa các path ấy.

ĐÃ THỬ VÁ: không trong Packet này; hướng xử lý bằng lời: cập nhật help/flow cũ và để stage rc hiện rõ dưới Packet khác.

ĐÃ THỬ NGHIỆM: `git diff --name-only cde2ef4 a5464c3 -- <bốn path>` rỗng; `rg` vẫn cho các dòng nêu trên. Không chạy LIVE.

ĐỘ TIN: cao.

## ĐẾM LỚP MỞ

| loại | P1 | P2 | P3 | tổng |
|---|---:|---:|---:|---:|
| finding có biểu hiện sai ở head, trong sáu path | 0 | 0 | 2 | 2 |
| finding ngoài sáu path, cần Packet khác | 0 | 0 | 1 | 1 |
| lớp lịch sử chưa có phép đo đủ để tuyên bố đóng, **không nâng thành finding** | 0 | 2 | 0 | 2 |
| tổng lớp còn mở hoặc chưa nghiệm thu | 0 | 2 | 3 | 5 |

Hai lớp lịch sử thiếu đo là `stage-canary-true-khi-than-rong-hoac-sai-id` và `linux-subreaper-khong-thu-hoi-zombie`. Ngưỡng `approve` chặt hơn trong PROMPT không đạt vì còn hai P3 trong sáu path, dù suite Windows đã chạy xanh. Không nhận `cross_approved` chỉ từ tên provider/model tự khai: runtime attestation và delivery/assurance bên ngoài sandbox chưa đo.

## HINT.patch

Dòng đầu giữ đúng nhãn nguyên văn. Patch chỉ sửa `changelog.d/wp-710.md` và `references/RUNBOOK.md`, dùng đường dẫn repo-relative không có `a/`–`b/`. Trên bản sao `review-hint-copy2/`, `git apply --check -p0 <HINT.patch>` rc0 và `git apply -p0 <HINT.patch>` rc0; không sửa `cay-kho`. Đã thử đúng `patch -p0 --fuzz=0 --dry-run -i <HINT.patch>` trên bản sao, nhưng `patch.exe` dừng **trước khi đọc patch**: `CreateFileMapping ... Win32 error 5`, rc256. Vì vậy phép dry-run bằng `patch` là **KHÔNG ĐO ĐƯỢC do sandbox**, không khai thành pass. Executor tự áp, tự đo, tự chịu trách nhiệm commit.

## TRẠNG THÁI CHECKOUT CUỐI

`git -C cay-kho status --porcelain=v1 --untracked-files=all` → **output rỗng**, rc0. `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'` → `a5464c3e84c9ef0ce4aec99e81749b2611976def` / `e02b0d40ab05d0f257e5206f3627e6a11d1cc708`. Bản ghi `review-tmp/tra_luat_nlm_credential_refresh.operation.json` không tồn tại sau suite/mutant. Các bản sao/probe nằm ở gốc sandbox; không gọi mạng, LIVE, CLI `nlm` thật hoặc đọc credential.
