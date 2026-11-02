from pathlib import Path
import datetime, hashlib, json, re, subprocess, sys, yaml
root=Path(__file__).resolve().parent.parent/'cay-kho'
sys.path.insert(0,str(root/'ops'))
import bien_nhan_v2 as gate
sha=lambda b:hashlib.sha256(b).hexdigest()
for n in (1,2):
    rp=root/f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml'
    r=yaml.safe_load(rp.read_text());p=root/f'ops/reviews/pr1050-review-{n}-codex'
    d=json.loads((p/'run/run.json').read_text());m=r['model_reviewer_identity']
    verdict=(p/'VERDICT.md').read_text()
    findings=re.findall(r'^### ([a-z0-9-]+)\s+\[P([0-3])\]',verdict,re.M)
    counts=[sum(int(sev)==i for _,sev in findings) for i in range(4)]
    print('ROUND',n,'TOP_LEVEL_FIELDS',len(r),'SCHEMA_GATE_ERRORS',gate._thieu(r))
    print('KIND',r['schema_version'],r['kind'],'PACKET',r['packet_id'],'TARGET_PR',r['target_pull_request'],'ROLE',r['role'],'ROUND',r['luot'])
    print('RECEIPT_ID_SUFFIX_MATCH',r['receipt_id'].endswith(sha((p/'VERDICT.md').read_bytes())[:8]))
    print('COUNTS_FROM_FINDING_HEADINGS',counts,'COUNTS_MATCH',counts==[r[f'so_p{i}'] for i in range(4)],'FINDING_IDS',findings,'IDS_MATCH',[x for x,_ in findings]==r['findings_ids'])
    print('VERDICT_MATCH',r['verdict']==verdict.splitlines()[0].split(': ',1)[1],'HEAD_MATCH',r['reviewed_sha']==verdict.splitlines()[1].split(': ',1)[1]==d['head'])
    print('HASH_MATCH',r['verdict_sha256']==sha((p/'VERDICT.md').read_bytes()),'BYTES_MATCH',r['verdict_bytes']==len((p/'VERDICT.md').read_bytes()))
    print('MODEL_IDENTITY_MATCH',{k:m[k]==d[other] for k,other in [('provider','provider'),('surface','execution_surface'),('transport','transport'),('session_run_id','run_id')]})
    print('MODEL',m['model'],m['model_da_chay'],'SERVED_MODELS',sorted({a['model'] for a in d['model_phuc_vu']}),'EVENTS',len(d['model_phuc_vu']),'EVIDENCE',m['model_evidence'],m['muc_bang_chung_model'])
    evpath,evkey=m['model_evidence_ref'].split('#')
    print('MODEL_EVIDENCE_REF_VALID',(root/evpath).is_file() and evkey in json.loads((root/evpath).read_text()))
    print('CANONICAL_FAMILIES_REVIEWER',gate._giai_ho_va_bc(r,'reviewer'),'EXECUTOR',gate._giai_ho_va_bc(r,'executor'),'ASSURANCE',r['assurance'])
    c=json.loads((p/'run/checkpoint.json').read_text())
    print('CHECKPOINT_FIELDS_MATCH',c['head']==d['head'] and c['prompt_sha256']==d['prompt_sha256'] and c['checkpoint_id']==d['run_id'],'CHECKPOINT_HASH_MATCH',sha((p/'run/checkpoint.json').read_bytes())==d['checkpoint_sha256'])
    elapsed=(datetime.datetime.fromisoformat(d['ket_thuc_utc'])-datetime.datetime.fromisoformat(d['bat_dau_utc'])).total_seconds()
    print('DURATION_DELTA_SECONDS',round(abs(elapsed-d['thoi_luong_giay']),6),'ACTUAL_RC',d['ma_thoat'],'STATUS',d['trang_thai'],'CLEAN_AT_LAUNCH',d['worktree_sach'])
    print('SANDBOX',d['sandbox_trang_thai'],'OBSERVED_PROFILES',sorted({json.dumps(x.get('permission_profile'),sort_keys=True) for x in d['sandbox_quan_sat']}))
    print('CLI_VERSION_FIELDS',[k for k in d if 'cli_version' in k or 'codex_version' in k],'RAW_ARGV_PRESENT',any(k in d for k in ['argv','command','args']))
    print('VERSION_IN_STDOUT_STDERR',any('0.164.0' in (p/f'run/{stream}.log').read_text() for stream in ['stdout','stderr']))
    print('AUTHORSHIP_SESSION_AND_HUMAN_ACTOR_NOT_IN_RUN_JSON',not any('session_01' in str(v) or 'ducthangho'==v for v in d.values()))
    print('USAGE_CAVEATS',[x['id'] for x in r['verdict_usage_caveats']])
    print('ANCHOR',r['anchor'],'INDEPENDENCE_DECLARED',r['independent_from_executor_session'],'AXES',r['review_axes'])
