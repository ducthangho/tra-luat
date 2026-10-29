verdict: changes_requested
reviewed_sha: ae0d06c23fb777545fd7547a07d9f368e4122f49
Kết quả: 0 P0, 5 P1, 0 P2, 0 P3.

## BẢNG ĐO

| khẳng định / yêu cầu | phép đo và output | kết luận |
|---|---|---|
| Đúng SHA/spec/lease | Hướng 1: HEAD ae0d06c…; tree 7312e5d6…; spec SHA256 9a155cb9…3b1ca; status sạch; packet 2 tệp/857 dòng | Khớp; phần ngoài packet do merge master, đã đối chiếu Git |
| Executor 1: _commit_cua có đủ ba trạng thái | Hướng 3/6/12: git mất/rc2/127/128 → CLI 2; hai commit trùng → _MoHo; object rỗng peel rc1 → None → CLI 0 hoặc NỢ CHẾT/1 | Chưa đủ; finding peel-rc1-an-loi-object |
| Executor 2: show-ref rc1 là vắng | Hướng 4: vắng thật fallback đúng; tree/blob có thật → 2; loose ref hỏng và symref gãy cũng show-ref 1 → fallback/CLI 1 | Sai; finding ref-hong-bi-doc-thanh-vang |
| Executor 3: run.json có nhưng hỏng → chưa đo | Hướng 4/9: directory, symlink gãy/vòng, lỗi quyền đều 2 ở có/không nợ; vắng thật/ENOTDIR theo quy tắc đã khai | Đạt hành vi nguyên trạng; chốt symlink/OSError thiếu răng M6 |
| Executor 4: sinh nợ cùng biên | Hướng 3/5: hai cờ × directory/UTF8/YAMLError đều 2; --sinh-no với timestamp sai hoặc lồng sâu → traceback/1 | Đóng một phần, còn finding sinh-no-van-thoat-loi-yaml |
| Executor 5: c91/c92/c87/c88/c72 | Hướng 5/10: c91 14/14 CLI 2; c92 6 hỏng/2 lành đúng; c87/c88 đủ bốn biên cũ; docstring c72 khai giới hạn | Khớp phép đo được khai; chưa đại diện mọi lỗi YAML/Git |
| Executor 6: m103–m113/m76/m84 | Hướng 10: 14 selected mutation đều giet_that vì đúng target assertion, đối chứng sạch | Khớp; mutant riêng của reviewer vẫn tìm chốt khác thiếu răng |
| Executor 7 / B7: N/N | Hướng 7: 89/89 ca, 110/110 mutant thường, 2/2 tự kiểm, rc0 | Khớp tỷ lệ, không đồng nghĩa mọi chốt mới có răng |
| Gate / ruff / doctrine / diff-check | Hướng 2/7: gate 0 với 1/60/0; F541 base=head=1, delta0; doctrine 0; diff-check 0 | Đạt các phép đo cục bộ |
| M5/B5: 61 mục nợ còn thật | Hướng 5: 61/61 khóa có chứng cứ riêng; head và base-data cùng gate HEAD có nợ rc0; bỏ nợ rc1 đúng 61 dòng | Đạt; không sửa hằng nợ hoặc receipts |
| M3 và hồi quy corpus | Hướng 8: 99 lượt / 31 token, resolver cũ so HEAD không khác kết quả; +97 git calls; median 25,3182→25,3249 giây | Chưa thấy hồi quy corpus; thời gian đo có tải đồng thời |
| CI pull_request không origin/HEAD | Hướng 7: merge 2 parent, đúng HEAD tree, shallow=false, remote master 2618eb4, gate 0 | Đạt mô phỏng local; CI online không đo vì cấm mạng |
| Biên KhongDoDuoc và receipt khác | Hướng 8: git hỏng dừng cả lượt/2, che diagnostic L-REVIEW của receipt khác; không traceback/NỢ CHẾT | Ghi giới hạn; chưa có căn cứ gán riêng thành sai M2 |
| M6: mutant riêng ≥5 ngoài m103–m113 | Hướng 11: 7 mutant chạy cả 89 ca; 5 chốt khác vị trí m103–m113 đều sống sót, 2 mutant nhỏ của except bị c92 giết | Không đạt M6; bảng cuối đủ 7 mutant và phản chứng không tương đương |
| B1/B6/B8 | Suite c86/m94 đạt; m78 giết literal đúng; baseline logging ở Hướng 12 | Nền đã đối chiếu; không dùng assertion đã tắt làm pass |

## BẢNG ĐÓNG FINDING LƯỢT 1

| slug lượt 1 | trạng thái | lệnh chạy lại trên HEAD | output thật |
|---|---|---|---|
| git-hong-thanh-token-thuong | ĐÓNG phản chứng cũ; còn đường object rỗng ở finding mới | `python3 -u probe_review.py boundaries` và `rawcli` | Cùng OID thuần chữ `dbffbbc…`, git lành rc=1; PATH không git rc=2, không traceback; c91/m103 giết vì fixture git_vang, không phải lỗi khác. |
| b2-chua-do-du-ma-tran | ĐÓNG | `python3 -u probe_r2.py matrix`; `python3 -u probe_review.py errors` | c91 14/14 lời gọi main rc=2, đủ receipt-thư-mục / alias vòng / ref tree thật × có/không nợ; stderr nêu nguồn, không NỢ CHẾT/Traceback. JSON hỏng vẫn có c77 và phản chứng CLI reviewer. |
| run-json-thu-muc-thanh-khong-ap | ĐÓNG | `python3 -u probe_review.py errors`; `python3 -u probe_r2.py symlinks` | run-directory cả hai trạng thái nợ rc=2, không NỢ CHẾT; m106 chết đúng run_json_thu_muc. |
| nhanh-mac-dinh-tree-bi-bo-qua | ĐÓNG phản chứng tree; còn ref hỏng theo finding mới | `python3 -u probe_review.py auxiliary`; `python3 -u probe_r2.py refs` | Ref tree thật không fallback, KhongDoDuoc và CLI rc=2; ref vắng thật vẫn fallback; m104 chết đúng nhanh_la_tree. |
| sinh-no-ngoai-bien-doc-receipt | ĐÓNG MỘT PHẦN | `python3 -u probe_review.py auxiliary`; `python3 -u probe_r2.py matrix` và `yaml_errors` | Phản chứng cũ IsADirectoryError đã rc=2 ở cả hai cờ; c92 cũng khóa byte UTF8/YAMLError. Timestamp sai và YAML lồng sâu vẫn `--sinh-no` traceback/rc=1, finding sinh-no-van-thoat-loi-yaml. |
| bien-utf8-receipt-chua-co-rang | ĐÓNG | `python3 -u probe_mutations.py r8-receipt-encoding`; mutation m107 ở `measure_target_mutants.py` | Bỏ riêng UnicodeDecodeError làm c91 đỏ đúng nguồn receipt UTF8; nguyên trạng subprocess rc=2; mutant subprocess rc=1/Traceback. |
| b6-docstring-chua-khai-gioi-han | ĐÓNG | `python3 -u probe_r2.py matrix`; selected m78 trong `measure_target_mutants.py` | Docstring nói rõ >- chỉ hồi quy/không có chốt riêng. m78 giết đúng khoi_lit, danh sách bị nhận vẫn có khoi_gap. |
| bo-chon-moi-chua-khoa-bien | ĐÓNG | `python3 -u probe_mutations.py r2-commit-boundary r4-backtick-close r5-provider-boundary r6-window-next`; selected m110–m113 | Từng guard cũ đều bị c87/c88 giết đúng assertion Precommit / backtick-chi-mo / notprovider / provider-dong-sau. Không dùng thất bại giàn giáo làm răng. |

Log: `evidence/old-{boundaries,errors,auxiliary,rawcli,mutants}.log`, `evidence/matrix.log`, `evidence/target-mutants-final.log`. 7 finding đóng phản chứng cũ, 1 đóng một phần; đóng phản chứng cụ thể không đồng nghĩa lớp lỗi đã đóng.

## BẢNG SĂN

Đã hoàn tất 12 hướng dưới đây; từng hướng có lệnh và output thật, cùng log/script tái lập trong thư mục giao việc này.

### Hướng 1 — xác minh định danh và phạm vi

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}; git -C cay-kho status --short; git -C cay-kho rev-parse --is-shallow-repository; sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`.
Output: HEAD `ae0d06c23fb777545fd7547a07d9f368e4122f49`; tree `7312e5d65f57740d8673b5491357532c2b09c9a9`; status rỗng; shallow `false`; spec SHA256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca`.
Diff packet so lease: `208/190 ops/bien_nhan_v2.py`, `354/105 ops/bien_nhan_v2_test.py`, tổng 857 dòng. Các tệp ngoài packet đến từ merge master; sẽ kiểm riêng bằng lịch sử Git. Bản sao đo `/tmp/wp960-r2-l2-copy` được checkout exact SHA; bản dữ liệu base `/tmp/wp960-r2-l2-base` ở `4488444…`. Không gọi mạng. Dùng lại ba script reviewer cũ từ lượt 1 nhưng đổi mọi neo SHA/đường dẫn sang lượt này; mọi output phải chạy lại.

### Hướng 2 — gate và các kiểm tra không phá gì

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .` tại cay-kho (`evidence/gate.log`). Output: `244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297`; nợ `L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0`, surface không áp `0`; `TỔNG: ĐẠT`, rc=0.
Lệnh: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0 (`evidence/doctrine.log`). `git diff --check 4488444 HEAD` ⇒ output rỗng, rc=0. `ruff check --select F --output-format json` trên hai tệp ở base và head ⇒ cùng một F541 có sẵn ở test dòng 1677; delta=0 (`evidence/ruff-{base,head}.json`). Suite đầy đủ đã hoàn tất; kết quả ở Hướng 7.

### Hướng 3 — lỗi phân tích YAML trên hai cờ sinh nợ

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_r2.py yaml_errors` (`evidence/yaml-extra.log`); giữ builder `_kho_cau`/`_ghi_bn_cau`, thêm receipt có `date: 2026-99-99`, chạy subprocess CLI thật.
Output: gate thường rc=2, không traceback, stderr nêu `hong.receipt.yaml: YAML hỏng (ValueError: month must be in 1..12)`; `--sinh-no-cau-lich-su` cũng rc=2; **`--sinh-no` rc=1 và Traceback/ValueError**. Receipt lồng 1.200 tầng gây `RecursionError` có cùng kết quả 2/1/2. Đối chứng YAML lành: hai cờ sinh nợ đều rc=0. Finding đã đo được; chưa coi bản vá `_sinh_no` là đóng toàn lớp lỗi YAML.

### sinh-no-van-thoat-loi-yaml [P1] `--sinh-no` còn traceback khi SafeLoader ném ValueError hoặc RecursionError
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1519`–`1524`.
VẤN ĐỀ: `_sinh_no` chỉ bắt OSError/UnicodeDecodeError/YAMLError. `yaml.safe_load` thực tế còn ném ValueError cho scalar timestamp có tháng không hợp lệ và RecursionError cho cấu trúc lồng sâu. Hai lỗi phân tích này thoát cả `main` (chỉ bắt KhongDoDuoc), thành traceback/rc=1, trái M2. Chuyển vị trí gọi vào try chưa đóng được lớp lỗi.
ĐÃ THỬ NGHIỆM: `python3 -u probe_r2.py yaml_errors` ⇒ trên cùng fixture `date: 2026-99-99`, subprocess gate thường và sinh nợ câu đều rc=2; `--sinh-no` rc=1, Traceback/ValueError. Log `evidence/yaml-extra.log` có cả phản chứng lồng sâu và đối chứng lành.
ĐỘ TIN: cao

### Hướng 4 — symlink và phân loại ref mặc định

Lệnh: `python3 -u probe_r2.py symlinks` và `python3 -u probe_r2.py refs` (`evidence/symlinks.log`, `evidence/refs.log`). Output run.json: symlink gãy, tự vòng, vòng ở thư mục cha và thư mục thật đều rc=2 ở cả có/không nợ, không traceback/NỢ CHẾT. Vắng thật và cha là file ⇒ rc=0 không nợ, rc=1 NỢ CHẾT khi có nợ (phù hợp lời khai `_vang` coi ENOTDIR là vắng).
Output ref: origin/HEAD vắng thật ⇒ fallback hợp lệ, fixture câu cũ rc=1. `origin/master` trỏ tree/blob hoặc OID thiếu ⇒ rc=2. **Ref tồn tại nhưng nội dung hỏng** (`this-is-not-an-oid`) và **symref origin/HEAD gãy** đều `show-ref --verify --quiet` rc=1, bị fallback sang ref khác ⇒ rc=1 và kết luận L-ANCESTRY, không có trạng thái chưa đo.

### ref-hong-bi-doc-thanh-vang [P1] `show-ref` rc=1 không chứng minh ref vắng
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1152`–`1156`.
VẤN ĐỀ: Bản vá phân rc=1 của `show-ref --verify --quiet` thành “ref vắng”, nhưng Git cũng trả 1 cho loose ref có nội dung hỏng và symref trỏ ref không tồn tại. `_nhanh_mac_dinh` vì vậy bỏ nguồn mặc định đang hỏng để đo bằng ref kế, biến lỗi git/ref thành kết luận vi phạm. Đây là đường còn lại của lớp lỗi M2; ca c91 chỉ dùng ref trỏ tree có show-ref rc=0 nên chưa khóa đường này.
ĐÃ THỬ NGHIỆM: `python3 -u probe_r2.py refs`: thay đúng nội dung `.git/refs/remotes/origin/master` thành `this-is-not-an-oid\n` trên fixture đã có remote master; Git show-ref rc=1, CLI rc=1/L-ANCESTRY. Đối chứng ref vắng thật fallback hợp lệ và tree/blob/OID thiếu rc=2. Symref gãy tái lập cùng lớp. Log `evidence/refs.log`.
ĐỘ TIN: cao

### Hướng 5 — đo lại ma trận mới và kiểm toán nợ độc lập

Lệnh: `python3 -u probe_r2.py matrix` ⇒ c91 `qua`, đúng 14 lời gọi main: 7 nguồn × 2 trạng thái nợ, tất cả rc=2 và stderr đúng nguồn; c92 `qua`, 6 lượt hỏng rc=2 + 2 lượt lành rc=0. Docstring c72 đã khai rõ folded chỉ là hồi quy (`evidence/matrix.log`). Ca JSON hỏng c77 vẫn có 8 tổ hợp API riêng; phản chứng CLI của reviewer ở `evidence/old-errors.log` xác nhận rc=2.
Lệnh: `python3 -u audit_corpus.py` (`evidence/corpus.log`, `evidence/corpus.json`): 297 receipts; **61/61** khóa nợ có bằng chứng Git/luot độc lập, gồm 60 ancestry + 1 review. 99 token ancestry, 97 resolve; hai token ngày `20260917`, `20260822` không ngữ cảnh được bỏ qua. Cổng HEAD chạy trên corpus HEAD và dữ liệu base lease đều rc=0 khi giữ nợ; xóa nợ đều rc=1, đúng 61 dòng ba luật, unknown=0. Chưa phát hiện nợ chết hoặc mục không có nguồn thật.

### Hướng 6 — object Git hỏng, tiền tố trùng giữa các loại object, shallow/partial

Lệnh: `python3 -u probe_objects.py objects` và `python3 -u probe_objects.py collisions`; builder kho thật hiện hữu, chỉ thay object/ref trong fixture, không đổi nguồn đang review. Log hợp lệ: `evidence/objects-valid.log`, `evidence/collisions.log`. Lượt `objects.log` đầu KHÔNG dùng: giàn giáo chưa unlink object chỉ đọc trước khi ghi, bị PermissionError; đã sửa cách đột biến và chạy lại.
Output: 2 commit cùng `5298700` ⇒ `_MoHo` trên cả kho đầy đủ và fixture có shallow boundary; commit+blob `8ac070d` và commit+tag-trỏ-blob `2f52361` resolve đúng 1 commit, CLI rc=1; commit+tag-trỏ-commit-khác `b4214fb` ⇒ `_MoHo`, CLI rc=2. Kết quả tương ứng với Git peel thật.
**Object commit thật thuần chữ `dbffbbc…` bị thay bằng file rỗng**: `--disambiguate=dbffbbc` rc=0 vẫn liệt kê đúng OID; peel rc=1 và stderr `object file … is empty`; `_commit_cua` trả None; CLI rc=0/TỔNG: ĐẠT. Object lỗi zlib trả 128 và được đổi đúng rc=2. Mô phỏng cấu hình promisor với object vắng không liệt kê ứng viên; token thuần không ngữ cảnh bị bỏ qua theo M3. Không gọi remote mạng; URL promisor là đường local không tồn tại. Shallow boundary có thể làm Git ancestry rc=1 vì thiếu lịch sử; đây là giới hạn fixture nông, không khẳng định corpus đầy đủ được giao có vấn đề này.

### peel-rc1-an-loi-object [P1] Commit object rỗng bị đọc thành token thường và gate trả sạch
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1120`–`1124`, `1141`.
VẤN ĐỀ: `_peel_commit` coi mọi rc=1 là bằng chứng “không có commit”, dù Git trả 1 cả khi commit object đang có nhưng rỗng. Sau khi `--disambiguate` đã liệt kê ứng viên, lỗi đọc object bị bỏ qua trong tập `ung`. Với token thuần chữ không ngữ cảnh, M3 vì vậy bỏ token và trả sạch, trái M2. `_git` cũng vứt stderr chứa bằng chứng lỗi.
ĐÃ THỬ NGHIỆM: `python3 -u probe_objects.py objects`: fixture OID `dbffbbc94a7488c35d0a4050c1d26ffad20fa8ad` đã vào master, câu `Ban dbffbbc chua vao master.`; nguyên trạng CLI rc=1. Chỉ thay object commit thành file rỗng ⇒ disambiguate vẫn rc=0/liệt kê OID, peel rc=1/`object … is empty`, CLI rc=0, không KHÔNG ĐO ĐƯỢC. Đối chứng zlib hỏng rc=2. Log `evidence/objects-valid.log`; lượt có nợ bổ sung ở `evidence/objects-final.log`.
ĐỘ TIN: cao

### Hướng 7 — suite đầy đủ và mô phỏng CI pull_request

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u ops/bien_nhan_v2_test.py` tại cây HEAD chỉ đọc (`evidence/suite.log`) ⇒ **89/89 ca · 110/110 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM · 92/110 khai đối chứng**, `TỔNG: ĐẠT`, rc=0. Các mutant cũ m76/m84 và mới m103–m113 đều có target `giet_that`; chi tiết assertion được đối chiếu ở Hướng 10.
Mô phỏng trên clone: `git commit-tree <HEAD-tree> -p 2618eb4… -p ae0d06c…`, checkout merge `31a06857cf9adc3406c32c18da7357e18e3ec5da`, xóa origin/HEAD bằng `git update-ref --no-deref -d refs/remotes/origin/HEAD`, đặt origin/master=`2618eb4…`, rồi chạy gate. Output: merge 2 parent, tree **trùng exact HEAD** `7312e5d6…`, shallow=false, origin/HEAD không có, gate rc=0 và nợ 1/60/0 (`evidence/ci-{identity,gate}.log`). Đây là mô phỏng local, không phải kết quả GitHub Actions online.
Kiểm lịch sử: `git diff --name-only 2618eb4 HEAD` chỉ đúng hai tệp packet; `git diff --stat f7659a2 0a37008 -- <hai tệp>` rỗng. Xác nhận merge master không sửa packet.

### Hướng 8 — so resolver trên corpus và biên lỗi theo từng receipt

Lệnh: `python3 -u probe_objects.py compare` (`evidence/compare.log`) ⇒ trên 99 lần xuất hiện / 31 token phân biệt, resolver cũ (`rev-parse --verify --quiet tok^{commit}`) và resolver HEAD **không đổi kết quả nào**. Đo đếm git/gate: resolver cũ 1.418 lời gọi, HEAD 1.515 (+97, đúng số lần token resolve được); benchmark xen kẽ 3 lượt mỗi bên đã hoàn tất (Hướng 9), chỉ ghi thời gian quan sát, không đặt ngưỡng hiệu năng ngoài spec.
Lệnh: `python3 -u probe_r2.py multi` (`evidence/multi.log`): ba receipt, một câu ancestry không vi phạm và một câu L-REVIEW vi phạm thật. Khi git lành ⇒ CLI rc=1, in L-REVIEW của b-old. Chỉ làm hỏng zlib object dùng bởi a-hong ⇒ CLI rc=2, stderr nêu lỗi git, stdout rỗng, không in kết quả b-old. Xác nhận `KhongDoDuoc` thoát cả lượt chứ không được gom per-receipt. M2 chỉ đòi rc=2/không traceback/không kết luận nợ chết cho nguồn hỏng; phép đo này đạt ba điều ấy, nên **không gán riêng việc mất diagnostics của receipt khác thành finding sai đặc tả**. Giới hạn báo cáo vẫn được ghi rõ.

### Hướng 9 — quyền đọc và kết quả đo thời gian

Lệnh: `python3 -u probe_r2.py permissions` (`evidence/permissions.log`), chmod 000 lần lượt receipt, run.json, verdict và cha run.json, mỗi thứ × có/không nợ. Output: 8/8 lượt rc=2, không traceback/NỢ CHẾT; thao tác đọc trực tiếp xác nhận PermissionError thực sự ở cả bốn nguồn. Không suy từ uid rằng quyền đọc luôn thành công.
Benchmark hoàn tất (`evidence/compare.log`): resolver cũ median **25,3182 s**, HEAD **25,3249 s** (3 lượt xen kẽ mỗi bên); 1.418→1.515 lời gọi git. Không thấy chênh thời gian đáng kể trong phép đo này; có các tiến trình test khác chạy cùng lúc, nên không diễn giải thành bảo đảm hiệu năng tổng quát. Không thấy OID corpus nào đổi kết quả.

### Hướng 10 — răng riêng của từng vá cũ, không chỉ tỷ lệ tổng

Lệnh: `python3 -u measure_target_mutants.py` (`evidence/target-mutants-final.log`): chọn nguyên 14 đột biến hiện hữu m76/m78/m84/m103–m113, giữ giàn giáo/đối chứng, ghi đầy đủ assertion của target. Output: **14 hàng, 14 target failure `giet_that`, tất cả có răng**. m103 chết vì `git_vang/khong-no` rc=0; m104 vì `nhanh_la_tree` rc=1; m105 vì `tien_to_mo_ho` rc=0; m106 vì `run_json_thu_muc` rc=0; m107 vì UnicodeDecodeError từ receipt; m108 vì KhongDoDuoc thoát main; m109 vì IsADirectoryError. m110–m113 lần lượt chết vì Precommit/backtick chỉ mở/notprovider/provider dòng sau, đúng điều từng finding nói. m76/m84 neo lại vẫn giết c71/c78; m78 chỉ giết literal `|`, folded vẫn được nhận.
Lượt `target-mutants.log` đầu lỗi bộ chọn ID `m2b` của giàn giáo; không dùng. `target-mutants-valid.log` là nháp dùng namespace sao chép; đã chạy lại với namespace gốc của test để khôi phục globals đúng, chỉ dùng bản `final` ở trên.
Bổ sung object rỗng có nợ (`evidence/objects-final.log`): CLI rc=1 và **NỢ CHẾT**; không nợ rc=0. Đây là hai trạng thái sai của cùng finding peel-rc1-an-loi-object, không đếm thêm finding.

### Hướng 11 — đột biến độc lập ngoài m103–m113 (kết quả từng bản sao)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u new_mutations.py n1-vang-stat n2-vang-oserror n3-peel-rc n4-ref-show-error n5-sinh-no-utf8 n6-sinh-no-yaml n7-peel-noncommit` (`evidence/new-mutants.log`). Mỗi mutant là clone checkout exact HEAD, thay đúng một mẫu (đòi count=1), rồi chạy lần lượt **cả 89 ca có sẵn**, không dùng exception vô can làm răng.
Hai kết quả đầu: n1 đổi `lstat()` thành `stat()` ⇒ **89/89, red=[]**; n2 đổi nhánh `except OSError` của `_vang` thành `return True` ⇒ **89/89, red=[]**.
Lệnh phản chứng không tương đương: `python3 -u mutant_witnesses.py` (`evidence/witness-index.log`, `evidence/witness-n*.log`). n1 trên symlink run.json gãy: nguyên trạng rc=2, mutant rc=0 không nợ / rc=1 NỢ CHẾT có nợ. n2 trên vòng symlink ở thư mục cha: cùng cặp kết quả. Chốt đang hoạt động đúng nhưng suite không khóa được từng nhánh lỗi nguồn mới.

### chot-loi-do-moi-chua-co-rang [P1] Bốn chốt lỗi đo vẫn có thể bị gỡ mà 89 ca xanh
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1123`, `1155`, `1168`–`1173`; ca c91 tại `ops/bien_nhan_v2_test.py:3081`, đột biến mới tại `3836` trở đi.
VẤN ĐỀ: M6 đòi đột biến cho từng chốt. c91/m106 chỉ khóa run.json là thư mục; chưa có ca khóa symlink gãy hoặc lỗi lstat khác ENOENT/ENOTDIR. Đổi riêng `lstat`→`stat`, hoặc biến lỗi OSError thành “vắng”, đều làm sai M2 (đo lỗi thành sạch/NỢ CHẾT) mà 89/89 ca vẫn đạt. Đây là thiếu răng đo được, không tuyên bố hành vi nguyên trạng trên symlink đang sai.
ĐÃ THỬ NGHIỆM: `python3 -u new_mutations.py n1-vang-stat n2-vang-oserror …` ⇒ cả hai `passed=89,cases=89,red=[]`. `python3 -u mutant_witnesses.py` ⇒ hai cặp phản chứng nguyên trạng rc=2 nhưng mutant rc=0 hoặc rc=1/NỢ CHẾT, cùng fixture/nguồn. Log `evidence/new-mutants.log`, `evidence/witness-n1-vang-stat.log`, `evidence/witness-n2-vang-oserror.log`.
ĐỘ TIN: cao

### Hướng 12 — mã lỗi git khác 127 và ranh giới B8

Lệnh: `python3 -u probe_r2.py gitfail` (`evidence/git-fail.log`): fixture đã dựng xong, PATH chỉ đổi sang executable git trả lần lượt 1/2/127/128, và một lượt stdout byte UTF8 lỗi. Output: **5/5 CLI rc=2**, không Traceback/NỢ CHẾT; rc=2 của git được nêu đúng ở stderr; byte lỗi được gom thành `[*] ... UnicodeDecodeError`. Không phát hiện đường thoát mới ở dispatch disambiguate này.
Lệnh nền: `python3 -u probe_review.py baseline` (`evidence/baseline.log`), chỉ đổi module gate của các fixture hiện hữu sang blob ở lease base 4488444; tắt assertion HEAD để thu đủ output nên nhãn `qua` của logger **KHÔNG được coi là test pass**. Đây là phép so nền trên dữ liệu fixture, không tuyên bố đã quay lại thời điểm executor bắt tay. Output được tổng hợp bên dưới khi đọc xong log.

Bổ sung Hướng 12 / B8: output nền trên lease base thật là B1 `[0,0]`; B3 c87 `[0,0,0,0,0,0,0]`; B4 c88 `[1,1,1,1,1]` và hai thứ tự khai báo cùng dòng `[1,1]`; A2 c71 `[1,0,2]`; OID thật toàn số/toàn chữ `[1,1]`. Khớp nền đã ghi; không dùng logger tắt assertion làm ca pass. Vế âm M1 trên HEAD: `rg -n '"dung_tai"|def _moc_|def _commit_them_cau|def _co_cau' cay-kho/ops/bien_nhan_v2.py` ⇒ 0 dòng (rg rc=1 vì không match), vế dương c86/m94 đạt trong suite đầy đủ.

Bổ sung Hướng 11: n3 (`_peel_commit`: bỏ kiểm rc và định dạng đầu ra) vừa kết thúc **89/89, red=[]**. Phản chứng object zlib hỏng từ `evidence/witness-n3-peel-rc.log`: nguyên trạng rc=2, mutant rc=0. Đây là chốt lỗi git thứ ba chưa có ca khóa, gộp vào finding chot-loi-do-moi-chua-co-rang.

Bổ sung Hướng 11: n4 (`_nhanh_mac_dinh`: bỏ biên show-ref rc ngoài 0/1) kết thúc **89/89, red=[]**. Cùng fixture remote master chứa OID vắng, show-ref rc=128: nguyên trạng CLI rc=2, mutant fallback và rc=1. Gộp vào finding chot-loi-do-moi-chua-co-rang cùng ba chốt trước; vị trí n4 tại `ops/bien_nhan_v2.py:1155`.

Bổ sung đóng finding lượt 1 từ cả bộ ca: r2/r4/r5/r6 đều **88/89**, đỏ đúng c87/c87/c88/c88; r8 UTF8 receipt **87/89**, đỏ đúng **c91 và c92** (cờ sinh nợ câu lịch sử cũng đọc receipt). Tất cả là `giet_that`, không lỗi giàn giáo (`evidence/old-mutants.log`, runner rc=0).

Bổ sung Hướng 5 / M4: `evidence/corpus.json` có 20 verdict với run.json; 9 verdict/10 dòng qua điều kiện cửa sổ provider/không citation. Trong đó 7 lời khai có giá trị surface chính tắc được so sánh, 6 verdict lệch surface và cả 6 đều có caveat. Các dòng còn lại là mô tả tự do không mang giá trị surface chính tắc; không dùng số dòng regex ứng viên thay cho số lời khai đã đối chiếu.

Bổ sung Hướng 6 — partial clone thật, hoàn toàn local: `python3 -u probe_objects.py partial` (`evidence/partial-real.log`) dựng từ `_kho_cau`, publish hai commit trùng tiền tố, bật `uploadpack.allowFilter`, rồi `git clone --no-checkout --filter=blob:none --no-local file:///tmp/.../source ...`. Không transport mạng. Output: clone rc=0; `remote.origin.promisor=true`, filter `blob:none`, 1 pack `.promisor`, `rev-list --missing=print` còn blob thiếu. Trong kho partial thật ấy, `5298700` vẫn `_MoHo` (2 commit), tiền tố M `e72d857` vẫn resolve đúng. Không thấy hồi quy disambiguate ở hai đối chứng này; không tuyên bố đã kiểm mọi server/filter partial clone.

Bổ sung Hướng 11: n5 bỏ riêng UnicodeDecodeError ở `_sinh_no` và n6 bỏ riêng yaml.YAMLError đều kết thúc **88/89**. Cả hai bị đúng c92 giết (`giet_that`): n5 UnicodeDecodeError thoát `--sinh-no`, n6 ParserError thoát cùng cờ; đối chứng khác không đỏ. Mutant n7 đã hoàn tất, kết quả ở bảng cuối bên dưới. Hai kết quả này xác nhận ca mới khóa đúng hai lớp ngoại lệ đã khai, không thay thế bằng chứng lỗi timestamp/RecursionError chưa được bắt ở nguyên trạng.


Bổ sung hoàn tất Hướng 11 — bảng cuối (tất cả đã chạy hết 89 ca, không chỉ target):

| mutant reviewer | chốt thay đổi trên bản sao | kết quả | ca đỏ đúng |
|---|---|---|---|
| n1-vang-stat | _vang: lstat → stat | 89/89 | **KHÔNG CÓ** |
| n2-vang-oserror | _vang: OSError → return True | 89/89 | **KHÔNG CÓ** |
| n3-peel-rc | _peel_commit: bỏ kiểm rc / OID đầu ra | 89/89 | **KHÔNG CÓ** |
| n4-ref-show-error | _nhanh_mac_dinh: lỗi show-ref → continue | 89/89 | **KHÔNG CÓ** |
| n5-sinh-no-utf8 | _sinh_no: bỏ riêng UnicodeDecodeError | 88/89 | c92/giet_that |
| n6-sinh-no-yaml | _sinh_no: bỏ riêng yaml.YAMLError | 88/89 | c92/giet_that |
| n7-peel-noncommit | _commit_cua: bỏ lọc None sau peel | 89/89 | **KHÔNG CÓ** |

Năm mutant n1/n2/n3/n4/n7 ở năm chốt khác vị trí với m103–m113. n5/n6 là hai phép gỡ nhỏ hơn tại nhóm except mà m109 gỡ cả nhóm; ghi riêng kết quả, không dùng chúng thay cho năm chốt độc lập. Hai mutant n5/n6 giết đúng c92 vì UnicodeDecodeError/ParserError thoát CLI; không tính exception từ giàn giáo làm răng.

Bổ sung finding chot-loi-do-moi-chua-co-rang: n3 và n4 cũng sống sót 89/89. n3 bỏ bảo vệ `_peel_commit:1123`, làm object zlib hỏng từ nguyên trạng rc=2 thành rc=0. n4 bỏ bảo vệ `_nhanh_mac_dinh:1155` với git show-ref rc=128, làm ref chứa OID không có từ rc=2 thành fallback/rc=1. Gộp cùng n1/n2 vì đều là chốt lỗi đo mới chưa có ca khóa. Bằng chứng `evidence/new-mutants.log` và `evidence/witness-n{3,4}-*.log`.

### loc-ung-vien-commit-chua-co-rang [P1] Bỏ lọc object không peel thành commit mà 89 ca vẫn xanh
HÌNH DẠNG: bo-chon-ung-vien
TỆP/DÒNG: `ops/bien_nhan_v2.py:1141`; ca mơ hồ c91 tại `ops/bien_nhan_v2_test.py:3130`, đột biến m105 tại `3845`.
VẤN ĐỀ: Resolver mới phải phân ứng viên là commit với blob/tag không trỏ commit; chốt `if c` loại None sau peel quyết định điều đó. Ca c91/m105 chỉ dùng hai commit trùng tiền tố. Bỏ riêng `if c` làm `{commit, None}` bị báo là hai commit và đẩy lời khai có thể đo sang trạng thái mơ hồ/rc=2, trong khi tất cả 89 ca hiện hữu vẫn đạt. M6 đòi chốt này có răng.
ĐÃ THỬ NGHIỆM: `python3 -u new_mutations.py ... n7-peel-noncommit` ⇒ `89/89, red=[]`. `python3 -u mutant_witnesses.py`, cùng fixture commit `8ac070d5f378d156c368085f9bd62a4b9257b14a` + blob `8ac070dd934a9b962f63a96d2eec64e4304e8d46`: Git peel chọn được commit; nguyên trạng CLI rc=1, mutant rc=2/`mơ hồ — 2 commit chung tiền tố`. Cặp commit+tag trỏ blob cũng đổi sai tương tự. Log `evidence/collisions.log`, `evidence/witness-n7-peel-noncommit.log`, `evidence/new-mutants.log`.
ĐỘ TIN: cao

Bổ sung đóng finding lượt 1: năm mutant r2/r4/r5/r6/r8 đã kết thúc: bốn mutant selector **88/89**, đúng một ca đỏ `giet_that` c87/c87/c88/c88; mutant UTF8 r8 **87/89**, cả c91 và c92 đỏ đúng UnicodeDecodeError ở đường đọc receipt. Đây là chạy lại cả bộ ca trên từng bản sao, xác nhận răng mới khóa đúng năm chốt từng sống sót ở lượt trước (`evidence/old-mutants.log`).

## TÍNH TOÀN VẸN VÀ GIỚI HẠN

Kiểm cuối (`evidence/final-tree.json`): HEAD vẫn `ae0d06c23fb777545fd7547a07d9f368e4122f49`, tree `7312e5d65f57740d8673b5491357532c2b09c9a9`, status rỗng; hai tệp byte-identical với blob tại SHA; `git diff --check 4488444 HEAD` rc=0. SHA256 cổng `62fba57035122b23a04233c34c34a03c2438ec2a7365e6bb13f7acf8861c2619`, test `f8ba288c1a13e576f30be83f158021f66cfd29ff56cd7667c563120a52d3d189`.

Không sửa cay-kho/, không push, không gọi mạng. Chỉ đo code/fixture hiện hữu và đột biến trên bản sao. Không tạo HINT.patch; verdict này không đưa bản vá. Các log thử giàn giáo bị lỗi đã chỉ rõ và loại khỏi kết luận; corpus, suite, target mutation và phản chứng dùng các log cuối được nêu trong từng hướng.

Không xác minh PR/check run online hoặc việc ghi numstat vào PR. Shallow và partial clone (blob:none qua file://, có promisor pack/blob thiếu) đã đo trên fixture local; không đo máy chủ từ xa hoặc mọi filter, không bảo đảm ancestry ngoài lịch sử có sẵn. FIFO không thử vì có thể chặn đọc vô hạn; không gán kết quả chưa đo thành pass. Thời gian benchmark chỉ có ý nghĩa ở lượt chạy quan sát này. Không suy execution surface/transport từ tên launcher hoặc tên reviewer.

Các hình dạng **loi-do** và **bo-chon-ung-vien** tái xuất. Theo spec r2 Q8 / lease M-4, executor phải dừng để chủ kho quyết định trước khi vá tiếp; verdict không cấp quyền sửa, merge hoặc land.
