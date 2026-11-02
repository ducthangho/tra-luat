Verdict: approve
Reviewed commit: 01044616f0258e41608feac5b01f80770beec7a5

Hoàn tất cross-review PR #1071 lượt 1: **approve — 0 P0, 0 P1, 0 P2, 0 P3** trong phạm vi đo offline bên dưới. Các cổng head/base đều qua, không có delta vi phạm; 64 tệp được chép khớp byte nguồn, 3 tệp bị loại đều được khai đúng; 116 đối chiếu biên nhận và 9 hàng README khớp. Hai đột biến băm bị cổng chặn đúng tên tệp. Kết luận dựa trên các script mới và output ghi trong sandbox, không dùng kết luận của executor làm kết quả đo.

Phạm vi: cross-review PR #1071 lượt 1; nguồn đối chiếu là git tại chỗ và hai thư mục `nguon/review1058{a,b}`. Các sự kiện GitHub không có bằng chứng tại chỗ: KHÔNG ĐO ĐƯỢC. Không cấp quyền merge/land.

Finding: không có mục `- [P0..P3]` đã xác minh. Ngưỡng áp dụng: không còn bất kỳ P0/P1/P2/P3 nào.

| Mức | Số finding |
|---|---|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |
| P3 | 0 |

Tiền kiểm — `PYTHONDONTWRITEBYTECODE=1 python3 setup_review.py` → head đúng `01044616f0258e41608feac5b01f80770beec7a5`, tree `eeca0a4c72f3995d462161d3572f8fb1769a9125`; merge-base với `origin/master` đúng `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`; `core.abbrev=7`; status rỗng; `changed_count=73`, `outside_reviews=[]`, `patch_equal=true` (rc0). Chi tiết: `evidence/preflight.json`, `evidence/changed-paths.txt`.

Byte — `PYTHONDONTWRITEBYTECODE=1 python3 measure_bytes.py` → rc0, `errors=[]`. Lượt 1: 32 tệp nguồn, 31 tệp được chép khớp byte; lượt 2: 35 tệp nguồn, 33 tệp được chép khớp byte. Hai bản phẳng khớp `VERDICT.md` gốc. `sha256sum -c SHA256SUMS` tại mỗi thư mục lưu trữ đều rc0 (32 và 34 mục), phủ toàn bộ tệp trừ chính `SHA256SUMS`. Hai tệp thêm để kiểm kê là `OMITTED.txt` và `SHA256SUMS`, không phải bản sao từ nguồn. Chi tiết ánh xạ từng tệp: `evidence/bytes-{1,2}-mapping.json`; kết quả: `evidence/bytes.json`, `evidence/bytes-{1,2}-sha256sum.log`.

Tệp nguồn vắng trong kho đều khai đúng trong `OMITTED.txt` (cùng lệnh trên): lượt 1 `DIFF.patch`, 605514 bytes, SHA256 `a8e3d2e479804d07751849d0dc4f74a2ae4c7d5613473833a8a3a9470a1ed8da`; lượt 2 `DIFF.patch`, 605759 bytes, SHA256 `de3c02ede2307ec3722563d52c4bb8e85b98583f51319e70fcfb660407e8c670`, và `evidence/gates-summary.log`, 4388 bytes, SHA256 `187c6b3825a453904074bdfdfe3ed2c244694c74af34b670280df437bc77c682`. Không tìm thấy tệp nguồn được cung cấp bị bỏ sót mà không khai. Các bản clone gốc không có trong đầu vào nguồn nên nội dung các thư mục clone đã bỏ: KHÔNG ĐO ĐƯỢC.

Cổng — `PYTHONDONTWRITEBYTECODE=1 python3 run_gates.py cay-kho head` và `PYTHONDONTWRITEBYTECODE=1 python3 run_gates.py base-copy base` → tất cả rc0. Runner ghi đầy đủ lệnh con, cwd, output và rc tại `evidence/{head,base}-gates.json`.

| Lệnh (cwd = checkout tương ứng) | Base `97120d3` | Head `0104461` | Delta |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | 262 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm, tổng 315 | 264 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm, tổng 317 | +2 v2; 0 vi phạm mới |
| `python3 ops/land_evidence_nguon.py --root .` | 68 ĐẠT, 25/28 miễn trừ, 0 vi phạm, tổng 93 | giống base | 0; log khớp byte |
| `python3 ../direct_gates.py .` | PASS cả 3 hàm `t26_*`/`t27_*` | PASS cả 3 hàm | 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | sạch, 10 tệp, 0 chỗ chép doctrine | giống base | 0 |
| `git diff --check 97120d3 HEAD` | output rỗng | output rỗng | 0 |

`direct_gates.py` import `ops/lease_publish_test.py` rồi gọi trực tiếp từng hàm phù hợp, bao gồm ca phản chứng đuôi HOA. Hai `SyntaxWarning` tại dòng 3062/5205 có ở cả head và base; không có test bị bỏ qua.

Đột biến — `PYTHONDONTWRITEBYTECODE=1 python3 mutate_receipts.py` (chỉ ghi vào `mutation-copy/`) đổi riêng `verdict_sha256` thành chuỗi 64 ký tự `f`, giữ kiểu chuỗi và hình dạng hash hợp lệ. Với từng biên nhận lượt 1/2: `bien_nhan_v2` rc1, chỉ đúng `pr1058-review-{1,2}-codex-verdict.receipt.yaml`, output “blob tại `evidence_url` băm f062f215087c…/00046bcde939… nhưng biên nhận khai … ffffffffffff… — mỏ neo KHÔNG trỏ đúng thứ nó khai”; `t26` rc1, output `LỆCH BĂM` và đúng tên tệp. Hai ca `t27` vẫn PASS; `land_evidence_nguon`/`doctrine-scan`/`git diff --check` vẫn rc0 (không phải cổng băm biên nhận mới này). Chi tiết: `evidence/mutations.json`, `evidence/mutant-{1,2}-*.log`. Mỗi lần thử đều khôi phục byte bản sao trong `finally`.

Biên nhận — `PYTHONDONTWRITEBYTECODE=1 python3 measure_receipts.py` → rc0, `check_count=116`, `errors=[]`. Log từng phép đối chiếu: `evidence/receipts-checks.json`; tóm tắt: `evidence/receipts.json`.

| Trường đo từ git/tệp nguồn | Lượt 1 | Lượt 2 |
|---|---|---|
| Verdict; số P0/P1/P2/P3 từ dòng finding | `changes_requested`; 0/0/1/1 | `approve`; 0/0/0/0 |
| `reviewed_sha` | `5dd347c67da680099e292acf02da7e363a0559bd` | `3534a6ec9b343cfa484142b14b7c7db7fd3b6f6e` |
| `reviewed_tree` | `7176a9306859b0b772d49d6ddf9d5ddca0cf8167` | `ef593ba2deffcac3b4fb3dbf6968e8bdd6a8aeb1` |
| Verdict bytes | 13159 | 13506 |
| Verdict SHA256 | `f062f215087cab163ac378a5582002842c8a50312fd1fc748a8942a4115bee7e` | `00046bcde93988d97ddd02a9a0a57710d60ad2aa1a142781baecb0a8c7840c27` |
| `run_id` | `f98dce6d25d347dc94348c1d5b9d399c` | `488b7693d2e84d30ac43cc5215eafaaa` |
| `ma_thoat`; trạng thái; thời lượng | 0; `xong`; 481.586 giây | 0; `xong`; 405.176 giây |
| Số sự kiện model; tập model; effort | 27; `gpt-6-astra`; `xhigh` | 20; `gpt-6-astra`; `xhigh` |
| `prompt_sha256` | `c7908dff5728e24280f66a1116dbe2eba9b46fe41d4a54171c1ede482d1b23b8` | `230fd3b21078dc4edf7952895f2d411e8cb507b2062f00ea302d15d90ef164e9` |
| `sandbox_trang_thai` | `KHONG_DO_DUOC`; lý do `luong lay mau sandbox hong (DanhTinhDoi)` | `DO_DUOC` |
| `git diff --name-only afc82f6 <reviewed_sha>` → `_tinh_lop_tu_write_set` | 51 tệp → `sensitive` | 51 tệp → `sensitive` |

Cùng script trên đo `git merge-base --is-ancestor <reviewed_sha> 9c7dc11` → rc0 cho cả hai lượt; `git show -s --format=%P 9c7dc11` → hai cha `3376d539b980ab1f4ee49d9932dd15bbac157441` và `3534a6ec9b343cfa484142b14b7c7db7fd3b6f6e`. `9c7dc11` là tổ tiên của base; merge-base giữa hai reviewed head và cha thứ nhất của merge đều là `afc82f6d7447eb76fc8adbe46c1be90be88d331f`. Hai `evidence_url` neo đúng `3145d821aecc6689dd64f197859f9aa1f43b27a7`; `git merge-base --is-ancestor 3145d82 HEAD` → rc0; `git show <anchor>:<verdict_path>` khớp nguyên byte và băm verdict. `3145d82` cũng là tổ tiên `c92c709`.

Cùng script đối chiếu `launcher.out` với `run/run.json` sau parse JSON → bằng nhau; băm/bytes stdout, stderr và checkpoint đều khớp run.json; checkpoint khớp run_id/head/prompt. Thời lượng từ hai timestamp là 481.585985 và 405.175532 giây, làm tròn 3 chữ số khớp biên nhận. `git diff afc82f6 <reviewed_sha>` tái tạo đúng hai `DIFF.patch` bị loại; `git diff 5dd347c 3534a6e` khớp `DIFF-LUOT2.patch`; `VERDICT-LUOT1.md` ở nguồn lượt 2 khớp verdict lượt 1.

README — `PYTHONDONTWRITEBYTECODE=1 python3 measure_readme.py` → rc0, `index_rows=2`, `caveat_rows=7`, `errors=[]`; mọi kiểm số đếm, verdict/assurance, run ID/model, head, bytes, liên kết receipt, tập ID caveat và nội dung cảnh báo đều true. Bỏ riêng 9 hàng mới → toàn bộ README còn lại bằng base nguyên byte (`readme_minus_new_rows_equals_base_bytewise=true`). 1115 hàng bảng có sẵn ở `origin/master`/base/cha thứ hai của merge được giữ, `missing_or_changed=0`; 1124 hàng ở cha thứ nhất cũng giữ nguyên. Chi tiết: `evidence/readme.json`, `evidence/readme.diff`.

Tiền lệ và lời khai đóng finding — `PYTHONDONTWRITEBYTECODE=1 python3 measure_context.py` → rc0, `errors=[]` (`evidence/context.json`). Các trường schema/kind/packet/role/provider/class/assurance/verdict/cách đếm/independence/review_axes/nguồn có thẩm quyền so với lượt tương ứng của pr1050: `fixed_field_mismatches={}`; loại/cường độ mỏ neo bằng nhau. Lượt 1 thêm đúng caveat `SANDBOX-MODE-KHONG-DO-DUOC`, có nguồn là trạng thái và lý do trong run.json; lượt 2 giữ ba ID caveat của tiền lệ. Model và số sự kiện khác tiền lệ có nguồn đo ở run.json; lượt 2 khai thêm tệp bỏ `evidence/gates-summary.log`, đã băm đúng và đo thấy whitespace cuối dòng. Việc executor tự ghi sổ được nói rõ trong comment đầu biên nhận, cùng dạng khai minh bạch đã có ở pr1056; đây không phải chứng minh danh tính người vận hành.

Cùng script lấy blob bằng `git show 5dd347c:ops/land/pr1047-wp1045-land-evidence.yaml` và `git show 3534a6e:ops/land/pr1047-wp1045-land-evidence.yaml`: câu suy ủy quyền từ merge đã được thay bằng “Readback chi chung minh THAO TAC merge … chua co nguon duyet land ben neo exact SHA 2014602”; điều kiện (5) vẫn `CHUA DAT`, `trang_thai_packet.landed=false` trước/sau. Đọc `readback-jobs-41099486628.json` ở `3534a6e` → 15 success/1 skipped, 14 job gate đã chạy và cả 14 có `windows-latest`; job `gate-cong-cu-gop` skipped, `labels=[]`, `runner_id=null`. Vì vậy lời khai hai finding cũ đã đóng khớp thay đổi và readback tại chỗ. Không coi readback là phép kiểm GitHub trực tiếp.

Lịch sử — cùng script chạy `git diff --name-only <commit>^1 <commit>`: `3145d82` thêm 70 tệp hiện vật; `c92c709` chỉ đổi README và hai receipt; merge `0104461` so với cha thứ nhất chỉ nhận `ops/specs/cloud-setup-p2b-wire-r1.md` từ master. Tệp đó không thuộc delta so base `97120d3`; phép đo phạm vi ban đầu vẫn là 73 tệp, toàn bộ `ops/reviews/**`.

Giới hạn bằng chứng (được liệt kê bởi `measure_context.py` trong `evidence/context.json`; không suy các điều này từ cổng xanh):

- Sự kiện GitHub hiện tại, actor/quyền tài khoản, việc URL đã được phục vụ công khai, thời điểm GitHub merge `2026-10-31T07:39:59Z`, và tham số request `expectedHeadSha`: **KHÔNG ĐO ĐƯỢC**. `git show -s --format=%cI 9c7dc11` → `2026-10-31T14:39:58+07:00` (07:39:58Z) chỉ là giờ commit, không phải phép đo `merged_at`; cha thứ hai khớp reviewed head không chứng minh tham số của request merge.
- Phiên bản binary `codex-cli 0.164.0`, toàn bộ lệnh launcher lịch sử và cờ yêu cầu model: **KHÔNG ĐO ĐƯỢC** từ tệp cung cấp. Các model/effort đã phục vụ trong bảng trên là đối chiếu với telemetry được lưu, không phải suy từ cờ CLI. `run.json.version=1.5.0` là phiên bản bản ghi launcher, không dùng làm chứng cứ phiên bản Codex.
- Danh tính/họ model của executor, chỉ thị của chủ kho, việc không fork/tái sử dụng context ngoài prompt/run/checkpoint được cung cấp: **KHÔNG ĐO ĐƯỢC** độc lập ngoài lời khai trong hồ sơ. Đối chiếu định lượng không xác thực các lời khai này.
- `sandbox_trang_thai=DO_DUOC` của lượt 2 chỉ có nghĩa đã quan sát cơ chế sandbox. Chính `run.json.sandbox_gioi_han` ghi lấy mẫu mỗi 0.2 giây, lệnh ngắn có thể lọt và không chứng minh mọi lệnh chạy trong sandbox. Cưỡng chế toàn bộ lượt chạy: **KHÔNG ĐO ĐƯỢC**; lượt 1 còn ghi rõ lỗi lấy mẫu. Báo cáo này không nâng các trạng thái đó thành bảo đảm toàn phiên.

Toàn vẹn cuối — `PYTHONDONTWRITEBYTECODE=1 python3 final_integrity.py` → rc0, `errors=[]`; head/tree giữ nguyên; `git status --porcelain=v1 --untracked-files=all --ignored` rỗng ở `cay-kho`, `base-copy`, `mutation-copy`; toàn bộ gate rc0 tại head/base, số lỗi của bốn nhóm phép đo đều 0; hai đột biến bị chặn; log land/doctrine/diff-check head/base bằng byte. Chi tiết: `evidence/final-integrity.json`. Không sửa nội dung kho được review; cấu hình `core.abbrev=7` đã đặt theo yêu cầu trước phép đo. Không cấp quyền merge/land.
