from pathlib import Path
import json,subprocess,sys,os
R=Path(__file__).resolve().parent;root=R.parent;rs=[]
for n,p in [('job_suffix_no_dot_pure',R/'frontier7b/job_suffix_no_dot_pure.py'),('name_run_strip_cr',R/'proof7/name_run_strip_cr.py'),('name_run_crlf_first_line',R/'frontier7b/name_run_crlf_first_line.py')]:
 a=[]
 for tag,ma in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
  cmd=[sys.executable,'-B',str(R/'cases7.py'),n];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(ma)));a.append({'label':tag,'source':str(ma),'command':cmd,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
 rs.append({'name':n,'pair':a,'rank':'PROVEN' if a[0]['rc']==0 and a[1]['rc']==3 and a[1]['output'].startswith('DO:'+n+':') else 'NOT_PROVEN'})
(R/'proof-repairs7-results.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2));print(json.dumps(rs,ensure_ascii=False,indent=2))
