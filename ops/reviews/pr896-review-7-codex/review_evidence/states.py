from pathlib import Path
import hashlib,json,re,subprocess,yaml
from audit import ROOT,OUT,SHA,PREV,MASTER,git,blob,record

def scalars(node,keys=()):
 if isinstance(node,yaml.MappingNode):
  for k,v in node.value:yield from scalars(v,keys+(k.value,))
 elif isinstance(node,yaml.SequenceNode):
  for i,v in enumerate(node.value):yield from scalars(v,keys+(str(i),))
 elif isinstance(node,yaml.ScalarNode):yield keys,node.start_mark.line+1,node.value

def at(d,keys):
 for k in keys:d=d[int(k)] if isinstance(d,list) else d[k]
 return d

def rc(*a):return subprocess.run(['git','-C',str(ROOT),*a],capture_output=True).returncode

def ancestry():
 entries=[];measurements=[]
 for p in sorted((ROOT/'ops/reviews').glob('*.receipt.yaml')):
  name=str(p.relative_to(ROOT))
  for keys,line,s in scalars(yaml.compose(p.read_text())):
   a=re.search(r'Anh chup lich su tai commit ghi bien nhan ([0-9a-f]{40}): (.*?) (?:Do lai tai|Sau moc ay,)',s,re.S)
   if not a:continue
   historical=yaml.safe_load(blob(a[1],name))
   try:
    if 'verdict_usage_caveats' in keys:
     now=yaml.safe_load(p.read_text()); ci=keys.index('verdict_usage_caveats'); current=at(now,keys[:ci+2]); cid=current['id']; past=next(c for c in historical['verdict_usage_caveats'] if c['id']==cid);old=at(past,keys[ci+2:])
    else:old=at(historical,keys)
   except (TypeError,KeyError,StopIteration) as e:
    old='FIELD_NOT_AT_SAME_PATH: '+repr(e);print(name,keys,old,flush=True)
   exists=True;identical=' '.join(str(old).split())==' '.join(a[2].split())
   addition=git('log','--format=%H','--diff-filter=A',SHA,'--',name).decode().splitlines()
   first_receipt=a[1] in addition
   entry={'receipt':name,'field':'.'.join(keys),'line':line,'anchor':a[1],'same_historical_scalar':identical,'receipt_introduced_at_anchor':first_receipt}
   if not identical:entry.update({'original':old,'claimed':a[2]})
   entries.append(entry)
   for m in re.finditer(r'git merge-base --is-ancestor ([0-9a-f]{7,40}) ([0-9a-f]{7,40}) va voi ([0-9a-f]{7,40}) deu rc=0',s):
    for target in [m[2],m[3],MASTER,SHA]:measurements.append({'receipt':name,'field':'.'.join(keys),'source':m[1],'target':target,'rc':rc('merge-base','--is-ancestor',m[1],target)})
 selected=[]
 for n,field in [('ci-windows-review-5',['chuoi_verdict_ghi_chu']),('doctrine-scan-review-1',['anchor','gioi_han']),('doctrine-scan-review-2',['anchor','gioi_han']),('doctrine-scan-review-3',['anchor','gioi_han']),('wp538-review-1',['anchor','gioi_han']),('wp538-review-2',['anchor','gioi_han']),('wp540-review-1',['anchor','gioi_han'])]:
  name=n+'-claude-verdict.receipt.yaml';s=at(yaml.safe_load((ROOT/'ops/reviews'/name).read_text()),field)
  m=re.search(r'git merge-base --is-ancestor ([0-9a-f]{40})',s);a=re.search(r'commit ghi bien nhan ([0-9a-f]{40})',s)
  selected.append({'receipt':name,'field':'.'.join(field),'anchor':a[1],'oid':m[1],'rc_master':rc('merge-base','--is-ancestor',m[1],MASTER),'rc_candidate':rc('merge-base','--is-ancestor',m[1],SHA)})
 # Supplementary ancestry entry covers frozen v1.
 supp=yaml.safe_load((ROOT/'ops/reviews/pr896-review-4-legacy-caveats.yaml').read_text())
 for x in supp['caveats']:
  for m in re.finditer(r'git merge-base --is-ancestor ([0-9a-f]{7,40}) ([0-9a-f]{7,40}) va voi ([0-9a-f]{7,40}) deu rc=0',x['mo_ta']):
   for target in [m[2],m[3],MASTER,SHA]:measurements.append({'receipt':x['receipt_path'],'field':'supplementary','source':m[1],'target':target,'rc':rc('merge-base','--is-ancestor',m[1],target)})
 exceptions={oid:{t:rc('merge-base','--is-ancestor',oid,t) for t in [MASTER,SHA]} for oid in ['03f12ac63284dd814dcf14664968af4872ef7f8a','4bc9432','604b8d9','82359c4','2e4183b','1a276a1','d308b0b']}
 data={'historical_anchors':entries,'measurements':measurements,'old_seven':selected,'exceptions':exceptions}
 (OUT/'states-ancestry.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 output=f'historical_fields={len(entries)} same_original={sum(x["same_historical_scalar"] for x in entries)} receipt_added_at_anchor={sum(x["receipt_introduced_at_anchor"] for x in entries)}\nancestry_measurements={len(measurements)} all_rc0={all(x["rc"]==0 for x in measurements)}\nold_seven='+json.dumps(selected,ensure_ascii=False,indent=2)+'\nexceptions='+json.dumps(exceptions)+'\nanchor_mismatches='+json.dumps([x for x in entries if not x['same_historical_scalar'] or not x['receipt_introduced_at_anchor']],ensure_ascii=False)
 record(6,'Mốc lịch sử và ancestry của mọi trường đã neo','python3 review_evidence/states.py ancestry; git merge-base --is-ancestor <source> <target>; git log --diff-filter=A '+SHA+' -- <receipt>',output,'KHÔNG PHẢI LỖI' if all(x['rc']==0 for x in measurements) and all(x['same_historical_scalar'] and x['receipt_introduced_at_anchor'] for x in entries) else 'CẦN KIỂM TRA')
def reviews():
 old_eight=[];new_two=[]
 for p in sorted((ROOT/'ops/reviews').glob('*.receipt.yaml')):
  for c in yaml.safe_load(p.read_text()).get('verdict_usage_caveats',[]) or []:
   s=c.get('mo_ta',c.get('noi_dung',''));m=re.search(r'Sau moc ay, (\S+-verdict.md) da review ban va tai ([0-9a-f]{40})',s)
   if not m:continue
   a=re.search(r'commit ghi bien nhan ([0-9a-f]{40}):',s)
   old_eight.append(check_review(m[1],m[2],a[1],p.name))
 for num,oid,anchor in [('870','06a50c5feea77c2654f31edd26efeed7eeee62f5','600b6ce90d97d5f606272af137d7153b7b32133c'),('889','094e8d17ae4dfcf21dca63702c9262267bdc072c','e02d0c31986f6ba5019fef21311a939f2d9c2f17')]:
  for turn in [2,3]:new_two.append(check_review(f'pr{num}-review-{turn}-codex-verdict.md',oid,anchor,f'pr{num}-review-1'))
 d={'old_eight':old_eight,'new_two_four_reviews':new_two}
 (OUT/'states-reviews.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
 output='old_eight_count='+str(len(old_eight))+'\n'+json.dumps(d,ensure_ascii=False,indent=2)
 record(7,'Verdict kế tiếp của các trạng thái chưa review','python3 review_evidence/states.py reviews; sha256sum <verdict>; git cat-file -e <historical>:<next-verdict>',output,'KHÔNG PHẢI LỖI')
def check_review(name,oid,anchor,source):
 p=ROOT/'ops/reviews'/name;data=p.read_bytes();d=yaml.safe_load(p.with_suffix('.receipt.yaml').read_text());header=data.decode().splitlines()[:20]
 return {'source':source,'verdict':name,'expected_sha':oid,'receipt_sha_match':d['reviewed_sha']==oid,'verdict_header_sha_match':any('reviewed_sha' in l and oid in l for l in header),'hash':hashlib.sha256(data).hexdigest(),'hash_match':hashlib.sha256(data).hexdigest()==d['verdict_sha256'],'result':d['verdict'],'counts':[d.get('so_'+k) for k in ['p0','p1','p2','p3']],'next_absent_at_anchor_rc':rc('cat-file','-e',anchor+':ops/reviews/'+name)}
if __name__=='__main__':
 import sys
 globals()[sys.argv[1]]()
