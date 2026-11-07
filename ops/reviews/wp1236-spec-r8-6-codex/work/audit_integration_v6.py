"""Integration measurements on a scratch copy of gen 1 plus the specified K7-S."""
import ast, collections, copy, hashlib, importlib.util, json, os, pathlib, re, subprocess, sys
import yaml
W=pathlib.Path(__file__).resolve().parent; R=W.parent/'repo'
sys.path.insert(0,str(W))
import gram, khoa_ast_r8 as ka, probes_r8 as probes, sinh_r8 as sinh

def git(*a,cwd=R,inp=None):
    return subprocess.run(['git',*a],cwd=cwd,input=inp,capture_output=True,check=True).stdout.decode().strip()
def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
src=git('show','508d678:ops/gate_output_doi_chieu.py')+'\n'
start=src.index('RE_ONG = re.compile'); end=src.index('\n\ndef _json_chuan',start)
src=src[:start]+ka.HANG+ka.THAM_CHIEU+src[end:]
start=src.index('def _bo_nhay('); end=src.index('def chan_k7(',start)
src=src[:start]+src[end:]
old='''            elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):
                nm.append(f"{ly}:{s['name'][:30]}")'''
new='''            elif ly := cu_phap_run(y.get("run"), y.get("shell")):
                nm.append(f"cu_phap_run:{ly}:{p['name']}:{s['name']}")'''
assert src.count(old)==1
src=src.replace(old,new)
(W/'model_gate.py').write_text(src,encoding='utf-8')
(W/'ci_provenance.py').write_bytes((R/'ops/ci_provenance.py').read_bytes())
(W/'model_test.py').write_text(git('show','508d678:ops/gate_output_doi_chieu_test.py')+'\n',encoding='utf-8')
os.environ['GATE_OUTPUT_DOI_CHIEU_GOC']=str(R)
os.environ['GATE_OUTPUT_DOI_CHIEU_MA']=str(W/'model_gate.py')
t=load('model_test',W/'model_test.py'); m=t.nap()
text,pv0=t.f_ok(); wf0=yaml.safe_load(t.ci_goc())
replacements={
 'tl selftest (co bang chung exact-identity)':'bash .github/checks/tl_selftest_bang_chung.sh\n',
 'release-bundle x2 cùng SHA-256':'bash .github/checks/release_bundle_x2.sh\n',
 'G5 manh ban kinh dot bien (#668)':'python ops/cong_cu_test.py\n',
 'lease-publish selftest (đo lại setup sau G5)':'bash ops/chay_lease_publish_test.sh\n',
 'don-nhanh selftest (chốt xoá nhánh)':'pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n',
 'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)':'bash ops/ci/gate_cgroup.sh\n'}
wf=copy.deepcopy(wf0)
for j in wf['jobs'].values():
    for b in j.get('steps',[]):
        if b.get('name') in replacements:
            b['run']=replacements[b['name']]
            if b['name']=='don-nhanh selftest (chốt xoá nhánh)': b.pop('shell',None)

def commit(wf):
    no_parent=t.commit_ci(yaml.safe_dump(wf,allow_unicode=True,sort_keys=False))
    tree=git('rev-parse',no_parent+'^{tree}',cwd=t.goc())
    return git('-c','user.name=review','-c','user.email=review@local','commit-tree',tree,'-p',t.SHA_CK,'-m','scratch fixture',cwd=t.goc())
def prov(wf):
    p=copy.deepcopy(pv0); sha=commit(wf)
    for c in p['moc']['checkout']: c['sha']=sha
    return p
p=prov(wf)
results={'F_ok':m.kiem(text,p,t.goc()),'F_ok_goc':m.kiem(text,pv0,t.goc())}
# Independent expectation from the workflow blob read at the provenance checkout.
def expected_pairs(p):
    ck={x['sha'] for x in p['moc']['checkout'] if x.get('trang_thai')=='passed'}; assert len(ck)==1
    source=git('show',next(iter(ck))+':.github/workflows/ci.yml',cwd=t.goc())
    w=yaml.safe_load(source); out=[]
    for j in p['moc']['gate_output']['jobs']:
        if j['conclusion']=='skipped' or 'ubuntu-latest' not in j['labels'] or j['name']=='chuan-bi': continue
        names={b['name'] for b in j['buoc'] if b['conclusion']=='success'}
        rule=m._muc(m.LUAT_v1,j['name']); assert len(rule)==1
        names &= {x for b in rule[0]['buoc'] for x in b['ten']}
        # YAML job is the leading REST name; do not use the validator's matching function.
        key=j['name'].split(' (')[0]
        out.extend((b.get('run'),b.get('shell')) for b in w['jobs'][key]['steps'] if b.get('name') in names)
    return out

def spy(p):
    f=m.cu_phap_run; seen=[]
    def record(run,shell): seen.append((run,shell)); return None
    m.cu_phap_run=record
    try: m.kiem(text,p,t.goc())
    finally: m.cu_phap_run=f
    expect=expected_pairs(p)
    return {'calls':len(seen),'expected':len(expect),'exact_multiset':collections.Counter(seen)==collections.Counter(expect)}
results['spy_F_ok']=spy(p); results['spy_F_ok_goc']=spy(pv0)
results['spy_special']=[]
for body in ka.VE_GIAN_DIEP:
    for sh in (None,'bash'):
        w=copy.deepcopy(wf); step=next(b for b in w['jobs']['gate-packet-loop']['steps'] if b.get('name')=='packet-loop selftest')
        step['run']=body
        if sh is None: step.pop('shell',None)
        else: step['shell']=sh
        pp=prov(w); result=spy(pp)
        results['spy_special'].append({'body':body,'shell':sh,**result})
# Execute every required S3b input using a real Git object and actual kiem().
corpus=[(run,sh) for body in sinh.kho() for sh in sinh.SHELL for run in (body,body+'\n')]
inputs=list(probes.AM.values())+list(probes.DUONG.values())+[v for i,v in enumerate(corpus) if i%299==0]
errors=[]
for i,(body,sh) in enumerate(inputs):
    w=copy.deepcopy(wf); step=next(b for b in w['jobs']['gate-packet-loop']['steps'] if b.get('name')=='packet-loop selftest');step['run']=body
    if sh is None: step.pop('shell',None)
    else: step['shell']=sh
    got=m.kiem(text,prov(w),t.goc()); ly=gram.cp(body,sh)
    expected=('passed',[]) if ly is None else ('not_measured',[f'cu_phap_run:{ly}:gate-packet-loop (ubuntu-latest):packet-loop selftest'])
    if got!=expected: errors.append({'i':i,'body':body,'shell':sh,'got':got,'expected':expected})
results['S3b']={'n':len(inputs),'errors':errors}
# Existing regression cases that do not depend on old shell rules.
t.f_ok=lambda:(text,copy.deepcopy(p))
results['legacy_cases']={}
for name in ('a03k_run_duong_nhanh_that','a21_pham_vi_land'):
    try: getattr(t,name)(); results['legacy_cases'][name]='passed'
    except Exception as e: results['legacy_cases'][name]=repr(e)
(W/'audit_integration_v6.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({'F_ok':results['F_ok'],'F_ok_goc_status':results['F_ok_goc'][0],'F_ok_goc_reasons':len(results['F_ok_goc'][1]),'spy_F_ok':results['spy_F_ok'],'spy_F_ok_goc':results['spy_F_ok_goc'],'special_spy_pass':sum(x['exact_multiset'] for x in results['spy_special']),'S3b':results['S3b'],'legacy_cases':results['legacy_cases']},ensure_ascii=False,indent=2))
