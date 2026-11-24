import ast,collections,hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W.parent/'repo';D=R/'ops/reviews/wp1236-r10-soan'
def read(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(W/'m1.jsonl');b=read(W/'m2.jsonl');h=read(W/'h.jsonl');p=read(D/'pilot_c2d606b_kq.jsonl');hdr=p.pop(0)
A={x['id']:x for x in a+h};P={x['id']:x for x in p};assert len(A)==927 and set(A)==set(P)
assert (W/'m1.jsonl').read_bytes()==(W/'m2.jsonl').read_bytes()
assert all(A[k]['sha256']==P[k]['sha256'] for k in A)
sm=json.loads((R/'ops/reviews/wp1236-spec-r10-6-codex/measurement_summary.json').read_text())
chosen={x['id'] for x in p if x['id'].startswith('kho:') and x['phan_hang']=='SONG'}
for x in p:
 if x['phan_hang']=='VO_CAN':chosen.add(x['id'])
for op in sorted({x['op'] for x in p}):
 group=[x for x in p if x['op']==op and x['phan_hang']=='GIET']
 if group:chosen.add(group[0]['id'])
# Include every first killed case and mixed error+kill outcome as evidence of current classifier.
for ca in sorted({x['giet'][0] for x in p if x['giet']}):chosen.add(next(x['id'] for x in p if x['giet']==[ca]))
chosen=sorted(chosen);(W/'pilot_subset.jsonl').write_text(''.join(json.dumps(A[k],ensure_ascii=False)+'\n' for k in chosen))
r={'deterministic':True,'m1_sha256':sha(W/'m1.jsonl'),'m2_sha256':sha(W/'m2.jsonl'),'counts':{'manifest':len(a),'regression':len(h),'total':len(A),'operators':dict(collections.Counter(x['op'] for x in a))},'pilot_header':hdr,'pilot_counts':dict(collections.Counter(x['phan_hang'] for x in p)),'pilot_per_op_survivors':dict(collections.Counter(x['op'] for x in p if x['phan_hang']=='SONG' and x['op']!='kho')),'all_source_hashes_match':True,'frozen_hashes':{n:sha(D/n) for n in ['quet_dot_bien.py','kho_dot_bien_reviewer_luot6.jsonl','pilot_c2d606b_kq.jsonl']},'subset_count':len(chosen),'subset_ids':chosen,'selection':'all34 historical survivors (25 non-equivalent+9 equivalent),all10 VO_CAN,one kill per available operator,one kill per distinct first targeted case; purposive nonstatistical sample','subset_expected_counts':dict(collections.Counter(P[k]['phan_hang'] for k in chosen)),'anchor_line_lengths':dict(collections.Counter(len(x['cu'].splitlines()) for x in read(D/'kho_dot_bien_reviewer_luot6.jsonl')))}
(W/'generation_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in r.items() if k not in ['subset_ids','pilot_header']},ensure_ascii=False,indent=2))
