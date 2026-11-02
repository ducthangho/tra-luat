import hashlib,json,re,yaml
from audit import ROOT,OUT,MASTER,PREV,blob,record
cases=[('pr832-wp831','verdict-luot7/wp831-g1-luot7-codex-verdict.md',6,'verdict-luot7/run.json'),('pr848-wp744','verdicts/wp744-g3-luot1-codex-verdict.md',36,'verdicts/run-f65e544e.json'),('pr862-wp748-r21','verdicts/wp748-r21-luot1-codex-verdict.md',3,'verdicts/wp748-r21-luot1-codex-transcript.txt')]
rows=[]
for stem,vname,line,rname in cases:
 prefix='ops/land/'+stem+'-provenance/';vp=prefix+vname;rp=prefix+rname;data=(ROOT/vp).read_bytes();d=yaml.safe_load((ROOT/('ops/land/'+stem+'-land-evidence.yaml')).read_text())
 c=next(c for c in d['verdict_usage_caveats'] if c['verdict_path']==vp)
 r={'land':'ops/land/'+stem+'-land-evidence.yaml','verdict':vp,'self_claim_line':line,'self_claim':data.decode().splitlines()[line-1],'hash':hashlib.sha256(data).hexdigest(),'hash_matches_caveat':hashlib.sha256(data).hexdigest()==c['verdict_sha256'],'same_prev':data==blob(PREV,vp),'same_master':data==blob(MASTER,vp),'source':rp,'caveat':c}
 if rname.endswith('.json'):
  run=json.loads((ROOT/rp).read_text());r.update({'run_id':run['run_id'],'head':run['head'],'surface':run['execution_surface'],'transport':run['transport'],'program':run['lenh']['chuong_trinh'],'same_round_head':run['head'] in '\n'.join(data.decode().splitlines()[:20]),'caveat_source_head_run_match':all(v in c['mo_ta'] for v in [rp,run['run_id'],run['head']])})
 else:
  lines=(ROOT/rp).read_text().splitlines();r.update({'transcript_header':lines[:13],'land_luot1_reviewer':d['review']['luot_1']['reviewer'],'source_and_session_in_caveat':rp in c['mo_ta'] and '01a157da-2170-7be2-b6d0-053fa8f91aec' in c['mo_ta'],'cli_header':lines[0].startswith('OpenAI Codex v0.163.0')})
 rows.append(r)
(OUT/'land-round6.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
summary='corrected_land_verdicts=3\n'
for r in rows:
 summary+=r['verdict']+':'+str(r['self_claim_line'])+'\nSELF: '+r['self_claim']+'\nHASH: '+r['hash']+' hash_matches_caveat='+str(r['hash_matches_caveat'])+' same_prev='+str(r['same_prev'])+' same_master='+str(r['same_master'])+'\nSOURCE: '+r['source']+'\n'
 if 'run_id' in r:summary+='run='+r['run_id']+' head='+r['head']+' surface='+r['surface']+' transport='+r['transport']+' program='+r['program']+' same_round_head='+str(r['same_round_head'])+' caveat_source_head_run_match='+str(r['caveat_source_head_run_match'])+'\n'
 else:summary+='header='+repr(r['transcript_header'])+'\nluot1='+r['land_luot1_reviewer']+'\nsource_and_session_in_caveat='+str(r['source_and_session_in_caveat'])+'\n'
 summary+='CAVEAT: '+r['caveat']['mo_ta']+'\n'
record(11,'Đính chính surface của ba verdict provenance land','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/land_round6.py; sha256sum <verdict>; read same-round run JSON/transcript and land.review.luot_1',summary)
