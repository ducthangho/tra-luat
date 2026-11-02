from pathlib import Path
import subprocess, os, json, concurrent.futures
S=Path(__file__).resolve().parent;E=S/'evidence';os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['GIT_CONFIG_GLOBAL']=str(S/'audit.gitconfig');os.environ['GIT_CONFIG_NOSYSTEM']='1'
B='62e629156fd0729b743f15eed2f32487786b9adc';H='1a87a863174ef104b2df8bc98b77724fb6796d9b'
def one(tree,name,cmd):
 r=subprocess.run(cmd,cwd=S/'work'/tree,capture_output=True)
 for suffix,b in [('stdout',r.stdout),('stderr',r.stderr)]: (E/f'{tree}-{name}.{suffix}').write_bytes(b)
 result={'tree':tree,'gate':name,'command':cmd,'rc':r.returncode,'stdout':r.stdout.decode(errors='replace'),'stderr':r.stderr.decode(errors='replace')}
 print(tree,name,'rc='+str(r.returncode),result['stdout'][-700:],result['stderr'][-250:],flush=True)
 return result
jobs=[]
for tree in ('base','head'):
 jobs.extend([(tree,'bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']), (tree,'land',['python3','ops/land_evidence_nguon.py','--root','.']), (tree,'direct',['python3',str(S/'direct_gates.py'),'.']), (tree,'doctrine',['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.']), (tree,'diff-ci',['git','-c','core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab','diff','--check',B,'HEAD']), (tree,'diff-default',['git','diff','--check',B,'HEAD'])])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(lambda j:one(*j),jobs))
(E/'gates.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
with (S/'VERDICT.md').open('a') as f:
 f.write('\nĐo cổng (lệnh chạy tại work/base hoặc work/head; log đầy đủ evidence/gates.json):\n\n| Cổng | base rc | HEAD rc |\n|---|---:|---:|\n')
 for name in ('bien-nhan','land','direct','doctrine','diff-ci','diff-default'):
  vals=[r['rc'] for r in results if r['gate']==name];f.write(f'| {name} | {vals[0]} | {vals[1]} |\n')
