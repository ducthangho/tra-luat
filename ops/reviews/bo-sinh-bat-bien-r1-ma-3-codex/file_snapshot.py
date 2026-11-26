from pathlib import Path
import hashlib,json,sys,subprocess
w=Path(__file__).resolve().parent;r=w.parent/'repo'
paths=set()
for args in [('ls-files','-z'),('ls-files','--others','--exclude-standard','-z'),('ls-files','--others','--ignored','--exclude-standard','-z')]:
 paths.update(p for p in subprocess.check_output(['git','-C',str(r),*args]).decode().split('\0') if p)
rows={p:hashlib.sha256((r/p).read_bytes()).hexdigest() for p in sorted(paths) if (r/p).is_file()}
(w/('files-'+sys.argv[1]+'.json')).write_text(json.dumps(rows,indent=2));print('files',len(rows),'snapshot',sys.argv[1])
