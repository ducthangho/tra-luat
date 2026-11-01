import os,sys,subprocess,json,re,hashlib,importlib.util
from datetime import datetime
from pathlib import Path
import yaml
S=Path(__file__).resolve().parent; R=S/'cay-kho'; N=S/'nguon/review1075a'; E=S/'evidence'
P='ops/reviews/pr1075-review-1-codex-verdict.receipt.yaml'; d=yaml.safe_load((R/P).read_text()); v=(N/'VERDICT.md').read_bytes(); txt=v.decode(); run=json.loads((N/'runs/71490d5a/run.json').read_text()); mi=d['model_reviewer_identity']; checks=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def g(*args): return git(*args).decode().strip()
def ck(label, actual, expected):
 checks.append({'check':label,'actual':actual,'expected':expected,'ok':actual==expected})
ck('verdict',d['verdict'],txt.splitlines()[0].split(': ',1)[1]); ck('reviewed_sha_verdict',d['reviewed_sha'],txt.splitlines()[1].split(': ',1)[1]); ck('hash',d['verdict_sha256'],sha(v)); ck('bytes',d['verdict_bytes'],len(v)); ck('flat_verdict',sha((R/d['verdict_path']).read_bytes()),sha(v))
counts=[len(re.findall(r'^- \[P'+str(i)+r'\]',txt,re.M)) for i in range(4)]
for i in range(4):
 ck('P'+str(i)+' findings',d['so_p'+str(i)],counts[i]); ck('P'+str(i)+' summary',f'0 P{i}' in txt.splitlines()[3],True)
ck('findings_ids',d['findings_ids'],[]); ck('count_basis',d['so_dem_theo'],'finding'); ck('reviewed_tree',d['reviewed_tree'],g('rev-parse',d['reviewed_sha']+'^{tree}')); ck('run head',d['reviewed_sha'],run['head'])
parents=g('show','-s','--format=%P',d['land_merge_commit']).split(); ck('merge parents count',len(parents),2); ck('merge second parent',parents[1],d['reviewed_sha']); ck('historical base',g('merge-base',parents[0],parents[1]),d['base_sha']); ck('historical diff',sha(git('diff',d['base_sha'],d['reviewed_sha'])),sha((N/'DIFF.patch').read_bytes()))
for name,commit in [('land',d['land_merge_commit']),('reviewed',d['reviewed_sha'])]:
 ck(name+' ancestor of origin/master',subprocess.run(['git','merge-base','--is-ancestor',commit,'origin/master'],cwd=R).returncode,0)
m=re.fullmatch(r'https://github.com/ducthangho/tra-luat/blob/([0-9a-f]{40})/(.+)',d['evidence_url']); ck('evidence URL grammar',bool(m),True); anchor,path=m.groups(); ck('evidence path',path,d['verdict_path']); ck('anchor ancestor of HEAD',subprocess.run(['git','merge-base','--is-ancestor',anchor,'HEAD'],cwd=R).returncode,0); ck('anchor hash',sha(git('show',anchor+':'+path)),d['verdict_sha256']); ck('anchor content commit',anchor,g('rev-parse','f0c4ed6')); ck('receipt commit parent',g('rev-parse','6af4c9a^'),anchor); ck('receipt commit content',sha(git('show','6af4c9a:'+P)),sha((R/P).read_bytes()))
ck('run copy',json.loads((R/mi['run_json']).read_text()),run); ck('launcher JSON equals run',json.loads((N/'launcher.json').read_text()),run)
for key,actual,expected in [('run_id',mi['session_run_id'],run['run_id']),('provider',mi['provider'],run['provider']),('surface',mi['surface'],run['execution_surface']),('transport',mi['transport'],run['transport']),('exit',run['ma_thoat'],0),('state',run['trang_thai'],'xong'),('duration',run['thoi_luong_giay'],412.567),('clean',run['worktree_sach'],True),('dirty count',run['so_muc_ban'],0),('sandbox state',run['sandbox_trang_thai'],'DO_DUOC'),('prompt',run['prompt_sha256'],sha((N/'PROMPT.md').read_bytes())),('model status',run['model_phuc_vu_trang_thai'],'DO_DUOC'),('effort status',run['effort_phuc_vu_trang_thai'],'DO_DUOC')]: ck(key,actual,expected)
duration=(datetime.fromisoformat(run['ket_thuc_utc'])-datetime.fromisoformat(run['bat_dau_utc'])).total_seconds(); ck('timestamp duration rounded',round(duration,3),run['thoi_luong_giay']); ck('model event count',len(run['model_phuc_vu']),19); ck('unique response IDs',len({x['response_id'] for x in run['model_phuc_vu']}),19); models=sorted({x['model'] for x in run['model_phuc_vu']}); ck('model',models,[mi['model']]); ck('model_da_chay',models,[mi['model_da_chay']]); ck('event types',sorted({x['su_kien'] for x in run['model_phuc_vu']}),['response.created']); ck('effort',run['effort_phuc_vu'],['xhigh']); ck('model evidence',mi['model_evidence'],'do_may'); ck('model ref',mi['model_evidence_ref'],mi['run_json']+'#model_phuc_vu')
for key in ['stdout','stderr']:
 b=(N/'runs/71490d5a'/f'{key}.log').read_bytes(); ck(key+' bytes',len(b),run[key+'_byte']); ck(key+' hash',sha(b),run[key+'_sha256'])
b=(N/'runs/71490d5a/checkpoint.json').read_bytes(); cp=json.loads(b); ck('checkpoint hash',sha(b),run['checkpoint_sha256']); ck('checkpoint id',cp['checkpoint_id'],run['run_id']); ck('checkpoint head',cp['head'],run['head']); ck('checkpoint prompt',cp['prompt_sha256'],run['prompt_sha256'])
sys.path.insert(0,str(R/'ops')); import lease_publish
paths=g('diff','--name-only',d['base_sha'],d['reviewed_sha']).splitlines(); cls=lease_publish._tinh_lop_tu_write_set(paths); ck('review class',d['review_class'],cls); ck('effective class',d['effective_review_class'],cls); ck('historical diff path count',len(paths),58); ck('historical paths outside reviews',[p for p in paths if not p.startswith('ops/reviews/')],[])
# ket_luan is a summary of the historical verdict, not the file counts of this PR.
for phrase in ['53 tep','2 tep','75 doi chieu','4 hang','dot bien bam']:
 ck('ket_luan token '+phrase,phrase in d['ket_luan'],True)
for phrase in ['53 tệp sao chép','hai tệp loại','75 đối chiếu','bốn hàng','Đột biến băm bị chặn đúng tên biên nhận']:
 ck('source verdict token '+phrase,phrase in txt.splitlines()[3],True)
a=json.loads((N/'evidence/archive.json').read_text()); rr=json.loads((N/'evidence/receipt.json').read_text()); rh=json.loads((N/'evidence/readme-history.json').read_text()); mut=json.loads((N/'evidence/mutation.json').read_text())
ck('historical report copied',a['copied_equal'],53); ck('historical report omitted',len(a['omitted']),2); ck('historical report receipt checks',rr['check_count'],75)
old=yaml.safe_load((R/'ops/reviews/pr1071-review-1-codex-verdict.receipt.yaml').read_text()); fixed=['schema_version','kind','packet_id','luot','role','provider','executor_provider','cross_provider','review_class','effective_review_class','assurance','verdict','nguon_tep','so_p0','so_p1','so_p2','so_p3','so_dem_theo','findings_ids','independent_from_executor_session','review_axes','nguon_co_tham_quyen']; differences={k:{'new':d[k],'old':old[k]} for k in fixed if d[k]!=old[k]}; ck('precedent fixed differences',differences,{})
ck('precedent caveat IDs and severity',[(x['id'],x['muc']) for x in d['verdict_usage_caveats']],[(x['id'],x['muc']) for x in old['verdict_usage_caveats']]); ck('precedent anchor type',d['anchor']['loai'],old['anchor']['loai']); ck('precedent anchor strength',d['anchor']['cuong_do'],old['anchor']['cuong_do']); ck('precedent keyset',sorted(d),sorted(old))
for key in ['provider','surface','transport','model_yeu_cau','model','model_da_chay','model_evidence']: ck('precedent model identity '+key,mi[key],old['model_reviewer_identity'][key])
errors=[c['check'] for c in checks if not c['ok']]
# Avoid bulky duplicate telemetry in the audit table; keep its equality result.
for c in checks:
 if isinstance(c['actual'],dict) and 'sandbox_quan_sat' in c['actual']:
  c['actual']='run.json decoded object'; c['expected']='source run.json decoded object'
r={'checks':len(checks),'errors':errors,'reviewed_sha':d['reviewed_sha'],'reviewed_tree':d['reviewed_tree'],'land_commit':d['land_merge_commit'],'land_parents':parents,'land_date':g('show','-s','--format=%cI',d['land_merge_commit']),'anchor':anchor,'anchor_blob_oid':g('rev-parse',anchor+':'+path),'counts':counts,'run_id':run['run_id'],'exit':run['ma_thoat'],'state':run['trang_thai'],'duration':run['thoi_luong_giay'],'timestamp_duration':duration,'events':len(run['model_phuc_vu']),'models':models,'effort':run['effort_phuc_vu'],'prompt_sha256':run['prompt_sha256'],'sandbox_state':run['sandbox_trang_thai'],'sandbox_limits':run['sandbox_gioi_han'],'class':cls,'historical_diff_paths':len(paths),'ket_luan':d['ket_luan'],'precedent_fixed_differences':differences}
(E/'receipt-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n'); (E/'receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(r,ensure_ascii=False,indent=2)); assert not errors
