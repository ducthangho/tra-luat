import os,subprocess,json,re
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1'
S=Path(__file__).resolve().parent; R=S/'cay-kho'; M=S/'work/mutant'; E=S/'evidence'; P='ops/reviews/pr1075-review-1-codex-verdict.receipt.yaml'
subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(R),str(M)],check=True)
subprocess.run(['git','-C',str(M),'config','core.abbrev','7'],check=True)
subprocess.run(['git','-C',str(M),'checkout','--detach','--quiet','3a3aac561ba359c08dfe92d95584b56494fc12d4'],check=True)
f=M/P; original=f.read_bytes(); mutant,n=re.subn(rb'(?m)^verdict_sha256: [0-9a-f]{64}$',b'verdict_sha256: '+b'f'*64,original); assert n==1
rows=[]
try:
 f.write_bytes(mutant)
 delta=subprocess.check_output(['git','diff','--name-only'],cwd=M).decode().splitlines(); assert delta==[P],delta
 for label,cmd in [('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']),('direct',['python3',str(S/'direct_checks.py'),'.'])]:
  p=subprocess.run(cmd,cwd=M,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); (E/f'mutant-{label}.log').write_bytes(p.stdout)
  out=p.stdout.decode(); rows.append({'label':label,'command':cmd,'cwd':str(M),'rc':p.returncode,'output':out}); print(label,'rc',p.returncode,out,flush=True)
finally:
 f.write_bytes(original)
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all','--ignored'],cwd=M).decode()
reds=[x for x in rows[0]['output'].splitlines() if x.startswith('  ĐỎ')]; direct=rows[1]['output']; errors=[]
if rows[0]['rc']!=1 or not reds or not all(Path(P).name in x for x in reds): errors.append('wrong gate rejection')
if rows[1]['rc']!=1 or 'FAIL t26_' not in direct or Path(P).name not in direct or 'LỆCH BĂM' not in direct or direct.count('PASS t27_')!=2: errors.append('wrong direct rejection')
if status or f.read_bytes()!=original:errors.append('restore')
r={'mutation':'only verdict_sha256 -> 64 f characters','changed_paths':delta,'gate_rc':rows[0]['rc'],'red_diagnostics':reds,'direct_rc':rows[1]['rc'],'t26_failed': 'FAIL t26_' in direct,'t27_passed':direct.count('PASS t27_'),'restored':f.read_bytes()==original,'status_after':status,'errors':errors}
(E/'mutation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(r,ensure_ascii=False,indent=2)); assert not errors
