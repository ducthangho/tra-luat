import collections, hashlib, importlib.util, json, pathlib, re, subprocess, sys, time
import yaml
W=pathlib.Path(__file__).resolve().parent; R=W.parent/'repo'; sys.path.insert(0,str(W))
import gram, sinh_r8, dot_bien_r8

def git(*args): return subprocess.check_output(['git','-C',str(R),*args])
sp=importlib.util.spec_from_file_location('model_counts',W/'model_gate.py'); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
corpus=[(run,sh) for body in sinh_r8.kho() for sh in sinh_r8.SHELL for run in (body,body+'\n')]
expected=[gram.cp(*x) for x in corpus]
counts={name:sum(f(*x)!=answer for x,answer in zip(corpus,expected)) for name,f in dot_bien_r8.DB_SINH.items()}
results={'mutants':{'n':len(counts),'killed':sum(x>0 for x in counts.values()),'min':min(counts.values()),'max':max(counts.values())}}
results['g1_hashes']={}
for sha,file in re.findall(r'^([a-f0-9]{64})  (.+)$',(W/'g1/README.md').read_text(),re.M): results['g1_hashes'][file]=hashlib.sha256((W/'g1'/file).read_bytes()).hexdigest()==sha
results['provenance']={}
for ref in ('b796259','d26b36f'):
    paths=git('ls-tree','-r','--name-only',ref,'--','ops/land').decode().splitlines()
    rows=[]
    for path in paths:
        if not path.endswith(('.yaml','.yml')) or 'provenance' not in path:continue
        b=git('show',f'{ref}:{path}')
        if b'ci_provenance/1' not in b:continue
        d=yaml.safe_load(b)
        if type(d) is dict and d.get('schema')=='ci_provenance/1': rows.append((path,d))
    checkout_mismatch=[]; blobs=[]; jobs=[]; runs=[]
    for path,d in rows:
        run=d['moc']['run']; co=d['moc'].get('checkout',[])
        checkout_mismatch.extend([path] if any(c.get('trang_thai')=='passed' and c.get('sha')!=run.get('head_sha') for c in co) else [])
        wf=d['moc'].get('workflow_definition',{})
        if wf.get('trang_thai')=='passed':
            sha=next(c['sha'] for c in co if c.get('trang_thai')=='passed')
            blob=git('rev-parse',sha+':'+run['loi_khai_rest_path']).decode().strip()
            blobs.append(blob==wf.get('blob'))
        if run.get('event')=='push' and run.get('loi_khai_rest_path')=='.github/workflows/ci.yml':
            jj=[j['name'] for j in d['moc']['gate_output']['jobs'] if j.get('conclusion')!='skipped' and 'ubuntu-latest' in (j.get('labels') or []) and j.get('name')!='chuan-bi']
            jobs.append(set(jj)==set(m.LUAT_v1['JOB_BAT_BUOC'])); runs.append(run['run_id'])
    results['provenance'][ref]={'files':len(rows),'checkout_mismatch':checkout_mismatch,'blobs':len(blobs),'blobs_match':sum(blobs),'jobs':len(jobs),'jobs_match':sum(jobs),'earliest_run':min(runs)}
for adr in ('0052-tran-loi-goi-codex-len-tam.md','0053-tran-kich-thuoc-sensitive-len-sau-tep.md'):
    oid='8ab100793df9831505f495543a74044b91c2c9ab'
    rc=[subprocess.run(['git','-C',str(R),'cat-file','-e',f'{prefix}:docs/adr/{adr}'],capture_output=True).returncode for prefix in (oid,oid+'^1')]
    results[adr]={'cat_file_rc':rc,'in_first_parent':oid in git('rev-list','--first-parent','origin/master').decode().splitlines()}
results['branch_outside_spec_reviews']=git('diff','--name-only','9607e3e...HEAD','--','.',':!ops/specs/**',':!ops/reviews/**').decode().strip()
results['gen1_numstat']=git('diff','--numstat','d26b36f...508d678','--','ops/gate_output_doi_chieu.py','ops/gate_output_doi_chieu_test.py','.claude/dev/ci_dang_ky_test.py').decode()
# Count the current proposal's five groups by their explicitly listed members.
results['K7S_mutants_current']=53+91+8+6+6+3
results['K7S_mutants_in_can_cu']=164
results['mutant_counts']=counts
(W/'audit_counts_v6.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in results.items() if k!='mutant_counts'},ensure_ascii=False,indent=2))
