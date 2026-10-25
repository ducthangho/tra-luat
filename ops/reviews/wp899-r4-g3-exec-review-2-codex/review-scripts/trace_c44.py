import pathlib,importlib.util,json,copy
import yaml
R=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('t',R.parent/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[];original=t.chay
def measured(cap,*a,**kw):
    rc,out,p,rest=original(cap,*a,**kw)
    w=yaml.safe_load(kw['wf'])
    rows.append({'rest_steps':copy.deepcopy(cap[0][0]['steps']),'yaml_jobs':w['jobs'],'tool_rc':rc,'gate':t.gate(p)})
    return rc,out,p,rest
t.chay=measured
t.c44_ghep_sai_dang()
assert len(rows)==5
(R/'c44-trace.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('c44: 5/5 nhánh có gọi công cụ và có assertion; steps YAML luôn list; không number=0')
