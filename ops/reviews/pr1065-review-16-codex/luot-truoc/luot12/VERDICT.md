verdict: changes_requested
reviewed_sha: b667da802074788c5b84ef21a3b91234e3f08b94

## ĐÓNG FINDING LƯỢT 11

| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | **Chưa đóng toàn bộ**; đã đóng phản chứng suffix-vs-stable L11. | `python3 probes/audit-identity-round12.py` → 7/7 PASS (3 control, 4 ca suffix bị từ chối đúng); `python3 -u probes/cli-case-identity-oracle.py` → CLI1.0.0-rc.a khác npm view1.0.0-rc.A vẫn giu/ok=true/exit0 ở cả claude/codex. Chi tiết H3/H11. |

Bản sao `copies/head/` nguyên byte tại SHA này; không sửa `cay-kho/`, không gọi mạng. Phép đo Windows thật tại head hiện tại: **KHÔNG ĐO ĐƯỢC** trong môi trường Linux. Lời khai executor và bằng chứng tại SHA cũ không được dùng thay phép đo hiện tại.

## BẢNG SĂN

Khởi tạo nhật ký; sẽ nối bằng chứng sau mỗi hướng thử.

HƯỚNG 1: neo nguồn và bản sao độc lập
  giả thuyết : source có thể sai SHA hoặc bản sao không khớp.
  lệnh       : `git -C cay-kho rev-parse HEAD`; `git -C cay-kho status --porcelain`; so byte 5 tệp cây thật/Git blob/copies/head (evidence/preflight.json).
  output     : {"head": "b667da802074788c5b84ef21a3b91234e3f08b94", "tree": "28a788beaff8a31bda4ed1c1ded9697805bcd052", "status": "", "matches": {"ops/vm/README.md": true, "ops/vm/cap-nhat-cong-cu.ps1": true, "ops/vm/cap-nhat-cong-cu_test.ps1": true, "ops/cong_cu.yaml": true, "requirements.txt": true}}
  kết luận   : KHÔNG PHẢI LỖI. Năm tệp trùng byte; cây review chỉ đọc.

HƯỚNG 2: bộ test bắt buộc trên cây review
  giả thuyết : bản vá hoặc fixture mới gây hồi quy trong bộ test chính thức.
  lệnh       : `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1`.
  output     : `cap-nhat-cong-cu tests: 102/102 ca QUA`; mã thoát 0.
  kết luận   : KHÔNG PHẢI LỖI trong bộ test chính thức trên Linux. Không suy thành Windows đạt; sẽ kiểm răng bằng đột biến riêng.

HƯỚNG 7: đăng ký lịch, ACL và reparse
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/registration-head.py` (qua `python3 probes/rerun-regressions.py`).
  output     : registration-head: rc0, {"mode": "install-ancestor-link", "passed": true, "rc": 0, "error": "t\u1eeb ch\u1ed1i: /tmp/review-register-0cbf36646bb44a12b7dd9727a2a15e12/PF/tra-luat-ops c\u00f3 reparse point (junction/symlink): /tmp/review-register-0cbf36646bb44a12b7dd9727a2a15e12/PF", "icacls_count": 0, "tool_acl_calls": 0, "audit_count": 0, "tasks": 0} | {"mode": "install-child-link", "passed": true, "rc": 0, "error": "t\u1eeb ch\u1ed1i: /tmp/review-register-65cfb50a5ce44dd89d5daada3d70e238/PF/tra-luat-ops c\u00f3 reparse point (junction/symlink): /tmp/review-register-65cfb50a5ce44dd89d5daada3d70e238/PF/tra-luat-ops/link", "icacls_count": 0, "tool_acl_calls": 0, "audit_count": 0, "tasks": 0}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 6: băm, cài HeThong, hậu kiểm và reboot
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/system-matrix.py`; `python3 -u probes/caller-matrix.py` (qua `python3 probes/rerun-regressions.py`).
  output     : system-matrix: rc0, {"mode": "msi-reboot", "rc": 0, "error": null, "spawns": 4, "verified": true, "left": 0, "restart": true, "rows": [["git", "nang_cap"], ["gh", "can_khoi_dong_lai"], ["node", "can_khoi_dong_lai"], ["pwsh", "can_khoi_dong_lai"], ["commander", "khoi_dong_lai"]]} | {"mode": "post-version-wrong", "rc": 0, "error": null, "spawns": 4, "verified": true, "left": 0, "restart": true, "rows": [["git", "loi"], ["gh", "loi"], ["node", "loi"], ["pwsh", "loi"], ["commander", "khoi_dong_lai"]]}; caller-matrix: rc0, {"mode": "zip-pre", "rc": 0, "data": {"mode": "zip-pre", "spawns": 0, "http_fixture_calls": 1, "results": [{"cong_cu": "rg", "truoc": "", "sau": "2.0.0", "hanh_dong": "cai_moi", "chi_tiet": ""}], "errors": 0}} | {"mode": "zip-post", "rc": 0, "data": {"mode": "zip-post", "spawns": 0, "http_fixture_calls": 1, "results": [{"cong_cu": "rg", "truoc": "1.0.0", "sau": "", "hanh_dong": "loi", "chi_tiet": "sau khi cài đo được '', mong '2.0.0'"}], "errors": 1}}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 4: ChiKiem và prerequisite trên cả hai tầng
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/third-paths-oracle.py`; `python3 -u probes/portable-check-oracle.py`; `python3 -u probes/system-check-oracle.py`; `python3 -u probes/absence-regression-oracle.py` (qua `python3 probes/rerun-regressions.py`).
  output     : third-paths-oracle: rc0, {"mode": "venv-cannot-start", "passed": true, "rc": 1, "ok": false, "errors": 1, "rows": 11, "venv": "loi", "direct_probe": {"path": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr12-pr1065.1Syt/fixtures/third-venv-cannot-start/venv/Scripts/python.exe", "exists": true, "rc": null, "error": "Cannot run a document in the middle of a pipeline: /tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr12-pr1065.1Syt/fixtures/third-venv-cannot-start/venv/Scripts/python.exe.", "output": ""}, "venv_native_calls": 0, "installs": 7} | Venv runtime oracle: 6/6 PASS; portable-check-oracle: rc0, {"mode": "check-zip-rc9", "passed": true, "rc": 1, "ok": false, "errors": 3, "rows": 11, "portable": {"rg": {"cong_cu": "rg", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr12-pr1065.1Syt/fixtures/check-zip-rc9/Tools/bin/rg.exe chưa cài hoặc không đọc được phiên bản"}, "shellcheck": {"cong_cu": "shellcheck", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr12-pr1065.1Syt/fixtures/check-zip-rc9/Tools/bin/shellcheck.exe chưa cài hoặc không đọc được phiên bản"}, "actionlint": {"cong_cu": "actionlint", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr12-pr1065.1Syt/fixtures/check-zip-rc9/Tools/bin/actionlint.exe chưa cài hoặc không đọc được phiên bản"}}, "installs": 0} | Portable ChiKiem oracle: 4/4 PASS; system-check-oracle: rc0, {"mode": "system-no-lts", "passed": true, "rc": 0, "ok": true, "errors": 0, "rows": [["git", "can_cap_nhat", "1.0.0"], ["gh", "can_cap_nhat", "1.0.0"], ["node-major", "can_quyet_dinh", "24.1.0"], ["node", "can_quyet_dinh", "24.1.0"], ["pwsh", "can_cap_nhat", "7.6.9"]], "native_calls": 4, "native_rcs": [0, 0, 0, 0]} | System ChiKiem oracle: 6/6 PASS; absence-regression-oracle: rc0, {"mode": "check-missing-nlm-all", "passed": true, "rc": 1, "ok": false, "nlm": "loi", "errors": 1} | NLM prerequisite oracle (head): 4/4 PASS
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 5: native/catch/continue và lưới nhật ký lượt 4–7
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/l4-user-oracle.py`; `python3 -u probes/user-oracle.py`; `python3 -u probes/user-version-oracle.py`; `python3 -u probes/new-paths-oracle.py`; `python3 -u probes/run-main-tail.py` (qua `python3 probes/rerun-regressions.py`).
  output     : l4-user-oracle: rc0, PASS nlm-status-fails | User native error oracle: 3/3 PASS; user-oracle: rc0, PASS nlm-status-fails | User native error oracle: 3/3 PASS; user-version-oracle: rc0, PASS nlm-version-fails | Version native failure oracle: 3/3 PASS; new-paths-oracle: rc0, {"mode": "check-metadata", "passed": true, "rc": 1, "chi_kiem": true, "loi": 3, "ok": false, "tong": 11} | Remaining native paths oracle: 6/6 PASS; run-main-tail: rc0, {"mode": "system-throw", "rc": 1, "passed": true, "ok": false, "loi": 1, "tong": 1, "ket_qua": [{"cong_cu": "tang-HeThong", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "dừng giữa chừng: REVIEW-SYSTEM-LAUNCH-FAILURE"}]} | {"mode": "programmer-throw", "rc": 1, "passed": true, "ok": false, "loi": 1, "tong": 1, "ket_qua": [{"cong_cu": "tang-NguoiDung", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "dừng giữa chừng: Exception calling \"Substring\" with \"1\" argument(s): \"startIndex cannot be larger than length of string. (Parameter 'startIndex')\""}]}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 3: đóng phản chứng định danh phiên bản lượt 11
  giả thuyết : prerelease cùng x.y.z vẫn bị nhận là đích stable ở CLI/ZIP/HeThong, trước hoặc sau cài.
  lệnh       : `python3 -u probes/version-identity-oracle.py > evidence/version-identity-summary.log 2>&1`; `python3 -u probes/cli-version-identity-oracle.py > evidence/cli-version-identity-summary.log 2>&1`; `python3 probes/audit-identity-round12.py`.
  output     : hai driver cũ rc1/AssertionError vì chúng assert FALSE SUCCESS còn tái hiện. Dữ liệu mới: stable-control (4 công cụ HT), zip-control (3 portable), cli-stable-control (2 CLI) đều ok=true/exit0/giu; suffix-before HT (4), suffix-after HT (4), zip-suffix-before (3), cli-suffix (2) đều ok=false/exit1, mọi dòng đích là loi. Getter giữ token -rc.7; sau installer fixture rc0 nhưng token sai vẫn loi. Assertion độc lập: Identity contract 7/7 PASS, stable controls 3/3, rejected suffix cases 4/4. JSON: evidence/version-identity-oracle.json, cli-version-identity-oracle.json, identity-assertions.json.
  kết luận   : KHÔNG PHẢI LỖI đối với phản chứng cụ thể lượt 11. Không lấy rc1 của driver cũ làm lỗi sản phẩm; không lấy mô hình HTTP/installer làm bằng chứng cài Windows thật.

HƯỚNG 8 (đang mở rộng): kiểm tương tác parser mới với chốt major Node
  giả thuyết : phiên bản Node có hậu tố giờ thành null ở parser nhưng vẫn là chuỗi khác rỗng ở Test-CoTheCai; Select-NodeLts nhận null như chưa cài và chọn major mới.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/node-major-unknown.ps1 -Mode node-prerelease -Log "$PWD/evidence/node-major-prerelease.json" -FixtureRoot "$PWD/fixtures/node-prerelease" > evidence/node-major-prerelease.log 2>&1`.
  output     : native trước `v24.1.0-rc.7` rc0; index offline có 26.2.0 + 24.2.0; product ghi `node 24.1.0-rc.7 -> 26.2.0 nang_cap`, KHÔNG có dòng node-major/can_quyet_dinh; `TONG: 5/5 dat · loi 0`, exit0. Installer/task/HTTP là mô hình offline, không cài Windows.
  kết luận   : LỖI P1 sơ bộ: tự đổi major trái chính sách Select-NodeLts. Đây là biểu hiện quay lại của node-khong-doc-duoc-van-nang-major lượt 1 dưới input mới; cần đo A/B head trước và control stable/build trước khi chốt.

HƯỚNG 9: hợp đồng cài, đích và native venv/NLM
  giả thuyết : rc0 nhưng không cài, thiếu ghim, launcher cũ hoặc cao hơn đích vẫn được ĐẠT.
  lệnh       : `python3 -u probes/run-contracts-round12.py` (gọi các driver riêng liệt kê trong evidence/contracts-round12.json).
  output     : target-equality-oracle: rc0, Target equality oracle: 5 / 5 PASS; zip-target-oracle: rc0, ZIP target oracle: 7/7 PASS; install-contract-oracle: rc0, Install contract oracle: 4/4 PASS; real-pip-oracle: rc0, Real pip oracle: 2/2 PASS; real-nlm-oracle: rc0, Real NLM stale launcher: REJECTED; absence-oracle: rc0, {"mode": "metadata-recover", "rc": 1, "ok": false, "errors": 2, "rows": 11, "actions": {"python": "giu", "pip": "nang_cap", "PyYAML": "nang_cap", "jsonschema": "nang_cap", "venv-kho": "loi", "claude": "giu", "codex": "giu", "rg": "giu", "shellcheck": "giu", "actionlint": "giu", "nlm": "loi"}, "installs": 8}; run-user-extra: rc0, {"mode": "nlm-version-fails", "rc": 0, "error": null, "errors": 1, "rows": 11, "restored": true, "last": {"cong_cu": "nlm", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "pip rc=0 "}, "native_installs": 8}
  kết luận   : KHÔNG PHẢI LỖI trong bộ oracle này. Pip thật chạy với PIP_NO_INDEX=1 trên wheel local tự tạo; HTTP/npm là fixture. Không chứng nhận gói upstream/Windows.

HƯỚNG 10: Node major A/B với phiên bản stable, prerelease, build và hỏng
  giả thuyết : hồi quy do parser mới, không phải mô hình installer diễn sẵn kết quả.
  lệnh       : `python3 -u probes/node-major-oracle.py > evidence/node-major-summary.log 2>&1`. Cùng native fixture (log stdout/rc), cùng index offline 26.2.0/24.2.0, Start-Process ghi installer/argv và đổi trạng thái file; source head và Git blob d20a69e đặt ngoài kho.
  output     : head stable24.1.0 -> node-major can_quyet_dinh26.2.0 + nang_cap24.2.0/exit0; head prerelease24.1.0-rc.7 và build24.1.0+build.1 -> nang_cap26.2.0/exit0/ok=true, KHÔNG có can_quyet_dinh, installer node-v26.2.0-x64.msi; garbage -> loi/exit1/không gọi installer Node. Cùng prerelease trên head trước -> can_quyet_dinh26.2.0 + nang_cap24.2.0/exit0. `Node major A/B: 5/5 observations asserted; head suffixes 2/2 AUTO MAJOR 24 -> 26; previous head stays 24`. evidence/node-major-oracle.json.
  kết luận   : LỖI P1 chắc chắn ở head hiện tại: thay parser khiến giá trị không rỗng nhưng không chuyển được thành [version] đi qua guard, rồi bị coi là chưa cài. L1 đã chỉ lớp chốt Node không đọc được nhưng chỉ khóa null/rỗng; nay có input suffix mà L11 mới giữ đầy đủ. Không gọi đó là lỗi Windows installer đã đo. Đây là lỗi chính sách trước khi gọi installer, không phải lỗ băm/quyền SYSTEM.

HƯỚNG 11: định danh đầy đủ qua nhánh so chuỗi npm, chỉ khác HOA/thường
  giả thuyết : giữ suffix chưa đủ vì PowerShell -eq/-ne mặc định không phân biệt hoa/thường; hai prerelease khác định danh có thể vẫn được ĐẠT.
  lệnh       : `python3 -u probes/cli-case-identity-oracle.py > evidence/cli-case-identity-summary.log 2>&1`. Gọi Invoke-TangNguoiDung/main-tail thật trên bản sao nguyên byte; getter, npm install/view, so chuỗi và JSON thật; native fixture chỉ in token/rc, không dựng Add-KetQua. Đo trực tiếp CLI --version và npm view sau run.
  output     : stable-control và case-equal (1.0.0-rc.A ở cả CLI/npm view) exit0/ok=true; case-other (CLI1.0.0-rc.B, npm1.0.0-rc.A) exit1/ok=false/2loi. case-different: CLI claude/codex --version rc0 in1.0.0-rc.a; npm view từng gói rc0 in1.0.0-rc.A; npm install rc0; cả hai dòng vẫn giu/sau1.0.0-rc.a, product exit0/ok=true. `Case identity: controls 3/3 as expected; case-different FALSE SUCCESS for both CLI`. evidence/cli-case-identity-oracle.json.
  kết luận   : LỖI P1 theo B: full identity khác nhau vẫn được chấp nhận ở nhánh không qua Compare-PhienBan. Phản chứng suffix-vs-stable lượt11 đã đóng, nhưng slug loi-native-tang-nguoi-dung vẫn còn mở với biểu hiện định danh phân biệt hoa/thường. Không khẳng định prerelease này đang tồn tại trên npm hoặc VM; đó là native fixture xác định input hợp lệ của nhánh.

HƯỚNG 12: audit đủ mọi Add-KetQua khác loi và các catch/continue/skip
  giả thuyết : còn nhánh phát ĐẠT/kiem bị bỏ sót, catch nuốt lỗi lập trình hoặc ca không đo được vẫn đếm ĐẠT.
  lệnh       : `pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory.json`; `pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/audit-source.log`; đọc source 1–704, test 1–861, README 1–62; `python3 probes/audit-regression-results.py`; `python3 probes/audit-extra-regressions.py`.
  output     : parse_errors=0; Add-KetQua=50, khác loi=19; 106 tên Ca tĩnh/106 duy nhất; Linux thực chạy102 (H2). Assertion system/caller26/26 PASS, absence/user-extra21/21 PASS. Main-tail: control exit0, user/system/programmer throw exit1/ok=false/loi1, JSON có exception. User-extra12 ca: không thoát hàm, 11 dòng, profile_restored=true, mọi lỗi native/status/JSON đều thành loi.
  kết luận   : KHÔNG PHẢI LỖI mới ở catch/continue/bo_qua trong tập đã đo. Các getter catch rộng có thể che loại lỗi lập trình thành null nhưng caller chuyển thành loi, không thành ĐẠT. Catch công cụ/main ghi loi; catch status giữ mode=null/rc chưa hợp lệ và khôi phục HOME/USERPROFILE nên lỗi không thành storage=file. Catch OutputEncoding rỗng không phát kết quả công cụ. Continue trong try chỉ sau kiem/loi hoặc phân loại HT; finally dọn tải vẫn chạy. Không có Add-KetQua bo_qua trong AST. Bootstrap PyYAML chưa kiểm rc riêng nhưng đọc ghim và dòng gói chính thức vẫn phải đạt. Admin Windows không đo mã3 thì Ca trả false; nhánh shebang ngoài Windows không gọi Ca trên Windows nên không được tính qua. ACL model giữ trạng thái nhưng dừng trước credentials/COM; không coi là đã đo trọn đăng ký Windows.

## KIỂM TOÀN BỘ ĐIỂM Add-KetQua KHÁC loi (19/19)

A: ChiKiem chỉ khác loi nếu phiên bản đang cài đo được (native rc0+match). B: cài thật chỉ giu/nang_cap/cai_moi khi sau đo được và bằng đúng định danh đích được xác định hợp lệ; ngoại lệ theo prompt. Dòng là số tại exact head, hàm/command đầy đủ có trong evidence/inventory.json.

| Dòng / hàm | Action | Kiểm A | Kiểm B / bằng chứng |
| --- | --- | --- | --- |
| 355 Update-CongCuZip | giu | Getter rc0+match; ChiKiem thiếu/broken bị guard348 chặn. Portable-check4/4. | Compare==0, parser neo cả token; không còn mất suffix. ZIP7/7 và identity stable/suffix H3. |
| 357 Update-CongCuZip | can_cap_nhat | Chỉ ChiKiem, guard348 có truoc; portable missing/rc9 đều loi. | Không phải dòng thành công cài thật; return trước tải. |
| 372 Update-CongCuZip | nang_cap/cai_moi | Không tới trong ChiKiem vì357 return. | Save kiểm băm, sau getter rc0+match, Compare==0 tại371. ZIP upgrade/badpost và caller-null; parser null -ne0 nên thành loi. Không đo ZIP Windows thật. |
| 390 Invoke-TangNguoiDung | python giu | pyTruoc lấy bằng getter rc0+match tại388,389 chặn null. User-version/native3/3. | Ngoại lệ chủ ý: Python chỉ báo, không tự nâng. |
| 405 Invoke-TangNguoiDung | pip/PyYAML/jsonschema kiem | Get-PhienBanGoi rc0+pattern;404 chặn null. New-paths6/6 + absence9 ca. | Chỉ ChiKiem,406 continue. |
| 413 Invoke-TangNguoiDung | pip/PyYAML/jsonschema giu/nang_cap | Không chạy ChiKiem. | Install rc0, metadata sau rc0+pattern, so ghim chính xác hoặc pip index rc0+pattern. Ghim hiện tại chỉ số; ca wrong-target/query-rc/metadata-rc bị chặn. Phép so -ne không phân biệt hoa/thường là rủi ro chung khi mở rộng định dạng; finding đo chắc chắn ở npm455. |
| 422 Invoke-TangNguoiDung | venv-kho kiem | Python getter rc0+match;422 chặn null. Third-paths6/6, runtime lỗi/cannot-start/thiếu đều loi. | Chỉ ChiKiem. |
| 435 Invoke-TangNguoiDung | venv-kho giu | Không chạy ChiKiem. | Pip rc0, python sau rc0+match, metadata hai gói rc0 và bằng ghim số. Install-contract4/4; actual pip offline2/2 (dryrun bị chặn). Không chứng nhận mọi requirement khác ngoài hợp đồng prompt. |
| 447 Invoke-TangNguoiDung | claude/codex kiem | Npm phải có; getter rc0+match,447 chặn null. Native/check/absence oracle. | Chỉ ChiKiem,448 continue. |
| 455 Invoke-TangNguoiDung | claude/codex giu/nang_cap/cai_moi | Không chạy ChiKiem. | **KHÔNG THỎA B**: dù native install/query/version đều rc0 và getter giữ đầy đủ suffix, `$sau -ne $dich` tại454 không phân biệt hoa/thường. H11: 1.0.0-rc.a != 1.0.0-rc.A nhưng vẫn giu/exit0 cả hai CLI. |
| 473 Invoke-TangNguoiDung | nlm kiem | nlmPy phải có, getter CLI rc0+match;473 chặn null. Prerequisite4/4, native-version3/3. | Chỉ ChiKiem. |
| 495 Invoke-TangNguoiDung | nlm giu/nang_cap | Không chạy ChiKiem. | Pip rc0; metadata và CLI sau phải cùng đích pip index rc0+match, storage statusrc0/JSONmode=file. Target5/5 + actual pip/NLM2/2, launcher cũ bị chặn. Các định danh số trong probes đạt; so -ne mặc định cũng không phân biệt hoa/thường nên không chứng nhận định danh tùy ý; không nhân finding từ suy đoán Python metadata. |
| 532 Invoke-TangHeThong | node-major can_quyet_dinh | ChiKiem guard521 yêu cầu truoc rc0+match. System-check6/6. | Ngoại lệ xin quyết định major mới, chưa tuyên bố cài. **Không được phát ra trong Node suffix H10 do parser null; guard bị bỏ qua**, dẫn tới installer major26. |
| 534 Invoke-TangHeThong | node can_quyet_dinh (major không còn LTS) | Cùng guard521; system-no-lts có native truoc24.1.0/rc0. | Nhánh xin quyết định, không phải thành công cài thật. |
| 548 Invoke-TangHeThong | git/gh/node/pwsh giu | Getter rc0+match và guard521; Test-CoTheCai chặn rỗng khi binary có. | Compare==0 với parser neo đầy đủ, identity stable4/4 được nhận, suffix-before4/4 bị chặn; target equal/above khác biệt đúng. |
| 550 Invoke-TangHeThong | can_cap_nhat | Guard521, getter trước rc0+match; system-check6/6. | Chỉ ChiKiem; continue trước installer. Node suffix ở ChiKiem có thể chọn sai đích26 dù A vẫn đạt; finding H10. |
| 564 Invoke-TangHeThong | can_khoi_dong_lai | Không chạy ChiKiem vì550 continue. | Ngoại lệ MSI3010 theo prompt. System-matrix reboot3 dòng gh/node/pwsh đúng action; Windows MSI thật chưa đo. |
| 566 Invoke-TangHeThong | nang_cap/cai_moi | Không chạy ChiKiem. | Install rc0 + getter sau rc0+match + Compare==0 tại565; suffix-after4/4 không còn ĐẠT. **Chọn đích Node có lỗi chính sách**: H10 từ24.1.0-rc.7 tự cài26.2.0, không xin quyết định. Hậu kiểm bằng đích đã chọn không sửa được lỗi chọn sai major. |
| 578 Invoke-TangHeThong | commander khoi_dong_lai | ChiKiem chuẩn không đặt DaCaiNode nên không tới; khởi tạo false, chỉ đặt556 sau550. | Không phải version/action B. Start-ScheduledTask EA Stop và đọc State==Running576–577; failure thành loi579. System-matrix success/failure/reboot đều thử restart. Windows task/Commander thật chưa đo. |

HƯỚNG 13: răng test mới, hạch toán Ca và hint_provenance
  giả thuyết : test mới chỉ đo đồ giả trả sẵn trạng thái, nhận skip là pass, hoặc không bắt được parser/regex hỏng trở lại.
  lệnh       : `python3 -u probes/review12-mutations.py > evidence/review12-mutations-summary.log 2>&1`; `python3 probes/test-accounting-round12.py`; `TL_TEST_PYTHON=python3 REVIEW_CASE_LOG="$PWD/evidence/case-values.jsonl" pwsh/pwsh -NoProfile -File copies/accounting/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/accounting.log 2>&1`; `python3 probes/check-l11-hint.py`.
  output     : `Review12 mutations: 11/11 KILLED`, mọi mutant exit1, có tên ca DO, không ParserError. 9 mutant cũ (CLI/metadata/query rc, target NLM/ZIP/HT, hậu điều venv/NLM, main-catch) đều đỏ. Parser không neo →99/102, đúng3 ca suffix/pure đỏ; regex CLI cắt suffix →99/102, đúng3 ca CLI/portable/HT đỏ. Accounting102/102/exit0; 102/102 giá trị Ca đều System.Boolean, không mảng chứa true/false hoặc null. `Round11 HINT verbatim + exactly the requested pure case matches reviewed test: True`.
  kết luận   : KHÔNG PHẢI LỖI về răng của 4 ca mới trong phạm vi đang đo: native fixture có output rc, caller và parser sản phẩm thật được gọi. Portable suffix dùng Update-CongCuZip thật; HTTP bị chặn, không dựng Add-KetQua. Ca HT suffix chỉ có index major24 và chặn tải nên không phát hiện hồi quy chọn major26 (H10). Không nhận đã đo lại đủ33 mutant executor nêu: reviewer tự đo11 mutant hiện tại. Phép so provenance đầu tiên cho False vì thiếu bước cộng ca thuần mà prompt yêu cầu; diff chỉ đúng1 dòng ca thuần, đã kiểm lại theo hợp đồng đầy đủ, không phải hunk hint bị thay.

HƯỚNG 14: HINT test-only A/B cho hai phản chứng mới
  giả thuyết : các ca khóa mới không phân biệt được lỗi thật hoặc buộc đúng một cách sửa.
  lệnh       : `python3 probes/build-round12-hint.py` (bước provenance đã hiệu chỉnh như H13); `TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/hint-head.log 2>&1`; cùng lệnh với hint-prototype/ (evidence/hint-prototype.log).
  output     : HINT áp patch -p0 rc0 trên hai bản sao; head+HINT **102/104**, exit1, đúng `nd_cli_dinh_danh_khac_hoa_thuong_khong_duoc_dat` và `node_hau_to_khong_duoc_tu_chon_major_moi` đỏ; witness scratch+HINT **104/104**, exit0. Witness dùng so chuỗi npm phân biệt hoa/thường và Select-NodeLts từ chối phiên bản đang có không xác định major; không sửa cây thật.
  kết luận   : LỖI P1 được khóa độc lập bằng hai ca, 102 ca cũ vẫn giữ. HINT chỉ thay tệp test; runtime witness nằm riêng ở hint-prototype/ và evidence/prototype-only.patch, không phải bản vá production đã duyệt.

### loi-native-tang-nguoi-dung  [P1]  Npm nhận hai prerelease khác định danh vì so chuỗi không phân biệt hoa/thường

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:454` (điều kiện bằng đích), `:455` (phát giu/nang_cap/cai_moi); getter `:444`, `:452` và truy vấn đích `:288`, `:453` đã giữ đủ hậu tố.

VẤN ĐỀ: L11 đã sửa đúng mất suffix và parser numeric. Nhưng hai nhánh CLI không qua Compare-PhienBan: chúng so `$sau -ne $dich`, vốn không phân biệt hoa/thường trong PowerShell. Full identity `1.0.0-rc.a` khác `1.0.0-rc.A`; getter ghi nguyên token nhỏ vào sau nhưng phép so vẫn coi bằng đích lớn. Với npm installrc0, CLI --versionrc0 và npm viewrc0, cả claude/codex vẫn được ghi giu, tổng ok=true/exit0. Vi phạm trực tiếp hợp đồng B định danh đầy đủ. Đây là đường mới của chính lớp finding L11; không tách một finding cho mỗi CLI.

ĐÃ THỬ NGHIỆM: `python3 -u probes/cli-case-identity-oracle.py` → 4 kịch bản được assert, 3 control như dự kiến; kịch bản chỉ khác hoa/thường FALSE SUCCESS cả2 CLI. Đo direct-after CLI1.0.0-rc.a và npm view1.0.0-rc.A đều rc0 (evidence/cli-case-identity-oracle.json). Getter/native launch/caller/main-tail dùng nguyên source head; chỉ output npm/CLI là executable fixture offline. Head+HINT102/104 exit1, riêng ca khóa này đỏ; witness scratch104/104 exit0. Không khẳng định prerelease đó đang tồn tại trên npm hoặc máy thật.

ĐỘ TIN: cao về lỗi so định danh ở exact head; native Windows/upstream chưa đo.

GỢI Ý VÁ: tại guard454 dùng phép bằng định danh có phân biệt hoa/thường, hoặc một chuẩn hóa được chứng minh bảo toàn định danh cho từng hệ gói; giữ getter và rc guard mới. Rà các guard version dạng so chuỗi tại412/433/492 để không tái tạo lớp khi định dạng đích thay đổi. Giữ control stable và hậu tố giống hoàn toàn, thêm ca khác chữ hoa/thường (HINT). Nguy cơ: không dùng so thứ tự SemVer bỏ build metadata để thay bằng định danh; cũng không đổi parser numeric trở lại cắt suffix.

### node-khong-doc-duoc-van-nang-major  [P1]  Parser mới biến Node có hậu tố thành “chưa cài”, tự nâng sang major mới

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:141`–`:142` (Select-NodeLts coi parser null là chưa cài), `:147`–`:150` (Test-CoTheCai chỉ kiểm chuỗi rỗng), `:520`–`:529` (caller giữ suffix và truyền tiếp), `:530`–`:536` (bỏ qua dòng xin quyết định rồi chọn đích), `:556`–`:566` (cài và phát nang_cap).

VẤN ĐỀ: Getter mới trả nguyên `24.1.0-rc.7`/`24.1.0+build.1` với rc0; Test-CoTheCai coi chuỗi không rỗng là đọc được. ConvertTo-PhienBan mới cố ý trả null cho suffix. Select-NodeLts vì vậy đi nhánh “chưa cài” và chọn LTS mới nhất bất kể major. Phép so null tại530 không lớn hơn0 nên không phát can_quyet_dinh. Với index gồm26.2.0 và24.2.0, script gọi installer26, rồi đo đúng26 nên báo nang_cap/ok=true/exit0. Trái chính sách không tự nâng major khi đã có Node. Chốt L1 vẫn bắt được output trống/rác, nhưng không bắt được giá trị không rỗng mà parser mới từ chối. Đây là hồi quy do tương tác L11, không phải yêu cầu hỗ trợ mọi prerelease.

ĐÃ THỬ NGHIỆM: `python3 -u probes/node-major-oracle.py` → 5/5 quan sát A/B được assert; head suffix2/2 tự major24→26, mỗi ca có argv msiexec chọn node-v26.2.0-x64.msi và không có dòng quyết định. Cùng fixture trên Git blob head trước d20a69e chọn node-v24.2.0-x64.msi và báo major26 cần quyết định. Head stable24.1.0 cũng giữ24; head garbage không gọi installer Node/loi/exit1. Installer model ghi target thực được caller chọn vào marker; native --version sau đọc marker đó, không diễn kết quả theo tên ca (evidence/node-major-oracle.json). Fixture A/B đầu tiên có lỗi hạch toán `$Log` bị local `$log` của Install-Msi che và version sau hardcode theo mode: đã sửa harness, chạy lại toàn bộ5 ca; không dùng lần lỗi ấy làm bằng chứng A/B. Head+HINT102/104 với ca Node đỏ; witness104/104.

ĐỘ TIN: cao về quyết định chọn installer và sai chính sách tại head; không khẳng định đã chạy MSI hoặc thay Node thật trên Windows.

GỢI Ý VÁ: phân biệt rõ ba trạng thái: chưa có Node, có Node và xác định được major, có Node nhưng không xác định được major. Trạng thái cuối phải dừng `loi`/quyết định trước chọn/tải/cài, hoặc dùng một parser major riêng đã kiểm nhưng vẫn giữ phép so định danh đầy đủ ở hậu kiểm. Không dùng null của parser làm bằng chứng chưa cài. Giữ case binary vắng được cài mới; stable cùng major vẫn cập nhật; major khác chỉ báo; suffix/build/rc lỗi không được tải major mới. HINT khóa đường trước tải; witness chỉ minh họa fail-closed, chưa là thiết kế production đã review đầy đủ.

`HINT.patch`: chỉ sửa `ops/vm/cap-nhat-cong-cu_test.ps1`, dùng `patch -p0` từ gốc bản sao `cay-kho/`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Nếu dùng, khai hint_provenance theo protocol. Runtime witness ngoài HINT chỉ dùng chứng minh hai ca mới có răng.

HƯỚNG 15: kiểm cuối exact SHA, nguồn read-only và artifact tái lập
  giả thuyết : đo nhầm cây/SHA, root source bị thay đổi hoặc HINT không khớp bản đã đo.
  lệnh       : `python3 probes/final-audit-round12.py > evidence/final-audit.log 2>&1`.
  output     : {"head": "b667da802074788c5b84ef21a3b91234e3f08b94", "tree": "28a788beaff8a31bda4ed1c1ded9697805bcd052", "status_including_ignored": "", "shallow": "false", "core_abbrev": "7", "files_match": {"ops/vm/README.md": true, "ops/vm/cap-nhat-cong-cu.ps1": true, "ops/vm/cap-nhat-cong-cu_test.ps1": true, "ops/cong_cu.yaml": true, "requirements.txt": true}, "git_checks": [{"command": ["git", "-C", "cay-kho", "diff", "--exit-code"], "rc": 0, "output": ""}, {"command": ["git", "-C", "cay-kho", "diff", "--cached", "--exit-code"], "rc": 0, "output": ""}, {"command": ["git", "-C", "cay-kho", "diff", "--check"], "rc": 0, "output": ""}], "pwsh": "7.6.9", "python": "3.13.17", "system": "Linux-6.18.44-fc-v185-x86_64-with-glibc2.39", "hint_sha256": "f9f07fe04e1284775e5da25f584a69e4cc153942646aff3f31cf12637d6d3050", "hint_patch_dryrun": 0, "hint_patch_apply": 0, "hint_matches_tested": true, "prompt_sha256": "47f88e5c834b15f962532393a90d62b5620ad3716f5e31c08cd482c68c51ab85", "baseline": "102/102", "hint_head": "102/104", "witness": "104/104", "mutations": "11/11 killed", "inventory": "19/19", "regression_groups": 4, "regression_drivers": 12, "contract_drivers": 7}
  kết luận   : KHÔNG PHẢI LỖI về nguồn và artifact. Tất cả biến đổi nằm ngoài cay-kho/. H8 sơ bộ đã được chốt bằng A/B H10; 2 finding P1 độc lập được khóa bởi H14.

Reviewer: Codex; provider OpenAI; model family GPT-6 theo chỉ thị phiên, không có phép đo API riêng về model triển khai. execution_surface=API agent có shell Linux; transport=machine/local; session=runs/d59592f7; github_submitter_identity=null. Phiên/context độc lập với executor Claude. Authority là chỉ thị trực tiếp trong prompt.snapshot/PROMPT.md; review class=sensitive; write set chỉ VERDICT/HINT/probe/log/bản sao ngoài cay-kho/. Verdict này là kết luận nội dung, không tự cấp cross_approved/land/deploy authority. Đã đọc skill cloud-environment-runtime; toolset không có environment_status, không suy readiness.

Giới hạn: NTFS junction/effective ACL/icacls Windows, Scheduled Task/COM/credential, msiexec, launcher .exe/.cmd và Commander thật trên Windows tại b667da8… **KHÔNG ĐO ĐƯỢC** từ Linux. Mô hình offline chỉ đo điều kiện chọn đích, đối số, native fixture rc/stdout, băm và luồng source thực. Pip thật chỉ chạy venv/wheel local tự tạo với PIP_NO_INDEX=1. Các ca không đo được không được tính PASS. Không dùng kết quả Windows ở SHA cũ hoặc lời khai executor để chứng nhận head mới; không mở lại P0 chỉ từ thiếu Windows. Không gọi mạng, push, merge hoặc sửa cây review; không xét ops/land/pr1065-*.

Kết quả: 0 P0, 2 P1, 0 P2, 0 P3.

**changes_requested** tại `b667da802074788c5b84ef21a3b91234e3f08b94`. Phản chứng suffix-vs-stable lượt11 đã đóng thật, nhưng finding `loi-native-tang-nguoi-dung` còn mở vì so chuỗi npm bỏ qua hoa/thường của định danh. Đồng thời bản vá tái mở `node-khong-doc-duoc-van-nang-major`: phiên bản Node có suffix đi qua chốt và tự chọn major mới. Bộ test bắt buộc Linux102/102, HINT head102/104, witness104/104; 11/11 mutant bị bắt; audit19/19 Add-KetQua khác loi. P0/P1/P2 chặn approve, P3 không chặn theo prompt. HINT test-only và bằng chứng chạy lại đặt cạnh verdict.
