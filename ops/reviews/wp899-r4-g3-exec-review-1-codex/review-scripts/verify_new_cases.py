import subprocess,sys,pathlib,json,os
R=pathlib.Path(__file__).resolve().parent
pairs=[('rest_order','sort_bi_bo'),('rest_duplicate','kiem_number_bi_bo'),('time_format','gio_nhan_offset'),('time_missing_header','gio_thieu_header_lay_rest'),('github_path','env_bo_PATH'),('expression_name','ten_name_khong_kiem_bieu_thuc'),('first_line','ten_run_lstrip')]
res=[]
for case,mut in pairs+[('invalid_calendar',None)]:
 for source in [None]+([mut] if mut else []):
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  if source:env['CI_PROVENANCE_MA']=str(R/f'extra-r4/{source}.py')
  cmd=[sys.executable,'-B',str(R/'reviewer_cases_r4.py'),case];p=subprocess.run(cmd,capture_output=True,env=env)
  res.append({'case':case,'source':source or 'candidate','command':cmd,'rc':p.returncode,'output':(p.stdout+p.stderr).decode()})
(R/'reviewer-cases-r4.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
for r in res:print(r['case'],r['source'],r['rc'],r['output'][:120])
