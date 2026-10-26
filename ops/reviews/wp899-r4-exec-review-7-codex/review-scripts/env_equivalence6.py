from pathlib import Path
import datetime,importlib.util,yaml,json
R=Path(__file__).resolve().parent;root=R.parent
def load(p):
 s=importlib.util.spec_from_file_location('env_equivalence',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
head=load(root/'ops/ci_provenance.py');mut=load(R/'frontier6/env_only_keys_str.py')
keys=['A','CI_DANG_KY_','CI_DANG_KY_X','ci_dang_ky_X',None,True,False,1,0,-1,1.5,float('inf'),float('nan'),b'CI_DANG_KY_X',datetime.date(2026,10,25),datetime.datetime(2026,10,25,10,0,tzinfo=datetime.timezone.utc)]
rows=[]
for k in keys:
 d=yaml.safe_load(yaml.safe_dump({'env':{k:'x'}}));a,b=head._env_chan(d),mut._env_chan(d);rows.append({'key_type':type(next(iter(d['env']))).__name__,'key_repr':repr(next(iter(d['env']))),'head':a,'mutant':b,'equal':a==b})
assert all(r['equal'] for r in rows)
reason='yaml.safe_load standard hashable mapping keys are plain str, bool, int, float, None, bytes, date/datetime; collections are unhashable and arbitrary Python objects are not constructed. For non-str keys, str(key) cannot start CI_DANG_KY_; for str keys both predicates are identical. The outer non-dict and key-presence guards are unchanged. This is a semantic argument on the YAML input domain, not a claim based only on these16 samples.'
(R/'env-equivalence6-results.json').write_text(json.dumps({'rows':rows,'argument':reason},ensure_ascii=False,indent=2));print('ENV EQUIVALENCE',len(rows),'/',len(rows));print(reason)
