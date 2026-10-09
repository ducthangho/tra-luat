import datetime as dt, hashlib, json, pathlib, re, subprocess, sys, zipfile
import yaml
ROOT=pathlib.Path('/tmp/claude-0/-home-user-tra-luat/0682048d-075d-5414-b3ff-642b89411167/scratchpad/rc1')
RAW=pathlib.Path('/tmp/do650'); P=ROOT/'ops/land/pr666-wp650-provenance'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],cwd=ROOT)
class Unique(yaml.SafeLoader): pass
def mapping(loader,node,deep=False):
    loader.flatten_mapping(node); out={}
    for k,v in node.value:
        key=loader.construct_object(k,deep=deep)
        if key in out: raise ValueError('duplicate key '+str(key)+' line '+str(k.start_mark.line+1))
        out[key]=loader.construct_object(v,deep=deep)
    return out
Unique.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
ys={}
for name in ['pr666-wp650-provenance.yaml','pr666-wp650-land-evidence.yaml']:
    b=(ROOT/'ops/land'/name).read_bytes(); ys[name]=yaml.load(b,Loader=Unique)
    print('YAML_UNIQUE',name,sha(b))
try: yaml.load('a: 1\na: 2\n',Loader=Unique)
except ValueError as e: print('YAML_NEGATIVE',str(e))
else: raise AssertionError('duplicate accepted')
v=ys['pr666-wp650-provenance.yaml']; land=ys['pr666-wp650-land-evidence.yaml']
rawmap={'readback-rules-branches-master.json':'rules.json','readback-ruleset-20856202.json':'ruleset.json','readback-branches-master.json':'branch.json','readback-commit-511612f.json':'c511.json','artifact-10956094584-tl-selftest-Linux.json':'art/tl-selftest-Linux.json'}
for kind in ('run','jobs'):
    for rid in (36379712476,36387278453,36387278424): rawmap[f'readback-{kind}-{rid}.json']=f'{kind}-{rid}.json'
for name,raw in rawmap.items():
    a=(P/name).read_bytes(); b=(RAW/raw).read_bytes(); assert a==b,(name,'bytes differ')
    print('RAW_BYTE_EXACT',name,sha(a))
for c in ('ceb1a3f','bf63bb1','511612f','f8a7829','3fee59e'):
    print('GIT',git('show','-s','--format=%H %T %P %cI',c).decode().strip())
merge=git('show','-s','--format=%H%n%T%n%P%n%cI','f8a7829').decode().splitlines()
assert (land['merge_commit'],land['tree'],land['hai_cha'])==tuple(merge[:3])
assert dt.datetime.fromisoformat(land['merged_at'])==dt.datetime.fromisoformat(merge[3])
assert land['authorized_head_sha']==land['merge_api_expected_head_sha']==merge[2].split()[1]
assert git('rev-parse','bf63bb1^{tree}').decode().strip()==land['tree']
assert (dt.datetime.fromisoformat(land['authorization_thu_tu_thoi_gian']['merged_at'])-dt.datetime.fromisoformat(land['authorization_thu_tu_thoi_gian']['comment_updated_at'])).total_seconds()==36
spec='ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md'
assert sha((ROOT/spec).read_bytes())==land['input_packet_generations'][0]['spec_sha256']
assert git('show','0fc9766:'+spec)==(ROOT/spec).read_bytes()
lease=yaml.load((ROOT/'ops/leases/c1a1a-exec-2-claude-20260927.yaml').read_bytes(),Loader=Unique)
for k in ('revision','generation','lease_id'): assert land['input_packet_generations'][0][k]==lease[k]
print('LAND_MERGE_SPEC_LEASE','MATCH; authorization time delta 36s (timestamps supplied, not independently fetched)')
for entry in v['bon_moc']:
    r=entry['run']; rid=r['id']; raw=json.loads((P/f'readback-run-{rid}.json').read_text())
    for k in ('id','event','head_sha','path','conclusion'): assert r[k]==raw[k],(rid,k)
    assert r['attempt']==raw['run_attempt']==1; assert r['repo']==raw['repository']['full_name']
    jraw=json.loads((P/f'readback-jobs-{rid}.json').read_text()); assert jraw['total_count']==len(jraw['jobs'])
    jmap={j['id']:j for j in jraw['jobs']}
    c=entry['checkout']; sha_c=git('rev-parse',c['sha']).decode().strip()
    assert git('rev-parse',sha_c+'^{tree}').decode().strip()==c['tree']
    assert git('show','-s','--format=%P',sha_c).decode().split()==c['parents']
    print('RUN_CHECKOUT',rid,r['event'],r['head_sha'],'actual',sha_c,'parents/tree MATCH')
    for g in entry['gate_output']:
        j=jmap[g['id']]; assert j['name']==g['job']; assert j['run_id']==rid and j['run_attempt']==1
        assert j['head_sha']==r['head_sha']; assert j['conclusion']=='success'
        log=(RAW/f"log-{g['id']}.txt").read_text(); lines=log.splitlines()
        checkout=[lines[i+1].split('Z ',1)[1] for i,x in enumerate(lines[:-1]) if '[command]' in x and x.endswith(' log -1 --format=%H')]
        assert checkout==[sha_c],(g['id'],checkout)
        skipped=[s['name'] for s in j['steps'] if s['conclusion']=='skipped']
        non=[s['name'] for s in j['steps'] if s['conclusion'] not in ('success','skipped')]
        assert non==g['steps_non_success']==[]
        assert (skipped==g['steps_skipped']) if isinstance(g['steps_skipped'],list) else (len(skipped)==g['steps_skipped'])
        marker=g['marker'].replace(' (positive_verified: true)','')
        marker_lines=[i+1 for i,x in enumerate(lines) if marker in x]
        assert marker_lines,(g['id'],marker)
        if 'runner' in g: assert j['runner_name']==g['runner']
        if isinstance(g['artifact'],str):
            prefix=re.search(r'sha256 ([0-9a-f]+)',g['artifact']).group(1)
            assert sha((RAW/f"log-{g['id']}.txt").read_bytes()).startswith(prefix)
        print('JOB',g['id'],j['name'],'runner='+j['runner_name'],'checkout='+checkout[0], 'marker_lines='+str(marker_lines),'skipped='+str(len(skipped)))
    w=entry['workflow_definition']; assert w['path']==r['path']
    for c in ('ceb1a3f','bf63bb1','511612f','f8a7829'):
        blob=git('rev-parse',c+':'+w['path']).decode().strip(); b=git('show',c+':'+w['path'])
        assert blob==w['blob']; assert sha(b)==w['sha256']
    print('WORKFLOW_BYTES_4_COMMITS',w['path'],w['blob'],w['sha256'])
for short,path in [('6f2b0f9','.github/workflows/ci.yml'),('f568e34','.github/workflows/launcher-windows.yml')]:
    for c in ('ceb1a3f','bf63bb1','511612f','f8a7829'):
        p=subprocess.run(['git','merge-base','--is-ancestor',short,c],cwd=ROOT); assert p.returncode==0
        assert git('log','-1','--format=%H',c,'--',path).decode().startswith(short)
    print('LATEST_WORKFLOW_ANCESTOR',git('show','-s','--format=%H %aI',short).decode().strip(),path)
synthetic=json.loads((P/'readback-commit-511612f.json').read_text()); c=v['bon_moc'][0]['checkout']
assert synthetic['sha']==c['sha'] and synthetic['tree']['sha']==c['tree'] and [p['sha'] for p in synthetic['parents']]==c['parents']
rules=json.loads((P/'readback-rules-branches-master.json').read_text()); rs=json.loads((P/'readback-ruleset-20856202.json').read_text()); branch=json.loads((P/'readback-branches-master.json').read_text()); req=v['required_contexts']
params=next(x for x in rules if x['type']=='required_status_checks')['parameters']
assert params==next(x for x in rs['rules'] if x['type']=='required_status_checks')['parameters']
assert params['required_status_checks']==req['required_status_checks']
assert params['strict_required_status_checks_policy']==req['strict_required_status_checks_policy']
for k in ('id','name','enforcement','bypass_actors','updated_at'): assert rs[k]==req['ruleset'][k]
assert rs['conditions']['ref_name']['include']==[req['ruleset']['target']]
assert rs['conditions']['ref_name']['exclude']==[]
assert {x['ruleset_id'] for x in rules}=={rs['id']}
assert branch['protected'] and branch['protection']['required_status_checks']=={'enforcement_level':'off','contexts':[],'checks':[]}
assert branch['commit']['sha']==git('rev-parse','origin/master').decode().strip()
print('REQUIRED_CONTEXTS_CURRENT',params,'classic',branch['protection']['required_status_checks'])
print('RULESET_UPDATED_AT',rs['updated_at'],'UTC',dt.datetime.fromisoformat(rs['updated_at']).astimezone(dt.timezone.utc).isoformat())
print('RULESET_HISTORY_RAW',json.loads((RAW/'hist.json').read_text()))
with zipfile.ZipFile(RAW/'art.zip') as z:
    assert sorted(z.namelist())==['tl-selftest-Linux.json','tl-selftest-Linux.out']
    for n in z.namelist(): assert z.read(n)==(RAW/'art'/n).read_bytes()
e=json.loads((RAW/'art/tl-selftest-Linux.json').read_text()); a=v['bon_moc'][1]['gate_output'][0]['artifact']; ar=json.loads((RAW/'art-36387278453.json').read_text())['artifacts'][0]
assert a['id']==ar['id']; assert a['name']==ar['name']; assert a['expires_at']==ar['expires_at']; assert a['zip_sha256']==sha((RAW/'art.zip').read_bytes())==ar['digest'].removeprefix('sha256:')
assert a['output_sha256']==e['output_sha256']==sha((RAW/'art/tl-selftest-Linux.out').read_bytes())
assert e['command']==['python','scripts/tl.py','--selftest'] and e['returncode']==0 and e['positive_verified'] is True
assert e['positive_match'].encode() in (RAW/'art/tl-selftest-Linux.out').read_bytes()
assert e['identity']==e['identity_after']; assert e['identity']['head_sha']==land['merge_commit'] and e['identity']['tree_sha']==land['tree'] and e['identity']['tracked_clean'] and e['identity']['worktree_clean']
log=(RAW/'log-108815233339.txt').read_text(); assert a['zip_sha256'] in log and str(a['id']) in log
for rid in (36379712476,36387278424):
    ar0=json.loads((RAW/f'art-{rid}.json').read_text()); assert ar0['total_count']==0 and ar0['artifacts']==[]
print('ARTIFACT_ZIP_JSON_OUTPUT','byte-exact; id=10956094584; rc=0; positive_verified=true; 1711/1711; identities stable')
print('ALL_TARGETED_FACT_ASSERTIONS_PASSED')
