import ast, collections, hashlib, json, re, subprocess, tempfile
from pathlib import Path
import yaml
BASE=Path(__file__).resolve().parent.parent; OUT=BASE/'review_evidence'; ROOT=BASE/'cay-kho'
SHA='22382d8c800bed7b995d093cdcfdc206360d7fd4'; PREV='1a276a15192013fdb1e472db409133b53ac57944'; MASTER='3e973a03b151e37cd402e0a723816eeaa8247193'
def git(*args):return subprocess.check_output(['git','-c','core.quotepath=false','-C',str(ROOT),*args])
def blob(ref,path):return git('show',ref+':'+path)
def record(n,title,cmd,output,conclusion='KHÔNG PHẢI LỖI'):
 (OUT/f'direction-{n}.log').write_text(output+'\n')
 with (BASE/'VERDICT.md').open('a') as f:f.write(f'\n### HƯỚNG {n}: {title}\n- giả thuyết: kiểm tra độc lập khẳng định và dữ liệu liên quan.\n- lệnh: `{cmd}`\n- output thật:\n```text\n{output}\n```\n- kết luận: {conclusion}.\n')
 print(output)
class UniqueLoader(yaml.SafeLoader):pass
def unique(loader,node,deep=False):
 out={}
 for k,v in loader.construct_pairs(node,deep=deep):
  if k in out:raise ValueError(f'duplicate key {k}')
  out[k]=v
 return out
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique)
def history():
 output=[]
 for name,args in [('diff.patch',('diff',PREV,SHA)),('numstat.txt',('diff','--numstat',PREV,SHA)),('diff-pr947.patch',('diff',MASTER,SHA)),('numstat-pr947.txt',('diff','--numstat',MASTER,SHA))]:output.append(f'{name}: byte_match={subprocess.check_output(['git','-c','core.quotepath=true','-C',str(ROOT),*args])==(BASE/name).read_bytes()}')
 hint=(BASE/'verdict-cu/pr896-review-5-codex-HINT.patch').read_bytes()
 paths=re.findall(rb'^\+\+\+ (\S+)',hint,re.M)
 scratch=Path(tempfile.mkdtemp(prefix='pr896-r6-hint-parent-'))
 (OUT/'hint-parent-path.txt').write_text(str(scratch))
 for path in paths:
  p=path.decode(); t=scratch/p; t.parent.mkdir(parents=True,exist_ok=True); t.write_bytes(blob(PREV,p))
 p=subprocess.run(['patch','--batch','--fuzz=0','-p0','-i',str(BASE/'verdict-cu/pr896-review-5-codex-HINT.patch')],cwd=scratch,capture_output=True,text=True)
 (OUT/'hint-parent-apply.log').write_text(p.stdout+p.stderr)
 exact=[p.decode() for p in paths if (scratch/p.decode()).read_bytes()==blob(SHA,p.decode())]
 output += [f'hint_paths={len(paths)} apply_rc={p.returncode}',p.stdout.strip(),f'byte_for_byte_matches={len(exact)}/{len(paths)}']
 output += exact
 readme_extra=subprocess.run(['diff','-u',str(scratch/'ops/reviews/README.md'),str(ROOT/'ops/reviews/README.md')],capture_output=True,text=True).stdout
 (OUT/'hint-readme-extra.diff').write_text(readme_extra)
 extra_lines=[l for l in readme_extra.splitlines() if l.startswith(('+','-')) and not l.startswith(('+++','---'))]
 output += ['README delta beyond hint: '+str(len(extra_lines))+' added/removed lines',*extra_lines]
 changed=git('diff','--name-only',PREV,SHA).decode().splitlines()
 output += ['outside_hint_non_artifact='+repr([p for p in changed if p not in exact and not p.startswith('ops/reviews/pr896-review-5-codex')])]
 artifact_paths=git('diff-tree','--no-commit-id','--name-only','-r','d308b0b').decode().splitlines()
 output += [f'd308b0b_paths={len(artifact_paths)} only_round5_artifacts={all(p.startswith("ops/reviews/pr896-review-5-codex/") or p=="ops/reviews/pr896-review-5-codex-verdict.md" for p in artifact_paths)}']
 for source,target in [('verdict-cu/pr896-review-5-codex-VERDICT.md','ops/reviews/pr896-review-5-codex-verdict.md'),('verdict-cu/pr896-review-5-codex-HINT.patch','ops/reviews/pr896-review-5-codex/HINT.patch')]:output.append(f'{source}: stored_byte_match={(BASE/source).read_bytes()==blob(SHA,target)}')
 record(2,'Tái áp hint lượt 5 và đối chiếu byte','python3 review_evidence/audit.py history','\n'.join(output))
def integrity():
 errors=[]; hashes=[]; caveats=[]
 receipts=sorted((ROOT/'ops/reviews').glob('*.receipt.yaml'))
 changed=git('diff','--name-only',MASTER,SHA).decode().splitlines()
 yaml_paths=sorted(set([p.relative_to(ROOT).as_posix() for p in receipts]+[p for p in changed if p.endswith(('.yaml','.yml')) and (ROOT/p).is_file()]))
 for path in yaml_paths:
  try:
   d=yaml.load((ROOT/path).read_text(),Loader=UniqueLoader)
   if isinstance(d,dict):
    ids=[c.get('id') for c in d.get('verdict_usage_caveats',[]) or []]
    if len(set(ids))!=len(ids):errors.append([path,'duplicate caveat id',ids])
  except Exception as e:errors.append([path,str(e)])
 def walk(x,path):
  if isinstance(x,dict):
   if 'verdict_sha256' in x:
    target=x.get('verdict_path')
    if target and (ROOT/target).is_file():
     actual=hashlib.sha256((ROOT/target).read_bytes()).hexdigest(); ok=actual==x['verdict_sha256']; hashes.append({'source':path,'target':target,'hash':actual,'ok':ok})
     if not ok:errors.append([path,target,'hash mismatch'])
   for v in x.values():walk(v,path)
  elif isinstance(x,list):
   for v in x:walk(v,path)
 for p in receipts:walk(yaml.safe_load(p.read_text()),p.relative_to(ROOT).as_posix())
 supplementary=ROOT/'ops/reviews/pr896-review-4-legacy-caveats.yaml'
 if supplementary.exists():walk(yaml.safe_load(supplementary.read_text()),supplementary.relative_to(ROOT).as_posix())
 # Match every flat *-verdict.md against any receipt hash (including nested chain entries).
 all_declared=[]
 def declarations(x):
  if isinstance(x,dict):
   if isinstance(x.get('verdict_sha256'),str):all_declared.append(x['verdict_sha256'])
   for v in x.values():declarations(v)
  elif isinstance(x,list):
   for v in x:declarations(v)
 for p in receipts:declarations(yaml.safe_load(p.read_text()))
 vfiles=sorted((ROOT/'ops/reviews').glob('*-verdict.md'))
 unclaimed=[str(p.relative_to(ROOT)) for p in vfiles if hashlib.sha256(p.read_bytes()).hexdigest() not in all_declared]
 # Frozen dicts read from AST rather than importing validator with side effects.
 tree=ast.parse((ROOT/'ops/bien_nhan_v2.py').read_text()); frozen={}
 for node in tree.body:
  if isinstance(node,(ast.Assign,ast.AnnAssign)):
   targets=node.targets if isinstance(node,ast.Assign) else [node.target]
   for t in targets:
    if isinstance(t,ast.Name) and t.id in ['ALLOWLIST_CUTOVER','NO_DA_DO']:frozen[t.id]=ast.literal_eval(node.value)
 frozen_results=[]
 for group,items in frozen.items():
  for path,value in items.items():
   target='ops/reviews/'+path
   if not (ROOT/target).exists():target=path
   data=(ROOT/target).read_bytes(); expected=value if isinstance(value,str) else value[0]
   checks={'declared_hash':hashlib.sha256(data).hexdigest()==expected,'same_master':data==blob(MASTER,target),'same_prev':data==blob(PREV,target)}
   frozen_results.append({'path':target,'group':group,**checks})
   if not all(checks.values()):errors.append(['frozen',target,checks])
 changed_verdicts=[p for p in git('diff','--name-only','--diff-filter=M',MASTER,SHA).decode().splitlines() if p.endswith('-verdict.md') or p.endswith('/VERDICT.md')]
 flat_pairs=[]
 for p in receipts:
  d=yaml.safe_load(p.read_text()); vp=d.get('verdict_path'); directory=ROOT/'ops/reviews'/p.name.removesuffix('-verdict.receipt.yaml')/'VERDICT.md'
  if directory.exists():flat_pairs.append({'path':str(directory.relative_to(ROOT)),'ok':directory.read_bytes()==(ROOT/vp).read_bytes()})
 result={'yaml_parsed':len(yaml_paths),'receipts':len(receipts),'hashes':hashes,'flat_verdict_files':len(vfiles),'unclaimed_flat_verdicts':unclaimed,'frozen':frozen_results,'modified_historical_verdicts':changed_verdicts,'flat_directory_pairs':flat_pairs,'errors':errors}
 (OUT/'integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 output=f'yaml_parsed={len(yaml_paths)} receipts={len(receipts)}\nverdict_path_hashes={len(hashes)} all_match={all(x["ok"] for x in hashes)}\nflat_verdict_files={len(vfiles)} unclaimed={unclaimed}\nflat_directory_pairs={len(flat_pairs)} all_match={all(x["ok"] for x in flat_pairs)}\nfrozen_groups={ {k:len(v) for k,v in frozen.items()} } all_hash_and_byte_match={all(all(x[k] for k in ["declared_hash","same_master","same_prev"]) for x in frozen_results)}\nmodified_historical_verdicts={changed_verdicts}\nerrors={errors}'
 record(3,'Toàn vẹn YAML, verdict và receipt v1','python3 review_evidence/audit.py integrity',output,'KHÔNG PHẢI LỖI' if not errors+unclaimed+changed_verdicts else 'CẦN KIỂM TRA')
if __name__=='__main__':
 import sys
 globals()[sys.argv[1]]()
