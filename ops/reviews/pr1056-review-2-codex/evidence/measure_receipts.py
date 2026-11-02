from pathlib import Path
from datetime import datetime
from collections import Counter
import json,yaml,re,subprocess,importlib.util,sys
b=Path(__file__).resolve().parent.parent;r=b/'cay-kho'
def git(*a):return subprocess.check_output(['git','-C',str(r),*a],text=True).strip()
for n in (1,2):
 rec=yaml.safe_load((r/f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml').read_text());run=json.loads((r/rec['model_reviewer_identity']['run_json']).read_text());m=rec['model_reviewer_identity'];v=(r/rec['verdict_path']).read_text();heads=v.splitlines()[:3]
 print('ROUND',n,'KEY_COUNT',len(rec),'ALL_FIELDS',json.dumps(rec,ensure_ascii=False,sort_keys=True))
 expected={'schema_version':2,'receipt_id':f'pr1050-review-{n}-codex-'+rec['verdict_sha256'][:8],'kind':'review_delivery_receipt','packet_id':'KHONG_AP_DUNG','target_pull_request':1050,'luot':n,'role':'reviewer','provider':'codex','executor_provider':'claude','cross_provider':True,'review_class':'sensitive','effective_review_class':'sensitive','independent_from_executor_session':True,'review_axes':['spec','standards_security'],'so_dem_theo':'finding','nguon_tep':'ban_sao_nguyen_byte_cua_tep_goc_trong_kho'}
 print('STATIC_FIELDS',json.dumps({k:rec.get(k)==x for k,x in expected.items()},ensure_ascii=False))
 count=[int(x) for x in re.findall(r'(\d+) P[0-3]',heads[2])]
 # Findings have slug and severity on same heading; retain actual headings for human check.
 findings=[l for l in v.splitlines() if re.match(r'^### [a-z0-9]+(?:-[a-z0-9]+)+\s+.*\[P[0-3]\]',l)]
 print('VERDICT_MATCH',rec['verdict']==heads[0].split(': ',1)[1],'SHA_MATCH',rec['reviewed_sha']==heads[1].split(': ',1)[1]==run['head'],'COUNTS',count,'RECEIPT_COUNTS',[rec['so_p'+str(i)] for i in range(4)],'FINDING_HEADINGS',findings,'IDS',rec['findings_ids'])
 print('ASSURANCE',rec['assurance'],'MATCH',rec['assurance']==('cross_approved' if rec['verdict']=='approve' else 'cross_reviewed'))
 print('MRI_MATCH', {k:m[k]==run[j] for k,j in [('provider','provider'),('surface','execution_surface'),('transport','transport'),('session_run_id','run_id')]})
 print('MODEL_MATCH',set(x['model'] for x in run['model_phuc_vu'])=={m['model'],m['model_da_chay']},'EVIDENCE',m['model_evidence'],m['muc_bang_chung_model'],'REF_MATCH',m['model_evidence_ref']==m['run_json']+'#model_phuc_vu')
 print('CLI_ARGV_OR_VERSION_FIELDS',[k for k in run if 'cli_version' in k or 'argv' in k],'LENH',run['lenh'])
 duration=(datetime.fromisoformat(run['ket_thuc_utc'])-datetime.fromisoformat(run['bat_dau_utc'])).total_seconds();print('DURATION',duration,'DECLARED',run['thoi_luong_giay'],'ERROR',round(duration-run['thoi_luong_giay'],6))
 print('BASE_MERGE_BASE_PRE_MERGE',git('merge-base',rec['reviewed_sha'],'79400f3^1'),'DECLARED',rec['base_sha'])
 print('CURRENT_MASTER_MERGE_BASE',git('merge-base',rec['reviewed_sha'],'6db9341'),'HISTORICAL_HEAD_NOT_SAME_BASE_EXPECTED')
 for a,c in [('7333f97','047eaa4'),('7333f97','6db9341'),(rec['reviewed_sha'],'79400f3')]:
  p=subprocess.run(['git','-C',str(r),'merge-base','--is-ancestor',a,c]);print('ANCESTOR',a,c,'rc',p.returncode)
print('MERGE',git('show','-s','--format=%H%n%P%n%cI%n%s','79400f3'))
print('MASTER_FIRST_PARENT_TIMELINE',git('log','--first-parent','--format=%H %cI %s','-4','6db9341'))
print('OLD_BASE_SNAPSHOT',*[l for l in (r/'ops/reviews/pr1050-review-1-codex/evidence/final-integrity.log').read_text().splitlines() if 'origin/master' in l])
print('PATCH_1050',git('diff','--numstat','c24875d','f37b519'))
print('LEASE_WINDOWS_PATCH',git('diff','c24875d','f37b519','--','ops/land/pr1041-wp1037-land-evidence.yaml'))
