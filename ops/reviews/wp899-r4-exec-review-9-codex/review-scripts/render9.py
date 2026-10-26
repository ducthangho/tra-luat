import collections, hashlib, json, pathlib, re
R=pathlib.Path(__file__).resolve().parent
def read(name): return json.loads((R/name).read_text())
def table(head,rows):
 return '\n'.join(['| '+' | '.join(head)+' |','|'+'|'.join('---' for _ in head)+'|']+['| '+' | '.join(str(x).replace('|','\\|').replace('\n',' ') for x in row)+' |' for row in rows])
a=read('audit9-results.json');sample=read('closed8-results.json');snap=read('snapshot-start.json')
full=(R/'full-closed-command9.json').exists();suite=(R/'suite.json').exists();complete=full and suite
if full:
 cmd=read('full-closed-command9.json');assert cmd['rc']==0
 raw=(R/'full-closed.raw.stdout.txt').read_text();records=re.findall(r'\[KQ\] (\S+) ([0-9a-f]{16}) (GIET|SONG|TIN_DUNG_GIA)',raw)
 wanted={x['id']:x['sha256'][:16] for x in a['mutants']};actual={m:(h,rank) for m,h,rank in records}
 assert len(records)==len(actual)==1011 and set(actual)==set(wanted)
 assert all(actual[m][0]==wanted[m] for m in wanted)
 eq=set(a['equivalence']);bad=[m for m,(_,rank) in actual.items() if rank!=('SONG' if m in eq else 'GIET')]
 assert not bad and 'TONG DONG: DAT' in raw
 ranks=collections.Counter(v[1] for v in actual.values());n=1011
 (R/'full-validation9.json').write_text(json.dumps({'records':len(records),'unique_ids':len(actual),'all_source_hashes_match':True,'ranks':dict(ranks),'bad':bad,'official_command':cmd},indent=2))
else:
 n=len(sample);ranks=collections.Counter(x['rank'] for x in sample)
state='' if complete else '\n**Trạng thái: pending — đang hoàn tất phép đo tập đóng / suite.**\n'
body=f'''verdict: changes_requested
reviewed_sha: d2cca1580ed23dbbc532fb21481d0fac1e6ad8ac
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: d2cca1580ed23dbbc532fb21481d0fac1e6ad8ac
reviewed_tree: ebd72d2b76b881acc341fe1ae18b1abb0664b0bf
packet: wp899-r4-g4
generation: 4
spec_hash: be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45
review_class: sensitive
review_round: 9
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a17439-142b-7672-8469-99a80fbc0a66
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred
{state}
**V2 chưa đạt: P0=0, P1=0, P2=1 theo lớp sản phẩm.** F12 là lỗi thật trên HEAD: YAML không dựng được scalar làm reader ném ngoại lệ, rồi `main` thoát 1, trái A18. Bản vá ExceptHandler lượt 8 đã có răng; không dùng lỗi của mutant làm lỗi sản phẩm. Các nợ P3 có đề xuất quyết định riêng dưới đây.

## Authority, preflight và phạm vi

Đọc CONTEXT, protocol, CLAUDE, adapter cross-review, kế hoạch đa provider, toàn bộ spec r4 và các phần dẫn từ r2/r3; review độc lập từ assignment offline. Nguồn spec của lượt này là bản user chỉ định `.review-input/wp899-r4.md`, SHA-256 khớp `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`. Không tự xác nhận freshness của Issue/lease từ mạng. Áp nguyên authority đã giao: Q1–Q12, D01, D02; checkpoint nâng budget lên 10 (lượt này 9/10, offline cuối), trần khoảng 2050; g4 chỉ còn hai tệp. Không coi lease còn ghi 8, phần MOI bị rút, hoặc giới hạn gốc tin tại SHA là finding.

`snapshot-start.json` giữ từng command/rc: origin đúng `https://github.com/ducthangho/tra-luat.git`; detached HEAD đúng OID trên; cha `431681270298ffab8edcd316bdf26670157b4b4e`; immutable base là commit và ancestor (rc0). `core.abbrev=7`. Diff từ base chỉ có `ops/ci_provenance.py` +444 và `ops/ci_provenance_test.py` +1585 = **2029** dòng; diff cha→HEAD chỉ đổi test. `git diff --check`, diff/index và status đều rc0/rỗng. Mã sản phẩm SHA-256 `346a436b5593dbaae8d079103b6fce891981a6d0f1f23348ff4439270968b707`, không đổi so lượt 8.

Runtime đo thật: Linux x86_64, Python 3.13.17, PyYAML 6.0.3, Git 2.43.0, Ruff 0.15.15. `identity9.json` đọc đúng thread/cwd từ rollout: `originator=codex_exec`, `model_provider=openai`, CLI 0.164.0, model/effort như header. Đây chỉ là model/effort CLI công bố; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Sandbox thực tế workspace-write / network=false / approval=never; `.git` bị giữ chỉ đọc. `codex --version` rc0 nhưng stderr có cảnh báo không tạo được PATH aliases vì filesystem chỉ đọc; không coi đó là phép đo gọi model mới. Launcher rc, stdout thread.started, hash/size rollout sau khi process kết thúc và receipt vận chuyển phải do bên chạy hoàn tất (A13).

## BẢNG LỚP

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| F12 `loi-constructor-yaml-thoat-doc-wf` | **P2**, 1 lớp / 8 đầu vào | `ops/ci_provenance.py:159`–160 chỉ bắt YAMLError/RecursionError. SafeLoader còn ném ValueError, KeyError, IndexError, AttributeError khi dựng scalar sai; lỗi đi qua thu tới `main` rc1. | `python -B .review/run9.py product-yaml-expanded python -B .review/product_yaml9.py` rc0 của driver xác nhận **8 con rc1**, đối chứng con rc0/Gate passed. Git blob/commit thật, REST giả giữ state; từng command, SHA/blob, stdout/stderr ở `product-yaml9-results.json` và `yaml-fixture9.json`. | Vá **reader `doc_wf`**, vì đây là ranh giới biến workflow không đọc được thành None; không đổi main thành nuốt mọi lỗi. Bao phủ các lỗi dựng scalar đã đo ngay quanh safe_load, giữ fail-closed. Thêm bảng A18 dùng REST/log dựng từ workflow đối chứng hợp lệ; từng nhánh lỗi có mutant bỏ ngoại lệ tương ứng phải chết đúng ca. Rủi ro: bắt quá rộng che lỗi lập trình; fixture parse YAML hỏng trước reader tạo tín dụng giả. | khoảng **8–16** cả code/test; đo lại so trần trước thi công |
| D02 `uses-nhieu-dong` | P3, nợ kế thừa | `ops/ci_provenance.py:174` giữ dòng đầu uses nhiều dòng. | Assertion lịch sử `name_uses_whole_value` chạy trên HEAD; không có log runner thật mới. | **Giữ nợ theo quyết định chủ kho**, owner `ducthangho`; không vá trong packet này. Nếu mở lại, cần scope và fixture runner riêng; tránh thay luật tên run cùng lúc. | 0 |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` — biểu hiện D03 | P3, 2 mutant ngoài bảng | `ops/ci_provenance.py:167`,172: đổi kiểm không chứa biểu thức thành kiểm không bắt đầu bằng biểu thức; cả hai sống 52/52. HEAD đúng. | `membership9-results.json`: tên `Build ${{{{x}}}}` ở alias job / name bước bị HEAD chặn, mutant tương ứng cho ghép và marker passed. | Đề xuất **ghi nợ test ngoài tập đóng**, owner `ducthangho`, successor hoặc quyết định bổ sung hai hàng tên có biểu thức ở giữa vào ca c52_tap_dong của ops/ci_provenance_test.py, để hai mutant prefix đã đo đều chết đúng ca. Compare đã có toán tử In↔NotIn trong bảng; thay predicate bằng startswith là toán tử khác ngoài bảng cố định, không báo survivor của chính tập đóng hay lỗi sản phẩm. Rủi ro: nới lại F10 thành tập vô hạn; không đổi luật sản phẩm đang đúng. | 2–6 test nếu được giao |
| D04 `dem-buoc-xac-thuc-chua-rang-buoc` | P3, 1 mutant ngoài bảng | `ops/ci_provenance.py:297`: bỏ phép cộng của AugAssign (`so += 1`→`so = 1`), sống 52/52; hai bước run xác thực được báo 1 thay 2. | `augassign9-results.json`: HEAD/mutant cùng hai marker đúng, cùng ghép so_buoc=3, chỉ buoc_xac_thuc 2→1. | Đề xuất owner `ducthangho` quyết định chuẩn hóa miền đếm này trong spec rồi mở rộng c27 của ops/ci_provenance_test.py: hai bước xác thực / uses không được đếm phải giết mutant +=→=; hoặc bỏ trường phụ nếu không dùng. Rủi ro: nhầm số nhóm với số bước xác thực. Spec đóng băng định nghĩa so_buoc của ghép, chưa ràng buộc riêng miền buoc_xac_thuc≥2; không nâng thành vi phạm M12/P2 từ tên trường. | 3–8 test/spec ở successor |

Không có P0/P1 mới. D03/D04 là khuyến nghị có căn cứ cho ngoài tập đóng theo mục 7; không dùng chúng để yêu cầu sửa sản phẩm. Với lỗ kiểu nút chưa được toán tử bảng xử lý, chỉ báo P2 khi survivor đổi kết quả spec đã định nghĩa; AugAssign đo được survivor nhưng chưa đủ vế nghiệm thu đó. Không tuyên bố bảng toán tử bao trùm mọi thay đổi chương trình.

## Lỗi sản phẩm F12: bằng chứng và giới hạn

Tất cả input là workflow YAML thông thường bị lỗi scalar, **không phải nội dung tấn công**. Có `jobs/steps` hợp lệ, log checkout/REST steps hợp lệ; chỉ thay scalar `name:`. Reader Git thật đọc `wf.yml` tại đúng commit trong `.review/yaml-git`. Con gọi mã HEAD `main`, tiêm REST theo M1 và Git reader theo đúng root fixture; không dùng parser của fixture để dựng REST từ YAML lỗi. Đối chứng `name: "2026-02-30"` trả rc0, checkout/ghép/Gate passed. Những input dưới đây phải ra workflow không đọc được → ghép not_measured, không marker, không ném theo A18; thực tế đều in `NOT_MEASURED: 4` rồi traceback / rc1 / không sinh provenance.

'''
yamlrows=read('product-yaml9-results.json')['results'];body+=table(['scalar name','ngoại lệ thật','rc con'],[(read('yaml-fixture9.json')['cases'][x['case']]['workflow'].splitlines()[0],x['stderr'].splitlines()[-1],x['rc']) for x in yamlrows[1:]])
body+='''

Đây là lỗi xử lý dữ liệu không đọc được, không phải đường giả marker cần sửa nội dung tin cậy để tấn công. Giới hạn gốc tin của r4 không miễn nghĩa vụ A18. Hạng P2 vì lỗi hẹp, fail-closed bằng crash, không có bằng chứng thiếu/lệch bị đổi thành passed. Chưa đo mọi constructor/PyYAML version, native Windows hoặc workflow này được GitHub runner chấp nhận; không cần khẳng định ấy để đo hợp đồng reader “YAML hỏng, không ném”. Không gom tám input thành tám lớp.

Ngoài F12, không tìm được lỗi sản phẩm ở các phép thử khác: `product9-results.json` có **1000/1000** kịch bản mới seed899009, REST dựng độc lập rồi đảo thứ tự, tên key/alias Unicode và ký tự regex, tiền tố matrix, run/uses/skipped, env/defaults ba mức, shell, nguồn PATH trước bước, count/name/time/number/job lệch; **0 mismatch**. `product8-results.json` chạy lại 300/300 oracle lịch sử; `history8-results.json` có 169 assertion cases lượt 3–7 đạt và 2×34 quan trắc lượt 1/2 không ném. Quan trắc không được gọi là assertion suite. Các input cần nội dung nhạy cảm chỉ thuộc hướng mô tả, không được tự soạn.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| mục lượt 8 / SHA 431681270298ffab8edcd316bdf26670157b4b4e | kết quả trên HEAD | bằng chứng tự đo |
|---|---|---|
| F10/P2 ExceptHandler bỏ RecursionError | **ĐÃ VÁ THẬT biểu hiện cũ** | Chạy nguyên `gap8.py`: rc1 tại assertion cũ “all_green”, vì mutant nay chết rc3 đúng `DO:c52_tap_dong:`. Giữ kết quả này là bằng chứng đóng lỗi, không gọi driver cũ rc0. `gap8-all52.json`, `gap8-results.json`, `gap8.json`. |
| Hai toán tử bo_ngoai_le mới | **ĐÃ VÁ THẬT** | `patch9-results.json`: mỗi target baseline rc0; `doc_wf#7:bo_ngoai_le0` rc3 đúng c32 / ParserError; `bo_ngoai_le1` rc3 đúng c52 / RecursionError. |
| Phản chứng end-to-end gap_e2e8 | giữ hành vi sản phẩm đúng | Script nguyên rc0: HEAD not_measured / workflow không đọc được; mutant bỏ RecursionError ném đúng như trước. Test mới bắt được nó; sản phẩm không đổi. |
| D02 | GIỮ NỢ theo authority | Assertion lịch sử và quyết định đã giao. Không gọi giữ nợ là vá mã. |
| Ba survivor tương đương ngoài tập | GIỮ, không ép giết | `old-equivalences9-results.json`: đo lại 52/52 trên mỗi source. `[:1:2]=[:1]`; match/fullmatch tương đương trên dòng logic với regex đã neo; lstrip ở lần rstrip thứ hai chỉ thêm/bớt dòng LF rỗng bị lọc sau đó. Không dùng mẫu hữu hạn thay lập luận cấu trúc. |

Không đổi slug F10 để xóa lịch sử: D03 được giữ trong lớp F10, hạ tầng thước đóng không biến nó thành lớp mới. Biểu hiện ExceptHandler đã đóng; tìm được F12 sản phẩm là **lớp mới**, không phải bằng chứng bản vá test làm sản phẩm hồi quy. Không suy kết quả đóng một biểu hiện thành chứng minh mọi toán tử tưởng tượng đều đã được khóa.

## Bộ sinh, phân hạng và bảng kiểu nút AST

`audit9-results.json` tái dựng từng phép duyệt/chỉnh/unparse/compile, đối chiếu bằng cả ID và nguồn với `sinh_dot_bien_dong`: **1011** mutant có hiệu lực, **0** lỗi compile bị bỏ, **0** trùng ID; hai phép `return None` vốn không đổi nguồn được loại (`doc_wf#12`, `_gio#7`). **13 nhóm nguồn trùng** vẫn giữ đủ các ID. Thêm mã ngoài chín hàm không đổi dãy ID. Không coi dict đã khử trùng làm phép đếm độc lập.

`criteria8-results.json` đo lại trên HEAD: rc0, rc4/lỗi vô can, rc3 sai tên và đúng tên; sai tên không được GIET. Tiêm rc4 rồi rc3 vào `--tat-ca-ca`, runner tiếp tục sau rc4 và dừng ở rc3 đầu, không gọi ca sau. Tập đóng đòi `d.startswith('DO:'+c+':')`; không đổi lỗi import/setup thành credit. Catalogue có phép tìm substring trong `phan_hang`, nhưng producer `chay_ca` gắn tên ca cố định; chưa tìm được đường credit giả thực tế trong các phép đo này. A7 có baseline rc0 và hai mutant rc3 đúng c18/c19 trong receipt riêng, không lấy tổng suite làm thay thế.

Census **49 kiểu / 1531 nút**, kể cả hàm lồng và nút phụ trợ. Cột “nút có toán tử riêng” đếm `_toan_tu` sau khi bỏ docstring; toán tử Eq/In/And/Not… được sửa qua nút cha nên 0 ở chính nút phụ trợ không có nghĩa bị bỏ logic ấy. Bảng “không” không tự là finding. Mẫu mới `operators9` đo **144** toán tử bổ sung: **143 GIET**, **1 SONG tương đương** (`k.group(0)`→`k.group()` cùng group0 mặc định), 0 tín dụng giả. Có thêm hai probe membership và một AugAssign sống ở D03/D04. `gap9` bỏ đối số rstrip phân biệt được dữ liệu nhưng bị c48 giết đúng ca (rc3); assertion cũ của driver rc1 được giữ, không báo là survivor.

'''
descriptions={
 'BoolOp':'Có: and↔or, bỏ từng vế.', 'Compare':'Có: đổi toán tử, kể cả In/NotIn; D03 là thay predicate ngoài bảng.',
 'Constant':'Một phần: bool, int ±1, chuỗi khác rỗng; bỏ docstring; None/chuỗi rỗng không có phép riêng.',
 'UnaryOp':'Một phần: bỏ Not; USub chưa có phép riêng.', 'If':'Có: cố định True/False.', 'IfExp':'Có: lấy từng nhánh.',
 'Return':'Có: tra_None; hai phép không đổi nguồn được loại có ghi sổ.', 'ExceptHandler':'Một phần: tuple bắt lỗi có bỏ từng lớp; hai ID mới chết đúng c32/c52. Catch ValueError đơn ở _gio không có phép riêng.',
 'Call':'Một phần: ≥2 đối số có bỏ từng đối số. Mới đo bỏ một đối số / keyword; group(0)→group() tương đương, các phép khác bị giết.',
 'Dict':'Không riêng; đã đo bỏ từng cặp key/value, bị giết.', 'Tuple':'Không riêng (ExceptHandler qua nút cha); mới đo bỏ từng phần tử tuple Load, bị giết.',
 'List':'Không riêng; mới đo bỏ từng phần tử list Load, bị giết.', 'For':'Không riêng; mới đo đảo iterable, bị giết.',
 'Continue':'Không riêng; đổi Continue→Pass bị giết.', 'AugAssign':'Không riêng; +=→= sống, nhưng chỉ đổi trường phụ chưa ràng buộc (D04).',
 'keyword':'Không riêng; bỏ key= của sorted bị giết.', 'comprehension':'Một phần: bỏ filter (4/16 có filter); iterable/target không có phép riêng.',
 'Attribute':'Không riêng; lượt 8 đã thử method variants. Lượt này không có survivor mới chứng minh lỗ kiểu này.',
 'Subscript':'Không riêng; lượt 8 đã thử chỉ số i±1. Chưa đo thêm miền chỉ số trong lượt này.',
 'Slice':'Không riêng; lượt 8 đã đo step/reverse/biên động. Giữ tương đương :1:2 bằng phép đo lại và lập luận.',
 'NamedExpr':'Không riêng; lượt 8 có probe binding h. Lượt này chưa có mutant mới đủ chứng minh lỗ.',
 'BinOp':'Không riêng; lượt 8 thử giữ từng vế. Mới đổi phép trừ set thành giao set, bị giết.',
 'Lambda':'Không riêng; drop keyword chứa lambda ở sorted bị giết; không suy đã phủ mọi lambda.',
}
rows=[]
for k in sorted(a['counts']):
 z=a['types'].get(k,{});desc=descriptions.get(k)
 if desc is None:
  if k in ('And','Or','Eq','NotEq','LtE','In','NotIn','Is','IsNot','Not'):desc='Qua BoolOp/Compare/UnaryOp cha; không có phép riêng trên nút phụ trợ.'
  elif k in ('Add','Sub','BitOr','USub'):desc='Không riêng; xét qua biểu thức cha; không tuyên bố bao phủ mọi phép số học.'
  elif k in ('Load','Store','arg','arguments'):desc='Nút context/chữ ký; không có toán tử riêng.'
  else:desc='Không riêng; nút con có thể có toán tử. Chưa đo survivor mới phân biệt được cho riêng kiểu này.'
 rows.append([k,a['counts'][k],z.get('with_operator',0),desc])
body+=table(['kiểu','số nút','nút có toán tử riêng','có / không / mutant đo được'],rows)
body+='''

## Tám chứng minh TUONG_DUONG

Giữ cả tám, không tìm được đầu vào phân biệt. Mỗi mutant được chạy đủ 52 ca trên HEAD trong mẫu hiện tại; thêm đối chứng riêng ở `equivalence8-results.json` chạy lại trong lượt này. Số ca/mẫu hữu hạn là đối chứng, lập luận dưới đây mới là lý do giữ.

'''
eqrows=[
 ['ghep_job#24:-1','GIỮ','Chỉ truy cập khi len(khop)=1 nên [0]=[-1]. 25 cặp 0/1/nhiều job, alias, Unicode.'],
 ['chan_buoc#103:bo_doi_so1','GIỮ',"Thiếu run: str(None) và '' đều không chứa GITHUB_ENV/PATH. 7 dạng bước trước; giá trị run có mặt giữ nguyên."],
 *[[f'tach_buoc#173:chuoi{k}','GIỮ','Hằng chỉ đứng trong len(), biến dạng hoa/thường giữ 13 ký tự. 5 cấu trúc log.'] for k in (2,3,4)],
 ['do_dau_duong#127:bo_ve0','GIỮ','goi rỗng ⇒ all([]) True nhưng comprehension vẫn rỗng, vòng marker không chạy. 351 cặp.'],
 *[[f'do_dau_duong#306:chuoi{k}','GIỮ',"Chỉ thêm đoạn LF rỗng cuối, dong_logic/strip/if d loại; phép so toàn khối trước đó không đổi. 351 cặp; hai ID cùng nguồn được giữ."] for k in (1,4)]]
body+=table(['mã','giữ / bác','lập luận và đối chứng'],eqrows)
body+=f'''

## Tập đóng đã đo độc lập

**{n}/1011 mã: {ranks['GIET']} GIET, {ranks['SONG']} SONG thuộc đúng TUONG_DUONG, {ranks['TIN_DUNG_GIA']} TIN_DUNG_GIA.** '''
if full:
 body+='''Đã tái lập trọn tập: **1003/1011 giết + 8 tương đương; 0 sống ngoài danh sách; 0 chứng minh tương đương sai; TONG DONG: DAT**, rc0. `full-validation9.json` kiểm 1011 record/ID duy nhất, nguồn hash khớp audit cho từng mã, không ID rời tập.

Lệnh `python -B .review/run9.py full-closed python -B .review/full9.py` gọi **runner gốc** `python -B ops/ci_provenance_test.py --dot-bien-dong 8`. Nó chỉ dùng lại **207** receipt do chính session này vừa đo, cùng SHA-256 đầy đủ của nguồn mutant; **804** mã còn lại được đo mới bằng runner gốc. `CIP_DONG_TIEP` chỉ trỏ `own-resume9.txt` tự sinh từ các receipt đó, không dùng hạng/log executor. `full-closed-command9.json`, `full-closed.raw.stdout.txt`, `full-closed.json` giữ command/rc/hash/output. Mẫu đầu có 150 mã phủ chín hàm + toàn bộ frontier, seed899008; không coi tên script closed8 là evidence lượt 8.
'''
else:
 body+=f'''Đã hoàn tất mẫu 150 mã phủ chín hàm + frontier; **{1011-n} mã còn lại KHÔNG ĐO ĐƯỢC tại mốc báo cáo pending này**. Full runner đang chạy; chưa gọi toàn tập passed.
'''
body+='''
Frontier lời dẫn nhắc “58” được kiểm bằng regex record trên **toàn** `dot-bien-dong-luot-dau.txt`, không đếm dòng (có record nối dòng): **1009 ID = 952 GIET + 30 SONG + 27 TIN_DUNG_GIA ⇒ 57 chưa giết thực có**. Đã đo đủ 57/57 trong lượt này: 49 GIET + 8 tương đương. Không tạo “mã thứ 58” không có trong hiện vật; phần ấy **KHÔNG ĐO ĐƯỢC**. HEAD thêm hai toán tử ExceptHandler nên tổng mới là1011, không nhầm con số1009 của bản cũ.

## ĐỐI CHIẾU F01–F11

| lớp | trạng thái trên HEAD | bằng chứng / giới hạn |
|---|---|---|
| F01 thieu-dinh-danh-van-passed | GIỮ ĐÓNG trong miền đo | c22, metadata thiếu/sai kiểu, tap_jobs/artifacts; không coi ghép passed là đủ Gate passed. |
| F02 nhac-ten-script-thanh-thuc-thi | GIỮ ĐÓNG các biểu hiện giao | c23/c25–27/c35/c40–43; assertion lịch sử, oracle mới, composite/nested/lệch bước. Giữ giới hạn gốc tin. |
| F03 phan-trang-dem-thay-vi-chung-minh-du | GIỮ ĐÓNG | c20 thiếu/lặp/total đổi cho jobs/artifacts; không suy len=total là đủ nếu ID trùng. |
| F04 rest-gia-khong-neo-run | GIỮ ĐÓNG | c20 wrong run/attempt/log URL bị REST stateful từ chối; không có mạng. |
| F05 duong-loi-bo-dong-dem-bat-buoc | GIỮ ĐÓNG | c01/c18/c19/c22; A7 baseline/mutant riêng. F12 vẫn in đúng dòng đếm, nên không đổi slug F05 cho crash mới. |
| F06 redirect-loi-thoat-ngoai-bo-boc | GIỮ ĐÓNG | c24 mock redirect/network/header; không đo endpoint thật. |
| F07 a10-doi-sha-khi-checkout-skipped | GIỮ ĐÓNG theo authority | Replay13+1/22+1; chuan-bi vẫn không có SHA, không lấy head REST bù. |
| F08 nguon-workflow-git-khong-duoc-kiem-thu | GIỮ ĐÓNG phép reader Git cũ | c34 Git/blob thật, thiếu path/nonUTF8; F12 là lỗi dựng scalar sau reader, đã tách lớp. |
| F09 thoi-diem-khong-hop-le-van-ghep | GIỮ ĐÓNG trong miền đo | c38/c51, lịch/format/biên; oracle mới đảo steps và cửa sổ. |
| F10 fixture-dinh-danh-buoc-chi-giu-dang-khop | **ĐÃ VÁ THẬT biểu hiện ExceptHandler**; cả lớp còn D03/P3 ngoài thước đóng | Target bo_ngoai_le0/1 có baseline/kill đúng; audit bộ sinh, mẫu/frontier và phép đo tập đóng ở trên. Các survivor ngoài bảng xử lý D03/D04; không khẳng định mọi toán tử có thể nghĩ ra đã được khóa. |
| F11 chan-path-chua-co-phan-chung | GIỮ ĐÓNG | c42/c47–51 và oracle mới: PATH trước/khác job/sau, không đổi PATH thành ENV để đo. |

U theo P0–P2 lượt 8={F10}; biểu hiện chặn ExceptHandler được vá thật, nhưng còn D03/P3 cùng lớp nên F=∅ theo nghĩa đóng TOÀN lớp: **0/1 lớp đóng hết**, không đếm hạ hạng/đổi thước thành vá. F12 mới báo riêng, không vào tử số đóng lớp cũ; D02 giữ nợ không được đếm là vá. Checkpoint thay thước đã được giao không tự cấp lượt offline tiếp theo hoặc approval.

## A1–A27

| tiêu chí | kết quả và phạm vi |
|---|---|
| A1 | passed c01: help đủ cờ, sai đối số rc2 và dòng đếm. |
| A2 | passed c02: attempt lệch failed/rc12, đối chứng đúng passed. |
| A3 | passed c03–09: Linux/Windows fixture, thiếu/nhiều/lệch SHA, PR parents; không là Windows/PR LIVE execution. |
| A4 | passed c10–15 và probes M4/M12: runner0/skipped, regex đúng bước, MOI import một nguồn. |
| A5 | passed c16: Workflow definition luôn not_measured, path chỉ là lời khai REST. |
| A6 | passed c17: fault injection giữ đích cũ/không để nửa output. |
| A7 | passed c18/c19; criteria8-results.json có hai receipt baseline rc0 / mutant rc3 đúng ca, dòng đếm và lỗi REST403/rc3. |
| A8 | Kết quả suite và tập đóng ghi bằng command/rc thật ở phần dưới; không dùng chúng miễn A18/F12. |
| A9 | **failed, giới hạn đã khai g4**: registry rc1,25/24, test sống chưa đăng ký. Full --chay not_run; không sửa tệp ngoài write set. |
| A10 | Replay offline passed, byte-identical cả hai. LIVE/freshness/retention REST KHÔNG ĐO ĐƯỢC. |
| A11 | passed local:2 tệp/2029 dòng theo trần checkpoint; diff-check0, Ruff0, doctrine10/0, ADR53/53. |
| A12 | not_run/not_measured: không đẩy/ls-remote/CI/connector; đây là lượt offline. |
| A13 | partial/not_measured: đã đọc identity đúng thread/cwd/model/effort CLI; receipt launcher/stdout/hash rollout sau kết thúc do bên vận chuyển hoàn tất. Không tự tạo approval. |
| A14 | passed c25: metadata mang màu không thành kịch bản. |
| A15 | passed c26: tập con khối không thành xác thực. |
| A16 | passed c27/c52 và đối chứng: toàn khối, nguyên văn, lời gọi tối giản. |
| A17 | passed c28–31/c46/c48–52, D01 env null≠vắng, nguồn chặn; giữ giới hạn uses trước bước. |
| A18 | **failed — F12/P2**: tám malformed scalar, bốn lớp ngoại lệ, main rc1. Nhánh YAMLError/RecursionError và reader Git cũ đạt không thay thế miền lỗi này. |
| A19 | passed c33, lịch sử/oracle: chặn theo đúng job, alias/job khác không làm bẩn nhau. |
| A20 | passed c36: số nhóm/REST/YAML, không zip cắt ngắn. |
| A21 | passed c37/c48–52: tên explicit/implicit và mismatch. D03 là mutant ngoài bảng, HEAD vẫn đúng tên có biểu thức giữa chuỗi. |
| A22 | passed c38/c51, lịch/giờ/format/cửa sổ; dữ liệu A10 thật được replay offline. |
| A23 | passed c39/c47–52: key/name/prefix/duy nhất; không đánh giá biểu thức matrix. |
| A24 | passed c40/c35/nested lịch sử; không ép giết biến đổi tương đương. |
| A25 | passed c41/composite lịch sử; composite thật trên runner KHÔNG ĐO ĐƯỢC. |
| A26 | passed c42/c47–51, ENV/PATH trước/khác job/sau/skipped; oracle mới có nguồn PATH trước. |
| A27 | passed c43: khối bước khác không thành marker. |

## Replay A10

`python -B .review/run9.py replay python -B .review/replay8.py` rc0; **37/37** log khớp SHA256SUMS. Thu lại bằng mã HEAD, Git objects cục bộ và REST stateful từ hiện vật đã tải. **Hai provenance khớp từng byte** bản đo trên52e9573; **0 khác biệt** cần giải thích.

| run / attempt | Run | Checkout / ghép | Gate / marker | SHA-256 provenance |
|---|---|---|---|---|
|39342960764 /1|passed|13 checkout passed b27fe85… +1 chuan-bi not_measured; ghép13/14|14 Gate not_measured,0 failed,0 marker MOI|5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0|
|40074551995 /1|passed|22 checkout passed dc65714… +1 chuan-bi not_measured; ghép22/23|23 Gate not_measured,0 failed;8 nhanh_don_duoc not_measured/che_do_khong_xac_dinh; gate-nhanh-gop không marker|24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b|

Labels đều ubuntu-latest, Workflow definition vẫn not_measured. Không dùng replay thay LIVE hoặc CI provenance mới, không suy tên job thành thực thi Windows. `replay8-results.json` chứa hash từng log, từng request REST giả và trạng thái.

## Command, rc, trạng thái và bằng chứng dương

Các lệnh Python đi qua `.review/run9.py <nhãn> <command…>`; wrapper giữ rc con thật, stdout/stderr, SHA-256 và thời lượng tại `<nhãn>.json`. PYTHONDONTWRITEBYTECODE=1, python -B; TMPDIR/TMP/TEMP ở `.review/tmp`; Ruff no-cache. Rc0 của driver không thay trạng thái con: đặc biệt product-yaml driver rc0 xác nhận tám con rc1, không phải sản phẩm passed.

'''
cmdrows=[]
for label,command,evidence in [
 ('suite','python -B ops/ci_provenance_test.py','CA/DOT BIEN/TU KIEM/TONG'),
 ('full-closed','python -B .review/full9.py','runner gốc --dot-bien-dong8; full-validation9.json'),
 ('closed-sample','python -B .review/closed8.py','207 mã,199 GIET+8 tương đương; đủ frontier57'),
 ('patch','python -B .review/patch9.py','2 target baseline0 / mutant3 đúng ca'),
 ('audit','python -B .review/audit9.py','1011 nguồn /0 compile lỗi /0 trùng ID'),
 ('operators','python -B .review/operators9.py','144:143 GIET+1 tương đương'),
 ('equivalences','python -B .review/equivalence8.py','8 chứng minh giữ; đối chứng25/7/5/351'),
 ('old-equivalences','python -B .review/old_equivalences9.py','3 source ×52/52'),
 ('history','python -B .review/history8.py','169 assertion đạt;2×34 quan trắc'),
 ('product-new-oracle','python -B .review/product9.py','1000/1000 oracle mới khớp'),
 ('product-yaml-expanded','python -B .review/product_yaml9.py','1 con0 đối chứng;8 con1 lỗi sản phẩm'),
 ('replay','python -B .review/replay8.py','37 hash đúng;2 provenance byte-identical'),
 ('criteria','python -B .review/criteria8.py','A7 dương/âm; phân hạng đúng tên; dừng đúngrc3'),
 ('ruff','python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py','All checks passed'),
 ('doctrine','python -B .claude/dev/packet_loop.py doctrine-scan --root .','10 tệp /0 chép doctrine'),
 ('adr','python -B .claude/dev/packet_loop.py adr-song --root .','53 ADR/53 dòng; exemption0016'),
 ('registry','python -B .claude/dev/ci_dang_ky_test.py','ĐỎ: test sống chưa đăng ký;25/24; Ruff contract3/3')]:
 p=R/(label+'.json')
 if p.exists():
  z=read(p.name);status='failed, giới hạn đã khai' if label=='registry' else 'phép đo passed; sản phẩm failed' if label=='product-yaml-expanded' else 'passed' if z['rc']==0 else 'failed'
  if label=='suite':evidence=(R/'suite.stdout.txt').read_text().strip().replace('\n','; ')
  cmdrows.append([command,z['rc'],status,evidence+'; '+label+'.json'])
 else:cmdrows.append([command,'chưa kết thúc','KHÔNG ĐO ĐƯỢC tại mốc pending',evidence])
body+=table(['command','rc thật','trạng thái','positive evidence / receipt'],cmdrows)
body+='''

`gap8` và `gap9` driver rc1 là assertion giả thuyết survivor bị bác, đã giải thích riêng, không lẫn với lỗi gate hoặc pass. Không có required check skipped nào bị đọc thành passed. Bare Ruff trên scripts/tl.py, full release/selftest toàn kho, network/LIVE, CI mới, connector, push/merge/land/deploy **not_run**; native Windows, GraphQL, action đổi môi trường và freshness remote **not_measured**. Các giới hạn này không được tự đổi thành waiver hoặc gate xanh.

## Read-only, evidence và bàn giao

'''
if (R/'snapshot-end.json').exists():
 end=read('snapshot-end.json');delta=[p for p in set(snap['files'])|set(end['files']) if snap['files'].get(p)!=end['files'].get(p)]
 assert not delta
 (R/'snapshot-comparison9.json').write_text(json.dumps({'files_checked':len(snap['files']),'delta':delta,'start_head_tree':snap['commands'][2]['stdout'],'end_head_tree':end['commands'][2]['stdout']},indent=2))
 body+=f'''`snapshot-start.json` / `snapshot-end.json` / `snapshot-comparison9.json` đối chiếu HEAD/tree, diff/index/status và **{len(snap['files'])} tệp** tracked/untracked/ignored ngoài `.review/` bằng path/size/SHA-256: **không có delta quan sát được**; status cuối rc0/rỗng. Chỉ chứng minh hai mốc và checkout được giao, không chứng minh chưa từng ghi rồi hoàn nguyên. Repo nguồn ngoài checkout không thuộc quan sát. `.review/` là ngoại lệ scratch user cấp; không sửa tệp sản phẩm hay nhánh Executor.
'''
else: body+='Snapshot cuối chưa lấy khi các writer phép đo còn đang chạy; chưa tuyên bố kết quả read-only cuối.\n'
body+='''
Tất cả hiện vật tạo bởi reviewer ở `.review/`; manifest evidence cuối ghi path/size/SHA-256 sau khi writer phép đo kết thúc. Không gọi subagent, mạng, đăng GitHub, đẩy Git hay cấp quyền mới. Verdict này là **changes_requested vì F12/P2**; không tự tạo cross_approved, không tự sửa lỗi và không tự cấp lời gọi offline tiếp theo. Phần authority/transport A13 sau process kết thúc do người giữ hoàn tất; owner quyết định bước tiếp theo trong checkpoint/budget đã giao.
'''
(R/'VERDICT.md').write_text(body)
print('VERDICT',len(body.encode()),'bytes','complete',complete,'closed_measured',n)
