import ast, hashlib, importlib.util, json, pathlib
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t9',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();tr=ast.parse(src);f=next(n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='do_dau_duong')
n=list(ast.walk(f))[262];before=ast.unparse(n);assert before=="run.rstrip('\\n')"
n.args.pop();after=ast.unparse(n);mut=ast.unparse(ast.fix_missing_locations(tr));compile(mut,'<gap9>','exec')
p=R/'gap9-drop-single.py';p.write_text(mut);allcases=t._tat_ca_ca(p)
run=t.X+chr(92)+' '+chr(10);body=t.buoc(run.rstrip(chr(10)),'THU: 4/4 dat')
rows=[]
for label,path in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
 t.MA=path
 pv=t.g1(t.wf_tu(run.rstrip(chr(10))),body,w_rest=t.wf_tu(run.rstrip(chr(10))))
 rows.append({'source':label,'gate':t.gate(pv)['trang_thai'],'ghep':t.gate(pv)['ghep_buoc'],'markers':t.gate(pv)['dau_duong']})
report={'node_type':'Call (one positional argument)','mutation':'delete the optional argument of the second run.rstrip',
        'before':before,'after':after,'source_sha256':hashlib.sha256(mut.encode()).hexdigest(),
        'closed_operator_available':False,
        'input_run_repr':repr(run),'input_run_utf8_sha256':hashlib.sha256(run.encode()).hexdigest(),'all_cases':allcases,'proof':rows}
(R/'gap9-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='all_cases'},ensure_ascii=False,indent=2));print('ALL',len(allcases),'GREEN',sum(rc==0 for _,rc,_ in allcases))
assert len(allcases)==52 and all(rc==0 for _,rc,_ in allcases)
assert rows[0]['markers']==[] and rows[0]['gate']=='not_measured' and rows[1]['markers'][0]['trang_thai']=='passed'
