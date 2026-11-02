from pathlib import Path
import yaml, re, unicodedata, json
from audit import ROOT,OUT

def norm(s):return unicodedata.normalize('NFD',s).encode('ascii','ignore').decode().lower().replace('đ','d')
def scalars(node,keys=()):
 if isinstance(node,yaml.MappingNode):
  for k,v in node.value:yield from scalars(v,keys+(k.value,))
 elif isinstance(node,yaml.SequenceNode):
  for i,v in enumerate(node.value):yield from scalars(v,keys+(str(i),))
 elif isinstance(node,yaml.ScalarNode):yield keys,node.start_mark.line+1,node.value
paths=sorted(set(list((ROOT/'ops/reviews').glob('*.receipt.yaml'))+list((ROOT/'ops/reviews').glob('*-legacy-caveats.yaml'))+list((ROOT/'ops/land').glob('pr896-*.yaml'))))
status=[];anchored=[]
for p in paths:
 for keys,line,s in scalars(yaml.compose(p.read_text())):
  n=norm(s)
  if not re.search(r'\bchua\b|khong.{0,60}(review|to tien)|chi.{0,30}(nhanh|branch)|not.{0,25}(merged|reviewed|ancestor)',n):continue
  if keys[-1] in ['id','receipt_id','evidence_url'] or s in ['CHUA DAT','KHONG_DO_DUOC']:continue
  entry={'path':str(p.relative_to(ROOT)),'field':'.'.join(keys),'line':line,'text':s}
  anchored_flag=bool(re.search(r'anh chup|tai moc|moc lich su|tai reviewed_sha|luc ghi|luc review|tai thoi|lich su tai|snapshot|tai commit|tai [0-9a-f]{7,40}|tren [0-9a-f]{7,40}|cham.{0,40}[0-9a-f]{7,40}',n))
  (anchored if anchored_flag else status).append(entry)
readme=[]
for i,l in enumerate((ROOT/'ops/reviews/README.md').read_text().splitlines(),1):
 if re.search(r'\bchua\b|khong.{0,60}(review|to tien)|chi.{0,30}(nhanh|branch)',norm(l)):readme.append({'line':i,'text':l})
(OUT/'status-inventory.json').write_text(json.dumps({'unanchored_candidates':status,'anchored_candidates':anchored,'readme':readme},ensure_ascii=False,indent=2))
for name,arr in [('unanchored',status),('anchored',anchored),('readme',readme)]:
 (OUT/f'status-{name}.txt').write_text('\n'.join((f'{x.get("path","README")}:{x["line"]} {x.get("field","")} {x["text"]}') for x in arr))
print(f'yaml_paths={len(paths)} unanchored_candidates={len(status)} anchored_candidates={len(anchored)} readme_candidates={len(readme)}')
