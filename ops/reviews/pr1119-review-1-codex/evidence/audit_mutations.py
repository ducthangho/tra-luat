from audit_common import *
import re, shutil

mut=ROOT/'work/mutant'
if not mut.exists(): shutil.copytree(ROOT/'work/head',mut)
results=[]
for pr,round_,_ in CASES:
    name=f'pr{pr}-review-{round_}-codex-verdict.receipt.yaml'
    path=mut/'ops/reviews'/name
    orig=path.read_bytes()
    old=re.search(rb'^verdict_sha256: ([0-9a-f]{64})$',orig,re.M)[1]
    new=(b'0' if old[:1]!=b'0' else b'1')+old[1:]
    changed=orig.replace(b'verdict_sha256: '+old,b'verdict_sha256: '+new)
    assert changed!=orig
    path.write_bytes(changed)
    try:
        changes=git('diff','--name-only',cwd=mut).decode().splitlines()
        assert changes==['ops/reviews/'+name],changes
        item={'receipt':name,'field':'verdict_sha256','old':old.decode(),'new':new.decode(),'changed_paths':changes}
        for key,args in [('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']),('direct',['python3',str(ROOT/'direct_gates.py'),str(mut)])]:
            p=run(args,mut,timeout=300)
            prefix=f'mutant-{pr}-{round_}-{key}'
            (EVID/(prefix+'.stdout')).write_bytes(p.stdout)
            (EVID/(prefix+'.stderr')).write_bytes(p.stderr)
            output=(p.stdout+p.stderr).decode(errors='replace')
            matches=[x for x in output.splitlines() if name in x]
            foreign=sorted(set(re.findall(r'pr\d+-review-\d+-codex-verdict\.receipt\.yaml',output))-{name})
            item[key]={'command':args,'rc':p.returncode,'target_lines':matches,'foreign_receipts':foreign,
                       'correctly_rejected':p.returncode!=0 and bool(matches) and not foreign}
            print(name,key,json.dumps(item[key],ensure_ascii=False),flush=True)
        results.append(item)
        save('mutations.json',results)
    finally: path.write_bytes(orig)
    assert git('diff','--name-only',cwd=mut)==b''
save('mutations.json',results)
append('Đột biến — `PYTHONDONTWRITEBYTECODE=1 python3 audit_mutations.py`: '+str(len(results))+' lần đổi duy nhất verdict_sha256 trên bản sao `work/mutant`, từng lần hồi nguyên; '+str(sum(x[k]['correctly_rejected'] for x in results for k in ('bien-nhan','direct')))+' / '+str(len(results)*2)+' lần cổng bien_nhan_v2 và t26 đỏ, nêu đúng tên biên nhận bị đổi. Chi tiết command/rc/output ở `evidence/mutations.json`, `evidence/mutant-*.stdout/.stderr`.')
