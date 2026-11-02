import os, subprocess, pathlib, json, concurrent.futures
root=pathlib.Path(__file__).resolve().parent
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
commands=[('receipts',['python3','ops/bien_nhan_v2.py','--root','.']),('land',['python3','ops/land_evidence_nguon.py','--root','.']),('t26-t27',['python3',str(root/'direct_cases.py'),'.']),('doctrine',['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.']),('diff-check',['git','diff','--check'])]
def one(label,folder):
    data=[]
    for name,cmd in commands:
        p=subprocess.run(cmd,cwd=root/folder,env=env,capture_output=True,text=True)
        log=root/'evidence'/f'{label}-{name}.log'
        log.write_text('$ '+' '.join(cmd)+'\n'+p.stdout+p.stderr+f'\nEXIT={p.returncode}\n')
        data.append(dict(name=name,command=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr))
        print(label,name,'rc='+str(p.returncode),'\n'+(p.stdout+p.stderr)[-2200:],flush=True)
    return label,data
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    out=dict(pool.map(lambda t:one(*t),[('head','cay-kho'),('base','base-copy')]))
(root/'evidence/gates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
p=subprocess.run(['git','diff','--check','afc82f6','HEAD'],cwd=root/'cay-kho',env=env,capture_output=True,text=True)
(root/'evidence/diff-range-check.log').write_text(p.stdout+p.stderr+f'EXIT={p.returncode}\n')
print('diff afc82f6 HEAD --check rc='+str(p.returncode),flush=True)
