import importlib.util, pathlib, os, subprocess, sys
K=pathlib.Path('/home/user/rv773')
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
MA=os.environ.get('LAND_EVIDENCE_NGUON_MA',str(K/'ops/land_evidence_nguon.py'))
def check(hs):
 with t.cay(hs,{'a.json':'{}'}) as g:
  r=subprocess.run([sys.executable,'-B',MA,'--root',str(g)],capture_output=True,text=True)
 t.bang(r.returncode==2 and r.stdout.rstrip().endswith('TỔNG: KHÔNG ĐO ĐƯỢC'),f'mong rc=2 + tổng kết, được rc={r.returncode}, stdout={r.stdout!r}, stderr cuối={r.stderr.splitlines()[-1:]}')
def r01_merge_duplicate():
 for hs in ["x: {<<: {a: 'measured — khong', a: ok}}\n","x: {<<: {null: 'measured — khong', null: ok}}\n"]:check(hs)
def r04_yaml_date():
 for hs in ['x: 2026-02-30\n','pre_merge_checks: [2026-99-16T02:00:00Z]\n']:check(hs)
if __name__=='__main__':
 name=sys.argv[-1]
 try:globals()[name]()
 except t.TinHieuChotCa as e:
  print(f'DO:{name}:{e}');sys.exit(3)
