from pathlib import Path
import concurrent.futures, json, os, subprocess, sys

work = Path(__file__).resolve().parent.parent
root = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else work/'cay-kho'
label = sys.argv[2] if len(sys.argv)>2 else 'baseline'
commands = {
 'bien_nhan_v2':['python3','ops/bien_nhan_v2.py','--root','.'],
 'land_evidence_nguon':['python3','ops/land_evidence_nguon.py','--root','.'],
 'doctrine_scan':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
 **{n:['python3','ops/lease_publish_test.py','--chi-ca='+n+'_'] for n in ['t26','t27','t138']},
}
def run(item):
 name, cmd = item
 env = {**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'}
 p = subprocess.run(cmd,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (work/f'evidence/{label}-{name}.log').write_text(p.stdout)
 (work/f'evidence/{label}-{name}.rc').write_text(str(p.returncode)+'\n')
 lines=p.stdout.splitlines()
 summary=[l for l in lines if 'TỔNG:' in l or 'lease_publish:' in l or 'DOCTRINE' in l or 'doctrine' in l or 'không đo' in l.lower() or 'vi phạm' in l.lower() or 'ĐỎ ' in l]
 return name, {'command':' '.join(cmd),'rc':p.returncode,'summary':summary or lines[-3:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 results=dict(pool.map(run,commands.items()))
(work/f'evidence/{label}-gates.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
with (work/'VERDICT.md').open('a') as f:
 f.write(f'\n### Đo cổng — {label}\n\nCây đo: `{root}`. `PYTHONDONTWRITEBYTECODE=1`; không ghi bytecode vào cây review. LỆNH và OUTPUT THẬT (rc lấy trực tiếp subprocess):\n\n```json\n'+json.dumps(results,ensure_ascii=False,indent=2)+'\n```\n')
 f.write('Log đầy đủ: `evidence/'+label+'-*.log`, mã thoát: `evidence/'+label+'-*.rc`.\n')
