from pathlib import Path
import subprocess,json,os,sys
R=Path(__file__).resolve().parent;root=R.parent
for n in (1,2):(R/f'prior{n}/extra-r4').mkdir(exist_ok=True)
# Updated anchors only; retain the recorded raw invocation failures.
p=R/'frontier5.py';s=p.read_text().replace('bool(v[k])','bool(d["env"][k])');p.with_name('frontier5_current.py').write_text(s)
rows=[]
for n in (1,2):
 for name in ('rest_order','rest_duplicate','time_format','time_missing_header','invalid_calendar','github_path','expression_name','first_line'):
  c=[sys.executable,'-B',str(R/f'prior{n}/reviewer_cases_r4.py'),name];q=subprocess.run(c,capture_output=True);rows.append({'command':c,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()});assert q.returncode==0,rows[-1]
(R/'legacy-cli-repaired6.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('legacy CLI cases 16/16 DAT')
