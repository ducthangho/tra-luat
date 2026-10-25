import os, sys, hashlib, subprocess, json
from pathlib import Path
root=Path.cwd(); files={}
for dp,dn,fn in os.walk(root):
    if Path(dp)==root:
        dn[:]=[x for x in dn if x not in ('.git','.review')]
    for n in fn:
        p=Path(dp)/n
        if p.is_symlink(): files[str(p.relative_to(root))]={'link':os.readlink(p)}
        elif p.is_file():
            b=p.read_bytes(); files[str(p.relative_to(root))]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
cmds=[['git','rev-parse','HEAD','HEAD^{tree}'],['git','status','--porcelain=v1','--untracked-files=all','--ignored=matching'],['git','diff','--binary'],['git','diff','--cached','--binary'],['git','ls-files','--others','--exclude-standard'],['git','ls-files','--others','--ignored','--exclude-standard']]
r={'files':files,'commands':[]}
for cmd in cmds:
    p=subprocess.run(cmd,capture_output=True); r['commands'].append({'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
Path(sys.argv[1]).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(len(files),'files',[(x['command'][1],x['rc']) for x in r['commands']])
