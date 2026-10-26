import ast, concurrent.futures, copy, hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('test8',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();tree=ast.parse(src);out=R/'operators8';out.mkdir(exist_ok=True);mut=[]
def add(f,j,label,new):
    tr=ast.parse(src);ff=next(x for x in tr.body if isinstance(x,ast.FunctionDef) and x.name==f.name);node=list(ast.walk(ff))[j]
    t._thay(node,new);source=ast.unparse(ast.fix_missing_locations(tr));compile(source,'<operator>','exec');mid=f'{f.name}_{j}_{label}';p=out/(mid+'.py');p.write_text(source);mut.append((mid,f.name,p,ast.unparse(list(ast.walk(f))[j]),ast.unparse(new)))
for f in tree.body:
    if not isinstance(f,ast.FunctionDef) or f.name not in t.HAM_DONG:continue
    for j,n in enumerate(ast.walk(f)):
        if isinstance(n,ast.Slice):
            for label,field,val in [('slice_step2','step',ast.Constant(2)),('slice_reverse','step',ast.Constant(-1))]:
                nn=copy.deepcopy(n);setattr(nn,field,val);add(f,j,label,nn)
            if isinstance(n.upper,ast.Name):
                for offset in (-1,1):
                    nn=copy.deepcopy(n);nn.upper=ast.BinOp(left=nn.upper,op=ast.Add(),right=ast.Constant(offset));add(f,j,'slice_upper'+str(offset),nn)
        if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Name) and n.slice.id=='i':
            for offset in (-1,1):
                nn=copy.deepcopy(n);nn.slice=ast.BinOp(left=nn.slice,op=ast.Add(),right=ast.Constant(offset));add(f,j,'index'+str(offset),nn)
        if isinstance(n,ast.BinOp):
            for label,nn in [('keep_left',n.left),('keep_right',n.right)]:add(f,j,label,copy.deepcopy(nn))
        if isinstance(n,ast.AugAssign) and isinstance(n.op,ast.Add):
            nn=copy.deepcopy(n);nn.op=ast.Sub();add(f,j,'subtract',nn)
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('any','all'):
            nn=copy.deepcopy(n);nn.func.id='any' if n.func.id=='all' else 'all';add(f,j,'quantifier',nn)
        if isinstance(n,ast.Attribute) and n.attr in ('startswith','rstrip','fullmatch','search'):
            nn=copy.deepcopy(n);nn.attr={'startswith':'endswith','rstrip':'lstrip','fullmatch':'match','search':'match'}[n.attr];add(f,j,'attribute_'+nn.attr,nn)
        if isinstance(n,ast.NamedExpr) and isinstance(n.target,ast.Name) and n.target.id=='h':
            for name in ('a','z'):nn=copy.deepcopy(n);nn.value=ast.Name(id=name,ctx=ast.Load());add(f,j,'walrus_'+name,nn)
def one(item):
    mid,func,p,old,new=item;cmd=[sys.executable,'-B',str(R/'closed8.py'),'child',str(p),func];z=subprocess.run(cmd,capture_output=True,timeout=1800)
    try:
        rows=json.loads(z.stdout)['cases'];kill=[c for c,rc,d in rows if rc==3 and d.startswith(f'DO:{c}:')];rank='GIET' if kill else 'TIN_DUNG_GIA' if any(rc for _,rc,_ in rows) else 'SONG'
    except (ValueError,KeyError):rows=[];kill=[];rank='HONG'
    v={'id':mid,'function':func,'before':old,'after':new,'command':cmd,'rc':z.returncode,'rank':rank,'kill':kill,'cases_measured':len(rows),'stdout':z.stdout.decode(),'stderr':z.stderr.decode()};(out/(mid+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=1));return {k:v[k] for k in ('id','function','before','after','rank','kill','cases_measured')}
rs=[]
with concurrent.futures.ThreadPoolExecutor(3) as ex:
    for v in ex.map(one,mut):rs.append(v);(R/'operators8-results.json').write_text(json.dumps(rs,ensure_ascii=False,indent=1));print(v['id'],v['rank'],flush=True)
print('OPERATORS',len(rs))
