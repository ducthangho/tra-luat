from pathlib import Path
import json,os,subprocess,sys
R=Path(__file__).resolve().parent;root=R.parent;src=(root/'ops/ci_provenance.py').read_text();out=R/'reanchored6';out.mkdir(exist_ok=True);rows=[]
for name,old,new,case in [
 ('time_drop_type','if type(v) is str and RE_GIO.fullmatch(v) else None','if RE_GIO.fullmatch(v) else None','c38_ghep_lech_gio'),
 ('mode_env_job_presence','_env_chan(j) or','("env" in j) or','c46_mien_che_do'),
 ('log_group_close_exact_backward','if t == "##[endgroup]":','if t.startswith("##[endgroup]"):','c47_bien_ghep')]:
 assert src.count(old)==1;path=out/(name+'.py');path.write_text(src.replace(old,new));pair=[]
 for label,ma in [('baseline',root/'ops/ci_provenance.py'),('mutant',path)]:
  cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',case];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(ma),PYTHONDONTWRITEBYTECODE='1'));pair.append({'source':label,'command':cmd,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
 rows.append({'name':name,'old':old,'new':new,'case':case,'pair':pair,'rank':'GIET' if pair[0]['rc']==0 and pair[1]['rc']==3 and pair[1]['output'].startswith('DO:'+case+':') else 'KHONG_CHUNG_MINH'});print(name,rows[-1]['rank'],flush=True)
(R/'reanchored6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));assert all(r['rank']=='GIET' for r in rows)
