import subprocess,json,hashlib
from pathlib import Path
S=Path(__file__).resolve().parent; E=S/'evidence'; H='3a3aac561ba359c08dfe92d95584b56494fc12d4'; B='fb74c6eca742205acc0af9bb7ea89da94f15aa21'; errors=[]; trees={}
for name in ['cay-kho','work/head','work/base','work/mutant']:
 root=S/name
 def git(*a):return subprocess.check_output(['git',*a],cwd=root).decode().strip()
 row={'head':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}'),'status':git('status','--porcelain=v1','--untracked-files=all','--ignored'),'core_abbrev':git('config','core.abbrev')}; trees[name]=row
 if row['head']!=(B if name=='work/base' else H) or row['status'] or row['core_abbrev']!='7': errors.append('tree integrity '+name)
for name in ['bytes','receipt','readme','mutation']:
 j=json.loads((E/f'{name}.json').read_text())
 if j['errors']:errors.append(name+' errors')
for name in ['head','base']:
 j=json.loads((E/f'{name}-gates.json').read_text())
 if len(j)!=5 or any(x['rc'] for x in j):errors.append(name+' gate failures')
equal={label:(E/f'head-{label}.log').read_bytes()==(E/f'base-{label}.log').read_bytes() for label in ['land','doctrine','diff-check']}
for k,v in equal.items():
 if not v:errors.append('unexpected log delta '+k)
direct_equal=(E/'head-direct.log').read_text().replace('/work/head/','/work/TREE/')==(E/'base-direct.log').read_text().replace('/work/base/','/work/TREE/')
if not direct_equal:errors.append('direct log difference beyond cwd')
p=subprocess.run(['git','diff','--check',B,'HEAD'],cwd=S/'cay-kho',stdout=subprocess.PIPE,stderr=subprocess.STDOUT); (E/'original-diff-check.log').write_bytes(p.stdout)
if p.returncode or p.stdout:errors.append('original diff check')
r={'trees':trees,'equal_logs':equal,'direct_logs_equal_after_cwd_normalization':direct_equal,'original_diff_check_rc':p.returncode,'original_diff_check_bytes':len(p.stdout),'errors':errors}
(E/'final-integrity.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(r,ensure_ascii=False,indent=2)); assert not errors
