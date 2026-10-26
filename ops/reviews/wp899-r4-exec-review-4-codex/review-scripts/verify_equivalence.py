from pathlib import Path
import os,sys,importlib.util,contextlib,json
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();old='and not t.startswith("##[group]") and (';new='and not (t.startswith("##[group]") and not b["tien_to"]) and ('
assert src.count(old)==1
p=R/'nested_after_equivalent.py';p.write_text(src.replace(old,new))
rows=[]
for pos in range(6):
 pair=[]
 for source in (root/'ops/ci_provenance.py',p):
  t.MA=source;b=t.buoc(t.X,'THU: 4/4 dat');b.insert(pos,t.T+' ##[group]details')
  pair.append(t.gate(t.g1(t.wf_tu(t.X),b)))
 rows.append({'position':pos,'equal':pair[0]==pair[1],'outputs':pair})
assert all(z['equal'] for z in rows)
logs=list((root/'.review-input/log-that').rglob('*.log'))
lines=[t.nap().than(z) for f in logs for z in f.read_text().splitlines() if '##[endgroup]' in z]
out={'nested_positions':rows,'endgroup_lines':len(lines),'exact_endgroup':sum(z=='##[endgroup]' for z in lines),'full_logs':len(logs),'proof':'Before shell, an uncolored nested group makes not tien_to or shell-prefix false regardless of the nested-group predicate. After shell, both predicates reject nested groups. Colored lines before shell follow the same separate branch in both implementations.','obsolete_anchor_count':src.count('if t.startswith("##[endgroup]"):')}
(R/'equivalence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('nested:',sum(z['equal'] for z in rows),'/',len(rows),'endgroup:',out['exact_endgroup'],'/',out['endgroup_lines'],'on',len(logs),'logs')
