import pathlib,json,collections,hashlib,subprocess,os,re
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
def read(n):return json.loads((w/n).read_text())
def lines(n):return [json.loads(l) for l in (w/n).read_text().splitlines()]
def cases(x):return x.get('cases') or [json.loads(l) for l in x.get('stdout','').splitlines() if l.startswith('{')]
def grade(x):
 cs=cases(x)
 if any(y['rc']==3 for y in cs):return 'GIET'
 if x.get('rc')==0 and len(cs)==36 and all(y['rc']==0 for y in cs):return 'SONG'
 return 'TIN_DUNG_GIA' if len(cs)==36 and any(y['rc']==4 for y in cs) else 'HONG'
base=read('independent_final.json');extra=lines('order_url_results.jsonl');native=lines('semantic_native_full.jsonl');old=lines('old_rerun.jsonl');ex=lines('executor_rerun.jsonl');nk=lines('ast_native_kills.jsonl');six=lines('scanner_native_results.jsonl')
assert (len(base),len(extra),len(native),len(old),len(ex),len(nk),len(six))==(102,5,21,381,368,362,7)
assert all(x['killed'] for x in nk)
reason_extra=lines('reason_complete_results.jsonl')
assert len(reason_extra)==20 and all(grade(x)=='GIET' for x in reason_extra)
allm=base+extra+reason_extra
for x in allm:x['grade']=grade(x)
assert all(x['grade'] in ('GIET','SONG') for x in allm)
equiv=set(read('equivalence.json')['identity_equivalent'])|{'ref_no_boundary'}
live=[x for x in allm if x['grade']=='SONG' and x['id'] not in equiv]
for x in live:
 n=next(y for y in native+extra if y['id']==x['id']);assert grade(n)=='SONG',x['id']
assert sum(x['id'] in equiv and x['grade']=='SONG' for x in allm)==9
(w/'all_independent_results.json').write_text(json.dumps(allm,ensure_ascii=False,indent=2))
diag={'skip_v3_partial','waiver_order_os_sha','waiver_order_author_url','waiver_order_line_author','waiver_order_os_date'}
p2=[x['id'] for x in live if x['id'] not in diag];p3=[x['id'] for x in live if x['id'] in diag]
assert len(p2)==20 and len(p3)==5,(p2,p3)
assert all(int((w/(n+'.rc')).read_text())==0 for n in ['suite','suite312','ruff','registration','prior','simplifications','corpus','consumer_matrix','independent_contrasts','real_waiver_matrix','cli_acceptance','dotpath','equivalence'])
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip();tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=r,text=True).strip();assert sha=='c2d606bb6fc230c288200b8f1dd79715462c172b';assert tree=='9b78e9e0b1e1d445e19747e65ab4f65ea4016511'
files={}
for root,dirs,names in os.walk(r):
 if pathlib.Path(root)==r:dirs[:]=[d for d in dirs if d!='.git']
 for name in names:
  p=pathlib.Path(root)/name;files[str(p.relative_to(r))]=('link:'+os.readlink(p)) if p.is_symlink() else hashlib.sha256(p.read_bytes()).hexdigest()
assert files==read('snapshot_before.json'),'snapshot changed'
(w/'snapshot_after.json').write_text(json.dumps(files,sort_keys=True))
cmds=[['git','status','--porcelain=v1','--untracked-files=all','--ignored=matching'],['git','diff','--check','0f9aa2a','HEAD'],['git','diff','--cached','--binary'],['git','diff','--numstat','0f9aa2a...HEAD']];post=[]
for c in cmds:
 z=subprocess.run(c,cwd=r,capture_output=True,text=True);assert z.returncode==0;post.append(dict(command=c,rc=z.returncode,stdout=z.stdout,stderr=z.stderr))
(w/'postflight.json').write_text(json.dumps(post,indent=2))
old_non=[x for x in old if 'GIET ' not in x.get('stdout','')];ex_non=[x for x in ex if 'GIET ' not in x.get('stdout','')]
assert len(old_non)==51 and len(ex_non)==6
assert all('HONG ' in x['stdout'] for x in ex_non)
summary={'independent_counts':dict(collections.Counter(x['grade'] for x in allm)),'equivalent':sorted(equiv),'p2_survivors':p2,'p3_survivors':p3,'old_ast':{'total':381,'no_valid_kill':len(old_non),'clean':sum(not x.get('stdout') for x in old_non),'incidental':sum('HONG ' in x.get('stdout','') for x in old_non)},'current_ast':{'total':368,'valid_kills_native':362,'incidental':6},'snapshot_files':len(files)}
(w/'measurement_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
v=read('VERDICT.json')
v['findings']=[
 {'id':'L01','class_slug':'test-thieu-chot','severity':'P2','vi_tri':'ops/gate_output_doi_chieu_test.py:437; :445; :545; :712',
  'van_de':'Bộ ca còn để 20 đột biến làm nhận sai, chặn oan hoặc ném ngoại lệ qua đủ 36/36 ca; lớp test-thieu-chot chưa đóng.',
  'bang_chung':"REVIEW_NO_CACHE=1 python3 -B ../work/run_scan.py ../work/semantic_survivors.jsonl ../work/semantic_native_full.jsonl native; cùng lệnh với order_url_mutants.jsonl/order_url_results.jsonl: rc=0, các ID P2 trong measurement_summary.json đều 36 ca rc=0. python3 -B ../work/independent_contrasts.py, consumer_matrix.py, real_waiver_matrix.py: rc=0; bỏ yêu cầu URL làm hồ sơ landed owner_waived thiếu URL từ hai vi phạm thành []; nới fullmatch dòng miễn hoặc grammar tệp/token nhận sai; đổi is True thành == True và bỏ dấu phân cách chặn oan; bỏ nhánh URL=0 khác làm kiem_ho_so ném TypeError. Các đối chứng trên HEAD xử lý đúng.",
  'de_xuat':'Tại a201/a202/a209/a215 và ca trích tệp, dựng một ma trận nghĩa từ hợp đồng đóng băng: so đủ tập TOKEN/PHI_LOI_KHAI, giữ chữ số khi chuẩn hoá, duyệt con của metadata, grammar tên tệp/dòng miễn, từng dấu phân cách, True so với 1 ở ba dạng landed, 0/1/2 URL và head None/chuỗi rỗng/SHA. Đo các biến thể từ fixture thật qua helper và kiem_ho_so, giữ đối chứng hợp lệ; thêm các toán tử trong all_independent_results.json và đòi chết đúng chốt. Dùng SafeLoader sản phẩm, phân riêng tương đương/lỗi vô can. Nguy cơ cần giữ: không siết grammar sản phẩm để làm ca xanh, không để lỗi setup hoặc một chốt khác cấp tín dụng cho chốt đang đo.'},
 {'id':'L02','class_slug':'test-thieu-chot','severity':'P3','vi_tri':'ops/gate_output_doi_chieu_test.py:167; :545; :590',
  'van_de':'Năm đột biến đổi chẩn đoán/thứ tự điều kiện miễn còn sống, và A2-10 chưa chạy fixture CLI thứ sáu T-khong-prov.',
  'bang_chung':'Cùng quét native của L01: skip_v3_partial và bốn waiver_order_* đều 36/36 ca rc=0. independent_contrasts.py: dong_la → co_job_skipped. real_waiver_matrix.py: html_url → tac_gia, tac_gia → dong_mien, han → os, os → sha khi hai điều kiện cùng sai. cli_acceptance.py rc=0: a210_rc 0 real_fixtures 5 sixth_called False sixth_direct_rc 3. Trạng thái từ chối không đổi trong năm biến thể chẩn đoán.',
  'de_xuat':'Ở a103 thêm hậu tố thừa riêng cho skipped v3; ở a209 dùng bảng lỗi đồng thời của các cặp điều kiện độc lập, so lý do đầu theo thứ tự đóng băng, kèm từng lỗi đơn và đối chứng sạch; ở a210 chạy đủ sáu fixture, gồm T-khong-prov. Thêm đột biến fullmatch v3 và hoán vị các cặp trên. Tránh phụ thuộc thứ tự tệp hoặc đổi thứ tự luật sản phẩm cho vừa oracle; phân rõ kiểm tên lý do với kiểm trạng thái.'},
 {'id':'L03','class_slug':'mo-ta-duong-dan-lech-hop-dong','severity':'P3','vi_tri':'ops/gate_output_doi_chieu.py:224',
  'van_de':'Docstring _tep_trong khai cấm thành phần dấu chấm, nhưng PurePosixPath chuẩn hoá dấu chấm và ./tệp vẫn được nhận theo đặc tả đợt A.',
  'bang_chung':'TMPDIR=../work/tmp python3 -B ../work/probes.py dotpath rc=0: cả tên tệp thật và ./danh-gia-gate-output-44669622916.txt đều kiem_ho_so=[]; dotpath_probes.json. Đã rà toàn bộ docstring và mô tả ràng buộc của module; biểu hiện lệch đo được là câu ở dòng 224.',
  'de_xuat':'Sửa mô tả tại _tep_trong để ghi đúng cấm tuyệt đối, .. và symlink; giữ quy tắc đợt A. Đối chứng đóng: ./tệp vẫn hợp lệ, ../ và symlink vẫn bị chặn, docstring không còn khai cấm dấu chấm. Nguy cơ: sửa mã để cấm ./ theo docstring cũ sẽ tự siết đầu vào ngoài đặc tả; không mang luật đường dẫn D2b của đợt C sang A.'}
]
history={
 'yaml-ngoai-schema-bi-chan':('lượt 1 @1719d6efb61433d92bbfba38f0a4add20a97be2b','Lọc kiểu/schema trước khi đọc trường.','probes.py prior: cả năm YAML ngoài schema giữ passed; m54 chết đúng a116.'),
 'k2-mat-loi-doc':('lượt 1 @1719d6efb61433d92bbfba38f0a4add20a97be2b; lượt 2 @6f7ccf10f2441d0c97b779cfa77ff2839b56fc47','Giữ lý do K2 và truyền lỗi đọc/duyệt về biên kiem_tep.','prior: YAML/UTF-8/symlink/PermissionError chặn đúng; kiểm 0/1/2 provenance; a116/a117 và các đột biến m55/m56/m59/m70 đạt.'),
 'cli-vong-yaml-traceback':('lượt 1 @1719d6efb61433d92bbfba38f0a4add20a97be2b; lượt 3 @e323bd4dfb4fe422016c4fd010fa964b6cb748b0','Phát hiện vòng và đặt đọc/kiểm filesystem trong biên lỗi CLI.','prior: cycle và hai đường stat quá dài rc=2 không traceback; alias chia sẻ vẫn duyệt hai đường; a214/m57/m58 và a210/m65 đạt.')}
for row in v['prior_class_status']:
 if row['slug']=='test-thieu-chot':
  row.update(status='VA_MOT_PHAN',evidence='20 đột biến đại diện các biểu hiện F04/G02/H01/J01/J02/K01/K02 trong audit_mutants.jsonl đều GIET đúng ca; bộ đối chứng mới 127 mutant còn 25 không tương đương SỐNG 36/36, gồm 20 biểu hiện L01 và 5 L02. A2-10 còn thiếu một fixture CLI. Lớp xuất hiện cả sáu lượt.',chua_do_duoc='')
 else:row.update(status='DA_VA_THAT',evidence=history[row['slug']][2]+'; probes.py prior rc=0; suite 36/36 và audit từng ca trên exact HEAD.',chua_do_duoc='')
v['class_table']=[]
for slug,(source,fix,closing) in history.items():
 old_ids=next(x['finding_cu'] for x in v['bang_noi_slug'] if x['slug']==slug)
 v['class_table'].append(dict(slug=slug,finding_ids=[],manifestations=[', '.join(old_ids)+': '+closing],highest_open_severity=None,nguon=source,common_fix=fix,closing_check=closing))
v['class_table'] += [dict(slug='test-thieu-chot',finding_ids=['L01','L02'],manifestations=[f'{x}: SỐNG 36/36 trên thước native; đối chứng phân biệt được' for x in p2+p3]+['A2-10: a210 chỉ chạy 5/6 fixture thật; T-khong-prov chưa nằm trong ca CLI'],highest_open_severity='P2',nguon='F04 lượt 1 @1719d6efb61433d92bbfba38f0a4add20a97be2b; G02 lượt 2 @6f7ccf10f2441d0c97b779cfa77ff2839b56fc47; H01 lượt 3 @e323bd4dfb4fe422016c4fd010fa964b6cb748b0; J01/J02 lượt 4 @b533028656dc2c4ac8de8751a9730f2d8b60d116; K01/K02 lượt 5 @028f8b3681edf41386ce6d89858505993b4ac82c; L01/L02 lượt 6 @'+sha,common_fix='Ma trận hợp đồng độc lập bao phủ tập giá trị, grammar, kiểu, đường đi và ưu tiên lỗi; đột biến theo nghĩa, qua đúng consumer, với dương/âm và phân hạng lỗi vô can/tương đương.',closing_check='Tất cả biểu hiện cũ giữ ca đích đỏ khi gỡ chốt; 25 mutant không tương đương hiện sống phải bị giết đúng ca và đúng tính chất, cùng đối chứng không chặn oan; A2-10 đủ sáu fixture. Quét lại toàn bộ miền toán tử đã công bố, native loader, rồi kiểm corpus/gate/trần trên SHA mới.'),dict(slug='mo-ta-duong-dan-lech-hop-dong',finding_ids=['L03'],manifestations=['_tep_trong docstring cấm . nhưng ./tệp được nhận'],highest_open_severity='P3',nguon='lượt 6 @'+sha,common_fix='Đồng bộ mô tả helper với đặc tả A và ngữ nghĩa PurePosixPath đã đo.',closing_check='probes.py dotpath giữ ./tệp đạt, ca đường dẫn ../ và symlink đạt chốt, câu mô tả hết lệch.')]
v['da_do_khop']=[
 'Preflight passed: repo ducthangho/tra-luat, checkout detached sạch; reviewed_sha '+sha+'; tree '+tree+'; baseline 0f9aa2a2cc697129e1f5be72feddf60986286865.',
 'Spec local và blob refs/remotes/origin/claude/spec-1236-r9 @176feba3a09a4e86c6d8b06487f3e4224571be51 cùng sha256 '+v['spec_sha256']+'; revision 9/generation 1; lease tới 2026-11-22T15:35:00Z; write_set_hash e348a0aec274cc000368e7b728a9a70423434e000ace619fbc059383907fb2f5 khớp.',
 'passed: python3 -B ops/gate_output_doi_chieu_test.py rc=0: CA 36/36 dat; DOT BIEN 124/124 bi giet dung ly do; TU KIEM PHAN HANG DAT (2); TONG DAT. Python 3.12 cũng cùng kết quả rc=0, stdout cả hai khớp MOI.',
 'passed: audit_mutants.py rc=0, 124/124 đúng TinHieuChotCa ở ca đích; một số chỉ kiểm chẩn đoán (m6→KeyError; m22/m23/m79 còn K2 symlink; m80→FileNotFoundError; m96–m100 kiểm tên lỗi kiểu). Không nâng chúng thành bằng chứng lật trạng thái cổng.',
 'passed: python3 -B -m ruff check --no-cache --select F trên đúng 3 tệp rc=0 (Ruff 0.15.15); python3 -B .claude/dev/ci_dang_ky_test.py rc=0:31/31, Ruff CI contract3/3,1226/1226 phản chứng.',
 'passed: probes.py corpus trên immutable base 0f9aa2a rc=0: 66=47 passed/10 failed/9 not_measured;170=25 cutover/56 đỏ/39 đạt/50 không lời khai;94 landed,0 lệch;BO_SINH khớp50script=20/28/2.',
 'passed: consumer_matrix.py rc=0: đối chứng dương cùng 21 biến thể, mọi lệch run/attempt/head/schema/event/path/cờ/job/log/thiếu provenance đều bị chặn trên HEAD; không tìm thấy lời khai dương lọt ngoài giới hạn đã khai.',
 'passed: bốn rút gọn so 89fb99b qua probes.py simplifications rc=0,27 đối chứng khớp; K5 tương đương đại số; walk không theo symlink; glob vắng/tệp/link; body JSON falsy/valid giữ kết quả.',
 'Quét executor đo lại:89fb99b sinh381,51 không bị giết hợp lệ ('+str(summary['old_ast']['clean'])+' sống sạch/'+str(summary['old_ast']['incidental'])+' lỗi vô can);HEAD sinh368,362 giết/6 lỗi vô can. 362 giết được xác nhận bằng ca đích native không patch/cache YAML; sáu bản còn lại chạy đủ36ca bằng SafeLoader có memo/deepcopy (không đổi sang C loader). M124 giết k339 ở a217.',
 'Bộ quét C loader không giữ ngữ nghĩa: yaml_parity.py rc=0 trên bản sao provenance thật, tab sau colon/tab cuối dòng SafeLoader→ScannerError nhưng CSafeLoader nhận; escape Unicode cũng đổi kết quả/lớp ngoại lệ. chay.py không ghi child rc và không có baseline tự kiểm; chay_ca.py chỉ nhìn rc3, dừng ở ca đầu. Không coi bảng này tự chứng minh đóng lớp.',
 'failed (nghiệm thu lớp):127 mutant độc lập=93 GIET,34 SỐNG;9 tương đương trong miền đầu vào,25 có đối chứng làm khác hành vi. Cả25 chạy đủ36ca không patch hoặc cache YAML. Bộ102 ban đầu dùng SafeLoader có memo/deepcopy để tăng tốc; hai lỗi riêng của script đo (ID trùng/ngoặc regex) đã loại và chạy lại, không lấy tín dụng từ output đó.',
 'K1–K8, BO_SINH/CHECK_BAT_BUOC_TEN, loi_khai/token/tep_danh_gia/la_landed/kiem_mien/kiem_ho_so/CLI đã đối chiếu toàn bộ với Module mới. Sai lệch còn mở:độ phủ nghiệm thu và docstring L03. L8/D2b thuộc B/C, không nằm trong diff A.',
 'passed:git diff --numstat 0f9aa2a...HEAD=3tệp,+1324/-0≤1400;git diff --check 0f9aa2a HEAD rc=0; snapshot '+str(len(files))+' tệp đầu/cuối (kể ignored .codex) khớp,HEAD/tree/index diff không đổi; không đo lịch sử ghi rồi hoàn nguyên hoặc repo nguồn ngoài checkout.',
 'Môi trường:Linux;Python3.13.18/PyYAML6.0.3 vàPython3.12.3/PyYAML6.0.1. CI khaiPython3.12,PyYAML6.0.3,fetch-depth0; các ca archive dùng OID sẵn trong ancestry và symlink POSIX, không thấy phụ thuộc ngoài CI. skipped:0 trênLinux;not_run:Windows,CI từ xa,full release/land gate (ngoài phạm vi review A).',
 'Reviewer openai_codex/codex_cli/machine,model_family openai theo identity provider,run887066e7bed94b84824ef0613a0acaf4;model/effort phục vụ KHONG_DO_DUOC. Sandbox khaiworkspace-write,giữ repo read-only bằng thao tác;không GitHub/mạng/commit/push. Executor theoLEASE:anthropic_claude/claude_code/machine/local,session_015GtxrYsNDbfLo32S39f5uY. Source receipt không được nâng thành authority land.'
]
v['verdict']='changes_requested';(w/'VERDICT.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
md=f'''Review wp1236 r9, đợt A, lượt 6: **changes_requested**. Còn **1 P2 và 2 P3**, thuộc **2 lớp mở**, với **27 biểu hiện** (25 mutant không tương đương, một fixture CLI thiếu, một mô tả lệch). Review class `sensitive` đòi đóng cả P3; chưa có miễn trừ neo SHA cho chúng.

`reviewed_sha: {sha}`  
`tree: {tree}`  
`spec_sha256: {v['spec_sha256']}`  
Baseline `0f9aa2a2cc697129e1f5be72feddf60986286865`; spec nguồn `176feba3a09a4e86c6d8b06487f3e4224571be51`, revision 9/generation 1. Repo, lease và write set đều khớp; đúng 3 tệp, +1324/−0 ≤1400.

Lịch sử được dựng lại từ cả năm verdict đã giao; mỗi finding cũ thuộc đúng một lớp. Các probe cũ được tái dựng theo biến đổi/fixture mô tả trong verdict; không có các script scratch cũ trong gói đầu vào. Bằng chứng mới đều chạy trên HEAD này.

| Lớp | Finding cũ và lượt | Trạng thái trên HEAD | Bằng chứng độc lập |
|---|---|---|---|
| `yaml-ngoai-schema-bi-chan` | F01, lượt 1 | `DA_VA_THAT` | Năm dạng YAML ngoài schema giữ passed; m54 đỏ đúng a116. |
| `k2-mat-loi-doc` | F02/G01, lượt 1–2 | `DA_VA_THAT` | YAML/UTF-8 hỏng, symlink tệp/thư mục, lỗi scandir và 0/1/2 provenance chặn đúng; m55/m56/m59/m70 đỏ đúng ca. |
| `cli-vong-yaml-traceback` | F03/H02, lượt 1/3 | `DA_VA_THAT` | Vòng alias và stat tệp/thư mục quá dài đều rc2 không traceback; alias chia sẻ vẫn duyệt được; m57/m58/m65 đỏ đúng ca. |
| `test-thieu-chot` | F04/G02/H01/J01/J02/K01/K02, lượt 1–5 | `VA_MOT_PHAN` | 20 mutant đại diện biểu hiện cũ đã bị giết đúng ca; lớp còn các biểu hiện L01/L02. |

[prior_probes.json](prior_probes.json), [prior_replay_map.json](prior_replay_map.json), [audit_mutants.jsonl](audit_mutants.jsonl) và bảng nối đầy đủ trong [VERDICT.json](VERDICT.json) giữ nguồn từng lượt/SHA. Lớp test xuất hiện cả sáu lượt; hai chuyển tiếp 4→5 và 5→6 đều F/U=0/1. Lớp mới L03 không nằm trong mẫu số này. Cần trả bằng chứng về checkpoint §12 để xét tiếp cách làm; thay phương pháp quét không xoá lịch sử lớp.

**L01 · P2 · `test-thieu-chot`**, tại `ops/gate_output_doi_chieu_test.py:437,445,545,712`. Hai mươi mutant làm sai quyết định hoặc ném ngoại lệ đều qua đủ 36 ca với mã thoát từng ca bằng 0. Các nhóm đã quét:

- `is True` ở dạng gốc/packet và khối ngày đổi thành `== True`: số 1 bị coi là landed, sinh chặn oan.
- PHI_LOI_KHAI bị mở rộng theo chuỗi con hoặc ngừng duyệt bên trong metadata: bỏ sót lời khai phải kiểm.
- Bỏ chữ số khi chuẩn hoá khoá, mở TOKEN để nhận `pass`, nới phần run/đuôi tệp: nhận sai hoặc chặn oan theo đối chứng.
- Bỏ sáu dấu phân cách được phép: `—`, `-`, `(`, `,`, `.`, `;`. Mutant bỏ `:` đã bị a202 bắt và được tính GIẾT.
- Dòng miễn chỉ khớp tiền tố, bỏ strip, hoặc kiểm head bằng truthiness: nhận miễn sai hoặc từ chối dòng hợp lệ.
- Hai biến thể không giữ điều kiện bắt buộc có URL: một bản nhận hồ sơ landed chỉ khai owner_waived mà không có URL; bản kia ném TypeError qua kiem_ho_so. Mã gốc trả đúng vi phạm `waiver_khong_co_can_cu:url` và `landed_khong_loi_khai_gate_output`.

Đối chứng ở [independent_contrasts.json](independent_contrasts.json), [extra_contrasts.json](extra_contrasts.json), [real_waiver_matrix.json](real_waiver_matrix.json). Ma trận miễn cuối dùng bản sao readback thật pr1340, lưu hash nguồn; chỉ sửa bản sao. Cách vá chung: ma trận nghĩa độc lập từ spec cho tập giá trị, grammar, kiểu, 0/1/2 URL và đường đi qua consumer; giữ cặp dương/âm, thêm mutant tương ứng và phân loại riêng tương đương/lỗi vô can. Cần bảo vệ đầu vào hợp lệ khi bổ sung ca, không siết luật sản phẩm để làm oracle xanh.

**L02 · P3 · `test-thieu-chot`**, tại `ops/gate_output_doi_chieu_test.py:167,545,590`. Năm mutant sống chỉ đổi chẩn đoán: skipped v3 có hậu tố (`dong_la`→`co_job_skipped`) và bốn cặp ưu tiên miễn (`html_url`→`tac_gia`, `tac_gia`→`dong_mien`, `han`→`os`, `os`→`sha`). Chúng vẫn từ chối nhưng sai lý do cố định. A2-10 còn thiếu T-khong-prov: trace a210 là **5 fixture thật**, fixture thứ sáu gọi trực tiếp ra rc3 đúng. Bổ sung ca skipped v3, bảng lỗi đồng thời/các đối chứng đơn lỗi và đủ sáu fixture CLI; giữ thứ tự luật theo spec. [cli_acceptance.json](cli_acceptance.json) lưu lời gọi thực tế.

**L03 · P3 · `mo-ta-duong-dan-lech-hop-dong`**, tại `ops/gate_output_doi_chieu.py:224`. Docstring khai cấm `.`; `PurePosixPath` chuẩn hoá thành phần đó và `./tệp` được nhận. Đặc tả A chỉ cấm `..`, tuyệt đối và symlink. Sửa mô tả cho đúng, giữ hành vi A; chốt đóng bằng đối chứng `./tệp` đạt và các ca `../`/symlink tiếp tục bị chặn. [dotpath_probes.json](dotpath_probes.json). Đây là biểu hiện lệch đo được sau khi rà các docstring/mô tả ràng buộc của module.

Bộ quét được kiểm ở hai mức, không dùng tổng đột biến để suy đóng lớp:

| Phép đo | Kết quả |
|---|---|
| Tái sinh/chạy lại bộ AST tại 89fb99b, bộ ca tại chính mốc ấy | 381; 51 không có tín dụng GIẾT: {summary['old_ast']['clean']} sống sạch, {summary['old_ast']['incidental']} lỗi vô can |
| Tái sinh/chạy lại bộ AST tại HEAD | 368; 362 GIẾT, 6 lỗi vô can; không còn bản sống sạch trong tập AST đó |
| Xác minh riêng | 362/362 chết đúng ca đích không patch/cache YAML; sáu bản còn lại chạy đủ 36 ca bằng SafeLoader có memo/deepcopy, không có tín dụng giết hợp lệ, có rc4; k339 chết tại a217 nhờ m124 |
| Thước độc lập mở rộng | **127 mutant: 93 GIẾT, 34 SỐNG** |
| Phân biệt 34 bản sống | **9 tương đương trong miền đầu vào; 25 làm khác hành vi** |
| Kiểm lại 25 bản làm khác hành vi | **36/36 ca rc0 cho từng bản**, không patch/cache YAML |

[all_independent_results.json](all_independent_results.json) liệt kê mọi toán tử và kết quả ca; nguồn bản sao ở `independent_mutants.jsonl`, `independent_corrected.jsonl`, `extra_mutants.jsonl` và `order_url_mutants.jsonl`, `reason_complete_mutants.jsonl`; [measurement_summary.json](measurement_summary.json) liệt kê đầy đủ 20 ID P2 và 5 ID P3; [semantic_native_full.jsonl](semantic_native_full.jsonl), [order_url_results.jsonl](order_url_results.jsonl) là kết quả không cache. Tập 102 ban đầu giữ SafeLoader và memo/deepcopy; hai lỗi của script đo riêng (trùng ID và sửa nhầm ngoặc regex) đã được loại, sửa và chạy lại. Quét bổ sung đủ 43 vị trí literal lý do cố định (kể cả append/comprehension/nhánh điều kiện), 20 bản bổ sung đều chết trên loader gốc không cache; xem `reason_census.json` và `reason_complete_results.jsonl`. Chín bản tương đương không tính thành finding; tám phép is/== trên giá trị parser/Path/regex chuẩn cùng một lookbehind dư được giải thích trong [equivalence.json](equivalence.json), với 20.736 đối chứng tên tệp không lệch. Hai phép is True không tương đương đã được giữ trong L01.

`quet/sinh.py` chỉ sinh phủ định/loại vế, thay số/bool và return; bỏ qua hằng chuỗi, regex, tập ở mức module, ưu tiên lỗi và thay is bằng ==. `chay_ca.py` dừng ở ca đầu rc3; `chay.py` không lưu child rc và không tự chứng minh baseline. C loader của scanner **đổi ngữ nghĩa**: tab sau colon/cuối dòng trong bản sao provenance bị SafeLoader từ chối nhưng CSafeLoader nhận; các escape Unicode cũng đổi kết quả/lớp ngoại lệ. [yaml_parity.json](yaml_parity.json). Vì vậy tín dụng của 362 bản đã được xác minh lại bằng tiến trình ca đích dùng loader sản phẩm. Sáu rc4 không phải SỐNG xanh và không được cấp tín dụng GIẾT.

| Kiểm bắt buộc / hợp đồng | Kết quả và giới hạn |
|---|---|
| Suite Python3.13.18/PyYAML6.0.3 | rc0; `CA: 36/36 dat`; `DOT BIEN: 124/124 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (2 dot bien)`; `TONG: DAT` |
| Suite Python3.12.3/PyYAML6.0.1 | Cùng bốn dòng, rc0; cả hai stdout khớp regex đăng ký |
| Audit 124 mutant khai trong suite | 124/124 TinHieuChotCa ở đúng ca đích. Một số chỉ chứng minh chẩn đoán: m6→KeyError; m22/m23/m79 còn K2 symlink; m80→FileNotFoundError; m96–m100 kiểm tên lỗi kiểu. |
| Ruff bare, đúng ba tệp, --no-cache --select F | rc0, All checks passed; Ruff0.15.15 |
| ci_dang_ky_test.py | rc0;31/31;Ruff CI contract3/3;1226/1226 phản chứng |
| Corpus tại immutable base0f9aa2a |66 tệp=47/10/9;170 hồ sơ=25/56/39/50;94 landed,0 lệch;50 script=20/28/2 và đúng ba băm BO_SINH |
| Consumer độc lập |1 đối chứng dương+21 biến thể; không tìm thấy lời khai dương lọt ngoài giới hạn r9 |
| Bốn rút gọn so89fb99b |27 đối chứng khớp; xem [simplifications_probes.json](simplifications_probes.json) |
| K1–K8 và mọi API/hằng/tên lý do/CLI của Module mới | Đã đối chiếu; các counterexample đo trên HEAD xử lý đúng. L01/L02 thuộc bộ nghiệm thu; L03 thuộc mô tả helper. L8/D2b là đợt B/C. |
| Diff/check/trần |3 tệp,+1324/−0≤1400;diff --check rc0 |

Đối chiếu chi tiết mục *Module mới* (đọc mã và đặc tả, kết hợp probe độc lập với audit ca đích):

| Phần | Hành vi và tên lý do đã đối chiếu | Bằng chứng |
|---|---|---|
| Hằng | BO_SINH đúng ba SHA/nhãn; CHECK_BAT_BUOC_TEN đúng năm tên; PHI_LOI_KHAI đúng ba tên; TOKEN đúng bảy giá trị | corpus/producer_contrasts; a104/a109/a201/a202; quét thay/bỏ từng thành viên |
| doc_danh_gia/K1 | UTF-8, LF/CRLF; fullmatch header/job/skip/tổng; `khong_phai_utf8`, `xuong_dong_tron`, `cr_le`, `dau_tep_sai`, `dong_la`, `job_lap`, `thieu_moc`, `moc_lap`, `bo_sinh_la` | a103/a104/a118; các mutation lý do; skip v3 thiếu ca riêng ghi L02 |
| chon_provenance/K2 | schema và bộ ba run/attempt/head, số int nghiêm, không theo symlink; `symlink`, `provenance_0`, `provenance_nhieu` | prior, consumer_matrix, a108/a116/a117/a118 |
| K3 | push/ci.yml, cờ run/tập job/checkout khác rỗng, ngoại lệ checkout skipped đúng job; `khong_phai_run_land`, `provenance_chua_du` | consumer_matrix, a108/a114/a119 |
| K4 | ID trùng và tập job/skip chính xác; `job_id_trung_provenance`, `tap_job_lech`, `tap_skip_lech` | consumer_matrix, a107/a117 |
| K5 | name/conclusion/labels, kết luận tương thích trạng thái; `job_lech:<id>`, `ket_luan_lech:<id>` | consumer_matrix, a106/a113; rút gọn tương đương đại số |
| K6 | băm dòng khớp str(băm provenance); `log_sha_lech:<id>` | consumer_matrix, a105 |
| K7 | skip đúng phiên bản, tính ba thành phần tổng; `dong_skip_sai_phien_ban`, `moc_lech` | a110/a111/a119 và corpus |
| K8/kiem_tep | failed trước skipped/check; `co_job_skipped`, `check_bat_buoc:<tên>`; gom lỗi K3–7, ngoại lệ → not_measured/TênNgoạiLệ | a109/a112/a115, prior, audit 124 |
| loi_khai/_chuan | casefold, giữ chữ và số, mọi độ sâu/list; loại đúng tên nhưng vẫn duyệt con; vòng alias bị chặn | prior, a201/a214; L01 là lỗ hổng test, mã gốc đúng |
| token/tep_danh_gia | đúng regex đóng băng, casefold/tập token; trích mọi tên tệp, kể cả nhiều tệp | independent_contrasts, a202/a207; L01 là lỗ hổng test |
| la_landed | is True ở ba dạng; ưu tiên có khoá packet; fullmatch khối ngày | corpus 94/170 lệch 0, independent_contrasts, a212/a213/a215 |
| _tep_trong/kiem_ho_so | tương đối provenance, cấm tuyệt đối/../symlink; mọi tệp phải khớp trạng thái; token âm không tạo lời khai hợp lệ; `dinh_dang_loi_khai`, `duong_khong_tep_danh_gia`, `tep_danh_gia_khong_hop_le`, `danh_gia_khong_passed/failed`, `waiver_khong_co_can_cu`, `landed_khong_loi_khai_gate_output` | consumer_matrix, dotpath, a203–a208/a212/a215/a216; docstring sai ở L03 |
| kiem_mien | đúng một URL/readback/dòng strip+fullmatch; chủ kho/OWNER; ngày lịch, ubuntu, head khác None so trực tiếp; thứ tự `url, readback, doc_readback, html_url, tac_gia, dong_mien, han, os, sha` | real_waiver_matrix, a209/a215; thiếu ca biên/thứ tự ghi L01/L02 |
| CLI/main | kiem-tep 0/1/3, sai tham số 2; kiem-ho-so 0/1/2, nhiều hồ sơ giữ lỗi; help 0; không traceback | prior, a210/a214/a217; A2-10 thiếu fixture thứ sáu ghi L02 |

K5 rút gọn tương đương đại số: vế `tt==passed && conclusion!=success` đã nằm trong `conclusion!=success && tt!=failed`. `os.walk(followlinks=False)` vẫn không đi vào symlink khi bỏ lọc thu[:]. Các đối chứng glob trên thư mục vắng/tệp/symlink và body JSON falsy/chuỗi miễn hợp lệ đều giữ kết quả. Không thấy regression từ bốn rút gọn.

CI khai Python3.12, PyYAML6.0.3, fetch-depth0; các OID archive đều có trong ancestry đã cấp, symlink POSIX chạy được. Không thấy ca cần thứ vắng trong CI đã khai. `skipped`:0 trên Linux; `not_run`:Windows và CI từ xa/full release/land gate. Những phần log thật, provenance/readback sửa tay, danh tính người gõ và neo commit hồ sơ khác được giữ đúng giới hạn `chua_do_duoc`/`ngoai_pham_vi` của r9.

Reviewer `openai_codex / codex_cli / machine`, họ `openai` theo identity provider, run `887066e7bed94b84824ef0613a0acaf4`; model/effort phục vụ `KHONG_DO_DUOC`. Executor theo lease: `anthropic_claude / claude_code / machine/local`, phiên `session_015GtxrYsNDbfLo32S39f5uY`. Sandbox khai `workspace-write`; repository được giữ read-only bằng thao tác, không GitHub/mạng/commit/push. Hash {len(files):,} tệp đầu/cuối, kể cả ignored .codex, khớp; HEAD/tree và diff index không đổi. Snapshot không chứng minh lịch sử ghi rồi hoàn nguyên; repo nguồn ngoài checkout không được quan sát.

Các lệnh/script và output đầy đủ nằm cạnh báo cáo; stdout/stderr có mã thoát thật, phân biệt tín dụng GIẾT, SỐNG và lỗi vô can. JSON đã kiểm bằng `kiem_verdict_lop.py --vong 6`; kết quả lưu ở [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: changes_requested
'''
(w/'VERDICT.md').write_text(md)
cmd=['python3','-B',str(w.parent/'kiem_verdict_lop.py'),str(w/'VERDICT.json'),'--vong','6'];z=subprocess.run(cmd,capture_output=True,text=True);(w/'kiem_verdict.txt').write_text(z.stdout+z.stderr);(w/'kiem_verdict.rc').write_text(str(z.returncode)+'\n');assert z.returncode==0,z.stdout+z.stderr
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in w.iterdir() if p.is_file() and p.name not in ('manifest.json',)};(w/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True))
print(z.stdout.strip());print(json.dumps(summary,ensure_ascii=False));print('VERDICT',sha,tree)
