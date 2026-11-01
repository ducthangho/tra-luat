from common import *
import sys
name=sys.argv[1];root=S/'work'/name
commands=[('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']),('land',['python3','ops/land_evidence_nguon.py','--root','.']),('direct',['python3',str(S/'direct.py'),'.']),('doctrine',['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.']),('diff-check',['git','diff','--check',BASE,'HEAD'])]
data=[logged(name+'-'+n,c,root) for n,c in commands]
save(name+'-gates.json',data)
for v in data:print(v['cmd'],v['rc'],(E/v['stdout']).read_text()[-1200:])
note('Cổng '+name+' — `PYTHONDONTWRITEBYTECODE=1 python3 gates.py '+name+'`: '+str([x['rc'] for x in data])+' theo thứ tự bien_nhan_v2, land_evidence_nguon, ba t26/t27 gọi trực tiếp, doctrine-scan, diff-check. Command/stdout/stderr: `evidence/'+name+'-gates.json`.')
