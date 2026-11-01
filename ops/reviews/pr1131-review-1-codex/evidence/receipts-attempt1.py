from pathlib import Path
import sys,os,subprocess,json,hashlib,re,yaml,collections
from datetime import datetime
S=Path(__file__).resolve().parent;R=S/'work/head';E=S/'evidence'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL=str(S/'audit.gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0')
sys.path.insert(0,str(R/'ops'));import lease_publish
checks=[];summaries=[];commands=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
 p=subprocess.run(['git',*args],cwd=R,capture_output=True);commands.append({'cmd':['git',*args],'rc':p.returncode,'stdout_sha256':sha(p.stdout),'stdout_bytes':len(p.stdout),'stderr':p.stderr.decode()});return p

def check(name,actual,expected):checks.append(dict(name=name,actual=actual,expected=expected,ok=actual==expected))
def gs(*a):
 p=git(*a);assert p.returncode==0,p.stderr;return p.stdout.decode().strip()
def blob(rev,path):
 p=git('show',rev+':'+path);assert p.returncode==0,p.stderr;return p.stdout
B='180039c4b791fba4c89991623151cbb7378fce53';H='0e824fe4c1ac674081c93c6f2098e5433c932890'
for n,letter,events,seconds in [(1,'b',22,619.803),(2,'c',20,540.166)]:
 stem=f'pr1119-review-{n}-codex';p=R/'ops/reviews'/f'{stem}-verdict.receipt.yaml';d=yaml.safe_load(p.read_text());root=R/'ops/reviews'/stem;src=S/'nguon'/('review1119'+letter)
 raw=(root/'VERDICT.md').read_bytes();v=raw.decode();lines=v.splitlines();run=json.loads((root/'run/run.json').read_text());cp=json.loads((root/'run/checkpoint.json').read_text());ident=d['model_reviewer_identity']
 findings=[dict(id=m[2],hang='P'+m[1]) for m in re.finditer(r'^- \[P([0-3])\] ([^:]+):',v,re.M)]
 prefix=f'r{n}.'
 check(prefix+'verdict',d['verdict'],{'request_changes':'changes_requested','approve':'approve'}[lines[0].split(': ',1)[1]])
 check(prefix+'assurance',d['assurance'],'cross_reviewed' if findings else 'cross_approved')
 for i in range(4):check(prefix+f'so_p{i}',d[f'so_p{i}'],sum(f['hang']=='P'+str(i) for f in findings))
 check(prefix+'findings_ids',d['findings_ids'],findings)
 check(prefix+'verdict_hash',d['verdict_sha256'],sha(raw));check(prefix+'verdict_bytes',d['verdict_bytes'],len(raw));check(prefix+'flat_equal',(R/d['verdict_path']).read_bytes()==raw,True)
 check(prefix+'reviewed_sha',d['reviewed_sha'],lines[1].split(': ',1)[1]);check(prefix+'reviewed_tree',d['reviewed_tree'],gs('rev-parse',d['reviewed_sha']+'^{tree}'))
 check(prefix+'run_head',run['head'],d['reviewed_sha']);check(prefix+'land_merge_commit',d['land_merge_commit'],B)
 parents=gs('show','-s','--format=%P',B).split();check(prefix+'merge_parent_count',len(parents),2);check(prefix+'merge_parent_2',parents[1],'8715ac9f591b27d9b176e9d656437ef4b71b54dc')
 check(prefix+'ancestor_reviewed_merge',git('merge-base','--is-ancestor',d['reviewed_sha'],B).returncode,0)
 check(prefix+'merge_message_PR1119','Merge pull request #1119' in gs('show','-s','--format=%s',B),True)
 check(prefix+'base_ancestor',git('merge-base','--is-ancestor',d['base_sha'],d['reviewed_sha']).returncode,0)
 delta=git('diff',d['base_sha'],d['reviewed_sha']).stdout
 check(prefix+'DIFF_original_bytes',delta==(src/'DIFF.patch').read_bytes(),True)
 changes=gs('diff','--name-only',d['base_sha'],d['reviewed_sha']).splitlines();review_class=lease_publish._tinh_lop_tu_write_set(changes)
 check(prefix+'changes_count',len(changes),254);check(prefix+'only_reviews',all(x.startswith('ops/reviews/') for x in changes),True)
 check(prefix+'review_class',d['review_class'],review_class);check(prefix+'effective_review_class',d['effective_review_class'],review_class)
 m=re.fullmatch(r'https://github.com/ducthangho/tra-luat/blob/([0-9a-f]{40})/(.+)',d['evidence_url']);assert m
 anchor,path=m.groups();check(prefix+'anchor_commit',anchor,'9105a1a6f82915c0382edb2d3198c227c6d56d7b');check(prefix+'anchor_path',path,d['verdict_path']);check(prefix+'anchor_ancestor',git('merge-base','--is-ancestor',anchor,H).returncode,0);check(prefix+'anchor_hash',sha(blob(anchor,path)),d['verdict_sha256'])
 check(prefix+'session_run_id',ident['session_run_id'],run['run_id']);check(prefix+'run_path',d['model_reviewer_identity']['run_json'],str((root/'run/run.json').relative_to(R)))
 for key,expected in [('ma_thoat',0),('trang_thai','xong'),('thoi_luong_giay',seconds),('worktree_sach',True),('so_muc_ban',0),('sandbox_trang_thai','DO_DUOC'),('model_phuc_vu_trang_thai','DO_DUOC'),('effort_phuc_vu_trang_thai','DO_DUOC'),('effort_phuc_vu',['xhigh'])]:check(prefix+'run_'+key,run[key],expected)
 check(prefix+'duration_from_timestamps',round((datetime.fromisoformat(run['ket_thuc_utc'])-datetime.fromisoformat(run['bat_dau_utc'])).total_seconds(),3),run['thoi_luong_giay'])
 check(prefix+'prompt_sha256',sha((root/'PROMPT.md').read_bytes()),run['prompt_sha256']);check(prefix+'event_count',len(run['model_phuc_vu']),events)
 check(prefix+'all_event_models',sorted({x['model'] for x in run['model_phuc_vu']}),[ident['model']]);check(prefix+'event_types',sorted({x['su_kien'] for x in run['model_phuc_vu']}),['response.created'])
 check(prefix+'event_response_ids_unique',len({x['response_id'] for x in run['model_phuc_vu']}),events)
 for key in ('model_yeu_cau','model','model_da_chay'):check(prefix+key,ident[key],'gpt-6-astra')
 for key,runkey in [('provider','provider'),('surface','execution_surface'),('transport','transport')]:check(prefix+'identity_'+key,ident[key],run[runkey])
 check(prefix+'model_evidence',ident['model_evidence'],'do_may');check(prefix+'model_evidence_ref',ident['model_evidence_ref'],ident['run_json']+'#model_phuc_vu')
 check(prefix+'launcher_equals_run',json.loads((root/'launcher.out').read_text()),run)
 for key,expected in [('checkpoint_id',run['run_id']),('head',d['reviewed_sha']),('prompt_sha256',run['prompt_sha256'])]:check(prefix+'checkpoint_'+key,cp[key],expected)
 check(prefix+'checkpoint_hash',sha((root/'run/checkpoint.json').read_bytes()),run['checkpoint_sha256'])
 for stream in ('stdout','stderr'):
  b=(root/f'run/{stream}.log').read_bytes();check(prefix+stream+'_hash',sha(b),run[stream+'_sha256']);check(prefix+stream+'_bytes',len(b),run[stream+'_byte'])
 check(prefix+'cli_version_log','0.164.0' in (root/'run/stderr.log').read_text(),True)
 summaries.append(dict(round=n,reviewed_sha=d['reviewed_sha'],reviewed_tree=d['reviewed_tree'],base_sha=d['base_sha'],parents=parents,run_id=run['run_id'],ma_thoat=run['ma_thoat'],duration=run['thoi_luong_giay'],events=len(run['model_phuc_vu']),models=sorted({x['model'] for x in run['model_phuc_vu']}),effort=run['effort_phuc_vu'],prompt_sha256=run['prompt_sha256'],sandbox_trang_thai=run['sandbox_trang_thai'],diff_sha256=sha(delta),diff_bytes=len(delta),changed_count=len(changes),review_class=review_class,findings=findings))
# Reconstruct excluded diff for failed run and second-round supplemental diff.
r1=summaries[0];r2=summaries[1]
check('failed_DIFF_git_equal',git('diff',r1['base_sha'],r1['reviewed_sha']).stdout==(S/'nguon/review1119a/DIFF.patch').read_bytes(),True)
check('round2_ops_DIFF',git('diff',r1['reviewed_sha'],r2['reviewed_sha'],'--','ops/reviews/').stdout==(S/'nguon/review1119c/DIFF-OPS-REVIEWS-TU-LUOT1.patch').read_bytes(),True)
check('round2_previous_verdict',(S/'nguon/review1119c/nguon/VERDICT-LUOT1.md').read_bytes()==(S/'nguon/review1119b/VERDICT.md').read_bytes(),True)
# README multiset delta and exact caveat rows.
baselines=blob(B,'ops/reviews/README.md').decode().splitlines();headlines=(R/'ops/reviews/README.md').read_text().splitlines()
bc=collections.Counter(x for x in baselines if x.startswith('| '));hc=collections.Counter(x for x in headlines if x.startswith('| '));added=list((hc-bc).elements());removed=list((bc-hc).elements())
check('README.added',len(added),10);check('README.removed',removed,[])
expected=[]
for n in (1,2):
 d=yaml.safe_load((R/f'ops/reviews/pr1119-review-{n}-codex-verdict.receipt.yaml').read_text());stem=f'pr1119-review-{n}-codex';vpath=Path(d['verdict_path']).name
 for c in d['verdict_usage_caveats']:
  row=f"| `{vpath}` | `{c['id']}` | {c['mo_ta']} |";expected.append(row);check(f'README.r{n}.caveat.{c["id"]}',hc[row],1)
 rows=[x for x in added if x.startswith(f'| [`{vpath}`]')];check(f'README.r{n}.index_count',len(rows),1)
 if rows:
  row=rows[0];expected.append(row)
  for term in [d['verdict'],d['assurance'],str(d['luot']),'/'.join(str(d[f'so_p{i}']) for i in range(4)),d['reviewed_sha'][:7],str(d['verdict_bytes']),d['model_reviewer_identity']['session_run_id'][:8],'gpt-6-astra',stem+'-verdict.receipt.yaml']:
   check(f'README.r{n}.index_contains.{term}',term in row,True)
check('README.only_expected_added',collections.Counter(added)==collections.Counter(expected),True)
readme=dict(base_rows=sum(bc.values()),head_rows=sum(hc.values()),added=added,removed=removed)
# Check fixed structural precedent fields, plus changes-requested / approve mapping.
fixed=['schema_version','kind','packet_id','role','provider','executor_provider','cross_provider','review_class','effective_review_class','nguon_tep','so_dem_theo','independent_from_executor_session','review_axes','nguon_co_tham_quyen']
precedents=[]
for n in (1,2):
 d=yaml.safe_load((R/f'ops/reviews/pr1119-review-{n}-codex-verdict.receipt.yaml').read_text())
 for pr in (1058,1110,1114):
  old=yaml.safe_load((R/f'ops/reviews/pr{pr}-review-{n}-codex-verdict.receipt.yaml').read_text())
  for key in fixed:check(f'precedent.r{n}.pr{pr}.{key}',d[key],old[key])
  for key in ('provider','surface','transport','model','model_yeu_cau','model_da_chay','model_evidence'):check(f'precedent.r{n}.pr{pr}.identity.{key}',d['model_reviewer_identity'][key],old['model_reviewer_identity'][key])
  precedents.append(dict(round=n,pr=pr,old_verdict=old['verdict'],new_verdict=d['verdict'],old_assurance=old['assurance'],new_assurance=d['assurance']))
  if pr==1058:check(f'precedent.r{n}.assurance',d['assurance'],old['assurance'])
check('receipt1.assurance_not_approved',yaml.safe_load((R/'ops/reviews/pr1119-review-1-codex-verdict.receipt.yaml').read_text())['assurance_KHONG_dat'],'cross_approved')
# Run e9bd: log demonstrates incomplete review despite launcher rc0.
f=S/'nguon/review1119a';run=json.loads(next((f/'runs').glob('*/run.json')).read_text());stdout=next((f/'runs').glob('*/stdout.log')).read_text();v=(f/'VERDICT.md').read_text()
failed=dict(run_id=run['run_id'],head=run['head'],ma_thoat=run['ma_thoat'],trang_thai=run['trang_thai'],duration=run['thoi_luong_giay'],stdout=stdout,verdict=v,model_events=len(run['model_phuc_vu']))
check('failed.id',run['run_id'],'e9bd849279954310b67722bef764b7f4');check('failed.head',run['head'],r1['reviewed_sha']);check('failed.incomplete','Trạng thái tạm thời' in v,True);check('failed.disk_error','No space left on device' in stdout,True)
report=dict(check_count=len(checks),failures=[c for c in checks if not c['ok']],runs=summaries,readme=readme,precedents=precedents,failed_attempt=failed,commands=commands,checks=checks)
(E/'receipts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('checks',len(checks),'failures',json.dumps(report['failures'],ensure_ascii=False));print('runs',json.dumps(summaries,ensure_ascii=False));print('README',sum(bc.values()),'->',sum(hc.values()),'added',len(added),'removed',len(removed))
with (S/'VERDICT.md').open('a') as out:
 out.write(f'\nBiên nhận/README: `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py`: checks={len(checks)}, failures={report["failures"]}; README {sum(bc.values())} → {sum(hc.values())}, added={len(added)}, removed={len(removed)}. Lệnh git, expected/actual và giới hạn nguồn trong `evidence/receipts.json`.\n')
