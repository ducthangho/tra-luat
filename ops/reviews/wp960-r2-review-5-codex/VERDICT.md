verdict: changes_requested
reviewed_sha: 6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf
Kết quả: 0 P0, 1 P1, 1 P2, 0 P3.

## BẢNG ĐO

Các cặp mã thoát `a/b` lần lượt là **không nợ / có mục nợ trúng khóa**; số `rc` của Git riêng được ghi tách khỏi `rc` của cổng.

| phép đo | lệnh | output / trạng thái |
|---|---|---|
| Exact head/spec | `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md` | HEAD `6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf`, tree `b95fb2108ab139c9a31f6f107797b00aa704ab34`, spec hash đúng `9a155cb…b1ca`; status sạch |
| Suite đầy đủ | `python3 -B -u /tmp/wp960-r5-copy/ops/bien_nhan_v2_test.py` | **93/93 ca, 129/129 thường CÓ RĂNG, 2/2 TỰ KIỂM, 111/129 khai đối chứng; rc=0/TỔNG: ĐẠT** (`evidence/suite.log`) |
| Gate corpus | `PYTHONDONTWRITEBYTECODE=1 python3 -B ops/bien_nhan_v2.py --root .` tại `cay-kho/` | rc=0; 244 v2 + 11 legacy + 42 nợ = 297 receipt; 0 vi phạm/0 unknown; nợ **1/60/0** |
| Ruff F so base | `python3 -B gate_checks.py` | base/head cùng 1 F541 dòng test:1677, delta=0 |
| Doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; 10 tệp, 0 chỗ chép doctrine |
| Diff-check | `git -C cay-kho diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD` | rc=0; stdout/stderr rỗng |
| Corpus nợ rỗng | `python3 -B corpus_review.py` | rc=1; đúng 61 dòng ba luật/0 lỗi khác/0 unknown; tập khóa = nợ |
| PR merge full history/no originHEAD | `python3 -B ci_review.py` | merge `e54e3a6…`, tree candidate; shallow=false; chỉ origin/master; gate rc=0/nợ1/60/0 |
| Đột biến reviewer | `python3 -B review_mutations.py <u1…u7>` | **7 lượt × 93ca: 4 bị giết, 3 survivor có witness**; không tính log giàn giáo hỏng |

## BẢNG ĐÓNG FINDING LƯỢT 4

| slug lượt 4 | trạng thái | lệnh | output thật |
|---|---|---|---|
| stderr-nen-nuot-loi-that | Đóng | `python3 -B stderr_extra.py stderr`; `python3 -B extra_review.py closure` | Cùng lỗi ở probe cũ và merge-base: 2/2; stderr chỉ ở probe đã xóa không còn được lấy làm nền; health mới có lỗi:2/2 |
| promisor-false-bi-coi-la-partial | Đóng | `python3 -B new_probes.py config`; `python3 -B extra_review.py promisor` | false/no/off: fsck0, gate1 đúng; true:gate2; corpus false cũng gate0/nợ1/60/0 |
| xoa-alternates-hop-le-lam-mat-object | Đóng | `python3 -B extra_review.py allowlist` | Dời nguyên object store: env/file cùng fsck0, gate1; không còn OID-missing giả |
| chot-probe-git-chua-co-rang | Đóng tại probe cũ; M6 tái xuất ở promisor (finding mới) | `python3 -B extra_review.py closure`; `python3 -B new_probes.py matrix` | Probe riêng đã xóa; --is-shallow-repository rc3/stdout=false và stderr-lỗi đều2/2; c96 qua, bao cả merge-base/health |

## BẢNG SĂN

| hướng độc lập | LỆNH | OUTPUT THẬT / kết luận |
|---|---|---|
| Stderr lỗi trùng nền | `python3 -B stderr_extra.py stderr` | same-error-wrong-ancestry=2/2; rc128=2/2; không nuốt lỗi nữa |
| Rc và stderr riêng lệnh sức khỏe | `python3 -B extra_review.py closure` | rc3 dù stdout=false =>2/2; stderr error=>2/2; cũ --git-dir đã xóa |
| Lệnh giả trong GIT_EXEC_PATH | `python3 -B extra_review.py allowlist` | fake_called=false; gate1/0, sáu builtin không bị thay |
| Object pool đầy đủ và OID ngoài | `python3 -B extra_review.py allowlist` | env/file pool cùng fsck0/gate1; foreign OID gate0 = nhập cùng byte object local, ancestry Git=1 |
| Worktree/env và cảnh báo | `python3 -B new_probes.py config`; `python3 -B extra_review.py closure` | worktree fsck0/gate1; GIT_DIR vắng vẫn1; warning1→2→1 đúng B2 |
| Boolean và promisor đa trị | `python3 -B extra_review.py promisor`; `python3 -B promisor_semantics.py` | false/no/off=1, true=2; true→false vẫn lazy-fetch qua remote file, không coi giá trị cuối làm oracle |
| Chuẩn hóa/kiểm dạng mới | `python3 -B extra_review.py survivors` | u4/off: head1/0→mutant2/2; u3/maybe: head2/2→mutant1/0; u3/u4 đều **93/93/red=[]** trên bản sao đầy đủ |
| Corpus và bánh cóc | `python3 -B corpus_review.py` | 31 token/99 lần, 61 khóa=nợ, unknown0; nợ rỗng1/61 luật/0 lỗi khác |
| Cô lập GIT_DIR riêng | `python3 -B gitdir_witness.py`; `python3 -B review_mutations.py u7-giu-GIT_DIR` | c95 qua và cả93ca qua khi cho GIT_DIR lọt; đổi master kho ngoài: head1/0→mutant0/1; P2 fixture |
| Topology checkout PR | `python3 -B ci_review.py` | merge2parent/tree candidate, full/nooriginHEAD, gate0/nợ1/60/0 |

## NHẬT KÝ TĂNG DẦN

- Khởi tạo verdict trước khi đọc mã và chạy kiểm tra.

### Hướng 1 — định danh và đặc tả

Lệnh: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`; `git -C cay-kho status --short`; `sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`.
Output thật: HEAD `6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf`; tree `b95fb2108ab139c9a31f6f107797b00aa704ab34`; status rỗng; spec SHA256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca`, đúng bản đóng băng. Đã đối chiếu lease g2, write set, sensitive, quyết định B1/B2 trong prompt. Mã đã bỏ `_NEN_STDERR` và probe riêng `--git-dir`; chưa coi việc đọc diff là bằng chứng đóng finding.

### Hướng 2 — gate corpus, doctrine, Ruff và phạm vi diff

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B ops/bien_nhan_v2.py --root .` và `.claude/dev/packet_loop.py doctrine-scan --root .` tại `cay-kho/`; `python3 -B -u gate_checks.py`.
Output thật: gate **rc=0**, `244 ĐẠT v2 · 11/11 legacy · 42 nợ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297`; nợ ba luật **1/60/0**, `TỔNG: ĐẠT`. Doctrine **rc=0**, quét 10 tệp/0 chỗ chép doctrine. Ruff `--select F` base/head đều rc=1, cùng **1 F541** tại test:1677, **delta=0** (`evidence/checks.log`). `git diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD` rc=0/stdout+stderr rỗng. Sau parent merge `43b96f0`, chỉ hai tệp packet thay đổi. Đo được Git 2.43.0, Python 3.13.17, Ruff 0.17.3.

### Hướng 3 — chạy lại phản chứng stderr/probe lượt 4

Lệnh: `python3 -B -u new_probes.py stderr`; `python3 -B -u stderr_extra.py stderr`; `python3 -B -u extra_review.py closure` (log `evidence/stderr*.log`, `evidence/closure.log`).
Output thật: wrapper lỗi trùng nền ở merge-base => **2/2**, không còn sạch/NỢ CHẾT. Phản chứng lỗi/rc3 chỉ ở `rev-parse --git-dir` => **1/0** vì probe ấy đã bị xóa, không còn là nguồn dữ liệu; lỗi stderr ở lệnh sức khỏe hiện hành và rc3 dù stdout=`false` => **2/2**. Cùng process/root, bật rồi bỏ fsync deprecated cho chuỗi **1→2→1**; lần 2 rc=2 là ĐÚNG theo B2, không lập lại finding cảnh báo. `GIT_DIR` trỏ kho không tồn tại vẫn **rc=1** theo kho gốc. Chưa lấy số tổng suite làm bằng chứng thay cho các phép này.

### Hướng 4 — danh sách cho phép: exec path và nguồn object ngoài

Lệnh: `python3 -B -u extra_review.py allowlist` (`evidence/allowlist.log`, `evidence/allowlist-complete-objects.log`).
Output thật: đặt sáu lệnh giả `git-{rev-parse,config,cat-file,for-each-ref,symbolic-ref,merge-base}` trong `GIT_EXEC_PATH`: gate **1/0**, **fake_called=false** cả hai lượt. Git 2.43.0 dùng builtin cho các lệnh đang đo. Dời nguyên object store ra pool: **fsck=0**, gate env/file alternates đều **rc=1**. OID chỉ có ở kho phụ: không pool => **2**, có pool => **0**, Git thật ancestry=1 (không là tổ tiên); nhập chính byte commit đó vào local object store cũng => **0**. Việc resolve object từ pool không tự chứng minh lỗi: phép so nhánh vẫn dùng ref của root và cho cùng đáp án khi object nằm local. Chưa thấy biến được giữ làm sai phép đo trong các thử này; không suy ra bảo đảm cho mọi phiên bản Git.

### Hướng 5 — promisor, worktree và cấu hình cảnh báo

Lệnh: `python3 -B -u new_probes.py config`; `python3 -B -u extra_review.py promisor` (`evidence/config.log`, `evidence/promisor.log`).
Output thật: các giá trị đơn `false/no/off` đều **fsck=0, rc=1**, đóng phản chứng tắt promisor; `true` => **rc=2**. Linked worktree thường => **fsck=0, rc=1**. HOME/includeIf và XDG phát cảnh báo fsync => **rc=2 đúng B2**. Chưa coi việc `config --get` trả false sau true là đủ để kết luận Git tắt promisor: đang đo trực tiếp hành vi Git để tránh gán nhầm ngữ nghĩa cấu hình đa trị.

### Hướng 6 — hai witness cho răng chốt promisor mới

Lệnh: `python3 -B -u extra_review.py survivors` (`evidence/survivors.log`).
Output thật: gỡ `--type=bool` (khác m132/m133), cấu hình đơn hợp lệ `remote.archive.promisor=off`: head **1/0**, mutant **2/2**, fsck=0; đây là witness Git thật của bước chuẩn hóa. Gỡ guard `gt not in ('true','false')`, wrapper chỉ trả stdout `remote.archive.promisor maybe`, rc=0/stderr rỗng ở config: head **2/2**, mutant **1/0**; đây là fault injection giao thức, không khai Git tự sinh dòng ấy. Đang chờ đo đủ 93 ca cho từng mutant để xác định chốt nào đã có răng.

### Hướng 7 — kiểm trực tiếp ngữ nghĩa promisor đa trị, bác nghi vấn bắt nhầm

Lệnh: `python3 -B -u promisor_semantics.py` (`evidence/promisor-semantics.log`). Chỉ dùng remote `file://` dựng từ `_kho_cau`; đặt `protocol.allow=never`, `protocol.file.allow=always`; không gọi mạng.
Output thật: với `true` rồi `false`, `git config --type=bool --get` in **false**, nhưng `git cat-file -t <commit chỉ ở remote file>` vẫn **rc=0/commit** (tự lấy object); chỉ có `false` thì **rc=128/could not get object info**; `false` rồi `true` lại **rc=0/commit**. Vì vậy không lấy giá trị cuối của `config --get` làm oracle cho nội bộ promisor của Git 2.43.0. Cổng chặn bất kỳ giá trị true là đúng trong đối chứng này; KHÔNG lập finding ghi đè boolean.

### Hướng 8 — corpus không nợ và CI PR merge

Lệnh: `python3 -B -u ci_review.py`; `python3 -B -u corpus_review.py` (log `evidence/ci.log`, `evidence/corpus.log`).
Output thật: **297 receipt, 99 lần xuất hiện/31 token phân biệt**, resolver không đổi đáp án so mã lượt 3; **61 khóa vi phạm = đúng tập nợ**, unknown=0. Nợ rỗng => **rc=1, 61 dòng ba luật, 0 lỗi khác, 0 unknown**. Merge mô phỏng **e54e3a69835a3874124f0ded0fd9437a6ff1c79e** có hai parent `2618eb4e59ab296e5dd8d2bc8543fe8e7e966b40` và reviewed SHA; tree **b95fb2108ab139c9a31f6f107797b00aa704ab34** đúng candidate; shallow=false, không `origin/HEAD`, `origin/master=2618eb4…`; gate **rc=0/TỔNG: ĐẠT**, nợ **1/60/0**. Đây là mô phỏng local checkout merge/fetch-depth:0, không khai CI GitHub online đã chạy.

### Sai giàn giáo reviewer, đã loại khỏi kết luận

Lượt `review_mutations.py` đầu dùng `_dot_bien_tep` cho cả 93 ca. Một ca tự kiểm dọn `_TAM_DOT_BIEN`, xóa luôn nguồn mutant đăng ký trong danh sách ấy; các ca sau c14/c44/c66/c68 gặp thiếu tệp. Các log `evidence/mutants-*-rig-broken.log` chỉ là bằng chứng GIÀN GIÁO LỖI, không được tính răng hoặc finding. Đã dừng các lượt đó và đổi sang bản sao đầy đủ riêng cho từng mutant, chỉ sửa đúng một mẫu trong nguồn trước khi import test; kiểm lại nguồn không đổi sau 93 ca. Chưa chốt verdict theo số mutant lỗi ấy.

### Hướng 9 — suite chính thức và corpus false đầy đủ

Lệnh: `python3 -B -u /tmp/wp960-r5-copy/ops/bien_nhan_v2_test.py`; trên bản sao nguyên cây tại đúng reviewed SHA: `git -C /tmp/wp960-r5-env config remote.archive.promisor false` rồi `python3 -B /tmp/wp960-r5-env/ops/bien_nhan_v2.py --root /tmp/wp960-r5-env`.
Output thật: suite **rc=0**, **93/93 ca · 129/129 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM · 111/129 khai đối chứng**, `TỔNG: ĐẠT` (`evidence/suite.log`). Corpus chỉ thêm promisor=false: **rc=0/TỔNG: ĐẠT, nợ1/60/0** (`evidence/corpus-promisor-false.log`), đóng cả phản chứng corpus của finding cũ. m125/m126/m129/m132/m133 đều `giet_that` trong log đầy đủ; không suy chúng khóa mọi bước mới trong cùng hàm.

### Hướng 10 — fixture GIT_DIR có thật sự phân biệt được kho?

Lệnh: `python3 -B -u gitdir_witness.py` (`evidence/gitdir-witness.log`); mutant chỉ thêm `GIT_DIR` vào `_GIT_GIU`, vẫn bỏ GIT_TRACE và mọi biến khác như head.
Output thật: **c95 vẫn `qua`**. Hai lần `_kho_cau` của fixture sinh đúng cùng **M=e72d8570d56391888423561308429963ae4f1b56** và cùng master=M, nên lấy kho ngoài vẫn cho ancestry=true như kho gốc. Đổi ĐÚNG master của kho ngoài thành X=`3ccd98856a70ffd3358ef59089963f08648370fc`, giữ object/receipt kho gốc: fsck kho ngoài=0; Git ancestry kho gốc=0, kho ngoài=1. Head **1/0** đúng; mutant **0/1 (NỢ CHẾT)** sai. Đây là phép đo Git thật, không có wrapper; đang chạy thêm mutant u7 qua toàn bộ93ca. Finding thuộc chất lượng fixture, không khai head đang chọn sai kho.

### Hướng 11 — phân biệt chốt trạng thái với chốt chẩn đoán

Lệnh: `python3 -B -u guard_witness.py` (`evidence/guard-witness.log`).
Output thật: u1 bỏ stderr guard; u2 chỉ lệnh sức khỏe bỏ `_git_do` và lấy stdout thẳng. Với stdout=`false` nhưng health có stderr error (u1), hoặc rc3/stderr rỗng (u2): head **2/2**, mutant **1/0**. Do đó cả hai đột biến đều có witness sai trạng thái độc lập, kể cả nếu ca hiện có làm đỏ trước vì thiếu chữ trong diagnostic. Dữ liệu là fault injection như c96, không gọi đó là lỗi Git tự nhiên.

### Hướng 12 — sáu đột biến đầy đủ đã hoàn tất, khác m132/m133

Lệnh: `python3 -B -u review_mutations.py <u1…u6>` (sáu lượt riêng, nguồn/bản sao riêng; `evidence/mutant-u1.log` đến `mutant-u6.log`). Mỗi mẫu thay khớp ĐÚNG1chỗ; nguồn sau suite vẫn bằng nguồn mutant lúc bắt đầu. Mỗi lượt gọi đủ93ca có sẵn, không chạy mutant lồng của suite. Output cuối:

| mutant | chốt gỡ | ca qua / tổng | ca ĐỎ và nguồn tín hiệu |
|---|---|---|---|
| u1-bo-stderr | Bỏ guard `if con` | 92/93 | c91 `giet_that`, mất diagnostic broken-ref (rc vẫn2); witness độc lập health-error cho head2/2→mutant1/0 |
| u2-bo-bien-suc-khoe | Chỉ health lấy stdout thẳng từ `_chay_git`, bỏ `_git_do` | 92/93 | c96 `giet_that`, rc vẫn2 nhưng mất diagnostic rc3; witness stdout=false/rc3 cho head2/2→mutant1/0 |
| u3-bo-kiem-dang-bool | Bỏ `if gt not in ('true','false')` | **93/93** | **Không ca nào đỏ**, red=[]; witness config trả maybe: head2/2→mutant1/0 |
| u4-bo-chuan-hoa-bool | Bỏ riêng `--type=bool` | **93/93** | **Không ca nào đỏ**, red=[]; Git thật promisor=off/fsck0: head1/0→mutant2/2 |
| u5-bo-loc-env | Bỏ lọc GIT_* (cùng cơ chế m126, khác m132/m133) | 92/93 | c95 `giet_that` ở git_trace, head1→mutant2; chưa đo riêng GIT_DIR bằng ca này |
| u6-bo-chan-promisor-true | Bỏ chặn giá trị true (cơ chế m129, khác m132/m133) | 92/93 | c91 `giet_that` ở partial clone thật: đòi2, được1 |

Không lấy mất diagnostic của u1/u2 làm bằng chứng đã kiểm đúng chuyển trạng thái; witness riêng đã ghi ở Hướng11. Hai survivor u3/u4 có witness không tương đương, đủ xác nhận một finding M6 ở phần đọc promisor mới. Lượt u7 riêng vẫn đang đo thêm.

## FINDING

### chot-promisor-moi-chua-co-rang [P1] Hai chốt đọc promisor mới vẫn gỡ được mà 93 ca không đỏ

HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1172`, `ops/bien_nhan_v2.py:1175`; `ops/bien_nhan_v2_test.py:3358`, `ops/bien_nhan_v2_test.py:3304`.
VẤN ĐỀ: M6 đòi đột biến cho từng chốt. Phần vá lượt4 thêm chuẩn hóa bằng `--type=bool` và chặn stdout không có giá trị true/false, nhưng bỏ riêng từng chốt vẫn **93/93**, không có ca `TinHieuChotCa` nào đỏ. c95 chỉ dùng giá trị nguyên văn `false`, nên không phân biệt lệnh đọc có/không chuẩn hóa; c94 không thử giao thức output của config promisor. m132 khóa điều kiện true/false sau khi đọc, không khóa bước chuẩn hóa hoặc guard kiểm dạng trước nó. Đây là thiếu răng mới ở M6; head xử lý đúng các witness đã đo, không khai có lỗi boolean đang xảy ra trên head.
ĐÃ THỬ NGHIỆM: `python3 -B -u review_mutations.py u3-bo-kiem-dang-bool` và `python3 -B -u review_mutations.py u4-bo-chuan-hoa-bool`: mỗi lượt bản sao đầy đủ, thay đúng1mẫu, **93/93, red=[]** (`evidence/mutant-u3.log`, `evidence/mutant-u4.log`). `python3 -B -u extra_review.py survivors`: u4 dùng **Git thật**, chỉ cấu hình đơn `remote.archive.promisor=off`, fsck=0/stderr rỗng; head **1/0**, mutant **2/2** vì đọc raw `off` thành dòng lạ. u3 dùng wrapper chỉ thay output config thành `remote.archive.promisor maybe`, rc0/stderr rỗng; head **2/2**, mutant **1/0**, lượt có nợ in `TỔNG: ĐẠT` thay vì không đo được (`evidence/survivors.log`). u3 là fault injection giao thức như c94, không tuyên bố Git thật tự sinh dòng maybe. Cả hai khác m132/m133 và có witness sai trạng thái, không phải mutant tương đương hoặc lỗi giàn giáo. Chốt P1 theo định nghĩa của prompt (“chốt không răng”/lệch M6), không theo một giả định về cấu hình cảnh báo đã được miễn B2.
ĐỘ TIN: cao

### c95-git-dir-khac-khong-phan-biet-kho [P2] Fixture GIT_DIR chọn kho ngoài có cùng đồ thị nên không đo được việc chọn nhầm kho

HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2_test.py:3349`, `ops/bien_nhan_v2_test.py:3352`; đối chiếu lời khai tại `ops/bien_nhan_v2_test.py:3341`.
VẤN ĐỀ: `git_dir_khac` gọi lại `_kho_cau(khac)` với ngày/nội dung ghim, nên kho ngoài có cùng M và master như kho cần đo. Khi cho GIT_DIR lọt vào, gate đo kho ngoài vẫn nhận cùng đáp án ancestry và c95 xanh. m126/u5 bị c95 giết ở GIT_TRACE, không chứng minh riêng fixture GIT_DIR phân biệt được nguồn. Đây là thiếu sót oracle của nhánh test khai kiểm việc GIT_DIR không đổi phép đo; phân P2 theo tiêu chí “ca test không đo đúng điều nó khai”. Head hiện tại vẫn bỏ GIT_DIR đúng; không lập finding hành vi sai trên head và không nhân P1 M6 chỉ vì thêm một tên biến.
ĐÃ THỬ NGHIỆM: `python3 -B -u review_mutations.py u7-giu-GIT_DIR`: bản sao đầy đủ, chỉ thêm GIT_DIR vào tập cho phép, giữ nguyên lọc GIT_TRACE/replace/alternates; **93/93, red=[]**, nguồn không đổi trong suite (`evidence/mutant-u7.log`). `python3 -B -u gitdir_witness.py`: c95 riêng `qua`; master/M của hai kho cùng **e72d8570d56391888423561308429963ae4f1b56**. Trên chính fixture ấy, đổi duy nhất master kho ngoài thành X=**3ccd98856a70ffd3358ef59089963f08648370fc**: fsck=0/stderr rỗng, Git ancestry ở kho gốc=0 và kho ngoài=1. Head **1/0**, mutant **0/1**, lượt có nợ kết luận NỢ CHẾT sai (`evidence/gitdir-witness.log`). Không wrapper, không object sai băm/commit-graph sai, không cấu hình phát cảnh báo.
ĐỘ TIN: cao

## HOÀN TẤT ĐO ĐỘT BIẾN

u7 đã xong **93/93, red=[]**. Tổng **7 mutant reviewer**, mỗi mutant đủ93ca: **4 bị giết bằng TinHieuChotCa, 3 survivor**. Cả3survivor có witness không tương đương: u3/u4 ở chốt promisor mới (gộp một P1), u7 ở nhánh fixture GIT_DIR (P2). Sáu mutant u1–u6 đáp ứng yêu cầu ≥5 chốt phần vá lượt4, không dùng m132/m133; u5/u6 được ghi rõ tái dùng cơ chế m126/m129, không giả nhận là mutant mới hoàn toàn. Không tính log giàn giáo hỏng.

Đối chứng OID kho ngoài đã đo thêm với **toàn bộ object đầy đủ** nhập local: `python3 -B -u extra_review.py allowlist` (`evidence/allowlist-complete-objects.log`), Git fsck **rc0/stderr rỗng**, chỉ thông báo dangling commit hợp lệ; gate **rc0** giống qua pool. Lần chép bổ sung đầu ghi đè object Git trùng đã read-only nên lỗi giàn giáo (`evidence/allowlist-copy-rig-broken.log`); đã đổi sang chỉ chép object còn thiếu, kiểm byte object trùng, rồi đo lại sạch. Lỗi chép và lỗi bộ gom JSON kéo theo không tính finding.

## READBACK CUỐI VÀ GIỚI HẠN

Lệnh: `python3 -B final_readback.py` (`evidence/final-readback.log`), **rc0**. HEAD vẫn **6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf**; tree **b95fb2108ab139c9a31f6f107797b00aa704ab34**; shallow=false; status rỗng; diff-check rc0/stdout+stderr rỗng. Product/test/spec trong cây review và baseline copy đều byte-identical với Git blob của reviewed SHA. SHA256 product **82a667496adc4ebbe9516f484fc4d9da4e79570ac20006b122a7400d0be539f6**, test **ee105c55140147c8cadb59f158cc2188602cc1bccbba3a4190b2bf5d10244039**, spec **9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca**. Numstat hai tệp so base: **+297/−193** và **+665/−104**, tổng **1.259 dòng**. Chưa đo disclosure ADR-0044 trên PR vì cấm mạng.

Đã đo bằng Git2.43.0/Python3.13.17/Ruff0.17.3 qua các lệnh ghi ở trên. Không tự khai execution surface, transport hoặc model runtime chưa đo được từ launcher/lease/tên tài khoản. CI PR GitHub thật, trạng thái PR/thread và authority ngoài snapshot: **KHÔNG ĐO ĐƯỢC trong nhiệm vụ cấm mạng**. Mô phỏng CI là local merge checkout với lịch sử đủ. Các wrapper và giới hạn của từng witness đã ghi riêng; không biến môi trường phát cảnh báo B2 hoặc object/graph sai im lặng B1 thành finding. Không thấy biến GIT_* cần bổ sung cho clone full-history và linked worktree thường trong các phép đo này; không khẳng định phủ mọi cấu hình hay phiên bản Git. Cấu hình credential của tác vụ mạng khác trong workflow không phải điều kiện của các phép đo builtin local đang review.

Không sửa `cay-kho/`, không push, không gọi mạng; các đột biến chỉ trên bản sao `/tmp`. Không tạo `HINT.patch`. Các lỗi giàn giáo reviewer đã tách và đo lại, không tính vào kết quả. Nhật ký trên giữ các trạng thái “đang đo” tại thời điểm ghi; bảng đầu và mục finding là kết quả cuối.

Bốn finding lượt4 đã đóng tại phản chứng/vị trí cũ; thiếu răng M6 tái xuất ở hai chốt promisor mới, và tìm thêm một P2 về oracle fixture GIT_DIR. Cả hai finding mang hình dạng **loi-do**; chưa thấy `bo-chon-ung-vien` hoặc `nguon-goc-cau` tái xuất. Với review class sensitive và còn P1/P2, verdict **changes_requested**. Q8/lease M-4 dành quyết định bước thi công tiếp cho chủ kho; review này không cấp quyền sửa nhánh, merge hoặc land.
