import json, os, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
repo=root/'cay-kho'
out=root/'review_evidence'
checks=[('t26',['python3','ops/lease_publish_test.py','--chi-ca=t26_']),('t27',['python3','ops/lease_publish_test.py','--chi-ca=t27_']),('t138',['python3','ops/lease_publish_test.py','--chi-ca=t138_']),('bien_nhan_v2',['python3','ops/bien_nhan_v2.py','--root','.']),('land',['python3','ops/land_evidence_nguon.py','--root','.']),('doctrine',['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.']),('doc_claims',['python3','scripts/tl.py','doc-claims-check','--json'])]
results=[]
for label,cmd in checks:
 p=subprocess.run(cmd,cwd=repo,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 for ext,v in [('stdout',p.stdout),('stderr',p.stderr),('rc',str(p.returncode))]: (out/f'{label}.{ext}').write_text(v)
 lines=p.stdout.splitlines()+p.stderr.splitlines()
 summary='\n'.join(x for x in lines if any(t in x for t in ['lease_publish:', 'bien_nhan_v2:', 'land_evidence_nguon:', 'TỔNG:', 'doctrine-scan:', '"ok"', '"strict"','Codex home']))
 item=dict(name=label,cmd=' '.join(cmd),rc=p.returncode,summary=summary)
 results.append(item); print(json.dumps(item,ensure_ascii=False),flush=True)
(out/'checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
with (root/'VERDICT.md').open('a') as f:
 f.write('\n### HƯỚNG 2: Ba ca riêng và bốn cổng trên cây gốc\n\n- giả thuyết: cổng xanh chỉ do bỏ qua, số đạt không đủ, hoặc doc-claims không ok.\n- lệnh và output thật (log đầy đủ ở `review_evidence/`):\n```text\n')
 for x in results: f.write(f"$ {x['cmd']}\nrc={x['rc']}\n{x['summary']}\n")
 f.write('```\n- kết luận: '+('KHÔNG PHẢI LỖI' if all(x['rc']==0 for x in results) else 'CẦN PHÂN LOẠI LỖI / KHÔNG ĐO ĐƯỢC')+'. Đây là phép đo cổng, không tự chứng minh nội dung mọi lời khai.\n')
