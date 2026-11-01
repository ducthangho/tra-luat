from audit_common import *
import re, yaml, importlib.util, sys
from datetime import datetime
sys.path.insert(0,str(REPO/'ops'))
import lease_publish

allrows=[]
summaries=[]
for pr,round_,source in CASES:
    stem=f'pr{pr}-review-{round_}-codex'
    receipt=REPO/'ops/reviews'/(stem+'-verdict.receipt.yaml')
    d=yaml.safe_load(receipt.read_text())
    arc=REPO/'ops/reviews'/stem
    runj=json.loads((arc/'run/run.json').read_text())
    launcher=json.loads((arc/'launcher.out').read_text())
    cp=json.loads((arc/'run/checkpoint.json').read_text())
    verdict=(arc/'VERDICT.md').read_text()
    rows=[]
    def check(label,actual,expected):
        rows.append({'field':label,'actual':actual,'expected':expected,'ok':actual==expected})
    check('target_pull_request',d['target_pull_request'],int(pr))
    check('luot',d['luot'],round_)
    check('schema_version',d['schema_version'],2)
    check('kind',d['kind'],'review_delivery_receipt')
    check('verdict',d['verdict'],re.search(r'^Verdict: (.*)$',verdict,re.M)[1])
    for n in range(4): check('so_p'+str(n),d['so_p'+str(n)],len(re.findall(r'^- \[P'+str(n)+r'\]',verdict,re.M)))
    check('findings_ids',d['findings_ids'],[])
    check('so_dem_theo',d['so_dem_theo'],'finding')
    check('verdict_path',d['verdict_path'],f'ops/reviews/{stem}-verdict.md')
    check('verdict_sha256',d['verdict_sha256'],sha((arc/'VERDICT.md').read_bytes()))
    check('verdict_bytes',d['verdict_bytes'],(arc/'VERDICT.md').stat().st_size)
    check('reviewed_sha.verdict',d['reviewed_sha'],re.search(r'^Reviewed commit: (\w+)',verdict,re.M)[1])
    check('reviewed_sha.run',d['reviewed_sha'],runj['head'])
    check('reviewed_sha.table',d['reviewed_sha'],git('rev-parse',{('1110',1):'e137f8c',('1110',2):'3a3aac5',('1114',1):'e101b11',('1114',2):'51435a4'}[(pr,round_)]).decode().strip())
    check('reviewed_tree',d['reviewed_tree'],git('rev-parse',d['reviewed_sha']+'^{tree}').decode().strip())
    merge=d['land_merge_commit']
    check('land_merge_commit',merge,git('rev-parse','f4b513d' if pr=='1110' else 'fb74c6e').decode().strip())
    parents=git('show','-s','--format=%P',merge).decode().split()
    check('merge_parent_count',len(parents),2)
    check('merge_second_parent',parents[1],git('rev-parse','3a3aac5' if pr=='1110' else '51435a4').decode().strip())
    check('reviewed_is_ancestor_merge',run(['git','merge-base','--is-ancestor',d['reviewed_sha'],merge]).returncode,0)
    check('reviewed_equals_merge_second_parent',d['reviewed_sha']==parents[1],round_==2)
    check('merge_is_ancestor_master',run(['git','merge-base','--is-ancestor',merge,'origin/master']).returncode,0)
    check('merge_date',git('show','-s','--format=%cs',merge).decode().strip(),'2026-11-01')
    check('merge_PR_message',f'#{pr}' in git('show','-s','--format=%s',merge).decode(),True)
    check('base_is_ancestor_reviewed',run(['git','merge-base','--is-ancestor',d['base_sha'],d['reviewed_sha']]).returncode,0)
    check('base_is_ancestor_merge_first_parent',run(['git','merge-base','--is-ancestor',d['base_sha'],parents[0]]).returncode,0)
    check('base_in_source_prompt',d['base_sha'][:7] in (arc/'PROMPT.md').read_text(),True)
    changed=git('diff','--name-only',d['base_sha'],d['reviewed_sha']).decode().splitlines()
    check('review_class',d['review_class'],lease_publish._tinh_lop_tu_write_set(changed))
    check('effective_review_class',d['effective_review_class'],lease_publish._tinh_lop_tu_write_set(changed))
    check('review_class_file_count',int(re.search(r'tren (\d+) tep',d['review_class_ghi_chu'])[1]),len(changed))
    anchor=re.fullmatch(r'https://github.com/ducthangho/tra-luat/blob/([a-f0-9]{40})/(.+)',d['evidence_url'])
    check('evidence_url_format',anchor is not None,True)
    check('evidence_url_commit',anchor[1],git('rev-parse','cf5acfa').decode().strip())
    check('evidence_url_path',anchor[2],d['verdict_path'])
    check('anchor_is_ancestor_HEAD',run(['git','merge-base','--is-ancestor',anchor[1],HEAD]).returncode,0)
    check('anchor_blob_hash',sha(git('show',anchor[1]+':'+anchor[2])),d['verdict_sha256'])
    check('anchor_blob_equal',git('show',anchor[1]+':'+anchor[2]),(arc/'VERDICT.md').read_bytes())
    # Keep byte comparisons serializable without dumping verdict text.
    for row in rows:
        for k in ('actual','expected'):
            if isinstance(row[k],bytes): row[k]={'bytes':len(row[k]),'sha256':sha(row[k])}
    check('anchor.loai',d['anchor']['loai'],'canonical_ancestry')
    check('anchor.cuong_do',d['anchor']['cuong_do'],'thap')
    model=d['model_reviewer_identity']
    check('run_json',model['run_json'],f'ops/reviews/{stem}/run/run.json')
    check('session_run_id',model['session_run_id'],runj['run_id'])
    for k in ('run_id','ma_thoat','head','prompt_sha256','trang_thai','thoi_luong_giay'):
        check('launcher.'+k,launcher.get(k),runj[k])
    for k in ('provider','transport'): check('identity.'+k,model[k],runj[k])
    check('identity.surface',model['surface'],runj['execution_surface'])
    check('identity.model_yeu_cau',model['model_yeu_cau'],'gpt-6-astra')
    check('identity.model_evidence',model['model_evidence'],'do_may')
    check('identity.model_evidence_ref',model['model_evidence_ref'],model['run_json']+'#model_phuc_vu')
    for k in ('model','model_da_chay'): check('identity.'+k,sorted({x['model'] for x in runj['model_phuc_vu']}),[model[k]])
    check('model_phuc_vu_trang_thai',runj['model_phuc_vu_trang_thai'],'DO_DUOC')
    check('model_event_count',int(re.search(r'(\d+) su kien',model['model_evidence_ghi_chu'])[1]),len(runj['model_phuc_vu']))
    check('model_unique_response_ids',len({x['response_id'] for x in runj['model_phuc_vu']}),len(runj['model_phuc_vu']))
    check('model_event_kind',sorted({x['su_kien'] for x in runj['model_phuc_vu']}),['response.created'])
    check('effort_phuc_vu',runj['effort_phuc_vu'],['xhigh'])
    check('effort_phuc_vu_trang_thai',runj['effort_phuc_vu_trang_thai'],'DO_DUOC')
    note=model['run_json_ghi_chu']
    check('note.ma_thoat',int(re.search(r'ma_thoat (\d+)',note)[1]),runj['ma_thoat'])
    check('note.thoi_luong_giay',float(re.search(r'thoi_luong_giay ([\d.]+)',note)[1]),runj['thoi_luong_giay'])
    check('note.trang_thai',re.search(r'trang_thai (\w+)',note)[1],runj['trang_thai'])
    check('note.head',re.search(r'head (\w+)',note)[1],runj['head'][:7])
    check('note.worktree_sach','worktree_sach true' in note,runj['worktree_sach'])
    check('note.execution_surface',re.search(r'execution_surface (\w+)',note)[1],runj['execution_surface'])
    check('note.sandbox_trang_thai',re.search(r'sandbox_trang_thai (\w+)',note)[1],runj['sandbox_trang_thai'])
    prefix=re.search(r'prompt_sha256 (\w+)',note)[1]
    check('note.prompt_sha256',prefix,runj['prompt_sha256'][:len(prefix)])
    check('run.prompt_sha256',runj['prompt_sha256'],sha((arc/'PROMPT.md').read_bytes()))
    check('run.duration_timestamps',round((datetime.fromisoformat(runj['ket_thuc_utc'])-datetime.fromisoformat(runj['bat_dau_utc'])).total_seconds(),3),runj['thoi_luong_giay'])
    for kind in ('stdout','stderr'):
        b=(arc/'run'/(kind+'.log')).read_bytes()
        check('run.'+kind+'_byte',runj[kind+'_byte'],len(b))
        check('run.'+kind+'_sha256',runj[kind+'_sha256'],sha(b))
    check('run.checkpoint_sha256',runj['checkpoint_sha256'],sha((arc/'run/checkpoint.json').read_bytes()))
    ids=[x['id'] for x in d['verdict_usage_caveats']]
    check('SANDBOX-KHONG-DO-DUOC', 'SANDBOX-KHONG-DO-DUOC' in ids,runj['sandbox_trang_thai']=='KHONG_DO_DUOC')
    check('KHONG-PHAI-HEAD-CUOI','KHONG-PHAI-HEAD-CUOI' in ids,round_==1)
    check('WINDOWS-THAT-KHONG-DO-TRONG-SANDBOX','WINDOWS-THAT-KHONG-DO-TRONG-SANDBOX' in ids,pr=='1114')
    check('caveat_ids_unique',len(ids),len(set(ids)))
    check('caveat_muc',sorted({x['muc'] for x in d['verdict_usage_caveats']}),['P3'])
    r={'receipt':receipt.name,'checks':len(rows),'failures':[x for x in rows if not x['ok']],
       'changed_paths':changed,'reviewed_sha':d['reviewed_sha'],'reviewed_tree':d['reviewed_tree'],
       'merge_parents':parents,'run_id':runj['run_id'],'duration':runj['thoi_luong_giay'],
       'model_events':len(runj['model_phuc_vu']),'sandbox':runj['sandbox_trang_thai'],'caveats':ids,
       'ket_luan':d['ket_luan'],'checkpoint_keys':sorted(cp.keys()),'launcher_keys':sorted(launcher.keys())}
    allrows.append({'receipt':receipt.name,'checks':rows})
    summaries.append(r)
    print(json.dumps(r,ensure_ascii=False))
save('receipts.json',summaries)
save('receipt-checks.json',allrows)
append('Biên nhận — `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py`: '+str(sum(x['checks'] for x in summaries))+' đối chiếu, '+str(sum(len(x['failures']) for x in summaries))+' lệch. Từng trường/lệnh git nằm ở script; expected/actual ở `evidence/receipt-checks.json`, tóm tắt `evidence/receipts.json`. Giới hạn: đối chiếu run.json là đối chiếu hiện vật, không tự xác thực nhà cung cấp/phiên máy chủ.')
