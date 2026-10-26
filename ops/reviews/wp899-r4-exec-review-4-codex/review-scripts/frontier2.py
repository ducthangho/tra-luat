from pathlib import Path
import ast,sys,os,json,subprocess,importlib.util,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('ct',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();out=R/'frontier2';out.mkdir(exist_ok=True)
M=[
('mode_defaults_wf_truthy', '"defaults" in wf or', 'bool(wf.get("defaults")) or'),
('mode_defaults_job_truthy', 'or "defaults" in j or', 'or bool(j.get("defaults")) or'),
('mode_env_truthy', 'return v is not None and (type(v) is not dict', 'return bool(v) and (type(v) is not dict'),
('mode_env_string_only', 'type(v) is not dict or any(str(k)', 'type(v) is str or any(str(k)'),
('number_type_bool_guard_drop','type(s) is dict and _so(s.get("number"), 1)', 'type(s) is dict and isinstance(s.get("number"), int) and s["number"] >= 1'),
('number_min_strict','_so(s.get("number"), 1)', '_so(s.get("number"), 2)'),
('header_time_other_group','(h := _gio(b["gio"]))','(h := _gio(buoc[0]["gio"]))'),
('header_window_other_step','_gio(ung[i].get("started_at"))','_gio(ung[0].get("started_at"))'),
('time_current_end_other_step','_gio(ung[i].get("completed_at"))','_gio(ung[0].get("completed_at"))'),
('name_only_first_rest','for s, y in zip(ung, sy)):', 'for s, y in list(zip(ung, sy))[:1]):'),
('name_only_last_rest','for s, y in zip(ung, sy)):', 'for s, y in list(zip(ung, sy))[-1:]):'),
]

# Compare against the executor's two immutable mutation inventories; don't call a duplicate a new probe.
executed=[]
for name in ('tu_dot_bien.py','tu_dot_bien2.py'):
 tree=ast.parse((root/'.review-input/tu-dot-bien'/name).read_text())
 for node in ast.walk(tree):
  if isinstance(node,ast.Tuple) and len(node.elts)==3:
   try:v=ast.literal_eval(node)
   except Exception:continue
   if all(isinstance(x,str) for x in v):executed.append(v)
known={(o,n) for _,o,n in executed}
M=[(name,o,n, (o,n) not in known) for name,o,n in M]
def cases(path):
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))"%str(root/'ops/ci_provenance_test.py')
 cmd=[sys.executable,'-B','-c',code]
 p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(path)),timeout=600)
 return p,json.loads(p.stdout)
p,baseline=cases(root/'ops/ci_provenance.py');assert all(rc==0 for c,rc,o in baseline)
(out/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2))
def one(v):
 name,old,new,isnew=v;rec={'name':name,'old':old,'new':new,'new_vs_executor':isnew,'count':src.count(old)}
 if src.count(old)!=1:return rec|{'rank':'HONG_NEO'}
 path=out/(name+'.py');path.write_text(src.replace(old,new));p,res=cases(path)
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 killed=[c for c,rc,o in res if rc==3 and o.startswith('DO:'+c+':')];bad=[{'case':c,'rc':rc,'output':o} for c,rc,o in res if rc and not (rc==3 and o.startswith('DO:'+c+':'))]
 return rec|{'rc':p.returncode,'rank':'GIET' if killed else 'TIN_DUNG_GIA' if bad else 'SONG_SOT','killed':killed,'other_errors':bad,'cases':res}
rows=[]
with concurrent.futures.ThreadPoolExecutor(4) as ex:
 for v in ex.map(one,M):
  rows.append(v);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(v['name'],v['rank'],v.get('killed'), 'OTHER',len(v.get('other_errors',[])),flush=True)
print(collections.Counter(r['rank'] for r in rows))
