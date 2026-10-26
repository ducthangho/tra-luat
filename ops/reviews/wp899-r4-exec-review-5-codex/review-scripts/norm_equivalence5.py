from pathlib import Path
import sys,importlib.util,json,yaml
R=Path(__file__).resolve().parent;root=R.parent
src=(root/'ops/ci_provenance.py').read_text();old='dong_logic(run.rstrip("\\n").split("\\n"))';new='dong_logic(run.strip().split("\\n"))';assert src.count(old)==1
p=R/'norm_equivalent.py';p.write_text(src.replace(old,new))
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[]
for run in (t.X,'  '+t.X,t.X+'  ','\n'+t.X,t.X+'\n\n','\n\n'+t.X+'\n','\t'+t.X+'\t',t.X+'\\\n',t.X+'\n'+'python ops/khac.py',t.X+'\n   \n',t.X+'\r\n'):
 v=[]
 for source in (root/'ops/ci_provenance.py',p):
  t.MA=source;b=t.khoi(run.rstrip('\n').split('\n'),'THU: 4/4 dat');pr=t.g1(t.wf_tu(t.X,buoc_them={'run':run}),b)
  v.append(t.gate(pr))
 rows.append({'run':run,'equal':v[0]==v[1],'head':v[0],'mutant':v[1]})
assert all(v['equal'] for v in rows)
(R/'norm-equivalence5.json').write_text(json.dumps({'cases':rows,'proof':'dong_logic strips every completed logical line and goi ignores empty logical lines. Leading/trailing whitespace only changes those discarded/stripped characters. The raw run must first match the printed block; that equality is not mutated.'},ensure_ascii=False,indent=2));print('equivalence',len(rows),'/',len(rows))
