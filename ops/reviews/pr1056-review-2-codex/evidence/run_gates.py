from pathlib import Path
import subprocess, os, json, sys, re
root=Path(__file__).resolve().parent.parent
commands={
'bien_nhan_v2':['python3','ops/bien_nhan_v2.py','--root','.'],
'land_evidence_nguon':['python3','ops/land_evidence_nguon.py','--root','.'],
'doctrine_scan':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
**{t:['python3','ops/lease_publish_test.py',f'--chi-ca={t}_'] for t in ('t26','t27','t138')}}
def run(folder, label):
 result={}
 for name,cmd in commands.items():
  p=subprocess.run(cmd,cwd=folder,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  (root/'evidence'/f'{label}-{name}.log').write_text(p.stdout)
  (root/'evidence'/f'{label}-{name}.rc').write_text(str(p.returncode)+'\n')
  summary=[l for l in p.stdout.splitlines() if re.match(r'^(bien_nhan_v2:|land_evidence_nguon:|TỔNG:|doctrine-scan:|lease_publish:)',l)]
  result[name]={'command':' '.join(cmd),'rc':p.returncode,'summary':summary,'sandbox_artifact':'Codex home is inside a repository' in p.stdout}
  print(label,name,json.dumps(result[name],ensure_ascii=False),flush=True)
 (root/'evidence'/f'{label}-gates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 with (root/'VERDICT.md').open('a') as f:
  f.write(f'\n### Đo cổng — {label}\n\nLỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_gates.py {folder.name} {label}`; mỗi subprocess chạy các lệnh sẵn có dưới đây tại `{folder}`. OUTPUT THẬT:\n\n```json\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n```\n\nLog đầy đủ: `evidence/'+label+'-*.log`; rc lưu riêng.\n')
 return result
if __name__=='__main__':run((root/sys.argv[1]).resolve(),sys.argv[2])
