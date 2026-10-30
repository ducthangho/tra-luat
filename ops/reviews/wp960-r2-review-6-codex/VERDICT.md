verdict: changes_requested
reviewed_sha: 78c138f863696def68f88080b2b32057fe98f207
Kết quả: 0 P0, 2 P1, 0 P2, 0 P3.

Hai finding lượt 5 đã đóng tại phản chứng cũ. Toàn bộ r2 còn hai thiếu sót M6 về răng test: hai guard giao thức batch-check và ngữ cảnh OID trộn số/chữ. Mã cổng HEAD xử lý đúng các witness; ba phép gỡ chốt riêng vẫn qua đủ93 ca. Phân P1 theo tiêu chí “chốt không răng”/lệch M6 trong prompt. Chưa thấy hành vi sản phẩm HEAD sai trong các phép đo này.

Review chỉ đọc exact HEAD, risk sensitive; không sửa `cay-kho/`, không push, không gọi mạng. Các số `a/b` là **không nợ / có mục nợ trúng khóa**, trừ khi ghi khác. `HINT.patch` chỉ là gợi ý test đã kiểm trên scratch; không cấp quyền sửa nhánh, merge hay land.

## BẢNG ĐO

| Tiêu chí | Lệnh | Output thật / kết luận |
|---|---|---|
| Exact HEAD/spec/lease | `python3 -B review_checks.py` | SHA `78c138f863696def68f88080b2b32057fe98f207`, tree `609bc213c6cfca1195100ed3ebec357003f7ace7`; spec sha256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca`; lease r2/g2; status sạch. |
| Chỉ vá test từ lượt 5 | `git -C cay-kho diff --numstat 6dca85f HEAD -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` | `22 4 ops/bien_nhan_v2_test.py`; product byte-identical6dca85f. |
| Suite B7 | `PYTHONDONTWRITEBYTECODE=1 python3 -B -u /tmp/wp960-r6-review/head/ops/bien_nhan_v2_test.py` | **rc=0;93/93 ca ·132/132 đột biến thường CÓ RĂNG ·2/2 TỰ KIỂM ·114/132 khai đối chứng;TỔNG: ĐẠT** (`evidence/suite.log`). |
| M1/B1, bỏ mốc | `python3 -B -u review_probes.py acceptance`; `python3 -B -u review_audit.py debt`; mutant m94 qua `review_mutations.py official` | c86 qua cả review/ancestry; m94 bị c86 giết; AST không còn literal dung_tai/hàm mốc bị cấm. |
| M2/B2, biên lỗi | `python3 -B -u review_probes.py closure`; `... surface-errors` | c91=17 nguồn×2 trạng thái nợ, đều rc=2/không Traceback/NỢ CHẾT; JSON hỏng/UTF8/mảng/null/surface rỗng qua CLI10/10 rc2. c90/c92 qua, cờ sinh nợ không thoát ngoại lệ. |
| M3/B3, OID ngữ cảnh | `python3 -B -u review_probes.py acceptance`; `... mixed-witness` | c71/c78/c87 qua; HEAD token40 hex/backtick/commit/mixed thiếu→2; deadbeef/run thường→0; token thuần resolve được→1. **Răng riêng mixed chưa đạt M6**, finding2. |
| M4/B4, lời tự khai | `python3 -B -u review_probes.py acceptance` | c73/c79/c83/c88 qua: provider/citation/cửa sổ ba dòng/mọi khai báo trên dòng/caveat đúng. m110–m113 giết đúng trường cũ. |
| M5/B5, corpus HEAD | `python3 -B review_checks.py`; `python3 -B -u review_topology.py corpus` | rc=0;244 v2+11 legacy+42 nợ=297;0 vi phạm/0 unknown;nợ**1/60/0**. |
| B5, nợ rỗng | `python3 -B -u review_topology.py corpus` | rc=1,**61 dòng ba luật/0 lỗi khác/0 unknown**; tập khóa đúng NO_CAU_LICH_SU; mọi tệp có thật, nợ⊆bản đóng băng test. |
| B5, base4488444 | Cùng lệnh corpus | Gate gốc base rc=0/nợ1/60/3; **mã HEAD trên corpus base rc=0/nợ1/60/0**. Không trộn hai định nghĩa surface. |
| Bằng chứng từng mục nợ | `python3 -B -u review_audit.py debt` | **61/61**có chứng cứ Git/receipt độc lập:60 ancestry+1 review. Không dùng resolver sản phẩm làm oracle. |
| B6, literal/folded | c72 qua acceptance; m78 qua official | m78 giết đúng `khoi_lit`; `khoi_gap` vẫn bị nhận. Docstring khai folded chỉ hồi quy/không có chốt riêng. |
| B7, Ruff F | `ruff check --select F --output-format json /tmp/wp960-r6-review/ruff-{base,head}/ops` | base/head cùng1 F541 tại test:1677; delta 0 (`evidence/ruff-*.log`). |
| B7, doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` tại cay-kho | rc=0;quét10 tệp,0 chỗ chép doctrine. |
| B7, whitespace/size | `git -C cay-kho diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD`; `git -C cay-kho diff --numstat 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` | diff-check rc=0/output rỗng;product+297/−193,test+683/−104,tổng1.277 dòng. PR disclosure ADR-0044 online KHÔNG ĐO ĐƯỢC vì cấm mạng. |
| B8, hồi dựng nền | `python3 -B -u review_audit.py baseline` | c86/c89/c87/c88 trên module exactbase lần lượt đỏ vì mốc còn miễn,receipt-thư-mục crash,40 hex thiếu thành0,citation bị bắt nhầm1. Đây là nền cần đỏ; không phải finding HEAD. Không chứng kiến thời điểm executor bắt đầu. |
| CI pull_request mô phỏng | `python3 -B -u review_topology.py ci` | merge`0a29864728af196ede954cb4ce57b02ffb288d00`,2 parent,tree đúng candidate,shallow=false,không origin/HEAD,origin/master79dbaf4;gate rc=0/nợ1/60/0. |
| M6, răng chính thức chọn riêng | `python3 -B -u review_mutations.py official` | **35/35 giet_that**,35/35 đối chứng c18 qua,bao gồm m134–m136 đúng lý do. |
| M6, mutant reviewer | `python3 -B -u review_mutations.py <v1…v5>` | **5 mutant mới**;v1/v2/v3 mỗi lượt93/93, red=[] và có witness sai trạng thái;v4→c88đỏ,v5→c87đỏ,đối chứng qua. **M6 KHÔNG ĐẠT**. |
| HINT.patch | `python3 -B -u review_hint.py` | `patch --dry-run --fuzz=0 -p0`rc=0/không offset trên bản sao HEAD. Sau áp scratch:c94/c87 qua,v1/v2/v3 giet_that đúng ca,c18 qua. Chưa đo fullsuite của hint. |

## BẢNG ĐÓNG FINDING LƯỢT 5

| Slug | Trạng thái | Lệnh | Output |
|---|---|---|---|
| chot-promisor-moi-chua-co-rang | ĐÓNG tại hai chốt cũ | `python3 -B -u review_mutations.py official`; `python3 -B -u review_probes.py r5` | m134 bị c95 giết đúng promisor_tat/off; m135 bị c94 giết đúng promisor-gia-tri-la; cả hai đối chứng c18 qua. Witness head/mutant: u3=2/2→1/0; u4=1/0→2/2. |
| c95-git-dir-khac-khong-phan-biet-kho | ĐÓNG | Cùng hai lệnh trên, m136/u7 | m136 bị c95 giết đúng git_dir_khac (đòi1, được0); đối chứng qua. Master kho ngoài=X; witness HEAD1/0→mutant0/1. |

## BẢNG ĐÓNG PHẢN CHỨNG LƯỢT 1–4

“Đóng” dưới đây chỉ nói phản chứng/vị trí cũ; không suy cả hình dạng lỗi đã hết. M6 tái xuất tại hai finding mới.

| Lượt / slug | Lệnh tại HEAD | Output / trạng thái |
|---|---|---|
| 1/git-hong-thanh-token-thuong | `review_probes.py closure` c91; `review_mutations.py official` m103 | git vắng/token thuần→rc2; m103 bị bắt diagnostic đúng; đóng. |
| 1/b2-chua-do-du-ma-tran | closure c91; surface-errors | Đủ34 lượt nguồn c91+JSON CLI cả có/không nợ,rc=2/không NỢ CHẾT/Traceback; đóng. |
| 1/run-json-thu-muc-thanh-khong-ap | closure c91; official m106 | thư mục run.json→2/2;m106 bị bắt;đóng. |
| 1/nhanh-mac-dinh-tree-bi-bo-qua | closure c91;official m104 | origin/master là tree→2/2;không fallback;m104 bị bắt;đóng. |
| 1/sinh-no-ngoai-bien-doc-receipt | closure c92;official m108 | Hai cờ sinh nợ giữrc2 với nguồn lỗi;m108 bị bắt;đóng. |
| 1/bien-utf8-receipt-chua-co-rang | closure c91;official m107 | Byte UTF8→2/2;m107 bị c91 giết đúng UnicodeDecodeError;đóng. |
| 1/b6-docstring-chua-khai-gioi-han | acceptance c72;official m78 | Docstring có giới hạn;m78giết literal riêng;đóng. |
| 1/bo-chon-moi-chua-khoa-bien | official m110–m113 | Precommit/backtick-chi-mo/notprovider/provider-dong-sau giết đúng c87/c88;đóng bốn chốt cũ. |
| 2/sinh-no-van-thoat-loi-yaml | closure c92;official m109 | Timestamp lỗi/lồng sâu→rc2;gỡ biên thì bị bắt;đóng. |
| 2/ref-hong-bi-doc-thanh-vang | closure c91;official m114/m119 | Loose ref hỏng và symref gãy đều2/2;đóng. |
| 2/peel-rc1-an-loi-object | closure c91 | Object rỗng→2/2,stderr is empty;không coi là token thường;đóng. |
| 2/chot-loi-do-moi-chua-co-rang | official m114–m119 | Từng target giet_that/đối chứng qua;đóng tại các guard cũ. |
| 2/loc-ung-vien-commit-chua-co-rang | closure/suite c93;official m120 | Commit+blob chung tiền tố vẫn chọn commit;m120 bị c93giết;đóng. |
| 3/stderr-rong-van-tin-lich-su-hong | Quyết định B1 trong prompt | TIỀN ĐỀ được chủ kho loại khỏi phạm vi;không lặp finding,không khai gate thay fsck. |
| 3/replace-graft-lam-sai-quan-he-oid | closure c91/c95;official m127/m130 | replace không đổi đáp án1/0;grafts tắt warning vẫn2/2;đóng. |
| 3/git-dir-ke-thua-do-nham-kho | closure c95;r5-witness;official m136 | HEAD1/0 dù master kho ngoài=X;mutant0/1 và c95đỏ;đóng. |
| 3/stderr-vo-hai-chan-nham-kho-lanh | closure c95/c91;review_topology.py config | GIT_TRACE bị cô lập1/0;config warning→2đúng thiết kế B2. Không lặp phần đã được chủ kho miễn. |
| 3/for-each-ref-nhan-nham-ref-hau-to | closure c95;official m131 | Ref con không bị nhận nhầm;1/0;m131 bị bắt;đóng. |
| 3/chot-ma-thoat-git-chua-co-rang | closure c96;official m125;stderr | merge-base/health rc3→2/2;m125giet_that;đóng. |
| 3/ca-partial-chi-bat-cau-hinh-cu | closure c91;official m129 | Clone partial file:// thật bị chặn bởi promisor2/2;m129 bị bắt;đóng. |
| 4/stderr-nen-nuot-loi-that | `review_probes.py stderr` | Lỗi trùng chữ probe/merge-base→2/2;không nuốt lỗi;đóng. |
| 4/promisor-false-bi-coi-la-partial | `review_topology.py config`;r5-witness | false/no/off fsck0/gate1/0;true/yes/on2/2;đóng. |
| 4/xoa-alternates-hop-le-lam-mat-object | config;official m133 | Dời nguyên object store:env/file đều1/0;m133 bị bắt;đóng. |
| 4/chot-probe-git-chua-co-rang | stderr;closure c96;official m125 | Probe cũ --git-dir đã xóa;health rc=3/stdoutfalse và stderrerror đều2/2;m125bị bắt;đóng. |

Các tên script trong bảng này chạy bằng `python3 -B -u`; lệnh đầy đủ và output được giữ trong nhật ký và `evidence/`.

## BẢNG SĂN

| Hướng độc lập | Lệnh | OUTPUT THẬT / kết luận |
|---|---|---|
| Boolean và chọn kho — witness lượt 5 | `python3 -B -u review_probes.py r5` | u3head2/2→mutant1/0;u4head1/0→mutant2/2;u7head1/0→mutant0/1. Hai finding cũ đóng nhờ răng đúng ca. |
| Biên I/O/YAML/ref/clone | `python3 -B -u review_probes.py closure` | 10/10 ca qua;c91=34 lượt rc=2,không Traceback/NỢ CHẾT. |
| run.json hỏng qua CLI | `python3 -B -u review_probes.py surface-errors` | 5 loại nguồn×2 trạng thái nợ=10/10 rc2;không NỢ CHẾT/Traceback. |
| Chọn OID/bỏ mốc/surface | `python3 -B -u review_probes.py acceptance` | 13/13 ca qua;B1/B3/B4/B6 hành vi HEAD đúng trong các fixture. |
| Stderr/rc ngoài tập sạch | `python3 -B -u review_probes.py stderr` | Trùng lỗi ở merge-base2/2;healtherror2/2;healthrc=3/false2/2;chỉ probe cũ1/0. |
| Giao thức batch-check, so OID | `python3 -B -u review_mutations.py v1-batch-oid`; `... review_probes.py batch-witness` | 93/93red=[];sai OIDhead2/2→mutant1/0. Finding1. |
| Giao thức batch-check, loại object | `python3 -B -u review_mutations.py v2-batch-type`; cùng batch-witness | 93/93red=[];loại nonsense: HEAD2/2→mutant0/1,có NỢ CHẾT. Cùngfinding1. |
| Ngữ cảnh OID trộn độc lập | `python3 -B -u review_mutations.py v3-mixed-context`; `... review_probes.py mixed-witness` | 93/93red=[];Git thật 12ab34c không resolve:head2/2→mutant0/1. Finding2. |
| Cửa sổ trước và phân biệt hoa | `python3 -B -u review_mutations.py v4-window-before`; `... v5-commit-case` | v4c88 giet_that/i-tu-khai;v5c87 giet_that/sau-commit;đối chứng c18 qua. |
| Cấu hình hợp lệ/object pool/worktree | `python3 -B -u review_topology.py config` | false/no/off1/0;env/file alternates1/0;linked worktree1/0;GIT_COMMON_DIR/GIT_CONFIG_COUNT cô lập1/0. |
| Corpus/bánh cóc | `python3 -B -u review_topology.py corpus`; `... review_audit.py debt` | nợrỗng1/61luật/0 lỗikhác/0 unknown;61/61 khóa có bằng chứng độc lập;head/basecorpus nợ1/60/0. |
| Checkout PR merge full history | `python3 -B -u review_topology.py ci` | Merge2 parent/tree candidate;shallow=false;không origin/HEAD;rc=0/nợ1/60/0. |
| Nền trước revision | `python3 -B -u review_audit.py baseline` | B1/B2/B3/B4 đỏ đúng hành vi nền trên4488444;HEADcác ca tương ứngqua. |

## FINDING

### chot-oid-va-loai-batch-check-chua-co-rang [P1] Hai guard giao thức còn gỡ riêng được mà cả93 ca đều qua

HÌNH DẠNG: loi-do

TỆP/DÒNG: `ops/bien_nhan_v2.py:1189`; `ops/bien_nhan_v2_test.py:3316`, `ops/bien_nhan_v2_test.py:4160`.

VẤN ĐỀ: M6 đòi đột biến cho từng chốt. Guard `_loai_object` kiểm ba điều: arity, OID trả về bằng OID yêu cầu, và loại object thuộc tập cho phép. c94 chỉ tiêm batch-check có BA cột (`<oid> commit thua`), nên riêng kiểm arity đã đủ làm ca ấy qua; m123 cũng bỏ nhiều vế cùng lúc. Bỏ riêng phép so OID hoặc riêng whitelist loại đều không làm bất kỳ ca nào trong93 ca đỏ. Cổng HEAD xử lý đúng witness; finding là thiếu răng M6, không khai có bypass Git thật đang xảy ra.

ĐÃ THỬ NGHIỆM: `python3 -B -u review_mutations.py v1-batch-oid` và `... v2-batch-type`: mỗi bản sao đầy đủ từ reviewed SHA, thay đúng1 mẫu, **93/93, red=[]**, nguồn mutant giữ nguyên sau phép đo. `python3 -B -u review_probes.py batch-witness`: fixture Git thật, token thuần chữ `dbffbbc` resolve ra commit; wrapper chỉ thay stdout của batch-check, rc=0/stderr rỗng. Sai OID: HEAD **2/2**, mutant **1/0**. Sai loại `nonsense`: HEAD **2/2**, mutant **0/1**, có nợ in **NỢ CHẾT**. Cặp số = không nợ/có nợ. Fixture fsck rc=0, không đổi object/graph. Đây là fault injection giao thức tương tự c94, không tuyên bố Git thật sinh output giả. Logs: `evidence/v1-batch-oid.log`, `evidence/v2-batch-type.log`, `evidence/batch-witness.log`. Hai mutant khác m123 vì mỗi mutant chỉ bỏ một vế và vẫn giữ kiểm arity.

ĐỘ TIN: cao

### ngu-canh-tron-so-chu-chua-co-rang-rieng [P1] Từ Commit trong c71 che mất chốt OID trộn số–chữ

HÌNH DẠNG: bo-chon-ung-vien

TỆP/DÒNG: `ops/bien_nhan_v2.py:986`; `ops/bien_nhan_v2_test.py:2660`, `ops/bien_nhan_v2_test.py:2949`.

VẤN ĐỀ: M3/B3 có bốn điều kiện độc lập cho token thiếu; M6 đòi răng từng chốt. c87 khai trộn số/chữ đã có ở c71, nhưng c71 dùng câu `Commit 1234abc chua vao master.`. Vì vậy điều kiện đứng sau từ commit vẫn trả rc=2 kể cả khi bỏ riêng `_oid_tron(x)` trong `_oid_bat_buoc`. Không ca hay mutant hiện hữu nào khóa riêng ngữ cảnh trộn số/chữ. Đây là thiếu răng M6, không khai HEAD đang xử lý sai token ấy.

ĐÃ THỬ NGHIỆM: `python3 -B -u review_mutations.py v3-mixed-context`: thay duy nhất `if len(x) == 40 or _oid_tron(x):` bằng `if len(x) == 40:`, giữ nguyên resolver và ngữ cảnh commit/backtick. Bản sao đầy đủ exact HEAD: **93/93, red=[]**, source không đổi sau93 ca. `python3 -B -u review_probes.py mixed-witness`: Git thật, `_commit_cua('12ab34c') is None`, fsck=0, câu `Ban 12ab34c chua vao master.` không backtick/từ commit; HEAD **2/2**, mutant **0/1**, có nợ in **NỢ CHẾT**. Không wrapper, không đổi object/graph hay cấu hình cảnh báo. Logs: `evidence/v3-mixed-context.log`, `evidence/mixed-witness.log`. Mutant khác m99 (gỡ độ dài40), m100 (gỡ ngữ cảnh commit), m84 (loại token thuần trước resolver).

ĐỘ TIN: cao

Gợi ý cho cả hai finding nằm trong `HINT.patch`: thêm ba hàng fixture độc lập và ba mutant riêng. Đã dry-run `patch --dry-run --fuzz=0 -p0` sạch trên bản sao exact HEAD; sau áp scratch, c94/c87 qua và cả ba survivor bị giết đúng nguyên nhân, đối chứng c18 qua (`evidence/hint-validation.log`). Chưa áp hint vào cây review.

## NHẬT KÝ ĐO TĂNG DẦN

- Khởi tạo VERDICT.md với verdict:dang_lam trước khi chạy kiểm tra. Đã nối bằng chứng sau từng hướng.

### Hướng 1 — exact SHA, đặc tả và phạm vi vá

Lệnh `python3 -B review_checks.py` (phần identity): HEAD/tree = `78c138f863696def68f88080b2b32057fe98f207
609bc213c6cfca1195100ed3ebec357003f7ace7`; status rỗng; spec sha256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` đúng. `git diff --numstat 6dca85f 78c138f863696def68f88080b2b32057fe98f207 -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py`: `22	4	ops/bien_nhan_v2_test.py`. Product so lượt 5 byte-identical. Log: `evidence/identity.log`, `evidence/patch-scope.log`.

### Kiểm tra corpus

Lệnh `/usr/bin/python3 -B ops/bien_nhan_v2.py --root .` tại `cay-kho/`: rc=0; output:

```text
bien_nhan_v2: 244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT

```
Log `evidence/corpus.log`.

### Kiểm tra doctrine

Lệnh `/usr/bin/python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` tại `cay-kho/`: rc=0; output:

```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine

```
Log `evidence/doctrine.log`.

### Kiểm tra diff-check

Lệnh `git diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD` tại `cay-kho/`: rc=0; output:

```text


```
Log `evidence/diff-check.log`.

### Ruff F delta so base

Lệnh `ruff check --select F --output-format json /tmp/wp960-r6-review/ruff-{base,head}/ops` trên byte từ `git show`: `{"base": [["bien_nhan_v2_test.py", "F541", {"column": 19, "row": 1677}, "f-string without any placeholders"]], "head": [["bien_nhan_v2_test.py", "F541", {"column": 19, "row": 1677}, "f-string without any placeholders"]]}`; delta=0. Logs `evidence/ruff-*.log`.

### Hướng 3 — mutant chính thức và răng đúng ca

Lệnh `python3 -B -u review_mutations.py official`: 35/35 mutant được chọn trả `giet_that`; đối chứng c18 đều `qua`. Bao gồm m134→c95/promisor_tat, m135→c94/promisor-gia-tri-la, m136→c95/git_dir_khac. Log nguyên nhân assertion: `evidence/official-mutants.log`.

### Hướng 4 — chạy lại CHÍNH u3/u4/u7 và witness lượt 5

Lệnh `python3 -B -u review_probes.py r5`. Trên HEAD: u3/config trả maybe → 2/2; u4/Git thật promisor=off → 1/0; u7/master kho ngoài=X → 1/0. Trên bản sao gỡ đúng chốt: tương ứng 1/0, 2/2, 0/1 (u7 có nợ in NỢ CHẾT). fsck các fixture=0. Hai số là không nợ/có nợ trúng khóa. Log `evidence/r5-witness.log`. Không nhận các hành vi mutant là lỗi hiện hữu trên HEAD; răng test được đo riêng bằng m134–m136.

### Hướng 7 — lỗi stderr trùng probe và rc sức khỏe

Lệnh `python3 -B -u review_probes.py stderr`: same-error-wrong-ancestry=2/2; health-error=2/2; health rc3 dù stdout=false=2/2; chỉ lỗi ở probe --git-dir đã xóa=1/0. Đóng phản chứng nuốt stderr lượt 4 và chốt rc/probe. Đây là fault injection bằng wrapper chuyển tiếp Git thật, không khai Git tự sinh chẩn đoán giả. Log `evidence/stderr.log`.

### Hướng 5 — biên lỗi và đóng phản chứng lượt 1–4

Lệnh `python3 -B -u review_probes.py closure`: 10/10 ca có sẵn `qua`; từng lời gọi CLI/API và output rc/diagnostic được ghi thật trong `evidence/closure.log`. Không sửa test; chỉ gắn bộ ghi vào helper khi chạy trên bản sao. c91 đo 17 nguồn × 2 trạng thái nợ, c77 đo JSON/UTF8 lỗi, c92 đo hai cờ sinh nợ; c94/c95/c96 đo giao thức/env/rc.

### Hướng 6 — M1/M3/M4 và B1/B3/B4/B6

Lệnh `python3 -B -u review_probes.py acceptance`: 13/13 ca có sẵn `qua`; từng lời gọi CLI/API và output rc/diagnostic được ghi thật trong `evidence/acceptance.log`. Không sửa test; chỉ gắn bộ ghi vào helper khi chạy trên bản sao. Bỏ mốc không còn miễn câu; OID thiếu theo bốn ngữ cảnh; token thuần có/không resolve; surface ba dòng/cả hai thứ tự/caveat; literal và folded.

### Hướng 8 — witness độc lập cho hai guard batch-check

Lệnh `python3 -B -u review_probes.py batch-witness`: chỉ thay stdout cat-file, rc=0/stderr rỗng. Sai OID (v1): HEAD2/2 → mutant1/0. Sai loại nonsense (v2), token thật thuần chữ dbffbbc không ngữ cảnh: HEAD2/2 → mutant0/1, lượt có nợ in NỢ CHẾT. Kho fixture fsck=0; đây là fault injection giao thức tương tự c94, không phải trạng thái Git thật tự sinh. Đang chờ đủ93 ca để xác định thiếu răng. Log `evidence/batch-witness.log`.

### Hướng 11 — cấu hình lành, object pool và linked worktree

Lệnh `python3 -B -u review_topology.py config`: false/no/off=1/0, true/yes/on=2/2; các boolean fixture fsck=0. Dời nguyên object store ra pool qua env hoặc info/alternates đều1/0. Linked worktree thường1/0; GIT_COMMON_DIR sai và GIT_CONFIG_COUNT tiêm warning bị cô lập nên1/0. Log `evidence/config.log`. Không biến cảnh báo deprecated cấu hình thực của B2 thành finding.

### Hướng 10 — mô phỏng CI pull_request

Lệnh `python3 -B -u review_topology.py ci`: merge `0a29864728af196ede954cb4ce57b02ffb288d00`, hai parent `79dbaf443f90daece751d9ab2537796bbd6084bf` + `78c138f863696def68f88080b2b32057fe98f207`, tree `609bc213c6cfca1195100ed3ebec357003f7ace7` đúng candidate, shallow=false (tương ứng fetch-depth:0), origin/HEAD vắng, origin/master=79dbaf443f90daece751d9ab2537796bbd6084bf; gate rc=0/TỔNG: ĐẠT, nợ1/60/0. Log `evidence/ci.log`. Đây là mô phỏng local, không phải check run GitHub online.

### Hướng 9 — tái sinh nợ độc lập trên base và HEAD

Lệnh `python3 -B -u review_topology.py corpus`: HEAD nợ rỗng rc=1, đúng61 dòng ba luật (1/60/0), 0 lỗi khác, 0 unknown; tập khóa bằng NO_CAU_LICH_SU; mọi tệp có thật; tập nợ ⊆ bản đóng băng test. Base exact4488444: gate gốc rc=0; mã HEAD trên corpus base rc=0/nợ1/60/0. Log `evidence/corpus-independent.log`.

### Hướng 12 — ngữ cảnh trộn số/chữ bị từ Commit che trong fixture

Lệnh `python3 -B -u review_probes.py mixed-witness`: fixture Git thật, câu `Ban 12ab34c chua vao master.`; token không resolve, không backtick/từ commit; fsck=0. HEAD2/2; bản sao chỉ bỏ `_oid_tron(x)` trong `_oid_bat_buoc` thành0/1, có nợ kết luận NỢ CHẾT. c71 hiện dùng `Commit 1234abc`, nên ngữ cảnh sau commit vẫn cứu được phép đo khi gỡ chốt trộn số/chữ. Đang chờ đủ93 ca; log `evidence/mixed-witness.log`.

### Suite chính thức hoàn tất

Lệnh `PYTHONDONTWRITEBYTECODE=1 python3 -B -u /tmp/wp960-r6-review/head/ops/bien_nhan_v2_test.py`: rc=0; **93/93 ca đạt · 132/132 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM · 114/132 khai đối chứng; TỔNG: ĐẠT**. Log `evidence/suite.log`. Tỷ lệ tổng này không tự chứng minh các chốt chưa có mutant riêng đều có răng.

### Hai survivor batch-check đã đo đủ93 ca

Lệnh `python3 -B -u review_mutations.py v1-batch-oid` và `... v2-batch-type`: mỗi lượt bản sao đầy đủ từ exact HEAD, thay đúng1 mẫu; **93/93, red=[]**; nguồn mutant không đổi sau các ca. Không chạy đột biến lồng trong hai lượt này. Cùng witness Hướng8 xác nhận hai guard không tương đương nhưng chưa có ca bắt. Log `evidence/v1-batch-oid.log`, `evidence/v2-batch-type.log`.

### HINT.patch kiểm trên bản sao exact HEAD

Lệnh `python3 -B -u review_hint.py`: tạo HINT.patch dạng `patch -p0`; `patch --dry-run --fuzz=0 -p0 -i HINT.patch` trên bản sao tại78c138f rc=0, `checking file ops/bien_nhan_v2_test.py`, không fuzz/offset. Sau áp trên scratch: c94/c87 nguyên trạng qua; v1/v2/v3 đều `giet_that` vì đúng batch-check-sai-oid / batch-check-sai-loai / tron-so-chu-rieng; đối chứng c18 qua. Gợi ý chỉ sửa test, chưa áp vào cay-kho; chưa khai full suite của hint. Log `evidence/hint-validation.log`.

### Hướng 13 — đủ5đột biến reviewer khác mutant hiện hữu

Lệnh `python3 -B -u review_mutations.py <v1…v5>` trên bản sao riêng, mỗi mutant thay đúng1 mẫu: v1 so OID batch-check, v2 whitelist loại batch-check, v3 ngữ cảnh trộn số/chữ đều **93/93, red=[]**; v4 bỏ dòng trước trong cửa sổ bị c88 giết đúng i-tu-khai (1→0); v5 bỏ IGNORECASE của từ commit bị c87 giết đúng sau-commit (2→0); hai đối chứng c18 qua. Đây là5 mutant mới: v4 khác m113/bỏ dòng sau; v5 khác m100/bỏ toàn bộ ngữ cảnh commit. Nguồn mutant giữ nguyên sau đo. Logs `evidence/v*.log`; không tính lỗi giàn giáo thành răng.

### Hướng 14 — B8 hồi dựng trên exact base

Lệnh `python3 -B -u review_audit.py baseline`: dùng module gốc từ4488444 với bốn ca hiện hữu c86/c89/c87/c88. Lần lượt đỏ đúng: mốc còn miễn câu (rc0), receipt-thư-mục thoát IsADirectoryError, OID40 thiếu thànhrc0, dòng trích dẫn bị nhậnrc1. Đây là kết quả nền cần ĐỎ theo B8, không phải finding ở HEAD; ca tương ứng trên HEAD đã qua. Log `evidence/baseline.log`. Không khai đã chứng kiến thời điểm executor trước khi bắt tay; đây là hồi dựng ngoại tuyến.

### Hướng 15 — bằng chứng độc lập cho61 khóa nợ và mã bỏ mốc

Lệnh `python3 -B -u review_audit.py debt`: duyệt từng khóa đóng băng;60 khóa ancestry có ít nhất1commit tra bằng `git rev-parse --verify --quiet <token>^{commit}` rồi Git merge-base=0/stderr rỗng;1 khóa review có biên nhận khác đúng40 hex và luot lớn hơn. **61/61 có bằng chứng độc lập**, không dùng `_commit_cua`/kết quả vi_pham_cau làm oracle. AST mã sản phẩm không còn literal dung_tai hay hàm mốc/lịch sử bị cấm. Log `evidence/debt-audit.log`. Regex vẫn chỉ chọn ứng viên theo phạm vi đặc tả.

### Readback cuối trên cây được review

Lệnh kiểm byte `git show 78c138f863696def68f88080b2b32057fe98f207:<tệp>` và `git status --short`/`git diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba HEAD`: HEAD/tree `78c138f863696def68f88080b2b32057fe98f207
609bc213c6cfca1195100ed3ebec357003f7ace7`; status sạch, diff-check rc=0/stdout/stderr rỗng. Product/test/spec vẫn bằng blob exact reviewed SHA. Không sửa cay-kho. Numstat packet so base: product+297/−193, test+683/−104, tổng1.277 dòng. Disclosure ADR-0044 trên PR online KHÔNG ĐO ĐƯỢC do cấm mạng; không suy từ numstat rằng disclosure đã có.

### Hướng 16 — run.json hỏng qua CLI cả hai trạng thái nợ

Lệnh `python3 -B -u review_probes.py surface-errors`: thay đúng run.json của fixture có sẵn thành JSON lỗi, UTF8 lỗi, JSON mảng, null, surface rỗng; **10/10 lượt CLI rc=2**, có/không nợ L-SURFACE trúng khóa, stderr nêu run.json, không Traceback/NỢ CHẾT. Bổ sung bằng chứng CLI cho c77 API. Log `evidence/surface-errors.log`.

## GIỚI HẠN VÀ KẾT LUẬN CUỐI

Đã đo Git 2.43.0,Python 3.13.17,Ruff 0.16.9. Không suy execution surface,transport hay model runtime từ tên thư mục/lease/tài khoản. GitHub check run thật,PR disclosure ADR-0044,thread và authority ngoài snapshot: **KHÔNG ĐO ĐƯỢC** vì nhiệm vụ cấm mạng. CI ở đây là mô phỏng local. Không gặp thông báo “Codex home is inside a repository” trong log đo.

Hai lỗi giàn giáo reviewer đã sửa và đo lại: bộ chọn ID mutant đọc m2b sai kiểu số; bộ ghi JSON witness dùng trùng khóa mutant. Output trước khi sửa không được tính là răng/finding. Không có lỗi giàn giáo trong các log kết quả cuối. Không gọi mạng,không push,không sửa cay-kho; mọi mutant nằm trên scratch.

M1–M5 có bằng chứng hành vi đạt trong các phép đo; **M6 chưa đạt** vì ba survivor không tương đương, gom thành hai P1. Hình dạng **loi-do** và **bo-chon-ung-vien** tái xuất ở răng test; chưa thấy **nguon-goc-cau** tái xuất. Đây kích hoạt điều kiện M-4/Q8 cho quyết định của chủ kho; review này không cấp quyền thi công thêm hay land. Verdict **changes_requested**.

Nhật ký trên giữ nguyên các trạng thái “đang chờ” ở thời điểm ghi; các bảng đầu,hai finding và kết luận cuối là trạng thái sau cùng.
