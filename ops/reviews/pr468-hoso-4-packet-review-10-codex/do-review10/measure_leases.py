from pathlib import Path
import importlib.util, subprocess, json, datetime as dt, contextlib, io
import yaml

ROOT=Path(__file__).resolve().parents[1]; TREE=ROOT/'cay-kho'; OUT=ROOT/'do-review10'
spec=importlib.util.spec_from_file_location('review10_lease',TREE/'ops/lease_publish.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
calls=[]
def offline_git(*args,cwd=None):
    args=list(args)
    if args[:2]==['ls-remote','--heads']:
        assert args==['ls-remote','--heads','origin']
        args[-1]=str(ROOT/'kho.git')
    assert not any('https://' in x or 'ssh://' in x for x in args)
    calls.append(args)
    p=subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True,timeout=20)
    if args[:2]==['ls-remote','--heads']:
        # Mirror packaging has materialized origin/HEAD as refs/heads/HEAD.
        # The production scanner explicitly skips */HEAD. Preserve and report it
        # in the separate branch census, but align this comparator with scanner.
        p.stdout='\n'.join(line for line in p.stdout.splitlines() if not line.endswith('\trefs/heads/HEAD'))+'\n'
    return p
m.GOI_GIT=offline_git

def git(*args,root=TREE):
    p=offline_git(*args,cwd=root); assert p.returncode==0,(args,p.stderr)
    return p.stdout.strip()

def cli(args,name):
    out=io.StringIO();err=io.StringIO()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):rc=m.main(args)
    (OUT/(name+'.stdout')).write_text(out.getvalue());(OUT/(name+'.stderr')).write_text(err.getvalue())
    return {'args':args,'rc':rc,'stdout':out.getvalue(),'stderr':err.getvalue()}

now=dt.datetime.now(dt.timezone.utc)
result={'measured_at_utc':now.isoformat(),'scope':'Exact functions/main from reviewed tree; GOI_GIT rewrites ls-remote origin to sandbox kho.git and excludes materialized refs/heads/HEAD from this comparator only, matching scanner exclusion of */HEAD. Local-ref completeness and stale-branch checks otherwise enabled. HEAD retained in separate census. No server readback.'}
result['commands']={}
paths=['.claude/dev/ci_dang_ky_test.py','.github/workflows/ci.yml']
for key,path in zip(['registry','workflow'],paths):
    result['commands'][key]=cli(['ai-dang-giu',path,'--root',str(TREE)],'offline-ai-dang-giu-'+key)
leasepath='ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml'
result['commands']['check']=cli(['check',str(TREE/leasepath),'--root',str(TREE)],'lease-check')
all_leases=m._quet_lease_toan_kho(TREE,doi_chieu_ref=True,chan_nhanh_tut_sau=True)
result['blob_path_pairs']=len(all_leases)
def holders(records,instant,path):
    found=set();broken=[]
    for r in records:
        d=r['lease']
        if not m._lease_cham_duong(d,path) or m._phan_loai_lease(d,instant)!='CÒN_HẠN':continue
        tomb=m._bia_mo_doi_xung(d,records)
        if tomb is False:broken.append(d['lease_id'])
        if tomb is not True:found.add(d['lease_id'])
    return {'count':len(found),'names':sorted(found),'broken_tombstones':broken}
result['states']={t:{path:holders(all_leases,dt.datetime.fromisoformat(t),path) for path in paths}
    for t in [now.isoformat(),'2026-09-07T14:30:06+00:00','2026-09-07T14:30:07+00:00','2026-09-07T14:30:08+00:00']}
old='ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml'
blob=git('rev-parse','origin/master:'+old)
result['old456_blob']=blob
result['old456_yaml']=yaml.safe_load(git('cat-file','-p',blob))
refs=git('for-each-ref','--format=%(refname)','refs/heads',root=ROOT/'kho.git').splitlines()
matching=[];other=[]
for ref in refs:
    p=offline_git('rev-parse','--verify',ref+':'+old,cwd=ROOT/'kho.git')
    if p.returncode==0:
        oid=p.stdout.strip()
        if oid==blob:matching.append(ref.removeprefix('refs/heads/'))
        else:other.append({'ref':ref,'blob':oid})
result['snapshot_branch_count']=len(refs);result['old456_branches']=matching;result['other456_branches']=other
claimed=['master','ops/cap-lease-456','ops/cap-lease-461','claude/agents-ngoai-goi','claude/cap-nhat-trang-thai-pr-taxzax','claude/elegant-bun-cd554f','claude/priceless-volhard-329577','claude/r356-bien-nhan-cross-review','claude/tra-luat-process-review-o4d7kb']
result['branches_vs_claim']={'omitted':sorted(set(matching)-set(claimed)),'not_found':sorted(set(claimed)-set(matching))}
result['grant_history']=[]
for rev in [3,4]:
    path=f'ops/leases/gate-tach-job-cat-chi-phi-exec-1r{rev}-claude-20260906.yaml'
    commit=git('log','--diff-filter=A','--format=%H', '--',path).splitlines()[0]
    data=yaml.safe_load(git('show',commit+':'+path))
    records=[]
    for line in git('ls-tree','-r',commit,'--','ops/leases').splitlines():
        meta,p=line.split('\t');oid=meta.split()[2]
        if p.endswith(('.yaml','.yml')):
            records.append({'lease':yaml.safe_load(git('cat-file','-p',oid)),'path':p,'blob':oid,'ref':commit})
    records.append({'lease':result['old456_yaml'],'path':old,'blob':blob,'ref':'snapshot old456 branch'})
    instant=m._doc_han(data['leased_at_utc'])
    result['grant_history'].append({'revision':rev,'commit':commit,'commit_metadata':git('show','-s','--format=%H %cI %s',commit),
        'present_at_base':offline_git('cat-file','-e','0bc6e56:'+path,cwd=TREE).returncode==0,
        'leased_at_utc':data['leased_at_utc'],'expires':data['lease_expires_at_utc'],
        'lease_id':data['lease_id'],'thay_the_cho':data.get('thay_the_cho'),
        'model_scope':'grant commit tree + known old456 blob; not live server state at historical instant',
        'states':{p:holders(records,instant,p) for p in paths}})
result['current_chain']=[]
for p in [TREE/old,*sorted((TREE/'ops/leases').glob('gate-tach-job-cat-chi-phi-*.yaml'))]:
    d=yaml.safe_load(p.read_text());result['current_chain'].append({k:d.get(k) for k in ['lease_id','revision','generation','thay_the_cho','da_bi_thay_the','leased_at_utc','lease_expires_at_utc']})
result['transport_git_calls']=len(calls)
(OUT/'leases.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n')
print(json.dumps({k:result[k] for k in ['measured_at_utc','blob_path_pairs','snapshot_branch_count','old456_branches','branches_vs_claim','states','grant_history']},ensure_ascii=False,indent=2,default=str))
print({k:(v['rc'],v['stdout'].splitlines()[-1:],v['stderr']) for k,v in result['commands'].items()})
