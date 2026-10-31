verdict: changes_requested
reviewed_sha: 8e67b70e173edbf72e275457761b297936875cae

## ĐÓNG FINDING LƯỢT 7
| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | Đóng thật biểu hiện NLM lượt 7; CHƯA đóng toàn lớp | Oracle khóa lượt 7 `python3 -u probes/absence-regression-oracle.py` → 4/4 PASS/rc0 (H2); các oracle lượt 4–6 đều PASS. Hai đường ChiKiem cùng lớp còn sót: venv runtime 4/6 và portable 2/4, cả hai oracle rc1 (H6/H7). |

## BẢNG SĂN

Đang xác minh head, đọc chỉ thị và chuẩn bị bản sao để đo; không sửa cây `cay-kho/`, không gọi mạng.

HƯỚNG 1: neo exact head và bản sao độc lập
  giả thuyết : sai head hoặc probe đo tệp khác blob được giao.
  lệnh       : `python3` preflight (Git rev-parse HEAD/HEAD^{tree}, symbolic-ref, status --porcelain=v1 --untracked-files=all --ignored=matching; đối chiếu byte git show HEAD:<path> với cây và copies/head/). Bằng chứng: `evidence/preflight.json`.
  output     : HEAD=8e67b70e173edbf72e275457761b297936875cae; tree=cc6fd57056e04bd3bac097d1f0229abf239c0a7f; detached=true; shallow=false; core.abbrev=7; status rỗng; cả 5 tệp source/blob/copy khớp byte.
  kết luận   : KHÔNG PHẢI LỖI. Tất cả probe sau nạp production từ copies/head/, không dùng kết quả lượt trước. Scope toàn bộ ba tệp ops/vm/; ops/land/pr1065-* ngoài phạm vi.

Authority: yêu cầu trực tiếp của người dùng và `runs/c564e276/prompt.snapshot`; reviewer độc lập, chỉ đọc cây được giao. Provider=openai_codex; model=GPT-6 theo chỉ thị môi trường (không có bằng chứng riêng nhận dạng từng request); execution_surface=codex_service, transport=machine, shell Linux, sandbox=workspace-write. Không suy danh tính từ GitHub; không gọi mạng/ghi credential/push/merge. Ngưỡng nội dung: P0/P1/P2 chặn approve, P3 không chặn theo prompt. Không có quyền land. Session plan: xác minh finding cũ; đo lỗi/catch và native; thử đột biến test; săn đường khác toàn ops/vm/; kiểm nguyên vẹn cuối.

HƯỚNG 2: oracle nguyên bản lượt 6–7, có hậu điều JSON/exit
  giả thuyết : vá thiếu venv chỉ đổi dòng hiển thị, vẫn ok=true/exit0 hoặc gây hỏng đối chứng lành.
  lệnh       : `python3 -u probes/absence-regression-oracle.py > evidence/absence-regression-summary.log 2>&1` (rc0); `python3 -u probes/new-paths-oracle.py > evidence/new-paths-summary.log 2>&1` (rc0). Probe được sao từ luot7/, nạp bản sao blob head.
  output     : NLM prerequisite oracle (head): 4/4 PASS. Control sạch rc0/ok=true/nlm=kiem/loi0; thiếu nlm.exe, thiếu riêng Python và mất cả NlmVenv đều rc1/ok=false/nlm=loi/loi1. Mỗi ca 11 dòng, không native install. Remaining native paths oracle: 6/6 PASS: check-python rc1/1 loi/1 dòng; check-cli rc1/2 loi/11 dòng; check-nlm rc1/1 loi; metadata-fails và check-metadata đều rc1/3 loi; control rc0/11 dòng.
  kết luận   : KHÔNG PHẢI LỖI ở các biểu hiện đã báo lượt 6–7. Finding thiếu NLM prerequisite được vá thật theo oracle khóa lượt 7; chưa suy tổng suite hay các ca này thành đóng mọi đường cùng lớp. Native fixture có stdout/stderr/rc thật và trace argv; ZIP/Set-Path là stub offline, không đo entry point Windows/installer thật.

HƯỚNG 3: baseline bắt buộc của exact head
  giả thuyết : lời khai 81/81 không tái lập ở Linux hiện tại.
  lệnh       : `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : `cap-nhat-cong-cu tests: 81/81 ca QUA`, mã thoát 0.
  kết luận   : KHÔNG PHẢI LỖI về số Linux executor khai. Đây là baseline Linux tại head 8e67b70e; chưa phải phép đo Windows. Bộ test ghi output/tệp tạm ngoài cay-kho/.

HƯỚNG 4: catch, continue và các lỗi native đã có oracle lượt 4–5
  giả thuyết : catch mới nuốt lỗi thành ĐẠT/bo_qua, continue làm mất công cụ sau, hoặc lỗi lập trình thoát khỏi nhật ký.
  lệnh       : `python3 -u probes/l4-user-oracle.py`, `probes/user-oracle.py`, `probes/user-version-oracle.py`, `probes/run-main-tail.py`, `probes/run-user-extra.py` (mỗi lệnh rc0; output/JSON lưu evidence/*summary.log và *oracle.json).
  output     : ba oracle đầu đều 3/3 PASS. Main-tail: success rc0/ok=true; user-throw, system-throw, programmer-throw đều rc1/ok=false/loi1, JSON giữ exception thực. User-extra 12 mode: error=null, restored=true; npm-cannot-start 2 loi/11 dòng; pip-fails, venv-disappears, nlm-pip-fails, nlm-disappears, status-broken-json, status-other đều 1 loi/11 dòng; py-disappears 3 loi/11; CLI version hỏng 2 loi; NLM version hỏng 1 loi; check-only 11 dòng/0 loi/0 install.
  kết luận   : KHÔNG PHẢI LỖI với các catch/continue đã đo. Catch có gom lỗi lập trình nhưng ghi loi/ok=false, không thành đạt; continue sau Add-KetQua vẫn tới các công cụ độc lập sau. rc0 của user-extra là mã giàn xuất JSON, không phải mã sản phẩm; suffix main nguyên văn đo mã sản phẩm riêng. Fixture native chạy thật, không pip/npm install thật; Set-Path/ZIP offline stub.

HƯỚNG 5: băm/installer/hậu kiểm tầng HeThong và caller null
  giả thuyết : thiếu/lệch băm vẫn chạy, installer rc lỗi thành đạt, Node làm rớt Commander mà không dựng lại, hoặc getter null không được kiểm hậu điều.
  lệnh       : `python3 -u probes/system-matrix.py > evidence/system-summary.log 2>&1`; `python3 -u probes/caller-matrix.py > evidence/caller-summary.log 2>&1` (đều rc0).
  output     : system control 4 spawn/4 hash_matches=true; download-tamper và missing-hash 0 spawn/4 loi; installer-failure 4 loi; MSI3010 cho gh/node/pwsh can_khoi_dong_lai; post-version-wrong 4 loi; tất cả error=null/remaining_downloads=0. Mọi mode đã cài Node đều commander_restart=true. Caller system-pre 4 loi/0 spawn/0 HTTP fixture; system-post 4 loi/4 spawn/Commander Running; zip-pre sửa version hỏng thành 2.0.0/cai_moi bằng ZIP hợp băm; zip-post version rc9 thành loi.
  kết luận   : KHÔNG PHẢI LỖI trong các đường đã đo. Control 4 spawn là bằng chứng dương cho kiểm băm; `verified=true` khi 0 spawn chỉ là all(empty). Save/Assert-Bam/Install-Msi/Update-CongCuZip là hàm thật; HTTP/installer/task/icacls là mô hình offline. MSI3010 được chính sách chấp nhận chờ reboot; không suy thành đã chạy đúng phiên bản mới. NTFS/icacls/Scheduled Task/msiexec thật KHÔNG ĐO ĐƯỢC ở Linux.

HƯỚNG 6: đường thứ ba — venv kho còn tệp nhưng interpreter hỏng trong ChiKiem
  giả thuyết : nhánh ChiKiem venv-kho chỉ Test-Path, không hề đo khả năng chạy; interpreter hỏng vẫn được tính ĐẠT.
  lệnh       : `python3 -u probes/third-paths-oracle.py > evidence/third-paths-summary.log 2>&1` (rc1 của oracle; production head không đổi). Giàn dựa trên fixture lượt 7, chỉ làm hỏng venv/Scripts/python.exe; tự gọi --version riêng trước khi chạy suffix main nguyên văn, lưu precheck và trace.
  output     : Venv runtime oracle: 4/6 PASS. Control check-only rc0/ok=true/11 dòng; mất venv rc1/ok=false/venv=loi. Python venv tồn tại nhưng --version rc9 (`REVIEW-broken-venv`) hoặc không khởi chạy được: CẢ HAI ChiKiem rc0/ok=true/loi0/11 dòng/venv=kiem, không native install và không gọi interpreter venv trong lượt sản phẩm. Cùng hai fixture ở chế độ cài thật đều rc1/ok=false/venv=loi. JSON và precheck: evidence/third-paths-oracle.json.
  kết luận   : LỖI P1 thuộc lớp loi-native-tang-nguoi-dung còn sót, không phải try/catch mới sinh ra. :399 nhận tồn tại là đủ để ghi kiem; mất venv đã chặn ở :406 nhưng runtime hỏng vẫn đi vòng. Có control và bằng chứng interpreter hỏng độc lập, không chỉ đo tên mode giả. Không khẳng định VM hiện bị hỏng venv. Tạm giữ lớp cũ mở; các biểu hiện NLM lượt 7 đã vá thật.

HƯỚNG 7: cùng lớp ở portable ZIP — getter null trong ChiKiem
  giả thuyết : sau khi getter đã trả null đúng cho native hỏng/mất, Update-CongCuZip vẫn ghi can_cap_nhat và toàn lượt xanh, trái hợp đồng NguoiDung hiện tại.
  lệnh       : `python3 -u probes/portable-check-oracle.py > evidence/portable-check-summary.log 2>&1` (rc1 của oracle). Production Invoke-TangNguoiDung/Update-CongCuZip/Get-PhienBanLenh và suffix main nguyên bản; Get-Release là HTTP fixture offline có tag/asset/digest, native portable là executable thật trong scratch.
  output     : Portable ChiKiem oracle: 2/4 PASS. Control đúng phiên bản và control bản cũ đo được đều rc0/ok=true; bản cũ có truoc=1.0.0/sau=2.0.0/can_cap_nhat hợp lệ. Xóa rg.exe: rg truoc='' nhưng can_cap_nhat/rc0/ok=true/loi0/11 dòng. Cả rg/shellcheck/actionlint --version thoát9: cả ba truoc='' nhưng can_cap_nhat, rc0/ok=true/loi0/11 dòng. Mọi mode 0 install. Bằng chứng: evidence/portable-check-oracle.json, check-zip-*.json/.log.
  kết luận   : LỖI P1, biểu hiện thứ hai cùng lớp loi-native-tang-nguoi-dung. Chốt :337 không kiểm truoc null; getter không nuốt rc nữa nhưng caller phân loại sai. Không yêu cầu lỗi khi đã đo được phiên bản cũ (control outdated vẫn xanh). Không coi ZIP có thể sửa lỗi trong chế độ cài thật là lỗi; caller zip-pre ở H5 sửa thành công có hậu kiểm.

HƯỚNG 8: răng của ca test qua đột biến độc lập, gồm đúng hai hunk lượt 8
  giả thuyết : test mới thiếu venv chỉ diễn theo tên mode hoặc vẫn xanh khi đổi loi về bo_qua; catch/metadata/config/ACL không có hậu điều thực.
  lệnh       : `python3 -u probes/mutations.py --group old`, `--group additional`, `--group models`; `python3 -u probes/user-mutations.py`; `python3 -u probes/new-mutations.py`; `python3 -u probes/round7-mutations.py`; `python3 -u probes/round8-mutations.py`. Tất cả runner rc0; command/patch/ca đỏ/log của từng mutant trong evidence/mutations-summary.json và mutation-*.
  output     : 6+4+4+3+2+4+2 = 25/25 mutant bị bắt (mỗi suite rc1, có ca đỏ đúng đích), 0 ParserError. NLM thiếu trở lại bo_qua: 78/81, đúng ba ca nd_chikiem_nlm_thieu_python_phai_ghi_loi, nd_chikiem_nlm_thieu_venv_phai_ghi_loi, nd_cai_that_nlm_thieu_venv_cung_la_loi đỏ. Venv kho thiếu trở lại bo_qua: 80/81, đúng nd_venv_kho_thieu_la_loi đỏ. Bỏ rc metadata: 79/81, hai ca metadata đỏ; bỏ null ChiKiem gói/CLI/NLM: mỗi mutant 80/81; bỏ getter rc: 75/81, sáu ca version đỏ. ACL/config/catch có ca đỏ liên quan.
  kết luận   : KHÔNG PHẢI LỖI về răng các ca hiện hữu đối với guard chúng nhắm. Độc lập đo 25 mutant, không nhận số 22 executor khai là số của reviewer. Fixture mới thực sự xóa tệp/cả venv trước gọi production; native fixture trả stdout/stderr/rc thật. Main-catch mutant bị ca regex bắt; bằng chứng hành vi main-catch là oracle H4, không gọi riêng ca regex là test hành vi. Các ca cũ chưa khóa hai đường H6/H7; không nhân cùng P1 thành P2 thiếu test riêng. Runner cũ chỉ được nâng timeout 60/90 lên 120 giây để tránh nghẽn khi đo song song; không thay production/test được chạy.

HƯỚNG 9: đăng ký lịch, ACL có trạng thái và trust của bản SYSTEM
  giả thuyết : Register thật còn đổi quyền dưới Tools hoặc đăng ký task khi audit/hash/reparse đã hỏng.
  lệnh       : `python3 -u probes/registration-matrix.py > evidence/registration-summary.log 2>&1` (rc0; chạy lại sau khi dựng đủ mutant); `pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source-audit.log 2>&1` (rc0).
  output     : Head clean icacls=3/tool_acl_calls=0/audit=4/tasks=1 rồi dừng REVIEW-STOP-BEFORE-CREDENTIALS; acl-reject/hash-reject tasks=0; ancestor/child symlink icacls=0/tasks=0. Owner Users và grant Users F bị audit từ chối/tasks=0. Mutant bỏ audit/hash/reparse thật đi được tới task trong mô hình, suite bắt các mutant này ở H8. Bỏ grant/admin readonly vẫn đi tới task trong oracle; suite bắt bằng đối số thực mà hàm gửi. AST parse_errors=0, pwsh=7.6.9, Ubuntu 24.04.5, README_native_acl_commands=0.
  kết luận   : KHÔNG PHẢI LỖI mới đo được trong mô hình. Register/copy/hash/path/symlink thật; icacls/Get-Acl/tasks là đồ giả có trạng thái. Lần chạy đầu khi mutant chưa dựng có rc1/tasks=null là lỗi setup cho các nhánh mutant, KHÔNG dùng làm bằng chứng; file summary cuối đã tái đo đầy đủ. NTFS junction/effective ACL/owner/task/COM/DACL/credential thật KHÔNG ĐO ĐƯỢC ở Linux; dừng trước credential, không khai đã đăng ký đầy đủ. Không biến mô hình Linux thành xác nhận an toàn Windows.

HƯỚNG 10: ca không đo được có bị đếm QUA, phân biệt nền và dependency
  giả thuyết : thiếu Python/nền/quyền bị bỏ qua nhưng vẫn ghi ĐẠT.
  lệnh       : `TL_TEST_PYTHON=REVIEW_PYTHON_NOT_PRESENT pwsh/pwsh -NoProfile -File copies/head/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/missing-python.log 2>&1` (rc1); `python3` liệt kê tên Ca và các nhánh nền/quyền từ source (evidence/test-accounting.json).
  output     : DO doc_ghim_tu_ban_ke_that; `cap-nhat-cong-cu tests: 80/81 ca QUA`. Source 85 khai báo/85 tên duy nhất, 15 ca nd_ chỉ đăng ký ngoài Windows. Nhánh Windows admin không đo được quyền rc3 trả false rõ ràng ở :266, không trả true.
  kết luận   : KHÔNG PHẢI LỖI về skip mà vẫn đếm QUA trong các nhánh đã rà. Không chạy script test-accounting cũ như oracle số vì các dòng tổng Linux/Windows trong chính probe cũ là số viết cứng đã stale; thay bằng đếm source + baseline thật. Kết quả Windows cho 8e67b70e KHÔNG ĐO ĐƯỢC; 68/68 của 00dd9d4 là SHA khác và chỉ là lời khai executor, không tính vào head này.

HƯỚNG 11: test khóa có đối chứng và khả năng phân biệt head với hướng sửa
  giả thuyết : H6/H7 chỉ do giàn sai hoặc test gợi ý đỏ vì lỗi setup; không phân biệt được head với caller xử lý null đúng.
  lệnh       : `python3 probes/build-round8-hint.py`; `patch -p0 --dry-run -d hint-validation < HINT.patch`; `patch -p0 -d hint-validation < HINT.patch` (rc0). `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/hint-on-head.log 2>&1` (rc1); cùng lệnh trên hint-prototype/ (evidence/hint-prototype.log, rc0). `python3 -u probes/third-paths-oracle.py --prototype` (rc0); `python3 -u probes/portable-check-oracle.py --prototype` (rc0).
  output     : Head+HINT 82/86, đúng 4 ca mới nd_chikiem_venv_kho_runtime_hong_la_loi, nd_chikiem_venv_kho_khong_khoi_chay_la_loi, zip_chikiem_thieu_exe_phai_ghi_loi, zip_chikiem_native_rc_khac_0_phai_ghi_loi đỏ; control portable phiên bản cũ đo được xanh. Prototype 86/86; venv runtime oracle 6/6 PASS (head 4/6), portable ChiKiem oracle 4/4 PASS (head 2/4). Các ca ChiKiem không install; JSON/exit phản ánh loi đúng. Native runtime rc9 trong chế độ cài thật có 1 event venv sau khi giàn bổ sung trace vào chính shim hỏng; không có event venv ở ChiKiem trên head. `git blame` xác nhận hai nhánh lỗi :337/:399 có từ 22840642, không phải bản vá try/catch mới.
  kết luận   : LỖI P1 được phân biệt bằng oracle head nguyên bản và test thêm. Lần dựng HINT đầu control portable đỏ vì regex của giàn thiếu ký tự escape; đã sửa regex của TEST scratch, kiểm lại control xanh và đo lại cả hai cây. Không dùng kết quả lần setup sai để đếm finding. HINT giao nộp chỉ sửa test (5 ca = 4 âm + 1 đối chứng), không chứa production patch. Prototype sửa caller chỉ để chứng minh tính phân biệt ở scratch, không phải head được duyệt và chưa chứng minh đủ mọi package/requirement của venv.

## ĐỐI CHIẾU LƯỢT TRƯỚC VÀ BẢNG LỚP

Nguồn: luot7/VERDICT.md tại 00dd9d43554c6cd2ed70c5526bbf1f21e76e354d; 1 lớp mở, stable slug giữ nguyên. Theo hợp đồng mới trong prompt, mọi công cụ NguoiDung không đo/cài được phải là loi, không có nhánh bo_qua. Quét source cho thấy không còn lời gọi Add-KetQua bo_qua; điều đó chưa đủ vì kiem/can_cap_nhat cũng bị tổng kết tính ĐẠT.

| slug lớp | phân loại đối chiếu | biểu hiện đã báo / còn mở | cách đóng và phép kiểm |
| --- | --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | ĐÃ VÁ THẬT biểu hiện NLM lượt 7; CHƯA VÁ hết lớp. Không có bằng chứng bản vá mới sinh lỗi. | Oracle NLM 4/4; missing venv-kho thành loi cả hai chế độ qua test và đột biến. Còn 2 nhóm biểu hiện cũ chưa được báo: venv interpreter hỏng ChiKiem; portable không đọc version ChiKiem. | Caller phải đòi kết quả đo hợp lệ trước khi ghi kiem/can_cap_nhat; giữ khả năng cài thật để sửa portable hỏng. Oracle H6/H7 phải đỏ ở head, xanh ở ứng viên mới; control công cụ lành/bản cũ vẫn xanh, 0 install ChiKiem, JSON ok=false/exit1 khi không đo được. |

Đếm **1 lớp còn mở**, 2 nhóm biểu hiện (venv kho; portable gồm rg/shellcheck/actionlint). Không mở P2 riêng cho khoảng trống test của cùng P1. Không đổi slug/tách PR để xóa lịch sử. Biểu hiện mới không tự chứng minh bản vá mới gây lỗi; blame và đo đối chứng cho thấy nhánh cũ còn sót.

### loi-native-tang-nguoi-dung  [P1]  ChiKiem vẫn báo ĐẠT khi venv kho hoặc portable không chạy được

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:399` (venv-kho chỉ kiểm tệp tồn tại); `ops/vm/cap-nhat-cong-cu.ps1:337` (Update-CongCuZip nhận getter null rồi ghi can_cap_nhat). Các caller portable ở :425–:427; tổng kết :653–:666 chỉ tính hanh_dong=loi nên các nhánh trên cho ok=true/exit0.

VẤN ĐỀ: Hợp đồng NguoiDung đã chốt trong prompt yêu cầu công cụ không đo/cài được phải là lỗi. Vá :435/:406 đã xử lý thiếu NLM/venv kho. Tuy nhiên khi venv/Scripts/python.exe tồn tại mà hỏng hoặc không khởi chạy được, ChiKiem không gọi nó, vẫn ghi venv-kho=kiem. Với rg/shellcheck/actionlint, getter thật đã loại rc9 thành null nhưng nhánh ChiKiem của Update-CongCuZip ghi can_cap_nhat mà không đòi phiên bản đo được. Cả hai nhóm được tổng kết TONG 11/11 dat, loi0, JSON ok=true, exit0. Đây là false success đo được ở exact head, cùng lớp qua các lượt 4–7; không phải lỗi P0 hoặc khẳng định VM hiện đã hỏng. Phiên bản cũ nhưng đo được có thể can_cap_nhat hợp lệ; trường hợp cài thật có thể sửa rồi hậu kiểm không thuộc finding này.

ĐÃ THỬ NGHIỆM:

- `python3 -u probes/third-paths-oracle.py` → rc1, 4/6 PASS. Direct precheck venv Python rc9 hoặc launch exception, tệp vẫn tồn tại; suffix main nguyên văn trả rc0/ok=true/venv=kiem trong cả hai ca ChiKiem. Chế độ cài thật tương ứng rc1/ok=false/venv=loi. Control sạch/mất venv phân loại đúng.
- `python3 -u probes/portable-check-oracle.py` → rc1, 2/4 PASS. Mất rg.exe hoặc cả ba version native rc9 đều toàn lượt rc0/ok=true, các portable hỏng can_cap_nhat/truoc rỗng. Control lành và control bản cũ đo được đều rc0, 0 install trong cả bốn ca.
- Test-only HINT trên bản sao head: 82/86, chỉ 4 ca âm mới đỏ; prototype scratch: 86/86, oracle venv 6/6 và portable 4/4. H11 nêu giới hạn/khắc phục setup. Command cụ thể từng subprocess, JSON nguyên bản và trace argv lưu trong evidence/third-paths-oracle.json và evidence/portable-check-oracle.json. Các probe chỉ fake native output/HTTP/Set-Path trong scratch, không fake Add-KetQua/kết luận của production.

ĐỘ TIN: cao về luồng, kết quả, JSON và mã thoát tại exact head; chưa đo thực trạng venv/công cụ trên VM Windows.

GỢI Ý VÁ:

- Vá tại caller :399 và :337: ChiKiem đo venv bằng phép đọc không cài (ít nhất chạy interpreter, kiểm rc và output); có thể bổ sung kiểm package/requirements theo hợp đồng venv. Portable getter trả null thì ghi loi trong ChiKiem. Cài thật vẫn được phục hồi công cụ rồi kiểm hậu điều. Không đổi đơn thuần nhãn kiem/can_cap_nhat thành lỗi cho mọi ca.
- Ca khóa: bốn ca âm trong HINT cộng control phiên bản cũ đo được; thêm hậu điều JSON ok=false/exit1 và 0 install trong oracle. Giữ test mất venv ở cả hai chế độ và các oracle lượt 4–7.
- Rủi ro của cách vá: quá chặt có thể biến mọi bản cũ thành lỗi, cản cài mới/sửa portable, hoặc làm ChiKiem gọi pip install. Cần giữ hai control H7/H11 và trace no-install; chỉ chạy lệnh đọc trong lượt kiểm. Nếu mở rộng thành pip check/requirements, chốt rõ thứ đang đo, không coi interpreter chạy được là đủ chứng minh mọi gói venv khớp.

`HINT.patch` dùng `patch -p0` từ gốc BẢN SAO cay-kho/, chỉ sửa TEST: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Nếu dùng phải khai hint_provenance; không tự suy hint là quyền push/merge/land. Prototype không nằm trong patch giao nộp.

HƯỚNG 12: kiểm cuối nguồn, artifact và ranh giới phép đo
  giả thuyết : cây review đã bị sửa, bằng chứng thuộc SHA khác, HINT không còn áp được hoặc đột biến đỏ do lỗi parser.
  lệnh       : `python3 probes/final-audit-round8.py > evidence/final-audit.log` (rc0; chi tiết evidence/final-readonly.json). Script chạy Git với GIT_OPTIONAL_LOCKS=0, kiểm HEAD/tree, status tracked/untracked/ignored, index/worktree diff, đối chiếu blob/preflight/copy, 25 mutant và patch --dry-run -p0 trên bản sao sạch.
  output     : HEAD=8e67b70e173edbf72e275457761b297936875cae; tree=cc6fd57056e04bd3bac097d1f0229abf239c0a7f; status rỗng; index/diff/diff--check rc0, 5/5 tệp khớp. 25/25 mutant bị bắt, parser_errors=0. HINT dry-run rc0 và chỉ đổi cap-nhat-cong-cu_test.ps1; SHA256=46e96414eeaaaa64d42b4cc12de6fef68495303f67a07f1e6b6351519ec0f78d. PowerShell 7.6.9, Ubuntu 24.04.5 LTS, PSNativeCommandUseErrorActionPreference=False.
  kết luận   : KHÔNG PHẢI LỖI về neo head/artifact và tính nguyên vẹn ở hai mốc quan sát. Snapshot đầu/cuối không chứng minh mọi thời điểm trong lịch sử. Scratch/fixture/mutant/prototype/HINT đều ngoài cay-kho/; không có commit/push/merge/mạng.

## QUYẾT ĐỊNH VÀ GIỚI HẠN

Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

**changes_requested** vì lớp `loi-native-tang-nguoi-dung` còn false success ở ChiKiem venv kho/portable theo hợp đồng NguoiDung đã chốt. Những ca NLM prerequisite của lượt 7 được vá thật, không còn bo_qua; bản vá mới không có bằng chứng sinh lỗi riêng. Hai đường còn sót là nhánh cũ và cùng lớp; không nhân số finding theo công cụ hay ca test.

- Linux head gốc **81/81, rc0**. Oracle khóa lượt 7 **4/4, rc0**, oracle lượt 6 **6/6, rc0**, ba oracle lượt 4–5 mỗi oracle **3/3, rc0**. Không gộp các mẫu số.
- Oracle mới của head: venv runtime **4/6, rc1** và portable ChiKiem **2/4, rc1**. Đây là phản chứng của finding. HINT chỉ test trên bản sao head **82/86, rc1**; prototype scratch **86/86, rc0**, hai oracle lần lượt **6/6** và **4/4, rc0**. Prototype không phải head được duyệt.
- **25/25 đột biến bị bắt** bằng suite hiện tại; hai hunk thiếu venv mới có test thực sự phân biệt. Bộ test vẫn thiếu bốn ca âm mới trong HINT. Không tìm thấy nhánh suite không đo được mà trả true rồi tính QUA trong các nhánh nền/quyền/dependency đã rà; điều này không phải chứng minh đủ độ phủ mọi hành vi.
- **KHÔNG ĐO ĐƯỢC**: entry point Windows đầy đủ với identity thật; NTFS junction/effective ACL/owner/handle/TOCTOU, icacls, Scheduled Task/COM/DACL/credential, msiexec, Commander thật, getter .cmd trên Windows, native install trên VM. Phân tích tĩnh và mô hình Linux không chứng minh các tính chất Windows ấy đúng. Không lấy kết quả Windows của head lượt 7 làm kết quả head này.
- Review chỉ toàn bộ `ops/vm/` tại exact SHA nêu ở dòng 2; `ops/land/pr1065-*` không được review. Không gọi mạng, không cài gói/installer thật, không sửa cay-kho/, không đăng thông điệp ra ngoài. Verdict này không cấp quyền merge/land.
