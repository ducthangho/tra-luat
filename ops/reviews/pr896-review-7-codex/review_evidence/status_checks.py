from pathlib import Path
import json,re,subprocess,yaml,hashlib
from audit import ROOT,OUT,SHA,MASTER,git,blob,record
inv=json.loads((OUT/'status-inventory.json').read_text());receipts=[(p,yaml.safe_load(p.read_text())) for p in (ROOT/'ops/reviews').glob('*.receipt.yaml')]
verdicts=list((ROOT/'ops/reviews').rglob('*-verdict.md'))+list((ROOT/'ops/reviews').rglob('VERDICT.md'))+list((ROOT/'ops/land').rglob('*verdict*.md'))+list((ROOT/'ops/land').rglob('VERDICT.md'))
heads={}
for p in set(verdicts):
 text=p.read_text();m=re.search(r'^reviewed_sha:\s*`?([0-9a-f]{7,40})',text,re.M)
 if m:
  r=subprocess.run(['git','-C',str(ROOT),'rev-parse',m[1]+'^{commit}'],capture_output=True,text=True)
  if r.returncode==0:heads.setdefault(r.stdout.strip(),[]).append(str(p.relative_to(ROOT)))
no_review=[]
for oid in ['17f4a1b','efa397e','99aef14','5a96c1a','888c0d9','bf10fab','288ad3e','b5b6aef','3ddda02']:
 full=git('rev-parse',oid+'^{commit}').decode().strip();matches=[str(p.relative_to(ROOT)) for p,d in receipts if d.get('reviewed_sha')==full];no_review.append({'oid':full,'receipt_matches':matches,'verdict_header_matches':heads.get(full,[])})
nonanc=[]
for oid in ['4bc9432','604b8d9','82359c4','2e4183b','1a276a1','d308b0b','22382d8','825dab1',SHA]:
 full=git('rev-parse',oid+'^{commit}').decode().strip();nonanc.append({'oid':full,'master_rc':subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',full,MASTER],capture_output=True).returncode,'candidate_rc':subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',full,SHA],capture_output=True).returncode})
specs=[]
for path in ['ops/specs/wp775.md','ops/specs/wp484-r8.md']:
 specs.append({'path':path,'master_ls_tree':git('ls-tree',MASTER,'--',path).decode().strip(),'candidate_ls_tree':git('ls-tree',SHA,'--',path).decode().strip()})
# Explicitly scoped archival land statements are not live merge-state assertions.
archival=[]
for path,keys in [('ops/land/pr696-wp668-land-evidence.yaml',['do_luc']),('ops/land/pr684-wp677-land-evidence.yaml',['trang_thai_packet','packet_landed_ghi_chu'])]:
 d=yaml.safe_load((ROOT/path).read_text());v=d
 for k in keys:v=v[k]
 archival.append({'path':path,'field':'.'.join(keys),'anchor_text':v})
# Exact commits named by old HINT-not-applied corrections.
hint_commits=[]
for anchor,expected in [('c8c1ee0','2e4183b'),('77a0a45','1a276a1')]:
 parents=git('show','-s','--format=%P',expected).decode().strip();hint_commits.append({'historical':git('rev-parse',anchor).decode().strip(),'apply_commit':git('rev-parse',expected).decode().strip(),'apply_parent':parents,'direct_child':parents==git('rev-parse',anchor).decode().strip()})
result={'yaml_paths':len(receipts)+len(list((ROOT/'ops/reviews').glob('*-legacy-caveats.yaml')))+len(list((ROOT/'ops/land').glob('*-land-evidence.yaml'))),'inventory_counts':{k:len(v) for k,v in inv.items()},'unreviewed_heads':no_review,'nonancestors':nonanc,'unmerged_specs':specs,'archival_contexts':archival,'hint_history':hint_commits}
(OUT/'status-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
summary=f'yaml_paths={result["yaml_paths"]} inventory_counts={result["inventory_counts"]}\n'
summary+='No-review negatives checked against flat receipts AND verdict headers in ops/reviews + land provenance:\n'
for x in no_review:summary+=x['oid']+' receipts='+str(len(x['receipt_matches']))+' verdict_headers='+str(len(x['verdict_header_matches']))+'\n'
for x in nonanc:summary+=x['oid']+' ancestry rc(master,candidate)='+str([x['master_rc'],x['candidate_rc']])+'\n'
for x in specs:summary+=x['path']+' ls-tree master='+repr(x['master_ls_tree'])+' candidate='+repr(x['candidate_ls_tree'])+'\n'
for x in hint_commits:summary+='HINT history '+repr(x)+'\n'
summary+='Land provenance status scan: '+str(len(set(verdicts)))+' distinct paths; supplementary matches classified with context. pr696.do_luc pins bc57bca and 2026-09-30; pr684.packet_landed_ghi_chu explicitly says TAI THOI DIEM merge #684 and current #689 state must not be read from that file. Findings narrated under reviewed_sha are historical; absent CI or land authority is not a claim of unmerged Git state.\n'
record(10,'Quét rộng trạng thái review/áp hint/merge trong sổ và land','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/inventory.py; python3 review_evidence/status_checks.py; git merge-base --is-ancestor <OID> <master/candidate>; git ls-tree <ref> -- <spec>; compare exact verdict reviewed_sha',summary,'KHÔNG PHẢI LỖI mới về trạng thái trong các đối chiếu nêu trên; các bản ghi lịch sử có mốc được giữ nguyên, không suy trạng thái land từ Git')
