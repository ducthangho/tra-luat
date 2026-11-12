"""Liet ke buoc cua ci.yml theo dieu kien che_do. Chay tu repo: python -I -B ../work/nhanh_yaml.py [sha]"""
import sys, re, subprocess, yaml
sha = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
t = subprocess.run(['git','show',f'{sha}:.github/workflows/ci.yml'],capture_output=True,text=True,check=True).stdout
wf = yaml.load(t, Loader=yaml.BaseLoader)
print('workflow env:', wf.get('env'), 'defaults:', wf.get('defaults'))
for k, j in wf['jobs'].items():
    st = j.get('steps', [])
    print(f'\n== {k}  runs-on={j.get("runs-on")} if={j.get("if")} strategy={ (j.get("strategy") or {}).get("matrix") } env={sorted((j.get("env") or {}).keys())}')
    for i, s in enumerate(st):
        cond = s.get('if', '')
        nm = s.get('name') or ('uses ' + s.get('uses','')) or s.get('run','')[:40]
        tag = 'NHANH' if re.search(r"==\s*'duong_nhanh'", cond) else ('DAYDU' if "!= 'duong_nhanh'" in cond else '-')
        ge = 'GITHUB_ENV/PATH' if re.search('GITHUB_(ENV|PATH)', str(s.get('run',''))) else ''
        print(f'  {i:2} {tag:5} {nm[:95]:95} shell={s.get("shell","-")} coe={s.get("continue-on-error","-")} env={sorted((s.get("env") or {}).keys()) if isinstance(s.get("env"),dict) else s.get("env")} {ge} if={cond[:80] if tag=="-" and cond else ""}')
