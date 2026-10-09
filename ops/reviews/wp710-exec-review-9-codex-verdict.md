verdict: approve
reviewed_sha: 6a8c8b593d9538864e53ac5f7f495ff2f1b7c379
reviewed_tree: 80621d6ecb69f02ff5a6545a56d98f7b81f2ea69
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: OpenAI (tự khai)
reviewer_model: GPT-6 (tự khai; runtime attestation KHÔNG ĐO ĐƯỢC)
reviewer_execution_surface: Codex local sandbox (tự khai)
reviewer_transport: local tools (tự khai)

Approve **nội dung trên đúng head** theo ngưỡng PROMPT: suite Windows độc lập xanh và không thấy lớp P1/P2/P3 còn mở trong sáu path write set. Đây không tự chứng minh cross_approved, admission, CI, lease, LIVE, Drive hay quyền land. Một finding P3 ở ngoài write set cần Packet khác; phép đo Linux độc lập bị WSL chặn.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Hash tự đo: SPEC.md = A51164CF4BB0B3F41D4C01EF56A522C339CAAC008F2D855B3819A3EBB642BC0B; VERDICT_LUOT_TRUOC.md = 4714D114C35A7768F439943B64E25BBB86C5F0F079D71A12EEA63E5DDD2F2790. git log -1 cho parent trực tiếp 5e9fd9247fa2e54f0b41b835c4bf01aeb1050a19. git diff --numstat parent HEAD chỉ có references/RUNBOOK.md 3/2. Hai blob PS1 tại a5464c3 và HEAD giống nhau: wrapper 24240a31be4d51332f748d3fdadf3307cb6f1a88; Tests 4dc5994c363245219419fc0e2a20350761d6f7f1.

| slug cũ | phân loại trên head này | lệnh và output tự đo |
|---|---|---|
| khai-rong-hon-phep-do-trong-changelog-runbook [P3 lịch sử] | **ĐÃ VÁ THẬT** trong phạm vi offline | Đọc RUNBOOK:738–742,839–844, changelog:8–20 và tl_gws.py:1743–1755: tiền kiểm jar trước canary được mô tả, payload đọc sau canary; stage_failure không hứa 0 upload. Suite Windows passed=34 failed=0; probe gate True/False/None bên dưới đo thứ tự canary→jar. Các số Linux 101/168 còn KHÔNG ĐO ĐƯỢC, không dùng để đóng lời khai Linux. |
| runbook-bao-tri-cu-bo-qua-refresh [P3 lượt trước] | **ĐÃ VÁ THẬT** | git -c core.autocrlf=false apply --check -p0 HINT_LUOT_TRUOC.patch và apply trên blob cha ở review-tmp/hint-check-lf đều rc0; so byte với RUNBOOK head = True. RUNBOOK:204–206 nay nói refresh **hoặc canary** auth_failure, khớp bảng :747. Fake CLI riêng: refresh rc0, canary rc7 Authentication expired → wrapper rc2, auth_failure/canary, 0 stage. |
| huong-dan-cu-con-lech-sau-va-ngoai-write-set [P3] | **CHƯA VÁ** | rg -n 'nlm login|login --check|nlm-auth-stage' trên bốn path ngoài lease còn cli.py:145, nlm-auto-refresh.sh:76–85, COWORK_PROJECT.md:83,94, WORKFLOW_RASOAT_TU_DONG.md:274,362. git diff parent HEAD chỉ RUNBOOK. Cần Packet khác. |
| stage-canary-true-khi-than-rong-hoac-sai-id [P2 lịch sử] | **ĐÃ VÁ THẬT trong fixture offline** | Selftest qua shim temp sandbox: 1728/1728 rc0, gồm tl_selftest.py:4790–4830 với thân đúng 1 upload và chín thân âm 0 upload; :4643–4680 gồm False/None/timeout và --force. Probe riêng _nlm_files_after_live_canary: True → rc0, calls=[canary,jar]; False/None → rc4, calls=[canary]. CLI/LIVE thật KHÔNG ĐO ĐƯỢC. |
| linux-subreaper-khong-thu-hoi-zombie [P2 lịch sử thiếu đo] | **CHƯA VÁ trong delta; việc đóng KHÔNG ĐO ĐƯỢC** | git diff a5464c3 HEAD -- hai PS1 rỗng; Windows suite không đo Linux. wsl.exe -d Ubuntu-Clean -u root -- pwd → Access is denied; Wsl/Service/E_ACCESSDENIED, LASTEXITCODE=-1. Không thấy biểu hiện lỗi mã ở head này để nâng thiếu phép đo thành finding mới. |

Các hướng chưa đo của lượt trước: quote/backslash nay đo 156 tổ hợp, 0 khác biệt; người dùng/phiên Windows thứ hai và lỗi Job API tự nhiên vẫn KHÔNG ĐO ĐƯỢC. Projection test không thay cho lỗi OS thật.

## SPEC r4

| mục | trạng thái | căn cứ |
|---|---|---|
| 1. Refresh trên host gốc | một phần | Wrapper kiểm profile path, timeout mặc định 120s, fake chạy refresh; không gọi nlm hay browser thật. |
| 2. Canary notebook thật | một phần | Fake đo thứ tự, ID/thân, auth lỗi, UTF-8; notebook/CLI thật chưa đo. |
| 3. Stage chỉ sau True, kể cả --force | đạt trong phép đo offline | Probe True/False/None và selftest 1728/1728 gồm ca --force, command-level upload count; LIVE/Drive chưa đo. |
| 4. Windows thứ tự/lock/test | đạt trong phép đo offline native | Tests.ps1 passed=34 failed=0 rc0, gồm hai tiến trình và các projection Job. |
| 5. Trạng thái riêng | đạt trong phép đo offline | Fake auth_failure/canary rc2/0 stage; suite kiểm network, timeout, inconclusive và stage_failure; mutant ran=false đỏ đúng nhãn. |
| 6. Keepalive/takeover | một phần | Suite Windows 34/0 gồm mutex, Job, ca z; user/session thứ hai và lỗi Job API thật chưa đo. |
| 7. Manifest ứng viên | đạt trong phép đo offline | files=183, required_missing=0, script mới và RUNBOOK có; pointer fail0/advisory107/baseline3; negative pointer fail đúng 1. |
| 8. Gate/handoff | một phần | Windows suite và secret scan rc0; selftest logic 1728/1728 qua shim; canonical selftest bị ACL. Admission, CI, assurance và LIVE không nằm trong bundle offline. |

## BẢNG ĐO

KHÔNG ĐO ĐƯỢC chỉ là giới hạn phép đo, trừ khi nêu một biểu hiện sai cụ thể. Không đọc credential, không gọi mạng, nlm thật hay Drive.

| khẳng định | PR/tài liệu khai | đo được | khớp? |
|---|---|---|---|
| Identity/phạm vi/hint | Head chỉ áp hint cũ, một hunk RUNBOOK | HEAD/tree như header; parent trực tiếp 5e9fd92; diff parent HEAD chỉ RUNBOOK 3 thêm/2 xoá. git apply hint trên blob cha với core.autocrlf=false rc0 và bằng byte head. Diff toàn PR sáu path tái tạo trùng nội dung sau chuẩn hoá EOL, 283562 ký tự. | Khớp nội dung và byte khi ghim EOL; git apply ngoài repo mặc định tự đổi LF→CRLF. |
| Phạm vi PR từ base | Chỉ sáu path | git diff --name-only 8c98afa HEAD -- sáu path cho đúng sáu; numstat lần lượt changelog 101/0, RUNBOOK 203/7, Tests 1329/0, wrapper 1059/0, tl_gws 346/47, tl_selftest 612/16. | Khớp patch được giao; không suy thay đổi ngoài phạm vi từ diff base toàn kho. |
| Windows suite | 34 passed, 0 failed trên Windows 11/pwsh 7.6.6/Python 3.13.1 | TEMP/TMP/TMPDIR dưới review-tmp; pwsh -NoProfile -File cay-kho/scripts/nlm-credential-refresh.Tests.ps1 → passed=34 failed=0, rc0. pwsh=7.6.6, Python=3.13.1, NT 10.0.26300.0. | Khớp. |
| Python selftest | 1728/1728 rc0; một lượt Executor treo >1 giờ | Canonical với temp sandbox rc1 tại tl_selftest.py:346 do WinError 5; retry TL_CACHE_DIR do PowerShell tạo tới :1412 rồi rc1 vì Python tempfile thư mục con cấm ghi. Shim chỉ thay tempfile.mkdtemp bằng pathlib.mkdir(mode=0777) trong sandbox → tl selftest 1728/1728 rc0. | Logic/count khớp qua shim; canonical môi trường sandbox KHÔNG ĐO ĐƯỢC. Không tái lập nguyên nhân lượt treo của Executor. |
| RUNBOOK bảo trì auth | refresh **hoặc canary** lỗi auth thì login | Fake chỉ cho canary rc7: wrapper JSON auth_failure/canary rc2, log --version/auth refresh/notebook get, 0 stage. | Khớp câu mới và bảng :747. |
| Cổng True/False/None | Chỉ True đọc jar/upload | Probe hàm: True → rc0, calls=[canary,jar]; False/None → rc4, calls=[canary]. Selftest command-level trên fixture có True=1, chín thân âm=0, và --force âm=0. | Khớp offline; không suy LIVE. |
| Manifest/pointer | 183 tệp, advisory107, baseline3 | probe-manifest.py → files=183, ok=True, required_missing=0, script=True, runbook=True, pointer fail0/advisory107/baseline3; pointer giả → negative_ok=False, đúng một fail. | Khớp. |
| Bảng trắng/JSON | 35 codepoint, tối đa 64 mức | AST Python + regex PS → 35/35, equal=True, unique=35. Tests.ps1:327–349 có âm NaN/overflow/surrogate/trùng key/deep65 và dương meta_ok; suite 34/0. | 35 khớp tĩnh, các fixture khớp; parity 101 dạng Linux chưa tự đo. |
| Windows Job/handle/ran | 3 handle, NUL stdin, wait 5s, rc5 trước stage/rc6 sau stage chạy | Source :234–269 lập list 3, đóng list/buffer/NUL trước hai đầu ghi parent; :275–282 bắt _alive; :664–724 giữ record/giải phóng; :931–943 xét ran. Suite 34/0; mutant ran=false biên dịch C# warning-as-error PASS và đỏ tại Tests.ps1:1315: rc5 inconclusive/tree_containment reason=job_unknown sau stage. | Khớp các fixture; lỗi OS tự nhiên chưa đo. |
| Ngưỡng/mã số WP710 | 120s timeout, 10s lock, 3600s interval, 1 cycle, 900s quarantine, 5s job wait, 1s PID tolerance, lý do 8–200, fingerprint 16 hex | Wrapper :12–19,:631,:540,:963,:971–972 chứa đúng hằng/biểu thức; suite kiểm các nhánh thực thi nhưng không chờ toàn bộ ngưỡng mặc định. | Khớp hằng mã; thời gian thật mỗi mặc định KHÔNG ĐO ĐƯỢC. |
| Quote/backslash | Chưa đo đủ ở lượt trước | C# Job.Quote so với Win32 CommandLineToArgvW trên 156 tổ hợp rỗng, space, quote, backslash, Unicode → diffs=0, rc0. | Khớp phạm vi ma trận này. |
| Linux | 34/0, 101 dạng/0 diff, 168 byte/0 diff, 4 cycle/0 zombie | WSL dừng trước helper với Wsl/Service/E_ACCESSDENIED; không chạy Linux suite. | KHÔNG ĐO ĐƯỢC độc lập. |
| Số lịch sử khác | 13 phút pipe treo; WSL lệch 2,9s/130s và 7,0s/256s; RUNBOOK latency/throughput/kích thước cũ, tuổi cookie ~2–4 tuần | Không có rig/lịch sử/nguồn LIVE để tái lập. Riêng ngưỡng cảnh báo 14 ngày có hằng _NLM_COOKIE_WARN_DAYS=14 trong tl_gws.py:828. | KHÔNG ĐO ĐƯỢC giá trị lịch sử/tuổi sống; 14 khớp mã. |
| Diff/secret/authority | diff --check và quét sáu path rc0; LIVE chưa làm | git diff --check base HEAD -- sáu path rc0; pkg_secret_scan.py trên bản sao sáu path rc0, output rỗng. Không có receipt admission, CI, LIVE hoặc runtime model trong sandbox. | Khớp gate local; các trạng thái còn lại not_measured. |

## BẢNG SĂN

S1–S8 là tám hướng độc lập của lượt này; các hướng trùng chủ đề cũ có phép đo sâu hơn hẳn. Hướng chỉ có hạn chế môi trường không bị nâng thành finding mã.

| hướng: giả thuyết | lệnh / output thật | kết luận |
|---|---|---|
| **S1.** Hunk mới chứa thay đổi ngoài hint mà diff ngắn che được do EOL. | probe-hint-lf.py lấy blob parent, git -c core.autocrlf=false apply --check/apply -p0 hint đều rc0; byte_equal=True. Git apply mặc định trên bản sao tạo CRLF, nhưng normalized_equal=True. | **KHÔNG PHẢI LỖI**; provenance nội dung và byte đã xác nhận. |
| **S2.** Con treo ngoài job bị mất record hoặc job rỗng cho phép takeover. | Tests.ps1:1186–1299 thật sự dựng con treo, xác nhận PID sống, outside_job=true, root_alive chặn operator, job khác rỗng vẫn quarantine, sau khi con chết vẫn quarantine; suite gốc passed=34 failed=0 rc0. | **KHÔNG PHẢI LỖI** ở fixture Windows. |
| **S3.** Stage đã chạy nhưng count job không đọc được bị gán inconclusive. | Bản sao mut-ran thay đúng một ran=true→ran=false tại return success-unproven; C# Add-Type -WarningAction Stop -ErrorAction Stop → compile=PASS; test file SHA-256 trùng gốc. Full Tests.ps1 mutant rc1 tại :1315, thông báo rc5 status=inconclusive step=tree_containment reason=job_unknown; gốc 34/0. | **KHÔNG PHẢI LỖI** ở head; ca z2 bắt được đúng đột biến có hiệu lực. |
| **S4.** Danh sách handle còn cho con giữ stdout wrapper hoặc stdin không là EOF đọc được. | Source C# :234–269 list đúng NUL + hai đầu ghi, :271 đóng đầu ghi parent, :265–269 giải phóng attribute list/buffer/NUL; Tests.ps1:258–265 kiểm stdin, :1227–1245 đọc pipe với hạn 90s và kiểm con treo thật; suite 34/0. | **KHÔNG PHẢI LỖI** trong fixture; leak handle tổng quát ngoài fixture KHÔNG ĐO ĐƯỢC. |
| **S5.** Quote của đường CreateProcess sai với empty/space/quote/backslash/Unicode. | pwsh -File review-tmp/probe-quote.ps1 biên dịch C# warning-as-error, so Win32 CommandLineToArgvW: cases=156 diffs=0 rc0. | **KHÔNG PHẢI LỖI** trên ma trận này. |
| **S6.** Test Windows cho byte canary chỉ có tên, không có đối chứng dương/âm và đếm stage. | Tests.ps1:327–349 đòi âm rc4/inconclusive/canary/0 stage và dương rc0/staged/1 stage, gồm BOM, UTF-8 hỏng, CRLF, keyring, U+2028/NEL; full suite Windows 34/0. | **KHÔNG PHẢI LỖI** ở các input fake; không thay phép so Linux 101/168 hoặc CLI thật. |
| **S7.** Cổng Python đọc jar khi False/None hoặc cho --force qua. | python review-tmp/probe-stage-gate.py → True rc0 [canary,jar], False/None rc4 [canary]. Selftest qua shim 1728/1728, gồm tl_selftest.py:4643–4680 ca --force âm và :4790–4830 thân thật/giả. | **KHÔNG PHẢI LỖI** offline; không gọi upload Drive thật. |
| **S8.** Các số Linux và thời gian lịch sử trong RUNBOOK/changelog có thể được nhận nhầm thành phép đo reviewer. | wsl.exe -d Ubuntu-Clean -u root -- pwd → Access is denied, Wsl/Service/E_ACCESSDENIED, rc=-1. rg trên changelog/RUNBOOK tìm 101/168/4 zombie/13 phút/2,9–7,0s; không có rig lịch sử trong bundle. | **KHÔNG ĐO ĐƯỢC**; giữ trạng thái lời khai Executor. |

Hướng săn cũ được xét lại: người dùng/phiên Windows thứ hai và lỗi Job API tự nhiên KHÔNG ĐO ĐƯỢC vì không có môi trường đó; không tự soạn nội dung để giả lập quyền khác người dùng. Nếu cần đo, chạy cùng suite offline trong hai phiên/user thật và ép lỗi API bằng OS rig có telemetry, so record, mutex, rc và 0 stage trước khi kết luận.

## FINDING THEO LỚP

Không có finding mới trong sáu path write set.

### huong-dan-cu-con-lech-sau-va-ngoai-write-set  [P3]  Hướng dẫn cũ ngoài lease còn lệch workflow

TỆP/DÒNG: scripts/tl_core/cli.py:145; scripts/nlm-auto-refresh.sh:76–85; references/COWORK_PROJECT.md:83,94; docs/WORKFLOW_RASOAT_TU_DONG.md:274,362.

VẤN ĐỀ: Trên head này, các path **ngoài sáu tệp write set** vẫn nêu nlm login/login --check như đường xác nhận, hoặc nuốt rc của nlm-auth-stage. Chúng có thể hướng người vận hành theo workflow cũ. Cần Packet khác với write set/owner riêng; đây không phải lỗi hunk của Executor vòng này.

ĐÃ THỬ VÁ: không — ngoài write set; hướng vá bằng lời: cập nhật các chỉ dẫn cũ về refresh + canary dương, hiển thị rc stage thay vì nuốt.

ĐÃ THỬ NGHIỆM: git diff parent HEAD chỉ có RUNBOOK; rg -n trên bốn path cho các dòng trên. Không chạy LIVE.

ĐỘ TIN: cao về nội dung tĩnh; tác động vận hành thực tế KHÔNG ĐO ĐƯỢC.

## ĐẾM LỚP MỞ

| phạm vi | P1 | P2 | P3 | tổng |
|---|---:|---:|---:|---:|
| Finding có biểu hiện sai ở head trong sáu path | 0 | 0 | 0 | 0 |
| Finding ngoài sáu path, cần Packet khác | 0 | 0 | 1 | 1 |
| Tổng finding ở head | 0 | 0 | 1 | 1 |

Lớp Linux P2 lịch sử vẫn **KHÔNG ĐO ĐƯỢC việc đóng** vì WSL bị chặn; chưa thấy biểu hiện sai ở head nên ghi nợ phép đo riêng, không nâng thành finding. Ngưỡng approve riêng của PROMPT đạt trong write set. Reviewer/Executor khác provider theo tự khai, nhưng bằng chứng runtime model và assurance bên ngoài sandbox chưa đo; không tự cấp nhãn cross_approved hay land authority. Không có HINT.patch mới vì không có cách vá trong write set cần gợi ý.

## TRẠNG THÁI CHECKOUT CUỐI

git -C cay-kho status --porcelain=v1 --untracked-files=all → output rỗng, rc0. git -C cay-kho rev-parse HEAD 'HEAD^{tree}' → 6a8c8b593d9538864e53ac5f7f495ff2f1b7c379 / 80621d6ecb69f02ff5a6545a56d98f7b81f2ea69. Không có tra_luat_nlm_credential_refresh.operation.json trong review-tmp sau suite/probe. Mọi probe, bản sao và shim nằm dưới review-tmp trong sandbox; không sửa cay-kho.
