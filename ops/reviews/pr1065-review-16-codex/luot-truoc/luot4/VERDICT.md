verdict: changes_requested
reviewed_sha: e5e2430d93dddfa643e949ef83c75b7aee59c58c

Kết quả: 0 P0, 1 P1, 1 P2, 0 P3.

## ĐÓNG FINDING LƯỢT 3

| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| giao-acl-theo-junction | **ĐÃ ĐÓNG biểu hiện/lớp cũ** | H2/H8: README_native_acl_commands=0; Register thật với Tools ancestor là symlink: tool_acl_calls=0, 3 call chỉ cây cài đặt. Native Windows KHÔNG ĐO ĐƯỢC. |
| test-thieu-duong-tich-hop | **CHƯA ĐÓNG LỚP**, đã bắt đủ 6/6 phản chứng cũ | H3: sáu mutant rc1, ca đỏ trong bảng. H6/H8: owner SID sai và Users F vẫn 63/63 rc0 vì mô hình bỏ qua operand ACL; mô hình độc lập từ chối đúng. |

## BẢNG SĂN

Nhật ký được nối thêm sau mỗi hướng thử; chỉ đo trên head được chỉ định hoặc bản sao có ghi rõ đột biến. Không sửa `cay-kho/`, không gọi mạng.

HƯỚNG 1: định danh, phạm vi và baseline Linux
  giả thuyết : checkout lệch head hoặc suite không đạt 63 ca như khai báo.
  lệnh       : `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1 --untracked-files=all`; `sha256sum PROMPT.md runs/8ea97b46/prompt.snapshot`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : HEAD=e5e2430d93dddfa643e949ef83c75b7aee59c58c; tree=00649aef2557455ce7fc1280ea78f1c121deba2e; status rỗng; cả hai prompt SHA256=e53560aaf7db1dbd7f42e8ec762f177048555c18778dfb1ee4c28bac88b79720. Suite: `cap-nhat-cong-cu tests: 63/63 ca QUA`, process_exit=0 (`evidence/baseline.log`).
  kết luận   : KHÔNG PHẢI LỖI ở baseline Linux. 65/65 Windows do executor khai KHÔNG ĐO ĐƯỢC lại tại đây.

Reviewer: Codex, provider OpenAI, model family GPT-6 theo chỉ thị phiên (không có API xác minh model triển khai cụ thể); execution_surface=API agent có shell Linux; transport=machine/local; session=runs/8ea97b46; github_submitter_identity=null. Review độc lập executor Claude. Chỉ thị trực tiếp của người dùng là authority cho review này; chỉ đọc toàn bộ ops/vm/, ghi verdict/evidence/probe/bản sao bên ngoài cay-kho/. Review class=sensitive. Không merge/land/push/mạng. Skill cloud-environment-runtime đã đọc; environment_status không có trong toolset, không tra credential/network. Quy định repo đã đọc; chỉ thị review cụ thể của người dùng quyết định phạm vi, không mở ops/land/.

HƯỚNG 2: loại bỏ đường giao quyền Tools trong README và Register
  giả thuyết : P0 cũ còn tồn tại ở công thức tay hoặc lệnh native khác trong ops/vm/.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/audit-source.log 2>&1`; đọc trọn ba tệp ops/vm/ và `diff-tu-luot3.patch`.
  output     : `parse_errors=0; pwsh=7.6.9; os=Ubuntu 24.04.5 LTS`; `README_native_acl_commands=0`. Register chỉ còn ba lời gọi Invoke-Icacls dòng 524/525/538 vào `$Script:ThuMucCaiDat`; cây Tools chỉ được Test-Path/Get-Acl (518). README 51–62 xóa toàn bộ block icacls tay và nêu giới hạn. New-ThuMucTai còn icacls riêng ở 302 (thư mục tải mới, không phải giao Tools).
  kết luận   : KHÔNG PHẢI LỖI ở biểu hiện P0 lượt 3: đã loại hành động gây lỗi thay vì chuyển hướng dẫn đi nơi khác. Việc cấp quyền đã làm trên VM trước đây không được rollback/chứng nhận bởi review này. Junction/ACL/Task native KHÔNG ĐO ĐƯỢC ở Linux; đo dispatch của Register bổ sung ở các hướng sau.

HƯỚNG 3: chạy lại ĐÚNG sáu đột biến sống ở lượt 3
  giả thuyết : suite mới vẫn để runtime bypass vượt qua dù giữ nguyên hình dạng AST.
  lệnh       : `python3 -u probes/mutations.py --group old > evidence/mutations-old-summary.log 2>&1`. Mỗi mutant là bản sao head với đúng một biến đổi theo slug; neo/thay nguyên văn ở `evidence/mutation-<slug>.patch`, command/rc/full output ở `evidence/mutations-old.json`.
  output     : cả 6/6 đều ĐỎ rc1, không ParserError/harness error. Chi tiết:

| mutant | N/M | ca đỏ (bỏ tiền tố dk_chay_) |
| --- | --- | --- |
| runtime-drop-task-config | 62/63 | doi_so_tac_vu_day_du |
| runtime-skip-audit | 60/63 | do_acl_moi_tep_sau_khi_chep; tu_choi_acl_sai; tu_choi_bam_lech |
| runtime-skip-inheritance | 59/63 | icacls_chi_cham_thu_muc_cai_dat; do_acl_moi_tep_sau_khi_chep; doi_so_tac_vu_day_du; tu_choi_bam_lech |
| runtime-skip-owner-after-copy | 59/63 | icacls_chi_cham_thu_muc_cai_dat; do_acl_moi_tep_sau_khi_chep; doi_so_tac_vu_day_du; tu_choi_bam_lech |
| runtime-skip-reparse | 61/63 | tu_choi_to_tien_cai_dat_la_lien_ket; tu_choi_cai_dat_la_lien_ket |
| registration-copy-hash | 62/63 | tu_choi_bam_lech |

  kết luận   : KHÔNG PHẢI LỖI với sáu phản chứng cũ: ca thực thi có răng đối với cả sáu. Chưa kết luận mô hình đồ giả đầy đủ chỉ từ kết quả này; kiểm tham số/thay đổi trạng thái tiếp ở hướng sau.

HƯỚNG 4: Invoke-Icacls thật — đường dẫn, mảng đối số và mã thoát
  giả thuyết : wrapper mới làm tách đối số, tra PATH, hoặc nuốt native rc khác 0.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/icacls.ps1 > evidence/icacls.json 2> evidence/icacls.stderr` (rc0). Shim executable Python nằm thật tại SystemRoot/System32 có dấu cách + tiếng Việt; ghi argv rồi trả rc, không giả hàm Invoke-Icacls.
  output     : cả bốn lần argv roundtrip=true với `D:\thư mục a&$`[x]\`, `/grant:r`, `*S-1-5-18:(OI)(CI)F`, `/L`, `/Q`; exe luôn tuyệt đối trong System32. rc0 không ném; rc1/5 ném thông báo đúng rc và dòng stderr cuối. Yêu cầu exit1332 trên POSIX được hệ điều hành rút còn52; wrapper ném rc52 (không lấy đây làm phép đo mã Windows1332). Xóa exe tuyệt đối ⇒ ném, không chạy executable từ PATH. stderr của probe rỗng.
  kết luận   : KHÔNG PHẢI LỖI trong dispatch/rc/splat đã đo Linux. Windows CreateProcess/icacls/NTFS thật KHÔNG ĐO ĐƯỢC tại đây. Wrapper chỉ là cửa chung cho đăng ký; New-ThuMucTai vẫn gọi native trực tiếp với chốt rc riêng, khớp chú thích sản phẩm.

HƯỚNG 5: bốn đột biến bổ sung executor khai đã giết
  giả thuyết : suite không bắt icacls chạm Tools, mất /L, mất ErrorAction Stop hoặc nuốt rc.
  lệnh       : `python3 -u probes/mutations.py --group additional > evidence/mutations-additional-summary.log 2>&1`; diff/command/full output ở `evidence/mutation-*.patch`, `evidence/mutations-additional.json`.
  output     : icacls-tools → 60/63 rc1 (ca chỉ chạm cài đặt + 2 ca reparse); icacls-without-L → 62/63 rc1 (dk_chay_icacls_chi_cham_thu_muc_cai_dat); register-without-erroraction → 61/63 rc1 (scheduledtask_co_erroraction_stop, dk_chay_doi_so_tac_vu_day_du); icacls-swallow-rc → 62/63 rc1 (icacls_rc_khac_0_thi_nem). Không ParserError.
  kết luận   : KHÔNG PHẢI LỖI ở bốn lời khai này. Cộng sáu đột biến cũ: 10/10 đều đỏ, xác nhận độc lập trên bản sao head.

HƯỚNG 6: đồ giả giữ trạng thái hay chỉ nhận diện tên công tắc
  giả thuyết : mô hình Get-Acl biến mọi `/setowner` thành Administrators và mọi `/inheritance:r` thành ACL đọc, bỏ qua principal/quyền thực.
  lệnh       : `python3 -u probes/mutations.py --group models > evidence/mutations-models-summary.log 2>&1`; đọc test 365–381.
  output     : owner-wrong-principal (cả hai setowner SID544→SID545), grant-user-write (Users RX→F), inheritance-without-grant (bỏ toàn bộ grant), grant-admin-readonly (SYSTEM/Administrators F→RX) đều `cap-nhat-cong-cu tests: 63/63 ca QUA`, rc0. Diff và full output ở `evidence/mutation-<slug>.patch/.log`; JSON `evidence/mutations-models.json`. Mô hình tại test 375–379 chỉ tra `/setowner` và `/inheritance:r`, không đọc SID đích/quyền grant; Invoke-Icacls giả 361 chỉ ghi sự kiện.
  kết luận   : LỖI tiềm năng P2 cần đối chứng hành vi: hai đột biến owner-wrong-principal/grant-user-write làm thay đổi đúng thuộc tính audit cần bảo vệ nhưng đồ giả vẫn trả tốt. Hai đột biến bỏ grant/giảm quyền chưa đủ làm finding riêng vì chưa đo native về khả năng chép/chạy. Không quy hành vi mutant thành P0/P1 của head. Đối chứng bằng Register thật với mô hình đọc argv ở hướng tiếp.

HƯỚNG 7: nhánh không đo được và cách đếm N/M
  giả thuyết : có nhánh thiếu quyền/nền/dependency được tính ĐẠT dù bỏ phép đo.
  lệnh       : `python3 probes/test-branches.py > evidence/test-branches.log`; đối chiếu ca thật trong `evidence/baseline.log` và test 79–94, 164–175, 228–255, 318–429.
  output     : 67 tên ca khai báo, đều duy nhất. Linux thực thi 63 ca; Windows thường thay ca Linux bằng wrong-host và thêm 2 ca nonadmin ⇒ 65 ca. Windows admin thay hai ca nonadmin bằng `admin_ca_ma_thoat_3_khong_do_duoc` trả `$false`, nên 64 ca và bị ĐỎ. Python/PyYAML thiếu ném lỗi qua Ca, không xanh. Không thấy nhánh `không đo được ⇒ $true` ở head. Các ca Register dừng trước credential/COM theo thiết kế và không tự tuyên bố đo hai đoạn ấy.
  kết luận   : KHÔNG PHẢI LỖI về nhánh skip vẫn đếm pass đã kiểm. Con số 65/65 tự nó không đo NTFS/icacls đăng ký thật vì đồ giả dùng trên cả hai nền; không đổi kết quả fake thành bằng chứng native.

HƯỚNG 8: đối chứng Register bằng mô hình ACL đọc target/SID/quyền thật
  giả thuyết : các mutant xanh ở H6 là vô hại hoặc mô hình reviewer cũng diễn kịch theo số lần gọi.
  lệnh       : `python3 -u probes/registration-matrix.py > evidence/registration-summary.log 2>&1`; từng command/rc/JSON ở `evidence/registration-matrix.json`, probe `probes/registration.ps1`.
  output     : head clean → 3 icacls, 4 audit, tool_acl_calls=0, task SYSTEM=1 rồi REVIEW-STOP-BEFORE-CREDENTIALS; head acl-reject/hash-reject → tasks=0 với lỗi ACL/lệch băm; head install-ancestor-link/install-child-link → 0 icacls, 0 task, lỗi reparse. Mọi ca có Tools là symlink tới victim; chưa có call nào vào Tools. Mô hình dùng target + /T + giá trị sau /setowner + SID/quyền sau /grant:r, thực chép tệp. owner-wrong-principal → `chủ sở hữu 'BUILTIN\Users'`, tasks=0; grant-user-write → `BUILTIN\Users: FullControl`, tasks=0. Cả hai bị audit thật của sản phẩm từ chối trong mô hình reviewer, trong khi suite head vẫn đăng ký task và xanh 63/63 dưới cùng đột biến. Hai mutant bỏ grant/giảm quyền vẫn tới task trong mô hình này; mô hình KHÔNG mô phỏng quyền I/O native nên không dùng chúng làm bằng chứng hỏng triển khai. Sáu mutant cũ có hành vi tương ứng ở JSON; skip-inheritance/owner bị audit mô hình có trạng thái từ chối.
  kết luận   : LỖI P2 xác nhận ở lớp test-thieu-duong-tich-hop: đã bắt đủ sáu chốt runtime cũ nhưng đồ giả vẫn tạo ACL tốt bất kể principal/quyền truyền vào. Không có P0/P1 của sản phẩm head từ phép đo mutant. P0 giao-acl-theo-junction đã đóng biểu hiện cũ (xóa hành động), cả mô hình độc lập cũng xác nhận dispatch Tools=0. NTFS/owner/ACL hiệu lực/junction/task/password/COM native KHÔNG ĐO ĐƯỢC.

HƯỚNG 9: đường thứ ba — tải/băm/chạy installer và dọn tệp của HeThong
  giả thuyết : ngoài Register, có đường chạy installer trước hash, thiếu hash vẫn cài, hoặc lỗi MSI/3010 làm sai kết quả.
  lệnh       : chạy `pwsh/pwsh -NoProfile -File probes/system-install.ps1 -Mode <mode>` với success/download-tamper/missing-hash/installer-failure/msi-reboot/post-version-wrong; command/rc/output ở `evidence/system-matrix.json`, full log `evidence/system-<mode>.log`.
  output     : cả 6 probe rc0 (probe bắt lỗi để xuất dữ liệu). success: 4 spawn, tất cả hash_matches=true, 4 nâng cấp + restart Commander; download-tamper và missing-hash: 0 spawn, cả 4 công cụ loi; installer-failure (rc1603): 4 loi, vẫn thử cả bốn và restart Commander; msi-reboot: gh/node/pwsh can_khoi_dong_lai, Git nâng cấp; post-version-wrong: cả 4 loi. Mọi mode remaining_downloads=0. Dùng Save-CoKiemBam/Assert-Bam/New-ThuMucTai/Install-Msi/Invoke-TangHeThong thật; HTTP, đọc phiên bản, Start-Process/task và native icacls là stub offline.
  kết luận   : KHÔNG PHẢI LỖI ở các nhánh fail-closed/thứ tự hash/khôi phục/dọn tệp đã đo. KHÔNG ĐO ĐƯỢC installer/msiexec/ACL/Node/Commander thật trên Windows; không lấy shim Linux làm chứng nhận native. Đây là hướng độc lập ngoài hai finding cũ.

HƯỚNG 10: đường thứ ba — lỗi khởi chạy npm có được cô lập theo công cụ?
  giả thuyết : npm tồn tại khi kiểm nhưng không khởi chạy được thì ghi `loi` rồi vẫn thử các công cụ độc lập và ghi nhật ký.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/user-errors.ps1 -Mode success`, `-Mode npm-cannot-start`, `-Mode npm-disappears`; command/rc/dữ liệu ở `evidence/user-matrix.json`, tóm tắt `evidence/user-summary.log`.
  output     : success: 11 dòng kết quả, error=null, error_rows=0. npm-cannot-start: tệp tồn tại nhưng fixture bỏ bit execute Unix, PS ném tại sản phẩm :388 (`Program 'npm.cmd' failed to run ... No such file or directory` — giữ nguyên thông báo thực tế, KHÔNG gọi đây là lỗi NTFS). npm-disappears: hook Test-Path đo có tệp rồi xóa nó để mô phỏng dependency biến mất giữa stat/launch; npm_removed_after_stat=true và lỗi `The term '.../npm.cmd' is not recognized ...`. Cả hai ca chỉ còn 5 dòng python/pip/PyYAML/jsonschema/venv-kho, error_rows=0; chưa thử rg/shellcheck/actionlint/nlm, không có dòng lỗi claude/codex. Probe rc0 vì bắt lỗi của hàm thật để in JSON.
  kết luận   : LỖI P1 của xử lý lỗi native trong NguoiDung: lỗi khởi chạy không đi qua nhánh `$rc` ở 389–392, thoát toàn bộ hàm. Phần main :609 gọi hàm không try/catch, nên về tĩnh không tới đoạn tạo nhật ký :611–624 khi lỗi ấy ném. Đo hàm thật tại head trên Linux, không sửa sản phẩm; KHÔNG ĐO ĐƯỢC chặn thực thi Windows hay lần chạy task Windows thật. Điều kiện dependency biến mất không phụ thuộc bit execute Unix; không khẳng định lỗi đang xảy ra trên VM.

HƯỚNG 11: đường thứ ba — native storage status thất bại nhưng còn JSON hợp lệ
  giả thuyết : status CLI trả rc≠0 thì phải ghi lỗi thay vì xác nhận credential storage thành công từ riêng stdout.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/user-errors.ps1 -Mode nlm-status-fails`; đối chứng `-Mode success`; fixture executable ghi JSON `{ "mode": "file" }`, stderr `storage-native-failure` rồi exit7, không gọi mạng/gói thật. Command/full output ở `evidence/user-matrix.json`, `evidence/user-nlm-status-fails.log`.
  output     : failed-status: last_native_exit=7, error=null, error_rows=0; kết quả nlm=`giu`, chi_tiet=`storage=file`, cùng toàn bộ 11 dòng được coi đạt như control rc0. Pip upgrade trước đó rc0 và version getter có dữ liệu; chỉ status bị lỗi. :416–419 parse JSON và chỉ so `$rc` đã lưu từ pip ở :410, không kiểm mã thoát của status. Ngoại lệ JSON thì catch, nhưng rc native mặc định không ném.
  kết luận   : LỖI P1, biểu hiện thứ hai cùng lớp loi-native-tang-nguoi-dung: lỗi native có thể bị nuốt thành ĐẠT. Theo công thức main :611–624 (phân tích tĩnh), error_rows=0 dẫn `ok=true` và exit0; probe chỉ trực tiếp đo hàm thật, không khai đã chạy entry point Windows. Không đo credential thật hay nlm package thật, chỉ đo phản ứng của head trước output+rc từ executable cục bộ.

HƯỚNG 12: test-only hint cho mô hình ACL, tự áp và đo ngoài cây review
  giả thuyết : có thể sửa điểm mù của đồ giả mà vẫn giữ các phản chứng cũ đỏ, không cần sửa production trong phiên reviewer.
  lệnh       : `python3 probes/build-hint.py`; `patch -p0 --dry-run -d hint-validation < HINT.patch`; `patch -p0 -d hint-validation < HINT.patch`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1`; `python3 -u probes/hint-check.py > evidence/hint-summary.log 2>&1`.
  output     : dry-run `checking file ops/vm/cap-nhat-cong-cu_test.ps1`, apply `patching file ...`, đều rc0. Hint baseline `64/64 ca QUA`, rc0 (`evidence/hint-baseline.log`; thêm 1 ca). 14/14 mutant rc1, parser_errors=0 (`evidence/hint-mutations.json`): 10 mutant cũ/bổ sung đều vẫn đỏ; owner-wrong-principal và grant-user-write đều 59/64, inheritance-without-grant và grant-admin-readonly đều 63/64. Hint chỉ đổi tệp TEST: mô hình nhận target, /T, owner SID và grant SID/quyền, cộng ca đòi đúng ACL dự kiến; không sửa sản phẩm.
  kết luận   : KHÔNG PHẢI LỖI về hiệu lực hint trong Linux đã đo. Đây là mô hình giới hạn của tập lệnh hiện tại, không phải engine NTFS (ví dụ inheritance removal không mô phỏng mọi explicit ACE có sẵn); không quảng bá hint thành native access proof. Windows chưa chạy. Không phải bản vá P1.

Bổ sung H10/H11: `python3 probes/user-oracle.py > evidence/user-oracle.log 2>&1` → `PASS success`, `FAIL npm-disappears`, `FAIL nlm-status-fails`, `User native error oracle: 1/3 PASS`, oracle_exit=1. Đây là hai phản chứng ĐỎ có chủ ý đối với hàm sản phẩm chưa sửa; khác với baseline suite 63/63. Dữ liệu đầy đủ và command ở `evidence/user-oracle.json`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| lớp / nguồn | phân loại tại head này | bằng chứng độc lập |
| --- | --- | --- |
| giao-acl-theo-junction — P0 lượt 3 tại bbc3430779327c64eb3f905fb0037d7882c4cc55 | **ĐÃ VÁ THẬT** biểu hiện/lớp giao quyền Tools được hướng dẫn | README bỏ block tay; Register chỉ đọc Tools. H2/H8: Tools ancestor là symlink, tool_acl_calls=0; 3 call chỉ vào PF/tra-luat-ops. Không suy việc cấp ACL lịch sử trên VM đã được thu hồi. |
| test-thieu-duong-tich-hop — P2 lượt 3 tại cùng SHA | **VÁ HỜ ở cấp lớp**; cả **6/6 phản chứng cũ ĐÃ VÁ THẬT**, nhưng mô hình chưa đọc giá trị owner/grant | H3 giết đủ sáu; H5 giết đủ bốn bổ sung; H6 hai mutant principal/quyền vẫn 63/63; H8 mô hình đọc argv xác nhận hai mutant phải bị audit từ chối. Giữ slug cũ, không đếm hai lỗi P2. |
| loi-native-tang-nguoi-dung — mới ở lượt này | **LỖI MỚI PHÁT HIỆN**, không có bằng chứng bản vá lượt 3 tạo ra | H10/H11/oracle đo hai biểu hiện cùng lớp xử lý kết quả native ở toàn ops/vm/, thuộc phạm vi đọc toàn cây được yêu cầu. |

### loi-native-tang-nguoi-dung  [P1]  Lỗi native ở NguoiDung làm mất phần còn lại của lượt hoặc được ghi ĐẠT

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:388` (khởi chạy npm), `:416`–`:420` (storage status của nlm); tác động tới tổng kết/nhật ký `:609`–`:624`.
VẤN ĐỀ: Có hai biểu hiện của một lớp xử lý lỗi native không đầy đủ. (a) Trong vòng npm, chỉ mã thoát sau khi tiến trình đã khởi chạy mới được xử lý; lỗi phân giải/khởi chạy ở `& $npm` không được catch. Khi dependency biến mất giữa Test-Path và invoke, cả tầng dừng trước rg/shellcheck/actionlint/nlm; chưa có dòng `loi` cho công cụ, và main không có catch để tới đoạn ghi nhật ký. (b) Với nlm, `$rc` dùng ở :418 là rc pip đã lưu tại :410. `auth storage status --json` có thể trả mã lỗi nhưng vẫn có JSON `mode=file`; code bỏ qua rc status, che stderr và ghi `giu`/`storage=file`. Theo công thức tổng kết, trường hợp này được `ok=true`/exit0 dù status probe thất bại. Không gọi đây là P0; đây là hành vi sai của chính head khi dependency báo lỗi, không phải mutation sản phẩm.
ĐÃ THỬ NGHIỆM: `pwsh/pwsh -NoProfile -File probes/user-errors.ps1 -Mode npm-disappears` → hook đo có tệp rồi xóa để mô phỏng dependency biến mất; hàm thật ném command-not-found, còn đúng 5 dòng kết quả đầu, 0 dòng lỗi, chưa tới các công cụ độc lập. `-Mode nlm-status-fails` → executable thật in JSON file + stderr rồi exit7; hàm ghi đủ 11 dòng ĐẠT, nlm `giu`, `storage=file`, last_native_exit=7, error_rows=0. Đối chứng success đủ 11 dòng, rc native0. `python3 probes/user-oracle.py` → 1/3 PASS rc1, hai ca lỗi đều ĐỎ (`evidence/user-oracle.log/.json`). Các probe nạp hàm nguyên bản bằng -NapHam và dùng executable fixture thật; chỉ Set-Path/ZIP được stub để không thay môi trường/cài/mạng. Không chạy entry point Windows vì Linux bị chốt nền; suy hệ quả nhật ký/exit từ main đã chỉ rõ là phân tích tĩnh. Lỗi quyền native Windows/nlm thật KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về luồng lỗi và phân loại kết quả tại head; chưa đo điều kiện dependency/ACL/runtime thật trên VM.
GỢI Ý VÁ: tại vòng npm trong Invoke-TangNguoiDung, đặt ranh giới try/catch theo công cụ để lỗi resolve/launch cũng Add-KetQua `loi` và tiếp tục công cụ độc lập; bảo đảm luồng tổng kết vẫn chạy. Tại status nlm, thu riêng stdout/stderr và rc NGAY sau lệnh native, yêu cầu rc0 + JSON đúng schema/mode=file; giữ riêng rc pip, không vô tình ghi đè. Không cần viết lại wrapper SYSTEM đã đo tốt. Ca khóa: success vẫn đủ 11 dòng; dependency biến mất sau Test-Path phải ghi loi và vẫn thử rg/shellcheck/actionlint/nlm, nhật ký có lỗi và exit1; status rc7 + JSON file phải ghi nlm loi, rc0 + JSON file phải đạt, JSON hỏng/mode khác vẫn lỗi. Script phản chứng chạy được ở probes/user-errors.ps1 và probes/user-oracle.py. Rủi ro vá: catch rộng có thể che lỗi lập trình/thay lỗi thành `bo_qua`; cần giữ thông báo và mã thất bại, không tự retry vô hạn hay in credential. Kiểm thêm main + task Windows khi executor có VM để khóa hệ quả nhật ký.

### test-thieu-duong-tich-hop  [P2]  Đồ giả ACL vẫn tạo trạng thái tốt bất kể SID owner và quyền grant

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu_test.ps1:361`, `:365`–`:381`, đặc biệt `:375`–`:379`; các ca Register `:395`–`:425`.
VẤN ĐỀ: Bộ test mới đã gọi Register thật và bắt cả sáu bypass cũ. Nhưng Get-Acl giả gán Administrators mặc định, xem bất kỳ `/setowner` nào như đã sửa owner, và xem bất kỳ `/inheritance:r` nào như đã bỏ quyền ghi; nó không lấy SID sau `/setowner`, SID/mask sau `/grant:r`, hay ứng dụng đúng thao tác tới node để suy ACL. Vì vậy đổi cả hai owner từ Administrators sang Users hoặc cấp Users F thay RX đều vẫn đăng ký task trong mô hình và đạt 63/63. Các ca pure Test-AclChiAdminGhi đúng nhưng dữ liệu sai không bao giờ tới chúng trong mô hình Register. Đây là một lớp P2 tiếp diễn, không phải thêm P0 vì mutant không phải head và không phải lời khẳng định head đang cấp Users F.
ĐÃ THỬ NGHIỆM: `python3 -u probes/mutations.py --group old` → cả sáu rc1, ca đỏ liệt kê H3. `--group models` → owner-wrong-principal và grant-user-write đều 63/63 rc0, diffs chỉ thay SID544→545 hoặc RX→F ở lệnh native, không sửa test. `python3 -u probes/registration-matrix.py` → mô hình đọc argv, gọi chính Register và chính Test-AclChiAdminGhi: owner sai bị `chủ sở hữu BUILTIN\Users`, grant sai bị `BUILTIN\Users: FullControl`, tasks=0; head clean tasks=1 và audit=4. Native ACL Windows KHÔNG ĐO ĐƯỢC; phản chứng này đo tính nhất quán của đồ giả và luồng audit. HINT.patch ở bản sao: 64/64 rc0, cả 14 mutant rc1, không ParserError.
ĐỘ TIN: cao.
GỢI Ý VÁ: sửa mô hình test Invoke-Icacls/Copy-Item/Get-Acl để giữ trạng thái theo từng node và đọc target, /T, SID owner, inheritance và từng grant thực; tệp chép có owner người chép cho tới setowner sau đó. Thêm khẳng định các ACL operand dự kiến để khóa cả độ an toàn và khả năng user đọc/admin ghi; mô hình không hỗ trợ một cú pháp phải fail rõ. Ca khóa: hai mutant owner sai/Users F bắt buộc đỏ do dữ liệu ACL sai thực sự tới audit; giữ sáu mutant runtime cũ đỏ; kiểm thiếu grant/quyền admin cũng đỏ ở assertion hợp đồng. Test-only HINT.patch là ví dụ đã đo Linux, executor tự tái dẫn xuất, không phải yêu cầu làm đúng nguyên văn. Rủi ro vá: mô hình tự viết có thể sai NTFS (deny, inheritance, owner, ACL copy, junction) hoặc quá chặt làm cản refactor; cần khai phạm vi mô hình và có phép đo native trên VM, không nâng model pass thành native pass.

`HINT.patch`: định dạng `patch -p0` từ gốc bản sao cay-kho/, chỉ sửa tệp TEST `ops/vm/cap-nhat-cong-cu_test.ps1`; SHA256 `14491ba9333662f1738f0e4ab6303e210214b59f91113c8b534786f7c659bdda`.
**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Hint không sửa P1 production, không cấp authority commit/push/merge/land. Nếu dùng, executor khai hint_provenance theo protocol. Các probe và mutation diff là dữ liệu phản chứng, không phải thay đổi branch executor.

## GIỚI HẠN VÀ QUYẾT ĐỊNH

- Chốt P0 giao Tools của lượt 3 đã được loại bỏ khỏi cả script và hướng dẫn. Không tìm thấy P0 mới được chứng minh trong lần rà toàn ops/vm/; không tuyên bố VM hoàn toàn an toàn.
- Còn 2 lớp: một P1 loi-native-tang-nguoi-dung (2 biểu hiện) và một P2 test-thieu-duong-tich-hop (điểm mù principal/quyền của mô hình). Đếm theo lớp, không nhân số lượng mutant/biểu hiện thành số finding.
- Baseline Linux **63/63 PASS, rc0**. Sáu mutant cũ **6/6 bị giết**, bốn mutant bổ sung **4/4 bị giết**; hai mutant ACL trọng yếu mới vẫn xanh trong suite head. Oracle lỗi user **1/3 PASS, rc1** là bằng chứng lỗi sản phẩm có chủ ý. Hint test-only **64/64 PASS**, **14/14 mutant bị giết** trên bản sao.
- Windows native **KHÔNG ĐO ĐƯỢC**: junction/NTFS/effective ACL/owner/handle, icacls thật, registration/password/COM/task DACL, msiexec/installer, Commander và môi trường PATH/PSModulePath/TEMP của SYSTEM/tladmin. Các mode symlink Linux chỉ đo scan/dispatch. Không lấy 65/65 do executor khai hoặc model Linux làm chứng nhận các thứ ấy.
- Các giả định cần VM: ProgramFiles và toàn chuỗi tổ tiên phải chỉ admin ghi; TEMP System/parent phải tin cậy, vì New-ThuMucTai tạo theo tên rồi siết ACL, không giữ handle; ProgramData/tra-luat-cap-nhat và tổ tiên log chưa được đọc ACL; module autoload/PATH/COM có ảnh hưởng môi trường. Không đủ điều kiện đo nên không tự gán thêm P0 từ giả định chưa xác minh. README clone còn gọi `git` theo PATH, đã được nêu ở lượt trước, không đếm như lỗi mới.
- Không HTTP/mạng, không credential thật, không pip/npm install thật, không Scheduled Task native, không sửa hay chạy mã trong ops/land/, không push/commit. Mọi fixture/bản sao/hint nằm ngoài cây review. Không thử vá production hoặc đoán bản vá chạy đúng.

Kiểm cuối read-only: `python3 probes/final-audit.py` (`evidence/final-readonly.json`) → mọi lệnh rc0; HEAD vẫn e5e2430d93dddfa643e949ef83c75b7aee59c58c, tree 00649aef2557455ce7fc1280ea78f1c121deba2e; status kể cả ignored rỗng, diff và cached diff rỗng; diff --check từ bbc3430 riêng ops/vm/ rỗng; core.abbrev=7, shallow=false. Cả 3 tệp ops/vm/ khớp byte chính xác blob Git của reviewed_sha. SHA256 script `48ebd0464a418ddc8d861b3091df42f3864b3678d1cd4a14c68d6ccc89da9ed2`; suite `c99a9025fa78b4f386bc52c00875bb782546e34c4b6e3c3982f7c3045fe2d185`; README `e450ff93992576a31b622ce6474c7158ba05f8fdf83c8f8e8267d80fdc95bb6e`.
