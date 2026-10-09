verdict: blocked
reviewed_sha: ed1288908e533491456f320e3ce07081f129c0a7
reviewed_tree: 1f0bf9f17fed5ef1e44c05376ae17881d88cc653
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: OpenAI (tự khai)
reviewer_model: GPT-6 (tự khai; runtime/model header KHÔNG ĐO ĐƯỢC)

Lý do blocked: Windows Tests.ps1 đã tự chạy xanh một lượt, nhưng full Python selftest không đo được vì sandbox từ chối ghi vào thư mục tạm do Python vừa tạo (probe tối giản tái hiện). Không có Linux để tự đóng ba phép đo Linux. Ngoài giới hạn đo, có hai đường lỗi P2 cần sửa/giải trình: mất bản ghi khi con treo ngoài Job không kết thúc được, và status inconclusive sau khi bước stage đã được gọi. Verdict này không cấp approval, lease, admission, LIVE hay land authority. Không gọi mạng/CLI nlm thật, không đọc credential.

Phạm vi: đọc SPEC.md, EVIDENCE.md, verdict lượt 3, protocol §8/§13, diff và checkout ở đúng head. git rev-parse HEAD và tree cho đúng hai SHA trên; core.abbrev=7. Product diff 183d1f5..ed12889 chỉ gồm bốn tệp: wrapper, Tests.ps1, RUNBOOK, changelog. Hai tệp Python không đổi ở g4. Test/đột biến chỉ ghi bản sao và fixture dưới sandbox; checkout không bị sửa.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lớp: VERDICT_LUOT3_ban_chieu.md, head cc020e02607bc27eb2a815e1ac282380a155820d. Bản chiếu không thay tệp verdict gốc; tôi không suy nhận dữ liệu lượt 3 là phép đo của lượt này.

- stage-canary-true-khi-than-rong-hoac-sai-id: VÁ HỜ. Lệnh: Python đếm hai bảng trong tl_gws.py:133-138 và wrapper:758-763; output ps_count=35 py_count=35 equal=True. Windows Tests.ps1 rc 0, passed=32 failed=0; ca n:306-329 chạm U+001C–001F, BOM và transport qua stdout thật. Mock Python force=True cho True/False/None có uploads 1/0/0. Các phép 101 dạng và 168 byte trên Linux của 183d1f5 chưa tự chạy; không đủ bằng chứng đóng toàn lớp.
- khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con: VÁ SINH LỖI MỚI. Lệnh: pwsh Tests.ps1 trên ed12889 → passed=32 failed=0, rc 0; cùng bộ ở bản sao 183d1f5 → rc 1, case stage failed: status=inconclusive rc=5 stageCalls=0. Nhưng wrapper:240-243,618-620,659 cho nhánh assign_alive/verify_alive mất bản ghi (bảng săn H2); Linux owner-death/timer chưa tự đo. Thước cleanup Boolean: started=False, confirmed=False → cleanup_condition=True. Không thể đóng lớp bằng suite tổng.
- linux-subreaper-khong-thu-hoi-zombie: VÁ HỜ. Lệnh: rg -n 'waitpid|Invoke-ReapAdopted|if ($IsLinux)' trên wrapper/Tests; code wrapper:413-455 có waitpid WNOHANG, Tests.ps1:969-996 chỉ chạy khi IsLinux. Windows không chạy ca này. Output zombie 0 qua bốn chu kỳ mà PR khai: KHÔNG ĐO ĐƯỢC trên máy này.
- khai-rong-hon-phep-do-trong-changelog-runbook: VÁ SINH LỖI MỚI. Lệnh: rg -n 'stage_failure|tree_containment|Exit-IfBlocked' wrapper và RUNBOOK → wrapper:876 xuất inconclusive, :977-983 gọi stage rồi mới Exit-IfBlocked; RUNBOOK:752 mô tả stage_failure cho lệnh stage đã gọi nhưng không rc 0. Phép chiếu job_unknown ở H1 cho stageCalls=1 mà status=inconclusive. Các tuyên bố 9 mutant và 30 vòng có script riêng không kèm bundle, vẫn KHÔNG ĐO ĐƯỢC. Changelog đã giới hạn rõ phép 101/168 ở Linux, nhưng phát sinh mâu thuẫn status mới.
- huong-dan-cu-con-lech-sau-va-ngoai-write-set: CHƯA VÁ. Lệnh: git diff cc020e0 ed12889 -- scripts/tl_core/cli.py scripts/nlm-auto-refresh.sh references/COWORK_PROJECT.md docs/WORKFLOW_RASOAT_TU_DONG.md tl-setup.ps1 → rỗng. rg vẫn cho cli.py:145 hướng dẫn sau nlm login; nlm-auto-refresh.sh:76-78 dùng login --check và nuốt lỗi stage; COWORK_PROJECT.md:83,94; WORKFLOW_RASOAT_TU_DONG.md:274,362. Những tệp này ngoài write set; cần packet kế nhiệm có chủ. tl-setup.ps1 không có hit nlm trong checkout này, không tính biểu hiện đã xác nhận.

## SPEC r4

| mục | trạng thái | căn cứ |
|---|---|---|
| 1 | một phần | Wrapper:939-957 đặt timeout/phiên bản/fingerprint; fake Windows test xanh. CLI thật, browser host và profile thật không chạy theo giới hạn Packet; fingerprint chỉ là hash đường dẫn khai báo, profile_bound_to_cli=false. |
| 2 | một phần | Ca canary Windows âm/dương qua stdout thật xanh; 35 phần tử Python/PS bằng nhau. 101 dạng/168 byte Linux và CLI thật KHÔNG ĐO ĐƯỢC. |
| 3 | một phần | Mock trực tiếp đường _nlm_auth_stage_body với force=True: True→rc0/upload1, False/None→rc4/upload0; mutant wrapper sai canary đỏ đúng ca wrong. Full selftest và command-level upload-count chưa đo được vì sandbox. |
| 4 | một phần | Windows Tests.ps1 32/0 xác nhận thứ tự/order, stage rc 9, sentinel, hai tiến trình cùng người dùng. H1 cho thấy một nhánh stage đã gọi nhưng bị nhãn inconclusive. |
| 5 | chưa đạt | H1: bước stage có thể đã gọi, song Exit-IfBlocked xuất inconclusive/tree_containment. Điều kiện bốn status đầu zero stage calls không giữ trên nhánh đó. |
| 6 | một phần | Mặc định một chu kỳ và opt-in hai chu kỳ, concurrency/owner-death fake Windows trong suite xanh. H2 có đường thất bại bỏ bản ghi của con chưa xác nhận chết; Linux không chạy. |
| 7 | một phần | Helper manifest trên checkout sạch: 183 file, có scripts/nlm-credential-refresh.ps1, pointer_fail=0/advisory=107/baseline=3; bơm con trỏ giả vào nội dung RUNBOOK trong RAM: pointer_ok=False, fail_count=1. r209 giữ tám ok1..ok8 trong mã; full selftest chưa chạy được. RELEASE_MANIFEST.json không đổi trong diff. |
| 8 | KHÔNG ĐO ĐƯỢC | Head/tree, diff --check, targeted PS, mock Python và secret scan tự đo. Full Python selftest, Linux suite, full repository gates, admission/required CI và review assurance bền không có phép đo đủ ở sandbox; LIVE không chạy. |

## BẢNG ĐO

KHÔNG ĐO ĐƯỢC nghĩa là không sao chép lời khai thành sự thật. Các con số lịch sử khác trong RUNBOOK nằm ngoài WP710/diff (ví dụ 60/60/30, 101/101, 9/9 của những phần cũ) không có fixture/cổng tương ứng trong bundle, nên cũng KHÔNG ĐO ĐƯỢC trong lượt này.

| khẳng định | PR khai | tự đo được | khớp? |
|---|---|---|---|
| SPEC SHA/head/tree | a51164cf… / ed12889 | SHA256 SPEC đúng a51164cf…; HEAD ed1288908e533491456f320e3ce07081f129c0a7; tree 1f0bf9f17fed5ef1e44c05376ae17881d88cc653 | khớp |
| G4 chỉ đổi bốn tệp, Python không đổi | 4 | git diff --numstat 183d1f5 ed12889: changelog 40/6, RUNBOOK 32/12, Tests 197/43, wrapper 346/6; Python rỗng | khớp |
| Windows suite | 32 passed, 0 failed, rc0, hai lượt | một lượt: passed=32 failed=0, rc0 | khớp một lượt; lượt thứ hai KHÔNG ĐO ĐƯỢC |
| Đối chứng 183d1f5 Windows | rc1 ở stage, inconclusive rc5 | bản sao hai file: rc1 dòng 238, case stage failed: status=inconclusive rc=5 stageCalls=0 | khớp |
| Python full selftest | 1728/1728 rc0 | hai lần rc1 trước tổng kết do PermissionError thư mục tạm; probe tối giản mkdtemp→write_text cũng Errno 13 | KHÔNG ĐO ĐƯỢC do sandbox, không quy lỗi code |
| Mutants Executor | 9/9 đỏ đúng ca, compile kiểm | script Executor không có; mutant riêng 1/1 đỏ đúng ca wrong, C# Add-Type WarningAction Stop rc0 | 9/9 KHÔNG ĐO ĐƯỢC |
| Kill-on-close 30 vòng, hai thành viên | 0 lần job tên biến mất khi thành viên còn sống, tối đa 34 ms | script 30 vòng không có; suite case x đo một fixture owner/member thành công | 30/0/34 ms KHÔNG ĐO ĐƯỢC |
| diff --check | rc0 | git diff --check 8c98afa ed12889: rỗng, rc0 | khớp |
| Secret scan sáu tệp | rc0 | sao đúng sáu tệp vào .review-work/scan; python pkg_secret_scan.py .review-work/scan → rc0 | khớp, phạm vi sáu tệp |
| Ruff F delta | 0 so với 183d1f5 | hai tệp Python byte-identical giữa hai head; bare Ruff không chạy | delta theo byte khớp; lint KHÔNG ĐO ĐƯỢC |
| Bảng trắng canary | 35 ký tự, Python/PS cùng bảng | ps_count=35 py_count=35 equal=True | khớp về bảng tĩnh |
| Parity Linux | 101 dạng/0 lệch; 168 byte/0 lệch (trước 8/30) | Linux không có; Windows suite chạm tập con | KHÔNG ĐO ĐƯỢC |
| JSON max-depth | 64, sâu 65 từ chối | test Windows case deep65 trong suite xanh; ranh giới dương 64 chưa đo riêng | một phần |
| Zombie subreaper | bốn chu kỳ: 0 từng khoảng, trước [1,2,3] | chỉ đọc mã waitpid và ca Linux-only | KHÔNG ĐO ĐƯỢC |
| Manifest ứng viên và guard | 183, pointer fail 0, advisory 107, baseline 3, tám assertion | helper trên checkout sạch: đúng 183/0/107/3, script mới có; ok1..ok8 có trong mã; probe âm in-memory fail_count=1 | khớp phép helper; tám assertion chưa chạy |
| Default quarantine, job wait, operator reason, fingerprint | 900 giây; job đợi 5 giây; reason 8–200; fingerprint 16 hex | tĩnh: wrapper:18,581,898,907 khớp; đồng hồ 900 giây và giới hạn thời gian OS chưa đo thực | khớp cấu hình, hành vi dài hạn KHÔNG ĐO ĐƯỢC |
| RUNBOOK stage_failure và inconclusive | lệnh stage đã gọi mà không rc0 → stage_failure; bốn status đầu không stage | nhánh job_unknown ở H1: stageCalls=1/status=inconclusive/rc5 | lệch |
| LIVE CLI/browser/Drive; full gates/admission | Executor tự khai chưa làm hoặc ngoài lease | không gọi; không có receipt đủ trong bundle | không suy là passed |

## BẢNG SĂN

HƯỚNG 1: nhãn kết quả sau khi stage đã chạy
  giả thuyết : nếu Job count không đọc được sau stage, inconclusive có stageCalls=1 và phá nghĩa zero-stage.
  lệnh       : rg -n 'Exit-IfBlocked|Invoke-Bounded $stagePath|stage_failure' wrapper; trên bản sao tạm ép riêng kết quả stage thành tree.State=unknown rồi chạy Tests.ps1.
  output     : wrapper:876 Emit inconclusive/tree_containment; :977 gọi stage; :980 Exit-IfBlocked. Phép chiếu: case ok failed: status=inconclusive rc=5 stageCalls=1 step=tree_containment reason=job_unknown.
  kết luận   : LỖI. Chiếu nhánh fail của API, không tuyên bố kernel thật đã trả unknown trong lượt này.

HƯỚNG 2: con treo chưa gán được job và không chết
  giả thuyết : nếu TerminateProcess/Wait thất bại sau assign/verify, finally xóa bản ghi dù con còn sống ngoài job.
  lệnh       : rg -n 'TerminateProcess|WaitForSingleObject(pi.hProcess|$confirmed = $stage|if (-not $started -or $confirmed)' wrapper; PowerShell tính điều kiện với stage=assign_alive.
  output     : wrapper:240-243 nối _alive; :618 confirmed=False; :622 started=True chỉ sau Start thành công; :659 xóa khi not started OR confirmed. assign_alive cleanup_condition=True.
  kết luận   : LỖI về đường fail-close; trigger OS thật KHÔNG ĐO ĐƯỢC. Con còn suspended nhưng không được theo dõi/bao.

HƯỚNG 3: thừa kế handle không thuộc stdout/stderr
  giả thuyết : nếu wrapper đang giữ handle khác có cờ inheritable, CreateProcessW true cho con thừa kế cả handle đó.
  lệnh       : rg -n 'SetHandleInformation|CreateProcessW|STARTF_USESTDHANDLES|HANDLE_LIST' wrapper.
  output     : :221 chỉ bật inherit cho hai write pipe; :229 truyền inheritHandles=true; không có STARTUPINFOEX/HANDLE_LIST trong file.
  kết luận   : KHÔNG ĐO ĐƯỢC ảnh hưởng thực tế; cần fixture handle thừa kế và kiểm từ con. Đây là rủi ro bề mặt handle, chưa tính thành finding chắc chắn.

HƯỚNG 4: namespace Global và bản ghi theo người dùng
  giả thuyết : nếu chủ mới khác user/phiên, Global lock/job và temp record có thể cho các quan sát khác nhau.
  lệnh       : rg -n 'GetTempPath|JobPrefix|Global\\tra_luat_nlm|OpenJobObjectW' wrapper.
  output     : :32 GetTempPath cho record; :45 job Global; :913 mutex Global; :201 OpenJobObjectW. RUNBOOK:828 tự nêu record theo user.
  kết luận   : KHÔNG ĐO ĐƯỢC khi không có tài khoản thứ hai; cần kiểm ACL và overlap thực trên hai user.

HƯỚNG 5: quote đường dẫn/argv của Windows
  giả thuyết : nếu Quote lệch ProcessStartInfo.ArgumentList khi có dấu cách/quote/backslash, CLI có thể chạy sai đối số.
  lệnh       : trích C# của wrapper, Add-Type, gọi Job.Quote với đường dẫn có dấu cách và ba đối số thử.
  output     : "C:\Program Files\Python\python.exe" "a b" "c\"d" tail\ ; Add-Type rc0.
  kết luận   : KHÔNG ĐO ĐƯỢC tương đương argv đầu-cuối với Process.Start; không thấy lỗi ở chuỗi thử tĩnh.

HƯỚNG 6: ca có tên nhưng không chạy trên nền hiện tại
  giả thuyết : nếu chỉ nhìn passed=32 sẽ tính cả kiểm zombie/escape Linux mặc dù các nhánh bị bỏ qua.
  lệnh       : rg -n 'if ($IsLinux)|if ($IsWindows)|passed=$cases' Tests.ps1.
  output     : Linux-only tại :783,927,969,1006; Windows-only tại :1065,1133; :1160 in tổng cases.
  kết luận   : KHÔNG ĐO ĐƯỢC hành vi Linux bằng suite Windows; 32 chỉ là số ca thực chạy trên Windows.

HƯỚNG 7: biên dịch Job API và lối fail-close
  giả thuyết : nếu C# lỗi cảnh báo/biên dịch, test đỏ sai lý do hoặc wrapper lùi sang tiến trình không bao.
  lệnh       : trích nguyên C# từ bản sao mutant, Add-Type -ErrorAction Stop -WarningAction Stop; rg -n 'JobReady|job_api_unavailable|job_create_failed' wrapper; Windows Tests.ps1.
  output     : CSharpCompile=PASS, rc0; wrapper:296 catch→JobReady=false, :672-675 blocked=job_api_unavailable; suite Windows 32/0 và ca y:1146-1151 đo job_create_failed với zero child.
  kết luận   : KHÔNG PHẢI LỖI trong phép biên dịch và nhánh job-create đã chạy; không suy mọi lỗi P/Invoke khác đều an toàn.

## FINDING THEO LỚP

### khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con  [P2]  Bản ghi biến mất khi con ngoài Job chưa xác nhận chết
TỆP/DÒNG: scripts/nlm-credential-refresh.ps1:236-243,615-620,659; liên hệ 527.
VẤN ĐỀ: Start tạo con suspended, nhưng nếu Assign/Verify thất bại và WaitForSingleObject không xác nhận con chết, stage mang hậu tố _alive. Invoke-BoundedJob đặt confirmed=false nhưng started vẫn false; finally xóa record vì not started. Job đóng không bao con ấy. Chủ sau thấy không record và đi tiếp; không có PID/flag cần cho xử lý tay. Đây là lỗi điều kiện, không phải chứng minh Windows đã phát sinh lỗi hiếm này trong test.
ĐÃ THỬ VÁ: có — g4 thêm Create/Assign/Verify, nhưng cleanup không phân biệt chưa tạo con với đã tạo con chưa dọn được. Hướng: giữ bản ghi và PID riêng cho con chưa gán, chỉ cho tiếp tục sau khi xác nhận nó chết hoặc xử lý tay; cân nhắc primitive tạo con trong job nguyên tử.
ĐÃ THỬ NGHIỆM: truth table PowerShell assign_alive cleanup_condition=True; Tests.ps1 32/0 không ép TerminateProcess fail; OS trigger KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về logic, vừa về khả năng kích hoạt ngoài môi trường lỗi.

### stage-da-goi-nhung-bao-inconclusive  [P2]  Inconclusive có thể có một stage call
TỆP/DÒNG: scripts/nlm-credential-refresh.ps1:649-653,872-877,977-983; references/RUNBOOK.md:749,752.
VẤN ĐỀ: sau khi lệnh stage đã chạy, job_alive/job_unknown đi qua Exit-IfBlocked trước nhánh stage_failure. JSON thành status=inconclusive, step=tree_containment dù stage có thể đã upload. Spec #5 đòi bốn status đầu zero stage calls; RUNBOOK chỉ cảnh báo khả năng upload ở stage_failure. Người vận hành có thể đọc nhầm inconclusive là chưa chạm Drive.
ĐÃ THỬ VÁ: không — chỉ mô tả hướng: nhãn kết quả phải giữ sự thật stage đã được gọi và khả năng upload, cùng containment_reason riêng; thêm ca test ép job count unknown sau stage.
ĐÃ THỬ NGHIỆM: phép chiếu riêng trên bản sao tạm ép stage tree.State=unknown, chạy Tests.ps1: case ok failed: status=inconclusive rc=5 stageCalls=1 step=tree_containment reason=job_unknown. C# của bản sao biên dịch; API count thật trả unknown: KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về control flow, vừa về tần suất nhánh API lỗi.

### stage-canary-true-khi-than-rong-hoac-sai-id  [P2]  Cần nghiệm thu độc lập parity Linux
TỆP/DÒNG: scripts/nlm-credential-refresh.ps1:758-784,836-869; scripts/tl_gws.py:125-143,229-263.
VẤN ĐỀ: biểu hiện U+001C–001F và BOM của lượt 3 có bản vá/tập test Windows dương, nhưng 101 dạng/168 byte Linux ở head 183d1f5 chưa được reviewer tự chạy; không đủ điều kiện lịch sử §8.3 để đóng lớp.
ĐÃ THỬ VÁ: có — bảng trắng chung và stdout byte/ConvertTo-StageText.
ĐÃ THỬ NGHIỆM: bảng 35/35 equal=True; Windows Tests.ps1 32/0 có ca âm tương ứng; Linux KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: vừa; không khẳng định có lệch còn tồn tại.

### linux-subreaper-khong-thu-hoi-zombie  [P2]  Chưa đo lại việc thu hồi zombie
TỆP/DÒNG: scripts/nlm-credential-refresh.ps1:413-455; scripts/nlm-credential-refresh.Tests.ps1:969-996.
VẤN ĐỀ: waitpid được thêm và ca v tồn tại, nhưng Windows bỏ qua ca v. Claim bốn chu kỳ zero zombie ở Linux chưa có phép đo độc lập tại head cuối.
ĐÃ THỬ VÁ: có — Invoke-ReapAdopted gọi waitpid WNOHANG sau Stop-OperationTree.
ĐÃ THỬ NGHIỆM: đọc mã; Linux runtime KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: thấp về lỗi còn tồn tại; cao về khoảng trống nghiệm thu.

### khai-rong-hon-phep-do-trong-changelog-runbook  [P3]  Mô tả stage_failure thiếu nhánh containment sau stage
TỆP/DÒNG: references/RUNBOOK.md:749,752; changelog.d/wp-710.md:85.
VẤN ĐỀ: RUNBOOK nói stage_failure cho lệnh stage đã gọi nhưng không rc0 và mới cảnh báo upload có thể xảy ra ở đó. Code cho trường hợp sau stage mà job_unknown xuất inconclusive/tree_containment. Changelog kết bằng định nghĩa stage_failure có thể đã upload, bỏ sót status kia. Các con số 9 mutant/30 vòng không có script kèm để reviewer xác minh.
ĐÃ THỬ VÁ: có — đã thu hẹp parity 101/168 về Linux, nhưng tài liệu g4 chưa bao nhánh mới.
ĐÃ THỬ NGHIỆM: H1 branch projection; Linux và 9/30 script Executor KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về mâu thuẫn nhãn; thấp về các con số không tái lập.

### huong-dan-cu-con-lech-sau-va-ngoai-write-set  [P3]  Hướng dẫn cũ còn nguyên ngoài sáu tệp
TỆP/DÒNG: scripts/tl_core/cli.py:145; scripts/nlm-auto-refresh.sh:76-85; references/COWORK_PROJECT.md:83,94; docs/WORKFLOW_RASOAT_TU_DONG.md:274,362.
VẤN ĐỀ: lời hướng dẫn dựa nlm login/login --check hoặc nuốt rc của stage vẫn còn, có thể khiến người vận hành bỏ qua đường refresh/canary và nhãn lỗi mới. Những tệp này ngoài write set của WP710.
ĐÃ THỬ VÁ: không trong head này; cần packet kế nhiệm có chủ và scope riêng.
ĐÃ THỬ NGHIỆM: git diff cc020e0 ed12889 trên bốn tệp trên rỗng; rg cho các dòng dẫn. Không thử LIVE.
ĐỘ TIN: cao.

## ĐẾM LỚP MỞ

| P1 | P2 | P3 | tổng |
|---:|---:|---:|---:|
| 0 | 4 | 2 | 6 |

Phân loại lớp mở theo §8.3: hai lớp P2 có lỗi control flow ở head này; hai lớp P2 khác thiếu phép đo Linux nên chưa được tuyên bố đóng. Không tạo HINT.patch vì các hướng sửa liên quan runtime/authority của Packet sensitive; chỉ mô tả bằng lời.

## TRẠNG THÁI CHECKOUT CUỐI

git -C cay-kho status --porcelain
(output rỗng, rc 0; HEAD ed1288908e533491456f320e3ce07081f129c0a7, tree 1f0bf9f17fed5ef1e44c05376ae17881d88cc653)

