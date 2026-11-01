import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
import yaml

HERE=Path(__file__).resolve().parent
ROOT=HERE/'work/head'
SOURCE=HERE/'nguon/review1071a'
RECEIPT=ROOT/'ops/reviews/pr1071-review-1-codex-verdict.receipt.yaml'
ARCHIVE=ROOT/'ops/reviews/pr1071-review-1-codex'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
checks=[]
def eq(name,actual,expected):
    checks.append({'field':name,'actual':actual,'expected':expected,'ok':actual==expected})
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env=env)
def gittext(*args):return git(*args).decode().strip()
def ancestor(a,b):return subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=ROOT,env=env).returncode

d=yaml.safe_load(RECEIPT.read_text())
v=(SOURCE/'VERDICT.md').read_bytes(); vt=v.decode(); vl=vt.splitlines()
r=json.loads((ARCHIVE/'run/run.json').read_text())
identity=d['model_reviewer_identity']
eq('verdict',d['verdict'],vl[0].split(': ',1)[1])
eq('reviewed_sha',d['reviewed_sha'],vl[1].split(': ',1)[1])
eq('reviewed_tree',d['reviewed_tree'],gittext('rev-parse',d['reviewed_sha']+'^{tree}'))
eq('verdict_bytes',d['verdict_bytes'],len(v))
eq('verdict_sha256',d['verdict_sha256'],sha(v))
eq('flat_verdict_bytewise',(ROOT/d['verdict_path']).read_bytes()==v,True)
eq('archived_verdict_bytewise',(ARCHIVE/'VERDICT.md').read_bytes()==v,True)
findings=re.findall(r'^- \[(P[0-3])\]\s+([^:]+):',vt,re.M)
counts=[sum(severity==f'P{i}' for severity,slug in findings) for i in range(4)]
for i,n in enumerate(counts): eq(f'so_p{i}',d[f'so_p{i}'],n)
eq('findings_ids',d['findings_ids'],[])
eq('verdict_nguon_line4','approve — 0 P0, 0 P1, 0 P2, 0 P3' in vl[3],True)
eq('receipt_id',d['receipt_id'],'pr1071-review-1-codex-'+sha(v)[:8])
eq('run_id',identity['session_run_id'],r['run_id'])
eq('short_id',r['short_id'],r['run_id'][:8])
eq('run_head',r['head'],d['reviewed_sha'])
eq('run_json_path',(ROOT/identity['run_json']).read_bytes(),(ARCHIVE/'run/run.json').read_bytes())
# Avoid binary values in the JSON report; equality is the measurement here.
checks[-1]['actual']=sha(checks[-1]['actual']);checks[-1]['expected']=sha(checks[-1]['expected'])
for key,target in [('provider','provider'),('surface','execution_surface'),('transport','transport')]:
    eq('identity_'+key,identity[key],r[target])
eq('ma_thoat',r['ma_thoat'],0)
eq('trang_thai',r['trang_thai'],'xong')
eq('worktree_sach',r['worktree_sach'],True)
eq('so_muc_ban',r['so_muc_ban'],0)
duration=(datetime.datetime.fromisoformat(r['ket_thuc_utc'])-datetime.datetime.fromisoformat(r['bat_dau_utc'])).total_seconds()
eq('duration_round',r['thoi_luong_giay'],round(duration,3))
claimed_duration=float(re.search(r'thoi_luong_giay (\d+\.\d+)',identity['run_json_ghi_chu']).group(1))
eq('receipt_duration',claimed_duration,r['thoi_luong_giay'])
eq('prompt_sha256',r['prompt_sha256'],sha((SOURCE/'PROMPT.md').read_bytes()))
eq('prompt_prefix_in_receipt',r['prompt_sha256'][:12] in identity['run_json_ghi_chu'],True)
eq('launcher_json_equals_run_json',json.loads((SOURCE/'launcher.json').read_text()),r)
checks[-1]['actual']='equal' if checks[-1]['ok'] else 'different';checks[-1]['expected']='equal'
eq('model_status',r['model_phuc_vu_trang_thai'],'DO_DUOC')
models=sorted({x['model'] for x in r['model_phuc_vu']})
for key in ['model','model_da_chay']:eq(key,[identity[key]],models)
eq('event_count',len(r['model_phuc_vu']),int(re.search(r'(\d+) su kien',identity['model_evidence_ghi_chu']).group(1)))
eq('unique_event_count',len({x['response_id'] for x in r['model_phuc_vu']}),len(r['model_phuc_vu']))
eq('effort',r['effort_phuc_vu'],['xhigh'])
eq('effort_status',r['effort_phuc_vu_trang_thai'],'DO_DUOC')
eq('sandbox_status',r['sandbox_trang_thai'],'DO_DUOC')
eq('sandbox_status_in_receipt','sandbox_trang_thai '+r['sandbox_trang_thai'] in identity['run_json_ghi_chu'],True)
eq('model_evidence_ref',identity['model_evidence_ref'],identity['run_json']+'#model_phuc_vu')
for name in ['stdout','stderr']:
    data=(ARCHIVE/'run'/f'{name}.log').read_bytes()
    eq(name+'_byte',r[name+'_byte'],len(data));eq(name+'_sha256',r[name+'_sha256'],sha(data))
checkpoint_data=(ARCHIVE/'run/checkpoint.json').read_bytes()
checkpoint=json.loads(checkpoint_data)
eq('checkpoint_sha256',r['checkpoint_sha256'],sha(checkpoint_data))
eq('checkpoint_run_id',checkpoint['checkpoint_id'],r['run_id'])
eq('checkpoint_head',checkpoint['head'],r['head'])
eq('checkpoint_prompt',checkpoint['prompt_sha256'],r['prompt_sha256'])

parents=gittext('show','-s','--format=%P',d['land_merge_commit']).split()
eq('merge_parent_count',len(parents),2)
eq('merge_second_parent',parents[1],d['reviewed_sha'])
eq('land_ancestor_HEAD',ancestor(d['land_merge_commit'],'HEAD'),0)
eq('land_ancestor_origin_master',ancestor(d['land_merge_commit'],'origin/master'),0)
eq('review_base',gittext('merge-base',d['reviewed_sha'],parents[0]),d['base_sha'])
url_match=re.fullmatch(r'https://github.com/ducthangho/tra-luat/blob/([a-f0-9]{40})/(.+)',d['evidence_url'])
eq('evidence_url_shape',bool(url_match),True)
anchor,path=url_match.groups()
blob=git('show',anchor+':'+path)
eq('evidence_path',path,d['verdict_path'])
eq('anchor_ancestor_HEAD',ancestor(anchor,'HEAD'),0)
eq('anchor_sha256',sha(blob),d['verdict_sha256'])
eq('anchor_verdict_bytes',blob==v,True)
eq('anchor_ancestor_receipt_commit',ancestor(anchor,'16f9658'),0)
eq('artifact_anchor',anchor,gittext('rev-parse','629543d'))
paths=gittext('diff','--name-only',d['base_sha'],d['reviewed_sha']).splitlines()
sys.path.insert(0,str(ROOT/'ops'))
spec=importlib.util.spec_from_file_location('measured_lease',ROOT/'ops/lease_publish.py')
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
review_class=module._tinh_lop_tu_write_set(paths)
eq('review_class',d['review_class'],review_class)
eq('effective_review_class',d['effective_review_class'],review_class)
eq('classified_file_count',len(paths),int(re.search(r'tren (\d+) tep',d['review_class_ghi_chu']).group(1)))
eq('classified_paths_within_reviews',all(x.startswith('ops/reviews/') for x in paths),True)
eq('historical_patch_bytewise',git('diff',d['base_sha'],d['reviewed_sha'])==(SOURCE/'DIFF.patch').read_bytes(),True)
eq('archived_data_unchanged_after_receipt',gittext('diff','--name-only','16f9658','HEAD','--','ops/reviews/pr1071-review-1-codex','ops/reviews/pr1071-review-1-codex-verdict.md','ops/reviews/pr1071-review-1-codex-verdict.receipt.yaml'),'')

# These are consistency checks against the preserved original verdict/logs, not a re-run of review #1071.
old_bytes=json.loads((SOURCE/'evidence/bytes.json').read_text())
old_receipts=json.loads((SOURCE/'evidence/receipts-checks.json').read_text())
old_readme=json.loads((SOURCE/'evidence/readme.json').read_text())
old_mutations=json.loads((SOURCE/'evidence/mutations.json').read_text())
summary={'copied':sum(x['mapped_files'] for x in old_bytes['rounds']),
         'omitted':sum(len(x['omissions']) for x in old_bytes['rounds']),
         'receipt_checks':len(old_receipts),'readme_rows':old_readme['index_rows']+old_readme['caveat_rows'],
         'mutations':len(old_mutations)}
for key,pattern in [('copied',r'(\d+) tep chep'),('omitted',r'(\d+) tep loai'),
                    ('receipt_checks',r'(\d+) doi chieu'),('readme_rows',r'(\d+) hang README')]:
    eq('ket_luan_'+key,int(re.search(pattern,d['ket_luan']).group(1)),summary[key])
eq('ket_luan_two_mutations','hai dot bien' in d['ket_luan'] and summary['mutations']==2,True)
eq('ket_luan_matches_verdict_summary',all(x in vl[3] for x in ['64 tệp','3 tệp','116 đối chiếu','9 hàng README','Hai đột biến băm']),True)

fixed=['schema_version','kind','packet_id','role','provider','executor_provider','cross_provider',
       'review_class','effective_review_class','assurance','verdict','so_p0','so_p1','so_p2','so_p3',
       'so_dem_theo','findings_ids','nguon_tep','independent_from_executor_session','review_axes','nguon_co_tham_quyen']
precedents=[]
for predecessor in ['pr1058-review-1-codex-verdict.receipt.yaml','pr1058-review-2-codex-verdict.receipt.yaml','pr1050-review-2-codex-verdict.receipt.yaml']:
    old=yaml.safe_load((ROOT/'ops/reviews'/predecessor).read_text())
    diff={key:{'new':d.get(key),'old':old.get(key)} for key in fixed if d.get(key)!=old.get(key)}
    precedents.append({'receipt':predecessor,'fixed_field_differences':diff,
                       'old_caveats':[x['id'] for x in old['verdict_usage_caveats']],
                       'new_caveats':[x['id'] for x in d['verdict_usage_caveats']],
                       'anchor_type_equal':d['anchor']['loai']==old['anchor']['loai'],
                       'anchor_strength_equal':d['anchor']['cuong_do']==old['anchor']['cuong_do']})
eq('approve_precedent_1058_fixed_fields',precedents[1]['fixed_field_differences'],{})
eq('approve_precedent_1050_fixed_fields',precedents[2]['fixed_field_differences'],{})
eq('approve_precedent_1058_caveats',precedents[1]['new_caveats'],precedents[1]['old_caveats'])

unmeasured={
 'github':'KHÔNG ĐO ĐƯỢC: current PR/CI state, public serving of evidence_url, actor, actual request merge_method/expectedHeadSha. Local two-parent graph is measured; API request arguments are not recorded in the supplied original run.',
 'cli':'KHÔNG ĐO ĐƯỢC: historical codex-cli version, complete launcher argv, requested model/effort. run.json stores lenh.chuong_trinh/so_doi_so/van_tay, not full argv or binary version.',
 'identity':'KHÔNG ĐO ĐƯỢC: executor identity/family, owner instruction, independent context beyond preserved prompt/run/checkpoint. No re-certification of cross_approved from this archival consistency check.',
 'sandbox':'KHÔNG ĐO ĐƯỢC: enforcement for every command of the historical run; sandbox_gioi_han explicitly limits DO_DUOC to sampled observation.',
 'omitted_copies':'KHÔNG ĐO ĐƯỢC: contents of omitted cay-kho/, base-copy/, mutation-copy/, nguon/; directories are absent from supplied source.'}
output={'check_count':len(checks),'errors':[x['field'] for x in checks if not x['ok']],
        'reviewed_sha':d['reviewed_sha'],'reviewed_tree':d['reviewed_tree'],'land_merge_commit':d['land_merge_commit'],
        'land_parents':parents,'land_commit_date':gittext('show','-s','--format=%cI',d['land_merge_commit']),
        'anchor':anchor,'verdict_sha256':sha(v),'verdict_bytes':len(v),'counts':counts,
        'run_id':r['run_id'],'ma_thoat':r['ma_thoat'],'duration':r['thoi_luong_giay'],'duration_from_timestamps':duration,
        'event_count':len(r['model_phuc_vu']),'models':models,'effort':r['effort_phuc_vu'],
        'prompt_sha256':r['prompt_sha256'],'sandbox_status':r['sandbox_trang_thai'],'sandbox_limits':r['sandbox_gioi_han'],
        'class':review_class,'changed_count':len(paths),'ket_luan_source_log_counts':summary,
        'precedents':precedents,'unmeasured':unmeasured}
(HERE/'evidence/receipt-checks.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
(HERE/'evidence/receipt.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ['precedents','unmeasured','sandbox_limits']},ensure_ascii=False))
raise SystemExit(bool(output['errors']))
