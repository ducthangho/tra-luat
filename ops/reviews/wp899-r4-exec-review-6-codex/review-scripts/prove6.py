from pathlib import Path
import sys,os,json,subprocess
R=Path(__file__).resolve().parent;root=R.parent
names=sys.argv[1:] or [r['name'] for r in json.loads((R/'frontier6/results.json').read_text()) if r['rank']=='SONG_SOT']
rows=[]
for name in names:
 pair=[]
 for tag,path in [('head',root/'ops/ci_provenance.py'),('mutant',next(p for d in ('frontier6','frontier6-extra','frontier6-extra2','frontier6-extra3') for p in [R/d/(name+'.py')] if p.exists()))]:
  cmd=[sys.executable,'-B',str(R/'cases6.py'),name];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(path),PYTHONDONTWRITEBYTECODE='1'))
  o=(q.stdout+q.stderr).decode();pair.append({'source':tag,'path':str(path),'command':cmd,'rc':q.returncode,'output':o})
 rows.append({'name':name,'pair':pair,'proven':pair[0]['rc']==0 and pair[1]['rc']==3 and pair[1]['output'].startswith('DO:'+name+':')})
 print(name,pair[0]['rc'],pair[1]['rc'],rows[-1]['proven'],flush=True)
(R/('proof6'+('-'+sys.argv[1] if len(sys.argv)==2 else '')+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2))
