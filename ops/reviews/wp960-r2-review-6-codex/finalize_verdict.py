from pathlib import Path
import hashlib
import json
import re
import subprocess
from review_checks import ROOT, SHA, BASE, E

p=ROOT.parent/'VERDICT.md'
current=p.read_text()
findings=current.split('## FINDING ĐÃ XÁC NHẬN\n\n',1)[1].split('### Hướng 1',1)[0]
journal='### Hướng 1'+current.split('### Hướng 1',1)[1]
closure=current.split('## BẢNG ĐÓNG FINDING LƯỢT 5\n\n',1)[1].split('## BẢNG SĂN',1)[0]

intro=f'''verdict: changes_requested
reviewed_sha: {SHA}
Kết quả: 0 P0, 2 P1, 0 P2, 0 P3.

Hai finding lượt5 đã đóng tại phản chứng cũ. Toàn bộ r2 còn hai thiếu sót M6 về răng test: hai guard giao thức batch-check và ngữ cảnh OID trộn số/chữ. Mã cổng HEAD xử lý đúng các witness; ba phép gỡ chốt riêng vẫn qua đủ93ca. Phân P1 theo tiêu chí “chốt không răng”/lệch M6 trong prompt. Chưa thấy hành vi sản phẩm HEAD sai trong các phép đo này.

Review chỉ đọc exact HEAD, risk sensitive; không sửa `cay-kho/`, không push, không gọi mạng. Các số `a/b` là **không nợ / có mục nợ trúng khóa**, trừ khi ghi khác. `HINT.patch` chỉ là gợi ý test đã kiểm trên scratch; không cấp quyền sửa nhánh, merge hay land.

## BẢNG ĐO

| Tiêu chí | Lệnh | Output thật / kết luận |
|---|---|---|
| Exact HEAD/spec/lease | `python3 -B review_checks.py` | SHA `{SHA}`, tree `609bc213c6cfca1195100ed3ebec357003f7ace7`; spec sha256 `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca`; lease r2/g2; status sạch. |
| Chỉ vá test từ lượt5 | `git -C cay-kho diff --numstat 6dca85f HEAD -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` | `22 4 ops/bien_nhan_v2_test.py`; product byte-identical6dca85f. |
| Suite B7 | `PYTHONDONTWRITEBYTECODE=1 python3 -B -u /tmp/wp960-r6-review/head/ops/bien_nhan_v2_test.py` | **rc0;93/93ca ·132/132đột biến thường CÓ RĂNG ·2/2TỰ KIỂM ·114/132khai đối chứng;TỔNG:ĐẠT** (`evidence/suite.log`). |
| M1/B1, bỏ mốc | `python3 -B -u review_probes.py acceptance`; `python3 -B -u review_audit.py debt`; mutant m94 qua `review_mutations.py official` | c86 qua cả review/ancestry; m94 bị c86 giết; AST không còn literal dung_tai/hàm mốc bị cấm. |
| M2/B2, biên lỗi | `python3 -B -u review_probes.py closure`; `... surface-errors` | c91=17nguồn×2trạng thái nợ, đều rc2/không Traceback/NỢ CHẾT; JSON hỏng/UTF8/mảng/null/surface rỗng qua CLI10/10rc2. c90/c92 qua, cờ sinh nợ không thoát ngoại lệ. |
| M3/B3, OID ngữ cảnh | `python3 -B -u review_probes.py acceptance`; `... mixed-witness` | c71/c78/c87 qua; HEAD token40hex/backtick/commit/mixed thiếu→2; deadbeef/run thường→0; token thuần resolve được→1. **Răng riêng mixed chưa đạt M6**, finding2. |
| M4/B4, lời tự khai | `python3 -B -u review_probes.py acceptance` | c73/c79/c83/c88 qua: provider/citation/cửa sổ ba dòng/mọi khai báo trên dòng/caveat đúng. m110–m113 giết đúng trường cũ. |
| M5/B5, corpus HEAD | `python3 -B review_checks.py`; `python3 -B -u review_topology.py corpus` | rc0;244v2+11legacy+42nợ=297;0vi phạm/0unknown;nợ**1/60/0**. |
| B5, nợ rỗng | `python3 -B -u review_topology.py corpus` | rc1,**61dòng ba luật/0lỗi khác/0unknown**; tập khóa đúng NO_CAU_LICH_SU; mọi tệp có thật, nợ⊆bản đóng băng test. |
| B5, base4488444 | Cùng lệnh corpus | Gate gốc base rc0/nợ1/60/3; **mã HEAD trên corpus base rc0/nợ1/60/0**. Không trộn hai định nghĩa surface. |
| Bằng chứng từng mục nợ | `python3 -B -u review_audit.py debt` | **61/61**có chứng cứ Git/receipt độc lập:60ancestry+1review. Không dùng resolver sản phẩm làm oracle. |
| B6, literal/folded | c72 qua acceptance; m78 qua official | m78 giết đúng `khoi_lit`; `khoi_gap` vẫn bị nhận. Docstring khai folded chỉ hồi quy/không có chốt riêng. |
| B7, Ruff F | `ruff check --select F --output-format json /tmp/wp960-r6-review/ruff-{{base,head}}/ops` | base/head cùng1F541 tại test:1677; delta0 (`evidence/ruff-*.log`). |
| B7, doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` tại cay-kho | rc0;quét10tệp,0chỗ chép doctrine. |
| B7, whitespace/size | `git -C cay-kho diff --check {BASE} HEAD`; `git -C cay-kho diff --numstat {BASE} HEAD -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` | diff-check rc0/output rỗng;product+297/−193,test+683/−104,tổng1277dòng. PR disclosure ADR-0044 online KHÔNG ĐO ĐƯỢC vì cấm mạng. |
| B8, hồi dựng nền | `python3 -B -u review_audit.py baseline` | c86/c89/c87/c88 trên module exactbase lần lượt đỏ vì mốc còn miễn,receipt-thư-mục crash,40hex thiếu thành0,citation bị bắt nhầm1. Đây là nền cần đỏ; không phải finding HEAD. Không chứng kiến thời điểm executor bắt đầu. |
| CI pull_request mô phỏng | `python3 -B -u review_topology.py ci` | merge`0a29864728af196ede954cb4ce57b02ffb288d00`,2parent,tree đúng candidate,shallow=false,không origin/HEAD,origin/master79dbaf4;gate rc0/nợ1/60/0. |
| M6, răng chính thức chọn riêng | `python3 -B -u review_mutations.py official` | **35/35giet_that**,35/35đối chứng c18qua,bao gồm m134–m136 đúng lý do. |
| M6, mutant reviewer | `python3 -B -u review_mutations.py <v1…v5>` | **5mutant mới**;v1/v2/v3 mỗi lượt93/93/red=[] và có witness sai trạng thái;v4→c88đỏ,v5→c87đỏ,đối chứng qua. **M6 KHÔNG ĐẠT**. |
| HINT.patch | `python3 -B -u review_hint.py` | `patch --dry-run --fuzz=0 -p0`rc0/không offset trên bản sao HEAD. Sau áp scratch:c94/c87qua,v1/v2/v3giet_that đúng ca,c18qua. Chưa đo fullsuite của hint. |

## BẢNG ĐÓNG FINDING LƯỢT 5

'''

old_closure='''## BẢNG ĐÓNG PHẢN CHỨNG LƯỢT 1–4

“Đóng” dưới đây chỉ nói phản chứng/vị trí cũ; không suy cả hình dạng lỗi đã hết. M6 tái xuất tại hai finding mới.

| Lượt / slug | Lệnh tại HEAD | Output / trạng thái |
|---|---|---|
| 1/git-hong-thanh-token-thuong | `review_probes.py closure` c91; `review_mutations.py official` m103 | git vắng/token thuần→rc2; m103 bị bắt diagnostic đúng; đóng. |
| 1/b2-chua-do-du-ma-tran | closure c91; surface-errors | Đủ34lượt nguồn c91+JSON CLI cả có/không nợ,rc2/không NỢ CHẾT/Traceback; đóng. |
| 1/run-json-thu-muc-thanh-khong-ap | closure c91; official m106 | thư mục run.json→2/2;m106bị bắt;đóng. |
| 1/nhanh-mac-dinh-tree-bi-bo-qua | closure c91;official m104 | origin/master là tree→2/2;không fallback;m104bị bắt;đóng. |
| 1/sinh-no-ngoai-bien-doc-receipt | closure c92;official m108 | Hai cờ sinh nợ giữrc2 với nguồn lỗi;m108bị bắt;đóng. |
| 1/bien-utf8-receipt-chua-co-rang | closure c91;official m107 | Byte UTF8→2/2;m107bị c91 giết đúng UnicodeDecodeError;đóng. |
| 1/b6-docstring-chua-khai-gioi-han | acceptance c72;official m78 | Docstring có giới hạn;m78giết literal riêng;đóng. |
| 1/bo-chon-moi-chua-khoa-bien | official m110–m113 | Precommit/backtick-chi-mo/notprovider/provider-dong-sau giết đúng c87/c88;đóng bốn chốt cũ. |
| 2/sinh-no-van-thoat-loi-yaml | closure c92;official m109 | Timestamp lỗi/lồng sâu→rc2;gỡ biên thì bị bắt;đóng. |
| 2/ref-hong-bi-doc-thanh-vang | closure c91;official m114/m119 | Loose ref hỏng và symref gãy đều2/2;đóng. |
| 2/peel-rc1-an-loi-object | closure c91 | Object rỗng→2/2,stderr is empty;không coi là token thường;đóng. |
| 2/chot-loi-do-moi-chua-co-rang | official m114–m119 | Từng target giet_that/đối chứng qua;đóng tại các guard cũ. |
| 2/loc-ung-vien-commit-chua-co-rang | closure/suite c93;official m120 | Commit+blob chung tiền tố vẫn chọn commit;m120bị c93giết;đóng. |
| 3/stderr-rong-van-tin-lich-su-hong | Quyết định B1 trong prompt | TIỀN ĐỀ được chủ kho loại khỏi phạm vi;không lặp finding,không khai gate thay fsck. |
| 3/replace-graft-lam-sai-quan-he-oid | closure c91/c95;official m127/m130 | replace không đổi đáp án1/0;grafts tắt warning vẫn2/2;đóng. |
| 3/git-dir-ke-thua-do-nham-kho | closure c95;r5-witness;official m136 | HEAD1/0 dù master kho ngoài=X;mutant0/1 và c95đỏ;đóng. |
| 3/stderr-vo-hai-chan-nham-kho-lanh | closure c95/c91;review_topology.py config | GIT_TRACE bị cô lập1/0;config warning→2đúng thiết kế B2. Không lặp phần đã được chủ kho miễn. |
| 3/for-each-ref-nhan-nham-ref-hau-to | closure c95;official m131 | Ref con không bị nhận nhầm;1/0;m131bị bắt;đóng. |
| 3/chot-ma-thoat-git-chua-co-rang | closure c96;official m125;stderr | merge-base/health rc3→2/2;m125giet_that;đóng. |
| 3/ca-partial-chi-bat-cau-hinh-cu | closure c91;official m129 | Clone partial file:// thật bị chặn bởi promisor2/2;m129bị bắt;đóng. |
| 4/stderr-nen-nuot-loi-that | `review_probes.py stderr` | Lỗi trùng chữ probe/merge-base→2/2;không nuốt lỗi;đóng. |
| 4/promisor-false-bi-coi-la-partial | `review_topology.py config`;r5-witness | false/no/off fsck0/gate1/0;true/yes/on2/2;đóng. |
| 4/xoa-alternates-hop-le-lam-mat-object | config;official m133 | Dời nguyên object store:env/file đều1/0;m133bị bắt;đóng. |
| 4/chot-probe-git-chua-co-rang | stderr;closure c96;official m125 | Probe cũ --git-dir đã xóa;health rc3/stdoutfalse và stderrerror đều2/2;m125bị bắt;đóng. |

Các tên script trong bảng này chạy bằng `python3 -B -u`; lệnh đầy đủ và output được giữ trong nhật ký và `evidence/`.

## BẢNG SĂN

| Hướng độc lập | Lệnh | OUTPUT THẬT / kết luận |
|---|---|---|
| Boolean và chọn kho — witness lượt5 | `python3 -B -u review_probes.py r5` | u3head2/2→mutant1/0;u4head1/0→mutant2/2;u7head1/0→mutant0/1. Hai finding cũ đóng nhờ răng đúng ca. |
| Biên I/O/YAML/ref/clone | `python3 -B -u review_probes.py closure` | 10/10caqua;c91=34lượt rc2,không Traceback/NỢ CHẾT. |
| run.json hỏng qua CLI | `python3 -B -u review_probes.py surface-errors` | 5loại nguồn×2trạng thái nợ=10/10rc2;không NỢ CHẾT/Traceback. |
| Chọn OID/bỏ mốc/surface | `python3 -B -u review_probes.py acceptance` | 13/13caqua;B1/B3/B4/B6 hành vi HEAD đúng trong các fixture. |
| Stderr/rc ngoài tập sạch | `python3 -B -u review_probes.py stderr` | Trùng lỗi ở merge-base2/2;healtherror2/2;healthrc3/false2/2;chỉ probe cũ1/0. |
| Giao thức batch-check, so OID | `python3 -B -u review_mutations.py v1-batch-oid`; `... review_probes.py batch-witness` | 93/93red=[];sai OIDhead2/2→mutant1/0. Finding1. |
| Giao thức batch-check, loại object | `python3 -B -u review_mutations.py v2-batch-type`; cùng batch-witness | 93/93red=[];loạinonsensehead2/2→mutant0/1,cóNỢCHẾT. Cùngfinding1. |
| Ngữ cảnh OID trộn độc lập | `python3 -B -u review_mutations.py v3-mixed-context`; `... review_probes.py mixed-witness` | 93/93red=[];Gitthật12ab34c không resolve:head2/2→mutant0/1. Finding2. |
| Cửa sổ trước và phân biệt hoa | `python3 -B -u review_mutations.py v4-window-before`; `... v5-commit-case` | v4c88giet_that/i-tu-khai;v5c87giet_that/sau-commit;đối chứng c18qua. |
| Cấu hình hợp lệ/object pool/worktree | `python3 -B -u review_topology.py config` | false/no/off1/0;env/filealternates1/0;linkedworktree1/0;GIT_COMMON_DIR/GIT_CONFIG_COUNTcôlập1/0. |
| Corpus/bánh cóc | `python3 -B -u review_topology.py corpus`; `... review_audit.py debt` | nợrỗng1/61luật/0lỗikhác/0unknown;61/61khóa có bằng chứng độc lập;head/basecorpus nợ1/60/0. |
| Checkout PR merge full history | `python3 -B -u review_topology.py ci` | Merge2parent/treecandidate;shallowfalse;khôngorigin/HEAD;rc0/nợ1/60/0. |
| Nền trước revision | `python3 -B -u review_audit.py baseline` | B1/B2/B3/B4 đỏ đúng hành vi nền trên4488444;HEADcác ca tương ứngqua. |

## FINDING

'''

tail='''
## GIỚI HẠN VÀ KẾT LUẬN CUỐI

Đã đo Git2.43.0,Python3.13.17,Ruff0.16.9. Không suy execution surface,transport hay model runtime từ tên thư mục/lease/tài khoản. GitHub check run thật,PR disclosure ADR-0044,thread và authority ngoài snapshot: **KHÔNG ĐO ĐƯỢC** vì nhiệm vụ cấm mạng. CI ở đây là mô phỏng local. Không gặp thông báo “Codex home is inside a repository” trong log đo.

Hai lỗi giàn giáo reviewer đã sửa và đo lại: bộ chọn ID mutant đọc m2b sai kiểu số; bộ ghi JSON witness dùng trùng khóa mutant. Output trước khi sửa không được tính là răng/finding. Không có lỗi giàn giáo trong các log kết quả cuối. Không gọi mạng,không push,không sửa cay-kho; mọi mutant nằm trên scratch.

M1–M5 có bằng chứng hành vi đạt trong các phép đo; **M6 chưa đạt** vì ba survivor không tương đương, gom thành haiP1. Hình dạng **loi-do** và **bo-chon-ung-vien** tái xuất ở răng test; chưa thấy **nguon-goc-cau** tái xuất. Đây kích hoạt điều kiện M-4/Q8 cho quyết định của chủ kho; review này không cấp quyền thi công thêm hay land. Verdict **changes_requested**.

Nhật ký trên giữ nguyên các trạng thái “đang chờ” ở thời điểm ghi; các bảng đầu,hai finding và kết luận cuối là trạng thái sau cùng.
'''
p.write_text(intro+closure+old_closure+findings+'## NHẬT KÝ ĐO TĂNG DẦN\n\n- Khởi tạo VERDICT.md với verdict:dang_lam trước khi chạy kiểm tra. Đã nối bằng chứng sau từng hướng.\n\n'+journal+tail)

# Readback không ghi vào repository được review.
checks={}
for name in ['ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py','ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md']:
    raw=(ROOT/name).read_bytes()
    assert raw==subprocess.check_output(['git','-C',str(ROOT),'show',SHA+':'+name])
    checks[name]=hashlib.sha256(raw).hexdigest()
assert subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()==SHA
assert not subprocess.check_output(['git','-C',str(ROOT),'status','--short'],text=True)
assert p.read_text().splitlines()[:3]==['verdict: changes_requested','reviewed_sha: '+SHA,'Kết quả: 0 P0, 2 P1, 0 P2, 0 P3.']
assert len(re.findall(r'^### [a-z0-9-]+ \[P1\]',p.read_text(),re.M))==2
checks['status']='clean'
checks['reviewed_sha']=SHA
(E/'final-readback.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(checks,ensure_ascii=False))
