import ast,collections,importlib.util,json,re,sys,subprocess
from review_measure import W,R,C,save,sha
D=R/'ops/reviews/wp1236-r10-soan';Q=D/'quet_dot_bien.py'
s=importlib.util.spec_from_file_location('scanner',Q); q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
M=[json.loads(x) for x in (W/'m1.jsonl').read_text().splitlines()];H=[json.loads(x) for x in (W/'h.jsonl').read_text().splitlines()]
key=lambda s: ast.dump(ast.parse(s),include_attributes=False)
md=collections.defaultdict(list)
for x in M:md[key(x['src'])].append(x['id'])
coverage=[]
for x in H:coverage.append({'id':x['id'],'kind':x['kind'],'exact_ast_generated':md[key(x['src'])],'src_sha256':x['sha256']})
# Inspect all regex mutations using actual production patterns, without inventing inputs or new product code.
t=ast.parse((C/'ops/gate_output_doi_chieu.py').read_text());base_patterns={n.targets[0].id:ast.literal_eval(n.value.args[0]) for n in t.body if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='compile'}
regex_rows=[]
for x in M:
 if x['op'] in {'i1','i2','i3','i4','i5','i6'}:
  u=ast.parse(x['src']);ps={n.targets[0].id:ast.literal_eval(n.value.args[0]) for n in u.body if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='compile'}
  for name,orig in base_patterns.items():
   if orig!=ps[name]:regex_rows.append({'id':x['id'],'name':name,'before':orig,'after':ps[name]})
# Corpus/sample totals and size use the actual frozen source/base.
spec=(W.parent/'SPEC.md').read_text(); counts={'A1':re.findall(r'^\| (A1-\d+) ',spec,re.M),'A2':re.findall(r'^\| (A2-\d+) ',spec,re.M),'rules':re.findall(r'^([1-5])\. \*\*',spec[spec.index('### Ma trận'):spec.index('### Đợt A')],re.M)}
num=subprocess.run(['git','-C',str(C),'diff','--numstat','0f9aa2a2cc697129e1f5be72feddf60986286865','HEAD','--','ops/gate_output_doi_chieu.py','ops/gate_output_doi_chieu_test.py','.claude/dev/ci_dang_ky_test.py'],capture_output=True,text=True)
waiver=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='kiem_ho_so')
# Read-only baseline of B/C interfaces; no suite execution needed.
interfaces={}
for name,p in [('B',R/'ops/land_evidence_nguon_test.py'),('C',R/'.claude/dev/packet_loop_test.py')]:
 u=ast.parse(p.read_text());functions={n.name for n in u.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}; names={v.id for n in u.body if isinstance(n,ast.Assign) for v in n.targets if isinstance(v,ast.Name)}
 interfaces[name]={'CA':'CA' in names,'CASES':'CASES' in names,'chay_ca':'chay_ca' in functions,'TinHieuChotCa':'TinHieuChotCa' in functions,'contains_GODC_override':'GATE_OUTPUT_DOI_CHIEU_MA' in p.read_text()}
# A pure read-only import checks the B override on a path that is not opened by nap().
bp=R/'ops/land_evidence_nguon_test.py'
code='import importlib.util,sys,os; s=importlib.util.spec_from_file_location("b",sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.MA); print(os.environ["GATE_OUTPUT_DOI_CHIEU_MA"])'
import os
b=subprocess.run([sys.executable,'-B','-c',code,str(bp)],capture_output=True,text=True,env=dict(os.environ,GATE_OUTPUT_DOI_CHIEU_MA=str(W/'module_not_loaded.py'),PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp')))
out={'coverage':coverage,'exact_ast_count':sum(bool(x['exact_ast_generated']) for x in coverage),'regex_inventory':regex_rows,'counts':counts,'numstat':{'rc':num.returncode,'stdout':num.stdout},'kiem_ho_so_args':[x.arg for x in waiver.args.args],'kiem_mien_calls':[ast.unparse(n) for n in ast.walk(waiver) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='kiem_mien'],'interfaces':interfaces,'B_override_probe':{'rc':b.returncode,'stdout':b.stdout,'stderr':b.stderr}}
save('structural_audit.json',out)
print('STRUCTURAL_AUDIT_COMPLETE',json.dumps({k:v for k,v in out.items() if k not in ['coverage','regex_inventory']},ensure_ascii=False))
