import os,subprocess,json,re,hashlib
from pathlib import Path
S=Path(__file__).resolve().parent; R=S/'cay-kho'; A=R/'ops/reviews/pr1075-review-1-codex'; N=S/'nguon/review1075a'; E=S/'evidence'
sha=lambda b:hashlib.sha256(b).hexdigest()
errors=[]; mapping=[]; accounted=set()
for f in sorted(A.rglob('*')):
 if not f.is_file(): continue
 p=f.relative_to(A).as_posix()
 if p in ('SHA256SUMS','OMITTED.txt'): continue
 if p=='launcher.out': src='launcher.json'
 elif p.startswith('run/'): src='runs/71490d5a/'+p[4:]
 elif p.startswith('evidence/') and p.endswith('.py'): src=p.split('/')[-1]
 else: src=p
 ok=(N/src).is_file() and f.read_bytes()==(N/src).read_bytes()
 if not ok: errors.append('copy mismatch '+p)
 accounted.add(src); mapping.append({'archive':p,'source':src,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes()),'equal':ok})
omit={}
for line in (A/'OMITTED.txt').read_text().splitlines():
 m=re.match(r'([^\t]+)\tsha256 ([a-f0-9]{64})\tbytes (\d+)\t',line)
 if m: omit[m[1]]={'sha256':m[2],'bytes':int(m[3])}
source={f.relative_to(N).as_posix() for f in N.rglob('*') if f.is_file()}
missing=sorted(source-accounted); omissions=[]
for p in missing:
 b=(N/p).read_bytes(); row={'source':p,'bytes':len(b),'sha256':sha(b)}; row['declared_correct']=omit.get(p)=={'bytes':len(b),'sha256':sha(b)}; omissions.append(row)
 if not row['declared_correct']: errors.append('undeclared/wrong omission '+p)
entries=[]
for line in (A/'SHA256SUMS').read_text().splitlines():
 h,p=line.split('  ',1); p=Path(p).as_posix(); entries.append(p)
 if not (A/p).is_file() or sha((A/p).read_bytes())!=h: errors.append('manifest hash '+p)
actual={f.relative_to(A).as_posix() for f in A.rglob('*') if f.is_file()}-{'SHA256SUMS'}
if set(entries)!=actual or len(set(entries))!=len(entries): errors.append('manifest coverage')
p=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=A,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); (E/'sha256sum.log').write_bytes(p.stdout)
flat=(R/'ops/reviews/pr1075-review-1-codex-verdict.md').read_bytes(); same=flat==(N/'VERDICT.md').read_bytes()
if not same or p.returncode: errors.append('flat/sha256sum')
r={'source_files':len(source),'copies':len(mapping),'archive_files':len(actual)+1,'manifest_entries':len(entries),'manifest_missing':sorted(actual-set(entries)),'manifest_extra':sorted(set(entries)-actual),'sha256sum_rc':p.returncode,'flat_equal':same,'flat_sha256':sha(flat),'flat_bytes':len(flat),'omissions':omissions,'unaccounted_source_files':sorted(source-accounted-set(omit)),'errors':errors}
(E/'bytes.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n'); (E/'byte-mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(r,ensure_ascii=False,indent=2)); assert not errors
