import hashlib,json,re,yaml
from pathlib import Path
from audit import ROOT,OUT,MASTER,PREV,blob,record
cases=[('pr823-wp802','verdict-luot5/wp802-g1-luot5-codex-verdict.md',6),('pr877-wp854','verdicts/wp854-g1-luot2-codex-verdict.md',11)]
runs=json.loads((OUT/'all-runtime-index.json').read_text());rows=[]
for stem,vname,line in cases:
 vp='ops/land/'+stem+'-provenance/'+vname;lp='ops/land/'+stem+'-land-evidence.yaml';b=(ROOT/vp).read_bytes();land=yaml.safe_load((ROOT/lp).read_text());head=re.search(r'^reviewed_sha:\s*([0-9a-f]{40})',b.decode(),re.M)[1]
 r={'land':lp,'verdict':vp,'self_line':line,'self_claim':b.decode().splitlines()[line-1],'head':head,'hash':hashlib.sha256(b).hexdigest(),'same_master':b==blob(MASTER,vp),'same_prev':b==blob(PREV,vp),'matching_runtime_records':[x for x in runs if x['head']==head],'surface_caveats':land.get('verdict_usage_caveats',[]),'limits':land.get('khong_do_duoc')}
 if stem=='pr823-wp802':
  r['recorded_cli_calls']=land['review']['so_loi_goi_codex_cli'];r['same_round_reviewer']=land['review']['luot_cuoi']['reviewer'];r['same_round_result']=land['review']['luot_cuoi']['ket_qua'];comment=json.loads((ROOT/'ops/land/pr823-wp802-provenance/readback-comment-6247520447.json').read_text());r['saved_comment_round_and_head_match']=all(x in comment['body'] for x in [head,'lượt 5/5','b3d8a108'])
 else:r['recorded_cli_header']=land['khong_do_duoc'][0]
 rows.append(r)
(OUT/'unresolved-land-surface.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
summary='unresolved_land_surface_disagreements=2\n'
for r in rows:
 summary+=r['verdict']+':'+str(r['self_line'])+'\nSELF: '+r['self_claim']+'\nhead='+r['head']+' hash='+r['hash']+' same_master='+str(r['same_master'])+' same_prev='+str(r['same_prev'])+'\n'
 if 'recorded_cli_calls' in r:summary+='LAND review.so_loi_goi_codex_cli='+str(r['recorded_cli_calls'])+'; luot_cuoi.reviewer='+r['same_round_reviewer']+'; ket_qua='+r['same_round_result']+'; saved_comment_round_and_head_match='+str(r['saved_comment_round_and_head_match'])+'\n'
 else:summary+='LAND khong_do_duoc.0='+r['recorded_cli_header']+'\n'
 summary+='matching_run_records='+str(len(r['matching_runtime_records']))+' surface_caveats='+repr(r['surface_caveats'])+'\n'
 summary+='LIMITS: '+repr(r['limits'])+'\n'
summary+='No actual execution surface selected: CLI references are secondary declarations without matching run.json/transcript. The measured defect is missing qualification of contradictory surface declarations, not proved runtime falsity.'
record(12,'Hai tự khai service còn trái hồ sơ land, nguồn runtime vắng','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/unresolved_land_surface.py; read exact verdict headers, YAML review/khong_do_duoc, saved same-round comment; index all run*.json',summary,'LỖI P2 surface-tu-khai-khac-ho-so-land-chua-co-caveat; không đủ nguồn để kết luận bề mặt thực chạy hoặc nâng thành P1')
