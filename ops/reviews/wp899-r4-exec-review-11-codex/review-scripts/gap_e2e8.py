import importlib.util, json, pathlib
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t);rows=[]
for label,p in [('head',root/'ops/ci_provenance.py'),('mutant',R/'gap8-drop-recursion.py')]:
    t.MA=p
    try:
        pv=t.g1('['*600+'0'+']'*600,t.buoc(t.X,'THU: 4/4 dat'),w_rest=t.wf_tu(t.X));answer={'gate':t.gate(pv)['trang_thai'],'ghep_buoc':t.gate(pv)['ghep_buoc'],'markers':t.gate(pv)['dau_duong']}
    except Exception as e:answer={'exception':type(e).__name__,'message':str(e)}
    rows.append({'source':label,'answer':answer})
(R/'gap-e2e8-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(rows,indent=2));assert rows[0]['answer']['gate']=='not_measured' and rows[1]['answer']['exception']=='RecursionError'
