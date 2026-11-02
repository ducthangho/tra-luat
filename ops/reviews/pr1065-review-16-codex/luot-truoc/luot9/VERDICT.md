verdict: changes_requested
reviewed_sha: e21890138ec770bd108384c49467f1fd362d704c

## ĐÓNG FINDING LƯỢT 8
| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | Đã vá thật hai biểu hiện ChiKiem lượt 8; CHƯA đóng toàn lớp theo hợp đồng cài thật | `python3 -u probes/third-paths-oracle.py` → 6/6 PASS, rc0; `python3 -u probes/portable-check-oracle.py` → 4/4 PASS, rc0. Venv/portable hỏng đều ok=false/exit1. Nhưng `python3 -u probes/real-pip-oracle.py` → 1/2 PASS, rc1: pip thật dry-run rc0, gói sau vắng, venv-kho vẫn giu/ok=true/exit0 (H6/H9). |

## BẢNG SĂN

Đã bắt đầu review độc lập; chỉ đọc cây `cay-kho/`, chạy phép đo trên bản sao khi cần thay fixture. Không gọi mạng.

HƯỚNG 1: neo head và bản sao độc lập
  giả thuyết : probe đo nhầm SHA hoặc bản sao lệch nguồn.
  lệnh       : `python3` preflight, đối chiếu `git show HEAD:<path>` với source và ghi bản sao; `git status --porcelain=v1 --untracked-files=all --ignored=matching`.
  output     : HEAD=e21890138ec770bd108384c49467f1fd362d704c, detached=true, shallow=false, core.abbrev=7, status rỗng; cả 5 tệp ops/vm + dependency khớp blob (evidence/preflight.json).
  kết luận   : KHÔNG PHẢI LỖI. Oracle sao từ luot8/probes/ (gồm oracle kế thừa lượt 4–7); các default còn trỏ ../cay-kho được chuyển sang ../copies/head, không đổi logic fixture/oracle. Không dùng kết quả cũ.

Authority: prompt.snapshot/yêu cầu trực tiếp; reviewer độc lập, read-only cay-kho/. Provider=openai_codex, model=GPT-6 theo môi trường (không có xác minh model từng request), execution_surface=codex_service, transport=machine; Linux, không mạng. Scope toàn ops/vm/, loại ops/land/pr1065-*.

HƯỚNG 2: khóa venv và portable của lượt 8
  giả thuyết : vá guard mới chỉ đổi nhãn, còn ok=true/exit0 khi native hỏng hoặc làm control bản cũ đỏ.
  lệnh       : `python3 -u probes/third-paths-oracle.py > evidence/third-paths-summary.log 2>&1`; `python3 -u probes/portable-check-oracle.py > evidence/portable-check-summary.log 2>&1` (đều rc0).
  output     : Venv runtime oracle: 6/6 PASS; Portable ChiKiem oracle: 4/4 PASS. Venv --version rc9 và không launch được đều venv=loi/ok=false/exit1/11 dòng. Mất rg: 1 loi; cả ba portable rc9: 3 loi; ok=false/exit1/11 dòng. Control lành và portable bản cũ đo được đều ok=true/exit0; bản cũ can_cap_nhat/truoc=1.0.0/sau=2.0.0. Mọi ChiKiem 0 install, venv lành có đúng 1 lần gọi interpreter.
  kết luận   : KHÔNG PHẢI LỖI với hai biểu hiện lượt 8; cả hai đã vá thật. JSON/argv/direct precheck lưu evidence/*oracle.json. Chưa suy thành đóng mọi lớp trước khi săn tiếp.

HƯỚNG 3: baseline bắt buộc của exact head
  giả thuyết : số Linux executor khai không tái lập.
  lệnh       : `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : `cap-nhat-cong-cu tests: 87/87 ca QUA`, rc0.
  kết luận   : KHÔNG PHẢI LỖI về baseline Linux. Không lấy 68/68 Windows của SHA cũ làm kết quả head này; Windows thật KHÔNG ĐO ĐƯỢC tại đây.

HƯỚNG 4: hồi quy oracle lượt 4–7 và catch/continue
  giả thuyết : catch mới đổi lỗi native/lỗi lập trình thành ĐẠT, làm mất công cụ sau hoặc mất nhật ký.
  lệnh       : `python3 -u probes/l4-user-oracle.py`, `probes/user-oracle.py`, `probes/user-version-oracle.py`, `probes/new-paths-oracle.py`, `probes/absence-regression-oracle.py`, `probes/run-main-tail.py` (log evidence/*summary.log).
  output     : Ba oracle đầu mỗi oracle 3/3 PASS; remaining native 6/6 PASS; NLM prerequisite 4/4 PASS. Main-tail success exit0/ok=true; user-throw, system-throw, programmer-throw đều exit1/ok=false/loi1, có message exception thật trong JSON. Mọi runner rc0.
  kết luận   : KHÔNG PHẢI LỖI ở các đường đã khóa. Catch có gom lỗi lập trình nhưng thành loi, không bo_qua/ĐẠT. continue sau ghi lỗi vẫn tới các công cụ độc lập sau; không mất JSON. Fixture có executable native/rc thật; ZIP/Set-Path/HTTP offline stub. Không coi suffix main là toàn entry point Windows.

HƯỚNG 5: băm, installer, reboot và hậu kiểm HeThong/portable
  giả thuyết : chạy installer thiếu/lệch băm, rc installer/post-version hỏng vẫn đạt, getter null không được caller kiểm.
  lệnh       : `python3 -u probes/system-matrix.py > evidence/system-summary.log 2>&1`; `python3 -u probes/caller-matrix.py > evidence/caller-summary.log 2>&1` (đều rc0).
  output     : System control 4 spawn, cả 4 hash_matches=true; tamper/missing-hash 0 spawn/4 loi; installer-failure và post-version-wrong 4 loi. MSI3010: gh/node/pwsh=can_khoi_dong_lai. Commander được dựng lại sau mọi mode đã thử cài Node; remaining_downloads=0. Caller system-pre 4 loi/0 spawn/0 HTTP; system-post 4 loi/4 spawn; zip-pre phục hồi version rc9 thành 2.0.0/cai_moi qua ZIP hợp băm; zip-post rc9 thành loi.
  kết luận   : KHÔNG PHẢI LỖI trong phép đo. rc0 của giàn system/caller là xuất JSON, không phải sản phẩm; phán đoán theo rows. verified=true khi 0 spawn là all(empty), chỉ control 4 spawn là bằng chứng dương. Reboot/decision là chờ người có chủ ý. Save/Assert/Install-Msi/caller thật, HTTP/installer/task/icacls mô hình; NTFS/icacls/msiexec/Scheduled Task thật KHÔNG ĐO ĐƯỢC trên Linux.

HƯỚNG 6: đường thứ ba — hậu kiểm cài thật của venv kho
  giả thuyết : venv-kho tin rc pip=0 rồi ghi giu, không đo phiên bản SAU cài theo hợp đồng mới của prompt.
  lệnh       : `python3 probes/build-install-contract.py`; `python3 -u probes/install-contract-oracle.py > evidence/install-contract-summary.log 2>&1` (oracle rc1).
  output     : Install contract oracle: 2/4 PASS. Control khỏe ok=true/exit0; pip rc8 ok=false/exit1. Hai ca âm pip rc0 nhưng (a) --version sau cài rc9, (b) metadata PyYAML/jsonschema=0.0.1 thay vì 6.0.3/4.25.1: CẢ HAI vẫn venv-kho=giu/truoc=''/sau='', chi_tiet='requirements.txt đã khớp', toàn lượt ok=true/loi0/exit0/11 dòng. Trace venv của sản phẩm chỉ có một lệnh -m pip install, không gọi --version/importlib.metadata. Direct-after độc lập đo rc/output của chính executable fixture; evidence/install-contract-oracle.json.
  kết luận   : LỖI P1 cùng lớp loi-native-tang-nguoi-dung chưa đóng hết theo hợp đồng cài thật. Đây là nhánh cũ tại :409, không phải try/catch mới sinh ra. Fixture mô hình installer rc0 nhưng hậu điều sai, không khẳng định pip chính thức/VM hiện thực sự tạo trạng thái ấy. Phản chứng chắc chắn về việc caller không đo hậu điều mà vẫn tuyên bố đạt; mọi production/blob giữ nguyên. Đối chứng rc8 chứng minh không phải nuốt mọi lỗi native.

HƯỚNG 7: ChiKiem HeThong và quét mọi dòng không lỗi
  giả thuyết : hợp đồng chung vẫn sót git/gh/node/pwsh hoặc dòng node-major không dựa trên rc0+khớp mẫu.
  lệnh       : `python3 probes/build-system-check.py`; `python3 -u probes/system-check-oracle.py > evidence/system-check-summary.log 2>&1` (rc0); `rg -n "'giu'|'nang_cap'|'cai_moi'|'kiem'|'can_cap_nhat'|'bo_qua'" cay-kho/ops/vm/cap-nhat-cong-cu.ps1`.
  output     : System ChiKiem oracle: 6/6 PASS. Control 4 can_cap_nhat/4 native rc0; rc9, output rác rc0, mất tệp, không launch được đều 4 loi/ok=false/exit1. No-LTS: node-major và node đều can_quyet_dinh, truoc=24.1.0, 4 phép đo rc0; 0 cài đặt. Source không có Add-KetQua bo_qua; các dòng ChiKiem NguoiDung đều bị chốt bởi getter tương ứng; node-major nằm sau guard :491.
  kết luận   : KHÔNG PHẢI LỖI ở hợp đồng ChiKiem trong phạm vi rà/đo. Bản vá guard không cấm control bản cũ và không biến lỗi thành chờ quyết định. Lần giàn đầu rc1 vì finally của fixture dọn native trace trước oracle đọc; đã chuyển trace ra evidence, chạy lại đủ 6 mode. Không dùng lượt setup ấy làm bằng chứng dương.

HƯỚNG 8: răng test mới qua đột biến độc lập
  giả thuyết : các ca mới chỉ diễn tên mode hoặc vẫn xanh khi bỏ từng guard thực.
  lệnh       : dựng 5 mutant từ blob head vào evidence/round8-mutants-input.json; `python3 -u probes/round8-mutations.py > evidence/mutations-new-guards-summary.log 2>&1`; `python3 -u probes/round7-mutations.py > evidence/mutations-existing-guards-summary.log 2>&1` (đều runner rc0).
  output     : 9/9 mutant bị bắt (suite mỗi mutant exit1, không ParserError). Bỏ ZIP guard: 85/87 (2 ca ZIP đỏ); bỏ system guard: 86/87 (he_thong_chikiem_thieu_cong_cu_la_loi đỏ); bỏ phép đo venv: 85/87 (2 ca runtime đỏ). Đổi thiếu NLM sang bo_qua: 84/87; thiếu venv sang bo_qua: 86/87. Bỏ rc metadata: 85/87; bỏ null gói/CLI/NLM mỗi mutant 86/87. Tên ca đỏ/command/patch/log lưu evidence/mutations-*.json và mutation-*.
  kết luận   : KHÔNG PHẢI LỖI ở răng các test đã nhắm. Fixture mới thực sự chmod/xóa tệp/thoát rc9; system test dùng getter stub nhưng phản chứng head ở H7 dùng native thật. Đây là 9 mutant do reviewer chạy, không tự nhận 25/25 executor khai. Không mở thêm P2 cho thiếu test của cùng P1 venv cài thật.

HƯỚNG 9: phản chứng venv bằng pip THẬT, offline
  giả thuyết : H6 chỉ do shim giả pip; pip thật rc0 có đủ đảm bảo hậu điều đã khớp không?
  lệnh       : `python3 -m pip install --help` (có --dry-run); `python3 -u probes/real-pip-oracle.py > evidence/real-pip-summary.log 2>&1` (oracle rc1).
  output     : Real pip oracle: 1/2 PASS. Dùng Python 3.13 và pip 26.2.2 thật trong hai venv scratch, hai wheel local do reviewer dựng, PIP_NO_INDEX=1/PIP_CONFIG_FILE=/dev/null, không mạng. Control PIP_DRY_RUN=0: pip rc0, metadata sau =6.0.3/4.25.1, ok=true/exit0. PIP_DRY_RUN=1: pip THẬT rc0 nhưng cả hai metadata sau đều PackageNotFoundError/rc1; sản phẩm vẫn venv-kho=giu, 'requirements.txt đã khớp', ok=true/loi0/exit0/11 dòng. Trace sản phẩm chỉ gọi pip install vào venv. evidence/real-pip-oracle.json lưu command, argv, rc, stdout/stderr, direct-after.
  kết luận   : LỖI P1 của H6 có điều kiện thực, không chỉ đồ giả diễn kịch bản. Biến PIP_DRY_RUN được pip kế thừa và script không vô hiệu hóa/không hậu kiểm. Không khẳng định VM đang có biến ấy; wheel chỉ là dữ liệu fixture, không phải gói PyPI chính thức; Windows Python 3.12/pip tại VM KHÔNG ĐO ĐƯỢC. Control chứng minh đường cài thật có thể thành công, không bắt mọi rc0 thành lỗi.

### loi-native-tang-nguoi-dung  [P1]  Venv cài thật vẫn báo ĐẠT khi pip rc0 nhưng hậu điều chưa khớp
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:408` và `:409`; tổng kết `:660`–`:673` tính mọi dòng khác loi là đạt.
VẤN ĐỀ: Nhánh cài thật venv-kho chỉ xem LASTEXITCODE của pip rồi ghi giu với trước/sau rỗng và tuyên bố requirements đã khớp. Khác các nhánh package/ZIP/HeThong, không gọi getter phiên bản interpreter/gói sau cài và không so ghim. Hợp đồng prompt yêu cầu dòng giu/nang_cap/cai_moi chỉ đạt khi phiên bản sau đo được và khớp đích. Pip dry-run là điều kiện có thật: PIP_DRY_RUN=1 làm installer trả thành công mà chưa cài gì. Head vẫn báo 11/11 đạt dù hai gói được chỉ định trong requirements và ghim đều vắng.
ĐÃ THỬ NGHIỆM: `python3 -u probes/install-contract-oracle.py` → 2/4 PASS, rc1; hai ca hậu điều rc9/lệch ghim vẫn ok=true/exit0. `python3 -u probes/real-pip-oracle.py` → 1/2 PASS, rc1; control cài đúng, ca PIP_DRY_RUN=1 có actual pip rc0 nhưng importlib.metadata của cả PyYAML/jsonschema trả PackageNotFoundError/rc1, sản phẩm vẫn giu/ok=true/exit0. Các oracle chạy trên blob head nguyên bản, chỉ fixture và môi trường scratch thay đổi.
ĐỘ TIN: cao về nhánh thiếu hậu kiểm và false success tại exact head; không khẳng định tình trạng VM Windows.

GỢI Ý VÁ: ở nhánh venv-kho, lưu rc pip ngay sau lệnh; đo lại interpreter và các phiên bản/requirements được yêu cầu trong CHÍNH venv ấy, so với đích/ghim rồi mới ghi giu. Có thể kiểm soát biến cấu hình pip như dry-run, nhưng chỉ bỏ PIP_DRY_RUN chưa thay thế hậu kiểm chung. Ca khóa cần control cài đúng, pip rc8, pip rc0 nhưng interpreter rc9, ghim lệch/vắng, và pip thật offline có PIP_DRY_RUN=1; đòi JSON ok=false/exit1 với ca âm và vẫn chạy các công cụ sau. Rủi ro: chỉ kiểm hai ghim chưa chứng minh toàn requirements.txt; chỉ pip check cũng chưa chứng minh từng spec đã cài. Hậu kiểm phải dùng đúng venv, xử lý marker/constraint theo hợp đồng và không chạy cài đặt trong ChiKiem. Không mở thêm P2 cho khoảng trống test của cùng P1.

HƯỚNG 10: đăng ký lịch, ACL và đường chạy SYSTEM toàn scope
  giả thuyết : code mới chạm lại Tools, nhận reparse/ACL/hash xấu rồi vẫn đăng ký task.
  lệnh       : `python3 -u probes/registration-head.py > evidence/registration-summary.log 2>&1`; `pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source-audit.log 2>&1` (đều rc0).
  output     : 5/5 mode đạt oracle. Clean icacls=3/tool_acl_calls=0/audit=4/tasks=1 rồi dừng REVIEW-STOP-BEFORE-CREDENTIALS. ACL/hash xấu tasks=0. Ancestor/child link icacls=0/tasks=0. AST parse_errors=0, pwsh=7.6.9; README_native_acl_commands=0.
  kết luận   : KHÔNG PHẢI LỖI mới đo được. Copy/hash/path/symlink thật; ACL/icacls/task giả có trạng thái, dừng trước credential/COM. Toàn bộ ops/vm được đọc, không có nguồn mới ở ngoài ba tệp. Chỉ chạy absolute installer sau Save-CoKiemBam ở HeThong; không suy thành native Windows an toàn: NTFS junction, effective ACL, owner, handle/TOCTOU, Scheduled Task/msiexec thật KHÔNG ĐO ĐƯỢC. Không tái mở P0 chỉ từ giả thiết attacker kiểm soát ProgramFiles/TEMP chưa được xác minh.

HƯỚNG 11: nhánh không đo được có bị đếm QUA
  giả thuyết : test thiếu dependency/quyền/nền vẫn return true rồi tính ĐẠT.
  lệnh       : `TL_TEST_PYTHON=REVIEW_NO_SUCH_PYTHON pwsh/pwsh -NoProfile -File copies/head/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/missing-python.log 2>&1` (rc1); `python3` liệt kê tên Ca và nhánh nền/quyền từ source (evidence/test-accounting.json).
  output     : DO doc_ghim_tu_ban_ke_that; `cap-nhat-cong-cu tests: 86/87 ca QUA`. Source 91 khai báo/91 tên duy nhất; 17 ca nd_ và 3 ca ZIP native chỉ đăng ký ngoài Windows. Nhánh Windows admin không đo được rc3 trả $false rõ tại :266; không trả true.
  kết luận   : KHÔNG PHẢI LỖI về bỏ qua mà vẫn đếm QUA ở các nhánh đã rà. Một ca âm ban_ke_thieu_ghim_thi_nem vẫn xanh khi Python vắng vì chấp nhận mọi exception, nhưng ca dương bản kê đỏ nên toàn suite không xanh; không có cơ sở mở finding riêng cho lời khai suite. Windows head này KHÔNG ĐO ĐƯỢC; không suy số Linux thành Windows.

HƯỚNG 12: HINT test-only có phân biệt head và hậu kiểm đúng không
  giả thuyết : H6/H9 là lỗi setup, hoặc các ca khóa mới không phân biệt được thay đổi caller.
  lệnh       : `python3 probes/build-round9-hint.py`; `patch -p0 --dry-run -d copies/head < HINT.patch` (rc0). `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/hint-on-head.log 2>&1` (rc1); cùng lệnh trên hint-prototype/ (rc0). `python3 -u probes/real-pip-oracle.py --prototype > evidence/real-pip-prototype-summary.log 2>&1` (rc0).
  output     : Head + 4 ca HINT = 89/91; đúng hai ca nd_venv_cai_pip_rc0_python_sau_rc9_phai_loi và nd_venv_cai_pip_rc0_ghim_sau_lech_phai_loi đỏ. Control cài đúng và pip rc8 xanh. Prototype scratch 91/91; real pip oracle prototype 2/2 PASS so với head 1/2. Ở prototype, dry-run vẫn actual pip rc0 nhưng metadata vắng khiến venv-kho=loi/ok=false/exit1; control vẫn xanh.
  kết luận   : LỖI H6/H9 được khóa bằng test có đối chứng, không do giàn báo mọi ca đỏ. HINT chỉ sửa TEST; prototype production là witness riêng ngoài cay-kho, chỉ kiểm interpreter + hai ghim của fixture, CHƯA chứng minh đủ mọi dòng requirements.txt thật. Các công cụ khác là fixture/stub lành để cô lập venv; không gọi full entry point Windows. Patch đã dry-run từ đúng gốc bản sao; không áp lên cây review.

## ĐỐI CHIẾU LƯỢT TRƯỚC VÀ BẢNG LỚP

Nguồn liền trước: `luot8/VERDICT.md`, reviewed_sha=8e67b70e173edbf72e275457761b297936875cae. Phạm vi lượt này là toàn ops/vm tại e21890138ec770bd108384c49467f1fd362d704c. Ngưỡng áp theo prompt: P0/P1/P2 chặn approve; P3 không chặn. Review class sensitive do có SYSTEM/credential/security boundary; verdict không cấp quyền land.

| slug lớp | phân loại đối chiếu | biểu hiện/nguồn và phép đo | cơ chế đóng chung |
| --- | --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | ĐÃ VÁ THẬT hai biểu hiện ChiKiem lượt 8; CHƯA VÁ hết lớp theo hợp đồng cài thật | Oracle venv ChiKiem 6/6, portable 4/4, HeThong ChiKiem 6/6; oracle lượt 4–7 xanh. Không còn dòng ChiKiem không loi thiếu phép đo rc0+khớp mẫu trong phạm vi rà. Còn venv cài thật chỉ tin pip rc0: oracle fixture 2/4, actual pip 1/2; vẫn giu khi hậu điều sai/vắng. | Áp hợp đồng đo tại mọi điểm ghi thành công: ChiKiem cần phiên bản đang cài; cài thật cần rc installer và hậu kiểm đúng interpreter/gói/đích trong cùng venv. Control không lỗi phải xanh; ca âm JSON ok=false/exit1; ChiKiem 0 install. |

Giữ **1 lớp P1 còn mở**, các ví dụ rc9/lệch ghim/dry-run là biểu hiện cùng cơ chế thiếu hậu kiểm venv, không đếm thành nhiều finding. Hai nhánh ChiKiem mới đã vá thật; không có bằng chứng vá tự sinh lỗ mới. Nhánh cài thật :409 tồn tại trước lượt vá này (diff-tu-luot8.patch chỉ đổi nhánh ChiKiem của venv), không gọi nó là regression mới. Không dùng suite 87/87 để đóng lớp. Không mở P2 riêng cho ca test thiếu của chính P1 ấy.

Reviewer model=GPT-6 theo chỉ thị môi trường, provider=openai_codex, execution_surface=codex_service, transport=machine, run=e235cf3f; effort/model từng request KHÔNG ĐO ĐƯỢC độc lập. Executor Claude và số test của executor là thông tin prompt, không phải runtime identity do reviewer xác minh. Không suy danh tính từ submitter; không đăng comment/PR, không push/commit/merge/land. Công cụ cloud environment_status không có trong tool list; không đọc credential hay gọi mạng.

`HINT.patch` dùng `patch -p0` từ gốc BẢN SAO cay-kho/, chỉ thêm fixture/test: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Nếu dùng cần khai hint_provenance. Prototype không nằm trong patch giao nộp và không phải head được approve.

HƯỚNG 13: kiểm cuối exact SHA, nguồn, bằng chứng và patch giao nộp
  giả thuyết : source/copy bị sửa, output thuộc SHA khác hoặc HINT không tái tạo đúng bản đã test.
  lệnh       : `python3 probes/final-audit-round9.py > evidence/final-audit.log` (rc0); Git với GIT_OPTIONAL_LOCKS=0 kiểm HEAD/tree/status tracked+untracked+ignored/index/worktree; đối chiếu bytes với blob, preflight và copies/head; áp HINT vào hint-patch-check rồi đối chiếu hint-validation.
  output     : HEAD=e21890138ec770bd108384c49467f1fd362d704c; tree=cc8788dea5128f673284a60b03028a7b16b4cae8; status rỗng; diff/index/diff--check rc0; 5/5 tệp khớp; 9/9 mutant bị bắt, 0 ParserError. HINT apply rc0/test_only=true/apply_matches_tested_copy=true; sha256=5d95e7c31af2cd527e35d5c2a271e413bd5a5d2b02a9a364450fbbc1600af022. PowerShell 7.6.9, PSNativeCommandUseErrorActionPreference=False, Ubuntu 24.04.5 LTS.
  kết luận   : KHÔNG PHẢI LỖI về neo nguồn và artifact ở hai mốc quan sát. Final auditor ban đầu đòi đúng một native event ở cả prototype, nhưng prototype có thêm hậu kiểm; đã sửa predicate để đếm đúng một lệnh pip install và đo lại rc0. Không đổi sản phẩm hay kết quả đo để sửa giàn. Snapshot sạch không chứng minh mọi thời điểm trong lịch sử; mọi scratch/mutant/hint/evidence nằm ngoài cay-kho/.

Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

**changes_requested**: lớp loi-native-tang-nguoi-dung còn false success ở cài thật venv-kho theo hợp đồng prompt, được tái hiện bằng pip thật offline. Hai biểu hiện ChiKiem của lượt 8 đã đóng và guard mới có test bắt được đột biến. Baseline exact head Linux 87/87, rc0; HINT trên head 89/91, rc1; prototype 91/91, rc0. Không gộp các mẫu số oracle với suite. Windows head này, NTFS/icacls/effective ACL/owner/TOCTOU, Scheduled Task/COM/credential, msiexec, Commander thật và getter .cmd Windows **KHÔNG ĐO ĐƯỢC**; kết quả Windows SHA cũ không được tính là bằng chứng của head này.
