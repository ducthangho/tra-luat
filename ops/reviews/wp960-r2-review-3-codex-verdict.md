verdict: changes_requested
reviewed_sha: 934a5b063670acfbed410487d8244cd17d586d6e
Kết quả: 0 P0, 6 P1, 1 P2, 0 P3.

## BẢNG ĐO

| yêu cầu / lời khai executor | phép đo và output thật | kết luận |
|---|---|---|
| SHA/spec/class/write set | Hướng 1/13: HEAD 934a5b0…; tree d46fa5b0…; spec SHA256 9a155cb9…3b1ca; status rỗng; diff với master chỉ hai tệp | Đúng exact SHA; sensitive; nguồn không bị sửa |
| 1. Git chỉ tin rc sạch + stderr rỗng | Hướng 3/7: object sai băm và graph sai parent vẫn stderr rỗng/rc sạch; CLI 0 hoặc NỢ CHẾT/1. Hướng 11: cảnh báo vô hại làm corpus rc2 | Điều kiện được thi hành nhưng không đủ/không đúng để phân loại sức khỏe; hai finding P1 |
| 2. Ứng viên qua disambiguate + batch, chỉ commit | Hướng 2/8/12: hai commit → _MoHo/2; cùng commit+blob 8ac070d → đúng commit/1; c93/c94 qua; annotated tag trả None trong khi bản cũ peel | Đạt cơ chế được khai; không khác 31 token corpus, có đổi kết quả tag ngoài corpus |
| 3. for-each-ref + symbolic-ref | Hướng 2/12: corrupt loose ref và dangling symref → 2; Hướng 4/11: thêm master/topic hợp lệ → 2/dòng lạ | Đóng phản chứng ref cũ; bắt nhầm ref con, P1 |
| 4. Kho nông/partial | Hướng 2/12: shallow và extensions.partialclone → 2; Hướng 5: clone blob:none thật có promisor pack nhưng không có extension → accepted/CLI1 | Kho nông được chặn; lời khai partial rộng hơn phép đo, P2 |
| 5. merge-base, biên _sinh_no | Hướng 11: merge-base128/stderr rỗng → HEAD2; Hướng 2/12: ValueError/RecursionError → 2 qua cả ba cờ, không traceback | Đóng lỗi YAML cũ và giữ lỗi merge-base thành chưa đo ở nguyên trạng |
| 6. c91–c94 và m114–m124, neo mutant cũ | Hướng 2: 28/28 CLI c91 đúng nguồn, c92 10 hỏng/2 lành, c93/c94 qua; Hướng 10: 25 selected mutant giet_that, đối chứng qua | Khớp số đo được khai; không thay bằng chứng thiếu răng của u1 |
| 7. Suite chính thức | Hướng 10: 91/91 · 121/121 thường · 2/2 tự kiểm · 103/121 khai đối chứng, rc0 | Hai số ca bằng nhau; đạt suite |
| B7: gate/ruff/doctrine/diff | Hướng 10/13: gate0; ruff base=head=1 F541, delta0; doctrine0/10 tệp/0 chỗ; diff-check0 | Đạt kiểm cục bộ; PR/check run online không đo |
| M1/B1/B6 | Hướng 13: vế âm mốc 0 dòng; suite c86/m94 và target m78 đúng literal đỏ, folded vẫn được nhận | Không thấy nguồn-gốc-câu tái xuất |
| M5/B5 | Hướng 8/13: 297 receipt, 61 vi phạm khớp 61 nợ; bỏ nợ rc1/đúng61 dòng; HEAD code trên base data rc0/nợ1/60/0 | Đạt; base code r1 tự chạy có 3 surface cũ, đã tách rõ |
| Hồi quy và thời gian | Hướng 8: 99 lần/31 token không khác; median 36.9093→35.5060 giây, 1759→1761 git calls | Chưa thấy hồi quy corpus; thời gian có tải song song |
| CI pull_request đầy đủ, không origin/HEAD | Hướng 10: local merge2 parent, tree bằng HEAD, shallow=false, gate0/nợ1/60/0 | Đạt mô phỏng local |
| ≥5 mutant riêng/M6 | Hướng 9/11/13: năm mutant, mỗi cái chạy91 ca; u1 sống91/91 và witness lỗi128 thành1/0 | Không đạt M6; một P1 thiếu răng mới |
| Thay lịch sử/đổi kho qua Git | Hướng 6: replace/graft và GIT_DIR khác đều làm1→0 hoặc NỢ CHẾT/1, stderr rỗng | Hai P1 độc lập: lịch sử overlay, chọn nhầm kho |

## BẢNG ĐÓNG FINDING LƯỢT 2

| slug | trạng thái | lệnh chạy lại tại HEAD mới | output thật |
|---|---|---|---|
| sinh-no-van-thoat-loi-yaml | **ĐÓNG** | `python3 -u replay_r2_recheck.py yaml_errors`; `probe_recheck.py matrix` | Cùng timestamp sai/lồng1200: 6/6 CLI2 qua gate và hai cờ, không traceback; m109 chết đúng timestamp ở c92 |
| ref-hong-bi-doc-thanh-vang | **ĐÓNG phản chứng cũ** | `python3 -u replay_r2_recheck.py refs` | this-is-not-an-oid và dangling symref đều2; OID vắng/tree/blob đều2; ref vắng thật fallback và1. Finding prefix mới được tách riêng |
| peel-rc1-an-loi-object | **ĐÓNG phản chứng cũ** | `python3 -u replay_objects_recheck.py objects` | Cùng dbffbbc94…; object rỗng/zlib hỏng × có/không nợ: 4/4 CLI2, không NỢ CHẾT/traceback. Sai băm/graph là finding mới |
| chot-loi-do-moi-chua-co-rang | **ĐÓNG bốn chốt cũ; M6 còn finding mới** | `replay_r2_recheck.py symlinks`; `replay_objects_recheck.py objects`; `target_mutants_recheck.py` | Symlink gãy/vòng và OSError ELOOP đều2; m115/m116 giết đúng c91; peel/show-ref cũ đã bị thay, lỗi nguồn nguyên bản vẫn2, guard batch/ref có target m123/m124 giet_that. Chốt rc mới u1 sống91/91 được tách riêng |
| loc-ung-vien-commit-chua-co-rang | **ĐÓNG** | `python3 -u replay_objects_recheck.py collisions`; `target_mutants_recheck.py` | Cùng commit+blob8ac070d và commit+tag-trỏ-blob2f52361 → commit/CLI1; m120 giết đúng c93 vì blob không được tính vào số commit |

Log của bảng: `evidence-recheck/replay-*.log`, `matrix.log`, `target-mutants.log`. Trạng thái đóng neo phản chứng cụ thể; không tuyên bố đóng cả lớp lỗi Git/M6.

## BẢNG ĐÓNG FINDING LƯỢT 1 (r2)

| slug | trạng thái | lệnh | output thật |
|---|---|---|---|
| git-hong-thanh-token-thuong | **ĐÓNG** | `replay_objects_recheck.py objects`; `replay_r2_recheck.py gitfail`; c91/target m103 | dbffbbc lành1; Git vắng hoặc rc1/2/127/128/byte lỗi đều2; m103 đúng c91 git_vang |
| b2-chua-do-du-ma-tran | **ĐÓNG** | `probe_recheck.py matrix` | 14 nguồn × hai trạng thái nợ, 28/28 CLI2, stderr nêu nguồn, không traceback/NỢ CHẾT |
| run-json-thu-muc-thanh-khong-ap | **ĐÓNG** | `replay_r2_recheck.py symlinks`; c91/target m106 | run.json directory2/2 CLI2, m106 chết đúng run_json_thu_muc |
| nhanh-mac-dinh-tree-bi-bo-qua | **ĐÓNG** | `replay_r2_recheck.py refs`; target m104 | Ref tree thật CLI2; m104 chết đúng nhanh_la_tree, không fallback |
| sinh-no-ngoai-bien-doc-receipt | **ĐÓNG** | `probe_recheck.py matrix`; `replay_r2_recheck.py yaml_errors` | Hai cờ × directory/UTF8/YAML/timestamp/deep:10/10 CLI2, hai lành0; không traceback |
| bien-utf8-receipt-chua-co-rang | **ĐÓNG** | `target_mutants_recheck.py`/m107 | c91 giet_that đúng UnicodeDecodeError khi bỏ guard; nguyên trạng nguồn UTF8 hỏng CLI2 |
| b6-docstring-chua-khai-gioi-han | **ĐÓNG** | suite c72; `target_mutants_recheck.py`/m78 | Docstring khai folded chỉ hồi quy; m78 giet_that đúng khoi_lit, danh sách kết quả vẫn có khoi_gap |
| bo-chon-moi-chua-khoa-bien | **ĐÓNG** | `target_mutants_recheck.py`/m110–m113 | Đều giet_that đúng Precommit/backtick-chi-mo/notprovider/provider-dong-sau ở c87/c88; đối chứng qua |

## BẢNG SĂN

Đã đo 13 hướng; lệnh, stdout/stderr và các giới hạn chi tiết nằm ngay dưới trong nhật ký tăng dần.

| hướng | lệnh chính | output thật nổi bật |
|---|---|---|
| 1 — định danh | `git rev-parse HEAD HEAD^{tree}`; `sha256sum ...r2.md` | Đúng934a5b0…/d46fa5b0…/9a155cb9…, status rỗng |
| 2 — YAML/ma trận | `probe_recheck.py matrix`; `probe_recheck.py yaml_cli` | 28/28 c91 CLI2; timestamp/deep6/6 CLI2 |
| 3 — object/cảnh báo | `probe_recheck.py objects` | fsck3/sai băm nhưng CLI0 hoặc NỢ CHẾT1; trace/cảnh báo làm CLI2 |
| 4 — ref hậu tố | `probe_recheck.py objects`/branch-prefix | for-each-ref0/đúng dạng nhưng CLI2 |
| 5 — partial thật | `probe_recheck.py partial` | promisor=true/1 pack/4 blob thiếu, health accepted |
| 6 — overlay/kho khác/alternates | `extra_recheck.py extra` | replace/graft/GIT_DIR: CLI0 hoặc NỢ CHẾT1; alternate hỏng CLI2 |
| 7 — graph/pack/ref | `graph_recheck.py`; `extra_recheck.py extra broken-commit-graph pack-corrupt packed-ref-broken` | graph verify1 nhưng query im lặng/CLI0; ba hỏng khác CLI2 |
| 8 — corpus/tag/thời gian | `corpus_recheck.py`; `tag_recheck.py` | 31/31 token giữ kết quả, 61/61 nợ; tag peel trước/None nay; 1759→1761 git calls |
| 9 — mutant riêng | `mutations_recheck.py u1-rc-check u4-preserve-status u5-exception-boundary`; lượt u2/u3 | 91/91,79/91,90/91,90/91,90/91; phân loại từng ca thật/giả bên dưới |
| 10 — checks/suite/CI/target | suite; `ci_recheck.py`; `target_mutants_recheck.py` | 91/91·121/121·2/2, CI local0,25 target giet_that |
| 11 — corpus lành/witness rc | `extra_recheck.py clean_corpus`; `rc_witness_recheck.py` | Corpus0→2 chỉ do trace/cảnh báo/ref con; wrapper128:HEAD2/u1 là1 hoặc0 |
| 12 — phản chứng cũ nguyên bản | `replay_r2_recheck.py ...`; `replay_objects_recheck.py ...` | Symlink8/8 lỗi2; ref5/5 lỗi2; YAML6/6 lỗi2; object4/4 lỗi2; collisionblob1 |
| 13 — base/integrity | HEAD gate trên base; `checks_recheck.py` | Base data nợ1/60/0/rc0; blob nguyên byte; diff-check0; doctrine0 |

## NHẬT KÝ ĐO TĂNG DẦN

- Khởi tạo báo cáo trước khi chạy các hướng thử.

### Hướng 1 — định danh và bản sao

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain`; `git -C cay-kho rev-parse --is-shallow-repository`; `sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`.
Output: HEAD `934a5b063670acfbed410487d8244cd17d586d6e`, tree `d46fa5b04fd1ae9d1580b59ae90e58ed73852451`; status rỗng; shallow `false`; spec `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` khớp.
Đã tạo bản sao mới `/tmp/wp960-r3-recheck-copy` bằng `cp -a cay-kho ...`. Các script có sẵn trong thư mục giao việc và evidence cũ KHÔNG được coi là kết quả lượt chạy này; chỉ dùng code sau khi đọc và chạy lại vào `evidence-recheck/`. Suite đang chạy trên bản sao.

### Hướng 2 — ca mới và đóng lỗi YAML cũ

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_recheck.py matrix` (lần chạy thành công dùng cùng script đã chép sang `/tmp/probe_recheck.py`); `python3 -u probe_recheck.py yaml_cli`.
Output thật (`evidence-recheck/matrix.log`, `yaml-cli.log`): c91 **28/28** lời gọi CLI rc=2 (14 nguồn × có/không nợ), không Traceback/NỢ CHẾT, stderr nêu nguồn; c92 **10 hỏng rc=2 / 2 lành rc=0**; c93 và c94 đều `qua`. Phản chứng timestamp `2026-99-99` và YAML lồng 1.200 tầng: cả gate thường, `--sinh-no`, `--sinh-no-cau-lich-su` đều **rc=2**, đúng ValueError/RecursionError, không traceback. Phản chứng cũ `sinh-no-van-thoat-loi-yaml` đã đóng về hành vi. UTF8 và receipt-thư-mục cũng 3/3 rc=2; hai cờ sinh nợ trên dữ liệu YAML lành đều rc=0 (gate thường của đối chứng này vẫn rc=1 do câu ancestry và receipt chưa đủ schema, không gọi đó là sạch).

### Hướng 3 — object hỏng và điều kiện stderr rỗng

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_recheck.py objects` (`evidence-recheck/objects.log`). Object rỗng và zlib hỏng đều bị chặn rc=2 cả có/không nợ; phản chứng `peel-rc1-an-loi-object` cũ đã đóng. Tuy nhiên thay commit object M bằng zlib hợp lệ chứa commit đã bỏ parent, GIỮ nguyên đường dẫn OID M: `git fsck --full` rc=3 có `hash-path mismatch`, còn toàn bộ lệnh tra của cổng stderr RỖNG và đúng dạng; `merge-base --is-ancestor B0 master` rc=1. CLI từ rc=1 trước đột biến thành **rc=0/TỔNG: ĐẠT** sau đột biến (không nợ), hoặc **rc=1/NỢ CHẾT** (có nợ). Đây là phản ví dụ đo được cho tiền đề “stderr rỗng đủ tin”.
Đối chứng Git tracing và cấu hình lành `core.fsyncObjectFiles=true`: các lệnh git rc=0, stdout hợp lệ nhưng stderr có trace/cảnh báo deprecated; CLI lại rc=2. Sẽ bổ sung phép chạy trên corpus lành và đối chứng băm trước khi chốt finding.

### Hướng 4 — chọn ref hợp lệ có hậu tố

Cùng lệnh `probe_recheck.py objects`, fixture `branch-prefix`: remote `origin/master` hợp lệ; đổi nhánh local thành `main`, tạo local `master/topic`. `for-each-ref ... refs/heads/master` trả hợp lệ `refs/heads/master/topic ... commit`, stderr RỖNG. Cổng coi dòng đó là “dạng lạ” và cả có/không nợ đều **rc=2**, dù remote master hợp lệ và ancestry đo được (`merge-base` rc=0). Đã ghi nhận đường bắt nhầm của bộ chọn ref; sẽ chạy đối chứng chỉ thêm một remote ref trên corpus thật.

### Hướng 5 — partial clone thật

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_recheck.py partial` (`evidence-recheck/partial.log`), clone qua `file://` cục bộ với `--filter=blob:none --no-local --no-checkout`, không gọi mạng.
Output: clone rc=0; `remote.origin.promisor=true`, `remote.origin.partialclonefilter=blob:none`, 1 pack `.promisor`, `rev-list --objects --all --missing=print` có 4 blob vắng; KHÔNG có `extensions.partialclone`. `_kho_lanh` vẫn **accepted**, gate rc=1/L-ANCESTRY (không phải rc=2). Ca c91 chỉ bật `extensions.partialclone`, chưa đại diện clone partial thật do Git 2.43.0 tạo. Không tuyên bố phép ancestry trên fixture này sai: các commit cần dùng vẫn đủ; sai đã đo là chốt được khai chặn mọi partial clone không nhận ra kho partial thật này.

### Hướng 6 — thay lịch sử bằng replace/graft và đổi kho bằng môi trường

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u extra_recheck.py extra` (`evidence-recheck/extra.log`, dùng các dòng JSON hoàn tất trước lỗi giàn giáo commit-graph).
Output `replace-drop-parent`: tạo một commit KHÁC hợp lệ không parent rồi `git replace M <commit-khác>`; `git fsck --full` **rc=0, stderr rỗng**; lệnh ancestry mặc định **rc=1, stderr rỗng**, còn cùng lệnh với `GIT_NO_REPLACE_OBJECTS=1` **rc=0**. Cổng từ rc=1 thành **rc=0 sạch** hoặc **rc=1/NỢ CHẾT** dù ref và object gốc không đổi. Graft `M\n` + `advice.graftFileDeprecated=false` tái hiện cùng cặp 0/1/NỢ CHẾT, mọi truy vấn stderr rỗng.
Output `foreign-git-dir`: chỉ đặt `GIT_DIR=<kho fixture khác>/.git` (master của kho ấy ở X); `--root` vẫn kho ban đầu, các câu/allowlist không đổi. Các lệnh vẫn rc sạch/stdout đúng dạng, nhưng cổng từ rc=1 thành **rc=0 sạch** hoặc **NỢ CHẾT/rc=1**. `-C root` không neo được kho khi kế thừa `GIT_DIR`.
Đối chứng alternates vắng: 2/2 lượt (có/không nợ) rc=2, stderr nêu object directory không tồn tại, không traceback/NỢ CHẾT. Phép commit-graph đầu bị PermissionError khi script reviewer ghi file graph chỉ đọc, KHÔNG coi đó là lỗi sản phẩm; đã bổ sung chmod trên fixture và chạy lại riêng dưới `extra-b.log`.

### Hướng 7 — commit-graph/pack/packed-ref

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u graph_recheck.py`; `python3 -u extra_recheck.py extra broken-commit-graph pack-corrupt packed-ref-broken` (`evidence-recheck/graph.log`, `extra-b.log`).
Output graph: dùng `_kho_cau` thật, `git commit-graph write --reachable`, thay parent của M trong chunk CDAT thành `GRAPH_PARENT_NONE`, cập nhật checksum của graph. `git commit-graph verify` **rc=1**, stderr `parent list ... terminates early`; `git merge-base --is-ancestor B0 master` **rc=1/stderr rỗng**, cùng lệnh với `-c core.commitGraph=false` **rc=0/stderr rỗng**. CLI **rc=0 sạch** hoặc **rc=1/NỢ CHẾT**; object và ref nguyên vẹn. Đây là phản ví dụ thứ hai độc lập với loose-object sai băm, cùng bác bỏ tiền đề stderr.
Đối chứng graph sai chữ ký, pack bị đảo byte, packed-refs sai dòng: mỗi nguồn × có/không nợ đều rc=2, không traceback/NỢ CHẾT. Chỉ tính các output cuối ở `extra-b.log`, không tính PermissionError của giàn giáo ở lượt đầu.

### Hướng 8 — corpus và tag

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u corpus_recheck.py`; `python3 -u tag_recheck.py` (`evidence-recheck/corpus.log`, `tags.log`).
Output corpus HEAD: **297 receipt**, 99 lần xuất hiện/31 token phân biệt; resolver trước vá (`ae0d06c` nạp trong module riêng) và HEAD **không đổi kết quả nào**; 61/61 khóa vi phạm khớp tập nợ (1/60/0), unknown=0. Có nợ rc=0; bỏ nợ rc=1 với **đúng 61 dòng ba luật, 0 lỗi khác, 0 unknown**.
Benchmark xen kẽ 3 lần mỗi bên, chạy đồng thời với các test khác: trước vá **32.3257 / 46.7503 / 36.9093 giây**, HEAD **31.9130 / 43.4598 / 35.5060 giây**; git calls **1759 → 1761**. Median quan sát **36.9093 → 35.5060**; không suy ngưỡng hiệu năng ổn định từ tải song song.
Tag fixture: annotated tag `7de224f…` trỏ M và `0de74a3…` trỏ X; Git peel và resolver cũ ra đúng commit, HEAD trả `None` cho CẢ token ngắn/đủ 40. Với câu có `Commit <tag-OID>`, HEAD CLI rc=2. Đây là thay đổi ngữ nghĩa tag đã đo; không có tag nào gây khác kết quả trên 31 token corpus. Chưa coi tag OID là commit OID theo định nghĩa mới; ghi hồi quy/giới hạn, không tự suy thành finding từ việc Git có phép peel.

### Hướng 9 — đột biến reviewer (đang chạy)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u mutations_recheck.py u1-rc-check u4-preserve-status u5-exception-boundary` và lượt độc lập `... u2-default-commit u3-ambiguous` (`evidence-recheck/mutants-{a,b}.log`). Từng mutant tạo bản sao ngoài kho, chỉ thay một mẫu có count=1, chạy cả **91 ca có sẵn**; không chạy bộ mutant lồng bên trong. Cả năm khác m114–m124 (u2/u3 cố ý kiểm lại các chốt đã tồn tại m104/m105).
Kết quả đầu: u1 bỏ kiểm rc trong `_git_do` ⇒ **91/91, red=[]**. u2 bỏ điều kiện object-type của ref mặc định ⇒ **90/91**, c91 `giet_that` (vẫn rc=2 nhưng lý do đổi thành lỗi merge-base thay vì tên ref đầy đủ). Đang chạy ba mutant còn lại và phản chứng hành vi riêng cho u1, không coi một survivor chưa có witness là đủ bằng chứng.

### Hướng 10 — gate, CI và răng đột biến chính thức

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u /tmp/wp960-r3-recheck-copy/ops/bien_nhan_v2_test.py` đã hoàn tất: **91/91 ca đạt · 121/121 đột biến thường CÓ RĂNG · 2/2 tự kiểm · 103/121 khai đối chứng**, `TỔNG: ĐẠT` (`evidence-recheck/suite.log`). Không thiếu ca, không viện lỗi sandbox làm finding.
Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .` tại cây review: rc=0, **244 ĐẠT v2 · 11/11 legacy · 42 nợ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297**, nợ lịch sử **1/60/0**, `TỔNG: ĐẠT` (`gate.log`). `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: rc=0, **10 tệp, 0 chỗ chép doctrine** (`doctrine.log`); `git diff --check 4488444 HEAD`: rc=0/output rỗng (`diff-check.log`).
Lệnh: `python3 -m ruff check --no-cache --select F --output-format json .../ops` trên bản hai tệp trích từ base 4488444 và HEAD: mỗi bên đúng **1 F541** tại test dòng 1677, **delta 0** (`ruff-{base,head}.json`); cả hai lệnh rc=1 vì lỗi có sẵn, KHÔNG gọi là 0 lỗi tuyệt đối.
Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u ci_recheck.py` (`ci.log`): clone local, tạo merge hai parent `2618eb4…` và exact reviewed SHA, HEAD merge **a6012e53d719d5e10615af494335c0ae96b887fd**, tree **d46fa5b04fd1ae9d1580b59ae90e58ed73852451** trùng HEAD, shallow=false, không origin/HEAD, origin/master=2618eb4…; gate **rc=0/TỔNG: ĐẠT**, nợ 1/60/0. Chưa thấy `_kho_lanh` bắt nhầm mô phỏng CI đầy đủ này.
Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u target_mutants_recheck.py`: 25 mutant chọn riêng **m76/m78/m84/m92/m103–m107/m109–m124** đều `giet_that` ở target, đối chứng `qua` (`target-mutants.log`). m115/m116 chết đúng symlink gãy/tên quá dài, m109 chết đúng ValueError timestamp, m120 chết đúng commit+blob; xác nhận các răng cũ đã bổ sung. Việc đủ 121/121 không bao gồm chốt rc mới bị u1 gỡ mà vẫn 91/91.

### Hướng 11 — đối chứng lành trên corpus, và witness cho survivor

Lệnh: `python3 -u extra_recheck.py clean_corpus` ở bản sao riêng (`clean-corpus.log`, `clean-corpus-ref.log`); bản lần hai chỉ đo ref. Corpus không đổi: `GIT_TRACE=1` hoặc cấu hình `core.fsyncObjectFiles=true` qua `GIT_CONFIG_COUNT` ⇒ **rc=2 ngay ở `rev-parse --is-shallow-repository` rc=0**, stderr chỉ có trace hoặc cảnh báo deprecated. Lần đầu thử thêm remote `origin/master/topic` bị Git từ chối vì origin/master tồn tại; KHÔNG dùng lần ấy làm phản chứng ref. Lần cuối chỉ thêm **local `refs/heads/master/topic`** (local master vắng, `update-ref` rc=0), gate **rc=2/dòng lạ**, xoá ref thành công. Giữ nguyên SHA/corpus/default ref.
Lệnh: `python3 -u rc_witness_recheck.py` (`rc-witness.log`): cùng fixture `_kho_cau`, wrapper Git chỉ cho `merge-base` thoát **128 với stdout/stderr đều rỗng**, còn lệnh khác dùng Git thật. HEAD **rc=2** cả có/không nợ; mutant u1 **rc=1/L-ANCESTRY** không nợ, **rc=0/TỔNG: ĐẠT** có nợ. Chốt rc bị bỏ có thay đổi hành vi sai thật, và **91/91 ca** không khóa được nó: finding M6 mới.

## FINDING MỚI

### stderr-rong-van-tin-lich-su-hong [P1] Object sai băm và commit-graph sai parent vẫn được tin thành sạch hoặc nợ chết
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1134`, `1139`, `1151`, `1336`.
VẤN ĐỀ: Kiểm rc + stderr và hình dạng stdout không kiểm được tính toàn vẹn đồ thị commit. `_kho_lanh` chỉ hỏi shallow/partial, nên hai trạng thái hỏng có thể trả mã 0/1 sạch và được dùng để kết luận L-ANCESTRY. Lỗi đo bị biến thành sạch hoặc NỢ CHẾT, trái M2; đây là hành vi nguyên trạng, không phải chỉ lời khai rộng.
ĐÃ THỬ NGHIỆM: `python3 -u probe_recheck.py objects`, mục `valid-zlib-wrong-hash`: giữ đường dẫn OID M, thay nội dung bằng commit zlib hợp lệ đã bỏ parent; `git fsck --full` rc=3/hash-path mismatch, mọi truy vấn cổng stderr rỗng, CLI từ rc=1 thành rc=0 không nợ hoặc rc=1/NỢ CHẾT có nợ. `python3 -u graph_recheck.py`: sửa parent trong graph cache và cập nhật checksum, không sửa object/ref; `commit-graph verify` rc=1/terminates early, merge-base rc=1/stderr rỗng so với rc=0 khi tắt core.commitGraph; CLI cũng 0 hoặc NỢ CHẾT/1. Log `evidence-recheck/{objects,graph}.log`.
ĐỘ TIN: cao

### replace-graft-lam-sai-quan-he-oid [P1] Phép đo SHA bất biến bị thay bằng lịch sử overlay cục bộ
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1124`, `1139`, `1336`.
VẤN ĐỀ: `_kho_lanh` không từ chối graft/replace và truy vấn không vô hiệu hóa các overlay ấy. Chỉ thêm replace ref hoặc graft có thể xoá quan hệ parent mà object gốc và default ref vẫn nguyên vẹn. Vì stderr có thể rỗng, cổng tin đồ thị thay thế thành quan hệ của chính các OID được receipt nêu. Đây là vấn đề khác với sai băm: `fsck` của fixture replace vẫn sạch.
ĐÃ THỬ NGHIỆM: `python3 -u extra_recheck.py extra`, mục `replace-drop-parent`: tạo commit không parent hợp lệ rồi `git replace M <replacement>`; fsck rc=0/stderr rỗng; merge-base B0→master rc=1/stderr rỗng, cùng lệnh `GIT_NO_REPLACE_OBJECTS=1` rc=0. CLI từ vi phạm/1 thành sạch/0 hoặc NỢ CHẾT/1. Mục `graft-silent`: `info/grafts` chứa M và `advice.graftFileDeprecated=false` có cùng kết quả; không sửa receipt/ref master/object gốc. Log `evidence-recheck/extra.log` (các dòng JSON hoàn tất).
ĐỘ TIN: cao

### git-dir-ke-thua-do-nham-kho [P1] `--root` không neo được kho khi môi trường có GIT_DIR khác
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1130`, `1131`.
VẤN ĐỀ: `env={**os.environ, **_ENV_GIT}` giữ `GIT_DIR`. Git ưu tiên biến này hơn dò `.git` dưới `-C root`; cổng đọc receipt của kho A nhưng resolve/đo ancestry bằng kho B. Cả rc, stderr và giao thức đều có thể hợp lệ, không có cảnh báo về việc chọn nhầm kho. Kết luận về SHA/default branch của root vì thế sai dù hai kho đều lành.
ĐÃ THỬ NGHIỆM: `python3 -u extra_recheck.py extra`, mục `foreign-git-dir`: hai fixture `_kho_cau`, master kho B chuyển sang X; chỉ truyền `GIT_DIR=B/.git`, giữ `--root A` và toàn bộ receipt A. Các truy vấn stderr rỗng, master đọc ra X, ancestry M→master rc=1. CLI A trước đó rc=1, sau đó rc=0 sạch hoặc rc=1/NỢ CHẾT nếu có nợ. Log `evidence-recheck/extra.log`.
ĐỘ TIN: cao

### stderr-vo-hai-chan-nham-kho-lanh [P1] Trace và cảnh báo cấu hình deprecated làm corpus sạch bị chặn rc=2
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1124`, `1131`, `1134`.
VẤN ĐỀ: Điều kiện “bất kỳ stderr nào đều là lỗi đo” gộp chẩn đoán tùy chọn và cảnh báo cấu hình lành với lỗi Git. Một người bật tracing để chẩn đoán hoặc còn cấu hình fsync cũ không làm mất thông tin ancestry, nhưng cổng bắt cả lượt KHÔNG ĐO ĐƯỢC. Đây là bắt nhầm đã đo được theo yêu cầu (b), không chỉ nghi ngại giả định.
ĐÃ THỬ NGHIỆM: `python3 -u probe_recheck.py objects` đối chiếu từng lệnh: `GIT_TRACE=1` hoặc `core.fsyncObjectFiles=true` vẫn có stdout đúng và rc=0 (ancestry đúng). `python3 -u extra_recheck.py clean_corpus`: trên bản sao 297 receipt nguyên byte, vốn gate rc=0, chỉ thêm từng cấu hình trên ⇒ CLI rc=2 ngay ở `rev-parse --is-shallow-repository` rc=0. Stderr chỉ là trace hoặc `warning: core.fsyncObjectFiles is deprecated; use core.fsync instead`. Log `evidence-recheck/{objects,clean-corpus}.log`; fixture trước/sau 1→2, corpus thật 0→2.
ĐỘ TIN: cao

### for-each-ref-nhan-nham-ref-hau-to [P1] Nhánh master/topic hợp lệ làm hỏng phép chọn default ref
HÌNH DẠNG: bo-chon-ung-vien
TỆP/DÒNG: `ops/bien_nhan_v2.py:1182`, `1186`.
VẤN ĐỀ: Đối số của `for-each-ref` còn khớp các ref con theo tiền tố. Cổng truyền ba tên exact rồi coi bất kỳ tên con hợp lệ nào là stdout sai giao thức, ngay cả khi origin/HEAD hoặc origin/master dùng để đo hoàn toàn lành. Thêm một nhánh không liên quan có thể làm CI rc=2.
ĐÃ THỬ NGHIỆM: `python3 -u probe_recheck.py objects`, mục `branch-prefix`: remote master hợp lệ, local main + master/topic ⇒ for-each-ref rc=0/stderr rỗng có refs/heads/master/topic, ancestry đúng rc=0, CLI 2/2 lượt rc=2. `python3 -u extra_recheck.py clean_corpus` lượt ref (`clean-corpus-ref.log`): trên corpus 297 receipt, local master vốn vắng (`show-ref` rc=1); CHỈ thêm `refs/heads/master/topic` tại reviewed SHA (`update-ref` rc=0), gate từ 0 thành 2 với “trả dòng lạ”, xoá lại rc=0. Không đổi SHA/default ref/receipt. Lần thử thêm remote master/topic bị Git từ chối đã loại khỏi bằng chứng.
ĐỘ TIN: cao

### chot-ma-thoat-git-chua-co-rang [P1] Gỡ kiểm rc của kiến trúc mới mà cả 91 ca vẫn xanh
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1134`; `ops/bien_nhan_v2_test.py:3081`, `4013`.
VẤN ĐỀ: M6 đòi từng chốt có đột biến. m114 chỉ gỡ kiểm stderr, không khóa độc lập vế rc. Ca c84/c91 dùng lỗi Git có stderr nên vẫn đỏ đúng ở vế còn lại khi vế rc đã bị xóa. Toàn bộ suite chấp nhận một cổng không kiểm mã lỗi; witness cho thấy nó biến lỗi đo thành vi phạm hoặc sạch. Đây là chốt thiếu răng mới; bốn chốt thiếu răng lượt 2 đã được khóa lại, không đồng nghĩa M6 đã đủ cho kiến trúc thay thế.
ĐÃ THỬ NGHIỆM: `python3 -u mutations_recheck.py u1-rc-check ...` trên bản sao, chỉ đổi `if p.returncode not in sach or p.stderr.strip():` thành `if p.stderr.strip():` ⇒ **91/91, red=[]**. `python3 -u rc_witness_recheck.py`: Git wrapper chỉ trả merge-base rc=128/stdout rỗng/stderr rỗng; HEAD rc=2 cả có/không nợ; u1 rc=1/L-ANCESTRY không nợ và rc=0/TỔNG: ĐẠT có nợ. Log `evidence-recheck/{mutants-a,rc-witness}.log`. Không dùng exception vô can làm răng.
ĐỘ TIN: cao

### ca-partial-chi-bat-cau-hinh-cu [P2] Chốt và fixture partial clone chưa bao phủ clone partial thật
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1141`, `1145`; `ops/bien_nhan_v2_test.py:3193`.
VẤN ĐỀ: Docstring khai loại partial clone nhưng chỉ dò `extensions.partialclone`; c91 “kho_partial” thực chất đặt chính khóa đó vào một kho đủ. Git 2.43.0 tạo clone partial thật bằng `remote.origin.promisor=true`, `remote.origin.partialclonefilter=blob:none` và promisor pack, không có extensions.partialclone, nên chốt không chạy. Phép đo đóng băng chưa đại diện cho điều nó khai. Xếp P2 vì fixture này còn đủ commit cho ancestry; chưa đo được kết luận ancestry sai chỉ từ bốn blob vắng.
ĐÃ THỬ NGHIỆM: `python3 -u probe_recheck.py partial`: clone `file://` local với `--filter=blob:none --no-local --no-checkout`, rc=0; config như trên, 1 `.promisor`, rev-list xác nhận 4 blob `?OID` vắng; `_kho_lanh` accepted, CLI rc=1/L-ANCESTRY, thay vì chủ động báo partial/2. So c91 synthetic có extensions.partialclone bị chặn/2. Log `evidence-recheck/partial.log`, `matrix.log`.
ĐỘ TIN: cao

### Hướng 12 — chạy lại nguyên phản chứng của lượt 2

Đã chép nguyên hai script reviewer lượt 2 (`probe_r2.py`, `probe_objects.py`) sang `replay_r2_recheck.py`, `replay_objects_recheck.py`; chỉ đổi import bridge để dùng test/module tại bản sao exact SHA mới. Không dùng output của lượt cũ làm bằng chứng.
Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u replay_r2_recheck.py {symlinks|refs|yaml_errors|gitfail}` và `python3 -u replay_objects_recheck.py {objects|collisions}`. Output thật ở `evidence-recheck/replay-*.log`:

- Symlink gãy/tự vòng/vòng cha/directory: **8/8 lượt rc=2**, không traceback/NỢ CHẾT. Vắng thật hoặc cha là file: **rc=0 không nợ, rc=1/NỢ CHẾT có nợ**, giữ định nghĩa ENOENT/ENOTDIR đã khai.
- Loose ref `this-is-not-an-oid`, dangling symref, OID object vắng, tree/blob: **5/5 rc=2**, không traceback/NỢ CHẾT. Không origin/HEAD nhưng origin/master lành: **rc=1/L-ANCESTRY** đúng.
- Timestamp tháng sai và lồng 1.200 tầng nguyên như script cũ: **6/6 rc=2** qua ba cờ, không traceback; hai cờ sinh nợ trên YAML lành **2/2 rc=0**.
- Git shim thoát 1/2/127/128 và stdout UTF8 lỗi: **5/5 CLI rc=2**, không traceback/NỢ CHẾT.
- Cùng commit thuần chữ **dbffbbc94a7488c35d0a4050c1d26ffad20fa8ad**: đối chứng rc=1, object rỗng/zlib hỏng × có/không nợ **4/4 rc=2**. Kho nông trên cùng fixture: rc=2.
- Cùng cặp commit+blob **8ac070d5… / 8ac070dd…**: resolver chọn đúng commit, CLI rc=1. Cùng commit+tag-trỏ-blob tiền tố **2f52361**: rc=1. Cùng commit+tag-trỏ-commit-khác tiền tố **b4214fb**: HEAD giờ chọn direct commit/rc=1, trước vá mơ hồ/2; thay đổi này đúng định nghĩa resolver mới không peel tag, được ghi riêng với thử tag ở Hướng 8.

### Hướng 13 — hoàn tất năm mutant và kiểm tính toàn vẹn

Cả năm mutant reviewer đã chạy hết 91 ca, không dùng `tin_dung_gia` làm răng:

| mutant | chốt bị thay | kết quả | ca đỏ có tín hiệu thật / giới hạn |
|---|---|---|---|
| u1-rc-check | `_git_do` bỏ kiểm rc, giữ stderr | **91/91**, red=[] | Không có; witness Git rc=128/stderr rỗng đã cho kết quả sai thật |
| u2-default-commit | bỏ `lo != commit` ở default ref | **90/91** | c91 `giet_that`; mã vẫn 2, assertion bắt mất tên ref đầy đủ trong lý do |
| u3-ambiguous | bỏ `len(commit)>1` | **90/91** | c91 `giet_that` đúng `tien_to_mo_ho`: mutant rc=0 thay vì 2 |
| u4-preserve-status | `_git_do` đổi rc trả về thành 0 | **79/91** | c1/c14/c40/c76/c91 `giet_that`; 7 ca khác là exception `tin_dung_gia`, không tính răng. c1/c14 đo corpus bị kết luận thêm ancestry sai, c76 đo 62 thay vì 61 dòng |
| u5-exception-boundary | bỏ đổi OSError thành KhongDoDuoc ở `_git_do` | **90/91** | c91 `giet_that` đúng git vắng; mã vẫn 2 nhờ biên ngoài, khác chuỗi nguồn (`FileNotFoundError` thay thông điệp chuẩn). Không khai mutant này làm traceback |

Log `evidence-recheck/mutants-{a,b}.log`; script đòi từng mẫu thay có count=1. u2/u3 trùng ý nghĩa chốt cũ m104/m105, nhưng CẢ NĂM khác m114–m124 theo yêu cầu; ba chốt `_git_do` là của kiến trúc thay thế.

Lệnh `git checkout --detach 4488444...` chỉ trên `/tmp/wp960-r3-recheck-base`, rồi chạy cổng của chính base: **rc=0**, nợ 1/60/**3** theo luật r1 cũ (`base-gate.log`). Chạy cổng HEAD exact SHA trên dữ liệu base ấy: **rc=0/TỔNG: ĐẠT, nợ 1/60/0**, 0 unknown (`head-on-base-data.log`); không nhầm số nợ r1 với M5 mới.

Lệnh `python3 -u checks_recheck.py` (`final-checks.jsonl`): HEAD/tree vẫn đúng, status rỗng, hai tệp product/test và spec **byte-identical** với Git blob tại reviewed SHA. SHA256 product **a470a159b104d2b4f802d1ad0b6b8828094a59ac05b5ee49bd94891860d1d05f**; test **780d9bc534423e16c730b2e06e2612bcd6a7fdb94656927a06d9ca5922a0e2ca**. Spec khớp băm đóng băng. Diff-check vẫn rc=0; doctrine vẫn 10 tệp/0 chỗ/rc=0. Vế âm M1 `rg` **0 dòng/rc=1 vì không match**, vế dương c86/m94 đã đạt trong suite.
Diff so master `2618eb4` chỉ hai tệp packet; numstat so lease base: **+260/-193 product, +532/-104 test, tổng 1.089 dòng**. Riêng vá lượt 2: **+91/-42 product, +215/-36 test**. Không dùng thay đổi từ merge master làm finding vượt write set.

## GIỚI HẠN VÀ BÀN GIAO

Chỉ đo cục bộ bằng Git **2.43.0**, Python **3.13.17**, Ruff **0.17.3** (phiên bản đều có output thật). Không tự suy tên execution surface/transport từ launcher hoặc lease; không ghi danh tính runtime chưa đo. Không gọi mạng, không push, không sửa `cay-kho/`; toàn bộ đột biến ở các bản sao dưới `/tmp`. Không tạo `HINT.patch` vì đây là review kiến trúc, không có patch gợi ý để áp dụng. Các script và log chứng cứ mới nằm cạnh báo cáo và trong `evidence-recheck/`.

CI GitHub thật, trạng thái PR #995/thread và việc khai numstat/ADR-0044 trên PR: **KHÔNG ĐO ĐƯỢC** do yêu cầu không gọi mạng. Mô phỏng local đã được phân biệt với CI online. Không đo Windows/mọi phiên bản Git/mọi filter partial; không chạy FIFO có thể treo đọc. Thời gian benchmark có tải đồng thời, không kết luận tốc độ ổn định.

Các hình dạng **loi-do** và **bo-chon-ung-vien** tái xuất; **nguon-goc-cau** chưa thấy tái xuất (mã mốc đã bỏ và c86/m94 đạt). Q8/lease M-4 dành quyết định bước thi công tiếp theo cho chủ kho; báo cáo này hoàn thành nhiệm vụ review được giao, không cấp quyền vá, merge hoặc land.
