import ast
import datetime as dt
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import yaml

BASE = pathlib.Path(__file__).resolve().parents[1]
ROOT = BASE / 'cay-kho'
OUT = BASE / 'do-review7'
PKG = ROOT / 'ops/reviews/pr468-hoso-4-packet-review-6-codex'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PKG))
scaffold = {'tai-lieu': BASE/'tai-lieu', 'cay-kho': ROOT, 'do-review': OUT/'replay'}
for name, dest in scaffold.items():
    (PKG.parent/name).symlink_to(dest, target_is_directory=True)
try:
    import harness as h
finally:
    for name in scaffold:
        (PKG.parent/name).unlink()
h.ROOT = ROOT
h.C.ROOT = ROOT

def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git', '-C', str(ROOT), *args])
report = {'utc': dt.datetime.now(dt.timezone.utc).isoformat()}
report['leases'] = []
for p in sorted((BASE / 'tai-lieu').glob('*exec-1-claude*.yaml*')):
    d = yaml.safe_load(p.read_text())
    sp = ROOT / d['spec_path']
    issue = next((ROOT / 'ops/issues').glob(str(d['packet_issue'])+'-*.md'))
    text = issue.read_text()
    frozen = re.search(r'@ `([0-9a-f]{40})`', text).group(1)
    frozen_hash = sha(git('show', frozen+':'+d['spec_path']))
    report['leases'].append(dict(file=p.name, spec_hash=sha(sp.read_bytes()),
        declared=d['spec_sha256'], hash_matches=sha(sp.read_bytes())==d['spec_sha256']==d['spec_hash'],
        issue_hash_matches=d['spec_sha256'] in text, issue_commit=frozen,
        issue_commit_hash=frozen_hash, issue_commit_hash_matches=frozen_hash==d['spec_sha256'],
        copies_match=sp.read_bytes()==(BASE/'tai-lieu'/sp.name).read_bytes() and p.read_bytes()==(ROOT/'ops/leases'/p.name).read_bytes(),
        write_set=d['write_set'], write_set_exists=[(ROOT / v).exists() for v in d['write_set']],
        dependency=d['depends_on'], null_keys=[k for k,v in d.items() if v is None],
        missing_protocol4=[k for k in ['packet_id','executor','environment','branch','write_set_hash','generation','heartbeat_at','lease_until'] if k not in d],
        missing_protocol32=[k for k in ['schema_version','packet_id','mission_issue','revision','spec_hash','objective','write_set','depends_on','executor','environment','risk','review_class','acceptance_criteria'] if k not in d]))
    if d['packet_issue']==463:
        payload='\n'.join(sorted(d['write_set']))+'\n'
        report['gate'] = dict(write_set_hash_declared=d['write_set_hash'], write_set_hash_actual=sha(payload.encode()),
            payload=payload, anchors={k:d[k] for k in ['base_sha','start_from_sha','reviewed_sha_required']},
            leased=d['leased_at_utc'], heartbeat=d['heartbeat_at'], until=d['lease_until'], expires=d['lease_expires_at_utc'],
            lease_minutes=(dt.datetime.fromisoformat(d['lease_until'])-dt.datetime.fromisoformat(d['leased_at_utc'])).total_seconds()/60,
            log=git('log','--first-parent','-n','8','--format=%H %cI %s',d['base_sha']).decode(),
            drift=git('diff','--numstat','1b3caa1',d['base_sha'],'--',*d['write_set']).decode())
report['issue_anchor_fix'] = {rev:sha(git('show',rev+':ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md')) for rev in ['b743f179','8c3e371','HEAD']}
report['consumer_copy_matches'] = (BASE/'tai-lieu/ci_dang_ky_test.py').read_bytes()==(ROOT/'.claude/dev/ci_dang_ky_test.py').read_bytes()
report['H_blocks'] = {name:dict(package=sha((PKG/name).read_bytes()), extracted=sha((OUT/'replay'/name).read_bytes())) for name in ['h_tong.py','h_predicate.py']}
report['replay_files_equal'] = {name:(PKG/name).read_bytes()==(OUT/'replay'/name).read_bytes() for name in ['attack-h-cases.json','attack-h-summary.json']}
report['MOI'] = dict(count=len(h.C.MOI), span_preserved=sum(h.C.MOI[p][0]==s for p,s in h.BASE_MOI.items()), type_changed=sum(type(h.C.MOI[p])!=type(s) for p,s in h.BASE_MOI.items()), windows_forms=sum(map(len,h.C.MOI_WINDOWS.values())))
def run(path,text,base=False):
    try: return h.replay(path,text,base=base)
    except Exception as e: return type(e).__name__
pre='.claude/hooks/pretooluse_guard_test.py'; mcp='.claude/dev/mcp_gh_test.py'
long='9'*5000
fixtures={
 'pre-ca':(pre, f'TONG: CA {long}/{long} dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n'),
 'pre-mutant':(pre, f'TONG: CA 39/39 dat · DOT BIEN {long}/{long} bi giet\nTONG: DAT\n'),
 'nhanh':('ops/nhanh_don_duoc_test.py', long+'/'+long+'\n'),
 'mcp-mutant':(mcp, f'CA         : 42/42 đạt · 0 đỏ · ĐẠT\nĐỘT BIẾN   : đã đo {long}/{long} tập giết · ĐẠT\nTỔNG: ĐẠT\n')}
report['d9'] = {name:dict(path=p, text=t, BASE=run(p,t,True), H=run(p,t)) for name,(p,t) in fixtures.items()}
report['issue464_examples'] = []
for ca,db in [('39/39','34/34'),('39/39','0/0'),('0/39','34/34')]:
    t=f'TONG: CA {ca} dat · DOT BIEN {db} bi giet\nTONG: DAT\n'
    report['issue464_examples'].append(dict(text=t,BASE=run(pre,t,True),H=run(pre,t)))
report['stored_outputs'] = []
for source in [*sorted((PKG/'outputs').glob('*.stdout')),*sorted((PKG/'outputs-that').glob('*.stdout'))]:
    name=source.name.split('.')[0]+'.py'
    p=next((k for k in h.C.MOI if pathlib.Path(k).name==name),None)
    if p is None: continue
    t=source.read_text()
    report['stored_outputs'].append(dict(file=str(source.relative_to(PKG)),bytes=len(source.read_bytes()),sha256=sha(source.read_bytes()),BASE_with_rc0=run(p,t,True),H_with_rc0=run(p,t)))
L=h.module(ROOT/'ops/lease_publish.py','lease_review7')
leases=L._quet_lease_toan_kho(ROOT,doi_chieu_ref=False)
report['snapshot_blob_path_pairs']=len(leases)
old='mutant-khong-chay-tren-windows-exec-1-claude-20260906'
report['predecessors']=[{k:r[k] for k in ['ref','path','blob']}|dict(tombstone=r['lease'].get('da_bi_thay_the'),status=L._phan_loai_lease(r['lease']),bidirectional=L._bia_mo_doi_xung(r['lease'],leases)) for r in leases if r['lease'].get('lease_id')==old]
report['holders']={}
for timestamp in [report['utc'],'2026-09-07T14:30:06+00:00','2026-09-07T14:30:07+00:00']:
    report['holders'][timestamp]={p:sorted({r['lease']['lease_id'] for r in leases if L._lease_cham_duong(r['lease'],p) and L._phan_loai_lease(r['lease'],dt.datetime.fromisoformat(timestamp))=='CÒN_HẠN' and L._bia_mo_doi_xung(r['lease'],leases) is not True}) for p in ['.github/workflows/ci.yml','.claude/dev/ci_dang_ky_test.py','.claude/hooks/subagent_ghi_detect_test.py','ops/nhanh_don_duoc_test.py']}
# Countermodel: only master acquires the PR tree; the old GATE branch stays put.
# No ref is created or mutated; use the production classification functions.
master_rows=[dict(r,ref='refs/remotes/origin/master') for r in leases if r['ref'].startswith('refs/heads/')]
merged_model=leases+master_rows
report['only_master_updated_model']={p:sorted({r['lease']['lease_id'] for r in merged_model if L._lease_cham_duong(r['lease'],p) and L._phan_loai_lease(r['lease'])=='CÒN_HẠN' and L._bia_mo_doi_xung(r['lease'],merged_model) is not True}) for p in ['.github/workflows/ci.yml','.claude/dev/ci_dang_ky_test.py']}
receipt=ROOT/'ops/reviews/pr468-hoso-4-packet-review-6-codex-verdict.receipt.yaml'
d=yaml.safe_load(receipt.read_text()); v=ROOT/d['verdict_path']
report['receipt'] = dict(schema=d['schema_version'], reviewed_sha=d['reviewed_sha'], verdict=d['verdict'], actual_bytes=len(v.read_bytes()), declared_bytes=d['verdict_bytes'], actual_sha256=sha(v.read_bytes()), declared_sha256=d['verdict_sha256'], frozen_blob_matches=git('show','8c3e371:'+d['verdict_path'])==v.read_bytes(),copy_matches=receipt.read_bytes()==(BASE/'tai-lieu'/receipt.name).read_bytes())
report['artifact_missing']={n:git('ls-files', '**/'+n).decode().splitlines() for n in ['do_h.py','do_h.json','do_t2.json','law7.json','prior131.json','hint_provenance.json','buoc_master.tsv','mruns_all.tsv','MANIFEST.sha256']}
(OUT/'static.json').write_text(json.dumps(report, ensure_ascii=False,indent=2)+'\n')
for key in ['leases','gate','H_blocks','replay_files_equal','MOI','issue464_examples','predecessors','holders','receipt','artifact_missing']:
    print(key, json.dumps(report[key],ensure_ascii=False))
print('d9',json.dumps({k:{a:b for a,b in v.items() if a!='text'} for k,v in report['d9'].items()}))
