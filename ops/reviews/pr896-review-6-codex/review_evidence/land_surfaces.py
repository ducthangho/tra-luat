from pathlib import Path
import hashlib,json,re,yaml
from audit import ROOT,OUT,MASTER,PREV,blob,record
cases=[('pr832-wp831','verdict-luot7/wp831-g1-luot7-codex-verdict.md',6,'verdict-luot7/run.json'),('pr848-wp744','verdicts/wp744-g3-luot1-codex-verdict.md',36,'verdicts/run-f65e544e.json'),('pr862-wp748-r21','verdicts/wp748-r21-luot1-codex-verdict.md',3,'verdicts/wp748-r21-luot1-codex-transcript.txt')]
results=[]
for stem,vname,line,rname in cases:
 prefix='ops/land/'+stem+'-provenance/';vp=prefix+vname;rp=prefix+rname;v=(ROOT/vp).read_bytes();source=(ROOT/rp).read_bytes();land=ROOT/('ops/land/'+stem+'-land-evidence.yaml');d=yaml.safe_load(land.read_text());r={'verdict':vp,'line':line,'self_claim':v.decode().splitlines()[line-1],'source':rp,'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest(),'same_master':v==blob(MASTER,vp),'same_prev':v==blob(PREV,vp),'land_review':d.get('review')}
 if rname.endswith('.json'):
  run=json.loads(source);r['runtime']={k:run[k] for k in ['run_id','head','provider','execution_surface','transport','lenh']};r['header_sha_matches_run']=run['head'] in '\n'.join(v.decode().splitlines()[:20])
 else:r['runtime']={'transcript_header':source.decode().splitlines()[:13]};r['land_receipt_explicit_cli']=d['review']['luot_1']['reviewer']
 results.append(r)
(OUT/'land-surfaces.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
output='runtime JSON inventory includes run-*.json: 120 records (48 literal run.json, including duplicates/snapshots; not 120 independent runs).\n'
for r in results:output+=f"{r['verdict']}:{r['line']}\nSELF: {r['self_claim']}\nSOURCE: {r['source']}\n"+json.dumps(r['runtime'],ensure_ascii=False)+f"\nsha256={r['sha256']} bytes={r['bytes']} same_master={r['same_master']} same_prev={r['same_prev']}\n"
output+='Two raw run IDs above belong to the exact verdict head and same review round. For #862 round 1, DO NOT borrow run-f0909b38.json: that is round 2 on the same head; the round-1 transcript and land.review.luot_1 identify direct codex exec. No explicit surface correction/caveat for these three verdicts was found in their land evidence or supplementary review caveats.\nExcluded: #849 round4/5 are explicitly corrected by review.luot_cuoi.reviewer (LOI TU PHAN LOAI; trust CLI header); run-03c4f6be is round6, not proof for round4/5. #823 round5 and #877 round2: no matching runtime with explicit contrary surface identified; no assertion of actual surface. Generic API/local-shell wording in other verdicts does not establish codex_service.'
record(11,'Surface ngoài ops/reviews, đối chiếu đúng lượt trong hồ sơ land','python3 review_evidence/land_surfaces.py; read run*.json, exact verdict lines and land.review; sha256sum <verdict>',output,'LỖI P1 surface-service-cli-trong-ho-so-land: 3 verdict tự khai service, nguồn CLI của chính lượt chứng minh khác; các băm lịch sử giữ nguyên')
