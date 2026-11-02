import ast, collections, hashlib, json, os, re, subprocess, tempfile
from pathlib import Path
import yaml
BASE=Path(__file__).resolve().parents[1]; ROOT=BASE/'cay-kho'; OUT=BASE/'review_evidence'
SHA='fb87110cfab832406984f893e6a4c79fbb932aef'; PREV='05bc12e2b9008071ca28edbd4574e58644d48220'; MASTER='3e973a03b151e37cd402e0a723816eeaa8247193'
def git(*a): return subprocess.check_output(['git','-C',str(ROOT),*a])
def blob(s,p): return git('show',s+':'+p)
def record(n,title,hyp,cmd,lines,conclusion='KHÔNG PHẢI LỖI'):
 s='\n'.join(lines); (OUT/f'{n:02d}.log').write_text(s+'\n'); print(s)
 with (BASE/'VERDICT.md').open('a') as f: f.write(f'\n### HƯỚNG {n}: {title}\n\n- giả thuyết: {hyp}\n- lệnh: `{cmd}`\n- output thật:\n```text\n{s}\n```\n- kết luận: {conclusion}.\n')
def history():
 lines=[]
 for name,args in [('diff.patch',('diff',PREV,SHA)),('numstat.txt',('diff','--numstat',PREV,SHA)),('diff-pr947.patch',('diff',MASTER,SHA)),('numstat-pr947.txt',('diff','--numstat',MASTER,SHA))]:lines.append(f'{name} byte_match={git(*args)==(BASE/name).read_bytes()}')
 hint=BASE/'verdict-cu/pr896-review-7-codex-HINT.patch'; paths=re.findall(r'^\+\+\+ (\S+)',hint.read_text(),re.M)
 scratch=Path(tempfile.mkdtemp(prefix='pr896-r8-hint-parent-')); (OUT/'hint-parent-path.txt').write_text(str(scratch))
 for p in paths:
  t=scratch/p; t.parent.mkdir(parents=True,exist_ok=True); t.write_bytes(blob(PREV,p))
 p=subprocess.run(['patch','--batch','--fuzz=0','-p0','-i',str(hint)],cwd=scratch,capture_output=True,text=True)
 (OUT/'prior-hint-apply.log').write_text(p.stdout+p.stderr); lines += [f'hint_paths={len(paths)} apply_rc={p.returncode}',p.stdout.strip()]
 for path in paths: lines.append(f'{path} full_byte_match={(scratch/path).read_bytes()==blob(SHA,path)}')
 a=(scratch/'ops/reviews/README.md').read_text().splitlines(keepends=True); b=(ROOT/'ops/reviews/README.md').read_text().splitlines(keepends=True)
 import difflib
 delta=''.join(difflib.unified_diff(a,b)); (OUT/'prior-hint-readme-extra.diff').write_text(delta)
 changes=[x for x in delta.splitlines() if x.startswith(('+','-')) and not x.startswith(('+++','---'))]; lines+=['README beyond hint:',*changes]
 artifact=git('diff-tree','--no-commit-id','--name-only','-r','54021fb').decode().splitlines(); lines.append(f'54021fb paths={len(artifact)} only_round7_artifacts={all(p.startswith("ops/reviews/pr896-review-7-codex/") or p=="ops/reviews/pr896-review-7-codex-verdict.md" for p in artifact)}')
 for src,dest in [('VERDICT.md','ops/reviews/pr896-review-7-codex-verdict.md'),('HINT.patch','ops/reviews/pr896-review-7-codex/HINT.patch')]:lines.append(f'prior {src} stored_byte_match={(BASE/("verdict-cu/pr896-review-7-codex-"+src)).read_bytes()==blob(SHA,dest)}')
 record(3,'Tái áp hint lượt 7 và đối chiếu byte','Hint bị áp thiếu/khác, hoặc snapshot/diff không đúng SHA.','python3 review_evidence/measure.py history',lines)
class UniqueLoader(yaml.SafeLoader): pass
def unique(loader,node,deep=False):
 d={}
 for k,v in loader.construct_pairs(node,deep=deep):
  if k in d:raise ValueError('duplicate key '+str(k))
  d[k]=v
 return d
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique)
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def integrity():
 receipts=sorted((ROOT/'ops/reviews').glob('*.receipt.yaml')); declarations=receipts+list((ROOT/'ops/reviews').glob('*-legacy-caveats.yaml'))+list((ROOT/'ops/land').glob('*-land-evidence.yaml'))
 changed=git('diff','--name-only',MASTER,SHA).decode().splitlines(); paths=set(p.relative_to(ROOT).as_posix() for p in declarations)|{p for p in changed if p.endswith(('.yaml','.yml'))}
 errors=[]; ids=[]; hashes=[]
 for p in sorted(paths):
  try:
   d=yaml.load((ROOT/p).read_text(),Loader=UniqueLoader)
   if p.endswith('.receipt.yaml'):
    caveats=[c.get('id') for c in d.get('verdict_usage_caveats',[]) or []]; ids.append([p,caveats])
    if len(caveats)!=len(set(caveats)): errors.append([p,'duplicate ids',caveats])
  except Exception as e:errors.append([p,str(e)])
 for p in declarations:
  for d in walk(yaml.safe_load(p.read_text())):
   if 'verdict_sha256' not in d or not d.get('verdict_path'):continue
   path=ROOT/d['verdict_path']; actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
   hashes.append(dict(source=str(p.relative_to(ROOT)),target=d['verdict_path'],sha256=actual,ok=actual==d['verdict_sha256']))
   if not hashes[-1]['ok']:errors.append(hashes[-1])
 frozen={}
 for n in ast.parse((ROOT/'ops/bien_nhan_v2.py').read_text()).body:
  if isinstance(n,(ast.Assign,ast.AnnAssign)):
   for t in (n.targets if isinstance(n,ast.Assign) else [n.target]):
    if isinstance(t,ast.Name) and t.id in ['ALLOWLIST_CUTOVER','NO_DA_DO']:frozen[t.id]=ast.literal_eval(n.value)
 frozen_checks=[]
 for group,items in frozen.items():
  for p,h in items.items():
   p='ops/reviews/'+p; data=(ROOT/p).read_bytes(); h=h if isinstance(h,str) else h[0]
   frozen_checks.append(dict(group=group,path=p,hash_match=hashlib.sha256(data).hexdigest()==h,master_match=data==blob(MASTER,p),prev_match=data==blob(PREV,p)))
 modified=[p for p in git('diff','--name-only','--diff-filter=M',MASTER,SHA).decode().splitlines() if p.endswith('-verdict.md') or p.endswith('/VERDICT.md')]
 allhash={d['verdict_sha256'] for p in receipts for d in walk(yaml.safe_load(p.read_text())) if isinstance(d.get('verdict_sha256'),str)}
 flat=list((ROOT/'ops/reviews').glob('*-verdict.md')); unclaimed=[p.name for p in flat if hashlib.sha256(p.read_bytes()).hexdigest() not in allhash]
 result=dict(yaml_parsed=len(paths),receipts=len(receipts),hashes=hashes,ids=ids,frozen=frozen_checks,modified_historical_verdicts=modified,unclaimed=unclaimed,errors=errors)
 (OUT/'integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 record(4,'Toàn vẹn YAML, hash và biên nhận v1','Phá YAML, trùng caveat, đổi byte verdict hoặc receipt miễn trừ.','python3 review_evidence/measure.py integrity',[f'yaml_parsed={len(paths)} receipts={len(receipts)} duplicate_ids={[(p,c) for p,c in ids if len(c)!=len(set(c))]}',f'verdict_path_hashes={len(hashes)} all_match={all(x["ok"] for x in hashes)}',f'flat_verdicts={len(flat)} unclaimed={unclaimed}',f'frozen_groups={ {k:len(v) for k,v in frozen.items()} } all_hash_and_bytes_match={all(x["hash_match"] and x["master_match"] and x["prev_match"] for x in frozen_checks)}',f'modified_historical_verdicts={modified}',f'errors={errors}'])
if __name__=='__main__':
 import sys
 globals()[sys.argv[1]]()
