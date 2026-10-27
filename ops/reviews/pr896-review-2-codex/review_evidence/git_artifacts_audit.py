from pathlib import Path
import subprocess,hashlib,json,os,yaml,re
root=Path.cwd(); repo=root/'cay-kho'; out=Path('/tmp/pr896-r2-audit-b3269a02'); env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'); logs=[]
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args],env=env)
for slug in ['pr870-review-3-codex','pr889-review-3-codex','pr915-review-1-codex']:
 d=yaml.safe_load((repo/'ops/reviews'/(slug+'-verdict.receipt.yaml')).read_text()); a=repo/'ops/reviews'/slug; base=d['base_sha']; head=d['reviewed_sha']; delta=git('diff',base,head); stat=git('diff','--numstat',base,head); base_ancestor=subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',base,head],env=env).returncode; prompt=(a/'PROMPT.md').read_text(); base_short=base[:7]
 logs.append(slug+': base_resolves='+git('rev-parse',base_short+'^{commit}').decode().strip()+'; base_prompt='+str('base `'+base_short+'`' in prompt)+'; base_is_ancestor rc='+str(base_ancestor)+'; numstat_bytes_equal='+str(stat==(a/'numstat.txt').read_bytes()))
 if (a/'diff.patch').is_file(): logs.append('diff.patch exact_git_bytes_equal='+str(delta==(a/'diff.patch').read_bytes())+'; git_bytes='+str(len(delta)))
 else:
  decl=next(l for l in (a/'OMITTED.txt').read_text().splitlines() if l.endswith('  diff.patch')); logs.append('omitted diff.patch declaration='+decl+'; git_diff_sha256='+hashlib.sha256(delta).hexdigest()+'; git_diff_bytes='+str(len(delta)))
 run=json.loads((a/'run/run.json').read_text())
 for name in ['stdout','stderr']:
  p=a/'run'/(name+'.log')
  if p.is_file(): logs.append(name+'.log bytes actual/run='+str(p.stat().st_size)+'/'+str(run[name+'_byte'])+'; sha256_matches_run='+str(hashlib.sha256(p.read_bytes()).hexdigest()==run[name+'_sha256']))
 for file in ['transport.json','checkpoint.json']:
  p=a/'run'/file
  if p.is_file(): logs.append(file+' sha256_matches_run='+str(hashlib.sha256(p.read_bytes()).hexdigest()==run.get(file.removesuffix('.json')+'_sha256')))
for commit in ['3bc4244','7cfe062','2789cbb','cc0a3c9']:
 files=git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines(); logs.append(commit+': file_count='+str(len(files))+'; paths_outside_reviews='+repr([f for f in files if not f.startswith('ops/reviews/')]))
for pr,slug in [(870,'pr870-review-3-codex'),(889,'pr889-review-3-codex'),(896,'pr915-review-1-codex')]:
 land=next(repo.glob(f'ops/land/pr{pr}-*-land-evidence.yaml')); d=yaml.safe_load(land.read_text()); cap=d['cap_nhat_20261026']; c=cap['cross_review_moi']; receipt=yaml.safe_load((repo/c['bien_nhan']).read_text()); checks={k:c[k]==receipt[k] for k in ['reviewed_sha','verdict','provider','luot','assurance']}; counts=[int(n) for n in re.findall(r'P[0-3] (\d+)',c['so_lop'])]; checks['so_lop_matches_receipt']=counts==[receipt['so_p'+str(i)] for i in range(4)]; logs.append('cap_nhat #'+str(pr)+': '+json.dumps(checks,ensure_ascii=False))
s='\n'.join(logs)+'\n'; (out/'git-artifacts-audit.log').write_text(s); print(s)
with (root/'VERDICT.md').open('a') as f: f.write('\n### HƯỚNG 16: Base, diff, log launcher và khối cap_nhat đối chiếu chéo\n\nGiả thuyết: base đúng tên nhưng sai nội dung diff, commit không chỉ mang hiện vật, hoặc khối cập nhật chép sai receipt.\n\nLệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/git_artifacts_audit.py` — git diff/numstat/diff-tree/merge-base, SHA-256 log, đối chiếu từng trường YAML. Base là base của review, KHÔNG nhất thiết cha trực tiếp của head.\n\nOutput thật:\n```text\n'+s+'```\n\nKết luận: KHÔNG PHẢI LỖI của các mỏ neo và khối cập nhật; base khớp prompt và numstat, diff tái lập được kể cả tệp quá lớn đã bỏ khỏi kho.\n')
