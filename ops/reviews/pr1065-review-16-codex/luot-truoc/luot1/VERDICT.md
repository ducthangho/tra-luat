verdict: changes_requested
reviewed_sha: b0814f4a4c6dc4793b02865c6f7915b316224cdb

Kết quả: 1 P0, 3 P1, 2 P2, 0 P3.

- Reviewer: Codex, họ model OpenAI; provider theo vai kho: codex/OpenAI. Tên model phục vụ cụ thể: KHÔNG ĐO ĐƯỢC từ sandbox, không suy từ tên công cụ.
- Execution surface thực tế: API agent với functions.exec/exec_command trên Linux; transport: machine/local; không tự khai Codex CLI/Desktop hoặc ChatGPT Web.
- Phiên review: runs/5821884e; độc lập với executor Claude; github_submitter_identity: null (không đăng GitHub).
- Reviewed tree: `0c5fd54bb260b0aea1f6b6d341906fa8743b3605`; base: `4afbe68c9a6b6326a04dd4c0bc419969d1426e2e`; review class đánh giá: sensitive (SYSTEM/admin/ACL).
- PROMPT.md và prompt.snapshot cùng SHA256 `34cc5f0bf1d402e4143570ee9e3ca49bcef665811dda4f3991bcfd3d02af1126`.
- Finding cần ưu tiên: `giao-acl-theo-junction` [P0, tĩnh/native chưa đo]; sau đó checksum sai tên, Node không đọc được phiên bản, và cấu hình lịch bị mất [P1]. Không có approval/land/deploy authority được tạo bởi verdict này.

## BẢNG ĐO

| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Exact HEAD / diff | 3 tệp mới, 515/135/47 dòng | `git -C cay-kho rev-parse HEAD; git -C cay-kho diff --stat <base> <head>` → đúng SHA; 3 files, 697 insertions; H1 | Có |
| Test Windows tại HEAD | Executor khai 38/38 | Linux: `cd cay-kho; TL_TEST_PYTHON=python3 ../pwsh/pwsh -NoProfile -File ops/vm/cap-nhat-cong-cu_test.ps1` → **36/36**, rc0; H1 | Windows KHÔNG ĐO ĐƯỢC; không đồng nhất mẫu số |
| Test với script 6733d09 | Executor khai 36/38 | Không dùng lời khai làm kết quả của reviewer; đối tượng review là b0814f4… | KHÔNG ĐO ĐƯỢC / không chạy lại head khác |
| Bộ test khoá các chốt quan trọng | Có test hành vi và test tĩnh | `python3 probes/run-mutations.py` → 4/7 mutant sống trên Linux, 3/7 bị giết; H3 | Không: finding P2 |
| HeThong không gọi exe qua PATH | Đường tuyệt đối Program Files/System32 | `probes/audit-commands.ps1` → Git/gh/Node/pwsh/icacls/msiexec đều đường tuyệt đối; ScheduledTasks vẫn autoload; H8 | Khớp lời gọi trực tiếp; VM env/module/dependency chưa đo |
| Script chạy SYSTEM ở Program Files chỉ admin ghi | Copy vào Program Files rồi tạo action SYSTEM | `probes/registration.ps1` → copied-exact-script=True, action trỏ bản copy; `-ReparseProbe` → ACL thao tác qua alias user tới chính thư mục ấy; H6–7 | Không đủ: finding P0 |
| Thư mục installer chỉ SYSTEM+Administrators | Bỏ thừa kế, cấp F cho 2 SID | `probes/temp-acl.ps1` → đúng /inheritance:r và 2 SID, rc7 ném lỗi; H9 | Đúng đối số; ACL/TOCTOU Windows KHÔNG ĐO ĐƯỢC |
| Nguồn băm đúng tài sản | digest → checksum cùng release → Node sums | `probes/checksums.ps1` → wrong-filename Save accepted=True; H2 | Không: finding P1 |
| Không có băm thì từ chối | Fail-close | `probes/checksums.ps1; probes/null-inputs.ps1` → null/rỗng/63 ký tự đều ném hoặc trả null, Save không trả thành công; H2 | Có trong các ca đo |
| Checksum có Content byte[] | Chuyển UTF8 trước regex | `probes/checksums.ps1` → bytes-checksum correct=True | Có |
| Node chỉ nâng cùng major | 24 → LTS 24, major mới cần chủ kho | `probes/system-flow.ps1` → success 24.1.0→24.2.0; unknown-version→installer 26.2.0; H4 | Không khi phiên bản không đọc được: P1 |
| Đặt cờ trước cài Node, phục hồi Commander | Kể cả MSI hỏng giữa chừng | `probes/system-flow.ps1 -Mode msi-failure` → installer flag=True rồi stop/start/state; download-failure không restart; H4 | Có ở luồng stub; Windows thực KHÔNG ĐO ĐƯỢC |
| Mã thoát 0/1/2/3/4/5/6 | Theo chú thích đầu script | `probes/exit-codes.py` + `probes/entry-slices.ps1` → đo logic 0–6; invalid-scope/unknown-argument ra 1 thay vì 2; H5 | Sai phạm vi tham số: P2; native Windows chưa đo |
| Write-Error không làm mất rc | Dùng Write-Loi ra stderr | `probes/exit-codes.py` → Write-Loi/catch rc6, Write-Error/catch rc1; mutation Write-Error → 34/36; H3/5 | Có |
| ScheduledTask cần EA Stop tường minh | Register 2 task có EA Stop | `probes/audit-commands.ps1` / registration stub → dòng 453,459 có Stop; mutant bỏ Stop → 35/36; start/state Commander cũng Stop; H3/6/8 | Đúng đối số; CDXML native KHÔNG ĐO ĐƯỢC |
| Lịch 2 tuần CN 02:30 / 03:30 | HeThong rồi NguoiDung, StartWhenAvailable | `probes/registration.ps1` → WeeksInterval=2, Sunday 02:30/03:30; source 445 StartWhenAvailable/IgnoreNew/limit 2h | Đúng đối số; không có phụ thuộc hoàn tất giữa hai task |
| Tham số đăng ký dùng lại khi chạy lịch | Có các tham số MayDich, thư mục công cụ, Commander | `probes/registration.ps1` → custom MayDich/tools/Commander persisted=False; H6 | Không: P1 |
| Quyền task user là đọc/chạy, logon bằng password | GRGX, Limited; SYSTEM Highest | AST dòng 450,459–470: đúng principal/runlevel/ACE; stub dừng trước credentials/COM | Ý định khớp, DACL hiệu lực/logon KHÔNG ĐO ĐƯỢC |
| Đường nhật ký | Tools/nhat-ky-cap-nhat, ProgramData/tra-luat-cap-nhat | Source 508–513 qua `nl -ba`; AST summary tạo JSON scratch với ok/loi đúng; H5 | Khớp đường mặc định; quyền thư mục Windows chưa đo |
| ChiKiem không cài | Vẫn đo phiên bản | `probes/user-layer.ps1` → user-controlled-exe-executed=True, mode=ChiKiem; H10 | Khớp “không cài”; không phải sandbox thực thi |
| Bộ test chưa nối CI | README dòng 47 | `rg -n 'cap-nhat-cong-cu|ops/vm|pwsh|powershell|_test\.ps1' cay-kho/.github/workflows` → chỉ launcher Windows và don-nhanh_test.ps1, không có suite VM | Không thấy wiring trực tiếp; không coi đây là CI pass |
| Gợi ý test có răng | Reviewer tạo riêng | `python3 probes/run-regressions.py` → HEAD 4/7, candidate scratch 7/7; 3 mutant trên candidate đều 6/7; patch áp được ở bản sao | Có, phạm vi như ghi dưới HINT.patch |

## BẢNG SĂN

Bắt đầu: đọc chỉ thị, xác minh SHA và hướng dẫn; chưa kết luận. Chỉ đọc cây `cay-kho/`, mọi phép thử biến đổi sẽ dùng bản sao ngoài cây.

HƯỚNG 1: định danh cây và bộ test nguyên bản
  giả thuyết : cây lệch SHA hoặc bộ test không chạy đủ trên Linux.
  lệnh       : `git -C cay-kho status --short; git -C cay-kho rev-parse HEAD; git -C cay-kho diff --stat 4afbe68c9a6b6326a04dd4c0bc419969d1426e2e b0814f4a4c6dc4793b02865c6f7915b316224cdb`; trong `cay-kho/`: `TL_TEST_PYTHON=python3 ../pwsh/pwsh -NoProfile -File ops/vm/cap-nhat-cong-cu_test.ps1`.
  output     : status rỗng; HEAD `b0814f4a4c6dc4793b02865c6f7915b316224cdb`; 3 files changed, 697 insertions(+); `cap-nhat-cong-cu tests: 36/36 ca QUA`, rc=0.
  kết luận   : KHÔNG PHẢI LỖI ở định danh/baseline. 38/38 trên Windows là lời khai executor, KHÔNG ĐO ĐƯỢC tại Linux; không gộp 36/36 thành 38/38.

HƯỚNG 2: checksum ràng buộc đúng tài sản, null/rỗng và byte[]
  giả thuyết : `Get-BamTaiSan` nhận băm của tài sản khác khi đọc `<asset>.sha256`.
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/checksums.ps1` (hàm `Invoke-WebRequest` bị thay bằng stub nội bộ, KHÔNG mạng; hàm sản phẩm đọc trực tiếp từ exact HEAD).
  output     : `wrong-filename returned=eac2d69b9d0388c397c8aa582ab9ab9ac38f376cac9b90cd3f4f21ef76623280; expected=null`; `wrong-filename Save accepted=True; downloads=OFFLINE:checksum,OFFLINE:asset`; hash-length=0,0,3,63 đều rejected=True; bytes-checksum correct=True; generic-wrong-name rejected=True; generic-bare-hash rejected=True; find-null=True; text-null-length=0. Đầy đủ: `evidence/checksums.log`.
  kết luận   : LỖI — nhánh đặc cách ở dòng 194 nhận token hash đầu dòng mà không kiểm tên. Null/rỗng và byte[] trong các ca còn lại fail-close đúng.

### checksum-khac-ten  [P1]  Tệp checksum riêng ghi tên tài sản khác vẫn được nhận
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:194` (đọc), `:237–240`, `:380–383` (hai tầng dùng kết quả).
VẤN ĐỀ: Với tài sản `wanted.msi` không có digest và checksum asset `wanted.msi.sha256` chứa `<hash>  different.msi`, nhánh regex trả hash ngay; `Find-BamTrongTep` không được hỏi. `Save-CoKiemBam` chấp nhận payload trùng hash ấy. Đã mất quan hệ giữa tên tài sản và băm; đây là đầu vào phản chứng offline, KHÔNG khẳng định release chính thức hiện tại có dữ liệu sai, cũng KHÔNG khẳng định khai thác SYSTEM đã chạy trên Windows.
ĐÃ THỬ NGHIỆM: `./pwsh/pwsh -NoProfile -File probes/checksums.ps1` → `wrong-filename Save accepted=True`; log tại `evidence/checksums.log`.
ĐỘ TIN: cao.
GỢI Ý VÁ: tại `Get-BamTaiSan`, chỉ đặc cách khi toàn bộ nội dung là hash trần (cho phép khoảng trắng), còn dòng có tên bắt buộc đi qua đối chiếu tên; thêm ca tên sai/đúng, checksum trần và nhiều dòng; đột biến trả lại regex tiền tố phải đỏ. Nguy cơ: loại nhầm định dạng checksum hợp lệ có chú thích; phải quy định định dạng được hỗ trợ và từ chối rõ phần còn lại.

HƯỚNG 3: đo độ nhạy bộ test bằng đột biến độc lập
  giả thuyết : bộ test đo hàm thuần nhưng không khoá đường gọi an ninh và phục hồi.
  lệnh       : `python3 probes/run-mutations.py` — tạo từng cây `mutants/<tên>/`, chỉ chép script/test/bản kê/requirements từ HEAD; chạy cùng pwsh với `TL_TEST_PYTHON=python3`.
  output     : baseline=36/36 rc0; no-save-assert=36/36 rc0; no-host-guard=36/36 rc0; node-different-major=33/36 rc1; no-task-stop=35/36 rc1; no-acl-inheritance-reset=36/36 rc0; no-node-restart-flag=36/36 rc0; write-error-before-exit=34/36 rc1. Log từng cây trong `evidence/mutation-*.log`; bảng máy đọc `evidence/mutations.json`.
  kết luận   : LỖI — 4/7 đột biến sống trên Linux. Chốt same-major, Register-ScheduledTask -ErrorAction và Write-Loi có răng ở các ca hiện có. Chốt tên máy có ca riêng trong nhánh Windows, chưa chạy Windows; không suy rằng ca ấy cũng sống trên Windows.

### test-thieu-duong-tich-hop  [P2]  Bộ test không bắt được bỏ kiểm băm, ACL thư mục tải và phục hồi Commander
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu_test.ps1:32–56`, `:96–101`, `:103–131`; sản phẩm `:204`, `:213`, `:385`, `:400–408`.
VẤN ĐỀ: Kiểm trực tiếp Assert-Bam không bảo vệ việc Save-CoKiemBam thật sự gọi nó. Không có ca đo lệnh ACL của New-ThuMucTai hoặc đường cài Node → restart, nên các đột biến tương ứng vẫn xanh hoàn toàn. Mất chốt tên máy cũng không được phát hiện trên Linux do thoát 4 trước nhánh này; phần đó là giới hạn nền, không phải chứng cứ ca Windows vô hiệu.
ĐÃ THỬ NGHIỆM: `python3 probes/run-mutations.py` → ba đột biến no-save-assert/no-acl-inheritance-reset/no-node-restart-flag đều 36/36 rc0; baseline cũng 36/36.
ĐỘ TIN: cao.
GỢI Ý VÁ: bổ sung test offline stub IWR/installer/icacls/ScheduledTasks, đo trực tiếp Save-CoKiemBam với băm sai và đo thứ tự cài Node/đặt cờ/restart; kiểm tham số /inheritance:r, không chỉ regex cả tệp. Phải giết chính ba đột biến trên. ACL hiệu lực và identity task vẫn cần ca Windows thật; stub chỉ chứng minh luồng và đối số. Nguy cơ: stub trả sẵn kết quả mong đợi, tạo xanh giả; phải đối chiếu lời gọi và dùng payload/file thật cho kiểm băm.

HƯỚNG 4: Node cùng major và cờ phục hồi trước khi gọi installer
  giả thuyết : cài Node có đường không đặt cờ hoặc bản không đọc được bị nâng major tự động.
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/system-flow.ps1 -Mode <success|msi-failure|download-failure|unknown-version|no-lts|up-to-date>`; hàm `Invoke-TangHeThong` từ exact HEAD, mọi hàm mạng/MSI/ScheduledTasks là stub có nhật ký lời gọi, không cài gì.
  output     : success → chọn 24.2.0 từ 24.1.0, installer thấy `flag=True`, stop/start/state Commander, `EA=Stop` ở start/state; msi-failure → node `loi offline-msi-failed` nhưng vẫn restart; download-failure → nodeFlag=False, không gọi MSI/restart; unknown-version → `existing-node-version-unreadable`, `save:node-v26.2.0-x64.msi`, MSI thấy flag=True, ghi `cai_moi`; no-lts → nodeFlag=False, can_quyet_dinh; up-to-date → nodeFlag=False, giu. Chi tiết `evidence/system-*.log`.
  kết luận   : LỖI ở việc gộp không đọc được phiên bản với chưa cài. Không tìm được đường cài Node bỏ cờ trong luồng bình thường; cờ đúng cả MSI ném lỗi. Khả năng MSI thật giết pwsh/Commander và quyền/State thực tế: KHÔNG ĐO ĐƯỢC trên Linux.

### node-khong-doc-duoc-van-nang-major  [P1]  Không đo được phiên bản Node đang có vẫn chọn LTS major mới nhất
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:136–137`, `:178–181`, `:355–365`.
VẤN ĐỀ: `Get-PhienBanLenh` trả cùng `$null` khi binary vắng và khi binary tồn tại nhưng lỗi/không khớp output. `Select-NodeLts` coi cả hai là chưa cài và lấy LTS mới nhất. Khi Node đang cài major 24 nhưng truy vấn phiên bản hỏng, index có 26 thì đường HeThong gọi installer 26 mà không có `can_quyet_dinh`, trái cam kết không tự đổi major. Phản chứng dùng stub mô phỏng không đọc được, không khẳng định Node trên VM đang hỏng.
ĐÃ THỬ NGHIỆM: `./pwsh/pwsh -NoProfile -File probes/system-flow.ps1 -Mode unknown-version` → `call=save:node-v26.2.0-x64.msi`, `call=msi:node flag=True`, kết quả node `cai_moi`. Ca success cùng index, phiên bản 24.1.0 đọc được → chọn 24.2.0 và báo major 26 cần quyết định.
ĐỘ TIN: cao với luồng điều kiện; điều kiện trên VM chưa đo.
GỢI Ý VÁ: trong nhánh Node của Invoke-TangHeThong, phân biệt `Test-Path` binary với kết quả đo phiên bản; binary tồn tại mà không đo được thì ghi lỗi/cần quyết định và không tải/cài. Giữ hành vi cài mới khi binary thật sự vắng. Khoá bằng hai ca cùng trả null nhưng tồn tại/vắng khác nhau; đột biến gộp lại phải đỏ. Nguy cơ: binary hỏng sẽ cần chủ kho can thiệp, vì vậy nhật ký phải nói rõ cách phục hồi có chủ ý.

HƯỚNG 5: mã thoát, tham số sai và Write-Error
  giả thuyết : Write-Error nuốt mã thoát hoặc lỗi binding không ra mã 2 như khai.
  lệnh       : `python3 probes/exit-codes.py` (tiến trình pwsh con riêng mỗi ca; nạp hàm nguyên bản, không mạng).
  output     : non-windows rc4 (`chỉ chạy trên Windows`); invalid-scope rc1 (`Cannot validate argument on parameter 'PhamVi'`); unknown-argument rc1 (`A parameter cannot be found...`); load-functions rc0; missing-manifest rc2 (`không thấy cong_cu.yaml...`); write-loi-then-exit6 rc6; write-error-then-exit6 rc1. Đầy đủ `evidence/exit-codes.json`, `evidence/exit-codes.log`. Lượt thử missing-manifest đầu không đặt ThuMucCongCu nên vướng ổ C: trên Linux (rc1); đã sửa harness sang đường dẫn scratch, không sửa sản phẩm.
  kết luận   : LỖI ở hợp đồng “tham số sai → 2”: binding PowerShell thoát 1 trước thân script. Write-Loi hiện tại giữ đúng mã 6; thay bằng Write-Error thì mất mã như chú thích. Mã 3/5 và catch đăng ký CDXML trên Windows thật: KHÔNG ĐO ĐƯỢC trên Linux.

### ma-thoat-tham-so-sai  [P2]  Hợp đồng mã 2 không áp dụng cho lỗi tham số của PowerShell
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:27–28`, `:32`.
VẤN ĐỀ: Chú thích gộp “thiếu bản kê/tham số sai” vào mã 2, nhưng -PhamVi Sai và tham số không tồn tại đều thoát 1. Lớp gọi dựa vào hợp đồng này không phân biệt lỗi sử dụng với lỗi công cụ. Đây là sai phạm vi lời khai, không phải Write-Loi bị lỗi.
ĐÃ THỬ NGHIỆM: `python3 probes/exit-codes.py` → invalid-scope/unknown-argument rc1, missing-manifest rc2.
ĐỘ TIN: cao.
GỢI Ý VÁ: sửa hợp đồng ở đầu script để ghi rõ lỗi binding do host PowerShell trả 1, mã 2 chỉ cho thiếu bản kê/lỗi do thân script xác nhận; nếu thật sự cần mã 2 cho mọi lỗi tham số thì cần wrapper parse trước binding. Khoá bằng ca tiến trình con cho cả ba loại lỗi. Nguy cơ: đổi wrapper làm thay đổi quoting/tham số chung; phương án rẻ và ít rủi ro là sửa lời khai.

HƯỚNG 6: tham số đăng ký có được giữ trong action và giờ chạy
  giả thuyết : cấu hình -MayDich/-ThuMucCongCu/-TacVuCommander được dùng khi chuẩn bị nhưng bị mất khi tạo Scheduled Task.
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/registration.ps1`; gọi hàm Register-LichCapNhat nguyên bản với OTHER-VM/custom-tools/CUSTOM-COMMANDER; giả lập icacls và cmdlet ScheduledTasks, dừng có chủ ý ở Get-Credential trước Windows COM. Mọi tệp tạo dưới evidence/registration/.
  output     : `custom-tools-created=True; custom-MayDich-persisted=False; custom-tools-persisted=False; custom-Commander-persisted=False`; action chỉ có `-NoProfile -NonInteractive -File ".../ProgramFiles/tra-luat-ops/cap-nhat-cong-cu.ps1" -PhamVi HeThong|NguoiDung`; `copied-exact-script=True`; trigger `{Weekly:true,WeeksInterval:2,DaysOfWeek:Sunday,At:02:30}` và `03:30`; Register HeThong nhận EA=Stop. Đầy đủ `evidence/registration.log`.
  kết luận   : LỖI với cấu hình khác mặc định; thời gian/đường dẫn/action mặc định khớp README trong đối số tạo ra. Đăng ký thật, logon, DACL task và ownership Windows: KHÔNG ĐO ĐƯỢC.

### dang-ky-lam-mat-tham-so  [P1]  Scheduled Task bỏ cấu hình mà lệnh đăng ký vừa dùng
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:35–41`, `:435–439`, `:448–449`.
VẤN ĐỀ: -DangKyLich -MayDich OTHER-VM qua được chốt hiện tại nhưng action không mang -MayDich nên lần chạy lịch quay về TRA-LUAT-WIN và thoát 5. -ThuMucCongCu custom-tools dùng để giao quyền nhưng action quay về C:\Tools; -TacVuCommander CUSTOM-COMMANDER cũng bị mất. Tương tự NlmVenv/VenvKho/HomeCommander có tham số nhưng không được ghi lại. Hành vi mặc định trên TRA-LUAT-WIN không mắc lỗi cấu hình này.
ĐÃ THỬ NGHIỆM: `./pwsh/pwsh -NoProfile -File probes/registration.ps1` → ba trường persisted=False, custom-tools-created=True; action được thu trực tiếp từ hàm sản phẩm, chưa đăng ký task Windows thật.
ĐỘ TIN: cao với action được sinh; mã 5 suy trực tiếp từ guard dòng 484, chưa chạy Windows.
GỢI Ý VÁ: khi sinh action, giữ các tham số runtime được hỗ trợ bằng cấu hình chỉ admin ghi ở Program Files hoặc serialize/quote đầy đủ vào argument; hoặc từ chối rõ mọi cấu hình khác mặc định khi đăng ký. Khoá bằng ca giá trị có khoảng trắng/dấu nháy, đọc action và chạy lại parser trên bản sao. Nguy cơ: nối chuỗi chưa quote mở lỗi injection/parse; cấu hình có schema trong thư mục được bảo vệ tránh phần lớn quoting nhưng phải kiểm ACL.

HƯỚNG 7: reparse point khi admin giao lại ownership/ACL vùng do user quản lý
  giả thuyết : `tlcommander` thay C:\Tools\npm bằng junction tới Program Files\tra-luat-ops trước lần admin đăng ký lại, khiến icacls trao quyền trên bản script SYSTEM.
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/registration.ps1 -ReparseProbe`; xem `evidence/registration-reparse.log` và `evidence/registration/icacls-calls.log`. Symlink Linux dựng trong scratch trỏ từ custom-tools/npm tới ProgramFiles/tra-luat-ops; icacls là shim ghi đối số và đường dẫn resolve, KHÔNG đổi ACL Windows.
  output     : `preplanted-link=SymbolicLink target=.../ProgramFiles/tra-luat-ops`; hàm không từ chối link, chạy tiếp `giao .../custom-tools/npm cho OTHER-VM\tlcommander`; shim nhận `.../custom-tools/npm /setowner OTHER-VM\tlcommander /T /C /Q` và `/grant OTHER-VM\tlcommander:(OI)(CI)M /T /C /Q`; cả hai `resolved=.../ProgramFiles/tra-luat-ops`. Hàm vẫn tới Register HeThong.
  kết luận   : LỖI an ninh phân tích tĩnh: admin đệ quy đổi owner/ACL qua tên trong vùng user kiểm soát, không từ chối reparse, không giữ handle chống đổi đường dẫn. KHÔNG ĐO ĐƯỢC icacls/junction/ACL native hay khai thác SYSTEM trên Windows tại đây; phép đo chỉ chứng minh link được nhận và đối số nguy hiểm thực sự được phát ra.

### giao-acl-theo-junction  [P0]  Đăng ký lại lịch có thể trao quyền sửa script SYSTEM qua junction do tlcommander dựng
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:434–440` (đường đi và icacls đệ quy), `:426` (bản script được chép trước đó), `:448–450` (SYSTEM chạy bản ấy); `ops/vm/README.md:12,27–29` yêu cầu đăng ký lại khi script đổi.
VẤN ĐỀ: Sau lần đăng ký đầu, npm/Python312/bin thuộc tlcommander; đề bài còn xác nhận tài khoản này ghi được C:\Tools. Trước lần đăng ký lại, người dùng có thể thay thư mục bằng junction/reparse trỏ tới C:\Program Files\tra-luat-ops (hoặc đặt reparse trong cây con). Admin chạy bản clone sạch vẫn đi vào các tên ấy bằng New-Item -Force rồi icacls /setowner, /grant M đệ quy. Không có kiểm tra reparse/ancestor, không /L, không chốt chống hoán đổi. Đường nguy hiểm là làm tlcommander có quyền trên script mà tác vụ SYSTEM chạy sau đó; đường dẫn tuyệt đối trong Program Files không cứu được khi chính ACL của nó bị trao lại qua một tên khác. Đây là finding tĩnh P0; hiệu lực native cần tái hiện Windows trước khi coi là exploit đã chứng minh.
ĐÃ THỬ NGHIỆM: `./pwsh/pwsh -NoProfile -File probes/registration.ps1 -ReparseProbe` → cả /setowner và /grant nhận đường link, resolve vào thư mục chứa bản script SYSTEM; không có chặn. KHÔNG ĐO ĐƯỢC icacls Windows thật vì sandbox Linux không có ACL/NTFS junction/SYSTEM; shim không chứng minh DACL đích đã đổi.
ĐỘ TIN: vừa (luồng và thiếu chốt đo trực tiếp; hiệu lực icacls/junction native chưa đo).
GỢI Ý VÁ: tại bước provisioning ACL, bỏ việc admin đệ quy đi lại cây đã bàn giao cho user mỗi lần đăng ký lịch. Tách migration một lần trong vùng có parent do admin giữ; từ chối reparse ở toàn bộ chuỗi đường dẫn/cây và phải chống được thay thế giữa kiểm tra với thao tác, không coi Get-Item rồi icacls là đã đóng TOCTOU. /L riêng lẻ cũng không bảo vệ ancestor junction. Test Windows: dựng junction npm → thư mục đích giả có ACL admin, gọi đăng ký bằng admin, đòi từ chối trước icacls và xác minh owner/DACL đích không đổi; thêm ca hoán đổi trong lúc chạy và link ở cây con. Nguy cơ: npm/Python có link hợp lệ; phải quy định cách migrate chúng, tránh vô tình chặn nâng cấp hoặc chỉ vá link ở gốc mà bỏ cây con.

HƯỚNG 8: lệnh trần, module autoload, PATH và đường script nguồn
  giả thuyết : đường dẫn exe tuyệt đối chưa loại được nạp module từ thư mục không tin cậy.
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/audit-commands.ps1`; `./pwsh/pwsh -NoProfile -File probes/module-path.ps1`.
  output     : AST `parse-errors=0; pwsh=7.6.9; platform=Unix`; liệt kê từng lệnh và dòng trong `evidence/audit-commands.log`; module probe `source-command-line=445`, `autoload-marker=True; user-module-result=True; module=.../user-modules/ScheduledTasks/ScheduledTasks.psm1`; `assumption=PSModulePath-was-deliberately-prepended-by-probe; VM-SYSTEM-module-path-not-measured`.
  kết luận   : KHÔNG ĐO ĐƯỢC đường khai thác module/PATH trên VM. Đã chứng minh cơ chế autoload vẫn còn khi một PSModulePath không tin cậy được cung cấp; không chứng minh tlcommander sửa được PSModulePath của SYSTEM/tladmin. Không gán P0 chỉ từ biến môi trường do chính reviewer chèn.

Rà đường thực thi quyền cao (phân biệt finding với điều kiện chưa xác minh):

| Đường | Dòng cụ thể | Đánh giá |
|---|---|---|
| Version probe Git/gh/Node/pwsh | script 346–355, 178–181 | Exe được ghép từ ProgramFiles, không có Get-Command/PATH trong đường HeThong; tin ProgramFiles/registry/dependencies của exe. Không đo Windows filesystem thực. |
| Cài Git / gh / Node / pwsh | 381–390, 202–205, 338 | Sau Save-CoKiemBam; Git chạy bằng đường tải tuyệt đối, MSI qua SystemRoot/System32/msiexec.exe. Không thấy đường trần msiexec/icacls trong script. DLL/custom action bên trong installer chính thức chưa có artifact để kiểm, không được tải. |
| Cmdlet PowerShell thường | 355–408 và helpers trong audit-commands.log | Utility/Management và pipeline gọi bằng tên cmdlet; không gán đồng nghĩa với exe tra PATH. Module path/nguồn cmdlet Windows thật chưa đọc được. |
| ScheduledTasks autoload | 402–405, 445–453, 459, 472 | Script không đặt PSModulePath/Import-Module từ thư mục cố định. Probe chứng minh module giả chạy nếu được đưa vào module path trước; điều kiện attacker điều khiển module path của đặc quyền chưa được chứng minh. |
| Chép script để SYSTEM chạy | 419, 424–426, 448–450 | Nguồn là PSCommandPath của file đang chạy, không có kiểm hash/ACL nguồn. README 15–23 yêu cầu clone vào TEMP riêng admin, cấm C:\work. Chạy file user sửa được đã mất an ninh trước khi thân script tự kiểm; phải bảo vệ nguồn từ caller. Không suy bản clone đang ở SHA review vì README clone nhánh mặc định, không pin SHA. |
| Giao lại owner/quyền qua C:\Tools | 434–440 → 448–450 | Finding `giao-acl-theo-junction` P0: đường alias có thể làm chính script Program Files trở thành user-writable. |
| git trong hướng dẫn chạy bằng admin | README 20–22 | `git clone` là tên trần; nếu PATH của admin có C:\Tools đứng trước Git chuẩn thì chạy mã user. PATH của tladmin/SYSTEM thật KHÔNG ĐO ĐƯỢC; script không chứng minh hay đóng điều kiện này. Nên hướng dẫn dùng đường Git được bảo vệ và xác minh nguồn clone. |
| Tầng NguoiDung được admin/SYSTEM gọi trực tiếp | 32, 255–269, 296, 320–327, 496–500 | Chỉ HeThong có guard quyền; không có guard từ chối elevated NguoiDung. Caller đặc quyền chọn mặc định/NguoiDung sẽ chạy Python/claude/codex/nlm do user sửa được, kể cả ChiKiem. Task SYSTEM được sinh đúng với -PhamVi HeThong; README hướng dẫn user layer dưới tlcommander. Không gộp việc caller đặc quyền gọi ngoài cách dùng công bố với khai thác task mặc định. |

HƯỚNG 9: thư mục tải, lỗi icacls và TOCTOU kiểm băm → chạy
  giả thuyết : lỗi icacls bị bỏ qua hoặc thư mục không yêu cầu bỏ thừa kế.
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/temp-acl.ps1` (icacls shim trả lần lượt 0 và 7, không sửa ACL).
  output     : `icacls-rc=0 returned=/tmp/tl-cap-nhat-... exists=True`; `icacls-rc=7 thrown=icacls thư mục tải hỏng:`; cả hai native-call có `/inheritance:r /grant:r *S-1-5-18:(OI)(CI)F *S-1-5-32-544:(OI)(CI)F`; `NOTE=icacls-is-shim; native-Windows-ACL-not-measured`.
  kết luận   : KHÔNG PHẢI LỖI ở chốt rc/đối số đã đo; ACL hiệu lực và TOCTOU native KHÔNG ĐO ĐƯỢC. Dòng 209–214 dùng temp của process, tạo thư mục rồi mới siết ACL, /grant:r không xoá mọi ACE explicit. Không được coi đây là chứng minh an toàn nếu TEMP/ancestor cho user đổi tên/reparse hoặc mở handle trước khi ACL siết; chưa có bằng chứng cấu hình ấy trên VM. Sau đó tệp được băm dòng 204 rồi mở lại để chạy dòng 388/338, nên an toàn của khoảng giữa phụ thuộc ACL/ancestor/handle, không phải hash tự đóng TOCTOU. Không có tệp nào được tải/cài bởi reviewer.

HƯỚNG 10: tầng NguoiDung vẫn thực thi mã công cụ khi ChiKiem
  giả thuyết : chọn ChiKiem có thể được hiểu nhầm là không chạy mã công cụ.
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/user-layer.ps1` — Python giả là file chạy thật trong vùng scratch mô phỏng user quản lý; mọi release lookup được stub để không mạng.
  output     : `user-controlled-exe-executed=True; process-linux-uid=0; mode=ChiKiem; scope=NguoiDung`; xem `evidence/user-layer.log`; mode ChiKiem vẫn in Python 3.12.0 và gọi chương trình Python để đọc ghim/metadata. Đây là phép đo hàm nguyên bản trên Linux, không chạy Windows entrypoint.
  kết luận   : KHÔNG PHẢI LỖI so với cách dùng công bố: ChiKiem là không cài, vẫn phải gọi công cụ để đo phiên bản. Điều kiện cần giữ: chỉ tlcommander/tài khoản không đặc quyền chạy tầng này. Không dùng ChiKiem như cơ chế cô lập khi admin điều tra binary không tin cậy.

Bổ sung HƯỚNG 2 — ma trận đầu vào null/rỗng:
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/null-inputs.ps1` (IWR stub, không mạng).
  output     : `Get-Bam(null,null)` và `(empty,empty)` đều is-null=True; Find(null,null)/Find(named-line,null) đều is-null=True; Text(null) length=0; Assert(null,valid)/Assert(null,null) đều THREW; Save(valid-dir,null-hash) THREW `không có sha256 hợp lệ...`; Save(null-dir,valid-hash) THREW lỗi binding; Save(valid-dir,null-name) THREW lỗi ghi vào thư mục. Đầy đủ `evidence/null-inputs.log`.
  kết luận   : KHÔNG PHẢI LỖI fail-open trong các ca null/rỗng này. Save vẫn tải trước khi nhận ra hash rỗng (dòng 203 trước 204), nhưng không trả đường dẫn thành công cho caller để chạy; finally ở caller dọn thư mục.

Bằng chứng gợi ý test đã tự đo trên bản sao:
- `python3 probes/run-regressions.py` → nguồn HEAD nguyên nội dung: **4/7**, rc1 (đỏ đúng 2 ca checksum và 1 ca Node unknown-version).
- Candidate chỉ trong `mutants/review-candidate-in-scratch/` sửa regex checksum + từ chối Node binary tồn tại/phiên bản không đọc được: **7/7**, rc0. Đây là bằng chứng phản chứng có thể sửa được, không phải phê duyệt candidate hay sửa cây review.
- Trên candidate đó, bỏ riêng Assert trong Save, /inheritance:r, hoặc cờ Node đều còn **6/7**, rc1; mỗi lần đỏ đúng ca tương ứng. `evidence/regressions.json` và `evidence/regressions-*.log` lưu output và exit code thật.
- `HINT.patch` chỉ thêm `ops/vm/cap-nhat-cong-cu_review_test.ps1`, định dạng `patch -p0` từ gốc cây. Test kiểm ACL bằng AST chỉ đo đối số, không phải ACL native; test Node/MSI là stub luồng, không gọi mạng/cài gì. Test không đóng P0 junction hay kiểm việc truyền cấu hình lịch; hướng vá và test Windows cần thiết nằm tại từng finding.
- `patch -p0 --dry-run -d mutants/baseline < HINT.patch` → `checking file ops/vm/cap-nhat-cong-cu_review_test.ps1`, rc0. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

Kiểm HINT.patch trên bản sao có cấu trúc thật: áp vào `mutants/hint-check/` bằng `patch -p0`, rc0; bộ test cũ trong cây ấy vẫn **36/36**, rc0; tệp test gợi ý chạy với đường mặc định → **4/7**, rc1 như dự kiến trên HEAD chưa vá. Bộ test cũ trên candidate scratch cũng **36/36**, rc0. Lệnh và output/exit code lưu `evidence/hint-validation.json`; không áp patch vào cay-kho/.

Bổ sung HƯỚNG 5 — đo riêng các đoạn entrypoint nguyên văn, không giả làm Windows thật:
  lệnh       : `./pwsh/pwsh -NoProfile -File probes/entry-slices.ps1 -Mode <summary-ok|summary-error|rights|host|registration-error>`; parser lấy nguyên AST dòng 502–515, 496, 484 hoặc 490–495 từ exact HEAD; cung cấp identity/quyền giả và Register-LichCapNhat ném lỗi offline.
  output     : summary-ok rc0, JSON `{ok:true,loi:0,tong:1}`; summary-error rc1, JSON `{ok:false,loi:1,tong:1}`; rights rc3; host rc5 với WRONG-HOST; registration-error rc6 với `-DangKyLich hỏng: injected-registration-error`. `evidence/entry-slices.json` lưu cả output nguyên văn và rc.
  kết luận   : KHÔNG PHẢI LỖI trong logic các đoạn được đo; kết hợp phép đo script nguyên bản ngoài Windows rc4, thiếu bản kê rc2, đã đo logic 0–6 nhưng chưa đo native identity/CDXML/Task Scheduler. Không thay nhãn thành “Windows integration pass”.

Giới hạn bắt buộc khi đọc verdict:
- P0 junction là phân tích luồng đặc quyền có phản chứng đường dẫn trên Linux; chưa có exploit Windows native hay DACL readback. Cần đo Windows trước khi khẳng định mức khai thác thực tế.
- Không đọc được PSModulePath, PATH, TEMP, ACL, registry hay nội dung task đang tồn tại của tài khoản SYSTEM/tladmin trên VM. Không suy chúng an toàn từ các đường dẫn trong mã.
- Không gọi mạng, không cài công cụ, không đổi lịch, không push/commit/publish. Mọi native Windows command trong harness là shim/stub; chỗ nào lấy nguyên AST/hàm được ghi rõ.
- Chỉ script/test/docs tại reviewed_sha là đối tượng chấm; candidate/mutant/test gợi ý là phản chứng ngoài cây, không phải một HEAD mới đã được review/approve.

Kiểm cuối read-only: `GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain=v1 --untracked-files=all` và `git -C cay-kho diff --exit-code HEAD --` đều output rỗng, rc0; HEAD/tree không đổi; diff --check base→head rc0. `evidence/final-readonly.json` lưu lệnh/output/rc. SHA256 script nguyên bản vẫn `80e66ab4d4928ac7536db291d7c2b0d89ba47cfc9b03890b4c4fb2f0d200fcd4`, trùng bản sao baseline.
