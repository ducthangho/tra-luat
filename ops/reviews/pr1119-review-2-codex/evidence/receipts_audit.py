from common import *
import yaml,re,sys,datetime,collections
sys.path.insert(0,str(R/'ops'))
from lease_publish import _tinh_lop_tu_write_set
checks=[];summary=[]
def ck(field,actual,expected):checks.append(dict(receipt=stem,field=field,actual=actual,expected=expected,ok=actual==expected))
def oid(x):return git('rev-parse',x).decode().strip()
def ancestor(a,b):return subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=R).returncode
expected_shas=['e137f8c','3a3aac5','e101b11','51435a4']
for (pr,turn,src),short in zip(ITEMS,expected_shas):
    stem=f'pr{pr}-review-{turn}-codex'; d=yaml.safe_load((R/'ops/reviews'/f'{stem}-verdict.receipt.yaml').read_text())
    srcdir=S/'nguon'/src; verdict=(srcdir/'VERDICT.md').read_bytes(); text=verdict.decode(); lines=text.splitlines()
    m=d['model_reviewer_identity'];runfile=next((srcdir/'runs').glob('*/run.json')); run=json.loads(runfile.read_text()); checkpoint=json.loads(runfile.with_name('checkpoint.json').read_text())
    for f,a,b in [('target_pull_request',d['target_pull_request'],pr),('luot',d['luot'],turn),('verdict',d['verdict'],lines[0].split(': ',1)[1]),('reviewed_sha',d['reviewed_sha'],oid(short)),('verdict reviewed SHA',lines[1],'Reviewed commit: '+d['reviewed_sha']),('reviewed_tree',d['reviewed_tree'],oid(short+'^{tree}')),('verdict_path',d['verdict_path'],f'ops/reviews/{stem}-verdict.md'),('verdict_sha256',d['verdict_sha256'],digest(verdict)),('verdict_bytes',d['verdict_bytes'],len(verdict)),('receipt_id',d['receipt_id'],stem+'-'+digest(verdict)[:8]),('land_merge_commit',d['land_merge_commit'],oid('f4b513d' if pr==1110 else 'fb74c6e'))]:ck(f,a,b)
    for p in range(4):ck(f'so_p{p}',d[f'so_p{p}'],0)
    ck('findings_ids',d['findings_ids'],[]);ck('finding bullets',re.findall(r'^- \[P[0-3]\] .+',text,re.M),[])
    ck('zero-count positive text',bool(re.search(r'0 P0, 0 P1, 0 P2, 0 P3|Không có finding P0/P1/P2/P3|Không có \(0/0/0/0\)',text)),True)
    ck('so_dem_theo',d['so_dem_theo'],'finding')
    merge=d['land_merge_commit'];parents=git('show','-s','--format=%P',merge).decode().split()
    ck('merge parent count',len(parents),2);ck('merge parent2',parents[1],oid('3a3aac5' if pr==1110 else '51435a4'))
    ck('reviewed ancestor merge rc',ancestor(short,merge),0);ck('reviewed equals final head',d['reviewed_sha']==parents[1],turn==2)
    ck('merge ancestor origin/master rc',ancestor(merge,'origin/master'),0)
    ck('merge date',git('show','-s','--format=%cs',merge).decode().strip(),'2026-11-01')
    ck('merge message PR',f'#{pr}' in git('show','-s','--format=%s',merge).decode(),True)
    ck('base ancestor reviewed rc',ancestor(d['base_sha'],short),0)
    anchor,path=re.fullmatch(r'https://github.com/ducthangho/tra-luat/blob/([0-9a-f]{40})/(.+)',d['evidence_url']).groups()
    ck('evidence_url anchor',anchor,oid('cf5acfa'));ck('evidence_url path',path,d['verdict_path']);ck('anchor ancestor HEAD rc',ancestor(anchor,'HEAD'),0)
    blob=git('show',anchor+':'+path);ck('anchor blob hash',digest(blob),d['verdict_sha256']);ck('anchor blob equals source',blob==verdict,True)
    paths=git('diff','--name-only',d['base_sha'],short).decode().splitlines();cls=_tinh_lop_tu_write_set(paths)
    for key in ['review_class','effective_review_class']:ck(key,d[key],cls)
    ck('classifier same at reviewed SHA',git('rev-parse',short+':ops/lease_publish.py').strip(),git('rev-parse','HEAD:ops/lease_publish.py').strip())
    # Store OIDs as strings for JSON.
    checks[-1]['actual']=checks[-1]['actual'].decode();checks[-1]['expected']=checks[-1]['expected'].decode()
    ck('class path count note',int(re.search(r'tren (\d+) tep',d['review_class_ghi_chu'])[1]),len(paths))
    ck('class diff note',d['base_sha'][:7]+'..'+short in d['review_class_ghi_chu'],True)
    ck('class scope',all(p.startswith('ops/reviews/') for p in paths) if pr==1110 else paths==['ops/cloud_agent_creds_test.py'],True)
    for f,a,b in [('run path',m['run_json'],f'ops/reviews/{stem}/run/run.json'),('run_id',m['session_run_id'],run['run_id']),('run head',run['head'],d['reviewed_sha']),('prompt hash',run['prompt_sha256'],digest((srcdir/'PROMPT.md').read_bytes())),('launcher JSON',json.loads((srcdir/'launcher.json').read_text()),run),('checkpoint id',checkpoint['checkpoint_id'],run['run_id']),('checkpoint head',checkpoint['head'],run['head']),('checkpoint prompt',checkpoint['prompt_sha256'],run['prompt_sha256']),('checkpoint hash',run['checkpoint_sha256'],digest(runfile.with_name('checkpoint.json').read_bytes()))]:ck(f,a,b)
    for key,expected in [('ma_thoat',0),('trang_thai','xong'),('worktree_sach',True),('so_muc_ban',0),('model_phuc_vu_trang_thai','DO_DUOC'),('effort_phuc_vu_trang_thai','DO_DUOC'),('effort_phuc_vu',['xhigh'])]:ck('run '+key,run[key],expected)
    for f,k in [('provider','provider'),('surface','execution_surface'),('transport','transport')]:ck('identity '+f,m[f],run[k])
    duration=round((datetime.datetime.fromisoformat(run['ket_thuc_utc'])-datetime.datetime.fromisoformat(run['bat_dau_utc'])).total_seconds(),3)
    ck('duration timestamps',run['thoi_luong_giay'],duration)
    n=m['run_json_ghi_chu']
    for key in ['ma_thoat','trang_thai','thoi_luong_giay','sandbox_trang_thai','execution_surface']:ck('note '+key,re.search(r'\b'+key+r' ([\w.]+)',n)[1],str(run[key]))
    ck('note head',re.search(r'head (\w+)',n)[1],run['head'][:7]);ck('note clean','worktree_sach true' in n,run['worktree_sach'])
    ck('note prompt hash',run['prompt_sha256'].startswith(re.search(r'prompt_sha256 (\w+)',n)[1]),True)
    for k in ['model','model_yeu_cau','model_da_chay']:ck(k,sorted({e['model'] for e in run['model_phuc_vu']}),[m[k]])
    ck('model event count',int(re.search(r'(\d+) su kien',m['model_evidence_ghi_chu'])[1]),len(run['model_phuc_vu']))
    ck('model event kind',sorted({e['su_kien'] for e in run['model_phuc_vu']}),['response.created'])
    ck('model evidence reference',m['model_evidence_ref'],m['run_json']+'#model_phuc_vu')
    ck('model note',f'model {m["model"]}' in m['model_evidence_ghi_chu'],True)
    ck('effort note','effort_phuc_vu xhigh' in m['model_evidence_ghi_chu'],True)
    for stream in ['stdout','stderr']:
        raw=runfile.with_name(stream+'.log').read_bytes();ck(stream+' hash',run[stream+'_sha256'],digest(raw));ck(stream+' bytes',run[stream+'_byte'],len(raw))
    caveats={c['id']:c for c in d['verdict_usage_caveats']}
    ck('SANDBOX caveat','SANDBOX-KHONG-DO-DUOC' in caveats,run['sandbox_trang_thai']=='KHONG_DO_DUOC')
    ck('old-head caveat','KHONG-PHAI-HEAD-CUOI' in caveats,turn==1)
    ck('caveat unique count',len(caveats),len(d['verdict_usage_caveats']))
    if pr==1114:
        ck('DIFF present caveat','DIFF.patch CO trong kho.' in caveats['TEP-LON-KHONG-VAO-KHO']['mo_ta'],(R/'ops/reviews'/stem/'DIFF.patch').is_file())
    summary.append(dict(stem=stem,sha=d['reviewed_sha'],tree=d['reviewed_tree'],base=d['base_sha'],run_id=run['run_id'],duration=duration,events=len(run['model_phuc_vu']),sandbox=run['sandbox_trang_thai'],paths=len(paths),review_class=cls,merge_parent2=parents[1],ket_luan=d['ket_luan']))
failed=[c for c in checks if not c['ok']];save('receipt-checks.json',checks);save('receipts.json',dict(check_count=len(checks),failures=failed,summary=summary))
print(json.dumps(dict(check_count=len(checks),failures=failed,summary=summary),ensure_ascii=False,indent=2))
note('Biên nhận — `PYTHONDONTWRITEBYTECODE=1 python3 receipts_audit.py`: '+str(len(checks))+' đối chiếu, failures='+str(len(failed))+'. Expected/actual từng trường ở `evidence/receipt-checks.json`; git/telemetry tóm tắt `evidence/receipts.json`. Chỉ xác minh hiện vật, không xác thực phiên/nhà cung cấp phía máy chủ.')
