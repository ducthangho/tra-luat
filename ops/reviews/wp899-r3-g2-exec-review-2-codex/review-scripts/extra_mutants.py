import sys,os,json,importlib.util,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('te',root/'ops/ci_provenance_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text(); out=R/'extra-mutants'; out.mkdir(exist_ok=True)
mutants=[('git_ignore_sha','f"{sha}:{path}"','f"HEAD:{path}"'),('git_always_unavailable','return r.stdout.decode("utf-8") if r.returncode == 0 else None','return None')]
rows=[]
for name,old,new in mutants:
 assert src.count(old)==1
 p=out/(name+'.py'); p.write_text(src.replace(old,new))
 row={'name':name,'old':old,'new':new,'cases':[]}
 for case in t.CA:
  cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',case]
  r=subprocess.run(cmd,env=dict(os.environ,CI_PROVENANCE_MA=str(p),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=300)
  row['cases'].append({'case':case,'command':cmd,'rc':r.returncode,'output':(r.stdout+r.stderr).decode('utf8','replace')})
 row['rank']='SONG_SOT' if all(c['rc']==0 for c in row['cases']) else 'CHECK_OUTPUT'
 rows.append(row); (out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 print(name,row['rank'],sum(c['rc']==0 for c in row['cases']),len(row['cases']),flush=True)
