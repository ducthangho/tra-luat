from pathlib import Path
import tempfile,subprocess
from audit import BASE,OUT,SHA
copy=Path(tempfile.mkdtemp(prefix='pr896-r6-mutations-'))/'copy'
p=subprocess.run(['git','clone','--no-hardlinks','--no-checkout',str(BASE/'mirror.git'),str(copy)],capture_output=True,text=True)
assert p.returncode==0,(p.stdout,p.stderr)
p2=subprocess.run(['git','-C',str(copy),'checkout','--detach',SHA],capture_output=True,text=True)
assert p2.returncode==0,(p2.stdout,p2.stderr)
(OUT/'copy-path.txt').write_text(str(copy));(OUT/'clone.log').write_text(p.stdout+p.stderr+p2.stdout+p2.stderr)
print(p.stderr+p2.stderr)
