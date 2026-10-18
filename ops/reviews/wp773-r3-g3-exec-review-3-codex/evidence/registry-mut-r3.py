import pathlib,subprocess,os
r=pathlib.Path('/tmp/rv778-review');p=r/'.claude/dev/ci_dang_ky_test.py';src=p.read_text();line=next(x for x in src.splitlines(True) if '"ops/land_evidence_nguon_test.py":' in x)
env=dict(os.environ,GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
for name,new in [('drop',''),('path',line.replace('ops/land_evidence_nguon_test.py','ops/no_such_test.py')),('pattern','    "ops/land_evidence_nguon_test.py": r"NEVER_MATCH",\n'),('no_DO',line.replace(r'(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b)','')),('no_end',line.replace(r'\Z',''))]:
 try:
  p.write_text(src.replace(line,new));q=subprocess.run(['python3.13','-B',str(p)],cwd=r,env=env,capture_output=True,text=True);print(name,'rc',q.returncode,'\n'+'\n'.join(x for x in q.stdout.splitlines() if 'chưa đăng ký' in x or 'không có tệp' in x or 'PHẢN CHỨNG:' in x or x.startswith('TỔNG:')),flush=True)
 finally:p.write_text(src)
