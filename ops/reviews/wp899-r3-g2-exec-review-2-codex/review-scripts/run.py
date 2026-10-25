import os, sys, json, hashlib, subprocess, time
from pathlib import Path
R = Path(__file__).resolve().parent
(R/'tmp').mkdir(exist_ok=True)
label, *cmd = sys.argv[1:]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(R/'tmp'), TMP=str(R/'tmp'), TEMP=str(R/'tmp'), RUFF_CACHE_DIR=str(R/'ruff-cache'))
t = time.time()
p = subprocess.run(cmd, capture_output=True, env=env)
receipt = {'command':cmd,'rc':p.returncode,'elapsed_seconds':time.time()-t}
for k,b in [('stdout',p.stdout),('stderr',p.stderr)]:
    f=R/f'{label}.{k}.txt'; f.write_bytes(b)
    receipt[k]={'path':str(f),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(R/f'{label}.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False))
print(p.stdout.decode('utf-8','replace')[-2500:])
print(p.stderr.decode('utf-8','replace')[-1000:])
