from measure import ROOT,OUT
import yaml,json,re,unicodedata,hashlib

def norm(s):return unicodedata.normalize('NFD',s.replace('đ','d').replace('Đ','D')).encode('ascii','ignore').decode().lower()
def scalars(n,keys=()):
 if isinstance(n,yaml.MappingNode):
  for k,v in n.value:yield from scalars(v,keys+(k.value,))
 elif isinstance(n,yaml.SequenceNode):
  for i,v in enumerate(n.value):yield from scalars(v,keys+(str(i),))
 elif isinstance(n,yaml.ScalarNode):yield keys,n.start_mark.line+1,n.value
paths=sorted(set(list((ROOT/'ops/reviews').glob('*.receipt.yaml'))+list((ROOT/'ops/reviews').glob('*-legacy-caveats.yaml'))+list((ROOT/'ops/land').glob('*-land-evidence.yaml')))); rows=[]
for p in paths:
 for keys,line,s in scalars(yaml.compose(p.read_text())):
  n=norm(s)
  if not re.search(r'\bchua\b|\bnot\b.{0,60}(merg|review|ancestor|appl)|\bkhong\b.{0,70}(to tien|review|ap dung|ap patch)|\bchi\b.{0,25}(nhanh|branch)',n):continue
  if keys[-1] in ['id','receipt_id','evidence_url']:continue
  historical=bool(re.search(r'anh chup|tai moc|moc lich su|tai reviewed_sha|luc ghi|luc review|tai thoi|lich su tai|snapshot|tai commit|tai [0-9a-f]{7,40}|tren [0-9a-f]{7,40}|cham.{0,40}[0-9a-f]{7,40}',n))
  rows.append(dict(path=str(p.relative_to(ROOT)),field='.'.join(keys),line=line,text=s,historical=historical))
readme=[dict(line=i,text=l) for i,l in enumerate((ROOT/'ops/reviews/README.md').read_text().splitlines(),1) if re.search(r'\bchua\b|\bnot\b.{0,60}(merg|review|ancestor|appl)|\bkhong\b.{0,70}(to tien|review|ap dung|ap patch)|\bchi\b.{0,25}(nhanh|branch)',norm(l))]
verdicts=[]; seen={}
for p in sorted(set(list((ROOT/'ops/reviews').rglob('*.md'))+list((ROOT/'ops/land').rglob('*.md')))):
 if not re.search('verdict',p.name,re.I):continue
 h=hashlib.sha256(p.read_bytes()).hexdigest();seen.setdefault(h,[]).append(str(p.relative_to(ROOT)))
 if len(seen[h])>1:continue
 text=p.read_text(errors='replace'); lines=text.splitlines()
 hits=[dict(line=i,text=s) for i,s in enumerate(lines,1) if re.search(r'codex[_ -](service|cli|desktop)|service/API|execution[_ -]?surface|reviewer[_ -]?surface|bề mặt.{0,70}(cli|service|desktop)',s,re.I)]
 neg=[dict(line=i,text=s) for i,s in enumerate(lines,1) if re.search(r'\bchua\b.{0,70}(review|ap|to tien|merge)|\bnot\b.{0,60}(merg|review|ancestor|appl)',norm(s))]
 verdicts.append(dict(path=str(p.relative_to(ROOT)),sha256=h,surface_mentions=hits,negative_mentions=neg))
runtime=[]
for p in sorted(ROOT.rglob('run.json')):
 try:d=json.loads(p.read_bytes())
 except (ValueError,UnicodeDecodeError):continue
 runtime.append(dict(path=str(p.relative_to(ROOT)),run_id=d.get('run_id'),head=d.get('head'),execution_surface=d.get('execution_surface'),program=d.get('lenh',{}).get('chuong_trinh')))
(OUT/'inventory.json').write_text(json.dumps(dict(scalars=rows,readme=readme,verdicts=verdicts,duplicates=seen,runtime=runtime),ensure_ascii=False,indent=2))
for name,arr in [('status-unanchored',[x for x in rows if not x['historical']]),('status-anchored',[x for x in rows if x['historical']])]:
 (OUT/(name+'.txt')).write_text('\n'.join(f"{x['path']}:{x['line']} {x['field']} {x['text']}" for x in arr))
(OUT/'surface-hits.txt').write_text('\n'.join(f"{x['path']}:{hit['line']} {hit['text']}" for x in verdicts for hit in x['surface_mentions']))
(OUT/'land-verdict-negative.txt').write_text('\n'.join(f"{x['path']}:{hit['line']} {hit['text']}" for x in verdicts if x['path'].startswith('ops/land') for hit in x['negative_mentions']))
print(f'yaml_files={len(paths)} status_scalars={len(rows)} unanchored_candidates={sum(not x["historical"] for x in rows)} readme_candidates={len(readme)} distinct_verdict_contents={len(verdicts)} surface_hits={sum(len(x["surface_mentions"]) for x in verdicts)} run_json_files={len(runtime)}')
