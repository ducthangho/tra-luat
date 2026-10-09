verdict: changes_requested
reviewed_sha: 5e9fd9247fa2e54f0b41b835c4bf01aeb1050a19
reviewed_tree: d43ad4ced6440d4a2ec94c60ea935ac92b574961
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: openai_codex (tự khai)
reviewer_model: GPT-6 (tự khai; runtime attestation KHÔNG ĐO ĐƯỢC)
reviewer_execution_surface: Codex local sandbox (tự khai)
reviewer_transport: local tools (tự khai)

`changes_requested`: suite Windows độc lập xanh, nhưng bản sửa RUNBOOK tạo một mâu thuẫn P3 trong sáu tệp write set. Lớp hướng dẫn cũ ngoài write set cần Packet khác. Không suy assurance, admission, CI, LIVE, lease hay land authority từ verdict này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

`Get-FileHash -Algorithm SHA256 SPEC.md,VERDICT_LUOT_TRUOC.md` → `A51164CF4BB0B3F41D4C01EF56A522C339CAAC008F2D855B3819A3EBB642BC0B` và `02F7F76E33D18B4F397DCCFBA98EFBF1287FF7DFDCE8744B69581930487DEC08`, khớp PROMPT. `git -C cay-kho show -s --format='%H %P' HEAD` → head này có **parent trực tiếp** `a5464c3e84c9ef0ce4aec99e81749b2611976def`; không có merge giữa hai head như PROMPT mô tả. `git diff --stat a5464c3 5e9fd92 -- <sáu path>` → changelog `4 +++-`, RUNBOOK `17 +++++++++++------`; numstat lần lượt `3/1` và `11/6`, bốn path khác không đổi. Áp `HINT_LUOT_TRUOC.patch` lên hai blob cũ trong `review-hint-copy/` rồi so với blob head sau chuẩn hóa CRLF/LF → cả hai `True`; không thấy hunk thêm.

| slug lớp trước | phân loại trên head này | lệnh / output tự đo |
|---|---|---|
| `khai-rong-hon-phep-do-trong-changelog-runbook` [P3] | **ĐÃ VÁ THẬT** | `diff-tu-luot-truoc.patch` và văn bản head: changelog mô tả tiền kiểm đọc jar rồi bỏ, RUNBOOK :738–740 và :840–842 bỏ hai câu tuyệt đối sai. Probe nhánh `Exit-IfBlocked`: `ran=false` → `rc5 inconclusive/tree_containment`, `ran=true` → `rc6 stage_failure/stage`, cùng `reason=job_unknown`. `tl_gws.py:1747,1755` xác nhận hai lần đọc, lần lấy payload sau cổng canary. |
| `runbook-bao-tri-cu-bo-qua-refresh` [P3] | **VÁ SINH LỖI MỚI** | RUNBOOK :203–205 nay dùng `nlm auth refresh` đúng hướng, nhưng câu “Chỉ khi refresh báo lỗi xác thực” bỏ sót canary. CLI giả trên bản sao wrapper: refresh rc0, canary rc7 `Authentication expired` → wrapper `status=auth_failure, step=canary, rc=7`, exit2; log có `--version`, `auth refresh`, `notebook get`, **0 stage**. RUNBOOK :746 lại bảo đăng nhập cho `auth_failure / refresh·canary`. |
| `huong-dan-cu-con-lech-sau-va-ngoai-write-set` [P3] | **CHƯA VÁ** | `git diff --name-only a5464c3 HEAD -- <bốn path ngoài lease>` rỗng; `rg -n 'nlm login|login --check|nlm-auth-stage'` vẫn thấy `scripts/tl_core/cli.py:145`, `scripts/nlm-auto-refresh.sh:76-85`, `references/COWORK_PROJECT.md:83,94`, `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`. Cần Packet khác. |
| `stage-canary-true-khi-than-rong-hoac-sai-id` [P2 lịch sử thiếu đo] | **ĐÃ VÁ THẬT trong fixture offline** | Lệnh selftest nguyên trạng rc1 vì ACL của Python `tempfile.mkdtemp`; chạy cùng `tl.py --selftest` với shim chỉ thay cách tạo thư mục tạm trong sandbox → `1728/1728`, rc0. Trong đó `tl_selftest.py:4790-4830` gọi command-function thật, chỉ giả `nlm_cli._run`/sink: 1 upload cho thân đúng và 0 cho 9 thân âm. Không gọi CLI/LIVE thật. |
| `linux-subreaper-khong-thu-hoi-zombie` [P2 lịch sử thiếu đo] | **CHƯA VÁ / KHÔNG ĐO ĐƯỢC việc đóng** | Hai tệp ps1 không đổi từ head trước; `wsl.exe -d Ubuntu-Clean -u root -- bash -c 'cd /mnt/c/Users/admin/cw/rv8 && pwd'` → rc1, `Wsl/Service/E_ACCESSDENIED`. Không có phép đo Linux độc lập 4 chu kỳ zombie. Không nâng hạn chế WSL thành finding mã. |

Các hướng cũ còn chưa đo: người dùng/phiên Windows thứ hai, lỗi Job API do hệ điều hành thật và ma trận quote/backslash đầy đủ. Suite fake/projection không thay các môi trường ấy.

## SPEC r4

| mục | đạt / một phần / chưa đạt / KHÔNG ĐO ĐƯỢC | căn cứ |
|---|---|---|
| 1. Refresh trên host gốc | một phần | Wrapper có timeout/đường dẫn profile, suite fake xanh; không gọi `nlm` thật hoặc xác nhận browser profile thật. |
| 2. Canary notebook thật | một phần | Fake Windows đo thứ tự và nhánh lỗi xác thực; bảng 35 codepoint khớp tĩnh; 101 dạng/168 byte Linux và notebook thật chưa đo độc lập. |
| 3. Cổng `nlm-auth-stage` | một phần | Source buộc `is True`; selftest 1728/1728 dưới shim temp gồm upload count/thân sai; LIVE/Drive và mutant None-cho-upload chưa tự đo. |
| 4. Windows thứ tự, lock, test | một phần | Native `Tests.ps1` `passed=34 failed=0`, rc0; lỗi Job API thật và nhiều user chưa đo. |
| 5. Trạng thái riêng | một phần | Fixture canary auth rc2/0 stage; projection `ran` rc5/rc6; RUNBOOK còn câu hướng dẫn mâu thuẫn. |
| 6. Keepalive/takeover | một phần | Suite 34/0 gồm mutex/Job/z; fake `-MaxCycles 3` thiếu opt-in chỉ chạy cycle1; khác user/session chưa đo. |
| 7. Manifest ứng viên | đạt trong phép đo offline | `files=183`, script mới và RUNBOOK có mặt, pointer_fail0/advisory107/baseline3; negative pointer giả bị bắt. Không sửa manifest committed. |
| 8. Gate/handoff | KHÔNG ĐO ĐƯỢC đầy đủ | Windows suite và secret scan có rc riêng; Python selftest qua shim temp 1728/1728 rc0, còn canonical command gặp lỗi ACL sandbox. CI/admission/LIVE/Drive ngoài phạm vi offline. |

## BẢNG ĐO

`KHÔNG ĐO ĐƯỢC` là giới hạn phép đo, không phải lỗi mã. Không đọc credential, không gọi mạng/CLI `nlm` thật/Drive.

| khẳng định định lượng / hành vi | PR hoặc tài liệu khai | đo được | khớp? |
|---|---|---|---|
| Exact identity và phạm vi | head, Spec, hint, chỉ 2 tài liệu đổi | HEAD/tree như đầu verdict; hash Spec/verdict cũ khớp; parent trực tiếp `a5464c3`; hai file 3/1 và 11/6, 4 path khác 0; áp hint cũ cho nội dung head giống sau chuẩn hóa EOL | Khớp nội dung; mô tả “có merge giữa hai head” trong PROMPT sai, không phải finding sản phẩm |
| Windows suite | changelog: 34 passed, 0 failed trên Windows 11, pwsh 7.6.6, Python 3.13.1; EVIDENCE không chạy lại | `pwsh -NoProfile -File cay-kho/scripts/nlm-credential-refresh.Tests.ps1` với TEMP trong sandbox → `passed=34 failed=0`, rc0; `pwsh -v` 7.6.6, `python --version` 3.13.1, OS NT 10.0.26300.0 | Khớp count/rc/versions trong môi trường này |
| Python selftest | 1728/1728 rc0 theo EVIDENCE và commit | Canonical command rc1 tại `tl_selftest.py:346` do `WinError 5` trong Python `tempfile.mkdtemp`; probe tối thiểu cùng lỗi, PowerShell tạo thư mục tương ứng được. `python review-tmp/run-selftest-with-sandbox-temp.py` chỉ thay cách tạo thư mục tạm, chạy test logic trên exact head → `== tl selftest 1728/1728 ==`, rc0. | Count/logic khớp qua shim; canonical môi trường sandbox KHÔNG ĐO ĐƯỢC |
| Manifest/pointer r209 | 183 hoặc số ứng viên hiện thời, 8 assertions, negative probe | `_build_release_manifest` → 183, script mới/ RUNBOOK có; `_doc_pointer_findings` → fail0, advisory107, baseline3; pointer `scripts/wp710_missing_probe.py` → `pointers_ok=False`, đúng một fail | Khớp offline |
| Bảng trắng | 35 ký tự ở PS và Python | AST Python + regex PS → `python_count=35 ps_count=35 equal=True` | Khớp tĩnh |
| Ngưỡng WP710 | timeout 120s, lock 10s, interval 3600s, max cycle1, quarantine900s, Job wait5s, fingerprint16 hex, lý do8–200 ký tự | Source wrapper :12–19,:631,:963,:972 chứa đúng hằng; fake `-MaxCycles 3` không opt-in → cycle1, 1 stage; fingerprint fake `D439509C70C55EC7` đúng SHA-256 của lower-case profile path | Khớp code/fixture; không đo đủ thời gian mặc định |
| Canary lỗi xác thực | bảng RUNBOOK cho `auth_failure / refresh·canary`, câu bảo trì chỉ refresh | Fake: refresh rc0, canary rc7, status auth_failure/canary, wrapper rc2, 0 stage | **Lệch hướng dẫn RUNBOOK** |
| NUL/handle | stdin là NUL đọc được, ba handle, không giữ pipe wrapper | Source có list 3 handle, CreateProcess rồi giải phóng; suite gốc 34/0; mutant NUL từ read→write biên dịch PASS và đỏ đúng `Tests.ps1:263` “child stdin must be readable EOF” | Khớp fixture; OS fault/leak tổng quát chưa đo |
| Changelog Linux | 34/0, 101 shapes/0 diff, 168 byte/0 diff, 4 cycles/0 zombie, drift 2.9s/130s và 7.0s/256s | WSL bị `E_ACCESSDENIED` trước khi chạy helper | KHÔNG ĐO ĐƯỢC độc lập |
| Changelog lịch sử khác | 13 phút pipe; trước đó 8 shape khác | Không có rig/đầu vào của lượt lịch sử; bản hiện tại có test tương ứng nhưng không tái lập số lịch sử | KHÔNG ĐO ĐƯỢC các số lịch sử |
| Số liệu cũ khác trong RUNBOOK | timeout GWS 120/600/900s, kích thước 2.487.725B, bảng latency/throughput, số file/doc ID và tuổi cookie 2–4 tuần | Không có rig và baseline lịch sử trong bundle. Ngưỡng cảnh báo 14 ngày có trong `tl_gws.py:828`; tuổi sống 2–4 tuần không đo LIVE | KHÔNG ĐO ĐƯỢC các đo lịch sử; 14 khớp hằng mã |
| Diff/secret | `git diff --check` và scan 6 path rc0 | `git diff --check a5464c3 HEAD -- <2 tài liệu>` rc0; `pkg_secret_scan.py review-scan` trên bản sao sáu path rc0, output rỗng | Khớp đúng scope |
| LIVE/authority | Executor tự khai chưa đo | Không có receipt độc lập trong bundle; không gọi mạng/LIVE | `not_measured`, không suy `passed` |

## BẢNG SĂN

S1–S7 là bảy hướng độc lập của lượt này; S8 đo sâu hơn ranh giới `ran` và không tính thay cho bảy hướng đó.

| hướng: giả thuyết | lệnh / output thật | kết luận |
|---|---|---|
| **S1.** Câu bảo trì mới bỏ canary `auth_failure` dù refresh thành công. | `rg -n 'Chỉ khi refresh|auth_failure.*canary' RUNBOOK` → :204 so với :746; wrapper copy + fake Python → refresh0, canary7, `auth_failure/canary`, rc2, log 0 stage. | **LỖI tài liệu** trong lớp cũ, bản vá sinh lỗi mới. |
| **S2.** Commit thêm hunk ngoài hint dù chỉ khai áp hint. | `git show -s --format='%H %P' HEAD` → parent `a5464c3`; `git diff --numstat` → 3/1 + 11/6; áp hint lên blob cha rồi so nội dung sau CRLF/LF → `True, True`. | **KHÔNG PHẢI LỖI** sản phẩm; không có merge giữa đúng hai head như PROMPT nói. |
| **S3.** `Get-Command` tìm được shim `.cmd` nhưng Job API không chạy được nó. | `pwsh -NoProfile -File review-tmp/probe-cmd-shim.ps1` biên dịch nguyên C# với warnings-as-errors; `found=...probe-shim.cmd child_null=False stage= error=0`, `resumed=True waited=True exit=0`. | **KHÔNG PHẢI LỖI** với shim benign này; không gọi `nlm` thật. |
| **S4.** Suite Windows chỉ có tên ca stdin, không bắt NUL sai quyền truy cập. | Bản sao PS1 + Tests đổi duy nhất `CreateFileW("NUL", 0x80000000`→`0x40000000`; `Add-Type -WarningAction Stop -ErrorAction Stop` → `compile=PASS`; suite mutant rc1 tại `Tests.ps1:263`, lỗi “the child stdin must be readable EOF from NUL”; suite gốc 34/0. | **KHÔNG PHẢI LỖI** ở head; test phân biệt đúng đột biến biên dịch được. |
| **S5.** Test r209 xanh giả vì manifest ứng viên thiếu script hoặc negative pointer không đỏ. | `_build_release_manifest` → `files=183 script=True runbook=True pointer_fail=0 advisory=107 baseline=3`; `_doc_pointer_findings` với `scripts/wp710_missing_probe.py` → `negative_ok=False`, đúng một fail. | **KHÔNG PHẢI LỖI** trong phép đo offline. |
| **S6.** Fingerprint tài liệu sai độ dài/cơ sở hash hoặc ngầm gắn profile cho CLI. | Fake wrapper JSON: `D439509C70C55EC7`, `profile_bound_to_cli=false`; Python SHA-256 trên lower-case full profile path → cùng 16 ký tự; source chỉ `Test-Path` profile, không truyền đường dẫn vào child. | **KHÔNG PHẢI LỖI** trong fixture; host profile thật chưa đo. |
| **S7.** `-MaxCycles 3` có thể bật keepalive mặc dù thiếu opt-in. | Fake wrapper copy với canary dương, `-MaxCycles 3` không `-EnableKeepalive` → rc0 `staged`, `cycle=1`, log đúng một `auth refresh`, một `notebook get`, một `stage`. | **KHÔNG PHẢI LỖI** trong fixture. |
| **S8 (đào sâu lớp cũ).** Mọi kết quả blocked của stage có thể bị gán cùng nhãn, mất `ran`. | `pwsh -NoProfile -File review-tmp/probe-stage-boundary.ps1` → `inconclusive/tree_containment` rc5; thêm `-Ran` → `stage_failure/stage` rc6; cả hai `reason=job_unknown`. Source kiểm `Exit-IfBlocked`, timeout stage và catch prestart riêng. | **KHÔNG PHẢI LỖI** trong projection; lỗi Job API thật chưa đo. |

## FINDING THEO LỚP

### runbook-bao-tri-cu-bo-qua-refresh  [P3]  Câu bảo trì mới bỏ sót lỗi xác thực của canary

TỆP/DÒNG: `references/RUNBOOK.md:203-205,746`; liên hệ `scripts/nlm-credential-refresh.ps1:1024-1030`.

VẤN ĐỀ: Trên **head này**, mục bảo trì đã chuyển đúng sang `nlm auth refresh`, nhưng viết “Chỉ khi refresh báo lỗi xác thực mới `nlm login` tương tác”. Chính bảng trạng thái cùng tài liệu chỉ dẫn đăng nhập lại khi **refresh hoặc canary** trả `auth_failure`. Đường canary ấy có thật: fake CLI cho refresh rc0, canary rc7 với `Authentication expired`; wrapper trả `auth_failure/canary` rc2 và 0 stage. Câu “chỉ khi refresh” có thể khiến người vận hành bỏ cách phục hồi đã chỉ ngay tại bảng.

ĐÃ THỬ VÁ: có — `HINT.patch` chỉ đổi câu RUNBOOK để nhắc cả lỗi xác thực ở canary; không đụng runtime nhạy cảm.

ĐÃ THỬ NGHIỆM: wrapper copy + fake Python như S1. `git apply --check -p0 ../HINT.patch` và `git apply -p0 ../HINT.patch` trên `review-hint-new/` đều rc0, nội dung mới đúng. `patch -p0 --fuzz=0 --dry-run -i ../HINT.patch` **KHÔNG ĐO ĐƯỢC**: `patch.exe` dừng trước khi đọc patch với `CreateFileMapping ... Win32 error 5`, rc256 (sandbox).

ĐỘ TIN: cao về mâu thuẫn và đường chạy fake; không suy tần suất auth failure LIVE.

### huong-dan-cu-con-lech-sau-va-ngoai-write-set  [P3]  Hướng dẫn cũ ngoài lease còn lệch workflow

TỆP/DÒNG: `scripts/tl_core/cli.py:145`; `scripts/nlm-auto-refresh.sh:76-85`; `references/COWORK_PROJECT.md:83,94`; `docs/WORKFLOW_RASOAT_TU_DONG.md:274,362`.

VẤN ĐỀ: Bốn path **ngoài sáu tệp write set** vẫn dẫn `nlm login`/`login --check` như phép xác nhận, hoặc nuốt rc của `nlm-auth-stage`. Cần Packet khác với owner/write set riêng; không quy lỗi này cho Executor ở head này.

ĐÃ THỬ VÁ: không trong Packet này; hướng xử lý bằng lời: cập nhật help/flow cũ và giữ rc của stage hiển thị.

ĐÃ THỬ NGHIỆM: `git diff --name-only a5464c3 HEAD -- <bốn path>` rỗng; `rg` vẫn trả các dòng trên. Không chạy LIVE.

ĐỘ TIN: cao về nội dung tĩnh.

## ĐẾM LỚP MỞ

| loại | P1 | P2 | P3 | tổng |
|---|---:|---:|---:|---:|
| finding có biểu hiện sai ở head, trong sáu path | 0 | 0 | 1 | 1 |
| finding ngoài sáu path, cần Packet khác | 0 | 0 | 1 | 1 |
| lớp lịch sử thiếu phép đo đủ để tuyên bố đóng, không nâng thành finding | 0 | 1 | 0 | 1 |
| tổng lớp còn mở hoặc chưa nghiệm thu | 0 | 1 | 2 | 3 |

Ngưỡng `approve` của PROMPT không đạt vì còn một P3 trong write set, dù Windows suite xanh. Không nhận `cross_approved` từ tên model/provider tự khai; runtime attestation và delivery/assurance bên ngoài sandbox chưa đo.

## HINT.patch

Dòng đầu giữ đúng nhãn nguyên văn; chỉ sửa `references/RUNBOOK.md`, đường dẫn repo-relative không có `a/`–`b/`. `git apply` check/áp trên bản sao rc0. `patch.exe` dry-run bị `Win32 error 5` của sandbox trước khi đọc patch, nên khả năng áp bằng đúng binary ấy là **KHÔNG ĐO ĐƯỢC**, không khai pass. Executor phải tự áp, tự đo và chịu trách nhiệm commit.

## TRẠNG THÁI CHECKOUT CUỐI

`git -C cay-kho status --porcelain=v1 --untracked-files=all` → output rỗng, rc0. `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'` → `5e9fd9247fa2e54f0b41b835c4bf01aeb1050a19` / `d43ad4ced6440d4a2ec94c60ea935ac92b574961`. `review-tmp/tra_luat_nlm_credential_refresh.operation.json` không tồn tại sau suite gốc/mutant và probe fake. Các bản sao/probe chỉ nằm trong sandbox.

