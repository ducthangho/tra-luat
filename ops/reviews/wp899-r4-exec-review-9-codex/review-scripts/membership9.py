import ast, concurrent.futures, hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t9',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();items=[]
for name in ['ghep_job','ten_du_kien']:
 tr=ast.parse(src);f=next(n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name==name)
 n=next(n for n in ast.walk(f) if isinstance(n,ast.Compare) and isinstance(n.left,ast.Constant) and n.left.value=='${{')
 old=ast.unparse(n);nn=ast.UnaryOp(op=ast.Not(),operand=ast.Call(func=ast.Attribute(value=n.comparators[0],attr='startswith',ctx=ast.Load()),args=[n.left],keywords=[]))
 t._thay(n,nn);text=ast.unparse(ast.fix_missing_locations(tr));p=R/(name+'-membership9.py');p.write_text(text);items.append((name,p,old,ast.unparse(n)))
def one(it):
 name,p,old,new=it;cmd=[sys.executable,'-B',str(R/'closed8.py'),'child',str(p),name];z=subprocess.run(cmd,capture_output=True)
 data=json.loads(z.stdout);rows=data['cases'];kill=[c for c,rc,d in rows if rc==3 and d.startswith(f'DO:{c}:')]
 return {'function':name,'before':old,'after':new,'path':str(p),'command':cmd,'rc':z.returncode,'cases':rows,
   'rank':'GIET' if kill else 'TIN_DUNG_GIA' if any(rc for _,rc,_ in rows) else 'SONG',
   'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'stdout':z.stdout.decode(),'stderr':z.stderr.decode()}
with concurrent.futures.ThreadPoolExecutor(2) as ex:rs=list(ex.map(one,items))
proof=[]
for label,path in [('head',root/'ops/ci_provenance.py')]+[(n,p) for n,p,_,_ in items]:
 t.MA=path
 for axis in ['job','step']:
  nm='Build ${{x}}';w=t.wf_job(j=({'name':nm},None)) if axis=='job' else t.wf_tu(t.X,buoc_them={'name':nm})
  pv=t.g1(w,t.buoc(t.X,'THU: 4/4 dat'),ten=nm if axis=='job' else 'j')
  proof.append({'source':label,'axis':axis,'ghep':t.gate(pv)['ghep_buoc'],'gate':t.gate(pv)['trang_thai'],'markers':t.gate(pv)['dau_duong']})
(R/'membership9-results.json').write_text(json.dumps({'mutants':rs,'proof':proof},ensure_ascii=False,indent=2))
print(json.dumps({'mutants':[{k:v[k] for k in ('function','rank','before','after')}|{'n':len(v['cases'])} for v in rs],'proof':proof},ensure_ascii=False,indent=2))
