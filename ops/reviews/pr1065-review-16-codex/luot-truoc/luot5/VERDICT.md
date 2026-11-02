verdict: changes_requested
reviewed_sha: ea5ccd5edeaccfce36eb3a8723002c636dcaf206

Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

## ĐÓNG FINDING LƯỢT 4
| slug | đã đóng? | phép đo (lệnh + output) |
|---|---|---|
| loi-native-tang-nguoi-dung | **Đóng hai phản chứng cũ; chưa đóng lớp** | `python3 probes/user-oracle.py` → 3/3 PASS, rc0; suffix main 4/4 (H7). Nhưng `python3 probes/user-version-oracle.py` → 1/3 PASS, rc1: CLI version exit1/9 vẫn giu (H6/H12). |
| test-thieu-duong-tich-hop | **Đã đóng điểm mù owner/grant lượt 4** | `python3 probes/mutations.py --group models` → owner Users và grant Users F đều 63/68 rc1; thiếu grant/admin readonly 67/68 rc1; oracle Register độc lập tasks=0 với owner/grant sai (H3/H8). |

## BẢNG SĂN

Bắt đầu review độc lập; chỉ đọc cây `cay-kho/`, mọi probe/mutant sẽ chạy trên bản sao. Không gọi mạng.

HƯỚNG 1: baseline và mỏ neo review
  giả thuyết : cây sai SHA hoặc bộ test được khai 68/68 không tái hiện.
  lệnh       : `git -C cay-kho rev-parse HEAD`; `git -C cay-kho status --short`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : HEAD `ea5ccd5edeaccfce36eb3a8723002c636dcaf206`; status rỗng; `cap-nhat-cong-cu tests: 68/68 ca QUA`, exit=0. SHA256 các tệp và tree ở `evidence/preflight.json`. Đã tạo bản sao đúng byte ở `copies/head/`.
  kết luận   : KHÔNG PHẢI LỖI ở baseline Linux. Chưa có phép đo Windows native; 68/68 không chứng minh ACL/task/installer Windows.

HƯỚNG 2: chạy lại oracle lỗi native lượt 4 trên head nguyên bản sao
  giả thuyết : bản vá chỉ đổi cách khai; npm biến mất vẫn làm dừng tầng hoặc status nlm exit7 vẫn thành ĐẠT.
  lệnh       : `python3 probes/user-oracle.py > evidence/user-oracle.log 2>&1`; probe lượt 4 được chép ra `probes/`, chỉ đổi đường nạp sang `copies/head/` (đúng byte head).
  output     : `PASS success`, `PASS npm-disappears`, `PASS nlm-status-fails`, `User native error oracle: 3/3 PASS`, oracle_exit=0. JSON đầy đủ: `evidence/user-oracle.json`.
  kết luận   : KHÔNG PHẢI LỖI với hai phản chứng cũ. Success đủ 11 dòng, không lỗi; npm biến mất có dòng lỗi và vẫn tới rg/shellcheck/actionlint/nlm; status exit7 được ghi nlm `loi`. Main/lưới cuối chưa được oracle này chạy; sẽ đo riêng. Không suy Linux executable fixture thành phép đo task Windows.

HƯỚNG 3: mô hình ACL đọc đúng principal/quyền, không chỉ có mặt lệnh
  giả thuyết : owner Users hoặc grant Users F vẫn làm suite xanh như lượt 4.
  lệnh       : `python3 -u probes/mutations.py --group models > evidence/mutations-models-summary.log 2>&1` (đột biến production trên bản sao; test head giữ nguyên).
  output     : owner-wrong-principal → 63/68 rc1; grant-user-write → 63/68 rc1; inheritance-without-grant → 67/68 rc1; grant-admin-readonly → 67/68 rc1. Hai mutant nguy hiểm làm các ca Register thật dừng trước task; cả bốn có ca `dk_chay_icacls_dung_owner_va_grant` đỏ. Diff/output từng mutant ở `evidence/mutation-*.patch/.log`, JSON `evidence/mutations-models.json`.
  kết luận   : KHÔNG PHẢI LỖI ở điểm mù SID/mask cũ. Mô hình + assertion hợp đồng mới đã bắt 4/4 phản chứng mô hình lượt 4. Đây chỉ là mô hình tập lệnh ACL, không phải hiệu lực NTFS.

HƯỚNG 4: bảo toàn sáu chốt runtime của Register từ các lượt trước
  giả thuyết : thêm mô hình ACL vô tình làm suite không còn bắt bypass config/audit/inheritance/owner/reparse/hash.
  lệnh       : `python3 -u probes/mutations.py --group old > evidence/mutations-old-summary.log 2>&1`.
  output     : 6/6 mutant rc1; lần lượt drop-task-config 67/68, skip-audit 65/68, skip-inheritance 63/68, skip-owner-after-copy 63/68, skip-reparse 66/68, copy-hash 67/68. Các ca đỏ đúng hành vi liên quan, không có ParserError (`evidence/mutations-old.json`).
  kết luận   : KHÔNG PHẢI LỖI hồi quy ở sáu chốt đã đo. Không dùng số mutant đỏ để chứng nhận task/ACL native.

HƯỚNG 5: try/catch mới, continue trong try và phục hồi môi trường
  giả thuyết : catch mới nuốt lỗi thành `giu`/`bo_qua`, lỗi một công cụ dừng cả vòng, hoặc finally để lại HOME sai.
  lệnh       : `python3 probes/build-extra.py`; `python3 -u probes/run-user-extra.py > evidence/user-extra-summary.log 2>&1`; gọi Invoke-TangNguoiDung nguyên bản sao, executable fixture ghi argv thật, không mạng.
  output     : success 11 dòng/0 lỗi; npm-cannot-start 11/2; pip-fails (rc8) 11/1; py-disappears sau đọc ghim 11/3; venv-disappears sau Test-Path 11/1; nlm-pip-fails (rc8) 11/1; nlm-disappears ngay trước status 11/1; JSON hỏng 11/1; mode=keyring 11/1. Mọi ca error=null (hàm không ném ra ngoài), HOME/USERPROFILE restored=true. check-only 11 dòng, 0 native install, pip/PyYAML/jsonschema đều hiện diện; continue không bỏ nhầm công cụ sau. Full dữ liệu `evidence/user-extra.json`.
  kết luận   : KHÔNG PHẢI LỖI ở các catch mới với lỗi launch/install/status đã đo: đều ghi `loi`, không đổi thành `bo_qua`. Còn đường getter phiên bản chưa kiểm rc, tách H6. Thiếu venv vốn là `bo_qua` theo thiết kế, không phải catch mới.

HƯỚNG 6: đường thứ ba — phiên bản từ stderr của CLI đang thất bại
  giả thuyết : Get-PhienBanLenh ghép stderr vào stdout và không kiểm rc, nên lấy version Node trong stack lỗi làm version claude/codex rồi ghi ĐẠT.
  lệnh       : `python3 -u probes/run-user-extra.py`, mode `cli-version-stderr-fails` và `nlm-version-fails`; fixture claude/codex --version chỉ in stderr `Error: Cannot find module 'offline-missing-module'\nNode.js v24.2.0` rồi exit1; fixture nlm --version in version rồi exit9.
  output     : cả hai mode vẫn error=null, 11 dòng/0 lỗi; mode nlm-version-fails vẫn `nlm: giu, storage=file`. Chi tiết claude/codex và phép đo trực tiếp getter/rc sẽ bổ sung ngay sau probe độc lập. Code head :264 nhập `2>&1`, :265–266 chỉ regex, không đọc LASTEXITCODE; catch mới không bắt lỗi native rc thông thường.
  kết luận   : LỖI P1 của lớp xử lý lỗi native còn lại; đang kiểm lại bằng executable probe độc lập trước chốt finding. Đây không phải lỗi do mutant sản phẩm.

Bổ sung H6 — `pwsh/pwsh -NoProfile -File probes/version-failure.ps1 > evidence/version-failure.log 2>&1` → `{raw_rc:1,getter:"24.2.0",getter_native_rc:1,existing_can_install:true}`, probe_exit=0. Output gốc chỉ là stderr lỗi + phiên bản Node, không có phiên bản CLI. Trong `evidence/user-extra.json`, cli-version-stderr-fails ghi **claude và codex đều truoc=sau=24.2.0, hanh_dong=giu**, error_rows=0. Xác nhận P1 ở chính head; chưa chứng minh VM hiện đang gặp lỗi dependency này.

HƯỚNG 7: lưới cuối, lỗi lập trình và nhật ký
  giả thuyết : regex main xanh nhưng catch không thực sự ghi được lỗi/JSON/exit1 khi tầng ném.
  lệnh       : `python3 -u probes/run-main-tail.py > evidence/main-tail-summary.log 2>&1`; `probes/main-tail.ps1` nạp hàm head rồi chạy NGUYÊN VĂN suffix từ `$batDau = Get-Date` đến exit, các hàm tầng được stub ném/đạt. Không bỏ chốt nền của entry point hoặc giả chạy Windows.
  output     : success rc0, JSON ok=true/loi=0; user-throw, system-throw và programmer-throw đều rc1, JSON ok=false/loi=1, dòng tang-NguoiDung/tang-HeThong `loi`. Programmer-throw giữ thông báo Substring/startIndex trong chi_tiet. 4/4 oracle PASS (`evidence/main-tail.json`).
  kết luận   : KHÔNG PHẢI LỖI trong catch + tổng kết/ghi JSON của suffix đã đo. Catch rộng giữ lỗi lập trình thành thất bại có thông báo; không biến nó thành ĐẠT/bo_qua. Entry point Windows, identity, task và đường log mặc định Windows KHÔNG ĐO ĐƯỢC; probe dùng -NhatKy scratch rõ ràng.

HƯỚNG 8: oracle Register độc lập, mô hình đọc argv và giao quyền Tools
  giả thuyết : suite mới chỉ diễn theo số lệnh; head còn sửa ACL trên Tools hoặc owner/grant sai không tới audit.
  lệnh       : `python3 -u probes/registration-matrix.py > evidence/registration-summary.log 2>&1`; chạy lại oracle lượt 4, chỉ đổi đường head sang copies/head.
  output     : head clean: icacls=3, tool_acl_calls=0, audit=4, tasks=1 rồi REVIEW-STOP-BEFORE-CREDENTIALS; acl-reject/hash-reject: tasks=0; ancestor/child-link: 0 icacls,0 task. Mutant owner Users: lỗi chủ sở hữu BUILTIN\Users, tasks=0; grant Users F: lỗi FullControl, tasks=0. Bỏ inheritance/owner-after-copy cũng bị audit từ chối. JSON đầy đủ `evidence/registration-matrix.json`; mọi probe rc0 vì bắt lỗi để xuất dữ liệu.
  kết luận   : KHÔNG PHẢI LỖI với giao quyền Tools đã loại bỏ và hai phản chứng ACL trọng yếu. Oracle mô hình độc lập khớp các ca suite head mới. Hai mutant thiếu grant/admin readonly vẫn tới task trong oracle không mô phỏng quyền I/O, nhưng suite head đã có assertion hợp đồng làm chúng đỏ (H3). NTFS/effective ACL/task native KHÔNG ĐO ĐƯỢC.

HƯỚNG 9: răng của các ca mới và bốn chốt bổ sung
  giả thuyết : bỏ catch npm/rc status/lưới cuối vẫn xanh, hoặc cải tiến test ACL làm mất các chốt phụ.
  lệnh       : `python3 -u probes/user-mutations.py > evidence/mutations-user-summary.log 2>&1`; `python3 -u probes/mutations.py --group additional > evidence/mutations-additional-summary.log 2>&1`.
  output     : bỏ catch npm → `nd_npm_bien_mat_ghi_loi_va_chay_tiep` đỏ; bỏ rc status → `nd_nlm_status_rc_khac_0_la_loi` đỏ; bỏ lưới cuối → `main_co_luoi_cuoi_ghi_nhat_ky` đỏ; cả ba 67/68 rc1, parser_error=false. Bốn mutant icacls-tools/without-L/register-without-erroraction/swallow-rc lần lượt 64/68,67/68,66/68,67/68 rc1. Tổng đã đo 17/17 mutant làm suite đỏ (6 cũ + 4 bổ sung + 4 mô hình + 3 user/main), không lấy số executor khai làm số của reviewer.
  kết luận   : KHÔNG PHẢI LỖI ở các ca mới đã nhắm. npm và nlm-status chạy executable thật với hành vi fixture có chủ đích; main chỉ là regex đã được khai TĨNH, không coi mutant đỏ của nó là bằng chứng ghi nhật ký runtime. H7 bổ sung phép đo runtime suffix riêng. Điểm mù phiên bản H6 thuộc P1, không đếm thêm P2 chỉ vì cùng lỗi thiếu ca test.

HƯỚNG 10: đường installer HeThong — băm, mã lỗi, 3010, dọn tệp và dựng lại Commander
  giả thuyết : có đường chạy installer chưa kiểm băm, rc1603/3010 bị ghi sai, hoặc không dọn tải/dựng lại Commander.
  lệnh       : `python3 -u probes/system-matrix.py > evidence/system-summary.log 2>&1`; probe lượt 4 nạp bản sao head, giữ Save-CoKiemBam/Assert-Bam/New-ThuMucTai/Install-Msi/Invoke-TangHeThong thật; HTTP/phiên bản/Start-Process/task/icacls là fixture offline.
  output     : success 4 spawn, cả 4 hash_matches=true; download-tamper và missing-hash 0 spawn, 4 dòng loi; rc1603 4 loi và vẫn restart Commander; MSI3010 ghi can_khoi_dong_lai cho gh/node/pwsh; post-version-wrong ghi 4 loi. Cả sáu mode remaining_downloads=0; mọi mode có thử cài Node đều commander_restart=true. Chi tiết và command/rc `evidence/system-matrix.json`.
  kết luận   : KHÔNG PHẢI LỖI ở thứ tự băm/chạy, xử lý mã cài đặt và phục hồi đã đo. Không coi trường verified=true khi spawns=0 là bằng chứng dương có cài. Installer/msiexec/ACL/Node/Commander thật trên Windows KHÔNG ĐO ĐƯỢC. Get-PhienBanLenh được stub trong probe installer; kết quả này không phủ nhận lỗi H6.

HƯỚNG 11: nhánh không đo được và đếm ĐẠT
  giả thuyết : thiếu dependency/nền/quyền khiến ca bỏ qua nhưng vẫn tăng số ĐẠT.
  lệnh       : `python3 probes/test-accounting.py > evidence/test-accounting.log`; `TL_TEST_PYTHON=REVIEW_PYTHON_NOT_PRESENT pwsh/pwsh -NoProfile -File copies/head/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/missing-python.log 2>&1`.
  output     : 72 khai báo Ca, 72 tên duy nhất; Linux thực chạy 68. Thiếu Python → `doc_ghim_tu_ban_ke_that` ném command-not-found, DO, 67/68, rc1. Nhánh Windows admin `admin_ca_ma_thoat_3_khong_do_duoc` trả `$false` rõ ràng; ba ca native-user chỉ được khai báo ngoài Windows. Số ca Windows suy tĩnh: nonadmin 67, admin 66 với một ca không đo được bị đỏ; KHÔNG phải kết quả đã chạy Windows.
  kết luận   : KHÔNG PHẢI LỖI về bỏ qua vẫn đếm ĐẠT trong các nhánh đã kiểm. Số Linux 68/68 không mang sang Windows. Mô hình ACL/ZIP/task vẫn chỉ đo phần đã khai là giả; không phải skip native rồi gọi pass.

HƯỚNG 12: phản chứng khóa lỗi phiên bản và HINT thuần test
  giả thuyết : lỗi H6 chỉ do fixture đo của reviewer, hoặc ca thêm vào suite head không phân biệt được đường hỏng với control.
  lệnh       : `python3 -u probes/user-version-oracle.py > evidence/user-version-oracle.log 2>&1`; `python3 probes/build-hint.py`; `patch -p0 --dry-run -d hint-validation < HINT.patch`; `patch -p0 -d hint-validation < HINT.patch`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/hint-on-head.log 2>&1`.
  output     : oracle độc lập PASS success, FAIL cli-version-stderr-fails, FAIL nlm-version-fails, **1/3 PASS, rc1**. Dry-run/apply HINT rc0. Suite head + hai ca HINT → **68/70, rc1**, chỉ hai ca mới `nd_cli_version_hong_phai_ghi_loi` và `nd_nlm_version_rc_khac_0_phai_ghi_loi` đỏ. Prototype tối thiểu trên BẢN SAO `hint-fix-validation/` chỉ từ chối rc native≠0 ở getter → **70/70, rc0** (`evidence/hint-with-prototype.log`). Không sửa cây review và không giao production patch.
  kết luận   : LỖI P1 H6 được khóa bởi test tích hợp và control xanh; không có ParserError hay dependency hỏng làm đỏ giả. 70/70 chỉ xác minh tính phân biệt của hai ca mới trên prototype scratch, không phải approval cho một bản vá tương lai.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| slug lượt 4 | phân loại tại head này | phép đo và giới hạn |
|---|---|---|
| loi-native-tang-nguoi-dung [P1] | **ĐÃ VÁ THẬT hai phản chứng cũ và lưới cuối; CHƯA VÁ hết lớp** | Oracle lượt 4 nay 3/3 PASS; thêm launch/pip/venv/status/JSON lỗi đều ghi loi, tiếp tục đúng (H2/H5); suffix main 4/4 ghi JSON/exit đúng (H7). Nhưng getter còn nhận chuỗi version dù native exit1/9, CLI hỏng được ghi giu (H6/H12). Giữ stable ID này, không đếm hai lỗi P1. |
| test-thieu-duong-tich-hop [P2] | **ĐÃ VÁ THẬT điểm mù owner/grant được nêu ở lượt 4** | Owner Users và grant Users F nay đều 63/68 rc1; thiếu grant/admin readonly cũng đỏ; sáu chốt cũ và bốn bổ sung còn đỏ. Oracle ACL độc lập khớp việc reject trước task (H3/H4/H8/H9). Không có P2 mới được chứng minh chỉ từ giới hạn mô hình đã khai; lỗi getter và thiếu ca khóa tương ứng tính trong P1. |

Không có bằng chứng bản vá lượt 4 tạo ra lỗi mới trong nhánh catch/mô hình ACL đã đo. Getter ở H6 là **đường còn sót mới phát hiện**: `git -C cay-kho blame -L 262,266 ea5ccd5edeaccfce36eb3a8723002c636dcaf206 -- ops/vm/cap-nhat-cong-cu.ps1` → cả năm dòng từ commit `22840642` (trước bản vá lượt 4), không phải catch mới sinh ra.

### loi-native-tang-nguoi-dung  [P1]  Getter nhận phiên bản từ lệnh thất bại, kể cả phiên bản Node trong stderr lỗi CLI

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:264`–`:266` (Get-PhienBanLenh); người gọi npm `:392`, `:397`–`:399`, nlm `:419`–`:433`; tổng kết `:627`–`:640`.

VẤN ĐỀ: Get-PhienBanLenh chỉ catch lỗi khởi chạy, không kiểm mã thoát của tiến trình. Nó ghép stderr vào stdout rồi regex trên toàn bộ văn bản. Nếu claude.cmd/codex.cmd khởi chạy được nhưng CLI hỏng, output lỗi kiểu `Error: Cannot find module ...` + `Node.js v24.2.0` và exit1 vẫn cho phiên bản `24.2.0`. Khi npm install rc0, cả lần đo trước/sau đều trả chuỗi ấy, nên tầng NguoiDung ghi `giu` cho hai CLI không chạy được, không có dòng loi. Với nlm --version trả text đúng rồi exit9, pip/status rc0 cũng che lỗi version thành `giu, storage=file`. Các catch mới không bắt native rc mặc định không ném. Getter dùng chung cho các công cụ/tầng khác nên nên đóng ở đây. Hai biểu hiện npm launch và nlm storage-status cũ đã sửa; đây là biểu hiện thứ ba cùng lớp, không nhân thành finding mới.

ĐÃ THỬ NGHIỆM: `pwsh/pwsh -NoProfile -File probes/version-failure.ps1` → raw_rc=1, getter_native_rc=1, getter="24.2.0", chỉ stderr lỗi có chuỗi Node; probe_exit=0. `python3 -u probes/run-user-extra.py` → mode cli-version-stderr-fails: Invoke-TangNguoiDung nguyên bản sao head trả 11 dòng, error=null, error_rows=0, claude/codex đều truoc=sau=24.2.0 và `giu`; mode nlm-version-fails: nlm `giu`, storage=file, error_rows=0. `python3 -u probes/user-version-oracle.py` → 1/3 PASS, rc1. HINT test-only áp trên head copy → 68/70 rc1 đúng hai ca mới; prototype scratch đòi rc0 ở getter → 70/70 rc0. Theo công thức main nguyên bản, error_rows=0 dẫn ok=true/exit0; chỉ công thức này là phân tích tĩnh với kết quả hàm H6, không khai đã chạy toàn entry point Windows. Suffix main được đo độc lập H7. Các fixture là executable cục bộ có rc thật; không chạy pip/npm/package hoặc CLI thực và không suy VM hiện đang gặp sự cố ấy.

ĐỘ TIN: cao về false success của chính head với phản chứng executable; tình trạng package/dependency thực tế trên Windows KHÔNG ĐO ĐƯỢC.

GỢI Ý VÁ: ở Get-PhienBanLenh, lưu rc NGAY sau native call và chỉ trả phiên bản khi tiến trình hoàn tất thành công; lỗi launch/rc/không match phải trả không biết để người gọi ghi loi theo hợp đồng. Kiểm các caller đang coi không biết là `giu`/`kiem` nếu muốn khai bao phủ cả lớp, đặc biệt dòng python chỉ báo :356; không tự nâng Python/đổi major để chữa getter. Khóa bằng hai ca tích hợp HINT (CLI stderr có version Node + exit1; nlm stdout version đúng + exit9), control rc0 vẫn đủ 11 dòng, giữ hai phản chứng cũ và ca main. Đột biến bỏ kiểm rc getter phải làm hai ca mới đỏ. Rủi ro vá: thu rc quá muộn có thể lấy rc của lệnh khác; ép mọi stderr thành lỗi có thể loại công cụ hợp lệ vốn in version ra stderr; rc0 vẫn cần định dạng version đúng công cụ. Không dùng bản vá ở wrapper pip/npm riêng để bỏ sót các caller khác.

`HINT.patch` chỉ sửa `ops/vm/cap-nhat-cong-cu_test.ps1`, định dạng **patch -p0 từ gốc bản sao cay-kho/**. SHA256 `d3294ae2d8fbc6ad498dbf5799b85caaea47d613f5ea952956c82e656187b46f`.
**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Nếu dùng phải khai hint_provenance. Hai ca mới dùng shebang nên chỉ có trên Linux, như ba ca native-user sẵn có; executor cần ca/đo tương ứng trên Windows. Prototype scratch chỉ dùng để kiểm răng ca test, không phải patch sản phẩm được giao hoặc approval.

## GIỚI HẠN VÀ QUYẾT ĐỊNH

Review class: sensitive (SYSTEM/admin/ACL). Reviewer Codex/OpenAI, model GPT-6 theo định danh phiên; không có phép đo deployment model riêng. Execution surface thực tế: API agent với functions.exec/exec_command và shell Ubuntu 24.04.5 LTS; transport machine/local; session runs/22677e0d; github_submitter_identity=null. Context độc lập executor Claude. Chỉ thị người dùng trong prompt.snapshot là authority cho review này, phạm vi toàn ops/vm/ tại exact SHA, loại trừ ops/land/. PowerShell Linux 7.6.9, Python 3.13.17. Không tự cấp authority merge/land/deploy.

- Baseline head: **68/68, rc0**. Oracle lỗi native cũ: **3/3 PASS, rc0**. **17/17** mutant suite đã đo rc1 đúng ca, gồm owner/grant cũ và ba chốt mới. Oracle phiên bản còn lỗi: **1/3 PASS, rc1**; hai failure có chủ ý là bằng chứng P1. HINT trên head **68/70, rc1**; prototype scratch **70/70, rc0**.
- Còn **một P1**, giữ slug loi-native-tang-nguoi-dung; P2 mô hình owner/grant cũ đã đóng trong phạm vi phản chứng đã yêu cầu. Không đếm thêm P2 cho thiếu test của cùng P1. Không tìm thấy P0 mới được chứng minh; không tuyên bố Windows đã an toàn.
- **KHÔNG ĐO ĐƯỢC Windows native**: NTFS junction/owner/effective ACL/handle, icacls, Scheduled Task/COM/password/task DACL, msiexec/installer, PATH/profile của SYSTEM/tlcommander và Commander thật. Linux symlink chỉ chứng minh scan/dispatch. Suite mô hình và suffix main không thay phép đo này; executor sẽ báo Windows riêng, phiên này không nhận lời đó làm kết quả đã đo.
- Các điều kiện môi trường chưa chứng minh vẫn cần VM: tổ tiên Program Files/TEMP/log phải tin cậy; ACL thư mục tải và chênh lệch kiểm băm/chạy theo tên; module autoload/PATH và quyền task. Không tự gán P0 từ điều kiện chưa xác minh. Không khẳng định đã thu hồi ACL từng cấp trên VM trong lịch sử.
- Không gọi mạng; không credential thật; không cài gói hay task native; không push/commit; không sửa cây cay-kho/. Các bản sao, mutant, probe, HINT và evidence nằm ngoài cây review. PROMPT.md và prompt.snapshot cùng SHA256 `4f35549ef0bbb17d637eeb2bfd0bafee37103cf846c9ec916585b91792286a84`.

Kiểm cuối read-only: `python3 probes/final-audit.py > evidence/final-readonly.log 2>&1` → audit_exit=0; HEAD vẫn `ea5ccd5edeaccfce36eb3a8723002c636dcaf206`, tree `aec9ad192c8f96413a768151d9bc11e1a5ab4855`; detached (`symbolic-ref -q HEAD` rc1 đúng mong đợi); status kể cả ignored rỗng; diff/cached diff/diff --check ops/vm/ so lượt 4 đều rỗng rc0; core.abbrev=7, shallow=false. Cả ba tệp ops/vm/ khớp byte blob Git của reviewed_sha và copies/head. 17 mutant đều rc1, có ca đỏ, **0 ParserError**. Chi tiết command/rc/hash ở `evidence/final-readonly.json`.

Quyết định: **changes_requested** vì P1 phản chứng phiên bản vẫn hiện diện tại exact head. Các phản chứng cũ và P2 ACL đã được cải thiện thực chất; kết quả ấy không triệt tiêu false success mới đo ở getter. Không cần quyền hoặc thao tác nào trên executor branch để hoàn tất review này.
