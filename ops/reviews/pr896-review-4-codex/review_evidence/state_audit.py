import json, re, subprocess, yaml
from pathlib import Path
root=Path('cay-kho');rd=root/'ops/reviews';result={'review':[], 'ancestry':[]}
def lines(p,needle):
 return [i for i,l in enumerate(p.read_text().splitlines(),1) if needle in l]
def first(p):
 return subprocess.check_output(['git','-C',str(root),'log','--reverse','--diff-filter=A','--format=%H','--',str(p.relative_to(root))],text=True).splitlines()[0]
for n in range(1,7):
 name=f'pr455-bien-nhan-v2-review-{n}-codex-verdict.receipt.yaml'
 p=rd/name;d=yaml.safe_load(p.read_text());nc='codex' if n+1<7 else 'gpt6astra'
 nxt=rd/f'pr455-bien-nhan-v2-review-{n+1}-{nc}-verdict.md'
 caveat=next(c for c in d['verdict_usage_caveats'] if 'VA-CAN-REVIEW-LAI' in c['id'])
 result['review'].append(dict(receipt=name,id=caveat['id'],line=lines(p,caveat['id'])[0],introduced=first(p),next_verdict=nxt.name,next_reviewed_sha=yaml.safe_load(nxt.with_suffix('.receipt.yaml').read_text())['reviewed_sha']))
for name,cid,nxt in [('pr896-review-1-codex','P2-DA-VA-CHUA-REVIEW-LAI','pr896-review-2-codex'),('pr915-review-1-codex','HEAD-CHUA-SACH-CAN-REVIEW-LAI','pr896-review-2-codex')]:
 p=rd/(name+'-verdict.receipt.yaml');nd=yaml.safe_load((rd/(nxt+'-verdict.receipt.yaml')).read_text())
 result['review'].append(dict(receipt=p.name,id=cid,line=lines(p,cid)[0],introduced=first(p),next_verdict=nxt+'-verdict.md',next_reviewed_sha=nd['reviewed_sha']))
selected=['assurance-ho-model-review-1-claude','ci-windows-review-5-claude',*[f'doctrine-scan-review-{n}-claude' for n in range(1,4)],'don-nhanh-base-review-1-codex',*[f'pr508-review-{n}-codex' for n in range(1,6)],'r330-rig-quyet-mau-audit-nguoi','wp538-review-1-claude','wp538-review-2-claude','wp540-review-1-claude','wp541-review-1-claude','wp541-review-2-claude',*[f'wp678-spec-review-{n}-claude' for n in range(7,13)]]
for name in selected:
 p=rd/(name+'-verdict.receipt.yaml');d=yaml.safe_load(p.read_text())
 blob=re.search(r'/blob/([0-9a-f]{40})/',d['evidence_url'])[1]
 oid=d['reviewed_sha'] if name.startswith('wp678-spec') else blob
 codes={base:subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',oid,base],capture_output=True).returncode for base in ['101263f','2e4183b']}
 print(name,'measured_oid=',oid,'ancestor_rc=',codes)
 result['ancestry'].append(dict(receipt=p.name,schema=d['schema_version'],oid=oid,ancestor_rc=codes,introduced=first(p)))
print('review_claims_with_later_review=',len(result['review']))
for x in result['review']:print(json.dumps(x,ensure_ascii=False))
print('proven_ancestry_receipts=',len(result['ancestry']))
for name,needle in [('pr896-review-3-codex-verdict.md','HINT.patch luot 3 chua ap'),('pr896-review-1-codex-verdict.md','CHUA review lai'),('pr915-review-1-codex-verdict.md','chua review lai')]:
 p=rd/'README.md'
 for i,l in enumerate(p.read_text().splitlines(),1):
  if name in l and needle in l:print('README_STALE',i,l)
result['readme_r3_stale_lines']=lines(rd/'README.md','HINT.patch luot 3 chua ap')
Path('review_evidence/proven-states.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
