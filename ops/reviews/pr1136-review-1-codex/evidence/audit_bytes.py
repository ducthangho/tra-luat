from pathlib import Path
import hashlib,re,subprocess,json,os
S=Path(__file__).resolve().parent;R=S/'cay-kho';E=S/'evidence';os.environ['GIT_CONFIG_GLOBAL']=str(S/'audit.gitconfig');os.environ['GIT_CONFIG_NOSYSTEM']='1';os.environ['PYTHONDONTWRITEBYTECODE']='1'
def sha(b):return hashlib.sha256(b).hexdigest()
D=R/'ops/reviews/pr1131-review-1-codex';out={}
for label,src,dest,run in [('counted',S/'nguon/review1131b',D,'260f271e'),('failed',S/'nguon/review1131a',D/'luot-hong-xac-thuc','ee42b27f')]:
 repo={p.relative_to(dest).as_posix():p for p in dest.rglob('*') if p.is_file() and 'luot-hong-xac-thuc' not in p.relative_to(dest).parts}
 source={p.relative_to(src).as_posix():p for p in src.rglob('*') if p.is_file()}
 matched=[];bad=[];used=set();extra=[]
 for n,p in repo.items():
  if n in ('SHA256SUMS','OMITTED.txt'):continue
  origin='launcher.json' if n=='launcher.out' else 'runs/'+run+'/'+n[4:] if n.startswith('run/') else n
  if n.startswith('evidence/') and Path(n).name in source and (n.endswith('.py') or n.endswith('/audit.gitconfig')):origin=Path(n).name
  if origin not in source:extra.append([n,origin]);continue
  used.add(origin);record={'repo':n,'source':origin,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
  (matched if p.read_bytes()==source[origin].read_bytes() else bad).append(record)
 omitted={}
 for line in (dest/'OMITTED.txt').read_text().splitlines():
  m=re.match(r'([^\t]+)\tsha256 ([0-9a-f]{64})\tbytes (\d+)\t',line)
  if m:omitted[m[1]]={'sha256':m[2],'bytes':int(m[3])}
 missing=sorted(set(source)-used); undeclared=[n for n in missing if n not in omitted];omitted_bad=[]
 for n in missing:
  if n in omitted and omitted[n]!={'sha256':sha(source[n].read_bytes()),'bytes':source[n].stat().st_size}:omitted_bad.append(n)
 manifest={}; dup=[]
 manifest_path=dest/'SHA256SUMS' if (dest/'SHA256SUMS').exists() else D/'SHA256SUMS'
 for line in manifest_path.read_text().splitlines():
  h,n=line.split(maxsplit=1);n=n.removeprefix('*').removeprefix('./')
  if manifest_path.parent!=dest:
   if not n.startswith('luot-hong-xac-thuc/'):continue
   n=n[len('luot-hong-xac-thuc/'):]
  if n in manifest:dup.append(n)
  manifest[n]=h
 # Parent manifest can cover failed child; count all actual files under this manifest.
 actual={p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file() and p!=dest/'SHA256SUMS'}
 r=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=manifest_path.parent,capture_output=True)
 (E/f'bytes-{label}-sha256sum.txt').write_bytes(r.stdout+r.stderr)
 out[label]={'source_count':len(source),'stored_count':len(matched),'matched':matched,'mismatch':bad,'generated_or_unknown':extra,'missing_source':missing,'omitted_metadata':omitted,'undeclared_missing':undeclared,'omitted_mismatch':omitted_bad,'declared_but_not_missing':sorted(set(omitted)-set(missing)),'sha256sum_rc':r.returncode,'manifest_count':len(manifest),'manifest_uncovered':sorted(actual-set(manifest)),'manifest_extra':sorted(set(manifest)-actual),'manifest_duplicates':dup}
 print(label,json.dumps({k:v for k,v in out[label].items() if k not in ('matched','omitted_metadata')},ensure_ascii=False),flush=True)
flat=R/'ops/reviews/pr1131-review-1-codex-verdict.md';out['flat']={'matches':flat.read_bytes()==(D/'VERDICT.md').read_bytes()==(S/'nguon/review1131b/VERDICT.md').read_bytes(),'sha256':sha(flat.read_bytes()),'bytes':flat.stat().st_size}
diff=subprocess.check_output(['git','diff','180039c','0e824fe'],cwd=R)
out['diff_reproduction']={'bytes':len(diff),'sha256':sha(diff),'matches_a':diff==(S/'nguon/review1131a/DIFF.patch').read_bytes(),'matches_b':diff==(S/'nguon/review1131b/DIFF.patch').read_bytes()}
p=D/'evidence/gates-progress.txt';b=p.read_bytes();out['whitespace']={'sha256':sha(b),'bytes':len(b),'source_matches':b==(S/'nguon/review1131b/evidence/gates-progress.txt').read_bytes(),'trailing_whitespace_lines':[i for i,x in enumerate(b.splitlines(),1) if x.endswith((b' ',b'\t'))]}
for n in ['flat','diff_reproduction','whitespace']:print(n,json.dumps(out[n],ensure_ascii=False))
(E/'bytes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
with (S/'VERDICT.md').open('a') as f:
 f.write('\nĐối chiếu byte — `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py`:\n```json\n'+json.dumps({k:{kk:vv for kk,vv in v.items() if kk not in ('matched','omitted_metadata')} for k,v in out.items()},ensure_ascii=False,indent=2)+'\n```\n')
