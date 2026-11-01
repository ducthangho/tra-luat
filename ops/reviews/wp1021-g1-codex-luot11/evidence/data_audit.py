import hashlib
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from record import REPO, ENV

names = os.listdir(REPO/'ops/reviews')
count = sum(x.lower().endswith('.receipt.yaml') for x in names)
log = (Path(__file__).parent/'h03.log').read_text()
actual = re.search(r'· tổng (\d+)',log)
assert actual and int(actual[1]) == count
print(f'sys.platform={sys.platform}\nPython={platform.python_version()}\nos.name={os.name}')
print(f'independent_os_listdir_total={count}\nCLI_total={actual[1]}\nequal={count==int(actual[1])}')
for rev in ('HEAD^1','HEAD'):
    raw = subprocess.check_output(['git','-C',str(REPO),'ls-tree','-z',rev+':ops/reviews'],env=ENV)
    entries = [x.split(b'\t',1)[1].decode() for x in raw.split(b'\0') if x]
    print(rev+' receipt-entry-count='+str(sum(n.lower().endswith('.receipt.yaml') for n in entries)))
for rel in ('ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG-r2.md','ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG.md'):
    raw = subprocess.check_output(['git','-C',str(REPO),'show','HEAD:'+rel],env=ENV)
    print(rel+' sha256='+hashlib.sha256(raw).hexdigest())
