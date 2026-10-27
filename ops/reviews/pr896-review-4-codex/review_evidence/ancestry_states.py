import json,re,subprocess,yaml
from pathlib import Path
root=Path('cay-kho');results=[]
state=re.compile(r'chưa (?:land|merge)|CHUA (?:land|merge)|chưa (?:tới|vào) [`\"]?master|CHUA (?:co|CO) (?:tren master|:) |khong phai master|chi nam tren nhanh|CHƯA (?:land|merge)|CHƯA (?:phải tổ tiên|ở trên|vào)|quan hệ tổ tiên với master chưa có',re.I)
history=re.compile(r'lúc|luc |khi (?:ghi|viet|viết|biên|bien|review)|tại (?:thời|mốc|lúc)|tai (?:moc|thoi)|423b4ba|thời điểm|thoi diem|thoi_diem|lượt.{0,20}(?:lúc|tại)',re.I)
def walk(d,path=''):
 if isinstance(d,dict):
  for k,v in d.items():yield from walk(v,path+'.'+k if path else k)
 elif isinstance(d,list):
  for i,v in enumerate(d):yield from walk(v,path+f'[{i}]')
 elif isinstance(d,str):yield path,d
for p in sorted((root/'ops/reviews').glob('*.receipt.yaml')):
 d=yaml.safe_load(p.read_text()); found=[]
 for key,s in walk(d):
  if not (key.startswith('anchor.') or key=='truy_xuat_ghi_chu' or key=='spec_ghi_chu' or key.startswith('verdict_usage_caveats')):continue
  if state.search(s) and not history.search(s):found.append((key,s))
 if not found:continue
 match=re.search(r'/blob/([0-9a-f]{40})/',d.get('evidence_url',''))
 oid=match[1] if match else None
 if not oid:continue
 r=subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',oid,'101263f'],capture_output=True)
 if r.returncode:continue
 item=dict(receipt=p.name,schema=d.get('schema_version'),evidence_commit=oid,ancestor_master_rc=r.returncode,fields=found)
 results.append(item)
 print(p.name,'schema=',d.get('schema_version'),'evidence_commit=',oid,'ancestor_master_rc=0')
 for key,s in found:print(' ',key,':',s)
print('measured_suspect_receipts=',len(results))
Path('review_evidence/ancestry-states.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
