import ast, collections, datetime, hashlib, json, pathlib, re, subprocess, yaml
from harness import BASE, ROOT, OUT, module

def git(*args):
    p=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr)
    return p.stdout

def sha(b): return hashlib.sha256(b).hexdigest()
report={'measured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
leases=[]
for p in sorted((BASE/'tai-lieu').glob('*.yaml*')):
    data=yaml.safe_load(p.read_text()); spec=ROOT/data['spec_path']; src=BASE/'tai-lieu'/spec.name
    leases.append({'file':p.name,'actual_spec_sha256':sha(spec.read_bytes()),'declared_spec_sha256':data['spec_sha256'],
     'spec_hash_equals_sha':data['spec_hash']==data['spec_sha256'], 'hash_matches':sha(spec.read_bytes())==data['spec_sha256'],
     'reference_copy_matches':spec.read_bytes()==src.read_bytes(), 'write_set':data['write_set'],'depends_on':data.get('depends_on'),
     'null_fields':[k for k,v in data.items() if v is None],
     'missing_protocol32_literal':[k for k in ['schema_version','packet_id','mission_issue','revision','spec_hash','objective','write_set','depends_on','executor','environment','risk','review_class','acceptance_criteria'] if k not in data],
     'missing_protocol4_literal':[k for k in ['packet_id','executor','environment','branch','write_set_hash','generation','heartbeat_at','lease_until'] if k not in data],
     'base_sha':data['base_sha'], 'issued':str(data['leased_at_utc']),'expires':str(data['lease_expires_at_utc'])})
report['leases']=leases
report['consumer_copy_matches']=(BASE/'tai-lieu/ci_dang_ky_test.py').read_bytes()==(ROOT/'.claude/dev/ci_dang_ky_test.py').read_bytes()
report['diff_numstat']=git('diff','--numstat','d28c4b1','HEAD')
report['provided_numstat_matches']=report['diff_numstat']==(BASE/'numstat.txt').read_text()
report['diff_patch_matches']=git('diff','d28c4b1','HEAD')==(BASE/'diff.patch').read_text()
report['drift_1b_to_28_count']=int(git('rev-list','--count','1b3caa1..28cb898'))
report['diff_parent_merge_456']=git('diff','--name-only','426bfc0','1b3caa1')
report['diff_0c5e889_numstat']=git('show','--format=','--numstat','0c5e889')
report['runtime_diff_1b_e5']=git('diff','--numstat','1b3caa1','e5ab4b7','--','.claude/dev/ci_dang_ky_test.py')
report['runtime_diff_master_head']=git('diff','--numstat','d28c4b1','HEAD','--','.github/workflows/ci.yml','.claude/dev/ci_dang_ky_test.py')
report['head_refs']=len(git('for-each-ref','--format=%(refname)','refs/heads').splitlines())
report['origin_refs']=len([s for s in git('for-each-ref','--format=%(refname)','refs/remotes/origin').splitlines() if s!='refs/remotes/origin/HEAD'])
report['current_master']='KHÔNG ĐO ĐƯỢC: không có refs/heads/master hoặc refs/remotes/origin/master'; report['comparison_base']=git('rev-parse','d28c4b1').strip()
report['runtime_drift_since_lease_anchor']=git('diff','--numstat','1b3caa1','d28c4b1','--','.github/workflows/ci.yml','.claude/dev/ci_dang_ky_test.py')
report['master_ancestor_pre_issue']=git('show','-s','--format=%H %cI','d28c4b1').strip()
report['blocks']={}
empty=OUT/'empty';empty.write_text('')
for rev in ['e5ab4b7','HEAD']:
    src=git('show',rev+':ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md')
    blocks=re.findall(r'```python\n(.*?)\n```',src,re.S)
    blocks=[x for x in blocks if 'TONG = {' in x or 'def bang_chung_xanh' in x]
    sizes=[]
    for i,x in enumerate(blocks):
        file=OUT/f'block-{rev}-{i}.py';file.write_text(x+'\n')
        p=subprocess.run(['git','diff','--no-index','--numstat',str(empty),str(file)],capture_output=True,text=True)
        sizes.append({'lines':len((x+'\n').splitlines()),'numstat':p.stdout.strip(),'rc':p.returncode})
    report['blocks'][rev]=sizes
report['workflow']={}
for rev in ['1b3caa1','28cb898','HEAD']:
    source=git('show',rev+':.github/workflows/ci.yml');data=yaml.safe_load(source);steps=data['jobs']['gate']['steps']
    runs=[' '.join(x['run'].split()) for x in steps if 'run' in x]
    report['workflow'][rev]={'steps':len(steps),'ifs':sum('if' in x for x in steps),'lines':len(source.splitlines()),
      'duplicate_run_bodies':sum(n-1 for n in collections.Counter(runs).values() if n>1),'timeout':data['jobs']['gate']['timeout-minutes']}
# AST counts of literal top-level collections, avoiding running suites a second time.
report['collections']={}
for rel in ['.claude/hooks/pretooluse_guard_test.py','.claude/hooks/subagent_ghi_detect_test.py','ops/nhanh_don_duoc_test.py']:
    sizes={}
    for stmt in ast.parse((ROOT/rel).read_text()).body:
        if isinstance(stmt,ast.Assign):
            for target in stmt.targets:
                if isinstance(target,ast.Name) and target.id in ['CA','DOT_BIEN','DOT_BIEN_NHAM_TEST','DOT_BIEN_SETTINGS']:
                    sizes[target.id]=len(stmt.value.elts) if isinstance(stmt.value,(ast.List,ast.Tuple)) else ast.dump(stmt.value)[:100]
    report['collections'][rel]=sizes
# Inventory only reviewer bundle data/tree; no access to service/session transcripts.
need=['do_h.py','do_h.json','law7.json','prior131.json','hint_provenance.json','buoc_master.tsv','mruns_all.tsv','executor-luot4-va','executor-luot3-va','MANIFEST.sha256','do_t2.json','attack-h.json']
roots=[ROOT,BASE/'tai-lieu']
paths=[]
for root in roots:
    paths.extend(p for p in root.rglob('*') if '.git' not in p.relative_to(root).parts)
report['artifact_paths']={n:[str(p.relative_to(BASE)) for p in paths if p.name==n] for n in need}
L=module(ROOT/'ops/lease_publish.py','lease_review')
all_leases=L._quet_lease_toan_kho(ROOT,doi_chieu_ref=False)
report['snapshot_lease_blob_path_pairs']=len(all_leases)
old_id='mutant-khong-chay-tren-windows-exec-1-claude-20260906'
report['predecessor_blobs']=[]
for row in all_leases:
    if row['lease'].get('lease_id')==old_id:
        report['predecessor_blobs'].append({k:row[k] for k in ['ref','path','blob']}|{'tombstone':row['lease'].get('da_bi_thay_the'),
             'status':L._phan_loai_lease(row['lease']),'bidirectional':L._bia_mo_doi_xung(row['lease'],all_leases)})
report['snapshot_holders']={}
for path in ['.github/workflows/ci.yml','.claude/dev/ci_dang_ky_test.py']:
    report['snapshot_holders'][path]=sorted({row['lease']['lease_id'] for row in all_leases
        if L._lease_cham_duong(row['lease'],path) and L._phan_loai_lease(row['lease'])=='CÒN_HẠN' and L._bia_mo_doi_xung(row['lease'],all_leases) is not True})
(OUT/'static-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
