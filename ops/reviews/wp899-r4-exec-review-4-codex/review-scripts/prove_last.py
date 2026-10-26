from pathlib import Path
import os,subprocess,json,sys
R=Path(__file__).resolve().parent
p=R/'frontier_cases.py';s=p.read_text();anchor=" if label=='run_trailing_space':"
s=s.replace(anchor,""" if label=='nonstr_no_throw':
  w=t.wf_tu(x,buoc_them={'name':'K','run':5})
  try:p=t.g1(w,t.buoc('5','THU: 4/4 dat'),sua=lambda st:st[2].update(name='K'),w_rest=t.wf_tu(x))
  except Exception as e:t.bang(False,'non-string run must remain unverified without throwing: '+type(e).__name__)
  g=t.gate(p);t.bang(t.ghep(p)=='passed' and g['dau_duong']==[] and g['kich_ban']['buoc_xac_thuc']==0,str(g));return g
 elif label=='run_trailing_space':""")
p.write_text(s)
rows=[]
for folder,name,case in [('frontier','run_type_coerce','nonstr_no_throw'),('frontier2','number_type_bool_guard_drop','number_bool_metadata')]:
 for path in (None,R/folder/(name+'.py')):
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  if path:env['CI_PROVENANCE_MA']=str(path)
  cmd=[sys.executable,'-B',str(p),case];q=subprocess.run(cmd,capture_output=True,env=env)
  rows.append({'mutant':name,'case':case,'source':str(path) if path else 'HEAD','command':cmd,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
  print(name,case,'mutant' if path else 'HEAD',q.returncode)
  assert q.returncode==(3 if path else 0)
old=json.loads((R/'frontier-counterexamples.json').read_text());(R/'frontier-counterexamples.json').write_text(json.dumps(old+rows,ensure_ascii=False,indent=2))
