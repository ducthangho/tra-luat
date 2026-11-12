"""Generation 1 + literal K7-S integration MODEL, not production r8 code."""
import ast
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import types
import yaml

W = Path(__file__).resolve().parent
R = W.parent/'repo'
sys.path.insert(0,str(W))
with contextlib.redirect_stdout(io.StringIO()):
    import audit_s0 as audit

def git(*args,cwd=R,data=None):
    return subprocess.check_output(['git',*args],cwd=cwd,input=data).decode().strip()

raw = git('show','508d678:ops/gate_output_doi_chieu.py')
raw = raw.replace('Path(__file__).with_name("ci_provenance.py")',repr(str(R/'ops/ci_provenance.py')))
old = 'elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):\n                nm.append(f"{ly}:{s[\'name\'][:30]}")'
new = 'elif ly := cu_phap_run(y.get("run"), y.get("shell")):\n                nm.append(f"cu_phap_run:{ly}:{p[\'name\']}:{s[\'name\']}")'
assert raw.count(old)==1
raw=raw.replace(old,new)
lines=raw.splitlines(keepends=True)
remove=set()
for node in ast.parse(raw).body:
    name = node.name if isinstance(node,ast.FunctionDef) else getattr(node.targets[0],'id',None) if isinstance(node,ast.Assign) else None
    if name in {'RE_ONG','RE_TAT_TUY_CHON','RE_CAU_TRUC_SHELL','_bo_nhay','che_do_shell'}:
        remove.update(range(node.lineno-1,node.end_lineno))
raw=''.join(line for i,line in enumerate(lines) if i not in remove)
base=raw+'\n'+audit.core
target='            y, lb = wf["jobs"][k]["steps"][sy[0]], ten_luat.get(s["name"])\n'
assert base.count(target)==1
caller=base.replace(target,target+'            y = dict(y)\n            if type(y.get("run")) is str:\n                y["run"] = unicodedata.normalize("NFC", y["run"])\n')+'\nimport unicodedata\n'
sources={'baseline':base,'rebound_callable':base+audit.normalise,'normalised_step':caller}
mods={}
out={'model':'generation1 + literal K7-S, not an r8 implementation','A14_S0':{}}
for name,src in sources.items():
    mods[name],clauses=audit.check(src)
    (W/('full_'+name+'.py')).write_text(src)
    assert all(clauses), (name,clauses)
    out['A14_S0'][name]=clauses

test=types.ModuleType('fixture_generation1')
test.__file__=str(W/'fixture_generation1.py')
os.environ['GATE_OUTPUT_DOI_CHIEU_GOC']=str(R)
test_src=git('show','508d678:ops/gate_output_doi_chieu_test.py')
exec(compile(test_src,test.__file__,'exec'),vars(test))
test.MA=W/'full_baseline.py'
goc=test.goc()

def commit(wf):
    blob=git('hash-object','-w','--stdin',cwd=goc,data=yaml.safe_dump(wf,allow_unicode=True,sort_keys=False).encode())
    tree=git('mktree',cwd=goc,data=f'100644 blob {blob}\tci.yml\n'.encode())
    tree=git('mktree',cwd=goc,data=f'040000 tree {tree}\tworkflows\n'.encode())
    tree=git('mktree',cwd=goc,data=f'040000 tree {tree}\t.github\n'.encode())
    return git('-c','user.name=review','-c','user.email=review@local','commit-tree',tree,'-p',test.SHA_CK,'-m','scratch fixture',cwd=goc)

wf=yaml.safe_load(test.ci_goc())
rewrite={
    'tl selftest (co bang chung exact-identity)':'bash .github/checks/tl_selftest_bang_chung.sh\n',
    'release-bundle x2 cùng SHA-256':'bash .github/checks/release_bundle_x2.sh\n',
    'G5 manh ban kinh dot bien (#668)':'python ops/cong_cu_test.py\n',
    'lease-publish selftest (đo lại setup sau G5)':'bash ops/chay_lease_publish_test.sh\n',
    'don-nhanh selftest (chốt xoá nhánh)':'pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n',
    'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)':'bash ops/ci/gate_cgroup.sh\n',
}
for j in wf['jobs'].values():
    for step in j['steps']:
        if step.get('name') in rewrite:
            step['run']=rewrite[step['name']]
            if step['name'].startswith('don-nhanh'):step.pop('shell')
sha=commit(wf)
text,original=test.f_ok()
p=copy.deepcopy(original)
for c in p['moc']['checkout']:c['sha']=sha
out['F_ok']={n:m.kiem(text,p,goc) for n,m in mods.items()}
out['F_ok_goc']=mods['baseline'].kiem(text,original,goc)
assert all(v==('passed',[]) for v in out['F_ok'].values())
assert out['F_ok_goc'][0]=='not_measured' and len(out['F_ok_goc'][1])==13

def changed(run,shell):
    change=copy.deepcopy(wf)
    step=next(s for s in change['jobs']['gate-packet-loop']['steps'] if s.get('name')=='packet-loop selftest')
    step['run']=run
    if shell is None:step.pop('shell',None)
    else:step['shell']=shell
    q=copy.deepcopy(p)
    ck=commit(change)
    for c in q['moc']['checkout']:c['sha']=ck
    return q

sample=audit.corpus[::300]+[audit.probes_r8.AM[n] for n in ('g_bom_dau','g_python_hoa','g_hoac_hai_cham')]
out['S3b_sample_n']=len(sample)
out['S3b_mismatches']={n:0 for n in mods}
for run,shell in sample:
    q=changed(run,shell)
    reason=audit.gram.cp(run,shell)
    expected=('passed',[]) if reason is None else ('not_measured',[f'cu_phap_run:{reason}:gate-packet-loop (ubuntu-latest):packet-loop selftest'])
    for n,m in mods.items():out['S3b_mismatches'][n]+=m.kiem(text,q,goc)!=expected
assert not any(out['S3b_mismatches'].values())
out['witness_run']=audit.witness
q=changed(audit.witness,None)
out['witness']={n:m.kiem(text,q,goc) for n,m in mods.items()}
assert out['witness']['baseline'][0]=='not_measured'
assert all(out['witness'][n]==('passed',[]) for n in ('rebound_callable','normalised_step'))

test.nap=lambda:mods['baseline']
test.kq=lambda txt,pv,g=None:mods['baseline'].kiem(txt,pv,g or goc)
test.f_ok=lambda:(text,copy.deepcopy(p))
out['existing_cases']={}
for name in ('a03k_run_duong_nhanh_that','a20_so_luat','a21_pham_vi_land'):
    test.__dict__[name]()
    out['existing_cases'][name]='passed'

original_wf=yaml.safe_load(test.ci_goc())
a15=[]
module=mods['baseline']
for job in original['moc']['gate_output']['jobs']:
    if job['conclusion']=='skipped' or 'ubuntu-latest' not in job['labels'] or job['name']=='chuan-bi':continue
    rule=module._muc(module.LUAT_v1,job['name'])[0]
    key=module.cp.ghep_job(job['name'],original_wf)
    for step in rule['buoc']:
        actual=[b for b in job['buoc'] if b['name'] in step['ten'] and b['conclusion']=='success']
        assert len(actual)==1
        matches=[s for s in original_wf['jobs'][key]['steps'] if module.cp.ten_du_kien(s)==actual[0]['name']]
        assert len(matches)==1
        s=matches[0]
        a15.append((actual[0]['name'],audit.gram.cp(s.get('run'),s.get('shell'))))
out['A15']={'pairs':len(a15),'accepted_pairs':sum(r is None for _,r in a15),'names':len(set(a15)),
            'accepted_names':len({n for n,r in a15 if r is None})}
(W/'audit_integration.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
