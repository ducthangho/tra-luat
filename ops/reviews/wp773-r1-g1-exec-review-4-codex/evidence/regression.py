import importlib.util,subprocess,sys,os,json
from pathlib import Path
K=Path('/home/user/rv773'); O=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
MA=Path(os.environ.get('LAND_EVIDENCE_NGUON_MA',str(t.MA)))
def r06():
 with t.cay("x: 'measured — a.json'\n",{'a.json':'{}'}) as root:
  f=root/'ops/land'/t.TEN
  for rt,fp in [(str(root),'ops/land/'+t.TEN),('.', 'ops/land/'+t.TEN), (str(root),str(f)), ('.',str(f))]:
   r=subprocess.run([sys.executable,'-B',str(MA),'--root',rt,'--tep',fp],cwd=root,capture_output=True,text=True)
   t.bang(r.returncode==0 and r.stdout.rstrip().endswith('TỔNG: ĐẠT'),f'--root {rt} --tep {fp}: rc={r.returncode}, stdout={r.stdout!r}, stderr={r.stderr[-400:]!r}')
if __name__=='__main__':
 try:r06()
 except t.TinHieuChotCa as e: print('DO:r06_cli_absolute:'+str(e));sys.exit(3)
 except Exception as e: print('HONG:r06_cli_absolute:'+repr(e));sys.exit(4)
