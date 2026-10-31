verdict: changes_requested
reviewed_sha: 28fdbdf0e6e8ce5565b6f2317bf28b05c63e81d0

Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

## ĐÓNG FINDING LƯỢT 5

Đã kiểm chứng độc lập trên bản sao đúng byte head. Ba biểu hiện cũ đóng thật, nhưng lớp lỗi còn đường khác; không đồng nhất "đóng phản chứng" với "đóng lớp".

| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung — npm mất tệp | **ĐÃ VÁ THẬT biểu hiện** | `python3 -u probes/l4-user-oracle.py` → npm-disappears PASS; có loi, còn rg/shellcheck/actionlint/nlm, oracle 3/3 rc0. |
| loi-native-tang-nguoi-dung — nlm status rc7 | **ĐÃ VÁ THẬT biểu hiện** | Cùng oracle → nlm-status-fails PASS; JSON file + rc7 nay nlm loi. |
| loi-native-tang-nguoi-dung — version CLI rc1/9 | **ĐÃ VÁ THẬT biểu hiện cài thật** | `python3 -u probes/user-version-oracle.py` → 3/3 PASS rc0; `pwsh/pwsh -NoProfile -File probes/version-failure.ps1` → getter=null dù stderr có version Node. |
| loi-native-tang-nguoi-dung — toàn lớp [P1] | **CHƯA ĐÓNG (VÁ HỜ ở cấp lớp)** | `python3 -u probes/new-paths-oracle.py` → 2/6 PASS rc1: check-cli/check-nlm/metadata-fails/check-metadata vẫn exit0, loi=0, ok=true (H6/H7/H12). |

## BẢNG SĂN

Khởi đầu: đã đọc `runs/1d559342/prompt.snapshot`; chỉ đọc `cay-kho/`, không push, không gọi mạng. Mọi phép đo sửa fixture sẽ chạy ngoài cây nguồn.

HƯỚNG 1: baseline Linux, SHA và tính nguyên vẹn
  giả thuyết : cây không đúng head hoặc khai 72/72 không tái hiện.
  lệnh       : `git -C cay-kho rev-parse HEAD`; `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : HEAD 28fdbdf0e6e8ce5565b6f2317bf28b05c63e81d0; status rỗng; `cap-nhat-cong-cu tests: 72/72 ca QUA`, rc0. Ba tệp ops/vm/ khớp byte blob Git và copies/head/; Git đầy đủ, core.abbrev=7 (evidence/preflight.json).
  kết luận   : KHÔNG PHẢI LỖI ở baseline Linux. Windows 68/68 là khai của executor, chưa đo độc lập ở đây. Môi trường không cung cấp tool environment_status; không gọi mạng để thay thế. Reviewer Codex / GPT-6, local shell, machine/local; không dùng context executor.

HƯỚNG 2: chạy lại oracle lượt 4 và lượt 5, đủ ba biểu hiện cũ
  giả thuyết : npm mất tệp vẫn làm dừng tầng; nlm status exit7 vẫn thành giu; version CLI exit1/9 vẫn được getter nhận.
  lệnh       : `python3 -u probes/l4-user-oracle.py`; `python3 -u probes/user-oracle.py`; `python3 -u probes/user-version-oracle.py`; `pwsh/pwsh -NoProfile -File probes/version-failure.ps1` (log tương ứng trong evidence/).
  output     : oracle lượt 4: `3/3 PASS`; oracle lỗi native lượt 5: `3/3 PASS`; version native failure oracle: `3/3 PASS`; tất cả rc0. Probe trực tiếp getter: raw_rc=1, getter=null, getter_native_rc=1, existing_can_install=false. Các executable fixture giữ hành vi lỗi thật và mã thoát thật; source nạp từ copies/head/ khớp Git, không sửa production.
  kết luận   : KHÔNG PHẢI LỖI với ba biểu hiện cũ: npm biến mất có loi và chạy tiếp; status exit7 có nlm loi; version exit1/9 bị loại và caller cài thật có loi. Chưa kết luận đóng cả lớp cho tới khi kiểm hết caller/null và các đường native còn lại.

HƯỚNG 3: try/catch, continue, lỗi lập trình và lưới cuối
  giả thuyết : catch biến lỗi thành bo_qua/ĐẠT, continue bỏ nhầm công cụ, hoặc không khôi phục HOME/USERPROFILE.
  lệnh       : `python3 -u probes/run-user-extra.py > evidence/user-extra-summary.log 2>&1`; `python3 -u probes/run-main-tail.py > evidence/main-tail-summary.log 2>&1`.
  output     : 12 mode user đều error=null, HOME/USERPROFILE restored=true; npm-cannot-start 11 dòng/2 loi; pip-fails 11/1; py-disappears 11/3; venv-disappears, nlm-pip-fails, nlm-disappears, JSON hỏng, keyring đều 11/1. check-only control: 11 dòng, 0 install; cli-version-stderr-fails 11/2; nlm-version-fails 11/1. Suffix main nguyên văn: success rc0 ok=true; user-throw/system-throw/programmer-throw đều rc1 ok=false loi=1; 4/4 PASS. Lỗi Substring vẫn giữ trong chi_tiet.
  kết luận   : KHÔNG PHẢI LỖI ở các catch/continue đã đo; không nuốt lỗi lập trình thành thành công hay bo_qua. Suffix được trích từ head, identity và hàm tầng là fixture; không khai đã chạy entry point Windows. Các catch trong bước cài đều giữ thất bại, không retry vô hạn.

HƯỚNG 4: hồi quy ACL/register và điểm mù principal/quyền của mô hình
  giả thuyết : đồ giả mới vẫn cho owner Users, Users F hoặc bỏ audit/hash/reparse/config được suite xanh.
  lệnh       : `python3 -u probes/mutations.py --group old > evidence/mutations-old-summary.log 2>&1`; `python3 -u probes/mutations.py --group models > evidence/mutations-models-summary.log 2>&1`.
  output     : 6 mutant runtime cũ đều rc1: drop-task-config 71/72; skip-audit 69/72; skip-inheritance 67/72; skip-owner-after-copy 67/72; skip-reparse 70/72; copy-hash 71/72. Bốn mutant model đều rc1: owner Users 67/72, Users F 67/72, inheritance-without-grant 71/72, admin readonly 71/72. Các ca đỏ liên quan và diff/output lưu trong evidence/mutations-*.json, mutation-*.patch/.log; không ParserError.
  kết luận   : KHÔNG PHẢI LỖI với 10 phản chứng này. SID owner và mask grant thực sự ảnh hưởng dữ liệu audit, không chỉ kiểm có tên lệnh. Mô hình chỉ mô tả tập lệnh hiện hành; không phải engine NTFS, không đo effective ACL trên Windows.

HƯỚNG 5: tải/băm/installer tầng HeThong và dọn dẹp
  giả thuyết : nhận null phiên bản/rc lỗi có thể dẫn tới chạy installer chưa kiểm băm, bỏ lỗi hoặc mất Commander.
  lệnh       : `python3 -u probes/system-matrix.py > evidence/system-summary.log 2>&1` (replay probe installer lượt 4/5 trên copies/head/).
  output     : control 4 spawn, 4 hash_matches=true, 0 tải còn lại; download-tamper và missing-hash: 0 spawn, 4 loi. rc1603: 4 loi, vẫn restart Commander; MSI3010: gh/node/pwsh can_khoi_dong_lai; post-version-wrong: 4 loi. Sáu mode error=null; mọi mode thử cài Node đều restart=true và 0 tệp tải còn lại.
  kết luận   : KHÔNG PHẢI LỖI trong luồng được mô phỏng. Save/Assert-Bam/New-ThuMucTai/Install-Msi/Invoke-TangHeThong là thật; HTTP/phiên bản/Start-Process/task/icacls là fixture offline. verified=true khi 0 spawn là all(empty), không dùng làm bằng chứng dương. msiexec, ACL, Commander thật KHÔNG ĐO ĐƯỢC trên Linux; getter null sẽ đo riêng với executable ở hướng kế tiếp.

HƯỚNG 6: caller getter nhận null — kiểm tất cả vị trí, đặc biệt -ChiKiem
  giả thuyết : getter đã đúng nhưng một caller vẫn biến không đọc được phiên bản thành ĐẠT.
  lệnh       : `rg -n 'Get-PhienBanLenh|LASTEXITCODE|catch|continue|bo_qua|ChiKiem' copies/head/ops/vm/cap-nhat-cong-cu.ps1 > evidence/caller-native-audit.txt`; `pwsh/pwsh -NoProfile -File probes/caller-null.ps1 -Mode system-pre`; chạy riêng cùng probe với `-Mode system-post`, `-Mode zip-pre`, `-Mode zip-post` (lệnh đầy đủ và rc ở evidence/caller-null.json); `pwsh/pwsh -NoProfile -File probes/new-paths.ps1 -Mode check-cli`; cùng probe `-Mode check-nlm`, `-Mode check-python`; suffix main NGUYÊN VĂN qua các lệnh kèm `-Log` ghi đầy đủ ở evidence/new-main.json, tái lập bằng probes/new-paths-oracle.py.
  output     : system-pre (4 executable in version rồi exit9): 4 loi, 0 HTTP fixture, 0 spawn; system-post: 4 spawn, hậu kiểm getter null → 4 loi; zip-pre null được sửa bằng ZIP hợp băm, kết quả cai_moi/2.0.0; zip-post getter null → 1 loi. Python exit3: 1 loi, dừng tầng, suffix rc1/ok=false. Nhưng check-cli: claude/codex trước/sau rỗng, hanh_dong=kiem, 11 dòng/0 loi; check-nlm: nlm rỗng, kiem, last_native_exit=9, 11/0. Cả hai suffix main in `TONG: 11/11 dat · loi 0`, ghi ok=true, exit0 (evidence/new-main.json và new-main-check-*.json/.log).
  kết luận   : LỖI P1 tiếp diễn của loi-native-tang-nguoi-dung, ở hai nhánh ChiKiem :399/:419. Các nhánh cài thật xử lý null đúng, HeThong không mở đường cài mù. ZIP probe dùng Save/hash/Expand-Archive/copy/getter thật; Copy-Item chỉ thêm chmod +x cần cho executable Linux, HTTP/install/task là fixture offline. Suffix thực thi đúng nguyên văn sau chốt nền, không phải entry point Windows. Không nâng phép đo này thành xác minh NTFS/msiexec.

HƯỚNG 7: đường thứ ba ngoài getter — mã thoát đọc metadata Python bị bỏ qua
  giả thuyết : chuyển kiểm rc vào Get-PhienBanLenh không phủ các lời gọi `python -c importlib.metadata` riêng.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/new-paths.ps1 -Mode metadata-fails`; cùng lệnh `-Log evidence/new-main-metadata-fails.json` (evidence/new-metadata-fails.log, new-main-metadata-fails.log, new-main.json).
  output     : fixture --version rc0, install rc0; mỗi metadata probe in đúng version (25.0/6.0.3/4.25.1), stderr REVIEW-metadata-native-error, rồi exit6. Hàm thật vẫn ghi cả pip/PyYAML/jsonschema truoc=sau đúng chuỗi và giu; error=null, 11 dòng/0 loi. Suffix main ghi ok=true/loi=0, `TONG: 11/11 dat`, rc0. :375 chỉ lưu rc của pip install; :376 đọc lại metadata nhưng :377 dùng rc install, không đọc mã thoát metadata.
  kết luận   : LỖI P1 cùng lớp xử lý lỗi native, chưa ai chỉ đường importlib.metadata trong các finding trước. Không đếm thêm một P1 cho mỗi biểu hiện. Đây là executable phản chứng trả lỗi thật, không mutant sản phẩm và không chứng minh Python thật trên VM hiện đang lỗi. Getter mới không tham gia đường này.

HƯỚNG 8: răng của ca mới và các chốt bổ sung
  giả thuyết : bỏ hai dòng vá mới (getter rc, Python guard) không làm test đỏ; đồ giả không diễn lỗi thật.
  lệnh       : `python3 -u probes/new-mutations.py > evidence/mutations-new-summary.log 2>&1` (mỗi bản sao riêng chạy bộ test head); `python3 -u probes/user-mutations.py`; `python3 -u probes/mutations.py --group additional`.
  output     : bỏ getter rc → 68/72 rc1, đúng bốn ca phien_ban_lenh/nd_python/nd_cli/nd_nlm đỏ; bỏ Python guard → 71/72 rc1, đúng nd_python đỏ. Ba mutant npm-catch/status-rc/main-catch đều 71/72 rc1 đúng ca tương ứng; bốn mutant Tools ACL, bỏ /L, Register thiếu ErrorAction, icacls nuốt rc lần lượt 68/72,71/72,70/72,71/72 rc1. Cộng H4: 19/19 mutant bị giết, 0 ParserError.
  kết luận   : KHÔNG PHẢI LỖI về răng của các ca mới đối với đường mà chúng nhắm; fixture rc1/3/9 thật được getter đọc thật, không đặt kết quả sản phẩm theo số lần gọi. Fixture thành công trả version cố định, nên không coi các ca này là bằng chứng nâng package thật. main-catch chỉ test regex tĩnh, H3 có phép đo suffix runtime bổ sung. Không sinh thêm P2 chỉ vì ca còn thiếu của P1 H6/H7.

HƯỚNG 9: không đo được có bị đếm ĐẠT, đối chiếu hai nền
  giả thuyết : thiếu Python/nền/quyền vẫn tăng số ca QUA hoặc lấy số Linux làm số Windows.
  lệnh       : `TL_TEST_PYTHON=REVIEW_PYTHON_NOT_PRESENT pwsh/pwsh -NoProfile -File copies/head/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/missing-python.log 2>&1`; regex liệt kê tên `Ca` và các nhánh IsWindows/laAdmin (evidence/test-accounting.json).
  output     : 76 khai báo/76 tên duy nhất, Linux thực chạy 72. Thiếu Python: doc_ghim_tu_ban_ke_that DO, 71/72 rc1. Nhánh admin không đo được rc3 trả false; sáu ca native-user ngoài Windows không được đăng ký trên Windows. Số tĩnh Windows nonadmin 68, admin 67 (có một ca đỏ không đo được), KHÔNG phải kết quả chạy.
  kết luận   : KHÔNG PHẢI LỖI về bỏ qua vẫn đếm đạt trong các nhánh đã rà. Lỗi P1 H6 là kết quả sản phẩm `kiem`, không phải bộ test tự skip rồi đếm pass. Windows getter .cmd, NTFS junction/icacls/task/msiexec thật KHÔNG ĐO ĐƯỢC tại đây.

HƯỚNG 10: oracle Register độc lập và rà toàn ops/vm/
  giả thuyết : suite đóng điểm mù nhưng Register thật vẫn giao Tools ACL hoặc không dừng trước tác vụ khi ACL/hash/reparse sai.
  lệnh       : `python3 -u probes/registration-matrix.py > evidence/registration-summary.log 2>&1`; `pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source-audit.log 2>&1`; `git -C cay-kho blame -L 370,378 28fdbdf0e6e8ce5565b6f2317bf28b05c63e81d0 -- ops/vm/cap-nhat-cong-cu.ps1`.
  output     : head clean icacls=3/tool_acl_calls=0/audit=4/tasks=1 rồi dừng trước credential; acl-reject/hash-reject tasks=0; ancestor/child symlink 0 icacls/0 task. Owner Users và grant Users F bị audit từ chối/tasks=0. Thiếu grant/admin readonly vẫn tới task trong oracle không mô phỏng effective I/O, nhưng suite đã bắt bằng assertion argv H4. AST parse_errors=0; README_native_acl_commands=0. Metadata :371–378 bắt nguồn 22840642, có trước bản vá hiện tại (evidence/metadata-blame.txt).
  kết luận   : KHÔNG PHẢI LỖI mới ở register và đường SYSTEM đã đo. Không tìm thấy P0 mới được chứng minh; không suy an toàn native Windows. Đã đọc cả ba tệp ops/vm/, rà mọi call native/catch và hướng dẫn; không đọc hay chạy ops/land/. H6/H7 là đường còn sót cũ, không có bằng chứng catch mới tạo lỗi ấy.

HƯỚNG 11: phản chứng test-only HINT và kiểm khả năng phân biệt
  giả thuyết : kết quả H6/H7 chỉ do bộ giàn reviewer hỏng, hoặc ca khóa không phân biệt head với việc xử lý rc/null.
  lệnh       : `python3 probes/build-hint.py`; `patch -p0 --dry-run -d hint-validation < HINT.patch`; `patch -p0 -d hint-validation < HINT.patch`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1`; cùng lệnh trên hint-prototype/.
  output     : dry-run/apply rc0; head + HINT → 72/76 rc1, đúng bốn ca mới nd_chikiem_cli, nd_chikiem_nlm, nd_metadata và nd_chikiem_metadata đỏ. Prototype scratch chỉ phân loại null trong ChiKiem và kiểm rc metadata → 76/76 rc0; 72 ca cũ vẫn xanh. HINT chỉ sửa TEST; prototype không nằm trong HINT và không phải production patch giao nộp.
  kết luận   : LỖI P1 đã có phản chứng tích hợp có control và khả năng phân biệt; không ParserError, không lỗi dependency giàn. 76/76 chỉ xác minh răng của hint trên prototype, không approve bản vá tương lai hay xác nhận Windows.

HƯỚNG 12: oracle có khẳng định hậu điều + suffix main cho các đường còn sót
  giả thuyết : H6/H7 chỉ in kết quả nhưng thực ra các dòng lỗi/mã thoát/nhật ký đã đúng.
  lệnh       : `python3 -u probes/new-paths-oracle.py > evidence/new-paths-oracle.log 2>&1` (fixture riêng dưới fixtures/, tự dọn, giữ trace argv thật trong JSON).
  output     : control check-only PASS rc0/ok=true/loi0; check-python PASS rc1/ok=false/loi1; check-cli FAIL rc0/ok=true/loi0; check-nlm FAIL rc0/ok=true/loi0; metadata-fails FAIL rc0/ok=true/loi0; check-metadata FAIL rc0/ok=true/loi0. `Remaining native paths oracle: 2/6 PASS`, oracle rc1. Metadata fixture chạy trực tiếp ngoài hàm: pip/PyYAML/jsonschema stdout=25.0/6.0.3/4.25.1, control rc0, broken rc6 + stderr REVIEW-metadata-native-error (evidence/metadata-direct.json).
  kết luận   : LỖI P1 được xác nhận cả kết quả theo công cụ và JSON/mã thoát runtime của suffix nguyên bản. Bốn ca FAIL là phản chứng sản phẩm có chủ ý, không phải thiếu công cụ giàn; ghi riêng khỏi baseline 72/72. Identity fixture chỉ phục vụ in tên, không giả chạy entry point Windows.

## KIỂM MỌI CALLER CỦA GET-PHIENBANLENH

| vị trí trong ops/vm/cap-nhat-cong-cu.ps1 | khi null | bằng chứng / đánh giá |
| --- | --- | --- |
| Update-CongCuZip trước :322 | không thể so, cài lại hoặc can_cap_nhat | H6 zip-pre: ZIP hợp băm sửa được, version sau 2.0.0, cai_moi. Đây là portable, không có ràng buộc giữ major như Node. |
| Update-CongCuZip sau :341 | Compare(null,moi) khác 0, loi | H6 zip-post 1 loi; getter thật. |
| Python :359 | loi và return | Ca suite mới + H6/check-python suffix rc1. |
| npm trước :397 | cài thật có thể sửa; ChiKiem ghi kiem ngay | Oracle cũ cài thật đã PASS; H6/H12 chứng minh ChiKiem lỗi vẫn ok=true. |
| npm sau :402 | loi nếu không có sau | Version failure oracle 3/3 PASS. |
| nlm trước :418 | cài thật có thể sửa; ChiKiem ghi kiem ngay | H6/H12 chứng minh đường ChiKiem còn lỗi. |
| nlm sau :424 | loi khi sau null (dù vẫn probe status rồi mới phân loại) | Version failure oracle và user-extra; không bị status rc0 che nữa. |
| HeThong trước :463 | tệp có mặt thì loi/không cài; chưa có tệp thì cho cài | H6 system-pre: cả git/gh/node/pwsh 4 loi/0 spawn/0 HTTP. Điều kiện Test-Path phân biệt chưa cài với đã có mà hỏng. |
| HeThong sau :504 | rc installer0 + null → loi; MSI3010 giữ can_khoi_dong_lai chờ reboot | H6 system-post 4 loi; H5 đo riêng 3010. Không yêu cầu phiên bản có hiệu lực ngay khi installer đã báo cần reboot. |

## ĐỐI CHIẾU LƯỢT TRƯỚC

| lớp / nguồn | phân loại tại head này | phép đo và giới hạn |
| --- | --- | --- |
| loi-native-tang-nguoi-dung [P1], lượt 5 ea5ccd5edeaccfce36eb3a8723002c636dcaf206 | **VÁ HỜ ở cấp lớp; ba phản chứng cũ ĐÃ VÁ THẬT** | H2 các oracle cũ đều 3/3 PASS; H3 catch/main giữ loi; H6/H7/H12 còn false success ở ChiKiem và metadata. Giữ một stable slug, một P1, không nhân theo công cụ/biểu hiện. |
| test-thieu-duong-tich-hop [P2], đã đóng ở lượt 5 | **Vẫn đóng điểm mù owner/grant đã nêu** | H4 owner/grant sai đều làm suite đỏ; H10 model độc lập audit reject. Không dùng mô hình làm bằng chứng NTFS. Không mở lại chỉ vì giới hạn mô hình vốn đã khai. |

Không có bằng chứng bản vá lượt 5 tự tạo lỗi mới ở try/catch/getter/Python guard. Những đường còn lại là chỗ chưa được phủ: :371–378 đã tồn tại từ 22840642. Cả ba tệp ops/vm/ đã được rà; không review ops/land/pr1065-*.

### loi-native-tang-nguoi-dung  [P1]  ChiKiem và metadata vẫn biến lỗi native thành lượt ĐẠT

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:399` và `:419` (caller ChiKiem bỏ qua null của getter); `:371`, `:373`, `:375`–`:378` (metadata Python bỏ qua rc riêng); hệ quả tổng kết/JSON/exit ở `:632`–`:645`.

VẤN ĐỀ: Getter mới từ chối rc≠0 đúng, nhưng caller claude/codex/nlm ở ChiKiem không kiểm kết quả ấy: CLI tồn tại, khởi chạy rồi exit1/9 vẫn được ghi `kiem` với phiên bản rỗng. Không có dòng loi nên main ghi ok=true/thoát0. Đường khác hoàn toàn không đi qua getter: `python -c importlib.metadata` trước/sau cài có thể in chuỗi phiên bản rồi thoát lỗi. Code chỉ lưu rc pip install, không lưu rc của metadata; nếu stdout còn phiên bản hợp ghim, nó ghi giu ngay cả khi mọi probe metadata exit6. Ở ChiKiem, nó đi tiếp sau phép đo lỗi trước cài. Đây là một lớp xử lý thất bại native còn sót, không phải P0, và không phải các try/catch mới che lỗi launch; native rc thông thường không ném để catch bắt được.

ĐÃ THỬ NGHIỆM: `python3 -u probes/new-paths-oracle.py` → 2/6 PASS, rc1. Hai control là kiểm bình thường và Python --version lỗi được phân loại đúng. Bốn phản chứng check-cli/check-nlm/metadata-fails/check-metadata đều khiến suffix main nguyên văn ghi 11/11 dat, loi=0, ok=true và exit0; từng dòng lỗi cần có đều vắng (evidence/new-paths-oracle.json/.log và new-oracle-*.json/.log). Probe nạp hàm nguyên bản từ copies/head/, chạy executable fixture thật với stdout/stderr/rc thật; không đột biến production. Get-PhienBanLenh là thật, Set-Path/ZIP chỉ stub để tránh đổi PATH/cài/mạng. `HINT.patch` test-only áp trên head copy → 72/76 rc1 đúng bốn ca mới; prototype scratch phân loại null/rc → 76/76 rc0. Entry point, identity thật và package Python/CLI thật trên VM Windows KHÔNG ĐO ĐƯỢC, không suy VM hiện đang hỏng.

ĐỘ TIN: cao về hành vi sai của chính head với các đầu vào lỗi native đã đo; không khai lỗi thực tế đang xảy ra trên VM.

GỢI Ý VÁ: ở :399/:419, khi ChiKiem không đọc được phiên bản phải ghi loi/không biết rõ ràng, và tổng kết không được ok=true cho phép đo thất bại; phân biệt tệp chưa cài nếu muốn hiển thị can_cap_nhat. Ở :371/:376 lưu rc NGAY sau từng metadata probe; chỉ tin phiên bản khi lệnh thành công. Trước cài có thể chưa có package nhưng cài xong và hậu kiểm thành công vẫn là một lần khôi phục hợp lệ; lỗi phép đo sau cài không được che bởi rc install0. Giữ rc install/status/metadata tách biệt và tiếp tục công cụ độc lập. Ca khóa: hai lỗi version trong ChiKiem, metadata có stdout hợp ghim nhưng exit6 ở cả cài thật/ChiKiem; control rc0, getter hỏng, npm mất tệp, status rc7 và suffix main phải giữ kết quả cũ. Bản vá có thể làm thiếu-package bị coi là lỗi không thể sửa, dừng vòng sai, hoặc đổi ChiKiem thành cài thật; các ca phải khóa cả ba rủi ro. Không chỉ thêm catch vì exit code khác0 không tự ném.

`HINT.patch` định dạng `patch -p0` từ gốc bản sao cay-kho/, chỉ sửa TEST `ops/vm/cap-nhat-cong-cu_test.ps1`.
**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Nếu dùng, executor khai hint_provenance; artifact không cấp quyền push/merge/land. Prototype nằm riêng trong hint-prototype/, không giao production patch và không được coi là sửa cây đang review.

## GIỚI HẠN VÀ QUYẾT ĐỊNH

- Baseline Linux Ubuntu 24.04.5 / PowerShell 7.6.9: **72/72 PASS, rc0**. Phản chứng mới: oracle **2/6 PASS, rc1**; HINT trên head **72/76, rc1**, prototype scratch **76/76, rc0**. Đây là ba loại phép đo khác nhau.
- 19/19 mutant bị giết trên bản sao, không ParserError. Đếm độc lập của reviewer, không sao chép số 16 do executor khai. Ca mới có răng trong phạm vi lỗi của chúng; chưa phủ hết lớp native.
- Không có P0 mới được chứng minh. Chỉ giữ **một P1** loi-native-tang-nguoi-dung; không đếm thiếu test của chính lỗi ấy thành P2 khác. Không phát hiện P2/P3 mới có đủ chứng cứ.
- **KHÔNG ĐO ĐƯỢC**: Windows NTFS junction/effective ACL/owner/handle, icacls thật, Scheduled Task/COM/DACL/credential, msiexec, Commander, PATH/module/TEMP thật của SYSTEM/tladmin; native getter .cmd và full entry point Windows. Model ACL Linux không chứng minh các tính chất ấy. Số Windows 68/68 chỉ là khai của executor, không phải kết quả reviewer.
- Không mạng, không credential thật, không pip/npm install thật, không commit/push/merge, không sửa cay-kho/. Mọi thay đổi fixture/mutant/hint ở ngoài cây review. Snapshot đầu/cuối chỉ chứng minh không có delta quan sát được tại hai mốc, không phải chứng minh toàn lịch sử ghi tệp.

Kiểm cuối: `python3 probes/final-audit.py > evidence/final-audit.log` → rc0; HEAD vẫn 28fdbdf0e6e8ce5565b6f2317bf28b05c63e81d0, tree 099a940c2b369bb2df417ba82d153c6d64445f40; detached, shallow=false, core.abbrev=7. Status kể cả ignored rỗng; diff/index/diff --check rỗng. Ba tệp ops/vm/ khớp byte blob Git, preflight và bản sao. 19/19 mutant có ca đỏ liên quan, parser_errors=0. Chi tiết/hashes: evidence/final-readonly.json. Runtime `PSNativeCommandUseErrorActionPreference=False` và pwsh=7.6.9 (evidence/powershell-environment.log).

HINT.patch SHA256: e699e30a9bd0abd4535a42d16081dca2aca4823cee7e0907953a15784bf2c4e0. Quyết định **changes_requested** vì P1 còn được đo ở chính head; baseline xanh và ba biểu hiện cũ đóng không đủ đóng toàn lớp.
