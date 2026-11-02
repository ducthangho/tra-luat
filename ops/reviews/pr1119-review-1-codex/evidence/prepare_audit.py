from audit_common import *
import shutil

before = {str(p.relative_to(REPO)):sha(p.read_bytes()) for p in REPO.rglob('*') if p.is_file() and '.git' not in p.relative_to(REPO).parts}
save('repo-before.json', before)
paths=git('diff','--name-only',BASE,HEAD).decode().splitlines()
actual=git('diff',BASE,HEAD)
preflight={'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),
 'base':git('merge-base','HEAD','origin/master').decode().strip(),'status':git('status','--porcelain').decode(),
 'paths':paths,'out_of_scope':[p for p in paths if not p.startswith('ops/reviews/')],
 'input_patch_equal':actual==(ROOT/'DIFF.patch').read_bytes(),'patch_sha256':sha(actual),
 'core_abbrev':git('config','core.abbrev').decode().strip()}
save('preflight.json',preflight)
for name,ref in [('head',HEAD),('base',BASE)]:
    dst=ROOT/'work'/name
    shutil.copytree(REPO,dst)
    git('config','core.abbrev','7',cwd=dst)
    git('checkout','--detach',ref,cwd=dst)
    print(name,git('rev-parse','HEAD',cwd=dst).decode().strip(), 'core.abbrev='+git('config','core.abbrev',cwd=dst).decode().strip())
print(json.dumps({k:v for k,v in preflight.items() if k!='paths'},ensure_ascii=False))
append('Preflight — `PYTHONDONTWRITEBYTECODE=1 python3 prepare_audit.py`: HEAD/tree/base, status, phạm vi và DIFF.patch ở `evidence/preflight.json`; '+str(len(paths))+' đường dẫn đổi, `out_of_scope=[]`, `input_patch_equal='+str(preflight['input_patch_equal'])+'`. Hai bản sao `work/head`, `work/base` đã ghim `git config core.abbrev 7`; `audit.gitconfig` áp cho phép đo git trên clone gốc.')
