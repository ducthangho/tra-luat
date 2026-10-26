from pathlib import Path
import ast,sys,os,json,subprocess
R=Path(__file__).resolve().parent;root=R.parent
norm=ast.literal_eval(ast.parse((R/'mau_chuan_hoa.py').read_text()).body[0].value)
s=ast.parse((root/'ops/ci_provenance_test.py').read_text());catalog=None
for n in s.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DOT_BIEN' for t in n.targets):catalog=ast.literal_eval(n.value)
known={(a,b):(name,pref) for name,a,b,pref in catalog};src=(root/'ops/ci_provenance.py').read_text();out=R/'normalization6';out.mkdir(exist_ok=True);rows=[]
for name,old,new in norm:
 if '_env_chan(wf.get("env"))' in old:old=old.replace('_env_chan(wf.get("env"))','_env_chan(wf)');new=new.replace('_env_chan(wf.get("env"))','_env_chan(wf)')
 if old not in src and 'str(k).startswith("CI_DANG_KY_") for k in v' in old:
  old=old.replace('for k in v','for k in d["env"]');new=new.replace('for k in v','for k in d["env"]')
 if old not in src and 'return v is not None and (' in old:
  old=old.replace('return v is not None and (','return "env" in d and (');new=new.replace('v is not None','"env" in d').replace('type(v)','type(d["env"])').replace('bool(v)','bool(d["env"])')
 if src.count(old)!=1:rows.append({'name':name,'rank':'HONG_NEO','old':old,'new':new});continue
 raw=known.get((old,new));pref=raw[1] if raw else 'c48'
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);c=next(k for k in t.CA if k.split('_')[0]==%r);r,o=t.chay_ca(c);print(json.dumps([c,r,o]))"%(str(root/'ops/ci_provenance_test.py'),pref)
 p=out/(name+'.py');p.write_text(src.replace(old,new));pair=[]
 for tag,ma in [('baseline',root/'ops/ci_provenance.py'),('mutant',p)]:
  q=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(ma),PYTHONDONTWRITEBYTECODE='1'))
  pair.append({'source':tag,'rc':q.returncode,'case':json.loads(q.stdout) if q.returncode==0 else ['import',4,q.stderr.decode()]})
 c,rc,o=pair[1]['case'];rank='GIET' if pair[0]['case'][1]==0 and rc==3 and o.startswith('DO:'+c+':') else 'TIN_DUNG_GIA' if rc not in (0,3) else 'SONG_SOT'
 rows.append({'name':name,'old':old,'new':new,'catalogue':raw,'pair':pair,'rank':rank});(R/'normalization6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(name,rank,flush=True)
(R/'normalization6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
