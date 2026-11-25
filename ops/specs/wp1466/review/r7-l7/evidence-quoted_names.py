"""Chỉ đọc một tên Unicode ĐÃ CÓ trong kho; không dựng tên/path đối kháng."""
from pathlib import Path
import subprocess,json,datetime
S=Path('cay-kho');O=Path('out')
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
ps=subprocess.check_output(['git','-C',str(S),'ls-tree','-r','-z','--name-only','HEAD']).decode().split('\0')
p=next(p for p in ps if not p.isascii());print('EXISTING_PATH',p)
for label,flags in [('default',[]),('nul',['-z'])]:
 cmd=['git','-C',str(S),'-c','core.quotePath=true','ls-tree','-r',*flags,'HEAD','--',p];b=subprocess.check_output(cmd).decode();parsed=b.rstrip('\n\0').split('\t',1)[1]
 print('COMMAND',json.dumps(cmd,ensure_ascii=False));print('RAW',repr(b));print('CASE',label,'PARSED_EQUALS_PATH',parsed==p,'SUFFIX_LOG',parsed.endswith('.log'))
blob=subprocess.check_output(['git','-C',str(S),'show','48d372e14f190dae83a75ccbca8ee9a0b25635c5:ops/lease_publish.py']).decode()
for i,l in enumerate(blob.splitlines(),1):
 if 742<=i<=760:print('B_SCANNER',i,l)
print('NO_NEW_ATTACK_PATH_CREATED True; lease .yaml bypass described only, not executed')
