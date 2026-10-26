import ast, copy, hashlib, importlib.util, itertools, json, pathlib, re
R=pathlib.Path(__file__).resolve().parent;root=R.parent
def load(p,name):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(root/'ops/ci_provenance_test.py','t8');head=load(root/'ops/ci_provenance.py','head8');src=(root/'ops/ci_provenance.py').read_text();results=[]
for mid,proof in t.TUONG_DUONG.items():
    func,rest=mid.split('#');index,label=rest.split(':');tr=ast.parse(src);f=next(x for x in tr.body if isinstance(x,ast.FunctionDef) and x.name==func);node=list(ast.walk(f))[1:][int(index)];fn=dict(t._toan_tu(node))[label];fn(node);text=ast.unparse(ast.fix_missing_locations(tr));p=R/('eq-'+mid.replace('#','_').replace(':','_')+'.py');p.write_text(text);mut=load(p,'eq8');pairs=[]
    if func=='ghep_job':
        for jobs in ({},{'j':{}},{'j':{'name':'Build'}},{'j':{'name':'Build'},'k':{'name':'Build'}},{'j':{'name':'Xây dựng'}}):
            for name in ('j','k','Build','Build (ubuntu-24.04)','Xây dựng'):
                pairs.append((head.ghep_job(name,{'jobs':jobs}),mut.ghep_job(name,{'jobs':jobs})))
    elif func=='chan_buoc':
        for prev in ({},{'uses':'./a'},{'run':None},{'run':''},{'run':0},{'run':'echo GITHUB_ENV'},{'run':'echo GITHUB_PATH'}):
            wf={'jobs':{'j':{'steps':[prev,{'run':'python x.py'}]}}};pairs.append((head.chan_buoc(wf,'j',1),mut.chan_buoc(wf,'j',1)))
    elif func=='tach_buoc':
        for body in ([],t.buoc(t.X,'THU: 4/4 dat'),t.khoi([t.X,t.X],'THU: 4/4 dat'),t.buoc('echo x'),t.buoc(t.X) + t.buoc(t.X,'x')):
            pairs.append((head.tach_buoc(body),mut.tach_buoc(body)))
    else:
        strings=['python x.py','python x.py\n','python x.py\n\n','python x.py\\','python x.py\\\n','python x.py\\\n\n','\npython x.py\n','python x.py\npython y.py','echo x','']
        strings += [''.join(z) for n in range(5) for z in itertools.product('x \\\n',repeat=n)]
        for run in strings:
            wf={'jobs':{'j':{'steps':[{'run':run}]}}};b={'lenh':run.split('\n')[0],'hop_le':True,'in_lai':run.rstrip('\n').split('\n'),'phan':['OK']}
            args=([b],{'x.py':'OK'},lambda a,b:True,wf,[('j',0)])
            pairs.append((head.do_dau_duong(*args),mut.do_dau_duong(*args)))
    unequal=[{'head':a,'mutant':b} for a,b in pairs if a!=b];results.append({'id':mid,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'proof':proof,'pairs':len(pairs),'unequal':unequal})
(R/'equivalence8-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2));assert all(not x['unequal'] for x in results)
