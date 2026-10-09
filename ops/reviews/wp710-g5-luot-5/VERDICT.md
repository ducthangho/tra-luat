verdict: changes_requested
reviewed_sha: 505a483e50bef5f84e4403ef0a1cb2277d32d4ac
reviewed_tree: 20a5a743682e7912f7274415ba012f836272caa8
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: OpenAI (tự khai)
reviewer_model: GPT-6 (tự khai; runtime/model header KHÔNG ĐO ĐƯỢC)

Lý do `changes_requested`: phản chứng trên head này cho thấy bản ghi con treo ngoài Job có thể bị coi là `clear` nếu thiếu `StartTime` **và một tiến trình khác còn giữ handle của Job rỗng**. Đường đóng Job thông thường trả `quarantine`. Suite không bắt một đột biến làm mất `NUL` stdin. RUNBOOK/changelog còn mô tả rc 5 cho cả trường hợp sau khi stage đã chạy, trái mã và bảng status. Hướng dẫn cũ ngoài write set vẫn cần Packet khác. Đây là verdict nội dung trên bản sao offline; không cấp lease, admission, LIVE, approval hay land authority.

## NHẬT KÝ ĐO

- SHA-256 `SPEC.md` = `a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b`; `VERDICT_LUOT_TRUOC.md` = `30849ac51d0f1906169fff741f065aa4ddfef28e1626aedda7e31807e09d7547`. `git -C cay-kho rev-parse HEAD` = `505a483e50bef5f84e4403ef0a1cb2277d32d4ac`; `status --porcelain` rỗng.
- `git diff --stat ed12889 505a483 -- <sáu tệp>`: chỉ bốn tệp đổi: changelog `23/16`, RUNBOOK `11/3`, Tests `107/2`, wrapper `74/21` (số thêm/xóa). Hai tệp Python không đổi giữa hai head. Đây là phạm vi cần review của g5.
- `git diff --check ed12889 505a483 -- <sáu tệp>` rc 0; `git diff --check 8c98afa 505a483 -- <sáu tệp>` rc 0. Nhưng `git diff --check 8c98afa 505a483` trên toàn PR rc 2 vì trailing whitespace trong các tệp `ops/reviews/` từ merge. Khẳng định không ghi rõ phạm vi của commit cần giới hạn lại.
- Đọc mã: `Start` nay trả `pid`, nhánh `*_alive` đặt `$started=$true` và giữ record; `Exit-IfBlocked` dùng `ran` để phân biệt stage đã chạy. Suite Windows chạy với `TEMP/TMP/TMPDIR` trỏ `review-temp/` dưới sandbox.
- `python cay-kho/scripts/tl.py --selftest` với `TEMP/TMP/TMPDIR=review-selftest-temp` dừng rc 1 trước tổng kết ở `tl_selftest.py:346`, `PermissionError [WinError 5]` khi tạo `selftest-r3` trong thư mục tạm Python vừa tạo. Probe riêng `tempfile.mkdtemp(dir=review-selftest-temp)` rồi `mkdir('probe')` cũng `PermissionError [WinError 5]` (rc 1). Kết luận hiện tại: full selftest **KHÔNG ĐO ĐƯỢC** vì sandbox.
- `wsl.exe -d Ubuntu-Clean -u root -- pwd` rc 1: `Access is denied. Error code: Wsl/Service/E_ACCESSDENIED`. Linux suite, zombie/subreaper và parity Linux **KHÔNG ĐO ĐƯỢC** tại đây. Không chạy `chay-linux.sh` vì helper đó ghi `/root`, `/opt`, `/tmp` ngoài sandbox.
- Probe độc lập `tl_core.release._build_release_manifest(root)` và `_doc_pointer_findings`: `files=183`, wrapper mới có trong manifest, `docs=36`, `pointers_ok=True`, `fail=0`, `advisory=107`, `baseline=3`. Chèn `references/RUNBOOK.md: scripts/no_such_wp710_file.py` vào bộ tài liệu trong RAM trả `negative_ok=False`, đúng một pointer fail.
- Hướng săn mới: nhánh con treo ngoài Job nhưng không đọc được `StartTime`. `pwsh -NoProfile -File review-probe.ps1` biên dịch C# với warning-as-error, tạo Job rỗng và một con sống ngoài Job, ghi record `pid` thật/`start_ticks=null`/`tree_unconfirmed=true`. Output: **giữ handle Job mở** `fixture_alive=True ... job_probe=0 job_active=0 verdict=clear`; **đóng handle Job cuối** `fixture_alive=True job_probe=1 verdict=quarantine reason=job_closed_unconfirmed`. Mã `Get-StartTicks` cho phép null ở `:360-361`; `Test-RecordedRootAlive` trả null nếu thiếu ticks ở `:527`; `Get-RecordVerdict` trả clear khi Job đếm 0 ở `:565` dù record unconfirmed. Đây là biểu hiện có điều kiện, chỉ khi có holder thứ hai của Job rỗng; lỗi đọc StartTime và holder ngoài wrapper thật chưa đo.
- Hướng săn tài liệu: `changelog.d/wp-710.md:60-63` và `references/RUNBOOK.md:803-807` vẫn nói mọi Job không về 0 trả rc 5/`tree_containment`, trong khi `:77-78` và RUNBOOK `:752` nói stage đã chạy trả rc 6/`stage_failure`. Mâu thuẫn còn trong cùng hai tệp sau g5.
- Windows `pwsh -NoProfile -File cay-kho/scripts/nlm-credential-refresh.Tests.ps1` với temp dưới sandbox: `passed=33 failed=0`, rc 0. Ca z có hai khẳng định z1/z2 trong cùng một `$cases++` (`Tests.ps1:1169-1263`); suite xanh chứng minh ca z đã đi qua trên Windows, không chứng minh API của OS thật tự lỗi.
- `python cay-kho/scripts/pkg_secret_scan.py review-secret-scan` trên đúng sáu tệp copy: output rỗng, rc 0.
- Đột biến tự dựng trên bản sao: `si.Info.hStdInput = nul` → `outWrite` (`anchor_count=1`); C# `Add-Type -WarningAction Stop -ErrorAction Stop` PASS. Probe trực tiếp `review-handle-probe.ps1` trên bản gốc: `resumed=True exited=True rc=0 stdout=EOF`; trên mutant: `resumed=True exited=True rc=1 stdout=`.
- Kết quả suite đột biến stdin: `passed=33 failed=0`, rc 0, dù probe trực tiếp đã xác nhận stdin của mutant không đọc được. Ca z1 chứng minh stdout của wrapper đóng đúng nhưng không đo stdin=`NUL`; đây là lỗ test mới, không phải lỗi runtime ở g5.
- Mock trực tiếp `_nlm_auth_stage_body` với `force=True`, kho giả và upload spy, không đọc credential: `canary=True rc=0 uploads=1`, `False rc=4 uploads=0`, `None rc=4 uploads=0`. Lượt đầu của harness thiếu `HOPNAP_FOLDER_ID` và dừng `NameError`; sau khi cung cấp global giả vốn do `tl.py` nạp, phép đo trên chạy rc 0. Đây là đo hàm thân, không phải `tl nlm-auth-stage` cuối-đầu.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT_LUOT_TRUOC.md` SHA-256 `30849ac5…7547`, head `ed1288908e533491456f320e3ce07081f129c0a7`. Lệnh `git -C cay-kho diff --name-only ed12889 186e6d5` cho `151` path; giao sáu path write set bằng `0`. `git diff --numstat ed12889 505a483 -- <sáu path>` cho changelog `23/16`, RUNBOOK `11/3`, Tests `107/2`, wrapper `74/21`; hai tệp Python không đổi.

| slug lớp cũ | phân loại | phép đo và giới hạn |
|---|---|---|
| `khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con` | **VÁ HỜ** | `Start` trả PID (`wrapper:273`); nhánh `_alive` giữ record (`:659-667`), ca z1 chạy trong suite `33/0`. Nhưng `review-probe.ps1` cho con ngoài Job còn sống + record thiếu `start_ticks` **khi holder thứ hai giữ Job rỗng** ⇒ `Get-RecordVerdict=clear`; đóng handle cuối ⇒ `quarantine`. Không đóng lớp vì state có điều kiện này chưa được chặn. |
| `stage-da-goi-nhung-bao-inconclusive` | **ĐÃ VÁ THẬT** đối với biểu hiện Windows cũ | `Exit-IfBlocked` ở `:919-930` chọn `stage_failure` nếu `ran`; ca z2 ép `job_unknown` **sau** khi fake stage ghi flag, kiểm một stage call và rc 6 (`Tests:1239-1256`); suite Windows `33/0`. Đường lỗi OS tự phát sinh và Linux vẫn KHÔNG ĐO ĐƯỢC, không suy từ phép chiếu. |
| `stage-canary-true-khi-than-rong-hoac-sai-id` | **VÁ HỜ** | Tự đếm bảng trắng Python/PS: `35/35`, bằng nhau; case n Windows trong suite `33/0` chạm các control và transport. Hai phép parity Linux `101` dạng/`168` byte không chạy lại được vì WSL `E_ACCESSDENIED`; chưa đủ đóng lịch sử lớp. Không thấy sai ở tập Windows đã đo. |
| `linux-subreaper-khong-thu-hoi-zombie` | **VÁ HỜ** | Mã `waitpid` và case v Linux-only còn đó; `wsl.exe -d Ubuntu-Clean -u root -- pwd` rc 1 `Wsl/Service/E_ACCESSDENIED`. Bốn chu kỳ zombie=0 chỉ là lời khai; chưa đủ đóng lớp. Không tạo finding lỗi code chỉ từ khoảng trống đo. |
| `khai-rong-hon-phep-do-trong-changelog-runbook` | **VÁ HỜ** | G5 thêm nhánh stage_failure đúng ở RUNBOOK `:752`/changelog `:77-78`, nhưng RUNBOOK `:803-807` và changelog `:60-63` vẫn nói Job count không về 0 ⇒ rc 5/tree_containment cho mọi bước. Full-PR `diff --check` rc 2 trong khi claim không ghim scope; sáu path thì rc 0. |
| `huong-dan-cu-con-lech-sau-va-ngoai-write-set` | **CHƯA VÁ** | `git diff ed12889 505a483 --` trên bốn tệp hướng dẫn cũ rỗng. `rg -n 'nlm login|login --check|nlm-auth-stage'` vẫn thấy `scripts/tl_core/cli.py:145`, `scripts/nlm-auto-refresh.sh:76-85`, `references/COWORK_PROJECT.md:83,94`, `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`. Ngoài lease sáu tệp, cần Packet khác. |

Các hướng săn cũ ở `KHÔNG ĐO ĐƯỢC`: (H3) handle thừa kế được đo sâu hơn: probe stdin gốc EOF, ca z1 Windows kiểm ống stdout đóng, nhưng mutation stdin vẫn xanh ⇒ tìm thấy lỗ test mới. (H4) user/phiên Windows thứ hai vẫn KHÔNG ĐO ĐƯỢC vì không có fixture hai user. (H5) `Quote` chạy được với `python -c` chứa dấu cách trong probe handle, nhưng ma trận argv/quote/backslash chưa đo đủ. (H6) các case Linux-only vẫn KHÔNG ĐO ĐƯỢC do WSL bị chặn. (H7) C# gốc và mutant đều `Add-Type -WarningAction Stop -ErrorAction Stop` thành công; không lấy đỏ do biên dịch hỏng làm tín dụng.

## SPEC r4

| mục | trạng thái | căn cứ |
|---|---|---|
| 1 | một phần | Suite Windows fake đo thứ tự, timeout, fingerprint 16 hex; CLI/profile thật và ràng buộc profile với CLI chưa đo, `profile_bound_to_cli=false`. |
| 2 | một phần | 35/35 bảng trắng và case n Windows xanh; parity 101/168 Linux cùng CLI thật KHÔNG ĐO ĐƯỢC. |
| 3 | một phần | Mock thân hàm `force=True` cho True→`rc0/upload1`, False/None→`rc4/upload0`; command-level `tl nlm-auth-stage` và full selftest KHÔNG ĐO ĐƯỢC do sandbox. |
| 4 | một phần | Suite Windows `33/0` xác nhận fake order/upload, stage failure, secret suppression; đột biến stdin đã biên dịch và sống sót `33/0`, nên test chưa khóa tuyên bố NUL mới. |
| 5 | một phần | Ca z2 đo stage đã chạy→`stage_failure` rc6; các nhánh `ran` được đọc ở cả Job (`:700`) và non-Job (`:787`). OS API thật lỗi và Linux runtime chưa đo. |
| 6 | một phần | Ca z1 đo có PID/ticks; phản chứng `start_ticks=null` với một holder khác giữ Job rỗng cho `clear` dù con ngoài Job còn sống. Khi Job đóng như bình thường, hệ thống trả `quarantine`. |
| 7 | một phần | Manifest ứng viên `183` tệp gồm wrapper mới, pointer fail `0`, advisory `107`, baseline `3`; con trỏ giả vào RUNBOOK bị bắt. Tám assertion r209 hiện diện trong mã nhưng full selftest không chạy được. Committed manifest không đổi trong diff sáu tệp. |
| 8 | KHÔNG ĐO ĐƯỢC | Targeted Windows/scan/diff sáu tệp có rc riêng. Full Python selftest, Linux, full repository gates, admission, CI required và LIVE không có bằng chứng đủ trong sandbox. |

## BẢNG ĐO

`KHÔNG ĐO ĐƯỢC` dưới đây không có nghĩa là mã sai. Các con số lịch sử ngoài WP710 trong RUNBOOK (ví dụ `60/60/30`, `101/101`, `9/9`) không có phép tái lập tương ứng trong bundle và không được nhận là đã kiểm.

| khẳng định | PR/Executor khai | tự đo được | khớp? |
|---|---|---|---|
| Spec/verdict trước/head/tree | SHA spec `a51164cf…`, verdict `30849ac5…`, head `505a483` | Hash đầy đủ khớp; HEAD `505a483e50bef5f84e4403ef0a1cb2277d32d4ac`; tree `20a5a743682e7912f7274415ba012f836272caa8` | khớp |
| Merge và g5 path | merge 151 path, 0 giao sáu; g5 bốn tệp | `git diff --name-only ed12889 186e6d5`: `151`, giao `0`; g5 numstat `23/16`, `11/3`, `107/2`, `74/21`, Python rỗng | khớp |
| Windows `Tests.ps1` | `33 passed/0 failed`, rc0, 6m06s | `passed=33 failed=0`, rc0 một lượt; không ghi stopwatch độc lập | khớp số/rc; thời gian KHÔNG ĐO ĐƯỢC |
| Linux `Tests.ps1`, trước sửa case m | `34/0` rc0; hai head cũ rc1 ở m | WSL `E_ACCESSDENIED` ngay ở `pwd` | KHÔNG ĐO ĐƯỢC |
| Drift WSL | 2,9 s/130 s; 7,0 s/256 s | script đo không có, WSL bị chặn | KHÔNG ĐO ĐƯỢC |
| G1/G2/G3 Executor | 3/3 đỏ đúng ca | Không chạy `mut5.py`: script tự ghi `/tmp`/temp người dùng và dọn tiến trình toàn máy, trái sandbox. Mutant độc lập stdin của reviewer biên dịch PASS và **sống sót 33/0** | 3/3 KHÔNG ĐO ĐƯỢC; mutant khác phạm vi |
| Full Python selftest | `1728/1728`, rc0 | rc1 trước tổng kết do `PermissionError [WinError 5]` trên thư mục tạm Python tạo; probe `mkdtemp→mkdir` cũng rc1 | KHÔNG ĐO ĐƯỢC do sandbox |
| 13 phút pipe treo trước g5 | một quan sát, không có rig | ca z1 và probe trực tiếp đo hiện tại; 13 phút lịch sử không tái lập | KHÔNG ĐO ĐƯỢC |
| Handle list và NUL | ba handle, NUL stdin | C# list ghi 3 pointer (`:244-260`); direct probe gốc `rc0/stdout=EOF`, mutant stdin `rc1`; stdout z1 nằm trong suite xanh | khớp tập đã đo; mọi handle khác chưa liệt kê |
| `diff --check` | rc0, scope không ghi | `git diff --check ed12889 505a483 -- <sáu>` rc0; base→head sáu path rc0; **base→head toàn PR rc2** do trailing whitespace tại `ops/reviews/` từ merge | chỉ khớp scope sáu path |
| Secret scan | rc0 sáu tệp | Copy đúng sáu path, `python pkg_secret_scan.py review-secret-scan` output rỗng rc0 | khớp |
| Canary table/parity | 35, 101 dạng/0 lệch, 168 byte/0 lệch | Python/PS `35/35 same=True`; Windows case n trong suite; rig 101/168 không có | 35 khớp; 101/168 KHÔNG ĐO ĐƯỢC |
| Zombie 4 chu kỳ | mỗi khoảng 0, trước `[1,2,3]` | Linux không gọi được | KHÔNG ĐO ĐƯỢC |
| Manifest/pointer | 183, 0 fail, 107 advisory, 3 baseline, tám assertion | Helper: `183`, wrapper có, `docs=36`, `True/0/107/3`; pointer giả bị bắt đúng 1; tám assertion chỉ đọc mã | helper khớp; tám assertion KHÔNG ĐO ĐƯỢC |
| Stage upload `--force` | True=1, False/None=0 | mock trực tiếp `_nlm_auth_stage_body`: `rc0/1`, `rc4/0`, `rc4/0` | khớp thân hàm; command-level KHÔNG ĐO ĐƯỢC |
| RUNBOOK/changelog rc sau stage | sau stage đã chạy là rc6, trước stage rc5 | Mã `Exit-IfBlocked`/z2 đúng; hai đoạn tổng quan tài liệu vẫn ghi mọi Job count không về 0 là rc5 | **lệch trong tài liệu** |
| LIVE/CI/admission/lease g5 | Executor tự khai chưa làm hoặc không có receipt riêng | Không gọi mạng/CLI LIVE; bundle không chứng minh các trạng thái ấy | không suy `passed` |

## BẢNG SĂN

Các hướng dưới đây độc lập về cơ chế; H4/H5 đi sâu hơn hướng status/handle lượt trước bằng đối chứng mới. Mỗi output là kết quả của lệnh trong sandbox này, không chép từ EVIDENCE.

| hướng: giả thuyết | lệnh / output thật | kết luận |
|---|---|---|
| **H1.** `_alive` có PID nhưng thiếu `StartTime` và có holder khác giữ Job rỗng thì chủ sau có thể coi con ngoài Job là đã hết. | `pwsh -NoProfile -File review-probe.ps1`: C# compile warning-as-error PASS; `held_job fixture_alive=True ... job_probe=0 job_active=0 verdict=clear`; sau `Close(job)`: `closed_job fixture_alive=True job_probe=1 verdict=quarantine reason=job_closed_unconfirmed`. `wrapper:360-361,527,559-566` đúng đường điều khiển. | **LỖI có điều kiện** ở state Job được giữ mở; đường đóng Job thông thường an toàn. Lỗi đọc `StartTime` thật và holder ngoài wrapper chưa ép bằng OS. |
| **H2.** Ca z1 kiểm ống stdout, bỏ qua lời khai stdin=`NUL`. | Đổi duy nhất `si.Info.hStdInput = nul`→`outWrite` trên bản sao, anchor=1, C# compile PASS. Probe trực tiếp: gốc `rc0/stdout=EOF`, mutant `rc1/stdout=`; suite gốc **và mutant** đều `passed=33 failed=0`. | **LỖI TEST**: đột biến có hiệu lực nhưng sống sót. Runtime g5 cho NUL đúng trên fixture. |
| **H3.** Các đoạn tổng quan mới sửa tài liệu có thể vẫn mâu thuẫn bảng status. | `rg -n 'tree_containment|stage_failure' changelog/RUNBOOK`; output changelog `:60-63` rc5 cho Job count, `:77-78` rc6 sau stage; RUNBOOK `:803-807` rc5, `:752` rc6. | **LỖI tài liệu** cùng lớp cũ. |
| **H4.** Cờ `ran` có thể chỉ gắn một lối trả, làm stage đã chạy báo inconclusive ở lối khác. | Đọc `Invoke-BoundedJob:636-704`, `Invoke-Bounded:716-795`, `Exit-IfBlocked:919-930`; blocked sau process chạy có `ran=$true` ở Job `:700` và non-Job `:787`; timeout stage đi `:1034-1036`; pre-run blocked không có `ran`. Ca z2 ép stage flag/counter, suite Windows `33/0`. | **KHÔNG PHẢI LỖI** trong các lối đã phân tích/Windows đã chạy; Linux runtime và lỗi OS tự phát KHÔNG ĐO ĐƯỢC. |
| **H5.** Danh sách handle/giải phóng có thể làm con không nhận stdin NUL hoặc giữ ống của caller. | `wrapper:234-271`: `NUL,outWrite,errWrite` được ghi vào list trước `CreateProcessW`, list/nul giải phóng sau call, parent đóng hai write ends ở `:271`. `review-handle-probe.ps1` chạy child `python -c 'sys.stdin.read()'` ⇒ gốc `resumed=True exited=True rc=0 stdout=EOF`; ca z1 trong suite `33/0` có deadline pipe 90 s. | **KHÔNG PHẢI LỖI** trên fixture NUL/stdout; không suy toàn bộ handle đang mở đã được quan sát. |
| **H6.** Case z chỉ có tên hoặc được tính dù không chạy. | `Tests:1179` bọc `$IsWindows`; `:1183-1190` yêu cầu anchor projection đúng một lần; `:1214-1233` kiểm z1 có con sống, record, takeover; `:1239-1256` kiểm z2 flag và một stage call; `$cases++` ở `:1262`. Suite native Windows `passed=33 failed=0` rc0. | **KHÔNG PHẢI LỖI**: z thực chạy và kiểm hai nhánh; `33` là số case, không phải số assertion. |
| **H7.** Claim `diff --check rc0` có thể chỉ đúng khi lọc path. | `git diff --check ed12889 505a483 -- <sáu>` rc0; `git diff --check 8c98afa 505a483 -- <sáu>` rc0; `git diff --check 8c98afa 505a483` rc2, output trailing whitespace tại các `ops/reviews/*HINT.patch`. | **LỖI phạm vi lời khai** nếu hiểu là toàn PR; sáu path của lease sạch. Không quy whitespace merge cho bốn tệp g5. |
| **H8.** Manifest helper có thể bỏ wrapper mới hoặc negative probe r209 trở thành vacuous. | Python trực tiếp `_build_release_manifest`/`_doc_pointer_findings`: `files 183 new_script True docs 36`, `pointers_ok True fail 0 advisory 107 baseline 3`; tài liệu RUNBOOK trong RAM chỉ đến `scripts/no_such_wp710_file.py` ⇒ `negative_ok False`, đúng một fail. | **KHÔNG PHẢI LỖI** ở helper; tám assertion trong full selftest chưa đo được. |

## FINDING THEO LỚP

### khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con  [P2]  Job rỗng còn mở có thể xoá record của con ngoài Job

TỆP/DÒNG: `scripts/nlm-credential-refresh.ps1:360-361,502-513,525-533,655-667,559-566`.

VẤN ĐỀ: G5 giữ bản ghi `_alive` và gọi `Get-Process -Id $childId`; `Write-OperationRecord` chỉ ghi PID/ticks nếu Get-Process trả đối tượng, còn `Get-StartTicks` được phép trả null. `Test-RecordedRootAlive` coi thiếu một trong hai là không có bằng chứng root. Nếu **một tiến trình khác còn giữ handle của Job rỗng**, `Get-RecordVerdict` trả `clear` ngay cả khi con treo sống **ngoài** Job; chủ mới xoá record và có thể bắt đầu refresh/stage. Khi handle Job cuối đóng như đường g5 thông thường, cùng state trả `quarantine`; không quy lỗi cho lối đó. Đây là lỗi logic có điều kiện ở head; sự đồng thời của lỗi đọc `StartTime` và holder ngoài wrapper chưa đo được trong vận hành thật.

ĐÃ THỬ VÁ: có — g5 đã sửa nhánh `_alive` giữ record/PID; hướng sửa còn lại: lưu PID nguyên thủy từ `Start` kể cả khi `Get-Process` thất bại, giữ trạng thái không xác nhận khi thiếu ticks, và không dùng ActiveProcesses=0 của Job làm chứng cứ cho con đã biết nằm ngoài Job. Cần ca test ép null process/ticks trong khi con ngoài Job vẫn sống, **giữ thêm một handle Job** và kiểm chủ kế không stage; đối chứng đóng handle cuối phải vẫn cách ly.

ĐÃ THỬ NGHIỆM: `pwsh -NoProfile -File review-probe.ps1` trên hàm/C# trích đúng head, với child Python đang ngủ **ngoài Job** và record mô phỏng nhánh `_alive`: giữ Job mở ⇒ `fixture_alive=True ... start_ticks=null ... job_probe=0 job_active=0 verdict=clear`; đóng Job ⇒ `fixture_alive=True job_probe=1 verdict=quarantine reason=job_closed_unconfirmed`. Probe không tạo chính con treo của `Job.Start`; suite Windows `33/0` chỉ phủ record có PID/ticks. Trigger hai điều kiện từ OS/holder thật: **KHÔNG ĐO ĐƯỢC**.

ĐỘ TIN: cao về logic của state phản chứng, thấp về tần suất kích hoạt vận hành.

### stdin-nul-chua-duoc-khoa-bang-test  [P3]  Suite không phát hiện stdin không còn là NUL

TỆP/DÒNG: `scripts/nlm-credential-refresh.Tests.ps1:13-202,229-249,1169-1263`; `scripts/nlm-credential-refresh.ps1:254-260`.

VẤN ĐỀ: RUNBOOK `:824-826` và comment mã nói child có `NUL` stdin. Ca z1 chỉ xem ống stdout của caller có đóng. Mutant đổi stdin sang handle `outWrite` vẫn biên dịch và làm một child đọc stdin thất bại, song toàn suite vẫn xanh. Đây là lỗ nghiệm thu của test, **không phải biểu hiện runtime lỗi ở g5**.

ĐÃ THỬ VÁ: có — `HINT.patch` thêm fake mode `stdin_eof` và ca test chỉ trên Windows (test thuần, không sửa runtime); Executor phải tự áp/đo/cập nhật con số suite trong tài liệu sau khi vá P2.

ĐÃ THỬ NGHIỆM: mutant C# compile PASS; direct probe gốc `rc0/EOF`, mutant `rc1/no stdout`; suite hiện hành cả hai `33/0`. Bản sao áp hint trên mutant đỏ rc1 đúng câu `the child stdin must be readable EOF from NUL`; bản sao áp hint trên gốc `passed=34 failed=0`, rc0. Đây là đối chứng target/non-target của chính ca mới.

ĐỘ TIN: cao.

### khai-rong-hon-phep-do-trong-changelog-runbook  [P3]  Tổng quan Job còn hứa rc 5 sau stage

TỆP/DÒNG: `changelog.d/wp-710.md:60-63,74-97`; `references/RUNBOOK.md:749,752,803-807`; thân commit g5 phần `git diff --check`.

VẤN ĐỀ: Bảng kết quả mới nói stage đã chạy và Job count không đọc được là `stage_failure` rc 6; đoạn giải thích Job ở hai tệp vẫn nói mọi count không về 0 là `tree_containment` rc 5. Người vận hành có thể hiểu nhầm khả năng đã upload. Claim `git diff --check rc0` trong commit không ghim sáu path; phép full PR rc 2 do merge, chỉ scope sáu path rc 0. Các số 13 phút, 2,9/7,0 giây, 34 Linux và 3 mutant không có phép tái lập trong bundle; giữ `KHÔNG ĐO ĐƯỢC`, không xem đó là lỗi code.

ĐÃ THỬ VÁ: có — g5 sửa bảng status nhưng bỏ đoạn tổng quan. `HINT.patch` chỉ gợi ý sửa đúng hai đoạn tài liệu; không chỉnh commit lịch sử.

ĐÃ THỬ NGHIỆM: `rg`/đối chiếu dòng như H3; `git diff --check` hai scope như H7. Hint `git apply --check -p0` rc0 trên hai bản sao; `patch.exe --dry-run` bị sandbox từ chối `CreateFileMapping ... Win32 error 5`, không suy là patch hỏng.

ĐỘ TIN: cao về mâu thuẫn; thấp về các số lịch sử không có rig.

### huong-dan-cu-con-lech-sau-va-ngoai-write-set  [P3]  Hướng dẫn cũ còn nguyên ngoài lease

TỆP/DÒNG: `scripts/tl_core/cli.py:145`; `scripts/nlm-auto-refresh.sh:76-85`; `references/COWORK_PROJECT.md:83,94`; `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`.

VẤN ĐỀ: help/flow cũ còn chỉ `nlm login`/`login --check` và shell nuốt rc stage, lệch đường refresh/canary mới. Bốn path này ngoài sáu path của WP710; Executor g5 không có quyền sửa trong Packet này.

ĐÃ THỬ VÁ: không trong head này; cần Packet khác có owner/write set riêng.

ĐÃ THỬ NGHIỆM: `git diff ed12889 505a483 -- <bốn path>` rỗng; `rg` cho các dòng nêu trên. Không chạy LIVE.

ĐỘ TIN: cao.

## ĐẾM LỚP MỞ

| loại | P1 | P2 | P3 | tổng |
|---|---:|---:|---:|---:|
| finding có biểu hiện sai ở head | 0 | 1 | 3 | 4 |
| lớp lịch sử chưa đủ phép đo để tuyên bố đóng, **không nâng thành finding mới** | 0 | 2 | 0 | 2 |
| tổng lớp chưa đóng hoặc chưa nghiệm thu | 0 | 3 | 3 | 6 |

Hai lớp lịch sử thiếu Linux là `stage-canary-true-khi-than-rong-hoac-sai-id` và `linux-subreaper-khong-thu-hoi-zombie`. Ba lớp trong sáu tệp có finding hành động là P2 Job còn mở, P3 stdin test, P3 tài liệu; P3 hướng dẫn cũ nằm ngoài write set và cần Packet khác. Ngưỡng `approve` chặt hơn của `PROMPT.md` (không còn P1/P2/P3 trong sáu tệp) chưa đạt.

## HINT.patch

Tệp hint chỉ đổi `scripts/nlm-credential-refresh.Tests.ps1`, `references/RUNBOOK.md`, `changelog.d/wp-710.md`; dòng đầu mang đúng nhãn reviewer. `git apply --check -p0 --directory=review-hint-original --unsafe-paths HINT.patch` và tương tự trên `review-hint-mutant` đều rc0; `git apply` thật lên hai bản sao đều rc0. Trên bản sao có hint, mutant đỏ rc1 đúng ca `stdin` mới, gốc xanh `passed=34 failed=0` rc0. `patch -p0 --fuzz=0 --dry-run` đã thử trên bản sao nhưng `patch.exe` của Git for Windows dừng ở `CreateFileMapping ... Win32 error 5` do sandbox trước khi đọc patch; tính tương thích của đúng executable này **KHÔNG ĐO ĐƯỢC**. Nếu Executor áp hint, số suite trong changelog cần được đo lại/cập nhật (hiện tài liệu ghi 33 trên head đã review). Hint chưa chạy trên cây thật; Executor tự áp, tự đo và tự chịu trách nhiệm commit.

## TRẠNG THÁI CHECKOUT CUỐI

`git -C cay-kho status --porcelain=v1 --untracked-files=all` → output rỗng, rc0. `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'` → `505a483e50bef5f84e4403ef0a1cb2277d32d4ac` / `20a5a743682e7912f7274415ba012f836272caa8`. `git diff --quiet` và `git diff --cached --quiet` đều rc0. Không để lại thay đổi trong `cay-kho`.

Các bản sao/probe `review-*` còn ở gốc sandbox. Đã kiểm chúng đều nằm trong `C:\Users\admin\cw\rv5`; công cụ tự động từ chối cả `Remove-Item` với đường dẫn tuyệt đối của một tệp scratch và một thư mục scratch, trả `Rejected ... blocked by policy`, không nêu lý do chi tiết. Không chuyển sang shell khác để xoá. Bốn thư mục temp của suite không còn tệp record `tra_luat_nlm_credential_refresh.operation.json`.
