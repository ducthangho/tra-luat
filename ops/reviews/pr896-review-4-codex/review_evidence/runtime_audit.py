from pathlib import Path
from datetime import datetime
import json,hashlib,subprocess,yaml
root=Path('cay-kho')
for name in ['pr896-review-2-codex','pr896-review-3-codex']:
 d=root/'ops/reviews'/name; receipt=yaml.safe_load((d.parent/(name+'-verdict.receipt.yaml')).read_text());r=json.loads((d/'run/run.json').read_text())
 events=r['model_phuc_vu'];identity=receipt['model_reviewer_identity']
 elapsed=(datetime.fromisoformat(r['ket_thuc_utc'])-datetime.fromisoformat(r['bat_dau_utc'])).total_seconds()
 checks=dict(head_matches=r['head']==receipt['reviewed_sha'],run_id_matches=r['run_id']==identity['session_run_id'],surface_matches=r['execution_surface']==identity['surface'],prompt_hash_matches=hashlib.sha256((d/'PROMPT.md').read_bytes()).hexdigest()==r['prompt_sha256'],elapsed_matches=round(elapsed,3)==r['thoi_luong_giay'])
 print(name,'version=',r['version'],'status=',r['trang_thai'],'rc=',r['ma_thoat'],'clean=',r['worktree_sach'],'elapsed=',elapsed,'stored_duration=',r['thoi_luong_giay'],'checks=',checks)
 print('events=',len(events),'distinct_response_ids=',len({x['response_id'] for x in events}),'event_types=',sorted({x['su_kien'] for x in events}),'stored_models=',sorted({x['model'] for x in events}),'model_state=',r['model_phuc_vu_trang_thai'])
 for stream in ['stdout','stderr']:
  raw=(d/'run'/(stream+'.log')).read_bytes()
  print(stream,'bytes=',len(raw),'metadata_bytes_match=',len(raw)==r[stream+'_byte'],'metadata_hash_match=',hashlib.sha256(raw).hexdigest()==r[stream+'_sha256'])
 result=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=d,text=True,capture_output=True)
 Path('review_evidence/'+name+'-checksums.log').write_text(result.stdout+result.stderr)
 print('SHA256SUMS_rc=',result.returncode,'OK_count=',sum(l.endswith(': OK') for l in result.stdout.splitlines()))
 print('omitted_metadata=',(d/'OMITTED.txt').read_text().strip().replace('\n',' | '))
