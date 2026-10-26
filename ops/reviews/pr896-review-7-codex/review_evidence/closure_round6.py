import hashlib,json,re,subprocess,yaml
from pathlib import Path
from audit import ROOT,OUT,SHA,PREV,MASTER,git,blob,record
from states import at,rc,scalars
rows=[]
for stem in ['wp461-review-1-codex-verdict','wp523-r15-review-1-codex-verdict']:
 path='ops/reviews/'+stem+'.receipt.yaml';d=yaml.safe_load((ROOT/path).read_text())
 for keys in [('anchor','cuong_do'),('lich_su_ban_ung_vien','ghi_chu')]:
  s=at(d,keys);m=re.search(r'Loi khai lich su trong blob tai ([0-9a-f]{40}): (.*?) Do lai tai ([0-9a-f]{40}):',s);assert m
  old=at(yaml.safe_load(blob(m[1],path)),keys)
  q=re.search(r'git merge-base --is-ancestor ([0-9a-f]{40}) ([0-9a-f]{40}) va voi ([0-9a-f]{40}) deu rc=0',s);assert q
  targets=[q[2],q[3],MASTER,SHA]
  last=git('log','-1','--format=%H',m[1],'--',path).decode().strip()
  rows.append({'receipt':path,'field':'.'.join(keys),'line':next(l for k,l,v in scalars(yaml.compose((ROOT/path).read_text())) if k==keys),'anchor':m[1],'last_receipt_commit_at_anchor':last,'anchor_touches_receipt':last==m[1],'historical_text_matches':' '.join(str(old).split())==' '.join(m[2].split()),'source_oid':q[1],'ancestry':[{ 'target':t,'rc':rc('merge-base','--is-ancestor',q[1],t)} for t in targets],'receipt_in_master':bool(git('ls-tree',MASTER,'--',path).strip())})
side=[];readme=(ROOT/'ops/reviews/README.md').read_text().splitlines();supp=yaml.safe_load((ROOT/'ops/reviews/pr896-review-6-legacy-caveats.yaml').read_text())
for c in supp['caveats']:
 path=c['receipt_path'];s=c['mo_ta'];a=re.search(r'blob ([0-9a-f]{40})',s)[1];q=re.search(r'git merge-base --is-ancestor ([0-9a-f]{40}) ([0-9a-f]{40}) va voi ([0-9a-f]{40}) deu rc=0',s);assert q
 old=yaml.safe_load(blob(a,path));key=('receipt_khong_khai','0') if 'doctor' in path else ('truy_xuat_ghi_chu',)
 match=[l for l in readme if l.startswith('| `'+Path(c['verdict_path']).name+'` | `'+c['id']+'` |')]
 side.append({'receipt':path,'field':'.'.join(key),'anchor':a,'anchor_touches_receipt':git('log','-1','--format=%H',a,'--',path).decode().strip()==a,'source_scalar':at(old,key),'frozen_bytes_match_anchor':blob(a,path)==(ROOT/path).read_bytes(),'verdict_hash_match':hashlib.sha256((ROOT/c['verdict_path']).read_bytes()).hexdigest()==c['verdict_sha256'],'readme_rows':len(match),'exact_readme_description':len(match)==1 and s in match[0],'oid':q[1],'ancestry':[{ 'target':t,'rc':rc('merge-base','--is-ancestor',q[1],t)} for t in [q[2],q[3],MASTER,SHA]]})
# All older ancestry claims re-measured independently, including supplementary v1 notes.
anchors=[];measurements=[]
paths=list((ROOT/'ops/reviews').glob('*.receipt.yaml'))+list((ROOT/'ops/reviews').glob('*-legacy-caveats.yaml'))
for p in paths:
 for keys,line,s in scalars(yaml.compose(p.read_text())):
  a=re.search(r'Anh chup lich su tai commit ghi bien nhan ([0-9a-f]{40}):',s)
  if a:
   anchors.append({'path':str(p.relative_to(ROOT)),'field':'.'.join(keys),'oid':a[1],'anchor_adds_receipt':a[1] in git('log','--format=%H','--diff-filter=A',SHA,'--',str(p.relative_to(ROOT))).decode().splitlines()})
  for q in re.finditer(r'git merge-base --is-ancestor ([0-9a-f]{7,40}) ([0-9a-f]{7,40}) va voi ([0-9a-f]{7,40}) deu rc=0',s):
   for t in [q[2],q[3],MASTER,SHA]:measurements.append({'path':str(p.relative_to(ROOT)),'field':'.'.join(keys),'source':q[1],'target':t,'rc':rc('merge-base','--is-ancestor',q[1],t)})
result={'round6_historical_fields':rows,'round6_v1_corrections':side,'older_anchors':anchors,'all_measurements':measurements}
(OUT/'closure-round6.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
summary=f'round6_historical_fields={len(rows)} all_text_and_anchor_match={all(r["historical_text_matches"] and r["anchor_touches_receipt"] for r in rows)}\nround6_v1_corrections={len(side)} all_frozen_hash_row_match={all(r["anchor_touches_receipt"] and r["frozen_bytes_match_anchor"] and r["verdict_hash_match"] and r["readme_rows"]==1 and r["exact_readme_description"] for r in side)}\nolder_historical_fields={len(anchors)} all_anchor_adds_receipt={all(r["anchor_adds_receipt"] for r in anchors)}\nall_ancestry_measurements={len(measurements)} all_rc0={all(r["rc"]==0 for r in measurements)}\n'
for r in rows:summary+=r['receipt']+' / '+r['field']+' anchor='+r['anchor']+' source='+r['source_oid']+' rc='+str([x['rc'] for x in r['ancestry']])+'\n'
for r in side:summary+=r['receipt']+' / '+r['field']+' anchor='+r['anchor']+' source='+r['oid']+' rc='+str([x['rc'] for x in r['ancestry']])+'\n'
record(6,'Đóng finding ancestry lượt 6 và đo lại các mốc cũ','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/closure_round6.py; git show <anchor>:<receipt>; git log -1 <anchor> -- <receipt>; git merge-base --is-ancestor <OID> <target>',summary)
