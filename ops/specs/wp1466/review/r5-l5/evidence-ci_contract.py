from pathlib import Path
import subprocess,sys,json,os
O=Path(__file__).resolve().parent
code="""import sys,json;sys.dont_write_bytecode=True;sys.path.insert(0,'.claude/dev');import ci_dang_ky_test as c;print(json.dumps({'registry':c.kiem(),'ruff_contract':c.loi_ruff_ci()},ensure_ascii=False))"""
for tree in ['base','prototype','master']:
 r=subprocess.run([sys.executable,'-B','-c',code],cwd=O/tree,capture_output=True,text=True);print(tree,'rc',r.returncode,r.stdout.strip(),r.stderr.strip())
