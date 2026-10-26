from pathlib import Path
import ast,sys,os,json,subprocess
R=Path(__file__).resolve().parent;root=R.parent;src=(root/'ops/ci_provenance.py').read_text();out=R/'frontier6-extra';out.mkdir(exist_ok=True);known=set()
base=json.loads((R/'frontier6/baseline.json').read_text());assert len(base)==49 and all(rc==0 for c,rc,o in base)
nodes=[n for n in ast.parse((R/'frontier6.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ('cases','one')]
exec(compile(ast.Module(body=nodes,type_ignores=[]),'frontier6-functions','exec'))
r=one(('rest_number_min_one_safe','len({s["number"] for s in st}) == len(st)','len({s["number"] for s in st}) == len(st) and (not st or min(s["number"] for s in st) == 1)'))
(out/'results.json').write_text(json.dumps([r],ensure_ascii=False,indent=2));print(r['name'],r['rank'],r.get('killed'),r.get('other_errors'))
