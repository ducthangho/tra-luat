verdict: changes_requested
reviewed_sha: e5838ff965cf1e7d85a574903a0f0cebd3e4ac41
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

## ĐÓNG FINDING LƯỢT 12

| slug | đã đóng? | phép đo (lệnh + output) |
| --- | --- | --- |
| loi-native-tang-nguoi-dung [P1] | Đã đóng các phản chứng L4–L12 được chạy lại; xem H3/H5/H8/H9. | `python3 probes/audit-closures-round13.py`: CLI4/4 PASS; `case-different` rc1, ok=false, claude/codex đều loi khi CLI1.0.0-rc.a khác npm view1.0.0-rc.A. Các oracle rc/getter/catch/venv/NLM được ghi riêng bên dưới. |
| node-khong-doc-duoc-van-nang-major [P1] | Đã đóng phản chứng L12. | Cùng lệnh: Node5/5 PASS; prerelease/build/garbage đều loi/exit1, không có installer Node; stable24.1.0 lên24.2.0, chỉ báo major26. |

Bản sao năm tệp khớp Git blob tại exact SHA; không sửa `cay-kho/`, không gọi mạng. Test Windows thật tại head này **KHÔNG ĐO ĐƯỢC** trên Linux. Chưa dùng lời khai executor hay kết quả SHA cũ làm bằng chứng Windows cho SHA này.

## BẢNG SĂN


HƯỚNG 1: neo SHA và bản sao độc lập
  giả thuyết : đo sai nguồn hoặc cây đã đổi.
  lệnh       : git -C cay-kho rev-parse HEAD; git -C cay-kho status --porcelain; so byte năm tệp Git blob/cây thật/copies/head (evidence/preflight.json).
  output     : {"head": "e5838ff965cf1e7d85a574903a0f0cebd3e4ac41", "tree": "9c3c7291390638e3fbeaa34bd15d8bded973a305", "status": "", "files": {"ops/vm/README.md": {"git_match": true, "copy_match": true, "sha256": "e450ff93992576a31b622ce6474c7158ba05f8fdf83c8f8e8267d80fdc95bb6e"}, "ops/vm/cap-nhat-cong-cu.ps1": {"git_match": true, "copy_match": true, "sha256": "8aec94e8ba93ddcfb91d35329dbaabf742f2c2eb9e6878fc3a34e4b59f0d6b83"}, "ops/vm/cap-nhat-cong-cu_test.ps1": {"git_match": true, "copy_match": true, "sha256": "22408a2391dd8df92dc5e8b0d320f88ef93ed8cf3629f27822e6f06f1b61fe23"}, "ops/cong_cu.yaml": {"git_match": true, "copy_match": true, "sha256": "71631bb6baf532deeb4847c5ff9c407a50bfdb4fc503621913eb42c719ee92fb"}, "requirements.txt": {"git_match": true, "copy_match": true, "sha256": "97733a880d95f8a900f39af2bcd1a59a3ecb357dfc928c01c7a06636b1b07657"}}}
  kết luận   : KHÔNG PHẢI LỖI; bản sao khớp byte, cây review sạch.

HƯỚNG 2: bộ test bắt buộc
  giả thuyết : bản vá phá bộ test chính thức.
  lệnh       : TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/baseline.log 2>&1
  output     : cap-nhat-cong-cu tests: 104/104 ca QUA; rc=0
  kết luận   : KHÔNG PHẢI LỖI trong bộ test Linux này. Không chứng nhận Windows.

HƯỚNG 7: đăng ký lịch, ACL và reparse
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/registration-head.py` (qua `python3 probes/rerun-regressions.py`).
  output     : registration-head: rc0, {"mode": "install-ancestor-link", "passed": true, "rc": 0, "error": "t\u1eeb ch\u1ed1i: /tmp/review-register-47fc4de071bd442f9bce36f1d4de30c5/PF/tra-luat-ops c\u00f3 reparse point (junction/symlink): /tmp/review-register-47fc4de071bd442f9bce36f1d4de30c5/PF", "icacls_count": 0, "tool_acl_calls": 0, "audit_count": 0, "tasks": 0} | {"mode": "install-child-link", "passed": true, "rc": 0, "error": "t\u1eeb ch\u1ed1i: /tmp/review-register-941fbf87461c445197d00f80e633f754/PF/tra-luat-ops c\u00f3 reparse point (junction/symlink): /tmp/review-register-941fbf87461c445197d00f80e633f754/PF/tra-luat-ops/link", "icacls_count": 0, "tool_acl_calls": 0, "audit_count": 0, "tasks": 0}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 6: băm, cài HeThong, hậu kiểm và reboot
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/system-matrix.py`; `python3 -u probes/caller-matrix.py` (qua `python3 probes/rerun-regressions.py`).
  output     : system-matrix: rc0, {"mode": "msi-reboot", "rc": 0, "error": null, "spawns": 4, "verified": true, "left": 0, "restart": true, "rows": [["git", "nang_cap"], ["gh", "can_khoi_dong_lai"], ["node", "can_khoi_dong_lai"], ["pwsh", "can_khoi_dong_lai"], ["commander", "khoi_dong_lai"]]} | {"mode": "post-version-wrong", "rc": 0, "error": null, "spawns": 4, "verified": true, "left": 0, "restart": true, "rows": [["git", "loi"], ["gh", "loi"], ["node", "loi"], ["pwsh", "loi"], ["commander", "khoi_dong_lai"]]}; caller-matrix: rc0, {"mode": "zip-pre", "rc": 0, "data": {"mode": "zip-pre", "spawns": 0, "http_fixture_calls": 1, "results": [{"cong_cu": "rg", "truoc": "", "sau": "2.0.0", "hanh_dong": "cai_moi", "chi_tiet": ""}], "errors": 0}} | {"mode": "zip-post", "rc": 0, "data": {"mode": "zip-post", "spawns": 0, "http_fixture_calls": 1, "results": [{"cong_cu": "rg", "truoc": "1.0.0", "sau": "", "hanh_dong": "loi", "chi_tiet": "sau khi cài đo được '', mong '2.0.0'"}], "errors": 1}}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 3: đóng phản chứng định danh phiên bản lượt 11
  giả thuyết : prerelease cùng x.y.z vẫn bị nhận là đích stable ở CLI/ZIP/HeThong, trước hoặc sau cài.
  lệnh       : `python3 -u probes/version-identity-oracle.py > evidence/version-identity-summary.log 2>&1`; `python3 -u probes/cli-version-identity-oracle.py > evidence/cli-version-identity-summary.log 2>&1`; `python3 probes/audit-identity-round12.py`.
  output     : hai driver cũ rc1/AssertionError vì chúng assert FALSE SUCCESS còn tái hiện. Dữ liệu mới: stable-control (4 công cụ HT), zip-control (3 portable), cli-stable-control (2 CLI) đều ok=true/exit0/giu; suffix-before HT (4), suffix-after HT (4), zip-suffix-before (3), cli-suffix (2) đều ok=false/exit1, mọi dòng đích là loi. Getter giữ token -rc.7; sau installer fixture rc0 nhưng token sai vẫn loi. Assertion độc lập: Identity contract 7/7 PASS, stable controls 3/3, rejected suffix cases 4/4. JSON: evidence/version-identity-oracle.json, cli-version-identity-oracle.json, identity-assertions.json.
  kết luận   : KHÔNG PHẢI LỖI đối với phản chứng cụ thể lượt 11. Không lấy rc1 của driver cũ làm lỗi sản phẩm; không lấy mô hình HTTP/installer làm bằng chứng cài Windows thật.

HƯỚNG 4: ChiKiem và prerequisite trên cả hai tầng
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/third-paths-oracle.py`; `python3 -u probes/portable-check-oracle.py`; `python3 -u probes/system-check-oracle.py`; `python3 -u probes/absence-regression-oracle.py` (qua `python3 probes/rerun-regressions.py`).
  output     : third-paths-oracle: rc0, {"mode": "venv-cannot-start", "passed": true, "rc": 1, "ok": false, "errors": 1, "rows": 11, "venv": "loi", "direct_probe": {"path": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr13-pr1065.jMpB/fixtures/third-venv-cannot-start/venv/Scripts/python.exe", "exists": true, "rc": null, "error": "Cannot run a document in the middle of a pipeline: /tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr13-pr1065.jMpB/fixtures/third-venv-cannot-start/venv/Scripts/python.exe.", "output": ""}, "venv_native_calls": 0, "installs": 7} | Venv runtime oracle: 6/6 PASS; portable-check-oracle: rc0, {"mode": "check-zip-rc9", "passed": true, "rc": 1, "ok": false, "errors": 3, "rows": 11, "portable": {"rg": {"cong_cu": "rg", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr13-pr1065.jMpB/fixtures/check-zip-rc9/Tools/bin/rg.exe chưa cài hoặc không đọc được phiên bản"}, "shellcheck": {"cong_cu": "shellcheck", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr13-pr1065.jMpB/fixtures/check-zip-rc9/Tools/bin/shellcheck.exe chưa cài hoặc không đọc được phiên bản"}, "actionlint": {"cong_cu": "actionlint", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "/tmp/claude-0/-home-user-tra-luat/edb6b026-69ec-5fe1-81b8-38640ff85a8e/scratchpad/cr13-pr1065.jMpB/fixtures/check-zip-rc9/Tools/bin/actionlint.exe chưa cài hoặc không đọc được phiên bản"}}, "installs": 0} | Portable ChiKiem oracle: 4/4 PASS; system-check-oracle: rc0, {"mode": "system-no-lts", "passed": true, "rc": 0, "ok": true, "errors": 0, "rows": [["git", "can_cap_nhat", "1.0.0"], ["gh", "can_cap_nhat", "1.0.0"], ["node-major", "can_quyet_dinh", "24.1.0"], ["node", "can_quyet_dinh", "24.1.0"], ["pwsh", "can_cap_nhat", "7.6.9"]], "native_calls": 4, "native_rcs": [0, 0, 0, 0]} | System ChiKiem oracle: 6/6 PASS; absence-regression-oracle: rc0, {"mode": "check-missing-nlm-all", "passed": true, "rc": 1, "ok": false, "nlm": "loi", "errors": 1} | NLM prerequisite oracle (head): 4/4 PASS
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 5: native/catch/continue và lưới nhật ký lượt 4–7
  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.
  lệnh       : `python3 -u probes/l4-user-oracle.py`; `python3 -u probes/user-oracle.py`; `python3 -u probes/user-version-oracle.py`; `python3 -u probes/new-paths-oracle.py`; `python3 -u probes/run-main-tail.py` (qua `python3 probes/rerun-regressions.py`).
  output     : l4-user-oracle: rc0, PASS nlm-status-fails | User native error oracle: 3/3 PASS; user-oracle: rc0, PASS nlm-status-fails | User native error oracle: 3/3 PASS; user-version-oracle: rc0, PASS nlm-version-fails | Version native failure oracle: 3/3 PASS; new-paths-oracle: rc0, {"mode": "check-metadata", "passed": true, "rc": 1, "chi_kiem": true, "loi": 3, "ok": false, "tong": 11} | Remaining native paths oracle: 6/6 PASS; run-main-tail: rc0, {"mode": "system-throw", "rc": 1, "passed": true, "ok": false, "loi": 1, "tong": 1, "ket_qua": [{"cong_cu": "tang-HeThong", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "dừng giữa chừng: REVIEW-SYSTEM-LAUNCH-FAILURE"}]} | {"mode": "programmer-throw", "rc": 1, "passed": true, "ok": false, "loi": 1, "tong": 1, "ket_qua": [{"cong_cu": "tang-NguoiDung", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "dừng giữa chừng: Exception calling \"Substring\" with \"1\" argument(s): \"startIndex cannot be larger than length of string. (Parameter 'startIndex')\""}]}
  kết luận   : KHÔNG PHẢI LỖI trong tập oracle này. HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.

HƯỚNG 9: hợp đồng cài, đích và native venv/NLM
  giả thuyết : rc0 nhưng không cài, thiếu ghim, launcher cũ hoặc cao hơn đích vẫn được ĐẠT.
  lệnh       : `python3 -u probes/run-contracts-round12.py` (gọi các driver riêng liệt kê trong evidence/contracts-round12.json).
  output     : target-equality-oracle: rc0, Target equality oracle: 5 / 5 PASS; zip-target-oracle: rc0, ZIP target oracle: 7/7 PASS; install-contract-oracle: rc0, Install contract oracle: 4/4 PASS; real-pip-oracle: rc0, Real pip oracle: 2/2 PASS; real-nlm-oracle: rc0, Real NLM stale launcher: REJECTED; absence-oracle: rc0, {"mode": "metadata-recover", "rc": 1, "ok": false, "errors": 2, "rows": 11, "actions": {"python": "giu", "pip": "nang_cap", "PyYAML": "nang_cap", "jsonschema": "nang_cap", "venv-kho": "loi", "claude": "giu", "codex": "giu", "rg": "giu", "shellcheck": "giu", "actionlint": "giu", "nlm": "loi"}, "installs": 8}; run-user-extra: rc0, {"mode": "nlm-version-fails", "rc": 0, "error": null, "errors": 1, "rows": 11, "restored": true, "last": {"cong_cu": "nlm", "truoc": "", "sau": "", "hanh_dong": "loi", "chi_tiet": "pip rc=0 "}, "native_installs": 8}
  kết luận   : KHÔNG PHẢI LỖI trong bộ oracle này. Pip thật chạy với PIP_NO_INDEX=1 trên wheel local tự tạo; HTTP/npm là fixture. Không chứng nhận gói upstream/Windows.

HƯỚNG 8: đóng hai finding lượt 12 và kiểm HINT nguyên văn
  giả thuyết : lỗi khác hoa/thường hoặc tự nâng Node major vẫn tái hiện, hay test mới lệch HINT.
  lệnh       : python3 -u probes/cli-case-identity-oracle.py; python3 -u probes/node-major-oracle.py (driver L12 nguyên văn, ghi JSON trước assertion); python3 probes/audit-closures-round13.py.
  output     : driver cũ cùng rc1 vì chúng assert lỗi CÒN tái hiện. Oracle độc lập mới: CLI4/4 PASS (stable/case-equal giu, case-different/case-other loi/exit1); Node5/5 PASS (head prerelease/build/garbage loi/exit1, không gọi installer Node; stable vẫn24.2.0 + can_quyet_dinh26; Git blob d20a69e là control lịch sử riêng). Áp luot12/HINT.patch vào test của b667da8: rc0, toàn bộ hunk giữ nguyên; chỉ thêm hai assert guard thuần vào ca L1 ngoài HINT. evidence/closures-round13.json.
  kết luận   : KHÔNG PHẢI LỖI; hai phản chứng cụ thể lượt12 đã đóng thật. Dữ liệu head lịch sử chỉ là control A/B, không thay bằng chứng tại SHA mới. Không lấy rc1 stale assertion làm lỗi sản phẩm.

HƯỚNG 10: hạch toán ca test, bỏ qua và return/continue
  giả thuyết : kết quả mảng/null hoặc nhánh bỏ qua bị đếm ĐẠT.
  lệnh       : python3 probes/test-accounting-round12.py; REVIEW_CASE_LOG="$PWD/evidence/accounting.jsonl" TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File copies/accounting/ops/vm/cap-nhat-cong-cu_test.ps1; assert độc lập JSONL.
  output     : cap-nhat-cong-cu tests: 104/104 ca QUA; rc0. 104 tên duy nhất, mỗi ca đúng một System.Boolean true, không mảng/null/trùng. Runtime source nguyên byte, chỉ thêm log vào test harness. AST có108 tên khác nhau cho mọi nhánh nền; Linux chạy104; nhánh Windows không chạy không được cộng vào104.
  kết luận   : KHÔNG PHẢI LỖI trong bộ đang chạy. Các nhánh không có Python/PyYAML trả false; nhánh Windows chạy admin cố ý false (không đo được mã3), không biến skipped thành passed. Không coi các ca mô hình là Windows native.

HƯỚNG 11: so số học có bảo toàn định danh ĐẦY ĐỦ không
  giả thuyết : ConvertTo-PhienBan đổi .windows. thành dấu chấm và bỏ zero đầu qua [version]; Compare=0 không chứng minh hai token định danh giống nhau.
  lệnh       : python3 -u probes/numeric-identity-oracle.py > evidence/numeric-identity-summary.log 2>&1.
  output     : control stable4/4 giu/exit0. Đích Git2.0.0.windows.4 nhưng native --version rc0 in2.0.0.4: trước cài giu, sau installer rc0 nang_cap; cả hai ok=true/exit0. Đích2.0.0/24.2.0/7.6.10 nhưng native in02.0.0/024.2.0/07.6.10: cả4 giu hoặc nang_cap, ok=true/exit0. Getter/caller/main-tail nguyên source; chỉ HTTP/installer/task và binary output là fixture offline; full native tokens ghi evidence/numeric-identity.json. Không khẳng định Node/Git upstream hiện phát token zero-padding hay Git không có windows marker.
  kết luận   : LỖI sơ bộ theo cách đọc B yêu cầu định danh đầy đủ: so thứ tự và so định danh đang bị dùng chung. Cần đối chiếu chuẩn hóa có chủ ý và khóa ca test trước khi chốt mức độ; đây không phải tái mở hai phản chứng L12 đã đóng.

HƯỚNG 13: alias số học ở portable không ghim và có ghim
  giả thuyết : cùng cách so Compare=0 còn ảnh hưởng cả hai nhánh giu/hậu cài của ZIP, kể cả đích ghim.
  lệnh       : python3 -u probes/zip-numeric-identity-oracle.py > evidence/zip-numeric-identity-summary.log 2>&1.
  output     : rg-at-target2.0.0 giu/exit0; rg/actionlint đích2.0.0 nhưng native trước02.0.0 -> giu, hoặc trước1.0.0/copy ZIP có bản02.0.0 -> nang_cap; cả4 ok=true/exit0. JSON evidence/zip-numeric-identity.json. Với actionlint đã truyền Tag=v2.0.0, response tag=v2.0.0, hash/copy/đo native thực; không dựa vào metadata API sai tag. Không khẳng định upstream có output zero-padding.
  kết luận   : LỖI theo B định danh đầy đủ ở hai đường ZIP. Chỉ một lớp lỗi chung với H11; không tách thành nhiều finding theo công cụ.

HƯỚNG 12: test mới có răng và catch có biến lỗi thành ĐẠT không
  giả thuyết : ca mới chỉ diễn output mong muốn hoặc catch/continue che mất lỗi lập trình/native.
  lệnh       : python3 -u probes/review13-mutations.py > evidence/mutations-driver.log 2>&1; python3 probes/run-main-tail.py (đã chạy ở H5); pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source-audit.log; rg -n 'try|catch|continue|bo_qua' cay-kho/ops/vm/cap-nhat-cong-cu.ps1.
  output     : 13/13 mutant bị bắt, mỗi mutant rc1 và ca đích đỏ, không ParserError. Đổi -cne của CLI về -ne =>103/104, riêng nd_cli_dinh_danh_khac_hoa_thuong_khong_duoc_dat đỏ. Guard Node trở lại chỉ kiểm rỗng =>102/104, ca thuần L1 và node_hau_to_khong_duoc_tu_chon_major_moi cùng đỏ. Thả rc getter, metadata, target; bỏ hậu điều venv/NLM; chấp nhận bản cao hơn; cắt suffix; bỏ main catch đều bị ca tương ứng bắt. Main-tail programmer-throw => exit1/ok=false/loi1, JSON còn ghi được. Parse0 lỗi, README0 lệnh icacls tay.
  kết luận   : KHÔNG PHẢI LỖI với các ca mới L12/catch. Patch từ b667da8 không thêm try/catch nào. Catch getter trả null; mọi nơi dùng null làm điều kiện thành công đều bị chặn; per-tool/main catch ghi loi, không bo_qua. continue trong try chỉ thoát vòng công cụ hiện tại; oracle người dùng giữ11 dòng. Catch status NLM giữ rcSt=null nếu launch hỏng => không thể đạt; finally phục hồi USERPROFILE/HOME. Catch Console encoding rỗng chỉ hạ trang trí console, không chứng nhận công cụ. Mô hình test CLI mới chỉ in token/rc, không tự ghi KetQua; mô hình Node ghi mọi tên tải rồi ném nên ca không được qua chỉ vì installer không chạy. Giới hạn: 13 mutant reviewer tự đo, không xác nhận con số37 executor khai.

HƯỚNG 15: biên quyền SYSTEM, đường dẫn, task và nền Windows
  giả thuyết : còn đường chạy payload chưa kiểm băm hoặc giao ACL theo cây người dùng sau các bản vá.
  lệnh       : pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source-audit.log; python3 probes/audit-old-matrices-round13.py; python3 probes/registration-head.py (H7); đọc cả3tệp ops/vm tại head.
  output     : source parser0lỗi, README_native_acl_commands=0; Invoke-Icacls chỉ SystemRoot/System32;3lời gọi đăng ký chỉ đụng thư mục cài ProgramFiles; Save-CoKiemBam gọi Assert-Bam trước return, đường tải HT đi qua nó trước Start-Process/Install-Msi. Mô hình tamper/missing-hash đều4loi/0spawn/0tệp tải còn; đăng ký ancestor/child symlink đều từ chối trước icacls/chép/task. Không có đường tự giao ACL C:/Tools trong source/README. New-ThuMucTai kiểm rc icacls, bỏ thừa kế rồi cấp SID SYSTEM/Administrators; registration đo ACL+băm sau copy trước tạo task.
  kết luận   : KHÔNG PHẢI LỖI trong luồng/static đã đo; KHÔNG ĐO ĐƯỢC effective NTFS ACL, junction Windows, Scheduled Task COM/credential, msiexec/3010 và Commander thật tại SHA này do chỉ có Linux. Không suy mô hình /inheritance:r thành effective access đã chứng nhận, cũng không mở P0 chỉ từ thiếu Windows. Task yêu cầu user/password từ Get-Credential giữ trong process, không ghi password vào câu lệnh hay JSON. Không gọi mạng để kiểm VM/GitHub; ops/land ngoài scope không được review.

## KIỂM TOÀN BỘ Add-KetQua KHÁC loi

Lệnh: `pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory.json`; `python3 probes/audit-contract-table-round13.py`. Output: parse_errors=0, add_count=50, nonloi_count=19; kiểm đủ19/19 vị trí, không suy từ chỉ danh sách ca cũ. A áp cho mọi dòng ChiKiem; B áp cho giu/nang_cap/cai_moi với các ngoại lệ được giao. Các phép đo liên kết trong bảng là trên bản sao exact head.

| Dòng | Hàm / hành động | Kết luận A/B | Phép đo hoặc lập luận |
| --- | --- | --- | --- |
| 357 | Update-CongCuZip / 'giu' | A đạt; B VI PHẠM | Getter rc0 + mẫu trước so; Compare=0 chỉ chứng minh cùng số. H13: rg/actionlint02.0.0 so đích2.0.0 vẫn giu. |
| 359 | Update-CongCuZip / 'can_cap_nhat' | A đạt; B không áp hành động này | Chỉ ChiKiem, đã loại truoc rỗng tại350. portable-check-oracle4/4; bản cũ đo được can_cap_nhat, rc9/vắng/cannot-start loi. |
| 374 | Update-CongCuZip / $(if ($truoc) { 'nang_cap' } else { 'cai_moi' }) | B VI PHẠM | Đã đo sau copy bằng getter rc0 + mẫu, nhưng so Compare chấp nhận02.0.0 khác2.0.0. H13 alias-after nang_cap/ok=true. |
| 392 | Invoke-TangNguoiDung / 'giu' | A đạt; B ngoại lệ Python chỉ báo | pyTruoc từ getter rc0 + Python\s+(\S+), nếu null thì loi/return391. new-paths-oracle check-python rc lỗi =>loi; third-paths check-only cóPython3.12.7/giu. |
| 407 | Invoke-TangNguoiDung / 'kiem' | A đạt | Chỉ ChiKiem, Get-PhienBanGoi bắt rc0 và toàn chuỗi mẫu; null=>loi406. new-paths-oracle/check-metadata=>3loi, absence-oracle kiểm metadata trống/rác cũng loi. |
| 415 | Invoke-TangNguoiDung / $(if ($truoc -ceq $sau) { 'giu' } else { 'nang_cap' }) | B đạt trong nhánh này | rc pip phải0, sau từ metadata rc0 + mẫu, đích pip từ pip index rc0 hoặc hai ghim bản kê, -cne buộc cùng token; target thiếu/rc4=>loi. run-contracts: real-pip2/2, install-contract4/4; mutant metadata/target bỏrc bị bắt. |
| 424 | Invoke-TangNguoiDung / 'kiem' | A đạt | ChiKiem đo interpreter bằng getter, null=>loi. third-paths6/6 gồm missing/rc9/cannot-start; đối chứng1dòng venv-kho/kiem. |
| 437 | Invoke-TangNguoiDung / 'giu' | B đạt | Sau pip rc0 đo Python và metadata hai gói; -cne với hai ghim. install-contract4/4 + pip wheel local2/2, rc0 không cài và Python sau rc9 đều loi. H12 mutant bỏ hậu điều bị bắt. |
| 449 | Invoke-TangNguoiDung / 'kiem' | A đạt | ChiKiem có npm prerequisite; truoc getter rc0 + mẫu, không đo được=>loi. new-paths check-cli/CLI native lỗi và absence missing CLI=>loi,11dòng. |
| 458 | Invoke-TangNguoiDung / $(if ($truoc -ceq $sau) { 'giu' } elseif ($truoc) { 'nang_cap' } else { 'cai_moi' }) | B đạt cho phản chứng được giao | npm install rc0; sau CLI getter rc0 + mẫu giữ suffix; đích npm view rc0 + mẫu; -cne đầy đủ. H8 CLI4/4 gồm case-equal giu, case-different loi. H3 stable/suffix kiểm thêm; H12 đảo -cne=>-ne bắt đúng ca. |
| 476 | Invoke-TangNguoiDung / 'kiem' | A đạt | nlmPy phải có; truoc nlm --version getter rc0 + mẫu, null=>loi. NLM prerequisite4/4 và user-version native rc9=>loi. |
| 498 | Invoke-TangNguoiDung / $(if ($truoc -ceq $sau) { 'giu' } else { 'nang_cap' }) | B đạt | pip rc0, nlm.exe getter rc0 + mẫu; metadata gói và CLI đều -cne đích pip index rc0; status rc0 + JSON mode=file. target-equality/stale launcher và real-nlm2/2; status rc7, bad JSON, mode khác, launcher cũ đều loi; finally phục hồi home. |
| 535 | Invoke-TangHeThong / 'can_quyet_dinh' | A đạt; B ngoại lệ can_quyet_dinh | Nếu ChiKiem, đầu vòng đã loại truoc null và guard yêu cầu parser nhận khi có tệp. system-check6/6: node-major chỉ khi đã đo current24.1.0; H8 prerelease/build bị loi trước index/installer. |
| 537 | Invoke-TangHeThong / 'can_quyet_dinh' | A đạt; B ngoại lệ can_quyet_dinh | ChiKiem có current đo được do524; no-LTS cùng major chỉ xin quyết định, không cài. system-check no-lts =>2can_quyet_dinh/rc0,4native_rc0. Cài thật thiếu binary được phép nhánh quyết định khi index không cóLTS; không phải giu/nang_cap/cai_moi. |
| 551 | Invoke-TangHeThong / 'giu' | A đạt; B VI PHẠM | Getter current rc0 + mẫu, guard parser nhận; nhưng Compare chuẩn hóa mất .windows. và zero đầu. H11 Git2.0.0.4 so đích2.0.0.windows.4 vẫn giu/exit0. |
| 553 | Invoke-TangHeThong / 'can_cap_nhat' | A đạt; B không áp hành động này | ChiKiem đã loại current null524. system-check missing/garbage/rc9/cannot-start đều loi; stable cũ can_cap_nhat, không installer. |
| 567 | Invoke-TangHeThong / 'can_khoi_dong_lai' | A không tới; B ngoại lệ MSI3010 | Chỉ sau khi cài thật; Install-Msi trả can_khoi_dong_lai duy nhất ExitCode3010. system-matrix msi-reboot =>git nang_cap,3MSI can_khoi_dong_lai; không đòi version đã có hiệu lực ở ngoại lệ này. |
| 569 | Invoke-TangHeThong / $(if ($truoc) { 'nang_cap' } else { 'cai_moi' }) | B VI PHẠM | Băm/rc installer/hậu getter đã chặn lỗi, nhưng hậu Compare chỉ so số. H11 git-alias-after =>sau2.0.0.4, đích2.0.0.windows.4, nang_cap/ok=true; zero-padding sau cũng được nhận. Khác lỗi hash/rc, không là P0. |
| 581 | Invoke-TangHeThong / 'khoi_dong_lai' | Ngoài hành động B; A không tới | khoi_dong_lai là trạng thái task, không giu/nang_cap/cai_moi. DaCaiNode chỉ bật khi ChiKiem=false trước installer, nên invocation CLI ChiKiem không tới. Đo Get-ScheduledTask.State Running; lỗi task=>loi. system-matrix cài Node hỏng vẫn dựng Commander; Windows native chưa đo. |

Cả bốn vị trí B vi phạm đều cùng nguyên nhân Compare=0 không bảo toàn định danh, được gộp thành một finding; 15 vị trí còn lại có guard/ngoại lệ nêu rõ. A không có phản chứng trong tập đã đo. Native Windows không được chứng nhận từ bảng này.

HƯỚNG 14: xác nhận dương/âm cho driver cũ không tự assert đủ
  giả thuyết : driver rc0 chỉ chứng minh có JSON, không chứng minh băm/installer/hậu phiên bản đúng.
  lệnh       : python3 probes/audit-old-matrices-round13.py
  output     : Independent matrix assertions: 6 system + 4 caller PASS; 12 regression drivers + 7 contract drivers rc0. Check số spawn, mọi băm khớp ở thời điểm spawn,4dòng công cụ, hành động từng ca, cleanup0 và Commander phục hồi đúng điều kiện. evidence/matrix-assertions-round13.json.
  kết luận   : KHÔNG PHẢI LỖI trong các oracle hồi quy; không chỉ dựa rc0. Driver test-branches từ L4 hardcode số ca lịch sử không dùng để chứng nhận head mới; inventory AST và accounting104 thay phần ấy. registration-head đã chạy5mode trên head; phần registration-matrix dùng mutant lịch sử không phải phép đo head, thay bằng mô hình stateful trong suite và mutant đã chọn.

### so-so-hoc-lam-mat-dinh-danh  [P1]  ZIP và HeThong vẫn nhận hai định danh khác nhau là cùng đích

TỆP/DÒNG: `ops/vm/cap-nhat-cong-cu.ps1:66` chuẩn hóa `.windows.` thành `.`, `:72` ép `[version]` mất zero đầu, `:80` trả CompareTo; bốn nơi dùng kết quả ấy để chứng nhận bằng đích: `:357`, `:373`, `:551`, `:568`.

VẤN ĐỀ: Chốt suffix và phép so chuỗi phân biệt hoa/thường đã đóng đúng hai phản chứng L12. Nhưng các nhánh ZIP/HeThong vẫn dùng duy nhất `Compare-PhienBan == 0` để ghi `giu`, hoặc hậu cài chỉ cần Compare không khác0 để ghi `nang_cap`/`cai_moi`. Hàm phục vụ so thứ tự biến nhiều token khác nhau thành một giá trị số: `2.0.0.windows.4` và `2.0.0.4` cùng `[version]2.0.0.4`; `2.0.0` và `02.0.0` cùng `[version]2.0.0`. Getter giữ nguyên token, native rc0 và khớp mẫu, nhưng không có bước kiểm token đầy đủ bằng đích. Vì vậy script có thể in ĐẠT/ok=true dù hai định danh nguyên vẹn khác nhau, trái B được giao. Đây là lỗ còn lại trong hợp đồng B L11, không phải guard Node L12 tự mở lại.

Không phản đối chuẩn hóa Git Windows để SO THỨ TỰ hoặc chọn major. Vấn đề là lấy quan hệ đó làm chứng cứ cùng ĐỊNH DANH. Token zero-padding không phải SemVer canonical; script hiện không từ chối nó mà ghi thành công. Không yêu cầu cài hay hỗ trợ phiên bản lạ: đầu vào không xác định cùng định danh phải `loi`, hoặc cài rồi đo lại đúng đích. Các ngoại lệ can_quyet_dinh/MSI3010/Python không áp cho các dòng `giu`/`nang_cap` đã đo này.

ĐÃ THỬ NGHIỆM: `python3 -u probes/numeric-identity-oracle.py > evidence/numeric-identity-summary.log 2>&1`: control4công cụ bình thường `giu`/exit0. Đích Git2.0.0.windows.4, native `git version 2.0.0.4` rc0: `git-alias-before` ghi `giu`, `git-alias-after` gọi installer model rc0 rồi ghi `nang_cap`, đều ok=true/exit0. Đích numeric2.0.0/24.2.0/7.6.10 nhưng đo02.0.0/024.2.0/07.6.10: cả4công cụ được nhận trước hoặc sau cài. `python3 -u probes/zip-numeric-identity-oracle.py > evidence/zip-numeric-identity-summary.log 2>&1`: ZIP thật được tạo, băm, tải offline, giải nén và chép native fixture; rg/actionlint không ghim/có Tag=v2.0.0, response tag đúngv2.0.0, đo02.0.0 trước/sau so đích2.0.0 vẫn giu/nang_cap/ok=true/exit0,4/4false success. Không dựa response GitHub sai tag. Bằng chứng đầy đủ ở `evidence/numeric-identity.json`, `evidence/zip-numeric-identity.json`.

`HINT.patch` test-only thêm4ca tích hợp: đối chứng ZIP bằng đích, System zero-padding trước, ZIP zero-padding trước và sau (mỗi ca ZIP thử không ghim/có ghim). Head + HINT:105/108,3ca đích đỏ; witness chỉ thêm điều kiện định danh ở4chỗ chứng nhận trên bản sao:108/108. Nguồn `cay-kho/` không sửa. Không khẳng định upstream/VM thật đang phát các token mô phỏng này; đây là phản chứng xác định cho tính chất B trên dữ liệu native được regex/parser head chấp nhận, và không phải một phép cài MSI Windows thật.

ĐỘ TIN: cao về hành vi source tại exact SHA và sự khác biệt token; giới hạn phạm vi như trên.

GỢI Ý VÁ:
- Vá ở đâu: tách điều kiện “cùng định danh” khỏi so thứ tự ở hai nhánh `giu` và hai hậu kiểm ZIP/HeThong. Giữ `ConvertTo-PhienBan`/Compare cho chọn major và so cao/thấp; sửa toàn cục comparator có thể gây hồi quy chính sách Node/Git.
- Vá thế nào: kiểm định danh đầy đủ đã chuẩn hóa CHỈ theo quy tắc biểu diễn có chứng cứ (caller đã bỏ `v` của release), giữ marker `.windows.`, hậu tố và mọi thành phần có ý nghĩa. Nếu token không thuộc ngữ pháp hợp lệ thì từ chối; không coi ép `[version]` thành công là cùng định danh. Bản cùng thứ tự nhưng khác token có thể báo lỗi, hoặc cài lại đích rồi đòi đo đúng token. Không cần triển khai SemVer ordering mới để đóng việc chứng nhận nhầm này.
- Ca test khóa: `HINT.patch` + các oracle trước/sau nêu trên; giữ control stable và Git `.windows.N` đúng nguyên vẹn. Đột biến bỏ riêng guard định danh nhánh `giu` hoặc bỏ riêng guard định danh hậu cài phải làm ca tương ứng đỏ; bằng chứng targeted sẽ được nối bên dưới.
- Nguy cơ bản vá: không chuyển nhầm “không biết” thành “chưa cài” rồi tự nâng major Node; không đòi ký tự `v` mà getter đã bỏ có chủ ý, cũng không bỏ `.windows.N` của Git thật. Không sửa phép so thứ tự để nó dùng thứ tự chuỗi. Giữ rc/hash/catch/cleanup và các ngoại lệ3010/quyết định như hiện tại.

`HINT.patch`: định dạng `patch -p0` từ gốc bản sao `cay-kho/`, chỉ sửa test. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**; nếu dùng khai hint_provenance=HINT lượt13. Runtime witness chỉ là chứng minh trên scratch, không phải bản vá production đã review để triển khai.

HƯỚNG 16: khóa finding mới bằng HINT và đột biến từng cửa
  giả thuyết : test zero-padding có thể đỏ vì setup hoặc chỉ bắt được một nhánh, còn witness làm sai control/Git/Node cũ.
  lệnh       : python3 probes/build-round13-hint.py; TL_TEST_PYTHON=python3 pwsh/pwsh -NoProfile -File hint-validation/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/hint-head.log 2>&1; cùng lệnh cho witness-validation > evidence/hint-witness.log; python3 -u probes/check-identity-mutants-round13.py > evidence/targeted-driver.log 2>&1.
  output     : head+HINT105/108, rc1; đúng3ca dich_he_thong_zero_dau_khong_phai_dinh_danh_dich, zip_zero_dau_truoc_khong_duoc_giu_dat, zip_zero_dau_sau_khong_duoc_bao_nang_cap đỏ. Witness108/108, rc0, giữ toàn bộ104ca cũ kể cả Git_windows/Node major/case CLI. Targeted AST lấy nguyên4ca và2helper trong HINT: control4/4/rc0; bỏ guard định danh ở hai nhánh giu =>2/4/rc1; bỏ guard hậu cài =>2/4/rc1. Không ERROR/setup/ParserError. evidence/identity-targeted-mutants.json. Đối chứng Git Windows thật về dạng token còn có system-matrix success: trước2.55.0.windows.1, sau2.56.0.windows.4 đúng tag, nang_cap.
  kết luận   : LỖI P1 đã khóa; H11 sơ bộ được chốt cùng H13/H16. Ba ca mới có răng ở cả trước/sau; bốn vị trí B vi phạm gộp một finding. Chuẩn hóa [version] để so thứ tự vẫn hoạt động khi bổ sung hậu điều riêng; witness không phải khuyến nghị dùng nguyên xi trong production.

Reviewer: Codex, provider OpenAI, model family openai/GPT-6 theo chỉ thị phiên (không có phép đo API riêng về model triển khai); execution_surface=API agent với shell Linux; transport=machine/local; session=runs/8284da89; github_submitter_identity=null; independent_from_executor_session=true. Authority là chỉ thị trực tiếp prompt.snapshot/PROMPT.md cho review lượt13; Review Class=sensitive; write set chỉ VERDICT/HINT/probe/log/bản sao ngoài cay-kho/. Không dùng verdict này để tự cấp cross_approved, merge/land/deploy hoặc chứng nhận CI/VM.

Đã đọc AGENTS, CONTEXT, các phần protocol/CLAUDE và kế hoạch provider liên quan đến vai Reviewer, exact SHA, bằng chứng, hint, stop condition. Chỉ thị trực tiếp yêu cầu lượt13 là authority cho lượt này, không tự dừng theo budget mặc định của Packet khác. Không cần thao tác pháp luật/corpus/Drive/NotebookLM LIVE. Không tải skill hay gọi dịch vụ mạng.

Giới hạn: NTFS junction, effective ACL/icacls Windows, Scheduled Task/COM/credential, msiexec/3010, launcher .exe/.cmd thật và Commander trên VM ở e5838ff… KHÔNG ĐO ĐƯỢC tại môi trường Linux. Những phần này chỉ có phân tích tĩnh và mô hình offline. Pip thật chỉ dùng venv/wheel local tự tạo với PIP_NO_INDEX=1; không đo upstream. Các native fixture chỉ chứng minh output/rc/file và luồng source; không khẳng định phiên bản mô phỏng đang phát hành. Không lấy bằng chứng Windows ở SHA cũ hay lời khai executor104/104/37độtbiến thay phép đo hiện tại. Không đếm Windows không chạy vào104; không suy thiếu Windows thành P0. Không sửa cay-kho/, không push, không gọi mạng; không review ops/land/pr1065-*.

HƯỚNG 17: kiểm cuối exact SHA, cây chỉ đọc và artifact
  giả thuyết : cây nguồn đổi, phép đo không neo head hoặc HINT không khớp bản đã chạy.
  lệnh       : python3 probes/final-audit-round13.py > evidence/final-audit.log 2>&1
  output     : {"head": "e5838ff965cf1e7d85a574903a0f0cebd3e4ac41", "tree": "9c3c7291390638e3fbeaa34bd15d8bded973a305", "status_including_ignored": "", "shallow": "false", "core_abbrev": "7", "detached": true, "files": {"ops/vm/README.md": "e450ff93992576a31b622ce6474c7158ba05f8fdf83c8f8e8267d80fdc95bb6e", "ops/vm/cap-nhat-cong-cu.ps1": "8aec94e8ba93ddcfb91d35329dbaabf742f2c2eb9e6878fc3a34e4b59f0d6b83", "ops/vm/cap-nhat-cong-cu_test.ps1": "22408a2391dd8df92dc5e8b0d320f88ef93ed8cf3629f27822e6f06f1b61fe23", "ops/cong_cu.yaml": "71631bb6baf532deeb4847c5ff9c407a50bfdb4fc503621913eb42c719ee92fb", "requirements.txt": "97733a880d95f8a900f39af2bcd1a59a3ecb357dfc928c01c7a06636b1b07657"}, "prompt_sha256": "4bfc404d292c28c64183462b1732ae80311ee3d02ae1ac8f0e6650fcd1755b3c", "hint_sha256": "91c067da17695a0506d7fb7b5d52eacd45bc59efdd30da4f4165695bdfd89c84", "hint_patch_dryrun_rc": 0, "hint_patch_apply_rc": 0, "hint_reapplied_matches_tested": true, "baseline": "104/104", "accounting": "104/104", "hint-head": "105/108", "hint-witness": "108/108", "reviewer_head_mutants": "13/13 killed", "reviewer_witness_mutants": "2/2 killed; control4/4", "non_loi_audit": "19/19; four sites, one finding", "case_accounting": "104 unique scalar true", "regressions-round12": 12, "contracts-round12": 7, "pwsh": "7.6.9", "python": "3.13.17", "system": "Linux-6.18.44-fc-v185-x86_64-with-glibc2.39", "hunting_directions": 16}
  kết luận   : KHÔNG PHẢI LỖI về nguồn/artifact; mọi thay đổi nằm ngoài cay-kho/.

Kết luận cuối: **changes_requested** tại `e5838ff965cf1e7d85a574903a0f0cebd3e4ac41`. Hai phản chứng lượt12 đã đóng thật. Còn một P1 độc lập `so-so-hoc-lam-mat-dinh-danh`: bốn cửa chứng nhận ZIP/HeThong chỉ so giá trị số, chưa chứng minh cùng định danh đầy đủ. Không phát hiện P0/P2/P3 trong phạm vi đã đo; phần Windows chưa đo được khai riêng, không tính PASS. Bộ bắt buộc Linux104/104; head+HINT105/108; witness108/108; mutant reviewer13/13 và targeted2/2 bị bắt. Đã kiểm đủ19/19 Add-KetQua khác loi qua17hướng, với lệnh/output và artifact đặt cạnh verdict.
