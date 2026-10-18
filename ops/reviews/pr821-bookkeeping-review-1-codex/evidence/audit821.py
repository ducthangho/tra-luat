import sys,json,pathlib,subprocess,hashlib
sys.path.insert(0,'/tmp'); import len as l
import yaml
r=pathlib.Path('/home/user/rv773'); t=r/'ops/land/pr779-wp775-land-evidence.yaml'; p=t.with_name('pr779-wp775-provenance')
d=l.nap_yaml(yaml,t.read_bytes())
for k,v in l.duyet(d):
 if isinstance(v,str) and l.RE_KHAI_DO.match(v):
  print('\nCLAIM',k, v)
  for tok in l.token_nguon(v): print('TOKEN',tok,'=>',l.phan_giai(tok,r,p,t))
for f in sorted(p.glob('*.json')):
 x=json.loads(f.read_text());print('\nFILE',f.name);print(json.dumps(x,ensure_ascii=False)[:18000])
