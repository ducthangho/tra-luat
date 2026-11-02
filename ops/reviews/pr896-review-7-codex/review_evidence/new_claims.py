from pathlib import Path
import hashlib,json,re,subprocess,yaml
from audit import ROOT,OUT,SHA,PREV,git,blob,record
p='ops/reviews/pr896-review-6-codex-verdict.receipt.yaml';d=yaml.safe_load((ROOT/p).read_text());run_path=d['model_reviewer_identity']['run_json'];run=json.loads((ROOT/run_path).read_text());v=(ROOT/d['verdict_path']).read_bytes();art=ROOT/'ops/reviews/pr896-review-6-codex'
check={}
check['receipt_verdict_bytes_sha256']={'bytes':len(v),'hash':hashlib.sha256(v).hexdigest(),'matches':len(v)==d['verdict_bytes'] and hashlib.sha256(v).hexdigest()==d['verdict_sha256']}
check['run_id_head_surface']={k:run[k] for k in ['run_id','head','ref','execution_surface','transport','ma_thoat','trang_thai','worktree_sach','thoi_luong_giay']}
check['prompt_sha256_match']=hashlib.sha256((art/'PROMPT.md').read_bytes()).hexdigest()==run['prompt_sha256']
check['reviewed_tree_match']=git('rev-parse',d['reviewed_sha']+'^{tree}').decode().strip()==d['reviewed_tree']
check['model_events']={'count':len(run['model_phuc_vu']),'response_ids':len(set(x['response_id'] for x in run['model_phuc_vu'])),'models':sorted(set(x['model'] for x in run['model_phuc_vu']))}
for name in ['stdout','stderr']:
 b=(art/'run'/f'{name}.log').read_bytes();check[name+'_run_hash_and_byte_match']=hashlib.sha256(b).hexdigest()==run[name+'_sha256'] and len(b)==run[name+'_byte']
m=re.search(r'/blob/([0-9a-f]{40})/(.+)',d['evidence_url']);check['evidence_blob_matches']=blob(m[1],m[2])==v;check['evidence_oid']=m[1]
check['receipt_addition_commit']=git('log','--diff-filter=A','--format=%H',SHA,'--',p).decode().splitlines()
check['artifact_commit_parent']=git('show','-s','--format=%P','825dab1').decode().strip();check['receipt_commit_parent']=git('show','-s','--format=%P',SHA).decode().strip()
readme=(ROOT/'ops/reviews/README.md').read_text().splitlines()
check['new_caveats_rows']=[{'id':c['id'],'rows':sum(l.startswith('| `'+Path(d['verdict_path']).name+'` | `'+c['id']+'` |') for l in readme),'exact_description':any(l.startswith('| `'+Path(d['verdict_path']).name+'` | `'+c['id']+'` |') and c['mo_ta'] in l for l in readme)} for c in d['verdict_usage_caveats']]
p2=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=art,capture_output=True,text=True);(OUT/'round6-sha256sums.log').write_text(p2.stdout+p2.stderr);check['artifact_sha256sums']={'rc':p2.returncode,'ok_count':sum(l.endswith(': OK') for l in p2.stdout.splitlines()),'failed':[l for l in p2.stdout.splitlines() if not l.endswith(': OK')],'stderr':p2.stderr}
land=yaml.safe_load((ROOT/'ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml').read_text());l5=land['cap_nhat_20261026_luot6']['cross_review_moi'];check['land_round6_sha_and_receipt_match']=l5['reviewed_sha']==d['reviewed_sha'] and l5['bien_nhan']==p and l5['hien_vat']==d['verdict_path'] and l5['verdict']==d['verdict']
(OUT/'new-claims.json').write_text(json.dumps(check,ensure_ascii=False,indent=2))
record(9,'Lời khai mới do 05bc12e ghi thêm','python3 review_evidence/new_claims.py; sha256sum -c SHA256SUMS; git show <OID>:<path>',json.dumps(check,ensure_ascii=False,indent=2),'KHÔNG PHẢI LỖI ở những lời khai mới này; mô tả finding thuộc verdict 22382d8, không coi là tự khai surface hoặc trạng thái hiện hành của mọi receipt')
