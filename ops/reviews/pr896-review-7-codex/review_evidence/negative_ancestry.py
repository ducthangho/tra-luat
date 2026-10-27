from pathlib import Path
import yaml, unicodedata,re,json,subprocess,collections
from audit import ROOT,OUT,MASTER,SHA
from states import scalars,rc

def norm(s):return unicodedata.normalize('NFD',s.replace('đ','d').replace('Đ','D')).encode('ascii','ignore').decode().lower()
rows=[]
for p in sorted((ROOT/'ops/reviews').glob('*.receipt.yaml')):
 d=yaml.safe_load(p.read_text());oid=re.search(r'/blob/([0-9a-f]{7,40})/',d.get('evidence_url',''))
 for keys,line,s in scalars(yaml.compose(p.read_text())):
  n=norm(s)
  if not re.search(r'(khong|chua).{0,100}(master|canonical|to tien)|(chi|only).{0,80}(nhanh|branch)',n):continue
  if re.search(r'anh chup|tai moc|moc lich su|khi bien nhan|tai reviewed|luc ghi|luc review|tai thoi|snapshot|tai commit|tai [0-9a-f]{7,40}',n):continue
  if keys[-1]=='id' or 'finding' in '.'.join(keys) or 'phat_hien' in '.'.join(keys):continue
  rows.append({'path':str(p.relative_to(ROOT)),'field':'.'.join(keys),'line':line,'text':s,'evidence_oid':oid[1] if oid else None,'rc_master':rc('merge-base','--is-ancestor',oid[1],MASTER) if oid else None,'rc_candidate':rc('merge-base','--is-ancestor',oid[1],SHA) if oid else None})
(OUT/'negative-ancestry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for i,x in enumerate(rows):
 if x['rc_master']!=0 or 'ci-g5-cong-cu-chia-manh' in x['path']:continue
 print(i,Path(x['path']).name+':'+str(x['line']),x['field'], 'evidence='+str(x['evidence_oid']), 'rc='+str([x['rc_master'],x['rc_candidate']]),x['text'][:320])
print('all_rows',len(rows),'with_evidence_ancestor_master',sum(x['rc_master']==0 for x in rows))
