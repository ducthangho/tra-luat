import datetime as dt, hashlib, importlib.util, json, pathlib, re, subprocess, sys, yaml, copy
B=pathlib.Path(__file__).resolve().parents[1]; R=B/'cay-kho'; O=B/'do-review9'; sys.dont_write_bytecode=True
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
report={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'initial_status':git('status','--porcelain').decode()}
report['diffs']={}
for key,rev,patch,num in [('since8','4d0ead5','diff-tu-luot8.patch','numstat-tu-luot8.txt'),('full','origin/master','diff.patch','numstat.txt')]:
 raw=git('diff',rev,'HEAD'); nums=git('diff','--numstat',rev,'HEAD'); lines=[v.split('\t') for v in nums.decode().splitlines()]
 report['diffs'][key]=dict(patch_matches=raw==(B/patch).read_bytes(),numstat_matches=nums==(B/num).read_bytes(),files=len(lines),additions=sum(int(x[0]) for x in lines if x[0].isdigit()),deletions=sum(int(x[1]) for x in lines if x[1].isdigit()),outside_ops=[x[2] for x in lines if not x[2].startswith('ops/')])
report['leases']=[]
for issueid in [463,464,465,466]:
 issue=next((R/'ops/issues').glob(str(issueid)+'-*.md')); it=issue.read_text(); frozen=re.search(r'@ `([0-9a-f]{40})`',it).group(1)
 leasepath=next((R/'ops/leases').glob({463:'gate-tach-job-cat-chi-phi-exec-1r3',464:'lo-319-linux-bang-chung-xanh-exec-1',465:'mutant-windows-subagent-ghi-detect-exec-1',466:'mutant-windows-nhanh-don-duoc-exec-1'}[issueid]+'-claude*.yaml*'))
 d=yaml.safe_load(leasepath.read_text()); p=R/d['spec_path']; blob=git('show',frozen+':'+d['spec_path'])
 report['leases'].append(dict(issue=issueid,lease=leasepath.name,revision=d['revision'],spec=p.name,hash_actual=sha(p.read_bytes()),hash_declared=d['spec_hash'],hash_alias=d['spec_sha256'],issue_commit=frozen,issue_blob_hash=sha(blob),issue_hash=d['spec_hash'] in it,copy_equal=p.read_bytes()==(B/'tai-lieu'/p.name).read_bytes() and leasepath.read_bytes()==(B/'tai-lieu'/leasepath.name).read_bytes() and issue.read_bytes()==(B/'tai-lieu'/issue.name).read_bytes(),granted_on_instruction=d['granted_on_instruction'],null_keys=[k for k,v in d.items() if v is None],write_set=d['write_set']))
 if issueid==463:
  report['gate']=dict(anchors={k:d[k] for k in ['base_sha','start_from_sha','reviewed_sha_required']},write_set_hash_actual=sha(('\n'.join(sorted(d['write_set']))+'\n').encode()),write_set_hash_declared=d['write_set_hash'],leased=d['leased_at_utc'],heartbeat=d['heartbeat_at'],until=d['lease_until'],expires=d['lease_expires_at_utc'],duration_minutes=(dt.datetime.fromisoformat(d['lease_until'])-dt.datetime.fromisoformat(d['leased_at_utc'])).total_seconds()/60,thay_the_cho=d['thay_the_cho'])
sp=importlib.util.spec_from_file_location('lease_review9',R/'ops/lease_publish.py'); L=importlib.util.module_from_spec(sp); sp.loader.exec_module(L)
leases=L._quet_lease_toan_kho(R,doi_chieu_ref=False); report['snapshot_blob_path_pairs']=len(leases)
ids=['mutant-khong-chay-tren-windows-exec-1-claude-20260906']+['gate-tach-job-cat-chi-phi-exec-'+v+'-claude-20260906' for v in ['1','1r2','1r3']]
report['chain_snapshot']=[{k:r[k] for k in ['ref','path','blob']}|dict(lease_id=r['lease']['lease_id'],thay_the_cho=r['lease'].get('thay_the_cho'),da_bi_thay_the=r['lease'].get('da_bi_thay_the'),status=L._phan_loai_lease(r['lease']),bidirectional=L._bia_mo_doi_xung(r['lease'],leases)) for r in leases if r['lease'].get('lease_id') in ids]
local=[yaml.safe_load((R/f'ops/leases/{i}.yaml').read_text()) for i in ids]
report['chain_current_tree']=[dict(lease_id=d['lease_id'],replaces=d.get('thay_the_cho'),tombstone=d.get('da_bi_thay_the'),bidirectional=L._bia_mo_doi_xung(d,[{'lease':l} for l in local])) for d in local]
for a,b in zip(local,local[1:]): assert a['da_bi_thay_the']==b['lease_id'] and a['lease_id'] in b['thay_the_cho']
paths=['.github/workflows/ci.yml','.claude/dev/ci_dang_ky_test.py','.claude/hooks/subagent_ghi_detect_test.py','ops/nhanh_don_duoc_test.py']
def holders(rs,t):
 result={}
 for p in paths:
  hs=[]
  for r in rs:
   d=r['lease']
   if L._lease_cham_duong(d,p) and L._phan_loai_lease(d,dt.datetime.fromisoformat(t))=='CÒN_HẠN':
    bm=L._bia_mo_doi_xung(d,rs)
    assert bm is not False, (r,'one-way tombstone')
    if bm is not True:hs.append(d['lease_id'])
  result[p]=sorted(set(hs))
 return result
report['holders']={t:holders(leases,t) for t in [report['utc'],'2026-09-07T14:30:06+00:00','2026-09-07T14:30:07+00:00','2026-09-07T14:30:08+00:00']}
model=copy.deepcopy(leases)
for r in model:
 if r['lease'].get('lease_id')==ids[0]:r['lease']['da_bi_thay_the']=ids[1]
report['model_all_456_copies_tombstoned']=holders(model,report['utc'])
report['master_old_blob']=git('rev-parse',f'origin/master:ops/leases/{ids[0]}.yaml').decode().strip()
report['refs']=git('for-each-ref','--format=%(refname) %(objectname)').decode().splitlines()
report['consumer_copy_equal']=(R/'.claude/dev/ci_dang_ky_test.py').read_bytes()==(B/'tai-lieu/ci_dang_ky_test.py').read_bytes()
report['manifest']={}
for turn in [6,7,8]:
 p=R/f'ops/reviews/pr468-hoso-4-packet-review-{turn}-codex'; items=[]
 for line in (p/'ARTIFACTS.sha256').read_text().splitlines():
  wanted,rel=line.split(maxsplit=1); rel=rel.lstrip('*'); f=p/rel; f.resolve().relative_to(B)
  items.append(dict(file=rel,match=f.is_file() and sha(f.read_bytes())==wanted))
 report['manifest'][str(turn)]=dict(listed=len(items),matched=sum(x['match'] for x in items),mismatches=[x for x in items if not x['match']])
receipt=R/'ops/reviews/pr468-hoso-4-packet-review-8-codex-verdict.receipt.yaml'; d=yaml.safe_load(receipt.read_text()); raw=(R/d['verdict_path']).read_bytes(); anchor=re.search('/blob/([0-9a-f]{40})/',d['evidence_url']).group(1)
report['receipt']=dict(schema=d['schema_version'],reviewed_sha=d['reviewed_sha'],declared_bytes=d['verdict_bytes'],bytes=len(raw),declared_hash=d['verdict_sha256'],hash=sha(raw),anchor=anchor,anchor_blob_matches=git('show',anchor+':'+d['verdict_path'])==raw,copy_equal=receipt.read_bytes()==(B/'tai-lieu'/receipt.name).read_bytes(),identity_fields={k:d[k] for k in ['model_reviewer_identity','github_submitter_identity','anchor']})
(O/'static.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['refs','chain_snapshot','receipt']},ensure_ascii=False,indent=2))
