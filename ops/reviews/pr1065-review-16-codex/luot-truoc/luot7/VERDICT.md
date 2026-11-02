verdict: changes_requested
reviewed_sha: 00dd9d43554c6cd2ed70c5526bbf1f21e76e354d

Review độc lập lượt 7; chỉ đọc cây `cay-kho/`, đo trên bản sao, không gọi mạng.

## ĐÓNG FINDING LƯỢT 6

| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | Đóng các phản chứng lượt 6, chưa đóng toàn lớp ChiKiem theo chính sách hiện hành | Oracle lượt 6 `6/6 PASS`; oracle prerequisite NLM mới `2/4 PASS`, còn thiếu nlmPy/cả venv bị bo_qua/ok=true/exit0. Chi tiết lệnh/output ở H2/H3/H7/H10 và bảng chốt cuối. |

## BẢNG SĂN

Các hướng dưới đây được nối dần sau mỗi phép đo; trạng thái cuối đã chốt theo bằng chứng.

HƯỚNG 1: neo head và giữ cây review chỉ đọc
  giả thuyết : đang review nhầm head hoặc bản sao không trùng blob Git.
  lệnh       : `python3` dựng snapshot ngoài repository (lệnh preflight trong phiên; dữ liệu đầy đủ `evidence/preflight.json`), dùng `git -C cay-kho rev-parse HEAD HEAD^{tree}`, `git status --porcelain=v1 --untracked-files=all --ignored=matching`, đối chiếu byte với `git show HEAD:<path>`.
  output     : HEAD=00dd9d43554c6cd2ed70c5526bbf1f21e76e354d; tree=8873bf62e954c9977e9b1cfd4a77ab09ef829c6e; detached=true; shallow=false; core.abbrev=7; status rỗng; source/blob/copy 5/5 match.
  kết luận   : KHÔNG PHẢI LỖI. Bản sao `copies/head/` dùng đúng head; probe kế thừa từ lượt 6 nhưng không dùng lại kết quả cũ. Scope chỉ ba tệp ops/vm/, không review ops/land/.

Danh tính thực thi: provider=openai_codex; model=GPT-6 (theo chỉ thị môi trường, không suy từ tài khoản GitHub); execution_surface=codex_service; transport=machine; shell cục bộ Linux. Authority là yêu cầu trực tiếp và `runs/30c6d543/prompt.snapshot`; không có thao tác đăng verdict lên GitHub.

HƯỚNG 2: baseline và oracle phản chứng trực tiếp của lượt 6
  giả thuyết : ChiKiem hoặc metadata vẫn biến native rc≠0 thành ĐẠT/ok=true.
  lệnh       : `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1` (rc0); `python3 -u probes/new-paths-oracle.py > evidence/new-paths-oracle.log 2>&1` (rc0). Probe chỉ nạp production nguyên bản từ copies/head/, thực thi suffix main nguyên văn.
  output     : `cap-nhat-cong-cu tests: 77/77 ca QUA`. Oracle check-only: rc0/ok=true/loi0/tong11; check-python: rc1/ok=false/loi1/tong1; check-cli: rc1/ok=false/loi2/tong11; check-nlm: rc1/ok=false/loi1/tong11; metadata-fails: rc1/ok=false/loi3/tong11; check-metadata: rc1/ok=false/loi3/tong11. `Remaining native paths oracle: 6/6 PASS`.
  kết luận   : KHÔNG PHẢI LỖI với sáu phản chứng này. Hai control dương/âm đúng; bốn đường còn hở lượt 6 đã được chặn ở kết quả từng công cụ lẫn JSON/mã thoát. Native fixture có stdout/stderr/rc thật, trace argv giữ trong evidence/new-paths-oracle.json; ZIP/Set-Path là stub offline. Không coi đây là full entry point Windows hay kiểm package thật trên VM.

HƯỚNG 3: native launch/rc, continue trong vòng lặp và catch lỗi lập trình
  giả thuyết : catch mới nuốt lỗi, biến thành bo_qua/ĐẠT hoặc continue làm mất các công cụ sau.
  lệnh       : `python3 -u probes/l4-user-oracle.py`, `python3 -u probes/user-oracle.py`, `python3 -u probes/user-version-oracle.py` (log cùng tên dưới evidence/); `python3 -u probes/run-main-tail.py > evidence/main-tail-summary.log 2>&1`; `python3 -u probes/run-user-extra.py > evidence/user-extra-summary.log 2>&1`.
  output     : cả ba oracle cũ đều 3/3 PASS. Main-tail: success rc0/ok=true; user-throw, system-throw, programmer-throw đều rc1/ok=false/loi1 và JSON có thông báo exception thật. User-extra: 12 chế độ, error=null và profile_restored=true; npm-cannot-start có 2 loi/11 dòng; pip-fails 1/11; py-disappears 3/11; venv-disappears 1/11; nlm-pip-fails/nlm-disappears/status-broken-json/status-other đều 1/11; check-only 0 loi/11 dòng/0 install; cli-version lỗi 2/11; nlm-version lỗi 1/11.
  kết luận   : KHÔNG PHẢI LỖI trong các đường đã đo. Lỗi lập trình bị catch nhưng được báo loi, không biến thành đạt; công cụ độc lập vẫn chạy sau lỗi cục bộ. rc0 của probe user-extra là mã giàn đo xuất JSON, không phải rc sản phẩm: rc sản phẩm được đo bằng suffix main riêng. `continue` ChiKiem nằm sau Add-KetQua và chỉ tiếp tục foreach; oracle xác nhận đủ 11 dòng.

HƯỚNG 4: tải/băm/installer và hậu kiểm tầng HeThong
  giả thuyết : lỗi hoặc thiếu hash vẫn chạy payload, rc cài lỗi bị che, hoặc mất bước dựng lại Commander.
  lệnh       : `python3 -u probes/system-matrix.py > evidence/system-summary.log 2>&1` (rc0; JSON chi tiết evidence/system-matrix.json).
  output     : control 4 spawn và cả 4 hash_matches=true; download-tamper/missing-hash đều 0 spawn/4 loi; installer-failure rc1603 cho 4 loi; MSI3010 cho gh/node/pwsh can_khoi_dong_lai; post-version-wrong cho 4 loi. Mọi mode error=null, remaining_downloads=0; mọi mode thực sự cài Node đều commander_restart=true.
  kết luận   : KHÔNG PHẢI LỖI trong mô hình offline này. Save/Assert-Bam/New-ThuMucTai/Install-Msi/Invoke-TangHeThong là hàm thật; HTTP/phiên bản/Start-Process/task/icacls là fixture. `verified=true` khi 0 spawn là all(empty), không coi là bằng chứng dương; control 4 spawn mới là bằng chứng dương. Installer/NTFS/task Windows thật KHÔNG ĐO ĐƯỢC.

HƯỚNG 5: Register thật, ACL có trạng thái và chặn reparse/hash
  giả thuyết : Register còn đổi ACL dưới Tools hoặc bỏ qua audit/owner/hash trước task SYSTEM.
  lệnh       : `python3 -u probes/registration-matrix.py > evidence/registration-summary.log 2>&1` (JSON evidence/registration-matrix.json); `pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source-audit.log 2>&1` (rc0).
  output     : head clean: icacls=3/tool_acl_calls=0/audit=4/tasks=1 rồi dừng REVIEW-STOP-BEFORE-CREDENTIALS; acl-reject/hash-reject tasks=0; ancestor/child symlink: icacls=0/tasks=0. Owner Users và grant Users F bị audit từ chối/tasks=0. AST parse_errors=0, README_native_acl_commands=0. Mutant thiếu grant/admin readonly vẫn tới task trong oracle; suite riêng bắt đúng bằng assertion argv.
  kết luận   : KHÔNG PHẢI LỖI mới trong các hành vi đã mô phỏng. Register/copy/hash/path/symlink là thật; icacls/Get-Acl/tasks là mô hình có trạng thái, không đo effective I/O hay NTFS. Task dừng trước credential/COM, không khai đã đăng ký hoàn chỉnh. Không suy mô hình Linux thành an toàn native Windows.

HƯỚNG 6: mọi caller null còn lại ở HeThong và portable ZIP
  giả thuyết : getter mới trả null nhưng caller cài mù hoặc biến hậu kiểm thất bại thành đạt.
  lệnh       : `python3 -u probes/caller-matrix.py > evidence/caller-summary.log 2>&1` (từng lệnh pwsh và output trong evidence/caller-null.json).
  output     : system-pre: 4 loi/0 spawn/0 HTTP fixture; system-post: 4 spawn, 4 loi, Commander Running; zip-pre: ZIP hợp băm sửa được thành 2.0.0/cai_moi; zip-post: version rc9 sau chép thành 1 loi.
  kết luận   : KHÔNG PHẢI LỖI ở bốn đường này. Getter/native executable/ZIP/Expand-Archive/copy/hash là thật; Copy-Item thêm chmod +x cho fixture Linux. HTTP/installer/task/icacls là đồ giả. Không xác minh native Windows.

HƯỚNG 7: đường thứ ba — thiếu venv NLM vượt qua chốt ChiKiem
  giả thuyết : chốt null nlm chỉ chạy khi nlmPy tồn tại; mất cả venv thì vẫn bo_qua/ok=true dù chỉ thị yêu cầu lượt kiểm báo thiếu là lỗi.
  lệnh       : `python3 -u probes/absence-oracle.py > evidence/absence-summary.log 2>&1` (rc0 của giàn; command/JSON/trace riêng evidence/absence-oracle.json và absence-*.json/.log).
  output     : control check-only: rc0/ok=true/loi0/11 dòng/0 install. Mất claude+codex: rc1/2 loi; mất nlm.exe nhưng Python venv còn: rc1/1 loi. Mất riêng nlm/Scripts/python.exe hoặc mất toàn bộ NlmVenv: CẢ HAI rc0/ok=true/loi0, nlm=bo_qua, TONG 11/11 dat, 0 install. Mất venv kho cũng bo_qua (chỉ ghi nhận, không gộp làm lỗi khi hợp đồng không yêu cầu nó bắt buộc). Metadata rc0 nhưng rỗng/rác: 3 loi/rc1; metadata pre rc6, post hợp lệ sau cài: rc0, ba gói nang_cap.
  kết luận   : LỖI P1 còn lại của loi-native-tang-nguoi-dung tại nhánh thiếu NLM prerequisite :433; sáu phản chứng lượt 6 đóng thật nhưng chưa đóng toàn lớp ChiKiem. Đây là đường cũ chưa được phủ, không do try/catch mới tạo ra. Đánh giá theo yêu cầu trực tiếp trong prompt: nlm chưa cài ở ChiKiem phải là loi. Nếu không còn yêu cầu này và NlmVenv được định nghĩa tùy chọn, cần đổi hợp đồng/khai kết quả; review hiện tại không tự coi bỏ qua là đạt đủ công cụ. Metadata recovery dùng fixture có trạng thái trước/sau, không chứng minh pip thực cài thành công.

HƯỚNG 8: răng của test qua đột biến độc lập trên bản sao
  giả thuyết : ca metadata/ChiKiem mới chỉ đo đồ giả hoặc không phân biệt khi bỏ đúng chốt production.
  lệnh       : `python3 -u probes/mutations.py --group old`, `--group additional`, `--group models`; `python3 -u probes/user-mutations.py`; `python3 -u probes/new-mutations.py`; `python3 -u probes/round7-mutations.py` (logs mutations-*-summary.log; mỗi mutant/command/ca đỏ/patch ở evidence/).
  output     : 6 old + 4 additional + 4 models + 3 user + 2 new + 4 round7 = 23 mutant, tất cả rc1 với ca đỏ đúng mục tiêu, 0 ParserError. Bỏ rc metadata: 75/77, đúng hai ca metadata đỏ; bỏ chốt null ChiKiem gói/CLI/nlm: mỗi mutant 76/77 và đúng ca tương ứng đỏ. Bỏ getter rc: 71/77, sáu ca version đỏ; bỏ Python guard: 76/77. Các mutant ACL/owner/grant/config/catch/status đều có ca đỏ liên quan.
  kết luận   : KHÔNG PHẢI LỖI về răng của các ca hiện hữu đối với chốt mà chúng nhắm. Độc lập chạy 23 mutant, không sao chép số 20 executor khai; tập mutant khác nhau. Probe cũ new-mutations.py được sửa ở giàn vì nay có HAI chốt rc cùng văn bản: mutant getter chỉ bỏ chốt thứ nhất trong Get-PhienBanLenh, không bỏ rc metadata. Native fixture trả stdout/stderr/rc thật; fixture metadata-hong không thay kết quả sản phẩm theo tên ca. Ca mới chưa phủ prerequisite mất ở H7; không đếm thiếu test của cùng P1 thành P2 riêng.

HƯỚNG 9: phép đo không thực hiện có bị đếm QUA
  giả thuyết : thiếu Python/nền/quyền vẫn xanh, hoặc lấy số Linux làm số Windows.
  lệnh       : `TL_TEST_PYTHON=REVIEW_PYTHON_NOT_PRESENT pwsh/pwsh -NoProfile -File copies/head/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/missing-python.log 2>&1` (rc1); đếm tên Ca/nhánh nền từ source, kết quả evidence/test-accounting.json.
  output     : `DO doc_ghim_tu_ban_ke_that`, `cap-nhat-cong-cu tests: 76/77 ca QUA`; 81 khai báo/81 tên duy nhất, 11 ca nd_ chỉ đăng ký ngoài Windows; ca admin không đo được quyền rc3 trả false rõ ràng.
  kết luận   : KHÔNG PHẢI LỖI về suite skip rồi vẫn đếm QUA trong các nhánh đã rà. Baseline reviewer là Linux 77/77; Windows head này KHÔNG ĐO ĐƯỢC. 68/68 trên head lượt 6 là khai executor trên SHA khác, không được dùng làm kết quả head hiện tại.

HƯỚNG 10: test khóa mới và oracle có hậu điều cho đường thiếu NLM
  giả thuyết : H7 chỉ do giàn đo hỏng, hoặc không phân biệt head với việc phân loại thiếu prerequisite thành lỗi trong ChiKiem.
  lệnh       : `python3 probes/build-round7-hint.py`; `patch -p0 --dry-run -d hint-validation < HINT.patch`; `patch -p0 -d hint-validation < HINT.patch` (đều rc0); `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1` (evidence/hint-on-head.log, rc1); cùng lệnh trên hint-prototype/ (evidence/hint-prototype.log, rc0); `python3 -u probes/absence-regression-oracle.py` (rc1); cùng lệnh thêm `--prototype` (rc0), logs evidence/absence-regression-{head,prototype}.log.
  output     : head+HINT 78/80, chỉ nd_chikiem_nlm_thieu_python_phai_ghi_loi và nd_chikiem_nlm_thieu_venv_phai_ghi_loi đỏ; prototype 80/80. Oracle head 2/4 PASS: đối chứng sạch và thiếu nlm.exe phân loại đúng; hai ca thiếu Python/cả venv đều rc0/ok=true/nlm=bo_qua, FAIL. Prototype 4/4 PASS: cùng hai ca thành rc1/ok=false/loi1/nlm=loi; control vẫn rc0/ok=true; mọi ca 11 dòng, 0 native install.
  kết luận   : LỖI P1 được phản chứng bằng production head nguyên bản, có control, JSON/rc và khả năng phân biệt. Prototype chỉ ở scratch đổi phân loại nhánh thiếu nlmPy theo ChiKiem, không phải bản vá production giao nộp. Ca đối chứng cài thật/venv NLM thiếu vẫn giữ bo_qua, tránh mở rộng thay đổi ngoài chính sách ChiKiem. git blame chỉ :433 thuộc commit 22840642, chốt :437 mới thuộc 00dd9d43: nhánh cũ đi vòng qua chốt mới, không phải try/catch mới sinh lỗi.

## ĐÓNG FINDING LƯỢT 6 — CHỐT THEO PHÉP ĐO

| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | Đã đóng 6 ca oracle lượt 6; CHƯA đóng toàn lớp kiểm-thiếu NLM theo hợp đồng hiện tại | `python3 -u probes/new-paths-oracle.py` → 6/6 PASS, rc0; ba oracle cũ → mỗi oracle 3/3 PASS. `python3 -u probes/absence-regression-oracle.py` → 2/4 PASS, rc1: thiếu nlmPy/cả venv vẫn bo_qua/ok=true/exit0. H2/H3/H7/H10. |

### loi-native-tang-nguoi-dung  [P1]  ChiKiem vẫn báo ĐẠT khi thiếu toàn bộ venv NLM

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:433` (nhánh `-not (Test-Path $nlmPy)`); chốt nlm null mới ở :436–:437 chỉ nằm trong `else`. Hệ quả ở :651–:655, :663–:664: chỉ đếm `hanh_dong='loi'` để tính ok và exit.

VẤN ĐỀ: Chỉ thị review hiện tại nêu chính sách ChiKiem: nlm không đọc được phiên bản, kể cả chưa cài, phải là lỗi. Bản vá thực hiện điều này khi Python venv còn mà nlm.exe thiếu/hỏng. Tuy nhiên, nếu NlmVenv chưa dựng, bị xóa, cấu hình sai đường dẫn, hoặc mất Scripts/python.exe, nhánh :433 ghi `bo_qua` ngay; không vào chốt mới, không có dòng loi. Tổng kết nguyên bản in `TONG: 11/11 dat`, JSON `loi=0, ok=true`, exit0. Lượt kiểm sức khỏe báo đạt trong tình trạng công cụ theo phạm vi không được kiểm và chưa cài. Đây là nhánh cũ còn sót của cùng lớp false success ChiKiem; giữ stable slug, chỉ đếm một P1. Không mở P2 riêng cho ca test thiếu, không gọi đây là P0 hay lỗi native Windows đã xảy ra trên VM.

ĐÃ THỬ NGHIỆM: `python3 -u probes/absence-regression-oracle.py > evidence/absence-regression-head.log 2>&1` → rc1, 2/4 PASS. Head không bị đột biến: probe nạp hàm từ bản sao khớp blob, tạo fixture venv rồi xóa riêng Python hoặc cả cây trước khi gọi; chạy suffix main nguyên văn với đường dẫn JSON đã chỉ định. Cả hai ca có 11 dòng, nlm=bo_qua, ok=true/loi0/rc0 và 0 install; native trace chứng minh không gọi nlm trong nhánh bị bỏ. Control sạch rc0, control chỉ thiếu nlm.exe rc1, đúng theo chính sách. `HINT.patch` chỉ thêm test: head+HINT 78/80 rc1, đúng hai ca đỏ; prototype scratch 80/80 rc0 và oracle 4/4 PASS. Các log và JSON chi tiết nằm trong evidence/absence-regression-*.json/.log.

ĐỘ TIN: cao về luồng/JSON/exit ở exact head với tình trạng tệp thiếu đã đo; không khẳng định VM hiện đang thiếu venv. Tiêu chí lỗi căn cứ trực tiếp chính sách “lượt kiểm báo thiếu là lỗi” trong prompt; với một hợp đồng khác cho NLM tùy chọn thì cần công bố/đánh giá lại thay vì ngầm suy optional ở lượt này.

GỢI Ý VÁ: ở nhánh thiếu nlmPy, khi ChiKiem hãy ghi loi và giữ thông tin NlmVenv thiếu; không cần tạo venv hay cài trong lượt kiểm. Có thể giữ hành vi bo_qua của chế độ cài thật theo hợp đồng cũ. Giữ control đủ công cụ, thiếu chỉ nlm.exe, thiếu Python và thiếu toàn venv; hậu điều phải gồm dòng nlm loi, ok=false/exit1 và không install. `HINT.patch` định dạng patch -p0 từ gốc bản sao cay-kho/, chỉ sửa TEST; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Không cấp quyền push/merge/land; nếu dùng khai hint_provenance.

HƯỚNG 11: kiểm cuối exact SHA, tính nguyên vẹn và ranh giới phép đo
  giả thuyết : kết quả thuộc SHA khác, mutant bị chết vì ParserError, hoặc cây review bị thay đổi.
  lệnh       : `python3 probes/final-audit-round7.py > evidence/final-audit.log` (rc0; dữ liệu evidence/final-readonly.json); `pwsh/pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString(); "PSNativeCommandUseErrorActionPreference=$PSNativeCommandUseErrorActionPreference"'` (rc0, evidence/powershell-environment.log).
  output     : HEAD=00dd9d43554c6cd2ed70c5526bbf1f21e76e354d; tree=8873bf62e954c9977e9b1cfd4a77ab09ef829c6e; detached=true/shallow=false/core.abbrev=7; status tracked/untracked/ignored rỗng, index/worktree diff rỗng, diff --check rc0. 5/5 tệp khớp blob/bản sao/preflight. 23/23 mutant có ca đỏ liên quan, parser errors=0. PowerShell 7.6.9, Ubuntu 24.04.5, PSNativeCommandUseErrorActionPreference=False. HINT SHA256=54eeea4cc1ce2a12090ff67643f5c59aaf4217fd0ba77c8b82911986350012ff.
  kết luận   : KHÔNG PHẢI LỖI về neo bằng chứng hay tính nguyên vẹn tại hai mốc đo. Snapshot đầu/cuối không phải bằng chứng mọi thời điểm trong lịch sử. Toàn bộ scratch/fixture/mutant/hint ở ngoài cay-kho/.

## GIỚI HẠN VÀ QUYẾT ĐỊNH

Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

- **changes_requested** vì một P1 còn lại theo chính sách ChiKiem hiện hành: thiếu venv NLM bị ghi bo_qua và toàn lượt vẫn ok=true/exit0. Sáu ca phản chứng lượt 6 đã được sửa thật; các try/catch mới chưa có bằng chứng tự tạo lỗi mới. Giữ một stable slug cho cả lớp, không nhân finding theo từng biểu hiện.
- Linux baseline **77/77 PASS, rc0**; oracle lượt 6 **6/6 PASS, rc0**; oracle NLM prerequisite của head **2/4 PASS, rc1**. Đây là các phép đo khác nhau, không gộp thành một mẫu số. Test-only HINT trên head **78/80, rc1**; prototype scratch **80/80, rc0**, oracle **4/4, rc0**. Prototype không phải head được duyệt.
- Các ca hiện hữu có răng với **23/23 đột biến bị bắt**. Không có bằng chứng hiện hữu về nhánh không đo được mà vẫn đếm QUA trong suite; Windows admin không đo quyền rc3 trả false, các ca native shebang Linux không được đăng ký trên Windows. Điểm mù thiếu NLM prerequisite được báo cùng P1, không tạo thêm P2.
- **KHÔNG ĐO ĐƯỢC**: full entry point Windows với identity thật; NTFS junction/effective ACL/owner/handle/TOCTOU; icacls, Scheduled Task/COM/DACL/credential, msiexec, Commander thật; getter .cmd trên Windows; trust của TEMP/ancestor và native install trên VM. Phân tích tĩnh về đường tuyệt đối/băm/ACL và mô hình Linux không chứng minh các tính chất này đúng trên Windows. Không nhận số 68/68 của SHA lượt 6 là test của SHA hiện tại.
- Không mạng, không pip/npm install thật, không credential thật, không sửa cay-kho/, không commit/push/merge. Không review ops/land/pr1065-*. Kết quả và giới hạn đều neo exact SHA nêu ở dòng 2.
