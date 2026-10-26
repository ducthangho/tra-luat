from pathlib import Path
import json,ast,sys,subprocess,os,time
R=Path(__file__).resolve().parent;root=R.parent
expected=sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='add' for n in ast.walk(ast.parse((R/'frontier6.py').read_text())))
start=time.monotonic()
while True:
 try:a=json.loads((R/'frontier6/results.json').read_text())
 except (FileNotFoundError,ValueError):a=[]
 if len(a)==expected:break
 if time.monotonic()-start>3600:raise TimeoutError('frontier not complete')
 time.sleep(2)
a+=json.loads((R/'frontier6-extra/results.json').read_text())+json.loads((R/'frontier6-extra2/results.json').read_text())+json.loads((R/'frontier6-extra3/results.json').read_text())
rows=[]
for z in a:
 if z['rank']!='SONG_SOT' or z['name']=='env_only_keys_str':continue
 pair=[]
 for label,p in [('head',root/'ops/ci_provenance.py'),('mutant',Path(z['source']))]:
  c=[sys.executable,'-B',str(R/'cases6.py'),z['name']];q=subprocess.run(c,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(p),PYTHONDONTWRITEBYTECODE='1'),timeout=120)
  pair.append({'source':label,'path':str(p),'command':c,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
 good=pair[0]['rc']==0 and pair[1]['rc']==3 and pair[1]['output'].startswith('DO:'+z['name']+':')
 rows.append({'name':z['name'],'pair':pair,'proven':good});(R/'proof-final6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(z['name'],pair[0]['rc'],pair[1]['rc'],good,flush=True)
print('PROVEN',sum(z['proven'] for z in rows),'/',len(rows))
