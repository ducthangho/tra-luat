from pathlib import Path
import subprocess,os,sys,time,json
w=Path(__file__).resolve().parent;env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
while True:
 try:g=json.loads((w/'gates.json').read_text())
 except (FileNotFoundError,json.JSONDecodeError):g=[]
 if (w/'probes-done').exists() and any(x['label']=='head-ruff' for x in g):break
 time.sleep(10)
rows=[]
for kind,script in [('B','ops/land_evidence_nguon_test.py'),('A','ops/gate_output_doi_chieu_test.py')]:
 for side in ['head','base']:
  label=f'{side}-{kind}-sample2';cmd=[sys.executable,'-B',script];start=time.monotonic()
  print('START',label,flush=True)
  with (w/(label+'.log')).open('w') as f:p=subprocess.run(cmd,cwd=w/side,env=env,stdout=f,stderr=subprocess.STDOUT)
  row=dict(label=label,command=cmd,rc=p.returncode,seconds=time.monotonic()-start);rows.append(row)
  (w/'timing2.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
