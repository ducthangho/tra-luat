verdict: approve
reviewed_sha: 97cb2dda246886c7d4bec2bea4a4b89342403a65
reviewed_tree: f5ab9894b8eeccd2aeab913cfa257a1d05db39e5

Merge giữ nguyên nội dung hai tệp đã được approve ở lượt 3. So master, HEAD chỉ có đúng hai tệp write set; không phát hiện P0–P2 hay finding mới. Approval này xác nhận phạm vi review sau merge; không chứng nhận t237 HTTP, Windows hoặc toàn bộ release/land gate.

## Neo và môi trường

- Cha 1, SHA đã review lượt 3: `69dbf3af3c82bc6e1d6769666ca670bd706e80a5`.
- Cha 2, master theo assignment: `4fb3c034d0456a600634f501b8f20bd1487e3b83`.
- Merge-base hai cha: `fe84620f897913c7f6c2ce5a0c7316a49655e82f`, khớp base của SPEC/LEASE wp1237/r1/g1, class sensitive. Checkout reviewer ở detached HEAD, worktree sạch.
- `SPEC.md` SHA-256: `b0e12304e0c591db6e2130454ed6a72c1458d4541b1312037935b0ccbb210666`, khớp lease. Write set: `ops/cai_actionlint.sh`, `ops/lease_publish_test.py`; diff so master là **214 dòng thêm, 3 dòng xóa, 2 tệp**, trong trần 250 dòng thêm.
- Reviewer/provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run `6ba97f33`, theo `runs/6ba97f33/run.json`. Sổ run hiện không có bằng chứng model/effort phục vụ: **KHÔNG ĐO ĐƯỢC**; không suy từ cấu hình yêu cầu hoặc tự chứng nhận assurance từ tên công cụ.
- Linux, Python 3.13.18, Bash 5.2.21, ShellCheck 0.9.0. Sandbox `workspace-write`; chỉ thị read-only áp riêng `cay-kho`. Không sửa kho, commit, push, gọi workflow hay đăng verdict ra dịch vụ ngoài.

## Bảng đo — LỆNH + OUTPUT

Các lệnh Git/lint/test dưới đây chạy trong `cay-kho`. Tiến trình Python kế thừa `PYTHONDONTWRITEBYTECODE=1`; Git kế thừa `GIT_OPTIONAL_LOCKS=0`. Script đo và bằng chứng nằm ngoài checkout, tại thư mục `xr4`.

| Lệnh | rc | OUTPUT thật, rút gọn | Kết quả |
|---|---:|---|---|
| `git rev-parse HEAD HEAD^1 HEAD^2` | 0 | `97cb2dda246886c7d4bec2bea4a4b89342403a65`; `69dbf3af3c82bc6e1d6769666ca670bd706e80a5`; `4fb3c034d0456a600634f501b8f20bd1487e3b83` | passed, đúng các mốc assignment |
| `git diff --stat HEAD^1 HEAD -- ops/cai_actionlint.sh ops/lease_publish_test.py` | 0 | stdout/stderr rỗng | passed, hai tệp giữ nguyên |
| `git diff --numstat HEAD^2 HEAD` | 0 | `36  3  ops/cai_actionlint.sh`; `178  0  ops/lease_publish_test.py` | passed, chỉ hai tệp write set |
| `git merge-base --is-ancestor HEAD^2 HEAD` | 0 | stdout/stderr rỗng | passed, master là tổ tiên của head |
| `git merge-base HEAD^1 HEAD^2` | 0 | `fe84620f897913c7f6c2ce5a0c7316a49655e82f` | passed |
| `git diff --check HEAD^2 HEAD` | 0 | stdout/stderr rỗng | passed |
| `bash -n ops/cai_actionlint.sh` | 0 | stdout/stderr rỗng | passed |
| `shellcheck ops/cai_actionlint.sh` | 0 | stdout/stderr rỗng | passed |
| `python3 ops/lease_publish_test.py --chi-ca=t35` | 0 | `QUA`; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | passed |
| `python3 ops/lease_publish_test.py --chi-ca=t37` | 0 | `QUA`; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | passed |
| `python3 ops/lease_publish_test.py --chi-ca=t38` | 0 | `QUA`; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | passed |
| `python3 ops/lease_publish_test.py --chi-ca=t237` | 1 | `PermissionError: [Errno 1] Operation not permitted`; `lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0` | **KHÔNG ĐO ĐƯỢC** HTTP do sandbox chặn socket; không phải pass |
| Từ `xr4`: `PYTHONDONTWRITEBYTECODE=1 python3 -B review_integration.py` | 0 | `inherited_paths_equal_master_delta: true`; `inherited_blob_mismatches: []`; `caller_dependency_delta_from_first_parent: []`; hai hiện vật patch/numstat khớp Git | passed kiểm tra cấu trúc merge và tương tác |
| Từ `xr4`: `python3 -B review_checks.py after` | 0 | `snapshots_equal: true`; `12254 → 12254`; `added: []`, `removed: []`, `changed: []`, `git_equal: true` | passed, không có delta quan sát được |

Các lệnh test Python phát hai `SyntaxWarning` tại dòng 3640 (`\s`) và 5783 (`\d`). AST parse cả base/master/cha 1/head cũng phát cùng cảnh báo; đây là phần cũ không đổi, không làm ba ca hồi quy thất bại. Stdout/stderr và rc đầy đủ được lưu trong [review-evidence](review-evidence/), mỗi lệnh một tệp JSON.

## Tương tác với thay đổi từ master

Đã đối chiếu độc lập qua Git, không chỉ đọc hai hiện vật cung cấp:

1. Tập 14 đường dẫn đổi từ merge-base đến master bằng đúng tập đổi từ cha 1 đến HEAD; cả 14 blob ở HEAD bằng blob tương ứng của master. Vì vậy merge không đưa thêm nội dung khác vào ngoài delta master. Hai tệp write set không có diff giữa merge-base và master, cũng không có diff giữa cha 1 và HEAD. Chi tiết đủ 14 đường dẫn nằm trong [integration.json](review-evidence/integration.json).
2. Workflow `.github/workflows/`, hook `.claude/hooks/session-start.sh`, wrapper `ops/chay_lease_publish_test.sh`, `ops/cai_cong_cu.sh`, `ops/lease_publish.py` và `ops/bash_nen.py` đều không đổi so SHA lượt 3. `git grep` các nơi gọi installer không thấy `AL_RETRY` mới trong các bề mặt đó. Bằng chứng: [callers.json](review-evidence/callers.json).
3. AST cho thấy base/master có 284 ca đăng ký và không có t237; cha 1/head đều có 285 ca, đúng một định nghĩa và một đăng ký `t237_cai_actionlint_retry_song_qua_5xx`, không có tên hàm cấp module trùng nhau. Không có ca từ master chiếm tên t237.
4. Phần runtime master đổi là NLM (`scripts/nlm_cli.py`, fragment wp1099 và registry fragment). Không thấy tham chiếu tới các module mới ấy trong test/implementation lease và `bash_nen` được kiểm tra (`rg` rc1, không khớp). AST registry xác nhận chỉ thêm `wp1099_nlm_nap_lai.py`, không xóa hay đổi fragment cũ; xem [bundled-registry.json](review-evidence/bundled-registry.json). Không nhận phép tìm chuỗi này là kiểm chứng toàn bộ runtime NLM.
5. Quét diff master tìm được 15 dòng `CMD bash ops/cai_actionlint.sh`; tất cả thuộc **log CI lịch sử** `ops/land/pr1127-wp1120-provenance/ci/gate-output-41356691133.txt`, không phải lời gọi thực thi mới. Không có thay đổi mã thực thi liên quan `AL_RETRY`, installer hay t237 trong delta master đã kiểm. Protocol chỉ thêm hàng ADR-0064 về NLM, không đổi hợp đồng review/installer; xem [master-protocol-delta.json](review-evidence/master-protocol-delta.json).

## Đối chiếu lượt trước và bảng lớp

Lượt 3 không có finding mới hay P0–P2 mở. Hai lớp lịch sử dưới đây không có thay đổi nội dung trong lượt merge này; phép đối chiếu byte/Git giữ nguyên trạng thái đã ghi tại lượt 3, không phải phép chạy lại phản chứng.

| Slug | Nguồn/trạng thái lượt 3 | Kết quả lượt 4 | Giới hạn |
|---|---|---|---|
| `retry-window-request-count-flakiness` | P3 đã đóng trên `69dbf3a…` | Giữ kết quả đã đóng: toàn bộ test, gồm D8a/D8b, giống cha 1 từng byte | Không chạy lại SIGSTOP/mutation hay chứng nhận HTTP trên head mới |
| `retry-max-time-decimal-equivalence` | P2 đã đóng trước lượt 3 | Giữ kết quả đã đóng: installer và D4 không đổi | Không chạy lại 200 đầu vào numeric |

## Findings và giới hạn

**Không có finding mới. P0–P2 mở: 0.** Không thấy tương tác từ master làm thay đổi nội dung đã review hoặc gây hồi quy trong các phép kiểm được yêu cầu.

- t237 HTTP: lệnh thật rc1 vì quyền socket; helper tại `ops/lease_publish_test.py:14636` khởi tạo `ThreadingHTTPServer` trên `127.0.0.1`. **KHÔNG ĐO ĐƯỢC**, không lấy phép thất bại hạ tầng làm kết quả chức năng hay tín dụng mutation.
- Windows t237/t35/t37/t38: **not_measured** trong phiên Linux. Toàn suite, mutation, actionlint workflow, bare Ruff và Ruff pin/probe contract: **not_run** lại lượt 4 theo phạm vi xác minh ngắn được giao. Không mượn kết quả SHA cũ làm gate pass cho SHA mới.
- Snapshot bao gồm byte/mode của tracked, untracked và ignored; không gồm metadata `.git`, nhưng kiểm riêng HEAD/tree, status, diff, danh sách index và SHA-256 index. Hai mốc giống nhau chỉ chứng minh không có delta quan sát được, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.
- Hai lỗi ban đầu trong script đo ngoài checkout đã được sửa và chạy lại; phân biệt với lỗi sản phẩm tại [setup-notes.txt](review-evidence/setup-notes.txt).

KET_LUAN: approve
