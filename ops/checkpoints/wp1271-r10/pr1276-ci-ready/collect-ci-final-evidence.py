import pathlib,sys,subprocess,json,hashlib,zipfile,re,datetime,importlib.util
S=pathlib.Path('/workspace/scratch/proxima-p1-s1-20261107');R=pathlib.Path('/workspace/scratch/wp1271-spec-publish');run=int(sys.argv[1]);H=sys.argv[2];D=S/sys.argv[3];logs=S/sys.argv[4];D.mkdir(exist_ok=False);GH='/workspace/scratch/proxima-p0-tools/gh';repo='ducthangho/tra-luat'
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(ep,n,pages=False):
 b=subprocess.check_output([GH,'api']+(['--paginate','--slurp'] if pages else [])+[ep]);(D/n).write_bytes(b);return json.loads(b)
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
sp=importlib.util.spec_from_file_location('cp',R/'ops/ci_provenance.py');cp=importlib.util.module_from_spec(sp);sp.loader.exec_module(cp)
r=fetch(f'repos/{repo}/actions/runs/{run}','run.json');assert r['head_sha']==H and r['status']=='completed' and r['conclusion']=='success'
j=fetch(f'repos/{repo}/actions/runs/{run}/attempts/{r["run_attempt"]}/jobs?per_page=100','jobs-pages.json',True);jobs=[x for p in j for x in p['jobs']];assert len(jobs)==j[0]['total_count'] and jobs and all(x['status']=='completed' and x['conclusion']=='success' and 'ubuntu-latest' in x['labels'] and not any('windows' in a.lower() for a in x['labels']) for x in jobs)
a=fetch(f'repos/{repo}/actions/runs/{run}/artifacts?per_page=100','artifacts-pages.json',True);arts=[x for p in a for x in p['artifacts']];assert len(arts)==a[0]['total_count']
logdir=D/'full-job-logs';logdir.mkdir();loghash={};checkouts=[];logcache={}
for job in jobs:
 p=logs/(str(job['id'])+'.json');v=json.loads(p.read_text());assert v['repository']==repo and v['job_id']==job['id'] and isinstance(v['content'],str);b=v['content'].encode('utf-8');(logdir/(str(job['id'])+'.log')).write_bytes(b);logcache[job['id']]=b
 c=cp.moc_checkout(cp.doc_sha_checkout(v['content'].splitlines()),r['event'],H,cp.git_cuc_bo);assert c['trang_thai']=='passed',(job['name'],c);checkouts.append({'job_id':job['id'],'name':job['name'],**c});loghash[str(job['id'])]={'sha256_of_received_UTF8_text':sha(b),'bytes':len(b),'source_record_sha256':sha(p.read_bytes()),'name':job['name'],'transport':'GitHub plugin decoded logs; original remote raw-byte identity not independently asserted'}
core=next(x for x in jobs if x['name']=='gate (ubuntu-latest)');lines=logcache[core['id']].decode().splitlines();tested=next(x['sha'] for x in checkouts if x['job_id']==core['id']);parents=git('show','-s','--format=%P',tested).decode().split();tree=git('rev-parse',tested+'^{tree}').decode().strip();assert all(c['sha']==tested for c in checkouts)
wd=json.loads((S/sys.argv[5]).read_text());assert wd['trang_thai']=='passed' and wd['run_id']==run and wd['run_attempt_luc_do']==r['run_attempt'] and wd['head_sha_rest']==H
blocks=cp.tach_buoc(lines);runtime=[cp.than(t) for t in lines if 'Successfully set up CPython' in t];assert runtime
artifact=None;lifecycle=None
if r['event']=='pull_request':
 assert tested!=H and H in parents and len(parents)==2
 q=[x for x in blocks if x['lenh']=='python scripts/tl.py --selftest'];assert len(q)==1 and q[0]['hop_le'];markers=re.findall(r'== tl selftest ([0-9]+)/([0-9]+) ==','\n'.join(q[0]['phan']));assert markers and markers[-1][0]==markers[-1][1] and int(markers[-1][0])>0
 st=[x for x in core['steps'] if x['name']=='tl selftest (luot PR — khong sinh bang chung)'];assert len(st)==1 and st[0]['conclusion']=='success'
 lifecycle={'status':'not_produced_by_PR_workflow_design','reason':'Exact frozen ci.yml runs direct selftest on synthetic merge and intentionally produces lifecycle artifact only for non-PR events; actual PR command/positive output/step success verified from logs, not replaced with API head.'}
else:
 assert r['event']=='push' and tested==H
 matches=[x for x in arts if x['name']=='gate-evidence-ubuntu-latest-'+str(r['run_attempt'])];assert len(matches)==1 and not matches[0]['expired'];art=matches[0];z=S/sys.argv[6];b=z.read_bytes();assert art['digest']=='sha256:'+sha(b);artifact={'id':art['id'],'name':art['name'],'sha256':sha(b),'matches_GitHub_artifact_digest':True}
 with zipfile.ZipFile(z) as zz:
  for info in zz.infolist():
   p=pathlib.PurePosixPath(info.filename);assert not p.is_absolute() and '..' not in p.parts
  zz.extractall(D/'gate-artifact')
 p=next((D/'gate-artifact').rglob('tl-selftest-Linux.json'));e=json.loads(p.read_text());out=p.with_suffix('.out').read_bytes();assert e['status']=='pass' and e['returncode']==0 and e['positive_verified'] and e['identity']==e['identity_after'];i=e['identity'];assert i['head_sha']==tested and i['tree_sha']==tree and i['system']=='Linux' and i['tracked_clean'] and i['worktree_clean'];assert e['output_sha256']==sha(out) and e['command']==['python','scripts/tl.py','--selftest'];assert e['command_sha256']==sha((json.dumps(e['command'],ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode());assert sha(git('show',tested+':.claude/dev/gate_lifecycle.py'))==i['runner_sha256']
 paths=['.claude/dev/gate_lifecycle.py','.github/workflows/ci.yml','docs/PROTOCOL_DA_PHIEN.md','docs/adr/0035-dieu-phoi-ben-vung-va-selftest-phan-tang.md','scripts/tl_selftest.py','scripts/test_fragments','scripts/tl_test_fragments_bundled.py'];rows=[]
 for line in git('ls-tree','-r',tested,'--',*paths).decode().splitlines():
  meta,path=line.split('\t');mode,kind,oid=meta.split();rows.append(f'{mode} {oid} 0\t{path}')
 assert sha('\n'.join(rows).strip().encode())==i['catalog_policy_sha256'];markers=re.findall(r'== tl selftest ([0-9]+)/([0-9]+) ==',out.decode());assert markers and markers[-1][0]==markers[-1][1] and int(markers[-1][0])>0;lifecycle={'status':'passed','identity':i,'command_hash_verified':True,'runner_code_hash_verified':True,'catalog_policy_hash_verified':True,'output_sha256':sha(out),'actual_rc':e['returncode']}
# Use the unmodified canonical provenance consumer with authenticated GitHub-plugin log text as its explicit transport adapter.
def observed_transport(url):
 m=re.fullmatch(r'https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/([0-9]+)/logs',url)
 if m:return 200,logcache[int(m[1])]
 return cp.goi_that(url)
prov,files=cp.thu(repo,run,r['run_attempt'],observed_transport,cp.git_cuc_bo);pd=D/'canonical-rest-provenance';cp.ghi_nguyen_tu(str(pd),files)
assert prov['moc']['run']['trang_thai']=='passed' and all(x['trang_thai']=='passed' for x in prov['moc']['checkout'])
assert not any(x['trang_thai']=='failed' for x in prov['moc']['gate_output']['jobs']) and prov['moc']['gate_output']['tap_jobs']['trang_thai']=='passed' and prov['moc']['gate_output']['tap_artifacts']['trang_thai']=='passed'
o={'run_id':run,'attempt':r['run_attempt'],'event':r['event'],'api_head':H,'actual_checkout':tested,'checkout_parents':parents,'actual_tree':tree,'all_jobs_Ubuntu_success':True,'jobs_total':len(jobs),'positive_output':markers[-1][0]+'/'+markers[-1][1],'runtime_observations':runtime,'lifecycle':lifecycle,'artifact':artifact,'workflow_definition':wd,'full_job_logs':loghash,'all_checkout_observations':checkouts,'four_anchors':{'run':'passed','checkout':'passed','workflow_definition':'passed','gate_output':'awaiting_mandatory_auxiliary_log_audit'},'canonical_gate_output_observations':[{k:x.get(k) for k in ['job_id','name','trang_thai','dau_duong']} for x in prov['moc']['gate_output']['jobs']],'canonical_consumer_note':'Original REST provenance workflow_definition slot remains not_measured by tool design; separate actual do-wd result supplies the fourth anchor in this derived index. No raw consumer output edited.','at':datetime.datetime.now(datetime.timezone.utc).isoformat()};(D/'validation.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({k:v for k,v in o.items() if k not in ['full_job_logs','all_checkout_observations']},indent=2))
