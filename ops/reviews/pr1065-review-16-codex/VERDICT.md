verdict: approve
reviewed_sha: 210ab81c3f1af36243748458eb5e70180baeab71

Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

## ĐÓNG FINDING LƯỢT 15

| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| ghim-actionlint-khong-la-dich-chung-nhan | ĐÃ VÁ THẬT | `python3 probes/closure16.py`: control pin1.7.7/response1.7.7 → nang_cap, downloads1, native1.7.7/rc0; response9.9.9 ở cả hậu cài và giu → loi, downloads0, native giữ nguyên. Chi tiết evidence/closure16.json. |

## BẢNG SĂN

Review ngoại tuyến hoàn tất trên exact SHA; cây `cay-kho/` chỉ đọc, mọi probe sửa mã chạy trên bản sao ngoài cây.

HƯỚNG 1: mỏ neo và bản sao phép đo
  giả thuyết : HEAD khác SHA được giao hoặc có sửa sẵn khiến phép đo không đúng đối tượng.
  lệnh       : python3 (preflight lưu ở evidence/preflight16.json): git rev-parse HEAD; git status --porcelain=v1 --untracked-files=all --ignored; git rev-parse --is-shallow-repository; git config core.abbrev; git show SHA:path và SHA-256 của 5 tệp.
  output     : HEAD=210ab81c3f1af36243748458eb5e70180baeab71; tree=40a4cbe161e513f202bd4681f9713e7f04fee741; status/diff HEAD/diff index rỗng; detached=true; shallow=false; core.abbrev=7; 5/5 tệp nguồn = Git blob = copies/head.
  kết luận   : KHÔNG PHẢI LỖI. Mọi bản sao/probe/output ở ngoài cay-kho/. Reviewer Codex, provider openai_codex, model_family openai, execution_surface codex_service (API với công cụ shell), transport machine; không đăng GitHub. Model/effort cụ thể KHÔNG ĐO ĐƯỢC từ công cụ phiên này. Chỉ thị prompt.snapshot là authority trực tiếp cho review ngoại tuyến lượt 16; phạm vi ops/vm, không xét ops/land.

HƯỚNG 2: bộ test bắt buộc trên head nguyên bản
  giả thuyết : bản vá lượt 15 làm test lỗi hoặc số 115/115 không tái lập được.
  lệnh       : TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/head-tests.log 2>&1
  output     : cap-nhat-cong-cu tests: 115/115 ca QUA; rc=0.
  kết luận   : KHÔNG PHẢI LỖI trong bộ test Linux. Không dùng số VM Windows của SHA trước để chứng nhận head này. Kiểu kết quả, ca không đăng ký theo nền và sức bắt đột biến được đo riêng ở H11/H12.

HƯỚNG 3: đóng finding ghim actionlint lượt 15
  giả thuyết : HTTP trả tag khác ghim vẫn được dùng làm đích của giu/nang_cap.
  lệnh       : python3 probes/pinned-release-round15.py > evidence/pinned-historical-driver.log 2>&1; python3 probes/closure16.py > evidence/closure16.log 2>&1
  output     : driver lịch sử rc1 tại assert cũ mong nang_cap cho post-mismatch; raw pinned-post-mismatch.json cho loi. Oracle hiện hành: 3/3 PASS; control đúng ghim nang_cap/native1.7.7/rc0/downloads1; post-mismatch và keep-mismatch đều loi/downloads0/native không đổi. Mọi request đúng URL /releases/tags/v1.7.7.
  kết luận   : KHÔNG PHẢI LỖI; ĐÃ VÁ THẬT finding lượt 15. Chốt chạy trước tải và trước chứng nhận giu; bản phản hồi vẫn được dùng sau chốt nhưng đã bằng ghim theo Test-CungDinhDanh. Hash/ZIP/copy/native thật trên Linux; HTTP thay thế ngoại tuyến; không khẳng định đã đo upstream.

HƯỚNG 4: ChiKiem và prerequisite của cả hai tầng
  giả thuyết : thiếu launcher/interpreter hoặc native in token nhưng rc khác 0 vẫn được kiem/can_cap_nhat.
  lệnh       : python3 -u probes/rerun-regressions.py > evidence/regressions16.log 2>&1 (third-paths-oracle, portable-check-oracle, system-check-oracle, absence-regression-oracle)
  output     : Venv runtime oracle: 6/6 PASS; Portable ChiKiem oracle: 4/4 PASS; System ChiKiem oracle: 6/6 PASS; NLM prerequisite oracle (head): 4/4 PASS; 4 driver rc0.
  kết luận   : KHÔNG PHẢI LỖI trong tập đo. Có tệp không thay cho getter; missing/rc9/cannot-start đều loi. Nhánh thiếu LTS với Node còn đo được chỉ can_quyet_dinh, thuộc ngoại lệ. Các ZIP stub của tầng user không chứng nhận ZIP; probe portable riêng gọi hàm thật.

HƯỚNG 5: catch/continue, lỗi native và lỗi lập trình
  giả thuyết : catch mới nuốt lỗi thành ĐẠT hoặc continue làm mất các công cụ sau.
  lệnh       : python3 -u probes/rerun-regressions.py (l4-user-oracle, user-oracle, user-version-oracle, new-paths-oracle, run-main-tail); python3 probes/audit-regression-results.py
  output     : l4-user3/3, user3/3, remaining-native6/6; cả5driver rc0; independent regression26/26 PASS. Programmer-throw → exit1/ok=false/loi1/tang-NguoiDung, thông điệp Substring; system-throw → exit1/ok=false/loi1/tang-HeThong. npm biến mất và NLM status rc7 đều loi; còn dòng của công cụ sau.
  kết luận   : KHÔNG PHẢI LỖI trong tập đo. Getter catch trả null bị caller chặn; catch từng công cụ và lưới cuối ghi loi. Catch status giữ rcSt null nếu khởi chạy ném, mode null nếu JSON hỏng; finally khôi phục home. Catch encoding rỗng chỉ là console. Continue nằm sau dòng kết quả hoặc trong nhánh ChiKiem, không biến lỗi thành bo_qua; source không có Add-KetQua bo_qua.

HƯỚNG 6: băm trước chạy và hậu cài HeThong
  giả thuyết : hash/installer sai vẫn spawn/chứng nhận hoặc MSI3010 bị coi là hậu cài đã đo.
  lệnh       : python3 -u probes/rerun-regressions.py (system-matrix, caller-matrix); python3 probes/audit-old-matrices-round13.py
  output     : Independent matrix assertions: 6 system + 4 caller PASS; 12 regression drivers + 7 contract drivers rc0. Tamper/missing-hash → 4loi/0spawn/0download còn; success → 4nang_cap, 4spawn đều hash_matches=true; post-version-wrong/installer-failure → 4loi; MSI-reboot → Git nâng + 3can_khoi_dong_lai, commander restart=true.
  kết luận   : KHÔNG PHẢI LỖI về logic đã đo. Hậu getter null ở system/zip đều loi. Hash/download/file có đo thật; Start-Process/MSI/ACL/tasks ở matrix là fixture, không phải Windows thật.

HƯỚNG 7: đích pip/npm, venv kho và launcher NLM
  giả thuyết : cài rc0 nhưng dry-run/launcher cũ/đích chưa biết vẫn được giu/nang_cap.
  lệnh       : python3 -u probes/run-contracts-round12.py > evidence/contracts16.log 2>&1; python3 probes/audit-extra-regressions.py
  output     : 7/7 driver rc0; target-equality5/5, ZIP7/7, install-contract4/4, real-pip2/2 PASS; Real NLM stale launcher: REJECTED; extra assertions21/21 PASS. Pip local dry-run chưa cài ghim → loi; NLM metadata/đích0.5.0 mà CLI0.4.0 → loi; control đúng đích đạt.
  kết luận   : KHÔNG PHẢI LỖI trong phạm vi hợp đồng B. Pip thật PIP_NO_INDEX=1, wheel local do reviewer tạo; không gọi upstream. Hợp đồng venv yêu cầu Python và hai gói ghim, không suy đã xác minh mọi dependency khác trong requirements.

HƯỚNG 8: đăng ký lịch, ACL và ranh giới SYSTEM
  giả thuyết : đăng ký tiếp sau hash/ACL/reparse sai hoặc quay lại giao ACL Tools.
  lệnh       : python3 -u probes/rerun-regressions.py (registration-head); python3 probes/audit-old-matrices-round13.py
  output     : registration5/5 PASS; clean tới1task HeThong rồi chốt fixture trước credential/COM; ACL/hash-reject → 0task; symlink ancestor/child → 0icacls/0task; tool_acl_calls=0 cả5ca.
  kết luận   : KHÔNG PHẢI LỖI ở mô hình và phần đọc tĩnh. 3lệnh Invoke-Icacls đăng ký chỉ trỏ ProgramFiles/tra-luat-ops; source không tự giao C:\Tools. KHÔNG ĐO ĐƯỢC hiệu lực NTFS junction/icacls/Scheduled Task/COM/msiexec thật do môi trường Linux. Không tính các phần này thành PASS Windows.

HƯỚNG 9: đường thứ ba mới — archive có băm đúng nhưng không cài được và pin alias
  giả thuyết : archive hỏng/0 hoặc2exe có hash hợp lệ, hoặc tag không đúng định danh ghim, vẫn được chứng nhận từ rc tải/copy.
  lệnh       : python3 -u probes/zip-third16.py > evidence/zip-third16.log 2>&1
  output     : ZIP third paths:14/14 PASS; control và tag bỏ v → nang_cap/native2.0.0/rc0; null/empty/zero-alias/suffix tag và transport throw → loi/download0/copy0; digest-missing + archive-corrupt/zero-exe/two-exes → loi/copy0/native giữ1.0.0; post-rc9/empty/cannot-start → loi dù đã copy1.
  kết luận   : KHÔNG PHẢI LỖI trong các đường vừa đo. ZIP/archive thực, hash thực (kể cả archive hỏng được cấp hash đúng), version getter/so đích/Add-KetQua không giả. HTTP là fixture, Copy wrapper chỉ ghi nhận và đặt execute bit của Linux. Đây là đường archive chưa có trong các verdict cũ; không suy ra Windows Expand-Archive/NTFS đã chạy.

HƯỚNG 10: định danh đầy đủ, case, alias số học, major Node và đích null
  giả thuyết : hồi quy cắt suffix/gộp alias/case hoặc nâng major từ token không parse được.
  lệnh       : python3 -u probes/run-identities-round15.py > evidence/identities16.log 2>&1; python3 probes/identity-audit16.py > evidence/identity-audit16.log 2>&1
  output     : suffix5+CLI2, case4, numeric-system5+ZIP5, Node current4, unknown-target4 đều PASS qua assert trên raw JSON; old-blob Node1ca chỉ đối chứng riêng. 6driver lịch sử rc1 do assert mong tái hiện lỗi cũ; không che rc1, output thô lưu đủ.
  kết luận   : KHÔNG PHẢI LỖI trong tập đo. Case-equal được giu, khác case/suffix/alias SAU cài bị loi; ZIP alias TRƯỚC được cài lại đúng đích, không giu sai; Node current không parse được → loi/0installer. ZIP suffix-before ra loi do OFFLINE-UNEXPECTED-HTTP khi đi nhánh nâng, vì vậy chỉ chứng minh không giu sai; không lấy nó chứng nhận hậu cài suffix. system suffix-after và CLI suffix có so đích thật bổ sung.

## KIỂM TOÀN BỘ Add-KetQua KHÁC loi

Lệnh: `pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory16.json`; `python3 probes/contracts16.py`. Output: parse_errors=0; Add-KetQua50; khác loi19; đối chiếu19/19. Bộ lọc AST lấy MỌI CommandAst gọi Add-KetQua mà đối số HanhDong không phải literal loi, bao gồm hành động tính bằng biểu thức; không lọc chỉ theo tên giu/nang_cap, không chỉ xét diff. Helper không phát dòng thành công khác ngoài các caller dưới đây; source đã được đọc toàn bộ. A áp ChiKiem; B áp giu/nang_cap/cai_moi cùng ngoại lệ được giao.

| Dòng | Hàm / hành động | A/B | Phép đo hoặc lập luận |
| --- | --- | --- | --- |
| 366 | Update-CongCuZip / `'giu'` | A/B đạt | Get-PhienBanLenh đã đo current: rc0 + mẫu caller. Test-CungDinhDanh so toàn token/case, chỉ bỏ v/V. Với Tag có chốt361 trước giu: response bằng ghim. closure16: keep-mismatch loi/0download; control đúng ghim, ZIP target/identity kiểm giu. |
| 368 | Update-CongCuZip / `'can_cap_nhat'` | A đạt; B không áp | Chỉ ChiKiem, guard357 chặn current rỗng; portable-check4/4: missing/rc9/cannot-start đều loi, bản cũ đo được mới can_cap_nhat. Không phải chứng nhận cài. |
| 383 | Update-CongCuZip / `$(if ($truoc) { 'nang_cap' } else { 'cai_moi' })` | B đạt | Save/Assert-Bam trước copy; getter381 đòi rc0+mẫu rồi Test-CungDinhDanh382 bằng moi. Nếu ghim, moi đã bị ràng361 bằng Tag. closure16 đúng ghim nâng1.7.7; ZIP third14/14 và alias-after không được đạt. |
| 401 | Invoke-TangNguoiDung / `'giu'` | A đạt; B ngoại lệ Python | pyTruoc đo --version rc0+Python\s+(\S+), null thì loi/return400. Chỉ báo Python không nâng, ngoại lệ rõ trong chỉ thị. Native version failure3 thành loi. |
| 416 | Invoke-TangNguoiDung / `'kiem'` | A đạt | ChiKiem chỉ vào else khi metadata current có rc0 và khớp mẫu đầy đủ của Get-PhienBanGoi. Không đọc được thì415 loi; absence/new-paths kiểm trống/rác/rc6. Đích moi nhat ở pip chỉ là nhãn kiểm, không chứng nhận giu. |
| 424 | Invoke-TangNguoiDung / `$(if ($truoc -ceq $sau) { 'giu' } else { 'nang_cap' })` | B đạt | pip install rc được chụp trước getter; sau metadata rc0+mẫu và đích không rỗng. PyYAML/jsonschema = ghim; pip = pip index rc0+mẫu. -cne chứng nhận đúng token. real-pip/install-contract/unknown-target chặn rc0 nhưng chưa lên đích. |
| 433 | Invoke-TangNguoiDung / `'kiem'` | A đạt | ChiKiem đo venv python --version rc0+mẫu; null thì loi. third-paths6/6: missing/runtime rc9/cannot-start lỗi; không chỉ Test-Path. |
| 446 | Invoke-TangNguoiDung / `'giu'` | B đạt theo hợp đồng venv | Sau pip rc0 đo lại python (rc0+mẫu) và PyYAML/jsonschema (rc0+mẫu), hai metadata -cne ghim. real-pip control/dryrun + install-contract: dry-run, Python hậu rc9, lệch ghim đều loi. Không chứng nhận mọi dependency ngoài hai ghim. |
| 458 | Invoke-TangNguoiDung / `'kiem'` | A đạt | ChiKiem cần current CLI do getter đo rc0+mẫu caller và npm tồn tại; null thì loi. user-version/check-missing-cli đo cả2CLI, giữ đủ dòng các công cụ sau. |
| 467 | Invoke-TangNguoiDung / `$(if ($truoc -ceq $sau) { 'giu' } elseif ($truoc) { 'nang_cap' } else { 'cai_moi' })` | B đạt | npm install rc0; đo CLI SAU qua getter rc0+mẫu giữ suffix; npm view version rc0+mẫu. -cne so đầy đủ, case-sensitive. case-equal giu, case-different/suffix/đích null/rác/rc9 loi; target-equality5/5. |
| 485 | Invoke-TangNguoiDung / `'kiem'` | A đạt | ChiKiem: nlmPy phải tồn tại, nlm getter rc0+nlm version\s+(\S+) khác rỗng mới kiem. NLM prerequisite4/4 và lỗi native rc9 đều loi. |
| 507 | Invoke-TangNguoiDung / `$(if ($truoc -ceq $sau) { 'giu' } else { 'nang_cap' })` | B đạt | pip rc0, nlm CLI SAU rc0+mẫu, metadata gói rc0+mẫu, pip index đích rc0+mẫu; cả CLI+metadata -cne đích. Thêm status rc0+JSON+mode=file. Real-NLM stale CLI0.4/metadata+đích0.5 bị loi; finally khôi phục env. |
| 544 | Invoke-TangHeThong / `'can_quyet_dinh'` | A đạt; B ngoại lệ quyết định | ChiKiem chặn current rỗng533 và Test-CoTheCai534 chặn token không parse được. current đo được mới thông báo có LTS major mới; không phải giu/nang_cap. Node current4ca chứng minh suffix/build/rác không cài. |
| 546 | Invoke-TangHeThong / `'can_quyet_dinh'` | A đạt; B ngoại lệ quyết định | Không LTS cùng major thì can_quyet_dinh, không chứng nhận cài. Nếu ChiKiem current đã đo ở532/533, nên A thoả. system-check no-lts:4native rc0, node chỉ báo quyết định. |
| 560 | Invoke-TangHeThong / `'giu'` | A/B đạt | Current getter532 đòi rc0+mẫu và Test-CoTheCai hợp lệ; đích lấy HTTP/index. Test-CungDinhDanh560 chứng nhận bằng token/case. numeric/git-alias-before không được giu sai; stable4/4 giu, cao hơn đích loi561. |
| 562 | Invoke-TangHeThong / `'can_cap_nhat'` | A đạt; B không áp | Chỉ ChiKiem sau guard533/534; current đo được mới can_cap_nhat. system-check6/6: missing/rác/rc9/cannot-start đều loi; không có installer. |
| 576 | Invoke-TangHeThong / `'can_khoi_dong_lai'` | A không tới; B ngoại lệ MSI3010 | Chỉ cài thật; Install-Msi516 trả can_khoi_dong_lai riêng khi ExitCode3010, tiếp tục trước chứng nhận phiên bản. system-matrix msi-reboot đo logic này bằng fixture; Windows msiexec thật KHÔNG ĐO ĐƯỢC. |
| 578 | Invoke-TangHeThong / `$(if ($truoc) { 'nang_cap' } else { 'cai_moi' })` | B đạt | Sau Save/Assert-Bam và installer thành công, getter575 đo SAU rc0+mẫu rồi Test-CungDinhDanh577 phải bằng đích. suffix-after/numeric/git-marker-after loi; control 4nang_cap. Post-rc9/empty/cannot-start driver bổ sung kiểm riêng. |
| 590 | Invoke-TangHeThong / `'khoi_dong_lai'` | Ngoài chứng nhận phiên bản B; A không tới | khoi_dong_lai là task Running, không phải giu/nang_cap/cai_moi. Script DaCaiNode khởi tạo false59, chỉ bật568 khi cài thật; ChiKiem không bật, không tới restart. system-matrix kiểm recovery cả khi Node MSI hỏng; task Windows thật chưa đo. |

Không có phản chứng A/B còn mở trong phạm vi đã đo/phân tích tĩnh; hai điểm ZIP ghim366/383 nay dùng đích bị ràng bằng Tag trước chứng nhận. Không biến kết luận logic thành bằng chứng Windows native.

HƯỚNG 11: không đếm skip là PASS; try/catch mới và argv native
  giả thuyết : Ca chấp nhận mảng truthy, thiếu nền/dependency vẫn tính QUA hoặc pinned helper diễn sẵn kết quả.
  lệnh       : python3 probes/test-accounting-round12.py; TL_TEST_PYTHON=python3 REVIEW_CASE_LOG=$PWD/evidence/cases16.jsonl pwsh/pwsh -NoProfile -File copies/accounting/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/accounting16.log 2>&1; pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory16.json; pwsh/pwsh -NoProfile -File probes/icacls-round15.ps1 > evidence/icacls16.json; python3 probes/accounting-audit16.py
  output     : 115/115/rc0; 115tên duy nhất, tất cả System.Boolean true; AST119tên duy nhất; 4ca Windows không đăng ký trên Linux: admin_ca_ma_thoat_3_khong_do_duoc, dang_ky_lich_khong_admin_thoat_3, he_thong_khong_admin_thoat_3, sai_may_thoat_5_truoc_moi_thay_doi. icacls fixture5/5: argv roundtrip cả4lần, rc0 không ném, rc1/5 ném, rc1332 cấu hình bị POSIX thu thành52 vẫn ném; mất binary tuyệt đối cũng ném. Diff sản phẩm c489c72..head chỉ thêm2dòng guard/comment, không thêm try/catch.
  kết luận   : KHÔNG PHẢI LỖI trong phép đo. Nhánh Windows admin không đo mã3 trả false; các nhánh chỉ chạy trên Linux không được đếm trên Windows. Pinned helper chỉ thay HTTP+execute bit Linux; version/hash/archive/copy thực, control đòi native2.0.0/rc0/download1, 2negative đòi loi. Getter/caller không bị giả. Không tính4ca vắng vào115ca và không dùng rc1332 cấu hình làm kết quả native Windows.

HƯỚNG 13: chạy lại probe hậu cài native lượt 15
  giả thuyết : rc0 installer che native hỏng chỉ SAU khi cài.
  lệnh       : python3 -u probes/new-third-paths-round15.py > evidence/system-post16.log 2>&1
  output     : New post-install native failures: 4/4 PASS; control nâng4công cụ; post-rc9/post-empty/post-cannot-start đều exit1/ok=false/4loi. Mỗi ca có4installer, hash tại spawn đúng,4marker và phép gọi native độc lập sau cài xác nhận lỗi.
  kết luận   : KHÔNG PHẢI LỖI. Chỉ sửa đích ghi note của bản sao driver thành evidence/legacy-verdict-discard.md để không chép verdict lịch sử; logic probe và sản phẩm giữ nguyên. Native/file thật trên Linux; MSI/ACL/task/HTTP là fixture ngoại tuyến.

HƯỚNG 12: test có răng — hồi quy ACL/native/ChiKiem và chốt pin mới
  giả thuyết : 115ca chỉ diễn output lành, bỏ guard vẫn xanh.
  lệnh       : python3 -u probes/review14-mutations.py > evidence/mutations16.log 2>&1; python3 -u probes/more-mutants16.py > evidence/more-mutants16.log 2>&1
  output     : Review14 mutations17/17 KILLED; Additional mutations23/23 KILLED. Mỗi mutant rc1, có tên ca DO, không ParserError. Bỏ riêng chốt tag → 113/115, đỏ đúng2ca zip_ghim_response_tag_lech_khong_duoc_nang_cap_dat và zip_ghim_response_tag_lech_khong_duoc_giu_dat.
  kết luận   : KHÔNG PHẢI LỖI về sức bắt trong 40đột biến độc lập đã đo tại head này. Các mẫu anchor cũ được tái dẫn xuất trên source hiện hành, 14mutant đăng ký dùng mô hình ACL giữ trạng thái; 5guard ChiKiem,3catch/native và chốt pin cùng17mutant định danh/hậu điều không sống sót. Đây là tập reviewer tự dựng và lưu từng patch/log, không tự nhận là trùng toàn bộ danh sách 40của executor.

## ÁNH XẠ PROBE LƯỢT 4–15 VÀ GIỚI HẠN TÁI CHẠY

Lệnh: `python3 probes/replay-map16.py`; output: 12/12 nhóm lượt có driver hành vi được tái chạy, danh sách và băm driver ở evidence/replay-map16.json. Dùng các bản driver tích luỹ ở luot15/probes, đã reroot vào copies/head; các getter/caller/main-tail lấy từ head hiện hành. Không chạy utility build-HINT/finalize-verdict lịch sử hay oracle hardcode SHA/số test cũ để chứng nhận head mới. Các kiểm tương ứng được thay bằng preflight16/accounting115/inventory119/final-audit16. Không sửa oracle lịch sử để che assertion đỏ; H3/H10 giải thích rc1 và có assert độc lập trên JSON.

| Lượt | Nhóm được chạy lại | Driver chính |
| --- | --- | --- |
| 4 | Native user, HeThong hash/MSI/recovery, register/ACL | `probes/l4-user-oracle.py`, `probes/system-matrix.py`, `probes/registration-head.py`, `probes/icacls-round15.ps1` |
| 5 | Getter rc và CLI/Python version failure | `probes/user-version-oracle.py`, `probes/run-user-extra.py` |
| 6 | Metadata rc và các nhánh native còn lại | `probes/new-paths-oracle.py`, `probes/caller-matrix.py` |
| 7 | Venv/NLM thiếu prerequisite, metadata phục hồi | `probes/absence-oracle.py`, `probes/absence-regression-oracle.py` |
| 8 | ChiKiem chung ở user/portable/system | `probes/third-paths-oracle.py`, `probes/portable-check-oracle.py`, `probes/system-check-oracle.py` |
| 9 | Hậu cài venv/ghim, pip thật offline, launcher | `probes/install-contract-oracle.py`, `probes/real-pip-oracle.py`, `probes/real-nlm-oracle.py` |
| 10 | Đích mới nhất, không giu bản cao hơn, NLM CLI | `probes/target-equality-oracle.py`, `probes/zip-target-oracle.py` |
| 11 | Định danh đầy đủ/suffix và parser | `probes/version-identity-oracle.py`, `probes/cli-version-identity-oracle.py` |
| 12 | Case và Node current không parse được | `probes/cli-case-identity-oracle.py`, `probes/node-major-oracle.py` |
| 13 | Định danh số học/Git .windows. trước/sau | `probes/numeric-identity-oracle.py`, `probes/zip-numeric-identity-oracle.py` |
| 14 | Hậu cài HeThong fixture có trạng thái + mutation | `probes/post-observations-round15.py`, `probes/review14-mutations.py` |
| 15 | Pin mismatch, native chỉ hỏng sau cài | `probes/pinned-release-round15.py`, `probes/new-third-paths-round15.py` |

Mô hình ngoại tuyến đo logic điều phối và phiên bản; chỉ interpreter/native fixture/file/hash/archive/local-pip là thật tại Linux. Không đo NTFS effective ACL/owner/race, Scheduled Task thật, COM, msiexec hoặc luồng NguoiDung thật trên Windows tại SHA này. Các phần đó là KHÔNG ĐO ĐƯỢC, không phải PASS. Review không suy tính an toàn của TEMP/PATH/PSModulePath/ProgramFiles trên VM từ một fixture do reviewer tự tạo.

HƯỚNG 14: đối chứng hậu cài có trạng thái và kiểm tĩnh toàn phạm vi
  giả thuyết : ca hậu cài vẫn dùng output trước cài hoặc giả hash/phiên bản để diễn kết quả.
  lệnh       : python3 -u probes/post-observations-round15.py > evidence/post-observations16.log 2>&1; pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source16.log
  output     : Post identity stateful observations: 6/6 PASS; head từ chối zero/Git-marker alias, mutant chấp nhận; mỗi ca có4installer,4marker và4native rc0. source parse_errors=0; pwsh7.6.9; Ubuntu24.04.5; README_native_acl_commands=0.
  kết luận   : KHÔNG PHẢI LỖI trên head; suite không chỉ đo output hardcode trước installer. Toàn ops/vm có3tệp, đã đọc sản phẩm/test/README; không có lời gọi Add-KetQua qua alias/dynamic wrapper bị sót ngoài50lệnh AST. Model installer tạo marker rồi binary tự đổi output, hash được kiểm trước spawn; không gọi installer Windows thật.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Finding duy nhất lượt15: `ghim-actionlint-khong-la-dich-chung-nhan` → **ĐÃ VÁ THẬT** tại SHA hiện hành. Có3phép đo control/post-mismatch/keep-mismatch,4biên tag malformed/alias, và mutant bỏ chốt làm đỏ đúng2ca. Lớp thiếu ràng buộc ghim không còn biểu hiện mở ở2cửa ZIP giu/hậu cài; không phát sinh lớp finding mới từ các phép đo đã làm. Bảng đóng finding đầu tệp và H3/H9/H12 lưu lệnh/output.

HƯỚNG 15: kiểm cuối SHA/cây/artifact và tính toàn vẹn phép đo
  giả thuyết : nguồn đổi sau đo, mutant trùng nhau, dữ liệu hiện hành bị trộn SHA hoặc verdict thiếu bảng chứng nhận.
  lệnh       : python3 probes/final-audit16.py > evidence/final-audit16.log 2>&1
  output     : exact HEAD=210ab81c3f1af36243748458eb5e70180baeab71; tree=40a4cbe161e513f202bd4681f9713e7f04fee741; Git status kể cả ignored rỗng; diff HEAD/index/diff --check rỗng; detached/full-history/core.abbrev7;5/5tệp source=Git blob=copies/head và khớp băm preflight; PROMPT=prompt.snapshot;115/115,115Booleantrue;40mutant khác byte,40/40bị bắt;19/19Add khác loi; pin3/3,ZIP mới14/14,post-native4/4,stateful6/6.
  kết luận   : KHÔNG PHẢI LỖI về mỏ neo và artifact. Snapshot sạch chỉ chứng minh không có delta tại hai mốc, không chứng minh không từng ghi rồi hoàn nguyên; các thao tác thực hiện trên cây nguồn chỉ đọc, mọi phép sửa chạy ngoài cay-kho/. Không push/merge/gọi mạng, không review ops/land. Windows native tại SHA này KHÔNG ĐO ĐƯỢC, không dùng71/71 hoặc11/11 ở SHA cũ làm chứng nhận mới.

Không có finding P0/P1/P2/P3 còn mở trong phạm vi đã đo/phân tích tĩnh. **approve** tại `210ab81c3f1af36243748458eb5e70180baeab71`: finding lượt15 đã đóng; bộ bắt buộc115/115/rc0; hợp đồng A/B kiểm đủ19/19điểm;40/40đột biến bị bắt. Không cần HINT.patch mới. Bằng chứng không bao gồm chạy Windows native tại head này.
