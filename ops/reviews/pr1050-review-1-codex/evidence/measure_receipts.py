from pathlib import Path
import yaml,json,hashlib,subprocess,re,datetime
repo=Path('cay-kho');oid='c24875d00e93e6a98e0a0abd0837e0cbcad65d4d';lease_oid='a34b9a38cda2669f9a90958c69bb6f2faa0f4353'
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args])
def ancestry(a,b):return subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',a,b],capture_output=True).returncode
lease=yaml.safe_load(git('show',lease_oid+':ops/leases/wp1037-r1-g1-claude.yaml'))
for n in (1,2):
 base=repo/f'ops/reviews/wp1037-g1-codex-luot{n}';p=Path(str(base)+'-verdict.receipt.yaml');d=yaml.safe_load(p.read_text());r=json.loads((base/'run/run.json').read_text());v=(repo/d['verdict_path']).read_bytes();text=v.decode();m=d['model_reviewer_identity']
 print('ROUND',n,'RECEIPT_FIELDS',json.dumps(d,ensure_ascii=False,sort_keys=True))
 for k in ['packet_id','packet_issue','revision','generation','lease_id']:
  print('ROUND',n,k,'receipt=',d[k],'lease=',lease[k],'equal=',d[k]==lease[k])
 print('ROUND',n,'schema_version',d['schema_version'],'kind',d['kind'],'receipt_id_hash_suffix',d['receipt_id'].endswith(hashlib.sha256(v).hexdigest()[:8]),'luot',d['luot'])
 print('ROUND',n,'HEADS',d['reviewed_sha'],r['head'],text.splitlines()[1],'TREE',git('rev-parse',d['reviewed_sha']+'^{tree}').decode().strip(),'BASE',lease['base_sha'])
 print('ROUND',n,'VERDICT',d['verdict'],text.splitlines()[0],'counts_claim',[d[f'so_p{i}'] for i in range(4)],'counts_measured',[len(re.findall(r'^- \[P'+str(i)+r'\]',text,re.M)) for i in range(4)],'count_basis',d['so_dem_theo'],'finding_ids',d['findings_ids'])
 print('ROUND',n,'HASH',hashlib.sha256(v).hexdigest(),'hash_equal',hashlib.sha256(v).hexdigest()==d['verdict_sha256'],'bytes',len(v),'bytes_equal',len(v)==d['verdict_bytes'])
 commit,path=d['evidence_url'].split('/blob/')[1].split('/',1)
 print('ROUND',n,'EVIDENCE',commit,path,'blob_equal',git('show',commit+':'+path)==v,'ancestor_of_review_head_rc',ancestry(commit,oid),'reviewed_ancestor_of_merge_rc',ancestry(d['reviewed_sha'],d['land_merge_commit']))
 for key,rkey in [('provider','provider'),('surface','execution_surface'),('transport','transport'),('session_run_id','run_id')]:
  print('ROUND',n,'IDENTITY',key,m[key],r[rkey],'equal',m[key]==r[rkey])
 print('ROUND',n,'MODEL',r['model_phuc_vu_trang_thai'],'events',len(r['model_phuc_vu']),'served',sorted({e['model'] for e in r['model_phuc_vu']}),'requested_claim',m['model_yeu_cau'],'declared',m['model'],'declared_served',m['model_da_chay'],'evidence',m['model_evidence'],'ref_exists',(repo/m['model_evidence_ref'].split('#')[0]).is_file())
 print('ROUND',n,'EFFORT',r['effort_phuc_vu_trang_thai'],r['effort_phuc_vu'],'SANDBOX',r['sandbox_trang_thai'],r.get('sandbox_ly_do'))
 for k in ['trang_thai','ma_thoat','thoi_luong_giay','worktree_sach','prompt_sha256','lenh']:
  print('ROUND',n,'RUN',k,r[k])
 start=datetime.datetime.fromisoformat(r['bat_dau_utc']);end=datetime.datetime.fromisoformat(lease['lease_until'].replace('Z','+00:00'));begin=datetime.datetime.fromisoformat(lease['leased_at_utc'].replace('Z','+00:00'))
 print('ROUND',n,'RUN_START_IN_LEASE',begin<=start<end,'assurance',d['assurance'],'executor_provider',d['executor_provider'],'executor_lease_model',lease['model'],'executor_lease_family',lease['model_family'])
 print('ROUND',n,'CLI_VERSION_METADATA_FIELDS',[k for k in r if any(s in k.lower() for s in ['cli_version','codex_version'])],'CLI_version_in_archived_stdout_stderr',any('0.164.0' in (base/f'run/{f}.log').read_text() for f in ['stdout','stderr']))
 print('ROUND',n,'OPTIONAL_ABSENT',[k for k in ['reviewed_tree','base_sha','muc_bang_chung_model'] if k not in d])
source_sums=git('show',lease_oid+':ops/handoff/wp1037-g1-claude/SHA256SUMS').decode()
print('SOURCE_SHA256SUMS')
for line in source_sums.splitlines():
 h,f=line.split(maxsplit=1);f=f.removeprefix('./');b=git('show',lease_oid+':ops/handoff/wp1037-g1-claude/'+f)
 print(f,'OK' if hashlib.sha256(b).hexdigest()==h else 'FAIL')
print('WRITE_SET_HASH',hashlib.sha256(json.dumps(sorted(s.casefold() for s in lease['write_set']),separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),lease['write_set_hash'])
