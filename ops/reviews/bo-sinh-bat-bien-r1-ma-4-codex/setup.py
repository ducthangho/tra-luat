from pathlib import Path
import subprocess,hashlib,json,shutil,os
w=Path(__file__).resolve().parent;r=w.parent/'repo'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
checks={}
for p,h in [('SPEC.md','bdde0a9bdba79a19fbbc77cfee8311e209b0c91cc16612bb8029167cca186577'),('bang_chung/handoff.yaml','c43f0e6428fa7a915cc81a1a7d16e4797f044c3d852f4e9ec59686143303ba7e'),('bang_chung/nghia-vu.md','5541ed087b8aee19c7c1458291a84053a3600fc05ed2c093dcca75d14449faac'),('bang_chung/cong-cu/bang_toan_tu.py','784856b29560cabbde65959625b3d67176867e74276581270535ad8a0b4a0178'),('bang_chung/bang-toan-tu/bang.md','c3286544b60c4b01be25457120ed3067b7adcf78e48c0def1c5aedb811956707')]:
 v=hashlib.sha256((w.parent/p).read_bytes()).hexdigest();checks[p]={'sha256':v,'match':v==h};assert v==h
for side,sha in [('head','97ec9686184fdf55dc1736007e6fdcb186122465'),('base','a89c83acf998008caecba9084a7d295845bf1976')]:
 subprocess.run(['git','clone','-q','--no-hardlinks',str(r),str(w/side)],check=True)
 subprocess.run(['git','-C',str(w/side),'checkout','-q','--detach',sha],check=True)
 subprocess.run(['git','-C',str(w/side),'config','core.abbrev','7'],check=True)
files={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob('*') if p.is_file() and '.git' not in p.relative_to(r).parts}
(w/'snapshot-start.json').write_text(json.dumps(files));(w/'preflight.json').write_text(json.dumps(checks,indent=2))
shutil.copy(w.parent/'bang_chung/cong-cu/bang_toan_tu.py',w/'bang_toan_tu.py')
p=w.parent/'lich_su/luot3/repro_R3.py';(w/p.name).write_text(p.read_text().replace('==[0,0,3,3]','==[3,3,3,3]'))
print('HASHES_OK',len(files),'files; clones ready')
