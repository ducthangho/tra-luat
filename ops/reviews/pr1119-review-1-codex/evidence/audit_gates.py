from audit_common import *
import sys

name=sys.argv[1]
cwd=ROOT/'work'/name
cmds={
 'bien-nhan':['python3','ops/bien_nhan_v2.py','--root','.'],
 'land':['python3','ops/land_evidence_nguon.py','--root','.'],
 'direct':['python3',str(ROOT/'direct_gates.py'),str(cwd)],
 'doctrine':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
 'diff-check':['git','diff','--check',BASE,'HEAD'],
}
results={}
for key,args in cmds.items():
    p=run(args,cwd,timeout=300)
    (EVID/f'{name}-{key}.stdout').write_bytes(p.stdout)
    (EVID/f'{name}-{key}.stderr').write_bytes(p.stderr)
    results[key]={'command':args,'cwd':str(cwd),'rc':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}
    print(name,key,'rc='+str(p.returncode),p.stdout.decode(errors='replace')[-1100:],p.stderr.decode(errors='replace')[-800:],flush=True)
save(name+'-gates.json',results)
append('Cổng '+name+' — `PYTHONDONTWRITEBYTECODE=1 python3 audit_gates.py '+name+'`: '+', '.join(k+' rc='+str(v['rc']) for k,v in results.items())+'. Lệnh và output nguyên văn: `evidence/'+name+'-gates.json`, `evidence/'+name+'-*.stdout/.stderr`.')
