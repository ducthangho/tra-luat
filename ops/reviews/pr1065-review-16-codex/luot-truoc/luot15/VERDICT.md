verdict: changes_requested
reviewed_sha: c489c722db43623f1d9b2250420edce0005a96d5
Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

## ĐÓNG FINDING LƯỢT 14
| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| test-thieu-duong-tich-hop [P2] | **Đã đóng** | `python3 -u probes/review14-mutations.py` + `python3 probes/post-observations-round15.py`: baseline112/112/rc0; áp đúng patch L14, mutant HeThong110/112/rc1, đỏ đúng2ca alias; ZIP tương ứng110/112/rc1;17/17mutant bị giết,6/6quan sát stateful. Xem H12 và `evidence/closure-round14.json`. |

## BẢNG SĂN

Bằng chứng được nối theo thứ tự hoàn tất từng hướng. Reviewer không sửa `cay-kho/`, không gọi mạng; mọi phép đo bổ sung và đột biến sẽ chạy trên bản sao.

HƯỚNG 1: exact SHA, bản sao và nguồn gốc test-only
  giả thuyết : đo nhầm nguồn hoặc hint không được áp nguyên văn.
  lệnh       : python3 (preflight: so Git blob với năm tệp nguồn/bản sao; patch -p0 --batch -i luot14/HINT.patch trên test f3231c8).
  output     : {"head": "c489c722db43623f1d9b2250420edce0005a96d5", "tree": "156f174533a899299bc1e4dd927366c7b63e83c0", "status": "", "shallow": "false", "abbrev": "7", "files": {"ops/vm/cap-nhat-cong-cu.ps1": "8516e075f06c300d36fdd7e105e930f1d669e465fa714cf16ecff0de5c8d758b", "ops/vm/cap-nhat-cong-cu_test.ps1": "0dbd1e3c50ec3e8432e392edeb14b4ebe4f3bcb7c0a30fd76ca59d1f1796263c", "ops/vm/README.md": "e450ff93992576a31b622ce6474c7158ba05f8fdf83c8f8e8267d80fdc95bb6e", "ops/cong_cu.yaml": "71631bb6baf532deeb4847c5ff9c407a50bfdb4fc503621913eb42c719ee92fb", "requirements.txt": "97733a880d95f8a900f39af2bcd1a59a3ecb357dfc928c01c7a06636b1b07657"}, "product_same_as_round14": true, "exact_hint_reapplication": true, "hint_apply_output": "patching file ops/vm/cap-nhat-cong-cu_test.ps1", "probe_source": "copied luot14/probes, paths resolve against current root", "reviewer": "OpenAI Codex; local shell tool execution on Linux; machine transport"}
  kết luận   : KHÔNG PHẢI LỖI; năm tệp khớp byte, mã sản phẩm không đổi; áp lại HINT L14 trên đúng base tạo test trùng byte head. Không sửa cay-kho/, không mạng. Chỉ thị người dùng hiện hành là authority cho review ngoại tuyến này; không suy review thành quyền merge/land.

HƯỚNG 2: bộ test bắt buộc tại exact head
  giả thuyết : bản vá test-only gây hồi quy hoặc đếm sai ca Linux.
  lệnh       : TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1
  output     : cap-nhat-cong-cu tests: 112/112 ca QUA; rc=0.
  kết luận   : KHÔNG PHẢI LỖI trong bộ Linux. Chưa chứng nhận các ca Windows hoặc con số executor khai. Sẽ kiểm riêng kiểu dữ liệu từng kết quả và nhánh điều kiện của ca test.

HƯỚNG 3: ChiKiem và prerequisite trên cả hai tầng
  giả thuyết : tệp tồn tại nhưng không chạy/rc9, hoặc thiếu prerequisite vẫn khác loi.
  lệnh       : python3 -u probes/rerun-regressions.py > evidence/regressions-round15.log 2>&1 (nhóm 1: third-paths-oracle, portable-check-oracle, system-check-oracle, absence-regression-oracle)
  output     : Venv runtime oracle: 6/6 PASS; Portable ChiKiem oracle: 4/4 PASS; System ChiKiem oracle: 6/6 PASS; NLM prerequisite oracle (head): 4/4 PASS; cả4driver rc0.
  kết luận   : KHÔNG PHẢI LỖI trong tập đã đo; native/file/rc thật, HTTP/installer/ZIP ở một số ca được mô hình riêng. Không suy thành kết quả Windows.

HƯỚNG 4: lỗi native, catch/continue và lưới nhật ký
  giả thuyết : lỗi một công cụ hoặc lỗi lập trình bị nuốt thành ĐẠT/bỏ qua.
  lệnh       : python3 -u probes/rerun-regressions.py (nhóm 2: l4-user-oracle,user-oracle,user-version-oracle,new-paths-oracle,run-main-tail)
  output     : l4-user-oracle: rc0; user-oracle: rc0; user-version-oracle: rc0; new-paths-oracle: rc0; run-main-tail: rc0. Programmer-throw tạo JSON: exit1/ok=false/loi1/tang-NguoiDung; các lỗi npm/NLM vẫn chạy tiếp công cụ sau.
  kết luận   : KHÔNG PHẢI LỖI trong tập đã đo. Catch lỗi lập trình ghi loi cùng thông điệp; continue chỉ kết thúc công cụ hiện tại sau khi ghi kết quả. Không có hành động bo_qua trong source.

HƯỚNG 5: băm và hậu cài HeThong, fail-close từng công cụ
  giả thuyết : payload sai băm/installer hỏng/hậu sai vẫn ĐẠT; driver rc0 chỉ có JSON mà không assert nội dung.
  lệnh       : python3 -u probes/rerun-regressions.py (system-matrix,caller-matrix); python3 probes/audit-regression-results.py; python3 probes/audit-old-matrices-round13.py
  output     : 6system +4caller PASS; 26/26 independent regression assertions PASS. Tamper/missing-hash:4loi/0spawn/0tệp còn; success:4nang_cap/4spawn băm đúng; hậu sai/installer1603:4loi; MSI3010:Git nâng+3can_khoi_dong_lai. Post getter null không được chứng nhận.
  kết luận   : KHÔNG PHẢI LỖI về logic đã đo. Installer/ACL/tasks/version ở matrix là mô hình; không đo NTFS/MSI Windows thật.

HƯỚNG 6: đăng ký lịch, reparse và giới hạn quyền SYSTEM
  giả thuyết : bước đăng ký lại giao ACL Tools hoặc tiếp tục tạo task sau ACL/hash/reparse sai.
  lệnh       : python3 -u probes/rerun-regressions.py (registration-head); pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source-audit.log
  output     : registration5/5: clean tới đúng điểm dừng trước credential/COM (1task HeThong); ACL/hash sai=>0task; symlink tổ tiên/con=>0icacls/0task. tool_acl_calls=0 cả5ca. Source parse_errors=0; README_native_acl_commands=0.
  kết luận   : KHÔNG PHẢI LỖI trong mô hình và phân tích tĩnh. Ba Invoke-Icacls đăng ký chỉ hướng ProgramFiles/tra-luat-ops; Save-CoKiemBam gọi Assert-Bam trước mọi spawn. KHÔNG ĐO ĐƯỢC NTFS junction/effective icacls/ScheduledTask COM/credential/msiexec trên Windows; không tính PASS.

HƯỚNG 7: đích cài, venv và launcher NLM
  giả thuyết : pip/npm rc0 nhưng chưa cài đúng đích, dry-run hoặc launcher cũ vẫn ĐẠT.
  lệnh       : python3 -u probes/run-contracts-round12.py > evidence/contracts-round15.log 2>&1; python3 probes/audit-extra-regressions.py
  output     : target-equality-oracle:rc0; zip-target-oracle:rc0; install-contract-oracle:rc0; real-pip-oracle:rc0; real-nlm-oracle:rc0; absence-oracle:rc0; run-user-extra:rc0. Target5/5, ZIP7/7, install-contract4/4, real-pip2/2;21/21 independent extra assertions PASS. NLM metadata/đích0.5.0 nhưng CLI0.4.0=>loi; control CLI0.5.0 đạt.
  kết luận   : KHÔNG PHẢI LỖI trong hợp đồng đã đo. Pip thật chỉ chạy PIP_NO_INDEX=1 với wheel local tự tạo; không gọi upstream/không cài gói mạng. Không dùng stub ZIP để chứng nhận ZIP; đã có ZIP oracle riêng.

HƯỚNG 8: định danh đầy đủ, hoa thường, major Node và đích không đọc được
  giả thuyết : các sửa lượt11–13 lại cắt suffix, gộp alias hoặc cho current không parse được tự nâng major.
  lệnh       : python3 -u probes/run-identities-round15.py > evidence/identities-round15.log 2>&1; python3 probes/audit-completed-round15.py
  output     : {"numeric_identity": "10/10 PASS", "suffix_identity": "7/7 PASS", "case_identity": "4/4 PASS", "node_major": "5/5 PASS (4 current head + 1 explicitly old Git blob A/B)", "unknown_target": "4/4 PASS"}. Sáu driver lịch sử rc1 ở assert còn tái hiện lỗi; raw JSON đủ ca được assert lại theo A/B hiện hành. Unknown-target driver rc0.
  kết luận   : KHÔNG PHẢI LỖI trong dữ liệu đã đo; không lấy rc1 lịch sử làm lỗi head, không sửa raw output cho xanh. Suffix/alias/case khác đích bị loi; control đạt. Node old Git blob được gắn nhãn riêng, không gán hành vi đó cho reviewed_sha.

HƯỚNG 10: test có đo thật, nhánh bỏ qua và try/catch mới
  giả thuyết : test trả mảng truthy hoặc không đo được vẫn đếm ĐẠT; try mới diễn sẵn kết quả.
  lệnh       : python3 probes/test-accounting-round12.py; TL_TEST_PYTHON=python3 REVIEW_CASE_LOG=$PWD/evidence/cases.jsonl pwsh/pwsh -NoProfile -File copies/accounting/ops/vm/cap-nhat-cong-cu_test.ps1; pwsh/pwsh -NoProfile -File probes/inventory.ps1
  output     : 112/112 QUA/rc0;112tên duy nhất,112kết quả System.Boolean true;AST116tên/116duy nhất;4ca không đăng ký trên Linux: admin_ca_ma_thoat_3_khong_do_duoc, dang_ky_lich_khong_admin_thoat_3, he_thong_khong_admin_thoat_3, sai_may_thoat_5_truoc_moi_thay_doi. Diff f3231c8..head chỉ thêm helper test+3ca, không thêm try/catch sản phẩm.
  kết luận   : KHÔNG PHẢI LỖI xanh giả trong phép đo này. Ca admin không đo mã3 trả false, không trả true. Test mới chỉ thay output khi installer tạo marker sau kiểm hash; yêu cầu4lần cài và đo native sau cài. Getter catch trả null rồi bị guard; catch từng công cụ/main ghi loi; catch encoding chỉ trang trí console. Không tính ca Windows vắng vào112ca.

HƯỚNG 11: đường thứ ba — đích ghim bị thay bằng tag trong phản hồi
  giả thuyết : với actionlint, phiên bản được chứng nhận dùng tag_name của HTTP thay vì ghim bản kê, thiếu điều kiện nhất quán giữa hai nguồn.
  lệnh       : python3 -u probes/pinned-release-round15.py > evidence/pinned-release-round15.log 2>&1
  output     : control: ghim1.7.7/responsev1.7.7/native1.7.7=>nang_cap; post-mismatch: URL /releases/tags/v1.7.7 nhưng đồ giả responsev9.9.9, asset vẫn đúng tên actionlint_1.7.7_windows_amd64.zip, ZIP có SHA256 đúng và native sau9.9.9/rc0=>nang_cap; keep-mismatch: native trước9.9.9/rc0=>giu,0download. Cả hai sau khác ghim. Harness rc0, ghi đầy đủ response/native/rows trong evidence/pinned-release-round15.json.
  kết luận   : LỖI P2 về thiếu điều kiện chứng nhận ghim theo B. Phân tích tĩnh chắc chắn: :361 gán moi từ rel.tag_name cho cả có Tag; :364 và :380 so với moi ấy, không so ghim. Đây là phản chứng metadata HTTP KHÔNG NHẤT QUÁN được bơm ngoại tuyến, không phải quan sát API GitHub thật hay lỗi VM thật. Chưa có bằng chứng dịch vụ thật trả sai quan hệ URL/tag nên không nâng thành P1/P0. Đang đo A/B gợi ý từ chối tag lệch trước khi giu/tải.

## KIỂM TOÀN BỘ Add-KetQua KHÁC loi

Lệnh: `pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory.json`; `python3 probes/contract-table-round15.py`. Output: parse_errors=0, Add-KetQua50, khác loi19; kiểm19/19. A áp mọi dòng ChiKiem, B áp giu/nang_cap/cai_moi cùng ngoại lệ được giao. Mẫu/rc ở getter, đích và phép so ở caller được kiểm riêng; không chỉ liệt kê test cũ.

| Dòng | Hàm / hành động | Kết luận A/B | Phép đo hoặc lập luận |
| --- | --- | --- | --- |
| 364 | Update-CongCuZip / 'giu' | A đạt; B thiếu chốt ghim P2 | Get-PhienBanLenh đo current rc0 + mẫu; Test-CungDinhDanh so token đầy đủ, phân biệt case, chỉ bỏ v/V. ZIP oracle L13 giữ định danh đầy đủ. Nhưng moi lấy từ rel.tag_name thay vì Tag: pinned-release keep-mismatch ghim1.7.7/response9.9.9/native9.9.9 vẫn giu. Thiếu điều kiện B khi response mâu thuẫn ghim; P2 mới, không phải lỗi VM/API thật đã đo. |
| 366 | Update-CongCuZip / 'can_cap_nhat' | A đạt; B không áp | Chỉ ChiKiem; guard358 loại truoc rỗng. portable-check4/4: missing/rc9/cannot-start đều loi; current đo được mới can_cap_nhat; không installer. |
| 381 | Update-CongCuZip / $(if ($truoc) { 'nang_cap' } else { 'cai_moi' }) | B thiếu chốt ghim P2 | Sau copy đo getter rc0 + mẫu và Test-CungDinhDanh380; ZIP alias-after bị loi; zip-target7/7 đúng trong trường hợp response khớp Tag. Pinned-release post-mismatch: ZIP có băm đúng, native9.9.9/rc0 được nang_cap dù ghim1.7.7, vì so với response9.9.9. Cần chốt Tag/ghim độc lập. |
| 399 | Invoke-TangNguoiDung / 'giu' | A đạt; B ngoại lệ Python | pyTruoc đo rc0 + Python\s+(\S+); null thì loi/return398. Python chỉ báo, không nâng theo ngoại lệ được giao. check-python native lỗi thành loi. |
| 414 | Invoke-TangNguoiDung / 'kiem' | A đạt | Chỉ ChiKiem; Get-PhienBanGoi yêu cầu rc0 + mẫu toàn token, null=>loi413. absence9mode và new-paths6/6: metadata rỗng/rác/rc6 đều loi. |
| 422 | Invoke-TangNguoiDung / $(if ($truoc -ceq $sau) { 'giu' } else { 'nang_cap' }) | B đạt | Pip install rc0; metadata SAU rc0 + mẫu, đích pip từ pip index rc0 + mẫu hoặc ghim PyYAML/jsonschema; -cne buộc cùng token. Empty/garbage/rc9 target đều loi; real-pip local và install-contract có kiểm hậu điều. |
| 431 | Invoke-TangNguoiDung / 'kiem' | A đạt | ChiKiem đo interpreter venv; null=>loi. third-paths6/6 kiểm missing/native rc9/cannot-start; không lấy tệp tồn tại làm phiên bản. |
| 444 | Invoke-TangNguoiDung / 'giu' | B đạt theo hợp đồng venv | Sau pip rc0 đo Python + hai metadata gói, -cne với ghim. install-contract4/4 và real-pip2/2: dry-run chưa cài, interpreter sau rc9, ghim lệch đều loi. Không suy đã kiểm mọi dependency khác của requirements. |
| 456 | Invoke-TangNguoiDung / 'kiem' | A đạt | ChiKiem còn npm prerequisite; truoc getter rc0 + mẫu đầy đủ, null=>loi. CLI version-failure/missing/metadata oracle giữ11dòng và ghi loi đúng công cụ. |
| 465 | Invoke-TangNguoiDung / $(if ($truoc -ceq $sau) { 'giu' } elseif ($truoc) { 'nang_cap' } else { 'cai_moi' }) | B đạt | npm install rc0; CLI SAU getter rc0 + suffix; npm view rc0 + mẫu; -cne so toàn token. CLI suffix/case-different đều loi; case-equal giu. Unknown target4/4 chặn output trống/rác/rc9. |
| 483 | Invoke-TangNguoiDung / 'kiem' | A đạt | nlmPy phải có; truoc nlm --version getter rc0 + mẫu, null=>loi. NLM prerequisite4/4, user-version và absence kiểm missing launcher/python/venv và rc9. |
| 505 | Invoke-TangNguoiDung / $(if ($truoc -ceq $sau) { 'giu' } else { 'nang_cap' }) | B đạt | Pip rc0; CLI SAU getter rc0 + mẫu; metadata gói và CLI cùng -cne đích pip index rc0. Status rc0 + JSON mode=file; catch status không đặt rcSt thành0, finally khôi phục home. Real-NLM launcher cũ bị từ chối. |
| 542 | Invoke-TangHeThong / 'can_quyet_dinh' | A đạt; B ngoại lệ quyết định | ChiKiem đã chặn current null531 và guard parser; Node5/5: suffix/build/rác loi trước installer, stable24.1.0 mới được can_quyet_dinh major26. |
| 544 | Invoke-TangHeThong / 'can_quyet_dinh' | A đạt; B ngoại lệ quyết định | Nếu ChiKiem thì current đã đo ở531; không có LTS cùng major chỉ xin quyết định, không là giu/nang_cap/cai_moi. system-check no-lts đo native rc0 cho4binary. |
| 558 | Invoke-TangHeThong / 'giu' | A/B đạt | Current getter rc0 + mẫu và Test-CoTheCai; Test-CungDinhDanh đảm bảo bằng token đích HTTP/index. L13 git-alias-before và numeric-alias-before đều bị chặn; stable4/4 giu. |
| 560 | Invoke-TangHeThong / 'can_cap_nhat' | A đạt; B không áp | Chỉ ChiKiem sau guard current. system-check6/6: missing/rác/rc9/cannot-start đều loi, bản cũ đọc được mới can_cap_nhat; không cài. |
| 574 | Invoke-TangHeThong / 'can_khoi_dong_lai' | A không tới; B ngoại lệ MSI3010 | Chỉ cài thật; Install-Msi trả can_khoi_dong_lai duy nhất khi msiexec ExitCode3010. system-matrix msi-reboot mô phỏng git nâng +3MSI reboot. Windows MSI thật chưa đo. |
| 576 | Invoke-TangHeThong / $(if ($truoc) { 'nang_cap' } else { 'cai_moi' }) | B đạt; khóa test lượt14 đã đóng | Sau installer/hash đo getter rc0 + mẫu rồi Test-CungDinhDanh575. Numeric/Git alias-after đều loi trên head; control nâng đúng đích. Native stateful6/6 quan sát: head từ chối alias, mutant nhận. Bộ test hiện có3ca hậu cài được thêm đúng HINT14; full mutant110/112/rc1 đỏ đúng2ca alias (H12); P2 test-thieu-duong-tich-hop đã đóng. |
| 588 | Invoke-TangHeThong / 'khoi_dong_lai' | Ngoài B; A không tới | khoi_dong_lai báo task Running, không chứng nhận phiên bản gói. DaCaiNode chỉ bật ở cài thật; invocation script ChiKiem khởi tạo false và không tới. system-matrix xác nhận restart khi đã thử installer kể cả cài lỗi; task thật Windows chưa đo. |

A được chặn đủ ở19vị trí; B còn một P2 thiếu ràng buộc ghim actionlint khi response HTTP mâu thuẫn Tag, ảnh hưởng2điểm ZIP364/381. Các vị trí khác có guard hoặc ngoại lệ được giao. Các HTTP/npm/installer/task/ACL fixture chỉ chứng minh logic; không chứng nhận VM Windows thật.

HƯỚNG 9: đường thứ ba — native chỉ hỏng SAU installer thành công
  giả thuyết : rc0 của installer hoặc phiên bản trước còn sót làm hậu cài HeThong được ĐẠT dù getter sau cài thất bại.
  lệnh       : python3 -u probes/new-third-paths-round15.py > evidence/new-third-paths-round15.log 2>&1
  output     : New post-install native failures: 4/4 PASS; control exit0/4nang_cap; post-rc9 (in đúng token nhưng rc9), post-empty (rc0), post-cannot-start (tệp còn nhưng chmod -x) đều exit1/ok=false/4loi. Mỗi ca có4installer, băm đo lại tại spawn đều đúng,4marker; đo trực tiếp ngoài sản phẩm xác nhận lỗi hậu cài.
  kết luận   : KHÔNG PHẢI LỖI ở đường mới đã đo. Getter/so đích/main-tail sản phẩm nguyên byte; lỗi được kích hoạt bởi installer marker, không giả Add-KetQua. HTTP/ACL/MSI/tasks là mô hình ngoại tuyến; native/file/rc là thật trên Linux, không chứng nhận Windows.

HƯỚNG 13: kiểm chứng gợi ý vá ghim bằng A/B và patch tái áp
  giả thuyết : test mới chỉ đỏ do fixture/lập trình hoặc gợi ý phá các trường hợp lành.
  lệnh       : python3 probes/build-hint-round15.py; TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File copies/hint-tests-only/ops/vm/cap-nhat-cong-cu_test.ps1; cùng lệnh cho hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1; python3 probes/validate-hint-round15.py
  output     : head+test113/115/rc1, chỉ zip_ghim_response_tag_lech_khong_duoc_nang_cap_dat và zip_ghim_response_tag_lech_khong_duoc_giu_dat đỏ, control xanh; prototype115/115/rc0. Probe độc lập với ghim thật1.7.7 trên prototype3/3, hai response lệch đều loi/0download. patch -p0 dry-run0/apply0, hai tệp trùng byte bản đã test.
  kết luận   : LỖI P2 có remediation kiểm chứng. HINT.patch là dữ liệu gợi ý, chỉ áp vào bản sao ngoài cay-kho/, không phải commit/vá lên cây Executor. Test HTTP cố ý mâu thuẫn pin nên chỉ chứng minh điều kiện fail-close/nguồn đích; không chứng minh API upstream thực tế sai.

HƯỚNG 12: đóng finding lượt14 bằng đột biến nguyên văn và quan sát độc lập
  giả thuyết : ba test mới vẫn không tới hậu cài HeThong hoặc đỏ do fixture thay vì định danh.
  lệnh       : python3 -u probes/review14-mutations.py > evidence/mutations-round15.log 2>&1; patch --batch copies/system-post-mutant/ops/vm/cap-nhat-cong-cu.ps1 -i luot14/evidence/r14-mutation-r13-system-post-numeric.patch; python3 -u probes/post-observations-round15.py > evidence/post-observations-round15.log 2>&1
  output     : Review14 mutations:17/17 KILLED. HeThong hậu cài số học:110/112/rc1, chỉ he_thong_hau_cai_zero_dau_phai_loi và he_thong_hau_cai_git_windows_marker_phai_loi đỏ; control xanh. ZIP hậu cài số học:110/112/rc1, đúng2ca alias đỏ. Không ParserError. Patch tái dựng và product mutant trùng byte bản áp nguyên văn L14. Quan sát6/6: head zero=>4loi, Git thiếu marker=>Gitloi; mutant nhận4nang_cap/Gitnang_cap; control cảhai4nang_cap. Mỗi run4installer kiểm băm+4marker+4native direct-after rc0.
  kết luận   : KHÔNG PHẢI LỖI ở bản vá test lượt14: finding test-thieu-duong-tich-hop ĐÃ ĐÓNG. Helper quan sát trùng byte helper thêm trong test; Get-PhienBanLenh, Save-CoKiemBam, Assert-Bam, Install-Msi và Invoke-TangHeThong là source thật; installer/HTTP/tasks được mô hình có trạng thái, không dựng Add-KetQua.17là số reviewer đo, không dùng40executor khai làm chứng cứ. Còn P2 ghim ở H11 là cơ chế khác, không tái mở finding cũ.

### ghim-actionlint-khong-la-dich-chung-nhan  [P2]  Thiếu chốt tag phản hồi phải khớp ghim trước khi chứng nhận actionlint
TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:361` (nguồn đích), `:364` (giu), `:380` (hậu cài), `:471` (caller truyền ghim).
VẤN ĐỀ: Hợp đồng B yêu cầu đích actionlint là ghim bản kê. Caller truyền Tag đúng, nhưng Update-CongCuZip gán `$moi` từ `$rel.tag_name` cả khi có Tag. Không có điều kiện buộc hai nguồn nhất quán; cả hai điểm chứng nhận chỉ so current/sau với giá trị response. Vì thế HTTP trả metadata mâu thuẫn ghim có thể thay đích cần chứng nhận. Probe đọc bản kê thật ghim1.7.7, quan sát Get-Release thật yêu cầu `/releases/tags/v1.7.7`; HTTP giả trả `tag_name=v9.9.9`, vẫn có asset đúng tên ghim và băm ZIP đúng. Native9.9.9/rc0 được `giu` hoặc `nang_cap`, dù khác1.7.7. Đây là P2 thiếu điều kiện theo hợp đồng, có phân tích tĩnh và phản chứng ngoại tuyến; **không có bằng chứng API GitHub thật trả metadata như vậy, không kết luận P1 trên VM hoặc P0**. Không phải hồi quy do bản vá chỉ-test lần này và không tái mở finding lượt14.
ĐÃ THỬ NGHIỆM: `python3 -u probes/pinned-release-round15.py`:3quan sát/harness rc0; control ghim1.7.7=>nang_cap1.7.7; post-mismatch=>nang_cap9.9.9/1download; keep-mismatch=>giu9.9.9/0download, cảhai native rc0, không khớp ghim. `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File copies/hint-tests-only/ops/vm/cap-nhat-cong-cu_test.ps1`=>113/115/rc1, đỏ đúng2ca mismatch; prototype có chốt=>115/115/rc0. `python3 probes/validate-hint-round15.py` xác nhận probe với ghim thật trên prototype3/3, mismatch thành loi trước tải, patch -p0 tái áp khớp byte bản đã test. Không ParserError/fixture exception ở hai ca đỏ. Xem `evidence/pinned-release-round15.json`, `evidence/hint-tests-head.log`, `evidence/hint-prototype.log`, `evidence/hint-validation-round15.json`.
ĐỘ TIN: cao về thiếu điều kiện trong source và kết quả fixture; chưa đo xác suất/khả năng dịch vụ thật trả response mâu thuẫn.
GỢI Ý — vá ở đâu: Update-CongCuZip, ngay sau Get-Release và trước mọi nhánh giu/so sánh/tải.
GỢI Ý — vá thế nào: nếu có Tag, dùng chính Tag làm đích, kiểm Test-CungDinhDanh giữa response tag với Tag; lệch thì throw để catch hiện hữu ghi loi. Không dùng metadata HTTP thay ghim. Không đổi chính sách latest của rg/shellcheck hoặc các ngoại lệ Node/3010/Python. `HINT.patch` minh họa guard và nguồn đích này, kèm3ca native, chỉ mới áp/test trên bản sao reviewer.
GỢI Ý — ca test khóa: control URL/response/pin/phiên bản đúng vẫn nâng; pin2.0.0 nhưng response3.0.0 ở cả current1.0.0 và current3.0.0 đều phải loi. Giữ băm/copy/getter thật, chỉ fake HTTP, quan sát URL yêu cầu và native rc/output; không giả Add-KetQua.
GỢI Ý — nguy cơ bản vá: từ chối release nếu upstream dùng quy tắc tag khác ghim. Dùng cùng Test-CungDinhDanh để chỉ bỏ tiền tố v, bảo toàn định danh và case; không dùng so số học để chấp nhận alias, không ảnh hưởng luồng không ghim. HINT chưa được áp vào cây thật; executor tự tái dẫn xuất, tự đo, tự commit và khai provenance nếu dùng.

HƯỚNG 14: native argv/icacls và phân biệt mã thoát theo nền
  giả thuyết : đường dẫn có khoảng trắng/Unicode/ký tự shell bị tách; mã lỗi bị nuốt ở cửa ACL.
  lệnh       : pwsh/pwsh -NoProfile -File probes/icacls-round15.ps1 > evidence/icacls-round15.json (probe L4 chỉ đổi đường nạp sang copies/head); Python assert5quan sát.
  output     : 5/5PASS; argv roundtrip=true cho4lần gọi đường dẫn tuyệt đối có Unicode/khoảng trắng và ký tự &$`[]; rc0 không ném, rc1/5 ném, rc1332 của fixture bị POSIX thu thành52 vẫn ném; bỏ binary tuyệt đối cũng ném.
  kết luận   : KHÔNG PHẢI LỖI về truyền argv/fail-close đã đo. Đây là executable giả native trên Linux, không phải icacls thật; không lấy1332 cấu hình fixture làm mã thoát Windows quan sát. Probe hardcode63/68ca từ L4/L5 và utility dựng HINT/finalize trên SHA cũ không dùng để chứng nhận head; AST/accounting112tên và phép đo tương ứng thay chúng. Các driver hành vi hồi quy L4–L14 đã reroot sang bản sao hiện tại, mọi kết quả ở evidence/. Không chạy script finalize verdict lịch sử hoặc dùng chúng ghi đè verdict hiện hành.

HƯỚNG 15: kiểm cuối exact SHA, chỉ đọc cây nguồn và tính toàn vẹn artifact
  giả thuyết : head/source đổi sau đo hoặc HINT không phải bản đã kiểm.
  lệnh       : python3 probes/final-audit-round15.py > evidence/final-audit-round15.log 2>&1
  output     : head=c489c722db43623f1d9b2250420edce0005a96d5; tree=156f174533a899299bc1e4dd927366c7b63e83c0; detached=true/shallow=false/core.abbrev7; status kể cả ignored rỗng; diff HEAD/index rỗng;5Git blob/source/copies khớp byte.112/112,112Booleantrue;17/17mutant;19/19Add khác loi được đối chiếu; HINT dry-run/apply0/trùng byte bản115/115;1findingP2. Chi tiết evidence/final-audit-round15.json.
  kết luận   : KHÔNG PHẢI LỖI về mỏ neo/artifact; không sửa cay-kho/, không push/merge/gọi mạng, không review ops/land/. Snapshot sạch không phải trace chứng minh chưa từng ghi rồi hoàn nguyên; các thao tác reviewer thực hiện chỉ đọc cây nguồn và ghi scratch/bản sao. Windows NTFS/ACL/tasks/MSI/luồng VM thật tại SHA này KHÔNG ĐO ĐƯỢC, không dùng số71/71 hoặc11/11 ở SHA trước để chứng nhận head này.

Kết luận cuối: **changes_requested** tại `c489c722db43623f1d9b2250420edce0005a96d5`: **0 P0,0 P1,1 P2,0 P3**. Finding lượt14 đã đóng bằng đột biến đúng2ca đỏ. Còn P2 `ghim-actionlint-khong-la-dich-chung-nhan`: thiếu ràng buộc pin khi metadata HTTP mâu thuẫn; phản chứng hoàn toàn ngoại tuyến, không khẳng định GitHub/VM thật có metadata sai. A không có phản chứng; B có thiếu điều kiện tại2điểm ZIP ghim; các vị trí còn lại có guard hoặc ngoại lệ theo yêu cầu. Bộ bắt buộc head112/112/rc0; HINT A/B113/115=>115/115, chỉ áp trên bản sao.
