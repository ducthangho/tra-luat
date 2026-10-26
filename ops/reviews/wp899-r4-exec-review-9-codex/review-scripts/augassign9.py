import ast, hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t9',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();tr=ast.parse(src);f=next(n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='do_dau_duong')
n=next(n for n in ast.walk(f) if isinstance(n,ast.AugAssign));old=ast.unparse(n);t._thay(n,ast.Assign(targets=[n.target],value=n.value))
mut=ast.unparse(ast.fix_missing_locations(tr));p=R/'augassign9-mutant.py';p.write_text(mut)
cmd=[sys.executable,'-B',str(R/'closed8.py'),'child',str(p),'do_dau_duong'];z=subprocess.run(cmd,capture_output=True)
rows=json.loads(z.stdout)['cases'];kill=[c for c,rc,d in rows if rc==3 and d.startswith(f'DO:{c}:')]
proof=[]
for name,path in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
 t.MA=path;pv=t.g1(t.wf_tu(t.X,t.X),t.buoc(t.X,'THU: 4/4 dat'),t.buoc(t.X,'THU: 4/4 dat'))
 proof.append({'source':name,'ghep':t.gate(pv)['ghep_buoc'],'kich_ban':t.gate(pv)['kich_ban'],'markers':t.gate(pv)['dau_duong']})
report={'before':old,'after':'so = 1','node':'AugAssign','source_sha256':hashlib.sha256(mut.encode()).hexdigest(),
        'rank':'GIET' if kill else 'TIN_DUNG_GIA' if any(rc for _,rc,_ in rows) else 'SONG','command':cmd,'rc':z.returncode,
        'cases':rows,'proof':proof,'stdout':z.stdout.decode(),'stderr':z.stderr.decode()}
(R/'augassign9-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ('cases','stdout','stderr')},ensure_ascii=False,indent=2))
