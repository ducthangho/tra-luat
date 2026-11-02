verdict: changes_requested
reviewed_sha: d20a69e211f24c0a4beffb1a9cdf41fdf45be531

Review độc lập lượt 11; chỉ đọc cây `cay-kho/`, phép đo trên bản sao khi cần, không gọi mạng. Các mục dưới đây đã được nối thêm sau mỗi hướng kiểm tra; kết luận cuối ở cuối tệp.

## ĐÓNG FINDING LƯỢT 10
| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung | **Đã đóng ba biểu hiện lượt 10; CHƯA ĐÓNG lớp theo B** | H2/H7/H8: target5/5, actual-pip NLM control+stale2/2, ZIP7/7 đều đúng. H10: `python3 -u probes/version-identity-oracle.py` tái hiện 3/3 lượt prerelease khác stable đích nhưng product exit0/ok=true. |

## BẢNG SĂN

HƯỚNG 6: đăng ký lịch, ACL và reparse
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/registration-head.py` (qua `python3 probes/rerun-regressions.py`).
  output     : registration-head: rc0, {"mode": "install-ancestor-link", "passed": true, "rc": 0, "error": "t\u1eeb ch\u1ed1i: /tmp/review-register-bec3cbf4c30946df8572d35ea82ac853/PF/tra-luat-ops c\u00f3 reparse point (junction/symlink): /tmp/review-register-bec3cbf4c30946df8572d35ea82ac853/PF", "icacls_count": 0, "tool_acl_calls": 0, "audit_count": 0, "tasks": 0} | {"mode": "install-child-link", "passed": true, "rc": 0, "error": "t\u1eeb ch\u1ed1i: /tmp/review-register-e7b3e4c40c73486a8b7eedd4c55df15b/PF/tra-luat-ops c\u00f3 reparse point (junction/symlink): /tmp/review-register-e7b3e4c40c73486a8b7eedd4c55df15b/PF/tra-luat-ops/link", "icacls_count": 0, "tool_acl_calls": 0, "audit_count": 0, "tasks": 0}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 5: băm, cài HeThong, hậu kiểm và reboot
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/system-matrix.py`; `python3 -u probes/caller-matrix.py` (qua `python3 probes/rerun-regressions.py`).
  output     : system-matrix: rc0, {"mode": "msi-reboot", "rc": 0, "error": null, "spawns": 4, "verified": true, "left": 0, "restart": true, "rows": [["git", "nang_cap"], ["gh", "can_khoi_dong_lai"], ["node", "can_khoi_dong_lai"], ["pwsh", "can_khoi_dong_lai"], ["commander", "khoi_dong_lai"]]} | {"mode": "post-version-wrong", "rc": 0, "error": null, "spawns": 4, "verified": true, "left": 0, "restart": true, "rows": [["git", "loi"], ["gh", "loi"], ["node", "loi"], ["pwsh", "loi"], ["commander", "khoi_dong_lai"]]}; caller-matrix: rc0, {"mode": "zip-pre", "rc": 0, "data": {"mode": "zip-pre", "spawns": 0, "http_fixture_calls": 1, "results": [{"cong_cu": "rg", "truoc": "", "sau": "2.0.0", "hanh_dong": "cai_moi", "chi_tiet": ""}], "errors": 0}} | {"mode": "zip-post", "rc": 0, "data": {"mode": "zip-post", "spawns": 0, "http_fixture_calls": 1, "results": [{"cong_cu": "rg", "truoc": "1.0.0", "sau": "", "hanh_dong": "loi", "chi_tiet": "sau khi cài đo được '', mong '2.0.0'"}], "errors": 1}}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 3: ChiKiem và prerequisite trên cả hai tầng
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/third-paths-oracle.py`; `python3 -u probes/portable-check-oracle.py`; `python3 -u probes/system-check-oracle.py`; `python3 -u probes/absence-regression-oracle.py` (qua `python3 probes/rerun-regressions.py`).
  output     : third-paths-oracle: rc0, {"mode": "venv-cannot-start", "passed": true, "rc": 1, "ok": false, "errors": 1, "rows": 11, "venv": "loi", "direct_probe": {"path": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr11-pr1065.v3gU/fixtures/third-venv-cannot-start/venv/Scripts/python.exe", "exists": true, "rc": null, "error": "Cannot run a document in the middle of a pipeline: /tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr11-pr1065.v3gU/fixtures/third-venv-cannot-start/venv/Scripts/python.exe.", "output": ""}, "venv_native_calls": 0, "installs": 7} | Venv runtime oracle: 6/6 PASS; portable-check-oracle: rc0, {"mode": "check-zip-rc9", "passed": true, "rc": 1, "ok": false, "errors": 3, "rows": 11, "portable": {"rg": {"cong_cu": "rg", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr11-pr1065.v3gU/fixtures/check-zip-rc9/Tools/bin/rg.exe chưa cài hoặc không đọc được phiên bản"}, "shellcheck": {"cong_cu": "shellcheck", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr11-pr1065.v3gU/fixtures/check-zip-rc9/Tools/bin/shellcheck.exe chưa cài hoặc không đọc được phiên bản"}, "actionlint": {"cong_cu": "actionlint", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr11-pr1065.v3gU/fixtures/check-zip-rc9/Tools/bin/actionlint.exe chưa cài hoặc không đọc được phiên bản"}}, "installs": 0} | Portable ChiKiem oracle: 4/4 PASS; system-check-oracle: rc0, {"mode": "system-no-lts", "passed": true, "rc": 0, "ok": true, "errors": 0, "rows": [["git", "can_cap_nhat", "1.0.0"], ["gh", "can_cap_nhat", "1.0.0"], ["node-major", "can_quyet_dinh", "24.1.0"], ["node", "can_quyet_dinh", "24.1.0"], ["pwsh", "can_cap_nhat", "7.6.9"]], "native_calls": 4, "native_rcs": [0, 0, 0, 0]} | System ChiKiem oracle: 6/6 PASS; absence-regression-oracle: rc0, {"mode": "check-missing-nlm-all", "passed": true, "rc": 1, "ok": false, "nlm": "loi", "errors": 1} | NLM prerequisite oracle (head): 4/4 PASS
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 4: native/catch/continue và lưới nhật ký lượt 4–7
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/l4-user-oracle.py`; `python3 -u probes/user-oracle.py`; `python3 -u probes/user-version-oracle.py`; `python3 -u probes/new-paths-oracle.py`; `python3 -u probes/run-main-tail.py` (qua `python3 probes/rerun-regressions.py`).
  output     : l4-user-oracle: rc0, PASS nlm-status-fails | User native error oracle: 3/3 PASS; user-oracle: rc0, PASS nlm-status-fails | User native error oracle: 3/3 PASS; user-version-oracle: rc0, PASS nlm-version-fails | Version native failure oracle: 3/3 PASS; new-paths-oracle: rc0, {"mode": "check-metadata", "passed": true, "rc": 1, "chi_kiem": true, "loi": 3, "ok": false, "tong": 11} | Remaining native paths oracle: 6/6 PASS; run-main-tail: rc0, {"mode": "system-throw", "rc": 1, "passed": true, "ok": false, "loi": 1, "tong": 1, "ket_qua": [{"cong_cu": "tang-HeThong", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "dừng giữa chừng: REVIEW-SYSTEM-LAUNCH-FAILURE"}]} | {"mode": "programmer-throw", "rc": 1, "passed": true, "ok": false, "loi": 1, "tong": 1, "ket_qua": [{"cong_cu": "tang-NguoiDung", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "dừng giữa chừng: Exception calling \"Substring\" with \"1\" argument(s): \"startIndex cannot be larger than length of string. (Parameter 'startIndex')\""}]}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 1: neo exact head và bộ test bắt buộc
  giả thuyết : source không đúng SHA hoặc bộ test không đạt như executor khai.
  lệnh       : `git -C cay-kho rev-parse HEAD`; `git -C cay-kho rev-parse HEAD^{tree}`; so byte 5 tệp với `git show HEAD:<path>` và bản sao; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : HEAD=d20a69e211f24c0a4beffb1a9cdf41fdf45be531; tree=bd3bb790baa9f0e5d07417c374b77e347c0fa56b; status rỗng; 5/5 tệp byte-match blob và copies/head; `cap-nhat-cong-cu tests: 98/98 ca QUA` (rc0). SHA256 chi tiết: evidence/preflight.json.
  kết luận   : KHÔNG PHẢI LỖI trong bộ test Linux. Không suy Windows hay các hợp đồng đều đúng từ tổng 98/98.

HƯỚNG 2: chạy lại target-equality lượt 10
  giả thuyết : NLM launcher cũ hoặc HeThong current>đích còn được ghi giu/ok=true.
  lệnh       : `python3 -u probes/target-equality-oracle.py > evidence/target-equality-summary.log 2>&1` (probes sao từ luot10, product=copies/head).
  output     : `Target equality oracle: 5 / 5 PASS` (rc0). nlm-control, system-install-control, system-at-target exit0/ok=true; nlm-cli-stale exit1/loi (CLI0.4.0, metadata/index0.5.0); system-above-target exit1/ok=false/4loi (Git/gh3.0.0 so2.0.0, Node24.3.0 so24.2.0, pwsh7.7.0 so7.6.10). evidence/target-equality.json có argv và native events.
  kết luận   : KHÔNG PHẢI LỖI với ba nhóm điều kiện cụ thể này; tiếp tục đo actual pip/launcher và ZIP trước khi đóng toàn lớp.

HƯỚNG 7: NLM launcher với pip/index/metadata thật offline
  giả thuyết : đồ giả diễn sẵn version, nên việc chặn launcher cũ chưa có bằng chứng với hai interpreter thật.
  lệnh       : `python3 -u probes/real-nlm-oracle.py > evidence/real-nlm-summary.log 2>&1`.
  output     : rc0, `Real NLM stale launcher: REJECTED`. Hai venv thật cài wheel local notebooklm-mcp-cli 0.4.0/0.5.0; pip install/index và metadata của nlmPy đều rc0/0.5.0. Control CLI0.5.0 → giu/ok=true/exit0; launcher interpreter0.4.0 → loi/ok=false/exit1. evidence/real-nlm-oracle.json lưu command/rc/stdout của lời gọi thật. PIP_NO_INDEX=1/PIP_FIND_LINKS=local.
  kết luận   : KHÔNG PHẢI LỖI cho biểu hiện stale launcher lượt 10. Wheel là gói fixture có metadata/CLI tối thiểu; không tự nhận đã chạy nlm.exe Windows hay upstream NLM thật.

HƯỚNG 8: ZIP bằng/cao hơn đích, ghim và hậu kiểm
  giả thuyết : nhánh giu mới hoặc xử lý cao hơn ghim còn trái B.
  lệnh       : `python3 -u probes/zip-target-oracle.py > evidence/zip-target-summary.log 2>&1`.
  output     : `ZIP target oracle: 7/7 PASS`, rc0. rg-equal/actionlint-equal giu/exit0; rg-newer/shellcheck-newer loi/exit1; actionlint-newer cài từ3.0.0 vềghim2.0.0 và nang_cap/exit0; rg-upgrade nang_cap/exit0; rg-badpost loi/exit1. ZIP/file/copy/hash/getter thật; HTTP là bản local, chmod bù quyền Unix. evidence/zip-target-oracle.json.
  kết luận   : KHÔNG PHẢI LỖI trong bảy ca phiên bản số; đã đóng biểu hiện >= ở ZIP lượt 10. Tiếp tục kiểm normalization và toàn inventory.

HƯỚNG 9: hậu điều venv, pip rc0 chưa đủ
  giả thuyết : bản vá làm mất hậu kiểm interpreter/ghim hoặc pip dry-run được tính ĐẠT.
  lệnh       : `python3 -u probes/install-contract-oracle.py`; `python3 -u probes/real-pip-oracle.py` (log evidence/*-summary.log).
  output     : `Install contract oracle: 4/4 PASS`, `Real pip oracle: 2/2 PASS`, cả hai rc0. Control interpreter3.12.7 + PyYAML6.0.3/jsonschema4.25.1 đúng ghim giu/exit0; piprc8, interpreter sau rc9, hai gói sai ghim đều loi/exit1. Với pip THẬT trên wheel local, PIP_DRY_RUN=1 khiến install rc0 nhưng importlib.metadata hai gói rc1 → loi/exit1. PIP_NO_INDEX=1; evidence/install-contract-oracle.json và real-pip-oracle.json.
  kết luận   : KHÔNG PHẢI LỖI; biểu hiện venv lượt 9 vẫn đóng.

HƯỚNG 10: đường thứ ba — định danh phiên bản có hậu tố bị cắt trước phép bằng
  giả thuyết : đổi >= thành == chỉ so phần số; bản prerelease vẫn có thể bị coi là đúng bản stable đích.
  lệnh       : `python3 -u probes/version-identity-oracle.py > evidence/version-identity-summary.log 2>&1`.
  output     : rc0 của driver tái hiện, `Version identity: stable controls 2/2 PASS; prerelease FALSE SUCCESS 3/3 reproduced`. Sản phẩm (source byte-match head, không mutation) ở system suffix-before/suffix-after và zip-suffix-before đều exit0/ok=true. Native system in rc0 các chuỗi `git version 2.0.0-rc.7`, `gh version 2.0.0-rc.7`, `v24.2.0-rc.7`, `7.6.10-rc.7`; trước cài được giu, sau installer fixture rc0 được nang_cap, đích đều bản số không hậu tố. ZIP qua Invoke-TangNguoiDung thật: raw `ripgrep 1.0.0-rc.7`, `version: 1.0.0-rc.7`, `1.7.7-rc.7` đều thành giu1.0.0/1.7.7; cả11 dòng ĐẠT. evidence/version-identity-oracle.json giữ stdout gốc, rc, dòng kết quả và main-tail JSON.
  kết luận   : LỖI P1 cùng lớp loi-native-tang-nguoi-dung theo B. Compare-PhienBan dùng regex prefix không neo cuối; các regex caller ZIP/gh/node/pwsh còn bỏ hậu tố ngay ở getter. Control stable vẫn đạt. Chưa khẳng định các bản prerelease này đang cài trên VM hay các version fixture tồn tại trên upstream; đây là phản ứng đo được với output native hợp lệ ở rc0. HTTP/installer/task là mô hình offline; không nhận là Windows thật.

HƯỚNG 11: kiểm răng test mới và provenance HINT lượt 10
  giả thuyết : năm ca mới không phân biệt được việc bỏ điều kiện NLM/ZIP/HeThong, hoặc HINT không được áp nguyên văn.
  lệnh       : `python3 -u probes/review11-mutations.py > evidence/review11-mutations-summary.log 2>&1`; `python3 probes/build-review11-hint.py > evidence/hint-build.log 2>&1`.
  output     : `Review11 mutations: 9 / 9 KILLED`, rc0. Ba mutant r10-nlm-without-cli-equality / r10-zip-keeps-above / r10-system-keeps-above đều 97/98, rc1, đúng ca mới tương ứng đỏ, không ParserError. Sáu mutant còn lại bỏ hậu điều venv, target NLM, rc query, rc metadata, rc getter và lưới catch main đều đỏ có tên ca thật. Áp nguyên văn luot10/HINT.patch vào tệp test lấy từ Git blob d005cf4… rồi so byte với head hiện tại → `Round10 HINT verbatim matches reviewed test: True`.
  kết luận   : KHÔNG PHẢI LỖI về răng của test mới ở ba biểu hiện cũ. Đây là 9 mutant reviewer tự đo tại head này; KHÔNG khai đã đo lại đủ 33 mutant executor nêu. Các control bằng đích và ca số cao hơn có mô hình native thật, download bị chặn, không dựng trước kết quả cuối. Chưa khóa hậu tố phiên bản (H10/H13).

HƯỚNG 12: kiểm độc lập oracle băm/caller và catch/continue/skip
  giả thuyết : driver cũ rc0 chỉ vì không assert; catch nuốt lỗi lập trình thành ĐẠT hoặc test không đo được vẫn đếm qua.
  lệnh       : `python3 probes/audit-regression-results.py`; `pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/audit-source.log 2>&1`; `pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory.json`; đọc trọn source/test/README, tìm catch/continue/bo_qua.
  output     : `Independent regression assertions: 26 / 26 PASS`, rc0, xác nhận lại hành vi từ JSON system-matrix/caller-null, không chỉ rc driver. AST parse_errors=0, Add-KetQua=50, khác loi=19; 102 tên Ca tĩnh,102 duy nhất,98 ca thực chạy Linux. `README_native_acl_commands=0`; runtime không có Add-KetQua bo_qua. Main-tail control exit0; user/system/programmer throw exit1/ok=false/loi1 với exception trong JSON. evidence/regression-assertions.json và regressions-round10.json.
  kết luận   : KHÔNG PHẢI LỖI mới ở catch/continue hoặc cơ chế đếm skip đã kiểm. Get-PhienBanLenh/Get-PhienBanGoi/Get-BanMoiNhat catch cả lỗi lập trình rồi trả null; caller chặn thành loi, không suy thành ĐẠT. Catch từng công cụ/main ghi loi; catch status NLM giữ rc/mode chưa hợp lệ nên cuối vẫn loi; catch OutputEncoding rỗng không phát kết quả công cụ. Continue trong try của vòng pip chỉ sau ghi kiem/loi; HeThong chỉ sau dòng đã phân loại, finally vẫn dọn tải. PyYAML bootstrap không kiểm rc riêng nhưng Read-BanGhim + dòng gói chính thức vẫn phải đạt hậu điều; không có suy thành công chỉ từ rc bootstrap. Ca thiếu Python/PyYAML đỏ; ca Windows admin không đo được mã3 trả false; Linux-only nằm ngoài nhánh nền nên không có trong mẫu số Windows. Test ACL có mô hình trạng thái owner/grant và tệp thật, nhưng chỉ đến sentinel trước mật khẩu/COM, không được tính là đo full đăng ký Windows. Các regex test tĩnh giữ vai trò giới hạn, không dùng thay phép đo hành vi.

HƯỚNG 13: mở rộng phản chứng CLI npm và HINT test-only A/B
  giả thuyết : chỉ Compare-PhienBan sai, còn các caller so chuỗi trực tiếp của npm không bị mất định danh; test thêm không phân biệt được bản vá.
  lệnh       : `python3 -u probes/cli-version-identity-oracle.py > evidence/cli-version-identity-summary.log 2>&1`; `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/hint-head.log 2>&1`; cùng lệnh trên hint-prototype/ (evidence/hint-prototype.log).
  output     : `CLI identity: stable control PASS; prerelease FALSE SUCCESS reproduced`, rc0 driver. Control CLI1.0.0 → giu/ok=true/exit0; direct CLI --version in1.0.0-rc.7/rc0 + npm view1.0.0/rc0 và npm installrc0 → cả claude/codex vẫn giu1.0.0, ok=true/exit0. Head+HINT **98/101**, rc1: đúng nd_cli_hau_to_khong_duoc_coi_la_stable_dich / nd_portable_hau_to_khong_duoc_coi_la_stable_dich / dich_he_thong_hau_to_khong_duoc_coi_la_stable_dich đỏ. Prototype scratch+HINT **101/101**, rc0; prototype giữ toàn token ở regex caller và neo cuối parser numeric, không sửa cây review.
  kết luận   : LỖI P1 được khóa độc lập cả ở so chuỗi npm lẫn so [version] ZIP/HeThong. HINT chỉ sửa TEST, chạy Update-CongCuZip thật trong ca portable (không dùng zip-gia ở ca đó), giữ control stable và chặn tải. Prototype chỉ là witness chứng minh phân biệt, chưa là phương án production đã kiểm đủ định dạng upstream/Windows.

## KIỂM TOÀN BỘ ĐIỂM Add-KetQua KHÁC loi

HƯỚNG 14: audit đủ 19/19 điểm ghi kết quả
  giả thuyết : còn điểm phát ĐẠT/kiem khác ngoài các nhánh probe đã kể, hoặc bỏ sót action động trong AST.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory.json`; đối chiếu từng command AST với source exact head và các oracle H2–13.
  output     : parse_errors=0; add_count=50; nonloi_count=19. Đủ 19 dòng dưới đây, gồm action là subexpression if (không chỉ literal giu). Bản ghi full command/function/line trong evidence/inventory.json.
  kết luận   : LỖI P1 theo B ở các điểm mất hậu tố nêu trong bảng; không phát hiện vi phạm A mới. Dấu “đạt A” chỉ xác nhận rc0+khớp mẫu của phiên bản đang cài, không chứng nhận parser giữ đủ định danh để đạt B.

A = khi ChiKiem, mọi dòng khác loi phải có phiên bản đang cài đo được. B = khi cài thật, giu/nang_cap/cai_moi chỉ đạt khi phiên bản sau đo được bằng đúng đích (ngoại lệ prompt). Tất cả dòng thuộc `ops/vm/cap-nhat-cong-cu.ps1` tại reviewed_sha.

| Dòng / hàm | Action / phạm vi | Kiểm A | Kiểm B / bằng chứng |
| --- | --- | --- | --- |
| 354 Update-CongCuZip | giu; rg/shellcheck/actionlint | Đạt: getter rc0+match, guard348 chặn null trong ChiKiem; portable-check4/4. | **Chưa đạt**: Compare-PhienBan chỉ so prefix, và caller457–459 đã cắt hậu tố. H8 số đúng7/7; H10/H13 prerelease khác stable vẫn giu. |
| 356 Update-CongCuZip | can_cap_nhat | Đạt: chỉ ChiKiem, guard348 có truoc đo được; H3 portable missing/rc9 lỗi, outdated báo cập nhật. | Không phải action thành công cài thật; nhánh return trước tải. |
| 371 Update-CongCuZip | nang_cap/cai_moi | Không chạy khi ChiKiem (356 return). | **Chưa đủ**: sau getter phải Compare==0 (:370), nhưng numeric prefix/hậu tố bị bỏ cũng được bằng. Lập luận tĩnh chắc chắn cùng parser/caller H10; H8 badpost số khác bị chặn, caller-matrix post-rc9 bị chặn. |
| 389 Invoke-TangNguoiDung | python giu | Đạt: pyTruoc đo rc0+match tại387; thiếu/hỏng return loi. user-version3/3 và baseline. | Ngoại lệ có chủ ý của prompt: Python chỉ báo, không nâng. |
| 404 Invoke-TangNguoiDung | pip/PyYAML/jsonschema kiem | Đạt: Get-PhienBanGoi rc0+pattern, nhánh403 ghi loi khi null; new-paths6/6. | Chỉ ChiKiem; không phải kết quả cài thật. |
| 412 Invoke-TangNguoiDung | pip/PyYAML/jsonschema giu/nang_cap | Không chạy ChiKiem vì405 continue. | Đạt trong hợp đồng: install rc0; sau metadata rc0+pattern; exact string==ghim hoặc pip index (rc0+match) tại409–411. H11 bỏ rc metadata/query/target bị test bắt; H13 không ảnh hưởng metadata. |
| 421 Invoke-TangNguoiDung | venv-kho kiem | Đạt: getter python rc0+match; null ghi loi. third-paths6/6, missing/rc9/cannot-start đều lỗi. | Chỉ ChiKiem. |
| 434 Invoke-TangNguoiDung | venv-kho giu | Không chạy ChiKiem. | Đạt: pip rc0, python sau rc0+match, PyYAML/jsonschema sau metadata rc0 và bằng ghim. H9 fixture4/4, actual pip2/2; mutant bỏ hậu điều đỏ. Không nhận đã kiểm mọi requirement ngoài hợp đồng prompt. |
| 445 Invoke-TangNguoiDung | claude/codex kiem | Đạt A: getter rc0+regex; không có npm hoặc CLI không đo được → loi. user/native/new-paths oracle. | Chỉ ChiKiem; regex prefix không đủ cho B ở nhánh khác. |
| 453 Invoke-TangNguoiDung | claude/codex giu/nang_cap/cai_moi | Không chạy ChiKiem vì446 continue. | **Chưa đạt**: dù installrc0/queryrc0 và so chuỗi đúng tại452, getter450 đã biến1.0.0-rc.7 thành1.0.0. H13 exact head native/JSON false success cả2 CLI. |
| 471 Invoke-TangNguoiDung | nlm kiem | Đạt: nlmPy phải có, getter CLI rc0+match; null → loi. prerequisite4/4, user-version3/3. | Chỉ ChiKiem. |
| 493 Invoke-TangNguoiDung | nlm giu/nang_cap | Không chạy ChiKiem. | Đạt cho điều kiện đang review: piprc0; CLI rc0+token đầy đủ; metadata rc0+pattern; cảhai==pip index rc0+match; statusrc0/JSONmode=file. H2/H7 stale launcher bị chặn, control được nhận; status lỗi/JSON hỏng/keyring bị chặn. |
| 530 Invoke-TangHeThong | node-major can_quyet_dinh | Đạt: ChiKiem guard518 bắt null; trước đó đã đo node rc0+match. system-check6/6. | Ngoại lệ Node major mới theo prompt, không tuyên bố đã nâng. |
| 532 Invoke-TangHeThong | node can_quyet_dinh khi major không còn LTS | Đạt trong ChiKiem nhờ guard518; system-no-lts có truoc24.1.0/rc0. | Nhánh dừng xin quyết định, không phải giu/nang_cap/cai_moi; không dùng như bằng chứng đã cài bản đích. |
| 546 Invoke-TangHeThong | giu; Git/gh/node/pwsh | Đạt A: guard518 và Test-CoTheCai chặn tệp có nhưng getter lỗi. | **Chưa đạt B**: ss==0 sau khi mất hậu tố, H10 suffix-before exit0; H2 at-target và above-target số phân biệt đúng. |
| 548 Invoke-TangHeThong | can_cap_nhat | Đạt: guard518, getter đo trước; system-check6/6 và native events. | Chỉ ChiKiem; continue trước tải/cài. |
| 562 Invoke-TangHeThong | can_khoi_dong_lai | Không chạy ChiKiem vì548 continue. | Ngoại lệ MSI3010 theo prompt. H5 MSI-reboot: gh/node/pwsh đều đúng action, không đòi version có hiệu lực trước reboot. |
| 564 Invoke-TangHeThong | nang_cap/cai_moi | Không chạy ChiKiem. | **Chưa đạt**: Install rc0 và getter sau rc0 chưa đủ nếu Compare563 bỏ hậu tố; H10 suffix-after vẫn nang_cap/exit0. H5 post-version-wrong số khác và caller postrc9 đều lỗi. |
| 576 Invoke-TangHeThong | commander khoi_dong_lai | Không thể chạy từ lượt ChiKiem chuẩn: DaCaiNode khởi tạo false, chỉ đặt true sau548, ngay trước cài Node. | Dòng trạng thái ScheduledTask, không thuộc ba action B; đọc lại State==Running tại574–575, catch lỗi thành loi. H5 success/install-failure/reboot vẫn thử dựng Commander; ScheduledTask thật KHÔNG ĐO ĐƯỢC. |

### loi-native-tang-nguoi-dung  [P1]  Bằng phần số vẫn có thể ghi ĐẠT cho bản prerelease khác đích stable

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:69` (parser lấy prefix); `:442`, `:450` (regex CLI npm); `:457`–`:459` (caller ZIP); `:512`–`:515` (regex HeThong); điểm phát ĐẠT `:354`, `:371`, `:453`, `:546`, `:564`.

VẤN ĐỀ: Ba biểu hiện cụ thể lượt10 đã vá thật, nhưng predicate “bằng đích” còn nhận kết quả sau khi bỏ phần định danh. `ConvertTo-PhienBan` không neo cuối nên2.0.0-rc.7 và2.0.0 cùng thành [version]2.0.0; các regex CLI npm/ZIP/gh/node/pwsh lấy luôn chỉ x.y.z trước khi so. Kết quả có thể là giu hoặc nang_cap dù native --version rc0 báo prerelease khác stable đích. Ví dụ actionlint raw1.7.7-rc.7 bị ghi giu1.7.7 khi ghim1.7.7. CLI npm raw1.0.0-rc.7 bị ghi giu1.0.0 khi npm view trả1.0.0 và install không đổi launcher. Ở nhánh cài HeThong, installer fixture rc0, raw sau vẫn-rc.7 mà main báo ok=true/exit0. Đó là hành vi sai đo được theo B, không chỉ thiếu test. Giữ một slug lớp cũ, không nhân finding theo từng công cụ. Không có bằng chứng ba hunk vá mới gây ra parser lỗi; đây là đường còn sót trong lớp, mới phát hiện lượt11.

ĐÃ THỬ NGHIỆM: `python3 -u probes/version-identity-oracle.py` → stable controls2/2, false success prerelease3/3; `python3 -u probes/cli-version-identity-oracle.py` → stable control đạt, prerelease của cảhai CLI vẫn ok=true/exit0, direct-after rc0/raw1.0.0-rc.7. Hai driver rc0 là xác nhận TÁI HIỆN lỗi, không phải xác nhận hợp đồng đạt; product rc0/JSON ok=true là phần sai. Source product không mutation, getter/caller/Compare/main-tail thật; chỉ HTTP/installer/task và package-manager fixture là offline. HINT test-only: head98/101 rc1 (đúng3 ca mới đỏ), scratch witness101/101 rc0; toàn98 ca cũ còn qua. Output đầy đủ: evidence/version-identity-oracle.json, cli-version-identity-oracle.json, hint-head.log, hint-prototype.log.

ĐỘ TIN: cao về vi phạm hậu điều tại head trước các output đã đo; trạng thái VM/upstream release/Windows native chưa đo. Không khẳng định đã tìm thấy bản prerelease tương ứng trên VM.

GỢI Ý VÁ — đủ bốn phần:
- **Ở đâu:** parser69, toàn regex caller ghi lại phiên bản (442/450/457–459/512–515), rồi giữ chốt bằng đích trước cả5 điểm phát thành công nêu trên.
- **Cách vá:** giữ nguyên định danh version có nghĩa khi lấy từ CLI, chỉ chuẩn hoá các biến thể đã chứng minh tương đương của từng công cụ (vd v đầu chuỗi và dạng Git `.windows.N`). So thứ tự số cho chính sách nâng/hạ tách khỏi phép xác nhận bằng đích. Nếu chưa hỗ trợ prerelease/suffix thì từ chối rõ thành loi; đừng bỏ suffix để nhận như stable. Không chỉ neo cuối ConvertTo-PhienBan vì một số caller đã cắt suffix trước khi parser được gọi; cũng phải giữ chốt npm so exact target từ npm view rc0.
- **Ca khóa:** stable=current và nâng đúng stable vẫn qua; prerelease cùng x.y.z khác đích stable phải lỗi hoặc thực sự cài về đúng đích rồi hậu kiểm; kiểm cả giu trước cài và hậu kiểm sau installrc0, cả npm/ZIP/HeThong, actionlint có ghim, Git Windows bốn thành phần, Node policy major và MSI3010. Ba ca HINT có control cũ và oracle H10/H13 chạy được; executor tự tái dẫn xuất và bổ sung ca hậu cài trên Windows.
- **Rủi ro vá:** neo regex quá chặt có thể từ chối định dạng Git Windows, output nhãn của từng CLI hoặc metadata build hợp lệ; [version] không mô hình đầy đủ SemVer. Không đổi thành tự hạ major khi gặp prerelease/phiên bản chưa biết, không làm mất ngoại lệ quyết định Node/reboot. Prototype chỉ chọn fail-closed để làm witness; không dùng nó như production patch đã duyệt.

`HINT.patch`: chỉ tệp `ops/vm/cap-nhat-cong-cu_test.ps1`, định dạng `patch -p0` từ gốc bản sao cay-kho/. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Nếu dùng, executor khai hint_provenance theo protocol. Đã áp và chạy trong hint-validation/; prototype runtime nằm riêng trong scratch, KHÔNG nằm trong HINT.

Reviewer: Codex, provider OpenAI, model family GPT-6 theo chỉ thị phiên (không có API xác minh model triển khai); execution_surface=API agent có shell Linux; transport=machine/local; session=runs/aef7f0df; github_submitter_identity=null. Authority là chỉ thị trực tiếp trong prompt.snapshot/PROMPT.md; review class=sensitive; write set chỉ artifact ngoài cay-kho/. Không xét ops/land/pr1065-*, không push/merge/land/mạng. Skill cloud-environment-runtime đã đọc; không có environment_status trong toolset nên không gọi hoặc suy readiness.

Giới hạn: NTFS junction/effective ACL/icacls Windows, ScheduledTask/COM/credential, msiexec, launcher .exe/.cmd và Commander thật trên Windows ở d20a69e… **KHÔNG ĐO ĐƯỢC** từ môi trường Linux này. Source/fixture/JSON không thay thế các phép đo ấy. Kết quả Windows ở SHA cũ và khai báo executor không được dùng làm bằng chứng chạy lại tại head hiện tại. Không có P0 mới được chứng minh; không tái mở giao-acl-theo-junction chỉ vì thiếu Windows.

HƯỚNG 15: quét bổ sung toàn bộ absence/metadata và lỗi native còn lại lượt 5–7
  giả thuyết : bộ regression gộp bỏ sót nhánh prerequisite/metadata rỗng, launcher không chạy hoặc lỗi status làm rò HOME.
  lệnh       : `python3 -u probes/absence-oracle.py > evidence/absence-summary.log 2>&1`; `python3 -u probes/run-user-extra.py > evidence/user-extra-summary.log 2>&1`; `python3 probes/audit-extra-regressions.py`.
  output     : cảhai driver rc0; `Extra regression assertions: 21 / 21 PASS`, rc0. Absence9 ca: control exit0/0loi; thiếu CLI2loi, từng kiểu thiếu NLM/venv1loi, metadata rỗng/rác3loi, đều exit1; ChiKiem0install. metadata-recover: pip/PyYAML/jsonschema đọc lần đầu lỗi rồi sau cài đo được → nang_cap; venv/NLM bị lần đo metadata đầu của chính interpreter đó lỗi →2loi/exit1 đúng fail-closed. User-extra12 ca đều không thoát hàm,11 dòng và profile_restored=true; control/check-only0loi; npm-cannot-start/CLI-version-stderr-fails2loi; py-disappears3loi; pip/venv/NLM pip/launcher/status JSON/mode/native-rc hỏng mỗi ca1loi. JSON: evidence/absence-oracle.json, user-extra.json, extra-regression-assertions.json.
  kết luận   : KHÔNG PHẢI LỖI mới ở các nhánh này. Hai driver cũ chỉ thu dữ liệu, vì thế đã thêm assertion độc lập, không gọi rc0 driver là hợp đồng đạt. ZIP/Set-Path được stub trong nhóm user-extra; không dùng chúng để chứng nhận ZIP (H8/H10/H13 đã gọi thật).

HƯỚNG 16: kiểm cuối exact SHA, nguồn read-only và artifact tái tạo được
  giả thuyết : probe đo source khác head, cây review bị thay đổi, hoặc HINT không khớp bản đã chạy.
  lệnh       : `python3 probes/final-audit-review11.py > evidence/final-audit.log 2>&1` (rc0; đã chạy lại sau regression bổ sung).
  output     : HEAD=d20a69e211f24c0a4beffb1a9cdf41fdf45be531; tree=bd3bb790baa9f0e5d07417c374b77e347c0fa56b; git status tracked/untracked/ignored rỗng; diff/index/diff--check rc0. shallow=false; core.abbrev=7; 5/5 tệp cây thật/Git blob/preflight/copies trùng byte. PROMPT.md=snapshot sha256 f39a2cbe83350d15ca2fca18e7842dae72c39e8486e1a9ef77070af6ce9785f5. HINT sha256 3383861346bbfbbe62ab637424fda79d2e2bf34f2b5f4cac429c42bfd80d513d; chỉ tệp TEST; patch -p0 dry-run/apply rc0; matches_tested=true. Baseline98/98; HINT trên head98/101, witness101/101;9/9 mutant bị bắt; inventory19/19. Chi tiết evidence/final-audit.json.
  kết luận   : KHÔNG PHẢI LỖI về nguồn/artifact ở mốc kiểm. Không sửa cây review, không gọi mạng/push/merge. Mọi thay đổi fixture/test/prototype/mutant nằm ngoài cay-kho/.

Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

**changes_requested** tại d20a69e211f24c0a4beffb1a9cdf41fdf45be531. Ba biểu hiện cụ thể lượt10 đã đóng bằng phép đo thật (target5/5, NLM actual-pip2/2, ZIP7/7), nhưng lớp `loi-native-tang-nguoi-dung` còn mở theo B: mất hậu tố khiến prerelease được nhận là bản stable đích ở CLI npm/ZIP/HeThong. Bộ test bắt buộc Linux98/98 không khóa ca này; HINT thêm3 ca làm head98/101, witness101/101. Đã rà19/19 điểm Add-KetQua khác loi và kiểm catch/continue/skip, không có finding độc lập khác được chứng minh. Chưa đo Windows thật tại head này. Ngưỡng prompt áp dụng: P0/P1/P2 chặn approve, P3 không chặn; verdict nội dung không cấp quyền land.
