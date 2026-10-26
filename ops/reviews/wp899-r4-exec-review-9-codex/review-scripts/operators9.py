import ast, collections, concurrent.futures, copy, hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('test9',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();tree=ast.parse(src);out=R/'operators9';out.mkdir(exist_ok=True);mut=[]
def add(f,j,label,new):
 tr=ast.parse(src);ff=next(x for x in tr.body if isinstance(x,ast.FunctionDef) and x.name==f.name)
 t._thay(list(ast.walk(ff))[j],new);v=ast.unparse(ast.fix_missing_locations(tr))
 try:compile(v,'<probe9>','exec')
 except (SyntaxError,ValueError,TypeError):return
 mid=f'{f.name}_{j}_{label}';p=out/(mid+'.py');p.write_text(v)
 mut.append((mid,f.name,p,ast.unparse(list(ast.walk(f))[j]),ast.unparse(new)))
for f in tree.body:
 if not isinstance(f,ast.FunctionDef) or f.name not in t.HAM_DONG:continue
 for j,n in enumerate(ast.walk(f)):
  if isinstance(n,ast.Dict):
   for k in range(len(n.keys)):
    nn=copy.deepcopy(n);nn.keys.pop(k);nn.values.pop(k);add(f,j,'drop_dict_'+str(k),nn)
  if isinstance(n,ast.Call):
   if len(n.args)==1:
    nn=copy.deepcopy(n);nn.args=[];add(f,j,'drop_single_arg',nn)
   if n.keywords:
    nn=copy.deepcopy(n);nn.keywords=[];add(f,j,'drop_keywords',nn)
  if isinstance(n,(ast.Tuple,ast.List)) and isinstance(n.ctx,ast.Load):
   for k in range(len(n.elts)):
    nn=copy.deepcopy(n);nn.elts.pop(k);add(f,j,'drop_elt_'+str(k),nn)
  if isinstance(n,ast.For):
   nn=copy.deepcopy(n);nn.iter=ast.Call(func=ast.Name(id='reversed',ctx=ast.Load()),args=[nn.iter],keywords=[]);add(f,j,'reverse_iter',nn)
  if isinstance(n,ast.Continue):add(f,j,'continue_to_pass',ast.Pass())
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Sub):
   nn=copy.deepcopy(n);nn.op=ast.BitAnd();add(f,j,'set_intersection',nn)
def one(item):
 mid,func,p,old,new=item;cmd=[sys.executable,'-B',str(R/'closed8.py'),'child',str(p),func]
 z=subprocess.run(cmd,capture_output=True,timeout=1800)
 try:
  rows=json.loads(z.stdout)['cases'];kill=[c for c,rc,d in rows if rc==3 and d.startswith(f'DO:{c}:')]
  rank='GIET' if kill else 'TIN_DUNG_GIA' if any(rc for _,rc,_ in rows) else 'SONG'
 except (ValueError,KeyError):rows=[];kill=[];rank='HONG'
 v={'id':mid,'function':func,'before':old,'after':new,'command':cmd,'process_rc':z.returncode,'rank':rank,'kill':kill,
    'cases_measured':len(rows),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'stdout':z.stdout.decode(),'stderr':z.stderr.decode()}
 (out/(mid+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=1))
 return {k:v[k] for k in ('id','function','before','after','rank','kill','cases_measured')}
rs=[]
with concurrent.futures.ThreadPoolExecutor(4) as ex:
 for v in ex.map(one,mut):
  rs.append(v);(R/'operators9-results.json').write_text(json.dumps(rs,ensure_ascii=False,indent=1));print(v['id'],v['rank'],flush=True)
print('OPERATORS9',len(rs),dict(collections.Counter(x['rank'] for x in rs)))
