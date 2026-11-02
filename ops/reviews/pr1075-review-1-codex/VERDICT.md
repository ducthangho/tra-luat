Verdict: approve
Reviewed commit: 907c474e5dd22b2f389e8c342e7c79c6fbcb760e

Hoàn tất cross-review PR #1075 lượt 1: **approve — 0 P0, 0 P1, 0 P2, 0 P3** trong phạm vi đo offline được giao. Cổng head/base cùng xanh, delta vi phạm bằng 0; 53 tệp sao chép khớp nguồn, hai tệp loại khai đúng; 75 đối chiếu biên nhận khớp; README giữ đủ hàng cũ và thêm đúng bốn hàng. Đột biến băm bị chặn đúng tên biên nhận. Các kết quả và lệnh tái hiện ở dưới; không dùng kết luận executor làm phép đo.

Finding: không có mục `- [P0..P3] <slug>` đã xác minh. Không có hướng vá cần yêu cầu.

| Mức | Số finding |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |
| P3 | 0 |

Phạm vi là tính toàn vẹn và việc ghi sổ review #1071, không tái thực hiện nội dung review #1071. Chỉ ghi trong sandbox; phép đo/chỉnh đột biến dùng `work/{head,base,mutant}`. `git config core.abbrev 7` đã đặt trên các bản sao trước khi chạy cổng; mọi script chạy với `PYTHONDONTWRITEBYTECODE=1`. Không cấp quyền merge/land.

Kết quả đã đo đợt 1:

- `PYTHONDONTWRITEBYTECODE=1 python3 measure_archive.py` → rc0; head `907c474e5dd22b2f389e8c342e7c79c6fbcb760e`, tree `d01f444ce113e812178093aab25ce3ea9d14aeed`, merge-base `3574cb07dba8a8f7f32384ee3d1d3dfbf3a4f70e`, 58 tệp đổi, `outside_reviews=[]`, `patch_equal=true`, status rỗng. Log: `evidence/preflight.json`.
- Cùng lệnh → 55 tệp nguồn; 53 bản sao khớp byte; 55 tệp lưu trữ gồm thêm OMITTED.txt/SHA256SUMS; `sha256sum -c SHA256SUMS` rc0, 54 mục phủ đủ trừ chính manifest; bản verdict phẳng khớp. Hai tệp loại có sha256/bytes đúng, `unaccounted_source_files=[]`, `errors=[]`. Log: `evidence/archive.json`, `evidence/archive-mapping.json`, `evidence/sha256sum.log`.
- `PYTHONDONTWRITEBYTECODE=1 python3 run_checks.py` → rc0 cho cả head/base và mọi cổng. `bien_nhan_v2`: 285→286 ĐẠT v2, 338→339 tổng, 0→0 vi phạm; legacy 11/11 và 42 nợ giữ nguyên. `land_evidence_nguon`: 74 ĐẠT, tổng 99, 0 vi phạm ở cả hai. Ba hàm `t26_*`/`t27_*` đều PASS trực tiếp; doctrine-scan sạch 10 tệp; diff-check output rỗng. Lệnh con/cwd/rc: `evidence/{head,base}-gates.json`, output tại các `.log` tương ứng.


Kết quả đã đo đợt 2:

- `PYTHONDONTWRITEBYTECODE=1 python3 measure_receipt.py` → rc0, `check_count=75`, `errors=[]`. `reviewed_sha/tree`, cha thứ hai của merge `0d79022`, blob ở `629543d`, telemetry run.json, prompt/checkpoint/stdout/stderr, class trên 73 tệp và tóm tắt `ket_luan` đều khớp. Chi tiết từng đối chiếu: `evidence/receipt-checks.json`; tóm tắt và giới hạn: `evidence/receipt.json`.
- `PYTHONDONTWRITEBYTECODE=1 python3 measure_readme_history.py` → rc0; base 1209 hàng, head 1213, `removed=[]`, một hàng mục lục + ba caveat; bỏ đúng bốn hàng thì README bằng base nguyên byte. Hai merge giữ mọi hàng của cả hai cha. Log: `evidence/readme-history.json`.
- `PYTHONDONTWRITEBYTECODE=1 python3 mutate_hash.py` → rc0 của phép thử; thay riêng verdict_sha256 bằng 64 ký tự f trong bản sao `work/mutant`. `bien_nhan_v2` rc1, chỉ đúng biên nhận mới đỏ; `t26` rc1, báo LỆCH BĂM đúng tên; hai hàm t27 PASS. Khôi phục byte gốc thành công, status bản sao rỗng. Log: `evidence/mutation.json`, `evidence/mutant-*.log`.


Đối chiếu cổng — lệnh tái hiện chung từ sandbox: `PYTHONDONTWRITEBYTECODE=1 python3 run_checks.py`. Runner lưu nguyên lệnh con, cwd, mã thoát ở `evidence/{head,base}-gates.json`; output ở `evidence/{head,base}-<cổng>.log`. Cwd của các lệnh dưới là `work/head` hoặc `work/base`.

| Lệnh | Base `3574cb0` | Head `907c474` | Delta |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0; 285 ĐẠT v2, tổng 338, 0 vi phạm | rc0; 286 ĐẠT v2, tổng 339, 0 vi phạm | +1 biên nhận v2; 0 vi phạm mới |
| `python3 ops/land_evidence_nguon.py --root .` | rc0; 74 ĐẠT, 25/28 miễn trừ, tổng 99 | giống base | 0; log bằng byte |
| `python3 ../../direct_checks.py .` | rc0; cả ba hàm PASS | rc0; cả ba hàm PASS | 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0; sạch, 10 tệp, 0 chỗ chép doctrine | giống base | 0; log bằng byte |
| `git diff --check 3574cb0 HEAD` | rc0; output rỗng | rc0; output rỗng | 0 |

`direct_checks.py` import tệp test của chính checkout rồi gọi trực tiếp mọi hàm `t26_*`/`t27_*`, không chạy toàn bộ suite. Hai SyntaxWarning về `\s`/`\d` ở 3062/5205 xuất hiện ở cả base/head; `final_integrity.py` đối chiếu được `syntax_warnings_equal=true`. Không có ca được yêu cầu bị bỏ qua.

Phản chứng — `PYTHONDONTWRITEBYTECODE=1 python3 mutate_hash.py` chỉ thay một trường `verdict_sha256` trên bản sao tạm, giữ hash có hình dạng hợp lệ. Output `bien_nhan_v2` rc1:

> ĐỎ pr1071-review-1-codex-verdict.receipt.yaml: blob tại `evidence_url` băm 8b8f3d9c709f… nhưng biên nhận khai `verdict_sha256` ffffffffffff… — mỏ neo KHÔNG trỏ đúng thứ nó khai.

Cùng phép thử: `t26` FAIL với `LỆCH BĂM`, đúng tên tệp trên; cả hai `t27` PASS. `red_receipts` chỉ có một tệp này; `restored_bytewise=true`, `status_after=""`. Log: `evidence/mutation.json`, `evidence/mutant-bien-nhan.log`, `evidence/mutant-direct.log`.

Kiểm kê byte — `PYTHONDONTWRITEBYTECODE=1 python3 measure_archive.py` đối chiếu toàn bộ tệp, gồm `launcher.out ↔ launcher.json`, `run/* ↔ runs/94bf0499/*`, `evidence/*.py ↔ *.py` ở gốc nguồn. 53/53 bản sao khớp byte; hai tệp bổ sung do ghi sổ là `OMITTED.txt` và `SHA256SUMS`. `sha256sum -c SHA256SUMS` tại `work/head/ops/reviews/pr1071-review-1-codex` → rc0, 54 dòng OK; tập manifest đúng toàn bộ tệp trừ chính nó, không trùng mục. Verdict phẳng cũng khớp `nguon/review1071a/VERDICT.md`.

| Tệp nguồn không đưa vào kho | Bytes đo được | SHA256 đo được | Đối chiếu OMITTED.txt |
|---|---:|---|---|
| `DIFF.patch` | 358925 | `f99409474b3e9f3a43825cc71c3cad7eacb7ce80346e260cea55711752431deb` | đúng |
| `evidence/readme.diff` | 4902 | `031d91875474e867f2572eeed3ed9e816ae358dd57bee778f2c3bfdf8d9fdae4` | đúng |

Cùng script chạy `git diff 97120d3 0104461` → bằng byte `DIFF.patch` nguồn; `unaccounted_source_files=[]`. Các thư mục clone/nguồn con được khai loại nhưng không có trong đầu vào: nội dung bên trong **KHÔNG ĐO ĐƯỢC**, không coi việc liệt kê tên thư mục là kiểm kê từng tệp của chúng.

Biên nhận — `PYTHONDONTWRITEBYTECODE=1 python3 measure_receipt.py` → rc0, 75 đối chiếu, `errors=[]`; từng cặp actual/expected nằm trong `evidence/receipt-checks.json`.

| Trường | Output đo độc lập từ git/tệp nguồn |
|---|---|
| Verdict và đếm dòng finding | `approve`; P0/P1/P2/P3 = 0/0/0/0; IDs rỗng |
| `reviewed_sha` | `01044616f0258e41608feac5b01f80770beec7a5` |
| `reviewed_tree` | `eeca0a4c72f3995d462161d3572f8fb1769a9125` |
| Verdict bytes/SHA256 | 12716; `8b8f3d9c709fcf7f9222c45c20440a47248ef38a24c2b3ae83a2ac552f720b78` |
| `land_merge_commit` | `0d7902229d3050bc58fa880abf267f0fafa335bf` |
| Hai cha của merge | `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`, `01044616f0258e41608feac5b01f80770beec7a5` |
| `evidence_url` commit | `629543d80388593df53e9bfbe181af2b52b007b1`; blob bằng byte verdict nguồn, băm đúng receipt |
| `run_id` | `94bf04993a7d4189a78fe43a4b261cea` |
| `ma_thoat`, trạng thái, thời lượng | 0; `xong`; 506.024 giây; chênh hai timestamp 506.02367 giây |
| Sự kiện model, model, effort | 27 sự kiện với 27 response_id khác nhau; chỉ `gpt-6-astra`; `xhigh` |
| `prompt_sha256` | `96dd3f7144b7584f455221418a4050adb7d422be72eb4016bc28ef1dddf1cec9` |
| `sandbox_trang_thai` | `DO_DUOC` trong run.json lịch sử, với giới hạn lấy mẫu được giữ nguyên |
| `_tinh_lop_tu_write_set(git diff --name-only 97120d3 0104461)` | 73 tệp, toàn bộ `ops/reviews/**`, trả `sensitive` |

Cùng script: `git merge-base --is-ancestor 629543d HEAD` và `git merge-base --is-ancestor 629543d 16f9658` → rc0; `git show 629543d:<verdict_path>` khớp byte/băm nguồn. `git merge-base --is-ancestor 0d79022 origin/master` → rc0. `git merge-base 0104461 0d79022^1` → `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`. Commit date của `0d79022` là `2026-10-31T16:54:03+07:00`; đây là thời gian commit cục bộ, không dùng thay `merged_at` của GitHub.

`launcher.json` parse bằng run.json; băm/bytes stdout và stderr đúng run.json; checkpoint có băm đúng và cùng run_id/head/prompt. Các model/effort trong bảng được đối chiếu telemetry lưu lại, không suy từ cờ CLI. `ket_luan` khớp dòng 4 verdict gốc và phép đếm trên các log nguồn: 64 tệp chép, 3 tệp loại, 116 đối chiếu, 9 hàng README, hai đột biến. Đây là kiểm tính trung thực của câu tóm tắt review #1071; không tuyên bố đã chạy lại review đó hoặc có lại các thư mục nguồn của #1058.

README/lịch sử — `PYTHONDONTWRITEBYTECODE=1 python3 measure_readme_history.py` → rc0, `errors=[]`. Tập đa hàng `| ` (giữ cả số lần lặp) của base có 1209 hàng, head có 1213, không mất/đổi hàng cũ. Bốn hàng mới gồm đúng một mục lục và ba caveat. Mọi ID và mô tả caveat bằng receipt; verdict/assurance, lượt/PR, đếm P*, head, merge, bytes, run ID, model và liên kết cùng khớp. Bỏ bốn hàng mới khỏi toàn văn README → bằng base nguyên byte.

| Merge | Hàng cha thứ nhất | Hàng master/cha thứ hai | Hàng sau merge | Thiếu so từng cha |
|---|---:|---:|---:|---:|
| `1907678` | 1123 | 1176 | 1180 | 0 / 0 |
| `907c474` | 1180 | 1209 | 1213 | 0 / 0 |

Cùng script: `git diff --name-only <commit>^1 <commit>` → `629543d` có 56 tệp hiện vật; `16f9658` chỉ README và receipt. `measure_receipt.py` chạy diff từ `16f9658` đến HEAD giới hạn thư mục hiện vật, verdict phẳng và receipt → output rỗng. Hai merge không đổi các hiện vật này. Delta cần review vẫn là 58 tệp `ops/reviews/**` so base đã giao, không phải toàn bộ thay đổi master đi vào mỗi merge.

Tiền lệ — cùng `measure_receipt.py`, `evidence/receipt.json.precedents`: 21 trường cấu trúc/kết quả được chọn so với pr1058 lượt 2 và pr1050 lượt 2 có `fixed_field_differences={}`; cùng loại/cường độ neo và ba ID caveat. So với pr1058 lượt 1, khác biệt verdict/assurance/đếm/IDs có nguồn từ verdict approve, và không cần caveat lỗi lấy mẫu vì run.json lần này ghi `DO_DUOC`. Số tệp, lượt, model event, prompt và thời lượng được đo riêng, không sao nguyên số của tiền lệ. Không tìm thấy sai lệch thiếu lý do trong phần đã đối chiếu.

Giới hạn và lời khai vượt phần đo độc lập — `PYTHONDONTWRITEBYTECODE=1 python3 measure_receipt.py` lưu các mục `unmeasured` trong `evidence/receipt.json`. Không suy các mục này từ cổng xanh:

- `land_merge_commit_ghi_chu` nói tới `merge_method merge`, `expectedHeadSha`; git chỉ cho phép đo đồ thị hai cha và SHA cha thứ hai. Tham số request GitHub, trạng thái PR/CI hiện tại, actor/quyền tài khoản, URL đã được phục vụ công khai: **KHÔNG ĐO ĐƯỢC**. Nhãn `(a)` trong ghi chú không làm các phần API này thành bằng chứng git.
- `model_reviewer_identity.cli` khai `codex-cli 0.164.0`, lệnh launcher và các cờ; run.json chỉ giữ chương trình/số đối số/vân tay, không giữ toàn argv hoặc phiên bản binary. Phiên bản CLI, cờ launcher lịch sử và model/effort yêu cầu: **KHÔNG ĐO ĐƯỢC**. Model/effort được phục vụ có đối chiếu telemetry như bảng trên.
- Danh tính/họ model executor, chỉ thị chủ kho, việc không fork hoặc tái sử dụng context ngoài prompt/run/checkpoint đã cung cấp: **KHÔNG ĐO ĐƯỢC** độc lập. Việc receipt khai `cross_approved` khớp tiền lệ/nguồn không phải tái chứng thực các danh tính này.
- `run.json.sandbox_gioi_han` ghi lấy mẫu mỗi 0.2 giây, lệnh ngắn có thể lọt; `DO_DUOC` chỉ nói đã quan sát cơ chế sandbox. Cưỡng chế mọi lệnh của lượt lịch sử: **KHÔNG ĐO ĐƯỢC**. Ba caveat đã được nâng đủ lên README.

Toàn vẹn cuối — `PYTHONDONTWRITEBYTECODE=1 python3 final_integrity.py` → rc0, `errors=[]`; `git status --porcelain=v1 --untracked-files=all --ignored` rỗng tại `cay-kho`, `work/head`, `work/base`, `work/mutant`; head/tree của kho được review giữ nguyên. Output xác nhận các cổng head/base rc0, đột biến được khôi phục, log land/doctrine/diff-check head/base bằng byte. Chi tiết: `evidence/final-integrity.json`. Không sửa kho `cay-kho/`; không cấp quyền merge/land.
