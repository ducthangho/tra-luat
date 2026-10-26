import ast, contextlib, hashlib, importlib.util, io, json, pathlib
R=pathlib.Path(__file__).resolve().parent;root=R.parent
def load(p,name):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
rows=[];copies=[]
sources=[(1,'new_probes_r4.py',None),(2,'new_probes_r4.py',None),(3,'frontier_cases.py','calc'),(4,'boundary_cases.py','case'),(5,'cases5.py','case'),(6,'cases6.py','probe'),(7,'cases7.py','probe')]
for rnd,name,func in sources:
    p=root/f'.review-input/r4-luot{rnd}'/name;q=R/f'history{rnd}-copy.py';q.write_bytes(p.read_bytes());text=p.read_text();copies.append({'round':rnd,'source':str(p.relative_to(root)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'copy':q.name})
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):m=load(q,'h'+str(rnd))
    if func is None:
        (R/f'history{rnd}-stdout.txt').write_text(buf.getvalue());rows.append({'round':rnd,'function':'top_level','exception':None,'observations':len(m.result),'results':m.result});continue
    tree=ast.parse(text);f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==func);arg=f.args.args[0].arg;labels=[]
    for n in ast.walk(f):
        if isinstance(n,ast.Compare) and isinstance(n.left,ast.Name) and n.left.id==arg:
            for c in n.comparators:
                if isinstance(c,ast.Constant) and isinstance(c.value,str):labels.append(c.value)
                elif isinstance(c,(ast.Tuple,ast.List)):labels += [z.value for z in c.elts if isinstance(z,ast.Constant) and isinstance(z.value,str)]
    if hasattr(m,'LABELS'):labels=list(m.LABELS)
    if rnd==3:labels=[x for x in labels if x!='key_']+['key_id','key_if','key_timeout-minutes','key_continue-on-error']
    for label in dict.fromkeys(labels):
        try:
            with contextlib.redirect_stdout(buf):answer=getattr(m,func)(label)
            result={'round':rnd,'case':label,'status':'passed'}
        except Exception as e:result={'round':rnd,'case':label,'status':'failed','exception':type(e).__name__,'message':str(e)}
        rows.append(result)
    print('HISTORY',rnd,len(labels),flush=True)
(R/'history8-results.json').write_text(json.dumps({'copies':copies,'rows':rows},ensure_ascii=False,indent=1))
bad=[x for x in rows if x.get('status')=='failed'];print('HISTORY cases',len(rows),'failed',len(bad));print(json.dumps(bad,ensure_ascii=False,indent=2))
