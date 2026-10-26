import ast, hashlib, importlib.util, json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('test8',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();tr=ast.parse(src);fn=next(x for x in tr.body if isinstance(x,ast.FunctionDef) and x.name=='doc_wf')
handler=next(x for x in ast.walk(fn) if isinstance(x,ast.ExceptHandler));before=ast.unparse(handler.type)
handler.type.elts.pop(1);after=ast.unparse(handler.type);mut=ast.unparse(ast.fix_missing_locations(tr));compile(mut,'<gap8>','exec')
p=R/'gap8-drop-recursion.py';p.write_text(mut)
full=t._tat_ca_ca(p);(R/'gap8-all52.json').write_text(json.dumps(full,ensure_ascii=False,indent=2))
inputs=[('nested_yaml', '['*600+'0'+']'*600),('invalid_yaml','jobs: [')]
rows=[]
for label,path in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
    t.MA=path;m=t.nap()
    for name,value in inputs:
        try: result=m.doc_wf(value);answer={'return':result}
        except Exception as e:answer={'exception':type(e).__name__,'message':str(e)}
        rows.append({'source':label,'input':name,'input_bytes':len(value.encode()),'input_sha256':hashlib.sha256(value.encode()).hexdigest(),'answer':answer})
report={'ast_node':'ExceptHandler.type Tuple','before':before,'after':after,'first_order':'delete one handled exception','source_sha256':hashlib.sha256(mut.encode()).hexdigest(),'all_cases':len(full),'all_green':len(full)==52 and all(rc==0 for _,rc,_ in full),'proof':rows}
(R/'gap8-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
assert not report['all_green'] and any(rc==3 and d.startswith('DO:'+c+':') for c,rc,d in full)
assert rows[0]['answer']=={'return':None} and rows[2]['answer'].get('exception')=='RecursionError'
