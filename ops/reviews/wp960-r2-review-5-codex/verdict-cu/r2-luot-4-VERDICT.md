verdict: changes_requested
reviewed_sha: 3a52e6d194d08a755793cf449f393fb15b56757b
Kết quả: 0 P0, 4 P1, 0 P2, 0 P3.

## Nhật ký tăng dần

- Đã đọc `run/2997494e/prompt.snapshot`. Phạm vi: review độc lập, chỉ đọc cây `cay-kho/`; mọi fixture/đột biến trên bản sao tạm; không gọi mạng.
- Đang xác minh SHA, đặc tả đóng băng, lease và finding lượt 3 trước khi chạy phép đo.

### Hướng 1 — định danh và phạm vi
Lệnh: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`; `git -C cay-kho status --short`; `sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md` (log: `evidence/preflight.log`).
Output: HEAD `3a52e6d194d08a755793cf449f393fb15b56757b`; tree `97ba989c22cbde6bd24cdd33671d9e7f2442ae58`; status rỗng; shallow=false; spec SHA256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca`. Git 2.43.0, Python 3.13.17, Ruff 0.17.3. Lease g2 ghi cùng base/write set/budget; lệnh review không suy execution surface từ tên launcher/lease. Numstat hai tệp so base: +294/-193 và +643/-104, tổng 1.234 dòng. Diff tổng còn có thay đổi từ merge master; không quy chúng thành sửa ngoài write set của packet.

### Hướng 2 — doctrine
Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` tại `cay-kho/`.
Output thật: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0 (`evidence/doctrine.log`). Suite đầy đủ và gate corpus đã bắt đầu; chưa kết luận trước khi có output cuối.

### Hướng 3 — gate corpus, Ruff và diff
Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .` trên cây review; `python3 gate_checks.py`.
Output (`evidence/gate.log`, `evidence/checks.log`): gate rc=0, **244 ĐẠT v2 · 11/11 legacy · 42 nợ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · 297 receipt**, nợ lịch sử **1/60/0**, `TỔNG: ĐẠT`. Ruff base/head mỗi bên rc=1 với đúng **1 F541** tại test dòng 1677, **delta 0**. `git diff --check 4488444 HEAD`: rc=0, stdout/stderr rỗng. Diff từ parent đã merge `43b96f0` chỉ hai tệp packet.

### Hướng 4 — chạy lại phản chứng lượt 3, nhóm A
Lệnh: `python3 -B -u replay_extra_recheck.py extra replace-drop-parent graft-silent foreign-git-dir`; `python3 -B -u replay_probe_recheck.py partial`; `python3 -B -u replay_rc_witness_recheck.py`.
Output (`evidence/replay-a.log`, `partial.log`, `rc-witness.log`): replace-drop-parent không còn đổi phép đo (rc=1 không nợ, rc=0 có nợ); graft đã tắt warning => rc=2 cả hai lượt; GIT_DIR kho khác không còn đổi kết quả (1/0). Partial clone file:// thật, **4 blob vắng, 1 promisor pack**, không extensions.partialclone => bị chặn đúng `remote.<x>.promisor`, rc=2. Wrapper merge-base rc=128/stderr rỗng => rc=2 cả có/không nợ. Script witness cũ sau phần head vấp thư mục mutant lượt trước đã tồn tại: lỗi GIÀN GIÁO reviewer, không finding; sẽ chạy lại head riêng. Nhóm B object sai băm/graph sai parent im lặng được giữ là tiền đề theo quyết định chủ kho, không lập lại finding.

### Hướng 5 — môi trường và cấu hình hợp lệ
Lệnh: `python3 -B -u new_probes.py config` (`evidence/config.log`).
Output: HOME/includeIf và XDG fsync cũ vẫn giữ đúng rc=1; linked worktree bình thường rc=1, fsck=0. Kho đủ chỉ thêm `remote.archive.promisor=false` (cũng thử `no`, `off`): fsck=0, merge-base=0/stderr rỗng nhưng gate từ rc=1 thành **rc=2/partial clone**. Giá trị `0` làm fsck Git 2.43.0 rc=128 nên KHÔNG dùng biến thể ấy làm đối chứng kho lành. Dời nguyên object store sang pool rồi trỏ GIT_ALTERNATE_OBJECT_DIRECTORIES: Git thật/fsck=0, merge-base=0 nhưng gate rc=2/OID không tra được — đang đối chiếu phạm vi cô lập có chủ ý trước khi phân loại.

### Hướng 6 — stderr nền và điều kiện lỗi
Lệnh: `python3 -B -u new_probes.py stderr` (`evidence/stderr.log`); wrapper chuyển tiếp Git thật, chỉ biến đổi stderr ở các lệnh khai trong script.
Output: stderr lỗi CHỈ ở `rev-parse --git-dir` bị nhận làm nền, gate ra 1/0 thay vì 2; warning vô hại lặp lại được trừ (1/0); lỗi KHÁC ở merge-base vẫn bị chặn 2/2. Thử dòng warning ref hỏng trùng nền bị chặn bởi chốt rc=128 của `symbolic-ref` (2/2), nên không gọi thử ấy là bypass. Đang bổ sung đối chứng lỗi merge-base trùng dòng nền để kiểm đúng phép trừ.

### Hướng 7 — lỗi trùng dòng nền (đối chứng âm/dương)
Lệnh: `python3 -B -u stderr_extra.py stderr` (`evidence/stderr-extra.log`). Fixture `_kho_cau` nguyên trạng; wrapper Git thật in cùng `error: probe cannot inspect repository state` ở lần lấy nền và ở merge-base. Chỉ biến đổi câu trả lời merge-base thành rc=1 dù M là tổ tiên.
Output: HEAD **rc=0/TỔNG: ĐẠT khi không nợ**, **rc=1/NỢ CHẾT khi có nợ**, không KHÔNG ĐO ĐƯỢC: phép trừ đã nuốt chẩn đoán lỗi và tin sai kết quả. Đối chứng cùng dòng nhưng rc=128 => **2/2** đúng; stderr KHÁC dòng nền => **2/2** đúng. Đây là mô phỏng giao thức bằng wrapper (như c96), KHÔNG khai là lỗi đã gặp với Git thật nguyên trạng. Không thuộc nhóm B vì stderr lỗi KHÔNG rỗng. Wrapper cảnh báo chỉ ở lệnh đo cũng bị 2; chưa tìm thấy cảnh báo vô hại tự nhiên của Git không có ở probe đầu, nên không tách nó thành finding.

### Hướng 8 — suite đầy đủ, corpus không nợ và mô phỏng CI
Lệnh: `python3 -B -u /tmp/wp960-r4-copy/ops/bien_nhan_v2_test.py`; `python3 -B -u corpus_review.py`; `python3 -B -u ci_review.py`.
Output (`evidence/suite.log`, `corpus.log`, `ci.log`): **93/93 ca · 128/128 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM · 110/128 khai đối chứng**, rc=0/TỔNG: ĐẠT. Corpus: 297 receipt, 99 lần xuất hiện/31 token phân biệt; resolver không đổi token nào so lượt 3; 61/61 khóa vi phạm trùng tập nợ, unknown=0. Nợ rỗng => **rc=1, đúng 61 dòng ba luật, 0 lỗi khác, 0 unknown**. CI local: tạo merge commit **c959746fa10dcee16d4fba0e86ed086391690363**, hai parent `2618eb4e…` + reviewed SHA, tree **97ba989c…** trùng candidate, shallow=false, origin/HEAD vắng, origin/master=2618eb4e… => **gate rc=0/TỔNG: ĐẠT, nợ 1/60/0**. Đây là mô phỏng local fetch-depth:0, không phải CI GitHub online.

### Hướng 9 — đo riêng các mutant chính thức
Lệnh: `python3 -B -u targeted_recheck.py` (`evidence/target-mutants.log`), trích AST các lời gọi `do` có sẵn để chạy riêng **m103, m114, m125–m131**.
Output: **9/9 `giet_that`, đối chứng 9/9 qua**. m103 giết c91/git vắng, m114 giết c91/ref hỏng, m125 giết c96/rc=3 không stderr; m126 giết c95/trace; m127 replace; m128 fsync warning; m129 c91 partial thật; m130 c91 grafts; m131 c95 ref con. Không gán kết quả suite đầy đủ thay cho phép đo từng mutant này.

### Hướng 10 — survivor mới có witness
Lệnh: `python3 -B -u review_mutations.py u1-health-probe-rc ...`; `python3 -B -u health_rc_witness.py` (`evidence/mutants-a.log`, `health-rc-witness.log`).
Output: chỉ bỏ **`if p.returncode != 0` của probe `rev-parse --git-dir`**, giữ nguyên vế rc trong `_git_do` mà m125 kiểm => **93/93, red=[]**. Wrapper trả CHỈ lệnh probe rc=3/stdout/stderr rỗng: HEAD rc=2/2; mutant rc=1 không nợ, rc=0 có nợ. Vì chốt mới có witness sai hành vi nhưng không ca nào đỏ, thiếu răng M6 vẫn tái xuất ở một chốt khác. Đột biến này khác m125–m131 cả vị trí lẫn tác động: m125 không chạm lệnh probe trực tiếp `_chay_git`.

## FINDING

### stderr-nen-nuot-loi-that [P1] Trừ mọi dòng stderr của probe đầu cho phép lỗi đo trở thành sạch hoặc NỢ CHẾT
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1168`, `ops/bien_nhan_v2.py:1151`.
VẤN ĐỀ: `_kho_lanh` nhận toàn bộ stderr của một lần `rev-parse --git-dir` làm nền mà không xác minh chúng vô hại hoặc lặp ở mọi lệnh. `_git_do` xoá mọi lần xuất hiện trùng chữ, kể cả chẩn đoán lỗi của phép đo sau. Vế rc không cứu được khi merge-base trả 1 (mã sạch hợp lệ cho “không là tổ tiên”). Như vậy M2 bị phá ngay ở biên lỗi mới; stderr lỗi chỉ xuất hiện ở probe đầu cũng bị tin trong im lặng.
ĐÃ THỬ NGHIỆM: `python3 -B -u stderr_extra.py stderr`, case `same-error-wrong-ancestry` (`evidence/stderr-extra.log`). Dùng fixture có sẵn `_kho_cau` với M đã vào master, không sửa object/graph/ref/receipt. Wrapper chuyển tiếp Git thật, in cùng dòng lỗi ở probe đầu và merge-base, đổi merge-base thành rc=1. HEAD: **rc=0/TỔNG: ĐẠT không nợ; rc=1/NỢ CHẾT có nợ**, thay vì rc=2. Cùng thông báo nhưng rc=128 => **2/2**; thông báo khác nền => **2/2**. `new_probes.py stderr`, case `first-only-error`: lỗi chỉ ở probe đầu cũng ra **1/0**. Đây là fault injection của giao thức, không phải tuyên bố Git thật tự phát ra chuỗi lỗi giả này. KHÔNG thuộc nhóm B: stderr ở lệnh sai không rỗng, nên tiền đề tính toàn vẹn object/commit-graph không miễn được phép bỏ chẩn đoán đó.
ĐỘ TIN: cao

### promisor-false-bi-coi-la-partial [P1] Cấu hình tắt promisor bị coi thành bật và chặn nhầm kho đầy đủ
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1174`.
VẤN ĐỀ: Lệnh `config --get-regexp` được kiểm bằng stdout `.strip()`, nên chỉ cần tồn tại khóa `remote.<x>.promisor` là bị chặn. `remote.archive.promisor=false` là giá trị boolean tắt hợp lệ, không biến kho đủ thành partial. Cấu hình này làm trạng thái vi phạm đo được rc=1 hoặc corpus sạch rc=0 thành KHÔNG ĐO ĐƯỢC/2. Chốt mới thiếu phân biệt giá trị boolean.
ĐÃ THỬ NGHIỆM: `python3 -B -u new_probes.py config`, các case `promisor-false`, `promisor-no`, `promisor-off` (`evidence/config.log`). Kho dựng bằng `_kho_cau`, Git thật `fsck --full` rc=0, merge-base rc=0/stderr rỗng; chỉ thêm khóa tắt => gate **1→2**, lý do partial clone. Không dùng biến thể `0` (fsck Git 2.43.0 rc=128) làm bằng chứng kho lành. `python3 -B -u corpus_environment.py`: trên corpus nguyên byte tại cùng SHA, chỉ thêm `remote.archive.promisor=false` làm **rc=0→2** (`evidence/corpus-environment.log`).
ĐỘ TIN: cao

### xoa-alternates-hop-le-lam-mat-object [P1] Loại GIT_ALTERNATE_OBJECT_DIRECTORIES làm kho đầy đủ mất nguồn object hợp lệ
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1134`, `ops/bien_nhan_v2.py:1141`.
VẤN ĐỀ: Bỏ tất cả `GIT_*` cũng bỏ đường dẫn object pool của một kho hợp lệ. Biến alternates không đổi repository/default ref được chọn bởi `--root`; nó cung cấp object đúng hash cho chính kho đó. Do đó đây là hồi quy khác với việc cần bỏ `GIT_DIR` trỏ kho ngoài. Cổng giờ báo OID không tra được/2 trong khi Git thật đo đầy đủ được cùng object/ref và repo không shallow/partial. Giới hạn “chỉ hỗ trợ alternates ghi trong tệp” không có trong đặc tả đóng băng.
ĐÃ THỬ NGHIỆM: `python3 -B -u alternates_ab.py` (`evidence/alternates-ab-fixed.log`): dựng `_kho_cau`, dời nguyên object store ra pool ngoài rồi cung cấp `GIT_ALTERNATE_OBJECT_DIRECTORIES`; **Git fsck=0, ancestry=0**, HEAD gate **rc=2/OID e72d857 không tra được commit**. Ghi CHÍNH pool ấy vào `.git/objects/info/alternates` (không thay một byte object/ref/receipt) => **rc=1/L-ANCESTRY, fsck=0**. Module lượt 3 dùng cùng fixture+biến env => **rc=1**. Linked worktree bình thường đã đo riêng vẫn rc=1, không khái quát lỗi này thành mọi worktree/CI.
ĐỘ TIN: cao

### chot-probe-git-chua-co-rang [P1] Các chốt của probe sức khỏe mới chưa được 93 ca khóa lại
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1141`, `ops/bien_nhan_v2.py:1166`, `ops/bien_nhan_v2.py:1168`, `ops/bien_nhan_v2_test.py:3372`, `ops/bien_nhan_v2_test.py:4143`.
VẤN ĐỀ: c96/m125 đã khóa được rc trong `_git_do`, nhưng `rev-parse --git-dir` mới gọi thẳng `_chay_git` và có một điều kiện rc RIÊNG. Bỏ điều kiện mới mà tất cả 93 ca vẫn xanh. Đã có witness lỗi probe bị biến thành vi phạm/sạch; vì vậy không phải mutant tương đương. M6 đòi răng cho từng chốt, nên việc 128/128 mutant chính thức đạt chưa bao phủ chốt này. Hai chốt khác cùng probe (làm mới stderr nền và cô lập env ngay từ lệnh đầu) cũng sống qua 93/93 và có witness sai hành vi; xem bảng đột biến và các log `baseline-refresh-witness.log`, `mutant-u2b.log`, `health-env-witness-fixed.log` bên dưới.
ĐÃ THỬ NGHIỆM: `python3 -B -u review_mutations.py u1-health-probe-rc ...`: trên bản sao chỉ thay đúng một mẫu `if p.returncode != 0` thành `if False`, giữ nguyên `_git_do` và m125 => **93/93, red=[]** (`evidence/mutants-a.log`). `python3 -B -u health_rc_witness.py`: Git wrapper chỉ cho probe đầu thoát **rc=3, stdout/stderr rỗng**, còn mọi lệnh khác chạy Git thật. HEAD **rc=2/2**; mutant **rc=1 không nợ, rc=0/TỔNG: ĐẠT có nợ** (`evidence/health-rc-witness.log`).
ĐỘ TIN: cao

### Hướng 11 — corpus với môi trường lành và đối chứng alternates
Lệnh: `python3 -B -u corpus_environment.py`; `python3 -B -u alternates_ab.py` (`evidence/corpus-environment.log`, `alternates-ab-fixed.log`).
Output: trên corpus 297 receipt nguyên byte, **GIT_TRACE=1**, cấu hình fsync deprecated GHI THẬT trong `.git/config`, và CHỈ thêm local `master/topic` đều giữ **rc=0/TỔNG: ĐẠT, nợ 1/60/0**. CHỈ thêm `remote.archive.promisor=false` => **rc=2/partial clone**. Kho alternates hợp lệ có **fsck=0**, pool qua env => HEAD **2**, cùng pool qua tệp => **1/L-ANCESTRY**, module lượt 3 qua env => **1/L-ANCESTRY**. Lần A/B đầu đặt module cũ ngoài cây hỗ trợ nên phát sinh lỗi nguồn provider riêng (KHÔNG dùng làm so sánh rc); đã sửa GIÀN GIÁO bằng bản sao đủ nguồn và đo lại sạch trong `alternates-ab-fixed.log`.

## BẢNG ĐÓNG FINDING LƯỢT 3

| slug | trạng thái | lệnh đã chạy trên exact candidate | output thật |
|---|---|---|---|
| stderr-rong-van-tin-lich-su-hong | **Tiền đề nhóm B theo chỉ thị; không lập lại**, không khai là đã vá | Không chạy lại hai phản chứng silent object-hash/parent-graph | KHÔNG ĐO LẠI theo quyết định chủ kho; không tính finding mới |
| replace-graft-lam-sai-quan-he-oid | **Đóng** | `python3 -B replay_extra_recheck.py extra replace-drop-parent graft-silent` | Replace: 1 không nợ / 0 có nợ (đúng vi phạm gốc); graft đã tắt warning: 2/2, không NỢ CHẾT; `replay-a.log` |
| git-dir-ke-thua-do-nham-kho | **Đóng đúng phản chứng cũ** | `python3 -B replay_extra_recheck.py extra foreign-git-dir` | GIT_DIR kho ngoài master=X vẫn giữ phép đo kho gốc: 1/0; `replay-a.log`. Việc xóa alternates hợp lệ là finding mới riêng |
| stderr-vo-hai-chan-nham-kho-lanh | **Đóng các phản chứng cũ** | `python3 -B corpus_environment.py`; `python3 -B new_probes.py matrix` | GIT_TRACE và local fsync warning trên corpus: 0/0, nợ 1/60/0; c95 `qua`. Cách trừ nền có lỗi mới khác chiều đã ghi riêng |
| for-each-ref-nhan-nham-ref-hau-to | **Đóng** | `python3 -B corpus_environment.py`; c95 trong `new_probes.py matrix` | Local master/topic trên corpus: 0; child origin/HEAD/topic trong c95: đúng một L-ANCESTRY/1; `corpus-environment.log`, `matrix.log` |
| chot-ma-thoat-git-chua-co-rang | **Đóng tại chốt cũ `_git_do`; M6 còn chốt probe mới chưa khóa** | `python3 -B rc_head_replay.py`; `python3 -B targeted_recheck.py`; `python3 -B review_mutations.py u1-health-probe-rc` | Cùng merge-base rc=128/stderr rỗng: HEAD 2/2; m125 giết c96 đúng rc=3; nhưng bỏ chốt probe mới: 93/93 + witness sai 1/0; `rc-head.log`, `target-mutants.log`, `mutants-a.log` |
| ca-partial-chi-bat-cau-hinh-cu | **Đóng** | `python3 -B replay_probe_recheck.py partial` | Clone local filter=blob:none thật, 4 blob vắng/1 promisor pack; không extensions.partialclone; `_kho_lanh` từ chối đúng remote promisor, CLI 2; `partial.log` |

## BẢNG ĐO

| yêu cầu / lời khai | command / evidence | output thật | kết luận |
|---|---|---|---|
| Exact SHA/tree/spec và cây sạch | `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`; `git status --short`; SHA256 spec; `evidence/preflight.log` | `3a52e6d…`; `97ba989c…`; status rỗng; spec `9a155cb9…3b1ca` | Đúng SHA/hash đóng băng; final readback bên dưới |
| Lời khai suite 93/93, 128/128, 2/2 | `python3 -B /tmp/wp960-r4-copy/ops/bien_nhan_v2_test.py`; `suite.log` | **93/93 · 128/128 · 2/2**, 110/128 đối chứng, rc=0 | Xác nhận số chính thức; chưa đủ M6 với guard probe mới |
| Ruff F delta 0 | `python3 gate_checks.py`; `checks.log`, `ruff-*.json` | Base/head đều 1 F541 tại test:1677, rc=1 mỗi bên, delta=0 | Đạt delta; không khai 0 lỗi tuyệt đối |
| Doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`; `doctrine.log` | 10 tệp, 0 chỗ, rc=0 | Đạt |
| Diff check | `git -C cay-kho diff --check 4488444 HEAD`; `checks.log` | rc=0, stdout/stderr rỗng | Đạt |
| Corpus thật nợ 1/60/0 | `python3 -B ops/bien_nhan_v2.py --root .`; `gate.log` | 297 receipt, 0 vi phạm/unknown, **1/60/0**, rc=0 | Đạt |
| Bỏ nợ phải ra 1, đúng số lỗi | `python3 -B corpus_review.py`; `corpus.log` | 61/61 khóa khớp nợ, nợ rỗng **rc=1/61 lỗi luật/0 khác/0 unknown**; 31 token không đổi resolver | Đạt |
| CI PR merge, đủ lịch sử, không origin/HEAD | `python3 -B ci_review.py`; `ci.log` | merge c959746f…, tree trùng head, 2 parent, shallow=false, origin/HEAD vắng; gate=0/nợ1/60/0 | Đạt mô phỏng local; CI online không đo |
| Cô lập GIT_* và replace | `replay_extra_recheck.py`, `new_probes.py config`; `replay-a.log`, `config.log` | Foreign GIT_DIR/replace đúng; HOME/includeIf/XDG/worktree thường đúng; **alternate env hợp lệ bị 2** | Đóng ca cũ, hồi quy alternates mới |
| Stderr nền | `stderr_extra.py stderr`; `stderr-extra.log` | Lỗi trùng nền + rc=1 => **sạch/0 hoặc NỢ CHẾT/1**; rc=128 và dòng khác => 2 | Không đạt M2 |
| Partial/promisor/grafts | `replay_probe_recheck.py partial`; `new_probes.py config`; `corpus_environment.py` | Partial thật/graft bị 2 đúng; **promisor=false làm corpus 0→2** | Có bắt nhầm cấu hình boolean tắt |
| Bỏ core.commitGraph=false | `git -C cay-kho diff 934a5b0 HEAD -- ops/bien_nhan_v2.py` (hunk trong `diff-tu-luot-3.patch`); suite/corpus | Không thêm cờ đó; suite/corpus đạt | Không đòi fsck hoặc tái lập finding nhóm B |
| Numstat/write set | `git diff --numstat 4488444 HEAD -- ops/bien_nhan_v2*.py`; `git diff --name-only 43b96f0 HEAD` | **+294/-193**, **+643/-104**, 1.234 dòng; delta sau merge chỉ 2 tệp | Chưa đo nội dung khai ADR-0044/numstat trên PR vì không gọi mạng |

## BẢNG SĂN

Mỗi hàng là một hướng độc lập; script dựng fixture hoặc đột biến trên bản sao `/tmp`, dùng fixture/ca có sẵn của exact candidate.

| hướng | LỆNH | OUTPUT THẬT / kết luận |
|---|---|---|
| 1. Chọn nhầm repo qua env | `python3 -B replay_extra_recheck.py extra foreign-git-dir` | Hai repo lành, repo ngoài master=X; gate vẫn 1/0 theo repo gốc (`replay-a.log`) |
| 2. Overlay đồ thị hợp lệ | `python3 -B replay_extra_recheck.py extra replace-drop-parent graft-silent` | Replace không làm đổi 1/0; graft tắt warning vẫn 2/2 (`replay-a.log`) |
| 3. Ref con khớp prefix | `python3 -B corpus_environment.py` + c95 qua `new_probes.py matrix` | Local master/topic corpus=0; origin/HEAD/topic đúng 1/L-ANCESTRY (`corpus-environment.log`, `matrix.log`) |
| 4. Partial thật và boolean promisor | `python3 -B replay_probe_recheck.py partial`; `python3 -B new_probes.py config` | Partial thật 4 blob thiếu=2; false/no/off ở kho đủ=2, fsck=0 => finding (`partial.log`, `config.log`) |
| 5. HOME/XDG/includeIf/worktree | `python3 -B new_probes.py config` | HOME/includeIf fsync, XDG fsync và linked worktree giữ 1 đúng; fsck=0 (`config.log`) |
| 6. Pool object qua env so tệp | `python3 -B alternates_ab.py` | Cùng object/ref/receipt: env=2; tệp alternates=1; fsck=0; lượt 3 env=1 (`alternates-ab-fixed.log`) |
| 7. Stderr lặp / một lần / trùng lỗi | `python3 -B new_probes.py stderr`; `python3 -B stderr_extra.py stderr` | First-only bị nuốt; lỗi trùng nền ra 0/NỢ CHẾT; khác dòng/rc128 bị 2 (`stderr*.log`) |
| 8. Mã lỗi độc lập stdout/stderr | `python3 -B rc_head_replay.py`; `python3 -B health_rc_witness.py` | Merge-base rc128: head2/2; probe rc3: head2/2, gỡ guard thành1/0 (`rc-head.log`, `health-rc-witness.log`) |
| 9. Corpus và bánh cóc | `python3 -B corpus_review.py` | 297 receipt/31 token không đổi; 61 khóa trùng nợ; nợ rỗng=1/61 luật/0 khác/0 unknown (`corpus.log`) |
| 10. CI merge đầy đủ | `python3 -B ci_review.py` | 2 parent/tree đúng/no originHEAD/nonshallow; gate0/nợ1/60/0 (`ci.log`) |
| 11. Răng từng mutant chính thức | `python3 -B targeted_recheck.py` | m103/m114/m125–131: 9/9 `giet_that`, 9/9 đối chứng qua (`target-mutants.log`) |
| 12. Gỡ thêm chốt mới | `python3 -B review_mutations.py ...` | u1 guard probe: 93/93, red=[] + witness sai1/0; bảng đầy đủ tiếp theo (`mutants-*.log`) |

## ĐỘT BIẾN REVIEWER TRÊN BẢN SAO

Lệnh đã chạy: `python3 -B -u review_mutations.py u1-health-probe-rc u2-health-probe-environment u3-query-environment` và lượt độc lập `python3 -B -u review_mutations.py u4-health-baseline-overwrite u5-prefix-boundary u6-newline-stderr`. Mỗi mutant có **đúng một mẫu thay, count=1**, một bản sao đầy đủ ngoài cây review, chạy toàn bộ **93 ca có sẵn** qua `_chay_1` (không chạy mutant lồng). Log đầy đủ: `evidence/mutants-a.log`, `evidence/mutants-b.log`.

| mutant | chốt/đường đi gỡ riêng; khác m125–m131 thế nào | kết quả | ca ĐỎ / răng thật |
|---|---|---|---|
| u1-health-probe-rc | Chỉ bỏ rc của `rev-parse --git-dir`; m125 chỉ bỏ rc ở `_git_do`, không đi qua probe này | **93/93**, red=[] | Không có; witness probe rc3: head2/2 → mutant1/0 |
| u2-health-probe-environment | Chỉ probe đầu bỏ dùng `_chay_git`, không sửa `_env_git` cho tất cả lệnh như m126 | **92/93** | c91 `giet_that` vì diagnostic Git vắng đổi từ thông điệp chuẩn sang FileNotFoundError; rc vẫn2. Chưa lĩnh tín dụng là đã đo riêng lỗi cô lập env; đo biến thể u2b giữ boundary bên dưới |
| u3-query-environment | Chỉ các lệnh đo `_git_do` bỏ dùng `_chay_git`, probe vẫn cô lập; khác m126 (mọi lệnh giữ nguyên bộ biến bắt buộc) | **92/93** | c95 `giet_that`: replace_ref ra **0** thay vì **1**. Răng đo đúng hành vi mất `GIT_NO_REPLACE_OBJECTS` ở truy vấn |
| u4-health-baseline-overwrite | Gỡ việc LÀM MỚI nền (dùng setdefault); m128 gỡ phép TRỪ nền, vẫn lưu nền mới | **93/93**, red=[] | Không có; `baseline_refresh_witness.py` cùng process/root, thêm fsync warning giữa hai lượt: head1→1, mutant1→2 |
| u5-prefix-boundary | Gỡ dấu `/` ranh giới khi bỏ qua ref con; m131 gỡ luôn `continue`, gây lỗi chiều ngược | **93/93**, red=[] | Không có. Chưa đo được ref thật nào Git trả ngoài bộ prefix mà mutant này đổi kết quả; không tự gọi nó là lỗi sản phẩm |
| u6-newline-stderr | Gỡ bỏ-qua dòng chỉ có khoảng trắng trong phép kiểm stderr; vẫn giữ phép trừ nền của m128 | **93/93**, red=[] | Không có. Không có witness Git thật tự phát ra stderr whitespace-only ở ca này; không suy survivor thành finding |

Lệnh witness bổ sung: `python3 -B -u baseline_refresh_witness.py` (`evidence/baseline-refresh-witness.log`). Hai lượt `_chay_cli` có sẵn dùng cùng root trong cùng process. Lượt đầu không warning; sau đó chỉ ghi cấu hình fsync deprecated. HEAD trả **1 rồi 1**, mutant u4 trả **1 rồi 2**, stderr chỉ cảnh báo fsync. Vì vậy việc overwrite `_NEN_STDERR` cũng là chốt có tác động thật mà 93 ca chưa khóa. Gộp thiếu răng của các chốt probe vào finding `chot-probe-git-chua-co-rang`, không nhân finding chỉ theo số mutant.

### Tách riêng cô lập env của probe mà giữ boundary
Lệnh: `python3 -B -u review_mutations.py u2b-health-probe-environment`; `python3 -B -u environment_health_witness.py` (`evidence/mutant-u2b.log`, `health-env-witness-fixed.log`).
Để không lĩnh tín dụng từ diagnostic FileNotFoundError của u2, u2b chỉ đổi `env` của `_chay_git` KHI args đúng `rev-parse --git-dir` sang `os.environ`; giữ toàn bộ xử lý ngoại lệ và môi trường cô lập của các lệnh khác. Kết quả **93/93, red=[]**. Trên kho lành, thêm duy nhất `GIT_DIR` trỏ đường không tồn tại: HEAD bỏ biến ấy đúng nên **rc=1**; mutant probe dùng biến kế thừa nên **rc=2/fatal: not a git repository**. Đây là survivor không tương đương nữa trong cùng phần probe mới, gộp M6 ở finding `chot-probe-git-chua-co-rang`.

Tổng cộng đã chạy **7 biến thể reviewer khác m125–m131**, mỗi biến thể qua đủ 93 ca: **2 bị giết đúng TinHieuChotCa, 5 sống**. Trong 5 survivor, u1/u4/u2b có witness độc lập sai hành vi; u5/u6 chưa có witness Git thật nên không tự biến thành finding. Không tính lỗi giàn giáo hoặc ngoại lệ vô can làm răng.

## READBACK CUỐI VÀ GIỚI HẠN

Lệnh: `python3 -B final_readback.py` (`evidence/final-readback.log`). HEAD vẫn **3a52e6d194d08a755793cf449f393fb15b56757b**, tree **97ba989c22cbde6bd24cdd33671d9e7f2442ae58**; status rỗng; diff-check rc=0/stdout/stderr rỗng. Ba tệp product/test/spec vẫn byte-identical với Git blob của reviewed SHA; SHA256 lần lượt **17b82cdb704fc935b92a196a7abd4e90401c71d9bbdb8534d7a4d3a4b81fa207**, **933b0e801dc016648ee89f77310d58d306da94982eb636be8edebeade4708cca**, **9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca**. Các đột biến chỉ trên bản sao `/tmp`; không sửa `cay-kho/`, không push, không gọi mạng, không tạo `HINT.patch`.

Đã đo bằng Git 2.43.0, Python 3.13.17, Ruff 0.17.3. Không tự đặt execution surface/model/transport chưa đo được từ launcher, lease hoặc tên tài khoản. CI GitHub thật, trạng thái PR #995/thread và disclosure numstat/ADR-0044 trên PR: **KHÔNG ĐO ĐƯỢC** vì nhiệm vụ cấm mạng. Chưa đo Windows/Git khác và hiệu năng ổn định; không tuyên bố phủ mọi cấu hình Git. Hai phép fault injection stderr/rc đã ghi rõ dùng wrapper; không khai chúng là sự cố Git thật tự nhiên. Hai lỗi giàn giáo reviewer (script rc cũ vấp thư mục scratch và module A/B cũ nằm sai gốc nguồn) đã ghi và đo lại; không tính chúng thành finding sản phẩm.

Đóng các phản chứng nhóm A của lượt 3 tại vị trí cũ, nhưng phát hiện **4 P1** thuộc hình dạng **loi-do**. Trong nhóm này, M6 vẫn thiếu răng ở các chốt probe mới. `bo-chon-ung-vien` của ref prefix đã đóng; `nguon-goc-cau` chưa thấy tái xuất — c86 và m94 đạt thật trong suite. Nhóm B được giữ là tiền đề theo quyết định chủ kho, không có finding lặp lại. Review Class sensitive và M-1 đòi không P0/P1/P2 nên kết luận **changes_requested**. Q8/lease M-4 dành quyết định bước thi công tiếp theo cho chủ kho; báo cáo không cấp quyền sửa, merge hoặc land.
