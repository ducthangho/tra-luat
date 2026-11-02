import sys, pathlib, re, json, collections, subprocess
from audit import R,P,S,y,j,git,sha,dt,out
land=y(R/'ops/land/pr1047-wp1045-land-evidence.yaml')
HEAD=land['authorized_head_sha']; MERGE=land['merge_commit']
# Each expected value is read from the candidate claims, then compared to readback.
for entry in land['pre_merge_checks']+land['post_merge_checks']:
    rid=entry.get('run_id')
    if not rid or 'not_measured' in entry['conclusion']: continue
    run=j(P/f'readback-run-{rid}.json'); jobs=j(P/f'readback-jobs-{rid}.json')
    assert run['id']==rid and run['head_sha']==entry['sha'] and run['conclusion']==entry['conclusion']=='success'
    assert run['run_attempt']==entry['run_attempt']==1 and run['status']=='completed'
    assert len(jobs['jobs'])==jobs['total_count'] and len({v['id'] for v in jobs['jobs']})==jobs['total_count']
    assert all(v['run_id']==rid and v['run_attempt']==1 and v['head_sha']==entry['sha'] for v in jobs['jobs'])
    assert all(dt(v['completed_at'])<=dt(run['updated_at']) for v in jobs['jobs'])
    counts=collections.Counter(v['conclusion'] for v in jobs['jobs'])
    assert counts==({41099144196:{'success':23},41099486628:{'success':15,'skipped':1},41110458965:{'success':2},41145468254:{'success':23},41145468496:{'success':2}}[rid])
    for label in ('ubuntu-latest','windows-latest'):
        q=[v for v in jobs['jobs'] if label in v['labels']]
        if q: assert all(v['runner_id'] not in (None,0) for v in q)
    out('run_jobs',dict(id=rid,path=run['path'],event=run['event'],head_sha=run['head_sha'],run_attempt=run['run_attempt'],status=run['status'],conclusion=run['conclusion'],total=jobs['total_count'],counts=counts,labels=collections.Counter(','.join(v['labels']) or '(empty)' for v in jobs['jobs']),created_at=run['created_at'],updated_at=run['updated_at']))
    if rid in (41099144196,41145468254): assert all(v['labels']==['ubuntu-latest'] for v in jobs['jobs'])
    if rid in (41110458965,41145468496): assert {tuple(v['labels']) for v in jobs['jobs']}=={('ubuntu-latest',),('windows-latest',)}
    if rid==41099486628:
        for v in jobs['jobs']:
            if v['name']=='chuan-bi': assert v['labels']==['ubuntu-latest']
        gate=[v for v in jobs['jobs'] if v['name'].startswith('gate')]
        counterexamples=[{k:v[k] for k in ('id','name','conclusion','labels','runner_id')} for v in gate if 'windows-latest' not in v['labels']]
        out('CLAIM_moi_job_gate_windows_COUNTEREXAMPLES',counterexamples)
        assert len(counterexamples)==1 and counterexamples[0]['name']=='gate-cong-cu-gop'
        out('windows_executed_gate_jobs',len(gate)-len(counterexamples))
        for name in ['gate-cong-cu (windows-latest, 0)','gate-packet-loop (windows-latest)']:
            job=next(v for v in jobs['jobs'] if v['name']==name)
            steps=[s for s in job['steps'] if 'cài shellcheck' in s['name'] or s['name'].startswith('G5')]
            assert len(steps)==2 and all(s['status']=='completed' and s['conclusion']=='success' for s in steps)
            out('target_steps',dict(job=name,labels=job['labels'],steps=[{k:s[k] for k in ('name','conclusion','started_at','completed_at')} for s in steps]))
pr=j(P/'readback-pr-1047.json')
assert pr['merged'] is True and pr['merge_commit_sha']==MERGE and pr['head']['sha']==HEAD
assert pr['merged_by']['login']=='ducthangho' and pr['merged_at']=='2026-10-30T23:36:15Z'
assert pr['base']['sha'].startswith('5e458f4')
out('pr',dict(number=pr['number'],merged=pr['merged'],merged_at=pr['merged_at'],merged_by=pr['merged_by']['login'],head=pr['head']['sha'],base=pr['base']['sha'],merge=pr['merge_commit_sha']))
for rid in (41099144196,41099486628,41110458965):
    assert dt(j(P/f'readback-run-{rid}.json')['updated_at'])<dt(pr['merged_at'])
for suffix in ('','-sau'):
    d=j(P/f'readback-runs-b2d5f06{suffix}.json'); rs=d['workflow_runs']
    assert d['total_count']==len(rs)==2
    assert {r['id'] for r in rs}=={41145468254,41145468496}
    for r in rs:
        assert r['head_sha']==MERGE and r['event']=='push' and r['run_attempt']==1
        assert r['status']==('completed' if suffix else 'in_progress')
        assert r['conclusion']==('success' if suffix else None)
    out('push_snapshot'+suffix,[{k:r[k] for k in ('id','status','conclusion','updated_at')} for r in rs])
r=j(P/'readback-run-41147719416.json')
assert r['head_sha']==git('rev-parse','a430543').decode().strip() and r['status']=='completed' and r['conclusion']=='success'
out('lease_publish_run',{k:r[k] for k in ('id','head_sha','event','status','conclusion','created_at','updated_at')})
c=j(P/'readback-comment-6529094452.json'); c2=j(P/'readback-comment-6531582115.json')
assert c['user']['login']=='ducthangho' and c['performed_via_github_app']['slug']=='claude'
assert c['created_at']=='2026-10-30T17:29:22Z'
assert c2['user']['login']=='chatgpt-codex-connector[bot]' and c2['updated_at']=='2026-10-30T19:24:25Z'
state=json.loads(re.search(r'<!-- codex-review-state:v1 (.*?) -->',c2['body']).group(1))
assert state['code_review']==dict(commit_sha=HEAD,has_any_findings=False,has_unresolved_findings=False,status='completed')
assert 'Draft marked ready' in c2['body']
out('lease_comment',dict(id=c['id'],created_at=c['created_at'],user=c['user']['login'],app=c['performed_via_github_app']['slug'],body=c['body']))
out('connector',dict(id=c2['id'],updated_at=c2['updated_at'],user=c2['user']['login'],state=state))
text=(P/'ai-dang-giu-sau-rut-han/luc-do.txt').read_text()
assert '2026-10-31T00:23:19Z' in text and '713 ten' in text and 'thieu (co tren may chu, vang cuc bo): 0; thua: 0' in text
blocks=re.split(r'^\$ python3 ops/lease_publish.py ai-dang-giu ',text,flags=re.M)[1:]
assert len(blocks)==3
for block in blocks:
    path=block.splitlines()[0]
    assert path in land['lease']['write_set']
    assert 'HẾT_HẠN\twp1045-r1-g2-claude\t' in block
    assert 'CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ\twp1045-r1-g1-claude\t' in block
    assert 'NGƯỜI_GIỮ 0: không có' in block and block.strip().endswith('rc=0')
    out('ai_dang_giu_snapshot',dict(path=path,g1='CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ',g2='HẾT_HẠN',holders=0,rc=0))
assert land['trang_thai_packet']['landed'] is False and land['assurance_81']['reviewer_assurance_81']=='CHUA_DAT'
out('land_status',dict(landed=land['trang_thai_packet']['landed'],assurance_81=land['assurance_81']['reviewer_assurance_81'],authorization_text=land['authorization_ghi_chu'],landed_conditions=land['trang_thai_packet']['landed_dieu_kien']))
# Preserve every prior README line, as well as all specifically requested PR1050 rows.
def lines(ref): return git('show',ref+':ops/reviews/README.md').decode().splitlines()
base=lines('afc82f6'); merged=lines('33118e0'); head=lines('HEAD')
for a,b,label in [(base,merged,'base_to_merge'),(base,head,'base_to_head'),(lines('33118e0^1'),merged,'first_parent_to_merge')]:
    i=iter(b); preserved=all(any(x==v for x in i) for v in a)
    assert preserved,label
    rows=[v for v in a if v.startswith('|') and 'pr1050-' in v]
    assert all(v in b for v in rows)
    out('README_'+label,dict(all_prior_lines_subsequence=preserved,pr1050_rows=len(rows),pr1050_rows_identical=True))
for n in (1,2,3):
    receipt=y(R/f'ops/reviews/wp1045-g1-codex-luot{n}-verdict.receipt.yaml'); name=pathlib.Path(receipt['verdict_path']).name
    rows=[v for v in head if v.startswith('|') and name in v]
    index=[v for v in rows if '.receipt.yaml' in v]; caveat=[v for v in rows if '.receipt.yaml' not in v]
    assert len(index)==1 and len(caveat)==3
    row=index[0]
    for token in (receipt['lease_id'],receipt['verdict'],receipt['assurance'],receipt['reviewed_sha'][:7],str(receipt['verdict_bytes']),receipt['model_reviewer_identity']['session_run_id'][:8],'/'.join(str(receipt[f'so_p{k}']) for k in range(4))): assert token in row,token
    assert all(any(c['id'] in x for x in caveat) for c in receipt['verdict_usage_caveats'])
    out('README_wp1045',dict(luot=n,index_rows=1,caveat_rows=3,index_fields_match=True))
print('PROVENANCE+README COMPLETE; semantic counterexample above retained (not promoted to PASS).')
