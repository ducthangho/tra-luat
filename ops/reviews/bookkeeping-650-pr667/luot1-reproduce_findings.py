import re, subprocess, yaml
from run_checks import ROOT, ENV

def git(*args, quiet=False):
    p=subprocess.run(['git',*args],cwd=ROOT,env=ENV,capture_output=True)
    print('git',' '.join(args),'rc='+str(p.returncode))
    if p.stdout and not quiet: print(p.stdout.decode().rstrip())
    if p.stderr: print(p.stderr.decode().rstrip())
    return p
def lines(path,start,end):
    content=(ROOT/path).read_text().splitlines()
    for i in range(start-1,min(end,len(content))): print(f'{path}:{i+1}: {content[i]}')

print('G1: RUN HEAD KHONG PHAI CHECKOUT / WORKFLOW PROVENANCE')
lines('ops/land/pr666-wp650-land-evidence.yaml',65,71)
w=git('show','bf63bb1:.github/workflows/ci.yml',quiet=True).stdout.decode().splitlines()
print('PINNED WORKFLOW EXCERPT')
for start,end in [(85,91),(207,217)]:
    for i in range(start-1,end): print(f'bf63bb1:.github/workflows/ci.yml:{i+1}: {w[i]}')
print('G2: LANDED VOI EVIDENCE CHUA DOC / BOOKKEEPING CHUA VAO MASTER')
lines('ops/land/pr666-wp650-land-evidence.yaml',100,113)
for path in ['ops/land/pr666-wp650-land-evidence.yaml','ops/leases/c1a1a-exec-2-claude-20260927.yaml']:
    git('cat-file','-e','origin/master:'+path)
print('G3: AUTHORITY BODY ABSENT')
import json,pathlib
d=json.loads(pathlib.Path('/tmp/review667-r1-input/github-readback.json').read_text())
c=d['audit_comment_5864536112']
print('audit_comment_fields='+','.join(sorted(c)))
print('body_present='+str('body' in c))
print('land_authorization_claim:')
lines('ops/land/pr666-wp650-land-evidence.yaml',33,52)
print('G4: EXECUTOR VA LAND OPERATOR CUNG SESSION')
lease=yaml.safe_load((ROOT/'ops/leases/c1a1a-exec-2-claude-20260927.yaml').read_bytes())
land=yaml.safe_load((ROOT/'ops/land/pr666-wp650-land-evidence.yaml').read_bytes())
sid=land['session_id'].rsplit('/',1)[-1]
print('land_session='+sid)
print('executor_selected_same_session='+str('chon executor la '+sid in lease['g1_ghi_chu']))
body=git('show','-s','--format=%B','cb9ecc8606a7d4b237a5b20702c04f096af2d0e6',quiet=True).stdout.decode()
print('product_commit_Claude_Session='+next(x for x in body.splitlines() if x.startswith('Claude-Session:')))
print('product_commit_session_matches_land='+str('Claude-Session: '+land['session_id'] in body))
lines('docs/PROTOCOL_DA_PHIEN.md',27,29)
lines('docs/PROTOCOL_DA_PHIEN.md',47,50)
print('G5: NO NGOAI PHAM VI DA KHAI')
lines('ops/land/pr666-wp650-land-evidence.yaml',109,110)
lines('ops/land/pr666-wp650-land-evidence.yaml',125,137)
print('DEBT A14 NUMSTAT TRUOC MERGE')
git('diff','--numstat','ceb1a3f36912dd4f03fe1741c443cd09e82a44ee','bf63bb1ec485bccf8eec34cc5604f949d70fc7d6','--',*lease['write_set'])
