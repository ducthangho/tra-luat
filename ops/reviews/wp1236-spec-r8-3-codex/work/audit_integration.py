"""Review model: gen1 with only the specified K7-S call substituted; not r8 implementation."""
import ast, copy, importlib.util, json, os, re, subprocess, sys, tempfile, types
from pathlib import Path
import yaml
W = Path(__file__).resolve().parent; R = W.parent/'repo'
sys.dont_write_bytecode = True
os.environ['TMPDIR'] = str(W/'tmp'); tempfile.tempdir = str(W/'tmp')
os.environ['GATE_OUTPUT_DOI_CHIEU_GOC'] = str(R)
sys.path[:0] = [str(W), str(W/'reference')]
import gram
import gate_output_doi_chieu_test as t
src = (W/'gate_output_doi_chieu.py').read_text()
old = '''elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):
                nm.append(f"{ly}:{s['name'][:30]}")'''
new = '''elif ly := cu_phap_run(y.get("run"), y.get("shell")):
                nm.append(f"cu_phap_run:{ly}:{p['name']}:{s['name']}")'''
assert src.count(old) == 1
model_source = src.replace(old, new)
def module(source=model_source):
    mod = types.ModuleType('review_r8_model'); mod.__file__ = str(W/'gate_output_doi_chieu.py')
    exec(compile(source, mod.__file__, 'exec'), mod.__dict__)
    mod.cu_phap_run = gram.cp
    return mod
m = module()
g = t.goc()
base = t.SHA_CK
def commit(wf):
    env = dict(os.environ, GIT_INDEX_FILE=str(W/'tmp/fixture-index'))
    def git(*args, data=None):
        return subprocess.check_output(['git','-C',str(g),*args], input=data, env=env).decode().strip()
    git('read-tree', base)
    blob = git('hash-object','-w','--stdin',data=yaml.safe_dump(wf, allow_unicode=True, sort_keys=False).encode())
    git('update-index','--add','--cacheinfo',f'100644,{blob},.github/workflows/ci.yml')
    tree = git('write-tree')
    return git('-c','user.name=Review fixture','-c','user.email=review@example.invalid',
               'commit-tree',tree,'-p',base,'-m','Review fixture child')
wf0 = yaml.safe_load(t.ci_goc()); wf = copy.deepcopy(wf0)
changes = {
 'tl selftest (co bang chung exact-identity)': 'bash .github/checks/tl_selftest_bang_chung.sh\n',
 'release-bundle x2 cùng SHA-256': 'bash .github/checks/release_bundle_x2.sh\n',
 'G5 manh ban kinh dot bien (#668)': 'python ops/cong_cu_test.py\n',
 'lease-publish selftest (đo lại setup sau G5)': 'bash ops/chay_lease_publish_test.sh\n',
 'don-nhanh selftest (chốt xoá nhánh)': 'pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n',
 'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)': 'bash ops/ci/gate_cgroup.sh\n'}
changed = []
for k,job in wf['jobs'].items():
    for i,s in enumerate(job.get('steps', [])):
        if s.get('name') in changes:
            changed.append(s['name']); s['run'] = changes[s['name']]
            if s['name'].startswith('don-nhanh selftest'): s.pop('shell')
            oldstep = wf0['jobs'][k]['steps'][i]
            ignore = {'run','shell'} if s['name'].startswith('don-nhanh selftest') else {'run'}
            assert {x:y for x,y in s.items() if x not in ignore} == {x:y for x,y in oldstep.items() if x not in ignore}
assert len(changed) == 6
sha = commit(wf)
text,p0=t.f_ok(); p=copy.deepcopy(p0)
for c in p['moc']['checkout']: c['sha']=sha
assert p['moc']['run']['head_sha'] == base
assert t.git('rev-parse',sha+'^',cwd=g) == base
assert t.git('diff-tree','--no-commit-id','--name-only','-r',sha,cwd=g) == '.github/workflows/ci.yml'
ok=m.kiem(text,p,g); original=m.kiem(text,p0,g)
assert ok == ('passed',[]),ok
assert original[0]=='not_measured' and len(original[1])==13 and all(x.startswith('cu_phap_run:') for x in original[1]),original
result={'model':'gen1 + reference K7-S call, not r8 implementation', 'F_ok':ok,'F_ok_original':original,
 'fixture_child':sha, 'fixture_parent':base, 'checkout_count':len(p['moc']['checkout'])}
def variant(run, shell):
    w=copy.deepcopy(wf)
    s=next(s for s in w['jobs']['gate-packet-loop']['steps'] if s.get('name')=='packet-loop selftest')
    s['run']=run
    if shell is None: s.pop('shell',None)
    else: s['shell']=shell
    pp=copy.deepcopy(p); ss=commit(w)
    for c in pp['moc']['checkout']: c['sha']=ss
    return pp
pipeline='python .claude/dev/packet_loop_test.py | python ops/tee_test.py'
result['A14_i']=m.kiem(text,variant(pipeline,'bash'),g)
result['A14_i_prime']=m.kiem(text,variant(pipeline,None),g)
assert result['A14_i']==('passed',[])
assert result['A14_i_prime']==('not_measured',['cu_phap_run:ong_khong_bash_tuong_minh:gate-packet-loop (ubuntu-latest):packet-loop selftest'])
bad=variant('python ops/hong_test.py','zsh')
result['A14_c']=m.kiem(text,bad,g)
mut20=module(model_source.replace('elif ly := cu_phap_run(y.get("run"), y.get("shell")):', 'if ly := cu_phap_run(y.get("run"), y.get("shell")):'))
result['m_S20']=mut20.kiem(text,bad,g)
assert len(result['A14_c'][1])==1 and len(result['m_S20'][1])==2
mut16=module(); mut16.cu_phap_run=lambda run,shell:None
result['m_S16']=mut16.kiem(text,p0,g); assert result['m_S16']==('passed',[])
mut15=module(); mut15.cu_phap_run=mut15.che_do_shell
result['m_A15c']=mut15.kiem(text,p0,g); assert result['m_A15c']==('passed',[])
from probes_r8 import AM
result['A14_S3']=[]
for key in ('l9_05_hoac_hoac','l8_10_set_sau_ong'):
    run,shell=AM[key]; pp=variant(run,'bash' if key.startswith('l8') else shell)
    got=m.kiem(text,pp,g); removed=mut16.kiem(text,pp,g)
    assert got==('not_measured',['cu_phap_run:lenh_ngoai_cu_phap:gate-packet-loop (ubuntu-latest):packet-loop selftest'])
    assert removed==('passed',[])
    result['A14_S3'].append((key,got,removed))
result['G1_cases_through_kiem']=[]
CMD='python .claude/dev/packet_loop_test.py'; PIPE=CMD+' | cat'
for f in ('rv-a1-8/work/probes.py','rv-a1-9/work/extra_shell_probes.py'):
    path=W/'reference/g1'/f
    cases=next(eval(compile(ast.Expression(n.value),str(path),'eval'),{'CMD':CMD,'PIPE':PIPE})
        for n in ast.walk(ast.parse(path.read_text())) if isinstance(n,ast.Assign) and getattr(n.targets[0],'id',None)=='cases')
    got=[]
    for row in cases:
        name,shell,run=row[:3] if 'a1-8' in f else (row[0],row[2],row[1])
        status,why=m.kiem(text,variant(run+'\n',shell),g)
        assert status=='not_measured' and any(x.startswith(('cu_phap_run:', 'che_do_khong_xac_dinh:')) for x in why),(name,status,why)
        got.append(name)
    result['G1_cases_through_kiem'].append((f,len(got)))

def ledger(mod,case):
    law=copy.deepcopy(mod.LUAT_v1)
    if case=='f': law['JOB_BAT_BUOC'].append(law['JOB_BAT_BUOC'][0])
    if case=='g': law['JOB_BAT_BUOC'].remove(mod.CHECK_BAT_BUOC[0])
    if case=='h': law['JOB_BAT_BUOC'].append('unmatched (ubuntu-latest)')
    if case=='i': law['MUC'].append(copy.deepcopy(law['MUC'][0]))
    if case=='i_prime':
        oldlaw=copy.deepcopy(law);oldlaw['JOB_BAT_BUOC'].remove(mod.CHECK_BAT_BUOC[0])
        oldkey=mod.bam(oldlaw); key=mod.bam(law)
        mod.LUAT_PHIEN_BAN={oldkey:oldlaw,key:law};mod.MIEN_HIEU_LUC={oldkey:(1,5),key:(6,None)}
    else:
        key=mod.bam(law); mod.LUAT_PHIEN_BAN={key:law};mod.MIEN_HIEU_LUC={key:(1,None)}
    return mod
mutations={
 'f':('(len(ds) != len(set(ds)))','False'),
 'g':('not set(CHECK_BAT_BUOC) <= set(ds)','False'),
 'h':('len(_muc(v, t)) != 1','len(_muc(v, t)) > 1'),
 'i':('len(_muc(v, t)) != 1','len(_muc(v, t)) < 1'),
 'i_prime':('MIEN_HIEU_LUC.get(k, (0, 0))[1] is None and','True and')}
result['A20']={}
for case,(before,after) in mutations.items():
    assert model_source.count(before)==1,(case,model_source.count(before))
    regular=ledger(module(),case); mutant=ledger(module(model_source.replace(before,after)),case)
    a=regular.kiem_so_luat(); b=mutant.kiem_so_luat()
    a_api=regular.kiem(text,p,g);b_api=mutant.kiem(text,p,g)
    assert bool(a)!=bool(b),(case,a,b)
    assert ('so_luat_hong' in a_api[1]) != ('so_luat_hong' in b_api[1]),(case,a_api,b_api)
    result['A20'][case]={'baseline':a,'mutant':b,'baseline_kiem':a_api[0:1]+(a_api[1][:2],),'mutant_kiem':b_api[0:1]+(b_api[1][:2],)}
print(json.dumps(result,ensure_ascii=False,indent=2))
(W/'integration.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
