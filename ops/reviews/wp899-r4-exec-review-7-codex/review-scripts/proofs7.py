from pathlib import Path
import runpy,subprocess,sys,os,json,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent;g=runpy.run_path(str(R/'frontier7.py'));out=R/'proof7';out.mkdir(exist_ok=True);src=g['src']
def one(z):
 n,a,b=z
 if src.count(a)!=1:return {'name':n,'rank':'HONG_NEO'}
 p=out/(n+'.py');p.write_text(src.replace(a,b));rs=[]
 for label,ma in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
  cmd=[sys.executable,'-B',str(R/'cases7.py'),n];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(ma),PYTHONDONTWRITEBYTECODE='1'),timeout=120)
  rs.append({'label':label,'source':str(ma),'command':cmd,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
 rank='PROVEN' if rs[0]['rc']==0 and rs[1]['rc']==3 and rs[1]['output'].startswith('DO:'+n+':') else 'BASELINE_ERROR' if rs[0]['rc'] else 'NO_DELTA' if rs[1]['rc']==0 else 'TIN_DUNG_GIA'
 return {'name':n,'old':a,'new':b,'pair':rs,'rank':rank}
rs=[]
with concurrent.futures.ThreadPoolExecutor(3) as ex:
 for r in ex.map(one,g['M']):
  rs.append(r);(R/'proof7-results.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2));print(r['name'],r['rank'],flush=True)
print(collections.Counter(z['rank'] for z in rs))
