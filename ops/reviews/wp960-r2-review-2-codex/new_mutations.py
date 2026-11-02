"""Independent reviewer mutations beyond m103-m113; existing 89 cases, exact-head copies."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path('/tmp/wp960-r2-l2-copy')
SHA='ae0d06c23fb777545fd7547a07d9f368e4122f49'
M={
 'n1-vang-stat':('        p.lstat()\n','        p.stat()\n'),
 'n2-vang-oserror':('    except OSError:\n        return False\n','    except OSError:\n        return True\n'),
 'n3-peel-rc':('    if rc != 0 or not _HEX40.match(ra):\n','    if False:\n'),
 'n4-ref-show-error':('        if rc != 0:\n            raise KhongDoDuoc(f"không kiểm được ref mặc định', '        if rc != 0:\n            continue\n            raise KhongDoDuoc(f"không kiểm được ref mặc định'),
 'n5-sinh-no-utf8':('        except (OSError, UnicodeDecodeError, yaml.YAMLError) as ex:\n','        except (OSError, yaml.YAMLError) as ex:\n'),
 'n6-sinh-no-yaml':('        except (OSError, UnicodeDecodeError, yaml.YAMLError) as ex:\n','        except (OSError, UnicodeDecodeError) as ex:\n'),
 'n7-peel-noncommit':(' if c}\n','}\n'),
}
for name in sys.argv[1:] or M:
 old,new=M[name]
 with tempfile.TemporaryDirectory(prefix='wp960-r2-l2-mutant-') as tmp:
  dest=Path(tmp)/'repo'
  subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(ROOT),str(dest)],check=True)
  subprocess.run(['git','-C',str(dest),'checkout','--quiet','--detach',SHA],check=True)
  source=dest/'ops/bien_nhan_v2.py';s=source.read_text();assert s.count(old)==1,(name,s.count(old));source.write_text(s.replace(old,new))
  sp=importlib.util.spec_from_file_location('tests_'+name,dest/'ops/bien_nhan_v2_test.py')
  t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
  failures=[]
  for fn in t.CA:
   state,detail=t._chay_1(fn)
   if state!='qua':failures.append([fn.__name__,state,detail])
  print(json.dumps(dict(mutation=name,cases=len(t.CA),passed=len(t.CA)-len(failures),red=failures,old=old,new=new),ensure_ascii=False),flush=True)
