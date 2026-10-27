from measure import *
lines=[]
p=ROOT/'ops/land/pr823-wp802-provenance/readback-comment-6247520447.json';d=json.loads(p.read_text());b=d['body'];lines.append(f'{p.relative_to(ROOT)} id={d.get("id")} round5={bool(re.search(r"(lượt|luot)\s*5",b,re.I))} head5c6c7a8={"5c6c7a8" in b} runb3d8a108={"b3d8a108" in b}')
lines.extend(l for l in b.splitlines() if 'b3d8a108' in l or '**Codex lượt 5/5' in l)
for pr,oid,anchor in [(870,'06a50c5feea77c2654f31edd26efeed7eeee62f5','600b6ce90d97d5f606272af137d7153b7b32133c'),(889,'094e8d17ae4dfcf21dca63702c9262267bdc072c','e02d0c31986f6ba5019fef21311a939f2d9c2f17')]:
 for n in [2,3]:
  p=ROOT/f'ops/reviews/pr{pr}-review-{n}-codex-verdict.receipt.yaml';d=yaml.safe_load(p.read_text());v=(ROOT/d['verdict_path']).read_bytes();r=subprocess.run(['git','-C',str(ROOT),'cat-file','-e',anchor+':'+d['verdict_path']],capture_output=True);lines.append(f'pr{pr} luot{n}: head={d["reviewed_sha"]} expected_match={d["reviewed_sha"]==oid} verdict={d["verdict"]} header_match={oid in v.decode().splitlines()[1]} hash_match={hashlib.sha256(v).hexdigest()==d["verdict_sha256"]} absent_at_anchor_rc={r.returncode}')
record(14,'Nguồn comment cùng lượt và các đính chính review kế tiếp','Caveat mới dẫn nhầm comment/run hoặc đính chính trạng thái chưa review dẫn sai head.','python3 review_evidence/correction_sources.py',lines)
