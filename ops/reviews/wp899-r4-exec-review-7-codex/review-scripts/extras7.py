from pathlib import Path
import json,subprocess,sys,os
R=Path(__file__).resolve().parent;root=R.parent;rs=[]
for name in ('extra6.py','extra6b.py','extra6c.py'):
 cmd=[sys.executable,'-B',str(R/name)];q=subprocess.run(cmd,capture_output=True);rs.append({'name':name,'command':cmd,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()})
src=(root/'ops/ci_provenance.py').read_text();a='len({s["number"] for s in st}) == len(st)';b=a+' and min(s["number"] for s in st) == 1';p=R/'contiguous7.py';p.write_text(src.replace(a,b))
for c in ('c22_thieu_dinh_danh_khong_passed','c50_mien_luot6'):
 for tag,ma in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
  cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',c];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(ma)));rs.append({'name':'contiguous-c22-c50','source':tag,'case':c,'command':cmd,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
(R/'extras7-results.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2));print(json.dumps(rs,ensure_ascii=False,indent=2))
