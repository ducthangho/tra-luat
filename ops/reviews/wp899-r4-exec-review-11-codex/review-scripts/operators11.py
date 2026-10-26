import ast, collections, concurrent.futures, copy, hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent
root=R.parent
def load(p,name):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(root/'ops/ci_provenance_test.py','t11')
src=(root/'ops/ci_provenance.py').read_text();tree=ast.parse(src)
out=R/'operators11';out.mkdir(exist_ok=True);mut=[];invalid=[]
def add(f,j,label,node):
    tr=ast.parse(src);ff=next(x for x in tr.body if isinstance(x,ast.FunctionDef) and x.name==f.name)
    target=list(ast.walk(ff))[j];before=ast.unparse(target);t._thay(target,node)
    source=ast.unparse(ast.fix_missing_locations(tr));mid=f'{f.name}_{j}_{label}'
    try:compile(source,'<r11>','exec')
    except (SyntaxError,ValueError,TypeError) as e:invalid.append([mid,type(e).__name__]);return
    p=out/(mid+'.py');p.write_text(source)
    mut.append((mid,f.name,p,before,ast.unparse(node)))
for f in tree.body:
    if not isinstance(f,ast.FunctionDef) or f.name not in t.HAM_DONG:continue
    for j,n in enumerate(ast.walk(f)):
        if isinstance(n,(ast.Assign,ast.AugAssign,ast.Expr)):
            if isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant):continue
            add(f,j,'delete_statement',ast.Pass())
        elif isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):
            nn=copy.deepcopy(n);nn.op=ast.UAdd();add(f,j,'unary_plus',nn)
        elif isinstance(n,ast.BinOp) and isinstance(n.op,ast.BitOr):
            nn=copy.deepcopy(n);nn.op=ast.BitAnd();add(f,j,'dict_intersection',nn)
        elif isinstance(n,ast.NamedExpr):
            add(f,j,'drop_binding',copy.deepcopy(n.value))
        elif isinstance(n,ast.ExceptHandler):
            nn=copy.deepcopy(n);nn.type=ast.Name(id='RuntimeError',ctx=ast.Load());add(f,j,'catch_runtime_only',nn)
        elif isinstance(n,ast.Slice) and isinstance(n.upper,ast.Name):
            for delta in (-1,1):
                nn=copy.deepcopy(n);nn.upper=ast.BinOp(left=nn.upper,op=ast.Add(),right=ast.Constant(delta));add(f,j,'upper'+str(delta),nn)
def one(item):
    mid,func,p,before,after=item
    cmd=[sys.executable,'-B',str(R/'closed8.py'),'child',str(p),func]
    z=subprocess.run(cmd,capture_output=True,timeout=1800)
    try:
        rows=json.loads(z.stdout)['cases'];kills=[c for c,rc,d in rows if rc==3 and d.startswith(f'DO:{c}:')]
        rank='GIET' if kills else 'TIN_DUNG_GIA' if any(rc for _,rc,_ in rows) else 'SONG'
        if not kills and len(rows)!=52:rank='HONG'
    except (ValueError,KeyError):rows=[];kills=[];rank='HONG'
    record={'id':mid,'function':func,'node_before':before,'node_after':after,'command':cmd,'process_rc':z.returncode,
            'rank':rank,'kills':kills,'cases_measured':len(rows),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
            'stdout':z.stdout.decode(),'stderr':z.stderr.decode()}
    (out/(mid+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=1))
    return {k:v for k,v in record.items() if k not in ('stdout','stderr')}
rows=[]
with concurrent.futures.ThreadPoolExecutor(4) as ex:
    for result in ex.map(one,mut):
        rows.append(result)
        (R/'operators11-results.json').write_text(json.dumps({'rows':rows,'invalid':invalid},ensure_ascii=False,indent=1))
        print(result['id'],result['rank'],flush=True)
print('OPERATORS11',len(rows),dict(collections.Counter(x['rank'] for x in rows)))
