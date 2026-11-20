import pathlib,importlib.util,json
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(r/'ops/gate_output_doi_chieu_test.py','t');g=t.G(); variants={x['id']:x for x in map(json.loads,(w/'independent_mutants.jsonl').read_text().splitlines())};rows=[]
for i,fx in enumerate(['T-v1-pass','T-v2-pass','T-v3-pass']):
 n='producer_version_'+str(i);p=w/'contrast_modules'/(n+'.py');p.write_text(variants[n]['src']);m=load(p,n)
 parsed,_=g.doc_danh_gia((r/t.FX[fx][0]).read_bytes());count=len(parsed['jobs']);v3=i==2;ft,fp=t._them_skip('v3' if v3 else 'cu',f'MOC_GATE_OUTPUT: {"not_measured" if v3 else "passed"} ({count}/{count+int(v3)} job co dau hieu duong)')
 with t.mini(fx,ft,fp) as (f,d):
  a,b=g.kiem_tep(f,d),m.kiem_tep(f,d);row={'id':n,'original':a,'mutant':b,'different':a!=b};rows.append(row);print(row)
(w/'producer_contrasts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
