import os, json, subprocess, hashlib, concurrent.futures
from pathlib import Path
S=Path(__file__).resolve().parent
ENV=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_GLOBAL=str(S/'audit.gitconfig'), GIT_CONFIG_NOSYSTEM='1', GIT_OPTIONAL_LOCKS='0')
B='180039c4b791fba4c89991623151cbb7378fce53'
H='0e824fe4c1ac674081c93c6f2098e5433c932890'
def run(label,root,cmd):
    p=subprocess.run(cmd,cwd=root,env=ENV,capture_output=True)
    for ext,b in [('stdout',p.stdout),('stderr',p.stderr)]: (S/'evidence'/f'{label}.{ext}').write_bytes(b)
    r=dict(label=label,cmd=cmd,cwd=str(root),rc=p.returncode,stdout=p.stdout.decode(errors='replace'),stderr=p.stderr.decode(errors='replace'))
    print(label, 'rc', p.returncode, 'stdout',r['stdout'][:1400], 'stderr',r['stderr'][:300],flush=True)
    return r
cmds={
 'bien-nhan':['python3','ops/bien_nhan_v2.py','--root','.'],
 'land':['python3','ops/land_evidence_nguon.py','--root','.'],
 'direct':['python3',str(S/'direct_tests.py'),'.'],
 'doctrine':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
}
tasks=[]
for name in ('base','head'):
    root=S/'work'/name
    for k,c in cmds.items(): tasks.append((name+'-'+k,root,c))
    tasks.append((name+'-diff-default',root,['git','diff','--check',B,'HEAD']))
    tasks.append((name+'-diff-ci',root,['git','-c','core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab','diff','--check',B,'HEAD']))
    code='import ci_duong_nhanh as m; import json; print(json.dumps(m.kiem_diff_check({m.BIEN_GOC:"'+B+'",m.BIEN_DAU:"HEAD"}),ensure_ascii=False))'
    tasks.append((name+'-ci-function',root,['python3','-c','import sys; sys.path.insert(0,"ops"); '+code]))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(lambda t:run(*t),tasks))
(S/'evidence/gates.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
with (S/'VERDICT.md').open('a') as f:
    f.write('\nĐo cổng: `PYTHONDONTWRITEBYTECODE=1 python3 measure_gates.py` (lệnh và output đầy đủ: `evidence/gates.json`).\n\n')
    for r in results: f.write(f"- `{r['label']}`: rc={r['rc']}; xem `evidence/{r['label']}.stdout` / `.stderr`.\n")
