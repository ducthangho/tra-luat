from review_common import *
import ast,re,random
s=load(R/'ops/gate_output_doi_chieu_test.py','tail_suite')
g=s.G();src=ast.unparse(ast.parse((R/'ops/gate_output_doi_chieu.py').read_text()))+'\n'
pool={x['id']:x for x in map(json.loads,(W.parent/'bang_chung/kho_dot_bien_reviewer_luot6_7_8.jsonl').read_text().splitlines())}
ledger=[x for x in map(json.loads,(W.parent/'bang_chung/ledger_kho_152_2719f81.jsonl').read_text().splitlines()) if x['ledger']!='GIET']
checks={'identity_126_7':['a103_bo_phan_tich','a101_sau_fixture_that'], 'identity_131_7':['a108_neo','a101_sau_fixture_that'], 'identity_154_11':['a107_tap_job'], 'identity_262_25':['a209_mien','a122_mien_ma_tran'], 'identity_271_11':['a202_token','a203_duong_khong_tep'], 'identity_285_19':['a204_duong_dan','a205_duong_khop'], 'identity_85_11':['a108_neo']}
# Resolve case prefixes from actual suite (avoid guessing exact suffix names).
checks={k:[next(n for n in s.CA if n.split('_')[0]==c.split('_')[0]) for c in v] for k,v in checks.items()}
reports=[]
def test(id,cu,moi,cases):
 assert src.count(cu)==1,(id,src.count(cu));p=W/(id+'.py');p.write_text(src.replace(cu,moi))
 m=load(p,id);old=s._M[:];s._M[:]=[m]
 rows=[]
 for c in cases:
  rc,msg=s.chay_ca(c);rows.append(dict(case=c,rc=rc,message=msg))
 s._M[:]=old
 return rows
for d in ledger:
 id=d['id']
 if d['ledger']=='TUONG_DUONG':
  p=pool[id];rows=test(id,p['cu'],p['moi'],checks[id]);assert all(x['rc']==0 for x in rows)
  proof=('type(x) yields built-in type for YAML types used; identity/equality of these types same' if id=='identity_85_11' else 'reachable operand is None or built-in dict/string/Path; equality with None is exactly identity on contracted inputs; head only str|None')
  reports.append(dict(id=id,status='TUONG_DUONG',cases=rows,proof=proof))
 elif id=='identity_72_67':
  rows=test(id,"s.re is RE_SKIP_V3","s.re == RE_SKIP_V3",['a111_skipped_theo_phien_ban','a115_skipped_mat_passed'])
  assert all(x['rc']==0 for x in rows)
  proof=dict(patterns_distinct=g.RE_SKIP_CU.pattern!=g.RE_SKIP_V3.pattern,v3_identity=g.RE_SKIP_V3.fullmatch('JOB 777 x: skipped -> not_measured (khong suy pass)').re is g.RE_SKIP_V3,cu_identity=g.RE_SKIP_CU.fullmatch('JOB 777 x: skipped (khong tinh)').re is g.RE_SKIP_CU)
  reports.append(dict(id=id,status='KHONG_AP_DUNG -> j1:doc_danh_gia:72:43 TUONG_DUONG',proof=proof,cases=rows))
 elif id=='ref_no_boundary':
  bound=re.compile(r'(?<![A-Za-z0-9_./-])'+g.RE_TEP_DG.pattern);rng=random.Random(1236)
  for i in range(10000):
   st=''.join(rng.choices('abc/._-! é012',k=20))+'danh-gia-gate-output-12.txt'+''.join(rng.choices('abc/._-! é012',k=20))
   assert bound.findall(st)==g.tep_danh_gia(st)
  reports.append(dict(id=id,status='KHONG_AP_DUNG -> CHOT_DA_BO',proof='r11 explicitly does not require lookbehind; greedy leftmost maximal token has same boundary',samples=10000,delta=0))
 elif id=='ref_any_run':
  db=next(x for x in s.DOT_BIEN if x[0]=='m131_tep_run_chu');k,ct=s.chay_dot_bien(*db);assert k=='GIET';reports.append(dict(id=id,status='KHONG_AP_DUNG -> m131 GIET',result=k,evidence=ct))
 elif id=='ref_txt_wild':
  line=next(x for x in src.splitlines(True) if x.startswith('RE_TEP_DG = '));new=line.replace(r'\\.txt','.txt');rows=test(id,line,new,['a121_token_tep_khoa_landed']);assert rows[0]['rc']==3;reports.append(dict(id=id,status='KHONG_AP_DUNG -> i5 GIET',cases=rows))
 elif id=='delete_return_227':
  tree=ast.parse(src);f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_tep_trong');ret=[x for x in ast.walk(f) if isinstance(x,ast.Return)]
  replacements=[]
  for i,n in enumerate(ret):
   tt=ast.parse(src);ff=next(x for x in tt.body if isinstance(x,ast.FunctionDef) and x.name=='_tep_trong')
   class Replace(ast.NodeTransformer):
    def visit_Return(self,x):return ast.Pass() if x.lineno==n.lineno else x
   Replace().visit(ff);p=W/f'return_{n.lineno}.py';p.write_text(ast.unparse(tt));m=load(p,f'return_{n.lineno}');old=s._M[:];s._M[:]=[m]
   case='a205_duong_khop' if isinstance(n.value,ast.IfExp) else 'a204_duong_dan';rc,msg=s.chay_ca(case);s._M[:]=old;assert rc==3,(rc,msg)
   replacements.append(dict(line=n.lineno,case=case,rc=rc,message=msg))
  reports.append(dict(id=id,status='KHONG_AP_DUNG -> 3 same-meaning returns GIET',replacements=replacements))
save('ledger_tail.json',reports)
print('LEDGER_TAIL 7 equivalent; 5 KAD valid under r11, all independently checked')
