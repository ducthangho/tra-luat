import subprocess,pathlib,json,sys,os
R=pathlib.Path('.review').resolve();rows=[]
for n in (1,2):
 for case in ('r4_F02_env_metadata','r4_F02_mixed_color','F02_collision_other_job','F02_missing_endgroup','git_workflow_source','control_simple'):
  cmd=[sys.executable,'-B',str(R/f'old{n}/review_cases.py'),case];p=subprocess.run(cmd,capture_output=True)
  rows.append({'round':n,'case':case,'command':cmd,'rc':p.returncode,'output':(p.stdout+p.stderr).decode()})
 for script in ('r4_compare.py',)+ (('composite_case.py','boundary_case.py') if n==2 else ()):
  cmd=[sys.executable,'-B',str(R/f'old{n}/{script}')];p=subprocess.run(cmd,capture_output=True); rows.append({'round':n,'script':script,'command':cmd,'rc':p.returncode,'output':(p.stdout+p.stderr).decode()})
(R/'old-cases-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for r in rows:print(r.get('case',r.get('script')),r['round'],r['rc'],r['output'][-150:])
