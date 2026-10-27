import json,hashlib,subprocess,yaml,ast
from pathlib import Path
from audit import BASE,ROOT,OUT,SHA,MASTER,UniqueLoader,blob,record
copy=Path((OUT/'copy-path.txt').read_text());paths=json.loads((OUT/'hint-paths.json').read_text());parsed=[]
for path in paths:
 if path.endswith('.yaml'):
  d=yaml.load((copy/path).read_text(),Loader=UniqueLoader);ids=[c['id'] for c in d.get('verdict_usage_caveats',[])];assert len(ids)==len(set(ids));parsed.append(path)
readme=(copy/'ops/reviews/README.md').read_text();r=yaml.safe_load((copy/'ops/reviews/pr896-review-6-codex-verdict.receipt.yaml').read_text());c=next(x for x in r['verdict_usage_caveats'] if x['id']=='LAN-CHAY-DAU-CHET-VI-MAY-CHU-QUA-TAI');assert c['mo_ta'] in readme
original_unchanged={}
for args in [('rev-parse','HEAD','HEAD^{tree}'),('status','--porcelain=v1','--untracked-files=all','--ignored'),('diff','--exit-code'),('rev-parse','--is-shallow-repository'),('config','core.abbrev')]:
 p=subprocess.run(['git','-C',str(ROOT),*args],capture_output=True,text=True);original_unchanged[' '.join(args)]={'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
assert original_unchanged['rev-parse HEAD HEAD^{tree}']['stdout'].splitlines()==[SHA,'3412a314b129d1ee1473e528a5ec438378ccebe5']
assert original_unchanged['status --porcelain=v1 --untracked-files=all --ignored']['stdout']==''
assert original_unchanged['diff --exit-code']['rc']==0
changed=subprocess.check_output(['git','-C',str(copy),'diff','--name-only']).decode().splitlines();assert sorted(changed)==sorted(paths)
verdict_changed=[p for p in changed if p.endswith('-verdict.md') or p.endswith('/VERDICT.md')];assert not verdict_changed
frozen=[];tree=ast.parse((ROOT/'ops/bien_nhan_v2.py').read_text())
for node in tree.body:
 if isinstance(node,(ast.Assign,ast.AnnAssign)):
  targets=node.targets if isinstance(node,ast.Assign) else [node.target]
  for t in targets:
   if isinstance(t,ast.Name) and t.id in ['ALLOWLIST_CUTOVER','NO_DA_DO']:
    for path,value in ast.literal_eval(node.value).items():
     rel='ops/reviews/'+path if (ROOT/'ops/reviews'/path).exists() else path;frozen.append((copy/rel).read_bytes()==(ROOT/rel).read_bytes())
assert len(frozen)==53 and all(frozen)
result={'reviewed_tree_unchanged':original_unchanged,'clone_changed_paths':changed,'hint_yaml_parsed_unique_ids':len(parsed),'hint_receipt_readme_description_match':True,'hint_modified_verdicts':verdict_changed,'hint_frozen_v1_unchanged':sum(frozen),'manifest_summary':json.loads((OUT/'verdict-manifests.json').read_text())['summary'],'hint_sha256':hashlib.sha256((BASE/'HINT.patch').read_bytes()).hexdigest()}
(OUT/'final-state.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));summary=json.dumps(result,ensure_ascii=False,indent=2)
record(17,'Toàn vẹn cuối cây gốc và bản sao hint','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/final_checks.py; git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored; git diff --exit-code; sha256sum <verdict manifests>',summary)
for name in ['residuals.py','land_surfaces.py']:
 p=OUT/name
 if p.exists():p.unlink()
