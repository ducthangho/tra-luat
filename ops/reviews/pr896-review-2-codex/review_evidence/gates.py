from pathlib import Path
import subprocess,os,json,re
root=Path.cwd(); repo=root/'cay-kho'; out=Path('/tmp/pr896-r2-audit-b3269a02')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
commands=[['python3','ops/lease_publish_test.py','--chi-ca='+s] for s in ['t26_','t27_','t138_','t161_','t162_']]+[['python3','ops/bien_nhan_v2.py','--root','.'],['python3','ops/land_evidence_nguon.py','--root','.'],['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],['python3','scripts/tl.py','doc-claims-check','--json']]
for i,cmd in enumerate(commands):
 p=subprocess.run(cmd,cwd=repo,env=env,text=True,capture_output=True,timeout=150)
 log=out/f'gate-{i}.log'; log.write_text('$ '+' '.join(cmd)+'\nrc='+str(p.returncode)+'\n'+p.stdout+p.stderr)
 print('$ '+' '.join(cmd)+'; rc='+str(p.returncode),flush=True)
 lines=p.stdout.strip().splitlines(); summary='\n'.join(lines[-4:])
 if '--json' in cmd:
  d=json.loads(p.stdout); summary=json.dumps({k:d[k] for k in ['ok','files_scanned','claims_flagged','advisory_count'] if k in d},ensure_ascii=False)
 print(summary,flush=True)
 with (root/'VERDICT.md').open('a') as f:
  f.write('\n### HƯỚNG '+str(i+2)+': Cổng gốc — '+(' '.join(cmd[1:]))+'\n\nGiả thuyết: cổng có lỗi hoặc không đo đủ ca.\n\nLệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`): `'+ ' '.join(cmd)+'`.\n\nOutput thật:\n```text\nrc='+str(p.returncode)+'\n'+summary+'\n```\n\nLog đầy đủ: `'+str(log)+'`.\n\nKết luận: '+('KHÔNG PHẢI LỖI' if p.returncode==0 else 'LỖI hoặc giới hạn môi trường; đối chiếu nguyên nhân bên dưới')+'.\n')
