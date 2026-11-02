verdict: changes_requested
reviewed_sha: aedd62077689045b676f5257ee5b6f67f44f8a66

Kết quả: 1 P0, 2 P1, 2 P2, 0 P3.

Review độc lập hoàn tất; chỉ đọc và đo, không sửa `cay-kho/`, không gọi mạng.

## ĐÓNG FINDING LƯỢT 1

| slug | đã đóng? | phép đo (lệnh + output) |
|---|---|---|
| giao-acl-theo-junction | **Chưa đóng lớp**; link trực tiếp đã bị chặn, native Windows chưa đo | `pwsh/pwsh -NoProfile -File probes/registration.ps1 -Mode root-link` → từ chối, icacls=0; `-Mode ancestor-link` và `-Mode swap-parent` → grant resolved=victim/*, tasks=1; H7, evidence/register-*.log. |
| checksum-khac-ten | **Đã đóng** trong phản chứng offline đúng lượt 1 | `pwsh/pwsh -NoProfile -File probes/checksums.ps1` → wrong-name hash_is_null=true, save_accepted=false; bare/đúng tên/nhiều dòng/byte[] accepted=true; H2. |
| node-khong-doc-duoc-van-nang-major | **Đã đóng** trong luồng offline; không làm hỏng cài mới | `pwsh/pwsh -NoProfile -File probes/system-flow.ps1 -Mode unreadable` → tệp tồn tại, installed=false, calls=[]; `-Mode missing` → installed=true, node26, cai_moi; H3. |
| dang-ky-lam-mat-tham-so | **Đóng các ví dụ cũ, chưa đóng đủ lớp** | `pwsh/pwsh -NoProfile -File probes/registration.ps1 -Mode clean` → VM/Tools/venv/profile/account/Commander được giữ; custom_log_preserved=false. `probes/arguments.ps1` → backslash cuối roundtrip=false; H4/H7. |
| ma-thoat-tham-so-sai | **Đã đóng** theo hợp đồng mới | Python subprocess với `pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu.ps1 -PhamVi Sai` → rc2; -DoesNotExist → rc1, được ghi rõ dòng 29; evidence/exit-codes.json; H6. |
| test-thieu-duong-tich-hop | **Ba phản chứng cũ đã đóng; phát sinh thiếu ở Register** | `python3 probes/run-mutations.py` → save-hash-call/download-acl-inheritance/node-recovery-flag nay đều đỏ 50/51; 6 đột biến Register mới vẫn 51/51; H8, evidence/mutations.json. |

## BẢNG SĂN

Các phép đo dưới đây neo đúng SHA; phần cần Windows thật được đánh dấu KHÔNG ĐO ĐƯỢC.

HƯỚNG 1: định danh cây và baseline
  giả thuyết : checkout lệch đối tượng hoặc suite không đạt số ca đã khai.
  lệnh       : `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain`; `sha256sum PROMPT.md runs/caf5756f/prompt.snapshot`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : HEAD=aedd62077689045b676f5257ee5b6f67f44f8a66; tree=11b21f30cb6046c28017a0c71e215e78b0c3d796; status rỗng; hai prompt cùng SHA256 a3fbc3ce135c9eca7462c18b3df479a231c19279f97a7dfdd77f333f9b8e78de; `cap-nhat-cong-cu tests: 51/51 ca QUA`, rc=0.
  kết luận   : KHÔNG PHẢI LỖI ở baseline Linux. Không chứng minh Windows/NTFS/Task Scheduler/MSI.

Định danh reviewer: Codex/OpenAI, họ model OpenAI theo môi trường phiên; không đo được tên model phục vụ cụ thể. Execution surface: API agent, functions.exec/exec_command trên Linux; transport: machine/local; session runs/caf5756f; độc lập với executor Claude; github_submitter_identity=null. Review class: sensitive (SYSTEM/admin/ACL). Quyền ghi chỉ gồm VERDICT và artifact đo ngoài `cay-kho/`; không có authority merge/land/deploy. Nguồn chỉ thị hiện hành là prompt.snapshot của người dùng; phạm vi ops/vm/, loại trừ ops/land/.

HƯỚNG 2: phản chứng checksum khác tên + SHASUMS256 Node
  giả thuyết : bản vá vẫn nhận hash của tài sản khác.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/checksums.ps1 > evidence/checksums.log 2>&1` (IWR stub offline; Get-BamTaiSan và Save-CoKiemBam thật).
  output     : wrong-name: hash_is_null=true, save_accepted=false; bare/right-name/multiline: hash_is_expected=true, save_accepted=true; Node sums khác tên: null=True; Node sums có dòng đúng thứ hai: correct=True; hash rỗng/null/63 ký tự/64 ký tự sai đều accepted=False; rc=0. Đợt đầu fixture switch unroll byte[] thành object[]; phép đo sửa fixture được bổ sung sau HƯỚNG 5.
  kết luận   : KHÔNG PHẢI LỖI ở phản chứng checksum-khac-ten; dữ liệu tên sai không còn được nhận.

HƯỚNG 3: Node có tệp không đo được / cài mới / MSI hỏng / SHASUMS sai
  giả thuyết : chốt Test-CoTheCai chặn thiếu tệp hoặc vẫn nhảy major khi không đọc được.
  lệnh       : `for mode in unreadable missing same-major msi-failure bad-sums; do pwsh/pwsh -NoProfile -File probes/system-flow.ps1 -Mode "$mode" > "evidence/system-$mode.log" 2>&1; done`.
  output     : unreadable: node_exists=true, installed=false, nodeFlag=false, calls=[]; missing: node_exists=false, installed=true, download=node-v26.2.0-x64.msi, hanh_dong=cai_moi; same-major: 24.1.0 -> 24.2.0, node-major=can_quyet_dinh; msi-failure: nodeFlag=true, MSI ném offline-msi-failed, vẫn stop/start/state Commander EA=Stop; bad-sums: installed=false, nodeFlag=false, node=loi vì thiếu sha256; tất cả rc=0 của probe. Payload/ghi tệp/hash thật; HTTP/MSI/ScheduledTasks là stub, không cài gì.
  kết luận   : KHÔNG PHẢI LỖI ở phản chứng node-khong-doc-duoc-van-nang-major và đường cài MỚI. Native MSI/Commander: KHÔNG ĐO ĐƯỢC.

HƯỚNG 4: serialize Scheduled Task và vòng lại parser
  giả thuyết : giá trị có dấu cách, $, backtick, dấu nháy hoặc backslash cuối bị đổi; còn tham số bị bỏ.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/arguments.ps1 > evidence/arguments.log 2>&1`. Lấy chuỗi từ New-DoiSoTacVu tại HEAD, truyền nguyên chuỗi qua ProcessStartInfo.Arguments tới pwsh -File probes/argument-receiver.ps1.
  output     : D:\cong cu: roundtrip=true; D:\literal$money`tick: true; D:\a&b;$(id): true; D:\x"y: bị từ chối. D:\cong cu\: rc=0 nhưng roundtrip=false, ThuMucCongCu nhận cả chuỗi `D:\cong cu" -NlmVenv C:\work\nlm-venv -VenvKho ... -TacVuCommander CMD-KHAC`. Mọi case: has_NhatKy=false, has_ChiKiem=false dù đã đặt giá trị tuỳ biến.
  kết luận   : LỖI — quoting backslash cuối làm mất ranh giới đối số. Có dấu hiệu cấu hình NhatKy/ChiKiem bị bỏ; sẽ kiểm tại đường Register thật. Phép đo parser Linux là thật; Task Scheduler/CreateProcess trên Windows KHÔNG ĐO ĐƯỢC.

HƯỚNG 5: allowlist danh tính và mặt nạ quyền ACL
  giả thuyết : tên giả chứa Administrators được tin, hoặc quyền ghi bị bỏ lọt do so chuỗi.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/acl.ps1 > evidence/acl.log 2>&1`.
  output     : BUILTIN\Administrators/S-1-5-18/NT SERVICE\TrustedInstaller: violations=0; xBUILTIN\Administrators, BUILTIN\AdministratorsEvil, ATTACKER\Administrators, x NT AUTHORITY\SYSTEM, S-1-5-18-evil: violations=2. Tất cả quyền ghi/xoá/đổi ACL/owner có tên trong FileSystemRights (WriteData, CreateDirectories, WriteExtendedAttributes, WriteAttributes, DeleteSubdirectoriesAndFiles, Write, Delete, Modify, ChangePermissions, TakeOwnership, FullControl) đều violations=1. Enum.ToObject(FileSystemRights,1073741826=0x40000002) chứa bit WriteData nhưng ToString thành số, violations=0; 0x40000000/0x10000000 cũng 0. rc=0 sau khi dùng Enum.ToObject thay cast PowerShell (cast đã từ chối enum ngoài miền).
  kết luận   : KHÔNG PHẢI LỖI ở tên giả và các quyền enum có tên. LỖI P2 ở hợp đồng kiểm ACL với mask không nhận diện: helper nhận đầu vào chưa chứng minh an toàn. KHÔNG ĐO ĐƯỢC Get-Acl Windows có trả những mask này hay đã map generic rights; không khẳng định đây là exploit Windows.

Bổ sung HƯỚNG 2: chạy lại fixture byte[] đúng kiểu → `bytes: hash_is_expected=true, save_accepted=true`, rc=0. Không có lỗi byte[] ở sản phẩm.

HƯỚNG 6: mã thoát tham số sai
  giả thuyết : -PhamVi Sai vẫn rc1, hoặc tài liệu tiếp tục khai mọi lỗi binding là rc2.
  lệnh       : Python subprocess gọi `pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu.ps1` với `-PhamVi Sai`, `-DoesNotExist`, không đối số, `-NapHam`; bảng đầy đủ `evidence/exit-codes.json`.
  output     : -PhamVi Sai → rc2, `-PhamVi 'Sai' không hợp lệ`; -DoesNotExist → rc1, `A parameter cannot be found that matches parameter name 'DoesNotExist'.`; mặc định → rc4 `chỉ chạy trên Windows`; -NapHam → rc0. Dòng 27–30 phân biệt -PhamVi sai (2) với tham số không tồn tại do host (1).
  kết luận   : KHÔNG PHẢI LỖI — ma-thoat-tham-so-sai đã đóng đúng phạm vi lời khai mới. Native exit 3/5/6 Windows chưa đo.

HƯỚNG 7: Register thật với symlink ở gốc/cha, hoán đổi cha, ACL và hash sai
  giả thuyết : chỉ kiểm reparse ở gốc cây/con cháu không chặn được ancestor hay hoán đổi; các chốt cuối có được gọi thật không.
  lệnh       : `for mode in clean root-link ancestor-link swap-parent owned acl-reject hash-reject; do pwsh/pwsh -NoProfile -File probes/registration.ps1 -Mode "$mode" > "evidence/register-$mode.log" 2>&1; done`. Dùng hàm Register tại HEAD, tệp và symlink Linux thật, icacls chỉ ghi argv + realpath (KHÔNG đổi quyền), Get-Acl/ScheduledTasks stub; cố ý dừng trước credentials.
  output     : root-link (Tools/npm -> victim) → `từ chối ... có reparse point`, icacls_count=0, tasks=0; clean → icacls_count=9, tasks=1; owned → icacls_count=3, tasks=1 (không lệnh ACL vùng Tools). ancestor-link (Tools -> victim) → icacls_count=9, tasks=1, sáu lệnh setowner/grant resolved=victim/{npm,Python312,bin} dù có /L; swap-parent (shim hoán đổi Tools ngay SAU /setowner đầu, trước /grant) → /setowner resolved=Tools/npm, /grant resolved=victim/npm, tasks=1. acl-reject → `ACL ... không đạt: VM\tlcommander: Modify`, tasks=0. hash-reject → `bản chép ... lệch băm nguồn`, tasks=0. clean action giữ VM/Tools/custom nlm/custom venv/custom profile/tlcommander/CMD-CUSTOM, nhưng custom_log_preserved=false, check_preserved=false. Các probe rc=0; dừng chủ ý OFFLINE-STOP-BEFORE-CREDENTIALS sau action SYSTEM ở các ca không bị chốt từ chối.
  kết luận   : LỖI — finding P0 cũ đóng đường link trực tiếp nhưng chưa đóng lớp ancestor/TOCTOU. /L trên mục đích không loại bỏ reparse ở tiền tố; quét trước rồi gọi native bằng tên không giữ identity của cây. Đích ngoài tra-luat-ops không được audit/reset ở cuối. Đây là bằng chứng dispatch và resolve trên Linux, KHÔNG ĐO ĐƯỢC hiệu lực ACL/owner/junction/leo SYSTEM trên Windows. LỖI P1 còn sót: NhatKy/ChiKiem bị bỏ ở action thật. Các chốt ACL/hash cuối được gọi và từ chối đúng trong luồng stub.

HƯỚNG 8: mutation testing — chốt mới và phản chứng test cũ
  giả thuyết : 51/51 không khoá việc Register dùng helper/chốt ACL/hash, dù helper tự nó được test.
  lệnh       : `python3 probes/run-mutations.py > evidence/mutations-summary.log 2>&1` (15 cây bản sao dưới mutants/, một thay đổi mỗi cây; old/new và lệnh đầy đủ trong evidence/mutations.json; TL_TEST_PYTHON=python3).
  output     : baseline 51/51 rc0. checksum-prefix → 49/51 rc1; unknown-version-helper → 49/51 rc1; unknown-version-call → 50/51 rc1; root-reparse → 50/51 rc1; registration-reparse-call → 50/51 rc1; icacls-L → 50/51 rc1; save-hash-call → 50/51 rc1; download-acl-inheritance → 50/51 rc1; node-recovery-flag → 50/51 rc1. Sáu mutant SỐNG, đều 51/51 rc0: task-argument-call (trả action SYSTEM về chỉ -PhamVi), registration-acl-validation (vô hiệu if vp.Count), registration-copy-hash (vô hiệu so băm), registration-owner-after-copy (bỏ setowner sau chép), registration-inheritance-reset (bỏ /inheritance:r khỏi o4), skip-owned (bỏ nhánh continue). Tổng killed=9, survived=6, total=15; không mutant nào chết do parser/thiếu môi trường.
  kết luận   : LỖI P2 — test-thieu-duong-tich-hop đã đóng ba phản chứng cũ (Save/ACL tải/Commander), nhưng tái xuất ở khối Register mới: 6 chốt chưa có răng. Đã thử >=6 chốt mới, không chỉ đột biến logic cũ. Bỏ chốt tên máy là nhánh Windows không đạt trên Linux, không dùng làm finding mới.

### giao-acl-theo-junction  [P0]  Chưa đóng lớp ancestor reparse và hoán đổi cây giữa các lệnh ACL
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:181` (Find-Reparse chỉ nhìn gốc được đưa vào và con cháu); `:489`–`:495` (giao quyền bằng tên); `:521` (audit chỉ tra-luat-ops).
VẤN ĐỀ: Link trực tiếp ở Tools/npm đã bị chặn. Nhưng các ancestor của Tools/npm không được kiểm/giữ cố định; /L không biến một tên có ancestor liên kết thành handle tới cây đã kiểm. Cả trường hợp Tools là link sẵn lẫn hoán đổi Tools sau /setowner đầu đều cho /grant chạy vào cây khác trong phép đo Linux. Nếu user có thể thay ancestor của vùng cấu hình (đặc biệt đường ThuMucCongCu tuỳ biến trong vùng user sở hữu), có thể hướng basename bin vào thư mục executable/DLL đặc quyền bên ngoài tra-luat-ops; ví dụ cấu trúc Program Files\Git\mingw64\bin mà Git hệ thống phụ thuộc. Reset/audit tra-luat-ops ở cuối không bảo vệ đích ấy. Điều kiện quyền đổi ancestor và ảnh hưởng Git/ACL thực tế phải đo trên VM; không khẳng định đã leo SYSTEM trên Linux.
ĐÃ THỬ NGHIỆM: `pwsh/pwsh -NoProfile -File probes/registration.ps1 -Mode root-link` → icacls=0, từ chối; `-Mode ancestor-link` → 6 lệnh giao quyền resolved=victim/*, tasks=1; `-Mode swap-parent` → /setowner đầu resolved=Tools/npm, /grant kế resolved=victim/npm, tasks=1. Native junction/icacls/ACL/SYSTEM: KHÔNG ĐO ĐƯỢC vì Linux; shim chỉ log đối số/realpath, không đổi DACL.
ĐỘ TIN: cao về thiếu kiểm ancestor và khe identity; vừa về chuỗi khai thác Windows, severity P0 tĩnh như finding lượt 1, không phải exploit đã chứng minh.
GỢI Ý VÁ: ở Register-LichCapNhat, tách giao quyền/migration một lần khỏi đăng ký lại task; không đệ quy tác động lên cây user đang điều khiển. Nếu phải migrate, kiểm cả chuỗi ancestor và giữ parent/identity ổn định trong toàn bộ thao tác; quét thêm một lần không đủ đóng race. Ca khoá: Windows dựng junction ở ancestor, rồi hoán đổi trong khoảng scan/setowner/grant; yêu cầu từ chối trước lệnh tác động và owner/DACL mọi đích đặc quyền không đổi, kể cả ngoài tra-luat-ops. Đột biến bỏ pin/ancestor guard phải đỏ. Rủi ro: migration/reparse hợp lệ có thể bị chặn; cần đường phục hồi có chủ ý, không trao quyền rộng để vượt lỗi.

### doi-so-duong-dan-ket-thuc-backslash  [P1]  Backslash cuối đường dẫn làm gộp các đối số tác vụ
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:172`, `:175`–`:178` (New-DoiSoTacVu).
VẤN ĐỀ: Chỉ bọc giá trị trong dấu nháy kép mà không xử lý chuỗi backslash trước nháy đóng. Ví dụ ThuMucCongCu=D:\cong cu\ sinh `-ThuMucCongCu "D:\cong cu\" -NlmVenv ...`; parser tiến trình con giữ dấu nháy như dữ liệu và nhận toàn bộ tham số sau là một giá trị. Không cần ký tự cấm hay input ác ý; đường dẫn thư mục có backslash cuối là hợp lệ. Không thấy thực thi $/backtick/$(id) trong các ca đã đo.
ĐÃ THỬ NGHIỆM: `pwsh/pwsh -NoProfile -File probes/arguments.ps1` → input D:\cong cu\: rc0 nhưng roundtrip=false; actual.ThuMucCongCu chứa cả `-NlmVenv`, `-VenvKho`, `-HomeCommander`, `-TaiKhoanNguoiDung`, `-TacVuCommander`; các khóa đó không còn trong PSBoundParameters. Chuỗi không có backslash cuối và chuỗi chứa $/backtick/&/; vòng lại đúng. Đây là parser tiến trình con Linux thật; Task Scheduler Windows chưa đo.
ĐỘ TIN: cao về serialize/round-trip, vừa về execution surface Windows chưa chạy.
GỢI Ý VÁ: tại New-DoiSoTacVu, dùng thuật toán quote đối số theo quy tắc native Windows, gồm nhân đôi dãy backslash trước nháy đóng; hoặc ghi cấu hình có schema vào vùng admin giữ và chỉ truyền đường dẫn cấu hình. Ca khoá: vòng qua pwsh -File bằng chuỗi action với mọi trường có dấu cách, một/nhiều backslash cuối, $, backtick; so toàn bộ bound values. Đột biến quay về quote đơn giản phải đỏ. Rủi ro: escape theo PowerShell -Command khác -File, dễ làm biến đổi giá trị literal hoặc mở injection nếu đổi tầng parser.

### dang-ky-lam-mat-tham-so  [P1]  Action vẫn bỏ NhatKy và chưa định nghĩa rõ ChiKiem khi đăng ký
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:44` (NhatKy), `:170`–`:171` (bảng serialize), `:533`–`:534` (action); `ops/vm/README.md:35` (khai mang đủ tham số).
VẤN ĐỀ: Các tham số MayDich/ThuMucCongCu/venv/profile/account/Commander đã được giữ. NhatKy là cấu hình runtime công khai nhưng không có trong $cap; đăng ký với -NhatKy D:\custom logs\run.json vẫn quay về đường mặc định ở lần chạy theo lịch. ChiKiem cũng bị bỏ; cần quy định rõ việc kết hợp -DangKyLich -ChiKiem (ghi nhận thiếu, không dùng riêng sự mơ hồ này để tăng severity).
ĐÃ THỬ NGHIỆM: `pwsh/pwsh -NoProfile -File probes/registration.ps1 -Mode clean` → action SYSTEM thật được thu từ Register: custom_log_preserved=false, check_preserved=false dù đã đặt cả hai; action có đủ bảy cấu hình còn lại. `probes/arguments.ps1` xác nhận has_NhatKy=false trong chuỗi và receiver không nhận khóa này. Chưa tạo ScheduledTask Windows thật.
ĐỘ TIN: cao về NhatKy bị mất; tác động -ChiKiem phụ thuộc hợp đồng cần làm rõ.
GỢI Ý VÁ: ở New-DoiSoTacVu, serialize NhatKy khi khác rỗng, giữ mặc định động khi rỗng; định nghĩa và test chính sách ChiKiem lúc đăng ký. Ca khoá: thu action từ Register với log tuỳ biến, chạy receiver để xác nhận đúng; đột biến xoá NhatKy khỏi action phải đỏ. Rủi ro: hai tầng dùng chung một tệp log có thể ghi đè nhau; cần quyết định đường riêng mỗi tầng hoặc mẫu tên có phạm vi, không tự tạo quyền ghi SYSTEM vào đường user kiểm soát.

### acl-mat-na-khong-nhan-dien  [P2]  So chuỗi quyền nhận nhầm mask chưa chứng minh an toàn
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:156`, `:162` (Test-AclChiAdminGhi).
VẤN ĐỀ: Hàm chỉ tìm từ khoá trong FileSystemRights.ToString(). Khi enum chứa bit ngoài danh sách tên, ToString có thể trả số; ngay cả mask 0x40000002 chứa WriteData (bit 2) cũng trả 1073741826 và không tạo vi phạm. Không có nhánh từ chối quyền không nhận diện. Allowlist danh tính được neo đúng, tên chứa Administrators ở vị trí khác không lọt. Mọi quyền ghi có tên enum đều đã bị chặn trong phép đo.
ĐÃ THỬ NGHIỆM: `pwsh/pwsh -NoProfile -File probes/acl.ps1` → [Enum]::ToObject(FileSystemRights,0x40000002), IdentityReference=VM\user, Allow: violations=0. Get-Acl NTFS có giữ generic bits, chuẩn hoá chúng hay có thể phát sinh mask ấy: KHÔNG ĐO ĐƯỢC trên Linux. Không nâng thành P0 chỉ từ đối tượng tổng hợp.
ĐỘ TIN: cao về kết quả helper; vừa về khả năng áp vào ACL native, ghi P2 giới hạn điều kiện/khai báo.
GỢI Ý VÁ: trong helper, so mặt nạ số với các bit ghi/xoá/đổi ACL/owner và từ chối bit không nhận diện; đo quyền effective/native nếu muốn khẳng định đầy đủ chỉ-admin-ghi. Ca khoá: enum có named rights và mask hỗn hợp chứa WriteData + bit lạ, ca read-only hợp lệ, ACE Deny; đột biến quay về regex phải đỏ. Rủi ro: chặn nhầm mask hợp lệ/chưa map generic hoặc ACL tuỳ hệ điều hành; cần quy định miền quyền được hỗ trợ và ghi lỗi rõ.

### test-thieu-duong-tich-hop  [P2]  Sáu chốt Register mới có thể bỏ mà suite vẫn 51/51
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu_test.ps1:108`–`:168`, `:205`–`:266`; sản phẩm `ops/vm/cap-nhat-cong-cu.ps1:492`, `:504`, `:518`, `:525`, `:526`, `:533`.
VẤN ĐỀ: Test helper ACL và helper đối số không khoá việc Register gọi helper/chốt kết quả. Phần luồng tích hợp mới chỉ chạy Save và HeThong; Register không được gọi. Bỏ dùng New-DoiSoTacVu ở action SYSTEM, bỏ từ chối ACL, bỏ so băm bản chép, bỏ đặt owner sau chép, bỏ reset inheritance và bỏ skip-owned đều xanh. Ba phản chứng tích hợp cũ đã có răng thật; finding hiện tại là phần thiếu của khối mới.
ĐÃ THỬ NGHIỆM: `python3 probes/run-mutations.py` → 9/15 mutant bị giết, 6/15 sống; sáu tên và neo/thay nguyên văn trong evidence/mutations.json, từng output trong evidence/mutation-*.log. Mỗi survivor 51/51 rc0, baseline 51/51 rc0.
ĐỘ TIN: cao.
GỢI Ý VÁ: thêm suite Register offline gọi hàm thật, thu action và các lời gọi native, bơm ACL/bản chép sai; assert chưa đăng ký task khi vi phạm, owner sau copy và không giao lại cây đã bàn giao. Sáu mutant trên phải đỏ ở đúng ca, baseline xanh. Test stub cần ghi rành mạch chỉ kiểm luồng/đối số; thêm VM thật cho junction/TOCTOU/owner/DACL/TaskScheduler. Rủi ro: mock luôn trả ACL an toàn tạo xanh giả; phải bơm trạng thái xấu và đo thứ tự/lời gọi, không chỉ tìm chuỗi trong cả tệp. HINT.patch sẽ chỉ chứa test/harness đã đo trên bản sao, không có bản vá sản phẩm.

HƯỚNG 9: đường thứ ba ở tầng NguoiDung — tệp có nhưng phiên bản không đọc được
  giả thuyết : Update-CongCuZip cũng coi bản có sẵn không đọc được là cài mới; có làm sai cam kết cùng-major/ChiKiem không.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/user-zip.ps1 > evidence/user-zip.log 2>&1`. ZIP, kiểm SHA256, giải nén, chép tệp đều thật trong temp; release/HTTP/version stub offline, không thực thi binary.
  output     : existing_version_unreadable=true, checkOnly=false → downloads=1, file_after=2.0.0, hanh_dong=cai_moi; checkOnly=true → downloads=0, file_after=unreadable-version, hanh_dong=can_cap_nhat; rc=0.
  kết luận   : KHÔNG PHẢI LỖI độc lập đủ căn cứ: có cùng mẫu phân loại cài_moi, nhưng công cụ portable tầng user được thiết kế cài latest/ghim, không có cam kết chỉ cùng-major như Node. ChiKiem không tải/ghi đè đúng. Không suy chính sách hệ thống sang tầng user để tăng finding. Đường thứ ba xác nhận thành lỗi ở HƯỚNG 4/7 là tham số NhatKy còn bị bỏ; Node SHASUMS cũng đã đo ở HƯỚNG 2/3.

HƯỚNG 10: test-only hint đóng sáu lỗ của suite Register
  giả thuyết : có thể thêm phản chứng offline cho sáu mutant sống mà không sửa mã sản phẩm/cây review.
  lệnh       : `TL_TEST_PWSH="$PWD/pwsh/pwsh" python3 hint/ops/vm/cap-nhat-cong-cu_dang-ky_test.py --product "$PWD/cay-kho/ops/vm/cap-nhat-cong-cu.ps1"`; chạy cùng lệnh với --product trỏ lần lượt sáu mutant (kết quả evidence/hint-mutations.json); `patch -p0 --dry-run -d hint-validation < HINT.patch`, rồi áp thật lên bản sao hint-validation và chạy cả suite cũ/suite mới.
  output     : head mới: `Register offline: 6/6 PASS; native ACL NOT_MEASURED`, rc0. Sáu mutant: task-argument-call 5/6 rc1, registration-acl-validation 5/6 rc1, registration-copy-hash 5/6 rc1, registration-owner-after-copy 2/6 rc1, registration-inheritance-reset 1/6 rc1, skip-owned 5/6 rc1. Ca đích tương ứng đều FAIL, không HARNESS_ERROR. Dry-run và apply đều rc0, đúng ba tệp mới ops/vm/*; trên bản sao áp patch suite mới 6/6 rc0 và suite gốc 51/51 rc0. Log evidence/hint-baseline.log, hint-mutation-*.log, hint-patch-*.log, hint-applied.log, hint-original-suite.log.
  kết luận   : KHÔNG PHẢI LỖI ở gợi ý test: có bằng chứng răng trên sáu chốt. Chỉ chứng minh luồng và đối số; các mô hình owner sau copy/ACL inheritance là giả có trạng thái, KHÔNG xác nhận ACL Windows. HINT.patch chỉ thêm harness/test, không vá sản phẩm, dùng `patch -p0` từ gốc bản sao cay-kho. `chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit`.

## GIỚI HẠN PHÉP ĐO

- Windows thật KHÔNG ĐO ĐƯỢC: NTFS junction/hardlink, quyền thực để user thay ancestor, icacls /L và reset DACL/owner effective, task SYSTEM/Limited/password/COM DACL, msiexec và Commander thật. Không đồng nhất shim Linux với chúng.
- P0 là finding tĩnh về lớp giao quyền còn hở, được bổ sung bằng chứng resolve/dispatch Linux; không có executable hay mã chưa kiểm băm nào chạy dưới SYSTEM trong phiên này.
- Không gọi mạng; mọi HTTP bị stub. Không chạy gate toàn kho/CI/land (ngoài phạm vi ops/vm); `git diff --check <old> <head> -- ops/vm/` rc0.
- HINT.patch là gợi ý test trên cây riêng, Linux-only, không phải bản vá production. Nó bảo vệ sáu chốt đang có, chưa sửa ancestor/TOCTOU/quoting/NhatKy/mask không nhận diện. Executor cần tự tái dẫn xuất và khai hint_provenance nếu dùng.
- Skip-owned chỉ dựa owner của gốc, không kiểm khả năng sửa tệp con: đây là giả định cần đo ở VM với gốc do user sở hữu nhưng tệp con do SYSTEM tạo. Chưa có bằng chứng native đủ để ghi thêm finding độc lập.

Kiểm tra cuối: `git -C cay-kho status --porcelain` → rỗng, rc0; HEAD vẫn aedd62077689045b676f5257ee5b6f67f44f8a66; blob script b89ca3db4aefcca097b670f07cddd5dc555bb65c và blob test 013f461f42016eb6b4dc86f26d56fde1cd615a45 khớp Git HEAD. Bằng chứng: evidence/final-identity.json. Không sửa cay-kho/, không push, không gọi mạng.
