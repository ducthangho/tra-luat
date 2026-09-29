import concurrent.futures, pathlib, subprocess, sys
out=pathlib.Path(__file__).resolve().parent; root=pathlib.Path.cwd()
jobs=[]
for v in ('3.10','3.11','3.12','3.13'):
 jobs.append(('suite-'+v,[f'python{v}','-B','.claude/dev/doc_receipt_thu_hoi_test.py']))
 for name in ('runtime_isolated','runtime_depth','focused_controls'):
  jobs.append((name+'-'+v,[f'python{v}','-B',str(out/(name+'.py')),str(root)]+(['receipt'] if name=='focused_controls' else [])))
for label,prefix in [('zero',['env','PYTHONINTMAXSTRDIGITS=0','python3.12','-B']),('x640',['python3.12','-X','int_max_str_digits=640','-B'])]:
 jobs.append(('suite-'+label,prefix+['.claude/dev/doc_receipt_thu_hoi_test.py']))
 for name in ('import_effect','executor_restore_chk'):
  jobs.append((name+'-'+label,prefix+[str(out/(name+'.py')),str(root)]))
 jobs.append(('limit-'+label,prefix+[str(out/'focused_controls.py'),str(root),'limit']))
for name in ('k4_patch_check','k4_survives','executor_va5_check'):
 jobs.append((name,['python3.12','-B',str(out/(name+'.py')),str(root)]))
jobs.extend([
 ('registry',['python3','-B','.claude/dev/ci_dang_ky_test.py']),
 ('doctrine',['python3','-B','.claude/dev/packet_loop.py','doctrine-scan','--root','.']),
 ('adr',['python3','-B','.claude/dev/packet_loop.py','adr-song','--root','.']),
 ('ruff-products',['python3','-m','ruff','check','--no-cache','--select','F','.claude/dev/doc_receipt_thu_hoi.py','.claude/dev/doc_receipt_thu_hoi_test.py','.claude/dev/ci_dang_ky_test.py']),
])
def run(job):
 name,cmd=job
 p=subprocess.run([sys.executable,'-B',str(out/'run_logged.py'),name,*cmd],capture_output=True,text=True)
 return name,p.returncode,p.stdout,p.stderr
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for name,rc,stdout,stderr in ex.map(run,jobs):
  print(stdout,flush=True)
  if rc or stderr:print(name,'runner_rc',rc,stderr,flush=True)
