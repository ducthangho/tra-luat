import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT/'cay-kho'
SHA = '356a27e1378b2162bbc0be2ec06ff08fdacbdead'
def git(*args):
    return subprocess.check_output(['git','--no-optional-locks','-C',str(REPO),*args]).decode()

rc_names = ('suite','gate','sinh-no','doctrine','diff-check','focused','extra','branches','references','ruff-delta')
for name in rc_names:
    assert (ROOT/f'evidence/{name}.rc').read_text().strip()=='rc=0',name
suite=(ROOT/'evidence/suite.log').read_text()
match=re.search(r'bien_nhan_v2_test: (\d+)/(\d+) ca đạt · (\d+)/(\d+) đột biến thường CÓ RĂNG · (\d+)/(\d+) ca TỰ KIỂM đạt',suite)
assert match and 'TỔNG: ĐẠT' in suite
counts=list(map(int,match.groups()))
assert all(counts[i]==counts[i+1] for i in (0,2,4)),counts
assert len(re.findall(r'^  ĐẠT   ',suite,re.M))==counts[1]
assert len(re.findall(r'^  CÓ RĂNG',suite,re.M))==counts[3]
assert len(re.findall(r'^  TỰ KIỂM ok',suite,re.M))==counts[5]
assert 'Codex home is inside a repository' not in suite
assert not re.search(r'^  (?:ĐỎ|KHÔNG ĐO ĐƯỢC|KHÔNG RĂNG|TỰ KIỂM ĐỎ)',suite,re.M)
ast_result=json.loads((ROOT/'evidence/ast.json').read_text())
for entry in ast_result['files']:
    assert hashlib.sha256((REPO/entry['path']).read_bytes()).hexdigest()==entry['source_sha256']
    assert (REPO/entry['path']).read_bytes()==subprocess.check_output(['git','-C',str(REPO),'show',f'{SHA}:{entry["path"]}'])
status=git('status','--porcelain=v1','--untracked-files=all','--ignored')
assert not status,status
assert git('rev-parse','HEAD').strip()==SHA
assert git('diff','--name-only','b29da0b','HEAD').splitlines()==['ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py']
assert not git('diff','HEAD')
assert not git('diff','--cached')
assert hashlib.sha256((ROOT/'SPEC.md').read_bytes()).hexdigest()=='d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d'
focused=json.loads((ROOT/'evidence/focused.json').read_text())
assert len(focused)==16 and all(x['row'][2] and x['row'][3]=='giet_that' for x in focused)
for prefix in ('m142_','m147_','m153_','m156_','m157_'):
    assert sum(x['name'].startswith(prefix) for x in focused)==1
extra=json.loads((ROOT/'evidence/extra.json').read_text())
assert len(extra)==4 and all(x['result'][0]=='giet_that' and x['control'][0] for x in extra)
ruff=json.loads((ROOT/'evidence/ruff-delta.json').read_text())
assert ruff['added']==[] and ruff['removed']==[]
gate=(ROOT/'evidence/gate.log').read_text()
count=sum(p.name.lower().endswith('.receipt.yaml') for p in (REPO/'ops/reviews').iterdir())
assert f'· tổng {count}\n' in gate and 'TỔNG: ĐẠT' in gate
result={'reviewed_sha':SHA,'tree':git('rev-parse','HEAD^{tree}').strip(),'suite_counts':counts,'suite_rc':0,'gate_count':count,'gate_rc':0,'sinh_no_rc':0,'focused_real_kills':16,'extra_real_kills':4,'ruff_delta_added':0,'ruff_delta_removed':0,'source_hashes_match_initial_and_HEAD':True,'status_tracked_untracked_ignored':status,'diff_HEAD':git('diff','HEAD'),'diff_cached':git('diff','--cached'),'head_still_exact':True}
(ROOT/'evidence/final-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
print('FINAL ASSERTIONS PASS')
