from pathlib import Path
import os,sys,json,subprocess
R=Path(__file__).resolve().parent
rows=[]
for m in json.loads((R/'frontier5/results.json').read_text()):
 if m['rank']!='SONG_SOT' or m['name']=='nested_only_after_shell':continue
 for source in (R.parent/'ops/ci_provenance.py', Path(m['source'])):
  cmd=[sys.executable,'-B',str(R/'cases5.py'),m['name']];env=dict(os.environ,CI_PROVENANCE_MA=str(source),PYTHONDONTWRITEBYTECODE='1')
  p=subprocess.run(cmd,capture_output=True,env=env);o=(p.stdout+p.stderr).decode('utf8','replace')
  rows.append({'mutant':m['name'],'source':str(source),'command':cmd,'rc':p.returncode,'output':o,'rank':'BASELINE_DAT' if source.name=='ci_provenance.py' and p.returncode==0 else 'GIET_DUNG_CA' if p.returncode==3 and o.startswith('DO:'+m['name']+':') else 'SETUP_OR_UNPROVEN'})
  print(m['name'],source.name,p.returncode,flush=True)
(R/'counterexamples5.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
