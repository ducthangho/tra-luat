verdict: changes_requested
reviewed_sha: cde2ef434d28ec3de20df47913b3d3cd97b097de
reviewed_tree: 5aecfa11a63f3baa59e277db41b1b1772ec2a09e
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: OpenAI (tự khai)
reviewer_model: KHÔNG ĐO ĐƯỢC (runtime không cấp bằng chứng model)

Review độc lập, chỉ đọc/ghi trong sandbox. Không gọi mạng, CLI `nlm` thật, Drive, hay đọc credential. `changes_requested` vì hai lớp P3 còn mở **trong sáu tệp write set**: suite không khóa nhánh lookup PID thất bại và các lời khai ở tài liệu/chú thích rộng hơn đường mã thực tế. P2 về Job rỗng của lượt trước đã được vá trên head này. Không cấp lease, admission, LIVE, approval hay land authority.

## ĐỐI CHIẾU LƯỢT TRƯỚC

`Get-FileHash -Algorithm SHA256 SPEC.md,VERDICT_LUOT_TRUOC.md` → lần lượt `A51164CF4BB0B3F41D4C01EF56A522C339CAAC008F2D855B3819A3EBB642BC0B`, `FE814DF21FA013E148AE7DA3C02A5F600AFF5BAB38E3E4B391FF1EA823ADF96D`, khớp PROMPT. `git -C cay-kho diff --numstat 505a483 cde2ef4 -- <sáu path>` → changelog `7/5`, RUNBOOK `4/3`, Tests `45/2`, wrapper `13/2`; hai tệp Python không đổi. `git -C cay-kho apply --reverse --check -p0 ../HINT_LUOT_TRUOC.patch` → rc 0.

| slug lớp cũ | phân loại | lệnh và output tự đo trên head mới |
|---|---|---|
| `khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con` [P2] | **ĐÃ VÁ THẬT** ở biểu hiện lượt trước | Wrapper `:513-519` ghi `outside_job=true` và PID từ `CreateProcess` cả khi lookup null; `:565-569` xử lý trước Job. Probe hàm với process null → `pid=4242 outside_job=True`; ca z1 với con sống + `start_ticks=null` + holder Job rỗng chạy trong suite `passed=34 failed=0`, rc 0, kiểm `tree_quarantine/stray_child_unconfirmed`. Đột biến mới cho thấy vẫn có lỗ test nhánh lookup null, ghi finding riêng; không quy mutant là lỗi runtime ở head. |
| `stage-da-goi-nhung-bao-inconclusive` [P2 lịch sử đã đóng lượt 5] | **ĐÃ VÁ THẬT** đối với đường `ran` đã kiểm | `rg -n 'ran=\$true|Exit-IfBlocked|stage.timeout'` → wrapper `:711,:798,:930-942,:1041-1047`; ca z2 `Tests:1282-1305` kiểm một stage call và rc 6/`stage_failure`, suite `34/0`. Đường ngoại lệ **trước** khi tạo con trả `stage_failure` với 0 call là vấn đề lời khai khác, không phải lỗi “đã gọi nhưng báo inconclusive”. |
| `stdin-nul-chua-duoc-khoa-bang-test` [P3] | **ĐÃ VÁ THẬT** trên Windows | Hunk test cũ có trên head (reverse-check rc 0). Suite gốc `34/0` rc 0. Bản sao đổi `si.Info.hStdInput = nul` → `outWrite`, C# biên dịch `Add-Type -WarningAction Stop -ErrorAction Stop` PASS; suite đỏ rc 1 đúng `Tests.ps1:263: the child stdin must be readable EOF from NUL`. |
| `khai-rong-hon-phep-do-trong-changelog-runbook` [P3] | **VÁ HỜ** | Hai đoạn Job cũ đã phân biệt trước/sau stage tại changelog `:60-63`, RUNBOOK `:803-808`; claim `diff --check` của commit nay ghim bốn tệp. Nhưng projection ngoại lệ trước khi tạo child cho `rc=6 stage_failure stage_calls=0`, ngược changelog `:99`/RUNBOOK `:752` nói stage đã được gọi; wrapper `:671-673` còn nói `root_alive` cả trường hợp thiếu ticks; `tl_gws.py:1747` nói chỉ hỏi sự tồn tại jar trước canary dù `_nlm_auth_files` đọc nội dung. Chi tiết ở finding. |
| `huong-dan-cu-con-lech-sau-va-ngoai-write-set` [P3] | **CHƯA VÁ** | `git diff 505a483 cde2ef4 -- <bốn path cũ>` rỗng; `rg -n 'nlm login|login --check|nlm-auth-stage'` vẫn thấy `scripts/tl_core/cli.py:145`, `scripts/nlm-auto-refresh.sh:76-85`, `references/COWORK_PROJECT.md:83,94`, `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`. **Ngoài sáu tệp lease; cần Packet khác.** |
| `stage-canary-true-khi-than-rong-hoac-sai-id` [P2 lịch sử thiếu phép đo] | **VÁ HỜ / chưa đóng độc lập** | Hai tệp Python không đổi giữa hai head; suite Windows `34/0` và probe thân hàm `force=True`: True→rc0/upload1, False/None→rc4/upload0. Full Python selftest dừng do sandbox trước tổng kết; hai phép parity Linux `101/168` chưa đo được. Không thấy biểu hiện mã sai mới; không nâng thiếu đo thành finding. |
| `linux-subreaper-khong-thu-hoi-zombie` [P2 lịch sử thiếu phép đo] | **CHƯA VÁ / KHÔNG ĐO ĐƯỢC** | Mã Linux không đổi; `wsl.exe -d Ubuntu-Clean -u root -- pwd` → `Access is denied. Error code: Wsl/Service/E_ACCESSDENIED`, rc -1. Không đo được bốn chu kỳ zombie hoặc Linux suite; không suy từ lời Executor. |

Các hướng săn cũ chưa đo: user/phiên Windows thứ hai, lỗi Job API do OS thật và ma trận quote/backslash đầy đủ vẫn **KHÔNG ĐO ĐƯỢC**. `chay-linux.sh` không chạy được vì WSL bị chặn; script còn ghi `/root`, `/opt`, `/tmp` ngoài phạm vi đọc/ghi được giao. Handle NUL nay được đo sâu hơn bằng đột biến biên dịch được và suite đỏ đúng ca. C# bản sao các đột biến đều đã kiểm biên dịch cảnh báo-là-lỗi trước khi tính kết quả; không nhận `job_api_unavailable` do lỗi compile làm tín dụng.

## SPEC r4

| mục | đạt / một phần / chưa đạt / KHÔNG ĐO ĐƯỢC | căn cứ |
|---|---|---|
| 1 | một phần | Suite fake Windows `34/0` có thứ tự và timeout; CLI, browser profile, fingerprint LIVE chưa đo. |
| 2 | một phần | Canary fake trong suite; parity `101` dạng/`168` byte Linux và notebook thật KHÔNG ĐO ĐƯỢC. |
| 3 | một phần | Probe cô lập đúng thân hàm với `force=True` cho True→1 upload, False/None→0; command-level `tl nlm-auth-stage`/full selftest không đo được vì temp sandbox. |
| 4 | một phần | Windows suite xanh, NUL mutant đỏ; mutation lookup null **sống sót** `34/0`, nên nhánh bản ghi đó chưa được suite khóa. |
| 5 | một phần | Ca z2 cho stage đã chạy→rc6. Ngoại lệ trước khi tạo con cũng cho rc6 với 0 call; tài liệu hiện diễn giải sai ranh giới này. |
| 6 | một phần | z1 đo Job rỗng/con ngoài Job còn sống và chủ kế không stage; holder/user/phiên thứ hai ngoài fixture, API OS tự lỗi chưa đo. |
| 7 | một phần | Manifest ứng viên `183` file có wrapper, pointer fail `0`, advisory `107`, baseline `3`; con trỏ giả bị bắt. Tám assertion r209 hiện diện ở `tl_selftest.py:21616-21662`, nhưng full selftest bị sandbox chặn. |
| 8 | KHÔNG ĐO ĐƯỢC | Targeted Windows/scan/diff có rc độc lập; full Python gate, Linux, CI/admission/GitHub required gates, LIVE và land không có phép đo hợp lệ trong sandbox. |

## BẢNG ĐO

`KHÔNG ĐO ĐƯỢC` không có nghĩa là sản phẩm sai. Các số lịch sử khác của RUNBOOK (như `60/60/30`, `101/101`, `9/9`, `2/2`, `14/14`, thông lượng và thời gian GWS) không có rig/đầu vào trong bundle; không xác nhận lại chúng từ recall.

| khẳng định | PR/Executor khai | đo được | khớp? |
|---|---|---|---|
| Head/tree/spec/verdict trước | SHA trong PROMPT/EVIDENCE | HEAD `cde2ef434d28ec3de20df47913b3d3cd97b097de`, tree `5aecfa11a63f3baa59e277db41b1b1772ec2a09e`; hai hash tệp khớp | khớp |
| Phạm vi g5 | bốn tệp đổi, hai Python không đổi | `git diff --numstat 505a483 cde2ef4 -- <sáu>` → `7/5,4/3,45/2,13/2`; `git diff --name-only 8c98afa cde2ef4` có `162` path, giao write set đúng `6` | khớp |
| Windows suite | `34 passed, 0 failed`, rc0, `8m47s` | `passed=34 failed=0`, rc0; `pwsh 7.6.6`, Python `3.13.1`; không có stopwatch độc lập | số/rc khớp; thời gian KHÔNG ĐO ĐƯỢC |
| Linux suite | `34/0`, rc0, `1082s`, WSL pwsh7.4.6 | `wsl.exe ... pwd` bị `Wsl/Service/E_ACCESSDENIED` rc -1 | KHÔNG ĐO ĐƯỢC |
| Hai mutant Executor H1/H2 | cả hai đỏ đúng ca | H2 stdin tự dựng lại: compile PASS, suite rc1 đúng câu NUL; H1 của `mut6.py` không chạy vì script tự dọn tiến trình Python toàn máy và temp người dùng, trái phạm vi. Mutant riêng lookup null: compile PASS nhưng suite `34/0` | H2 khớp; H1 KHÔNG ĐO ĐƯỢC; tìm thêm lỗ test |
| Selftest Python | `1728/1728`, rc0 | `python cay-kho/scripts/tl.py --selftest` với `TEMP/TMP/TMPDIR` trong sandbox rc1 ở `tl_selftest.py:346`: `PermissionError [WinError 5]` tạo `selftest-r3`; probe `tempfile.mkdtemp()→mkdir child` cũng rc1 | KHÔNG ĐO ĐƯỢC do sandbox |
| `diff --check` và secret scan | rc0 trong bốn tệp/ sáu tệp | `git diff --check 8c98afa cde2ef4 -- <sáu>` rc0; full PR rc2 với 66 dòng báo whitespace ở `ops/reviews/` từ merge; `pkg_secret_scan.py` trên sáu bản sao rc0/output rỗng | khớp khi ghi rõ scope |
| HINT lượt trước | áp không sửa tay | `git apply --reverse --check -p0` trên head rc0 | khớp ba hunk; thao tác executor lịch sử không quan sát trực tiếp |
| Manifest/pointer | `183`, fail0/advisory107/baseline3 | `python review-manifest-probe.py` → `files=183 wrapper_included=True docs=36 pointers_ok=True fail=0 advisory=107 baseline=3`; pointer giả → `negative_ok=False negative_fail=1` | khớp helper; tám assertion full selftest KHÔNG ĐO ĐƯỢC |
| Stage body `--force` | True→upload1, False/None→0 | `python review-stage-probe.py` → True rc0/1, False rc4/0, None rc4/0; True+jar vắng rc3/0. Đây là AST hai hàm với dependency giả trong RAM | khớp thân hàm; command-level KHÔNG ĐO ĐƯỢC |
| Bản ghi con ngoài Job | PID luôn từ CreateProcess; `outside_job` kể cả lookup null | Probe hàm gốc process null → `pid=4242 outside_job=True`; mutant bỏ nhánh đó → `pid= outside_job=`; z1 suite gốc xanh | khớp mã; suite thiếu riêng nhánh null |
| Các ngưỡng số WP710 trong RUNBOOK/comment | timeout 120 s, lock wait 10 s, interval 3600 s, 1 cycle mặc định, quarantine 900 s, fingerprint 16 hex, lý do thả tay 8–200 ký tự, Job đợi tối đa 5 s | Đối chiếu wrapper `:12-19,:631,:962,:971` cho đúng các hằng/điều kiện; suite fake chỉ phủ một số giá trị rút ngắn, không đo đủ các mốc thời gian mặc định | khớp mã tĩnh; hành vi đủ thời gian KHÔNG ĐO ĐƯỢC |
| Lời khai `stage_failure` | stage command đã được gọi/có thể upload | Projection lỗi trước tạo con → `rc=6 status=stage_failure stage_calls=0`; log chỉ `--version`, `auth refresh`, `notebook get ...` | **lệch** ở changelog/RUNBOOK |
| Chú thích đọc jar | chỉ hỏi có jar; bytes sau canary | `_nlm_auth_files` tại `tl_gws.py:737-753` đọc file; probe thứ tự canary False: `read_files,canary`, upload0; True: `read_files,canary,read_files,upload` | **lệch chú thích**, upload gate vẫn đúng trong probe |
| Số lịch sử ở changelog/RUNBOOK/comment | 13 phút pipe; drift 2,9s/130s và 7,0s/256s; parity101/168; zombie 4 chu kỳ; số liệu GWS cũ | không có rig/lượt WSL độc lập; không tái lập 13 phút hay dữ liệu GWS | KHÔNG ĐO ĐƯỢC |
| LIVE/lease/admission/CI | Executor tự khai chưa làm hoặc không có receipt | không gọi mạng/LIVE, không có receipt độc lập trong bundle | `not_measured`; không suy `passed` |

## BẢNG SĂN

Các hướng dưới đây tách theo cơ chế. H3/H7 đi sâu hơn lượt trước nhờ ca mới hoặc đối chứng đột biến trên head này; các hướng khác là mới.

| hướng: giả thuyết | lệnh / output thật | kết luận |
|---|---|---|
| **S1.** Lookup process thất bại trong nhánh `*_alive` làm bản ghi mất PID/cờ mà suite vẫn xanh. | Bản sao đổi `if ($strayPid -gt 0)`→`if ($strayPid -gt 0 -and $process)` (anchor 1), C# compile PASS; `review-pid-probe.ps1` gốc `pid=4242 outside_job=True`, mutant `pid= outside_job=`; full suite mutant `passed=34 failed=0`, rc0. | **LỖI TEST** ở nhánh lookup null; mã head hiện đúng. |
| **S2.** Ngoại lệ trước khi con stage sinh ra vẫn bị catch chung gọi `stage_failure`, trái câu “đã được gọi”. | `pwsh -File review-stage-exception-probe.ps1` (CLI giả, projection throw trước spawn) → log `--version/auth refresh/notebook get`, `rc=6 status=stage_failure step=stage stage_calls=0`. Wrapper `:1041-1042`. | **LỖI lời khai tài liệu**, không phải upload sai. Lỗi OS/disk thật chưa đo. |
| **S3.** Handle list/NUL có thể chỉ hiện trong mã mà stdin không dùng được; test mới có bắt hồi quy không? | `rg` cho ba `Marshal.WriteIntPtr` tại wrapper `:246-248`, NUL/stdout/stderr tại `:257`, giải phóng list/nul sau `CreateProcess` `:266-271`. Suite gốc `34/0`; mutant NUL→`outWrite` C# compile PASS, suite rc1 đúng `the child stdin must be readable EOF from NUL`. | **KHÔNG PHẢI LỖI** ở head Windows đã đo. |
| **S4.** Bản ghi JSON hỏng có thể fail-open khi chủ mới lấy mutex. | `pwsh -File review-bad-record-probe.ps1` (temp trong sandbox, CLI giả) → `rc=5 status=inconclusive step=lock_busy reason=record_unreadable calls=0`. | **KHÔNG PHẢI LỖI** trên fixture; bản ghi được giữ. |
| **S5.** Tiền kiểm stage có thể đọc bytes credential trước canary, trái chú thích. | `rg -n '^def _nlm_auth_files|open\(p|if not _nlm_auth_files' tl_gws.py` → `:737,:747,:1747`; probe AST với fake trả canary False: `events=read_files,canary`, rc4/upload0; True: `read_files,canary,read_files,upload`. | **LỖI chú thích/diễn giải**. Không đọc credential thật; upload sau canary dương ở probe. |
| **S6.** `--force` hoặc jar biến mất sau canary có thể bypass cổng và upload. | `python review-stage-probe.py` → `force=True canary=False/None` đều rc4/upload0; `canary=True jar=absent` rc3/upload0; True+jar có rc0/upload1. | **KHÔNG PHẢI LỖI** ở hai hàm đã đo; command-level chưa đo. |
| **S7.** Ca z mới chỉ tăng số `passed` mà không có holder Job rỗng/con sống thật. | Đọc `Tests:1233-1266`: kiểm PID còn sống, `empty-job.ready` bằng `0`, holder chưa thoát, record `start_ticks=null`, rc5/`stray_child_unconfirmed`/0 calls; suite Windows `34/0`. Mutation S1 vẫn sống vì fixture không ép `Get-Process` null. | **KHÔNG PHẢI LỖI** cho tình huống z đã dựng; có lỗ khác S1. |
| **S8.** Claim `diff --check rc0` có thể lại không ghim scope. | Commit body ghi rõ bốn tệp; `git diff --check 8c98afa cde2ef4 -- <sáu>` rc0; full PR rc2/66 dòng ở `ops/reviews/`. | **KHÔNG PHẢI LỖI** ở claim đã giới hạn; full PR vẫn không sạch do merge, không quy cho bốn tệp g5. |
| **S9.** Linux-only và hai user có thể lộ đường khác. | `wsl.exe -d Ubuntu-Clean -u root -- pwd` → `Wsl/Service/E_ACCESSDENIED`, rc -1; không có fixture user/phiên Windows thứ hai. | **KHÔNG ĐO ĐƯỢC**. |

## FINDING THEO LỚP

### lookup-null-khong-duoc-suite-khoa  [P3]  Suite không ép lookup null của con treo ngoài Job

TỆP/DÒNG: `scripts/nlm-credential-refresh.Tests.ps1:1186-1307`; liên hệ runtime `scripts/nlm-credential-refresh.ps1:513-519,669-678`.

VẤN ĐỀ: Head hiện **có mã đúng**: `outside_job=true` và PID từ `CreateProcess` ngay cả khi `Get-Process` trả null. Nhưng ca z1 lấy process thật thành công, rồi chỉ tự sửa `start_ticks=null` ở record; nó không kiểm chính lúc **ghi** record với `$process=$null`. Mutant điều kiện ghi cờ chỉ khi process lookup thành công làm mất PID/cờ ở trường hợp đó, vẫn qua toàn suite `34/0`. Nếu hồi quy ấy xuất hiện, Job rỗng được holder khác giữ mở lại có thể xóa record như P2 lượt trước. Đây là lỗ test, không phải biểu hiện sản phẩm lỗi ở head này.

ĐÃ THỬ VÁ: có — `HINT.patch` chỉ thêm test thuần: gọi đúng `Write-OperationRecord` được trích từ wrapper với process null và PID 4242, đòi PID/cờ/`tree_unconfirmed`. Executor tự áp, tự chạy suite trên head mới và thử mutant để kiểm hint.

ĐÃ THỬ NGHIỆM: mutant bản sao anchor=1, C# warning-as-error PASS; probe hàm gốc `pid=4242 outside_job=True`, mutant `pid= outside_job=`; suite mutant `passed=34 failed=0` rc0. `HINT.patch` áp bản sao bằng `git apply` rc0, PowerShell parse errors 0. Chạy đúng block test mới đã áp, riêng trên hai nguồn: head `hint_unit=PASS`/rc0, mutant rc1 đúng câu `a failed process lookup must keep the stray PID and outside-job flag`. **Chưa chạy full suite trên bản sao có hint**. `patch.exe --dry-run` bị sandbox từ chối trước khi đọc patch, ghi riêng dưới.

ĐỘ TIN: cao về lỗ test; không khẳng định lỗi runtime hiện tại.

### khai-rong-hon-phep-do-trong-changelog-runbook  [P3]  Ba lời mô tả tuyệt đối còn lệch các nhánh đã đo

TỆP/DÒNG: `changelog.d/wp-710.md:99`; `references/RUNBOOK.md:752`; `scripts/nlm-credential-refresh.ps1:671-673`; `scripts/tl_gws.py:737-753,1747`.

VẤN ĐỀ: Hai đoạn tổng quan Job của lượt trước đã sửa đúng, nhưng ba câu còn rộng hơn mã. (1) RUNBOOK/changelog nói `stage_failure` nghĩa là lệnh stage **đã được gọi**; catch `Invoke-Bounded` tại wrapper `:1041-1042` cũng trả rc6 khi ngoại lệ xảy ra trước spawn. Projection đã cho `stage_calls=0`. (2) Chú thích wrapper nói chủ kế đợi `root_alive` cho con `_alive`; thiếu `start_ticks` thì `Test-RecordedRootAlive` trả null và `Get-RecordVerdict` trả `stray_child_unconfirmed`, được chính z1 mới kiểm. (3) Chú thích `tl_gws.py:1747` nói tiền kiểm chỉ hỏi “CÓ jar”, bytes để sau canary; `_nlm_auth_files()` thật mở/đọc file auth trước canary rồi đọc lại sau canary dương. Đây là sai lời giải thích, **không** phải bằng chứng upload khi canary âm. Các số lịch sử thiếu rig không tính là lỗi chỉ vì chưa đo.

ĐÃ THỬ VÁ: có — `HINT.patch` sửa câu stage_failure ở RUNBOOK/changelog cho phép ngoại lệ trước tạo con và 0 call. Với hai chú thích trong runtime/Python nhạy cảm, chỉ mô tả hướng: ghi đúng điều kiện `root_alive` khi có ticks, và nói rõ preflight có đọc jar trong RAM rồi bỏ, còn payload được đọc lại sau canary; hoặc đổi tiền kiểm sang kiểm tồn tại thật sự nếu muốn giữ bất biến “không đọc trước canary”. Executor chọn và tự đo; hint không vá hai tệp đó.

ĐÃ THỬ NGHIỆM: `review-stage-exception-probe.ps1` → rc6/stage_calls0; case z1 trong suite `34/0` kiểm `stray_child_unconfirmed`; `review-stage-probe.py` → `read_files,canary` khi False, không upload. Hint `git apply --check`/apply trên bản sao rc0; không có lỗi parse test. Lỗi OS/disk thật và credential thật **KHÔNG ĐO ĐƯỢC**.

ĐỘ TIN: cao về đường mã và lời khai lệch; không suy tần suất ngoại lệ thật.

### huong-dan-cu-con-lech-sau-va-ngoai-write-set  [P3]  Hướng dẫn cũ còn chỉ đăng nhập và nuốt rc stage

TỆP/DÒNG: `scripts/tl_core/cli.py:145`; `scripts/nlm-auto-refresh.sh:76-85`; `references/COWORK_PROJECT.md:83,94`; `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`.

VẤN ĐỀ: Những path ngoài lease vẫn chỉ `nlm login`/`login --check`, hoặc nuốt rc của `nlm-auth-stage`, lệch workflow refresh/canary hiện hành. Không quy cho Executor g5 vì **ngoài sáu tệp write set**; cần Packet khác với owner/write set riêng.

ĐÃ THỬ VÁ: không trong Packet này; mô tả hướng: cập nhật help/flow cũ và để lỗi stage hiện rõ dưới một Packet mới.

ĐÃ THỬ NGHIỆM: `git diff 505a483 cde2ef4 -- <bốn path>` rỗng; `rg` ở BẢNG ĐỐI CHIẾU còn các dòng chỉ dẫn cũ. Không chạy LIVE.

ĐỘ TIN: cao.

## ĐẾM LỚP MỞ

| loại | P1 | P2 | P3 | tổng |
|---|---:|---:|---:|---:|
| finding có biểu hiện sai ở head, trong sáu tệp | 0 | 0 | 2 | 2 |
| finding ngoài sáu tệp, cần Packet khác | 0 | 0 | 1 | 1 |
| lớp lịch sử thiếu phép đo để tuyên bố đóng, **không nâng thành finding** | 0 | 2 | 0 | 2 |
| tổng lớp còn mở hoặc chưa nghiệm thu | 0 | 2 | 3 | 5 |

Hai lớp lịch sử thiếu đo là `stage-canary-true-khi-than-rong-hoac-sai-id` và `linux-subreaper-khong-thu-hoi-zombie`. Ngưỡng `approve` của PROMPT không đạt vì còn hai P3 nằm trong sáu path.

## HINT.patch

Dòng đầu đúng nhãn bắt buộc. Patch chỉ gồm `scripts/nlm-credential-refresh.Tests.ps1`, `references/RUNBOOK.md`, `changelog.d/wp-710.md`, đường dẫn repo-relative không tiền tố `a/`/`b/`. Đã copy ba tệp vào `review-hint-dry2/`, thử `patch -p0 --fuzz=0 --dry-run -d <bản sao> -i HINT.patch`: `patch.exe` dừng trước khi đọc patch với `CreateFileMapping ... Win32 error 5` (rc 256), nên phép thử **KHÔNG ĐO ĐƯỢC do sandbox**. `git apply --check -p0` rc0 và `git apply -p0` thật trên cùng bản sao rc0; PowerShell parser báo 0 lỗi. Block test mới trong bản sao đã chạy head rc0 và mutant rc1 đúng câu đích; full suite với hint chưa chạy. Hint chưa chạy trên cây thật; Executor tự áp, tự đo, tự chịu trách nhiệm commit.

## TRẠNG THÁI CHECKOUT CUỐI

`git -C cay-kho status --porcelain=v1 --untracked-files=all` → **output rỗng**, rc0. `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'` → `cde2ef434d28ec3de20df47913b3d3cd97b097de` / `5aecfa11a63f3baa59e277db41b1b1772ec2a09e`. Không để lại thay đổi trong `cay-kho/`. Các bản sao/probe độc lập nằm ở gốc sandbox để tái lập; không có CLI LIVE hay credential được dùng.
