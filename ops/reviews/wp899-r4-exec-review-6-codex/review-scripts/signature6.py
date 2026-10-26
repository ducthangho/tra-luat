from pathlib import Path
import os,sys,json,subprocess
R=Path(__file__).resolve().parent;root=R.parent;src=(root/'ops/ci_provenance.py').read_text();rows=[]
for name,old,new,case in [('n_env_v_truthy_current','return "env" in d and (','return bool(d.get("env")) and (','c46_mien_che_do'),('env_prefix_value_only_current','str(k).startswith("CI_DANG_KY_")','str(k).startswith("CI_DANG_KY_") and bool(d["env"][k])','c49_oracle_nhieu_truc')]:
 assert src.count(old)==1;p=R/(name+'.py');p.write_text(src.replace(old,new));pair=[]
 for tag,ma in [('baseline',root/'ops/ci_provenance.py'),('mutant',p)]:
  c=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',case];q=subprocess.run(c,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(ma),PYTHONDONTWRITEBYTECODE='1'));pair.append({'source':tag,'command':c,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
 rank='GIET' if pair[0]['rc']==0 and pair[1]['rc']==3 and pair[1]['output'].startswith('DO:'+case+':') else 'KHONG_CHUNG_MINH';rows.append({'name':name,'old':old,'new':new,'case':case,'rank':rank,'pair':pair});(R/'signature6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(name,rank,flush=True)
assert all(r['rank']=='GIET' for r in rows)
