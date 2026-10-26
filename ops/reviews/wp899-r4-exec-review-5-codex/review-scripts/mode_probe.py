from pathlib import Path
import importlib.util,json
import yaml
root=Path.cwd();s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[]
for scope in ('job','workflow'):
 for v in (None,False,0,[],{},'${{ inputs.e }}'):
  w=t.wf_tu(t.X,**{'job_them' if scope=='job' else 'goc_them':{'env':v}})
  p=t.g1(w,t.buoc(t.X,'THU: 4/4 dat'))
  rows.append({'scope':scope,'value':v,'yaml':w,'gate':t.gate(p)})
(Path('.review')/'mode-probes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for r in rows:print(r['scope'],repr(r['value']),r['gate']['trang_thai'],r['gate']['dau_duong'])
