from measure import *
import unicodedata

def scalars(n,keys=()):
 if isinstance(n,yaml.MappingNode):
  for k,v in n.value:yield from scalars(v,keys+(k.value,))
 elif isinstance(n,yaml.SequenceNode):
  for i,v in enumerate(n.value):yield from scalars(v,keys+(str(i),))
 elif isinstance(n,yaml.ScalarNode):yield keys,n.start_mark.line+1,n.value

def at(d,keys):
 for k in keys:d=d[int(k)] if isinstance(d,list) else d[k]
 return d

def rc(*args):return subprocess.run(['git','-C',str(ROOT),*args],capture_output=True).returncode

def norm(s):return unicodedata.normalize('NFD',s.replace('đ','d').replace('Đ','D')).encode('ascii','ignore').decode().lower()

def anchors():
 fields=[]; measurements=[]; reviews=[]; lines=[]
 for p in sorted((ROOT/'ops/reviews').glob('*.receipt.yaml')):
  path=str(p.relative_to(ROOT)); now=yaml.safe_load(p.read_text())
  for keys,line,s in scalars(yaml.compose(p.read_text())):
   a=re.search(r'Anh chup lich su tai commit ghi bien nhan ([0-9a-f]{40}): (.*?) (?:Do lai tai|Sau moc ay,)',s,re.S)
   if a:
    historical=yaml.safe_load(blob(a[1],path))
    if 'verdict_usage_caveats' in keys:
     i=keys.index('verdict_usage_caveats'); current=at(now,keys[:i+2]); past=next((c for c in historical['verdict_usage_caveats'] if isinstance(c,dict) and c.get('id')==current['id']),None)
     if past is None:
      old=historical.get('anchor',{}).get('gioi_han','')
     else:old=at(past,keys[i+2:])
    else:old=at(historical,keys)
    additions=git('log','--format=%H','--diff-filter=A',SHA,'--',path).decode().splitlines()
    fields.append(dict(path=path,field='.'.join(keys),line=line,anchor=a[1],text_matches=' '.join(str(old).split())==' '.join(a[2].split()),added_at_anchor=a[1] in additions,original=old,claimed=a[2]))
   for m in re.finditer(r'git merge-base --is-ancestor ([0-9a-f]{7,40}) ([0-9a-f]{7,40}) va voi ([0-9a-f]{7,40}) deu rc=0',s):
    for target in [m[2],m[3],MASTER,SHA]:measurements.append(dict(path=path,field='.'.join(keys),source=m[1],target=target,rc=rc('merge-base','--is-ancestor',m[1],target)))
  for c in now.get('verdict_usage_caveats',[]) or []:
   s=c.get('mo_ta',c.get('noi_dung',''));m=re.search(r'Sau moc ay, (\S+-verdict.md) da review ban va tai ([0-9a-f]{40})',s)
   if m:
    vd=ROOT/'ops/reviews'/m[1]; rd=yaml.safe_load(vd.with_suffix('.receipt.yaml').read_text());anchor=re.search(r'commit ghi bien nhan ([0-9a-f]{40}):',s)[1]
    reviews.append(dict(source=path,next=m[1],sha=m[2],receipt_sha_match=rd['reviewed_sha']==m[2],header_sha_match=any(m[2] in l and 'reviewed_sha' in l for l in vd.read_text().splitlines()[:20]),hash_match=hashlib.sha256(vd.read_bytes()).hexdigest()==rd['verdict_sha256'],absent_at_anchor_rc=rc('cat-file','-e',anchor+':ops/reviews/'+m[1])))
 for p in (ROOT/'ops/reviews').glob('*-legacy-caveats.yaml'):
  for c in yaml.safe_load(p.read_text())['caveats']:
   s=c['mo_ta']
   for m in re.finditer(r'git merge-base --is-ancestor ([0-9a-f]{7,40}) ([0-9a-f]{7,40}) va voi ([0-9a-f]{7,40}) deu rc=0',s):
    for target in [m[2],m[3],MASTER,SHA]:measurements.append(dict(path=str(p.relative_to(ROOT)),field=c['id'],source=m[1],target=target,rc=rc('merge-base','--is-ancestor',m[1],target)))
 lines += [f'historical_scalar_fields={len(fields)} exact_original_text={sum(x["text_matches"] for x in fields)} all_creation_anchor_match={all(x["added_at_anchor"] for x in fields)}',f'ancestry_measurements={len(measurements)} all_rc0={all(x["rc"]==0 for x in measurements)}',f'next_review_corrections={len(reviews)} all_sha_hash_header_match={all(x["receipt_sha_match"] and x["header_sha_match"] and x["hash_match"] and x["absent_at_anchor_rc"]==128 for x in reviews)}']
 lines += [str(x) for x in reviews]
 (OUT/'historical-anchors.json').write_text(json.dumps(dict(fields=fields,measurements=measurements,reviews=reviews),ensure_ascii=False,indent=2))
 record(9,'Đo lại mọi mốc lịch sử và đính chính chưa review của các receipt','Neo nhầm commit đầu, chép sai câu lịch sử hoặc chỉ sang sai lượt review tiếp.','python3 review_evidence/states.py anchors',lines,'KHÔNG PHẢI LỖI mới thuộc hai lớp săn. So byte lời diễn giải lịch sử không tự kết luận sai trạng thái; 12 trường wp678 diễn giải lại điều kiện cục bộ/đã đẩy và thời gian, 1 caveat pr508 diễn giải anchor.gioi_han tại mốc (ID caveat chưa có ở commit gốc). Chi tiết original/claimed trong historical-anchors.json; không gọi 48 trường là nguyên văn byte-exact')

def scan_status():
 inv=json.loads((OUT/'inventory.json').read_text()); receipts=[(p,yaml.safe_load(p.read_text())) for p in (ROOT/'ops/reviews').glob('*.receipt.yaml')]
 lines=[f'negative_status_scalars={len(inv["scalars"])} readme_candidates={len(inv["readme"])}']; rows=[]
 # Bind exact reviewed SHA, including nested directories and land provenance, rather than branch names.
 heads={}
 for v in inv['verdicts']:
  p=ROOT/v['path'];s=p.read_text(errors='replace')
  for m in re.finditer(r'(?im)^\s*(?:[-*]\s*)?(?:reviewed_sha|reviewed.commit|Reviewed SHA)\s*[:=]\s*[`*\s]*([0-9a-f]{7,40})',s):
   r=subprocess.run(['git','-C',str(ROOT),'rev-parse',m[1]+'^{commit}'],capture_output=True,text=True)
   if r.returncode==0:heads.setdefault(r.stdout.strip(),[]).append(v['path'])
 for short in ['17f4a1b','efa397e','99aef14','5a96c1a','888c0d9','bf10fab','288ad3e','b5b6aef','3ddda02']:
  oid=git('rev-parse',short+'^{commit}').decode().strip(); matching=[p.name for p,d in receipts if d.get('reviewed_sha')==oid];vs=heads.get(oid,[]); rows.append(dict(oid=oid,receipts=matching,verdicts=vs));lines.append(f'unreviewed_candidate {oid} receipts={len(matching)} verdict_headers={len(vs)}')
 for short in ['4bc9432','604b8d9','82359c4','2e4183b','1a276a1','d308b0b','22382d8','825dab1','05bc12e','54021fb',SHA]:
  oid=git('rev-parse',short+'^{commit}').decode().strip(); lines.append(f'ancestry {oid} master_rc={rc("merge-base","--is-ancestor",oid,MASTER)} candidate_rc={rc("merge-base","--is-ancestor",oid,SHA)}')
 for path in ['ops/specs/wp775.md','ops/specs/wp484-r8.md']:
  lines.append(f'{path} ls-tree master={git("ls-tree",MASTER,"--",path).decode().strip()!r} candidate={git("ls-tree",SHA,"--",path).decode().strip()!r}')
 for p,k in [('ops/land/pr696-wp668-land-evidence.yaml',['do_luc']),('ops/land/pr684-wp677-land-evidence.yaml',['trang_thai_packet','packet_landed_ghi_chu']),('ops/land/pr554-wp541-land-evidence.yaml',['CAP_NHAT_1'])]:
  d=yaml.safe_load((ROOT/p).read_text());v=at(d,k)
  if isinstance(v,dict):v={key:value for key,value in v.items() if re.search(r'moc|luc|ngay|ghi_chu|thoi',key)}
  lines.append(p+' historical_context='+json.dumps(v,ensure_ascii=False))
 for a,b in [('c8c1ee0','2e4183b'),('77a0a45','1a276a1')]:lines.append(f'HINT applied {b} parent_is_{a}={git("show","-s","--format=%P",b).strip()==git("rev-parse",a).strip()}')
 (OUT/'status-checks.json').write_text(json.dumps(dict(unreviewed=rows,heads=heads),ensure_ascii=False,indent=2))
 record(10,'Quét lớp trạng thái review / áp hint / ancestry / merge','Câu phủ định hiện hành đã bị Git hoặc verdict mới bác bỏ.','python3 review_evidence/states.py scan_status; git merge-base --is-ancestor; git ls-tree',lines,'KHÔNG PHẢI LỖI mới qua các đối chiếu này; âm tính về review chỉ có giá trị trong tập hiện vật, không chứng minh ngoài kho không có review. Mốc CAP_NHAT_1, do_luc, packet_landed_ghi_chu được xét theo cả khối; chưa land không được đồng nhất với chưa merge')
if __name__=='__main__':
 import sys
 globals()[sys.argv[1]]()
